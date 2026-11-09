# Finanças Empresariais, apostila do MBA em Gestão Empresarial da FGV (José Carlos Abreu e Newton Ricardo Rezende Moraes)

## Tese central

Toda decisão de negócio é, no fundo, uma decisão financeira, e o segredo do sucesso em administração financeira é aumentar valor. A apostila ensina que qualquer ativo (uma empresa, um projeto, uma máquina, um imóvel, uma ação) deve ser representado como uma sequência de fluxos de caixa futuros e avaliado pelo valor presente desses fluxos, descontados por uma taxa que remunere o investidor pelo tempo de espera e pelo risco assumido. O administrador financeiro responde a duas perguntas fundamentais: em que investir (decisão de investimento) e como levantar o dinheiro necessário (decisão de financiamento). Uma boa decisão de investimento é comprar um ativo que vale mais do que custa, e todos os critérios do curso (VPL, TIR, payback, CAPM, CMPC) existem para operacionalizar essa ideia simples.

## Conceitos e frameworks

### 1. Representação financeira de ativos (a linguagem do administrador)

O ponto de partida do material é uma mudança de linguagem. O livro usa um exemplo memorável: peça a três profissionais que representem a mesma casa. O arquiteto desenha a planta, o corretor escreve o anúncio de classificados ("linda casa, vista indevassável"), e o administrador financeiro pergunta quanto custou, quanto rende de aluguel, quanto paga de imposto. Para o financista, todo ativo é representado assim:

- t=0: investimento inicial (saída de caixa, negativo)
- t=1, t=2, ... t=T: fluxos de caixa livres após taxas e impostos (entradas)

O fluxo de caixa que interessa para decisão é o operacional, incremental e livre após impostos, obtido de forma simplificada como: faturamento, menos custos variáveis, menos custos fixos, igual a lucro bruto operacional, menos impostos, igual a fluxo de caixa operacional. Quatro características do fluxo importam para avaliar: valor em dinheiro, timing (datas), risco e sinal (entrada ou saída).

Exemplo do livro: imóvel comprado por $100.000, alugado por $1.000 mensais durante 12 meses e vendido ao final por $120.000. A representação é a linha do tempo com -100.000 em t=0, +1.000 de t=1 a t=12 e +120.000 em t=12.

### 2. Dicionário de fundamentos (o jargão)

O material insiste que grande parte dos erros vem do desconhecimento do vocabulário. Conceitos-chave:

- **Fluxo de caixa**: entradas e saídas de dinheiro ao longo do tempo. É financeiro, não contábil.
- **Investimento**: dispêndio corrente de caixa visando retornos futuros.
- **Perpetuidade**: fluxos periódicos, com taxa de crescimento constante (pode ser zero), que duram até o infinito.
- **Ativo**: qualquer bem, tangível ou intangível, que proporcione fluxo de caixa ao dono.
- **Arbitragem**: operação com retorno positivo, risco zero e investimento nulo (ex: ouro cotado a $320 em Nova York e $310 em Hong Kong no mesmo instante). Em mercados eficientes, oportunidades de arbitragem praticamente não existem porque os primeiros a perceber corrigem os preços.
- **Risco**: é função da incerteza, não sinônimo. Risco é a possibilidade de o resultado sair diferente do esperado, para mais ou para menos. Se há certeza absoluta, não há risco.
- **Fontes de risco**: risco de negócio (operação, mercado), financeiro (capacidade de pagar dívidas), de liquidez, cambial e político. O livro destaca o risco político como o maior de todos, justamente por ser aquele sobre o qual a empresa pouco ou nada pode fazer.

Os quatro objetivos de finanças: onde investir, quanto investir, como financiar o investimento e como distribuir os resultados.

### 3. Mercado eficiente e suas consequências

Mercado eficiente é aquele em que os preços refletem toda a informação disponível. Há três formas: fraca (preços refletem a informação dos preços passados), semiforte (mais toda informação pública) e forte (mais toda análise fundamentalista possível). Consequências práticas listadas no material: mercados não têm memória (o histórico de preços não prevê o futuro), confie nos preços de mercado, não há ilusão monetária (métodos contábeis e splits não mudam valor), diversificação que o investidor pode fazer sozinho não agrega valor, e os preços refletem expectativas futuras. Daí vem a crítica ao ditado "compre na baixa, venda na alta": sem informação que o mercado não tenha, não existe VPL positivo em comprar ações cotadas de forma justa.

### 4. Valor presente e perpetuidade (a fórmula fundamental)

