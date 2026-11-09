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
        --cache-file meus-produtos/{ativo}/trafego/analise/cache/1234567890123456_last_30d_curso_x_apw_diagnostico.json \
        --ticket 497 \
        --output diagnostico

Ou informando os mesmos args do fetch, inclusive --status (o script monta o
caminho do cache com a mesma regra do trafego_fetch.py):
    python3 trafego_processar.py \
        --account 1234567890123456 \
        --filtro "CURSO X" \
        --periodo last_30d \
        --status ACTIVE,PAUSED,WITH_ISSUES \
        --output diagnostico \
        --cache-dir meus-produtos/{ativo}/trafego/analise/cache

O --cache-dir é o mesmo do fetch (a skill passa a pasta do produto ativo); sem
ele, vale a pasta reserva skill-analise/cache, a mesma reserva do fetch.

Período customizado: trocar --periodo por --since AAAA-MM-DD --until AAAA-MM-DD
(os mesmos valores passados ao fetch). Conta de captação: passar --cpl-alvo
para a nota de performance financeira (D4) comparar o CPL com a meta.

Saída: JSON estruturado com métricas, sinais e health score. O campo "avisos"
lista o que ficou de fora (chamada que falhou no fetch, dado de outro dia,
D4 sem CPL-alvo).
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone

STATUS_VALIDOS = ("ACTIVE", "PAUSED", "WITH_ISSUES", "ARCHIVED", "DELETED")
STATUS_PADRAO = "ACTIVE,PAUSED,WITH_ISSUES"

# Mesmo fuso de referência do trafego_fetch.py (America/Sao_Paulo, UTC-3 fixo).
FUSO_SP = timezone(timedelta(hours=-3))

# O que cada chamada complementar do fetch alimenta (para avisar o aluno quando falha).
BLOCOS_POR_CHAMADA = {
    "1b": "comparativo com o período anterior",
    "1d": "gasto de hoje (alerta de orçamento)",
    "1e": "série diária (gráfico de tendência)",
}


# ── Nome do cache (cópia fiel da regra do trafego_fetch.py) ────────────────────

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
    """Parte do nome do cache que identifica o período (igual ao trafego_fetch.py)."""
    if since and until:
        return "{}_{}".format(since.replace("-", ""), until.replace("-", ""))
    return periodo


def nome_cache(account, periodo, filtro, status_list, output):
    return "{}_{}_{}_{}_{}.json".format(
        account, periodo, slug_filtro(filtro), slug_status(status_list), output
    )


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


def get_leads(actions):
    """Leads sem dupla contagem.

    O tipo "lead" da Meta é o total de leads (site pelo pixel + formulário
    instantâneo). Ele é a contagem quando vem; sem ele, vale o lead do pixel
    (offsite_conversion.fb_pixel_lead). Nunca somar os dois: o lead do pixel já
    está dentro do "lead". O max() cobre os dois casos, inclusive a campanha que
    mistura site e formulário (o total é maior que o pixel sozinho).
    """
    return max(get_action(actions, "lead"),
               get_action(actions, "offsite_conversion.fb_pixel_lead"))


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
        total_leads += get_leads(actions)

        # Link clicks (outbound): diferente de clicks total
        total_link_clicks += get_action(actions, "link_click")

        # Landing page views: campo dentro de actions (nao campo topo nivel!)
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
    leads = get_leads(actions)
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
        # O campo ctr da Graph API já vem em porcentagem (ex: 0.85 = 0,85%).
        # Não multiplicar por 100 quando for menor que 1: CTR abaixo de 1% é comum.
        "ctr": round(ctr_raw, 3),
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
    """Campanhas com gasto > limite e zero conversoes: queima de dinheiro."""
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
        # ctr da Graph API já vem em porcentagem; sem normalização (ver processar_campanha).
        ctr_val = float(c.get("ctr", 0) or 0)
        if cid not in ctr_anterior or c.get("date_start", "") > ctr_anterior[cid].get("date_start", ""):
            ctr_anterior[cid] = {"ctr": ctr_val, "date_start": c.get("date_start", "")}

    fadigadas = []
    for c in camps_1a:
        proc = processar_campanha(c)
        freq = proc["frequency"]
        ctr_atual = proc["ctr"]

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
            # Sem dado anterior mas freq alta: considerar risco
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
        # 1c reaproveita a lista da Chamada 0 do fetch, que segue o --status escolhido
        # e pode trazer campanhas pausadas. Alerta de orçamento só vale para as ativas.
        if c.get("effective_status") not in (None, "ACTIVE"):
            continue
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

