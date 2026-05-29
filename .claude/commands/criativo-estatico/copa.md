# Copa / Futebol. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 25 (Copa / Futebol). Conecta QUALQUER nicho ao universo do futebol e da Copa do Mundo. Gera 10 ideias com distribuição emocional (2 desejo, 2 medo, 2 oportunidade, 2 curiosidade, 2 prova), o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
Conectar o nicho ao universo do futebol gera um anúncio que parece campanha antes de parecer anúncio. A metáfora visual com vestiário, troféu, VAR, prancheta ou narração esportiva ativa identificação coletiva e impacto memorável estilo Cannes Lions, sem precisar de oferta agressiva.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço (ex: "automação com IA pra pequenos negócios", "preparação pra concurso PRF", "inglês pra atletas").
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

**Se escolher 1**, pular pra etapa 2 (Identificar equivalente futebolístico + gerar 10 ideias).

**Se escolher 2**, perguntar qual campo ajustar e refazer só a parte indicada.

**Pergunta de ajuste (caso aluno escolha 2)**, com exemplos do nicho do produto ativo:

```
Qual é o seu produto e nicho?
(ex: [3 exemplos do mesmo universo do produto ativo])
```

**IMPORTANTE: os exemplos NUNCA podem ser genéricos.** Antes de fazer a pergunta, construa 3 exemplos do mesmo universo do produto ativo:

- Automação/IA: "Mentoria de Automações com IA pra criadores", "Curso de Agentes GPT pra atendimento", "Treinamento de N8N pra agências"
- Concurso/PRF: "Curso preparatório pra PRF", "Mentoria de redação pra concursos", "Pacote de questões comentadas pra PF"
- Inglês: "Curso de Inglês Fluente em 90 dias", "Mentoria de Conversação pra Executivos", "Plataforma de Inglês pra Atletas"
- Tarot: "Curso de Tarot online pra iniciantes", "Mentoria de Leitura de Cartas pra terapeutas", "Ebook de Tarô pra autoconhecimento"
- Tráfego: "Mentoria de Tráfego Pago pra criadores", "Curso de Anúncios no Meta pra agências", "Consultoria de Performance pra ecommerce"
- Emagrecimento: "Programa de Emagrecimento em 90 dias", "Mentoria de Reeducação Alimentar", "Plano de Treino pra Mulheres 40+"
- Último recurso (se realmente não der pra inferir nicho): "Mentoria de tráfego pago pra criadores", "Curso de inglês pra atletas", "Programa de emagrecimento em 90 dias"

Se o aluno não especificou público, assumir um plausível com base no produto/nicho e avisar antes de gerar as 10 ideias:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Identificar equivalente futebolístico + gerar 10 ideias

Anuncie:

```
🔍 Próximo passo: identificar o equivalente futebolístico do seu nicho e gerar 10 ideias de criativo. Tempo estimado: cerca de 60 segundos.
```

#### 2a. Identificar o equivalente futebolístico

Mapeie o nicho para o universo do futebol. Use a tabela abaixo como referência, mas crie conexões originais quando necessário:

| Nicho | Equivalente Futebolístico |
|---|---|
| Concurso | Convocação |
| PRF | Seleção dos aprovados |
| Inglês | Liga internacional |
| Emagrecimento | Pré-temporada |
| Investimentos | Tabela do campeonato |
| LinkedIn | Olheiro |
| Marketing | Técnico |
| Academia | Centro de treinamento |
| Homeopatia | Recuperação de atleta |
| Artesanato | Talento revelado |
| Dentista | Preparação pra final |
| Terapia | Treinador mental |
| Emprego | Convocação |
| Tarot | Leitura do jogo |
| Automação/IA | Reforço técnico do time |
| Tráfego pago | Olheiro dos craques |
| Cafeteria | Pré-jogo da torcida |
| Vendas | Centroavante artilheiro |

Pra nichos não listados, crie uma metáfora original e coerente. Anuncie internamente qual é o equivalente antes de gerar as ideias (sem mostrar pro aluno ainda, isso aparece dentro de cada ideia).

#### 2b. Distribuição emocional obrigatória

As 10 ideias devem seguir exatamente esta distribuição:

- 2 ideias de **DESEJO** (mostrar o resultado, a conquista, o after)
- 2 ideias de **MEDO** (mostrar o custo de não agir, o risco)
- 2 ideias de **OPORTUNIDADE** (timing, janela, momento único)
- 2 ideias de **CURIOSIDADE** (gerar inquietação, pergunta mental)
- 2 ideias de **PROVA** (resultado, números, credibilidade)

#### 2c. Regra de diversidade visual

As 10 ideias devem usar mecanismos visuais COMPLETAMENTE DIFERENTES entre si. Não pode haver duas com o mesmo elemento visual principal:

- Se uma usa camisa pendurada, nenhuma outra usa camisa
- Se uma usa VAR, nenhuma outra usa VAR
- Se uma usa troféu, nenhuma outra usa troféu
- Se uma usa campo, nenhuma outra usa campo como cenário principal

Cada ideia explora um território visual único: vestiário, prancheta, narração, transmissão, comemoração, treino, túnel de entrada, banco de reservas, juiz, bandeirinha, pênalti, escanteio, sala de imprensa, ônibus do time, etc.

#### 2d. Regra de ouro. Nicho reconhecível em 2 segundos

O nicho precisa ser entendido em menos de 2 segundos. Teste: se eu remover TODO o texto da imagem, uma pessoa ainda consegue entender o nicho? Se não, refaça a ideia.

O nicho aparece através de elementos visuais concretos e específicos do universo do produto:

| Nicho | Elementos visuais obrigatórios (exemplos) |
|---|---|
| PRF | Distintivo, viatura, uniforme, radar, apostila |
| Inglês | Frases em inglês, passaporte, bandeiras, entrevista |
| Artesanato | Linhas, agulhas, crochê, bordado, peças artesanais |
| Investimentos | Gráficos, moedas, calculadora, cofre |
| Emagrecimento | Fita métrica, balança, roupas largas, espelho |
| Tarot | Cartas espalhadas, velas, cristais, mesa mística |
| Automação/IA | Notebook, tela com fluxo, ícones de robô, gráfico crescente |
| Cafeteria | Xícara de cerâmica, café fumegante, máquina espresso, balcão |

O nicho NUNCA pode ficar escondido apenas no CTA ou no texto.

#### 2e. Regra do nome do nicho visível

O NOME do nicho deve aparecer como texto legível na cena ou na headline de TODA ideia. Não basta ter objetos do nicho. A palavra precisa estar escrita e visível (no uniforme, numa placa, num livro, na headline, em qualquer elemento textual da composição).

Exemplos:
- Se o nicho é "PRF", as letras "PRF" têm que ser lidas na imagem
- Se o nicho é "Inglês", a palavra "Inglês" ou frase em inglês aparece visível
- Se o nicho é "Artesanato", a palavra "Artesanato" aparece na cena
- Se o nicho é "Feng Shui", a palavra "Feng Shui" aparece numa placa ou livro

#### 2f. Formato de cada ideia

```
IDEIA [número] — [EMOÇÃO]

Conceito: [a metáfora central em uma frase]
Cena: [descrição visual detalhada da imagem]
Headline: [frase principal do anúncio]
Texto de apoio: [complemento da headline]
CTA: [chamada pra ação]
```

#### 2g. Estilo criativo

Pense como Diretor de Criação premiado, Cannes Lions, Nike, Apple, Heineken. NÃO pense como copywriter de panfleto, banner promocional, oferta agressiva. A prioridade é a IDEIA. Depois a venda.

#### 2h. Apresentação

Mostre as 10 ideias numeradas de 1 a 10, agrupadas pela emoção:

```
Identifiquei o equivalente futebolístico do seu nicho: [equivalente].

Aqui estão 10 ideias de criativo Copa / Futebol pro seu nicho.

✨ DESEJO

1. IDEIA 1 — DESEJO
   Conceito: [conceito]
   Cena: [descrição]
   Headline: [headline]
   Texto de apoio: [texto]
   CTA: [CTA]

2. IDEIA 2 — DESEJO
   (...)

⚠️ MEDO

3. IDEIA 3 — MEDO
   (...)

4. IDEIA 4 — MEDO
   (...)

⏳ OPORTUNIDADE

5. IDEIA 5 — OPORTUNIDADE
   (...)

6. IDEIA 6 — OPORTUNIDADE
   (...)

🤔 CURIOSIDADE

7. IDEIA 7 — CURIOSIDADE
   (...)

8. IDEIA 8 — CURIOSIDADE
   (...)

📊 PROVA

9. IDEIA 9 — PROVA
   (...)

10. IDEIA 10 — PROVA
    (...)

---
Qual ideia você quer transformar em criativo?
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

### 3. Geração do prompt do criativo

Após o aluno escolher um número de 1 a 10, anuncie:

```
🔍 Próximo passo: gerar legenda e os prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

