# -*- coding: utf-8 -*-
"""
Gera carrossel para Instagram com foto IA.

Pipeline por card:
  1. Gera foto via OpenRouter (Gemini Flash Image)
  2. Compõe card diretamente com Pillow (sem Chrome/HTML)
  3. Salva PNG em output_dir

Requer: pip install Pillow

Fontes: coloque Inter-Light.ttf, Inter-Bold.ttf, Inter-Black.ttf em
scripts/fonts/  (https://github.com/rsms/inter/releases)
Se não encontrado, usa fontes do sistema como fallback.

Uso (na raiz do projeto):
  py -3 scripts/gerar-carrossel-foto.py --config config.json
  py -3 scripts/gerar-carrossel-foto.py --config config.json --skip-ai
  py -3 scripts/gerar-carrossel-foto.py --config config.json --only 01,03

Schema do config.json:
{
  "slug": "slug-do-produto",
  "handle": "@seuhandle",
  "output_dir": "meus-produtos/slug/entregas/criativos/carrosseis/carrossel-01",
  "accent_dark":  "#FF6B01",
  "accent_light": "#8B5CF6",
  "cards": [
    {
      "id": "01",
      "tipo": "capa",
      "headline": "HEADLINE EM CAIXA ALTA",
      "headline_highlight": "PALAVRA",
      "subheadline": "Complemento da capa",
      "prompt_en": "..."
    },
    {
      "id": "02",
      "tipo": "conteudo",
      "tema": "escuro",
      "label": "Ponto 1",
      "titulo": "Titulo do card",
      "paragrafos": ["linha 1", "linha 2", "linha 3", "linha 4"],
      "destaques": ["trecho em destaque"],
      "prompt_en": "..."
    },
    {
      "id": "08",
      "tipo": "cta",
      "tema": "claro",
      "label": "Agora voce sabe",
      "titulo": "CTA final",
      "paragrafos": ["linha 1", "linha 2"],
      "destaques": []
    }
  ]
}
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import platform
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

ROOT = Path(__file__).resolve().parent.parent

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OR_MODEL       = "google/gemini-3.1-flash-image-preview"

PHOTO_SUFFIX = (
    ", shot on Sony A7R IV, 35mm prime lens, f/2.0 aperture, "
    "cinematic color grading, dramatic directional studio lighting, "
    "shallow depth of field, editorial photography quality, "
    "ultra realistic, hyper detailed, 8K resolution, "
    "no text, no watermark, no logo, "
    "anatomically correct, no distorted limbs, no distorted fingers"
)

# ── Dimensões ─────────────────────────────────────────────────────────
CARD_W       = 1080
CARD_H       = 1350
IMG_MARGIN_X = 90
IMG_MARGIN_Y = 60
IMG_RADIUS   = 28
PAD_X        = 90


# ── env ───────────────────────────────────────────────────────────────

def load_env(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, _, v = s.partition("=")
        k, v = k.strip(), v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        if k and k not in os.environ:
            os.environ[k] = v


# ── Fonts ─────────────────────────────────────────────────────────────

FONTS_DIR = Path(__file__).parent / "fonts"

_INTER_NAMES = {
    "light":   ["Inter-Light.ttf",   "Inter_Light.ttf",   "Inter-300.ttf",  "inter-light.ttf"],
    "regular": ["Inter-Regular.ttf", "Inter.ttf",          "Inter-400.ttf"],
    "bold":    ["Inter-Bold.ttf",    "Inter_Bold.ttf",     "Inter-700.ttf",  "inter-bold.ttf"],
    "black":   ["Inter-Black.ttf",   "Inter_Black.ttf",    "Inter-900.ttf",  "inter-black.ttf"],
}

_FALLBACK_NAMES = {
    "light":   ["segoeui.ttf",  "Helvetica.ttc", "arial.ttf",   "DejaVuSans.ttf"],
    "regular": ["segoeui.ttf",  "Helvetica.ttc", "arial.ttf",   "DejaVuSans.ttf"],
    "bold":    ["segoeuib.ttf", "arialbd.ttf",   "DejaVuSans-Bold.ttf"],
    "black":   ["ariblk.ttf",   "segoeuib.ttf",  "DejaVuSans-Bold.ttf"],
}

_SYS_FONT_DIRS = [
    Path("C:/Windows/Fonts"),
    Path.home() / "Library/Fonts",
    Path("/Library/Fonts"),
    Path("/usr/share/fonts/truetype"),
    Path("/usr/share/fonts"),
]

_font_cache: dict[tuple, "ImageFont.FreeTypeFont"] = {}


def _find_font_path(variant: str) -> str | None:
    search_dirs = [FONTS_DIR] + _SYS_FONT_DIRS
    for d in search_dirs:
        for name in _INTER_NAMES.get(variant, []):
            p = d / name
            if p.exists():
                return str(p)
    for d in search_dirs:
        for name in _FALLBACK_NAMES.get(variant, []):
            p = d / name
            if p.exists():
                return str(p)
    return None


def fnt(variant: str, size: int) -> "ImageFont.FreeTypeFont":
    key = (variant, size)
    if key in _font_cache:
        return _font_cache[key]
    path = _find_font_path(variant)
    if path:
        try:
            f = ImageFont.truetype(path, size)
            _font_cache[key] = f
            return f
        except Exception:
            pass
    f = ImageFont.load_default()
    _font_cache[key] = f
    return f


# ── API OpenRouter ────────────────────────────────────────────────────

def _post(url: str, headers: dict, payload: dict, timeout: int = 300) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        url, data=data,
        headers={**headers, "Content-Length": str(len(data))},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _save_data_url(data_url: str, dest: Path) -> None:
    m = re.match(r"data:image/[^;]+;base64,(.+)", data_url, re.DOTALL)
    if not m:
        raise ValueError("data URL inesperado")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(base64.b64decode(m.group(1)))


def _extract_img(result: dict) -> str | None:
    msg = (result.get("choices") or [{}])[0].get("message", {})
    for img in (msg.get("images") or []):
        url = (img.get("image_url") or {}).get("url") if isinstance(img, dict) else None
        if isinstance(url, str) and url.startswith("data:image"):
            return url
    content = msg.get("content")
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "image_url":
                url = (part.get("image_url") or {}).get("url", "")
                if url.startswith("data:image"):
                    return url
    if isinstance(content, str) and "data:image" in content:
        m = re.search(r"data:image/[^;]+;base64,[A-Za-z0-9+/=]+", content)
        if m:
            return m.group(0)
    return None


def gerar_foto_openrouter(api_key: str, prompt: str, dest: Path) -> bool:
    print(f"      OpenRouter ({OR_MODEL})...", flush=True)
    full_prompt = prompt.rstrip() + PHOTO_SUFFIX
    try:
        result = _post(
            OPENROUTER_URL,
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type":  "application/json",
                "HTTP-Referer":  "https://workshop.inteligente",
                "X-Title":       "Workshop Marketing IA",
            },
            {
                "model":      OR_MODEL,
                "messages":   [{"role": "user", "content": full_prompt}],
                "modalities": ["image", "text"],
            },
        )
        if result.get("error"):
            print(f"      ERRO: {str(result['error'])[:200]}", file=sys.stderr)
            return False
        url = _extract_img(result)
        if not url:
            print("      ERRO: sem imagem na resposta", file=sys.stderr)
            return False
        _save_data_url(url, dest)
        return True
    except urllib.error.HTTPError as e:
        print(f"      ERRO HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"      ERRO: {e}", file=sys.stderr)
        return False


def gerar_foto(prompt: str, dest: Path) -> bool:
    or_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not or_key:
        print("      ERRO: configure OPENROUTER_API_KEY no .env", file=sys.stderr)
        return False
    return gerar_foto_openrouter(or_key, prompt, dest)


# ── Utilitários Pillow ────────────────────────────────────────────────

def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rounded_mask(size: tuple[int, int], radius: int) -> "Image.Image":
    scale = 4
    big = Image.new("L", (size[0] * scale, size[1] * scale), 0)
    ImageDraw.Draw(big).rounded_rectangle(
        [0, 0, size[0] * scale - 1, size[1] * scale - 1],
        radius=radius * scale,
        fill=255,
    )
    return big.resize(size, Image.LANCZOS)


def fit_crop(img: "Image.Image", w: int, h: int) -> "Image.Image":
    r_src = img.width / img.height
    r_tgt = w / h
    if r_src > r_tgt:
        new_h, new_w = h, int(img.width * h / img.height)
    else:
        new_w, new_h = w, int(img.height * w / img.width)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    ox = (new_w - w) // 2
    return resized.crop((ox, 0, ox + w, h))


def gradient_overlay(width: int, height: int) -> "Image.Image":
    """Gradiente dark para a capa: transparente no topo, opaco embaixo."""
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels  = overlay.load()
    dark    = (10, 8, 28)
    stops   = [(0.0, 0), (0.30, 0), (0.50, int(0.55 * 255)), (0.75, int(0.92 * 255)), (1.0, int(0.98 * 255))]
    for y in range(height):
        t     = y / height
        alpha = 0
        for i in range(len(stops) - 1):
            t0, a0 = stops[i]
            t1, a1 = stops[i + 1]
            if t0 <= t <= t1:
                f     = (t - t0) / (t1 - t0) if t1 > t0 else 0
                alpha = int(a0 + (a1 - a0) * f)
                break
        for x in range(width):
            pixels[x, y] = (*dark, alpha)
    return overlay


def paste_rgba(canvas: "Image.Image", overlay: "Image.Image") -> "Image.Image":
    base = canvas.convert("RGBA")
    base.alpha_composite(overlay)
    return base.convert("RGB")


def mword(draw: "ImageDraw.ImageDraw", word: str, font: "ImageFont.FreeTypeFont") -> int:
    bb = draw.textbbox((0, 0), word, font=font)
    return bb[2] - bb[0]


def line_height(draw: "ImageDraw.ImageDraw", font: "ImageFont.FreeTypeFont", spacing: int = 10) -> int:
    bb = draw.textbbox((0, 0), "Ag", font=font)
    return (bb[3] - bb[1]) + spacing


def wrap_lines(draw: "ImageDraw.ImageDraw", text: str, font: "ImageFont.FreeTypeFont", max_w: int) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if mword(draw, test, font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def build_segments(text: str, highlights: list[str], color: tuple, hl_color: tuple) -> list:
    lower  = text.lower()
    spans: list[list[int]] = []
    for h in highlights:
        idx = lower.find(h.lower())
        if idx >= 0:
            spans.append([idx, idx + len(h)])
    spans.sort()
    merged: list[list[int]] = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    segs, pos = [], 0
    for s, e in merged:
        if pos < s:
            segs.append((text[pos:s], color))
        segs.append((text[s:e], hl_color))
        pos = e
    if pos < len(text):
        segs.append((text[pos:], color))
    return segs or [(text, color)]


def render_paragraph(
    draw: "ImageDraw.ImageDraw",
    text: str,
    x0: int,
    y: int,
    font_normal: "ImageFont.FreeTypeFont",
    font_hl: "ImageFont.FreeTypeFont",
    max_w: int,
    color: tuple,
    highlights: list[str],
    hl_color: tuple,
    spacing: int = 12,
) -> int:
    segs   = build_segments(text, highlights, color, hl_color)
    lh     = line_height(draw, font_normal, spacing)
    sp_w   = mword(draw, " ", font_normal)
    cx     = x0
    for si, (seg_text, seg_color) in enumerate(segs):
        seg_fnt = font_hl if seg_color == hl_color else font_normal
        words   = seg_text.split(" ")
        for wi, word in enumerate(words):
            is_last = wi == len(words) - 1
            if not word:
                if not is_last:
                    cx += sp_w
                continue
            ww = mword(draw, word, seg_fnt)
            if cx > x0 and cx + ww > x0 + max_w:
                y  += lh
                cx  = x0
            draw.text((cx, y), word, font=seg_fnt, fill=seg_color)
            cx += ww
            if not is_last:
                cx += sp_w
            elif si < len(segs) - 1:
                nxt = segs[si + 1][0]
                if not nxt.startswith((" ", ".", ",", ";", ":", "!", "?")):
                    cx += sp_w
    return y + lh


# ── Composição por tipo ────────────────────────────────────────────────

def compositar_capa(card: dict, cfg: dict, foto_path: Path | None) -> "Image.Image":
    accent    = cfg.get("accent_dark", "#FF6B01")
    handle    = cfg.get("handle", "@seuhandle")
    headline  = card.get("headline", "")
    hl_word   = card.get("headline_highlight", "")
    subhead   = card.get("subheadline", "")
    max_w     = CARD_W - 2 * PAD_X

    canvas = Image.new("RGB", (CARD_W, CARD_H), "#0d0d1a")

    if foto_path and foto_path.exists():
        foto = Image.open(foto_path).convert("RGB")
        canvas.paste(fit_crop(foto, CARD_W, CARD_H), (0, 0))

    canvas = paste_rgba(canvas, gradient_overlay(CARD_W, CARD_H))
    draw   = ImageDraw.Draw(canvas)

    f_hl  = fnt("black", 76)
    f_sub = fnt("light", 34)
    f_hdl = fnt("light", 24)
    f_arr = fnt("light", 44)

    hl_lines  = wrap_lines(draw, headline, f_hl, max_w)
    hl_lh     = line_height(draw, f_hl, 4)
    sub_lines = wrap_lines(draw, subhead, f_sub, max_w)
    sub_lh    = line_height(draw, f_sub, 8)
    divider_h = 1 + 22 + 18

    total_h   = hl_lh * len(hl_lines) + divider_h + sub_lh * len(sub_lines)
    y         = (CARD_H - 140) - total_h

    # Headline — centralizada, palavra de destaque em accent
    sp_w = mword(draw, " ", f_hl)
    for line in hl_lines:
        words  = line.split()
        line_w = sum(mword(draw, w, f_hl) for w in words) + sp_w * max(0, len(words) - 1)
        x      = (CARD_W - line_w) // 2
        for word in words:
            color = hex_rgb(accent) if word.upper() == hl_word.upper() else (255, 255, 255)
            draw.text((x, y), word, font=f_hl, fill=color)
            x += mword(draw, word, f_hl) + sp_w
        y += hl_lh

    # Linha divisória semi-transparente
    y     += 22
    div_w  = int(CARD_W * 0.7)
    dx     = (CARD_W - div_w) // 2
    # Composite via overlay RGBA
    div_layer = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    ImageDraw.Draw(div_layer).line([(dx, y), (dx + div_w, y)], fill=(255, 255, 255, int(0.35 * 255)), width=1)
    canvas = paste_rgba(canvas, div_layer)
    draw   = ImageDraw.Draw(canvas)
    y     += 18

    # Subheadline
    for line in sub_lines:
        lw = mword(draw, line, f_sub)
        draw.text(((CARD_W - lw) // 2, y), line, font=f_sub, fill=(204, 204, 204))
        y += sub_lh

    # Handle centralizado
    hw = mword(draw, handle, f_hdl)
    draw.text(((CARD_W - hw) // 2, CARD_H - 80), handle, font=f_hdl, fill=(136, 136, 136))

    # Setas ›  ›  ›
    arrows = "›  ›  ›"
    aw     = mword(draw, arrows, f_arr)
    abb    = draw.textbbox((0, 0), "›", font=f_arr)
    draw.text((CARD_W - PAD_X - aw, CARD_H - 38 - (abb[3] - abb[1])), arrows, font=f_arr, fill=(136, 136, 136))

    return canvas


def compositar_conteudo(card: dict, cfg: dict, foto_path: Path | None) -> "Image.Image":
    tema    = card.get("tema", "claro")
    is_dark = tema == "escuro"
    accent  = cfg.get("accent_dark", "#FF6B01") if is_dark else cfg.get("accent_light", "#8B5CF6")
    handle  = cfg.get("handle", "@seuhandle")

    bg            = "#1C1C2E" if is_dark else "#F4F4F2"
    body_text     = (208, 208, 208) if is_dark else (80, 80, 80)
    body_muted    = (170, 170, 170) if is_dark else (150, 150, 150)
    divider_color = (58,  58,  80)  if is_dark else (200, 200, 200)
    photo_border  = (58,  58,  80)  if is_dark else (220, 220, 220)
    accent_rgb    = hex_rgb(accent)
    max_w         = CARD_W - 2 * PAD_X

    canvas = Image.new("RGB", (CARD_W, CARD_H), bg)
    draw   = ImageDraw.Draw(canvas)

    f_lbl = fnt("bold",  26)
    f_ttl = fnt("black", 52)
    f_bdy = fnt("light", 32)
    f_hl  = fnt("bold",  32)
    f_hdl = fnt("light", 24)
    f_arr = fnt("light", 44)

    # Altura dinâmica da foto
    paragrafos = card.get("paragrafos", [])
    n_linhas   = sum(len(p) // 40 + 1 for p in paragrafos)
    photo_h    = max(360, min(520, 560 - n_linhas * 22))

    img_x = IMG_MARGIN_X
    img_y = IMG_MARGIN_Y
    img_w = CARD_W - 2 * IMG_MARGIN_X

    if foto_path and foto_path.exists():
        foto    = Image.open(foto_path).convert("RGB")
        cropped = fit_crop(foto, img_w, photo_h)
    else:
        cropped = Image.new("RGB", (img_w, photo_h), "#2A2A40" if is_dark else "#DDDDDD")

    mask = rounded_mask((img_w, photo_h), IMG_RADIUS)
    canvas.paste(cropped, (img_x, img_y), mask)
    draw.rounded_rectangle(
        [img_x, img_y, img_x + img_w - 1, img_y + photo_h - 1],
        radius=IMG_RADIUS, outline=photo_border, width=3,
    )
    draw = ImageDraw.Draw(canvas)

    y = img_y + photo_h + 24

    # Label
    draw.text((PAD_X, y), card.get("label", ""), font=f_lbl, fill=body_muted)
    lbb = draw.textbbox((0, 0), "Ag", font=f_lbl)
    y  += (lbb[3] - lbb[1]) + 8

    # Título
    titulo     = card.get("titulo", "")
    ttl_lines  = wrap_lines(draw, titulo, f_ttl, max_w)
    ttl_lh     = line_height(draw, f_ttl, 4)
    for line in ttl_lines:
        draw.text((PAD_X, y), line, font=f_ttl, fill=accent_rgb)
        y += ttl_lh
    y += 10

    # Divisória
    draw.line([(PAD_X, y), (CARD_W - PAD_X, y)], fill=divider_color, width=2)
    y += 22

    # Parágrafos
    destaques = card.get("destaques", [])
    for para in paragrafos:
        y = render_paragraph(draw, para, PAD_X, y, f_bdy, f_hl, max_w, body_text, destaques, accent_rgb, spacing=12)
        y += 14

    # Handle
    hw = mword(draw, handle, f_hdl)
    draw.text(((CARD_W - hw) // 2, CARD_H - 80), handle, font=f_hdl, fill=(150, 150, 150))

    # Setas
    arrows = "›  ›  ›"
    aw     = mword(draw, arrows, f_arr)
    abb    = draw.textbbox((0, 0), "›", font=f_arr)
    draw.text((CARD_W - PAD_X - aw, CARD_H - 38 - (abb[3] - abb[1])), arrows, font=f_arr, fill=(150, 150, 150))

    return canvas


def compositar_cta(card: dict, cfg: dict) -> "Image.Image":
    tema    = card.get("tema", "claro")
    is_dark = tema == "escuro"
    accent  = cfg.get("accent_dark", "#FF6B01") if is_dark else cfg.get("accent_light", "#8B5CF6")
    handle  = cfg.get("handle", "@seuhandle")

    bg            = "#1C1C2E" if is_dark else "#F4F4F2"
    body_text     = (208, 208, 208) if is_dark else (80, 80, 80)
    body_muted    = (170, 170, 170) if is_dark else (150, 150, 150)
    divider_color = (58,  58,  80)  if is_dark else (200, 200, 200)
    accent_rgb    = hex_rgb(accent)
    max_w         = CARD_W - 2 * PAD_X

    canvas = Image.new("RGB", (CARD_W, CARD_H), bg)
    draw   = ImageDraw.Draw(canvas)

    f_lbl = fnt("bold",  26)
    f_ttl = fnt("black", 52)
    f_bdy = fnt("light", 32)
    f_hl  = fnt("bold",  32)
    f_hdl = fnt("light", 24)

    paragrafos = card.get("paragrafos", [])
    destaques  = card.get("destaques", [])
    titulo     = card.get("titulo", "")
    label      = card.get("label", "")

    # Calcular altura total para centralizar verticalmente
    lbb    = draw.textbbox((0, 0), "Ag", font=f_lbl)
    lbl_h  = (lbb[3] - lbb[1]) + 12

    ttl_lines = wrap_lines(draw, titulo, f_ttl, max_w)
    ttl_lh    = line_height(draw, f_ttl, 4)
    ttl_h     = ttl_lh * len(ttl_lines) + 14

    div_h  = 2 + 24
    bdy_lh = line_height(draw, f_bdy, 12)
    bdy_h  = sum(bdy_lh * max(1, len(p) // 40 + 1) + 14 for p in paragrafos)

    total_h  = lbl_h + ttl_h + div_h + bdy_h
    avail    = CARD_H - 80 - 160
    y        = 80 + max(0, (avail - total_h) // 2)

    # Label
    draw.text((PAD_X, y), label, font=f_lbl, fill=body_muted)
    y += lbl_h

    # Título
    for line in ttl_lines:
        draw.text((PAD_X, y), line, font=f_ttl, fill=accent_rgb)
        y += ttl_lh
    y += 14

    # Divisória
    draw.line([(PAD_X, y), (CARD_W - PAD_X, y)], fill=divider_color, width=2)
    y += 24

    # Parágrafos
    for para in paragrafos:
        y = render_paragraph(draw, para, PAD_X, y, f_bdy, f_hl, max_w, body_text, destaques, accent_rgb, spacing=12)
        y += 14

    # Handle (sem setas no CTA)
    hw = mword(draw, handle, f_hdl)
    draw.text(((CARD_W - hw) // 2, CARD_H - 80), handle, font=f_hdl, fill=(150, 150, 150))

    return canvas


def compositar_card(card: dict, cfg: dict, foto_path: Path | None) -> "Image.Image":
    tipo = card.get("tipo", "conteudo")
    if tipo == "capa":
        return compositar_capa(card, cfg, foto_path)
    if tipo == "cta":
        return compositar_cta(card, cfg)
    return compositar_conteudo(card, cfg, foto_path)


# ── pipeline por card ─────────────────────────────────────────────────

def processar_card(card: dict, cfg: dict, out_dir: Path, skip_ai: bool) -> bool:
    card_id  = card["id"]
    tipo     = card["tipo"]
    tem_foto = tipo in ("capa", "conteudo")
    print(f"\nCARD {card_id} — {card.get('label', tipo).upper()}", flush=True)

    foto_path = out_dir / f"_foto-{card_id}.png"
    if tem_foto and not skip_ai:
        prompt = card.get("prompt_en", "")
        if not prompt:
            print("      Sem prompt_en — pulando foto.", flush=True)
            foto_path = None
        else:
            ok = gerar_foto(prompt, foto_path)
            if not ok:
                foto_path = None
    elif not tem_foto:
        foto_path = None
    else:
        foto_path = foto_path if foto_path.exists() else None

    print("      Compondo card...", flush=True)
    try:
        img = compositar_card(card, cfg, foto_path)
    except Exception as e:
        print(f"      ERRO na composição: {e}", file=sys.stderr)
        return False

    label_slug = card.get("label", tipo).lower().replace(" ", "-").replace("/", "-")
    out_png    = out_dir / f"card-{card_id}-{label_slug}.png"
    img.save(str(out_png), "PNG")
    print(f"      Salvo: {out_png.name}", flush=True)
    return True


# ── main ──────────────────────────────────────────────────────────────

def main() -> None:
    if not HAS_PIL:
        sys.exit("ERRO: instale Pillow primeiro — pip install Pillow")

    load_env(ROOT / ".env")

    ap = argparse.ArgumentParser(description="Gera carrossel Instagram com foto IA.")
    ap.add_argument("--config",  required=True, help="Caminho para o config.json")
    ap.add_argument("--skip-ai", action="store_true", help="Pular geração de foto (usa existentes)")
    ap.add_argument("--only",    help="IDs de cards separados por vírgula (ex: 01,03)")
    args = ap.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.is_absolute():
        cfg_path = ROOT / cfg_path
    if not cfg_path.exists():
        sys.exit(f"ERRO: config não encontrado: {cfg_path}")

    cfg     = json.loads(cfg_path.read_text(encoding="utf-8"))
    out_dir = Path(cfg.get("output_dir", f"meus-produtos/{cfg.get('slug','produto')}/entregas/criativos/carrosseis/carrossel-01"))
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    only_ids = set(args.only.split(",")) if args.only else None
    cards    = cfg.get("cards", [])

    print(f"\n=== Carrossel — {cfg.get('slug', 'produto')} ({len(cards)} cards) ===")
    print(f"Saída: {out_dir}\n")

    ok_count = 0
    for card in cards:
        if only_ids and card["id"] not in only_ids:
            continue
        ok = processar_card(card, cfg, out_dir, args.skip_ai)
        if ok:
            ok_count += 1

    print(f"\nConcluído: {ok_count}/{len(cards)} cards gerados.")
    print(f"Pasta: {out_dir}")


if __name__ == "__main__":
    main()
