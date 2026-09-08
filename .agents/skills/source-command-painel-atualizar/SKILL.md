---
name: "source-command-painel-atualizar"
description: "Atualizar o manifest meus-produtos/index.js que alimenta o painel global painel/index.html. Varre a pasta meus-produtos/ e regenera a lista de produtos, seus nomes e caminhos dos painéis."
---

# source-command-painel-atualizar

Use this skill when the user asks to run the migrated source command `painel-atualizar`.

## Command Template

# Atualizar Manifest do Painel

Regenera o arquivo `meus-produtos/index.js`, que é lido pelo painel global (`painel/index.html`) para listar os produtos e os caminhos dos seus painéis de entregas.

## Quando usar

Rodar esse comando sempre que:

- Você renomeou um produto manualmente no filesystem.
- Você adicionou ou removeu o arquivo `painel-entregas.html` de algum produto sem passar pelo comando `/produto-concepcao`.
- O painel global está mostrando produto errado, painel errado ou diz "Manifest não encontrado".
- Você criou um `nome.txt` novo dentro de algum produto para customizar o display.

Os comandos `/produto-novo`, `/produto-excluir` e `/produto-trocar` **já chamam esse script automaticamente** ao mexer na estrutura. Esse comando é o fallback manual.

## O que fazer

1. Rodar no terminal o script na raiz do projeto:

   ```
   py -3 scripts/painel-atualizar.py
   ```

2. O script:
   - Varre cada subpasta de `meus-produtos/` (ignorando pastas que começam com `_` ou `.`).
   - Para cada produto, descobre o painel: primeiro procura `painel-entregas.html`; se não existir, pega qualquer `painel-*.html`; se nenhum existir, o produto entra no manifest com `url: null` (o painel global mostra aviso amigável).
   - Descobre o nome amigável nessa ordem: arquivo `nome.txt` (se existir) > título do `perfil.md` após separador (`—`, `–`, `-`, `:`) > campo `**Produto ativo:**` no `perfil.md` > slug em Title Case.
   - Lê `meus-produtos/.ativo` pra saber qual produto deve vir selecionado ao abrir o painel.
   - Escreve `meus-produtos/index.js` com `window.MEUS_PRODUTOS = {...}`.

3. Retornar ao aluno:

   ```
   Manifest atualizado.
   Produtos: {total} (com painel: {com}, sem painel: {sem})
   Ativo: {slug ativo}

   Abra painel/index.html na raiz do projeto para ver o resultado.
   ```

## Dica

Pra customizar o nome de exibição de um produto, crie um arquivo `meus-produtos/{slug}/nome.txt` com uma linha só, contendo o nome desejado (com acentos, espaços etc). O script respeita esse arquivo antes de qualquer outra heurística.
