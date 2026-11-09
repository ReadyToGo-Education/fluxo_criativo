# -*- coding: utf-8 -*-
"""
Monta a pagina final de vendas a partir de copias HTML ja geradas pela
ui-reverse-engineer + copy aprovada em 16 blocos.

Pipeline:
1. Le meus-produtos/{slug}/entregas/paginas/copias/manifest.json
   (ordem das secoes + mapeamento copia -> bloco da copy)
2. Para cada entrada do manifest, le o HTML da copia correspondente em
   meus-produtos/{slug}/entregas/paginas/copias/{arquivo}.html
3. Extrai <style> e <body> de cada copia, escopa o CSS sob um wrapper
   unico (.secao-{id}) pra nao colidir com outras secoes
4. Concatena todas as secoes na ordem do manifest
5. Monta HTML final com <head> minimo + fontes do Google + JS de animacao
6. Salva em meus-produtos/{slug}/entregas/paginas/vendas-{slug}.html

IMPORTANTE. Esta etapa NAO adapta copy ao design. A adaptacao acontece
no passo anterior (agente clonador-de-bloco-visual), que ja grava os
code.html das copias com a copy aprovada substituindo os textos do print
original. Este script so monta.

Regra de ouro do design. Cada copia preserva 100 porcento do design
extraido do print. O script escopa o CSS sob wrapper pra evitar colisao,
mas NUNCA mescla cores ou fontes entre secoes.

Uso:
  py -3 scripts/montar-pagina-copias.py --slug meu-produto
  py -3 scripts/montar-pagina-copias.py --slug meu-produto --verbose
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def extract_style(html: str) -> str:
    """Extrai conteudo do primeiro <style>...</style>."""
    m = re.search(r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def extract_body(html: str) -> str:
    """Extrai conteudo do <body>...</body>."""
    m = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else html


def extract_font_links(html: str) -> list[str]:
    """Coleta <link> de fontes do Google/Fontsource pra injetar no head final."""
    links = re.findall(
        r'<link[^>]+href="[^"]*fonts\.(?:googleapis|gstatic)\.com[^"]*"[^>]*/?>',
        html,
        flags=re.IGNORECASE,
    )
    return [re.sub(r"\s+", " ", l).strip() for l in links]


def extract_tailwind_script(html: str) -> str | None:
    """Se a copia usa tailwindcss via CDN, retorna o <script> (pra unificar no head)."""
    m = re.search(
        r'<script[^>]*src="https://cdn\.tailwindcss\.com[^"]*"[^>]*>\s*</script>',
        html,
        flags=re.IGNORECASE,
    )
    return m.group(0) if m else None


def extract_body_scripts(body: str) -> tuple[str, list[str]]:
    """Remove <script>...</script> do body e retorna (body_sem_scripts, lista_de_scripts)."""
    scripts = re.findall(r"<script\b[^>]*>.*?</script>", body, flags=re.DOTALL | re.IGNORECASE)
    body_clean = re.sub(r"<script\b[^>]*>.*?</script>", "", body, flags=re.DOTALL | re.IGNORECASE)
    return body_clean.strip(), scripts


def _escopar_seletor(s: str, scope: str) -> str:
    """Aplica o prefixo `scope` a um seletor individual."""
    if s == ":root" or s.startswith(":"):
        return s
    if s in ("html", "body"):
        return scope
    if s == "*":
        return f"{scope} *"
    return f"{scope} {s}"


def _fim_do_bloco(css: str, inicio: int) -> int:
    """Recebe a posição logo após um `{` e devolve a posição do `}` correspondente."""
    profundidade = 1
    i = inicio
    while i < len(css):
        if css[i] == "{":
            profundidade += 1
        elif css[i] == "}":
            profundidade -= 1
            if profundidade == 0:
                return i
        i += 1
    return len(css)


def scope_css(css: str, scope: str) -> str:
    """Prefixa seletores CSS com `scope` pra evitar colisao entre secoes.

    Regras:
    - html, body, * viram o proprio scope (nao vazam pro documento global)
    - :root, keyframes, font-face e demais @-rules sem seletores ficam intactos
    - @media, @supports e @container sao percorridos por dentro, para que as
      regras responsivas recebam o mesmo prefixo (e a mesma especificidade)
      das regras de fora. Sem isso, a versão de celular perde para a de desktop.
    - seletores normais recebem prefixo `scope `
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    out: list[str] = []
    i = 0
    while i < len(css):
        abre = css.find("{", i)
        if abre == -1:
            out.append(css[i:])
            break
        preludio = css[i:abre]
        # Declarações soltas do tipo @import ...; antes do próximo bloco
        if ";" in preludio:
            corte = preludio.rfind(";") + 1
            out.append(preludio[:corte])
            preludio = preludio[corte:]
        fecha = _fim_do_bloco(css, abre + 1)
        corpo = css[abre + 1:fecha]
        cabeca = preludio.strip()
        if cabeca.startswith(("@media", "@supports", "@container")):
            out.append(f"{cabeca} {{{scope_css(corpo, scope)}}}")
        elif cabeca.startswith("@"):
            out.append(f"{cabeca} {{{corpo}}}")
        else:
            seletores = [s.strip() for s in cabeca.split(",") if s.strip()]
            out.append(", ".join(_escopar_seletor(s, scope) for s in seletores) + f" {{{corpo}}}")
        out.append("\n")
        i = fecha + 1
    return "".join(out)


