---
name: trafego-insights
description: >
  Base de conhecimento e fonte única de leitura de métricas Meta Ads (Facebook + Instagram).
  Puxa dados nativos da Graph API, calcula métricas derivadas (connect rate, taxa de conversão da
  página, taxa de conversão do anúncio, taxas de checkout) e entrega payload pronto para diagnóstico.
  É a base de dados que /trafego-otimizar, /trafego-escalar e /trafego-analise consomem.
  Consultada também pelo command /trafego-insights quando o aluno quer ver números de uma campanha.
  Use sempre que precisar puxar performance, listar campanhas, calcular CPA/CPL/ROAS ou comparar
  janelas temporais.
user-invocable: false
---

# Tráfego Insights. Leitura de Métricas Meta Ads

Você é a fonte única de verdade sobre dados de performance do Meta Ads. Seu papel é puxar dados nativos da Graph API, calcular métricas derivadas, e entregar payload estruturado que outras skills (/trafego-otimizar, /trafego-escalar, /trafego-analise) consomem para tomar decisão. Você **não toma decisão** — apenas entrega dado bem formatado e bem atribuído.

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
- `lead` (lead)
- `complete_registration`
- `add_to_cart`
- `initiate_checkout`
- `landing_page_view` (LP View)
- `link_click`
- `video_view`

### 4.2 Métricas-norte (decide a ação principal)
- **Perpétuo:** `cpa` = `cost_per_action_type[purchase]`.
- **Lançamento:** `cpl` = `cost_per_action_type[lead]`.

### 4.3 Métricas leading
- `ctr_link_unico` (`unique_inline_link_click_ctr`). **Métrica leading primária.** Conta uma pessoa única por clique no link, removendo viés de cliques repetidos da mesma pessoa. Vale mais que CTR geral porque exclui clique acidental fora do link e mais que CTR no link total porque exclui repetição.
- `ctr_link_total` (`inline_link_click_ctr`). Métrica complementar. Conta todos os cliques no link (com repetição da mesma pessoa). Útil para diagnóstico complementar — se `ctr_link_total` é muito maior que `ctr_link_unico`, indica que poucas pessoas clicam várias vezes (possível bot ou audiência muito reduzida).
- `hook_rate` = `video_p25_watched_actions` ÷ `impressions` (proxy para 3s. Meta deprecou alguns campos antigos de vídeo).
- `frequencia` (`frequency`).
- `cpm`.

### 4.4 Eventos brutos para cálculo de derivadas
- `link_clicks` (`inline_link_clicks`)
- `lp_views` (`actions[landing_page_view]`)
- `add_to_cart` (`actions[add_to_cart]`)
- `initiate_checkout` (`actions[initiate_checkout]`)
- `purchases` (`actions[purchase]`)
- `leads` (`actions[lead]`)

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
1. `GET /act_{id}/campaigns?fields=id,name,status,objective,daily_budget,lifetime_budget&limit=200&effective_status=%5B%22ACTIVE%22%5D`
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
      ctr_link_unico: ...
      purchases_ou_leads: ...
      cpa_ou_cpl: ...
      conversoes: ...
    classificacao_vencedor: true | false           # CTR único saudável + ≥ 50 conversões
```

**Limite de proteção a rate limit:** máximo 200 ads por execução. Acima disso, paginar com cursor.

---

## 7. Cache em duas camadas (memória + arquivo)

A skill mantém dois níveis de cache, complementares:

### 7.1 Cache em memória (curto prazo)
- Chave: hash de (`object_id`, `nivel`, `janelas`, `janela_atribuicao`, `breakdowns`).
- TTL: **5 minutos**.
- Escopo: por sessão de conversa. Não persiste entre conversas.
- Camada mais rápida, evita refetch dentro da mesma chamada.

### 7.2 Cache em arquivo .md (médio prazo, entre sessões)
- Localização: `meus-produtos/{ativo}/trafego/insights/`.
- TTL adaptativo: 1h (today), 6h (7-14d), 24h (30d), 7d (períodos fechados).
- Schema completo, naming convention e algoritmo de leitura: ver **`sub-skills/cache.md`**.
- Permite que outras skills (analise, otimizar, regras, publicos, testes) compartilhem leituras dentro da mesma sessão e entre sessões próximas, evitando bater na Graph API repetidas vezes pelo mesmo período.

### 7.3 Ordem de consulta
1. Memória → se hit válido, retorna.
2. Arquivo .md → se hit válido (não stale, não expirado), retorna e popula memória.
3. Graph API → busca, salva no arquivo .md e na memória.

### 7.4 Invalidação automática
Ambos os caches da `ad_account_id` (memória + todos os arquivos da pasta) são invalidados **imediatamente** quando:
- Qualquer skill de edição executa write (`/trafego-otimizar`, `/trafego-escalar`, `/trafego-criar-campanha`, Gerenciador (Regras automáticas), Gerenciador de Audiences, Duplicar entidade no Gerenciador (variando 1 dimensão)).
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
  budget:
    tipo: ABO | CBO
    valor_diario_brl: 200.00
  metricas_por_janela:
    curta:                                # ex: 1d
      janela: "1d"
      spend: 198.50
      impressions: 12450
      reach: 8920
      frequency: 1.4
      ctr_link_unico: 0.0118       # unique_inline_link_click_ctr — primária
      ctr_link_total: 0.0142       # inline_link_click_ctr — complementar
      hook_rate: 0.27
      cpm: 15.95
      cpa: 198.50
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
    budget_diario_brl: 100.00
    aprendizado: ATIVO | EM_APRENDIZADO | APRENDIZADO_LIMITADO
    metricas_por_janela:
      curta: { ... }
      media: { ... }
      longa: { ... }

anuncios:
  - id: "120203456789999"
    nome: "AD - Dor - Vídeo 30s"
    status: ACTIVE
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

A skill respeita a preferência de conexão definida em `META_AUTH_MODO` no `.env` (ver `/trafego-conexao`).

### 10.1 Modo `MCP_CONECTOR`
Usar as tools do MCP da Meta que o aluno adicionou como conector personalizado. Localizar tools com prefixo `mcp__*` cujo sufixo seja relacionado a Meta Ads (ex: `mcp__Meta_Ads__ads_get_ad_entities`, `mcp__Meta_Ads__ads_insights_*`, `mcp__Meta_Ads__ads_get_ad_accounts`).

Mapeamento direto:
- `list_campaigns` → `mcp__*__ads_get_ad_entities` com filtro de tipo `campaign`
- `get_insights` → `mcp__*__ads_insights_*`
- `get_ad_account_info` → `mcp__*__ads_get_ad_accounts`

### 10.2 Modo `APP`
Ler `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` do `.env`. Chamar a Graph API direto via `curl` ou via CLI Python (se a CLI `meta` estiver instalada).

Endpoint base: `https://graph.facebook.com/v25.0/`

