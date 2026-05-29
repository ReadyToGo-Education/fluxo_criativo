# Output [7] — Lifecycle & Histórico

Memória da conta. O que aconteceu nos últimos 6 meses, quais campanhas estão envelhecendo, qual foi o melhor período de todos e quais anúncios pausados ainda têm valor para reativar.

> **Nota de escopo:** este output sempre usa janela de 6 meses independentemente do período selecionado no Passo 3. O período do Passo 3 serve apenas como referência para identificar o "mês corrente" (último mês do histórico). Não perguntar período novamente.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- "Quais campanhas estão rodando há mais de 60 dias sem pausa? Precisam de refresh?"
- "Me mostra a evolução do meu CPA mês a mês nos últimos 6 meses"
- "Qual foi meu melhor mês de todos os tempos em ROAS?"
- "Tem campanha pausada que performava bem e vale a pena reativar?"
- "Qual foi o anúncio que mais gerou resultado na história da conta?"

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## Dados necessários

### O que já vem do Passo 4 do command principal

`level=campaign`, sem breakdowns. Campos base: `spend`, `impressions`, `clicks`, `ctr`, `cpm`, `cpc`, `reach`, `frequency`, `actions`, `action_values`, `cost_per_action_type`, métricas de vídeo.

Esses dados cobrem apenas o período selecionado no Passo 3 e servem como âncora para o "mês corrente". Os dados históricos de 6 meses exigem as chamadas adicionais abaixo.

### Campos adicionais

```
created_time,start_time,stop_time,effective_status,updated_time
```

Necessários para calcular dias ativos e identificar campanhas longevas.

### Chamadas adicionais (executar antes de montar os blocos)

**Chamada 7a — Histórico mensal de 6 meses (campanhas ativas)**

Usar `date_preset=last_6_months` com `time_increment=monthly`. Retorna uma linha por campanha por mês, permitindo calcular ROAS e CPA mês a mês.

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=campaign_id,campaign_name,spend,impressions,clicks,actions,action_values,cost_per_action_type
  &level=campaign
  &date_preset=last_6_months
  &time_increment=monthly
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com `time_increment=monthly` e `date_preset=last_6_months`.

---

**Chamada 7b — Listagem completa de campanhas (ativas + pausadas + arquivadas)**

Necessária para identificar campanhas longevas (campo `start_time`) e campanhas pausadas com histórico de performance.

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/campaigns
  ?fields=id,name,status,effective_status,objective,daily_budget,lifetime_budget,created_time,start_time,stop_time,updated_time
  &effective_status=['ACTIVE','PAUSED','ARCHIVED']
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Modo MCP_CONECTOR:** usar `mcp__*__ads_get_ad_entities` com `entity_type=campaign` e filtro de status `['ACTIVE','PAUSED','ARCHIVED']`.

---

**Chamada 7c — Performance das campanhas pausadas e arquivadas (últimos 6 meses)**

Necessária para identificar campanhas pausadas que performavam bem antes de serem desligadas.

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=campaign_id,campaign_name,spend,actions,action_values,cost_per_action_type,impressions,clicks,frequency
  &level=campaign
  &date_preset=last_6_months
  &time_increment=1
  &effective_status=['PAUSED','ARCHIVED']
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

