# Output [8] — Problemas Ocultos

Achados que normalmente passam despercebidos: ad sets com configuração quebrada, anúncios sem clique, audiências micro, desaprovados silenciosos, pixel sem atividade e públicos de remarketing secando.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- "Tem algum ad set que nunca gastou nada? Pode estar com problema de configuração"
- "Tem anúncio com muita impressão mas zero clique? Criativo pode estar ruim"
- "Algum conjunto de anúncios tem público menor que 1.000 pessoas?"
- "Tem campanha ativa sem nenhuma conversão nos últimos 7 dias?"
- "Estou com algum anúncio desaprovado que eu nem percebi?"
- "Meus pixels estão recebendo eventos? Tem algum sem atividade?"
- "Meus públicos de remarketing estão sendo alimentados ou estão secando?"

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## REGRA OBRIGATÓRIA ANTES DE ENTREGAR QUALQUER BLOCO

> **Todas as 7 perguntas da seção "Perguntas que cobre" precisam ter resposta antes de montar qualquer bloco de output.**
> Não é permitido entregar a análise com "dados não disponíveis" ou "rodar outra skill para detalhar" em substituição a uma busca que poderia ter sido feita.
> Fazer TODAS as chamadas de API abaixo em paralelo ANTES de escrever qualquer parágrafo de análise.

---

## Dados necessários

### O que já vem do Passo 4 do command principal

`level=campaign + adset + ad`, sem breakdowns. Campos base: `spend`, `impressions`, `clicks`, `ctr`, `actions`, `cost_per_action_type`, `effective_status`.

Período: conforme escolha do aluno no Passo 3. Não perguntar novamente.

### Campos adicionais a acrescentar na chamada principal deste output

```
delivery_info,issues_info,
review_feedback,bid_amount,
daily_budget,lifetime_budget
```

`delivery_info` expõe o subestado de entrega do ad set (ex: `CAMPAIGN_PAUSED`, `ADSET_PAUSED`, `ADS_PAUSED`, `AD_SET_NOT_DELIVERING`). `issues_info` expõe problemas conhecidos pelo Meta (ex: `ADS_PROBLEM_FEEDBACK`). `review_feedback` traz o motivo de rejeição quando disponível.

### Chamadas adicionais (executar antes de montar os blocos)

**Chamada 8a — Listagem de ad sets com status detalhado e entrega**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/adsets
  ?fields=id,name,status,effective_status,delivery_info,issues_info,
          daily_budget,lifetime_budget,bid_amount,campaign_id,targeting
  &effective_status={STATUS_FILTRO}
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Chamada 8b — Insights de ad sets no período (para identificar gasto zero e zero conversão)**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=adset_id,adset_name,campaign_id,campaign_name,
          spend,impressions,clicks,ctr,actions,cost_per_action_type
  &level=adset
  &date_preset={PRESET_PERIODO}
  &effective_status={STATUS_FILTRO}
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

Usar `date_preset` equivalente ao período escolhido pelo aluno no Passo 3:
- 7 dias → `last_7d`
- 14 dias → `last_14d`
- 30 dias → `last_30d`
- Customizado → `since={YYYY-MM-DD}&until={YYYY-MM-DD}` (substituir `date_preset`)

**Chamada 8c — Listagem de anúncios com status e motivo de rejeição**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/ads
  ?fields=id,name,status,effective_status,review_feedback,adset_id,campaign_id
  &effective_status={STATUS_FILTRO}
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Chamada 8d — Insights de anúncios no período (impressões vs cliques)**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=ad_id,ad_name,adset_id,adset_name,campaign_id,campaign_name,
          spend,impressions,clicks,ctr
  &level=ad
  &date_preset={PRESET_PERIODO}
  &effective_status={STATUS_FILTRO}
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Chamada 8e — Custom Audiences (remarketing) com tamanho estimado**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/customaudiences
  ?fields=id,name,subtype,approximate_count_lower_bound,
          approximate_count_upper_bound,time_updated,data_source
  &limit=200
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

`approximate_count_lower_bound` e `approximate_count_upper_bound` são os campos corretos para tamanho de audience. O campo legado `approximate_count` foi descontinuado na versão 17.0. Se os dois bounds retornarem `-1`, a audience tem menos de 1.000 pessoas e o Meta não expõe o número exato por privacidade.

**Chamada 8f — Pixels da conta (resumo de atividade)**

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/adspixels
  ?fields=id,name,last_fired_time,is_unavailable
  &limit=50
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

