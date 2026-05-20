# Nunca. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 18 (Nunca). Cria criativos UGC estáticos no formato "Nunca": foto meme de uma pessoa cometendo um erro específico do nicho que nunca deveria fazer, com explicação curta do porquê e CTA com promessa. Estilo TikTok/Reels viral. Esse formato é par com "Sempre" (opção 19): Nunca alerta sobre o erro a não cometer, Sempre revela o hack a sempre fazer.

**Por que esse formato funciona:**
A foto parece um frame de TikTok pausado no momento do erro, não peça publicitária. O alerta direto "NUNCA [faça isso]" faz a pessoa parar o scroll e pensar "eu faço isso". A combinação de utilidade (dica real) com identificação (erro que ela comete) gera compartilhamento orgânico. A CTA promete a solução, fechando o ciclo de curiosidade aberto pelo alerta.

## O que você está criando

Anúncios UGC que parecem:
- frame de TikTok pausado no momento do erro
- dica viral que alguém mandaria no grupo de WhatsApp
- alerta que faz a pessoa parar o scroll e pensar "eu faço isso"
- conteúdo compartilhável pela utilidade + identificação

## O que você NUNCA cria

- Erros genéricos sem conexão com o nicho
- Expressões discretas (precisa ser performática, meme)
- Cenas com muitos elementos (1 pessoa + no máximo 1 objeto)
- Estética de estúdio ou banco de imagem
- Marketing óbvio na imagem
- Texto com cara de anúncio

## Regra de ouro

A cena precisa de 3 coisas:
1. **ERRO ESPECÍFICO** — algo concreto que o público faz errado e não sabe. Quanto mais específico e surpreendente, melhor
2. **EXPRESSÃO PERFORMÁTICA** — a pessoa tá cometendo o erro de forma exagerada, meme. Quase cômica
3. **SIMPLICIDADE** — 1 pessoa + no máximo 1 objeto. Fundo com contexto do nicho, desfocado

## Fluxo da conversa

Siga os 4 passos abaixo em ordem.

### PASSO 1 — Briefing

Verifique se existe `meus-produtos/.ativo` apontando pra um produto com `perfil.md`.

**Se existir produto ativo com perfil**, pergunte apenas:

```
Usar os dados do produto ativo ({slug}) ou informar manualmente?

1. Usar do produto ativo
2. Informar manualmente
```

Se escolher 1, extraia produto, nicho e público do `perfil.md` e `idconsumidor.md` e siga pro Passo 2.

Se escolher 2, faça o briefing direto:

```
Qual o produto/serviço?
Qual o público?
```

Pare e espere a resposta.

**Se NÃO existir produto ativo**, faça o briefing direto:

```
Qual o produto/serviço?
Qual o público?
```

Pare e espere a resposta.

### PASSO 2 — 10 ideias de "Nunca"

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de "Nunca" do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Com base no briefing, gere 10 ideias. Cada ideia deve conter:

- **CENA:** descrição curta (1 pessoa cometendo o erro de forma exagerada + no máximo 1 objeto)
- **TÍTULO:** sempre "NUNCA [faça isso]." — curto, direto, máximo 7-8 palavras
- **EXPLICAÇÃO:** 1 parágrafo curto (3 linhas) explicando por que nunca fazer isso. Dado concreto ou consequência real
- **CTA:** "Clique aqui para [promessa] + [produto/nicho]" 👉

Regras das 10 ideias:
- Todos os erros precisam ser ESPECÍFICOS do nicho
- Variar entre erros de iniciante, erros que todo mundo comete, e erros surpreendentes que pouca gente sabe
- Cada cena é SIMPLES: 1 pessoa + 1 objeto máximo
- O título SEMPRE contém o nicho de forma clara
- A CTA SEMPRE contém uma promessa + o nome do nicho/produto
- Variar entre homem e mulher
- Sem travessão. Use vírgula, ponto final ou parênteses.

Mostre as 10 ideias numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de "Nunca" pro seu nicho.

---

**1.**
**CENA:** [descrição curta da cena: 1 pessoa cometendo o erro de forma exagerada + objeto se houver]
**TÍTULO:** "NUNCA [faça isso]."
**EXPLICAÇÃO:** [3 linhas curtas, dado concreto ou consequência real]
**CTA:** "Clique aqui para [promessa] + [produto/nicho]" 👉

---

**2.**
...

---

Escolha uma ideia.
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

### PASSO 3 — Desenvolvimento e aprovação

Quando o aluno escolher a ideia, anuncie:

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

Desenvolva o criativo:

```
TÍTULO: "NUNCA [faça isso]."

CENA UGC: [1 pessoa cometendo o erro de forma exagerada/meme + objeto se houver. Descrição simples]

EXPLICAÇÃO (na imagem):
"[Linha 1]
[Linha 2]
[Linha 3]"

CTA: Clique aqui para [promessa] + [produto/nicho] 👉
```

**LEGENDA DO INSTAGRAM (longa, com lead e CTA):**

A legenda conta a história de alguém que cometeu esse erro e o que aconteceu. Estrutura:
- **Lead forte** — confissão de ter cometido o erro
- **A consequência** — 4-6 linhas curtas mostrando o que aconteceu. Tom de conversa, frases curtas
- **A descoberta** — o momento onde a pessoa entendeu o porquê do erro
- **A solução** — como o produto/método resolveu
- **CTA** — chamada direta pro link com emoji 👉

Tom da legenda: primeira pessoa, creator brasileiro, casual, útil. Começa no erro, termina na solução. Light Copy aplicada.

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) na legenda. Corrigir direto. Nunca mostrar versão bruta. O título "NUNCA [faça isso].", a explicação na imagem e o texto do CTA na arte NÃO passam pela revisora (são conteúdo da arte com tom específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, e a explicação sempre baseada em dado concreto ou consequência real.

Depois de entregar, escreva:

**"Aprovou? Se sim, eu gero o prompt da imagem e o de animação."**

### PASSO 4 — Prompts prontos (Imagem + Animação + Legenda)

Quando o aluno aprovar, entregue tudo junto:

**A) Legenda do Instagram** — texto final pronto pra colar.

**B) Prompt de Feed (4:5)** — texto pronto pra colar no ChatGPT. Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

````
Cria pra mim uma foto UGC ultra-realista pra anúncio de Instagram. Estilo TikTok/Reels, parece que alguém tirou a foto com iPhone no momento.

A FOTO:
[DESCRIÇÃO SIMPLES: pessoa brasileira, idade, roupa, EXPRESSÃO EXAGERADA cometendo o erro. O que está fazendo, objeto se houver. 1 pessoa + 1 objeto máximo. Performático, meme.]

REGRA CRÍTICA DE ENQUADRAMENTO: a pessoa deve estar enquadrada do PEITO PRA BAIXO ou levemente acima, deixando o TERÇO SUPERIOR DA IMAGEM LIVRE (só fundo desfocado) pra o título ficar SEM cobrir o rosto. O rosto aparece no terço central da imagem. O título fica no topo, sobre o fundo, NUNCA sobre o rosto.

Fundo simples: [contexto do nicho, desfocado]. Luz natural. Foto de iPhone, levemente amadora. Estética UGC brasileira.

TEXTO NA IMAGEM — ESTILO TIKTOK/STORIES NATIVO:

Todos os textos direto sobre a foto, sem faixas de fundo coloridas, sem caixas. Fonte branca com sombra preta sutil. Parece caption nativa de TikTok.

TOPO (sobre o fundo desfocado, ACIMA do rosto da pessoa):
"NUNCA [ERRO ESPECÍFICO]."
Fonte SANS-SERIF EXTRA-BOLD, caixa alta, tamanho grande.
Branco puro com sombra preta sutil.
Centralizado.
REGRA CRÍTICA: o título fica NO TOPO DA IMAGEM, sobre o fundo. NUNCA sobre o rosto da pessoa.

CENTRO-INFERIOR:
"[Linha 1]
[Linha 2]
[Linha 3]"
Fonte SANS-SERIF BOLD, branco puro com sombra preta sutil.
Tamanho médio-grande, legível no celular.
Centralizado.
REGRA CRÍTICA DE ESPAÇAMENTO: as 3 linhas ficam JUNTAS, com espaçamento MÍNIMO entre elas (line-height apertado, quase colado). Bloco compacto de texto. Se precisar de fundo pra legibilidade, UMA ÚNICA faixa PRETA arredondada englobando as 3 linhas juntas.

BASE:
"Clique aqui para [promessa] + [produto/nicho] 👉"
Fonte SANS-SERIF BOLD, MESMO TAMANHO que o texto de explicação acima.
Cor AMARELO VIVO (#FFD700) com sombra preta sutil.
Centralizado.
NÃO é maior que o texto de explicação. Mesmo tamanho, só muda a cor pra amarelo.
Margem mínima de 8% da borda inferior.

REGRA CRÍTICA: parecer FRAME DE TIKTOK pausado. Orgânico, não anúncio.

REGRA DE LIMPEZA:
PROIBIDO: estrelas, sparkles, brilhos, emojis decorativos, molduras, faixas brancas, faixas coloridas. Só foto + texto com sombra.

REGRAS DA FOTO:
- Ultra-realista, iPhone
- Expressão PERFORMÁTICA, meme, exagerada
- Cena simples, 1 pessoa + 1 objeto máximo
- Contexto do nicho visível no cenário/roupa
- Terço superior da imagem LIVRE pro título (sem rosto nessa zona)
- Fundo desfocado
- Não pode parecer banco de imagem

COMPLIANCE FACEBOOK ADS:
- Roupas cobertas
- Sem violência

PROIBIDO usar travessão. Use vírgula ou ponto final.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Exact size reference: 1080x1350.
````

**C) Prompt de Animação pro Freepik** — texto pronto pra colar. Serve tanto pro Feed quanto pro Stories.

