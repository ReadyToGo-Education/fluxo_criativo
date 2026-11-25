# Sub-fluxo. Regra Automática Meta Ads

Cria uma regra automática que avalia campanhas, conjuntos ou anúncios contra um gatilho e executa uma das 6 ações:

- **Pausar** o conjunto ou a campanha
- **Aumentar o orçamento do CONJUNTO** em % (escalar vencedor; só ABO, conjunto com orçamento próprio)
- **Reduzir o orçamento do CONJUNTO** em % (frear perdedor; só ABO)
- **Aumentar o orçamento da CAMPANHA** em % (CBO ou ABO, mexe na campanha inteira)
- **Reduzir o orçamento da CAMPANHA** em % (CBO ou ABO)
- **Só avisar** (e-mail para o administrador do Business, sem mexer na campanha)

No App, as 6 usam o mesmo `POST /act_<id>/adrules_library` e mudam só no `execution_spec.execution_type` (`PAUSE`, `CHANGE_BUDGET`, `CHANGE_CAMPAIGN_BUDGET`, `NOTIFICATION`). No Gerenciador, todas aparecem juntas em "Regras automatizadas".

Passo 0 e gate: ver `SKILL.md` desta skill.

> ⚠️ **Roteamento por modo.** A regra automática vive no `adrules_library`, que **não tem tool no MCP**:
> - **`APP`:** a skill cria por `curl`, como descrito abaixo (token lido do `.env` na própria chamada), com bloco 🛡️.
> - **`MCP_CONECTOR`:** a skill faz a mesma coleta, as mesmas validações e o mesmo resumo, e no fim entrega o **passo a passo para o aluno criar no Gerenciador** (seção "Criar pelo Gerenciador (modo MCP)"). Nunca montar `POST /adrules_library` no MCP. As leituras de apoio (listar campanhas e conjuntos, detectar CBO ou ABO, ler orçamento) seguem pelo `ads_get_ad_entities`. Quem recebe o e-mail o aluno escolhe na própria tela da regra (o MCP não lista administradores do Business).

## Perguntas que cobre

- "Cria uma regra: se o CPA passar de R$ 40, pausa o conjunto"
- "Configura para aumentar o orçamento em 15% se o ROAS ficar acima de 3"
- "Pausa o anúncio se o CTR cair abaixo de 0,5%"
- "Me avisa se o gasto da campanha passar de R$ 500 por dia"

## Inputs

### Gatilho
| Campo | Opções |
|---|---|
| `metrica` | `cost_per_purchase_fb` (CPA, valor em **centavos**), `cost_per_lead_fb` (CPL, em centavos; ⚠️ por analogia, ainda NÃO validado em produção, conferir na primeira criação), `purchase_roas`, `ctr`, `frequency`, `spent`, `cpm`, `cpc`. **NÃO usar** `cost_per_action_type:*` nem `cost_per_result` (a API recusa com `Unrecognized filter field`). |
| `operador` | `GREATER_THAN`, `LESS_THAN` |
| `valor` | em reais ou na unidade da métrica |
| `janela` | `LAST_3_DAYS`, `LAST_7_DAYS`, `LAST_14_DAYS`, `LAST_30_DAYS`, `MAXIMUM`, `LIFETIME` |
| `gasto_minimo` | (recomendado) gasto mínimo na janela para a regra avaliar |

### Ação
| Opção (o aluno escolhe) | `execution_type` (a skill resolve no passo 3.5) | Campos | Quando usar |
|---|---|---|---|
| Pausar | `PAUSE` | nenhum | Cortar gasto ruim (ex: CPA estourou) |
| Aumentar orçamento (+%) | `CHANGE_BUDGET` se ABO, `CHANGE_CAMPAIGN_BUDGET` se CBO | `change_spec: {amount: <inteiro positivo>, unit: "PERCENTAGE"}` | Escalar vencedor (padrão +20%). Detecta CBO ou ABO sozinha. Validado em produção em 2026-05-19 |
| Reduzir orçamento (−%) | `CHANGE_BUDGET` se ABO, `CHANGE_CAMPAIGN_BUDGET` se CBO | `change_spec: {amount: <inteiro negativo>, unit: "PERCENTAGE", limit: <piso em centavos>}` **obrigatório** | Frear perdedor (padrão −20%). Piso **obrigatório** de R$ 30/dia (ou 50% do orçamento atual) para a regra não cortar até zero. O piso vai como `limit` **dentro** do `change_spec`, NÃO como `min_daily_budget` solto (a API recusa) |
| Só me avisar por e-mail | `NOTIFICATION` | `execution_options[{field: "user_ids", value: [<user_id_admin_BM>]}]` | Só alertar (monitoramento, oportunidade) |

### Escopo
| Tipo | Como funciona |
|---|---|
| `CAMPAIGN_IDS` | campanhas específicas |
| `ADSET_IDS` | conjuntos específicos |
| `AD_IDS` | anúncios específicos |
| `ALL_ACTIVE` | tudo o que está ativo na conta |
| `ALL_ACTIVE` + filtro | por objetivo, trecho do nome etc. |

