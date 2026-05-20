"""
trafego_processar.py
Script de processamento de dados do Meta Ads para o trafego-analise.

Le o cache gerado pelo trafego_fetch.py e calcula todos os KPIs:
- ROAS, CPA, connect rate
- Health Score (5 dimensoes, pesos definidos na sub-skill 1-diagnostico-rapido.md)
- Ranking de queima de dinheiro (gasto sem conversao)
- Lista de fadiga de criativo (frequencia alta + CTR caindo)
- Alertas de budget (daily budget quase esgotado hoje)

Uso:
    python3 trafego_processar.py \
        --cache-file skill-analise/cache/<AD_ACCOUNT_ID>_last_30d_vtsdcv_diagnostico.json \
        --ticket 497 \
        --output diagnostico

Ou informando os mesmos args do fetch (o script monta o caminho do cache):
    python3 trafego_processar.py \
        --account <AD_ACCOUNT_ID> \
        --filtro "VTSD - CV" \
        --periodo last_30d \
        --output diagnostico \
        --cache-dir skill-analise/cache

Saida: JSON estruturado com metricas, sinais e health score.
"""

import sys
import os
import json
import argparse
from pathlib import Path


def write_out(data):
    """Saida JSON sempre em UTF-8, funciona em Windows (cp1252) e Mac (utf-8)."""
    sys.stdout.buffer.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    sys.stdout.buffer.write(b"\n")
    sys.stdout.buffer.flush()


def err(msg):
    sys.stderr.buffer.write(f"[ERRO] {msg}\n".encode("utf-8"))
    sys.stderr.buffer.flush()


def info(msg):
    sys.stderr.buffer.write(f"[INFO] {msg}\n".encode("utf-8"))
    sys.stderr.buffer.flush()


# ── Extratores de actions ──────────────────────────────────────────────────────

def get_action(actions, action_type, default=0.0):
    """Extrai valor de um tipo de acao da lista actions da API."""
    if not actions:
        return default
    for a in actions:
        if a.get("action_type") == action_type:
            return float(a.get("value", 0))
    return default


def get_action_value(action_values, action_type, default=0.0):
    """Extrai valor monetario de action_values."""
    if not action_values:
        return default
    for a in action_values:
        if a.get("action_type") == action_type:
            return float(a.get("value", 0))
    return default


def get_cost_per(cost_list, action_type, default=None):
    """Extrai custo por acao de cost_per_action_type."""
    if not cost_list:
        return default
    for a in cost_list:
        if a.get("action_type") == action_type:
            return float(a.get("value", 0))
    return default


# ── Classificacao de funil ─────────────────────────────────────────────────────

def classificar_funil(ticket):
    """Retorna (tipo, roas_min, cpa_max_pct) com base no ticket."""
    if ticket is None:
        return ("desconhecido", 3.0, 0.30)
    if ticket <= 97:
        return ("low_ticket", 2.5, 0.40)
    if ticket <= 497:
        return ("mid_ticket", 3.0, 0.30)
    return ("high_ticket", 4.0, 0.25)


# ── Metricas agregadas ─────────────────────────────────────────────────────────

