---
name: "source-command-avat-whisk"
description: "Gerar briefings visuais prontos para o Whisk (Google Labs). Cria os 3 inputs do Whisk (Subject, Scene, Style) para anuncios, carrossel e capa de produto, mantendo personagem e estetica consistentes entre pecas."
---

# source-command-avat-whisk

Use this skill when the user asks to run the migrated source command `avat-whisk`.

## Command Template

# Imagem com Whisk. Briefings Visuais para Personagem Consistente

Gera briefings prontos para colar no Whisk (labs.google/fx/tools/whisk). O Whisk nao trabalha com prompt de texto, ele usa 3 entradas visuais: **Subject** (quem aparece), **Scene** (onde) e **Style** (como). Esta skill monta essas 3 entradas alinhadas ao perfil do produto ativo e garante que o mesmo personagem apareca em todas as pecas.

## Usage

```
/avat-whisk
```

## Por Que Whisk

- Mantem o mesmo personagem em varias imagens, coisa que DALL-E e Flux nao fazem bem
- Nao precisa de API, funciona no navegador (labs.google/fx/tools/whisk)
- Ideal para criar uma "marca visual" com um avatar fictcio ou foto real do aluno
- Usa Imagen 3 + Gemini por baixo

**Limitacao:** Whisk nao tem API publica. Esta skill nao gera a imagem automaticamente. Ela entrega o briefing pronto e voce faz o upload no site.

## O Que Fazer

### 0. Contexto

Leia `meus-produtos/.ativo`, depois `meus-produtos/{ativo}/perfil.md` e `meus-produtos/{ativo}/idconsumidor.md`. Se nao existirem, oriente o aluno a rodar `/produto-editar` primeiro.

Extraia:
- Quadro (transformacao principal)
- Nicho e publico
- 3 Urgencias Ocultas mais fortes (Dores, Desejos, Urgencias Quentes)
- Identidade do Consumidor (tom, estetica preferida, cultura visual)

### 1. Entrevista (UMA pergunta por vez, com progresso visual)

**Bloco 1/5. Caso de uso:**

```
O que voce quer criar no Whisk?

1. Imagens para anuncios (Meta Ads, formato 1:1 ou 4:5)
2. Carrossel de Instagram (10 frames do mesmo personagem)
3. Capa de produto (e-book, mockup, modulo de curso)
4. Pacote completo (anuncios + carrossel + capa)

Digite o numero:
```

```
--- Bloco 1/5 concluido ---
Caso de uso: [escolha]
Proximo: Personagem principal
---
```

**Bloco 2/5. Personagem (Subject):**

```
Quem vai aparecer nas imagens?

1. Voce mesmo (tenho foto minha para usar no Whisk)
2. Personagem fictcio (mulher/homem com caracteristicas especificas)
3. Objeto ou simbolo do produto (nada de pessoa)
4. Mao/silhueta (meio caminho, sem rosto)

Digite o numero:
```

Se escolher 1: pergunte se a foto ja existe em algum lugar e instrua a deixar ela em `meus-produtos/{ativo}/entregas/criativos/whisk-assets/subject.jpg` antes de subir no Whisk.

Se escolher 2: faca perguntas curtas, UMA por vez:
- Idade aparente
- Estilo (ex: empresaria moderna, mae de familia, atleta, mistica)
- Traco marcante (ex: cabelo cacheado, oculos, tattoo)

Se escolher 3 ou 4: pergunte qual objeto/simbolo representa o produto.

```
--- Bloco 2/5 concluido ---
Subject: [descricao]
Proximo: Estetica visual
---
```

**Bloco 3/5. Estilo (Style):**

Baseado na identidade do consumidor, sugira 3 esteticas que combinam:

```
Qual estetica visual?

1. [Estetica A sugerida com base no perfil]
2. [Estetica B sugerida]
3. [Estetica C sugerida]
4. Outro (descreva)

Digite o numero:
```

Sugestoes possiveis:
- Foto de celular com luz natural (autentica, funciona para anuncios)
- Editorial minimalista (capa de e-book premium)
- Ilustracao flat colorida (carrossel educativo)
- Cinematografica com cor quente (transformacao/resultado)
- Documental preto e branco (autoridade)

```
--- Bloco 3/5 concluido ---
Style: [estetica]
Proximo: Cenas
---
```

**Bloco 4/5. Cenas (Scenes):**

Dependendo do caso de uso, determine quantas cenas precisam ser geradas:

- Anuncios: 3 cenas (gancho de dor, gancho de desejo, prova/resultado)
- Carrossel: 10 cenas, uma por slide (abertura, 3 dores, 3 quebras de objecao, transformacao, CTA, encerramento)
- Capa: 1 cena principal + 2 variacoes para modulos
- Pacote completo: soma dos tres

Gere as descricoes de cena automaticamente a partir das Urgencias Ocultas do perfil. Nao pergunte cena por cena. Mostre as cenas prontas:

```
Gerei [N] cenas baseadas nas Urgencias Ocultas do seu perfil:

1. [Nome da cena]. [descricao visual em portugues]
2. [Nome da cena]. [descricao visual em portugues]
...

1. Aprovar as cenas
2. Quero ajustar alguma
```

**Bloco 5/5. Texto na imagem:**

```
Quer texto nas imagens?

1. Sim, vou adicionar overlay depois no Canva
2. Sim, quero que o Whisk gere com texto (aviso: Whisk gera texto ruim, nao recomendado)
3. Sem texto

Digite o numero:
```

