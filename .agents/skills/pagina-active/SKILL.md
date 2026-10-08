---
name: pagina-active
description: >
  Conecta uma página de captura HTML ao ActiveCampaign via API. Cadastra o
  lead na lista certa, aplica tag, dispara a automação de emails e redireciona
  pra página de obrigado. Skill de infraestrutura. Roda depois que a copy da
  página de captura estiver pronta e antes de publicar.
---

# Página ActiveCampaign. Integração via API

Pega uma página de captura já pronta (HTML local) e faz a integração completa com o ActiveCampaign. Quando o visitante preenche o formulário, o contato é criado, adicionado à lista, recebe uma tag e é redirecionado pra página de obrigado. Sem Zapier, sem plugin do WordPress, sem complicação.

## Quando Usar

- Depois de gerar a página de captura com `/copy-pagina`.
- Quando o usuário disser "conecta essa captura com o ActiveCampaign", "quero integrar com o Active", "preciso que o lead caia no Active".
- Antes de publicar a página via `/pagina-vercel`.

## O Que Fazer

### 0. Contexto e verificação de API

Leia `entregas/.ativo`. Se não houver produto, oriente a rodar `/produto-novo` antes.

**Verificar credenciais do ActiveCampaign:**

Leia `.env` e procure `ACTIVE_API_URL` e `ACTIVE_API_KEY`.

**Cenário A. Existem e não estão vazios.** Siga em frente.

**Cenário B. Não existem ou estão vazios.**

Mostre o setup guiado:
```
Pra integrar com o ActiveCampaign preciso de duas informações:

1. Acesse sua conta em https://www.activecampaign.com
2. Vá em Settings > Developer
3. Copie a API URL (algo como https://SUACONTA.api-us1.com)
4. Copie a API Key
5. Cola aqui no chat primeiro a URL, depois a Key

Não abra o .env, eu salvo as duas pra você.
```

Quando o usuário colar, valide que a URL começa com `https://` e termina com `.api-us1.com` (ou equivalente), salve `ACTIVE_API_URL=...` e `ACTIVE_API_KEY=...` no `.env`, verifique que `.env` está no `.gitignore`, e confirme "Credenciais salvas. Pronto pra integrar."

### 1. Coletar dados (uma pergunta por vez)

**Pergunta 1. Qual página de captura vou conectar?**
1. Última página de captura salva em `entregas/{ativo}/paginas/`
2. Outra (informar caminho)

**Pergunta 2. Qual lista do ActiveCampaign esse lead deve entrar?**

Antes de perguntar, faça uma chamada `GET {ACTIVE_API_URL}/api/3/lists` com header `Api-Token: {ACTIVE_API_KEY}` pra listar as listas disponíveis. Mostre numeradas:
```
Suas listas no ActiveCampaign:

1. Leads Gerais (id 1)
2. Curso de Inglês (id 5)
3. VIP (id 8)

Qual a lista alvo?
```

**Pergunta 3. Que tag aplicar no lead?**
(ex: `captura-ebook-ingles`, `webinar-gratuito`)

**Pergunta 4. Qual a URL da página de obrigado?**
Se já existe uma em `entregas/{ativo}/paginas/`, oferecer usar ela (caminho relativo ou URL pública se já estiver publicada).

### 2. Decidir o modo de integração

A API do ActiveCampaign exige que a API Key vá no header, o que significa que **não dá pra chamar direto do front-end** sem expor a chave. Duas opções:

**Opção A. Formulário nativo do ActiveCampaign (recomendada).**
Pedir pro aluno criar um formulário dentro do ActiveCampaign (Site > Forms), associar à lista certa e aplicar a tag. Depois, pegar o código embed do formulário e inserir no lugar do `<form>` da página. Essa é a opção mais segura, sem vazamento de chave, e é o caminho oficial.

**Opção B. Endpoint intermediário (Serverless Function).**
Criar uma função serverless no Vercel (`entregas/{ativo}/paginas/api/active-sync.js`) que recebe `{email, first_name, list, tag}` do front, chama a API do ActiveCampaign pelo servidor (com a chave como variável de ambiente na Vercel, nunca no HTML) e devolve sucesso/erro. O `<form>` da página faz `fetch('/api/active-sync', {...})`.

Pergunte qual modo preferir. Padrão: Opção A (mais simples e segura).

### 3. Aplicar a integração

**Modo A (formulário nativo):**
1. Peça o HTML do formulário embed (aluno cola no chat).
2. Localize o `<form>...</form>` da página de captura e substitua pelo embed do ActiveCampaign, mantendo as classes CSS do formulário original pra preservar o design.
3. Ajuste o redirect no painel do ActiveCampaign (Forms > Options > Thank You Page URL) pra URL informada.

**Modo B (serverless):**
1. Gere o arquivo `entregas/{ativo}/paginas/api/active-sync.js` com o código Node.js que usa `fetch` pra chamar `POST /api/3/contact/sync`, `POST /api/3/contactLists` e `POST /api/3/contactTags` do ActiveCampaign.
2. Injete no HTML da página um `<script>` que intercepta o submit do form, faz `fetch('/api/active-sync', { method: 'POST', body: JSON.stringify({...}) })`, e em sucesso redireciona pra página de obrigado.
3. Salve a página modificada como `entregas/{ativo}/paginas/{nome-original}-active.html`.
4. Instrua o aluno a adicionar `ACTIVE_API_URL` e `ACTIVE_API_KEY` nas Environment Variables do projeto na Vercel (mostrar caminho exato no painel da Vercel).

### 4. Teste e entrega

Mostre resumo final:
```
Pronto. Página conectada ao ActiveCampaign.

Modo:            {A / B}
Página:          {caminho}
Lista:           {nome} (id {id})
Tag:             {tag}
Obrigado:        {url}

Próximo passo:
- Publique com /pagina-vercel
- Teste preenchendo o formulário com um email seu
- Confira no ActiveCampaign se o contato caiu na lista
```

## Regras

- Nunca colocar a API Key direto no HTML final. Se for Opção B, a chave só vai na Vercel como variável de ambiente.
- Sempre confirmar antes de modificar a página. Salvar versão nova, não sobrescrever original.
- Se a API do ActiveCampaign retornar 401 ou 403, avisar que a chave tá inválida e pedir nova.
- Validar que `.env` está no `.gitignore` antes de salvar credenciais.
- A documentação oficial do ActiveCampaign (`developers.activecampaign.com/reference`) é a fonte de verdade. Se a chamada falhar, ler o erro e adaptar.
- Não usar travessão em nenhum texto exibido.
