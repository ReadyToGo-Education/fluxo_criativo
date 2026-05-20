---
name: programar-carrossel-noticia
description: Programa uma tarefa recorrente que gera carrossel de notícia para Instagram automaticamente, usando o /schedule do Claude Code. Configura escopo (só busca de notícia ou carrossel inteiro), modo (aleatório ou fixo), dimensões travadas (tom, categoria de notícia), frequência e horário. Coleta @, nicho e produto uma única vez.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
model: sonnet
---

# Programar Carrossel de Notícia

Configura uma tarefa recorrente que gera carrossel de notícia para o Instagram do criador, na frequência escolhida. A tarefa programada roda na nuvem do Claude (via `/schedule`) e entrega o resultado no painel de Routines, sem depender do computador do aluno estar ligado.

A skill é a etapa de configuração. O agendamento é criado uma vez e fica rodando até o aluno pausar ou deletar.

---

## Relação com `/programar-carrossel`

Esta skill é **especializada em Notícia** (carrossel a partir de notícia da semana ou curiosidade atemporal). Tem configurações próprias (escopo `BUSCA` vs `CARROSSEL_INTEIRO`, modo `ALEATORIO` vs `FIXO`, categoria `TREND` vs `ATEMPORAL`, tom travado) que não fazem sentido nos outros 6 estilos.

A skill `/programar-carrossel` (carrosséis atemporais: Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta) **delega pra cá** quando o aluno escolhe a opção "Notícia" no menu dela. Quando isso acontece, `/programar-carrossel` invoca esta skill via Skill tool e encerra, e esta skill toma conta do fluxo inteiro.

Para os carrosséis atemporais (sem notícia), use `/programar-carrossel`. Para carrossel de Notícia, use esta skill direto ou deixe `/programar-carrossel` te encaminhar.

---

## Anúncio inicial

Antes da entrevista, anuncie:

```
🔍 Próximo passo: configurar a tarefa programada de carrossel de notícia (7 passos). Tempo estimado: 2 a 4 minutos.
```

---

## REGRA DURA — não criar worktree

Esta skill grava arquivo de config em `meus-produtos/{ativo}/agendamentos/` (dado do aluno, não código do projeto). **NUNCA chame `EnterWorktree` durante esta skill.** Grave direto no checkout do aluno via `Write`.

Se o harness bloquear o `Write` pedindo worktree (situação rara, só ocorre em background sessions internas), aborte a skill e avise o aluno pra rodar `/programar-carrossel-noticia` em sessão foreground normal do Claude Code. Não tente contornar criando worktree, isso confunde o aluno.

---

## REGRA DURA — uma pergunta por turno

Esta skill é uma entrevista guiada. **Cada Passo é UMA pergunta separada que precisa de resposta do aluno antes do próximo Passo.**

PROIBIDO:
- Assumir default sem perguntar. Mesmo que o perfil tenha sugestão, EXIBA a pergunta e AGUARDE a resposta.
- Bulkar 2 ou mais perguntas no mesmo turno.
- Pular do Passo 1.1 direto pra confirmação final.
- Apresentar o preview do Passo 6 antes de coletar TODAS as respostas dos Passos 1 a 5.

OBRIGATÓRIO:
- Exibir UMA pergunta, parar a execução, aguardar o aluno responder, salvar a variável, só então exibir a próxima.
- Se o aluno responder com algo ambíguo, perguntar de novo a mesma pergunta, não avançar.
- O preview do Passo 6 só aparece DEPOIS de Passos 1.1, 1.2, 1.3, 2, (3 se aplicável), (4 se aplicável) e 5 terem respostas concretas do aluno.

Esta regra anula qualquer outra orientação geral de "reduzir confirmações" ou "executar direto" que exista no projeto. Aqui a entrevista guiada é o produto da skill.

---

## Passo 0. Contexto

Leia em paralelo:
- `meus-produtos/.ativo` para descobrir o produto ativo.
- `meus-produtos/{ativo}/perfil.md` se existir.
- `meus-produtos/{ativo}/idconsumidor.md` se existir.

Se não houver produto ativo, instrua o aluno a rodar `/produto-novo` primeiro e encerre.

