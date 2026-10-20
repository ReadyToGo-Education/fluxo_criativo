"""
trafego_fetch.py
Script unificado de busca de dados do Meta Ads para o trafego-analise (modo APP).

Faz TODAS as chamadas necessárias em uma única execução e salva o resultado
em cache local, na pasta passada em --cache-dir. A skill passa sempre a pasta
do produto ativo (meus-produtos/{ativo}/trafego/analise/cache); sem
--cache-dir, vale a pasta reserva skill-analise/cache/. Próximas chamadas
reutilizam o cache só no mesmo dia (fuso America/Sao_Paulo) e só se a busca anterior veio
completa; cache de outro dia, incompleto ou da versão antiga é ignorado e a
busca é refeita. Use --force para buscar de novo no mesmo dia.

Uso:
    python3 trafego_fetch.py \
        --account 1234567890123456 \
        --filtro "CURSO X" \
        --periodo last_30d \
        --status ACTIVE,PAUSED,WITH_ISSUES \
        --output diagnostico \
        --cache-dir meus-produtos/{ativo}/trafego/analise/cache

Período customizado: trocar --periodo por --since AAAA-MM-DD --until AAAA-MM-DD.

Saída: escreve JSON em stdout (UTF-8) + salva em
cache_dir/{account}_{periodo}_{filtro}_{status}_{output}.json
(no período customizado, {periodo} vira AAAAMMDD_AAAAMMDD).

Se a chamada principal (1a) falhar, devolve {"error": "falha_insights"} e não
grava cache. Se uma chamada complementar (1b, 1d ou 1e) falhar, o resultado sai
com _meta.falhas preenchido e o arquivo nunca é reaproveitado depois.

O nome do cache é montado por nome_cache() e rotulo_periodo(), que o
trafego_processar.py repete igual. Mudou um, mude o outro.

Não imprime o token em lugar nenhum (stdout, stderr ou cache).
"""

import sys
import re
import json
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, date, timedelta, timezone

GRAPH_VERSION = "v25.0"

STATUS_VALIDOS = ("ACTIVE", "PAUSED", "WITH_ISSUES", "ARCHIVED", "DELETED")
STATUS_PADRAO = "ACTIVE,PAUSED,WITH_ISSUES"

# Fuso de referência do cache: America/Sao_Paulo. O Brasil não tem horário de
# verão desde 2019, então UTC-3 fixo dá o mesmo dia sem depender de tzdata.
FUSO_SP = timezone(timedelta(hours=-3))


def hoje_sp():
    return datetime.now(FUSO_SP).date()


def write_out(data):
    """Saída JSON sempre em UTF-8, funciona em Windows (cp1252) e Mac (utf-8)."""
    sys.stdout.buffer.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    sys.stdout.buffer.write(b"\n")
    sys.stdout.buffer.flush()


def err(msg):
    sys.stderr.buffer.write(f"[ERRO] {msg}\n".encode("utf-8"))
    sys.stderr.buffer.flush()


def info(msg):
    sys.stderr.buffer.write(f"[INFO] {msg}\n".encode("utf-8"))
    sys.stderr.buffer.flush()


# ── Nome do cache (mesma regra no trafego_processar.py) ─────────────────────────

def parse_status(texto):
    """Converte "ACTIVE,PAUSED" em lista válida, sem repetição, na ordem informada."""
    lista = []
    for s in (texto or "").split(","):
        s = s.strip().upper()
        if s in STATUS_VALIDOS and s not in lista:
            lista.append(s)
    return lista


def slug_filtro(filtro):
    """Slug do filtro de nome para o arquivo de cache (seguro no Windows)."""
    s = (filtro or "").replace(" ", "_").replace("-", "").lower()
    s = re.sub(r"[^\w]", "", s)
    return s or "all"


def slug_status(status_list):
    """Slug curto do status (ex: ACTIVE,PAUSED,WITH_ISSUES -> apw)."""
    return "".join(s[0].lower() for s in status_list) or "all"


def rotulo_periodo(periodo, since=None, until=None):
    """Parte do nome do cache que identifica o período.

    Preset: o próprio preset (ex: last_30d). Customizado: AAAAMMDD_AAAAMMDD,
    sem aspas nem dois-pontos (seguro no Windows).
    """
    if since and until:
        return "{}_{}".format(since.replace("-", ""), until.replace("-", ""))
    return periodo


def nome_cache(account, periodo, filtro, status_list, output):
    return "{}_{}_{}_{}_{}.json".format(
        account, periodo, slug_filtro(filtro), slug_status(status_list), output
    )


