# Output [4] — Geo & Demografia

Análise de quem está convertendo: faixa etária, gênero, estado e capital vs. interior. Revela se a Identidade do Consumidor declarada no perfil bate com quem de fato compra.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- "Qual estado/cidade está me trazendo as conversões mais baratas?"
- "Tem região onde estou gastando muito e não vem resultado?"
- "Homens ou mulheres convertem mais nas minhas campanhas?"
- "Qual faixa etária é meu ponto cego — gasto pouco e poderia explorar?"
- "Meus anúncios performam melhor em capitais ou no interior?"

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## Dados necessários

### O que já vem do Passo 4 do command principal

`level=account`, sem breakdowns. Campos base: `spend`, `impressions`, `clicks`, `ctr`, `actions`, `action_values`, `cost_per_action_type`.

Período: conforme escolha do aluno no Passo 3. Não perguntar novamente.

### Campos adicionais a acrescentar na chamada principal deste output

Nenhum campo adicional é necessário na chamada base. Todas as análises deste output dependem das chamadas com breakdowns abaixo. Os breakdowns de Geo & Demo exigem chamadas separadas — a API não permite combinar `age,gender` com `region` numa única requisição. Tampouco é possível cruzar geo + demo numa única chamada (ex: "mulheres 25-34 em SP"). Os pontos cegos demográfico e geográfico são calculados separadamente.

### Chamadas adicionais (executar antes de montar os blocos)

**Chamada 4a — Demográfica (idade + gênero)**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights\
?fields=spend,impressions,clicks,actions,action_values,cost_per_action_type\
&breakdowns=age,gender\
&level=account\
&date_preset={PERIOD_DO_ALUNO}\
&limit=500\
&access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com `breakdown=["age","gender"]` e demais parâmetros equivalentes.

---

**Chamada 4b — Geográfica por estado (region)**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights\
?fields=spend,impressions,clicks,actions,action_values,cost_per_action_type\
&breakdowns=region\
&level=account\
&date_preset={PERIOD_DO_ALUNO}\
&limit=500\
&access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com `breakdown=["region"]` e demais parâmetros equivalentes.

---

**Chamada 4c — Por país (confirmação de cobertura)**

Usar somente se a conta tiver targeting para múltiplos países. Se o targeting for exclusivamente Brasil, esta chamada pode ser omitida.

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights\
?fields=spend,impressions,clicks,actions,action_values,cost_per_action_type\
&breakdowns=country\
&level=account\
&date_preset={PERIOD_DO_ALUNO}\
&limit=500\
&access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com `breakdown=["country"]` e demais parâmetros equivalentes.

---

**Nota sobre capital vs. interior:** o breakdown `dma` da API é calibrado para o mercado americano e retorna dados pouco granulares no Brasil. A divisão capital/interior é feita manualmente: usar os dados da Chamada 4b e classificar cada região retornada como capital ou interior com base na lista de capitais estaduais (São Paulo, Rio de Janeiro, Belo Horizonte, Salvador, Fortaleza, Manaus, Curitiba, Recife, Porto Alegre, Belém, Goiânia, Florianópolis, São Luís, Maceió, Natal, Teresina, Campo Grande, João Pessoa, Aracaju, Cuiabá, Macapá, Porto Velho, Rio Branco, Palmas, Boa Vista). Regiões não mapeadas nessa lista são tratadas como interior.

### Referência de produto

Ler `perfil.md` e `idconsumidor.md` (já carregados no Passo 0):
- Campo `preco` → benchmark de CPA/CPL conforme tabela do output [1]
- Campo de público-alvo declarado (sexo, faixa etária, região) → comparar com o que a API retornar
- Inferir tipo de funil pelo objetivo predominante das campanhas: `OUTCOME_SALES` = venda direta (métrica-norte: CPA + ROAS); `OUTCOME_LEADS` = captação (métrica-norte: CPL)

---

## Fórmulas de cálculo (obrigatório aplicar antes de montar os blocos)

