# Criativo Notícia. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 13 (Criativo Notícia). Gera uma arte com cara de matéria real de portal de notícias brasileiro, com selo de editoria, manchete jornalística, subtítulo de apoio e CTA nativo de "continue lendo a matéria". Gera 10 headlines de notícia variando o tom, o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories), já com o estilo de portal que casa melhor com o tom da headline escolhida.

**Por que esse formato funciona:**
O criativo parece uma reportagem real, não propaganda. O selo de editoria, a manchete em fonte jornalística e o CTA de portal são padrões visuais que o leitor já confia, então o anúncio fura o ceticismo do feed. O subtítulo expande a manchete sem entregar a resposta, e essa lacuna é o que gera o clique pra "ler a matéria".

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço. O nicho decide o mapa secundário de estilo de portal.
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho. Inclua a faixa etária, porque o avatar da arte precisa ser coerente com a idade do público.
- **Quadro / promessa**: a transformação principal do `perfil.md`, pra alimentar o subtítulo (a linha de apoio insinua o resultado sem entregar a resposta).

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

**Se escolher 1**, pular pra etapa 2 (Geração das 10 headlines).

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

Se o aluno não especificou público, assumir um plausível brasileiro com base no produto/nicho e avisar antes de gerar as headlines:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Geração das 10 headlines de notícia

Anuncie:

```
🔍 Próximo passo: gerar 10 headlines de notícia do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere 10 headlines de notícia numa lista única numerada de 1 a 10. Cada headline tem:

- **Selo de editoria** estilo portal (ex: "BELEZA | COMPORTAMENTO", "ECONOMIA | PREVIDÊNCIA", "PETS | SAÚDE ANIMAL").
- **Tom indicado em parênteses** (Sensacionalista, Científico, Polêmico, Sério).
- **Manchete em itálico**, escrita como notícia real, não como propaganda.

#### Variedade de tons obrigatória

Misture os quatro tons ao longo das 10 headlines:

- **Sensacionalista**: chocante, com exagero numérico ou comportamental, manchete que para o scroll.
- **Científico**: cita estudos, pesquisas e dados de forma genérica, tom sóbrio e de credibilidade.
- **Polêmico**: opinião forte que contraria o senso comum do nicho.
- **Sério**: institucional, factual, manchete equilibrada de jornal grande.

#### Regras das headlines

- Cada headline conectada ao nicho/produto, mas escrita como matéria de portal, nunca como anúncio.
- Identificação do público integrada no selo de editoria ou na própria manchete.
- Pode usar estatísticas, estudos, pesquisas e referências a especialistas de forma genérica. Permitido: "Pesquisa mostra que 80%...", "Estudo aponta...", "Especialistas alertam...", "Dermatologista revela...". Se o produto é da própria criadora especialista, ela pode aparecer como fonte ("Veterinária revela", "Dermatologista expõe").
- PROIBIDO inventar fontes específicas falsas. Nunca cite "Estudo da USP", "Pesquisa de Harvard", "Dr. João Silva afirma" ou qualquer instituição ou pessoa específica que possa ser verificada e desmentida. Use sempre referências genéricas.
- Sem travessão. Use vírgula, ponto final ou parênteses no lugar.

#### Apresentação

Mostre as 10 headlines numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 headlines de notícia pro seu nicho.

---

**1.** (Sensacionalista)
**[EDITORIA | SUBCATEGORIA]**
*"[Manchete em estilo de notícia]"*

---

**2.** (Científico)
**[EDITORIA | SUBCATEGORIA]**
*"[Manchete em estilo de notícia]"*

---

Qual número você quer transformar em criativo?
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

### 3. Escolha e geração do criativo

Após o aluno escolher um número de 1 a 10, anuncie:

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

#### Decisão sobre o estilo de portal correto

Antes de montar os prompts, decida o estilo visual do portal. **O estilo casa primeiro com o TOM da headline escolhida (primário) e depois com o NICHO (secundário).**

##### Mapa de tom × estilo de portal

- **Sensacionalista** → Tabloide brasileiro estilo Metrópoles, Extra, R7 (manchete agressiva, cores vibrantes saturadas, flash forte, contraste alto, vinheta escura, tipografia jornalística pesada, expressão dramática exagerada).
- **Científico** → Jornalismo de saúde e ciência estilo G1 Bem-Estar, Veja Saúde, UOL Viva Bem (clean, sóbrio, paleta muted, iluminação natural neutra, com elementos editoriais discretos como diagramas ou frascos organizados).
- **Polêmico** → Pode ir em qualquer um dos dois, conforme o peso. Se a polêmica é de mercado, dinheiro ou comportamento extremo, vai pra tabloide. Se é técnica ou profissional, vai pra institucional.
- **Sério** → Jornalismo institucional estilo Folha, Estadão, Valor Econômico, Forbes Brasil (editorial premium, paleta sóbria, foto editorial com profundidade, tipografia clássica pesada).

##### Mapa secundário de nicho × portal

- **Saúde infantil / maternidade / introdução alimentar** → G1, UOL Viva Bem (sério, limpo, credibilidade alta).
- **Concursos / educação** → R7, Estadão (sério-popular, jornalístico institucional).
- **Relacionamento / esquecer o ex / sexualidade / comportamento** → Metrópoles, Extra (sensacionalista, foto dramática).
- **Beleza / skincare / anti-aging** → Metrópoles (sensacional) ou Veja Saúde (científico), conforme tom.
- **Alimentação saudável / meal prep / nutrição (pessoa física)** → G1 Bem-Estar, UOL Viva Bem (científico, credibilidade de saúde) ou Metrópoles (sensacional), conforme tom.
- **Finanças / investimentos / previdência** → Valor Econômico, InfoMoney, Estadão, Exame (institucional financeiro, paleta sóbria).
- **Empreendedorismo / marketing / IA / tech** → Forbes Brasil, Exame (institucional moderno premium).
- **Espiritualidade / Feng Shui / bem-estar** → Catraca Livre, Vogue Wellness (editorial leve, lifestyle).
- **Bonsai / hobby / artesanato** → Catraca Livre, blog editorial (calmo, leve, foto natural).
- **Gastronomia / cafeteria / negócio próprio** → Pequenas Empresas Grandes Negócios, Sebrae (institucional acessível).
- **Pets / veterinária / animais** → Metrópoles (sensacional pra dor emocional) ou G1 (científico, saúde animal), conforme tom.

Use os gatilhos visuais do estilo decidido a partir da seção "Biblioteca de gatilhos visuais por estilo de portal" no fim deste arquivo.

Gere quatro coisas a partir da headline escolhida:

#### A) Título do anúncio

A própria manchete da headline escolhida. Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem promessa vaga (incluir dado, prazo ou situação concreta)
- Sem "não é X. É Y."
- Produto não aparece no lead
- Não inventar fontes específicas falsas

#### B) Legenda pro Instagram

2 a 3 linhas, conecta com a manchete, gera curiosidade sem entregar a resposta. Termina com "Link na bio". Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

````
Cria pra mim uma arte de anúncio pra Instagram no formato de notícia de portal jornalístico brasileiro estilo [NOME DO PORTAL REFERÊNCIA]. A arte tem que parecer uma matéria REAL publicada num portal grande, com [TOM ESPECÍFICO DO ESTILO]. Não pode parecer propaganda nem foto bonita de banco de imagem.

[SE FOR TABLOIDE SENSACIONALISTA] O CHOQUE VISUAL VEM DA EMOÇÃO E DO SIMBOLISMO, NÃO DA EXPOSIÇÃO DE PROBLEMA FÍSICO. Respeite políticas do Facebook Ads: PROIBIDO mostrar feridas, cortes, sangue, lesões visíveis na pele, pelagem rarefeita, cadáveres, cenas de violência, agressão, sofrimento físico extremo, comparações médicas chocantes (acne severa, lesões), conteúdo gore. O que comunica o problema são EXPRESSÃO EMOCIONAL EXAGERADA, LINGUAGEM CORPORAL, CENÁRIO SIMBÓLICO (papéis espalhados, remédios, calculadora, calendário, colar elisabetano, etc) e COMPOSIÇÃO DRAMÁTICA, nunca a exposição do problema em si.

ESTILO FOTOGRÁFICO OBRIGATÓRIO (gatilhos pro gerador de imagem):
[INSERIR GATILHOS DO ESTILO ESCOLHIDO, VER BIBLIOTECA ABAIXO]

LAYOUT DA NOTÍCIA:

NO TOPO, um selo/tag de editoria estilo portal de notícias: retângulo pequeno com cor sólida [COR DO SELO COERENTE COM O ESTILO], texto em branco bold: "[EDITORIA | SUBCATEGORIA]"

IMAGEM DE FUNDO:
[DESCRIÇÃO DETALHADA DA IMAGEM CONECTADA À HEADLINE, com avatar brasileiro real do nicho, cenário cotidiano brasileiro, expressão e linguagem corporal que comunicam o tom da matéria. Se for tabloide, adicionar elementos de choque emocional/simbólico compliance-safe. Se for institucional, adicionar elementos editoriais de credibilidade.]

A imagem deve ter um filtro escurecido sutil pra dar leitura ao texto que vem por cima.

MANCHETE (HEADLINE):
Texto grande, bold, em fonte serifada jornalística pesada (estilo manchete de [PORTAL REFERÊNCIA]), branca com sombra escura pra leitura sobre a foto. Manchete: "[MANCHETE ESCOLHIDA]"

SUBTÍTULO (LINHA DE APOIO):
Logo abaixo da manchete, em fonte menor, sans-serif clara, cor branca: "[SUBTÍTULO DE 1-2 LINHAS QUE EXPANDE A MANCHETE SEM ENTREGAR A RESPOSTA]"

CTA NATIVO DE PORTAL:
Na base da arte, um link estilo portal jornalístico: "Continue lendo a matéria →" em sans-serif bold, cor [COR DO CTA COERENTE COM O ESTILO], com sublinhado discreto indicando link clicável.

ESTÉTICA GERAL:
- Visual de portal jornalístico [SENSACIONALISTA / INSTITUCIONAL / CIENTÍFICO / FINANCEIRO] coerente.
- A imagem [PARA O SCROLL em 1 segundo pelo choque emocional / Transmite credibilidade jornalística].
- Tem que parecer matéria de portal, não anúncio.
- Hiperrealismo fotográfico, pessoa real brasileira, expressão real coerente com o tom.

POSICIONAMENTO: TODOS OS ELEMENTOS (selo, manchete, subtítulo, CTA) DEVEM SUBIR um pouco do rodapé. Deixa margem generosa entre o CTA e a borda inferior da arte (mínimo 8 a 10% da altura), pra não correr risco de corte quando o Instagram exibir o anúncio. Mesmo respeito de margem no topo.

PROIBIDO usar travessão (nem o "—" nem o "–") em nenhum texto da arte. Use vírgula ou ponto final no lugar.

Fonte grande, legível em celular. Pouco texto extra na arte, foco na manchete e subtítulo.

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

A manchete e o subtítulo da arte NÃO passam pela revisora (são conteúdo da arte com tom jornalístico específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, sem fontes específicas falsas, sem estrutura "não é X. É Y." (afirmar diretamente, sem negação), e o subtítulo nunca entrega a resposta completa.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Notícia:

📌 HEADLINE ESCOLHIDA (nº {numero_headline} das 10)
[EDITORIA | SUBCATEGORIA]
[manchete escolhida]

📌 TÍTULO DO ANÚNCIO
[título gerado]

📝 LEGENDA PRO INSTAGRAM
[legenda gerada terminando em "Link na bio"]

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

📱 PROMPT PRO CHATGPT, FORMATO STORIES
[prompt Stories, dentro de bloco de código]

---
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher outra headline (das 10)
```

