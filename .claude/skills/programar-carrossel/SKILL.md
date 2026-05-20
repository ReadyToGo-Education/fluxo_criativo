---
name: programar-carrossel
description: Programa uma tarefa recorrente que gera carrossel para Instagram automaticamente, em 1 dos 9 estilos (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia da semana, Curiosidade, Editorial). A tarefa roda na nuvem do Claude via /schedule, na frequência escolhida (diária, semanal, quinzenal, customizada). O resultado aparece no painel de Routines.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
model: sonnet
---

# Programar Carrossel Recorrente

Configura uma tarefa que gera carrossel de Instagram automaticamente, no estilo e frequência escolhidos. A tarefa programada roda na nuvem do Claude (via `/schedule`) e entrega o resultado no painel de Routines, sem depender do computador do aluno estar ligado.

---

## Anúncio inicial

```
🔍 Próximo passo: configurar a tarefa programada de carrossel (entre 6 e 14 perguntas, dependendo do estilo e do modo escolhido). Tempo estimado: 3 a 6 minutos.
```

> Use exatamente esse texto. A faixa "8 a 14" é só uma estimativa de esforço, não um total exato. NÃO mostre total fixo nos cabeçalhos das perguntas: o número real só é conhecido no fim, porque a frequência escolhida no Passo 4 muda a conta. Numere as perguntas em sequência simples: "Pergunta 1", "Pergunta 2", e assim por diante.

---

## REGRA DURA. Não criar worktree

Esta skill grava arquivo de config em `meus-produtos/{ativo}/agendamentos/` (dado do aluno, não código do projeto). **NUNCA chame `EnterWorktree` durante esta skill.** Grave direto no checkout via `Write`.

---

## REGRA DURA. Uma pergunta por turno + progresso visível

Cada pergunta é UM turno separado. Após cada resposta, exiba um **micro-resumo de progresso** antes da próxima pergunta:

```
--- Pergunta {N} concluída ---
{label}: {valor escolhido}
Próximo: {label da próxima pergunta}
---
```

Numere as perguntas em sequência: "Pergunta 1", "Pergunta 2", "Pergunta 3", e assim por diante. NÃO use "de {total}" nos cabeçalhos. O número total de perguntas varia conforme o estilo, o modo de tema e a frequência, e só é conhecido no fim. Prometer um total no começo entrega um número errado.

Quando o estilo escolhido não pede input extra (Sempre, Odeio, Amo), a pergunta da seção 2.3 é pulada: ajuste a numeração das perguntas seguintes para continuar sequencial, sem buraco. Nunca, Curiosidade e Editorial têm ramo próprio (Passos 1.x dedicados) e nem chegam ao 2.3.

PROIBIDO bulkar perguntas no mesmo turno.

PROIBIDO bulkar perguntas no mesmo turno.

---

## Passo 0. Contexto

Leia em paralelo:
- `meus-produtos/.ativo`
- `meus-produtos/{ativo}/perfil.md` (se existir)
- `meus-produtos/{ativo}/idconsumidor.md` (se existir)

Extraia como sugestão (não use ainda):
- **Handle do Instagram.**
- **Nicho.**
- **Produto.**

Sem produto ativo, instrua o aluno a rodar `/produto-novo` e encerre.

---

## Passo 1. Escolha do estilo

Exiba SOMENTE este bloco e pare:

```
Pergunta 1. Estilo do carrossel

Qual estilo você quer programar?

1. Nunca. 5 proibições contraintuitivas + CTA.
2. Sempre. 5 ações contraintuitivas + CTA.
3. Odeio. 5 takes polêmicos defendidos + CTA tribal.
4. Erros. 5 erros que sabotam um desejo + CTA. Precisa do desejo do público.
5. Amo. 5 takes afirmativos defendidos + CTA tribal.
6. Ninguém Conta. 5 verdades ocultas sobre um objetivo + CTA. Precisa do objetivo do público.
7. Notícia da semana. Abre o fluxo /programar-carrossel-noticia (skill própria, configurações extras).
8. Curiosidade. Carrossel a partir de uma curiosidade atemporal do nicho (fato chocante, recorde, dado contraintuitivo). Busca na web a cada execução, 7 a 9 slides.
9. Editorial. Carrossel editorial de 6 slides com narrativa de especialista baseada em notícias reais, pesquisas, polêmicas e contas malucas do nicho. A tarefa gera 10 ideias internamente e escolhe sozinha a mais forte a cada execução. Entrega o prompt único pra colar no ChatGPT.

Digite o número (ou digite "cancelar" para sair).
```

AGUARDE A RESPOSTA. Se a resposta for `cancelar`, `0`, `sair` ou variação clara, encerre. Caso contrário salve como `estilo_carrossel`.

---

## Passo 1.1. Delegação para Notícia

**Se `estilo_carrossel == 7`** (Notícia), informe:

```
Beleza. Notícia tem fluxo próprio porque depende de busca web semanal e tem configurações extras (categoria Trend ou Atemporal, modo aleatório ou fixo, tom travado ou livre).

Vou te direcionar para a skill /programar-carrossel-noticia que cuida disso. Vou passar o que já temos (@, nicho e produto do seu perfil) para você não digitar de novo.
```

Em seguida, invoque a skill `workshop-marketing:programar-carrossel-noticia` via `Skill` tool **passando os dados já extraídos do perfil ativo** (handle, nicho, produto). A skill de Notícia tem que detectar que essas variáveis já estão presentes na sessão e **pular as perguntas 1.1, 1.2 e 1.3** se elas tiverem valor (mostrar como sugestão "1. Sim ({valor})" em vez de pedir tudo de novo).

**Encerre esta skill aqui**. A skill de Notícia toma conta do resto.

**Se `estilo_carrossel` está entre 1 e 6**, prossiga para o Passo 2.

**Se `estilo_carrossel == 8` (Curiosidade)**, prossiga para o Passo 1.2.

**Se `estilo_carrossel == 9` (Editorial)**, prossiga para o Passo 1.3.

---

## Passo 1.2. Ramo Curiosidade

O estilo Curiosidade é atemporal, mas tem fluxo próprio: a tarefa programada busca uma curiosidade na web a cada execução e escolhe o tema sozinha. Não há modo FIXO, não há Desejo nem Objetivo. Em relação ao fluxo dos 6 estilos atemporais, valem estas diferenças:

1. **Passo 2.1 e 2.2** (@ do Instagram, nicho e produto): iguais aos atemporais, execute normalmente.
2. **Passo 2.3** (input extra Desejo/Objetivo): não se aplica, pule.
3. **Passo 2.4** (tom): use a **versão Curiosidade** da pergunta de tom (ver o bloco "Se Curiosidade" na seção 2.4).
4. **Passo 3** (modo de geração de tema): não se aplica, pule o Passo 3 inteiro. Salve `modo_geracao = AUTO_WEB`.
5. **Passo 4** (frequência e horário): igual aos atemporais.
6. **Passo 5** (confirmação): igual, com a linha específica de Curiosidade no preview.
7. **Passo 6** (montar prompt): não use o `prompts-routine.md`. Use `references/prompt-curiosidade-routine.md` (ver o bloco "Se Curiosidade" no Passo 6).

Siga agora para o Passo 2.

---

## Passo 1.3. Ramo Editorial

O estilo Editorial é atemporal, mas tem fluxo próprio: a tarefa programada gera 10 ideias internamente e escolhe sozinha a mais forte a cada execução. Não há modo FIXO, não há tom (o tom de especialista/newsletter é parte do estilo), não há Desejo nem Objetivo, mas tem 2 dados próprios (público e tipo de CTA). Em relação ao fluxo dos 6 estilos clássicos, valem estas diferenças:

1. **Passo 2.1 e 2.2** (@ do Instagram, nicho e produto): iguais aos clássicos, execute normalmente. O `nicho_produto` será interpretado como "produto/serviço" pelo prompt Editorial.
2. **Passo 2.3** (Erros/Ninguém Conta): não se aplica, pule.
3. **Passo 2.3.E** (extras de Editorial): execute as 2 perguntas adicionais (público e tipo de CTA), ver o bloco "Se Editorial" no fim da seção 2.3.
4. **Passo 2.4** (tom): não se aplica, pule. Editorial não usa tom variável.
5. **Passo 3** (modo de geração de tema): não se aplica, pule o Passo 3 inteiro. Salve `modo_geracao = AUTO_INTERNAL`.
6. **Passo 4** (frequência e horário): igual aos clássicos.
7. **Passo 5** (confirmação): igual, com a linha específica de Editorial no preview.
8. **Passo 6** (montar prompt): não use o `prompts-routine.md`. Use `references/prompt-editorial-routine.md` (ver o bloco "Se Editorial" no Passo 6).

Siga agora para o Passo 2.

---

## Passo 2. Coleta de contexto (para os 6 estilos clássicos, Curiosidade e Editorial)

### 2.1. @ do Instagram

**Ordem de tentativa de sugestão:**

1. **`.env` na raiz do projeto** com chave `IG_USER=` (salvo por `dashboard-social`, `instagram-dashboard`, `dados-instagram` e outras skills). Esta é a fonte preferida.
2. **`perfil.md`** do produto ativo (procure `@`, "Instagram", "perfil").
3. **Nenhuma**: pergunte sem sugestão.

Com sugestão (vinda do `.env` ou `perfil.md`):

```
Pergunta 2. @ do Instagram

Sugestão: @{ig_user_sugerido}
{Se veio do .env} (achei no seu .env, salvo por outra skill do projeto)
{Se veio do perfil.md} (achei no seu perfil.md)

1. Sim, é esse mesmo
2. Outro @

Digite o número ou cole o @.
```

Sem sugestão:

```
Pergunta 2. @ do Instagram

Qual o @ do seu Instagram?

(ex: @leandroladeiran)

Digite o @.
```

