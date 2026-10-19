# Sub-fluxo. Pixels Sem Atividade

Destaque exclusivo de pixels da conta sem disparo nos últimos 7 dias. É o output que o aluno acessa quando suspeita que algum pixel está com problema mas não sabe qual.

## Perguntas que cobre

- "Tem algum pixel sem atividade nos últimos 7 dias?"
- "Quais pixels estão silenciosos?"
- "Tem pixel obsoleto que eu deveria limpar?"
- "Por que meu público de remarketing está secando?"

## Dados necessários

> **Roteamento por modo (ver SKILL.md, Passo 0):** os GET abaixo são o caminho `APP` (curl, `v25.0`, token mascarado na tela). No `MCP_CONECTOR`: `adspixels` → `ads_get_datasets`; `/stats event_total_counts` → `ads_get_dataset_stats`; o cruzamento com públicos (Bloco 4) usa `ads_get_ad_account_custom_audiences`. Leitura pura, sem lacuna.

```
GET /act_{ad_account_id}/adspixels?fields=id,name,last_fired_time,is_unavailable,creation_time
```

Para cada pixel com `last_fired_time` ausente ou > 7d, complementar com:

```
GET /{pixel_id}/stats?aggregation=event_total_counts&start_time={now-30d}&end_time={now}
```

Janela de 30d permite distinguir entre "pixel novo nunca disparou" e "pixel ativo que parou de disparar".

> **Importante:** sempre `aggregation=event_total_counts`. Se a leitura retornar 0 mas o `last_fired_time` for recente (menos de 24h), **não classificar como sem atividade**: é sinal de leitura no formato errado. Refazer com `event_total_counts`. Ver a seção 2.2 do SKILL.md.

### Checagem extra automática

Depois do Bloco 4 (cruzamento com públicos), executar a "Checagem extra: pixel usado pelas campanhas" descrita em SKILL.md seção 1.4. Pixel sem atividade que está sendo usado por uma campanha ativa é o sinal mais grave possível e merece destaque imediato.

## Critério

Um pixel entra nesta lista se **qualquer** das condições for verdadeira:

- `last_fired_time` é `null`
- `last_fired_time` > 7 dias atrás
- `is_unavailable: true`

## O que entregar

### Bloco 1. Resumo
```
🔴 PIXELS SEM ATIVIDADE (últimos 7 dias)

Total: 2 de 4 pixels da conta
```

Quando todos estão ativos, exibir: `🟢 Todos os pixels da conta dispararam nos últimos 7 dias.`

### Bloco 2. Tabela detalhada
```
| Pixel              | Último disparo | Criado em   | Eventos 30d | Diagnóstico       |
|--------------------|----------------|-------------|-------------|-------------------|
| Pixel Antigo (BR)  | há 9 dias      | 2024-08-12  | 1.205       | parou recentemente|
| Pixel Teste        | nunca          | 2025-11-03  | 0           | nunca instalado   |
```

### Bloco 3. Diagnóstico por pixel

Para cada pixel sem atividade, classificar em uma das categorias:

| Categoria | Critério | Causa provável | Ação |
|---|---|---|---|
| **Nunca instalado** | `last_fired_time = null` E `eventos 30d = 0` | O código do pixel não foi colocado na página | `/pagina-pixel` para instalar (página HTML) ou configurar na plataforma da página |
| **Parou recentemente** | Disparou nos últimos 30d mas não nos 7d | Página mudou, código removido, redirecionamento novo | Conferir a página e reinstalar o código se necessário (`/pagina-pixel`) |
| **Obsoleto** | Último disparo há mais de 60 dias | Site antigo, projeto encerrado | Considerar arquivar no Gerenciador de Negócios |
| **Desativado** | `is_unavailable: true` | Pixel desativado no Gerenciador de Negócios | Reativar ou usar outro pixel |
| **Pixel duplicado** | Mais de 1 pixel ativo na conta com nome similar | Aluno criou novo sem desativar o velho | Limpeza manual |

### Bloco 4. Cruzamento com públicos

Se o aluno tem públicos personalizados alimentados pelo pixel inativo, sinalizar:

```
🔗 IMPACTO EM PÚBLICOS

O pixel "Pixel Antigo (BR)" alimenta os seguintes públicos personalizados:

- Visitantes 30d (atual: 8.500, leitura anterior: 14.000, queda 39%)
- Carrinho abandonado (atual: 320, leitura anterior: 480, queda 33%)
- Compradores (atual: 180, leitura anterior: 175, estável)

Sem disparo do pixel, esses públicos vão continuar encolhendo.
Toda campanha de remarketing que depende delas perde alcance progressivamente.
```

A skill lê os públicos (`APP`: `/act_{ad_account_id}/customaudiences?fields=id,name,subtype,rule,operation_status,approximate_count_lower_bound`; `MCP_CONECTOR`: `ads_get_ad_account_custom_audiences`) e cruza com o pixel. A comparação de tamanho só aparece quando houver uma leitura anterior salva no cache (`meus-produtos/_global/trafego/pixel/`); a API não guarda o histórico de tamanho, então, sem leitura anterior, mostrar só o tamanho atual. Nunca inventar o número antigo.

## Handoffs

| Achado | Para onde |
|---|---|
| Nunca instalado | `/pagina-pixel` (instalar) |
| Parou recentemente | Conferir a página; depois `/pagina-pixel` se o código foi mesmo removido |
| Obsoleto | Limpeza manual no Gerenciador de Negócios |
| Públicos secando junto | `/trafego-publicos` (recriar o público) **depois** de resolver o pixel; senão o público novo também esvazia |
| Vários pixels duplicados | Decisão manual de qual manter; depois `/pagina-pixel` para apontar a página para o pixel definitivo |

## Cache

Salvar o resultado em `meus-produtos/_global/trafego/pixel/sem-atividade-{YYYY-MM-DD}-{hh}.md` com validade de 1h. Nunca gravar token no cache.
