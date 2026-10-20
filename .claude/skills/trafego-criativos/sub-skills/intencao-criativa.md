# Sub-skill. Intenção Criativa

Avalia se o criativo **transforma atenção em interesse real e ação qualificada**. Não é ranking de CTR como o output [3] da `/trafego-analise`. Aqui: análise de qualidade da intenção, detecção de curiosidade vazia, mapeamento de tipo de intenção por criativo.

**Diferença vs `/trafego-analise` output [3]:** o output [3] mostra CTR e CPC num ranking rápido. Esta sub-skill investiga se o clique é qualificado (a pessoa queria ir para a página) ou vazio (clicou por curiosidade e saiu), calcula o Intent Rate (quanto da atenção vira visita real) e classifica cada criativo pelo tipo de intenção que gera.

---

## Contexto multi-produto

Quando a conta tem mais de 1 produto declarado, a análise de intenção roda **por produto** separadamente. Motivo: um criativo de perpétuo pode ter CTR alto com curiosidade vazia (promessa forte demais), enquanto um criativo de lançamento pode ter CTR baixo mas altamente qualificado. Misturar distorce o diagnóstico.

Cada produto gera seu próprio mapa de intenção e ranking. O relatório apresenta uma seção por produto:

```
PRODUTO: Produto A (R$ 2.500, perpétuo high)
  Criativos analisados: 6
  Padrão dominante: gerador_clique (curiosidade vazia detectada)

PRODUTO: Produto B (R$ 997, perpétuo mid)
  Criativos analisados: 4
  Padrão dominante: gerador_visita_qualificada
```

**Exceção:** se um padrão é compartilhado entre todos os produtos (ex: LPV Rate baixo em toda a conta indicando problema técnico de página), destacar como "padrão transversal" no topo.

---

## Quando é acionado

- Opção [3] do menu principal
- Automaticamente na Inteligência Completa (segundo módulo da sequência: atenção → **intenção** → conversão → diagnóstico → DNA → briefing)
- Quando o aluno diz "CTR alto mas não converte" (roda intenção + conversão)
- Quando o aluno pergunta "meus cliques são qualificados?" ou "estou atraindo curioso?"
- Quando `/trafego-diagnostico` diferencial aponta hipótese "oferta_funil" e a leitura de atenção já está ok

---

## Dados necessários

Pedir à `/trafego-insights`:
- Escopo: `conta_completa` ou campanhas específicas
- Nível: `ad`
- Período: definido na entrevista de entrada (Passo 0.9 do padrão da `/trafego-diagnostico`) + período anterior para comparação
- Métricas obrigatórias (nomes da Graph API, modo `APP`; no MCP, tradução na seção 3.1 do SKILL.md):
  - `inline_link_clicks`
  - `unique_inline_link_clicks`
  - `actions` (filtrar `landing_page_view`)
  - `outbound_clicks`
  - `ctr`
  - `cpc`
  - `impressions`
  - `spend`
- Métrica de atenção (vinda do módulo 1 ou calculada aqui se rodando isolado):
  - `video_p25_watched_actions` (denominador do Intent Rate, a mesma base do Hook Rate)

**Dados complementares (leitura pura, por modo):**
- Formato do criativo pelo `object_type`. `MCP_CONECTOR`: `ads_get_creatives` ou o campo de criativo do `ads_get_ad_entities`. `APP`: `curl -g` em `/{ad_id}?fields=creative{id,object_type}`.

**Disponibilidade no MCP (seção 6.1 do SKILL.md):** no `ads_get_ad_entities`, o clique no link vem como `link_click`, a visita à página como `landing_page_view` e o gasto como `amount_spent` (conferidos na conta real, inclusive no nível de anúncio; contrato do conector na `.claude/skills/trafego-insights/SKILL.md` §10.1). CTR de link e CPC saem da conta: `link_click ÷ impressions` e `amount_spent ÷ link_click`. Cliques de saída e os campos de vídeo não estão na lista conferida: confirmar com `ads_get_field_context` antes da coleta. Se a visita à página vier `null`, a conta não registra o evento: Click-to-LPV e Intent Rate ficam `indisponivel` ou usam substituto declarado.

