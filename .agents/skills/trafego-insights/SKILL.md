---
name: trafego-insights
description: >
  Base de conhecimento e fonte única de leitura de métricas Meta Ads (Facebook + Instagram).
  Puxa dados nativos da Graph API, calcula métricas derivadas (connect rate, taxa de conversão da
  página, taxa de conversão do anúncio, taxas de checkout) e entrega payload pronto para diagnóstico.
  É a base de dados que /trafego-otimizar, /trafego-escalar, /trafego-analise e /trafego-diagnostico consomem.
  Consultada também pelo command /trafego-insights quando o aluno quer ver números de uma campanha.
  Use sempre que precisar puxar performance, listar campanhas, calcular CPA/CPL/ROAS ou comparar
  janelas temporais.
user-invocable: false
---

# Tráfego Insights. Leitura de Métricas Meta Ads

Você é a fonte única de verdade sobre dados de performance do Meta Ads. Seu papel é puxar dados nativos da Graph API, calcular métricas derivadas, e entregar payload estruturado que outras skills (/trafego-otimizar, /trafego-escalar, /trafego-analise, /trafego-diagnostico) consomem para tomar decisão. Você **não toma decisão**: apenas entrega dado bem formatado e bem atribuído.

**Princípios que guiam toda chamada:**
- Janela de atribuição é declarada explicitamente em todo output. Sem janela declarada, dado não tem significado.
- Métricas derivadas são parte do payload obrigatório. Não são opcionais. São o que diferencia leitura sênior de leitura crua.
- Sempre cruzar 3 janelas temporais da trilha (curta, média, longa). Sem isso, não dá para diagnosticar tendência depois.
- Cache de 5 minutos para proteger rate limit. Mas dado pós-edição (publicar, pausar, ajustar budget) sempre invalida cache.
- Falha parcial é aceitável. Em modo conta completa, uma campanha com problema não pode quebrar o relatório das outras.

---

## 1. Inputs

### 1.1 Obrigatório (um dos dois)
- `campaign_id`. Para leitura de campanha específica e seus filhos (conjuntos e anúncios).
- `escopo: conta_completa`. Para varredura de todas as campanhas ativas da conta.

### 1.2 Opcionais com default
| Input | Default | Descrição |
|---|---|---|
| `nivel` | `auto` | `auto` (skill decide), `campaign`, `adset`, `ad`. No modo `auto`, retorna campanha + conjuntos + anúncios em uma chamada estruturada. |
| `tipo_funil` | inferir | `perpetuo_venda_direta` ou `lancamento_captacao`. Quando inferir falhar, perguntar. Define quais janelas e métricas-norte aplicar. |
| `ticket_brl` | inferir | Necessário para classificar trilha. Pergunta se não conseguir inferir. |
| `janelas` | derivar da trilha | Lista explícita de janelas. Default: as 3 da trilha (1d/3d/7d, 3d/7d/14d, 7d/14d/30d, etc.). Aceita override (ex: `["7d", "30d", "lifetime"]`). |
| `data_inicio` / `data_fim` | n/a | Janela custom em vez das padrão da trilha. Formato `YYYY-MM-DD`. |
| `janela_atribuicao` | conta default → `7d_click` | Atribuição usada na consulta. Override com `1d_click`, `7d_click`, `1d_view`, `7d_click_1d_view`. |
| `incluir_pausadas` | `false` | Se `true`, inclui ativos com `status: PAUSED`. |
| `incluir_arquivadas` | `false` | Se `true`, inclui `status: ARCHIVED` e `DELETED`. |
| `usar_cache` | `true` | Cache de 5 min em memória + cache em arquivo .md. Sempre `false` após uma ação de edição na mesma conversa. |
| `breakdowns` | `[]` | Lista de breakdowns da Graph API (ex: `["age", "gender"]`, `["publisher_platform"]`, `["hourly_stats_aggregated_by_advertiser_time_zone"]`). Cada breakdown gera 1 chamada e 1 arquivo de cache. Ver `sub-skills/breakdowns.md`. |
| `incluir_serie_diaria` | `false` | Se `true`, calcula `serie_diaria` (valores dia a dia) das métricas-norte (CPA/CPL) e leading (CTR, CPM) para cada entidade. Adiciona campos `{metrica}_cv` (coeficiente de variação) ao output. Requer janela >= 3d. Consumido por `/trafego-diagnostico` (score de confiança, falso vencedor). |

---

## 2. Janela de atribuição

A janela de atribuição é o que define **quais conversões contam** para cada anúncio. Sem declarar, número não tem significado.

### 2.1 Detecção automática
A skill primeiro tenta ler a janela de atribuição padrão da ad account via Graph API:

```
GET /act_{ad_account_id}?fields=attribution_spec
```

Se a conta tem atribuição configurada, usar essa.

### 2.2 Fallback
Se não houver atribuição configurada na conta (raro mas acontece em contas novas), default = `7d_click` (padrão atual da plataforma).

### 2.3 Override
O gestor pode pedir explicitamente outra janela (ex: "quero ver com atribuição de 1 dia"). Skill respeita e declara no output.

### 2.4 Sempre declarar no output
Todo bloco de métricas declara qual atribuição foi usada. Sem isso, comparação entre campanhas e leitura histórica fica corrompida.

---

## 3. Janelas temporais. Sempre cruzar 3 da trilha

Quando o `tipo_funil` e `ticket_brl` estão disponíveis, classificar a trilha e puxar **as 3 janelas** automaticamente em uma única chamada (paralela quando possível). Isso permite diagnóstico de tendência das outras skills funcionar sem chamadas adicionais.

### 3.1 Janelas por trilha

| Trilha | Janela curta | Janela média | Janela longa |
|---|---|---|---|
| `perpetuo_low` (até R$ 500) | 1d | 3d | 7d |
| `perpetuo_mid` (R$ 501 a 1.499) | 3d | 7d | 14d |
| `perpetuo_high` (R$ 1.500+) | 7d | 14d | 30d |
| `lancamento_low/mid/high` | 1d | 3d | 7d |

### 3.2 Janela custom
Se o gestor pedir janela explícita (`data_inicio` + `data_fim`), puxar essa janela única e declarar como `custom_range`. Não cruzar 3 janelas neste caso.

### 3.3 Lifetime
`lifetime` (toda a vida da campanha) sempre disponível como bloco extra quando o gestor pedir explicitamente, mas não entra no cruzamento padrão.

