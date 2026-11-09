# -*- coding: utf-8 -*-
"""Regenera code.html a partir dos templates *_minimal_claro. Uso: py -3 build_merge.py"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def extract_style(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", t, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def extract_body(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    m = re.search(r"<body[^>]*>(.*?)</body>", t, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def extract_body_opening_classes(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    m = re.search(r"<body([^>]*)>", t, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def strip_body_scripts(html: str) -> str:
    return re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE).strip()


def unwrap_main_to_div(html: str, class_attr: str) -> str:
    """Evita vários <main> na página completa: um único landmark fica no documento."""
    open_re = re.compile(rf"<main\s+class=(['\"]){re.escape(class_attr)}\1\s*>", re.IGNORECASE)
    m = open_re.search(html)
    if not m:
        return html
    html = open_re.sub(f'<div class="{class_attr}">', html, count=1)
    return re.sub(r"</main>", "</div>", html, count=1)


def scope_shimmer(css: str, scope_selector: str) -> str:
    lines = css.splitlines()
    out = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(".shimmer-line"):
            indent = line[: len(line) - len(stripped)]
            rest = stripped[len(".shimmer-line") :]
            line = f"{indent}{scope_selector} .shimmer-line{rest}"
        out.append(line)
    return "\n".join(lines)


def prefix_class_css(css: str, class_name: str, scope: str) -> str:
    lines = []
    for line in css.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(class_name):
            if scope not in stripped[: len(scope) + 2]:
                indent = line[: len(line) - len(stripped)]
                line = indent + scope + " " + stripped
        lines.append(line)
    return "\n".join(lines)


def scope_stack_valor(css: str) -> str:
    prefixes = (
        ".stack-label",
        ".stack-list",
        ".stack-item",
        ".stack-total",
        ".stack-total-label",
        ".stack-total-value",
        ".stack-footer",
    )
    lines = []
    for line in css.splitlines():
        stripped = line.lstrip()
        for p in prefixes:
            if stripped.startswith(p) and ".stack-card" not in stripped:
                indent = line[: len(line) - len(stripped)]
                line = indent + ".stack-card " + stripped
                break
        lines.append(line)
    return "\n".join(lines)


def scope_price_under_stack(css: str) -> str:
    lines = []
    for line in css.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(".price-old") and ".stack-card" not in stripped:
            indent = line[: len(line) - len(stripped)]
            line = indent + ".stack-card " + stripped
        lines.append(line)
    return "\n".join(lines)


def scope_oferta_minimal(css: str) -> str:
    prefixes = (
        ".stack-total-real-value",
        ".stack-total-real-label",
        ".stack-total-real",
        ".stack-check-wrap",
        ".stack-row-left",
        ".stack-row--last",
        ".stack-row",
        ".stack-price",
        ".oferta-inclui-label",
        ".price-old",
        ".oferta-trust-line",
    )
    lines = []
    for line in css.splitlines():
        stripped = line.lstrip()
        for p in prefixes:
            if stripped.startswith(p) and ".oferta-card" not in stripped:
                indent = line[: len(line) - len(stripped)]
                line = indent + ".oferta-card " + stripped
                break
        lines.append(line)
    return "\n".join(lines)


TOGGLE_FAQ_JS = """
function toggleFaq(btn) {
  const item = btn.closest('.faq-item');
  const wasOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));
  if (!wasOpen) item.classList.add('open');
}
"""


def main():
    hero_path = BASE / "hero_minimal_claro" / "code.html"
    hero_html_raw = extract_body(hero_path)
    hero_css = extract_style(hero_path)
    hero_css = prefix_class_css(hero_css, ".flat-button", ".tpl-hero-minimal")

    body_classes = extract_body_opening_classes(hero_path)

    def sc(css: str, sel: str) -> str:
        return scope_shimmer(css, sel)

    blocks = [
        ("dor", BASE / "dor_minimal_claro" / "code.html", "tpl-minimal-dor"),
        ("paliativo", BASE / "paliativo_minimal_claro" / "code.html", "tpl-minimal-paliativo"),
        ("provas", BASE / "provas_sociais_minimal_claro" / "code.html", "tpl-minimal-provas"),
        ("cta", BASE / "cta_minimal_claro" / "code.html", None),
        ("metodo", BASE / "metodo_minimal_claro" / "code.html", "tpl-minimal-metodo"),
        ("para_quem", BASE / "para_quem_minimal_claro" / "code.html", "tpl-minimal-paraquem"),
        ("entregaveis", BASE / "entregaveis_minimal_claro" / "code.html", "tpl-minimal-entregaveis"),
        ("bonus", BASE / "bonus_minimal_claro" / "code.html", "tpl-minimal-bonus"),
        ("stack", BASE / "stack_valor_minimal_claro" / "code.html", "tpl-minimal-stack"),
        ("suporte", BASE / "suporte_minimal_claro" / "code.html", "tpl-minimal-suporte"),
        ("garantia", BASE / "garantia_minimal_claro" / "code.html", "tpl-minimal-garantia"),
        ("autoridade", BASE / "autoridade_minimal_claro" / "code.html", "tpl-minimal-autoridade"),
        ("faq", BASE / "faq_minimal_claro" / "code.html", "tpl-minimal-faq"),
        ("oferta", BASE / "oferta_final_minimal_claro" / "code.html", "tpl-minimal-oferta"),
    ]

    page_top_css = """
