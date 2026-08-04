# Reflexão Editorial. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 24 (Reflexão Editorial). Formato de criativo estático onde o texto é o protagonista. Estilo post jornalístico/editorial com dados, notícias reais, polêmicas, contas malucas ou curiosidades surpreendentes do nicho. Fundo branco limpo, imagem jornalística de apoio, CTA sutil em cor forte. Gera 10 ideias de Reflexão Editorial, o aluno escolhe uma, e a sub-skill entrega legenda longa e prompt pronto pra colar no ChatGPT (Feed, com Stories).

**Por que esse formato funciona:**
O objetivo principal NÃO é vender. É fazer a pessoa pensar, se surpreender, se identificar. A venda aparece só no último parágrafo da legenda, quase como um P.S. Isso baixa a guarda do leitor, que consome o conteúdo como informação útil antes de perceber que é anúncio. A legenda longa faz o trabalho pesado de desenvolver a reflexão e vender, enquanto a arte vende a curiosidade.

## O que você está criando

Anúncios que parecem:
- post intelectual de newsletter ou tweet expandido
- matéria de revista com dado impactante
- reflexão compartilhável pela inteligência do argumento
- conteúdo que faz a pessoa pensar "nunca tinha visto por esse ângulo"

## O que você NUNCA cria

- Texto comercial óbvio (a venda é sutil, só no final)
- Dados inventados sem base (use pesquisas reais ou contas plausíveis)
- Apelo pra medo de doença ou morte
- Menção a remédios, medicamentos, doenças específicas, condições de saúde mental
- Linguagem sensacionalista de saúde
- Título gigante que domina a arte
- Conteúdo colado no rodapé

## Regra de ouro

O criativo precisa de 3 coisas:
1. **DADO/REFLEXÃO GENUINAMENTE INTERESSANTE**, algo que faz a pessoa parar e pensar, não algo que tenta vender disfarçado
2. **IMAGEM JORNALÍSTICA DE APOIO**, gráfico, infográfico, foto editorial, comparação visual. Reforça o dado
3. **CTA SUTIL**, aparece só no final, em cor forte, como um convite. Não como um botão de vendas

## Tipos de reflexão (variar nas 10 ideias)

- **Notícia real**, dado de pesquisa, estudo científico, notícia recente conectada ao nicho
- **Polêmica**, questionamento provocativo que desafia o senso comum do nicho
- **Conta maluca**, cálculo hipotético que prova um ponto de forma surpreendente (custo, tempo, comparação absurda)
- **Curiosidade**, fato surpreendente que ninguém sabe sobre o nicho
- **Comparação**, dois cenários lado a lado que mostram um contraste revelador

## Compliance de bom senso

- NÃO apelar pra medo de doença, morte ou consequências graves de saúde pra vender
- NÃO mencionar remédios, antidepressivos, medicamentos específicos
- NÃO mencionar condições de saúde mental (depressão, ansiedade) como argumento de venda
- NÃO criar contas que parecem manipulativas ou de mau gosto
- Manter o tom inteligente e respeitoso, nunca apelativo
- Se o dado envolve saúde, focar no lado positivo (benefícios de fazer) e não no negativo (horrores de não fazer)

## Fluxo da conversa

Siga os 4 passos abaixo em ordem.

### PASSO 1 — Briefing

Se existir `meus-produtos/.ativo` e o `perfil.md` do produto ativo, pergunte:

```
Usar dados do produto ativo ou informar manualmente?

1. Usar dados do produto ativo
2. Informar manualmente
```

Se o aluno escolher 1, leia `meus-produtos/{ativo}/perfil.md` e (se existir) `meus-produtos/{ativo}/idconsumidor.md`, extraia produto, nicho e público, e siga pro Passo 2.

Se o aluno escolher 2, ou se não existir produto ativo, pergunte direto:

- Qual o produto/serviço?
- Qual o público?

Pare e espere a resposta.

### PASSO 2 — 10 ideias de Reflexão Editorial

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de Reflexão Editorial do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Com base no briefing, gere 10 ideias. Cada ideia deve conter:

- **TÍTULO:** frase impactante com o dado/polêmica/curiosidade. Nicho claro
- **ÂNGULO:** tipo de reflexão (notícia, polêmica, conta maluca, curiosidade, comparação) + resumo do argumento
- **CTA SUTIL:** frase que convida sem pressionar, conectada ao produto/nicho

