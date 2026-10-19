# Sub-skill. Detector de Falso Vencedor

Identifica campanhas, conjuntos ou anúncios que **parecem vencedores** (ROAS positivo, CPA dentro da meta) mas podem estar enganando por baixa amostra, dependência de remarketing, frequência alta, baixa consistência temporal ou atribuição frágil.

**Por que isso importa:** escalar um falso vencedor queima caixa. O gestor vê ROAS 5x, escala, e descobre 7 dias depois que o resultado era concentrado em remarketing com frequência 6 e 4 compras no total.

## Contexto multi-produto

Quando a conta tem mais de 1 produto declarado, a avaliação roda **por produto** separadamente. Motivo: ROAS de 5x num produto de R$ 30.000 com 2 vendas é completamente diferente de ROAS 5x num produto de R$ 97 com 200 vendas. Os limiares de volume, gasto e consistência dependem do ticket.

Cada produto usa **seus próprios limiares** derivados da trilha (low/mid/high):
- Gasto relevante: ajustado ao ticket (R$ 200 para low, R$ 500 para mid, R$ 2.000 para high)
- Conversões mínimas para `vencedor_real`: 15 (low/mid perpétuo), 10 (high perpétuo), 30 leads (lançamento)

No output, cada produto ganha sua seção de classificações. Nunca misturar entidades de produtos diferentes no mesmo ranking.

---

## Quando é acionado

- Opção [4] do menu principal
- Automaticamente no Diagnóstico Completo (terceiro módulo da sequência)
- Quando o aluno pergunta "essa campanha é vencedora mesmo?" ou "vale a pena escalar?"
- **Integração crítica:** sugerido pela `/trafego-otimizar` antes de emitir `sinal_para_escala.pronta=true`, e é o freio do `/trafego-escalar` (seção 12 do SKILL.md: só escala `vencedor_real` com score de confiança 50 ou mais)

## Dados necessários

Pedir à `/trafego-insights`:
- Campanha(s) específica(s) ou `escopo: conta_completa`
- `nivel: campaign + adset + ad`
- 3 janelas da trilha
- `serie_diaria` das métricas-norte (CPA/CPL) por entidade
- Frequência por entidade

Complementar (leitura pura, por modo, conforme a seção 3.1 do SKILL.md):
- Tipo de público de cada conjunto: segmentação com públicos personalizados (remarketing) ou com interesses, semelhantes e público aberto (prospecção). `APP`: `curl -g` no campo `targeting` do conjunto. `MCP_CONECTOR`: `ads_get_ad_account_custom_audiences` + `ads_get_custom_audience_adsets`, ou `ads_get_ad_entities` se `ads_get_field_context` confirmar o campo de segmentação.
- Sem leitura possível: marcar "segmentação não verificada", perguntar ao aluno quais conjuntos são de remarketing e nunca deduzir pelo nome.

## As 4 classificações

### `vencedor_real`

Entidade que merece confiança e pode ser considerada para escala.

**Todos os critérios devem ser verdadeiros:**
- Gasto relevante: > R$ 200 no período (low ticket) ou > R$ 500 (mid/high)
- Conversões: ≥ 15 (perpétuo) ou ≥ 30 leads (lançamento)
- CPA/CPL dentro do target (ou zona verde de lucro quando margem disponível)
- Consistência: CV da métrica-norte < 0.30 na serie_diaria (mesmo limiar do score de confiança)
- Frequência: < 3.0
- Distribuição: resultado não concentrado em 1 único dia (nenhum dia com > 40% das conversões totais)
- Fonte: pelo menos 50% do gasto em prospecção (não remarketing), confirmado pela segmentação real
- Janela: dados de 7+ dias

### `vencedor_promissor`

Entidade com bons sinais iniciais, mas dados insuficientes para classificar como real.

**Critérios:**
- CPA/CPL dentro ou próximo do target (até 1.2× target)
- Conversões: 5-14 (perpétuo) ou 10-29 leads (lançamento)
- Tendência estável ou melhorando
- Frequência: < 3.5
- Janela: 4-6 dias, ou 7+ dias com pouco gasto

