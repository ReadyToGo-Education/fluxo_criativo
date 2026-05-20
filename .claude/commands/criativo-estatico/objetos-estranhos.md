# Objetos Estranhos. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 23 (Objetos Estranhos). Cria criativos UGC ultra-realistas estilo frame de TikTok/Reels onde uma pessoa segura um objeto curioso MUITO perto da câmera como metáfora visual do nicho. Gera 10 ideias de Objetos Estranhos, o aluno escolhe uma, e a sub-skill entrega legenda longa, prompt de Feed pro ChatGPT e prompt de animação pro Freepik. Depois pergunta se quer também o prompt no formato Reels (9:16).

**Por que esse formato funciona:**
A imagem parece um frame REAL de vídeo gravado com iPhone, não anúncio. O objeto curioso na mão funciona como metáfora visual do problema do nicho e gera curiosidade imediata ("por que essa pessoa tá segurando isso?"). Os textos em faixas pretas com destaques amarelos imitam o padrão nativo de creator brasileiro de TikTok/Reels. O criativo aparece como conteúdo orgânico de descoberta pessoal, não como peça publicitária.

## O que você está criando

Anúncios que parecem:
- frame pausado de Reels/TikTok real
- creator brasileiro mostrando algo curioso na câmera
- vídeo orgânico que viralizou
- conteúdo espontâneo de descoberta pessoal

## O que você NUNCA cria

- Propaganda profissional ou estética publicitária
- Modelo perfeito ou foto de banco de imagem
- Visual corporativo ou thumbnail estilo YouTube guru
- Objeto pequeno ou distante (o objeto DOMINA a imagem)
- Copy agressiva ou marketing clássico
- Promessas exageradas ("método revolucionário", "transforme sua vida", "garanta sua vaga")

## Regra de ouro

A cena precisa de 3 coisas:

1. **OBJETO DOMINANTE**. Segurado na mão, MUITO perto da câmera, ocupando boa parte da tela. É a metáfora visual do problema/solução do nicho.
2. **PESSOA VISÍVEL**. Rosto com leve desfoque natural de iPhone (NÃO borrado). O rosto precisa ser VISÍVEL e RECONHECÍVEL, com expressão claramente legível. Desfoque sutil, não blur pesado.
3. **TEXTO ESTILO TIKTOK**. Faixas pretas arredondadas com texto branco e destaques em amarelo dourado. CTA em faixa branca com destaque rosa/pink.

## Regra do objeto

O objeto precisa:

- Ocupar muito espaço visual (lado direito ou central da imagem)
- Ser segurado na mão, em foco nítido
- Gerar curiosidade imediata ("por que essa pessoa tá segurando isso?")
- Funcionar como metáfora visual do problema do nicho
- Ser algo do dia a dia, reconhecível, não exótico

## O Que Fazer

Siga os 4 passos abaixo em ordem.

### PASSO 1. Briefing

Se `meus-produtos/.ativo` existir e apontar pra um produto com `perfil.md` preenchido, pergunte ANTES de qualquer coisa:

```
Usar dados do produto ativo ({slug}) ou informar manualmente?

1. Usar dados do produto ativo
2. Informar manualmente
```

Se escolher 1, extraia do `perfil.md` (e dos demais arquivos do produto): produto, nicho, formato, preço, público. Avise em uma linha qual público assumiu se ele não estiver explícito.

Se escolher 2 (ou se não houver produto ativo), pergunte:

- Qual o nicho?
- Qual o produto?
- Qual o formato (curso, mentoria, ebook, app)?
- Qual o preço?

Pare e espere a resposta.

### PASSO 2. 10 ideias de Objetos Estranhos

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de Objetos Estranhos do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Com base no briefing (nicho + produto + formato + preço), gere 10 ideias. Cada ideia deve conter:

- **OBJETO:** objeto curioso e visualmente forte
- **AMBIENTE:** ambiente coerente com o nicho + elementos visuais do nicho ao fundo
- **ENQUADRAMENTO:** objeto muito perto da câmera em plano detalhe
- **EXPRESSÃO:** emoção humana real
- **TEXTO:**
  - "[hook curto e curioso COM NICHO CLARO]"
  - "[mini explicação simples]"
  - "[dor/consequência]"
  - CTA: "[CTA leve estilo creator]"

#### Regras das 10 ideias

- O objeto é sempre algo do DIA A DIA que funciona como metáfora
- O ambiente SEMPRE tem elementos visuais do nicho ao fundo
- O hook SEMPRE deixa o nicho claro imediatamente
- Variar os objetos (nunca 2 iguais)
- O texto todo precisa parecer conversa de TikTok, não copy
- Variar expressões (descoberta, choque, surpresa, "agora faz sentido")
- Sem travessão. Use vírgula, ponto final ou parênteses.

