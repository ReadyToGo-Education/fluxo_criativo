# Output [2]. Performance & Funil

Visão narrada de **performance comparada e mapa de funil** para um período. O aluno entende quem é melhor, quem é pior, e onde o funil vaza.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- “Me dá um ranking das 5 melhores campanhas por ROAS dos últimos 30 dias”
- “Compara o CPM desse mês vs. mês anterior: ficou mais caro anunciar?”
- “Qual posicionamento (Feed, Stories, Reels) está trazendo mais resultado?”
- “Me mostra o funil completo: impressões → cliques → conversões de cada campanha”
- “Qual público (idade, gênero, região) está convertendo mais barato?”

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## Dados necessários

### O que já vem do Passo 4 do command principal

`level=campaign + ad`, breakdowns `publisher_platform` e `platform_position`. Campos base: `spend`, `impressions`, `clicks`, `ctr`, `cpm`, `cpc`, `reach`, `frequency`, `actions`, `action_values`, `cost_per_action_type`, métricas de vídeo.

Período: conforme escolha do aluno no Passo 3. Não perguntar novamente.

### Campos adicionais a acrescentar na chamada principal deste output

```
outbound_clicks
```

**`landing_page_views` NÃO é um campo válido no parâmetro `fields` da Insights API**: causa erro 400 imediato.
O valor de LP views vem do array `actions` com `action_type = "landing_page_view"`:

```python
lp_views = next((float(a['value']) for a in actions if a['action_type'] == 'landing_page_view'), 0)
```

`outbound_clicks` é um campo válido (retorna lista: pegar `[0]['value']` se existir).
Os rankings de qualidade (`quality_ranking`, `engagement_rate_ranking`, `conversion_rate_ranking`) estão disponíveis apenas no nível `ad`, não no nível `campaign`. Omitir na chamada de nível campanha.

### Chamada adicional. Comparativo CPM e ROAS (período anterior)

Para responder "CPM de maio vs. abril ficou mais caro?", fazer **duas chamadas curl separadas**: uma por período.

**Regras obrigatórias:**
- Usar `time_range` como JSON (não `since`/`until` direto no urlencode: causa comportamento imprevisível).
- **NÃO usar `effective_status` nas chamadas de comparação**: com `effective_status`, a API ignora a janela histórica e retorna sempre o estado atual, fazendo ambos os períodos retornarem dados idênticos.
- Calcular as datas em **chamadas Bash separadas** com `date` (nunca em script Python heredoc: ver regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md).

#### Padrão obrigatório (modo APP)

**Passo 1. Calcular as 4 datas em chamadas `Bash(date ...)` separadas:**

No Mac, cada uma é uma chamada Bash independente:
```
date -v-1d +%Y-%m-%d     # atual_ate (ontem)
date -v-30d +%Y-%m-%d    # atual_de (há 30 dias)
date -v-31d +%Y-%m-%d    # ant_ate (anteontem da janela atual)
date -v-60d +%Y-%m-%d    # ant_de (60 dias atrás)
```

No Linux, equivalente:
```
date -d "1 day ago" +%Y-%m-%d
date -d "30 days ago" +%Y-%m-%d
date -d "31 days ago" +%Y-%m-%d
date -d "60 days ago" +%Y-%m-%d
```

**Passo 2. Disparar 2 chamadas curl separadas (cada uma é uma `Bash(curl ...)` independente):**

```
curl -s "https://graph.facebook.com/v25.0/act_<ACCOUNT_ID>/insights?fields=campaign_id,campaign_name,spend,impressions,cpm,actions,action_values&level=campaign&time_range=%7B%22since%22%3A%22<atual_de>%22%2C%22until%22%3A%22<atual_ate>%22%7D&limit=500&access_token=<TOKEN_DO_ENV>"
```

```
curl -s "https://graph.facebook.com/v25.0/act_<ACCOUNT_ID>/insights?fields=campaign_id,campaign_name,spend,impressions,cpm,actions,action_values&level=campaign&time_range=%7B%22since%22%3A%22<ant_de>%22%2C%22until%22%3A%22<ant_ate>%22%7D&limit=500&access_token=<TOKEN_DO_ENV>"
```