---

## Métricas derivadas calculadas

| Métrica | Fórmula | O que mede |
|---------|---------|-----------|
| **Intent Rate** | `landing_page_views / video_p25_watched` | Quanto da atenção (quem passou do gancho) vira intenção real de visitar a página. Para imagens: `landing_page_views / impressions`. |
| **Click-to-LPV Rate** | `landing_page_views / inline_link_clicks` | Qualidade do clique. Do total que clicou, quantos realmente chegaram na página. |
| **Cost per LPV** | `spend / landing_page_views` | Custo para gerar uma visita qualificada à página. |

**Tratamento de denominador zero:** retornar `null`. Nunca dividir por zero, nunca inventar valor.

**Quando `landing_page_view` não está disponível:** usar `outbound_clicks` como fallback e declarar: "Visitas à página (landing page views) indisponíveis. Usando os cliques de saída (outbound clicks) como substituto. A medição é menos precisa."

**Para imagens (sem `video_p25_watched`):** o Intent Rate usa `impressions` no denominador. Declarar a mudança de base: "Intent Rate calculado com impressões (não com quem passou do gancho do vídeo). Valor será naturalmente menor."

---

## Qualidade da intenção

Classificação do clique em 3 categorias:

### Clique qualificado

| Critério | Limiar |
|----------|--------|
| CTR | Acima do benchmark da conta (ou > 1.0% como fallback) |
| Click-to-LPV Rate | 80% ou mais |

**O que significa:** a pessoa clicou E chegou na página. A intenção é real. O criativo atraiu alguém genuinamente interessado na oferta.

**Benchmark dinâmico:** o benchmark de CTR é a mediana dos criativos ativos na conta. Se não houver histórico suficiente, usar 1.0% como fallback para Sales e 1.5% para Leads.

### Clique vazio (curiosidade)

| Critério | Limiar |
|----------|--------|
| CTR | Acima do benchmark |
| Click-to-LPV Rate | < 60% |

**O que significa:** a pessoa clicou mas não chegou na página (ou saiu antes de carregar). Duas causas prováveis: (1) página lenta ou com erro técnico, (2) o criativo prometeu algo que a página não entrega, e o visitante fecha ao ver o conteúdo.

**Distinção crítica:** Click-to-LPV Rate entre 60% e 79% é zona cinza. Classificar como `clique_misto` e investigar se o problema é técnico (página lenta) ou de alinhamento (promessa vs entrega). Abaixo de 70%, a primeira hipótese é técnica (página lenta, link errado, redirecionamento): conferir com `/pagina-performance` e a congruência com `/trafego-oferta-funil` antes de mexer no anúncio. Régua única do Severino para a visita à página: saudável 80% ou mais, atenção de 60% a 79%, crítico abaixo de 60%.

### Baixa intenção

| Critério | Limiar |
|----------|--------|
| CTR | Abaixo do benchmark |

**O que significa:** o criativo não gera interesse suficiente para o clique. Pode ser que a atenção seja boa (Hook Rate alto) mas a proposta de valor não convence, ou pode ser que o público não se identifique com a oferta mostrada.

---

## Detecção de curiosidade vazia

Padrão explícito que esta sub-skill rastreia: **CTR alto + CPA ruim**.

### Sinais de curiosidade vazia

| Sinal | Direção | Peso |
|-------|---------|------|
| CTR acima do benchmark | confirma | alto |
| Click-to-LPV Rate < 60% | confirma | alto |
| CPA acima de 1.5× a meta | confirma | alto |
| CPC baixo (clicks baratos mas inúteis) | confirma | médio |
| Outbound clicks muito menor que inline_link_clicks | confirma | médio |
| Muitas impressões com poucos LPV | confirma | médio |

### Alerta de curiosidade vazia

Quando detectado (2+ sinais confirmando), emitir alerta:

