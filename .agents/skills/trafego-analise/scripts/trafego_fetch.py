"""
trafego_fetch.py
Script unificado de busca de dados do Meta Ads para o trafego-analise.

Faz TODAS as chamadas necessarias em uma unica execucao e salva o resultado
em cache local (skill-analise/cache/). Proximas chamadas reutilizam o cache
da mesma sessao sem bater na API novamente.

Uso:
    python3 trafego_fetch.py \
        --account <AD_ACCOUNT_ID> \
        --filtro "VTSD - CV" \
        --periodo last_30d \
        --output diagnostico \
        --cache-dir skill-analise/cache

Saida: escreve JSON em stdout (UTF-8) + salva em cache_dir/{account}_{periodo}_{output}.json
"""

import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime


def write_out(data):
    """Saida JSON sempre em UTF-8, funciona em Windows (cp1252) e Mac (utf-8)."""
    sys.stdout.buffer.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    sys.stdout.buffer.write(b"\n")
    sys.stdout.buffer.flush()


def err(msg):
    sys.stderr.buffer.write(f"[ERRO] {msg}\n".encode("utf-8"))
    sys.stderr.buffer.flush()


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
        except Exception as e:
            err(f"Excecao na requisicao: {e}")
            return {"error": str(e)}
    return {"error": "max_retries_exceeded"}