`last_fired_time` indica o último disparo de qualquer evento. Para ver breakdown por evento nos últimos 7 dias, usar Gerenciador de Eventos (diagnóstico aprofundado). Aqui só verificar se o pixel disparou nas últimas 24h.

**Modo MCP_CONECTOR:** usar `mcp__*__ads_get_ad_entities` com `entity_type=adset` para 8a; `mcp__*__ads_insights_performance_trend` para 8b e 8d; `mcp__*__ads_get_ad_entities` com `entity_type=ad` para 8c; `mcp__*__ads_get_dataset_stats` para 8f. Para audiences (8e), não há tool MCP equivalente — fazer chamada REST direta via `access_token`.

### Referência de produto

Ler `perfil.md` (já carregado no Passo 0): campo `preco`. Inferir tipo de funil pelo objetivo predominante das campanhas:
- `OUTCOME_SALES` → funil de venda direta → tipo canônico de conversão: `offsite_conversion.fb_pixel_purchase`
- `OUTCOME_LEADS` → funil de captação → tipo canônico de conversão: `offsite_conversion.fb_pixel_lead`

---

## Fórmulas de cálculo

### Identificação de ad set com gasto zero

```
ad_set_gasto_zero = adset.spend == 0 AND adset.effective_status == "ACTIVE"
  E adset aparece na Chamada 8a com effective_status ACTIVE
  E adset NÃO aparece na Chamada 8b (ou aparece com spend = 0)
```

Se o ad set apareceu na Chamada 8b com `spend = 0` e existe na Chamada 8a com `effective_status = ACTIVE`, trata-se de problema de entrega, não de pausa intencional.

### Identificação de anúncio com impressão alta e zero clique

```
impressoes_altas_sem_clique = ad.impressions >= 5.000 AND ad.clicks == 0
  (período do Passo 3, Chamada 8d)
```

Threshold: 5.000 impressões é o mínimo para considerar o padrão estatisticamente relevante. Abaixo disso, pode ser volume insuficiente.

### Identificação de audience micro

```
audience_micro = approximate_count_upper_bound < 1.000
               OU (lower_bound == -1 AND upper_bound == -1)
```

Bounds retornando `-1` significam menos de 1.000 pessoas (limite de privacidade do Meta).

### Identificação de conversão zero no período

**Template A — Venda direta (OUTCOME_SALES):**

```
conversao_zero_sales = sum(actions onde action_type = "offsite_conversion.fb_pixel_purchase") == 0
  E adset.spend > 50 no período (Chamada 8b)
  E adset.effective_status == "ACTIVE" (Chamada 8a)
```

**Template B — Captação de leads (OUTCOME_LEADS):**

```
conversao_zero_leads = sum(actions onde action_type = "offsite_conversion.fb_pixel_lead") == 0
  E adset.spend > 50 no período (Chamada 8b)
  E adset.effective_status == "ACTIVE" (Chamada 8a)
```

Threshold de spend: R$ 50 no período. Abaixo disso, o ad set pode simplesmente não ter recebido budget suficiente para converter.

### Pixel inativo

```
pixel_inativo = last_fired_time < (agora - 24h)
pixel_morto   = last_fired_time < (agora - 72h) OU last_fired_time ausente
```

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "Tem algum ad set que nunca gastou nada? Pode estar com problema de configuração"

Cruzar Chamada 8a (ad sets ACTIVE) com Chamada 8b (insights). Ad sets presentes em 8a com `effective_status = ACTIVE` que não aparecem em 8b ou aparecem com `spend = 0`.

**Classificar causa provável por campo `delivery_info` e `issues_info` da Chamada 8a:**

| `delivery_info` retornado | Causa provável |
|---|---|
| `AD_SET_NOT_DELIVERING` | problema no próprio ad set (budget, bid, público) |
| `ADS_PAUSED` | todos os anúncios dentro do ad set estão pausados |
| `CAMPAIGN_PAUSED` | a campanha-pai está pausada (ad set herdou) |
| `PENDING_REVIEW` | em revisão |
| Ausente ou nulo | causa desconhecida — verificar manualmente |

