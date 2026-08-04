#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anima um criativo estático em loop (image-to-video) via Replicate.

Recebe a imagem do criativo já gerada (Feed ou Stories) e um prompt de
animação, e devolve um vídeo MP4 em loop com o texto estático e apenas
o fundo em movimento.

Uso:
  py -3 scripts/animar-criativo.py \
      --image "meus-produtos/{ativo}/entregas/criativos/criativo-x-1-feed.png" \
      --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-x-1-loop.txt" \
      --out "meus-produtos/{ativo}/entregas/criativos/criativo-x-1-loop.mp4"

Modelos (atalhos):
  i2v          -> wan-video/wan-2.7-i2v  (padrão: aceita quadro inicial E final,
                                          o que fecha o loop de verdade, e é mais barato)
  i2v-quality  -> kwaivgi/kling-v2.6     (qualidade maior, sem quadro final)

Configuração:
  Preencha REPLICATE_API_TOKEN no arquivo .env da raiz do projeto.
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPLICATE_BASE = "https://api.replicate.com/v1"

MODELOS = {
    "i2v": "wan-video/wan-2.7-i2v",
    "i2v-fast": "wan-video/wan-2.7-i2v",
    "i2v-quality": "kwaivgi/kling-v2.6",
}

# O que evitar em toda animação de criativo (dores mapeadas com o time de criativos)
NEGATIVE_PROMPT = (
    "talking, speech, lip movement, dialogue, new objects, extra people, "
    "new text, changing text, morphing text, distorted text, camera cuts, "
    "aggressive panning, flickering"
)


def _montar_inputs(model: str, prompt: str, image_uri: str) -> dict:
    """Monta os inputs conforme o schema de cada modelo.

    Wan aceita quadro inicial e final: passamos a MESMA imagem nos dois,
    que é o que fecha o loop sem salto. Kling só aceita quadro inicial.
    """
    if "wan-video" in model:
        return {
            "prompt": prompt,
            "first_frame": image_uri,
            "last_frame": image_uri,
            "negative_prompt": NEGATIVE_PROMPT,
        }
    if "kling" in model:
        return {
            "prompt": prompt,
            "start_image": image_uri,
            "negative_prompt": NEGATIVE_PROMPT,
        }
    # Modelo desconhecido: tenta o campo generico
    return {"prompt": prompt, "image": image_uri}


def load_env_file(path: Path) -> None:
    """Carrega variáveis do .env sem sobrescrever as já definidas no ambiente."""
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
        val = rest.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def _file_to_data_uri(file_path: Path) -> str:
    """Converte a imagem local para data URI base64."""
    raw = file_path.read_bytes()
    b64 = base64.b64encode(raw).decode()
    ext = file_path.suffix.lstrip(".").lower()
    mime = {
        "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "png": "image/png", "webp": "image/webp",
    }.get(ext, "image/png")
    return f"data:{mime};base64,{b64}"


def _download_url(url: str, dest: Path) -> bool:
    """Baixa o vídeo gerado para o destino."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=300) as r:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"ERRO no download: {e}", file=sys.stderr)
        return False


def _replicate_predict(api_key: str, model: str, inputs: dict,
                       timeout_secs: int = 420) -> dict | None:
    """Cria a prediction no Replicate e aguarda o resultado (polling)."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Prefer": "wait=60",
    }
    url = f"{REPLICATE_BASE}/models/{model}/predictions"
    payload = {"input": inputs}
    use_generic = False

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        result = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=90) as resp:
                    result = json.loads(resp.read().decode())
                break
            except urllib.error.HTTPError as e:
                if e.code == 404 and not use_generic:
                    # Modelos community usam o endpoint genérico com "version"
                    use_generic = True
                    url = f"{REPLICATE_BASE}/predictions"
                    payload = {"version": model, "input": inputs}
                    data = json.dumps(payload).encode("utf-8")
                    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                    continue
                if e.code == 429 and attempt < 3:
                    retry_after = int(e.headers.get("Retry-After", "5"))
                    wait = max(retry_after, 3) * (attempt + 1)
                    print(f"Rate limit. Aguardando {wait}s (tentativa {attempt + 2}/4)...", flush=True)
                    time.sleep(wait)
                    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                    continue
                raise
        if result is None:
            print("ERRO Replicate: falhou após 4 tentativas", file=sys.stderr)
            return None

        if result.get("status") == "succeeded":
            return result

        poll_url = result.get("urls", {}).get("get", "")
        if not poll_url:
            print("ERRO Replicate: sem URL de polling", file=sys.stderr)
            return None

        elapsed = 0
        while elapsed < timeout_secs:
            time.sleep(5)
            elapsed += 5
            poll_req = urllib.request.Request(poll_url, headers={"Authorization": f"Bearer {api_key}"})
            with urllib.request.urlopen(poll_req, timeout=15) as resp:
                status = json.loads(resp.read().decode())
            state = status.get("status", "")
            if state == "succeeded":
                return status
            if state in ("failed", "canceled"):
                print(f"ERRO Replicate: {status.get('error', state)}", file=sys.stderr)
                return None

        print(f"ERRO Replicate: tempo esgotado ({timeout_secs}s)", file=sys.stderr)
        return None
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"ERRO Replicate HTTP {e.code}: {err_body[:300]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERRO Replicate: {e}", file=sys.stderr)
        return None


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Anima um criativo estático em loop (image-to-video) via Replicate."
    )
    ap.add_argument("--image", required=True,
                    help="Caminho da imagem do criativo (PNG/JPG já gerado)")
    ap.add_argument("--prompt-file", required=True,
                    help="Arquivo .txt com o prompt de animação")
    ap.add_argument("--out", required=True,
                    help="Caminho de saída do vídeo (.mp4)")
    ap.add_argument("--model", default="i2v",
                    help="Atalho (i2v, i2v-quality) ou nome completo do modelo Replicate")
    args = ap.parse_args()

    load_env_file(ROOT / ".env")
    api_key = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if not api_key:
        print("ERRO: REPLICATE_API_TOKEN não encontrado no .env da raiz do projeto.", file=sys.stderr)
        print("Preencha a chave e rode de novo.", file=sys.stderr)
        return 1

    image_path = Path(args.image)
    if not image_path.is_file():
        print(f"ERRO: imagem não encontrada: {image_path}", file=sys.stderr)
        return 1

    prompt_path = Path(args.prompt_file)
    if not prompt_path.is_file():
        print(f"ERRO: arquivo de prompt não encontrado: {prompt_path}", file=sys.stderr)
        return 1
    prompt = prompt_path.read_text(encoding="utf-8").strip()
    if not prompt:
        print("ERRO: o arquivo de prompt está vazio.", file=sys.stderr)
        return 1

    model = MODELOS.get(args.model, args.model)
    dest = Path(args.out)

    print(f"Animando {image_path.name} com {model}...", flush=True)
    result = _replicate_predict(api_key, model, _montar_inputs(model, prompt, _file_to_data_uri(image_path)))
    if not result:
        return 1

    output = result.get("output")
    video_url = output[0] if isinstance(output, list) else output
    if not (isinstance(video_url, str) and video_url.startswith("http")):
        print(f"ERRO: output inesperado do Replicate: {str(output)[:200]}", file=sys.stderr)
        return 1

    if not _download_url(video_url, dest):
        return 1

    print(f"OK: vídeo salvo em {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
