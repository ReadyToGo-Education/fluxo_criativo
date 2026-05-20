# Criativo História + Quebra de Objeção. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 15 (Criativo História + Quebra de Objeção). Formato de criativo estático que usa uma mini-história em 4 quadros de diálogo entre duas pessoas pra quebrar uma objeção real do público. O anúncio precisa parecer conteúdo, não propaganda. Uma conversa inteligente que faz a pessoa pensar.

O entregável final são três prompts prontos pra colar: dois no ChatGPT (Feed + Stories) que geram a arte do criativo, e um terceiro no Freepik que anima a arte gerada sem alterar nada nela (nem foto, nem texto, só micro-movimento sutil).

## O que você está criando

Anúncios estáticos que parecem:
- prints virais
- conversas reais de WhatsApp
- mini histórias compartilháveis
- posts que fazem a pessoa parar o scroll

## O que você NUNCA cria

- Anúncio com cara de varejo
- Texto longo ou explicativo
- Linguagem de coach ou motivacional
- Frases genéricas tipo "acredite em você"
- Marketing óbvio, texto corporativo, cara de panfleto
- Infográfico escolar

## Fluxo da conversa

Siga os 5 passos abaixo em ordem. Cada passo depende da resposta do usuário. Nunca pule etapas.

---

### PASSO 1 — Briefing

Antes de perguntar, verifique se existe `meus-produtos/.ativo`. Se existir, leia `meus-produtos/{ativo}/perfil.md` (e `idconsumidor.md`, `tipo.md`, `preco.md` se existirem). Caso o orquestrador `/criativo-estatico` já tenha chamado esta sub-skill, o contexto já está carregado.

**Se houver produto ativo com dados úteis no perfil**, pergunte uma única vez:

```
Quer usar os dados do produto ativo ({nome do produto}) ou informar manualmente?

1. Usar os dados do produto ativo
2. Informar manualmente
```

Se escolher 1, extraia direto do perfil (Produto, Preço, Público) e siga pro PASSO 2.

Se escolher 2 (ou se não houver produto ativo), faça o briefing direto:

```
- Qual o produto?
- Qual o preço?
- Quem é o público?
```

Pare e espere a resposta.

---

### PASSO 2 — 10 objeções

Anuncie:

```
🔍 Próximo passo: gerar 10 objeções reais do seu público. Tempo estimado: cerca de 60 segundos.
```

Com base no briefing, gere 10 objeções reais que impedem esse público de comprar.

As objeções precisam soar como pensamentos reais, o tipo de coisa que a pessoa diria num grupo de WhatsApp ou pensaria sozinha antes de dormir. Específicas, emocionais ou práticas.

Bons exemplos de tom:
- "Já tentei isso antes e não funcionou."
- "Não tenho tempo pra mais uma coisa."
- "Tenho medo de gastar e me frustrar."
- "Isso deve funcionar só pra quem já sabe."
- "Minha idade já passou pra isso."
- "Não levo jeito."

Apresentação:

```
Aqui estão 10 objeções reais do seu público.

1. "[objeção 1]"
2. "[objeção 2]"
3. "[objeção 3]"
4. "[objeção 4]"
5. "[objeção 5]"
6. "[objeção 6]"
7. "[objeção 7]"
8. "[objeção 8]"
9. "[objeção 9]"
10. "[objeção 10]"

---
Escolha uma objeção.
```

Pare e espere o aluno escolher um número de 1 a 10. Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

---

### PASSO 3 — 10 ideias de criativo

Quando o usuário escolher a objeção, gere 10 ideias de criativo baseadas nela.

Cada ideia deve conter:
- **Título forte** (funciona como manchete)
- **Mini premissa** (a situação)
- **Quebra de expectativa** (o giro)
- **Gancho de curiosidade** (o que puxa pro clique)

As ideias precisam parecer conteúdos virais, algo que a pessoa compartilharia ou pararia pra ler.

Apresentação:

```
Aqui estão 10 ideias de criativo pra essa objeção.

---

**1.**
**Título forte:** [título]
**Mini premissa:** [a situação]
**Quebra de expectativa:** [o giro]
**Gancho de curiosidade:** [o que puxa pro clique]

---

**2.**
...

---

Escolha uma ideia.
```

