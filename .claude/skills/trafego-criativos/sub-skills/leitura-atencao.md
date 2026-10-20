# Sub-skill. Leitura de Atenção

Avalia se o criativo **captura e sustenta atenção** do público. Não é média agregada como o output [3] da `/trafego-analise`. Aqui: curva de retenção individual por anúncio, detecção do ponto exato de queda, classificação por perfil de atenção e comparação de eficiência entre criativos.

**Diferença vs `/trafego-analise` output [3]:** o output [3] é foto rápida com retenção agregada, fadiga e tier S-D. Esta sub-skill vai mais fundo: abre a curva de retenção de cada anúncio individualmente, identifica onde o público abandona, agrupa por perfil comportamental e calcula o custo para capturar cada segundo de atenção.

---

## Contexto multi-produto

Quando a conta tem mais de 1 produto declarado, a leitura de atenção roda **por produto** separadamente. Motivo: um criativo de perpétuo (R$ 2.500) pode ter retenção completamente diferente de um criativo de lançamento (R$ 97). Comparar criativos de produtos diferentes no mesmo ranking distorce a análise.

Cada produto gera sua própria curva, perfis e ranking de eficiência. O relatório apresenta uma seção por produto:

```
PRODUTO: Produto A (R$ 2.500, perpétuo high)
  Criativos analisados: 6 (4 vídeos, 2 imagens)
  Perfil dominante: gancho_forte_dev_fraco

PRODUTO: Produto B (R$ 997, perpétuo mid)
  Criativos analisados: 4 (3 vídeos, 1 imagem)
  Perfil dominante: retencao_linear
```

**Exceção:** se um padrão é compartilhado entre todos os produtos (ex: Hook Rate caindo em toda a conta), destacar como "padrão transversal" no topo.

---

## Quando é acionado

- Opção [2] do menu principal
- Automaticamente na Inteligência Completa (primeiro módulo da sequência: atenção → intenção → conversão → diagnóstico → DNA → briefing)
- Quando o aluno pergunta "meus criativos estão cansando?" (roda atenção + diagnóstico)
- Quando `/trafego-diagnostico` diferencial aponta hipótese "criativo" com probabilidade alta e sugere detalhar

---

## Dados necessários

Pedir à `/trafego-insights`:
- Escopo: `conta_completa` ou campanhas específicas
- Nível: `ad`
- Período: definido na entrevista de entrada (Passo 0.9 do padrão da `/trafego-diagnostico`) + período anterior para comparação
- Métricas obrigatórias de vídeo (nome na Graph API, modo `APP`; no modo `MCP_CONECTOR`, a tradução está na seção 6 do SKILL.md):
  - `video_p25_watched_actions`
  - `video_p50_watched_actions`
  - `video_p75_watched_actions`
  - `video_p95_watched_actions`
  - `video_p100_watched_actions`
  - `video_play_actions` (reproduções, rótulo `video_plays` nas fórmulas)
  - visualizações de 3 segundos: `actions` com `action_type=video_view` (rótulo `video_3sec_views`, usado no Hold Rate e na reserva do Completion Rate)
  - `video_avg_time_watched_actions`
  - `impressions`
  - `spend` (no MCP, `amount_spent`)
- `video_p95_watched_actions` e `video_play_actions` não fazem parte da lista 4.1 da `/trafego-insights`: pedir como acréscimo à coleta dela. As visualizações de 3 segundos já vêm em `actions` (`video_view`) pela própria 4.1 e não entram no `fields=`. Não existem na Graph API os campos `video_plays` nem `video_3_sec_views`: são só rótulos internos. Definições de vídeo: `.claude/skills/trafego-insights/SKILL.md` §4.5.
- Métricas complementares (para fallback de imagem):
  - `ctr`
  - `cpc`
  - `clicks`
  - No MCP, calcular a partir dos campos conferidos: CTR de link = `link_click ÷ impressions` e CPC = `amount_spent ÷ link_click`.

**Dados complementares (leitura pura, por modo):**
- Formato do criativo (vídeo ou imagem) pelo `object_type`. `MCP_CONECTOR`: `ads_get_creatives` ou o campo de criativo do `ads_get_ad_entities` (confirmar com `ads_get_field_context`). `APP`: `curl -g` em `/{ad_id}?fields=creative{id,object_type,thumbnail_url}`.
- No MCP, os campos de vídeo não estão na lista conferida do conector: confirmar com `ads_get_field_context` antes da coleta (seções 3.1 e 6 do SKILL.md).

