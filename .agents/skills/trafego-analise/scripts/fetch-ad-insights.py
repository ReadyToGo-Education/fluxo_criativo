"""
fetch-ad-insights.py
Script reutilizável para buscar insights de anúncios na Graph API do Meta.
Compatível com Windows, macOS e Linux.

Uso:
    python fetch-ad-insights.py [filtro_campanha] [periodo] [saida.json]

Exemplos:
    python fetch-ad-insights.py "VTSD - CV" last_30d vtsd_cv_30d.json
    python fetch-ad-insights.py "" last_7d conta_completa_7d.json

Saídas:
    - Arquivo JSON salvo diretamente em disco (nunca no stdout)
    - Stdout: apenas resumo compacto, seguro para Claude Code

Erros corrigidos vs. tentativas anteriores:
    1. effective_status REMOVIDO do /insights (causa 403 — só válido em /ads, /campaigns)
    2. limit=100 fixo (limit>=200 com campos pesados causa 403 por complexidade da query)
    3. Campos divididos em 2 chamadas + merge por ad_id (evita query overly complex)
    4. JSON salvo em arquivo DENTRO do script, nunca impresso no stdout (evita truncamento)
    5. UTF-8 forçado no stdout ANTES de qualquer print (corrige cp1252 no Windows)
    6. Busca do .env funciona em Windows, macOS e Linux via os.path
"""

import io
import sys
import json
import time
import urllib.request
import urllib.parse
import os

# ── UTF-8 obrigatório (Windows usa cp1252 por padrão; Mac/Linux já são UTF-8) ─
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Configuração via argumentos ou .env ───────────────────────────────────────
FILTRO_CAMPANHA = sys.argv[1] if len(sys.argv) > 1 else ""
DATE_PRESET     = sys.argv[2] if len(sys.argv) > 2 else "last_30d"
OUTPUT_FILE     = sys.argv[3] if len(sys.argv) > 3 else "ad_insights.json"