def agregar_campanhas(camps):
    """Agrega metricas de uma lista de campanhas (nivel campaign insights)."""
    total_spend = 0.0
    total_impressions = 0
    total_clicks = 0
    total_reach = 0
    total_purchases = 0.0
    total_purchase_value = 0.0
    total_leads = 0.0
    total_link_clicks = 0.0
    total_lpv = 0.0
    freq_list = []

    for c in camps:
        spend = float(c.get("spend", 0) or 0)
        total_spend += spend
        total_impressions += int(c.get("impressions", 0) or 0)
        total_clicks += int(c.get("clicks", 0) or 0)
        total_reach += int(c.get("reach", 0) or 0)

        freq = float(c.get("frequency", 0) or 0)
        if freq > 0:
            freq_list.append(freq)

        actions = c.get("actions", [])
        action_values = c.get("action_values", [])

        # Compras (pixel purchase)
        total_purchases += get_action(actions, "offsite_conversion.fb_pixel_purchase")
        total_purchase_value += get_action_value(action_values, "offsite_conversion.fb_pixel_purchase")

        # Leads
        total_leads += get_action(actions, "offsite_conversion.fb_pixel_lead")
        total_leads += get_action(actions, "lead")  # formato alternativo

        # Link clicks (outbound) — diferente de clicks total
        total_link_clicks += get_action(actions, "link_click")

        # Landing page views — campo dentro de actions (nao campo topo nivel!)
        total_lpv += get_action(actions, "landing_page_view")

    return {
        "spend": round(total_spend, 2),
        "impressions": total_impressions,
        "clicks": total_clicks,
        "reach": total_reach,
        "purchases": round(total_purchases, 1),
        "purchase_value": round(total_purchase_value, 2),
        "leads": round(total_leads, 1),
        "link_clicks": round(total_link_clicks, 1),
        "lpv": round(total_lpv, 1),
        "freq_avg": round(sum(freq_list) / len(freq_list), 2) if freq_list else 0.0,
    }


# ── KPIs derivados ─────────────────────────────────────────────────────────────

def calcular_kpis(agg, ticket=None):
    """Calcula KPIs derivados a partir das metricas agregadas."""
    spend = agg["spend"]
    purchases = agg["purchases"]
    purchase_value = agg["purchase_value"]
    leads = agg["leads"]
    link_clicks = agg["link_clicks"]
    lpv = agg["lpv"]
    impressions = agg["impressions"]
    clicks = agg["clicks"]

    # ROAS
    roas = round(purchase_value / spend, 3) if spend > 0 and purchase_value > 0 else 0.0

    # CPA (custo por compra ou por lead)
    cpa_purchase = round(spend / purchases, 2) if purchases > 0 else None
    cpa_lead = round(spend / leads, 2) if leads > 0 else None
    cpa = cpa_purchase or cpa_lead

    # CTR (porcentagem)
    ctr = round((clicks / impressions) * 100, 3) if impressions > 0 else 0.0

    # CPM
    cpm = round((spend / impressions) * 1000, 2) if impressions > 0 else 0.0

    # CPC (custo por clique total, nao link click)
    cpc = round(spend / clicks, 2) if clicks > 0 else 0.0

    # Connect Rate: LPV / link_clicks (outbound, nao total clicks)
    # Nota: link_clicks e a metrica correta pois representa cliques reais para fora
    # Total clicks inclui engajamento no post, que nao gera visita real na pagina
    connect_rate = round((lpv / link_clicks) * 100, 1) if link_clicks > 0 else None
    # Fallback: se nao tem link_clicks separado, usar total clicks
    if connect_rate is None and clicks > 0 and lpv > 0:
        connect_rate = round((lpv / clicks) * 100, 1)

    return {
        "roas": roas,
        "cpa": cpa,
        "cpa_purchase": cpa_purchase,
        "cpa_lead": cpa_lead,
        "ctr": ctr,
        "cpm": cpm,
        "cpc": cpc,
        "connect_rate": connect_rate,
    }


# ── Por campanha ───────────────────────────────────────────────────────────────