```
--- Bloco 5/5 concluido ---
Caso de uso: [caso]
Subject: [subject]
Style: [style]
Scenes: [N cenas]
Texto: [opcao]
---
```

### 2. Confirmacao

```
Resumo do que vou preparar:

- Caso de uso: [caso]
- Personagem: [subject]
- Estetica: [style]
- Cenas: [N cenas baseadas em Urgencias Ocultas]
- Texto: [opcao]

Vou entregar:
1. Um arquivo whisk-briefings.md com todos os 3 inputs prontos
2. Instrucoes passo a passo de como usar no labs.google/fx/tools/whisk
3. Estrutura de pastas para voce salvar as imagens geradas e reutilizar

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 3. Geracao do Briefing

Crie o arquivo `meus-produtos/{ativo}/entregas/criativos/whisk-briefings.md` com esta estrutura:

```markdown
# Whisk. Briefings Visuais

Produto: {nome do produto}
Caso de uso: {caso}
Data: {data de hoje}

## Como Usar

1. Acesse https://labs.google/fx/tools/whisk
2. Faca login com conta Google
3. Na tela inicial voce vera 3 boxes: **Subject**, **Scene**, **Style**
4. Para cada box, voce tem duas opcoes:
   - Upload de imagem (ideal, melhor resultado)
   - Clicar em "Describe" e colar o texto deste briefing
5. Para cada cena abaixo, troque apenas o Scene e mantenha Subject e Style identicos
6. Isso garante o mesmo personagem em todas as imagens

## Subject (fixo em todas as cenas)

**Descricao para colar no box Subject:**
```
{descricao do personagem, em ingles, com detalhes visuais}
```

**Ou suba esta imagem:**
{caminho sugerido. meus-produtos/{ativo}/entregas/criativos/whisk-assets/subject.jpg}

## Style (fixo em todas as cenas)

**Descricao para colar no box Style:**
```
{descricao da estetica, em ingles}
```

## Cenas

### Cena 1. {nome da cena}

**Urgencia Oculta usada:** {item exato do perfil}

**Descricao para colar no box Scene:**
```
{descricao da cena, em ingles}
```

**Conceito (em portugues):**
{o que a imagem vai comunicar e por que}

**Onde usar:**
{ex: anuncio de descoberta, slide 1 do carrossel, capa do modulo 1}

**Nome do arquivo esperado:**
meus-produtos/{ativo}/entregas/criativos/whisk-{caso}-01.png

---

### Cena 2. {nome}
... (repetir estrutura)
```

**Regras para os prompts em ingles:**
- Subject: maximo 2 frases, foco em aparencia fisica e postura
- Style: maximo 2 frases, foco em tipo de foto/ilustracao, iluminacao e paleta
- Scene: 2 a 3 frases, foco em acao, ambiente e composicao. Nao repetir o Subject aqui.
- Nao usar "—" em nenhum lugar
- Nao pedir texto dentro da imagem (Whisk e ruim com texto)

### 4. Aprovacao

Mostre o conteudo completo do whisk-briefings.md ao usuario:

```
1. Aprovar e salvar
2. Quero ajustar algo
```

Apos aprovacao, salve o arquivo e crie a pasta vazia `meus-produtos/{ativo}/entregas/criativos/whisk-assets/` com um README.md explicando:
- subject.jpg. foto do personagem (se for foto real)
- style-ref.jpg. referencia de estetica opcional
- Imagens geradas vao para a pasta pai (`whisk-{caso}-NN.png`)

### 5. Entrega e Proximo Passo

```
Briefing pronto.

Salvei em:
- meus-produtos/{ativo}/entregas/criativos/whisk-briefings.md
- meus-produtos/{ativo}/entregas/criativos/whisk-assets/ (pasta para suas imagens de referencia)

Proximo passo:

1. Abra labs.google/fx/tools/whisk no navegador
2. Siga a secao "Como Usar" do arquivo whisk-briefings.md
3. Para cada cena, troque apenas o Scene e mantenha Subject e Style fixos
4. Baixe as imagens e salve em meus-produtos/{ativo}/entregas/criativos/ com o nome indicado em cada cena
5. Depois volte aqui e use:
   - /copy-anuncio. para escrever a copy dos anuncios que vao usar essas imagens
   - /copy-carrossel. para montar o carrossel com as imagens
   - /video-remotion. para jogar as cenas num video
```

### 6. Modo Iterativo

Se o usuario pedir para adicionar ou refinar cenas depois:

```
O que quer fazer?

1. Adicionar N cenas novas ao briefing existente
2. Trocar a estetica (Style) de todas as cenas
3. Trocar o personagem (Subject) de todas as cenas
4. Refinar uma cena especifica
```

Ajuste apenas a parte solicitada e atualize o arquivo whisk-briefings.md, mantendo a numeracao coerente.

## Regras

- Sempre usar as Urgencias Ocultas reais do perfil como base das cenas. Nunca inventar dor ou desejo que nao esta la.
- Subject e Style precisam ser identicos em todas as cenas do mesmo briefing. Essa e a razao de usar Whisk.
- Nao usar travessao em lugar nenhum do arquivo.
- Nao gerar texto dentro das imagens via Whisk. Orientar o aluno a fazer overlay de texto no Canva ou direto nas skills de copy.
- Nao prometer que o Whisk tem API. Deixar claro que o fluxo e manual.