#### Distribuição obrigatória das 10 ideias

Pelo menos 2 contas malucas, 2 polêmicas, 2 notícias/dados reais, 2 curiosidades, 2 comparações.

#### Regras das ideias


- O objetivo é ser GENUINAMENTE INTERESSANTE, não comercial.
- Variar os tipos de reflexão (não fazer 10 contas malucas, por exemplo).
- Todos os títulos com nicho claro.
- CTA sempre sutil, quase um P.S.
- Respeitar compliance de bom senso (sem apelar pra medo de doença/morte).
- Sem travessão. Use vírgula, ponto final ou parênteses.

#### Apresentação

Mostre as 10 ideias numeradas de 1 a 10, separadas por `---`:

```
Aqui estão 10 ideias de Reflexão Editorial pro seu nicho.

---

**1.** (ângulo: notícia real / polêmica / conta maluca / curiosidade / comparação)
**TÍTULO:** [frase impactante com o dado/polêmica/curiosidade, nicho claro]
**ÂNGULO:** [tipo de reflexão + resumo do argumento]
**CTA SUTIL:** [frase que convida sem pressionar, conectada ao produto/nicho]

---

**2.** (ângulo: ...)
...

---

Escolha uma ideia.
```

### PASSO 3 — Desenvolvimento e aprovação

Após o aluno escolher um número de 1 a 10, anuncie. Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

```
🔍 Próximo passo: gerar legenda e desenvolvimento da reflexão. Tempo estimado: cerca de 30 segundos.
```

Gere duas coisas a partir da ideia escolhida:

#### Desenvolvimento da reflexão (texto curto da arte)

```
TÍTULO: "[dado/polêmica/curiosidade impactante]"

REFLEXÃO:
"[Texto curto, máximo 5-6 linhas, que desenvolve o argumento. Parágrafos curtos com espaço entre eles. Dados em negrito.]"

CTA: [frase sutil, convite, não pressão] 👉
```

#### Legenda pro Instagram (longa, desenvolve a reflexão completa)

A legenda é onde o argumento é desenvolvido por completo. Estrutura:

- **Lead impactante**, o dado/fato que para o scroll
- **Desenvolvimento**, 6-10 linhas curtas que constroem o argumento com dados, comparações, lógica. Tom de conversa inteligente
- **Virada**, o momento onde o argumento se conecta ao produto/nicho, de forma natural
- **CTA sutil**, convite pro link, quase como P.S., com emoji 👉

Tom da legenda: inteligente, editorial, provocativo. Não é vendedor. É alguém compartilhando uma reflexão que faz sentido.

#### Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) na legenda. Corrigir direto. Nunca mostrar versão bruta.

O texto da reflexão na arte e o CTA NÃO passam pela revisora (são conteúdo da arte com tom editorial específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, e tom inteligente, não vendedor.

#### Apresentação e aprovação

```
Pronto. Aqui está o desenvolvimento da sua Reflexão Editorial:

📌 IDEIA ESCOLHIDA (nº {numero_ideia} das 10)
TÍTULO: [título da ideia]
ÂNGULO: [tipo de reflexão + argumento]
CTA SUTIL: [cta da ideia]

📌 DESENVOLVIMENTO DA REFLEXÃO (texto da arte)
[bloco com TÍTULO + REFLEXÃO + CTA]

📝 LEGENDA PRO INSTAGRAM (longa, desenvolve a reflexão)
[legenda gerada, terminando com CTA sutil + 👉]

---
1. Aprovou? Eu gero o prompt da imagem.
2. Quero ajustar algo
3. Voltar e escolher outra ideia (das 10)
```

Se escolher 2, perguntar o que ajustar (legenda, descrição da imagem, CTA ou corpo do texto da arte) e refazer apenas a parte indicada.

Se escolher 3, apresentar a lista das 10 ideias novamente e perguntar o novo número.

### PASSO 4 — Prompt pronto pro ChatGPT

Quando o usuário aprovar, entregue:

**A) Legenda do Instagram**, texto final pronto pra colar.

**B) Prompt de Feed (4:5)**, texto pronto pra colar no ChatGPT. Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