def processar_campanha(c):
    """Extrai e calcula metricas de uma campanha individual."""
    spend = float(c.get("spend", 0) or 0)
    impressions = int(c.get("impressions", 0) or 0)
    clicks = int(c.get("clicks", 0) or 0)
    freq = float(c.get("frequency", 0) or 0)
    ctr_raw = float(c.get("ctr", 0) or 0)
    actions = c.get("actions", [])
    action_values = c.get("action_values", [])

    purchases = get_action(actions, "offsite_conversion.fb_pixel_purchase")
    purchase_value = get_action_value(action_values, "offsite_conversion.fb_pixel_purchase")
    leads = get_action(actions, "offsite_conversion.fb_pixel_lead") + get_action(actions, "lead")
    link_clicks = get_action(actions, "link_click")
    lpv = get_action(actions, "landing_page_view")

    roas = round(purchase_value / spend, 3) if spend > 0 and purchase_value > 0 else 0.0
    conversions = purchases or leads
    cpa = round(spend / conversions, 2) if conversions > 0 else None

    connect_rate = round((lpv / link_clicks) * 100, 1) if link_clicks > 0 else None
    if connect_rate is None and clicks > 0 and lpv > 0:
        connect_rate = round((lpv / clicks) * 100, 1)

    return {
        "campaign_id": c.get("campaign_id", ""),
        "campaign_name": c.get("campaign_name", ""),
        "spend": round(spend, 2),
        "impressions": impressions,
        "clicks": clicks,
        "frequency": round(freq, 2),
        "ctr": round(ctr_raw * 100, 3) if ctr_raw < 1 else round(ctr_raw, 3),
        "purchases": round(purchases, 1),
        "purchase_value": round(purchase_value, 2),
        "leads": round(leads, 1),
        "link_clicks": round(link_clicks, 1),
        "lpv": round(lpv, 1),
        "roas": roas,
        "cpa": cpa,
        "conversions": round(conversions, 1),
        "connect_rate": connect_rate,
    }


# ── Sinais ────────────────────────────────────────────────────────────────────

def detectar_queima(camps_1a, limite_spend=50.0):
    """Campanhas com gasto > limite e zero conversoes — queima de dinheiro."""
    queimadoras = []
    for c in camps_1a:
        proc = processar_campanha(c)
        if proc["spend"] > limite_spend and proc["conversions"] == 0:
            queimadoras.append(proc)
    queimadoras.sort(key=lambda x: x["spend"], reverse=True)
    return queimadoras[:5]  # top 5


def detectar_fadiga(camps_1a, camps_1b, freq_minima=4.0, queda_ctr_pct=15.0):
    """Campanhas com frequencia alta e CTR caindo vs periodo anterior."""
    # Indexar period anterior por campaign_id
    ctr_anterior = {}
    for c in camps_1b:
        cid = c.get("campaign_id", "")
        ctr_val = float(c.get("ctr", 0) or 0)
        # Normalizar: API pode retornar 0-1 ou 0-100
        if ctr_val < 1:
            ctr_val *= 100
        if cid not in ctr_anterior or c.get("date_start", "") > ctr_anterior[cid].get("date_start", ""):
            ctr_anterior[cid] = {"ctr": ctr_val, "date_start": c.get("date_start", "")}

    fadigadas = []
    for c in camps_1a:
        proc = processar_campanha(c)
        freq = proc["frequency"]
        ctr_atual = proc["ctr"]
        if ctr_atual < 1:
            ctr_atual *= 100  # normalizar

        if freq < freq_minima:
            continue

        cid = proc["campaign_id"]
        if cid in ctr_anterior:
            ctr_ant = ctr_anterior[cid]["ctr"]
            if ctr_ant > 0:
                queda = ((ctr_ant - ctr_atual) / ctr_ant) * 100
                if queda >= queda_ctr_pct:
                    fadigadas.append({
                        **proc,
                        "ctr_anterior": round(ctr_ant, 3),
                        "queda_ctr_pct": round(queda, 1),
                    })
        else:
            # Sem dado anterior mas freq alta — considerar risco
            if freq >= 5.0:
                fadigadas.append({
                    **proc,
                    "ctr_anterior": None,
                    "queda_ctr_pct": None,
                })

    fadigadas.sort(key=lambda x: x["frequency"], reverse=True)
    return fadigadas[:3]


def detectar_saturacao(camps_1a, freq_minima=5.0):
    """Campanhas com objetivo de trafego frio e frequencia alta."""
    saturadas = []
    for c in camps_1a:
        proc = processar_campanha(c)
        if proc["frequency"] >= freq_minima:
            saturadas.append(proc)
    saturadas.sort(key=lambda x: x["frequency"], reverse=True)
    return saturadas[:3]


