# ASMR / Sensação. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 10 (ASMR / Sensação). Gera um criativo a partir de uma foto super zoom ultra macro de um detalhe sensorial específico do nicho, com textura ASMR rica (microreflexos, fibras, gotas, microtextura tátil), capturada como um frame perfeito de ASMR pausado. A imagem comunica a identidade visual do nicho em 1 segundo. Gera 10 ideias ASMR/Sensação, o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
A imagem super macro ativa uma sensação física no espectador antes de ele perceber que é anúncio. A textura ASMR rica para o scroll porque o olho é atraído pelo detalhe sensorial congelado no tempo. O texto principal declara a sensação prazerosa mais a categoria do produto, e o CTA promete o resultado concreto, mantendo o método escondido. Essa lacuna entre o que a arte mostra e o que o CTA promete é o que gera o clique.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço.
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho.
- **Quadro / promessa**: a transformação principal do `perfil.md`, pra alimentar a regra de curiosidade (o CTA promete revelar o que entrega esse resultado).

### 1. Apresentar resumo do contexto e confirmar

SEMPRE mostre o resumo, mesmo se algum campo veio de inferência. Marque o que é real e o que foi inferido:

```
Vou usar estes dados do seu produto ativo ({slug}):

Produto: [nome do produto]
Nicho: [nicho]
Público: [resumo do público]

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
- Se for de yoga/bem-estar: "Curso de Yoga pra iniciantes em casa", "Mentoria de Meditação pra ansiedade", "Treinamento de Yoga Restaurativa pra mulheres 40+"
- Se for de skincare: "Curso de Skincare pra mulheres 40+", "Mentoria de rotina de pele pós-menopausa", "Ebook de anti-aging caseiro"
- Se for de tráfego: "Mentoria de Tráfego Pago pra criadores", "Curso de Anúncios no Meta pra agências", "Consultoria de Performance pra ecommerce"
- Se for de cafeteria: "Consultoria de Cardápio pra donos de cafeteria", "Treinamento de Barista pra equipes", "Curso de Como Abrir uma Cafeteria"
- Último recurso (se realmente não der pra inferir nicho): "Mentoria de tráfego pago pra criadores de conteúdo", "Curso de skincare pra mulheres 40+", "Consultoria de cardápio pra donos de cafeteria"

Se o aluno não especificou público, assumir um plausível brasileiro com base no produto/nicho e avisar antes de gerar as ideias:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Geração das 10 ideias ASMR/Sensação

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de ASMR/Sensação do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere 10 ideias ASMR/Sensação numeradas de 1 a 10, separadas por `---`.

#### REGRA CRÍTICA. Todas as 10 ideias em super zoom + textura ASMR + identificação do nicho

**TODAS as 10 ideias** precisam ter super zoom e textura ASMR rica. NÃO use cenas de "pessoa caminhando" ou "pessoa sentada" sem detalhe sensorial em super zoom. Sempre há um objeto, superfície ou gesto em close extremo.

**Distribuição obrigatória:**
- Cerca de 7 ideias **macro/close extremo** em objetos e detalhes inanimados do nicho (frascos, papéis, equipamentos, ferramentas, texturas).
- Cerca de 3 ideias com **detalhe corpóreo em super zoom** que comunica o nicho (mão pousada em algo do nicho, pose corporal característica em close, gesto sensorial específico).

#### Identificação visual do nicho é OBRIGATÓRIA

A imagem em super zoom precisa comunicar o nicho **em 1 segundo**, mesmo no close extremo. Se o close pode ser confundido com outro nicho, ajuste o enquadramento pra incluir um elemento icônico do nicho:

- Yoga: pose corporal específica reconhecível (árvore, lótus, downdog), tapete texturizado, manga ou tecido de yoga
- Cannabis medicinal: frasco âmbar de óleo CBD, certificado profissional, embalagem premium farmacêutica
- Direito empresarial: contrato premium, caneta tinteiro, lombada de couro, código CLT
- Skincare: textura de creme, gota de sérum, frasco premium, dedo na pele
- Investimentos: assinatura de contrato, notificação de PIX, gráfico em alta, escritura

#### Regras da imagem (todas as cenas)

**Super zoom ASMR extremo:**
- O detalhe sensorial ocupa **70 a 80% da composição**.
- Microreflexos, microtextura, gotas, fibras, vapor, brilho, sempre presentes.
- Atmosfera de "vídeo de ASMR pausado num frame", congelada no tempo.
- Microssombras da luz lateral suave.
- Profundidade rasa de campo.

**Estética:**
- UGC autêntico brasileiro estilo TikTok/Instagram (não cinemático nem editorial).
- Foto de iPhone amador macro.
- Luz natural quente lateral.
- Fundo desfocado, ambiente brasileiro classe média bem-cuidado.

**Compliance Facebook Ads:**
- Sem pernas de fora, decote, roupa curta, partes do corpo expostas, poses sensualizadas.
- Sem violência, sangue, ferida, lesão.
- Roupas SEMPRE cobertas (manga longa, calça comprida).
- Nichos sensíveis (cannabis medicinal): estética estritamente medicinal e farmacêutica premium, SEM folha verde da planta, SEM associação a uso recreativo.

#### Regra crítica do texto principal (faixas brancas)

A frase combina **3 camadas em 3 linhas**:
1. **SENSAÇÃO**: o gesto sensorial, a vivência física prazerosa.
2. **CATEGORIA DO PRODUTO**: deixa claro qual o nicho (yoga, cannabis medicinal, advocacia trabalhista, skincare).
3. **INSINUAÇÃO DA PROMESSA**: o resultado concreto que o produto entrega.

**Regra de curiosidade (igual ao POV):** a frase NUNCA entrega o método (o como). Mostra a sensação, a categoria e o resultado insinuado. O método fica reservado pro CTA.

**ERRADO** (entrega o método):
- "Faça 15 minutos por dia de yoga em casa e relaxe o corpo" (já contou o método: 15 min em casa)

**CERTO** (insinua sem entregar):
- "Equilibrar em pose árvore por 1 minuto e sentir o corpo finalmente se acalmar." (mostra a sensação, o nicho e o resultado)

#### Regra crítica do CTA (faixas coloridas temáticas)

**Estrutura do CTA:**
- **FAIXA 1**: promessa concreta direta do produto (o que a pessoa vai aprender ou conquistar).
- **FAIXA 2**: 👉 + chamada pro link.

**Objetividade do CTA:**
- "Aprenda yoga em 15min/dia 👉 Clique no link"
- "Vire consultor canábico em 90 dias 👉 Te ensino tudo no link"
- "Atenda empresas e fature R$ 15 mil/mês 👉 Te mostro como no link"

**NÃO use:**
- "Comente CONTRATO", "Comenta X que te mando o link", "Marca uma amiga" (modas que não foram pedidas).
- CTAs vagos demais ("Quer saber?").
- Travessão.

**Verbos da chamada:** "Clique no link", "Te mostro no link", "Te ensino no link", "Te conto tudo no link", "Link na bio".

#### Formato da listagem

Mostre só **Cena**, **Texto** e **CTA** em linguagem corrida pra facilitar a leitura. NÃO inclua as faixas separadas na listagem. As faixas só aparecem no prompt final quando o aluno escolher um número.

```
Aqui estão 10 ideias de ASMR/Sensação pro seu nicho.