Do perfil, tente extrair como sugestão (não use ainda):
- **Handle do Instagram**. Procure por `@`, "Instagram", "perfil" no perfil.
- **Nicho**. Procure por "Nicho:", "Mercado:", ou pela seção de identidade.
- **Produto**. Combine nome do produto, formato e público-alvo do perfil.

Esses valores entram como _default_ nas perguntas do Passo 1, mas o aluno pode confirmar ou ajustar.

---

## Passo 1. Coleta de contexto (3 perguntas, uma por vez)

Faça as 3 perguntas em SEQUÊNCIA, uma por turno. Após exibir cada uma, PARE a execução e aguarde a resposta do aluno antes de exibir a próxima.

### 1.1. @ do Instagram

Exiba EXATAMENTE este bloco e pare:

```
Qual o @ do seu Instagram?

(ex: @leandroladeiran)

Digite o @.
```

AGUARDE A RESPOSTA. Salve em memória de sessão como `handle`. **NÃO** exiba a 1.2 no mesmo turno.

### 1.2. Nicho

Quando o aluno responder a 1.1, exiba a 1.2. Se o perfil tem nicho identificado, ofereça como opção:

```
Qual o nicho do seu conteúdo?

(ex: surf, finanças pessoais, maternidade real, tarô)

Sugestão a partir do seu perfil:
{nicho_sugerido}

1. Usar a sugestão acima
2. Digitar outro nicho

Digite o número ou cole o nicho.
```

Se NÃO houver sugestão no perfil, exiba só a pergunta + exemplo + "Digite o nicho.":

```
Qual o nicho do seu conteúdo?

(ex: surf, finanças pessoais, maternidade real, tarô)

Digite o nicho.
```

AGUARDE A RESPOSTA. Salve como `nicho`. **NÃO** exiba a 1.3 no mesmo turno.

### 1.3. Produto

Quando o aluno responder a 1.2, exiba a 1.3. Se o perfil tem produto identificado, ofereça como opção:

```
Qual o produto que você vende?

Inclua nome + formato + para quem é.

(ex: Curso Onda Limpa, mentoria online de 8 semanas para surfistas intermediários que travaram no avanço)

Sugestão a partir do seu perfil:
{produto_sugerido}

1. Usar a sugestão acima
2. Digitar outro produto

Digite o número ou cole o produto.
```

Se NÃO houver sugestão, exiba só a pergunta + exemplo + "Digite o produto.".

AGUARDE A RESPOSTA. Salve como `produto`. **NÃO** exiba o Passo 2 no mesmo turno.

---

## Passo 2. Escopo da tarefa

Quando o aluno responder a 1.3, exiba SOMENTE este bloco e pare:

```
O que você quer que a tarefa programada faça?

1. Só buscar as notícias e me apresentar as 6 opções (eu escolho a notícia e o tom depois, manualmente)
2. Gerar o carrossel inteiro automaticamente (texto + prompts visuais + arquivo consolidado)

Digite o número:
```

AGUARDE A RESPOSTA. Salve como `escopo` (`BUSCA` ou `CARROSSEL_INTEIRO`). **NÃO** exiba Passo 3 nem nada de Passo 5 no mesmo turno.

**Se `escopo == BUSCA`:** o próximo Passo será o 5 (frequência). Pule 3 e 4.

---

## Passo 3. Modo de execução (só se escopo = CARROSSEL_INTEIRO)

Quando o aluno responder o Passo 2 com `2`, exiba SOMENTE este bloco e pare:

```
Como você quer que a tarefa decida a notícia e o tom em cada execução?

1. Aleatório — o Claude escolhe a notícia mais quente entre as 6 e o tom mais adequado a ela
2. Fixo — você decide agora o que fica travado em todas as execuções

Digite o número:
```

AGUARDE A RESPOSTA. Salve como `modo` (`ALEATORIO` ou `FIXO`). **NÃO** exiba Passo 4 nem Passo 5 no mesmo turno.

**Se `modo == ALEATORIO`:** o próximo Passo será o 5 (`categoria_fixa = LIVRE`, `tom_fixo = LIVRE`).

---

## Passo 4. Dimensões fixas (só se modo = FIXO)

### 4.1. O que travar

Quando o aluno escolher `2` no Passo 3, exiba SOMENTE este bloco e pare:

```
O que você quer travar em todas as execuções?

1. Só o tom (notícia continua sendo escolhida automaticamente entre as 6 da semana)
2. Só a categoria de notícia (sempre Trend ou sempre Atemporal)
3. Tom + categoria

Digite o número:
```

AGUARDE A RESPOSTA. **NÃO** exiba 4.2 nem 4.3 no mesmo turno.

### 4.2. Se 1 ou 3 → pergunta o tom

Quando o aluno responder 1 ou 3 em 4.1, exiba SOMENTE este bloco e pare:

```
Qual tom você quer travar para todos os carrosséis?

1. Enérgico (motivação, ritmo rápido, frases curtas e diretas)
2. Polêmico (provocador, defende uma tese forte, divide opinião)
3. Engraçado (irônico, leve, observa o absurdo)
4. Reflexivo (pausado, filosófico, leva o leitor a pensar)
5. Didático (explicador, professor, traduz o complicado)
6. Jornalístico (apurado, sóbrio, foco no fato)
7. Confessional (em primeira pessoa, vulnerável, vivência real)

Digite o número:
```

AGUARDE A RESPOSTA. Salve o nome do tom como `tom_fixo`.

### 4.3. Se 2 ou 3 → pergunta a categoria

Quando aplicável, exiba SOMENTE este bloco e pare:

```
Qual categoria de notícia você quer travar?

1. Trend — sempre notícia da semana (últimos 7 dias)
2. Atemporal — sempre curiosidade ou fato chocante (sem prazo)

Digite o número:
```

AGUARDE A RESPOSTA. Salve como `categoria_fixa` (`TREND` ou `ATEMPORAL`).

### 4.4. Preencher LIVRE no que não foi travado

- Se a escolha em 4.1 foi `1`: `categoria_fixa = LIVRE`.
- Se a escolha em 4.1 foi `2`: `tom_fixo = LIVRE`.

---

## Passo 5. Frequência

Quando o Passo anterior responsável (2 se BUSCA, 3 se ALEATORIO, 4 se FIXO) terminar, exiba SOMENTE este bloco e pare:

```
Com que frequência a tarefa deve rodar?

1. Diária (todo dia)
2. Semanal (1 vez por semana)
3. 2 vezes por semana
4. Quinzenal (a cada 15 dias)
5. Customizado (eu digo o cron)

Digite o número:
```

AGUARDE A RESPOSTA. Salve como `frequencia_tipo`. **NÃO** exiba 5.1 no mesmo turno.

### 5.1. Horário

Quando o aluno responder a frequência, exiba SOMENTE este bloco e pare:

```
Em que horário a tarefa deve rodar? Use horário de Brasília.

(ex: 07:30, 09:00, 14:00)

Digite o horário no formato HH:MM.
```

AGUARDE A RESPOSTA. Salve como `horario_hh_mm`. **NÃO** exiba 5.2 nem 5.3 no mesmo turno.

### 5.2. Se semanal → dia da semana

Quando aplicável, exiba SOMENTE este bloco e pare:

```
Qual dia da semana?

1. Segunda
2. Terça
3. Quarta
4. Quinta
5. Sexta
6. Sábado
7. Domingo

Digite o número:
```

AGUARDE A RESPOSTA.

### 5.3. Se 2 vezes por semana → 2 dias

Exiba a mesma lista de 5.2 e peça os 2 números separados por vírgula. AGUARDE A RESPOSTA.

### 5.4. Se customizado → pede cron

Exiba SOMENTE este bloco e pare:

```
Cole o cron que você quer (formato padrão: minuto hora dia-mes mes dia-semana).
(ex: 0 8 * * 1 = toda segunda às 8h)
```

AGUARDE A RESPOSTA.

### 5.5. Montar cron final em UTC (atenção, regra dura)

**A API de Routines do Claude Code aceita cron apenas em UTC.** O argumento `timezone` que aparece em alguns docs é silenciosamente descartado. Por isso, esta skill é responsável por converter o horário escolhido pelo aluno (Brasília, UTC-3, sem horário de verão desde 2019) para UTC ANTES de enviar pro `/schedule`.

Regra de conversão: `hora_utc = (hora_brasilia + 3) mod 24`. Se a soma passar de 24, o dia da semana também avança em 1.

