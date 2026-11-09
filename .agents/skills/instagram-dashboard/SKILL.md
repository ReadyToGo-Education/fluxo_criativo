---
name: instagram-dashboard
description: >
  Configura dashboard HTML de metricas do Instagram via Apify. Coleta dados
  publicos do perfil (seguidores, bio, foto), posts recentes e Reels (likes,
  comentarios, views). Todas as imagens embutidas em base64. Busca expandida
  para substituir posts com likes ocultos (ate 100 posts). Roda localmente
  na maquina do mentorado, sem servidor, sem GitHub, sem agendamento automatico.
user-invocable: false
---

# Instagram Dashboard. Metricas Diarias Automaticas

## Quando Usar

- Quando o aluno quiser monitorar o crescimento do proprio perfil no Instagram de forma automatica, sem precisar abrir ferramentas toda manha.
- Como base de dados para `/copy-carrossel` (conteudo baseado no que ja funciona) e `/dados-instagram` (analise profunda com insights de copy).
- Quando o aluno precisar mostrar evolucao de metricas para clientes ou parceiros.

**Nao usar para:**
- Analisar perfis de concorrentes (usar `/dados-instagram`).
- Perfis privados (o Apify nao coleta dados de perfis privados).

## O Que Entrega

| Arquivo | Descricao |
|---|---|
| `.claude/skills/instagram-dashboard/scripts/atualizar.py` | Script Python principal (Windows, macOS, Linux) — compartilhado entre todos os produtos |
| `.claude/skills/instagram-dashboard/scripts/atualizar_powershell.ps1` | Script PowerShell de backup (Windows) |
| `meus-produtos/{ativo}/entregas/instagram-dashboard/dashboard.html` | Dashboard HTML completo, abre no navegador |
| `meus-produtos/{ativo}/entregas/instagram-dashboard/imagens/` | Thumbnails e slides dos posts (gerados pelo script) |
| `meus-produtos/{ativo}/entregas/instagram-dashboard/insights.json` | Dados estruturados sem base64 (usado por /copy-variacao-post) |
| `meus-produtos/{ativo}/entregas/instagram-dashboard/historico.json` | Snapshots acumulativos (seguidores, engajamento) entre execucoes |
| `meus-produtos/{ativo}/entregas/instagram-dashboard/log.txt` | Log de cada execucao com timestamp e status |

## Como Funciona

```
atualizar.py  (ou atualizar_powershell.ps1 no Windows como backup)
  ├── POST apify~instagram-scraper (sync, timeout 60s)
  │     directUrls + resultsType:"details"  → seguidores, bio, foto de perfil
  │     Baixa profilePicUrl via requests/WebClient → base64
  ├── POST apify~instagram-scraper (sync, timeout 300s) — loop ate 100 posts
  │     directUrls + resultsType:"posts"    → posts (fotos, carrosseis, reels)
  │     Se posts com likesCount=-1 > 0: expande resultsLimit e busca de novo
  │     Para quando tiver 30 posts com likes visiveis OU atingir 100 posts
  │     Seleciona 30 priorizando posts com likes visiveis
  ├── Para cada post: baixa displayUrl via requests/WebClient → base64
  │     Para carrosseis: baixa cada imagem do array images → base64
  │     (CDN do Instagram bloqueia URLs diretas em HTML local)
  ├── Salva thumbnails e slides como .jpg em entregas/instagram-dashboard/imagens/
  │     Armazena caminhos relativos em insights.json (thumbnailPath, carouselPaths)
  │     Para Reels: transcreve audio via apify~whisper-speech-to-text → transcricao
  └── Regenera dashboard.html com dados + imagens embutidos como variavel JS
```

O `dashboard.html` e sempre autossuficiente: dados e thumbnails embutidos diretamente no HTML gerado pelo script. Nao depende de servidor local nem de `fetch()`. Funciona abrindo direto no navegador, inclusive offline apos a primeira geracao.

## APIs Utilizadas

Uma chamada de perfil + loop de posts (ambas sync, mesmo ator):

