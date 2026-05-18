---
name: linkedin-dashboard
description: >
  Configura e gera o dashboard HTML de metricas do LinkedIn para o produto ativo.
  Coleta dados publicos do perfil (seguidores, headline, bio) e dos ultimos 30 posts
  (likes, comentarios, shares, tipo de post, data) via Apify, sem exigir login.
  Gera dashboard autossuficiente que abre direto no navegador com filtros interativos.
---

# LinkedIn Dashboard

## Quando Usar

Quando o aluno quiser ver as metricas do seu perfil no LinkedIn: engajamento por tipo de post, melhores dias para postar, top posts, hashtags mais eficazes e historico de crescimento.

**Alternativa:** o comando `dashboard-social` orquestra LinkedIn junto com Instagram, TikTok e YouTube em um fluxo unificado.

---

## Atores Apify Utilizados

| Ator | Finalidade | Custo aprox. |
|---|---|---|
| `harvestapi~linkedin-profile-posts` | Posts (texto, likes, comentarios, shares, data, tipo, midia) | US$1,50/1000 posts |
| `dev-fusion~linkedin-profile-scraper-no-cookies` | Perfil (seguidores, headline, bio, avatar) | US$10/1000 perfis |

Ambos funcionam sem cookies e sem login no LinkedIn.

---

## Variaveis de Ambiente

| Variavel | Exemplo | Descricao |
|---|---|---|
| `APIFY_API_TOKEN` | `apify_api_...` | Token do Apify (compartilhado com outros dashboards) |
| `LINKEDIN_PROFILE` | `leandroladeira` | Handle, URL completa ou `/in/handle` do perfil |

O script aceita qualquer formato para `LINKEDIN_PROFILE`:
- Handle puro: `leandroladeira`
- Com arroba: `@leandroladeira`
- URL: `https://www.linkedin.com/in/leandroladeira`
- Caminho: `/in/leandroladeira`

---

## O Que o Dashboard Mostra

| Secao | Dados |
|---|---|
| Header | Foto, nome, headline, URL do perfil |
| Visao Geral (KPIs) | Seguidores, Conexoes, Engajamento medio, Posts analisados, Tipo mais postado |
| Evolucao historica | Seguidores e engajamento ao longo do tempo (cresce a cada execucao) |
| Desempenho por tipo | Texto, Imagem, Video, Documento (PDF/carrossel), Artigo, Repost -- likes/comentarios/shares/eng medios |
| Melhores dias | Engajamento medio por dia da semana |
| Frequencia | Posts por semana com insight automatico |
| Top 3 posts | Maior engajamento (likes + comentarios + shares / seguidores) |
| Hashtags | Top 10 hashtags por engajamento medio |
| Texto vs Engajamento | Posts curtos (ate 100 char), medios (101-300), longos (301+) |
| Linha do Tempo | Likes, comentarios, shares e engajamento ao longo do tempo |
| Filtros interativos | Por tipo de post + por periodo (7, 15, 30 dias ou todos) |
| Grade de posts | Todos os posts com miniatura, metricas e link |

---

## Fluxo de Execucao

1. Le `APIFY_API_TOKEN` e `LINKEDIN_PROFILE` do `.env`
2. Busca perfil e posts em paralelo (dois atores simultaneos)
3. Se o ator de perfil nao retornar nome, extrai do campo `author` dos posts (fallback)
4. Calcula engajamento = (likes + comentarios + shares) / seguidores * 100
5. Baixa avatar e imagens dos posts com cache entre execucoes
6. Salva `insights.json` (sem base64, para uso por outras skills)
7. Atualiza `historico.json` (snapshot diario para grafico de evolucao)
8. Gera `dashboard.html` autossuficiente

**Saidas:**
- `meus-produtos/{ativo}/entregas/linkedin-dashboard/{handle}/dashboard.html`
- `meus-produtos/{ativo}/entregas/linkedin-dashboard/{handle}/insights.json`
- `meus-produtos/{ativo}/entregas/linkedin-dashboard/{handle}/historico.json`
- `meus-produtos/{ativo}/entregas/linkedin-dashboard/{handle}/imagens/`

---

## Como Executar

```bash
python .claude/skills/linkedin-dashboard/scripts/atualizar.py
python .claude/skills/linkedin-dashboard/scripts/atualizar.py --abrir
python .claude/skills/linkedin-dashboard/scripts/atualizar.py --perfil leandroladeira
```

---

## Limitacoes Conhecidas

- LinkedIn restringe scraping agressivamente. Os atores "no cookies" contornam isso, mas perfis com poucos posts ou configuracoes de privacidade altas podem retornar dados incompletos.
- Seguidores podem nao ser retornados em perfis pessoais (LinkedIn oculta para nao-conexoes). Nesse caso, o engajamento e calculado sobre 1 seguidor (o denominador fica 1) -- os numeros de engajamento serao altos mas relativos.
- O actor de perfil pode falhar sem impactar os posts: o fallback extrai nome e avatar do campo `author` dos proprios posts.
- Impressoes (views de post) raramente sao expostas pela API publica do LinkedIn.

---

## Proximos Passos Apos Gerar

- `dashboard-social` -- ver todos os dashboards juntos
- `copy-social` -- criar conteudo baseado nos posts que performaram melhor
- `copy-anuncio` -- criar anuncios baseados nos temas com mais engajamento