```
🔌 AD SETS ATIVOS SEM GASTO  ·  {período}

  #   Ad Set                    Campanha               Último status            Causa provável
  ──────────────────────────────────────────────────────────────────────────────────────────────
  1.  {nome}                    {nome_campanha}        AD_SET_NOT_DELIVERING    público muito restrito
  2.  {nome}                    {nome_campanha}        ADS_PAUSED               todos os anúncios pausados
  3.  {nome}                    {nome_campanha}        —                        verificar manualmente

  Total: {N} ad sets ativos sem nenhum gasto no período.
```

Se nenhum ad set tiver esse problema: "Nenhum ad set ativo sem gasto identificado no período."

---

### Resposta 2. "Tem anúncio com muita impressão mas zero clique? Criativo pode estar ruim"

Cruzar Chamada 8d. Filtrar `impressions >= 5.000 AND clicks == 0` no período.

```
👁️  ANÚNCIOS QUE APARECEM MAS NINGUÉM CLICA  ·  {período}

  #   Anúncio                   Ad Set                 Impressões   Cliques   CTR
  ──────────────────────────────────────────────────────────────────────────────────
  1.  {nome}                    {nome_adset}           {N:,}        0         0%
  2.  {nome}                    {nome_adset}           {N:,}        0         0%
  ...

  Total gasto nesses anúncios: R$ {X}
```

Causa provável por combinação de campos:
- Alto `spend` + CTR 0%: criativo não comunica o que é clicável, ou a audiência é completamente errada para o ângulo.
- `spend = 0` + impressões altas: anúncio está sendo entregue por tráfego de alcance (objetivo `OUTCOME_AWARENESS`) — sem CTA de clique, comportamento esperado. Não é problema nesse caso, apenas documentar.

Se nenhum anúncio atender ao critério: "Nenhum anúncio com 5.000+ impressões e zero clique no período."

---

### Resposta 3. "Algum conjunto de anúncios tem público menor que 1.000 pessoas?"

Dados vêm da Chamada 8e. Listar audiences onde `approximate_count_upper_bound < 1.000` ou ambos os bounds retornam `-1`.

```
🎯 AUDIÊNCIAS MICRO  ·  (tamanho estimado pelo Meta)

  #   Audience                   Tipo            Tamanho estimado     Criada em
  ──────────────────────────────────────────────────────────────────────────────
  1.  {nome}                     CUSTOM          < 1.000              {data}
  2.  {nome}                     LOOKALIKE       < 1.000              {data}
  ...
```

Classificar `subtype` (campo da Chamada 8e):

| Subtipo | Nome exibido |
|---|---|
| `CUSTOM` | CUSTOM (pixel, lista ou engajamento) |
| `LOOKALIKE` | LOOKALIKE |
| `SAVED_AUDIENCE` | SAVED |
| `ENGAGEMENT` | ENGAJAMENTO |

Causa provável por tipo:
- CUSTOM (pixel): evento rastreando pouco volume. Solução: ampliar janela de atribuição ou usar evento de mais alto volume (ex: `ViewContent` em vez de `Purchase`).
- CUSTOM (lista): lista de emails pequena. Solução: fazer upload de lista maior ou usar como semente de Lookalike.
- LOOKALIKE: audience-semente muito pequena. Lookalike precisa de pelo menos 100 pessoas na semente para ser gerado.

Se nenhuma audience for micro: "Nenhuma audience com tamanho abaixo de 1.000 pessoas identificada."

---

### Resposta 4. "Tem campanha ativa sem nenhuma conversão nos últimos 7 dias?"

Cruzar Chamada 8b com tipo canônico conforme tipo de funil. **Agrupar por campanha:** somar gasto e conversões de todos os adsets de uma mesma campanha (`campaign_id`). O template exibe uma linha por campanha, com o número de adsets com zero conversão dentro dela.

#### Template A — Venda direta (OUTCOME_SALES)

```
💸 CAMPANHAS ATIVAS SEM COMPRA  ·  {período}  ·  Threshold: gasto > R$ 50 + zero compras

  #   Campanha               Adsets c/ zero compra   Gasto total   Compras   Nota de risco
  ────────────────────────────────────────────────────────────────────────────────────────────
  1.  {nome_campanha}        {N} de {total}           R$ {X}        0         🔴 alto
  2.  {nome_campanha}        {N} de {total}           R$ {X}        0         🟡 médio
  ...

  Gasto total nessas campanhas: R$ {soma}
```

#### Template B — Captação de leads (OUTCOME_LEADS)

