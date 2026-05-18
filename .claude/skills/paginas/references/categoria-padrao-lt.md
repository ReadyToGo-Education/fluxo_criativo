# Categoria Padrão. Página de Vendas Low Ticket

> Fonte de verdade do processo detalhado de geração de cada uma das 14 seções da Categoria Padrão.
> Consultar este arquivo quando a skill `/lt-pagina` precisar gerar uma seção específica da Estrutura E.

A Categoria Padrão é a recomendação automática quando o aluno está criando a primeira página low ticket no sistema (pasta `meus-produtos/{ativo}/entregas/paginas/` sem nenhuma página low ticket).

Cobre 14 seções na ordem fixa:

1. Cabeçalho (Headline + Pitadas de Desejo)
2. Comparação Primária (Visual, 2 lados)
3. Tabela Comparação (Resultado e Processo)
4. Diálogo Mental Negativo
5. A Culpa Não É Sua
6. Faça as Contas pro Cliente
7. Centro da Atenção
8. Dinâmica de Acesso
9. Demonstração
10. Quem É o Especialista
11. Depoimentos
12. Entregáveis Complementares
13. Resumo da Ópera (ancoragem final)
14. FAQ

Modo de geração default: **Híbrido**. Seções que vêm do perfil rodam automáticas. Seções que exigem dado real (Faça a Conta, Demonstração, Depoimentos, Quem É) entram em modo guiado com o aluno.

---

## REFERÊNCIA DE DESIGN VISUAL (north star)

A página de referência visual oficial da Categoria Padrão é:

**`https://bibliotecadecriativos.com.br/?utm_source=Instagram&utm_medium=Vendas&utm_id=Bio`** (Biblioteca de Criativos com ROI 2+, do Ricardo Maxxima)

**Antes de gerar o HTML da página, abrir essa URL** (via `mcp__Claude_in_Chrome__navigate` + `read_page` se o Chrome estiver conectado, ou via `WebFetch` como fallback) para conferir cores atuais, tipografia, espaçamentos e elementos visuais únicos. A página é o north star. Quando houver dúvida sobre como apresentar uma seção, replicar o estilo dela.

### Padrões de design observados nessa referência

**Estrutura geral.** Seções na vertical, mobile-first, alinhamento centrado, hierarquia clara H1 > H2 > H3 > body. Espaçamento generoso entre seções.

**Paleta.** Fundo branco/off-white predominante. Texto principal em preto ou cinza escuro. Accent de destaque em cor contrastante forte (azul ou laranja vibrante). Use cores acinzentadas em áreas de "estado ruim" e cor accent forte em "estado bom" (típico da Comparação Primária).

**Tipografia.** Sans-serif em heading e body. Heading em peso bold (600 a 700). Body em regular (400). Hierarquia bem marcada entre H1, H2 e parágrafo.

**Elementos visuais recorrentes.**

- Cards com ícone SVG iconografado por benefício/entregável.
- Listas com checkmarks visíveis (✓) em cada item.
- Números grandes como peça visual de destaque ("32 formatos", "ROI 2", "R$ 67"). Usar essa estética nas seções Faça as Contas, Centro da Atenção, Entregáveis e Resumo da Ópera.
- Badges/selos de validação ("Acesso imediato", "Atualização constante"). Replicar perto do CTA principal.
- Comparação visual binária (Opção 1 vs. Opção 2) com layout lado a lado. Reproduzir nas seções 2 (Comparação Primária) e 3 (Tabela Comparação).
- Imagens de depoimento real em formato vertical com print do canal de origem.

**CTA.** Texto no padrão "EU QUERO A [coisa]" em caixa alta, sempre derivado do Quadro. Aparece **pelo menos 2 vezes na página** (após hero e após oferta). Ancoragem de preço sempre com valor riscado acima do preço real. CTA flutuante mobile obrigatório.

**Tom de voz visual.** Casual + urgência + confiança. Design clean com elementos pontuais que remetem a oportunidade. Provocação direta na copy.

### Quando consultar a URL

Sempre que gerar uma página Padrão pela primeira vez para um produto novo. Em ajustes pontuais posteriores (via `/pagina-ajuste`), só consultar de novo se o aluno pedir mudança estrutural visual.

---

## SEÇÃO 1. CABEÇALHO (Headline + Pitadas de Desejo)

Você é um copywriter especialista em ofertas low ticket. Sua função é criar a headline principal e as pitadas de desejo do topo da página de vendas.

Siga este processo obrigatório em dois passos. Não pule etapas. Só avance pro Passo 2 (pitadas) depois que o aluno aprovar uma headline no Passo 1.

### Passo 0. Contexto

1. Qual é o produto? (planilha, template, calendário, estrutura de campanha, mini-curso, checklist)
2. Qual é a promessa central? (o grande resultado que a pessoa quer alcançar)
3. Qual é o formato de entrega? (o que a pessoa vai baixar/acessar/receber de imediato)

### Passo 1. Headline principal

Antes de escrever, faça essa análise interna (não mostre pro aluno):

**1. Encontre o desejo profundo do nicho.** Quem é o comprador? O que tira o sono dele? Não o que o produto faz, mas o resultado final que ele persegue e não consegue alcançar.

**2. Encontre o comportamento ultrapassado.** O que o comprador provavelmente faz hoje que é velho, ineficiente ou errado? O que alguém com resultado melhor já parou de fazer? O objetivo é fazer ele pensar "será que eu sou esse cara?".

**3. Encontre os comportamentos de identificação (para produtos subjetivos).** Se o produto resolve um problema emocional (relacionamento, ansiedade, autoestima, propósito, luto, vícios, produtividade pessoal), os números não funcionam como prova. O que funciona é descrever comportamentos específicos do dia a dia que a pessoa vive e não conta pra ninguém. Não é o problema genérico ("sofre com o término"). É o que ela faz por causa do problema: stalkeiar o ex, pegar o celular de manhã pra ver se ele postou, não conseguir passar 30 minutos sem pensar nele, fingir que tá bem no trabalho mas chorar no banho, não ter vontade de conhecer ninguém, tudo lembrar a pessoa. Liste pelo menos 5 desses comportamentos antes de escrever as headlines. Use como abertura ou centro da headline no lugar dos números. Esse é o equivalente emocional da especificidade numérica.

**Camadas que cada headline pode usar (uma ou mais):**

- **Provocação por contraste.** Mostrar que o que ele faz hoje é ultrapassado, fazendo ele se sentir defasado.
- **Relato pessoal com resultado específico.** Não prometa, conte o que você fez e o resultado que teve. Use números que pareçam reais e vividos. Quando é relato, o cara não avalia se acredita, avalia se quer o mesmo resultado.
- **Oferta embutida no relato.** Deixe claro que está entregando pronto o exato mecanismo que gerou aquele resultado. O cara não precisa aprender, precisa copiar.
- **Prova social ampliada.** Referencie quem tá no topo do nicho. Os que mais faturam, os que têm fila, os mais conhecidos. O comprador quer copiar quem tá ganhando, não um professor.
- **Identificação íntima (para produtos subjetivos).** Use comportamentos específicos do dia a dia como elemento de identificação. A headline segue a mesma estrutura direta de qualquer low ticket. Ex: "Aplique essa técnica e pare de pensar nele o dia inteiro. Você vai voltar a viver sua vida ainda hoje." Verbo de ação concreto continua abrindo (aplique, use, copie, pegue, implemente). A identificação e a promessa vêm logo depois. Não conte história. Não faça parágrafo. Seja tão direto quanto "Copie esse cardápio e saia de 15 mil pra 50 mil por mês".

**Fórmula obrigatória.** Toda headline segue exatamente essa ordem:

1. Verbo de ação concreto (copie, use, teste, aplique, implemente, pegue) + o que vai receber/usar
2. Identificação com o problema ou situação do comprador
3. Solução desejada / resultado que a pessoa quer

Varie os verbos e as combinações, mas nunca fuja dessa ordem. Exemplos: "Aplique essa técnica e pare de [problema]. Você vai [resultado] ainda hoje." / "Copie essa estrutura e saia de [situação ruim] pra [situação boa]."

**Regras de escrita:**

- **Objetivo central em todas.** Identifique qual é o objetivo central do produto e garanta que todas as 10 headlines falem dele. Se o produto é pra esquecer o ex, todas falam de esquecer o ex ou superar o término. Se é pra ter ROAS alto, todas falam de ROAS. O objetivo central nunca pode sumir de nenhuma headline.
- **Nicho e produto explícitos.** O leitor tem que bater o olho na headline e entender imediatamente do que se trata. Nunca deixe implícito. Se é tarô, a palavra "tarô" tem que aparecer. Se é superar o ex, "ex" ou "término" tem que aparecer. Teste cada headline perguntando: se alguém lê só essa frase, sem contexto nenhum, sabe exatamente do que é o produto? Se não sabe, reescreva.
- Escreva como uma pessoa comum falaria. Simples, direto, sem jargão.
- Quando for headline de facilidade direta, comece com o verbo de ação: copie, cole, use, pegue, monte, baixe.
- Quando for headline de inadequação/provocação, abra com a provocação e o verbo de ação vem depois.
- **Benefício específico.** Para produtos tangíveis (negócios, tráfego, finanças), use números com contexto: "ROAS de 3.5", "faturar 100 mil por mês", "ticket médio de 45 reais". Para produtos subjetivos, use comportamentos específicos do dia a dia: "parar de pegar o celular pra ver se ele postou", "conseguir passar um dia inteiro sem pensar nele", "parar de chorar no banho". Nunca seja abstrato em nenhum dos dois casos.
- **Resultado imediato.** Nunca use prazos como "em 7 dias", "em uma semana", "em um mês". Low ticket é consumo rápido e resultado rápido. Use "hoje", "agora", "ainda hoje", "na hora", "na primeira vez". O comprador tem que sentir que aplica e já funciona.
- **Respeite o escopo.** Nunca prometa algo que o produto não entrega. Se o produto é sobre tráfego, fale só de tráfego. Nunca mencione benefícios ou áreas que não estejam explicitamente no produto.
- Números que pareçam reais e vividos, não redondos e fabricados.
- Nunca use travessões.
- Frases curtas. Se ficou longo, corte.
- Cada headline deve ter uma arquitetura diferente. Varie entre provocação, relato, prova social, facilidade direta.

**Entrega obrigatória.** Gere SEMPRE 10 opções de headline. Depois das 10, pergunte: "Gostou de alguma? Se sim, me diz qual que eu refino e a gente avança pro Passo 2 com as pitadas de desejo. Se não, gero mais 10 com ângulos completamente diferentes."

### Passo 2. Pitadas de desejo (só depois da headline aprovada)

Gere 15 pitadas de desejo numeradas de 1 a 15. São frases curtíssimas que ficam logo abaixo da headline. **Máximo de 6 palavras cada.**

Cada pitada precisa ser de uma dessas 3 categorias:

- **Desejo.** Característica ou resultado do produto que gera vontade imediata. Ex: "Estrutura que fatura mais de 30 milhões", "Cardápio das cafeterias com fila", "ROAS validado acima de 3.5".
- **Facilidade.** Algo que mostra que é fácil e rápido. Ex: "Só copiar e colar", "Implementa em 20 minutos", "Não precisa saber programar".
- **Quebra de objeção.** Algo que responde uma dúvida antes dela aparecer. Ex: "Não precisa aumentar custo", "Funciona com equipe pequena", "Seu time já sabe fazer".

Regras: misture as 3 categorias. Frases curtíssimas. Linguagem simples. Numere todas de 1 a 15.

Depois das 15, pergunte: "Escolhe 3 ou 4 que mais te agradaram que eu monto a versão final com a headline + as pitadas."

Quando o aluno escolher, monte a versão final com a headline aprovada + as pitadas escolhidas, pronta pra ir pra página.

### Layout HTML

Fundo escuro com gradiente, logo no topo (header sticky), headline em destaque grande, pitadas como tags ou linhas curtas abaixo. CTA com Quadro adaptado. Nota "Acesso imediato após o pagamento".

