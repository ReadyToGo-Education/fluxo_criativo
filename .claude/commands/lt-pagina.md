---
name: workshop-marketing:lt-pagina
description: Criar copies e páginas de vendas low ticket com as 4 categorias da metodologia low ticket. Inadequação, Identificação com o Problema, Plug & Play e Promessa Boa Demais. Cada copy segue as 7 leis e termina com parágrafo técnico/racional.
---

# Páginas Low Ticket — 4 Copies

Gera as 4 copies de abertura para páginas de vendas low ticket. Cada copy é um estilo diferente de gancho. Você escolhe qual usar ou testa as 4.

## Usage

```
/lt-pagina
```

## Princípio Central

A melhor copy não parece copy. Parece alguém inteligente explicando algo que você nunca tinha entendido direito.

A copy nunca vende. Ela informa, avisa ou ensina. O produto não existe nos primeiros parágrafos. Só existe o leitor e a realidade dele.

## As 7 Leis (aplicar em todas as copies)

1. **Ensinar em vez de prometer**: a copy entrega conhecimento real ali mesmo. A curiosidade vem de querer saber o resto, não de uma promessa vaga.
2. **Nomear cria realidade**: sempre que possível, crie um nome próprio para o conceito, problema ou solução. Exemplos que funcionam: "Negociação Terapêutica", "Programação Emocional Repetitiva", "Peeling Estratificado Programado".
3. **O produto não aparece na copy**: nenhuma copy fala "esse curso", "esse treinamento", "compre".
4. **Tom de escritor, não de vendedor**: frases proibidas: "Isso vai transformar sua vida", "Descubra o método", "Não perca essa oportunidade".
5. **Especificidade mata generalização**: "Antes dos 7 anos" > "na infância". "15 mil pra 70 mil por projeto" > "multiplique seus ganhos".
6. **Informar, não vender**: as copies fazem uma de duas coisas, avisam ou ensinam. Nunca vendem.
7. **Crie um inimigo concreto**: vendedora da loja, professor do YouTube, método antigo. A pessoa não precisa admitir que errou, só que foi mal orientada.

## Vícios Proibidos

- Travessão longo: NUNCA usar. Use vírgula, ponto, ou reformule a frase.
- Estrutura "Não é X. É Y.": NUNCA usar. É muleta de IA.
- Frases genéricas: "Transforme sua vida", "Descubra o segredo", "Método revolucionário".
- Mencionar o produto na copy.
- Emojis.

**Checklist obrigatório antes de entregar qualquer copy:**

- [ ] Nenhum travessão no texto
- [ ] Nenhuma estrutura "Não é X. É Y."
- [ ] Nenhuma frase genérica de vendedor

---

## O Que Fazer

### 1. Contexto

Leia `meus-produtos/.ativo` e `meus-produtos/{ativo}/perfil.md`. Se não existir, oriente a usar `/produto-editar` primeiro.
Leia também `meus-produtos/{ativo}/idconsumidor.md` se existir.

### 1.4.5. Detecção de primeira página low ticket (Categoria Padrão automática)

Antes do framework Quiz vs. Página, verifique se a pasta `meus-produtos/{ativo}/entregas/paginas/` está vazia ou se nenhum arquivo dela começa com `pagina-`. Se está vazia, é a primeira página low ticket do aluno. Nesse caso, recomende a Categoria **Padrão** automaticamente.

Apresente:

```
Esta é a primeira página low ticket que você está criando. A recomendação para começar é a Categoria Padrão.

A Padrão é uma estrutura completa de 14 seções que cobre todos os ângulos clássicos de uma página low ticket: cabeçalho com gancho, comparações visuais, diálogo mental negativo, "a culpa não é sua", prova matemática, centro da atenção, dinâmica de acesso, demonstração, autoridade, depoimentos, entregáveis, ancoragem final e FAQ. É a base mais segura para quem está começando.

1. Seguir com a Padrão (recomendado)
2. Quero ver as outras 4 categorias mesmo assim

Digite o número:
```

**Se escolher 1:** pule direto para a Seção 5.3 (Entrevista Específica da Padrão) e depois a Seção 6 com a Estrutura E. Pular as Etapas 2, 3 e 4 (entrevista de público, geração das 4 copies, matriz de decisão).

**Se escolher 2:** continue para a Etapa 1.5 abaixo.

Se a pasta já tem páginas anteriores, NÃO ofereça a Padrão automaticamente. Siga direto para a Etapa 1.5 (o framework Quiz vs. Página vai decidir o fluxo).

### 1.5. Framework de Decisão: Página vs. Quiz

Antes de iniciar a entrevista, analise os dados do perfil e do consumidor e aplique este framework. **Nunca pergunte de cara qual formato o aluno quer**. Recomende com base nos critérios abaixo e explique o porquê.

| Critério | Aponta para QUIZ | Aponta para PÁGINA |
|---|---|---|
| Tipo de produto | Emocional / dor / identificação | Prático / ferramenta / direto ao ponto |
| Nível de consciência do lead | Não sabe que tem problema | Já sabe o que quer |
| Complexidade da decisão | Precisa diagnosticar / explicar | Decisão simples e direta |
| Faixa de preço | Até R$47 | Acima de R$97 |
| Tipo de público | Emocional | Analítico / pragmático |

**Regra:** 2 ou mais critérios para o mesmo lado, siga ele. **Desempate:** recomendar QUIZ (mais rápido de validar).

Apresente a recomendação assim:

```
Com base no seu produto e público, minha recomendação é:

→ [QUIZ ou PÁGINA DE VENDAS]

Por quê:
• [Critério 1]: [explicação com dado real do produto]
• [Critério 2]: [explicação com dado real do produto]
• [Critério 3]: [explicação com dado real do produto]

Você pode trocar depois se quiser testar o outro formato.

1. Concordo, seguir com [recomendação]
2. Prefiro o outro formato
```

**Se escolher QUIZ:** encaminhe para `/lt-quiz` e encerre este comando.
**Se escolher PÁGINA:** continue para a Etapa 2 abaixo.

