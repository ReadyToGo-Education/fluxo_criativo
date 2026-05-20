# Você Merece. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 22 (Você Merece). Mostra uma pessoa vivendo o sucesso ou resultado que o produto promete, com título "Você merece [conquista específica do nicho]", 3 desejos reais do público e CTA. Gera 10 ideias de "Você Merece", o aluno escolhe uma, e a sub-skill entrega título, legenda longa, prompt de Feed pro ChatGPT, prompt de animação pro Freepik e, ao final, pergunta se quer Stories também.

**Por que esse formato funciona:**
A foto parece um frame de TikTok ou Reels pausado, não anúncio. A pessoa já tá vivendo o resultado, ativando projeção positiva imediata. Os 3 desejos com tracinho são coisas concretas que o público quer, gerando identificação direta. O título nominal e o CTA amarelo no padrão nativo de TikTok criam um meme emocional de conquista que é compartilhável pela identificação com o desejo.

O entregável final inclui:
1. Prompt da imagem pro ChatGPT (Feed)
2. Legenda longa do Instagram com lead e CTA
3. Prompt de animação pro Freepik com sugestão de música
4. (mesmo texto de animação serve pros dois)

## O que você está criando

Anúncios UGC que parecem:
- frame de TikTok pausado no momento do resultado
- post aspiracional que faz a pessoa pensar "eu quero isso pra mim"
- conteúdo compartilhável pela identificação com o desejo
- meme emocional de conquista

## O que você NUNCA cria

- Expressões discretas (precisa ser genuinamente feliz, performática)
- Conquistas genéricas sem conexão com o nicho
- Cenas com muitos elementos (1 pessoa + no máximo 1 objeto do resultado)
- Estética de estúdio ou banco de imagem
- Marketing óbvio na imagem
- Texto com cara de anúncio
- Desejos genéricos que servem pra qualquer nicho. Os 3 desejos precisam ter o nicho claro

## Regra de ouro

A cena precisa de 3 coisas:
1. **RESULTADO VISÍVEL**. A pessoa tá vivendo o sucesso que o produto promete. Não é antes, é o depois
2. **3 DESEJOS REAIS**. Coisas concretas que o público quer e que o produto pode proporcionar. Específicos do nicho
3. **SIMPLICIDADE**. 1 pessoa + no máximo 1 objeto que simboliza o resultado. Fundo com contexto

## O Que Fazer

Siga os 4 passos abaixo em ordem.

### PASSO 1 — Briefing

Se existir `meus-produtos/{ativo}/perfil.md`, pergunte uma única coisa:

```
Usar os dados do produto ativo ou informar manualmente?

1. Usar os dados do produto ativo
2. Informar manualmente
```

Se escolher 1, extraia produto, nicho e público do `perfil.md` e do `idconsumidor.md` e siga pro PASSO 2.

Se escolher 2 ou se não existir `perfil.md`, pergunte apenas:

- Qual o produto/serviço?
- Qual o público?

Pare e espere a resposta.

### PASSO 2 — 10 ideias de "Você Merece"

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de Você Merece pro seu nicho. Tempo estimado: cerca de 60 segundos.
```

Com base no briefing, gere 10 ideias. Cada ideia deve conter:

- **CENA:** descrição curta (1 pessoa vivendo o resultado + expressão genuína de felicidade + no máximo 1 objeto)
- **TÍTULO:** sempre "Você merece [conquista específica do nicho]." (o nicho SEMPRE claro no título)
- **3 DESEJOS:** 3 coisas concretas que esse público quer, cada um com tracinho (—). O nicho precisa estar presente nos desejos
- **CTA:** "Clique aqui para [ação] + [produto/nicho]" 👉

Regras das 10 ideias:
- Todos os títulos precisam ter o NICHO explícito e claro
- Todos os 3 desejos precisam ter conexão clara com o nicho (não genéricos)
- A imagem mostra o RESULTADO (o depois, não o antes)
- Cada cena é SIMPLES: 1 pessoa + expressão genuína + no máximo 1 objeto
- A CTA SEMPRE contém "Clique aqui" + o nome do nicho/produto
- Variar entre homem e mulher
- Variar os contextos de resultado (pessoal, social, físico, emocional)

Mostre as 10 ideias numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de Você Merece pro seu nicho.

---

**1.**
**CENA:** [1 pessoa vivendo o resultado + expressão genuína de felicidade + objeto se houver]
**TÍTULO:** "Você merece [conquista específica do nicho]."
**3 DESEJOS:**
— [Desejo 1 com nicho claro]
— [Desejo 2 com nicho claro]
— [Desejo 3 com nicho claro]
**CTA:** Clique aqui para [ação] + [produto/nicho] 👉

---

**2.**
...

---

Escolha uma ideia.
```