| # | Ator Apify | Tipo | Parametro chave | Retorna |
|---|---|---|---|---|
| 1 | `apify~instagram-scraper` | sync, timeout 60s | `directUrls`, `resultsType: "details"` | seguidores, bio, foto, verificado |
| 2 | `apify~instagram-scraper` | sync, timeout 300s | `directUrls`, `resultsType: "posts"`, `resultsLimit: 30..100` | posts com likes, comentarios, views. Expande ate 100 para substituir likes ocultos. |

**Por que sync e nao async:** o endpoint async do Apify retorna run IDs que ficam inacessiveis via polling (`record-not-found`) dependendo do plano da conta. O sync e mais simples e confiavel.

**Todas as imagens em base64:** o CDN do Instagram bloqueia carregamento de imagens de arquivos HTML locais. O script baixa TODAS as imagens (foto de perfil, thumbnails dos posts, imagens do carrossel) via `requests` (Python) ou `WebClient` (PowerShell) com `User-Agent` e `Referer: https://www.instagram.com/` e converte para `data:image/jpeg;base64,...`.

**Campo de imagem usado:** `displayUrl` (thumbnail JPEG do post). Para carrosseis, o campo `images` pode estar vazio — o script usa `displayUrl` como fallback. O cycling de carrossel funciona quando `images` tem multiplas entradas.

**insights.json com caminhos de arquivo:** alem de embutir base64 no dashboard, o script salva os thumbnails e slides como `.jpg` em `entregas/instagram-dashboard/imagens/` e armazena os caminhos relativos no `insights.json` (`thumbnailPath`, `carouselPaths`). Isso permite que o `/copy-variacao-post` use o Read tool do Claude para analisar visualmente as imagens.

**Transcricao de Reels:** para posts do tipo Video, o script chama `apify~whisper-speech-to-text` com a `videoUrl` do post e armazena a transcricao em `insights.json`. O `/copy-variacao-post` usa essa transcricao para entender o conteudo real do Reel sem precisar reproduzir o video.

Custo por execucao: ~US$0,05-0,20 no plano gratuito Apify (varia com quantas iteracoes de busca expandida forem necessarias).

## Compatibilidade por Sistema Operacional

O script principal e `atualizar.py` (Python 3), que funciona nativamente em todos os sistemas. O `atualizar_powershell.ps1` e o backup validado para Windows.

Instalacao da dependencia (unica):
```
pip install requests
```

| OS | Script | Como rodar |
|---|---|---|
| Windows | `atualizar.py` | `python atualizar.py --abrir` |
| macOS | `atualizar.py` | Python 3 ja incluso. `python3 atualizar.py --abrir` |
| Linux | `atualizar.py` | Python 3 ja incluso. `python3 atualizar.py --abrir` |
| Windows (backup) | `atualizar_powershell.ps1` | `powershell -ExecutionPolicy Bypass -File atualizar_powershell.ps1 -Abrir` |

## Configuracao Necessaria

| Chave | Onde fica | Como obter |
|---|---|---|
| `APIFY_API_TOKEN` | `.env` | console.apify.com > Settings > Integrations > Personal API token |
| `IG_USER` | `.env` | @ do perfil do aluno (sem @, lowercase). Tambem salvo em `entregas/conta.md` |

## Dashboard: O Que Mostra

**ESTRUTURA OBRIGATORIA — todas as 12 secoes devem estar presentes em todos os dashboards gerados, nesta ordem:**

