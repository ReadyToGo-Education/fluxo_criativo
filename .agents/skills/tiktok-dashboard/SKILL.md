---
name: tiktok-dashboard
description: >
  Configura dashboard HTML de metricas do TikTok via Apify. Coleta dados
  publicos do perfil (seguidores, likes totais, bio, avatar), videos recentes
  (views, likes, comentarios, compartilhamentos, saves, duracao). Todas as
  thumbnails embutidas em base64. Roda localmente na maquina do mentorado,
  sem servidor, sem GitHub, sem agendamento automatico.
user-invocable: false
---

# TikTok Dashboard. Metricas Diarias Automaticas

## Quando Usar

- Quando o aluno quiser monitorar o crescimento do proprio perfil no TikTok de forma automatica, sem precisar abrir ferramentas toda manha.
- Como base de dados para `/copy-social` (conteudo baseado no que ja funciona) e para analisar padroes de videos que viralizaram.
- Quando o aluno precisar mostrar evolucao de metricas para clientes ou parceiros.

**Nao usar para:**
- Analisar perfis de concorrentes (adaptar o script passando outro username).
- Perfis privados (o Apify nao coleta dados de perfis privados).

## O Que Entrega

| Arquivo | Descricao |
|---|---|
| `.claude/skills/tiktok-dashboard/scripts/atualizar.py` | Script Python principal (Windows, macOS, Linux) — compartilhado entre todos os produtos |
| `meus-produtos/{ativo}/entregas/tiktok-dashboard/dashboard.html` | Dashboard HTML completo, abre no navegador |
| `meus-produtos/{ativo}/entregas/tiktok-dashboard/imagens/` | Thumbnails dos videos (gerados pelo script) |
| `meus-produtos/{ativo}/entregas/tiktok-dashboard/insights.json` | Dados estruturados sem base64 |
| `meus-produtos/{ativo}/entregas/tiktok-dashboard/historico.json` | Snapshots acumulativos (seguidores, engajamento) entre execucoes |
| `meus-produtos/{ativo}/entregas/tiktok-dashboard/log.txt` | Log de cada execucao com timestamp e status |

## Como Funciona

```
atualizar.py
  ├── POST Apify (ator TikTok, sync) — perfil
  │     username → seguidores, seguindo, likes totais, bio, avatar
  │     Baixa avatar → base64
  ├── POST Apify (ator TikTok, sync) — videos
  │     username → ultimos N videos
  │     Para cada video: views, likes, comentarios, compartilhamentos,
  │                      saves, duracao, hashtags, descricao, data
  │     Baixa thumbnail de cada video → base64
  ├── Calcula metricas: engajamento = (likes+comentarios+shares) / views
  ├── Atualiza historico.json com snapshot do dia
  └── Regenera dashboard.html com dados + thumbnails embutidos como variavel JS
```

O `dashboard.html` e sempre autossuficiente: dados e thumbnails embutidos diretamente no HTML. Nao depende de servidor local. Funciona abrindo direto no navegador, inclusive offline apos a primeira geracao.

## APIs Utilizadas

Ator utilizado: `clockworks~tiktok-scraper` (o mais estavel e completo em 2026).

| # | Ator Apify | Tipo | Parametro chave | Retorna |
|---|---|---|---|---|
| 1 | `clockworks~tiktok-scraper` | sync, timeout 300s | `profiles` (URL do perfil), `resultsPerPage: 30` | lista de videos com `authorMeta` embutido (perfil + videos numa so chamada) |

Chamada sync (endpoint `run-sync-get-dataset-items`). Uma unica chamada retorna perfil (via `authorMeta` do primeiro item) e todos os videos. Nao ha chamada separada de perfil.

**Por que sync e nao async:** mesmo motivo do Instagram: endpoints async retornam run IDs que podem ficar inacessiveis dependendo do plano. Sync e mais simples e confiavel.

**Todas as thumbnails em base64:** TikTok CDN pode bloquear imagens em HTML local. O script baixa cada thumbnail com `requests` usando User-Agent e Referer adequados.

Custo por execucao: a definir (depende do ator escolhido e do numero de videos coletados).

## Compatibilidade por Sistema Operacional

Instalacao da dependencia (unica):
```
pip install requests
```

| OS | Como rodar |
|---|---|
| Windows | `python .claude/skills/tiktok-dashboard/scripts/atualizar.py --abrir` |
| macOS | `python3 .claude/skills/tiktok-dashboard/scripts/atualizar.py --abrir` |
| Linux | `python3 .claude/skills/tiktok-dashboard/scripts/atualizar.py --abrir` |

## Configuracao Necessaria

| Chave | Onde fica | Como obter |
|---|---|---|
| `APIFY_API_TOKEN` | `.env` | console.apify.com > Settings > Integrations > Personal API token |
| `TIKTOK_USER` | `.env` | @ do perfil do aluno (sem @, lowercase) |

## Dashboard: O Que Mostra

**ESTRUTURA OBRIGATORIA — todas as secoes devem estar presentes, nesta ordem:**

