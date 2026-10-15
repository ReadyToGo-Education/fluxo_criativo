# Quadrinho (Jornada em 4 quadros ou Paródia em 3 quadros). Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 29 (Quadrinho). Gera um anúncio em história em quadrinhos ilustrada, em um de dois estilos:

- **Jornada em 4 quadros:** uma única protagonista, com a cara do público, vive a transformação do produto em um grid 2x2: problema, descoberta, aplicação e resultado. Faixa da marca no topo.
- **Paródia em 3 quadros:** uma cena famosa de filme, série ou novela, recriada em 3 faixas empilhadas, com a fala icônica adaptada para a oferta e o nome do produto na resposta final. Faixa de oferta na base.

Quem escolhe o estilo é o Claude, a partir de critérios do produto e do momento do anúncio. Ele mostra a recomendação com o motivo e o aluno confirma com um número (mesmo padrão do Framework Quiz vs. Página do CLAUDE.md).

O entregável final é a legenda e três prompts prontos: Feed e Stories no ChatGPT, e animação no Freepik (Magnific). No fim, o aluno escolhe gerar a imagem colando o prompt ou direto pela API.

**Diferença pro formato 15 (Criativo História + Quebra de Objeção):** o formato 15 usa fotos realistas, título no topo e um diálogo entre duas pessoas para quebrar uma objeção. Este formato (29) é ilustração de quadrinho, sem título no topo, e conta uma jornada (uma protagonista) ou parodia uma cena famosa (dois personagens). Quando o aluno pedir "quebra de objeção", "diálogo 4 quadros" ou "fotos reais", use o formato 15.

**Por que esse formato funciona:**
Quadrinho é lido como conteúdo, não como propaganda. A Jornada mostra o produto funcionando na vida de alguém parecido com o leitor, então ele entende o que é e se vê no último quadro. A Paródia pega carona numa cena que o público já tem na memória: o cérebro completa a fala original sozinho e a troca pela oferta vira a piada, o que prende atenção e é compartilhado.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (resumo-produto.md, tipo.md, preco.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `resumo-produto.md` ou inferido do slug).
- **Nicho e Quadro**: do `resumo-produto.md`.
- **Público**: do `resumo-produto.md` (seção "Público"), com faixa etária e gênero predominante. A faixa etária decide quais cenas famosas o público reconhece.
- **Furadeira**: nome do método e as macroetapas, resumidas em até 2 palavras cada. Vão para a tela do quadro 2 da Jornada.
- **Dores e Urgências Quentes**: das Urgências Ocultas. Alimentam o quadro 1 da Jornada.
- **Decorados principais**: alimentam o quadro 4 da Jornada.
- **Tom do comunicador**: da Identidade do Comunicador (tom, referências, o que evitar). Decide se o humor da Paródia combina com a marca.
- **Paleta do produto**: se já existe (procure `COLOR PALETTE` em `meus-produtos/{ativo}/entregas/furadeira/prompt-furadeira.md` ou as cores de uma página já gerada), use. Se não existe, use a tabela de cores por nicho no fim deste arquivo.

**Imagem de referência:** se o aluno mandou uma imagem de quadrinho como referência, ela manda no estilo. Grid 2x2 com uma protagonista é Jornada. Três faixas empilhadas com cena de filme é Paródia. Nesse caso, pule a decisão do Passo 2 e só confirme em uma linha qual estilo vai seguir. Guarde a imagem: no modo API, ela vai junto como referência de estilo (Passo 8b).

### 1. Apresentar resumo do contexto e confirmar

SEMPRE mostre o resumo, mesmo se algum campo veio de inferência:

```
Vou usar estes dados do seu produto ativo ({slug}):

Produto: [nome do produto]
Quadro: [Quadro]
Público: [resumo do público, com faixa etária]
Método: [nome da Furadeira e as macroetapas resumidas]
Tom do comunicador: [tom]

(Marque "✓ do perfil" pros campos extraídos diretamente do resumo-produto.md.
Marque "○ inferido" pros campos que foram um chute a partir do slug, tipo ou preço.)

Está tudo certo?

1. Sim, está certo, pode seguir
2. Quero ajustar algum campo
```

Se escolher 2, pergunte qual campo ajustar e refaça só a parte indicada.

### 2. Escolher o estilo (o Claude recomenda, o aluno confirma)

Pule este passo se o aluno já pediu um estilo de forma explícita ("quadrinho de 4", "jornada", "paródia", "cena de filme", "3 quadros") ou mandou uma imagem de referência. Nesse caso, confirme o estilo em uma linha e siga.

#### 2.1 Pergunta do momento do anúncio

É o único dado que quase nunca está no perfil. Se o aluno ainda não disse, pergunte:

```
Esse anúncio vai rodar em qual momento?

1. Campanha com oferta especial (Black, desconto, 2 por 1, bônus com prazo)
2. Divulgação contínua para quem ainda não conhece o produto
3. Remarketing para quem já conhece e ainda não comprou

Digite o número:
```

#### 2.2 Aplicar os critérios

