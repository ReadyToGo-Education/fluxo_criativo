# UGC Rotina Real. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 5 (UGC Rotina Real). Cria um criativo que parece 100% um post orgânico de uma brasileira comum em momento de rotina cotidiana conectado ao nicho, com sobreposição de texto estilo TikTok/Instagram amador (caixinha preta sólida, fonte default, emojis). Gera 10 ideias de rotina visual com headline "O que eu fiz pra [resultado]", o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
A foto é indistinguível de uma selfie real de pessoa comum, então o leitor consome como conteúdo orgânico antes de perceber que é anúncio. A caixinha preta inclinada e os emojis são padrões visuais nativos que o usuário do Instagram e do TikTok já confia. A headline em primeira pessoa "O que eu fiz pra [resultado]" e a resposta contra-intuitiva curta geram curiosidade, e o CTA discreto promete revelar o resto no link.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço.
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho. Inclua a faixa etária, porque o público define a idade e o fenótipo da pessoa que aparece na foto e a rotina cotidiana retratada.
- **Quadro / promessa**: a transformação principal do `perfil.md`, pra alimentar as headlines "O que eu fiz pra [resultado]" com resultados específicos do produto.

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

### 2. Geração das 10 ideias UGC Rotina Real

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de UGC Rotina Real do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere 10 ideias UGC Rotina Real numa lista única numerada de 1 a 10.

#### Estrutura de cada ideia

Cada ideia tem três partes:

- **Rotina visual** (em parênteses): descrição concreta da cena do dia a dia conectada ao nicho. Exemplos: mulher passando creme em frente ao espelho do banheiro, mãe sentada no chão da sala com a filha lendo, dono de cafeteria passando café atrás do balcão, pai colocando filho pra dormir com livro na mão, professora preparando aula na mesa da cozinha.
- **Headline padrão "O que eu fiz pra [resultado]"**: a frase começa com "O que eu fiz pra" e termina com um resultado específico, conectado ao nicho. Tom de relato em primeira pessoa, pra amiga, sem cara publicitária.
- **Resposta contra-intuitiva curta**: 1 linha que dá o insight surpreendente. O hack, a virada, o que ninguém faz. Não pode ser óbvio nem genérico.

#### Regras das ideias

- **Rotina visual ESPECÍFICA do nicho**, não genérica. Skin care vira passando creme. Discipulado infantil vira fazendo devocional com filho. Cafeteria vira atrás do balcão fazendo café. Tráfego pago vira mexendo no notebook na mesa da cozinha.
- **Cenário brasileiro real**: apartamento de classe média, com bagunça normal de quem mora, sem cara de cenário de filme.
- **Headline em primeira pessoa**, tom casual de quem está contando pra amiga uma descoberta. Específica e benefício-direto.
- **Resposta contra-intuitiva**: tem que ter o "uau, eu não tinha pensado assim". Sem chavão, sem solução óbvia.
- **NÃO usar travessão** em nenhum texto. Use vírgula, ponto final ou parênteses.

#### Apresentação

Mostre as 10 ideias numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de UGC Rotina Real pro seu nicho.

---

**1.** (Rotina: [descrição visual concreta da cena do dia a dia conectada ao nicho])
**Headline:** O que eu fiz pra [resultado específico]
**Resposta:** [hack contra-intuitivo em 1 linha]

---

**2.** (Rotina: [descrição visual concreta da cena])
**Headline:** O que eu fiz pra [resultado específico]
**Resposta:** [hack contra-intuitivo em 1 linha]

---

