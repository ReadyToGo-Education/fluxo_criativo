---
name: trafego-conexao
description: >
  Base de conhecimento e fluxo executável para estabelecer a conexão do projeto com o Meta Ads
  (Facebook + Instagram). Porta única de entrada de autenticação de toda a stack de tráfego.
  Cobre dois modos: MCP_CONECTOR (conector personalizado da Meta na conta Claude, via OAuth) e APP
  (App no Facebook Developers com token permanente no .env). Descobre e grava no .env o modo de
  autenticação, a lista de contas de anúncio, a conta padrão, a Página e o perfil do Instagram.
  Valida a conexão antes de declarar pronto. É o gate duro consultado no Passo 0 de
  /trafego-insights, /trafego-criar-campanha, /trafego-otimizar, /trafego-escalar e /trafego-analise.
  Consultada pelo command /trafego-conexao. Use quando o aluno pedir "conectar Meta Ads",
  "conectar Facebook", "configurar conta de anúncio", "trocar de conta", ou quando qualquer skill de
  tráfego encontrar META_AUTH_MODO vazio no .env.
---

# Tráfego Conexão. Estabelecer Conexão com o Meta Ads

Esta skill é o ponto único de entrada de autenticação da stack de tráfego. Ela pergunta o modo de conexão preferido, executa o caminho correto, descobre os identificadores da conta e grava tudo no `.env`. Nenhuma outra skill de tráfego pede credencial ao aluno: todas leem o que esta skill gravou.

A skill é idempotente. Pode ser chamada quantas vezes for preciso sem efeito colateral.

---

## 1. Contrato de saída. O que esta skill grava no `.env`

Este é o contrato que as skills downstream consomem. Toda variável abaixo é escrita por esta skill e por nenhuma outra.

| Variável | Quando é gravada | Consumida por |
|---|---|---|
| `META_AUTH_MODO` | Sempre, ao final da validação | Passo 0 de todas as skills `trafego-*` |
| `FB_ACCESS_TOKEN_PERMANENTE` | Modo `APP`, via `/gerar-token-permanente-facebook-ads` | Toda chamada Graph API no modo `APP` |
| `FB_AD_ACCOUNT_ID` | Sempre, após o Passo 3.5 | Conta padrão de leitura e escrita |
| `FB_AD_ACCOUNT_IDS` | Sempre, após o Passo 3.5 | Menu multi-conta de todas as skills |
| `FB_PAGE_ID` | Sempre, após o Passo 3.6 | `/trafego-criar-campanha` (gate duro) |
| `FB_INSTAGRAM_USER_ID` | Quando houver Instagram vinculado | `/trafego-criar-campanha`, posicionamentos Reels e Stories |

**Regra dura de integridade.** `META_AUTH_MODO` é a última variável gravada. Ela só entra no `.env` depois que a validação do Passo 3 passou e os identificadores dos Passos 3.5 e 3.6 foram descobertos. Isso impede o estado inconsistente em que a skill diz "conectado" mas as skills downstream falham no gate por falta de conta ou de Página.

**Versão da Graph API.** Toda chamada desta skill usa `v25.0`. Esta skill é a fonte de verdade da versão para a stack de tráfego.

### Variáveis que esta skill nunca toca

- `RELATORIO_AUTH_MODO`. Legada, pertence a `/ads-relatorio` e `/enviar-relatorio-ads`.
- `META_ACCESS_TOKEN` e `META_AD_ACCOUNT_ID`. Legadas, do bloco antigo do `.env.example`. A stack de tráfego usa exclusivamente as `FB_*`.

---

## 2. Modos suportados

### `MCP_CONECTOR`
Conector personalizado da Meta registrado na conta Claude, autorizado por OAuth do Facebook. Sem token permanente, sem App no Facebook Developers, sem instalar nada na máquina. A conexão fica vinculada à conta Anthropic, então segue ativa em qualquer máquina logada na mesma conta.

**Custo de operação:** as chamadas passam pelas tools `mcp__*`. A skill nunca vê o token.

### `APP`
App criado no developers.facebook.com com token permanente gerado por Usuário do Sistema e salvo no `.env`. Caminho técnico tradicional, funciona em qualquer plano do Claude, portável entre máquinas.

**Custo de operação:** as chamadas passam por `curl` direto na Graph API com o token lido do `.env`. Vale a regra global de mascaramento de tokens do `CLAUDE.md`.

---

## 3. Máquina de estados da conexão

