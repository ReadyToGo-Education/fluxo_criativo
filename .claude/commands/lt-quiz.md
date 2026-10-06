---
name: workshop-marketing:quiz
description: Gerar quiz de vendas completo para o Low Ticket. 10 perguntas (estrutura SPIN) + prompt técnico para o Lovable.dev, entregues em um único arquivo .md pronto para colar.
---

# Quiz de Vendas. Low Ticket

Gera **um único arquivo** com tudo em sequência:
- Perguntas do quiz (Tela de Entrada + 10 perguntas SPIN com prompts de imagem e tipos variados)
- Prompt técnico completo para o Lovable.dev (com as perguntas já embutidas no formato técnico)

O arquivo é salvo em `meus-produtos/{ativo}/entregas/quiz/quiz-[produto].md` e está pronto para colar diretamente no Lovable.dev.

## Usage

```
/quiz
```

---

## Princípios de Comportamento

### O que é o quiz nesse contexto

O quiz é a ponte entre o anúncio e a venda do produto de entrada (Low Ticket). O lead responde exatamente 10 perguntas sobre sua situação atual, dores e desejos, recebe um "diagnóstico personalizado" e é direcionado para a página final com a oferta do produto.

### Foco correto

- ✅ Todas as perguntas falam sobre o **público**. dores, desejos, situação atual
- ❌ Nunca falam sobre o produto, funcionalidades ou características
- ❌ Sem perguntas óbvias, abstratas ou sem propósito estratégico

### Light Copy (SEMPRE)

- Argumentativo, objetivo e lógico
- Conversacional. parece conversa, não venda
- Sem ponto de exclamação
- Sem "sem X", "não precisa", "mesmo que". em nenhuma forma
- Sem clichês: "segredo que ninguém te contou", "revolucionário", "milagroso"

---

## FASE 0 — VERIFICAÇÃO: QUIZ É O FORMATO CERTO?

Antes de começar, aplique o framework de decisão com base no perfil do produto. Leia `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md).

| Critério | Aponta para QUIZ | Aponta para PÁGINA |
|---|---|---|
| Tipo de produto | Emocional / dor / identificação | Prático / ferramenta / direto ao ponto |
| Nível de consciência do lead | Não sabe que tem problema | Já sabe o que quer |
| Complexidade da decisão | Precisa diagnosticar / explicar | Decisão simples e direta |
| Faixa de preço | Até R$47 | Acima de R$97 |
| Tipo de público | Emocional | Analítico / pragmático |

**Regra:** 2 ou mais critérios para PÁGINA — informe o usuário e sugira `/paginas-low-ticket` antes de continuar. Desempate: seguir com QUIZ.

Se o quiz for confirmado como formato correto (ou o usuário insistir), continue para a Fase 1.

---

## FASE 1 — PERGUNTAS DO QUIZ

### 1. Contexto

Leia `meus-produtos/.ativo`, depois `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md).

Se `perfil.md` não existir, oriente a usar `/produto-concepcao` primeiro.

Use o Quadro, Furadeira, Urgências Ocultas, Decorados e público do resumo para gerar as perguntas.

### 2. Entrevista (máximo 2 perguntas)

Pergunte apenas o que NÃO está no perfil:

- Se o **Quadro** não estiver no perfil: "Qual resultado final o cliente conquista com esse produto? (ex: Perder 5kg em 21 dias)"
- Se o **preço do produto** não estiver claro: "Qual o preço do produto low ticket? (ex: R$ 47)"

Se ambos estiverem no perfil, pule direto para a confirmação.

**Confirmação antes de gerar:**