---

## 4. Métricas que a skill puxa

### 4.1 Métricas nativas da Graph API
Endpoint: `GET /{object_id}/insights`

Os nomes desta seção são os da Graph API (modo `APP`). No modo `MCP_CONECTOR`, o conector usa outros nomes e não aceita `actions` nem `action_values` crus: usar a tradução da seção 10.1 (Contrato do conector da Meta).

Campos obrigatórios na requisição:
```
spend, impressions, reach, frequency, clicks, cpc, cpm, ctr,
inline_link_clicks, inline_link_click_ctr,
unique_inline_link_clicks, unique_inline_link_click_ctr,
actions, action_values, cost_per_action_type,
video_p25_watched_actions, video_p50_watched_actions,
video_p75_watched_actions, video_p100_watched_actions,
video_thruplay_watched_actions, video_avg_time_watched_actions,
date_start, date_stop, account_currency
```

Em `actions`, extrair específico:
- `purchase` (compra)
- `lead` (lead, total da Meta: site + formulário instantâneo)
- `offsite_conversion.fb_pixel_lead` (lead do pixel, só como reserva quando `lead` não vier, ver 4.4)
- `complete_registration`
- `add_to_cart`
- `initiate_checkout`
- `landing_page_view` (LP View)
- `link_click`
- `video_view` (visualização de 3 segundos do vídeo)

### 4.2 Métricas-norte (decide a ação principal)
- **Perpétuo:** `cpa` = `cost_per_action_type[purchase]`.
- **Lançamento:** `cpl` = `spend ÷ leads`, com `leads` contado pela régua da seção 4.4 (a mesma contagem vale para CPL e para as taxas de lead).

### 4.3 Métricas leading
- `ctr_link_unico` (`unique_inline_link_click_ctr`). **Métrica leading primária.** Conta uma pessoa única por clique no link, removendo viés de cliques repetidos da mesma pessoa. Vale mais que CTR geral porque exclui clique acidental fora do link e mais que CTR no link total porque exclui repetição.
- `ctr_link_total` (`inline_link_click_ctr`). Métrica complementar. Conta todos os cliques no link (com repetição da mesma pessoa). Útil para diagnóstico complementar: se `ctr_link_total` é muito maior que `ctr_link_unico`, indica que poucas pessoas clicam várias vezes (possível bot ou audiência muito reduzida).
- `hook_rate` = `video_p25_watched_actions` ÷ `impressions` (proxy para 3s. Meta deprecou alguns campos antigos de vídeo). Faixas: crítico abaixo de 15%, atenção de 15% a 25%, saudável 25% ou mais. Thumbstop, quando aparecer em outra skill, é esta mesma conta.
- `frequencia` (`frequency`).
- `cpm`.

### 4.4 Eventos brutos para cálculo de derivadas
- `link_clicks` (`inline_link_clicks`)
- `lp_views` (`actions[landing_page_view]`)
- `add_to_cart` (`actions[add_to_cart]`)
- `initiate_checkout` (`actions[initiate_checkout]`)
- `purchases` (`actions[purchase]`)
- `leads`: `actions[lead]` (total da Meta, site + formulário instantâneo) quando vier; sem ele, `actions[offsite_conversion.fb_pixel_lead]`. **Nunca somar os dois** (o `lead` já inclui o lead do pixel). No conector: `results` quando o objetivo da campanha é leads; senão, o campo que `ads_get_field_context` indicar (seção 10.1).

### 4.5 Métricas de vídeo (régua única do projeto)
Toda skill de tráfego que usa métrica de vídeo (ex.: `/trafego-criativos`) segue estas definições.

| Métrica | Campo na Graph API (modo `APP`) | Conta |
|---|---|---|
| `video_plays` (reproduções) | `video_play_actions` | n/a |
| `video_3s` (visualização de 3 segundos) | `actions[video_view]` | n/a |
| `video_p25` a `video_p100` (retenção) | `video_p25_watched_actions`, `video_p50_watched_actions`, `video_p75_watched_actions`, `video_p95_watched_actions`, `video_p100_watched_actions` | n/a |
| `hook_rate` | `video_p25_watched_actions` e `impressions` | `video_p25 ÷ impressions` (faixas na 4.3) |
| `hold_rate` | `video_p50_watched_actions` e `actions[video_view]` | `video_p50 ÷ video_3s` (das pessoas que ficaram 3 segundos, quantas chegam à metade) |
| `completion_rate` | `video_p95_watched_actions` e `video_play_actions` | `video_p95 ÷ video_plays` |

`video_p95_watched_actions` e `video_play_actions` não fazem parte da lista padrão da 4.1: entram como acréscimo à coleta quando a skill que consome pede (ex.: leitura de atenção da `/trafego-criativos`). No modo `MCP_CONECTOR`, os campos de vídeo não estão na lista conferida: conferir os nomes com `ads_get_field_context` antes da coleta (seção 10.1). Campo que não vier deixa a métrica `null` (`indisponível neste nível`). Reservas permitidas (marcadas `fallback_aplicado` e declaradas ao aluno): sem visualizações de 3 segundos, o `hold_rate` usa `video_p25` no denominador; sem `video_play_actions`, o `completion_rate` usa `video_3s` (ou, sem ele, `video_p25`) no denominador.

---

## 5. Métricas derivadas (calculadas pela skill)

A skill **sempre** calcula e entrega as 7 métricas derivadas no output. Estas são parte do vocabulário comum do sistema e não devem ser duplicadas em outras skills.

### 5.1 Definições

| Métrica | Fórmula | Quando aplica |
|---|---|---|
| `connect_rate` | `lp_views ÷ link_clicks` | Sempre |
| `taxa_conversao_pagina_perpetuo` | `purchases ÷ lp_views` | Apenas perpétuo |
| `taxa_conversao_pagina_lancamento` | `leads ÷ lp_views` | Apenas lançamento |
| `taxa_conversao_anuncio_perpetuo` | `purchases ÷ link_clicks` | Apenas perpétuo |
| `taxa_conversao_anuncio_lancamento` | `leads ÷ link_clicks` | Apenas lançamento |
| `taxa_carrinho_compra` | `purchases ÷ add_to_cart` | Apenas perpétuo |
| `taxa_checkout_compra` | `purchases ÷ initiate_checkout` | Apenas perpétuo |