Os placeholders são:
- `[TÍTULO IMPACTANTE]`: o título da ideia escolhida (dado/polêmica/curiosidade).
- `[REFLEXÃO CURTA — máximo 5-6 linhas]`: o texto curto que desenvolve o argumento na arte. Parágrafos curtos com espaço entre eles. Dados em negrito.
- `[DESCRIÇÃO DA IMAGEM]`: gráfico, infográfico comparativo, foto editorial, recorte de reportagem. Sempre com CONTRASTE VISUAL que reforça o dado. Pode ter legendas curtas embaixo.
- `[CTA SUTIL]`: frase sutil da ideia escolhida, convite, não pressão.

````
Cria pra mim uma arte de texto com imagem jornalística de apoio pra anúncio de Instagram. Estilo post editorial/reflexão com dado impactante. Fundo branco limpo.

REGRA CRÍTICA DE PROPORÇÃO E RESPIRO:
Todo o conteúdo (título, texto, imagem, CTA) deve ficar concentrado nos 80% SUPERIORES da arte. Os 20% inferiores são respiro puro, quase vazio (fundo branco). Nada pode ficar colado na borda inferior. O CTA fica no limite entre o conteúdo e o respiro, NUNCA no rodapé.

COMPOSIÇÃO (de cima pra baixo, tudo nos 75% superiores):

ZONA 1 — TÍTULO (topo):
"[TÍTULO IMPACTANTE]"
Fonte SANS-SERIF BOLD, preto puro.
REGRA CRÍTICA DE TAMANHO DO TÍTULO: o título é aproximadamente 1.5x o tamanho do corpo do texto. Visivelmente maior, mas não absurdamente maior. Se o corpo é tamanho 16, o título é tamanho 24. Proporcional, elegante. NÃO é 3x, 5x ou 8x maior.
Alinhado à esquerda com margem generosa (10-12%).