| Critério | JORNADA (4 quadros) | PARÓDIA (3 quadros) |
|---|---|---|
| Momento do anúncio | Divulgação contínua, sem oferta especial | Campanha com oferta especial |
| Quem vai ver | Quem ainda não conhece o produto (Descoberta ou Relacionamento na Mandala) | Quem já conhece e não comprou (Conversão ou RMKT) |
| O que o público precisa | Entender o que o produto é e como funciona (nível de consciência até 3) | Um motivo para comprar agora (nível 4 ou 5) |
| Tom do comunicador | Sério, didático ou acolhedor, sem espaço para piada | Aceita humor e referência de cultura pop |
| Cena famosa que encaixa | Nenhuma encaixa sem forçar | Existe uma cena que a faixa etária do público reconhece em 1 segundo e que comporta a oferta ou o produto |

**Regra:** 3 ou mais critérios para o mesmo lado, siga ele. Critério sem informação fica de fora da conta. **Desempate: JORNADA**, porque não depende de o público reconhecer a cena nem de a marca aceitar humor.

Para o último critério, pense rápido em 2 ou 3 cenas candidatas antes de decidir. Se nenhuma encaixa sem forçar, o critério vai para a Jornada.

#### 2.3 Apresentar a recomendação

```
Recomendo o estilo **[estilo]** para este anúncio:

- Momento: [resposta do aluno]. Pesa para [estilo].
- Quem vai ver: [público]. Pesa para [estilo].
- O que o público precisa: [leitura]. Pesa para [estilo].
- Tom do comunicador: [tom]. Pesa para [estilo].
- Cena famosa: [cena candidata ou "nenhuma encaixa"]. Pesa para [estilo].

1. Seguir com [estilo recomendado] (recomendado)
2. Usar [outro estilo]

Digite o número:
```

Se o aluno escolher o estilo não recomendado, siga sem discutir.

---

### 3A. Jornada em 4 quadros: perguntas

Faça UMA pergunta por mensagem, nesta ordem. Pule a pergunta cuja resposta o aluno já deu.

**Pergunta 1. Situação de abertura (quadro 1)**

Gere 4 situações a partir das Dores e Urgências Quentes do produto. Cada uma é uma cena concreta, com objeto, número ou momento do dia. Marque a recomendada com o motivo em poucas palavras:

```
Que situação abre a história no quadro 1?

1. [situação] (recomendado: [motivo curto])
2. [situação]
3. [situação]
4. [situação]

Digite o número:
```

**Pergunta 2. Faixa do topo**

```
O que vai na faixa do topo?

1. [nome da campanha] + [nome do produto]   (só mostre se o momento for campanha com oferta)
2. [formato do produto, ex: "Desafio 14 dias"] + [nome do produto]
3. Só a marca [nome do produto]
4. Outra (me diga o texto)

Digite o número:
```

**Pergunta 3. Protagonista**

Use a faixa etária e o gênero predominante do público:

```
Quem é a protagonista?

1. [descrição a partir do público, ex: "Mulher de uns 30 anos, profissional em ascensão"]
2. [variação com o outro gênero]
3. Outra (me descreva)

Digite o número:
```

### 4A. Jornada em 4 quadros: roteiro

Anuncie:

```
🔍 Próximo passo: gerar o roteiro do quadrinho em 4 quadros. Tempo estimado: cerca de 30 segundos.
```

#### Estrutura obrigatória

- **Quadro 1, PROBLEMA.** Balão de PENSAMENTO. A dor concreta escolhida na Pergunta 1, com número ou cena real. O produto não aparece aqui.
- **Quadro 2, DESCOBERTA.** Balão de fala começando com reação ("Olha só..."). Diz o formato e um ganho concreto (prazo, minutos por dia, número). A personagem olha uma tela (notebook ou celular) que mostra o nome do produto e 3 cartões com as macroetapas da Furadeira, até 2 palavras cada.
- **Quadro 3, APLICAÇÃO.** Balão de fala com o primeiro ganho percebido, retomando a dor do quadro 1, e o nome do produto ("Treinei com o [produto]"). Expressão confiante, pode piscar o olho.
- **Quadro 4, RESULTADO.** Balão de fala com o Quadro conquistado e um Decorado (o que muda na vida), com prazo concreto, fechando a cena do quadro 1. Abaixo do balão, uma linha menor: "Se você também [dor curta], clique em [CTA]." e um botão com o CTA.

#### Regras do roteiro

- Até 16 palavras por balão. Se passar, corte.
- Um trecho de destaque por balão (marca-texto na cor de destaque), sempre a palavra mais concreta: número, prazo ou nome do produto.
- O resultado do quadro 4 não promete mais do que o Quadro e os Decorados do perfil prometem.
- Sem travessão, sem exclamação, sem "mesmo que", sem "sem precisar", sem lero-lero.
- A mesma protagonista nos 4 quadros, com o mesmo rosto, o mesmo cabelo e a mesma roupa.

#### Formato de apresentação

