# Sub-fluxo. Regra Automática Meta Ads

Cria uma Automated Rule no Meta Ads que avalia campanhas/adsets/ads contra um trigger e executa uma ação (pausar, ajustar budget, notificar).

## Perguntas que cobre

- "Cria uma regra automática: se CPA passar de R$ 40, pausa o ad set"
- "Configura pra aumentar orçamento em 15% se ROAS estiver acima de 3"
- "Pausa anúncio se CTR cair abaixo de 0.5%"
- "Me notifica se gasto da campanha passar de R$ 500/dia"

## Inputs

### Trigger
| Campo | Opções |
|---|---|
| `metrica` | `cost_per_action_type:purchase` (CPA), `cost_per_action_type:lead` (CPL), `purchase_roas`, `ctr`, `frequency`, `spend`, `cpm`, `cpc` |
| `operador` | `GREATER_THAN`, `LESS_THAN` |
| `valor` | numérico em reais ou unidade da métrica |
| `janela_lookback` | `LAST_3_DAYS`, `LAST_7_DAYS`, `LAST_14_DAYS`, `LAST_30_DAYS`, `MAXIMUM`, `LIFETIME` |
| `gasto_minimo` | (recomendado) gasto mínimo na janela para a regra avaliar (evita decidir com pouco dado) |

### Ação
| Tipo | Campos |
|---|---|
| `PAUSE` | nenhum |
| `CHANGE_BUDGET` | `value` (% positivo ou negativo), `change_strategy` (`PERCENTAGE_OF_CURRENT_BUDGET`) |
| `NOTIFICATION` | `subscribers` (lista de user IDs do BM) |

### Scope
| Tipo | Como funciona |
|---|---|
| `CAMPAIGN_IDS` | regra aplica em campanhas específicas |
| `ADSET_IDS` | regra aplica em adsets específicos |
| `AD_IDS` | regra aplica em ads específicos |
| `ALL_ACTIVE` | todas as campanhas/adsets/ads ativos da conta |
| `ALL_ACTIVE` + `filter` | filtro por objective, name pattern, etc. |

## Endpoint

```
POST /act_<id>/adrules_library
{
  "name": "[FC] AutoRule-PauseCPAGT40-curso-tarot",
  "evaluation_spec": {
    "evaluation_type": "SCHEDULE",
    "filters": [{
      "field": "entity_type",
      "value": "ADSET",
      "operator": "EQUAL"
    }, {
      "field": "cost_per_action_type:offsite_conversion.fb_pixel_purchase",
      "value": 40.0,
      "operator": "GREATER_THAN",
      "time_preset": "LAST_3_DAYS"
    }, {
      "field": "spent",
      "value": 5000,                       // R$ 50 em centavos
      "operator": "GREATER_THAN",
      "time_preset": "LAST_3_DAYS"
    }]
  },
  "execution_spec": {
    "execution_type": "PAUSE",
    "execution_options": [{
      "field": "user_business_id",
      "value": "<bm_id>",
      "operator": "EQUAL"
    }]
  },
  "schedule_spec": {
    "schedule_type": "SEMI_HOURLY"        // avalia a cada 30 min
  },
  "status": "PAUSED"                        // sempre nasce PAUSED
}
```

## Receitas pré-configuradas (atalhos comuns)

A skill oferece atalhos para regras típicas:

### Receita 1. Pausar adset com CPA alto
```
Trigger: CPA > 1.4× ticket (na janela média da trilha)
        AND spend > 1× ticket (gasto mínimo)
Ação:    PAUSE adset
Scope:   adsets ativos com objective=OUTCOME_SALES
```

### Receita 2. Pausar ad com CTR baixo
```
Trigger: CTR < 0.5%
        AND spend > R$ 50
Ação:    PAUSE ad
Scope:   ads ativos
```

### Receita 3. Aumentar budget de adset com ROAS alto
```
Trigger: ROAS > 3.0
        AND spend > 2× ticket (validação)
Ação:    CHANGE_BUDGET +20%
Scope:   adsets ativos
```

### Receita 4. Pausar campanha com frequência alta
```
Trigger: Frequency > 4
        AND spend > R$ 200
Ação:    PAUSE campaign
Scope:   campanhas ativas
```

### Receita 5. Notificar (sem ação)
```
Trigger: Spend > R$ 500/dia (qualquer campanha)
Ação:    NOTIFICATION (sem mudar nada)
Scope:   todas as campanhas ativas
```

A skill apresenta as 5 receitas + opção "personalizada" e deixa o aluno escolher.

## Validação antes de criar

Antes do POST, a skill valida:

1. **Trigger faz sentido?** Ex: "CPA > R$ 1" em produto de R$ 500 vai pausar tudo na primeira venda.
2. **Gasto mínimo definido?** Sem isso, regra dispara com 1 conversão.
3. **Janela compatível com ticket?** High ticket (≥ R$1.500) precisa de janela ≥ 7 dias.
4. **Não conflita com outra regra ativa?** Listar regras existentes e checar overlap.

Se algo falhar, exibe alerta:

```
⚠️ Atenção:

A regra que você quer criar pode ter problemas:

- "CPA > R$ 40" sem gasto mínimo pode pausar adsets com 1 venda boa que custou R$ 50.
  Recomendado adicionar: AND spend > R$ 200 (4× CPA target).

Quer que eu adicione esse gasto mínimo automaticamente? (sim/não)
```

## Preview YAML

```yaml
sub_fluxo: regra_automatica
nome_final: "[FC] AutoRule-PauseCPAGT40-curso-tarot"
status_inicial: PAUSED

trigger:
  metrica: cost_per_action_type:purchase
  operador: GREATER_THAN
  valor: 40.0 (BRL)
  janela: LAST_3_DAYS
  guard_clause: spend > R$ 50 na mesma janela

acao:
  tipo: PAUSE
  alvo: adset

scope:
  tipo: ALL_ACTIVE
  filtro: objective=OUTCOME_SALES
  cobertura: 12 adsets ativos serão avaliados

cooldown: 24h
frequencia_avaliacao: a cada 30 min

confirma criar como PAUSED? (digite SIM)
```

## Após criar

```
✅ Regra criada (PAUSED): [FC] AutoRule-PauseCPAGT40-curso-tarot
   ID: 7654321098

A regra está PAUSED. Para ativar:
   POST /7654321098 { "status": "ENABLED" }

Ou rodar:
   /trafego-regras → opção "ativar regra"

Para ver histórico de execução:
   /trafego-regras → opção "histórico"

Comando de reversão:
   DELETE /7654321098
```

## Avisos

- **Regras Meta avaliam a cada 30 min** (default `SEMI_HOURLY`). Não é instantâneo.
- **Pausar via regra dispara reset de aprendizado** se a campanha estiver em fase de aprendizado ativa. Avisar.
- **Aumentar budget > 20% também dispara reset.** A skill recomenda cap de +20% por execução.
- **Limite Meta**: máximo de 200 regras por ad account.
- **Notificação chega no email do BM admin**, não no WhatsApp/Telegram. Para alerta no canal externo, usar sub-fluxo "resumo recorrente" + condicional na geração.
