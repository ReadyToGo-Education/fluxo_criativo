"""Análise 4.5 — Pausa Hierárquica.

Decide o NÍVEL correto de pausa: anúncio, adset ou campanha inteira.

Regra VTSD:
  - Campanha com 1 adset e todos ads ruins → pausar a campanha inteira (1 clique vale por muitos)
  - Campanha com múltiplos adsets, só um adset ruim → pausar só o adset
  - Campanha saudável no geral, só alguns ads específicos ruins → pausar os ads

Heurística de "ruim":
  - Gasto > R$ 50 e zero conversão
  - OU CPA > 2x a mediana + frequency > 4.0 + rankings múltiplos below_average
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Any

from trafego_analysis.core import meta_client as mc
from trafego_analysis.core import report
from trafego_analysis.core.periods import Period


@dataclass
class RecomendacaoPausa:
    nivel: str                    # "ad" | "adset" | "campaign"
    alvo: str                     # nome do recurso a pausar
    justificativa: str
    ads_afetados: int
    economia_estimada: float      # R$/dia a recuperar
    prioridade: int               # 1 = alta urgência


def _cpa(row: dict) -> float | None:
    spend = float(row.get("spend") or 0)
    p = mc.extract_action_count(row.get("actions"), "purchase")
    l = mc.extract_action_count(row.get("actions"), "lead")
    r = p or l
    return (spend / r) if r > 0 else None


def _ad_ruim(row: dict, cpa_mediano: float | None) -> bool:
    """Heurística para ad 'ruim'."""
    spend = float(row.get("spend") or 0)
    if spend < 50:
        return False

    p = mc.extract_action_count(row.get("actions"), "purchase")
    l = mc.extract_action_count(row.get("actions"), "lead")
    results = p or l

    # Zero conversão
    if results == 0:
        return True

    # CPA 2x mediano
    if cpa_mediano:
        cpa = spend / results
        if cpa > cpa_mediano * 2:
            freq = float(row.get("frequency") or 0)
            rankings = [
                row.get("quality_ranking"),
                row.get("engagement_rate_ranking"),
                row.get("conversion_rate_ranking"),
            ]
            below = sum(1 for r in rankings if r and str(r).lower().startswith("below_average"))
            if freq > 4.0 and below >= 1:
                return True

    return False


def decidir_pausas(rows: list[dict[str, Any]]) -> list[RecomendacaoPausa]:
    # CPA mediano (pra comparação)
    cpas = [c for r in rows if (c := _cpa(r)) is not None]
    cpa_med = median(cpas) if cpas else None

    # Agrupa ads por campaign / adset
    estrutura: dict[str, dict[str, list[dict]]] = {}
    for r in rows:
        cname = r.get("campaign_name") or "(sem campaign)"
        aname = r.get("adset_name") or "(sem adset)"
        estrutura.setdefault(cname, {}).setdefault(aname, []).append(r)

    recomendacoes: list[RecomendacaoPausa] = []

    for cname, adsets in estrutura.items():
        campaign_ads = [ad for a in adsets.values() for ad in a]
        total_campaign_ads = len(campaign_ads)
        campaign_ads_ruins = [ad for ad in campaign_ads if _ad_ruim(ad, cpa_med)]
        campaign_gasto_ruim_diario = sum(
            float(ad.get("spend") or 0) for ad in campaign_ads_ruins
        ) / 7

        # Caso 1: TODA a campanha está ruim (1 adset e todos ads ruins, ou múltiplos adsets todos ruins)
        if total_campaign_ads > 0 and len(campaign_ads_ruins) == total_campaign_ads and total_campaign_ads >= 2:
            recomendacoes.append(RecomendacaoPausa(
                nivel="campaign",
                alvo=cname,
                justificativa=(
                    f"TODOS os {total_campaign_ads} ads dessa campanha estão com sinais ruins. "
                    "Pausar a campanha inteira é mais eficiente que pausar 1 por 1."
                ),
                ads_afetados=total_campaign_ads,
                economia_estimada=campaign_gasto_ruim_diario,
                prioridade=1,
            ))
            continue

        # Caso 2: Um adset inteiro ruim (todos ads ruins) em campanha com múltiplos adsets
        if len(adsets) >= 2:
            for aname, ads_adset in adsets.items():
                ads_ruins_adset = [ad for ad in ads_adset if _ad_ruim(ad, cpa_med)]
                if len(ads_adset) >= 2 and len(ads_ruins_adset) == len(ads_adset):
                    gasto_diario = sum(
                        float(ad.get("spend") or 0) for ad in ads_ruins_adset
                    ) / 7
                    recomendacoes.append(RecomendacaoPausa(
                        nivel="adset",
                        alvo=f"{cname} / {aname}",
                        justificativa=(
                            f"Todos os {len(ads_adset)} ads do adset estão ruins. "
                            "Pausar o adset — outros adsets da mesma campanha continuam rodando."
                        ),
                        ads_afetados=len(ads_adset),
                        economia_estimada=gasto_diario,
                        prioridade=2,
                    ))
                    # Marca que já resolveu esse adset — não duplicar com ads individuais
                    for ad in ads_adset:
                        ad["_handled_by_adset_pause"] = True

        # Caso 3: ads individuais ruins (fora de adsets já marcados)
        for aname, ads_adset in adsets.items():
            for ad in ads_adset:
                if ad.get("_handled_by_adset_pause"):
                    continue
                if _ad_ruim(ad, cpa_med):
                    spend_diario = float(ad.get("spend") or 0) / 7
                    recomendacoes.append(RecomendacaoPausa(
                        nivel="ad",
                        alvo=f"{ad.get('ad_name', '?')} (em {cname})",
                        justificativa=(
                            "Ad individual com sinais ruins. Campanha e adset saudáveis — "
                            "pausar apenas esse ad."
                        ),
                        ads_afetados=1,
                        economia_estimada=spend_diario,
                        prioridade=3,
                    ))

    # Ordena por prioridade + economia
    recomendacoes.sort(key=lambda r: (r.prioridade, -r.economia_estimada))
    return recomendacoes


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

    recs = decidir_pausas(rows)
    economia_total = sum(r.economia_estimada for r in recs)

    context = {
        "produto": produto_nome or "todos",
        "periodo": periodo,
        "recomendacoes": recs,
        "total": len(recs),
        "economia_total_diaria": economia_total,
    }
    filename = report.build_output_filename("pausa-hierarquica", produto_nome)
    return report.render_markdown("pausa_hierarquica.md.j2", context, output_filename=filename)
