# Output [2] — Performance & Funil

Visão narrada de **performance comparada e mapa de funil** para um período. O aluno entende quem é melhor, quem é pior, e onde o funil vaza.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- “Me dá um ranking das 5 melhores campanhas por ROAS dos últimos 30 dias”
- “Compara o CPM desse mês vs. mês anterior — ficou mais caro anunciar?”
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

**`landing_page_views` NÃO é um campo válido no parâmetro `fields` da Insights API** — causa erro 400 imediato.
O valor de LP views vem do array `actions` com `action_type = "landing_page_view"`:

```python
lp_views = next((float(a['value']) for a in actions if a['action_type'] == 'landing_page_view'), 0)
```

`outbound_clicks` é um campo válido (retorna lista — pegar `[0]['value']` se existir).
Os rankings de qualidade (`quality_ranking`, `engagement_rate_ranking`, `conversion_rate_ranking`) estão disponíveis apenas no nível `ad`, não no nível `campaign`. Omitir na chamada de nível campanha.

### Chamada adicional — Comparativo CPM e ROAS (período anterior)

Para responder "CPM de maio vs. abril ficou mais caro?", fazer **duas chamadas curl separadas** — uma por período.

**Regras obrigatórias:**
- Usar `time_range` como JSON (não `since`/`until` direto no urlencode — causa comportamento imprevisível).
- **NÃO usar `effective_status` nas chamadas de comparação** — com `effective_status`, a API ignora a janela histórica e retorna sempre o estado atual, fazendo ambos os períodos retornarem dados idênticos.
- Calcular as datas em **chamadas Bash separadas** com `date` (nunca em script Python heredoc — ver regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md).

#### Padrão obrigatório (modo APP)

**Passo 1 — Calcular as 4 datas em chamadas `Bash(date ...)` separadas:**

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

**Passo 2 — Disparar 2 chamadas curl separadas (cada uma é uma `Bash(curl ...)` independente):**

```
curl -s "https://graph.facebook.com/v21.0/act_<ACCOUNT_ID>/insights?fields=campaign_id,campaign_name,spend,impressions,cpm,actions,action_values&level=campaign&time_range=%7B%22since%22%3A%22<atual_de>%22%2C%22until%22%3A%22<atual_ate>%22%7D&limit=500&access_token=<TOKEN_DO_ENV>"
```

```
curl -s "https://graph.facebook.com/v21.0/act_<ACCOUNT_ID>/insights?fields=campaign_id,campaign_name,spend,impressions,cpm,actions,action_values&level=campaign&time_range=%7B%22since%22%3A%22<ant_de>%22%2C%22until%22%3A%22<ant_ate>%22%7D&limit=500&access_token=<TOKEN_DO_ENV>"
```

Notar o `time_range` URL-encoded: `%7B` é `{`, `%22` é `"`, `%2C` é `,`, `%7D` é `}`. URL final é `time_range={"since":"YYYY-MM-DD","until":"YYYY-MM-DD"}`.

**Passo 3 — Processamento dos JSONs:**

Cada `curl` retorna `{"data": [{"campaign_id": "...", "spend": "...", "cpm": "...", "actions": [...], "action_values": [...]}, ...]}`. O Claude lê os 2 JSONs como texto, calcula ROAS/CPL/CPM por campanha aplicando as fórmulas da seção "Fórmulas de cálculo" abaixo, e devolve o comparativo em linguagem natural.

**Não rodar Python adicional pra fazer essas contas.** A regra global no CLAUDE.md proíbe heredoc, pipe `curl | python3` e `python3 -c` longo com token — disparam o detector "expansion obfuscation" e exibem o token no pop-up nativo.

#### Modo MCP_CONECTOR

Usar `mcp__*__ads_insights_performance_trend` com parâmetros equivalentes (sem token na chamada — o MCP cuida).

#### Exceção (volume grande)

Se a campanha tem 200+ entidades e o cálculo manual fica inviável, salvar os 2 JSONs em arquivos separados via `curl ... > /tmp/cmp_atual.json` e `curl ... > /tmp/cmp_anterior.json`, depois rodar `python3 /tmp/script.py` onde o script lê os arquivos locais (sem token dentro). Limpar `/tmp/cmp_*.json` ao final.

### Referência de produto