---

**1.** (Super zoom, [descrição rápida do detalhe])
**Cena:** [descrição visual do detalhe sensorial super zoom com identificação clara do nicho]
**Texto:** [frase principal, as 3 camadas em linguagem corrida]
**CTA:** [promessa concreta] 👉 [chamada pro link]

---

**2.** (Super zoom, [descrição rápida do detalhe])
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

Frase de impacto conectada à promessa do produto. Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem pergunta no título
- Sem promessa vaga (incluir dado, prazo ou situação concreta)
- Sem "não é X. É Y."
- Produto não aparece no lead
- Linguagem que a pessoa usaria com uma amiga

#### B) Legenda pro Instagram

2 a 3 linhas em primeira pessoa, tom de creator. Gera curiosidade sem entregar o método. Termina com "Te conto tudo no link 👇" ou similar. Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

````
Cria pra mim uma arte de anúncio pra Instagram no formato ASMR/SENSAÇÃO UGC ESTILO TIKTOK/INSTAGRAM. Foto SUPER MACRO ULTRA ZOOM de iPhone, com FOCO ULTRA-DETALHADO num gesto sensorial. A imagem tem que parecer um VÍDEO DE ASMR PAUSADO num frame de máxima textura. Detalhes microscópicos visíveis, textura tátil intensa, microreflexos de luz.

