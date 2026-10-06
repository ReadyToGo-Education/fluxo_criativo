---
name: youtube-dashboard
description: >
  Configura dashboard HTML de metricas do YouTube via Apify. Coleta dados
  publicos do canal (inscritos, total de views, descricao), videos recentes
  (views, likes, comentarios, duracao, titulo, thumbnail). Todas as
  thumbnails embutidas em base64. Roda localmente na maquina do mentorado,
  sem servidor, sem GitHub, sem agendamento automatico.
user-invocable: false
---

# YouTube Dashboard. Metricas Diarias Automaticas

## Quando Usar

- Quando o aluno quiser monitorar o crescimento do proprio canal no YouTube de forma automatica, sem precisar abrir o YouTube Studio toda manha.
- Como base de dados para `/copy-roteiro` (roteiros baseados nos videos que performam melhor) e analise de padroes de titulo e thumbnail.
- Quando o aluno precisar mostrar evolucao de metricas para clientes ou parceiros.

**Nao usar para:**
- Analisar canais de concorrentes (adaptar o script passando outro canal).
- Dados avancados do YouTube Analytics (CPM, receita, retencao) — esses requerem a YouTube Data API com OAuth, fora do escopo do Apify.

## O Que Entrega

| Arquivo | Descricao |
|---|---|
| `.claude/skills/youtube-dashboard/scripts/atualizar.py` | Script Python principal (Windows, macOS, Linux) — compartilhado entre todos os produtos |
| `meus-produtos/{ativo}/entregas/youtube-dashboard/dashboard.html` | Dashboard HTML completo, abre no navegador |
| `meus-produtos/{ativo}/entregas/youtube-dashboard/imagens/` | Thumbnails dos videos (gerados pelo script) |
| `meus-produtos/{ativo}/entregas/youtube-dashboard/insights.json` | Dados estruturados sem base64 |
| `meus-produtos/{ativo}/entregas/youtube-dashboard/historico.json` | Snapshots acumulativos (inscritos, engajamento) entre execucoes |
| `meus-produtos/{ativo}/entregas/youtube-dashboard/log.txt` | Log de cada execucao com timestamp e status |

## Como Funciona

```
atualizar.py
  ├── POST Apify (streamers~youtube-scraper, sync) — videos regulares
  │     {canal_url} → ultimos 30 videos + metadados do canal embutidos
  │     avatar: aboutChannelInfo.channelAvatarUrl → base64
  ├── POST Apify (streamers~youtube-scraper, sync, opcional) — Shorts
  │     {canal_url}/shorts → ate 30 Shorts
  │     Deduplicados por id/videoId e mesclados com os videos regulares
  │     Se falhar ou estiver vazio, continua sem erro
  ├── Para cada video/Short: views, likes, comentarios, duracao, titulo, data, thumbnail → base64
  ├── Calcula metricas: engajamento = (likes + comentarios) / views * 100
  ├── Atualiza historico.json com snapshot do dia
  └── Regenera dashboard.html com dados + thumbnails embutidos como variavel JS
```

O `dashboard.html` e sempre autossuficiente. Nao depende de servidor local. Funciona abrindo direto no navegador, inclusive offline apos a primeira geracao.

## APIs Utilizadas

Ator utilizado: `streamers~youtube-scraper`.

| # | Ator Apify | URL chamada | Tipo | Parametro chave | Retorna |
|---|---|---|---|---|---|
| 1 | `streamers~youtube-scraper` | `{canal_url}` | sync, timeout 300s | `startUrls`, `maxResults: 30` | videos regulares + metadados do canal (`aboutChannelInfo.channelAvatarUrl`, `channelName`, `numberOfSubscribers` etc.) |
| 2 | `streamers~youtube-scraper` | `{canal_url}/shorts` | sync, timeout 300s, **obrigatorio=False** | `startUrls`, `maxResults: 30` | Shorts do canal (adicionados e deduplicados por `id`/`videoId`) |

Chamada 1 busca os videos regulares. Chamada 2 busca a aba `/shorts` — se falhar ou retornar vazio, o script continua sem erro. Os resultados sao mesclados e deduplicados por ID antes de normalizar. O script extrai os dados do canal percorrendo os itens da chamada 1 e priorizando o que tiver mais dados.

