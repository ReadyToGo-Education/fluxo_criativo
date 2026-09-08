# Sub-fluxo. Ações em Lote por Filtro

Aplica uma ação (pausar, reduzir budget) em múltiplas entidades de uma vez, filtradas por critério. Diferente da otimização padrão (que age por campanha), aqui o aluno define um filtro e a skill aplica a todas as entidades que casam.

## Perguntas que cobre

- "Pausa tudo que tem ROAS abaixo de 1 nas últimas 2 semanas"
- "Reduz 20% o budget de todos os adsets com CPA > R$ 80"
- "Pausa todos os anúncios com CTR < 0.5% e gasto > R$ 100"
- "Pausa as campanhas ativas sem nenhuma conversão nos últimos 7 dias"

## Funções suportadas

| Função | Descrição |
|---|---|
| `pausar_em_lote(filtro)` | Pausa todas as entidades que batem o filtro |
| `reduzir_budget_em_lote(filtro, percent)` | Reduz budget % nas entidades que batem |
| `pausar_top_n_pior(metric, n)` | Pausa as N piores em uma métrica |
| `aumentar_top_n(metric, n, percent)` | Atalho para escala (delegar para `/trafego-escalar` quando faz sentido) |

## Sintaxe de filtro

A skill aceita filtro estruturado:

```yaml
escopo: ad | adset | campaign           # nível
periodo: today | last_3d | last_7d | last_14d | last_30d
condicoes:
  - metrica: roas
    operador: less_than
    valor: 1.0
  - metrica: spend
    operador: greater_than
    valor: 50.0                          # gasto mínimo (guard)
combinacao: AND                          # AND padrão; OR aceito
```

Ou descrição em linguagem natural que a skill traduz:
- "pausa tudo com ROAS < 1 últimas 2 semanas e gasto > R$ 50" → filtro acima

### Métricas suportadas no filtro

`roas`, `cpa`, `cpl`, `ctr_link_unico`, `ctr_link_total`, `ctr`, `frequency`, `cpm`, `spend`, `impressions`, `purchases`, `leads`, `cpc`, `link_clicks`.

> Para diagnóstico de criativo, prefira `ctr_link_unico` (`unique_inline_link_click_ctr`). `ctr_link_total` (`inline_link_click_ctr`) e `ctr` (geral) ficam disponíveis como complementares.

### Operadores
`less_than`, `less_than_or_equal`, `greater_than`, `greater_than_or_equal`, `equal`, `not_equal`, `between`.

## Validação antes de aplicar

A skill **sempre lista** o que vai acontecer antes de executar:

```
🔎 Filtro:
   roas < 1.0 AND spend > R$ 50 AND período = last_14d

📋 Vai aplicar PAUSE em 7 entidades:

   ❌ Pausará:
   1. [Adset] Tarot LAL1pct        ROAS 0.42, gasto R$ 380, conversões: 3
   2. [Adset] Tarot Broad-25-44    ROAS 0.78, gasto R$ 240, conversões: 5
   3. [Ad]    Tarot-criativo-A1    ROAS 0.65, gasto R$ 120, conversões: 2
   4. [Ad]    Tarot-criativo-B2    ROAS 0.50, gasto R$ 180, conversões: 3
   5. [Adset] Tarot Interesse-1    ROAS 0.91, gasto R$ 220, conversões: 6
   6. [Ad]    Tarot-criativo-C1    ROAS 0.70, gasto R$ 95,  conversões: 1
   7. [Adset] Tarot Saved-Iniciantes ROAS 0.88, gasto R$ 310, conversões: 4

⚠️ Vai disparar reset de aprendizado em 4 adsets ativos.

   Confirma pausar todos? (digite SIM)
```

## Implementação

```python
# 1. Puxar dados via /trafego-insights (escopo conta_completa, breakdowns conforme filtro)
data = trafego_insights(escopo='conta_completa', periodo=filtro.periodo, nivel='auto')

# 2. Aplicar filtro
matches = [e for e in data if matches_filter(e, filtro)]

# 3. Listar matches em preview
print_preview(matches)

# 4. Confirmação SIM
if confirmacao != "SIM": return

# 5. Aplicar ação
for entidade in matches:
    POST /<entidade.id> { "status": "PAUSED" }      # ou update_budget

# 6. Invalidar cache do /trafego-insights
invalidate_cache(account_id)

# 7. Salvar log da operação
log_acao_em_lote(matches, action, timestamp)
```

## Atalhos comuns (receitas)

| Receita | Filtro | Ação |
|---|---|---|
| **Pausar queimadores** | `roas<1 AND spend>50 AND last_14d` | PAUSE adset |
| **Pausar criativos mortos** | `ctr_link_unico<0.4 AND spend>50 AND last_7d` | PAUSE ad |
| **Pausar por frequência** | `frequency>4.5 AND last_7d` | PAUSE adset |
| **Reduzir CPA alto** | `cpa>1.5x_target AND last_7d` | budget -20% |
| **Pausar sem conversão** | `purchases=0 AND spend>100 AND last_7d` | PAUSE adset |
| **Pausar 5 piores ROAS** | `top_n=5 metric=roas asc` | PAUSE adset |

A skill apresenta a lista de receitas + opção "filtro custom" e deixa o aluno escolher.

## Output

```yaml
operacao: acao_lote
filtro: { ... }
acao: pause | reduce_budget
total_avaliado: 23 (entidades verificadas)
matches: 7 (entidades que bateram o filtro)
aplicado: 7 ✅
falhou: 0

entidades_afetadas:
  - { id: ..., tipo: adset, nome: "...", metrica_no_momento: "ROAS=0.42, spend=380", acao: paused }
  - ...

resets_aprendizado_disparados: 4

rollback:
  - DELETE-or-reactivate /6111111
  - DELETE-or-reactivate /6222222
  - ...
```

## Avisos

- **Pausar com filtro disparou reset de aprendizado** se o adset estava em learning. Confirmação extra para essas entidades.
- **Limite de segurança**: a skill bloqueia ações que afetam > 50% dos adsets ativos da conta sem confirmação tripla.
- **Não combinar com `/trafego-otimizar` padrão na mesma conversa.** Se otimização individual já pausou, ações em lote vão sobrescrever sem ganho.
- **Não usar para escala.** Para "aumentar 20% nas top 3", encaminhar para `/trafego-escalar`. Aqui apenas atalho.