## Endpoint (modo App)

As 4 ações usam o mesmo `POST /act_<id>/adrules_library`. O `evaluation_spec` (gatilho) é igual nos 4 casos; muda só o `execution_spec`.

**Estrutura do `filters[]`:** cada filtro é um objeto com `field`, `value` e `operator`. O `time_preset` **NÃO** vai dentro do filtro da métrica: é um **filtro próprio**, com `field: "time_preset"`. Erro confirmado em produção (a Meta devolve `Invalid keys "time_preset" were found in param "evaluation_spec[filters][N]"`).

**Status inicial:** `"status": "DISABLED"` no payload. O Gerenciador mostra como "Pausada", mas o valor aceito pela API é `DISABLED`. Valores válidos: `ENABLED`, `DISABLED`, `DELETED`, `HAS_ISSUES`. Não existe `PAUSED` (erro confirmado em produção).

### Variação 1: PAUSE

```
POST /act_<id>/adrules_library
{
  "name": "[WS] AutoRule-PauseCPAGT40-curso-tarot",
  "evaluation_spec": {
    "evaluation_type": "SCHEDULE",
    "filters": [
      { "field": "entity_type",          "value": "ADSET",            "operator": "EQUAL" },
      { "field": "campaign.id",          "value": ["<campaign_id>"],  "operator": "IN" },
      { "field": "time_preset",          "value": "LAST_3_DAYS",      "operator": "EQUAL" },
      { "field": "cost_per_purchase_fb", "value": 4000,               "operator": "GREATER_THAN" },
      { "field": "spent",                "value": 5000,               "operator": "GREATER_THAN" }
    ]
  },
  "execution_spec": {
    "execution_type": "PAUSE"
  },
  "schedule_spec": { "schedule_type": "SEMI_HOURLY" },
  "status": "DISABLED"
}
```

(`4000` = R$ 40 em centavos; `5000` = R$ 50 em centavos.)

### Variação 2: CHANGE_BUDGET (+ ou −)

> **Pré-requisitos (confirmados em produção):**
> 1. `entity_type` no `evaluation_spec.filters[]` **precisa** ser `ADSET`. Com `CAMPAIGN`, a Meta devolve `subcode 1815677: "Para o tipo de execução CHANGE_BUDGET, o tipo de entidade precisa ser ADSET."`
> 2. **Não funciona em CBO.** Em campanha com orçamento de campanha (CBO), os conjuntos não têm orçamento próprio. A skill escolhe sozinha `CHANGE_CAMPAIGN_BUDGET` nesse caso (passo 3.5).
> 3. O campo certo é `change_spec` (não `change_strategy` nem `value`). As tentativas antigas devolvem `"Unrecognized execution option field"`.

```
"execution_spec": {
  "execution_type": "CHANGE_BUDGET",
  "execution_options": [
    {
      "field": "change_spec",
      "value": {
        "amount": 20,
        "unit": "PERCENTAGE"
      },
      "operator": "EQUAL"
    }
  ]
}
```

(`amount`: inteiro positivo para escalar, negativo para frear. `unit`: `PERCENTAGE` ou `ABSOLUTE`, em centavos da moeda da conta.)

Outros campos do `change_spec`:
- `limit` (em centavos): trava o resultado. Na **redução**, é **piso** (a regra não corta abaixo disso). No **aumento**, é **teto**. É AQUI que o piso e o teto vivem: não existe `min_daily_budget`/`max_daily_budget` como opção separada (a API recusa com `Unrecognized execution option field`). Obrigatório na redução.
- `target_field`: campo do conjunto onde aplicar (`daily_budget` por padrão).

### Variação 3: CHANGE_CAMPAIGN_BUDGET (+ ou −)

Funciona em CBO **e** ABO. Mexe no orçamento da campanha inteira. É o único caminho automático para ajustar orçamento de CBO.

```
"execution_spec": {
  "execution_type": "CHANGE_CAMPAIGN_BUDGET",
  "execution_options": [
    {
      "field": "change_spec",
      "value": {
        "amount": -10,
        "unit": "PERCENTAGE"
      },
      "operator": "EQUAL"
    }
  ]
}
```

⚠️ **Pré-requisito:** `entity_type` no `evaluation_spec.filters[]` precisa ser `CAMPAIGN` (não `ADSET`). Usar `campaign.id` como filtro de escopo. Validado em produção em 2026-05-19 com esse formato.

### Variação 4: NOTIFICATION

```
"execution_spec": {
  "execution_type": "NOTIFICATION",
  "execution_options": [
    { "field": "user_ids",
      "value": ["<user_id_admin_BM>"],
      "operator": "EQUAL" }
  ]
}
```

O resto do payload (`name`, `evaluation_spec`, `schedule_spec`, `status`) é igual.

## Gatilhos prontos (atalhos)

A skill oferece 6 gatilhos prontos (só a condição). A **ação** é escolhida em outro passo (passo 4 da coleta), o que permite combinar qualquer gatilho com qualquer ação.