AGUARDE A RESPOSTA. Quando o aluno responder:

- **Normalize**: remova o `@` se vier, lowercase, sem espaços. Salve como `handle`.
- **Se veio um @ novo (opção 2 ou resposta livre)**: salve no `.env` como `IG_USER={handle_sem_arroba}` (sobrescreve se já existe).
- **Se confirmou a sugestão (opção 1)**: não escreve no `.env`.

Mostre micro-resumo.

### 2.2. Nicho e produto em uma frase

**Antes de exibir a pergunta**, monte uma `sugestao_nicho_produto` lendo o `perfil.md`:

1. Procure o **Quadro** (transformação principal) e o **nicho/categoria** declarados no perfil.
2. Combine no formato `{nicho}, {tipo de produto} {duração se houver} para {público}` em UMA frase. Ex: "leitura rápida, curso online de 4 semanas para profissionais ocupados".
3. Se não conseguir montar uma frase clara (perfil incompleto), `sugestao_nicho_produto = null`.

**Com sugestão (perfil tem dado suficiente):**

```
Pergunta 3. Nicho e produto

Sugestão a partir do seu perfil: {sugestao_nicho_produto}

1. Sim, é essa mesma
2. Outra (eu digito)

Digite o número ou cole a frase.
```

Se o aluno responder `1`, salve `nicho_produto = sugestao_nicho_produto`. Se responder `2` ou colar frase nova, peça/use a frase. Se a resposta for um número que não é 1/2 mas a sugestão couber, trate como frase livre.

**Sem sugestão (perfil incompleto):**

```
Pergunta 3. Nicho e produto

Descreva seu nicho e produto em UMA frase.

(ex: {exemplo_dinamico})

Digite a frase.
```

Onde `{exemplo_dinamico}` deve usar o nicho do produto ativo se conhecido (ex: "leitura rápida, curso online de 4 semanas para profissionais ocupados"). Se não souber o nicho, use o exemplo padrão "surf, mentoria online de 8 semanas para surfistas intermediários".

AGUARDE. Salve como `nicho_produto`. Mostre micro-resumo.

### 2.3. Input extra (só se estilo pede)

Os estilos Erros e Ninguém Conta precisam de um input extra (Desejo ou Objetivo do público). Esse input deriva direto do **Quadro** do produto ativo (a transformação principal). Não peça em branco: leia o Quadro do `perfil.md`, reformule num desejo/objetivo concreto e mensurável, e devolva como sugestão para o aluno confirmar, mesmo padrão das perguntas 2.1 e 2.2.

**Antes de exibir a pergunta**, monte a sugestão:

1. Leia o **Quadro** no `perfil.md`.
2. O Quadro é redigido como transformação (verbo no infinitivo). Reformule num objetivo/desejo **concreto e mensurável**, com número, prazo ou marco quando o Quadro permitir. Ex: Quadro "Criar o hábito de leitura" vira objetivo "ler 3 livros por mês".
3. Se o Quadro for abstrato demais para virar um objetivo concreto, ou o perfil não tiver Quadro, a sugestão é `null`.

**Se `estilo_carrossel == 4` (Erros), com sugestão:**

```
Pergunta 4. Desejo do público

Sugestão a partir do seu produto: {sugestao_desejo}

1. Sim, é esse mesmo
2. Outro (eu digito)

Digite o número ou cole o desejo.
```

**Se `estilo_carrossel == 4` (Erros), sem sugestão:**

```
Pergunta 4. Desejo do público

Qual o desejo concreto do seu público?

(ex: emagrecer 10 kg, passar em concurso, atrair os primeiros clientes)

Digite o desejo.
```

Salve como `desejo_publico`.

**Se `estilo_carrossel == 6` (Ninguém Conta), com sugestão:**

```
Pergunta 4. Objetivo do público

Sugestão a partir do seu produto: {sugestao_objetivo}

1. Sim, é esse mesmo
2. Outro (eu digito)

Digite o número ou cole o objetivo.
```

**Se `estilo_carrossel == 6` (Ninguém Conta), sem sugestão:**

```
Pergunta 4. Objetivo do público

Qual o objetivo concreto que seu público quer atingir?

(ex: ganhar primeiro R$10 mil por mês, perder 10 kg, abrir o primeiro estúdio)

Digite o objetivo.
```

Salve como `objetivo_publico`.

Em ambos: se o aluno responder `1`, salve a sugestão. Se responder `2` ou colar texto novo, use o texto dele.

**Se estilo NÃO pede (1, 2, 3, 5):** pule esta pergunta e ajuste a numeração das perguntas seguintes para continuar sequencial.

Mostre micro-resumo se aplicável.

**Se `estilo_carrossel == 9` (Editorial):** pule a pergunta de Desejo/Objetivo acima e execute as 2 perguntas extras de Editorial abaixo, em sequência, uma por turno.

#### 2.3.E.1. Público (só Editorial)