def detectar_budget(camps_1c, camps_1d, pct_alerta=0.90):
    """Campanhas com daily budget quase esgotado hoje."""
    spend_hoje = {}
    for c in camps_1d:
        cid = c.get("campaign_id", "")
        spend_hoje[cid] = float(c.get("spend", 0) or 0)

    alertas = []
    for c in camps_1c:
        cid = c.get("id", "")
        nome = c.get("name", "")
        daily_budget = c.get("daily_budget")
        lifetime_budget = c.get("lifetime_budget")
        budget_remaining = c.get("budget_remaining")

        if daily_budget:
            # API retorna em centavos
            daily_budget_reais = int(daily_budget) / 100.0
            gasto_hoje = spend_hoje.get(cid, 0.0)
            if daily_budget_reais > 0:
                pct = gasto_hoje / daily_budget_reais
                restante = daily_budget_reais - gasto_hoje
                if pct >= pct_alerta:
                    alertas.append({
                        "campaign_id": cid,
                        "campaign_name": nome,
                        "daily_budget": round(daily_budget_reais, 2),
                        "spend_hoje": round(gasto_hoje, 2),
                        "restante": round(restante, 2),
                        "pct_consumido": round(pct * 100, 1),
                        "tipo": "daily_budget",
                    })
        elif budget_remaining is not None and lifetime_budget:
            remaining_reais = int(budget_remaining) / 100.0
            lifetime_reais = int(lifetime_budget) / 100.0
            if lifetime_reais > 0:
                pct_usado = 1 - (remaining_reais / lifetime_reais)
                if pct_usado >= pct_alerta:
                    alertas.append({
                        "campaign_id": cid,
                        "campaign_name": nome,
                        "lifetime_budget": round(lifetime_reais, 2),
                        "budget_remaining": round(remaining_reais, 2),
                        "pct_consumido": round(pct_usado * 100, 1),
                        "tipo": "lifetime_budget",
                    })

    alertas.sort(key=lambda x: x["pct_consumido"], reverse=True)
    return alertas


# ── Health Score ───────────────────────────────────────────────────────────────

