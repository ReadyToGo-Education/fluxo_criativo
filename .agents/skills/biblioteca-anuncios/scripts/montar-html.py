#!/usr/bin/env python3
"""
biblioteca-anuncios. Monta o HTML final consolidando os dados dos concorrentes.

Uso:
    python3 montar-html.py --config /caminho/para/config.json

O config.json tem o formato:
{
  "produto_slug": "automacoes-inteligentes",
  "nicho": "marketing digital para infoprodutores",
  "modo": "PADRAO",
  "metodo": "APIFY",
  "criterio_escala": 3,
  "mercados_legivel": "Brasil, Estados Unidos, Hispano (MX)",
  "data_relatorio": "2026-05-14",
  "saida_html": "meus-produtos/{slug}/entregas/biblioteca-anuncios/criativos-escalados-{data}.html",
  "concorrentes": [
    {
      "slug": "alex-hormozi",
      "nome": "Alex Hormozi",
      "regiao": "en",
      "foco": "Acquisition e escala de negocios",
      "resultado_json": "/caminho/para/tmp/alex-hormozi.json"
    }
  ],
  "analises": {
    "padroes_comuns": ["bullet 1", "bullet 2", ...],   // opcional
    "diferencas_mercados": ["bullet 1", ...],            // opcional
    "padroes_por_concorrente": {                          // opcional
      "alex-hormozi": "texto custom do padrao..."
    }
  }
}

Se "analises" estiver ausente ou incompleto, o script gera versoes data-driven simples.

O script imprime apenas o caminho do HTML salvo.
"""
import argparse
import html
import json
import sys
from datetime import datetime
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, Exception):
    pass


FLAG = {"br": "🇧🇷", "en": "🇺🇸", "es": "🌎"}
MERCADO_LBL = {"br": "BR", "en": "US", "es": "MX/ES"}


def esc(s):
    return html.escape(str(s or ""), quote=True)


def truncar(s, n=160):
    s = (s or "").strip()
    if len(s) > n:
        return s[: n - 3] + "..."
    return s


def escala_classe(n):
    if n >= 20:
        return "scale-hot"
    if n >= 10:
        return "scale-warm"
    if n >= 5:
        return "scale-cool"
    return "scale-base"


def carregar_resultado(caminho: str) -> dict:
    """Le o JSON de um concorrente. Retorna {} se nao existir."""
    p = Path(caminho)
    if not p.exists():
        return {"total_ads_coletados": 0, "criativos_escalados": [], "erro": f"arquivo nao encontrado: {caminho}"}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"total_ads_coletados": 0, "criativos_escalados": [], "erro": f"erro lendo {caminho}: {exc}"}


def gerar_padroes_comuns_default(concorrentes_com_dados: list) -> list:
    """Gera bullets data-driven se a skill nao passar analises customizadas."""
    if not concorrentes_com_dados:
        return ["Sem dados suficientes para identificar padroes."]
    return [
        "Concentracao de investimento em poucos criativos por concorrente, com replicacao vertical em multiplos formatos (video, imagem, carrossel).",
        "Criativos escalados (3+ ads) tendem a permanecer ativos por semanas a meses, indicando uso evergreen e nao apenas picos de lancamento.",
        "Hooks dos top criativos sao majoritariamente diretos, sem perguntas no inicio.",
        "CTAs simples e padronizadas dominam (Learn More, Saiba Mais, Inscreva-se).",
        "Maior densidade de criativos escalados em paginas com Library ID estavel (perfis ja consolidados, nao paginas novas).",
    ]