### 2. Entrevista (UMA pergunta por vez)

**Bloco 1/2. Público:**
```
O público do produto é:

1. O profissional da área (ex: o terapeuta, o nutricionista, o designer)
2. O cliente final (ex: quem quer emagrecer, quem quer aprender inglês)

Digite o número:
```

**Bloco 2/2. Faixa de Preço:**
```
Qual a faixa de preço do produto?

1. R$17 a R$47 (entrada ultra low ticket)
2. R$47 a R$97 (low ticket clássico)
3. R$97 a R$197 (low ticket premium)
4. R$197 a R$497 (mid ticket)

Digite o número:
```

**Confirmação antes de gerar:**
```
Resumo do que vou criar:
- Produto: [nome do produto ativo]
- Público: [profissional / cliente final]
- Faixa de preço: R$[faixa]
- Entregáveis: 4 copies completas (Inadequação, Identificação, Plug & Play, Promessa Boa Demais)

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 3. Geração das 4 Copies

Gere as 4 copies em sequência. Cada copy deve:
- Aplicar as 7 leis sem exceção
- Evitar todos os vícios proibidos
- Terminar com parágrafo técnico/racional em itálico

---

#### Copy 1. Inadequação

**Engrenagem:** a pessoa descobre que está fazendo algo errado ou está desatualizada. Sente "será que estou ficando pra trás?". Urgência silenciosa impossível de ignorar.

**Estrutura obrigatória:**
1. Afirmação direta que coloca o leitor numa posição desconfortável (desatualizado, fazendo errado, ignorando algo que deveria saber)
2. Contextualização curta: o que mudou, por que o jeito antigo não funciona mais
3. Nome próprio para o problema ou solução
4. Parágrafo técnico/racional em itálico

**Variação poderosa. Inadequação com Alerta:** crie um inimigo concreto externo (vendedora, professor, método antigo). Use números específicos (7 itens, R$1.600). Escale de consequência financeira para emocional ou de segurança.

**Melhor para:** cursos, aulas, métodos, frameworks. Nichos com atualização constante. Versátil em preço (R$47 a R$500+).

---

#### Copy 2. Identificação com o Problema

**Engrenagem:** a pessoa lê e pensa "isso sou eu." Você descreve a realidade dela com tanta precisão que ela sente que você está dentro da cabeça dela. Confiança instantânea.

**Estrutura obrigatória:**
1. Descrição vívida do problema com detalhes sensoriais e emocionais (4 a 6 parágrafos, sem pressa)
2. Amplificação: aprofunde na dor OU pinte o cenário ideal
3. Revele o "grande problema": por que o que a pessoa já tentou não funciona
4. Parágrafo técnico/racional em itálico

**Melhor para:** métodos, cursos práticos, mentorias. Público que já tentou resolver sozinho e fracassou. Forte para low ticket puro (R$27 a R$197).

---

#### Copy 3. Plug & Play

**Engrenagem:** a pessoa não precisa aprender nada, estudar nada, mudar nada. Só precisa pegar e usar. O valor está na praticidade imediata.

**Estrutura obrigatória:**
1. Headline curta que mostra o resultado prático
2. Um parágrafo que explica o que a pessoa recebe e como usa (sem jargão)
3. Parágrafo técnico/racional em itálico
4. CTA

**Melhor para:** planilhas, templates, checklists, scripts prontos, kits, packs. Low ticket clássico (R$37 a R$97).

---

#### Copy 4. Promessa Boa Demais (Específica)

**Engrenagem:** a pessoa lê e pensa "não é possível, mas se for verdade...". O que segura ela é a combinação de resultado muito desejável com especificidade tão concreta que parece real demais pra ser marketing.

**Estrutura obrigatória:**
1. Resultado específico com números e situação concreta (antes e depois pessoal)
2. Frase que derruba uma objeção ou crença limitante
3. Convite a ver os detalhes, sem pressão
4. Parágrafo técnico/racional em itálico

**ATENÇÃO:** essa categoria exige história verdadeira com números verificáveis. Sem história real, não use essa categoria. Ela desaba.

---

### 4. Matriz de Decisão (indicar qual copy usar)

Após gerar as 4, indique qual é mais indicada para o produto:

- Precisa aprender → Inadequação, Identificação ou Promessa Boa Demais
- Precisa usar → Plug & Play
- Já sabe e já sofre → Identificação com o Problema
- Não sabe ou acha que está bem → Inadequação
- Expert tem história real com números → Promessa Boa Demais

### 5. Aprovação e Salvamento

Mostre as 4 copies e pergunte:
```
As 4 copies estão prontas.

1. Aprovar e salvar todas
2. Quero ajustar alguma copy
3. Salvar só a copy [número]
```

Salvar em: `meus-produtos/{ativo}/entregas/copy-pagina/copies-low-ticket-[produto].md`

Após salvar, pergunte:
```
Quer que eu gere a página HTML agora com a copy escolhida?

1. Sim, gerar a página HTML completa
2. Não, vou usar /copy-pagina depois

Digite o número:
```

Se escolher **1**, continue:

```
Qual copy usar na página?

1. Inadequação
2. Identificação com o Problema
3. Plug & Play
4. Promessa Boa Demais

Digite o número:
```

```
Qual o preço do produto?
(ex: "R$37" ou "R$97 ou 12x R$9")
```

```
O acesso ao produto é vitalício?

Objetivo: se for vitalício, vou destacar "Acesso vitalício" em todos os pontos de preço da página.
É um argumento forte de venda.

1. Sim, acesso vitalício
2. Não, tem prazo de acesso
```
Se tiver prazo: perguntar qual é.

```
Link de checkout (Hotmart, Kiwify)?
```

```
Preferência de cor?

1. Azul (confiança, autoridade)
2. Verde (saúde, resultados)
3. Roxo (marketing, criatividade)
4. Vermelho (urgência, paixão)
5. Rosa (beleza, feminino)
6. Preto/Dourado (premium)
7. Deixa comigo