**Recomendação padrão:** manter rodando, não escalar ainda. Reavaliar em +7 dias.

### `falso_vencedor_provavel`

Entidade que parece boa mas tem sinais de que o resultado é inflado ou insustentável.

**Pelo menos 2 destes critérios devem ser verdadeiros:**
- Poucas conversões com ROAS alto: < 10 compras mas ROAS > 3x (resultado concentrado em poucas vendas de ticket alto)
- Dependência de remarketing: > 70% do resultado vem de conjuntos com público personalizado (remarketing), confirmado pela segmentação real
- Frequência alta: > 3.5 (mesmo público vendo o anúncio muitas vezes, conversões podem ser "inevitáveis" sem ser incremental)
- Baixa consistência: CV da métrica-norte > 0.60 (dias bons e ruins extremos)
- Concentração temporal: > 50% das conversões em 1-2 dias (pico, não padrão)
- Resultado piorou na janela curta vs longa: CPA subiu 20%+ (tendência de deterioração)
- Gasto irrelevante: < R$ 100 no período inteiro

**Recomendação padrão:** NÃO escalar. Rodar teste controlado em condições mais amplas (prospecção pura, 7 dias ou mais, sem remarketing misturado) antes de investir mais.

### `inconclusivo`

Dados insuficientes para classificar.

**Critérios:**
- < 5 conversões no período
- < 4 dias de dados
- Gasto < R$ 50
- Score de confiança < 25

**Recomendação padrão:** aguardar mais dados. Não tomar decisão estrutural.

## Fluxo de avaliação

Para cada entidade (campanha, conjunto ou anúncio) no escopo:

1. Puxar métricas das 3 janelas + serie_diaria
2. Calcular score de confiança (invocar sub-skill score-confianca internamente)
3. Verificar classificação na ordem: `vencedor_real` → `vencedor_promissor` → `falso_vencedor_provavel` → `inconclusivo`
4. Para cada entidade, gerar o bloco de output abaixo

**Prioridade de avaliação (drill-down):**
- Primeiro avaliar no nível campanha
- Para campanhas classificadas como `vencedor_real` ou `vencedor_promissor`, drill-down nos conjuntos
- Para conjuntos classificados como `vencedor_real`, drill-down nos ads (identificar qual criativo sustenta o resultado)

## Explicação obrigatória no output (regra dura)

Cada classificação DEVE vir com explicação em linguagem natural. O aluno precisa entender: **o que a classificação significa** (em português, sem jargão), **por que essa classificação** (evidência simples) e **o que fazer ou não fazer**.

**Formato obrigatório por classificação:**

### Vencedor real
```
{nome}: VENCEDOR REAL ✅

O que significa: esta campanha está de fato gerando resultado
consistente. Pode confiar nos números.

Por que é vencedor real:
- {evidência 1 em linguagem simples}
  Ex: "22 vendas em 7 dias com CPA de R$ 42 (meta: R$ 50)"
- {evidência 2}
  Ex: "Resultado estável: variação diária de apenas 28%"

Pode escalar? Sim, com cuidado, se o score de confiança
for 50 ou mais. Rode /trafego-escalar.
```

### Vencedor promissor
```
{nome}: VENCEDOR PROMISSOR ⏳

O que significa: tem bons sinais, mas ainda faltam dados para
ter certeza. Pode ser que esteja funcionando de verdade, ou
pode ser uma fase boa que não se sustenta.

O que falta para confirmar: {lista}
Ex: "Precisa de mais 7 conversões e mais 3 dias rodando para
ter confiança alta."

O que fazer: manter rodando sem mexer. NÃO escalar ainda.
Reavaliar em {X} dias.
```

