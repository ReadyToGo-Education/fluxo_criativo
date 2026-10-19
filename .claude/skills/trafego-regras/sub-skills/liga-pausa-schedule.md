# Sub-fluxo. Liga e Pausa por Horário (programação de entrega do conjunto)

Configura o `adset_schedule` do conjunto para que ele entregue só nos dias e horários escolhidos. Útil para parar fora do horário comercial, no fim de semana ou de madrugada.

Passo 0 e gate: ver `SKILL.md` desta skill. Este sub-fluxo **roda pelo MCP** (`ads_update_entity`) e pelo App (`curl`).

## Perguntas que cobre

- "Programa para ligar minhas campanhas na segunda e pausar no domingo"
- "Pausa os anúncios entre meia-noite e 6h"
- "Quero rodar só de segunda a sexta, das 8h às 22h"
- "Pausa minha campanha no fim de semana inteiro"
- "Roda só no horário de pico do meu público (18h às 23h)"

## Inputs

| Input | Padrão | Descrição |
|---|---|---|
| `adset_id` | obrigatório | Conjunto (pode ser mais de um) |
| `dias_semana` | segunda a sexta | 0 = domingo, 1 = segunda, ..., 6 = sábado |
| `hora_inicio` | 08:00 | Quando a entrega começa |
| `hora_fim` | 22:00 | Quando a entrega termina |
| `timezone` | o da conta | Fuso usado pela Meta |

## Pré-requisito crítico: orçamento total

`adset_schedule` **só funciona com orçamento total** (`lifetime_budget`). Não funciona com orçamento diário (`daily_budget`).

**A skill confere ANTES de qualquer coisa**, lendo o orçamento do conjunto e da campanha (MCP: `ads_get_ad_entities`; App: `GET /<adset_id>?fields=daily_budget,lifetime_budget,end_time,effective_status,campaign{daily_budget,lifetime_budget}` com `curl -g`):

| Situação | O que fazer |
|---|---|
| Conjunto (ABO) com orçamento total e data de fim | Segue direto |
| Campanha com orçamento de campanha (CBO) | Quem precisa ter orçamento total é a **campanha**, não o conjunto. Se a campanha tem orçamento total, segue. Se tem orçamento diário, mesma conversa da linha abaixo, no nível da campanha |
| Conjunto com orçamento diário | Explicar e oferecer as saídas abaixo |

### Conjunto com orçamento diário: explicar antes

**Trocar orçamento diário por total num conjunto que já foi publicado costuma ser recusado pela Meta** (o tipo de orçamento é definido na criação). Por isso a skill não promete a conversão. Mostrar:

```
⚠️ O conjunto "{nome}" usa orçamento diário (R$ {X}/dia).
A programação por horário só funciona com orçamento TOTAL (um valor para o período
inteiro, com data de fim). Num conjunto que já foi publicado, a Meta costuma recusar
essa troca.

Como prefere seguir?

1. Criar um conjunto novo, igual a este, já com orçamento total e com a programação
   (nasce pausado; o original continua como está até você decidir)
2. Tentar converter este conjunto mesmo assim (se a Meta recusar, eu te aviso e
   voltamos para a opção 1)
3. Deixar como está (cancelo a programação)

Digite o número:
```

**Opção 1 (conjunto novo):**
- Pedir a data de fim ("Até quando esse conjunto deve rodar?") e calcular o orçamento total: `lifetime_budget = daily_budget × dias até a data de fim`.
- **MCP:** criar a cópia com `ads_create_ad_set` passando `source_adset_id` (copiar de existente) e os campos novos que o schema aceitar (orçamento total, data de fim, `adset_schedule`, `pacing_type`, status pausado); depois os anúncios com `ads_create_ad` e `source_ad_id`. Se a cópia falhar, **duplicação guiada no Gerenciador**: o aluno duplica o conjunto, define orçamento total, data de fim e "Programação de veiculação" na cópia, deixa pausada, e a skill confere pela leitura. (No MCP, `ads_get_ad_entities` não devolve a segmentação do conjunto, então não dá para "ler e recriar" pelo conector.)
- **App:** seguir o padrão "ler e recriar" da seção "Lições de campo" de `.claude/skills/trafego-testes/sub-skills/ab-generico.md` (ler a configuração por `GET`, criar o conjunto com `targeting_automation.advantage_audience`, orçamento total, `end_time`, `adset_schedule` e status `PAUSED`, e criar os anúncios apontando para o `creative_id` existente). `/copies` só para conjunto com 1 anúncio.
- Tudo num bloco 🛡️ só (um lote). Pausar o conjunto original fica a critério do aluno, em outra confirmação.

