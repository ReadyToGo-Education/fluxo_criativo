# Problema × Solução Emoji. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 28 (Problema × Solução Emoji). Gera um grid comparativo minimalista e premium: 4 dores reais do público à esquerda (com emojis) pareadas com 4 dicas úteis à direita. Gera 5 variações (cada uma explorando um ângulo de dor diferente), o aluno escolhe uma, e a sub-skill entrega título, legenda e três prompts prontos (Feed, Stories e animação no Freepik).

**Diferença pro formato 7 (Problema-Solução):** o formato 7 é arte dividida ao meio, estética UGC brasileira, foto de creator, foco antes/depois com uma única dor. Este formato (28) é grid de 4 linhas, estética editorial minimalista premium (Apple, Aesop), emojis como gatilho visual, foco em valor de conteúdo. São formatos distintos; quando o aluno disser só "problema solução" sem citar emoji ou grid, use o formato 7.

**Por que esse formato funciona:**
O grid de 4 pares é entendido em 2 segundos: "são problemas comuns e dicas úteis pra cada um". Os emojis contam a história da dor antes do texto, então o leitor se identifica no scroll. Cada solução é uma dica real entregue de graça, o que faz o leitor pensar "se o conteúdo grátis já é assim, imagina o pago". A estética premium tira a cara de panfleto e constrói autoridade.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug).
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço. É o dado central deste formato.
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho.
- **Dores reais**: das Urgências Ocultas (categoria DORES) do `perfil.md` e das objeções/paliativos do `idconsumidor.md`, se houver. Essas dores alimentam os problemas das variações.
- **Método / abordagem do produto**: o vocabulário do método da Furadeira do `perfil.md`, se houver. As soluções usam esse vocabulário quando existir.

### 1. Apresentar resumo do contexto e confirmar

SEMPRE mostre o resumo, mesmo se algum campo veio de inferência. Marque o que é real e o que foi inferido:

```
Vou usar estes dados do seu produto ativo ({slug}):

Produto: [nome do produto]
Nicho: [nicho]
Público: [resumo do público]
Método / abordagem: [método do produto, se houver]

(Marque "✓ do perfil" pros campos extraídos diretamente do perfil.md ou idconsumidor.md.
Marque "○ inferido" pros campos que foram um chute a partir do slug, tipo ou preço.)

Está tudo certo?

1. Sim, está certo, pode seguir
2. Quero ajustar algum campo
```

**Se escolher 1**, pular pra etapa 2 (Geração das 5 variações).

**Se escolher 2**, perguntar qual campo ajustar e refazer só a parte indicada. Pergunta de ajuste com exemplos do mesmo universo do produto ativo (NUNCA genéricos):

```
Qual é o seu nicho?
(ex: [3 exemplos do mesmo universo do produto ativo])
```

Se o aluno não especificou público, assumir um plausível brasileiro com base no nicho e avisar antes de gerar as variações. Não travar o fluxo.

### 2. Geração das 5 variações

Anuncie:

```
🔍 Próximo passo: gerar 5 variações de Problema × Solução com emoji pro seu nicho. Tempo estimado: cerca de 60 segundos.
```

Cada variação tem 4 linhas (4 problemas + 4 soluções + emojis). As 5 variações exploram ÂNGULOS DE DOR diferentes:

- Variação 1: problemas do DIA A DIA (situações cotidianas).
- Variação 2: problemas EMOCIONAIS (frustrações, medos, vergonhas).
- Variação 3: problemas de TEMPO / PRATICIDADE (correria, falta de tempo).
- Variação 4: problemas SOCIAIS (situações com outras pessoas, julgamento).
- Variação 5: problemas de RESULTADO (o que acontece quando não resolve).

**Regras dos problemas:**
- Situações REAIS e ESPECÍFICAS do dia a dia, nunca genéricas. Frase curta (máximo 5 a 6 palavras).
- Imediatamente reconhecíveis pelo público, em linguagem coloquial, como a pessoa fala na vida real.

Errado: "Dificuldades com a pele" (genérico). Certo: "Pele seca na viagem" (específico, situacional).

**Regras das soluções:**
- NÃO são nomes de produto. São DICAS REAIS E ÚTEIS, ensinamentos práticos que a pessoa já consegue usar.
- Frase curta e direta (máximo 6 a 8 palavras), específica o suficiente pra ser útil.
- Quando o produto tem método específico, a dica usa o vocabulário desse método.
- Sem travessão.

Errado: "Ebook Protocolo Endo" (venda). Certo: "Chá de gengibre + cúrcuma antes de dormir" (dica real).

**Regras dos emojis:**
- 2 a 3 emojis por linha, que ILUSTRAM a situação e contam a história sozinhos.
- Expressivos e visuais, nunca genéricos (nada de 👍 ou ❤️ pra tudo).
- DIFERENTES entre as 4 linhas, sem repetir emoji.

#### Formato da listagem

Apresente as 5 variações em texto. Não descreva o layout visual ainda (entra quando o aluno escolher).