1. **Cabecalho (perfil):** avatar em base64 (fallback: inicial do nome), @username, bio, total de likes, ultima atualizacao
2. **Visao Geral (KPIs):** seguidores, engajamento medio (%), total de videos, formato/duracao mais comum
3. **Evolucao ao Longo do Tempo:** tendencia de seguidores e engajamento medio entre execucoes. So aparece com 2+ snapshots em historico.json.
4. **Desempenho por Duracao:** videos agrupados por faixa de duracao (ate 15s, 16-30s, 31-60s, 60s+). Media de views, likes, engajamento.
5. **Melhores Horarios para Postar:** heatmap 7x24 (dia da semana x hora). Intensidade = engajamento medio.
6. **Frequencia de Postagem:** videos por semana vs engajamento. Insight comparando semanas mais ativas.
7. **Top 3 Videos:** os 3 com maior views ou engajamento, com thumbnail em base64, views, likes, comentarios, shares, saves, taxa de engajamento e link.
8. **Analise de Hashtags:** top 10 hashtags por engajamento medio. Barras horizontais.
9. **Tamanho da Descricao vs Engajamento:** 3 buckets (curta, media, longa) com engajamento medio por faixa.
10. **Linha do Tempo (graficos):** views, likes, engajamento (%), saves ao longo do tempo. Canvas puro, tooltip.
11. **Barra de Filtros:** filtros por duracao e periodo (7/15/30 dias). Afeta grade de videos, Top 3 e KPIs.
12. **Todos os Videos (grade):** thumbnail em base64, views, likes, comentarios, shares, saves, data, descricao truncada e link.

**NUNCA omitir nenhuma dessas 12 secoes.**

## Metricas TikTok (diferente do Instagram)

| Metrica | Campo Apify | Observacao |
|---|---|---|
| Views | `playCount` ou `videoPlayCount` | Metrica principal no TikTok |
| Likes | `diggCount` ou `likesCount` | |
| Comentarios | `commentCount` ou `commentsCount` | |
| Compartilhamentos | `shareCount` ou `sharesCount` | |
| Saves | `collectCount` ou `bookmarkCount` | Pode nao estar disponivel em todos os atores |
| Duracao | `duration` (segundos) | |
| Hashtags | `hashtags` (array) ou extraido da `desc` | |
| Engajamento TikTok | (likes + comentarios + shares) / views * 100 | Nao divide por seguidores como no Instagram |

> **Nota de implementacao:** os nomes exatos dos campos dependem do ator Apify escolhido. Verificar no JSON de retorno antes de codar.

## Fluxo

### PASSO -1. Verificar Plataforma Ativa (OBRIGATORIO — executar antes de qualquer outra coisa)

Leia `.env`. Verifique o valor de `TIKTOK_ATIVO`.

**Cenario: `TIKTOK_ATIVO=false` (aluno ja disse que nao tem TikTok)**

```
Voce marcou que nao tem um perfil ativo no TikTok.

Quer atualizar essa preferencia?

1. Sim, tenho TikTok agora — configurar o dashboard
2. Nao, pode ignorar
```

Se escolher 1: apague a linha `TIKTOK_ATIVO=false` do `.env` (ou troque por `TIKTOK_ATIVO=true`) e continue para o PASSO 0.
Se escolher 2: encerre sem fazer nada.

---

**Cenario: `TIKTOK_ATIVO` nao existe no `.env` (primeira vez)**

```
Voce tem um perfil ativo no TikTok que quer monitorar?

1. Sim, tenho TikTok
2. Nao tenho TikTok
```

Se escolher 1: salve `TIKTOK_ATIVO=true` no `.env` (Edit cirurgico, adicionar linha). Continue para o PASSO 0.
Se escolher 2: salve `TIKTOK_ATIVO=false` no `.env`. Encerre com:

```
Tudo bem. Se um dia criar um perfil no TikTok, e so chamar essa skill de novo.
```

---

**Cenario: `TIKTOK_ATIVO=true` (aluno confirmou que tem TikTok)**

Continue direto para o PASSO 0 sem perguntar nada.

---

### PASSO 0. Detectar Estado

Antes de qualquer pergunta, leia em paralelo:
1. `.env` na raiz do projeto — existe `APIFY_API_TOKEN` com valor? existe `TIKTOK_USER` com valor?
2. `meus-produtos/{ativo}/entregas/tiktok-dashboard/dashboard.html` — o arquivo existe?

---

#### Cenario A. Dashboard ja configurado (dashboard.html existe)

Mostre o menu sem perguntas:

```
Dashboard do TikTok ja esta configurado.

Perfil monitorado: @{TIKTOK_USER do .env}

O que quer fazer?

1. Abrir o dashboard agora
2. Atualizar os dados agora
3. Trocar o perfil monitorado
4. Recriar o script do zero
```

---

#### Cenario B. Primeira configuracao

**1. Username do TikTok**

Prioridade: ler `.env` primeiro (`TIKTOK_USER`). Se encontrar, confirme:

```
Encontrei o TikTok configurado: @{username}

E esse mesmo perfil que quer monitorar?

1. Sim, pode continuar
2. Nao, quero usar outro
```

