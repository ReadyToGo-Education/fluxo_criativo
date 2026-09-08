---
name: "source-command-ads-relatorio"
description: "Configura as credenciais e preferências do relatório de Facebook Ads (canal, métricas, filtro de campanhas) e oferece envio imediato via /enviar-relatorio-ads. Telegram ou WhatsApp. Usa o Meta Ads CLI via Python."
---

# source-command-ads-relatorio

Use this skill when the user asks to run the migrated source command `ads-relatorio`.

## Command Template

# Configurar Relatorio de Ads

Configura o canal de envio, as credenciais e as preferencias do relatorio de Facebook Ads. Ao final, voce pode enviar um relatorio imediatamente.

O mentoreado nunca abre arquivo, nunca instala nada manualmente. So cola as chaves no chat e segue as instrucoes.

## COMO FUNCIONA

1. Codex configura o Meta Ads CLI (Python) e as credenciais
2. Codex registra as preferencias de metricas e filtro de campanhas
3. Ao final, voce pode enviar um relatorio imediatamente com `/enviar-relatorio-ads`

---

## PASSO -1. Verificar modo de conexão Meta

Antes de qualquer coisa, leia `META_AUTH_MODO` no `.env`.

**Se a variável estiver vazia ou ausente:**

A conexão Meta ainda não foi configurada. Avise o aluno:

```
Você ainda não configurou a conexão com o Meta Ads.

Vou rodar /trafego-conexao primeiro para você escolher entre o MCP da
Meta (recomendado) ou o caminho do App via Facebook Developers.
Quando terminar, volto direto pra configuração do relatório.
```

Acione a skill `/trafego-conexao`. Quando ela terminar e gravar `META_AUTH_MODO` no `.env`, retorne aqui e siga conforme o valor salvo.

**Se `META_AUTH_MODO=MCP_CONECTOR`:**

Pule todo o **Passo 0** e o **Passo 0-CLI**. Não precisa instalar Python, nem o pacote `meta-ads`, nem coletar `ACCESS_TOKEN` ou `AD_ACCOUNT_ID` (essas variáveis só importam no caminho APP). A conexão com o Meta já está garantida pelo conector personalizado validado em `/trafego-conexao`.

Vá direto para o **Passo 0-CANAL** (configuração do canal de envio Telegram ou WhatsApp).

**Se `META_AUTH_MODO=APP`:**

Siga para o **Passo 0** atual. Dentro do ramo APP, a variável `RELATORIO_AUTH_MODO` continua decidindo qual script de execução roda (Python CLI ou PowerShell).

> **Nota sobre as duas variáveis.** `META_AUTH_MODO` decide o caminho de autenticação com o Meta (MCP via Codex ou Token via App no `.env`). `RELATORIO_AUTH_MODO` decide o executor do relatório dentro do ramo App (Python CLI cross-platform ou PowerShell Windows). Não são redundantes, atuam em camadas diferentes.

---

## PASSO 0. Verificar Modo de Integracao

> Este passo só executa se `META_AUTH_MODO=APP`. Caminho MCP pula direto para o Passo 0-CANAL.

Leia `.env`. Se `RELATORIO_AUTH_MODO` ja existir com valor `CLI`, pule para o **Passo 0-CLI**.

Se nao existir (ou tiver qualquer outro valor), salve `RELATORIO_AUTH_MODO=CLI` no `.env` com `Edit` e siga para o **Passo 0-CLI**.

---

## PASSO 0-CLI. Configurar o Meta Ads CLI

### CLI-1. Verificar Python

Execute:

```bash
python --version 2>&1 || python3 --version 2>&1
```

- Se retornar `Python 3.12` ou superior: continue.
- Se retornar versao inferior a 3.12 ou nao encontrado: exiba a mensagem abaixo e pare ate o usuario resolver.

```
O Meta Ads CLI exige Python 3.12 ou superior.

Versao detectada: [versao encontrada ou "nao encontrado"]

Para instalar:
- Windows: acesse https://python.org/downloads e baixe a versao mais recente
- Mac: brew install python@3.12
- Linux: sudo apt install python3.12

Apos instalar, rode o comando "/ads-relatorio" novamente.
```

### CLI-2. Instalar o meta-ads

Use Bash para verificar se ja esta instalado:

```bash
meta --version 2>&1 || python -m meta --version 2>&1 || python3 -m meta --version 2>&1
```

Se ja estiver instalado, informe "Meta Ads CLI ja instalado." e avance.

Se nao estiver instalado, informe "Instalando o Meta Ads CLI..." e use Bash para instalar:

```bash
pip install meta-ads
```

Se `pip` retornar erro, use Bash para tentar:

```bash
pip3 install meta-ads
```

Apos instalar, use Bash para confirmar:

```bash
meta --help 2>&1 | head -5
```

Se retornar a ajuda do CLI, informe "Meta Ads CLI instalado com sucesso." e avance.
Se retornar erro mesmo apos instalar, informe o erro exato ao usuario e pare.