Ler `perfil.md` (já carregado no Passo 0): campo `preco`. Inferir tipo de funil pelo objetivo predominante das campanhas:
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
| Hook Rate | `video_p25_watched_actions` / `impressions` | marcar `—` se não houver vídeo |
| CTR (link) | `clicks` / `impressions` | nunca zero |
| Connect Rate | `landing_page_views` / `clicks` | marcar `—` se LP views ausente |
| Lead Rate | `leads` / `landing_page_views` | só para funil OUTCOME_LEADS |
| Checkout Rate | `initiate_checkout` / `landing_page_views` | só para funil OUTCOME_SALES |
| Conversion Rate | `purchases` / `initiate_checkout` | só para funil OUTCOME_SALES |

`initiate_checkout` = `offsite_conversion.fb_pixel_initiate_checkout` (tipo canônico).

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "Me dá um ranking das 5 melhores campanhas por ROAS dos últimos 30 dias"

Usar métrica-norte conforme tipo de funil (ROAS para venda direta, CPL para captação). Se a conta tiver campanhas dos dois tipos, calcular separado e exibir dois rankings.

**Venda direta — ranking por ROAS:**

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

**Captação de leads — ranking por CPL:**

```
🏆 TOP 5 WINNERS  ·  {período}  ·  Métrica: CPL

  #   Campanha                   CPL        Leads    Spend
  ──────────────────────────────────────────────────────
  1.  {nome}                     R$ {X}     {N}      R$ {Y}
  ...
```

---

### Resposta 2. "Compara o CPM desse mês vs. mês anterior — ficou mais caro anunciar?"

```
📊 CPM — EVOLUÇÃO DO LEILÃO

  Período atual ({datas}):    R$ {X}  (média ponderada por spend)
  Período anterior ({datas}): R$ {Y}
  Variação:                   {+/-Z%}  {🟢 | 🟡 | 🔴}

  Leitura:
```

| Variação do CPM | Interpretação | Hipóteses |
|---|---|---|
| Subiu > 20% | 🔴 Leilão ficou caro | Sazonalidade, criativo fadigado, novo concorrente na praça |
| Subiu 10% a 20% | 🟡 Atenção | Monitorar — pode ser pontual |
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

  Vencedor: {posicionamento} — CPA {X%} abaixo da média
  Perdedor: {posicionamento} — CPA {X%} acima da média → testar excluir duplicando entidade no Gerenciador (variando 1 dimensão)
```

Se um posicionamento tiver gasto > 10% do total E conversões = 0 → marcar como `⚠️ queimando`.

---

### Resposta 4. "Me mostra o funil completo: impressões → cliques → conversões de cada campanha"

Mostrar o funil da campanha winner da Resposta 1 (ou da campanha que o aluno escolheu no escopo). Usar dois templates conforme o tipo de funil:

#### Template A — Venda direta (OUTCOME_SALES)

```
🔻 FUNIL — {nome_campanha}  ·  {período}

IMPRESSÕES         {N:,}
  ↓ Hook Rate {X%} {🟢|🟡|🔴}      — Urgência Oculta ativa (ou não)
  [somente se campanha tiver vídeo — omitir linha se estático]

CLIQUES (LINK)     {N:,}
  CTR {X%} {🟢|🟡|🔴}             — Identidade do Produto: promessa clara?

LP VIEWS           {N:,}
  ↓ Connect Rate {X%} {🟢|🟡|🔴}  — Quadro na Parede: anúncio alinhado com a página?

CHECKOUT INICIADO  {N:,}
  ↓ Checkout Rate {X%} {🟢|🟡|🔴} — Oferta: preço, garantia e stack de valor OK?

COMPRAS            {N:,}
  ↓ Conv. Rate {X%} {🟢|🟡|🔴}    — Furadeira + Decorados: checkout convence?

────────────────────────────────
ROAS final: {X.X}x  ·  CPA: R$ {Y}  ·  Spend: R$ {Z}
```

#### Template B — Captação de leads (OUTCOME_LEADS)

```
🔻 FUNIL — {nome_campanha}  ·  {período}

IMPRESSÕES         {N:,}
  ↓ Hook Rate {X%} {🟢|🟡|🔴}      — Urgência Oculta ativa (ou não)
  [somente se vídeo]

CLIQUES (LINK)     {N:,}
  CTR {X%} {🟢|🟡|🔴}             — Identidade do Produto: ângulo correto?

