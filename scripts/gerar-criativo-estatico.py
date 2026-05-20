# -*- coding: utf-8 -*-
"""
Gera um criativo estatico de anuncio via OpenRouter, a partir de um prompt.

O modelo de imagem gera a arte completa (cena, texto e layout) em uma unica
chamada, igual ao que aconteceria colando o prompt no ChatGPT ou no Gemini.
Sem template HTML, sem composicao, sem navegador.

Usado pela skill /criativo-estatico no modo "Gerar agora pela API".

Uso:
  py -3 scripts/gerar-criativo-estatico.py \
      --prompt-file meus-produtos/{slug}/entregas/criativos/prompt-1.txt \
      --model openai/gpt-5.4-image-2 \
      --aspect 4:5 \
      --out meus-produtos/{slug}/entregas/criativos/criativo-aida-1.png

  # Uso com imagem de referência (image-to-image):
  py -3 scripts/gerar-criativo-estatico.py \
      --prompt-file .../prompt-stories.txt \
      --reference-image .../criativo-feed.png \
      --model google/gemini-3.1-flash-image-preview \
      --aspect 9:16 \
      --out .../criativo-stories.png

Modelos usados pela skill:
  openai/gpt-5.4-image-2                  (GPT Image 2, recomendado)
  google/gemini-3.1-flash-image-preview   (Gemini Nano Banana 2)

Chave da API:
  Preencha OPENROUTER_API_KEY no arquivo .env da raiz do projeto.
  O .env nao vai para o Git. O comando /configurar-imagens guia o processo.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_env_file(path: Path) -> None:
    """Carrega VAR=valor no processo. Nao sobrescreve variavel ja definida."""
    if not path.is_file():
        return
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        key, _, rest = s.partition("=")
        key = key.strip()
        val = rest.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        if key and key not in os.environ:
            os.environ[key] = val


def _png_to_data_url(path: Path) -> str:
    """Lê um PNG/JPG/WEBP local e devolve uma data URL base64."""
    raw = path.read_bytes()
    ext = path.suffix.lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    if ext not in {"png", "jpeg", "webp"}:
        raise ValueError(f"Formato de imagem nao suportado para referencia: {path.suffix}")
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:image/{ext};base64,{b64}"


def gerar_imagem(
    api_key: str,
    model: str,
    prompt: str,
    aspect_ratio: str,
    reference_image: Path | None = None,
) -> str:
    """Chama a OpenRouter e devolve a data URL da imagem gerada.

    Se reference_image for passado, o content vira multimodal (texto + imagem)
    e o modelo trata como image-to-image, mantendo a cena, cores e elementos
    da imagem de referencia e ajustando para a nova proporcao.
    """
    if reference_image is not None:
        content: Any = [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": _png_to_data_url(reference_image)},
            },
        ]
    else:
        content = prompt

    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": aspect_ratio, "image_size": "1K"},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/workshop_inteligente",
        "X-Title": "Workshop Marketing IA criativo estatico",
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OPENROUTER_URL, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=300) as resp:
        body = resp.read().decode("utf-8")
    result = json.loads(body)
    if result.get("error"):
        raise RuntimeError(json.dumps(result["error"], ensure_ascii=False))
    choices = result.get("choices") or []
    if not choices:
        raise RuntimeError("Resposta sem choices: " + json.dumps(result)[:600])
    message = choices[0].get("message") or {}
    images = message.get("images") or []
    if not images:
        raise RuntimeError(
            "A resposta nao trouxe imagem. Conteudo: "
            + json.dumps(message, ensure_ascii=False)[:800]
        )
    first = images[0]
    url = None
    if isinstance(first, dict):
        iu = first.get("image_url") or first.get("imageUrl")
        if isinstance(iu, dict):
            url = iu.get("url")
        elif isinstance(iu, str):
            url = iu
    if not (isinstance(url, str) and url.startswith("data:image")):
        raise RuntimeError("Formato de imagem inesperado na resposta da API.")
    return url


def salvar_imagem(data_url: str, dest: Path) -> None:
    """Decodifica a data URL base64 e grava o arquivo."""
    m = re.match(r"data:image/(png|jpeg|jpg|webp);base64,(.+)", data_url, re.DOTALL)
    if not m:
        raise ValueError("URL de imagem inesperada (esperado data:image/...;base64,...).")
    raw = base64.b64decode(m.group(2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)


def main() -> int:
    load_env_file(ROOT / ".env")

    ap = argparse.ArgumentParser(
        description="Gera um criativo estatico de anuncio via OpenRouter."
    )
    ap.add_argument("--prompt-file", required=True,
                    help="Arquivo .txt com o prompt da imagem")
    ap.add_argument("--model", required=True,
                    help="Modelo OpenRouter (ex: openai/gpt-5.4-image-2)")
    ap.add_argument("--aspect", default="4:5",
                    help="Proporcao da imagem (ex: 4:5, 9:16, 1:1)")
    ap.add_argument("--out", required=True,
                    help="Caminho do PNG de saida, relativo a raiz do projeto")
    ap.add_argument("--reference-image", default=None,
                    help="Imagem PNG/JPG/WEBP de referencia para image-to-image. "
                         "Quando passada, o modelo recebe a imagem junto com o prompt.")
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        print(
            "Nao encontrei OPENROUTER_API_KEY no .env da raiz do projeto.\n"
            "Configure com o comando /configurar-imagens e tente de novo.",
            file=sys.stderr,
        )
        return 1

    prompt_path = Path(args.prompt_file)
    if not prompt_path.is_absolute():
        prompt_path = ROOT / prompt_path
    if not prompt_path.is_file():
        print(f"Arquivo de prompt nao encontrado: {prompt_path}", file=sys.stderr)
        return 1
    prompt = prompt_path.read_text(encoding="utf-8").strip()
    if not prompt:
        print("O arquivo de prompt esta vazio.", file=sys.stderr)
        return 1

    raw_out = args.out.strip().replace("\\", "/")
    if ".." in raw_out or raw_out.startswith("/"):
        print("Caminho de --out invalido. Use um caminho relativo a raiz do projeto.",
              file=sys.stderr)
        return 1
    dest = ROOT / raw_out

    reference_image_path: Path | None = None
    if args.reference_image:
        ref_raw = args.reference_image.strip().replace("\\", "/")
        ref = Path(ref_raw)
        if not ref.is_absolute():
            ref = ROOT / ref
        if not ref.is_file():
            print(f"Imagem de referencia nao encontrada: {ref}", file=sys.stderr)
            return 1
        reference_image_path = ref

    print(f"Modelo: {args.model}")
    print(f"Proporcao: {args.aspect}")
    print(f"Arquivo: {raw_out}")
    if reference_image_path is not None:
        print(f"Referencia visual: {reference_image_path}")
    try:
        data_url = gerar_imagem(
            api_key, args.model, prompt, args.aspect, reference_image_path
        )
        salvar_imagem(data_url, dest)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"ERRO HTTP {e.code}: {err_body[:500]}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 1

    print("Concluido.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