```
Aqui estão 5 variações de Problema × Solução com emoji pro seu nicho.

**Variação 1. Dia a dia**
1. [emojis] [problema] → [solução]
2. [emojis] [problema] → [solução]
3. [emojis] [problema] → [solução]
4. [emojis] [problema] → [solução]

**Variação 2. Emocional**
[mesmo formato]

... até a Variação 5 (Resultado).

---
Qual variação você quer transformar em criativo?
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

### 3. Escolha e geração do criativo

Após o aluno escolher uma variação, anuncie:

```
🔍 Próximo passo: gerar título, legenda e os prompts. Tempo estimado: cerca de 30 segundos.
```

Gere quatro coisas a partir da variação escolhida:

#### A) Título do anúncio

Curto, conecta com o tema das dores da variação, Light Copy aplicada. Sem travessão, sem exclamação, sem pergunta, sem promessa vaga, sem "não é X. É Y.". Produto não aparece no lead.

#### B) Legenda pro Instagram

2 a 3 linhas. Reforça o valor das dicas e gera curiosidade. Termina com a chamada do CTA escolhido, padrão **"Saiba mais"**. Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.** O prompt é CURTO, DESCRITIVO e CONCEITUAL: descreve o que se quer VER, não como construir. Deixa o GPT interpretar o layout.

````
Cria pra mim um infográfico minimalista e premium de problema e solução pra Instagram sobre [NICHO]. Quatro linhas, cada uma mostrando um problema comum à esquerda com emojis grandes e expressivos, e uma dica prática à direita em cards de tom suave. Os pares de problema e solução: [LISTAR AS 4 LINHAS, CADA UMA COM EMOJIS, PROBLEMA E SOLUÇÃO]. No topo, o nome do nicho como título: "[NICHO]". Embaixo, um CTA suave: "[CTA DE VALOR] →". Estilo de direção de arte de marca premium, vibe Apple e Aesop, design editorial minimalista, muito respiro, paleta [CORES SUAVES E SOFISTICADAS], nada de panfleto de farmácia, nada de oferta agressiva. Tipografia sans-serif limpa e legível em celular. Sem travessão em nenhum texto. IMPORTANT: exact 4:5 Instagram feed aspect ratio. Exact size reference: 1080x1350. SAFE ZONE: keep the bottom 12% of the image free of essential text and CTA, the Meta Ads feed overlay covers this area with the advertiser name and the "Saiba mais" button. LEGIBILITY: use as little text as possible on the art. All text must be large, bold, high contrast and easily readable on a small phone screen at arm's length. Never use small fonts, never shrink the font to fit more content, cut content instead.
````

#### D) Prompt pro ChatGPT (formato Stories)

Esse é fixo. Não precisa preencher placeholders.

````
Agora cria a exata mesma arte, mesmas 4 linhas, mesmos emojis, mesmas cores, mesmo texto, só diagramada pro formato Stories, com espaçamento vertical generoso pra ocupar a tela inteira.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Exact size reference: 1080x1920. SAFE ZONE: the background art fills the entire canvas, but all essential text, the headline and the CTA must stay inside the safe area. Keep the bottom 14% completely empty, it is covered by the native Meta Ads overlay and the "Saiba mais" button. Keep the top 12% and the right 15% free of critical text as well, covered by the profile bar and the action icons column. Never let text touch the edges.
````

#### E) Prompt de Animação pro Freepik (Magnific)

Texto curto (2 a 3 frases) pra animar a imagem do Stories. Foco apenas em movimento e transição, não repete a descrição da arte.

````
Anima essa imagem mantendo as 4 linhas, todos os emojis, os textos de problema e solução, o título e o CTA 100% estáticos e legíveis. APENAS um leve fade ou entrada suave linha por linha, de cima pra baixo, em loop calmo de 4 a 6 segundos, como se cada par problema e solução aparecesse na sequência. Nada de texto balança ou some depois de aparecer. Trilha instrumental minimalista e elegante de fundo, sem letra.
````

### 4. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) no título e na legenda. Corrigir direto. Nunca mostrar versão bruta.

Os textos de problema, solução e o CTA NÃO passam pela revisora (são conteúdo da arte), mas respeitam Light Copy: sem travessão, sem exclamação, problemas específicos e soluções úteis e concretas.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Problema × Solução Emoji:

📌 VARIAÇÃO ESCOLHIDA (nº {numero_variacao} das 5, ângulo: {angulo})
[listar as 4 linhas com emojis, problema e solução]

📌 TÍTULO DO ANÚNCIO
[título gerado]

📝 LEGENDA PRO INSTAGRAM
[legenda gerada terminando na chamada do CTA escolhido]

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

🎬 PROMPT DE ANIMAÇÃO PRO FREEPIK (MAGNIFIC)
[prompt de animação, dentro de bloco de código]

📱 PROMPT PRO CHATGPT, FORMATO STORIES
[prompt Stories, dentro de bloco de código]

---
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher outra variação (das 5)
```

Se escolher 2, perguntar o que ajustar (título, legenda, problemas, soluções, emojis ou CTA) e refazer apenas a parte indicada.

Se escolher 3, apresentar as 5 variações de novo e perguntar o novo número.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-problema-solucao-emoji-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-emoji-{numero}.md`

Conteúdo do arquivo:

```markdown
# Problema × Solução Emoji nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Variação escolhida (nº {numero_variacao} das 5, ângulo: {angulo})

