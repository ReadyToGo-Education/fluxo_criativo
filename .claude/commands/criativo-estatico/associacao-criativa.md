# Associação Criativa. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção de Associação Criativa. Cria criativos estáticos que associam um objeto completamente aleatório e improvável ao produto ou serviço, estilo agência de publicidade premiada (Leão de Ouro). Gera 10 ideias de associação, o aluno escolhe uma, e a sub-skill entrega título, legenda e prompts prontos pra colar no ChatGPT (Feed e Stories) e no Freepik (animação image-to-video).

Formato de criativo estático que associa um objeto completamente aleatório e improvável ao produto ou serviço do cliente. A lógica é: qualquer coisa pode ensinar algo sobre qualquer produto, desde que a conexão seja inteligente e surpreendente.

Exemplo: "O que um abacaxi pode te ensinar sobre inglês?" → abacaxi é pineapple → lição rápida → CTA pro curso.

O criativo precisa parecer que foi feito por uma agência de publicidade premiada no Leão de Ouro: design bonito, sofisticado, lúdico, super criativo e fora do padrão. Não é post de infoprodutor genérico. É peça de portfólio.

**Por que esse formato funciona:**
A associação distante e inteligente gera a reação "caramba, faz sentido" antes de a pessoa identificar que é anúncio. O design conceitual de agência premiada destoa do feed cheio de templates Canva e prende o olho. A ponte improvável entre objeto e nicho é compartilhável pela sacada, virando peça de portfólio que ainda vende.

## O que você está criando

Anúncios estáticos que parecem:
- peça de agência premiada
- arte conceitual de portfólio
- post que faz a pessoa parar e pensar "que sacada"
- conteúdo compartilhável pela inteligência da conexão

## O que você NUNCA cria

- Associações óbvias ou próximas (se o produto é violão, não associar com guitarra ou música)
- Design genérico de infoprodutor
- Cara de template Canva
- Texto longo ou explicativo
- Marketing óbvio, texto corporativo
- Associações forçadas que não fazem sentido lógico (a ponte precisa ser inteligente)

## Regra de ouro das associações

A associação precisa ser DISTANTE e RICA. Quanto mais improvável o objeto e mais inteligente a ponte, melhor o criativo.

RUIM (associação próxima): violão → guitarra, música, nota musical
BOM (associação distante): violão → abacaxi, chave de fenda, semáforo

RUIM (ponte forçada): "O que um sapato pode te ensinar sobre Excel?" → "Porque os dois precisam de ajuste" (fraco)
BOM (ponte inteligente): "O que um chiclete pode te ensinar sobre alisamento?" → "Entender a química muda tudo" (sacada real)

A ponte entre o objeto e o produto precisa gerar a reação: "caramba, faz sentido."

## O Que Fazer

### 1. Briefing

Se o produto ativo existir (há `meus-produtos/.ativo` apontando pra um produto com `perfil.md`), faça UMA pergunta única:

```
Quer usar os dados do produto ativo ({nome}) ou prefere informar produto e público manualmente?

1. Usar os dados do produto ativo
2. Informar manualmente
```

Se escolher 1, extraia produto, nicho e público do `perfil.md` (e `idconsumidor.md` se existir) e siga pra etapa 2.

Se escolher 2, OU se não houver produto ativo, pergunte direto:

```
Qual o produto/serviço?
```

Pare e espere a resposta. Depois pergunte:

```
Qual o público?
```

Pare e espere a resposta. Se o aluno não souber especificar o público, assuma um plausível brasileiro com base no produto e avise antes de gerar as ideias: "Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer."

### 2. Geração das 10 associações criativas

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de associação criativa pro seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere 10 associações entre objetos aleatórios e o produto.

Cada associação deve conter:
- O OBJETO improvável
- A PERGUNTA: "O que [objeto] pode te ensinar sobre [produto/nicho]?"
- A PONTE: a conexão inteligente em 1 frase (a sacada)

#### Regras das associações