Pare e espere o aluno escolher um número de 1 a 10. Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

---

### PASSO 4 — Roteiro final

Quando o usuário escolher a ideia, anuncie:

```
🔍 Próximo passo: gerar o roteiro do criativo em 4 quadros. Tempo estimado: cerca de 30 segundos.
```

Crie o roteiro completo do criativo seguindo a estrutura abaixo.

#### Estrutura obrigatória do roteiro

Todo criativo tem exatamente 3 partes:

**1. TÍTULO**

Frase curta, direta, provocativa, em primeira pessoa quando fizer sentido. O título precisa conter obrigatoriamente duas coisas em linguagem simples:
- O PRODUTO ou NICHO (o que é)
- A OBJEÇÃO (o conflito)

Leitura instantânea. Sem floreio, sem drama de revista, sem construções elaboradas. É uma afirmação ou pergunta provocativa que entrega o tema em 1 segundo.

Exemplo RUIM: "O erro invisível." (sem produto, sem objeção)
Exemplo RUIM: "O erro que faz tanta gente estudar inglês por anos sem conseguir falar." (longo demais, construção rebuscada)
Exemplo RUIM: "Por que quem não tem tempo aprende violão mais rápido do que quem tem" (confuso, longo)

Exemplo BOM: "Quem não tem tempo aprende violão mais rápido."
Exemplo BOM: "O medo de dirigir piora quando você tenta enfrentar."
Exemplo BOM: "Você não trava no inglês por falta de vocabulário."
Exemplo BOM: "Currículo bonito não garante entrevista."

Regra: se o título precisa ser relido pra ser entendido, está longo demais. Corte.

**2. DIÁLOGO EM 4 QUADROS**

Duas pessoas conversando. Cada quadro tem uma função:

- Quadro 1, OBJEÇÃO: a pessoa verbaliza a crença, medo ou dúvida
- Quadro 2, QUEBRA DE LÓGICA: a outra pessoa responde com algo inesperado
- Quadro 3, NOVA DÚVIDA: a primeira pessoa reage, intrigada
- Quadro 4, MICRO REVELAÇÃO: a segunda pessoa entrega uma percepção que muda tudo

Regras do diálogo:
- Parecer conversa real entre duas pessoas diferentes
- Frases curtas, naturais, emocionais
- Sem cara de copy, sem marketing óbvio, sem explicação longa
- Cortar ~60% do texto que parecer desnecessário, o criativo precisa ser instantâneo de ler

A resposta da segunda pessoa (quadro 2) NUNCA pode ser:
- "você consegue"
- "é só acreditar"
- "todo mundo consegue"
- qualquer variação motivacional vazia

A resposta precisa trazer:
- Uma lógica inesperada
- Uma percepção contraintuitiva
- Um erro invisível que a pessoa não sabia que cometia
- Algo que faça pensar "caramba, isso faz sentido"

**3. CTA VISUAL**

Exemplos:
- QUERO APRENDER ↓
- DESCUBRA O MÉTODO ↓
- VEJA COMO FUNCIONA ↓
- QUERO COMEÇAR ↓
- CLIQUE E APRENDA ↓

#### Personagens

Sempre 2 pessoas visualmente diferentes (roupas, estilo, aparência, gênero ou idade diferentes). Nunca pode parecer a mesma pessoa falando consigo mesma. Pessoa 1 aparece nos painéis 1 e 3, Pessoa 2 aparece nos painéis 2 e 4.

#### Tom

- Moderno, inteligente, perspicaz
- Natural e compartilhável
- Emocional sem ser piegas
- Nunca professoral, corporativo, coach ou exageradamente vendedor

#### Formato de apresentação do roteiro

Apresente assim:

```
TÍTULO: [título]

PERSONAGENS:
- Pessoa 1: [descrição visual breve]
- Pessoa 2: [descrição visual breve]

QUADRO 1:
[Pessoa 1]: "[fala]"

QUADRO 2:
[Pessoa 2]: "[fala]"

QUADRO 3:
[Pessoa 1]: "[fala]"

QUADRO 4:
[Pessoa 2]: "[fala]"

CTA: [texto] ↓
```

Depois de entregar o roteiro, escreva:

**"Aprovou o roteiro? Se sim, eu gero o prompt pra você colar no ChatGPT e criar a arte."**

