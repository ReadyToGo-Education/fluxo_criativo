# Output [9] — Orçamento & Projeção

Visão de para onde o dinheiro vai, quanto ainda vai gastar até o fim do mês e como redistribuir para maximizar resultado sem aumentar o gasto total.

---

## Perguntas que cobre (Obrigatório a resposta dessas perguntas)

- "No ritmo atual, quanto vou gastar até o fim do mês?"
- "Qual campanha tem o melhor custo-benefício pra eu aumentar o orçamento?"
- "Redistribui meu orçamento: tira de quem performa mal e joga pra quem performa bem"
- "Quanto sobra de orçamento se eu pausar os perdedores?"

Mas pode trazer respostas adicionais correlacionadas a essas perguntas

---

## Dados necessários

### O que já vem do Passo 4 do command principal

`level=campaign`, sem breakdowns. Campos base: `spend`, `impressions`, `clicks`, `ctr`, `cpm`, `cpc`, `reach`, `frequency`, `actions`, `action_values`, `cost_per_action_type`, métricas de vídeo.

Período: conforme escolha do aluno no Passo 3. Não perguntar novamente.

### Campos adicionais a acrescentar na chamada principal deste output

```
landing_page_views
```

Necessário para calcular connect rate e identificar gargalos de funil nos candidatos a escala.

### Chamadas adicionais (executar antes de montar os blocos)

**Chamada 9b — Orçamentos e gasto de hoje**

Retorna `daily_budget`, `lifetime_budget`, `budget_remaining` por campanha ativa, e o gasto acumulado de hoje para cruzar com o orçamento diário.

```bash
# Modo APP — orçamentos das campanhas
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/campaigns
  ?fields=id,name,status,daily_budget,lifetime_budget,budget_remaining,start_time,stop_time
  &effective_status={STATUS_FILTRO}
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

```bash
# Modo APP — gasto de hoje (para calcular ritmo diário do mês corrente)
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=campaign_id,campaign_name,spend
  &level=campaign
  &date_preset=today
  &effective_status={STATUS_FILTRO}
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Chamada 9c — Gasto do mês corrente até hoje**

```bash
# Modo APP
# Calcular since=primeiro dia do mês corrente, until=hoje (YYYY-MM-DD)
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=campaign_id,campaign_name,spend,actions,action_values,cost_per_action_type,frequency
  &level=campaign
  &time_range={'since':'{PRIMEIRO_DIA_MES}','until':'{HOJE}'}
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Chamada 9d — Gasto do mês anterior (para comparativo)**

```bash
# Modo APP
# Calcular since=primeiro dia do mês anterior, until=último dia do mês anterior
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields=spend,actions,action_values
  &level=account
  &time_range={'since':'{PRIMEIRO_DIA_MES_ANTERIOR}','until':'{ULTIMO_DIA_MES_ANTERIOR}'}
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

**Notas sobre orçamentos na API:**
- `budget_remaining` só é populado pela API para campanhas com **lifetime budget**. Para campanhas com **daily budget**, o campo retorna nulo — calcular restante manualmente: `restante = daily_budget − spend_hoje`.
- `daily_budget` e `lifetime_budget` são retornados em centavos (inteiros). Dividir por 100 para obter valor em reais.
- Campanhas CBO: o orçamento fica no nível de campanha. Campanhas ABO: o orçamento está no nível de adset. Para ABO, usar chamada adicional ao nível de adsets se necessário.

**Modo MCP_CONECTOR:** usar `mcp__*__ads_get_ad_entities` com `entity_type=campaign` para 9b; `mcp__*__ads_insights_performance_trend` com `date_preset=this_month` para 9c e com o mês anterior para 9d.

### Referência de produto (benchmarks)

Ler do `perfil.md` (já carregado no Passo 0): campo `preco`. Inferir tipo de funil pelo objetivo predominante das campanhas.

