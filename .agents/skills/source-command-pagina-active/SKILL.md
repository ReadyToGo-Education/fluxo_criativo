---
name: "source-command-pagina-active"
description: "Conectar uma página de captura HTML ao ActiveCampaign via API. Cadastra o lead na lista certa, dispara a sequência de emails e redireciona para a página de obrigado. Skill de infraestrutura, roda depois da copy da captura estar pronta."
---

# source-command-pagina-active

Use this skill when the user asks to run the migrated source command `pagina-active`.

## Command Template

# Página ActiveCampaign. Integração via API

Pega uma página de captura pronta e conecta ao ActiveCampaign. Quando o lead preenche o formulário, é cadastrado na lista, recebe tag e entra na automação de emails. Sem Zapier, sem plugin, sem servidor próprio.

## Usage

```
/pagina-active
```

## O Que Fazer

Acione a skill `pagina-active` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo`. Se não houver produto, oriente a usar `/produto-novo`.
2. Verificar `ACTIVE_API_URL` e `ACTIVE_API_KEY` no `.env`. Se não existirem, mostrar setup guiado (login no ActiveCampaign, Settings > Developer, copiar URL e Key, colar no chat). Salvar no `.env` silenciosamente.
3. Coletar (uma pergunta por vez): qual página de captura, ID da lista, tag do lead, URL da página de obrigado.
4. Testar a API buscando as listas disponíveis. Se o usuário não souber o ID da lista, mostrar a lista numerada e pedir pra escolher.
5. Injetar um `<script>` no final da página HTML com a função `fetch()` que envia `email` e `first_name` pro endpoint `POST /api/3/contact/sync` do ActiveCampaign, adiciona na lista via `POST /api/3/contactLists`, adiciona tag via `POST /api/3/contactTags` e redireciona pra página de obrigado.
6. Salvar página modificada como `{nome}-active.html` na mesma pasta.
7. Oferecer rodar `/pagina-vercel` pra publicar.

## Regras Resumidas

- Nunca pedir login/senha do ActiveCampaign. Só URL + Key da API.
- A chave nunca aparece no HTML final. Use um endpoint intermediário do próprio ActiveCampaign (CORS habilitado com a key no header) ou instrua o aluno a criar um formulário nativo do ActiveCampaign e embutir via iframe.
- Confirmar antes de modificar a página. Salvar como arquivo novo, nunca sobrescrever a original.
- Validar que `.env` está no `.gitignore`.
- Não usar travessão em nenhum texto exibido.