Qual número você quer transformar em criativo?
```

#### Biblioteca de cenários brasileiros por tipo de nicho

Use a biblioteca abaixo como inspiração pra montar a rotina visual de cada ideia, sempre adaptando ao público específico do produto ativo.

**Skin care / beleza / anti-aging**
Rotinas: passar creme no espelho do banheiro, lavar o rosto na pia da cozinha, aplicar sérum sentada no sofá vendo TV, tirar maquiagem na cama, passar protetor antes de sair, organizar produtos na pia.

**Maternidade / discipulado / educação infantil**
Rotinas: sentar no chão da sala com filho fazendo atividade, preparar lanchinho na cozinha, ler na cama antes de dormir, brincar no tapete, conduzir devocional no sofá.

**Cafeteria / negócio próprio / empreendedorismo**
Rotinas: atrás do balcão fazendo café, anotando pedido na bancada, organizando cardápio, abrindo a loja de manhã, contando o caixa no fim do dia.

**Tráfego pago / IA / digital**
Rotinas: notebook na mesa da cozinha, fazendo ligação no celular na sala, mexendo no Meta Ads em casa, planejando no caderno com café.

**Relacionamento / esquecer o ex / autoconhecimento**
Rotinas: deitada na cama olhando teto, na varanda olhando o nada, escrevendo no caderno na mesa, vendo Stories no sofá, fazendo skincare antes de dormir.

**Fitness / emagrecimento / saúde**
Rotinas: cozinhando refeição saudável na cozinha, separando marmita, sentada na cozinha tomando café, andando no parque do bairro, em casa de roupa de academia preparando smoothie.

**Pets / cachorro / saúde animal**
Rotinas: dando banho no cachorro na varanda, escovando na sala, dando comida na cozinha, brincando no tapete, na cama com o pet ao lado.

**Finanças pessoais / investimentos / previdência**
Rotinas: anotando contas na mesa da cozinha, mexendo no app do banco no sofá, organizando documentos na escrivaninha, tomando café com agenda aberta.

**Alimentação saudável / meal prep / nutrição**
Rotinas: montando marmita na bancada da cozinha, organizando a geladeira com potes identificados, cozinhando legumes no fogão, pesando comida na balança de cozinha, arrumando a lancheira antes do trabalho.

**Hobbies / artesanato / bonsai / costura**
Rotinas: trabalhando o hobby na mesa da sala, organizando materiais na bancada da cozinha, fazendo na varanda com luz natural, mostrando o trabalho com a câmera frontal.

### 3. Escolha e geração do criativo

Após o aluno escolher um número de 1 a 10, anuncie. Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

Gere quatro coisas a partir da ideia escolhida:

#### A) Título do anúncio

Repete o headline da ideia escolhida ("O que eu fiz pra [resultado]"). Frase de impacto conectada à promessa do produto, Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem pergunta no título
- Sem promessa vaga (incluir dado, prazo ou situação concreta)
- Sem "não é X. É Y."
- Produto não aparece no lead
- Linguagem que a pessoa usaria com uma amiga

#### B) Legenda pro Instagram

2 a 3 linhas em primeira pessoa, tom de creator amador brasileira. Gera curiosidade sem entregar tudo. Termina com "Link na bio te conto tudo 👇" ou similar. Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

````
Cria pra mim uma arte de anúncio pra Instagram no formato UGC ULTRA REALISTA. A imagem tem que parecer 100% uma foto TIRADA POR UMA PESSOA COMUM no celular, em casa, sem produção nenhuma. NÃO pode parecer foto profissional, NÃO pode parecer fotografia editorial, NÃO pode parecer foto gerada por IA. Tem que ser indistinguível de uma foto real de iPhone tirada por uma brasileira normal.

GATILHOS DE ULTRA-REALISMO OBRIGATÓRIOS (em inglês pro gerador de imagem):
- "amateur iPhone photo, casual snapshot"
- "raw unedited smartphone photography"
- "candid moment at home"
- "real Brazilian person, no model, no makeup professional"
- "imperfect framing, slightly off-center composition"
- "natural skin texture with visible pores"
- "natural daylight or warm home lamp, no studio lighting"
- "authentic Brazilian middle-class home interior"
- "smartphone camera quality, slight motion blur acceptable"
- "non-American interior, Brazilian context"

CONTEXTO BRASILEIRO REAL OBRIGATÓRIO:
[DESCRIÇÃO ESPECÍFICA DO CENÁRIO BRASILEIRO baseado no nicho: cozinha americana de apartamento brasileiro com bancada de granito, sala de estar com sofá comum marrom/cinza e tapete simples, quarto com cama box e abajur de mesinha, banheiro pequeno com pia comum, varanda de apartamento com churrasqueira/estendal. SEMPRE incluir elementos de bagunça normal de casa real: brinquedos espalhados se tem criança, pano de prato pendurado na cozinha, controle remoto na mesa, copo de água, almofadas amassadas. Parede branca padrão construtora.]

A PESSOA:
[DESCRIÇÃO DA PESSOA brasileira real do público do nicho: idade específica, fenótipo brasileiro autêntico (mistura real de pardos/brancos/negros), cabelo natural sem produção, sem maquiagem profissional, pele real com poros e textura. Roupa casual brasileira (camiseta básica, regata, calça legging, moletom, pijama). Expressão natural de quem foi pego em momento real, não pose de modelo.]

A ROTINA:
[DESCRIÇÃO ESPECÍFICA DA AÇÃO da rotina, conectada ao nicho: o que a pessoa tá fazendo concretamente, com gestos naturais do dia a dia. Postura relaxada de quem mora naquela casa.]

A luz é natural (janela ou abajur comum), com sombras reais e ângulo levemente torto, como se a pessoa tivesse encostado o celular em alguma coisa pra gravar.

SOBREPOSIÇÃO DE TEXTO ESTILO TIKTOK/INSTAGRAM AMADOR:

NO TERÇO SUPERIOR DA FOTO, uma caixinha de legenda preta sólida (estilo padrão da legenda do TikTok), retangular, com cantos levemente arredondados, levemente inclinada uns 3 a 5 graus pra parecer jogada por cima. Texto em branco, sans-serif comum (fonte default do TikTok ou Instagram Stories, tipo Helvetica ou similar), peso médio: "[HEADLINE]"

NO MEIO DA FOTO, mais pra baixo do headline, outra caixinha de legenda preta sólida menor, com o mesmo estilo, levemente inclinada no sentido oposto, com um emoji [EMOJI COERENTE COM O TOM: 😱 / 🤯 / 🙏 / ✨ / 👀 / 💡] no início. Texto em branco: "[EMOJI] [RESPOSTA]"

NA BASE DA FOTO, um CTA simples e discreto estilo creator amador (sem botão, sem caixa, só texto com emoji): "👇 te conto tudo no link da bio"

REGRA DE CONTRASTE DO CTA (obrigatória): o CTA precisa ter contraste forte com a cor de fundo da região onde foi posicionado, garantindo legibilidade máxima.
- Se a base da imagem está escura: texto em amarelo vivo, branco puro ou laranja vivo.
- Se a base está clara: texto em preto, vermelho ou azul-marinho.
- Se está em tom neutro: branco puro ou preto puro com fundo semi-transparente fino atrás.

ESTÉTICA GERAL:
- Visual de UGC autêntico brasileiro, indistinguível de post real de pessoa comum.
- Pode ter pequenas imperfeições visuais: leve grão de smartphone, foco não perfeito, enquadramento amador.
- NÃO pode parecer foto profissional, NÃO pode ter estética editorial, NÃO pode parecer banner publicitário, NÃO pode ter aquela cara de "foto perfeita de IA".
- Tem que parecer post real de pessoa brasileira gravando um momento de rotina pra contar pras amigas.

PROIBIDO usar travessão (nem o "—" nem o "–") em nenhum texto da arte. Use vírgula ou ponto final no lugar.

POSICIONAMENTO: TODOS OS ELEMENTOS (caixinhas de texto, CTA) DEVEM SUBIR um pouco do rodapé. Deixa margem entre o CTA e a borda inferior da arte (mínimo 8 a 10% da altura). Mesmo respeito de margem no topo.

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

A headline e a resposta contra-intuitiva da arte NÃO passam pela revisora (são conteúdo da arte com tom de creator amador), mas devem respeitar Light Copy: sem travessão, sem exclamação, e a resposta nunca pode ser um chavão óbvio.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo UGC Rotina Real:

📌 IDEIA ESCOLHIDA (nº {numero_ideia} das 10)
Rotina: [rotina visual]
Headline: [headline]
Resposta: [resposta contra-intuitiva]

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

Se escolher 2, perguntar o que ajustar (título, legenda, headline, resposta, rotina visual ou cenário) e refazer apenas a parte indicada.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-ugc-rotina-real-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-ugc-rotina-real-{numero}.md`

