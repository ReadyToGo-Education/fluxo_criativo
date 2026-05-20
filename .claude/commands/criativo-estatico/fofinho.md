# Fofinho. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 17 (Fofinho). Cria criativos com ilustração 3D hiper-detalhada estilo Pixar moderno (Toy Story 4, Monstros SA, Elemental) onde um elemento específico do nicho é transformado em personagem/bichinho ultra fofo. Gera 10 ideias, o aluno escolhe uma, e a sub-skill entrega título, legenda longa, prompt Feed pro ChatGPT, prompt de animação pro Freepik com sugestão de música, e pergunta se quer o prompt no formato Stories também.

**Por que esse formato funciona:**
A fofura extrema para o scroll. O elemento do nicho transformado em bichinho 3D é imediatamente reconhecível como pertencente àquele universo, então a pessoa identifica o tema antes mesmo de perceber que é anúncio. A renderização tipo frame de filme Pixar (não cartoon 2D, não foto) gera o efeito "que fofo!" que faz parar, ler o título e as 3 promessas. A imagem é compartilhável pela fofura, o título e as promessas vendem.

## O que você está criando

Anúncios que parecem:
- frame de filme Pixar moderno
- post que faz a pessoa parar e falar "que fofo!"
- conteúdo compartilhável pela fofura extrema
- imagem que dá vontade de apertar

## O que você NUNCA cria

- Bichinhos genéricos sem conexão com o nicho (gatinho aleatório, ursinho genérico)
- Cartoon 2D plano sem textura
- Foto realista ou UGC
- Estética de banco de imagem
- Marketing óbvio na imagem
- Elementos que servem pra qualquer nicho. Cada criativo precisa ser ÚNICO pro nicho

## Regra de ouro

A cena precisa de 3 coisas:

1. **ELEMENTO DO NICHO COMO PERSONAGEM**. Um objeto/ferramenta/símbolo específico do nicho transformado em bichinho fofo 3D (frasco de sérum vira bichinho, notebook vira personagem, tênis de corrida vira criatura). Reconhecível em 1 segundo como sendo daquele nicho.
2. **FOFURA EXTREMA**. Proporções exageradas (olhos enormes, bochechas rosadas, patinhas gordinhas), texturas reais (plástico, vidro, pelúcia, metal), iluminação cinematográfica. Nível gatinho do Shrek.
3. **3 PROMESSAS DE VIDA BONITINHA**. Desejos reais do público conectados ao nicho.

## Fluxo da conversa

Siga os 4 passos abaixo em ordem.

### PASSO 1. Briefing

Se `meus-produtos/{ativo}/perfil.md` existe (orquestrador `/criativo-estatico` já carregou o contexto, ou a sub-skill foi chamada com produto ativo definido), pergunte:

```
Usar dados do produto ativo ou informar manualmente?

1. Usar dados do produto ativo
2. Informar manualmente
```

Se escolher 1, extraia produto, nicho e público do `perfil.md` / `idconsumidor.md` e siga pro PASSO 2.

Se escolher 2 (ou se não existe `perfil.md`), pergunte apenas:

- Qual o produto/serviço?
- Qual o público?

Pare e espere a resposta.

### PASSO 2. 10 ideias de "Fofinho"

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de Fofinho do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Com base no briefing, gere 10 ideias. Cada ideia deve conter:

- **CENA**. Descrição curta do elemento do nicho transformado em personagem 3D fofo + o que está fazendo.
- **TÍTULO**. Frase fofa e acolhedora conectada ao nicho.
- **3 PROMESSAS**. 3 desejos reais do público com tracinho (—), todos com nicho presente.
- **CTA**. "Clique aqui para [ação] + [produto/nicho]" 👉.

#### Regras das 10 ideias

