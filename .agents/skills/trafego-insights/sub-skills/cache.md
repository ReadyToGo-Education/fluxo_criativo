# Cache Local de Insights em Arquivo .md

Esta sub-skill define o sistema de cache em arquivo do `/trafego-insights`, complementar ao cache em memória de 5 minutos. Serve para evitar requisições redundantes à Graph API quando várias skills (analise, otimizar, escalar, regras, publicos, testes) precisam dos mesmos dados no mesmo período dentro da mesma sessão ou entre sessões próximas.

---

## 1. Por que cache em arquivo

O cache em memória da seção 7 do SKILL.md vive apenas dentro de uma chamada da skill. Se o aluno roda `/trafego-analise` e depois Gerenciador (Regras automáticas) segundos depois, ambos pedem os mesmos dados de período. Sem cache de arquivo, são duas requisições à Graph API. Com cache de arquivo, a segunda lê do disco.

---

## 2. Localização

```
meus-produtos/{ativo}/trafego/insights/
├── INDEX.md                    # índice navegável de todos os caches
├── conta-completa-2026-04-21_2026-05-04-base.md
├── conta-completa-2026-04-21_2026-05-04-age_gender.md
├── campanha-12345-2026-04-28_2026-05-04-platform_position.md
└── ...
```

Se o aluno não tem produto ativo, usar `meus-produtos/_global/trafego/insights/`.

---

## 3. Convenção de nome de arquivo

```
{escopo}-{periodo}-{breakdowns_hash}.md
```

Exemplos:
- `conta-completa-2026-04-21_2026-05-04-base.md` (escopo conta, período 14d, sem breakdown)
- `campanha-120203456789-2026-04-28_2026-05-04-age_gender.md` (campanha específica com breakdown demo)
- `adset-120203456789001-2026-05-01_2026-05-04-platform_position.md` (adset com breakdown posicionamento)

**Componentes:**
- `escopo`: `conta-completa` | `campanha-{id}` | `adset-{id}` | `ad-{id}`
- `periodo`: `{data_inicio}_{data_fim}` em ISO `YYYY-MM-DD`
- `breakdowns_hash`: lista alfabética de breakdowns separados por `_`, ou `base` se nenhum

**Hash dos breakdowns:**
- Sem breakdown → `base`
- `["age", "gender"]` → `age_gender`
- `["country", "region", "dma"]` → `country_dma_region` (ordem alfabética)

---

## 4. Schema do arquivo .md

```markdown
---
escopo: conta-completa | campanha | adset | ad
object_id: 120203456789                       # null se conta-completa
periodo:
  inicio: 2026-04-21
  fim: 2026-05-04
  rotulo: "14d"                                # opcional, ajuda leitura humana
breakdowns: [age, gender]                     # vazio se base
janela_atribuicao: 7d_click
ad_account_id: act_1234567890
moeda: BRL
timestamp_leitura: 2026-05-04T14:30:00-03:00
ttl_segundos: 21600                           # 6h para janela 7-14d
status: fresh                                  # fresh | stale | expired
hash_filtros: a3f1c8                          # hash dos filtros para invalidação seletiva
---

# Cache: {escopo} {periodo}

Resumo human-readable em 2 a 3 linhas para facilitar inspeção do arquivo.

## Payload

\`\`\`json
{
  "campanha": { ... },
  "conjuntos": [ ... ],
  "anuncios": [ ... ],
  "erros": []
}
\`\`\`
```

O bloco `## Payload` contém o output completo do `/trafego-insights` em JSON, idêntico ao schema da seção 9 do SKILL.md.

---

## 5. TTL (time-to-live)

| Janela do período | TTL padrão |
|---|---|
| `today` (período inclui hoje) | 1 hora |
| `7d`, `14d` (terminam hoje) | 6 horas |
| `30d` (terminam hoje) | 24 horas |
| Período histórico fechado (não inclui hoje) | 7 dias |

Após o TTL, marcar status como `expired` e tratar como cache miss. Não deletar — apenas ignorar. (Histórico fica útil para auditoria.)

---

## 6. Invalidação

### 6.1 Invalidação automática por edição
Quando QUALQUER skill executa edição na conta Meta Ads (pausar, ajustar budget, criar campanha, criar regra, criar audience, criar adset de teste), todos os caches dessa `ad_account_id` são marcados como `stale` (sufixo no nome: `*.stale.md`).

