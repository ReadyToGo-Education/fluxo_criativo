# Output [1] — Diagnóstico Rápido (60 segundos)

Visão geral pragmática que cabe numa olhada. Para o aluno que abre o Workshop e quer saber: "está tudo bem com minhas campanhas hoje?".

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- "Qual campanha está queimando mais dinheiro sem resultado?"
- "Tem algum anúncio com frequência alta e CTR caindo? (fadiga de criativo)"
- "Quanto gastei no total essa semana vs. semana passada?"
- "Alguma campanha estourou o orçamento diário hoje?"
- "Como está a saúde geral da minha conta? (Health Score)"

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## Dados necessários

### O que já vem do Passo 4 do command principal

`level=campaign`, sem breakdowns. Campos base: `spend`, `impressions`, `clicks`, `ctr`, `cpm`, `cpc`, `reach`, `frequency`, `actions`, `action_values`, `cost_per_action_type`, métricas de vídeo.

Período: conforme escolha do aluno no Passo 3. Não perguntar novamente.

### Campo de landing page view (leitura correta)

O campo `landing_page_view` **não existe como campo de topo nível** na chamada de insights em nível de campanha. Ele fica dentro do array `actions`, como item com `action_type = "landing_page_view"`.

Para ler corretamente:

```python
lpv = sum(
    float(a["value"])
    for a in camp.get("actions", [])
    if a["action_type"] == "landing_page_view"
)
```

O `trafego_processar.py` faz isso automaticamente ao processar o cache do `trafego_fetch.py`. Não adicionar `landing_page_views` como campo separado na chamada — a API retorna HTTP 400.

### Chamadas adicionais (executar antes de montar os blocos)

**IMPORTANTE — regras da Graph API que causaram erros reais:**
- `effective_status` é parâmetro válido SOMENTE no endpoint `/campaigns`. **Nunca usar no endpoint `/insights`** — a API ignora silenciosamente ou retorna resultado vazio.
- Não usar `curl` com arrays JSON (`["ACTIVE"]`) no shell. O quoting varia entre Windows e Mac e causa "unexpected token". Usar sempre o `trafego_fetch.py` via Python.

**Uso padrão (modo APP):**

Todas as chamadas 1a, 1b, 1c e 1d são feitas por um único script Python que salva em cache local. Isso evita rate limit, encoding issues e problemas de shell cross-platform:

```bash
python3 .claude/skills/trafego-analise/scripts/trafego_fetch.py \
  --account {CONTA_ATIVA_ID} \
  --filtro "VTSD - CV" \
  --periodo last_30d \
  --output diagnostico \
  --project-root . \
  --cache-dir skill-analise/cache
```

O script faz as 4 chamadas em sequência com retry em rate limit e salva o resultado em `skill-analise/cache/{account}_{periodo}_{filtro}_{output}.json`.

**Chamada 1b — Comparativo WoW (dentro do fetch):**

Usa `date_preset` expandido com `time_increment` automático conforme o período principal:

| Período principal | Comparativo 1b | time_increment |
|---|---|---|
| `last_7d` | `last_14d` | 7 |
| `last_14d` | `last_28d` | 14 |
| `last_30d` | `last_60d` | 30 |

**Chamada 1c — Orçamentos** (endpoint `/campaigns`, único que aceita `effective_status`):

`budget_remaining` só é populado para campanhas com **lifetime budget**. Para **daily budget**, cruzar `spend_hoje` (Chamada 1d) com `daily_budget` manualmente. A API retorna valores em centavos — dividir por 100 para obter reais.

**Chamada 1d — Gasto de hoje** (endpoint `/insights`, sem `effective_status`):

`date_preset=today` no endpoint de insights. O parâmetro `effective_status` **não existe** em insights — o filtro de campanhas ativas é feito no pós-processamento comparando os IDs das campanhas da chamada 1c.

**Modo MCP_CONECTOR:** usar `mcp__*__ads_insights_performance_trend` para 1b e 1d; `mcp__*__ads_get_ad_entities` com `entity_type=campaign` para 1c.

### Referência de produto (benchmarks)

Ler do `perfil.md` (já carregado no Passo 0): campo `preco`. Inferir tipo de funil pelo objetivo predominante das campanhas (`OUTCOME_LEADS` = captação; `OUTCOME_SALES` = venda direta).

| Tipo de funil | Ticket | ROAS mínimo saudável | CPA máximo saudável |
|---|---|---|---|
| Venda direta — low ticket | ≤ R$ 97 | 2.5x | ticket × 0.40 |
| Venda direta — ticket médio | R$ 98 a R$ 497 | 3.0x | ticket × 0.30 |
| Venda direta — high ticket | > R$ 497 | 4.0x | ticket × 0.25 |
| Captação de leads | qualquer | — | CPL-alvo: perguntar ao aluno se não estiver no perfil |

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "Qual campanha está queimando mais dinheiro sem resultado?"