#### Biblioteca de objetos por nicho (referência)

- Skincare: uva passa, esponja seca, elástico frouxo, planta murcha, ameixa seca
- Corrida: tênis destruído, mola aberta, elástico arrebentado, esponja espremida
- Marketing digital: funil de cozinha, peneira furada, torneira pingando
- Pet/dermatite: esponja de aço, lixa, folha seca, plástico bolha furado
- Diástase: zíper aberto, balão murcho, faixa elástica frouxa, almofada afundada

#### Biblioteca de elementos do ambiente por nicho (referência)

O ambiente ao fundo SEMPRE precisa ter elementos visuais reconhecíveis do nicho. Sem isso, ninguém entende do que se trata. O objeto é a metáfora, o ambiente é o contexto.

- Pet/cachorro: o cachorro visível ao fundo (deitado, sentado, se coçando), vasilha de ração, brinquedo de cachorro, caminha
- Skincare: banheiro com produtos de pele na bancada (frascos, sérums, espelho), ou penteadeira com cremes
- Corrida: tênis de corrida no chão, medalha na parede, roupa de corrida pendurada, parque ao fundo
- Marketing digital: notebook aberto com tela brilhando, celular com notificações, mesa de trabalho
- Diástase: tapete de exercício, roupa de treino, colchonete, elástico de exercício
- Música/violão: violão encostado na parede, partitura, palheta na mesa

O elemento do nicho no fundo pode estar com leve desfoque mas precisa ser RECONHECÍVEL. A pessoa bate o olho e entende o universo em 1 segundo.

#### REGRA CRÍTICA DO HOOK

O primeiro texto (hook no topo) SEMPRE precisa deixar o NICHO claro imediatamente. A pessoa lê o hook e já sabe sobre o que é.

ERRADO: "a pele saudável protege igual plástico bolha" (qual pele? de quem?)
CERTO: "a pele do seu cachorro protege igual plástico bolha intacto" (nicho claro de cara)

ERRADO: "minha barriga tava funcionando assim" (pode ser qualquer coisa)
CERTO: "minha barriga depois da gravidez tava funcionando assim" (nicho claro)

#### REGRA CRÍTICA DO TEXTO (TOM)

Os textos precisam parecer creator brasileiro, TikTok/Reels, descoberta pessoal, conversa espontânea.

PREFERIR:
- "eu achava que…"
- "ninguém me explicou isso…"
- "foi aí que entendi…"
- "o erro tava aqui…"
- "isso mudou minha rotina…"
- "queria ter descoberto antes…"

NUNCA:
- "método revolucionário"
- "transforme sua vida"
- "garanta sua vaga"
- "descubra o segredo"
- "resultado imediato"

#### Estrutura do texto na imagem

1. **Hook** (topo). Curiosidade que para o scroll, NICHO CLARO.
2. **Explicação** (meio). O que o objeto representa no nicho.
3. **Consequência** (meio-baixo). A dor/problema prático.
4. **CTA** (base). Convite leve estilo creator.

#### Apresentação

Mostre as 10 ideias numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de Objetos Estranhos pro seu nicho.

---

**IDEIA 1, [NOME DO OBJETO]**

OBJETO: [descrição]
AMBIENTE: [descrição com elementos do nicho]
ENQUADRAMENTO: [descrição]
EXPRESSÃO: [descrição]

TEXTO:
"[hook com nicho claro]"
"[explicação]"
"[consequência]"
CTA: "[CTA leve]"

---

**IDEIA 2, [NOME DO OBJETO]**
...

---

Escolha uma ideia.
```

### PASSO 3. Desenvolvimento e aprovação

Após o aluno escolher um número de 1 a 10 (pode dizer "cria a 3", "faz a 7", etc.), anuncie. Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

```
🔍 Próximo passo: gerar legenda longa, prompt de Feed pro ChatGPT e prompt de animação pro Freepik. Tempo estimado: cerca de 30 segundos.
```

Desenvolva a ideia escolhida no formato:

```
IDEIA [N], [NOME DO OBJETO]

OBJETO: [descrição]
AMBIENTE: [descrição com elementos do nicho]
ENQUADRAMENTO: [descrição]
EXPRESSÃO: [descrição]

