# POV (Ponto de Vista). Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 6 (POV). Coloca o público vivendo uma situação reconhecível do nicho, antes (dor), depois (resultado) ou durante (processo). Gera 10 ideias de POV, o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
A pessoa se reconhece na situação antes de perceber que é anúncio. O texto em faixas brancas estilo TikTok parece conteúdo orgânico, não peça publicitária. A regra de curiosidade mantém o método escondido: o POV mostra a virada conquistada, o CTA promete revelar o como, e essa lacuna é o que gera o clique.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço.
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho. Inclua a faixa etária, porque o POV decide se mantém ou tira a sigla "POV:" no texto da arte conforme a idade do público.
- **Quadro / promessa**: a transformação principal do `perfil.md`, pra alimentar a regra de curiosidade (o CTA promete revelar o que entrega esse resultado).

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

### 2. Geração das 10 ideias POV

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de POV do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere 10 ideias POV. **Distribuição obrigatória: 7 ideias de DOR/SITUAÇÃO ANTES + 3 ideias de RESULTADO/SITUAÇÃO DEPOIS.** A maioria foca em identificação com a dor, algumas mostram o desejo conquistado pra ativar projeção positiva.

#### Tipos de POV que funcionam pra venda

1. **POV ANTES, dor reconhecida**: pessoa vivendo a situação ANTES de ter o produto. Identificação imediata.
2. **POV DEPOIS, resultado conquistado**: pessoa vivendo o resultado. Ativa desejo.
3. **POV PROCESSO, no meio da virada**: pessoa no momento da decisão ou aplicação do método.
4. **POV CONFUSO, perdido sem método**: pessoa tentando fazer sozinha e travando.
5. **POV MOMENTO ESPECÍFICO, vivência marcante**: instante singular reconhecível do nicho.
6. **POV BASTIDOR, por trás dos panos**: o que o público não vê. Cria intimidade.
7. **POV REVELAÇÃO, insight contra-intuitivo**: pessoa descobrindo algo que muda o jogo.
8. **POV TERCEIRA PESSOA, cliente ou aluno satisfeito**: olhando pra alguém que conquistou.
9. **POV FUTURO, projeção desejável**: pessoa daqui a X tempo se beneficiando do método.

#### Regras das ideias

- Frase começa com situação reconhecível, NÃO obrigatoriamente com a palavra "POV:" (a decisão de manter ou tirar é tomada no Passo 3).
- Frase em primeira ou segunda pessoa, vívida, com detalhes específicos.
- Cena descrita com elementos visuais inconfundíveis do nicho.
- Pessoa autenticamente cuidada (não modelo, não esculhambada).
- Ambiente brasileiro classe média organizado (não cenário, não bagunça).
- Sem travessão. Use vírgula, ponto final ou parênteses.

#### REGRA CRÍTICA DE CURIOSIDADE (o POV NUNCA entrega o método)

A frase do POV mostra A VITÓRIA, A SENSAÇÃO, A VIRADA CONQUISTADA, mas NUNCA entrega O COMO. O método, o segredo, a ordem, o produto específico ficam reservados pro CTA. Se a frase do POV já conta o "como", queima o clique.

**ERRADO** (entrega o método na frase):
- "Você descobre que protetor solar previne mais ruga que sérum de R$ 600" (já contou)
- "Você passa vitamina C de manhã e retinol à noite e a pele responde" (já contou)
- "Você usa 4 produtos só e a pele tá melhor" (já contou)

**CERTO** (insinua o resultado, gera curiosidade pro método):
- "Você descobre o que ninguém te conta sobre prevenir ruga depois dos 40"
- "Sua filha de 22 anos te pergunta qual o seu segredo e você só sorri"
- "Você acorda aos 46 sem inchaço e sabe exatamente o que mudou"
- "Sua amiga de 38 te pergunta o que mudou e você não conta tudo"

Estrutura mental pra cada frase: **mostra** o resultado conquistado e a virada, **esconde** o como, **tom** de vitória, satisfação ou descoberta com gancho de curiosidade implícito.

#### Apresentação

Mostre as 10 ideias numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de POV pro seu nicho.

---

**1.** (POV ANTES, dor reconhecida)
**Frase:** "[situação reconhecível em primeira ou segunda pessoa]"
**Cena:** [descrição visual da pessoa + ambiente do nicho]

---

**2.** (POV DEPOIS, resultado conquistado)
...