````
Anima essa imagem com movimentos sutis e engraçados. APENAS a foto se mexe. Os textos ficam 100% ESTÁTICOS, não se movem em nenhum momento.

MOVIMENTO DA CENA:
[DESCRIÇÃO DO MOVIMENTO: sutil, performático, reforça o erro sendo cometido de forma exagerada. A pessoa continua fazendo a coisa errada de forma repetitiva e cômica. Loop de 3-5 segundos.]

REGRA CRÍTICA: os textos na imagem (título, explicação e CTA) são ESTÁTICOS. Não balançam, não aparecem com animação, não se movem. Ficam fixos o tempo todo. Só a foto por trás é que tem movimento.

MÚSICA DE FUNDO SUGERIDA: [MÚSICA MEME RECONHECÍVEL que amplifique o momento do erro. O contraste entre a dramaticidade da música e o erro bobo cria o humor.]
````

Se o aluno responder que sim, entregue o prompt fixo abaixo:

````
Agora cria a exata mesma foto, mesma pessoa, mesma roupa, mesma expressão, mesmo objeto, mesmos textos, só diagramada pro formato Stories.

Os textos mantêm a mesma posição relativa (título no topo acima do rosto, explicação no centro-inferior, CTA na base). A foto pode mostrar mais do cenário verticalmente.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

Este mesmo texto de animação do item C serve tanto pro formato Feed quanto pro Stories.

---

## Padrão de Personagem (obrigatório em qualquer prompt gerado)

Toda descrição de pessoa em qualquer prompt gerado por esta sub-skill (Feed, Stories, animação ou listagem de ideias) deve garantir que a pessoa retratada seja:

- **Pessoa comum de classe média brasileira**, cuidada e bem-apresentada, mesmo em momento cotidiano
- **Aparência arrumada**: cabelo penteado, pele cuidada e saudável, roupa limpa e adequada à cena
- **Vestuário casual de classe média**: peças simples mas em bom estado (camiseta básica, blusa, calça, vestido comum), nunca rasgado, sujo, manchado ou muito amassado
- **NÃO modelo profissional** e **NÃO esculhambado**: o equilíbrio é pessoa real de classe média com vida normal e aparência cuidada

PROIBIDO gerar pessoa muito feia, descabelada, mal-vestida, com aparência de desleixo extremo, esculhambada, com roupa rasgada ou suja, ou em estado de descuido visível. Mesmo na cena do erro sendo cometido de forma performática, o exagero vem da expressão e da ação errada, NUNCA do desleixo da aparência. A pessoa permanece dentro do padrão de classe média brasileira cuidada.

---

## Padrão de Legenda (obrigatório)

Toda legenda pro Instagram entregue por esta sub-skill deve ter **no mínimo 3 linhas**, redigida seguindo os princípios do Manual da Copy (`.claude/skills/revisora/references/manual-copy.md`):

- **Tom de escritor, não de vendedor**: alguém explicando uma coisa real, não fazendo propaganda
- **Ensina ou avisa, nunca vende**: nas primeiras linhas, a legenda traz um pedaço de conteúdo real (uma observação, um aprendizado, um aviso)
- **Especificidade mata generalização**: usar dados concretos, situações específicas, detalhes que parecem reais
- **Produto não aparece no início**: nada de "esse curso", "esse treinamento", nome do método ou sigla nas primeiras linhas
- **Sem travessão (—), sem ponto de exclamação, sem "Não é X. É Y."**, sem frases genéricas de vendedor ("transforme sua vida", "descubra o segredo", "método revolucionário")
- **Sem "mesmo que" e "sem precisar" como muleta**, sem lero-lero, sem promessa vaga
- **Sem emojis dentro do texto** (exceto o emoji final do CTA, do tipo "👉", que já está previsto na skill)
- A legenda termina com a chamada pro link, no padrão já previsto na skill original

---

## Apresentação final e aprovação

Depois de entregar título, legenda e prompts (Feed e Stories), apresente:

```
Pronto. Aqui está o seu criativo Nunca:

📌 IDEIA ESCOLHIDA (nº {numero_ideia} das 10)
CENA: [descrição da cena]
TÍTULO: "NUNCA [faça isso]."
EXPLICAÇÃO: [3 linhas]
CTA: "Clique aqui para [promessa] + [produto/nicho]" 👉

📝 LEGENDA PRO INSTAGRAM
[legenda gerada]

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

Se escolher 2, perguntar o que ajustar (legenda, cena, explicação, CTA, descrição visual ou prompt de animação) e refazer apenas a parte indicada.

Se escolher 3, apresentar a lista das 10 ideias novamente e perguntar o novo número.

## Gerar e salvar

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-nunca-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-nunca-{numero}.md`

Conteúdo do arquivo:

```markdown
# Nunca nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**CENA:** [descrição da cena]
**TÍTULO:** "NUNCA [faça isso]."
**EXPLICAÇÃO:** [3 linhas]
**CTA:** "Clique aqui para [promessa] + [produto/nicho]" 👉

## Legenda pro Instagram

[legenda]

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
3. Se quiser a versão vertical, mande "ok" no chat e cole o **Prompt Stories**.
4. Pra animar, abra o Freepik (ferramenta de imagem-pra-vídeo), suba a imagem gerada e cole o **Prompt de Animação**. O mesmo prompt serve pro Feed e pro Stories.

## Banco completo (as 10 ideias geradas nesta sessão)

[Listar todas as 10 ideias Nunca geradas nesta sessão, com número, cena, título, explicação e CTA, para o aluno usar depois sem precisar rodar a sub-skill de novo.]
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-nunca-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-nunca-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Nunca salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-nunca-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Nunca com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Nunca gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-nunca-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-nunca-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Nunca com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-nunca-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-nunca-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-nunca-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-nunca-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-nunca-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras críticas consolidadas

### Sobre as ideias
- Título SEMPRE é "NUNCA [faça isso]." — curto, direto, máximo 7-8 palavras
- Erros ESPECÍFICOS do nicho, nunca genéricos
- Variar entre erros de iniciante, erros comuns e erros surpreendentes
- 1 pessoa + expressão exagerada + no máximo 1 objeto
- Variar entre homem e mulher

### Sobre a expressão
- PERFORMÁTICA, MEME, EXAGERADA
- A pessoa tá cometendo o erro de forma quase cômica
- Exagero é o que faz funcionar como meme
- É o centro visual de tudo, o texto só complementa

### Sobre a imagem
- UGC ultra-realista, foto de iPhone
- 1 pessoa brasileira cometendo o erro de forma exagerada
- Contexto do nicho visível (roupa, cenário, objeto)
- Fundo simples e desfocado
- Terço superior LIVRE pro título (rosto no terço central, NUNCA na zona do título)
- Não pode parecer banco de imagem ou estúdio
- Zero elementos decorativos

### Sobre os textos na imagem
- Estilo TIKTOK/STORIES NATIVO, texto solto sobre a foto com sombra preta
- TÍTULO no topo (acima do rosto): "NUNCA [erro].", branco com sombra, fonte grande
- EXPLICAÇÃO no centro-inferior: 3 linhas JUNTAS (espaçamento mínimo, bloco compacto), branco com sombra
- CTA na base: AMARELO VIVO (#FFD700), MESMO TAMANHO que a explicação (não maior), "Clique aqui para" + promessa + produto/nicho + 👉
- Título + explicação + CTA. Só isso na imagem

### Sobre a legenda do Instagram
- Mínimo de 3 linhas
- Longa, conta a história de alguém que cometeu o erro
- Lead confessional, consequência, descoberta, solução, CTA
- Tom de creator brasileiro: casual, útil
- Primeira pessoa, começa no erro, termina na solução
- CTA com emoji 👉 e chamada pro link

### Sobre a animação
- Só a foto se mexe, textos ficam 100% estáticos
- Movimento sutil, performático, reforça o erro sendo cometido
- Loop de 3-5 segundos
- Sugestão de música meme que amplifique o momento do erro
- Mesmo prompt serve pro Feed e pro Stories

### Compliance Facebook Ads
- Roupas cobertas
- Sem violência
- PROIBIDO travessão (— ou –). Use vírgula ou ponto final

## Regras de copy e operação

- Light Copy obrigatória na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- **Exceção documentada: emoji no CTA da legenda.** O Manual da Copy proíbe emojis em geral, mas a legenda do Nunca termina com emoji (do tipo "👉") no CTA porque integra o padrão visual de creator amador, que é o que confere autenticidade ao formato. Essa exceção vale SOMENTE para o CTA da legenda.
- Produto NÃO aparece no lead da legenda.
- O título "NUNCA [faça isso].", a explicação na imagem e o texto do CTA na arte seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar a legenda.
- Substituir TODOS os placeholders dos prompts pro ChatGPT e pro Freepik. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
