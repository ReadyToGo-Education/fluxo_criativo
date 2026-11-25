#!/usr/bin/env python3
"""
biblioteca-anuncios. Buscar criativos escalados via Apify.

Uso:
    python3 buscar-apify.py \
        --concorrente "Erico Rocha" \
        --pais BR \
        --criterio-escala 3 \
        --count 100 \
        --actor curious_coder

Saida JSON em stdout:
{
    "concorrente": "Erico Rocha",
    "pais": "BR",
    "total_ads_coletados": 87,
    "criativos_escalados": [
        {
            "collationCount": 12,
            "collationID": "abc123",
            "adArchiveID": "1234567890",
            "pageName": "Erico Rocha",
            "hook": "Primeira linha da copy...",
            "title": "Titulo do anuncio",
            "cta": "LEARN_MORE",
            "startDate": "2026-04-01",
            "link_anuncio": "https://www.facebook.com/ads/library/?id=1234567890"
        }
    ],
    "erro": null
}

Em caso de erro:
{
    "concorrente": "...",
    "pais": "...",
    "erro": "mensagem de erro",
    "total_ads_coletados": 0,
    "criativos_escalados": []
}

Le APIFY_API_TOKEN do .env na raiz do projeto.
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


# Forca UTF-8 no stdout. No Windows o default e cp1252 e quebra com emojis.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, Exception):
    pass


ACTORS = {
    "curious_coder": "curious_coder~facebook-ads-library-scraper",
    "apify_oficial": "apify~facebook-ads-scraper",
}


def load_token_from_env():
    """Le APIFY_API_TOKEN do .env subindo da raiz do script ate achar."""
    cur = Path(__file__).resolve().parent
    while cur.parent != cur:
        candidate = cur / ".env"
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                if line.startswith("APIFY_API_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
        cur = cur.parent

    env_var = os.environ.get("APIFY_API_TOKEN")
    if env_var:
        return env_var

    return None


def montar_url_biblioteca(concorrente: str, pais: str) -> str:
    """Monta a URL da Biblioteca de Anuncios da Meta."""
    nome_encoded = urllib.parse.quote(concorrente)
    return (
        f"https://www.facebook.com/ads/library/"
        f"?active_status=active"
        f"&ad_type=all"
        f"&country={pais}"
        f"&q={nome_encoded}"
        f"&search_type=keyword_unordered"
        f"&media_type=all"
    )


def http_post(url: str, payload: dict, token: str) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_get(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_get_raw(url: str, token: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def start_run(actor_id: str, token: str, input_payload: dict) -> dict:
    url = f"https://api.apify.com/v2/acts/{actor_id}/runs"
    return http_post(url, input_payload, token)


def wait_for_run(run_id: str, token: str, max_wait_s: int = 600) -> dict:
    url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    waited = 0
    while waited < max_wait_s:
        data = http_get(url, token)
        status = data.get("data", {}).get("status")
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            return data.get("data", {})
        time.sleep(5)
        waited += 5
    raise TimeoutError(f"Run {run_id} demorou mais de {max_wait_s}s")


def get_dataset_items(dataset_id: str, token: str) -> list:
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?format=json"
    raw = http_get_raw(url, token)
    return json.loads(raw.decode("utf-8"))


def extrair_hook(snapshot: dict) -> str:
    """Pega a primeira linha util da copy."""
    body = snapshot.get("body") or {}
    text = body.get("text") or ""
    if not text:
        text = snapshot.get("title") or ""
    primeira_linha = text.split("\n")[0].strip()
    if len(primeira_linha) > 140:
        primeira_linha = primeira_linha[:137] + "..."
    return primeira_linha


def primeiro_valor_nao_nulo(item: dict, chaves: list):
    """Retorna o primeiro valor nao-None entre as chaves listadas."""
    for chave in chaves:
        valor = item.get(chave)
        if valor is not None:
            return valor
    return None


def normalizar_item(item: dict) -> dict:
    """Normaliza item de qualquer dos actors suportados.

    Os actors podem usar:
    - snake_case (curious_coder~facebook-ads-library-scraper): collation_count, ads_count, ad_archive_id, page_name
    - camelCase (apify~facebook-ads-scraper): collationCount, adArchiveID, pageName
    - Title Case (variante antiga): "Collation Count", "Ad Archive ID", "Page Name"

    Para a contagem de escala, usa collation_count se nao for None,
    senao ads_count (ambos do curious_coder representam o mesmo conceito).
    """
    # Contagem de escala: tenta varias chaves e usa o primeiro valor nao-None.
    collation_count = primeiro_valor_nao_nulo(item, [
        "collation_count",  # curious_coder
        "collationCount",   # apify oficial
        "Collation Count",  # variante Title Case
        "ads_count",        # fallback curious_coder quando collation_count e None
        "adsCount",
    ])
    if collation_count is None:
        collation_count = 1

    collation_id = primeiro_valor_nao_nulo(item, [
        "collation_id", "collationID", "Collation ID",
    ]) or ""

    ad_archive_id = primeiro_valor_nao_nulo(item, [
        "ad_archive_id", "adArchiveID", "adArchiveId", "Ad Archive ID", "ad_id",
    ]) or ""

    page_name = primeiro_valor_nao_nulo(item, [
        "page_name", "pageName", "Page Name",
    ]) or ""

    start_date = primeiro_valor_nao_nulo(item, [
        "start_date_formatted", "start_date", "startDate", "Start Date",
    ]) or ""

    snapshot = item.get("snapshot") or {}
    cta = snapshot.get("cta_type") or snapshot.get("callToActionType") or item.get("CTA") or ""
    title = snapshot.get("title") or snapshot.get("link_url") or ""

    return {
        "collationCount": int(collation_count),
        "collationID": str(collation_id),
        "adArchiveID": str(ad_archive_id),
        "pageName": page_name,
        "hook": extrair_hook(snapshot),
        "title": title,
        "cta": cta,
        "startDate": start_date,
        "link_anuncio": f"https://www.facebook.com/ads/library/?id={ad_archive_id}"
        if ad_archive_id
        else "",
    }


def detectar_campo_count_ausente(items: list) -> dict:
    """Sanity check: detecta se nenhum item tem campo de contagem reconhecido.

    Retorna dict com warning se 100% dos items caem no default 1 mesmo havendo
    chaves desconhecidas que se parecem com contagem.
    """
    if not items:
        return {}

    chaves_conhecidas = {
        "collation_count", "collationCount", "Collation Count",
        "ads_count", "adsCount",
    }
    chaves_suspeitas = set()
    items_com_count_conhecido = 0

    for item in items:
        if not isinstance(item, dict):
            continue
        for k in item.keys():
            kl = k.lower()
            if k in chaves_conhecidas and item.get(k) is not None:
                items_com_count_conhecido += 1
                break
            if ("collat" in kl or "count" in kl) and k not in chaves_conhecidas:
                chaves_suspeitas.add(k)

    # Se nenhum item tem campo conhecido com valor mas existem chaves suspeitas,
    # provavelmente o actor mudou o nome do campo.
    if items_com_count_conhecido == 0 and chaves_suspeitas:
        return {
            "campo_count_nao_reconhecido": True,
            "chaves_suspeitas": sorted(chaves_suspeitas),
            "mensagem": (
                "Nenhum item retornou campo de contagem reconhecido. "
                "O actor pode ter renomeado o campo. Atualize normalizar_item() "
                "em buscar-apify.py com as chaves suspeitas acima."
            ),
        }
    return {}


def filtrar_e_deduplicar(items: list, criterio_escala: int) -> list:
    """Filtra collationCount >= criterio_escala e mantem 1 por collationID."""
    vistos = set()
    resultado = []
    for item in items:
        norm = normalizar_item(item)
        if norm["collationCount"] < criterio_escala:
            continue
        chave = norm["collationID"] or norm["adArchiveID"]
        if chave and chave in vistos:
            continue
        vistos.add(chave)
        resultado.append(norm)
    resultado.sort(key=lambda x: x["collationCount"], reverse=True)
    return resultado


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concorrente", required=True)
    parser.add_argument("--pais", required=True, choices=["BR", "US", "MX", "AR", "CO", "ES"])
    parser.add_argument("--criterio-escala", type=int, default=3)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument(
        "--actor",
        default="curious_coder",
        choices=list(ACTORS.keys()),
    )
    args = parser.parse_args()

    saida_base = {
        "concorrente": args.concorrente,
        "pais": args.pais,
        "actor": args.actor,
        "total_ads_coletados": 0,
        "criativos_escalados": [],
        "erro": None,
    }

    token = load_token_from_env()
    if not token:
        saida_base["erro"] = "APIFY_API_TOKEN nao encontrado no .env"
        print(json.dumps(saida_base, ensure_ascii=False))
        sys.exit(1)

    actor_id = ACTORS[args.actor]
    url_biblioteca = montar_url_biblioteca(args.concorrente, args.pais)

    input_payload = {
        "urls": [{"url": url_biblioteca}],
        "count": args.count,
        "scrapeAdDetails": True,
    }

    try:
        run = start_run(actor_id, token, input_payload)
        run_id = run.get("data", {}).get("id")
        if not run_id:
            saida_base["erro"] = "Nao consegui iniciar o run do actor"
            print(json.dumps(saida_base, ensure_ascii=False))
            sys.exit(1)

        run_final = wait_for_run(run_id, token)
        if run_final.get("status") != "SUCCEEDED":
            saida_base["erro"] = f"Run terminou com status {run_final.get('status')}"
            print(json.dumps(saida_base, ensure_ascii=False))
            sys.exit(1)

        dataset_id = run_final.get("defaultDatasetId")
        items = get_dataset_items(dataset_id, token)
        saida_base["total_ads_coletados"] = len(items)
        saida_base["criativos_escalados"] = filtrar_e_deduplicar(
            items, args.criterio_escala
        )

        # Sanity check: detecta se o campo de contagem mudou de nome no actor
        warning = detectar_campo_count_ausente(items)
        if warning:
            saida_base["warning"] = warning

        print(json.dumps(saida_base, ensure_ascii=False))
    except Exception as exc:
        saida_base["erro"] = f"{type(exc).__name__}: {exc}"
        print(json.dumps(saida_base, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
