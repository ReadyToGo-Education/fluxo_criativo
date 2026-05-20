# -*- coding: utf-8 -*-
"""
Corrige o menu API pos-entrega nas 20 sub-skills migradas.

Hoje esta como bullets em prosa:
  - Opção 1: Gerar para o formato de Stories (a partir da imagem do Feed)
  - Opções 2, 3, 4: mesmas opções do menu ChatGPT acima, na mesma ordem, renumeradas

O Claude que executa a sub-skill nao consegue inferir as opcoes 2, 3 e 4 e
acaba mostrando o menu ChatGPT antigo. Vamos extrair o menu ChatGPT atual de
cada arquivo, renumerar adicionando "Stories" como opcao 1, e gravar como
bloco de codigo numerado explicito.

Uso:
  py -3 scripts/corrigir-menu-api.py            # dry-run
  py -3 scripts/corrigir-menu-api.py --apply
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "commands" / "criativo-estatico"

# Sub-skills ja corretas manualmente (nao mexer)
JA_CORRETAS = {
    "ugc-rotina-real.md",
    "promessa-simples.md",
    "caixinha-de-perguntas.md",
    "aida.md",  # tem fluxo proprio
}

# Bloco antigo em bullets a substituir
REGEX_BULLETS = re.compile(
    r"Depois ofereça o menu com \"Gerar para o formato de Stories\" como nova primeira opção \(deslocando as demais em 1\):\s*\n\n"
    r"- Opção 1: Gerar para o formato de Stories \(a partir da imagem do Feed\)\s*\n"
    r"- Opções 2, 3, 4: mesmas opções do menu ChatGPT acima, na mesma ordem, renumeradas\s*\n"
)

# Regex para extrair o menu ChatGPT acima (numerado em bloco de codigo)
REGEX_MENU_CHATGPT = re.compile(
    r"No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:\s*\n\s*```\s*\n"
    r"(?P<intro>[^\n]+)\n"  # "Quer fazer mais alguma coisa?" ou similar
    r"(?P<opcoes>(?:\d+\.[^\n]+\n)+)"
    r"```",
    re.MULTILINE,
)


def extrair_opcoes(menu: str) -> list[str]:
    """Extrai opcoes numeradas '1. ...', '2. ...' do texto."""
    return re.findall(r"^\d+\.\s*([^\n]+)$", menu, flags=re.MULTILINE)


def construir_novo_menu_api(intro: str, opcoes_chatgpt: list[str]) -> str:
    """Constroi o menu API com Stories como opcao 1 + opcoes ChatGPT renumeradas."""
    linhas = [
        "Depois ofereça o menu com \"Gerar para o formato de Stories\" como nova primeira opção:",
        "",
        "```",
        intro,
        "1. Gerar para o formato de Stories (a partir da imagem do Feed)",
    ]
    for i, op in enumerate(opcoes_chatgpt, start=2):
        linhas.append(f"{i}. {op}")
    linhas.append("```")
    linhas.append("")
    return "\n".join(linhas)


def migrar_arquivo(path: Path) -> tuple[bool, str]:
    content = path.read_text(encoding="utf-8")
    original = content

    m_chat = REGEX_MENU_CHATGPT.search(content)
    if not m_chat:
        return False, "[ERRO] menu ChatGPT nao encontrado"

    intro = m_chat.group("intro").strip()
    opcoes_chatgpt = extrair_opcoes(m_chat.group("opcoes"))
    if not opcoes_chatgpt:
        return False, "[ERRO] opcoes do menu ChatGPT vazias"

    novo_bloco = construir_novo_menu_api(intro, opcoes_chatgpt)

    if not REGEX_BULLETS.search(content):
        return False, "[INFO] bullets nao encontrados (talvez ja corrigido)"

    content = REGEX_BULLETS.sub(lambda _: novo_bloco, content, count=1)
    return content != original, content


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    arquivos = sorted(SKILLS_DIR.glob("*.md"))
    arquivos = [p for p in arquivos if p.name not in JA_CORRETAS]

    ok = 0
    erros = 0
    for p in arquivos:
        mudou, content_or_err = migrar_arquivo(p)
        if not mudou:
            if content_or_err.startswith("[ERRO"):
                print(f"  - {p.name}: {content_or_err}")
                erros += 1
            else:
                print(f"  - {p.name}: {content_or_err}")
            continue
        if args.apply:
            p.write_text(content_or_err, encoding="utf-8")
            print(f"  - {p.name}: aplicado.")
        else:
            print(f"  - {p.name}: pronto (dry-run).")
        ok += 1

    print()
    print(f"Total processado: {ok}. Erros: {erros}.")
    if not args.apply and ok > 0:
        print("Dry-run. Rode com --apply para gravar.")
    return 0 if erros == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
