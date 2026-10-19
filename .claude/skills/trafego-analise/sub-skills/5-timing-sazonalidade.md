# Output [5]. Timing & Sazonalidade

Quando os anúncios performam melhor: dia da semana, horário do dia, efeito salário, tendência mensal e impacto de datas comemorativas e feriados nacionais.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- "Qual dia da semana eu deveria aumentar o orçamento?"
- "Meus resultados de segunda a sexta são diferentes do fim de semana?"
- "Meus resultados mudam no começo vs. final do mês? O público compra mais perto do salário?"
- "Qual horário do dia meus anúncios performam melhor?"
- "Datas comemorativas afetaram meu CPM? (Black Friday, Dia das Mães, etc.)"
- "Feriado atrapalha ou melhora meus resultados?"

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## Dados necessários

### O que já vem do Passo 4 do command principal

`level=account`, sem breakdowns. Campos base: `spend`, `impressions`, `clicks`, `actions`, `action_values`, `cost_per_action_type`.

Período: conforme escolha do aluno no Passo 3. Não perguntar novamente.

**Alerta de período curto:** se o período selecionado for menor que 30 dias, informar antes de executar:

```
⚠️ Períodos curtos (< 30 dias) reduzem a confiabilidade da análise de timing:
   - Padrão por dia da semana precisa de pelo menos 4 semanas para amostragem confiável
   - Padrão por horário agrega o total do período, funciona com qualquer janela
   - Tendência mensal usa sempre os últimos 6 meses (Chamada 5c), independente do período principal

Deseja estender o período de análise para 60 ou 90 dias? (opcional)
1. Sim, usar 60 dias
2. Sim, usar 90 dias
3. Não, continuar com o período atual
```

### Campos adicionais

Nenhum campo adicional além dos que já vêm do Passo 4. Os detalhamentos de timing são obtidos por breakdowns e `time_increment` nas chamadas adicionais abaixo.

### Chamadas adicionais (executar antes de montar os blocos)

**Chamada 5a. Horário do dia (breakdown por hora)**

Usa `since` / `until` derivados do período do aluno. O breakdown `hourly_stats_aggregated_by_advertiser_time_zone` retorna 24 linhas agregando todo o período: uma linha por hora (0 a 23) no fuso da conta do anunciante.

Nota técnica: este breakdown não é compatível com `date_preset`. Converter o período do aluno para `since` / `until` antes de montar a URL.

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=spend,impressions,clicks,actions,action_values,cost_per_action_type
  &breakdowns=hourly_stats_aggregated_by_advertiser_time_zone
  &level=account
  &since={DATA_INICIO}
  &until={DATA_FIM}
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com `breakdown=hourly_stats_aggregated_by_advertiser_time_zone` e as datas convertidas. Conferir os parâmetros pelo schema da tool; se ela não aceitar o recorte por hora, avisar o aluno e omitir a análise por horário (nunca inventar a distribuição).

---

**Chamada 5b. Diária (padrão por dia da semana e efeito salário)**

Retorna uma linha por dia calendário (formato `YYYY-MM-DD`). A partir dessas datas:
- Agrupar por dia da semana: extrair `weekday()` de cada data (0 = segunda, 6 = domingo) e calcular média por dia.
- Agrupar por decêndio do mês: dias 1-10 / 11-20 / 21-31, para identificar efeito salário.
- Cruzar datas com calendário de comemorativas e feriados (Bloco 4).

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=spend,impressions,clicks,actions,action_values,cost_per_action_type
  &level=account
  &date_preset={PERIOD_DO_ALUNO}
  &time_increment=1
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

Nota: o parâmetro `effective_status` NÃO é aceito no endpoint `/insights` (vale apenas nos endpoints de listagem `/campaigns`, `/adsets` e `/ads`). Se o filtro por status for necessário, a filtragem é feita na etapa anterior, na listagem de campanhas.

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com `time_increment=1` e os parâmetros de período equivalentes.

---

**Chamada 5c. Mensal (tendência de 6 meses: sempre fixa, independente do período principal)**