def calcular_health_score(camps_1a, camps_1b, agg, kpis, ticket_tipo):
    """
    Calcula o Health Score com 5 dimensoes conforme 1-diagnostico-rapido.md.
    D1 (20%) = Diversidade criativa (proxy: campanhas ativas com spend > 10)
    D2 (20%) = Saude de publicos (% campanhas com freq <= 3)
    D3 (25%) = Eficiencia de funil (connect rate)
    D4 (25%) = Performance financeira (ROAS vs benchmark)
    D5 (10%) = Consistencia temporal (variacao de CPA WoW)
    """
    detalhes = {}

    # Dimensao 1 — Diversidade criativa
    camps_com_gasto = [c for c in camps_1a if float(c.get("spend", 0) or 0) > 10]
    n_ativas = len(camps_com_gasto)
    if n_ativas >= 10:
        d1 = 100
    elif n_ativas >= 6:
        d1 = 75
    elif n_ativas >= 3:
        d1 = 50
    elif n_ativas == 2:
        d1 = 30
    elif n_ativas == 1:
        d1 = 15
    else:
        d1 = 0
    detalhes["d1"] = {"score": d1, "camps_com_gasto": n_ativas, "descricao": "Diversidade criativa"}

    # Dimensao 2 — Saude de publicos
    total_camps = len(camps_1a)
    if total_camps == 0:
        d2 = 0
    else:
        freq_ok = sum(1 for c in camps_1a if float(c.get("frequency", 0) or 0) <= 3)
        pct_ok = freq_ok / total_camps
        if pct_ok >= 1.0:
            d2 = 100
        elif pct_ok >= 0.75:
            d2 = 80
        elif pct_ok >= 0.50:
            d2 = 55
        elif pct_ok >= 0.25:
            d2 = 30
        else:
            d2 = 10
        # Penalidade: freq > 6
        freq_critica = any(float(c.get("frequency", 0) or 0) > 6 for c in camps_1a)
        if freq_critica:
            d2 = max(0, d2 - 10)
        detalhes["d2"] = {
            "score": d2,
            "pct_freq_ok": round(pct_ok * 100, 1),
            "penalidade_freq_critica": freq_critica,
            "descricao": "Saude de publicos",
        }

    # Dimensao 3 — Eficiencia de funil (connect rate)
    connect_rate = kpis.get("connect_rate")
    if connect_rate is not None:
        if connect_rate >= 70:
            d3 = 100
        elif connect_rate >= 55:
            d3 = 75
        elif connect_rate >= 40:
            d3 = 50
        elif connect_rate >= 20:
            d3 = 25
        else:
            d3 = 10
        detalhes["d3"] = {"score": d3, "connect_rate": connect_rate, "metodo": "lpv_link_clicks", "descricao": "Eficiencia de funil"}
    else:
        # Fallback: CTR medio
        ctr = kpis.get("ctr", 0)
        if ctr >= 2.0:
            d3 = 80
        elif ctr >= 1.0:
            d3 = 55
        else:
            d3 = 25
        detalhes["d3"] = {"score": d3, "ctr_fallback": ctr, "metodo": "ctr_fallback", "descricao": "Eficiencia de funil (fallback CTR)"}

    # Dimensao 4 — Performance financeira
    roas = kpis.get("roas", 0)
    _, roas_min, _ = classificar_funil(None)
    if ticket_tipo == "high_ticket":
        roas_min = 4.0
    elif ticket_tipo == "mid_ticket":
        roas_min = 3.0
    elif ticket_tipo == "low_ticket":
        roas_min = 2.5
    else:
        roas_min = 3.0

    if roas > 0:
        if roas >= 4.0:
            d4 = 100
        elif roas >= 3.0:
            d4 = 85
        elif roas >= 2.0:
            d4 = 65
        elif roas >= 1.5:
            d4 = 40
        elif roas >= 1.0:
            d4 = 20
        else:
            d4 = 0
    else:
        # Sem ROAS, verificar leads
        leads_total = agg.get("leads", 0)
        if leads_total == 0:
            d4 = 0
        else:
            d4 = 35  # tem conversoes mas sem pixel de compra configurado

    detalhes["d4"] = {
        "score": d4,
        "roas": roas,
        "roas_benchmark": roas_min,
        "tipo_funil": ticket_tipo,
        "descricao": "Performance financeira",
    }

    # Dimensao 5 — Consistencia temporal (WoW CPA)
    d5 = 50  # neutro por padrao (sem dados comparativos)
    if camps_1b:
        # Calcular CPA periodo atual vs anterior com os dados 1b
        # camps_1b tem time_increment, entao tem date_start/date_stop
        # Separar em periodo mais recente e anterior
        todos_com_data = sorted(camps_1b, key=lambda x: x.get("date_start", ""))
        if todos_com_data:
            # Metade mais recente vs metade mais antiga
            meio = len(todos_com_data) // 2
            recentes = todos_com_data[meio:]
            anteriores = todos_com_data[:meio]

            def cpa_periodo(lista):
                spend_t = sum(float(c.get("spend", 0) or 0) for c in lista)
                conv_t = sum(
                    get_action(c.get("actions", []), "offsite_conversion.fb_pixel_purchase") +
                    get_action(c.get("actions", []), "offsite_conversion.fb_pixel_lead") +
                    get_action(c.get("actions", []), "lead")
                    for c in lista
                )
                return spend_t / conv_t if conv_t > 0 else None

            cpa_rec = cpa_periodo(recentes)
            cpa_ant = cpa_periodo(anteriores)

            if cpa_rec is not None and cpa_ant is not None and cpa_ant > 0:
                variacao_wow = ((cpa_rec - cpa_ant) / cpa_ant) * 100
                if variacao_wow <= 20:
                    d5 = 100
                elif variacao_wow <= 30:
                    d5 = 70
                elif variacao_wow <= 50:
                    d5 = 40
                else:
                    d5 = 10
                detalhes["d5"] = {
                    "score": d5,
                    "cpa_recente": round(cpa_rec, 2),
                    "cpa_anterior": round(cpa_ant, 2),
                    "variacao_wow_pct": round(variacao_wow, 1),
                    "descricao": "Consistencia temporal",
                }
            else:
                detalhes["d5"] = {"score": d5, "descricao": "Consistencia temporal (sem dados suficientes)"}
        else:
            detalhes["d5"] = {"score": d5, "descricao": "Consistencia temporal (sem dados 1b)"}
    else:
        detalhes["d5"] = {"score": d5, "descricao": "Consistencia temporal (sem comparativo WoW)"}

    # Score final ponderado
    score = (d1 * 0.20) + (detalhes["d2"]["score"] * 0.20) + (d3 * 0.25) + (d4 * 0.25) + (d5 * 0.10)
    score = round(score, 1)

    if score >= 85:
        classificacao = "excelente"
        emoji = "verde"
    elif score >= 70:
        classificacao = "boa"
        emoji = "amarelo"
    elif score >= 50:
        classificacao = "regular"
        emoji = "laranja"
    else:
        classificacao = "critica"
        emoji = "vermelho"

    return {
        "score": score,
        "classificacao": classificacao,
        "emoji": emoji,
        "dimensoes": detalhes,
    }


