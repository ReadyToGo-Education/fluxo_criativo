---
name: pesquisa-mercado-instagram
description: >
  Pesquisa de mercado via Instagram usando Apify. Descobre perfis de referencia
  do nicho no Brasil e no mundo a partir de hashtags, analisa conteudo dos top
  perfis (formato, engajamento, horarios, hashtags) e gera dashboard HTML
  interativo com ranking de perfis, mapa de hashtags e analise de conteudo.
  Roda localmente via script Python.
---

# Pesquisa de Mercado Instagram. Descoberta de Perfis e Conteudo do Nicho

## Quando Usar

- Quando o aluno quiser mapear os principais perfis do nicho dele no Instagram.
- Para entender que tipo de conteudo funciona no nicho (formato, horario, hashtags).
- Como base de dados para estrategia de conteudo e posicionamento.
- Na fase de concepcao de produto, para validar nicho e identificar oportunidades.

**Nao usar para:**
- Monitorar o proprio perfil (usar `/instagram-dashboard`).
- Analise profunda de um perfil especifico (usar `/dados-instagram`).
- Perfis privados (o Apify nao coleta dados de perfis privados).

## O Que Entrega

| Arquivo | Descricao |
|---|---|
| `.claude/skills/pesquisa-mercado-instagram/scripts/pesquisar.py` | Script Python principal (Windows, macOS, Linux) |
| `meus-produtos/{ativo}/entregas/pesquisa-nicho/config.json` | Configuracao de hashtags e parametros |
| `meus-produtos/{ativo}/entregas/pesquisa-nicho/{slug}/dashboard.html` | Dashboard HTML completo |
| `meus-produtos/{ativo}/entregas/pesquisa-nicho/{slug}/insights.json` | Dados estruturados dos perfis e analise |
| `meus-produtos/{ativo}/entregas/pesquisa-nicho/{slug}/imagens/` | Fotos de perfil dos perfis encontrados |
| `meus-produtos/{ativo}/entregas/pesquisa-nicho/{slug}/log.txt` | Log de cada execucao |

## Como Funciona

```
pesquisar.py
  ├── Le config.json (hashtags BR, hashtags Mundo, perfis semente, minSeguidores)
  ├���─ Etapa 1: Busca posts por hashtag (50 posts por hashtag, sync)
  │     Para cada hashtag BR e Mundo → extrai ownerUsername dos posts
  ├── Etapa 2: Enriquece perfis unicos em batch (20 por chamada)
  │     directUrls + resultsType:"details" → seguidores, bio, verificado
  │     Baixa fotos de perfil em paralelo → base64 + .jpg em imagens/
  │     Filtra por minSeguidores (padrao: 1000)
  ├── Etapa 3: Busca 30 posts dos top 15 perfis por seguidores
  │     directUrls + resultsType:"posts" → analise de conteudo
  ├── Etapa 4: Calcula metricas
  │     Engajamento por perfil, formato, hashtags, horarios
  └── Etapa 5: Gera dashboard.html + insights.json
```

## APIs Utilizadas

Mesmo ator do instagram-dashboard, chamadas sync:

| # | Tipo | Parametro | Retorna |
|---|---|---|---|
| 1 | Hashtag posts | `directUrls: [URL da hashtag]`, `resultsType: "posts"` | Posts com ownerUsername |
| 2 | Perfil details (batch) | `directUrls: [URLs de perfis]`, `resultsType: "details"` | Seguidores, bio, verificado |
| 3 | Posts top perfis | `directUrls: [URL do perfil]`, `resultsType: "posts"` | Posts para analise |

Custo estimado: US$ 1-2 por execucao (mais chamadas que o dashboard de perfil).

## Configuracao Necessaria

| Chave | Onde fica | Como obter |
|---|---|---|
| `APIFY_API_TOKEN` | `.env` | console.apify.com > Settings > Integrations |

O `config.json` e criado na entrevista (Passo 1) com as hashtags do nicho.

## Dashboard: O Que Mostra

1. **KPIs gerais:** perfis descobertos (BR/Mundo), media de seguidores, engajamento medio, verificados
2. **Top Perfis Brasil:** cards com foto, username, seguidores, engajamento, formato top, bio, link
3. **Top Perfis Mundo:** idem
4. **Desempenho por Formato:** engajamento medio de Reel vs Carrossel vs Foto
5. **Top Hashtags do Nicho:** ranking por engajamento medio (minimo 3 ocorrencias)
6. **Melhores Horarios para Postar:** heatmap 7x24 (dia x hora, horario local)
7. **Todos os Perfis:** grade filtravel por origem (BR/Mundo)

## Fluxo

### PASSO 0. Detectar Estado