### PASSO 3 — Desenvolvimento e aprovação

Quando o usuário escolher a ideia, desenvolva:

```
TÍTULO: "Você merece [conquista específica do nicho]."

CENA UGC: [1 pessoa vivendo o resultado + expressão genuína de felicidade + objeto se houver. Descrição simples]

3 DESEJOS:
"— [Desejo 1 com nicho claro]"
"— [Desejo 2 com nicho claro]"
"— [Desejo 3 com nicho claro]"

CTA: Clique aqui para [ação] + [produto/nicho] 👉
```

**LEGENDA DO INSTAGRAM (longa, com lead e CTA):**

A legenda conta a jornada de alguém que conquistou o que o público deseja. Estrutura:
- **Lead forte**. Frase de abertura que puxa identificação
- **O antes**. 4-6 linhas curtas mostrando como era antes. Tom de conversa, frases curtas
- **A virada**. O momento onde o produto/método entrou
- **O resultado**. A conquista que a pessoa vive agora
- **CTA**. Chamada direta pro link com emoji 👉

Tom da legenda: primeira pessoa, creator brasileiro, casual, emocional. Começa no desejo, termina no resultado.

Mínimo de 3 linhas. Aplica Padrão de Legenda (seção mais abaixo nas Regras): tom de escritor, ensina ou avisa, especificidade mata generalização, produto não aparece no início, sem travessão, sem exclamação, sem "não é X. É Y.", sem "mesmo que" e "sem precisar" como muleta, sem lero-lero, sem promessa vaga, sem emojis dentro do texto (exceto o 👉 do CTA), termina com chamada pro link.

Auto-revisão obrigatória: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) no título e na legenda. Corrigir direto. Nunca mostrar versão bruta.

A cena, os 3 desejos, o CTA da arte e o prompt de animação NÃO passam pela revisora (são conteúdo da arte e direção visual com tom específico), mas devem respeitar Light Copy: sem travessão fora do bullet point dos desejos, sem exclamação, sem promessa vaga.

Depois de entregar, escreva:

**"Aprovou? Se sim, eu gero o prompt da imagem e o de animação."**

### PASSO 4 — Prompts prontos (Imagem + Animação + Legenda)

Anuncie:

```
🔍 Próximo passo: gerar prompt de Feed pro ChatGPT e prompt de animação pro Freepik. Tempo estimado: cerca de 30 segundos.
```

Quando o usuário aprovar, entregue tudo junto:

**A) Legenda do Instagram** — texto final pronto pra colar.

**B) Prompt de Feed (4:5) pro ChatGPT** — texto pronto pra colar. Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

````
Cria pra mim uma foto UGC ultra-realista pra anúncio de Instagram. Estilo TikTok/Reels, parece que alguém tirou a foto com iPhone no momento.

A FOTO:
[DESCRIÇÃO SIMPLES: pessoa brasileira, idade, roupa, EXPRESSÃO GENUÍNA DE FELICIDADE vivendo o resultado do produto. O que está fazendo, objeto se houver. 1 pessoa + 1 objeto máximo. A pessoa JÁ ALCANÇOU o resultado.]

REGRA CRÍTICA DE ENQUADRAMENTO: a pessoa deve estar enquadrada deixando o TERÇO SUPERIOR DA IMAGEM LIVRE (só fundo desfocado) pra o título ficar SEM cobrir o rosto. O rosto aparece no terço central da imagem. O título fica no topo, sobre o fundo, NUNCA sobre o rosto.

