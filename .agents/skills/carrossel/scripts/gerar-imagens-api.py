#!/usr/bin/env python3
"""
carrossel. Gerar as 6 imagens via API em paralelo.

Uso:
    python3 gerar-imagens-api.py \
        --prompts-file "/caminho/para/prompts.txt" \
        --output-dir "/caminho/para/imagens" \
        --provider openrouter

Le OPENROUTER_API_KEY ou OPENAI_API_KEY do .env.

Saida JSON em stdout:
{
    "provider": "openrouter",
    "total_solicitadas": 6,
    "sucesso": 6,
    "falhas": 0,
    "imagens": [
        {"slide": 1, "status": "ok", "path": "...", "erro": null},
        {"slide": 2, "status": "ok", "path": "...", "erro": null},
        ...
    ],
    "custo_estimado_usd": 0.12,
    "tempo_total_s": 58
}
"""

import argparse
import base64
import concurrent.futures
import json
import os
import sys
import time
import urllib.request
from pathlib import Path


def load_token_from_env(key_name: str):
    """Le {key_name} do .env subindo da raiz do script ate achar."""
    cur = Path(__file__).resolve().parent
    while cur.parent != cur:
        candidate = cur / ".env"
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                if line.startswith(f"{key_name}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
        cur = cur.parent

    return os.environ.get(key_name)


def carregar_prompts(prompts_file: str) -> list:
    """Le prompts.txt separados por linha em branco. Retorna lista de strings."""
    texto = Path(prompts_file).read_text(encoding="utf-8")
    blocos = [b.strip() for b in texto.split("\n\n") if b.strip()]
    return blocos


def gerar_openrouter(prompt: str, slide_num: int, token: str, output_path: Path) -> dict:
    """Gera 1 imagem via OpenRouter (google/gemini-3.1-flash-image-preview)."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": "google/gemini-3.1-flash-image-preview",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "modalities": ["image", "text"],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "HTTP-Referer": "https://workshop-marketing.local",
            "X-Title": "Workshop Marketing IA - Carrossel",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            response = json.loads(resp.read().decode("utf-8"))

        # OpenRouter retorna imagem em base64 dentro de message.images[0].image_url.url
        # ou message.content (depende do modelo). Tentamos os 2 formatos.
        msg = response.get("choices", [{}])[0].get("message", {})

        imagens_dict = msg.get("images") or []
        b64_image = None

        if imagens_dict:
            url_data = imagens_dict[0].get("image_url", {}).get("url", "")
            if url_data.startswith("data:image"):
                b64_image = url_data.split(",", 1)[1]

        if not b64_image:
            content = msg.get("content", "")
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "image_url":
                        url_data = item.get("image_url", {}).get("url", "")
                        if url_data.startswith("data:image"):
                            b64_image = url_data.split(",", 1)[1]
                            break

        if not b64_image:
            return {
                "slide": slide_num,
                "status": "erro",
                "path": None,
                "erro": "API nao retornou imagem (verifique modelo ou prompt)",
            }

        png_bytes = base64.b64decode(b64_image)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(png_bytes)

        return {
            "slide": slide_num,
            "status": "ok",
            "path": str(output_path),
            "erro": None,
        }

    except Exception as exc:
        return {
            "slide": slide_num,
            "status": "erro",
            "path": None,
            "erro": f"{type(exc).__name__}: {exc}",
        }


def gerar_openai(prompt: str, slide_num: int, token: str, output_path: Path) -> dict:
    """Gera 1 imagem via OpenAI gpt-image-1 (DALL-E)."""
    url = "https://api.openai.com/v1/images/generations"
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1024x1536",
        "n": 1,
    }

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

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            response = json.loads(resp.read().decode("utf-8"))

        items = response.get("data", [])
        if not items:
            return {
                "slide": slide_num,
                "status": "erro",
                "path": None,
                "erro": "OpenAI nao retornou imagem",
            }

        b64_image = items[0].get("b64_json")
        if not b64_image:
            image_url = items[0].get("url")
            if image_url:
                with urllib.request.urlopen(image_url, timeout=120) as r2:
                    png_bytes = r2.read()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(png_bytes)
                return {
                    "slide": slide_num,
                    "status": "ok",
                    "path": str(output_path),
                    "erro": None,
                }
            return {
                "slide": slide_num,
                "status": "erro",
                "path": None,
                "erro": "Resposta sem b64_json nem url",
            }

        png_bytes = base64.b64decode(b64_image)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(png_bytes)

        return {
            "slide": slide_num,
            "status": "ok",
            "path": str(output_path),
            "erro": None,
        }

    except Exception as exc:
        return {
            "slide": slide_num,
            "status": "erro",
            "path": None,
            "erro": f"{type(exc).__name__}: {exc}",
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts-file", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--provider",
        default="openrouter",
        choices=["openrouter", "openai"],
    )
    args = parser.parse_args()

    saida_base = {
        "provider": args.provider,
        "total_solicitadas": 0,
        "sucesso": 0,
        "falhas": 0,
        "imagens": [],
        "custo_estimado_usd": 0.0,
        "tempo_total_s": 0,
    }

    if args.provider == "openrouter":
        token = load_token_from_env("OPENROUTER_API_KEY")
    else:
        token = load_token_from_env("OPENAI_API_KEY")

    if not token:
        env_name = "OPENROUTER_API_KEY" if args.provider == "openrouter" else "OPENAI_API_KEY"
        saida_base["erro_global"] = f"{env_name} nao encontrado no .env"
        print(json.dumps(saida_base, ensure_ascii=False))
        sys.exit(1)

    try:
        prompts = carregar_prompts(args.prompts_file)
    except Exception as exc:
        saida_base["erro_global"] = f"Falha ao ler prompts.txt: {exc}"
        print(json.dumps(saida_base, ensure_ascii=False))
        sys.exit(1)

    saida_base["total_solicitadas"] = len(prompts)
    output_dir = Path(args.output_dir)

    gerador = gerar_openrouter if args.provider == "openrouter" else gerar_openai

    inicio = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = []
        for idx, prompt in enumerate(prompts, start=1):
            output_path = output_dir / f"slide-{idx}.png"
            futures.append(
                executor.submit(gerador, prompt, idx, token, output_path)
            )

        resultados = []
        for fut in concurrent.futures.as_completed(futures):
            resultados.append(fut.result())

    resultados.sort(key=lambda r: r["slide"])
    saida_base["imagens"] = resultados
    saida_base["sucesso"] = sum(1 for r in resultados if r["status"] == "ok")
    saida_base["falhas"] = sum(1 for r in resultados if r["status"] == "erro")
    saida_base["tempo_total_s"] = int(time.time() - inicio)

    if args.provider == "openrouter":
        saida_base["custo_estimado_usd"] = round(saida_base["sucesso"] * 0.02, 3)
    else:
        saida_base["custo_estimado_usd"] = round(saida_base["sucesso"] * 0.06, 3)

    print(json.dumps(saida_base, ensure_ascii=False))


if __name__ == "__main__":
    main()
