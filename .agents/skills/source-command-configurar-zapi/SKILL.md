---
name: "source-command-configurar-zapi"
description: "Guia para criar conta na Z-API, configurar uma instância e conectar o WhatsApp para envio de mensagens automatizadas."
---

# source-command-configurar-zapi

Use this skill when the user asks to run the migrated source command `configurar-zapi`.

## Command Template

# Configurar Z-API

Guia interativo para criar a conta, configurar a instancia e conectar o WhatsApp. So precisa fazer uma vez.

---

## O que e a Z-API?

A Z-API e um servico que permite enviar mensagens de WhatsApp de forma automatizada. Com ela conectada, o assistente consegue enviar relatorios, notificacoes e mensagens direto pelo WhatsApp, sem voce precisar fazer nada manualmente.

Isso serve para:
- Receber relatorios diarios de metricas do Facebook Ads no WhatsApp
- Enviar lembretes automaticos para leads e clientes
- Automatizar follow-up pos-evento

**Custo:** a Z-API tem plano gratuito para testes (limitado). O plano pago comeca em ~R$ 60/mes por instancia.

**Atencao:** automacoes no WhatsApp tem risco de banimento do numero. Use um numero secundario aquecido, nunca o numero principal da operacao. O Telegram (/configurar-telegram) e a opcao mais segura e gratuita para relatorios.

---

## Passo 0. Verificar se ja esta configurado

Leia `.env`. Verifique se `ZAPI_INSTANCE_ID`, `ZAPI_TOKEN` e `ZAPI_CLIENT_TOKEN` existem e tem valores nao vazios.

**Se os tres tiverem valor:** teste a instancia (Passo 4). Se o teste passar, informe:

```
Sua Z-API ja esta configurada e conectada.

Nao precisa fazer nada. O WhatsApp esta pronto para enviar mensagens.
```

Encerre a skill.

**Se faltar algum:** siga para o Passo 1.

---

## Passo 1. Criar conta na Z-API

Pergunte:

```
Voce ja tem conta na Z-API?

1. Sim, ja tenho
2. Nao tenho ainda
```

**Se nao tiver:** instrua:

```
Para criar sua conta:

1. Acesse https://app.z-api.io
2. Crie sua conta com email ou Google
3. Pronto, conta criada

Quando estiver logado, me avise.
```

**Se ja tiver:** avance para o Passo 2.

---

## Passo 2. Criar e conectar a instancia

Instrua o usuario:

```
Agora vamos criar a instancia (e a "linha" que conecta ao seu WhatsApp):

1. No menu lateral da Z-API, clique em "Instancias Web"
2. Clique em "Adicionar"
3. De um nome para a instancia (ex: "Numero do Relatorio")
4. Role ate o final da tela e clique em "Salvar"
5. Na lista de instancias, clique na que acabou de criar
6. Clique em "Assinar" para ativar a assinatura (obrigatorio para liberar o QR Code)
7. Apos assinar, o QR Code aparece na mesma tela
8. Abra o WhatsApp no celular e escaneie o QR Code (mesmo processo do WhatsApp Web)
9. Aguarde a confirmacao de conexao

Quando estiver conectado, me avise.
```

---

## Passo 3. Copiar as credenciais

Instrua o usuario:

```
Agora preciso de 3 dados da sua instancia. Copie um por vez:

1. Instance ID e Token: estao na mesma tela da instancia (apos conectar)
2. Client-Token: no menu lateral, clique em "Seguranca" > "Gerar Token de seguranca da conta"

O Client-Token so aparece uma vez. Copie e guarde.
```

Peca cada credencial:

```
Cole seu Instance ID:
```

Depois:

```
Cole seu Token:
```

Depois:

```
Cole seu Client-Token (Security Token):
```

---

## Passo 4. Testar a instancia

Rode o teste de conexao com os valores informados:

```bash
curl -s "https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}/status" -H "Client-Token: {CLIENT_TOKEN}"
```

Interpretacao das respostas:

- `{"connected":true}`: WhatsApp conectado, instancia pronta. Continua para o Passo 5.
- `{"connected":false}`: instancia existe mas WhatsApp nao esta conectado. Oriente a voltar ao Passo 2 e escanear o QR Code novamente.
- `{"error":"To continue sending a message, you must subscribe to this instance again"}`: assinatura expirada ou nao ativada. Oriente a acessar app.z-api.io, abrir a instancia e clicar em "Assinar".
- `{"error":"...unauthorized..."}` ou status 401: credenciais invalidas. Peca para verificar e colar novamente. Repita o Passo 3.

---

## Passo 5. Salvar no .env

Leia o `.env`.

Para cada variavel (`ZAPI_INSTANCE_ID`, `ZAPI_TOKEN`, `ZAPI_CLIENT_TOKEN`):
- Se a linha ja existir: atualize o valor com Edit.
- Se nao existir: adicione ao final do arquivo (ou na secao correspondente, se existir).

Os nomes obrigatorios sao `ZAPI_INSTANCE_ID`, `ZAPI_TOKEN` e `ZAPI_CLIENT_TOKEN`. Nao usar variacao diferente.

Confirme ao usuario:

```
Z-API configurada e testada com sucesso.

Instance ID: {INSTANCE_ID}
Status: WhatsApp conectado
```

---

## Passo 6. Numero de destino (opcional)

Pergunte:

```
Quer salvar um numero padrao para receber os relatorios?

1. Sim (cole o numero com DDD, ex: 11999998888)
2. Nao, prefiro informar na hora
```

Se escolher 1: salve como `RELATORIO_WHATSAPP_NUMERO={numero}` no `.env` com Edit.

---

## Apos configurar

Confirme ao usuario:

```
Z-API configurada.

Voce pode usar agora:
- /ads-relatorio para configurar o envio diario de metricas pelo WhatsApp
- /enviar-relatorio-ads para enviar um relatorio agora mesmo
```

Retorne ao fluxo que chamou esta skill (ex: `/ads-relatorio`) e continue de onde parou.

---

## Perguntas frequentes

**Preciso instalar algum programa?**
Nao. A Z-API funciona pela internet. Voce so precisa do WhatsApp instalado no celular (que ja tem).

**Quanto custa?**
O plano pago comeca em ~R$ 60/mes por instancia. Tem periodo de teste gratuito para validar.

**Posso usar meu numero principal?**
Nao recomendamos. Automacoes no WhatsApp podem resultar em banimento do numero. Use um numero secundario, preferencialmente aquecido (com historico de conversas normais).

**O que e "aquecer" um numero?**
E usar o numero normalmente por algumas semanas antes de conectar a automacao. Envie e receba mensagens reais, entre em grupos, mande audios. Isso reduz o risco de o WhatsApp identificar como spam.

**E se o WhatsApp desconectar?**
Volta ao painel da Z-API (app.z-api.io), abre a instancia e escaneia o QR Code novamente. As credenciais no .env continuam as mesmas.

**Por que o Telegram e mais recomendado?**
O Telegram e gratuito, sem risco de banimento e sem limite de mensagens. A Z-API so vale a pena se voce PRECISA que o relatorio chegue no WhatsApp especificamente.

**E se eu perder o Client-Token?**
Acesse app.z-api.io > Seguranca > gere um novo token. Depois rode /configurar-zapi para atualizar.

---

## Se o usuario nao encontrar uma tela ou opcao descrita

As interfaces mudam com o tempo. Se o usuario disser que nao encontra alguma tela, botao ou opcao descrita neste guia:

**1. Fazer WebSearch na documentacao oficial:**

```
site:developer.z-api.io criar instancia conectar whatsapp
```

Adapte as instrucoes com base no que encontrar.

**2. Se mesmo com a busca nao for possivel resolver:**

```
A interface pode ter mudado. Acesse a documentacao oficial:
https://developer.z-api.io

Procure pelos passos de criacao de instancia e obtencao das credenciais.
Quando tiver Instance ID, Token e Client-Token em maos, volte aqui e cole os valores.
```

---

## Links uteis

- Painel da Z-API: https://app.z-api.io
- Documentacao: https://developer.z-api.io