Aplicar por linha de cada breakdown:

| Métrica | Fórmula | Tipo canônico |
|---|---|---|
| CPA | `spend` / `purchases` | `offsite_conversion.fb_pixel_purchase` |
| CPL | `spend` / `leads` | `offsite_conversion.fb_pixel_lead` |
| ROAS | `action_values[offsite_conversion.fb_pixel_purchase]` / `spend` | `offsite_conversion.fb_pixel_purchase` |
| CTR | `clicks` / `impressions` | — |

Usar a métrica-norte do funil (CPA/ROAS para venda direta, CPL para captação) como critério de ordenação e classificação em todos os blocos.

**Thresholds de classificação por linha de breakdown (aplicar uniformemente em todos os blocos):**

| Classificação | Critério |
|---|---|
| Vencedor | CPA ou CPL ≤ 80% do benchmark do produto |
| Saudável | CPA ou CPL entre 81% e 110% do benchmark |
| Atenção | CPA ou CPL entre 111% e 150% do benchmark |
| Buraco | CPA ou CPL > 150% do benchmark E spend > 5% do total do período |
| Ponto cego | CPA ou CPL ≤ 110% do benchmark E spend < 5% do total E ≥ 3 conversões |

Se conversões = 0 para uma linha: marcar CPA/CPL como `∞`. Marcar como "Queimando" se spend > 2% do total.

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

---

### Resposta 1. "Qual estado/cidade está me trazendo as conversões mais baratas?"

Dados vêm da Chamada 4b. Mostrar top 10 estados por spend, ordenados por CPA ou CPL crescente para identificar os vencedores geográficos.

#### Template A — Venda direta:

```
🗺️  POR ESTADO  ·  {período}  ·  Top 10 por spend

  Estado   Spend      CPA        ROAS    Conv.   % do total   Decisão
  ────────────────────────────────────────────────────────────────────
  SP       R$ {X}     R$ {Y}     {Z}x    {N}     {P%}         ✅ Manter
  RJ       R$ {X}     R$ {Y}     {Z}x    {N}     {P%}         📈 Escalar
  MG       R$ {X}     R$ {Y}     {Z}x    {N}     {P%}         🟡 Revisar
  BA       R$ {X}     ∞          —       0       {P%}         🛑 Excluir

  Top 3 por CPA mais barato:  {estado 1}, {estado 2}, {estado 3}
  Candidatos a excluir:       {estados com spend > 5% do total e CPA > 150% do benchmark}
```

#### Template B — Captação de leads:

```
🗺️  POR ESTADO  ·  {período}  ·  Top 10 por spend

  Estado   Spend      CPL        Leads   % do total   Decisão
  ──────────────────────────────────────────────────────────
  SP       R$ {X}     R$ {Y}     {N}     {P%}         ✅ Manter
  RJ       R$ {X}     R$ {Y}     {N}     {P%}         📈 Escalar
  MG       R$ {X}     R$ {Y}     {N}     {P%}         🟡 Revisar
  BA       R$ {X}     ∞          0       {P%}         🛑 Excluir

  Top 3 por CPL mais barato:  {estado 1}, {estado 2}, {estado 3}
  Candidatos a excluir:       {estados com spend > 5% do total e CPL > 150% do benchmark}
```

**Critério da coluna Decisão (aplicar com os thresholds canônicos da seção "Fórmulas"):**

| Decisão | Critério |
|---|---|
| Escalar | CPA ou CPL ≤ 80% do benchmark E spend < 20% do total (sub-explorado) |
| Manter | CPA ou CPL entre 81% e 110% do benchmark |
| Revisar | CPA ou CPL entre 111% e 150% do benchmark |
| Excluir | CPA ou CPL > 150% do benchmark E spend > 5% do total — ou spend > 2% com 0 conversões |

Se a conta tiver targeting nacional sem exclusões e houver 3 ou mais estados com decisão "Escalar", sugerir criar adsets separados para esses estados vencedores.