TEXTO:
"[hook com nicho claro]"
"[explicação]"
"[consequência]"
CTA: "[CTA leve]"
```

#### Legenda longa pro Instagram

Estrutura:
- **Lead visceral**. Frase de abertura que conecta o objeto ao problema.
- **A descoberta**. 4 a 6 linhas curtas contando como descobriu o problema.
- **O erro**. O que fazia errado antes.
- **A virada**. Quando entendeu a causa real.
- **CTA**. Chamada pro link com emoji 👉.

Tom: primeira pessoa, creator brasileiro, casual, descoberta pessoal. Light Copy aplicada.

Depois de entregar, escreva:

**"Aprovou? Se sim, eu gero o prompt da imagem (Feed 4:5) e o de animação."**

### PASSO 4. Prompts prontos (Imagem + Animação + Legenda)

Quando o aluno aprovar, anuncie e entregue tudo junto:

```
🔍 Próximo passo: montar os prompts finais. Tempo estimado: cerca de 30 segundos.
```

Gere três coisas:

#### A) Legenda do Instagram

Texto final pronto pra colar.

#### B) Prompt de Feed (4:5) pro ChatGPT, VERBATIM

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

````
Crie uma foto UGC ultra-realista para anúncio de Instagram.

FORMATO:
Feed 4:5 (1080x1350)

A imagem deve parecer um frame pausado de um vídeo REAL gravado com iPhone por um creator brasileiro.

NÃO pode parecer:
- IA
- banco de imagens
- publicidade profissional
- render
- foto corporativa

CENA:
[Descrever pessoa brasileira real: gênero, idade, roupa casual, posição das mãos (uma segura o objeto, outra pode estar no rosto)]

O rosto aparece com leve desfoque natural de profundidade de campo de iPhone (NÃO borrado). O rosto precisa ser VISÍVEL e RECONHECÍVEL, com expressão claramente legível. Desfoque sutil, não blur pesado.

OBJETO PRINCIPAL:
[Descrever o objeto em detalhe: textura, estado, como está sendo segurado]

O objeto deve estar MUITO perto da câmera ocupando boa parte da tela ([LADO DIREITO ou CENTRAL]).
A mão segurando o objeto precisa estar em foco nítido.

AMBIENTE:
[Descrever ambiente brasileiro real. OBRIGATÓRIO ter pelo menos 1-2 elementos visuais reconhecíveis do nicho ao fundo. O elemento do nicho pode estar com leve desfoque mas precisa ser reconhecível em 1 segundo.]

ESTILO VISUAL:
- UGC brasileiro
- luz natural
- estética TikTok/Reels
- imperfeição natural
- pele real
- sem aparência publicitária
- vídeo orgânico
- creator brasileiro
- levemente amador

ENQUADRAMENTO:
- plano detalhe
- profundidade natural (objeto nítido, rosto com leve desfoque mas visível e reconhecível)
- objeto dominante no primeiro plano
- composição espontânea

TEXTO NA IMAGEM (fonte ÚNICA em toda a arte):

REGRA CRÍTICA DE FONTE: TODOS os textos usam a MESMA fonte, MESMO tamanho, MESMO peso (sans-serif bold). Não existe texto maior ou menor. A única diferença visual entre os blocos é a cor da faixa (preta ou branca) e a cor dos destaques (amarelo ou rosa). O tamanho da fonte é IDÊNTICO em todos os blocos.

TOPO-ESQUERDO:
"[HOOK COM NICHO CLARO]"
Fonte sans-serif bold, branca, sobre FAIXAS PRETAS ARREDONDADAS individuais por linha.
Palavra-chave em AMARELO DOURADO.

MEIO-ESQUERDO:
"[EXPLICAÇÃO]"
Fonte sans-serif bold, branca, sobre FAIXAS PRETAS ARREDONDADAS.
Palavra-chave em AMARELO DOURADO.

MEIO-BAIXO ESQUERDO:
"[CONSEQUÊNCIA]"
Fonte sans-serif bold, branca, sobre FAIXAS PRETAS ARREDONDADAS.
Palavra-chave em AMARELO DOURADO.

BASE-ESQUERDO:
"[CTA] →"
Fonte sans-serif bold, preta, sobre FAIXA BRANCA ARREDONDADA.
Palavra-chave em ROSA/PINK.
Seta → no final.

REGRA DE DIAGRAMAÇÃO:
- TODOS os textos alinhados à ESQUERDA
- MESMA fonte, MESMO tamanho, MESMO peso em TODOS os blocos
- Cada linha de texto tem sua PRÓPRIA faixa arredondada (não uma caixa grande)
- Faixas com largura proporcional ao texto de cada linha
- Distribuição vertical com respiro entre os blocos
- Textos NUNCA sobre o objeto
- CTA na base com margem da borda inferior
- Estilo TikTok/Reels nativo brasileiro

IMPORTANTE:
O texto da imagem deve ser EXATAMENTE o texto informado. Não resumir. Não alterar palavras. Não inventar novas frases.

Margem mínima de 8% em todos os lados.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Exact size reference: 1080x1350.
````

#### C) Prompt de animação pro Freepik

Substitua o placeholder do movimento da cena e da música pelos dados reais da ideia escolhida. **O texto final ao usuário não pode ter colchetes.** Esse mesmo prompt de animação serve tanto pro formato Feed quanto pro Reels.

````
Anima essa imagem com movimentos sutis e orgânicos. APENAS a foto se mexe. Os textos ficam 100% ESTÁTICOS, não se movem em nenhum momento.

MOVIMENTO DA CENA:
[DESCRIÇÃO DO MOVIMENTO: a mão interage com o objeto (aperta, gira, estica, puxa). A pessoa ao fundo reage sutilmente (cabeça se move, boca se abre, expressão muda). Elementos do nicho ao fundo podem ter micro movimentos (cachorro se coça, tela do notebook pisca). Leve tremida natural de câmera como iPhone na mão. Loop de 3-5 segundos.]

REGRA CRÍTICA: os textos na imagem (faixas pretas e faixa branca do CTA) são 100% ESTÁTICOS. Não balançam, não aparecem com animação, não se movem, não entram em sequência. Ficam fixos o tempo todo exatamente onde estão. Só a foto por trás é que tem movimento.

MÚSICA DE FUNDO SUGERIDA: [MÚSICA MEME/TIKTOK RECONHECÍVEL que combine com o tom de descoberta da cena.]
````

### Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) na legenda. Corrigir direto. Nunca mostrar versão bruta.

O texto da imagem (hook, explicação, consequência e CTA da arte) e o prompt de animação NÃO passam pela revisora (são conteúdo da arte com tom específico de creator brasileiro), mas devem respeitar Light Copy: sem travessão, sem exclamação, sem promessa exagerada e com nicho claro no hook.

### Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Objetos Estranhos:

📌 IDEIA ESCOLHIDA (nº {numero_ideia} das 10)
OBJETO: [descrição]
AMBIENTE: [descrição com elementos do nicho]
ENQUADRAMENTO: [descrição]
EXPRESSÃO: [descrição]

TEXTO NA IMAGEM:
"[hook com nicho claro]"
"[explicação]"
"[consequência]"
CTA: "[CTA leve]"

📝 LEGENDA LONGA PRO INSTAGRAM
[legenda gerada com lead, descoberta, erro, virada e CTA]

🎨 PROMPT PRO CHATGPT, FORMATO FEED (4:5)
[prompt Feed preenchido, dentro de bloco de código]

🎬 PROMPT DE ANIMAÇÃO PRO FREEPIK
[prompt de animação preenchido, dentro de bloco de código]

---
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher outra ideia (das 10)
```

