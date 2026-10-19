# Output [6]. Investigação Profunda

Análises técnicas que vão além do óbvio: comportamento por dispositivo, fase de aprendizado das campanhas, subida brusca de CPA, retenção de vídeo por posicionamento, janela de decisão do comprador e gargalo entre clique e ação na página.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- "Qual o custo por resultado nas primeiras 24h de cada campanha nova vs. depois que sai do aprendizado?"
- "Meus anúncios performam diferente em mobile vs. desktop?"
- "Tem algum anúncio onde o custo por resultado subiu mais de 50% na última semana?"
- "Qual o tempo médio de visualização dos meus vídeos por posicionamento?"
- "Tem alguma campanha onde estou pagando caro por clique mas ninguém converte na página?"
- "Qual a taxa de rejeição entre clique no anúncio e ação no site?"
- "Quanto tempo em média leva do primeiro clique até a conversão?"

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## Dados necessários

- Breakdown `device_platform` e `impression_device`
- Breakdown `publisher_platform` para tempo de vídeo por posicionamento
- Métricas de vídeo: `video_avg_time_watched_actions`, `video_p25_watched_actions`, `video_p50_watched_actions`, `video_p75_watched_actions`, `video_p100_watched_actions`
- Comparativo: primeiras 24h vs total da campanha (cálculo manual)
- Conversion windows: 1d_click vs 7d_click (revela tempo de decisão)
- Por campanha: `cost_per_inline_link_click` (CPC), `inline_link_clicks`, `actions[purchase]` para calcular taxa de conversão clique → compra

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "Qual o custo por resultado nas primeiras 24h de cada campanha nova vs. depois que sai do aprendizado?"

Aplicar somente a campanhas com `created_time` há mais de 7 dias em relação ao início do período analisado. Campanhas mais recentes estão provavelmente em fase de aprendizado ativo e não têm dado comparativo suficiente.

Para calcular o CPA das "primeiras 24h": usar `time_range` com `since` e `until` correspondendo ao dia de criação da campanha. A data vem da listagem de campanhas (`GET /act_{AD_ACCOUNT_ID_ATUAL}/campaigns?fields=id,name,created_time,start_time`); com ela em mãos, executar a Chamada 6f abaixo com datas manuais. Para o CPA "pós-aprendizado": usar o período selecionado pelo aluno.

**Chamada 6f. Insights das primeiras 24-48h por campanha (executar após obter `created_time`/`start_time` na listagem de campanhas)**

Para cada campanha elegível (com `created_time` há mais de 7 dias), substituir `{DATA_INICIO}` pela data de `start_time` da campanha no formato `YYYY-MM-DD` e `{DATA_INICIO_MAIS_2}` por essa data acrescida de 2 dias:

```bash
# Modo APP (time_range e filtering URL-codificados: since/until soltos são ignorados pelo /insights)
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=campaign_id,campaign_name,spend,impressions,clicks,
          actions,cost_per_action_type
  &level=campaign
  &time_increment=1
  &time_range=%7B%22since%22%3A%22{DATA_INICIO}%22%2C%22until%22%3A%22{DATA_INICIO_MAIS_2}%22%7D
  &filtering=%5B%7B%22field%22%3A%22campaign.id%22%2C%22operator%22%3A%22IN%22%2C%22value%22%3A%5B%22{CAMPAIGN_ID}%22%5D%7D%5D
  &access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

> **Nota de API:** `landing_page_views` é inválido no parâmetro `fields` da Insights API (erro 400). O valor de visualizações da página de destino vem do array `actions` (action_type = `landing_page_view`), já retornado nos campos acima.

`time_increment=1` retorna uma linha por dia. Somar os dias dentro da janela para obter o CPA acumulado das primeiras 24-48h. Cruzar com o CPA do período completo (Chamada principal) para calcular a variação de aprendizado.

**Modo MCP_CONECTOR:** usar `mcp__*__ads_get_ad_entities` em nível campanha (`level: "campaign"`, filtro `{field: "campaign.id", operator: "IN", value: ["{CAMPAIGN_ID}"]}`, `time_increment: "1"`) com o intervalo dos 2 primeiros dias de cada campanha em `time_range` **como texto JSON** (`"{\"since\":\"{DATA_INICIO}\",\"until\":\"{DATA_INICIO_MAIS_2}\"}"`, ver Contrato anti-erros), uma chamada por campanha elegível. A `ads_insights_performance_trend` não serve aqui: ela não faz nível campanha (ver **Contrato anti-erros** no `SKILL.md`).

```
🎓 FASE DE APRENDIZADO  ·  {período}

  Campanha                CPA primeiras 24h   CPA pós-aprendizado   Variação
  ──────────────────────────────────────────────────────────────────────────
  {nome}                  R$ {X}              R$ {Y}                {-Z%}
  {nome}                  R$ {X}              R$ {Y}                {+Z%}
  ...

  Leitura:
```

| Variação do CPA após aprendizado | Classificação | O que significa |
|---|---|---|
| Queda > 30% | 🟢 Saudável | Algoritmo encontrou o público. Manter e monitorar |
| Queda de 10% a 30% | 🟡 Convergência parcial | Possível melhora com ajuste de audiência |
| Estável (±10%) | 🟠 Atenção | Aprendizado não convergiu: estrutura da campanha pode estar limitando |
| Alta > 10% | 🔴 Problemas | Criativo fraco, segmentação errada ou pixel misconfigured |

Se o período selecionado for menor que 7 dias, suprimir esta seção e informar: "Período insuficiente para análise de aprendizado. Selecione ao menos 14 dias para ver essa comparação."

---

### Resposta 2. "Meus anúncios performam diferente em mobile vs. desktop?"

Dados vêm da chamada de insights com breakdown `device_platform` (mesmos campos da chamada principal, acrescentando `breakdowns=device_platform`). Separar por objetivo da campanha dominante na conta.

#### Template A. Venda direta (OUTCOME_SALES)

```
📱 DISPOSITIVO  ·  {período}  ·  Métrica: ROAS / CPA

  Dispositivo        Spend       CPA         ROAS    CTR     LP Views
  ────────────────────────────────────────────────────────────────────
  Mobile (app)       R$ {X}      R$ {Y}      {Z}x    {W%}    {N}
  Mobile (web)       R$ {X}      R$ {Y}      {Z}x    {W%}    {N}
  Desktop            R$ {X}      R$ {Y}      {Z}x    {W%}    {N}
  Connected TV       R$ {X}      R$ {Y}      {Z}x    {W%}    {N}

  Vencedor: {dispositivo}, CPA {X%} abaixo da média
  Perdedor: {dispositivo}, CPA {X%} acima da média
```

#### Template B. Captação de leads (OUTCOME_LEADS)

```
📱 DISPOSITIVO  ·  {período}  ·  Métrica: CPL

  Dispositivo        Spend       CPL         Leads   CTR     LP Views
  ────────────────────────────────────────────────────────────────────
  Mobile (app)       R$ {X}      R$ {Y}      {N}     {W%}    {N}
  Mobile (web)       R$ {X}      R$ {Y}      {N}     {W%}    {N}
  Desktop            R$ {X}      R$ {Y}      {N}     {W%}    {N}
  Connected TV       R$ {X}      R$ {Y}      {N}     {W%}    {N}

  Vencedor: {dispositivo}, CPL {X%} abaixo da média
  Perdedor: {dispositivo}, CPL {X%} acima da média
```

---

### Resposta 3. "Tem algum anúncio onde o custo por resultado subiu mais de 50% na última semana?"

Comparar o CPA de cada anúncio na semana atual com o da semana anterior (duas janelas consecutivas da mesma chamada de insights) e listar os que subiram mais de 50%.

#### Template A. Venda direta (OUTCOME_SALES)

```
⚠️ ANÚNCIOS COM CPA EM ALTA  ·  variação WoW > +50%

  Anúncio              Campanha            CPA atual    CPA anterior   Variação
  ──────────────────────────────────────────────────────────────────────────────
  {nome}               {campanha}          R$ {X}       R$ {Y}         +{Z%}
  {nome}               {campanha}          R$ {X}       R$ {Y}         +{Z%}
  ...
```

#### Template B. Captação de leads (OUTCOME_LEADS)

```
⚠️ ANÚNCIOS COM CPL EM ALTA  ·  variação WoW > +50%

  Anúncio              Campanha            CPL atual    CPL anterior   Variação
  ──────────────────────────────────────────────────────────────────────────────
  {nome}               {campanha}          R$ {X}       R$ {Y}         +{Z%}
  ...