---

### Resposta 2. "Tem região onde estou gastando muito e não vem resultado?"

Usar os mesmos dados da Chamada 4b e da tabela gerada na Resposta 1. Destacar os estados com coluna Decisão "Excluir": spend alto sem retorno equivalente.

Critério de destaque: `CPA ou CPL > 150% do benchmark E spend > 5% do total` — ou `spend > 2% do total com 0 conversões`.

Para cada estado que se enquadrar:

```
🛑 REGIÃO SEM RETORNO

  Estado:          {nome do estado}
  Gasto no período: R$ {X}  ({P%} do total)
  Conversões:      {N}
  CPA atual:       R$ {Y}  ({Z%} acima do benchmark de R$ {benchmark})
  Ação imediata:   excluir esse estado do targeting via ajuste no adset (handoff para "trafego-otimizar")
```

Se nenhum estado se enquadrar nos critérios: informar "Nenhuma região com gasto elevado e resultado zero identificada no período."

---

### Resposta 3. "Homens ou mulheres convertem mais nas minhas campanhas?"

Dados vêm da Chamada 4a. Usar o template conforme tipo de funil identificado no Passo 0.

#### Template A — Venda direta (OUTCOME_SALES)

```
👥 DEMOGRAFIA  ·  {nome_conta}  ·  {período}

  Idade   Gênero   Spend      CPA        ROAS    Conv.   Classificação
  ────────────────────────────────────────────────────────────────────
  25-34   F        R$ {X}     R$ {Y}     {Z}x    {N}     ✅ Vencedor
  35-44   F        R$ {X}     R$ {Y}     {Z}x    {N}     ✅ Saudável
  25-34   M        R$ {X}     R$ {Y}     {Z}x    {N}     🟡 Atenção
  45-54   M        R$ {X}     R$ {Y}     ∞       0       🔴 Queimando
  18-24   F        R$ {X}     R$ {Y}     {Z}x    {N}     🔍 Ponto cego

  Vencedor:    {faixa etária + gênero} — CPA R$ {X}, {Y%} abaixo do benchmark (R$ {benchmark})
  Ponto cego:  {faixa etária + gênero} — gasto R$ {X} ({P%} do total), CPA R$ {Y} (saudável)
  Buraco:      {faixa etária + gênero} — R$ {X} gastos, {N} conversões, CPA {Y%} acima do benchmark
```

#### Template B — Captação de leads (OUTCOME_LEADS)

```
👥 DEMOGRAFIA  ·  {nome_conta}  ·  {período}

  Idade   Gênero   Spend      CPL        Leads   Classificação
  ────────────────────────────────────────────────────────────
  25-34   F        R$ {X}     R$ {Y}     {N}     ✅ Vencedor
  35-44   F        R$ {X}     R$ {Y}     {N}     ✅ Saudável
  25-34   M        R$ {X}     R$ {Y}     {N}     🟡 Atenção
  45-54   M        R$ {X}     ∞          0       🔴 Queimando
  18-24   F        R$ {X}     R$ {Y}     {N}     🔍 Ponto cego

  Vencedor:    {faixa etária + gênero} — CPL R$ {X}, {Y%} abaixo do benchmark (R$ {benchmark})
  Ponto cego:  {faixa etária + gênero} — gasto R$ {X} ({P%} do total), CPL R$ {Y} (saudável)
  Buraco:      {faixa etária + gênero} — R$ {X} gastos, {N} leads, CPL {Y%} acima do benchmark
```

Ordenar por `spend` decrescente. Mostrar todas as linhas com spend > 0. Omitir linhas sem impressões.

Após a tabela, consolidar por gênero (agregar todas as faixas etárias de cada gênero) para responder diretamente à pergunta:

```
  Resumo por gênero:
  Feminino    Spend total: R$ {X}   CPA médio: R$ {Y}   Conv. total: {N}
  Masculino   Spend total: R$ {X}   CPA médio: R$ {Y}   Conv. total: {N}

  Gênero vencedor: {F | M} — CPA {X%} mais barato
```

