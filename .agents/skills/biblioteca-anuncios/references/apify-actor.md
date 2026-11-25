# Apify Actor para Biblioteca de Anúncios (referência)

> Documentação dos actors disponíveis para investigar a Biblioteca de Anúncios da Meta via Apify, sem depender do Claude in Chrome.

---

## Quando usar Apify vs Claude in Chrome

| Aspecto | Apify | Claude in Chrome |
|---|---|---|
| Pré-requisito | `APIFY_API_TOKEN` no `.env` | Claude in Chrome instalado |
| Velocidade | 2 a 5 minutos | 20 a 25 minutos |
| Cliques de permissão | Zero | ~28 (modo completo) |
| Custo | $0.75 a $3.40 por 1000 ads | Gratuito |
| Confiabilidade | Alta (API estável) | Média (pop-ups falham) |
| Identificação de escala | Campo nativo `collationCount` | Regex em texto da página |

**Recomendação:** Apify como opção principal. Claude in Chrome como fallback para quem não tem token ou prefere zero custo.

---

## Actors disponíveis (ordem de preferência)

### 1. `curious_coder/facebook-ads-library-scraper` (recomendado por preço)

- **ID do actor:** `curious_coder~facebook-ads-library-scraper` (formato API) ou `XtaWFhbtfxyzqrFmd` (legacy)
- **Preço:** $0.75 por 1000 ads
- **Output do campo de escala:** `Collation Count` (número de ads com o mesmo criativo) + `Collation ID` (id de agrupamento)
- **Vantagem:** mais barato, output bem estruturado
- **Limitação:** rate limit menor que o oficial

### 2. `apify/facebook-ads-scraper` (alternativa oficial)

- **ID do actor:** `apify~facebook-ads-scraper` ou `JJghSZmShuco4j9gJ`
- **Preço:** $3.40 por 1000 ads
- **Output do campo de escala:** `collationCount` (camelCase, sem espaço)
- **Vantagem:** mantido pelo time Apify, mais confiável a longo prazo
- **Limitação:** 4x mais caro

A skill `/biblioteca-anuncios` usa **curious_coder por default** e expõe a alternativa oficial como opção avançada.

---

## Schema de input do actor

Os 2 actors aceitam input similar. Padrão usado pela skill:

```json
{
  "urls": [
    {
      "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q=Erico%20Rocha&search_type=keyword_unordered&media_type=all"
    }
  ],
  "count": 100,
  "scrapeAdDetails": true,
  "scrapePageAds.activeStatus": "all"
}
```

Campos importantes:
- `urls`: lista de URLs da Biblioteca de Anúncios. UMA URL por concorrente/mercado.
- `count`: máximo de ads a coletar por URL. Default `100`. Para modo Rápido use `50`. Para Completo use `200`.
- `scrapeAdDetails`: `true` para coletar detalhes (incluindo `Collation Count`).
- `proxy`: usar proxy residencial Apify (default ativado, evita bloqueio do Facebook).

A skill monta a URL da Biblioteca conforme o formato:

```
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={CODIGO_PAIS}&q={NOME_URL_ENCODED}&search_type=keyword_unordered&media_type=all&sort_data[mode]=total_impressions&sort_data[direction]=desc
```

Códigos válidos: `BR`, `US`, `MX`, `AR`, `CO`, `ES`.

---

## Output esperado (por anúncio)

Cada item do dataset retornado pelo actor tem essa estrutura simplificada:

```json
{
  "adArchiveID": "1234567890",
  "pageName": "Erico Rocha",
  "pageID": "9876543210",
  "startDate": "2026-04-01",
  "endDate": null,
  "isActive": true,
  "publisherPlatform": ["facebook", "instagram"],
  "collationCount": 12,
  "collationID": "abcdef123",
  "snapshot": {
    "body": {
      "text": "Texto principal do anúncio aqui..."
    },
    "title": "Título do anúncio",
    "callToActionType": "LEARN_MORE",
    "linkUrl": "https://...",
    "images": [...],
    "videos": [...]
  },
  "currency": "BRL",
  "spend": {"lower_bound": null, "upper_bound": null}
}
```

Os campos que a skill usa:

| Campo | Uso |
|---|---|
| `collationCount` | número que define escala. Se `>= criterio_escala`, inclui no relatório |
| `collationID` | agrupa ads com mesmo criativo. A skill exibe só 1 ad por collationID |
| `adArchiveID` | usado para gerar o link "Ver anúncio" no HTML |
| `pageName` | nome do anunciante (deve bater com o concorrente buscado) |
| `snapshot.body.text` | texto/copy do anúncio. Skill mostra como hook no card |
| `snapshot.title` | título (se houver). Skill mostra junto da hook |
| `snapshot.callToActionType` | CTA usado. Skill mostra como meta info |
| `startDate` | data de início. Skill mostra como meta info |
| `isActive` | filtra apenas ativos |

---

## URL pública do anúncio (para link "Ver anúncio")

Padrão Meta:

```
https://www.facebook.com/ads/library/?id={adArchiveID}
```

Skill usa esse padrão para popular o link no card do HTML.

---

## Processo de chamada da API (executado pelo script Python)

1. **Start a run** do actor:
   ```
   POST https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_API_TOKEN}
   Body: {input JSON conforme schema acima}
   ```
2. **Aguardar run terminar** (polling no endpoint `/runs/{runId}` até `status == "SUCCEEDED"`).
3. **Buscar dataset** com os resultados:
   ```
   GET https://api.apify.com/v2/datasets/{defaultDatasetId}/items?token={APIFY_API_TOKEN}&format=json
   ```
4. **Parse JSON** e filtrar por `collationCount >= criterio_escala`.
5. **Deduplicar por `collationID`** (1 entrada por grupo de criativos idênticos).

Tudo isso é feito pelo script `scripts/buscar-apify.py` da skill, que recebe os parâmetros via CLI e retorna JSON pronto pra stdout.

---

## Tempo estimado de execução

| Modo | Concorrentes × Mercados | Tempo Apify | Custo aproximado |
|---|---|---|---|
| Rápido | 3 × 1 = 3 buscas | ~2 min | ~$0.10 |
| Padrão | 8 × 2 = 16 buscas | ~5 min | ~$0.50 |
| Completo | 14 × 6 = 84 buscas | ~12 min | ~$3.00 |

**Importante:** o cálculo de custo assume ~100 ads coletados por busca. Concorrentes com volume gigante (Hormozi, Erico Rocha) podem retornar mais e custar um pouco mais.

A skill avisa o aluno do custo aproximado antes de executar.

---

## Fallback se Apify falhar

Se o actor retornar erro (rate limit, token inválido, conta sem crédito):

1. A skill mostra o erro pro aluno.
2. Pergunta se quer:
   - Tentar de novo (retry imediato)
   - Trocar pra Claude in Chrome (fallback gratuito)
   - Cancelar

O fluxo Claude in Chrome continua disponível como Passo 7.B na SKILL.md.

---

## Variável de ambiente

```bash
# .env (raiz do projeto)
APIFY_API_TOKEN=apify_api_***TOKEN_MASCARADO***
```

A skill `configurar-apify` (que já existe no projeto) guia o aluno na criação do token caso ainda não tenha. A skill `/biblioteca-anuncios` chama `/configurar-apify` automaticamente se a variável estiver ausente.