def calcular_health_score(camps_1a, camps_1b, agg, kpis, ticket_tipo, cpl_alvo=None, metrica_wow=None):
    """
    Calcula o Health Score com 5 dimensoes conforme 1-diagnostico-rapido.md.
    D1 (20%) = Diversidade criativa (proxy: campanhas ativas com spend > 10)
    D2 (20%) = Saude de publicos (% campanhas com freq <= 3)
    D3 (25%) = Eficiencia de funil (connect rate)
    D4 (25%) = Performance financeira (ROAS vs benchmark; captação: CPL vs cpl_alvo)
    D5 (10%) = Consistencia temporal (variacao de CPA WoW, na metrica_wow:
               "compras" ou "leads", a mesma métrica nas duas janelas; janela
               atual sem conversão e anterior com conversão = pior faixa, com
               rótulo "parou de converter")
    """
    detalhes = {}

    # Dimensao 1. Diversidade criativa
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

    # Dimensao 2. Saude de publicos
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

    # Dimensao 3. Eficiencia de funil (connect rate)
    # Régua única do projeto: 80% ou mais saudável, 60% a 79% atenção, abaixo
    # de 60% crítico (abaixo de 70%, a primeira hipótese é técnica). Os 5 degraus
    # estão documentados na Dimensão 3 do 1-diagnostico-rapido.md.
    connect_rate = kpis.get("connect_rate")
    if connect_rate is not None:
        if connect_rate >= 80:
            d3 = 100
        elif connect_rate >= 70:
            d3 = 75
        elif connect_rate >= 65:
            d3 = 50
        elif connect_rate >= 60:
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

    # Dimensao 4. Performance financeira
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
        detalhes["d4"] = {
            "score": d4,
            "roas": roas,
            "roas_benchmark": roas_min,
            "tipo_funil": ticket_tipo,
            "descricao": "Performance financeira",
        }
    elif agg.get("purchases", 0) > 0 or metrica_wow == "compras":
        # Conta de venda sem ROAS no período (compra sem valor no pixel, ou vendas
        # que zeraram em relação à janela anterior): mantém a regra de antes.
        leads_total = agg.get("leads", 0)
        d4 = 0 if leads_total == 0 else 35
        detalhes["d4"] = {
            "score": d4,
            "roas": roas,
            "roas_benchmark": roas_min,
            "tipo_funil": ticket_tipo,
            "descricao": "Performance financeira",
        }
    else:
        # Sem compra em nenhuma janela: conta de captação. Nota pelo CPL contra o CPL-alvo, tabela do
        # 1-diagnostico-rapido.md (D4, captação). Sem CPL-alvo, nota neutra (50)
        # marcada como sem referência: nunca uma nota fixa que não diferencia
        # captação boa de captação ruim.
        leads_total = agg.get("leads", 0)
        cpl = round(agg.get("spend", 0) / leads_total, 2) if leads_total > 0 else None
        sem_referencia = False
        if leads_total == 0:
            d4 = 0
        elif cpl_alvo and cpl_alvo > 0:
            razao = cpl / cpl_alvo
            if razao <= 0.60:
                d4 = 100
            elif razao <= 0.80:
                d4 = 80
            elif razao <= 1.00:
                d4 = 60
            elif razao <= 1.30:
                d4 = 35
            else:
                d4 = 10
        else:
            d4 = 50
            sem_referencia = True
        detalhes["d4"] = {
            "score": d4,
            "cpl": cpl,
            "cpl_alvo": cpl_alvo,
            "sem_referencia": sem_referencia,
            "descricao": "Performance financeira (captação: CPL vs CPL-alvo)"
                         + (" sem CPL-alvo, nota neutra" if sem_referencia else ""),
        }

    # Dimensao 5. Consistencia temporal (WoW CPA)
    # Compara o CPA do periodo principal (1a) com o da janela anterior (1b).
    # 1b ja e a janela anterior fechada: agregar inteiro, sem fatiar ao meio.
    d5 = 50  # neutro por padrao (sem dados comparativos)
    if camps_1b:
        def cpa_periodo(lista):
            spend_t = sum(float(c.get("spend", 0) or 0) for c in lista)
            # A métrica é escolhida UMA vez para as duas janelas (metrica_wow, no
            # main): compras se qualquer janela teve compra; senão, leads. Escolher
            # por janela comparava CPA de uma semana com CPL da outra.
            if metrica_wow == "leads":
                conv_t = sum(get_leads(c.get("actions", [])) for c in lista)
            else:
                conv_t = sum(
                    get_action(c.get("actions", []), "offsite_conversion.fb_pixel_purchase")
                    for c in lista
                )
            return spend_t / conv_t if conv_t > 0 else None

        cpa_rec = cpa_periodo(camps_1a)   # periodo principal (atual)
        cpa_ant = cpa_periodo(camps_1b)   # janela anterior

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
                "metrica": metrica_wow,
                "descricao": "Consistencia temporal",
            }
        elif cpa_rec is None and cpa_ant is not None:
            # Janela atual sem nenhuma conversão e a anterior com conversões: a
            # conta parou de converter. Pior faixa do D5, nunca a nota neutra.
            d5 = 10
            detalhes["d5"] = {
                "score": d5,
                "cpa_recente": None,
                "cpa_anterior": round(cpa_ant, 2),
                "variacao_wow_pct": None,
                "metrica": metrica_wow,
                "rotulo": "parou de converter",
                "descricao": "Consistencia temporal (parou de converter)",
            }
        else:
            detalhes["d5"] = {"score": d5, "descricao": "Consistencia temporal (sem dados suficientes)"}
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


