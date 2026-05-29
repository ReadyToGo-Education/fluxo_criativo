# Eleições. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 26 (Eleições). Conecta QUALQUER nicho ao universo das eleições e da política brasileira de forma INSTITUCIONAL, SOFISTICADA e APARTIDÁRIA. Gera 10 ideias com distribuição emocional (2 desejo, 2 medo, 2 oportunidade, 2 curiosidade, 2 prova), o aluno escolhe uma, e a sub-skill entrega legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
Usar a linguagem visual das eleições (santinho, carro de som, urna, palanque, fila na escola pública, horário eleitoral) como METÁFORA CRIATIVA para vender o produto do nicho gera um anúncio que parece campanha publicitária premiada antes de parecer anúncio. O reconhecimento cultural brasileiro é instantâneo e ativa identificação coletiva. O tom é apartidário e institucional, nunca militante.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço (ex: "automação com IA pra pequenos negócios", "preparação pra concurso PRF", "marmita fitness pra rotina corrida").
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

**Se escolher 1**, pular pra etapa 2 (Identificar equivalente eleitoral + gerar 10 ideias).

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
- Emagrecimento/Nutrição: "Programa de Emagrecimento em 90 dias", "Mentoria de Reeducação Alimentar", "Marmita Fitness pra Rotina Corrida"
- Último recurso (se realmente não der pra inferir nicho): "Mentoria de tráfego pago pra criadores", "Curso de inglês pra atletas", "Programa de emagrecimento em 90 dias"

Se o aluno não especificou público, assumir um plausível com base no produto/nicho e avisar antes de gerar as 10 ideias:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Identificar equivalente eleitoral + gerar 10 ideias

Anuncie:

```
🔍 Próximo passo: identificar o equivalente eleitoral do seu nicho e gerar 10 ideias de criativo. Tempo estimado: cerca de 60 segundos.
```

#### 2a. Identificar o equivalente eleitoral

Mapeie o nicho para o universo das eleições. Use a tabela abaixo como referência, mas crie conexões originais quando necessário:

| Nicho | Equivalente Eleitoral |
|---|---|
| Concurso | Candidatura aprovada |
| PRF | Segurança da campanha |
| Inglês | Diplomacia internacional |
| Emagrecimento | Plano de governo do corpo |
| Investimentos | Orçamento público / cofres públicos |
| LinkedIn | Comício do currículo |
| Marketing | Marqueteiro de campanha |
| Academia | Palanque do corpo |
| Homeopatia | Ministério da saúde pessoal |
| Artesanato | Voto popular / feito pelo povo |
| Dentista | Sorriso de candidato |
| Terapia | Assessor de imagem interior |
| Emprego | Candidatura aberta |
| Feng Shui | Plano de governo da sua casa |
| Nutrição/Marmita Fitness | Plataforma alimentar |
| Coaching | Debate interno |
| Finanças pessoais | Prestação de contas |
| Relacionamento | Coligação |
| Produtividade | Primeiro mandato |
| Automação/IA | Reforma administrativa |
| Tráfego pago | Cabo eleitoral digital |
| Tarot | Pesquisa de intenção do destino |

Pra nichos não listados, crie uma metáfora original e coerente. Anuncie internamente qual é o equivalente antes de gerar as ideias (sem mostrar pro aluno ainda, isso aparece dentro de cada ideia).

#### 2b. Distribuição emocional obrigatória

As 10 ideias devem seguir exatamente esta distribuição:

- 2 ideias de **DESEJO** (mostrar o resultado, a conquista, a vitória)
- 2 ideias de **MEDO** (mostrar o custo de não agir, a derrota, o mandato perdido)
- 2 ideias de **OPORTUNIDADE** (timing, janela, momento único, última chance)
- 2 ideias de **CURIOSIDADE** (gerar inquietação, pergunta mental, bastidores)
- 2 ideias de **PROVA** (resultado, números, credibilidade, votos conquistados)

#### 2c. Regra de diversidade visual (universo eleitoral BRASILEIRO)

As 10 ideias devem usar mecanismos visuais COMPLETAMENTE DIFERENTES entre si. Não pode haver duas com o mesmo elemento visual principal:

- Se uma usa urna, nenhuma outra usa urna
- Se uma usa palanque, nenhuma outra usa palanque
- Se uma usa debate, nenhuma outra usa debate
- Se uma usa santinho, nenhuma outra usa santinho
- Se uma usa pesquisa eleitoral, nenhuma outra usa pesquisa
- Se uma usa cédula/voto, nenhuma outra usa cédula

**IMPORTANTE: as referências visuais devem ser da ELEIÇÃO BRASILEIRA REAL, não americana nem europeia.** Nada de ballot box de madeira, nada de cédula de papel estilo americano, nada de cabine com cortina. O visual tem que ser reconhecido por qualquer brasileiro como "dia de eleição".