```

**Para cada anúncio listado**, cruzar com a frequência do conjunto de anúncios (disponível no Passo 4) para determinar hipótese:

| Frequência do conjunto | Hipótese principal |
|---|---|
| ≥ 4 | Fadiga de criativo: mesmo público viu muitas vezes |
| < 4 e CPA subindo | Perda de relevância no leilão (quality ranking caindo) |
| < 4 e CTR caindo | Saturação do ângulo: novo Decorado ou Urgência Oculta necessário |

Se nenhum anúncio tiver variação WoW > +50%, informar: "Nenhum anúncio com subida brusca de CPA/CPL no período. Conta estável nessa dimensão."

---

### Resposta 4. "Qual o tempo médio de visualização dos meus vídeos por posicionamento?"

Dados vêm da chamada de insights com breakdown `publisher_platform` e os campos de vídeo (`video_avg_time_watched_actions`, `video_p25_watched_actions`, `video_p50_watched_actions`, `video_p75_watched_actions`, `video_p100_watched_actions`). Omitir esta seção se nenhuma campanha tiver vídeo.

```
🎬 RETENÇÃO DE VÍDEO  ·  {período}

  Posicionamento      Avg watch time   Hook (25%)   Hold (50%)   Play-through (100%)
  ─────────────────────────────────────────────────────────────────────────────────
  Instagram Reels     {X}s             {Y%}         {Z%}         {W%}
  Instagram Stories   {X}s             {Y%}         {Z%}         {W%}
  Facebook Feed       {X}s             {Y%}         {Z%}         {W%}
  In-stream Video     {X}s             {Y%}         {Z%}         {W%}
  (outros se houver)

  Melhor retenção: {posicionamento}, público engaja mais com o criativo neste formato
  Pior retenção:   {posicionamento}, criativo provavelmente não foi adaptado para o formato
```

#### Benchmarks de retenção por métrica

| Métrica | 🔴 Baixo | 🟡 Atenção | 🟢 Saudável |
|---|---|---|---|
| Hook Rate (25%) | < 15% | 15% a 25% | > 25% |
| Hold Rate (50%) | < 8% | 8% a 15% | > 15% |
| Play-through (100%) | < 3% | 3% a 8% | > 8% |

**Interpretação no VTSD:** Hook Rate baixo no Reels indica que os primeiros 3 segundos não ativam a Urgência Oculta. Hold Rate baixo indica que os Decorados (benefícios encadeados) não estão sendo comunicados no formato vertical curto. Play-through baixo indica que a Furadeira (método) não está sendo percebida como suficientemente relevante para assistir até o fim.

---

### Resposta 5. "Tem alguma campanha onde estou pagando caro por clique mas ninguém converte na página?"

Dados vêm da chamada principal: cliques no link = `link_click` do array `actions` (ou `inline_link_clicks`), nunca o campo de topo `clicks`, que soma cliques em qualquer parte do post e derruba o connect rate; visitas = `landing_page_view` do array `actions`; custos de `cost_per_action_type`. Se `link_click` não vier, usar `clicks` só como último recurso e avisar o aluno que o connect rate sai subestimado. No modo MCP, usar direto os campos `link_click` e `landing_page_view` do `ads_get_ad_entities`.

```
🚪 GARGALO CLIQUE → PÁGINA  ·  {período}

  Total de cliques (link):       {N}
  LP views rastreadas:           {M}
  Connect Rate:                  {X%}  (M/N)
  Abandono antes de carregar:    {Z%}  (1 - Connect Rate)
```

**Cruzamento obrigatório com CPC efetivo:**

```
  CPC efetivo médio:   R$ {X}  (spend / link_click)
  Connect Rate:        {Y%}
  Custo por LP view:   R$ {Z}  (spend / landing_page_views)

  {emoji}  Leitura: {interpretação automática conforme quadrante abaixo}