ZONA 2 — CORPO DO TEXTO:
"[REFLEXÃO CURTA — máximo 5-6 linhas]"
Fonte SANS-SERIF REGULAR, grafite escuro (#333333), tamanho médio, legível.
Dados e números em NEGRITO pra destacar.
Alinhado à esquerda. Parágrafos curtos com espaço entre eles.

ZONA 3 — IMAGEM JORNALÍSTICA DE APOIO:
[DESCRIÇÃO DA IMAGEM: gráfico, infográfico comparativo, foto editorial, recorte de reportagem. Sempre com CONTRASTE VISUAL que reforça o dado. Pode ter legendas curtas embaixo.]

ZONA 4 — CTA (final do conteúdo, ACIMA do respiro inferior):
"[CTA SUTIL] 👉"
Fonte SANS-SERIF BOLD, cor LARANJA VIVO (#E85D04), tamanho médio.
Se destaca claramente do texto pela cor forte.
Alinhado à esquerda, mesma margem.
NÃO parece botão. É texto em cor forte e negrito.
REGRA CRÍTICA: o CTA fica no final do bloco de conteúdo. ABAIXO dele, há pelo menos 15-20% da arte de RESPIRO VAZIO (fundo branco puro). O CTA nunca encosta no rodapé.

REGRAS DE DESIGN:
- Fundo 100% BRANCO, sem textura
- Título proporcionalmente maior que o corpo (1.5x, não mais)
- Todo conteúdo nos 75% superiores da arte
- 20% inferiores são respiro branco puro
- Corpo de texto curto com dados/números em negrito
- Imagem jornalística de apoio com contraste visual
- CTA em LARANJA VIVO (#E85D04)
- Margem generosa em TODOS os lados
- Parece matéria de revista editorial ou post de newsletter
- Clean, sóbrio, inteligente

REGRA DE LIMPEZA:
PROIBIDO: foto de perfil, @nome, estrelas, sparkles, molduras, elementos decorativos. Só texto + imagem editorial + CTA.

COMPLIANCE FACEBOOK ADS:
- Sem violência, sem conteúdo sensível
- Sem menção a doenças, remédios, medicamentos, condições de saúde mental ou física
- Sem linguagem que apele pra medo de doença ou morte

PROIBIDO usar travessão. Use vírgula ou ponto final.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Exact size reference: 1080x1350. SAFE ZONE: keep the bottom 12% of the image free of essential text and CTA, the Meta Ads feed overlay covers this area with the advertiser name and the "Saiba mais" button. LEGIBILITY: use as little text as possible on the art. All text must be large, bold, high contrast and easily readable on a small phone screen at arm's length. Never use small fonts, never shrink the font to fit more content, cut content instead.
````

Depois de entregar a legenda e o prompt Feed, pergunte:

```
1. Sim, gera o Stories também
2. Não, só o Feed
```

#### Prompt pro ChatGPT (formato Stories), se o aluno pedir

Esse é fixo. Não precisa preencher placeholders.

````
Agora cria a exata mesma arte, mesmo texto, mesma imagem, mesmo layout, só diagramada pro formato Stories.

O conteúdo continua nos 75% superiores com 25% de respiro na base. O título pode ter fonte levemente maior. A imagem de apoio pode ocupar mais espaço vertical.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920. SAFE ZONE: the background art fills the entire canvas, but all essential text, the headline and the CTA must stay inside the safe area. Keep the bottom 14% completely empty, it is covered by the native Meta Ads overlay and the "Saiba mais" button. Keep the top 12% and the right 15% free of critical text as well, covered by the profile bar and the action icons column. Never let text touch the edges.
````

Esse formato não tem animação (é texto estático).

### Gerar e salvar

Após a entrega dos prompts Feed e Stories, pergunte como o aluno quer gerar a imagem:

```
Como você quer gerar a imagem?

1. Colar no ChatGPT ou Gemini (grátis)
   Eu te entrego os prompts prontos. Você cola, gera as artes e salva.

2. Gerar agora pelo OpenRouter (tem custo)
   Eu mando o prompt direto pro modelo de imagem e já salvo o PNG na sua
   pasta. Custa centavos por imagem.

Digite o número:
```

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-reflexao-editorial-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-reflexao-editorial-{numero}.md`

Conteúdo do arquivo:

```markdown
# Reflexão Editorial nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**Título:** [título da ideia]
**Ângulo:** [tipo de reflexão + argumento]
**CTA sutil:** [cta da ideia]

## Desenvolvimento da reflexão (texto da arte)

TÍTULO: [título impactante]

REFLEXÃO:
[texto curto, máximo 5-6 linhas]

CTA: [frase sutil] 👉

## Legenda pro Instagram

[legenda longa, desenvolve a reflexão completa, terminando com CTA sutil + 👉]

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
4. (Se gerou Stories) Cole o **Prompt Stories** pra gerar a versão vertical da mesma arte.

## Banco completo (as 10 ideias geradas nesta sessão)

[Listar todas as 10 ideias geradas nesta sessão, com número, título, ângulo e CTA sutil, para o aluno usar depois sem precisar rodar a sub-skill de novo.]
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-reflexao-editorial-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-reflexao-editorial-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Reflexão Editorial salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-reflexao-editorial-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outra Reflexão Editorial com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Reflexão Editorial gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-reflexao-editorial-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-reflexao-editorial-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outra Reflexão Editorial com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-reflexao-editorial-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16. SAFE ZONE: keep the bottom 14% completely empty, it is covered by the native Meta Ads overlay and the "Saiba mais" button. Keep the top 12% and the right 15% free of critical text, covered by the profile bar and the action icons column. Reposition text and CTA if needed to respect these margins, without changing wording.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-reflexao-editorial-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-reflexao-editorial-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-reflexao-editorial-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-reflexao-editorial-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

#### Sub-fluxo "Animar em loop" (vídeo a partir da imagem gerada)

Sempre que uma imagem do criativo estiver pronta (Feed ou Stories), inclua a opção **"Animar em loop (vídeo)"** no menu final, logo depois das opções de geração de imagem.

Quando o aluno escolher animar, pergunte o caminho:

```
Como você quer animar?

1. Colar o prompt numa ferramenta externa (Freepik/Magnific)
2. Higgsfield direto por aqui (conector do Claude)
3. Automático via Replicate (API)

Digite o número:
```

Antes de mostrar o menu, verifique a disponibilidade e marque na própria linha:

- **Linha 2 (Higgsfield):** disponível se existir alguma ferramenta MCP com "higgsfield" no nome nesta sessão. Se não existir, escreva a linha como "2. Higgsfield direto por aqui (não conectado, eu te ajudo a conectar)". Se o aluno escolher assim mesmo, acione a skill `configurar-higgsfield` e retome este sub-fluxo depois.
- **Linha 3 (Replicate):** disponível se `REPLICATE_API_TOKEN` existir no `.env` da raiz. Se não existir, escreva a linha como "3. Automático via Replicate (precisa de chave, eu te ajudo a criar)". Se o aluno escolher assim mesmo, acione a skill `configurar-replicate` e retome este sub-fluxo depois.

**Opção 1. Colar o prompt numa ferramenta externa:** entregue o Prompt de Animação do formato. Se este formato não tiver seção própria de Prompt de Animação, use o prompt padrão abaixo. Instrua: "Abra o Freepik (Magnific) no modo vídeo, suba a imagem gerada e defina a MESMA imagem como quadro inicial e quadro final, isso fecha o loop sem salto. Cole o prompt e gere. Modelo recomendado: Google Veo Lite, melhor custo-benefício." Se o aluno for usar outro modelo de vídeo, adapte o prompt às características dele antes de entregar (instruções mais restritivas ou prompt negativo, quando o modelo aceitar).

**Opção 2. Higgsfield pelo conector:** use as ferramentas MCP do Higgsfield para gerar o vídeo image-to-video: envie a imagem gerada e o prompt de animação (o do formato, ou o padrão abaixo), pedindo loop com a mesma imagem como quadro inicial e quadro final quando a ferramenta aceitar. Salve o vídeo na pasta de criativos com o sufixo `-loop.mp4`, no mesmo padrão da Opção 3. Requer assinatura ativa do Higgsfield.

**Opção 3. Automático via Replicate (API):** execute:

a) Grave o prompt de animação num arquivo `.txt` na pasta de criativos, com o nome `prompt-reflexao-editorial-{numero}-loop.txt`. Use o Prompt de Animação do formato; se não houver, use o prompt padrão abaixo.

b) Anuncie:

```
🔍 Próximo passo: animar a imagem em loop via API. Tempo estimado: 3 a 5 minutos.
```

c) Rode o script. Ele fecha o loop sozinho, mandando a mesma imagem como quadro inicial e quadro final:

```bash
py -3 scripts/animar-criativo.py --image "meus-produtos/{ativo}/entregas/criativos/criativo-reflexao-editorial-{numero}-feed.png" --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-reflexao-editorial-{numero}-loop.txt" --out "meus-produtos/{ativo}/entregas/criativos/criativo-reflexao-editorial-{numero}-loop.mp4"
```

Para animar a versão Stories, troque `-feed.png` por `-stories.png` no `--image` e o sufixo do `--out` para `-stories-loop.mp4`.

d) Confirme:

```
✅ Concluído: vídeo em loop gerado e salvo.

Vídeo: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-reflexao-editorial-{numero}-loop.mp4
```

**Prompt padrão de animação em loop** (só quando o formato não tem Prompt de Animação próprio):

```
Anima essa imagem em loop com um movimento sutil e elegante. APENAS o fundo e os elementos visuais se mexem. Os textos ficam 100% ESTÁTICOS, não se movem em nenhum momento.

MOVIMENTO DA CENA: micro-movimento de respiração na imagem (leve zoom in/out de 1-2% no eixo central), com leve parallax horizontal se houver fundo. Sem cortes, sem panning agressivo. Loop suave de 3 a 5 segundos: o último frame emenda no primeiro sem salto perceptível.

REGRA CRÍTICA: todo texto na imagem (título, legenda, CTA) é ESTÁTICO. Não balança, não aparece com animação, não se move. Só os elementos visuais por trás é que respiram.

NÃO INVENTA: não adiciona nenhum elemento que não existe na imagem original. Nada de objeto novo, pessoa nova, texto novo, logo, partícula ou efeito que não estava lá. Anima somente o que já existe.

SE HOUVER PESSOA NA IMAGEM: sem falas, sem diálogo, sem movimento labial. A pessoa não conversa com a câmera. Apenas o movimento descrito acima.
```

Nem todo criativo vale animar: quanto mais texto na arte, maior a chance de o modelo remover, alterar ou inventar texto no vídeo. Em formato de texto pesado, avise o aluno desse risco antes de gerar. Se o vídeo vier com texto distorcido ou tremido, gere de novo uma vez. Se persistir, avise que essa imagem não anima bem e sugira manter a versão estática.

## Regras

