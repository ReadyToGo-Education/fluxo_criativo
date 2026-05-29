---
name: workshop-marketing:gerar-token-permanente-facebook-ads
description: Guia para gerar token permanente de acesso ao Facebook Ads via Usuário do Sistema no Business Manager. Token nunca expira e não precisa ser renovado.
allowed-tools: Read, Write, Edit, Glob, Bash, WebFetch, WebSearch
model: sonnet
---

# Gerar Token Permanente do Facebook Ads

Token via Usuario do Sistema. Nao expira. Nao precisa renovar.

Prerequisito: ter o App criado conforme a skill `criar-aplicativo-analise-ads`.

---

## Passo 1. Criar o Usuario do Sistema

- Acesse business.facebook.com/latest/settings
- No menu lateral, em "Usuarios", clique em "Usuarios do sistema"
- No canto superior direito, clique em "Adicionar"
- Na tela que abrir:
  - Nomeie o usuario: use "relatorio-ads" (sem espaço, tudo minúsculo). O Facebook não aceita espaço nem maiúscula nesse campo
  - Em "System user role", selecione "Admin"
  - Clique em "Adicionar"

---

## Passo 2. Atribuir Ativos ao Usuario

Com o usuario do sistema criado e selecionado, clique em "Atribuir Ativos". Uma tela vai abrir com menu lateral. Faca as atribuicoes abaixo na ordem:

**Contas de anuncio (a tela ja abre aqui):**
- A tela abre diretamente em "Contas de anuncio"
- Selecione todas as contas que deseja monitorar
- Ative "Controle total" em cada uma
- Clique em "Atribuir ativos"

**Apps:**
- No menu lateral, clique em "Apps"
- Selecione o app criado ("Relatorio de Anuncios" ou o nome que usou)
- Ative "Controle total"
- Clique em "Atribuir ativos"

**Páginas (obrigatório se for criar ou analisar criativos):**
- No menu lateral, clique em "Páginas"
- Selecione a página do Facebook conectada à conta de anúncios
- Ative "Criar conteúdo" e "Anúncios"
- Clique em "Atribuir ativos"

**Contas do Instagram (se houver perfil comercial vinculado):**
- No menu lateral, clique em "Contas do Instagram"
- Selecione o perfil do Instagram vinculado à página
- Ative "Anúncios"
- Clique em "Atribuir ativos"

**Conjuntos de dados (Pixel e Conversions API):**
- No menu lateral, clique em "Conjuntos de dados" (antigo "Fontes de dados" ou "Pixels")
- Selecione o conjunto de dados do negócio (o Pixel principal vinculado à conta de anúncios)
- Ative "Gerenciar conjunto de dados" (controle total) ou no mínimo "Visualizar conjunto de dados" + "Enviar eventos"
- Clique em "Atribuir ativos"

> **Atenção, esses três últimos passos são os mais esquecidos da configuração.** Sem a Página atribuída, o token funciona em testes simples como `GET /me`, mas dá erro de permissão na hora de subir criativo, disparar relatório que cruza dados de página, ou puxar insights de Reels. Sem o Conjunto de dados, qualquer chamada que envolva eventos do Pixel ou Conversions API (envio de eventos server-side, leitura de qualidade de eventos, deduplicação) volta erro 200 de permissão. Se o anunciante não usa Instagram, o passo do Instagram pode ser pulado, mas Páginas e Conjuntos de dados são obrigatórios.

---

## Passo 3. Gerar o Token

- Ao lado do nome do usuario de sistema, clique em "Gerar token"
- Uma tela com 4 etapas vai abrir:

**Etapa 1. Selecionar app**
- Selecione o app criado ("Relatorio de Anuncios")
- Clique em "Avancar"

**Etapa 2. Definir expiracao**
- Selecione "Nunca" (nao selecione "60 dias" para evitar manutencao futura)
- Clique em "Avancar"

> **O que "Nunca" significa de verdade.** O token não expira por tempo, mas pode ser revogado pela Meta em alguns cenários: troca da senha do admin que criou o usuário do sistema, troca do segredo do app, mudanças nas permissões do Business Manager, ou inatividade prolongada (raro). Recomendação de higiene: gerar um token novo a cada 6 meses, mesmo sem aviso de erro. Se um teste de validação retornar erro 190 lá na frente, o caminho é repetir esse Passo 3, não recriar o usuário do sistema nem o app.