- Os 10 objetos precisam ser de categorias completamente diferentes entre si (comida, ferramenta, animal, objeto doméstico, brinquedo, natureza, etc.)
- Nenhum objeto pode ter relação óbvia com o nicho
- A ponte precisa ser uma sacada real, inteligente, que faça sentido
- Variar entre pontes práticas, emocionais, contraintuitivas e bem-humoradas
- Sem travessão. Use vírgula, ponto final ou parênteses.

#### Apresentação

Mostre as 10 associações numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de associação criativa pro seu nicho.

---

**1.** OBJETO: [objeto improvável]
**Pergunta:** "O que [objeto] pode te ensinar sobre [produto/nicho]?"
**Ponte:** [a sacada inteligente em 1 frase]

---

**2.** OBJETO: [objeto improvável]
...

---

Escolha uma associação.
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

### 3. Desenvolvimento da ideia

Após o aluno escolher um número de 1 a 10, anuncie:

```
🔍 Próximo passo: desenvolver a ideia escolhida. Tempo estimado: cerca de 30 segundos.
```

Desenvolva a ideia completa com 2 pontos de desenvolvimento:

**TÍTULO:** A pergunta provocativa ("O que [objeto] pode te ensinar sobre [nicho]?")

**2 PONTOS DE DESENVOLVIMENTO:** Cada ponto tem uma frase de impacto em bold + uma frase de explicação que faz a ponte entre o objeto e o produto/nicho. A ponte é essencial, sem ela a associação não faz sentido.

**CTA:** Chamada direta pro produto.

Apresente assim:

```
TÍTULO: [pergunta provocativa]

OBJETO: [descrição visual do objeto integrado ao universo do nicho, os dois elementos precisam aparecer juntos na mesma cena]

DESENVOLVIMENTO:

01. "[Frase de impacto]"
"[Frase de explicação fazendo a ponte objeto → nicho]"

02. "[Frase de impacto]"
"[Frase de explicação fazendo a ponte objeto → nicho]"

CTA: [texto] →
```

Regra crítica do objeto visual: o objeto NUNCA aparece sozinho. Ele sempre aparece INTEGRADO ao universo do nicho. Exemplos:
- Cubo de gelo derretendo sobre cordas de violão (não cubo de gelo sozinho num fundo preto)
- Cebola cortada ao lado de frascos de skincare (não cebola sozinha)
- Liquidificador com dashboard de tráfego dentro (não liquidificador sozinho)

Depois de entregar, escreva:

**"Aprovou a ideia? Se sim, eu gero o prompt pra você colar no ChatGPT e criar a arte."**

### 4. Entrega dos prompts

Quando o aluno aprovar a ideia, entregue:

#### A) Legenda pro Instagram

Mínimo 3 linhas em primeira pessoa, tom de creator e de escritor (não de vendedor). Gera curiosidade sobre a associação sem entregar a sacada toda. Termina com "Te conto tudo no link 👇" ou similar.

Regras adicionais da legenda (Padrão de Legenda obrigatório desta skill):
- **Tom de escritor, não de vendedor**: alguém explicando uma coisa real, não fazendo propaganda
- **Ensina ou avisa, nunca vende**: nas primeiras linhas, a legenda traz um pedaço de conteúdo real (uma observação, um aprendizado, um aviso)
- **Especificidade mata generalização**: usar dados concretos, situações específicas, detalhes que parecem reais
- **Produto não aparece no início**: nada de "esse curso", "esse treinamento", nome do método ou sigla nas primeiras linhas
- **Sem travessão (—), sem ponto de exclamação, sem "Não é X. É Y."**, sem frases genéricas de vendedor ("transforme sua vida", "descubra o segredo", "método revolucionário")
- **Sem "mesmo que" e "sem precisar" como muleta**, sem lero-lero, sem promessa vaga
- **Sem emojis dentro do texto** (exceto o emoji final do CTA, do tipo "👇", que já está previsto na skill)
- A legenda termina com a chamada pro link, no padrão previsto na skill

