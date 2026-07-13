# Storytelling com Dados (Cole Nussbaumer Knaflic)

> Baseado na edição brasileira "Storytelling com Dados: Um Guia sobre Visualização" (Alta Books, 2019; original de 2015). A autora foi gerente da equipe People Analytics do Google, onde criou o curso interno de visualização de dados que deu origem ao livro, e conduziu workshops para mais de 100 organizações nos Estados Unidos e Europa.

## Tese central

Aprendemos linguagem e matemática na escola, mas ninguém nos ensina a juntar as duas coisas: contar histórias com números. O resultado é um mundo cheio de gráficos ruins, apresentações confusas e relatórios que ninguém entende. A tese de Knaflic é que qualquer pessoa pode se comunicar de forma eficaz com dados aplicando seis lições: entender o contexto antes de tudo, escolher o visual adequado, eliminar a saturação (todo elemento na tela consome carga cognitiva do público), focalizar a atenção com atributos pré-atentivos, pensar como um designer e, por fim, contar uma história com começo, meio e fim. A ferramenta nunca conhece a história que está nos seus dados; quem dá vida a ela é o comunicador. O objetivo é sair de "simplesmente mostrar dados" para "contar uma história com dados", porque histórias engajam emocionalmente e ficam na memória de um jeito que fatos soltos jamais conseguem.

## Conceitos e frameworks

### Lição 1: A importância do contexto

Antes de abrir qualquer ferramenta, distinga **análise exploratória** de **análise explanatória**. Exploratória é abrir 100 ostras para achar 2 pérolas; explanatória é mostrar ao público só as 2 pérolas. O erro mais comum é despejar as 100 ostras na frente do público como prova de esforço.

Depois responda três perguntas, nesta ordem:

1. **Quem** é o público? Quanto mais específico, melhor. Evite públicos vagos como "interessados internos e externos". Identifique o tomador de decisão.
2. **O quê** você precisa que ele saiba ou faça? Se você não consegue articular a ação desejada, questione se a comunicação precisa existir. Quem analisa os dados é o especialista e deve ter postura confiante para recomendar, não apenas apresentar.
3. **Como** os dados disponíveis sustentam a tese? Os dados são a evidência da história. Não esconda dados contrários: um público perspicaz acha os furos e a credibilidade vai embora.

Ferramentas de contexto:
- **História de 3 minutos**: se você tivesse só 3 minutos, o que diria? Elimina a dependência de slides.
- **Grande Ideia** (conceito de Nancy Duarte): reduzir tudo a UMA frase completa que articula o ponto de vista único e o que está em jogo.
- **Storyboard**: planejar a estrutura da comunicação em post-its ou papel, nunca direto no software de apresentação (o que criamos no computador gera apego e resistência a cortar).
- **Mecanismo**: numa apresentação ao vivo você controla o ritmo e precisa de menos detalhe no slide; num documento enviado o leitor controla tudo e o material precisa se explicar sozinho. Tentar servir os dois com o mesmo arquivo gera o "slidemento", que não atende bem nenhum dos dois.

### Lição 2: A escolha de um visual eficaz

Uma dúzia de tipos de gráfico resolve quase tudo:

- **Texto simples**: quando há só 1 ou 2 números, mostre os números grandes com poucas palavras. Colocar dois números num gráfico enfraquece a mensagem (exemplo do Pew Research: 20% vs 41% de mães que ficam em casa dizia mais como frase do que como gráfico).
- **Tabela**: interage com o sistema verbal, o público lê. Boa para públicos mistos que buscam cada um a sua linha. Ruim em apresentação ao vivo (o público lê e para de ouvir). Bordas devem ser leves ou inexistentes; o dado é o protagonista.
- **Mapa de calor**: tabela com saturação de cor para guiar o olho ao maior e ao menor valor.
- **Gráfico de dispersão**: relação entre duas variáveis.
- **Gráfico de linhas**: dados contínuos no tempo. Intervalos do eixo precisam ser consistentes. Pode ter linha de base diferente de zero, com cautela.
- **Gráfico de inclinação (slopegraph)**: dois períodos comparados, mostra aumento e queda por categoria de forma intuitiva pela inclinação.
- **Barras (verticais, empilhadas, horizontais)**: melhor escolha para dados categóricos. Regra inegociável: barra sempre com linha de base ZERO, porque o olho compara os extremos (exemplo da Fox News: eixo começando em 34 fez um aumento de imposto de 13% parecer de 460%). Barras horizontais são as mais fáceis de ler, especialmente com nomes de categoria longos. Ordene as categorias com lógica (maior para menor, ou ordem natural).
- **Cascata (waterfall)**: ponto de partida, adições, subtrações e resultado (exemplo: movimentação de headcount no ano).
- **Área quadrada**: só quando as magnitudes são muito diferentes entre si.