### 5.2 Custo por etapa de funil (perpétuo)
Calcular para diagnosticar onde o custo escala desproporcionalmente:
- `custo_por_lp_view` = `spend ÷ lp_views`
- `custo_por_atc` = `spend ÷ add_to_cart`
- `custo_por_ic` = `spend ÷ initiate_checkout`
- `custo_por_purchase` = `spend ÷ purchases` (= CPA)

### 5.3 Tratamento de denominador zero
Se denominador for 0 (ex: 0 link clicks), retornar `null` em vez de erro. Outras skills sabem interpretar `null` como "dado insuficiente".

### 5.4 Tratamento de dados imaturos
Se denominador for menor que 50 (ex: 30 link clicks), calcular mas marcar `confiabilidade: baixa`. Acima de 200, `confiabilidade: alta`. Entre 50 e 200, `media`.

---

## 6. Modo conta completa

Quando `escopo: conta_completa`, a skill executa em duas fases:

### 6.1 Fase de listagem
1. `GET /act_{id}/campaigns?fields=id,name,status,effective_status,created_time,objective,daily_budget,lifetime_budget&limit=200&effective_status=%5B%22ACTIVE%22%5D`
2. Para cada campanha ativa, puxar insights da janela média da trilha (ex: 7d para perpétuo low).
3. Calcular métrica-norte (CPA ou CPL) por campanha.
4. Ranquear por urgência:
   - **Crítico** (CPA/CPL ≥ 1.7× target): topo do ranking
   - **Atenção** (CPA/CPL 1.3 a 1.7× target): meio
   - **Saudável** (CPA/CPL ≤ target): base

### 6.2 Fase de drill-down (top 5 piores)
Para as 5 campanhas no topo do ranking (mais urgentes), automaticamente:
- Puxar as 3 janelas da trilha
- Puxar conjuntos e anúncios filhos
- Calcular métricas derivadas
- Entregar payload completo pronto para diagnóstico de otimização

Para as demais (saudáveis ou volume baixo), entregar apenas o resumo da janela média.

### 6.3 Limites
- Máximo 200 campanhas listadas por chamada (paginação acima disso).
- Drill-down limitado a 5 campanhas por execução para proteger rate limit.

### 6.4 Modo `escopo: conta_completa, nivel: ad` (varredura plana de ads)

Quando a chamada vem com `escopo: conta_completa` **e** `nivel: ad` explicitamente declarado, a skill **pula** a fase de ranking + drill-down em top 5 e roda uma varredura plana retornando todos os ads ativos da conta com métricas da janela média da trilha. Esse modo é consumido por `/trafego-escalar` (Passo 0.75.1) para detectar ads vencedores espalhados em conjuntos diferentes.

**Output específico desse modo:**

```yaml
status: ok
ad_account_id: act_<id>
escopo: conta_completa
nivel: ad
total_ads_ativos: 64

ads:
  - id: <ad_id>
    nome: <nome>
    campaign_id: <id>
    campaign_name: <nome>
    adset_id: <id>
    adset_name: <nome>
    metricas_janela_media:
      spend: ...
      impressions: ...
      link_clicks: ...                  # inline_link_clicks; no conector, link_click
      ctr_link_unico: ...               # unique_inline_link_click_ctr; no conector fica null (salvo se ads_get_field_context devolver o campo único, seção 10.1)
      ctr_link_total: ...               # inline_link_click_ctr; no conector, link_click ÷ impressions (calculado). Com ctr_link_unico null, quem consome usa este e declara a troca
      purchases_ou_leads: ...
      cpa_ou_cpl: ...
      conversoes: ...
    classificacao_vencedor: true | false           # definição única de anúncio vencedor da /trafego-escalar (Passo 0.75.1): CTR único saudável (no conector, o ctr_link_total) + 50 conversões em low e middle ticket ou 30 em high ticket, pelo tipo do produto no resumo (não pela trilha da 3.1), na janela média da trilha; o "validado" da /trafego-testes é somado pela skill que consome
```

**Limite de proteção a rate limit:** máximo 200 ads por execução. Acima disso, paginar com cursor.

---

## 7. Cache em duas camadas (memória + arquivo)

A skill mantém dois níveis de cache, complementares:

### 7.1 Cache em memória (curto prazo)
- Chave: os mesmos parâmetros do cache em arquivo (`sub-skills/cache.md` seção 5): conta (`ad_account_id`), período (`janelas` ou `data_inicio`/`data_fim`), `janela_atribuicao`, quebras (`breakdowns`) e `hash_filtros`. O `hash_filtros` cobre só o filtro de escopo (`campaign_id` ou `conta_completa`, e `nivel`) e o de status (`incluir_pausadas`, `incluir_arquivadas`). Mudou qualquer um desses, é cache miss.
- TTL: **5 minutos**.
- Escopo: por sessão de conversa. Não persiste entre conversas.
- Camada mais rápida, evita refetch dentro da mesma chamada.

### 7.2 Cache em arquivo .md (médio prazo, entre sessões)
- Localização: `meus-produtos/{ativo}/trafego/insights/` (sem produto ativo: `meus-produtos/_global/trafego/insights/`).
- TTL adaptativo: 1h (today), 6h (7-14d); 30d e períodos fechados valem até o fim do dia. O cache só vale no mesmo dia (fuso America/Sao_Paulo) e para os mesmos parâmetros da chave da 7.1 (conta, período, janela de atribuição, quebras e `hash_filtros`, que cobre escopo e status): mudou o dia, busca de novo.
- Resposta com erro, ou leitura em que a chamada principal falhou, nunca vira cache.
- Schema completo, naming convention e algoritmo de leitura: ver **`sub-skills/cache.md`**.
- Permite que outras skills (`/trafego-otimizar`, `/trafego-regras`, `/trafego-publicos`, `/trafego-testes`, e a `/trafego-analise` nas quebras que as sub-skills pedem) compartilhem leituras dentro do mesmo dia, evitando bater na Graph API repetidas vezes pelo mesmo período. A busca base da `/trafego-analise` (Passo 4 dela) é própria e não passa por este cache.

### 7.3 Ordem de consulta
1. Memória → se hit válido, retorna.
2. Arquivo .md → se hit válido (não stale, não expirado), retorna e popula memória.
3. Graph API → busca, salva no arquivo .md e na memória.