**Antes de exibir**, monte uma `sugestao_publico` lendo o `idconsumidor.md` (se existir) ou o `perfil.md`:

1. Procure a descrição de público-alvo do produto, incluindo dor principal, contexto e o que o produto resolve para ele.
2. Combine numa frase clara. Ex: "atletas amadores e profissionais que precisam falar inglês em entrevistas, contratos e patrocínios internacionais".
3. Se não conseguir montar uma frase clara, `sugestao_publico = null`.

Com sugestão:

```
Pergunta {N}. Público

Sugestão a partir do seu produto: {sugestao_publico}

1. Sim, é esse mesmo
2. Outro (eu digito)

Digite o número ou cole a descrição.
```

Sem sugestão:

```
Pergunta {N}. Público

Descreva o público do seu produto em UMA frase (quem é, qual a dor, o que o produto resolve).

(ex: atletas amadores e profissionais que precisam falar inglês em entrevistas, contratos e patrocínios internacionais)

Digite a frase.
```

Salve como `editorial_publico`. Mostre micro-resumo.

#### 2.3.E.2. Tipo de CTA do slide 6 (só Editorial)

```
Pergunta {N}. Tipo de CTA do slide 6

Qual ação você quer pedir ao final do carrossel?

1. ManyChat (comente uma palavra-chave X e receba isca no direct)
2. Seguir o perfil
3. Engajar (pedir opinião nos comentários)
4. Salvar o post

Digite o número.
```

AGUARDE. Salve como `editorial_cta_tipo` (`ManyChat`, `Seguir`, `Engajar` ou `Salvar`). Mostre micro-resumo.

### 2.4. Tom da copy

Pergunta única (sem desdobrar em 2 turnos):

```
Pergunta {N}. Tom da copy

Qual tom você quer no texto dos carrosséis?

1. Variar a cada execução (Claude escolhe o melhor para o tema do dia)
2. Clássica e direta
3. Bem-humorada (trocadilhos, ironia)
4. Técnica (dados, mecanismos)
5. Inspiracional (aspiracional)
6. Casual (conversa de amigo)
7. Polêmica (provocações diretas)

Para a maioria, recomendo opção 1 (variar).

Digite o número.
```

AGUARDE. Se `1`, salve `tom_fixo = LIVRE`. Senão, salve o nome do tom em `tom_fixo`. Mostre micro-resumo.

**Se `estilo_carrossel == 8` (Curiosidade), use ESTA versão da pergunta de tom no lugar da acima** (os tons são os do prompt de Curiosidade):

```
Pergunta {N}. Tom da copy

Qual tom você quer no carrossel de Curiosidade?

1. Variar a cada execução (o Claude escolhe o melhor para o tema do dia)
2. Enérgico (motivação, ritmo rápido, frases curtas)
3. Polêmico (provocador, defende uma tese forte)
4. Engraçado (irônico, leve, observa o absurdo)
5. Reflexivo (pausado, filosófico)
6. Didático (explicador, professor)
7. Jornalístico (apurado, sóbrio, foco no fato)
8. Confessional (primeira pessoa, vulnerável)

Para a maioria, recomendo opção 1 (variar).

Digite o número.
```

AGUARDE. Se `1`, salve `tom_fixo = LIVRE`. Senão, salve o nome do tom (Enérgico, Polêmico, Engraçado, Reflexivo, Didático, Jornalístico ou Confessional) em `tom_fixo`. Mostre micro-resumo.

> **Editorial (estilo 9).** Pule esta pergunta de tom. Editorial não usa tom variável (o tom de especialista/newsletter é parte do estilo).

---

## Passo 3. Modo de geração de tema

> **Clássicos migrados (estilos 1 a 6: Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta).** Pule o Passo 3 inteiro. Cada um usa o respectivo `prompt-{estilo}-routine.md` (verbatim), que implementa "aleatório" internamente (escolhe um ângulo novo a cada execução, evitando repetir temas anteriores). Não existe mais modo FIXO para estes estilos. Salve `modo_geracao = AUTO_VERBATIM`. Vá direto para o Passo 4.

> **Curiosidade (estilo 8).** Pule o Passo 3 inteiro. A Curiosidade agendada sempre busca a curiosidade na web e escolhe o tema sozinha a cada execução, não existe modo FIXO. O `modo_geracao` já foi definido como `AUTO_WEB` no Passo 1.2. Vá direto para o Passo 4.

> **Editorial (estilo 9).** Pule o Passo 3 inteiro. O Editorial agendado sempre gera 10 ideias internamente e escolhe sozinho a mais forte a cada execução, não existe modo FIXO. O `modo_geracao` já foi definido como `AUTO_INTERNAL` no Passo 1.3. Vá direto para o Passo 4.

> **TODOS OS ESTILOS ATUAIS PULAM O PASSO 3.** A pergunta abaixo (ALEATORIO vs FIXO) é seção legada do modelo leve e não é mais invocada por nenhum estilo do menu atual. Mantida para referência histórica.