Critério: campanha com `spend` > R$ 50 no período E conversões = 0 (usando tipo canônico: `offsite_conversion.fb_pixel_purchase` para vendas, `offsite_conversion.fb_pixel_lead` para captação).

Montar ranking das top 3 campanhas por gasto com zero resultado:

```
🚨 [QUEIMA]  {nome_campanha}
   Gasto: R$ {X} em {N} dias  ·  Conversões: 0
   CPA implícito: infinito — cada real investido aqui está sendo descartado
   Ação: pausar via "trafego-otimizar" — atalho "pausar com filtro" (gasto > X + zero conversão)
```

Se nenhuma campanha se enquadrar no critério, responder explicitamente: "Nenhuma campanha com gasto significativo e zero conversão identificada no período."

---

### Resposta 2. "Tem algum anúncio com frequência alta e CTR caindo? (fadiga de criativo)"

Verificar duas categorias de sinal, nesta ordem:

**Fadiga de criativo**

Critério: campanha com `frequency` ≥ 4 E `ctr` caindo ≥ 15% em relação ao período anterior (Chamada 1b).

```
🚨 [FADIGA]  {nome_campanha}
   Frequência: {X.X}  ·  CTR atual: {Y%}  ·  CTR anterior: {Z%}  (queda de {W%})
   Gasto em risco: R$ {spend_campanha} com retorno decaindo
   Ação: rodar output [3] Criativos & Copy para identificar o anúncio específico e criar variações
```

Nota: a frequência disponível aqui é no nível de campanha. Para identificar qual anúncio exato tem fadiga, usar output [3].

**Saturação de público**

Critério: campanha com objetivo de tráfego frio (`OUTCOME_SALES` ou `LINK_CLICKS`) e `frequency` ≥ 5.

```
🚨 [SATURAÇÃO]  {nome_campanha}
   Frequência: {X.X}  ·  CPM: R$ {Y}  ·  CTR: {Z%}
   Mesmo público viu o criativo {X} vezes — leilão encarecendo, resposta caindo
   Ação: criar nova audience no Gerenciador de Audiences (Lookalike ou público aberto) ou expandir targeting
```

**Below average rankings**

Este sinal exige campos `quality_ranking`, `engagement_rate_ranking`, `conversion_rate_ranking` que só existem no nível de `ad`, não de `campaign`. Não estão disponíveis nas chamadas deste output.

Regra: não inventar este sinal. Mencionar ao final: "Para verificar anúncios com qualidade abaixo da média no leilão, rode output [3] Criativos & Copy."

Se nenhum sinal de fadiga ou saturação for identificado, responder explicitamente: "Nenhuma campanha com frequência elevada e queda de CTR detectada no período."

---

### Resposta 3. "Quanto gastei no total essa semana vs. semana passada?"

Apresentar a tabela comparativa completa do período:

```
🔍 DIAGNÓSTICO RÁPIDO  ·  {nome_conta}  ·  {período}

                         Este período      Período anterior    Variação
──────────────────────────────────────────────────────────────────────
Gasto total              R$ {X}            R$ {Y}              {+/-Z%}
Compras / Leads          {N}               {M}                 {+/-Z%}
ROAS médio               {X.X}x            {Y.Y}x              {+/-Z%}
CPA / CPL médio          R$ {X}            R$ {Y}              {+/-Z%}
Campanhas ativas         {N}               —                   —
```

Se a Chamada 1b não retornar dados comparativos (ex: período customizado muito antigo), suprimir a coluna "Período anterior" e mostrar só os valores atuais, informando o motivo.

---

### Resposta 4. "Alguma campanha estourou o orçamento diário hoje?"

Critério: `spend_hoje` (Chamada 1d) ≥ 90% de `daily_budget` (Chamada 1c).

Para campanhas com **daily budget**: restante = `daily_budget` − `spend_hoje` (cálculo manual, API não expõe este campo).
Para campanhas com **lifetime budget**: usar `budget_remaining` da Chamada 1c diretamente.

```
🚨 [BUDGET]  {nome_campanha}
   Gasto hoje: R$ {X}  ·  Budget diário: R$ {Y}  ·  Restante estimado: R$ {Z}
   Risco: orçamento pode esgotar antes do horário nobre (18h-22h), pausando a veiculação
   Ação: aumentar budget via "trafego-escalar" OU criar regra de alerta no Gerenciador (Regras automáticas)
```

Se restante = 0 E campanha ainda ativa → sinal crítico imediato, listar no topo independente da ordem.

Se nenhuma campanha atingiu 90% do budget diário, responder explicitamente: "Nenhuma campanha com orçamento diário esgotado ou próximo do limite hoje."

