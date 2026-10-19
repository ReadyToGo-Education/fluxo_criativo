# Sub-fluxo. Status dos Pixels

Visão geral de saúde de todos os pixels da conta. É o output mais comum quando o aluno pergunta "meu pixel está funcionando?".

## Perguntas que cobre

- "Meus pixels estão recebendo eventos?"
- "Qual foi o último disparo?"
- "Tem algum pixel com problema?"
- "Quantos pixels eu tenho na conta? Algum sobrando?"

## Dados necessários

> **Roteamento por modo (ver SKILL.md, Passo 0):** os GET abaixo são o caminho `APP` (curl, `v25.0`, token mascarado na tela). No `MCP_CONECTOR`, usar as tools: `adspixels` → `ads_get_datasets`, `/{pixel_id}` → `ads_get_dataset_details`, `/stats event_total_counts` → `ads_get_dataset_stats`. Leitura pura, sem lacuna.

```
GET /act_{ad_account_id}/adspixels?fields=id,name,last_fired_time,is_unavailable,creation_time
```

Para cada pixel retornado, complementar com:

```
GET /{pixel_id}?fields=id,name,last_fired_time,is_unavailable,can_proxy,data_use_setting,owner_business
GET /{pixel_id}/stats?aggregation=event_total_counts&start_time={now-7d}&end_time={now}
```

Total: 1 + 2N chamadas, em que N = pixels da conta. No modo APP, cada chamada é um `curl` separado (regra do CLAUDE.md).

> **Importante:** sempre `aggregation=event_total_counts`, nunca `aggregation=event` para totais. Ver as seções 2.1 e 2.2 do SKILL.md (erro conhecido de contagem zerada quando a leitura usa o formato errado).

### Checagem extra automática quando há 2+ pixels ativos

Após o Bloco 4 desta sub-skill, executar a "Checagem extra: pixel usado pelas campanhas" descrita em SKILL.md seção 1.4. É bloco final automático, não pergunta. Apenas pula em contas com 1 único pixel.

## O que entregar

### Bloco 1. Resumo
```
📡 PIXELS DA CONTA

Total: 3 pixels
🟢 Ativos:        2
🟡 Em atenção:    0
🔴 Sem atividade: 1
```

### Bloco 2. Tabela por pixel
```
| Pixel              | Status        | Último disparo  | Eventos 7d | Sinais críticos |
|--------------------|---------------|-----------------|------------|-----------------|
| Loja Principal     | 🟢 Ativo      | há 12 minutos   | 18.420     | nenhum          |
| Captura Lançamento | 🟢 Ativo      | há 2 horas      | 1.205      | nenhum          |
| Pixel Antigo (BR)  | 🔴 Sem ativ.  | há 9 dias       | 0          | desativar/limpar|
```

### Bloco 3. Drill-down rápido por pixel ativo
Para cada pixel verde, listar contagem dos 8 eventos padrão na janela:

```
🟢 Loja Principal: últimos 7 dias

PageView           14.230
ViewContent         3.180
AddToCart             420
InitiateCheckout      210
Purchase               48
Lead                    0   (esperado: conta de venda direta)
CompleteRegistration    0
Subscribe               0

Custom events: 2
- ClickWhatsApp        180
- Watch50pctVSL         92
```

### Bloco 4. Sinais críticos consolidados
Lista priorizada de problemas que apareceram:

```
⚠️ SINAIS CRÍTICOS

1. 🔴 Pixel "Pixel Antigo (BR)" sem disparo há 9 dias.
   Causa provável: código do pixel removido da página antiga ou pixel obsoleto.
   Ação: confirmar se ainda está em uso. Se não, desativar no Gerenciador de Negócios.

2. 🟡 Loja Principal: taxa de deduplicação = 22%.
   Causa provável: a CAPI não está enviando metade dos eventos, ou as chaves de correspondência (e-mail, telefone)
   estão incompletas no envio do lado do servidor.
   Ação: investigar a configuração da CAPI no Gerenciador de Eventos. Se a página foi feita no Severino, revisar a instalação com /pagina-pixel.
```

## Critério de status (recap)

| Status | Critério |
|---|---|
| 🟢 Ativo | Último disparo ≤ 24h **e** eventos > 0 nos últimos 7d |
| 🟡 Atenção | Último disparo entre 24h e 7d **ou** eventos < 50 nos 7d |
| 🔴 Sem atividade | Último disparo > 7d **ou** `last_fired_time = null` **ou** `is_unavailable: true` |

## Handoffs típicos

| Achado | Para onde |
|---|---|
| Pixel verde sem `Purchase` (em conta perpétuo) | Investigar CAPI / checkout. Verificar no Gerenciador de Eventos se o checkout dispara `Purchase` |
| Pixel sem `PageView` ou `last_fired_time = null` | `/pagina-pixel` (reinstalar o pixel na página HTML) ou configuração na plataforma da página |
| Pixel duplicado ou sem uso | Limpeza manual no Gerenciador de Negócios |
| Pixel ativo mas taxa de deduplicação < 30% | Investigação manual no Gerenciador de Eventos (não é função desta skill) |
| Públicos de remarketing secando + pixel inativo | Resolver o pixel; depois `/trafego-publicos` (recriar o público) + `/trafego-analise` [8] |

## Cache

Salvar o resultado em `meus-produtos/_global/trafego/pixel/status-{YYYY-MM-DD}-{hh}.md` com validade de 1h (o pixel é da conta, não do produto). A próxima chamada na mesma hora lê direto do arquivo. Nunca gravar token no cache.