```
Pergunta {N}. Tema dos slides

Como você quer que a tarefa decida o tema de cada execução?

1. Aleatório. A cada execução, o Claude escolhe um ângulo novo dentro do estilo "{nome do estilo}", baseado nas Urgências Ocultas e Decorados do seu produto.
2. Fixo. Você define agora os 5 temas exatos (título de cada slide). A tarefa gera os mesmos 6 slides em toda execução, mudando só a legenda e os prompts visuais.

Para a maioria, recomendo "Aleatório".

Digite o número.
```

AGUARDE. Salve como `modo_geracao` (`ALEATORIO` ou `FIXO`). Mostre micro-resumo.

### 3.1. Se `modo_geracao == FIXO`

Peça os 5 temas, **um por turno**, com cabeçalho "Pergunta {N}.{i}" e micro-resumo entre cada um:

```
Pergunta {N}.1. Tema do slide 1

Lead obrigatório do estilo "{Estilo}": {lead_do_estilo}.

(ex para Sempre: "Sempre coma proteína no café da manhã")

Digite o título do slide 1.
```

Repita para slides 2 a 5. Para o slide 6, monte automaticamente a CTA conforme regra do estilo. Salve como `temas_fixos`.

---

## Passo 4. Frequência e horário

### 4.1. Frequência

```
Pergunta {N}. Frequência

Com que frequência a tarefa deve rodar?

1. Diária
2. Semanal
3. 2 vezes por semana
4. Quinzenal
5. Customizado (eu digo o cron, ou descrevo em texto)

Digite o número.
```

AGUARDE. Salve como `frequencia_tipo`. Mostre micro-resumo.

### 4.2. Horário (pular se já tem cron customizado de 4.5)

```
Pergunta {N}. Horário

Em que horário a tarefa deve rodar? Horário de Brasília.

1. 07:30 (manhã cedo, antes do trabalho)
2. 09:00 (manhã)
3. 12:00 (almoço)
4. 19:00 (noite, depois do trabalho)
5. 21:00 (final do dia)
6. Outro horário (eu digito)

Digite o número.
```

AGUARDE. Se `6`, pergunte:

```
Digite o horário no formato HH:MM (ex: 07:30, 14:00, 18:45).
```

Salve como `horario_hh_mm`. Mostre micro-resumo.

### 4.3. Dia da semana (se semanal)

Se `frequencia_tipo == 2`:

```
Pergunta {N}. Dia da semana

Qual dia da semana?

1. Segunda
2. Terça
3. Quarta
4. Quinta
5. Sexta
6. Sábado
7. Domingo

Digite o número.
```

Salve. Mostre micro-resumo.

### 4.4. Dois dias (se 2x semana)

Se `frequencia_tipo == 3`:

```
Pergunta {N}. Dois dias da semana

Quais 2 dias? Digite os números separados por vírgula.

(ex: 2,5 para terça e sexta)

1. Segunda  2. Terça  3. Quarta  4. Quinta  5. Sexta  6. Sábado  7. Domingo

Digite os 2 números separados por vírgula.
```

Salve. Mostre micro-resumo.

### 4.5. Customizado (se frequência = 5)

Se `frequencia_tipo == 5`:

```
Pergunta {N}. Cron customizado

Você pode:

A. Colar o cron direto, no formato padrão (minuto hora dia-mês mês dia-semana). Ex: "0 8 * * 1" = toda segunda às 8h.

B. Descrever em português o que você quer, e eu monto o cron pra você. Ex: "toda terça e quinta às 7h30", "todo dia 1 e 15 às 9h", "a cada 4 horas".

Digite o cron ou descreva em texto.
```

AGUARDE. Se o aluno digitou cron (5 campos separados por espaço): use direto. Se descreveu em texto: interprete e monte o cron. Antes de avançar, mostre:

```
Cron montado a partir da sua descrição: `{cron}`
Equivale a: {tradução legível em pt-BR}

1. Confirmar e seguir
2. Refazer

Digite o número.
```

Se 2, peça o texto de novo.

### 4.6. Conversão para UTC

A API de Routines aceita cron apenas em **UTC**. Brasília é UTC-3 (sem horário de verão desde 2019).

Regra: `hora_utc = (hora_brasilia + 3) mod 24`. Se passar de 24, o dia da semana avança 1.

Guarde duas variáveis:
- `cron`: cron real em UTC, enviado pro `/schedule`
- `frequencia_humana`: descrição em horário de Brasília, mostrada ao aluno

Exemplos:

| Brasília | cron UTC | frequencia_humana |
|---|---|---|
| Diária 8h | `0 11 * * *` | todo dia às 8h (Brasília) |
| Semanal segunda 9h | `0 12 * * 1` | toda segunda às 9h (Brasília) |
| 2x semana terça/sexta 8h | `0 11 * * 2,5` | toda terça e sexta às 8h (Brasília) |
| Quinzenal dia 1 e 15 às 8h | `0 11 1,15 * *` | dia 1 e 15 às 8h (Brasília) |