[listar as 4 linhas com emojis, problema e solução]

## Título do anúncio

[título]

## Legenda pro Instagram

[legenda terminando na chamada do CTA escolhido]

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt de Animação pro Freepik (Magnific) (serve pro Feed e pro Stories)

\`\`\`
[prompt de animação preenchido]
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
5. Pra animar, abra o Freepik (Magnific), suba a imagem gerada e cole o **Prompt de Animação**. O mesmo prompt serve pro Feed e pro Stories. No modo vídeo do Magnific, defina a MESMA imagem como quadro inicial e quadro final, isso fecha o loop sem salto. Modelo recomendado: Google Veo Lite (melhor custo-benefício).

## Banco completo (as 5 variações geradas nesta sessão)

Liste aqui todas as 5 variações geradas nesta sessão, pra o aluno usar depois sem rodar a sub-skill de novo.
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

3. Grave o Prompt Feed num arquivo `.txt` na pasta de criativos, com o nome `prompt-problema-solucao-emoji-{numero}-feed.txt`. Conteúdo é o Prompt Feed apresentado ao aluno, sem alterações.

4. Anuncie e rode o script no formato Feed (4:5):

```
🔍 Próximo passo: gerar a imagem do Feed via API. Tempo estimado: 2 a 3 minutos.
```

Use o comando Python correto da sessão (`python3` ou `py -3`), conforme a seção Execução de Scripts Python do CLAUDE.md.

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-problema-solucao-emoji-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-emoji-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image).

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Problema × Solução Emoji salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-problema-solucao-emoji-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Problema × Solução Emoji com outra das 5 variações
2. Trocar o nicho ou público e gerar 5 variações novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Problema × Solução Emoji gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-problema-solucao-emoji-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-problema-solucao-emoji-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Problema × Solução Emoji com outra das 5 variações
3. Trocar o nicho ou público e gerar 5 variações novas
4. Voltar e escolher outro formato de criativo
```

#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-problema-solucao-emoji-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same 4 rows, same emojis, same colors, same text content, same problems and solutions, same title, same CTA, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16. SAFE ZONE: keep the bottom 14% completely empty, it is covered by the native Meta Ads overlay and the "Saiba mais" button. Keep the top 12% and the right 15% free of critical text, covered by the profile bar and the action icons column. Reposition text and CTA if needed to respect these margins, without changing wording.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-problema-solucao-emoji-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-emoji-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-emoji-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-problema-solucao-emoji-{numero}-stories.png
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

a) Grave o prompt de animação num arquivo `.txt` na pasta de criativos, com o nome `prompt-problema-solucao-emoji-{numero}-loop.txt`. Use o Prompt de Animação do formato; se não houver, use o prompt padrão abaixo.

b) Anuncie:

```
🔍 Próximo passo: animar a imagem em loop via API. Tempo estimado: 3 a 5 minutos.
```

c) Rode o script. Ele fecha o loop sozinho, mandando a mesma imagem como quadro inicial e quadro final:

```bash
py -3 scripts/animar-criativo.py --image "meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-emoji-{numero}-feed.png" --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-problema-solucao-emoji-{numero}-loop.txt" --out "meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-emoji-{numero}-loop.mp4"
```

Para animar a versão Stories, troque `-feed.png` por `-stories.png` no `--image` e o sufixo do `--out` para `-stories-loop.mp4`.

d) Confirme:

```
✅ Concluído: vídeo em loop gerado e salvo.

Vídeo: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-problema-solucao-emoji-{numero}-loop.mp4
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

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda.
- Os textos de problema, solução e o CTA seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- **NUNCA use travessão** em nenhum texto da skill. Use vírgula ou ponto final no lugar.
- **Problemas específicos e situacionais**, em linguagem coloquial, máximo 5 a 6 palavras. Nunca genéricos.
- **Soluções são dicas reais e úteis**, não nomes de produto, máximo 6 a 8 palavras. Quando o produto tem método específico, usam o vocabulário desse método.
- **Emojis expressivos**, 2 a 3 por linha, diferentes entre as 4 linhas, contando a história da dor sozinhos.
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês (gatilhos eficazes pro gerador de imagem).
- **É conteúdo de valor, não venda.** O CTA é sempre suave (ex: "Clique aqui e entenda", "Saiba mais", "Veja o guia completo"). PROIBIDO CTA comercial ou de escassez ("compre agora", "garanta sua vaga", "últimas vagas", "oferta por tempo limitado").

### Regras de segurança e compliance

- Nunca usar marcas reais de concorrentes, logos, fotos de pessoas reais identificáveis, celebridades, propriedades intelectuais protegidas, claims médicos não comprovados, diagnósticos ou prescrições, nem comparação direta com produto concorrente real nomeado.
- As dicas são seguras, baseadas em conhecimento geral do nicho, nunca substituindo orientação profissional quando aplicável. Sempre usar versões genéricas e seguras.
- Compliance Facebook Ads: sem nudez, sensualização ou violência.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica, solução, situação.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
