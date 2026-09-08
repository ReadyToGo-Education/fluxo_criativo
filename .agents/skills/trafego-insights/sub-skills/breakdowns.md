# Breakdowns Suportados pelo /trafego-insights

Esta sub-skill mapeia os breakdowns disponíveis na Graph API que o `/trafego-insights` puxa, qual output da `/trafego-analise` (ou outra skill) consome cada um, e exemplos de chamada.

---

## 1. Tabela mestre

| Breakdown (param Graph API) | Valor exemplo | Output que consome | Limitação |
|---|---|---|---|
| `age` | "25-34" | analise [4] Geo & Demografia | Combinável com `gender` |
| `gender` | "female" \| "male" \| "unknown" | analise [4] Geo & Demografia | Combinável com `age` |
| `country` | "BR" | analise [4] Geo (capital vs interior parcial) | Top-level |
| `region` | "São Paulo" | analise [4] Geo (estado) | Combinável com `country` |
| `dma` | "Sao Paulo" (Designated Market Area) | analise [4] Geo (capital vs interior fino) | Apenas para mercados com DMA mapeado |
| `publisher_platform` | "facebook" \| "instagram" \| "audience_network" \| "messenger" | analise [2] Performance, [6] Investigação | — |
| `platform_position` | "feed" \| "story" \| "reels" \| "marketplace" \| "instream_video" | analise [2], [6] | Combinável com `publisher_platform` |
| `device_platform` | "mobile" \| "desktop" | analise [6] Investigação | — |
| `impression_device` | "iphone" \| "android_smartphone" \| "desktop" \| "tablet" | analise [6] Investigação | NÃO distingue Wi-Fi vs dados móveis. Marcar como limitação. |
| `hourly_stats_aggregated_by_advertiser_time_zone` | "00:00:00 - 00:59:59" | analise [5] Timing (horário) | Combinável com data range |

---

## 2. Combinações permitidas

A Graph API aceita até 2 breakdowns na mesma chamada (com restrições). Combinações comuns:

- `age, gender` — split demográfico completo
- `country, region` — geografia hierárquica
- `publisher_platform, platform_position` — onde aparece e em qual posição
- `age, device_platform` — quem usa cada dispositivo

**Combinações proibidas pela API:**
- `hourly_stats` + qualquer outro breakdown em ATIVO (só funciona em períodos fechados)
- 3+ breakdowns ao mesmo tempo
- `dma` + `region` (redundante)

Quando o aluno pedir uma combinação proibida, fazer 2 chamadas separadas e cruzar manualmente no payload.

---

## 3. Mapa output → breakdowns necessários

| Output da analise | Breakdowns que pede |
|---|---|
| [1] Diagnóstico Rápido | `base` (sem breakdown) — só métricas agregadas |
| [2] Performance & Funil | `publisher_platform`, `platform_position` (uma chamada cada) |
| [3] Criativos & Copy | `base` + `publisher_platform` (qual posicionamento performa cada criativo) |
| [4] Geo & Demografia | `age, gender`, `country`, `region`, `dma` (4 chamadas cacheadas) |
| [5] Timing & Sazonalidade | `hourly_stats_aggregated_by_advertiser_time_zone` + `base` por dia |
| [6] Investigação Profunda | `device_platform`, `impression_device`, `publisher_platform` (3 chamadas) |
| [7] Lifecycle & Histórico | `base` por mês x N meses |
| [8] Problemas Ocultos | `base` (filtros internos) |
| [9] Orçamento & Projeção | `base` |

---

## 4. Exemplo de chamada por breakdown

### `age, gender`
```
GET /act_<id>/insights
  ?fields=spend,impressions,clicks,actions
  &breakdowns=age,gender
  &time_range={"since":"2026-04-21","until":"2026-05-04"}
  &action_attribution_windows=["7d_click"]
```

### `publisher_platform, platform_position`
```
GET /act_<id>/insights
  ?fields=spend,impressions,clicks,ctr,actions
  &breakdowns=publisher_platform,platform_position
  &time_range={"since":"2026-04-21","until":"2026-05-04"}
```

### `hourly_stats_aggregated_by_advertiser_time_zone`
```
GET /act_<id>/insights
  ?fields=spend,impressions,clicks,actions
  &breakdowns=hourly_stats_aggregated_by_advertiser_time_zone
  &time_range={"since":"2026-04-21","until":"2026-05-04"}
```

---

## 5. Output esperado com breakdown

O payload retorna uma array, com um item por valor único do breakdown:

```yaml
campanha:
  id: "120203456789"
  nome: "Perpétuo - Curso X"
  breakdown: "age,gender"
  resultados:
    - age: "18-24"
      gender: "female"
      spend: 120.00
      impressions: 5400
      cpa: 30.00
      derivadas: { ... }
    - age: "18-24"
      gender: "male"
      spend: 80.00
      impressions: 3200
      cpa: 40.00
      derivadas: { ... }
    - age: "25-34"
      gender: "female"
      spend: 280.00
      ...
```

A skill `/trafego-analise` consome esse array e narra (ex: "mulheres 25-34 convertem por R$ 12 — 60% mais barato que a média da conta").

---

## 6. Cache integrado

Cada chamada com breakdown gera um arquivo de cache separado. Ex: o output [4] Geo & Demografia gera 4 arquivos no cache local:

```
campanha-12345-2026-04-21_2026-05-04-age_gender.md
campanha-12345-2026-04-21_2026-05-04-country.md
campanha-12345-2026-04-21_2026-05-04-region.md
campanha-12345-2026-04-21_2026-05-04-dma.md
```

Próxima vez que o aluno pedir o output [4] no mesmo período, a skill lê os 4 arquivos sem chamar API.

---

## 7. Limitações conhecidas

1. **Wi-Fi vs dados móveis:** a Meta não expõe esse breakdown via API pública. `impression_device` distingue dispositivo (iPhone, Android, desktop), mas não tipo de conexão. Quando o aluno perguntar, responder com a limitação e usar `impression_device` como proxy parcial.

2. **DMA fora dos EUA:** `dma` é menos rico no Brasil. Para split capital vs interior brasileiro, usar `region` (estados) e cruzar manualmente com lista de capitais.

3. **Breakdown + ad ativo:** alguns breakdowns só funcionam em períodos fechados (ex: `hourly_stats` em campanhas pausadas). Se a campanha está ativa hoje e o aluno pediu hoje, alertar e usar período de ontem.

4. **Tamanho do payload:** breakdown demográfico em conta com muitas campanhas pode estourar 200KB. Paginar via cursor da Graph API quando necessário.

---

## 8. Princípios

1. **Cada breakdown = 1 chamada API + 1 arquivo de cache.** Não misturar.
2. **Sempre declarar breakdown no output.** Sem isso, métricas perdem contexto.
3. **Limitação explícita.** Se a Meta não suporta o split que o aluno pediu, dizer claro e oferecer proxy.
4. **Combinação proibida vira 2 chamadas.** Cruzar no payload, não na API.
