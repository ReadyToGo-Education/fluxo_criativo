---
name: "source-command-gerar-token-permanente-facebook-ads"
description: "Guia para gerar token permanente de acesso ao Facebook Ads via Usuário do Sistema no Business Manager. Token nunca expira e não precisa ser renovado."
---

# source-command-gerar-token-permanente-facebook-ads

Use esta skill quando o usuário pedir o comando `/gerar-token-permanente-facebook-ads` do workshop (ou `gerar-token-permanente-facebook-ads`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/gerar-token-permanente-facebook-ads.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Gerar Token Permanente do Facebook Ads

Token via Usuario do Sistema. Nao expira. Nao precisa renovar.

Pré-requisito: ter o App criado conforme a skill `criar-aplicativo-analise-ads`.

Quando o App e o Usuário do Sistema já existem (o `/trafego-conexao` aciona este command assim para gerar um token novo, por exemplo no modo `APP` com o token ausente), começar direto pelo Passo 3. Os Passos 1 e 2 só entram se o aluno disser que não tem mais o Usuário do Sistema ou se um teste der erro de permissão.

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

**Antes dos testes, gravar só o token no `.env`**, sem abrir o arquivo, com o padrão do item 4 da seção "LEITURA SEGURA DO .env" do CLAUDE.md, em duas chamadas `Bash`. O token antigo não é apagado agora: ele fica guardado como `FB_ACCESS_TOKEN_ANTERIOR` até os 3 testes passarem. Assim, quem já tinha um token funcionando (troca de higiene a cada 6 meses ou opção "Gerar um token novo" do `/trafego-conexao`) não fica sem acesso se colar o novo pela metade ou desistir no meio.

A primeira chamada, sem o token, garante a quebra de linha, guarda a linha antiga com o outro nome (só se ainda não houver cópia guardada, para uma nova tentativa não trocar o token bom pelo que falhou) e apaga a linha do token. Na primeira vez, quando o `.env` não tem nenhuma linha `FB_ACCESS_TOKEN_PERMANENTE`, não há o que guardar: a chamada grava `FB_ACCESS_TOKEN_ANTERIOR=` vazia, só como marca de que não havia token antes (a linha vazia que vem do `.env.example` vira a mesma marca). Assim, numa nova tentativa, o token que falhou também não vira cópia:

```bash
touch .env && { [ -z "$(tail -c1 .env)" ] || echo >> .env; } && { grep -q "^FB_ACCESS_TOKEN_ANTERIOR=" .env || sed -i 's/^FB_ACCESS_TOKEN_PERMANENTE=/FB_ACCESS_TOKEN_ANTERIOR=/' .env; } && { grep -q "^FB_ACCESS_TOKEN_ANTERIOR=" .env || echo "FB_ACCESS_TOKEN_ANTERIOR=" >> .env; } && sed -i '/^FB_ACCESS_TOKEN_PERMANENTE=/d' .env
```

A segunda só acrescenta o token colado pelo aluno. É a única chamada em que o valor aparece no texto de um comando (exceção do item 4 do CLAUDE.md): nada mais vai nela, e o valor nunca é repetido na resposta.

```bash
printf 'FB_ACCESS_TOKEN_PERMANENTE=%s\n' "<token colado pelo aluno>" >> .env
```

No Mac, trocar `sed -i` por `sed -i ''`. Confirmar só com "token salvo", sem repetir o valor. `META_AUTH_MODO=APP` só é gravado depois que os 3 testes passarem. Depois dos testes:

- **Os três passaram:** apagar a cópia com `sed -i '/^FB_ACCESS_TOKEN_ANTERIOR=/d' .env` (seção "Após validar o token").
- **Algum falhou e o aluno vai gerar outro token:** gravar de novo com as mesmas duas chamadas. A cópia guardada continua intacta.
- **O aluno desistiu:** antes, conferir se havia token com `grep -q "^FB_ACCESS_TOKEN_ANTERIOR=[^[:space:]]" .env && echo "havia" || echo "primeira vez"`. Depois, apagar o token novo, apagar a marca vazia (primeira vez) e devolver o token de antes, se havia um: `sed -i '/^FB_ACCESS_TOKEN_PERMANENTE=/d' .env && sed -i '/^FB_ACCESS_TOKEN_ANTERIOR=[[:space:]]*$/d' .env && sed -i 's/^FB_ACCESS_TOKEN_ANTERIOR=/FB_ACCESS_TOKEN_PERMANENTE=/' .env`. Avisar em 1 linha: se havia, que o token anterior voltou a valer; se era a primeira vez, que o token novo foi apagado e nada mais mudou no `.env`.

Execute os três testes abaixo, **um por vez, em chamadas Bash separadas**. Os três precisam passar. Se qualquer um falhar, consulte o **Mapa de erros** logo abaixo antes de pedir ajuda.

> ### ⚙️ Como executar (regra dura para a skill)
>
> **Cada teste é uma chamada `Bash` independente, com o token entrando por substituição dentro do próprio `curl`** (`$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)`), lido do `.env` gravado logo acima. Nunca colar o valor do token na URL. NÃO empacotar os 3 testes num script multi-linha com `TOKEN="..."` no início + `echo` + múltiplos `curl`: esse formato dispara o pop-up nativo de permissão, que exibe o token completo na tela.
>
> Formato CORRETO (3 chamadas Bash independentes, cada uma um único `curl` com o token por substituição):
>
> ```
> curl -s "https://graph.facebook.com/v25.0/me?access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
> ```
> ```
> curl -s "https://graph.facebook.com/v25.0/me/adaccounts?access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
> ```
> ```
> curl -s "https://graph.facebook.com/v25.0/act_<id>/campaigns?limit=1&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
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
> A diferença para o aluno: nos testes, no formato CORRETO, o token nunca aparece no texto do comando, nem quando o Claude pede permissão para rodar. O formato ERRADO exibe o token na tela e exige clique manual.
>
> Após cada chamada, mostrar a resposta resumida ao aluno (sucesso/erro), seguindo a regra de mascaramento de tokens do CLAUDE.md (não ecoar a URL completa com o token na resposta — descrever em linguagem natural: "Teste 1 passou: token responde como `relatorio-ads` em /me").

No Teste 3, substitua `SEU_AD_ACCOUNT_ID` pelo número de uma conta que apareceu no Teste 2 (só os números, sem o prefixo `act_`).

**Teste 1. Token está válido**

```bash
curl -s "https://graph.facebook.com/v25.0/me?access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

Esperado: `{"id":"...","name":"relatorio-ads"}` (ou o nome que deu ao usuário do sistema). Se vier erro, o token foi copiado errado ou já está revogado.

**Teste 2. Usuário do sistema enxerga a conta de anúncios**

```bash
curl -s "https://graph.facebook.com/v25.0/me/adaccounts?access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

Esperado: lista contendo `act_<seu_ad_account_id>`. Se vier vazio ou sem a conta esperada, a atribuição da conta no Passo 2 não foi feita corretamente, refaça aquele passo.

**Teste 3. Permissão de leitura na conta funciona de verdade**

```bash
curl -s "https://graph.facebook.com/v25.0/act_SEU_AD_ACCOUNT_ID/campaigns?limit=1&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
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

## Após validar o token

O token já foi gravado antes dos testes. Primeiro, apague a cópia do token anterior (`sed -i '/^FB_ACCESS_TOKEN_ANTERIOR=/d' .env`). Depois, grave o modo no `.env`:

```
META_AUTH_MODO=APP
```

Use o comando de uma linha do item 4 da seção "LEITURA SEGURA DO .env" do CLAUDE.md, sem abrir o `.env` com Read, Edit ou Write. Não sobrescreva outras variáveis.

> **Por que `META_AUTH_MODO=APP`:** as skills `/trafego-*` leem essa variavel no Passo 0 para decidir como se conectar com o Meta Ads. Sem ela, qualquer skill de trafego para no gate e manda o aluno rodar `/trafego-conexao` mesmo com o token e ad account ja configurados. Salvar `APP` aqui evita esse desvio.

---

## Passo 5. Buscar contas de anuncio automaticamente (OBRIGATORIO)

> Esta etapa NUNCA deve ser pulada. Logo depois que os 3 testes passarem e o modo for gravado, faça a requisição abaixo SEM perguntar ao usuário, listando todas as contas que o token enxerga.

Execute via Bash com curl, com o token entrando por substituição, lido do `.env` (mesmo padrão dos testes e da seção 4.3 da SKILL `trafego-conexao`):

```bash
curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name,account_status,currency,business_name&limit=100&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
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

Salvar direto, sem perguntar nada ao usuário. No `.env`, gravar cada variável com o comando de uma linha do item 4 da seção "LEITURA SEGURA DO .env" do CLAUDE.md, sem abrir o arquivo:

```
FB_AD_ACCOUNT_ID={apenas_numeros}
FB_AD_ACCOUNT_IDS={apenas_numeros}
```

Avisar o usuário:

```
Conta única detectada: {nome} ({id}). Salva como padrão.
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

Gravar as duas variáveis com o comando de uma linha do item 4 da seção "LEITURA SEGURA DO .env" do CLAUDE.md (um comando por variável), sem abrir o arquivo:

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

Você pode trocar a conta padrão depois com /trafego-conexao.
```

> **Regra dura: não expandir esta saída.** Não acrescentar lista de "Próximas skills disponíveis", não categorizar em "Tráfego pago", "Operacional do Meta", "Relatórios e otimização atalho" nem variantes parecidas, não citar `/trafego-insights`, `/trafego-criar-campanha`, `/trafego-otimizar`, `/trafego-escalar`, `/trafego-analise`, `/trafego-diagnostico`, `/trafego-criativos`, `/trafego-oferta-funil`, `/trafego-pixel`, `/trafego-publicos`, `/trafego-regras`, `/trafego-testes`, `/trafego-dashboard`, `/ads-relatorio`, `/enviar-relatorio-ads`, `/lt-otimizar` ou qualquer outra skill aqui. Recomendação de "próximo passo" é responsabilidade exclusiva de `/trafego-conexao` (que é o ponto de entrada e tem o bloco `🔭 Próximo passo recomendado`). Esta skill é só infraestrutura técnica de geração de token; encerra com a confirmação acima e ponto.

---

## Quando a tela do Business Manager estiver diferente

Se o usuario disser que nao encontrou alguma opcao ou que a tela esta diferente, use WebFetch para buscar a documentacao atualizada:

```
https://developers.facebook.com/docs/marketing-api/system-users
```

Adapte as instrucoes com base no conteudo retornado. Nao cite que buscou na documentacao.