Agregar por `campaign_id` após receber: somar `spend`, `actions` (compras ou leads), `action_values`. Calcular CPA/ROAS médio histórico por campanha pausada.

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` filtrando por `effective_status=['PAUSED','ARCHIVED']`.

---

**Chamada 7d — Top anúncios históricos (level=ad, incluindo pausados)**

Necessária para o Bloco 4. Ordenar todos os anúncios pelos resultados históricos totais.

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=ad_id,ad_name,campaign_name,adset_name,spend,actions,action_values,cost_per_action_type,impressions,clicks
  &level=ad
  &date_preset=last_6_months
  &effective_status=['ACTIVE','PAUSED','ARCHIVED']
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

Após receber: agrupar por `ad_id`, somar totais, ordenar por `offsite_conversion.fb_pixel_purchase` decrescente (ou `offsite_conversion.fb_pixel_lead` para funil de captação).

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com `level=ad` e filtros equivalentes.

---

**Chamada 7e — Data do primeiro gasto de cada campanha ativa (para cálculo de dias ativos)**

Calcular quantos dias cada campanha ativa está rodando sem pausa longa: cruzar `start_time` (Chamada 7b) com a data atual. Se `start_time` for anterior a 60 dias e o `effective_status` for `ACTIVE` hoje, a campanha é candidata ao Bloco 1.

Não é necessária uma chamada extra: usar os campos `start_time` e `effective_status` já retornados na Chamada 7b.

---

### Referência de produto

Ler `perfil.md` (já carregado no Passo 0): campo `preco`. Inferir tipo de funil pelo objetivo predominante das campanhas:
- `OUTCOME_SALES` → funil de venda direta → métrica-norte = **ROAS** e **CPA**
- `OUTCOME_LEADS` → funil de captação → métrica-norte = **CPL** e **total de leads**

Essa inferência determina qual template (A ou B) usar nos blocos de análise.

---

## Fórmulas de cálculo

### ROAS mensal
```
ROAS_mês = sum(action_values onde action_type = "offsite_conversion.fb_pixel_purchase" no mês) / sum(spend no mês)
```

### CPA mensal
```
CPA_mês = sum(spend no mês) / sum(actions onde action_type = "offsite_conversion.fb_pixel_purchase" no mês)
```

### CPL mensal
```
CPL_mês = sum(spend no mês) / sum(actions onde action_type = "offsite_conversion.fb_pixel_lead" no mês)
```

### Dias ativos (campanha longeva)
```
dias_ativos = data_atual − start_time (em dias corridos)
```
Usar `start_time` da Chamada 7b. Se `stop_time` existir e for anterior a hoje, a campanha foi pausada: não considerar como longeva.

### Degradação de CPA (campanha longeva)
```
degradação_% = ((CPA_mês_atual − CPA_primeiro_mês) / CPA_primeiro_mês) × 100
```
Usar dados mensais da Chamada 7a. "Primeiro mês" = primeiro mês com `spend > R$ 100` na série histórica da campanha (evita meses de teste com pouco gasto).

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "Quais campanhas estão rodando há mais de 60 dias sem pausa? Precisam de refresh?"

Calcular `dias_ativos` para cada campanha com `effective_status = ACTIVE`. Listar apenas as com `dias_ativos > 60`.

#### Template A — Venda direta (OUTCOME_SALES)

```
🔄 CAMPANHAS LONGEVAS  ·  Ativas ininterruptas > 60 dias

  Campanha              Dias ativa   CPA atual    CPA 1º mês   Variação    Freq. atual
  ─────────────────────────────────────────────────────────────────────────────────────
  {nome}                92d          R$ {X}       R$ {Y}       +{Z%}       {F.x}
  {nome}                78d          R$ {X}       R$ {Y}       −{Z%}       {F.x}
  ...

  Legenda:
  🟢 CPA estável ou melhora (≤ +20%)
  🟡 CPA degradou +21% a +30%
  🔴 CPA degradou > 30% OU frequência > 5  →  refresh urgente

  Critérios de refresh (qualquer um basta):
  • CPA degradou > 30% vs. primeiro mês
  • Frequência atual > 5
  • Nenhum criativo novo adicionado nos últimos 30 dias (verificar via output [3])
```

#### Template B — Captação de leads (OUTCOME_LEADS)

```
🔄 CAMPANHAS LONGEVAS  ·  Ativas ininterruptas > 60 dias

  Campanha              Dias ativa   CPL atual    CPL 1º mês   Variação    Freq. atual
  ─────────────────────────────────────────────────────────────────────────────────────
  {nome}                105d         R$ {X}       R$ {Y}       +{Z%}       {F.x}
  ...

  Critérios de refresh (qualquer um basta):
  • CPL degradou > 30% vs. primeiro mês
  • Frequência atual > 5
  • Nenhum criativo novo nos últimos 30 dias
