# Output [6] — Investigação Profunda

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

Para calcular o CPA das "primeiras 24h": usar `since/until` correspondendo ao dia de criação da campanha (Chamada 6e + chamada adicional com datas manuais). Para o CPA "pós-aprendizado": usar o período selecionado pelo aluno.

**Chamada 6f — Insights das primeiras 24-48h por campanha (executar após Chamada 6e)**

Para cada campanha elegível (com `created_time` há mais de 7 dias), substituir `{DATA_INICIO}` pela data de `start_time` da campanha no formato `YYYY-MM-DD` e `{DATA_INICIO_MAIS_2}` por essa data acrescida de 2 dias:

```bash
# Modo APP
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=campaign_id,campaign_name,spend,impressions,clicks,
          actions,cost_per_action_type,landing_page_views
  &level=campaign
  &time_increment=1
  &since={DATA_INICIO}&until={DATA_INICIO_MAIS_2}
  &filtering=[{'field':'campaign.id','operator':'IN','value':['{CAMPAIGN_ID}']}]
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

`time_increment=1` retorna uma linha por dia. Somar os dias dentro da janela para obter o CPA acumulado das primeiras 24-48h. Cruzar com o CPA do período completo (Chamada principal) para calcular a variação de aprendizado.

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` com `time_increment=1` e filtro de `since/until` correspondendo aos 2 primeiros dias de cada campanha.

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
| Estável (±10%) | 🟠 Atenção | Aprendizado não convergiu — estrutura da campanha pode estar limitando |
| Alta > 10% | 🔴 Problemas | Criativo fraco, segmentação errada ou pixel misconfigured |

Se o período selecionado for menor que 7 dias, suprimir esta seção e informar: "Período insuficiente para análise de aprendizado. Selecione ao menos 14 dias para ver essa comparação."

---

### Resposta 2. "Meus anúncios performam diferente em mobile vs. desktop?"

Dados vêm da Chamada 6a (breakdown `device_platform`). Separar por objetivo da campanha dominante na conta.

#### Template A — Venda direta (OUTCOME_SALES)

```
📱 DISPOSITIVO  ·  {período}  ·  Métrica: ROAS / CPA

  Dispositivo        Spend       CPA         ROAS    CTR     LP Views
  ────────────────────────────────────────────────────────────────────
  Mobile (app)       R$ {X}      R$ {Y}      {Z}x    {W%}    {N}
  Mobile (web)       R$ {X}      R$ {Y}      {Z}x    {W%}    {N}
  Desktop            R$ {X}      R$ {Y}      {Z}x    {W%}    {N}
  Connected TV       R$ {X}      R$ {Y}      {Z}x    {W%}    {N}

  Vencedor: {dispositivo} — CPA {X%} abaixo da média
  Perdedor: {dispositivo} — CPA {X%} acima da média
```

### Bloco 4. CPC caro sem conversão (Q5)
Filtrar campanhas com `cost_per_inline_link_click` > 2× benchmark do nicho E taxa de conversão (purchases / inline_link_clicks) < 1%:
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

---

### Bloco 5. Tempo de vídeo por posicionamento
```
📱 DISPOSITIVO  ·  {período}  ·  Métrica: CPL

  Dispositivo        Spend       CPL         Leads   CTR     LP Views
  ────────────────────────────────────────────────────────────────────
  Mobile (app)       R$ {X}      R$ {Y}      {N}     {W%}    {N}
  Mobile (web)       R$ {X}      R$ {Y}      {N}     {W%}    {N}
  Desktop            R$ {X}      R$ {Y}      {N}     {W%}    {N}
  Connected TV       R$ {X}      R$ {Y}      {N}     {W%}    {N}

  Vencedor: {dispositivo} — CPL {X%} abaixo da média
  Perdedor: {dispositivo} — CPL {X%} acima da média
```

### Bloco 6. Tempo do primeiro clique até conversão
Comparar atribuição 1d_click vs 7d_click:
```
⚠️ ANÚNCIOS COM CPA EM ALTA  ·  variação WoW > +50%

  Anúncio              Campanha            CPA atual    CPA anterior   Variação
  ──────────────────────────────────────────────────────────────────────────────
  {nome}               {campanha}          R$ {X}       R$ {Y}         +{Z%}
  {nome}               {campanha}          R$ {X}       R$ {Y}         +{Z%}
  ...
```

