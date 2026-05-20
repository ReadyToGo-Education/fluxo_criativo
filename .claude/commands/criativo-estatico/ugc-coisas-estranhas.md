# UGC Coisas Estranhas. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 21 (UGC Coisas Estranhas). Cria criativos UGC estáticos e animados onde uma pessoa faz algo completamente absurdo e engraçado com um único objeto, que se conecta de forma inteligente ao produto/nicho. Gera 10 ideias, o aluno escolhe uma, e a sub-skill entrega título, legenda longa do Instagram e prompts prontos pra colar (Feed pro ChatGPT e Animação pro Freepik com sugestão de música).

**Por que esse formato funciona:**
A foto parece um frame de TikTok/Reels pausado, não anúncio. O absurdo chama atenção e faz a pessoa parar o scroll. A inteligência da conexão entre a loucura e o produto é o que vende. A legenda longa do Instagram faz o trabalho pesado de explicar e converter, enquanto a imagem é orgânica e compartilhável pelo humor.

## O entregável final inclui

1. Prompt da imagem pro ChatGPT (Feed)
2. Legenda longa do Instagram com lead e CTA
3. Prompt de animação pro Freepik com sugestão de música
4. (mesmo texto de animação serve pros dois)

## O que você está criando

Anúncios UGC que parecem:
- frame de TikTok pausado
- print de Reels que alguém mandou no grupo de WhatsApp
- cena absurda que faz a pessoa parar o scroll
- conteúdo compartilhável pelo humor + inteligência da conexão

## O que você NUNCA cria

- Cenas com muitos elementos ou detalhes (1 pessoa + 1 objeto = a cena inteira)
- Cenários complexos ou elaborados
- Estética de estúdio ou banco de imagem
- Marketing óbvio na imagem
- Texto com cara de anúncio (faixas brancas, faixas coloridas, layout de designer)
- Absurdo sem conexão com o produto

## Regra de ouro

A cena precisa de 3 coisas:
1. **ABSURDO**, a pessoa tá fazendo algo estranho, engraçado, bizarro
2. **SIMPLICIDADE**, 1 pessoa + 1 objeto + 1 ação. Fundo simples. Só isso. Nada mais
3. **PONTE GENIAL**, a conexão entre a loucura e o produto precisa ser inteligente e surpreendente

Exemplos de cenas simples:
- Homem beijando um chinelo (1 pessoa + 1 objeto)
- Mulher abraçando uma vassoura no sofá (1 pessoa + 1 objeto)
- Homem mordendo um tênis (1 pessoa + 1 objeto)
- Homem enfiando o pé numa panela (1 pessoa + 1 objeto)

NUNCA: "mulher cercada de 47 velas no chão" ou "homem correndo na rua com mochila desviando de pessoas". Muitos elementos = imagem ruim.

## Fluxo da conversa

Siga os 4 passos abaixo em ordem.

### PASSO 1 — Briefing

Antes de perguntar, verifique se existe `meus-produtos/.ativo` e o `perfil.md` correspondente.

**Se houver perfil ativo**, pergunta única:

```
Usar dados do produto ativo ({slug}) ou informar manualmente?

1. Usar dados do produto ativo
2. Informar manualmente
```

Se o aluno escolher 1, extraia do `perfil.md` e `idconsumidor.md`:
- Produto (nome)
- Nicho
- Público

Se o aluno escolher 2, pergunte como no caso sem perfil (abaixo).

**Se não houver perfil ativo**, pergunte direto:

- Qual o produto/serviço?
- Qual o público?

Pare e espere a resposta.

### PASSO 2 — 10 ideias de UGC Coisas Estranhas

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de UGC Coisas Estranhas do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Com base no briefing, gere 10 ideias. Cada ideia deve conter:

- **CENA:** descrição curta (1 pessoa + 1 objeto + 1 ação estranha. Só isso)
- **TÍTULO:** frase curta e provocativa que vai na imagem (máximo 6-7 palavras, nicho claro)
- **EXPLICAÇÃO:** 3 linhas compactas que fazem a ponte entre o absurdo e o produto/nicho
- **CTA:** "Clique aqui para [ação] + [produto/nicho]" 👉

#### Regras das 10 ideias

- Pelo menos 2 ideias COMPLETAMENTE ABSURDAS (nível comer planta, Nutella na cara, enfiar o pé numa panela, beijar um objeto aleatório). Loucura total sem relação aparente com o nicho, mas com ponte genial
- As outras 8 podem ser estranhas com conexão mais próxima ao nicho
- Todas precisam da PONTE INTELIGENTE, absurdo sem ponte é só barulho
- Cada cena é SIMPLES: 1 pessoa + 1 objeto + 1 ação. Sem múltiplos objetos
- O título SEMPRE contém o nicho de forma clara
- A CTA SEMPRE contém o nome do nicho/produto explicitamente

