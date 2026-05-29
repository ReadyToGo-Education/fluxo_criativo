# Sub-fluxo. Regra Automática Meta Ads

Cria uma Automated Rule no Meta Ads que avalia campanhas/adsets/ads contra um trigger e executa uma das 6 ações disponíveis:

- **Pausar** o adset/campanha automaticamente
- **Aumentar budget de ADSET** em % (escalar vencedor — só ABO, adset com budget próprio)
- **Reduzir budget de ADSET** em % (desacelerar perdedor — só ABO)
- **Aumentar budget de CAMPANHA** em % (escalar vencedor — CBO ou ABO, mexe na campanha inteira)
- **Reduzir budget de CAMPANHA** em % (desacelerar perdedor — CBO ou ABO)
- **Só notificar** (envia email pro admin do BM, não toca na campanha)

As 6 ações usam o mesmo endpoint (`POST /act_<id>/adrules_library`) e diferem apenas no campo `execution_spec.execution_type` (`PAUSE`, `CHANGE_BUDGET`, `CHANGE_CAMPAIGN_BUDGET`, `NOTIFICATION`). No painel do Gerenciador, todas aparecem misturadas em "Regras Automatizadas".

## Perguntas que cobre

- "Cria uma regra automática: se CPA passar de R$ 40, pausa o ad set"
- "Configura pra aumentar orçamento em 15% se ROAS estiver acima de 3"
- "Pausa anúncio se CTR cair abaixo de 0.5%"
- "Me notifica se gasto da campanha passar de R$ 500/dia"

## Inputs

### Trigger
| Campo | Opções |
|---|---|
| `metrica` | `cost_per_action_type:purchase` (CPA), `cost_per_action_type:lead` (CPL), `purchase_roas`, `ctr`, `frequency`, `spend`, `cpm`, `cpc` |
| `operador` | `GREATER_THAN`, `LESS_THAN` |
| `valor` | numérico em reais ou unidade da métrica |
| `janela_lookback` | `LAST_3_DAYS`, `LAST_7_DAYS`, `LAST_14_DAYS`, `LAST_30_DAYS`, `MAXIMUM`, `LIFETIME` |
| `gasto_minimo` | (recomendado) gasto mínimo na janela para a regra avaliar (evita decidir com pouco dado) |

### Ação
| Opção semântica (aluno escolhe) | Execution type usado (skill resolve sozinha no passo 3.5) | Campos | Quando usar |
|---|---|---|---|
| Pausar | `PAUSE` | nenhum | Cortar gasto ruim automaticamente (ex: CPA estourou) |
| Aumentar orçamento (+%) | `CHANGE_BUDGET` se ABO, `CHANGE_CAMPAIGN_BUDGET` se CBO | `change_spec: {amount: <int positivo>, unit: "PERCENTAGE"}` | Escalar vencedor (default +20%). Auto-detecta CBO/ABO. Validado em produção 2026-05-19. |
| Reduzir orçamento (−%) | `CHANGE_BUDGET` se ABO, `CHANGE_CAMPAIGN_BUDGET` se CBO | `change_spec: {amount: <int negativo>, unit: "PERCENTAGE"}` + `min_daily_budget` **obrigatório** | Desacelerar perdedor (default −20%). Piso mínimo de R$ 30/dia (ou 50% do budget atual) **obrigatório** pra evitar regra cortar até zero. |
| Só me avisar por email | `NOTIFICATION` | `execution_options[{field: "user_ids", value: [<user_id_admin_BM>]}]` | Só alertar, sem mexer na campanha (monitoramento, oportunidade) |

### Scope
| Tipo | Como funciona |
|---|---|
| `CAMPAIGN_IDS` | regra aplica em campanhas específicas |
| `ADSET_IDS` | regra aplica em adsets específicos |
| `AD_IDS` | regra aplica em ads específicos |
| `ALL_ACTIVE` | todas as campanhas/adsets/ads ativos da conta |
| `ALL_ACTIVE` + `filter` | filtro por objective, name pattern, etc. |

## Endpoint

Todas as 4 ações usam o mesmo `POST /act_<id>/adrules_library`. A estrutura de `evaluation_spec` (trigger) é idêntica nos 4 casos. O que muda é o bloco `execution_spec`. Abaixo, os 3 variantes de `execution_type`:

**Estrutura do `filters[]`** (vale pras 3 variantes abaixo): cada filter é um objeto independente com `field`/`value`/`operator`. O `time_preset` **NÃO** entra dentro do filter de métrica — ele é um **filter próprio**, separado, com `field: "time_preset"`. Erro confirmado em produção (Meta retorna `Invalid keys "time_preset" were found in param "evaluation_spec[filters][N]"`).

**Status inicial**: usar `"status": "DISABLED"` no payload. O painel do Gerenciador exibe esse estado como "Pausada" (em PT-BR), mas o valor aceito pela API é `DISABLED`. Os valores válidos do enum são `ENABLED`, `DISABLED`, `DELETED`, `HAS_ISSUES`. Não existe `PAUSED` (erro confirmado em produção).

### Variante 1: PAUSE

```
POST /act_<id>/adrules_library
{
  "name": "[FC] AutoRule-PauseCPAGT40-curso-tarot",
  "evaluation_spec": {
    "evaluation_type": "SCHEDULE",
    "filters": [
      { "field": "entity_type",  "value": "ADSET",                                         "operator": "EQUAL" },
      { "field": "campaign.id",  "value": ["<campaign_id>"],                               "operator": "IN" },
      { "field": "time_preset",  "value": "LAST_3_DAYS",                                   "operator": "EQUAL" },
      { "field": "cost_per_action_type:offsite_conversion.fb_pixel_purchase",
                                 "value": 40.0,                                            "operator": "GREATER_THAN" },
      { "field": "spent",        "value": 5000,                  // R$ 50 em centavos       "operator": "GREATER_THAN" }
    ]
  },
  "execution_spec": {
    "execution_type": "PAUSE"
  },
  "schedule_spec": { "schedule_type": "SEMI_HOURLY" },
  "status": "DISABLED"                       // aparece como "Pausada" no painel
}
```