```
⚠️ CURIOSIDADE VAZIA DETECTADA

Criativo "{nome}": CTR de {ctr}% (acima da média da conta), mas
Click-to-LPV Rate de apenas {lpv_rate}%. De cada 100 cliques, apenas
{lpv_pct} chegam na página.

O que está acontecendo: o criativo desperta curiosidade, mas não
interesse real. As pessoas clicam para ver do que se trata, mas não
ficam.

Possíveis causas:
1. Promessa do anúncio desalinhada com a página (o anúncio promete X,
   a página mostra Y)
2. Página lenta ou com erro técnico (a pessoa desiste antes de carregar)
3. CTA ambíguo (a pessoa clica sem saber que vai sair da plataforma)

O que fazer:
- Verificar se a página carrega em menos de 3 segundos (`/pagina-performance`)
- Comparar a promessa do anúncio com a headline da página (`/trafego-oferta-funil`, módulo de congruência)
- Se a página funciona e a promessa está alinhada, o criativo precisa
  qualificar melhor (mostrar preço, duração, público-alvo no anúncio
  para filtrar curiosos antes do clique)

O que NÃO fazer:
- NÃO aumentar orçamento deste criativo pelo CTR alto. CTR alto com
  LPV baixo é gasto sem retorno.
```

---

## Mapa de intenção

Classificação de cada criativo pelo tipo de intenção que gera:

### `gerador_atencao`

| Critério | Limiar |
|----------|--------|
| Hook Rate (vídeo) ou impressões relativas (imagem) | Alto (acima da mediana) |
| CTR | Baixo (abaixo do benchmark) |

**O que significa:** o criativo chama atenção no feed (pessoas param para olhar, assiste o vídeo), mas não gera clique. A atenção não se transforma em ação.

**Interpretação provável:** o criativo é visualmente atraente ou interessante como conteúdo, mas não cria desejo de saber mais. Funciona como "entretenimento" no feed.

**O que fazer:** adicionar CTA mais forte, criar urgência, mostrar benefício claro que justifique o clique. O ativo existe (atenção), falta a ponte para a ação.

**Tradução VTSD:** Quadro na Parede forte (prende quem olha), mas sem Furadeira (não conecta com dor/desejo que motive ação).

### `gerador_clique`

| Critério | Limiar |
|----------|--------|
| CTR | Acima do benchmark |
| Click-to-LPV Rate | < 60% |

**O que significa:** o criativo gera cliques, mas as pessoas não chegam na página ou não ficam. O clique é de curiosidade, não de intenção real.

**Interpretação provável:** a promessa do anúncio é forte, mas (1) a página não carrega ou tem problema técnico, ou (2) o que a pessoa encontra na página não corresponde ao que o anúncio prometeu, ou (3) o anúncio atrai público errado.

**O que fazer:** investigar a jornada pós-clique. Página carrega? O headline da página reflete a promessa do anúncio? O público que o criativo atrai é o comprador ou apenas o curioso?

**Tradução VTSD:** Decorado forte (atrai clique), mas a Identidade do Produto no anúncio não casa com a realidade da oferta na página.

### `gerador_visita_qualificada`

| Critério | Limiar |
|----------|--------|
| CTR | Acima do benchmark |
| Click-to-LPV Rate | 80% ou mais |

**O que significa:** o criativo gera cliques E as pessoas chegam na página. A intenção é qualificada. O tráfego que este criativo envia para a página é de boa qualidade.

**Interpretação provável:** a promessa do anúncio está alinhada com a oferta. O público que clica sabe o que vai encontrar e tem interesse genuíno.

**O que fazer:** proteger este criativo. Se o CPA está na meta, é candidato a escala. Se o CPA está ruim APESAR de tráfego qualificado, o problema está na página ou na oferta, não no criativo.

**Tradução VTSD:** Furadeira alinhada com Identidade do Produto. A dor/desejo que o anúncio ativa é a mesma que a oferta resolve.

### `gerador_intencao_silenciosa`

