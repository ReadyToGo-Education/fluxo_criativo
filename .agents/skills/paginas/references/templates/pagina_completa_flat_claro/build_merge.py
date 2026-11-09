# -*- coding: utf-8 -*-
"""Regenera code.html a partir dos templates *_flat_claro. Uso: py -3 build_merge.py"""
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


def scope_oferta_flat(css: str) -> str:
    prefixes = (
        ".stack-label",
        ".stack-list",
        ".stack-item",
        ".stack-item-name",
        ".stack-item-value",
        ".stack-total",
        ".stack-total-label",
        ".stack-total-value",
        ".valor-total",
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
    hero_path = BASE / "hero_flat_claro" / "code.html"
    hero_html_raw = extract_body(hero_path)
    hero_css = extract_style(hero_path)
    hero_css = prefix_class_css(hero_css, ".cta-button", ".tpl-hero-flat")

    body_classes = extract_body_opening_classes(hero_path)

    # Wrapper por bloco: ancora real para scope_shimmer (.shimmer-line) no merge
    def sc(css: str, sel: str) -> str:
        return scope_shimmer(css, sel)

    blocks = [
        ("dor", BASE / "dor_flat_claro" / "code.html", "tpl-flat-dor"),
        ("paliativo", BASE / "paliativo_flat_claro" / "code.html", "tpl-flat-paliativo"),
        ("provas", BASE / "provas_sociais_flat_claro" / "code.html", "tpl-flat-provas"),
        ("cta", BASE / "cta_flat_claro" / "code.html", None),
        ("metodo", BASE / "metodo_flat_claro" / "code.html", "tpl-flat-metodo"),
        ("para_quem", BASE / "para_quem_flat_claro" / "code.html", "tpl-flat-paraquem"),
        ("entregaveis", BASE / "entregaveis_flat_claro" / "code.html", "tpl-flat-entregaveis"),
        ("bonus", BASE / "bonus_flat_claro" / "code.html", "tpl-flat-bonus"),
        ("stack", BASE / "stack_valor_flat_claro" / "code.html", "tpl-flat-stack"),
        ("suporte", BASE / "suporte_flat_claro" / "code.html", "tpl-flat-suporte"),
        ("garantia", BASE / "garantia_flat_claro" / "code.html", "tpl-flat-garantia"),
        ("autoridade", BASE / "autoridade_flat_claro" / "code.html", "tpl-flat-autoridade"),
        ("faq", BASE / "faq_flat_claro" / "code.html", "tpl-flat-faq"),
        ("oferta", BASE / "oferta_final_flat_claro" / "code.html", "tpl-flat-oferta"),
    ]

    css_chunks = ["/* === hero_flat_claro === */", hero_css]
    for name, path, wrap_class in blocks:
        scope = ".tpl-cta-flat" if name == "cta" else (f".{wrap_class}" if wrap_class else "")
        css = extract_style(path)
        css = sc(css, scope)
        if name == "stack":
            css = scope_stack_valor(css)
        if name == "cta":
            css = prefix_class_css(css, ".cta-btn", ".tpl-cta-flat")
        if name == "oferta":
            css = scope_oferta_flat(css)
            css = prefix_class_css(css, ".cta-btn", "#oferta")
        css_chunks.append(f"/* === {name} === */")
        css_chunks.append(css)

    merged_css = "\n\n".join(css_chunks)

    # Ordem: provas sociais aparece duas vezes (como na página completa manual)
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

    provas_path = BASE / "provas_sociais_flat_claro" / "code.html"
    provas_body = strip_body_scripts(extract_body(provas_path))
    provas_body = f'<div class="tpl-flat-provas">\n{provas_body}\n</div>'

    hero_btn_re = re.compile(
        r'<button class="flat-border bg-ink text-white w-fit px-8 py-4 uppercase tracking-widest text-sm font-bold cta-button flex items-center gap-3">'
    )
    hero_btn_fixed = (
        '<button type="button" class="flat-border bg-ink text-white w-fit px-8 py-4 uppercase '
        'tracking-widest text-sm font-bold cta-button flex items-center gap-3" '
        'onclick="document.getElementById(\'oferta\').scrollIntoView({behavior:\'smooth\'})">'
    )
    hero_inner = hero_btn_re.sub(hero_btn_fixed, hero_html_raw, count=1)
    hero_inner = strip_body_scripts(hero_inner)
    hero_html = '<div class="tpl-hero-flat">\n' + hero_inner + "\n</div>"

    by_name: dict[str, str] = {"hero": hero_html, "provas2": provas_body}
    for name, path, wrap_class in blocks:
        b = strip_body_scripts(extract_body(path))
        if name == "cta":
            b = b.replace(
                '<section class="section-cta py-24 sm:py-32 px-6">',
                '<section class="section-cta tpl-cta-flat py-24 sm:py-32 px-6">',
                1,
            )
            b = b.replace(
                '<button class="cta-btn" onclick="window.location.hash=\'checkout\'">',
                '<button type="button" class="cta-btn" onclick="document.getElementById(\'oferta\').scrollIntoView({behavior:\'smooth\'})">',
                1,
            )
        if name == "oferta":
            b = re.sub(
                r'<section class="w-full py-20 md:py-28 px-6">',
                '<section id="oferta" class="w-full py-20 md:py-28 px-6">',
                b,
                count=1,
            )
            b = b.replace(
                """      <div class="fade-up fade-up-delay-1 flat-border rounded-2xl bg-white/70 backdrop-blur-sm p-8 md:p-10">

        <p class="text-xs uppercase tracking-widest text-warm font-bold mb-5">O que está incluso</p>

        <div>
          <div class="stack-item">
            <span class="flex items-center"><span class="material-symbols-outlined">check</span>Método completo em 42 aulas</span>""",
                """      <div class="oferta-card fade-up fade-up-delay-1 flat-border rounded-2xl bg-white/70 backdrop-blur-sm p-8 md:p-10">

        <p class="text-xs uppercase tracking-widest text-warm font-bold mb-5">O que está incluso</p>

        <div>
          <div class="stack-item">
            <span class="flex items-center"><span class="material-symbols-outlined">check</span>Método completo em 42 aulas</span>""",
                1,
            )
        if wrap_class and name != "cta":
            b = f'<div class="{wrap_class}">\n{b}\n</div>'
        by_name[name] = b

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
  document.querySelectorAll('.fade-up, .fadeUp').forEach((el) => fadeUpObs.observe(el));
}});
{TOGGLE_FAQ_JS}
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
          colors: { base:'#fafafa', surface:'#f0f0f2', ink:'#18181b', accent:'#d4d4d8', warm:'#c2956b' },
          fontFamily: { sans:['Inter','sans-serif'], inter:['Inter','sans-serif'] }
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

  <footer class="border-t border-accent/60 py-10 px-6 text-center" style="background:#fafafa;">
    <p class="text-sm text-gray-500">SuaMarca &copy; 2026. Todos os direitos reservados.</p>
    <p class="text-xs text-gray-400 mt-2">
      <a href="#" class="underline hover:text-ink/60">Termos de uso</a>
      <span class="mx-2">&middot;</span>
      <a href="#" class="underline hover:text-ink/60">Política de privacidade</a>
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
