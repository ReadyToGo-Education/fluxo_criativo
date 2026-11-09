#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor MCP da Hotmart (API de Vendas e Produtos).

Expõe as vendas da Hotmart como ferramentas MCP para o Claude Code, já
digeridas e prontas para leitura, sem JSON cru.

O que ele faz:
  - Busca o produto pelo NOME (não precisa saber o id).
  - Período em linguagem curta: "hoje", "7d", "30d", "mes", "2026-10-01:2026-10-31".
  - Junta todas as páginas da API sozinho.
  - Agrupa status em grupos que fazem sentido no dia a dia (aprovadas,
    pendentes, reembolsos, canceladas).
  - Lê o rastreamento de cada venda (xcod, sck, src) e mostra de qual
    campanha e anúncio veio, sem depender da Utmify.

Protocolo: MCP via stdio (JSON-RPC 2.0, uma mensagem por linha).
Sem dependências externas: apenas biblioteca padrão do Python.

Autenticação: HOTMART_BASIC no .env da raiz do projeto (ou variável de
ambiente). É o "Basic" das Credenciais Hotmart (client_id:client_secret em
base64). Nunca escrever a credencial neste arquivo.

Documentação oficial: https://developers.hotmart.com/docs/pt-BR/
"""

import base64
import json
import os
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# No Windows o stdout padrão é cp1252; o protocolo MCP exige UTF-8
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

SERVER_NAME = "hotmart"
SERVER_VERSION = "1.0.0"
AUTH_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
API_URL = "https://developers.hotmart.com"
FUSO = timezone(timedelta(hours=-3))  # horário de Brasília
POR_PAGINA = 100
LIMITE_PADRAO = 2000

GRUPOS_STATUS = {
    "aprovadas": ["APPROVED", "COMPLETE"],
    "pendentes": ["WAITING_PAYMENT", "PRINTED_BILLET", "PROCESSING_TRANSACTION", "UNDER_ANALISYS", "PRE_ORDER"],
    "reembolsos": ["REFUNDED", "PARTIALLY_REFUNDED", "CHARGEBACK", "PROTESTED"],
    "canceladas": ["CANCELLED", "EXPIRED", "NO_FUNDS", "BLOCKED", "OVERDUE"],
}
GRUPOS_STATUS["todas"] = sum(GRUPOS_STATUS.values(), [])
NOME_STATUS = {
    "APPROVED": "aprovada", "COMPLETE": "completa", "WAITING_PAYMENT": "aguardando pagamento",
    "PRINTED_BILLET": "boleto impresso", "PROCESSING_TRANSACTION": "processando",
    "UNDER_ANALISYS": "em análise", "PRE_ORDER": "pré-venda", "REFUNDED": "reembolsada",
    "PARTIALLY_REFUNDED": "reembolso parcial", "CHARGEBACK": "chargeback", "PROTESTED": "contestada",
    "CANCELLED": "cancelada", "EXPIRED": "expirada", "NO_FUNDS": "sem saldo", "BLOCKED": "bloqueada",
    "OVERDUE": "atrasada", "STARTED": "iniciada",
}
SEPARADOR_XCOD = "hQwK21wXxR"  # separador padrão dos parâmetros da Utmify dentro do xcod


class ErroHotmart(Exception):
    pass


# ---------------------------------------------------------------------------
# Credencial e token
# ---------------------------------------------------------------------------

def carregar_basic():
    valor = os.environ.get("HOTMART_BASIC")
    if valor:
        return valor.strip()
    cur = Path(__file__).resolve().parent
    while cur.parent != cur:
        candidato = cur / ".env"
        if candidato.exists():
            try:
                for linha in candidato.read_text(encoding="utf-8").splitlines():
                    linha = linha.strip()
                    if linha.startswith("HOTMART_BASIC="):
                        return linha.split("=", 1)[1].strip().strip('"').strip("'")
            except OSError:
                pass
        cur = cur.parent
    return None


_TOKEN = {"valor": None, "expira": 0}


def obter_token(forcar=False):
    if not forcar and _TOKEN["valor"] and time.time() < _TOKEN["expira"] - 300:
        return _TOKEN["valor"]
    basic = carregar_basic()
    if not basic:
        raise ErroHotmart("HOTMART_BASIC não encontrado no .env. Gere as credenciais em Hotmart > Ferramentas > "
                          "Credenciais Hotmart e salve o valor \"Basic\" no .env.")
    try:
        client_id, client_secret = base64.b64decode(basic).decode("utf-8").split(":", 1)
    except Exception:
        raise ErroHotmart("HOTMART_BASIC no .env não está no formato esperado (base64 de client_id:client_secret).")
    query = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": client_id,
                                    "client_secret": client_secret})
    req = urllib.request.Request(AUTH_URL + "?" + query, method="POST", data=b"",
                                 headers={"Authorization": "Basic " + basic, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            dados = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise ErroHotmart("A Hotmart recusou a credencial (HTTP %s). Confira se as Credenciais Hotmart ainda estão "
                          "ativas." % e.code)
    except urllib.error.URLError as e:
        raise ErroHotmart("Sem conexão com a Hotmart: %s" % e.reason)
    _TOKEN["valor"] = dados.get("access_token")
    _TOKEN["expira"] = time.time() + int(dados.get("expires_in", 3600))
    if not _TOKEN["valor"]:
        raise ErroHotmart("A Hotmart não devolveu o token de acesso.")
    return _TOKEN["valor"]


def api(path, params=None, tentativa=0):
    params = {k: v for k, v in (params or {}).items() if v not in (None, "")}
    url = API_URL + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + obter_token(tentativa > 0),
                                               "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            corpo = r.read()
            return json.loads(corpo) if corpo else {}
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")[:300]
        if e.code == 401 and tentativa == 0:
            return api(path, params, 1)
        if e.code == 429 and tentativa < 3:
            time.sleep(5 * (tentativa + 1))
            return api(path, params, tentativa + 1)
        if e.code == 403:
            raise ErroHotmart("A credencial não tem permissão para este recurso da Hotmart (HTTP 403).")
        raise ErroHotmart("Erro da Hotmart (HTTP %s): %s" % (e.code, corpo))
    except urllib.error.URLError as e:
        raise ErroHotmart("Sem conexão com a Hotmart: %s" % e.reason)


def paginar(path, params, limite=LIMITE_PADRAO):
    itens, token_pagina = [], None
    while True:
        p = dict(params, max_results=POR_PAGINA)
        if token_pagina:
            p["page_token"] = token_pagina
        dados = api(path, p)
        itens.extend(dados.get("items") or [])
        token_pagina = (dados.get("page_info") or {}).get("next_page_token")
        if not token_pagina or len(itens) >= limite:
            return itens[:limite]


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def _normalizar(texto):
    texto = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return " ".join(texto.lower().split())


def _ms(dt):
    return int(dt.timestamp() * 1000)


def _data(ms):
    if not ms:
        return "-"
    return datetime.fromtimestamp(int(ms) / 1000, FUSO).strftime("%d/%m %H:%M")


def _dia(ms):
    return datetime.fromtimestamp(int(ms) / 1000, FUSO).strftime("%Y-%m-%d") if ms else "-"


def resolver_periodo(periodo):
    """Aceita: hoje, ontem, 7d, 30d, 90d, mes, mes-passado, AAAA-MM-DD, AAAA-MM-DD:AAAA-MM-DD."""
    agora = datetime.now(FUSO)
    hoje = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    p = (periodo or "30d").strip().lower()
    if p == "hoje":
        ini, fim = hoje, agora
    elif p == "ontem":
        ini, fim = hoje - timedelta(days=1), hoje - timedelta(milliseconds=1)
    elif p.endswith("d") and p[:-1].isdigit():
        ini, fim = hoje - timedelta(days=int(p[:-1]) - 1), agora
    elif p in ("mes", "mês", "este-mes"):
        ini, fim = hoje.replace(day=1), agora
    elif p in ("mes-passado", "mês-passado"):
        fim_mes = hoje.replace(day=1) - timedelta(milliseconds=1)
        ini, fim = fim_mes.replace(day=1, hour=0, minute=0, second=0, microsecond=0), fim_mes
    else:
        partes = p.split(":")
        try:
            ini = datetime.strptime(partes[0], "%Y-%m-%d").replace(tzinfo=FUSO)
            fim_d = datetime.strptime(partes[-1], "%Y-%m-%d").replace(tzinfo=FUSO)
            fim = fim_d + timedelta(days=1) - timedelta(milliseconds=1)
        except ValueError:
            raise ErroHotmart("Período inválido: \"%s\". Use hoje, ontem, 7d, 30d, mes, mes-passado ou "
                              "AAAA-MM-DD:AAAA-MM-DD." % periodo)
    return ini, fim


_PRODUTOS = {"lista": None, "quando": 0}


def listar_produtos():
    if _PRODUTOS["lista"] is None or time.time() - _PRODUTOS["quando"] > 600:
        _PRODUTOS["lista"] = paginar("/products/api/v1/products", {}, limite=1000)
        _PRODUTOS["quando"] = time.time()
    return _PRODUTOS["lista"]


def resolver_produtos(termo):
    """Devolve ([ids], nomes) a partir de um id numérico ou de parte do nome.

    Se o nome bater exatamente com um produto, usa só ele. Se bater com vários
    (ex: o produto e o order bump "- Vitalício"), usa todos e mostra quais.
    """
    if not termo:
        return [], None
    termo = str(termo).strip()
    try:
        produtos = listar_produtos()
    except ErroHotmart:
        produtos = []
    if termo.isdigit():
        nome = next((p.get("name") for p in produtos if str(p.get("id")) == termo), termo)
        return [termo], nome
    alvo = _normalizar(termo)
    achados = [p for p in produtos if alvo in _normalizar(p.get("name"))]
    if not achados:
        nomes = ", ".join(p.get("name", "") for p in produtos[:20])
        raise ErroHotmart("Nenhum produto com \"%s\" no nome. Produtos encontrados: %s" % (termo, nomes or "nenhum"))
    exatos = [p for p in achados if _normalizar(p.get("name")) == alvo]
    escolhidos = exatos or achados
    return [str(p.get("id")) for p in escolhidos], " + ".join(p.get("name", "") for p in escolhidos)


def buscar_vendas(periodo, produto=None, status="aprovadas", extra=None, limite=LIMITE_PADRAO):
    ini, fim = resolver_periodo(periodo)
    pids, pnome = resolver_produtos(produto)
    grupo = (status or "aprovadas").lower()
    lista_status = GRUPOS_STATUS.get(grupo) or [s.strip().upper() for s in grupo.split(",")]
    vendas = []
    for pid in pids or [None]:
        params = {"start_date": _ms(ini), "end_date": _ms(fim), "product_id": pid,
                  "transaction_status": ",".join(lista_status)}
        params.update(extra or {})
        vendas.extend(paginar("/payments/api/v1/sales/history", params, limite))
    vendas.sort(key=lambda v: (v.get("purchase") or {}).get("order_date") or 0)
    return vendas, ini, fim, pnome


def valor(v):
    preco = (v.get("purchase") or {}).get("price") or {}
    return float(preco.get("value") or 0), preco.get("currency_code") or "BRL"


def moeda(total, cod="BRL"):
    texto = "{:,.2f}".format(total).replace(",", "X").replace(".", ",").replace("X", ".")
    return ("R$ " if cod == "BRL" else cod + " ") + texto


def rastreamento(v):
    t = (v.get("purchase") or {}).get("tracking") or {}
    return {
        "xcod": t.get("external_code") or t.get("xcod") or "",
        "sck": t.get("source_sck") or t.get("sck") or "",
        "src": t.get("source") or t.get("src") or "",
    }


def ler_xcod(xcod):
    """O xcod da Utmify chega como FB{sep}campanha|id{sep}conjunto|id{sep}anuncio|id{sep}posicionamento."""
    if not xcod or SEPARADOR_XCOD not in xcod:
        return None
    partes = xcod.split(SEPARADOR_XCOD)
    nomes = ["origem", "campanha", "conjunto", "anuncio", "posicionamento"]
    return {nomes[i]: partes[i] for i in range(min(len(partes), len(nomes)))}


def origem_curta(v):
    r = rastreamento(v)
    lido = ler_xcod(r["xcod"])
    if lido:
        return "%s > %s" % (lido.get("campanha", "?").split("|")[0], lido.get("anuncio", "?").split("|")[0])
    if r["src"]:
        return "src: " + r["src"][:60]
    if r["sck"]:
        return "sck: " + r["sck"][:60]
    return "sem rastreamento"


def cabecalho(titulo, ini, fim, pnome):
    return "%s | %s a %s%s" % (titulo, ini.strftime("%d/%m/%Y"), fim.strftime("%d/%m/%Y"),
                               " | produto: %s" % pnome if pnome else "")


# ---------------------------------------------------------------------------
# Ferramentas
# ---------------------------------------------------------------------------

def t_produtos(args):
    produtos = listar_produtos()
    busca = _normalizar(args.get("busca"))
    if busca:
        produtos = [p for p in produtos if busca in _normalizar(p.get("name"))]
    if not produtos:
        return "Nenhum produto encontrado."
    linhas = ["PRODUTOS NA HOTMART (%d)" % len(produtos), "id | código | status | formato | nome"]
    for p in sorted(produtos, key=lambda p: p.get("name", "")):
        linhas.append("%s | %s | %s | %s | %s" % (p.get("id"), p.get("ucode", "-"), p.get("status", "-"),
                                                  p.get("format", "-"), p.get("name")))
    return "\n".join(linhas)


def t_ofertas(args):
    pids, _ = resolver_produtos(args.get("produto"))
    if not pids:
        raise ErroHotmart("Informe o produto (nome ou id).")
    linhas = []
    for pid in pids:
        prod = next((p for p in listar_produtos() if str(p.get("id")) == pid), {})
        if not prod.get("ucode"):
            linhas.append("Não encontrei o código interno do produto %s." % pid)
            continue
        ofertas = paginar("/products/api/v1/products/%s/offers" % prod["ucode"], {}, limite=200)
        linhas += ["", "OFERTAS DE %s (%d)" % (prod.get("name"), len(ofertas)),
                   "código | principal | preço | pagamento | nome"]
        for o in ofertas:
            preco = o.get("price") or {}
            linhas.append("%s | %s | %s | %s | %s" % (
                o.get("code"), "sim" if o.get("is_main_offer") else "não",
                moeda(float(preco.get("value") or 0), preco.get("currency_code") or "BRL"),
                o.get("payment_mode", "-"), o.get("name") or "-"))
    return "\n".join(linhas).strip()


def t_vendas(args):
    vendas, ini, fim, pnome = buscar_vendas(args.get("periodo"), args.get("produto"), args.get("status"),
                                            limite=int(args.get("limite") or 200))
    if not vendas:
        return cabecalho("VENDAS", ini, fim, pnome) + "\nNenhuma venda no período."
    linhas = [cabecalho("VENDAS (%d)" % len(vendas), ini, fim, pnome),
              "data | transação | status | valor | pagamento | oferta | produto | origem"]
    for v in vendas:
        p = v.get("purchase") or {}
        val, cod = valor(v)
        linhas.append("%s | %s | %s | %s | %s | %s | %s | %s" % (
            _data(p.get("order_date")), p.get("transaction", "-"), NOME_STATUS.get(p.get("status"), p.get("status")),
            moeda(val, cod), (p.get("payment") or {}).get("type") or (p.get("payment") or {}).get("method") or "-",
            (p.get("offer") or {}).get("code", "-"), (v.get("product") or {}).get("name", "-"), origem_curta(v)))
    return "\n".join(linhas)


def t_resumo(args):
    vendas, ini, fim, pnome = buscar_vendas(args.get("periodo"), args.get("produto"), "todas")
    titulo = cabecalho("RESUMO DE VENDAS", ini, fim, pnome)
    if not vendas:
        return titulo + "\nNenhuma venda no período."
    grupo_de = {s: g for g, lista in GRUPOS_STATUS.items() if g != "todas" for s in lista}
    por_grupo = defaultdict(lambda: [0, 0.0])
    aprovadas = []
    for v in vendas:
        st = (v.get("purchase") or {}).get("status")
        g = grupo_de.get(st, "outras")
        por_grupo[g][0] += 1
        por_grupo[g][1] += valor(v)[0]
        if g == "aprovadas":
            aprovadas.append(v)
    linhas = [titulo, "", "POR STATUS"]
    for g in ["aprovadas", "pendentes", "reembolsos", "canceladas", "outras"]:
        if por_grupo[g][0]:
            linhas.append("%s: %d vendas | %s" % (g, por_grupo[g][0], moeda(por_grupo[g][1])))
    if aprovadas:
        total = sum(valor(v)[0] for v in aprovadas)
        linhas.append("ticket médio das aprovadas: %s" % moeda(total / len(aprovadas)))
        linhas += ["", "APROVADAS POR PRODUTO (order bump aparece como produto separado)"]
        for nome, qtd in Counter((v.get("product") or {}).get("name", "-") for v in aprovadas).most_common():
            linhas.append("%s: %d" % (nome, qtd))
        linhas += ["", "APROVADAS POR FORMA DE PAGAMENTO"]
        formas = Counter(((v.get("purchase") or {}).get("payment") or {}).get("type") or "-" for v in aprovadas)
        for forma, qtd in formas.most_common():
            linhas.append("%s: %d" % (forma, qtd))
        linhas += ["", "APROVADAS POR OFERTA"]
        for cod, qtd in Counter(((v.get("purchase") or {}).get("offer") or {}).get("code", "-")
                                for v in aprovadas).most_common():
            linhas.append("%s: %d" % (cod, qtd))
        linhas += ["", "APROVADAS POR DIA"]
        for dia, qtd in sorted(Counter(_dia((v.get("purchase") or {}).get("order_date")) for v in aprovadas).items()):
            linhas.append("%s: %d" % (dia, qtd))
    cartao = [v for v in vendas if ((v.get("purchase") or {}).get("payment") or {}).get("type") == "CREDIT_CARD"]
    if cartao:
        recusas = sum(1 for v in cartao if (v.get("purchase") or {}).get("status") in ("NO_FUNDS", "BLOCKED", "CANCELLED"))
        linhas += ["", "CARTÃO: %d tentativas, %d recusadas ou canceladas" % (len(cartao), recusas)]
    return "\n".join(linhas)


def t_rastreamento(args):
    vendas, ini, fim, pnome = buscar_vendas(args.get("periodo"), args.get("produto"), args.get("status") or "aprovadas")
    titulo = cabecalho("RASTREAMENTO DAS VENDAS", ini, fim, pnome)
    if not vendas:
        return titulo + "\nNenhuma venda no período."
    total = len(vendas)
    com_xcod = [v for v in vendas if ler_xcod(rastreamento(v)["xcod"])]
    com_src = [v for v in vendas if rastreamento(v)["src"]]
    com_sck = [v for v in vendas if rastreamento(v)["sck"]]
    sem_nada = [v for v in vendas if not any(rastreamento(v).values())]
    pct = lambda n: "%d de %d (%.0f%%)" % (n, total, 100.0 * n / total)
    linhas = [titulo, "",
              "com xcod da Utmify (atribuível a campanha e anúncio): " + pct(len(com_xcod)),
              "com src: " + pct(len(com_src)),
              "com sck: " + pct(len(com_sck)),
              "sem nenhum rastreamento: " + pct(len(sem_nada))]
    if com_xcod:
        camp, anuncio = Counter(), Counter()
        for v in com_xcod:
            lido = ler_xcod(rastreamento(v)["xcod"])
            camp[lido.get("campanha", "?")] += 1
            anuncio["%s > %s" % (lido.get("campanha", "?").split("|")[0], lido.get("anuncio", "?"))] += 1
        linhas += ["", "VENDAS POR CAMPANHA (pelo xcod)"] + ["%s: %d" % c for c in camp.most_common()]
        linhas += ["", "VENDAS POR ANÚNCIO (pelo xcod)"] + ["%s: %d" % a for a in anuncio.most_common()]
    outros = Counter()
    for v in vendas:
        if v in com_xcod:
            continue
        r = rastreamento(v)
        outros["src=%s | sck=%s" % (r["src"] or "-", r["sck"] or "-")] += 1
    if outros:
        linhas += ["", "VENDAS SEM XCOD, AGRUPADAS POR SRC E SCK"] + ["%s: %d" % o for o in outros.most_common(20)]
    por_dia = defaultdict(lambda: [0, 0])
    for v in vendas:
        d = _dia((v.get("purchase") or {}).get("order_date"))
        por_dia[d][0] += 1
        por_dia[d][1] += 1 if v in com_xcod else 0
    linhas += ["", "POR DIA (vendas | com xcod)"] + ["%s: %d | %d" % (d, a, b) for d, (a, b) in sorted(por_dia.items())]
    return "\n".join(linhas)


def t_compradores(args):
    vendas, ini, fim, pnome = buscar_vendas(args.get("periodo"), args.get("produto"), args.get("status") or "aprovadas")
    titulo = cabecalho("COMPRADORES", ini, fim, pnome)
    if not vendas:
        return titulo + "\nNenhuma venda no período."
    vistos, linhas = set(), [titulo, "data | nome | email | produto | status"]
    for v in vendas:
        b = v.get("buyer") or {}
        chave = ((b.get("email") or "").lower(), (v.get("product") or {}).get("id"))
        if chave in vistos:
            continue
        vistos.add(chave)
        p = v.get("purchase") or {}
        linhas.append("%s | %s | %s | %s | %s" % (_data(p.get("order_date")), b.get("name", "-"), b.get("email", "-"),
                                                  (v.get("product") or {}).get("name", "-"),
                                                  NOME_STATUS.get(p.get("status"), p.get("status"))))
    linhas.insert(1, "%d compradores únicos" % (len(linhas) - 2))
    return "\n".join(linhas)


def t_venda(args):
    transacao = (args.get("transacao") or "").strip()
    if not transacao:
        raise ErroHotmart("Informe o código da transação (começa com HP).")
    itens = api("/payments/api/v1/sales/history", {"transaction": transacao}).get("items") or []
    if not itens:
        itens = api("/payments/api/v1/sales/history",
                    {"transaction": transacao, "transaction_status": "WAITING_PAYMENT"}).get("items") or []
    if not itens:
        return "Transação %s não encontrada." % transacao
    v = itens[0]
    p, b = v.get("purchase") or {}, v.get("buyer") or {}
    val, cod = valor(v)
    r = rastreamento(v)
    lido = ler_xcod(r["xcod"])
    linhas = ["VENDA %s" % transacao,
              "produto: %s (id %s)" % ((v.get("product") or {}).get("name"), (v.get("product") or {}).get("id")),
              "comprador: %s | %s" % (b.get("name", "-"), b.get("email", "-")),
              "status: %s" % NOME_STATUS.get(p.get("status"), p.get("status")),
              "pedido em: %s | aprovado em: %s" % (_data(p.get("order_date")), _data(p.get("approved_date"))),
              "valor: %s | pagamento: %s em %s parcela(s)" % (
                  moeda(val, cod), (p.get("payment") or {}).get("type", "-"),
                  (p.get("payment") or {}).get("installments_number", 1)),
              "oferta: %s" % (p.get("offer") or {}).get("code", "-"),
              "", "RASTREAMENTO",
              "xcod: %s" % (r["xcod"] or "-"), "sck: %s" % (r["sck"] or "-"), "src: %s" % (r["src"] or "-")]
    if lido:
        linhas += ["campanha: %s" % lido.get("campanha", "-"), "conjunto: %s" % lido.get("conjunto", "-"),
                   "anúncio: %s" % lido.get("anuncio", "-"), "posicionamento: %s" % lido.get("posicionamento", "-")]
    try:
        det = api("/payments/api/v1/sales/price/details", {"transaction": transacao}).get("items") or []
        if det:
            d = det[0]
            linhas += ["", "DETALHE DO PREÇO"]
            for chave in ("base", "total", "vat", "fee", "real_conversion_rate"):
                if d.get(chave) is not None:
                    item = d.get(chave)
                    linhas.append("%s: %s" % (chave, moeda(float(item.get("value") or 0), item.get("currency_code", cod))
                                              if isinstance(item, dict) else item))
    except ErroHotmart:
        pass
    return "\n".join(linhas)


PERIODO = {"type": "string", "description": "hoje, ontem, 7d, 30d, mes, mes-passado ou AAAA-MM-DD:AAAA-MM-DD. Padrão: 30d"}
PRODUTO = {"type": "string", "description": "Nome (ou parte do nome) ou id do produto. Vazio = todos os produtos"}
STATUS = {"type": "string", "description": "aprovadas (padrão), pendentes, reembolsos, canceladas ou todas"}

REGISTRO = [
    ("hotmart_produtos", t_produtos, "Lista os produtos da conta Hotmart com id, código, status e formato.",
     {"busca": {"type": "string", "description": "Filtra pelo nome (opcional)"}}, []),
    ("hotmart_ofertas", t_ofertas, "Lista as ofertas de um produto (código da oferta, preço, se é a principal).",
     {"produto": PRODUTO}, ["produto"]),
    ("hotmart_vendas", t_vendas,
     "Lista as vendas do período, uma por linha: data, transação, status, valor, pagamento, oferta, produto e "
     "origem (campanha e anúncio lidos do xcod).",
     {"periodo": PERIODO, "produto": PRODUTO, "status": STATUS,
      "limite": {"type": "integer", "description": "Máximo de vendas listadas (padrão 200)"}}, []),
    ("hotmart_resumo", t_resumo,
     "Resumo do período: vendas por status, faturamento, ticket médio, produtos (inclui order bump), formas de "
     "pagamento, ofertas, vendas por dia e recusas de cartão.",
     {"periodo": PERIODO, "produto": PRODUTO}, []),
    ("hotmart_rastreamento", t_rastreamento,
     "Mostra quantas vendas chegaram com rastreamento (xcod, src, sck) e agrupa por campanha e anúncio. Serve para "
     "conferir a atribuição sem depender da Utmify.",
     {"periodo": PERIODO, "produto": PRODUTO, "status": STATUS}, []),
    ("hotmart_compradores", t_compradores,
     "Lista os compradores únicos do período (nome, email, produto e status). Útil para lista de participantes.",
     {"periodo": PERIODO, "produto": PRODUTO, "status": STATUS}, []),
    ("hotmart_venda", t_venda, "Mostra todos os detalhes de uma venda pelo código da transação, incluindo rastreamento.",
     {"transacao": {"type": "string", "description": "Código da transação (ex: HP1234567890)"}}, ["transacao"]),
]
TOOLS = {nome: (fn, desc, props, req) for nome, fn, desc, props, req in REGISTRO}


def montar_lista_tools():
    return [{"name": nome, "description": desc,
             "inputSchema": {"type": "object", "properties": props, "required": req}}
            for nome, (fn, desc, props, req) in TOOLS.items()]


# ---------------------------------------------------------------------------
# Protocolo MCP (stdio)
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
            except ErroHotmart as e:
                texto, erro = str(e), True
            except Exception as e:  # falha inesperada não pode derrubar o servidor
                texto, erro = "Erro inesperado no MCP da Hotmart: %s: %s" % (type(e).__name__, e), True
            responder(msg_id, {"content": [{"type": "text", "text": texto}], "isError": erro})
        elif msg_id is not None:
            responder(msg_id, {"content": [{"type": "text", "text": "Método não suportado"}], "isError": True})


if __name__ == "__main__":
    main()