### CLI-3. Verificar ou Configurar Credenciais do Facebook Ads

Leia `.env`. Verifique se alguma dessas variaveis ja existe com valor preenchido:
- `ACCESS_TOKEN`
- `FB_ACCESS_TOKEN_PERMANENTE`
- `FB_ACCESS_TOKEN_TEMPORARIO`

E tambem:
- `AD_ACCOUNT_ID`
- `FB_AD_ACCOUNT_ID`

**Se ja tiver credenciais (qualquer combinacao acima):**

Informe:

```
Encontrei credenciais existentes do Facebook Ads.

Vou configurar os nomes de variavel que o CLI usa (ACCESS_TOKEN e AD_ACCOUNT_ID)
aproveitando os valores que voce ja tem. Nenhum token novo precisa ser gerado.
```

Use `Edit` para adicionar (sem sobrescrever os existentes):
- Se tem `FB_ACCESS_TOKEN_PERMANENTE`: adicione `ACCESS_TOKEN=[mesmo valor]`
- Se tem apenas `FB_ACCESS_TOKEN_TEMPORARIO`: adicione `ACCESS_TOKEN=[mesmo valor]`
- Se tem `FB_AD_ACCOUNT_ID`: adicione `AD_ACCOUNT_ID=[mesmo valor]`

Se `ACCESS_TOKEN` ou `AD_ACCOUNT_ID` ja existirem no `.env`, nao sobrescreva.

**Se NAO tiver nenhuma credencial do Facebook Ads:**

Exiba:

```
Para conectar ao Facebook Ads, precisamos do token de acesso e do ID da conta.

Voce ja criou o App no Facebook Developers (developers.facebook.com)?

1. Sim, ja tenho o App criado
2. Nao tenho ainda
```

- **Opcao 1 (ja tem o App):** execute a skill `gerar-token-permanente-facebook-ads`. Ela cria o Usuario do Sistema, atribui a conta de anuncios e gera o token permanente. Apos concluir, retorne aqui e salve tambem `ACCESS_TOKEN=[valor do token gerado]` e `AD_ACCOUNT_ID=[valor do FB_AD_ACCOUNT_ID]` no `.env`.

- **Opcao 2 (nao tem o App):** execute a skill `criar-aplicativo-analise-ads` e depois `gerar-token-permanente-facebook-ads`. Apos concluir, retorne aqui e salve `ACCESS_TOKEN` e `AD_ACCOUNT_ID` como descrito acima.

### CLI-4. Testar a conexao

Execute o teste de conexao com o CLI:

```bash
meta ads insights get --date-preset yesterday --fields spend --format json --no-input
```

- Se retornar JSON com `"data"`: conexao validada. Informe "Conexao com o Facebook Ads confirmada."
- Se retornar erro de autenticacao (codigo 3 ou mensagem de token invalido): o token nao tem permissoes suficientes. Execute novamente a skill `gerar-token-permanente-facebook-ads` e certifique-se de selecionar todas as permissoes.
- Se o comando `meta` nao for reconhecido: verifique se o Python esta no PATH e tente `python -m meta.ads insights get ...`

Continue para o **Passo 0-CANAL**.

---

## PASSO 0-CANAL. Verificar Canal de Envio

Leia `.env`. Se `RELATORIO_CANAL` ja existir com valor `TELEGRAM` ou `WHATSAPP`, pule para o **Passo 0.5**.

Se nao existir, exiba:

```
Por qual canal quer receber o relatorio?

1. Telegram (Recomendado)
2. WhatsApp

Digite o numero:
```

Se o usuario perguntar por que Telegram e recomendado, explique: "O Telegram e gratuito e nao tem risco de bloqueio. Automacoes de mensagem no WhatsApp podem levar ao banimento do numero."

**Se escolher Telegram (opcao 1):**
- Salve `RELATORIO_CANAL=TELEGRAM` no `.env` com `Edit`

**Se escolher WhatsApp (opcao 2):**
- Salve `RELATORIO_CANAL=WHATSAPP` no `.env` com `Edit`
- Exiba o aviso abaixo antes de continuar:

```
Aviso importante sobre WhatsApp:

Automacoes de mensagem tem risco de banimento do numero.
Use um numero secundario aquecido, nunca o numero principal da sua operacao.
```

---

## PASSO 0.5. Verificar Chaves de Canal Existentes

Leia `.env`.

**Se `RELATORIO_CANAL=TELEGRAM`:** verifique `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`.

**Se `RELATORIO_CANAL=WHATSAPP`:** verifique `ZAPI_INSTANCE_ID`, `ZAPI_TOKEN`, `ZAPI_CLIENT_TOKEN`, `RELATORIO_WHATSAPP_NUMERO`.

Se todas as chaves do canal estiverem presentes, pule para o **Passo 2**.

---

## PASSO 1. Coletar Credenciais do Canal de Envio

### 1.1 Credenciais do Canal de Envio

**Se `RELATORIO_CANAL=TELEGRAM`:**

Verifique se `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` existem no `.env`.