#### B) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.** O prompt já traz a regra de paleta monocromática e a hierarquia visual; mantenha tudo no texto colado no ChatGPT.

Use a tabela "Paleta de cores por nicho" (logo abaixo de Regras) pra definir a paleta correta antes de preencher o prompt. Se o nicho não estiver na lista, escolha uma paleta monocromática que combine com a identidade visual do produto.

````
Cria pra mim uma arte de anúncio pra Instagram no formato ASSOCIAÇÃO CRIATIVA. Estilo agência de publicidade premiada. Design sofisticado, lúdico, conceitual.

CONCEITO DA ARTE:
[DESCRIÇÃO DETALHADA DO OBJETO INTEGRADO AO UNIVERSO DO NICHO. O objeto e elementos do nicho aparecem JUNTOS na mesma cena, fundidos numa composição editorial. Descrever: o que é o objeto, como ele interage com elementos do nicho, iluminação, atmosfera, tons de cor coerentes com o nicho.]

PALETA DE CORES DA ARTE INTEIRA (SEGUIR À RISCA):
[DEFINIR PALETA MONOCROMÁTICA COERENTE COM O NICHO. Incluir:
- Cor de fundo
- Cor de destaque tipográfico (hex)
- Cor do texto principal
- Cor do botão CTA
- Tom geral
- Reforçar: NÃO misturar cores que destoam. Paleta coesa.]

HIERARQUIA VISUAL E PROPORÇÕES (CRÍTICO, SEGUIR À RISCA):

A arte tem 3 zonas com proporções específicas. A harmonia entre elas é prioridade máxima.

ZONA 1 — TÍTULO (topo, ~20% da arte):
Texto: "[TÍTULO, PERGUNTA PROVOCATIVA]"
Fonte SANS-SERIF EXTRA-BOLD, caixa alta.
"[PALAVRA DO OBJETO]" e "[PALAVRA DO NICHO]" em [COR DE DESTAQUE] e levemente maiores. Restante em [PRETO ou BRANCO dependendo do fundo].
O título é GRANDE e impactante, mas ocupa no máximo 20% da altura da arte.

REGRA CRÍTICA DE LIMPEZA: NENHUM elemento decorativo ao redor do título. Sem estrelas, sem brilhos, sem sparkles, sem linhas decorativas, sem ícones, sem formas geométricas ornamentais. O título é SÓ TEXTO sobre fundo limpo. Nada mais.

ZONA 2 — IMAGEM + 2 PONTOS (centro, ~58% da arte):
Esta é a zona principal. Ocupa a maior parte da arte.

Imagem [DO OBJETO INTEGRADO AO NICHO] em posição dominante (lado esquerdo ou centro-esquerdo).

Do outro lado, 2 PONTOS NUMERADOS (01, 02) com ícones minimalistas elegantes em [COR DE DESTAQUE]:

01. Frase em BOLD: "[FRASE DE IMPACTO 1]"
Texto embaixo: "[EXPLICAÇÃO FAZENDO A PONTE OBJETO → NICHO]"

02. Frase em BOLD: "[FRASE DE IMPACTO 2]"
Texto embaixo: "[EXPLICAÇÃO FAZENDO A PONTE OBJETO → NICHO]"

SEM elementos decorativos ao redor dos pontos. Sem estrelas, sem brilhos, sem sparkles, sem linhas ornamentais. Só os números, os ícones minimalistas e o texto.

TAMANHO DAS FONTES (proporção entre si):
- Frases de impacto (bold): tamanho 100% (referência base)
- Textos de explicação: tamanho ~70% das frases de impacto
- Título (zona 1): tamanho ~120% das frases de impacto

As frases de impacto e as explicações precisam ser CONFORTAVELMENTE legíveis num celular.

Espaço generoso entre os pontos 01 e 02. Respiro visual.

ZONA 3 — CTA (base, ~22% da arte):
Fundo [TOM CLARO OU ESCURO COERENTE COM A PALETA], levemente separado do centro por uma linha fina ou mudança sutil de tom.