### 7.4 Invalidação automática
Ambos os caches da `ad_account_id` (memória + todos os arquivos da pasta) são invalidados **imediatamente** quando:
- Qualquer skill de edição executa write (`/trafego-otimizar`, `/trafego-escalar`, `/trafego-criar-campanha`, `/trafego-regras`, `/trafego-publicos`, `/trafego-testes`).
- Gestor pede explicitamente "atualizar dados" ou "puxar de novo sem cache".
- TTL expirou.

Arquivos em disco são marcados com sufixo `.stale.md` em vez de deletados (preserva auditoria).

### 7.5 Bypass manual
Gestor pode forçar leitura fresca com `usar_cache: false` no input ou flag `--refresh` no command.

---

## 8. Tratamento de erros (falha parcial)

Quando uma chamada à Graph API falha em modo `escopo: conta_completa`, a skill **não falha o relatório inteiro**. Em vez disso:

### 8.1 Erros recuperáveis (mantém relatório, marca o item)
- Permissão negada em uma campanha específica (código 200): pula a campanha, registra em `erros[]`.
- Conta sem dados na janela: retorna métricas zeradas, marca `dados_disponiveis: false`.
- Rate limit pontual (código 4 ou 17): aguarda backoff exponencial (1s, 2s, 4s, 8s. Máximo 4 retries) antes de marcar como erro definitivo.

### 8.2 Erros fatais (falha a skill toda)
- Token revogado (código 190): para tudo, instrui o gestor a executar `/trafego-conexao`.
- Ad account inteira sem permissão: para tudo, instrui o gestor a verificar atribuição do System User.
- Erro 100 com mensagem indicando ID inválido: para tudo, declara qual ID está errado.

### 8.3 Output sempre tem bloco de erros
Mesmo em sucesso total, o campo `erros[]` aparece no output como lista vazia. Quando há erros parciais, eles aparecem com contexto suficiente para o gestor entender o que ficou de fora.

---

## 9. Output esperado

### 9.1 Modo campanha única (nivel: auto)

```yaml
status: ok | erro_fatal
ad_account_id: "act_1234567890"
campaign_id: "120203456789"
trilha: perpetuo_low | perpetuo_mid | perpetuo_high | lancamento_low | lancamento_mid | lancamento_high
moeda: BRL

contexto:
  janela_atribuicao: "7d_click"
  detectada_da_conta: true
  cache_usado: false
  timestamp_leitura: "2026-05-04T14:30:00-03:00"

campanha:
  id: "120203456789"
  nome: "Perpétuo - Curso X - 2026"
  objetivo: OUTCOME_SALES
  status: ACTIVE
  effective_status: ACTIVE
  created_time: "2026-03-15T10:30:00-0300"
  budget:
    tipo: ABO | CBO
    valor_diario_brl: 200.00        # sempre na unidade da moeda (reais), nunca em centavos (seção 10.1)
  metricas_por_janela:
    curta:                                # ex: 1d
      janela: "1d"
      spend: 198.50
      impressions: 12450
      reach: 8920
      frequency: 1.4
      ctr_link_unico: 0.0118       # unique_inline_link_click_ctr, primária (no conector, null salvo a exceção da seção 10.1)
      ctr_link_total: 0.0142       # inline_link_click_ctr, complementar
      hook_rate: 0.27
      cpm: 15.95
      cpm_cv: null                    # coeficiente de variação diária do CPM
      cpa: 198.50
      cpa_cv: null                    # coeficiente de variação diária (desvio padrão / média). null quando janela < 3d
      cpl: null
      eventos:
        link_clicks: 177
        lp_views: 152
        add_to_cart: 18
        initiate_checkout: 12
        purchases: 1
        leads: null
      derivadas:
        connect_rate: 0.859
        taxa_conversao_pagina: 0.0066
        taxa_conversao_anuncio: 0.0056
        taxa_carrinho_compra: 0.056
        taxa_checkout_compra: 0.083
        custo_por_lp_view: 1.31
        custo_por_atc: 11.03
        custo_por_ic: 16.54
        custo_por_purchase: 198.50
      confiabilidade: baixa | media | alta
      dados_disponiveis: true
    media:                                # ex: 3d
      ...
    longa:                                # ex: 7d
      ...

conjuntos:
  - id: "120203456789001"
    nome: "AS - Lookalike compradores 1%"
    status: ACTIVE
    effective_status: ACTIVE | PAUSED | CAMPAIGN_PAUSED | IN_PROCESS | WITH_ISSUES | ARCHIVED   # não informa a fase de aprendizado
    created_time: "2026-03-15T10:35:00-0300"
    budget_diario_brl: 100.00       # sempre na unidade da moeda (reais), nunca em centavos (seção 10.1)
    aprendizado: ATIVO | EM_APRENDIZADO | APRENDIZADO_LIMITADO | NAO_VERIFICADO   # de learning_stage_info.status: SUCCESS | LEARNING | FAIL; no conector, só se ads_get_field_context listar o campo (senão NAO_VERIFICADO)
    metricas_por_janela:
      curta: { ... }
      media: { ... }
      longa: { ... }

anuncios:
  - id: "120203456789999"
    nome: "AD - Mito - Vídeo 30s"
    status: ACTIVE
    effective_status: ACTIVE
    created_time: "2026-03-15T11:00:00-0300"
    adset_id: "120203456789001"
    metricas_por_janela:
      curta: { ... }
      media: { ... }
      longa: { ... }

erros: []
```

### 9.2 Modo conta completa

```yaml
status: ok | erro_fatal
ad_account_id: "act_1234567890"
escopo: conta_completa
moeda: BRL

contexto:
  janela_atribuicao: "7d_click"
  cache_usado: false
  timestamp_leitura: "2026-05-04T14:30:00-03:00"
  total_campanhas_ativas: 14
  drill_down_aplicado_em: 5

ranking_urgencia:
  - posicao: 1
    classificacao: critico
    campaign_id: "120203456789"
    nome: "Perpétuo - Curso X"
    cpa_ou_cpl_atual: 198.50
    target: 100.00
    desvio_pct: +98.5
    drill_down_disponivel: true

  - posicao: 2
    classificacao: atencao
    campaign_id: "..."
    ...

  - posicao: 14
    classificacao: saudavel
    campaign_id: "..."
    ...

drill_down:                              # apenas top 5
  - campaign_id: "120203456789"
    [bloco completo igual ao output de campanha única]
  - campaign_id: "..."
    ...

resumo:
  saudaveis: 8
  atencao: 3
  criticas: 3
  total_spend_periodo_brl: 2840.00

erros: []
```

### 9.3 Modo erro fatal