```
Resumo do que vou criar:
- Produto: [nome]
- Quadro: [transformação]
- Público: [descrição resumida]
- Preço: R$ [valor]
- Total: 10 perguntas (fixo)

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 3. Geração das Perguntas

Gere tudo em sequência, sem pausas entre blocos.

---

#### TIPOS DE PERGUNTA DISPONÍVEIS

O quiz pode usar 5 tipos de pergunta diferentes. Variar os tipos ao longo do quiz torna a experiência mais dinâmica e aumenta o engajamento. Use o tipo mais adequado para o objetivo de cada pergunta.

**Tipo 1. Múltipla escolha** (padrão)
- 4 opções com emoji, clicar em uma opção já avança para a próxima
- Ideal para: situação, problema, necessidade, diagnóstico

**Tipo 2. Calculadora**
- O lead digita valores em 2 campos e clica em "Calcular"
- A tela exibe o resultado calculado com destaque visual antes de avançar
- Ideal para: revelar uma implicação concreta (ex: valor real da hora de trabalho)
- Formato de saída:
```
Campo 1: [label] (unidade: R$, horas, kg, etc.)
Campo 2: [label] (unidade)
Fórmula: [campo1 / campo2] ou [campo1 × campo2]
Texto do resultado: "[Template com {resultado} interpolado]"
Botão após calcular: "Entendi, continuar →"
```

**Tipo 3. Slider**
- Barra deslizante de 1 a 10 com labels nos extremos
- Ideal para: autopercepção, confiança, urgência subjetiva
- Formato de saída:
```
Mínimo (1): [label do extremo negativo]
Máximo (10): [label do extremo positivo]
Valor salvo: [nome do campo no banco]
```

**Tipo 4. Sim/Não**
- Dois botões grandes, ícone ✅ e ❌
- Ideal para: confirmar comportamento direto, gerar comprometimento
- Clicar já avança

**Tipo 5. Input numérico**
- Campo de digitação com label e unidade
- Ideal para: coletar valor de referência que será usado em cálculo posterior
- Formato de saída:
```
Label: [texto do campo]
Unidade: [R$, horas, kg, etc.]
Chave de banco: [nome_do_campo]
```

---

**Regras de uso dos tipos:**
- A **Calculadora** deve aparecer **obrigatoriamente** em pelo menos uma pergunta de Implicação. é onde o lead confronta um dado numérico real sobre sua situação
- O **Slider** deve aparecer em pelo menos uma pergunta de Problema ou Necessidade
- **Sim/Não** deve ser usado em perguntas de resposta direta, não em perguntas de nuance
- Nunca usar mais de 2 perguntas do mesmo tipo em sequência (exceto múltipla escolha)
- No prompt técnico para o Lovable.dev: incluir a estrutura de dados de cada tipo na Seção 5 (Quiz), com os campos específicos de cada question type

---

#### ESTRUTURA DAS 10 PERGUNTAS (SPIN)

O quiz segue a metodologia SPIN de forma adaptada para diagnóstico de vendas:

| Posição | Fase SPIN | Pergunta | Tipo sugerido |
|---|---|---|---|
| P1 | Segmentação | Tela de Entrada (com fotos) | Múltipla escolha |
| P2 | Situação | Contexto atual. comportamento e realidade | Calculadora ou Input numérico |
| P3 | Situação | Contexto secundário. confirmação da situação | Múltipla escolha |
| P4 | Problema | Dor cotidiana direta | Sim/Não ou Múltipla escolha |
| P5 | Problema | Comportamento-problema mais recorrente | Múltipla escolha |
| P6 | Implicação | Consequência concreta da situação (calculada ou visual) | Calculadora |
| P7 | Implicação | Reação ao resultado. aprofundamento da tensão | Slider ou Múltipla escolha |
| P8 | Necessidade | Visualização Profunda (cenas cotidianas transformadas) | Múltipla escolha |
| P9 | Necessidade | O que precisa para mudar. comprometimento | Múltipla escolha |
| P10 | Diagnóstico Final | Síntese que conecta ao Quadro do produto | Múltipla escolha |

**Regra da Calculadora na Implicação (P6):**
A Pergunta 6 deve preferencialmente usar o tipo Calculadora para criar um confronto com dado real. Para produtos de precificação: `preço por leitura ÷ horas dedicadas = valor da hora`. Para outros nichos: adaptar com um cálculo equivalente que revele o custo da inação.

---

#### TELA DE ENTRADA + PERGUNTA 1

A Tela de Entrada e a Pergunta 1 são a **mesma tela**. O lead vê headline, subheadline e tempo estimado. e já responde a primeira pergunta sem botão intermediário. As opções funcionam como "Começar Agora".

**Regras da Headline:**

Combina obrigatoriamente: **resultado específico + número concreto + prazo realista**

A headline fala **somente sobre o que o lead ganha**.

- ✅ "Elimine até 5kg nos próximos 7 dias"
- ✅ "Prepare seu corpo para um parto mais seguro em 4 semanas"
- ❌ "Emagreça sem fazer dieta" / "Elimine 5kg sem passar fome"
- ❌ Vaga: "Quando o corpo e a mente vivem em alerta..."
- ❌ Quiz como fim: "Diagnóstico financeiro do casal"
- ❌ Clichês: "segredo que ninguém te contou", "método revolucionário", "milagroso"

Teste interno: "Uma pessoa cética leria isso e pensaria que é enrolação?" Se sim, reescreva.

**Regras da Pergunta 1:**

- Segmentação leve: faixa etária, gênero ou situação atual
- Não filtra ninguém. o quiz continua para todas as opções
- Clicar na opção já avança (sem botão separado)

**Prompts de imagem para cada opção:**

- Pessoa que o lead se vê. não modelo genérico
- Expressão aspiracional ou de forte identificação emocional (sorridente, confiante, presente)
- Fundo neutro desfocado, foco no rosto
- Fotorrealista, iluminação natural, sem texto sobreposto
- ❌ Proibido: expressão neutra, posada demais ou imagem genérica de banco de fotos

Formato do prompt:
> "Fotografia realista de [pessoa correspondente ao perfil da opção], expressão [aspiracional/confiante], fundo neutro desfocado, iluminação natural, qualidade fotográfica profissional, sem texto."

**Formato de saída:**

```
🖥️ TELA DE ENTRADA + PERGUNTA 1