| Critério | Limiar |
|----------|--------|
| CTR | Abaixo do benchmark |
| Taxa de conversão (entre os que clicam) | Acima da mediana |

**O que significa:** poucos clicam, mas quem clica, compra. O criativo funciona como filtro natural: repele curiosos e atrai compradores.

**Interpretação provável:** o criativo é específico, direto, talvez até "chato" para quem não é o público. Mostra preço, público-alvo, ou detalhes que afastam curiosos. Quem resta é comprador.

**O que fazer:** NUNCA matar por CTR baixo. Este é um criativo qualificado. A tentação de "melhorar o CTR" pode destruir o filtro natural e atrair curiosos que não compram.

**Tradução VTSD:** Identidade do Consumidor perfeitamente definida. O criativo fala apenas com quem se reconhece. As 3 Identidades (Comunicador, Consumidor e Produto) alinhadas.

### Regra de prioridade

Se um criativo pode se encaixar em mais de uma classificação, usar esta ordem:
1. `gerador_intencao_silenciosa` (CTR baixo + conversão alta sempre prevalece, é o mais contraintuitivo)
2. `gerador_clique` (curiosidade vazia detectada)
3. `gerador_visita_qualificada`
4. `gerador_atencao`

---

## Explicação obrigatória (regra dura)

Todo número, classificação e alerta DEVE ter texto explicativo em linguagem natural.

### Templates por classificação

**Gerador de atenção:**
```
Criativo "{nome}": GERADOR DE ATENÇÃO 👁️

O que está acontecendo: esse criativo chama atenção no feed. Hook Rate de
{hook_rate}% mostra que as pessoas param para olhar. Mas o CTR de apenas
{ctr}% indica que a atenção não vira clique.

O que isso significa na prática: o criativo é interessante de assistir,
mas não cria vontade de saber mais. Funciona como "entretenimento" no
feed, não como gerador de tráfego.

O que fazer: testar CTA mais direto, mostrar benefício claro, criar
urgência. O ativo é a atenção. Falta transformar atenção em ação.
```

**Gerador de clique (curiosidade vazia):**
```
Criativo "{nome}": GERADOR DE CLIQUE (CURIOSIDADE) 🖱️

O que está acontecendo: CTR de {ctr}% (acima da média), mas Click-to-LPV
Rate de apenas {lpv_rate}%. As pessoas clicam, mas {pct_perdido}% não
chega na página.

O que isso significa na prática: o criativo gera curiosidade, não intenção
real. Os cliques são baratos (CPC de R$ {cpc}) mas inúteis. Dinheiro
sendo gasto em tráfego que não converte.

O que fazer: verificar se a página carrega rápido. Se sim, alinhar a
promessa do anúncio com o que a página entrega. Se já está alinhado,
qualificar melhor o anúncio (mostrar preço, público-alvo) para filtrar
curiosos antes do clique.
```

**Gerador de visita qualificada:**
```
Criativo "{nome}": GERADOR DE VISITA QUALIFICADA ✅

O que está acontecendo: CTR de {ctr}% com Click-to-LPV Rate de
{lpv_rate}%. De cada 100 cliques, {lpv_count} chegam na página e ficam.

O que isso significa na prática: tráfego qualificado. As pessoas que
clicam querem estar na página. A promessa do anúncio está alinhada com
a oferta.

O que fazer: proteger este criativo. Se CPA na meta, candidato a escala.
Se CPA ruim, o gargalo está na página, não no criativo.
```

**Gerador de intenção silenciosa:**
```
Criativo "{nome}": GERADOR DE INTENÇÃO SILENCIOSA 🤫

O que está acontecendo: CTR de apenas {ctr}% (abaixo da média), MAS
taxa de conversão de {conv_rate}% entre quem clica. Poucos clicam.
Quem clica, compra.

O que isso significa na prática: este criativo funciona como filtro
natural. Repele curiosos e atrai compradores. O CTR baixo não é falha,
é qualificação.

ATENÇÃO: NÃO melhorar o CTR deste criativo. A tentação de "turbinar"
o gancho pode destruir o filtro e atrair curiosos que não compram. O
resultado é MAIS cliques e MENOS vendas.

O que fazer: manter como está. É um dos criativos mais valiosos da conta,
apesar de parecer "fraco" no ranking de CTR.
```

