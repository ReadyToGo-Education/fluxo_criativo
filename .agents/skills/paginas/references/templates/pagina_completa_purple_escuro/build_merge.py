# -*- coding: utf-8 -*-
"""Regenera code.html a partir dos templates *_purple_escuro. Uso: py -3 build_merge.py"""
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
    return m.group(1).strip() if m else 'class="text-ink font-sans antialiased min-h-screen"'


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


def prefix_cta_button_css(css: str, scope: str) -> str:
    """Evita que .cta-button do hero sobrescreva CTA e oferta (e vice-versa)."""
    lines = []
    for line in css.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(".cta-button"):
            if scope not in stripped[: len(scope) + 5]:
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


TOGGLE_FAQ_JS = """
function toggleFaq(btn) {
  const item = btn.closest('.faq-item');
  const wasOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));
  if (!wasOpen) item.classList.add('open');
}
"""


def main():
    hero_path = BASE / "hero_purple_escuro" / "code.html"
    hero_html_raw = extract_body(hero_path)
    hero_css = extract_style(hero_path)
    hero_css = prefix_cta_button_css(hero_css, ".tpl-hero-purple")

    body_classes = extract_body_opening_classes(hero_path)

    blocks = [
        ("dor", BASE / "dor_purple_escuro" / "code.html", ".section-dor"),
        ("paliativo", BASE / "paliativo_purple_escuro" / "code.html", ".paliativo-section"),
        ("provas", BASE / "provas_sociais_purple_escuro" / "code.html", ".provas-section"),
        ("cta", BASE / "cta_purple_escuro" / "code.html", ".cta-section"),
        ("metodo", BASE / "metodo_purple_escuro" / "code.html", ".metodo-section"),
        ("para_quem", BASE / "para_quem_purple_escuro" / "code.html", ".paraquem-section"),
        ("entregaveis", BASE / "entregaveis_purple_escuro" / "code.html", ".entregaveis-section"),
        ("bonus", BASE / "bonus_purple_escuro" / "code.html", ".bonus-section"),
        ("stack", BASE / "stack_valor_purple_escuro" / "code.html", ".stack-section"),
        ("suporte", BASE / "suporte_purple_escuro" / "code.html", ".suporte-section"),
        ("garantia", BASE / "garantia_purple_escuro" / "code.html", ".garantia-section"),
        ("autoridade", BASE / "autoridade_purple_escuro" / "code.html", ".autoridade-section"),
        ("faq", BASE / "faq_purple_escuro" / "code.html", ".faq-section"),
        ("oferta", BASE / "oferta_final_purple_escuro" / "code.html", ".oferta-section"),
    ]

    dep_path = BASE / "hero_purple_escuro_depoimentos" / "code.html"
    dep_body = extract_body(dep_path)
    dep_main_m = re.search(r"(<main>.*?</main>)", dep_body, re.DOTALL | re.IGNORECASE)
    dep_main = dep_main_m.group(1) if dep_main_m else ""
    dep_script_m = re.search(r"<script>(.*?)</script>", dep_body, re.DOTALL | re.IGNORECASE)
    dep_script = dep_script_m.group(1).strip() if dep_script_m else ""
    dep_css = scope_shimmer(extract_style(dep_path), ".depoimentos-wrap")

    css_chunks = ["/* === hero_purple_escuro === */", hero_css]
    for name, path, scope in blocks:
        css = extract_style(path)
        css = scope_shimmer(css, scope)
        if name == "stack":
            css = scope_stack_valor(css)
        if name == "cta":
            css = prefix_cta_button_css(css, ".cta-section-purple")
        if name == "oferta":
            css = prefix_cta_button_css(css, "#oferta")
        css_chunks.append(f"/* === {name} === */")
        css_chunks.append(css)

    css_chunks.append("/* === hero_purple_escuro_depoimentos === */")
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

    hero_btn_re = re.compile(
        r'<button class="flat-border bg-warm text-white w-fit px-8 py-4 uppercase tracking-widest text-sm font-bold cta-button flex items-center gap-3">'
    )
    hero_btn_fixed = (
        '<button type="button" class="flat-border bg-warm text-white w-fit px-8 py-4 uppercase '
        'tracking-widest text-sm font-bold cta-button flex items-center gap-3" '
        'onclick="document.getElementById(\'oferta\').scrollIntoView({behavior:\'smooth\'})">'
    )
    hero_inner = hero_btn_re.sub(hero_btn_fixed, hero_html_raw, count=1)

    hero_html = '<div class="tpl-hero-purple">\n' + hero_inner + "\n</div>"

    by_name: dict[str, str] = {"hero": hero_html}
    for name, path, _scope in blocks:
        b = strip_body_scripts(extract_body(path))
        if name == "oferta":
            b = b.replace(
                '<section class="gradient-bg py-20 px-4 sm:px-6 lg:px-8">',
                '<section id="oferta" class="gradient-bg py-20 px-4 sm:px-6 lg:px-8">',
                1,
            )
        if name == "cta":
            b = b.replace(
                '<section class="py-28',
                '<section class="cta-section-purple py-28',
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
  document.querySelectorAll('.fade-up').forEach((el) => fadeUpObs.observe(el));
}});
{TOGGLE_FAQ_JS}

{dep_script}
</script>
"""

    tailwind_head = """  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            base: "#0a0a0f",
            surface: "#12121a",
            ink: "#f0f0f5",
            accent: "#2a2a3a",
            warm: "#6c5ce7"
          },
          fontFamily: {
            sans: ['Inter', 'sans-serif'],
          }
        }
      }
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

  <footer class="border-t border-accent/60 bg-base/80 py-10 px-6 text-center">
    <p class="text-sm text-ink/40">SuaMarca &copy; 2026. Todos os direitos reservados.</p>
    <p class="text-xs text-ink/30 mt-2">
      <a href="#" class="underline hover:text-ink/50">Termos de uso</a>
      <span class="mx-2">&middot;</span>
      <a href="#" class="underline hover:text-ink/50">Política de privacidade</a>
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