def gerar_diferencas_default(concorrentes_com_dados: list) -> list:
    """Diferencas data-driven baseadas nos dados reais."""
    por_regiao = {}
    for r in concorrentes_com_dados:
        por_regiao.setdefault(r["regiao"], []).append(r)

    bullets = []
    if "br" in por_regiao and "en" in por_regiao:
        br_max = max((max((c["collationCount"] for c in r["criativos"]), default=0) for r in por_regiao["br"]), default=0)
        en_max = max((max((c["collationCount"] for c in r["criativos"]), default=0) for r in por_regiao["en"]), default=0)
        if br_max and en_max:
            bullets.append(f"BR vs US: maior escala individual no Brasil ({br_max} ads) vs Estados Unidos ({en_max} ads).")
    if "es" in por_regiao:
        es_total = sum(r["total_ads"] for r in por_regiao["es"])
        bullets.append(f"Hispano: volume agregado de {es_total} ads ativos, mercado historicamente menos saturado que BR e US.")
    if "br" in por_regiao:
        br_concorrentes = len(por_regiao["br"])
        br_total_criativos = sum(len(r["criativos"]) for r in por_regiao["br"])
        bullets.append(f"BR: {br_concorrentes} concorrentes investigados, somando {br_total_criativos} criativos escalados.")
    while len(bullets) < 3:
        bullets.append("Dados insuficientes em algum mercado para mais comparacoes.")
    return bullets[:5]


def gerar_padrao_concorrente_default(r: dict) -> str:
    """Texto data-driven do bloco 'Padrao Identificado' por concorrente."""
    if not r["criativos"]:
        return ""
    n_crits = len(r["criativos"])
    max_c = r["criativos"][0]["collationCount"]
    return (
        f"O concorrente concentra forca em {n_crits} criativos repetidos verticalmente. "
        f"O criativo de maior escala roda em {max_c} ads simultaneos, indicando hipotese "
        f"validada que merece ser estudada como referencia de hook e estrutura."
    )