**Opção 2 (tentar converter):**
- Pedir a data de fim (orçamento total exige `end_time`) e calcular `lifetime_budget = daily_budget × dias`.
- Bloco 🛡️ com a conversão e a programação no mesmo lote (conversão primeiro). MCP: `ads_update_entity` com `lifetime_budget` e `end_time`, depois `adset_schedule` + `pacing_type`. App: `POST /<adset_id>`.
- Se a Meta recusar a troca, parar, mostrar o motivo em linguagem simples e oferecer a opção 1.

## Endpoint

> **Roteamento por modo:** `adset_schedule` é campo do conjunto. **MCP:** `ads_update_entity` com `adset_schedule` + `pacing_type` (conforme o schema da tool). **App:** o `curl` abaixo. Lista de conjuntos para escolher: `ads_get_ad_entities` (MCP) ou `GET /act_<id>/adsets` (App).

```
POST /<adset_id>
{
  "adset_schedule": [
    { "start_minute": 480, "end_minute": 1320, "days": [1, 2, 3, 4, 5] }
  ],
  "pacing_type": ["standard", "day_parting"]
}
```

`start_minute` e `end_minute` são minutos desde a meia-noite:
- 0 = 00:00
- 360 = 06:00
- 480 = 08:00
- 720 = 12:00
- 1080 = 18:00
- 1320 = 22:00
- 1440 = 24:00 (dia seguinte)

Vários blocos no mesmo dia são permitidos (ex: 8h às 12h e 14h às 18h):
```json
[
  { "start_minute": 480,  "end_minute": 720,  "days": [1,2,3,4,5] },
  { "start_minute": 840,  "end_minute": 1080, "days": [1,2,3,4,5] }
]
```

## Receitas prontas

### Receita 1. Horário comercial (segunda a sexta, 8h às 22h)
```yaml
days: [1,2,3,4,5]
start_minute: 480   # 08:00
end_minute: 1320    # 22:00
```

### Receita 2. Sem fim de semana (segunda a sexta, 24h)
```yaml
days: [1,2,3,4,5]
start_minute: 0
end_minute: 1440
```

### Receita 3. Sem madrugada (todo dia, 6h às 23h)
```yaml
days: [0,1,2,3,4,5,6]
start_minute: 360   # 06:00
end_minute: 1380    # 23:00
```

### Receita 4. Só fim de semana (sábado e domingo, 9h às 23h)
```yaml
days: [0,6]
start_minute: 540   # 09:00
end_minute: 1380    # 23:00
```

### Receita 5. Personalizada
O aluno define dias e horários.

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**.

### Ordem fixa

1. **Conjunto.** "Qual conjunto você quer programar? (digite o nome, completo ou em parte, ou peça para eu listar)". Aceita (mesmo padrão da coleta por nome da `regra-automatica.md`):
   - **(a) Nome, completo ou em parte:** listar conjuntos (MCP `ads_get_ad_entities`; App `GET /act_<id>/adsets?fields=name,status,effective_status,daily_budget,lifetime_budget`) e procurar o trecho. 1 resultado: confirmar. Vários: lista numerada.
   - **(b) Listar:** conjuntos ativos e pausados dos últimos 90 dias, com nome, status e orçamento.
   - **(c) ID direto** (raro): conferir e confirmar.

   **O aluno nunca digita ID sem ter sido pedido.**

2. **Conferir o orçamento** (sem pergunta, ver "Pré-requisito crítico"). Se for orçamento diário, mostrar as 3 saídas agora, antes de coletar o resto: não adianta montar a programação se o aluno vai cancelar.

3. **Receita.** Mostrar as 5 receitas numeradas.

4. **Dias.** *Só na receita 5.* Lista numerada: segunda a sexta, todos os dias, só fim de semana, personalizado (números de 0 = domingo a 6 = sábado, separados por vírgula).

5. **Horários.** *Só na receita 5.* Uma pergunta por vez:
   - Hora de início (HH:MM, ex: 08:00)
   - Hora de fim (HH:MM, ex: 22:00)

6. **Onde aplicar.**
   ```
   Quer aplicar essa programação:
   1. Só nesse conjunto
   2. Em todos os conjuntos ativos da campanha {nome}
   3. Em todos os conjuntos ativos da conta (cuidado: reset de aprendizado em todos)

   Digite o número:
   ```
   Nas opções 2 e 3, conferir o orçamento de cada conjunto. Os que tiverem orçamento diário ficam de fora, com aviso e as mesmas saídas.

**Proibido:** pedir `start_minute`, `end_minute`, `pacing_type` ou qualquer chave da Marketing API (sempre converter HH:MM internamente); agrupar inputs; pular para o resumo sem os passos 1 a 6.

## Resumo em linguagem natural (obrigatório, antes do bloco 🛡️)