```
Passo 0  Verificar estado atual do .env
   |
   +-- META_AUTH_MODO válido ......... menu manter / trocar / validar
   +-- META_AUTH_MODO inválido ....... avisa e trata como ausente
   +-- META_AUTH_MODO ausente ........ segue direto
   |
Passo 1  Escolher modo (MCP_CONECTOR ou APP)
   |
   +-- 2A  Registrar MCP personalizado na conta Claude
   +-- 2B  Encadear criação de App no Facebook Developers
   |
Passo 3    Validar a conexão            (bloqueia se falhar)
Passo 3.5  Descobrir contas de anúncio  (grava FB_AD_ACCOUNT_ID + FB_AD_ACCOUNT_IDS)
Passo 3.6  Descobrir Página e Instagram (grava FB_PAGE_ID + FB_INSTAGRAM_USER_ID)
Passo 4    Gravar META_AUTH_MODO        (último, sela a conexão)
   |
Saída final + handoff para /trafego-criar-campanha
```

---

## Passo 0. Verificar estado atual

Leia o `.env` na raiz do projeto e procure a linha `META_AUTH_MODO`.

**Caso 1. Valor válido (`MCP_CONECTOR` ou `APP`).** Perguntar:

```
Já existe uma conexão configurada com o Meta Ads.

Modo ativo: {valor encontrado}

O que você quer fazer?

1. Manter como está
2. Trocar de modo
3. Validar a conexão atual
4. Redescobrir contas, Página e Instagram

Digite o número:
```

| Opção | Ação |
|---|---|
| 1 | Encerrar com "Conexão atual mantida. Modo ativo: {valor}." |
| 2 | Ir ao Passo 1 e refazer a configuração. As variáveis do modo anterior ficam no `.env`, para o aluno poder voltar atrás |
| 3 | Ir ao Passo 3, escolhendo o ramo de validação pelo `META_AUTH_MODO` gravado |
| 4 | Ir aos Passos 3.5 e 3.6, sem refazer autenticação. Use quando o aluno ganhou acesso a uma conta nova ou trocou de Página |

**Caso 2. Valor inválido.** Avisar e tratar como ausente:

```
Encontrei a variável META_AUTH_MODO no .env, mas o valor "{valor}" não é
reconhecido (esperado MCP_CONECTOR ou APP). Vou tratar como se a conexão
não estivesse configurada.
```

**Caso 3. Ausente ou vazia.** Ir direto ao Passo 1, sem aviso.

---

## Passo 1. Escolher o modo de conexão

Apresentar exatamente neste formato, com o conector sempre em primeiro lugar:

```
Como você quer conectar com o Meta Ads?

1. MCP da Meta via Claude (recomendado)
   Adiciona o servidor MCP da Meta como conector personalizado no seu
   Claude e autoriza via OAuth do Facebook. Sem instalar nada na
   máquina, sem token permanente, sem App no Facebook Developers.
   A conexão fica vinculada à sua conta Anthropic, então funciona em
   qualquer máquina onde você estiver logado na mesma conta.

2. App via Facebook Developers
   Cria um App no developers.facebook.com, gera um token permanente
   via Usuário do Sistema e salva no .env. Caminho técnico
   tradicional. Funciona em qualquer plano do Claude. O token fica na
   sua máquina, então é portável e não depende da Anthropic.

Digite o número:
```

Opção 1 leva ao Passo 2A. Opção 2 leva ao Passo 2B.

---

## Passo 2A. Registrar o MCP da Meta como conector personalizado

> **Atenção.** O MCP da Meta ainda não está na lista oficial de conectores do Claude, então precisa ser adicionado como conector personalizado. Leva cerca de 1 minuto.

Instruir o aluno e aguardar confirmação:

```
Para adicionar o MCP da Meta na sua conta Claude:

1. Abra o aplicativo do Claude Desktop. O site
   https://claude.com/settings/connectors não tem mais a opção de
   adicionar conector personalizado.

2. Clique em "Customize" (Personalizar) e depois em "Connectors"
   (Conectores).

3. Dentro de Conectores, clique no símbolo de "+" e escolha
   "Adicionar conector personalizado" (Add custom connector).

4. Preencha os campos:
   - URL do servidor: https://mcp.facebook.com/ads
   - Nome da conexão: Meta Ads
     (pode usar outro nome, mas "Meta Ads" deixa fácil de achar depois)

5. Clique em "Adicionar" para registrar o MCP.

6. Vai abrir uma aba do Facebook pedindo autorização:
   - Entre com a conta de admin do Business Manager que tem a conta
     de anúncios que você quer usar
   - Selecione a Página do Facebook e o perfil do Instagram
   - Confirme as permissões pedidas

7. Quando o status do MCP "Meta Ads" estiver "Conectado", me avisa
   aqui que eu continuo a validação.
```