**Por que sync e nao async:** mesmo motivo do Instagram/TikTok. Endpoints async retornam run IDs que podem ficar inacessiveis dependendo do plano. Sync e mais simples e confiavel.

**Thumbnails do YouTube:** o script baixa thumbnails via `https://i.ytimg.com/vi/{videoId}/hqdefault.jpg` com `requests`. Se a URL vier preenchida no campo `thumbnailUrl` do Apify, usa essa. Caso contrario, monta a URL padrao com o `videoId`. Converte para base64 para funcionar em HTML local.

Custo por execucao: cerca de US$0,05-0,30 no plano gratuito Apify (varia com o numero de videos coletados).

## Compatibilidade por Sistema Operacional

Instalacao da dependencia (unica):
```
pip install requests
```

| OS | Como rodar |
|---|---|
| Windows | `python .claude/skills/youtube-dashboard/scripts/atualizar.py --abrir` |
| macOS | `python3 .claude/skills/youtube-dashboard/scripts/atualizar.py --abrir` |
| Linux | `python3 .claude/skills/youtube-dashboard/scripts/atualizar.py --abrir` |

## Configuracao Necessaria

| Chave | Onde fica | Como obter |
|---|---|---|
| `APIFY_API_TOKEN` | `.env` | console.apify.com > Settings > Integrations > Personal API token |
| `YOUTUBE_CHANNEL` | `.env` | URL do canal ou @handle (ex: `https://www.youtube.com/@meuperfil` ou `@meuperfil`) |

## Dashboard: O Que Mostra

**ESTRUTURA OBRIGATORIA — todas as secoes devem estar presentes, nesta ordem:**

1. **Cabecalho (canal):** avatar em base64 (fallback: inicial do nome), nome do canal, descricao, data de criacao, ultima atualizacao
2. **Visao Geral (KPIs):** inscritos, total de views do canal, engajamento medio (%), total de videos
3. **Evolucao ao Longo do Tempo:** tendencia de inscritos e engajamento medio entre execucoes. So aparece com 2+ snapshots em historico.json.
4. **Desempenho por Duracao:** videos agrupados por faixa (Short ate 60s, curto 1-5min, medio 5-15min, longo 15min+). Media de views, likes, engajamento.
5. **Melhores Dias para Publicar:** heatmap ou grafico de barras por dia da semana. Intensidade = views medias.
6. **Frequencia de Publicacao:** videos por semana vs views. Insight comparando semanas mais ativas.
7. **Top 3 Videos:** os 3 com mais views, com thumbnail em base64, views, likes, comentarios, duracao, taxa de engajamento e link.
8. **Analise de Titulos:** palavras mais frequentes nos videos com mais views (wordcloud ou barras). Insight sobre comprimento ideal de titulo.
9. **Tamanho do Titulo vs Views:** 3 buckets (curto, medio, longo) com views medias por faixa.
10. **Linha do Tempo (graficos):** views, likes, engajamento (%) ao longo do tempo. Canvas puro, tooltip.
11. **Barra de Filtros:** filtros por duracao e periodo (7/15/30 dias). Afeta grade de videos, Top 3 e KPIs.
12. **Todos os Videos (grade):** thumbnail em base64, views, likes, comentarios, duracao, data, titulo truncado e link.

**NUNCA omitir nenhuma dessas 12 secoes.**

## Metricas YouTube (diferente do Instagram e TikTok)

| Metrica | Campos Apify tentados (em ordem) | Observacao |
|---|---|---|
| Views | `views`, `viewCount` | Metrica principal no YouTube |
| Likes | `likes`, `likeCount` | YouTube removeu dislikeCount da API publica |
| Comentarios | `commentsCount`, `commentCount`, `comments` | |
| Duracao | `duration`, `durationSeconds` | Script converte ISO 8601 (PT1H2M3S), HH:MM:SS e segundos para int |
| Titulo | `title`, `name` | |
| Thumbnail | `thumbnailUrl`, `thumbnail`, ou montar de `videoId` | URL padrao: `i.ytimg.com/vi/{id}/hqdefault.jpg` |
| Video ID | `id`, `videoId`, ou extraido de `url` (`v=...`) | |
| Inscritos | `numberOfSubscribers`, `subscriberCount` (no item ou em `channelInfo`) | |
| Total views canal | `channelInfo.viewCount`, `channelInfo.totalViews`, `channelTotalViews` | Fallback: soma dos videos coletados |
| Engajamento YouTube | (likes + comentarios) / views * 100 | Benchmark: acima de 3% e bom |