📌 Headline: [resultado + número + prazo]
📌 Subheadline: [o que vai descobrir + reforço de personalização]
⏱️ Leva apenas 2 minutos para responder

❓ [Pergunta de segmentação leve]

A) [opção] → 🖼️ Prompt: "[prompt de imagem]"
B) [opção] → 🖼️ Prompt: "[prompt de imagem]"
C) [opção] → 🖼️ Prompt: "[prompt de imagem]"
D) [opção] → 🖼️ Prompt: "[prompt de imagem]"

⚠️ Por que essa headline converte: [2 linhas]
```

---

#### S. SITUAÇÃO (Perguntas 2 e 3)

Mapeiam a realidade atual do lead. o que ele faz, como opera, qual é o ponto de partida. **Exatamente 2 perguntas.**

- Ancora em comportamento concreto e mensurável
- Não carregam julgamento. apenas descrevem
- P2 preferencialmente usa **Calculadora** ou **Input numérico** para capturar um dado real que será usado na Implicação

---

#### P. PROBLEMA (Perguntas 4 e 5)

Revelam a dor cotidiana. o que incomoda, o que trava, o comportamento problemático. **Exatamente 2 perguntas.**

- Ancora a dor em algo específico, físico ou cotidiano
- Cada opção descreve uma realidade diferente e reconhecível. não sinônimos do mesmo estado emocional
- P4 funciona bem com **Sim/Não** para gerar comprometimento direto

---

#### I. IMPLICAÇÃO (Perguntas 6 e 7)

Amplificam a consequência da situação-problema. Revelam o custo real de não resolver. **Exatamente 2 perguntas.**

- **P6 deve usar obrigatoriamente o tipo Calculadora**. o lead confronta um número real derivado das respostas S
- P7 aprofunda a tensão gerada pela calculadora com **Slider** ou múltipla escolha sobre como o lead se sente diante do resultado

---

#### N. NECESSIDADE (Perguntas 8 e 9)

Movem o lead da dor para o desejo. o que ele quer, o que precisa para mudar. **Exatamente 2 perguntas.**

- **P8 é obrigatoriamente a Pergunta de Visualização Profunda:**
  Formato: "Imagine que daqui a [prazo], você já [resultado do Quadro]. O que mudou primeiro na sua vida?"
  Opções: cenas concretas do cotidiano transformado. nunca estados emocionais genéricos.
  - ✅ "Visto uma roupa guardada há 2 anos" / "Meu filho me pergunta por que estou tão bem-humorada"
  - ❌ "Me sinto mais feliz e realizada"
- P9 mapeia o que o lead precisa para agir agora

---

#### DIAGNÓSTICO FINAL (Pergunta 10)

Pergunta síntese que conecta diretamente ao Quadro do produto. Prepara o lead para a Tela de Resultado. **Exatamente 1 pergunta, tipo múltipla escolha.**

---

**Contagem obrigatória: P1 (segmentação) + S (2) + P (2) + I (2) + N (2) + Diagnóstico (1) = 10 perguntas. Nunca mais, nunca menos.**

**Formato de cada pergunta (2 a 10). adaptar conforme o tipo:**

```
**Pergunta [número]. [Fase SPIN]**
🎯 Objetivo: [em uma linha]
📐 Tipo: [multipla_escolha | calculadora | slider | sim_nao | input_numero]
❓ [Texto da pergunta]

