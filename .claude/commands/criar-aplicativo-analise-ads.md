---
name: workshop-marketing:criar-aplicativo-analise-ads
description: Guia passo a passo para criar um App no Facebook Developers com acesso à Marketing API, necessário para gerar o token de acesso ao Facebook Ads.
allowed-tools: Read, Write, Edit, Glob, Bash, WebFetch, WebSearch
---

# Criar Aplicativo de Análise de Ads no Facebook

Guia para criar o App no Facebook Developers. So precisa fazer uma vez. O App e o que permite gerar o token de acesso a Marketing API.

---

## Fluxo de criacao (5 etapas)

Acesse developers.facebook.com e faca login com a conta de admin do negocio. Clique em "Meus Apps" > "Criar App".

**Etapa 1. Detalhes do app**
- Nome do app: use "Relatorio de Anuncios" ou qualquer nome simples
- Email de contato: ja vem preenchido com o email do Facebook, pode deixar como esta
- Clique em "Avancar"

**Etapa 2. Casos de uso (passo crítico)**
- A tela abre com o filtro "Em Destaque" selecionado, mostrando apenas 6 opcoes
- Troque o filtro para "Tudo" para ver todas as opcoes disponiveis
- Selecione TODOS os 7 casos de uso abaixo (marcar o checkbox de cada um):
  1. Criar e gerenciar anúncios com a API de Marketing
  2. Mensurar dados de desempenho do anúncio com a API de Marketing
  3. Capturar e gerenciar leads de anúncios com a API de Marketing
  4. Criar e gerenciar anúncios de apps com o Gerenciador de Anúncios da Meta
  5. Anuncie no seu app com o Meta Audience Network
  6. Gerenciar mensagens e conteúdo no Instagram
  7. Gerenciar tudo na sua Página
- Clique em "Avancar"

> **Atenção, marque os 7.** Os 4 primeiros (com a palavra "Marketing") liberam a Marketing API que é o que permite puxar métricas e gerar relatórios. Os 3 últimos (Audience Network, Instagram, Página) liberam endpoints adicionais que skills futuras vão precisar (postagem programada no Instagram, leitura de página, monetização). Se faltar algum, depois precisa recriar o App, então marca todos agora.

**Etapa 3. Empresa**
- Selecione o Portfolio Empresarial (Business Manager) que contem a conta de anuncios que voce quer monitorar
- Se nao aparecer nenhuma opcao, verifique se esta logado com a conta de admin do BM
- Clique em "Avancar"

**Etapa 4. Requisitos**
- Nenhuma acao necessaria nessa tela
- Clique em "Avancar"

**Etapa 5. Visao geral**
- Revise as informacoes do app
- Clique em "Criar Aplicativo"

---

## Apos criar o App: configurar e publicar

**Passo 1. Adicionar politica de privacidade**
- No menu lateral do app, clique em "Configuracoes do App" > "Basico"
- No campo "URL da Politica de Privacidade", cole a URL da pagina de politica de privacidade do negocio
- A URL precisa ser real e acessivel (nao aceita placeholder)
- Se nao tiver uma pagina de politica pronta, pode usar o link da pagina de politica do site existente, ou criar uma pagina simples no Notion, Google Sites ou similar
- Clique em "Salvar alteracoes"

**Passo 2. Publicar o app**
- No menu lateral, clique em "Publicar"
- Clique no botao "Publicar"
- O app precisa estar publicado para que o token funcione corretamente

---

## Apos criar o App: gerar o token de acesso

Execute a skill `gerar-token-permanente-facebook-ads`. Ela guia o usuario pelo processo completo de criacao do Usuario do Sistema, atribuicao de ativos (conta de anuncios, App, Pagina, Instagram), geracao do token permanente e validacao com 3 testes na Graph API.

Ao final, ela ja encadeia em `obter-id-conta-anuncios` para localizar e salvar o ID da conta de anuncios em `FB_AD_ACCOUNT_ID` no `.env`.

---

## Se o usuario nao encontrar alguma opcao

Use `WebFetch` para buscar a documentacao atualizada antes de responder:

```
URL 1: https://developers.facebook.com/docs/marketing-apis/get-started
URL 2: https://developers.facebook.com/docs/marketing-api/system-users
```

Se as URLs retornarem erro ou conteudo vago, use WebSearch com a query: `site:developers.facebook.com marketing api access token tutorial`

Adapte as instrucoes com base no conteudo retornado. Nao cite que buscou na documentacao.
