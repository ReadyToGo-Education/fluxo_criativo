# -*- coding: utf-8 -*-
"""
Migra as sub-skills de /criativo-estatico para o novo fluxo:
  - Passo 6b: modo API gera apenas o Feed, sem perguntar formato
  - Passo 7: menu de 4 opcoes no modo API com "Gerar para Stories" como opcao 1
  - Sub-fluxo Stories: image-to-image usando --reference-image no script

Pula sub-skills ja convertidas manualmente e tambem o aida.md (caso especial).

Uso:
  py -3 scripts/migrar-criativos-stories.py            # dry-run, mostra o que vai mudar
  py -3 scripts/migrar-criativos-stories.py --apply    # aplica as mudancas
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "commands" / "criativo-estatico"

JA_CONVERTIDAS = {
    "ugc-rotina-real.md",
    "promessa-simples.md",
    "caixinha-de-perguntas.md",
}
SKIP = JA_CONVERTIDAS | {"aida.md"}


def detectar_slug_arquivos(content: str) -> str:
    """O slug usado em 'criativo-{slug}-{numero}.md' pode diferir do nome do .md."""
    candidates = re.findall(r"criativo-([a-z0-9-]+)-\{numero\}-feed\.png", content)
    if candidates:
        return candidates[0]
    m = re.search(r"prompt-([a-z0-9-]+)-\{numero\}-feed\.txt", content)
    if m:
        return m.group(1)
    raise ValueError("Slug nao encontrado")


def detectar_nome_humano(content: str) -> str:
    """Nome humano do criativo (ex: 'POV', 'Caixinha de Perguntas')."""
    m = re.search(r"^# ([^\n]+) n[ºo°] \{numero\}", content, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    raise ValueError("Nome humano nao encontrado")


def novo_passo_6b(slug: str) -> str:
    return f"""### 6b. Modo API (só se o aluno escolheu a opção 2)

Depois de salvar o `.md`, gere apenas a imagem do Feed pela API. A versão Stories sai depois, como opção no menu do Passo 7, reaproveitando a imagem do Feed como referência visual.

1. Leia `OPENROUTER_API_KEY` no `.env`. Se faltar, ofereça configurar com o `/configurar-imagens` ou voltar pro modo ChatGPT.

2. Pergunte o modelo:

```
Qual modelo de imagem?

1. GPT Image 2 (recomendado)
   Cerca de US$ 0,05 por imagem.
2. Gemini Nano Banana 2
   Cerca de US$ 0,07 por imagem.

Digite o número:
```

Opção 1 vira `openai/gpt-5.4-image-2`, opção 2 vira `google/gemini-3.1-flash-image-preview`. Guarde o modelo escolhido, ele vai ser reaproveitado se o aluno pedir Stories no Passo 7.

3. Grave o Prompt Feed num arquivo `.txt` na pasta de criativos. Conteúdo é o Prompt Feed apresentado ao aluno, sem alterações.

4. Anuncie e rode o script no formato Feed (4:5):

```
🔍 Próximo passo: gerar a imagem do Feed via API. Tempo estimado: cerca de 60 segundos.
```

Use o comando Python correto da sessão (`python3` ou `py -3`), conforme a seção Execução de Scripts Python do CLAUDE.md.

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{{ativo}}/entregas/criativos/prompt-{slug}-{{numero}}-feed.txt" --model "{{modelo}}" --aspect "4:5" --out "meus-produtos/{{ativo}}/entregas/criativos/criativo-{slug}-{{numero}}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

"""


def novo_bloco_menu(slug: str, nome_humano: str, menu_original: str) -> str:
    """Novo bloco substituindo 'Depois, nos dois modos, ofereça:' + menu original."""
    # Limpa marcadores de codigo e linha final do menu original
    menu_limpo = menu_original.strip()

    novo = f"""No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
{menu_limpo}
```

**No modo API:**

```
✅ Concluído: criativo {nome_humano} gerado e salvo.

Imagem do Feed: {{caminho-raiz-projeto}}\\meus-produtos\\{{ativo}}\\entregas\\criativos\\criativo-{slug}-{{numero}}-feed.png
Briefing: {{caminho-raiz-projeto}}\\meus-produtos\\{{ativo}}\\entregas\\criativos\\criativo-{slug}-{{numero}}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção (deslocando as demais em 1):