Digite o número:
```

**Se a copy escolhida for "Identificação com o Problema":** seguir para a Seção 5.1.
**Se a copy escolhida for "Inadequação":** seguir para a Seção 5.2.
Para Plug & Play e Promessa Boa Demais, seguir direto para a Seção 6.

### 5.1. Entrevista Específica: Identificação com o Problema

**Fazer UMA pergunta por vez.**

**Pergunta 1. Logo:**
```
Você tem a logo do produto em PNG com fundo transparente?

Objetivo: a logo fica centralizada no topo da página, sobre fundo branco.

1. Tenho, vou informar o caminho do arquivo
2. Não tenho logo
```
Se tiver: pedir o caminho. Copiar para `meus-produtos/{ativo}/entregas/paginas/`.
Se não tiver: usar o nome do produto como texto no header.

**Pergunta 2. Depoimentos:**
```
Você tem prints/screenshots de depoimentos de clientes?

Objetivo: a página mostra os depoimentos como imagens reais, não como texto.

1. Tenho prints, vou informar a pasta
2. Não tenho depoimentos ainda
```
Se tiver: pedir o caminho da pasta. Copiar todas as imagens para `meus-produtos/{ativo}/entregas/paginas/`.
Se NÃO tiver: buscar notícias e estatísticas via WebSearch. Criar uma seção "Argumentos" com cards contendo os dados encontrados, com fonte citada.

**Pergunta 3. História do criador:**
```
Qual a história por trás da criação desse produto? Como você chegou até ele?

Objetivo: a seção "Quem sou eu" conta a história real de como e por que o produto foi criado.
```

**Pergunta 4. Imagem da seção "Quem sou eu":**
```
Quer usar uma foto sua na seção "Quem sou eu" ou prefere uma imagem que gere identificação com o público?

1. Quero usar minha foto
2. Prefiro uma imagem que represente o público
```
Copiar o arquivo escolhido para `meus-produtos/{ativo}/entregas/paginas/`.

**Pergunta 5. Suporte:**
```
Como funciona o suporte do produto? Por onde a cliente tira dúvidas?

Objetivo: o suporte é um argumento forte de venda. Vou destacar isso ao lado da garantia.

(ex: "WhatsApp direto comigo, resposta em até 24h", "Grupo no Telegram")
```

**Confirmação antes de gerar HTML:**
```
Resumo do que vou criar:
- Tipo: Página de vendas low ticket (Identificação com o Problema)
- Produto, Preço, Acesso, Cor
- Logo, Depoimentos, História, Imagem Quem Sou, Suporte

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 5.2. Entrevista Específica: Inadequação

**Pergunta 1. Ângulo do inimigo:**
```
Qual o "inimigo" da copy de inadequação? É o comportamento errado que o público pratica hoje.

Objetivo: vou criar um nome próprio para esse comportamento (ex: "Precificação Espelho").

1. Copiar o preço da concorrente
2. A formação/curso que nunca ensinou algo essencial
3. O "achismo" ou feeling como método
4. Outro (me descreva)
```

**Perguntas 2 a 5.** Seguir exatamente o mesmo fluxo da Seção 5.1 (Logo, Depoimentos, História, Imagem Quem Sou, Suporte).

**Confirmação antes de gerar HTML:**
```
Resumo do que vou criar:
- Tipo: Página de vendas low ticket (Inadequação)
- Produto, Preço, Acesso, Cor
- Inimigo: [ângulo] → Nome: [nome criado]
- Logo, Depoimentos, História, Imagem Quem Sou, Suporte

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 5.3. Entrevista Específica: Padrão (Estrutura E)

Esta seção é acionada quando o aluno escolheu a Categoria Padrão na Etapa 1.4.5. As outras 4 estruturas (A, B, C, D) NÃO passam por aqui.

**Antes de qualquer pergunta, leia `.claude/skills/paginas/references/categoria-padrao-lt.md`.** Esse arquivo contém o processo detalhado de cada uma das 18 seções (prompt, regras e layout). Use-o como fonte de verdade ao gerar a página.

**Fazer UMA pergunta por vez.**

**Pergunta 1. Modo de geração:**

```
A Categoria Padrão tem 3 modos de geração. Qual você prefere?

1. Híbrido (recomendado). As seções que dependem só do perfil rodam automáticas. As que exigem dado real (Faça a Conta, Demonstração, Quem É, Depoimentos) entram em modo guiado.
2. Guiado. A skill faz uma seção por vez, perguntando o que precisa, gerando, aprovando e seguindo pra próxima. Mais lento, mais profundo.
3. Automático. A skill gera as 14 seções de uma vez usando só o que está no perfil.md e idconsumidor.md. Mais rápido.

Digite o número:
```

**Pergunta 2. Preço:**

```
Qual o preço do produto?
(ex: "R$37" ou "R$97 ou 12x R$9")
```

**Pergunta 3. Acesso:**

```
O acesso ao produto é vitalício?

1. Sim, acesso vitalício
2. Não, tem prazo de acesso
```

Se tiver prazo, perguntar qual é.

**Pergunta 4. Link de checkout:**

```
Link de checkout (Hotmart, Kiwify)?
```

**Pergunta 5. Preferência de cor:**

```
Preferência de cor?

1. Azul (confiança, autoridade)
2. Verde (saúde, resultados)
3. Roxo (marketing, criatividade)
4. Vermelho (urgência, paixão)
5. Rosa (beleza, feminino)
6. Preto/Dourado (premium)
7. Deixa comigo

Digite o número:
```

**Perguntas 6 a 10. Mesmo fluxo da Seção 5.1** (Logo, Depoimentos, História do criador, Imagem da seção Quem Sou, Suporte). Repetir exatamente as mesmas perguntas e regras de cópia de arquivo.

**Perguntas específicas da Padrão (só se modo Guiado ou Híbrido). Pular se modo Automático.**

**Pergunta 11. Demonstração:**

```
Para a seção Demonstração, você tem material visual real do produto rodando?