Se existirem, avance sem imprimir o token no terminal. Para testar, execute a skill `configurar-telegram`.

Se nao existirem: **execute a skill `configurar-telegram`**

---

**Se `RELATORIO_CANAL=WHATSAPP`:**

```
Agora as credenciais do Z-API para enviar no WhatsApp.

Voce tem conta na Z-API com instancia e WhatsApp conectado?

1. Sim, ja tenho
2. Nao tenho ainda
```

**Se nao tiver (opcao 2):** execute a skill `configurar-zapi`

Pergunte um por vez:

```
Cole o Instance ID da Z-API:
```

```
Cole o Token da Z-API:
```

```
Cole o Client-Token (Security Token):
```

Salve os tres no `.env`.

**Teste de conexao Z-API:**

```bash
python scripts/relatorio-ads-cli.py 1
```

Se o envio concluir sem erro, WhatsApp conectado.

### 1.2 Numero de destino (somente para WhatsApp)

Esta etapa so se aplica se `RELATORIO_CANAL=WHATSAPP`.

```
Para qual numero do WhatsApp devo enviar o relatorio?

Digite no formato internacional sem + e sem espacos.
(ex: 5511999887766)

Lembre: use um numero secundario aquecido, nao o numero principal da operacao.
```

Salve como `RELATORIO_WHATSAPP_NUMERO=valor` no `.env`.

---

## PASSO 2. Escolher Metricas

```
Quais metricas quer ver no relatorio?

1. Basico: gasto, alcance e impressoes
2. Completo: gasto, alcance, impressoes, cliques, CTR, CPM, CPC
3. Completo + conversoes (compras ou leads e custo por resultado)
4. Tudo acima

Digite o numero:
```

Salve a escolha no `.env` como `RELATORIO_METRICAS=1` (ou 2, 3, 4).

---

## PASSO 3. Filtro de Campanhas

```
Quais campanhas incluir no relatorio?

1. Todas as campanhas ativas
2. Todas (ativas e pausadas)
3. Filtrar por nome (eu digo o termo)

Digite o numero:
```

Se opcao 3: pergunte o termo de filtro (ex: "baixo custo", "produto X"). Salve como `RELATORIO_FILTRO_CAMPANHA=valor` no `.env`. Para opcoes 1 e 2, salve `RELATORIO_FILTRO_CAMPANHA=ativas` ou `RELATORIO_FILTRO_CAMPANHA=todas`.

---

## PASSO 4. Confirmacao

Mostre o resumo da configuracao salva:

**Se Telegram:**
```
Configuracao salva.

- Conta Meta Ads: [nome retornado no teste]
- Canal: Telegram (@username_do_bot)
- Metricas: [descricao da escolha]
- Campanhas: [descricao do filtro]

1. Tudo certo
2. Quero ajustar algo
```

**Se WhatsApp:**
```
Configuracao salva.

- Conta Meta Ads: [nome retornado no teste]
- Canal: WhatsApp [numero mascarado, ex: 5511****7766]
- Metricas: [descricao da escolha]
- Campanhas: [descricao do filtro]

1. Tudo certo
2. Quero ajustar algo
```

---

## PASSO 5. Oferecer Envio Imediato

Apos a confirmacao, pergunte:

```
Quer enviar um relatorio agora?

1. Sim, enviar relatorio de ontem
2. Nao, so queria configurar
```

Se opcao 1: execute a skill `enviar-relatorio-ads`. Ela cuida do periodo, busca os dados e envia no canal configurado.

Se opcao 2: encerre com a mensagem abaixo.

---

## PASSO 6. Entrega

```
Configuracao concluida.

Canal: [Telegram ou WhatsApp]
Metricas: [descricao]
Campanhas: [descricao]

Para enviar um relatorio a qualquer momento: /enviar-relatorio-ads
```

---

## CHECKPOINTS OBRIGATORIOS

| Etapa | Aprovacao? |
|---|---|
| Teste de conexao Facebook (CLI) | Confirmado antes de continuar |
| Teste de conexao Telegram ou Z-API | Confirmado antes de continuar |
| Confirmacao geral (resumo) | Sim, obrigatoria |

---

## REGRAS

- Nunca sobrescrever chaves ja existentes no `.env` sem perguntar. Usar `Edit` cirurgico.
- Nao exibir scripts ou arquivos de configuracao no chat. Salvar silenciosamente e informar apenas o caminho.
- Se a conta nao tiver dados no periodo, o relatorio informa "sem dados" e envia assim mesmo.
- Se o usuario ja tem `RELATORIO_CANAL` salvo e quiser trocar de canal: salvar novo valor e refazer o passo de credenciais do novo canal.
- O modo CLI usa `ACCESS_TOKEN` e `AD_ACCOUNT_ID`. Se o `.env` tiver variaveis no formato legado (`FB_ACCESS_TOKEN_PERMANENTE`, `FB_AD_ACCOUNT_ID`), mapear para os nomes do CLI sem remover as originais.