---

## SEÇÃO 2. COMPARAÇÃO PRIMÁRIA (Visual)

Você é um copywriter e diretor de arte. Crie uma peça visual única de alto impacto que mostra dois mundos lado a lado: o mundo sem o produto e o mundo com o produto.

### Passo 1. Contexto

1. Qual é o produto?
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Títulos dos dois lados

Crie 3 opções de par de títulos. Regras:

- NUNCA "Antes" e "Depois".
- Lado esquerdo (ruim) nomeia o estado atual como categoria, rótulo, tipo. Sem ofender.
- Lado direito (bom) nomeia o estado aspiracional.
- Funcionam como opostos naturais (dois tipos de pessoa, dois tipos de negócio).
- Máximo 4 palavras cada.
- Esquerdo com ✗ (vermelho), direito com ✓ (verde).

Exemplos de referência (NÃO copiar):

- "✗ Cafeterias normais" vs. "✓ Cafeterias de alto valor"
- "✗ Currículo invisível" vs. "✓ Currículo que convoca"
- "✗ Gestão no achismo" vs. "✓ Gestão com método"
- "✗ Vida no automático" vs. "✓ Vida com intenção"
- "✗ Tráfego no escuro" vs. "✓ Tráfego com inteligência"

Apresente as 3 opções e peça pro aluno escolher.

### Passo 3. Cena de cada lado

Descreva em 2-3 frases o que aparece em cada lado da imagem. Pense como se estivesse explicando pra um designer o que você quer ver.

- **Lado esquerdo (ruim).** Realista e identificável, nunca exagerado ou humilhante. A pessoa olha e pensa "é assim mesmo que tá".
- **Lado direito (bom).** Aspiracional e desejável, mas alcançável. A pessoa olha e pensa "é isso que eu quero".

### Passo 4. Os números

Defina 2 métricas por lado que vão aparecer embaixo da imagem, como etiquetas de preço de um cardápio.

Regras:

- Pelo menos 1 métrica financeira desdobrada até o bolso.
- Se o produto for subjetivo/emocional e não tiver números financeiros, use métricas de comportamento concretas.
- Números são hipotéticos. Avise o aluno para trocar pelos reais.

### Regras gerais

- O lado esquerdo nunca pode ser ofensivo ou humilhante. Ele é identificável, não ridículo.
- O lado direito nunca pode ser irreal ou fantasioso demais. Ele é aspiracional, mas alcançável.
- O contraste entre vermelho (✗) e verde (✓) tem que ser óbvio num relance.

### Layout HTML

Fundo claro, grid 2 colunas (1 mobile). Ícones grandes ✗ e ✓ no topo de cada lado. Contraste vermelho/verde óbvio num relance.

---

## SEÇÃO 3. TABELA COMPARAÇÃO

Você é um copywriter. Crie as 2 categorias de comparação da página.

### Passo 1. Contexto

1. Qual é o produto?
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Classificar o tipo de produto

**Tipo A. Tangível/Objetivo.** Resultado mensurável com números (culinária, tráfego pago, organização financeira). Itens diretos e factuais. Ticket médio, faturamento, tempo, ROI. Transformação se prova com dados.

**Tipo B. Subjetivo/Emocional.** Resultado interno (superação, espiritualidade, autoestima, ansiedade). Itens precisam de mistura:

- **3 itens técnicos.** Mostram método, mecanismo, técnica. O "depois" mostra NOME da técnica, MECANISMO, PROTOCOLO. Demonstra competência e autoridade do criador. A pessoa lê e pensa "essa pessoa sabe o que tá fazendo, não é coach de Instagram".
- **3 itens emocionais/identificação.** Mostram transformação que a pessoa sente por dentro. Sentimento de vazio que vira alívio. Vida paralisada que volta a fluir. Aqui pode ser mais simples e direto, mas nunca bobinho.

Informe ao aluno o tipo do produto.

### Passo 3. Gerar as 2 categorias

**Categoria 1. Resultado (Antes vs. Depois).**

Compare o RESULTADO antes vs. depois. 6 itens.

Regras:

- Cada item é par claro: estado negativo (antes) e positivo (depois).
- Não fique só no óbvio. Expandir para consequências secundárias, emocionais, percepção de terceiros.
- Frases curtas, máximo 15 palavras.
- Tipo A com itens financeiros: SEMPRE desdobrar até o bolso. Não basta dizer "faturamento aumentou". Tem que mostrar: faturamento de X, margem de Y%, sobra Z no fim do mês.
- Tipo B: 3 técnicos + 3 emocionais, nessa ordem.

**Categoria 2. Processo (Como fazia antes vs. Como faz agora).**

Compare o JEITO DE FAZER. 6 itens.

Regras:

- Foco no processo, na rotina, no modo de operar.
- Mostre a transformação no dia a dia: o que a pessoa fazia de um jeito tosco, improvisado, demorado ou desinformado, e como agora ela faz de um jeito mais inteligente, estruturado ou consciente.
- Tipo A: pelo menos 1 item com impacto financeiro desdobrado até o bolso e 1 item com impacto em percepção externa (o que os outros pensam, indicações, reputação).
- Tipo B: 3 técnicos + 3 emocionais. Os técnicos mostram o método novo de agir. Os emocionais mostram como a pessoa se sente operando dessa forma nova.
- Frases curtas, máximo 15 palavras.

### Passo 4. Apresentar e refinar

Apresente as 2 categorias e pergunte qual usar (1, 2 ou ambas). Depois da escolha:

1. Reescreva com mais precisão e tom do produto.
2. Sugira 2 títulos de seção.
3. Sugira layout (tabela 2 colunas, cards antes/depois, checklist ✗/✓).

### Regras gerais

- Itens concretos e específicos. "Mais vendas" é genérico. "Ticket médio de R$ 15 pra R$ 38" é concreto. "Ficou feliz" é genérico. "Acorda e o primeiro pensamento não é mais sobre ele" é específico.
- Tipo B técnico nunca pode ser promessa vazia. "Agora se sente melhor" é proibido. "Aplica a regra dos 3 segundos e redireciona o impulso" é o padrão.
- Tipo B emocional nunca bobinho. "Era triste, ficou feliz" é proibido. "Olha pra própria vida e reconhece que o extraordinário já começou" é o padrão.
- Números são sempre exemplos hipotéticos. Avisar pro aluno trocar pelos reais.

### Layout HTML

Tabela 2 colunas no desktop, stack vertical no mobile. Linhas alternadas com fundo neutro. Cabeçalhos em cor accent.

---

## SEÇÃO 4. DIÁLOGO MENTAL NEGATIVO

Você é um copywriter. Crie a seção que mostra ao visitante que você sabe exatamente o que ele pensa, sente e sofre no dia a dia em relação ao problema que o produto resolve. São aqueles pensamentos que passam na cabeça dele no banho, de madrugada, no caminho do trabalho. Coisas que ele pensa mas não fala pra ninguém. Quando ele lê isso, pensa: "esse cara tá dentro da minha cabeça".

### Passo 1. Contexto

1. Qual é o produto?
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Mapa de empatia negativo

Sem mostrar pro aluno, mapeie:

- O que ele PENSA de madrugada quando não consegue dormir?
- O que ele SENTE comparando a vida dele com a dos outros?
- O que ele TEM MEDO que aconteça se nada mudar?
- O que ele FALA PRA SI MESMO nos piores dias?
- Qual é a VERGONHA que ele não conta pra ninguém?
- Qual é a FRUSTRAÇÃO que se repete toda semana/todo mês?

### Passo 3. Título principal

Crie 3 opções de título. Regras:

- Nomeia a dor principal de forma direta, sem rodeio.
- Pode ser pergunta retórica ou afirmação que descreve a situação do avatar.
- Tom conversacional, como amigo que entende a situação. Nunca formal, nunca técnico.
- Parte mais dolorosa em negrito.
- Máximo 2 linhas.

Exemplos de referência (NÃO copiar):

- "Eu sei. Seu produto Low Ticket não vende e seu ROI só diminui, não é mesmo?"
- "Você não aguenta mais torrar dinheiro no tráfego pago com campanhas que não funcionam."
- "Todo fim de mês é a mesma coisa: as contas apertam e você pensa se vale a pena continuar."

Apresente as 3 opções e peça pro aluno escolher.

### Passo 4. 12 pensamentos do avatar

Crie 12 pensamentos que representam o diálogo mental negativo do avatar. Divida em dois grupos:

**6 pensamentos emocionais.** Tocam em: comparação com os outros, medo do futuro, identidade ferida, vergonha, solidão, sensação de fracasso.

**6 pensamentos racionais/técnicos.** Tocam em: conta que não fecha, métrica ruim, processo que não funciona, falta de método, problema operacional, dinheiro que não sobra.

Regras para todos os 12:

- Escritos em primeira pessoa, como se fosse a pessoa falando consigo mesma.
- Entre aspas, como balões de pensamento.
- Tom visceral, emocional, real. Linguagem de desabafo, não de livro.
- FRASES CURTAS. Máximo 1 linha. Se a frase tem mais de 15 palavras, encurte.
- Cada pensamento deve ter uma parte em negrito, que é a parte mais dolorosa.
- Pode ter palavrão leve se fizer sentido pro público. Se for público mais formal, não use.
- Específicos ao nicho, nunca genéricos.

Apresente os 12 e peça pro aluno escolher os 4 que mais combinam com o público dele.

### Passo 5. Resumo final

```
Título: [escolhido com negrito]
Subtítulo: "e você sofre todo dia com pensamentos como..."

1. "[pensamento escolhido]"
2. "[pensamento escolhido]"
3. "[pensamento escolhido]"
4. "[pensamento escolhido]"
```

Pergunte: "Quer ajustar algum pensamento ou trocar a ordem?"

### Regras gerais

- Tom visceral e real, nunca genérico, nunca autoajuda.
- Frases curtas. Máximo 15 palavras por pensamento. Se não cabe em 1 linha, tá grande demais.
- Pensamentos específicos ao nicho. "Nada funciona" é genérico. "Já mudei cardápio, fiz promoção, postei no Instagram, nada muda" é específico.
- Cada pensamento deve fazer a pessoa sentir que você invadiu a mente dela.
- Nunca humilhe o avatar. Você mostra que entende a dor, não ri dela.

### Layout HTML

Fundo escuro, cards estilo balão de pensamento, parte mais dolorosa em negrito accent. Título grande no topo.

---

## SEÇÃO 5. A CULPA NÃO É SUA

Você é um copywriter especialista em produtos digitais low ticket. Crie a seção que mostra pro visitante que ele faz tudo certo, se esforça de verdade, mas o resultado não vem porque o MÉTODO que ele aprendeu é que tá errado. E isso não é culpa dele.

A estrutura tem 3 blocos, mas os nomes dos blocos devem ser personalizados ao nicho. Nunca use "Identificação", "Absolvição" ou "Revelação" como títulos visíveis.

### Passo 1. Contexto

1. Qual é o produto?
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Mapear o esforço e as dores

Analise o produto e o público. Mapeie internamente (sem mostrar pro aluno):

- Quais são os esforços genuínos que essa pessoa faz todo dia?
- Quais são os PROBLEMAS REAIS que ela enfrenta mesmo se esforçando? (conta não fecha, cliente some, toma caldo, funcionário pede demissão, conta bloqueada, peso não desce)
- O que ela vê os outros conseguindo e não entende por quê?
- Qual é o ERRO INVISÍVEL que ela comete sem saber?
- Qual é o jeito CONTRAINTUITIVO que realmente funciona?

### Passo 3. Bloco 1. A pessoa se esforça de verdade

Crie uma lista de EXATAMENTE 3 situações onde a pessoa se esforça, enfrenta problemas reais e mesmo assim o resultado não vem.

Regras:

- EXATAMENTE 3 pontos. Não mais, não menos.
- Cada ponto deve misturar o esforço genuíno COM o problema real que acontece. Não é só "ela trabalha duro". É "ela trabalha duro E mesmo assim acontece isso".
- Ultra específico ao nicho. Detalhes que só quem vive aquela realidade reconhece.
- A pessoa lê e pensa "é exatamente isso que acontece comigo".
- Frases de 1-2 linhas cada.
- O tom é de reconhecimento, nunca de acusação.

O subtítulo desse bloco deve ser personalizado ao nicho. Exemplos:

- Brunch: "Você se dedica de verdade:"
- Surf: "Você se joga de verdade:"
- Tráfego: "Você se dedica de verdade:"
- Vendas: "Você dá o seu melhor todo dia:"

### Passo 4. Bloco 2. Mas ninguém te explicou isso

Um parágrafo curto de 2-3 linhas dizendo que a culpa não é dela.

Regras:

- Máximo 3 linhas. Curto e direto.
- Tom de alívio. A pessoa lê e sente um peso saindo.
- Diga claramente: a culpa não é dela, foi assim que ensinaram, é o jeito mais comum, ela não tinha como saber.
- Não culpe ninguém. Só diga que o método convencional é limitado.
- Aponte brevemente onde está o erro real (o processo, não a pessoa).

O subtítulo desse bloco deve ser personalizado. Exemplos:

- "Mas ninguém te contou isso:"
- "Mas ninguém te explicou isso:"
- "Só que tem uma coisa que ninguém te disse:"

### Passo 5. Bloco 3. O que funciona de verdade

2 a 3 mudanças contraintuitivas que o método do produto ensina.

Regras:

- 2 a 3 mudanças. Cada uma em um parágrafo CURTO de 2-3 linhas.
- Cada mudança mostra: o que a maioria faz (jeito comum) vs. o que realmente funciona (jeito novo) e por quê em 1 linha.
- O jeito novo deve parecer contraintuitivo. A pessoa lê e pensa "sério? É ao contrário?"
- O tom é de quem tá revelando algo que poucas pessoas sabem.
- Parágrafos curtos e diretos. Se passou de 3 linhas, corte.

O subtítulo desse bloco deve ser personalizado ao nicho. Nunca use "Revelação" ou "O que todo mundo faz vs. o que funciona". Exemplos:

- Brunch: "O que as cafeterias que lotam fazem diferente:"
- Surf: "O que quem dropa toda onda faz diferente:"
- Tráfego: "O que quem escala com ROAS alto faz diferente:"
- Vendas: "O que quem bate meta todo mês faz diferente:"

### Passo 6. Título e subtítulo da seção

Crie título e subtítulo da seção.

Regras:

- DEVEM ser personalizados ao nicho e ao produto. Nunca genéricos.
- O título mostra o esforço + o resultado frustrante. A pessoa lê e se identifica na hora.
- O subtítulo revela que existe um detalhe que ela não sabe. Gera curiosidade.
- Tom empático. Você tá do lado dela.
- Máximo 1 linha cada.
- NUNCA use títulos genéricos que funcionariam pra qualquer nicho. Se o título funciona pra brunch e pra surf ao mesmo tempo, tá genérico demais.

Exemplos de referência (NÃO copiar):

- Brunch: "Você abre a cafeteria todo dia às 6h, faz tudo com carinho e mesmo assim o caixa não fecha." / "O problema não é o seu esforço. É um detalhe no cardápio que ninguém te ensinou."
- Surf: "Você rema com toda força, levanta no timing certo e mesmo assim cai toda vez." / "O problema não é a sua força nem a sua coragem. É um erro na remada que ninguém corrigiu."
- Tráfego: "Você estuda tráfego todo dia, testa tudo que ensinam e o ROAS não passa de 1,5." / "O problema não é o seu orçamento nem o seu criativo. É uma etapa da otimização que você faz na mão e não deveria."

### Passo 7. Resumo final

```
[Título]
[Subtítulo]

[Subtítulo do bloco 1 personalizado ao nicho]
- [situação 1 com esforço + problema real]
- [situação 2 com esforço + problema real]
- [situação 3 com esforço + problema real]

[Subtítulo do bloco 2 personalizado]
[Parágrafo curto de 2-3 linhas]

[Subtítulo do bloco 3 personalizado ao nicho]
[Mudança contraintuitiva 1 em 2-3 linhas]

[Mudança contraintuitiva 2 em 2-3 linhas]

[Mudança contraintuitiva 3 em 2-3 linhas] (se tiver)
```

Apresente e pergunte: "Essas situações fazem sentido com o seu público? Quer ajustar alguma ou adicionar algo que você ouve muito dos seus clientes?"

### Regras gerais

- Tom empático, de aliança. Você tá do lado da pessoa, nunca contra.
- EXATAMENTE 3 pontos no bloco de identificação. Não mais.
- Cada ponto de identificação deve misturar esforço COM problema real. Não só esforço.
- A absolvição é curta: 2-3 linhas. Sem drama, sem vitimismo.
- A revelação tem 2-3 mudanças contraintuitivas em parágrafos CURTOS de 2-3 linhas cada.
- TODOS os títulos, subtítulos e nomes de blocos devem ser personalizados ao nicho. Nada genérico.
- Nunca use "Identificação", "Absolvição", "Revelação" como títulos visíveis.
- Nunca culpe a pessoa. O esforço dela é real. O método que ela aprendeu é que é limitado.
- Nunca culpe professores, escolas ou concorrentes específicos.
- A revelação deve gerar a reação: "sério? É ao contrário do que eu pensava?"
- O título e subtítulo devem ser tão específicos ao nicho que não funcionariam pra nenhum outro produto.

### Layout HTML

Fundo claro com tom acolhedor. 3 blocos em cards ou seções separadas com hierarquia visual clara. Subtítulo de cada bloco em destaque accent. Bloco 2 (absolvição) com fundo levemente diferente pra criar pausa visual. Bloco 3 (revelação) com bullets ou ícones de "x → ✓" mostrando o contraste do jeito comum vs. jeito novo.

---

## SEÇÃO 6. FAÇA AS CONTAS PRO CLIENTE

Você é um copywriter e analista de negócios. Crie a seção que faz a conta na frente do cliente com números reais. Mostra os números do cenário ruim e do cenário bom lado a lado, de um jeito que qualquer pessoa entenda. Quando a pessoa lê essa seção, ela pensa: "puta merda, eu tô perdendo essa grana toda?"

**Atenção.** Essa seção só funciona pra produtos com resultados mensuráveis (dinheiro, peso, tempo, volume, clientes, margem, calorias, economia). Se o produto for puramente emocional, avise que essa seção não se aplica e sugira substituir por reforço da Tabela Comparação ou expandir o Diálogo Mental Negativo.

### Passo 1. Contexto

1. Qual é o produto?
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Identificar variáveis do negócio

Categorias (use as que fizerem sentido):

**Negócio/Renda.** Ticket médio, quantidade de clientes/pedidos por dia, faturamento, custo de operação, margem, lucro líquido, horas de trabalho.

**Saúde/Corpo.** Calorias consumidas, calorias gastas, déficit semanal, peso perdido por semana e mês, litros de água, horas de sono, medidas.

**Organização/Economia.** Gasto mensal total, gasto por categoria, economia por item, economia acumulada em 3/6/12 meses, tempo gasto em tarefas, tempo economizado.

**Produtividade/Marketing.** Horas por tarefa, custo por lead, taxa de conversão, ROI/ROAS, número de leads/vendas/clientes.

Escolha 4-6 variáveis que criam o contraste mais forte.

### Passo 3. Montar os 2 cenários

**Cenário A. Sem o produto.** Números realistas do cenário ruim. A pessoa olha e pensa "é mais ou menos isso mesmo".

**Cenário B. Com o produto.** Números realistas do cenário bom. A pessoa olha e pensa "isso é possível".

Regras:

- Números plausíveis, não fantasiosos. Se o ticket hoje é R$ 12, não coloque R$ 200 no cenário bom. Coloque R$ 42 ou R$ 55.
- Cada número com lógica entre si. Se o ticket médio subiu e o volume de clientes subiu, o faturamento tem que bater.
- SEMPRE desdobrar até o resultado final no bolso, no corpo, na conta bancária. Não pare no faturamento. Vá até o lucro líquido, o peso real perdido, a economia real acumulada.
- Cálculo simples, como guardanapo.

### Passo 4. Título da seção

Conecta uma ação concreta do universo do produto com o convite "faz a conta comigo". O formato é: "[ação concreta ligada ao dia a dia do avatar] e faz a conta comigo."

A ação concreta deve puxar um objeto, ferramenta ou hábito que a pessoa já conhece e que já dói por si só.

Crie 3 opções de título.

Exemplos de referência (NÃO copiar):

- Brunch: "Pega o cardápio e faz a conta comigo."
- Tráfego pago: "Abre o gerenciador de anúncios e faz a conta comigo."
- Design com IA: "Olha a fatura do seu designer e faz a conta comigo."
- Jejum: "Sobe na balança e faz a conta comigo."
- Sustentabilidade: "Pega sua conta de luz e faz a conta comigo."
- Adestramento: "Soma tudo que seu cachorro já destruiu e faz a conta comigo."
- Procrastinação: "Olha seu histórico de tela e faz a conta comigo."

### Passo 5. Estrutura da conta

```
CENÁRIO A. [nome do cenário ruim]
[Variável 1]: [valor]
[Variável 2]: [valor]
[Variável 3]: [valor]
[Cálculo]: [variável] x [variável] = [resultado parcial]
[Resultado parcial] - [custo] = [RESULTADO FINAL]

CENÁRIO B. [nome do cenário bom]
[Variável 1]: [valor]
[Variável 2]: [valor]
[Variável 3]: [valor]
[Cálculo]: [variável] x [variável] = [resultado parcial]
[Resultado parcial] - [custo] = [RESULTADO FINAL]
```

Máximo 5-6 linhas por cenário. Não é uma planilha, é uma conta de guardanapo.

Os cálculos devem ser simples: multiplicação, subtração, porcentagem. Nada complexo.

Use sempre a mesma estrutura nos dois cenários pra facilitar a comparação visual.

### Passo 6. Linha de impacto

Uma frase final que mostra a diferença entre os dois cenários de forma chocante.

Exemplo: "A diferença? R$ 21.500 por mês. R$ 258 mil por ano. Com o mesmo número de horas trabalhadas."

A linha de impacto é obrigatória. É ela que faz a pessoa sentir o peso do número.

### Passo 7. Apresentar e ajustar

"Esses números fazem sentido com a realidade do seu público? Quer ajustar algum valor? Lembre que são exemplos hipotéticos. Troque pelos dados reais dos seus clientes pra ficar ainda mais forte."

### Regras gerais

- Os números devem ser plausíveis. Exagerar pros dois lados mata a credibilidade.
- SEMPRE desdobrar até o resultado final no bolso, no corpo ou na conta bancária. Nunca pare no meio do cálculo.
- A conta tem que ser simples o suficiente pra uma pessoa que não gosta de matemática entender em 10 segundos.
- A linha de impacto final deve traduzir a diferença em termos que doam: valor por ano, valor por hora trabalhada, peso perdido em 3 meses, economia em 1 ano.
- Sempre avise que os números são hipotéticos e que o aluno deve trocar pelos reais.
- Se o produto não tem resultado mensurável, avise que essa seção não se aplica. Não force números onde eles não existem.

### Layout HTML

Fundo claro com gradiente, 2 colunas (cenário A e B), tipografia grande nos números, linha de impacto no fim com destaque accent.

---

## SEÇÃO 7. CENTRO DA ATENÇÃO

Você é um copywriter e estrategista visual. Crie uma peça onde UM elemento central do produto é o protagonista, com benefícios apontando pra ele com setas. A pessoa olha e entende: "tudo gira em torno disso".

### Passo 1. Contexto

1. Qual é o produto?
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Definir o centro da atenção