---

## Métricas derivadas calculadas

Todas calculadas pela skill, não são campos nativos da API:

| Métrica | Fórmula | O que mede |
|---------|---------|-----------|
| **Hook Rate** | `video_p25_watched / impressions` | Força do gancho inicial. Quantas pessoas param o scroll e seguem assistindo (o p25 é a aproximação dos 3 segundos). Mesma conta da `/trafego-insights`; Thumbstop Rate é a mesma métrica. |
| **Hold Rate** | `video_p50_watched / video_3sec_views` | Sustentação após o gancho. Das que ficaram 3s, quantas chegam na metade. |
| **Story Rate** | `video_p75_watched / video_p25_watched` | Força da narrativa. Do quarto inicial ao terceiro quarto, quanto retém. |
| **Completion Rate** | `video_p95_watched / video_plays` | Quantos chegam perto do final. Força da conclusão. |
| **Cost per Hook** | `spend / video_p25_watched` | Custo de cada pessoa que passou do gancho. |
| **Cost per Hold** | `spend / video_p50_watched` | Custo para sustentar atenção até o meio do vídeo. |

**Faixas do Hook Rate (régua única do Severino):** crítico abaixo de 15%, atenção de 15% a 25%, saudável 25% ou mais.

**Tratamento de denominador zero:** retornar `null`. Nunca dividir por zero, nunca inventar valor.

**Fallback quando campo indisponível** (só as reservas da `/trafego-insights` §4.5; fora delas, a métrica fica `indisponivel`): se `video_plays` não estiver disponível, usar `video_3sec_views` (ou, sem ele, `video_p25_watched`) como denominador do Completion Rate e marcar como `fallback_aplicado`. Se `video_3sec_views` não vier, o Hold Rate usa `video_p25_watched` no denominador, marcado como `fallback_aplicado`, e o relatório declara que os limiares de Hold ficam aproximados. Se `video_p25_watched` estiver ausente, marcar Hook Rate, Cost per Hook e Story Rate como `indisponivel`.

---

## Curva de retenção por criativo

Para cada anúncio de vídeo, montar a curva de retenção com os pontos de referência disponíveis:

```
impressões → p25 → p50 → p75 → p95 → p100
```

### Cálculo do ponto de queda

Entre cada par consecutivo de pontos, calcular o **percentual de perda**:

| Transição | Fórmula | O que representa |
|-----------|---------|------------------|
| impressões → p25 | `1 - (p25 / impressions)` | Perda antes do primeiro quarto |
| p25 → p50 | `1 - (p50 / p25)` | Perda no meio do vídeo |
| p50 → p75 | `1 - (p75 / p50)` | Perda no terceiro quarto |
| p75 → p95 | `1 - (p95 / p75)` | Perda antes do final |
| p95 → p100 | `1 - (p100 / p95)` | Perda no finalzinho |

O **ponto de queda** (`ponto_de_queda`) é a transição com a **maior perda percentual**. É o momento exato onde o criativo perde mais audiência.

### Interpretação do ponto de queda

| Ponto de queda | Interpretação provável |
|----------------|----------------------|
| impressões → p25 | O público nem para para olhar. Thumbnail ou primeiros frames fracos. |
| p25 → p50 | Gancho funciona, mas o desenvolvimento perde a atenção. Promessa não se sustenta. |
| p50 → p75 | Desenvolvimento bom, mas o meio do vídeo arrasta. Narrativa perde ritmo. |
| p75 → p95 | Criativo engaja bem, mas o final desanima. CTA ou encerramento fracos. |
| p95 → p100 | Retenção excelente. Perda no final é normal e esperada. |

**Regra:** interpretações são hipóteses comportamentais, não afirmações sobre o conteúdo do vídeo. Se o nível da análise for `metricas` (sem descrição do criativo), declarar: "A métrica sugere [X], mas sem ver o conteúdo do vídeo, é uma hipótese baseada em comportamento."

---

## Classificação por perfil de atenção

5 perfis baseados na combinação de métricas:

### `gancho_forte_dev_fraco`

| Critério | Limiar |
|----------|--------|
| Hook Rate | 25% ou mais |
| Hold Rate | < 30% |

**O que significa:** o criativo para o scroll. O gancho é forte, a thumbnail atrai. Mas quem fica 3 segundos não aguenta até o meio. O desenvolvimento (argumento, história, transição) não sustenta a promessa do gancho.

**O que fazer:** manter o gancho e refazer o desenvolvimento. O ativo valioso é o início do vídeo. Testar nova versão mantendo os primeiros 3-5 segundos e mudando o restante.

**Tradução VTSD:** Decorado forte (chama atenção), mas Furadeira fraca (não perfura a dor/desejo). A Urgência Oculta está no gancho, mas não se sustenta no desenvolvimento.

### `gancho_medio_retencao_alta`

| Critério | Limiar |
|----------|--------|
| Hook Rate | de 15% a menos de 25% |
| Hold Rate | > 50% |

**O que significa:** o criativo não para o scroll de todo mundo, mas quem decide ficar, fica até o final. A qualidade do conteúdo é alta. O problema é que poucas pessoas param para descobrir isso.

**O que fazer:** testar novos ganchos (primeiros 3 segundos) mantendo o corpo do vídeo intacto. O conteúdo funciona, só precisa de uma porta de entrada melhor.

**Tradução VTSD:** Quadro na Parede forte (conteúdo que prende quem para), mas Urgência Oculta fraca no primeiro segundo (não provoca a parada do scroll).

### `retencao_linear`

| Critério | Limiar |
|----------|--------|
| Perda em cada transição | < 20% |

**O que significa:** o público assiste de forma consistente. Não há um ponto de queda dramático. O criativo mantém ritmo equilibrado do início ao fim.

**O que fazer:** este é o perfil mais saudável. Se o CPA está na meta, proteger. Se não está convertendo, o problema provavelmente não é atenção, investigar intenção e conversão (módulos seguintes).

**Tradução VTSD:** Equilíbrio entre Decorado (atrai), Furadeira (sustenta) e Quadro na Parede (educa/conecta).

### `queda_abrupta_meio`

| Critério | Limiar |
|----------|--------|
| p50 / p25 | < 0.40 |

**O que significa:** mais de 60% do público abandona entre o primeiro quarto e a metade do vídeo. Algo acontece nesse trecho que causa rejeição massiva. Transição brusca de tom, promessa quebrada, ou conteúdo que não entrega o que o gancho prometeu.

**O que fazer:** analisar o trecho entre 25% e 50% do vídeo. Se o nível da análise é `metricas_mais_descricao`, identificar o momento exato. Se é `metricas`, recomendar ao aluno rever esse trecho manualmente.

**Tradução VTSD:** Ruptura na narrativa. O Decorado atraiu, mas o desenvolvimento traiu a expectativa. Identidade do Consumidor desalinhada: o criativo atraiu um público que não se reconhece no conteúdo do meio.

### `atencao_baixa`

| Critério | Limiar |
|----------|--------|
| Hook Rate | < 15% |

**O que significa:** o criativo não captura atenção inicial. O scroll não para. Nem o gancho funciona. Menos de 15 em cada 100 pessoas passam do gancho (chegam a 25% do vídeo).

**O que fazer:** o criativo precisa de um gancho novo. Testar: abertura com uma afirmação direta que nomeia uma Urgência Oculta do resumo do produto (Light Copy: gancho sem pergunta), movimento nos primeiros frames, texto em tela nos primeiros 2 segundos, ou formato completamente diferente.

**Tradução VTSD:** Urgência Oculta ausente. O criativo não encontra a dor/desejo que faz o dedo parar de rolar.

### Regra de prioridade

Se um criativo se encaixa em mais de um perfil, usar esta ordem de prioridade:
1. `atencao_baixa` (se Hook Rate < 15%, sempre prevalece)
2. `queda_abrupta_meio` (se p50/p25 < 0.40)
3. `gancho_forte_dev_fraco`
4. `gancho_medio_retencao_alta`
5. `retencao_linear`

---

## Comparação de eficiência

Ranking dos criativos por custo de atenção:

| Métrica de ranking | O que compara | Melhor = |
|--------------------|---------------|----------|
| Cost per Hook | Custo de cada pessoa que passou do gancho | Menor valor |
| Cost per Hold | Custo para sustentar até o meio | Menor valor |

**Formato de comparação:**

```
RANKING DE EFICIÊNCIA DE ATENÇÃO (por Cost per Hook)

1. Criativo "VSL Curso v3":          R$ 0,14/hook  (o mais barato para capturar atenção)
2. Criativo "Depoimento Maria":      R$ 0,18/hook
3. Criativo "Carrossel benefícios":  R$ 0,25/hook
4. Criativo "Imagem estática":       R$ 0,41/hook  (o mais caro)
```

**Insight obrigatório:** comparar Cost per Hook vs Cost per Hold para identificar criativos que capturam atenção barata mas perdem rápido (custo de hook baixo, custo de hold desproporcional) vs criativos que custam mais para atrair mas retêm com eficiência (custo de hook alto, custo de hold proporcional).

---

## Tratamento sem vídeo (contas com apenas imagem)

Quando **nenhum anúncio** no escopo tem métricas de vídeo:

| Métrica de vídeo | Substituto para imagem |
|------------------|----------------------|
| Hook Rate | `nao_aplicavel_formato_imagem` |
| Hold Rate | `nao_aplicavel_formato_imagem` |
| Story Rate | `nao_aplicavel_formato_imagem` |
| Completion Rate | `nao_aplicavel_formato_imagem` |
| Cost per Hook | `nao_aplicavel_formato_imagem` |
| Cost per Hold | `nao_aplicavel_formato_imagem` |

**Proxies de atenção para imagem:**
- **CTR** como proxy de interesse visual (a imagem atraiu o suficiente para clicar)
- **CPC** como proxy de custo de atenção (custo para gerar uma ação)

**Classificação por perfil de CTR (imagem):**

| Perfil | Critério | Interpretação |
|--------|----------|---------------|
| `imagem_atrativa` | CTR > 2.0% | Imagem captura atenção e gera clique |
| `imagem_funcional` | CTR 1.0% - 2.0% | Imagem cumpre o papel, sem destaque |
| `imagem_invisivel` | CTR < 1.0% | Imagem não se destaca no feed |

**Declaração obrigatória:** "Análise baseada em CTR e CPC como proxies de atenção. Sem métricas de vídeo, não é possível mapear curva de retenção nem identificar ponto de queda. As conclusões sobre atenção são limitadas ao comportamento de clique."

**Mix (imagem + vídeo):** analisar separadamente. Vídeos com curva completa, imagens com proxies. Nunca misturar no mesmo ranking. Apresentar dois blocos distintos.

---

## Explicação obrigatória (regra dura)

Todo número, classificação e curva DEVE ter texto explicativo em linguagem natural. O aluno precisa entender o que o número significa, por que está nesse nível e o que fazer.

### Templates por perfil

**Gancho forte, desenvolvimento fraco:**
```
Criativo "{nome}": GANCHO FORTE, DESENVOLVIMENTO FRACO

O que está acontecendo: esse criativo para o scroll de {hook_rate}%
das pessoas (25% ou mais, saudável). Mas apenas {hold_rate}% de quem
fica 3 segundos chega até a metade do vídeo. Algo entre o gancho e o
meio do vídeo faz o público perder interesse.

O que isso significa na prática: você tem um gancho que funciona. Esse é
um ativo valioso. O problema está no que vem depois.

O que fazer: manter os primeiros 3-5 segundos do vídeo (o gancho funciona)
e refazer o desenvolvimento. Testar uma versão nova com transição diferente
após o gancho.
```

**Gancho médio, retenção alta:**
```
Criativo "{nome}": GANCHO MÉDIO, RETENÇÃO ALTA

O que está acontecendo: o criativo captura {hook_rate}% das pessoas
(dentro da média), mas quem decide ficar, fica. Hold Rate de {hold_rate}%
é excelente.

O que isso significa na prática: o conteúdo do vídeo é forte, mas poucas
pessoas param para descobrir isso. O gargalo é a porta de entrada.

O que fazer: testar 2-3 ganchos novos (primeiros 3 segundos) mantendo
o restante do vídeo intacto. O corpo funciona, só precisa de mais gente
entrando.
```