Notar o `time_range` URL-encoded: `%7B` é `{`, `%22` é `"`, `%2C` é `,`, `%7D` é `}`. URL final é `time_range={"since":"YYYY-MM-DD","until":"YYYY-MM-DD"}`.

**Passo 3. Processamento dos JSONs:**

Cada `curl` retorna `{"data": [{"campaign_id": "...", "spend": "...", "cpm": "...", "actions": [...], "action_values": [...]}, ...]}`. Manter só as campanhas cujo `campaign_id` está em `CAMPANHAS_SESSAO` (status e escopo escolhidos nos Passos 0.55 e 0.6 do `SKILL.md`). O Claude lê os 2 JSONs como texto, calcula ROAS/CPL/CPM por campanha aplicando as fórmulas da seção "Fórmulas de cálculo" abaixo, e devolve o comparativo em linguagem natural.

**Não rodar Python adicional pra fazer essas contas.** A regra global no CLAUDE.md proíbe heredoc, pipe `curl | python3` e `python3 -c` longo com token: disparam o detector "expansion obfuscation" e exibem o token no pop-up nativo.

#### Modo MCP_CONECTOR

Buscar com `mcp__*__ads_get_ad_entities` em `level=campaign`, uma chamada por janela (atual e anterior), usando o **dicionário de campos do MCP** (a tool **não** aceita `actions`/`action_values`/`outbound_clicks`):

- Para ROAS/ranking: `purchase_roas`, `actions:omni_purchase`, `cost_per_result`, `result_values`, `spend`, `impressions`, `cpm`, `ctr` (+ `id`, `name`).
- Para o funil: `actions:link_click`, `video_p25_watched_actions`; eventos de página/checkout (LPV, initiate_checkout) podem não estar no dicionário básico, confirmar com `ads_get_field_context`. Se a tool não entregar, omitir as etapas do funil que dependem desse evento e avisar o aluno (nunca inventar o número). Se o aluno precisar do funil completo com frequência, o modo App (`/trafego-conexao`) traz esses eventos dentro do array `actions`.

**Nunca** usar `ads_insights_performance_trend` aqui: ela só faz tendência temporal de conta/anúncio/conjunto e **não tem nível campanha**: retorna vazio para ranking e funil. Whitelist de campos + `limit` sempre, e se o retorno for salvo em arquivo (conta grande), processar com python/jq. Ver **Contrato anti-erros** no `SKILL.md` (Passo 0).

#### Exceção (volume grande)

Se a campanha tem 200+ entidades e o cálculo manual fica inviável, salvar os 2 JSONs em arquivos separados via `curl ... > /tmp/cmp_atual.json` e `curl ... > /tmp/cmp_anterior.json`, depois rodar `{PY} /tmp/script.py` (interpretador detectado na sessão) onde o script lê os arquivos locais (sem token dentro). Limpar `/tmp/cmp_*.json` ao final.

### Referência de produto

Ler do `resumo-produto.md` (já carregado no Passo 0.1 do `SKILL.md`): preço e tipo de produto. Não perguntar de novo. Inferir tipo de funil pelo objetivo predominante das campanhas:
- `OUTCOME_SALES` → funil de venda direta → métrica-norte = **ROAS**
- `OUTCOME_LEADS` → funil de captação → métrica-norte = **CPL**

---

## Fórmulas de cálculo (obrigatório aplicar antes de montar os blocos)

### ROAS
```
ROAS = sum(action_values onde action_type = "offsite_conversion.fb_pixel_purchase") / sum(spend)
```
Usar tipo canônico. Nunca somar outros tipos de purchase.

### CPL
```
CPL = sum(spend) / sum(actions onde action_type = "offsite_conversion.fb_pixel_lead")
```

### CPA
```
CPA = sum(spend) / sum(actions onde action_type = "offsite_conversion.fb_pixel_purchase")
```

### Métricas de funil (calcular por campanha)

| Métrica | Fórmula | Denominador zero |
|---|---|---|
| Hook Rate | `video_p25_watched_actions` / `impressions` | marcar `-` se não houver vídeo |
| CTR (link) | `link_click` / `impressions` | nunca zero |
| Connect Rate | `landing_page_view` / `link_click` (ambos do array `actions`) | marcar `-` se LP views ausente |
| Lead Rate | `leads` / `landing_page_views` | só para funil OUTCOME_LEADS |
| Checkout Rate | `initiate_checkout` / `landing_page_views` | só para funil OUTCOME_SALES |
| Conversion Rate | `purchases` / `initiate_checkout` | só para funil OUTCOME_SALES |