Se escolher 2, perguntar o que ajustar (título, legenda, manchete, subtítulo, estilo de portal ou descrição visual) e refazer apenas a parte indicada.

Se escolher 3, apresentar a lista das 10 headlines novamente e perguntar o novo número.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-noticia-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-noticia-{numero}.md`

Conteúdo do arquivo:

```markdown
# Criativo Notícia nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Headline escolhida (nº {numero_headline} das 10)

**Editoria:** [EDITORIA | SUBCATEGORIA]
**Tom:** [tom da headline]
**Manchete:** [EDITORIA | SUBCATEGORIA]: [manchete escolhida]

(Separador entre editoria e manchete é sempre dois-pontos. Nunca usar travessão.)
**Estilo de portal:** [estilo de portal escolhido]

## Título do anúncio

[título]

## Legenda pro Instagram

[legenda terminando em "Link na bio"]

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

## Banco completo (as 10 headlines geradas nesta sessão)

Liste todas as 10 headlines geradas nesta sessão, no mesmo formato numerado da apresentação (número, tom, editoria e manchete). Isso permite ao aluno usar as outras headlines depois sem precisar rodar a sub-skill de novo.
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-noticia-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-noticia-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Criativo Notícia salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-noticia-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Criativo Notícia com outra das 10 headlines
2. Trocar o nicho ou público e gerar 10 headlines novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Criativo Notícia gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-noticia-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-noticia-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Criativo Notícia com outra das 10 headlines
3. Trocar o nicho ou público e gerar 10 headlines novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-noticia-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-noticia-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-noticia-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-noticia-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-noticia-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda.
- A manchete e o subtítulo seguem regras próprias (tom jornalístico, sem fontes falsas) e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- **Variedade de tons obrigatória nas 10 headlines**: misturar sensacionalista, científica, polêmica e séria.
- Preencha todos os campos entre colchetes com o conteúdo real. O texto final entregue ao aluno e no arquivo salvo NÃO pode ter colchetes.
- O texto pro ChatGPT é em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês (que são gatilhos eficazes pro gerador de imagem).
- **Avatar brasileiro real**: pessoa de classe média típica, sem produção de modelo, contexto cotidiano brasileiro. Faixa etária coerente com o público do nicho.
- **NUNCA use travessão** em nenhum texto (manchete, subtítulo, título do anúncio, legenda, prompt do ChatGPT). Vírgula ou ponto final no lugar.
- **NUNCA invente fontes específicas falsas.** Use referências genéricas a estudos, pesquisas, especialistas. Pode usar estatísticas concretas. Não pode citar USP, Harvard, "Dr. Fulano", instituições reais.
- **COMPLIANCE Facebook Ads obrigatório:** PROIBIDO mostrar feridas, cortes, sangue, lesões, pelagem rarefeita, cadáveres, violência, agressão, sofrimento físico extremo, comparações médicas chocantes. O choque visual vem da emoção e do simbolismo, nunca da exposição do problema físico.
- **O estilo do portal casa primeiro com o TOM da headline, depois com o NICHO.** Sensacionalista pede tabloide; científica pede saúde editorial; séria pede institucional; polêmica pode ir nos dois caminhos conforme o peso da polêmica.
- Subtítulo do criativo expande a manchete sem entregar a resposta completa. CTA sempre "Continue lendo a matéria →" estilo portal nativo.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível brasileiro com base no produto e avisar antes de gerar as 10 headlines. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).