**Proibições**: gráfico de pizza (o olho humano não avalia ângulos e áreas; no exemplo do livro, o segmento de 31% parecia maior que o de 35%), gráfico de rosca (comparar comprimentos de arco é ainda pior), 3D (distorce a percepção dos valores, nunca use) e eixo y secundário (obriga o leitor a decifrar qual série pertence a qual eixo; separe em dois gráficos ou legende direto).

### Lição 3: A saturação é sua inimiga

Cada elemento na página consome **carga cognitiva** do público. Saturação são os elementos que ocupam espaço sem acrescentar entendimento, e ela faz o material parecer mais complicado do que é, a ponto de o público desistir. É a versão prática da relação data-ink de Tufte e da relação sinal-ruído de Duarte.

**Princípios da Gestalt** aplicados a gráficos:
1. **Proximidade**: objetos próximos parecem grupo (use o espaçamento para criar linhas ou colunas sem bordas).
2. **Similaridade**: mesma cor ou forma indica relação (legenda com a mesma cor da linha dispensa a legenda separada).
3. **Acercamento (enclosure)**: um sombreado leve delimita um grupo (área sombreada separando previsão de dado real).
4. **Fechamento**: o olho completa formas; bordas e fundos de gráfico são desnecessários.
5. **Continuidade**: o olho busca o caminho mais suave; dá para remover a linha do eixo y e o gráfico continua legível.
6. **Conexão**: objetos ligados por linha são percebidos como grupo (é por isso que gráfico de linhas funciona).

Regras complementares: alinhamento à esquerda em vez de texto centralizado (linhas limpas), evitar elementos diagonais (texto a 45 graus é lido 52% mais devagar; a 90 graus, 205% mais devagar), não ter medo de espaço em branco (ele é a pausa do discurso visual) e usar contraste estrategicamente (a analogia de Colin Ware: é fácil achar um falcão num céu de pombos; quanto mais variedade, menos qualquer coisa se destaca).

O passo a passo de dessaturação demonstrado no caso da equipe de TI: remover borda do gráfico, remover linhas de grade, remover marcadores de dados, limpar as legendas de eixo (fora zeros à direita), legendar as séries diretamente e usar cores consistentes entre legenda e dado.

### Lição 4: Focalize a atenção do público

Existem três memórias: icônica (fração de segundo, pré-consciente), de curto prazo (guarda cerca de 4 blocos de informação visual) e de longo prazo (onde a história precisa chegar, via repetição e combinação de memória visual e verbal).

Os **atributos pré-atentivos** (tamanho, cor, intensidade, posição, orientação, forma, comprimento, largura, movimento) são processados pela memória icônica antes do pensamento consciente. O exercício dos números 3 num bloco de texto prova: sem pista visual, você varre tudo; com os 3 destacados em cor, você os vê instantaneamente. Usados com estratégia, eles fazem o público ver o que você quer antes mesmo de saber que está vendo. Estudos mostram que temos de 3 a 8 segundos de atenção inicial do público.