- Opção 1: Gerar para o formato de Stories (a partir da imagem do Feed)
- Opções 2, 3, 4: mesmas opções do menu ChatGPT acima, na mesma ordem, renumeradas

#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-{slug}-{{numero}}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: cerca de 60 segundos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{{ativo}}/entregas/criativos/prompt-{slug}-{{numero}}-stories.txt" --model "{{modelo}}" --aspect "9:16" --reference-image "meus-produtos/{{ativo}}/entregas/criativos/criativo-{slug}-{{numero}}-feed.png" --out "meus-produtos/{{ativo}}/entregas/criativos/criativo-{slug}-{{numero}}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {{caminho-raiz-projeto}}\\meus-produtos\\{{ativo}}\\entregas\\criativos\\criativo-{slug}-{{numero}}-stories.png
```

e) Reapresente o mesmo menu de opções."""
    return novo


# Padrao do Passo 6b atual (com pergunta de formato Feed/Stories/os dois)
REGEX_PASSO_6B = re.compile(
    r"#{2,3} (?:\d+b?\. )?Modo API.*?(?=#{2,3} (?:\d+\. )?Confirma)",
    re.DOTALL,
)

# Padrao do bloco "Depois, nos dois modos, ofereça:" + bloco de codigo do menu
# Captura ate o proximo \n## (proxima secao do arquivo, geralmente "## Regras")
# ou ate "Se o aluno escolher" linha solta
REGEX_BLOCO_MENU = re.compile(
    r"Depois, nos dois modos, ofereça:\s*\n\s*```\s*\n(.*?)\n```\s*\n+(Se o aluno escolher [^\n]+\n+)?",
    re.DOTALL,
)


def migrar_arquivo(path: Path) -> tuple[bool, str]:
    """Aplica migracao a UM arquivo. Retorna (mudou, conteudo_novo)."""
    content = path.read_text(encoding="utf-8")
    original = content

    try:
        slug = detectar_slug_arquivos(content)
        nome_humano = detectar_nome_humano(content)
    except ValueError as e:
        return False, f"[ERRO ao detectar slug/nome] {e}"

    # 1) Substituir o Passo 6b (lambda evita problemas de escape em \m, \n, etc.)
    if not REGEX_PASSO_6B.search(content):
        return False, "[ERRO] Passo 6b nao encontrado no formato esperado."
    novo_6b = novo_passo_6b(slug)
    content = REGEX_PASSO_6B.sub(lambda _: novo_6b, content, count=1)

    # 2) Substituir o bloco do menu pos-entrega
    m = REGEX_BLOCO_MENU.search(content)
    if not m:
        return False, "[ERRO] Bloco do menu pos-entrega nao encontrado."
    menu_original = m.group(1)
    novo_bloco = novo_bloco_menu(slug, nome_humano, menu_original) + "\n\n"
    content = REGEX_BLOCO_MENU.sub(lambda _: novo_bloco, content, count=1)

    mudou = content != original
    return mudou, content


def main() -> int:
    ap = argparse.ArgumentParser(description="Migra sub-skills criativo-estatico.")
    ap.add_argument("--apply", action="store_true",
                    help="Aplica as mudancas. Sem essa flag, faz dry-run.")
    args = ap.parse_args()

    arquivos = sorted(SKILLS_DIR.glob("*.md"))
    arquivos = [p for p in arquivos if p.name not in SKIP]

    ok = 0
    erros = 0
    for p in arquivos:
        mudou, content_or_err = migrar_arquivo(p)
        if not mudou and content_or_err.startswith("[ERRO"):
            print(f"  - {p.name}: {content_or_err}")
            erros += 1
            continue
        if args.apply:
            p.write_text(content_or_err, encoding="utf-8")
            print(f"  - {p.name}: aplicado.")
        else:
            print(f"  - {p.name}: pronto (dry-run, nao gravado).")
        ok += 1

    print()
    print(f"Total processado: {ok} arquivos. Erros: {erros}.")
    if not args.apply:
        print("Dry-run. Rode novamente com --apply para gravar.")
    return 0 if erros == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
