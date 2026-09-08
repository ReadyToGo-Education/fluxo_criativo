---
name: "source-command-configurar-apify"
description: "Guia para criar conta no Apify, gerar o Personal API Token e salvar no .env como APIFY_API_TOKEN. Skill reutilizável chamada por qualquer skill que dependa do Apify (instagram-dashboard, etc.)."
---

# source-command-configurar-apify

Use this skill when the user asks to run the migrated source command `configurar-apify`.

## Command Template

# Configurar Apify

Guia para criar a conta, gerar o token e salvar no `.env`. So precisa fazer uma vez.

O Apify tem plano gratuito com US$ 5/mes de credito, suficiente para rodar o dashboard do Instagram todo dia e outras automacoes. Nao precisa de cartao de credito para comecar.

---

## Passo 1. Criar a conta

Pergunte:

```
Voce ja tem conta no Apify?

1. Sim, ja tenho
2. Nao tenho ainda
```

**Se nao tiver:** instrua a acessar `https://console.apify.com/sign-up`, criar conta gratuita com email ou Google e voltar quando estiver logado.

**Se ja tiver:** avance para o Passo 2.

---

## Passo 2. Copiar o Personal API Token

Instrua o usuario:

```
Para copiar o token:

1. Acesse https://console.apify.com/settings/integrations
2. Localize a secao "Personal API Tokens"
3. Copie o token listado
```

Peca o token:

```
Cole seu Apify API Token aqui:
```

---

## Passo 3. Testar o token

Rode o teste de conexao com o valor informado:

```bash
curl -s "https://api.apify.com/v2/users/me?token={TOKEN_INFORMADO}" | head -c 300
```

- Se retornar `{"data":{"id":...}}`: token valido, continua.
- Se retornar `{"error":...}`: token invalido ou copiado com espaco. Peca para verificar e colar novamente. Repita o Passo 2.

---

## Passo 4. Salvar no .env

Leia o `.env`.

- Se a linha `APIFY_API_TOKEN` ja existir: atualize o valor com Edit.
- Se nao existir: adicione `APIFY_API_TOKEN={valor}` ao final do arquivo.

O nome padrao obrigatorio da variavel e `APIFY_API_TOKEN`. Nao usar variacao diferente desse nome.

Confirme ao usuario:

```
Token do Apify salvo como APIFY_API_TOKEN e testado com sucesso.
```

---

## Apos configurar

Retorne ao fluxo que chamou esta skill (ex: `/instagram-dashboard`) e continue de onde parou.