`initiate_checkout` = `offsite_conversion.fb_pixel_initiate_checkout` (tipo canônico).

`link_click` vem do array `actions` (`action_type = "link_click"`), nunca do campo de topo `clicks`: o campo `clicks` inclui cliques em qualquer parte do post e inflaria o CTR (link).

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "Me dá um ranking das 5 melhores campanhas por ROAS dos últimos 30 dias"

Usar métrica-norte conforme tipo de funil (ROAS para venda direta, CPL para captação). Se a conta tiver campanhas dos dois tipos, calcular separado e exibir dois rankings.

**Venda direta: ranking por ROAS:**

```
🏆 TOP 5 WINNERS  ·  {período}  ·  Métrica: ROAS

  #   Campanha                   ROAS    CPA        Spend      Compras
  ─────────────────────────────────────────────────────────────────────
  1.  {nome}                     {X.X}x  R$ {Y}     R$ {Z}     {N}
  2.  {nome}                     {X.X}x  R$ {Y}     R$ {Z}     {N}
  3.  {nome}                     {X.X}x  R$ {Y}     R$ {Z}     {N}
  4.  {nome}                     {X.X}x  R$ {Y}     R$ {Z}     {N}
  5.  {nome}                     {X.X}x  R$ {Y}     R$ {Z}     {N}

🛑 TOP 5 LOSERS  (mesma métrica, ordem inversa)

  #   Campanha                   ROAS    CPA        Spend      Compras
  ─────────────────────────────────────────────────────────────────────
  1.  {nome}                     {X.X}x  R$ {Y}     R$ {Z}     {N}
  ...
  ⚠️  {campanha com gasto alto + ROAS < 1} → candidata a pausar
```

**Captação de leads: ranking por CPL:**

```
🏆 TOP 5 WINNERS  ·  {período}  ·  Métrica: CPL

  #   Campanha                   CPL        Leads    Spend
  ──────────────────────────────────────────────────────
  1.  {nome}                     R$ {X}     {N}      R$ {Y}
  ...
```

---

### Resposta 2. "Compara o CPM desse mês vs. mês anterior: ficou mais caro anunciar?"

```
📊 CPM: EVOLUÇÃO DO LEILÃO

  Período atual ({datas}):    R$ {X}  (média ponderada por spend)
  Período anterior ({datas}): R$ {Y}
  Variação:                   {+/-Z%}  {🟢 | 🟡 | 🔴}

  Leitura:
```

| Variação do CPM | Interpretação | Hipóteses |
|---|---|---|
| Subiu > 20% | 🔴 Leilão ficou caro | Sazonalidade, criativo fadigado, novo concorrente na praça |
| Subiu 10% a 20% | 🟡 Atenção | Monitorar: pode ser pontual |
| Estável (±10%) | 🟢 Leilão saudável | Nenhuma ação necessária |
| Caiu > 10% | 🟢 Leilão melhorou | Novo criativo, novo público, fora de sazonalidade |

Também comparar ROAS médio ponderado do período atual vs. anterior:

```
  ROAS atual:    {X.X}x
  ROAS anterior: {Y.Y}x
  Variação:      {+/-Z%}  {🟢 | 🔴}
```

---

### Resposta 3. "Qual posicionamento (Feed, Stories, Reels) está trazendo mais resultado?"

Dados vêm do breakdown `publisher_platform` + `platform_position` já incluído na chamada do Passo 4.

```
📱 POSICIONAMENTO  ·  {período}

  Posicionamento             Spend     CPA/CPL    CTR     Conversões
  ──────────────────────────────────────────────────────────────────
  Instagram Reels            R$ {X}    R$ {Y}     {Z%}    {N}
  Instagram Feed             R$ {X}    R$ {Y}     {Z%}    {N}
  Facebook Feed              R$ {X}    R$ {Y}     {Z%}    {N}
  Instagram Stories          R$ {X}    R$ {Y}     {Z%}    {N}
  Audience Network           R$ {X}    R$ {Y}     {Z%}    {N}
  (outros se houver)

  Vencedor: {posicionamento}, CPA {X%} abaixo da média
  Perdedor: {posicionamento}, CPA {X%} acima da média → testar excluir via /trafego-testes
```