Retorna uma linha por mês calendário. Usar sempre `last_180d` com `time_increment=monthly` para garantir 6 meses de histórico independente do que o aluno escolheu no Passo 3.

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=spend,impressions,clicks,cpm,actions,action_values,cost_per_action_type
  &level=account
  &date_preset=last_180d
  &time_increment=monthly
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

Sem filtro de status: `effective_status` não vale em `/insights` (ver nota da Chamada 5b). Se necessário, a filtragem é feita na etapa de listagem de campanhas.

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com `time_increment=monthly` e `date_preset=last_180d`.

### Referência de produto

Ler do `resumo-produto.md` (já carregado no Passo 0.1 do `SKILL.md`) o preço e o tipo de produto. Não perguntar de novo. O preço serve para classificar CPA/CPL como saudável ou problemático nos comparativos de timing. Inferir tipo de funil pelo objetivo predominante das campanhas: `OUTCOME_SALES` → métrica-norte ROAS + CPA; `OUTCOME_LEADS` → métrica-norte CPL.

---

## Fórmulas de cálculo (obrigatório aplicar antes de montar os blocos)

| Métrica | Fórmula | Tipo canônico |
|---|---|---|
| CPA | `spend` / `purchases` | `offsite_conversion.fb_pixel_purchase` |
| CPL | `spend` / `leads` | `offsite_conversion.fb_pixel_lead` |
| ROAS | `sum(action_values onde action_type = "offsite_conversion.fb_pixel_purchase")` / `spend` | `offsite_conversion.fb_pixel_purchase` |
| CPM | (`spend` / `impressions`) × 1000 | - |

**Métrica-norte por tipo de funil:**
- `OUTCOME_SALES`: CPA e ROAS em todos os blocos.
- `OUTCOME_LEADS`: CPL em todos os blocos.

**CPM médio da conta** = `sum(spend de todos os dias)` / (`sum(impressions)` / 1000). Calculado a partir da Chamada 5b. Usado como linha de base para identificar datas com leilão inflacionado no Bloco 4.

**Índice vs. média** (usado no Bloco 1): `(CPA_dia - CPA_medio) / CPA_medio × 100`. Negativo = dia mais barato que a média (bom). Positivo = dia mais caro (pior).

**Variação de tendência** (usado no Bloco 3): regressão linear simples sobre os 6 pontos mensais de CPA/CPL. Classificar:
- Melhorando: inclinação negativa ≥ 5% no período.
- Piorando: inclinação positiva ≥ 5% no período.
- Estável: variação < 5% em qualquer direção.

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "Qual dia da semana eu deveria aumentar o orçamento?"

Usar dados da Chamada 5b agrupados por `weekday()`. Calcular a média de cada métrica por dia: total acumulado do dia ÷ número de ocorrências daquele dia no período.

**Template A. Venda direta (OUTCOME_SALES):**

```
📅 DIA DA SEMANA  ·  {período}  ·  média por dia

  Dia        Spend      CPA        ROAS    Conv.   Índice vs. média
  ──────────────────────────────────────────────────────────────────
  Segunda    R$ {X}     R$ {Y}     {Z}x    {N}     {+/-P%}
  Terça      R$ {X}     R$ {Y}     {Z}x    {N}     {+/-P%}
  Quarta     R$ {X}     R$ {Y}     {Z}x    {N}     {+/-P%}
  Quinta     R$ {X}     R$ {Y}     {Z}x    {N}     {+/-P%}
  Sexta      R$ {X}     R$ {Y}     {Z}x    {N}     {+/-P%}
  Sábado     R$ {X}     R$ {Y}     {Z}x    {N}     {+/-P%}
  Domingo    R$ {X}     R$ {Y}     {Z}x    {N}     {+/-P%}

  Top 3 dias (CPA mais barato):  {lista}
  Bottom 2 dias (CPA mais caro): {lista}
  Fim de semana vs. semana:      CPA {X%} {melhor | pior} nos fins de semana
```

**Template B. Captação de leads (OUTCOME_LEADS):**