Regras de ouro:
- **Tamanho**: tamanho relativo sinaliza importância relativa. Coisas igualmente importantes, tamanhos iguais.
- **Cor**: a ferramenta mais poderosa quando usada com moderação. O padrão da autora: tudo em tons de cinza e UMA cor de destaque (azul, que funciona para daltônicos e imprime bem em preto e branco). Cinza como base, não preto, para sobrar contraste. Usar cor de forma consistente ao longo da apresentação; mudança de cor sinaliza mudança de assunto. Cerca de 8% dos homens são daltônicos: evite vermelho contra verde, prefira azul para positivo e laranja para negativo. Cor carrega tom (relatório clínico pede paleta sóbria) e conotações culturais.
- **Posição**: sem outras pistas, o público lê em zigue-zague em forma de Z a partir do canto superior esquerdo. O topo da página é área nobre: o mais importante vai ali.

Teste prático: "para onde os olhos são atraídos?" Crie o visual, desvie o olhar, olhe de novo e observe onde o olho pousa primeiro. Melhor ainda: peça a um colega para narrar o que vê.

### Lição 5: Pense como um designer

A forma segue a função: primeiro defina o que o público deve fazer com o dado (função), depois crie o visual (forma).

- **Affordances**: como a maçaneta que pede para ser girada e o utensílio OXO que só pode ser pegado do jeito certo, o visual deve indicar como ser usado. Três táticas: realçar o importante (no máximo 10% do visual realçado; negrito é melhor que itálico e sublinhado; caixa alta funciona em palavras curtas; nunca pisca-pisca), eliminar distrações (a frase de Saint-Exupéry: a perfeição é atingida quando não há mais nada a tirar; se remover não muda nada, remova) e criar hierarquia visual clara (supercategorias em tabelas, primeiro plano e segundo plano).
- **Acessibilidade**: o design deve ser compreensível por não especialistas. Quando alguém não entende um gráfico, a culpa é do design, não do leitor (exemplo do mapa do metrô de Londres de Harry Beck). Estudo de Song e Schwarz (2008): instruções em fonte difícil de ler fizeram as pessoas estimarem a tarefa como mais demorada e ficarem menos dispostas a executá-la. Se parece complicado, o público acredita que É complicado. Texto é seu amigo: todo gráfico precisa de título, todo eixo precisa de título, e a conclusão desejada deve estar escrita em palavras, porque duas pessoas olhando o mesmo gráfico chegam a conclusões diferentes. Use título de ação no slide ("Despesa estimada de 2015 está acima do orçamento"), não título descritivo ("Orçamento 2015").
- **Estética**: designs bonitos são percebidos como mais fáceis de usar, geram mais tolerância a problemas (caso do sabão Method que vazava e mesmo assim vendia) e sinalizam respeito pelo público. Três alavancas: cor inteligente, alinhamento e espaço em branco.
- **Aceitação**: pessoas resistem à mudança de formato. Estratégias: anunciar as vantagens do novo formato, mostrar antes e depois lado a lado, oferecer opções e colher opiniões, conquistar um membro influente do público.

### Lição 6: Conte uma história

- **Estrutura de 3 atos de Aristóteles**: preparação (contexto, personagem, o que mudou), conflito (o problema e suas consequências) e solução (clímax e chamada para ação). Conflito e tensão dramática são obrigatórios: uma história em que está tudo bem não move ninguém. Nancy Duarte chama essa tensão de "o conflito entre o que é e o que poderia ser".
- **Robert McKee**: há dois modos de persuadir. A retórica convencional (slides com fatos e marcadores) é um processo intelectual em que o público debate mentalmente com você. A história une ideia e emoção e inspira ação. O livro mostra a Chapeuzinho Vermelho reduzida a bullets de PowerPoint para provar como os fatos sozinhos matam o interesse.
- **Kurt Vonnegut**: encontre um assunto com que se importe, não divague, simplifique, tenha coragem de cortar, pareça você mesmo, diga o que pretende dizer, tenha dó dos leitores.
- **Começo, meio e fim aplicados a negócios**: o começo estabelece o problema do público (para ele apostar na solução), o meio desenvolve o que poderia ser com dados como evidência, e o fim termina com chamada para ação explícita.
- **Fluxo narrativo**: contar em ordem cronológica (bom para estabelecer credibilidade e mostrar processo) ou começar pelo fim (a recomendação primeiro; bom para públicos ocupados que só querem o "e daí").
- **Poder da repetição e Bing, Bang, Bongo**: diga o que vai contar, conte, resuma o que contou. A repetição transfere a mensagem da memória de curto prazo para a de longo prazo (é por isso que todo mundo lembra da Chapeuzinho Vermelho).
- **Táticas de verificação**: lógica horizontal (ler só os títulos dos slides deve contar a história completa), lógica vertical (tudo dentro de um slide se reforça mutuamente), storyboard inverso (folhear o deck pronto anotando o ponto de cada página e conferir se forma a história) e nova perspectiva (mostrar a alguém sem contexto e pedir que narre o que entende).
- O protagonista de toda história é sempre o público, nunca o apresentador.