**Regra crítica.** O centro DEVE ser algo físico e visual. Algo que dá pra desenhar, fotografar ou ilustrar. Porque essa seção vai virar uma imagem na página. Nunca pode ser um conceito abstrato, um método ou uma ideia.

Pode ser:

- Ferramenta real (Claude na tela, planilha aberta, app)
- Parte do corpo (pênis, pélvis, intestino, coluna)
- Prato ou produto físico (toast, bolo, peça de crochê)
- Documento físico (currículo, cardápio, manual)
- Objeto do dia a dia (computador, balança, celular)

NÃO pode ser:

- Um método ("o método X")
- Um conceito ("a transformação", "o controle", "a técnica")
- Um sentimento ("a confiança", "o equilíbrio")

Se você pensar num centro e não conseguir imaginar uma foto ou ilustração dele, ele não serve.

Crie 3 opções de centro com nome curto (1-3 palavras) + frase de 1 linha justificando.

Exemplos de referência (NÃO copiar):

- Brunch → "O Toast" / "O prato que transforma cafeteria de R$ 12 em cafeteria de R$ 45"
- Tráfego com IA → "O Claude" / "A tela do Claude aberta, a ferramenta que faz o trabalho de uma equipe"
- Fisioterapia pélvica → "O assoalho pélvico" / "A região que comanda tudo e ninguém te ensinou a cuidar"
- Ejaculação precoce → "O pênis" / "A região que você usa todo dia e nunca treinou"
- Casamento → "A planilha" / "Um arquivo que organiza o casamento inteiro"
- Jejum → "O prato" / "O prato que você monta dentro da janela de 8 horas"

Peça pro aluno escolher uma opção.

### Passo 3. 30 elementos ao redor

Crie 30 elementos que ficam ao redor apontando pro centro com setas. O aluno vai escolher os 8 que mais fazem sentido pro público dele.

Regras:

- Cada elemento deve ser curto: máximo 4 palavras.
- Mistura de:
  - Benefícios diretos (o que melhora)
  - Funções/mecanismos (o que o centro faz ou ativa)
  - Resultados práticos (o que a pessoa ganha)
  - Vantagens operacionais (o que fica mais fácil, rápido ou barato)
  - Problemas eliminados (o que para de acontecer)
  - Métricas concretas quando possível (números, tempos, valores)
- Não repita a mesma ideia com palavras diferentes.
- Cada elemento deve ser bem prático e específico ao nicho. Nada genérico.
- Pense: se a pessoa lê aquele elemento, ela tem que pensar "isso sozinho já vale a pena".

Apresente os 30 e peça pro aluno escolher 8.

### Passo 4. Título da seção

Crie 3 opções de título pra essa seção na página.

Regras:

- O título deve comunicar que existe UM elemento central que resolve vários problemas ao mesmo tempo.
- Tom direto, curto, impactante.
- Máximo 1 linha.
- O título deve ter relação direta com o centro escolhido, não pode ser genérico.

Exemplos de referência (NÃO copiar):

- Brunch: "Tudo muda quando você coloca um toast no cardápio"
- Tráfego: "Tudo que muda quando você coloca o Claude pra trabalhar no seu tráfego"
- Ejaculação precoce: "Tudo que você nunca aprendeu sobre o que tá entre as suas pernas"
- Casamento: "Um arquivo. O casamento inteiro organizado."

Apresente as 3 opções e peça pro aluno escolher.

### Passo 5. Resumo final

```
Título: [escolhido]
Centro: [nome do centro]

1. [elemento] →
2. [elemento] →
3. [elemento] →
4. [elemento] →
5. [elemento] →
6. [elemento] →
7. [elemento] →
8. [elemento] →

(todas as setas apontam pro centro)
```

Apresente e pergunte: "Quer trocar algum elemento ou ajustar a ordem?"

### Regras gerais

- O centro da atenção DEVE ser algo físico e visual, que dá pra ilustrar ou fotografar. Nunca um conceito abstrato.
- Os elementos ao redor devem ser curtos (máximo 4 palavras). Eles vão virar labels numa imagem.
- Sempre gerar 30 elementos pro aluno escolher 8. Quantidade gera qualidade de escolha.
- Se o produto tiver mais de um possível centro, sempre dê opções pro aluno escolher. Nunca decida sozinho.
- Os elementos devem ser práticos, específicos ao nicho e nunca genéricos.

### Layout HTML

Centro grande visualmente, 8 labels distribuídos ao redor com setas indicando o centro. Fundo claro com gradiente sutil.

---

## SEÇÃO 8. DINÂMICA DE ACESSO

Você é um copywriter. Crie a seção que mostra ao visitante que o caminho entre comprar o produto e ter resultado é curto, simples e óbvio. A pessoa lê e pensa: "é só isso? Consigo fazer hoje".

A lógica dos passos é sempre:

1. Começa com **ACESSO** (como ele recebe / entra no material)
2. Passa por **EXECUÇÃO** (o que ele faz com o que aprendeu)
3. Termina com **RESULTADO** (o que muda na vida dele)

### Passo 1. Contexto

1. Qual é o produto? (nome, o que ele ensina/entrega, formato)
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Título da seção

Crie 3 opções de título. Regras:

- Passa a sensação de que é simples, rápido e qualquer pessoa consegue.
- Tem relação direta com o produto, nunca genérico.
- Tom confiante e leve.
- Máximo 1 linha.

Exemplos de referência (NÃO copiar):

- "Do acesso ao primeiro brunch vendido em menos de 24 horas"
- "3 passos pra sua cafeteria nunca mais depender de café com pão de queijo"
- "É mais simples do que parece. Olha o caminho:"
- "Do download ao resultado no mesmo dia"
- "Compra agora, aplica hoje, resultado amanhã"

Apresente as 3 opções e peça pro aluno escolher.

### Passo 3. Versões A e B dos passos

Gere SEMPRE 2 versões:

- **Versão A.** 3 passos.
- **Versão B.** 5 passos.

Cada passo tem:

- Número (Passo 1, Passo 2...)
- Título ULTRA CURTO: máximo 3-4 palavras. É quase uma etiqueta.
- Uma frase de apoio de NO MÁXIMO 1 linha curta embaixo.

Regras:

- O primeiro passo é SEMPRE sobre acessar o material.
- O último passo é SEMPRE o resultado.
- Os passos devem parecer MÁGICOS e FÁCEIS. A pessoa tem que sentir que não dá trabalho nenhum.
- Nunca use "na mesma semana". Sempre "hoje", "no mesmo dia", "agora", "em minutos". Low ticket é resultado imediato.
- Os passos de execução devem ser específicos ao produto, nunca genéricos.
- Cada título de passo deve caber dentro de um ícone ou badge numa página de vendas.

Exemplos de referência (NÃO copiar):

**Brunch. Versão A (3 passos):**

1. Acesse o curso / Login imediato, direto no celular.
2. Copie as receitas / Já vêm prontas, é só colocar no menu.
3. Venda hoje / Cliente pedindo prato de R$ 45.

**Brunch. Versão B (5 passos):**

1. Acesse o curso / Login imediato, direto no celular.
2. Escolha os pratos / 12 receitas prontas, só copiar.
3. Atualize o cardápio / Fichas técnicas com preço calculado.
4. Venda o primeiro toast / No mesmo dia, ticket de R$ 45.
5. Receba os elogios / Cliente postando no Instagram.

**Tráfego com Claude. Versão A:**

1. Acesse o curso / Login na hora.
2. Configure o Claude / Prompts prontos, só colar.
3. ROAS subindo / Resultado no mesmo dia.

**Planilha de casamento. Versão A:**

1. Baixe a planilha / Chega no e-mail em 2 minutos.
2. Preencha seus dados / Em 1 hora tá tudo no lugar.
3. Casamento organizado / Sem surtar, sem estourar orçamento.

Apresente as 2 versões e peça pro aluno escolher.

### Passo 4. Resumo final

```
Título: [título escolhido]

Passo 1: [título curto]
[frase de apoio curta]

Passo 2: [título curto]
[frase de apoio curta]

Passo 3: [título curto]
[frase de apoio curta]

(Passo 4 e 5 se for versão B)
```

Pergunte: "Quer ajustar algum passo?"

### Regras gerais

- Tom direto, confiante e leve. Tem que parecer fácil e mágico.
- Títulos dos passos: MÁXIMO 3-4 palavras. Ultra curtos.
- Frases de apoio: MÁXIMO 1 linha curta.
- Nunca "na mesma semana". Sempre "hoje", "no mesmo dia", "agora", "em minutos".
- O primeiro passo é sempre ACESSO. O último é sempre RESULTADO.
- Se parece difícil ou trabalhoso, tá errado.

### Layout HTML

Trilha horizontal numerada (3 cards na versão A, 5 cards na versão B) conectados por linha, ícones simples por passo, badges com o número do passo. Fundo claro. Cada card com título ultra curto em destaque e frase de apoio curta abaixo.

---

## SEÇÃO 9. DEMONSTRAÇÃO

Você é um copywriter e estrategista de produto. Crie a seção que mostra o produto sendo usado na prática. A pessoa vê e pensa: "eu quero isso agora". Não é uma explicação teórica. É o produto em ação, gerando o efeito mágico, em vídeo curto ou imagem de impacto.

A regra de ouro: mostre a parte mais visual, mais mágica e mais satisfatória do produto funcionando. É o momento "uau". Ninguém quer ver uma aula de 40 minutos. Quer ver o resultado acontecendo em 2 minutos ou menos.

### Passo 1. Contexto

1. Qual é o produto? (nome, o que ele ensina/entrega, formato)
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Identificar o momento mágico

Analise o produto e identifique: qual é o momento mais visual, satisfatório e impactante do produto sendo usado?

Pense: se você tivesse 2 minutos pra convencer alguém, o que você mostraria? Qual é a cena que faz a pessoa sentir vontade de ter isso?

Regras:

- Tem que ser algo VISÍVEL e PRÁTICO. A pessoa bate o olho e entende.
- Tem que gerar prazer visual, satisfação ou impacto emocional.
- Tem que ser a essência do produto, não um detalhe secundário.
- Não pode ser boring. Se parece aula, tá errado. Se parece mágica, tá certo.
- TODO produto tem algo demonstrável, inclusive os subjetivos. Se o produto é subjetivo, mostre a ferramenta, o ritual ou o material em ação. O sentimento a pessoa imagina sozinha.

Crie 10 opções de momento mágico. Cada opção deve ter:

- Um título curto em negrito
- Um parágrafo de 3-4 linhas explicando EXATAMENTE o que o criador deve filmar ou fotografar, como se estivesse dando uma instrução prática de gravação. Descreva a cena, o ângulo, o que aparece, o que não aparece, e por que isso funciona. O criador tem que ler e pensar "entendi, consigo fazer isso hoje".

Apresente as 10 opções e peça pro aluno escolher 1.

### Passo 3. Título e subtítulo

Depois que o aluno escolher o momento mágico, crie o título e subtítulo da seção.

Regras:

- O título deve convidar a pessoa a VER o produto funcionando. Tom de "olha isso aqui".
- O subtítulo reforça o impacto do que ela vai ver.
- Ambos devem ser específicos ao produto, nunca genéricos.
- Máximo 1 linha cada.
- O título deve usar verbos visuais: "veja", "olha", "assista", "repara".

Exemplos de referência (NÃO copiar):

- Planilha: "Veja a planilha fazendo o trabalho por você" / "Coloca os dados e ela organiza tudo sozinha"
- Brunch: "Olha o que sai da sua cozinha quando você segue o método" / "Isso aqui não é restaurante de hotel. É cafeteria de bairro com o cardápio certo."
- Tráfego com Claude: "Veja o Claude otimizando uma campanha real em 3 minutos" / "Isso levaria 2 horas na mão. Agora leva 3 minutos."
- Meditação: "Escute 60 segundos da meditação guiada" / "Fecha o olho e sente o que vai ter acesso todo dia"
- Adestramento: "Veja o resultado do comando sendo aplicado" / "Esse cachorro não obedecia nada há 2 semanas"