**Comparação com perfil declarado:** após o resumo por gênero, cruzar com o público-alvo em `perfil.md` e `idconsumidor.md`. Se o vencedor real divergir do perfil declarado, sinalizar explicitamente:

```
⚠️  DIVERGÊNCIA DE PÚBLICO
    Perfil declarado:  {sexo + faixa etária declarados no perfil.md/idconsumidor.md}
    Quem está {comprando | convertendo} de fato: {sexo + faixa etária vencedores}
    Leitura: ou a Identidade do Consumidor precisa ser atualizada, ou há um segmento
    novo que o produto alcançou sem intenção. Nos dois casos, vale investigar.
```

---

### Resposta 4. "Qual faixa etária é meu ponto cego — gasto pouco e poderia explorar?"

Dados vêm da Chamada 4a. Identificar clusters demográficos (faixa etária + gênero) que atendam os três critérios de ponto cego:

**Critério para ponto cego demográfico:**
- Spend < 5% do total do período
- CPA ou CPL ≤ 110% do benchmark do produto
- Mínimo de 3 conversões ou leads (sinal não-trivial)

#### Template A — Venda direta:

```
🔍 PONTO CEGO DEMOGRÁFICO

  Cluster:        {faixa etária} {gênero}
  Gasto atual:    R$ {X}  ({P%} do total)
  CPA atual:      R$ {Y}  ({Z%} do benchmark — saudável)
  Conversões:     {N}
  Estimativa:     se receber 10% do budget total (R$ {10%_do_spend_total}),
                  projeção de {floor(R$_10pct / CPA_atual)} compras adicionais no período.
  Ação: criar adset segmentado para este perfil no Gerenciador de Audiences + validar duplicando entidade no Gerenciador (variando 1 dimensão)
```

#### Template B — Captação de leads:

```
🔍 PONTO CEGO DEMOGRÁFICO

  Cluster:        {faixa etária} {gênero}
  Gasto atual:    R$ {X}  ({P%} do total)
  CPL atual:      R$ {Y}  ({Z%} do benchmark — saudável)
  Leads:          {N}
  Estimativa:     se receber 10% do budget total (R$ {10%_do_spend_total}),
                  projeção de {floor(R$_10pct / CPL_atual)} leads adicionais no período.
  Ação: criar adset segmentado para este perfil no Gerenciador de Audiences + validar duplicando entidade no Gerenciador (variando 1 dimensão)
```

**Fórmula da estimativa (obrigatório usar):**

```
budget_hipotetico = spend_total_periodo * 0.10
estimativa_adicional = floor(budget_hipotetico / CPA_ou_CPL_atual_do_cluster)
```

Nunca apresentar estimativa sem mostrar o raciocínio (`R$ {budget_hipotetico} / R$ {CPA_atual} = {N}`).

Se nenhum cluster demográfico atender os 3 critérios: informar "Nenhum ponto cego demográfico identificado com dados suficientes no período. Mínimo necessário: 3 conversões com spend < 5% do total e CPA dentro do benchmark."

---

### Resposta 5. "Meus anúncios performam melhor em capitais ou no interior?"

Agregar os dados da Chamada 4b: somar spend, conversões/leads e calcular CPA/CPL para o grupo "Capitais" (regiões que aparecem na lista de capitais estaduais) e o grupo "Interior" (todas as demais regiões).

#### Template A — Venda direta:

```
🏙️  CAPITAL vs. INTERIOR  ·  {período}

  Capitais    Spend: R$ {X}   CPA: R$ {Y}   ROAS: {Z}x   Conv.: {N}   ({P%} do gasto)
  Interior    Spend: R$ {X}   CPA: R$ {Y}   ROAS: {Z}x   Conv.: {N}   ({P%} do gasto)

  Vencedor: {Capital | Interior} — CPA {X%} mais barato
  Leitura: {interpretação concreta — ex: "Interior converte 28% mais barato mas recebe apenas 18%
            do budget. Rebalancear o gasto geográfico pode reduzir o CPA médio da conta."}
```

