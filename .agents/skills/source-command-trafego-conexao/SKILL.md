---
name: "source-command-trafego-conexao"
description: "Porta única de entrada para conectar o projeto com o Meta Ads (Facebook + Instagram). Pergunta se o aluno quer usar o conector oficial Codex + Meta (recomendado, MCP via OAuth) ou criar um App via Facebook Developers (token permanente no .env). Salva o modo escolhido em META_AUTH_MODO no .env, para que as skills de tráfego saibam qual caminho usar. Skill reutilizável, deve ser chamada por qualquer skill de Meta Ads quando a variável META_AUTH_MODO ainda não está configurada."
---

# source-command-trafego-conexao

Use this skill when the user asks to run the migrated source command `trafego-conexao`.

## Command Template

# Tráfego Conexão. Estabelecer Conexão com o Meta Ads

Esta skill é o ponto único de entrada para conectar o projeto com o Meta Ads. Ela pergunta o modo de conexão preferido, executa o caminho correto e salva a preferência em `META_AUTH_MODO` no `.env`. Skills de tráfego como `/ads-relatorio`, `/enviar-relatorio-ads`, `/lt-otimizar` e qualquer skill futura de análise de campanhas vão ler essa variável para saber qual caminho usar.

Os dois modos suportados são:

- **`MCP_CONECTOR`** — Conector oficial Codex + Meta. Login via OAuth direto na conta Codex. Sem token permanente, sem App no Facebook Developers, sem instalar nada na máquina.
- **`APP`** — App via Facebook Developers. Token permanente gerado pelo Usuário do Sistema, salvo no `.env`. Caminho técnico tradicional, portável entre máquinas e planos.

---

## Passo 0. Verificar estado atual

Leia o arquivo `.env` na raiz do projeto.

**Caso 1. Linha `META_AUTH_MODO` já existe com valor `MCP_CONECTOR` ou `APP`:**

Pergunte:

```
Já existe uma conexão configurada com o Meta Ads.

Modo ativo: {valor encontrado}

O que você quer fazer?

1. Manter como está
2. Trocar de modo
3. Validar a conexão atual

Digite o número:
```

- Opção 1: encerrar com mensagem de confirmação ("Conexão atual mantida. Modo ativo: {valor}.").
- Opção 2: seguir para o Passo 1 e refazer a configuração. As variáveis do modo anterior (ex: `FB_ACCESS_TOKEN_PERMANENTE`, `FB_AD_ACCOUNT_ID`) ficam no `.env` por segurança, caso o aluno queira voltar para o modo anterior depois.
- Opção 3: pular direto para o Passo 3 (validação) usando o modo registrado no `.env`. A skill precisa ler `META_AUTH_MODO` de novo no Passo 3 para escolher o ramo certo de validação.

**Caso 2. Linha `META_AUTH_MODO` existe mas o valor é inválido** (qualquer coisa que não seja `MCP_CONECTOR` nem `APP`):

Avisar o aluno:

```
Encontrei a variável META_AUTH_MODO no .env, mas o valor "{valor}" não é
reconhecido (esperado MCP_CONECTOR ou APP). Vou tratar como se a conexão
não estivesse configurada.
```

Em seguida, ir direto para o Passo 1.

**Caso 3. Linha `META_AUTH_MODO` não existe ou está vazia:** ir direto para o Passo 1, sem aviso.

---

## Passo 1. Escolher o modo de conexão

Pergunte exatamente neste formato:

```
Como você quer conectar com o Meta Ads?

1. MCP da Meta via Codex (recomendado)
   Adiciona o servidor MCP oficial da Meta como conector personalizado
   no seu Codex (ainda não está na lista oficial, mas leva 1 minuto
   para registrar) e autoriza via OAuth do Facebook. Sem instalar
   nada na máquina, sem token permanente, sem App no Facebook
   Developers. A conexão fica vinculada à sua conta Anthropic.
   Funciona em qualquer máquina onde você estiver logado na mesma
   conta.

2. App via Facebook Developers
   Cria um App no developers.facebook.com, gera um token permanente
   via Usuário do Sistema e salva no .env. Caminho técnico
   tradicional. Funciona em qualquer plano do Codex. O token fica
   na sua máquina, então é portável e não depende da Anthropic.

Digite o número:
```

- Opção 1 → seguir para o Passo 2A.
- Opção 2 → seguir para o Passo 2B.

---

## Passo 2A. Adicionar o MCP da Meta como conector personalizado

> **Atenção.** O MCP da Meta ainda não está na lista oficial de conectores do Codex, então precisa ser adicionado como **MCP personalizado**. É rápido, só leva 1 minuto.

Instrua o aluno na seguinte ordem, esperando confirmação ao final:

```
Para adicionar o MCP da Meta na sua conta Codex:

1. Abra o aplicativo do Codex Desktop (não vale o site
   https://Codex.com/settings/connectors, esse caminho não
   tem mais a opção de adicionar MCP personalizado).

2. Clique em "Customize" (Personalizar) e depois em
   "Connectors" (Conectores).

3. Dentro de Conectores, clique no símbolo de "+" e escolha
   "Adicionar conector personalizado" (Add custom connector).

4. Preencha os campos do conector personalizado:
   - URL do servidor: https://mcp.facebook.com/ads
   - Nome da conexão: Meta Ads
     (pode usar outro nome se quiser, mas "Meta Ads" deixa fácil
     de identificar depois)

5. Clique em "Adicionar" / "Salvar" para registrar o MCP.

6. Vai abrir uma aba do Facebook pedindo autorização. Faça assim:
   - Entre com a conta de admin do Business Manager que tem a
     conta de anúncios que você quer usar
   - Selecione a Página do Facebook e o perfil do Instagram que
     quer autorizar
   - Confirme as permissões pedidas

7. Quando voltar ao Codex e o status do MCP "Meta Ads" estiver
   "Conectado", me avisa aqui ("conectei", "feito" ou similar) que
   continuo a validação.
```

Aguardar a resposta do aluno.

> **Atenção, conector é por conta Anthropic, não por máquina.** Se o aluno usar o Codex em outra máquina logada na mesma conta, o MCP Meta Ads segue ativo lá também. Não precisa adicionar de novo.

Quando o aluno confirmar, seguir para o Passo 3 (validação MCP).

---

## Passo 2B. Criar App via Facebook Developers

Acione a skill `/criar-aplicativo-analise-ads`. Ela é o ponto de entrada do caminho técnico e encadeia automaticamente nas duas skills seguintes.

Sequência completa do encadeamento:

1. **`/criar-aplicativo-analise-ads`** — criar o App no developers.facebook.com com o caso de uso "Mensurar dados de desempenho do anúncio com a API de Marketing", adicionar política de privacidade e publicar.
2. **`/gerar-token-permanente-facebook-ads`** (encadeada pela primeira) — criar Usuário do Sistema, atribuir Conta de Anúncios + App + Página + Instagram, gerar token permanente, validar com 3 testes na Graph API e salvar `FB_ACCESS_TOKEN_PERMANENTE` no `.env`.
3. **`/obter-id-conta-anuncios`** (encadeada pela segunda) — localizar o ID da conta de anúncios e salvar como `FB_AD_ACCOUNT_ID` no `.env`.

Ao final do encadeamento, o `.env` deve ter as duas variáveis:

```
FB_ACCESS_TOKEN_PERMANENTE={token}
FB_AD_ACCOUNT_ID={id}
```

Quando o encadeamento terminar, retornar aqui e seguir para o Passo 3 (validação APP).

---

## Passo 3. Validar a conexão

**Se o modo escolhido foi `MCP_CONECTOR`:**

🔍 Próximo passo: validar o MCP da Meta. Tempo estimado: cerca de 15 segundos.

Identifique a tool de listagem de contas de anúncio disponibilizada pelo MCP da Meta. O nome exato depende do nome que o aluno deu ao conector personalizado no Passo 2A. Estratégia de busca, em ordem:

1. **Listar tools MCP disponíveis no momento.** Procure tools com prefixo `mcp__` cujo sufixo trate de Meta Ads (ex: `mcp__Meta_Ads__ads_get_ad_accounts`, `mcp__metaads__list_ad_accounts`, `mcp__meta__get_ad_accounts`).
2. **Se a busca não for conclusiva**, perguntar ao aluno: *"Qual nome você deu ao MCP da Meta no Passo 2A? Vou usar pra localizar a tool certa."*
3. Tentar chamar a tool encontrada sem parâmetros.

- **Se retornar uma lista de contas de anúncios:** conexão validada. Seguir para o Passo 4.
- **Se nenhuma tool com prefixo MCP relacionada ao Meta estiver disponível** (erro "tool not found" ou similar): o conector ainda não está ativo na conta. Avisar o aluno:

  ```
  Não consegui acessar nenhuma tool do MCP da Meta. Confirme:

  - Você está logado no Codex com a mesma conta onde adicionou o
    MCP personalizado?
  - Em https://Codex.com/settings/connectors o MCP que você
    adicionou (ex: "Meta Ads") aparece como "Conectado" (verde)?
  - Você precisa reiniciar o Codex para o MCP recém-adicionado
    aparecer? (saia do CLI e abra de novo)

  Quando estiver tudo certo, me avisa que tento de novo.
  ```

  Aguardar e tentar de novo. Se o aluno desistir, oferecer trocar para o modo `APP` (voltar ao Passo 1).

