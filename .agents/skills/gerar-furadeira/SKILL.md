---
name: gerar-furadeira
description: Apoio tecnico para o command /gerar-furadeira. Decide automaticamente qual das 6 mecanicas (ou combinacao) faz mais sentido para o produto ativo e gera a Furadeira no perfil.md aplicando o teste de eficiencia. Sem entrevista, gera tudo a partir do contexto ja existente.
---

# Skill. Gerar Furadeira (Texto Estruturado)

Apoio técnico do command `/gerar-furadeira`. A skill decide a mecânica, gera a estrutura, sugere o nome do método, mapeia a eficiência e salva no `perfil.md`. Sem entrevista. O aluno só aprova ou ajusta no final.

Coexiste com `/furadeira-visual`, que lê a Furadeira gerada por aqui e produz o prompt para o ChatGPT desenhar a imagem.

## Pré-requisitos de contexto

Antes de gerar, a skill PRECISA ter acesso a estes 3 arquivos do produto ativo:

- `meus-produtos/{ativo}/perfil.md` (Quadro, Decorados, Urgências Ocultas, 3 Identidades, Argumentos Incontestáveis)
- `meus-produtos/{ativo}/idconsumidor.md` (perfil do comprador, paliativos, objeções, frases que público diria)
- `meus-produtos/{ativo}/pesquisa-mercado.md` (concorrentes, ângulos, biblioteca de anúncios)

Se faltar um desses, parar e redirecionar para `/produto-concepcao`. Não tentar adivinhar do nada.

## As 6 Mecânicas (decisão automática)

A skill cruza sinais do contexto e escolhe 1 mecânica principal (e às vezes 1 complementar). Detalhamento completo das mecânicas em `.claude/skills/furadeira-visual/references/6-mecanicas.md`.

### Tabela de decisão

Aplicar nesta ordem. A primeira regra que casar define a mecânica principal. Se duas casarem com força similar, registra uma como principal e a outra como complementar.

| Sinal no contexto | Mecânica principal |
|---|---|
| Quadro tem prazo definido (ex: "em 90 dias", "em 6 meses") OU Quadro descreve uma progressão clara (ex: "do iniciante ao avançado") | **Fases e Sequências** |
| `idconsumidor.md` lista 2 ou mais perfis de comprador com necessidades opostas (ex: "iniciante vs avançado", "mãe de criança reativa vs passiva") E o protocolo muda conforme o perfil | **Lógica Condicional** |
| `idconsumidor.md` mostra que o aluno precisa primeiro se identificar com uma categoria antes de seguir o método (ex: "qual o seu temperamento?", "qual o seu tipo?") | **Enquadramento** |
| `perfil.md` lista 3 a 7 Argumentos Incontestáveis ou pilares que precisam coexistir para o resultado funcionar | **Listas** |
| `idconsumidor.md` ou `pesquisa-mercado.md` mostram que o público tenta sozinho e falha por causas específicas (ex: "falta de consistência", "pouco tempo", "medo de errar") | **Empecilhos** (geralmente combinada com Fases) |
| O resultado do Quadro depende de repetição diária ou hábito (ex: "leitura diária", "30 min por dia", "toda segunda e quinta") | **Dinâmica de Entrega** (geralmente combinada com Fases) |
| Nenhum sinal forte | **Fases e Sequências** (default) |

### Combinações comuns

- **Fases + Empecilhos**: produto com público que falha sozinho. Cada fase ataca um empecilho.
- **Fases + Dinâmica de Entrega**: produto que depende de hábito. As fases são a progressão; o ritual é a marca.
- **Condicional + Enquadramento**: produto com perfis distintos. O enquadramento classifica, a lógica condicional ramifica.
- **Listas + Fases**: produto com pilares que precisam ser instalados em ordem.

Limite: no máximo 2 mecânicas combinadas. Mais que isso vira complexidade desnecessária.

## Geração da Furadeira por mecânica

A estrutura no `perfil.md` muda conforme a mecânica. Não force "macroetapas + microetapas" sempre.

### Fases e Sequências
- 3 a 5 fases ordenadas, cada uma com:
  - Nome da fase (curto, ação ou estado)
  - 1 frase descrevendo o que acontece nela
  - 2 a 4 microetapas (ações práticas)
  - 1 forma de eficiência (das 14)
- Inferir as fases a partir dos Decorados (cada Decorado é um benefício; agrupe por estágio do progresso) e Urgências Ocultas (Dores no início, Desejos no fim).

### Lógica Condicional
- 1 decisão crítica (ex: "criança reativa, equilibrada ou passiva?")
- 2 ou 3 ramificações, cada uma com:
  - Nome da ramificação
  - Descrição curta de quem se enquadra
  - Protocolo específico (3 a 5 passos)