```
📅 DIA DA SEMANA  ·  {período}  ·  média por dia

  Dia        Spend      CPL        Leads   Índice vs. média
  ──────────────────────────────────────────────────────────
  Segunda    R$ {X}     R$ {Y}     {N}     {+/-P%}
  Terça      R$ {X}     R$ {Y}     {N}     {+/-P%}
  Quarta     R$ {X}     R$ {Y}     {N}     {+/-P%}
  Quinta     R$ {X}     R$ {Y}     {N}     {+/-P%}
  Sexta      R$ {X}     R$ {Y}     {N}     {+/-P%}
  Sábado     R$ {X}     R$ {Y}     {N}     {+/-P%}
  Domingo    R$ {X}     R$ {Y}     {N}     {+/-P%}

  Top 3 dias (CPL mais barato):  {lista}
  Bottom 2 dias (CPL mais caro): {lista}
  Fim de semana vs. semana:      CPL {X%} {melhor | pior} nos fins de semana
```

Threshold para sinalizar dia crítico: CPA/CPL ≥ 40% acima da média E gasto no dia ≥ 10% do total do período → marcar com `⚠️ candidato a dayparting`.

---

### Resposta 2. "Meus resultados de segunda a sexta são diferentes do fim de semana?"

Usar a mesma tabela gerada na Resposta 1. Destacar a linha de resumo comparativo:

- Dias úteis (segunda a sexta): CPA/CPL médio R$ {X}, volume {N} conversões.
- Fim de semana (sábado e domingo): CPA/CPL médio R$ {X}, volume {N} conversões.
- Diferença: CPA/CPL {X%} {melhor | pior} nos fins de semana vs. dias úteis.

Se a diferença for ≥ 20%: recomendar ajuste de budget por dia da semana via `trafego-regras` (delivery schedule ou regra automática).

Se a diferença for < 20%: informar "Distribuição uniforme entre dias úteis e fim de semana, sem padrão que justifique dayparting por dia da semana no momento."

---

### Resposta 3. "Meus resultados mudam no começo vs. final do mês? O público compra mais perto do salário?"

Agregar os dias da Chamada 5b em três grupos e comparar CPA/CPL médio de cada grupo. Exibir somente se a diferença entre o grupo mais barato e o mais caro for ≥ 15%:

```
  Efeito salário detectado:
  Dias  1-10:  CPA R$ {X}  ·  Conv.: {N}
  Dias 11-20:  CPA R$ {X}  ·  Conv.: {N}
  Dias 21-31:  CPA R$ {X}  ·  Conv.: {N}
  Padrão: {início | meio | fim} do mês converte mais barato ({X%} abaixo da média)
```

Se diferença < 15%: informar "Efeito salário não detectado neste período, distribuição de conversões uniforme ao longo do mês."

---

### Resposta 4. "Qual horário do dia meus anúncios performam melhor?"

Usar dados da Chamada 5a (24 linhas, uma por hora). Agrupar em 4 faixas para visualização inicial, depois detalhar a hora exata de melhor e pior desempenho.

**Template A. Venda direta (OUTCOME_SALES):**

```
🕐 HORÁRIO  ·  {período}  ·  totais agregados do período

  Faixa        Spend      CPA        ROAS    Conv.
  ──────────────────────────────────────────────────
  00h-05h      R$ {X}     R$ {Y}     {Z}x    {N}
  06h-11h      R$ {X}     R$ {Y}     {Z}x    {N}
  12h-17h      R$ {X}     R$ {Y}     {Z}x    {N}
  18h-23h      R$ {X}     R$ {Y}     {Z}x    {N}

  Pico de conversão:  {faixa ou hora exata com mais conversões}
  Melhor CPA:         {hora exata}h  ·  CPA R$ {X}
  Vale (CPA alto):    {hora exata}h  ·  CPA R$ {X} ({Y%} acima da média) → candidato a dayparting
```

**Template B. Captação de leads (OUTCOME_LEADS):**