---

### Resposta 5. "Como está a saúde geral da minha conta? (Health Score)"

Calculado inteiramente a partir dos dados disponíveis nas chamadas 1a, 1b, 1c, 1d. Fórmula operacional:

```
Score = (D1 × 0.20) + (D2 × 0.20) + (D3 × 0.25) + (D4 × 0.25) + (D5 × 0.10)
```

#### Dimensão 1 — Diversidade criativa (peso 20%)

Proxy: número de campanhas ativas com `spend` > R$ 10 no período. A contagem real da Mandala (18 tipos) só é verificável no output [3].

| Campanhas ativas com gasto | Pontos |
|---|---|
| ≥ 10 | 100 |
| 6 a 9 | 75 |
| 3 a 5 | 50 |
| 2 | 30 |
| 1 | 15 |
| 0 | 0 |

#### Dimensão 2 — Saúde de públicos (peso 20%)

Percentual de campanhas ativas com `frequency` ≤ 3.

| % campanhas com freq ≤ 3 | Pontos |
|---|---|
| 100% | 100 |
| 75% a 99% | 80 |
| 50% a 74% | 55 |
| 25% a 49% | 30 |
| < 25% | 10 |

Penalidade: se qualquer campanha tiver `frequency` > 6, subtrair 10 pontos desta dimensão (mínimo 0).

#### Dimensão 3 — Eficiência de funil (peso 25%)

Connect rate = `landing_page_view` (do array `actions`) / `link_click` (do array `actions`), somando todas as campanhas.

**Por que `link_click` e não `clicks`:**
- `clicks` (campo de topo) inclui cliques em qualquer lugar do post (curtir, expandir, ver mais, etc.)
- `link_click` (dentro de `actions`) representa apenas cliques que abrem o link de destino
- Usar `clicks` inflaria artificialmente o denominador e produziria um Connect Rate falso (ex: 12% em vez de 58%)
- O `trafego_processar.py` usa `link_click` do array `actions` automaticamente, com fallback para `clicks` se `link_click` não estiver disponível

| Connect Rate | Pontos |
|---|---|
| ≥ 70% | 100 |
| 55% a 69% | 75 |
| 40% a 54% | 50 |
| 20% a 39% | 25 |
| < 20% | 10 |

Se `landing_page_view` não retornar para nenhuma campanha (pixel sem evento de LP view configurado): usar CTR médio como fallback.

| CTR médio (fallback) | Pontos |
|---|---|
| ≥ 2% | 80 |
| 1% a 1.99% | 55 |
| < 1% | 25 |

#### Dimensão 4 — Performance financeira (peso 25%)

Para funil de **venda direta**: ROAS médio ponderado por spend (soma de `action_values` / soma de `spend`, usando tipo canônico de compra).

| ROAS médio | Pontos |
|---|---|
| ≥ 4.0x | 100 |
| 3.0x a 3.9x | 85 |
| 2.0x a 2.9x | 65 |
| 1.5x a 1.9x | 40 |
| 1.0x a 1.4x | 20 |
| < 1.0x | 0 |

Para funil de **captação de leads**: CPL médio vs. benchmark do produto (calculado via `cost_per_action_type` com tipo canônico de lead).

| CPL vs. benchmark | Pontos |
|---|---|
| ≤ 60% do benchmark | 100 |
| 61% a 80% | 80 |
| 81% a 100% | 60 |
| 101% a 130% | 35 |
| > 130% | 10 |

Se conversões = 0 em todas as campanhas (pixel não rastreando): atribuir 0 pontos e alertar o aluno separadamente.

#### Dimensão 5 — Consistência temporal (peso 10%)

Requer Chamada 1b. Calcular variação de CPA (ou CPL) semana atual vs. semana anterior.

| Variação WoW do CPA | Pontos |
|---|---|
| Melhora ou estável (≤ +20%) | 100 |
| Aumento +21% a +30% | 70 |
| Aumento +31% a +50% | 40 |
| Aumento > +50% | 10 |
| Sem dados comparativos | 50 (neutro) |

#### Apresentação do score

```
HEALTH SCORE: {XX}/100  {emoji}

  Diversidade criativa    {D1}/100  (peso 20%)  →  {N} campanhas ativas com gasto
  Saúde de públicos       {D2}/100  (peso 20%)  →  {X%} com frequência ≤ 3
  Eficiência de funil     {D3}/100  (peso 25%)  →  Connect Rate {Y%}
  Performance financeira  {D4}/100  (peso 25%)  →  ROAS médio {Z}x  (benchmark: {W}x)
  Consistência temporal   {D5}/100  (peso 10%)  →  CPA {+/-V%} vs. período anterior
```