Se escolher 2, perguntar o que ajustar (legenda, texto da imagem, descrição visual, objeto, ambiente ou prompt de animação) e refazer apenas a parte indicada.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-objetos-estranhos-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-objetos-estranhos-{numero}.md`

Conteúdo do arquivo:

```markdown
# Objetos Estranhos nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Formato:** [curso, mentoria, ebook, app]
**Preço:** [preço]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**OBJETO:** [descrição]
**AMBIENTE:** [descrição com elementos do nicho]
**ENQUADRAMENTO:** [descrição]
**EXPRESSÃO:** [descrição]

**TEXTO NA IMAGEM:**
- Hook: "[hook com nicho claro]"
- Explicação: "[explicação]"
- Consequência: "[consequência]"
- CTA: "[CTA leve]"

## Legenda longa pro Instagram

[legenda com lead, descoberta, erro, virada e CTA]

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt de animação pro Freepik

\`\`\`
[prompt de animação preenchido]
\`\`\`

## Como usar

1. Abra o ChatGPT (com geração de imagem habilitada).
2. Cole o **Prompt Feed** e espere a arte ser gerada.
3. Para animar, suba a imagem gerada no Freepik e cole o **Prompt de animação**. Esse mesmo prompt serve tanto pro Feed quanto pro Reels.

## Banco completo (as 10 ideias geradas nesta sessão)

[Listar todas as 10 ideias de Objetos Estranhos geradas nesta sessão, com número, objeto, ambiente, enquadramento, expressão e os 4 blocos de texto (hook, explicação, consequência, CTA), para o aluno usar depois sem precisar rodar a sub-skill de novo.]
```

Após salvar o `.md`, pergunte se o aluno quer também a versão Reels (9:16):

