# Output [1]. Diagnóstico Rápido (60 segundos)

Visão geral pragmática que cabe numa olhada. Para o aluno que abre o projeto e quer saber: "está tudo bem com minhas campanhas hoje?".

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

O `trafego_processar.py` faz isso automaticamente ao processar o cache do `trafego_fetch.py`. Não adicionar `landing_page_views` como campo separado na chamada: a API retorna HTTP 400.

### Chamadas adicionais (executar antes de montar os blocos)

**IMPORTANTE: regras da Graph API que causaram erros reais:**
- `effective_status` é parâmetro válido SOMENTE no endpoint `/campaigns`. **Nunca usar no endpoint `/insights`**: a API ignora silenciosamente ou retorna resultado vazio.
- Não usar `curl` com arrays JSON (`["ACTIVE"]`) no shell. O quoting varia entre Windows e Mac e causa "unexpected token". Usar sempre o `trafego_fetch.py` via Python.

**Uso padrão (modo APP):**

Todas as chamadas 1a, 1b, 1c, 1d e 1e são feitas por um único script Python que salva em cache local. Isso evita rate limit, encoding issues e problemas de shell cross-platform:

```bash
{PY} .claude/skills/trafego-analise/scripts/trafego_fetch.py \
  --account {AD_ACCOUNT_ID_ATUAL} \
  --filtro "{ESCOPO_FILTRO_TEXTO}" \
  --periodo {PERIODO} \
  --status "{STATUS_FILTRO_LISTA}" \
  --output diagnostico \
  --project-root . \
  --cache-dir meus-produtos/{ativo}/trafego/analise/cache
```

`{PY}` é o interpretador detectado na sessão (`python3` ou `py -3`). `{PERIODO}` é o preset do Passo 3 (`last_7d`, `last_14d` ou `last_30d`); no período customizado, trocar `--periodo {PERIODO}` por `--since AAAA-MM-DD --until AAAA-MM-DD`. `{STATUS_FILTRO_LISTA}` vem do Passo 0.55 do `SKILL.md` (ex: `ACTIVE,PAUSED,WITH_ISSUES`). `{ativo}` é o produto lido em `meus-produtos/.ativo`. Depois, rodar o `trafego_processar.py` com os mesmos argumentos (inclusive `--status` e o mesmo `--cache-dir`), `--ticket` com o preço do `resumo-produto.md` e, em conta de captação, `--cpl-alvo {CPL_ALVO}` com o CPL-alvo do resumo ou perguntado ao aluno (Passo 4 do `SKILL.md`).

O script faz a Chamada 0 (lista as campanhas com o status escolhido) e as 5 chamadas abaixo em sequência, com retry em rate limit, e salva o resultado em `meus-produtos/{ativo}/trafego/analise/cache/{account}_{periodo}_{filtro}_{status}_{output}.json` (sem `--cache-dir`, o script cai na pasta reserva `skill-analise/cache/`; por isso o caminho do produto vai sempre). O cache só é reaproveitado no mesmo dia; se o fetch devolver `{"error": ...}`, parar e explicar ao aluno que a Meta não respondeu, sem rodar o processar (Passo 4 do `SKILL.md`).

**Chamada 1b. Comparativo WoW (dentro do fetch):**

Busca a janela imediatamente **anterior**, do mesmo tamanho do período principal, via `time_range` fechado (uma linha agregada por campanha: **sem** `time_increment`). A janela termina 1 dia antes do início do período principal, ancorada no `date_start` que a Meta devolveu no 1a (no customizado, nas datas informadas):

| Período principal (1a) | Janela anterior (1b) |
|---|---|
| `last_7d` → `[hoje-7, hoje-1]` | `[hoje-14, hoje-8]` |
| `last_14d` → `[hoje-14, hoje-1]` | `[hoje-28, hoje-15]` |
| `last_30d` → `[hoje-30, hoje-1]` | `[hoje-60, hoje-31]` |

O `trafego_processar.py` compara o **agregado inteiro de 1a (atual) contra o agregado inteiro de 1b (anterior)**. Nunca fatiar 1b ao meio: todas as linhas de 1b têm a mesma `date_start`, então o split geraria dois pedaços da mesma semana anterior (comparativo falso). A contagem de campanhas pode diferir entre 1a e 1b (campanhas ligadas/pausadas entre as semanas): isso é esperado num WoW de grupo.

