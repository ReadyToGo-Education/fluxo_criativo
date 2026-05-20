# Checklist. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 9 (Checklist). Cria uma arte híbrida (foto UGC ultra realista da pessoa do nicho num momento caótico do problema, segurando um caderno com um checklist de 5 passos práticos bem legível). Gera 10 temas de checklist, o aluno escolhe um, e a sub-skill monta o checklist completo de 5 itens, título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
O aluno vê uma cena reconhecível e caótica do próprio problema, se identifica na hora e o olho trava na arte. O caderno entrega um protocolo prático de verdade, o que gera valor antes de o leitor perceber que é anúncio. O checklist mostra os 5 passos, mas o método completo fica reservado pro link, e essa lacuna é o que gera o clique.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço.
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho.
- **Método / framework do produto**: a Furadeira ou método estruturado do `perfil.md`, se houver. Quando o produto tem um framework próprio, o checklist usa o vocabulário específico desse método.
- **Quadro / promessa**: a transformação principal do `perfil.md`, pra alimentar o problema/promessa central que os 10 temas vão orbitar.

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

**Se escolher 1**, pular pra etapa 2 (Geração dos 10 temas de checklist).

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

Se o aluno não especificou público, assumir um plausível brasileiro com base no produto/nicho e avisar antes de gerar os temas:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Geração dos 10 temas de checklist

Anuncie:

```
🔍 Próximo passo: gerar 10 temas de checklist do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere 10 temas de checklist numa lista única numerada de 1 a 10.

**CRÍTICO: TODOS os 10 checklists devem orbitar o MESMO problema/promessa central do produto**, atacando ele em ângulos e situações diferentes. Não pulverizar em temas distintos do nicho.

Exemplos:

- Produto "esquecer o ex" → todos os 10 checklists são sobre esquecer o ex (primeiro dia, 7 dias depois, quando ele chama, durante crise de saudade, etc).
- Produto "cachorro parar de coçar" → todos os 10 são sobre coceira/dermatite (identificar gatilho, primeira crise, dormir sem coçar, antes do Apoquel, etc).
- Produto "cestas de café da manhã" → todos os 10 são sobre vender cesta (primeira venda, precificar, divulgar, datas, embalagem, etc).

#### Regras dos temas

- **Específicos e descritivos.** Cada tema deve identificar pra qual sub-situação do problema ele serve.
- **Sem prazos longos.** PROIBIDO prometer resultado em 30, 60 ou 90 dias. Permitido: 24 horas, 48 horas, 7 dias, ou sem prazo (com promessa no método ou no resultado).
- **Variedade de ângulos.** Cobrir situações diferentes: primeira vez, crise, manutenção, dia a dia, problemas específicos, sinais de melhora.

#### Apresentação

Cada tema tem o formato:
- Selo "✅ Checklist [Categoria do nicho]"
- Tema específico do checklist em itálico abaixo

Mostre os 10 temas numerados de 1 a 10, separados por linhas divisórias `---`. Sem isso fica amontoado e confuso.

```
Aqui estão 10 temas de checklist pro seu nicho.

---

**1.** ✅ Checklist [Categoria do nicho]
*[Tema específico do checklist]*

---

**2.** ✅ Checklist [Categoria do nicho]
*[Tema específico do checklist]*

---

**3.** ✅ Checklist [Categoria do nicho]
*[Tema específico do checklist]*

---

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

Primeiro, construa o **checklist completo de 5 itens** do tema escolhido. Não mais que 5 itens. Cada item segue estas regras:

- **AÇÃO concreta executável.** Verbo imperativo no início (Tire, Compre, Use, Aplique, Passe, Evite, Escolha, Suba, Otimize, Monte, Crie, Envie, Aceite, Anote).
- **Objeto específico.** Não pode ser abstrato. Item ruim: "Observe o cachorro". Item bom: "Tire a caminha do cachorro e coloque ele pra dormir em outro cômodo por 3 noites".
- **Curto e nítido.** Cabe em 1 linha do caderno na arte.
- **Sequência lógica.** Os 5 passos compõem um protocolo executável, do começo ao fim.
- **Sem prazos longos.** Se mencionar dias, máximo 7. Senão, sem prazo.
- **Coerente com o método ou produto.** Se o produto tem framework próprio, usar o vocabulário específico dele.

Depois gere quatro coisas a partir do tema e do checklist construído:

#### A) Título do anúncio