Territórios visuais brasileiros disponíveis (lista de referência, não fechada):
- Santinho espalhado no chão (papel pequeno com foto e número, típico do Brasil)
- Carro de som com megafone no teto rodando pelo bairro
- Adesivo de candidato no carro, no poste ou na camisa
- Fila na escola pública pra votar (cadeiras de plástico, pátio, fila no sol)
- Horário eleitoral na TV (tela de TV com "HORÁRIO ELEITORAL GRATUITO")
- Palanque improvisado com microfone na praça
- Bandeirinha e bandeirão em cruzamento de avenida
- Cabo eleitoral com colete distribuindo material
- Jingle tocando no carro de som
- Pesquisa de intenção de voto estilo gráfico de barras na TV
- Boca de urna na porta da escola
- Apuração ao vivo na TV (mapa do Brasil com porcentagens)
- Debate na TV (dois púlpitos, fundo escuro, logo genérico de emissora)
- Cola com número do candidato escrita na mão ou no papel
- Comício de rua com bandeiras e multidão

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
| Feng Shui | Bússola Luo Pan, cristais, bambu, plantas posicionadas |
| Marmita fitness | Tupperware aberto, frango grelhado, arroz integral, brócolis, potão |
| Automação/IA | Notebook, tela com fluxo, ícones de robô, gráfico crescente |

O nicho NUNCA pode ficar escondido apenas no CTA ou no texto.

#### 2e. Regra de presença visual forte do produto (ESPECÍFICA DE ELEIÇÕES)

O PRODUTO ou elementos concretos do nicho devem ser VISUALMENTE DOMINANTES na cena, tão presentes quanto o elemento eleitoral. A imagem é uma FUSÃO de dois mundos: o mundo da eleição E o mundo do nicho. Os dois precisam ter peso visual igual (mínimo 40% da composição pra cada).

ERRADO: uma urna sozinha com a palavra "Marmita Fitness" escrita em texto. (O nicho só existe no texto, não na imagem.)

CERTO: uma urna com marmitas fitness de verdade ao redor, tupperware aberto mostrando frango grelhado, arroz integral, brócolis. A comida é tão protagonista quanto a urna.

- Se o nicho é marmita fitness, marmitas reais, comida visível, tupperware, potão, ingredientes
- Se o nicho é inglês, livros de inglês, caderno com frases, bandeira, headset
- Se o nicho é artesanato, peças prontas, linhas, agulhas, crochê na cena
- Se o nicho é investimentos, gráficos, notas de dinheiro, calculadora, cofre

O produto NÃO pode ser figurante. O produto é co-protagonista.

#### 2f. Regra do nome do nicho visível

O NOME do nicho deve aparecer como texto legível na cena ou na headline de TODA ideia. Não basta ter objetos do nicho. A palavra precisa estar escrita e visível (no santinho, numa faixa, num pôster, na headline, em qualquer elemento textual da composição).

Exemplos:
- Se o nicho é "PRF", as letras "PRF" têm que ser lidas na imagem
- Se o nicho é "Feng Shui", a palavra "Feng Shui" aparece numa faixa ou pôster
- Se o nicho é "Marmita Fitness", as palavras "Marmita Fitness" aparecem visíveis (num santinho, numa faixa, numa pesquisa, em qualquer texto da cena)

#### 2g. Formato de cada ideia

```
IDEIA [número] — [EMOÇÃO]

Conceito: [a metáfora central em uma frase]
Cena: [descrição visual detalhada da imagem]
Headline: [frase principal do anúncio]
Texto de apoio: [complemento da headline]
CTA: [chamada pra ação]
```

#### 2h. Estilo criativo e tom apartidário

Pense como Diretor de Criação premiado, Cannes Lions, campanhas institucionais sofisticadas, The Economist, Apple. NÃO pense como marqueteiro de campanha real, panfleto eleitoral, propaganda política, oferta agressiva.

A prioridade é a IDEIA. Depois a venda.

O tom deve ser APARTIDÁRIO, INSTITUCIONAL e SOFISTICADO. Nunca militante.

A diferença é crucial:
- Errado: "Vote no candidato X" (parece propaganda política)
- Certo: "Vote na sua transformação" (metáfora criativa usando linguagem eleitoral)

#### 2i. Apresentação

Mostre as 10 ideias numeradas de 1 a 10, agrupadas pela emoção:

```
Identifiquei o equivalente eleitoral do seu nicho: [equivalente].

Aqui estão 10 ideias de criativo Eleições pro seu nicho.

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

2 a 4 linhas. Conecta a metáfora eleitoral ao nicho sem entregar tudo. Termina com **"Link na bio"** se o produto for de captação ou ofertas pagas. Light Copy aplicada (sem travessão, sem exclamação, sem pergunta no início, sem promessa vaga).

A legenda NÃO precisa repetir a headline da arte. Ela complementa, dá contexto ou puxa pra ação. Mantém o tom institucional e apartidário.

#### B) Prompt pro ChatGPT (formato Feed)

Use o estilo simples e direto descrito abaixo, substituindo os placeholders pelos dados da ideia escolhida. **O texto final ao usuário não pode ter colchetes.**

REGRAS DE ESCRITA DO PROMPT:
- Frases curtas, uma instrução por linha
- Sem headers, sem numeração, sem bullets dentro do prompt
- Sem estrutura pesada (nada de "1. Estilo visual:", "2. Composição:")
- Texto corrido fluindo naturalmente: formato → estilo → cena → elementos → o que NÃO incluir → iluminação → textos → hierarquia
- Usar negativas explícitas ("No real politicians.", "No party logos.", "No partisan colors.", "No ideological messaging.")
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
Brazilian election day atmosphere.
[Descrição da cena eleitoral brasileira em 1 a 2 frases, baseada na Cena da ideia escolhida, ex: "A worn pile of small candidate flyers scattered on a public school floor during election day."].
[Frase descrevendo os elementos concretos do nicho ocupando pelo menos 40% da composição, ex: "Among the flyers, several open tupperware containers showing grilled chicken, brown rice and broccoli sit on the floor as if they were the real candidates."].
The product elements are as visually dominant as the election elements.
The word "[nome do nicho em português]" is clearly visible written on [santinho, faixa, pôster, headline, etc].
Brazilian visual context, not American or European elections.
No real politicians.
No real party logos or symbols.
No partisan colors.
No ideological messaging.
No real candidate names or numbers.
Warm cinematic lighting.
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
Anima essa imagem com micro-movimento sutil do dia de eleição brasileira, no padrão de campanha institucional. APENAS os elementos do universo eleitoral e os elementos concretos do nicho se mexem. A headline, o texto de apoio e o CTA ficam 100% ESTÁTICOS, não se movem em nenhum momento.

MOVIMENTO DA CENA:
Micro-movimento brasileiro reconhecível do dia de eleição: santinho caindo devagar no chão, bandeirinha tremulando ao vento da tarde, carro de som passando devagar ao fundo, fila andando lentamente, mão segurando o título de eleitor, papel sendo dobrado pra entrar na urna, balão subindo, luz quente de tarde de domingo de eleição. O elemento concreto do nicho na cena também ganha micro-movimento próprio coerente. Loop hipnótico de 4-6 segundos no padrão The Economist / Apple ad / campanha institucional. Sem cortes, sem zoom agressivo.

REGRA CRÍTICA: a headline, o texto de apoio e o botão CTA são ESTÁTICOS. Não balançam, não aparecem com animação, não se movem. Ficam fixos o tempo todo. Só os elementos visuais da cena (eleição brasileira + nicho) é que têm o micro-movimento sutil.

MÚSICA DE FUNDO SUGERIDA: trilha institucional brasileira, instrumental, sem letra. Padrão de campanha publicitária sofisticada (The Economist, Itaú, Petrobras). Piano minimalista, cordas suaves ou ambient atmosférico. Sem jingle político, sem música partidária, sem referência a qualquer campanha real. Tom apartidário e contemplativo.
````

### 4. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) na legenda. Corrigir direto. Nunca mostrar versão bruta.

A headline e o CTA da ideia escolhida seguem o tom Cannes Lions (mais conceitual e visual) e NÃO passam pela revisora, mas devem respeitar Light Copy mínima: sem travessão, sem exclamação, sem promessa vaga. Se a headline tiver exclamação ou travessão, ajustar antes de gerar o prompt.

**Filtro extra de neutralidade política:** antes de mostrar, varrer a legenda e a headline em busca de:
- Posicionamento ideológico (esquerda, direita, conservador, progressista, militante)
- Nome de político real ou partido real
- Pauta política real (aborto, armas, reforma X, privatização Y)
- Slogan real de campanha
Se aparecer qualquer um, reescrever o trecho neutralizando.

### 5. Apresentação e aprovação

Mostre tudo junto:

```
Pronto. Aqui está o seu criativo Eleições:

🗳️ EQUIVALENTE ELEITORAL
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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-eleicoes-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-eleicoes-{numero}.md`

Conteúdo do arquivo:

```markdown
# Eleições nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]
**Equivalente eleitoral:** [equivalente]

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

3. Grave o Prompt Feed num arquivo `.txt` na pasta de criativos. Conteúdo é o Prompt Feed apresentado ao aluno, sem alterações. Nome: `prompt-eleicoes-{numero}-feed.txt`.