Conteúdo do arquivo:

```markdown
# UGC Rotina Real nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**Rotina:** [rotina visual]
**Headline:** [headline]
**Resposta:** [resposta contra-intuitiva]

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

[Listar todas as 10 ideias UGC Rotina Real geradas nesta sessão, para o aluno usar depois sem precisar rodar a sub-skill de novo.]
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

3. Grave o Prompt Feed num arquivo `.txt` na pasta de criativos. O conteúdo é o Prompt Feed apresentado ao aluno, sem alterações.

4. Anuncie e rode o script no formato Feed (4:5):

```
🔍 Próximo passo: gerar a imagem do Feed via API. Tempo estimado: 2 a 3 minutos.
```

Use o comando Python correto da sessão (`python3` ou `py -3`), conforme a seção Execução de Scripts Python do CLAUDE.md.

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-ugc-rotina-real-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-ugc-rotina-real-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo UGC Rotina Real salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-ugc-rotina-real-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu de 3 opções:

```
Quer fazer mais alguma coisa?
1. Gerar outro UGC Rotina Real com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

Se o aluno escolher 3, voltar ao orquestrador `/criativo-estatico`.

**No modo API:**

```
✅ Concluído: criativo UGC Rotina Real gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-ugc-rotina-real-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-ugc-rotina-real-{numero}.md
```