```
🕐 HORÁRIO  ·  {período}  ·  totais agregados do período

  Faixa        Spend      CPL        Leads
  ──────────────────────────────────────────
  00h-05h      R$ {X}     R$ {Y}     {N}
  06h-11h      R$ {X}     R$ {Y}     {N}
  12h-17h      R$ {X}     R$ {Y}     {N}
  18h-23h      R$ {X}     R$ {Y}     {N}

  Pico de captação:   {faixa ou hora exata com mais leads}
  Melhor CPL:         {hora exata}h  ·  CPL R$ {X}
  Vale (CPL alto):    {hora exata}h  ·  CPL R$ {X} ({Y%} acima da média) → candidato a dayparting
```

Threshold para candidato prioritário a dayparting: faixa horária com CPA/CPL ≥ 50% acima da média da conta E spend da faixa > 10% do total. Sinalizar como `⚠️ programar pausa via "trafego-regras"`.

Se `actions` retornar zero em todas as horas (pixel sem conversão configurada): exibir somente CPM e CTR por faixa e alertar: "Conversões não rastreadas por hora. Configure o evento de compra/lead no pixel via 'trafego-pixel' para análise completa."

---

### Resposta 5. "Datas comemorativas afetaram meu CPM? (Black Friday, Dia das Mães, etc.)"

Detectar dias com CPM > 30% acima da média da conta (calculada via Chamada 5b) e cruzar com o calendário de datas comemorativas comerciais.

Datas que concentram volume de anúncios concorrentes e encarecem o leilão de forma previsível:

| Data comemorativa | Período de impacto no leilão |
|---|---|
| Black Friday | Semana anterior ao último sexta de novembro |
| Natal | 18 a 24/12 |
| Dia das Mães | Semana anterior ao 2º domingo de maio |
| Dia dos Pais | Semana anterior ao 2º domingo de agosto |
| Dia dos Namorados | 06 a 12/06 |
| Volta às aulas | 1ª quinzena de fevereiro e de julho |
| Carnaval | 4 dias antes da quarta de cinzas + própria semana |

**Formato de apresentação:**

```
🎉 DATAS COMEMORATIVAS  ·  {período analisado}

  Data / Evento            Tipo            CPM no período    vs. média    Impacto no CPA/CPL
  ──────────────────────────────────────────────────────────────────────────────────────────
  {data}: {evento}        Comemorativa    R$ {X}            +{Y%}        CPA {+/-Z%}

  Legenda: Comemorativa = data de alto volume comercial (Dia das Mães, Dia dos Namorados,
  Black Friday etc.). Leilão tende a encarecer porque concorrentes aumentam budget.
  Oportunidade de copy temática alinhada ao contexto emocional da data.

  Estratégia para próxima ocorrência:
  - CPM alto + CPA piorou:    reduzir budget ou pausar na semana do evento
  - CPM alto + CPA manteve:   leilão caro mas produto resistiu, manter com orçamento controlado
  - CPM alto + CPA melhorou:  público em modo de compra, considerar aumentar budget
```

Threshold de detecção: CPM do período de 3 dias em torno da data ≥ 30% acima do CPM médio do mês calculado via Chamada 5b.

Se nenhuma data comemorativa for identificada no período: informar "Nenhuma data comemorativa com CPM anômalo detectado no período selecionado."

---

### Resposta 6. "Feriado atrapalha ou melhora meus resultados?"

Cruzar os dados diários da Chamada 5b com o calendário de feriados nacionais brasileiros. Feriados alteram o comportamento de consumo, mas não necessariamente encarecem o leilão: às vezes o CPM cai porque concorrentes pausam.

| Feriado | Data fixa ou referência |
|---|---|
| Ano Novo | 01/01 |
| Carnaval | Calculado (móvel: 47 dias antes da Páscoa) |
| Sexta-Feira Santa | Calculado (móvel: véspera da Páscoa) |
| Tiradentes | 21/04 |
| Dia do Trabalho | 01/05 |
| Corpus Christi | Calculado (móvel: 60 dias após Páscoa) |
| Independência do Brasil | 07/09 |
| Nossa Senhora Aparecida | 12/10 |
| Finados | 02/11 |
| Proclamação da República | 15/11 |
| Natal (feriado) | 25/12 |

