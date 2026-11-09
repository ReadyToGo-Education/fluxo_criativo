# Output [4]. Geo & Demografia

Análise de quem está convertendo: faixa etária, gênero, estado e região do país. Revela se a Identidade do Consumidor declarada no perfil do produto bate com quem de fato compra.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- "Qual estado está me trazendo as conversões mais baratas?"
- "Tem região onde estou gastando muito e não vem resultado?"
- "Homens ou mulheres convertem mais nas minhas campanhas?"
- "Qual faixa etária é meu ponto cego: gasto pouco e poderia explorar?"
- "Em qual região do país meus anúncios performam melhor?"

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## Dados necessários

### O que já vem do Passo 4 do command principal

`level=account`, sem breakdowns. Campos base: `spend`, `impressions`, `clicks`, `ctr`, `actions`, `action_values`, `cost_per_action_type`.

Período: conforme escolha do aluno no Passo 3. Não perguntar novamente.

### Campos adicionais a acrescentar na chamada principal deste output

Nenhum campo adicional é necessário na chamada base. Todas as análises deste output dependem das chamadas com breakdowns abaixo. Os breakdowns de Geo & Demo exigem chamadas separadas: a API não permite combinar `age,gender` com `region` numa única requisição. Tampouco é possível cruzar geo + demo numa única chamada (ex: "mulheres 25-34 em SP"). Os pontos cegos demográfico e geográfico são calculados separadamente.

### Chamadas adicionais (executar antes de montar os blocos)

`{PERIOD_PARAM}` é o parâmetro de período da tabela do Passo 3 do command (`date_preset=last_Nd` ou, no customizado, o `time_range` já codificado). As três chamadas são no nível da conta, nos dois modos (`level=account` no App, `level: "ad_account"` no conector), e esse nível não aceita filtro de campanha. Com `ESCOPO_FILTRO` diferente de `conta_completa`, avisar o aluno que idade, gênero, região e país são da conta inteira, não do grupo escolhido. No conector, dá para tentar o recorte só do grupo com `level: "campaign"` e `filtering: [{field: "campaign.id", operator: "IN", value: [ids do escopo]}]` quando o schema da tool aceitar quebra nesse nível; se não aceitar, seguir com a conta inteira e o aviso.

**Chamada 4a. Demográfica (idade + gênero)**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights\
?fields=spend,impressions,clicks,actions,action_values,cost_per_action_type\
&breakdowns=age,gender\
&level=account\
&{PERIOD_PARAM}\
&limit=500\
&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

**Modo MCP_CONECTOR:** usar `mcp__*__ads_get_ad_entities` com `level: "ad_account"`, `breakdowns: ["age","gender"]`, o mesmo período (`date_preset` ou `time_range` em texto JSON), os campos `amount_spent`, `impressions`, `link_click`, `omni_purchase`, `offsite_conversion_fb_pixel_purchase_values` (ou `purchase_roas`) e `results` (leads), e `limit: 1000`. Antes, conferir que o recorte existe (no schema da tool ou em `ads_get_field_context`, como no contrato do conector, `trafego-insights/SKILL.md` §10.1). Se a tool recusar o recorte, avisar o aluno e seguir sem ele; nunca inventar.

---

**Chamada 4b. Geográfica por estado (region)**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights\
?fields=spend,impressions,clicks,actions,action_values,cost_per_action_type\
&breakdowns=region\
&level=account\
&{PERIOD_PARAM}\
&limit=500\
&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

**Modo MCP_CONECTOR:** usar `mcp__*__ads_get_ad_entities` com `level: "ad_account"`, `breakdowns: ["region"]`, o mesmo período (`date_preset` ou `time_range` em texto JSON), os campos `amount_spent`, `impressions`, `link_click`, `omni_purchase`, `offsite_conversion_fb_pixel_purchase_values` (ou `purchase_roas`) e `results` (leads), e `limit: 1000`. Antes, conferir que o recorte existe (no schema da tool ou em `ads_get_field_context`, como no contrato do conector, `trafego-insights/SKILL.md` §10.1). Se a tool recusar o recorte, avisar o aluno e seguir sem ele; nunca inventar.

