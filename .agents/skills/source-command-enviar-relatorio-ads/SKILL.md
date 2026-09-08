---
name: "source-command-enviar-relatorio-ads"
description: "Busca as métricas do Facebook Ads e envia o relatório pelo Telegram ou WhatsApp. Detecta automaticamente o modo configurado (CLI Python ou Manual PowerShell)."
---

# source-command-enviar-relatorio-ads

Use this skill when the user asks to run the migrated source command `enviar-relatorio-ads`.

## Command Template

# Enviar Relatorio de Ads

Executa imediatamente: busca as metricas do Facebook Ads do periodo escolhido e envia no canal configurado (Telegram ou WhatsApp). Sem agendamento.

Detecta `RELATORIO_AUTH_MODO` no `.env` e usa o script correto:
- `CLI`: `scripts/relatorio-ads-cli.py` (Python, cross-platform)
- `MANUAL` ou nao definido: `scripts/relatorio-ads.ps1` (PowerShell, Windows)

## PASSO 0. Verificar modo de conexão Meta

Antes de qualquer coisa, leia `META_AUTH_MODO` no `.env` para decidir o caminho.

- **Vazia ou ausente:** chame a skill `/trafego-conexao` para o aluno escolher o modo. Quando ela terminar e gravar `META_AUTH_MODO`, retorne aqui.
- **`META_AUTH_MODO=MCP_CONECTOR`:** o Passo 1.1 (credenciais Facebook) é pulado por completo. A conexão Meta foi validada via conector personalizado em `/trafego-conexao` e não usa token no `.env`. Vá direto para o Passo 1.2 (canal de envio).
- **`META_AUTH_MODO=APP`:** executar normalmente o Passo 1.1 e o Passo 1.2.

> **Nota sobre as duas variáveis.** `META_AUTH_MODO` decide o caminho de autenticação com o Meta (MCP via Codex ou Token via App no `.env`). `RELATORIO_AUTH_MODO` decide o executor do relatório dentro do ramo App (Python CLI cross-platform ou PowerShell Windows). Não são redundantes, atuam em camadas diferentes.

---

## PASSO 1. Verificar credenciais

### 1.1 Credenciais Facebook (apenas modo APP)

> Pular este sub-passo completo se `META_AUTH_MODO=MCP_CONECTOR`. No modo MCP não há token Facebook no `.env`.

Leia `.env`.

**Detectar o sub-modo de execução:**

Se `RELATORIO_AUTH_MODO=CLI` (ou nao definido mas `ACCESS_TOKEN` existir):
- Verificar `ACCESS_TOKEN` (ou fallback `FB_ACCESS_TOKEN_PERMANENTE` / `FB_ACCESS_TOKEN_TEMPORARIO`)
- Verificar `AD_ACCOUNT_ID` (ou fallback `FB_AD_ACCOUNT_ID`)
- Se faltar: oriente a rodar `/ads-relatorio` primeiro para configurar o modo CLI.

Se `RELATORIO_AUTH_MODO=MANUAL` (ou nao definido e `ACCESS_TOKEN` nao existir):
- Verificar pelo menos uma das variaveis: `FB_ACCESS_TOKEN_PERMANENTE` ou `FB_ACCESS_TOKEN_TEMPORARIO`
- Verificar `FB_AD_ACCOUNT_ID`
- Se faltar token: pergunte se tem App no Facebook Developers
  - Se sim: execute a skill `gerar-token-permanente-facebook-ads`
  - Se nao: execute a skill `criar-aplicativo-analise-ads`, depois `gerar-token-permanente-facebook-ads`
- Se faltar `FB_AD_ACCOUNT_ID`: execute a skill `obter-id-conta-anuncios`

### 1.2 Canal de envio (sempre, independente do modo)
- Se `RELATORIO_CANAL` nao existir no `.env`, pergunte:

```
Por qual canal quer enviar o relatorio?

1. Telegram (Recomendado)
2. WhatsApp

Digite o numero:
```

Se o usuario perguntar por que Telegram e recomendado: "O Telegram e gratuito e nao tem risco de bloqueio. Automacoes no WhatsApp podem banir o numero."

Se WhatsApp, exiba antes de continuar: "Atencao: use um numero secundario aquecido, nao o numero principal da operacao."

Salve `RELATORIO_CANAL=TELEGRAM` ou `RELATORIO_CANAL=WHATSAPP` no `.env` com `Edit`.

**Se `RELATORIO_CANAL=TELEGRAM`:**
- Verificar `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`
- Se faltar qualquer um: execute a skill `configurar-telegram`, depois retorne

**Se `RELATORIO_CANAL=WHATSAPP`:**
- Verificar `ZAPI_INSTANCE_ID`, `ZAPI_TOKEN`, `ZAPI_CLIENT_TOKEN`, `RELATORIO_WHATSAPP_NUMERO`
- Se faltar qualquer credencial Z-API: pergunte se tem conta na Z-API
  - Se sim: peca as 3 credenciais uma por vez e salve no `.env` com `Edit`
  - Se nao: execute a skill `configurar-zapi`, depois retorne