- TODOS os elementos fofos precisam ser OBJETOS/FERRAMENTAS/SÍMBOLOS ESPECÍFICOS DO NICHO transformados em personagens.
- Nunca bichinhos genéricos desconectados do nicho (gatinho aleatório, ursinho genérico).
- Cada personagem fofo precisa ser reconhecível como pertencente ao nicho em 1 segundo.
- Variar os objetos do nicho (se é skincare: frasco, potinho, conta-gotas, máscara, protetor. Se é corrida: tênis, medalha, relógio, garrafa).
- Todos os títulos e promessas com nicho claro.
- A CTA SEMPRE contém "Clique aqui" + o nome do nicho/produto.

#### Apresentação

Mostre as 10 ideias numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de Fofinho pro seu nicho.

---

**1.**
**CENA:** [elemento do nicho como personagem 3D fofo + o que está fazendo]
**TÍTULO:** "[frase fofa conectada ao nicho]"
**3 PROMESSAS:**
— [Promessa 1 com nicho claro]
— [Promessa 2 com nicho claro]
— [Promessa 3 com nicho claro]
**CTA:** Clique aqui para [ação] + [produto/nicho] 👉

---

**2.**
...

---

Escolha uma ideia.
```

### PASSO 3. Desenvolvimento e aprovação

Quando o aluno escolher um número de 1 a 10, anuncie. Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

```
🔍 Próximo passo: desenvolver a ideia escolhida e gerar a legenda. Tempo estimado: cerca de 30 segundos.
```

Desenvolva:

```
TÍTULO: "[frase fofa conectada ao nicho]"

CENA: [elemento do nicho como personagem 3D fofo. Descrição detalhada: material, textura, olhinhos, expressão, o que está fazendo. Estilo Pixar moderno.]

3 PROMESSAS:
"— [Promessa 1 com nicho claro]"
"— [Promessa 2 com nicho claro]"
"— [Promessa 3 com nicho claro]"