---

**Chamada 4c. Por país (confirmação de cobertura)**

Usar somente se a conta tiver targeting para múltiplos países. Se o targeting for exclusivamente Brasil, esta chamada pode ser omitida.

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights\
?fields=spend,impressions,clicks,actions,action_values,cost_per_action_type\
&breakdowns=country\
&level=account\
&{PERIOD_PARAM}\
&limit=500\
&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

**Modo MCP_CONECTOR:** usar `mcp__*__ads_get_ad_entities` com `level: "ad_account"`, `breakdowns: ["country"]`, o mesmo período (`date_preset` ou `time_range` em texto JSON), os campos `amount_spent`, `impressions`, `link_click`, `omni_purchase`, `offsite_conversion_fb_pixel_purchase_values` (ou `purchase_roas`) e `results` (leads), e `limit: 1000`. Antes, conferir que o recorte existe (no schema da tool ou em `ads_get_field_context`, como no contrato do conector, `trafego-insights/SKILL.md` §10.1). Se a tool recusar o recorte, avisar o aluno e seguir sem ele; nunca inventar.

---

**Nota sobre granularidade geográfica:** o breakdown `region` da API retorna apenas o ESTADO, sem granularidade de cidade, portanto a divisão capital vs. interior NÃO é possível com o dado disponível (o breakdown `dma` é calibrado para o mercado americano e retorna dados pouco granulares no Brasil). A análise geográfica deste output trabalha por estado e, na Resposta 5, agrega os estados nas cinco regiões do país: Norte (Acre, Amapá, Amazonas, Pará, Rondônia, Roraima, Tocantins), Nordeste (Alagoas, Bahia, Ceará, Maranhão, Paraíba, Pernambuco, Piauí, Rio Grande do Norte, Sergipe), Centro-Oeste (Distrito Federal, Goiás, Mato Grosso, Mato Grosso do Sul), Sudeste (Espírito Santo, Minas Gerais, Rio de Janeiro, São Paulo) e Sul (Paraná, Rio Grande do Sul, Santa Catarina).

### Referência de produto

Ler do `resumo-produto.md` (já carregado no Passo 0.1 do `SKILL.md`). Não perguntar de novo:
- Preço e tipo de produto → benchmark de CPA/CPL conforme tabela do output [1]
- Público-alvo declarado (sexo, faixa etária, região) → comparar com o que a API retornar
- Identidade do Consumidor do produto → enriquece a comparação entre público declarado e público real. Para o detalhe (baldes de "Para quem é"), ler só a seção indicada na tabela "Onde está o detalhe completo" do resumo.
- Se o resumo não trouxer sexo, faixa etária ou região do público, perguntar só o que faltar (uma pergunta por mensagem).
- Inferir tipo de funil pelo objetivo predominante das campanhas: `OUTCOME_SALES` = venda direta (métrica-norte: CPA + ROAS); `OUTCOME_LEADS` = captação (métrica-norte: CPL)

---

## Fórmulas de cálculo (obrigatório aplicar antes de montar os blocos)

Aplicar por linha de cada breakdown:

| Métrica | Fórmula | Tipo canônico |
|---|---|---|
| CPA | `spend` / `purchases` | `offsite_conversion.fb_pixel_purchase` |
| CPL | `spend` / `leads` | `lead` (total); sem ele, `offsite_conversion.fb_pixel_lead`; nunca a soma (regra de leads do command) |
| ROAS | `action_values[offsite_conversion.fb_pixel_purchase]` / `spend` | `offsite_conversion.fb_pixel_purchase` |
| CTR | `clicks` / `impressions` | - |

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

### Resposta 1. "Qual estado está me trazendo as conversões mais baratas?"

Dados vêm da Chamada 4b. Mostrar top 10 estados por spend, ordenados por CPA ou CPL crescente para identificar os vencedores geográficos.