**Formato de apresentação:**

```
🗓️ FERIADOS  ·  {período analisado}

  Data / Evento            Tipo      CPM no período    vs. média    Impacto no CPA/CPL
  ──────────────────────────────────────────────────────────────────────────────────────
  {data}: {evento}        Feriado   R$ {X}            +{Y%}        CPA {+/-Z%}

  Legenda: Feriado = dia sem trabalho (Tiradentes, Corpus Christi, etc.). Comportamento do
  público muda, mas o leilão pode cair se concorrentes pausarem. Verificar CPM real antes
  de interpretar.

  Nota condicional. Feriado + CPM baixo:
  Se Tipo = Feriado E variação de CPM < -10%: marcar como "oportunidade"
  (leilão esvaziou porque concorrentes pausaram; CPA tende a ser melhor mesmo com volume menor).
  Ação sugerida: aumentar budget moderadamente (+20%) e monitorar CPA nas primeiras 4 horas.

  Estratégia para próxima ocorrência:
  - CPM caiu + CPA manteve:   concorrentes pausaram, oportunidade de escalar com CPM baixo
  - CPM caiu + CPA piorou:    público distraído pelo feriado, produto sensível a contexto emocional
```

Se nenhum feriado for identificado no período: informar "Nenhum feriado nacional detectado no período selecionado."

---

### Análise adicional. Tendência mensal (últimos 6 meses)

Usar dados da Chamada 5c. Exibir sempre os 6 meses independente do período principal escolhido pelo aluno no Passo 3. Esta seção fornece contexto histórico e complementa as respostas acima.

**Template A. Venda direta (OUTCOME_SALES):**

```
📈 TENDÊNCIA MENSAL  ·  últimos 6 meses

  Mês        CPM        CPA        ROAS    Spend      Conv.
  ───────────────────────────────────────────────────────────
  {YYYY-MM}  R$ {X}     R$ {Y}     {Z}x    R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     {Z}x    R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     {Z}x    R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     {Z}x    R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     {Z}x    R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     {Z}x    R$ {W}     {N}

  Tendência de CPA:     {melhorando | estável | piorando}  ({+/-X%} no período)
  Tendência de CPM:     {subindo | estável | caindo}       ({+/-X%} no período)
  Mês de melhor CPA:    {mês}  ·  hipótese: {o que funcionou naquele mês}
  Mês de CPM mais caro: {mês}  ·  hipótese: {sazonalidade / Black Friday / concorrência}
```

**Template B. Captação de leads (OUTCOME_LEADS):**

```
📈 TENDÊNCIA MENSAL  ·  últimos 6 meses

  Mês        CPM        CPL        Spend      Leads
  ────────────────────────────────────────────────────
  {YYYY-MM}  R$ {X}     R$ {Y}     R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     R$ {W}     {N}
  {YYYY-MM}  R$ {X}     R$ {Y}     R$ {W}     {N}

  Tendência de CPL:     {melhorando | estável | piorando}  ({+/-X%} no período)
  Tendência de CPM:     {subindo | estável | caindo}       ({+/-X%} no período)
  Mês de melhor CPL:    {mês}  ·  hipótese: {o que funcionou naquele mês}
  Mês de CPM mais caro: {mês}  ·  hipótese: {sazonalidade / Black Friday / concorrência}
```

Regra de interpretação de tendência de CPM:

| Variação do CPM (6 meses) | Interpretação | Hipótese prioritária |
|---|---|---|
| Subindo > 30% | 🔴 Leilão encarecendo | Saturação de público ou concorrência crescente no nicho |
| Subindo 10% a 30% | 🟡 Atenção | Pode ser sazonalidade: cruzar com datas do calendário |
| Estável (±10%) | 🟢 Leilão saudável | Nenhuma ação necessária |
| Caindo > 10% | 🟢 Leilão melhorando | Novo criativo, novo público ou saída de concorrentes |

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0. Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] Qual dia da semana deveria aumentar o orçamento?
    → coberto? Se não: agregar spend e CPA por day_of_week e identificar o dia com melhor custo-benefício