Pare e espere a resposta. Se o aluno pedir ajuste no roteiro (título, fala de um quadro, CTA, descrição dos personagens), refaça só a parte indicada e volte ao gate.

---

### PASSO 5 — Prompts prontos (Feed + Stories no ChatGPT + Animação no Freepik)

Quando o usuário aprovar o roteiro, anuncie:

```
🔍 Próximo passo: gerar legenda e prompts pro ChatGPT + Freepik. Tempo estimado: cerca de 30 segundos.
```

Em seguida, entregue:

#### A) Legenda pro Instagram

**Mínimo 3 linhas**, em primeira pessoa, tom de creator. Termina com "Te conto tudo no link 👇" ou similar.

Aplicar os princípios do Manual da Copy (`.claude/skills/revisora/references/manual-copy.md`):

- **Tom de escritor, não de vendedor**: alguém explicando uma coisa real, não fazendo propaganda
- **Ensina ou avisa, nunca vende**: nas primeiras linhas, a legenda traz um pedaço de conteúdo real (uma observação, um aprendizado, um aviso)
- **Especificidade mata generalização**: usar dados concretos, situações específicas, detalhes que parecem reais
- **Produto não aparece no início**: nada de "esse curso", "esse treinamento", nome do método ou sigla nas primeiras linhas
- **Sem travessão (—), sem ponto de exclamação, sem "Não é X. É Y."**, sem frases genéricas de vendedor ("transforme sua vida", "descubra o segredo", "método revolucionário")
- **Sem "mesmo que" e "sem precisar" como muleta**, sem lero-lero, sem promessa vaga
- **Sem emojis dentro do texto** (exceto o emoji final do CTA, do tipo "👇", que já está previsto na skill)
- A legenda termina com a chamada pro link

#### B) Prompt de Feed (4:5)

Substitua todos os placeholders pelos dados reais (título do criativo, descrição visual dos personagens, falas dos 4 quadros, cor temática do nicho). **O texto final ao usuário não pode ter colchetes.**

````
Cria pra mim uma arte de anúncio pra Instagram no formato HISTÓRIA EM QUADRINHOS COM FOTOS REAIS + QUEBRA DE OBJEÇÃO.

COMPOSIÇÃO GERAL:
Arte estática estilo QUADRINHO / HQ com FOTOS REAIS de pessoas brasileiras. Layout vertical dividido em 3 zonas: título dramático no topo, grid 2x2 de painéis fotográficos no centro, CTA grande na base. Estética de quadrinho moderno com bordas grossas entre os painéis. Fundo branco ou claro entre os painéis.

ESTRUTURA OBRIGATÓRIA, 3 ZONAS VERTICAIS:

ZONA 1, TÍTULO (topo, ~18% da arte):
Fundo branco ou claro.
Texto: "[TÍTULO DO CRIATIVO]"
Fonte SANS-SERIF EXTRA-BOLD/BLACK, caixa alta, tamanho BEM GRANDE e impactante.
A palavra-chave principal do nicho ou a palavra mais emocional do título deve estar DESTACADA em cor [COR TEMÁTICA DO NICHO] (o resto em preto puro).
Pode ter elementos gráficos de ênfase ao redor (linhas de impacto estilo HQ, aspas estilizadas, sublinhado em cor).
Centralizado.

ZONA 2, GRID 2x2 DE PAINÉIS FOTOGRÁFICOS (centro, ~60% da arte):
4 painéis fotográficos organizados em GRID 2x2 (2 colunas, 2 linhas).
Cada painel é uma FOTO REAL mostrando a cena do diálogo.
Bordas grossas (3 a 5px) entre os painéis, cor escura ou preta.
Cada painel tem um NÚMERO no canto superior esquerdo (1, 2, 3, 4) dentro de um círculo colorido [COR TEMÁTICA DO NICHO].

PERSONAGEM 1, [DESCRIÇÃO VISUAL DA PESSOA 1]:
Aparece nos painéis 1 e 3 (esquerda superior e esquerda inferior).
Expressão facial compatível com o que está dizendo.
Enquadramento de busto/rosto, close expressivo.

PERSONAGEM 2, [DESCRIÇÃO VISUAL DA PESSOA 2]:
Aparece nos painéis 2 e 4 (direita superior e direita inferior).
Expressão facial compatível com o que está dizendo (confiante, explicando).
Enquadramento de busto/rosto, close expressivo.