**Retenção linear:**
```
Criativo "{nome}": RETENÇÃO LINEAR ✅

O que está acontecendo: o público assiste de forma consistente. A maior
queda entre etapas é de apenas {max_drop}%. Não há um ponto de abandono
dramático.

O que isso significa na prática: perfil saudável de atenção. Se o CPA está
na meta, proteger este criativo. Se não está convertendo, o problema
provavelmente não é atenção. Investigue intenção e conversão.
```

**Queda abrupta no meio:**
```
Criativo "{nome}": QUEDA ABRUPTA NO MEIO ⚠️

O que está acontecendo: {pct_queda}% do público abandona entre o primeiro
quarto e a metade do vídeo. A queda é drástica e concentrada nesse trecho.

O que isso significa na prática: algo nesse intervalo causa rejeição massiva.
Pode ser mudança brusca de tom, promessa quebrada, ou conteúdo que não entrega
o que o gancho prometeu.

O que fazer: revisar o trecho entre 25% e 50% do vídeo. Algo nessa parte
precisa mudar.
```

**Atenção baixa:**
```
Criativo "{nome}": ATENÇÃO BAIXA ❌

O que está acontecendo: apenas {hook_rate}% das pessoas passam do gancho.
O scroll não para. O gancho não funciona.

O que isso significa na prática: o criativo não está conseguindo competir
pela atenção no feed. Mudanças incrementais provavelmente não resolvem.

O que fazer: testar gancho completamente novo. Opções: abertura com uma
afirmação direta sobre a dor principal do público, movimento nos primeiros
frames, texto grande em tela nos primeiros 2 segundos, ou formato diferente
(se era a pessoa falando para a câmera, testar imagens de apoio; se eram
imagens de apoio, testar o rosto na câmera). A produção do gancho novo
fica com /copy-anuncio, /mandala-de-anuncios ou as skills de vídeo.
```

---

## Output YAML

```yaml
leitura_atencao:
  periodo: "2026-05-20 a 2026-05-27"
  periodo_anterior: "2026-05-13 a 2026-05-20"
  nivel_analise: metricas | metricas_mais_descricao
  produto: "Produto A"
  criativos_analisados: 6
  formato_mix: "4 vídeos, 2 imagens"
  padrao_transversal: null | "Hook Rate caindo em toda a conta (-18%)"

  videos:
    - ad_id: "<ad_id_1>"
      ad_name: "VSL Curso v3"
      metricas:
        impressions: 28500
        video_3sec_views: 8550
        video_p25_watched: 7125
        video_p50_watched: 3420
        video_p75_watched: 2137
        video_p95_watched: 1282
        video_p100_watched: 855
        video_plays: 9975
        spend: 1026.00
      derivadas:
        hook_rate: 0.250
        hold_rate: 0.400
        story_rate: 0.300
        completion_rate: 0.129
        cost_per_hook: 0.14
        cost_per_hold: 0.30
      curva_retencao:
        impressoes_p25_perda: 0.750
        p25_p50_perda: 0.520
        p50_p75_perda: 0.375
        p75_p95_perda: 0.400
        p95_p100_perda: 0.333
      ponto_de_queda: "impressoes_p25"
      perfil_atencao: "gancho_forte_dev_fraco"
      comparacao_temporal:
        hook_rate_anterior: 0.300
        hook_rate_atual: 0.250
        direcao: "piorando"
        variacao_pct: -16.7

    - ad_id: "<ad_id_2>"
      ad_name: "Depoimento Maria"
      # ... mesma estrutura

  imagens:
    - ad_id: "<ad_id_3>"
      ad_name: "Carrossel benefícios"
      metricas:
        impressions: 15000
        clicks: 225
        ctr: 1.50
        cpc: 2.80
        spend: 630.00
      metricas_video: nao_aplicavel_formato_imagem
      perfil_atencao_imagem: "imagem_funcional"
      comparacao_temporal:
        ctr_anterior: 1.65
        ctr_atual: 1.50
        direcao: "piorando"
        variacao_pct: -9.1

  ranking_eficiencia:
    por_cost_per_hook:
      - ad_name: "VSL Curso v3"
        valor: 0.14
      - ad_name: "Depoimento Maria"
        valor: 0.18
    por_cost_per_hold:
      - ad_name: "Depoimento Maria"
        valor: 0.25
      - ad_name: "VSL Curso v3"
        valor: 0.30

  insight_eficiencia: "VSL Curso v3 captura atenção mais barato (R$ 0,14/hook), mas Depoimento Maria sustenta com mais eficiência (R$ 0,25/hold vs R$ 0,30)."
```