1. Tenho print da ferramenta/template preenchido
2. Tenho vídeo curto (30 a 60 segundos)
3. Tenho foto de antes e depois real
4. Não tenho material visual ainda

Digite o número:
```

Se tiver: pedir o caminho do arquivo e copiar para `meus-produtos/{ativo}/entregas/paginas/`.
Se não tiver: avisar que essa seção fica com placeholder visual e sugerir gravar 30 segundos no celular abrindo o produto depois.

**Pergunta 12. Faça as Contas (se produto tem resultado mensurável):**

Antes de perguntar, analisar o perfil. Se o produto é puramente emocional (autoestima, espiritualidade, luto, ansiedade), pular essa pergunta e marcar a seção 5 como "não se aplica" (substituir por reforço da Tabela Comparação).

Se tem resultado mensurável:

```
Para a seção Faça as Contas, qual é a métrica principal que muda com o produto?

(ex: "ticket médio sobe de R$ 12 para R$ 45", "fatura sobe de 14 mil para 38 mil", "perde 4 kg por mês", "economiza R$ 600 por mês na conta de luz")

Pode dar uma estimativa realista. Os números viram exemplo hipotético na página, o aluno depois substitui pelos reais.
```

**Confirmação antes de gerar HTML:**

```
Resumo do que vou criar:
- Tipo: Página de vendas low ticket (Categoria Padrão, Estrutura E, 14 seções)
- Modo: [Híbrido / Guiado / Automático]
- Produto, Preço, Acesso, Cor
- Logo, Depoimentos, História, Imagem Quem Sou, Suporte
- Demonstração: [tem material / placeholder]
- Faça as Contas: [aplica com métrica X / não se aplica]

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

---

### 6. Geração da Página HTML

#### REGRA DE OURO #1: Toda a página converge para o Quadro

O Quadro é o resultado final que a pessoa conquista usando o produto (lido em `meus-produtos/{ativo}/perfil.md`). Isso significa:

- **TODOS os botões de CTA** usam o Quadro como texto do botão (adaptado para "Quero + [Quadro]"). NUNCA usar "Comprar agora", "Saiba mais" ou "Quero descobrir".
- **A conclusão da seção "Quem Sou"** termina reforçando o Quadro como motivo da criação do produto.
- **O CTA Final** usa o Quadro como headline principal.
- **O CTA flutuante mobile** também usa o Quadro como texto.

Exemplo (Quadro = "Ter lucratividade real em todos os procedimentos da agenda"):
- Botão hero: "Quero ter lucro real em cada procedimento"
- Botão oferta: "Quero ter lucratividade real em toda a minha agenda"
- Conclusão Quem Sou: "...para que toda profissional possa ter lucratividade real em todos os procedimentos da agenda"
- Headline CTA Final: "Ter lucratividade real em todos os procedimentos da sua agenda"

#### REGRA DE OURO #2: Ancoragem + Acesso Vitalício + Suporte (aplicar em TODAS as páginas)

1. **Ancoragem de preço:** em TODOS os pontos onde o preço aparece, mostrar valor riscado acima do preço real. Valor âncora = preço + R$200. Usar tag `<s>` para riscar.

2. **Acesso vitalício ou prazo:** exibir "Pagamento único. Acesso vitalício." em todos os pontos de preço (ou "Acesso por [prazo]").

3. **Suporte:** incluir como card próprio ao lado da garantia. Copy emocional: "Você não fica sozinha" + canal + prazo.

#### REGRA DE OURO #3: Header sem logo placeholder gerado (aplicar em TODAS as páginas)

**PROIBIDO** gerar header sticky com placeholder visual no logo (quadradinho/círculo/forma colorida gerada por CSS `::before` ou `::after`, ícone genérico, gradiente decorativo no lugar de logo real). Esse padrão deixa a página com cara de template de IA não finalizado.

Comportamento obrigatório:

1. **Se o aluno tem logo PNG/SVG real:** usar a logo dele dentro de `<img>` no header. Pedir o caminho do arquivo na Seção 5.x correspondente. Copiar pra `meus-produtos/{ativo}/entregas/paginas/`.
2. **Se o aluno não tem logo:** usar APENAS o nome do produto em tipografia limpa (sans-serif, peso 700 a 800, sem ícone decorativo ao lado). Sem quadrado colorido, sem círculo gradiente, sem placeholder gráfico.
3. **Se o aluno preferir página mais limpa:** pode optar por não ter header sticky no topo. O Hero da Seção 1 já cumpre o papel de identificação visual do produto.

Pergunta a fazer durante a Seção 5.3 (entrevista da Padrão):

```
Você tem a logo do produto em PNG/SVG?

1. Tenho, vou informar o caminho do arquivo
2. Não tenho. Usar só o nome do produto em texto no header.
3. Não tenho e prefiro página sem header sticky (Hero vira o topo da página)

Digite o número:
```

Aplicar a mesma regra nas Estruturas A, B, C, D (Identificação, Inadequação, Promessa Boa Demais, Plug & Play). Nenhuma página gerada pela skill pode sair com logo placeholder colorido decorativo.

#### Design Rules (aplicar obrigatoriamente)

Antes de gerar, leia `.claude/skills/paginas/SKILL.md` e `.claude/skills/paginas/references/cdn-design-resources.md`.

**Regras críticas:**
- **TODAS as fontes sans-serif** (heading E body). Serifadas são PROIBIDAS.
- **Mínimo 4 tipos de fundo** diferentes entre seções (claro, escuro, imagem+overlay, gradiente)
- **Pelo menos 2 seções com imagem de fundo** (placeholder HTML/CSS com emoji+label, nunca picsum aleatório)
- **Grid 2 colunas** para entregáveis. NUNCA 3 colunas
- **Cards** com min-width 320px, padding 28px+, font-size 0.95rem+
- **Header com logotipo** obrigatório
- **Texto SEMPRE em pt-BR com acentos** corretos
- **NÃO parecer Lovable/v0**