---

## Output YAML

```yaml
intencao_criativa:
  periodo: "2026-05-20 a 2026-05-27"
  periodo_anterior: "2026-05-13 a 2026-05-20"
  nivel_analise: metricas | metricas_mais_descricao
  produto: "Produto A"
  criativos_analisados: 6
  benchmark_ctr_conta: 1.35
  alertas_curiosidade_vazia: 1

  criativos:
    - ad_id: "<ad_id_1>"
      ad_name: "VSL Curso v3"
      formato: video
      metricas:
        impressions: 28500
        inline_link_clicks: 399
        landing_page_views: 342
        video_p25_watched: 7125
        ctr: 1.40
        cpc: 2.57
        spend: 1026.00
      derivadas:
        intent_rate: 0.048
        click_to_lpv_rate: 0.857
        cost_per_lpv: 3.00
      qualidade_clique: qualificado
      mapa_intencao: gerador_visita_qualificada
      comparacao_temporal:
        ctr_anterior: 1.52
        ctr_atual: 1.40
        click_to_lpv_anterior: 0.88
        click_to_lpv_atual: 0.857
        direcao_ctr: "piorando"
        direcao_lpv: "estavel"

    - ad_id: "<ad_id_2>"
      ad_name: "Hook Polêmico v2"
      formato: video
      metricas:
        impressions: 22000
        inline_link_clicks: 550
        landing_page_views: 198
        video_p25_watched: 7700
        ctr: 2.50
        cpc: 1.45
        spend: 798.00
      derivadas:
        intent_rate: 0.026
        click_to_lpv_rate: 0.360
        cost_per_lpv: 4.03
      qualidade_clique: vazio
      mapa_intencao: gerador_clique
      alerta_curiosidade_vazia: true
      comparacao_temporal:
        ctr_anterior: 2.30
        ctr_atual: 2.50
        click_to_lpv_anterior: 0.42
        click_to_lpv_atual: 0.360
        direcao_ctr: "estavel"
        direcao_lpv: "piorando"

    - ad_id: "<ad_id_3>"
      ad_name: "Depoimento técnico"
      formato: video
      metricas:
        impressions: 12000
        inline_link_clicks: 84
        landing_page_views: 72
        video_p25_watched: 3600
        ctr: 0.70
        cpc: 4.76
        spend: 400.00
      derivadas:
        intent_rate: 0.020
        click_to_lpv_rate: 0.857
        cost_per_lpv: 5.56
      qualidade_clique: baixa_intencao
      mapa_intencao: gerador_intencao_silenciosa
      taxa_conversao_pos_clique: 4.17
      nota: "CTR baixo mas 3 compras em 72 cliques. Não matar por CTR."

  resumo_mapa:
    gerador_atencao: 1
    gerador_clique: 1
    gerador_visita_qualificada: 2
    gerador_intencao_silenciosa: 1
    nao_classificado: 1
```

---

## Relatório humano

Usar a estrutura de 7 seções do SKILL.md principal. Exemplo narrativo completo:

```
1. CONTEXTO RESUMIDO

Analisei a intenção de 6 criativos do Produto A nos últimos 7 dias
(20/05 a 27/05). Benchmark de CTR da conta: 1.35%. Nível da análise:
métricas. Limitação: sem acesso ao conteúdo dos criativos ou da
landing page.


2. DIAGNÓSTICO REAL

O que as métricas dizem:
- A conta tem um problema de curiosidade vazia. O criativo "Hook
  Polêmico v2" tem o melhor CTR (2.50%) mas o pior Click-to-LPV Rate
  (36%). De cada 100 cliques, apenas 36 chegam na página. Os outros
  64 são cliques desperdiçados.
- Custo por LPV do "Hook Polêmico": R$ 4,03. Custo por LPV do "VSL
  Curso v3": R$ 3,00. O criativo com CTR alto custa MAIS por visita
  qualificada do que o com CTR normal.
- Descoberta importante: "Depoimento técnico" tem CTR de apenas 0.70%
  (metade da média), mas taxa de conversão de 4.17% entre quem clica.
  É o criativo mais eficiente da conta em conversão, escondido atrás
  do pior CTR.

O que as métricas NÃO dizem:
- Não sabemos se o Click-to-LPV Rate baixo do "Hook Polêmico" é por
  página lenta ou por desalinhamento promessa/entrega.
- Não sabemos por que o "Depoimento técnico" atrai poucos cliques mas
  qualificados. Pode ser o formato, o tom, ou a especificidade.

Erro a evitar: NÃO pausar o "Depoimento técnico" pelo CTR baixo. É
o criativo mais qualificado da conta. Pausar esse e manter o "Hook
Polêmico" é trocar comprador por curioso.


3. HIPÓTESE CENTRAL

A conta está gerando tráfego de curiosidade, não de intenção. O
criativo com melhor CTR é o que menos entrega visitas qualificadas.
O criativo com pior CTR é o que mais entrega compradores.

Nível de confiança: alto para a classificação de curiosidade vazia
(CTR 2.5% + LPV Rate 36% é padrão clássico). Médio para o "Depoimento
técnico" como gerador de intenção silenciosa (3 compras em 72 cliques
é amostra pequena).


5. RISCOS E ARMADILHAS

- Risco 1: otimizar por CTR vai PIORAR o resultado. O CTR mais alto
  da conta é o mais desperdiçador de orçamento.
- Risco 2: escalar "Hook Polêmico" pelo CTR atraente vai multiplicar
  gasto sem retorno.
- Armadilha: melhorar o gancho do "Depoimento técnico" para aumentar
  CTR pode destruir o filtro natural que qualifica os poucos que clicam.
- Ponto cego: se o Click-to-LPV Rate baixo for problema técnico
  (página lenta), resolver isso pode transformar o "Hook Polêmico" em
  criativo funcional. Verificar antes de condenar.


7. DECISÃO RECOMENDADA

Fazer agora:
- Verificar velocidade da landing page (se leva mais de 3s, pode ser
  causa técnica do LPV Rate baixo)
- Proteger "Depoimento técnico" (não pausar, não mexer)
- Reduzir orçamento do "Hook Polêmico" até investigar o Click-to-LPV

NÃO fazer:
- Não escalar "Hook Polêmico" pelo CTR alto
- Não pausar "Depoimento técnico" pelo CTR baixo
- Não usar CTR como métrica de decisão isolada

Fazer SOMENTE SE:
- Se a página estiver rápida (< 3s) E o LPV Rate continuar < 60%, o
  "Hook Polêmico" precisa de nova versão com promessa mais alinhada
- Se o "Depoimento técnico" acumular 10+ compras mantendo taxa > 3%,
  considerar duplicar o formato com variações
```

---

## Repasse para os módulos seguintes

Quando rodando como parte da Inteligência Completa (opção [1]):

**Dados que esta sub-skill repassa para o módulo de Conversão Criativa:**
- Classificação do mapa de intenção de cada criativo
- Click-to-LPV Rate de cada criativo (para contextualizar taxa de conversão)
- Criativos flagrados com curiosidade vazia (para explicar CPA alto)
- Intent Rate por criativo

**Dados que repassa para o Diagnóstico Criativo:**
- Mapa de intenção completo
- Alertas de curiosidade vazia
- Qualidade do clique por criativo
- Comparação temporal (direção do CTR e LPV Rate)

**Integração com a Leitura de Atenção (módulo 1):**
- Recebe Hook Rate de cada criativo para calcular Intent Rate com denominador de atenção
- Criativos com `atencao_baixa` + `baixa_intencao` = problema de atenção, não de intenção
- Criativos com `gancho_forte_dev_fraco` + `gerador_clique` = atenção funciona mas não qualifica
