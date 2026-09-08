---
name: "source-command-pagina-vercel"
description: "Publicar uma página HTML do projeto direto na Vercel via API e devolver o link público. Inclui setup guiado do token da API. Skill de infraestrutura, última etapa do fluxo de página, depois de copy + performance + pixel + checkout."
---

# source-command-pagina-vercel

Use this skill when the user asks to run the migrated source command `pagina-vercel`.

## Command Template

# Página Vercel. Publicação via API

Publica uma página HTML local diretamente na Vercel e devolve o link público pronto pra usar em anúncios, bio e emails. Sem upload manual, sem Git.

## Usage

```
/pagina-vercel
```

## O Que Fazer

Acione a skill `pagina-vercel` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo`. Se não houver produto, oriente a usar `/produto-novo`.
2. Verificar `VERCEL_API_TOKEN` no `.env`. Se não existir, mostrar setup guiado (cadastro em vercel.com > Settings > Tokens, colar o token no chat). O assistente salva no `.env` automaticamente, nunca pede pro usuário abrir o arquivo.
3. Coletar (uma pergunta por vez): qual página, nome do projeto na Vercel, conta pessoal ou time, modo (novo projeto ou nova versão de projeto existente).
4. Se já existe `meus-produtos/{ativo}/entregas/.vercel` com `project_id`, oferecer publicar nova versão do projeto anterior.
5. Mostrar resumo e pedir confirmação:
   ```
   1. Publicar
   2. Cancelar
   ```
6. Publicar via `curl` POST em `https://api.vercel.com/v13/deployments` com payload no formato `{name, files: [{file, data}], target: "production"}`. Usar arquivo de payload temporário pra evitar problema de tamanho. Apagar depois.
7. Se o deploy voltar como `QUEUED` ou `BUILDING`, fazer polling em `GET /v13/deployments/{id}` até virar `READY` (máximo 30 segundos).
8. Tratar erros de API (até 3 tentativas com ajuste). Se persistir, mostrar erro completo e perguntar como prosseguir.
9. Salvar histórico em `meus-produtos/{ativo}/entregas/.vercel` e atualizar `meus-produtos/{ativo}/entregas/paginas/.vercel-link.md` com o link público.
10. Mostrar resumo final com URL pública (`https://{projeto}.vercel.app`) e sugerir próximos passos: usar o link no `/copy-anuncio` para tráfego pago.

## Regras Resumidas

- Nunca pedir login/senha da Vercel. Só o token da API, colado no chat.
- Nunca expor o token em mensagens, logs ou arquivos fora do `.env`.
- `.env` deve estar no `.gitignore` (validar antes de salvar).
- Sempre confirmar antes de publicar.
- Nome do projeto precisa ser minúsculo, sem acentos, sem espaços. Normalizar silenciosamente se o usuário informar fora do padrão.
- A documentação oficial da Vercel (`vercel.com/docs/rest-api`) é fonte de verdade. Se a chamada falhar, ler o erro e adaptar. Não tentar adivinhar mais de 3 vezes.
- Não usar travessão em nenhum texto exibido.
