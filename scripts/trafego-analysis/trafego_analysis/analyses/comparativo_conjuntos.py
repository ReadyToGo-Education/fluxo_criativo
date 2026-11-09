"""Análise 1.3 — Comparativo de Conjuntos (HOT / COLD / SUPERCOLD).

Classifica cada conjunto de anúncios (adset) por **temperatura de público** via
heurística de nome + objetivo, e compara performance:

  - CPL/CPA por temperatura
  - % do orçamento em cada temperatura vs. % dos resultados
  - Detecção de anomalia: HOT mais caro que COLD (problema na lista quente)
  - Oportunidade: SUPERCOLD com CPA aceitável (escala via público aberto)

Atua em **nível de conjunto (adset)**, não campanha.

No VTSD: o mix HOT/COLD/SUPERCOLD depende da fase:
  - Pico: 40/40/20
  - Evergreen: 20/50/30
  - Caixa Rápido: 0-20/40/40-60
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from trafego_analysis.core import meta_client as mc
from trafego_analysis.core import metrics as m
from trafego_analysis.core import report
from trafego_analysis.core.periods import Period

# Heurísticas para classificar adset por temperatura.
# Nota: `_` faz parte de \w, então `\b` não funciona em `_rmk_` — usamos
# (?:^|[^a-z]) / (?:[^a-z]|$) para permitir underscore/hífen como separador.
_SEP = r"(?:^|[^a-z0-9])"
_SEP_END = r"(?:[^a-z0-9]|$)"

PATTERNS = {
    "HOT": [
        rf"{_SEP}hot{_SEP_END}",
        rf"{_SEP}rmk{_SEP_END}",
        r"retarget",
        r"remarketing",
        r"engajam",
        r"lista",
        r"video.?view",
    ],
    "COLD": [
        rf"{_SEP}cold{_SEP_END}",
        r"lookalike",
        rf"{_SEP}lal{_SEP_END}",
        r"interess",
        r"prospect",
    ],
    "SUPERCOLD": [
        r"super.?cold",
        r"supercold",
        r"aberto",
        r"broad",
        rf"{_SEP}open{_SEP_END}",
        r"advantage",
    ],
}


def classificar_temperatura(nome: str) -> str:
    """Retorna 'HOT', 'COLD' ou 'SUPERCOLD'. Fallback: 'INDEFINIDO'."""
    n = (nome or "").lower()
    # Ordem de tentativa: SUPERCOLD → HOT → COLD (SUPERCOLD é mais específico)
    for temp, patts in [("SUPERCOLD", PATTERNS["SUPERCOLD"]),
                         ("HOT", PATTERNS["HOT"]),
                         ("COLD", PATTERNS["COLD"])]:
        for p in patts:
            if re.search(p, n):
                return temp
    return "INDEFINIDO"


@dataclass
class TempResumo:
    nome: str
    adsets: list[str] = field(default_factory=list)
    spend: float = 0.0
    impressions: float = 0.0
    clicks: float = 0.0
    results: float = 0.0
    # Calculados
    cpl: float = 0.0
    ctr: float = 0.0
    cpm: float = 0.0
    share_spend: float = 0.0
    share_results: float = 0.0


def _extract_results(row: dict) -> float:
    p = mc.extract_action_count(row.get("actions"), "purchase")
    l = mc.extract_action_count(row.get("actions"), "lead")
    return p or l


def analisar_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Agrupa por temperatura e calcula métricas + insights VTSD."""
    buckets: dict[str, TempResumo] = {
        "HOT": TempResumo("HOT"),
        "COLD": TempResumo("COLD"),
        "SUPERCOLD": TempResumo("SUPERCOLD"),
        "INDEFINIDO": TempResumo("INDEFINIDO"),
    }

    adsets_vistos: set[str] = set()
    for r in rows:
        # Classifica pelo nome do adset primeiro, fallback campanha
        adset_name = r.get("adset_name") or ""
        temp = classificar_temperatura(adset_name)
        if temp == "INDEFINIDO":
            temp = classificar_temperatura(r.get("campaign_name") or "")

        b = buckets[temp]
        if adset_name and adset_name not in adsets_vistos:
            b.adsets.append(adset_name)
            adsets_vistos.add(adset_name)

        b.spend += float(r.get("spend") or 0)
        b.impressions += float(r.get("impressions") or 0)
        b.clicks += float(r.get("inline_link_clicks") or r.get("clicks") or 0)
        b.results += _extract_results(r)

    # Calcula métricas derivadas
    total_spend = sum(b.spend for b in buckets.values())
    total_results = sum(b.results for b in buckets.values())
    for b in buckets.values():
        b.cpl = m.cpa(b.spend, b.results)
        b.ctr = m.ctr(b.clicks, b.impressions)
        b.cpm = m.cpm(b.spend, b.impressions)
        b.share_spend = (b.spend / total_spend * 100) if total_spend else 0
        b.share_results = (b.results / total_results * 100) if total_results else 0

    # Insights VTSD
    insights: list[str] = []

    # HOT mais caro que COLD = problema
    hot = buckets["HOT"]
    cold = buckets["COLD"]
    if hot.spend > 0 and cold.spend > 0 and hot.cpl > cold.cpl * 1.2 and hot.results > 0:
        insights.append(
            f"🔴 **HOT custando mais que COLD** (HOT {hot.cpl:.2f} > COLD {cold.cpl:.2f}). "
            "No VTSD isso aponta para **qualidade ruim da lista quente** — pode ser Identidade "
            "do Consumidor desalinhada, engajamento de baixa qualidade ou lista antiga/saturada."
        )

    # SUPERCOLD performando bem = oportunidade
    sc = buckets["SUPERCOLD"]
    if sc.spend > 50 and sc.cpl > 0 and cold.cpl > 0 and sc.cpl <= cold.cpl * 1.3:
        insights.append(
            f"🟢 **SUPERCOLD com CPA aceitável** (CPL {sc.cpl:.2f}). "
            "Sinal forte de espaço para escala com público aberto — Meta achando "
            "Identidade do Consumidor sozinha. Ampliar budget aqui é seguro."
        )

    # INDEFINIDO alto = problema de nomenclatura
    ind = buckets["INDEFINIDO"]
    if ind.spend > 0 and ind.share_spend > 15:
        insights.append(
            f"⚠️ **{ind.share_spend:.0f}% do gasto em conjuntos sem classificação** (nome não bate com padrões). "
            "Padronize nomes (ex: `HOT_LAL1_v2`, `COLD_interesse_X`, `SUPERCOLD_broad`) "
            "para o diagnóstico VTSD ficar preciso."
        )

    if not insights:
        insights.append(
            "Distribuição HOT/COLD/SUPERCOLD sem anomalias. "
            "Verifique se o mix bate com a fase VTSD atual (Pico vs. Evergreen vs. Caixa Rápido)."
        )

    return {
        "buckets": [b for b in buckets.values() if b.spend > 0 or b.results > 0],
        "total_spend": total_spend,
        "total_results": total_results,
        "insights": insights,
    }


def analisar(
    *,
    meta: mc.MetaClient,
    ad_account_id: str,
    periodo: Period,
    produto_nome: str | None = None,
    filtering: list[dict[str, Any]] | None = None,
) -> tuple[str, Any]:
    rows = meta.get_ad_insights(
        ad_account_id, since=periodo.since, until=periodo.until, filtering=filtering,
    )
    if produto_nome:
        nome_low = produto_nome.lower()
        rows = [r for r in rows if nome_low in (r.get("campaign_name") or "").lower()]

    resultado = analisar_rows(rows)

    context = {
        "produto": produto_nome or "todos",
        "periodo": periodo,
        **resultado,
    }
    filename = report.build_output_filename("comparativo-conjuntos", produto_nome)
    return report.render_markdown(
        "comparativo_conjuntos.md.j2", context, output_filename=filename,
    )
