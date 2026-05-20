# Jogo dos 7 Erros. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 12 (Jogo dos 7 Erros). Cria uma cena fotorrealista brasileira do dia a dia do público com 7 erros visuais embutidos que o espectador precisa encontrar. Gera 10 ideias de cena, o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
A gamificação prende o scroll: a pessoa para pra "jogar" e procurar os erros. Quando acha, comenta no post ("achei o terceiro"), e isso gera engajamento orgânico que o algoritmo entrega. O CTA promete revelar a resposta e a solução pelo link, e essa lacuna é o que gera o clique. A mistura de 4 erros profissionais reais com 2 easter eggs e 1 absurdo cartoon equilibra dor, identificação e humor.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço.
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho. Inclua a faixa etária, porque ela ajuda a calibrar os erros profissionais, os easter eggs e a cena do dia a dia.
- **Quadro / promessa**: a transformação principal do `perfil.md`, pra alimentar o título e o CTA (o CTA promete revelar a resposta e a solução que levam a esse resultado).

### 1. Apresentar resumo do contexto e confirmar

SEMPRE mostre o resumo, mesmo se algum campo veio de inferência. Marque o que é real e o que foi inferido:

```
Vou usar estes dados do seu produto ativo ({slug}):

Produto: [nome do produto]
Nicho: [nicho]
Público: [resumo do público, com faixa etária]

(Marque "✓ do perfil" pros campos extraídos diretamente do perfil.md ou idconsumidor.md.
Marque "○ inferido" pros campos que foram um chute a partir do slug, tipo ou preço.)

Está tudo certo?

1. Sim, está certo, pode seguir
2. Quero ajustar algum campo
```

**Se escolher 1**, pular pra etapa 2 (Geração das 10 ideias).

**Se escolher 2**, perguntar qual campo ajustar e refazer só a parte indicada.

**Pergunta de ajuste (caso aluno escolha 2)**, com exemplos do nicho do produto ativo:

```
Qual é o seu produto e nicho?
(ex: [3 exemplos do mesmo universo do produto ativo])
```

**IMPORTANTE: os exemplos NUNCA podem ser genéricos.** Antes de fazer a pergunta, construa 3 exemplos do mesmo universo do produto ativo:

- Se o produto for de automação/IA: "Mentoria de Automações com IA pra criadores de conteúdo", "Curso de Agentes GPT pra atendimento", "Treinamento de N8N pra agências"
- Se for de skincare: "Curso de Skincare pra mulheres 40+", "Mentoria de rotina de pele pós-menopausa", "Ebook de anti-aging caseiro"
- Se for de tráfego: "Mentoria de Tráfego Pago pra criadores", "Curso de Anúncios no Meta pra agências", "Consultoria de Performance pra ecommerce"
- Se for de cafeteria: "Consultoria de Cardápio pra donos de cafeteria", "Treinamento de Barista pra equipes", "Curso de Como Abrir uma Cafeteria"
- Último recurso (se realmente não der pra inferir nicho): "Mentoria de tráfego pago pra criadores de conteúdo", "Curso de skincare pra mulheres 40+", "Consultoria de cardápio pra donos de cafeteria"

Se o aluno não especificou público, assumir um plausível brasileiro com base no produto/nicho e avisar antes de gerar as ideias:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Geração das 10 ideias

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de cena do Jogo dos 7 Erros do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere 10 ideias. Cada ideia é uma **cena diferente do dia a dia do nicho** (banheiro, escritório, mercado, consultório, sala de casa, academia, etc), com 7 erros específicos daquele momento.

#### Composição obrigatória dos 7 erros em cada cena

**Proporção fixa:**

- **4 erros profissionais reais** do nicho (ativam dor/identificação do público: produtos errados, métricas ruins, decisões erradas, comportamentos prejudiciais).
- **2 easter eggs/piadas internas** do nicho (referências cult, ironias visuais, brincadeiras que só quem é do segmento entende, recompensam o olhar atento e geram comentário).
- **1 absurdo visual cartoon** (animal gigante, objeto absurdo, elemento claramente cartoon misturado no realismo, pros olhos atentos que estão jogando o jogo).