**Etapa 3. Atribuir permissoes**

Marque TODOS os escopos que aparecerem na tela (selecionar tudo). O Facebook só mostra os escopos que são compatíveis com os casos de uso que foram selecionados na criação do App, então não tem risco de marcar algo que não deveria. Liberar tudo evita ter que voltar aqui depois para regerar o token quando uma skill nova precisar de um escopo que não foi marcado da primeira vez.

Para referência, os escopos principais que as skills do projeto usam são:

| Escopo | Para que serve |
|---|---|
| `ads_management` | Criar e gerenciar campanhas, conjuntos e anuncios |
| `ads_read` | Ler dados de anuncios e metricas |
| `business_management` | Acesso ao Business Manager e ativos |
| `read_insights` | Buscar relatorios e insights de desempenho |
| `pages_read_engagement` | Dados de engajamento de paginas vinculadas |
| `pages_show_list` | Listar paginas vinculadas ao negocio |
| `catalog_management` | Gerenciar catalogos de produtos |
| `instagram_basic` | Ler dados básicos do perfil Instagram vinculado |
| `instagram_content_publish` | Publicar conteúdo no Instagram via API |

Não precisa identificar um por um. É só marcar a opção "Selecionar tudo" no topo da lista (se existir) ou marcar todos os checkboxes manualmente.

- Clique em "Gerar token"

**Etapa 4. Concluir**
- O token vai aparecer na tela
- Copie o token e guarde em um lugar seguro (ele nao aparece novamente)
- Clique em "Concluir"

---

## Passo 4. Validar o token (3 testes)

Execute os três testes abaixo, **um por vez, em chamadas Bash separadas**. Os três precisam passar. Se qualquer um falhar, consulte o **Mapa de erros** logo abaixo antes de pedir ajuda.

> ### ⚙️ Como executar (regra dura para a skill)
>
> **Cada teste é uma chamada `Bash` independente.** Substituir `TOKEN` pelo valor literal **inline na URL** do `curl`. NÃO empacotar os 3 testes num script multi-linha com `TOKEN="..."` no início + `echo` + múltiplos `curl`. Esse formato (script bash com variável shell) **não casa** com os padrões `Bash(curl -s "https://graph.facebook.com/*)` autorizados no `.claude/settings.local.json` e dispara o pop-up nativo de permissão — que exibe o token completo na tela.
>
> Formato CORRETO (3 chamadas Bash independentes, cada uma um único `curl` com token inline):
>
> ```
> curl -s "https://graph.facebook.com/v25.0/me?access_token=<TOKEN_DO_ENV>"
> ```
> ```
> curl -s "https://graph.facebook.com/v25.0/me/adaccounts?access_token=<TOKEN_DO_ENV>"
> ```
> ```
> curl -s "https://graph.facebook.com/v25.0/act_<id>/campaigns?limit=1&access_token=<TOKEN_DO_ENV>"
> ```
>
> Formato ERRADO (script multi-linha, dispara pop-up com token visível):
>
> ```
> TOKEN="EAA..."
> echo "==== TESTE 1 ===="
> curl -s "https://graph.facebook.com/v25.0/me?access_token=${TOKEN}"
> echo ""
> echo "==== TESTE 2 ===="
> curl -s "https://graph.facebook.com/v25.0/me/adaccounts?access_token=${TOKEN}"
> ```
>
> A diferença pro aluno: o formato CORRETO roda direto sem balão de permissão. O formato ERRADO exibe o token na tela e exige clique manual.
>
> Após cada chamada, mostrar a resposta resumida ao aluno (sucesso/erro), seguindo a regra de mascaramento de tokens do CLAUDE.md (não ecoar a URL completa com o token na resposta — descrever em linguagem natural: "Teste 1 passou: token responde como `relatorio-ads` em /me").

Substitua `TOKEN` pelo token copiado e `SEU_AD_ACCOUNT_ID` pelo número da conta de anúncios (só os números, sem o prefixo `act_`).

**Teste 1. Token está válido**

```bash
curl "https://graph.facebook.com/v25.0/me?access_token=TOKEN"
```

Esperado: `{"id":"...","name":"relatorio-ads"}` (ou o nome que deu ao usuário do sistema). Se vier erro, o token foi copiado errado ou já está revogado.

**Teste 2. Usuário do sistema enxerga a conta de anúncios**