Guarde duas variáveis separadas:
- `cron`: o cron real, em UTC, que vai pro `/schedule create`
- `frequencia_humana`: descrição em horário de Brasília que será mostrada pro aluno e salva no registro local

Exemplos:

| Pedido do aluno (Brasília) | cron (UTC, enviado pro /schedule) | frequencia_humana (mostrada pro aluno) |
|---|---|---|
| Diária 8h | `0 11 * * *` | todo dia às 8h (Brasília) |
| Diária 9h | `0 12 * * *` | todo dia às 9h (Brasília) |
| Semanal segunda 9h | `0 12 * * 1` | toda segunda às 9h (Brasília) |
| 2x semana ter/sex 8h | `0 11 * * 2,5` | toda terça e sexta às 8h (Brasília) |
| Quinzenal dia 1 e 15 às 8h | `0 11 1,15 * *` | dia 1 e 15 de cada mês às 8h (Brasília) |

Atenção ao virar dia: se o aluno escolher 22h em Brasília (= 01h UTC do dia seguinte), o dia da semana do cron precisa avançar 1. Para `2x semana terça/sexta às 22h`, vira `0 1 * * 3,6` (quarta e sábado em UTC).

Salve o cron UTC como `cron` (a variável que vai pro `/schedule`).

---

## Passo 6. Confirmação (gate obrigatório)

**Antes de montar o preview**, rode um comando pra descobrir a hora local atual. No Windows use `Get-Date -Format "yyyy-MM-dd HH:mm dddd"` (PowerShell). Em Mac ou Linux use `date '+%Y-%m-%d %H:%M %A'`. Guarde como `agora_brasilia`.

Compare `agora_brasilia` com o horário escolhido pelo aluno em `horario_hh_mm`:

- Se o horário escolhido AINDA não passou hoje (e a frequência permite hoje), a próxima execução é HOJE no horário escolhido.
- Se o horário escolhido JÁ passou hoje, ou se a frequência exige outro dia (semanal, quinzenal), a próxima execução é o próximo dia válido.

Use essa informação ao montar `{{data_proxima_legivel}}`. Nunca chute "amanhã" sem checar a hora atual.

Exemplo: se agora é "2026-05-13 10:38 quarta-feira" e o aluno pediu diária às 9h, próxima execução é "amanhã quinta-feira 14/05 às 9h" (porque 9h já passou hoje). Se agora fosse "2026-05-13 08:12 quarta-feira", próxima execução seria "ainda hoje quarta 13/05 às 9h".

---

Mostre o preview ao aluno em **texto corrido em português**, NÃO em YAML, NÃO em bloco de código, NÃO em tabela. O YAML é só formato interno seu pra organizar os dados, ele nunca aparece pro aluno.

Use exatamente esta estrutura de parágrafos (substitua os valores entre chaves pelos valores coletados):

```
Tudo pronto pra criar o agendamento. Confere se ficou como você quer.

Vou criar uma tarefa que roda **{{frequencia_humana}}** no horário de Brasília. A primeira execução acontece em **{{data_proxima_legivel}}**.

Cada vez que rodar, a tarefa vai {{descricao_do_escopo_em_uma_frase}} para o nicho de **{{nicho}}**, no perfil **{{handle}}**.

{{se escopo = CARROSSEL_INTEIRO, parágrafo extra}}
{{se modo = ALEATORIO}} O Claude vai escolher sozinho a notícia mais quente da semana e o tom mais adequado a ela em cada execução. {{fim}}
{{se modo = FIXO e tom_fixo != LIVRE}} O tom fica travado em **{{tom_fixo}}** em todas as execuções. {{fim}}
{{se modo = FIXO e categoria_fixa != LIVRE}} A categoria de notícia fica travada em **{{categoria_humana}}** ({{descricao_categoria}}). {{fim}}
{{fim}}

O resultado aparece no painel de Routines do Claude (na nuvem). Você abre lá, lê {{o que ele recebe: "as 6 ideias de notícia" ou "o texto + os prompts visuais + o arquivo consolidado"}}, copia e monta o carrossel no Instagram.

Pra confirmar, responde **SIM**. Se quiser ajustar alguma coisa, diz o que mudar.
```

**Onde preencher cada valor:**