### 10.2.1 Boas práticas obrigatórias no Modo APP

**URL encoding:** parâmetros que contêm colchetes `[]` DEVEM ser URL-encoded antes de montar a URL do curl. O bash interpreta colchetes literais como globbing e o curl falha silenciosamente (exit code 3). Sempre usar a forma encoded:
- `effective_status=['ACTIVE']` → `effective_status=%5B%22ACTIVE%22%5D`
- `time_range={"since":"..."}` → `time_range=%7B%22since%22%3A%22...%22%7D`

**Cadência entre chamadas (rate limit):** o Meta aplica limite de uso por token. Em modo conta completa, nunca encadear mais de 3 chamadas sem pausa. Aguardar 3 segundos entre cada chamada à Graph API. Em Python, usar `time.sleep(3)` antes de cada request. Se a resposta vier com `"code": 4` (rate limit), aplicar backoff: aguardar 30s antes de retentar. Máximo 2 retries.

**Paths de arquivo:** NUNCA salvar arquivos temporários em `/tmp` ou depender de variáveis de ambiente de sessões bash anteriores (`$TEMP`, `$TMPDIR`). Cada chamada bash tem sessão isolada. Salvar sempre em `meus-produtos/{ativo}/trafego/insights/` com path absoluto derivado do diretório de trabalho atual. Para arquivos intermediários de processamento, usar o mesmo diretório do produto.

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
| `age` | "25-34" | analise [4] Geo & Demografia |
| `gender` | "female" | analise [4] |
| `country` | "BR" | analise [4] |
| `region` | "São Paulo" | analise [4] |
| `dma` | "Sao Paulo" | analise [4] (capital vs interior) |
| `publisher_platform` | "instagram" | analise [2] Performance, [6] Investigação |
| `platform_position` | "reels" | analise [2], [6] |
| `device_platform` | "mobile" | analise [6] |
| `impression_device` | "iphone" | analise [6] (não distingue Wi-Fi vs móvel — ver limitação) |
| `hourly_stats_aggregated_by_advertiser_time_zone` | "20:00-20:59" | analise [5] Timing |

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
  lp_views: 2578              ; lpvr: 77%
  leads: 51                   ; opt_in: 2.0%
  initiate_checkout: 89       ; offer_rate: 3.4%
  purchases: 22               ; connect_rate: 43% (compras/leads)
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

### 12.5 Quem usa
- `comparar_periodos`: outputs [1], [5], [7] da analise
- `ranking_top_n`: output [2] (best/worst) e `/trafego-otimizar` (atalho `aumentar_top_n`)
- `funil_por_campanha`: output [2]
- `historico_mensal`: output [7]

Estas funções consultam o cache antes de chamar a Graph API, igual ao restante da skill.

---

## 13. Princípios que a skill nunca viola

1. **Janela de atribuição declarada em todo output.** Sem isso, número não tem significado.
2. **Métricas derivadas sempre calculadas.** Fazem parte do payload obrigatório, não são opcionais.
3. **Sempre puxar 3 janelas da trilha** quando o tipo de funil e ticket são conhecidos. Sem isso, diagnóstico de tendência das outras skills cai pela metade.
4. **Não tomar decisão.** Apenas entregar dado bem formatado. Diagnóstico é responsabilidade de `/trafego-otimizar`. Crescimento é de `/trafego-escalar`.
5. **Cache invalida em qualquer edição.** Dados pós-ação devem ser frescos, sempre.
6. **Falha parcial não quebra relatório** em modo conta completa. Uma campanha problemática não pode esconder as outras 13.
7. **Denominador zero retorna `null`, não erro.** Outras skills sabem interpretar.
8. **Sempre declarar `confiabilidade`** das métricas derivadas. Protege contra decisão sobre dado imaturo.
9. **Não chamar tools de edição.** Leitura é leitura. Edição mora em outras skills.
10. **Bypass de cache é explícito.** Gestor pede, ou edição prévia disparou invalidação. Nunca implícito.