```

Se nenhuma campanha ativa tiver mais de 60 dias, exibir: "Nenhuma campanha longeva identificada. Conta está renovando criativos regularmente."

---

### Resposta 2. "Me mostra a evolução do meu CPA mês a mês nos últimos 6 meses"

Construir a série a partir da Chamada 7a, agregando todas as campanhas por mês.

#### Template A — Venda direta (ROAS e CPA)

```
📈 EVOLUÇÃO 6 MESES — Conta: {nome_conta}

  Métrica principal: CPA  (funil de venda direta)

  {mês -5}  ████████████ R$ {CPA}  ({spend} spend · {N} compras · ROAS {X.X}x)
  {mês -4}  ██████████   R$ {CPA}  ({spend} spend · {N} compras · ROAS {X.X}x)
  {mês -3}  █████████    R$ {CPA}  ({spend} spend · {N} compras · ROAS {X.X}x)
  {mês -2}  ███████      R$ {CPA}  ({spend} spend · {N} compras · ROAS {X.X}x)  ← melhor CPA
  {mês -1}  █████████    R$ {CPA}  ({spend} spend · {N} compras · ROAS {X.X}x)
  {mês 0}   ████████████ R$ {CPA}  ({spend} spend · {N} compras · ROAS {X.X}x)  ← atual

  Tamanho da barra: proporcional ao CPA (barra maior = CPA mais alto = pior)

  Tendência últimos 3 meses: {melhora | estável | deterioração}
  Variação acumulada (mês 0 vs. mês -5): {+/-Z%} de CPA
```

#### Template B — Captação de leads (CPL e volume de leads)

```
📈 EVOLUÇÃO 6 MESES — Conta: {nome_conta}

  Métrica principal: CPL  (funil de captação)

  {mês -5}  ████████████ R$ {CPL}  ({spend} spend · {N} leads)
  {mês -4}  ██████████   R$ {CPL}  ({spend} spend · {N} leads)
  {mês -3}  █████████    R$ {CPL}  ({spend} spend · {N} leads)
  {mês -2}  ███████      R$ {CPL}  ({spend} spend · {N} leads)  ← melhor CPL
  {mês -1}  █████████    R$ {CPL}  ({spend} spend · {N} leads)
  {mês 0}   ████████████ R$ {CPL}  ({spend} spend · {N} leads)  ← atual

  Tendência últimos 3 meses: {melhora | estável | deterioração}
  Variação acumulada (mês 0 vs. mês -5): {+/-Z%} de CPL