#### Template A. Venda direta:

```
🗺️  POR ESTADO  ·  {período}  ·  Top 10 por spend

  Estado   Spend      CPA        ROAS    Conv.   % do total   Decisão
  ────────────────────────────────────────────────────────────────────
  SP       R$ {X}     R$ {Y}     {Z}x    {N}     {P%}         ✅ Manter
  RJ       R$ {X}     R$ {Y}     {Z}x    {N}     {P%}         📈 Escalar
  MG       R$ {X}     R$ {Y}     {Z}x    {N}     {P%}         🟡 Revisar
  BA       R$ {X}     ∞          -       0       {P%}         🛑 Excluir

  Top 3 por CPA mais barato:  {estado 1}, {estado 2}, {estado 3}
  Candidatos a excluir:       {estados com spend > 5% do total e CPA > 150% do benchmark}
```

#### Template B. Captação de leads:

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
| Excluir | CPA ou CPL > 150% do benchmark E spend > 5% do total, ou spend > 2% com 0 conversões |

Se a conta tiver targeting nacional sem exclusões e houver 3 ou mais estados com decisão "Escalar", sugerir criar adsets separados para esses estados vencedores.

---

### Resposta 2. "Tem região onde estou gastando muito e não vem resultado?"

Usar os mesmos dados da Chamada 4b e da tabela gerada na Resposta 1. Destacar os estados com coluna Decisão "Excluir": spend alto sem retorno equivalente.

Critério de destaque: `CPA ou CPL > 150% do benchmark E spend > 5% do total`, ou `spend > 2% do total com 0 conversões`.

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

#### Template A. Venda direta (OUTCOME_SALES)

```
👥 DEMOGRAFIA  ·  {nome_conta}  ·  {período}

  Idade   Gênero   Spend      CPA        ROAS    Conv.   Classificação
  ────────────────────────────────────────────────────────────────────
  25-34   F        R$ {X}     R$ {Y}     {Z}x    {N}     ✅ Vencedor
  35-44   F        R$ {X}     R$ {Y}     {Z}x    {N}     ✅ Saudável
  25-34   M        R$ {X}     R$ {Y}     {Z}x    {N}     🟡 Atenção
  45-54   M        R$ {X}     R$ {Y}     ∞       0       🔴 Queimando
  18-24   F        R$ {X}     R$ {Y}     {Z}x    {N}     🔍 Ponto cego

  Vencedor:    {faixa etária + gênero}, CPA R$ {X}, {Y%} abaixo do benchmark (R$ {benchmark})
  Ponto cego:  {faixa etária + gênero}, gasto R$ {X} ({P%} do total), CPA R$ {Y} (saudável)
  Buraco:      {faixa etária + gênero}, R$ {X} gastos, {N} conversões, CPA {Y%} acima do benchmark
```

#### Template B. Captação de leads (OUTCOME_LEADS)

```
👥 DEMOGRAFIA  ·  {nome_conta}  ·  {período}

  Idade   Gênero   Spend      CPL        Leads   Classificação
  ────────────────────────────────────────────────────────────
  25-34   F        R$ {X}     R$ {Y}     {N}     ✅ Vencedor
  35-44   F        R$ {X}     R$ {Y}     {N}     ✅ Saudável
  25-34   M        R$ {X}     R$ {Y}     {N}     🟡 Atenção
  45-54   M        R$ {X}     ∞          0       🔴 Queimando
  18-24   F        R$ {X}     R$ {Y}     {N}     🔍 Ponto cego

  Vencedor:    {faixa etária + gênero}, CPL R$ {X}, {Y%} abaixo do benchmark (R$ {benchmark})
  Ponto cego:  {faixa etária + gênero}, gasto R$ {X} ({P%} do total), CPL R$ {Y} (saudável)
  Buraco:      {faixa etária + gênero}, R$ {X} gastos, {N} leads, CPL {Y%} acima do benchmark
```

