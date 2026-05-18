---
name: programar-carrossel
description: Programa uma tarefa recorrente que gera carrossel para Instagram automaticamente, em 1 dos 7 estilos (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia da semana). A tarefa roda na nuvem do Claude via /schedule, na frequência escolhida (diária, semanal, quinzenal, customizada). O resultado aparece no painel de Routines.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
model: sonnet
---

# Programar Carrossel Recorrente

Configura uma tarefa que gera carrossel de Instagram automaticamente, no estilo e frequência escolhidos. A tarefa programada roda na nuvem do Claude (via `/schedule`) e entrega o resultado no painel de Routines, sem depender do computador do aluno estar ligado.

---

## Anúncio inicial

```
🔍 Próximo passo: configurar a tarefa programada de carrossel (entre 8 e 14 perguntas, dependendo do estilo e do modo escolhido). Tempo estimado: 3 a 6 minutos.
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

Quando o estilo escolhido não pede input extra (Nunca, Sempre, Odeio, Amo), a pergunta da seção 2.3 é pulada: ajuste a numeração das perguntas seguintes para continuar sequencial, sem buraco.

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

---

## Passo 2. Coleta de contexto (para os 6 estilos atemporais)

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

---

## Passo 3. Modo de geração de tema

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

(ex para Nunca: "Nunca corte carboidrato no jantar")

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

Carregue `references/prompts-routine.md` e monte o prompt final concatenando:

- **Bloco A. Cabeçalho** (sempre)
- **Bloco B-{Estilo}** (específico do estilo, com o critério central e estrutura dos slides)
- **Bloco C-ALEATORIO** ou **Bloco C-FIXO** conforme `modo_geracao`
- **Bloco D. Output** (sempre): formato esperado, salvamento, formato do arquivo consolidado

Substitua placeholders:
- `{{HANDLE}}` → `handle`
- `{{NICHO_PRODUTO}}` → `nicho_produto`
- `{{ESTILO}}` → nome do estilo (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta)
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