Se virar dia (ex: 22h Brasília → 01h UTC do dia seguinte), avance o dia da semana em 1.

---

## Passo 5. Confirmação consolidada (gate obrigatório)

Antes de montar o preview, descubra a hora local atual via `Bash` com `Get-Date -Format "yyyy-MM-dd HH:mm dddd"` (PowerShell). Calcule a próxima execução comparando com `horario_hh_mm`:

- Se o horário escolhido ainda não passou hoje e a frequência permite hoje: próxima execução é hoje.
- Caso contrário: próximo dia válido.

Mostre o preview em **texto corrido**, NÃO em YAML, NÃO em bloco de código, NÃO em tabela:

```
Tudo pronto para criar o agendamento. Confere se ficou como você quer.

Vou criar uma tarefa que roda **{frequencia_humana}** no horário de Brasília. A primeira execução acontece em **{data_proxima_legivel}**.

Cada vez que rodar, a tarefa vai gerar um carrossel de Instagram no estilo **{Estilo}** para o nicho **{nicho_produto}**, no perfil **{handle}**.

{se modo == ALEATORIO} O Claude vai criar um ângulo novo a cada execução, baseado nas Urgências Ocultas e Decorados do seu produto. {fim}
{se modo == FIXO} Os 5 temas dos slides ficam travados nos títulos que você definiu. Só a legenda e os prompts visuais mudam a cada execução. {fim}
{se Curiosidade} A cada execução, a tarefa busca curiosidades atemporais do seu nicho na web, escolhe sozinha a mais forte e monta um carrossel de 7 a 9 slides no formato editorial (capa com o fato, narrativa de revista, CTA fixo de seguir o perfil). {fim}
{se Editorial} A cada execução, a tarefa gera 10 ideias editoriais (notícia real, polêmica, conta maluca, pesquisa, comparação) para o público "{editorial_publico}", escolhe sozinha a mais forte e entrega o texto dos 6 slides + legenda + o prompt único pra colar no ChatGPT. CTA do slide 6: {editorial_cta_tipo}. {fim}
{se tom_fixo == LIVRE} O tom vai variar conforme o tema escolhido em cada execução. {fim}
{se tom_fixo != LIVRE} O tom fica travado em **{tom_fixo}** em todas as execuções. {fim}

O resultado aparece no painel de Routines do Claude (na nuvem). Você abre lá, lê os 6 slides + a legenda + os 6 prompts visuais, copia e monta o carrossel no Instagram.

1. Confirmar e criar o agendamento
2. Ajustar algo (diga qual campo)
3. Cancelar

Digite o número.
```

**Aguarde resposta explícita.**

- **Opção 1**: prossiga para o Passo 6 (montar prompt) e Passo 7-9 (criar agendamento).
- **Opção 2**: pergunte qual campo ajustar, refaça aquela pergunta, volte aqui.
- **Opção 3**: encerre sem criar agendamento.

---

## Passo 6. Montar prompt da tarefa

**Se `estilo_carrossel == 8` (Curiosidade):** NÃO use o `prompts-routine.md`. Carregue `references/prompt-curiosidade-routine.md` inteiro e use o bloco "Prompt final injetado na tarefa programada" dele como prompt da routine, substituindo os placeholders: `{{HANDLE}}` → `handle`, `{{NICHO_PRODUTO}}` → `nicho_produto`, `{{TOM}}` → nome do tom OU `LIVRE`, `{{DATA_HOJE_REF}}` → `[calcule a data de hoje no início da execução]`. Pule o resto deste Passo 6 (o Bloco A/B/C/D não se aplica à Curiosidade) e siga para o Passo 7.

**Se `estilo_carrossel == 9` (Editorial):** NÃO use o `prompts-routine.md`. Carregue `references/prompt-editorial-routine.md` inteiro e use o bloco "Prompt final injetado na tarefa programada" dele como prompt da routine, substituindo os placeholders: `{{HANDLE}}` → `handle`, `{{NICHO_PRODUTO}}` → `nicho_produto`, `{{PUBLICO}}` → `editorial_publico`, `{{CTA_TIPO}}` → `editorial_cta_tipo`, `{{DATA_HOJE_REF}}` → `[calcule a data de hoje no início da execução]`. Pule o resto deste Passo 6 (o Bloco A/B/C/D não se aplica ao Editorial) e siga para o Passo 7.

**Se `estilo_carrossel == 1` (Nunca):** NÃO use o `prompts-routine.md`. Carregue `references/prompt-nunca-routine.md` inteiro e use o bloco "Prompt final injetado na tarefa programada" dele como prompt da routine, substituindo os placeholders: `{{HANDLE}}` → `handle`, `{{NICHO_PRODUTO}}` → `nicho_produto`, `{{CORES_MARCA}}` → `cores_marca` (ou `DEFAULT` se o aluno não respondeu), `{{TOM_FIXO}}` → nome do tom OU `LIVRE`, `{{ESTILO_DESIGN}}` → `estilo_design`, `{{DATA_HOJE_REF}}` → `[calcule a data de hoje no início da execução]`. Pule o resto deste Passo 6 (o Bloco A/B/C/D não se aplica ao Nunca migrado) e siga para o Passo 7.