### Estudos de caso (capítulo 9)

1. **Fundo escuro**: fundo branco é o padrão recomendado; em fundo preto a lógica inverte (branco destaca, cinza recua) e cores proibidas no branco, como amarelo, passam a funcionar.
2. **Animação**: em apresentação ao vivo, revelar o gráfico por partes (começando pelos eixos vazios) controla a atenção e cria expectativa; a versão distribuída recebe todas as anotações num único gráfico final.
3. **Lógica na ordem**: os mesmos dados de pesquisa de satisfação contam três histórias diferentes (satisfação, insatisfação, recursos não usados) só mudando ordem, cor e texto; mantenha a mesma ordenação de categorias ao contar múltiplas histórias para não recarregar o público.
4. **Gráfico espaguete** (muitas linhas sobrepostas): enfatizar uma linha por vez, separar espacialmente (pequenos múltiplos) ou combinar as duas técnicas.
5. **Alternativas à pizza**: mostrar os números diretamente, barras simples, barras horizontais empilhadas a 100% (preserva a noção de parte do todo) ou gráfico de inclinação.

### Dicas finais (capítulo 10)

Conheça bem UMA ferramenta (todos os exemplos do livro foram feitos no Excel); itere e busque opiniões (a "estratégia do optometrista": versão A ou versão B, uma mudança por vez); reserve tempo para a etapa de comunicação, que é a única parte do processo analítico que o público vê; construa uma biblioteca de bons exemplos para imitar; desenvolva um estilo próprio. Para times: treinar todo mundo no básico, investir em 1 ou 2 especialistas internos e terceirizar pontualmente, de preferência combinando as três coisas.

## Dados, números e casos citados

- A memória de curto prazo retém cerca de 4 blocos de informação visual por vez.
- Temos de 3 a 8 segundos até o público decidir se continua olhando ou desvia a atenção.
- Texto inclinado a 45 graus é lido em média 52% mais devagar; a 90 graus, 205% mais devagar (Wigdor e Balakrishnan, 2005).
- Aproximadamente 8% dos homens e cerca de 4% das mulheres têm daltonismo.
- Realce no máximo 10% do design visual (Lidwell, Holden e Butler, Universal Principles of Design).
- Caso Fox News: eixo de barras começando em 34 em vez de zero transformou visualmente um aumento de imposto de 13% em 460%.
- Caso Pew Research (mães que ficam em casa, 20% em 2012 vs 41% em 1970): dois números dispensam gráfico.
- Caso Project Oxygen do Google: pesquisa sobre o que torna um gerente excelente, comunicada para públicos que iam de engenheiros céticos a executivos, citada no New York Times e em estudo de caso da Harvard Business Review.
- Estudo Song e Schwarz (2008): fonte difícil de ler faz a tarefa parecer mais longa e reduz a disposição de executá-la.
- Caso do curso de verão de ciências: 40% dos alunos achavam ciências apenas "OK" antes; depois do programa, quase 70% expressaram interesse. Usado do começo ao fim do livro para ilustrar Grande Ideia, storyboard e alternativas à pizza.
- Referências de mestres: Edward Tufte (data-ink), Nancy Duarte (Ressonância, Grande Ideia), Robert McKee (Story), Kurt Vonnegut, Stephen Few (Show Me the Numbers), Colin Ware (falcão entre pombos), Cliff Atkinson (Beyond Bullet Points), David McCandless (anotações e cores por cultura).