```
Resumo do que vou criar:

- Produto: [nome]
- Formato: quadrinho ilustrado de 4 quadros (Jornada)
- Tamanhos: Feed (4:5) e Stories (9:16)
- Protagonista: [descrição]
- Cores: [paleta e de onde veio]
- Chamada: [CTA]

Faixa do topo: [descrição]

Quadro 1 ([cena])
💭 "[fala]"

Quadro 2 ([cena, com o que aparece na tela])
💬 "[fala]"

Quadro 3 ([cena])
💬 "[fala]"

Quadro 4 ([cena])
💬 "[fala]"
Linha menor: "[linha]"
Botão: [CTA]

Os trechos em negrito ganham o marca-texto na cor de destaque.

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

Marque em negrito, dentro de cada fala, o trecho de destaque. Se o aluno pedir ajuste, refaça só a parte indicada e volte a este gate.

---

### 3B. Paródia em 3 quadros: perguntas

**Pergunta 1. Oferta**

Se o momento for campanha com oferta, pergunte:

```
Qual é a oferta, do jeito que ela vai aparecer na arte?
(ex: "2 pós-graduações pelo preço de 1, Esquenta Black", "Desafio por R$ 47 só até domingo")
```

A oferta precisa ter número ou condição concreta (preço, quantidade, prazo). Se vier vaga ("preço especial"), peça o número.

Se não houver oferta (remarketing ou divulgação), a punchline usa o nome do produto e o Quadro, e a faixa da base traz o Quadro como headline e a marca no selo. Não pergunte nada; avise em uma linha.

**Pergunta 2. As 10 cenas**

Anuncie:

```
🔍 Próximo passo: gerar 10 cenas famosas adaptadas para a sua oferta. Tempo estimado: cerca de 60 segundos.
```

Gere 10 cenas de filmes, séries, novelas ou programas de TV que a faixa etária do público reconhece em 1 segundo. Misture produções internacionais conhecidas no Brasil com produções brasileiras (novelas, filmes nacionais, programas de TV). Cada cena vira 3 falas:

- **Quadro 1, FALA ICÔNICA ADAPTADA.** O personagem A diz a fala famosa com o começo idêntico ao original e o final trocado pela oferta ou pelo benefício. É uma afirmação, nunca pergunta.
- **Quadro 2, FALA ORIGINAL.** O personagem B responde com a fala original da cena, igual ou quase igual. É ela que confirma a referência na cabeça de quem lê.
- **Quadro 3, PUNCHLINE.** O personagem A responde com o nome do produto ou a campanha, em até 7 palavras.

**Regras das cenas:**

- A fala icônica precisa ser conhecida de verdade. Se você não tem certeza do diálogo original, não use a cena.
- O diálogo cabe em 3 falas entre 2 personagens. Cena que depende de áudio, música ou movimento para ter graça não entra.
- A piada nasce da troca no final da fala do quadro 1. Se precisar de explicação, a cena não funciona.
- Fora da lista: violência, arma, sangue, morte explícita, conteúdo sexual, drogas, política partidária e religião. Filme de suspense ou terror pode entrar quando a cena escolhida mostra só expressão e ambiente.
- O nome do produto entra só no quadro 3 e na faixa da base, nunca no quadro 1.

Formato da listagem:

```
Aqui estão 10 cenas famosas adaptadas para a sua oferta.

---

**1. [Obra] ([ano])**
Cena original: [quem fala com quem, onde]
Diálogo original: "[fala 1]" / "[fala 2]" / "[fala 3]"
Quadro 1: "[fala 1 adaptada]"
Quadro 2: "[fala 2]"
Quadro 3: "[punchline]"

---

**2. ...**

---
Escolha uma cena.
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

### 4B. Paródia em 3 quadros: roteiro

Anuncie:

```
🔍 Próximo passo: gerar o roteiro da paródia em 3 quadros. Tempo estimado: cerca de 30 segundos.
```

#### Personagens sem rosto de ator

A arte recria o CLIMA da cena (cenário, enquadramento, luz, figurino, idade e postura dos personagens) com personagens originais. Nunca peça o rosto, o nome ou a semelhança de um ator ou pessoa real, e nunca coloque o nome ou o logo da obra na arte. O reconhecimento vem da fala e da composição, não do rosto.

**Por quê:** o ChatGPT recusa ou deforma rostos de famosos, e usar a imagem de um ator num anúncio pago abre problema de direito de imagem e de reprovação na Meta.

#### Formato de apresentação