def cache_invalido(cached):
    """Devolve o motivo para NÃO reaproveitar o cache, ou None se ele vale.

    Vale só o cache gerado hoje (fuso America/Sao_Paulo), com a busca completa
    (sem _meta.falhas) e com a série diária (1e) da versão atual.
    """
    if not isinstance(cached, dict):
        return "arquivo ilegível"
    meta = cached.get("_meta") or {}
    gerado = str(meta.get("gerado_em", ""))[:10]
    if gerado != hoje_sp().isoformat():
        return "gerado em outro dia ({})".format(gerado or "sem data")
    if meta.get("falhas"):
        return "busca anterior incompleta"
    if "1e" not in cached:
        return "versão antiga, sem a série diária"
    return None


# ── Chamadas HTTP ──────────────────────────────────────────────────────────────

def fetch(url, retries=3, backoff=5):
    """Faz GET com retry em rate limit."""
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(body)
                code = parsed.get("error", {}).get("code", 0)
            except Exception:
                code = 0
            # Rate limit: code 4 ou 17
            if code in (4, 17) and attempt < retries - 1:
                wait = backoff * (attempt + 1)
                err(f"Rate limit (code {code}). Aguardando {wait}s antes de tentar novamente...")
                time.sleep(wait)
                continue
            err(f"HTTP {e.code}: {body[:300]}")
            return {"error": body, "http_code": e.code}
        except urllib.error.URLError as e:
            # reason traz só o motivo de rede (ex: DNS, timeout), sem a URL.
            err(f"Falha de rede na requisição: {e.reason}")
            return {"error": "url_error"}
        except Exception as e:
            # Algumas exceções (ex: InvalidURL) repetem a URL inteira, que tem o token.
            # Por isso só o tipo da exceção é mostrado.
            err(f"Exceção na requisição: {type(e).__name__}")
            return {"error": type(e).__name__}
    return {"error": "max_retries_exceeded"}


def fetch_all_pages(base_params, account, endpoint, token):
    """Busca todas as páginas de um endpoint de insights ou campaigns."""
    params = dict(base_params)
    params["access_token"] = token
    url = "https://graph.facebook.com/{}/act_{}/{}?{}".format(
        GRAPH_VERSION, account, endpoint, urllib.parse.urlencode(params)
    )
    results = []
    while url:
        d = fetch(url)
        if "error" in d and "data" not in d:
            err(f"Falha ao buscar página: {str(d.get('error', ''))[:200]}")
            return None  # None = falha, [] = vazio válido
        results.extend(d.get("data", []))
        url = d.get("paging", {}).get("next")
    return results


def filtrar(lista, filtro):
    """Filtra campanhas pelo nome (case-insensitive, substring)."""
    if lista is None:
        return []
    filtro_lower = filtro.lower()
    return [c for c in lista if filtro_lower in c.get("campaign_name", c.get("name", "")).lower()]


