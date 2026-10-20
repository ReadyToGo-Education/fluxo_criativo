"""
painel-trafego.py

Injeta/atualiza os cards de análise de tráfego na seção analise-trafego
do painel-entregas.html do produto ativo.

Varre meus-produtos/{slug}/trafego/analise/ em busca de snapshots HTML
(arquivos com padrão {slug-output}-YYYY-MM-DD-HHMM.html) e gera um card
para cada um, ordenados do mais recente ao mais antigo.

Uso:
    python3 scripts/painel-trafego.py
    python3 scripts/painel-trafego.py --slug leitura-10x

O script é chamado automaticamente pela sub-skill _export-html.md ao final
de cada geração de snapshot.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
PRODUTOS_DIR = REPO_ROOT / "meus-produtos"
ATIVO_FILE = PRODUTOS_DIR / ".ativo"
PAINEL_NOME = "painel-entregas.html"

# Mapeamento slug → nome legível
SLUGS_NOMES = {
    "diagnostico-rapido":   "Diagnóstico Rápido",
    "performance-funil":    "Performance & Funil",
    "criativos-copy":       "Criativos & Copy",
    "geo-demografia":       "Geo & Demografia",
    "timing-sazonalidade":  "Timing & Sazonalidade",
    "investigacao-profunda": "Investigação Profunda",
    "lifecycle-historico":  "Lifecycle & Histórico",
    "problemas-ocultos":    "Problemas Ocultos",
    "orcamento-projecao":   "Orçamento & Projeção",
    "comparativo-ab":       "Comparativo A x B",
}

# Regex para extrair slug e timestamp do nome do arquivo
# Ex: criativos-copy-2026-05-06-1824.html
_SNAP_RE = re.compile(
    r"^(?P<slug>[a-z][a-z0-9-]+?)-(?P<ts>\d{4}-\d{2}-\d{2}-\d{4})\.html$"
)

_CSS = (
    "<style>"
    # Wrapper geral
    ".th-wrap{margin-top:var(--s-5)}"
    # Cabeçalho com contagem
    ".th-header{display:flex;align-items:baseline;gap:var(--s-3);"
    "margin-bottom:var(--s-6);padding-bottom:var(--s-3);"
    "border-bottom:1px solid var(--line-1)}"
    ".th-title{font-family:var(--font-mono);font-size:10px;font-weight:400;"
    "letter-spacing:.2em;text-transform:uppercase;color:var(--text-faint)}"
    ".th-count{font-family:var(--font-mono);font-size:10px;color:var(--neon);"
    "letter-spacing:.08em}"
    # Grupo por dia
    ".th-group{margin-bottom:var(--s-6)}"
    ".th-day{font-family:var(--font-mono);font-size:10px;font-weight:500;"
    "letter-spacing:.14em;text-transform:uppercase;color:var(--text-dim);"
    "padding:0 0 var(--s-2);margin-bottom:2px;"
    "border-bottom:1px solid var(--line-1)}"
    # Linha de entrada do log
    ".th-row{display:flex;align-items:center;gap:var(--s-4);"
    "padding:9px 0;border-bottom:1px solid var(--line-1);"
    "transition:background .12s;cursor:default}"
    ".th-row:last-child{border-bottom:none}"
    ".th-row:hover{background:var(--ink-2)}"
    # Indicador de linha do tempo (ponto + linha vertical)
    ".th-dot{width:6px;height:6px;border-radius:50%;background:var(--line-2);"
    "flex-shrink:0;margin-left:2px}"
    ".th-row:hover .th-dot{background:var(--neon)}"
    # Hora
    ".th-time{font-family:var(--font-mono);font-size:11px;color:var(--text-faint);"
    "width:42px;flex-shrink:0;letter-spacing:.04em}"
    ".th-row:hover .th-time{color:var(--text-mid)}"
    # Badge tipo de análise
    ".th-badge{font-family:var(--font-mono);font-size:9px;letter-spacing:.1em;"
    "text-transform:uppercase;color:var(--neon);background:var(--neon-deep);"
    "padding:2px 7px;border-radius:2px;flex-shrink:0;white-space:nowrap}"
    # Nome do output
    ".th-nome{font-family:var(--font-body);font-size:13px;font-weight:300;"
    "color:var(--text-mid);flex:1;min-width:0;white-space:nowrap;"
    "overflow:hidden;text-overflow:ellipsis}"
    ".th-row:hover .th-nome{color:var(--text-hi)}"
    # Fonte (Meta Ads)
    ".th-fonte{font-family:var(--font-mono);font-size:9px;color:var(--text-faint);"
    "letter-spacing:.06em;white-space:nowrap;flex-shrink:0}"
    # Botão abrir
    ".th-btn{font-family:var(--font-mono);font-size:10px;letter-spacing:.08em;"
    "color:var(--text-faint);text-decoration:none;flex-shrink:0;"
    "padding:3px 10px;border:1px solid var(--line-2);border-radius:2px;"
    "transition:color .12s,border-color .12s;white-space:nowrap}"
    ".th-btn:hover{color:var(--neon);border-color:var(--neon-deep)}"
    # Vazio
    ".th-empty{padding:var(--s-7);color:var(--text-faint);font-size:13px;"
    "font-family:var(--font-mono);border:1px dashed var(--line-2);"
    "border-radius:var(--r-md);text-align:center}"
    "</style>"
)


def ler_slug() -> str | None:
    if not ATIVO_FILE.exists():
        return None
    txt = ATIVO_FILE.read_text(encoding="utf-8").strip()
    return txt or None


def ts_para_display(ts: str) -> str:
    """Converte '2026-05-06-1824' → '06/05/2026 18:24'."""
    try:
        dt = datetime.strptime(ts, "%Y-%m-%d-%H%M")
        return dt.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return ts


def nome_output(slug: str) -> str:
    """Retorna nome legível do slug do output."""
    if slug in SLUGS_NOMES:
        return SLUGS_NOMES[slug]
    # fallback: primeira parte antes do slug do output (ex: "criativos")
    partes = slug.split("-")
    return " ".join(p.capitalize() for p in partes)


def escapar(txt: str) -> str:
    return txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_section(analise_dir: Path) -> str:
    """Gera o bloco HTML da seção analise-trafego como histórico cronológico."""
    snapshots: list[dict] = []

    if analise_dir.is_dir():
        for arq in sorted(analise_dir.iterdir(), reverse=True):
            if arq.name == "index.html" or not arq.name.endswith(".html"):
                continue
            m = _SNAP_RE.match(arq.name)
            if not m:
                continue
            slug_out = m.group("slug")
            ts = m.group("ts")
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d-%H%M")
                dia = dt.strftime("%d/%m/%Y")
                hora = dt.strftime("%H:%M")
            except ValueError:
                dia = ts[:10]
                hora = ts[11:]
            snapshots.append({
                "arquivo": arq.name,
                "nome": nome_output(slug_out),
                "dia": dia,
                "hora": hora,
                "ts_raw": ts,
            })

    snapshots.sort(key=lambda x: x["ts_raw"], reverse=True)

    if not snapshots:
        inner = (
            _CSS
            + '<div class="th-empty">Nenhuma análise gerada ainda.'
            " Execute /trafego-analise e salve um output como dashboard.</div>"
        )
        return f"<!-- SECTION:analise-trafego -->\n{inner}\n<!-- /SECTION:analise-trafego -->"

    # Agrupar por dia
    grupos: dict[str, list[dict]] = {}
    for snap in snapshots:
        grupos.setdefault(snap["dia"], []).append(snap)

    # Ordenar grupos por dia (mais recente primeiro)
    dias_ordenados = sorted(grupos.keys(), reverse=True)

    total = len(snapshots)
    grupos_html = ""
    for dia in dias_ordenados:
        linhas = ""
        for snap in grupos[dia]:
            nome_esc = escapar(snap["nome"])
            href = f"trafego/analise/{snap['arquivo']}"
            # Badge curto para o tipo
            badge = nome_esc.split("&")[0].strip()[:20]
            linhas += (
                f'<div class="th-row">'
                f'<span class="th-dot"></span>'
                f'<span class="th-time">{snap["hora"]}</span>'
                f'<span class="th-badge">{badge}</span>'
                f'<span class="th-nome">{nome_esc}</span>'
                f'<span class="th-fonte">Meta Ads</span>'
                f'<a href="{href}" target="_blank" class="th-btn">Abrir ↗</a>'
                f"</div>"
            )
        grupos_html += (
            f'<div class="th-group">'
            f'<div class="th-day">{escapar(dia)}</div>'
            f"{linhas}"
            f"</div>"
        )

    inner = (
        _CSS
        + '<div class="th-wrap">'
        + f'<div class="th-header">'
        + f'<span class="th-title">Histórico de análises</span>'
        + f'<span class="th-count">{total} snapshot{"s" if total != 1 else ""}</span>'
        + "</div>"
        + grupos_html
        + "</div>"
    )
    return f"<!-- SECTION:analise-trafego -->\n{inner}\n<!-- /SECTION:analise-trafego -->"


def substituir_secao(html_txt: str, novo_bloco: str) -> str:
    pad = re.compile(
        r"<!--\s*SECTION:analise-trafego\s*-->.*?<!--\s*/SECTION:analise-trafego\s*-->",
        re.DOTALL,
    )
    if pad.search(html_txt):
        return pad.sub(novo_bloco, html_txt, count=1)
    # Se não encontrou, não altera (seção não existe no painel)
    return html_txt


def main() -> int:
    parser = argparse.ArgumentParser(description="Atualiza seção de tráfego no painel-entregas.html")
    parser.add_argument("--slug", default="", help="Slug do produto (ex: leitura-10x)")
    args = parser.parse_args()

    slug = args.slug.strip() or ler_slug()
    if not slug:
        print("[ERRO] Produto ativo não encontrado. Informe --slug ou configure meus-produtos/.ativo.")
        return 1

    produto_dir = PRODUTOS_DIR / slug
    painel_path = produto_dir / PAINEL_NOME
    analise_dir = produto_dir / "trafego" / "analise"

    if not painel_path.exists():
        print(f"[ERRO] Painel não encontrado: {painel_path}")
        return 1

    existente = painel_path.read_text(encoding="utf-8")
    novo_bloco = render_section(analise_dir)
    atualizado = substituir_secao(existente, novo_bloco)

    if atualizado == existente:
        print("[AVISO] Seção analise-trafego não encontrada no painel. Nenhuma alteração feita.")
        print("        Execute /produto-concepcao para gerar o painel com a seção de tráfego.")
        return 0

    snapshots = analise_dir.glob("*.html") if analise_dir.is_dir() else []
    n = sum(1 for f in snapshots if f.name != "index.html")

    painel_path.write_text(atualizado, encoding="utf-8")
    print(f"✅ Painel atualizado: {painel_path}")
    print(f"   Seção analise-trafego: {n} snapshot(s) injetado(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