## Aplicações práticas para um CEO de negócio digital de infoprodutos e mentorias

1. **Todo relatório de tráfego deve começar pela Grande Ideia.** Antes de mostrar CPM, CTR e ROAS ao time ou ao mentorado, escreva em UMA frase o que os números dizem e o que fazer ("o criativo X saturou; realocar 40% do orçamento para o Y esta semana"). Dado sem chamada para ação vira "ah, interessante" e nada acontece.

2. **Dashboards e relatórios de campanha: cinza mais uma cor.** Aplique o padrão da autora nos dashboards de Instagram, TikTok e Meta Ads: tudo em cinza, uma única cor de destaque no número que exige decisão. Fuja de pizza, rosca, 3D e arco-íris de categorias. Barra horizontal ordenada resolve quase toda comparação de criativos, públicos e campanhas.

3. **Use texto simples para os números de impacto.** Na página de vendas, no pitch de webinário e no relatório para o cliente, um número grande com uma frase curta ("70% dos alunos concluíram em 30 dias") vale mais que qualquer gráfico. É o mesmo princípio da prova concreta do Light Copy.

4. **Estruture apresentações de vendas e webinários em 3 atos.** Preparação (o mundo do lead e o que mudou), conflito (o problema e o custo de não agir, com dados como evidência) e resolução (o método e a chamada para ação). Tensão entre "o que é" e "o que poderia ser" é exatamente o motor de uma boa VSL.

5. **Lógica horizontal nos decks e nas páginas.** Se alguém ler apenas as headlines das seções da sua página de vendas ou os títulos dos slides do webinário, a história completa precisa estar contada. Títulos de ação, nunca títulos descritivos.

6. **Apresentação ao vivo é diferente de material enviado.** O slide do webinário ao vivo é limpo, revelado por partes, com você narrando; o PDF enviado para o lead ou o relatório mensal do mentorado precisa das anotações completas porque se explica sozinho. Não use o mesmo arquivo para os dois papéis.

7. **Explique o gráfico antes do gráfico.** Ao apresentar dados para mentorados leigos, monte primeiro os eixos vazios ("aqui é o faturamento, aqui são os meses") e só depois revele os dados. Isso controla a atenção e evita que a pessoa se perca ou pule para conclusões.

8. **Peça o teste da nova perspectiva.** Antes de enviar qualquer relatório ou página, mostre a alguém sem contexto e peça para narrar o que entende e para onde o olho vai primeiro. É o QA mais barato que existe para comunicação.

## Frases e ideias marcantes (paráfrases)

- Não nos ensinam a contar histórias com números; qualquer um faz um gráfico no Excel, e é justamente por isso que existem tantos gráficos ruins.
- Há uma história nos seus dados, mas a ferramenta não sabe qual é; quem dá vida a ela é você.
- Mostrar a análise inteira é obrigar o público a reabrir as 100 ostras; entregue só as pérolas.
- Se você não consegue dizer em uma frase o que quer que o público saiba ou faça, não está pronto para comunicar.
- Cada elemento na página cobra um pedágio de energia mental do público; a saturação é sua inimiga.
- Quanto mais coisas você destaca, menos qualquer coisa se destaca (o falcão no céu de pombos).
- Nunca use 3D. Gráficos de barra sempre começam no zero. Pizza é ruim; rosca é pior.
- Se parece difícil de ler, as pessoas concluem que é difícil de fazer, e desistem.
- Atributos pré-atentivos fazem o público ver o que você quer antes de saber que está vendo.
- A perfeição do design chega quando não há mais nada a tirar, não quando não há mais nada a acrescentar.
- Fatos convencem o intelecto, mas as pessoas não agem só por razão; a história une ideia e emoção.
- Uma apresentação boa supera slides medíocres, e uma narrativa forte supera visuais ruins, mas o ideal é visual eficaz mais narrativa poderosa.
- Diga o que vai contar, conte, e resuma o que contou (Bing, Bang, Bongo).
- O personagem principal de toda história de dados é o público, nunca o apresentador.
- A etapa de comunicação é a única parte do processo analítico que o público vê; reserve tempo para ela.