**Chamada 1c. Orçamentos** (endpoint `/campaigns`, único que aceita `effective_status`; o fetch reaproveita a lista da Chamada 0):

`budget_remaining` só é populado para campanhas com **lifetime budget**. Para **daily budget**, cruzar `spend_hoje` (Chamada 1d) com `daily_budget` manualmente. No modo APP (Graph API), os orçamentos vêm como número em centavos: dividir por 100 para obter reais. No modo MCP_CONECTOR, o `daily_budget` vem como objeto com moeda, já em reais: usar o valor como veio (número puro, em qualquer modo, é centavos).

**Chamada 1d. Gasto de hoje** (endpoint `/insights`, sem `effective_status`):

`date_preset=today` no endpoint de insights. O parâmetro `effective_status` **não existe** em insights: o filtro de status é feito no pós-processamento comparando os IDs das campanhas da Chamada 0 (as mesmas da 1c).

**Chamada 1e. Série diária** (endpoint `/insights`, nível campanha + `time_increment=1`):

Puxa uma linha por campanha por dia no período principal, com o mesmo filtro de nome e status do 1a. O `trafego_processar.py` agrupa por `date_start` e entrega `serie_diaria` (lista por dia) + `serie_diaria_svg` (geometria pronta do gráfico de linha). A soma diária fecha com o agregado do 1a (mesma janela, mesmo filtro). Usado só para o gráfico de tendência do HTML: não entra em nenhuma das 5 respostas narradas.

**Modo MCP_CONECTOR:** sem scripts e sem token. Usar `mcp__*__ads_get_ad_entities` em nível campanha (`level: "campaign"`, `limit: 1000`, filtro `campaign.impressions` maior que zero) para 1a (período atual), 1b (janela anterior do mesmo tamanho, `time_range` em texto JSON), 1c (orçamentos) e 1d (gasto de hoje, `date_preset: "today"`), com os campos conferidos do conector (ver **Contrato anti-erros** no `SKILL.md`). A série diária (1e) sai da mesma tool, em nível campanha, com `time_increment: "1"` no período do 1a, agrupada por `date_start` só com as campanhas do escopo: assim a soma diária fecha com o 1a. `mcp__*__ads_insights_performance_trend` só serve quando o escopo é a conta inteira (`conta_completa`): ela não faz nível campanha e não respeita o filtro de escopo. Aplicar o filtro de status cruzando com a lista de campanhas do Passo 0.6 do `SKILL.md`.

### Referência de produto (benchmarks)

Ler do `resumo-produto.md` (já carregado no Passo 0.1 do `SKILL.md`): preço e tipo de produto. Não perguntar de novo. Inferir tipo de funil pelo objetivo predominante das campanhas (`OUTCOME_LEADS` = captação; `OUTCOME_SALES` = venda direta).

| Tipo de funil | Ticket | ROAS mínimo saudável | CPA máximo saudável |
|---|---|---|---|
| Venda direta: low ticket | ≤ R$ 97 | 2.5x | ticket × 0.40 |
| Venda direta: ticket médio | R$ 98 a R$ 497 | 3.0x | ticket × 0.30 |
| Venda direta: high ticket | > R$ 497 | 4.0x | ticket × 0.25 |
| Captação de leads | qualquer | - | CPL-alvo: perguntar ao aluno se não estiver no resumo |

---

## O que entregar

> **REGRA:** as seções abaixo seguem a ordem das perguntas obrigatórias. Responda TODAS as perguntas antes de incluir qualquer análise adicional. Não omitir nenhuma.

### Resposta 1. "Qual campanha está queimando mais dinheiro sem resultado?"

Critério: campanha com `spend` > R$ 50 no período E conversões = 0 (usando tipo canônico: `offsite_conversion.fb_pixel_purchase` para vendas; para captação, a contagem de leads da tabela de deduplicação do command: `lead` e, sem ele, `offsite_conversion.fb_pixel_lead`, nunca a soma).

Montar ranking das top 3 campanhas por gasto com zero resultado:

```
🚨 [QUEIMA]  {nome_campanha}
   Gasto: R$ {X} em {N} dias  ·  Conversões: 0
   CPA implícito: infinito, cada real investido aqui está sendo descartado
   Ação: pausar via "trafego-otimizar", atalho "pausar com filtro" (gasto > X + zero conversão)
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
   Mesmo público viu o criativo {X} vezes: leilão encarecendo, resposta caindo
   Ação: criar nova audience via "trafego-publicos" (Lookalike ou público aberto) ou expandir targeting
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
Campanhas ativas         {N}               -                   -
```

As linhas "Compras / Leads" e "CPA / CPL" usam a mesma métrica nas duas colunas, a indicada em `wow.metrica` (`compras` ou `leads`): rotular a linha conforme ela. Se `cpa_atual` vier nulo (nenhuma conversão no período atual), mostrar "sem vendas no período" (ou "sem leads no período") no lugar do valor e da variação, nunca "-100%".

Se a Chamada 1b não retornar dados comparativos (ex: período customizado muito antigo, ou a Meta não respondeu e o processar avisou em `avisos`), suprimir a coluna "Período anterior" e mostrar só os valores atuais, informando o motivo.

---

### Resposta 4. "Alguma campanha estourou o orçamento diário hoje?"

Critério: `spend_hoje` (Chamada 1d) ≥ 90% de `daily_budget` (Chamada 1c).

Para campanhas com **daily budget**: restante = `daily_budget` − `spend_hoje` (cálculo manual, API não expõe este campo).
Para campanhas com **lifetime budget**: usar `budget_remaining` da Chamada 1c diretamente.

```
🚨 [BUDGET]  {nome_campanha}
   Gasto hoje: R$ {X}  ·  Budget diário: R$ {Y}  ·  Restante estimado: R$ {Z}
   Risco: orçamento pode esgotar antes do horário nobre (18h-22h), pausando a veiculação
   Ação: aumentar budget via "trafego-escalar" OU criar regra de alerta via "trafego-regras"
```

Se restante = 0 E campanha ainda ativa → sinal crítico imediato, listar no topo independente da ordem.

Se nenhuma campanha atingiu 90% do budget diário, responder explicitamente: "Nenhuma campanha com orçamento diário esgotado ou próximo do limite hoje."

---

### Resposta 5. "Como está a saúde geral da minha conta? (Health Score)"

Calculado inteiramente a partir dos dados disponíveis nas chamadas 1a, 1b, 1c, 1d. Fórmula operacional:

```
Score = (D1 × 0.20) + (D2 × 0.20) + (D3 × 0.25) + (D4 × 0.25) + (D5 × 0.10)
```

#### Dimensão 1. Diversidade criativa (peso 20%)

Proxy: número de campanhas ativas com `spend` > R$ 10 no período. A contagem real da Mandala (18 tipos) só é verificável no output [3].

| Campanhas ativas com gasto | Pontos |
|---|---|
| ≥ 10 | 100 |
| 6 a 9 | 75 |
| 3 a 5 | 50 |
| 2 | 30 |
| 1 | 15 |
| 0 | 0 |

#### Dimensão 2. Saúde de públicos (peso 20%)

Percentual de campanhas ativas com `frequency` ≤ 3.

| % campanhas com freq ≤ 3 | Pontos |
|---|---|
| 100% | 100 |
| 75% a 99% | 80 |
| 50% a 74% | 55 |
| 25% a 49% | 30 |
| < 25% | 10 |

Penalidade: se qualquer campanha tiver `frequency` > 6, subtrair 10 pontos desta dimensão (mínimo 0).

#### Dimensão 3. Eficiência de funil (peso 25%)

Connect rate = `landing_page_view` (do array `actions`) / `link_click` (do array `actions`), somando todas as campanhas.

**Por que `link_click` e não `clicks`:**
- `clicks` (campo de topo) inclui cliques em qualquer lugar do post (curtir, expandir, ver mais, etc.)
- `link_click` (dentro de `actions`) representa apenas cliques que abrem o link de destino
- Usar `clicks` inflaria artificialmente o denominador e produziria um Connect Rate falso (ex: 12% em vez de 58%)
- O `trafego_processar.py` usa `link_click` do array `actions` automaticamente, com fallback para `clicks` se `link_click` não estiver disponível

| Connect Rate | Pontos |
|---|---|
| ≥ 80% | 100 |
| 70% a 79% | 75 |
| 65% a 69% | 50 |
| 60% a 64% | 25 |
| < 60% | 10 |