[Se múltipla escolha ou sim/não:]
A) [opção concreta e distinta]
B) [opção concreta e distinta]
C) [opção concreta e distinta]
D) [opcional]

[Se calculadora:]
Campo 1: [label] (unidade: [unidade])
Campo 2: [label] (unidade: [unidade])
Fórmula: [campo1 / campo2] ou outra operação
Texto do resultado: "[Template com {resultado}]"
Botão após calcular: "Entendi, continuar →"

[Se slider:]
Mínimo (1): [label]
Máximo (10): [label]
Chave: [nome_no_banco]

[Se input numérico:]
Label: [texto]
Unidade: [R$, horas, etc.]
Chave: [nome_no_banco]
```

---

#### TELA DE RESULTADO

Gere a Tela de Resultado **na mesma fase das perguntas**, antes do prompt técnico. Ela é entregue junto com as perguntas no mesmo arquivo.

A Tela de Resultado aparece depois da última pergunta do quiz e entrega o "diagnóstico personalizado" ao lead, validando a dor e fazendo a ponte para a página de vendas.

**Estrutura obrigatória:**

1. **Título do diagnóstico**. igual para todos, resume o que o quiz revelou
2. **Mensagem condicional**. varia conforme a resposta da Pergunta 1 (segmentação), personaliza o diagnóstico para o perfil da pessoa
3. **Parágrafo final**. igual para todos, valida que existe solução direta e prepara para a oferta
4. **CTA**. botão que leva para a página de vendas

**Regras:**
- O título deve nomear o problema central revelado pelo quiz, sem clichê e sem ponto de exclamação
- Cada mensagem condicional deve falar da realidade específica daquele perfil. não variações do mesmo texto
- O parágrafo final nunca deve mencionar o produto diretamente. apenas abrir a porta para a solução
- O CTA deve ser uma ação natural, não um grito de venda

**Formato de saída:**

```
🖥️ TELA DE RESULTADO

📌 Título: [diagnóstico central. igual para todos]

👤 Mensagem para quem respondeu A (Pergunta 1):
[texto personalizado]

👤 Mensagem para quem respondeu B:
[texto personalizado]

👤 Mensagem para quem respondeu C:
[texto personalizado]

👤 Mensagem para quem respondeu D:
[texto personalizado]

📌 Parágrafo final (igual para todos):
[validação + abertura para a solução]

→ CTA: "[texto do botão]"
```

---

#### RESUMO FINAL DAS PERGUNTAS

```
📊 RESUMO DO QUIZ

- Tela de Entrada + Pergunta 1 + Prompts de Imagem: ✅
- S. Situação: perguntas 2 e 3 (2 perguntas)
- P. Problema: perguntas 4 e 5 (2 perguntas)
- I. Implicação: perguntas 6 e 7 (2 perguntas, P6 obrigatoriamente Calculadora)
- N. Necessidade: perguntas 8 e 9 (2 perguntas, P8 obrigatoriamente Visualização Profunda)
- Diagnóstico Final: pergunta 10 (1 pergunta)
- Tela de Resultado: ✅
- Total: 10 perguntas
- Tipos usados: [listar quais tipos foram aplicados em cada pergunta]