| Código | Gatilho | Padrão sugerido |
|---|---|---|
| **T1** | CPA passar de X | 1,4 vez o ticket (na janela média da trilha) |
| **T2** | CTR cair abaixo de X | 0,5% |
| **T3** | ROAS passar de X | 3,0 |
| **T4** | Frequência passar de X | 4 |
| **T5** | Gasto diário passar de X | R$ 500 |
| **T6** | Personalizado | o aluno define métrica, operador, valor e janela |

O ticket vem do resumo do produto (`meus-produtos/{ativo}/resumo-produto.md`).

### Combinações comuns (gatilho × ação)

| Gatilho | Ação | Resultado prático |
|---|---|---|
| T1 (CPA alto) | Pausar | Pausa o conjunto que pesa no CPA |
| T1 (CPA alto) | Só avisar | Alerta antes de pausar à mão |
| T2 (CTR baixo) | Pausar | Pausa o anúncio cansado |
| T2 (CTR baixo) | Só avisar | Avisa que o criativo cansou |
| T3 (ROAS alto) | +20% orçamento | Escala o vencedor sozinho |
| T3 (ROAS alto) | Só avisar | Alerta de oportunidade, o aluno decide |
| T4 (Frequência alta) | Pausar | Evita saturar o público |
| T5 (Gasto alto) | Só avisar | Monitora o gasto sem cortar |
| T5 (Gasto alto) | −20% orçamento | Freia sozinho |

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**.

### Ordem fixa

1. **Gatilho.** Mostrar os 6 gatilhos prontos numerados (T1 a T6).

2. **Gatilho personalizado.** *Só se T6.* Em sequência, uma pergunta por vez:
   - Métrica (CPA, CPL, ROAS, CTR, frequência, gasto, CPM, CPC)
   - Operador (maior que, menor que)
   - Valor (em reais ou na unidade da métrica)
   - Janela (3 dias, 7, 14, 30, máximo, vida toda)

3. **Escopo.** "Aplicar essa regra em qual campanha ou conjunto? (digite o nome, completo ou em parte, ou peça para eu listar)". Aceita:
   - **(a) Nome, completo ou em parte:** listar campanhas (ou conjuntos) com `ads_get_ad_entities` (MCP) ou `GET /act_<id>/campaigns?fields=name,status,effective_status` (App) e procurar o trecho no nome, sem diferenciar maiúsculas. 1 resultado: confirmar. Vários: lista numerada.
   - **(b) Listar:** "lista", "não lembro": campanhas ou conjuntos ativos e pausados dos últimos 90 dias.
   - **(c) Todas as ativas com filtro:** "todas as de vendas" ou parecido.
   - **(d) ID direto** (raro): conferir e confirmar.

   **O aluno nunca digita ID sem ter sido pedido.**

3.5. **Detecção de CBO ou ABO** (sem pergunta). *Só quando há campanha específica.* Ler o orçamento da campanha (`ads_get_ad_entities` no MCP; `GET /<campaign_id>?fields=daily_budget,lifetime_budget` no App):
   - `daily_budget` ou `lifetime_budget` da campanha maior que 0 → **CBO**.
   - Vazios → **ABO**.
   - Guardar para escolher a ação e mostrar no resumo.

4. **Ação.** Sempre:
   ```
   O que essa regra deve fazer quando o gatilho bater?

   1. Pausar o conjunto ou a campanha
   2. Aumentar o orçamento (em %)
   3. Reduzir o orçamento (em %)
   4. Só me avisar por e-mail (sem mexer na campanha)

   Digite o número:
   ```
   - **1 (PAUSE):** segue para o passo 6.
   - **2 ou 3:** pedir o percentual (padrão ±20%, alinhado ao limite que evita reset de aprendizado). Escolha automática:
     - **ABO** → `CHANGE_BUDGET`, `entity_type: ADSET`.
     - **CBO** → `CHANGE_CAMPAIGN_BUDGET`, `entity_type: CAMPAIGN`.
     - **Escopo "todas as ativas" sem campanha específica:** usar `CHANGE_CAMPAIGN_BUDGET` (funciona nos dois). Avisar: "vou mexer no orçamento da campanha porque o escopo é amplo".
   - **4 (NOTIFICATION):** vai ao passo 5 e depois ao 6.

   **A skill nunca pergunta "conjunto ou campanha?" para o orçamento.** Ela decide pela leitura do passo 3.5.

5. **Quem recebe o e-mail.** *Só se ação 4.*
   ```
   Quem deve receber o alerta por e-mail?

   1. Só você
   2. Você e outros administradores do Business (mostro a lista)
   3. Adicionar outros administradores pelo nome

   Digite o número:
   ```
   - **App, opção 1:** usar o `user_id` do aluno (`GET /me?fields=id`).
   - **App, opções 2 e 3:** listar as pessoas da conta com `GET /act_<id>/assigned_users?business=<bm_id>&fields=id,name,user_type,tasks` e **manter só `user_type == business_user`** (tirar `system_user`). **NÃO usar `GET /<bm_id>/business_users`**: com token de Usuário do Sistema (o caso padrão do token permanente) ele volta `data: []`. Erro confirmado em produção.
   - Na primeira vez, pode guardar `META_USER_ID` no `.env` para não buscar de novo (é um ID, não um segredo).
   - **MCP:** registrar a escolha; o aluno marca as pessoas na própria tela da regra no Gerenciador.