**Se `estilo_carrossel == 2` (Sempre):** NÃO use o `prompts-routine.md`. Carregue `references/prompt-sempre-routine.md` inteiro e use o bloco "Prompt final injetado na tarefa programada" dele como prompt da routine, substituindo os placeholders: `{{HANDLE}}` → `handle`, `{{NICHO_PRODUTO}}` → `nicho_produto`, `{{CORES_MARCA}}` → `cores_marca` (ou `DEFAULT`), `{{TOM_FIXO}}` → nome do tom OU `LIVRE`, `{{ESTILO_DESIGN}}` → `estilo_design`, `{{DATA_HOJE_REF}}` → `[calcule a data de hoje no início da execução]`. Pule o resto deste Passo 6 e siga para o Passo 7.

**Se `estilo_carrossel == 3` (Odeio):** NÃO use o `prompts-routine.md`. Carregue `references/prompt-odeio-routine.md` inteiro e use o bloco "Prompt final injetado na tarefa programada" dele como prompt da routine, substituindo os 6 placeholders padrão (`{{HANDLE}}`, `{{NICHO_PRODUTO}}`, `{{CORES_MARCA}}`, `{{TOM_FIXO}}`, `{{ESTILO_DESIGN}}`, `{{DATA_HOJE_REF}}`). Pule o resto deste Passo 6 e siga para o Passo 7.

**Se `estilo_carrossel == 4` (Erros):** NÃO use o `prompts-routine.md`. Carregue `references/prompt-erros-routine.md` inteiro e use o bloco "Prompt final injetado na tarefa programada" dele como prompt da routine, substituindo os 7 placeholders: os 6 padrão (`{{HANDLE}}`, `{{NICHO_PRODUTO}}`, `{{CORES_MARCA}}`, `{{TOM_FIXO}}`, `{{ESTILO_DESIGN}}`, `{{DATA_HOJE_REF}}`) **+ `{{DESEJO}}` → `desejo_publico`** (pergunta extra do Erros). Pule o resto deste Passo 6 e siga para o Passo 7.

**Se `estilo_carrossel == 5` (Amo):** NÃO use o `prompts-routine.md`. Carregue `references/prompt-amo-routine.md` inteiro e use o bloco "Prompt final injetado na tarefa programada" dele como prompt da routine, substituindo os 6 placeholders padrão (`{{HANDLE}}`, `{{NICHO_PRODUTO}}`, `{{CORES_MARCA}}`, `{{TOM_FIXO}}`, `{{ESTILO_DESIGN}}`, `{{DATA_HOJE_REF}}`). Pule o resto deste Passo 6 e siga para o Passo 7.

**Se `estilo_carrossel == 6` (Ninguém Conta):** NÃO use o `prompts-routine.md`. Carregue `references/prompt-ninguem-conta-routine.md` inteiro e use o bloco "Prompt final injetado na tarefa programada" dele como prompt da routine, substituindo os 7 placeholders: os 6 padrão (`{{HANDLE}}`, `{{NICHO_PRODUTO}}`, `{{CORES_MARCA}}`, `{{TOM_FIXO}}`, `{{ESTILO_DESIGN}}`, `{{DATA_HOJE_REF}}`) **+ `{{OBJETIVO}}` → `objetivo_publico`** (pergunta extra do Ninguém Conta). Pule o resto deste Passo 6 e siga para o Passo 7.

> **SEÇÃO LEGADA.** O bloco abaixo (`prompts-routine.md` com Bloco A/B/C/D + lista de placeholders) NÃO é mais invocado por nenhum estilo após a migração dos 6 clássicos. Mantida apenas como referência histórica do modelo leve. Se um estilo futuro precisar do padrão Bloco A/B/C/D, ele pode reutilizar este caminho.

Para referência (sem aplicação ativa hoje): Carregue `references/prompts-routine.md` e monte o prompt final concatenando:

- **Bloco A. Cabeçalho** (sempre)
- **Bloco B-{Estilo}** (específico do estilo, com o critério central e estrutura dos slides)
- **Bloco C-ALEATORIO** ou **Bloco C-FIXO** conforme `modo_geracao`
- **Bloco D. Output** (sempre): formato esperado, salvamento, formato do arquivo consolidado

Placeholders padrão do modelo leve:
- `{{HANDLE}}` → `handle`
- `{{NICHO_PRODUTO}}` → `nicho_produto`
- `{{ESTILO}}` → nome do estilo
- `{{TOM_FIXO}}` → nome do tom OU `LIVRE`
- `{{DESEJO}}` → `desejo_publico` (se Erros)
- `{{OBJETIVO}}` → `objetivo_publico` (se Ninguém Conta)
- `{{TEMAS_FIXOS}}` → lista dos 5 títulos (se modo FIXO)
- `{{DATA_HOJE_REF}}` → `[calcule a data de hoje no início da execução]`