| Tipo de funil | Ticket | ROAS mínimo saudável | CPA máximo saudável | Candidato a escala |
|---|---|---|---|---|
| Venda direta — low ticket | ≤ R$ 97 | 2.5x | ticket × 0.40 | ROAS ≥ 3.0x + freq ≤ 3.5 |
| Venda direta — ticket médio | R$ 98 a R$ 497 | 3.0x | ticket × 0.30 | ROAS ≥ 3.5x + freq ≤ 3.0 |
| Venda direta — high ticket | > R$ 497 | 4.0x | ticket × 0.25 | ROAS ≥ 4.5x + freq ≤ 2.5 |
| Captação de leads | qualquer | — | CPL-alvo do perfil (ou perguntar) | CPL ≤ 70% do benchmark + freq ≤ 3.5 |

---

## Fórmulas de cálculo

### ROAS por campanha
```
ROAS = sum(action_values onde action_type = "offsite_conversion.fb_pixel_purchase") / spend
```
Usar tipo canônico. Nunca somar outros tipos de purchase.

### CPL por campanha
```
CPL = spend / sum(actions onde action_type = "offsite_conversion.fb_pixel_lead")
```

### CPA por campanha
```
CPA = spend / sum(actions onde action_type = "offsite_conversion.fb_pixel_purchase")
```

### Projeção de gasto do mês
```
dias_passados = dia_atual (número do dia no mês, ex: 12)
dias_totais   = total de dias do mês corrente (ex: 31)
dias_restantes = dias_totais − dias_passados

ritmo_diario  = spend_mes_ate_hoje / dias_passados
projecao_fim  = spend_mes_ate_hoje + (dias_restantes × orcamento_diario_total_ativo)
```

Usar `orcamento_diario_total_ativo` (soma dos `daily_budget` de todas as campanhas ativas) como numerador para os dias restantes, não o `ritmo_diario`. Justificativa: o ritmo histórico pode incluir campanhas que foram pausadas. O orçamento diário atual reflete o estado real.

### Liberação potencial (quanto sobra ao pausar perdedores)
```
liberacao_diaria     = sum(daily_budget das campanhas marcadas como "pausar")
liberacao_mensal     = liberacao_diaria × dias_restantes
gasto_ja_realizado   = sum(spend_mes_ate_hoje das campanhas marcadas como "pausar")
```

### ROAS médio ponderado (conta inteira)
```
ROAS_medio = sum(action_values de todas as campanhas) / sum(spend de todas as campanhas)
```

### CPL médio ponderado (conta de leads)
```
CPL_medio = sum(spend) / sum(leads de todas as campanhas)
```

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "No ritmo atual, quanto vou gastar até o fim do mês?"

Mostrar dois sub-blocos separados conforme o tipo de funil predominante.

#### Template A — Venda direta (OUTCOME_SALES)

```
💰 PROJEÇÃO DO MÊS  ·  {nome_conta}  ·  {mês/ano}

Hoje: dia {X} de {Y} (restam {Z} dias)
Gasto acumulado no mês:        R$ {A}   (média de R$ {A/X}/dia)
Orçamento diário total ativo:  R$ {B}
─────────────────────────────────────────
Projeção até o fim do mês:     R$ {A + (Z × B)}

Mês anterior — gasto total:    R$ {C}
Variação projetada:            {+/-D%}  {🟢 | 🟡 | 🔴}

ROAS médio no mês até hoje:    {X.X}x
CPA médio no mês até hoje:     R$ {Y}
```

#### Template B — Captação de leads (OUTCOME_LEADS)

```
💰 PROJEÇÃO DO MÊS  ·  {nome_conta}  ·  {mês/ano}

Hoje: dia {X} de {Y} (restam {Z} dias)
Gasto acumulado no mês:        R$ {A}   (média de R$ {A/X}/dia)
Orçamento diário total ativo:  R$ {B}
─────────────────────────────────────────
Projeção até o fim do mês:     R$ {A + (Z × B)}

Mês anterior — gasto total:    R$ {C}
Variação projetada:            {+/-D%}  {🟢 | 🟡 | 🔴}

CPL médio no mês até hoje:     R$ {X}   (benchmark: R$ {Y})
Leads gerados no mês até hoje: {N}
Ritmo de leads/dia:            {N/X}
Projeção de leads até o fim:   ~{N + (Z × N/X)}
```