6. **Gasto mínimo (proteção).**
   ```
   Quer um gasto mínimo na janela para a regra não disparar com 1 conversão? (recomendado)

   1. Sim, usar o padrão sugerido (4 vezes o CPA alvo)
   2. Sim, eu digito o valor
   3. Não (assumo o risco de decidir com pouco dado)

   Digite o número:
   ```
   Se (2): pedir o valor em reais.

7. **Nome.** Sugerir `[WS] AutoRule-{tipo}-{slug}` (ex: PauseCPAGT40, Boost20PctROASGT3, AlertCPLGT15) e perguntar "uso esse ou prefere outro?".

**Proibido:**
- Pedir `evaluation_spec`, `filters[]`, `time_preset`, `entity_type`, `execution_spec`, `user_id` ou qualquer chave da Marketing API ao aluno.
- Agrupar 2 ou mais inputs na mesma mensagem.
- Pular para o resumo sem passar pelos passos que se aplicam (1, 3, 4, 6, 7 sempre; 2 só em T6; 5 só na ação 4).

## Validação antes de criar

1. **O gatilho faz sentido?** Limites de sanidade (avisa, não bloqueia; o aluno digita "sim" para forçar):
   - `CTR < 0,3%` → "esse CTR é muito baixo, a regra pode nunca disparar. Tem certeza?"
   - `CPA < ticket/2` → "esse CPA é menos da metade do seu ticket ({ticket}/2 = R$ {valor}): a regra vai pausar tudo na primeira venda. Tem certeza?"
   - `ROAS > 20` → "ROAS acima de 20 é altíssimo, a regra pode nunca disparar. Tem certeza?"
   - `frequência < 1` ou `> 10` → "frequência fora da faixa comum (1 a 10). Tem certeza?"
2. **Tem gasto mínimo?** Sem ele, a regra dispara com 1 conversão.
3. **Janela combina com o ticket?** High ticket (R$ 1.500 ou mais) precisa de janela de 7 dias ou mais.
4. **Conflita com outra regra ativa?** No App, listar as regras e checar sobreposição. No MCP, perguntar ao aluno se já existe regra parecida no Gerenciador.
5. **CBO ou ABO mudou desde o passo 3.5?** *Só nas ações 2 e 3.* Ler de novo o orçamento da campanha. Se mudou (raro: o aluno trocou no Gerenciador no meio do fluxo):
   ```
   ⚠️ A campanha mudou de estrutura desde que eu conferi (era {CBO|ABO},
   agora é {ABO|CBO}). Vou refazer a escolha da ação.

   Posso continuar? (sim/não)
   ```

Se algo falhar:

```
⚠️ Atenção:

A regra que você quer criar pode dar problema:

- "CPA > R$ 40" sem gasto mínimo pode pausar um conjunto com 1 venda boa que custou R$ 50.
  Recomendado: só agir com gasto acima de R$ 200 (4 vezes o CPA alvo).

Quer que eu adicione esse gasto mínimo?

1. Sim, usar o padrão (R$ X = 4 vezes o CPA alvo da trilha)
2. Sim, eu digito o valor
3. Não, criar do jeito que pedi

Digite o número:
```

## Resumo em linguagem natural (obrigatório)

**Quando:** depois da coleta e da validação. No App, vem antes do bloco 🛡️. No MCP, vem antes do passo a passo do Gerenciador.

```
📋 Antes de {eu criar | você criar} essa regra, um resumo do plano:

O que vai ser criado:
  Uma regra automática DESATIVADA chamada "{nome}".

O que ela faz:
  A cada 30 minutos, a Meta olha {escopo em português, ex: "os seus 12 conjuntos
  ativos de campanhas de vendas"} e, se {gatilho em português, ex: "o CPA dos
  últimos 3 dias passar de R$ 40 e o gasto na mesma janela for maior que R$ 200"},
  vai {ação:
    [1] "pausar o conjunto ou a campanha"
    [2] "aumentar o orçamento em 20%"
    [3] "reduzir o orçamento em 20%"
    [4] "te mandar um e-mail (sem mexer na campanha)"
  }.

{Ações 2 e 3:}
Orçamento atual {da campanha | do conjunto}: R$ {valor_atual}
Depois do disparo: R$ {valor_pos} (R$ {valor_atual} × {fator})
{Ação 3:} Piso garantido: R$ {piso} (a regra não corta abaixo disso)

{Ação 4:}
Onde o aviso chega:
  - E-mail para o administrador do Business (você e mais {N} pessoas)
  - Notificação no app do Gerenciador de Anúncios (se instalado)
  - Sino do business.facebook.com

Alcance agora: {N} {campanhas | conjuntos | anúncios} ativos seriam avaliados.

Intervalo: depois de {agir | avisar} numa entidade, espera {24h | 1h} antes de
{agir | avisar} nela de novo.

{Ação 4:} Importante: essa regra NÃO pausa nem mexe nas campanhas, só avisa.

Para desfazer: desativar a regra (/trafego-regras → 3 → C). Excluir é à parte.

Está certo? (sim segue, não cancela aqui)
```