Gere três coisas a partir da ideia escolhida:

#### A) Legenda pro Instagram

2 a 4 linhas. Conecta a metáfora futebolística ao nicho sem entregar tudo. Termina com **"Link na bio"** se o produto for de captação ou ofertas pagas. Light Copy aplicada (sem travessão, sem exclamação, sem pergunta no início, sem promessa vaga).

A legenda NÃO precisa repetir a headline da arte. Ela complementa, dá contexto ou puxa pra ação.

#### B) Prompt pro ChatGPT (formato Feed)

Use o estilo simples e direto descrito abaixo, substituindo os placeholders pelos dados da ideia escolhida. **O texto final ao usuário não pode ter colchetes.**

REGRAS DE ESCRITA DO PROMPT:
- Frases curtas, uma instrução por linha
- Sem headers, sem numeração, sem bullets dentro do prompt
- Sem estrutura pesada (nada de "1. Estilo visual:", "2. Composição:")
- Texto corrido fluindo naturalmente: formato → estilo → cena → elementos → o que NÃO incluir → iluminação → textos → hierarquia
- Usar negativas explícitas ("No people.", "No brands.", "No logos.")
- Descrever a cena como se estivesse dirigindo um fotógrafo
- O GPT Images renderiza melhor com prompts limpos e diretos do que com prompts ultra-estruturados

REGRAS DE TEXTO E CTA (obrigatórias em TODO prompt):

- Todos os textos devem ter alto contraste com o fundo (branco sobre escuro ou escuro sobre claro)
- Fonte grande, bold, sem serifa, limpa
- Se necessário, usar faixa de fundo sólido ou semitransparente atrás do texto pra garantir leitura
- Headline ocupa posição de destaque com tamanho generoso
- Nenhum texto pode competir com o fundo ou se perder na composição
- O CTA é um botão com fundo sólido e contrastante (não semitransparente, não sutil), cor vibrante (dourado forte, branco sólido, amarelo vivo), tamanho menor que a headline mas grande o suficiente pra ser notado imediatamente
- Sempre incluir as duas frases obrigatórias no final do prompt:
  - "All text must be large, bold, high contrast and immediately readable."
  - "CTA button must be visually prominent with solid contrasting background, not subtle or transparent."

Template do prompt Feed (preencher cada `[ ]` e remover os colchetes):

````
Instagram Feed 4:5 (1080x1350).
Ultra realistic advertising photography, Cannes Lions award-winning campaign.
[Descrição da cena em 1 a 2 frases curtas, baseada na Cena da ideia escolhida].
[Frase descrevendo a atmosfera ou ambientação, ex: "The locker room is elegant, dramatic and cinematic."].
[Frase descrevendo os elementos do nicho na cena, ex: "Several generic yellow jerseys hang neatly inside wooden lockers."].
[Frase com o elemento dominante do nicho, ex: "In the center, a single PRF badge hangs among the jerseys."].
[Frase reforçando que o elemento do nicho é visível e reconhecível, ex: "The badge must be visually dominant and immediately recognizable."].
The word "[nome do nicho em português]" must appear visibly written on [placa, uniforme, livro, headline, etc].
No people.
No brands.
No logos.
No real club crests.
No real player names or numbers.
Warm cinematic lighting from above.
TEXT HIERARCHY:
Main Headline:
[headline da ideia escolhida]
Supporting Text:
[texto de apoio da ideia escolhida]
CTA Button:
[CTA da ideia escolhida] →
All text must be large, bold, high contrast and immediately readable.
CTA button must be visually prominent with solid contrasting background, not subtle or transparent.
````

#### C) Prompt pro ChatGPT (formato Stories)

Esse é fixo, sem placeholders. Reorganiza a composição, textos e elementos pra tela cheia vertical, mantendo a mesma identidade visual e conceito.