# ── Serie diaria (tendencia) ────────────────────────────────────────────────────

def serie_diaria(camps_1e):
    """Agrupa as linhas diarias (1e) por data, somando metricas-chave.

    1e vem do fetch como level=campaign + time_increment=1: uma linha por
    campanha por dia, já filtrada pelos mesmos IDs do 1a (nome + status). Agrupamos por date_start para a
    serie de tendencia. Soma diaria fecha com o agregado filtrado do dashboard
    (mesma janela, mesmo filtro).
    """
    por_dia = {}
    for c in camps_1e:
        dia = c.get("date_start", "")
        if not dia:
            continue
        d = por_dia.setdefault(dia, {"spend": 0.0, "impressions": 0, "vendas": 0.0, "receita": 0.0, "leads": 0.0})
        d["spend"] += float(c.get("spend", 0) or 0)
        d["impressions"] += int(c.get("impressions", 0) or 0)
        actions = c.get("actions", [])
        action_values = c.get("action_values", [])
        d["vendas"] += get_action(actions, "offsite_conversion.fb_pixel_purchase")
        d["receita"] += get_action_value(action_values, "offsite_conversion.fb_pixel_purchase")
        d["leads"] += get_leads(actions)

    serie = []
    for dia in sorted(por_dia.keys()):
        d = por_dia[dia]
        serie.append({
            "data": dia,
            "spend": round(d["spend"], 2),
            "impressions": d["impressions"],
            "vendas": round(d["vendas"], 1),
            "receita": round(d["receita"], 2),
            "leads": round(d["leads"], 1),
        })
    return serie