Ordenar por `spend` decrescente. Mostrar todas as linhas com spend > 0. Omitir linhas sem impressões.

Após a tabela, consolidar por gênero (agregar todas as faixas etárias de cada gênero) para responder diretamente à pergunta:

```
  Resumo por gênero:
  Feminino    Spend total: R$ {X}   CPA médio: R$ {Y}   Conv. total: {N}
  Masculino   Spend total: R$ {X}   CPA médio: R$ {Y}   Conv. total: {N}

  Gênero vencedor: {F | M}, CPA {X%} mais barato
```

**Comparação com perfil declarado:** após o resumo por gênero, cruzar com o público-alvo do `resumo-produto.md`. Se o vencedor real divergir do perfil declarado, sinalizar explicitamente:

```
⚠️  DIVERGÊNCIA DE PÚBLICO
    Perfil declarado:  {sexo + faixa etária declarados no resumo-produto.md}
    Quem está {comprando | convertendo} de fato: {sexo + faixa etária vencedores}
    Leitura: ou a Identidade do Consumidor precisa ser atualizada, ou há um segmento
    novo que o produto alcançou sem intenção. Nos dois casos, vale investigar.
```

---

### Resposta 4. "Qual faixa etária é meu ponto cego: gasto pouco e poderia explorar?"

Dados vêm da Chamada 4a. Identificar clusters demográficos (faixa etária + gênero) que atendam os três critérios de ponto cego:

**Critério para ponto cego demográfico:**
- Spend < 5% do total do período
- CPA ou CPL ≤ 110% do benchmark do produto
- Mínimo de 3 conversões ou leads (sinal não-trivial)

#### Template A. Venda direta:

```
🔍 PONTO CEGO DEMOGRÁFICO

  Cluster:        {faixa etária} {gênero}
  Gasto atual:    R$ {X}  ({P%} do total)
  CPA atual:      R$ {Y}  ({Z%} do benchmark, saudável)
  Conversões:     {N}
  Estimativa:     se receber 10% do budget total (R$ {10%_do_spend_total}),
                  projeção de {floor(R$_10pct / CPA_atual)} compras adicionais no período.
  Ação: criar adset segmentado para este perfil via "trafego-publicos" + validar via "trafego-testes"
```

#### Template B. Captação de leads:

```
🔍 PONTO CEGO DEMOGRÁFICO

  Cluster:        {faixa etária} {gênero}
  Gasto atual:    R$ {X}  ({P%} do total)
  CPL atual:      R$ {Y}  ({Z%} do benchmark, saudável)
  Leads:          {N}
  Estimativa:     se receber 10% do budget total (R$ {10%_do_spend_total}),
                  projeção de {floor(R$_10pct / CPL_atual)} leads adicionais no período.
  Ação: criar adset segmentado para este perfil via "trafego-publicos" + validar via "trafego-testes"
```

**Fórmula da estimativa (obrigatório usar):**

```
budget_hipotetico = spend_total_periodo * 0.10
estimativa_adicional = floor(budget_hipotetico / CPA_ou_CPL_atual_do_cluster)
```

Nunca apresentar estimativa sem mostrar o raciocínio (`R$ {budget_hipotetico} / R$ {CPA_atual} = {N}`).

Se nenhum cluster demográfico atender os 3 critérios: informar "Nenhum ponto cego demográfico identificado com dados suficientes no período. Mínimo necessário: 3 conversões com spend < 5% do total e CPA dentro do benchmark."

---

### Resposta 5. "Em qual região do país meus anúncios performam melhor?"

Agregar os dados da Chamada 4b por região do país (Norte, Nordeste, Centro-Oeste, Sudeste, Sul), usando o mapa estado → região da nota sobre granularidade geográfica: somar spend, conversões/leads e calcular CPA/CPL de cada região. O breakdown `region` retorna apenas estado, sem granularidade de cidade: por isso a comparação é entre regiões do país, e não capital vs. interior.

#### Template A. Venda direta:

```
🧭  REGIÕES DO PAÍS  ·  {período}

  Região         Spend      CPA        ROAS    Conv.   % do gasto
  ────────────────────────────────────────────────────────────────
  Sudeste        R$ {X}     R$ {Y}     {Z}x    {N}     {P%}
  Nordeste       R$ {X}     R$ {Y}     {Z}x    {N}     {P%}
  Sul            R$ {X}     R$ {Y}     {Z}x    {N}     {P%}
  Centro-Oeste   R$ {X}     R$ {Y}     {Z}x    {N}     {P%}
  Norte          R$ {X}     R$ {Y}     {Z}x    {N}     {P%}

  Vencedora: {região}, CPA {X%} mais barato que a média da conta
  Leitura: {interpretação concreta, ex: "Nordeste converte 28% mais barato mas recebe apenas 18%
            do budget. Rebalancear o gasto geográfico pode reduzir o CPA médio da conta."}
```

#### Template B. Captação de leads:

```
🧭  REGIÕES DO PAÍS  ·  {período}

  Região         Spend      CPL        Leads   % do gasto
  ────────────────────────────────────────────────────────
  Sudeste        R$ {X}     R$ {Y}     {N}     {P%}
  Nordeste       R$ {X}     R$ {Y}     {N}     {P%}
  Sul            R$ {X}     R$ {Y}     {N}     {P%}
  Centro-Oeste   R$ {X}     R$ {Y}     {N}     {P%}
  Norte          R$ {X}     R$ {Y}     {N}     {P%}

  Vencedora: {região}, CPL {X%} mais barato que a média da conta
  Leitura: {interpretação concreta, ex: "Nordeste gera leads 22% mais baratos mas recebe apenas
            20% do budget. Criar adsets geográficos separados pode otimizar o CPL médio."}
```

Ordenar por `spend` decrescente. Omitir regiões sem impressões no período.

Se a diferença de CPA ou CPL entre a melhor e a pior região (entre as que têm conversões) for menor que 15%: informar "Diferença de {X%}, abaixo do limiar de 15%. Targeting nacional é adequado para este produto no período analisado."

---

### Análise adicional. Ponto cego geográfico

A API não permite cruzar faixa etária + gênero + estado numa única chamada. O ponto cego geográfico é calculado separadamente a partir da Chamada 4b e reportado aqui como análise complementar.

**Critério para ponto cego geográfico:**
- Spend < 5% do total do período
- CPA ou CPL ≤ 110% do benchmark do produto
- Mínimo de 3 conversões ou leads (sinal não-trivial)

#### Template A. Venda direta:

```
🔍 PONTO CEGO GEOGRÁFICO

  Estado/região:  {nome do estado}
  Gasto atual:    R$ {X}  ({P%} do total)
  CPA atual:      R$ {Y}  ({Z%} do benchmark, saudável)
  Conversões:     {N}
  Estimativa:     se receber 10% do budget total (R$ {10%_do_spend_total}),
                  projeção de {floor(R$_10pct / CPA_atual)} compras adicionais no período.
  Ação: criar adset com targeting geográfico isolado via "trafego-testes", duplicar campanha winner
        restringindo a este estado
```

#### Template B. Captação de leads:

```
🔍 PONTO CEGO GEOGRÁFICO

  Estado/região:  {nome do estado}
  Gasto atual:    R$ {X}  ({P%} do total)
  CPL atual:      R$ {Y}  ({Z%} do benchmark, saudável)
  Leads:          {N}
  Estimativa:     se receber 10% do budget total (R$ {10%_do_spend_total}),
                  projeção de {floor(R$_10pct / CPL_atual)} leads adicionais no período.
  Ação: criar adset com targeting geográfico isolado via "trafego-testes", duplicar campanha winner
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

### Passo 0. Checklist antes de montar qualquer bloco

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

[ ] Em qual região do país os anúncios performam melhor?
    → coberto? Se não: agregar os estados nas cinco regiões do país e comparar o CPA médio de cada região
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico**: vencedor demográfico (faixa etária + gênero), vencedor geográfico (estado), resultado da comparação entre regiões do país, e os pontos cegos identificados (se existirem).
2. **Causa provável**: por que esse cluster converte: alinhamento com a Identidade do Consumidor do produto, poder de compra da região, comportamento de consumo da faixa etária. Informar se é descoberta esperada (confirma o perfil declarado) ou surpresa (diverge do perfil declarado).
3. **No VTSD, isso significa…**: relacionar os achados com o método. Exemplos:
   - "Você desenhou a Identidade do Consumidor para mulheres 35-44, mas os dados mostram homens 45-54 como vencedores. Ou a Identidade está desalinhada com a realidade, ou há um público novo que o produto alcançou sem intenção. Nos dois casos, vale revisar o perfil ou criar uma linha de comunicação específica para esse cluster."
   - "Nordeste convertendo 30% mais barato que o Sudeste com 80% menos budget: a Urgência Oculta do produto ressoa mais forte nessa região, oportunidade clara de rebalancear o gasto geográfico."
   - "Faixa 45-54 com CPA 40% abaixo do benchmark mas apenas 3% do gasto: o Quadro do produto resolve um problema que essa faixa sente com mais intensidade. Falta orçamento alocado para ela."
4. **Ação recomendada**: 1 a 3 ações concretas com handoff para a skill executora.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Cluster demográfico vencedor com gasto < 10% do total | "trafego-publicos": criar Saved Audience segmentada para o cluster + "trafego-testes", adset isolado para validar em escala |
| Estado com gasto > 5% e CPA ou CPL > 150% do benchmark | "trafego-otimizar": excluir região via ajuste de targeting no adset |
| Ponto cego demográfico identificado | "trafego-testes": duplicar adset winner com segmentação de faixa etária + gênero isolados |
| Ponto cego geográfico identificado | "trafego-testes": duplicar adset winner com targeting geográfico restrito ao estado |
| Vencedor real difere do público declarado no perfil | "produto-concepcao": revisar Identidade do Consumidor com os dados reais da API |
| Regiões do país com diferença > 30% de CPA ou CPL entre si | "trafego-testes": criar adsets separados com targeting geográfico distinto (uma região em cada) |

---

## Mapeamento HTML (export via `_export-html.md`)

Componentes definidos na seção 3.2 do `_export-html.md`. **Usar exatamente estes nomes de classe.** O vocabulário antigo (`.kpi-grid`, `.kpi`, `.table`, `.regra`, `.callout`, `.pitch-box`, `.up`, `.down`, `--neon`) foi descontinuado e NÃO existe no CSS embutido: usá-lo gera seção sem estilo.

| Bloco do output narrado | Componente do design system |
|---|---|
| KPIs globais (gasto, vendas/leads, CPA/CPL, gênero vencedor, região líder) | `.stats-grid` com um `.stat-card` por métrica (`.value.green/.yellow/.red`) |
| Cada "Resposta N" obrigatória | `.section` com `.section-header` (`.section-num` + `.section-title` + `.section-question`) |
| Tabela demográfica (idade + gênero + classificação) | `.card` + `table`; `.num` nas colunas numéricas; coluna Classificação colorida com `style="color:var(--green/--yellow/--red/--text-muted)"` |
| Vencedor / Ponto cego / Buraco demográfico (3 destaques) | `.stats-grid` com 3 `.stat-card` (`.value.green` no Vencedor, `.value.red` no Buraco, `.value.yellow` no Ponto cego) |
| Alerta de divergência de público declarado vs. real | `.diag-box.yellow` (ou `.red`) com texto descritivo |
| Tabela geográfica (top 10 estados + coluna Decisão) | `.card` + `table`; linha "Excluir" com `style="color:var(--red)"`, linha "Escalar" com `var(--green)` |
| Top 3 estados mais baratos | `.stats-grid` com 3 `.stat-card` compactos |
| Comparativo de regiões do país (melhor vs. pior) | `.card` + `.fmt-compare` com 2 `.fmt-box` (região vencedora / região mais cara), métrica-norte em `.fmt-metric` |
| Ponto cego demográfico / geográfico (estimativa) | `.diag-box` (azul) com a fórmula e a estimativa em `<strong>` |
| Frase "No VTSD isso significa..." | `.diag-box` (azul padrão) |
| Ação recomendada | `.action-box` (com `<ol>`/`<li>` se houver passos) |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no `.page-foot` |

### Gráficos obrigatórios deste output

Renderizar todos os gráficos abaixo que tiverem dado real, logo após o `.stats-grid` de KPIs, sob um `.section-h` "Visão visual". Todos em SVG/CSS inline, sem dependência (receitas na seção **3.2.1** e **3.2.1.1** do `_export-html.md`). As fontes vêm das chamadas com breakdown (4a `age,gender` e 4b `region`, separadas: a API não combina). Se um breakdown não retornar, **omitir só o gráfico que dele depende** e seguir com os demais: nunca inventar número.

> ⚠️ **Limitação de dado confirmada em conta real:** o breakdown `region` (4b) **NÃO retorna `offsite_conversion.fb_pixel_purchase`**: só engajamento, cliques e `link_click`. Além disso `region` = **estado** (não cidade), então não há granularidade de capital. Portanto: (a) o gráfico geográfico é por **investimento + eficiência de clique**, não por venda; (b) a leitura por **vendas** é confiável apenas no breakdown **demográfico** (`age,gender`, 4a), que retorna as compras corretamente. Antes de montar "vendeu vs queimou por estado", checar se `actions` da 4b traz o tipo de compra; se não trouxer (caso comum), usar o gráfico de eficiência de clique e avisar no HTML.

| Gráfico | Componente / receita | Fonte de dado | Posição |
|---|---|---|---|
| CPA por faixa etária | SVG `vbars` (receita G, via helper) | Chamada 4a por `age` (soma gêneros): CPA por faixa (vendas reais) | `.charts-grid`, 1ª coluna |
| Gênero · CPA e ROAS | `.wow-chart` (receita C) | Chamada 4a por `gender`: CPA/ROAS masculino × feminino (vendas reais) | `.charts-grid`, 2ª coluna |
| Investimento por estado · eficiência de clique | `.hbar-row` (receita D) | Chamada 4b (`region`): top estados por spend; cor = custo por `link_click` abaixo (`.win`) ou acima (`.burn`) da mediana | `.chart-card` full-width |
| Estados: venderam vs. queimaram (SÓ se 4b trouxer compras) | `.hbar-row` (receita D) | Chamada 4b: `.win` para estados que converteram, `.burn` para spend alto sem venda | substitui o gráfico de eficiência quando o dado de venda existir |

Regras dos gráficos: usar só cores da paleta. **CPA por faixa etária (receita G, helper `vbars`):** gravar o spec `{"bars":[{"label":"25-34","value":<CPA>,"color":<verde ≤ R$ X · amarelo · vermelho>}]}` com o Write em `{RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/tmp/spec-vbars.json` (caminho absoluto) e rodar `{PY} "{RAIZ_PROJETO}/.claude/skills/trafego-analise/scripts/trafego_chart_geom.py" vbars < "{RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/tmp/spec-vbars.json"` (`{PY}` = interpretador detectado na sessão; regra do spec na seção 3.2.1.2 do `_export-html.md`); colar `bars[]` como `<rect>` + `<text>`; faixa sem conversão (CPA `∞`) é omitida. **Gênero (receita C):** par masculino × feminino; menor CPA / maior ROAS recebe `.good` (verde). **Estados (receita D):** largura proporcional ao spend; cor pela eficiência de clique (mediana) quando não houver venda por região, ou por conversão (`.win`/`.burn`) quando houver. Sempre que a leitura geográfica for por clique e não por venda, deixar isso explícito num `.funnel-meta`.