CTA: Clique aqui para [ação] + [produto/nicho] 👉
```

**LEGENDA DO INSTAGRAM (longa, com lead e CTA):**

Mínimo de 3 linhas, redigida em primeira pessoa, tom de creator brasileiro casual e acolhedor. Estrutura:

- **Lead forte**. Frase de abertura acolhedora que puxa identificação.
- **O antes**. 4 a 6 linhas curtas mostrando a frustração anterior.
- **A virada**. O momento onde o produto/método entrou.
- **O resultado**. A conquista que veio.
- **CTA**. Chamada direta pro link com emoji 👉.

Light Copy aplicada. Padrão de Legenda (ver Regras no fim deste arquivo) obrigatório:
- Tom de escritor, não de vendedor.
- Ensina ou avisa, nunca vende.
- Especificidade mata generalização.
- Produto não aparece no início.
- Sem travessão (—), sem ponto de exclamação, sem "Não é X. É Y.", sem frases genéricas de vendedor.
- Sem "mesmo que" e "sem precisar" como muleta, sem lero-lero, sem promessa vaga.
- Sem emojis dentro do texto (exceto o 👉 final do CTA).

Depois de entregar, escreva:

**"Aprovou? Se sim, eu gero o prompt da imagem e o de animação."**

### PASSO 4. Prompts prontos (Legenda + Imagem + Animação)

Quando o aluno aprovar, entregue tudo junto.

#### A) Legenda do Instagram

Texto final pronto pra colar.

#### B) Prompt de Feed (4:5) pro ChatGPT

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.** Aplicar o Padrão de Personagem (ver Regras) na descrição de qualquer pessoa que apareça no cenário de fundo.

````
Cria pra mim uma ilustração 3D ultra fofa e hiper-detalhada pra anúncio de Instagram. Estilo PIXAR MODERNO / TOY STORY / MONSTROS SA — renderização 3D com texturas reais, iluminação cinematográfica, como se os objetos existissem de verdade. NÃO é cartoon 2D. É 3D hiper-realista fofo.

A IMAGEM:
[DESCRIÇÃO DETALHADA DO ELEMENTO DO NICHO COMO PERSONAGEM 3D:
- Qual objeto do nicho é (frasco, notebook, tênis, panela, etc.)
- Material e textura real (plástico brilhante, vidro reflexivo, borracha, metal, papel, tecido)
- Olhinhos enormes de vidro brilhante e reflexivos
- Bochechas rosadas, sorriso, expressão
- Patinhas/bracinhas gordinhas
- O que está fazendo
- Outros elementos do nicho ao redor (menores, também com carinhas se fizer sentido)]

[DESCRIÇÃO DO CENÁRIO: contexto do nicho levemente desfocado ao fundo. Iluminação cinematográfica quente, sombras suaves e realistas. Profundidade de campo rasa focando no personagem principal.]

ESTILO VISUAL:
- Renderização 3D hiper-detalhada estilo PIXAR MODERNO (Toy Story 4, Monstros SA, Elemental)
- Texturas reais em cada superfície (plástico, metal, papel, vidro, borracha, tecido)
- Iluminação cinematográfica com reflexos e sombras realistas
- Proporções exageradas de fofura mas com acabamento realista
- Profundidade de campo rasa, bokeh suave no fundo
- Parece frame de filme Pixar, não cartoon 2D
- Todos os elementos são do universo de [NICHO]
- Nível de fofura: Pixar moderno com textura de tocar

REGRA CRÍTICA DE ENQUADRAMENTO: o personagem principal fica no centro da imagem. O TERÇO SUPERIOR tem espaço livre (fundo desfocado) pro título ficar sem cobrir o personagem. O título fica no topo, sobre o fundo.

TEXTO NA IMAGEM — ESTILO TIKTOK/STORIES NATIVO:

Todos os textos direto sobre a imagem, sem faixas de fundo coloridas, sem caixas. Fonte branca com sombra preta sutil.

TOPO (sobre o fundo desfocado, ACIMA do personagem):
"[TÍTULO FOFO]"
Fonte SANS-SERIF EXTRA-BOLD, caixa alta, tamanho grande.
Branco puro com sombra preta sutil.
Centralizado.
REGRA CRÍTICA: o título fica NO TOPO DA IMAGEM, sobre o fundo. NUNCA sobre o personagem.

CENTRO-INFERIOR:
"— [Promessa 1]
— [Promessa 2]
— [Promessa 3]"
Fonte SANS-SERIF BOLD, branco puro com sombra preta sutil.
Tamanho médio-grande, legível no celular.
Centralizado.
Cada promessa começa com tracinho (—).
REGRA CRÍTICA DE ESPAÇAMENTO: as 3 linhas ficam JUNTAS, com espaçamento MÍNIMO entre elas (line-height apertado, quase colado). Bloco compacto de texto. Se precisar de fundo pra legibilidade, UMA ÚNICA faixa PRETA arredondada englobando as 3 linhas juntas.

BASE:
"Clique aqui para [ação] + [produto/nicho] 👉"
Fonte SANS-SERIF BOLD, MESMO TAMANHO que as 3 promessas acima.
Cor AMARELO VIVO (#FFD700) com sombra preta sutil.
Centralizado.
NÃO é maior que o texto das promessas. Mesmo tamanho, só muda a cor pra amarelo.
Margem mínima de 8% da borda inferior.

REGRA DE LIMPEZA:
PROIBIDO: elementos de anúncio, logos, selos, badges, molduras pesadas, estrelas decorativas. A arte é a ilustração 3D fofa + texto. Só isso.

COMPLIANCE FACEBOOK ADS:
- Sem violência, sem conteúdo sensível

PROIBIDO usar travessão nos textos de copy. O tracinho (—) é usado APENAS como bullet point antes de cada promessa.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Exact size reference: 1080x1350.
````

#### C) Prompt de Animação pro Freepik

Esse serve tanto pro Feed quanto pro Stories. Substitua os placeholders pela descrição do movimento da cena escolhida e por uma sugestão de música doce (preferencialmente versão music box/caixinha de música de uma música conhecida).

````
Anima essa imagem com movimentos sutis e fofos. APENAS a ilustração se mexe. Os textos ficam 100% ESTÁTICOS, não se movem em nenhum momento.

MOVIMENTO DA CENA:
[DESCRIÇÃO DO MOVIMENTO: sutil, fofo, reforça a personalidade do personagem. O personagem faz gestos pequenos e acolhedores. Reflexos de luz se movem nas superfícies texturizadas. Loop de 3-5 segundos.]

REGRA CRÍTICA: os textos na imagem (título, promessas e CTA) são ESTÁTICOS. Não balançam, não aparecem com animação, não se movem. Ficam fixos o tempo todo. Só a ilustração por trás é que tem movimento.

MÚSICA DE FUNDO SUGERIDA: [MÚSICA DOCE E ACOLHEDORA — preferencialmente versão music box/caixinha de música de uma música conhecida. Tom delicado que amplifique a fofura.]
````

Se o aluno disser sim, entregue o template fixo abaixo:

````
Agora cria a exata mesma ilustração 3D, mesmos personagens, mesmas texturas, mesma iluminação, mesmos textos, só diagramada pro formato Stories.

O personagem pode ocupar mais espaço vertical. Os textos mantêm a mesma posição relativa (título no topo, promessas no centro-inferior, CTA na base).

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

### Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) no título e na legenda. Corrigir direto. Nunca mostrar versão bruta.

A cena, as 3 promessas, o CTA da arte e o prompt de animação NÃO passam pela revisora (são conteúdo da arte e direção visual com tom específico), mas devem respeitar Light Copy: sem travessão no texto de copy (o tracinho, é usado APENAS como bullet point antes de cada promessa), sem exclamação, e o título nunca usa o produto no lead.

### Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Fofinho:

📌 IDEIA ESCOLHIDA (nº {numero_ideia} das 10)
CENA: [cena]
TÍTULO: [título]
3 PROMESSAS:
— [Promessa 1]
— [Promessa 2]
— [Promessa 3]
CTA: Clique aqui para [ação] + [produto/nicho] 👉

📝 LEGENDA PRO INSTAGRAM
[legenda longa gerada]

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

🎬 PROMPT DE ANIMAÇÃO PRO FREEPIK
[prompt de animação preenchido, dentro de bloco de código]

---
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher outra ideia (das 10)
```