```bash
curl "https://graph.facebook.com/v25.0/me/adaccounts?access_token=TOKEN"
```

Esperado: lista contendo `act_<seu_ad_account_id>`. Se vier vazio ou sem a conta esperada, a atribuição da conta no Passo 2 não foi feita corretamente, refaça aquele passo.

**Teste 3. Permissão de leitura na conta funciona de verdade**

```bash
curl "https://graph.facebook.com/v25.0/act_SEU_AD_ACCOUNT_ID/campaigns?limit=1&access_token=TOKEN"
```

Esperado: um objeto `data` com 1 campanha (se a conta tiver), ou `data: []` (se a conta for nova). Em ambos os casos, sem mensagem de erro.

Os três testes passaram? Token validado, siga para a próxima seção. Se algum falhou, consulte o Mapa de erros abaixo.

---

## Mapa de erros comuns

Quando algum teste falhar, identifique o erro abaixo e siga a recomendação. Não chute, siga o mapa.

| Código do erro | Causa provável | Solução |
|---|---|---|
| `190 — Invalid OAuth access token` | Token errado, copiado parcialmente, ou já revogado | Voltar ao Passo 3 e gerar de novo. Tokens da Meta têm 200+ caracteres, conferir se copiou o token inteiro |
| `200 — Permissions error` (ou `(#200) ...`) | Token válido, mas o usuário do sistema não tem o ativo atribuído | Voltar ao Passo 2 e confirmar as permissões certas em cada bloco. Conta de anúncios: "Controle total". App: "Controle total". Páginas: "Criar conteúdo" + "Anúncios". Instagram: "Anúncios" |
| `100 — Invalid parameter` (geralmente o `ad_account_id`) | Prefixo `act_` no lugar errado | No `.env`, salvar só os números. Na URL do curl, prefixar com `act_`. Ex: `.env` tem `1234567890`, URL fica `act_1234567890` |
| `10 — Application does not have permission` | App sem o caso de uso "Marketing API" ou usuário do sistema sem o app atribuído | Voltar à skill `criar-aplicativo-analise-ads` (confirmar caso de uso) e ao Passo 2 daqui (confirmar app com Controle total) |
| `4 — Application request limit reached` | Rate limit do app (acontece se o app está em modo Desenvolvimento com volume alto) | Aguardar 1 hora. Se persistir, publicar o app (precisa da política de privacidade configurada) |
| `17 — User request limit reached` | Muitas chamadas em pouco tempo com esse token | Aguardar e implementar pausa entre chamadas. Não regerar o token, não resolve |
| `appsecret_proof` exigido mas não enviado | App Secret Proof ativado nas Configurações Avançadas, mas o curl manual não envia o proof | Para teste manual, desativar temporariamente em Configurações → Avançado do app, fazer os testes, religar. O Meta Ads CLI calcula o proof automaticamente, em uso real não precisa desligar |

Se a tela do Business Manager não bater com este roteiro, descreva o que está vendo (menus na lateral, botões na página). A Meta atualiza a UI sem aviso, e o roteiro pode estar uma versão atrás.

---

## Apos validar o token

Salve o token no `.env` com os nomes exatos:

```
FB_ACCESS_TOKEN_PERMANENTE=seu_token_aqui
META_AUTH_MODO=APP
```

Use `Edit` cirurgico para adicionar ou atualizar essas linhas no `.env`. Nao sobrescreva outras variaveis.

> **Por que `META_AUTH_MODO=APP`:** as skills `/trafego-*` leem essa variavel no Passo 0 para decidir como se conectar com o Meta Ads. Sem ela, qualquer skill de trafego para no gate e manda o aluno rodar `/trafego-conexao` mesmo com o token e ad account ja configurados. Salvar `APP` aqui evita esse desvio.

---

## Passo 5. Buscar contas de anuncio automaticamente (OBRIGATORIO)

> Esta etapa NUNCA deve ser pulada. Logo apos salvar o token no `.env`, faca a requisicao abaixo SEM perguntar ao usuario, listando todas as contas que o token enxerga.

Execute via Bash com curl, substituindo `TOKEN_AQUI` pelo token recem-salvo:

```bash
curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name,account_status,currency,business_name&limit=100&access_token=TOKEN_AQUI"
```