def serie_diaria_svg(serie, vb_w=720, vb_h=240, pad_l=54, pad_r=44, pad_t=16, pad_b=30):
    """Pre-calcula a geometria SVG da linha de tendencia para o template HTML.

    Emite os 'points' das polylines de gasto e vendas + a area de gasto + os
    labels de data do eixo X, prontos para injetar no SVG. Mantem o grafico
    100% deterministico: o gerador do HTML so cola as strings, sem plotar
    ~30 pontos a mao (fonte de erro). Eixo duplo: gasto na escala esquerda,
    vendas na escala direita.
    """
    if not serie:
        return None
    n = len(serie)
    plot_w = vb_w - pad_l - pad_r
    plot_h = vb_h - pad_t - pad_b
    base_y = pad_t + plot_h
    max_spend = max((d["spend"] for d in serie), default=0.0) or 1.0
    max_vendas = max((d["vendas"] for d in serie), default=0.0) or 1.0

    def px(i):
        return pad_l + (plot_w * i / (n - 1)) if n > 1 else pad_l + plot_w / 2.0

    def py_spend(v):
        return pad_t + plot_h * (1 - v / max_spend)

    def py_vendas(v):
        return pad_t + plot_h * (1 - v / max_vendas)

    spend_pts = " ".join("{},{}".format(round(px(i), 1), round(py_spend(d["spend"]), 1)) for i, d in enumerate(serie))
    vendas_pts = " ".join("{},{}".format(round(px(i), 1), round(py_vendas(d["vendas"]), 1)) for i, d in enumerate(serie))
    area_pts = "{},{} {} {},{}".format(round(pad_l, 1), round(base_y, 1), spend_pts, round(pad_l + plot_w, 1), round(base_y, 1))

    vendas_dots = [{"cx": round(px(i), 1), "cy": round(py_vendas(d["vendas"]), 1), "v": d["vendas"]} for i, d in enumerate(serie)]

    n_labels = min(6, n)
    x_labels = []
    for k in range(n_labels):
        i = round(k * (n - 1) / (n_labels - 1)) if n_labels > 1 else 0
        dia = serie[i]["data"]  # YYYY-MM-DD
        x_labels.append({"x": round(px(i), 1), "label": dia[8:10] + "/" + dia[5:7]})

    return {
        "viewbox": "0 0 {} {}".format(vb_w, vb_h),
        "area_points": area_pts,
        "spend_points": spend_pts,
        "vendas_points": vendas_pts,
        "vendas_dots": vendas_dots,
        "x_labels": x_labels,
        "baseline_y": round(base_y, 1),
        "plot_left": round(pad_l, 1),
        "plot_right": round(pad_l + plot_w, 1),
        "max_spend": round(max_spend, 2),
        "max_vendas": round(max_vendas, 1),
        "dias": n,
    }


# ── Proxima acao recomendada ───────────────────────────────────────────────────