ESTRUTURA OBRIGATÓRIA DA ARTE, 2 BLOCOS DE TEXTO SEPARADOS (CRÍTICO):
A arte tem DOIS BLOCOS DE TEXTO OBRIGATORIAMENTE PRESENTES:
1. TEXTO PRINCIPAL (faixas brancas) no MEIO/INFERIOR da arte
2. CTA (faixas [COR DO NICHO]) NA BASE da arte, ABAIXO do texto principal, SEMPRE PRESENTE
Os dois blocos são EMPILHADOS VERTICALMENTE com um GAP MAIOR entre eles (uns 30-40 pixels de respiro) deixando claro que são dois grupos visuais separados. NUNCA esqueça do CTA. Se houver apenas um bloco de texto, a arte está errada e precisa ser refeita.

COMPOSIÇÃO OBRIGATÓRIA DA FOTO (SUPER ZOOM ASMR COM IDENTIFICAÇÃO CLARA DO NICHO, ESPAÇO NEGATIVO NO TERÇO INFERIOR):

O enquadramento é um SUPER ZOOM EXTREMO num detalhe sensorial que COMUNICA O NICHO IMEDIATAMENTE. O detalhe principal OCUPA 70 a 80% DA COMPOSIÇÃO. O elemento tem que ser RECONHECÍVEL EM 1 SEGUNDO como pertencente ao nicho [NICHO], mesmo em close extremo.

O ENQUADRAMENTO DEIXA ESPAÇO NEGATIVO no terço CENTRAL-INFERIOR e na BASE da arte (fundo desfocado neutro) pra acomodar os DOIS BLOCOS de texto. O detalhe sensorial fica no terço SUPERIOR ou ALTO da arte.

CRÍTICO: O TEXTO PRINCIPAL VAI NO TERÇO CENTRAL-INFERIOR, O CTA VAI NA BASE. O detalhe sensorial SEMPRE LIVRE, sem texto cobrindo.

REGRA DE COMPLIANCE / FACEBOOK ADS:
Sem pernas de fora, decote, roupa curta, partes do corpo expostas, ou poses sensualizadas. Roupa SEMPRE fechada e coberta. Sem violência. [REGRAS ESPECÍFICAS DO NICHO QUANDO APLICÁVEL, ex: cannabis medicinal: SEM folha verde, estética estritamente medicinal/farmacêutica].

GATILHOS DE ULTRA-REALISMO ASMR/MACRO MICROSCÓPICO (em inglês pro gerador de imagem):
- "extreme super macro iPhone photo, ASMR frame quality"
- "microscopic detail of [ELEMENTO ESPECÍFICO DO NICHO]"
- "raw unedited macro smartphone photography"
- "ultra shallow depth of field, focus on [DETALHE PRINCIPAL]"
- "real Brazilian [HOMEM/MULHER + IDADE] with naturally cared appearance"
- "natural texture visible at microscopic level"
- "intimate sensory moment, ASMR aesthetic frozen in time"
- "soft warm natural daylight creating micro-shadows"
- "smartphone camera macro lens quality"
- "non-American context, Brazilian aesthetic"
- [GATILHOS ESPECÍFICOS DO NICHO]