````
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same colors, same text content, same headline, same supporting text, same CTA, same elements, same design language, same cinematic mood. Only recompose the framing and hierarchy for full-screen vertical viewing. The headline stays at the top third, the visual scene fills the middle, and the CTA button sits at the bottom third for easy thumb reach. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16. All text must be large, bold, high contrast and immediately readable. CTA button must be visually prominent with solid contrasting background.
````

#### D) Prompt de Animação pro Freepik (Magnific)

Texto pronto pra colar na ferramenta de imagem-pra-vídeo do Freepik (Magnific). Serve tanto pro Feed quanto pro Stories.

````
Anima essa imagem com micro-movimento cinematográfico no padrão de campanha publicitária esportiva premiada. APENAS os elementos do universo do futebol e do nicho se mexem. A headline, o texto de apoio e o CTA ficam 100% ESTÁTICOS, não se movem em nenhum momento.

MOVIMENTO DA CENA:
Micro-movimento que reforça a metáfora futebolística: camisa balançando devagar no vestiário, luz do estádio acendendo gradual, multidão pulsando sutilmente ao fundo, troféu refletindo luz, bandeira tremulando ao vento leve, partículas de pó voando devagar, chuteira balançando pendurada. O elemento do nicho dentro da cena também ganha micro-movimento próprio coerente. Loop hipnótico de 4-6 segundos no padrão Cannes Lions / Nike ad. Sem cortes, sem zoom agressivo.

REGRA CRÍTICA: a headline, o texto de apoio e o botão CTA são ESTÁTICOS. Não balançam, não aparecem com animação, não se movem. Ficam fixos o tempo todo. Só os elementos visuais da cena (futebol + nicho) é que têm o micro-movimento cinematográfico.

MÚSICA DE FUNDO SUGERIDA: trilha épica esportiva instrumental, crescente, sem letra. Padrão de comercial de Copa do Mundo: tambores graves, cordas marcantes, build-up emocional. Algo que dê peso de momento histórico. Sem narração e sem letra.
````

### 4. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) na legenda. Corrigir direto. Nunca mostrar versão bruta.

A headline e o CTA da ideia escolhida seguem o tom Cannes Lions (mais conceitual e visual) e NÃO passam pela revisora, mas devem respeitar Light Copy mínima: sem travessão, sem exclamação, sem promessa vaga. Se a headline tiver exclamação ou travessão, ajustar antes de gerar o prompt.

### 5. Apresentação e aprovação

Mostre tudo junto:

```
Pronto. Aqui está o seu criativo Copa / Futebol:

⚽ EQUIVALENTE FUTEBOLÍSTICO
[equivalente identificado pro nicho]

📌 IDEIA ESCOLHIDA (nº {numero_ideia} — {EMOÇÃO})
Conceito: [conceito]
Cena: [cena]
Headline: [headline]
Texto de apoio: [texto de apoio]
CTA: [CTA]

📝 LEGENDA PRO INSTAGRAM
[legenda gerada]

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

🎬 PROMPT DE ANIMAÇÃO PRO FREEPIK (MAGNIFIC)
[prompt de animação, dentro de bloco de código]

📱 PROMPT PRO CHATGPT, FORMATO STORIES
[prompt Stories, dentro de bloco de código]

---
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher outra ideia (das 10)
```

Se escolher 2, perguntar o que ajustar (legenda, headline, texto de apoio, CTA ou cena visual) e refazer apenas a parte indicada.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-copa-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-copa-{numero}.md`

Conteúdo do arquivo:

```markdown
# Copa / Futebol nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]
**Equivalente futebolístico:** [equivalente]

## Ideia escolhida (nº {numero_ideia} das 10 — {EMOÇÃO})

**Conceito:** [conceito]
**Cena:** [cena]
**Headline:** [headline]
**Texto de apoio:** [texto de apoio]
**CTA:** [CTA]

## Legenda pro Instagram

[legenda]

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

1. Abra o ChatGPT (com geração de imagem habilitada) ou o Gemini.
2. Cole o **Prompt Feed** e espere a arte ser gerada.
3. Quando estiver pronto, mande "ok" no chat.
4. Cole o **Prompt Stories** pra gerar a versão vertical da mesma arte.
5. Pra animar, abra o Freepik (Magnific) (ferramenta de imagem-pra-vídeo), suba a imagem gerada e cole o **Prompt de Animação**. O mesmo prompt serve pro Feed e pro Stories.