**Tradução obrigatória:**

| Campo técnico | Tradução |
|---|---|
| `cost_per_purchase_fb` | "CPA (custo por compra)" |
| `cost_per_lead_fb` | "CPL (custo por lead)" |
| `purchase_roas` | "ROAS (retorno sobre o investimento)" |
| `ctr` | "CTR (taxa de clique)" |
| `frequency` | "frequência (vezes que cada pessoa viu o anúncio)" |
| `spent` | "gasto" |
| `cpm` | "CPM (custo por mil impressões)" |
| `cpc` | "CPC (custo por clique)" |
| `GREATER_THAN` | "passar de" / "ficar acima de" |
| `LESS_THAN` | "cair abaixo de" |
| `LAST_3_DAYS` | "últimos 3 dias" |
| `LAST_7_DAYS` | "última semana" |
| `LAST_30_DAYS` | "últimos 30 dias" |
| `MAXIMUM` | "toda a vida da campanha" |
| `PAUSE` | "pausar" |
| `CHANGE_BUDGET +20%` ou `CHANGE_CAMPAIGN_BUDGET +20%` | "aumentar o orçamento em 20%" |
| `CHANGE_BUDGET -20%` ou `CHANGE_CAMPAIGN_BUDGET -20%` | "reduzir o orçamento em 20%" |
| `NOTIFICATION` | "te avisar (sem mudar nada na campanha)" |
| `SEMI_HOURLY` | "a cada 30 minutos" |
| `spent: 5000` (centavos) | "R$ 50" (sempre converter) |
| `ALL_ACTIVE` + filtro | o filtro em português ("todas as campanhas ativas de vendas") |

**Proibido no resumo:** IDs, chaves da Marketing API, valores em centavos, inglês técnico (`adset`, `bidding`, `evaluation_type`).

**Depois:** "sim" segue (App: bloco 🛡️; MCP: passo a passo). "Não": "1. Quer ajustar algo, 2. cancelar de vez?".

## Preview YAML (modo App, dentro do bloco 🛡️)

O bloco `acao` muda conforme a ação; gatilho, escopo e intervalo são iguais.

### Com PAUSE

```yaml
sub_fluxo: regra_automatica
nome_final: "[WS] AutoRule-PauseCPAGT40-curso-tarot"
status_inicial: DISABLED (aparece como "Pausada" no Gerenciador)

gatilho:
  metrica: cost_per_purchase_fb
  operador: GREATER_THAN
  valor: 4000 (R$ 40 em centavos)
  janela: LAST_3_DAYS
  protecao: gasto > R$ 200 na mesma janela

acao:
  tipo: PAUSE
  alvo: conjunto

escopo:
  tipo: ALL_ACTIVE
  filtro: objetivo de vendas
  alcance: 12 conjuntos ativos

intervalo: 24h
frequencia_avaliacao: a cada 30 min
```

### Com CHANGE_BUDGET (conjunto ABO)

```yaml
acao:
  tipo: CHANGE_BUDGET
  delta_percentual: +20                # negativo para reduzir
  alvo: conjunto                       # OBRIGATÓRIO ser conjunto
  change_spec: {amount: 20, unit: PERCENTAGE}

gatilho:
  entity_type: ADSET                   # OBRIGATÓRIO
```

⚠️ Só em **conjuntos de campanhas ABO**. Em CBO, usar a variação abaixo.

### Com CHANGE_CAMPAIGN_BUDGET (campanha CBO ou ABO)

```yaml
acao:
  tipo: CHANGE_CAMPAIGN_BUDGET
  delta_percentual: -10
  alvo: campanha                       # OBRIGATÓRIO
  change_spec: {amount: -10, unit: PERCENTAGE, limit: 3000}

gatilho:
  entity_type: CAMPAIGN
  campaign_id: ["<campaign_id>"]
```

⚠️ Funciona em CBO e ABO. Em ABO, mexe no orçamento da campanha (afeta os conjuntos dela). Validado em 2026-05-19.

### Com NOTIFICATION

```yaml
acao:
  tipo: NOTIFICATION
  destinatarios:
    - administrador do Business: {nome}
  canal: e-mail + app do Gerenciador + sino do business.facebook.com

intervalo: 1h
```

## Criar pelo Gerenciador (modo MCP)

Depois do "sim" no resumo, entregar o passo a passo com os valores já preenchidos (nada de termo técnico):

