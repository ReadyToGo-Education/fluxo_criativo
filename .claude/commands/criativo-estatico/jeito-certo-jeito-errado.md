# Jeito Certo × Jeito Errado. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 8 (Jeito Certo × Jeito Errado). Mostra um erro específico que a maioria do público comete vs o jeito correto contra-intuitivo, numa arte dividida ao meio com a mesma pessoa em duas cenas. Estética UGC ultra realista brasileira em split vertical, com cenário inconfundível do nicho. Gera 10 ideias de erro × acerto, o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
A comparação lado a lado é um padrão visual que o olho do usuário entende em meio segundo, sem precisar ler. O lado errado gera identificação imediata (a pessoa se reconhece no erro), o lado certo abre a curiosidade (ela quer saber o como). A estética UGC ultra realista faz a arte parecer post orgânico de pessoa comum, não peça publicitária, o que aumenta o tempo de atenção antes do leitor perceber que é anúncio.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço (ex: "automação com IA pra pequenos negócios").
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho.

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
- Se for de videomaker: "Mentoria de Videomaker pra quem cobra barato", "Curso de Edição de Vídeo pra freelancers", "Treinamento de Captação pra produtoras"
- Se for de tráfego: "Mentoria de Tráfego Pago pra criadores", "Curso de Anúncios no Meta pra agências", "Consultoria de Performance pra ecommerce"
- Se for de cafeteria: "Consultoria de Cardápio pra donos de cafeteria", "Treinamento de Barista pra equipes", "Curso de Como Abrir uma Cafeteria"
- Último recurso (se realmente não der pra inferir nicho a partir do slug, perfil.md ou idconsumidor.md): construa 3 exemplos fictícios do universo mais próximo que for possível inferir. Os exemplos dos nichos listados acima são apenas referência interna de formato para o assistente, nunca devem ser exibidos ao aluno quando há um nicho identificável. Exibir exemplos de nicho errado (ex: tráfego pago quando o produto é de culinária) quebra a credibilidade do fluxo. Em caso de dúvida genuína, pergunte antes: "Qual é o nicho do seu produto?" em vez de assumir um universo incorreto.

Se o aluno não especificou público, assumir um plausível brasileiro com base no produto/nicho e avisar antes de gerar as ideias:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Geração das 10 ideias

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de Jeito Errado × Jeito Certo do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere 10 ideias Jeito Errado × Jeito Certo numa lista única numerada de 1 a 10. Cada ideia tem três partes:

- **Indicação de funil em parênteses**: (Topo), (Meio) ou (Fundo)
- **Jeito errado**: ação ou crença ESPECÍFICA que a maioria do público comete. Não pode ser genérico.
- **Jeito certo**: o hack contra-intuitivo que muda o jogo. Profundo, específico, com vocabulário do nicho/método quando relevante. Nunca solução boba.

#### Regras das ideias

- **Variedade obrigatória de profundidade**: misture topo de funil (mais emocional, oportunidade, falas mais simples), meio (intermediário) e fundo (técnico e profundo). Algumas ideias podem ser mais "bobinhas" pra ressoar com gente que está começando, outras precisam ser técnicas e profundas pra ressoar com quem já está na manha.
- **Jeito errado ESPECÍFICO**: não pode ser "fazer tudo errado". Tem que ser um comportamento concreto, observável, identificável. Exemplo: "Cobrar por hora ou diária no orçamento de vídeo" (bom) vs "Cobrar errado" (ruim).
- **Jeito certo PROFUNDO**: não pode ser óbvio nem chavão. Tem que ser a virada de chave, o insight que ninguém te conta, o hack que muda o jogo. Se houver método ou framework do produto, use o vocabulário específico.
- **NÃO usar travessão** em nenhum texto. Use vírgula, ponto final ou parênteses.

#### Apresentação

Mostre as 10 ideias numeradas de 1 a 10:

```
Aqui estão 10 ideias de Jeito Errado × Jeito Certo pro seu nicho.

**1.** (Topo)
**Errado:** [ação ou crença específica que a maioria faz]
**Certo:** [hack contra-intuitivo profundo]

**2.** (Meio)
**Errado:** [ação ou crença específica que a maioria faz]
**Certo:** [hack contra-intuitivo profundo]

**3.** (Fundo)
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

Frase de impacto conectada ao jeito certo, em primeira pessoa ou afirmativa. Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem pergunta no título
- Sem promessa vaga (incluir dado, prazo ou situação concreta)
- Sem "não é X. É Y."
- Produto não aparece no lead
- Linguagem que a pessoa usaria com uma amiga

#### B) Legenda pro Instagram

2 a 3 linhas em primeira pessoa, tom de creator amador. Gera curiosidade sem entregar tudo. Termina com "Link na bio te conto tudo 👇" ou similar. Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

Os placeholders são:
- `[INSERIR ELEMENTOS INCONFUNDÍVEIS DO NICHO]`: 4 a 6 elementos visuais característicos do nicho, tirados da Biblioteca de elementos visuais por nicho no fim deste arquivo.
- `[DESCRIÇÃO DA PESSOA]`: brasileira real do público do nicho, com idade, fenótipo brasileiro autêntico, cabelo natural, sem produção, roupa casual brasileira. Mesma pessoa, mesma roupa, mesmo cenário, em momentos diferentes.
- `[DESCRIÇÃO VISUAL DO JEITO ERRADO]`: a pessoa fazendo o jeito errado, com expressão de cansaço, frustração ou erro.
- `[RESUMO CURTO DO JEITO ERRADO]`: a versão curta do erro, pra aparecer na arte.
- `[DESCRIÇÃO VISUAL DO JEITO CERTO]`: a MESMA pessoa, no MESMO cenário, aplicando o jeito certo, com expressão de domínio e satisfação.
- `[RESUMO CURTO DO JEITO CERTO]`: a versão curta do acerto, pra aparecer na arte.
- `[EMOJI]`: um entre 🤯 / 😱 / 💡 / ✨ / 👀.
- `[INSIGHT CURTO E DIRETO]`: a frase central que explica por que o jeito certo funciona.

````
Cria pra mim uma arte de anúncio pra Instagram no formato UGC ULTRA REALISTA, dividido em split de duas imagens. A imagem tem que parecer 100% uma foto TIRADA POR UMA PESSOA COMUM no celular, sem produção. NÃO pode parecer foto profissional, NÃO pode parecer fotografia editorial, NÃO pode parecer foto gerada por IA. Tem que ser indistinguível de uma foto real de iPhone tirada por uma pessoa brasileira normal.

GATILHOS DE ULTRA-REALISMO OBRIGATÓRIOS (em inglês pro gerador de imagem):
- "amateur iPhone photo, casual snapshot"
- "raw unedited smartphone photography"
- "candid moment at home"
- "real Brazilian person, no model, no makeup professional"
- "imperfect framing, slightly off-center composition"
- "natural skin texture with visible pores"
- "natural daylight or warm home lamp, no studio lighting"
- "authentic Brazilian middle-class interior"
- "smartphone camera quality"
- "non-American interior, Brazilian context"

ELEMENTOS VISUAIS DO NICHO OBRIGATÓRIOS NO CENÁRIO (TÊM QUE APARECER VISIVELMENTE NA CENA):
[INSERIR ELEMENTOS INCONFUNDÍVEIS DO NICHO, VER BIBLIOTECA ABAIXO]

O cenário tem que ficar INCONFUNDÍVEL do nicho. Tem que ficar claro pra qualquer um bater o olho e saber a profissão/contexto, sem precisar de legenda.

A ARTE É DIVIDIDA VERTICALMENTE AO MEIO POR UMA LINHA BRANCA SÓLIDA E VISÍVEL no centro, separando os dois lados.

MESMA PESSOA NAS DUAS CENAS:
[DESCRIÇÃO DA PESSOA brasileira real do público do nicho: idade, fenótipo brasileiro autêntico, cabelo natural, sem produção, roupa casual brasileira. Mesma pessoa, mesma roupa, mesmo cenário, em momentos diferentes.]

LADO ESQUERDO (JEITO ERRADO):
[DESCRIÇÃO VISUAL ESPECÍFICA da pessoa fazendo o jeito errado. Expressão de cansaço, frustração ou erro. Elementos do cenário mostrando o problema. Postura abatida.]

NO TOPO desse lado, uma caixinha de legenda VERMELHA sólida (estilo etiqueta TikTok), levemente inclinada uns 5 graus, texto em branco sans-serif bold: "JEITO ERRADO ❌"

Logo abaixo da etiqueta, em texto bold branco com leve sombra preta: "[RESUMO CURTO DO JEITO ERRADO]"

LADO DIREITO (JEITO CERTO):
[DESCRIÇÃO VISUAL ESPECÍFICA da MESMA pessoa, no MESMO cenário, mas agora aplicando o jeito certo. Expressão de domínio e satisfação. Mesmos elementos do nicho, mas usados/dispostos de forma diferente. Postura ereta de quem se posicionou.]

NO TOPO desse lado, uma caixinha de legenda VERDE sólida (estilo etiqueta TikTok), levemente inclinada uns 5 graus no sentido oposto, texto em branco sans-serif bold: "JEITO CERTO ✅"

Logo abaixo da etiqueta, em texto bold branco com leve sombra preta: "[RESUMO CURTO DO JEITO CERTO]"

SOBRE TODA A ARTE, próximo ao centro mas integrado de forma natural, uma caixinha de legenda preta sólida (estilo padrão da legenda do TikTok), levemente inclinada uns 3 graus, com emoji [🤯 / 😱 / 💡 / ✨ / 👀] e texto branco sans-serif: "[EMOJI] [INSIGHT CURTO E DIRETO QUE EXPLICA POR QUE O JEITO CERTO FUNCIONA]"

NA BASE DA FOTO, um CTA simples e discreto estilo creator amador: "👇 te conto tudo no link da bio"

REGRA DE CONTRASTE DO CTA (obrigatória): o CTA precisa ter contraste forte com a cor de fundo da região onde foi posicionado, garantindo legibilidade máxima.
- Se a base da imagem está escura: texto em amarelo vivo, branco puro ou laranja vivo.
- Se a base está clara: texto em preto, vermelho ou azul-marinho.
- Se está em tom neutro: branco puro ou preto puro com fundo semi-transparente fino atrás.

ESTÉTICA GERAL:
- Visual de UGC autêntico brasileiro, indistinguível de post real de pessoa comum.
- Pequenas imperfeições visuais bem-vindas (grão de smartphone, foco amador).
- Cenário INCONFUNDIVELMENTE do nicho, com os elementos visuais característicos bem visíveis.
- NÃO pode parecer foto profissional, NÃO pode ter estética editorial, NÃO pode parecer banner publicitário.

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

O texto do jeito errado, do jeito certo e o insight central NÃO passam pela revisora (são conteúdo da arte com tom específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, jeito errado específico e jeito certo profundo.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Jeito Certo × Jeito Errado:

📌 IDEIA ESCOLHIDA (nº {numero_ideia} das 10)
Errado: [resumo do jeito errado]
Certo: [resumo do jeito certo]

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

Se escolher 2, perguntar o que ajustar (título, legenda, jeito errado, jeito certo, insight, descrição da pessoa ou elementos visuais do nicho) e refazer apenas a parte indicada.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-jeito-certo-errado-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-jeito-certo-errado-{numero}.md`