def recomendar_proximo(health, sinais):
    """Indica o próximo output a rodar conforme o sintoma dominante."""
    score = health["score"]
    n_sinais = len(sinais.get("queima", [])) + len(sinais.get("fadiga", [])) + len(sinais.get("budget", []))

    queima_total = sum(s["spend"] for s in sinais.get("queima", []))

    d3_score = health["dimensoes"].get("d3", {}).get("score", 50)
    connect_rate = health["dimensoes"].get("d3", {}).get("connect_rate")

    if score < 50 or n_sinais >= 2:
        return {"output": 8, "label": "Problemas Ocultos", "motivo": "Score crítico ou múltiplos sinais simultâneos"}
    if sinais.get("fadiga") or sinais.get("saturacao"):
        return {"output": 3, "label": "Criativos & Copy", "motivo": "Fadiga ou saturação de público detectada"}
    if queima_total > 300:
        return {"output": 2, "label": "Performance & Funil", "motivo": f"Queima de R$ {round(queima_total, 0)} sem conversão"}
    if sinais.get("budget"):
        return {"output": 9, "label": "Orçamento & Projeção", "motivo": "Budget estourando antes do horário nobre"}
    if connect_rate is not None and connect_rate < 60:  # crítico pela régua única (D3)
        return {"output": 2, "label": "Performance & Funil", "motivo": f"Connect Rate baixo ({connect_rate}%): gargalo na página"}
    if score >= 85:
        return {"output": 9, "label": "Orçamento & Projeção", "motivo": "Conta saudável: hora de escalar"}
    return {"output": 2, "label": "Performance & Funil", "motivo": "Verificar distribuição de gasto e ROAS por campanha"}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-file", help="Caminho direto para o arquivo de cache JSON")
    parser.add_argument("--account", help="ID da conta (para montar o caminho do cache)")
    parser.add_argument("--filtro", default="", help="Filtro de campanhas (mesmo do fetch)")
    parser.add_argument("--periodo", default="last_30d")
    parser.add_argument("--since", help="Mesmo --since do trafego_fetch.py (período customizado)")
    parser.add_argument("--until", help="Mesmo --until do trafego_fetch.py (período customizado)")
    parser.add_argument("--status", default=STATUS_PADRAO,
                        help="Mesmo --status usado no trafego_fetch.py (entra no nome do cache)")
    parser.add_argument("--output", default="diagnostico")
    parser.add_argument("--cache-dir", default="skill-analise/cache",
                        help="Mesmo --cache-dir do trafego_fetch.py (a skill passa "
                             "meus-produtos/{ativo}/trafego/analise/cache; o padrão é a reserva)")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--ticket", type=float, default=None, help="Preço do ticket para benchmarks")
    parser.add_argument("--cpl-alvo", type=float, default=None,
                        help="CPL-alvo do produto (captação). Sem ele, a nota D4 de captação fica neutra")
    args = parser.parse_args()

    # Descobrir o arquivo de cache
    if args.cache_file:
        cache_file = Path(args.cache_file)
    elif args.account:
        status_list = parse_status(args.status)
        if not status_list:
            err(f"--status inválido: {args.status}. Use ACTIVE, PAUSED, WITH_ISSUES, ARCHIVED ou DELETED.")
            write_out({"error": "status_invalido"})
            return
        account = args.account.strip()
        if account.lower().startswith("act_"):
            account = account[4:]
        if bool(args.since) != bool(args.until):
            err("Período customizado: informe --since e --until juntos (AAAA-MM-DD).")
            write_out({"error": "periodo_invalido"})
            return
        project_root = Path(args.project_root).resolve()
        cache_file = project_root / args.cache_dir / nome_cache(
            account, rotulo_periodo(args.periodo, args.since, args.until),
            args.filtro, status_list, args.output
        )
    else:
        err("Informe --cache-file ou --account para localizar o cache.")
        write_out({"error": "args_missing"})
        return

    if not cache_file.exists():
        err(f"Cache não encontrado: {cache_file}")
        err("Rode trafego_fetch.py primeiro para gerar o cache.")
        write_out({"error": "cache_not_found", "path": str(cache_file)})
        return

    with open(cache_file, "rb") as f:
        raw = json.loads(f.read())

    camps_1a = raw.get("1a", [])
    camps_1b = raw.get("1b", [])
    camps_1c = raw.get("1c", [])
    camps_1d = raw.get("1d", [])
    camps_1e = raw.get("1e", [])
    meta = raw.get("_meta", {})

    info(f"Cache carregado: {cache_file.name}")
    info(f"1a: {len(camps_1a)} | 1b: {len(camps_1b)} | 1c: {len(camps_1c)} | 1d: {len(camps_1d)} | 1e: {len(camps_1e)}")

    if not camps_1a:
        write_out({
            "error": "sem_dados",
            "mensagem": "Nenhuma campanha encontrada no cache 1a. Verifique o filtro, o status e o período.",
            "_meta": meta,
        })
        return

    # Classificar funil
    ticket = args.ticket
    tipo_funil, roas_min, _ = classificar_funil(ticket)

    # Metricas agregadas
    agg = agregar_campanhas(camps_1a)
    kpis = calcular_kpis(agg, ticket)

    # Metricas WoW (periodo principal 1a vs janela anterior 1b)
    # 1a = janela principal (ex: last_7d). 1b = janela imediatamente anterior,
    # do mesmo tamanho, ja entregue pelo fetch como time_range fechado (uma linha
    # por campanha). Comparar os dois agregados direto. NUNCA fatiar 1b ao meio:
    # todas as linhas de 1b tem a mesma date_start, entao o split gera dois
    # pedacos da MESMA semana anterior (comparativo sem sentido).
    wow = None
    metrica_wow = None
    if camps_1b:
        agg_anterior = agregar_campanhas(camps_1b)
        kpis_anterior = calcular_kpis(agg_anterior, ticket)

        def variacao(atual, anterior):
            if atual is None:
                return None
            if anterior and anterior > 0:
                return round(((atual - anterior) / anterior) * 100, 1)
            return None

        # Uma métrica só para as duas janelas: compras se qualquer uma teve compra;
        # senão, leads. Nunca comparar CPA de uma semana com CPL da outra.
        if agg["purchases"] > 0 or agg_anterior["purchases"] > 0:
            metrica_wow = "compras"
            conv_atual, conv_anterior = agg["purchases"], agg_anterior["purchases"]
            cpa_atual, cpa_anterior = kpis["cpa_purchase"], kpis_anterior["cpa_purchase"]
        else:
            metrica_wow = "leads"
            conv_atual, conv_anterior = agg["leads"], agg_anterior["leads"]
            cpa_atual, cpa_anterior = kpis["cpa_lead"], kpis_anterior["cpa_lead"]

        wow = {
            "metrica": metrica_wow,
            "spend_atual": agg["spend"],
            "spend_anterior": agg_anterior["spend"],
            "spend_variacao_pct": variacao(agg["spend"], agg_anterior["spend"]),
            "conversoes_atual": conv_atual,
            "conversoes_anterior": conv_anterior,
            "conversoes_variacao_pct": variacao(conv_atual, conv_anterior),
            "roas_atual": kpis["roas"],
            "roas_anterior": kpis_anterior["roas"],
            "roas_variacao_pct": variacao(kpis["roas"], kpis_anterior["roas"]),
            # CPA (compras) ou CPL (leads), conforme "metrica". Sem conversão na
            # janela atual, cpa_atual é None e a variação também (nunca -100%).
            "cpa_atual": cpa_atual,
            "cpa_anterior": cpa_anterior,
            "cpa_variacao_pct": variacao(cpa_atual, cpa_anterior),
        }

    # Sinais criticos
    sinais = {
        "queima": detectar_queima(camps_1a),
        "fadiga": detectar_fadiga(camps_1a, camps_1b),
        "saturacao": detectar_saturacao(camps_1a),
        "budget": detectar_budget(camps_1c, camps_1d),
    }

    # Health Score
    health = calcular_health_score(camps_1a, camps_1b, agg, kpis, tipo_funil,
                                   cpl_alvo=args.cpl_alvo, metrica_wow=metrica_wow)

    # Avisos para o aluno: o que ficou de fora ou pode estar desatualizado.
    avisos = []
    for chamada in meta.get("falhas") or []:
        avisos.append("A Meta não respondeu à chamada {} ({}): esse bloco ficou de fora. "
                      "Rodar a busca de novo traz o dado.".format(
                          chamada, BLOCOS_POR_CHAMADA.get(chamada, "dado complementar")))
    gerado = str(meta.get("gerado_em", ""))[:10]
    if gerado and gerado != datetime.now(FUSO_SP).date().isoformat():
        avisos.append("Estes números foram buscados em {}/{}/{}, não hoje. Rodar a busca de "
                      "novo traz os números atuais.".format(gerado[8:10], gerado[5:7], gerado[0:4]))
    if health["dimensoes"].get("d4", {}).get("sem_referencia"):
        avisos.append("Conta de captação sem CPL-alvo: a nota de performance financeira (D4) "
                      "ficou neutra (50). Informe o CPL-alvo para pontuar de verdade.")

    # Proximo passo recomendado
    proximo = recomendar_proximo(health, sinais)

    # Ranking de campanhas por spend (para tabelas)
    ranking_spend = sorted(
        [processar_campanha(c) for c in camps_1a],
        key=lambda x: x["spend"],
        reverse=True
    )[:10]

    # Serie diaria (tendencia) + geometria SVG pre-calculada
    serie = serie_diaria(camps_1e)
    serie_svg = serie_diaria_svg(serie)

    result = {
        "_meta": {
            **meta,
            "ticket": ticket,
            "tipo_funil": tipo_funil,
            "roas_benchmark": roas_min,
            "processado_de": str(cache_file),
        },
        "avisos": avisos,
        "agregado": agg,
        "kpis": kpis,
        "wow": wow,
        "sinais": sinais,
        "health": health,
        "proximo": proximo,
        "ranking_spend": ranking_spend,
        "serie_diaria": serie,
        "serie_diaria_svg": serie_svg,
    }

    write_out(result)


if __name__ == "__main__":
    main()