```
Resumo do que vou criar:

- Produto: [nome]
- Formato: quadrinho de paródia em 3 quadros
- Cena: [obra], [momento da cena]
- Tamanhos: Feed (4:5) e Stories (9:16)
- Estilo: ilustração semi-realista de graphic novel, luz [clima da cena]
- Chamada: [CTA]

Personagem A: [descrição genérica: idade, cabelo, roupa]
Personagem B: [descrição genérica]
Cenário: [cenário]

Quadro 1 ([enquadramento e expressão de A])
💬 "[fala]"

Quadro 2 ([enquadramento e expressão de B])
💬 "[fala]"

Quadro 3 ([enquadramento e expressão de A])
💬 "[fala, com o trecho da marca ou da oferta em negrito]"

Faixa da base:
- Headline: "[headline da oferta, com o número em negrito]"
- Selo: "[nome da campanha ou da marca]"
- Botão: "[CTA] >"

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

Se o aluno pedir ajuste, refaça só a parte indicada e volte a este gate.

---

### 5. Gerar legenda e prompts

Quando o aluno aprovar o roteiro (e o CTA estiver definido, ver Regras), anuncie:

```
🔍 Próximo passo: gerar a legenda e os prompts do quadrinho para Feed e Stories. Tempo estimado: cerca de 30 segundos.
```

#### A) Legenda pro Instagram

Mínimo 3 linhas, tom de creator. Na Jornada, conta em primeira pessoa o que muda quando a dor do quadro 1 vai embora. Na Paródia, brinca com a referência em uma linha e entrega a oferta com o número. Termina com a chamada do CTA escolhido. Produto fora das primeiras linhas, sem emoji no meio do texto (só o emoji final do CTA, como "👇").

#### B) Prompt Feed (4:5)

Use o modelo do estilo escolhido. Substitua todos os placeholders pelos dados reais. **O texto final ao aluno não pode ter colchetes.**

**Modelo Jornada (4 quadros):**

````
Cria pra mim uma arte de anúncio pra Instagram no formato HISTÓRIA EM QUADRINHOS ILUSTRADA, com 4 quadros e uma única protagonista.

Se eu anexei uma imagem junto com este pedido, use ela SÓ como referência de estilo e de diagramação (traço, cores chapadas, balões, faixa no topo, grid 2x2). Não copie nenhum texto, logo, marca ou personagem dela.

ESTILO VISUAL:
Ilustração estilo cartoon moderno, traço preto grosso e limpo, cores chapadas com sombreamento suave, expressões faciais bem marcadas, visual leve e acolhedor. Nada de foto, nada de 3D.

PALETA (usar exatamente):
- [COR PRINCIPAL COM HEX]
- [COR DE DESTAQUE COM HEX], no marca-texto dos balões e no botão
- [COR ESCURA COM HEX], na faixa do topo
- Branco nos balões

ESTRUTURA, de cima para baixo:

1. FAIXA DO TOPO (cerca de 9% da altura):
Fundo [COR ESCURA], largura total. Centralizado: [ÍCONE SIMPLES LIGADO AO NICHO] na cor de destaque e o texto "[TEXTO DA FAIXA]" em fonte sans-serif extra-bold branca[, com "[TRECHO]" na cor de destaque]. Nada mais na faixa.

2. GRID 2x2 DE QUADROS (logo abaixo da faixa, até a base da arte):
4 quadros com borda preta grossa e um espaço branco fino entre eles. A mesma protagonista aparece nos 4 quadros, sempre com o mesmo rosto, o mesmo cabelo e a mesma roupa.

PROTAGONISTA: [DESCRIÇÃO: nome, idade, cabelo, pele, roupa]. Aparência arrumada e cuidada, de pessoa comum de classe média. Roupa sempre coberta, sem decote.

QUADRO 1 (superior esquerdo):
Cena: [CENA DO PROBLEMA].
Balão de PENSAMENTO (nuvem com bolinhas) com o texto:
"[FALA DO QUADRO 1]"
Destaque: o trecho "[TRECHO]" com marca-texto na cor de destaque atrás das letras.

QUADRO 2 (superior direito):
Cena: [CENA DA DESCOBERTA]. Na tela do [NOTEBOOK OU CELULAR] aparece o título "[NOME DO PRODUTO]" e 3 cartões lado a lado, cada um com um ícone simples e os rótulos "[ETAPA 1]", "[ETAPA 2]" e "[ETAPA 3]".
Balão de FALA:
"[FALA DO QUADRO 2]"
Destaque na cor de destaque em "[TRECHO]".

QUADRO 3 (inferior esquerdo):
Cena: [CENA DA APLICAÇÃO].
Balão de FALA:
"[FALA DO QUADRO 3]"
Destaque na cor de destaque em "[TRECHO]".

QUADRO 4 (inferior direito):
Cena: [CENA DO RESULTADO].
Balão de FALA:
"[FALA DO QUADRO 4]"
Destaque na cor de destaque em "[TRECHO]".
Abaixo do balão, alinhada à esquerda do quadro, uma linha menor em [COR ESCURA]: "[LINHA MENOR]"
Logo abaixo, também alinhado à esquerda do quadro, um botão arredondado na cor de destaque com o texto "[CTA]" em [COR ESCURA], extra-bold.

TEXTOS:
- Fonte dos balões: sans-serif bold, preta, grande e legível.
- Balões brancos com contorno preto e rabinho apontando para a protagonista.
- Escrever cada texto EXATAMENTE como está acima, com todos os acentos (á, é, í, ó, ú, ã, õ, ç). Não inventar, não resumir, não traduzir.
- PROIBIDO travessão (— ou –) e ponto de exclamação.
- Sem logos de redes sociais, sem marca d'água, sem nenhum texto extra.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Exact size reference: 1080x1350. Do NOT create a 9:16 composition. SAFE ZONE: the bottom 12% of the image may contain only illustration (panel backgrounds and characters), never balloons, text or the button, because the Meta Ads feed overlay covers this area. In the two right-hand panels, keep balloons, text and the button out of the rightmost 15% of the image width, so the same art also works in Stories. LEGIBILITY: all text must be large, bold, high contrast and easy to read on a phone screen at arm's length. Never shrink the font to fit more content.
````

**Modelo Paródia (3 quadros):**

````
Cria pra mim uma arte de anúncio pra Instagram no formato QUADRINHO DE PARÓDIA, com 3 quadros empilhados e uma faixa de oferta na base.

Se eu anexei uma imagem junto com este pedido, use ela SÓ como referência de estilo e de diagramação. Não copie nenhum texto, logo, marca ou personagem dela.

A arte recria o clima de uma cena famosa de [FILME, SÉRIE OU NOVELA], com personagens originais. NÃO desenhe o rosto de nenhum ator ou pessoa real e não escreva o nome da obra. Os personagens lembram o papel só pela idade, pela roupa, pelo cenário e pela luz.

ESTILO VISUAL:
Ilustração semi-realista estilo graphic novel pintada, contorno marcado, luz cinematográfica [CLIMA DA LUZ], expressões faciais fortes e fiéis à emoção de cada fala. Nada de foto, nada de 3D, nada de cartoon infantil.

ESTRUTURA, de cima para baixo:

1. TRÊS QUADROS EMPILHADOS (cerca de 76% da altura):
Três faixas horizontais, cada uma com a largura toda da arte, separadas por uma borda escura fina. Em cada quadro, o personagem fica do lado esquerdo e o balão de fala fica do lado direito, sem passar de 85% da largura da arte.

CENÁRIO: [CENÁRIO DA CENA].
PERSONAGEM A: [DESCRIÇÃO GENÉRICA: idade, cabelo, roupa]. Aparece nos quadros 1 e 3, com o mesmo rosto e a mesma roupa.
PERSONAGEM B: [DESCRIÇÃO GENÉRICA]. Aparece no quadro 2.

QUADRO 1 (topo): [ENQUADRAMENTO E EXPRESSÃO DE A].
Balão: "[FALA DO QUADRO 1]"

QUADRO 2 (meio): [ENQUADRAMENTO E EXPRESSÃO DE B].
Balão: "[FALA DO QUADRO 2]"

QUADRO 3 (último quadro): [ENQUADRAMENTO E EXPRESSÃO DE A, igual ao quadro 1].
Balão: "[FALA DO QUADRO 3]", com "[TRECHO DA MARCA OU DA OFERTA]" em [COR DE DESTAQUE].

Balões brancos com contorno preto e rabinho apontando pro personagem. Texto em CAIXA ALTA, sans-serif bold condensada, preta, grande e legível.

2. FAIXA DE OFERTA (cerca de 24% da altura, na base):
Fundo [COR ESCURA] com um brilho sutil.
À esquerda, em duas linhas: "[HEADLINE DA OFERTA]" em fonte extra-bold branca, com "[NÚMERO OU PALAVRA-CHAVE]" em [COR DE DESTAQUE].
À direita, separado por uma linha vertical fina: "[SELO: CAMPANHA OU MARCA]" em fonte extra-bold branca.
Abaixo, centralizado, um botão arredondado em [COR DE DESTAQUE] com o texto "[CTA] >" em preto, extra-bold.

TEXTOS:
- Escrever cada texto EXATAMENTE como está acima, com todos os acentos (á, é, í, ó, ú, ã, õ, ç). Não inventar, não resumir, não traduzir.
- PROIBIDO travessão (— ou –) e ponto de exclamação.
- Sem nome ou logo da obra, sem logos de redes sociais, sem marca d'água, sem nenhum texto extra.
- Sem sangue, arma, ferida ou criatura assustadora, mesmo que a cena original seja de suspense.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Exact size reference: 1080x1350. Do NOT create a 9:16 composition. SAFE ZONE: the bottom 12% of the image shows only the plain background of the offer bar, with no text and no button, because the Meta Ads feed overlay covers this area: place the offer text and the button above it. LEGIBILITY: all text must be large, bold, high contrast and easy to read on a phone screen at arm's length. Never shrink the font to fit more content.
````

#### C) Prompt Stories (9:16)

Fixo por estilo, sem placeholders. Vai no mesmo chat do ChatGPT depois que a arte do Feed ficar pronta.

**Stories da Jornada** (a arte fica inteira, centralizada, com faixas lisas em cima e embaixo, como nos anúncios de referência):

````
Agora cria a mesma arte pro formato Stories, sem redesenhar nada: mesma ilustração, mesmos 4 quadros, mesmos textos, mesmas cores, mesma faixa do topo.

Coloque a arte inteira centralizada num canvas vertical 9:16, ocupando toda a largura. Preencha o espaço que sobra em cima e embaixo com faixas lisas na mesma cor escura da faixa do topo, sem nenhum texto, ícone ou elemento nelas.

IMPORTANT: exact 9:16 vertical canvas, 1080x1920. The comic art keeps its original proportion and is centered vertically. The top and bottom bars are plain, with nothing on them, because the Instagram profile bar and the Meta Ads overlay cover those areas. Do not change any text, do not add text, do not crop the panels.
````

**Stories da Paródia** (os 3 quadros ficam mais altos para ocupar a tela):

````
Agora cria a mesma arte pro formato Stories: mesmos 3 quadros, mesmos personagens, mesmas falas, mesmas cores, mesma faixa de oferta. Os quadros podem ficar mais altos pra ocupar a tela.

IMPORTANT: exact 9:16 vertical composition for Instagram Stories and Reels, 1080x1920. SAFE ZONE: the top eighth of the height shows only background, with no text, because the Instagram profile bar covers it. The bottom seventh of the height shows only the plain background of the offer bar, with no text and no button, because the Meta Ads overlay and the native button cover it: place the offer text and the button above that area. Keep every balloon, text and button out of the right quarter of the canvas, because the Instagram action icons cover that side: in the panels, each balloon sits between the character and three quarters of the width; in the offer bar, stack the headline, the seal and the button left-aligned instead of side by side. Do not change any wording. Never let text touch the edges.
````

#### D) Prompt de Animação pro Freepik (Magnific)

Serve para os dois estilos, no Feed e no Stories:

````
Animate this comic-style image with extremely subtle, slow, idle motion inside each panel. DO NOT change anything in the image: keep the exact same artwork, composition, framing, panel layout, panel borders, characters, facial expressions, poses, lighting and colors.

DO NOT add, remove, move, redraw, restyle or modify any text. Every speech balloon (with its exact text, font, color, position and shape), the top bar or the offer bar, and the button must remain 100% STATIC and UNCHANGED. No text animation, no text fade, no bubble morphing.

Only animate the characters with EXTREMELY SUBTLE idle motion: very light breathing and one slow blink every 2 to 3 seconds, keeping each facial expression frozen exactly as in the original. Background details may have a tiny ambient motion (lamp light flicker, curtain, steam), nothing else.

CRITICAL CONSTRAINTS: no camera movement, no zoom, no pan, no shake. Do not add objects, people, particles or text. Do not break the panel borders. Output: a seamless looping video, same aspect ratio as the input image (4:5 for Feed, 9:16 for Stories), 3 to 5 seconds, 24 fps.
````

### 6. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) na legenda. Corrigir direto. Nunca mostrar versão bruta.

As falas dos quadros, a linha menor, a headline da oferta e o CTA NÃO passam pela revisora (são conteúdo da arte com tom próprio), mas respeitam Light Copy: sem travessão, sem exclamação, sem promessa vaga, sem "mesmo que" e sem "sem precisar". Pergunta só é permitida no quadro 2 da Paródia, porque é a fala original da cena.

### 7. Apresentação e aprovação

```
Pronto. Aqui está o seu quadrinho ([estilo]):