def load_env(project_root):
    """Lê variáveis do .env sem dependências externas."""
    env_path = Path(project_root) / ".env"
    env = {}
    if not env_path.exists():
        return env
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", required=True)
    parser.add_argument("--filtro", default="")
    parser.add_argument("--periodo", default="last_30d",
                        help="Preset da API: last_7d, last_14d, last_30d. "
                             "Para período customizado, usar --since e --until.")
    parser.add_argument("--since", help="Início do período customizado (AAAA-MM-DD), junto com --until")
    parser.add_argument("--until", help="Fim do período customizado (AAAA-MM-DD), junto com --since")
    parser.add_argument("--status", default=STATUS_PADRAO,
                        help="Lista de effective_status separados por vírgula. "
                             "Valores: ACTIVE, PAUSED, WITH_ISSUES, ARCHIVED, DELETED. "
                             "Padrão ACTIVE,PAUSED,WITH_ISSUES (visão do presente sem arquivadas).")
    parser.add_argument("--output", default="diagnostico",
                        help="Tipo de output: diagnostico, performance, criativos, etc.")
    parser.add_argument("--cache-dir", default="skill-analise/cache",
                        help="Pasta do cache, relativa ao --project-root. A skill passa "
                             "meus-produtos/{ativo}/trafego/analise/cache; o padrão "
                             "skill-analise/cache é só a reserva de quem roda sem esse argumento.")
    parser.add_argument("--force", action="store_true",
                        help="Ignora cache e busca da API mesmo que cache exista")
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    status_list = parse_status(args.status)
    if not status_list:
        err(f"--status inválido: {args.status}. Use ACTIVE, PAUSED, WITH_ISSUES, ARCHIVED ou DELETED.")
        write_out({"error": "status_invalido"})
        return

    # Período customizado (--since/--until) ou preset (--periodo).
    custom_since = custom_until = None
    if args.since or args.until:
        try:
            custom_since = date.fromisoformat(str(args.since))
            custom_until = date.fromisoformat(str(args.until))
        except ValueError:
            err("Período customizado inválido. Informe --since e --until no formato AAAA-MM-DD.")
            write_out({"error": "periodo_invalido"})
            return
        if custom_since > custom_until:
            err("Período customizado inválido: --since depois de --until.")
            write_out({"error": "periodo_invalido"})
            return

    account = args.account.strip()
    if account.lower().startswith("act_"):
        account = account[4:]

    project_root = Path(args.project_root).resolve()
    cache_dir = project_root / args.cache_dir
    cache_dir.mkdir(parents=True, exist_ok=True)

    periodo_nome = rotulo_periodo(
        args.periodo,
        custom_since.isoformat() if custom_since else None,
        custom_until.isoformat() if custom_until else None,
    )

    # Nome do cache inclui o slug do status para filtros diferentes não colidirem.
    cache_file = cache_dir / nome_cache(account, periodo_nome, args.filtro, status_list, args.output)

    # Usar cache só se for de hoje, completo e da versão atual (e sem --force).
    if cache_file.exists() and not args.force:
        try:
            with open(cache_file, "rb") as f:
                cached = json.loads(f.read())
        except (OSError, ValueError):
            cached = None
        motivo = cache_invalido(cached)
        if motivo is None:
            cached["_from_cache"] = True
            cached["_cache_file"] = str(cache_file)
            write_out(cached)
            return
        # Apaga o cache vencido já aqui: se a busca nova falhar, o
        # trafego_processar.py não lê número velho como se fosse atual.
        try:
            cache_file.unlink()
        except OSError:
            pass
        info(f"Cache ignorado ({motivo}). Buscando de novo na API.")

    # Carregar token do .env (nunca é impresso)
    env = load_env(project_root)
    token = env.get("FB_ACCESS_TOKEN_PERMANENTE", "")
    if not token:
        err("FB_ACCESS_TOKEN_PERMANENTE não encontrado no .env")
        write_out({"error": "token_missing"})
        return

    periodo = args.periodo
    filtro = args.filtro

    # Parâmetro de período das chamadas 1a e 1e: date_preset ou time_range (customizado).
    if custom_since:
        param_periodo = {"time_range": json.dumps({"since": custom_since.isoformat(),
                                                   "until": custom_until.isoformat()})}
        dias_periodo = (custom_until - custom_since).days + 1
    else:
        param_periodo = {"date_preset": periodo}
        periodo_dias_map = {"last_7d": 7, "last_14d": 14, "last_30d": 30}
        dias_periodo = periodo_dias_map.get(periodo)

    # ── CHAMADA 0: IDs de campanhas permitidos pelo --status ──
    # O /insights não aceita effective_status. Solução: listar as campanhas via
    # /campaigns (que aceita) e filtrar todas as chamadas seguintes pelo conjunto
    # de IDs permitidos. Sem isso, o /insights devolve métricas de qualquer campanha
    # que gastou no período, inclusive PAUSED/ARCHIVED/DELETED, e infla os dados.
    todas_camps = fetch_all_pages(
        {
            "fields": "id,name,status,effective_status,objective,daily_budget,lifetime_budget,budget_remaining",
            "effective_status": json.dumps(status_list),
            "limit": 500,
        },
        account, "campaigns", token
    )
    if todas_camps is None:
        err("Falha ao listar campanhas com filtro de status. Abortando.")
        write_out({"error": "falha_listar_campanhas"})
        return
    todas_camps_filtradas = filtrar(todas_camps, filtro)
    ids_permitidos = {c["id"] for c in todas_camps_filtradas if c.get("id")}
    info(f"Campanhas no escopo (status={','.join(status_list)}, filtro='{filtro}'): {len(ids_permitidos)}")

    def filtrar_por_id(lista):
        """Mantém apenas linhas cujo campaign_id está no conjunto permitido."""
        if lista is None:
            return []
        return [c for c in lista if c.get("campaign_id") in ids_permitidos]

    # ── CHAMADA 1A: Métricas principais do período ──
    # Campos do nível campaign. landing_page_views NÃO vai no fields (erro 400):
    # o valor vem dentro de actions como landing_page_view.
    campos_1a = ",".join([
        "campaign_id", "campaign_name", "spend", "impressions", "clicks",
        "ctr", "cpm", "cpc", "reach", "frequency",
        "actions", "action_values", "cost_per_action_type",
        "date_start", "date_stop",
    ])
    all_1a = fetch_all_pages(
        dict({"fields": campos_1a, "level": "campaign", "limit": 500}, **param_periodo),
        account, "insights", token
    )
    if all_1a is None:
        # Falha não é "zero campanhas": não grava cache.
        err("Falha ao buscar as métricas do período (chamada 1a). Nada foi salvo no cache.")
        write_out({"error": "falha_insights", "chamada": "1a"})
        return
    camps_1a = filtrar_por_id(all_1a)

    # Chamadas complementares que falharem entram aqui (o resultado não vira cache reaproveitável).
    falhas = []

    # Janela do período anterior (1b): MESMO tamanho do período principal,
    # terminando 1 dia antes do início dele. No customizado, sai das datas
    # informadas. No preset, é ancorada no date_start que a Meta devolveu no 1a
    # (fuso da conta), nunca no relógio do computador. Só sem nenhuma linha no 1a
    # usa hoje (America/Sao_Paulo) como reserva.
    wow_since = wow_until = None
    if dias_periodo:
        if custom_since:
            inicio_atual = custom_since
        else:
            inicio_atual = None
            for linha in all_1a:
                try:
                    inicio_atual = date.fromisoformat(str(linha.get("date_start", "")))
                    break
                except ValueError:
                    continue
            if inicio_atual is None:
                inicio_atual = hoje_sp() - timedelta(days=dias_periodo)
        wow_until = inicio_atual - timedelta(days=1)
        wow_since = wow_until - timedelta(days=dias_periodo - 1)

    # ── CHAMADA 1B: Comparativo do período anterior (mesma duração) ──
    # time_range fechado, sem time_increment: uma linha agregada por campanha
    # cobrindo a janela anterior inteira. O processar compara 1a inteiro x 1b inteiro.
    camps_1b = []
    if wow_since and wow_until:
        all_1b = fetch_all_pages(
            {
                "fields": "campaign_id,campaign_name,spend,impressions,clicks,ctr,cpm,reach,frequency,actions,action_values,cost_per_action_type,date_start,date_stop",
                "level": "campaign",
                "time_range": json.dumps({"since": wow_since.isoformat(), "until": wow_until.isoformat()}),
                "limit": 500,
            },
            account, "insights", token
        )
        if all_1b is None:
            falhas.append("1b")
        camps_1b = filtrar_por_id(all_1b)

    # ── CHAMADA 1C: Orçamentos das campanhas ──
    # Reusa a lista da Chamada 0 (mesmo filtro de status, mesmos campos de
    # orçamento). Evita uma chamada redundante à Graph API.
    camps_1c = todas_camps_filtradas

    # ── CHAMADA 1D: Gasto de hoje ──
    all_1d = fetch_all_pages(
        {"fields": "campaign_id,campaign_name,spend", "level": "campaign", "date_preset": "today", "limit": 500},
        account, "insights", token
    )
    if all_1d is None:
        falhas.append("1d")
    camps_1d = filtrar_por_id(all_1d)

    # ── CHAMADA 1E: Série diária do período (gráfico de tendência) ──
    # level=campaign + time_increment=1 => uma linha por campanha por dia.
    # Filtra pelos mesmos IDs do 1a; o processar agrupa por date_start.
    # NÃO usa level=account: o filtro de campanha precisa ser respeitado para
    # a soma diária bater com o agregado filtrado do dashboard.
    all_1e = fetch_all_pages(
        dict({
            "fields": "campaign_id,campaign_name,spend,impressions,actions,action_values,date_start",
            "level": "campaign",
            "time_increment": 1,
            "limit": 500,
        }, **param_periodo),
        account, "insights", token
    )
    if all_1e is None:
        falhas.append("1e")
    camps_1e = filtrar_por_id(all_1e)

    result = {
        "_meta": {
            "account": account,
            "filtro": filtro,
            "periodo": periodo_nome,
            "since": custom_since.isoformat() if custom_since else None,
            "until": custom_until.isoformat() if custom_until else None,
            "janela_anterior": [wow_since.isoformat(), wow_until.isoformat()] if wow_since else None,
            "output": args.output,
            "status_filter": status_list,
            "campanhas_no_escopo": len(ids_permitidos),
            "gerado_em": datetime.now(FUSO_SP).isoformat(timespec="seconds"),
            "falhas": falhas,
            "camps_1a": len(camps_1a),
            "camps_1b": len(camps_1b),
            "camps_1c": len(camps_1c),
            "camps_1d": len(camps_1d),
            "camps_1e": len(camps_1e),
        },
        "_from_cache": False,
        "_cache_file": str(cache_file),
        "1a": camps_1a,
        "1b": camps_1b,
        "1c": camps_1c,
        "1d": camps_1d,
        "1e": camps_1e,
    }

    # Salvar cache. Com falha em chamada complementar, o arquivo é gravado só para o
    # trafego_processar.py desta execução ler (com _meta.falhas preenchido) e nunca
    # é reaproveitado: cache_invalido() recusa e a próxima execução busca de novo.
    if falhas:
        err("Algumas chamadas complementares falharam ({}). Este resultado não será "
            "reaproveitado: a próxima execução busca de novo.".format(", ".join(falhas)))
    with open(cache_file, "wb") as f:
        f.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

    write_out(result)


if __name__ == "__main__":
    main()
