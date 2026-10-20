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

**Disponibilidade do funil (seção 3 do SKILL.md):** no `APP`, puxar visita à página, carrinho e checkout iniciado pela Graph API (`insights?fields=actions`): funil completo, obrigatório. No `MCP_CONECTOR`, pedir no `ads_get_ad_entities` os campos conferidos `link_click`, `landing_page_view`, `omni_initiated_checkout` e `omni_purchase` (seção 3 do SKILL.md); carrinho só depois de confirmar com `ads_get_field_context`. Se a visita à página ou o checkout voltarem `null`, seguir a alternativa da seção 3 do SKILL.md: leitura guiada das colunas no Gerenciador de Anúncios (sem troca de modo). Só depois disso, e com a escolha do aluno, declarar o funil incompleto e usar CPA/ROAS como substitutos (funil: impressões → cliques → [lacuna] → conversões). **Nunca declarar o funil indisponível sem antes pedir os campos do conector e oferecer a leitura guiada.** O carrinho não entra nesse gatilho: sem ele (não confirmado no `ads_get_field_context` ou `null`), o funil segue visita à página → checkout iniciado → compra, com uma linha dizendo ao aluno que o carrinho não veio pelo conector e que, se ele quiser, dá para ler a coluna "Adições ao carrinho" no Gerenciador.

## Funil por etapas e gap

Para cada campanha/produto, montar o funil:

```
Funil pós-clique: Produto A (R$ 2.500, perpétuo)
Período: 25/05 a 31/05

Etapa             | Volume  | Taxa    | Custo/un  | Perda
──────────────────|─────────|─────────|───────────|──────────
Impressões        | 180.000 |         | R$ 0,014  |
Cliques no link   | 3.600   | CTR 2%  | R$ 0,69   |
Visitas à página  | 2.880   | 80%     | R$ 0,87   |
Cadastro/carrinho | 230     | 8%      | R$ 10,87  | ← MAIOR PERDA
Checkout iniciado | 45      | 19,6%   |           |
Compras           | 18      | 40%     | R$ 138,89 |

Maior perda: visita à página → cadastro (de 2.880 para 230 = 92% de perda)
Custo dessa perda: R$ 328/dia desperdiçados em visitas que não convertem
```

**Regra:** identificar a etapa com maior % de perda entre consecutivas. Essa é a "etapa de quebra" e o foco do diagnóstico.

**Julgar as taxas pela faixa de ticket (seção 3.5 do SKILL.md, ticket lido do resumo do produto), não por limiar fixo.** Connect rate (não muda com preço): saudável 80% ou mais, atenção de 60% a 79%, crítico abaixo de 60%; abaixo de 70%, a primeira hipótese é técnica (página lenta, link errado, redirecionamento), conforme a seção 3.5 do SKILL.md. Já conversão da página e conclusão de checkout dependem do ticket (ex.: alto ticket R$ 2.500 → página de 0,4% a 1,2%, checkout de 7% a 18%). Comparar a taxa do aluno com a faixa do ticket dele, sempre com etiqueta de confiança. Quando a conversão estiver abaixo da faixa mas houver campanhas de zero venda no escopo, declarar "média envenenada" (distribuição), não página ruim.

## Quantificação do gap em R$/dia

Para cada etapa de quebra, calcular:
```
Gap diário = (gasto_diario × taxa_perda_na_etapa)
```

Exemplo: "Entre a visita à página e o cadastro, você perde 92% do tráfego. Com gasto de R$ 357/dia, isso são R$ 328/dia em visitas que chegam na página mas não demonstram interesse."

## Comparação temporal

Funil atual vs anterior (mesmo tamanho de janela):

```
Evolução do funil (últimos 7d vs 7d anteriores):

Etapa                                                  | Anterior | Atual  | Variação | Direção
───────────────────────────────────────────────────────|──────────|────────|──────────|──────────
Connect rate (visitas ÷ cliques)                       | 82%      | 80%    | -2,4%    | estável
Visita à página → cadastro                             | 10%      | 8%     | -20%     | piorando ⚠️
Cadastro → checkout iniciado                           | 22%      | 19,6%  | -10,9%   | piorando
Conclusão de checkout (compras ÷ checkouts iniciados)  | 45%      | 40%    | -11,1%   | piorando
```

## Mobile vs desktop

Pedir breakdown `device_platform` via insights. Se houver diferença significativa:

```
⚠️ Conversão no celular muito inferior:
- Computador: taxa de cadastro 12%, CPA R$ 95
- Celular: taxa de cadastro 5%, CPA R$ 220

A experiência da página no celular pode estar prejudicando.
Medir a velocidade e a usabilidade no celular com /pagina-performance.
```

## Explicação obrigatória

Cada etapa DEVE ter explicação:

```
ETAPA DE QUEBRA: visita à página → cadastro (92% de perda)

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
    taxa_visita_cadastro: 0.080              # cadastro ou carrinho ÷ visitas à página
    taxa_conversao_pagina_perpetuo: 0.00625  # compras ÷ visitas à página (/trafego-insights §5.1)
    taxa_checkout_compra: 0.400
    taxa_carrinho_compra: 0.078

  etapa_de_quebra: lpv_to_lead
  perda_pct: 0.920
  gap_diario_brl: 328.00

  comparacao_temporal:
    connect_rate: { anterior: 0.82, atual: 0.80, direcao: estavel }
    taxa_visita_cadastro: { anterior: 0.10, atual: 0.08, direcao: piorando }

  mobile_vs_desktop:
    mobile: { taxa_visita_cadastro: 0.05, cpa: 220.00 }
    desktop: { taxa_visita_cadastro: 0.12, cpa: 95.00 }
    alerta_mobile: true
```