Se um posicionamento tiver gasto > 10% do total E conversões = 0 → marcar como `⚠️ queimando`.

---

### Resposta 4. "Me mostra o funil completo: impressões → cliques → conversões de cada campanha"

Mostrar o funil da campanha winner da Resposta 1 (ou da campanha que o aluno escolheu no escopo). Usar dois templates conforme o tipo de funil:

#### Template A. Venda direta (OUTCOME_SALES)

```
🔻 FUNIL: {nome_campanha}  ·  {período}

IMPRESSÕES         {N:,}
  ↓ Hook Rate {X%} {🟢|🟡|🔴}     · Urgência Oculta ativa (ou não)
  [somente se campanha tiver vídeo: omitir linha se estático]

CLIQUES (LINK)     {N:,}
  CTR {X%} {🟢|🟡|🔴}            · Identidade do Produto: promessa clara?

LP VIEWS           {N:,}
  ↓ Connect Rate {X%} {🟢|🟡|🔴} · Quadro na Parede: anúncio alinhado com a página?

CHECKOUT INICIADO  {N:,}
  ↓ Checkout Rate {X%} {🟢|🟡|🔴} · Oferta: preço, garantia e stack de valor OK?

COMPRAS            {N:,}
  ↓ Conv. Rate {X%} {🟢|🟡|🔴}   · Furadeira + Decorados: checkout convence?

────────────────────────────────
ROAS final: {X.X}x  ·  CPA: R$ {Y}  ·  Spend: R$ {Z}
```

#### Template B. Captação de leads (OUTCOME_LEADS)

```
🔻 FUNIL: {nome_campanha}  ·  {período}

IMPRESSÕES         {N:,}
  ↓ Hook Rate {X%} {🟢|🟡|🔴}     · Urgência Oculta ativa (ou não)
  [somente se vídeo]

CLIQUES (LINK)     {N:,}
  CTR {X%} {🟢|🟡|🔴}            · Identidade do Produto: ângulo correto?

LP VIEWS           {N:,}
  ↓ Connect Rate {X%} {🟢|🟡|🔴} · Quadro na Parede: anúncio alinhado com a página?

LEADS              {N:,}
  ↓ Lead Rate {X%} {🟢|🟡|🔴}    · Isca Digital: oferta de captura convincente?

────────────────────────────────
CPL: R$ {X}  ·  Total leads: {N}  ·  Spend: R$ {Y}
```

#### Benchmarks para classificação de cada etapa

| Métrica | 🔴 Abaixo | 🟡 Atenção | 🟢 Saudável |
|---|---|---|---|
| Hook Rate (vídeo) | < 15% | 15% a 25% | > 25% |
| CTR (link) | < 1% | 1% a 2% | > 2% |
| Connect Rate | < 50% | 50% a 70% | > 70% |
| Checkout Rate | < 5% | 5% a 12% | > 12% |
| Conversion Rate | < 20% | 20% a 35% | > 35% |
| Lead Rate | < 5% | 5% a 15% | > 15% |

Se `landing_page_views` não retornar (pixel sem evento de LP view), omitir as linhas "LP VIEWS", "Connect Rate" e tudo que depende delas. Alertar: "LP views não rastreado. Conecte o evento no pixel via 'trafego-pixel' para ver o funil completo."

---

### Resposta 5. "Qual público (idade, gênero, região) está convertendo mais barato?"

Cruzar os breakdowns de idade (`age`), gênero (`gender`) e região (`region`) com a métrica-norte (CPA para venda direta, CPL para captação) e destacar o segmento mais eficiente de cada dimensão.

