# AIDA Completo. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 4 (AIDA Completo). Gera criativo estático de anúncio dividido em 3 passos AIDA. Cada passo é validado antes de avançar para o próximo. No fim, o aluno escolhe gerar a imagem colando o prompt no ChatGPT ou direto pela API.

**Por que 3 passos separados:**
A maioria dos criativos falha porque o texto é escrito antes do layout ser definido.
O texto não cabe na composição, o visual não reforça a mensagem, o botão some no fundo.
Este fluxo inverte: primeiro a imagem que para o scroll, depois onde cada coisa fica, depois o texto que cabe naquele espaço.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto (sem passar pelo orquestrador), carregar esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência quando o perfil for incompleto):

- **Quadro** (transformação principal): do `perfil.md` se existir, ou inferido do nome + tipo + preço.
- **Nicho e público**: do `perfil.md` e `idconsumidor.md` se existirem, ou inferidos do slug + tipo.
- **Top 5 Urgências Ocultas mais fortes** (priorizando Dores, Desejos e Urgências Quentes): da seção "Urgências Ocultas" do `perfil.md` se existir. Se NÃO existir, **inferir 5 urgências plausíveis** a partir do nicho e do público. Marcar como "○ inferido" quando apresentar na Pergunta 2/2.
- **Identidade do Consumidor** (estética, tom, cultura visual se disponível): do `idconsumidor.md` se existir.

**Resumo de contexto antes da entrevista (sempre mostrar):**

Antes da Pergunta 1/2 da Entrevista, mostre um pequeno resumo do que foi extraído/inferido pro aluno confirmar:

```
Vou usar estes dados do seu produto ativo ({slug}):

Quadro: [Quadro real ou inferido]
Nicho: [nicho]
Público: [público]

(Marque "✓ do perfil" pros campos do perfil.md / idconsumidor.md, e "○ inferido" pros campos derivados do slug, tipo ou preço.)

Está tudo certo?

1. Sim, pode seguir pra entrevista
2. Quero ajustar algum campo
```

Se escolher 2, faça entrevista parcial só dos campos a ajustar. Use exemplos do nicho do produto ativo nas perguntas de ajuste, nunca genéricos.

### 1. Pesquisa de Referências Virais (opcional, recomendado)

Pergunte:

```
Quer que eu pesquise referências virais antes de criar?
Demora cerca de 60 segundos e melhora a qualidade visual.

1. Sim, pesquisar agora
2. Não, pular e ir direto para a entrevista
```

**Se escolher 1**, anuncie e execute:

```
🔍 Próximo passo: pesquisar formatos virais de anúncio estático no nicho. Tempo estimado: cerca de 60 segundos.
```

Faça 2 buscas (WebSearch):
- `"Instagram static ad formats high converting [mês/ano atual]"`
- `"Instagram ad examples [nicho do produto] [ano atual]"`

Cruze com a referência interna em `.claude/skills/anuncios/references/formatos-virais-instagram.md`.

Apresente:

```
✅ Concluído: pesquisa de virais.

Os formatos que mais estão convertendo no seu nicho:
1. [Formato A]. [por que funciona]
2. [Formato B]. [por que funciona]
3. [Formato C]. [por que funciona]

Vou usar essas referências como inspiração para a cena do Passo 1.
```

### 2. Entrevista (2 perguntas)

**Pergunta 1/2. Formato:**

```
Qual formato de imagem?

1. Feed retrato (4:5, 1080x1350). Mais espaço na tela, melhor para feed
2. Quadrado (1:1, 1080x1080). Clássico, funciona em tudo
3. Stories ou Reels (9:16, 1080x1920). Tela cheia vertical

Digite o número:
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

**Pergunta 2/2. Urgência base:**

Use as 5 urgências extraídas no Passo 0 (reais do `perfil.md` ou inferidas a partir do nicho/público quando o perfil não existir). Priorize Dores, Urgências Quentes e Desejos.

```
Qual situação vai inspirar o criativo?
(escolha a que mais ressoa com o momento de compra)

1. [Urgência 1] [marcar ✓ se veio do perfil.md, ○ se foi inferida]
2. [Urgência 2] [marcar ✓ ou ○]
3. [Urgência 3] [marcar ✓ ou ○]
4. [Urgência 4] [marcar ✓ ou ○]
5. [Urgência 5] [marcar ✓ ou ○]