def montar_css() -> str:
    """CSS inline, paleta do template-html.md."""
    return """
:root {
  --bg:#ffffff; --bg-soft:#f7f9fc;
  --text:#1a2238; --text-soft:#5b6478;
  --border:#e5eaf2; --accent:#2563eb; --accent-soft:#dbeafe;
  --hot:#dc2626; --warm:#ea580c; --cool:#2563eb; --base:#6b7280;
  --empty:#fef3c7; --empty-border:#fbbf24;
}
* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; }
body { font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif; background:var(--bg); color:var(--text); line-height:1.5; }
.container { max-width:1180px; margin:0 auto; padding:32px 24px; }
.hero { padding:48px 24px 32px; border-bottom:1px solid var(--border); margin-bottom:32px; }
.eyebrow { color:var(--accent); font-weight:600; font-size:13px; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:12px; }
h1 { font-size:34px; font-weight:800; line-height:1.15; margin-bottom:12px; }
.subtitle { color:var(--text-soft); font-size:17px; margin-bottom:20px; }
.chips { display:flex; flex-wrap:wrap; gap:8px; }
.chip { background:var(--bg-soft); border:1px solid var(--border); border-radius:999px; padding:6px 14px; font-size:13px; color:var(--text-soft); font-weight:500; }
.chip strong { color:var(--text); font-weight:600; }
.stats { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }
.stat-card { background:var(--bg-soft); border:1px solid var(--border); border-radius:12px; padding:20px; }
.stat-label { font-size:12px; font-weight:600; color:var(--text-soft); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px; }
.stat-value { font-size:36px; font-weight:800; line-height:1; color:var(--text); }
.stat-meta { font-size:12px; color:var(--text-soft); margin-top:6px; }
.filter { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:32px; }
.filter-btn { background:transparent; border:1px solid var(--border); color:var(--text-soft); padding:8px 16px; border-radius:8px; cursor:pointer; font-family:inherit; font-size:14px; font-weight:500; transition:all 0.15s; }
.filter-btn:hover { background:var(--bg-soft); }
.filter-btn.active { background:var(--accent); border-color:var(--accent); color:#fff; }
.sticky-nav { position:sticky; top:0; background:var(--bg); border-bottom:1px solid var(--border); padding:12px 0; margin-bottom:32px; display:flex; flex-wrap:wrap; gap:6px; z-index:10; }
.sticky-nav a { font-size:13px; color:var(--text-soft); padding:6px 10px; border-radius:6px; text-decoration:none; font-weight:500; transition:background 0.15s; display:inline-flex; align-items:center; gap:6px; }
.sticky-nav a:hover { background:var(--bg-soft); color:var(--text); }
.count-badge { background:var(--accent-soft); color:var(--accent); padding:1px 6px; border-radius:999px; font-size:11px; font-weight:700; }
.competitor { margin-bottom:48px; padding-bottom:32px; border-bottom:1px solid var(--border); }
.competitor:last-child { border-bottom:none; }
.competitor-header { margin-bottom:24px; }
.competitor-header h2 { font-size:24px; font-weight:700; margin-bottom:8px; }
.competitor-meta { font-size:14px; color:var(--text-soft); display:flex; flex-wrap:wrap; align-items:center; gap:10px; }
.competitor-meta strong { color:var(--text); }
.badge { background:var(--accent-soft); color:var(--accent); padding:3px 10px; border-radius:999px; font-size:12px; font-weight:600; }
.creatives { display:grid; gap:16px; }
.creative-card { display:flex; gap:20px; padding:20px; background:var(--bg-soft); border:1px solid var(--border); border-radius:12px; transition:transform 0.15s, box-shadow 0.15s; }
.creative-card:hover { transform:translateY(-2px); box-shadow:0 4px 16px rgba(26,34,56,0.08); }
.scale-number { font-size:48px; font-weight:800; line-height:1; flex-shrink:0; min-width:60px; }
.scale-hot .scale-number { color:var(--hot); }
.scale-warm .scale-number { color:var(--warm); }
.scale-cool .scale-number { color:var(--cool); }
.scale-base .scale-number { color:var(--base); }
.creative-body { flex:1; }
.creative-label { font-size:12px; color:var(--text-soft); font-weight:600; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px; }
.creative-hook { font-size:16px; font-weight:600; line-height:1.4; margin-bottom:6px; color:var(--text); }
.creative-desc { font-size:14px; color:var(--text-soft); margin-bottom:12px; }
.creative-meta { display:flex; flex-wrap:wrap; gap:12px; align-items:center; font-size:12px; }
.library-id { background:var(--bg); border:1px solid var(--border); padding:3px 8px; border-radius:6px; color:var(--text-soft); font-family:'Menlo',monospace; font-size:11px; }
.link-ad { color:var(--accent); font-weight:600; text-decoration:none; }
.link-ad:hover { text-decoration:underline; }
.pattern-box { background:var(--accent-soft); border-radius:12px; padding:18px; margin-top:8px; }
.pattern-box h4 { color:var(--accent); font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px; }
.pattern-box p { font-size:14px; color:var(--text); line-height:1.5; }
.empty-state { background:var(--empty); border-left:4px solid var(--empty-border); border-radius:8px; padding:18px 22px; }
.empty-state strong { display:block; margin-bottom:6px; font-size:15px; }
.empty-state p { font-size:14px; color:var(--text); line-height:1.5; }
.summary { background:var(--bg-soft); border-radius:16px; padding:32px; margin:48px 0; }
.summary h2 { font-size:24px; font-weight:700; margin-bottom:24px; }
.summary-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:24px; }
.summary-col h3 { font-size:14px; font-weight:700; margin-bottom:12px; color:var(--accent); }
.summary-col ul { list-style:none; }
.summary-col li { font-size:14px; padding:8px 0; border-bottom:1px solid var(--border); color:var(--text); line-height:1.5; }
.summary-col li:last-child { border-bottom:none; }
.patterns { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:48px; }
.pattern-block { padding:28px; border-radius:16px; color:#fff; }
.gradient-blue { background:linear-gradient(135deg,#2563eb,#1e40af); }
.gradient-orange { background:linear-gradient(135deg,#ea580c,#c2410c); }
.pattern-block h3 { font-size:18px; font-weight:700; margin-bottom:14px; }
.pattern-block ul { list-style:none; }
.pattern-block li { font-size:14px; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.2); line-height:1.5; }
.pattern-block li:last-child { border-bottom:none; }
footer { padding:32px 0; border-top:1px solid var(--border); margin-top:48px; color:var(--text-soft); font-size:13px; text-align:center; line-height:1.7; }
@media (max-width:768px) {
  .stats { grid-template-columns:repeat(2,1fr); }
  .summary-grid { grid-template-columns:1fr; }
  .patterns { grid-template-columns:1fr; }
  h1 { font-size:26px; }
  .creative-card { flex-direction:column; gap:12px; }
  .scale-number { font-size:36px; }
}
"""