Os degraus seguem a régua única do Connect Rate (a mesma da §3.5 de `trafego-oferta-funil/SKILL.md`): 80% ou mais saudável (nota máxima), 60% a 79% atenção, abaixo de 60% crítico (pior nota). Abaixo de 70%, a primeira hipótese é técnica (página lenta, link errado, redirecionamento): conferir com `/pagina-performance` e a congruência anúncio x página com `/trafego-oferta-funil` antes de mexer no anúncio.

Se `landing_page_view` não retornar para nenhuma campanha (pixel sem evento de LP view configurado): usar CTR médio como fallback.

| CTR médio (fallback) | Pontos |
|---|---|
| ≥ 2% | 80 |
| 1% a 1.99% | 55 |
| < 1% | 25 |

#### Dimensão 4. Performance financeira (peso 25%)

Para funil de **venda direta**: ROAS médio ponderado por spend (soma de `action_values` / soma de `spend`, usando tipo canônico de compra).

| ROAS médio | Pontos |
|---|---|
| ≥ 4.0x | 100 |
| 3.0x a 3.9x | 85 |
| 2.0x a 2.9x | 65 |
| 1.5x a 1.9x | 40 |
| 1.0x a 1.4x | 20 |
| < 1.0x | 0 |

Para funil de **captação de leads** (nenhuma compra no período nem na janela anterior): CPL médio (gasto ÷ leads, com a contagem de leads da tabela de deduplicação do command) vs. CPL-alvo do produto. O CPL-alvo vem do resumo ou é perguntado ao aluno e vai no `--cpl-alvo` do processar; sem ele, o D4 fica neutro (50) e o processar avisa em `avisos`.

| CPL vs. benchmark | Pontos |
|---|---|
| ≤ 60% do benchmark | 100 |
| 61% a 80% | 80 |
| 81% a 100% | 60 |
| 101% a 130% | 35 |
| > 130% | 10 |

Se conversões = 0 em todas as campanhas (pixel não rastreando): atribuir 0 pontos e alertar o aluno separadamente.

#### Dimensão 5. Consistência temporal (peso 10%)

Requer Chamada 1b. Calcular variação de CPA (ou CPL) semana atual vs. semana anterior, com a mesma métrica nas duas janelas (compras se qualquer uma teve compra; senão, leads). Sem conversão no período atual e com conversão na janela anterior, a conta parou de converter: o D5 recebe a pior faixa (10) e o processar marca `d5.rotulo` = `parou de converter`. Sem conversão nas duas janelas, a variação não é calculada e o D5 fica neutro.

| Variação WoW do CPA | Pontos |
|---|---|
| Melhora ou estável (≤ +20%) | 100 |
| Aumento +21% a +30% | 70 |
| Aumento +31% a +50% | 40 |
| Aumento > +50% | 10 |
| Parou de converter (zero conversões agora, com conversões na janela anterior) | 10 |
| Sem dados comparativos | 50 (neutro) |

#### Apresentação do score

```
HEALTH SCORE: {XX}/100  {emoji}

  Diversidade criativa    {D1}/100  (peso 20%)  →  {N} campanhas ativas com gasto
  Saúde de públicos       {D2}/100  (peso 20%)  →  {X%} com frequência ≤ 3
  Eficiência de funil     {D3}/100  (peso 25%)  →  Connect Rate {Y%}
  Performance financeira  {D4}/100  (peso 25%)  →  {TEXTO_D4}
  Consistência temporal   {D5}/100  (peso 10%)  →  {CPA ou CPL} {+/-V%} vs. período anterior
```

`{TEXTO_D4}` depende do tipo de conta (campos de `health.dimensoes.d4` do processar):
- Venda direta: `ROAS médio {Z}x  (benchmark: {W}x)`, com `roas` e `roas_benchmark`.
- Captação com CPL-alvo: `CPL R$ {cpl}  (alvo: R$ {cpl_alvo})`.
- Captação sem CPL-alvo (`sem_referencia` verdadeiro): `CPL R$ {cpl}, sem CPL-alvo: nota neutra`.
- Captação sem nenhum lead no período (`cpl` vazio, nota 0): `nenhum lead no período`.