```yaml
status: erro_fatal
codigo: token_revogado | sem_permissao_conta | id_invalido
mensagem: "Token revogado pelo Meta. Provavelmente houve troca de senha do admin que criou o System User."
acao_recomendada: "Execute /trafego-conexao para regenerar o token."
detalhes_tecnicos:
  graph_api_error_code: 190
  graph_api_message: "..."
```

---

## 10. Como puxar os dados (rota por META_AUTH_MODO)

A skill respeita a preferência de conexão definida em `META_AUTH_MODO` no `.env` (ver `/trafego-conexao`). Só existem dois modos: `MCP_CONECTOR` e `APP`. Valor vazio, ausente ou diferente desses dois (inclusive o legado `HIBRIDO`): acionar `/trafego-conexao` antes de ler (Passo 0.2 do command). Esta skill é **100% leitura**, então **não tem lacuna** em nenhum modo: toda leitura tem tool no conector. Não há gate (não escreve na conta).

### 10.1 Contrato do conector da Meta (MCP)

Regras do modo `MCP_CONECTOR`. Fonte: seção 4.3 do `.claude/skills/trafego-dashboard/SKILL.md`, conferida no conector oficial da Meta em 09/10/2026. As outras skills de tráfego apontam para esta seção em vez de manter listas próprias de campos.

Usar as tools de leitura do conector da Meta. **Descobrir a tool pelo final do nome, nunca pelo prefixo**: o prefixo varia por ambiente (pode ser `mcp__Meta_Ads__...` ou um UUID como `mcp__9dc3edbb-...__ads_get_ad_entities`). Procurar pelo final estável `ads_get_ad_entities` ou `ads_get_ad_accounts` (ver `trafego-conexao` §5.1). Nesse modo não se usa token, mesmo que exista um `FB_ACCESS_TOKEN_PERMANENTE` antigo no `.env`.

**Ferramentas (sufixo da tool, a partir da camada lógica da 10.3):**
- `get_ad_account_info` → `ads_get_ad_accounts` (nome, `currency`, `account_status`, `is_ads_mcp_enabled`).
- `list_campaigns`, `get_campaign`, `list_adsets`, `get_adset`, `list_ads`, `get_ad` e `get_insights` (métricas de qualquer nível) → `ads_get_ad_entities` com `level`: `ad_account`, `campaign`, `adset` ou `ad`. Os dados da entidade e as métricas vêm na mesma chamada, com a lista de campos da tabela abaixo.
- Série dia a dia (`incluir_serie_diaria`, seção 12.5) → `ads_get_ad_entities` no `level` da entidade, com `time_increment: "1"`.
- `ads_insights_performance_trend` → só a tendência da conta, de um conjunto ou de um anúncio, quando pedida. **Não faz nível campanha** (volta vazio) e nunca serve para métricas por campanha, ranking, funil, comparativo ou série por campanha.
- Detecção de atribuição / datasets → `ads_get_ad_accounts` / `ads_get_datasets` conforme o campo. Se a atribuição não vier, usar o fallback da seção 2.2 e declarar.

**Tradução dos campos (Graph API da seção 4 → conector):** campos conferidos com `ads_get_field_context` para o `ads_get_ad_entities`.

| Graph API (modo `APP`) | Conector (`ads_get_ad_entities`) |
|---|---|
| `spend` | `amount_spent` |
| `inline_link_clicks` / `actions[link_click]` | `link_click` |
| `actions[landing_page_view]` | `landing_page_view` |
| `actions[purchase]` (`offsite_conversion.fb_pixel_purchase`) | `omni_purchase` |
| `actions[initiate_checkout]` | `omni_initiated_checkout` |
| valor das compras (`action_values[purchase]`) | `offsite_conversion_fb_pixel_purchase_values` (sem ele: `purchase_roas × amount_spent`) |
| `purchase_roas`, `impressions`, `reach`, `name`, `effective_status`, `campaign_id`, `adset_id` | iguais |
| `daily_budget` (número em centavos) | `daily_budget` (objeto com moeda e valor em reais) |
| resultado do objetivo da campanha | `results` (objeto com `indicator` e `values`) |

Métrica sem evento volta `null`: conta sem pixel de compra mostra compras e faturamento vazios, e isso é dado, não erro.

**Campos sem tradução conferida** (frequência, CPM, CTR, cliques totais, `unique_inline_link_click_ctr`, `cost_per_action_type`, carrinho, leads por evento, métricas de vídeo, demografia):
- Calcular a partir dos conferidos quando der e declarar no output que o número foi calculado: frequência = `impressions ÷ reach`; CPM = `amount_spent ÷ impressions × 1000`; CTR de link (total) = `link_click ÷ impressions`, gravado em `ctr_link_total`; custo por etapa = `amount_spent ÷` evento. O `ctr_link_unico` só é preenchido se `ads_get_field_context` devolver `unique_inline_link_click_ctr` ou os cliques únicos no link; sem esse campo, `ctr_link_unico` fica `null`, com registro em `erros[]`, e quem consome usa o `ctr_link_total` e declara a troca.
- Para o resto, chamar `ads_get_field_context` antes da coleta e pedir só o que ele devolver. Se o campo não existir, marcar a métrica como `indisponível neste nível`, registrar em `erros[]` e seguir sem ela (quando ajudar, guiar o aluno a ler a coluna no Gerenciador). Nunca inventar o número.
- Nunca pedir `actions` ou `action_values` crus ao conector (voltam `Unsupported field`). Nunca afirmar que um campo "não existe no conector" se ele está na tabela acima.
- Leads: `results` quando o objetivo da campanha é leads; senão, o campo que `ads_get_field_context` indicar. Mesma régua da seção 4.4 (nunca somar duas contagens de lead).
- Fase de aprendizado: o `effective_status` não informa aprendizado. Usar o campo que `ads_get_field_context` indicar (`learning_stage_info`); sem esse campo, `aprendizado: NAO_VERIFICADO` e avisar que o conector não mostra essa fase.