## Biblioteca de gatilhos visuais por estilo de portal

### Tabloide sensacionalista (Metrópoles, Extra, R7)

- "tabloid magazine cover photography"
- "harsh on-camera flash, direct flash like paparazzi"
- "extreme close-up, dramatic angle"
- "high saturation, high contrast, punchy colors"
- "yellow-red color grading typical of sensationalist media"
- "heavy vignette around edges"
- "British tabloid Sun magazine cover style"
- "dramatic exaggerated emotional expression"
- "documentary nighttime reportage style"
- "shocking visual that stops the scroll"

Cor do selo: VERMELHO ou LARANJA sólido
Cor do CTA: VERMELHO vibrante

### Jornalismo científico/saúde editorial (G1 Bem-Estar, Veja Saúde, UOL Viva Bem)

- "editorial science magazine photography"
- "clean studio portrait, neutral lighting"
- "macro close-up, scientific aesthetic"
- "muted natural color grading"
- "high-end magazine quality"
- "subtle scientific diagram overlay"
- "soft natural lighting, refined composition"

Cor do selo: AZUL ESCURO ou VERDE INSTITUCIONAL sólido
Cor do CTA: AZUL ESCURO institucional ou VERDE

### Jornalismo institucional sério (Folha, Estadão, Valor Econômico)

- "editorial newspaper photography"
- "documentary-style reportage with emotional weight"
- "clean corporate portrait, soft natural lighting"
- "muted neutral color grading, professional"
- "Brazilian editorial photography"
- "high-end magazine quality, refined composition"
- "subtle depth of field, premium feel"

Cor do selo: AZUL ESCURO ou PRETO sólido
Cor do CTA: AZUL ESCURO institucional

### Jornalismo financeiro premium (Valor, InfoMoney, Exame, Forbes)

- "editorial business magazine photography"
- "Bloomberg magazine aesthetic"
- "clean corporate portrait, soft natural lighting"
- "muted neutral color grading, professional"
- "Brazilian financial editorial photography"
- "high-end magazine quality, refined composition"
- "subtle depth of field, premium feel"

Cor do selo: AZUL ESCURO institucional ou VERDE financeiro
Cor do CTA: AZUL ESCURO institucional ou VERDE

### Editorial leve/lifestyle (Catraca Livre, Vogue Wellness)

- "lifestyle magazine photography"
- "warm natural lighting"
- "soft pastel color grading"
- "editorial wellness aesthetic"
- "refined minimalist composition"
- "magazine spread quality"

Cor do selo: TONS QUENTES (terracota, mostarda apagada, verde musgo)
Cor do CTA: NA PALETA DA EDITORIA