📝 LEGENDA PRO INSTAGRAM
[legenda]

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

📱 PROMPT PRO CHATGPT, FORMATO STORIES
[prompt Stories do estilo, dentro de bloco de código]

🎬 PROMPT DE ANIMAÇÃO PRO FREEPIK (MAGNIFIC)
[prompt de animação, dentro de bloco de código]

Dica: se você tem uma imagem de quadrinho de referência, anexe ela junto com o
prompt do Feed no ChatGPT. O traço fica bem mais parecido.

---
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher [outra situação de abertura | outra das 10 cenas]
```

Se escolher 2, pergunte o que ajustar e refaça só a parte indicada. Se escolher 3, volte à lista correspondente do estilo.

**Revisão da arte gerada:** se o aluno mandar a imagem que o ChatGPT gerou, confira quadro por quadro: texto escrito igual ao roteiro e com acentos, destaques nos trechos certos, mesmo rosto e mesma roupa nos quadros, rosto de ator real (na Paródia), CTA fora do rodapé coberto pelo Meta e texto fora da borda direita. Aponte o que está certo, liste os pontos de atenção e ofereça um prompt curto de correção para colar no mesmo chat.

### 8. Gerar e salvar

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-quadrinho-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-quadrinho-{numero}.md`

Conteúdo do arquivo:

```markdown
# Quadrinho nº {numero} ([Jornada em 4 quadros | Paródia em 3 quadros])

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Público:** [público]
**Momento do anúncio:** [resposta do Passo 2.1]
**Por que este estilo:** [os critérios do Passo 2.2, em uma linha cada]
**Cores:** [paleta e de onde veio]

## Roteiro

[roteiro aprovado, no formato do Passo 4A ou 4B]

## Legenda pro Instagram

[legenda]

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt pro ChatGPT. Formato Stories (1080x1920, 9:16)

\`\`\`
[prompt Stories do estilo]
\`\`\`

## Prompt de Animação pro Freepik (Magnific) (serve pro Feed e pro Stories)

\`\`\`
[prompt de animação]
\`\`\`

## Como usar

1. Abra o ChatGPT (com geração de imagem habilitada).
2. Cole o **Prompt Feed**. Se tiver uma imagem de quadrinho de referência, anexe junto.
3. Quando a arte estiver pronta, mande "ok" no chat.
4. Cole o **Prompt Stories** pra gerar a versão vertical da mesma arte.
5. Pra animar, abra o Freepik (Magnific) no modo vídeo, suba a imagem gerada, defina a MESMA imagem como quadro inicial e quadro final e cole o **Prompt de Animação**. Modelo recomendado: Google Veo Lite (melhor custo-benefício).

## Banco completo desta sessão

[Jornada: as 4 situações de abertura geradas. Paródia: as 10 cenas geradas, com diálogo original e adaptação. Assim o aluno usa depois sem rodar a sub-skill de novo.]
```