def montar_secao(copia_html: str, secao_id: str) -> tuple[str, str, list[str], list[str]]:
    """Dado o HTML bruto de uma copia, retorna:
    - css_escopado: CSS da copia com scope .secao-{id}
    - body_wrapped: <div class="secao-{id}"> + body da copia + </div>
    - font_links: lista de <link> de fontes pra injetar no head
    - body_scripts: lista de <script> do body pra injetar no fim da pagina
    """
    scope = f".secao-{secao_id}"
    css = extract_style(copia_html)
    body = extract_body(copia_html)
    body_clean, scripts = extract_body_scripts(body)
    font_links = extract_font_links(copia_html)
    css_scoped = scope_css(css, scope) if css else ""
    body_wrapped = f'<div class="secao-{secao_id}">\n{body_clean}\n</div>'
    return css_scoped, body_wrapped, font_links, scripts


def main() -> None:
    p = argparse.ArgumentParser(description="Monta pagina final a partir de copias HTML.")
    p.add_argument("--slug", default=None, help="Slug do produto (default: meus-produtos/.ativo)")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    slug = args.slug
    if not slug:
        ativo = ROOT / "meus-produtos" / ".ativo"
        if ativo.is_file():
            slug = ativo.read_text(encoding="utf-8").strip()
    if not slug:
        print("Defina --slug ou crie meus-produtos/.ativo", file=sys.stderr)
        sys.exit(2)

    base = ROOT / "meus-produtos" / slug / "entregas" / "paginas"
    copias_dir = base / "copias"
    manifest_path = copias_dir / "manifest.json"
    dest = base / f"vendas-{slug}.html"

    if not manifest_path.is_file():
        print(f"manifest.json nao encontrado em {manifest_path}", file=sys.stderr)
        print("Rode /pagina-visual primeiro para gerar as copias e o manifest.", file=sys.stderr)
        sys.exit(3)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, list) or not manifest:
        print("manifest.json invalido ou vazio. Esperado lista de entradas.", file=sys.stderr)
        sys.exit(4)

    if args.verbose:
        print(f"Slug: {slug}")
        print(f"Copias: {copias_dir}")
        print(f"Secoes no manifest: {len(manifest)}")

    tailwind_tag: str | None = None
    all_font_links: list[str] = []
    all_css: list[str] = []
    all_body: list[str] = []
    all_scripts: list[str] = []

    for i, entry in enumerate(manifest, start=1):
        arquivo = entry.get("copia") or entry.get("file") or entry.get("arquivo")
        if not arquivo:
            print(f"[entrada {i}] sem campo 'copia'. Pulando.", file=sys.stderr)
            continue
        secao_id = entry.get("secao") or entry.get("id") or f"s{i:02d}"
        copia_path = copias_dir / arquivo
        if not copia_path.is_file():
            print(f"[entrada {i}] arquivo nao encontrado: {copia_path}", file=sys.stderr)
            continue
        html = copia_path.read_text(encoding="utf-8")
        if tailwind_tag is None:
            tailwind_tag = extract_tailwind_script(html)
        css_scoped, body_wrapped, font_links, scripts = montar_secao(html, secao_id)
        all_css.append(f"/* === secao-{secao_id} ({arquivo}) === */\n{css_scoped}")
        all_body.append(body_wrapped)
        all_scripts.extend(scripts)
        for fl in font_links:
            if fl not in all_font_links:
                all_font_links.append(fl)
        if args.verbose:
            print(f"[{i}] secao-{secao_id} <- {arquivo} ({len(css_scoped)} chars css)")

    if not all_body:
        print("Nenhuma secao valida no manifest. Abortando.", file=sys.stderr)
        sys.exit(5)

    # Monta HTML final
    fonts_head = "\n".join(all_font_links)
    tailwind_head = tailwind_tag or ""
    page_title = manifest[0].get("title") if isinstance(manifest[0], dict) else None
    if not page_title:
        page_title = f"Pagina de vendas. {slug}"
    page_desc = manifest[0].get("description") if isinstance(manifest[0], dict) else ""
    if not page_desc:
        page_desc = "Pagina de vendas do produto."

    # Trecho opcional para o <head> (ex: Meta Pixel). Fica em copias/head-extra.html
    # para sobreviver a cada nova montagem da página.
    head_extra_path = copias_dir / "head-extra.html"
    head_extra = head_extra_path.read_text(encoding="utf-8").strip() if head_extra_path.is_file() else ""

    merged_css = "\n\n".join(all_css)
    merged_body = "\n\n".join(all_body)
    merged_scripts = "\n".join(all_scripts)

    html_out = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<meta name="description" content="{page_desc}">
{head_extra}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fonts_head}
{tailwind_head}
<style>
/* Reset minimo pra wrappers nao colidirem com margens do body */
html, body {{ margin: 0; padding: 0; overflow-x: hidden; }}
body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
[class^="secao-"] {{ width: 100%; max-width: 100%; }}

{merged_css}
</style>
</head>
<body>

{merged_body}

{merged_scripts}

</body>
</html>
"""

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_out, encoding="utf-8")

    print(f"Gerado: {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")
    print(f"Secoes: {len(all_body)}")


if __name__ == "__main__":
    main()