**Formatos que o conector exige:**
- `time_range` vai como **texto JSON**: `'{"since":"AAAA-MM-DD","until":"AAAA-MM-DD"}'`, por exemplo `"{\"since\":\"2026-10-01\",\"until\":\"2026-10-07\"}"`. Nunca como objeto nem com `since` e `until` soltos.
- `date_preset` só com os valores válidos da Meta: `today`, `yesterday`, `last_3d`, `last_7d`, `last_14d`, `last_28d`, `last_30d`, `last_90d`, `this_month`, `last_month`, `this_quarter`, `last_quarter`, `this_year`, `last_year`, `maximum` (os mesmos valem na Graph API). Não existem `last_180d`, `last_6_months` nem `last_365d`: para períodos assim, usar `time_range` com as datas calculadas.
- Série por dia: `time_increment: "1"`. Cada linha traz `date_start`; agregar por ele.
- Próxima página em `cursor`. Pedir `limit: 1000` (o máximo). O conector pode cortar a resposta no `limit` sem devolver a próxima página: quando uma consulta chegar ao limite, avisar o aluno e registrar em `erros[]`.
- Filtro: `filtering: [{field: "{nível}.campo", operator, value: [...]}]`. O nível `ad_account` não aceita `sort` nem `filtering`.
- Sem filtro, o conector devolve também entidades antigas sem entrega (uma conta teve mais de 2.000 conjuntos). Quando a pergunta é sobre o que está rodando: em campanha e anúncio, filtrar `impressions` maior que zero (`{field: "campaign.impressions", operator: "GREATER_THAN", value: ["0"]}`, com `ad.` no nível anúncio); em conjunto, `{field: "adset.effective_status", operator: "IN", value: ["ACTIVE"]}`. Para uma entidade específica, filtrar pelo id no mesmo formato (`{field: "campaign.id", operator: "IN", value: ["<id>"]}`).
- Quebras (`breakdowns`): ler os valores aceitos no schema da tool ou em `ads_get_field_context`. Por hora é `hourly_stats_aggregated_by_advertiser_time_zone`, só no nível da conta. Se a quebra pedida não existir, dizer ao aluno e seguir sem ela.
- Orçamento: `daily_budget` em objeto com moeda já está em reais (usar como veio); número puro está em centavos (padrão da Graph API, dividir por 100). O payload sempre entrega `valor_diario_brl` e `budget_diario_brl` na unidade da moeda (reais), nunca em centavos; as outras skills usam esses campos e citam esta regra. Para escrita, cada skill de escrita confere a unidade no schema da tool.
- Moeda: cada conta tem a sua (`currency` em `ads_get_ad_accounts`), que vai no campo `moeda` do output. Nunca somar moedas diferentes: em leitura de várias contas, separar os totais por moeda.
- Conta grande: lista enxuta de campos e `limit` explícito. Se o retorno for salvo em arquivo pela ferramenta, processar o arquivo (ele não tem token) em vez de reler tudo.

O `ad_account_id` exigido pelas tools vem de `FB_AD_ACCOUNT_ID` do `.env` (ou da conta escolhida no Passo 0.3 do command). Se `FB_AD_ACCOUNT_ID` estiver vazio ou ausente (conexão feita por uma versão antiga, que não gravava a conta no modo MCP), nunca seguir com conta vazia nem escolher sozinho uma conta da listagem: acionar `/trafego-conexao` na opção "Validar a conexão atual", que lista as contas pela seção 5.1.1 e grava `FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS`.

**Conta não liberada no conector** (`is_ads_mcp_enabled: false` ou erro "Ads MCP is gradually being rolled out"): parar, avisar o aluno em linguagem simples e oferecer o modo App pelo `/trafego-conexao` (seção 5.1.2 da skill `trafego-conexao`). Uma tool específica em liberação gradual ("This tool is new and is being gradually rolled out") não trava a leitura: usar outra tool de leitura do conector que traga o mesmo dado (conferindo o schema) ou registrar em `erros[]` qual dado ficou de fora.

Ferramentas de leitura que podem complementar a análise quando o aluno pedir: `ads_insights_anomaly_signal` (anomalias), `ads_insights_industry_benchmark` e `ads_insights_auction_ranking_benchmarks` (comparação com o mercado), `ads_account_get_activity_logs` (o que mudou na conta). Os parâmetros vêm do schema da tool na hora.

### 10.2 Modo `APP`
Conferir que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` têm valor (`grep -q "^FB_ACCESS_TOKEN_PERMANENTE=." .env` e `grep -q "^FB_AD_ACCOUNT_ID=." .env`, com o ponto: linha vazia conta como ausente) e chamar a Graph API direto via `curl`, uma chamada por `Bash`, com o token por substituição dentro do próprio comando: `$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)` (seções "LEITURA SEGURA DO .env" e "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" do CLAUDE.md). Usar `curl -g` sempre que a URL tiver `{}` ou `[]` (ex.: campos aninhados no `fields=`, como `adsets{name}`). `effective_status`, `time_range`, `filtering` e `action_attribution_windows` levam aspas e vão sempre URL-codificados (10.2.1): só o `-g` não basta para eles. Nunca exibir o token.

Endpoint base: `https://graph.facebook.com/v25.0/`

Fase de aprendizado do conjunto: pedir `learning_stage_info` no `fields=` do conjunto (`status`: `LEARNING`, `SUCCESS` ou `FAIL`, que viram `EM_APRENDIZADO`, `ATIVO` e `APRENDIZADO_LIMITADO` no campo `aprendizado`). O `effective_status` não informa aprendizado.

### 10.2.1 Boas práticas obrigatórias no Modo APP

**URL encoding:** o `curl` trata colchetes `[]` e chaves `{}` crus na URL como padrão de expansão: colchete dá erro "bad range" (exit code 3) e chave com vírgula vira duas requisições (o `time_range` quebra ao meio). Parâmetros com colchetes, chaves ou aspas (`effective_status`, `time_range`, `filtering`, `action_attribution_windows`) vão URL-encoded, com aspas duplas no JSON antes de codificar. Só pôr `-g` não basta quando o valor tem aspas duplas dentro de uma URL entre aspas duplas. Exemplos:
- `effective_status=["ACTIVE"]` → `effective_status=%5B%22ACTIVE%22%5D`
- `effective_status=["ACTIVE","PAUSED"]` → `effective_status=%5B%22ACTIVE%22%2C%22PAUSED%22%5D`
- `time_range={"since":"2026-10-01","until":"2026-10-07"}` → `time_range=%7B%22since%22%3A%222026-10-01%22%2C%22until%22%3A%222026-10-07%22%7D`
- `filtering=[{"field":"campaign.id","operator":"IN","value":["{ID}"]}]` → `filtering=%5B%7B%22field%22%3A%22campaign.id%22%2C%22operator%22%3A%22IN%22%2C%22value%22%3A%5B%22{ID}%22%5D%7D%5D` (trocar `{ID}` pelo número antes de rodar)
- `action_attribution_windows=["7d_click"]` → `action_attribution_windows=%5B%227d_click%22%5D`