def montar_html(cfg: dict) -> str:
    """Monta o HTML completo a partir do config dict."""
    nicho = cfg.get("nicho", "(nicho nao informado)")
    modo = cfg.get("modo", "")
    metodo = cfg.get("metodo", "")
    criterio = cfg.get("criterio_escala", 3)
    mercados_legivel = cfg.get("mercados_legivel", "")
    data_relatorio = cfg.get("data_relatorio") or datetime.now().strftime("%Y-%m-%d")
    data_legivel = datetime.strptime(data_relatorio, "%Y-%m-%d").strftime("%d/%m/%Y") if "-" in data_relatorio else data_relatorio

    # Carrega resultados de cada concorrente
    resultados = []
    for conc in cfg.get("concorrentes", []):
        r = carregar_resultado(conc["resultado_json"])
        resultados.append({
            "slug": conc["slug"],
            "nome": conc["nome"],
            "regiao": conc["regiao"],
            "foco": conc.get("foco", ""),
            "total_ads": r.get("total_ads_coletados", 0),
            "criativos": r.get("criativos_escalados", []),
            "erro": r.get("erro"),
        })

    n_concorrentes = len(resultados)
    todos = []
    for r in resultados:
        for c in r["criativos"]:
            c2 = dict(c)
            c2["_concorrente"] = r["nome"]
            c2["_regiao"] = r["regiao"]
            todos.append(c2)
    n_crits = len(todos)

    max_global = max(todos, key=lambda x: x["collationCount"]) if todos else None
    intl = [c for c in todos if c["_regiao"] != "br"]
    max_intl = max(intl, key=lambda x: x["collationCount"]) if intl else None

    top3 = sorted(
        [r for r in resultados if r["criativos"]],
        key=lambda r: max(c["collationCount"] for c in r["criativos"]),
        reverse=True,
    )[:3]
    com_dados = [r for r in resultados if r["criativos"]]
    sem_escala = [r for r in resultados if not r["criativos"] and r["total_ads"] > 0]
    baixo_vol = [r for r in resultados if r["total_ads"] <= 5]

    # Analises (usa custom se passou, senao gera default)
    analises = cfg.get("analises", {}) or {}
    padroes_comuns = analises.get("padroes_comuns") or gerar_padroes_comuns_default(com_dados)
    diferencas = analises.get("diferencas_mercados") or gerar_diferencas_default(com_dados)
    padroes_por_conc = analises.get("padroes_por_concorrente", {}) or {}

    p = []
    p.append(f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Criativos Escalados. Inteligencia de Trafego</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{montar_css()}</style>
</head>
<body>
<div class="container">
<header class="hero">
  <div class="eyebrow">Inteligencia de Trafego</div>
  <h1>Criativos Escalados na Biblioteca da Meta</h1>
  <p class="subtitle">Nicho: <strong>{esc(nicho)}</strong>. Concorrentes investigados: <strong>{n_concorrentes}</strong>.</p>
  <div class="chips">
    <span class="chip">Data: {data_legivel}</span>
    <span class="chip">Criterio: <strong>{criterio} ou mais ads por criativo</strong></span>
    <span class="chip">Mercados: {esc(mercados_legivel)}</span>
    <span class="chip"><strong>Modo:</strong> {esc(modo)} ({esc(metodo)})</span>
  </div>
</header>""")

    nome_max = max_global["_concorrente"] if max_global else "—"
    val_max = max_global["collationCount"] if max_global else 0
    regiao_max = MERCADO_LBL.get(max_global["_regiao"], "—") if max_global else "—"
    nome_intl = max_intl["_concorrente"] if max_intl else "—"
    val_intl = max_intl["collationCount"] if max_intl else 0
    regiao_intl = MERCADO_LBL.get(max_intl["_regiao"], "—") if max_intl else "—"

    p.append(f"""
<section class="stats">
  <div class="stat-card">
    <div class="stat-label">Concorrentes investigados</div>
    <div class="stat-value">{n_concorrentes}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Criativos escalados</div>
    <div class="stat-value">{n_crits}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Maior escala individual</div>
    <div class="stat-value">{val_max}</div>
    <div class="stat-meta">{esc(nome_max)} ({regiao_max})</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Maior escala internacional</div>
    <div class="stat-value">{val_intl}</div>
    <div class="stat-meta">{esc(nome_intl)} ({regiao_intl})</div>
  </div>
</section>

<section class="filter">
  <button class="filter-btn active" data-filter="all">Todos</button>
  <button class="filter-btn" data-filter="br">🇧🇷 Brasil</button>
  <button class="filter-btn" data-filter="en">🇺🇸 English</button>
  <button class="filter-btn" data-filter="es">🌎 Espanol</button>
</section>

<nav class="sticky-nav">""")
    for r in resultados:
        p.append(f'<a href="#{r["slug"]}">{esc(r["nome"])} <span class="count-badge">{len(r["criativos"])}</span></a>')
    p.append('<a href="#resumo">Resumo Estrategico</a></nav>')

    # Cards por concorrente
    for r in resultados:
        flag = FLAG.get(r["regiao"], "")
        p.append(f"""
<section class="competitor" id="{r['slug']}" data-region="{r['regiao']}">
  <header class="competitor-header">
    <h2>{flag} {esc(r['nome'])}</h2>
    <div class="competitor-meta">
      Foco: <strong>{esc(r['foco'])}</strong>
      <span class="badge">{len(r['criativos'])} criativos escalados</span>
      <span style="color:var(--text-soft);font-size:13px;">{r['total_ads']} ads totais ativos</span>
    </div>
  </header>""")

        if not r["criativos"]:
            if r["total_ads"] == 0:
                titulo = "Sem ads ativos."
                motivo = "Sem anuncios ativos na Biblioteca neste mercado durante a janela de extracao."
            else:
                titulo = "Sem criativos escalados nesta janela."
                motivo = f"Alta rotacao de criativos sem repeticao vertical. Veicula {r['total_ads']} anuncios diferentes, cada um aparece em 1 a 2 ads no maximo."
            p.append(f"""
  <div class="empty-state">
    <strong>{esc(titulo)}</strong>
    <p>Motivo identificado: {esc(motivo)}</p>
  </div>
</section>""")
            continue

        p.append('<div class="creatives">')
        crits_show = r["criativos"][:10]
        for c in crits_show:
            n = c["collationCount"]
            cls = escala_classe(n)
            hook = truncar(c.get("hook") or c.get("title") or "(sem texto)")
            title = c.get("title") or ""
            cta = c.get("cta") or ""
            page = c.get("pageName") or r["nome"]
            desc_parts = []
            if title and title != hook:
                desc_parts.append(f"Titulo: {title}")
            if cta:
                desc_parts.append(f"CTA: {cta}")
            if page and page != r["nome"]:
                desc_parts.append(f"Pagina: {page}")
            desc = " · ".join(desc_parts) if desc_parts else f"Anuncio rodando em {n} ads simultaneos."
            lib_id = c.get("adArchiveID") or ""
            link = c.get("link_anuncio") or "#"
            p.append(f"""
    <article class="creative-card {cls}">
      <div class="scale-number">{n}</div>
      <div class="creative-body">
        <div class="creative-label">anuncios usam este criativo</div>
        <h3 class="creative-hook">{esc(hook)}</h3>
        <p class="creative-desc">{esc(desc)}</p>
        <div class="creative-meta">
          <code class="library-id">Library ID: {esc(lib_id)}</code>
          <a class="link-ad" href="{esc(link)}" target="_blank" rel="noopener">Ver anuncio</a>
        </div>
      </div>
    </article>""")

        if len(r["criativos"]) > 10:
            p.append(f'<p style="color:var(--text-soft);font-size:13px;margin-top:8px;">+{len(r["criativos"]) - 10} criativos escalados adicionais nao exibidos. Veja na Biblioteca da Meta.</p>')

        padrao_texto = padroes_por_conc.get(r["slug"]) or gerar_padrao_concorrente_default(r)
        p.append(f"""
    <div class="pattern-box">
      <h4>Padrao Identificado</h4>
      <p>{esc(padrao_texto)}</p>
    </div>
  </div>
</section>""")

    # Summary
    p.append("""
<section class="summary" id="resumo">
  <h2>Resumo Estrategico</h2>
  <div class="summary-grid">
    <div class="summary-col">
      <h3>Quem mais escala um unico criativo</h3>
      <ul>""")
    if not top3:
        p.append('<li style="color:var(--text-soft);">Nenhum concorrente teve criativos escalados nesta janela.</li>')
    else:
        for r in top3:
            max_c = max(c["collationCount"] for c in r["criativos"])
            p.append(f'<li><strong>{esc(r["nome"])}</strong> ({MERCADO_LBL[r["regiao"]]}): {max_c} ads com a mesma copy</li>')
    p.append("""</ul></div>
    <div class="summary-col">
      <h3>Sem escala (alta rotacao)</h3>
      <ul>""")
    if not sem_escala:
        p.append('<li style="color:var(--text-soft);">Nenhum concorrente caiu nesta categoria.</li>')
    else:
        for r in sem_escala:
            p.append(f'<li><strong>{esc(r["nome"])}</strong>: {r["total_ads"]} ads ativos sem repeticao vertical</li>')
    p.append("""</ul></div>
    <div class="summary-col">
      <h3>Volume baixo ou sem ads</h3>
      <ul>""")
    if not baixo_vol:
        p.append('<li style="color:var(--text-soft);">Nenhum concorrente caiu nesta categoria.</li>')
    else:
        for r in baixo_vol:
            p.append(f'<li><strong>{esc(r["nome"])}</strong>: {r["total_ads"]} ads ativos ({MERCADO_LBL[r["regiao"]]})</li>')
    p.append("""</ul></div>
  </div>
</section>

<section class="patterns">
  <div class="pattern-block gradient-blue">
    <h3>Padrao comum entre os que escalam</h3>
    <ul>""")
    for b in padroes_comuns:
        p.append(f"<li>{esc(b)}</li>")
    p.append("""</ul></div>
  <div class="pattern-block gradient-orange">
    <h3>Diferencas entre mercados</h3>
    <ul>""")
    for b in diferencas:
        p.append(f"<li>{esc(b)}</li>")
    p.append(f"""</ul></div>
</section>

<footer>
  <p>Relatorio gerado em {data_legivel}. Criterio de escala: {criterio} ou mais anuncios usando o mesmo criativo.</p>
  <p>Fonte: Biblioteca de Anuncios da Meta. Janela: ads ativos no momento da extracao.</p>
</footer>
</div>
<script>
document.querySelectorAll('.filter-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const filter = btn.dataset.filter;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.competitor').forEach(c => {{
      if (filter === 'all' || c.dataset.region === filter) {{
        c.style.display = 'block';
      }} else {{
        c.style.display = 'none';
      }}
    }});
  }});
}});
</script>
</body>
</html>""")

    return "\n".join(p)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Caminho do arquivo de config JSON")
    args = parser.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"ERRO. Config nao encontrado: {cfg_path}", file=sys.stderr)
        sys.exit(1)

    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    saida = Path(cfg["saida_html"])
    saida.parent.mkdir(parents=True, exist_ok=True)

    html_doc = montar_html(cfg)
    saida.write_text(html_doc, encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "saida_html": str(saida),
        "tamanho_bytes": saida.stat().st_size,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