- Valor presente de um fluxo: VP = FC / (1 + K) elevado a t.
- Valor presente de vários fluxos: soma dos fluxos descontados.
- Valor presente de uma perpetuidade com crescimento g: VP = FC1 / (K - g).

A taxa K sempre embute prêmio pelo tempo (taxa livre de risco, como poupança ou títulos do tesouro) mais prêmio pelo risco. O material demonstra a fórmula da perpetuidade algebricamente e a constrói na intuição com uma sequência de exercícios: o valor presente de 10 pagamentos de $100 a 10% ao mês é $614; de 100 pagamentos, $999,93; de 500 pagamentos, $1.000,00. Conclusão do aluno: quando o número de fluxos idênticos tende ao infinito, VP = FC / K. Verificação: 100 / 0,1 = 1.000.

### 5. VPL, Valor Presente Líquido (o critério rei)

VPL = valor presente dos fluxos futuros, menos o custo do investimento hoje. Regra de decisão: aceitar se VPL > 0 (a empresa troca caixa por um ativo que vale mais), indiferente se VPL = 0, rejeitar se VPL < 0 (o projeto paga menos que o custo do capital que o financia). Exemplo do livro: projeto XINGU custa $2.000.000 e tem valor presente de $2.800.000, logo VPL de $800.000, investimento aprovado. O VPL tem uma propriedade operacional valiosa: é aditivo, VPL(A+B) = VPL(A) + VPL(B), o que permite analisar projetos separadamente.

### 6. CAPM (Capital Asset Pricing Model)

Modelo desenvolvido por Sharpe (1964) e Lintner (1965) para definir a taxa de retorno adequada ao risco de um ativo:

Ki = RF + Beta_i x (ERm - RF)

Onde RF é a taxa livre de risco, ERm é o retorno esperado do mercado como um todo e Beta é o risco relativo do ativo em relação ao mercado. Exemplo do livro: com ERm de 14%, RF de 8% e Beta de 0,7, a taxa adequada é 12,2%.

### 7. Beta (a medida de risco relativo)

Beta mede a sensibilidade de um ativo aos movimentos do mercado. O livro traz um exemplo empírico ótimo: você e 20 amigos saem para beber; no carnaval o grupo consome 105 chopes, média de 5 por pessoa. Quem sempre bebe a média do grupo tem beta 1. Quem bebe metade tem beta 0,5. A amiga que bebe o dobro tem beta 2. Traduzindo para o mercado: ação com beta 1 sobe 10% quando o mercado sobe 10%; beta 0,5 sobe 5%; beta 2 sobe 20%. Tecnicamente, o beta é a inclinação da reta de regressão entre os retornos diários do ativo e os retornos do mercado. O risco absoluto, por outro lado, é medido pelo desvio padrão dos resultados. O investidor típico é avesso ao risco: entre dois ativos com o mesmo valor esperado, prefere o de menor dispersão, e por isso cobra retorno adicional para aceitar risco adicional (é por isso que bancos cobram juros menores para financiar imóveis do que automóveis).

### 8. CMPC / WACC (Custo Médio Ponderado de Capital)

Uma empresa só tem duas fontes de capital: capital de terceiros (credores, que recebem juros, taxa Kd, menos arriscado porque tem garantias e pode executar a empresa) e capital próprio (sócios, que recebem dividendos, taxa Ks, mais arriscado porque não tem garantia nenhuma). Como o acionista corre mais risco, Ks é sempre maior que Kd. A fórmula:

CMPC = Kd x (1 - IR) x (Dívida / Capital Total) + Ks x (Capital Próprio / Capital Total)

O fator (1 - IR) captura o benefício fiscal: como os juros são dedutíveis do imposto de renda, uma dívida a 10% com IR de 35% custa efetivamente 6,5%. O material demonstra isso com um exemplo completo comparando o lucro líquido com e sem o abatimento dos juros. Ponto teórico importante: mudar a estrutura de capital (proporção dívida/capital próprio) não muda o risco operacional da empresa nem seu custo total de capital em condições ideais sem imposto; quando a dívida cai, o risco dos acionistas cai e eles aceitam retorno menor, e o CMPC permanece o mesmo.

### 9. Avaliação de ações e política de reinvestimento