CONTEXTO BRASILEIRO BEM-CUIDADO (totalmente desfocado, mal aparece):
[DESCRIÇÃO DO AMBIENTE BRASILEIRO CLASSE MÉDIA BEM-CUIDADO DESFOCADO QUE FAZ SENTIDO PRO NICHO]. Atmosfera serena, premium. Luz natural quente lateral criando microssombras delicadas.

A IMAGEM (SUPER MACRO ULTRA ZOOM COM IDENTIFICAÇÃO DO NICHO):
[DESCRIÇÃO ESPECÍFICA DO DETALHE SENSORIAL EM SUPER ZOOM com:
- O elemento icônico do nicho em primeiro plano
- Identificação visual inequívoca do nicho
- Detalhes microscópicos específicos (textura, microreflexos, gotas, fibras, etc)
- Mão/dedos/parte corpórea aparecendo parcialmente quando relevante]

Detalhes microscópicos OBRIGATÓRIOS:
- [Detalhe 1, microtextura específica]
- [Detalhe 2, microreflexo de luz]
- [Detalhe 3, sensação tátil]
- Microssombras criadas pela luz lateral
- Tom geral [TONALIDADE QUENTE/NEUTRA], atmosfera de [SENSAÇÃO DO NICHO]

A composição transmite: [SENSAÇÃO CONQUISTADA DO NICHO], momento sensorial congelado no tempo. Como se o tempo tivesse parado naquele exato segundo.

ESTILO EXATO DO TEXTO PRINCIPAL (BLOCO 1, FAIXAS BRANCAS QUEBRADAS, FONTE BEM GRANDE):

NO TERÇO CENTRAL-INFERIOR DA FOTO (NÃO na base, deixando espaço pro CTA embaixo), o texto principal aparece em ESTILO BLOCOS QUEBRADOS:

- Texto DIVIDIDO EM 3 LINHAS SEPARADAS, cada uma com FAIXA BRANCA DE FUNDO INDIVIDUAL.
- Cada FAIXA é um RETÂNGULO BRANCO SÓLIDO ESTREITO, altura JUSTA pro texto.
- Cada FAIXA com LARGURA PROPORCIONAL ao texto da linha. Larguras DIFERENTES entre si.
- As 3 FAIXAS EMPILHADAS COM GAP PEQUENO (4 a 8 pixels) entre elas.
- ALINHADAS À ESQUERDA, margem esquerda de uns 5% da borda.
- Texto em PRETO PURO #000000.
- Fonte SANS-SERIF EXTRA-BOLD/BLACK (Helvetica Black, Inter Black, Arial Black).
- TAMANHO: 50% MAIOR QUE O CTA. Se CTA é 10, principal é 15. Cada faixa ocupa 70-85% da largura.

Texto principal distribuído nas 3 linhas (SENSAÇÃO + CATEGORIA DO PRODUTO + INSINUAÇÃO DA PROMESSA, REGRA DE CURIOSIDADE: NÃO ENTREGA O MÉTODO):

FAIXA 1: "[LINHA 1]"
FAIXA 2: "[LINHA 2]"
FAIXA 3: "[LINHA 3]"

BLOCO 2, CTA SEMPRE PRESENTE (FAIXAS [COR DO NICHO], FONTE MENOR):

NA BASE DA FOTO (no rodapé, abaixo do texto principal com gap de 30-40 pixels entre eles), o CTA aparece OBRIGATORIAMENTE com FUNDO [COR DO NICHO] e TAMANHO DE FONTE 33% MENOR que o texto principal.

ESPECIFICAÇÕES DO CTA:
- Texto DIVIDIDO EM 2 LINHAS SEPARADAS, cada uma com FAIXA [COR DO NICHO] SÓLIDA INDIVIDUAL.
- Cada FAIXA com altura JUSTA pro texto.
- Larguras DIFERENTES entre si, proporcionais ao texto.
- As 2 FAIXAS EMPILHADAS COM GAP PEQUENO (4 a 8 pixels).
- ALINHADAS À ESQUERDA, MESMA MARGEM ESQUERDA do texto principal.
- Texto em PRETO PURO #000000.
- Fonte SANS-SERIF EXTRA-BOLD/BLACK (MESMA do texto principal).
- TAMANHO ~33% MENOR QUE O TEXTO PRINCIPAL.