```
💸 CAMPANHAS ATIVAS SEM LEAD  ·  {período}  ·  Threshold: gasto > R$ 50 + zero leads

  #   Campanha               Adsets c/ zero lead      Gasto total   Leads   Nota de risco
  ──────────────────────────────────────────────────────────────────────────────────────────
  1.  {nome_campanha}        {N} de {total}           R$ {X}        0       🔴 alto
  2.  {nome_campanha}        {N} de {total}           R$ {X}        0       🟡 médio
  ...

  Gasto total nessas campanhas: R$ {soma}
```

**Nota de risco por campanha:**
- 🔴 alto: todos os adsets da campanha têm zero conversão E gasto > R$ 150.
- 🟡 médio: parte dos adsets tem zero conversão OU gasto entre R$ 50 e R$ 150 (pode estar em aprendizado).
- 🟢 ok: campanha tem pelo menos uma conversão (não aparece nesta lista).

Causa provável:
- Pixel não rastreando: verificar com Resposta 6 (pixel).
- Ad set em fase de aprendizado inicial: se `spend` < R$ 150, pode ser normal não ter conversão ainda.
- Público errado para o ângulo do criativo.

Se nenhuma campanha atender ao critério: "Nenhuma campanha ativa com gasto acima de R$ 50 e zero conversão no período."

---

### Resposta 5. "Estou com algum anúncio desaprovado que eu nem percebi?"

Dados vêm da Chamada 8c. Filtrar `effective_status == "DISAPPROVED"` ou `review_feedback` com conteúdo.

```
🚫 ANÚNCIOS DESAPROVADOS

  #   Anúncio                   Ad Set                 Motivo de rejeição
  ─────────────────────────────────────────────────────────────────────────────────────
  1.  {nome}                    {nome_adset}           "{review_feedback}"
  2.  {nome}                    {nome_adset}           "{review_feedback}"
  ...

  Impacto: {N} anúncio(s) desaprovado(s). Cada desaprovação ativa reduz o score
  de qualidade da conta (Account Quality) e pode encarecer o leilão das campanhas ativas.
```

Cruzar motivo com categorias comuns de rejeição do Meta:

| Categoria de motivo | Como identificar no `review_feedback` | Ação recomendada |
|---|---|---|
| Promessa de resultado de saúde | "health", "cure", "heal", "medical" | Revisar copy — remover promessas de resultado médico |
| Conteúdo financeiro sensível | "financial", "investment", "income" | Remover promessas de retorno financeiro específico |
| Imagem enganosa | "misleading", "before and after" | Substituir imagem |
| Política de publicidade | "policy", "prohibited content" | Ler política de anúncios do Meta e refazer |
| Público restrito (18+) | "alcohol", "gambling", "adult" | Adicionar restrição de idade ao ad set |
| Motivo não informado | campo vazio ou ausente | Verificar Account Quality no Gerenciador |

Se nenhum anúncio estiver desaprovado: "Nenhum anúncio desaprovado identificado."

---

### Resposta 6. "Meus pixels estão recebendo eventos? Tem algum sem atividade?"

Dados vêm da Chamada 8f. Apresentar resumo de atividade de cada pixel da conta, classificando por status:

```
📡 PIXELS DA CONTA  ·  (atividade baseada em last_fired_time)

  #   Pixel                        ID                  Último disparo         Status
  ──────────────────────────────────────────────────────────────────────────────────────
  1.  {nome}                       {id}                há {N} minutos         🟢 ativo
  2.  {nome}                       {id}                há {N} dias            🟡 verificar
  3.  {nome}                       {id}                sem registro           🔴 sem atividade
```

Classificação por `last_fired_time`:

| Condição | Classificação | O que significa |
|---|---|---|
| Disparou nas últimas 24h | 🟢 ativo | Pixel funcionando normalmente |
| Disparou entre 24h e 72h | 🟡 verificar | Site pode ter pouco tráfego ou evento intermitente |
| Não disparou há mais de 72h | 🔴 sem atividade | Pixel provavelmente quebrado ou script removido |
| `last_fired_time` ausente | 🔴 sem registro | Pixel nunca disparou ou foi recriado recentemente |

**Limitação importante:** este bloco mostra apenas se o pixel disparou algum evento recente. Para ver breakdown por tipo de evento (Purchase, Lead, ViewContent etc.) e detectar quais eventos pararam de disparar, usar o diagnóstico completo no Gerenciador de Eventos.