```
📋 Antes de eu mexer no conjunto, um resumo do plano:

O que vai acontecer:
  O conjunto "{nome}" vai entregar só:
  - {dias em português, ex: "de segunda a sexta"}
  - {horário em português, ex: "das 08:00 às 22:00"}
  - Fuso: {fuso, ex: "horário de Brasília"}

  Fora desses horários, o conjunto fica parado sozinho.

Cobertura: {N} horas por semana de entrega, de 168 possíveis ({%}% do tempo).

{Se houver conversão ou conjunto novo:}
{Opção 1:} Antes, vou criar um conjunto novo igual ao "{nome}", com orçamento total
de R$ {Y} até {data de fim}, já com essa programação, pausado.
{Opção 2:} Antes, vou tentar trocar o orçamento de R$ {X}/dia para R$ {Y} no total
até {data de fim}. A Meta pode recusar.

Efeito colateral: isso reseta o aprendizado do conjunto. Evite se a campanha está em
fase de aprendizado, a não ser que a perda de dado compense.

Para desfazer (voltar a entregar 24 horas): te passo o caminho depois.

Está certo? (sim segue para a confirmação final, não cancela aqui)
```

**Tradução obrigatória:**

| Campo técnico | Tradução |
|---|---|
| `days: [1,2,3,4,5]` | "de segunda a sexta" |
| `days: [0,6]` | "sábado e domingo" |
| `days: [0,1,2,3,4,5,6]` | "todos os dias" |
| `start_minute: 480` | "08:00" |
| `end_minute: 1320` | "22:00" |
| `start_minute: 0` + `end_minute: 1440` | "24 horas (o dia inteiro)" |
| `lifetime_budget: 500000` (centavos) | "R$ 5.000 no total" |
| `daily_budget: 5000` (centavos) | "R$ 50/dia" |
| `pacing_type: day_parting` | "entrega controlada por horário" |

**Proibido no resumo:** minutos desde a meia-noite, dias como `[1,2,3,4,5]`, valores em centavos, chaves da Marketing API.

## Preview YAML (dentro do bloco 🛡️)

```yaml
sub_fluxo: liga_pausa_schedule
modo: MCP_CONECTOR | APP
conjunto: "[Conjunto] LAL1pct 25-44"
orcamento_atual: total de R$ 5.000
acao_orcamento: nenhuma | conjunto_novo_com_orcamento_total | tentar_conversao

programacao:
  dias: [1, 2, 3, 4, 5]                # segunda a sexta
  janela: 08:00 às 22:00               # 14h por dia
  fuso: America/Sao_Paulo
  horas_semanais: 70                   # de 168 (semana inteira) = 41% do tempo

efeitos_esperados:
  - entrega_parada_fora_do_horario: sim
  - reset_aprendizado: SIM (mudança de ritmo de entrega)
  - orcamento_diario_equivalente: R$ 5.000 / 7 dias / (70/168) = cerca de R$ 1.714 por dia de entrega
```

## Depois de aplicar

```
✅ Programação aplicada: [Conjunto] LAL1pct 25-44

Agora o conjunto entrega só:
- De segunda a sexta
- Das 08:00 às 22:00 (horário de Brasília)

Reset de aprendizado disparado.
Próxima reanálise sugerida: 48h depois da primeira execução da programação.

Para desfazer (voltar a rodar 24 horas): /trafego-regras → opção 2 → escolher o
conjunto → "tirar a programação" (bloco 🛡️ próprio). Por baixo, isso grava
`adset_schedule` vazio e `pacing_type` padrão no conjunto.

Para ver a entrega ao longo do dia depois de 7 dias:
   /trafego-analise → Timing & Sazonalidade
```

## Vários conjuntos de uma vez

A mesma programação pode ir para vários conjuntos (passo 6). Todos entram num único bloco 🛡️ (um lote). Conjuntos com orçamento diário ficam de fora com aviso.

## Avisos

- **Reset de aprendizado.** Toda mudança de programação reseta. Evitar em campanha em aprendizado, a não ser que a perda compense.
- **O fuso é o da conta de anúncios**, não do produto. Conferir em `ads_get_ad_accounts` (MCP) ou `GET /act_<id>?fields=timezone_name` (App).
- **Orçamento total exige data de fim.** Sem ela, a skill pergunta ou não aplica.
- **Trocar orçamento diário por total num conjunto publicado costuma ser recusado.** A skill confere antes e oferece o conjunto novo.
- **A entrega não começa no minuto exato.** Pode levar até 30 min depois do início (leilão).
- **Campanha com orçamento de campanha (CBO):** o orçamento total precisa estar na campanha. Conferir a campanha, não o conjunto.