/* Barra de progresso + landmark único na página completa */
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 2px;
  width: 0%;
  z-index: 300;
  background: linear-gradient(90deg, #18181b, #52525b);
  pointer-events: none;
  transition: width 0.12s ease-out;
}
"""
    css_chunks = ["/* === page_chrome === */", page_top_css.strip(), "/* === hero_minimal_claro === */", hero_css]
    for name, path, wrap_class in blocks:
        scope = ".tpl-cta-minimal" if name == "cta" else (f".{wrap_class}" if wrap_class else "")
        css = extract_style(path)
        if name == "dor":
            css = prefix_class_css(css, ".flat-button", ".tpl-minimal-dor")
        css = sc(css, scope)
        if name == "stack":
            css = scope_stack_valor(css)
            css = scope_price_under_stack(css)
        if name == "cta":
            css = prefix_class_css(css, ".cta-button", ".tpl-cta-minimal")
        if name == "oferta":
            css = scope_oferta_minimal(css)
            css = prefix_class_css(css, ".cta-btn", "#oferta")
        css_chunks.append(f"/* === {name} === */")
        css_chunks.append(css)

    merged_css = "\n\n".join(css_chunks)

    order_names = [
        "hero",
        "dor",
        "paliativo",
        "provas",
        "cta",
        "metodo",
        "para_quem",
        "entregaveis",
        "bonus",
        "stack",
        "provas2",
        "suporte",
        "garantia",
        "autoridade",
        "faq",
        "oferta",
    ]

    provas_path = BASE / "provas_sociais_minimal_claro" / "code.html"
    provas_body = strip_body_scripts(extract_body(provas_path))
    provas_body = f'<div class="tpl-minimal-provas">\n{provas_body}\n</div>'

    hero_btn_re = re.compile(
        r'<button class="flat-border bg-ink text-base w-full sm:w-fit px-8 py-4 uppercase tracking-widest text-sm font-medium flat-button inline-flex items-center justify-center gap-3 hero-cta-below-video mx-auto">'
    )
    hero_btn_fixed = (
        '<button type="button" class="flat-border bg-ink text-base w-full sm:w-fit px-8 py-4 uppercase '
        'tracking-widest text-sm font-medium flat-button inline-flex items-center justify-center gap-3 hero-cta-below-video mx-auto" '
        'onclick="document.getElementById(\'oferta\').scrollIntoView({behavior:\'smooth\'})">'
    )
    hero_inner = hero_btn_re.sub(hero_btn_fixed, hero_html_raw, count=1)
    hero_inner = strip_body_scripts(hero_inner)
    hero_html = '<div class="tpl-hero-minimal">\n' + hero_inner + "\n</div>"

    by_name: dict[str, str] = {"hero": hero_html, "provas2": provas_body}
    for name, path, wrap_class in blocks:
        b = strip_body_scripts(extract_body(path))
        if name == "dor":
            b = unwrap_main_to_div(b, "max-w-7xl mx-auto px-6 py-16 md:py-24")
        if name == "faq":
            b = unwrap_main_to_div(b, "max-w-3xl mx-auto px-6 py-16 md:py-24")
        if name == "cta":
            b = b.replace(
                '<section class="py-24 px-6 md:py-32 bg-canvas">',
                '<section class="py-24 px-6 md:py-32 bg-canvas tpl-cta-minimal">',
                1,
            )
        if name == "oferta":
            b = re.sub(
                r'<section class="w-full px-6 py-20 md:py-28">',
                '<section id="oferta" class="w-full px-6 py-20 md:py-28">',
                b,
                count=1,
            )
            b = b.replace(
                '<div class="fade-up oferta-card-shell rounded-xl border border-zinc-200 bg-canvas p-8 md:p-10 shadow-sm">',
                '<div class="oferta-card fade-up oferta-card-shell rounded-xl border border-zinc-200 bg-canvas p-8 md:p-10 shadow-sm">',
                1,
            )
        if wrap_class and name != "cta":
            b = f'<div class="{wrap_class}">\n{b}\n</div>'
        by_name[name] = b

    final_body = "\n\n".join(by_name[n] for n in order_names)
    final_body = (
        '<main id="conteudo-principal">\n'
        + '<div id="scroll-progress" class="scroll-progress" aria-hidden="true"></div>\n'
        + final_body
        + "\n</main>"
    )

    unified_script = f"""
