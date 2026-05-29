---
name: workshop-marketing:configurar-imagens
description: Guia para conectar uma API de geração de imagens (OpenRouter) ao projeto. Salva OPENROUTER_API_KEY no .env, usado pela skill /criativo-estatico.
allowed-tools: Read, Edit, Bash
model: sonnet
---

# Configurar Geracao de Imagens com IA

Guia interativo para conectar o OpenRouter ao projeto. So precisa fazer uma vez.

Quando voce usa o comando `/criativo-estatico`, o assistente cria imagens prontas para usar nos seus anuncios do Instagram e Facebook. Imagens profissionais, no tamanho certo, com o estilo que voce escolher.

Para isso funcionar automaticamente, voce precisa conectar uma API de geracao de imagens. E como dar ao assistente acesso a uma "impressora de imagens".

**Sem a API:** o assistente gera os prompts (descricoes detalhadas da imagem) e voce copia e cola manualmente em qualquer gerador de imagem (Midjourney, Leonardo.ai, Freepik (Magnific), etc.).

**Com a API:** o assistente gera a imagem automaticamente e salva na sua pasta de entregas. Pronto para subir no Meta Ads.

---

## Por que o OpenRouter?

O OpenRouter e um "portal" que da acesso a dezenas de modelos de geracao de imagem por um unico cadastro. Com uma chave so, voce usa Flux, DALL-E, Stable Diffusion e outros.

| API | Custo | Qualidade | Facilidade |
|-----|-------|-----------|------------|
| **OpenRouter** (recomendado) | ~US$ 0,01-0,05 por imagem | Alta (varios modelos) | Muito facil |

**Conta de padaria:**
- 1 imagem de teste (Flux Schnell) = ~US$ 0,003 (menos de 1 centavo)
- 1 imagem final (Flux Pro) = ~US$ 0,05
- Se voce gera 20 imagens por mes = ~US$ 1,00
- Voce carrega creditos (minimo US$ 5) e vai usando conforme precisa

---

## Passo 0. Verificar se ja esta configurado

Leia `.env`. Verifique se `OPENROUTER_API_KEY` existe e tem valor nao vazio.

**Se tiver valor:** teste o token (Passo 3). Se o teste passar, informe:

```
Sua chave do OpenRouter ja esta configurada e funcionando.

Nao precisa fazer nada. Pode usar /criativo-estatico direto.
```

Encerre a skill.

**Se nao tiver:** siga para o Passo 1.

---

## Passo 1. Criar conta no OpenRouter

Pergunte:

```
Voce ja tem conta no OpenRouter?

1. Sim, ja tenho
2. Nao tenho ainda
```

**Se nao tiver:** instrua:

```
Para criar sua conta (gratis, sem cartao de credito):

1. Acesse https://openrouter.ai
2. Clique em "Sign Up" (Criar conta)
3. Escolha como quer entrar: Google (mais rapido) ou email + senha
4. Pronto, conta criada

Depois de criar, voce precisa adicionar creditos para gerar imagens:

1. Apos entrar, clique no seu nome (canto superior direito)
2. Clique em "Credits" ou "Billing"
3. Clique em "Add Credits"
4. Escolha o valor (minimo US$ 5, dura meses para geracao de imagem)
5. Preencha os dados de pagamento e confirme

Com US$ 5 voce gera mais de 100 imagens de teste ou cerca de 100 imagens finais. Dura bastante.

Quando estiver com a conta criada e creditos adicionados, me avise.
```

**Se ja tiver:** avance para o Passo 2.

---

## Passo 2. Copiar a chave de API

Instrua o usuario:

```
Para copiar sua chave de API:

1. Acesse https://openrouter.ai/settings/keys
2. Clique em "Create Key" (Criar chave)
3. De um nome para a chave (ex: "Workshop Marketing")
4. Clique em "Create"
5. A chave vai aparecer na tela. Copie imediatamente.

A chave comeca com sk-or-v1- e tem este formato:
sk-or-v1-abc123def456...

Copie TUDO, sem espacos. A chave so aparece uma vez.
Se fechar a pagina sem copiar, gere uma nova.
```

Peca a chave:

```
Cole sua chave do OpenRouter aqui:
```

---

## Passo 3. Testar a chave

Rode o teste de conexao com o valor informado:

```bash
curl -s -H "Authorization: Bearer {CHAVE_INFORMADA}" "https://openrouter.ai/api/v1/models" | head -c 300
```

