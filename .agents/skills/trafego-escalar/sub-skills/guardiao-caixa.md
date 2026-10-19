# Sub-skill. Guardião de Caixa

Módulo de proteção de caixa da conta inteira. Calcula gasto total, compara com teto, projeta até o fim do mês, identifica vazamentos e classifica urgência. Usado principalmente pela `/trafego-escalar` (antes de aprovar incremento e no modo carteira), mas referenciável por `/trafego-otimizar` e `/trafego-diagnostico` como leitura.

Tudo aqui é leitura: não passa pelo gate 🛡️. As ações que saem daqui (cortar vazamento, escalar vencedor) passam pelo gate da skill que executa.

## Quando é invocado

- Automaticamente no **modo carteira** da escalar (§3.6) como primeiro passo
- Antes do gate de confirmação (§11 da escalar) para validar que os incrementos propostos cabem no teto
- Quando o aluno pergunta "quanto estou gastando?", "meu caixa aguenta?", "onde estou vazando dinheiro?"

## Dados necessários

Consumir via `/trafego-insights`:
- `escopo: conta_completa`
- Campos: gasto (`spend`), orçamento (`daily_budget` ou `lifetime_budget`), compras, valor de compra, custo por compra
- Por campanha ativa: gasto no período, conversões, CPA, ROAS
- `teto_de_orcamento_diario_brl` do Passo 0.7 da escalar (input opcional)

> **Nomes de campo por modo** (mapa da §3.5.1 da `trafego-otimizar`): no MCP, compras vêm de `actions:omni_purchase`, CPA de `cost_per_action_type:omni_purchase`, ROAS de `purchase_roas` e o valor de compra é derivado (`purchase_roas × spend`); `actions` e `action_values` crus não existem na tool `ads_get_ad_entities`. No APP (curl), valem os nomes clássicos (`actions`, `action_values`, `cost_per_action_type`).

## O que calcula

### 1. Gasto total da conta

**Base canônica: `gasto_medio_7d`** (gasto real, não orçamento configurado).

```
gasto_medio_7d = soma de spend dos últimos 7 dias / 7
budget_configurado = soma de daily_budget de todas as campanhas/adsets ativos
```

Usar `gasto_medio_7d` como referência para urgência e projeção (é o gasto real). Usar `budget_configurado` apenas para validação de incrementos (orçamento pós-incremento não pode ultrapassar o teto).

### 2. Teto de referência

- Se o aluno declarou `teto_de_orcamento_diario_brl`: usar esse valor
- Se não declarou: usar `gasto_medio_7d` como base e avisar: "Sem teto declarado, uso o gasto médio recente (R$ {X}/dia) como referência."

### 3. Projeção mensal

```
dias_restantes_mes = último dia do mês - hoje
gasto_projetado_mes = gasto_medio_7d × dias_restantes_mes
gasto_acumulado_mes = soma de spend desde o dia 1 do mês
gasto_total_estimado = gasto_acumulado_mes + gasto_projetado_mes
```

Cada data (hoje, primeiro e último dia do mês) é calculada com uma chamada `date` separada, como manda a regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" do CLAUDE.md.

### 4. Vazamentos (campanhas que gastam sem retornar)

Para cada campanha ativa, calcular:
```
share_de_gasto = spend_campanha / spend_total
share_de_conversoes = purchases_campanha / purchases_total
eficiencia = share_de_conversoes / share_de_gasto
```

**Vazamento detectado quando:** `eficiencia < 0.5` (campanha consome mais de 2× sua fatia justa de gasto vs resultado).

**Conta sem conversões na janela:** se `purchases_total = 0`, a fórmula de eficiência não se aplica. Classificar todas as campanhas com gasto como vazamento potencial e declarar: "Sem conversões na janela, toda campanha é vazamento. Verificar pixel e evento de conversão." Handoff para `/trafego-pixel` (e `/pagina-pixel` se o pixel nem estiver instalado na página).

### 5. Validação de incrementos propostos

Quando a escalar propõe incrementos:
```
gasto_pos_incremento = gasto_diario_total + soma_dos_incrementos
folga = teto - gasto_pos_incremento
```

Se `folga < 0`: incrementos **ultrapassam o teto**. Alertar e propor ajuste.

## Classificação de urgência de caixa