Texto do CTA distribuído nas 2 linhas (PROMESSA CONCRETA + AÇÃO DIRETA):

FAIXA 1: "[PROMESSA CONCRETA DO PRODUTO]"
FAIXA 2: "👉 Clique no link"

CRÍTICO: O CTA É OBRIGATÓRIO. A arte tem QUE TER os dois blocos: texto principal (faixas brancas) E CTA (faixas [COR DO NICHO]). Se faltar o CTA, a arte está incompleta.

ESTÉTICA GERAL:
- UGC autêntico brasileiro estilo TikTok/Instagram.
- IMAGEM SUPER MACRO ULTRA ZOOM com IDENTIFICAÇÃO IMEDIATA DO NICHO (reconhecível em 1 segundo).
- TEXTO PRINCIPAL no terço CENTRAL-INFERIOR em FAIXAS BRANCAS QUEBRADAS, FONTE BEM GRANDE.
- CTA NA BASE em FAIXAS [COR DO NICHO] no MESMO PADRÃO VISUAL, FONTE 33% MENOR. SEMPRE PRESENTE.
- CTA com PROMESSA CONCRETA + CHAMADA DIRETA pra clicar no link.
- Compliance Facebook Ads.

PROIBIDO usar travessão. Use vírgula ou ponto final.

POSICIONAMENTO: margem mínima de 8 a 10% entre CTA e borda inferior.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Composition must be optimized for feed posts and carousels. Shorter vertical framing. Exact size reference: 1080x1350.
````

**Regra de cor do CTA por nicho** (substituir `[COR DO NICHO]`):
- Yoga/bem-estar/meditação: VERDE-MUSGO ESCURO
- Cannabis medicinal: VERDE-ESCURO MUSGO
- Direito/advocacia: AZUL-MARINHO PROFUNDO
- Skincare/lifestyle/geral: LARANJA VIVO
- Maternidade/beleza feminina/cestas: ROSA ESCURO ou TERRACOTA
- Finanças/investimentos/previdência: VERDE-ESCURO ou DOURADO QUEIMADO
- Concurso público/educação: AZUL-MARINHO ou AMARELO MOSTARDA
- Pet/animais: VERDE-MUSGO
- Cafeteria/gastronomia: MARROM CARAMELO
- Alimentação saudável/meal prep/nutrição: VERDE-OLIVA ou TERRACOTA
- Tráfego pago/IA/digital: AZUL ELÉTRICO ou ROXO
- Fitness/saúde/emagrecimento: VERDE-LIMÃO ESCURO ou VERMELHO TIJOLO

A cor do CTA puxa a paleta do nicho. Texto SEMPRE em preto puro sobre o fundo colorido.

#### D) Prompt pro ChatGPT (formato Stories)

Esse é fixo. Não precisa preencher placeholders.

````
Agora cria a exata mesma arte, mesmas cores, mesmo texto, mesmo visual, mesmos elementos, só diagramada pro formato Stories.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

### 4. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) no título e na legenda. Corrigir direto. Nunca mostrar versão bruta.