#### Apresentação

Mostre as 10 ideias numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de UGC Coisas Estranhas pro seu nicho.

---

**1.**
**CENA:** [1 pessoa + 1 objeto + 1 ação estranha]
**TÍTULO:** [frase curta provocativa, máximo 6-7 palavras, nicho claro]
**EXPLICAÇÃO:**
[Linha 1]
[Linha 2]
[Linha 3]
**CTA:** Clique aqui para [ação] + [produto/nicho] 👉

---

**2.**
...

---

Escolha uma ideia.
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

### PASSO 3 — Desenvolvimento e aprovação

Quando o usuário escolher a ideia, anuncie:

```
🔍 Próximo passo: gerar título, legenda e desenvolvimento da ideia escolhida. Tempo estimado: cerca de 30 segundos.
```

Desenvolva:

```
TÍTULO: [frase curta provocativa]

CENA UGC: [1 pessoa + 1 objeto + 1 ação. Descrição simples: pessoa, roupa, expressão, o que faz com o objeto]

EXPLICAÇÃO (na imagem):
"[Linha 1]
[Linha 2]
[Linha 3]"

CTA: Clique aqui para [ação] + [produto/nicho] 👉
```

**LEGENDA DO INSTAGRAM (longa, com lead e CTA):**

A legenda é onde o trabalho pesado acontece. Estrutura:
- **Lead forte**, frase de abertura que puxa atenção (engraçada, provocativa ou confessional)
- **Desenvolvimento**, 4-6 linhas curtas que constroem a ponte entre o absurdo e o produto. Tom de conversa, frases curtas, quebras de linha frequentes
- **Virada**, o momento onde a loucura faz sentido e o produto entra naturalmente
- **CTA**, chamada direta pro link com emoji 👉

Tom da legenda: primeira pessoa, creator brasileiro, casual, engraçado mas com substância. Mínimo de 3 linhas. Light Copy aplicada.