> **O conector é por conta Anthropic, não por máquina.** Se o aluno usar o Claude em outra máquina logada na mesma conta, o MCP segue ativo lá. Não precisa repetir este passo.

Quando o aluno confirmar, seguir para o Passo 3.

---

## Passo 2B. Criar App via Facebook Developers

Acionar `/criar-aplicativo-analise-ads`. Ela é o ponto de entrada e encadeia as duas skills seguintes automaticamente:

1. **`/criar-aplicativo-analise-ads`.** Cria o App com o caso de uso "Mensurar dados de desempenho do anúncio com a API de Marketing", adiciona política de privacidade e publica.
2. **`/gerar-token-permanente-facebook-ads`.** Cria o Usuário do Sistema, atribui Conta de Anúncios, App, Página e Instagram, gera o token permanente, valida e grava `FB_ACCESS_TOKEN_PERMANENTE`.
3. **`/obter-id-conta-anuncios`.** Localiza o ID da conta e grava `FB_AD_ACCOUNT_ID`.

Ao final, o `.env` precisa ter `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID`. Se qualquer uma faltar, não avançar: repetir o passo que falhou.

Seguir para o Passo 3.

---

## Passo 3. Validar a conexão

Nada é gravado enquanto esta validação não passar.

### Ramo `MCP_CONECTOR`

Localizar a tool de listagem de contas de anúncio. O prefixo depende do nome que o aluno deu ao conector, então a busca é por padrão e não por nome fixo:

1. Varrer as tools disponíveis procurando prefixo `mcp__` com sufixo de Meta Ads. Exemplos observados: `mcp__Meta_Ads__ads_get_ad_accounts`, `mcp__claude_ai_Meta_Ads__ads_get_ad_entities`, `mcp__metaads__list_ad_accounts`.
2. Se a varredura não for conclusiva, perguntar: "Qual nome você deu ao MCP da Meta? Vou usar para localizar a tool certa."
3. Chamar a tool encontrada sem parâmetros.

| Resultado | Ação |
|---|---|
| Lista de contas de anúncios | Conexão validada. Seguir para 3.5, aproveitando a lista já retornada |
| Nenhuma tool `mcp__*` de Meta disponível | Conector não está ativo. Aplicar o diagnóstico abaixo |
| Erro de permissão | MCP conectado, mas nenhuma conta autorizada no OAuth. Pedir para refazer o item 6 do Passo 2A |

Diagnóstico de conector ausente:

```
Não consegui acessar nenhuma tool do MCP da Meta. Confirme:

- Você está logado no Claude com a mesma conta onde adicionou o
  conector personalizado?
- O conector "Meta Ads" aparece como "Conectado" na sua lista de
  conectores?
- Você reiniciou o Claude Code depois de adicionar? MCP recém-
  adicionado costuma precisar de reload (saia do CLI e abra de novo).

Quando estiver tudo certo, me avisa que eu tento de novo.
```

Se o aluno desistir, oferecer trocar para o modo `APP` (voltar ao Passo 1).

### Ramo `APP`

Ler `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` do `.env` e rodar os 3 testes. Cada `curl` é uma chamada `Bash` separada, conforme a regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" do `CLAUDE.md`. Nunca usar heredoc Python nem pipe para `python3`.

| # | Teste | Endpoint | Passa quando |
|---|---|---|---|
| 1 | Identidade do token | `GET /v25.0/me` | Retorna `id` e `name` |
| 2 | Acesso a contas | `GET /v25.0/me/adaccounts?fields=id,account_id,name,account_status` | Retorna ao menos 1 conta |
| 3 | Leitura na conta padrão | `GET /v25.0/act_{id}/campaigns?limit=1` | Retorna `data`, mesmo vazio |

Se os 3 passarem, conexão validada. Seguir para 3.5 reaproveitando o retorno do teste 2.

Se algum falhar, consultar o mapa de erros da seção 4 e o "Mapa de erros comuns" de `/gerar-token-permanente-facebook-ads`. Não gravar `META_AUTH_MODO`.

---

## Passo 3.5. Descobrir e gravar as contas de anúncio

Este passo fecha o gap que fazia o menu multi-conta nunca disparar nas skills downstream.

**Fonte dos dados.** Reaproveitar o retorno de `GET /v25.0/me/adaccounts?fields=id,account_id,name,account_status` (modo `APP`) ou da tool de listagem do MCP (modo `MCP_CONECTOR`). Não repetir a chamada se ela já foi feita no Passo 3.

