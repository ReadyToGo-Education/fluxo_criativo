# Portabilidade. Rodando o App Pratico em Outro Projeto Fluxo Criativo

Esta skill foi desenhada para viver dentro de qualquer instalacao do
projeto fluxo-criativo (mesma base de produto ativo, `.env`, VTSD e demais
skills). Levar para outra maquina ou outro aluno e so questao de
sincronizar o repositorio (`.claude/skills/app-pratico/`,
`.claude/commands/app-pratico.md`) e conferir as dependencias abaixo.

## O que precisa estar instalado

| Ferramenta | Para que serve | Quando e obrigatorio | Como verificar |
|---|---|---|---|
| Python 3.10+ | Rodar `scripts/cortes_transcrever.py` | Se as aulas estiverem no YouTube (Etapa 1, opcao 1) | `python --version` ou `python3 --version` |
| yt-dlp | Baixar so a legenda automatica das aulas | Se as aulas estiverem no YouTube (Etapa 1, opcao 1) | `yt-dlp --version` |
| `VERCEL_API_TOKEN` no `.env` | Publicar o app pronto | Sempre, na Etapa 9 | A propria Etapa 9 guia o cadastro se faltar |

Nenhuma outra credencial, MCP ou API paga e necessaria. Se as aulas ja
estiverem em texto, PDF ou Word (Etapa 1, opcoes 3 e 4), nem Python nem
yt-dlp sao necessarios, so as skills nativas `anthropic-skills:pdf` e
`anthropic-skills:docx`, que ja vem com qualquer instalacao do Claude Code.

## Passo a passo de instalacao (se faltar algo)

**Windows:**
```
pip install -U yt-dlp
```

**Mac:**
```
brew install yt-dlp
```

**Linux (Debian/Ubuntu):**
```
pip install -U yt-dlp
```

## Pre-requisito de produto

Esta skill sempre parte de um produto ja cadastrado em
`meus-produtos/{slug}/`, com `perfil.md` preenchido. Se o curso ainda nao
foi cadastrado nessa instalacao, rode `/produto-novo` primeiro (ele guia o
cadastro completo, incluindo Quadro, Furadeira e publico, que a Etapa 3
desta skill usa para propor ideias de app relevantes).

## O que NAO precisa refazer em outra instalacao

- Nao precisa reconfigurar nenhuma outra variavel do `.env` alem do
  `VERCEL_API_TOKEN` (e mesmo esse, se a conta Vercel ja tiver token
  salvo de outro uso do `/pagina-vercel`, e so reaproveitar).
- Nao precisa copiar `scripts/cortes_transcrever.py` a parte: se o
  projeto fluxo-criativo foi clonado inteiro, o script ja vem junto (e
  compartilhado com a skill `cortes-live`).
- Nao precisa duplicar regras de acentuacao, mascaramento de token ou
  aprovacao antes de publicar: essas regras ja vem do `CLAUDE.md` da
  instalacao e valem automaticamente para esta skill tambem.
