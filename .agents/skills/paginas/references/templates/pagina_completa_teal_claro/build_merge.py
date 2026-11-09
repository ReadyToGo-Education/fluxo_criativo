# -*- coding: utf-8 -*-
"""Regenera code.html a partir dos templates *_teal_claro. Uso: py -3 build_merge.py"""
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


def strip_body_scripts(html: str) -> str:
    return re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE).strip()


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
    return "\n".join(out)


def prefix_class_css(css: str, class_name: str, scope: str) -> str:
    """Prefixa regras que começam com .class_name (ex.: .cta-button) para evitar colisão entre blocos."""
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


def sanitize_depoimentos_css(css: str) -> str:
    """Remove reset de body/header do template isolado e evita segundo <main> no CSS."""
    css = re.sub(r"\n\s*body\s*\{[^}]*\}", "", css, flags=re.DOTALL)
    css = re.sub(r"\n\s*header\s*\{[^}]*\}", "", css, flags=re.DOTALL)
    css = re.sub(r"\n\s*\.logo\s*\{[^}]*\}", "", css, flags=re.DOTALL)
    css = re.sub(r"\n\s*\.logo span\s*\{[^}]*\}", "", css, flags=re.DOTALL)
    css = re.sub(r"\n\s*::selection\s*\{[^}]*\}", "", css, flags=re.DOTALL)
    css = css.replace("main {", ".depoimentos-wrap .depoimentos-inner {")
    return css


TOGGLE_FAQ_JS = """
function toggleFaq(btn) {
  const item = btn.closest('.faq-item');
  const wasOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));
  if (!wasOpen) item.classList.add('open');
}
"""


def main():
    hero_path = BASE / "hero_teal_claro" / "code.html"
    hero_html_raw = extract_body(hero_path)
    hero_css = extract_style(hero_path)
    hero_css = prefix_class_css(hero_css, ".cta-button", ".tpl-hero-teal")

    blocks = [
        ("dor", BASE / "dor_teal_claro" / "code.html", ".pain-section"),
        ("paliativo", BASE / "paliativo_teal_claro" / "code.html", ".section-paliativo"),
        ("provas", BASE / "provas_sociais_teal_claro" / "code.html", ".section-provas"),
        ("cta", BASE / "cta_teal_claro" / "code.html", ".cta-section"),
        ("metodo", BASE / "metodo_teal_claro" / "code.html", ".metodo-section"),
        ("para_quem", BASE / "para_quem_teal_claro" / "code.html", ".section-paraquem"),
        ("entregaveis", BASE / "entregaveis_teal_claro" / "code.html", ".section-entregaveis"),
        ("bonus", BASE / "bonus_teal_claro" / "code.html", ".section-bonus"),
        ("stack", BASE / "stack_valor_teal_claro" / "code.html", ".section-stack"),
        ("suporte", BASE / "suporte_teal_claro" / "code.html", ".section-suporte"),
        ("garantia", BASE / "garantia_teal_claro" / "code.html", ".section-garantia"),
        ("autoridade", BASE / "autoridade_teal_claro" / "code.html", ".section-autoridade"),
        ("faq", BASE / "faq_teal_claro" / "code.html", ".faq-section"),
        ("oferta", BASE / "oferta_final_teal_claro" / "code.html", ".section-oferta"),
    ]

    dep_path = BASE / "hero_teal_claro_depoimentos" / "code.html"
    dep_body = extract_body(dep_path)
    dep_main_m = re.search(r"(<main>.*?</main>)", dep_body, re.DOTALL | re.IGNORECASE)
    dep_main = dep_main_m.group(1) if dep_main_m else ""
    dep_main = dep_main.replace("<main>", '<div class="depoimentos-inner">', 1).replace("</main>", "</div>", 1)
    dep_script_m = re.search(r"<script>(.*?)</script>", dep_body, re.DOTALL | re.IGNORECASE)
    dep_script = dep_script_m.group(1).strip() if dep_script_m else ""
    dep_css = sanitize_depoimentos_css(scope_shimmer(extract_style(dep_path), ".depoimentos-wrap"))

    css_chunks = ["/* === hero_teal_claro === */", hero_css]
    for name, path, scope in blocks:
        css = extract_style(path)
        css = scope_shimmer(css, scope)
        if name == "stack":
            css = scope_stack_valor(css)
        if name == "cta":
            css = prefix_class_css(css, ".cta-btn", ".tpl-cta-teal")
        css_chunks.append(f"/* === {name} === */")
        css_chunks.append(css)

    css_chunks.append("/* === hero_teal_claro_depoimentos === */")
    css_chunks.append(dep_css)

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
        "depoimentos",
        "suporte",
        "garantia",
        "autoridade",
        "faq",
        "oferta",
    ]

    hero_inner = strip_body_scripts(hero_html_raw)
    hero_inner = hero_inner.replace(
        '<button class="cta-button">',
        '<button type="button" class="cta-button" onclick="document.getElementById(\'oferta\').scrollIntoView({behavior:\'smooth\'})">',
        1,
    )
    hero_html = '<div class="tpl-hero-teal">\n' + hero_inner + "\n</div>"

    by_name: dict[str, str] = {"hero": hero_html}
    for name, path, _scope in blocks:
        b = strip_body_scripts(extract_body(path))
        if name == "oferta":
            b = b.replace(
                '<section class="section-oferta">',
                '<section id="oferta" class="section-oferta">',
                1,
            )
        if name == "cta":
            b = b.replace(
                '<section class="cta-section">',
                '<section class="cta-section tpl-cta-teal">',
                1,
            )
        by_name[name] = b

    by_name["depoimentos"] = f'<div class="depoimentos-wrap">\n{dep_main}\n</div>'

    final_body = "\n\n".join(by_name[n] for n in order_names)

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
  document.querySelectorAll('.fadeUp').forEach((el) => fadeUpObs.observe(el));
}});
{TOGGLE_FAQ_JS}

{dep_script}
</script>
"""

    fonts_head = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">"""

    html_out = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nome do Produto. Transformação Principal</title>
  <meta name="description" content="Descrição de até 160 caracteres com a promessa principal do produto.">
{fonts_head}
  <style>
{merged_css}
  </style>
</head>
<body>

{final_body}

  <footer style="padding:40px 24px; text-align:center; border-top:1px solid #EAEAEA; background:#F8F8F8;">
    <p style="font-size:0.85rem; color:#666;">SuaMarca &copy; 2026. Todos os direitos reservados.</p>
    <p style="font-size:0.75rem; color:#888; margin-top:8px;"><a href="#" style="color:#666; text-decoration:underline;">Termos de uso</a> &middot; <a href="#" style="color:#666; text-decoration:underline;">Política de privacidade</a></p>
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