**Mixagem de templates (inspiração, não bloqueia estrutura):**
Os templates de `skills/paginas/references/templates/` servem como inspiração visual. A ESTRUTURA de seções abaixo SEMPRE vence qualquer sugestão de template. Se o template não tem uma seção da estrutura obrigatória, criar a seção do zero usando `design-system-components.md` como fallback.

---

## Estruturas HTML específicas por categoria

**IMPORTANTE:** a estrutura depende da categoria de copy escolhida. NÃO aplicar a mesma estrutura para as 4 categorias. Cada uma tem um layout próprio.

---

### Estrutura A. Identificação com o Problema

**Seções obrigatórias (11. conferir TODAS antes de salvar):**

**1. Header**: fundo branco, logo centralizada, sticky com sombra sutil. Fallback: nome do produto em texto.

**2. Hero (copy + CTA)**: fundo escuro (gradiente), headline com números específicos do perfil, bloco de história com borda lateral colorida (3 parágrafos: situação, descoberta, impacto), números em destaque (cor accent). **CTA = Quadro adaptado**. Nota: "Acesso imediato após o pagamento".

**3. Depoimentos com imagens reais**: fundo claro, título "Mais de X [público] já [resultado]", grid 2 colunas desktop / 1 mobile. Cada card = imagem do print + caption "Depoimento real via WhatsApp" + ícone WhatsApp verde (#25d366). Se NÃO tiver prints: seção "O que os dados mostram" com estatísticas e fontes buscadas via WebSearch.

**4. Como Funciona (Trilha Vertical com Decorados)**: fundo claro alternativo (rosa-claro/cinza-claro), label com nome do método (Furadeira). Layout = trilha vertical com linha conectando etapas (NÃO grid). Cada etapa = número circular + card com título, texto curto (1-2 frases) e benefício emocional (Decorado). Última etapa com fundo escuro e tags de output.

**5. Oferta (Benefícios Emocionais do Dia a Dia)**: fundo escuro (gradiente), título "O que muda no seu dia a dia". NÃO usar Stack de Valor tradicional. Box com 6-8 benefícios emocionais (Decorados), cada um com ícone de check. Bloco de preço: ancoragem riscada + preço real + "Pagamento único. Acesso vitalício.". **CTA = Quadro adaptado** (variação diferente do hero).

**6. Garantia + Suporte (Cards lado a lado)**: fundo claro com gradiente sutil. Grid 2 colunas (1 no mobile):
- Card Suporte: header accent, ícone do canal, copy "Você não fica sozinha" + canal + prazo
- Card Garantia: header cor primária, selo circular com dias, copy humanizada

**7. Quem Sou Eu**: fundo escuro, grid imagem + texto. Imagem = foto do criador ou imagem de identificação com o público (borda dourada). Label "Por que criei essa ferramenta". História em Light Copy, destaques em accent. **Última frase DEVE concluir com o Quadro** (ex: "Criei para que toda [público] possa [Quadro]").

**8. FAQ**: 5 perguntas. NUNCA revelar formato do produto. NUNCA criar objeções que não existiam. Priorizar aplicabilidade, tempo de resultado, dificuldade, garantia, compatibilidade.

**9. CTA Final**: fundo gradiente (primária → escuro), **headline = Quadro do perfil como frase principal**, texto de suporte pintando cenário transformado, preço com ancoragem, **CTA = Quadro adaptado**, nota de garantia.

**10. Footer**: nome do produto + links (política, termos, contato).

**11. CTA Flutuante Mobile**: barra fixa no rodapé apenas em mobile, texto = Quadro adaptado.

Salvar em: `meus-produtos/{ativo}/entregas/paginas/pagina-low-ticket-[produto].html`

---

### Estrutura B. Inadequação

#### REGRA DE OURO desta estrutura: Foco na solução, problema é contexto

A página de Inadequação cria um conceito nomeado (inimigo) e faz o paralelo com a solução. O problema aparece para gerar identificação, mas o FOCO é sempre na solução e no Quadro.

#### Regra dos Bullet Points Emocionais

Na seção de oferta e no comparativo, usar **no máximo 4 bullet points**, todos 100% na emoção do dia a dia. Sem dados técnicos. Cada bullet descreve um sentimento ou situação emocional que a pessoa vai viver.

Exemplos bons: "Fechar o mês sentindo que o dinheiro faz jus ao que você trabalhou", "Cobrar sem aquele aperto no peito de quem não sabe se o preço está certo".
Exemplos ruins: "Ter clareza financeira", "Saber o custo real de cada procedimento".

**Seções obrigatórias (11. conferir TODAS antes de salvar):**

**1. Header**: mesmo padrão (branco, logo centralizada, sticky).

**2. Hero. Inadequação com foco na solução**: tag = nome do produto/solução (NÃO do problema). Headline forte de identificação com o comportamento errado. Copy com elementos do dia a dia (aluguel, insumo, energia). Menciona o conceito nomeado (ex: "Precificação Espelho") em 1 parágrafo como contexto. **A copy CONCLUI no Quadro**, não no problema. **CTA = Quadro adaptado**.

**3. Comparativo lado a lado (EXCLUSIVO da Inadequação)**: fundo escuro (gradiente), título de contraste (ex: "Duas formas de precificar. Só uma dá lucro."), subtítulo provocativo. **2 cards lado a lado**:
- **Card esquerdo. Problema (APAGADO):** fundo quase transparente, borda cinza fraca, opacidade 0.4-0.5, ícones X vermelhos. Título = nome do problema. **Máximo 4 itens NA EMOÇÃO**.
- **Card direito. Solução (DESTAQUE):** borda com cor primária + glow (box-shadow com blur), background iluminado, opacidade 0.85-0.9, badge "O que muda na sua rotina", ícones check dourados. Título = nome da solução. **Máximo 4 itens NA EMOÇÃO** (espelho positivo da esquerda). **O olho do visitante deve ir naturalmente para este card**.

**4. Depoimentos com imagens reais**: mesmo padrão da Estrutura A. Título adaptado ao ângulo (ex: "Quem parou de copiar preço e calculou o seu"). Se NÃO tiver prints: dados via WebSearch.

**5. Como Funciona (Trilha Vertical com Decorados)**: mesmo padrão da Estrutura A. Título adaptado (ex: "Como sair da Precificação Espelho").

**6. Oferta (Benefícios Emocionais)**: fundo escuro, título adaptado (ex: "O que muda quando o preço é seu"). **Máximo 4 bullets 100% emoção**. Preço com ancoragem + acesso vitalício. CTA = Quadro.

**7. Garantia + Suporte (Cards lado a lado)**: mesmo padrão da Estrutura A.

**8. Quem Sou Eu**: mesmo padrão. A história menciona o conceito nomeado como o que a pessoa praticava. **Última frase conclui no Quadro**.

**9. FAQ**: mesmo padrão (sem revelar produto).

**10. CTA Final + Footer**: headline = Quadro, CTA = Quadro adaptado, footer abaixo.

**11. CTA Flutuante Mobile**: texto = Quadro adaptado.

Salvar em: `meus-produtos/{ativo}/entregas/paginas/pagina-inadequacao-[produto].html`

---

### Estrutura C. Promessa Boa Demais

#### REGRA DE OURO desta estrutura: Tom de relato, não de promessa

A página inteira soa como alguém contando o que aconteceu. "Deixa eu te contar o que aconteceu" é o tom. A história real com números verificáveis é o motor. Sem história real, NÃO usar essa categoria.

**Seções obrigatórias (11. conferir TODAS antes de salvar):**

**1. Header**: mesmo padrão.

**2. Hero. Relato pessoal com números**: tag "Caso real de [tema]", headline com números antes/depois em destaque (ex: "Eu cobrava R$750. Precisava cobrar R$1.157,25."), copy em tom de relato (situação → descoberta → impacto). **Bloco de impacto**: caixa destacada com borda dourada contendo os números-chave. Frase de virada (ex: "Você não está aumentando o preço. Está cobrando o preço certo pela primeira vez."). CTA = Quadro adaptado.

**3. Prova. Citações verticais (EXCLUSIVO da Promessa Boa Demais)**: fundo claro, título "Não foi só comigo". **Layout: citações verticais, UMA debaixo da outra** (NUNCA grid lado a lado). Cada citação = borda lateral cor primária, fundo suave, aspas decorativas grandes, texto em itálico com números em negrito, rodapé "Cliente via WhatsApp" + badge de resultado. 3 citações. Max-width ~640px, centralizado.

**4. Depoimentos com imagens reais**: mesmo padrão. Título "Os prints falam por si".

**5. Como Funciona (Trilha Vertical)**: mesmo padrão, títulos em tom de relato ("Como eu fiz esse cálculo", não "Como funciona"). Títulos das etapas em linguagem pessoal.

**6. Oferta (Benefícios Emocionais)**: mesmo padrão (máximo 4 bullets). Título adaptado (ex: "Isso é o que acontece quando você faz a conta pela primeira vez"). Ancoragem + acesso vitalício.

**7. Garantia + Suporte**: mesmo padrão.

**8. Quem Sou Eu**: mesmo padrão, conclusão no Quadro.

**9. FAQ**: mesmo padrão.

**10. CTA Final + Footer**: Quadro + ancoragem + acesso vitalício, footer abaixo.

**11. CTA Flutuante Mobile**: mesmo padrão.

Salvar em: `meus-produtos/{ativo}/entregas/paginas/pagina-promessa-boa-demais-[produto].html`

---

### Estrutura D. Plug & Play

Página mais curta e direta. O valor é praticidade imediata. Mesmo assim, TODAS as seções são obrigatórias.

**Seções obrigatórias (11. conferir TODAS antes de salvar):**

**1. Header**: fundo branco, logo centralizada, sticky.
**2. Hero**: headline curta mostrando resultado prático (ex: "3 produtos. Menos de R$120. Resultado em 2 semanas."). CTA = Quadro adaptado. Nota "Acesso imediato".
**3. Ferramenta / o que é**: fundo claro, 1 parágrafo explicando o que a pessoa recebe e como usa (sem jargão).
**4. Depoimentos ou prova**: grid 2 colunas com prints reais ou dados do nicho.
**5. Entregáveis em grid 2 colunas**: cards com o que compõe o pack (checklist, planilha, guia).
**6. Oferta**: fundo escuro, bullets emocionais (até 4), preço com ancoragem, acesso vitalício, CTA = Quadro.
**7. Garantia + Suporte (cards lado a lado)**: mesmo padrão.
**8. Quem Sou Eu**: versão curta, conclusão no Quadro.
**9. FAQ**: 3 a 5 perguntas, sem revelar formato.
**10. CTA Final + Footer**: headline = Quadro, ancoragem, footer.
**11. CTA Flutuante Mobile**: texto = Quadro adaptado.

Salvar em: `meus-produtos/{ativo}/entregas/paginas/pagina-plug-play-[produto].html`

---

### Estrutura E. Padrão (recomendada para a primeira página low ticket do aluno)

#### REGRA DE OURO desta estrutura: 14 seções na ordem fixa

A Categoria Padrão é a recomendação default quando o aluno está criando a primeira página low ticket no sistema (acionada pela Etapa 1.4.5). Cobre 14 seções que mapeiam todos os ângulos clássicos de venda de produto digital de entrada: cabeçalho com gancho, comparações visuais, diálogo mental negativo, absolvição (A Culpa Não É Sua), prova matemática, centro da atenção, dinâmica de acesso, demonstração, autoridade, depoimentos, entregáveis, ancoragem final e FAQ.

#### Fonte de verdade do processo detalhado

Antes de gerar qualquer seção, leia `.claude/skills/paginas/references/categoria-padrao-lt.md`. Esse arquivo contém o prompt completo de cada uma das 14 seções (contexto, passos, exemplos de referência, regras e layout HTML). Use-o como manual de execução. Esta skill só lista a estrutura e as regras de orquestração.

#### Modo de geração (definido na Pergunta 1 da Seção 5.3)

- **Híbrido (default).** Seções que vêm do perfil rodam automáticas. Seções que exigem dado real (Faça a Conta, Demonstração, Quem É, Depoimentos) entram em modo guiado.
- **Guiado.** Faz uma seção por vez, pergunta o que precisa, gera, aprova, próxima.
- **Automático.** Gera as 14 de uma vez usando só `perfil.md` e `idconsumidor.md`. Seções que dependem de input real entram com placeholder claro pra revisão posterior.

#### Seções obrigatórias (14, conferir TODAS antes de salvar)

**1. Cabeçalho (Headline + Pitadas de Desejo).** Headline principal seguindo fórmula obrigatória (verbo de ação concreto + identificação com problema + resultado imediato). Subhead com 3 a 4 pitadas de desejo (máximo 6 palavras cada). Layout: fundo escuro com gradiente, logo no topo (header sticky), headline em destaque grande, CTA com Quadro adaptado, nota "Acesso imediato após o pagamento".

**2. Comparação Primária (visual).** Peça única de alto impacto com 2 lados. Esquerdo (✗) com título do estado ruim + cena identificável + 2 métricas. Direito (✓) com título do estado aspiracional + cena desejável + 2 métricas. Nunca usar "Antes" e "Depois" como título. Layout: grid 2 colunas (1 mobile), ícones grandes ✗ e ✓, contraste vermelho/verde óbvio.

**3. Tabela Comparação.** 2 categorias (Resultado e Processo), 6 itens cada. Para produto subjetivo: 3 itens técnicos + 3 emocionais por categoria. Layout: tabela 2 colunas no desktop, stack vertical no mobile.

**4. Diálogo Mental Negativo.** Título com a dor principal em negrito. Subtítulo "e você sofre todo dia com pensamentos como...". 4 pensamentos escolhidos do mapa de 12 (6 emocionais + 6 racionais). Layout: fundo escuro, cards estilo balão de pensamento, parte mais dolorosa em negrito.

**5. A Culpa Não É Sua.** Identificação + absolvição + revelação. 3 blocos com subtítulos personalizados ao nicho (nunca "Identificação/Absolvição/Revelação"). Bloco 1: EXATAMENTE 3 situações com esforço + problema real. Bloco 2: parágrafo curto de 2-3 linhas de absolvição. Bloco 3: 2-3 mudanças contraintuitivas em parágrafos curtos. Título e subtítulo personalizados ao nicho. Layout: fundo claro acolhedor, 3 blocos com hierarquia visual, bloco 2 com fundo levemente diferente.

**6. Faça as Contas pro Cliente.** SÓ usar se o produto tem resultado mensurável. Título conectando ação do dia a dia com "faz a conta comigo". 2 cenários numéricos (A sem o produto, B com o produto). Cálculos simples até o resultado final no bolso. Linha de impacto final. Se o produto for puramente emocional, substituir essa seção por reforço da Tabela Comparação ou expandir o Diálogo Mental Negativo.

**7. Centro da Atenção.** 1 elemento físico do produto no centro (objeto, ferramenta, parte do corpo, prato, documento). 8 elementos curtos (máximo 4 palavras cada) ao redor com setas apontando pro centro. Centro DEVE ser visualmente representável.

**8. Dinâmica de Acesso.** Mostra que o caminho entre comprar e ter resultado é curto, simples e óbvio. Sempre Acesso → Execução → Resultado. Gerar 2 versões (A com 3 passos, B com 5 passos) e o aluno escolhe. Cada passo com título ultra curto (máximo 3-4 palavras) + frase de apoio de 1 linha. Primeiro passo SEMPRE acesso; último passo SEMPRE resultado. Nunca "na mesma semana": usar "hoje", "no mesmo dia", "agora", "em minutos". Layout: trilha horizontal numerada com badges, fundo claro.

**9. Demonstração.** Peça visual REAL do produto rodando (print, vídeo curto, foto antes/depois). 10 opções de "momento mágico" para o aluno escolher 1. Título com verbo visual ("veja", "olha", "assista", "repara"). 3 orientações práticas de gravação. Se aluno não tiver material, marcar com placeholder visual e sugerir gravar 30 segundos no celular depois. Para temas sensíveis (luto, trauma, saúde mental), aplicar regras de acolhimento silencioso.

**10. Quem É o Especialista.** Entrevista em 3 blocos (Autoridade e credenciais, História pessoal e motivação, Valores e humanidade). Texto final em 3 parágrafos de até 6 linhas: parágrafo 1 (autoridade), parágrafo 2 (história e fragilidade), parágrafo 3 (valores e humanidade). Última frase OBRIGATORIAMENTE conclui no Quadro do produto. 3 a 5 destaques em accent. Antes de escrever o texto real, mostrar um exemplo hipotético do nicho do aluno marcado como fictício. Layout: grid imagem + texto, fundo escuro, borda dourada na foto.

**11. Depoimentos.** Mínimo 10 depoimentos reais distribuídos em 5 categorias (Resultado rápido, Resultado impressionante, Já tentei outras coisas, Perfil improvável, Mudança de vida). Cada categoria com no mínimo 2 depoimentos. A skill gera 10 exemplos fictícios + 5 exemplos ruins (com explicação) + 5 orientações de coleta. Caption "Depoimento real via [canal], [mês/ano]". Comprovação visual obrigatória sempre que possível (print de WhatsApp, antes/depois, foto do resultado). NUNCA inventar depoimento.

**12. Entregáveis Complementares.** A skill gera 30 entregáveis divididos em 3 categorias (Copia e Aplica Agora mín. 12, Ferramentas Práticas mín. 6, Aulas Estratégicas mín. 6) para o aluno escolher 4 a 5. Todo entregável DEVE ter nome próprio (nunca genérico). Cada um com descrição de 1 linha + valor de ancoragem entre R$ 27 e R$ 97. Soma total entre 5x e 10x o preço real do low ticket. Pelo menos 3 entregáveis devem envolver IA. Pelo menos 2 devem ser ferramentas práticas. Layout: grid 2 colunas (1 mobile), nunca 3 colunas.

**13. Resumo da Ópera (Ancoragem Final).** Lista ULTRA RESUMIDA de tudo que a pessoa leva (só nome + valor riscado). Soma total riscada. Preço real grande. Ancoragem em 3 camadas: valor riscado + frase de retorno (compara com gasto fútil + contrasta com resultado real) + mini depoimento de exemplo (sempre marcar como exemplo a substituir). CTA = Quadro adaptado. NUNCA comparar com serviços profissionais de saúde, com produtos similares ao do criador, ou com vícios/substâncias. Layout: bloco de oferta em destaque, preço real em tipografia gigante, frase de retorno em destaque, mini depoimento em card separado.

**14. FAQ.** Mínimo 12 perguntas divididas em duas categorias: Dúvidas sobre acesso (4 a 5 perguntas) e Dúvidas sobre o produto (7 a 8 perguntas). Respostas sobre acesso: 2-3 linhas. Respostas sobre o produto: 3-5 linhas com confirmação + argumento lógico. NUNCA responder só "sim, funciona". NUNCA excluir outro perfil de comprador ao responder pra um perfil específico (sempre acolher todos). Última pergunta liga ao CTA. NUNCA revelar formato exato do produto. Layout: acordeão (FAQ accordion), com separação visual entre as duas categorias.

**CTA Final.** Entre a seção 14 e o footer. Headline = Quadro. Preço com ancoragem + acesso vitalício. CTA = Quadro adaptado. Nota de garantia.

**Footer.** Nome do produto + links (política, termos, contato).

**CTA Flutuante Mobile.** Barra fixa no rodapé apenas em mobile. Texto = Quadro adaptado.

Salvar em: `meus-produtos/{ativo}/entregas/paginas/pagina-padrao-[produto].html`

---

## Checklist Final de Seções (OBRIGATÓRIO antes de salvar)

Antes de salvar QUALQUER estrutura, conferir item por item. Se faltar qualquer seção, voltar e adicionar ANTES de salvar.

**Estruturas A, B, C, D (Identificação, Inadequação, Promessa Boa Demais, Plug & Play). 11 seções:**

- [ ] 1. Header com logo
- [ ] 2. Hero com CTA = Quadro adaptado
- [ ] 3. Seção específica da categoria (Depoimentos / Comparativo / Citações / Ferramenta)
- [ ] 4. Depoimentos com imagens reais (ou dados via WebSearch)
- [ ] 5. Como Funciona / Entregáveis em grid 2 colunas
- [ ] 6. Oferta com bullets emocionais + ancoragem + acesso vitalício + CTA = Quadro
- [ ] 7. Garantia + Suporte (cards lado a lado)
- [ ] 8. Quem Sou Eu com conclusão no Quadro
- [ ] 9. FAQ sem revelar produto
- [ ] 10. CTA Final com headline = Quadro + Footer
- [ ] 11. CTA Flutuante Mobile = Quadro adaptado

**Estrutura E (Categoria Padrão). 14 seções:**

- [ ] 1. Cabeçalho com headline na fórmula obrigatória + pitadas de desejo (máximo 6 palavras cada)
- [ ] 2. Comparação Primária visual (2 lados ✗ e ✓, sem "Antes/Depois")
- [ ] 3. Tabela Comparação (Resultado e Processo, 6 itens cada)
- [ ] 4. Diálogo Mental Negativo (título com dor em negrito + 4 pensamentos)
- [ ] 5. A Culpa Não É Sua (3 blocos com subtítulos personalizados ao nicho, 3 situações + absolvição + 2-3 revelações)
- [ ] 6. Faça as Contas (2 cenários numéricos + linha de impacto) OU substituição declarada se produto emocional
- [ ] 7. Centro da Atenção (elemento físico + 8 elementos ao redor)
- [ ] 8. Dinâmica de Acesso (2 versões A/B, 3 ou 5 passos com título ultra curto)
- [ ] 9. Demonstração (peça visual real ou placeholder declarado, com regras de acolhimento se tema sensível)
- [ ] 10. Quem É o Especialista (entrevista em 3 blocos, 3 parágrafos, fechamento no Quadro)
- [ ] 11. Depoimentos mínimo 10 reais em 5 categorias com comprovação visual (ou avisos claros se sem prints)
- [ ] 12. Entregáveis Complementares (30 sugestões em 3 categorias, escolha 4-5, nomes próprios, ancoragem 5x a 10x)
- [ ] 13. Resumo da Ópera (lista ultra resumida + soma riscada + preço real + frase de retorno + mini depoimento)
- [ ] 14. FAQ mínimo 12 perguntas (4-5 acesso + 7-8 produto), sem excluir outro perfil de comprador
- [ ] CTA Final entre seção 14 e footer (headline = Quadro)
- [ ] CTA Flutuante Mobile = Quadro adaptado
- [ ] Detalhes processuais de cada seção lidos em `.claude/skills/paginas/references/categoria-padrao-lt.md`

**Regras de conteúdo (todas as estruturas):**
- [ ] Todos os CTAs usam variações do Quadro (zero "Comprar agora", "Saiba mais")
- [ ] Todos os pontos de preço têm ancoragem riscada (preço + R$200)
- [ ] "Acesso vitalício" (ou prazo) em todos os pontos de preço
- [ ] Suporte aparece como card ao lado da garantia (estruturas A a D) ou como seção 17 (Estrutura E)
- [ ] Última frase de "Quem Sou" / "Quem É" conclui no Quadro

**Regras de design:**
- [ ] Mínimo 4 tipos de fundo diferentes
- [ ] Pelo menos 2 seções com imagem de fundo (overlay)
- [ ] Grid 2 colunas em entregáveis (nunca 3)
- [ ] Todas as fontes sans-serif
- [ ] Texto pt-BR com acentos corretos

Após salvar: "Pronto. Sua página foi salva em `[caminho]`. Abra no navegador para visualizar."

---

### 7. Próximo Passo

Sugerir: `/copy-anuncio` para criar anúncios que levam tráfego para essa página.
