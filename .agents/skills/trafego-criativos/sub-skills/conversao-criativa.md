# Sub-skill. Conversão Criativa

Avalia se o criativo atrai comprador/lead qualificado ou apenas curioso. Diferente do output [3] (CPA por formato, ROAS por tier), esta sub-skill cruza **performance do criativo com temperatura do público** (cold vs warm), calcula métricas de conversão por etapa e identifica o gap atenção-conversão.

## Contexto multi-produto

Roda **por produto**. Cada produto tem ticket e CPA target diferentes, então benchmarks de conversão são específicos.

## Quando é acionado

- Opção [4] do menu principal
- Automaticamente na Inteligência Completa (terceiro módulo)
- Quando o aluno pergunta "atrai comprador ou só curioso?" ou "esse criativo converte?"

## Dados necessários

Pedir à `/trafego-insights`:
- Nível: `ad` + `adset` (para detectar temperatura do público)
- Campos de conversão: `actions[purchase, lead, add_to_cart, initiate_checkout]`, `action_values`, `cost_per_action_type`
- Campos base: `landing_page_views` (dentro de actions), `impressions`, `video_3sec_views`, `spend`
- Período atual + anterior

Complementar (leitura pura, por modo):
- Segmentação de cada conjunto para detectar cold vs warm (públicos personalizados = warm, interesses ou semelhantes = cold), seguindo a escada da seção 4.5 do SKILL.md: no `MCP_CONECTOR`, `ads_get_ad_account_custom_audiences` + `ads_get_custom_audience_adsets` (ou o campo de segmentação do `ads_get_ad_entities`, se o `ads_get_field_context` confirmar); no `APP`, `curl -g` em `/{adset_id}?fields=targeting{custom_audiences,flexible_spec,targeting_automation}`; sem leitura possível, perguntar ao aluno.

> **Atenção modo MCP:** a visita à página (`landing_page_views`) costuma não vir em nível de anúncio no `ads_get_ad_entities` (conferir com `ads_get_field_context`). Sem ela, Offer Rate, Purchase Rate e Add to Cart Rate (que dividem pela visita) ficam `indisponivel` no MCP, ou usam `actions:link_click` como substituto de intenção, **declarando que é substituto** (seção 6.1 do SKILL.md). Não apresentar substituto como métrica real.
>
> **Temperatura SÓ pela segmentação real (seção 4.5 do SKILL.md):** públicos personalizados (`custom_audiences`, `excluded_connections`) = warm, interesses ou semelhantes = cold, público aberto ou Advantage+ = mixed. NUNCA inferir temperatura pelo nome do conjunto/campanha.

## Métricas derivadas

| Métrica | Fórmula | O que mede |
|---------|---------|-----------|
| Offer Rate | (leads ou initiate_checkout) / landing_page_views | Interesse demonstrado na oferta |
| Purchase Rate | purchases / landing_page_views | Taxa de compra pós-visita |
| Add to Cart Rate | add_to_cart / landing_page_views | Interesse no produto |
| Creative Conversion Rate | purchases / video_3sec_views (impressions para imagem) | Eficiência ponta a ponta |

## Conversão por temperatura de público

Para cada criativo, separar a performance em conjuntos cold vs warm:

**Como detectar temperatura:**
- Conjunto com `targeting.custom_audiences` ou `targeting.excluded_connections` → **warm/remarketing**
- Conjunto com `targeting.flexible_spec` (interesses) ou `targeting.lookalike_audience` → **cold**
- Conjunto sem segmentação detalhada (público aberto ou Advantage+) → **mixed** (declarar limitação)

```yaml
conversao_por_temperatura:
  ad_id: "<id>"
  ad_name: "AD - Dor - Vídeo 30s"
  cold:
    spend: 800.00
    conversoes: 5
    cpa: 160.00
    roas: 1.8
  warm:
    spend: 200.00
    conversoes: 8
    cpa: 25.00
    roas: 12.0
  alerta: falso_conversor_criativo
  motivo: "62% das conversões vêm de warm com 20% do gasto. CPA em cold é 6× maior."
```

**Detecção de falso conversor criativo:** quando > 60% das conversões vêm de conjuntos warm com < 30% do gasto. O criativo **parece** bom pelo ROAS geral, mas só converte quem já ia comprar.

## Gap atenção-conversão

Dois padrões importantes que cruzam com os módulos anteriores:

### Alta atenção + baixa conversão
- Hook Rate alto + CTR bom + CPA ruim
- **Significado:** o criativo captura atenção e gera clique, mas quem chega na página não compra. O problema provavelmente NÃO é o criativo. É a página, oferta, preço ou checkout.
- **O que NÃO fazer:** não pausar o criativo. Ele está fazendo o trabalho dele (trazer tráfego qualificado).
- **O que fazer:** revisar a página de destino, a oferta e a garantia com `/trafego-oferta-funil`.

### Baixa atenção + alta conversão
- Hook Rate baixo + CTR baixo + CPA bom
- **Significado:** o criativo é menos massivo (não chama atenção de todo mundo), mas altamente qualificado. Quem presta atenção é comprador.
- **O que NÃO fazer:** não matar por CTR baixo. Não comparar com criativos de curiosidade vazia.
- **O que fazer:** manter com orçamento dedicado. Testar novo gancho para aumentar alcance sem perder qualificação.

## Explicação obrigatória

Cada achado DEVE vir com explicação:

```
AD "Dor - Vídeo 30s": FALSO CONVERSOR CRIATIVO ⚠️

O que significa: esse criativo parece ter ROAS 5.2x, mas 62% das
vendas vieram de público de remarketing (que gastou só 20% do orçamento).
No público frio, o CPA é R$ 160 (acima da meta de R$ 150).

Por que importa: se escalar esse criativo, o orçamento vai para público
frio onde ele NÃO converte bem. O ROAS geral vai cair drasticamente.

O que NÃO fazer: não escalar baseado no ROAS geral de 5.2x.

O que fazer: testar esse criativo APENAS em público frio por 7 dias.
Se CPA ficar abaixo de R$ 180 com 10+ conversões, tem potencial.
Se não, usar apenas para remarketing.
```

## Output YAML

```yaml
conversao_criativa:
  produto: "Produto A"
  cpa_target: 150.00
  total_analisados: 8

  criativos:
    - ad_id: "<id>"
      ad_name: "<nome>"
      offer_rate: 0.08
      purchase_rate: 0.021
      add_to_cart_rate: 0.045
      creative_conversion_rate: 0.0012
      cpa_geral: 95.00
      roas_geral: 3.2
      temperatura:
        cold: { spend: 800, conversoes: 5, cpa: 160.00 }
        warm: { spend: 200, conversoes: 8, cpa: 25.00 }
      falso_conversor: true | false
      gap: alta_atencao_baixa_conversao | baixa_atencao_alta_conversao | equilibrado | nenhum
      tendencia_vs_anterior: melhorando | piorando | estavel
```

## Ranking por formato (obrigatório)

Além do comparativo agregado entre formatos, entregar **três rankings separados** (seção 5.2 do SKILL.md): Top vídeos, Top imagens/cards, Top carrosséis. Cada um ordenado pela meta do aluno (ROAS ≥ break-even / CPA ≤ meta), com trava de volume: ⚠️ em todo criativo com < 4 vendas, e nunca coroar campeão item de 1-3 vendas. Formato detectado pelo `object_type` do criativo, não pelo nome (seção 5.1 do SKILL.md). Nunca um ranking único misturando formatos.

## Tratamento sem vídeo (imagem only)

A conversão criativa funciona normalmente com imagens. As métricas de conversão (CPA, ROAS, Offer Rate, Purchase Rate) não dependem de vídeo. A única diferença:
- Creative Conversion Rate usa `purchases / impressions` em vez de `purchases / video_3sec_views`
- Declarar no output: "Creative Conversion Rate calculado sobre impressões (sem dado de atenção de vídeo)"

## Explicação obrigatória

Cada achado DEVE ter explicação em linguagem natural:

### Falso conversor criativo
```
{nome}: FALSO CONVERSOR CRIATIVO ⚠️

O que significa: esse criativo parece converter bem (ROAS {X}x),
mas {Y}% das vendas vieram de público de remarketing, que gastou
apenas {Z}% do orçamento. No público frio, o CPA é R$ {cpa_cold}.

Por que importa: se escalar, o orçamento vai para público frio onde
o criativo NÃO converte. O ROAS geral vai cair.

O que NÃO fazer: não escalar baseado no ROAS geral.
O que fazer: testar em público frio isolado por 7 dias.
```

### Gap atenção-conversão (alta atenção, baixa conversão)
```
{nome}: ATENÇÃO ALTA, CONVERSÃO BAIXA

O que significa: esse criativo captura atenção e gera clique
qualificado, mas quem chega na página não compra. O problema
provavelmente NÃO é o criativo. É a página ou a oferta.

O que NÃO fazer: não pausar esse criativo. Ele está trazendo
tráfego qualificado.
O que fazer: revisar a página de destino (oferta, preço, prova,
velocidade de carregamento) com /trafego-oferta-funil.
```

### Gap atenção-conversão (baixa atenção, alta conversão)
```
{nome}: ATENÇÃO BAIXA, CONVERSÃO ALTA ✅

O que significa: poucos clicam, mas quem clica compra. Esse
criativo filtra naturalmente: só atrai quem tem intenção real.

O que NÃO fazer: não matar por CTR baixo. Esse é o criativo
mais eficiente por R$ investido.
O que fazer: proteger e manter verba dedicada (aumento de verba
passa pelo /trafego-escalar). Testar novo gancho para ampliar
alcance sem perder qualificação.
```

## Relatório humano (seções aplicáveis)

Usar as 7 seções do SKILL.md principal. Exemplo de narrativa:

```
1. CONTEXTO RESUMIDO
Analisei 8 criativos do Produto A nos últimos 7 dias.
Cruzei métricas de conversão com temperatura de público
(cold vs warm) para cada criativo.

2. DIAGNÓSTICO REAL
Os dados dizem: 2 criativos são falsos conversores (60% das
vendas em remarketing). 1 criativo tem gap atenção-conversão
(CTR 2.1% mas CPA R$ 195, acima da meta).
Os dados NÃO dizem: se o problema do CPA alto é o criativo
ou a página. Offer Rate de 1.8% sugere página.
Erro a evitar: escalar os 2 falsos conversores pelo ROAS geral.

7. DECISÃO RECOMENDADA
Fazer agora: isolar os 2 falsos conversores em público frio
por 7 dias para validar.
NÃO fazer: não escalar sem testar em cold.
Fazer somente se: se CPA em cold ficar abaixo de R$ 180 com
10+ conversões, o criativo tem força própria.
```