---

## Passo 7. Salvar registro local

Antes de chamar `/schedule create`, salve em:

```
meus-produtos/{ativo}/agendamentos/carrossel/{slug}.md
```

Onde `slug` = `carrossel-{estilo}-{nicho-slug}-{YYYY-MM-DD-HHmmss}` (timestamp da criação).

Conteúdo:

```yaml
schedule_id: pendente
nome: "[FC] Carrossel {Estilo} {frequencia_humana} {nicho}"
criado_em: {data_de_hoje}

contexto:
  handle: {handle}
  nicho_produto: {nicho_produto}
  desejo: {desejo_publico ou null}
  objetivo: {objetivo_publico ou null}

agendamento:
  cron: "{cron}"
  timezone: "America/Sao_Paulo"
  frequencia_humana: {frequencia_humana}

config:
  estilo: {estilo_carrossel}
  modo_geracao: {modo_geracao}
  tom_fixo: {tom_fixo}
  temas_fixos: {temas_fixos ou null}

prompt_final: |
  {prompt completo do Passo 6}
```

---

## Passo 8. Acionar /schedule create

Use a tool `Skill` para invocar a skill `schedule` do Claude Code:
- `action`: `create`
- `name`: nome do agendamento
- `cron`: cron em UTC (Passo 4.6)
- `prompt`: prompt final do Passo 6

Não passe `timezone` (a API descarta).

**REGRA DURA. Criar a routine SEM repositório Git anexado.** Ao montar o corpo da criação (`job_config.ccr.session_context`), NÃO inclua o campo `sources` com `git_repository`. A tarefa de carrossel é autossuficiente: todo o contexto necessário já está no prompt do Passo 6. Anexar o repositório faz a execução do remote agent FALHAR. O `session_context` deve conter apenas `model` e `allowed_tools`, sem `sources`. Se a skill `schedule` montar o corpo com `sources` por padrão, remova o campo antes de criar (ou crie via `RemoteTrigger` com `session_context` sem `sources`).

Quando retornar o `schedule_id`, atualize o arquivo do Passo 7 com o ID.

### Limitação conhecida do /schedule

A skill nativa `schedule` do Claude Code suporta apenas `create`, `update`, `list` e `run`. **Não tem `delete` via CLI.** Para deletar um agendamento, o aluno precisa acessar https://claude.ai/code/routines pela web e remover lá.

Para PAUSAR um agendamento (sem deletar), use `/schedule update {schedule_id}` com `enabled=false`.

---

## Passo 9. Entrega

Exiba:

```
✅ Agendamento criado.

Nome: {nome}
Schedule ID: {schedule_id}
Link direto: https://claude.ai/code/routines/{schedule_id}
Próxima execução: {data_proxima_calculada}
Horário recorrente: {frequencia_humana}

O que a tarefa faz:
A cada execução, gera 1 carrossel de Instagram no estilo "{Estilo}" para o nicho {nicho}, com {modo_descrito}.

Onde ver o resultado:
Painel de Routines do Claude. Você abre, lê os slides + legenda + prompts visuais, copia e monta o carrossel no Instagram.

Configuração local salva em:
{caminho_absoluto}

Para pausar: abra o link acima e desabilite, ou rode /schedule update {schedule_id} com enabled=false.
Para deletar: acesse https://claude.ai/code/routines pela web (a CLI não suporta delete).
Para criar outro agendamento: /programar-carrossel.
```

Exiba o caminho absoluto em formato copiável conforme regra do `CLAUDE.md`.

---

## Regras

- **Aprovação obrigatória** no Passo 5 antes de chamar `/schedule create`.
- **Cron sempre em UTC.** Brasília convertida automaticamente.
- **Sem tokens expostos.** Nunca exiba access tokens em comando ou log.
- **Slug sem confirmação.** Gerado automaticamente conforme regra global.
- **Sem auto-revisão de copy nesta skill.** A copy real é gerada pela tarefa programada em runtime. O prompt do Bloco B já carrega as proibições do Light Copy.
- **"Cancelar" disponível** em toda aprovação. No Passo 1, o aluno pode digitar `cancelar`, `0` ou `sair` em vez de escolher um estilo. No Passo 5, é a opção 3 do bloco de confirmação.
- **Micro-resumo de progresso** após cada resposta (formato no início deste arquivo).
- **Passar contexto na delegação para Notícia** (Passo 1.1). O aluno não deve digitar o mesmo dado duas vezes.

---

## Quando NÃO usar esta skill

- O aluno quer **um carrossel agora** (sem agendamento recorrente). Use `/carrossel`.
- O aluno quer agendar **outra coisa** (resumo de tráfego, post avulso). Use `/trafego-regras` ou crie skill específica.
- O aluno ainda não cadastrou produto. Use `/produto-novo`.