Fundo simples: [contexto do resultado, desfocado]. Luz natural. Foto de iPhone, levemente amadora. Estética UGC brasileira.

TEXTO NA IMAGEM — ESTILO TIKTOK/STORIES NATIVO:

Todos os textos direto sobre a foto, sem faixas de fundo coloridas, sem caixas. Fonte branca com sombra preta sutil. Parece caption nativa de TikTok.

TOPO (sobre o fundo desfocado, ACIMA do rosto da pessoa):
"VOCÊ MERECE [CONQUISTA ESPECÍFICA DO NICHO]."
Fonte SANS-SERIF EXTRA-BOLD, caixa alta, tamanho grande.
Branco puro com sombra preta sutil.
Centralizado.
REGRA CRÍTICA: o título fica NO TOPO DA IMAGEM, sobre o fundo. NUNCA sobre o rosto da pessoa.

CENTRO-INFERIOR:
"— [Desejo 1]
— [Desejo 2]
— [Desejo 3]"
Fonte SANS-SERIF BOLD, branco puro com sombra preta sutil.
Tamanho médio-grande, legível no celular.
Centralizado.
Cada desejo começa com tracinho (—).
REGRA CRÍTICA DE ESPAÇAMENTO: as 3 linhas ficam JUNTAS, com espaçamento MÍNIMO entre elas (line-height apertado, quase colado). Bloco compacto de texto. Se precisar de fundo pra legibilidade, UMA ÚNICA faixa PRETA arredondada englobando as 3 linhas juntas.

BASE:
"Clique aqui para [ação] + [produto/nicho] 👉"
Fonte SANS-SERIF BOLD, MESMO TAMANHO que os 3 desejos acima.
Cor AMARELO VIVO (#FFD700) com sombra preta sutil.
Centralizado.
NÃO é maior que o texto dos desejos. Mesmo tamanho, só muda a cor pra amarelo.
Margem mínima de 8% da borda inferior.

REGRA CRÍTICA: parecer FRAME DE TIKTOK pausado. Orgânico, não anúncio.

REGRA DE LIMPEZA:
PROIBIDO: estrelas, sparkles, brilhos, emojis decorativos, molduras, faixas brancas, faixas coloridas. Só foto + texto com sombra.

REGRAS DA FOTO:
- Ultra-realista, iPhone
- Expressão GENUÍNA de felicidade, satisfação, orgulho
- Cena simples, 1 pessoa + 1 objeto máximo
- Contexto do nicho visível
- Terço superior da imagem LIVRE pro título (sem rosto nessa zona)
- Fundo desfocado
- Não pode parecer banco de imagem

COMPLIANCE FACEBOOK ADS:
- Roupas cobertas
- Sem violência

PROIBIDO usar travessão nos textos de copy. O tracinho (—) é usado APENAS como bullet point antes de cada desejo.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Exact size reference: 1080x1350.
````

**C) Prompt de Animação pro Freepik** — texto pronto pra colar. Serve tanto pro Feed quanto pro Stories. Substitua os placeholders pelos dados reais.

````
Anima essa imagem com movimentos sutis e emocionais. APENAS a foto se mexe. Os textos ficam 100% ESTÁTICOS, não se movem em nenhum momento.

MOVIMENTO DA CENA:
[DESCRIÇÃO DO MOVIMENTO: sutil, genuíno, reforça a felicidade do resultado alcançado. A pessoa faz um gesto de satisfação ou orgulho. Loop de 3-5 segundos.]

REGRA CRÍTICA: os textos na imagem (título, 3 desejos e CTA) são ESTÁTICOS. Não balançam, não aparecem com animação, não se movem. Ficam fixos o tempo todo. Só a foto por trás é que tem movimento.

MÚSICA DE FUNDO SUGERIDA: [MÚSICA EMOCIONAL/INSPIRACIONAL RECONHECÍVEL que amplifique o sentimento de conquista e merecimento.]
````

Se o aluno responder que sim, entregue o prompt de Stories abaixo. Esse é fixo, não precisa preencher placeholders.

````
Agora cria a exata mesma foto, mesma pessoa, mesma roupa, mesma expressão, mesmo objeto, mesmos textos, só diagramada pro formato Stories.