#### Template B — Captação de leads:

```
🏙️  CAPITAL vs. INTERIOR  ·  {período}

  Capitais    Spend: R$ {X}   CPL: R$ {Y}   Leads: {N}   ({P%} do gasto)
  Interior    Spend: R$ {X}   CPL: R$ {Y}   Leads: {N}   ({P%} do gasto)

  Vencedor: {Capital | Interior} — CPL {X%} mais barato
  Leitura: {interpretação concreta — ex: "Interior gera leads 22% mais baratos mas recebe apenas
            20% do budget. Criar adsets geográficos separados pode otimizar o CPL médio."}
```

Se a diferença de CPA ou CPL entre capital e interior for menor que 15%: informar "Diferença de {X%} — abaixo do limiar de 15%. Targeting nacional é adequado para este produto no período analisado."

---

### Análise adicional — Ponto cego geográfico

A API não permite cruzar faixa etária + gênero + estado numa única chamada. O ponto cego geográfico é calculado separadamente a partir da Chamada 4b e reportado aqui como análise complementar.

**Critério para ponto cego geográfico:**
- Spend < 5% do total do período
- CPA ou CPL ≤ 110% do benchmark do produto
- Mínimo de 3 conversões ou leads (sinal não-trivial)

#### Template A — Venda direta:

```
🔍 PONTO CEGO GEOGRÁFICO

  Estado/região:  {nome do estado}
  Gasto atual:    R$ {X}  ({P%} do total)
  CPA atual:      R$ {Y}  ({Z%} do benchmark — saudável)
  Conversões:     {N}
  Estimativa:     se receber 10% do budget total (R$ {10%_do_spend_total}),
                  projeção de {floor(R$_10pct / CPA_atual)} compras adicionais no período.
  Ação: criar adset com targeting geográfico isolado duplicando entidade no Gerenciador (variando 1 dimensão) — duplicar campanha winner
        restringindo a este estado
```

#### Template B — Captação de leads:

```
🔍 PONTO CEGO GEOGRÁFICO

  Estado/região:  {nome do estado}
  Gasto atual:    R$ {X}  ({P%} do total)
  CPL atual:      R$ {Y}  ({Z%} do benchmark — saudável)
  Leads:          {N}
  Estimativa:     se receber 10% do budget total (R$ {10%_do_spend_total}),
                  projeção de {floor(R$_10pct / CPL_atual)} leads adicionais no período.
  Ação: criar adset com targeting geográfico isolado duplicando entidade no Gerenciador (variando 1 dimensão) — duplicar campanha winner
        restringindo a este estado
```

**Fórmula da estimativa (obrigatório usar):**

```
budget_hipotetico = spend_total_periodo * 0.10
estimativa_adicional = floor(budget_hipotetico / CPA_ou_CPL_atual_do_cluster)
```

Nunca apresentar estimativa sem mostrar o raciocínio (`R$ {budget_hipotetico} / R$ {CPA_atual} = {N}`).

Se nenhum estado atender os 3 critérios: informar "Nenhum ponto cego geográfico identificado com dados suficientes no período. Mínimo necessário: 3 conversões com spend < 5% do total e CPA dentro do benchmark."

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0 — Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] Qual estado traz conversões mais baratas?
    → coberto? Se não: ordenar estados por CPA, destacar top 3 mais baratos e bottom 3 mais caros

[ ] Tem região onde estou gastando muito sem resultado?
    → coberto? Se não: calcular ROAS por estado e sinalizar onde gasto > 15% do total com ROAS abaixo de 1x

[ ] Homens ou mulheres convertem mais?
    → coberto? Se não: comparar CPA, CTR e volume de conversões segmentados por gênero

[ ] Qual faixa etária é meu ponto cego (gasto baixo e CPA competitivo)?
    → coberto? Se não: identificar faixas com share de gasto < 10% do total e CPA abaixo da média