def ler_env():
    """
    Busca o .env subindo de diretório até encontrar.
    Funciona em Windows (C:\\), macOS (/Users/...) e Linux (/home/...).
    Tenta a partir do diretório do script E do cwd, cobrindo qualquer
    ponto de execução (CLI, IDE, terminal no meio do projeto).
    """
    env = {}
    candidatos = []

    # Sobe até 6 níveis a partir do diretório do script
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        candidatos.append(os.path.join(d, '.env'))
        pai = os.path.dirname(d)
        if pai == d:  # chegou na raiz do sistema de arquivos
            break
        d = pai

    # Sobe até 6 níveis a partir do cwd (quem chama de outro diretório)
    d = os.getcwd()
    for _ in range(6):
        candidatos.append(os.path.join(d, '.env'))
        pai = os.path.dirname(d)
        if pai == d:
            break
        d = pai

    for caminho in candidatos:
        if os.path.exists(caminho):
            with open(caminho, encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if '=' in linha and not linha.startswith('#'):
                        chave, _, valor = linha.partition('=')
                        env[chave.strip()] = valor.strip().strip('"').strip("'")
            break

    return env

env = ler_env()
TOKEN   = env.get('FB_ACCESS_TOKEN_PERMANENTE', '')
ACCOUNT = env.get('FB_AD_ACCOUNT_ID', '').replace('act_', '')

if not TOKEN or not ACCOUNT:
    print("ERRO: FB_ACCESS_TOKEN_PERMANENTE ou FB_AD_ACCOUNT_ID ausente no .env")
    sys.exit(1)

# ── Helpers ───────────────────────────────────────────────────────────────────
def api_get(url, label="chamada"):
    """GET paginado com retry e tratamento de erro detalhado."""
    resultados = []
    pagina = 0
    while url:
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                d = json.loads(r.read().decode('utf-8'))
            lote = d.get('data', [])
            resultados.extend(lote)
            pagina += 1
            proximo = d.get('paging', {}).get('next')
            url = proximo if proximo else None
            if proximo:
                time.sleep(0.3)  # evitar rate limit
        except urllib.error.HTTPError as e:
            corpo = e.read().decode('utf-8', errors='replace')
            try:
                erro_json = json.loads(corpo)
                msg = erro_json.get('error', {}).get('message', corpo[:300])
            except Exception:
                msg = corpo[:300]
            print(f"  HTTP {e.code} em {label} (pagina {pagina}): {msg}")
            break
        except Exception as e:
            print(f"  Erro em {label} (pagina {pagina}): {e}")
            break
    return resultados

def get_action(actions, tipo):
    if not actions:
        return 0.0
    for a in actions:
        if a.get('action_type') == tipo:
            return float(a['value'])
    return 0.0

def get_video(vlist):
    if not vlist or not isinstance(vlist, list):
        return 0.0
    return float(vlist[0].get('value', 0))

# ── Chamada A: Métricas de performance (sem rankings) ─────────────────────────
# Regra: limit=100 com este volume de campos funciona; limit>=200 causa 403
CAMPOS_A = ','.join([
    'ad_id', 'ad_name', 'campaign_name', 'adset_name',
    'spend', 'impressions', 'reach', 'frequency',
    'clicks', 'ctr', 'cpm',
    'inline_link_clicks', 'inline_link_click_ctr',
    'actions', 'action_values', 'cost_per_action_type',
    'video_p25_watched_actions', 'video_p50_watched_actions',
    'video_p100_watched_actions', 'video_play_actions',
])

params_a = urllib.parse.urlencode({
    'fields':      CAMPOS_A,
    'level':       'ad',
    'date_preset': DATE_PRESET,
    'limit':       100,         # NUNCA usar >100 com este volume de campos
    'access_token': TOKEN,
})
url_a = f'https://graph.facebook.com/v21.0/act_{ACCOUNT}/insights?{params_a}'

print(f"Buscando metricas de performance (chamada A)...")
registros_a = api_get(url_a, "chamada A - performance")
print(f"  Retornados: {len(registros_a)} ads (conta completa)")

# ── Chamada B: Rankings de leilão (separada para evitar 403) ─────────────────
# Ranking só disponível em level=ad. Separar da chamada A reduz complexidade.
CAMPOS_B = ','.join([
    'ad_id',
    'quality_ranking',
    'engagement_rate_ranking',
    'conversion_rate_ranking',
])

params_b = urllib.parse.urlencode({
    'fields':      CAMPOS_B,
    'level':       'ad',
    'date_preset': DATE_PRESET,
    'limit':       100,
    'access_token': TOKEN,
})
url_b = f'https://graph.facebook.com/v21.0/act_{ACCOUNT}/insights?{params_b}'

print(f"Buscando rankings de leilao (chamada B)...")
registros_b = api_get(url_b, "chamada B - rankings")
print(f"  Retornados: {len(registros_b)} ads")

# ── Merge A + B por ad_id ─────────────────────────────────────────────────────
rankings_por_id = {r['ad_id']: r for r in registros_b}
for reg in registros_a:
    rank = rankings_por_id.get(reg['ad_id'], {})
    reg['quality_ranking']          = rank.get('quality_ranking', 'UNKNOWN')
    reg['engagement_rate_ranking']  = rank.get('engagement_rate_ranking', 'UNKNOWN')
    reg['conversion_rate_ranking']  = rank.get('conversion_rate_ranking', 'UNKNOWN')

# ── Filtrar por nome de campanha ──────────────────────────────────────────────
if FILTRO_CAMPANHA:
    registros_filtrados = [
        r for r in registros_a
        if FILTRO_CAMPANHA in r.get('campaign_name', '')
    ]
    print(f"  Filtro '{FILTRO_CAMPANHA}': {len(registros_filtrados)} de {len(registros_a)} ads")
else:
    registros_filtrados = registros_a

# ── Calcular métricas derivadas ───────────────────────────────────────────────
BENCHMARK_CPA = 1370  # ajustar conforme produto ativo

def is_below_avg(valor):
    return isinstance(valor, str) and 'BELOW' in valor

processados = []
for ad in registros_filtrados:
    spend  = float(ad.get('spend', 0))
    imp    = max(float(ad.get('impressions', 1)), 1)
    freq   = float(ad.get('frequency', 0))
    ctr    = float(ad.get('ctr', 0))
    ilc    = float(ad.get('inline_link_click_ctr', 0))
    cpm    = float(ad.get('cpm', 0))

    actions = ad.get('actions', [])
    av      = ad.get('action_values', [])

    purchases = (
        get_action(actions, 'offsite_conversion.fb_pixel_purchase') or
        get_action(actions, 'purchase')
    )
    revenue = (
        get_action(av, 'offsite_conversion.fb_pixel_purchase') or
        get_action(av, 'purchase')
    )
    initiate_checkout = get_action(actions, 'initiate_checkout')
    landing_pv        = get_action(actions, 'landing_page_view')

    cpa  = spend / purchases if purchases > 0 else None
    roas = revenue / spend   if spend > 0 and revenue > 0 else None

    vp25   = get_video(ad.get('video_p25_watched_actions'))
    vp50   = get_video(ad.get('video_p50_watched_actions'))
    vp100  = get_video(ad.get('video_p100_watched_actions'))
    vplay  = get_video(ad.get('video_play_actions'))

    hook_rate   = vp25  / imp  if vp25  > 0 else None
    hold_rate   = vp50  / vp25 if vp25  > 0 else None
    play_through= vp100 / imp  if vp100 > 0 else None
    thumbstop   = vplay / imp  if vplay > 0 else None
    is_video    = vp25 > 0 or vplay > 0

    qual = ad.get('quality_ranking', 'UNKNOWN')
    eng  = ad.get('engagement_rate_ranking', 'UNKNOWN')
    conv = ad.get('conversion_rate_ranking', 'UNKNOWN')

    # Score composto (0-100)
    if is_video:
        score_hook  = min((hook_rate or 0) / 0.25 * 30, 30)
        score_hold  = min((hold_rate or 0) / 0.40 * 20, 20)
        score_ctr   = min(ilc / 0.015 * 25, 25)
        score_cpr   = min((BENCHMARK_CPA / cpa) * 25, 25) if cpa else 0
        score = score_hook + score_hold + score_ctr + score_cpr
    else:
        score_thumb = min((thumbstop or 0) / 0.25 * 25, 25)
        score_ctr   = min(ilc / 0.015 * 40, 40)
        score_cpr   = min((BENCHMARK_CPA / cpa) * 35, 35) if cpa else 0
        score = score_thumb + score_ctr + score_cpr

    tier = (
        'S' if score >= 85 else
        'A' if score >= 70 else
        'B' if score >= 55 else
        'C' if score >= 40 else
        'D'
    )

    # Fadiga (sinais 1+4+5, sem WoW aqui)
    s1 = freq >= 3.0
    s4 = is_below_avg(qual) or is_below_avg(eng) or is_below_avg(conv)
    s5_val = (BENCHMARK_CPA / cpa) < 0.5 if cpa else False  # CPA >= 2x benchmark
    score_fadiga = (1 if s1 else 0) + (1 if s4 else 0) + (2 if s5_val else 0)

    veredicto_fadiga = (
        'Saudavel'      if score_fadiga <= 1 else
        'Monitorar'     if score_fadiga <= 3 else
        'Subst_48h'     if score_fadiga == 4 else
        'Pausar'
    )

    processados.append({
        'ad_id':    ad['ad_id'],
        'ad_name':  ad['ad_name'],
        'campaign': ad['campaign_name'],
        'adset':    ad.get('adset_name', ''),
        'tipo':     'VIDEO' if is_video else 'IMAGEM',
        'spend':    round(spend, 2),
        'imp':      int(imp),
        'freq':     round(freq, 2),
        'ctr':      round(ctr, 2),
        'ilc':      round(ilc, 2),
        'cpm':      round(cpm, 2),
        'purchases':round(purchases, 0),
        'revenue':  round(revenue, 2),
        'cpa':      round(cpa, 2) if cpa else None,
        'roas':     round(roas, 2) if roas else None,
        'initiate_checkout': int(initiate_checkout),
        'landing_pv':        int(landing_pv),
        'hook_rate':    round(hook_rate * 100, 2)    if hook_rate    else None,
        'hold_rate':    round(hold_rate * 100, 2)    if hold_rate    else None,
        'play_through': round(play_through * 100, 2) if play_through else None,
        'thumbstop':    round(thumbstop * 100, 2)    if thumbstop    else None,
        'qual': qual,
        'eng':  eng,
        'conv': conv,
        'score':          round(score, 1),
        'tier':           tier,
        'score_fadiga':   score_fadiga,
        'veredicto_fadiga': veredicto_fadiga,
        'has_below_avg':  s4,
    })

# Ordenar por spend
processados.sort(key=lambda x: x['spend'], reverse=True)

# ── Salvar em arquivo JSON (NUNCA imprimir JSON bruto no stdout) ──────────────
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(processados, f, ensure_ascii=False, indent=2)

# ── Resumo compacto no stdout ─────────────────────────────────────────────────
total_spend    = sum(r['spend'] for r in processados)
total_purch    = sum(r['purchases'] for r in processados)
total_rev      = sum(r['revenue'] for r in processados)
total_imp      = sum(r['imp'] for r in processados)
total_ic       = sum(r['initiate_checkout'] for r in processados)
total_lpv      = sum(r['landing_pv'] for r in processados)
video_n        = sum(1 for r in processados if r['tipo'] == 'VIDEO')
img_n          = sum(1 for r in processados if r['tipo'] == 'IMAGEM')
with_conv      = [r for r in processados if r['purchases'] > 0]
below_avg_n    = sum(1 for r in processados if r['has_below_avg'])
tier_s         = [r for r in processados if r['tier'] == 'S']
tier_a         = [r for r in processados if r['tier'] == 'A']
tier_d         = [r for r in processados if r['tier'] == 'D']

print()
print(f"=== RESUMO: {len(processados)} ads | {video_n} video / {img_n} imagem ===")
print(f"Spend: R$ {total_spend:,.0f}  |  Impressoes: {total_imp:,.0f}  |  CPM: R$ {total_imp and total_spend/total_imp*1000:.2f}")
print(f"Compras: {total_purch:.0f}  |  Receita: R$ {total_rev:,.0f}  |  Initiate Checkout: {total_ic:.0f}  |  LPV: {total_lpv:.0f}")
if total_purch:
    print(f"CPA: R$ {total_spend/total_purch:.0f}  |  ROAS: {total_rev/total_spend:.2f}x")
else:
    print("CPA: sem compras no periodo")

print()
print(f"Tier S: {len(tier_s)} ads  |  Tier A: {len(tier_a)} ads  |  Tier D (sem conv): {len(tier_d)} ads")
print(f"Below Average no leilao: {below_avg_n} ads")

print()
print("Top 5 por SPEND:")
for r in processados[:5]:
    cpa_s = f"R$ {r['cpa']:,.0f}" if r['cpa'] else "INF"
    hook_s = f"{r['hook_rate']:.1f}%" if r['hook_rate'] else "--"
    print(f"  [{r['tier']}][{r['tipo'][:3]}] {r['ad_name'][:55]:<57}"
          f" spend=R${r['spend']:>6,.0f}  CPA={cpa_s:<10}  hook={hook_s}")

print()
print("Ads com compras:")
for r in sorted(with_conv, key=lambda x: x['cpa'] or 999999):
    roas_s = f"{r['roas']:.2f}x" if r['roas'] else "--"
    hook_s = f"{r['hook_rate']:.1f}%" if r['hook_rate'] else "--"
    print(f"  [{r['tier']}][{r['tipo'][:3]}] {r['ad_name'][:55]:<57}"
          f" purch={r['purchases']:.0f}  CPA=R${r['cpa']:>7,.0f}  ROAS={roas_s}  hook={hook_s}")

if not with_conv:
    print("  Nenhum ad com compras no periodo.")

print()
print(f"JSON salvo em: {OUTPUT_FILE}")
print(f"Total de registros: {len(processados)}")