Os textos mantêm a mesma posição relativa (título no topo acima do rosto, 3 desejos no centro-inferior, CTA na base). A foto pode mostrar mais do cenário verticalmente.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Você Merece:

📌 IDEIA ESCOLHIDA (nº {numero_ideia} das 10)
CENA: [descrição da cena]
TÍTULO: "Você merece [conquista específica do nicho]."
3 DESEJOS:
— [Desejo 1]
— [Desejo 2]
— [Desejo 3]
CTA: Clique aqui para [ação] + [produto/nicho] 👉

📝 LEGENDA PRO INSTAGRAM
[legenda longa gerada]

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

🎬 PROMPT DE ANIMAÇÃO PRO FREEPIK
[prompt de animação preenchido, dentro de bloco de código]

📱 PROMPT PRO CHATGPT, FORMATO STORIES
[prompt Stories, dentro de bloco de código]

---
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher outra ideia (das 10)
```

Se escolher 2, perguntar o que ajustar (legenda, cena, desejos, CTA, descrição visual ou prompt de animação) e refazer apenas a parte indicada.

Se escolher 3, apresentar a lista das 10 ideias novamente e perguntar o novo número.

### 6. Gerar e salvar

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-voce-merece-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-voce-merece-{numero}.md`

Conteúdo do arquivo:

```markdown
# Você Merece nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**CENA:** [descrição da cena]
**TÍTULO:** "Você merece [conquista específica do nicho]."
**3 DESEJOS:**
— [Desejo 1]
— [Desejo 2]
— [Desejo 3]
**CTA:** Clique aqui para [ação] + [produto/nicho] 👉

## Legenda pro Instagram

[legenda longa]

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt de Animação pro Freepik

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
3. Pegue a imagem gerada e cole no Freepik junto com o **Prompt de Animação** pra animar (mesmo prompt serve pro Feed e pro Stories).
4. Se gerou também o **Prompt Stories**, mande "ok" no chat depois do Feed e cole o Stories pra gerar a versão vertical da mesma arte.

## Banco completo (as 10 ideias geradas nesta sessão)

[Listar todas as 10 ideias geradas nesta sessão, com número, CENA, TÍTULO, 3 DESEJOS e CTA, para o aluno usar depois sem precisar rodar a sub-skill de novo.]
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-voce-merece-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-voce-merece-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Você Merece salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-voce-merece-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Você Merece com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Você Merece gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-voce-merece-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-voce-merece-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Você Merece com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-voce-merece-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-voce-merece-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-voce-merece-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-voce-merece-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-voce-merece-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

### Light Copy e auto-revisão

- Light Copy obrigatória no título e na legenda. Sem travessão (—), sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- **Exceção documentada: tracinho (—) como bullet point nos 3 desejos.** O Light Copy proíbe travessão em geral, mas o tracinho (—) é usado APENAS como bullet point antes de cada desejo na arte e no banco da ideia. Não vale como travessão de texto corrido.
- **Exceção documentada: emoji no CTA da legenda.** O Manual da Copy proíbe emojis em geral, mas a legenda termina com emoji 👉 no CTA porque integra o padrão visual de creator amador, que confere autenticidade ao formato. Essa exceção vale SOMENTE para o CTA da legenda. O título do anúncio nunca usa emoji.
- Produto NÃO aparece no lead do título nem da legenda.
- Cena, 3 desejos, CTA da arte e prompt de animação seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.

### Sobre as ideias

- Título SEMPRE é "Você merece [conquista específica do nicho]." (nicho SEMPRE claro)
- 3 desejos reais do público, cada um com tracinho (—), todos com nicho presente
- A imagem mostra o RESULTADO (o depois), não o processo
- 1 pessoa + expressão genuína + no máximo 1 objeto do resultado
- A CTA SEMPRE contém "Clique aqui" + o nome do nicho/produto
- Variar entre homem e mulher
- Variar os contextos de resultado (pessoal, social, físico, emocional)

### Sobre a expressão

- GENUÍNA de felicidade, satisfação, orgulho
- Performática mas não cômica. Aqui é emoção real, não meme de humor
- A pessoa tá vivendo o melhor momento do resultado
- É o centro visual de tudo. O texto só complementa

### Sobre a imagem

- UGC ultra-realista, foto de iPhone
- 1 pessoa brasileira vivendo o resultado
- Contexto do nicho visível
- Fundo simples e desfocado
- Terço superior LIVRE pro título (rosto no terço central, NUNCA na zona do título)
- Não pode parecer banco de imagem ou estúdio
- Zero elementos decorativos

### Sobre os textos na imagem

- Estilo TIKTOK/STORIES NATIVO. Texto solto sobre a foto com sombra preta
- TÍTULO no topo (acima do rosto): "VOCÊ MERECE [conquista do nicho].", branco com sombra, fonte grande
- 3 DESEJOS no centro-inferior: bloco compacto, linhas juntas (espaçamento mínimo), cada um com tracinho (—), branco com sombra
- CTA na base: AMARELO VIVO (#FFD700), MESMO TAMANHO que os desejos (não maior), "Clique aqui para" + produto/nicho + 👉
- Título + 3 desejos + CTA. Só isso na imagem

### Padrão de Personagem (Obrigatório)

Toda descrição de pessoa em qualquer prompt gerado por esta sub-skill (Feed, Stories, animação ou listagem de ideias) deve garantir que a pessoa retratada seja:

- **Pessoa comum de classe média brasileira**, cuidada e bem-apresentada, mesmo em momento cotidiano
- **Aparência arrumada**: cabelo penteado, pele cuidada e saudável, roupa limpa e adequada à cena
- **Vestuário casual de classe média**: peças simples mas em bom estado (camiseta básica, blusa, calça, vestido comum), nunca rasgado, sujo, manchado ou muito amassado
- **NÃO modelo profissional** e **NÃO esculhambado**: o equilíbrio é pessoa real de classe média com vida normal e aparência cuidada

PROIBIDO gerar pessoa muito feia, descabelada, mal-vestida, com aparência de desleixo extremo, esculhambada, com roupa rasgada ou suja, ou em estado de descuido visível. Como esta skill mostra a pessoa vivendo o RESULTADO (depois), a aparência cuidada de classe média brasileira reforça a sensação aspiracional de conquista.

### Padrão de Legenda (Obrigatório)

Toda legenda pro Instagram entregue por esta sub-skill deve ter **no mínimo 3 linhas**, redigida seguindo os princípios do Manual da Copy (`.claude/skills/revisora/references/manual-copy.md`):

- **Tom de escritor, não de vendedor**: alguém explicando uma coisa real, não fazendo propaganda
- **Ensina ou avisa, nunca vende**: nas primeiras linhas, a legenda traz um pedaço de conteúdo real (uma observação, um aprendizado, um aviso)
- **Especificidade mata generalização**: usar dados concretos, situações específicas, detalhes que parecem reais
- **Produto não aparece no início**: nada de "esse curso", "esse treinamento", nome do método ou sigla nas primeiras linhas
- **Sem travessão (—), sem ponto de exclamação, sem "Não é X. É Y."**, sem frases genéricas de vendedor ("transforme sua vida", "descubra o segredo", "método revolucionário")
- **Sem "mesmo que" e "sem precisar" como muleta**, sem lero-lero, sem promessa vaga
- **Sem emojis dentro do texto** (exceto o emoji final do CTA, do tipo 👉, que já está previsto na skill)
- A legenda termina com a chamada pro link, no padrão já previsto na skill

### Sobre a animação

- Só a foto se mexe, textos ficam 100% estáticos
- Movimento sutil, genuíno, reforça a felicidade do resultado
- Loop de 3-5 segundos
- Sugestão de música emocional/inspiracional
- Mesmo prompt serve pro Feed e pro Stories

### Compliance Facebook Ads

- Roupas cobertas
- Sem violência
- PROIBIDO travessão (— ou –) nos textos de copy. O tracinho é usado APENAS como bullet point antes de cada desejo

### Operação

- Substituir TODOS os placeholders dos prompts pro ChatGPT e do prompt de animação. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