**Filtro.** Considerar apenas contas com `account_status` igual a `1` (ativa). Contas desabilitadas, em revisão ou fechadas ficam de fora da lista, mas devem ser mencionadas ao aluno se forem as únicas encontradas.

**Se houver exatamente 1 conta ativa:** gravar direto, sem perguntar.

**Se houver 2 ou mais contas ativas:** apresentar a lista e perguntar qual é a padrão:

```
Encontrei {N} contas de anúncio no seu acesso:

1. {nome_conta_1}  (act_{id_1})
2. {nome_conta_2}  (act_{id_2})
3. {nome_conta_3}  (act_{id_3})

Qual delas é a sua conta principal? Ela vira a padrão das skills de
tráfego. As outras continuam disponíveis no menu quando você quiser
trocar.

Digite o número:
```

**Gravação no `.env`:**

- `FB_AD_ACCOUNT_ID` recebe o ID numérico da conta escolhida, sem o prefixo `act_`.
- `FB_AD_ACCOUNT_IDS` recebe todos os IDs numéricos ativos separados por vírgula, sem espaços, com a conta padrão em primeiro lugar.

```
FB_AD_ACCOUNT_ID=1234567890
FB_AD_ACCOUNT_IDS=1234567890,9876543210,5555555555
```

**Regra de formato.** Sempre sem `act_` e sempre sem espaço depois da vírgula. As skills downstream montam `act_{id}` por conta própria e fazem `split(",")` sem `trim`.

**Se nenhuma conta ativa for encontrada:** parar e instruir. Não gravar `META_AUTH_MODO`.

```
O token está válido, mas não encontrei nenhuma conta de anúncios ativa
no seu acesso. Isso costuma ser um destes casos:

- A conta existe mas está desabilitada ou em revisão no Business Manager
- O Usuário do Sistema não recebeu a conta de anúncios como ativo
- Você entrou com um perfil pessoal que não é admin do Business Manager

Resolva no business.facebook.com e rode /trafego-conexao de novo.
```

---

## Passo 3.6. Descobrir e gravar Página e Instagram

Este passo fecha o gap que fazia `/trafego-criar-campanha` reprovar no gate duro em instalação limpa. Sem `FB_PAGE_ID`, a Marketing API rejeita a criação de anúncio com erro 200.

**Buscar as Páginas com acesso na conta escolhida:**

```
GET /v25.0/act_{FB_AD_ACCOUNT_ID}/promote_pages?fields=id,name,username
```

Se o endpoint retornar vazio ou erro de permissão, usar o fallback:

```
GET /v25.0/me/accounts?fields=id,name,username
```

**Se houver exatamente 1 Página:** gravar direto, informando ao aluno qual foi.

**Se houver 2 ou mais:** perguntar, sempre mostrando nome junto do ID:

```
Qual Página do Facebook vai assinar os anúncios?

1. {nome_pagina_1}  ({id_1})
2. {nome_pagina_2}  ({id_2})

Digite o número:
```

**Instagram vinculado.** Para a Página escolhida, buscar o perfil do Instagram:

```
GET /v25.0/{FB_PAGE_ID}?fields=instagram_business_account{id,username}
```

- Se retornar um perfil, gravar `FB_INSTAGRAM_USER_ID` e confirmar ao aluno com `@username`.
- Se não retornar, não gravar a variável e avisar:

```
Não encontrei perfil do Instagram vinculado à Página {nome}. Você ainda
consegue anunciar no Feed do Facebook, mas Reels e Stories do Instagram
ficam indisponíveis até vincular o perfil no business.facebook.com.
```

Isso não bloqueia a conexão. É aviso, não gate.

**Regra de identificação por nome.** Toda vez que este passo exibir um ID, o nome humano acompanha, no formato `Nome (ID)`. Nunca mostrar `Page ID 106712754455284` sozinho.

---

## Passo 4. Gravar `META_AUTH_MODO` e selar a conexão

Só chegar aqui se o Passo 3 validou e os Passos 3.5 e 3.6 gravaram.

- Se a linha já existe no `.env`, atualizar com `Edit` cirúrgico, trocando só ela.
- Se não existe, acrescentar ao final do arquivo.

```
META_AUTH_MODO=MCP_CONECTOR
```

ou

```
META_AUTH_MODO=APP
```

Não sobrescrever outras variáveis. Não tocar em `RELATORIO_AUTH_MODO`.

---

## Saída final