1. **Cabecalho (perfil):** foto de perfil em base64 (fallback: inicial do nome), @username, bio, ultima atualizacao
2. **Visao Geral (4 cards KPI):** seguidores, engajamento medio (%) com total de shares, total de posts, formato mais postado
3. **Evolucao ao Longo do Tempo:** graficos de tendencia de seguidores e engajamento medio entre execucoes. So aparece quando historico.json tem 2+ snapshots.
4. **Desempenho por Formato:** cards separados para Reels, Carrossel e Foto com media de likes, comentarios, shares e views totais (Reels).
5. **Melhores Horarios para Postar:** heatmap 7x24 (dia da semana x hora). Intensidade = engajamento medio. Tooltip com contagem e media.
6. **Frequencia de Postagem:** posts por semana vs engajamento. Insight comparando semanas com 4+ posts vs menos.
7. **Top 3 Posts:** os 3 com maior engajamento, com thumbnail em base64, badge de tipo, likes, comentarios, shares, views (Reels), taxa de engajamento e link.
8. **Analise de Hashtags:** top 10 hashtags por engajamento medio. Barras horizontais com contagem e media.
9. **Tamanho da Legenda vs Engajamento:** 3 buckets (curta, media, longa) com engajamento medio por faixa. Insight textual.
10. **Linha do Tempo (4 graficos):** curtidas, visualizacoes (Reels), engajamento (%) e compartilhamentos. Canvas puro, uma linha por formato, tooltip colorido.
11. **Barra de Filtros:** filtros interativos por tipo (Reel/Carrossel/Foto) e periodo (7/15/30 dias). Afeta grade de posts, Top 3 e KPIs.
12. **Todos os Posts (grade):** thumbnail ciclavel em base64, badge de tipo, likes, comentarios, shares, views (Reels), data, legenda truncada e link.

**NUNCA omitir nenhuma dessas 12 secoes.** Nao existe versao simplificada do dashboard.

## Fluxo

### PASSO -1. Verificar Plataforma Ativa (OBRIGATORIO — executar antes de qualquer outra coisa)

Leia `.env`. Verifique o valor de `INSTAGRAM_ATIVO`.

**Cenario: `INSTAGRAM_ATIVO=false` (aluno ja disse que nao tem Instagram)**

```
Voce marcou que nao tem um perfil ativo no Instagram.

Quer atualizar essa preferencia?

1. Sim, tenho Instagram agora — configurar o dashboard
2. Nao, pode ignorar
```

Se escolher 1: troque `INSTAGRAM_ATIVO=false` por `INSTAGRAM_ATIVO=true` no `.env` e continue para o PASSO 0.
Se escolher 2: encerre sem fazer nada.

---

**Cenario: `INSTAGRAM_ATIVO` nao existe no `.env` (primeira vez)**

```
Voce tem um perfil ativo no Instagram que quer monitorar?

1. Sim, tenho Instagram
2. Nao tenho Instagram
```

Se escolher 1: salve `INSTAGRAM_ATIVO=true` no `.env` (Edit cirurgico, adicionar linha). Continue para o PASSO 0.
Se escolher 2: salve `INSTAGRAM_ATIVO=false` no `.env`. Encerre com:

```
Tudo bem. Se um dia criar um perfil no Instagram, e so chamar essa skill de novo.
```

---

**Cenario: `INSTAGRAM_ATIVO=true` (aluno confirmou que tem Instagram)**

Continue direto para o PASSO 0 sem perguntar nada.

---

### PASSO 0. Detectar Estado

Antes de qualquer pergunta, leia em paralelo:
1. `.env` na raiz do projeto — existe `APIFY_API_TOKEN` com valor? existe `IG_USER` com valor?
2. `meus-produtos/{ativo}/entregas/instagram-dashboard/dashboard.html` — o arquivo existe?

---

#### Cenario A. Dashboard ja configurado (dashboard.html existe)

Mostre o menu sem perguntas:

```
Dashboard do Instagram ja esta configurado.

Perfil monitorado: @{IG_USER do .env}

O que quer fazer?

1. Abrir o dashboard agora
2. Atualizar os dados agora
3. Trocar o perfil monitorado
4. Recriar o script do zero
```

**Opcao 1 — Abrir (Windows):**
```bash
start meus-produtos/{ativo}/entregas/instagram-dashboard/dashboard.html
```
macOS: `open ...` / Linux: `xdg-open ...`

**Opcao 2 — Atualizar:**
```bash
python .claude/skills/instagram-dashboard/scripts/atualizar.py --abrir
```
Aguarde, leia o log em `meus-produtos/{ativo}/entregas/instagram-dashboard/log.txt`, informe o resultado.

**Opcao 3 — Trocar perfil:**
Pergunte o novo @. Normalize (sem @, lowercase). Atualize com Edit cirurgico no `.env`: linha `IG_USER=<novo_username>`. Execute para testar:
```bash
python .claude/skills/instagram-dashboard/scripts/atualizar.py --abrir
```