**Atenção — falso positivo:** `last_fired_time` indica o último disparo de qualquer evento, não necessariamente o evento de conversão configurado na campanha. Um pixel que dispara `PageView` continuamente mas não dispara `Purchase` vai aparecer como "ativo" (🟢) neste bloco, mesmo sem conversões rastreadas. Para verificar se o evento específico da campanha está sendo disparado, cruzar com os dados de `event_stats` do dataset (Chamada 8f aprofundada ou Gerenciador de Eventos).

---

### Resposta 7. "Meus públicos de remarketing estão sendo alimentados ou estão secando?"

Cruzar Chamada 8e com foco em audiences de remarketing (subtipo `CUSTOM` ou `ENGAGEMENT`) que têm `time_updated` disponível. Detectar audiences que encolheram em relação ao período anterior.

**Nota de limitação:** a Graph API não retorna histórico de tamanho de audience por data — só o snapshot atual via `approximate_count_lower_bound` e `approximate_count_upper_bound`. O tamanho "anterior" só está disponível se houver cache local de execução anterior desta análise salvo em `meus-produtos/{ativo}/trafego/insights/`. Se não houver cache, exibir apenas o snapshot atual com `time_updated`.

```
💧 REMARKETING — SNAPSHOT ATUAL  ·  (histórico disponível se houver cache anterior)

  #   Audience                   Subtipo        Tamanho estimado        Atualizada em
  ──────────────────────────────────────────────────────────────────────────────────────
  1.  {nome}                     CUSTOM         {lower} a {upper}       {data}
  2.  {nome}                     ENGAGEMENT     {lower} a {upper}       {data}
  ...

  ⚠️  Audiences com tamanho baixo (< 5.000): {lista}
  ⚠️  Audiences não atualizadas há mais de 7 dias: {lista}
```

Se houver cache anterior (arquivo de insights salvo com data anterior):

```
💧 REMARKETING — VARIAÇÃO  ·  {data_cache_anterior} → hoje

  #   Audience                   Subtipo        Tamanho anterior   Tamanho atual   Variação
  ────────────────────────────────────────────────────────────────────────────────────────────
  1.  {nome}                     CUSTOM         {N}                {M}             {+/-X%}
  ...

  🔴 Audiences encolhendo > 20%: {lista}
```

Threshold de alerta:
- Audience com `approximate_count_upper_bound < 5.000` ativa em campanha de remarketing: alto risco de micro-segmentação.
- Audience não atualizada (`time_updated`) há mais de 14 dias: evento de pixel pode ter parado de alimentar a audience.
- Variação negativa > 20% entre snapshots: funil de topo esfriando ou evento quebrado.

**Instrução de cache — obrigatória ao concluir o output [8]:**

Ao finalizar a entrega deste output, salvar um resumo dos problemas identificados em:

```
meus-produtos/{ativo}/.cache-problemas-ocultos.md
```

O arquivo deve conter:
- Data do diagnóstico (formato `YYYY-MM-DD HH:MM`)
- Lista de problemas encontrados por resposta (1 a 7), com severidade (alto / médio / nenhum)
- Snapshot de tamanho das audiences de remarketing (para comparação futura)

Este cache é lido pelo output [9] (Orçamento e Projeção) se precisar cruzar com problemas estruturais identificados aqui. Regra de invalidação: se a data registrada no arquivo for anterior a 24 horas em relação ao momento atual, ignorar o cache e rodar o output [8] novamente antes de prosseguir para o [9].

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto exato da pergunta como título (formato "Resposta N. '{pergunta}'"). A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada uma das 7 perguntas tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0 — Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] "Tem algum ad set que nunca gastou nada? Pode estar com problema de configuração"
    → coberto? Se não: filtrar adsets com spend = 0 e status ACTIVE no período e listar com possíveis causas (delivery_info + issues_info)

[ ] "Tem anúncio com muita impressão mas zero clique? Criativo pode estar ruim"
    → coberto? Se não: listar anúncios com impressions >= 5.000 e clicks == 0 no período

[ ] "Algum conjunto de anúncios tem público menor que 1.000 pessoas?"
    → coberto? Se não: verificar approximate_count_upper_bound de cada audience e sinalizar as micro

[ ] "Tem campanha ativa sem nenhuma conversão nos últimos 7 dias?"
    → coberto? Se não: listar campanhas ACTIVE com 0 conversões no período e gasto > R$ 50

[ ] "Estou com algum anúncio desaprovado que eu nem percebi?"
    → coberto? Se não: buscar anúncios com effective_status = DISAPPROVED e informar motivo quando disponível

