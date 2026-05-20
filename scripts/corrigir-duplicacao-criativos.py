# -*- coding: utf-8 -*-
"""
Corrige a duplicacao gerada pelo migrar-criativos-stories.py.

Apos a migracao, ficaram blocos antigos de confirmacao ChatGPT/API DUPLICADOS
com o novo bloco. Esse script detecta o bloco antigo (marcado pelo texto
"(mais a versão Stories, se o aluno pediu)") e remove apenas a versao antiga.

Uso:
  py -3 scripts/corrigir-duplicacao-criativos.py            # dry-run
  py -3 scripts/corrigir-duplicacao-criativos.py --apply
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "commands" / "criativo-estatico"

SKIP = {
    "ugc-rotina-real.md",
    "promessa-simples.md",
    "caixinha-de-perguntas.md",
    "aida.md",
}

# Bloco antigo a remover:
# **No modo ChatGPT:**
# ```
# (confirmacao antiga ChatGPT)
# ```
#
# **No modo API:**
# ```
# (confirmacao antiga API com "mais a versão Stories, se o aluno pediu")
# ```
#
# (e logo apos vem "No modo ChatGPT, depois da mensagem")
REGEX_DUPLICADO = re.compile(
    r"\*\*No modo ChatGPT:\*\*\s*\n\s*```\s*\n.*?\n```\s*\n+"
    r"\*\*No modo API:\*\*\s*\n\s*```\s*\n.*?mais a vers[ãa]o Stories.*?\n```\s*\n+"
    r"(?=No modo ChatGPT, depois da mensagem)",
    re.DOTALL,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    arquivos = sorted(SKILLS_DIR.glob("*.md"))
    arquivos = [p for p in arquivos if p.name not in SKIP]

    corrigidos = 0
    nao_corrigidos = 0
    for p in arquivos:
        content = p.read_text(encoding="utf-8")
        new = REGEX_DUPLICADO.sub("", content)
        if new != content:
            if args.apply:
                p.write_text(new, encoding="utf-8")
                print(f"  - {p.name}: corrigido.")
            else:
                print(f"  - {p.name}: pronto (dry-run).")
            corrigidos += 1
        else:
            print(f"  - {p.name}: nada a corrigir.")
            nao_corrigidos += 1

    print()
    print(f"Corrigidos: {corrigidos}. Sem mudanca: {nao_corrigidos}.")
    if not args.apply and corrigidos > 0:
        print("Dry-run. Rode com --apply para gravar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