#### Template B — Captação de leads (OUTCOME_LEADS)

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
| ≥ 4 | Fadiga de criativo — mesmo público viu muitas vezes |
| < 4 e CPA subindo | Perda de relevância no leilão (quality ranking caindo) |
| < 4 e CTR caindo | Saturação do ângulo — novo Decorado ou Urgência Oculta necessário |

Se nenhum anúncio tiver variação WoW > +50%, informar: "Nenhum anúncio com subida brusca de CPA/CPL no período. Conta estável nessa dimensão."

---

### Resposta 4. "Qual o tempo médio de visualização dos meus vídeos por posicionamento?"

Dados vêm da Chamada 6c. Omitir esta seção se nenhuma campanha tiver vídeo.

```
🎬 RETENÇÃO DE VÍDEO  ·  {período}

  Posicionamento      Avg watch time   Hook (25%)   Hold (50%)   Play-through (100%)
  ─────────────────────────────────────────────────────────────────────────────────
  Instagram Reels     {X}s             {Y%}         {Z%}         {W%}
  Instagram Stories   {X}s             {Y%}         {Z%}         {W%}
  Facebook Feed       {X}s             {Y%}         {Z%}         {W%}
  In-stream Video     {X}s             {Y%}         {Z%}         {W%}
  (outros se houver)

  Melhor retenção: {posicionamento} — público engaja mais com o criativo neste formato
  Pior retenção:   {posicionamento} — criativo provavelmente não foi adaptado para o formato
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

Dados vêm dos campos `clicks`, `landing_page_views` e `cost_per_action_type` da chamada principal.

```
🚪 GARGALO CLIQUE → PÁGINA  ·  {período}

  Total de cliques (link):       {N}
  LP views rastreadas:           {M}
  Connect Rate:                  {X%}  (M/N)
  Abandono antes de carregar:    {Z%}  (1 - Connect Rate)
```

**Cruzamento obrigatório com CPC efetivo:**

```
  CPC efetivo médio:   R$ {X}  (spend / cliques)
  Connect Rate:        {Y%}
  Custo por LP view:   R$ {Z}  (spend / landing_page_views)

  {emoji}  Leitura: {interpretação automática conforme quadrante abaixo}