`since` e `until` soltos não valem em `/insights`: usar sempre `time_range`.

**Paginação sem expor o token:** a resposta traz `paging.next` e `paging.previous` com a URL completa da próxima página, que inclui o `access_token`. Nunca copiar, reaproveitar nem exibir essas URLs. Para a próxima página, montar um novo `curl` com `after=<cursor>` (o valor de `paging.cursors.after`; no processamento em Python abaixo, tirado da saída do script) e o token por substituição na hora.

**Cadência entre chamadas (rate limit):** o Meta aplica limite de uso por token. Em modo conta completa, nunca encadear mais de 3 chamadas sem pausa. Aguardar 3 segundos entre cada chamada à Graph API. Em Python, usar `time.sleep(3)` antes de cada request. Se a resposta vier com `"code": 4` (rate limit), aplicar backoff: aguardar 30s antes de retentar. Máximo 2 retries.

**Paths de arquivo:** NUNCA salvar arquivos temporários em `/tmp` ou depender de variáveis de ambiente de sessões bash anteriores (`$TEMP`, `$TMPDIR`). Cada chamada bash tem sessão isolada. Salvar sempre em `meus-produtos/{ativo}/trafego/insights/` com path absoluto derivado do diretório de trabalho atual. Arquivos intermediários (JSONs brutos da API) ficam só na subpasta temporária `meus-produtos/{ativo}/trafego/insights/tmp/`, separada dos caches.

**Processamento em Python (exceção controlada do CLAUDE.md):** só quando o volume não der para processar lendo os JSONs direto. A resposta bruta traz `paging.next` e `paging.previous` com o `access_token`, então ela só existe em disco entre o `curl` que a gravou e a limpeza logo em seguida: nunca fica guardada até o fim nem vai para a pasta dos caches. Ordem:
1. Antes da primeira chamada: apagar sobras de `tmp/*.json` de execuções interrompidas (rate limit, erro ou aluno que parou no meio) e escrever com `Write` o script de limpeza (sem token dentro dele). Ele regrava o JSON bruto sem o bloco `paging` (guarda só `data`; se a resposta for erro, guarda só o bloco `error`), imprime só o cursor `after` (se houver) ou, em resposta de erro, só o código e a mensagem do erro, e nunca imprime nem regrava `paging`.
2. Para cada chamada ou página, nesta ordem: (a) `curl ... > arquivo.json` na subpasta `tmp/` acima; (b) logo em seguida, antes do próximo `curl`, rodar o script de limpeza nesse arquivo. O cursor `after` da próxima página vem da saída do script, nunca da leitura do JSON bruto. Se a saída trouxer um erro, seguir a cadência acima (código 4) e a seção 8 antes de continuar. Resposta com erro não entra no processamento nem no cache.
3. Com todas as respostas já limpas, rodar o processamento (no mesmo script ou em outro, também escrito com `Write`). Sempre com o interpretador detectado na sessão (`python3` ou `py -3`). Nunca heredoc nem `curl | python3` com token.
4. Ao final, apagar os `.json` da subpasta `tmp/`. No cache `.md` (seção 7.2) só entra o payload já processado, sem `paging`.

**Encoding Python (Windows):** o terminal Windows usa `cp1252` por padrão, que não suporta emojis (ex: 👀 nos nomes de campanhas do Instagram). Todo script Python que imprime nomes de campanhas DEVE começar com:
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```
Alternativa quando se escreve em arquivo: abrir com `open(path, 'w', encoding='utf-8')`. Nunca confiar no encoding padrão do terminal.

**f-string com lógica condicional:** NUNCA colocar expressão condicional dentro do especificador de formato. Isso gera `ValueError` em runtime. Sempre resolver antes:
```python
# ERRADO
f"CPA: {valor:.0f if valor else '-'}"

# CORRETO
cpa_str = f"R${valor:.0f}" if valor else '-'
f"CPA: {cpa_str}"
```

**sleep em background:** quando precisar aguardar reset de rate limit, usar `run_in_background=true` na tool Bash. O bash tool bloqueia `sleep` encadeado com `&&`.

### 10.3 Tool calls equivalentes (camada lógica)

```yaml
tools_consumidas:
  - get_ad_account_info       # detecta atribuição padrão da conta
  - list_campaigns            # listagem em modo conta completa
  - get_campaign              # detalhes de uma campanha
  - list_adsets               # conjuntos de uma campanha
  - get_adset                 # detalhes de um conjunto
  - list_ads                  # anúncios de um conjunto
  - get_ad                    # detalhes de um anúncio
  - get_insights              # insights em qualquer nível, com janela e atribuição
```

A skill nunca chama tools de **edição** (pause, update, duplicate, create). Essas são exclusivas de `/trafego-criar-campanha`, `/trafego-otimizar` e `/trafego-escalar`.

---

## 11. Breakdowns (split por dimensão)

A skill suporta os breakdowns abaixo da Graph API. Cada breakdown gera 1 chamada e 1 arquivo de cache separado. Detalhes completos (combinações permitidas, payload de saída, mapa output → breakdown) em **`sub-skills/breakdowns.md`**.

| Breakdown | Valor exemplo | Output que consome |
|---|---|---|
| `age` | "25-34" | análise [4] Geo & Demografia |
| `gender` | "female" | análise [4] |
| `country` | "BR" | análise [4] |
| `region` | "São Paulo" | análise [4] |
| `dma` | "Sao Paulo" | análise [4] (pouco útil no Brasil) |
| `publisher_platform` | "instagram" | análise [2] Performance, [6] Investigação |
| `platform_position` | "reels" | análise [2], [6] |
| `device_platform` | "mobile" | análise [6] |
| `impression_device` | "iphone" | análise [6] (não distingue Wi-Fi de dados móveis, ver limitação) |
| `hourly_stats_aggregated_by_advertiser_time_zone` | "20:00-20:59" | análise [5] Timing |

Combinações comuns: `age+gender`, `country+region`, `publisher_platform+platform_position`. Máximo 2 breakdowns por chamada (regra da Graph API). Para 3+, fazer chamadas separadas e cruzar no payload.

---

## 12. Funções utilitárias

Além de retornar payload bruto, a skill expõe funções de alto nível que outras skills consomem:

### 12.1 `comparar_periodos(p1, p2, metricas[])`
Compara dois períodos arbitrários e retorna diff + variação%.

Exemplo: CPM mês X vs mês Y, gasto semana atual vs anterior.

```yaml
periodo_1:
  inicio: 2026-04-01
  fim: 2026-04-30
  cpm: 18.50
  spend: 4200.00