Se escolher 2, perguntar o que ajustar (título, legenda, cena, promessas, CTA, descrição visual, animação ou música sugerida) e refazer apenas a parte indicada.

Se escolher 3, apresentar a lista das 10 ideias novamente e perguntar o novo número.

### Gerar e salvar

Após a aprovação, pergunte como o aluno quer gerar a imagem:

```
Como você quer gerar a imagem?

1. Colar no ChatGPT ou Gemini (grátis)
   Eu te entrego os prompts prontos. Você cola, gera as artes e salva.

2. Gerar agora pelo OpenRouter (tem custo)
   Eu mando o prompt direto pro modelo de imagem e já salvo o PNG na sua
   pasta. Custa centavos por imagem.

Digite o número:
```

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-fofinho-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-fofinho-{numero}.md`

Conteúdo do arquivo:

```markdown
# Fofinho nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**CENA:** [cena]
**TÍTULO:** [título]
**3 PROMESSAS:**
— [Promessa 1]
— [Promessa 2]
— [Promessa 3]
**CTA:** Clique aqui para [ação] + [produto/nicho] 👉

## Legenda pro Instagram

[legenda longa]

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt de Animação pro Freepik (serve pro Feed e pro Stories)

\`\`\`
[prompt de animação preenchido]
\`\`\`

## Prompt pro ChatGPT. Formato Stories (1080x1920, 9:16)

\`\`\`
[prompt Stories]
\`\`\`

## Como usar

1. Abra o ChatGPT (com geração de imagem habilitada).
2. Cole o **Prompt Feed** e espere a arte ser gerada.
3. Quando estiver pronto, mande "ok" no chat.
4. (Se gerou o Stories) Cole o **Prompt Stories** pra gerar a versão vertical da mesma arte.
5. Depois, abra o Freepik (ferramenta de animação) e cole o **Prompt de Animação** sobre a imagem gerada. O mesmo prompt serve pros dois formatos (Feed e Stories).

## Banco completo (as 10 ideias geradas nesta sessão)

[Listar todas as 10 ideias geradas nesta sessão, com número, CENA, TÍTULO, 3 PROMESSAS e CTA, para o aluno usar depois sem precisar rodar a sub-skill de novo.]
```