O texto principal (faixas brancas) e o texto do CTA NÃO passam pela revisora (são conteúdo da arte com tom específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, e o texto principal nunca entrega o método.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo ASMR/Sensação:

📌 IDEIA ESCOLHIDA (nº {numero_ideia} das 10)
[descrição da cena escolhida]

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
3. Voltar e escolher outra ideia (das 10)
```

Se escolher 2, perguntar o que ajustar (título, legenda, texto principal, descrição visual ou CTA) e refazer apenas a parte indicada.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-asmr-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-asmr-{numero}.md`

Conteúdo do arquivo:

```markdown
# ASMR / Sensação nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**Cena:** [descrição da cena escolhida]
**Texto:** [frase principal]
**CTA:** [promessa concreta] 👉 [chamada pro link]

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

Liste aqui todas as 10 ideias ASMR/Sensação geradas nesta sessão, pra o aluno poder usar qualquer uma depois sem precisar rodar a sub-skill de novo.
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-asmr-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-asmr-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo ASMR / Sensação salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-asmr-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro ASMR/Sensação com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo ASMR / Sensação gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-asmr-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-asmr-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro ASMR/Sensação com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-asmr-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-asmr-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-asmr-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-asmr-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-asmr-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda.
- O texto principal e o texto do CTA seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- **Regra de curiosidade**: o texto principal NUNCA entrega o método. Mostra a sensação, a categoria e o resultado insinuado. O CTA promete revelar o como.
- **Distribuição obrigatória das 10 ideias**: cerca de 7 de macro/close extremo em objetos inanimados, cerca de 3 com detalhe corpóreo em super zoom.

### Sobre a imagem (todas as 10 ideias)

- **Super zoom ASMR extremo**: o detalhe ocupa 70 a 80% da composição.
- **Textura microscópica obrigatória**: microreflexos, fibras, gotas, vapor, brilho.
- **Identificação visual do nicho em 1 segundo**: o close precisa comunicar o nicho mesmo em extremo, sem deixar dúvida.
- **"Frame de ASMR pausado"**: momento congelado de máxima textura sensorial.
- **Estética UGC brasileira autêntica** (não cinemática editorial).
- **Luz natural quente lateral** criando microssombras delicadas.

### Sobre o texto principal (faixas brancas, fonte bem grande)

- 3 linhas, cada uma com faixa branca individual.
- Faixas com altura justa, larguras proporcionais.
- Gap pequeno entre faixas (4 a 8 pixels).
- Alinhamento à esquerda, fonte sans-serif extra-bold.
- Tamanho 50% maior que o CTA.
- Posicionamento no terço CENTRAL-INFERIOR (deixando espaço pro CTA na base).
- **3 camadas obrigatórias**: SENSAÇÃO + CATEGORIA DO PRODUTO + INSINUAÇÃO DA PROMESSA.
- **Regra de curiosidade**: NÃO entrega o método. Mostra o resultado, esconde o como.

### Sobre o CTA (faixas coloridas, mesmo padrão visual do texto principal)

- Mesma estrutura, mesma fonte, mesmo alinhamento.
- Única diferença: cor de fundo + tamanho 33% menor que o texto principal.
- Cor adaptada ao nicho (tabela de cor do CTA por nicho).
- **SEMPRE PRESENTE**, nunca pode sumir.
- Gap de 30 a 40 pixels entre o texto principal e o CTA.
- **Estrutura obrigatória**: FAIXA 1 = promessa concreta direta, FAIXA 2 = 👉 + "Clique no link" (ou similar direto).
- **NUNCA** use "Comente X", "Marca uma amiga" e outras modas.

### Sobre o ambiente brasileiro de classe média

- Apartamento brasileiro bem-cuidado, organizado, com gosto.
- Não é cenário de revista, não é foto de banco de imagem.
- Equilíbrio entre autêntico e cuidado.

### Sobre NÃO usar

- Travessão (— ou –). Sempre vírgula ou ponto final.
- Logos de redes sociais.
- "Comente X", "Marca amiga", modas não pedidas.
- Fontes serifadas elegantes (é estilo TikTok cru, sans-serif pesada).
- Caixas brancas grandes envolvendo várias linhas (são faixas individuais).
- Texto cobrindo o detalhe sensorial.

### Compliance Facebook Ads (crítica)

- Sem pernas de fora, decote, roupa curta, partes do corpo expostas, poses sensualizadas.
- Sem violência, sangue, ferida, lesão.
- Roupas SEMPRE cobertas (manga longa, calça comprida).
- Nichos sensíveis (cannabis medicinal): estética estritamente medicinal e farmacêutica premium, SEM folha verde da planta, SEM associação a uso recreativo.

### Regras operacionais

- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
