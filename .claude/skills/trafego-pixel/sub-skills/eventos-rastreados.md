# Sub-fluxo. Eventos Rastreados

Drill-down em um pixel específico. Lista todos os eventos disparados nos últimos 7 dias com contagem, frequência e deduplicate rate.

## Perguntas que cobre

- "Quais eventos o pixel está rastreando?"
- "PageView, Purchase, Lead estão chegando?"
- "Tem evento custom no meu pixel?"
- "Meu CAPI está enviando direito?"
- "Qual a frequência de disparo de cada evento?"

## Dados necessários

> **Roteamento por modo (ver SKILL.md, Passo 0):** os GET abaixo são o caminho `APP` (curl, `v25.0`, token mascarado na tela). No `MCP_CONECTOR`: `/{pixel_id}` → `ads_get_dataset_details`; `/stats event_total_counts` → `ads_get_dataset_stats`; `/stats event_match_quality` → `ads_get_dataset_quality`. Leitura pura, sem lacuna.
>
> **Reforço opcional no MCP (seção 2.0 do SKILL.md):** `ads_pixel_event_read` mostra os eventos configurados no pixel (separa "configurado e parado" de "nem configurado") e `ads_pixel_parameter_read` mostra os parâmetros configurados (ex.: `value` e `currency` na compra). Só leitura: nunca usar as tools de criar, editar ou apagar evento.

```
GET /{pixel_id}?fields=id,name,last_fired_time,is_unavailable,can_proxy
GET /{pixel_id}/stats?aggregation=event_total_counts&start_time={now-7d}&end_time={now}
GET /{pixel_id}/stats?aggregation=event_match_quality&start_time={now-7d}&end_time={now}
GET /{pixel_id}/stats?aggregation=event_total_counts&start_time={now-14d}&end_time={now-7d}   # janela anterior, para comparação
```

A primeira chamada confirma os metadados. **A segunda é a fonte canônica de "Total 7d" por evento** (formato `data: [{ event, value }]` direto). A terceira traz a qualidade de correspondência (EMQ), se disponível. A quarta puxa a janela anterior (D-14 a D-7) para detectar quedas: usar `event_total_counts` também aqui, não série temporal.

> **Atenção:** NÃO usar `aggregation=event` para somar totais. Esse formato é série temporal e não retorna o campo `value` no formato que a leitura espera. Ver as seções 2.1 e 2.2 do SKILL.md (erro conhecido de contagem zerada).

Se o aluno pedir gráfico temporal explicitamente (ex: "mostra a curva de Purchase no dia"), aí sim chamar `aggregation=event` como complemento. Mas nunca como fonte de totais.

## O que entregar

### Bloco 1. Header do pixel
```
📡 Pixel "{nome}" ({id})
Último disparo: há 12 minutos
Status geral: 🟢 Ativo
Janela analisada: últimos 7 dias
```

### Bloco 2. Eventos padrão (sempre na ordem)
```
EVENTOS PADRÃO

| Evento               | Total 7d | Por dia (média) | Último disparo | Saúde |
|----------------------|----------|-----------------|----------------|-------|
| PageView             | 14.230   | 2.033           | há 12 min      | 🟢    |
| ViewContent          | 3.180    | 454             | há 14 min      | 🟢    |
| AddToCart            | 420      | 60              | há 1h          | 🟢    |
| InitiateCheckout     | 210      | 30              | há 2h          | 🟢    |
| Purchase             | 48       | 6.8             | há 3h          | 🟢    |
| Lead                 | 0        | 0               | nunca          | ⚪    |
| CompleteRegistration | 0        | 0               | nunca          | ⚪    |
| Subscribe            | 0        | 0               | nunca          | ⚪    |
```

**Saúde do evento:**
| Estado | Critério |
|---|---|
| 🟢 | Disparou nas últimas 24h e contagem > 0 |
| 🟡 | Disparou nos últimos 7d mas há > 24h, ou queda > 50% vs janela anterior |
| 🔴 | Não disparou nos últimos 7d **e** o evento é esperado para o tipo de conta |
| ⚪ | Não disparou e não é esperado |