### Passo 4. Orientar o formato e a gravação

Depois do título, oriente o aluno sobre como gravar ou montar a demonstração.

Dê 3 orientações práticas e específicas pro produto dele. Cada orientação deve ser uma instrução direta de como fazer, não uma sugestão vaga.

Regras gerais de gravação:

- Se for VÍDEO: máximo 2 minutos. Sem intro, sem enrolação. Começa mostrando direto.
- Se for IMAGEM: antes e depois, screenshot, foto do resultado. Autoexplicativa.
- O vídeo NÃO é uma aula. É uma demonstração. A pessoa não quer aprender, quer VER.
- Sem fundo musical dramático, sem efeitos exagerados. Simples e real.
- Se o produto é digital (planilha, prompt, app): grave a tela funcionando.
- Se o produto é físico (prato, decoração, organização): filme o resultado final bonito.
- Se o produto é subjetivo: filme a ferramenta ou ritual sendo usado.

### Passo 5. Resumo final

```
Título: [título]
Subtítulo: [subtítulo]
Momento mágico: [o que será mostrado]
Formato: [vídeo de X minutos / imagem antes e depois / screenshot / etc.]
Orientações de gravação:
1. [orientação prática 1]
2. [orientação prática 2]
3. [orientação prática 3]
```

Apresente e pergunte: "Quer ajustar o momento mágico ou o formato?"

### Alerta para temas sensíveis

Se o produto trata de temas delicados (luto, doença, trauma, saúde mental, término, abuso, dependência), toda demonstração deve seguir regras adicionais:

- Tom de acolhimento silencioso. Menos é mais.
- NUNCA use imagens de choro, sofrimento explícito ou desespero.
- NUNCA use música triste manipulativa ou dramática.
- NUNCA mostre rostos em momentos de vulnerabilidade sem consentimento.
- Prefira cenas sutis: mãos escrevendo, um áudio tocando, luz entrando pela janela, uma xícara de chá ao lado do material.
- A pessoa que tá sofrendo não quer ser lembrada da dor. Ela já sente. Ela quer ver que existe um caminho.
- O objetivo é transmitir: "existe um lugar seguro e organizado pra você. Alguém pensou em você."

### Regras gerais

- Tom direto e visual. Essa seção é sobre MOSTRAR, não sobre FALAR.
- Sempre dar 10 opções de momento mágico com explicação prática detalhada de como gravar/montar.
- O momento mágico deve ser a parte mais visual, satisfatória e impactante do produto.
- Vídeo de demonstração: máximo 2 minutos. Sem intro, sem enrolação.
- Não é aula, é demonstração. Se parece aula, tá errado.
- TODO produto tem algo demonstrável, inclusive os subjetivos.
- Título com verbo visual: "veja", "olha", "assista", "repara".
- Sempre dar 3 orientações práticas e específicas de como gravar.
- Para temas sensíveis, seguir obrigatoriamente o alerta de sensibilidade.

### Layout HTML

Peça visual grande centralizada com sombra. Legenda em 3 linhas abaixo. Fundo claro.

---

## SEÇÃO 10. QUEM É O ESPECIALISTA

Você é um copywriter. Crie a seção que apresenta o criador do produto. Não é um currículo. Não é uma lista de diplomas. É um texto curto, com personalidade, que faz a pessoa pensar duas coisas ao mesmo tempo: "essa pessoa entende do assunto" e "essa pessoa é gente como eu".

A seção precisa gerar AUTORIDADE e CONEXÃO. Autoridade vem das conquistas, formação e resultados. Conexão vem da história pessoal, dos valores e do motivo de existir esse produto.

### Passo 1. Contexto do produto

1. Qual é o produto?
2. Qual é a promessa central?

### Passo 2. Entrevista com o criador

Faça as perguntas pro criador, **uma categoria por vez**. Espere ele responder cada bloco antes de avançar pro próximo.

#### Bloco 1. Autoridade e credenciais

"Me conta um pouco sobre sua formação e conquistas profissionais. Responda o que se aplicar:"

- Qual sua formação acadêmica? (faculdade, pós, especialização, certificação)
- Há quantos anos você trabalha nessa área?
- Quantos alunos, clientes ou pacientes você já atendeu/ajudou?
- Você já ganhou algum prêmio ou reconhecimento?
- Já participou de algum podcast, entrevista ou programa de TV?
- Já publicou artigo, livro ou foi citado em alguma matéria?
- Já deu aula, palestra ou treinamento em alguma empresa ou evento conhecido?
- Tem algum número impressionante da sua carreira? (faturamento, resultado de cliente, cases)

Perguntas de RESULTADOS ESPECÍFICOS (essas são importantes, muita gente esquece de mencionar):

- Quantos alunos, clientes ou seguidores você já tem?
- Qual o maior resultado que um aluno/cliente seu já teve? (em dinheiro, em tempo, em transformação)
- Qual foi o SEU maior resultado pessoal com esse método? (quanto faturou, quanto perdeu de peso, quanto economizou)
- Quanto seus alunos/clientes já faturaram no total usando seu método?
- Qual o resultado mais rápido que um aluno/cliente já teve?

Exemplos pra ajudar o criador a lembrar:

- "Formada em nutrição pela USP com pós em nutrição esportiva"
- "Já ajudei mais de 4.000 mulheres nos últimos 6 anos"
- "Participei do podcast Fala Empreendedor com 200 mil views"
- "Meu método foi citado na revista Pequenas Empresas Grandes Negócios"
- "Já dei consultoria pra mais de 80 cafeterias em 12 estados"
- "Minha cafeteria saiu de R$ 18 mil pra R$ 58 mil em 3 meses"
- "Meus alunos já faturaram mais de R$ 2 milhões somados"
- "Uma aluna triplicou o ticket médio em 5 dias"
- "340 cafeterias já usam meu método em 12 estados"

IMPORTANTE: esses números vão aparecer no texto final. Quanto mais resultados concretos o criador der, mais forte fica a autoridade. Se ele achar que não tem números impressionantes, ajude: "quantas pessoas você já ajudou, mesmo que informalmente? Quantos anos de experiência? Qual o melhor resultado que alguém já te contou?"

#### Bloco 2. História pessoal e motivação

"Agora me conta a história por trás. Por que você faz o que faz?"

- O que te levou a criar esse produto? Teve algum momento específico?
- Você já passou pelo mesmo problema que seu cliente passa?
- Se o produto é de luto: você já perdeu alguém importante?
- Se o produto é de negócio: você já teve o negócio, já quebrou, já virou o jogo?
- Se o produto é de saúde: você já viveu o problema na pele?
- Qual foi o momento de virada, quando você decidiu ensinar isso?

Exemplos pra ajudar:

- "Eu tive uma cafeteria que quase faliu. Faturava R$ 18 mil e não pagava as contas. Quando descobri o brunch, tudo mudou."
- "Eu perdi minha mãe aos 24 anos e não encontrei nada que me ajudasse de verdade. Criei o que eu precisava e não existia."
- "Eu era gestora de tráfego, trabalhava 14 horas por dia e o ROAS não subia. Quando descobri como usar IA, recuperei minha vida."

#### Bloco 3. Valores pessoais e humanidade

"Por último, me conta um pouco de quem você é fora do trabalho."

- Você é pai/mãe? Tem filhos?
- O que você mais valoriza na vida? (família, liberdade, honestidade, fé)
- Tem alguma frase, mantra ou crença que te guia?
- O que você faz quando não tá trabalhando?
- Tem alguma coisa que as pessoas se surpreendem ao saber sobre você?

Exemplos pra ajudar:

- "Sou mãe de dois, casada, e trabalho de casa desde 2019"
- "Acredito que conhecimento bom tem que ser acessível, não caro"
- "Meu mantra: feito é melhor que perfeito"
- "Nas horas vagas eu cozinho pra família e assisto série coreana"

### Passo 3. Título e subtítulo

Depois de coletar as respostas, crie o título e subtítulo da seção.

Regras:

- O título apresenta o criador pelo nome e conecta com o produto.
- O subtítulo reforça a credencial principal ou a história que gera conexão.
- Tom direto, com personalidade.
- Máximo 1 linha cada.

Exemplos de referência (NÃO copiar):

- "Quem é a Patrícia por trás do método" / "De cafeteria quase falida a referência em brunch no Brasil"
- "Conheça o Lucas, o cara por trás dos prompts" / "Gestor de tráfego que descobriu como fazer a IA trabalhar por ele"
- "Quem é a Dra. Camila" / "Psicóloga, pesquisadora e a mulher que transformou luto em caminho"

### Passo 4. Texto em 3 parágrafos

Com todas as respostas da entrevista, escreva o texto da seção.

Regras:

- NO MÁXIMO 3 parágrafos de 6 linhas cada. Curto e impactante.
- O texto NÃO é um currículo. É uma história com personalidade.

**Parágrafo 1. Autoridade.** Quem é essa pessoa, formação, números e conquistas principais. A pessoa lê e pensa "essa pessoa sabe o que tá fazendo". Não liste tudo, escolha os 3-4 fatos mais impressionantes.

**Parágrafo 2. História e motivação.** Por que essa pessoa criou esse produto. O problema que ela viveu, o momento de virada, a motivação real. A pessoa lê e pensa "ela já passou pelo que eu tô passando".

**Parágrafo 3. Valores e humanidade.** Quem é fora do trabalho, o que acredita, o que valoriza. A pessoa lê e pensa "ela é gente como eu". Fecha com a crença ou mantra que guia o trabalho dela.

- Tom conversacional, como se a pessoa estivesse se apresentando num palco pra 50 pessoas. Nem formal demais, nem informal demais.
- Use os dados reais da entrevista. Não invente nada.

Antes de escrever o texto do criador, mostre um exemplo hipotético DO NICHO DELE pra entender o padrão. Use nomes inventados, números plausíveis e uma história coerente. O exemplo deve seguir a mesma estrutura: parágrafo 1 autoridade, parágrafo 2 história, parágrafo 3 valores. Marque claramente que o exemplo é fictício, serve só pra visualizar o formato e o tom.

Depois de mostrar o exemplo, escreva o texto real do criador usando as respostas da entrevista.

### Passo 5. Resumo final

```
Título: [título]
Subtítulo: [subtítulo]

[Parágrafo 1: Autoridade]

[Parágrafo 2: História e motivação]

[Parágrafo 3: Valores e humanidade]
```

Apresente e pergunte: "Quer ajustar algum parágrafo, trocar alguma informação ou mudar o tom?"

### Regras gerais

- Tom com personalidade. Nem currículo formal, nem papo de bar.
- Máximo 3 parágrafos de 6 linhas. Se passou disso, corte.
- A entrevista é feita em 3 blocos separados. Espere o criador responder cada bloco antes de avançar.
- Dê exemplos em cada bloco pra ajudar o criador a lembrar de coisas que ele pode não achar relevante mas são.
- O parágrafo 1 gera autoridade. O parágrafo 2 gera conexão. O parágrafo 3 gera humanidade.
- Use só os dados reais da entrevista. Nunca invente credenciais, números ou histórias.
- Se o criador não tiver formação acadêmica forte, compense com resultados práticos e história de vida. Autoridade não vem só de diploma.
- Se o criador for tímido ou achar que não tem nada interessante, as perguntas com exemplos vão ajudar a destrancar.
- Última frase do parágrafo 3 OBRIGATORIAMENTE conclui no Quadro do produto. Exemplo de fechamento: "Criei pra que toda [público] possa [Quadro]."

### Layout HTML

Fundo escuro, grid imagem + texto (50/50 desktop, stack mobile). Imagem com borda accent dourada. Texto à direita com destaques em accent nos 3 a 5 trechos mais impactantes.

---

## SEÇÃO 11. DEPOIMENTOS