Antes de mostrar ao aluno, aplique a rotina de auto-revisão obrigatória do CLAUDE.md (Manual da Copy + revisora) no título e na legenda. Corrigir direto, nunca mostrar versão bruta. O texto da imagem (título da arte, explicação, CTA) e o prompt de animação NÃO passam pela revisora (são conteúdo da arte com tom específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, e o título sempre contém o nicho de forma clara.

Depois de entregar, escreva:

**"Aprovou? Se sim, eu gero o prompt da imagem e o de animação."**

### PASSO 4 — Prompts prontos (Imagem + Animação + Legenda)

Quando o aluno aprovar, entregue tudo junto. Substitua todos os placeholders pelos dados reais. O texto final ao usuário não pode ter colchetes.

#### A) Legenda do Instagram

Texto final pronto pra colar (a legenda já gerada e revisada no Passo 3).

#### B) Prompt de Feed (4:5) pro ChatGPT

````
Cria pra mim uma foto UGC ultra-realista pra anúncio de Instagram. Estilo TikTok/Reels, parece que alguém tirou a foto com iPhone no momento.

A FOTO:
[DESCRIÇÃO SIMPLES: pessoa brasileira, idade, roupa básica, expressão facial, O QUE ESTÁ FAZENDO COM O OBJETO. 1 pessoa + 1 objeto + 1 ação. Só isso.]

Fundo simples: [ambiente brasileiro básico — parede de casa, chão de cozinha, sofá]. Luz natural. Foto de iPhone, levemente amadora. Estética UGC brasileira.

TEXTO NA IMAGEM — ESTILO TIKTOK/STORIES NATIVO:

Todos os textos direto sobre a foto, sem faixas de fundo coloridas, sem caixas. Fonte branca com sombra preta sutil. Parece caption nativa de TikTok.

CENTRO-TOPO:
"[TÍTULO CURTO EM CAIXA ALTA]"
Fonte SANS-SERIF EXTRA-BOLD, caixa alta, tamanho grande.
Branco puro com sombra preta sutil.
Centralizado.

CENTRO-INFERIOR:
"[Linha 1]
[Linha 2]
[Linha 3]"
Fonte SANS-SERIF BOLD, branco puro com sombra preta sutil.
Tamanho médio-grande, legível no celular.
Centralizado.
REGRA CRÍTICA DE ESPAÇAMENTO: as 3 linhas ficam JUNTAS, com espaçamento MÍNIMO entre elas (line-height apertado, quase colado). Bloco compacto de texto. Se precisar de fundo pra legibilidade, UMA ÚNICA faixa PRETA arredondada englobando as 3 linhas juntas.

BASE:
"Clique aqui para [ação] + [produto/nicho] 👉"
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
- Só 2 elementos: a pessoa e o objeto
- Cena simples, fundo simples
- Não pode parecer banco de imagem

COMPLIANCE FACEBOOK ADS:
- Roupas cobertas
- Sem violência

PROIBIDO usar travessão. Use vírgula ou ponto final.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Exact size reference: 1080x1350.
````

#### C) Prompt de Animação pro Freepik (com sugestão de música)

Este mesmo prompt serve tanto pro formato Feed quanto pro Stories. Não precisa gerar dois prompts de animação separados.

````
Anima essa imagem com movimentos sutis e engraçados. APENAS a foto se mexe. Os textos ficam 100% ESTÁTICOS, não se movem em nenhum momento.

MOVIMENTO DA CENA:
[DESCRIÇÃO DO MOVIMENTO: sutil, engraçado, reforça o absurdo da cena. A pessoa faz um movimento lento e repetitivo com o objeto. Loop de 3-5 segundos.]

REGRA CRÍTICA: os textos na imagem (título, explicação e CTA) são ESTÁTICOS. Não balançam, não aparecem com animação, não se movem. Ficam fixos o tempo todo. Só a foto por trás é que tem movimento.

MÚSICA DE FUNDO SUGERIDA: [MÚSICA MEME RECONHECÍVEL que crie contraste cômico com a cena. Explicar por que combina.]
````

#### D) Prompt de Stories (9:16) pro ChatGPT

Só entregue se o aluno responder que sim na pergunta acima. Esse prompt é fixo, não precisa preencher placeholders.

````
Agora cria a exata mesma foto, mesma pessoa, mesma roupa, mesma expressão, mesmo objeto, mesmos textos, só diagramada pro formato Stories.

Os textos mantêm a mesma posição relativa (título no centro-topo, explicação no centro-inferior, CTA na base). A foto pode mostrar mais do cenário verticalmente.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo UGC Coisas Estranhas:

📌 IDEIA ESCOLHIDA (nº {numero_ideia} das 10)
CENA: [descrição da cena]

📌 TÍTULO DO ANÚNCIO
[título gerado]

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

Se escolher 2, perguntar o que ajustar (título, legenda, cena, descrição visual, CTA, movimento da animação ou música) e refazer apenas a parte indicada.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-ugc-coisas-estranhas-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-ugc-coisas-estranhas-{numero}.md`

Conteúdo do arquivo:

```markdown
# UGC Coisas Estranhas nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**CENA:** [descrição da cena]

## Título do anúncio

[título]

## Legenda pro Instagram

[legenda]

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt de Animação pro Freepik (serve pro Feed e pro Stories)

\`\`\`
[prompt de animação preenchido com música sugerida]
\`\`\`

## Prompt pro ChatGPT. Formato Stories (1080x1920, 9:16)

\`\`\`
[prompt Stories]
\`\`\`

## Como usar

1. Abra o ChatGPT (com geração de imagem habilitada).
2. Cole o **Prompt Feed** e espere a arte ser gerada.
3. Quando estiver pronto, mande "ok" no chat.
4. (Opcional) Cole o **Prompt Stories** pra gerar a versão vertical da mesma arte.
5. Pegue qualquer uma das imagens (Feed ou Stories) e cole no Freepik junto com o **Prompt de Animação** pra criar o vídeo animado. O mesmo prompt serve pros dois formatos.

## Banco completo (as 10 ideias geradas nesta sessão)

[Listar todas as 10 ideias geradas nesta sessão, com número, cena, título, explicação e CTA, para o aluno usar depois sem precisar rodar a sub-skill de novo.]
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-ugc-coisas-estranhas-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-ugc-coisas-estranhas-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo UGC Coisas Estranhas salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-ugc-coisas-estranhas-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro UGC Coisas Estranhas com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo UGC Coisas Estranhas gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-ugc-coisas-estranhas-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-ugc-coisas-estranhas-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro UGC Coisas Estranhas com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-ugc-coisas-estranhas-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-ugc-coisas-estranhas-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-ugc-coisas-estranhas-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-ugc-coisas-estranhas-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-ugc-coisas-estranhas-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

### Sobre as ideias

- 1 pessoa + 1 objeto + 1 ação = a cena. NADA MAIS.
- Pelo menos 2 das 10 ideias COMPLETAMENTE ABSURDAS com ponte genial.
- A ponte absurdo → produto é OBRIGATÓRIA e precisa ser inteligente.
- O título SEMPRE contém o nicho de forma clara.
- A CTA SEMPRE contém "Clique aqui" + o nome do nicho/produto.

### Sobre a imagem

- UGC ultra-realista, foto de iPhone.
- 1 pessoa brasileira + 1 objeto. Fundo simples.
- Não pode parecer banco de imagem ou estúdio.
- Zero elementos decorativos.

### Sobre os textos na imagem

- Estilo TIKTOK/STORIES NATIVO, texto solto sobre a foto com sombra preta, sem faixas brancas.
- TÍTULO no centro-topo: curto, provocativo, máximo 6-7 palavras, caixa alta, branco com sombra.
- EXPLICAÇÃO no centro-inferior: 3 linhas JUNTAS (espaçamento mínimo, bloco compacto), branco com sombra. Se precisar de fundo, UMA faixa preta arredondada. NUNCA faixas brancas ou coloridas.
- CTA na base: AMARELO VIVO (#FFD700), MESMO TAMANHO que a explicação (não maior), com "Clique aqui para" + produto/nicho + 👉.
- Precisa parecer frame de TikTok pausado, não layout de anúncio.

### Sobre a legenda do Instagram

- Longa, com lead forte, desenvolvimento e CTA.
- Mínimo de 3 linhas.
- Tom de creator brasileiro: casual, engraçado, com substância.
- Primeira pessoa.
- A legenda faz o trabalho pesado de explicar e vender.
- CTA com emoji 👉 e chamada pro link.
- Tom de escritor, não de vendedor: alguém explicando uma coisa real, não fazendo propaganda.
- Ensina ou avisa, nunca vende: nas primeiras linhas, a legenda traz um pedaço de conteúdo real (uma observação, um aprendizado, um aviso).
- Especificidade mata generalização: usar dados concretos, situações específicas, detalhes que parecem reais.
- Produto não aparece no início: nada de "esse curso", "esse treinamento", nome do método ou sigla nas primeiras linhas.
- Sem "mesmo que" e "sem precisar" como muleta, sem lero-lero, sem promessa vaga.
- Sem emojis dentro do texto (exceto o emoji final do CTA, do tipo "👉").

### Sobre a animação

- Só a foto se mexe, textos ficam 100% estáticos.
- Movimento sutil, engraçado, loop de 3-5 segundos.
- Reforça o absurdo da cena.
- Sugestão de música meme que crie contraste cômico.
- Mesmo prompt de animação serve pro Feed e pro Stories.

### Padrão de personagem (obrigatório em todos os prompts)

Toda descrição de pessoa em qualquer prompt gerado por esta skill (Feed, Stories, animação ou listagem de ideias) deve garantir que a pessoa retratada seja:

- **Pessoa comum de classe média brasileira**, cuidada e bem-apresentada, mesmo em momento cotidiano.
- **Aparência arrumada**: cabelo penteado, pele cuidada e saudável, roupa limpa e adequada à cena.
- **Vestuário casual de classe média**: peças simples mas em bom estado (camiseta básica, blusa, calça, vestido comum), nunca rasgado, sujo, manchado ou muito amassado.
- **NÃO modelo profissional** e **NÃO esculhambado**: o equilíbrio é pessoa real de classe média com vida normal e aparência cuidada.

PROIBIDO gerar pessoa muito feia, descabelada, mal-vestida, com aparência de desleixo extremo, esculhambada, com roupa rasgada ou suja, ou em estado de descuido visível. Mesmo na cena absurda/bizarra com o objeto, o humor vem da ação estranha em si, NUNCA do desleixo da aparência. A pessoa permanece dentro do padrão de classe média brasileira cuidada, o que aumenta o impacto do contraste com a ação absurda.

### O que NUNCA criar

- Cenas com muitos elementos ou detalhes (1 pessoa + 1 objeto = a cena inteira).
- Cenários complexos ou elaborados.
- Estética de estúdio ou banco de imagem.
- Marketing óbvio na imagem.
- Texto com cara de anúncio (faixas brancas, faixas coloridas, layout de designer).
- Absurdo sem conexão com o produto.

### Compliance Facebook Ads

- Roupas cobertas.
- Sem violência.
- PROIBIDO travessão (— ou –). Use vírgula ou ponto final.

### Light Copy e regras gerais

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- **Exceção documentada: emoji no CTA da legenda e do texto da arte.** O Manual da Copy proíbe emojis em geral, mas a legenda do UGC Coisas Estranhas termina com emoji (ex: "👉") no CTA porque integra o padrão visual de creator amador, que é o que confere autenticidade ao formato. Mesma exceção vale pro CTA da arte. O título do anúncio nunca usa emoji.
- Produto NÃO aparece no lead do título nem da legenda.
- O texto da imagem (título, explicação, CTA) e o prompt de animação seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- Substituir TODOS os placeholders dos prompts pro ChatGPT e Freepik. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