---

## Relatório humano

Usar a estrutura de 7 seções do SKILL.md principal, com foco nas seções 1, 2, 3, 5 e 7. Exemplo narrativo:

```
1. CONTEXTO RESUMIDO

Analisei 6 criativos (4 vídeos, 2 imagens) do Produto A nos últimos
7 dias (20/05 a 27/05). Nível da análise: métricas (sem descrição dos
criativos). Período anterior: 13/05 a 20/05. Limitação: as 2 imagens
foram avaliadas apenas por CTR/CPC, sem curva de retenção.


2. DIAGNÓSTICO REAL

O que as métricas dizem:
- O Hook Rate médio da conta caiu 18% na última semana. Os criativos
  estão perdendo capacidade de parar o scroll.
- Dos 4 vídeos, 2 têm perfil "gancho forte, desenvolvimento fraco":
  atraem atenção mas perdem o público no meio.
- O criativo "Depoimento Maria" é o único com retenção linear
  consistente, mas tem Hook Rate médio (19%).
- "VSL Curso v3" tem o melhor hook da conta (25%), mas Hold Rate de
  apenas 40%. Perde 52% do público entre p25 e p50.

O que as métricas NÃO dizem:
- Sem ver o conteúdo dos vídeos, não sabemos POR QUE a queda acontece
  no meio. As hipóteses são comportamentais.
- Não sabemos se a queda de Hook Rate é fadiga (mesmo público vendo
  muitas vezes) ou perda de relevância (criativo envelheceu).

Erro a evitar: não matar o "Depoimento Maria" pelo Hook Rate médio.
Ele tem a melhor retenção da conta. O problema é a porta de entrada,
não o conteúdo.


3. HIPÓTESE CENTRAL

O gancho dos criativos está perdendo força (Hook Rate caindo em toda a
conta), e os que ainda capturam atenção não sustentam no desenvolvimento
(2 de 4 vídeos com perfil gancho_forte_dev_fraco).

Nível de confiança: médio-alto. A tendência de queda do Hook Rate é
consistente entre os 4 vídeos, mas 7 dias é janela curta para confirmar
fadiga.


5. RISCOS E ARMADILHAS

- Risco 1: matar criativos pela atenção quando o problema pode ser
  intenção ou conversão. Hook/Hold bom não garante venda. Esperar os
  módulos seguintes antes de decidir.
- Risco 2: focar em melhorar o Hold Rate do "VSL Curso v3" sem testar
  ganchos novos para o "Depoimento Maria". Os dois precisam de ações
  diferentes.
- Armadilha: confundir atenção baixa temporária com criativo morto.
  Se a frequência subiu, o criativo pode estar ok, o público que
  está saturado.


7. DECISÃO RECOMENDADA

Fazer agora:
- Testar 2 ganchos novos (primeiros 3s) no "Depoimento Maria",
  mantendo o corpo do vídeo.
- Refazer o trecho p25-p50 do "VSL Curso v3" (manter o gancho).

NÃO fazer:
- Não pausar nenhum criativo ainda. A leitura de atenção sozinha
  não justifica pausa. Esperar intenção e conversão.

Fazer SOMENTE SE:
- Se o Hook Rate continuar caindo na próxima semana, aí sim considerar
  que é fadiga e não apenas flutuação.
```

---

## Repasse para os módulos seguintes

Quando rodando como parte da Inteligência Completa (opção [1]):

**Dados que esta sub-skill repassa para o módulo de Intenção Criativa:**
- Perfil de atenção de cada criativo
- Hook Rate de cada criativo (usado como denominador no Intent Rate)
- Criativos classificados como `atencao_baixa` (para contextualizar CTR baixo)

**Dados que repassa para o Diagnóstico Criativo:**
- Classificação completa por perfil
- Ponto de queda de cada criativo
- Comparação temporal (melhorando/piorando/estável)