### Variante 2: CHANGE_BUDGET (+/−)

> **Pré-requisitos críticos** (confirmados em produção):
> 1. `entity_type` no `evaluation_spec.filters[]` **deve** ser `ADSET`. CHANGE_BUDGET com `entity_type: CAMPAIGN` retorna erro `subcode 1815677: "Para o tipo de execução CHANGE_BUDGET, o tipo de entidade precisa ser ADSET."`
> 2. **Incompatível com CBO.** Em campanhas Advantage Campaign Budget (CBO), os adsets compartilham o budget da campanha e não têm budget próprio. CHANGE_BUDGET via Marketing API não tem nada onde agir. A skill **bloqueia** essa combinação (ver "Validação antes de criar" abaixo).
> 3. O campo correto é `change_spec` (não `change_strategy`/`value`). Tentativas anteriores com `change_strategy` retornam `"Unrecognized execution option field"`.

```
"execution_spec": {
  "execution_type": "CHANGE_BUDGET",
  "execution_options": [
    {
      "field": "change_spec",
      "value": {
        "amount": 20,           // inteiro positivo (escalar) ou negativo (desacelerar)
        "unit": "PERCENTAGE"    // ou "ABSOLUTE" (em centavos da moeda da conta)
      },
      "operator": "EQUAL"
    }
  ]
}
```

Outros campos opcionais do `change_spec` (não usados no MVP):
- `limit`: teto (em centavos) que o ajuste não pode ultrapassar.
- `target_field`: campo do adset onde aplicar (`daily_budget` default).

### Variante 3: CHANGE_CAMPAIGN_BUDGET (+/−)

Funciona em campanhas CBO **e** ABO. Mexe no orçamento da campanha inteira, não dos adsets individuais. É o único caminho automatizado pra ajustar budget de uma campanha CBO via Marketing API.

```
"execution_spec": {
  "execution_type": "CHANGE_CAMPAIGN_BUDGET",
  "execution_options": [
    {
      "field": "change_spec",
      "value": {
        "amount": -10,          // inteiro positivo (escalar) ou negativo (desacelerar)
        "unit": "PERCENTAGE"
      },
      "operator": "EQUAL"
    }
  ]
}
```

⚠️ **Pré-requisito:** `entity_type` no `evaluation_spec.filters[]` deve ser `CAMPAIGN` (não `ADSET`). Use `campaign.id` como filtro de escopo.

Validado em produção 2026-05-19 com esse payload — Meta aceitou e retornou rule ID válido. Caso de teste completo em `entregas/trafego/regras/<rule_id>.md`.

### Variante 4: NOTIFICATION

```
"execution_spec": {
  "execution_type": "NOTIFICATION",
  "execution_options": [
    { "field": "user_ids",
      "value": ["<user_id_admin_BM>"],       // 1 ou mais admins do BM
      "operator": "EQUAL" }
  ]
}
```

O resto do payload (`name`, `evaluation_spec`, `schedule_spec`, `status`) é idêntico nos 3.

## Presets de trigger (atalhos comuns)

A skill oferece 6 presets de **trigger** (apenas a condição). A **ação** é escolhida em passo separado (passo 4 da seção "Padrão de coleta"), permitindo combinar qualquer trigger com qualquer ação (pausar, mexer no budget, ou só notificar).

| Código | Trigger | Default sugerido |
|---|---|---|
| **T1** | CPA passar de X | 1.4× ticket (na janela média da trilha) |
| **T2** | CTR cair abaixo de X | 0.5% |
| **T3** | ROAS passar de X | 3.0 |
| **T4** | Frequência passar de X | 4 |
| **T5** | Gasto diário passar de X | R$ 500 |
| **T6** | Personalizado | aluno define métrica, operador, valor e janela |

### Combinações típicas (trigger × ação)

| Trigger | Ação | Resultado prático |
|---|---|---|
| T1 (CPA alto) | Pausar | Pausa adset que tá pesando no CPA |
| T1 (CPA alto) | Só notificar | Recebe alerta preventivo antes de pausar manual |
| T2 (CTR baixo) | Pausar | Pausa anúncio cansado |
| T2 (CTR baixo) | Só notificar | Sabe que o criativo cansou pra decidir trocar |
| T3 (ROAS alto) | +20% budget | Escala vencedor automaticamente |
| T3 (ROAS alto) | Só notificar | Recebe alerta de oportunidade, decide se escala manual |
| T4 (Frequência alta) | Pausar | Evita saturar audiência |
| T5 (Gasto alto) | Só notificar | Monitora gasto sem cortar nada |
| T5 (Gasto alto) | −20% budget | Desacelera automaticamente |

A skill apresenta os 6 presets de trigger e deixa o aluno escolher o trigger primeiro, a ação depois.

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Reforça a regra global do CLAUDE.md.

### Ordem fixa

1. **Trigger.** Mostrar os 6 presets numerados (T1-T6 da seção "Presets de trigger" acima). Aluno digita o número.