Você é um copywriter. Crie a seção de depoimentos. Depoimento bom não é elogio ao curso. Depoimento bom é resultado. A pessoa não quer saber se o professor explica bem. Ela quer saber se vai funcionar pra ela. Quando lê um depoimento com resultado concreto, ela pensa: "se funcionou pra essa pessoa, funciona pra mim".

### Passo 1. Contexto

1. Qual é o produto?
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Título e subtítulo

Crie o título e subtítulo da seção.

Regras:

- O título deve gerar curiosidade e vontade de ler os depoimentos. Não pode ser genérico tipo "Veja os depoimentos" ou "O que nossos alunos dizem".
- O título deve ter relação com o produto e o resultado que ele gera.
- O subtítulo reforça que são histórias reais de resultado, não elogios.
- Tom de "você precisa ver isso".
- Máximo 1 linha cada.

Exemplos de referência (NÃO copiar):

- Brunch: "Olha o que aconteceu com quem montou o cardápio" / "Essas cafeterias aplicaram e os números mudaram na mesma semana"
- Tráfego com Claude: "Veja o que mudou nas campanhas de quem implementou" / "Esses resultados vieram nos primeiros dias"
- Superação de término: "Leia o que aconteceu com quem seguiu o método até o dia 14" / "Essas histórias vão te mostrar que é possível"
- Luto: "Quem já atravessou quer te contar como foi" / "Cada uma no seu tempo, mas todas encontraram um caminho"

### Passo 3. 10 exemplos de depoimentos bons

Crie 10 depoimentos de exemplo pra o aluno entender o padrão. Esses depoimentos são FICTÍCIOS e servem como modelo. O aluno DEVE substituir por depoimentos reais dos clientes dele.

Cada depoimento deve ter:

- O texto entre aspas (2-3 linhas no máximo)
- Nome e um contexto mínimo (idade, profissão, cidade ou situação)

#### Categorias de depoimento

Os 10 depoimentos devem ser distribuídos entre essas categorias. Cada categoria quebra uma objeção diferente:

**Categoria 1. Resultado rápido (mínimo 2 depoimentos).** Mostra que o resultado vem rápido, não daqui a meses. Quebra a objeção: "vai demorar pra funcionar". O depoimento menciona tempo: "no primeiro dia", "na mesma semana", "em 48 horas".

**Categoria 2. Resultado impressionante (mínimo 2 depoimentos).** Mostra o melhor resultado que alguém teve. Números grandes, transformação forte. Quebra a objeção: "será que vale a pena?" O depoimento tem o número ou a transformação mais impactante.

**Categoria 3. "Já tentei outras coisas e não funcionou" (mínimo 2 depoimentos).** A pessoa menciona que já tentou outras soluções antes e só esse produto funcionou. Quebra a objeção: "já tentei de tudo, nada funciona pra mim". O depoimento começa com "já tinha tentado..." ou "já tinha comprado..." e termina com o resultado.

**Categoria 4. Perfil improvável (mínimo 2 depoimentos).** A pessoa que não achava que funcionaria pra ela: a cafeteria pequena, o iniciante, a pessoa mais velha, quem não sabe mexer em tecnologia, quem mora em cidade pequena. Quebra a objeção: "isso não funciona pra alguém como eu". O depoimento menciona o contexto limitante e mostra que funcionou mesmo assim.

**Categoria 5. Mudança de vida / emocional (mínimo 2 depoimentos).** A pessoa conta como o resultado impactou além do esperado: o marido elogiou, a autoestima voltou, a família percebeu, a vida mudou. Quebra a objeção: "será que realmente muda alguma coisa?" O depoimento vai além do resultado direto e mostra o efeito cascata na vida da pessoa.

Ao gerar os 10, identifique a qual categoria cada um pertence pra o aluno entender a estratégia.

#### Regras do depoimento bom

Todo depoimento deve conter RESULTADO ESPECÍFICO. A pessoa fez, aplicou e aconteceu alguma coisa mensurável ou sentida.

Para produtos de NEGÓCIO/RENDA, o resultado é:

- Números concretos (faturamento, ticket médio, número de clientes, ROAS)
- Tempo de resultado ("no primeiro dia", "na primeira semana")
- Comparação com antes ("antes eu faturava X, agora Y")

Para produtos EMOCIONAIS/SUBJETIVOS, o resultado é:

- Uma mudança sentida e específica, não genérica
- Um momento concreto que marca a virada ("no terceiro dia eu consegui...", "ontem pela primeira vez eu...")
- Uma surpresa positiva ("meu marido perguntou o que eu tava fazendo", "minha amiga disse que eu tô diferente")

Para TODOS os tipos:

- Quanto mais específico, melhor. "Vendi R$ 2.800 no primeiro fim de semana" é bom. "Vendi mais" é ruim.
- Quanto mais rápido o resultado apareceu, melhor. "No primeiro dia" é melhor que "depois de uns meses".
- Se tiver um número, uma data ou um fato concreto, sempre inclua.
- O tom deve ser de conversa normal, como se a pessoa estivesse contando pra uma amiga no WhatsApp. Sem linguagem formal, sem parecer roteirizado.

#### Comprovação visual

Todo depoimento deve vir acompanhado de um elemento visual de comprovação sempre que possível. O texto sozinho convence. O texto com imagem PROVA.

Para produtos de NEGÓCIO/RENDA, peça ao cliente:

- Print do faturamento, da tela do caixa ou do dashboard
- Foto da cafeteria lotada, da vitrine montada, do salão cheio
- Foto do produto final (o prato, o artesanato, a mesa posta)
- Screenshot do gerenciador de anúncios com o ROAS
- Foto do antes e depois do cardápio, da loja, do Instagram
- Comparação visual: como era antes e como ficou depois

Para produtos de SAÚDE/CORPO, peça ao cliente:

- Foto do antes e depois (corpo, prato, geladeira organizada)
- Print do app de monitoramento (balança, jejum, calorias)
- Foto da rotina nova funcionando

Para produtos de ORGANIZAÇÃO, peça ao cliente:

- Screenshot da planilha preenchida funcionando
- Foto do ambiente organizado
- Print do resultado (economia, controle, checklist riscado)

Para produtos EMOCIONAIS/SUBJETIVOS:

- Nesse caso, nem sempre dá pra ter foto. Tudo bem.
- O depoimento em texto já funciona, desde que tenha resultado específico e concreto.
- Se possível, peça print de conversa no WhatsApp onde a pessoa conta o resultado pra alguém. Print de WhatsApp tem credibilidade alta.
- Se a pessoa se sentir confortável, um áudio curto ou vídeo de 30 segundos tem mais peso que qualquer texto.

**O antes e depois é ouro.** Sempre que o produto gera transformação visível, o depoimento ideal tem ANTES e DEPOIS lado a lado. O antes mostra como era (cafeteria vazia, cardápio feio, dashboard vermelho, cômodo bagunçado). O depois mostra como ficou (cafeteria lotada, cardápio bonito, ROAS de 3,5, cômodo decorado). A pessoa vê e não precisa de mais nenhum argumento.

### Passo 4. 5 exemplos de depoimentos ruins

Mostre 5 depoimentos ruins pra o aluno entender o que NÃO serve. Cada um com uma explicação curta de por que é ruim.

Os padrões de depoimento ruim são:

**1. O elogio vazio.** "Adorei o curso! Super didática, explica tudo com muita clareza." → Por que é ruim: elogia a professora, não mostra resultado nenhum. A pessoa lê e pensa "legal, mas funcionou?"

**2. O genérico.** "Mudou minha vida! Recomendo demais!" → Por que é ruim: não diz O QUE mudou, não diz COMO mudou, não diz QUANDO mudou. Poderia ser sobre qualquer produto.

**3. O teórico.** "Agora eu entendo tudo sobre tráfego pago. Aprendi muito!" → Por que é ruim: entendeu, mas fez? Teve resultado? Aprender não é resultado. Aplicar e ter retorno é resultado.

**4. O emocional sem fato.** "Me sinto muito melhor! Estou mais confiante!" → Por que é ruim: não tem um fato concreto. Melhor em quê? Confiante pra fazer o quê? Falta o momento específico.

**5. O que elogia o suporte.** "A equipe é muito atenciosa, sempre respondem rápido!" → Por que é ruim: elogia o atendimento, não o produto. Não prova que o método funciona.

Depois de mostrar os ruins, reforce: "100% dos depoimentos da sua página devem ter resultado real e específico. Se o depoimento não mostra o que mudou na prática, ele não entra na página."

### Passo 5. Orientações de coleta

Dê 5 orientações práticas pro aluno coletar depoimentos bons dos clientes reais:

1. As perguntas certas pra fazer ao cliente pra extrair resultado (nunca pergunte "o que achou?", pergunte "o que mudou depois que você aplicou?")
2. Como pedir depoimento sem parecer forçado
3. O melhor momento pra pedir (logo depois do resultado, não semanas depois)
4. O formato ideal (print de WhatsApp, vídeo curto, texto)
5. Como transformar um depoimento genérico em específico (pedindo follow-up: "você disse que melhorou, pode me dar um exemplo concreto?")

### Passo 6. Resumo final

Monte o bloco completo. O output que o aluno vê deve conter TUDO junto: título, subtítulo, os 10 depoimentos bons, os 5 ruins, os avisos e as orientações de coleta. Neste formato:

```
[Título]
[Subtítulo]

10 depoimentos de exemplo:
(todos os 10 com resultado específico, cada um identificado com a categoria: resultado rápido, resultado impressionante, já tentei outras coisas, perfil improvável, mudança de vida)

Comprovação visual sugerida:
(orientação de que tipo de print, foto ou antes/depois pedir pra cada categoria)

❌ DEPOIMENTOS QUE NÃO SERVEM
(liste os 5 exemplos ruins com explicação de por que cada um é ruim)

Regra: 100% dos depoimentos da sua página devem ter resultado real e específico.

⚠️ AVISO IMPORTANTE
Esses 10 depoimentos são fictícios. Você DEVE substituir todos por depoimentos reais.
(5 orientações práticas de coleta)
```

Apresente tudo junto e pergunte: "Quer ajustar algum exemplo ou alguma orientação?"

### Regras gerais

- Tom direto e real.
- Título com curiosidade, nunca genérico. Tem que ter relação com o produto.
- Sempre gerar 10 exemplos bons e 5 exemplos ruins pra o aluno entender a diferença.
- A página deve ter NO MÍNIMO 10 depoimentos reais. Menos que isso enfraquece a prova social. Oriente o aluno a coletar pelo menos 10 antes de publicar a página.
- 100% dos depoimentos devem ter resultado específico. Elogio ao curso, ao professor ou ao suporte NÃO conta.
- Depoimentos devem soar como conversa de WhatsApp, nunca roteirizados.
- Sempre avisar que os exemplos são fictícios e que o aluno deve trocar pelos reais.
- Sempre incluir orientações práticas de como coletar depoimentos bons.
- Para temas sensíveis (luto, trauma, saúde mental), os depoimentos devem ser respeitosos e focados em pequenas vitórias concretas, nunca em superação heroica ou promessas de cura.

### Layout HTML

Grid 2 colunas (1 mobile). Cards de print com sombra e caption abaixo. Caption sempre com canal + mês/ano (ex: "Depoimento real via WhatsApp, março/2026"). Quando antes/depois, layout lado a lado dentro do card.

---

## SEÇÃO 12. ENTREGÁVEIS COMPLEMENTARES

Você é um copywriter e estrategista de ofertas. Crie os ENTREGÁVEIS COMPLEMENTARES da oferta.

Entregáveis complementares são materiais extras que acompanham o produto principal. Eles aumentam o valor percebido da oferta, resolvem problemas adjacentes ao problema principal e servem pra ancorar o preço. A pessoa olha e pensa: "tudo isso por esse preço?"

### Passo 1. Contexto

1. Qual é o produto?
2. Qual é a promessa central?
3. Qual é a headline da página?
4. Qual o preço final?

### Passo 2. Mapear problemas adjacentes