```
O conector da Meta ainda não cria regra automática, então você cria em uns 3 minutos
no Gerenciador, com tudo que a gente definiu:

📋 Passo 1. Gerenciador de Anúncios → menu "Regras automatizadas" (ou o ícone de
           regras no topo da tabela de campanhas) → "Criar regra" → "Regra personalizada"
📋 Passo 2. Aplicar regra a: {"Todas as campanhas ativas" | "Todos os conjuntos de
           anúncios ativos" | "Todos os anúncios ativos" | os itens que você marcou}
           {se escopo específico: antes de abrir a regra, marque "{nome}" na tabela}
📋 Passo 3. Ação: {"Desativar conjuntos de anúncios" | "Aumentar orçamento diário em
           20%" | "Diminuir orçamento diário em 20%" | "Enviar somente notificação"}
           {Ação 3: defina o mínimo do orçamento diário em R$ {piso}}
           {Ação 2 com teto: defina o máximo do orçamento diário em R$ {teto}}
📋 Passo 4. Condições:
           • {métrica em português} {é maior que | é menor que} {valor}
           • Valor gasto é maior que R$ {gasto_minimo}
📋 Passo 5. Intervalo de tempo: {últimos 3 dias | ...}
📋 Passo 6. Frequência de ação: {uma vez a cada 12 horas | uma vez por dia | ...}
📋 Passo 7. Programação: {Continuamente | Diariamente | Personalizado: dias e horários}
📋 Passo 8. Notificação e assinantes: {você | você e {nomes}}
📋 Passo 9. Nome da regra: {nome}
📋 Passo 10. Clique em "Criar"
📋 Passo 11. Na lista de regras, desligue a chave da regra "{nome}". Ela fica
            desativada até você revisar e ligar.

🛟 Se algum nome de botão estiver diferente, me mande um print.

Me avise com "feito" quando terminar.
```

Depois do "feito":
- Registrar em `meus-produtos/_global/trafego/regras/INDEX.md` e num arquivo `{slug-do-nome}.md` com todo o desenho da regra e `origem: criada no Gerenciador (modo MCP)`.
- Seguir para "Depois de criar" (versão MCP).

## Depois de criar

Mensagem em linguagem natural, **sem `curl`, sem `POST`, sem `DELETE`** no texto.

```
✅ Pronto. A regra "{nome}" foi criada na sua conta, DESATIVADA (ainda não está agindo).

Onde ver e gerenciar:
   Gerenciador de Anúncios → "Regras automatizadas"
   Procure "{nome}" (o prefixo "[WS] AutoRule-..." ajuda a achar).

🟢 Para ATIVAR (e começar a avaliar a cada 30 minutos):
   /trafego-regras → 3 → B, ou no Gerenciador, ligando a chave da regra.

📊 Para ver QUANDO ela agiu e o que fez (depois de ativada):
   /trafego-regras → 3 → F, ou no Gerenciador, na própria regra.

✏️ Para EDITAR ou DESATIVAR:
   /trafego-regras → 3, ou no Gerenciador (três pontos na linha da regra).

📝 Registro em: meus-produtos/_global/trafego/regras/INDEX.md
   {App: o ID técnico fica lá, só para suporte da Meta ou investigação.}
```

### Atalho: ativar agora (opcional)

Logo depois da mensagem acima:

```
A regra nasceu DESATIVADA por segurança. Quer ATIVAR agora para ela começar a avaliar
a cada 30 minutos?

1. Sim, ativar agora
2. Não, deixar desativada (ativo depois pelo /trafego-regras → 3 → B)

Digite o número (Enter para usar 2):
```

**Se 1:**
- **App:** bloco 🛡️ curto (a criação foi aprovada há pouco; este é só a mudança de status, que é outra escrita):
  ```
  🛡️ Confirmação rápida
  Operação: ativar a regra que acabamos de criar
  O que vai mudar: status DESATIVADA → ATIVA
  Reversível? sim, pelo /trafego-regras → 3 → C
  Pode aplicar? (sim/não)
  ```
  Com "sim": `POST /<rule_id> { "status": "ENABLED" }`. Mensagem: "✅ Regra criada E ativada. A primeira avaliação acontece em até 30 minutos."
- **MCP:** orientar a ligar a chave da regra na lista de "Regras automatizadas".

**Regras para a mensagem final:**
- **Nunca** mostrar `POST /<id>` ou `DELETE /<id>` no texto principal.
- Sempre falar da ação pelo nome ("Ativar regra", "Desativar regra") e pelo menu da skill.
- Citar o Gerenciador como caminho alternativo.
- O ID da regra pode aparecer **uma vez** no fim, como "ID técnico para suporte".

### Nome por tipo de ação

| Ação | Padrão | Exemplo |
|---|---|---|
| PAUSE | `[WS] AutoRule-Pause{Metrica}{Op}{Valor}-{slug}` | `[WS] AutoRule-PauseCPAGT40-curso-tarot` |
| Aumentar orçamento | `[WS] AutoRule-Boost{Delta}Pct{Metrica}{Op}{Valor}-{slug}` | `[WS] AutoRule-Boost20PctROASGT3-curso-tarot` |
| Reduzir orçamento | `[WS] AutoRule-Brake{Delta}Pct{Metrica}{Op}{Valor}-{slug}` | `[WS] AutoRule-Brake20PctCPAGT40-curso-tarot` |
| NOTIFICATION | `[WS] AutoRule-Alert{Metrica}{Op}{Valor}-{slug}` | `[WS] AutoRule-AlertSpendGT500-curso-tarot` |

O `INDEX.md` registra qual `execution_type` foi usado (CHANGE_BUDGET ou CHANGE_CAMPAIGN_BUDGET). O aluno vê só o nome (Boost, Brake).