```
👥 PÚBLICO: SEGMENTO MAIS EFICIENTE  ·  {período}

  Por faixa etária:
    Melhor:  {faixa}  →  CPA/CPL R$ {X}  ({N} conversões)
    Pior:    {faixa}  →  CPA/CPL R$ {Y}  ({N} conversões)

  Por gênero:
    Melhor:  {gênero}  →  CPA/CPL R$ {X}  ({N} conversões)
    Pior:    {gênero}  →  CPA/CPL R$ {Y}  ({N} conversões)

  Por região (top 3):
    1. {estado/cidade}  →  CPA/CPL R$ {X}  ({N} conversões)
    2. {estado/cidade}  →  CPA/CPL R$ {Y}  ({N} conversões)
    3. {estado/cidade}  →  CPA/CPL R$ {Z}  ({N} conversões)

  ⚠️  Segmento queimando dinheiro: {faixa/gênero/região com gasto > 10% do total + zero conversão}
```

Se os breakdowns de público não estiverem disponíveis nos dados retornados pelo Passo 4, informar: "Breakdowns de público não retornaram. Para ver essa análise, use `trafego-insights` com breakdown de age/gender/region."

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0. Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] Ranking das 5 melhores campanhas por ROAS no período
    → coberto? Se não: ordenar campanhas por ROAS e exibir top 5 com gasto, compras e ROAS

[ ] CPM comparativo: período atual vs. anterior (ficou mais caro anunciar?)
    → coberto? Se não: calcular CPM médio dos dois períodos e delta percentual

[ ] Qual posicionamento (Feed, Stories, Reels) traz mais resultado?
    → coberto? Se não: agrupar por publisher_platform + platform_position e comparar CPA de cada combinação

[ ] Funil completo por campanha: impressões → cliques → LPV → conversões
    → coberto? Se não: montar tabela com cada etapa e taxa de passagem entre elas

[ ] Qual público (idade, gênero, região) converte mais barato?
    → coberto? Se não: cruzar breakdowns de idade, gênero e região com CPL/CPA e destacar o mais eficiente
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico**: winner e loser do ranking, posicionamento vencedor, qual etapa do funil é o gargalo principal.
2. **Causa provável**: relação entre os dados. Ex: "CPM subiu 18% e Connect Rate caiu 30%: o leilão está mais caro E a página não converte quem chegou. Dois problemas distintos, não um."
3. **No VTSD, isso significa…**: qual elemento do método está em jogo. Usar a tabela abaixo como guia:

| Gargalo do funil | Elemento VTSD | Interpretação |
|---|---|---|
| Hook Rate baixo | Urgência Oculta | A dor não está sendo ativada no primeiro segundo do criativo |
| CTR baixo | Identidade do Produto | O ângulo do anúncio não comunica o diferencial claramente |
| Connect Rate baixo | Quadro na Parede | O que o anúncio promete não é o que a página entrega |
| Checkout Rate baixo | Oferta | Preço, garantia, bônus ou stack de valor não convencem |
| Conversion Rate baixa | Furadeira + Decorados | O método e os benefícios não estão claros na página de checkout |
| Lead Rate baixa | Isca Digital | A oferta de captura (e-book, aula, etc.) não é atraente o suficiente |

4. **Ação recomendada**: handoff para skill executora com instrução específica.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Top winner com ROAS > 3x e freq < 3 | "trafego-escalar": escalar com cautela |
| Top loser com gasto alto + zero conversão | "trafego-otimizar": pausar com filtro |
| Posicionamento perdedor com gasto > 15% do total | "trafego-testes": criar teste A/B de posicionamento |
| Gargalo em Hook Rate | "trafego-testes": A/B de criativo com nova Urgência Oculta |
| Gargalo em Connect Rate | "trafego-oferta-funil" para confirmar o gargalo; correção em "feedback-pagina" (headline e promessa da página não batem com o anúncio) ou "pagina-performance" (velocidade, URL/redirect) |
| Gargalo em Checkout Rate ou Conversion Rate | "trafego-oferta-funil" para o diagnóstico; correção em "feedback-pagina" ou "pagina-checkout" (oferta, garantia, stack de valor). Low ticket: "feedback-low-ticket" |
| CPM subindo > 20% WoW | Investigar fadiga → output [3] Criativos & Copy |
| Lead Rate baixa | "copy-pagina": revisar isca digital e formulário de captura |

---

## Mapeamento HTML (export via `_export-html.md`)

Componentes definidos na seção 3.2 do `_export-html.md`. **Usar exatamente estes nomes de classe.** O vocabulário antigo (`.kpi-grid`, `.kpi`, `.table`, `.bar-row`, `.callout`, `.pitch-box`, `.up`, `.down`, `--neon`) foi descontinuado e NÃO existe no CSS embutido: usá-lo gera seção sem estilo.

