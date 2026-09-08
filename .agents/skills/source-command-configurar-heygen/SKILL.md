---
name: "source-command-configurar-heygen"
description: "Guia para conectar uma conta do HeyGen ao projeto (videos com avatar IA). Salva a API key no .env como HEYGEN_API_KEY para ser usada pela skill /video-heygen."
---

# source-command-configurar-heygen

Use this skill when the user asks to run the migrated source command `configurar-heygen`.

## Command Template

# Configurar HeyGen para Videos com Avatar IA

Guia interativo para conectar sua conta do HeyGen ao projeto. So precisa fazer uma vez.

---

## O que e o HeyGen?

O HeyGen e uma plataforma que cria videos com avatares de inteligencia artificial. Voce escolhe (ou cria) um avatar, seleciona uma voz, escreve o roteiro e ele gera um video com o avatar "falando" o texto. Parece uma pessoa real gravando.

Isso serve para:
- Criar anuncios em video sem precisar gravar nada
- Testar diferentes "porta-vozes" para seu produto
- Escalar a producao de conteudo (varios videos por dia)
- Criar versoes diferentes do mesmo video para testar qual converte mais

---

## Quanto custa?

| Plano | Preco | O que inclui | Tem acesso a API? |
|-------|-------|--------------|-------------------|
| Gratuito | R$ 0 | 3 videos/mes, 3 min cada, com marca d'agua, 720p | NAO |
| Creator | ~US$ 29/mes (US$ 24 no anual) | Videos ilimitados, 1080p, sem marca d'agua | SIM |
| Business | ~US$ 149/mes | Tudo do Creator + 4K + time | SIM |

**IMPORTANTE:** O plano gratuito NAO da acesso a API. Pelo plano gratuito voce pode criar videos pelo site do HeyGen (manualmente), mas o comando /video-heygen nao consegue gerar automaticamente.

**Conta de padaria:**
- Um video de 60 segundos custa ~US$ 0,50 em creditos
- Se voce faz 10 videos por mes = US$ 5
- O plano Creator (US$ 29/mes) inclui 15 minutos = ~15 videos de 60s
- Compensa a partir de 5-10 videos por mes

**Recomendacao para comecar:**
1. Crie a conta gratuita e teste pelo site (app.heygen.com)
2. Quando gostar do resultado, assine o Creator
3. Pegue a chave de API e conecte aqui

---

## Passo 0. Verificar se ja esta configurado

Leia `.env`. Verifique se `HEYGEN_API_KEY` existe e tem valor nao vazio.

**Se tiver valor:** teste a chave (Passo 3). Se o teste passar, informe:

```
Sua chave do HeyGen ja esta configurada e funcionando.

Nao precisa fazer nada. Pode usar /video-heygen direto.
```

Encerre a skill.

**Se nao tiver:** siga para o Passo 1.

---

## Passo 1. Criar conta no HeyGen

Pergunte:

```
Voce ja tem conta no HeyGen?

1. Sim, ja tenho (plano Creator ou superior)
2. Sim, tenho conta gratuita
3. Nao tenho ainda
```

**Se nao tiver (opcao 3):** instrua:

```
Para criar sua conta (gratis, sem cartao de credito):

1. Acesse https://heygen.com
2. Clique em "Get started for free"
3. Escolha como quer entrar: Google (mais rapido) ou email + senha
4. Pronto, conta criada

Antes de pegar a API, vale explorar o HeyGen pelo site:
- Clique em "Create Video" para ver como funciona
- Escolha um avatar da biblioteca (tem centenas de opcoes)
- Escreva um texto curto e clique em "Submit"
- O HeyGen vai gerar um video de teste para voce ver a qualidade

Quando quiser gerar videos pelo assistente automaticamente, assine o plano Creator
(US$ 29/mes ou US$ 24/mes no anual) e volte aqui.

Me avise quando estiver pronto.
```

**Se tiver conta gratuita (opcao 2):**

```
A conta gratuita nao da acesso a API. Voce pode criar videos manualmente pelo site
(app.heygen.com), mas o comando /video-heygen precisa do plano Creator.

Para assinar:
1. Entre no painel do HeyGen
2. Clique no seu avatar (canto superior direito)
3. Clique em "Pricing" ou "Upgrade"
4. Escolha o plano Creator (US$ 29/mes ou US$ 24/mes no anual)

Quando assinar, me avise que eu te guio para pegar a chave de API.
```

**Se ja tiver conta Creator ou superior (opcao 1):** avance para o Passo 2.

---

## Passo 2. Copiar a chave de API

Instrua o usuario:

```
Para copiar sua chave de API:

1. Entre no painel: https://app.heygen.com
2. Clique no seu avatar ou foto (canto superior direito)
3. Clique em "Settings" (Configuracoes)
4. No menu do lado esquerdo, clique em "API"
5. Copie a chave (ou clique em "Generate" se for a primeira vez)

A chave e uma sequencia longa de letras e numeros, tipo:
MGRlMjM1MzBlOTAzNDY5MmI3YjY4ZjQ5...

Copie TUDO, sem espacos. A chave so aparece uma vez.
Se perder, gere uma nova (a antiga para de funcionar).
```

Peca a chave:

```
Cole sua chave do HeyGen aqui:
```

---

## Passo 3. Testar a chave

Rode o teste de conexao com o valor informado:

```bash
curl -s -H "X-Api-Key: {CHAVE_INFORMADA}" "https://api.heygen.com/v2/avatars" | head -c 300
```

- Se retornar JSON com `{"data":...}` ou lista de avatares: chave valida, continua.
- Se retornar `{"code":401,...}` ou `unauthorized`: chave invalida. Peca para verificar e colar novamente. Repita o Passo 2.
- Se retornar erro de permissao ou `403`: conta pode estar no plano gratuito (sem acesso a API). Oriente a assinar o plano Creator.

---

## Passo 4. Salvar no .env

Leia o `.env`.

- Se a linha `HEYGEN_API_KEY` ja existir: atualize o valor com Edit.
- Se nao existir: adicione `HEYGEN_API_KEY={valor}` ao final do arquivo (ou na secao correspondente, se existir).

O nome padrao obrigatorio da variavel e `HEYGEN_API_KEY`. Nao usar variacao diferente desse nome.

Confirme ao usuario:

```
Chave do HeyGen salva e testada com sucesso.

Voce ja pode usar o comando /video-heygen para criar videos com avatar IA.
```

---

## Passo 5. Avatar e voz favoritos (opcional)

Pergunte:

```
Quer escolher um avatar e uma voz padrao agora? Assim nao precisa escolher toda vez.

1. Sim, quero escolher agora
2. Nao, prefiro escolher na hora de criar o video
```

**Se escolher 1:**

Liste os avatares disponiveis:

```bash
curl -s -H "X-Api-Key: {CHAVE}" "https://api.heygen.com/v2/avatars" | head -c 2000
```

Mostre os 5-10 primeiros avatares com nome e ID. Peca para o usuario escolher. Salve o ID no `.env` como `HEYGEN_AVATAR_ID={id}` com Edit.

Para vozes, liste as opcoes em portugues:

```bash
curl -s -H "X-Api-Key: {CHAVE}" "https://api.heygen.com/v2/voices" | head -c 2000
```

Filtre vozes em portugues (pt-BR), mostre as opcoes e peca para escolher. Salve como `HEYGEN_VOICE_ID={id}` com Edit.

**Se escolher 2:** encerre normalmente. O /video-heygen lista as opcoes na hora.

---

## Apos configurar

Confirme ao usuario:

```
HeyGen configurado.

Voce pode usar agora:
- /video-heygen para criar videos com avatar IA (escreva o roteiro antes)
```

Retorne ao fluxo que chamou esta skill (ex: `/video-heygen`) e continue de onde parou.

---

## Perguntas frequentes

**Preciso instalar algum programa?**
Nao. Tudo funciona pela internet. O HeyGen roda nos servidores deles.

**Posso usar minha propria foto como avatar?**
Sim. O /video-heygen tem a opcao de enviar uma foto e o HeyGen transforma em avatar falante. A foto precisa ser de rosto frontal, bem iluminada.

**Posso usar foto do Pinterest ou banco de imagens?**
Sim. Pode usar qualquer foto de rosto frontal. Muitos infoprodutores usam fotos de banco de imagens para criar um "porta-voz" para o produto.

**Quanto tempo leva para gerar um video?**
Entre 2 e 5 minutos, dependendo da duracao do roteiro.

**Posso cancelar o plano depois?**
Sim. O plano Creator e mensal e pode ser cancelado a qualquer momento.

**A qualidade e boa para anuncios?**
Sim. O HeyGen gera videos em 1080p (Full HD) no plano Creator, que e a qualidade padrao para Reels e anuncios no Meta Ads.

**Posso clonar minha propria voz?**
Sim. O HeyGen tem recurso de clonagem de voz. Voce envia um audio de ~30 segundos falando naturalmente e ele cria uma voz sintetica que soa como voce. Essa opcao esta disponivel no plano Creator.

**E se eu perder minha chave de API?**
Acesse app.heygen.com > Settings > API, gere uma nova chave e rode /configurar-heygen novamente para atualizar.

---

## Links uteis

- Site do HeyGen: https://heygen.com
- Painel (login): https://app.heygen.com
- Precos: https://heygen.com/pricing
- Precos da API: https://heygen.com/api-pricing
- Documentacao da API: https://docs.heygen.com
- Suporte: https://help.heygen.com
