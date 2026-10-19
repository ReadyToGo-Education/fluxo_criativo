---
name: trafego-analise/comparativo
description: Confronta duas campanhas Meta Ads lado a lado, calculando métricas derivadas VTSD (connect rate, hook rate, hold rate, play-through rate, CPA/CPL, custo por etapa do funil) e entregando diagnóstico de qual vence em cada dimensão, qual gargalo a perdedora tem e qual das duas escalar.
---

# Output [10]. Comparativo A x B

Confronta duas campanhas do mesmo período, calculando métricas derivadas para cada uma e identificando qual vence em cada dimensão do funil VTSD. Útil para decidir qual escalar, qual pausar e entender qual elemento do método está fazendo a diferença.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- "Qual das duas campanhas tem melhor CPA ou CPL no período?"
- "Onde está a diferença principal entre A e B no funil?"
- "Em qual etapa a campanha perdedora está travando?"
- "A diferença de resultado é por causa do criativo (hook/hold) ou da página (connect rate)?"
- "Qual campanha devo escalar e qual devo pausar ou revisar?"
- "Como as métricas de vídeo (hook, hold, play-through) diferem entre A e B?"
- "Tem fadiga em alguma das duas? Frequência alta, CTR caindo?"

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## Dados necessários

### O que já vem do Passo 4 do command principal

`level=campaign`, campos base: `spend`, `impressions`, `clicks`, `ctr`, `cpm`, `cpc`, `reach`, `frequency`, `actions`, `action_values`, `cost_per_action_type`, métricas de vídeo (`video_p25_watched_actions`, `video_p50_watched_actions`, `video_p75_watched_actions`, `video_p95_watched_actions`).

Período: conforme escolha do aluno no Passo 3. Não perguntar novamente.

### Campos adicionais

Acrescentar na chamada de cada campanha:

```
outbound_clicks,
unique_clicks,unique_link_clicks_ctr
```

> **Nota de API:** `landing_page_views` é inválido no parâmetro `fields` da Insights API (erro 400). O valor de visualizações da página de destino vem do array `actions` (action_type = `landing_page_view`), já retornado nos campos base. Usar esse valor nas fórmulas que citam `landing_page_views` (Connect Rate, Lead Rate, Custo por LP View etc.).

### Chamadas adicionais (curl exato)

Fazer **duas chamadas separadas**, uma por campanha. Se o aluno informou nomes em vez de IDs, fazer primeiro a chamada de listagem abaixo para resolver os IDs.