## Fluxo

### PASSO -1. Verificar Plataforma Ativa (OBRIGATORIO — executar antes de qualquer outra coisa)

Leia `.env`. Verifique o valor de `YOUTUBE_ATIVO`.

**Cenario: `YOUTUBE_ATIVO=false` (aluno ja disse que nao tem YouTube)**

```
Voce marcou que nao tem um canal ativo no YouTube.

Quer atualizar essa preferencia?

1. Sim, tenho YouTube agora — configurar o dashboard
2. Nao, pode ignorar
```

Se escolher 1: troque `YOUTUBE_ATIVO=false` por `YOUTUBE_ATIVO=true` no `.env` e continue para o PASSO 0.
Se escolher 2: encerre sem fazer nada.

---

**Cenario: `YOUTUBE_ATIVO` nao existe no `.env` (primeira vez)**

```
Voce tem um canal ativo no YouTube que quer monitorar?

1. Sim, tenho YouTube
2. Nao tenho YouTube
```

Se escolher 1: salve `YOUTUBE_ATIVO=true` no `.env` (Edit cirurgico, adicionar linha). Continue para o PASSO 0.
Se escolher 2: salve `YOUTUBE_ATIVO=false` no `.env`. Encerre com:

```
Tudo bem. Se um dia criar um canal no YouTube, e so chamar essa skill de novo.
```

---

**Cenario: `YOUTUBE_ATIVO=true` (aluno confirmou que tem YouTube)**

Continue direto para o PASSO 0 sem perguntar nada.

---

### PASSO 0. Detectar Estado

Antes de qualquer pergunta, leia em paralelo:
1. `.env` na raiz do projeto — existe `APIFY_API_TOKEN` com valor? existe `YOUTUBE_CHANNEL` com valor?
2. `meus-produtos/{ativo}/entregas/youtube-dashboard/dashboard.html` — o arquivo existe?

---

#### Cenario A. Dashboard ja configurado (dashboard.html existe)

Mostre o menu sem perguntas:

```
Dashboard do YouTube ja esta configurado.

Canal monitorado: {YOUTUBE_CHANNEL do .env}

O que quer fazer?

1. Abrir o dashboard agora
2. Atualizar os dados agora
3. Trocar o canal monitorado
4. Recriar o script do zero
```

---

#### Cenario B. Primeira configuracao

**1. Canal do YouTube**

Prioridade: ler `.env` primeiro (`YOUTUBE_CHANNEL`). Se encontrar, confirme.
Se nao encontrar, pergunte:
```
Qual o endereco do seu canal no YouTube?
(ex: https://www.youtube.com/@meuperfil  ou  @meuperfil)
```

Normalize: aceitar `@handle`, URL completa ou channel ID. Salve com Edit cirurgico no `.env`: `YOUTUBE_CHANNEL=<valor>`.

**2. Token Apify**

Se `APIFY_API_TOKEN` estiver no `.env`: use diretamente, nao pergunte.
Se nao estiver: execute a skill `configurar-apify` e retorne aqui apos concluir.

---

### PASSO 1. Confirmacao

```
Configuracao confirmada:

- Canal YouTube: {YOUTUBE_CHANNEL}
- Token Apify: configurado
- Script: .claude/skills/youtube-dashboard/scripts/atualizar.py
- Dashboard: meus-produtos/{ativo}/entregas/youtube-dashboard/dashboard.html

1. Tudo certo, gerar agora
2. Quero ajustar algo
```

---

### PASSO 2. Executar

```bash
python .claude/skills/youtube-dashboard/scripts/atualizar.py --abrir
```