### Falso vencedor provável
```
{nome}: FALSO VENCEDOR PROVÁVEL ⚠️

O que significa: os números parecem bons, mas há sinais fortes
de que o resultado não é sustentável. Se escalar, provavelmente
vai perder dinheiro.

Por que parece bom mas engana:
- {motivo 1 em linguagem simples}
  Ex: "ROAS de 8x, mas com apenas 3 vendas. Pode ser sorte."
- {motivo 2}
  Ex: "80% das vendas vieram de remarketing com frequência 5.2.
  O mesmo público está vendo o anúncio muitas vezes. Escalar
  não vai trazer gente nova."

O que NÃO fazer:
- NÃO escalar esta campanha
- NÃO usar como referência para criar campanhas similares

O que fazer: {teste para validar}
Ex: "Duplicar o criativo em um conjunto só de prospecção.
Se converter com CPA abaixo de 2× a meta em 7 dias, o
criativo tem força. Se não, o resultado era do remarketing."
```

### Inconclusivo
```
{nome}: INCONCLUSIVO ❓

O que significa: dados insuficientes para classificar.
Não é bom nem ruim, simplesmente não dá para saber ainda.

O que falta: {lista}
Ex: "2 conversões em 4 dias. Preciso de pelo menos 5
conversões e 7 dias para ter qualquer conclusão."

O que fazer: manter rodando. Reavaliar em {X} dias.
```

---

## Output por entidade

```yaml
falso_vencedor:
  itens_avaliados:
    - id: "<id>"
      nome: "<nome>"
      nivel: campanha | conjunto | anuncio
      classificacao: vencedor_real | vencedor_promissor | falso_vencedor_provavel | inconclusivo
      score_confianca: 72
      motivo: "CPA dentro da meta, 22 compras em 7d, CV 0.35, frequência 1.8, 65% prospecção"
      sinais_positivos:
        - "CPA R$ 42 (meta R$ 50) sustentado em 7 dias"
        - "22 compras com distribuição equilibrada entre dias"
      sinais_negativos:
        - "30% do resultado vem de remarketing"
        - "2 criativos concentram 75% do gasto"
      nivel_risco: baixo | medio | alto
      acao_recomendada: "Pode considerar escala. Antes, diversificar criativos para reduzir concentração."
      nao_fazer: "Não escalar sem testar pelo menos 1 criativo novo. Dependência de 2 anúncios é risco."
```

## Impacto no Diagnóstico Completo

Quando rodado como terceiro módulo da sequência:
- Recebe o score de confiança geral do módulo 1 (se baixo, classificações são automaticamente mais conservadoras)
- Recebe alertas de fragmentação do módulo 2 (se estrutura fragmentada, entidades com pouco gasto são automaticamente `inconclusivo`)
- Passa para o módulo 4 (diferencial): lista de entidades flagradas como falso vencedor, que são excluídas do cálculo de "o que está funcionando"

## Relatório humano (seções aplicáveis)

Usar todas as 7 seções da estrutura do SKILL.md principal. Exemplo de narrativa:

```
CONTEXTO: Avaliei 12 entidades (4 campanhas, 8 conjuntos) nos últimos 7 dias.

DIAGNÓSTICO REAL:
- Os dados dizem: 2 campanhas são vencedoras reais, 1 é promissora, 1 é falso vencedor provável.
- Os dados NÃO dizem: se o falso vencedor se sustentaria em escala sem remarketing.
- Erro a evitar: escalar "Produto A Remarketing" pelo ROAS de 8x. São 3 compras com frequência 5,2.

HIPÓTESE: "Produto A Remarketing" parece vencedora por atingir público já aquecido
repetidas vezes. O ROAS alto reflete o remarketing, não a força do criativo.

RISCOS: Se escalar, o ROAS vai cair drasticamente ao expandir para público frio.
Frequência 5.2 indica saturação: as mesmas pessoas vendo o anúncio muitas vezes.

TESTE: Duplicar o melhor criativo dessa campanha em um conjunto só de prospecção
(lookalike 1%). Se CPA ficar abaixo de 2× target em 7 dias com 15+ conversões,
o criativo tem força própria. Se não, o resultado era do remarketing.

DECISÃO:
- Fazer agora: manter rodando sem escalar. Testar o criativo em prospecção.
- NÃO fazer: não aumentar o orçamento da campanha de remarketing.
- Fazer somente se: escalar apenas se o teste em prospecção confirmar.
```