- Se faltar `RELATORIO_WHATSAPP_NUMERO`:

```
Para qual numero do WhatsApp devo enviar o relatorio?

Digite no formato internacional sem + e sem espacos.
(ex: 5511999887766)
```

Salve como `RELATORIO_WHATSAPP_NUMERO=valor` no `.env`.

**Quando todas as credenciais estiverem presentes:** avance para o Passo 2.

## PASSO 2. Perguntar o periodo

Pergunte ao usuario:

```
Qual periodo voce quer no relatorio?

1. Ontem
2. Ultimos 7 dias
3. Ultimos 30 dias
4. Periodo personalizado (informar data inicial e final)

Digite o numero:
```

- Opcao 1: calcule `INICIO_ISO` e `FIM_ISO` como ontem. Label do periodo: `{ONTEM_BR}`.
- Opcao 2: `INICIO_ISO` = hoje menos 7 dias, `FIM_ISO` = ontem. Label: `Ultimos 7 dias`.
- Opcao 3: `INICIO_ISO` = hoje menos 30 dias, `FIM_ISO` = ontem. Label: `Ultimos 30 dias`.
- Opcao 4: peca a data inicial (formato DD/MM/AAAA) e a data final (formato DD/MM/AAAA), converta para ISO (AAAA-MM-DD). Label: `{INICIO_BR} a {FIM_BR}`.

Para calcular as datas use Bash:
```bash
# Ontem
date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d
# 7 dias atras
date -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d
# 30 dias atras
date -d "30 days ago" +%Y-%m-%d 2>/dev/null || date -v-30d +%Y-%m-%d
```

Guarde `INICIO_ISO`, `FIM_ISO` e `LABEL_PERIODO`.

## PASSO 3. Executar busca de dados

A busca varia conforme `META_AUTH_MODO`.

### Se `META_AUTH_MODO=MCP_CONECTOR` (modo MCP)

Identifique no namespace MCP a tool de insights da Meta exposta pelo conector personalizado adicionado no `/trafego-conexao`. O nome exato depende do nome que o aluno deu ao conector. Estratégia:

1. Listar tools com prefixo `mcp__*` cujo sufixo trate de insights/performance (ex: `mcp__Meta_Ads__ads_insights_advertiser_context`, `mcp__Meta_Ads__ads_insights_performance_trend`).
2. Se a busca não for conclusiva, perguntar ao aluno o nome que ele deu ao MCP.

Chame a tool de insights passando o intervalo de datas (`INICIO_ISO` a `FIM_ISO`) e os campos de métrica relevantes (gasto, alcance, impressões, cliques, CTR, CPM, CPC, ações de purchase/lead). O conector é responsável por decidir qual conta de anúncios usar (definido no OAuth feito em `/trafego-conexao`).

Guarde o JSON retornado na variável `data` para o Passo 4 montar a mensagem.

> **Nota.** O modo MCP busca os dados, mas não envia mensagem. O envio (Telegram ou Z-API) é feito separadamente no Passo 6.

### Se `META_AUTH_MODO=APP` (modo App via Facebook Developers)

Use o script adequado ao sub-modo configurado em `RELATORIO_AUTH_MODO`. Ambos os scripts lêem o `.env`, mascaram segredos nos logs e já retornam os dados formatados E enviam pelo canal configurado de uma vez só.

**Se `RELATORIO_AUTH_MODO=CLI`:**

Determine o comando Python correto primeiro:
```bash
python --version 2>&1 || python3 --version 2>&1
```

Depois execute (substitua `python` por `python3` se necessario):
```bash
python scripts/relatorio-ads-cli.py {ESCOLHA_PERIODO} {INICIO_BR} {FIM_BR}
```

Onde `{ESCOLHA_PERIODO}` e o numero escolhido no Passo 2 (1, 2, 3 ou 4). Para opcao 4, passe tambem inicio e fim no formato DD/MM/AAAA. Exemplos:
- Ontem: `python scripts/relatorio-ads-cli.py 1`
- Ultimos 7 dias: `python scripts/relatorio-ads-cli.py 2`
- Personalizado: `python scripts/relatorio-ads-cli.py 4 01/04/2026 30/04/2026`

**Se `RELATORIO_AUTH_MODO=MANUAL` (ou nao definido):**
```bash
powershell.exe -ExecutionPolicy Bypass -File "scripts/relatorio-ads.ps1"
```

Nunca passe `ACCESS_TOKEN`, `ZAPI_TOKEN`, `TELEGRAM_BOT_TOKEN` ou qualquer chave pela URL, pelo chat ou por comando que possa aparecer no historico do terminal.

> **Nota.** No modo APP, os scripts já fazem busca + envio juntos. O Passo 6 não precisa rodar de novo.

## PASSO 4. Montar a mensagem

Se `data` vier vazio (`[]`):

```
*Relatorio Meta Ads - {LABEL_PERIODO}*

Sem dados para o periodo. Verifique se ha campanhas ativas.
```

Se `data` tiver conteudo, monte:

```
*Relatorio Meta Ads - {LABEL_PERIODO}*

*Investimento e Alcance*
Gasto: R$ X,XX
Alcance: X.XXX
Impressoes: X.XXX

*Engajamento*
Cliques: X.XXX
CTR: X,XX%
CPM: R$ X,XX
CPC: R$ X,XX
```

Se houver `actions` com `action_type` igual a `purchase` ou `lead`, adicione:

```
*Conversoes*
Resultados: X
Custo por resultado: R$ X,XX
```

Formatacao numerica: valores monetarios com virgula decimal e ponto milhar (ex: `R$ 1.234,56`). Percentuais com virgula (ex: `3,42%`).

## PASSO 5. Confirmar envio

**Se Telegram:**

```
Relatorio pronto. Deseja enviar para o seu Telegram?

1. Sim, enviar agora
2. Nao, apenas exibir aqui
```

**Se WhatsApp:**

```
Relatorio pronto. Deseja enviar para o WhatsApp {NUMERO_MASCARADO}?

1. Sim, enviar agora
2. Nao, apenas exibir aqui
```

Se opcao 2: encerre sem chamar nenhuma API de envio.

## PASSO 6. Enviar

O fluxo de envio depende do `META_AUTH_MODO`.

### Se `META_AUTH_MODO=APP`

O script já cuidou do envio internamente no Passo 3 (busca + envio integrados). Não há nada para refazer aqui — só conferir o resultado e passar para o Passo 7.

Se por algum motivo o script no Passo 3 só buscou sem enviar (ex: aluno escolheu opção 2 "apenas exibir aqui" no Passo 5), execute o mesmo comando do Passo 3 para disparar de novo:

**Se `RELATORIO_AUTH_MODO=CLI`:**
```bash
python scripts/relatorio-ads-cli.py {ESCOLHA_PERIODO}
```

**Se `RELATORIO_AUTH_MODO=MANUAL` (ou nao definido):**
```bash
powershell.exe -ExecutionPolicy Bypass -File "scripts/relatorio-ads.ps1"
```

Nao use `curl` manual com token em URL ou header escrito no comando.

### Se `META_AUTH_MODO=MCP_CONECTOR`

A tool MCP do Passo 3 só busca os dados, não envia. O envio precisa ser feito agora com a mensagem montada no Passo 4.

**Se `RELATORIO_CANAL=TELEGRAM`:**

Use Bash para chamar a API do Telegram. Leia `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` do `.env`. Salve a mensagem montada no Passo 4 num arquivo temporário para evitar problemas de escape e expor o token na linha de comando:

```bash
# Substitua {MENSAGEM} pelo texto montado no Passo 4
TMPFILE=$(mktemp)
cat > "$TMPFILE" <<'EOF'
{MENSAGEM}
EOF
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
  --data-urlencode "parse_mode=Markdown" \
  --data-urlencode "text@${TMPFILE}"
rm "$TMPFILE"
```

**Se `RELATORIO_CANAL=WHATSAPP`:**

Use Bash para chamar a Z-API. Leia `ZAPI_INSTANCE_ID`, `ZAPI_TOKEN`, `ZAPI_CLIENT_TOKEN` e `RELATORIO_WHATSAPP_NUMERO` do `.env`:

```bash
TMPFILE=$(mktemp)
cat > "$TMPFILE" <<'EOF'
{
  "phone": "${RELATORIO_WHATSAPP_NUMERO}",
  "message": "{MENSAGEM}"
}
EOF
curl -s -X POST "https://api.z-api.io/instances/${ZAPI_INSTANCE_ID}/token/${ZAPI_TOKEN}/send-text" \
  -H "Content-Type: application/json" \
  -H "Client-Token: ${ZAPI_CLIENT_TOKEN}" \
  --data-binary "@${TMPFILE}"
rm "$TMPFILE"
```

> **Atenção.** Não imprima o token no chat. Não passe credenciais como argumento da linha de comando (ficam no histórico). Sempre use variável de ambiente lida do `.env`. Apague os arquivos temporários ao final.

## PASSO 7. Resultado

**Se Telegram:**

- Sucesso (`"ok":true`): informe "Relatorio enviado para o seu Telegram."
- Erro: mostre a mensagem de erro e oriente:
  - `"Unauthorized"` ou error_code 401: token do bot invalido. Rode `/configurar-telegram` para reconfigurar.
  - `"chat not found"`: Chat ID errado. Rode `/configurar-telegram` para obter o Chat ID correto.
  - Qualquer outro erro: mostre o retorno bruto para diagnostico.

**Se WhatsApp (Z-API):**

- Sucesso: informe "Relatorio enviado para {numero mascarado}."
- Erro, mostre a mensagem e oriente:
  - `"subscribe to this instance again"`: assinatura Z-API expirada. Acesse o painel da Z-API e renove o plano.
  - `"connected":false`: WhatsApp desconectado. Acesse o painel da Z-API e reconecte pelo QR Code.
  - Qualquer outro erro: mostre o retorno bruto para diagnostico.