**Só na ação NOTIFICATION:**

```
Onde o aviso chega quando o gatilho disparar:
  - E-mail: {o seu e-mail cadastrado no Business}
  - Celular: notificação no app do Gerenciador de Anúncios (se instalado)
  - Web: sino do business.facebook.com
```

## Avisos

**Pegadinhas da Marketing API confirmadas em produção (modo App):**
- **`status` é `DISABLED`, não `PAUSED`.** Valores aceitos: `ENABLED`, `DISABLED`, `DELETED`, `HAS_ISSUES`. O Gerenciador chama `DISABLED` de "Pausada".
- **`time_preset` é filtro próprio.** Nunca dentro do filtro da métrica. Sempre `{"field":"time_preset","value":"LAST_3_DAYS","operator":"EQUAL"}` como item separado.
- **`CHANGE_BUDGET` usa `change_spec`**, não `change_strategy` nem `value` soltos. Formato: `execution_options: [{field: "change_spec", value: {amount: 20, unit: "PERCENTAGE"}, operator: "EQUAL"}]`.
- **`CHANGE_BUDGET` exige `entity_type: ADSET`.** Com `CAMPAIGN`: `subcode 1815677`.
- **`CHANGE_BUDGET` não funciona em CBO.** Detectar antes pelo orçamento da campanha (algum valor maior que 0 = CBO). Em CBO, usar `CHANGE_CAMPAIGN_BUDGET`.
- **`CHANGE_CAMPAIGN_BUDGET` funciona em CBO e ABO**, com `entity_type: CAMPAIGN` e o mesmo `change_spec`. É o que o Gerenciador usa em "Aplicar regra a: todas as campanhas ativas" com aumento ou redução de orçamento.
- **`GET /<bm_id>/business_users` volta `data: []` com token de Usuário do Sistema.** Usar `GET /act_<id>/assigned_users?business=<bm_id>&fields=id,name,user_type,tasks` e filtrar `user_type == business_user`.
- **Piso e teto NÃO são `min_daily_budget`/`max_daily_budget`** separados (ambos devolvem `(#100) Unrecognized execution option field`). Vivem como `limit` (centavos) **dentro** do `change_spec`: `{amount: -20, unit: "PERCENTAGE", limit: 6300}`. Confirmado em produção em 2026-06-09.
- **Aviso junto de ação CHANGE ou PAUSE usa `user_ids`**, não `notification_user_ids` nem `notify_user_ids` (devolvem `(#100) Unrecognized execution option field`). Confirmado em produção em 2026-06-09.
- **CPA no gatilho é `cost_per_purchase_fb`, em centavos.** `cost_per_action_type:offsite_conversion.fb_pixel_purchase`, `cost_per_action_type:purchase` e `cost_per_result` são recusados com `(#100) Unrecognized filter field`. R$ 1.250 = 125000. Confirmado em produção em 2026-06-09. O CPL análogo seria `cost_per_lead_fb`, **ainda não validado em produção**: conferir na primeira regra de CPL.

**Outros avisos:**
- **A Meta avalia a cada 30 minutos** (`SEMI_HOURLY`). Não é instantâneo.
- **Pausar pela regra reseta o aprendizado** se a campanha estiver em aprendizado. Avisar.
- **Aumentar mais de 20% também reseta.** A skill recomenda no máximo +20% por execução.
- **Limite da Meta:** 200 regras por conta de anúncios (todas as ações somam no mesmo limite).

---

## Recursos extras do Gerenciador (suportados)

O Gerenciador tem 7 controles além de gatilho, ação e escopo. A skill cobre todos. Se o aluno não mencionar, usar o padrão; se mencionar, perguntar depois do passo 4 (Ação) e antes do passo 6 (Gasto mínimo). No modo MCP, cada escolha vira uma linha do passo a passo do Gerenciador.

### A. Orçamento mínimo diário (proteção para aumentar ou reduzir orçamento)

**Vale para:** ações 2 e 3.
**Por quê:** evita a regra reduzir o orçamento abaixo de um piso em que a campanha para de entregar (redução), ou limita o teto (aumento).
**Payload (App):** `limit` DENTRO do `change_spec`:

```
"execution_options": [
  { "field": "change_spec",
    "value": { "amount": -20, "unit": "PERCENTAGE", "limit": 3000 },
    "operator": "EQUAL" }
]
```

(`3000` = piso de R$ 30,00 em centavos.)

| Ação | O piso é... | Padrão | A skill pergunta? |
|---|---|---|---|
| 2 (Aumentar) | Opcional | Sem piso | Só se o aluno mencionar teto |
| 3 (Reduzir) | **OBRIGATÓRIO** | o maior entre R$ 30/dia e 50% do orçamento atual | Não: aplica o padrão e avisa no resumo |

Na ação 3, mostrar no resumo:
```
Vou garantir que o orçamento não caia abaixo de R$ {padrao} por dia.
(O padrão é 50% do seu orçamento atual de R$ {valor_atual}, ou R$ 30, o que for maior.)

Quer ajustar esse piso?
1. Não, manter R$ {padrao}
2. Quero outro valor (digito)
3. Tirar o piso (assumo o risco de a regra cortar até zero)

Digite o número (Enter para manter o padrão):
```

