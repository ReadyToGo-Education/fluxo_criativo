---
name: "source-command-pagina-lovable"
description: "Publicar uma página HTML do projeto direto no Lovable via API e devolver o link público. Inclui setup guiado da chave da API. Skill de infraestrutura, última etapa do fluxo de página, depois de copy + performance + pixel + checkout."
---

# source-command-pagina-lovable

Use this skill when the user asks to run the migrated source command `pagina-lovable`.

## Command Template

# Página Lovable. Publicação via API

Publica uma página HTML local diretamente no Lovable e devolve o link público pronto pra usar em anúncios, bio e emails. Sem upload manual.

## Usage

```
/pagina-lovable
```

## O Que Fazer

Acione a skill `pagina-lovable` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo`. Se não houver produto, oriente a usar `/produto-novo`.
2. Verificar `LOVABLE_API_KEY` no `.env`. Se não existir, mostrar setup guiado (cadastro em lovable.dev > Settings > API Keys, colar a chave no chat). O assistente salva no `.env` automaticamente, nunca pede pro usuário abrir o arquivo.
3. Coletar (uma pergunta por vez): qual página, nome no Lovable, subdomínio (auto ou escolhido), modo (nova ou atualizar página existente).
4. Se já existe `meus-produtos/{ativo}/entregas/.lovable` com `project_id`, oferecer atualizar a versão anterior.
5. Mostrar resumo e pedir confirmação:
   ```
   1. Publicar
   2. Cancelar
   ```
6. Publicar via `curl` POST/PATCH na API do Lovable. Usar arquivo de payload temporário pra evitar problema de tamanho. Apagar depois.
7. Tratar erros de API (até 3 tentativas com ajuste). Se persistir, mostrar erro completo e perguntar como prosseguir.
8. Salvar histórico em `meus-produtos/{ativo}/entregas/.lovable` e atualizar `meus-produtos/{ativo}/entregas/paginas/.lovable-link.md` com o link público.
9. Mostrar resumo final com URL pública e sugerir próximos passos: usar o link no `/copy-anuncio` para tráfego pago.

## Regras Resumidas

- Nunca pedir login/senha do Lovable. Só a API key, colada no chat.
- Nunca expor a chave em mensagens, logs ou arquivos fora do `.env`.
- `.env` deve estar no `.gitignore` (validar antes de salvar).
- Sempre confirmar antes de publicar.
- A documentação oficial do Lovable é fonte de verdade. Se a chamada falhar, ler o erro e adaptar (endpoint, header, payload). Não tentar adivinhar mais de 3 vezes.
- Não usar travessão em nenhum texto exibido.