Digite o número (ou descreva outra situação se nenhuma encaixar):
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

Se as 5 urgências forem todas inferidas (perfil ausente), avise no topo: "As urgências abaixo são inferidas do nicho do produto. Se nenhuma encaixar, descreva a situação específica que quer atacar no criativo."

```
--- Entrevista concluída ---
Formato: [formato]
Urgência: [urgência escolhida]
CTA padrão: Saiba mais (para trocar, diga a qualquer momento)
Próximo: Passo 1 de 3 (imagem de fundo)
---
```

### 3. Passo 1 de 3: Imagem de Fundo (Atenção)

**Objetivo:** gerar a imagem de fundo que para o scroll.
Sem texto. Sem botão. Apenas o visual que cria impacto emocional imediato.

**Lógica de construção:**

A urgência oculta escolhida mapeia para uma categoria visual:

| Categoria de urgência | Direção visual |
|---|---|
| Dor física ou emocional | Cena do instante em que o problema ainda persiste (não após a derrota aceita). Tensão presente que convida "como resolve?" não resignação que conclui "não tem saída". Preferir objetos que contam a história ou detalhe de costas/mãos. Luz neutra ou quente. Luz fria + postura caída = derrota (estado fechado). |
| Desejo de resultado | Cena de conquista ou de resultado já tangível, luz quente, espaço aberto, postura confiante ou relaxada |
| Urgência quente (evento próximo) | Cena de tempo passando ou decisão iminente, contraste claro/escuro, elemento que transmite prazo |
| Urgência fria (acúmulo de tempo) | Cena de padrão que se repete, peso de longa data sem resignação. Transmite "mais uma vez aqui" não "desisti de mudar". Tons neutros aceitos se a composição transmite repetição, não fechamento. |
| Urgência inusitada | Cena de contraste inesperado, elemento fora de lugar, composição que gera curiosidade antes de qualquer texto |

**Regras do prompt de fundo:**
- Sempre em inglês
- Descrever composição primeiro (o que está em primeiro plano, ângulo)
- Iluminação especificada explicitamente
- Referência de câmera/lente para fotorrealismo (ex: "shot on Sony A7, 85mm")
- Mood emocional no final
- Sem rostos completos e visíveis (preferir costas, mãos, objetos ou detalhe de corpo; silhueta com postura caída e luz fria gera visual de derrota. Usar silhueta apenas em cenas aspiracionais ou de movimento)
- Sujeito humano SEMPRE vestido de forma adequada para anúncios de mídia social. Especificar a roupa no prompt (ex: "wearing a bikini", "in a dress", "in casual clothes"). Nunca omitir a vestimenta.
- Sem texto, logo ou watermark na cena
- Negative prompt separado quando a ferramenta suportar

**Estrutura interna do prompt (referência para construção):**

```
[Composição: o que está em cena e ângulo], [sujeito sem rosto ou silhueta],
[ação ou estado], [ambiente e contexto], [iluminação: tipo, direção, temperatura],
[referência de câmera se fotorrealista], [paleta de cor dominante],
[mood emocional final]. --no text, faces, watermark, logo
```

**Derivar os ingredientes visuais do produto antes de criar as opções:**

Antes de escrever qualquer prompt, extraia do perfil do produto:
- Ambiente típico do consumidor: onde ele está quando sente essa urgência? (quarto, cozinha, academia, escritório, praia, vestiário, consultório, carro?)
- Objeto do cotidiano diretamente ligado à urgência: o que ele vê, toca ou evita nesse momento? (balança, espelho, prato, calça que não fecha, agenda lotada, carteira vazia, celular com notificação?)
- Situação concreta e específica: não "ela se sente mal" mas "ela está olhando para a calça jeans dobrada na gaveta há três meses"
- Elemento do nicho que qualquer pessoa do público reconhece de imediato

Esses 4 ingredientes são a matéria-prima das 3 opções. Não gere opções sem eles.

**Gere 3 opções de imagem de fundo**, cada uma com uma técnica de composição diferente:

- Opção A: close extremo em objeto do nicho. Sem pessoa ou apenas detalhe (mãos, costas, silhueta de costas). O objeto conta a história sozinho. A cena convida "como muda isso?" não conclui "já acabou". Luz neutra ou quente. Ex: a calça dobrada, a balança, o prato intocado.
- Opção B: cena de cotidiano exata. O consumidor no ambiente e momento específico da urgência, ângulo de câmera natural como se alguém fotografasse sem que a pessoa soubesse. Luz realista do ambiente. Ex: ela sentada na beira da cama olhando para o espelho, ele na mesa de trabalho às 22h.
- Opção C: composição de contraste ou surpresa. Elemento fora do lugar, ângulo inesperado (de cima para baixo, de baixo para cima, close em detalhe minúsculo), ou dois elementos opostos no mesmo quadro. Cria curiosidade antes de qualquer leitura de texto.

Apresente as 3 opções com apenas descrição em português. O prompt em inglês é derivado internamente após a escolha e aparece somente no prompt consolidado final.

```
Passo 1 de 3: imagem de fundo

Escolha a cena que vai parar o scroll:

Opção A. [nome descritivo em português]:
[descrição visual em português, 2 a 3 frases. O que aparece, o ângulo, a luz,
o mood. Como se você estivesse descrevendo um quadro para alguém que não pode ver.]

Opção B. [nome descritivo em português]:
[descrição visual em português, 2 a 3 frases]

Opção C. [nome descritivo em português]:
[descrição visual em português, 2 a 3 frases]

Cada opção representa um momento específico da urgência escolhida. O kicker do Passo 3 deve capturar o momento da opção escolhida, não uma versão genérica da urgência.

---
1. Usar Opção A
2. Usar Opção B
3. Usar Opção C
4. Quero ajustar uma das opções
```

Após aprovação, avance para o Passo 2.

### 4. Passo 2 de 3: Layout e Cores (Interesse e Desejo)

**Objetivo:** definir onde cada elemento vai ficar e como vai se parecer.
Esta etapa acontece ANTES de escrever o texto para que as palavras sejam escritas
dentro dos limites reais do espaço disponível.

**Lógica de construção do layout:**

O layout cria uma hierarquia visual que guia o olho na sequência:
1. Imagem de fundo capta a atenção (Passo 1)
2. Título gera interesse em menos de 2 segundos
3. Apoio cria desejo aprofundando o benefício
4. Botão converte o desejo em ação

**Zonas padrão por formato:**

ATENÇÃO: o Meta Ads sobrepõe na base da imagem o nome do anunciante e o botão nativo
("Saiba mais"). Essa sobreposição ocupa aproximadamente os últimos 10-12% da imagem.
Todos os elementos do criativo (apoio, botão, instrução de clique) devem estar
posicionados acima dessa zona, com folga de pelo menos 10% extra no rodapé para
não colidir com a UI nativa da plataforma.

Para feed retrato (4:5, 1080x1350):
- Zona A (imagem limpa, topo, 60-65%): cena fotográfica sem texto, iluminada naturalmente
- Zona B (bloco de texto, base, 25-30%): kicker + headline + apoio + instrução de clique
- Zona C (rodapé, 10-12%): VAZIA, reservada para sobreposição nativa do Meta

Zona B. Ordem dos elementos de cima para baixo dentro do bloco escuro:
  1. Kicker (linha pequena no topo do bloco)
  2. Headline (elemento dominante, fonte enorme, ocupa a maior parte visual da zona)
  3. Apoio linha 1 (dado concreto, abaixo do headline)
  4. Apoio linha 2 (complemento, opcional)
  5. Instrução de clique (alinhada à esquerda, base do bloco)

Para quadrado (1:1, 1080x1080):
- Zona A (imagem limpa, topo, 60%): cena fotográfica sem texto
- Zona B (bloco de texto, base, 28%): kicker + headline + apoio + instrução
- Zona C (rodapé, 12%): VAZIA

Para stories/reels (9:16, 1080x1920):
- Zona A (imagem limpa, topo, 55%): cena fotográfica sem texto
- Zona B (bloco de texto, base, 31%): kicker + headline + apoio + instrução
- Zona C (rodapé, 14%): VAZIA (safe zone)

**Derivar cor de destaque pela categoria de urgência (não pelo nicho):**

A cor do headline deve ser brilhante e saturada. O fundo escuro natural faz o trabalho de contraste sem precisar de sombra.

