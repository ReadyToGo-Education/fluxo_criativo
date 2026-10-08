---
name: "source-command-configurar-telegram"
description: "Guia para criar um bot no Telegram via BotFather, obter o Chat ID e conectar ao Workshop para envio de relatórios e automações."
---

# source-command-configurar-telegram

Use esta skill quando o usuário pedir o comando `/configurar-telegram` do workshop (ou `configurar-telegram`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/configurar-telegram.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Configurar Telegram

Guia interativo para criar o bot, obter o Chat ID e conectar ao projeto. So precisa fazer uma vez.

---

## O que isso faz?

O Telegram e usado como canal de notificacao do Workshop. Quando voce configura, o assistente consegue enviar mensagens automaticas direto pro seu Telegram, como:

- Relatorio diario de metricas do Facebook Ads (via /ads-relatorio)
- Alertas e notificacoes de campanhas
- Resumos automaticos de performance

Funciona com um "bot" do Telegram (um robozinho que envia mensagens pra voce). Voce cria o bot em 2 minutos, sem programar nada, e ele fica enviando os relatorios no horario que voce escolher.

**Custo:** zero. O Telegram e 100% gratuito, incluindo a API de bots.

---

## Passo 0. Verificar se ja esta configurado

Leia `.env`. Verifique se `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` existem e tem valores nao vazios.

**Se ambos tiverem valor:** teste o envio (Passo 4). Se o teste passar, informe:

```
Seu Telegram ja esta configurado e funcionando.

Nao precisa fazer nada. O bot esta pronto para enviar relatorios.
```

Encerre a skill.

**Se faltar algum dos dois:** siga para o Passo 1.

---

## Passo 1. Criar o bot no BotFather

Pergunte:

```
Voce ja tem um bot do Telegram criado para o Workshop?

1. Sim, ja tenho o token do bot
2. Nao tenho ainda
```

**Se nao tiver:** instrua:

```
Vamos criar seu bot no Telegram (leva 2 minutos):

1. Abra o Telegram no celular ou computador
2. Busque por @BotFather (e o "pai" de todos os bots)
3. Envie o comando: /newbot
4. Escolha um nome para o bot (ex: Relatorio Ads)
5. Escolha um username que termine em "bot" (ex: meurelatorio_ads_bot)
   Se aparecer "Sorry, this username is already taken", escolha um username diferente.
6. O BotFather vai responder com o token do bot

O token tem este formato:
123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Copie esse token e cole aqui.
```

**Se ja tiver:** peca o token:

```
Cole o token do seu bot aqui:
```

---

## Passo 2. Testar o token do bot

Rode o teste de conexao com o valor informado:

```bash
curl -s "https://api.telegram.org/bot{TOKEN_INFORMADO}/getMe" | head -c 300
```

- Se retornar JSON com `{"ok":true,"result":{"id":...,"first_name":"..."}}`: token valido, continua.
- Se retornar `{"ok":false,...}` ou `401`: token invalido. Peca para verificar e colar novamente.

---

## Passo 3. Obter o Chat ID

O Chat ID identifica para qual conversa o bot vai enviar as mensagens.

Instrua o usuario:

```
Agora preciso do seu Chat ID. Faca o seguinte:

1. Abra o Telegram
2. Busque o bot pelo username que voce criou (ex: @meurelatorio_ads_bot)
3. Clique no botao "Iniciar" (ou "Start") que aparece na conversa
   Esse botao so aparece na primeira vez. Se ja tiver iniciado antes, envie qualquer mensagem (ex: "oi").
4. Volte aqui e me avise que fez isso
```

Quando o usuario confirmar, rode:

```bash
curl -s "https://api.telegram.org/bot{TOKEN}/getUpdates"
```

No JSON retornado, localize `result[0].message.chat.id`. Esse e o Chat ID.

**Se `result` vier como array vazio (`[]`):** o bot ainda nao recebeu nenhuma mensagem. Peca para o usuario voltar ao Telegram, abrir a conversa com o bot e clicar em Iniciar (ou enviar uma mensagem). Depois rode o curl novamente.

Quando encontrar o Chat ID, confirme com o usuario:

```
Encontrei seu Chat ID: {CHAT_ID}

Vou testar o envio agora.
```

---

## Passo 4. Testar o envio

Envie uma mensagem de teste:

```bash
curl -s -X POST "https://api.telegram.org/bot{TOKEN}/sendMessage" -H "Content-Type: application/json" -d "{\"chat_id\":\"{CHAT_ID}\",\"text\":\"Teste Workshop Marketing IA. Bot conectado com sucesso.\"}"
```

Interpretacao das respostas:

- `{"ok":true,...}`: bot conectado, mensagem enviada. Peca para o usuario confirmar que recebeu no Telegram.
- `{"ok":false,"error_code":401,...}`: token invalido. Verifique se copiou o token completo do BotFather.
- `{"ok":false,"error_code":400,"description":"Bad Request: chat not found"}`: Chat ID errado. Repita o Passo 3.

---

## Passo 5. Salvar no .env

Leia o `.env`.

Para cada variavel (`TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`):
- Se a linha ja existir: atualize o valor com Edit.
- Se nao existir: adicione ao final do arquivo.

Os nomes obrigatorios das variaveis sao `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`. Nao usar variacao diferente.

Confirme ao usuario:

```
Telegram configurado e testado com sucesso.

Bot: @{username_do_bot}
Chat ID: {CHAT_ID}
```

---

## Apos configurar

Retorne ao fluxo que chamou esta skill (ex: `/ads-relatorio`) e continue de onde parou.

---

## Perguntas frequentes

**Preciso instalar algum programa?**
Nao. Voce so precisa do Telegram instalado no celular ou computador (que voce provavelmente ja tem).

**Quanto custa?**
Zero. O Telegram e 100% gratuito, incluindo a API de bots. Sem limite de mensagens.

**O bot pode ver minhas conversas?**
Nao. O bot so ve as mensagens que voce envia diretamente para ele. Ele nao tem acesso a nenhuma outra conversa.

**Posso usar o mesmo bot para outros projetos?**
Sim. O bot e seu. Voce pode usar o mesmo token em quantos projetos quiser.

**E se eu perder o token do bot?**
Acesse o @BotFather no Telegram, envie /mybots, selecione seu bot e clique em "API Token" para ver novamente. Depois rode /configurar-telegram para atualizar.

**Posso receber os relatorios num grupo?**
Sim. Adicione o bot ao grupo, envie uma mensagem mencionando o bot, e rode /configurar-telegram novamente para pegar o Chat ID do grupo.

---

## Se o usuario nao encontrar uma tela ou opcao descrita

As interfaces mudam com o tempo. Se o usuario disser que nao encontra alguma tela, botao ou opcao descrita neste guia, siga esta ordem:

**1. Fazer WebSearch na documentacao oficial:**

```
site:core.telegram.org BotFather criar bot token
```

Adapte as instrucoes com base no que encontrar. Explique o caminho atualizado ao usuario e continue o processo.

**2. Se mesmo com a busca nao for possivel resolver:**

```
A interface pode ter mudado. Acesse a documentacao oficial:
https://core.telegram.org/bots#how-do-i-create-a-bot

Siga os passos descritos la para criar o bot e obter o token.
Quando tiver o token em maos, volte aqui e cole o valor.
```

---

## Links uteis

- Documentacao de bots do Telegram: https://core.telegram.org/bots
- BotFather: https://t.me/BotFather