Cada painel tem um BALÃO DE FALA branco com borda, estilo HQ clássico, com texto em PRETO.
Palavras-chave importantes dentro dos balões podem estar em NEGRITO ou em cor [COR TEMÁTICA DO NICHO] pra destaque.

PAINEL 1 (superior esquerdo): [FALA PESSOA 1, QUADRO 1]
PAINEL 2 (superior direito): [FALA PESSOA 2, QUADRO 2]
PAINEL 3 (inferior esquerdo): [FALA PESSOA 1, QUADRO 3]
PAINEL 4 (inferior direito): [FALA PESSOA 2, QUADRO 4]

Fonte dos balões: SANS-SERIF BOLD, legível, tamanho médio-grande.
Texto em preto sobre fundo branco do balão.
Balões com formato orgânico de HQ (não retangulares perfeitos), com rabinho apontando pro personagem.

ZONA 3, CTA (base, ~22% da arte):
Faixa grande ocupando toda a largura da arte.
Fundo: [COR TEMÁTICA DO NICHO] vibrante e forte.
Pode ter 2 a 3 linhas de texto empilhadas:
- Linha principal: frase de promessa/impacto em fonte EXTRA-BOLD BEM GRANDE, caixa alta.
- Linha secundária: "CLIQUE NO LINK ABAIXO ↓" ou similar em fonte menor, também bold.
Cor do texto: branco puro ou preto puro (o que contrastar melhor).
Pode ter elementos gráficos de ênfase (linhas de impacto, setas, brilhos estilo HQ).
Margem mínima de 8 a 10% da borda inferior.

REFERÊNCIA DE COR DO NICHO: [COR TEMÁTICA BASEADA NA TABELA]

SOBRE AS FOTOS:
- Fotos ULTRA-REALISTAS de brasileiros reais
- Expressões faciais EXPRESSIVAS e EMOCIONAIS (compatíveis com o diálogo)
- Pessoa 1: expressão de dúvida, frustração ou medo nos painéis 1 e 3
- Pessoa 2: expressão confiante, explicando, acolhedora nos painéis 2 e 4
- Enquadramento close/busto
- Cenário coerente com o nicho (pode ser o mesmo cenário nos 4 painéis ou cenários complementares)
- Os 2 personagens precisam ser VISUALMENTE DIFERENTES (gênero, idade, roupa ou estilo)
- Iluminação natural, estética UGC brasileira

COMPLIANCE FACEBOOK ADS:
- Sem pernas de fora, decote, roupa curta, poses sensualizadas
- Sem violência, sangue, ferida, lesão
- Roupas sempre cobertas

PROIBIDO usar travessão (— ou –). Use vírgula ou ponto final.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Exact size reference: 1080x1350.
````

Pare e espere a resposta.

#### C) Prompt de Stories (9:16)

Se o usuário disser sim, entregue o prompt de Stories. Esse é fixo, não precisa preencher placeholders.

````
Agora cria a exata mesma arte, mesmas cores, mesmo texto, mesmo visual, mesmos elementos, mesmos personagens, mesmos cenários, só diagramada pro formato Stories.

O grid 2x2 pode ter painéis ligeiramente mais altos. O título pode ter fonte um pouco maior. O CTA mantém a mesma posição na base. Manter os mesmos personagens, mesmas expressões, mesmos balões.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

#### D) Prompt de Animação (Freepik)

Depois de entregar o Stories (ou junto com ele, se o usuário pular pro Stories direto), entregue o terceiro prompt pra colar no Freepik. Ele anima a imagem JÁ gerada sem mexer em nada nela: nem na foto, nem nos personagens, nem nas expressões, nem nos balões de fala, nem no título, nem no CTA, nem nas cores, nem no enquadramento. Só adiciona micro-movimento idle sutil em cada um dos 4 painéis (respiração leve, piscar lento, leve micro-tremor da mão), preservando 100% a leitura da história em quadrinhos.

````
Animate this comic-style image with extremely subtle, slow, idle motion in each of the 4 panels. DO NOT change anything in the image: keep the exact same artwork, same composition, same framing, same 2x2 grid layout, same panel borders, same numbered circles, same characters, same facial expressions, same poses, same lighting, same colors, same background of each panel.

