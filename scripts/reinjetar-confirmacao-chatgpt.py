# -*- coding: utf-8 -*-
"""
Reinjeta a confirmacao ChatGPT que foi removida pelo corrigir-duplicacao.

Detecta o padrao:
  Apresente o resultado conforme o modo escolhido. ...

  No modo ChatGPT, depois da mensagem de confirmacao, ofereça o menu padrao:

E insere entre eles o bloco:
  **No modo ChatGPT:**

  ```
  ✅ Concluido: criativo {Nome} salvo.
  Caminho: ...
  Como usar: ...
  ```

Uso:
  py -3 scripts/reinjetar-confirmacao-chatgpt.py            # dry-run
  py -3 scripts/reinjetar-confirmacao-chatgpt.py --apply
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


def detectar_nome_humano(content: str) -> str:
    m = re.search(r"^# ([^\n]+) n[ºo°] \{numero\}", content, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    raise ValueError("Nome humano nao encontrado")


def detectar_slug(content: str) -> str:
    candidates = re.findall(r"criativo-([a-z0-9-]+)-\{numero\}-feed\.png", content)
    if candidates:
        return candidates[0]
    raise ValueError("Slug nao encontrado")


def bloco_chatgpt(nome: str, slug: str) -> str:
    return f"""**No modo ChatGPT:**

```
✅ Concluído: criativo {nome} salvo.

Caminho: {{caminho-raiz-projeto}}\\meus-produtos\\{{ativo}}\\entregas\\criativos\\criativo-{slug}-{{numero}}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

"""


REGEX_INSERIR = re.compile(
    r"(Apresente o resultado conforme o modo escolhido[^\n]*\n\n)"
    r"(No modo ChatGPT, depois da mensagem de confirma[çc][ãa]o,)",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    arquivos = sorted(SKILLS_DIR.glob("*.md"))
    arquivos = [p for p in arquivos if p.name not in SKIP]

    ok = 0
    for p in arquivos:
        content = p.read_text(encoding="utf-8")

        try:
            nome = detectar_nome_humano(content)
            slug = detectar_slug(content)
        except ValueError as e:
            print(f"  - {p.name}: ERRO {e}")
            continue

        # Verifica se a confirmacao ChatGPT ja existe (evita duplicar)
        if re.search(r"\*\*No modo ChatGPT:\*\*\s*\n\s*```\s*\n.*?salvo\.\s*\n.*?Caminho:", content, re.DOTALL):
            print(f"  - {p.name}: ja tem a confirmacao ChatGPT, pulando.")
            continue

        injecao = bloco_chatgpt(nome, slug)
        new = REGEX_INSERIR.sub(
            lambda m: m.group(1) + injecao + m.group(2),
            content,
            count=1,
        )
        if new == content:
            print(f"  - {p.name}: padrao nao casou, pulando.")
            continue

        if args.apply:
            p.write_text(new, encoding="utf-8")
            print(f"  - {p.name}: reinjetado.")
        else:
            print(f"  - {p.name}: pronto (dry-run).")
        ok += 1

    print()
    print(f"Reinjetados: {ok}.")
    if not args.apply and ok > 0:
        print("Dry-run. Rode com --apply para gravar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