---

Qual número você quer transformar em criativo?
```

### 3. Escolha e geração do criativo

Após o aluno escolher um número de 1 a 10, anuncie. Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

#### Decisão sobre incluir "POV:" no texto

Pra a ideia escolhida, decida se a frase começa com "POV:" ou direto na situação:

- **Mantém "POV:"** se o público é digital-nativo, jovem-adulto, familiar com vocabulário de redes sociais (gestores de tráfego, criadores de conteúdo, infoprodutores).
- **Tira "POV:" e começa com letra maiúscula direto na situação** se o público é mais velho (40+), classe média tradicional, ou nicho onde "POV" pode não ser universal (skincare 40+, maternidade, finanças, esquecer o ex, dermatite canina, cestas).

Use a faixa etária do público extraída no Passo 0 pra decidir.

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

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.** O prompt já traz a tabela de cor do CTA por nicho e os exemplos de pareamento; mantenha tudo no texto colado no ChatGPT.

````
Cria pra mim uma arte de anúncio pra Instagram no formato POV UGC ESTILO TIKTOK/INSTAGRAM. Foto de iPhone tirada por uma brasileira cuidada de classe média, com FOCO PRINCIPAL NA PESSOA.

COMPOSIÇÃO OBRIGATÓRIA DA FOTO (FOCO NA PESSOA, ESPAÇO NEGATIVO NO TERÇO INFERIOR):

O ENQUADRAMENTO É FECHADO NA PESSOA. A pessoa OCUPA 60 a 70% DA COMPOSIÇÃO. O ambiente aparece SÓ COMO PANO DE FUNDO desfocado, reconhecível mas não dominante.

O ENQUADRAMENTO DEIXA ESPAÇO NEGATIVO NO TERÇO INFERIOR da arte (edredom, mesa, bancada, ou área desfocada limpa) pra acomodar o texto do POV nessa região baixa. A pessoa fica enquadrada com a CABEÇA POSICIONADA NO TERÇO SUPERIOR ou ALTO CENTRAL da arte, busto/ombros embaixo, e ABAIXO do peito tem ESPAÇO LIMPO onde o texto vai aparecer.

CRÍTICO: O TEXTO VAI NO TERÇO INFERIOR/CENTRAL DA ARTE, NÃO NO TOPO. O rosto da pessoa SEMPRE LIVRE, sem texto cobrindo.

REGRA DE COMPLIANCE / FACEBOOK ADS:
NÃO mostrar pernas de fora, roupa curta, decote, partes do corpo expostas, ou poses sensualizadas. Roupa SEMPRE fechada e coberta (camisola elegante de manga longa, robe fechado, blusa de manga longa, calça comprida). Postura natural e respeitosa.

GATILHOS DE UGC AUTÊNTICO BRASILEIRO COM FOCO NA PESSOA (em inglês pro gerador de imagem):
- "amateur iPhone close-up photo, person fills upper and middle frame"
- "tight composition with intentional negative space at LOWER third for text"
- "raw unedited smartphone photography"
- "background slightly out of focus, shallow depth of field"
- "real Brazilian person with naturally cared appearance, hydrated glowing skin"
- "no model, no makeup professional, but well-groomed"
- "fully covered modest clothing"
- "natural skin texture with visible pores and healthy glow"
- "elegant Brazilian middle-class home interior in background, blurred"
- "natural daylight, warm tones"
- "smartphone camera quality"
- "non-American interior, Brazilian context"

CONTEXTO BRASILEIRO BEM-CUIDADO (de fundo, levemente desfocado):
[DESCRIÇÃO DO AMBIENTE DO NICHO: cozinha, quarto, sala, home office, banheiro, etc, sempre brasileiro de classe média BEM-CUIDADO. Elementos visíveis mas em segundo plano. Tudo levemente desfocado dando profundidade.]

A PESSOA (enquadrada com espaço LIMPO ABAIXO DO PEITO, rosto livre, roupas COBERTAS):
[DESCRIÇÃO DA PESSOA brasileira real do público do nicho: idade, fenótipo brasileiro autêntico, cabelo natural penteado e cuidado, pele real mas HIDRATADA com brilho saudável, expressão coerente com a situação do POV, roupa elegante mas COBERTA. Postura natural.]

ENQUADRAMENTO: pessoa aparece do PEITO PRA CIMA, posicionada no terço SUPERIOR/CENTRAL da composição. ABAIXO DO PEITO tem ESPAÇO LIMPO (superfície desfocada relevante ao nicho) pra acomodar o texto.

ESTILO EXATO DO TEXTO POV (FAIXAS BRANCAS QUEBRADAS, TIKTOK/INSTAGRAM CRU, FONTE GRANDE):

NO TERÇO INFERIOR/CENTRAL DA FOTO, abaixo do peito da pessoa (sobre o espaço negativo desfocado), o texto aparece em ESTILO BLOCOS QUEBRADOS:

ESPECIFICAÇÕES TÉCNICAS DO TEXTO:
- Texto DIVIDIDO EM 2 OU 3 LINHAS SEPARADAS, cada uma com FAIXA BRANCA DE FUNDO INDIVIDUAL.
- Cada FAIXA é um RETÂNGULO BRANCO SÓLIDO ESTREITO, altura JUSTA pro texto (padding interno mínimo 6-10 pixels em cima e embaixo).
- Cada FAIXA com LARGURA PROPORCIONAL ao texto da linha específica (padding interno 12-16 pixels nas laterais). Larguras DIFERENTES entre si.
- As FAIXAS EMPILHADAS COM GAP PEQUENO (4 a 8 pixels) entre elas, mostrando a foto atrás nos gaps.
- ALINHADAS À ESQUERDA, margem esquerda de uns 5% da borda.
- Texto em PRETO PURO #000000.
- Fonte SANS-SERIF EXTRA-BOLD/BLACK (Helvetica Black, Inter Black, Arial Black).
- TAMANHO DO TEXTO POV: BEM GRANDE, aproximadamente 50% MAIOR QUE O TEXTO DO CTA. Se o CTA tem tamanho 10, o POV tem tamanho 15. Cria hierarquia visual clara: POV domina visualmente, CTA acompanha em escala menor. Cada faixa horizontal do POV ocupa aproximadamente 70-85% da largura da arte. Tamanho que prende o olho imediatamente.

INSTRUÇÕES CRÍTICAS DO TEXTO:
- NÃO criar um único retângulo branco grande envolvendo as linhas. SÃO FAIXAS SEPARADAS, uma por linha.
- NÃO usar fonte serifada elegante. É SANS-SERIF PESADA E CRUA, tipo TikTok.
- NÃO altura inflada. JUSTA PRO TEXTO, mas com TEXTO GRANDE.
- NÃO centralizar. ALINHAR À ESQUERDA.
- NÃO usar margem grande entre as faixas. GAP PEQUENO mostrando linha da foto atrás.
- NÃO usar fundo branco semitransparente. BRANCO SÓLIDO PURO #FFFFFF.
- NÃO adicionar sombras, gradientes ou bordas. RETÂNGULOS BRANCOS PLANOS PUROS.
- TEXTO TEM QUE SER BEM GRANDE, com presença forte.

Texto distribuído em linhas, cada uma na sua faixa branca individual:

[INSERIR TEXTO QUEBRADO EM 2 OU 3 LINHAS, sem aspas ao redor. A primeira linha começa com letra maiúscula. Decidir se mantém "POV:" ou começa direto na situação conforme regra do público do nicho.]

POSICIONAMENTO DO CTA (MESMO PADRÃO VISUAL DO POV, FAIXAS COLORIDAS POR LINHA, FONTE GRANDE):

NA BASE DA FOTO, abaixo do texto do POV, o CTA aparece no MESMO ESTILO VISUAL do texto POV (mesmas faixas individuais empilhadas, mesma fonte, mesmo alinhamento à esquerda), mas com FUNDO COLORIDO em vez de branco e TAMANHO DE FONTE MENOR QUE O POV (proporção 10/15, ou seja, ~33% menor que o POV).

ESPECIFICAÇÕES TÉCNICAS DO CTA (IDÊNTICAS AO POV, MUDA SÓ A COR DA FAIXA):
- Texto DIVIDIDO EM 2 LINHAS SEPARADAS, cada uma com FAIXA COLORIDA SÓLIDA INDIVIDUAL.
- Cada FAIXA com altura JUSTA pro texto (padding mínimo, MESMO DAS FAIXAS DO POV).
- Larguras DIFERENTES entre si, proporcionais ao texto. Cada faixa ocupa entre 50% e 75% da largura da arte.
- As 2 FAIXAS EMPILHADAS COM GAP PEQUENO (4 a 8 pixels).
- ALINHADAS À ESQUERDA, MESMA MARGEM ESQUERDA do POV.
- Texto em PRETO PURO #000000 (NÃO usar branco, NÃO usar duas cores).
- Fonte SANS-SERIF EXTRA-BOLD/BLACK (EXATAMENTE A MESMA do POV).
- TAMANHO DO CTA: aproximadamente 33% MENOR QUE O TEXTO DO POV. Se POV tem tamanho 15, CTA tem tamanho 10. Mantém presença visual forte mas em escala menor que o POV, criando hierarquia clara.

REGRA DE COR DO CTA POR NICHO:
- Default (skincare, lifestyle, geral): LARANJA VIVO
- Maternidade/beleza feminina/cestas: ROSA ESCURO ou TERRACOTA
- Finanças/investimentos/empreendedorismo: VERDE-ESCURO ou DOURADO QUEIMADO
- Concurso público/educação: AZUL-MARINHO ou AMARELO MOSTARDA
- Pet/animais: VERDE-MUSGO
- Cafeteria/gastronomia: MARROM CARAMELO
- Tráfego pago/IA/digital: AZUL ELÉTRICO ou ROXO
- Fitness/saúde/emagrecimento: VERDE-LIMÃO ESCURO ou VERMELHO TIJOLO
- Maternidade religiosa/discipulado: VINHO ou TERRACOTA QUENTE
- Esquecer o ex/relacionamento: VINHO SUAVE ou ROSA-NUDE ESCURO
- Alimentação saudável/meal prep/nutrição: VERDE-OLIVA ou LARANJA QUEIMADO
- Hobbies/artesanato: BEGE ESCURO ou MOSTARDA
- Bonsai/jardinagem: VERDE-MUSGO ESCURO

A cor do CTA puxa a paleta do nicho. Texto SEMPRE em preto puro. A cor da faixa do CTA deve ser DIFERENTE da cor da faixa do POV (que é branca).

Texto do CTA distribuído nas 2 linhas (REGRA CRÍTICA: o CTA PROMETE REVELAR o método/segredo/como que ficou escondido no POV):

FAIXA 1: "[FRASE QUE PROMETE REVELAR O QUE TÁ ESCONDIDO NO POV]"
FAIXA 2: "👉 [CHAMADA PRO LINK]"

EXEMPLOS DE PAREAMENTO POV + CTA:

POV: "Você descobre que tem uma coisa que faz mais diferença que sérum de R$ 600"
CTA FAIXA 1: "Eu te conto o que é."
CTA FAIXA 2: "👉 Link na bio"

POV: "Sua filha de 22 anos te pergunta qual é o seu segredo e você só sorri"
CTA FAIXA 1: "Quer saber meu segredo?"
CTA FAIXA 2: "👉 Te conto no link"

POV: "Você acorda aos 46 sem o inchaço do rosto e sabe exatamente o que mudou"
CTA FAIXA 1: "Eu te mostro o que mudou."
CTA FAIXA 2: "👉 Link na bio"

POV: "A dermato te entrega a receita e você nem sabe por onde começar"
CTA FAIXA 1: "A ordem certa existe."
CTA FAIXA 2: "👉 Te conto tudo no link"

PADRÃO DO CTA (verbos de promessa):
- Faixa 1 sempre PROMETE A REVELAÇÃO do que tá escondido no POV
- Verbos: contar, revelar, ensinar, mostrar, descobrir, entender
- Primeira pessoa: "Eu te conto", "Eu te mostro", "Eu te ensino"
- Ou pergunta direta: "Quer saber como?", "Quer aprender?", "Quer descobrir?"
- Faixa 2 sempre direciona pro link com emoji 👉

INSTRUÇÕES CRÍTICAS DO CTA:
- IDÊNTICO ao POV em estrutura, fonte, alinhamento e TAMANHO. ÚNICA diferença: cor de fundo das faixas (colorida em vez de branca).
- NÃO é faixa horizontal cobrindo toda a largura da arte. É FAIXA INDIVIDUAL POR LINHA, largura proporcional ao texto.
- NÃO duas cores no texto. TEXTO INTEIRO EM PRETO PURO.
- NÃO criar retângulo único cobrindo as 2 linhas. SÃO 2 FAIXAS SEPARADAS, mesmo padrão do POV.
- Emoji 👉 só na linha 2 (chamada de ação).
- TAMANHO DA FONTE MENOR QUE O POV (proporção 10/15, ou seja, ~33% menor).

ESTÉTICA GERAL:
- Visual UGC autêntico brasileiro estilo TikTok/Instagram.
- FOCO PRINCIPAL NA PESSOA (60-70% do enquadramento), ambiente como contexto desfocado.
- TEXTO POV NO TERÇO INFERIOR/CENTRAL em FAIXAS BRANCAS QUEBRADAS, FONTE BEM GRANDE.
- CTA ABAIXO DO POV em FAIXAS COLORIDAS no MESMO PADRÃO VISUAL, mas com FONTE ~33% MENOR QUE O POV (hierarquia visual).
- Composição limpa, pessoa autenticamente cuidada, ambiente classe média organizado.
- Roupas SEMPRE COBERTAS, sem sensualidade.
- NÃO esculhambado. Equilíbrio entre autêntico e cuidado.

PROIBIDO usar travessão em nenhum texto. Use vírgula ou ponto final no lugar.

POSICIONAMENTO: TODOS OS ELEMENTOS COM MARGEM GENEROSA, mínimo 8 a 10% entre CTA e borda inferior.

Fonte legível em celular.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Composition must be optimized for feed posts and carousels. Shorter vertical framing. Exact size reference: 1080x1350.
````

#### D) Prompt pro ChatGPT (formato Stories)

Esse é fixo. Não precisa preencher placeholders.

````
Agora cria a exata mesma arte, mesmas cores, mesmo texto, mesmo visual, mesmos elementos, só diagramada pro formato Stories.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

### 4. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) no título e na legenda. Corrigir direto. Nunca mostrar versão bruta.

A frase do POV e o texto do CTA NÃO passam pela revisora (são conteúdo da arte com tom específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, e a frase do POV nunca entrega o método.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo POV:

📌 POV ESCOLHIDO (nº {numero_pov} das 10)
[frase do POV]

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
3. Voltar e escolher outro POV (dos 10)
```