```

| CPC efetivo | Connect Rate | Quadrante | O que significa |
|---|---|---|---|
| Alto (> R$ 3) | Baixo (< 80%) | 🔴 Dupla ineficiência | Paga caro pelo clique E perde visitante antes de a página carregar. Dois problemas distintos |
| Alto (> R$ 3) | Alto (80% ou mais) | 🟡 Caro mas funciona | Leilão caro: investigar CPM e sazonalidade no output [2] |
| Baixo (≤ R$ 3) | Baixo (< 80%) | 🟠 Problema de página | Clique barato mas a página perde o visitante: auditar velocidade |
| Baixo (≤ R$ 3) | Alto (80% ou mais) | 🟢 Eficiente | Tráfego qualificado chegando. Próximo gargalo está na conversão |

Connect Rate pela régua única do projeto (a mesma da §3.5 de `trafego-oferta-funil/SKILL.md`): 80% ou mais saudável, 60% a 79% atenção, abaixo de 60% crítico. Abaixo de 70%, a primeira hipótese é técnica (página lenta, link errado, redirecionamento): conferir com `/pagina-performance` e a congruência anúncio x página com `/trafego-oferta-funil` antes de mexer no anúncio.

**Cruzamento complementar: clique caro sem compra** (independe de LP views). Filtrar campanhas com `cost_per_inline_link_click` > 2× benchmark do nicho E taxa de conversão (purchases / inline_link_clicks) < 1%:

```
💸 CLIQUE CARO SEM COMPRA

| Campanha | Spend | CPC | Cliques | Compras | Conv. Rate | ROAS |
|----------|-------|-----|---------|---------|-----------|------|
| {nome}   | R$ X  | R$Y | N       | 0       | 0%        | 0×   |
...

Leitura:
- CPC alto + conv. rate baixo = promessa do anúncio não está alinhada com a página de destino
- CPC alto + zero compras = público errado ou oferta não ressoa após o clique
```

Se `landing_page_views` não retornar (pixel sem evento de LP view configurado): suprimir os blocos de Connect Rate acima (manter o cruzamento complementar) e alertar: "LP views não rastreado. Sem essa métrica, não é possível identificar abandono entre clique e página. Configurar via 'trafego-pixel'."

---

### Resposta 6. "Qual a taxa de rejeição entre clique no anúncio e ação no site?"

Dados vêm de `link_click` e `landing_page_view` (array `actions`) da chamada principal, com a mesma regra da Resposta 5: nunca o campo de topo `clicks` (complementam a Resposta 5 com foco na taxa de abandono por campanha individual).

| Connect Rate | Classificação | Hipótese principal |
|---|---|---|
| 80% ou mais | 🟢 Saudável | Página carrega rápido e URL está correta |
| 70% a 79% | 🟡 Atenção | Monitorar: possível lentidão pontual |
| 60% a 69% | 🟠 Atenção (primeira hipótese técnica) | Página lenta, link errado ou redirecionamento: conferir com `/pagina-performance` e a congruência com `/trafego-oferta-funil` antes de mexer no anúncio |
| < 60% | 🔴 Crítico | URL do anúncio quebrada, redirect em loop, página muito lenta ou bloqueada |

Aplicar a tabela de classificação acima para cada campanha individualmente e sinalizar as que estiverem abaixo de 70% (primeira hipótese técnica), com prioridade para as abaixo de 60%. Se `landing_page_views` não retornar, indicar a mesma limitação da Resposta 5.

---

### Resposta 7. "Quanto tempo em média leva do primeiro clique até a conversão?"

Dados vêm da chamada de insights com comparação de janelas de atribuição (`action_attribution_windows=['1d_click','7d_click']` sobre as mesmas ações de conversão da chamada principal). Usar tipos canônicos conforme objetivo.

```
⏱️ TEMPO DE DECISÃO  ·  {período}

  Conversões em até 1 dia (1d_click):        {N}
  Conversões em até 7 dias (7d_click):       {M}  ← inclui as {N} acima
  Conversões entre dia 1 e dia 7 (delta):    {M-N}

  {X%} do total fechou no mesmo dia do clique
  {Z%} precisou de 1 a 7 dias para decidir