```
✅ Conexão com Meta Ads configurada.

Modo ativo: {MCP_CONECTOR | APP}
Conta padrão: {nome} (act_{id})
Outras contas disponíveis: {N}
Página: {nome} ({id})
Instagram: @{username} ({id})

As próximas skills de tráfego leem essa configuração sozinhas. Você não
precisa configurar de novo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-criar-campanha
Agora que sua conta está conectada, suba sua primeira campanha
(perpétuo de venda direta ou lançamento de captação).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Já tem campanha rodando? Use /trafego-analise para diagnóstico narrado
ou /trafego-otimizar para agir sobre os números.

Para trocar de modo ou de conta, rode /trafego-conexao de novo.
```

Nunca exibir token, nem parcial, nem mascarado, salvo pedido explícito do aluno. Ver a regra "MASCARAMENTO DE TOKENS SENSÍVEIS" do `CLAUDE.md`.

---

## 4. Mapa de erros comuns

| Sintoma | Causa provável | Ação |
|---|---|---|
| `OAuthException` código 190 | Token expirado ou revogado | Refazer `/gerar-token-permanente-facebook-ads`. Token de Usuário do Sistema não expira, então isso indica revogação manual ou troca de senha |
| `OAuthException` código 200 | Falta permissão `ads_management` ou `ads_read` | Revisar as permissões do Usuário do Sistema no Business Manager |
| Erro 200 ao criar anúncio | `FB_PAGE_ID` ausente ou sem acesso na conta escolhida | Rodar o Passo 3.6 de novo pela opção 4 do Passo 0 |
| `me/adaccounts` vazio | Usuário do Sistema sem conta atribuída | Atribuir a conta de anúncios como ativo no Business Manager |
| `(#100) Tried accessing nonexisting field` | Versão da Graph API antiga | Confirmar que a chamada usa `v25.0` |
| Tool `mcp__*` some entre sessões | MCP recém-adicionado sem reload | Reiniciar o Claude Code |
| Conta aparece na lista mas rejeita escrita | `account_status` diferente de 1 | Verificar cobrança e situação da conta no Gerenciador |

---

## 5. Contrato de consumo. Como as outras skills usam

Toda skill de tráfego roda este bloco no Passo 0, antes de qualquer outra ação:

1. Ler `META_AUTH_MODO` do `.env`.
2. **Vazio ou ausente:** acionar `/trafego-conexao` e aguardar. Nunca adivinhar, nunca cair em fallback, nunca pedir credencial por conta própria.
3. **`MCP_CONECTOR`:** confirmar que existe ao menos uma tool `mcp__*` de Meta Ads. Se não existir, instruir reload do Claude Code. Se persistir, voltar a `/trafego-conexao`.
4. **`APP`:** confirmar `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID`. Em `/trafego-criar-campanha`, confirmar também `FB_PAGE_ID`. Se faltar qualquer uma, acionar `/trafego-conexao`.

**Seleção de conta nas skills downstream.** Ler `FB_AD_ACCOUNT_IDS`. Se tiver 2 ou mais IDs, apresentar menu com a conta de `FB_AD_ACCOUNT_ID` em primeiro lugar e etiqueta `"padrão"`. Se tiver 1 ou estiver vazio, usar `FB_AD_ACCOUNT_ID` direto sem perguntar. A conta escolhida vive só na execução, em variável local. Skill downstream não reescreve o `.env`.

---

## 6. Princípios que esta skill nunca viola

1. **`META_AUTH_MODO` é gravada por último.** Validação e descoberta de identificadores vêm antes. Sem isso, a conexão fica "pronta" no papel e quebra no primeiro uso real.
2. **Nunca pular a pergunta de modo na primeira execução.** Mesmo com `FB_ACCESS_TOKEN_PERMANENTE` já no `.env`, o aluno escolhe conscientemente.
3. **Nunca pedir nem exibir token no chat no caminho MCP.** No caminho MCP a skill não vê token nenhum.
4. **Nunca tocar em `RELATORIO_AUTH_MODO`,** `META_ACCESS_TOKEN` ou `META_AD_ACCOUNT_ID`. São legadas de outra stack.
5. **Sempre apresentar o conector como recomendado primeiro,** deixando o aluno escolher consciente.
6. **Sempre validar antes de declarar pronto.** No MCP, chamando uma tool de leitura. No APP, rodando os 3 testes.
7. **Toda chamada Graph API é um `Bash(curl ...)` separado.** Sem heredoc Python, sem pipe para `python3`. Ver a regra de execução técnica no `CLAUDE.md`.
8. **Todo ID exibido vem acompanhado do nome humano,** no formato `Nome (ID)`.
9. **Esta skill é a única que escreve as variáveis do contrato da seção 1.** Nenhuma skill downstream reescreve o `.env` de conexão.
10. **Idempotência.** Rodar de novo nunca corrompe estado. No pior caso, revalida e regrava os mesmos valores.