Na linha do D5, escrever `CPA` quando `d5.metrica` for `compras` e `CPL` quando for `leads`. Com `d5.rotulo` = `parou de converter`, escrever `parou de converter: nenhuma {compra ou lead} no período, contra {CPA ou CPL} de R$ {cpa_anterior} no período anterior`. Sem `variacao_wow_pct` e sem esse rótulo (sem dados comparativos ou sem conversão nas duas janelas), escrever `sem dados comparativos`.

| Score final | Classificação | O que significa |
|---|---|---|
| 85 a 100 | 🟢 Excelente | Conta saudável: foco em escala |
| 70 a 84 | 🟡 Boa | Funcionando bem: otimizações pontuais |
| 50 a 69 | 🟠 Regular | Problemas específicos a resolver antes de escalar |
| 0 a 49 | 🔴 Crítica | Parar escalada: diagnóstico profundo urgente |

---

### Análise adicional. Próximo passo VTSD

Indicar em 1 linha qual output rodar a seguir, conforme o sintoma dominante identificado nas respostas acima:

| Situação | Output recomendado |
|---|---|
| Score < 50 OU 2+ sinais críticos simultâneos | [8] Problemas Ocultos |
| Fadiga ou saturação de público detectada | [3] Criativos & Copy |
| Queima de dinheiro > R$ 300 no período | [2] Performance & Funil (ranking por ROAS) |
| Budget estourando antes das 18h | [9] Orçamento & Projeção |
| Connect Rate < 60% (crítico) | [2] Performance & Funil (gargalo de funil) |
| Score ≥ 85, sem sinais críticos | [9] Orçamento & Projeção (quem escalar) |

---

## Estrutura de resposta obrigatória

Para cada pergunta listada em "Perguntas que cobre", gerar uma seção numerada com o texto da pergunta como título. A seção deve conter os dados e diagnóstico que respondem aquela pergunta diretamente. Não omitir nenhuma pergunta.

Só após cobrir todas as perguntas obrigatórias, incluir blocos adicionais de análise.

**Verificação final:** antes de entregar, confirmar que cada pergunta tem uma seção de resposta no output. Acrescentar as que faltarem.

---

### Passo 0. Checklist antes de montar qualquer bloco

Antes de escrever qualquer bloco, mapear cada pergunta obrigatória e confirmar cobertura:

```
[ ] Qual campanha está queimando mais dinheiro sem resultado?
    → coberto? Se não: calcular CPR e rankear campanhas por gasto/resultado, identificando a maior queimadora

[ ] Tem algum anúncio com frequência alta e CTR caindo? (fadiga de criativo)
    → coberto? Se não: verificar frequência >= 4 e queda de CTR WoW em cada anúncio ativo

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

1. **Diagnóstico**: apresentar Bloco 1 (números com WoW) e informar quantos sinais críticos foram identificados.
2. **Causa provável**: o que os sinais do Bloco 2 sugerem em conjunto. Ex: "dois sinais de fadiga + frequência alta = criativo esgotado, não é problema de público"; "queima de dinheiro sem conversão = pixel provavelmente misconfigured ou página quebrando".
3. **No VTSD, isso significa…**: ex: "Score 92 + ROAS subindo = Identidade do Consumidor bem calibrada, Quadro na Parede chegando ao público certo. Hora de escalar." Ou: "Frequência > 4 em 3 campanhas = o mesmo criativo atingiu as mesmas pessoas muitas vezes. A Urgência Oculta esgotou. Precisamos de novos ângulos pela Mandala."
4. **Ação recomendada**: 1 a 3 ações concretas com handoff para a skill executora.

---

## Handoffs típicos

| Sinal predominante | Para onde mandar |
|---|---|
| Queima de dinheiro | "trafego-otimizar": ações em lote: pausar campanhas com gasto > X e zero conversão |
| Fadiga de criativo | "trafego-testes" (A/B de criativo novo) ou "trafego-publicos" (nova audience) |
| Conta saudável + ROAS alto | "trafego-escalar": aumentar budget das campanhas vencedoras |
| Budget estourando | "trafego-regras": criar regra automática de freio por budget diário |
| Connect Rate baixo | "trafego-oferta-funil" para confirmar o gargalo; correção em "pagina-performance" (velocidade, URL/redirect) ou "feedback-pagina" (promessa da página). O gargalo está na página, não no anúncio |
| Pixel sem conversão | "trafego-pixel": diagnóstico aprofundado do rastreamento (reinstalar o pixel na página: "pagina-pixel") |
| Anomalia sem padrão claro (múltiplos sinais conflitantes) | "trafego-diagnostico": diagnóstico diferencial com 3 hipóteses competitivas |
| Dúvida se o "vencedor" é real | "trafego-diagnostico" opção [4]: detector de falso vencedor |

---

## Mapeamento HTML (export via `_export-html.md`)

Componentes definidos na seção 3.2 do `_export-html.md`. **Usar exatamente estes nomes de classe.** O vocabulário antigo (`.kpi-grid`, `.regra`, `.metric`, `.callout`, `.pitch-box`, `.bar-row`) foi descontinuado e NÃO existe no CSS embutido: usá-lo gera seção sem estilo.

| Bloco do output narrado | Componente do design system |
|---|---|
| KPIs globais (gasto, vendas, receita, ROAS, CPA, Health Score) | `.stats-grid` com um `.stat-card` por métrica (`.value.green/.yellow/.red` conforme semântica) |
| Cada "Resposta N" obrigatória | `.section` com `.section-header` (`.section-num` + `.section-title` + `.section-question`) |
| Tabela comparativa atual vs. anterior | `table` padrão; variação colorida com `style="color:var(--green)"` ou `var(--red)` |
| Ranking de queima / demais rankings | `.card` + `table` com `.num` nas colunas numéricas e `.rank` na posição |
| Health Score total + classificação | `.stat-card` (valor grande, cor por faixa) |
| Detalhamento das 5 dimensões | `.dim-row` (`.dim-label` + `.dim-track`/`.dim-fill` + `.dim-score`), largura do fill proporcional ao score; cor do fill pela faixa do Health Score (verde ≥ 85, amarelo 70–84, laranja 50–69, vermelho < 50): a MESMA cor do vértice correspondente no radar |
| Diagnóstico / "No VTSD isso significa..." | `.diag-box` (+ `.green/.yellow/.red` conforme o sinal) |
| Ação recomendada | `.action-box` |
| Próximo output recomendado / handoffs | `.term.next` dentro de `.terms` no `.page-foot` |

### Gráficos obrigatórios deste output

Renderizar SEMPRE os 5 gráficos abaixo, logo após o `.stats-grid` de KPIs, sob um `.section-h` "Visão visual". Todos em SVG/CSS inline, sem dependência (receitas detalhadas na seção **3.2.1** do `_export-html.md`).

| Gráfico | Componente / receita | Fonte de dado | Posição |
|---|---|---|---|
| Tendência diária (gasto + vendas) | SVG linha eixo duplo (receita E) | `serie_diaria_svg` (pré-calculado) | `.chart-card` full-width, topo da "Visão visual" |
| Radar das 5 dimensões | SVG radar (receita A) | `health.dimensoes` | `.charts-grid`, 1ª coluna |
| Funil VTSD | `.funnel` (receita B) | `agregado`: impressions → link_clicks → lpv → purchases | `.charts-grid`, 2ª coluna |
| Barras atual vs. anterior | `.wow-chart` (receita C) | `wow` | `.chart-card` full-width sob o `.charts-grid` |
| Alocação: convertendo vs. queimando | `.hbar-row` (receita D) | `ranking_spend` (vendeu) + `sinais.queima` (zerou) | `.chart-card` dentro da Resposta 1 |

A série diária vem da **Chamada 1E** do `trafego_fetch.py` (nível campanha + `time_increment=1`, mesmo filtro do 1a) e é agregada por dia no `trafego_processar.py`, que já entrega a geometria SVG pronta em `serie_diaria_svg`. Se a série diária não vier (a Chamada 1E falhou, o que aparece em `avisos`, ou voltou vazia), `serie_diaria_svg` é `null`: nesse caso o gráfico de tendência é omitido, o aluno é avisado, e os outros 4 continuam. Cache antigo sem `1e` não é mais reaproveitado: o fetch busca de novo.

Regras dos gráficos: usar só cores da paleta (`--green/--yellow/--orange/--red/--accent`); truncar nomes longos de campanha; o radar colore cada vértice pela mesma faixa da classificação do Health Score (verde ≥ 85, amarelo 70–84, laranja 50–69, vermelho < 50), igual à cor da barra `.dim-fill` da dimensão correspondente na Resposta 5; o funil usa largura em escala logarítmica mas exibe os números reais e a taxa de conversão entre etapas.