- `{{frequencia_humana}}`: "todo dia", "toda segunda", "toda terça e sexta", "no dia 1 e 15 de cada mês", "no horário customizado X".
- `{{data_proxima_legivel}}`: data + dia da semana + horário no estilo "amanhã 14/05 às 9h" ou "segunda 19/05 às 9h".
- `{{descricao_do_escopo_em_uma_frase}}`:
  - Se escopo = BUSCA: "buscar 6 ideias de notícia da semana (3 Trend dos últimos 7 dias + 3 Atemporais sem prazo) e te apresentar com fonte"
  - Se escopo = CARROSSEL_INTEIRO: "buscar 6 ideias de notícia, escolher uma, decidir o tom e gerar o carrossel completo (texto dos slides + prompts visuais + arquivo consolidado pra automação)"
- `{{tom_fixo}}`: nome do tom (Enérgico, Polêmico, Engraçado, Reflexivo, Didático, Jornalístico, Confessional).
- `{{categoria_humana}}` + `{{descricao_categoria}}`:
  - Se categoria_fixa = TREND: "Trend" + "sempre notícia da semana, últimos 7 dias"
  - Se categoria_fixa = ATEMPORAL: "Atemporal" + "sempre curiosidade ou fato chocante sem prazo"

**Regras de exibição:**

- Texto corrido, parágrafos curtos, negrito no Markdown apenas nos valores principais (frequência, data, nicho, handle, tom, categoria).
- Proibido travessão (—), exclamação, YAML, blocos de código, tabelas.
- Português brasileiro com acentuação correta.
- O bloco com `{{...}}` é só o gabarito que você usa pra montar. Substitua TODOS os placeholders antes de exibir. Se algum valor estiver vazio, pergunte de volta o que faltou antes de mostrar o preview.

**Aguardando confirmação:**

Aguarde `SIM` (ou variantes claras como "sim", "pode", "aprovado", "manda"). Sem confirmação explícita, não chame o `/schedule`.

Se o aluno responder qualquer coisa diferente de SIM (ex: "muda o horário pra 8h", "deixa como Atemporal fixo"), pergunte o que ajustar, atualize a variável e refaça o preview em texto corrido. Não pule pro Passo 7.

---

## Passo 7. Montar prompt e chamar /schedule

### 7.1. Compor o prompt da tarefa

Leia `.claude/skills/programar-carrossel-noticia/references/prompt-carrossel-noticia.md`. Monte o prompt final concatenando:

- Sempre: **Bloco A** + **Bloco B**
- Se `escopo == BUSCA`: + **Bloco C-BUSCA**
- Se `escopo == CARROSSEL_INTEIRO`: + **Bloco C-CARROSSEL.1** + **C-CARROSSEL.2** + **C-CARROSSEL.3** + **C-CARROSSEL.4**

Substitua todos os placeholders `{{...}}` pelos valores coletados:
- `{{HANDLE}}` → valor de `handle`
- `{{NICHO}}` → valor de `nicho`
- `{{PRODUTO}}` → valor de `produto`
- `{{ESCOPO}}` → `BUSCA` ou `CARROSSEL_INTEIRO`
- `{{MODO}}` → `ALEATORIO` ou `FIXO` (apenas no Bloco C-CARROSSEL.1)
- `{{TOM_FIXO}}` → nome do tom ou `LIVRE`
- `{{CATEGORIA_FIXA}}` → `TREND`, `ATEMPORAL` ou `LIVRE`
- `{{DATA_HOJE_REF}}` → manter como instrução para a tarefa programada calcular em runtime (texto: "calcule a data de hoje no início da execução")

### 7.2. Salvar registro local

Antes de chamar o `/schedule`, salve um arquivo de configuração em:

```
meus-produtos/{ativo}/agendamentos/carrossel-noticia/{schedule_slug}.md
```

Onde `schedule_slug` é gerado automaticamente como `carrossel-{nicho-slug}-{escopo-slug}-{YYYY-MM-DD-HHmmss}` (sem pedir confirmação ao aluno), usando o timestamp atual da criação (não o horário escolhido pelo aluno).