### 6b. Modo API (só se o aluno escolheu a opção 2)

Depois de salvar o `.md`, gere apenas a imagem do Feed pela API. A versão Stories sai depois, como opção no menu do Passo 7, reaproveitando a imagem do Feed como referência visual.

1. Leia `OPENROUTER_API_KEY` no `.env`. Se faltar, ofereça configurar com o `/configurar-imagens` ou voltar pro modo ChatGPT.

2. Pergunte o modelo:

```
Qual modelo de imagem?

1. GPT Image 2 (recomendado)
   Cerca de US$ 0,05 por imagem.
2. Gemini Nano Banana 2
   Cerca de US$ 0,07 por imagem.

Digite o número:
```

Opção 1 vira `openai/gpt-5.4-image-2`, opção 2 vira `google/gemini-3.1-flash-image-preview`. Guarde o modelo escolhido, ele vai ser reaproveitado se o aluno pedir Stories no Passo 7.

3. Grave o Prompt Feed num arquivo `.txt` na pasta de criativos. Conteúdo é o Prompt Feed apresentado ao aluno, sem alterações.

4. Anuncie e rode o script no formato Feed (4:5):

```
🔍 Próximo passo: gerar a imagem do Feed via API. Tempo estimado: 2 a 3 minutos.
```

Use o comando Python correto da sessão (`python3` ou `py -3`), conforme a seção Execução de Scripts Python do CLAUDE.md.

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-fofinho-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-fofinho-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Fofinho salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-fofinho-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Fofinho com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Fofinho gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-fofinho-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-fofinho-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Fofinho com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-fofinho-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-fofinho-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-fofinho-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-fofinho-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-fofinho-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

### Sobre as ideias

- O elemento fofo é SEMPRE um objeto/ferramenta/símbolo ESPECÍFICO DO NICHO transformado em personagem 3D.
- NUNCA bichinhos genéricos (gatinho, ursinho) desconectados do nicho.
- Reconhecível como sendo daquele nicho em 1 segundo.
- Título fofo e acolhedor com nicho claro.
- 3 promessas de "vida bonitinha" com nicho presente, cada uma com tracinho (—).
- A CTA SEMPRE contém "Clique aqui" + o nome do nicho/produto + 👉.

### Sobre o estilo visual

- Renderização 3D hiper-detalhada estilo PIXAR MODERNO (Toy Story 4, Monstros SA, Elemental).
- NÃO é cartoon 2D, NÃO é foto realista, NÃO é UGC.
- Texturas reais em cada superfície (plástico, vidro, metal, borracha, papel, tecido).
- Iluminação cinematográfica com reflexos e sombras realistas.
- Proporções exageradas de fofura com acabamento realista.
- Profundidade de campo rasa, bokeh suave.
- Parece frame de filme Pixar, não ilustração flat.
- Nível de fofura: Pixar moderno com textura de tocar.

### Sobre a imagem

- Personagem principal no centro.
- Cenário do nicho levemente desfocado ao fundo.
- Terço superior LIVRE pro título.
- Zero elementos decorativos genéricos.
- NUNCA estética de banco de imagem (foto stock, modelo profissional, composição publicitária).
- NUNCA marketing óbvio na imagem (logo grande, claim de vendas, watermark de propaganda).

### Sobre os textos na imagem