#### Tipos de cena que funcionam pra venda

1. **No momento do problema** (chuveiro com queda de cabelo, pia entulhada de produtos).
2. **Comprando o produto ou consultando profissional** (farmácia, consultório, banco).
3. **No trabalho ou na rotina** (home office, mesa do escritório, reunião).
4. **Em casa relaxando** (sofá, cama, varanda).
5. **Com a família** (mesa do café, sala com filhos).
6. **Em situação social** (academia, restaurante, evento).
7. **Pesquisando ou aprendendo** (notebook com várias abas, livros, vídeos do YouTube).

#### Apresentação

Mostre as 10 ideias numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de cena do Jogo dos 7 Erros pro seu nicho.

---

**1.** **Cena: [DESCRIÇÃO DA CENA]**
[descrição visual da cena: pessoa, ambiente, ação, atmosfera]
**Os 7 erros:**
1. [Erro profissional 1] (PROFISSIONAL)
2. [Erro profissional 2] (PROFISSIONAL)
3. [Erro profissional 3] (PROFISSIONAL)
4. [Erro profissional 4] (PROFISSIONAL)
5. [Easter egg 1] (EASTER EGG)
6. [Easter egg 2] (EASTER EGG INTERNO)
7. [Absurdo visual] (ABSURDO VISUAL)

---

**2.** **Cena: [DESCRIÇÃO DA CENA]**
...

---

Qual número você quer transformar em criativo?
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

### 3. Escolha e geração do criativo

Após o aluno escolher um número de 1 a 10, anuncie:

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

Gere quatro coisas a partir da ideia escolhida:

#### A) Título do anúncio

Frase de impacto conectada ao público + chamada pra encontrar os erros (ex: "Mulheres com queda de cabelo, encontrem os 7 erros nessa imagem."). Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem pergunta no título
- Sem promessa vaga (incluir dado, prazo ou situação concreta)
- Sem "não é X. É Y."
- Produto não aparece no lead
- Linguagem que a pessoa usaria com uma amiga

#### B) Legenda pro Instagram

2 a 3 linhas em primeira pessoa, tom de creator, convidando pra encontrar os erros e clicar no link pra ver a resposta e a solução. Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

**IMPORTANTE: o prompt do Jogo dos 7 Erros é mais denso que os outros formatos porque precisa renderizar 7 erros distintos simultaneamente. Por isso o aspect ratio precisa estar reforçado no INÍCIO, MEIO e FIM do prompt. Preserve esse reforço triplo exatamente como está abaixo.**

````
IMPORTANTE, FORMATO E ASPECT RATIO (LER PRIMEIRO):
Esta arte é PARA FEED DO INSTAGRAM. Aspect ratio EXATO 4:5 vertical fechada (1080x1350 pixels). NÃO é 9:16 Stories. NÃO é quadrado 1:1. Composição vertical curta de feed, mais larga e menos alta que Stories. Esse formato é OBRIGATÓRIO.

FORMATO DO CRIATIVO: JOGO DOS 7 ERROS

A arte é uma cena fotorrealista brasileira com 7 erros visuais embutidos. Mistura híbrida: realismo fotográfico + 1 elemento cartoon absurdo.

ESTRUTURA EM 3 ZONAS HORIZONTAIS:

1. TOPO: Faixa branca sólida com título em 2 linhas:
"ENCONTRE OS 7 ERROS"
"[FRASE COMPLEMENTAR DO NICHO]"
Fonte sans-serif extra-bold, texto preto, alinhado centro.

2. CENTRO (a cena): [DESCRIÇÃO DA CENA COM PESSOAS BRASILEIRAS REAIS, AMBIENTE BRASILEIRO CLASSE MÉDIA BEM-CUIDADO, ROUPA COBERTA, EXPRESSÃO COERENTE, LUZ NATURAL QUENTE.]