<script>
document.addEventListener('DOMContentLoaded', () => {{
  const fadeUpObs = new IntersectionObserver(
    (entries) => {{
      entries.forEach((entry) => {{
        if (entry.isIntersecting) entry.target.classList.add('visible');
      }});
    }},
    {{ threshold: 0.12, rootMargin: '0px 0px -40px 0px' }}
  );
  document.querySelectorAll('.fade-up').forEach((el) => fadeUpObs.observe(el));

  const bar = document.getElementById('scroll-progress');
  const onScroll = () => {{
    const el = document.documentElement;
    const max = el.scrollHeight - el.clientHeight;
    const p = max > 0 ? (el.scrollTop / max) * 100 : 0;
    if (bar) bar.style.width = Math.min(100, Math.max(0, p)) + '%';
  }};
  onScroll();
  window.addEventListener('scroll', onScroll, {{ passive: true }});
}});
{TOGGLE_FAQ_JS}
</script>
"""

    tailwind_head = """  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,300,0,0" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: { sans: ['Inter', 'sans-serif'] },
          colors: {
            canvas: '#ffffff',
            surface: '#f4f4f5',
            ink: '#18181b',
            accent: '#e4e4e7',
          },
        },
      },
    }
  </script>"""

    html_out = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nome do Produto. Transformação Principal</title>
  <meta name="description" content="Descrição de até 160 caracteres com a promessa principal do produto.">
{tailwind_head}
  <style>
{merged_css}
  </style>
</head>
<body {body_classes}>

{final_body}

  <footer class="border-t border-ink/10 py-10 px-6 text-center bg-base">
    <p class="text-sm text-gray-500">SuaMarca &copy; 2026. Todos os direitos reservados.</p>
    <p class="text-xs text-gray-400 mt-2">
      <a href="#" class="underline hover:text-ink/70">Termos de uso</a>
      <span class="mx-2">&middot;</span>
      <a href="#" class="underline hover:text-ink/70">Política de privacidade</a>
    </p>
  </footer>

{unified_script}

</body>
</html>
"""

    out = Path(__file__).resolve().parent / "code.html"
    out.write_text(html_out, encoding="utf-8")
    print("Wrote", out, "chars", len(html_out))


if __name__ == "__main__":
    main()