| Bloco do output narrado | Componente do design system |
|---|---|
| KPIs globais (gasto, vendas, receita, ROAS, CPA, CPM) | `.stats-grid` com um `.stat-card` por métrica (`.value.green/.yellow/.red` conforme semântica) |
| Cada "Resposta N" obrigatória | `.section` com `.section-header` (`.section-num` + `.section-title` + `.section-question`) |
| Ranking de winners (top 5) | `.card` + `table`; `.rank` na posição, `.num` nas colunas numéricas, `.ad-name` no nome; ROAS da linha #1 com `style="color:var(--green)"` |
| Ranking de losers (top 5) | `.card` + `table`; linha mais crítica com `.num` em `style="color:var(--red)"` |
| CPM / ROAS atual vs. anterior | `table` comparativa (Métrica · Atual · Anterior · Variação); variação colorida com `style="color:var(--green)"` ou `var(--red)` |
| Tabela de posicionamento | `.card` + `table`; vencedor com `style="color:var(--green)"`, perdedor/queimando com `var(--red)` |
| Funil completo da campanha winner | `.funnel` (`.funnel-stage` + `.funnel-bar` + `.funnel-meta`): uma etapa por nível, taxa de passagem no `.funnel-meta` |
| Interpretação de cada etapa do funil / gargalo | `.diag-box` (azul) ou `.diag-box.yellow/.red` conforme o sinal |
| Frase "No VTSD isso significa..." | `.diag-box` (azul padrão) |
| Ação recomendada | `.action-box` (com `<ol>`/`<li>` se houver passos) |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no `.page-foot` |

### Gráficos obrigatórios deste output

Renderizar todos os gráficos abaixo que tiverem dado real disponível, logo após o `.stats-grid` de KPIs, sob um `.section-h` "Visão visual". Todos em SVG/CSS inline, sem dependência (receitas na seção **3.2.1** e **3.2.1.1** do `_export-html.md`). Se um gráfico depender de dado que a chamada não retornou (ex: breakdown de posicionamento vazio), **omitir só esse gráfico** e seguir com os demais, nunca inventar número.

| Gráfico | Componente / receita | Fonte de dado | Posição |
|---|---|---|---|
| Radar do funil vs. benchmark | SVG radar (receita A) | 5 etapas como % do benchmark: Hook/CTR, CTR-link, Connect Rate, Checkout Rate, Conversion Rate (Fórmulas + tabela de benchmarks da Resposta 4) | `.charts-grid`, 1ª coluna |
| Funil completo da winner | `.funnel` (receita B) | agregado da campanha winner: impressões → cliques link → LPV → vendas | `.charts-grid`, 2ª coluna |
| CPM / CPC / CTR atual vs. anterior | `.wow-chart` (receita C) | Chamada de comparação (período atual × anterior), média ponderada por spend | `.chart-card` full-width sob o `.charts-grid` |
| Posicionamento: vendeu vs. queimou | `.hbar-row` (receita D) | breakdown `platform_position` da Resposta 3: top que converteu (`.win`) vs. top que queimou (`.burn`) | `.chart-card` dentro da Resposta 3 |

Regras dos gráficos: usar só cores da paleta (`--green/--yellow/--orange/--red/--accent`); truncar nomes longos de posicionamento/campanha. **Radar (receita A):** cada vértice é a etapa do funil normalizada ao benchmark (`min(score/benchmark, 1)·100`), cor do vértice pela faixa, verde ≥ 90% do alvo, amarelo 60–89%, vermelho < 60%. **Barras pareadas CPM (receita C):** a barra atual recebe `.bad` (vermelho) quando o CPM/CPC subiu, `.good` (verde) quando caiu; CTR fica `.good` quando subiu; altura normalizada ao maior do par. **Barras horizontais de posicionamento (receita D):** largura proporcional ao spend do posicionamento; `.win` para os que converteram, `.burn` para gasto > 10% do total com zero conversão. O radar usa um `viewBox="0 0 360 300"`, centro `(180,160)`, raio `R=120`; cos/sin dos 5 eixos prontos na receita A (θ0 a θ4).