- **CTA:** o padrão é "Saiba mais", que é o botão nativo do Meta Ads. Se o aluno indicou outro em qualquer momento, usar esse. Nunca inventar CTA. Nunca usar "Link na bio" nem "Clique no link da bio", porque em anúncio pago o clique acontece no botão nativo, não na bio.
- **Perguntar o CTA antes de gerar:** se o aluno ainda não indicou a chamada, pergunte antes de montar a legenda e os prompts:

  ```
  Qual chamada você quer no criativo?

  1. Saiba mais (padrão do Meta Ads)
  2. Cadastre-se
  3. Comprar agora
  4. Outra (me diga qual)

  Digite o número:
  ```

  Se o aluno já indicou o CTA antes, não repita a pergunta, apenas confirme em uma linha.
- **Zona segura no formato Stories/Reels:** o rodapé 14% fica vazio, é onde o Meta Ads sobrepõe o nome do anunciante e o botão "Saiba mais". O topo 12% e a lateral direita 15% ficam livres de texto crítico, cobertos pela barra de perfil e pela coluna de ícones. Texto nunca encosta na borda.
- **Texto legível na arte:** pouco texto e fonte grande. Todo texto da arte precisa ser lido com facilidade na tela de um celular, a um braço de distância. Se o conteúdo não couber com fonte grande, corte conteúdo, nunca diminua a fonte. Título e CTA sempre em alto contraste com o fundo.

### Sobre as ideias
- O objetivo é ser GENUINAMENTE INTERESSANTE, não comercial.
- Variar tipos: notícia real, polêmica, conta maluca, curiosidade, comparação.
- Distribuição obrigatória: pelo menos 2 contas malucas, 2 polêmicas, 2 notícias/dados reais, 2 curiosidades, 2 comparações.
- Todos os títulos com nicho claro.
- CTA sempre sutil, quase um P.S.
- Respeitar compliance de bom senso.

### Sobre o título da arte
- Tamanho 1.5x o corpo do texto (não 3x, não 8x).
- Proporcionalmente maior, elegante, não gigante.
- Fonte bold, preto puro.

### Sobre o corpo do texto da arte
- CURTO: máximo 5-6 linhas.
- Dados e números em negrito.
- Parágrafos curtos com espaço entre eles.
- Grafite escuro, fonte regular, legível.

### Sobre a imagem de apoio
- Jornalística/editorial: gráfico, infográfico, foto editorial, recorte de reportagem.
- Sempre com CONTRASTE VISUAL que reforça o dado.
- Pode ter legendas curtas.
- Estilo clean, minimalista, de revista.

### Sobre o CTA da arte
- LARANJA VIVO (#E85D04), fonte bold.
- Sutil, texto em cor forte, não parece botão.
- Fica no final do conteúdo, NUNCA no rodapé.
- 20-25% de respiro branco ABAIXO do CTA.

### Sobre proporção e respiro
- Todo conteúdo nos 80% SUPERIORES da arte.
- 20% inferiores são respiro branco puro.
- Margem generosa em todos os lados (10-12%).
- Nada colado nas bordas.

### Sobre a legenda do Instagram
- Longa, desenvolve o argumento completo.
- Tom inteligente, editorial, provocativo.
- Não é vendedor, é alguém compartilhando uma reflexão.
- CTA sutil no final, quase P.S.
- Emoji 👉

### Compliance
- Sem menção a doenças, remédios, medicamentos, saúde mental.
- Sem apelar pra medo de doença ou morte.
- Sem linguagem sensacionalista de saúde.
- Tom inteligente e respeitoso, nunca apelativo.
- Compliance Facebook Ads: sem violência, sem conteúdo sensível.

### Sobre Light Copy (legenda)
- Light Copy obrigatória na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- **Exceção documentada: emoji no CTA da legenda.** O Manual da Copy proíbe emojis em geral, mas a legenda da Reflexão Editorial termina com emoji 👉 no CTA porque integra o padrão editorial/conversacional do formato. Essa exceção vale SOMENTE para o CTA da legenda.
- Produto NÃO aparece no lead da legenda.
- O texto da reflexão na arte e o CTA seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar a legenda.

### Sem animação
- Este formato é texto estático. Não tem prompt de animação pro Freepik (Magnific).

### Operacional
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
- PROIBIDO travessão. Use vírgula ou ponto final.