DO NOT add, remove, move, redraw, restyle, or modify any text. The top title text, ALL 4 speech bubbles (with their exact text content, font, color, position, and shape), the panel numbers (1, 2, 3, 4) and the bottom CTA bar (with all its text lines) must remain 100% STATIC, FIXED, UNCHANGED, in the exact same position, size, color, font, and content as the original image. No text animation, no text fade, no text shift, no text replacement, no bubble morphing.

Only animate the people inside each photographic panel with EXTREMELY SUBTLE, SLOW, idle motion that preserves the comic-book "frozen moment" feeling:
- Panel 1: very subtle breathing motion of Person 1, slight micro-movement preserving the same facial expression of doubt/frustration.
- Panel 2: very subtle breathing motion of Person 2, slight micro-movement preserving the same confident/explaining facial expression.
- Panel 3: very subtle breathing motion of Person 1, slight micro-movement preserving the same intrigued facial expression.
- Panel 4: very subtle breathing motion of Person 2, slight micro-movement preserving the same revealing facial expression.
- A single slow blink every 2-3 seconds is OK in each panel.
- Keep the exact same facial expressions frozen as in the original, no smile change, no eyebrow change, no mouth change, no head turn.
- Ultra slow, looping, "still photo barely alive" pace. No fast motion, no camera shake, no zoom in/out, no panning inside the panels.

CRITICAL CONSTRAINTS:
- Do NOT alter, replace, regenerate, restyle, recolor, or animate the title text, the speech bubbles, the panel numbers, or the CTA bar. They are static graphic overlays.
- Do NOT change any character's facial expression, pose, framing, lighting, colors, or composition.
- Do NOT add new objects, new people, particles, props, or elements that are not in the original image.
- Do NOT add camera movement, zoom, dolly, or pan.
- Do NOT break the 2x2 grid or the panel borders.
- Output: a seamless looping video, same aspect ratio as the input image (4:5 for Feed, 9:16 for Stories), 3 to 5 seconds, 24 fps.
````

Depois de entregar os prompts, diga pro usuário:

1. Colar o primeiro prompt no ChatGPT pra gerar o Feed, mandar "ok", e colar o segundo pra gerar o Stories.
2. Baixar a imagem gerada (Feed ou Stories, ou as duas).
3. Subir a imagem no Freepik (ferramenta de image-to-video) e colar o terceiro texto como prompt de animação. O Freepik vai entregar um vídeo curto em loop com a arte animada de forma sutil, sem mexer em texto, balões, título nem CTA.

---

## Auto-revisão obrigatória

Antes de mostrar a legenda ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) na legenda. Corrigir direto. Nunca mostrar versão bruta.