Se nao encontrar, pergunte:
```
Qual o usuario do seu perfil no TikTok? (so o nome, sem o arroba)
(ex: meuperfil)
```

Normalize: sem @, lowercase. Salve com Edit cirurgico no `.env`: `TIKTOK_USER=<username>`.

**2. Token Apify**

Se `APIFY_API_TOKEN` estiver no `.env`: use diretamente, nao pergunte.
Se nao estiver: execute a skill `configurar-apify` e retorne aqui apos concluir.

---

### PASSO 1. Confirmacao

```
Configuracao confirmada:

- Perfil TikTok: @{username}
- Token Apify: configurado
- Script: .claude/skills/tiktok-dashboard/scripts/atualizar.py
- Dashboard: meus-produtos/{ativo}/entregas/tiktok-dashboard/dashboard.html

1. Tudo certo, gerar agora
2. Quero ajustar algo
```

---

### PASSO 2. Executar

```bash
python .claude/skills/tiktok-dashboard/scripts/atualizar.py --abrir
```

macOS / Linux: `python3 ...`

Leia o log para confirmar sucesso:
```bash
tail -10 meus-produtos/{ativo}/entregas/tiktok-dashboard/log.txt
```

**Erros comuns:**

| Erro no log | Causa | Solucao |
|---|---|---|
| `401` ou autenticacao | Token Apify invalido | Verificar token em console.apify.com |
| `Perfil vazio` ou erro | @ errado ou perfil privado | Confirmar username; perfis privados nao funcionam |
| Timeout | Ator TikTok lento | Aumentar timeout no script ou rodar novamente |

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
Dashboard do TikTok gerado.

Acesse pelo Painel de Entregas:
meus-produtos/{ativo}/painel-entregas.html  (aba Dashboards)

Para atualizar os dados quando quiser:
python .claude/skills/tiktok-dashboard/scripts/atualizar.py
(depois rode: py -3 scripts/painel-incremental.py --secao dashboards)

Perfil monitorado: @{username}
```

**Sem agendamento automatico:** o aluno roda o script manualmente.

---

### PASSO 4. Verificar Proxima Plataforma na Fila

Apos confirmar entrega com sucesso, verifique se `meus-produtos/{ativo}/.dashboard-queue.json` existe.

**Se o arquivo NAO existir:** exibir os "Proximos Passos" normalmente e encerrar. (Skill foi chamada diretamente, sem fila.)

**Se o arquivo EXISTIR:**

1. Leia o conteudo do arquivo.
2. Mova `"tiktok"` de `pendentes` para `concluidos` (Edit cirurgico no JSON).
3. Verifique se ainda ha itens em `pendentes`.

**Se `pendentes` estiver vazio:** delete o arquivo `.dashboard-queue.json`. Exiba:

```
Todos os dashboards foram gerados.
```

E encerre.

**Se `pendentes` tiver proxima plataforma**, exiba a oferta de continuacao:

```
TikTok concluido.

Proximo na fila: {Plataforma} ({@username ou canal, se ja estiver no .env})

1. Gerar o dashboard do {Plataforma} agora
2. Parar por aqui (posso continuar depois chamando /dashboard-social)
```

- Opcao 1: executar a skill correspondente (`youtube-dashboard`).
- Opcao 2: encerrar sem alterar a fila. Na proxima chamada a `/dashboard-social`, o arquivo sera detectado e oferecera retomada automatica.

**Regra:** nunca exibir os "Proximos Passos" quando o arquivo de fila existir. A fila tem prioridade sobre as sugestoes de conteudo.

---

## Regras

- **Sempre ler `.env` antes de pedir o token Apify ao usuario.** Se `APIFY_API_TOKEN` estiver presente, usar diretamente.
- O token Apify e o username ficam no `.env` (`APIFY_API_TOKEN` e `TIKTOK_USER`). Nunca hardcodar no script.
- Dashboard em HTML puro. Sem libs externas alem de Google Fonts. Canvas puro para graficos.
- Nao usar travessao em nenhum texto exibido no dashboard.
- Design system Fluxo Criativo: fundo `#000000`, surface `#111111`, borda `#252525`, texto `#e8e8e6`, muted `#a8a8a3`, neon `#c4ff5e` como cor de destaque principal. Fontes JetBrains Mono + Space Grotesk via Google Fonts. Cards com `border-top:2px solid`, sem sombra, sem border-radius.
- Se o perfil for privado, informar e encerrar com orientacao.
- **CRITICO — Thumbnails obrigatorias em base64:** NUNCA usar URL do CDN do TikTok diretamente como src de img. Baixar via requests com User-Agent adequado.
- **CRITICO — Engajamento no TikTok e calculado sobre views, nao sobre seguidores.** Formula: (likes + comentarios + shares) / views * 100.

## Proximos Passos Apos Configurar

- `/copy-variacao-post` — criar variacoes dos videos com mais views
- `/copy-social` — criar conteudo novo baseado nos videos com mais engajamento
- `/copy-anuncio` — transformar os dados em anuncios com angulos testados