Frase de impacto conectada ao resultado prometido pelo checklist, objetiva. Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem pergunta no título
- Sem promessa vaga (incluir dado, prazo ou situação concreta)
- Sem "não é X. É Y."
- Produto não aparece no lead
- Linguagem que a pessoa usaria com uma amiga

#### B) Legenda pro Instagram

2 a 3 linhas em primeira pessoa, tom de creator amador. Gera curiosidade sem entregar o método. Termina com "Link na bio te conto tudo 👇" ou similar. Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

````
Cria pra mim uma arte de anúncio pra Instagram no formato HÍBRIDO UGC + ARTE, com elemento visual EXTRAVAGANTE/EXAGERADO. A foto principal tem que parecer 100% uma foto TIRADA POR UMA PESSOA COMUM no celular, mas o momento capturado é o momento ABSURDO/CAÓTICO do problema/processo, não um momento neutro. Cena que prende o olho na hora.

GATILHOS DE ULTRA-REALISMO OBRIGATÓRIOS (em inglês pro gerador de imagem):
- "amateur iPhone photo, casual snapshot"
- "raw unedited smartphone photography"
- "candid chaotic moment at home"
- "real Brazilian person, no model, no makeup professional"
- "imperfect framing, slightly off-center composition"
- "natural skin texture with visible pores"
- "natural daylight, no studio lighting"
- "authentic Brazilian middle-class home interior"
- "smartphone camera quality"
- "non-American interior, Brazilian context"

ELEMENTO EXTRAVAGANTE OBRIGATÓRIO:
[DESCRIÇÃO DA CENA NO MOMENTO ABSURDO/CAÓTICO do problema ou processo do nicho. Skin care: mulher lambuzada de creme até o pescoço. Tráfego pago: cara totalmente descabelado mexendo no Meta Ads. Dermatite canina: cachorro coçando freneticamente. Cestas: mulher no meio do caos de itens espalhados. SEMPRE compliance Facebook Ads: PROIBIDO mostrar feridas, sangue, lesões, cadáveres, violência. O exagero vem da situação visual e expressão, nunca da exposição de problema físico explícito.]

ELEMENTOS VISUAIS DO NICHO OBRIGATÓRIOS NO CENÁRIO (TÊM QUE APARECER VISIVELMENTE):
[INSERIR 4 a 6 ELEMENTOS INCONFUNDÍVEIS DO NICHO baseado na biblioteca abaixo. O cenário tem que ficar INCONFUNDÍVEL pra qualquer um bater o olho e saber o nicho.]

A CENA:
[DESCRIÇÃO DA PESSOA brasileira real do público do nicho: idade, fenótipo brasileiro autêntico, cabelo natural, sem produção, roupa casual brasileira, expressão exagerada do momento absurdo. Local brasileiro real (apartamento de classe média) com bagunça normal.]

A pessoa segura nas mãos um caderno (ou bloco/folha, ESCOLHIDO conforme o nicho, feminino: caderno espiral colorido, diário, bloco floral. Masculino/tech: caderno preto, bloco simples, folha A4 amassada, prancheta) aberto numa página com o checklist visível e bem legível, no meio do caos.

ELEMENTO DESIGN NO CADERNO (prioridade total na legibilidade):

A pessoa segura o caderno aberto numa página com o checklist. Design da página: limpo, com cara de mistura entre anotação real e arte editorial, garantindo LEITURA PERFEITA.

Conteúdo da página (deve aparecer TODO visível e legível, com tipografia GRANDE):

NO TOPO DA PÁGINA, título em destaque, fonte sans-serif bold preta, TAMANHO BEM GRANDE:
"✅ CHECKLIST [CATEGORIA DO NICHO]"

Subtítulo logo abaixo, fonte sans-serif média preta, TAMANHO MÉDIO:
"[TEMA ESPECÍFICO DO CHECKLIST]"

Linha divisória fina abaixo.

Lista numerada de 1 a 5 (5 itens, não mais), cada item com checkbox quadrado vazio (☐) à esquerda, fonte sans-serif bold preta TAMANHO GRANDE, com espaço generoso entre os itens:

☐ 1. [AÇÃO 1 PRÁTICA E ESPECÍFICA]
☐ 2. [AÇÃO 2 PRÁTICA E ESPECÍFICA]
☐ 3. [AÇÃO 3 PRÁTICA E ESPECÍFICA]
☐ 4. [AÇÃO 4 PRÁTICA E ESPECÍFICA]
☐ 5. [AÇÃO 5 PRÁTICA E ESPECÍFICA]