"Esperado para o tipo de conta": determinado pelo tipo de funil (Passo 0.1 do SKILL.md, lido do resumo do produto ativo ou perguntado). Conta de venda direta espera `Purchase`. Conta de captação espera `Lead`.

### Bloco 3. Eventos custom
```
EVENTOS CUSTOM

| Evento               | Total 7d | Por dia | Último disparo |
|----------------------|----------|---------|----------------|
| ClickWhatsApp        | 180      | 25.7    | há 22 min      |
| Watch50pctVSL        | 92       | 13.1    | há 1h          |
| ClickButtonOferta    | 48       | 6.8     | há 4h          |
```

Quando não há eventos custom, exibir: `Nenhum evento custom configurado.`

### Bloco 4. Taxa de deduplicação (CAPI)
Quando disponível:
```
🔁 TAXA DE DEDUPLICAÇÃO (CAPI vs navegador)

Total recebido: 22.418 eventos
Deduplicados:  16.180 (72%)

Status: 🟢 Saudável (faixa 60% a 90%)
```

Faixas:
| Range | Status | Diagnóstico |
|---|---|---|
| 60% a 90% | 🟢 Saudável | CAPI + browser pareando bem |
| 30% a 59% | 🟡 Atenção | CAPI cobre menos eventos do que deveria, ou chaves de match incompletas |
| < 30% | 🔴 CAPI quase inativo | CAPI não está enviando, ou está enviando sem `event_id` ou chaves de match (email, phone, click_id) |
| > 95% | 🟡 Suspeito | Pixel browser bloqueado pelo navegador (Safari ITP, ad block) |

Quando não disponível, exibir: `Taxa de deduplicação não disponível (CAPI não detectada ou a leitura não retornou o dado).`

### Bloco 5. Sinais críticos consolidados
```
⚠️ SINAIS CRÍTICOS

1. 🔴 Lead = 0 nos últimos 7d.
   Esperado para conta de venda direta? Não.
   Esperado para conta de captação? Sim. Investigar a página de captura.

2. 🟡 Purchase caiu 38% vs semana anterior (78 → 48).
   Causas possíveis: queda de tráfego, fluxo de checkout quebrado, evento de compra deixando de disparar.
   Próximo passo: cruzar com /trafego-analise [8] (Problemas Ocultos).
```

## Detecção de anomalias

Comparar contagem de cada evento com janela anterior (7d a 14d atrás):

| Variação | Sinal |
|---|---|
| Queda > 50% | 🔴 Crítico |
| Queda 20% a 50% | 🟡 Atenção |
| Variação < 20% | 🟢 Estável |
| Aumento > 100% | 🟢 Crescimento (não é problema) |

## Handoffs

| Achado | Para onde |
|---|---|
| `Purchase` zerado em conta de venda direta | Conferir no Gerenciador de Eventos se o checkout dispara `Purchase` (e a integração da CAPI na plataforma, ex: Hotmart ou Kiwify); `/pagina-checkout` para revisar a ligação da página com o checkout |
| `Lead` zerado em conta de captação | `/pagina-pixel` (reinstalar o pixel na página de captura) + conferência manual do formulário |
| Taxa de deduplicação < 30% | Investigação manual no Gerenciador de Eventos (chaves de correspondência do lado do servidor) |
| Evento personalizado que deve virar público | `/trafego-publicos` (opção de evento personalizado) |
| Queda > 50% em evento padrão | `/trafego-analise` [8] (Problemas Ocultos) para correlacionar com campanhas |

## Cache

Salvar o resultado em `meus-produtos/_global/trafego/pixel/eventos-{pixel_id}-{YYYY-MM-DD}-{hh}.md` com validade de 1h. Nunca gravar token no cache.