🎯 Lógica de conversão: [2 linhas]
```

---

#### PÁGINA FINAL DE OFERTA

Após gerar a Tela de Resultado, gere também a **copy da Página Final de Oferta**. ainda na Fase 1, entregue no mesmo arquivo.

A Página Final é a página de vendas que aparece depois da Tela de Resultado. É onde o lead compra o produto.

**Estrutura obrigatória (11 blocos). SEM vídeo:**

1. **Headline com premissas**. resultado específico + premissa que valida o diagnóstico do quiz
2. **Subheadline**. reforço da dor ou desejo central
3. **Quadro Comparativo Antes x Depois**. máximo 3 linhas, só os contrastes mais fortes
4. **Valor e Botão de Checkout #1**
5. **Entregáveis**. para cada item: nome, benefícios práticos, resumo simples do que é, suporte (se houver)
6. **Valor e Botão de Checkout #2**
7. **Bônus**. para cada bônus: nome, benefícios, explicação do conteúdo
8. **Valor e Botão de Checkout #3**
9. **Garantia**
10. **Autoridade do Criador**. nome, experiência; depoimentos/provas sociais indicados como **[IMAGEM. inserir print aqui]** (nunca em texto corrido)
11. **Valor e Botão de Checkout #4**. última chamada

> ⚠️ A Página Final de Oferta do quiz **não tem seção de vídeo**. O lead já foi aquecido pelo quiz.

**Regras:**
- **Copy direta e curta.** Frases curtas, parágrafos de no máximo 2-3 linhas. Sem rodeios, sem repetição de argumento. O lead já passou pelo quiz inteiro, então a página final vai direto ao ponto.
- **Quadro Comparativo: máximo 3 linhas.** Escolher os 3 contrastes mais impactantes entre a situação atual e o resultado. Menos é mais.
- Produto obrigatoriamente entre R$37 e R$97
- Formatos permitidos: e-book, guia, planilha, desafio, mini-curso, agente GPT
- Depoimentos/provas sociais SEMPRE indicados como imagem. nunca transcritos como texto
- Copy no estilo Light Copy. argumentativa, lógica, conversacional, sem ponto de exclamação
- O link de checkout aparece em todos os 4 botões

**Dados a coletar antes de gerar (pergunte UMA por vez o que não estiver no perfil):**
- Entregáveis detalhados (nome + benefícios + resumo)
- Suporte incluso?
- Bônus?
- Garantia
- Autoridade do criador (nome + experiência)
- Depoimentos/provas sociais (prints ou descrição. serão indicados como imagem)
- Link de checkout

**Formato de saída:**

```
📄 PÁGINA FINAL DE OFERTA

**[Headline com premissas]**

[Subheadline]

---

📊 ANTES × DEPOIS (máximo 3 linhas)