Preço justo da ação: Po = D1 / (Ks - g), onde D1 é o dividendo do próximo período, Ks vem do CAPM e g é a taxa de crescimento, dada por g = r x b (taxa de retorno dos reinvestimentos vezes taxa de reinvestimento dos lucros). Exemplo central da firma EXCEL: com lucro de $110 e 100 ações, sem reinvestimento a ação vale $11,00 (dividendo de 1,10 dividido por 0,10). Reinvestindo 40% do lucro à mesma taxa Ks de 10%, o dividendo cai para $0,66 mas g sobe para 4%, e a ação vale os mesmos $11,00. Moral: reinvestir só cria valor quando o retorno do reinvestimento supera o custo de capital. No exercício da Cia MACAPÁ, quando a firma passa a reinvestir numa divisão que rende 30% ao ano (acima do custo de capital de 25%), o valor da ação sobe de $140,00 para $161,54.

O livro também distingue Valor de Cotação: cotação é o preço pelo qual o ativo é efetivamente negociado (percepção, humor de mercado); valor é o preço de equilíbrio sem oportunidades de arbitragem. E cita os quatro mitos de Damodaran sobre avaliação: avaliação não é busca objetiva pelo valor real, não fornece valor exato, mais quantitativo não significa melhor, e o modelo não é inválido só porque o preço de mercado diverge dele.

### 10. Valor da firma versus valor das ações

Conciliação fundamental, sempre em cenário de perpetuidade:
- Valor da firma (V) = Valor das ações (S) + Valor das dívidas (D)
- Valor das dívidas = Juros / Kd
- Valor das ações = Dividendos / (Ks - g)
- Valor da firma = FCO / CMPC, onde FCO = LAJIR x (1 - IR)

O exemplo do imóvel de $200.000 comprado com $85.000 de financiamento e $115.000 de entrada deixa claro: o valor do ativo independe de como ele é financiado; o lado esquerdo do balanço mostra a firma, o lado direito mostra como ela é financiada. Regra de ouro do material: nunca desconte o fluxo do acionista pela taxa do credor, nem vice-versa. Cada fluxo tem sua taxa.

### 11. Os sete critérios de classificação de investimentos

1. **Taxa média de retorno contábil** (VF / VP): fácil de calcular, mas ignora o valor do dinheiro no tempo. Veredito do livro: muito inconsistente, não use.
2. **Payback simples**: tempo para recuperar o investimento a valor de face. Usa fluxo de caixa e serve como medida bruta de risco, mas ignora o valor do dinheiro no tempo, ignora fluxos após o payback e o critério de corte é arbitrário.
3. **Payback descontado**: igual ao simples, mas desconta os fluxos antes. Melhor, mas ainda ignora o que vem depois do ponto de recuperação.
4. **VPL**: o critério de referência, mede benefício menos custo em dinheiro de hoje, aceita se maior que zero e ranqueia projetos.
5. **TIR (Taxa Interna de Retorno)**: a taxa de desconto que zera o VPL. Aceitar se TIR > K. Cuidado: pode haver múltiplas TIRs (uma por mudança de sinal na sequência de fluxos).
6. **ILL (Índice de Lucratividade Líquida)**: VP das entradas dividido pelo VP das saídas, aceitar se maior que 1. Medida relativa, boa quando o capital é limitado, mas ILL(A) > ILL(B) não garante que A seja melhor.
7. **Break Even (ponto de equilíbrio)**: em três medidas, operacional (caixa zero), contábil (lucro zero) e econômico (VPL zero). O livro enfatiza que só o break even econômico interessa em finanças, porque é o único equivalente à análise por VPL.

O material fecha com uma tabela comparativa de 4 projetos em que cada critério aponta um vencedor diferente (TIR elege B, VPL elege C, payback elege A, ILL elege D), para provar que nenhum critério isolado decide: é preciso olhar disponibilidade de capital, quantidade de projetos e taxa de retorno de alternativas de risco semelhante.

## Dados, números e casos citados

- Caso da montadora asiática no centro-sul do Brasil: investimento de $150 milhões, carro vendido a $3.800, custo variável de $3.000, custos fixos de $32 milhões ao ano, IR de 40%, 10 anos de operação. VPL de $46,6 milhões. Os três pontos de equilíbrio: operacional 40.000 carros/ano, contábil 58.750 carros/ano, econômico 82.808 carros/ano. A distância entre 40 mil e 82,8 mil carros mostra o quanto o "empatar no caixa" engana: a empresa pode estar no azul contábil e destruindo valor econômico.
- Caso DEEP SPACE COMPANY: dividendos de $114.000 a Ks de 12% dão ações de $950.000; juros de $90.000 a Kd de 8% dão dívida de $1.125.000; valor da firma de $2.075.000, conferido pelo desconto do FCO de $204.000 pelo CMPC de 9,83%.
- Caso QUIKOISA (com IR de 30%): LAJIR de $500, equity de $2.450, dívida de $1.000, valor total $3.450, CMPC de 10,145%, com checagem cruzada pelas três fórmulas.
- Retornos históricos: poupança rende cerca de 5% a 6% ao ano (EUA e Brasil); o mercado de ações oferece retornos consistentemente superiores à renda fixa desde 1920.
- Firma EXCEL: demonstração numérica de que reinvestir lucros à taxa igual ao custo de capital não altera o valor da ação ($11,00 nos dois cenários).
- Bibliografia de referência citada: Brealey e Myers (a "bíblia" de Corporate Finance), Ross, Gitman, Damodaran, Copeland (Valuation).