A página tem aparência limpa, levemente angulada (segurada pela pessoa), leve perspectiva. Fundo branco. PRIORIDADE TOTAL: LEITURA NÍTIDA. Tipografia grande o suficiente pra qualquer um ler na timeline. Espaço generoso entre itens.

SOBREPOSIÇÃO DE TEXTO ESTILO TIKTOK/INSTAGRAM AMADOR (sobre a foto, fora do caderno):

NO TERÇO SUPERIOR DA FOTO (sobre a parte da foto, não sobre o caderno), uma caixinha de legenda preta sólida (estilo padrão da legenda do TikTok), retangular, com cantos levemente arredondados, levemente inclinada uns 3 a 5 graus pra parecer jogada por cima. Texto em branco, sans-serif bold: "[CHAMADA QUE CONDUZ PRO LINK, NUNCA "salva", PUXANDO PALAVRA-CHAVE DO TEMA ESPECÍFICO DO CHECKLIST + EMOJI DO NICHO]"

NA BASE DA FOTO, um CTA simples e discreto estilo creator amador: "👇 te conto tudo no link da bio"

REGRA DE CONTRASTE DO CTA (obrigatória): o CTA precisa ter contraste forte com a cor de fundo da região onde foi posicionado.
- Fundo escuro: texto amarelo vivo, branco puro ou laranja vivo.
- Fundo claro: texto preto, vermelho ou azul-marinho.
- Tom neutro: branco ou preto puro com fundo semi-transparente fino atrás.

ESTÉTICA GERAL:
- Foto principal: UGC autêntico brasileiro CAÓTICO, capturando o momento absurdo/extravagante.
- Caderno/checklist: leitura nítida com tipografia grande, fundo branco, design limpo, prioridade total na legibilidade.
- Cenário INCONFUNDIVELMENTE do nicho.
- Compliance Facebook Ads: PROIBIDO ferida, sangue, lesão, cadáver, violência. Exagero vem da situação e expressão.
- NÃO pode parecer banner publicitário polido.

PROIBIDO usar travessão em nenhum texto. Use vírgula ou ponto final no lugar.

POSICIONAMENTO: TODOS OS ELEMENTOS DEVEM SUBIR um pouco do rodapé. Margem mínima de 8 a 10% da altura entre CTA e borda inferior.

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