```

**Classificação de tendência:**

| Variação acumulada do CPA/CPL (mês 0 vs. mês -5) | Classificação |
|---|---|
| Melhora ≥ 15% (CPA/CPL caiu) | 🟢 Conta evoluindo |
| Estável (variação entre −14% e +14%) | 🟡 Conta estável |
| Deterioração +15% a +30% | 🟠 Atenção — investigar causa |
| Deterioração > +30% | 🔴 Degradação grave — output [6] Investigação Profunda |

Se em algum mês `spend < R$ 200`, marcar como "(mês sem dados suficientes)" e excluir do cálculo de tendência.

---

### Resposta 3. "Qual foi meu melhor mês de todos os tempos em ROAS?"

Identificar na série da Chamada 7a o mês com melhor ROAS (Template A) ou menor CPL (Template B), considerando apenas meses com `spend > R$ 500` (evitar meses de teste com volume insuficiente).

#### Template A — Venda direta

```
🏆 MELHOR MÊS HISTÓRICO  ·  {nome_conta}

  Mês:      {AAAA-MM}
  ROAS:     {X.X}x
  Spend:    R$ {valor}
  Compras:  {N}
  CPA:      R$ {valor}

  O que estava diferente nesse mês vs. hoje:
  ─────────────────────────────────────────────────────────────────────
  Campanhas ativas então, pausadas hoje:
    • "{nome_campanha}" — pausada em {data} (identificada via Chamada 7b: stop_time)
    • "{nome_campanha}" — arquivada

  Campanhas ativas hoje que não existiam então:
    • "{nome_campanha}" — criada em {data} (start_time após o mês do pico)

  Spend nesse mês vs. spend atual:
    • Então: R$ {X} / Hoje: R$ {Y} / Variação: {+/-Z%}

  Hipótese mais provável:
    {Ex: "Campanha '{nome}' gerou 74% das compras daquele mês e foi pausada 45 dias depois.
     Reativar ou replicar o padrão dessa campanha é o caminho mais direto."}
```

#### Template B — Captação de leads

```
🏆 MELHOR MÊS HISTÓRICO  ·  {nome_conta}

  Mês:        {AAAA-MM}
  CPL:        R$ {valor}
  Spend:      R$ {valor}
  Leads:      {N}

  O que estava diferente nesse mês vs. hoje:
  ─────────────────────────────────────────────────────────────────────
  Campanhas ativas então, pausadas hoje:
    • "{nome_campanha}" — pausada em {data}
  ...
  Hipótese mais provável: {hipótese específica}
```

---

### Resposta 4. "Tem campanha pausada que performava bem e vale a pena reativar?"

Usar dados da Chamada 7c (performance histórica das campanhas pausadas/arquivadas) cruzados com os campos `created_time`, `updated_time` e `effective_status` da Chamada 7b. Exibir apenas campanhas com `spend > 0` no período de 6 meses.

**Regra de veredicto (aplicar na ordem abaixo — a primeira que bater define o veredicto):**

| Condição | Veredicto |
|---|---|
| ROAS > 2 (ou CPL < meta × 0,8) | Candidata a reativar |
| spend total < R$ 100 | Teste incompleto |
| ROAS < 1 (ou CPL > meta × 1,5) | Pausada com razão |
| Demais casos | Avaliar contexto |

#### Template A — Venda direta (OUTCOME_SALES)

```
⏸ CAMPANHAS PAUSADAS / ARQUIVADAS  ·  Últimos 6 meses  ·  Métrica: ROAS

  Campanha            Status     Criada em    Última modif.   Spend total   ROAS    Veredicto
  ───────────────────────────────────────────────────────────────────────────────────────────────
  {nome}              PAUSED     {AAAA-MM-DD} {AAAA-MM-DD}    R$ {X}        {Y.Y}x  Candidata a reativar
  {nome}              ARCHIVED   {AAAA-MM-DD} {AAAA-MM-DD}    R$ {X}        {Y.Y}x  Pausada com razão
  {nome}              PAUSED     {AAAA-MM-DD} {AAAA-MM-DD}    R$ {X}        {Y.Y}x  Teste incompleto
  ...

  Legenda:
  🟢 Candidata a reativar  — ROAS > 2. Vale testar novamente com budget controlado.
  🟡 Avaliar contexto      — ROAS entre 1 e 2. Reativar só se criativo foi renovado.
  🔴 Pausada com razão     — ROAS < 1. Não reativar sem reformular oferta e criativo.
  ⚪ Teste incompleto      — Spend < R$ 100. Sem dados suficientes para veredicto.

  Ação recomendada por grupo:
  • Candidatas a reativar: reativar com budget mínimo de R$ 30/dia via "trafego-otimizar"
    OU duplicar variando uma dimensão duplicando entidade no Gerenciador (variando 1 dimensão) antes de reativar.
  • Testes incompletos: avaliar se o objetivo ainda é relevante antes de continuar.
  • Pausadas com razão: reformular oferta/criativo via "copy-anuncio" antes de qualquer reativação.
```

#### Template B — Captação de leads (OUTCOME_LEADS)

```
⏸ CAMPANHAS PAUSADAS / ARQUIVADAS  ·  Últimos 6 meses  ·  Métrica: CPL

  Campanha            Status     Criada em    Última modif.   Spend total   CPL       Veredicto
  ──────────────────────────────────────────────────────────────────────────────────────────────────
  {nome}              PAUSED     {AAAA-MM-DD} {AAAA-MM-DD}    R$ {X}        R$ {Y}    Candidata a reativar
  {nome}              ARCHIVED   {AAAA-MM-DD} {AAAA-MM-DD}    R$ {X}        R$ {Y}    Pausada com razão
  {nome}              PAUSED     {AAAA-MM-DD} {AAAA-MM-DD}    R$ {X}        R$ {Y}    Teste incompleto
  ...

  Legenda:
  🟢 Candidata a reativar  — CPL < meta × 0,8. Eficiência acima da meta histórica.
  🟡 Avaliar contexto      — CPL entre meta × 0,8 e meta × 1,5. Decisão depende do contexto.
  🔴 Pausada com razão     — CPL > meta × 1,5. Custo inviável sem reformulação.
  ⚪ Teste incompleto      — Spend < R$ 100. Sem dados suficientes para veredicto.

  Ação recomendada por grupo:
  • Candidatas a reativar: reativar com budget mínimo de R$ 20/dia via "trafego-otimizar".
  • Testes incompletos: decidir se a hipótese original ainda faz sentido.
  • Pausadas com razão: reformular isca digital ou oferta via "lt-pagina" ou "copy-anuncio".
```

Se nenhuma campanha pausada ou arquivada tiver gasto nos últimos 6 meses, exibir: "Nenhuma campanha pausada com histórico de gasto identificada no período. Conta sem oportunidades óbvias de reativação."

> **Nota de cálculo:** para funil de venda direta, usar `meta de ROAS = receita_total / spend_total` do período ativo (Chamada 7a) como referência quando o perfil.md não informar meta explícita. Para funil de captação, usar CPL médio do período ativo como meta de referência.

---

### Resposta 5. "Qual foi o anúncio que mais gerou resultado na história da conta?"

Usar dados da Chamada 7d. Ordenar por total de `offsite_conversion.fb_pixel_purchase` (Template A) ou `offsite_conversion.fb_pixel_lead` (Template B) no período de 6 meses.

#### Template A — Venda direta

```
🥇 TOP 5 ANÚNCIOS HISTÓRICOS  ·  Últimos 6 meses  ·  Métrica: compras

  #   Anúncio                   Status atual   Campanha          Compras   CPA médio   Última atividade
  ──────────────────────────────────────────────────────────────────────────────────────────────────────
  1.  {nome}                    PAUSED         {nome_campanha}   187       R$ 64       2026-03-15
  2.  {nome}                    ACTIVE         {nome_campanha}   142       R$ 78       hoje
  3.  {nome}                    PAUSED         {nome_campanha}   98        R$ 81       2026-02-20
  4.  {nome}                    ARCHIVED       {nome_campanha}   87        R$ 89       2025-12-10
  5.  {nome}                    ACTIVE         {nome_campanha}   74        R$ 94       hoje

  Candidatos a reativar (PAUSED com histórico forte):
  • {nome} — pausado há {X dias}, gerou {N} compras com CPA R$ {Y}. CPA abaixo da média atual.
    Ação: reativar diretamente OU duplicar variando headline duplicando entidade no Gerenciador (variando 1 dimensão).

  Nota: anúncios ARCHIVED não podem ser reativados diretamente. Recriar com os mesmos criativos
  e copy via "copy-anuncio" usando o histórico como referência.
```

#### Template B — Captação de leads

```
🥇 TOP 5 ANÚNCIOS HISTÓRICOS  ·  Últimos 6 meses  ·  Métrica: leads

  #   Anúncio                   Status atual   Campanha          Leads     CPL médio   Última atividade
  ──────────────────────────────────────────────────────────────────────────────────────────────────────
  1.  {nome}                    PAUSED         {nome_campanha}   1.240     R$ 4,80     2026-03-10
  2.  {nome}                    ACTIVE         {nome_campanha}   980       R$ 5,20     hoje
  ...

  Candidatos a reativar: {nome} — pausado há {X dias}, gerou {N} leads com CPL R$ {Y}.
```

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0 — Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] Quais campanhas estão rodando há mais de 60 dias sem pausa? Precisam de refresh?
    → coberto? Se não: filtrar campanhas com data de criação anterior a 60 dias do período analisado e avaliar frequência e CTR atual

[ ] Evolução do CPA mês a mês nos últimos 6 meses?
    → coberto? Se não: montar tabela de CPA por mês com indicação de tendência (subindo/caindo/estável)

[ ] Qual foi o melhor mês em ROAS de todos os tempos?
    → coberto? Se não: identificar o mês com maior ROAS no histórico de 6 meses e destacar o contexto (sazonalidade, criativo, oferta)

[ ] Tem campanha pausada que performava bem e vale reativar?
    → coberto? Se não: listar campanhas com status PAUSED e CPA histórico abaixo do benchmark, com gasto total acumulado

[ ] Qual foi o anúncio que mais gerou resultado na história da conta?
    → coberto? Se não: rankear todos os anúncios por total de conversões no histórico disponível e destacar o vencedor absoluto
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico** — informar: (a) quantas campanhas longevas foram encontradas e quantas precisam de refresh; (b) tendência dos 6 meses (melhora, estável, deterioração); (c) qual foi o melhor mês e se está longe ou próximo da performance atual; (d) quantos dos top 5 anúncios estão pausados.

2. **Causa provável** — relacionar os dados em conjunto. Exemplos:
   - "CPA degradou 40% em 3 meses e as 2 campanhas com melhor histórico foram pausadas nesse mesmo intervalo. A degradação provavelmente veio da perda desses criativos, não de mudança de público."
   - "Melhor mês teve spend 30% menor que hoje — o crescimento de investimento não veio acompanhado de criativos novos, diluindo a performance média."

3. **No VTSD, isso significa…** — interpretar o dado histórico pelo método. Usar a tabela abaixo como guia:

   | Padrão histórico identificado | Elemento VTSD | Interpretação |
   |---|---|---|
   | Mês pico teve criativo específico, depois removido | Identidade do Comunicador | O tom e o estilo daquele criativo encarnavam a voz do Comunicador. Recriar no mesmo estilo é mais barato que criar do zero |
   | CPM subiu consistentemente nos últimos 3 meses | Saturação de público | A Urgência Oculta foi esgotada com o mesmo público. Precisamos de novos ângulos pela Mandala |
   | CPA degradou só em campanha específica longeva | Fadiga criativa por Quadro repetido | O Quadro foi mostrado tantas vezes que perdeu impacto. Variar a Furadeira no criativo resolve mais rápido que trocar público |
   | Volume de leads caiu sem mudança de CPL | Isca Digital | A oferta de captura ficou velha para o público novo que está chegando. Atualizar o Decorado da isca |
   | Melhor mês coincide com sazonalidade (ex: jan, set) | Timing | A Urgência Quente estava naturalmente alta naquele período. Replicar em próxima janela sazonal equivalente |

4. **Ação recomendada** — 1 a 3 ações concretas priorizadas por impacto esperado, com handoff para a skill executora.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Campanha longeva com CPA/CPL degradado > 30% | Duplicar entidade no Gerenciador (variando 1 dimensão) (A/B de criativo novo) ou "trafego-otimizar" (refresh defensivo com pausa parcial) |
| Anúncio pausado com histórico forte (top 5) | Sugerir reativar manualmente OU duplicar variando uma dimensão duplicando entidade no Gerenciador (variando 1 dimensão) |
| Anúncio arquivado com histórico forte | "copy-anuncio" para recriar no mesmo estilo + "trafego-criar-campanha" para subir novamente |
| Tendência de deterioração > +30% em 3 meses | output [6] Investigação Profunda para isolar a causa raiz |
| Melhor mês distante da performance atual | output [2] Performance & Funil para mapear onde o funil piorou desde então |
| Público/audience do melhor mês não em uso | Gerenciador de Audiences (recriar Lookalike a partir da base do período pico) |
| Campanha do melhor mês pausada e elegível | "trafego-otimizar" para reativar em modo controlado (budget pequeno + monitoramento) |

---

## Mapeamento HTML (export via `_export-html.md`)

| Bloco do output narrado | Componente do design system |
|---|---|
| Tabela de campanhas longevas (Bloco 1) | `.table` com colunas mono — `.down` (rust) nas linhas com degradação > 30% ou freq > 5 |
| Status de cada campanha longeva (🟢/🟡/🔴) | `.kpi` com classe `.up` ou `.down` conforme classificação |
| Gráfico de barras da evolução mensal (Bloco 2) | série de `.bar-row` — largura proporcional ao CPA/CPL, cor conforme tendência do mês |
| KPIs do melhor mês histórico (Bloco 3) | `.kpi-grid` com 4 `.kpi` (mês, ROAS/CPL, spend, compras/leads) |
| Lista do que estava diferente no melhor mês | `.callout` (um por diferença identificada) |
| Tabela top 5 anúncios históricos (Bloco 4) | `.table` com `--neon` na linha #1 e `.down` em anúncios ARCHIVED |
| Candidatos a reativar | `.regra.alerta` (um elemento por candidato identificado) |
| Frase "No VTSD isso significa..." | `.callout` |
| Ação recomendada | `.pitch-box` |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no rodapé |