### 8b. Modo API (só se o aluno escolheu a opção 2)

Depois de salvar o `.md`, gere apenas a imagem do Feed pela API. A versão Stories sai depois, como opção no menu do Passo 9, reaproveitando a imagem do Feed como referência visual.

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

Opção 1 vira `openai/gpt-5.4-image-2`, opção 2 vira `google/gemini-3.1-flash-image-preview`. Guarde o modelo escolhido, ele vai ser reaproveitado se o aluno pedir Stories no Passo 9.

3. Grave o Prompt Feed num arquivo `.txt` na pasta de criativos, com o nome `prompt-quadrinho-{numero}-feed.txt`. Conteúdo é o Prompt Feed apresentado ao aluno, sem alterações.

4. Se o aluno mandou uma imagem de quadrinho como referência de estilo (PNG, JPG ou WEBP), copie para a pasta de criativos como `referencia-quadrinho-{numero}.{extensão}` e passe com `--reference-image` no comando abaixo. O prompt já instrui o modelo a usar a imagem só como estilo.

5. Anuncie e rode o script no formato Feed (4:5):

```
🔍 Próximo passo: gerar a imagem do Feed via API. Tempo estimado: 2 a 3 minutos.
```

Use o comando Python correto da sessão (`python3` ou `py -3`), conforme a seção Execução de Scripts Python do CLAUDE.md.

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-quadrinho-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-quadrinho-{numero}-feed.png"
```

Com imagem de referência, acrescente `--reference-image "meus-produtos/{ativo}/entregas/criativos/referencia-quadrinho-{numero}.{extensão}"`.

6. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

7. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 9 e usa a imagem do Feed como referência (image-to-image).

### 9. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: quadrinho salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-quadrinho-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo, com a imagem de referência anexada se tiver.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

Depois ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro quadrinho no mesmo estilo (outra situação ou outra cena)
2. Gerar um quadrinho no outro estilo
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: quadrinho gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-quadrinho-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-quadrinho-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro quadrinho no mesmo estilo (outra situação ou outra cena)
3. Gerar um quadrinho no outro estilo
4. Voltar e escolher outro formato de criativo
```

#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos, com o nome `prompt-quadrinho-{numero}-stories.txt`, o Prompt Stories do estilo (Passo 5C), trocando a primeira frase por: "Recompose this exact same comic for a vertical 9:16 canvas, without redrawing the panels or changing any wording."

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 8b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-quadrinho-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-quadrinho-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-quadrinho-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-quadrinho-{numero}-stories.png
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

**Opção 1. Colar o prompt numa ferramenta externa:** entregue o Prompt de Animação do Passo 5D. Instrua: "Abra o Freepik (Magnific) no modo vídeo, suba a imagem gerada e defina a MESMA imagem como quadro inicial e quadro final, isso fecha o loop sem salto. Cole o prompt e gere. Modelo recomendado: Google Veo Lite, melhor custo-benefício." Se o aluno for usar outro modelo de vídeo, adapte o prompt às características dele antes de entregar (instruções mais restritivas ou prompt negativo, quando o modelo aceitar).

**Opção 2. Higgsfield pelo conector:** use as ferramentas MCP do Higgsfield para gerar o vídeo image-to-video: envie a imagem gerada e o Prompt de Animação, pedindo loop com a mesma imagem como quadro inicial e quadro final quando a ferramenta aceitar. Salve o vídeo na pasta de criativos com o sufixo `-loop.mp4`, no mesmo padrão da Opção 3. Requer assinatura ativa do Higgsfield.

**Opção 3. Automático via Replicate (API):** execute:

a) Grave o Prompt de Animação num arquivo `.txt` na pasta de criativos, com o nome `prompt-quadrinho-{numero}-loop.txt`.

b) Anuncie:

```
🔍 Próximo passo: animar a imagem em loop via API. Tempo estimado: 3 a 5 minutos.
```

c) Rode o script. Ele fecha o loop sozinho, mandando a mesma imagem como quadro inicial e quadro final:

```bash
py -3 scripts/animar-criativo.py --image "meus-produtos/{ativo}/entregas/criativos/criativo-quadrinho-{numero}-feed.png" --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-quadrinho-{numero}-loop.txt" --out "meus-produtos/{ativo}/entregas/criativos/criativo-quadrinho-{numero}-loop.mp4"
```

Para animar a versão Stories, troque `-feed.png` por `-stories.png` no `--image` e o sufixo do `--out` para `-stories-loop.mp4`.

d) Confirme:

```
✅ Concluído: vídeo em loop gerado e salvo.

Vídeo: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-quadrinho-{numero}-loop.mp4
```