| Categoria de urgência | Cor de destaque do headline | Uso |
|---|---|---|
| Dor física ou emocional | Laranja-vermelho (#FF4500) ou Âmbar (#FF8C00) | Tensão, urgência, peso |
| Desejo de resultado | Verde elétrico (#00D400) ou Dourado (#FFD700) | Aspiração, conquista, leveza |
| Urgência quente (evento próximo) | Laranja elétrico (#FF6600) ou Vermelho (#FF2D55) | Prazo, decisão iminente |
| Urgência fria (acúmulo de tempo) | Teal brilhante (#00CED1) ou Branco puro (#FFFFFF) | Reflexão, padrão repetido |
| Urgência inusitada | Roxo elétrico (#8B5CF6) ou Lima (#A3E635) | Curiosidade, contraste |

Kicker e apoio sempre em branco puro (#FFFFFF). Só o headline recebe a cor de destaque.
A cor de destaque vai em TODO o texto do headline, não apenas em uma palavra.

**Layout calculado internamente. Não apresentar ao usuário como etapa separada.**

Com base no formato escolhido na Entrevista e na categoria de urgência, determine silenciosamente:
- Cor de destaque do headline (tabela acima)
- Limites de caractere internos por zona (kicker: 50, headline: 30, apoio: 55 cada, instrução: 55)

Mostre apenas uma linha de transição após o usuário escolher a cena, antes de gerar o texto:

```
Layout definido: [cor hex] ([nome da cor]). Gerando as versões de texto.
```

Avance diretamente para o Passo 3 sem pedir aprovação do layout.

### 5. Passo 3 de 3: Texto da Imagem (Ação)

**Objetivo:** escrever o texto exato de cada zona definida no Passo 2.
O texto é escrito para caber no espaço real, não o contrário.

**Regras de texto interno (Light Copy aplicada à imagem):**

- Kicker: voz de monólogo interno, não narrador. O kicker é o pensamento que passa pela cabeça da pessoa naquele momento, não uma marca descrevendo a situação de fora. Teste: a pessoa poderia pensar isso com essas palavras exatas em conversa com uma amiga? Se não, reescreva. Bom: "Mais um verão guardando o biquíni no fundo da gaveta" (pensamento dela, primeira pessoa implícita). Ruim: "Esse biquíni esperou tempo demais na gaveta" (narrador apontando de fora, tom de marca). Para qualquer nicho: bom = "Mais um mês olhando para a fatura sem saber por onde começar". Ruim = "Suas dívidas cresceram enquanto você tentava economizar".
- Kicker: afirmação curta. Sem exclamação, sem pergunta.
- Kicker: fala sobre o estado atual do leitor, não sobre o produto
- Kicker: tempo presente ou padrão recorrente ainda ativo. Nunca derrota passada já encerrada. "Mais um mês no mesmo ponto" funciona (padrão que continua). "Mais uma tentativa que ficou para trás" não funciona (ciclo encerrado, estado fechado).
- Kicker: deve capturar o MOMENTO ESPECÍFICO da cena escolhida no Passo 1, não uma versão genérica da urgência. O específico cria identificação imediata. O genérico passa despercebido.
- Título: sem ponto de exclamação, sem pergunta, sem travessão
- Título: dado concreto ou afirmação direta (nunca promessa vaga)
- Headline: escrito em CAIXA ALTA (ALL CAPS). Fonte enorme exige brevidade. Max 30 chars.
- Headline: todo o texto na cor de destaque brilhante da categoria (ver Passo 2). Não usar warm white. A cor vai em todo o headline, não apenas em uma palavra.
- Kicker + Título: escrito como trava e chave. O kicker abre uma pergunta implícita ("por que não funciona?", "quando isso muda?", "existe outro caminho?"). O título fecha exatamente essa pergunta com dado concreto. O título deve responder diretamente ao kicker, não ser independente. Exemplo: Kicker "Mais um mês no mesmo ponto de partida" então Título "[resultado concreto] em [prazo] acontece quando muda o método, não o esforço". Exemplo: Kicker "Seis tentativas e o padrão continua igual" então Título "[resultado concreto] para quem parou de repetir o mesmo caminho". Regra prática: se você cobrir o título e o kicker ainda fizer sentido sozinho, o par não está funcionando. Se o título pudesse existir sem o kicker, o par está desconectado.
- Apoio linha 1: o dado concreto isolado (número, prazo, resultado específico)
- Apoio linha 2: o argumento ou complemento da linha 1 (o "como" ou "sem X"). PROIBIDO usar termos técnicos ou nomes de categorias. Use o vocabulário que a pessoa usaria com uma amiga: não "grupo alimentar" mas "doce, pão, arroz com feijão"; não "sedentarismo" mas "sem sair do sofá ou da mesa de trabalho"; não "gestão emocional" mas "sem explodir com todo mundo à toa"; não "renda passiva" mas "dinheiro caindo na conta enquanto você dorme". Dois ou três exemplos concretos valem mais que um nome de categoria.
- Instrução de clique: SEMPRE gerar o complemento completo. O CTA padrão é "Saiba mais". Se o usuário indicou outro em qualquer momento, usar esse. Nunca inventar CTA.
- Instrução de clique: SEMPRE gerar o complemento completo, nunca deixar como placeholder. O complemento é uma frase de curiosidade ou desejo que conecta com o kicker ou o título. Começa com "e" (conectivo suave). Usa verbo de descoberta: "veja", "descubra", "entenda", "confira". Não menciona "curso", "treinamento", "compra". Pode ter 1 ou 2 linhas. Max 55 chars. Exemplos: "e veja com os seus próprios olhos o porquê", "e descubra o que muda nas primeiras 2 semanas", "e entenda por que tantas pessoas estão conseguindo".
- Nenhuma zona pode ter texto que não caiba no limite de caracteres do Passo 2

**Lógica AIDA para o texto:**

- Passo 1 (visual) cumpriu ATENÇÃO
- Passo 2 (layout) define onde INTERESSE e DESEJO vão aparecer
- Passo 3 (texto): kicker cria identificação, título entrega INTERESSE, apoio cria DESEJO, botão converte em AÇÃO

**Verificar antes de gerar as versões:**
- O headline está em CAIXA ALTA (ALL CAPS) e tem no máximo 30 chars? Se não, converter e cortar.
- O headline usa a cor de destaque brilhante da categoria (não warm white)? Se não, corrigir.
- O kicker está no presente ou em padrão recorrente ainda ativo? Se estiver no passado de derrota concluída, reescrever para tensão presente antes de continuar.
- O kicker captura o MOMENTO ESPECÍFICO da cena escolhida no Passo 1 ou virou genérico? Se virou genérico, retornar ao momento específico.
- O kicker abre uma pergunta implícita que o título responde? Se o título pudesse existir sem o kicker, o par está desconectado.
- O tom emocional do kicker combina com o tom visual da cena? Cena de tensão presente + kicker de tensão presente = coerente. Cena neutra + kicker de derrota = incoerente.
- O kicker soa como pensamento humano ou como narrador/marca descrevendo de fora? Teste: a pessoa poderia pensar isso com essas palavras exatas? Se não, reescrever na voz interna do leitor antes de continuar.
- O apoio usa termos técnicos ou nomes de categorias (grupo alimentar, sedentarismo, gestão emocional, renda passiva)? Se sim, substituir por exemplos concretos do vocabulário cotidiano antes de continuar.

**Antes de mostrar as versões:** aplicar a rotina de auto-revisão de copy obrigatória do CLAUDE.md (carregar Manual da Copy + acionar revisora) e corrigir direto no texto. Não mostrar versão bruta.

**Gere 2 versões completas do anúncio**, cada uma com kicker, título, apoio (2 linhas) e botão já combinados.
Não apresentar opções separadas por zona. O usuário escolhe a versão inteira.

**INSTRUÇÃO DE CLIQUE. OBRIGATÓRIA EM AMBAS AS VERSÕES:** Nunca deixar o complemento como placeholder. Gere uma frase concreta baseada no kicker ou no título da versão. O complemento começa com "e" e usa verbo de descoberta ("veja", "descubra", "entenda", "confira"). Max 55 chars. Exemplos: "e veja o que muda nas primeiras semanas", "e descubra por que quem já tentou antes consegue com este método", "e entenda o que faz a diferença desta vez".

Apresente assim (sem contadores de caractere, que são verificação interna, não output):

```
Versão 1:
"[kicker 1]"
[HEADLINE 1 EM CAIXA ALTA]
[apoio linha 1]
[apoio linha 2]
👆 Clique em "[CTA]" e [complemento]

Versão 2:
"[kicker 2]"
[HEADLINE 2 EM CAIXA ALTA]
[apoio linha 1]
[apoio linha 2]
👆 Clique em "[CTA]" e [complemento]

---
1. Versão 1
2. Versão 2
3. Quero ajustar algo
```

Após o usuário escolher a versão de texto, siga para a seção 6 (Saída) para montar o prompt e gerar a imagem.

### 6. Saída: geração e entrega

Depois que o usuário escolheu a versão de texto, monte o **PROMPT FINAL CONSOLIDADO** em inglês. Ele é a base para os dois modos de geração da imagem.

REGRA CRÍTICA: usar linguagem visual espacial (upper area, lower band, centered),
NUNCA porcentagens numéricas. Porcentagens são apenas para cálculo interno no Passo 2.
O modelo de imagem não deve renderizar nenhuma anotação de layout.

```
Generate a complete Instagram feed ad ([dimensoes]px).

SCENE: [descrição visual completa do Passo 1 em inglês,
com o sujeito vestido de forma adequada para anúncios de mídia social.]
The upper area of the image must be a clean, well-lit photographic scene
with no text and no dark areas. The photograph should look natural and bright.
The lower band must fade into a very deep dark gradient
(near-black at the bottom, fade begins around two-thirds from the top).
IMPORTANT: leave a large empty margin at the very bottom of the image.
The bottom quarter must be completely free of any text, icon, or element.
The entire text block must sit in the upper half of the dark band,
well above the bottom edge of the image.

TEXT ON PHOTO (all text in the dark lower zone only, concentrated in the upper
portion of that zone. No text near the bottom edge):
- In the upper part of the dark lower zone: small regular white sans-serif
  text, no bold, clean, centered (dark background provides contrast,
  no shadow needed):
  "[kicker do Passo 3]"
- Immediately below the kicker: ENORMOUS ultra-bold black-weight all-caps
  sans-serif text (the dominant visual element, 3 to 5 times larger than
  the kicker), in bright saturated [cor hex destaque], centered,
  max 2 lines, no shadow needed:
  "[HEADLINE DO PASSO 3 EM MAIÚSCULAS]"
- Below the headline: small regular white sans-serif text, clean, centered:
  "[apoio linha 1 do Passo 3]"
- Immediately below: slightly smaller regular white sans-serif text, centered:
  "[apoio linha 2 do Passo 3]"
- Below the support lines, still well above the bottom quarter safe zone,
  left-aligned: a small hand cursor tap icon followed by light gray (#BBBBBB)
  regular small sans-serif text: Clique em, then "[CTA]" in bold white,
  then in light gray: "[instrução de clique do Passo 3]"

Style: professional Instagram ad, photorealistic clean scene in the upper zone,
bold dominant typography in the upper portion of the dark lower zone, generous
empty space at the very bottom. No text in the photographic area.
No background bands, no colored rectangles, no overlay boxes,
no percentage labels, no zone markers, no annotations.
```

Depois pergunte como o usuário quer gerar a imagem:

```
Como você quer gerar a imagem?

1. Colar no ChatGPT ou Gemini (grátis)
   Eu te entrego o prompt pronto. Você cola, gera a arte e salva a imagem.

2. Gerar agora pelo OpenRouter (tem custo)
   Eu mando o prompt direto pro modelo de imagem e já salvo o PNG na sua
   pasta de entregas. Custa centavos por imagem.

Digite o número:
```

Em qualquer um dos dois modos, salve o briefing legível em:
`meus-produtos/{ativo}/entregas/criativos/criativo-aida-{numero}.md`

Conteúdo do briefing:
- Nome do criativo, data, formato, urgência base
- Cena escolhida (descrição em português)
- Layout em tópicos (zonas, fontes, cores)
- Texto escolhido (kicker, headline, apoio, instrução)
- Prompt final consolidado em inglês em bloco de código

O número do criativo é sequencial dentro da pasta. Verifique os arquivos `criativo-aida-*.md` existentes antes de numerar.

#### Modo ChatGPT (escolha 1)

Apresente:

```
Pronto. Cole esse prompt no seu gerador de imagem:

[PROMPT CONSOLIDADO EM INGLES]

Adaptar para sua ferramenta:
- ChatGPT / Gemini: cole como está, sem alteração
- Midjourney: adicione ao final: --ar [ratio] --v 6.1 --style raw --s 250 --no text, faces, watermark
- Ideogram: adicione ao final: Style: Realistic, Aspect Ratio: [ratio]

Antes de entregar este bloco ao aluno, substitua `[ratio]` pelo valor real do formato escolhido na Entrevista: feed retrato = 4:5, quadrado = 1:1, stories ou reels = 9:16. O placeholder `[ratio]` não pode aparecer literal no texto entregue.

Briefing salvo em meus-produtos/{ativo}/entregas/criativos/criativo-aida-{numero}.md
```

#### Modo API (escolha 2)

1. Leia `OPENROUTER_API_KEY` no `.env`. Se não existir ou estiver vazia, ofereça:

```
Para gerar pela API você precisa da chave do OpenRouter no .env.

1. Configurar agora (uso o /configurar-imagens para guiar)
2. Voltar e usar o modo ChatGPT
```

2. Pergunte o modelo:

```
Qual modelo de imagem?

1. GPT Image 2 (recomendado)
   Cerca de US$ 0,05 por imagem.
2. Gemini Nano Banana 2
   Cerca de US$ 0,07 por imagem.

Digite o número:
```

Mapa de modelo: opção 1 vira `openai/gpt-5.4-image-2`, opção 2 vira `google/gemini-3.1-flash-image-preview`.

3. Defina a proporção pelo formato escolhido na Entrevista: feed retrato vira `4:5`, quadrado vira `1:1`, stories ou reels vira `9:16`.

4. Anuncie:

```
🔍 Próximo passo: gerar a imagem do criativo via API. Tempo estimado: 2 a 3 minutos.
```

5. Grave o prompt final consolidado num arquivo de texto. Isso evita erro de aspas no comando:
`meus-produtos/{ativo}/entregas/criativos/prompt-criativo-aida-{numero}.txt`

6. Rode o script, substituindo os campos entre chaves pelos valores reais:

Use o comando Python correto da sessão (`python3` ou `py -3`), conforme a seção Execução de Scripts Python do CLAUDE.md. Nos comandos abaixo, troque `py -3` pelo comando detectado se necessário.

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-criativo-aida-{numero}.txt" --model "{modelo escolhido}" --aspect "{proporcao}" --out "meus-produtos/{ativo}/entregas/criativos/criativo-aida-{numero}.png"
```

7. Se o script terminar com sucesso, apresente:

```
✅ Concluído: criativo gerado e salvo.

Imagem: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-aida-{numero}.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-aida-{numero}.md
```

Se o script falhar (erro de chave, de rede ou de modelo), avise o aluno em linguagem simples, mostre o prompt consolidado e ofereça gerar pelo modo ChatGPT.

#### Depois de gerar — modo ChatGPT

```
Quer ajustar algum dos 3 passos?
1. Trocar a cena
2. Mudar a cor ou o layout
3. Reescrever o texto
```

#### Depois de gerar — modo API

```
Quer fazer mais alguma coisa?

1. Gerar em outro formato a partir da arte atual (image-to-image)
2. Trocar a cena
3. Mudar a cor ou o layout
4. Reescrever o texto
```

##### Sub-fluxo "Gerar em outro formato" (opção 1 do menu API)

Quando o aluno escolher 1, pergunte qual formato gerar (excluindo o que já foi feito na entrevista inicial):

```
Qual formato você quer gerar a partir da arte atual?

[Listar somente os 2 formatos que NÃO foram gerados]
- Feed retrato (4:5, 1080x1350)
- Quadrado (1:1, 1080x1080)
- Stories ou Reels (9:16, 1080x1920)

Digite o número:
```

Depois execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-criativo-aida-{numero}-{novo-formato}.txt`. Onde `{novo-formato}` é `feed`, `quadrado` ou `stories`:

```
Recompose this exact same creative for a {NOVO_ASPECT} canvas. Keep the same scene, same person, same colors, same text content, same on-image text, same elements, same design language. Only recompose the framing to fill the new proportion. Do not redesign, do not change typography, do not change wording. Only adapt the proportion.
```

Substitua `{NOVO_ASPECT}` por:
- `vertical 9:16 Instagram Stories and Reels (1080x1920)` se Stories
- `square 1:1 (1080x1080)` se Quadrado
- `vertical 4:5 Instagram Feed (1080x1350)` se Feed

b) Anuncie:

```
🔍 Próximo passo: gerar a versão em outro formato a partir da arte atual. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no passo Modo API, passando a arte atual como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-criativo-aida-{numero}-{novo-formato}.txt" --model "{modelo}" --aspect "{novo-aspect}" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-aida-{numero}.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-aida-{numero}-{novo-formato}.png"
```

Onde `{novo-aspect}` é `4:5`, `1:1` ou `9:16` conforme o formato escolhido.

d) Confirme:

```
✅ Concluído: versão em novo formato gerada e salva.

Imagem: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-aida-{numero}-{novo-formato}.png
```

e) Reapresente o menu de 4 opções, removendo a opção 1 se o aluno já gerou todos os formatos disponíveis.

### 7. Modo Iterativo

Se o usuário quiser refinar um passo específico depois de salvar:

```
Qual passo quer ajustar?

1. Passo 1: imagem de fundo (trocar a cena)
2. Passo 2: layout e cores (ajustar zonas, fontes ou paleta)
3. Passo 3: texto da imagem (kicker, headline, apoio ou botão)

O que quer mudar?
```

Ajuste apenas o passo solicitado, atualize os arquivos mantendo os outros passos intactos. No modo API, atualize o arquivo de prompt e rode o script de novo para gerar a imagem com o ajuste.

## Regras

- Não escrever texto antes do Passo 2 estar definido. O texto do Passo 3 depende dos limites de caractere definidos no layout.
- Nunca inventar urgência. A urgência base vem obrigatoriamente das Urgências Ocultas do perfil.
- Prompt do Passo 1 sempre em inglês, adaptado ao formato nativo da ferramenta escolhida.
- Light Copy obrigatória no Passo 3: sem travessão, sem ponto de exclamação, sem pergunta, sem promessa vaga.
- Auto-revisão obrigatória de copy (Manual + revisora) antes de mostrar as versões ao usuário.
- O número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- No Passo 1, mostrar apenas descrições em português para as 3 opções. O prompt em inglês da cena escolhida é derivado internamente e incluído somente no prompt consolidado final.
- Passo 3 gera SEMPRE 2 versões completas (kicker+headline+apoio+botão juntos), nunca opções isoladas por zona.
- Prompt final consolidado usa linguagem visual espacial (upper area, lower band, centered). NUNCA incluir porcentagens numéricas. Porcentagens são apenas para cálculo interno do limite de caracteres no Passo 2.
- Sujeito humano no prompt do Passo 1 deve estar vestido de forma adequada para anúncios. Especificar a roupa explicitamente no prompt. Nunca omitir a vestimenta.
- CTA: o padrão é "Saiba mais". Se o usuário indicou outro em qualquer momento, usar esse. Nunca inventar.
- Headline: sempre em CAIXA ALTA (ALL CAPS), max 30 chars, todo na cor de destaque brilhante da categoria. Nunca warm white. Nunca destacar só uma palavra.
- Texto no Passo 3: sem sombra. O fundo escuro natural e a cor saturada do headline garantem contraste.
- Kicker: tensão presente ou padrão recorrente ainda ativo. Nunca derrota passada concluída. Voz de monólogo interno do leitor, não narrador. Captura o MOMENTO ESPECÍFICO da cena do Passo 1.
- Apoio sem jargão técnico: nunca usar nomes de categorias (grupo alimentar, sedentarismo, gestão emocional, renda passiva). Usar palavras específicas que a pessoa usa no dia a dia.
- Cenas de dor: preferir objetos, mãos ou detalhe de costas. Silhueta com postura caída e luz fria gera imagem de derrota (estado fechado).
- Opções do Passo 1: cada cena deve usar pelo menos um elemento visual concreto do nicho. Proibido cenas genéricas que poderiam servir para qualquer produto.
- Opções do Passo 1: as 3 opções devem diferir em técnica de composição, não apenas em "tom emocional".
- Modo API: gravar o prompt consolidado num arquivo .txt em UTF-8 e chamar `scripts/gerar-criativo-estatico.py`. O modelo de imagem gera a arte inteira (cena e texto) numa só chamada. Sem template HTML, sem composição.
- Modo API: modelo da opção 1 é `openai/gpt-5.4-image-2` (recomendado), da opção 2 é `google/gemini-3.1-flash-image-preview`. Proporção conforme o formato: feed retrato 4:5, quadrado 1:1, stories 9:16.
