#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor MCP da VTurb (Analytics API) — versão otimizada.

Expõe as métricas de VSL da VTurb como ferramentas MCP para o Claude Code,
já digeridas e prontas para leitura, sem JSON cru.

Otimizações em relação à v1:
  - Busca o vídeo pelo NOME (não precisa saber o player_id).
  - Cache local dos players (evita rebaixar a lista a cada chamada).
  - Preenche video_duration e pitch_time sozinho, a partir do cache.
  - Normaliza datas para o formato que a API exige (com hora completa).
  - Período em linguagem curta: "30d", "tudo", "2026-04-01:2026-05-31".
  - Converte a curva de retenção (que vem como histograma de abandono)
    em retenção acumulada real, já com os maiores pontos de queda.
  - Converte valores de centavos para reais.
  - Agrupa origens de tráfego sem diferenciar maiúscula de minúscula.
  - vturb_analise faz 5 chamadas em paralelo e devolve o diagnóstico pronto.
  - Saída em texto tabulado, muito mais leve que o JSON original.

Protocolo: MCP via stdio (JSON-RPC 2.0, uma mensagem por linha).
Sem dependências externas: apenas biblioteca padrão do Python.

Autenticação: VTURB_API_TOKEN no .env da raiz do projeto (ou variável de
ambiente). Nunca escrever o token neste arquivo.