macOS / Linux: `python3 ...`

Leia o log para confirmar sucesso:
```bash
tail -10 meus-produtos/{ativo}/entregas/youtube-dashboard/log.txt
```

**Erros comuns:**

| Erro no log | Causa | Solucao |
|---|---|---|
| `401` ou autenticacao | Token Apify invalido | Verificar token em console.apify.com |
| `Canal vazio` ou erro | URL errada ou canal sem videos publicos | Confirmar URL do canal |
| Timeout | Ator YouTube lento | Aumentar timeout no script ou rodar novamente |

---

### PASSO 3. Entrega

Apos confirmar sucesso no log, atualize o painel de entregas:

```bash
py -3 scripts/painel-incremental.py --secao dashboards
```

(macOS/Linux: `python3 scripts/painel-incremental.py --secao dashboards`)

Se o painel ainda nao existir, informe:

```
O painel de entregas ainda nao foi criado para este produto.
Rode /produto-concepcao primeiro para gerar o painel, depois atualize os dashboards.
```

Informe ao aluno:

```
Dashboard do YouTube gerado.

Acesse pelo Painel de Entregas:
meus-produtos/{ativo}/painel-entregas.html  (aba Dashboards)

Para atualizar os dados quando quiser:
python .claude/skills/youtube-dashboard/scripts/atualizar.py
(depois rode: py -3 scripts/painel-incremental.py --secao dashboards)

Canal monitorado: {YOUTUBE_CHANNEL}
```

**Sem agendamento automatico:** o aluno roda o script manualmente.

---

### PASSO 4. Verificar Proxima Plataforma na Fila

Apos confirmar entrega com sucesso, verifique se `meus-produtos/{ativo}/.dashboard-queue.json` existe.

**Se o arquivo NAO existir:** exibir os "Proximos Passos" normalmente e encerrar. (Skill foi chamada diretamente, sem fila.)

**Se o arquivo EXISTIR:**

1. Leia o conteudo do arquivo.
2. Mova `"youtube"` de `pendentes` para `concluidos` (Edit cirurgico no JSON).
3. Verifique se ainda ha itens em `pendentes`.

**Se `pendentes` estiver vazio:** delete o arquivo `.dashboard-queue.json`. Exiba:

```
Todos os dashboards foram gerados.
```

E encerre.

**Regra:** o YouTube e sempre o ultimo da fila (ordem Instagram, TikTok, YouTube). Se `pendentes` ficar vazio aqui, e porque todos foram concluidos. Nunca havera proximo apos o YouTube.

**Regra:** nunca exibir os "Proximos Passos" quando o arquivo de fila existir. A fila tem prioridade sobre as sugestoes de conteudo.

---

## Regras

- **Sempre ler `.env` antes de pedir o token Apify ao usuario.**
- O token Apify e o canal ficam no `.env` (`APIFY_API_TOKEN` e `YOUTUBE_CHANNEL`). Nunca hardcodar no script.
- Dashboard em HTML puro. Sem libs externas alem de Google Fonts. Canvas puro para graficos.
- Nao usar travessao em nenhum texto exibido no dashboard.
- Tema claro: fundo #f8fafc, cards brancos, accent vermelho YouTube #ff0000 ou neutro indigo.
- **CRITICO — Thumbnails:** verificar se as URLs publicas do YouTube (`i.ytimg.com`) carregam em HTML local. Se nao, converter para base64.
- **CRITICO — Duracao ISO 8601:** converter `PT1H2M3S` para segundos no script. Exibir no dashboard em formato `1h 2min 3s` ou `HH:MM:SS`.
- **CRITICO — Engajamento no YouTube e calculado sobre views.** Formula: (likes + comentarios) / views * 100. Benchmark: 3-5% e considerado bom.
- **YouTube removeu dislikes da API:** nao tentar coletar ou exibir dislikeCount.

## Proximos Passos Apos Configurar

- `/copy-roteiro` — criar roteiros baseados nos videos com mais views
- `/copy-social` — criar conteudo para outras plataformas baseado nos temas que performam
- `/copy-anuncio` — transformar videos de sucesso em anuncios