| Antes | Depois |
|---|---|
| [dor concreta #1] | [resultado concreto #1] |
| [dor concreta #2] | [resultado concreto #2] |
| [dor concreta #3] | [resultado concreto #3] |

---

💳 [Preço]. [Botão de Checkout #1]

---

📦 O QUE VOCÊ RECEBE

[Nome do entregável]
- [Benefícios]
- [Resumo simples]
[Suporte, se houver]

---

💳 [Preço]. [Botão de Checkout #2]

---

🎁 BÔNUS

[Nome do bônus]
- [Benefícios]
- [O que entrega]

---

💳 [Preço]. [Botão de Checkout #3]

---

🛡️ GARANTIA
[Texto da garantia]

---

👤 QUEM CRIOU
[Nome]. [Experiência]

📸 DEPOIMENTOS
[IMAGEM. inserir print aqui]
[IMAGEM. inserir print aqui]
[IMAGEM. inserir print aqui]

---

💳 [Preço]. [Botão de Checkout #4. última chamada]
```

---

### 4. Aprovação

```
Quiz completo gerado (perguntas, diagnóstico e página de oferta).

1. Aprovar e gerar o arquivo final
2. Quero ajustar algo
```

### 5. Gerar e Salvar o Arquivo Único

Após aprovação, gere o conteúdo completo do zero com base no produto do aluno.

Gere um **único arquivo** que contém, em sequência:
1. As perguntas do quiz (com prompts de imagem, tipos de pergunta e valores de banco)
2. O prompt técnico completo para o Lovable.dev

As perguntas já devem estar embutidas dentro do prompt técnico (Seção 5. Quiz), com os prompts de imagem da P1 incluídos diretamente no campo `image_prompt` de cada opção.

Substitua todo o conteúdo do exemplo do curso de francês pelo produto do aluno, mantendo a estrutura técnica intacta. Adapte seção por seção:

**Seção 4. LANDING PAGE:**
- Título H1: use a headline gerada
- Subtítulo: use a subheadline gerada
- Botão CTA: texto adequado ao produto (ex: "Começar o Diagnóstico →")
- Remova o emoji 🇫🇷 e referências à Paris. substitua por fundo adequado ao nicho
- Texto "⏱ Leva menos de 2 minutos". manter

**Seção 5. QUIZ:**
- Substitua as 5 perguntas do exemplo pelas 10 perguntas geradas (estrutura SPIN)
- Para cada pergunta, inclua o campo `type` com o tipo de pergunta (`multipla_escolha`, `calculadora`, `slider`, `sim_nao`, `input_numero`)
- Para perguntas do tipo `calculadora`: incluir campos, fórmula e template de resultado
- Para perguntas do tipo `slider`: incluir min, max, labels e chave
- Para perguntas do tipo `multipla_escolha`: manter formato `{ label, emoji, value }`
- P1: incluir campo `image_prompt` em cada opção (prompts de imagem embutidos)
- Adapte o mapeamento de values para labels legíveis (Tab RESPOSTAS)
- Atualize o `last_step` para `quiz_pergunta_1` até `quiz_pergunta_10`

**Seção 6. TELA DE RESULTADO:**
- Substitua as mensagens condicionais pelo nicho do produto
- Adapte título e subtítulo para refletir o Quadro do produto
- Mantenha a lógica condicional baseada na resposta da Pergunta 1

**Seção 7. PÁGINA DE VENDAS:**
- Hero: substitua Paris por fundo do nicho; remova referências ao francês
- Badge: "✅ Método validado por +[X] alunos". número realista
- H1: use o Quadro do produto
- Barra de prova social: adapte os 4 itens para o produto
- Seção Benefícios: use 8 Decorados principais
- Depoimentos: placeholders marcados como "[Substituir por depoimento real]"
- Seção de Oferta: preço real do produto; sem seção de vídeo
- Sem seção de vídeo na Página Final

**Seção 8. MODAL DE PRÉ-CHECKOUT:**
- Adapte título e descrição para o produto
- Manter os 3 campos (nome, email, telefone)

**Seção 9. PAINEL ADMINISTRATIVO:**
- Header: substitua pelo nome do produto
- Adapte labels das etapas para 10 perguntas (P1 a P10)
- Tab RESPOSTAS: 10 colunas com scroll horizontal
- Tab PERFORMANCE: 14 etapas (landing + 10 perguntas + resultado + vendas + checkout)

**Banco de dados e tracking:**
- Manter tabelas `leads` e `funnel_events` como no template
- Atualizar `last_step` para refletir 10 perguntas

**Design System:**
- Manter paleta original (azul marinho, dourado, creme). universal para qualquer nicho
- Só trocar paleta se o nicho exigir (ex: saúde infantil, moda feminina)

Salve o arquivo em:

`meus-produtos/{ativo}/entregas/quiz/quiz-[produto].md`

### 6. Entrega + Captura do Link do Lovable + Registro no Painel

Após salvar o arquivo `.md` do prompt, **NÃO encerre o fluxo**. O quiz só está completo quando o link publicado no Lovable também estiver registrado, para o painel de entregas exibir os dois.

Logo depois de salvar o prompt, e antes do Passo 6.1, rode em silêncio `python3 scripts/painel-incremental.py --secao low-ticket` (no Windows, `py -3` quando `python3` não responder). Assim o prompt já aparece na aba Low Ticket do painel quando o aluno for copiar.

> **Princípio de comunicação:** o aluno SÓ INTERAGE pelo chat. Em nenhuma mensagem visível ao aluno mencione `quiz-meta.json`, `perfil.md`, `painel-incremental.py`, "rode no terminal", "edite o arquivo" ou qualquer detalhe técnico de bastidor. Esses arquivos existem nos bastidores e o agente cuida deles silenciosamente. Para o aluno, só existem: o painel de entregas (que ele abre no navegador) e o chat (onde ele fala comigo).

**Passo 6.1. Confirmar que o prompt foi salvo (mensagem visível ao aluno):**

```
✅ Quiz pronto. Para gerar o funil:

1. Abra https://lovable.dev em uma aba nova
2. Copie todo o conteúdo do prompt: no painel de entregas, aba Low Ticket, clique em "Abrir prompt"
3. Cole no chat do Lovable e aguarde gerar
4. Quando terminar, volte aqui e me mande o link do quiz publicado
```

**Passo 6.2. Pedir o link do quiz publicado:**

Pergunte de forma direta:

```
Você já tem o link do quiz que o Lovable gerou?

Se sim, é só colar aqui no chat (ex: https://desafio-cura-coracao.lovable.app).
Se ainda não publicou, é só responder "ainda não". Quando publicar, é só voltar aqui no chat e me mandar o link, que eu atualizo o painel automaticamente.
```

**Comportamento esperado do agente:**

- Se o aluno responder com um texto que começa com `http://` ou `https://` (em qualquer momento da conversa, mesmo depois de horas/dias): tratar como link novo do quiz, sobrescrever os arquivos automaticamente e reconstruir o painel. Não pedir confirmação.
- Se o aluno responder "ainda não", "não publiquei", "depois", ou similar: registrar como pendente e seguir.
- **Nunca** peça ao aluno para editar arquivo, abrir arquivo, rodar script ou qualquer coisa fora do chat. Tudo é resolvido pelo agente nos bastidores.

**Passo 6.3 a 6.5. Bastidores do agente (silencioso, NÃO mostrar nada disso ao aluno):**

Após capturar o link (ou registrar como pendente), o agente faz silenciosamente:

1. Salva os metadados do quiz em `meus-produtos/{ativo}/entregas/quiz/quiz-meta.json` (estrutura: `prompt_path`, `lovable_url`, `generated_at`, `url_updated_at`, `produto_nome`, `produto_slug`)
2. Faz upsert da seção `## Quiz` no `perfil.md` (campos `_prompt`, `_lovable_url`, `_meta`, `_atualizado`)
3. Roda `python3 scripts/painel-incremental.py --secao low-ticket` (no Windows, `py -3` quando `python3` não responder) para atualizar a aba Low Ticket do painel

A aba Low Ticket mostra o card do quiz lendo o JSON: o link publicado (ou o aviso de pendente) e o prompt. Tudo isso é invisível para o aluno, ele só vê a mensagem do passo 6.6.

**Passo 6.6. Confirmação final ao aluno (UMA mensagem curta, sem mencionar arquivos internos):**

Se o aluno colou um link válido:
```
✅ Link salvo no painel de entregas. O card do quiz agora mostra: {link}

Próximo passo: /copy-anuncio para criar os anúncios que vão direcionar tráfego para o quiz.
```

Se ainda não publicou:
```
✅ Quiz registrado no painel como pendente.

Quando publicar no Lovable, é só voltar aqui no chat e me mandar o link. Eu atualizo o painel automaticamente.

Próximo passo: /copy-anuncio para criar os anúncios que vão direcionar tráfego para o quiz quando estiver no ar.
```

---

## Nunca Faça

❌ Headline com "sem", "não precisa", "mesmo que", "mesmo sem". de nenhuma forma
❌ Headline sem número concreto e prazo específico
❌ Clichês: "segredo que ninguém te contou", "revolucionário", "milagroso"
❌ Opções semanticamente parecidas (sinônimos do mesmo estado emocional)
❌ Perguntas abstratas sem ancoragem cotidiana
❌ Quiz sem pergunta de visualização profunda (obrigatória em N. P8)
❌ Quiz sem Calculadora na fase I (obrigatória em P6)
❌ Todas as perguntas do mesmo tipo (variar os tipos é regra)
❌ Mais de 2 perguntas do mesmo tipo em sequência (exceto múltipla escolha)
❌ Prompts de imagem genéricos ou neutros na Pergunta 1
❌ Separar Pergunta 1 da Tela de Entrada
❌ Expor o produto antes da página final
❌ Número diferente de 10 perguntas (nem mais, nem menos)
❌ Coletar dados dentro do quiz (só no modal de pré-checkout)
❌ Alterar a estrutura técnica do template (tabelas, tracking, componentes). só substituir conteúdo