| Nível | Critério | Significado |
|-------|----------|-------------|
| `caixa_seguro` | Gasto < 70% do teto E sem vazamentos E lucro/dia positivo | Margem confortável para escalar |
| `caixa_atencao` | Gasto entre 70 e 90% do teto OU 1 vazamento detectado OU margem apertada | Escalar com cautela, priorizar eficiência |
| `caixa_critico` | Gasto > 90% do teto OU lucro/dia negativo na conta OU 2+ vazamentos | NÃO escalar. Cortar vazamentos primeiro. |

## Mapa de caixa (saída visual)

```
MAPA DE CAIXA DA CONTA
Teto: R$ 500/dia (declarado) | Gasto atual: R$ 420/dia (84%)
Projeção mês: R$ 12.600 | Folga: R$ 80/dia
Urgência: ATENÇÃO ⚠️

Campanha              | Gasto/dia | % Gasto | Conversões | % Conv | Eficiência
──────────────────────|───────────|─────────|────────────|────────|──────────
Campanha A Perpétuo   | R$ 200    | 48%     | 12         | 67%    | 1.40 ✅
Campanha B Remarketing| R$ 80     | 19%     | 5          | 28%    | 1.47 ✅
Campanha C Lançamento | R$ 100    | 24%     | 1          | 5%     | 0.21 🔴
Teste Broad           | R$ 40     | 9%      | 0          | 0%     | 0.00 🔴

Vazamentos detectados:
🔴 Campanha C Lançamento: consome 24% do gasto, contribui 5% das vendas
🔴 Teste Broad: consome 9% sem nenhuma conversão

Recomendação:
- Cortar/reduzir Campanha C e Teste Broad libera R$ 140/dia (pela /trafego-otimizar)
- Essa folga pode escalar a Campanha A Perpétuo com segurança
```

## Explicação obrigatória

Cada classificação DEVE ter explicação:

### caixa_seguro
```
CAIXA: SEGURO ✅

Gasto atual R$ {X}/dia, teto R$ {Y}/dia ({Z}% utilizado).
Sem vazamentos. Lucro/dia positivo.

Há R$ {folga}/dia de margem para escalar sem ultrapassar o teto.
```

### caixa_atencao
```
CAIXA: ATENÇÃO ⚠️

Gasto atual R$ {X}/dia, teto R$ {Y}/dia ({Z}% utilizado).
{motivo: vazamento / margem apertada / próximo do teto}

Escalar é possível, mas priorize eficiência:
cortar vazamentos libera verba para vencedores.
```

### caixa_critico
```
CAIXA: CRÍTICO 🔴

Gasto atual R$ {X}/dia, teto R$ {Y}/dia ({Z}% utilizado).
{motivo: acima do teto / lucro negativo / múltiplos vazamentos}

NÃO escalar agora. Primeiro:
1. Cortar vazamentos ({lista}) pela /trafego-otimizar
2. Estabilizar lucro/dia
3. Depois considerar escala
```

## Output YAML

```yaml
guardiao_caixa:
  teto_diario_brl: 500.00
  teto_fonte: declarado | inferido_media_7d
  gasto_diario_atual: 420.00
  utilizacao_pct: 0.84
  folga_diaria_brl: 80.00
  projecao_mes_brl: 12600.00
  urgencia: caixa_seguro | caixa_atencao | caixa_critico

  campanhas:
    - id: "<id>"
      nome: "<nome>"
      gasto_diario: 200.00
      share_gasto: 0.48
      conversoes: 12
      share_conversoes: 0.67
      eficiencia: 1.40
      vazamento: false

  vazamentos:
    - id: "<id>"
      nome: "<nome>"
      gasto_diario: 100.00
      share_gasto: 0.24
      share_conversoes: 0.05
      eficiencia: 0.21
      recomendacao: "Cortar ou reduzir pela /trafego-otimizar. Libera R$ 100/dia."

  validacao_incrementos:
    incrementos_propostos_brl: 60.00
    gasto_pos_incremento: 480.00
    cabe_no_teto: true
    folga_pos_incremento: 20.00
```

## Referência por outras skills

- `/trafego-otimizar`: pode referenciar este módulo para dimensionar contenção ("quanto posso reduzir sem comprometer caixa?"). Leitura, não dependência dura.
- `/trafego-diagnostico`: pode usar `urgencia` e `vazamentos` no relatório de proteção de caixa. Leitura.
- Se a transversalidade crescer, considerar migrar para `/trafego-insights` como função utilitária.