[ ] "Meus pixels estão recebendo eventos? Tem algum sem atividade?"
    → coberto? Se não: checar last_fired_time de cada pixel vinculado à conta e sinalizar os inativos

[ ] "Meus públicos de remarketing estão sendo alimentados ou estão secando?"
    → coberto? Se não: verificar tamanho atual das custom audiences de remarketing e alertar as com menos de 5.000 pessoas ou não atualizadas há mais de 14 dias
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico** — lista priorizada dos problemas ocultos identificados, do mais crítico (impacto financeiro imediato) ao menos crítico (risco futuro).
2. **Causa provável** — o que os sinais sugerem em conjunto. Exemplos: "3 ad sets ativos sem gasto + pixel sem atividade há 5 dias = provável que o pixel parou de rastrear, o Meta perdeu o sinal de conversão e pausou automaticamente os ad sets por não encontrar padrão para otimizar"; "audience de remarketing com 800 pessoas + event de Purchase com volume baixo = funil de topo pequeno demais para sustentar o remarketing".
3. **No VTSD, isso significa…** — qual elemento do método está sendo afetado. Exemplos: "Audience de carrinho abandonado caiu 33% e pixel está sem atividade. Provável: evento `InitiateCheckout` parou de disparar. Sem esse evento, a Furadeira vaza antes do checkout — o aluno não retorna, a Urgência Oculta morre sem reforço."; "Anúncio com 12.000 impressões e 0 cliques = Identidade do Produto não está sendo comunicada. O criativo aparece, mas não convida à ação.".
4. **Ação recomendada** — handoffs específicos por categoria de problema (ver tabela abaixo). Ordenar pelas ações de maior impacto primeiro.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Ad set ativo sem gasto por problema de público micro | Gerenciador de Audiences — recriar audience com critérios mais amplos ou usar Advantage+ Audience |
| Ad set ativo sem gasto por anúncios pausados | Verificar manualmente no Gerenciador e reativar os anúncios |
| Anúncio com impressão alta e zero clique | "trafego-otimizar" (pausar) seguido de Duplicar entidade no Gerenciador (variando 1 dimensão) (novo criativo com CTA mais claro) |
| Audiência micro em campanha ativa | Gerenciador de Audiences — recriar com janela maior, evento de mais volume ou Lookalike |
| Ad set com zero conversão e gasto > R$ 50 | "trafego-otimizar" — atalho pausar com filtro: conversoes=0 E spend>50 |
| Anúncio desaprovado | "copy-anuncio" (refazer copy respeitando política) e recurso manual no Meta se copy estiver correta |
| Pixel sem atividade | Gerenciador de Eventos (diagnóstico completo de eventos) — pode exigir "pagina-pixel" para reinstalar script |
| Remarketing secando por pixel quebrado | Gerenciador de Eventos (verificar evento que alimenta a audience) seguido de Gerenciador de Audiences (recriar audience com critério maior enquanto corrige o evento) |

---

## Mapeamento HTML (export via `_export-html.md`)

| Bloco do output narrado | Componente do design system |
|---|---|
| Bloco 1 — Ad sets sem gasto (tabela) | `.table` com colunas: ad set / campanha / status / causa — linha com causa desconhecida recebe `.down` |
| Bloco 2 — Impressões sem clique (tabela) | `.table` com colunas: anúncio / ad set / impressões / cliques / CTR — coluna CTR recebe `.down` (rust) |
| Bloco 3 — Audiências micro (tabela) | `.table` com colunas: audience / tipo / tamanho / criada em — linhas com `-1` recebem `.down` |
| Bloco 4 — Zero conversão (tabela) | `.table` com coluna "CPA implícito" exibindo "infinito" em `.down` (rust) |
| Total de gasto em campanhas sem resultado | `.metric` (número grande em `--accent`) com rótulo "em risco" |
| Bloco 5 — Desaprovados (tabela) | `.regra.alerta` por anúncio — um elemento por linha de rejeição |
| Bloco 6 — Pixels (tabela de status) | `.kpi-grid` com um `.kpi` por pixel: `--neon` para 🟢, `--accent` para 🟡, `--rust` para 🔴 |
| Bloco 7 — Remarketing secando (tabela) | `.table` com coluna de variação: `.up` para positivo, `.down` para negativo — destacar linhas com variação < -20% |
| Frase "No VTSD isso significa..." | `.callout` |
| Ação recomendada | `.pitch-box` |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no rodapé |