**Chamada 10a. Listagem de campanhas (só se o aluno informou nomes)**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/campaigns
  ?fields=id,name,status,objective
  &filtering=[{\"field\":\"effective_status\",\"operator\":\"IN\",\"value\":[\"ACTIVE\",\"PAUSED\"]}]
  &limit=100
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

Exibir lista numerada, pedir confirmação do match de nome para cada campanha, depois prosseguir com os IDs confirmados.

**Modo MCP_CONECTOR:** usar `mcp__*__ads_get_ad_entities` com `entity_type=campaign` para obter IDs.

**Chamada 10b. Insights da Campanha A**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/{CAMPAIGN_A_ID}/insights
  ?fields=campaign_id,campaign_name,spend,impressions,reach,frequency,clicks,ctr,cpm,cpc,
    outbound_clicks,unique_clicks,unique_link_clicks_ctr,
    actions,action_values,cost_per_action_type,
    video_p25_watched_actions,video_p50_watched_actions,
    video_p75_watched_actions,video_p95_watched_actions
  &level=campaign
  &{PERIOD_PARAM}
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Chamada 10c. Insights da Campanha B** (mesma estrutura, trocando o ID)

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/{CAMPAIGN_B_ID}/insights
  ?fields=campaign_id,campaign_name,spend,impressions,reach,frequency,clicks,ctr,cpm,cpc,
    outbound_clicks,unique_clicks,unique_link_clicks_ctr,
    actions,action_values,cost_per_action_type,
    video_p25_watched_actions,video_p50_watched_actions,
    video_p75_watched_actions,video_p95_watched_actions
  &level=campaign
  &{PERIOD_PARAM}
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

`{PERIOD_PARAM}` = mesmo parâmetro de período já definido no Passo 3 do command principal (`date_preset=last_7d` OU `since=YYYY-MM-DD&until=YYYY-MM-DD`).

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com o `campaign_id` de cada campanha separadamente, mesmo período do Passo 3.

### Referência de produto

Ler do `resumo-produto.md` (já carregado no Passo 0.1 do `SKILL.md`) o preço e o tipo de produto. Não perguntar de novo. Inferir tipo de funil pelo objetivo das campanhas informadas:

- `OUTCOME_SALES` → funil de venda direta → métrica-norte = **CPA** (e ROAS se pixel de compra ativo)
- `OUTCOME_LEADS` → funil de captação → métrica-norte = **CPL**

Se as duas campanhas tiverem objetivos diferentes, alertar que comparação direta de CPA vs. CPL não é válida e adaptar o veredicto (comparar cada uma contra seu próprio benchmark).

| Tipo de funil | Ticket | CPA máximo saudável | ROAS mínimo saudável |
|---|---|---|---|
| Venda direta: low ticket | até R$ 97 | ticket x 0,40 | 2,5x |
| Venda direta: ticket médio | R$ 98 a R$ 497 | ticket x 0,30 | 3,0x |
| Venda direta: high ticket | acima de R$ 497 | ticket x 0,25 | 4,0x |
| Captação de leads | qualquer | CPL-alvo: ler do resumo ou perguntar | - |

---

## Fórmulas de cálculo

Calcular para cada campanha **antes** de montar a tabela. Para denominadores zero ou campos ausentes: marcar `-` na tabela (nunca inventar).

| Métrica derivada | Fórmula | Elemento VTSD |
|---|---|---|
| Hook Rate | `video_p25_watched_actions` / `impressions` | Urgência Oculta |
| CTR (link) | `clicks` / `impressions` | Identidade do Produto |
| Connect Rate | `landing_page_views` / `clicks` | Quadro na Parede |
| Hold Rate | `video_p50_watched_actions` / `video_p25_watched_actions` | Decorados |
| Play-Through Rate | `video_p95_watched_actions` / `impressions` | Furadeira |
| Checkout Rate | `offsite_conversion.fb_pixel_initiate_checkout` / `landing_page_views` | Oferta (só OUTCOME_SALES) |
| Conversion Rate | `offsite_conversion.fb_pixel_purchase` / `offsite_conversion.fb_pixel_initiate_checkout` | Furadeira + Decorados (só OUTCOME_SALES) |
| Lead Rate | `offsite_conversion.fb_pixel_lead` / `landing_page_views` | Isca Digital (só OUTCOME_LEADS) |
| CPA | `spend` / `offsite_conversion.fb_pixel_purchase` | (métrica-norte SALES) |
| CPL | `spend` / `offsite_conversion.fb_pixel_lead` | (métrica-norte LEADS) |
| Custo por LP View | `spend` / `landing_page_views` | Connect (custo) |
| ROAS | `action_values[offsite_conversion.fb_pixel_purchase]` / `spend` | (só OUTCOME_SALES) |

**Regra de deduplicação obrigatória:** o campo `actions` da API retorna múltiplos `action_type` que representam o mesmo evento. Usar APENAS o tipo canônico para evitar dupla contagem:

- Compras: `offsite_conversion.fb_pixel_purchase`
- Leads: `offsite_conversion.fb_pixel_lead`
- Checkouts iniciados: `offsite_conversion.fb_pixel_initiate_checkout`
- Add to cart: `offsite_conversion.fb_pixel_add_to_cart`

Se o tipo canônico retornar zero e outro tipo tiver valor, usar o que tiver dado e registrar qual foi usado na narrativa.

**Diferença percentual entre A e B:** `abs(A - B) / max(A, B) * 100`. Usar esse cálculo para identificar a métrica com maior divergência no Bloco 3.

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "Qual das duas campanhas tem melhor CPA ou CPL no período?"

Calcular CPA ou CPL de cada campanha (conforme o objetivo: `OUTCOME_SALES` → CPA, `OUTCOME_LEADS` → CPL). Apresentar lado a lado com delta percentual e veredicto de qual vence na métrica-norte.

Usar o template correspondente ao tipo de funil (A = venda direta, B = captação de leads). Antes de exibir qualquer número, confirmar as campanhas que serão comparadas:

```
Comparando:

Campanha A: {nome_A}  (ID: {ID_A})
Campanha B: {nome_B}  (ID: {ID_B})
Período: {período}
Tipo de funil: {Venda direta | Captação de leads}
Métrica-norte: {CPA | CPL}
```

Se os objetivos das duas campanhas forem diferentes, alertar aqui antes de prosseguir.

Calcular todas as métricas derivadas antes de montar a tabela. Mostrar o vencedor em cada linha conforme a regra: menor é melhor em custo (CPA, CPL, CPM, Custo por LP View), maior é melhor nas demais.

#### Template A. Venda direta (OUTCOME_SALES)

```
COMPARATIVO A x B
Período: {período}  |  Conta: {nome_conta}

                              A                    B
                         {nome_A}             {nome_B}
─────────────────────────────────────────────────────────────
INVESTIMENTO
  Gasto total            R$ {valor}           R$ {valor}

ALCANCE
  Impressões             {N}                  {N}
  Frequência             {X,X}                {X,X}       {<- A | <- B | aprox.}
  CPM                    R$ {valor}           R$ {valor}  {vencedora}

ENGAJAMENTO
  CTR (link)             {X,XX%}              {X,XX%}     {vencedora}
  Hook Rate              {X,XX%}              {X,XX%}     {vencedora}
  Hold Rate              {X,XX%}              {X,XX%}     {vencedora}
  Play-Through           {X,XX%}              {X,XX%}     {vencedora}

FUNIL
  Cliques no link        {N}                  {N}
  Connect Rate           {X,XX%}              {X,XX%}     {vencedora}
  LP Views               {N}                  {N}
  Checkout Rate          {X,XX%}              {X,XX%}     {vencedora}
  Checkouts iniciados    {N}                  {N}
  Conversion Rate        {X,XX%}              {X,XX%}     {vencedora}
  Compras                {N}                  {N}

EFICIÊNCIA
  ROAS                   {X,X}x               {X,X}x      {vencedora}
  CPA                    R$ {valor}           R$ {valor}  {vencedora}
  Custo por LP View      R$ {valor}           R$ {valor}  {vencedora}
─────────────────────────────────────────────────────────────

VENCEDORA NA MÉTRICA-NORTE: {A | B}
   CPA: R$ {melhor} vs R$ {pior} ({X% de diferença})
   ROAS: {melhor}x vs {pior}x
```

#### Template B. Captação de leads (OUTCOME_LEADS)

```
COMPARATIVO A x B
Período: {período}  |  Conta: {nome_conta}

                              A                    B
                         {nome_A}             {nome_B}
─────────────────────────────────────────────────────────────
INVESTIMENTO
  Gasto total            R$ {valor}           R$ {valor}

ALCANCE
  Impressões             {N}                  {N}
  Frequência             {X,X}                {X,X}       {vencedora}
  CPM                    R$ {valor}           R$ {valor}  {vencedora}

ENGAJAMENTO
  CTR (link)             {X,XX%}              {X,XX%}     {vencedora}
  Hook Rate              {X,XX%}              {X,XX%}     {vencedora}
  Hold Rate              {X,XX%}              {X,XX%}     {vencedora}
  Play-Through           {X,XX%}              {X,XX%}     {vencedora}

FUNIL
  Cliques no link        {N}                  {N}
  Connect Rate           {X,XX%}              {X,XX%}     {vencedora}
  LP Views               {N}                  {N}
  Lead Rate              {X,XX%}              {X,XX%}     {vencedora}
  Leads                  {N}                  {N}

EFICIÊNCIA
  CPL                    R$ {valor}           R$ {valor}  {vencedora}
  Custo por LP View      R$ {valor}           R$ {valor}  {vencedora}
─────────────────────────────────────────────────────────────

VENCEDORA NA MÉTRICA-NORTE: {A | B}
   CPL: R$ {melhor} vs R$ {pior} ({X% de diferença})
```

**Marcação de vencedora:** `<- A` ou `<- B` na coluna da direita. Se a diferença for menor que 5%, marcar `aprox.` (empate técnico).

**Linhas de LP View:** omitir Connect Rate, Checkout Rate e Lead Rate se `landing_page_views` não retornar para nenhuma das campanhas. Alertar: "LP views não rastreado. Conecte o evento no pixel via 'trafego-pixel' para ver o funil completo."

---

### Resposta 2. "Onde está a diferença principal entre A e B no funil?"

Identificar a métrica com maior divergência percentual entre A e B (fórmula: `abs(A - B) / max(A, B) * 100`). Nomear o elemento VTSD correspondente.

```
A maior diferença está em {nome_métrica}: A em {X%} vs B em {X%} ({N% de diferença}).

No VTSD, isso indica que {campanha_vencedora} está com {elemento_VTSD}
mais alinhado ao público. {Explicação em 2 linhas do que isso significa na prática.}
```

| Métrica com maior diferença | Elemento VTSD | O que reescrever |
|---|---|---|
| Hook Rate | Urgência Oculta | O ângulo de dor do primeiro segundo não ativa o público-alvo |
| CTR (link) | Identidade do Produto | O diferencial do produto não está claro na headline ou copy do anúncio |
| Connect Rate | Quadro na Parede | O que o anúncio promete é diferente do que a página entrega |
| Hold Rate | Decorados | Os benefícios apresentados no meio do vídeo não sustentam o interesse |
| Play-Through Rate | Furadeira | O método não está claro o suficiente para o espectador terminar o vídeo |
| Checkout Rate | Oferta | Preço, garantia ou stack de valor não convencem quem chegou na página |
| Conversion Rate | Furadeira + Decorados | O checkout não reforça o método e os benefícios o suficiente |
| Lead Rate | Isca Digital | A oferta de captura não é suficientemente atraente |
| CPM | Leilão | Uma das campanhas está pagando mais caro por atenção: pode ser criativo fadigado ou público mais concorrido |
| Frequência | Fadiga | Uma das campanhas está saturando o mesmo público |

Complementar com a relação entre as métricas do funil para precisar onde o volume é perdido (ex: "A venceu em CTR mas B venceu em Connect Rate: o criativo de A atrai mais cliques, mas a página de B converte melhor quem chega"). Indicar o elemento VTSD em jogo.

---

### Resposta 3. "Em qual etapa a campanha perdedora está travando?"

Identificar a etapa do funil onde a campanha com pior CPA/CPL perde mais volume em relação à vencedora. Usar os benchmarks abaixo para classificar se o valor está abaixo do esperado.

```
O gargalo principal de {campanha_perdedora} está em {etapa_do_funil}.
{Métrica} de {X%} está abaixo do padrão saudável (benchmark: {faixa saudável}).

No VTSD, isso aponta para {elemento}: {ação específica para corrigir}.
```

**Benchmarks para classificar gargalo:**

| Métrica | Abaixo do esperado | Saudável | Excelente |
|---|---|---|---|
| Hook Rate | < 15% | 15% a 30% | > 30% |
| CTR (link) | < 1% | 1% a 3% | > 3% |
| Connect Rate | < 50% | 50% a 70% | > 70% |
| Hold Rate | < 40% | 40% a 60% | > 60% |
| Play-Through Rate | < 5% | 5% a 15% | > 15% |
| Checkout Rate | < 5% | 5% a 12% | > 12% |
| Conversion Rate | < 20% | 20% a 35% | > 35% |
| Lead Rate | < 5% | 5% a 15% | > 15% |
| Frequência | > 4 (sinal de fadiga) | 2 a 4 | < 2 |

---

### Resposta 4. "A diferença de resultado é por causa do criativo (hook/hold) ou da página (connect rate)?"

Comparar diretamente Hook Rate e Hold Rate (criativo) versus Connect Rate (página) das duas campanhas:

- Se Hook Rate ou Hold Rate de A supera B com diferença percentual maior, o problema está no **criativo** da campanha perdedora. Elemento VTSD: Urgência Oculta (hook) ou Decorados (hold).
- Se Connect Rate de A supera B com diferença percentual maior (enquanto CTR é parecido), o problema está na **página** da campanha perdedora. Elemento VTSD: Quadro na Parede (promessa do anúncio não bate com a página).
- Se ambas as diferenças forem expressivas, nomear qual é maior e indicar a prioridade de correção.

```
Criativo (Hook Rate): A em {X%} vs B em {X%}, diferença de {N%}
Criativo (Hold Rate): A em {X%} vs B em {X%}, diferença de {N%}
Página (Connect Rate): A em {X%} vs B em {X%}, diferença de {N%}

O fator dominante é {criativo | página}: {explicação em 1 linha do que fazer}.
```

**Linhas de vídeo:** omitir Hook Rate e Hold Rate se nenhuma das campanhas tiver vídeo. Registrar na narrativa: "Sem criativo de vídeo, métricas de retenção não disponíveis. Usar CTR como proxy de atenção do criativo."

**Formatos assimétricos (vídeo vs. estático):** se apenas uma das campanhas tiver `video_p25_watched_actions > 0`, omitir a comparação de Hook Rate e Hold Rate e adicionar:

```
Nota: Hook Rate omitido. As campanhas usam formatos diferentes (vídeo vs. estático).
Comparar CTR como proxy de atenção.
```

---

### Resposta 5. "Qual campanha devo escalar e qual devo pausar ou revisar?"

Emitir o veredicto final baseado na métrica-norte (CPA ou CPL) e nos gargalos identificados.

```
Veredicto: {A | B} tem melhor eficiência no período analisado.

Recomendação:
- {campanha_vencedora}: candidata a escala via "trafego-escalar"
- {campanha_perdedora}: {pausar | revisar criativo | revisar página} via "trafego-otimizar"
```

Se as campanhas tiverem eficiência muito próxima (diferença < 10% no CPA/CPL), declarar empate técnico e recomendar um A/B formal via "trafego-testes" antes de decidir escala.

Incluir o handoff correspondente conforme o achado (ver tabela de handoffs abaixo).

---

### Resposta 6. "Como as métricas de vídeo (hook, hold, play-through) diferem entre A e B?"

Exibir as três métricas de retenção lado a lado com veredicto por linha:

```
MÉTRICAS DE VÍDEO

                              A                    B
                         {nome_A}             {nome_B}
─────────────────────────────────────────────────────────────
  Hook Rate              {X,XX%}              {X,XX%}     {vencedora}
  Hold Rate              {X,XX%}              {X,XX%}     {vencedora}
  Play-Through           {X,XX%}              {X,XX%}     {vencedora}
─────────────────────────────────────────────────────────────
```

Para cada métrica, nomear o elemento VTSD em jogo (Hook Rate = Urgência Oculta, Hold Rate = Decorados, Play-Through = Furadeira) e indicar se o valor está abaixo do benchmark saudável.

Se nenhuma das campanhas tiver vídeo (`video_p25_watched_actions` ausente ou zero em ambas), substituir o bloco por: "Sem criativo de vídeo, métricas de retenção não disponíveis para este comparativo."

Se os formatos forem assimétricos (uma tem vídeo, a outra não), omitir a tabela de vídeo e registrar: "Formatos diferentes entre A e B. Comparação de métricas de vídeo não é válida neste caso."

---

### Resposta 7. "Tem fadiga em alguma das duas? Frequência alta, CTR caindo?"

Verificar os sinais de fadiga em cada campanha:

- **Frequência acima de 3:** sinal de saturação do público (benchmark: saudável entre 2 e 4, acima de 4 é alerta de fadiga).
- **CTR abaixo de 1%:** proxy de anúncio cansado ou criativo saturado.

```
Fadiga detectada?

Campanha A. Frequência: {X,X} | CTR: {X,XX%}
→ {Sem sinal de fadiga | ALERTA: frequência acima de {N}, público saturado | ALERTA: CTR abaixo de 1%, criativo possivelmente cansado}

Campanha B. Frequência: {X,X} | CTR: {X,XX%}
→ {Sem sinal de fadiga | ALERTA: frequência acima de {N}, público saturado | ALERTA: CTR abaixo de 1%, criativo possivelmente cansado}
```

**Limitação de tendência de CTR:** este output trabalha com dados agregados do período e não detecta se o CTR está caindo ao longo do tempo. Para detectar queda gradual de CTR (fadiga progressiva), usar o output [5] (Timing e Sazonalidade, chamada 5b), que fornece a série diária com `time_increment=1`.

Se houver fadiga em alguma campanha, incluir handoff para "trafego-publicos" para criar nova audiência (Lookalike ou aberto) e rodar o mesmo criativo com público fresco.

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0. Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] Qual das duas campanhas tem melhor CPA ou CPL no período?
    → coberto? Se não: calcular e comparar diretamente CPA/CPL das duas campanhas com delta percentual

[ ] Onde está a diferença principal entre A e B no funil?
    → coberto? Se não: calcular cada etapa (CTR, LPV rate, conversão) das duas e identificar onde o gap percentual é maior

[ ] Em qual etapa a campanha perdedora está travando?
    → coberto? Se não: nomear explicitamente a etapa com maior diferença entre A e B (ex: "A perdedora para no clique: CTR de 0.8% vs 2.1%")

[ ] A diferença é por causa do criativo (hook/hold) ou da página (connect rate)?
    → coberto? Se não: se hook/hold de A > B mas connect_rate similar, problema é criativo; se connect_rate de A < B com CTR parecido, problema é página

[ ] Qual campanha escalar e qual pausar ou revisar?
    → coberto? Se não: indicar a vencedora em CPA e ROAS com recomendação clara de escalar, e a perdedora com causa e handoff para /trafego-otimizar ou /trafego-escalar

[ ] Como as métricas de vídeo (hook, hold, play-through) diferem entre A e B?
    → coberto? Se não: exibir tabela comparativa com hook_rate, hold_rate e play_through_rate lado a lado das duas campanhas

[ ] Tem fadiga em alguma das duas?
    → coberto? Se não: verificar frequência > 3 e queda de CTR WoW em cada uma e sinalizar com diagnóstico de fadiga
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico**: apresentar a confirmação das campanhas comparadas e a tabela comparativa com vencedora por linha (ambas na Resposta 1). Informar quantas dimensões cada campanha venceu.
2. **Causa provável**: relacionar as métricas. Ex: "A venceu em CTR mas B venceu em Connect Rate: o criativo de A atrai mais cliques, mas a página de B converte melhor quem chega. O problema de A está na promessa da página, não no anúncio." Ou: "Frequência de B acima de 4 e CTR médio abaixo do período anterior: sinal de fadiga, não é problema de público ou de página."

   **Limitação de tendência de CTR:** este output trabalha com dados agregados do período e não consegue responder se o CTR está caindo ao longo do tempo. Para detectar tendência de CTR (queda gradual, sazonalidade, fadiga por data), use o output [5] (Timing & Sazonalidade, chamada 5b), que fornece a série diária com `time_increment=1`. Este output mostra apenas a média do período completo.
3. **No VTSD, isso significa...**: qual elemento do método está em jogo na diferença principal e no gargalo identificado. Ex: "Connect Rate 40% abaixo em B = Quadro na Parede quebrado. O anúncio de B está prometendo uma coisa e a página entregando outra. Reescrever a headline da página para espelhar o gancho do anúncio."
4. **Ação recomendada**: 1 a 3 ações concretas com handoff para a skill executora correspondente.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Campanha vencedora com CPA dentro do benchmark e frequência < 3 | "trafego-escalar": candidata a escala vertical ou horizontal |
| Campanha perdedora com gasto alto e conversões zero | "trafego-otimizar": pausar via ação em lote (filtro: gasto > X e zero conversão) |
| Diferença principal em Hook Rate ou Hold Rate | "trafego-testes": A/B de criativo com nova Urgência Oculta ou Decorado diferente |
| Diferença principal em Connect Rate | "feedback-pagina": headline e promessa da página não batem com o anúncio ("trafego-oferta-funil" para confirmar o gargalo) |
| Diferença principal em Checkout Rate ou Conversion Rate | "feedback-pagina" ou "pagina-checkout": revisar oferta, garantia e stack de valor |
| Diferença principal em Lead Rate | "copy-pagina": revisar isca digital e formulário de captura |
| Frequência acima de 4 em alguma das campanhas | "trafego-publicos": criar nova audience (Lookalike ou aberto) para rodar a mesma campanha |
| Campanhas com eficiência próxima (diferença < 10% no CPA/CPL) | "trafego-testes": A/B formal antes de decidir qual escalar |
| Objetivos diferentes entre A e B (SALES vs. LEADS) | Não comparar CPA vs. CPL: avaliar cada uma contra seu benchmark individual |

---

## Mapeamento HTML (export via `_export-html.md`)

Componentes definidos na seção 3.2 do `_export-html.md`. **Usar exatamente estes nomes de classe.** O vocabulário antigo (`.table`, `.kpi`, `.kpi-grid`, `.callout`, `.pitch-box`, `.regra`, `.up`, `.down`, `--neon`, `--rust`) foi descontinuado e NÃO existe no CSS embutido: usá-lo gera seção sem estilo.

| Bloco do output narrado | Componente do design system |
|---|---|
| KPIs globais (métrica-norte A, métrica-norte B, vencedora, nº de dimensões vencidas) | `.stats-grid` com `.stat-card` (`.value.green` na vencedora, `.value.red` na perdedora) |
| Confirmação das campanhas comparadas (Resposta 1, cabeçalho) | `.diag-box` com nomes (IDs mascarados nos últimos 4 dígitos) e período |
| Tabela comparativa lado a lado (Resposta 1, todas as métricas) | `.card` + `table` com colunas métrica / A / B / vencedora; valor vencedor por linha em `style="color:var(--green)"` |
| Totais finais (CPA, CPL ou ROAS) | `.stats-grid` com 2 `.stat-card` lado a lado (`.value.green` no melhor, `.value.red` no pior) |
| Cada "Resposta N" (2 a 7) | `.section` com `.section-header` (`.section-num` + `.section-title` + `.section-question`) |
| "A maior diferença está em..." (Resposta 2) | `.diag-box` com destaque na métrica divergente |
| Gargalo da campanha perdedora (Resposta 3) | `.diag-box.red` com a faixa de benchmark de referência |
| Métricas de vídeo lado a lado (Resposta 6) | `.card` + `.fmt-compare` com um `.fmt-box` por campanha (Hook / Hold / Play-Through) |
| Fadiga em A e B (Resposta 7) | `.card` + `.fmt-compare` (Frequência + CTR por campanha); alerta em `.diag-box.yellow` |
| Diagnóstico / "No VTSD isso significa..." | `.diag-box` (+ `.green/.yellow/.red` conforme o sinal) |
| Veredicto e recomendação final (Resposta 5) | `.action-box` |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no `.page-foot` |

### Gráficos obrigatórios deste output

Renderizar os gráficos abaixo logo após o `.stats-grid` de KPIs, sob um `.section-h` "Visão visual". Todos em SVG/CSS inline, sem dependência (receitas nas seções **3.2.1** e **3.2.1.1** do `_export-html.md`). Gerar cada gráfico SOMENTE com dado real; se um campo não retornar (ex: campanha sem vídeo), omitir o gráfico correspondente (nunca inventar).

| Gráfico | Componente / receita | Fonte de dado | Posição |
|---|---|---|---|
| Funil duplo A × B (Impressões → Cliques → LPV → Vendas) | SVG funil duplo (receita J, helper `dual_funnel`) | Chamadas 10b/10c por campanha | `.chart-card` full-width, topo da "Visão visual" |
| Retenção de vídeo A × B | `.fmt-compare` (ou vbars G via helper) | `video_p25/p50/p75/p95_watched_actions` de 10b/10c | `.charts-grid`, 1ª coluna: **omitir** se nenhuma campanha tiver vídeo ou se os formatos forem assimétricos |
| CTR ao longo do tempo (fadiga) | SVG linha (receita F, helper `line`) | CTR período anterior × atual por campanha (10b/10c + WoW) | `.charts-grid`, 2ª coluna: usar só os pontos que existirem (uma campanha pode não ter janela anterior) |
| Tabela comparativa A × B | `.card` + `table` | 10b/10c (todas as métricas derivadas) | dentro da Resposta 1 |

**Funil duplo (receita J via helper):** montar o spec com os 4 estágios reais de cada campanha, gravar num arquivo e rodar `{PY} .claude/skills/trafego-analise/scripts/trafego_chart_geom.py dual_funnel < /tmp/spec.json` (`{PY}` = interpretador detectado na sessão, `python3` ou `py -3`). O helper devolve `a.stages[]` e `b.stages[]` com `width_pct` (largura em escala log do topo, mínimo 8) e `meta_pct` (taxa de conversão do estágio anterior). Template: `.dual-funnel-grid` com 2 `.dual-funnel-col`; em cada, um `.df-name` + os estágios como `.funnel-stage`/`.funnel-bar` (`style="width:{width_pct}%"`) + `.funnel-meta` com `{meta_pct}% do estágio anterior`. Colorir a barra de Vendas pela vencedora (verde quem converteu, neutro/vermelho quem zerou).

**CTR (receita F via helper):** spec com `series` de uma entrada por campanha (`values` = [CTR anterior, CTR atual]); rodar `dots:true`. Se uma campanha não tiver janela anterior (campanha nova), renderizar só o ponto atual dela e registrar na legenda "sem histórico anterior". Eixo esquerdo em % de CTR.

Regras dos gráficos: usar só cores da paleta; truncar nomes longos; funil duplo sempre via helper `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py dual_funnel`; as métricas de vídeo só entram com `video_p25_watched_actions > 0` real em AMBAS as campanhas.