# ── Proxima acao recomendada ───────────────────────────────────────────────────

def recomendar_proximo(health, sinais):
    """Indica o proximo output a rodar conforme o sintoma dominante."""
    score = health["score"]
    n_sinais = len(sinais.get("queima", [])) + len(sinais.get("fadiga", [])) + len(sinais.get("budget", []))

    queima_total = sum(s["spend"] for s in sinais.get("queima", []))

    d3_score = health["dimensoes"].get("d3", {}).get("score", 50)
    connect_rate = health["dimensoes"].get("d3", {}).get("connect_rate")

    if score < 50 or n_sinais >= 2:
        return {"output": 8, "label": "Problemas Ocultos", "motivo": "Score critico ou multiplos sinais simultaneos"}
    if sinais.get("fadiga") or sinais.get("saturacao"):
        return {"output": 3, "label": "Criativos & Copy", "motivo": "Fadiga ou saturacao de publico detectada"}
    if queima_total > 300:
        return {"output": 2, "label": "Performance & Funil", "motivo": f"Queima de R$ {round(queima_total, 0)} sem conversao"}
    if sinais.get("budget"):
        return {"output": 9, "label": "Orcamento & Projecao", "motivo": "Budget estourando antes do horario nobre"}
    if connect_rate is not None and connect_rate < 40:
        return {"output": 2, "label": "Performance & Funil", "motivo": f"Connect Rate baixo ({connect_rate}%) — gargalo na pagina"}
    if score >= 85:
        return {"output": 9, "label": "Orcamento & Projecao", "motivo": "Conta saudavel — hora de escalar"}
    return {"output": 2, "label": "Performance & Funil", "motivo": "Verificar distribuicao de gasto e ROAS por campanha"}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-file", help="Caminho direto para o arquivo de cache JSON")
    parser.add_argument("--account", help="ID da conta (para montar o caminho do cache)")
    parser.add_argument("--filtro", default="", help="Filtro de campanhas (mesmo do fetch)")
    parser.add_argument("--periodo", default="last_30d")
    parser.add_argument("--output", default="diagnostico")
    parser.add_argument("--cache-dir", default="skill-analise/cache")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--ticket", type=float, default=None, help="Preco do ticket para benchmarks")
    args = parser.parse_args()

    # Descobrir o arquivo de cache
    if args.cache_file:
        cache_file = Path(args.cache_file)
    elif args.account:
        project_root = Path(args.project_root).resolve()
        filtro_slug = args.filtro.replace(" ", "_").replace("-", "").lower() or "all"
        cache_file = project_root / args.cache_dir / f"{args.account}_{args.periodo}_{filtro_slug}_{args.output}.json"
    else:
        err("Informe --cache-file ou --account para localizar o cache.")
        write_out({"error": "args_missing"})
        return

    if not cache_file.exists():
        err(f"Cache nao encontrado: {cache_file}")
        err("Rode trafego_fetch.py primeiro para gerar o cache.")
        write_out({"error": "cache_not_found", "path": str(cache_file)})
        return

    with open(cache_file, "rb") as f:
        raw = json.loads(f.read())

    camps_1a = raw.get("1a", [])
    camps_1b = raw.get("1b", [])
    camps_1c = raw.get("1c", [])
    camps_1d = raw.get("1d", [])
    meta = raw.get("_meta", {})

    info(f"Cache carregado: {cache_file.name}")
    info(f"1a: {len(camps_1a)} | 1b: {len(camps_1b)} | 1c: {len(camps_1c)} | 1d: {len(camps_1d)}")

    if not camps_1a:
        write_out({
            "error": "sem_dados",
            "mensagem": "Nenhuma campanha encontrada no cache 1a. Verifique o filtro e o periodo.",
            "_meta": meta,
        })
        return

    # Classificar funil
    ticket = args.ticket
    tipo_funil, roas_min, _ = classificar_funil(ticket)

    # Metricas agregadas
    agg = agregar_campanhas(camps_1a)
    kpis = calcular_kpis(agg, ticket)

    # Metricas WoW (periodo anterior para comparacao)
    wow = None
    if camps_1b:
        # camps_1b tem time_increment — separar os dois periodos
        # O mais recente e o periodo principal, o mais antigo e o comparativo
        sorted_1b = sorted(camps_1b, key=lambda x: x.get("date_start", ""))
        if sorted_1b:
            meio = len(sorted_1b) // 2
            camps_periodo_recente = sorted_1b[meio:]
            camps_periodo_anterior = sorted_1b[:meio]
            agg_recente = agregar_campanhas(camps_periodo_recente)
            agg_anterior = agregar_campanhas(camps_periodo_anterior)
            kpis_recente = calcular_kpis(agg_recente, ticket)
            kpis_anterior = calcular_kpis(agg_anterior, ticket)

            def variacao(atual, anterior):
                if anterior and anterior > 0:
                    return round(((atual - anterior) / anterior) * 100, 1)
                return None

            wow = {
                "spend_atual": agg_recente["spend"],
                "spend_anterior": agg_anterior["spend"],
                "spend_variacao_pct": variacao(agg_recente["spend"], agg_anterior["spend"]),
                "conversoes_atual": agg_recente["purchases"] or agg_recente["leads"],
                "conversoes_anterior": agg_anterior["purchases"] or agg_anterior["leads"],
                "conversoes_variacao_pct": variacao(
                    agg_recente["purchases"] or agg_recente["leads"],
                    agg_anterior["purchases"] or agg_anterior["leads"]
                ),
                "roas_atual": kpis_recente["roas"],
                "roas_anterior": kpis_anterior["roas"],
                "roas_variacao_pct": variacao(kpis_recente["roas"], kpis_anterior["roas"]),
                "cpa_atual": kpis_recente["cpa"],
                "cpa_anterior": kpis_anterior["cpa"],
                "cpa_variacao_pct": variacao(kpis_recente["cpa"] or 0, kpis_anterior["cpa"] or 0),
            }

    # Sinais criticos
    sinais = {
        "queima": detectar_queima(camps_1a),
        "fadiga": detectar_fadiga(camps_1a, camps_1b),
        "saturacao": detectar_saturacao(camps_1a),
        "budget": detectar_budget(camps_1c, camps_1d),
    }

    # Health Score
    health = calcular_health_score(camps_1a, camps_1b, agg, kpis, tipo_funil)

    # Proximo passo recomendado
    proximo = recomendar_proximo(health, sinais)

    # Ranking de campanhas por spend (para tabelas)
    ranking_spend = sorted(
        [processar_campanha(c) for c in camps_1a],
        key=lambda x: x["spend"],
        reverse=True
    )[:10]

    result = {
        "_meta": {
            **meta,
            "ticket": ticket,
            "tipo_funil": tipo_funil,
            "roas_benchmark": roas_min,
            "processado_de": str(cache_file),
        },
        "agregado": agg,
        "kpis": kpis,
        "wow": wow,
        "sinais": sinais,
        "health": health,
        "proximo": proximo,
        "ranking_spend": ranking_spend,
    }

    write_out(result)


if __name__ == "__main__":
    main()
