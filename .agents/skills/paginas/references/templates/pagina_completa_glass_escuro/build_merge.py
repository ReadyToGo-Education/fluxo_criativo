# -*- coding: utf-8 -*-
"""Regenera code.html a partir dos templates *_glass_escuro. Uso: py -3 build_merge.py"""
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


def scope_oferta_final(css: str) -> str:
    prefixes = (
        ".stack-label",
        ".stack-list",
        ".stack-item",
        ".stack-item-name",
        ".stack-item-value",
        ".stack-total",
        ".stack-total-label",
        ".stack-total-value",
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


def main():
    hero_path = BASE / "hero_glass_escuro" / "code.html"
    hero_html = extract_body(hero_path)
    hero_css = extract_style(hero_path)

    blocks = [
        ("dor", BASE / "dor_glass_escuro" / "code.html", ".section-dor"),
        ("paliativo", BASE / "paliativo_glass_escuro" / "code.html", ".paliativo-section"),
        ("provas", BASE / "provas_sociais_glass_escuro" / "code.html", ".provas-section"),
        ("cta", BASE / "cta_glass_escuro" / "code.html", ".cta-section"),
        ("metodo", BASE / "metodo_glass_escuro" / "code.html", ".metodo-section"),
        ("para_quem", BASE / "para_quem_glass_escuro" / "code.html", ".paraquem-section"),
        ("entregaveis", BASE / "entregaveis_glass_escuro" / "code.html", ".entregaveis-section"),
        ("bonus", BASE / "bonus_glass_escuro" / "code.html", ".bonus-section"),
        ("stack", BASE / "stack_valor_glass_escuro" / "code.html", ".stack-section"),
        ("suporte", BASE / "suporte_glass_escuro" / "code.html", ".suporte-section"),
        ("garantia", BASE / "garantia_glass_escuro" / "code.html", ".garantia-section"),
        ("autoridade", BASE / "autoridade_glass_escuro" / "code.html", ".autoridade-section"),
        ("faq", BASE / "faq_glass_escuro" / "code.html", ".faq-section"),
        ("oferta", BASE / "oferta_final_glass_escuro" / "code.html", ".oferta-section"),
    ]

    dep_path = BASE / "hero_glass_escuro_depoimentos" / "code.html"
    dep_body = extract_body(dep_path)
    dep_main_m = re.search(r"(<main>.*?</main>)", dep_body, re.DOTALL | re.IGNORECASE)
    dep_main = dep_main_m.group(1) if dep_main_m else ""
    dep_script_m = re.search(r"(<script>.*?</script>)", dep_body, re.DOTALL | re.IGNORECASE)
    dep_script = dep_script_m.group(1) if dep_script_m else ""
    dep_css = scope_shimmer(extract_style(dep_path), ".depoimentos-wrap")

    css_chunks = ["/* === hero_glass_escuro === */", hero_css]
    for name, path, scope in blocks:
        css = extract_style(path)
        css = scope_shimmer(css, scope)
        if name == "stack":
            css = scope_stack_valor(css)
        if name == "oferta":
            css = scope_oferta_final(css)
        css_chunks.append(f"/* === {name} === */")
        css_chunks.append(css)

    css_chunks.append("/* === hero_glass_escuro_depoimentos === */")
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

    by_name: dict[str, str] = {"hero": hero_html}
    for name, path, _scope in blocks:
        b = extract_body(path)
        if name == "oferta":
            b = b.replace(
                '<section class="oferta-section">',
                '<section id="oferta" class="oferta-section">',
                1,
            )
        if name == "cta":
            b = b.replace(
                '<a href="#" class="cta-button">',
                '<a href="#oferta" class="cta-button">',
                1,
            )
        by_name[name] = b

    by_name["depoimentos"] = f'<div class="depoimentos-wrap">\n{dep_main}\n</div>'

    by_name["hero"] = by_name["hero"].replace(
        '<button class="cta-button">',
        '<button type="button" class="cta-button" onclick="document.getElementById(\'oferta\').scrollIntoView({behavior:\'smooth\'})">',
        1,
    )

    final_body = "\n\n".join(by_name[n] for n in order_names)

    faq_full = (BASE / "faq_glass_escuro" / "code.html").read_text(encoding="utf-8")
    fm = re.search(r"<script>(.*?)</script>", faq_full, re.DOTALL)
    faq_script = ""
    if fm:
        faq_script = "<script>\n" + fm.group(1).strip() + "\n</script>"

    html_out = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nome do Produto. Transformação Principal</title>
  <meta name="description" content="Descrição de até 160 caracteres com a promessa principal do produto.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap" rel="stylesheet">
  <style>
{merged_css}
  </style>
</head>
<body>

{final_body}

  <footer style="padding:40px 24px; text-align:center; border-top:1px solid rgba(255,255,255,0.08);">
    <p style="font-size:0.85rem; color:#6c6c6c;">SuaMarca &copy; 2026. Todos os direitos reservados.</p>
    <p style="font-size:0.75rem; color:#6c6c6c; margin-top:8px;"><a href="#" style="color:#6c6c6c; text-decoration:underline;">Termos de uso</a> &middot; <a href="#" style="color:#6c6c6c; text-decoration:underline;">Política de privacidade</a></p>
  </footer>

{dep_script}

{faq_script}

</body>
</html>
"""

    out = Path(__file__).resolve().parent / "code.html"
    out.write_text(html_out, encoding="utf-8")
    print("Wrote", out, "chars", len(html_out))


if __name__ == "__main__":
    main()