**Opcao 4 — Recriar do zero:**
Siga o Cenario B abaixo.

---

#### Cenario B. Primeira configuracao

**1. Username do Instagram**

Prioridade: ler `.env` primeiro (`IG_USER`). Se encontrar, confirme:

```
Encontrei o Instagram configurado: @{username}

E esse mesmo perfil que quer monitorar?

1. Sim, pode continuar
2. Nao, quero usar outro
```

Se nao encontrar, pergunte:
```
Qual o usuario do seu perfil no Instagram? (so o nome, sem o arroba)
(ex: meuperfil)
```

Normalize: sem @, lowercase. Salve com Edit cirurgico no `.env`: `IG_USER=<username>`.

**2. Token Apify**

Se `APIFY_API_TOKEN` estiver no `.env`: use diretamente, nao pergunte.
Se nao estiver: execute a skill `configurar-apify` e retorne aqui apos concluir.

---

### PASSO 1. Confirmacao

```
Configuracao confirmada:

- Perfil Instagram: @{username}
- Token Apify: configurado
- Script: .claude/skills/instagram-dashboard/scripts/atualizar.py
- Dashboard: meus-produtos/{ativo}/entregas/instagram-dashboard/dashboard.html

Custo estimado no Apify: menos de US$ 0,20 por geracao no plano gratuito.

1. Tudo certo, atualizar agora
2. Quero ajustar algo
```

---

### PASSO 2. Executar

```bash
python .claude/skills/instagram-dashboard/scripts/atualizar.py --abrir
```

macOS / Linux: `python3 ...`

Aguarde a conclusao (pode levar ate 10 minutos — busca expandida de ate 100 posts).

Leia o log para confirmar sucesso:
```bash
tail -10 meus-produtos/{ativo}/entregas/instagram-dashboard/log.txt
```

**Erros comuns:**

| Erro no log | Causa | Solucao |
|---|---|---|
| `401` ou autenticacao | Token Apify invalido | Verificar token em console.apify.com |
| `Perfil vazio` ou erro | @ errado ou perfil privado | Confirmar username; perfis privados nao funcionam |
| Arquivo travado pelo navegador | Browser com dashboard aberto | Fechar a aba do dashboard e rodar novamente |

---

### PASSO 3. Entrega

Apos confirmar sucesso no log, atualize o painel de entregas:

```bash
py -3 scripts/painel-incremental.py --secao dashboards
```

(macOS/Linux: `python3 scripts/painel-incremental.py --secao dashboards`)

Isso embute o dashboard como aba dentro do painel de entregas do produto ativo.

Se o painel ainda nao existir (produto recente sem /produto-concepcao), informe:

```
O painel de entregas ainda nao foi criado para este produto.
Rode /produto-concepcao primeiro para gerar o painel, depois atualize os dashboards.
```

Informe ao aluno:

```
Dashboard do Instagram gerado.

Acesse pelo Painel de Entregas:
meus-produtos/{ativo}/painel-entregas.html  (aba Dashboards)

Para atualizar os dados quando quiser:
python .claude/skills/instagram-dashboard/scripts/atualizar.py
(depois rode: py -3 scripts/painel-incremental.py --secao dashboards)

Perfil monitorado: @{username}
```

**Sem agendamento automatico:** nao configurar CronCreate nem schtasks. O aluno roda o script manualmente.

Backup PowerShell (Windows):
```
powershell -ExecutionPolicy Bypass -File .claude\skills\instagram-dashboard\scripts\atualizar_powershell.ps1 -Abrir
```

---

### PASSO 4. Verificar Proxima Plataforma na Fila

Apos confirmar entrega com sucesso, verifique se `meus-produtos/{ativo}/.dashboard-queue.json` existe.

**Se o arquivo NAO existir:** exibir os "Proximos Passos" normalmente e encerrar. (Skill foi chamada diretamente, sem fila.)

**Se o arquivo EXISTIR:**

1. Leia o conteudo do arquivo.
2. Mova `"instagram"` de `pendentes` para `concluidos` (Edit cirurgico no JSON).
3. Verifique se ainda ha itens em `pendentes`.

**Se `pendentes` estiver vazio:** delete o arquivo `.dashboard-queue.json`. Exiba:

```
Todos os dashboards foram gerados.
```

E encerre.

**Se `pendentes` tiver proxima plataforma**, exiba a oferta de continuacao:

```
Instagram concluido.

Proximo na fila: {Plataforma} ({@username ou canal, se ja estiver no .env})

1. Gerar o dashboard do {Plataforma} agora
2. Parar por aqui (posso continuar depois chamando /dashboard-social)
```

- Opcao 1: executar a skill correspondente (`tiktok-dashboard` ou `youtube-dashboard`).
- Opcao 2: encerrar sem alterar a fila. Na proxima chamada a `/dashboard-social`, o arquivo sera detectado e oferecera retomada automatica.

**Regra:** nunca exibir os "Proximos Passos" quando o arquivo de fila existir. A fila tem prioridade sobre as sugestoes de conteudo.

---

## Regras

- **Sempre ler `.env` antes de pedir o token Apify ao usuario.** Se `APIFY_API_TOKEN` estiver presente, usar diretamente. So perguntar se o arquivo nao existir ou a chave estiver vazia.
- O token Apify e o username do Instagram ficam no `.env` (`APIFY_API_TOKEN` e `IG_USER`). O script le essas variaveis do `.env` em runtime. Nunca hardcodar no script.
- Nunca sobrescrever `entregas/conta.md` inteiro. Usar Edit cirurgico para atualizar so o campo `Instagram:`.
- Dashboard em HTML puro. Sem libs externas alem de Google Fonts. Canvas puro para grafico.
- Nao usar travessao em nenhum texto exibido no dashboard.
- Design system Fluxo Criativo: fundo `#000000`, surface `#111111`, borda `#252525`, texto `#e8e8e6`, muted `#a8a8a3`, neon `#c4ff5e` como cor de destaque principal. Fontes JetBrains Mono + Space Grotesk via Google Fonts. Cards com `border-top:2px solid`, sem sombra, sem border-radius.
- Se o perfil for privado, informar e sugerir export manual via Metricool ou Instagram Insights.
- **CRITICO — Thumbnails obrigatorios em base64:** NUNCA usar a URL do CDN do Instagram diretamente como `src` de `<img>`. O CDN bloqueia carregamento de arquivos HTML locais. O script DEVE baixar cada thumbnail com `requests` (Python) ou `WebClient` (PowerShell) com User-Agent e Referer do Instagram e converter para `data:image/jpeg;base64,...` antes de embutir no JSON. Isso e inegociavel para as imagens aparecerem no dashboard.
- **CRITICO — Usar apenas `apify~instagram-scraper` com chamadas sync:** NAO usar atores `nH2AHrwxeTRJoN5hX` nem `xMc5Ga1oCONPmWJIa` (retornam run IDs inacessiveis no polling). Usar sempre o endpoint `run-sync-get-dataset-items` com `resultsType:"details"` (perfil) e `resultsType:"posts"` (posts), ambos via `directUrls` com a URL do perfil.
- **CRITICO — Campo de imagem correto:** o campo `displayUrl` do Apify retorna a thumbnail do post. O campo `images` pode estar vazio mesmo para carrosseis. O script deve sempre usar `displayUrl` como fallback obrigatorio para a thumbnail principal.
- **Likes ocultos (likesCount = -1):** o Instagram permite que criadores ocultem a contagem de likes por post. O Apify retorna `likesCount: -1` nesses casos. O script deve: (1) tentar buscar mais posts do perfil para substituir os com likes ocultos — expande o `resultsLimit` incrementalmente ate ter 30 posts com likes visiveis ou atingir o cap de 100 posts; (2) priorizar posts com likes visiveis na selecao final dos 30 exibidos; (3) exibir `--` no lugar de `-1` no dashboard; (4) usar `0` nos calculos internos (media, ordenacao Top 3, altura de barras no grafico).

## Proximos Passos Apos Configurar

- `/copy-variacao-post` — criar variacoes dos posts com mais engajamento (le thumbnails e insights.json do dashboard)
- `/copy-carrossel` — criar conteudo novo baseado nos posts com mais engajamento
- `/copy-anuncio` — transformar os dados em anuncios com angulos testados