## Banco completo (as 10 ideias geradas nesta sessão)

Liste aqui todas as 10 ideias geradas nesta sessão, numeradas de 1 a 10, agrupadas pelas 5 emoções (Desejo, Medo, Oportunidade, Curiosidade, Prova).
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

3. Grave o Prompt Feed num arquivo `.txt` na pasta de criativos. Conteúdo é o Prompt Feed apresentado ao aluno, sem alterações. Nome: `prompt-copa-{numero}-feed.txt`.

4. Anuncie e rode o script no formato Feed (4:5):

```
🔍 Próximo passo: gerar a imagem do Feed via API. Tempo estimado: 2 a 3 minutos.
```

Use o comando Python correto da sessão (`python3` ou `py -3`), conforme a seção Execução de Scripts Python do CLAUDE.md.

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-copa-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-copa-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Copa / Futebol salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-copa-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

Depois ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro criativo Copa com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato
```

**No modo API:**

```
✅ Concluído: criativo Copa / Futebol gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-copa-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-copa-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro criativo Copa com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato
```

#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-copa-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same colors, same text content, same headline, same supporting text, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-copa-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-copa-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-copa-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-copa-{numero}-stories.png
```

e) Reapresente o mesmo menu de 4 opções.

## Regras de Propriedade Intelectual (obrigatórias)

NUNCA utilizar em nenhuma ideia ou prompt:

- Marcas reais (FIFA, Nike, Adidas, Puma, Umbro, etc.)
- Logos reais
- Clubes reais (Flamengo, Barcelona, Real Madrid, Palmeiras, etc.)
- Campeonatos reais com nome (Premier League, Champions League, Brasileirão, La Liga)
- Jogadores reais (Neymar, Messi, Cristiano Ronaldo, etc.)
- Técnicos reais
- Celebridades, influenciadores ou narradores reais
- Estádios identificáveis (Maracanã, Camp Nou, Wembley, etc.)
- Emissoras reais (ESPN, Globo, SporTV, etc.)

Sempre usar versões genéricas:

| Proibido | Substituição |
|---|---|
| FIFA | Campeonato mundial de futebol |
| Premier League | Liga internacional |
| Champions League | Torneio internacional |
| Neymar | Jogador profissional brasileiro |
| ESPN | Rede internacional de esportes |
| Seleção Brasileira | Equipe nacional com uniforme amarelo genérico |
| Flamengo / Palmeiras | Time genérico com cor X |
| Maracanã | Estádio profissional genérico |

### Regra de camisas. Sem nomes, sem identificação

Camisas de futebol que aparecerem nas ideias ou nos prompts devem ser SEMPRE genéricas:

- Sem nome de jogador nas costas
- Sem número identificável de jogador real
- Sem escudo de clube ou seleção
- Sem patrocínio ou marca visível

Usar sempre: camisa lisa genérica, número genérico (qualquer número 1 a 99 sem associação com jogador real) ou nenhuma identificação. Incluir explicitamente no prompt: "No real club crests. No real player names or numbers."

## Regras gerais

- Light Copy mínima na legenda. Sem travessão, sem exclamação, sem pergunta no início, sem promessa vaga, sem "não é X. É Y.".
- A headline e o CTA da ideia seguem tom Cannes Lions (mais conceitual e visual), com licença pra ser mais editorial, mas sem exclamação e sem travessão.
- Produto NÃO aparece no lead da legenda. Nada de "curso", "treinamento", nome do método ou sigla do programa no começo.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar a legenda. A headline e o CTA passam por uma checagem rápida de Light Copy mínima (sem travessão, sem exclamação, sem promessa vaga).
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- O prompt Feed segue o estilo de instruções visuais simples e diretas pro GPT Images: frases curtas, uma por linha, sem headers, sem numeração, sem bullets dentro do prompt.
- O nome do nicho aparece visível na arte. Reforçar isso no prompt sempre.
- Cada ideia explora um território visual único. Sem repetir camisa, troféu, VAR, campo ou qualquer outro elemento principal.
- Distribuição emocional travada em 2 desejo + 2 medo + 2 oportunidade + 2 curiosidade + 2 prova. Total 10.
- Regras de propriedade intelectual são duras. Nada de marca, clube, jogador, estádio, emissora real.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