| Score final | Classificação | O que significa |
|---|---|---|
| 85 a 100 | 🟢 Excelente | Conta saudável — foco em escala |
| 70 a 84 | 🟡 Boa | Funcionando bem — otimizações pontuais |
| 50 a 69 | 🟠 Regular | Problemas específicos a resolver antes de escalar |
| 0 a 49 | 🔴 Crítica | Parar escalada — diagnóstico profundo urgente |

---

### Análise adicional — Próximo passo VTSD

Indicar em 1 linha qual output rodar a seguir, conforme o sintoma dominante identificado nas respostas acima:

| Situação | Output recomendado |
|---|---|
| Score < 50 OU 2+ sinais críticos simultâneos | [8] Problemas Ocultos |
| Fadiga ou saturação de público detectada | [3] Criativos & Copy |
| Queima de dinheiro > R$ 300 no período | [2] Performance & Funil (ranking por ROAS) |
| Budget estourando antes das 18h | [9] Orçamento & Projeção |
| Connect Rate < 40% | [2] Performance & Funil (gargalo de funil) |
| Score ≥ 85, sem sinais críticos | [9] Orçamento & Projeção (quem escalar) |

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0 — Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] Qual campanha está queimando mais dinheiro sem resultado?
    → coberto? Se não: calcular CPR e rankear campanhas por gasto/resultado, identificando a maior queimadora

[ ] Tem algum anúncio com frequência alta e CTR caindo? (fadiga de criativo)
    → coberto? Se não: verificar frequência >= 3 e queda de CTR WoW em cada anúncio ativo

[ ] Quanto gastei no total essa semana vs. semana passada?
    → coberto? Se não: comparar total de spend do período atual com o WoW e calcular delta percentual

[ ] Alguma campanha estourou o orçamento diário hoje?
    → coberto? Se não: listar campanhas com daily_budget atingido no dia corrente

[ ] Como está a saúde geral da minha conta? (Health Score)
    → coberto? Se não: calcular as 5 dimensões e exibir score com classificação (Excelente/Boa/Regular/Crítica)
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão (obrigatório)

1. **Diagnóstico** — apresentar Bloco 1 (números com WoW) e informar quantos sinais críticos foram identificados.
2. **Causa provável** — o que os sinais do Bloco 2 sugerem em conjunto. Ex: "dois sinais de fadiga + frequência alta = criativo esgotado, não é problema de público"; "queima de dinheiro sem conversão = pixel provavelmente misconfigured ou página quebrando".
3. **No VTSD, isso significa…** — ex: "Score 92 + ROAS subindo = Identidade do Consumidor bem calibrada, Quadro na Parede chegando ao público certo. Hora de escalar." Ou: "Frequência > 4 em 3 campanhas = o mesmo criativo atingiu as mesmas pessoas muitas vezes. A Urgência Oculta esgotou. Precisamos de novos ângulos pela Mandala."
4. **Ação recomendada** — 1 a 3 ações concretas com handoff para a skill executora.

---

## Handoffs típicos

| Sinal predominante | Para onde mandar |
|---|---|
| Queima de dinheiro | "trafego-otimizar" — ações em lote: pausar campanhas com gasto > X e zero conversão |
| Fadiga de criativo | Duplicar entidade no Gerenciador (variando 1 dimensão) (A/B de criativo novo) ou Gerenciador de Audiences (nova audience) |
| Conta saudável + ROAS alto | "trafego-escalar" — aumentar budget das campanhas vencedoras |
| Budget estourando | Gerenciador (Regras automáticas) — criar regra automática de freio por budget diário |
| Connect Rate baixo | "feedback-pagina" ou "pagina-performance" — gargalo está na página, não no anúncio |
| Pixel sem conversão | Gerenciador de Eventos — diagnóstico aprofundado do rastreamento |

---

## Mapeamento HTML (export via `_export-html.md`)

| Bloco do output narrado | Componente do design system |
|---|---|
| Métricas do Bloco 1 (gasto, conversões, ROAS, CPA) | `.kpi-grid` com 4 a 6 `.kpi` — classe `.up` ou `.down` conforme WoW |
| Tabela comparativa período atual vs. anterior | `.table` com colunas `.up`/`.down` |
| Cada sinal crítico do Bloco 2 | `.regra.alerta` (um elemento por sinal identificado) |
| Ranking de queima de dinheiro (top 3) | `.table` com colunas: campanha / gasto / conversões / CPA implícito |
| Health Score total + emoji de classificação | `.metric` (número grande em `--neon`) |
| Detalhamento das 5 dimensões | série de `.bar-row` (uma por dimensão, largura proporcional ao score parcial) |
| Frase "No VTSD isso significa..." | `.callout` |
| Ação recomendada | `.pitch-box` |
| Próximo output recomendado | `.term.next` dentro de `.terms` no rodapé |