```

| CPC efetivo | Connect Rate | Quadrante | O que significa |
|---|---|---|---|
| Alto (> R$ 3) | Baixo (< 50%) | 🔴 Dupla ineficiência | Paga caro pelo clique E a página não carrega. Dois problemas distintos |
| Alto (> R$ 3) | Alto (> 70%) | 🟡 Caro mas funciona | Leilão caro — investigar CPM e sazonalidade no output [2] |
| Baixo (≤ R$ 3) | Baixo (< 50%) | 🟠 Problema de página | Clique barato mas a página perde o visitante — auditar velocidade |
| Baixo (≤ R$ 3) | Alto (> 70%) | 🟢 Eficiente | Tráfego qualificado chegando. Próximo gargalo está na conversão |

Se `landing_page_views` não retornar (pixel sem evento de LP view configurado): suprimir esta seção e alertar: "LP views não rastreado — sem essa métrica, não é possível identificar abandono entre clique e página. Configurar no Gerenciador de Eventos."

---

### Resposta 6. "Qual a taxa de rejeição entre clique no anúncio e ação no site?"

Dados vêm dos campos `clicks` e `landing_page_views` da chamada principal (complementam a Resposta 5 com foco na taxa de abandono por campanha individual).

| Connect Rate | Classificação | Hipótese principal |
|---|---|---|
| > 70% | 🟢 Saudável | Página carrega rápido e URL está correta |
| 50% a 70% | 🟡 Atenção | Monitorar — possível lentidão pontual |
| 30% a 50% | 🟠 Atenção alta | Página lenta ou redirect com problema |
| < 30% | 🔴 Crítico | URL do anúncio quebrada, redirect em loop ou página bloqueada |

Aplicar a tabela de classificação acima para cada campanha individualmente e sinalizar as que estiverem abaixo de 50%. Se `landing_page_views` não retornar, indicar a mesma limitação da Resposta 5.

---

### Resposta 7. "Quanto tempo em média leva do primeiro clique até a conversão?"

Dados vêm da Chamada 6d. Usar tipos canônicos conforme objetivo.

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

**Nota:** a API retorna contagens por janela (1d_click, 7d_click, 28d_click), não a janela média ponderada diretamente. A "janela predominante" é inferida pela maior contagem — não é um valor exato.

**Se o produto for de consideração** e não houver campanha de remarketing ativa (verificar pelo objetivo das campanhas no Passo 4): recomendar criar audience de retargeting no Gerenciador de Audiences e campanha duplicando entidade no Gerenciador (variando 1 dimensão) (fluxo de campanha de remarketing).

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0 — Checklist antes de montar qualquer bloco

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
    → coberto? Se não: calcular connect_rate (LPV / link_clicks) por campanha e sinalizar as com connect_rate < 30%

[ ] Taxa de rejeição entre clique no anúncio e ação no site?
    → coberto? Se não: calcular bounce_rate = (link_clicks - LPV) / link_clicks por campanha

[ ] Quanto tempo leva do primeiro clique até a conversão?
    → coberto? Se não: verificar janela de atribuição configurada e estimar tempo médio de conversão com base nos dados disponíveis
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico** — enumerar os achados de cada bloco: fase de aprendizado das campanhas, dispositivo vencedor e perdedor, anúncios com CPA em alta, posicionamento de melhor retenção de vídeo, perfil de decisão do comprador, connect rate.
2. **Causa provável** — relação entre os achados. Exemplos: "aprendizado não convergiu + CPA subindo + Connect Rate baixo = problema de página, não de anúncio ou público"; "decisão > 5 dias + sem campanha de remarketing ativa = metade da receita potencial sendo ignorada".
3. **No VTSD, isso significa…** — usar os elementos do método como âncora:
   - Hook Rate baixo = Urgência Oculta não ativada nos primeiros 3 segundos
   - Hold Rate baixo = Decorados não estão sendo percebidos no formato
   - Dispositivo perdedor com gasto alto = Identidade do Consumidor não mapeou comportamento de dispositivo
   - Produto de consideração sem retargeting = Furadeira (método) precisa de mais toques para convencer
   - Connect Rate baixo = o Quadro na Parede (promessa) do anúncio não é coerente com a experiência da página
4. **Ação recomendada** — 1 a 3 ações concretas com handoff para a skill executora.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Aprendizado não convergiu (CPA subiu após aprendizado) | "trafego-otimizar" — diagnóstico de gargalo + Gerenciador de Audiences (nova audiência) |
| Dispositivo perdedor com gasto > 15% do total | Duplicar entidade no Gerenciador (variando 1 dimensão) — A/B de posicionamento excluindo dispositivo |
| Anúncio com CPA WoW > +50% e freq ≥ 4 | Duplicar entidade no Gerenciador (variando 1 dimensão) — A/B de criativo com nova Urgência Oculta |
| Anúncio com CPA WoW > +50% e freq < 4 | "trafego-otimizar" — pausar anúncio específico |
| Hold Rate < 8% em Reels | "copy-anuncio" — reescrever criativo adaptado para formato vertical curto com Decorados nos primeiros 10s |
| Produto de consideração sem retargeting | Gerenciador de Audiences (criar audience de visitantes) + Duplicar entidade no Gerenciador (variando 1 dimensão) (campanha de remarketing) |
| Connect Rate < 30% | "pagina-performance" — auditar velocidade e URL do anúncio |
| CPC alto + Connect Rate baixo | "pagina-performance" (velocidade) e output [2] (CPM do leilão) — problemas distintos |
| Pixel sem LP view configurado | Gerenciador de Eventos — configurar evento de landing page view |

---

## Mapeamento HTML (export via `_export-html.md`)

| Bloco do output narrado | Componente do design system |
|---|---|
| Tabela de aprendizado (Bloco 1) | `.table` com colunas `.up` (queda de CPA) ou `.down` (alta de CPA) |
| Tabela de dispositivos (Bloco 2) | `.table` com destaque `.up` no vencedor e `.down` no perdedor |
| Alerta dispositivo queimando | `.regra.alerta` |
| Tabela de anúncios com CPA em alta (Bloco 3) | `.table` com coluna `.down` na variação |
| Tabela de retenção de vídeo (Bloco 4) | `.table` com colunas coloridas conforme benchmark (`.up`/`.down`) |
| Barras de Hook/Hold/Play-through por posicionamento | série de `.bar-row` — largura proporcional ao percentual, cor conforme benchmark |
| Painel de janela de decisão (Bloco 5) | `.kpi-grid` com 3 `.kpi` (1d, 7d, delta) |
| Perfil de decisão (impulso vs. consideração) | `.callout` com classificação |
| Connect Rate + CPC efetivo (Bloco 6) | `.kpi` duplo com `.up`/`.down` |
| Quadrante CPC × Connect Rate | `.callout` com interpretação do quadrante |
| Frase "No VTSD isso significa..." | `.callout` |
| Ação recomendada | `.pitch-box` |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no rodapé |