**Referência de variação:**

| Variação projetada vs. mês anterior | Classificação |
|---|---|
| Crescimento > 20% com ROAS/CPL melhor ou estável | 🟢 Escala saudável |
| Crescimento > 20% com ROAS/CPL piorando | 🟡 Crescendo com ineficiência |
| Estável (±20%) | 🟡 Manter |
| Queda > 20% | 🔴 Orçamento retraindo — verificar se foi intencional |

Se a Chamada 9d não retornar (conta sem histórico de mês anterior): suprimir a linha "Mês anterior" e exibir apenas os valores do mês corrente.

---

### Resposta 2. "Qual campanha tem o melhor custo-benefício pra eu aumentar o orçamento?"

Filtrar as campanhas com melhor performance e calcular o headroom estimado para cada candidata a escala. Ordenar por ROAS decrescente (venda direta) ou CPL crescente (captação).

**Headroom:** estimativa de quanto o orçamento pode crescer antes de o algoritmo começar a degradar performance. Basear em dois sinais: frequência atual (quanto mais baixa, mais espaço) e tamanho do público (não disponível aqui — usar frequência como proxy).

```
🚀 CANDIDATOS A ESCALA  ·  {mês/ano}

  Campanha         ROAS/CPL         Freq   Daily Budget   Headroom estimado   Modo escala
  ────────────────────────────────────────────────────────────────────────────────────────
  {nome}           {X.X}x / R$ {Y}  {Z.Z}  R$ {W}         até +50%            vertical
  {nome}           {X.X}x / R$ {Y}  {Z.Z}  R$ {W}         até +30%            vertical
  {nome}           {X.X}x / R$ {Y}  {Z.Z}  R$ {W}         até +20%            horizontal
```

**Regra de headroom por frequência:**

| Frequência atual | Headroom estimado | Modo recomendado |
|---|---|---|
| < 1.5 | até +70% | vertical (aumentar budget direto) |
| 1.5 a 2.4 | até +50% | vertical |
| 2.5 a 3.0 | até +30% | vertical com cautela ou horizontal |
| 3.1 a 3.5 | até +20% | horizontal (duplicar adset ou nova audience) |
| > 3.5 | não escalar — público saturando | investigar primeiro |

**Atenção:** se só uma campanha for candidata a escala e ela já concentrar > 70% do orçamento total, alertar: "Dependência excessiva de um único winner. Escalar aumenta risco de ruptura. Criar campanha paralela duplicando entidade no Gerenciador (variando 1 dimensão) (duplicar-variando) antes de aumentar o orçamento desta."

---

### Resposta 3. "Redistribui meu orçamento: tira de quem performa mal e joga pra quem performa bem"

Mostrar como realocar o orçamento dos perdedores nos winners, sem mudar o total diário da conta. Esta resposta depende da classificação de veredicto por campanha (feita na Análise adicional abaixo) — executar a classificação antes de montar os templates desta seção.

#### Verificação de modo orçamentário (executar antes de montar os templates)

Antes de apresentar a redistribuição, identificar se a conta opera em modo CBO ou ABO:

- **CBO (Campaign Budget Optimization):** o campo `daily_budget` está presente nas campanhas (retornado pela Chamada 9b). O orçamento é controlado no nível de campanha. Usar os templates A e B abaixo normalmente.
- **ABO (Adset Budget Optimization):** o campo `daily_budget` está ausente ou nulo nas campanhas, mas presente nos adsets. Nesse caso, a redistribuição deve operar no nível de conjunto de anúncios, não de campanha. Adaptar os templates substituindo "Campanha" por "Conjunto de anúncios" e usando os `daily_budget` dos adsets como referência.

Se o modo ABO for detectado, exibir a seguinte nota no topo desta seção:

```
⚠️ Conta em modo ABO: redistribuição feita no nível de conjunto de anúncios. Para centralizar o controle, considere migrar para CBO via "trafego-criar-campanha".
```

Para verificar os orçamentos em modo ABO, executar chamada adicional ao nível de adsets das campanhas ativas antes de montar o bloco.

---

#### Template A — Venda direta (OUTCOME_SALES)

```
🔀 REDISTRIBUIÇÃO PROPOSTA  ·  gasto total mantido em R$ {total}/dia

  Tirar:
  ─ {nome}  -R$ {X}/dia  (pausar — ROAS {Y}x, abaixo do mínimo)
  ─ {nome}  -R$ {X}/dia  (reduzir de R$ {A} para R$ {B}/dia — revisar mas manter rodando)

  Colocar:
  + {nome}  +R$ {X}/dia  (winner principal — ROAS {Y}x, headroom até +{Z}%)
  + {nome}  +R$ {X}/dia  (winner secundário — ROAS {Y}x)

  ─────────────────────────────────────────────────────────────────────
  Antes:   ROAS médio {A}x  ·  CPA médio R$ {B}  ·  Budget/dia R$ {C}
  Depois:  ROAS médio ~{D}x ·  CPA médio ~R$ {E} ·  Budget/dia R$ {C}
  Ganho estimado de eficiência: {+F%} no ROAS
```

#### Template B — Captação de leads (OUTCOME_LEADS)

```
🔀 REDISTRIBUIÇÃO PROPOSTA  ·  gasto total mantido em R$ {total}/dia

  Tirar:
  ─ {nome}  -R$ {X}/dia  (pausar — CPL R$ {Y}, acima do benchmark)
  ─ {nome}  -R$ {X}/dia  (reduzir — CPL aceitável mas frequência alta)

  Colocar:
  + {nome}  +R$ {X}/dia  (winner — CPL R$ {Y}, {Z%} abaixo do benchmark)
  + {nome}  +R$ {X}/dia  (testar nova audience no Gerenciador de Audiences)

  ─────────────────────────────────────────────────────────────────────
  Antes:   CPL médio R$ {A}  ·  Leads/dia ~{B}  ·  Budget/dia R$ {C}
  Depois:  CPL médio ~R$ {D} ·  Leads/dia ~{E}  ·  Budget/dia R$ {C}
  Ganho estimado: {+F%} mais leads com o mesmo gasto
```

**Regra de cautela:** nunca propor aumento de mais de 50% em um único passo em campanhas com histórico < 7 dias. Nesse caso, sinalizar: "Campanha com histórico curto — aumentar no máximo 20% e aguardar 3 dias para reavaliar."

---

### Resposta 4. "Quanto sobra de orçamento se eu pausar os perdedores?"

Calcular a liberação diária e mensal ao pausar as campanhas com veredicto 🔴. Usar as fórmulas de liberação potencial definidas em "Fórmulas de cálculo".

```
💡 LIBERAÇÃO POTENCIAL — PAUSAR OS PERDEDORES

  Campanhas candidatas a pausar:
  ─────────────────────────────────────────────────────────────────────
  {nome}            Daily budget: R$ {X}   Gasto no mês até hoje: R$ {Y}
  {nome}            Daily budget: R$ {X}   Gasto no mês até hoje: R$ {Y}
  ─────────────────────────────────────────────────────────────────────
  Total diário liberado:   R$ {soma_daily}
  Dias restantes no mês:   {Z}
  Liberação potencial:     R$ {soma_daily × Z}  (a partir de hoje até o dia {fim_mes})

  Já foi gasto nessas campanhas este mês: R$ {soma_spend_mes} (não recuperável)
```

---

### Análise adicional — Distribuição atual de orçamento

Mostrar onde o orçamento está alocado e emitir veredicto por campanha. Esta tabela alimenta as Respostas 3 e 4 acima — deve ser executada antes de montar os templates de redistribuição e liberação. Ordenar por `daily_budget` decrescente.

#### Template A — Venda direta (OUTCOME_SALES)