Depois, ofereça o menu de 4 opções, com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro UGC Rotina Real com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```

#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-ugc-rotina-real-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-ugc-rotina-real-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-ugc-rotina-real-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-ugc-rotina-real-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-ugc-rotina-real-{numero}-stories.png
```

e) Reapresente o mesmo menu de 4 opções, agora com a opção 1 marcada como "Gerar novamente o Stories (refazer a versão atual)".

Se o aluno escolher 4 (ou 3 no modo ChatGPT), voltar ao orquestrador `/criativo-estatico`.

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- **Exceção documentada — emoji no CTA da legenda:** o emoji 👇 no CTA da legenda ("Link na bio te conto tudo 👇" ou similar) é permitido porque integra o padrão visual de creator amador brasileiro e faz parte da autenticidade do formato UGC. Essa exceção NÃO vale para o título do anúncio, que segue Light Copy sem emojis.
- Produto NÃO aparece no lead do título nem da legenda.
- A headline e a resposta da arte seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- **Ultra-realismo brasileiro obrigatório**: a foto tem que ser indistinguível de selfie ou snapshot real de brasileira comum. Cabelo natural, pele real, casa com bagunça, fenótipo brasileiro autêntico, sem cara de modelo americano de banco de imagem, sem cara de IA.
- **Headline padrão "O que eu fiz pra [resultado]"**: formato fixo, com resultado específico e benefício direto.
- **Resposta contra-intuitiva**: 1 linha, com insight surpreendente. Sem chavão, sem solução óbvia.
- **Rotina visual específica do nicho**: a cena escolhida casa especificamente com o nicho. Usar a biblioteca de cenários brasileiros como inspiração, mas adaptar ao público específico.
- **Cenário brasileiro real**: apartamento de classe média com bagunça normal de quem mora, sem cara de cenário de filme.
- **Sobreposição de texto estilo TikTok/Instagram amador**: caixinha preta sólida, fonte default sans-serif, leve inclinação, emojis. Sem tipografia editorial, sem design publicitário.
- **CTA com regra de contraste contextual**: a cor do CTA adapta ao fundo da imagem pra garantir legibilidade. Estilo "👇 te conto tudo no link da bio", sem botão.
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês (que são gatilhos eficazes pro gerador de imagem).
- Margens generosas pra não cortar no Instagram (mínimo 8 a 10% entre o CTA e a borda inferior).
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível brasileiro com base no produto e avisar antes de gerar as 10 ideias. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