periodo_2:
  inicio: 2026-05-01
  fim: 2026-05-31
  cpm: 21.30
  spend: 4800.00
diff:
  cpm: { delta: +2.80, variacao_pct: +15.1 }
  spend: { delta: +600.00, variacao_pct: +14.3 }
```

### 12.2 `ranking_top_n(metric, n, ordem, periodo)`
Retorna ranking dos top N por métrica num período (ROAS, CPL, CPA, CTR etc.). Aceita `desc` (melhores) ou `asc` (piores).

Exemplo: top 5 campanhas por ROAS últimos 30 dias.

```yaml
ranking:
  - posicao: 1
    campaign_id: "120203456789"
    nome: "Perpétuo - Curso X"
    roas: 5.8
    spend: 1200.00
  - posicao: 2
    ...
```

### 12.3 `funil_por_campanha(campaign_id, periodo)`
Retorna o funil completo (impressões → cliques → LP views → leads/checkouts → compras) com taxas calculadas em cada etapa, para uma campanha específica.

```yaml
funil:
  impressions: 186000
  link_clicks: 3348           ; ctr: 1.8%
  lp_views: 2578              ; connect_rate: 77% (lp_views/cliques)
  leads: 51                   ; opt_in: 2.0%
  initiate_checkout: 89       ; offer_rate: 3.4%
  purchases: 22               ; lead_para_compra: 43% (compras/leads)
  conversao_geral: 0.66%      ; (compras/cliques)
```

### 12.4 `historico_mensal(metric, n_meses, escopo)`
Retorna série temporal mensal de uma métrica (CPA, ROAS, gasto, etc.) para os últimos N meses. Usado pelo output [7] Lifecycle & Histórico.

```yaml
historico:
  metric: cpa
  meses:
    - mes: 2025-12
      valor: 95.40
      spend: 3200.00
    - mes: 2026-01
      valor: 88.20
      spend: 3600.00
    ...
```

### 12.5 `serie_diaria(metric, object_id, janela)`
Retorna valores dia a dia de uma métrica para um objeto (campanha, adset ou ad) em uma janela. Permite calcular variação diária, consistência temporal e coeficiente de variação.

```yaml
serie_diaria:
  metric: cpa
  object_id: "120203456789"
  janela: "7d"
  dias:
    - data: "2026-05-25"
      valor: 42.00
    - data: "2026-05-26"
      valor: 68.00
    - data: "2026-05-27"
      valor: 35.00
    - data: "2026-05-28"
      valor: 51.00
    - data: "2026-05-29"
      valor: 44.00
    - data: "2026-05-30"
      valor: 39.00
    - data: "2026-05-31"
      valor: 59.00
  media: 48.29
  desvio_padrao: 11.63
  coeficiente_variacao: 0.241
  dias_com_dado: 7
  dias_sem_conversao: 0
```

**Implementação, por modo:**
- **`APP`:** chamada Graph API em `/{object_id}/insights` com `time_increment=1` no período da janela (`time_range` codificado, seção 10.2.1).
- **`MCP_CONECTOR`:** `ads_get_ad_entities` no `level` da entidade (`campaign`, `adset` ou `ad`), com `time_increment: "1"`, o período em `date_preset` ou em `time_range` como texto JSON, o filtro pelo id da entidade (ou `impressions` maior que zero) e os campos da tradução da seção 10.1 (`amount_spent`, `impressions`, `link_click`, `omni_purchase` ou `results`). Agregar por `date_start`. Nunca usar `ads_insights_performance_trend` para campanha (volta vazio). Frequência por dia: conferir `frequency` com `ads_get_field_context`; se não vier, calcular `impressions ÷ reach` da mesma janela e declarar que foi calculada.

Cacheada normalmente (memória + arquivo). Quando a janela tem menos de 3 dias, retorna a série mas marca `coeficiente_variacao: null` (amostra insuficiente para variação significativa).

**Campo `_cv` no output principal:** quando a `serie_diaria` estiver disponível para uma métrica (janela >= 3d), o campo `{metrica}_cv` é calculado automaticamente e inserido no bloco `metricas_por_janela`. Fórmula: `desvio_padrao / media`. Quanto mais alto, mais instável o resultado.

### 12.6 Quem usa
- `comparar_periodos`: outputs [1], [5], [7] da análise
- `ranking_top_n`: output [2] (best/worst) e `/trafego-otimizar` (atalho `aumentar_top_n`)
- `funil_por_campanha`: output [2]
- `historico_mensal`: output [7]
- `serie_diaria`: `/trafego-diagnostico` (score de confiança, falso vencedor), output [5] da análise (timing), `/trafego-otimizar` (refinamento de tendência)

Estas funções consultam o cache antes de chamar a Graph API, igual ao restante da skill.

---

## 13. Princípios que a skill nunca viola

1. **Janela de atribuição declarada em todo output.** Sem isso, número não tem significado.
2. **Métricas derivadas sempre calculadas.** Fazem parte do payload obrigatório, não são opcionais.
3. **Sempre puxar 3 janelas da trilha** quando o tipo de funil e ticket são conhecidos. Sem isso, diagnóstico de tendência das outras skills cai pela metade.
4. **Não tomar decisão.** Apenas entregar dado bem formatado. Diagnóstico operacional é responsabilidade de `/trafego-otimizar`. Diagnóstico estratégico é de `/trafego-diagnostico`. Crescimento é de `/trafego-escalar`.
5. **Cache invalida em qualquer edição.** Dados pós-ação devem ser frescos, sempre.
6. **Falha parcial não quebra relatório** em modo conta completa. Uma campanha problemática não pode esconder as outras 13.
7. **Denominador zero retorna `null`, não erro.** Outras skills sabem interpretar.
8. **Sempre declarar `confiabilidade`** das métricas derivadas. Protege contra decisão sobre dado imaturo.
9. **Não chamar tools de edição.** Leitura é leitura. Edição mora em outras skills.
10. **Bypass de cache é explícito.** Gestor pede, ou edição prévia disparou invalidação. Nunca implícito.