Texto de promessa: "[FRASE CURTA DE PROMESSA DO PRODUTO]"
Fonte SANS-SERIF SEMIBOLD, tamanho médio-grande. Alinhado à esquerda.

Ao lado direito, botão com fundo [COR DE DESTAQUE]:
"[CTA CURTO] →"
Fonte SANS-SERIF BOLD, [COR CONTRASTANTE].
O botão é PROPORCIONAL ao texto de promessa ao lado. NÃO é gigante. Ele ocupa ~35-40% da largura da zona. É um elemento dentro da zona de CTA, não a zona inteira.

O conjunto (texto de promessa + botão) fica alinhado horizontalmente, lado a lado, com respiro entre eles.

REGRA GERAL DE LIMPEZA (APLICAR NA ARTE INTEIRA):
PROIBIDO qualquer elemento puramente decorativo em toda a arte: estrelas, sparkles, brilhos, diamantes, formas geométricas ornamentais, linhas decorativas, arabescos, molduras, cantos decorados. A arte é LIMPA. Só tem: texto, imagem, números, ícones funcionais e o botão de CTA. NADA MAIS.

ESTÉTICA:
- Paleta MONOCROMÁTICA coerente com o nicho
- Objeto e elementos do nicho JUNTOS na mesma cena, integrados
- Qualidade fotográfica editorial/cinematográfica
- Layout ULTRA LIMPO, sem nenhum enfeite decorativo
- Harmonia de proporções e harmonia cromática
- NÃO pode parecer template Canva
- Peça de agência premiada

COMPLIANCE FACEBOOK ADS:
- Sem violência, sem conteúdo sensível
- Sem pernas de fora, decote, roupa curta, poses sensualizadas (quando houver pessoas)

PROIBIDO usar travessão (— ou –). Use vírgula ou ponto final.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Exact size reference: 1080x1350.
````

#### C) Prompt pro Freepik (animação image-to-video)

Esse é fixo. Não precisa preencher placeholders. Esse prompt anima a imagem JÁ gerada sem mexer em nada na arte nem no texto.

````
Animate this exact image keeping EVERYTHING exactly as it is. Do NOT change anything in the image, do NOT change any text, do NOT change colors, do NOT change composition, do NOT change framing, do NOT change aspect ratio, do NOT add elements, do NOT remove elements, do NOT crop, do NOT zoom, do NOT pan, do NOT rotate.

ALL TEXT OVERLAYS (title, headline, subtitle, captions, labels, CTA, any text box, any sticker text, any number, any icon, any button) MUST REMAIN 100% STATIC, FIXED, UNCHANGED, in the EXACT same position, EXACT same size, EXACT same color, EXACT same font, and EXACT same content as the original image. NO text can be cut off, cropped, moved, scaled, distorted, faded, replaced, animated, or pushed off-screen at any point in the video. Every letter of every text element must remain fully visible and identical from frame 1 to the last frame.

ALLOWED MOTION (only extremely subtle, ultra realistic micro-movements inside the image):
- If there is a person in the scene: natural slow blink every 2 to 3 seconds, soft breathing, very slight head or shoulder shift. Keep the exact facial expression frozen as in the original.
- If there are objects in the scene: barely perceptible ambient micro-motion (light reflection breathing slowly across a surface, soft vapor rising if applicable, fibers gently swaying, particles floating gently, leaves softly moving).
- Camera: 100% LOCKED. No pan, no zoom in, no zoom out, no parallax, no dolly, no rotation, no shake.

ENGLISH TRIGGERS (mandatory):
- "subtle micro-movements only"
- "static locked camera, no pan, no zoom, no parallax"
- "preserve all text overlays exactly as drawn, no text cropping, no text movement, no text scaling"
- "preserve composition, framing and aspect ratio identical to the input image"
- "natural blinking and breathing only"
- "no morphing, no text distortion, no warping"
- "image-to-video with minimal motion, cinemagraph style"
- "do not regenerate the image, animate the given image"

