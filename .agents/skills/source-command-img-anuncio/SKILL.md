---
name: "source-command-img-anuncio"
description: "Edita uma imagem de referência que o usuário já tem. Troca personagem, altera texto, altera cor ou faz edição pontual. Executa via skill usar-referencia-visual com OpenRouter (único provider com visão multimodal)."
---

# source-command-img-anuncio

Use this skill when the user asks to run the migrated source command `img-anuncio`.

## Command Template

# Imagem para Anúncio. Referência Visual

Edita uma imagem existente mantendo 100% do layout original. Troca personagem, texto, cor ou faz edição pontual.

## Passo 0. Contexto

Leia `meus-produtos/.ativo`, depois `meus-produtos/{ativo}/perfil.md` e `meus-produtos/{ativo}/idconsumidor.md` se existir.

Extraia internamente: Urgências Ocultas, Quadro, nicho, handle e paleta de cores do produto.

## Passo 1. Execução

Acionar a skill `usar-referencia-visual` para conduzir o fluxo completo:

- Quantidade de imagens (1 = banner, 2+ = carrossel)
- Nome da sessão (cria pasta de trabalho)
- Origem da imagem: link (curl) ou caminho local (cp)
- Modo de edição: trocar personagem, alterar texto, alterar cor, edição pontual
- Execução via `gerar-banner-estatico.py` com OpenRouter

Provider obrigatório: **sempre OpenRouter** (único com visão multimodal).

Arquivos gerados salvos em `meus-produtos/{ativo}/entregas/criativos/`.