Na ação 2: se o aluno disser "quero limitar o teto em R$ X", usar o mesmo `limit` (com `amount` positivo ele vira teto).

### B. Programação (continuamente, diariamente, personalizado)

**Vale para:** todas as ações. Mapeia para `schedule_spec.schedule_type`:
- Continuamente → `SEMI_HOURLY` (padrão, a cada 30 min)
- Diariamente → `DAILY` (1 vez por dia, entre 0h e 1h do fuso da conta)
- Personalizado → `CUSTOM` (dias da semana e horário)

```
Com que frequência a Meta deve checar essa regra?

1. Continuamente, a cada 30 min (padrão, pega mudanças rápidas)
2. Diariamente, 1 vez por dia, entre 0h e 1h
3. Personalizado, escolho dias e horários

Digite o número:
```

Se (3), payload:
```
"schedule_spec": {
  "schedule_type": "CUSTOM",
  "schedule": [
    { "days": [1,2,3,4,5], "start_minute": 480, "end_minute": 1080 }
  ]
}
```

### C. Frequência de ação

**Vale para:** PAUSE, CHANGE_BUDGET, CHANGE_CAMPAIGN_BUDGET (o aviso tem padrão de 1h).
**Por quê:** controla quantas vezes a regra pode **agir** na mesma entidade num período. É diferente da programação (frequência de avaliação).
**Payload (App):**

```
{ "field": "execution_frequency",
  "value": "ONCE_PER_DAY",
  "operator": "EQUAL" }
```

(Outros valores: `ONCE_EVERY_12_HOURS`, `ONCE_PER_WEEK` etc.)

```
Quantas vezes a regra pode agir na MESMA campanha, conjunto ou anúncio?

1. Uma vez a cada 12 horas (padrão)
2. Uma vez por dia
3. Uma vez por semana
4. Sem limite (cuidado: pode causar ciclo)

Digite o número:
```

### D. Janela de avaliação

Já coberta no passo 2 (T6). Nos gatilhos prontos, o padrão é `LAST_3_DAYS`. **Aviso:** `MAXIMUM` equivale a 37 meses (teto da Meta).

### E. Escopo em anúncio

Somar ao passo 3:

```
Aplicar essa regra em quê?

1. Numa campanha específica (ou todas as ativas com filtro)
2. Num conjunto específico (ou todos os ativos)
3. Num anúncio específico (ou todos os ativos)

Digite o número:
```

Se (3): `entity_type: "AD"`. Uso típico: pausar anúncios com CTR abaixo de 0,3% sem mexer no conjunto.

**⚠️ Limite:** escopo em anúncio só faz sentido para PAUSE e NOTIFICATION. Mudança de orçamento exige conjunto ou campanha.

### F. Várias condições juntas (E)

**Vale para:** gatilho personalizado (T6). O `filters[]` já é um E lógico: várias linhas = todas precisam bater (ex: "CTR < 0,5% E CPA > R$ 40 E frequência > 4").

```
Quer adicionar outra condição que precisa bater junto? (recomendado para evitar alarme falso)

1. Não, só essa
2. Adicionar mais uma (ex: CTR e frequência)

Digite o número:
```

Se (2): repetir a coleta de métrica, operador, valor e janela e somar ao array.

### G. Margem contra alarme falso

As métricas oscilam por horas (atraso de atribuição, conversões fora da janela). O gasto mínimo (passo 6) é a forma mais simples de margem. Casos avançados ("bateu 2 dias seguidos") ficam para uma versão futura.

### H. Aviso junto de qualquer ação

**Vale para:** PAUSE, CHANGE_BUDGET, CHANGE_CAMPAIGN_BUDGET. O Gerenciador permite "pausar e me avisar que pausou": um `user_ids` extra em `execution_options` (usar `user_ids`, NÃO `notification_user_ids` nem `notify_user_ids`, que a API recusa):

```
{ "field": "user_ids",
  "value": ["<user_id_admin_BM>"],
  "operator": "EQUAL" }
```

```
Quer receber e-mail TODA vez que essa regra agir?

1. Sim, receber o e-mail da Meta junto com a ação
2. Não, só a ação

Digite o número:
```

Se (1): coletar quem recebe pelo passo 5.

**Sobre o aviso por e-mail:**
- **E-mail para o administrador do Business**, notificação no app do Gerenciador (se instalado) e sino do business.facebook.com. **Não vai para Telegram nem WhatsApp.**
- **Atraso:** até 30 min entre o gatilho bater e o e-mail chegar.
- **Volume:** se a regra disparar 30 vezes ou mais por dia, a Meta junta tudo num resumo diário.
- **Modelo do e-mail:** fixo da Meta.
- **Notificação no celular** só funciona com o app do Gerenciador instalado e logado com a pessoa escolhida.
- **Resumo semanal agendado:** fora desta skill. Caminho manual: Gerenciador → Relatórios → Relatórios agendados.