## Aplicações práticas para um CEO de negócio digital de infoprodutos e mentorias

1. **Trate cada funil como um ativo com fluxo de caixa.** Um funil perpétuo de low ticket é exatamente uma perpetuidade: investimento inicial (produção de criativos, páginas, tráfego de teste) e fluxo mensal recorrente. O valor do funil é FC mensal / (K - g). Isso permite decidir racionalmente quanto vale a pena investir para construir ou consertar um funil.
2. **Use VPL, não faturamento, para escolher projetos.** Entre lançar um produto novo, escalar o funil atual ou gravar um curso high ticket, a comparação correta é o valor presente dos fluxos de cada opção menos o custo (dinheiro e tempo) de cada uma. O material prova que critérios diferentes elegem vencedores diferentes; o VPL é o árbitro final.
3. **Conheça seus três pontos de equilíbrio no tráfego pago.** O break even operacional (ROAS que paga o anúncio) é o mais fraco. O contábil inclui custos fixos, equipe e ferramentas. O econômico inclui o custo do seu capital e do seu tempo. Muita operação de tráfego "no azul" está abaixo do break even econômico, exatamente como a montadora do caso que precisava vender o dobro de carros para de fato criar valor.
4. **Reinvestir só cria valor se o retorno supera o custo de capital.** A lição da firma EXCEL vale para reinvestir lucro em mais tráfego, mais equipe ou mais produto: se o reinvestimento rende o mesmo que uma aplicação financeira, ele não aumenta o valor do negócio, só muda a data em que o dinheiro chega. Escalar por escalar não é estratégia.
5. **Precifique o risco das suas apostas.** Um lançamento tem beta alto (resultado muito sensível ao humor do mercado); um perpétuo validado tem beta baixo. Exija margem (taxa de desconto) maior das apostas arriscadas antes de aprovar o orçamento delas, como o CAPM manda.
6. **Ao avaliar seu negócio para venda ou sociedade, separe valor da firma e valor do dono.** Valor da empresa = fluxo de caixa operacional / custo de capital. Se há dívidas ou antecipações de recebíveis, o valor do que é seu é o total menos a dívida. E lembre dos mitos de Damodaran: nenhuma avaliação fornece valor exato, e a cotação que o mercado (ou um comprador) oferece não é necessariamente o valor justo.
7. **Payback como filtro de caixa, VPL como decisão.** Para quem vive de capital de giro apertado (tráfego pago antecipa custo e o checkout paga em D+15 ou D+30), o payback descontado é um filtro legítimo de sobrevivência, mas a decisão final de qual campanha manter deve ser por VPL.

## Frases e ideias marcantes

- O segredo do sucesso em administração financeira é aumentar valor: simples de dizer, difícil de fazer, e é justamente por isso que vale a pena estudar finanças.
- Uma boa decisão de investimento é comprar um ativo que vale mais do que custa.
- Risco não tem a ver com dar certo ou dar errado; tem a ver com a probabilidade de dar diferente do esperado.
- O beta não é trazido pela cegonha: ele nasce da regressão entre os retornos do ativo e os retornos do mercado.
- O valor de um ativo independe de como ele é financiado; o lado esquerdo do balanço mostra a firma, o lado direito mostra quem paga a conta.
- Nunca desconte o fluxo do acionista pela taxa do credor, nem o contrário: cada fluxo de caixa tem a taxa do seu próprio risco.
- Não há geração perpétua de lucros anormais: vantagens competitivas se dissipam, e a avaliação deve assumir isso.
- Em finanças corporativas, o único ponto de equilíbrio que interessa é o econômico, porque é o único equivalente ao VPL igual a zero.
- Reduzir incerteza custa informação; administrar incerteza é aceitar o desconhecido como fato da vida e se adaptar.