```
Quer que eu gere o prompt no formato Reels (9:16) também?

1. Sim, gerar versão Reels
2. Não, fica só com o Feed
```

Se escolher 1, entregue o prompt fixo abaixo (não precisa preencher placeholders). No modo ChatGPT, basta colar logo depois que a arte de Feed foi gerada. No modo API, a versão Stories será gerada na etapa 6b com a linha de FORMAT OVERRIDE.

````
Agora cria a exata mesma foto, mesma pessoa, mesma roupa, mesma expressão, mesmo objeto, mesmos textos, só diagramada pro formato Reels/Stories.

O objeto continua dominante e muito perto da câmera. Os textos mantêm a mesma posição relativa (topo, meio, meio-baixo, base). Deixar espaço seguro no topo e na base pro UI do Instagram.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-objetos-estranhos-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-objetos-estranhos-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Objetos Estranhos salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-objetos-estranhos-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Objetos Estranhos com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Objetos Estranhos gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-objetos-estranhos-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-objetos-estranhos-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Objetos Estranhos com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-objetos-estranhos-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-objetos-estranhos-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-objetos-estranhos-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-objetos-estranhos-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-objetos-estranhos-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

- Light Copy obrigatória na legenda. Sem travessão, sem exclamação, sem promessa vaga, sem "não é X. É Y.".
- **Exceção documentada: emoji no CTA da legenda.** O Manual da Copy proíbe emojis em geral, mas a legenda do Objetos Estranhos termina com emoji 👉 no CTA porque integra o padrão visual de creator amador, que é o que confere autenticidade ao formato. Essa exceção vale SOMENTE para o CTA da legenda.
- Produto NÃO aparece no lead da legenda.
- O texto da imagem (hook, explicação, consequência, CTA) e o prompt de animação seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar a legenda.
- **Regra do ambiente (CRÍTICA)**: o ambiente ao fundo SEMPRE precisa ter elementos visuais reconhecíveis do nicho. Sem isso, ninguém entende do que se trata. O objeto é a metáfora, o ambiente é o contexto. O elemento do nicho no fundo pode estar com leve desfoque mas precisa ser RECONHECÍVEL em 1 segundo.
- **Regra do hook (CRÍTICA)**: o primeiro texto (hook no topo) SEMPRE precisa deixar o NICHO claro imediatamente. A pessoa lê o hook e já sabe sobre o que é. Nunca hook genérico que pode ser de qualquer nicho.
- **Regra dos textos da imagem**: 4 blocos (hook no topo, explicação no meio, consequência no meio-baixo, CTA na base). TODOS alinhados à ESQUERDA, nunca sobre o objeto. MESMA fonte, MESMO tamanho, MESMO peso em TODOS os blocos. Faixas PRETAS arredondadas com texto branco e destaques AMARELO DOURADO. CTA em faixa BRANCA arredondada com texto preto e destaque ROSA/PINK. Cada LINHA tem sua própria faixa (não uma caixa grande). Estilo TikTok/Reels nativo brasileiro.
- **Regra do tom**: creator brasileiro, TikTok, descoberta pessoal. PREFERIR "eu achava que…", "ninguém me explicou isso…", "foi aí que entendi…", "o erro tava aqui…", "isso mudou minha rotina…", "queria ter descoberto antes…". NUNCA "método revolucionário", "transforme sua vida", "garanta sua vaga", "descubra o segredo", "resultado imediato".
- **Regra da legenda do Instagram**: longa, conta a história de descoberta. Lead visceral, erro anterior, virada, resultado, CTA. Tom de creator brasileiro casual e pessoal. Primeira pessoa. CTA com emoji 👉.
- **Regra da animação**: só a foto se mexe, textos ficam 100% ESTÁTICOS. Mão interage com o objeto. Pessoa ao fundo reage sutilmente. Elementos do nicho ao fundo podem ter micro movimentos. Leve tremida de câmera (iPhone na mão). Loop de 3 a 5 segundos. Sugestão de música meme/TikTok. Mesmo prompt serve pro Feed e pro Reels.
- Substituir TODOS os placeholders dos prompts pro ChatGPT e pro Freepik. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- O texto da imagem deve ser EXATAMENTE o texto informado na ideia escolhida. Não resumir. Não alterar palavras. Não inventar novas frases.
- Margem mínima de 8% em todos os lados da arte.
- **Compliance Facebook Ads**: sem violência, sem conteúdo sensível, sem menção a doenças de forma apelativa. Estilo UGC orgânico, não publicitário. PROIBIDO travessão. Use vírgula ou ponto final.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