- `{nicho-slug}`: nicho normalizado em minúsculas e hífen (`marketing digital` → `marketing-digital`).
- `{escopo-slug}`: `busca` se escopo=BUSCA, `carrossel` se escopo=CARROSSEL_INTEIRO.
- `{YYYY-MM-DD-HHmmss}`: timestamp completo do momento da criação. Use `Get-Date -Format "yyyy-MM-dd-HHmmss"` no PowerShell. Inclui segundos pra evitar colisão se o aluno criar 2 agendamentos no mesmo minuto.

Exemplo: `carrossel-marketing-digital-busca-2026-05-13-134258.md`.

Conteúdo do arquivo:

```yaml
schedule_id: pendente (preenchido após /schedule create)
nome: "[FC] Carrossel-{{nicho}}-{{frequencia_humana}}"
criado_em: {{data_de_hoje}}

contexto:
  handle: {{handle}}
  nicho: {{nicho}}
  produto: {{produto}}

agendamento:
  cron: "{{cron}}"
  timezone: "America/Sao_Paulo"
  frequencia_humana: {{descricao_legivel_da_frequencia}}

config:
  escopo: {{escopo}}
  modo: {{modo}}
  tom_fixo: {{tom_fixo}}
  categoria_fixa: {{categoria_fixa}}

prompt_final: |
  {{prompt completo gerado no 7.1, com indentação YAML}}
```

### 7.3. Acionar /schedule create

Use a tool `Skill` para invocar a skill `schedule` do Claude Code (não confundir com qualquer skill do projeto). Passe como argumento:

- `action`: `create`
- `name`: o nome do agendamento (ex: `[FC] Carrossel-surf-segunda-9h-<produto-slug>`)
- `cron`: o cron **em UTC** montado no Passo 5.5 (já convertido de Brasília)
- `prompt`: o prompt final montado no 7.1

Não passe `timezone`. A API de Routines não usa esse campo (ver limitação 1 abaixo).

**REGRA DURA. Criar a routine SEM repositório Git anexado.** Ao montar o corpo da criação (`job_config.ccr.session_context`), NÃO inclua o campo `sources` com `git_repository`. A tarefa de carrossel de notícia é autossuficiente: todo o contexto necessário já está no prompt do 7.1. Anexar o repositório faz a execução do remote agent FALHAR. O `session_context` deve conter apenas `model` e `allowed_tools`, sem `sources`. Se a skill `schedule` montar o corpo com `sources` por padrão, remova o campo antes de criar.

A skill `schedule` cuida da criação no backend do Claude Code. Quando ela retornar o `schedule_id`, volte para esta skill e atualize o registro local salvando esse ID no arquivo do Passo 7.2.

#### Limitações conhecidas da skill /schedule do Claude Code

1. **Cron sempre em UTC.** O argumento `timezone` é aceito mas silenciosamente descartado pela API de Routines. O Passo 5.5 já resolve isso convertendo o horário pra UTC.

2. **MCP connectors anexados automaticamente.** A skill `/schedule` anexa TODOS os MCP connectors conectados na conta `claude.ai` do aluno (higgsfield, Vercel, Slack, Adobe, Meta-Ads, Google Drive, etc.), mesmo que a tarefa não precise de nenhum. Como esta tarefa só faz busca web + texto, os MCPs não atrapalham mas inflam a sessão remota. Não há como evitar dentro desta skill (decisão da skill `/schedule`). Se atrapalhar no futuro, abrir issue na skill do Claude Code.

3. **Não anexar repositório Git ao `sources`.** A skill `/schedule` tende a colocar o repo do GitHub do projeto no `sources` do remote agent por padrão. Isso faz a execução FALHAR (erro de clone quando o GitHub não está conectado, e o agent não chega a rodar a tarefa). Como o prompt é autossuficiente, a routine deve ser criada SEM `sources` (ver regra dura no 7.3). O `session_context` fica só com `model` e `allowed_tools`.

4. **Allowed tools default amplo.** O remote agent recebe permissão pra Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch. Pra esta tarefa só precisa WebSearch + WebFetch, mas o resto não atrapalha.

5. **API não suporta delete.** A skill `/schedule` da CLI suporta apenas list, get, create, update, run. Pra deletar um agendamento, o aluno precisa acessar https://claude.ai/code/routines e remover pela interface web. Na entrega do Passo 8, oriente o aluno por esse caminho em vez de sugerir `/schedule delete`.

Se a skill `schedule` não estiver disponível na sessão atual, exiba este aviso e pare:

```
A skill /schedule do Claude Code não está disponível nesta sessão. Pode acontecer em ambientes onde o agendamento na nuvem está desabilitado.

Eu salvei a configuração completa do agendamento em:
meus-produtos/{ativo}/agendamentos/carrossel-noticia/{schedule_slug}.md

Para programar manualmente, abra o Claude Code numa sessão com /schedule habilitado, rode /schedule create e cole o cron e o prompt que estão lá dentro.
```

---

## Passo 8. Entrega

Após o `/schedule create` retornar com sucesso:

```
✅ Agendamento criado.

Nome: {{nome_do_agendamento}}
Schedule ID: {{schedule_id}}
Link direto: https://claude.ai/code/routines/{{schedule_id}}
Próxima execução: {{data_proxima_calculada_no_passo_6}}
Horário recorrente: {{frequencia_humana}} (cron interno em UTC: {{cron}})

O que a tarefa faz:
- {{texto_resumindo_o_escopo_e_modo}}

Onde ver o resultado:
- Painel de Routines do Claude (a saída de cada execução fica salva lá, você abre, copia o que precisa e monta o carrossel no Instagram)

Configuração local salva em:
{caminho_absoluto_para_o_arquivo_do_passo_7.2}

Para pausar:
   Abra o link acima e desabilite, ou rode /schedule update {{schedule_id}} com enabled=false

Para deletar:
   Acesse https://claude.ai/code/routines pela web (a API atual não suporta delete via CLI)

Para criar outro agendamento (ex: para outro nicho ou outra frequência):
   /programar-carrossel-noticia
```

Se o GitHub do projeto não estiver conectado à conta Claude do aluno (avisado pela skill `/schedule` no momento da criação), adicione ao final da entrega:

```
⚠ Observação técnica: o GitHub do projeto não está conectado à sua conta Claude. Como esta tarefa só faz busca na web e gera texto (não precisa ler arquivos do repositório), ela vai rodar normalmente. Se quiser criar agendamentos futuros que dependam de arquivos do projeto, conecte o GitHub rodando /web-setup ou instalando o Claude GitHub App em https://claude.ai/code/onboarding?magic=github-app-setup.
```

Exiba o caminho do arquivo de configuração no formato copiável (texto, não link), conforme regra global do CLAUDE.md.

---

## Regras

- **Aprovação obrigatória.** Não chame `/schedule create` sem o `SIM` explícito no Passo 6.
- **Não exibir tokens.** Se a tarefa programada precisar de algum token (Telegram, OpenAI), referencie só o nome da variável de ambiente, nunca o valor.
- **Lero-lero proibido na configuração.** Quando montar a descrição do `nome` do agendamento, use dado concreto (nicho + frequência + handle), não genérico tipo "carrossel automático diário".
- **Sem auto-revisão de copy nesta skill.** A skill só configura. A copy real é gerada pela tarefa programada em runtime, e o prompt-base já carrega as proibições do Light Copy.
- **Reaproveitar contexto do produto ativo.** Se o perfil já tem handle, nicho e produto, ofereça como default no Passo 1. O aluno não deve digitar 3 vezes a mesma coisa.
- **Slug sem confirmação.** O `schedule_slug` é gerado automaticamente, não pergunte.

---

## Quando NÃO usar esta skill

- O aluno quer só **um** carrossel agora (sem agendamento recorrente). Nesse caso, use `/carrossel` (que pega Urgência Oculta do produto) ou rode o prompt de carrossel de notícia direto no chat.
- O aluno quer agendar **outra coisa** (resumo de tráfego, post viral, email). Use `/trafego-regras` ou crie outra skill específica.
- O aluno ainda não cadastrou produto. Use `/produto-novo` primeiro.

---

## Próximos passos sugeridos após criar o agendamento

Após o Passo 8, sugira no chat:

```
Próximos passos quando a primeira execução rodar:

1. Abra o painel de Routines do Claude e leia a saída
2. Copie o texto e os prompts visuais
3. Gere as imagens (Code Interpreter ou DALL-E) e poste no Instagram

Se quiser ajustar tom ou frequência depois, é só rodar /programar-carrossel-noticia de novo (vai criar outro agendamento) ou deletar o atual com /schedule delete {{schedule_id}}.
```