- 1 método de diagnóstico (questionário, autoavaliação, observação)

### Enquadramento
- Nome do sistema de categorias (próprio, não genérico)
- 3 ou 4 categorias, cada uma com:
  - Nome
  - Características observáveis
  - Protocolo específico ou ajuste de aplicação
- 1 método de diagnóstico

### Listas
- 3 a 7 pilares finitos
- Sugerir acrônimo se as iniciais formarem palavra memorável
- Cada pilar com:
  - Nome
  - 1 frase de explicação
  - 1 forma de eficiência

### Empecilhos
- 3 a 5 empecilhos comuns do nicho (extrair de `idconsumidor.md` e `pesquisa-mercado.md`)
- Para cada empecilho:
  - Nome
  - Por que ele acontece
  - Qual fase do método remove ele
- Geralmente combinada com Fases.

### Dinâmica de Entrega
- Nome do ritual (verbo+ação memorável: "Aperta e Solta", "Liga e Desliga")
- Frequência (diária, semanal, etc.)
- Duração (3 min, 10 min, 30 min)
- Em qual momento (ao acordar, antes de dormir, segunda e quinta)
- O que o aluno faz exatamente
- Por quanto tempo total (4 semanas, 5 semanas)

## Nome do método (7 técnicas)

Sugerir 1 nome principal + 2 alternativas. Cada uma usando uma técnica diferente das 7:

| Técnica | Exemplo |
|---|---|
| Acrônimo | CAVE, VTSD, 3F |
| Nome do Autor | Método {Nome do Aluno} |
| Curioso | Furadeira, Aperta e Solta |
| Impactante | Escudo do Comportamento, Blindagem Financeira |
| Benefício | Fluência em 90 Dias, Zero Dívida em 6 Meses |
| Mistério | Tecnologia de Alinhamento Postural Titanium |
| Número + Substantivo | 3 Pilares, 4 C's, Sistema Tríplice |

Evitar: termos genéricos ("Método Online"), técnicos demais ("Protocolo de Regulação Neuroemocional"), parecidos com o normal ("Curso de Emagrecimento").

## Teste de Eficiência (14 formas)

Para cada componente da Furadeira (cada fase, pilar, ramificação, ritual), mapear qual das 14 formas de eficiência ele entrega. Se um componente não carregar nenhuma, reescrever ou descartar.

| Forma | O que entrega |
|---|---|
| Mais rápido | Reduz o tempo até o resultado |
| Mais barato | Reduz o investimento necessário |
| Menos esforço | Reduz o trabalho ou a dificuldade |
| Menos dor | Reduz o sofrimento ou desconforto |
| Menos erro | Reduz a chance de falhar |
| Menos desperdício | Reduz perda de tempo ou dinheiro |
| Mais adesão | Aumenta a chance de continuar |
| Mais prazeroso | Torna o processo mais agradável |
| Mais ético | Sem atalhos duvidosos |
| Mais bonito | Resultado esteticamente superior |
| Mais sustentável | Resultado duradouro |
| Mais saudável | Menos dano colateral |
| Mais gostoso | Experiência mais satisfatória |
| Menos apelativo | Sem manipulação ou exagero |

Cada componente carrega no mínimo 1, no máximo 2 formas. Mais que isso dilui o argumento.

## Estrutura no perfil.md

A seção "Furadeira (Método)" no `perfil.md` passa a seguir este schema:

```markdown
## Furadeira (Método)

**Nome do método:** {nome principal}
**Mecânica(s):** {principal} + {complementar se houver}
**Eficiência principal:** {qual das 14 formas é o argumento mais forte}

### Estrutura

{conteúdo específico da mecânica, conforme schema acima}

### Eficiência por componente

- {Componente 1}: {forma de eficiência}
- {Componente 2}: {forma de eficiência}
- {...}
```

Mantém os campos antigos `### Macroetapas` e microetapas APENAS se a mecânica for "Fases e Sequências" (compatível com o que `painel-incremental.py` já parseia).

## Erros comuns e como evitar

| Sintoma | Causa | Correção |
|---|---|---|
| Furadeira sai sempre como "Fases" | Não cruzou sinais do idconsumidor | Verificar perfis no idconsumidor antes de decidir |
| Componente sem eficiência | Pulou o teste das 14 formas | Aplicar o teste antes de salvar |
| Nome genérico ("Método Completo") | Não aplicou as 7 técnicas | Sugerir 3 nomes, cada um com técnica diferente |
| Microetapas vagas ("estudar mais") | Não usou os Decorados como insumo | Cada microetapa deve ser ação concreta |