4. Anuncie e rode o script no formato Feed (4:5):

```
🔍 Próximo passo: gerar a imagem do Feed via API. Tempo estimado: 2 a 3 minutos.
```

Use o comando Python correto da sessão (`python3` ou `py -3`), conforme a seção Execução de Scripts Python do CLAUDE.md.

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-eleicoes-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-eleicoes-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Eleições salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-eleicoes-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

Depois ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro criativo Eleições com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato
```

**No modo API:**

```
✅ Concluído: criativo Eleições gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-eleicoes-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-eleicoes-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro criativo Eleições com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato
```

#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-eleicoes-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same colors, same text content, same headline, same supporting text, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-eleicoes-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-eleicoes-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-eleicoes-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-eleicoes-{numero}-stories.png
```

e) Reapresente o mesmo menu de 4 opções.

## Regras de Neutralidade Política e Propriedade Intelectual (obrigatórias)

NUNCA utilizar em nenhuma ideia ou prompt:

- Políticos reais (Lula, Bolsonaro, Temer, FHC, Dilma, qualquer figura pública política)
- Partidos reais (PT, PL, MDB, PSOL, PSDB, União Brasil, Republicanos, etc.)
- Logos ou símbolos de partidos reais (estrela, bandeiras partidárias, etc.)
- Slogans reais de campanhas ("Brasil acima de tudo", "Lula lá", etc.)
- Cores associadas a partidos específicos de forma identificável (evitar vermelho isolado como tema central, evitar verde-amarelo como símbolo político)
- Instituições eleitorais identificáveis (TSE, TRE com logo real, Justiça Eleitoral)
- Urna eletrônica brasileira real com identidade visual oficial do TSE
- Números de candidatos reais (13, 22, 45, etc.)
- Referências a eleições específicas (2022, 2024, 2026, etc.)
- Posicionamento ideológico (esquerda, direita, centro, militante)
- Pautas políticas reais (aborto, armas, privatização, reforma da previdência, etc.)
- Celebridades, influenciadores ou figuras públicas
- Fake news, desinformação eleitoral ou linguagem polarizadora

Sempre usar versões genéricas e apartidárias:

| Proibido | Substituição |
|---|---|
| Político real | Candidato genérico, silhueta, figura sem rosto |
| Partido real | Partido genérico sem cor ou símbolo identificável |
| Urna eletrônica oficial | Urna de votação genérica estilo eletrônico sem logotipo do TSE, ou mesa de votação genérica |
| Slogan real | Frase original criada pro anúncio |
| Cores partidárias | Paleta neutra institucional (dourado, verde escuro, azul marinho, branco) |
| Eleição específica | "Próxima eleição", "período eleitoral", "temporada de votos" |
| Número de candidato real | Número fictício como 99, 77, 88 |

### Regra de tom político

O criativo NUNCA deve parecer propaganda política real. Deve parecer uma CAMPANHA PUBLICITÁRIA PREMIADA que usa a linguagem visual das eleições como METÁFORA CRIATIVA pra vender o produto do nicho.

A diferença é crucial:
- Errado: "Vote no candidato X" (propaganda política)
- Certo: "Vote na sua transformação" (metáfora criativa usando linguagem eleitoral)

Tom sempre institucional, sofisticado e apartidário.

## Regras gerais

- Light Copy mínima na legenda. Sem travessão, sem exclamação, sem pergunta no início, sem promessa vaga, sem "não é X. É Y.".
- A headline e o CTA da ideia seguem tom Cannes Lions / The Economist (mais conceitual e visual), com licença pra ser mais editorial, mas sem exclamação e sem travessão.
- Produto NÃO aparece no lead da legenda. Nada de "curso", "treinamento", nome do método ou sigla do programa no começo.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar a legenda. A headline e o CTA passam por uma checagem rápida de Light Copy mínima e filtro de neutralidade política.
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- O prompt Feed segue o estilo de instruções visuais simples e diretas pro GPT Images: frases curtas, uma por linha, sem headers, sem numeração, sem bullets dentro do prompt.
- O nome do nicho aparece visível na arte. Reforçar isso no prompt sempre.
- O produto ocupa pelo menos 40% da composição visual. Não pode ser figurante. Reforçar no prompt.
- Cada ideia explora um território visual brasileiro único do universo eleitoral. Sem repetir santinho, urna, palanque, debate, etc.
- Distribuição emocional travada em 2 desejo + 2 medo + 2 oportunidade + 2 curiosidade + 2 prova. Total 10.
- Regras de neutralidade política são duras. Nada de político, partido, slogan, cor partidária, pauta ideológica.
- Contexto visual é ELEIÇÃO BRASILEIRA, não americana nem europeia.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica, eleições, candidato.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
