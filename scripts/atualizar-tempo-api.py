# -*- coding: utf-8 -*-
"""
Atualiza o tempo estimado das mensagens de geracao via API nas sub-skills:
  "cerca de 60 segundos" -> "2 a 3 minutos"
nos anuncios "Proximo passo: gerar a imagem do Feed via API" e
"Proximo passo: gerar a versao Stories a partir da imagem do Feed".

Uso:
  py -3 scripts/atualizar-tempo-api.py            # dry-run
  py -3 scripts/atualizar-tempo-api.py --apply
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "commands" / "criativo-estatico"

# Padroes a substituir
SUBSTITUICOES: list[tuple[str, str]] = [
    # Feed via API
    (
        r"(🔍 Próximo passo: gerar a imagem do Feed via API\. Tempo estimado:)\s*cerca de 60 segundos\.",
        r"\1 2 a 3 minutos.",
    ),
    # Stories a partir da imagem do Feed
    (
        r"(🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed\. Tempo estimado:)\s*cerca de 60 segundos\.",
        r"\1 2 a 3 minutos.",
    ),
    # AIDA: gerar a imagem do criativo via API
    (
        r"(🔍 Próximo passo: gerar a imagem do criativo via API\. Tempo estimado:)\s*cerca de 60 segundos\.",
        r"\1 2 a 3 minutos.",
    ),
    # AIDA: gerar a versao em outro formato a partir da arte atual
    (
        r"(🔍 Próximo passo: gerar a versão em outro formato a partir da arte atual\. Tempo estimado:)\s*cerca de 60 segundos\.",
        r"\1 2 a 3 minutos.",
    ),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    arquivos = sorted(SKILLS_DIR.glob("*.md"))
    total = 0
    for p in arquivos:
        content = p.read_text(encoding="utf-8")
        new = content
        for pat, repl in SUBSTITUICOES:
            new = re.sub(pat, repl, new)
        if new != content:
            if args.apply:
                p.write_text(new, encoding="utf-8")
                print(f"  - {p.name}: atualizado.")
            else:
                print(f"  - {p.name}: pronto (dry-run).")
            total += 1
        else:
            pass  # silencioso para arquivos sem mudanca

    print()
    print(f"Total com mudancas: {total}.")
    if not args.apply and total > 0:
        print("Dry-run. Rode com --apply para gravar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
