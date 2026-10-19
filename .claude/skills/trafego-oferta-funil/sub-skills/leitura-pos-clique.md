# Sub-skill. Leitura Pós-Clique

Mapeia o funil completo pós-clique e identifica em qual etapa a maior perda acontece. Diferente da `/trafego-analise` output [2] (que narra o funil), esta sub-skill **quantifica o gap em R$/dia** e contextualiza para diagnóstico de página/oferta.

## Contexto multi-produto

Roda **por produto**. Cada produto tem funil e benchmarks diferentes (perpétuo tem checkout, lançamento tem captação).

## Quando é acionado

- Opção [2] do menu principal
- Automaticamente no Diagnóstico Completo (primeiro módulo)
- Quando o aluno pergunta "onde o funil quebra?" ou "o problema é no tráfego ou na página?"

## Dados necessários

Consumir via `/trafego-insights` (NÃO recalcular):
- `funil_por_campanha()` para cada campanha do escopo
- Métricas derivadas (nomes exatos da seção 5.1 da `/trafego-insights`): `connect_rate`, `taxa_conversao_pagina_perpetuo` ou `taxa_conversao_pagina_lancamento` (conforme tipo de funil), `taxa_carrinho_compra`, `taxa_checkout_compra`
- Custos por etapa: custo_por_lp_view, custo_por_atc, custo_por_ic, custo_por_purchase
- `serie_diaria` para comparação temporal
- Período atual + anterior

**Disponibilidade do funil (seção 3 do SKILL.md):** no `APP`, puxar visita à página, carrinho e checkout iniciado pela Graph API (`insights?fields=actions`): funil completo, obrigatório. No `MCP_CONECTOR`, descobrir na hora com `ads_get_field_context` quais campos de ação o `ads_get_ad_entities` aceita (visita à página, carrinho, checkout iniciado) e pedir os que existirem. Se não vierem, seguir a alternativa da seção 3 do SKILL.md: leitura guiada das colunas no Gerenciador de Anúncios ou troca para o modo App pelo `/trafego-conexao`. Só depois disso, e com a escolha do aluno, declarar o funil incompleto e usar CPA/ROAS como substitutos (funil: impressões → cliques → [lacuna] → conversões). **Nunca declarar o funil indisponível sem antes tentar os campos do MCP e oferecer a leitura guiada.**

## Funil por etapas e gap

Para cada campanha/produto, montar o funil:

```
Funil pós-clique: Produto A (R$ 2.500, perpétuo)
Período: 25/05 a 31/05

Etapa            | Volume  | Taxa    | Custo/un  | Perda
─────────────────|─────────|─────────|───────────|──────────
Impressões       | 180.000 |         | R$ 0,014  |
Cliques no link  | 3.600   | CTR 2%  | R$ 0,69   |
Landing Page View| 2.880   | 80%     | R$ 0,87   |
Lead/ATC         | 230     | 8%      | R$ 10,87  | ← MAIOR GAP
Init Checkout    | 45      | 19,6%   |           |
Purchase         | 18      | 40%     | R$ 138,89 |

Maior perda: LPV → Lead (de 2.880 para 230 = 92% de perda)
Custo desse gap: R$ 2.187/dia desperdiçados em visitas que não convertem
```

**Regra:** identificar a etapa com maior % de perda entre consecutivas. Essa é a "etapa de quebra" e o foco do diagnóstico.

**Julgar as taxas pela faixa de ticket (seção 3.5 do SKILL.md, ticket lido do resumo do produto), não por limiar fixo.** Connect rate bom acima de 70% (não muda com preço). Já conversão da página e conclusão de checkout dependem do ticket (ex.: alto ticket R$ 2.500 → página de 0,4% a 1,2%, checkout de 7% a 18%). Comparar a taxa do aluno com a faixa do ticket dele, sempre com etiqueta de confiança. Quando a conversão estiver abaixo da faixa mas houver campanhas de zero venda no escopo, declarar "média envenenada" (distribuição), não página ruim.

## Quantificação do gap em R$/dia

Para cada etapa de quebra, calcular:
```
Gap diário = (gasto_diario × taxa_perda_na_etapa)
```

Exemplo: "Entre LPV e Lead, você perde 92% do tráfego. Com gasto de R$ 357/dia, isso são R$ 328/dia em visitas que chegam na página mas não demonstram interesse."

## Comparação temporal

Funil atual vs anterior (mesmo tamanho de janela):

```
Evolução do funil (últimos 7d vs 7d anteriores):

Etapa                          | Anterior | Atual  | Variação | Direção
───────────────────────────────|──────────|────────|──────────|──────────
connect_rate                   | 82%      | 80%    | -2,4%    | estável
taxa_conversao_pagina          | 10%      | 8%     | -20%     | piorando ⚠️
taxa_checkout_compra           | 22%      | 19,6%  | -10,9%   | piorando
taxa_carrinho_compra           | 45%      | 40%    | -11,1%   | piorando
```

## Mobile vs desktop

Pedir breakdown `device_platform` via insights. Se houver diferença significativa:

```
⚠️ Conversão mobile muito inferior:
- Desktop: Lead Rate 12%, CPA R$ 95
- Mobile: Lead Rate 5%, CPA R$ 220

A experiência da página no celular pode estar prejudicando.
Medir a velocidade e a usabilidade no celular com /pagina-performance.
```

## Explicação obrigatória

Cada etapa DEVE ter explicação:

```
ETAPA DE QUEBRA: LPV → Lead (92% de perda)

O que significa: 2.880 pessoas chegam na sua página por dia,
mas apenas 230 (8%) demonstram interesse na oferta (seja
preenchendo um formulário, clicando em comprar ou adicionando
ao carrinho).

Por que importa: você está pagando R$ 0,87 por cada visita
à página. Dessas visitas, 92% vão embora sem fazer nada.
Isso custa R$ 328/dia em tráfego desperdiçado.

O que isso sugere: o problema provavelmente está na PÁGINA
ou na OFERTA, não no tráfego (CTR 2% e connect rate 80%
indicam que o criativo e o link funcionam).
```

## Output YAML

```yaml
leitura_pos_clique:
  produto: "Produto A"
  periodo: { atual: "2026-05-25 a 2026-05-31", anterior: "2026-05-18 a 2026-05-24" }

  funil:
    impressions: 180000
    link_clicks: 3600
    lp_views: 2880
    leads_ou_atc: 230
    initiate_checkout: 45
    purchases: 18

  taxas:
    ctr: 0.020
    connect_rate: 0.800
    taxa_conversao_pagina: 0.080
    taxa_checkout_compra: 0.196
    taxa_carrinho_compra: 0.400

  etapa_de_quebra: lpv_to_lead
  perda_pct: 0.920
  gap_diario_brl: 328.00

  comparacao_temporal:
    connect_rate: { anterior: 0.82, atual: 0.80, direcao: estavel }
    taxa_conversao_pagina: { anterior: 0.10, atual: 0.08, direcao: piorando }

  mobile_vs_desktop:
    mobile: { taxa_conversao_pagina: 0.05, cpa: 220.00 }
    desktop: { taxa_conversao_pagina: 0.12, cpa: 95.00 }
    alerta_mobile: true
```