Conteúdo do arquivo:

```markdown
# Jeito Certo × Jeito Errado nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**Funil:** [Topo, Meio ou Fundo]
**Errado:** [jeito errado]
**Certo:** [jeito certo]

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

Liste aqui todas as 10 ideias geradas nesta sessão, com funil, jeito errado e jeito certo de cada uma. Isso permite que o aluno volte e use as ideias restantes sem precisar rodar a sub-skill de novo.
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-jeito-certo-errado-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-jeito-certo-errado-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Jeito Certo × Jeito Errado salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-jeito-certo-errado-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Jeito Certo × Jeito Errado com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Jeito Certo × Jeito Errado gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-jeito-certo-errado-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-jeito-certo-errado-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Jeito Certo × Jeito Errado com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-jeito-certo-errado-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-jeito-certo-errado-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-jeito-certo-errado-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-jeito-certo-errado-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-jeito-certo-errado-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda.
- O texto do jeito errado, do jeito certo e o insight central seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- Preencha todos os campos entre colchetes com o conteúdo real. O texto final entregue ao usuário NÃO pode ter colchetes.
- O texto pro ChatGPT é em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês (que são gatilhos eficazes pro gerador de imagem).
- **Ultra-realismo brasileiro obrigatório**: a foto tem que ser indistinguível de selfie/snapshot real de brasileiro comum. Cabelo natural, pele real, casa com bagunça, fenótipo brasileiro autêntico, sem cara de modelo americano de banco de imagem, sem cara de IA.
- **Cenário inconfundível do nicho obrigatório**: 4 a 6 elementos visuais característicos do nicho precisam aparecer visivelmente. Use a biblioteca por nicho.
- **NUNCA use travessão** em nenhum texto. Vírgula ou ponto final no lugar.
- **Jeito errado específico, jeito certo profundo**: nunca generalize. Variedade de profundidade obrigatória (topo, meio, fundo).
- **Split vertical com linha branca divisora central**, etiquetas VERMELHA "JEITO ERRADO ❌" e VERDE "JEITO CERTO ✅" com leve inclinação estilo TikTok, insight central com emoji, CTA discreto na base.
- **CTA com regra de contraste contextual**: cor adapta ao fundo da imagem.
- **Margens generosas** pra não cortar no Instagram.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias. Não travar o fluxo.
- Se o nicho não tiver na biblioteca de elementos visuais, construa uma lista de 4 a 6 elementos inconfundíveis baseada no contexto do produto, sempre priorizando objetos que aparecem visivelmente na cena e identificam o nicho de cara.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).

## Biblioteca de elementos visuais por nicho

Use essa biblioteca pra preencher a seção "ELEMENTOS VISUAIS DO NICHO OBRIGATÓRIOS NO CENÁRIO" do prompt. Cada nicho tem 4 a 6 elementos inconfundíveis que precisam aparecer visivelmente na cena pra qualquer um identificar a profissão/contexto.

### Videomaker / produção audiovisual
- Câmera mirrorless ou DSLR profissional (Sony A7, Canon R6) com lente grande acoplada
- Tripé de vídeo ou gimbal estabilizador (DJI Ronin, Zhiyun)
- 2 ou 3 lentes de tamanhos diferentes espalhadas
- Notebook ou monitor mostrando timeline de edição de vídeo visível (Premiere, DaVinci, Final Cut)
- Fone de monitoração profissional grande (Sony MDR-7506)
- HD externo, SSD portátil ou cartões SD
- Painel LED de iluminação ou softbox pequeno
- Pôster de filme ou storyboard na parede

### Skin care / beleza / anti-aging
- 4 ou 5 frascos de sérum, hidratante, protetor e demaquilante na pia ou prateleira
- Espelho de banheiro com luz frontal ou natural
- Algodão, cotonete, gaze de limpeza facial
- Pano de rosto pendurado ou dobrado
- Estojo de maquiagem ou nécessaire
- Toalha de banho usada visível
- Frasco de água termal ou loção tônica

### Maternidade / discipulado infantil / educação cristã
- Apostila impressa em papel A4 com atividades visíveis
- Bíblia infantil ou Bíblia com marcador
- Lápis de cor, giz de cera, tesoura sem ponta
- Atividade colorida em andamento, desenho infantil
- Brinquedo cristão, bichinho de pelúcia
- Caderno de anotações da mãe com versículos

### Cafeteria / negócio gastronômico
- Máquina de espresso comercial (Lacave, Rancilio, Astoria)
- Moedor de café elétrico profissional
- Leiteira de inox, jarra de leite vaporizado
- Grãos de café à mostra em recipiente de vidro
- Balcão de granito ou madeira com gotas de café
- Xícaras de porcelana, copos de papel kraft
- Cardápio em quadro negro ou impresso, tablet de pedidos

### Tráfego pago / marketing digital / IA
- Notebook com Meta Ads Manager ou Google Ads visível na tela (gráficos de CPM, CPL, ROAS)
- Segunda tela ou tablet mostrando dashboard de campanha
- Fone de ouvido em volta do pescoço
- Caderno de anotações com cálculos, planilhas impressas
- Garrafa de água ou copo de café
- Pode incluir tela com Claude/ChatGPT aberto pra nicho de IA

### Bonsai / jardinagem / hobby botânico
- Vasos de bonsai em diferentes estágios (mudas, adultos)
- Akadama (substrato granular marrom-avermelhado típico)
- Tesoura de poda específica de bonsai
- Arame de cobre enrolado pra aramação
- Regador pequeno, borrifador
- Pinça de bonsai, ancinho miniatura

### Concurso público / estudos / educação
- Vade Mecum aberto com grifos
- Marca-texto coloridos (3 ou 4 cores diferentes)
- Caderno espiral com anotações grifadas
- Notebook ou tablet com videoaula pausada
- Fone de ouvido sobre a mesa
- Calendário de cronograma de estudos na parede
- Garrafa de café, xícara de café passado

### Esquecer o ex / relacionamento / autoconhecimento
- Caderno de anotações ou journal abertos
- Caneta, marca-texto
- Celular ao lado mostrando WhatsApp ou Instagram fechado
- Xícara de chá ou café
- Vela acesa, planta natural
- Cama ou sofá com edredom amassado
- Livro de autoajuda ou estoicismo

### Bonecas de pano / artesanato têxtil
- Tecidos de algodão dobrados em pilhas
- Linhas coloridas em carretéis
- Agulhas, alfinetes em alfineteiro
- Tesoura de costura específica
- Bonecas de pano em diferentes etapas (sem rosto, com rosto, completas)
- Botões variados, fitas, rendas
- Mesa de costura com máquina ao fundo

### Feng Shui / arquitetura / harmonização
- Bagua do Feng Shui em mapa ou desenho
- Cristais variados (ametista, quartzo rosa)
- Bambu da sorte, planta na água
- Espelho pequeno decorativo
- Sineta dos ventos ou mobile
- Bússola pequena, mapa de planta baixa
- Velas, sálvia ou incenso

### Introdução alimentar / nutrição infantil
- Pratinho infantil colorido com divisórias
- Babador de silicone com bolso
- Cadeira de alimentação visível
- Frutas e legumes cortados em diferentes formatos (tira, cubo, quartos)
- Talher infantil de plástico ou silicone
- Copo de transição
- Caderno de registro de introdução

### Dermatite canina / pet care
- Cachorro com pelagem saudável (NUNCA com lesão visível)
- Colar elisabetano de plástico transparente
- Bisnagas de pomada veterinária e frascos de remédio
- Caminha do pet visível
- Comedouro e bebedouro com ração
- Coleira pendurada
- Caderno com anotações da rotina do pet

### Infoproduto / negócios digitais / criadores
- Notebook com dashboard de vendas visível na tela
- Segunda tela com gráficos ou Meta Ads
- Celular ao lado mostrando notificações de venda
- Ring light pequeno improvisado ou apoiado
- Caderno com funis desenhados, fluxograma
- Garrafa de café, post-its colados na mesa

### Skincare profissional / dermato / estética
- Maca de procedimento estético com lençol branco
- Aparelhos de skincare profissional (LED, radiofrequência)
- Frascos de cosméticos profissionais alinhados
- Lupa facial, pinça de extração
- Avental ou jaleco branco
- Caderno de ficha de paciente

### Fitness / emagrecimento / nutrição esportiva
- Marmita organizada com porções coloridas
- Balança de cozinha digital
- Tupperware em pilha
- Tênis de corrida, faixa elástica, halter
- Garrafa de água com escala de medida
- Caderno de plano alimentar ou app aberto

### Alimentação saudável / meal prep / nutrição
- Potes de vidro ou plástico com marmitas prontas empilhadas na geladeira
- Fogão com 3 queimadores com panelas em uso simultâneo
- Bancada organizada com marmitas identificadas por etiqueta ou dia da semana
- Legumes cortados (brócolis, cenoura, abobrinha) em tábua de madeira
- Geladeira aberta mostrando prateleira com potes organizados por refeição
- Balança de cozinha digital, colher de medida, copo medidor