Skills que disparam invalidação:
- `/trafego-otimizar` (pausa, ajuste de budget)
- `/trafego-escalar` (aumento de budget, duplicação)
- `/trafego-criar-campanha` (criação de campanha)
- Gerenciador (Regras automáticas) (criação ou ativação de regra)
- Gerenciador de Audiences (criação de audience — não muda métricas existentes mas pode invalidar lookalike sources)
- Duplicar entidade no Gerenciador (variando 1 dimensão) (criação de adset/ad de teste)

### 6.2 Invalidação manual
- Aluno pede explicitamente "atualizar dados" ou "puxar de novo": deletar arquivo `*.stale.md` correspondente.
- Flag `--refresh` na chamada: força refresh ignorando cache (não deleta, sobrescreve).

### 6.3 Limpeza periódica
Sugestão: hook ou comando manual que limpa arquivos com mais de 30 dias na pasta `trafego/insights/`.

---

## 7. Algoritmo de leitura (pseudo-código)

```
def ler_insights(escopo, periodo, breakdowns, force_refresh=False):
    nome_arquivo = montar_nome(escopo, periodo, breakdowns)
    caminho = f"meus-produtos/{ativo}/trafego/insights/{nome_arquivo}"

    if not force_refresh and arquivo_existe(caminho):
        cache = ler_md(caminho)
        if cache.status == "fresh" and not expirou(cache.timestamp, cache.ttl_segundos):
            return cache.payload  # CACHE HIT

    # CACHE MISS ou stale ou refresh forçado
    payload = chamar_graph_api(escopo, periodo, breakdowns)
    salvar_md(caminho, payload, escopo, periodo, breakdowns)
    atualizar_index()
    return payload
```

---

## 8. INDEX.md (índice de caches)

Arquivo opcional mas recomendado para inspeção humana. Listagem cronológica:

```markdown
# Cache Index — Tráfego Insights

Última atualização: 2026-05-04 14:35

| Quando | Escopo | Período | Breakdowns | Status | Arquivo |
|---|---|---|---|---|---|
| 2026-05-04 14:30 | conta-completa | 14d | base | 🟢 fresh | conta-completa-2026-04-21_2026-05-04-base.md |
| 2026-05-04 14:28 | campanha 12345 | 7d | age,gender | 🟢 fresh | campanha-12345-2026-04-28_2026-05-04-age_gender.md |
| 2026-05-04 09:15 | conta-completa | today | base | 🟠 expired | conta-completa-2026-05-04_2026-05-04-base.md |
| 2026-05-03 16:42 | adset 67890 | 30d | platform_position | 🔴 stale | adset-67890-2026-04-04_2026-05-03-platform_position.md.stale |
```

Atualizar o INDEX a cada novo cache salvo, marcação de stale ou refresh.

---

## 9. Quem lê o cache

Toda skill de tráfego que precisa de métrica deve passar por `/trafego-insights`, que internamente checa o cache antes de chamar a API:

| Skill | Como usa |
|---|---|
| `/trafego-analise` | Lê para narrar os 9 outputs |
| `/trafego-otimizar` | Lê para diagnóstico em 2 camadas. Após edição, invalida. |
| `/trafego-escalar` | Lê para validar gatilhos. Após escalar, invalida. |
| Gerenciador (Regras automáticas) | Lê para construir condições baseadas em valores atuais (ex: "CPA atual"). Após criar regra ativa, invalida. |
| Gerenciador de Audiences | Lê para identificar audiences source mais valiosas (ex: lookalike de quem). Após criar audience, invalida. |
| Gerenciador de Eventos | Não usa cache de insights (usa endpoint próprio do pixel) |
| Duplicar entidade no Gerenciador (variando 1 dimensão) | Lê para identificar best-performer a duplicar. Após criar teste, invalida. |

---

## 10. Princípios

1. **Cache transparente.** Aluno nunca precisa saber que existe. Ele pede dado, recebe dado.
2. **Invalidação rigorosa.** Se houve edição, dados antigos viraram fonte de erro. Marcar como stale imediatamente.
3. **Diretório por produto ativo.** Mistura entre produtos é proibida. Cada produto tem seu cache.
4. **Histórico preservado.** Caches expirados não são deletados, ficam para auditoria. Apenas ignorados na leitura.
5. **Uma chamada por arquivo.** Não tentar agregar múltiplos períodos no mesmo arquivo. Cada combinação de filtros = um arquivo.