```
🥧 ONDE SEU DINHEIRO ESTÁ HOJE

  Campanha              Daily Budget   % total   ROAS (mês)   CPA (mês)    Veredicto
  ─────────────────────────────────────────────────────────────────────────────────
  {nome}                R$ {X}         {Y%}      {Z.Z}x       R$ {W}       🟢 escalar
  {nome}                R$ {X}         {Y%}      {Z.Z}x       R$ {W}       🟡 manter
  {nome}                R$ {X}         {Y%}      {Z.Z}x       R$ {W}       🟠 revisar
  {nome}                R$ {X}         {Y%}      {Z.Z}x       R$ {W}       🔴 pausar
  ─────────────────────────────────────────────────────────────────────────────────
  TOTAL                 R$ {sum}       100%      {ROAS_medio}x R$ {CPA_med}  —

  Ineficiência detectada:
  {lista das campanhas 🔴 com cálculo} queimam R$ {X}/dia (R$ {X × Z}/mês restante).
  Pausar libera R$ {liberacao_mensal} até o dia {Y} do mês.
```

#### Template B — Captação de leads (OUTCOME_LEADS)

```
🥧 ONDE SEU DINHEIRO ESTÁ HOJE

  Campanha              Daily Budget   % total   CPL (mês)    Leads (mês)  Veredicto
  ─────────────────────────────────────────────────────────────────────────────────
  {nome}                R$ {X}         {Y%}      R$ {Z}       {N}          🟢 escalar
  {nome}                R$ {X}         {Y%}      R$ {Z}       {N}          🟡 manter
  {nome}                R$ {X}         {Y%}      R$ {Z}       {N}          🟠 revisar
  {nome}                R$ {X}         {Y%}      R$ {Z}       {N}          🔴 pausar
  ─────────────────────────────────────────────────────────────────────────────────
  TOTAL                 R$ {sum}       100%      R$ {CPL_med}  {total_leads}  —

  Ineficiência detectada:
  {lista 🔴} geram CPL {X%} acima do benchmark ({R$ benchmark}).
  Pausar libera R$ {liberacao_mensal} até o fim do mês.
```

**Critérios de veredicto:**

| Veredicto | Critério — Venda direta | Critério — Captação |
|---|---|---|
| 🟢 escalar | ROAS ≥ mínimo da faixa × 1.2 E freq ≤ 3.5 | CPL ≤ 70% do benchmark E freq ≤ 3.5 |
| 🟡 manter | ROAS entre mínimo e mínimo × 1.2 | CPL entre 70% e 100% do benchmark |
| 🟠 revisar | ROAS entre 1.0x e mínimo | CPL entre 100% e 150% do benchmark |
| 🔴 pausar | ROAS < 1.0x OU spend > R$ 100 no mês com 0 conversões | CPL > 150% do benchmark OU spend > R$ 100 com 0 leads |

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0 — Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] No ritmo atual, quanto vai gastar até o fim do mês?
    → coberto? Se não: calcular gasto diário médio do período e multiplicar pelos dias restantes no mês, somando ao gasto atual

[ ] Qual campanha tem o melhor custo-benefício para aumentar o orçamento?
    → coberto? Se não: rankear campanhas por ROAS e CPA e identificar as com headroom de escala (CPA < benchmark e frequência < 2.5)

[ ] Redistribuição de orçamento: tirar de quem performa mal, jogar para quem performa bem
    → coberto? Se não: calcular quanto liberar das perdedoras (CPA > benchmark x 1.5) e propor realocação explícita em valores de orçamento

[ ] Quanto sobra de orçamento se pausar os perdedores?
    → coberto? Se não: somar o budget diário atual das campanhas abaixo da linha de corte e mostrar o valor liberado