- Se retornar JSON com `{"data":[...]}`: chave valida, continua.
- Se retornar `{"error":...}` ou `401`: chave invalida ou copiada com espaco. Peca para verificar e colar novamente. Repita o Passo 2.

---

## Passo 4. Salvar no .env

Leia o `.env`.

- Se a linha `OPENROUTER_API_KEY` ja existir: atualize o valor com Edit.
- Se nao existir: adicione `OPENROUTER_API_KEY={valor}` ao final do arquivo.

O nome padrao obrigatorio da variavel e `OPENROUTER_API_KEY`. Nao usar variacao diferente desse nome.

Confirme ao usuario:

```
Chave do OpenRouter salva e testada com sucesso.

Modelo padrao configurado: Flux Schnell (rapido e barato, ideal para testes).
Quando quiser imagens finais de alta qualidade, voce pode trocar para Flux Pro.
```

---

## Passo 5. Escolher o modelo (opcional)

Pergunte:

```
O modelo padrao e o Flux Schnell (rapido, ~US$ 0,003 por imagem). Quer manter esse ou trocar?

1. Manter o Flux Schnell (recomendado para comecar)
2. Trocar para Flux Pro (melhor qualidade, ~US$ 0,05 por imagem)
3. Me explique as opcoes
```

**Se escolher 3**, mostre:

```
Modelos disponiveis:

- Flux Schnell: testes rapidos, rascunhos. Muito rapido, ~US$ 0,003 por imagem.
- Flux 1.1 Pro: imagens finais, alta qualidade. Rapido, ~US$ 0,05 por imagem.
- DALL-E 3: conceitos criativos, texto na imagem. Medio, ~US$ 0,04 por imagem.
- Stable Diffusion 3.5: fotos realistas. Medio, ~US$ 0,04 por imagem.

Recomendacao:
- Para testar ideias: Flux Schnell (padrao)
- Para imagem final do anuncio: Flux Pro
- Para imagem com texto legivel: DALL-E 3
```

Depois pergunte qual quer usar.

**Se escolher 2:** atualize `OPENROUTER_IMAGE_MODEL=black-forest-labs/flux-1.1-pro` no `.env` com Edit.

**Se escolher 1:** mantenha como esta (`black-forest-labs/flux-schnell`).

---

## Apos configurar

Confirme ao usuario:

```
Geracao de imagens configurada.

Voce pode usar agora:
- /criativo-estatico para gerar criativos de anuncio (prompt para colar em ferramenta externa OU geracao automatica via API)
```

Retorne ao fluxo que chamou esta skill (ex: `/criativo-estatico`) e continue de onde parou.

---

## Perguntas frequentes

**Preciso instalar algum programa?**
Nao. Tudo funciona pela internet. As APIs rodam nos servidores deles.

**Quanto custa por mes?**
Depende de quantas imagens voce gera. Com OpenRouter, a maioria dos usuarios gasta menos de US$ 2/mes gerando 20-40 imagens. E pago por uso (sem mensalidade fixa).

**Posso usar as imagens geradas nos meus anuncios?**
Sim. As imagens geradas por IA sao de uso comercial. Voce pode usar em anuncios, posts, paginas, onde quiser.

**E se eu nao quiser pagar nada?**
Sem problema. O assistente gera os prompts detalhados e voce usa qualquer ferramenta gratuita para criar a imagem: Canva, Leonardo.ai (plano free), ou o proprio site do Freepik (Magnific) (com limite de geracoes gratuitas). Use `/criativo-estatico` no modo "prompt" (entrega prompt consolidado em ingles, sem API) para isso.

**Posso trocar de API depois?**
Sim. Basta mudar a chave no arquivo `.env`. O assistente detecta automaticamente qual API esta configurada.

**A qualidade e boa para anuncios profissionais?**
Sim. Os modelos como Flux Pro e DALL-E 3 geram imagens em alta resolucao (1024x1024 ou maior) com qualidade profissional. Para anuncios no Instagram, a resolucao e mais que suficiente.

**E se eu perder minha chave?**
Acesse https://openrouter.ai/settings/keys, apague a chave antiga e crie uma nova. Depois rode `/configurar-imagens` de novo para atualizar.

**Meus creditos expiram?**
Nao. Os creditos do OpenRouter nao expiram. Voce carrega uma vez e usa no seu ritmo.

---

## Links uteis

- OpenRouter: https://openrouter.ai
- Chaves de API: https://openrouter.ai/settings/keys
- Modelos de imagem: https://openrouter.ai/models?modality=image