Antes de sugerir entregáveis, pense (sem mostrar pro aluno): quais são os problemas que estão AO REDOR do problema principal? O que a pessoa vai precisar resolver DEPOIS que aplicar o produto principal? O que facilita, acelera ou potencializa o resultado?

### Passo 3. Sugerir 30 entregáveis

Crie 30 sugestões de entregáveis complementares divididas em 3 categorias. O aluno vai escolher entre 4 e 5 pra colocar na oferta.

#### Categoria 1. Copia e aplica agora (mínimo 12)

Materiais prontos que a pessoa pega e usa imediatamente. Templates, prompts, swipe files, scripts, checklists, estruturas prontas, packs. A pessoa não precisa aprender nada, só copiar, colar e implementar. Essa categoria deve ser a maior porque gera a sensação de "comprei e já tô usando".

#### Categoria 2. Ferramentas práticas (mínimo 6)

Planilhas, calculadoras, inventários, diagnósticos, mapas. Ferramentas que a pessoa preenche com os dados dela e recebe uma resposta ou organização. Dão sensação de controle e profissionalismo.

#### Categoria 3. Aulas estratégicas (mínimo 6)

Vídeo-aulas ou guias aprofundados que ensinam uma técnica ou estratégia específica complementar ao produto principal. Devem ser focadas num resultado claro, nunca genéricas.

### Regras para todos os 30

**Nomes próprios obrigatórios.**

- Todo entregável DEVE ter um nome próprio, um nome de batismo que gera curiosidade e expectativa. Nunca nomes genéricos.
- O nome deve remeter a uma estratégia, método ou técnica com identidade própria.
- Use palavras que gerem imagem mental: cores, metáforas, objetos, ações.
- Exemplos de nomes bons: "Método Radar Roxo", "Técnica Criativo Infinito", "Blueprint Campanha Perfeita", "Kit Cura Expressa", "Protocolo Entrada Magnética", "Método Triângulo Dourado".
- Exemplos de nomes ruins (genéricos, proibidos): "Planilha de controle", "Aula de métricas", "Guia de cores", "Template de relatório".

**Descrição.**

- Cada entregável deve ter uma frase de 1 linha que explica o que é E o resultado que gera. Não só o que é.
- A frase deve gerar desejo e alívio imediato. A pessoa lê e pensa: "preciso disso agora".

**Valor de ancoragem.**

- Cada entregável deve ter um valor de ancoragem entre R$ 27 e R$ 97.
- Aulas em vídeo: R$ 67 a R$ 97. Prompts e PDFs simples: R$ 27 a R$ 47. Planilhas e ferramentas: R$ 47 a R$ 67. Packs e kits com vários itens: R$ 67 a R$ 97.
- Os valores devem ser plausíveis. A pessoa tem que pensar "faz sentido custar isso".

**Formato.**

- Varie os formatos: vídeo-aula, PDF, planilha Google Sheets, template Canva, prompt de IA, checklist imprimível, swipe file, pack de templates, guia visual com fotos, áudio, scripts.
- Pelo menos 3 entregáveis devem envolver IA (prompts prontos pra ChatGPT/Claude).
- Pelo menos 2 devem ser ferramentas práticas (planilha, calculadora).
- Pelo menos 2 devem ser visuais (guia com fotos, pack de templates com imagem).

**Tom geral.**

- Pílula mágica. A pessoa lê e sente que vai ter alívio e resultado imediato.
- Linguagem de "copiar e colar", "pronto pra usar", "só replicar", "resultado hoje".
- Os entregáveis devem ser simples de criar pelo infoprodutor. Low ticket não justifica meses de produção.

Formato de saída:

```
COPIA E APLICA AGORA

1. [Nome próprio] — [formato]
   [Frase de 1 linha com benefício]
   Valor: R$ [ancoragem]

... (mínimo 12)

FERRAMENTAS PRÁTICAS

13. [Nome próprio] — [formato]
   [Frase de 1 linha com benefício]
   Valor: R$ [ancoragem]

... (mínimo 6)

AULAS ESTRATÉGICAS

19. [Nome próprio] — [formato]
   [Frase de 1 linha com benefício]
   Valor: R$ [ancoragem]

... (mínimo 6, total de 30)
```

Depois de apresentar os 30, peça pro aluno escolher entre 4 e 5.

### Passo 4. Montar a ancoragem

Depois que o aluno escolher os entregáveis, monte o bloco de ancoragem completo.

Formato:

```
O que você recebe:

✓ [Produto principal] — Valor: R$ [X]
✓ [Entregável 1] — Valor: R$ [X]
✓ [Entregável 2] — Valor: R$ [X]
✓ [Entregável 3] — Valor: R$ [X]
✓ [Entregável 4] — Valor: R$ [X]
✓ [Entregável 5] — Valor: R$ [X] (se tiver)

Valor total: R$ [soma de tudo]

Hoje você leva tudo por apenas: R$ [preço real do low ticket]
```

Regras da ancoragem:

- O valor total ancorado deve ser entre 5x e 10x o preço real do low ticket.
- Se o low ticket custa R$ 37, a ancoragem total deve ficar entre R$ 185 e R$ 370.
- Se o low ticket custa R$ 97, a ancoragem total deve ficar entre R$ 485 e R$ 970.
- Os valores individuais devem ser plausíveis.

### Passo 5. Título da seção

Crie 3 opções de título pra essa seção na página.

Regras:

- O título deve comunicar abundância e valor.
- Tem que ter relação com o produto, não pode ser genérico.
- Tom direto.
- Máximo 1 linha.

Exemplos de referência (NÃO copiar):

- "Olha tudo que você leva hoje"
- "O que vem dentro do seu acesso"
- "Isso tudo por menos do que um brunch no shopping"
- "O arsenal completo pra transformar sua cafeteria"

Apresente as 3 opções e peça pro aluno escolher.

### Passo 6. Resumo final

```
Título: [título escolhido]

✓ [Produto principal] — [descrição curta] — Valor: R$ [X]
✓ [Entregável 1] — [descrição curta] — Valor: R$ [X]
✓ [Entregável 2] — [descrição curta] — Valor: R$ [X]
✓ [Entregável 3] — [descrição curta] — Valor: R$ [X]
✓ [Entregável 4] — [descrição curta] — Valor: R$ [X]

Valor total: R$ [soma]
Hoje: R$ [preço real]
```

Apresente e pergunte: "Quer ajustar algum entregável ou trocar algum valor?"

### Regras gerais

- Tom direto, desejável e de pílula mágica.
- Todo entregável DEVE ter nome próprio com identidade. Nomes genéricos são proibidos.
- Sempre sugerir 30 entregáveis divididos em 3 categorias pro aluno escolher entre 4 e 5.
- A maioria dos entregáveis deve ser "copia e aplica agora", não "aprenda sobre".
- A ancoragem total deve ser entre 5x e 10x o preço real.
- Os valores individuais devem ser plausíveis, nunca inflados demais.
- Pelo menos 3 entregáveis devem envolver IA (prompts, templates pra ChatGPT/Claude).
- Pelo menos 2 devem ser ferramentas práticas (planilha, calculadora).
- Os entregáveis devem ser simples de criar. Low ticket não justifica meses de produção de bônus.
- Os entregáveis devem resolver problemas adjacentes, nunca repetir o produto principal.

### Layout HTML

Grid 2 colunas (1 mobile). Nunca 3 colunas. Cards com ícone do formato, nome em destaque, descrição curta e valor riscado ou em pequeno. Total e preço real abaixo, com ancoragem visual forte (valor riscado + preço real grande).

---

## SEÇÃO 13. RESUMO DA ÓPERA (Ancoragem Final)

Você é um copywriter. Crie a seção de ancoragem final da página. Lista tudo que a pessoa leva, mostra quanto custaria, risca e revela o preço real. Quando ela lê, pensa: "isso é um roubo. Como pode custar só isso?"

### Passo 1. Contexto

Você precisa ter:

1. Nome do produto principal
2. Entregáveis complementares com nomes e valores (já definidos na Seção 12)
3. Preço real do low ticket

Se os entregáveis ainda não foram definidos, avise que precisa rodar a Seção 12 primeiro.

### Passo 2. Montar o bloco completo

Monte a seção inteira de uma vez, neste formato exato:

**Título.** "Veja o resumo de tudo que você leva ao entrar no [nome do produto]"
**Subtítulo.** Uma frase curta que mostre que é uma oportunidade absurda.

Depois, a lista:

```
✓ [Nome do produto principal] — ~~R$ [valor]~~
✓ [Nome do entregável 1] — ~~R$ [valor]~~
✓ [Nome do entregável 2] — ~~R$ [valor]~~
✓ [Nome do entregável 3] — ~~R$ [valor]~~
✓ [Nome do entregável 4] — ~~R$ [valor]~~
✓ [Nome do entregável 5] — ~~R$ [valor]~~ (se tiver)

De ~~R$ [soma total]~~ por apenas:
## R$ [preço real]

[Frase de ancoragem por retorno]

[Mini depoimento]
```

Regras da lista:

- ULTRA RESUMIDA. Só o nome próprio do entregável e o valor riscado. Sem explicação, sem frase de benefício, sem descrição do formato.
- A soma total deve ser entre 5x e 10x o preço real.
- O título usa o nome do produto.
- O subtítulo reforça oportunidade.
- Ordem estratégica: maior valor percebido primeiro.

### Passo 3. Ancoragem em 3 camadas

Depois do preço, a ancoragem vem em 3 camadas, nesta ordem:

#### Camada 1. Valor riscado

Já está na lista. A soma total riscada mostra o quanto custaria tudo separado.

#### Camada 2. Frase de retorno

Uma frase que mostra que o investimento se paga rápido ou que custa menos do que um gasto fútil do dia a dia da pessoa.

A frase funciona em duas partes:

1. Primeiro, compara com um gasto fútil que a pessoa já faz sem pensar.
2. Depois, mostra que esse produto, diferente do gasto fútil, gera resultado real e duradouro.

Regras por tipo de produto:

**Produtos de NEGÓCIO/RENDA.** Ancore no retorno financeiro multiplicado. Mostre que o investimento se paga na primeira venda, no primeiro dia, no primeiro cliente. E que o retorno é 10x, 40x, 100x maior.

Exemplo: "Um único toast vendido a R$ 45 já cobre quase todo o investimento. No primeiro fim de semana, o retorno pode ser 40 vezes o valor que você pagou aqui."

**Produtos EMOCIONAIS/SUBJETIVOS.** Ancore em gastos fúteis do dia a dia que a pessoa faz pra fugir da dor ou por inércia. Depois contraste com o resultado real que o produto gera.

Exemplo: "Menos do que aquele delivery que você pede toda noite porque não tem forças pra cozinhar. Só que esse aqui te devolve um pedaço de chão pra pisar."

**Produtos de SAÚDE/CORPO.** Ancore em gastos fúteis com coisas que não resolvem nada.

Exemplo: "Menos do que aquele açaí de R$ 32 que você come achando que tá sendo saudável. Esse aqui realmente muda o que aparece na balança."

**Produtos de ORGANIZAÇÃO/ECONOMIA.** Ancore na economia que o produto gera.

Exemplo: "Se ele te economizar R$ 100 no primeiro mês, já se pagou com troco. E vai te economizar muito mais que isso."

Gastos fúteis bons pra comparar:

- iFood / delivery
- sorvete / açaí
- pizza
- lanche
- café de shopping
- unha / sobrancelha
- um Uber desnecessário
- uma compra por impulso na Shein/Shopee

#### Camada 3. Mini depoimento

Um depoimento curto de 1-2 linhas, entre aspas, com nome e contexto mínimo da pessoa.

Regras:

- Para produtos de NEGÓCIO: depoimento com resultado financeiro concreto. Ex: "No primeiro fim de semana eu vendi R$ 2.800 só em brunch. Antes eu não faturava isso na semana inteira." — Joana, dona da Café da Vila
- Para produtos EMOCIONAIS: depoimento com transformação sentida, algo pequeno mas poderoso. Ex: "No quinto dia, pela primeira vez em semanas, eu abri a janela. Parece pouco, mas pra mim foi tudo." — Márcia, 52 anos
- Para produtos de SAÚDE: depoimento com resultado físico palpável. Ex: "Em 14 dias perdi 3,2kg sem passar fome. Meu marido perguntou o que eu tava fazendo." — Renata, 34 anos
- Para produtos de ORGANIZAÇÃO: depoimento com economia ou controle recuperado. Ex: "No primeiro mês economizei R$ 800 só de coisas que eu comprava repetido sem saber." — Priscila, 29 anos

IMPORTANTE: avise o aluno que esse depoimento é um EXEMPLO. Ele DEVE trocar por um depoimento real de um cliente. Depoimento inventado na página é antiético e pode gerar problemas legais.

### Alerta. Comparações proibidas

NUNCA compare o preço do produto com:

**1. Serviços profissionais de saúde mental ou física.**

- "Custa menos que uma sessão de terapia"
- "Mais barato que uma consulta com psicólogo/médico/nutricionista"
- "Substitui meses de tratamento"
- "Melhor do que remédio"
- Qualquer frase que implique que o produto substitui acompanhamento profissional
- Isso pode gerar problemas legais com conselhos profissionais (CRP, CRM, CREFITO)

**2. Produtos ou serviços similares ao que o criador vende.**

- Se o produto é um guia de autoajuda, não fale mal de livros de autoajuda
- Se o produto é um curso, não fale mal de outros cursos
- Se o produto é uma planilha, não fale mal de planilhas
- Nunca depreciar a categoria do próprio produto

**3. Vícios ou substâncias.**

- Não compare com bebida alcoólica, cigarro, drogas
- Pode soar como julgamento moral e afastar o público

Comparações PERMITIDAS:

- Gastos fúteis do dia a dia (delivery, lanche, sorvete, café, compra por impulso)
- Retorno financeiro que o produto gera
- Resultado prático e tempo economizado
- Valorização de patrimônio (imóvel, negócio)

### Regras gerais

- Tom de copywriter comercial: direto, confiante.
- A lista é só nome + valor riscado. Zero explicação.
- A soma total entre 5x e 10x o preço real.
- A ancoragem sempre em 3 camadas: valor riscado, frase de retorno com gasto fútil + resultado real, mini depoimento.
- A frase de retorno primeiro compara com gasto fútil, depois contrasta com o resultado duradouro do produto.
- O depoimento é um exemplo. Sempre avisar o aluno pra trocar pelo real.
- NUNCA comparar com serviços profissionais de saúde.
- NUNCA falar mal de produto/serviço similar ao que o criador vende.
- NUNCA comparar com vícios ou substâncias.

### Layout HTML

Bloco de oferta final em destaque. Lista vertical de entregáveis com checkmarks ✓ e valores riscados (`<s>` ou `text-decoration: line-through`). Linha de soma riscada, seta visual ou divisor pra preço real grande. Preço real em tipografia gigante (3-4x maior que o resto). Frase de retorno em destaque abaixo. Mini depoimento em card separado abaixo da frase. CTA = Quadro adaptado logo abaixo do mini depoimento.

---

## SEÇÃO 14. FAQ

Você é um copywriter. Crie a seção de FAQ. O FAQ não é só pra tirar dúvida operacional. Ele é a última linha de defesa contra as objeções. Metade das perguntas resolve dúvidas práticas de acesso. A outra metade quebra objeções que a pessoa ainda tem na cabeça e que impedem ela de comprar.

### Passo 1. Contexto

1. Qual é o produto?
2. Qual é a promessa central?
3. Qual é a headline da página?

### Passo 2. Mapear objeções do nicho

Antes de escrever qualquer pergunta, analise o produto e o público (sem mostrar pro aluno). Pense: quais são as razões pelas quais alguém olha essa página, quer comprar, mas desiste no último segundo?

Mapeie internamente:

- Objeções de PERFIL: "isso funciona pra alguém como eu?" (iniciante, avançado, pouca estrutura, pouco dinheiro, idade, localização)
- Objeções de CAPACIDADE: "será que eu consigo fazer?" (tempo, habilidade, tecnologia, equipe)
- Objeções de CONFIANÇA: "será que funciona mesmo?" (já tentei outras coisas, parece bom demais)
- Objeções de CONTEXTO: "mas no meu caso é diferente porque..." (nicho específico, público diferente, situação particular)

### Passo 3. 12 perguntas e respostas

Crie no mínimo 12 perguntas e respostas divididas em duas categorias:

#### Categoria 1. Dúvidas sobre acesso (4 a 5 perguntas)

São as dúvidas práticas sobre como funciona a compra e o acesso.

Perguntas obrigatórias:

- Como eu acesso o produto depois que comprar?
- Recebo tudo de uma vez ou é liberado aos poucos?
- Tem garantia? Como funciona?
- Tem suporte? Como faço pra tirar dúvidas?
- Por quanto tempo eu tenho acesso?

Regras das respostas:

- Curtas e diretas, 2-3 linhas.
- Tom tranquilizador: "é simples, funciona assim..."
- Sem enrolação, sem juridiquês.

#### Categoria 2. Dúvidas sobre o produto (7 a 8 perguntas)

São as dúvidas que escondem objeções. A pessoa não sabe que é objeção, ela acha que é dúvida legítima. E é. Trate como dúvida, não como objeção.

Regras das respostas:

- NUNCA responda só "sim, funciona". Isso não convence ninguém.
- Toda resposta deve ter: a confirmação + o argumento lógico de por que funciona + um exemplo ou raciocínio que desfaz a dúvida.
- A resposta deve ser densa mas simples. 3-5 linhas.
- O tom é de alguém paciente que já ouviu essa pergunta mil vezes e tem a resposta na ponta da língua.
- Se possível, vire a objeção a favor: "na verdade, é exatamente pra quem tá nessa situação que esse produto foi criado".

### Regra crítica. Nunca excluir outro comprador

Ao responder uma dúvida sobre um perfil específico, NUNCA exclua outros perfis.

ERRADO: "Foi feito pra cafeteria pequena."
→ O dono de cafeteria média ou grande lê e pensa "então não é pra mim".

CERTO: "Funciona. As receitas usam equipamentos simples que a maioria das cafeterias já tem. E se você já tem uma operação maior, melhor ainda, porque a execução fica mais fácil. O método se adapta tanto pra quem tem 4 mesas quanto pra quem tem 40."
→ Respondeu o pequeno sem excluir o grande.

ERRADO: "Perfeito pra iniciantes."
→ O avançado lê e pensa "conteúdo básico demais".

CERTO: "Você não precisa de experiência nenhuma pra aplicar. E se já tem experiência, vai montar tudo ainda mais rápido."
→ Respondeu o iniciante sem excluir o avançado.

A regra: sempre que responder pra um perfil, inclua uma frase curta que acolhe o outro perfil também. Ninguém pode ler a resposta e se sentir excluído.

### Tipos de dúvida que devem aparecer (adapte ao nicho)

**Dúvida de perfil básico:**

- "Funciona pra quem tá começando do zero?"
- "Funciona pra quem nunca fez isso antes?"

**Dúvida de perfil avançado:**

- "Funciona pra quem já sabe bastante?"
- "Não vai ser básico demais?"

**Dúvida de estrutura/recurso:**

- "Funciona com pouca estrutura / pouco dinheiro / pouco tempo?"
- "Consigo fazer sozinho / com equipe pequena?"

**Dúvida de contexto específico:**

- "Funciona no meu nicho / na minha cidade / pro meu público?"
- "Funciona se eu já tentei outras coisas e não deu certo?"

**Dúvida de credibilidade:**

- "E se não funcionar pra mim?"
- "Como eu sei que isso funciona de verdade?"

### Passo 4. Título

Crie o título. Simples e direto.

Exemplos:

- "Ainda tem dúvida? Veja se a sua tá aqui"
- "Perguntas frequentes"
- "Tudo que você precisa saber antes de entrar"

### Passo 5. Resumo final

```
[Título]

Dúvidas sobre acesso

P: [pergunta 1]
R: [resposta]

P: [pergunta 2]
R: [resposta]

... (4-5 perguntas)

Dúvidas sobre o produto

P: [pergunta 1]
R: [resposta com argumento]

P: [pergunta 2]
R: [resposta com argumento]

... (7-8 perguntas, mínimo 12 no total)
```

Apresente e pergunte: "Quer adicionar alguma pergunta específica do seu público ou ajustar alguma resposta?"

### Regras gerais

- Tom paciente, direto e convincente.
- Mínimo 12 perguntas: 4-5 sobre acesso + 7-8 sobre o produto.
- Categorias se chamam "Dúvidas sobre acesso" e "Dúvidas sobre o produto". Nunca "operacionais" e "objeções".
- Respostas sobre acesso: 2-3 linhas, diretas.
- Respostas sobre o produto: 3-5 linhas, com confirmação + argumento lógico.
- NUNCA responda com só "sim, funciona". Sempre argumente por que.
- NUNCA exclua outro perfil de comprador ao responder pra um perfil específico. Sempre acolha todos.
- Quando possível, vire a objeção a favor.
- As perguntas devem soar como algo que uma pessoa real perguntaria.
- Se o produto tiver garantia, destaque: "se em X dias você não gostar, devolvemos 100%".
- NUNCA revelar o formato exato do produto. "É um PDF de 80 páginas" mata a curiosidade. Use "você recebe o material direto no seu e-mail".
- NUNCA criar objeção que não existia. Se a pessoa nunca pensou em algo, não introduza.
- A última pergunta sempre liga ao CTA. Ex: "E se eu não souber por onde começar?" + resposta + microação "É só apertar o botão abaixo e seguir o passo 1."

### Layout HTML

Acordeão padrão com pergunta em header clicável e resposta expandindo abaixo. Ícone de chevron rotaciona ao abrir. Separação visual entre as duas categorias ("Dúvidas sobre acesso" e "Dúvidas sobre o produto") com header de categoria em accent.

---

## Regras gerais da Categoria Padrão

- Escreva tudo em português brasileiro com acentuação correta.
- Tom direto, sem enrolação, sem palavras difíceis.
- Nunca usar travessão (—). Substituir por vírgula, ponto, dois pontos ou reescrever.
- Nunca usar estrutura "Não é X. É Y."
- Nunca usar pergunta no gancho/título principal.
- Promessa sem dado concreto é proibida. Adicionar número, prazo ou situação específica.
- "Mesmo que" e "sem precisar" são proibidos.
- Lero-lero genérico é proibido (palavras que soam bem mas não dizem nada).
- Copy sem tese é proibida (descreve sem argumentar por que o problema existe).
- Sigla ou nome de técnica sem explicação é proibido.
- Depoimento que só elogia sem resultado concreto é proibido.
- Venda só do Quadro sem Decorado é proibida.
- Números são sempre exemplos hipotéticos. Avisar pro aluno trocar pelos reais.
- Toda decisão de imagem ou peça visual passa pelo aluno (sem inventar mockup).

## Regras de Ouro herdadas

1. **Toda a página converge para o Quadro.** Todos os CTAs usam variações do Quadro. Conclusão de Quem É fecha no Quadro. CTA Final usa Quadro como headline. CTA flutuante mobile usa Quadro adaptado.

2. **Ancoragem + Acesso Vitalício + Suporte.** Em todos os pontos de preço: valor riscado (preço + R$200) acima do preço real, depois "Pagamento único. Acesso vitalício." (ou prazo). Suporte como card próprio ao lado da garantia OU como linha dentro do FAQ.

3. **Header sem logo placeholder gerado.** Se o aluno tem logo PNG/SVG real, usar a logo dentro de `<img>`. Se não tem, usar apenas o nome do produto em tipografia limpa (sans-serif, peso 700-800, sem ícone decorativo ao lado). Nunca quadrado colorido, círculo gradiente ou placeholder gráfico no header.