As falas dos 4 quadros, o título do criativo (que vai dentro do prompt) e o texto do CTA NÃO passam pela revisora (são conteúdo da arte com tom específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, e a resposta do quadro 2 nunca cai em motivação vazia.

---

## Aprovação final e salvamento

Após entregar os prompts, pergunte:

```
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher outra ideia (das 10) ou outra objeção
```

Se escolher 2, perguntar o que ajustar (legenda, descrição visual dos personagens, cor temática) e refazer apenas a parte indicada.

Se escolher 3, perguntar se quer trocar só a ideia (apresentar a lista das 10 ideias novamente) ou trocar a objeção (apresentar a lista das 10 objeções novamente).

Quando aprovar, pergunte como o aluno quer gerar a imagem:

```
Como você quer gerar a imagem?

1. Colar no ChatGPT ou Gemini (grátis)
   Eu te entrego os prompts prontos. Você cola, gera as artes e salva.

2. Gerar agora pelo OpenRouter (tem custo)
   Eu mando o prompt direto pro modelo de imagem e já salvo o PNG na sua
   pasta. Custa centavos por imagem.

Digite o número:
```

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-criativo-historia-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-criativo-historia-{numero}.md`

Conteúdo do arquivo:

```markdown
# Criativo História + Quebra de Objeção nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Preço:** [preço]
**Nicho:** [nicho]
**Público:** [público]
**Cor temática do nicho:** [cor]

## Objeção escolhida (nº {numero_objecao} das 10)

"[objeção]"

## Ideia escolhida (nº {numero_ideia} das 10)

**Título forte:** [título]
**Mini premissa:** [premissa]
**Quebra de expectativa:** [giro]
**Gancho de curiosidade:** [gancho]

## Legenda pro Instagram

[legenda, mínimo 3 linhas]

## Roteiro em 4 quadros

TÍTULO: [título do criativo]

PERSONAGENS:
- Pessoa 1: [descrição visual]
- Pessoa 2: [descrição visual]

QUADRO 1:
[Pessoa 1]: "[fala]"

QUADRO 2:
[Pessoa 2]: "[fala]"

QUADRO 3:
[Pessoa 1]: "[fala]"

QUADRO 4:
[Pessoa 2]: "[fala]"

CTA: [texto] ↓

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt pro ChatGPT. Formato Stories (1080x1920, 9:16)

\`\`\`
[prompt Stories]
\`\`\`

## Prompt pro Freepik. Animação image-to-video

\`\`\`
[prompt Freepik]
\`\`\`

## Como usar

1. Abra o ChatGPT (com geração de imagem habilitada).
2. Cole o **Prompt Feed** e espere a arte ser gerada.
3. Quando estiver pronto, mande "ok" no chat.
4. Cole o **Prompt Stories** pra gerar a versão vertical da mesma arte.
5. Baixe a imagem gerada (Feed ou Stories, ou as duas).
6. Suba a imagem no Freepik (ferramenta de image-to-video) e cole o **Prompt Freepik** como prompt de animação. O Freepik vai entregar um vídeo curto em loop com a arte animada de forma sutil, sem mexer em texto, balões, título nem CTA.

## Banco completo (as 10 objeções e as 10 ideias geradas nesta sessão)

### 10 objeções
1. "[objeção 1]"
2. "[objeção 2]"
...
10. "[objeção 10]"

### 10 ideias (a partir da objeção escolhida)
[Listar todas as 10 ideias geradas nesta sessão, com número, título forte, mini premissa, quebra de expectativa e gancho de curiosidade, para o aluno usar depois sem precisar rodar a sub-skill de novo.]
```

---

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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-criativo-historia-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-criativo-historia-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

## Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Criativo História + Quebra de Objeção salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-criativo-historia-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro criativo com outra das 10 ideias
2. Voltar e escolher outra objeção (gera 10 novas ideias)
3. Trocar o nicho ou público e gerar 10 objeções novas
4. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Criativo História + Quebra de Objeção gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-criativo-historia-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-criativo-historia-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro criativo com outra das 10 ideias
3. Voltar e escolher outra objeção (gera 10 novas ideias)
4. Trocar o nicho ou público e gerar 10 objeções novas
5. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-criativo-historia-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-criativo-historia-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-criativo-historia-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-criativo-historia-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-criativo-historia-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

---

## Tabela de cores por nicho

- Música/instrumentos: ROXO PROFUNDO ou AZUL ELÉTRICO
- Yoga/bem-estar/meditação: VERDE-MUSGO ESCURO
- Cannabis medicinal: VERDE-ESCURO MUSGO
- Direito/advocacia: AZUL-MARINHO PROFUNDO
- Skincare/lifestyle/geral: LARANJA VIVO
- Maternidade/beleza feminina: ROSA ESCURO ou TERRACOTA
- Finanças/investimentos: VERDE-ESCURO ou DOURADO QUEIMADO
- Educação/concursos: AZUL-MARINHO ou AMARELO MOSTARDA
- Pet/animais: VERDE-MUSGO
- Culinária/gastronomia: MARROM CARAMELO
- Tráfego pago/IA/digital: AZUL ELÉTRICO ou ROXO
- Fitness/saúde/emagrecimento: VERDE-LIMÃO ESCURO ou VERMELHO TIJOLO
- Empregabilidade/currículo: AZUL-MARINHO ou LARANJA VIVO

Se o nicho não estiver na lista, escolha a cor que melhor combina com a identidade visual do produto.

---

## Regras

### Sobre copy (Light Copy)
- Light Copy obrigatória no título do criativo e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- **Exceção documentada: emoji no CTA da legenda.** O Manual da Copy proíbe emojis em geral, mas a legenda termina com emoji (ex: "👇") no CTA porque integra o padrão visual de creator amador, que é o que confere autenticidade ao formato. Essa exceção vale SOMENTE para o CTA da legenda.
- Produto NÃO aparece no lead do título do criativo nem da legenda.
- **Legenda mínima de 3 linhas**, redigida seguindo o Manual da Copy: tom de escritor (não de vendedor), ensina ou avisa nas primeiras linhas, especificidade mata generalização, produto fora do início, sem "mesmo que" / "sem precisar" / lero-lero / promessa vaga, sem emojis no meio do texto (só no CTA final).
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar a legenda.
- As falas dos 4 quadros, o título do criativo e o texto do CTA NÃO passam pela revisora, mas respeitam Light Copy (sem travessão, sem exclamação).

### Sobre o título do criativo
- O título do criativo (que vai na ZONA 1 da arte) precisa conter PRODUTO/NICHO + OBJEÇÃO em linguagem simples.
- Leitura instantânea em 1 segundo. Se precisa ser relido pra ser entendido, está longo demais. Cortar.

### Sobre o diálogo em 4 quadros
- Estrutura obrigatória: Quadro 1 OBJEÇÃO, Quadro 2 QUEBRA DE LÓGICA, Quadro 3 NOVA DÚVIDA, Quadro 4 MICRO REVELAÇÃO.
- Frases CURTAS, o criativo inteiro precisa ser lido em 3 segundos.
- Cortar ~60% do texto que parecer desnecessário.
- A resposta do Quadro 2 NUNCA pode ser motivação vazia ("você consegue", "é só acreditar", "todo mundo consegue"). Precisa trazer lógica inesperada, percepção contraintuitiva, erro invisível ou algo que faça pensar "caramba, isso faz sentido".
- Sem cara de copy, sem marketing óbvio, sem explicação longa, sem texto vendedor.

### Sobre a estrutura visual
- 3 zonas verticais obrigatórias: TÍTULO (topo, ~18%) + GRID 2x2 DE PAINÉIS FOTOGRÁFICOS (centro, ~60%) + CTA (base, ~22%).
- Estilo QUADRINHO / HQ com fotos reais de brasileiros.
- Grid 2x2 com bordas grossas (3 a 5px) entre painéis.
- Números nos cantos (1, 2, 3, 4) em círculos coloridos na cor temática do nicho.
- Balões de fala brancos estilo HQ com texto em preto.
- Palavra-chave do título destacada em cor temática do nicho.
- CTA grande, faixa colorida, pode ter 2 a 3 linhas empilhadas.

### Sobre o CTA visual
- SEMPRE PRESENTE, nunca pode sumir.
- Faixa colorida ocupando toda a largura.
- Cor adaptada ao nicho (tabela de cores).
- Texto em caixa alta, fonte extra-bold.
- Pode ter linha principal (promessa) + linha secundária (chamada pro link).
- Margem mínima de 8 a 10% da borda inferior.
- NUNCA usar "Comente X", "Marca uma amiga", ou modas não pedidas.

### Sobre os personagens
- Sempre 2 pessoas VISUALMENTE DIFERENTES (gênero, idade, roupa ou estilo diferentes entre si).
- Nunca parecer a mesma pessoa falando consigo mesma.
- Fotos ultra-realistas, enquadramento close/busto.
- Expressões faciais expressivas e compatíveis com o diálogo.
- Pessoa 1 (painéis 1 e 3): expressão de dúvida, frustração, medo.
- Pessoa 2 (painéis 2 e 4): expressão confiante, acolhedora, explicando.

### Padrão de Personagem (Adição Obrigatória)

Toda descrição de pessoa em qualquer prompt gerado por esta skill (Feed, Stories, animação ou listagem de ideias) deve garantir que a pessoa retratada seja:

- **Pessoa comum de classe média brasileira**, cuidada e bem-apresentada, mesmo em momento cotidiano
- **Aparência arrumada**: cabelo penteado, pele cuidada e saudável, roupa limpa e adequada à cena
- **Vestuário casual de classe média**: peças simples mas em bom estado (camiseta básica, blusa, calça, vestido comum), nunca rasgado, sujo, manchado ou muito amassado
- **NÃO modelo profissional** e **NÃO esculhambado**: o equilíbrio é pessoa real de classe média com vida normal e aparência cuidada

PROIBIDO gerar pessoa muito feia, descabelada, mal-vestida, com aparência de desleixo extremo, esculhambada, com roupa rasgada ou suja, ou em estado de descuido visível. Mesmo nas cenas de "problema", "antes" ou "jeito errado", a pessoa mantém aparência de classe média comum, cuidada, dentro do padrão visual de pessoa normal brasileira que cuida de si.

Esta diretriz deve ser incorporada ao descrever a pessoa dentro do prompt para o ChatGPT, garantindo que a imagem gerada nunca traga personagem feio, descabelado ou muito mal vestido.

### Padrão de Legenda (Adição Obrigatória)

Toda legenda pro Instagram entregue por esta skill deve ter **no mínimo 3 linhas**, redigida seguindo os princípios do Manual da Copy (`.claude/skills/revisora/references/manual-copy.md`):

- **Tom de escritor, não de vendedor**: alguém explicando uma coisa real, não fazendo propaganda
- **Ensina ou avisa, nunca vende**: nas primeiras linhas, a legenda traz um pedaço de conteúdo real (uma observação, um aprendizado, um aviso)
- **Especificidade mata generalização**: usar dados concretos, situações específicas, detalhes que parecem reais
- **Produto não aparece no início**: nada de "esse curso", "esse treinamento", nome do método ou sigla nas primeiras linhas
- **Sem travessão (—), sem ponto de exclamação, sem "Não é X. É Y."**, sem frases genéricas de vendedor ("transforme sua vida", "descubra o segredo", "método revolucionário")
- **Sem "mesmo que" e "sem precisar" como muleta**, sem lero-lero, sem promessa vaga
- **Sem emojis dentro do texto** (exceto o emoji final do CTA, do tipo "👇", que já está previsto na skill)
- A legenda termina com a chamada pro link, no padrão já previsto na skill original

Aplicar esta regra ao redigir a legenda apresentada ao usuário no item "Legenda pro Instagram" da entrega, expandindo para no mínimo 3 linhas e checando todos os vícios proibidos do Manual da Copy.

### Sobre o prompt de animação (Freepik)
- É o TERCEIRO bloco de texto entregue, depois dos prompts de Feed e Stories do ChatGPT.
- Roda no Freepik (image-to-video), não no ChatGPT.
- Função única: animar a imagem JÁ gerada.
- **PROIBIDO** mudar qualquer coisa na imagem: foto, composição, enquadramento, layout do grid 2x2, bordas dos painéis, círculos numerados, personagens, expressões faciais, poses, luz, cores.
- **PROIBIDO** mudar, redesenhar, animar ou substituir o título no topo, os 4 balões de fala (com seu conteúdo, fonte, cor, posição e forma exatos), os números dos painéis (1, 2, 3, 4) e o CTA na base. Tudo isso fica 100% estático.
- **PROIBIDO** adicionar câmera (zoom, pan, dolly, shake) ou quebrar o grid 2x2.
- **As expressões faciais SÃO a história**: ficam congeladas idênticas ao frame original. Sem mudança de sorriso, sobrancelha, boca, virada de cabeça.
- Movimento permitido: micro-motion idle muito sutil em cada painel (respiração leve, piscar lento a cada 2-3 segundos).
- Ritmo: ultra lento, "foto parada que mal está viva", loop curto de 3 a 5 segundos.
- Aspect ratio: igual ao da imagem de origem (4:5 pro Feed, 9:16 pros Stories).

### Compliance Facebook Ads
- Sem pernas de fora, decote, roupa curta, poses sensualizadas.
- Sem violência, sangue, ferida, lesão.
- Roupas sempre cobertas.

### O que NÃO usar na arte
- Travessão (— ou –). Usar vírgula ou ponto final.
- Logos de redes sociais.
- "Comente X", "Marca uma amiga".
- Fontes serifadas.
- Visual poluído ou com excesso de elementos.
- Texto longo nos balões.
- Linguagem de coach, motivacional, corporativa, professoral ou exageradamente vendedora.
- Frases genéricas tipo "acredite em você", "transforme sua vida", "descubra o segredo", "método revolucionário".
- Cara de varejo, panfleto ou infográfico escolar.

### Operação
- Substituir TODOS os placeholders dos prompts. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