2. **Trigger custom.** *Só se trigger = T6 (personalizado).* Em sequência (1 pergunta cada):
   - Métrica (lista numerada: CPA, CPL, ROAS, CTR, frequência, gasto, CPM, CPC)
   - Operador (numerada: maior que / menor que)
   - Valor (em reais ou unidade da métrica)
   - Janela de avaliação (numerada: 3d, 7d, 14d, 30d, MAXIMUM, LIFETIME)

3. **Escopo (campanha/adset alvo).** Pergunta neutra: "Aplicar essa regra em qual campanha/adset?". Aceita 3 modos (mesmo padrão da [`ab-generico` Helper de molde](../../trafego-testes/sub-skills/ab-generico.md#padrão-de-coleta-de-inputs-uma-pergunta-por-mensagem)):
   - **(a) Nome (total ou parcial):** `GET /act_<id>/campaigns?fields=name,status,effective_status` (ou `/adsets`) → match case-insensitive `contains`. 1 match: confirma. Múltiplos: lista numerada filtrada.
   - **(b) Listar:** "lista", "não lembro" → mostra campanhas/adsets ACTIVE/PAUSED dos últimos 90d.
   - **(c) Todas ativas com filtro:** "todas com objective=OUTCOME_SALES" ou similar.
   - **(d) ID direto** (raro): valida e confirma.

   **Aluno nunca digita ID cru sem ter sido pedido.**

3.5. **Detecção automática CBO/ABO** (transparente pro aluno, sem pergunta). *Só roda se aluno já escolheu uma campanha alvo (não "todas com filtro").* Antes do passo 4, fazer:
   ```
   GET /<campaign_id>?fields=daily_budget,lifetime_budget
   ```
   - Se `daily_budget` ou `lifetime_budget` da campanha > 0 → marcar como **CBO**.
   - Se vazios → marcar como **ABO**.
   - Guardar resultado pra rotear ação no payload + mostrar info no resumo natural.

4. **Ação.** *Sempre presente.* Pergunta numerada, **4 opções únicas** (a skill resolve sozinha se vai virar CHANGE_BUDGET ou CHANGE_CAMPAIGN_BUDGET conforme o passo 3.5):
   ```
   O que você quer que essa regra faça quando o trigger bater?

   1. Pausar adset/campanha automaticamente
   2. Aumentar orçamento (em %)
   3. Reduzir orçamento (em %)
   4. Só me avisar por email (sem mexer na campanha)

   Digite o número:
   ```

   - **Se 1 (PAUSE):** segue direto pro passo 6 (gasto mínimo). Sem inputs adicionais aqui.
   - **Se 2 (aumentar) ou 3 (reduzir):** pedir o percentual (default sugerido: ±20%, alinhado com cap anti-reset). Roteamento automático conforme passo 3.5:
     - **ABO** → `execution_type: CHANGE_BUDGET`, `entity_type: ADSET` no filter.
     - **CBO** → `execution_type: CHANGE_CAMPAIGN_BUDGET`, `entity_type: CAMPAIGN` no filter.
     - **Escopo "todas ativas" sem campanha específica:** assumir CBO (mais defensivo, funciona nos dois). Avisar: "vou usar CHANGE_CAMPAIGN_BUDGET porque escopo é amplo".
   - **Se 4 (NOTIFICATION):** vai pro passo 5 (subscribers), pula direto pro passo 6 depois.

   **A skill nunca pergunta "ADSET ou CAMPANHA?" ao aluno** — isso é decisão técnica que ela toma sozinha com o GET do passo 3.5.

5. **Subscribers (quem recebe o email).** *Só se ação = 4 (NOTIFICATION).* Pergunta numerada:
   ```
   Quem deve receber o alerta por email?

   1. Só você (admin do BM, descoberto via GET /me?fields=id)
   2. Você + outros admins do BM (mostro a lista)
   3. Adicionar outros admins do BM por nome

   Digite o número:
   ```
   - **Se 1:** salva o `user_id` do aluno como subscriber.
   - **Se 2 ou 3:** listar admins humanos da conta de anúncios via:
     ```
     GET /act_<id>/assigned_users?business=<bm_id>&fields=id,name,user_type,tasks
     ```
     **Filtrar `user_type == business_user`** (descartar `system_user`). Apresentar lista numerada com `name`, aluno escolhe.

     **NÃO usar `GET /<bm_id>/business_users`** — esse endpoint retorna `data: []` quando o token é de System User (caso padrão do curso). Erro confirmado em produção.

   - Se for a primeira vez, salvar `META_USER_ID` no `.env` pra cachear.

6. **Gasto mínimo (guard clause).** Pergunta direta:
   ```
   Quer adicionar gasto mínimo na janela pra evitar regra disparar com 1 conversão? (recomendado)

   1. Sim, usar default sugerido (4× CPA target)
   2. Sim, eu digito o valor
   3. Não (assumo o risco de regra com dado imaturo)

   Digite o número:
   ```
   Se (2): pedir valor em reais.

7. **Nome.** Sugerir nome auto-gerado seguindo `[FC] AutoRule-{tipo}-{slug}` (onde `{tipo}` = PauseCPAGT40, Boost20PctROAS3, AlertCPLGT15, etc., conforme ação) e perguntar "uso esse ou você prefere outro?". Aluno aprova ou edita.

**Proibido:**
- Pedir `evaluation_spec`, `filters[]`, `time_preset`, `entity_type`, `execution_spec`, `subscribers[]`, `user_id` ou qualquer chave da Marketing API direto ao aluno.
- Agrupar 2+ inputs na mesma mensagem.
- Pular pro Preview YAML sem passar pelos passos aplicáveis (1, 3, 4, 6, 7 sempre; 2 só se trigger = T6; 5 só se ação = 4).

## Validação antes de criar

Antes do POST, a skill valida:

1. **Trigger faz sentido?** Ex: "CPA > R$ 1" em produto de R$ 500 vai pausar tudo na primeira venda. Limiares de sanidade (avisa mas não bloqueia, aluno digita "sim" pra forçar):
   - `CTR < 0.3%` → "esse CTR é muito baixo, regra pode nunca disparar — tem certeza?"
   - `CPA < ticket/2` → "esse CPA é menor que metade do seu ticket ({ticket}/2 = R$ {valor}) — regra vai pausar tudo na primeira venda. Tem certeza?"
   - `ROAS > 20` → "ROAS > 20 é extremamente alto, regra pode nunca disparar — tem certeza?"
   - `frequência < 1` ou `frequência > 10` → "frequência fora do range típico (1-10) — tem certeza?"
2. **Gasto mínimo definido?** Sem isso, regra dispara com 1 conversão.
3. **Janela compatível com ticket?** High ticket (≥ R$1.500) precisa de janela ≥ 7 dias.
4. **Não conflita com outra regra ativa?** Listar regras existentes e checar overlap.
5. **Sanity check do roteamento CBO/ABO.** *Só se ação ∈ {2 (aumentar), 3 (reduzir)}.* A detecção foi feita no passo 3.5; aqui só validamos que nada mudou entre lá e o POST.

   - Re-fazer `GET /<campaign_id>?fields=daily_budget,lifetime_budget`.
   - Comparar com o resultado do passo 3.5:
     - **Mesmo resultado** (continua CBO ou continua ABO) → seguir.
     - **Mudou** (raro, mas pode acontecer se aluno migrou CBO↔ABO no Gerenciador no meio do fluxo) → avisar e perguntar:
       ```
       ⚠️ A campanha mudou de estrutura desde que eu chequei (era {CBO|ABO},
       agora é {ABO|CBO}). Vou refazer o roteamento da regra.

       Posso continuar? (sim/não)
       ```

   Com a auto-detecção do passo 3.5, **não existe mais a combinação "CHANGE_BUDGET + CBO" que precisava de bloqueio explícito** — a skill já escolhe o execution_type correto (`CHANGE_BUDGET` se ABO, `CHANGE_CAMPAIGN_BUDGET` se CBO) antes de chegar aqui.

Se algo falhar, exibe alerta:

```
⚠️ Atenção:

A regra que você quer criar pode ter problemas:

- "CPA > R$ 40" sem gasto mínimo pode pausar adsets com 1 venda boa que custou R$ 50.
  Recomendado adicionar: AND spend > R$ 200 (4× CPA target).

Quer que eu adicione esse gasto mínimo automaticamente?

1. Sim, usar default sugerido (R$ X = 4× CPA target da trilha)
2. Sim, eu digito o valor
3. Não, criar do jeito que pedi

Digite o número:
```

Se (2): pedir o valor em reais ("Qual o gasto mínimo, em R$?").

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

**Quando exibir:** sempre, depois de coletar todos os inputs (passos 1-7 aplicáveis da seção "Padrão de coleta") e DEPOIS da Validação. ANTES do Preview YAML.

**Por que existe:** o Preview YAML expõe `evaluation_spec`, `filters[]`, `time_preset`, IDs longos e valores em centavos. O aluno trava. Esse resumo traduz pro português corrente antes do bloco técnico.

**Formato fixo (varia conforme a ação escolhida):**

```
📋 Antes de eu criar essa regra na sua conta, deixa eu te resumir o plano:

O que eu vou criar:
  Uma regra automática em PAUSED chamada "{nome}".

O que ela faz:
  A cada 30 minutos, o Meta vai olhar {escopo em português,
  ex: "todos os seus 12 adsets ativos com objetivo de vendas"} e,
  se {trigger em português, ex: "o CPA dos últimos 3 dias passar de R$ 40
  E o gasto na mesma janela for maior que R$ 200"},
  vai {AÇÃO em português, conforme a opção escolhida:
    [1 PAUSE]      "pausar o adset/campanha automaticamente"
    [2 BOOST]      "aumentar o orçamento em 20%" (skill aplica em adset ou campanha conforme estrutura)
    [3 BRAKE]      "reduzir o orçamento em 20%" (idem)
    [4 NOTIFY]     "te enviar um email (sem mexer na campanha)"
  }.

{Se ação ∈ {2 BOOST, 3 BRAKE}, adicionar:}
Orçamento atual da {campanha|adset}: R$ {valor_atual}
Depois do disparo: R$ {valor_pos_disparo} (cálculo: R$ {valor_atual} × {fator})
{Se ação = 3 BRAKE:}
Piso mínimo garantido: R$ {min_daily_budget} (a regra não vai cortar abaixo desse valor)

{Se ação = NOTIFY, adicionar:}
Onde a notificação chega:
  - Email pro admin do BM (você + {N} pessoas adicionadas)
  - Push no Ads Manager mobile (se você tem o app instalado)
  - Sino do business.facebook.com

Cobertura agora: {N} {campanhas|adsets|ads} ativos seriam avaliados nesse momento.

Cooldown: depois de {agir|te avisar} em uma entidade, espera {24h|1h} antes
de {agir|avisar} nela de novo. (24h pra ações que mexem; 1h pra notificações.)

{Se ação = NOTIFY:}
Importante: essa regra NÃO pausa nem mexe nas campanhas, só te avisa.
Se você quiser ação automática quando o trigger bater, escolha a opção
1 (pausar) ou 2/3 (mexer no budget) em vez de "só notificar".

Para reverter: te passo o comando de DELETE depois que criar.

Tá certo? (sim segue pro YAML, não cancela aqui)
```

**Regras de tradução obrigatórias:**

| Campo técnico | Tradução pro resumo |
|---|---|
| `cost_per_action_type:purchase` | "CPA (custo por compra)" |
| `cost_per_action_type:lead` | "CPL (custo por lead)" |
| `purchase_roas` | "ROAS (retorno sobre investimento)" |
| `ctr` | "CTR (taxa de clique)" |
| `frequency` | "frequência (vezes que cada pessoa viu o anúncio)" |
| `spend` | "gasto" |
| `cpm` | "CPM (custo por mil impressões)" |
| `cpc` | "CPC (custo por clique)" |
| `GREATER_THAN` | "passar de" / "ficar acima de" |
| `LESS_THAN` | "cair abaixo de" |
| `LAST_3_DAYS` | "últimos 3 dias" |
| `LAST_7_DAYS` | "última semana" |
| `LAST_30_DAYS` | "últimos 30 dias" |
| `MAXIMUM` | "tempo todo de vida da campanha" |
| `PAUSE` | "pausar" |
| `CHANGE_BUDGET +20%` ou `CHANGE_CAMPAIGN_BUDGET +20%` | "aumentar o orçamento em 20%" (skill escolhe internamente o execution_type baseado em CBO/ABO) |
| `CHANGE_BUDGET -20%` ou `CHANGE_CAMPAIGN_BUDGET -20%` | "reduzir o orçamento em 20%" (idem) |
| `NOTIFICATION` | "te notificar (sem mudar nada na campanha)" |
| `SEMI_HOURLY` | "a cada 30 minutos" |
| `spent: 5000` (centavos) | "R$ 50" (sempre converter) |
| `ALL_ACTIVE + filter` | tradução do filtro em português ("todas as campanhas ativas com objetivo de vendas") |

**Proibido neste resumo:**
- Mostrar IDs, hashes, chaves da Marketing API, valores em centavos.
- Usar inglês técnico (`adset`, `bidding`, `evaluation_type`).
- Pular esse resumo pra ir direto pro YAML.

**Comportamento depois:**
- "sim" → segue pro Preview YAML.
- "não" → "1. Quer ajustar algo, 2. cancelar de vez?". Se ajustar, volta ao passo da coleta correspondente.

## Preview YAML

O bloco `acao` varia conforme a opção escolhida no passo 4. As demais seções (trigger, scope, cooldown) são iguais nos 4 casos.

### Exemplo com ação PAUSE

```yaml
sub_fluxo: regra_automatica
nome_final: "[FC] AutoRule-PauseCPAGT40-curso-tarot"
status_inicial: PAUSED

trigger:
  metrica: cost_per_action_type:purchase
  operador: GREATER_THAN
  valor: 40.0 (BRL)
  janela: LAST_3_DAYS
  guard_clause: spend > R$ 200 na mesma janela

acao:
  tipo: PAUSE
  alvo: adset

scope:
  tipo: ALL_ACTIVE
  filtro: objective=OUTCOME_SALES
  cobertura: 12 adsets ativos serão avaliados

cooldown: 24h
frequencia_avaliacao: a cada 30 min

confirma criar como PAUSED? (digite SIM)
```

### Exemplo com ação CHANGE_BUDGET (+/−) — adset ABO

Mesma estrutura, trocando o bloco `acao` e garantindo que `entity_type` no trigger é `ADSET`:

```yaml
acao:
  tipo: CHANGE_BUDGET
  delta_percentual: +20                # negativo para reduzir
  alvo: adset                          # OBRIGATÓRIO ser adset
  change_spec: {amount: 20, unit: PERCENTAGE}

trigger:
  entity_type: ADSET                   # OBRIGATÓRIO ser ADSET nesse payload
  ...
```

⚠️ **Compatibilidade:** só funciona em **adsets de campanhas ABO**. Em CBO, usar a variante `CHANGE_CAMPAIGN_BUDGET` abaixo.

### Exemplo com ação CHANGE_CAMPAIGN_BUDGET (+/−) — campanha CBO ou ABO

Mesma estrutura, trocando o bloco `acao` e `entity_type: CAMPAIGN`:

```yaml
acao:
  tipo: CHANGE_CAMPAIGN_BUDGET
  delta_percentual: -10                # negativo para reduzir, positivo para escalar
  alvo: campanha                       # OBRIGATÓRIO ser CAMPAIGN
  change_spec: {amount: -10, unit: PERCENTAGE}

trigger:
  entity_type: CAMPAIGN
  campaign_id: ["<campaign_id>"]
  ...
```

⚠️ **Compatibilidade:** funciona em CBO **e** ABO. Em CBO mexe no budget da campanha (que é onde está). Em ABO mexe no budget da campanha (afeta todos os adsets daquela campanha proporcionalmente). Único caminho automatizado pra ajustar budget de CBO. Validado 2026-05-19.

### Exemplo com ação NOTIFICATION

Mesma estrutura, trocando o bloco `acao` (e cooldown menor):

```yaml
acao:
  tipo: NOTIFICATION
  destinatarios:
    - admin do BM: {nome}
    - {outros admins, se houver}
  canal: email + push Ads Manager mobile + sino business.facebook.com

cooldown: 1h   # menor pra notificações (não bloqueia learning)
```

## Após criar

Mensagem em linguagem natural — **nunca expor curl/POST/DELETE direto pro aluno**. O aluno final não vai rodar comando na mão. Tudo é feito via menu da própria skill ou via Gerenciador de Anúncios.

Formato fixo:

```
✅ Pronto! A regra "{nome}" foi criada na sua conta, em modo PAUSADA (não está agindo ainda).

Onde você consegue ver e gerenciar:
   Gerenciador de Anúncios → menu lateral "Regras Automatizadas"
   Procure pelo nome "{nome}" (aparece com o prefixo "[FC] AutoRule-..." pra
   você identificar rápido entre suas outras regras).

🟢 Pra ATIVAR a regra (e começar a avaliar a cada 30 min):
   No Gerenciador, clica na linha da regra → muda o status pra "Ativa".
   Depois disso, o Meta começa a checar a cada 30 minutos e age sozinho quando o trigger bater.

📊 Pra ver QUANDO ela rodou e o que aconteceu (depois de ativada):
   No Gerenciador, clica na regra → aba "Histórico de Atividade".

✏️ Pra EDITAR (mudar trigger, ação, valor) ou EXCLUIR a regra:
   Tudo direto no painel do Gerenciador (linha da regra → botão de 3 pontos).

📝 Registrei tudo em: meus-produtos/{ativo}/trafego/regras/INDEX.md
   (Lá tem o ID técnico {rule_id} da regra. Não precisa pra uso normal, só serve
   caso você precise abrir ticket com suporte do Meta ou debug.)
```

### Atalho: ativar imediatamente (passo 9, opcional)

Logo após a mensagem "✅ Pronto!" acima, oferecer:

```
A regra nasceu PAUSADA por segurança. Quer ATIVAR agora pra ela começar a avaliar a cada 30 min?

1. Sim, ativar agora
2. Não, deixar pausada (ativo depois quando quiser, via /trafego-regras → [3] Gerir regras → B. Ativar)

Digite o número (Enter pra usar 2):
```

**Se 1 (Sim, ativar):**

- Apresenta gate 🛡️ resumido (aluno já aprovou a criação há segundos; gate aqui é só pra status change):
  ```
  🛡️ Confirmação rápida
  Operação: ativar a regra que acabamos de criar
  O que vai mudar: status PAUSADA → ATIVA
  Reversível? sim, via /trafego-regras → [3] → C. Pausar
  Pode aplicar? (sim/não)
  ```
- Se "sim": `POST /<rule_id> { "status": "ENABLED" }`. Mensagem final muda pra:
  ```
  ✅ Regra criada E ATIVADA. Já começou a avaliar a cada 30 min.
  Próxima execução prevista: ~30 min a partir de agora.
  ```
- Se "não": mensagem final do "Após criar" segue como está (regra fica PAUSADA).

**Se 2 (deixar pausada):** segue fluxo normal sem POST extra.

**Regras pro Claude ao gerar essa mensagem:**
- **Nunca** mostrar `POST /<id>` ou `DELETE /<id>` no texto principal. ID técnico fica só no INDEX local.
- Sempre referenciar **ação semântica** ("Ativar regra", "Excluir regra") via menu da skill, não payload da API.
- Mencionar o Gerenciador como caminho alternativo — aluno experiente prefere a UI nativa, aluno comum prefere a skill.
- O ID da regra pode aparecer **uma única vez** no fim, marcado como "ID técnico pra debug", pra aluno avançado ter acesso se precisar.

Convenção de nome por tipo de ação:

| Ação | Padrão do nome | Exemplo |
|---|---|---|
| PAUSE | `[FC] AutoRule-Pause{Metrica}{Op}{Valor}-{slug}` | `[FC] AutoRule-PauseCPAGT40-curso-tarot` |
| Aumentar orçamento (CHANGE_BUDGET ou CHANGE_CAMPAIGN_BUDGET) | `[FC] AutoRule-Boost{Delta}Pct{Metrica}{Op}{Valor}-{slug}` | `[FC] AutoRule-Boost20PctROASGT3-curso-tarot` |
| Reduzir orçamento (CHANGE_BUDGET ou CHANGE_CAMPAIGN_BUDGET) | `[FC] AutoRule-Brake{Delta}Pct{Metrica}{Op}{Valor}-{slug}` | `[FC] AutoRule-Brake20PctCPAGT40-curso-tarot` |
| NOTIFICATION | `[FC] AutoRule-Alert{Metrica}{Op}{Valor}-{slug}` | `[FC] AutoRule-AlertSpendGT500-curso-tarot` |

Skill registra no `INDEX.md` qual `execution_type` foi efetivamente usado (CHANGE_BUDGET ou CHANGE_CAMPAIGN_BUDGET), pra debug futuro. O aluno vê só o nome semântico (Boost/Brake), o detalhe técnico fica no INDEX.

Bloco adicional **só se ação = NOTIFICATION**:

```
Onde a notificação chega quando o trigger disparar:
  - Email: {seu email cadastrado no BM}
  - Mobile: notificação push no Ads Manager (se você tem o app)
  - Web: sino do business.facebook.com
```

## Avisos

**Pegadinhas da Marketing API confirmadas em produção:**
- **`status` no payload é `DISABLED`, não `PAUSED`.** Enum aceito: `ENABLED`, `DISABLED`, `DELETED`, `HAS_ISSUES`. O painel do Gerenciador rotula `DISABLED` como "Pausada" em PT-BR — daí a confusão. Internamente nos textos narrados pro aluno, dizer "regra pausada"/"em pausa" está OK; no payload JSON, **sempre** `DISABLED`.
- **`time_preset` é filter próprio, não chave aninhada.** Não embutir `"time_preset": "LAST_3_DAYS"` dentro do filter de métrica. Sempre adicionar um filter dedicado `{"field":"time_preset","value":"LAST_3_DAYS","operator":"EQUAL"}` no array `filters[]`. Meta valida em runtime e rejeita.
- **CHANGE_BUDGET usa `change_spec`, não `change_strategy`/`value` soltos.** Estrutura correta: `execution_options: [{field: "change_spec", value: {amount: 20, unit: "PERCENTAGE"}, operator: "EQUAL"}]`. Tentar `change_strategy` retorna `"Unrecognized execution option field change_strategy"`. Tentar `value` solto retorna `"Unrecognized execution option field value"`.
- **CHANGE_BUDGET exige `entity_type: ADSET`.** Com `entity_type: CAMPAIGN` Meta retorna `subcode 1815677: "Para o tipo de execução CHANGE_BUDGET, o tipo de entidade precisa ser ADSET."`
- **`CHANGE_BUDGET` (não `CHANGE_CAMPAIGN_BUDGET`) é incompatível com CBO.** Em CBO os adsets compartilham budget da campanha e não têm budget próprio — `CHANGE_BUDGET` não tem onde agir. Detectar antes do POST via `GET /<campaign_id>?fields=daily_budget,lifetime_budget`. Se algum > 0 na campanha, é CBO. Pra mexer no budget de uma CBO via regra automática, usar `CHANGE_CAMPAIGN_BUDGET` (ver Variante 3 da seção "Endpoint").
- **`CHANGE_CAMPAIGN_BUDGET` funciona em CBO e ABO.** Diferente do `CHANGE_BUDGET`, esse execution_type aceita `entity_type: CAMPAIGN` e mexe no orçamento da campanha inteira. Estrutura do `change_spec` é idêntica (`amount` + `unit`). Compatível com `evaluation_type: SCHEDULE` (igual ao `CHANGE_BUDGET`). Validado em produção 2026-05-19. Esse é o caminho que a UI do Gerenciador usa quando o aluno escolhe "Aplicar regra a: Todas as campanhas ativas" + "Reduzir/Aumentar orçamento".
- **`GET /<bm_id>/business_users` retorna `data: []` com token de System User.** É o caso padrão do curso (token permanente gerado via System User). Pra listar admins humanos da conta, usar: `GET /act_<id>/assigned_users?business=<bm_id>&fields=id,name,user_type,tasks` e filtrar `user_type == business_user`.

**Outros avisos:**
- **Regras Meta avaliam a cada 30 min** (default `SEMI_HOURLY`). Não é instantâneo.
- **Pausar via regra dispara reset de aprendizado** se a campanha estiver em fase de aprendizado ativa. Avisar.
- **Aumentar budget > 20% também dispara reset.** A skill recomenda cap de +20% por execução.
- **Limite Meta**: máximo de 200 regras por ad account (PAUSE + CHANGE_BUDGET + CHANGE_CAMPAIGN_BUDGET + NOTIFICATION somam pro mesmo limite).

---

## Funcionalidades adicionais do painel nativo (suportadas)

O painel do Gerenciador expõe 7 controles extras além de trigger + ação + escopo. Esta skill cobre todos via campos opcionais. Quando o aluno não menciona, usar default; se mencionar, perguntar como input adicional após o passo 4 (Ação) e antes do passo 6 (Gasto mínimo).

### A. Orçamento mínimo diário (guard pra CHANGE_BUDGET / CHANGE_CAMPAIGN_BUDGET)

**Aplica-se a:** ações 2 (aumentar) e 3 (reduzir) — qualquer alteração de budget.
**Por que existe:** evita regra reduzir budget abaixo de um piso onde a campanha pararia de entregar (caso de redução), ou opcionalmente limita teto (caso de aumento).
**Payload (campo extra em `execution_options`):**

```
{ "field": "min_daily_budget",
  "value": 3000,           // R$ 30,00 em centavos
  "operator": "EQUAL" }
```

**Comportamento:**

| Ação | Piso é... | Default | Skill pergunta? |
|---|---|---|---|
| 2 (Aumentar) | Opcional | Sem piso | Não — só pergunta se aluno mencionar |
| 3 (Reduzir) | **OBRIGATÓRIO** | maior entre R$ 30/dia e 50% do budget atual da campanha/adset | Não pergunta — aplica default e avisa no resumo |

**Pra ação 3 (Reduzir), a skill calcula o default automaticamente e mostra no resumo natural:**
```
Vou garantir que o orçamento não caia abaixo de R$ {default} por dia.
(Default é 50% do seu orçamento atual de R$ {valor_atual}, ou R$ 30 — o que for maior.)

Quer ajustar esse piso?
1. Não, manter R$ {default}
2. Quero outro valor (digito)
3. Desabilitar piso (assumo o risco de regra cortar até zero)

Digite o número (Enter pra manter default):
```

**Pra ação 2 (Aumentar):** se aluno mencionar "quero limitar o teto em R$ X", aplicar via campo análogo `max_daily_budget`. Caso contrário, não pergunta.

### B. Programação (Continuamente / Diariamente / Personalizado)

**Aplica-se a:** todas as ações.
**Mapeia pra `schedule_spec.schedule_type`:**
- Continuamente → `SEMI_HOURLY` (default da skill, avalia a cada 30 min)
- Diariamente → `DAILY` (avalia 1x por dia entre 0h00 e 1h00 do timezone da conta)
- Personalizado → `CUSTOM` (aluno escolhe dias da semana e janela horária)

**Pergunta ao aluno (após Ação):**
```
Com que frequência o Meta deve checar essa regra?

1. Continuamente — a cada 30 min (default, captura mudanças rápidas)
2. Diariamente — 1 vez por dia, entre 0h e 1h
3. Personalizado — escolho dias e horários

Digite o número:
```

Se (3): coletar dias da semana (0-6) e janela horária. Payload:
```
"schedule_spec": {
  "schedule_type": "CUSTOM",
  "schedule": [
    { "days": [1,2,3,4,5], "start_minute": 480, "end_minute": 1080 }
  ]
}
```

### C. Frequência de ação (12h / 24h / semana / customizado)

**Aplica-se a:** ações 1-5 (PAUSE, CHANGE_BUDGET, CHANGE_CAMPAIGN_BUDGET). Default da NOTIFICATION é 1h.
**Por que existe:** controla quantas vezes a regra pode **agir** na mesma entidade num período. Diferente do `schedule_spec` (frequência de avaliação) e do cooldown automático.
**Payload (campo extra em `execution_options`):**

```
{ "field": "execution_frequency",
  "value": "ONCE_PER_DAY",   // ou ONCE_EVERY_12_HOURS, ONCE_PER_WEEK, etc.
  "operator": "EQUAL" }
```

**Pergunta ao aluno (após Programação):**
```
Quantas vezes a regra pode agir na MESMA entidade?

1. Uma vez a cada 12 horas (padrão)
2. Uma vez por dia
3. Uma vez por semana
4. Sem limite (cuidado: pode causar loop)

Digite o número:
```

### D. Janela de avaliação (intervalo de tempo)

Já coberta no passo 2 (Trigger custom). Para presets T1-T5, default é `LAST_3_DAYS`. **Aviso adicional:** `MAXIMUM` na prática equivale a 37 meses (teto do Meta). Se aluno escolhe MAXIMUM, mencionar isso.

### E. Escopo `entity_type: AD` (terceiro escopo)

**Adicional ao passo 3 (Escopo).** Hoje a skill cobre CAMPAIGN e ADSET. Adicionar opção AD:

```
Aplicar essa regra em qual entidade?

1. Em uma campanha específica (ou todas ativas com filtro)
2. Em um conjunto específico (ou todos ativos)
3. Em um anúncio específico (ou todos ativos)

Digite o número:
```

Se (3): `entity_type: "AD"` no filter. Caso de uso: regra que pausa anúncios com CTR < 0.3% sem mexer no adset/campanha.

**⚠️ Limitação:** `entity_type: AD` só faz sentido pra ações PAUSE e NOTIFICATION. CHANGE_BUDGET e CHANGE_CAMPAIGN_BUDGET exigem ADSET ou CAMPAIGN respectivamente.

### F. Múltiplas condições (E composto)

**Aplica-se a:** trigger custom (T6).
**Por que existe:** o filters[] da Marketing API é naturalmente um AND lógico — múltiplas linhas significam "todas precisam bater". A skill hoje pergunta só 1 métrica + gasto mínimo, mas o Meta suporta combinações como "CTR < 0.5% E CPA > R$ 40 E frequência > 4".

**Pergunta ao aluno (no fim do trigger custom T6):**
```
Quer adicionar mais condições que precisam bater junto? (recomendado pra evitar falsos positivos)

1. Não, só essa condição
2. Adicionar mais uma (CTR + frequência, por exemplo)

Digite o número:
```

Se (2): rodar de novo o sub-fluxo de coleta de métrica/operador/valor/janela e adicionar como filter extra no array.

### G. Buffer pra evitar falsos positivos

**Aplica-se a:** qualquer trigger.
**Por que existe:** métricas oscilam por horas (latência de atribuição, conversões fora da janela, etc.). Sem buffer, a regra pode disparar com 1 dado ruim que vai voltar ao normal.

**Implementação prática:** adicionar `gasto mínimo` (passo 6) é a forma mais simples de buffer. Pra casos avançados, o Meta suporta filters compostos como "métrica X bateu por 2 dias consecutivos" via `time_preset: LAST_2_DAYS` + comparação com janela maior. Não cobrir no MVP — mencionar como roadmap.

### H. Notificação anexa a qualquer ação (não só NOTIFICATION pura)

**Aplica-se a:** ações 1-5 (PAUSE, CHANGE_BUDGET, CHANGE_CAMPAIGN_BUDGET).
**Por que existe:** o painel nativo permite "pausar + me avisar que pausou". A action principal da regra é PAUSE/CHANGE_BUDGET; um campo extra `notify_user_ids` em `execution_options` adiciona email pros admins escolhidos.

**Payload (campo extra em `execution_options` da Variante 1, 2 ou 3):**

```
{ "field": "notification_user_ids",
  "value": ["<user_id_admin_BM>"],
  "operator": "EQUAL" }
```

**Pergunta ao aluno (após coletar a ação não-NOTIFICATION):**
```
Quer ser notificado por email TODA vez que essa regra agir?

1. Sim, receber email do Meta junto com a ação
2. Não, só a ação silenciosa

Digite o número:
```

Se (1): coletar subscribers via mesmo fluxo do passo 5 (NOTIFICATION). Se (2): payload sem notification_user_ids.

**Específicos da ação NOTIFICATION:**
- **Email pro admin do BM**, push no Ads Manager mobile (se instalado) e sino do business.facebook.com. **Não vai pra Telegram/WhatsApp** (decisão arquitetural — não é tecnicamente possível sem SaaS/headless service externo).
- **Latência:** até 30 min entre o trigger bater e o email chegar (SEMI_HOURLY + delay SMTP do Meta).
- **Volume:** se a regra dispara 30+ vezes/dia, o Meta agrupa em "digest" diário automaticamente.
- **Template do email:** formato fixo do Meta, não dá pra customizar.
- **Push notification só funciona** se o aluno tem Ads Manager mobile instalado e logado com o user_id que está nos subscribers.
- **Pra digest semanal agendado** (toda segunda 8h, resumo da semana inteira): essa skill não cobre. Caminho manual: Ads Manager → Configurações → Relatórios Agendados → Criar Novo.