Gatilhos de realismo (em inglês):
- "real Brazilian [pessoa] in his/her [idade]s, naturally cared appearance"
- "no model, no stock photo aesthetic"
- "Brazilian middle-class [ambiente]"
- "non-American context, Brazilian everyday life"
- "amateur lifestyle photography, natural lighting"
- "modest covered clothing"

OS 7 ERROS (todos devem estar visíveis e identificáveis):

1. [Erro profissional 1, descrição visual específica e nítida]
2. [Erro profissional 2, descrição visual específica e nítida]
3. [Erro profissional 3, descrição visual específica e nítida]
4. [Erro profissional 4, descrição visual específica e nítida]
5. [Easter egg 1, descrição visual específica]
6. [Easter egg 2, descrição visual específica, mais sutil]
7. ABSURDO CARTOON: [descrição do elemento cartoon misturado no realismo]

3. BASE: Faixa horizontal [COR ESCURA TEMÁTICA DO NICHO] com texto em 2 linhas:
"ACHOU OS 7? CLIQUE NO LINK"
"👉 TE MOSTRO A RESPOSTA E A SOLUÇÃO"
Fonte sans-serif extra-bold, texto branco, alinhado centro.

REGRAS GERAIS:
- Os 7 erros DISTRIBUÍDOS pela cena, todos visíveis ao olhar atento
- Composição em 3 zonas claras: título topo, cena centro, CTA base
- Estética inspirada em "Onde está Wally" com base fotográfica realista
- Compliance Facebook Ads: sem decote, sem violência, sem nada chocante
- Proibido travessão. Use vírgula ou ponto final.

REFORÇO DO FORMATO (IMPORTANTE):
ASPECT RATIO 4:5 (1080x1350). FEED DO INSTAGRAM, NÃO STORIES. Composição vertical fechada, mais larga que alta no padrão de feed. NÃO crie 9:16 nem 1:1. NÃO crie composição alongada de Stories.
````

**Regra de cor do CTA por nicho** (substituir `[COR ESCURA TEMÁTICA DO NICHO]`):

- Alimentação/emagrecimento: VERDE-ESCURO MUSGO
- Alimentação saudável/meal prep/nutrição: VERDE-ESCURO MUSGO
- Yoga/bem-estar: VERDE-MUSGO ESCURO
- Cannabis medicinal: VERDE-ESCURO MUSGO
- Direito/advocacia: AZUL-MARINHO PROFUNDO
- Tráfego pago/IA/digital: AZUL-MARINHO PROFUNDO ou AZUL ELÉTRICO ESCURO
- Skincare/lifestyle: TERRACOTA ESCURO
- Maternidade/beleza feminina/cabelo: VINHO ESCURO ou TERRACOTA
- Finanças/investimentos/aposentadoria: VERDE-ESCURO PROFUNDO ou DOURADO QUEIMADO
- Concurso público/educação: AZUL-MARINHO ou VINHO ESCURO
- Pet/animais: VERDE-MUSGO
- Cafeteria/gastronomia: MARROM CARAMELO ESCURO
- Fitness/saúde: VERDE-LIMÃO ESCURO ou VERMELHO TIJOLO

**Frase complementar do título por nicho** (substituir `[FRASE COMPLEMENTAR DO NICHO]`):

- Cronograma capilar: "QUE TÃO FAZENDO SEU CABELO CAIR"
- Aposentadoria: "QUE TÃO ATRASANDO SUA APOSENTADORIA"
- Skincare: "QUE TÃO ENVELHECENDO SUA PELE"
- Tráfego pago: "QUE TÃO TRAVANDO SUA CAMPANHA"
- Marmita/emagrecimento: "QUE TÃO TE FAZENDO ENGORDAR"
- Meal prep/organização alimentar: "QUE TÃO DESPERDIÇANDO SEU TEMPO E DINHEIRO NA COZINHA"

Construa a frase complementar no mesmo padrão pro nicho do produto ativo: começa com "QUE TÃO" e termina no problema concreto que o público vive.

#### D) Prompt pro ChatGPT (formato Stories)

Esse é fixo. Não precisa preencher placeholders.

