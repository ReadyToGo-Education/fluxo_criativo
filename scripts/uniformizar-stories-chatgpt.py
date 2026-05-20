# -*- coding: utf-8 -*-
"""
Uniformiza o fluxo do modo ChatGPT nas sub-skills do Padrao B: remove a pergunta
"Quer que eu gere o prompt no formato Stories tambem?" e torna a entrega do
Prompt Stories incondicional (sempre vai junto do Feed).

Uso:
  py -3 scripts/uniformizar-stories-chatgpt.py            # dry-run
  py -3 scripts/uniformizar-stories-chatgpt.py --apply
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "commands" / "criativo-estatico"

SKIP = {"aida.md"}


# Patterns a substituir
SUBSTITUICOES: list[tuple[str, str]] = [
    # 1) Remove a pergunta + frase que a introduz
    # "Depois de entregar, escreva:\n\n**"Quer que eu gere..."**" -> remove tudo
    (
        r"Depois de entregar(?: este bloco ao aluno)?(?:[^\n]*?), escreva:\s*\n\n\*\*[\"“]Quer que eu gere o prompt no formato Stories \(9:16\) tamb[ée]m\?[\"”]\*\*\s*\n\n",
        "",
    ),
    # 2) Em arquivos onde a pergunta aparece em outro lugar sem o "Depois de entregar"
    (
        r"\*\*[\"“]Quer que eu gere o prompt no formato Stories \(9:16\) tamb[ée]m\?[\"”]\*\*\s*\n\n",
        "",
    ),
    # 3) Linha solta (sem ** **) com a pergunta
    (
        r"^\s*Quer que eu gere o prompt no formato Stories \(9:16\) tamb[ée]m\?\s*\n",
        "",
    ),
    # 4) "Se o aluno responder sim, entregue o prompt Stories:" -> "Em seguida, entregue o prompt no formato Stories:"
    (
        r"Se o aluno responder (?:que )?sim, entregue(?: o prompt Stories)?:\s*\n",
        "Em seguida, entregue o prompt no formato Stories:\n",
    ),
    # 5) "Se o aluno responder sim, entregue:" -> "Em seguida, entregue:"
    (
        r"Se o aluno responder (?:que )?sim, entregue:\s*\n",
        "Em seguida, entregue:\n",
    ),
    # 6) "(Se o aluno pediu Stories também:)" -> remove (sempre incluir)
    (
        r"\(Se o aluno pediu Stories(?: tamb[ée]m)?[:.]?\)\s*\n",
        "",
    ),
    # 7) "(Se o aluno pediu Stories, incluir também o bloco ...)" -> remove
    (
        r"\(Se o aluno pediu Stories,? incluir tamb[ée]m[^)]*\)\s*\n",
        "",
    ),
    # 8) "(Se o aluno pediu Stories, incluir a seção abaixo.)" -> remove
    (
        r"\(Se o aluno pediu Stories,? incluir a se[çc][ãa]o abaixo\.\)\s*\n",
        "",
    ),
    # 9) "(Incluir apenas se o aluno pediu Stories...)" -> remove
    (
        r"\(Incluir apenas se o aluno pediu [Ss]tories[^)]*\)\s*\n",
        "",
    ),
    # 10) "(Incluir só se o aluno pediu Stories também.)" -> remove
    (
        r"\(Incluir s[óo] se o aluno pediu [Ss]tories[^)]*\)\s*\n",
        "",
    ),
    # 11) "Formato Stories (1080x1920, 9:16) — opcional" -> "Formato Stories (1080x1920, 9:16)"
    (
        r"Formato Stories \(1080x1920, 9:16\)\s*[—-]\s*opcional",
        "Formato Stories (1080x1920, 9:16)",
    ),
    # 12) "Prompt de Stories (9:16) pro ChatGPT (entrega condicional)" -> sem o (entrega condicional)
    (
        r"(Prompt de Stories \(9:16\) pro ChatGPT)\s*\(entrega condicional\)",
        r"\1",
    ),
    # 13) Regra de Stories opcional: substituir por sempre obrigatorio
    (
        r"-\s*Stories [ée] entrega OPCIONAL e condicional\.[^\n]*\n",
        "- Stories é entrega OBRIGATÓRIA, sempre junto do Feed.\n",
    ),
    # 14) "Se gerou Stories, cole o Prompt Stories..." -> "Cole o Prompt Stories..."
    (
        r"Se gerou Stories,\s*c",
        "C",
    ),
    # 15) "(mais a versão Stories, se o aluno pediu)" em mensagem de confirmação API
    #    (caso ainda exista após corrigir-duplicacao)
    (
        r"\s*\n\(mais a vers[ãa]o Stories, se o aluno pediu\)",
        "",
    ),
    # 16) Descrição da skill no header: "Feed e Stories opcional" -> "Feed e Stories"
    (
        r"Feed e Stories opcional",
        "Feed e Stories",
    ),
    # 17) "Stories opcional" no header da descrição (modo geral)
    (
        r"Stories opcional",
        "Stories",
    ),
    # 18) "Depois pergunta se quer Stories também" no header (timelapse, etc.)
    (
        r"\s*Depois pergunta se quer Stories tamb[ée]m\.?",
        "",
    ),
    # 19) "(e o Stories opcional, se o aluno pediu)" -> "(Feed e Stories)"
    (
        r"\(e o Stories(?: opcional)?, se o aluno pediu\)",
        "(Feed e Stories)",
    ),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    arquivos = sorted(SKILLS_DIR.glob("*.md"))
    arquivos = [p for p in arquivos if p.name not in SKIP]

    total_mudancas = 0
    for p in arquivos:
        content = p.read_text(encoding="utf-8")
        original = content

        for pat, repl in SUBSTITUICOES:
            flags = re.MULTILINE
            new = re.sub(pat, repl, content, flags=flags)
            content = new

        if content != original:
            if args.apply:
                p.write_text(content, encoding="utf-8")
                print(f"  - {p.name}: atualizado.")
            else:
                print(f"  - {p.name}: pronto (dry-run).")
            total_mudancas += 1
        else:
            print(f"  - {p.name}: sem mudancas.")

    print()
    print(f"Total com mudancas: {total_mudancas}.")
    if not args.apply and total_mudancas > 0:
        print("Dry-run. Rode com --apply para gravar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