Duration: 5 seconds. Seamless loop. Output must look like the exact same still photo with only very subtle life added. Anyone comparing frame 1 of the video with the original image must see the SAME composition, SAME text fully visible, SAME colors, SAME framing, SAME aspect ratio.
````

Depois de entregar o Prompt Feed e o Prompt Freepik, pergunte:

Se o aluno disser sim, entregue o Prompt Stories:

````
Agora cria a exata mesma arte, mesmas cores, mesmo texto, mesmo visual, mesmo objeto, mesmos elementos, só diagramada pro formato Stories.

O objeto pode ocupar mais espaço vertical. O título pode ter fonte um pouco maior. O CTA mantém a mesma posição na base. Manter a mesma estética de agência premiada. Manter a arte LIMPA sem elementos decorativos.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

### 5. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) na legenda. Corrigir direto. Nunca mostrar versão bruta.

O texto interno do criativo (frases de impacto, explicações, CTA da arte, descrição do objeto) NÃO passa pela revisora, mas deve respeitar Light Copy: sem travessão, sem exclamação, sem "não é X. É Y.", e a ponte objeto → nicho precisa fazer sentido real.

### 6. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Associação Criativa:

📌 ASSOCIAÇÃO ESCOLHIDA (nº {numero_associacao} das 10)
Objeto: [objeto]
Ponte: [a sacada]

📝 LEGENDA PRO INSTAGRAM
[legenda gerada, mínimo 3 linhas]

🎯 DESENVOLVIMENTO (vai dentro da arte)
TÍTULO: [pergunta provocativa]
01. [frase de impacto 1]
    [explicação 1 fazendo a ponte]
02. [frase de impacto 2]
    [explicação 2 fazendo a ponte]
CTA: [texto do CTA] →

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

🎬 PROMPT PRO FREEPIK, ANIMAÇÃO
[prompt Freepik, dentro de bloco de código]

---
1. Sim, quero o Stories também
2. Aprovar e salvar do jeito que está
3. Quero ajustar algo
4. Voltar e escolher outra associação (das 10)
```

Se escolher 1, entregar o Prompt Stories e depois repetir a pergunta de aprovação (salvar incluindo o Stories).

Se escolher 3, perguntar o que ajustar (legenda, descrição do objeto, frases de impacto, explicações ou CTA) e refazer apenas a parte indicada.

Se escolher 4, apresentar a lista das 10 associações novamente e perguntar o novo número.

### 7. Gerar e salvar

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-associacao-criativa-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-associacao-criativa-{numero}.md`

Conteúdo do arquivo:

```markdown
# Associação Criativa nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Associação escolhida (nº {numero_associacao} das 10)

**Objeto:** [objeto]
**Pergunta:** "[pergunta provocativa]"
**Ponte:** [a sacada]

## Título do anúncio

[título, pergunta provocativa]

## Legenda pro Instagram

[legenda mínimo 3 linhas terminando com chamada pro link]

## Desenvolvimento (vai dentro da arte)

**OBJETO:** [descrição visual do objeto integrado ao universo do nicho]

**01.** "[frase de impacto 1]"
"[explicação 1 fazendo a ponte objeto → nicho]"

**02.** "[frase de impacto 2]"
"[explicação 2 fazendo a ponte objeto → nicho]"

**CTA:** [texto do CTA] →

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt pro ChatGPT. Formato Stories (1080x1920, 9:16)

\`\`\`
[prompt Stories]
\`\`\`

## Prompt pro Freepik (animação image-to-video)

\`\`\`
[prompt Freepik]
\`\`\`

## Como usar

1. Abra o ChatGPT (com geração de imagem habilitada).
2. Cole o **Prompt Feed** e espere a arte ser gerada.
3. (Opcional) Se gerou o Stories, mande "ok" e cole o **Prompt Stories** pra gerar a versão vertical da mesma arte.
4. Salve a imagem gerada (Feed ou Stories) e suba no Freepik (ferramenta image-to-video). Cole o **Prompt Freepik** como prompt de animação. O Freepik vai entregar um vídeo curto em loop com a arte animada de forma sutil, sem cortar nem mexer no texto.

## Banco completo (as 10 ideias geradas nesta sessão)

[Listar todas as 10 associações geradas nesta sessão, com número, objeto, pergunta e ponte, para o aluno usar depois sem precisar rodar a sub-skill de novo.]
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-associacao-criativa-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-associacao-criativa-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 8. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Associação Criativa salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-associacao-criativa-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outra Associação Criativa com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Associação Criativa gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-associacao-criativa-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-associacao-criativa-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outra Associação Criativa com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-associacao-criativa-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-associacao-criativa-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-associacao-criativa-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-associacao-criativa-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-associacao-criativa-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

### Light Copy e copy do anúncio

- Light Copy obrigatória no título e na legenda. Sem travessão (—), sem exclamação (!), sem promessa vaga, sem "não é X. É Y.".
- **Título é pergunta no formato fixo da associação** ("O que [objeto] pode te ensinar sobre [nicho]?"). Essa é a exceção do formato. A pergunta é o cerne do criativo. Objeto + nicho obrigatoriamente presentes no título.
- **Exceção documentada: emoji no CTA da legenda.** O Manual da Copy proíbe emojis em geral, mas a legenda termina com emoji (ex: "👇") no CTA pra fechar o padrão de creator. Essa exceção vale SOMENTE para o CTA da legenda. O título nunca usa emoji.
- Produto NÃO aparece no lead da legenda. Nada de "esse curso", "esse treinamento" ou nome do método nas primeiras linhas.
- **Legenda com no mínimo 3 linhas**, tom de escritor (não de vendedor), ensinando ou avisando antes de chamar pro link. Sem "mesmo que", "sem precisar", sem lero-lero. Sem emojis dentro do texto, exceto o emoji final do CTA.
- O texto interno do criativo (frases de impacto, explicações, CTA da arte, descrição do objeto) NÃO passa pela revisora, mas deve respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar a legenda.

### Sobre as associações

- SEMPRE distantes e improváveis, nunca objetos do mesmo universo do produto.
- A ponte precisa ser inteligente e fazer sentido real ("caramba, faz sentido").
- Os 10 objetos devem ser de categorias completamente diferentes entre si (comida, ferramenta, animal, objeto doméstico, brinquedo, natureza, etc.).
- Variar entre pontes práticas, emocionais, contraintuitivas e bem-humoradas.
- Sem associações óbvias ou próximas (se o produto é violão, não associar com guitarra ou música).

### Sobre a imagem

- O objeto NUNCA aparece sozinho, sempre integrado ao universo visual do nicho (cubo de gelo sobre cordas de violão, cebola ao lado de frascos de skincare, liquidificador com dashboard de tráfego dentro).
- Qualidade fotográfica editorial/cinematográfica.
- Iluminação coerente com a paleta do nicho.

### Sobre a estética

- Design de AGÊNCIA PREMIADA (Leão de Ouro). Sofisticado + lúdico + conceitual.
- Paleta MONOCROMÁTICA coerente com o nicho.
- Tipografia forte e editorial com hierarquia clara.
- Espaço negativo generoso.
- ZERO elementos decorativos (sem estrelas, sparkles, brilhos, linhas ornamentais, molduras).
- NUNCA parecer template Canva, post genérico, ou material varejão.

### Sobre o título

- Sempre no formato pergunta: "O que [objeto] pode te ensinar sobre [nicho]?"
- Curto, direto, provocativo
- Objeto + nicho obrigatoriamente presentes
- Só texto sobre fundo limpo, sem enfeites

### Sobre os 2 pontos de desenvolvimento

- Cada ponto: frase de impacto em bold + frase de explicação que faz a ponte objeto → nicho.
- A ponte objeto → nicho é essencial e não pode ser cortada.
- Legíveis no celular. Se ficarem pequenos, a arte falhou.
- Proporção: frases de impacto 100%, explicações 70%, título 120%.

### Sobre o CTA

- SEMPRE PRESENTE, nunca pode sumir.
- Texto de promessa à esquerda + botão proporcional à direita.
- Botão ocupa ~35-40% da largura, não domina a zona.
- Cor adaptada ao nicho.
- NUNCA usar "Comente X", "Marca uma amiga", ou modas não pedidas.

### Padrão de Personagem (se houver pessoa na cena)

Toda descrição de pessoa em qualquer prompt gerado por esta skill (Feed, Stories, animação ou listagem de ideias) deve garantir que a pessoa retratada seja:

- **Pessoa comum de classe média brasileira**, cuidada e bem-apresentada, mesmo em momento cotidiano
- **Aparência arrumada**: cabelo penteado, pele cuidada e saudável, roupa limpa e adequada à cena
- **Vestuário casual de classe média**: peças simples mas em bom estado (camiseta básica, blusa, calça, vestido comum), nunca rasgado, sujo, manchado ou muito amassado
- **NÃO modelo profissional** e **NÃO esculhambado**: o equilíbrio é pessoa real de classe média com vida normal e aparência cuidada

PROIBIDO gerar pessoa muito feia, descabelada, mal-vestida, com aparência de desleixo extremo, esculhambada, com roupa rasgada ou suja, ou em estado de descuido visível. Mesmo nas cenas de "problema", "antes" ou "jeito errado", a pessoa mantém aparência de classe média comum, cuidada, dentro do padrão visual de pessoa normal brasileira que cuida de si.

Esta diretriz deve ser incorporada ao descrever a pessoa dentro do prompt para o ChatGPT, garantindo que a imagem gerada nunca traga personagem feio, descabelado ou muito mal vestido.

### Compliance Facebook Ads

- Sem pernas de fora, decote, roupa curta, poses sensualizadas.
- Sem violência, sangue, ferida, lesão.
- Roupas sempre cobertas.
- PROIBIDO travessão (— ou –) em todo o texto gerado. Use vírgula ou ponto final.

### Fluxo e operação

- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Stories é entrega OBRIGATÓRIA, sempre junto do Feed.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 associações. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).

---

## Paleta de cores por nicho

A paleta precisa ser MONOCROMÁTICA e COERENTE com o universo do nicho. Usar uma cor de destaque que combine com a identidade visual do segmento:

- Música/instrumentos: fundo escuro, destaque DOURADO/ÂMBAR, texto branco
- Yoga/bem-estar/meditação: fundo claro, destaque VERDE-MUSGO ESCURO, texto grafite
- Cannabis medicinal: fundo escuro, destaque VERDE-ESCURO MUSGO, texto branco
- Direito/advocacia: fundo escuro, destaque DOURADO QUEIMADO, texto branco
- Skincare/beleza: fundo nude/rosé claro, destaque ROSÉ ESCURO (#8B4557), texto grafite
- Maternidade/bebê: fundo claro quente, destaque TERRACOTA ou ROSA ESCURO, texto grafite
- Finanças/investimentos: fundo escuro, destaque VERDE-ESCURO ou DOURADO, texto branco
- Educação/concursos: fundo claro, destaque AZUL-MARINHO, texto grafite
- Pet/animais: fundo claro, destaque VERDE-MUSGO, texto grafite
- Culinária/gastronomia: fundo quente, destaque MARROM CARAMELO, texto grafite
- Tráfego pago/IA/digital: fundo escuro, destaque VERDE-LIMÃO ou AZUL ELÉTRICO, texto branco
- Fitness/saúde/emagrecimento: fundo escuro, destaque VERDE-LIMÃO ESCURO, texto branco
- Empregabilidade/currículo: fundo claro, destaque AZUL-MARINHO, texto grafite
- Inglês/idiomas: fundo escuro, destaque AZUL ROYAL ou VERMELHO VIVO, texto branco
- Autoescola/direção: fundo escuro, destaque AMARELO VIVO, texto branco

Se o nicho não estiver na lista, escolha uma paleta monocromática que combine com a identidade visual do produto. A regra é: cor de destaque + fundo + texto precisam ser harmônicos entre si.
