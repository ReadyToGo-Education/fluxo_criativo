# -*- coding: utf-8 -*-
"""
Troca "Gerar agora pela API" por "Gerar agora pelo OpenRouter" nas sub-skills
de /criativo-estatico, porque os alunos do sistema estao mais familiarizados
com o nome do provider.

Uso:
  py -3 scripts/trocar-api-por-openrouter.py            # dry-run
  py -3 scripts/trocar-api-por-openrouter.py --apply
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "commands" / "criativo-estatico"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    total = 0
    for p in sorted(SKILLS_DIR.glob("*.md")):
        content = p.read_text(encoding="utf-8")
        if "Gerar agora pela API" not in content:
            continue
        new = content.replace(
            "Gerar agora pela API",
            "Gerar agora pelo OpenRouter",
        )
        if args.apply:
            p.write_text(new, encoding="utf-8")
            print(f"  - {p.name}: atualizado.")
        else:
            print(f"  - {p.name}: pronto (dry-run).")
        total += 1

    print()
    print(f"Total com mudancas: {total}.")
    if not args.apply and total > 0:
        print("Dry-run. Rode com --apply para gravar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