- **Se a tool retornar erro de permissão:** o MCP está conectado mas o aluno não autorizou nenhuma conta de anúncios na hora do OAuth. Pedir para refazer o passo 5 do Passo 2A no Facebook (o passo de seleção da Página e do perfil do Instagram).

**Se o modo escolhido foi `APP`:**

🔍 Próximo passo: validar o token permanente com 3 testes na Graph API. Tempo estimado: cerca de 20 segundos.

Leia `FB_ACCESS_TOKEN_PERMANENTE` e o ID da conta no `.env`. Rode os 3 testes definidos no Passo 4 do `/gerar-token-permanente-facebook-ads`:

```bash
curl "https://graph.facebook.com/v25.0/me?access_token=TOKEN"
curl "https://graph.facebook.com/v25.0/me/adaccounts?access_token=TOKEN"
curl "https://graph.facebook.com/v25.0/act_AD_ACCOUNT_ID/campaigns?limit=1&access_token=TOKEN"
```

- **Se os 3 passarem:** conexão validada. Seguir para o Passo 4.
- **Se algum falhar:** consultar o "Mapa de erros comuns" do `/gerar-token-permanente-facebook-ads`. Não salvar `META_AUTH_MODO` enquanto a validação não passar.

✅ Concluído: conexão validada.

---

## Passo 4. Salvar a preferência no .env

Leia o `.env`.

**Se a linha `META_AUTH_MODO` já existir:** atualize o valor com `Edit` cirúrgico (substituir só essa linha).

**Se não existir:** adicione no final do arquivo:

```
META_AUTH_MODO=MCP_CONECTOR
```

ou

```
META_AUTH_MODO=APP
```

conforme o modo escolhido. Não sobrescrever outras variáveis. Não tocar na linha `RELATORIO_AUTH_MODO=CLI` se ela existir, ela é legada e vai ser tratada na próxima rodada de refatoração do `/ads-relatorio` e `/enviar-relatorio-ads`.

---

## Saída final

Mostre ao aluno:

```
✅ Conexão com Meta Ads configurada.

Modo ativo: {MCP_CONECTOR | APP}

Variável salva no .env: META_AUTH_MODO={valor}

As próximas skills de tráfego vão ler essa preferência e usar o
caminho certo automaticamente. Você não precisa configurar de novo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-criar-campanha
Agora que sua conta está conectada, suba sua primeira campanha
(perpétuo de venda direta ou lançamento de captação).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Outras skills de tráfego pago ficam disponíveis no menu / pra
quem já tem campanha rodando.

Para trocar o modo no futuro, é só rodar /trafego-conexao de novo.
```

---

## Como outras skills devem usar esta variável

Toda skill de tráfego que precise se conectar ao Meta deve, no início:

1. Ler `META_AUTH_MODO` do `.env`.
2. **Se a variável estiver vazia ou ausente:** chamar `/trafego-conexao` para o aluno escolher o modo. Não tentar adivinhar nem cair em fallback.
3. **Se o valor for `MCP_CONECTOR`:** usar as tools do MCP da Meta que o aluno adicionou como conector personalizado. O prefixo das tools depende do nome que o aluno deu ao MCP (ex: `mcp__Meta_Ads__*`, `mcp__metaads__*`). Localize na lista de tools disponíveis as que começam com `mcp__` e tratam de Meta Ads.
4. **Se o valor for `APP`:** ler `FB_ACCESS_TOKEN_PERMANENTE` (e demais variáveis salvas pelo caminho do App) e fazer as chamadas via `curl`/CLI Python como faz hoje.

Esta skill é idempotente, pode ser chamada várias vezes sem efeito colateral.

---

## Princípios que esta skill nunca viola

1. **Nunca salvar `META_AUTH_MODO` antes da validação passar.** Se o conector ou o token falham na hora de validar, a variável não entra no `.env`. Evita estado inconsistente em que a skill diz "conectado" mas as skills downstream falham.
2. **Nunca pular a pergunta de modo na primeira execução.** Mesmo que o aluno já tenha `FB_ACCESS_TOKEN_PERMANENTE` no `.env` por ter rodado o caminho técnico antes, perguntar e deixar ele escolher conscientemente.
3. **Nunca pedir token completo no chat no caminho MCP.** Token e auth ficam todos na conta Anthropic, a skill nem vê.
4. **Nunca tocar em `RELATORIO_AUTH_MODO`.** Variável legada, deixa intacta. A migração das skills antigas é assunto separado.
5. **Nunca recomendar o caminho do App sem aviso.** Sempre apresentar o conector como recomendado primeiro, deixar o aluno escolher consciente.
6. **Sempre validar antes de declarar conexão pronta.** Para MCP, chamar uma tool de leitura. Para APP, rodar os 3 testes da Graph API.