[ ] Anúncios performam melhor em capitais ou no interior?
    → coberto? Se não: classificar top cidades entre capitais e interior e comparar CPA médio de cada grupo
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico** — vencedor demográfico (faixa etária + gênero), vencedor geográfico (estado), resultado da comparação capital vs. interior, e os pontos cegos identificados (se existirem).
2. **Causa provável** — por que esse cluster converte: alinhamento com a Identidade do Consumidor do produto, poder de compra da região, comportamento de consumo da faixa etária. Informar se é descoberta esperada (confirma o perfil declarado) ou surpresa (diverge do perfil declarado).
3. **No VTSD, isso significa…** — relacionar os achados com o método. Exemplos:
   - "Você desenhou a Identidade do Consumidor para mulheres 35-44, mas os dados mostram homens 45-54 como vencedores. Ou a Identidade está desalinhada com a realidade, ou há um público novo que o produto alcançou sem intenção. Nos dois casos, vale revisar o perfil ou criar uma linha de comunicação específica para esse cluster."
   - "Interior convertendo 30% mais barato que capitais com 80% menos budget: a Urgência Oculta do produto ressoa mais com quem não tem alternativa local — oportunidade clara de rebalancear o gasto geográfico."
   - "Faixa 45-54 com CPA 40% abaixo do benchmark mas apenas 3% do gasto: o Quadro do produto resolve um problema que essa faixa sente com mais intensidade. Falta orçamento alocado para ela."
4. **Ação recomendada** — 1 a 3 ações concretas com handoff para a skill executora.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Cluster demográfico vencedor com gasto < 10% do total | Gerenciador de Audiences — criar Saved Audience segmentada para o cluster + Duplicar entidade no Gerenciador (variando 1 dimensão) — adset isolado para validar em escala |
| Estado com gasto > 5% e CPA ou CPL > 150% do benchmark | "trafego-otimizar" — excluir região via ajuste de targeting no adset |
| Ponto cego demográfico identificado | Duplicar entidade no Gerenciador (variando 1 dimensão) — duplicar adset winner com segmentação de faixa etária + gênero isolados |
| Ponto cego geográfico identificado | Duplicar entidade no Gerenciador (variando 1 dimensão) — duplicar adset winner com targeting geográfico restrito ao estado |
| Vencedor real difere do público declarado no perfil | "produto-concepcao" — revisar Identidade do Consumidor com os dados reais da API |
| Capital vs. interior com diferença > 30% de CPA ou CPL | Duplicar entidade no Gerenciador (variando 1 dimensão) — criar adsets separados com targeting geográfico distinto (capitais em um, interior em outro) |

---

## Mapeamento HTML (export via `_export-html.md`)

| Bloco do output narrado | Componente do design system |
|---|---|
| Tabela demográfica (idade + gênero + classificação) | `.table` — coluna Classificação como badge colorido (verde/amarelo/vermelho/cinza) |
| Vencedor / Ponto cego / Buraco demográfico (3 destaques) | `.kpi-grid` com 3 `.kpi` — `.up` no Vencedor, `.down` no Buraco, `--neon` no Ponto cego |
| Alerta de divergência de público declarado vs. real | `.regra.alerta` com texto descritivo |
| Tabela geográfica (top 10 estados + coluna Decisão) | `.table` — linha "Excluir" em `.down` (rust), linha "Escalar" em `.up` (verde) |
| Top 3 estados mais baratos | `.kpi-grid` com 3 `.kpi` compactos |
| Capital vs. interior (dois valores comparativos) | `.kpi` duplo lado a lado com `.up`/`.down` conforme vencedor |
| Ponto cego demográfico | `.callout` com `--neon` no número da estimativa |
| Ponto cego geográfico | `.callout` com `--neon` no número da estimativa |
| Frase "No VTSD isso significa..." | `.callout` |
| Ação recomendada | `.pitch-box` |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no rodapé |