[ ] Resultados de segunda a sexta são diferentes do fim de semana?
    → coberto? Se não: calcular médias de CPA e CTR separadas por dias úteis vs. sábado-domingo

[ ] Resultados mudam no começo vs. final do mês? (efeito salário)
    → coberto? Se não: dividir os dias em três decêndios (1-10, 11-20 e 21-31) e comparar o CPA de cada um

[ ] Qual horário do dia os anúncios performam melhor?
    → coberto? Se não: usar breakdown hourly_stats e identificar janelas de menor CPA e maior CTR

[ ] Datas comemorativas afetaram o CPM? (Black Friday, Dia das Mães, etc.)
    → coberto? Se não: marcar datas especiais no histórico e comparar CPM nessas datas vs. média do período

[ ] Feriado atrapalha ou melhora os resultados?
    → coberto? Se não: identificar dias com CPM acima da média em 30% e cruzar com calendário de feriados
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico**: melhor dia da semana (com CPA/CPL), melhor faixa horária, tendência dos últimos 6 meses (CPA/CPL e CPM) e datas/feriados detectados no período.
2. **Causa provável**: explicação por sazonalidade, comportamento do público ou competição no leilão. Ex: "CPA sobe às segundas porque o público retoma o trabalho e a atenção cai. Fim de semana converte mais barato porque a decisão é tomada no momento de lazer, sem pressão de agenda."
3. **No VTSD, isso significa…**: qual elemento do método está em jogo. Ex: "Pico de conversão às 21h = horário de cama, estado emocional de baixa guarda. Urgência Oculta de conforto e desejo funciona melhor que argumento racional nesse horário." Ou: "Conversões concentradas nos dias 1 a 5 do mês = público compra com salário fresco. Aumentar budget nessa janela e reduzir no final do mês, onde o CPA dobra, sem mudar uma linha de copy."
4. **Ação recomendada**: 1 a 3 ações concretas com handoff para skill executora.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Vale horário claro (CPA/CPL ≥ 50% acima da média em faixa específica com gasto > 10%) | "trafego-regras": programação liga/pausa (delivery schedule) |
| Dia da semana crítico (CPA/CPL ≥ 40% acima da média) | "trafego-regras": regra automática para reduzir budget no dia problemático |
| Data comemorativa com CPM alto confirmado | "trafego-regras": regra automática para reduzir budget na semana do evento |
| Efeito salário detectado (dias 1-10 mais baratos ≥ 15%) | "trafego-regras", regra: aumentar budget +20% nos dias 1-10 do mês |
| Feriado com CPM baixo + CPA manteve | "trafego-escalar": oportunidade de escalar quando concorrentes pausam |
| Mês com CPA/CPL melhor identificado (hipótese clara) | "trafego-testes": reproduzir condições do mês vencedor (criativo, público, orçamento) |
| Tendência de CPM subindo por 3 ou mais meses | "trafego-publicos": explorar audiências novas antes que o CPM torne inviável |

---

## Mapeamento HTML (export via `_export-html.md`)

Componentes definidos na seção 3.2 do `_export-html.md`. **Usar exatamente estes nomes de classe.** O vocabulário antigo (`.table`, `.kpi-grid`, `.kpi`, `.regra`, `.callout`, `.pitch-box`, `.bar-row`, `.up`, `.down`, `--neon`) foi descontinuado e NÃO existe no CSS embutido: usá-lo gera seção sem estilo.