- Estilo TIKTOK/STORIES NATIVO. Texto solto sobre a imagem com sombra preta.
- TÍTULO no topo (acima do personagem): frase fofa, branco com sombra, fonte grande.
- 3 PROMESSAS no centro-inferior: bloco compacto, linhas juntas, cada uma com tracinho (—), branco com sombra.
- CTA na base: AMARELO VIVO (#FFD700), MESMO TAMANHO que as promessas (não maior), "Clique aqui para" + produto/nicho + 👉.

### Sobre a legenda do Instagram (Padrão de Legenda)

Toda legenda pro Instagram entregue por esta skill deve ter **no mínimo 3 linhas**, redigida seguindo os princípios do Manual da Copy (`.claude/skills/revisora/references/manual-copy.md`):

- **Tom de escritor, não de vendedor**: alguém explicando uma coisa real, não fazendo propaganda.
- **Ensina ou avisa, nunca vende**: nas primeiras linhas, a legenda traz um pedaço de conteúdo real (uma observação, um aprendizado, um aviso).
- **Especificidade mata generalização**: usar dados concretos, situações específicas, detalhes que parecem reais.
- **Produto não aparece no início**: nada de "esse curso", "esse treinamento", nome do método ou sigla nas primeiras linhas.
- **Sem travessão (—), sem ponto de exclamação, sem "Não é X. É Y."**, sem frases genéricas de vendedor ("transforme sua vida", "descubra o segredo", "método revolucionário").
- **Sem "mesmo que" e "sem precisar" como muleta**, sem lero-lero, sem promessa vaga.
- **Sem emojis dentro do texto** (exceto o emoji final do CTA, do tipo "👉", que já está previsto na skill).
- A legenda termina com a chamada pro link, no padrão já previsto na skill original.

Estrutura: Lead forte, O antes (4 a 6 linhas), A virada, O resultado, CTA.

Tom da legenda: primeira pessoa, creator brasileiro, casual, acolhedor.

### Sobre a animação

- Só a ilustração se mexe, textos ficam 100% estáticos.
- Movimento sutil, fofo, reforça a personalidade do personagem.
- Reflexos de luz se movem nas texturas.
- Loop de 3 a 5 segundos.
- Sugestão de música doce (versão music box/caixinha de música).
- Mesmo prompt serve pro Feed e pro Stories.

### Padrão de Personagem (Adição Obrigatória)

Toda descrição de pessoa em qualquer prompt gerado por esta skill (Feed, Stories, animação ou listagem de ideias) deve garantir que a pessoa retratada seja:

- **Pessoa comum de classe média brasileira**, cuidada e bem-apresentada, mesmo em momento cotidiano.
- **Aparência arrumada**: cabelo penteado, pele cuidada e saudável, roupa limpa e adequada à cena.
- **Vestuário casual de classe média**: peças simples mas em bom estado (camiseta básica, blusa, calça, vestido comum), nunca rasgado, sujo, manchado ou muito amassado.
- **NÃO modelo profissional** e **NÃO esculhambado**: o equilíbrio é pessoa real de classe média com vida normal e aparência cuidada.

PROIBIDO gerar pessoa muito feia, descabelada, mal-vestida, com aparência de desleixo extremo, esculhambada, com roupa rasgada ou suja, ou em estado de descuido visível. Esta skill gera ilustração 3D estilo Pixar do elemento do nicho como personagem, então a regra também se aplica ao "humano" que possa aparecer no cenário de fundo (se houver): mantém padrão de classe média brasileira cuidada.

Esta diretriz deve ser incorporada ao descrever a pessoa dentro do prompt para o ChatGPT, garantindo que a imagem gerada nunca traga personagem humano feio, descabelado ou muito mal vestido.

### Compliance Facebook Ads

- Sem violência, sem conteúdo sensível.

### Light Copy e regras gerais

- Light Copy obrigatória no título e na legenda. Sem travessão no texto de copy, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- **PROIBIDO travessão (—) nos textos de copy. O tracinho (—) é usado APENAS como bullet point antes de cada promessa.**
- **Exceção documentada: emoji 👉 no CTA da legenda e no CTA da arte.** O Manual da Copy proíbe emojis em geral, mas o CTA do Fofinho termina com 👉 porque integra o padrão visual de creator amador, que é o que confere autenticidade ao formato. Essa exceção vale SOMENTE para o CTA da legenda e o CTA da arte. O título do anúncio nunca usa emoji.
- Produto NÃO aparece no lead do título nem da legenda.
- A cena, as 3 promessas, o CTA e o prompt de animação seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- Substituir TODOS os placeholders dos prompts pro ChatGPT e pro Freepik. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT e pro Freepik em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês quando aplicável.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