````
Agora cria a exata mesma arte, mesmas cores, mesmo texto, mesmo visual, mesmos elementos, só diagramada pro formato Stories.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

### 4. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) no título e na legenda. Corrigir direto. Nunca mostrar versão bruta.

A descrição dos 7 erros, o texto do título da arte e o texto do CTA NÃO passam pela revisora (são conteúdo da arte com tom específico), mas devem respeitar Light Copy: sem travessão, sem exclamação.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Jogo dos 7 Erros:

📌 CENA ESCOLHIDA (nº {numero_cena} das 10)
[descrição da cena + os 7 erros]

📌 TÍTULO DO ANÚNCIO
[título gerado]

📝 LEGENDA PRO INSTAGRAM
[legenda gerada]

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

📱 PROMPT PRO CHATGPT, FORMATO STORIES
[prompt Stories, dentro de bloco de código]

---
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher outra cena (das 10)
```

Se escolher 2, perguntar o que ajustar (título, legenda, cena, os 7 erros ou CTA) e refazer apenas a parte indicada.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-jogo-7-erros-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-jogo-7-erros-{numero}.md`

Conteúdo do arquivo:

```markdown
# Jogo dos 7 Erros nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Cena escolhida (nº {numero_cena} das 10)

**Cena:** [descrição da cena]

**Os 7 erros:**
1. [erro profissional 1] (PROFISSIONAL)
2. [erro profissional 2] (PROFISSIONAL)
3. [erro profissional 3] (PROFISSIONAL)
4. [erro profissional 4] (PROFISSIONAL)
5. [easter egg 1] (EASTER EGG)
6. [easter egg 2] (EASTER EGG INTERNO)
7. [absurdo visual] (ABSURDO VISUAL)

## Título do anúncio

[título]

## Legenda pro Instagram

[legenda]

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt pro ChatGPT. Formato Stories (1080x1920, 9:16)

\`\`\`
[prompt Stories]
\`\`\`

## Como usar

1. Abra o ChatGPT (com geração de imagem habilitada).
2. Cole o **Prompt Feed** e espere a arte ser gerada.
3. Quando estiver pronto, mande "ok" no chat.
4. Cole o **Prompt Stories** pra gerar a versão vertical da mesma arte.

## Banco completo (as 10 ideias geradas nesta sessão)

Liste aqui todas as 10 cenas geradas nesta sessão, para o aluno usar depois sem precisar rodar a sub-skill de novo.
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-jogo-7-erros-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-jogo-7-erros-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Jogo dos 7 Erros salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-jogo-7-erros-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Jogo dos 7 Erros com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Jogo dos 7 Erros gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-jogo-7-erros-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-jogo-7-erros-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Jogo dos 7 Erros com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-jogo-7-erros-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-jogo-7-erros-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-jogo-7-erros-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-jogo-7-erros-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-jogo-7-erros-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda.
- A descrição dos 7 erros, o título da arte e o texto do CTA seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.

### Sobre a cena (sempre)

- Cena fotorrealista brasileira autêntica, ambiente classe média bem-cuidado.
- Pessoa(s) brasileira(s) real(is), não modelo de stock photo.
- Roupa coberta (compliance Facebook Ads).
- Expressão coerente com o contexto da cena.
- Luz natural quente (exceto se o erro envolve atmosfera fria, tipo escritório à noite).
- Cena identificável imediatamente como pertencente ao dia a dia do nicho.

### Sobre os 7 erros (proporção fixa)

- **4 erros profissionais reais** do nicho (ativam dor).
- **2 easter eggs/piadas internas** do nicho (geram comentário "kkkk vi o XXXX").
- **1 absurdo visual cartoon** (animal gigante, objeto absurdo).

Cada erro precisa estar:
- CLARAMENTE VISÍVEL (não escondido demais que ninguém ache).
- DISTRIBUÍDO pela cena (não amontoados num canto só).
- COM TEXTO LEGÍVEL quando o erro envolver letra (valor, etiqueta, calendário).

### Sobre o título (faixa branca no topo)

- "ENCONTRE OS 7 ERROS" + frase complementar do nicho.
- Exemplos de frase complementar:
  - Cronograma capilar: "QUE TÃO FAZENDO SEU CABELO CAIR"
  - Aposentadoria: "QUE TÃO ATRASANDO SUA APOSENTADORIA"
  - Skincare: "QUE TÃO ENVELHECENDO SUA PELE"
  - Tráfego pago: "QUE TÃO TRAVANDO SUA CAMPANHA"
  - Marmita/emagrecimento: "QUE TÃO TE FAZENDO ENGORDAR"
  - Meal prep/organização alimentar: "QUE TÃO DESPERDIÇANDO SEU TEMPO E DINHEIRO NA COZINHA"
- Fonte sans-serif extra-bold, texto preto sobre fundo branco.
- Alinhado ao centro.

### Sobre o CTA (faixa colorida na base)

- Cor de fundo escura temática do nicho (ver tabela de cor por nicho no Passo 3).
- Texto: "ACHOU OS 7? CLIQUE NO LINK" + "👉 TE MOSTRO A RESPOSTA E A SOLUÇÃO".
- Texto branco em sans-serif extra-bold.
- Alinhado ao centro.

### Sobre o reforço do aspect ratio

CRÍTICO: porque o prompt do Jogo dos 7 Erros é denso (7 erros + título + CTA + cena fotorrealista + cartoon absurdo), o GPT tende a esquecer o aspect ratio. SEMPRE colocar a instrução de 4:5:

1. **NO INÍCIO** do prompt (primeira coisa que aparece, antes mesmo do formato).
2. **NO MEIO** do prompt (na estrutura).
3. **NO FIM** do prompt (reforço explícito).

Isso reduz drasticamente a chance do GPT gerar em Stories (9:16) ou quadrado (1:1) por engano. O reforço triplo já está embutido no prompt Feed do Passo 3 e deve ser preservado intacto.

### Sobre compliance Facebook Ads (crítica)

- Sem pernas de fora, decote, roupa curta, poses sensualizadas.
- Sem violência, sangue, ferida, lesão grotesca.
- Pessoas SEMPRE com roupa coberta (manga longa, calça comprida).
- Sem expressões dramáticas exageradas de sofrimento.
- Os erros são humorísticos/irônicos, não chocantes ou apelativos.

### Sobre os easter eggs

Pra cada nicho, criar referências culturais que só quem é do segmento entende:
- Tráfego pago: ferramenta antiga ainda aberta, referência a guru polêmico, métrica famosa por ser inútil.
- Skincare: produto popular conhecido por não funcionar, referência a celebridade da propaganda.
- Cabelo: produto famoso barato, foto antiga da pessoa com cabelão.
- Aposentadoria: frase típica de quem procrastina ("vou pensar amanhã"), livro empoeirado de educação financeira.
- Yoga: aplicativo aberto que ela está em mais 30 abas, frase mística mal aplicada.
- Cannabis medicinal: confusão entre uso recreativo vs medicinal.
- Direito empresarial: livro de código antigo, diploma antigo.

### Sobre o absurdo visual cartoon

Sempre 1 elemento claramente cartoon no meio do realismo:
- Animal gigante (tartaruga, pinguim, hamster gigante, canguru, leão).
- Objeto fora de escala (patinho gigante, vassoura voadora).
- Personagem fora de contexto (hamster piloto, polvo segurando xícara).
- Elemento mágico (vassoura, bola de cristal, varinha).

A função é gerar humor e recompensar quem está realmente prestando atenção na imagem. Nunca mais que 1 absurdo cartoon: a magia está em 1 só, no meio do realismo.

### Sobre o que NÃO usar

- Travessão (— ou –). Sempre vírgula ou ponto final.
- Erros chocantes ou apelativos (ferida real, dor física grotesca).
- Erros impossíveis de ver (escondidos demais).
- Mais que 1 absurdo cartoon.
- Texto cobrindo a cena.

### Regras padrão

- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