```

Se qualquer item estiver descoberto: adicionar a seção correspondente antes de entregar. Não pular para o Diagnóstico sem este checklist completo.

---

## Protocolo padrão

1. **Diagnóstico** — projeção do mês, distribuição atual com veredictos, campanhas candidatas a escala e candidatas a pausar.
2. **Causa provável** — desbalanceamento da alocação: por que o orçamento está concentrado em campanhas ineficientes. Ex: "Campanha D era winner há 60 dias e nunca foi revisada. O algoritmo aprendeu a gastar o budget dela mesmo sem resultado."
3. **No VTSD, isso significa…** — "Funil perpétuo saudável exige no mínimo 70% do budget no winner do momento. Você está em {X%}. O restante está pulverizado em campanhas que já deram o que podiam. Concentrar é mais importante que criar campanhas novas agora." Ou, para leads: "CPL subindo enquanto volume cai é sinal clássico de público esgotando. Antes de redistribuir, criar nova audience no Gerenciador de Audiences para abrir espaço."
4. **Ação recomendada** — 1 a 3 ações concretas com handoff para skill executora. Priorizar a ação de maior impacto imediato (pausar perdedor > escalar winner > testar nova campanha).

---

## Handoffs típicos

| Achado | Para onde mandar |
|---|---|
| Candidato claro a escala (venda direta) com ROAS acima do mínimo e freq < 3.0 | "trafego-escalar" — modo vertical, velocidade gradual |
| Candidato claro a escala (captação de leads) com CPL abaixo do benchmark e freq < 3.0 | "trafego-escalar" — modo vertical, velocidade gradual |
| Candidato a escala (venda direta) com freq entre 3.0 e 3.5 | "trafego-escalar" — modo horizontal (nova audience ou novo adset) |
| Candidato a escala (captação de leads) com freq entre 3.0 e 3.5 | "trafego-escalar" — modo horizontal (nova audience ou novo adset) |
| Perdedor com gasto significativo (venda direta) | "trafego-otimizar" — atalho "pausar com filtro" (ROAS < 1 OU gasto > X + zero conversão) |
| Perdedor com gasto significativo (captação de leads) | "trafego-otimizar" — atalho "pausar com filtro" (CPL > 150% do benchmark OU gasto > X + zero leads) |
| Pulverização — nenhuma campanha > 25% do budget | "trafego-otimizar" — consolidar manualmente: pausar os menores e redirecionar |
| Top 1 concentra > 70% do budget | Duplicar entidade no Gerenciador (variando 1 dimensão) — duplicar variando criativo ou audience para criar redundância |
| Projeção do mês > 20% acima do mês anterior com piora de ROAS/CPL | "trafego-otimizar" — diagnóstico de ineficiência antes de continuar investindo |
| Budget esgotando antes do horário nobre (estimativa de hoje) | Gerenciador (Regras automáticas) — criar regra automática de alerta por budget diário |

---

## Mapeamento HTML (export via `_export-html.md`)

| Bloco do output narrado | Componente do design system |
|---|---|
| Projeção do mês — gasto, ritmo e estimativa (Bloco 1) | `.kpi-grid` com 4 a 5 `.kpi` — `.up` ou `.down` na variação vs. mês anterior |
| Comparativo mês atual vs. anterior | `.kpi` duplo lado a lado com `.up`/`.down` |
| Tabela de distribuição de orçamento por campanha (Bloco 2) | `.table` com colunas — `.up` na linha 🟢, `.down` na linha 🔴 |
| Alerta de ineficiência (campanha queimando) | `.regra.alerta` (um por campanha 🔴) |
| Tabela de candidatos a escala (Bloco 3) | `.table` com colunas — `--neon` na linha #1 |
| Alerta de dependência excessiva de winner | `.regra.alerta` |
| Cálculo de liberação potencial (Bloco 4) | `.metric` (número grande em `--neon`) para o valor total liberado |
| Redistribuição proposta — tirar/colocar (Bloco 5) | `.callout` (um para tirar, um para colocar) |
| Comparativo antes/depois da redistribuição | `.kpi` duplo com `.up` no "depois" |
| Frase "No VTSD isso significa..." | `.callout` |
| Ação recomendada | `.pitch-box` |
| Handoffs para skills executoras | `.term.next` dentro de `.terms` no rodapé |