Os 5 itens do checklist, o título do caderno e a caixinha sobre a foto NÃO passam pela revisora (são conteúdo da arte com tom específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, e a caixinha nunca usa "salva".

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Checklist:

📌 TEMA ESCOLHIDO (nº {numero_tema} dos 10)
✅ Checklist [categoria do nicho]
[tema específico do checklist]

✅ CHECKLIST DE 5 ITENS
☐ 1. [ação 1]
☐ 2. [ação 2]
☐ 3. [ação 3]
☐ 4. [ação 4]
☐ 5. [ação 5]

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
3. Voltar e escolher outro tema (dos 10)
```

Se escolher 2, perguntar o que ajustar (título, legenda, os 5 itens do checklist, descrição visual ou caixinha sobre a foto) e refazer apenas a parte indicada.

Se escolher 3, apresentar a lista dos 10 temas novamente e perguntar o novo número.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-checklist-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-checklist-{numero}.md`

Conteúdo do arquivo:

```markdown
# Checklist nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Tema escolhido (nº {numero_tema} dos 10)

✅ Checklist [categoria do nicho]
[tema específico do checklist]

## Checklist de 5 itens

☐ 1. [ação 1]
☐ 2. [ação 2]
☐ 3. [ação 3]
☐ 4. [ação 4]
☐ 5. [ação 5]

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

## Banco completo (os 10 temas gerados nesta sessão)

Liste aqui todos os 10 temas de checklist gerados nesta sessão, pra o aluno usar depois sem rodar a sub-skill de novo.
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-checklist-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-checklist-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Checklist salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-checklist-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Checklist com outro dos 10 temas
2. Trocar o nicho ou público e gerar 10 temas novos
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Checklist gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-checklist-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-checklist-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Checklist com outro dos 10 temas
3. Trocar o nicho ou público e gerar 10 temas novos
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-checklist-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-checklist-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-checklist-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-checklist-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-checklist-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda.
- Os 5 itens do checklist, o título do caderno e a caixinha sobre a foto seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- **Todos os 10 checklists orbitam o MESMO problema/promessa central do produto.** Não pulverizar em temas distintos do nicho.
- **Variedade de prazos curtos** (24h, 48h, 7 dias) ou sem prazo. PROIBIDO prazos longos (30/60/90 dias).
- **5 itens no checklist, não mais.** Cada um é AÇÃO concreta executável, com verbo imperativo no início e objeto específico, curto o suficiente pra caber em 1 linha do caderno.
- **Sequência lógica.** Os 5 passos compõem um protocolo executável do começo ao fim.
- **Coerente com o método ou produto.** Se o produto tem framework próprio, usar o vocabulário específico dele nos itens.
- **Ultra-realismo brasileiro obrigatório** mais **elemento extravagante** capturado no momento absurdo do problema.
- **Cenário inconfundível do nicho** com 4 a 6 elementos visuais característicos.
- **Caderno ou bloco escolhido conforme o nicho** (feminino, masculino, criativo, técnico).
- **Tipografia GRANDE no checklist** pra leitura nítida na timeline. Título grande, subtítulo médio, itens grandes.
- **A caixinha sobre a foto NUNCA usa "salva esse checklist".** Salvamentos não convertem em clique. A caixinha sempre conduz pro link. Padrões aceitos:
  - "Use esse checklist [contexto/quando] e eu te conto o resto no link [emoji do nicho]"
  - "Pega esse checklist, mas o método completo tá no link [emoji]"
  - "Esse checklist é só o começo. Te conto tudo lá no link [emoji]"
  - "Faz esse checklist [contexto/quando] e me chama no link [emoji]"
- **A caixinha SEMPRE puxa palavra-chave do tema específico** do checklist escolhido, pra diferenciar cada criativo da mesma campanha. Exemplos pro nicho de dermatite canina:
  - Tema "identificar gatilho" → "Use esse checklist pra descobrir o gatilho da dermatite do teu cachorro 🐶"
  - Tema "antes do Apoquel" → "Pega esse checklist antes de comprar Apoquel 🐶"
  - Tema "dormir sem coçar" → "Use esse checklist se teu cachorro não dorme de tanto coçar 🐶"
- **CTA com regra de contraste contextual** (fundo escuro pede texto claro, fundo claro pede texto escuro, tom neutro pede branco ou preto com fundo semitransparente fino atrás).
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- **Compliance Facebook Ads** obrigatório: sem ferida, sangue, lesão, cadáver, violência. O exagero vem da situação visual e da expressão, nunca da exposição de problema físico explícito.
- Se o nicho não estiver na biblioteca de elementos visuais, construir 4 a 6 elementos inconfundíveis baseado no contexto do produto.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar os 10 temas. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).

## Biblioteca de elementos visuais por nicho

Use essa biblioteca pra preencher a seção "ELEMENTOS VISUAIS DO NICHO" e o "ELEMENTO EXTRAVAGANTE" do prompt. Cada nicho tem 4 a 6 elementos inconfundíveis que precisam aparecer visivelmente na cena pra qualquer um identificar o nicho.

### Dermatite canina / pet care
**Elementos**: cachorro de porte médio com pelagem íntegra, caminha do pet, comedouro com ração, coleira pendurada, brinquedo no chão, pomada veterinária e frascos de remédio na mesa.
**Extravagante**: cachorro se coçando freneticamente com a pata traseira, mordendo a própria pata ou esfregando no tapete. Compliance: sem lesão visível.
**Caderno**: caderno casual feminino ou masculino conforme o tutor.

### Skin care / beleza / anti-aging
**Elementos**: 4 ou 5 frascos de sérum/hidratante/protetor na pia, espelho de banheiro com luz, algodão e demaquilante, pano de rosto, estojo de maquiagem.
**Extravagante**: mulher lambuzada de creme até o pescoço, máscara facial escorrendo, papel toalha pendurado no cabelo, expressão de "tô fazendo de tudo".
**Caderno**: diário feminino floral ou caderno espiral colorido.

### Maternidade / discipulado infantil / introdução alimentar
**Elementos**: apostila impressa com atividades, Bíblia infantil, lápis de cor, atividade colorida em andamento, brinquedo, mochila escolar.
**Extravagante**: criança chorando ou pulando, comida no chão, brinquedos espalhados pela sala, mãe segurando o caderno no meio da bagunça.
**Caderno**: caderno espiral feminino, agenda de mãe com adesivos.

### Cafeteria / gastronomia / cestas de café da manhã
**Elementos**: cesta de palha aberta, potinhos de geleia, pães caseiros, frutas variadas, fita de cetim, papel kraft, máquina de café se for cafeteria.
**Extravagante**: bancada transbordando de itens, farinha no rosto/mãos, pacote rasgado, vapor de café, fita pendurada no braço.
**Caderno**: caderno espiral colorido, bloco de receitas com capa floral.

### Tráfego pago / marketing digital / IA
**Elementos**: notebook com Meta Ads visível, segunda tela com dashboard, fone, planilha impressa, garrafa de café, post-its colados.
**Extravagante**: cara totalmente descabelado, várias telas ligadas ao redor, papéis voando, expressão de "tô no caos".
**Caderno**: caderno preto simples, bloco com fluxograma desenhado, prancheta.

### Bonsai / jardinagem / hobby botânico
**Elementos**: vasos de bonsai, akadama, tesoura de poda, arame de cobre, regador pequeno, pinça.
**Extravagante**: terra espalhada na bancada, raízes expostas em transplante, várias ferramentas espalhadas, expressão concentrada.
**Caderno**: caderno de capa rústica ou bloco de anotações com folhas amareladas.

### Concurso público / estudos
**Elementos**: vade mecum aberto, marca-textos coloridos, caderno espiral grifado, notebook com videoaula, cronograma na parede.
**Extravagante**: marca-textos espalhados, várias canetas, papel amassado, expressão de exaustão concentrada, cabelo bagunçado.
**Caderno**: caderno espiral universitário, prancheta com cronograma.

### Esquecer o ex / relacionamento / autoconhecimento
**Elementos**: caderno/journal aberto, vela acesa, planta natural, celular escondido, xícara de chá, livro de estoicismo.
**Extravagante**: olhos vermelhos de choro, lenços de papel no chão, edredom amassado, foto antiga na mão.
**Caderno**: journal feminino com capa em tom pastel, caderno de anotações de autocuidado.

### Bonecas de pano / artesanato têxtil
**Elementos**: tecidos dobrados, linhas coloridas em carretéis, agulhas em alfineteiro, tesoura de costura, bonecas em diferentes etapas, botões.
**Extravagante**: linhas espalhadas, tecidos cobrindo a mesa, retalhos no chão, máquina de costura ligada.
**Caderno**: caderno espiral feminino vintage, bloco com moldes desenhados.

### Feng Shui / arquitetura / harmonização
**Elementos**: bagua, cristais, bambu da sorte, espelho decorativo, sineta dos ventos, bússola, velas.
**Extravagante**: móveis fora do lugar, cristais espalhados pelo chão, vela quase apagada, expressão concentrada.
**Caderno**: caderno com capa zen ou bloco com símbolos orientais.

### Videomaker / produção audiovisual
**Elementos**: câmera mirrorless ou DSLR com lente, tripé/gimbal, lentes espalhadas, notebook com timeline de edição, fone de monitoração, HD externo.
**Extravagante**: cabos enrolados nos pés, várias câmeras ligadas, expressão de exaustão criativa, monitor mostrando timeline complexa.
**Caderno**: prancheta com storyboard, caderno preto simples de roteiro.

### Infoproduto / negócios digitais / criadores
**Elementos**: notebook com dashboard de vendas, segunda tela com Meta Ads, celular mostrando notificações de venda, ring light caseiro, caderno com funis desenhados.
**Extravagante**: várias telas ligadas, notificações pipocando, post-its em todo lugar, expressão de "tô no caos do negócio".
**Caderno**: caderno preto simples ou bloco com desenhos de funil.

### Fitness / emagrecimento / nutrição esportiva
**Elementos**: marmita organizada, balança digital, tupperwares, tênis de corrida, halter, garrafa de água com escala.
**Extravagante**: vários tupperwares espalhados, balança em uso, suor no rosto, expressão de "tô na missão".
**Caderno**: planner de treino, caderno fitness com tabelas.

### Alimentação saudável / meal prep / nutrição
**Elementos**: marmitas empilhadas com tampa, balança de cozinha digital, potes de vidro com ingredientes separados, tábua de corte com legumes, colher de medida, lista de compras impressa.
**Extravagante**: bancada lotada de marmitas abertas, ingredientes espalhados, pessoa segurando tampa e colher ao mesmo tempo, expressão de "preparei a semana toda de uma vez".
**Caderno**: caderno espiral colorido ou planner semanal de refeições com colunas de segunda a domingo.