LP VIEWS           {N:,}
  ↓ Connect Rate {X%} {🟢|🟡|🔴}  — Quadro na Parede: anúncio alinhado com a página?

LEADS              {N:,}
  ↓ Lead Rate {X%} {🟢|🟡|🔴}     — Isca Digital: oferta de captura convincente?

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

Se `landing_page_views` não retornar (pixel sem evento de LP view), omitir as linhas "LP VIEWS", "Connect Rate" e tudo que depende delas. Alertar: "LP views não rastreado — conecte o evento no pixel no Gerenciador de Eventos para ver o funil completo."

---

### Resposta 5. "Qual público (idade, gênero, região) está convertendo mais barato?"

Cruzar os breakdowns de idade (`age`), gênero (`gender`) e região (`region`) com a métrica-norte (CPA para venda direta, CPL para captação) e destacar o segmento mais eficiente de cada dimensão.

```
👥 PÚBLICO — SEGMENTO MAIS EFICIENTE  ·  {período}

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

Se os breakdowns de público não estiverem disponíveis nos dados retornados pelo Passo 4, informar: "Breakdowns de público não retornaram — para ver essa análise, use `trafego-insights` com breakdown de age/gender/region."

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0 — Checklist antes de montar qualquer bloco

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

1. **Diagnóstico** — winner e loser do ranking, posicionamento vencedor, qual etapa do funil é o gargalo principal.
2. **Causa provável** — relação entre os dados. Ex: "CPM subiu 18% e Connect Rate caiu 30% — o leilão está mais caro E a página não converte quem chegou. Dois problemas distintos, não um."
3. **No VTSD, isso significa…** — qual elemento do método está em jogo. Usar a tabela abaixo como guia:

| Gargalo do funil | Elemento VTSD | Interpretação |
|---|---|---|
| Hook Rate baixo | Urgência Oculta | A dor não está sendo ativada no primeiro segundo do criativo |
| CTR baixo | Identidade do Produto | O ângulo do anúncio não comunica o diferencial claramente |
| Connect Rate baixo | Quadro na Parede | O que o anúncio promete não é o que a página entrega |
| Checkout Rate baixo | Oferta | Preço, garantia, bônus ou stack de valor não convencem |
| Conversion Rate baixa | Furadeira + Decorados | O método e os benefícios não estão claros na página de checkout |
| Lead Rate baixa | Isca Digital | A oferta de captura (e-book, aula, etc.) não é atraente o suficiente |

4. **Ação recomendada** — handoff para skill executora com instrução específica.

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Top winner com ROAS > 3x e freq < 3 | "trafego-escalar" — escalar com cautela |
| Top loser com gasto alto + zero conversão | "trafego-otimizar" — pausar com filtro |
| Posicionamento perdedor com gasto > 15% do total | Duplicar entidade no Gerenciador (variando 1 dimensão) — criar teste A/B de posicionamento |
| Gargalo em Hook Rate | Duplicar entidade no Gerenciador (variando 1 dimensão) — A/B de criativo com nova Urgência Oculta |
| Gargalo em Connect Rate | "feedback-pagina" — headline e promessa da página não batem com o anúncio |
| Gargalo em Checkout Rate ou Conversion Rate | "feedback-pagina" ou "pagina-checkout" — oferta, garantia, stack |
| CPM subindo > 20% WoW | Investigar fadiga → output [3] Criativos & Copy |
| Lead Rate baixa | "copy-pagina" — revisar isca digital e formulário de captura |

---

## Mapeamento HTML (export via `_export-html.md`)

| Bloco do output narrado | Componente do design system |
|---|---|
| Ranking de winners (top 5) | `.table` com colunas mono — `--neon` na linha #1 |
| Ranking de losers (top 5) | `.table` com colunas — `.down` (rust) na linha mais crítica |
| CPM atual vs. anterior | `.kpi` duplo (lado a lado) com `.up`/`.down` |
| ROAS atual vs. anterior | `.kpi` duplo com `.up`/`.down` |
| Tabela de posicionamento | `.table` com destaque `.up` no vencedor e `.down` no perdedor |
| Funil (cada etapa) | série de `.bar-row` — largura proporcional ao volume, cor conforme benchmark |
| Interpretação de cada etapa do funil | `.callout` (um por gargalo identificado) |
| Frase "No VTSD isso significa..." | `.callout` |
| Ação recomendada | `.pitch-box` |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no rodapé |