Antes de qualquer pergunta, leia:
1. `.env` na raiz → existe `APIFY_API_TOKEN`?
2. `meus-produtos/{ativo}/entregas/pesquisa-nicho/config.json` → existe?
3. `meus-produtos/{ativo}/entregas/pesquisa-nicho/{slug}/dashboard.html` → existe?

---

#### Cenario A. Pesquisa ja configurada (config.json e dashboard existem)

```
Pesquisa de mercado Instagram ja esta configurada.

O que quer fazer?

1. Abrir o dashboard agora
2. Atualizar os dados (rodar novamente)
3. Editar hashtags ou parametros
4. Criar pesquisa para outro nicho
```

**Opcao 1:** abrir o dashboard.html no navegador.
**Opcao 2:** rodar o script novamente.
**Opcao 3:** editar config.json com Edit cirurgico.
**Opcao 4:** seguir Cenario B para novo slug.

---

#### Cenario B. Primeira configuracao

**1. Token Apify**
Se `APIFY_API_TOKEN` estiver no `.env`: usar diretamente.
Se nao: executar a skill `configurar-apify` e retornar.

**2. Entrevista (3 perguntas, UMA por vez)**

Pergunta 1:
```
Qual o nicho que quer pesquisar?
(ex: emagrecimento, tarot, marketing digital, confeitaria)
```

Pergunta 2:
```
Me diga 5 hashtags em portugues que representam esse nicho.
(ex: #emagrecimento, #perderpeso, #vidasaudavel, #dieta, #corposaudavel)
```

Pergunta 3:
```
Agora 5 hashtags em ingles do mesmo nicho.
(ex: #weightloss, #fatloss, #healthylifestyle, #fitnessmotivation, #bodypositive)
```

Opcional:
```
Tem algum perfil que ja conhece e quer incluir na pesquisa? (pode pular)
```

**3. Gerar config.json**

Gerar o slug a partir do nicho (lowercase, sem acentos, hifen no lugar de espaco).
Salvar em `meus-produtos/{ativo}/entregas/pesquisa-nicho/config.json`:

```json
{
  "slug": "emagrecimento",
  "hashtagsBR": ["emagrecimento", "perderpeso", "vidasaudavel", "dieta", "corposaudavel"],
  "hashtagsMundo": ["weightloss", "fatloss", "healthylifestyle", "fitnessmotivation", "bodypositive"],
  "perfisSemente": [],
  "minSeguidores": 1000
}
```

---

### PASSO 1. Confirmacao

```
Configuracao da pesquisa:

- Nicho: {nicho}
- Hashtags BR: {lista}
- Hashtags Mundo: {lista}
- Perfis semente: {lista ou nenhum}
- Minimo de seguidores: 1.000

Custo estimado no Apify: US$ 1-2 por execucao.
Tempo estimado: 10-20 minutos.

1. Tudo certo, pesquisar agora
2. Quero ajustar algo
```

---

### PASSO 2. Executar

```bash
python .claude/skills/pesquisa-mercado-instagram/scripts/pesquisar.py --abrir
```

macOS / Linux: `python3 ...`

Aguardar conclusao (pode levar 10-20 minutos dependendo do numero de perfis encontrados).

---

### PASSO 3. Entrega

```
Pesquisa de mercado concluida.

Arquivos:
- Dashboard: meus-produtos/{ativo}/entregas/pesquisa-nicho/{slug}/dashboard.html
- Dados:     meus-produtos/{ativo}/entregas/pesquisa-nicho/{slug}/insights.json
- Log:       meus-produtos/{ativo}/entregas/pesquisa-nicho/{slug}/log.txt

Para atualizar:
python .claude/skills/pesquisa-mercado-instagram/scripts/pesquisar.py --abrir
```

## Regras

- Sempre ler `.env` antes de pedir o token Apify. Se presente, usar direto.
- Cada pesquisa de nicho fica em subpasta separada pelo slug.
- Dashboard em HTML puro. Sem libs externas alem de Google Fonts.
- Nao usar travessao em nenhum texto do dashboard.
- Fotos de perfil sempre em base64 (CDN do Instagram bloqueia HTML local).
- Separacao BR/Mundo feita pela origem da hashtag (hashtags BR → perfil BR).
- Perfis que aparecem em ambos os grupos ficam como BR.

## Proximos Passos Apos Pesquisar

- `/instagram-dashboard` para monitorar um dos perfis descobertos em detalhes
- `/copy-carrossel` para criar conteudo baseado nos padroes encontrados
- `/copy-anuncio` para criar anuncios com angulos validados pelo nicho
- `/produto-concepcao` para usar os dados na concepcao de produto