def fetch_all_pages(base_params, account, endpoint, token):
    """Busca todas as paginas de um endpoint de insights ou campaigns."""
    params = dict(base_params)
    params["access_token"] = token
    url = "https://graph.facebook.com/v21.0/act_{}/{}?{}".format(
        account, endpoint, urllib.parse.urlencode(params)
    )
    results = []
    while url:
        d = fetch(url)
        if "error" in d and "data" not in d:
            err(f"Falha ao buscar pagina: {d.get('error','')[:200]}")
            return None  # None = falha, [] = vazio valido
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
    """Le variaveis do .env sem dependencias externas."""
    env_path = Path(project_root) / ".env"
    env = {}
    if not env_path.exists():
        return env
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip()
    return env


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", required=True)
    parser.add_argument("--filtro", default="")
    parser.add_argument("--periodo", default="last_30d",
                        help="Preset da API: last_7d, last_14d, last_30d, last_60d")
    parser.add_argument("--output", default="diagnostico",
                        help="Tipo de output: diagnostico, performance, criativos, etc.")
    parser.add_argument("--status", default="ACTIVE,PAUSED,WITH_ISSUES",
                        help="Lista de effective_status separados por virgula. "
                             "Valores: ACTIVE, PAUSED, WITH_ISSUES, ARCHIVED, DELETED. "
                             "Default ACTIVE,PAUSED,WITH_ISSUES (visao do presente sem arquivadas).")
    parser.add_argument("--cache-dir", default="skill-analise/cache")
    parser.add_argument("--force", action="store_true",
                        help="Ignora cache e busca da API mesmo que cache exista")
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    cache_dir = project_root / args.cache_dir
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Parsear status e montar slug curto pro cache (ex: "ACTIVE,PAUSED" -> "ap")
    status_list = [s.strip().upper() for s in args.status.split(",") if s.strip()]
    status_valid = {"ACTIVE", "PAUSED", "WITH_ISSUES", "ARCHIVED", "DELETED"}
    status_list = [s for s in status_list if s in status_valid]
    if not status_list:
        err(f"--status invalido: {args.status}. Use ACTIVE, PAUSED, WITH_ISSUES, ARCHIVED ou DELETED.")
        write_out({"error": "status_invalido"})
        return
    status_slug = "".join(s[0].lower() for s in status_list)

    # Nome do arquivo de cache (inclui status_slug pra cache nao colidir)
    filtro_slug = args.filtro.replace(" ", "_").replace("-", "").lower() or "all"
    cache_file = cache_dir / f"{args.account}_{args.periodo}_{filtro_slug}_{status_slug}_{args.output}.json"

    # Usar cache se existir e nao forcar
    if cache_file.exists() and not args.force:
        with open(cache_file, "rb") as f:
            cached = json.loads(f.read())
        cached["_from_cache"] = True
        cached["_cache_file"] = str(cache_file)
        write_out(cached)
        return

    # Carregar token do .env
    env = load_env(project_root)
    token = env.get("FB_ACCESS_TOKEN_PERMANENTE", "")
    if not token:
        err("FB_ACCESS_TOKEN_PERMANENTE nao encontrado no .env")
        write_out({"error": "token_missing"})
        return

    account = args.account
    periodo = args.periodo
    filtro = args.filtro

    # Calcula janela do periodo anterior usando time_range com datas explicitas.
    # Evita usar presets compostos (ex: last_60d) que nao existem na Graph API v21.
    # A janela anterior tem o MESMO tamanho do periodo principal e termina 1 dia
    # antes do inicio do periodo principal.
    from datetime import date, timedelta
    periodo_dias_map = {"last_7d": 7, "last_14d": 14, "last_30d": 30}
    dias_periodo = periodo_dias_map.get(periodo)
    wow_since = wow_until = None
    if dias_periodo:
        # Periodo principal vai de hoje - dias_periodo ate ontem (Meta exclui hoje em "last_Nd").
        inicio_atual = date.today() - timedelta(days=dias_periodo)
        wow_until = inicio_atual - timedelta(days=1)
        wow_since = wow_until - timedelta(days=dias_periodo - 1)

    # ── CHAMADA 0: Listar IDs de campanhas permitidos pelo --status ──
    # /insights nao aceita effective_status. Solucao: buscar a lista de campanhas
    # via /campaigns (que aceita) e filtrar todas as chamadas seguintes pelo conjunto
    # de IDs permitidos. Sem isso, /insights retorna metricas de qualquer campanha
    # que teve gasto no periodo, incluindo PAUSED/ARCHIVED/DELETED — inflando os dados.
    status_filter_param = json.dumps(status_list)
    todas_camps = fetch_all_pages(
        {
            "fields": "id,name,status,effective_status,daily_budget,lifetime_budget,budget_remaining",
            "effective_status": status_filter_param,
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
        """Mantem apenas campanhas cujo campaign_id esta no conjunto permitido."""
        if lista is None:
            return []
        return [c for c in lista if c.get("campaign_id") in ids_permitidos]

    # ── CHAMADA 1A: Metricas principais do periodo ──
    # Campos do nivel campaign (sem landing_page_views que so existe em ad level)
    campos_1a = ",".join([
        "campaign_id", "campaign_name", "spend", "impressions", "clicks",
        "ctr", "cpm", "cpc", "reach", "frequency",
        "actions", "action_values", "cost_per_action_type",
    ])
    all_1a = fetch_all_pages(
        {"fields": campos_1a, "level": "campaign", "date_preset": periodo, "limit": 500},
        account, "insights", token
    )
    camps_1a = filtrar_por_id(all_1a)

    # ── CHAMADA 1B: Comparativo do periodo anterior (mesma duracao) ──
    # Usa time_range com datas explicitas em vez de preset combinado com time_increment.
    # Retorna 1 linha agregada por campanha cobrindo a janela inteira do periodo anterior.
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
        camps_1b = filtrar_por_id(all_1b)

    # ── CHAMADA 1C: Orcamentos das campanhas ──
    # Reusa a lista ja buscada na Chamada 0 (mesmo filtro de status, mesmos campos
    # de orcamento). Evita uma chamada redundante a Graph API.
    camps_1c = todas_camps_filtradas

    # ── CHAMADA 1D: Gasto de hoje ──
    all_1d = fetch_all_pages(
        {"fields": "campaign_id,campaign_name,spend", "level": "campaign", "date_preset": "today", "limit": 500},
        account, "insights", token
    )
    camps_1d = filtrar_por_id(all_1d)

    result = {
        "_meta": {
            "account": account,
            "filtro": filtro,
            "periodo": periodo,
            "output": args.output,
            "status_filter": status_list,
            "campanhas_no_escopo": len(ids_permitidos),
            "gerado_em": datetime.now().isoformat(),
            "camps_1a": len(camps_1a),
            "camps_1b": len(camps_1b),
            "camps_1c": len(camps_1c),
            "camps_1d": len(camps_1d),
        },
        "_from_cache": False,
        "_cache_file": str(cache_file),
        "1a": camps_1a,
        "1b": camps_1b,
        "1c": camps_1c,
        "1d": camps_1d,
    }

    # Salvar cache
    with open(cache_file, "wb") as f:
        f.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

    write_out(result)


if __name__ == "__main__":
    main()