Quadrinho tem bastante texto na arte, então avise o aluno antes de gerar: o modelo de vídeo pode tremer ou trocar letras dos balões. Se o vídeo vier com texto distorcido, gere de novo uma vez. Se persistir, avise que essa imagem não anima bem e sugira manter a versão estática.

---

## Tabela de cores por nicho

Use só quando o produto ainda não tem paleta própria.

- Música/instrumentos: ROXO PROFUNDO ou AZUL ELÉTRICO
- Yoga/bem-estar/meditação: VERDE-MUSGO ESCURO
- Direito/advocacia: AZUL-MARINHO PROFUNDO
- Skincare/lifestyle/geral: LARANJA VIVO
- Maternidade/beleza feminina: ROSA ESCURO ou TERRACOTA
- Finanças/investimentos/contabilidade: VERDE-ESCURO ou DOURADO QUEIMADO
- Educação/concursos/leitura: AZUL-MARINHO ou AMARELO MOSTARDA
- Pet/animais: VERDE-MUSGO
- Culinária/gastronomia: MARROM CARAMELO
- Tráfego pago/IA/digital: AZUL ELÉTRICO ou ROXO
- Fitness/saúde/emagrecimento: VERDE-LIMÃO ESCURO ou VERMELHO TIJOLO
- Empregabilidade/currículo: AZUL-MARINHO ou LARANJA VIVO

Na Paródia, a luz e as cores dos quadros seguem o clima da cena original. A cor de destaque (marca-texto, palavra da oferta e botão) vem da paleta do produto. Em campanha de Black, a faixa de oferta pode ser preta com destaque amarelo ou dourado.

## Regras

- **CTA:** o padrão é "Saiba mais", que é o botão nativo do Meta Ads. Se o aluno indicou outro em qualquer momento, ou se a imagem de referência dele já trazia a chamada, usar esse e só confirmar em uma linha. Nunca inventar CTA. Nunca usar "Link na bio" nem "Clique no link da bio", porque em anúncio pago o clique acontece no botão nativo, não na bio.
- **Perguntar o CTA antes de gerar:** se o aluno ainda não indicou a chamada, pergunte antes de montar a legenda e os prompts:

  ```
  Qual chamada você quer no criativo?

  1. Saiba mais (padrão do Meta Ads)
  2. Cadastre-se
  3. Comprar agora
  4. Outra (me diga qual)

  Digite o número:
  ```

- **Zona segura no Feed:** o rodapé 12% da arte não tem balão, texto nem botão, só ilustração ou fundo liso. É onde o Meta Ads sobrepõe o nome do anunciante e o botão nativo.
- **Zona segura no Stories/Reels:** o rodapé 14% fica vazio, o topo 12% e a lateral direita 15% ficam livres de texto crítico, cobertos pela barra de perfil e pela coluna de ícones. Na Jornada, a arte do Feed vai inteira para o Stories com faixas lisas em cima e embaixo, por isso o prompt do Feed já tira os balões dos quadros da direita dos últimos 15% da largura. Na Paródia, os quadros são rediagramados e os balões ficam até três quartos da largura.
- **Texto legível na arte:** até 16 palavras por balão e fonte grande. Se não couber, corte conteúdo, nunca diminua a fonte.
- **Escolha do estilo:** o Claude sempre recomenda com os critérios do Passo 2.2 e o aluno confirma. Nunca escolher em silêncio, a não ser quando o aluno já pediu o estilo ou mandou a imagem de referência.

### Sobre copy (Light Copy)

- Light Copy obrigatória na legenda e em todos os textos da arte. Sem travessão, sem exclamação, sem promessa vaga, sem "não é X. É Y.", sem "mesmo que" e sem "sem precisar".
- Produto NÃO aparece no quadro 1 (o lead da história) nem nas primeiras linhas da legenda. Na Jornada, ele entra nos quadros 2, 3 e na faixa do topo. Na Paródia, entra no quadro 3 e na faixa da base.
- O resultado prometido nunca passa do que o Quadro e os Decorados do perfil sustentam.
- **Exceção documentada: emoji no CTA da legenda.** A legenda termina com emoji (ex: "👇") no CTA. Vale só para o CTA da legenda.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar a legenda.

### Sobre os personagens

- Toda pessoa desenhada é uma pessoa comum de classe média brasileira, arrumada e cuidada, com roupa casual limpa e em bom estado. Nem modelo profissional, nem desleixada, mesmo no quadro do problema.
- Na Jornada, a mesma protagonista nos 4 quadros: mesmo rosto, mesmo cabelo, mesma roupa. O prompt repete isso.
- Na Paródia, os personagens são originais. **PROIBIDO** pedir o rosto, o nome ou a semelhança de ator, celebridade ou pessoa real, e **PROIBIDO** colocar o nome ou o logo da obra na arte. O reconhecimento vem da fala e da composição.

### Compliance Facebook Ads

- Sem pernas de fora, decote, roupa curta ou pose sensualizada.
- Sem violência, sangue, arma, ferida ou criatura assustadora.
- Roupas sempre cobertas.

### Operação

- Substituir TODOS os placeholders dos prompts. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.
- **NUNCA use travessão** em nenhum texto da skill. Use vírgula ou ponto final no lugar.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica, paródia.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).