| Bloco do output narrado | Componente do design system |
|---|---|
| KPIs globais (gasto, CPA/CPL, ROAS, CPM médio, melhor dia, melhor faixa horária) | `.stats-grid` com um `.stat-card` por métrica (`.value.green/.yellow/.red` conforme semântica) |
| Cada "Resposta N" obrigatória | `.section` com `.section-header` (`.section-num` + `.section-title` + `.section-question`, texto exato da pergunta) |
| Tabela por dia da semana | `.card` + `table`; coluna "Índice vs. média" colorida com `style="color:var(--green)"` (dia abaixo do CPA/CPL médio) ou `var(--red)` (acima); `.num` nas colunas numéricas |
| Tabela por faixa horária | `.card` + `table`; linha do vale com `var(--red)`, linha do pico de conversão com `var(--green)` |
| Efeito salário (3 decêndios) | `.card` + `.card-grid-3` com um bloco por período (dias 1-10, 11-20, 21-31) OU os 3 decêndios como `.funnel-item` numa `.funnel-row` |
| Tendência mensal (6 meses) | `.card` + `table`; melhor mês com célula em `var(--green)` |
| Cada data comemorativa / feriado detectado | `.diag-box` (`.yellow` se CPM inflacionou, `.green` se virou oportunidade): um por data |
| Frase "No VTSD isso significa..." | `.diag-box` (+ `.green/.yellow/.red` conforme o sinal) |
| Ação recomendada | `.action-box` |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no `.page-foot` |

### Gráficos obrigatórios deste output

Renderizar os gráficos abaixo logo após o `.stats-grid` de KPIs, sob um `.section-h` "Visão visual". Todos em SVG/CSS inline, sem dependência (receitas detalhadas nas seções **3.2.1** e **3.2.1.1** do `_export-html.md`). Gráficos com muitos pontos ou geometria não trivial usam o helper `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py` (matemática pura, sem token, sem Graph API).

| Gráfico | Componente / receita | Fonte de dado | Posição |
|---|---|---|---|
| Heatmap hora × dia da semana de CPA | SVG heatmap (receita H via helper `heatmap`, `scale:"good_low"`) | matriz hora×dia cruzando Chamada 5a com 5b: **ver regra abaixo** | `.chart-card` full-width, topo da "Visão visual" |
| CPA por faixa horária (4 buckets) | SVG barras verticais (receita G via helper `vbars`) | Chamada 5a agregada em 0-5h / 6-11h / 12-17h / 18-23h | `.charts-grid`, junto da Resposta 4 |
| Tendência mensal de CPM (6 meses) | SVG linha (receita F via helper `line`) | Chamada 5c (`time_increment=monthly`, `last_180d`), série de CPM | `.chart-card` full-width, junto da Análise adicional (tendência mensal) |

**Regra do heatmap hora × dia da semana (limitação real da API):** o breakdown `hourly_stats_aggregated_by_advertiser_time_zone` (Chamada 5a) entrega **24 valores agregados sobre todo o período**, NÃO cruzados com o dia da semana. A Meta **não oferece** breakdown combinado hora×dia em uma única chamada de insights de conta. Caminhos, em ordem de preferência:

1. **Matriz real:** disparar a Chamada 5a uma vez por dia da semana, restringindo `since`/`until` a cada conjunto de datas do mesmo weekday no período (7 chamadas). Montar a matriz 7×24 (ou 7×4 faixas) e renderizar o heatmap com `scale:"good_low"` (CPA baixo = verde, alto = vermelho). Custa 7 chamadas extras e exige período ≥ 4 semanas para amostragem confiável por célula.
2. **Degradar para vbars:** se as 7 chamadas estourarem rate limit ou o período for curto, renderizar apenas o gráfico de **CPA por faixa horária** (vbars, 4 buckets, agregado do período) e **omitir o heatmap**, documentando no chat que o cruzamento hora×dia exige período longo.
3. **Nunca inventar a matriz** a partir dos 24 valores agregados: isso fabricaria um cruzamento que o dado não contém.

Regras dos gráficos: usar só cores da paleta (`--green/--yellow/--orange/--red/--accent`); CPA/CPL é "quanto menor melhor" → no heatmap usar `scale:"good_low"`, nas vbars colorir verde a faixa de menor CPA e vermelho a de maior; rótulos de mês saem como `YYYY-MM` ou abreviados; se a Chamada 5c retornar menos de 3 meses com `spend > R$ 200`, omitir a linha de tendência de CPM.