Se escolher 2, perguntar o que ajustar (título, legenda, frase do POV, descrição visual ou CTA) e refazer apenas a parte indicada.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-pov-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-pov-{numero}.md`

Conteúdo do arquivo:

```markdown
# POV nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## POV escolhido (nº {numero_pov} das 10)

[frase do POV]

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

[Listar todas as 10 ideias POV geradas nesta sessão, com número e frase, para o aluno usar depois sem precisar rodar a sub-skill de novo.]
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-pov-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-pov-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo POV salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-pov-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro POV com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo POV gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-pov-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-pov-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro POV com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-pov-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-pov-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-pov-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-pov-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-pov-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- **Exceção documentada: emoji no CTA da legenda.** O Manual da Copy proíbe emojis em geral, mas a legenda do POV termina com emoji (ex: "👇") no CTA porque integra o padrão visual de creator amador, que é o que confere autenticidade ao formato. Essa exceção vale SOMENTE para o CTA da legenda. O título do anúncio nunca usa emoji.
- Produto NÃO aparece no lead do título nem da legenda.
- A frase do POV e o texto do CTA seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- **Regra de curiosidade**: o POV NUNCA entrega o método. Mostra a vitória, esconde o como. O CTA promete revelar o que ficou escondido.
- **Distribuição obrigatória das 10 ideias**: 7 de dor/situação antes, 3 de resultado/situação depois.
- **Decisão "POV:"**: manter pra público digital-nativo jovem, tirar pra público 40+ ou tradicional (começa com letra maiúscula na situação).
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- Texto do POV em faixas brancas individuais por linha, fonte sans-serif extra-bold, preto puro, alinhado à esquerda, terço inferior/central. Rosto da pessoa sempre livre.
- CTA no mesmo padrão visual do POV, mudando só a cor da faixa (temática do nicho) e o tamanho da fonte (~33% menor). A cor da faixa do CTA deve ser diferente do branco do POV.
- Não usar na arte: logos de redes sociais, emojis dentro do texto do POV (emoji só no CTA, na linha 2), fontes serifadas elegantes, caixas brancas grandes envolvendo várias linhas (são faixas individuais), texto cobrindo o rosto da pessoa.
- Compliance Facebook Ads: sem pernas de fora, decote, roupa curta, poses sensualizadas, violência, sangue, ferida, lesão. Roupa sempre coberta.
- Ambiente brasileiro de classe média bem-cuidado e organizado, nem cenário de revista nem esculhambado.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
