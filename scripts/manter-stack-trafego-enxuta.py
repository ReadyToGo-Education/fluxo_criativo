#!/usr/bin/env python3
"""
Mantem a stack de trafego enxuta conforme decidido no PRD.

Decisao do PRD (PRD-stack-trafego-enxuta.md):
- MANTER: trafego-conexao, trafego-criar-campanha, trafego-insights,
          trafego-otimizar, trafego-escalar, trafego-analise, trafego-pago.
- REMOVER: trafego-pixel, trafego-publicos, trafego-regras, trafego-testes.
- REMOVER tambem: sub-skill atalhos-compostos do trafego-otimizar.

O script e idempotente. Pode rodar quantas vezes precisar:
- Remove pasta/arquivo so se ainda existir.
- Edita arquivo so se ainda contiver referencia.

Uso:
    python3 scripts/manter-stack-trafego-enxuta.py
    python3 scripts/manter-stack-trafego-enxuta.py --dry-run
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Pastas inteiras a remover
SKILL_FOLDERS = [
    ROOT / ".claude" / "skills" / "trafego-pixel",
    ROOT / ".claude" / "skills" / "trafego-publicos",
    ROOT / ".claude" / "skills" / "trafego-regras",
    ROOT / ".claude" / "skills" / "trafego-testes",
]

# Arquivos individuais a remover
INDIVIDUAL_FILES = [
    ROOT / ".claude" / "commands" / "trafego-pixel.md",
    ROOT / ".claude" / "commands" / "trafego-publicos.md",
    ROOT / ".claude" / "commands" / "trafego-regras.md",
    ROOT / ".claude" / "commands" / "trafego-testes.md",
    ROOT / ".claude" / "skills" / "trafego-otimizar" / "sub-skills" / "atalhos-compostos.md",
]

# Substituicoes texto-a-texto aplicadas em todos os arquivos .md varridos.
# Ordem importa: padroes mais especificos primeiro pra evitar substituicao parcial.
SUBSTITUTIONS = [
    # trafego-pixel
    ("via 'trafego-pixel' (diagnostico aprofundado)",
     "no Gerenciador de Eventos (diagnostico aprofundado de pixel)"),
    ("via `trafego-pixel` (diagnostico aprofundado)",
     "no Gerenciador de Eventos (diagnostico aprofundado de pixel)"),
    ("via 'trafego-pixel'", "no Gerenciador de Eventos"),
    ("via `trafego-pixel`", "no Gerenciador de Eventos"),
    ('via "trafego-pixel"', "no Gerenciador de Eventos"),
    ("via /trafego-pixel", "no Gerenciador de Eventos"),
    ("`/trafego-pixel`", "Gerenciador de Eventos"),
    ('"/trafego-pixel"', "Gerenciador de Eventos"),
    ("'trafego-pixel'", "Gerenciador de Eventos"),
    ('"trafego-pixel"', "Gerenciador de Eventos"),
    ("/trafego-pixel", "Gerenciador de Eventos"),

    # trafego-publicos
    ("via 'trafego-publicos'", "no Gerenciador de Audiences"),
    ("via `trafego-publicos`", "no Gerenciador de Audiences"),
    ('via "trafego-publicos"', "no Gerenciador de Audiences"),
    ("via /trafego-publicos", "no Gerenciador de Audiences"),
    ("`/trafego-publicos`", "Gerenciador de Audiences"),
    ('"/trafego-publicos"', "Gerenciador de Audiences"),
    ("'trafego-publicos'", "Gerenciador de Audiences"),
    ('"trafego-publicos"', "Gerenciador de Audiences"),
    ("/trafego-publicos", "Gerenciador de Audiences"),

    # trafego-regras
    ("via 'trafego-regras'", "no Gerenciador (Regras automaticas)"),
    ("via `trafego-regras`", "no Gerenciador (Regras automaticas)"),
    ('via "trafego-regras"', "no Gerenciador (Regras automaticas)"),
    ("via /trafego-regras", "no Gerenciador (Regras automaticas)"),
    ("`/trafego-regras`", "Gerenciador (Regras automaticas)"),
    ('"/trafego-regras"', "Gerenciador (Regras automaticas)"),
    ("'trafego-regras'", "Gerenciador (Regras automaticas)"),
    ('"trafego-regras"', "Gerenciador (Regras automaticas)"),
    ("/trafego-regras", "Gerenciador (Regras automaticas)"),

    # trafego-testes
    ("via 'trafego-testes'", "duplicando entidade no Gerenciador (variando 1 dimensao)"),
    ("via `trafego-testes`", "duplicando entidade no Gerenciador (variando 1 dimensao)"),
    ('via "trafego-testes"', "duplicando entidade no Gerenciador (variando 1 dimensao)"),
    ("via /trafego-testes", "duplicando entidade no Gerenciador (variando 1 dimensao)"),
    ("`/trafego-testes`", "Duplicar entidade no Gerenciador (variando 1 dimensao)"),
    ('"/trafego-testes"', "Duplicar entidade no Gerenciador (variando 1 dimensao)"),
    ("'trafego-testes'", "Duplicar entidade no Gerenciador (variando 1 dimensao)"),
    ('"trafego-testes"', "Duplicar entidade no Gerenciador (variando 1 dimensao)"),
    ("/trafego-testes", "Duplicar entidade no Gerenciador (variando 1 dimensao)"),
]

# Pastas e arquivos varridos pelas substituicoes (auto-descobre .md dentro)
SCAN_TARGETS = [
    ROOT / ".claude" / "skills",
    ROOT / ".claude" / "commands",
    ROOT / "CLAUDE.md",
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "ARQUITETURA.md",
]

# Arquivos que NUNCA devem ser editados pelo script
EXCLUDE = {
    Path(__file__).resolve(),
    (ROOT / "PRD-stack-trafego-enxuta.md").resolve(),
}


def remove_folder(path: Path, dry_run: bool) -> bool:
    if not path.exists():
        return False
    if dry_run:
        return True
    shutil.rmtree(path)
    return True


def remove_file(path: Path, dry_run: bool) -> bool:
    if not path.exists():
        return False
    if dry_run:
        return True
    path.unlink()
    return True


def iter_md_files(target: Path):
    if target.is_file() and target.suffix == ".md":
        yield target
    elif target.is_dir():
        for p in target.rglob("*.md"):
            yield p


def apply_substitutions(path: Path, dry_run: bool) -> bool:
    if path.resolve() in EXCLUDE:
        return False
    try:
        original = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return False
    new = original
    for needle, replacement in SUBSTITUTIONS:
        new = new.replace(needle, replacement)
    if new == original:
        return False
    if not dry_run:
        path.write_text(new, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Mostra o que faria sem alterar nada")
    args = parser.parse_args()

    folders_removed = []
    files_removed = []
    files_edited = []

    for folder in SKILL_FOLDERS:
        if remove_folder(folder, args.dry_run):
            folders_removed.append(folder.relative_to(ROOT))

    for f in INDIVIDUAL_FILES:
        if remove_file(f, args.dry_run):
            files_removed.append(f.relative_to(ROOT))

    seen = set()
    for target in SCAN_TARGETS:
        for f in iter_md_files(target):
            key = f.resolve()
            if key in seen:
                continue
            seen.add(key)
            if apply_substitutions(f, args.dry_run):
                files_edited.append(f.relative_to(ROOT))

    prefix = "[dry-run] " if args.dry_run else ""

    print(f"{prefix}Pastas removidas: {len(folders_removed)}")
    for p in folders_removed:
        print(f"  - {p}")

    print(f"{prefix}Arquivos removidos: {len(files_removed)}")
    for f in files_removed:
        print(f"  - {f}")

    print(f"{prefix}Arquivos com referencias limpas: {len(files_edited)}")
    for f in files_edited:
        print(f"  - {f}")

    if not (folders_removed or files_removed or files_edited):
        print("Nada a fazer. Stack ja esta enxuta.")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