Documentação oficial: https://vturb.gitbook.io/analytics-api/pt
"""

import json
import os
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

# No Windows o stdout padrão é cp1252; o protocolo MCP exige UTF-8
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://analytics.vturb.net"
API_VERSION = "v1"
SERVER_NAME = "vturb"
SERVER_VERSION = "2.0.0"

CACHE_PLAYERS = Path(tempfile.gettempdir()) / "vturb-players-cache.json"
CACHE_TTL = 600  # 10 minutos


# ---------------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------------

def carregar_token():
    token = os.environ.get("VTURB_API_TOKEN")
    if token:
        return token.strip()
    cur = Path(__file__).resolve().parent
    while cur.parent != cur:
        candidato = cur / ".env"
        if candidato.exists():
            try:
                for linha in candidato.read_text(encoding="utf-8").splitlines():
                    linha = linha.strip()
                    if linha.startswith("VTURB_API_TOKEN="):
                        return linha.split("=", 1)[1].strip().strip('"').strip("'")
            except OSError:
                pass
        cur = cur.parent
    return None


class ErroVTurb(Exception):
    pass


# ---------------------------------------------------------------------------
# Camada HTTP
# ---------------------------------------------------------------------------

def api(path, payload=None, method="POST"):
    token = carregar_token()
    if not token:
        raise ErroVTurb(
            "Token da VTurb não configurado. Adicione VTURB_API_TOKEN=seu_token "
            "no arquivo .env da raiz do projeto. O token é gerado no painel da "
            "VTurb, em configurações de API."
        )
    url = BASE_URL + path
    headers = {
        "X-Api-Token": token,
        "X-Api-Version": API_VERSION,
        "Content-Type": "application/json",
    }
    payload = {k: v for k, v in (payload or {}).items() if v not in (None, "", [])}
    if method == "GET":
        if payload:
            url += "?" + urllib.parse.urlencode(payload, doseq=True)
        req = urllib.request.Request(url, headers=headers, method="GET")
    else:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
        )
    # A VTurb às vezes devolve vazio ou 429 quando recebe chamadas em paralelo.
    # Tentamos de novo com espera crescente para não entregar número errado.
    ultimo_erro = None
    for tentativa in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                bruto = resp.read().decode("utf-8", errors="replace")
            break
        except urllib.error.HTTPError as e:
            detalhe = e.read().decode("utf-8", errors="replace")[:600]
            if e.code == 401:
                raise ErroVTurb("Token da VTurb inválido ou expirado (401). Confira o .env.")
            if e.code == 429:
                ultimo_erro = ErroVTurb("Limite de requisições da VTurb atingido (429).")
                time.sleep(1.5 * (tentativa + 1))
                continue
            raise ErroVTurb("Erro HTTP %s da VTurb: %s" % (e.code, detalhe))
        except urllib.error.URLError as e:
            ultimo_erro = ErroVTurb("Falha de conexão com a VTurb: %s" % e.reason)
            time.sleep(1.0 * (tentativa + 1))
    else:
        raise ultimo_erro or ErroVTurb("A VTurb não respondeu após 3 tentativas.")
    try:
        dados = json.loads(bruto)
    except ValueError:
        raise ErroVTurb("Resposta inesperada da VTurb: %s" % bruto[:300])
    if isinstance(dados, dict) and dados.get("error"):
        raise ErroVTurb("A VTurb recusou a consulta: %s" % dados["error"])
    return dados


# ---------------------------------------------------------------------------
# Players: cache e resolução por nome
# ---------------------------------------------------------------------------

def listar_players(forcar=False):
    if not forcar and CACHE_PLAYERS.exists():
        try:
            if time.time() - CACHE_PLAYERS.stat().st_mtime < CACHE_TTL:
                return json.loads(CACHE_PLAYERS.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    dados = api("/players/list", method="GET")
    try:
        CACHE_PLAYERS.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    return dados


def _normalizar(texto):
    texto = unicodedata.normalize("NFKD", str(texto or ""))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower().strip()


def resolver_player(termo):
    """Aceita o player_id ou parte do nome do vídeo. Devolve o dicionário do player."""
    if not termo:
        raise ErroVTurb("Informe o nome do vídeo ou o player_id.")
    players = listar_players()
    termo_str = str(termo).strip()
    for p in players:
        if p.get("id") == termo_str:
            return p
    alvo = _normalizar(termo_str)
    exatos = [p for p in players if _normalizar(p.get("name")) == alvo]
    if len(exatos) == 1:
        return exatos[0]
    parciais = [p for p in players if alvo in _normalizar(p.get("name"))]
    if not parciais:
        # segunda tentativa: cache pode estar velho
        players = listar_players(forcar=True)
        parciais = [p for p in players if alvo in _normalizar(p.get("name"))]
    if not parciais:
        amostra = ", ".join(p.get("name", "?") for p in players[:8])
        raise ErroVTurb(
            'Nenhum vídeo encontrado com "%s". Use vturb_players para ver a lista. '
            "Alguns vídeos da conta: %s" % (termo_str, amostra)
        )
    if len(exatos) > 1:
        parciais = exatos
    if len(parciais) > 1:
        # desempate: nome mais curto (mais próximo do termo), depois mais recente
        parciais = sorted(parciais, key=lambda p: (len(p.get("name", "")), p.get("created_at", "")))
        opcoes = " | ".join("%s (%s)" % (p.get("name"), p.get("id")) for p in parciais[:6])
        parciais[0]["_ambiguo"] = opcoes
    return parciais[0]


# ---------------------------------------------------------------------------
# Datas e períodos
# ---------------------------------------------------------------------------

def _para_datetime(valor, fim_do_dia=False):
    texto = str(valor).strip().replace("T", " ")
    for corte in ("+", "Z"):
        if corte in texto[10:]:
            texto = texto[:10] + " " + texto[11:19]
            break
    texto = texto[:19]
    if len(texto) == 10:
        texto += " 23:59:59" if fim_do_dia else " 00:00:00"
    elif len(texto) < 19:
        texto = (texto + " 00:00:00")[:19]
    return texto


def resolver_periodo(periodo, player=None):
    """
    Aceita: "30d", "7d", "90d", "tudo", "hoje", "ontem",
            "2026-04-01:2026-05-31", "2026-04-01".
    Devolve (inicio, fim) já no formato exigido pela API.
    """
    agora = datetime.now()
    fim = agora.strftime("%Y-%m-%d 23:59:59")
    p = (periodo or "tudo").strip().lower()

    if ":" in p:
        a, b = p.split(":", 1)
        return _para_datetime(a), _para_datetime(b, fim_do_dia=True)
    if p in ("tudo", "sempre", "total", "vida"):
        criado = (player or {}).get("created_at")
        inicio = _para_datetime(criado) if criado else (agora - timedelta(days=365)).strftime("%Y-%m-%d 00:00:00")
        return inicio, fim
    if p == "hoje":
        return agora.strftime("%Y-%m-%d 00:00:00"), fim
    if p == "ontem":
        d = agora - timedelta(days=1)
        return d.strftime("%Y-%m-%d 00:00:00"), d.strftime("%Y-%m-%d 23:59:59")
    if p.endswith("d") and p[:-1].isdigit():
        d = agora - timedelta(days=int(p[:-1]))
        return d.strftime("%Y-%m-%d 00:00:00"), fim
    if p.endswith("m") and p[:-1].isdigit():
        d = agora - timedelta(days=30 * int(p[:-1]))
        return d.strftime("%Y-%m-%d 00:00:00"), fim
    return _para_datetime(p), fim


# ---------------------------------------------------------------------------
# Formatação
# ---------------------------------------------------------------------------

def n(valor):
    try:
        return "{:,}".format(int(valor)).replace(",", ".")
    except (TypeError, ValueError):
        return str(valor)


def reais(centavos):
    try:
        v = float(centavos) / 100.0
    except (TypeError, ValueError):
        return "R$ 0,00"
    return "R$ " + "{:,.2f}".format(v).replace(",", "@").replace(".", ",").replace("@", ".")


def pct(parte, total, casas=1):
    if not total:
        return "0,0%"
    return ("{:." + str(casas) + "f}%").format(100.0 * parte / total).replace(".", ",")


def mmss(segundos):
    s = int(segundos)
    return "%d:%02d" % (s // 60, s % 60)


def f(valor, casas=2):
    try:
        return ("{:." + str(casas) + "f}").format(float(valor)).replace(".", ",")
    except (TypeError, ValueError):
        return str(valor)


def cabecalho(player, inicio, fim, extra=""):
    linhas = [
        "VÍDEO: %s" % player.get("name"),
        "id %s | duração %s | oferta (pitch) aos %s"
        % (player.get("id"), mmss(player.get("duration") or 0), mmss(player.get("pitch_time") or 0)),
        "PERÍODO: %s até %s" % (inicio[:10], fim[:10]),
    ]
    if not player.get("pitch_time"):
        linhas.append("ATENÇÃO: pitch_time não configurado na VTurb. Métricas de audiência na oferta ficam zeradas.")
    if player.get("_ambiguo"):
        linhas.append("Vários vídeos batem com o nome. Usei o primeiro. Opções: %s" % player["_ambiguo"])
    if extra:
        linhas.append(extra)
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Blocos de análise (cada um devolve texto pronto)
# ---------------------------------------------------------------------------

def bloco_funil(s):
    views = s.get("total_viewed", 0) or 0
    plays = s.get("total_started", 0) or 0
    pitch = s.get("total_over_pitch", 0) or 0
    cliques = s.get("total_clicked_session_uniq", 0) or 0
    vendas = s.get("total_conversions", 0) or 0
    brl = s.get("total_amount_brl", 0) or 0
    ticket = (brl / 100.0 / vendas) if vendas else 0

    # play rate vem pronto da VTurb (calculado sobre dispositivos únicos, não sobre views brutas)
    play_rate = "%s%%" % f(s.get("play_rate", 0), 1) if s.get("play_rate") else pct(plays, views)

    L = ["FUNIL", "etapa                    pessoas    taxa"]
    L.append("carregaram a página    %10s       ." % n(views))
    L.append("deram play             %10s  %6s  (play rate oficial VTurb)" % (n(plays), play_rate))
    L.append("chegaram na oferta     %10s  %6s  dos plays" % (n(pitch), pct(pitch, plays)))
    L.append("clicaram no botão      %10s  %6s  de quem viu a oferta" % (n(cliques), pct(cliques, pitch)))
    L.append("compraram              %10s  %6s  de quem clicou" % (n(vendas), pct(vendas, cliques)))
    L.append("")
    L.append("Faturamento: %s  |  ticket médio: %s" % (reais(brl), reais(ticket * 100)))
    L.append("Conversão sobre plays: %s  |  sobre quem viu a oferta: %s"
             % (pct(vendas, plays, 2), pct(vendas, pitch, 2)))
    L.append("Engajamento médio: %s%%" % f(s.get("engagement_rate", 0), 2))
    return "\n".join(L)


def curva_retencao(dados_ret, duracao, pitch_time):
    """Converte o histograma de abandono da VTurb em retenção acumulada."""
    g = sorted(dados_ret.get("grouped_timed", []), key=lambda x: x["timed"])
    base = sum(x["total_users"] for x in g)
    if not base:
        return None, None, 0
    acumulado = {}
    corrente = 0
    for x in reversed(g):  # soma da cauda: quem chegou em t = todos que pararam em t ou depois
        corrente += x["total_users"]
        acumulado[x["timed"]] = corrente

    def chegaram(t):
        candidatos = [k for k in acumulado if k >= t]
        return acumulado[min(candidatos)] if candidatos else 0

    return chegaram, base, base


def bloco_retencao(dados_ret, player):
    duracao = player.get("duration") or 0
    pitch_time = player.get("pitch_time") or 0
    chegaram, base, _ = curva_retencao(dados_ret, duracao, pitch_time)
    if not chegaram:
        return "RETENÇÃO\nSem dados de retenção no período."

    marcos = [0, 5, 10, 15, 20, 30, 45, 60, 90, 120, 180, 240, 300, 360]
    marcos = [m for m in marcos if m < duracao]
    if pitch_time:
        marcos.append(pitch_time)
    marcos.append(duracao)
    marcos = sorted(set(marcos))

    L = ["RETENÇÃO (base: %s plays)" % n(base),
         "tempo média assistida: %ss  |  engajamento: %s%%"
         % (f(dados_ret.get("average_watched_time", 0), 0), f(dados_ret.get("engagement_rate", 0), 2)),
         "",
         "tempo    pessoas   retenção   perda no trecho"]
    anterior = None
    for m in marcos:
        u = chegaram(m)
        r = 100.0 * u / base
        perda = "" if anterior is None else "  -%s pp" % f(anterior - r, 1)
        marca = "   <== OFERTA" if pitch_time and m == pitch_time else ""
        L.append("%6s %9s   %6s%%%s%s" % (mmss(m), n(u), f(r, 1), perda, marca))
        anterior = r

    # maiores quedas por trecho de 5 segundos nos primeiros 60s
    quedas = []
    for ini in range(0, min(60, int(duracao)), 5):
        a, b = chegaram(ini), chegaram(ini + 5)
        if a:
            quedas.append((100.0 * (a - b) / base, ini, a - b))
    quedas.sort(reverse=True)
    if quedas:
        L.append("")
        L.append("Maiores quedas nos primeiros 60 segundos:")
        for pp, ini, pessoas in quedas[:3]:
            L.append("  %s a %s  perde %s pp (%s pessoas)" % (mmss(ini), mmss(ini + 5), f(pp, 1), n(pessoas)))

    # leitura automática: hook x corpo
    if pitch_time:
        r15 = 100.0 * chegaram(15) / base
        rpitch = 100.0 * chegaram(pitch_time) / base
        L.append("")
        L.append("LEITURA: o hook (0 a 15s) segura %s%% e o corpo do vídeo (15s até a oferta) segura %s%% dos que passaram do hook."
                 % (f(r15, 1), f(100.0 * rpitch / r15 if r15 else 0, 1)))
        if r15 < 65:
            perdidos = base - chegaram(15)
            L.append("O hook é o gargalo: %s pessoas deram play e saíram antes de 15 segundos." % n(perdidos))
    return "\n".join(L)


def bloco_cliques(dados_cli, player):
    itens = dados_cli if isinstance(dados_cli, list) else dados_cli.get("data", [])
    itens = sorted(itens, key=lambda x: x["timed"])
    total = sum(x["total_users"] for x in itens)
    if not total:
        return "CLIQUES\nSem cliques registrados no período."
    pitch_time = player.get("pitch_time") or 0
    antes = sum(x["total_users"] for x in itens if x["timed"] < pitch_time) if pitch_time else 0
    L = ["CLIQUES NO BOTÃO (total: %s)" % n(total)]
    if pitch_time:
        L.append("antes da oferta: %s (%s)  |  depois da oferta: %s (%s)"
                 % (n(antes), pct(antes, total), n(total - antes), pct(total - antes, total)))
    L.append("")
    L.append("Momentos de maior clique:")
    for x in sorted(itens, key=lambda x: -x["total_users"])[:8]:
        marca = " (após a oferta)" if pitch_time and x["timed"] >= pitch_time else ""
        L.append("  %6s  %6s cliques%s" % (mmss(x["timed"]), n(x["total_users"]), marca))
    inicio = sum(x["total_users"] for x in itens if x["timed"] <= 1)
    if inicio and 100.0 * inicio / total >= 5:
        L.append("")
        L.append("ALERTA: %s cliques (%s do total) acontecem no primeiro segundo. "
                 "Verifique se o botão de compra está visível na página antes do vídeo rodar."
                 % (n(inicio), pct(inicio, total)))
    return "\n".join(L)


def bloco_trafego(dados_tr):
    itens = dados_tr if isinstance(dados_tr, list) else dados_tr.get("data", [])
    ag = {}
    for x in itens:
        chave = (x.get("grouped_field") or "(sem utm)").strip().lower()
        a = ag.setdefault(chave, {"plays": 0, "pitch": 0, "vendas": 0, "brl": 0})
        a["plays"] += x.get("total_started", 0) or 0
        a["pitch"] += x.get("total_over_pitch", 0) or 0
        a["vendas"] += x.get("total_conversions", 0) or 0
        a["brl"] += x.get("total_amount_brl", 0) or 0
    if not ag:
        return "ORIGEM DE TRÁFEGO\nSem dados de UTM no período."
    L = ["ORIGEM DE TRÁFEGO (agrupado, maiúscula e minúscula juntas)",
         "origem            plays   na oferta   vendas   conversão   faturamento"]
    for k, a in sorted(ag.items(), key=lambda i: -i[1]["plays"]):
        if a["plays"] < 10:
            continue
        L.append("%-14s %8s %10s %8s %10s   %s"
                 % (k[:14], n(a["plays"]), pct(a["pitch"], a["plays"]), n(a["vendas"]),
                    pct(a["vendas"], a["plays"], 2), reais(a["brl"])))
    validos = [(k, a) for k, a in ag.items() if a["plays"] >= 50]
    if len(validos) >= 2:
        validos.sort(key=lambda i: -(i[1]["vendas"] / i[1]["plays"]))
        melhor, pior = validos[0], validos[-1]
        tm = melhor[1]["vendas"] / melhor[1]["plays"] if melhor[1]["plays"] else 0
        tp = pior[1]["vendas"] / pior[1]["plays"] if pior[1]["plays"] else 0
        if tp and tm / tp >= 1.5:
            L.append("")
            L.append("LEITURA: %s converte %sx melhor que %s. Vale testar mais verba na origem que converte."
                     % (melhor[0], f(tm / tp, 1), pior[0]))
    return "\n".join(L)


def bloco_mensal(dias):
    if not isinstance(dias, list) or not dias:
        return "EVOLUÇÃO\nSem série diária no período."
    meses = {}
    for x in sorted(dias, key=lambda d: d.get("date_key", "")):
        k = (x.get("date_key") or "")[:7]
        if not k:
            continue
        a = meses.setdefault(k, {"plays": 0, "pitch": 0, "vendas": 0, "brl": 0})
        a["plays"] += x.get("total_started", 0) or 0
        a["pitch"] += x.get("total_over_pitch", 0) or 0
        a["vendas"] += x.get("total_conversions", 0) or 0
        a["brl"] += x.get("total_amount_brl", 0) or 0
    L = ["EVOLUÇÃO POR MÊS", "mês        plays   na oferta   vendas   faturamento"]
    for k, a in meses.items():
        L.append("%-9s %8s %10s %8s   %s"
                 % (k, n(a["plays"]), pct(a["pitch"], a["plays"]), n(a["vendas"]), reais(a["brl"])))
    ultimos = [x for x in sorted(dias, key=lambda d: d.get("date_key", ""))][-7:]
    p7 = sum(x.get("total_started", 0) or 0 for x in ultimos)
    v7 = sum(x.get("total_conversions", 0) or 0 for x in ultimos)
    L.append("")
    L.append("Últimos 7 dias do período: %s plays e %s vendas." % (n(p7), n(v7)))
    if p7 < 50:
        L.append("LEITURA: o vídeo está praticamente sem tráfego agora. Os números do período vêm do passado.")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# Ferramentas
# ---------------------------------------------------------------------------

def t_players(args):
    players = listar_players(forcar=bool(args.get("atualizar")))
    busca = _normalizar(args.get("busca", ""))
    if busca:
        players = [p for p in players if busca in _normalizar(p.get("name"))]
    players = sorted(players, key=lambda p: p.get("created_at", ""), reverse=True)
    L = ["VÍDEOS NA CONTA VTURB (%s)" % len(players),
         "nome                                          duração   oferta   criado em"]
    for p in players:
        L.append("%-45s %8s %8s   %s"
                 % ((p.get("name") or "")[:45], mmss(p.get("duration") or 0),
                    mmss(p.get("pitch_time") or 0) if p.get("pitch_time") else "nao def",
                    (p.get("created_at") or "")[:10]))
    L.append("")
    L.append("Use o nome do vídeo direto nas outras ferramentas, não precisa do id.")
    return "\n".join(L)


def _stats(player, inicio, fim, tz):
    corpo = {
        "player_id": player["id"], "start_date": inicio, "end_date": fim,
        "video_duration": player.get("duration"), "pitch_time": player.get("pitch_time"),
        "timezone": tz}
    s = api("/sessions/stats", corpo)
    # Zero absoluto quase sempre é resposta vazia da VTurb sob concorrência, não
    # ausência real de dados. Confere uma segunda vez antes de reportar zero.
    if not (s.get("total_viewed") or s.get("total_started")):
        time.sleep(1.2)
        segunda = api("/sessions/stats", corpo)
        if segunda.get("total_viewed") or segunda.get("total_started"):
            return segunda
    return s


def t_analise(args):
    player = resolver_player(args.get("video"))
    inicio, fim = resolver_periodo(args.get("periodo"), player)
    tz = args.get("timezone") or "America/Sao_Paulo"
    pid, dur, pit = player["id"], player.get("duration"), player.get("pitch_time")

    tarefas = {
        "stats": lambda: _stats(player, inicio, fim, tz),
        "ret": lambda: api("/times/user_engagement", {
            "player_id": pid, "video_duration": dur,
            "start_date": inicio, "end_date": fim, "timezone": tz}),
        "cli": lambda: api("/clicks/total_by_company_timed", {
            "player_id": pid, "start_date": inicio, "end_date": fim, "timezone": tz}),
        "dia": lambda: api("/sessions/stats_by_day", {
            "player_id": pid, "start_date": inicio, "end_date": fim,
            "video_duration": dur, "pitch_time": pit, "timezone": tz}),
        "tra": lambda: api("/traffic_origin/stats", {
            "player_id": pid, "start_date": inicio, "end_date": fim,
            "query_key": "utm_source", "video_duration": dur, "pitch_time": pit, "timezone": tz}),
    }
    res, erros = {}, []
    with ThreadPoolExecutor(max_workers=5) as ex:
        futuros = {k: ex.submit(fn) for k, fn in tarefas.items()}
        for k, fu in futuros.items():
            try:
                res[k] = fu.result()
            except ErroVTurb as e:
                res[k] = None
                erros.append("%s: %s" % (k, e))

    partes = [cabecalho(player, inicio, fim)]
    if res.get("stats"):
        partes.append(bloco_funil(res["stats"]))
    if res.get("ret"):
        partes.append(bloco_retencao(res["ret"], player))
    if res.get("cli"):
        partes.append(bloco_cliques(res["cli"], player))
    if res.get("tra"):
        partes.append(bloco_trafego(res["tra"]))
    if res.get("dia"):
        partes.append(bloco_mensal(res["dia"]))
    if erros:
        partes.append("Blocos que falharam: " + "; ".join(erros))
    return "\n\n".join(partes)


def t_funil(args):
    player = resolver_player(args.get("video"))
    inicio, fim = resolver_periodo(args.get("periodo"), player)
    tz = args.get("timezone") or "America/Sao_Paulo"
    return cabecalho(player, inicio, fim) + "\n\n" + bloco_funil(_stats(player, inicio, fim, tz))


def t_retencao(args):
    player = resolver_player(args.get("video"))
    inicio, fim = resolver_periodo(args.get("periodo"), player)
    tz = args.get("timezone") or "America/Sao_Paulo"
    d = api("/times/user_engagement", {
        "player_id": player["id"], "video_duration": player.get("duration"),
        "start_date": inicio, "end_date": fim, "timezone": tz})
    return cabecalho(player, inicio, fim) + "\n\n" + bloco_retencao(d, player)


def t_cliques(args):
    player = resolver_player(args.get("video"))
    inicio, fim = resolver_periodo(args.get("periodo"), player)
    tz = args.get("timezone") or "America/Sao_Paulo"
    d = api("/clicks/total_by_company_timed", {
        "player_id": player["id"], "start_date": inicio, "end_date": fim, "timezone": tz})
    return cabecalho(player, inicio, fim) + "\n\n" + bloco_cliques(d, player)


def t_por_dia(args):
    player = resolver_player(args.get("video"))
    inicio, fim = resolver_periodo(args.get("periodo"), player)
    tz = args.get("timezone") or "America/Sao_Paulo"
    d = api("/sessions/stats_by_day", {
        "player_id": player["id"], "start_date": inicio, "end_date": fim,
        "video_duration": player.get("duration"), "pitch_time": player.get("pitch_time"), "timezone": tz})
    L = [cabecalho(player, inicio, fim), "", bloco_mensal(d)]
    if args.get("detalhe_diario"):
        L.append("")
        L.append("DIA A DIA (apenas dias com play)")
        L.append("data          plays   na oferta   cliques   vendas   faturamento")
        for x in sorted(d, key=lambda i: i.get("date_key", "")):
            p = x.get("total_started", 0) or 0
            if not p:
                continue
            L.append("%-12s %7s %10s %9s %8s   %s"
                     % (x.get("date_key"), n(p), pct(x.get("total_over_pitch", 0) or 0, p),
                        n(x.get("total_clicked_session_uniq", 0) or 0),
                        n(x.get("total_conversions", 0) or 0), reais(x.get("total_amount_brl", 0) or 0)))
    return "\n".join(L)


def t_trafego(args):
    player = resolver_player(args.get("video"))
    inicio, fim = resolver_periodo(args.get("periodo"), player)
    tz = args.get("timezone") or "America/Sao_Paulo"
    chave = args.get("parametro") or "utm_source"
    d = api("/traffic_origin/stats", {
        "player_id": player["id"], "start_date": inicio, "end_date": fim,
        "query_key": chave, "video_duration": player.get("duration"),
        "pitch_time": player.get("pitch_time"), "timezone": tz})
    return cabecalho(player, inicio, fim, "Agrupado por: %s" % chave) + "\n\n" + bloco_trafego(d)


def t_segmentar(args):
    player = resolver_player(args.get("video"))
    inicio, fim = resolver_periodo(args.get("periodo"), player)
    tz = args.get("timezone") or "America/Sao_Paulo"
    campo = args.get("campo") or "country"
    d = api("/sessions/stats_by_field", {
        "player_id": player["id"], "start_date": inicio, "end_date": fim, "field": campo,
        "video_duration": player.get("duration"), "pitch_time": player.get("pitch_time"), "timezone": tz})
    itens = d if isinstance(d, list) else [d]
    L = [cabecalho(player, inicio, fim, "Segmentado por: %s" % campo), "",
         "valor              plays   na oferta   vendas   conversão   faturamento"]
    for x in sorted(itens, key=lambda i: -(i.get("total_started", 0) or 0)):
        p = x.get("total_started", 0) or 0
        if p < 10:
            continue
        L.append("%-16s %8s %10s %8s %10s   %s"
                 % (str(x.get("grouped_field"))[:16], n(p), pct(x.get("total_over_pitch", 0) or 0, p),
                    n(x.get("total_conversions", 0) or 0),
                    pct(x.get("total_conversions", 0) or 0, p, 2), reais(x.get("total_amount_brl", 0) or 0)))
    return "\n".join(L)


def t_comparar(args):
    videos = args.get("videos") or []
    if len(videos) < 2:
        raise ErroVTurb("Informe pelo menos 2 vídeos para comparar.")
    tz = args.get("timezone") or "America/Sao_Paulo"
    periodo = args.get("periodo")
    players = [resolver_player(v) for v in videos]

    def puxar(p):
        ini, f_ = resolver_periodo(periodo, p)
        return p, ini, f_, _stats(p, ini, f_, tz)

    linhas = []
    with ThreadPoolExecutor(max_workers=min(6, len(players))) as ex:
        for p, ini, f_, s in ex.map(puxar, players):
            linhas.append((p, ini, f_, s))
    L = ["COMPARATIVO DE VÍDEOS", "",
         "vídeo                              plays  play rate  na oferta  vendas  conv%   faturamento"]
    for p, ini, f_, s in linhas:
        plays = s.get("total_started", 0) or 0
        taxa_play = "%s%%" % f(s.get("play_rate", 0), 1) if s.get("play_rate") else pct(plays, s.get("total_viewed", 0) or 0)
        L.append("%-32s %7s %9s %10s %7s %6s   %s"
                 % ((p.get("name") or "")[:32], n(plays), taxa_play,
                    pct(s.get("total_over_pitch", 0) or 0, plays), n(s.get("total_conversions", 0) or 0),
                    pct(s.get("total_conversions", 0) or 0, plays, 2), reais(s.get("total_amount_brl", 0) or 0)))
    L.append("")
    L.append("Períodos usados: " + "; ".join("%s (%s a %s)" % (p.get("name"), i[:10], f_[:10])
                                             for p, i, f_, _ in linhas))
    return "\n".join(L)


def t_conversoes_no_video(args):
    player = resolver_player(args.get("video"))
    inicio, fim = resolver_periodo(args.get("periodo"), player)
    tz = args.get("timezone") or "America/Sao_Paulo"
    d = api("/conversions/video_timed", {
        "player_id": player["id"], "start_date": inicio, "end_date": fim, "timezone": tz})
    # o endpoint às vezes devolve objeto e às vezes lista de objetos
    if isinstance(d, dict):
        bruto = d.get("grouped_timed", [])
    else:
        bruto = []
        for item in d or []:
            if isinstance(item, dict):
                bruto.extend(item.get("grouped_timed", []) or [])
    g = sorted(bruto, key=lambda x: -(x.get("timed_conversions") or 0))
    L = [cabecalho(player, inicio, fim), "", "ONDE OS COMPRADORES ESTAVAM NO VÍDEO AO CONVERTER"]
    if not g:
        L.append("Sem conversões atribuídas a momentos do vídeo no período.")
    else:
        L.append("tempo do vídeo    conversões")
        for x in g[:15]:
            L.append("%12s %12s" % (mmss(x.get("timed") or 0), n(x.get("timed_conversions") or 0)))
    return "\n".join(L)


def t_ao_vivo(args):
    player = resolver_player(args.get("video"))
    d = api("/sessions/live_users", {
        "player_id": player["id"], "minutes": args.get("minutos") or 60}, method="GET")
    itens = d if isinstance(d, list) else []
    total = sum(x.get("live_users", 0) for x in itens)
    L = ["AO VIVO: %s | últimos %s minutos" % (player.get("name"), args.get("minutos") or 60),
         "total assistindo agora: %s" % n(total)]
    for x in itens:
        L.append("  %-40s %s" % (str(x.get("domain"))[:40], n(x.get("live_users", 0))))
    return "\n".join(L)


def t_ab_tests(args):
    inicio, fim = resolver_periodo(args.get("periodo") or "90d")
    d = api("/comparison_groups/list", {"start_date": inicio, "end_date": fim,
                                        "timezone": args.get("timezone") or "America/Sao_Paulo"})
    if not d:
        return "Nenhum teste A/B encontrado no período."
    L = ["TESTES A/B (%s)" % len(d)]
    for g in d:
        L.append("")
        L.append("%s  (id %s)" % (g.get("name"), g.get("id")))
        L.append("  início %s | fim %s" % (str(g.get("started_at"))[:10], str(g.get("finished_at"))[:10]))
        for p in g.get("players", []):
            L.append("    player %s  %s%% do tráfego" % (p.get("player_id"), f(p.get("traffic_percentage", 0), 0)))
    return "\n".join(L)


def t_quota(args):
    d = api("/quota/usage", method="GET")
    L = ["QUOTA DA API VTURB"]
    for q in d.get("quotas", []):
        janela = q.get("interval_seconds")
        rotulo = "por minuto" if janela == 60 else ("por dia" if janela == 86400 else "janela de %ss" % janela)
        c = q.get("queries", {})
        L.append("  %-14s usadas %s de %s (restam %s)"
                 % (rotulo, n(c.get("used", 0)), n(c.get("limit", 0)), n(c.get("remaining", 0))))
    return "\n".join(L)


# ---------------------------------------------------------------------------
# Registro das ferramentas
# ---------------------------------------------------------------------------

P_VIDEO = {"type": "string", "description": "Nome do vídeo (aceita parte do nome) ou o player_id."}
P_PERIODO = {"type": "string", "description": "Período: '7d', '30d', '90d', 'tudo' (desde a criação, padrão), 'hoje', 'ontem' ou '2026-04-01:2026-05-31'."}
P_TZ = {"type": "string", "description": "Timezone. Padrão: America/Sao_Paulo."}

REGISTRO = [
    ("vturb_analise", t_analise,
     "ANÁLISE COMPLETA de um VSL em uma única chamada: funil, curva de retenção com pontos de queda, cliques por momento, origem de tráfego e evolução mensal, tudo já interpretado. Use esta ferramenta sempre que o pedido for 'analisar' um vídeo.",
     {"video": P_VIDEO, "periodo": P_PERIODO, "timezone": P_TZ}, ["video"]),

    ("vturb_players", t_players,
     "Lista ou busca os vídeos da conta VTurb com duração, momento da oferta e data de criação. Use quando não souber o nome exato do vídeo.",
     {"busca": {"type": "string", "description": "Filtro por parte do nome."},
      "atualizar": {"type": "boolean", "description": "Ignorar o cache e rebaixar a lista."}}, []),

    ("vturb_funil", t_funil,
     "Funil do vídeo no período: views, plays, play rate, quantos chegaram na oferta, cliques, vendas, faturamento e ticket médio.",
     {"video": P_VIDEO, "periodo": P_PERIODO, "timezone": P_TZ}, ["video"]),

    ("vturb_retencao", t_retencao,
     "Curva de retenção real do vídeo (já convertida de histograma para retenção acumulada), com marcos de tempo, os maiores pontos de queda nos primeiros 60 segundos e leitura automática de hook x corpo do vídeo.",
     {"video": P_VIDEO, "periodo": P_PERIODO, "timezone": P_TZ}, ["video"]),

    ("vturb_cliques", t_cliques,
     "Em que momento do vídeo as pessoas clicam no botão, quanto acontece antes e depois da oferta, e alerta de cliques no segundo zero.",
     {"video": P_VIDEO, "periodo": P_PERIODO, "timezone": P_TZ}, ["video"]),

    ("vturb_por_dia", t_por_dia,
     "Evolução do vídeo por mês e nos últimos 7 dias, com opção de abrir o detalhe dia a dia.",
     {"video": P_VIDEO, "periodo": P_PERIODO, "timezone": P_TZ,
      "detalhe_diario": {"type": "boolean", "description": "Incluir a tabela dia a dia."}}, ["video"]),

    ("vturb_trafego", t_trafego,
     "Performance por origem de tráfego (utm_source, utm_campaign, src, sck etc.), com variações de maiúscula agrupadas e comparação de qual origem converte melhor.",
     {"video": P_VIDEO, "periodo": P_PERIODO, "timezone": P_TZ,
      "parametro": {"type": "string", "description": "Parâmetro de tráfego.",
                    "enum": ["utm_source", "utm_campaign", "utm_medium", "utm_content", "utm_term", "src", "sck"]}},
     ["video"]),

    ("vturb_segmentar", t_segmentar,
     "Performance do vídeo segmentada por país, navegador ou tipo de dispositivo.",
     {"video": P_VIDEO, "periodo": P_PERIODO, "timezone": P_TZ,
      "campo": {"type": "string", "description": "Campo de segmentação.",
                "enum": ["country", "browser", "device_type", "utm_campaign", "utm_source", "utm_medium"]}},
     ["video"]),

    ("vturb_comparar", t_comparar,
     "Compara vários vídeos lado a lado (plays, play rate, audiência na oferta, vendas, conversão e faturamento). Ideal para comparar versões de VSL ou hooks diferentes.",
     {"videos": {"type": "array", "items": {"type": "string"},
                 "description": "Nomes ou ids dos vídeos a comparar (mínimo 2)."},
      "periodo": P_PERIODO, "timezone": P_TZ}, ["videos"]),

    ("vturb_conversoes_no_video", t_conversoes_no_video,
     "Mostra em que ponto do vídeo os compradores estavam quando converteram.",
     {"video": P_VIDEO, "periodo": P_PERIODO, "timezone": P_TZ}, ["video"]),

    ("vturb_ao_vivo", t_ao_vivo,
     "Quantas pessoas estão assistindo o vídeo agora, por domínio.",
     {"video": P_VIDEO, "minutos": {"type": "integer", "description": "Janela em minutos (padrão 60)."}}, ["video"]),

    ("vturb_ab_tests", t_ab_tests,
     "Lista os testes A/B configurados na VTurb, com os players de cada um e o percentual de tráfego.",
     {"periodo": P_PERIODO, "timezone": P_TZ}, []),

    ("vturb_quota", t_quota,
     "Consulta quanto da quota da API da VTurb já foi usada.", {}, []),
]

TOOLS = {nome: (fn, desc, props, req) for nome, fn, desc, props, req in REGISTRO}


def montar_lista_tools():
    return [{
        "name": nome,
        "description": desc,
        "inputSchema": {"type": "object", "properties": props, "required": req},
    } for nome, _fn, desc, props, req in REGISTRO]


# ---------------------------------------------------------------------------
# Loop JSON-RPC (MCP stdio)
# ---------------------------------------------------------------------------

def escrever(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def responder(msg_id, resultado):
    escrever({"jsonrpc": "2.0", "id": msg_id, "result": resultado})


def main():
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha:
            continue
        try:
            msg = json.loads(linha)
        except ValueError:
            continue
        metodo, msg_id = msg.get("method"), msg.get("id")

        if metodo == "initialize":
            versao = (msg.get("params") or {}).get("protocolVersion", "2024-11-05")
            responder(msg_id, {
                "protocolVersion": versao,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            })
        elif metodo == "notifications/initialized":
            continue
        elif metodo == "ping":
            responder(msg_id, {})
        elif metodo == "tools/list":
            responder(msg_id, {"tools": montar_lista_tools()})
        elif metodo == "tools/call":
            params = msg.get("params") or {}
            nome = params.get("name")
            entrada = TOOLS.get(nome)
            if not entrada:
                responder(msg_id, {"content": [{"type": "text", "text": "Ferramenta desconhecida: %s" % nome}],
                                   "isError": True})
                continue
            try:
                texto = entrada[0](params.get("arguments") or {})
                erro = False
            except ErroVTurb as e:
                texto, erro = str(e), True
            except Exception as e:  # falha inesperada não pode derrubar o servidor
                texto, erro = "Erro inesperado no MCP da VTurb: %s: %s" % (type(e).__name__, e), True
            responder(msg_id, {"content": [{"type": "text", "text": texto}], "isError": erro})
        elif msg_id is not None:
            responder(msg_id, {"content": [{"type": "text", "text": "Método não suportado"}], "isError": True})


if __name__ == "__main__":
    main()