```

| Perfil de decisão | Critério | Implicação para o funil |
|---|---|---|
| Produto de impulso | > 70% em 1d_click | Oferta direta funciona. Retargeting é residual |
| Produto misto | 40% a 70% em 1d_click | Combinar campanha fria + retargeting de 3-7 dias |
| Produto de consideração | < 40% em 1d_click | Retargeting é decisivo. Sem ele, metade da receita some |

**Nota:** a API retorna contagens por janela (1d_click, 7d_click, 28d_click), não a janela média ponderada diretamente. A "janela predominante" é inferida pela maior contagem: não é um valor exato.

**Se o produto for de consideração** e não houver campanha de remarketing ativa (verificar pelo objetivo das campanhas no Passo 4): recomendar criar audience de retargeting via "trafego-publicos" e campanha via "trafego-testes" (fluxo de campanha de remarketing).

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0. Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] Custo por resultado nas primeiras 24h vs. depois do aprendizado?
    → coberto? Se não: separar campanhas novas (< 7 dias) de maduras (> 30 dias) e comparar CPA médio de cada grupo

[ ] Anúncios performam diferente em mobile vs. desktop?
    → coberto? Se não: agrupar por device_platform e comparar CPA, CTR e taxa de conversão de cada dispositivo

[ ] Algum anúncio com custo por resultado subiu mais de 50% WoW?
    → coberto? Se não: calcular variação de CPA semana atual vs. anterior por campanha e sinalizar os que ultrapassaram 50%

[ ] Tempo médio de visualização dos vídeos por posicionamento?
    → coberto? Se não: cruzar video_avg_time_watched com publisher_platform e comparar retenção por canal

[ ] Campanha pagando caro por clique mas sem conversão na página?
    → coberto? Se não: calcular connect_rate (LPV / link_clicks) por campanha e sinalizar as com connect_rate < 70% (crítico abaixo de 60%)

[ ] Taxa de rejeição entre clique no anúncio e ação no site?
    → coberto? Se não: calcular bounce_rate = (link_clicks - LPV) / link_clicks por campanha

[ ] Quanto tempo leva do primeiro clique até a conversão?
    → coberto? Se não: verificar janela de atribuição configurada e estimar tempo médio de conversão com base nos dados disponíveis
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico**: enumerar os achados de cada bloco: fase de aprendizado das campanhas, dispositivo vencedor e perdedor, anúncios com CPA em alta, posicionamento de melhor retenção de vídeo, perfil de decisão do comprador, connect rate.
2. **Causa provável**: relação entre os achados. Exemplos: "aprendizado não convergiu + CPA subindo + Connect Rate baixo = problema de página, não de anúncio ou público"; "decisão > 5 dias + sem campanha de remarketing ativa = metade da receita potencial sendo ignorada".
3. **No VTSD, isso significa…**: usar os elementos do método como âncora:
   - Hook Rate baixo = Urgência Oculta não ativada nos primeiros 3 segundos
   - Hold Rate baixo = Decorados não estão sendo percebidos no formato
   - Dispositivo perdedor com gasto alto = Identidade do Consumidor não mapeou comportamento de dispositivo
   - Produto de consideração sem retargeting = Furadeira (método) precisa de mais toques para convencer
   - Connect Rate baixo = o Quadro na Parede (promessa) do anúncio não é coerente com a experiência da página
4. **Ação recomendada**: 1 a 3 ações concretas com handoff para a skill executora.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Aprendizado não convergiu (CPA subiu após aprendizado) | "trafego-otimizar": diagnóstico de gargalo + "trafego-publicos" (nova audiência) |
| Dispositivo perdedor com gasto > 15% do total | "trafego-testes": A/B de posicionamento excluindo dispositivo |
| Anúncio com CPA WoW > +50% e freq ≥ 4 | "trafego-testes": A/B de criativo com nova Urgência Oculta |
| Anúncio com CPA WoW > +50% e freq < 4 | "trafego-otimizar": pausar anúncio específico |
| Hold Rate < 8% em Reels | "copy-anuncio": reescrever criativo adaptado para formato vertical curto com Decorados nos primeiros 10s (vídeo: "video-editar" ou "video-remotion") |
| Produto de consideração sem retargeting | "trafego-publicos" (criar audience de visitantes) + "trafego-testes" (campanha de remarketing) |
| Connect Rate < 70% | "pagina-performance": auditar velocidade, link e redirecionamento do anúncio ("trafego-oferta-funil" para conferir a congruência anúncio x página), antes de mexer no anúncio |
| CPC alto + Connect Rate baixo | "pagina-performance" (velocidade) e output [2] (CPM do leilão): problemas distintos |
| Pixel sem LP view configurado | "trafego-pixel": configurar evento de landing page view |

---

## Mapeamento HTML (export via `_export-html.md`)

Componentes definidos na seção 3.2 do `_export-html.md`. **Usar exatamente estes nomes de classe.** O vocabulário antigo (`.table`, `.kpi-grid`, `.kpi`, `.regra`, `.regra.alerta`, `.callout`, `.pitch-box`, `.bar-row`, `.up`, `.down`) foi descontinuado e NÃO existe no CSS embutido: usá-lo gera seção sem estilo.

| Bloco do output narrado | Componente do design system |
|---|---|
| KPIs globais (gasto, CPA/CPL, ROAS, Connect Rate, CPC efetivo, dispositivo vencedor) | `.stats-grid` com um `.stat-card` por métrica (`.value.green/.yellow/.red` conforme semântica) |
| Cada "Resposta N" obrigatória | `.section` com `.section-header` (`.section-num` + `.section-title` + `.section-question`, texto exato da pergunta) |
| Tabela de aprendizado (Resposta 1) | `.card` + `table`; variação de CPA colorida com `style="color:var(--green)"` (queda) ou `var(--red)` (alta) |
| Tabela de dispositivos (Resposta 2) | `.card` + `table`; CPA do vencedor em `var(--green)`, do perdedor em `var(--red)` |
| Alerta dispositivo queimando | `.diag-box.red` |
| Tabela de anúncios com CPA em alta (Resposta 3) | `.card` + `table`; coluna de variação em `var(--red)` |
| Tabela de retenção de vídeo (Resposta 4) | `.card` + `table`; ou `.fmt-compare`/`.funnel-row` por posicionamento, cores conforme benchmark |
| Painel de janela de decisão (Resposta 7) | `.card` + `.funnel-row` com 3 `.funnel-item` (1d, 7d, delta) |
| Perfil de decisão (impulso vs. consideração) | `.diag-box` com a classificação |
| Connect Rate + CPC efetivo (Respostas 5 e 6) | `.card` + `.funnel-row`/`.stat-card`, valores com cor semântica |
| Quadrante CPC × Connect Rate | `.diag-box` (+ `.green/.yellow/.red` conforme quadrante) com a interpretação |
| Frase "No VTSD isso significa..." | `.diag-box` (+ `.green/.yellow/.red` conforme o sinal) |
| Ação recomendada | `.action-box` |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no `.page-foot` |

### Gráficos obrigatórios deste output

Renderizar os gráficos abaixo logo após o `.stats-grid` de KPIs, sob um `.section-h` "Visão visual". Todos em SVG/CSS inline, sem dependência (receitas detalhadas nas seções **3.2.1** e **3.2.1.1** do `_export-html.md`). Geometria não trivial usa o helper `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py` (matemática pura, sem token, sem Graph API).

| Gráfico | Componente / receita | Fonte de dado | Posição |
|---|---|---|---|
| Scatter CPC × Connect Rate por campanha | SVG scatter com quadrantes (receita K via helper `scatter`) | por campanha: `cost_per_inline_link_click` (eixo X) × Connect Rate `landing_page_view`/`link_click` (eixo Y); `x_mid`/`y_mid` = mediana de cada eixo | `.chart-card` full-width, topo da "Visão visual" |
| CPA mobile × desktop | SVG barras pareadas / barras verticais (receita G via helper `vbars`) | breakdown `device_platform`: CPA por dispositivo | `.charts-grid`, junto da Resposta 2 |
| Retenção de vídeo por posicionamento | SVG barras verticais (receita G via helper `vbars`) OU `.funnel` (receita B) por posicionamento | breakdown `publisher_platform` + `video_p25/p50/p100_watched_actions` | `.charts-grid`, junto da Resposta 4: **omitir se nenhuma campanha tiver vídeo** |

**Regras do scatter (quadrante):** colorir cada ponto pela zona desejada: quadrante de CPC baixo + Connect Rate alto é o bom (verde); CPC alto + Connect Rate baixo é a dupla ineficiência (vermelho); os outros dois ficam amarelos. As linhas de quadrante (`x_mid_px`/`y_mid_px`) vêm da mediana de cada eixo: calcular a mediana dos pontos e passar como `x_mid`/`y_mid` no spec (o helper só converte para pixels). Não escolher cutoff arbitrário. Raio `r` opcionalmente proporcional ao spend da campanha (limitar a 4–10 px para não estourar). Se `landing_page_view` não retornar para nenhuma campanha (pixel sem evento de LP view), omitir o scatter e os gráficos que dependem de Connect Rate, documentando a limitação no chat.

**Regras das vbars de dispositivo e vídeo:** CPA é "quanto menor melhor" → colorir verde o dispositivo de menor CPA e vermelho o de maior. Para retenção de vídeo, percentual é "quanto maior melhor" → verde acima do benchmark saudável, vermelho abaixo. Usar só cores da paleta (`--green/--yellow/--orange/--red/--accent`); truncar nomes longos de campanha no scatter.