**Mapeamento de status (`account_status`):**
- `1` = Ativa
- `2` = Desabilitada
- `3` = Sem conformidade
- `7` = Pendente de risco
- `9` = Em revisao
- `100` = Pendente de fechamento
- `101` = Fechada
- `201` = Qualquer outro motivo de inatividade

**Regras de tratamento de erro:**
- Se vier 0 contas, avisar que o usuario do sistema nao tem nenhuma conta atribuida e mandar de volta para o Passo 2 (atribuir ativos).
- Se vier erro 190 ou 200, consultar o Mapa de erros acima e ajustar o token ou as permissoes antes de tentar de novo.

---

### Caso A. Token retorna 1 conta

Salvar direto, sem perguntar nada ao usuario. No `.env`, usar `Edit` cirurgico para adicionar ou atualizar:

```
FB_AD_ACCOUNT_ID={apenas_numeros}
FB_AD_ACCOUNT_IDS={apenas_numeros}
```

Avisar o usuario:

```
Conta unica detectada: {nome} ({id}). Salva como padrao.
```

---

### Caso B. Token retorna 2 ou mais contas

Mostrar a tabela completa:

```
Contas de anuncio encontradas:

| # | Nome | ID | Moeda | Status |
|---|---|---|---|---|
| 1 | {nome} | {account_id} | {currency} | {Ativa/Inativa} |
| 2 | {nome} | {account_id} | {currency} | {Ativa/Inativa} |
...
```

**Pergunta 1 (multi-selecao):**

```
Quais contas quer salvar no projeto? Digite os numeros separados por virgula
(ex: 1,3,5) ou "todas" para salvar todas.
```

Aguardar resposta. Validar que pelo menos 1 numero foi escolhido. Filtrar contas inativas se o usuario incluiu alguma e avisar antes de salvar.

**Pergunta 2 (default):**

```
Qual delas e a padrao? Sera usada nos relatorios automaticos quando nenhuma
for especificada. Digite o numero:
```

Aguardar resposta. O numero precisa estar dentro das contas salvas no passo anterior.

**Salvar no `.env`:**

Usar `Edit` cirurgico para adicionar ou atualizar as duas variaveis:

```
FB_AD_ACCOUNT_ID={id_da_conta_default}
FB_AD_ACCOUNT_IDS={id_1},{id_2},{id_3}
```

Regras de formato:
- Apenas numeros, SEM o prefixo `act_`.
- `FB_AD_ACCOUNT_IDS` separado por virgula sem espaco.
- O `FB_AD_ACCOUNT_ID` (padrao) precisa aparecer tambem dentro de `FB_AD_ACCOUNT_IDS`.

---

### Confirmacao final

Apos salvar, confirmar com o usuario EXATAMENTE com o bloco abaixo, nada mais:

```
✅ Salvo no .env:
- META_AUTH_MODO = APP
- FB_ACCESS_TOKEN_PERMANENTE = (token salvo, mascarado)
- FB_AD_ACCOUNT_ID = {id_default} ({nome_default})
- FB_AD_ACCOUNT_IDS = {n} contas salvas

Tudo pronto. As skills /trafego-* já conseguem acessar o Meta Ads.

Você pode trocar a conta padrão depois com /meta-conta-trocar.
Você pode adicionar mais contas com /meta-conta-adicionar.
```

> **Regra dura — não expandir esta saída.** Não acrescentar lista de "Próximas skills disponíveis", não categorizar em "Tráfego pago", "Operacional do Meta", "Relatórios e otimização atalho" nem variantes parecidas, não citar `/trafego-insights`, `/trafego-criar-campanha`, `/trafego-otimizar`, `/trafego-escalar`, `/trafego-analise`, `/ads-relatorio`, `/enviar-relatorio-ads`, `/lt-otimizar` ou qualquer outra skill aqui. Recomendação de "próximo passo" é responsabilidade exclusiva de `/trafego-conexao` (que é o ponto de entrada e tem o bloco `🔭 Próximo passo recomendado`). Esta skill é só infraestrutura técnica de geração de token; encerra com a confirmação acima e ponto.

---

## Quando a tela do Business Manager estiver diferente

Se o usuario disser que nao encontrou alguma opcao ou que a tela esta diferente, use WebFetch para buscar a documentacao atualizada:

```
https://developers.facebook.com/docs/marketing-api/system-users
```

Adapte as instrucoes com base no conteudo retornado. Nao cite que buscou na documentacao.
