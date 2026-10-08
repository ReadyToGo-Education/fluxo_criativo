---
name: dados-instagram
description: >
  Analisa um perfil do Instagram coletando dados públicos dos posts recentes
  (tipo, legenda, engajamento, horário, temas) e entrega um dashboard HTML
  interativo com filtros + um relatório escrito em markdown com insights
  acionáveis de conteúdo. Serve pra auditar o próprio perfil ou estudar
  concorrentes.
---

# Dados Instagram. Análise de Perfil com Dashboard

Pega um perfil do Instagram público e entrega duas coisas: um dashboard HTML interativo com filtros (tipo de post, engajamento, tema) e um relatório escrito com insights práticos. O aluno pode usar pra auditar o próprio perfil e descobrir o que funciona, ou pra estudar um concorrente e identificar padrões.

## Quando Usar

- Quando o aluno disser "analisa meu Instagram", "quero entender o que funciona no meu perfil", "estuda o perfil @fulano", "o que os concorrentes estão postando".
- Como input pra `/copy-carrossel` (insights viram ideias de conteúdo).

## O Que Fazer

### 0. Contexto

Leia `meus-produtos/.ativo`, `meus-produtos/{ativo}/perfil.md` e `meus-produtos/{ativo}/idconsumidor.md` (se existir).

### 1. Entrevista (uma pergunta por vez)

**Pergunta 1. Qual o @ do perfil?**
(aceitar com ou sem @)

**Pergunta 2. O objetivo é auditar o próprio perfil ou estudar um concorrente?**
1. Meu perfil
2. Concorrente ou referência
3. Vários perfis (fazer um de cada vez)

**Pergunta 3. Quantos posts recentes analisar?**
(padrão 30, pode ser 20 ou 50)

### 2. Coletar dados

**Passo 0. Verificar dados existentes (prioridade máxima).**
Antes de qualquer estratégia de coleta, verifique na ordem:

1. `meus-produtos/{ativo}/entregas/instagram-dashboard/insights.json` (gerado pelo `/instagram-dashboard`)
2. `meus-produtos/{ativo}/entregas/dados/instagram-{perfil}.json` (gerado por execução anterior do `/dados-instagram`)

Se qualquer um existir: leia o arquivo, extraia `perfil` e `posts`, e pule direto para o Passo 3 (Processar os dados). Informe ao aluno: "Usando dados já coletados ({n} posts, última atualização {data})."

Só siga para as estratégias abaixo se nenhum dos dois existir ou estiverem vazios.

---

A API oficial do Instagram não permite scraping de perfis públicos sem autenticação. Use uma das três estratégias, na ordem:

**Estratégia A. WebSearch por ferramentas públicas.**
Faça buscas como:
- `"inflact.com" {perfil}`
- `"picuki.com/profile/" {perfil}`
- `"inbeat.co/profile" {perfil}`
- `{perfil} engagement rate instagram`

Se encontrar bio, seguidores e alguns posts, use esses dados.

**Estratégia B. Pedir export ao aluno.**
Se o perfil é do próprio aluno, peça pra ele ir em:
- Instagram > Settings > Insights (pro conta profissional)
- Ou usar uma ferramenta gratuita tipo `metricool.com`, `notjustanalytics.com`
- Exportar como CSV com as colunas: data, tipo (Reel/Carrossel/Imagem), legenda, curtidas, comentários, salvamentos, alcance
- Colar o CSV ou o caminho do arquivo

**Estratégia C. Colagem manual.**
Se as outras duas falharem, peça pro aluno abrir o perfil no navegador, copiar as 30 legendas mais recentes com curtidas e comentários e colar no chat em formato livre. Processe o que vier.

### 3. Processar os dados

Calcule:
- **Taxa de engajamento média**: `(curtidas + comentários) / seguidores * 100`
- **Engajamento por tipo de post**: média separada pra Reel, Carrossel e Imagem
- **Melhor horário de postagem**: agrupar posts por faixa de horário (manhã, tarde, noite, madrugada) e comparar engajamento médio de cada faixa
- **Temas recorrentes**: extrair 10 a 15 palavras-chave das legendas (ignorar stopwords em português), agrupar em 3 a 5 temas
- **Top 3 posts**: maior engajamento absoluto
- **Bottom 3 posts**: menor engajamento

### 4. Gerar o dashboard HTML

Arquivo: `meus-produtos/{ativo}/entregas/dados/instagram-{perfil}.html`

Estrutura:
- `<header>`: @ do perfil, bio curta, foto placeholder, seguidores, taxa de engajamento
- `<section class="cards">`: 4 cards grandes com: total de posts, engajamento médio, melhor tipo, melhor horário
- `<section class="grafico">`: gráfico de barras em Canvas puro mostrando engajamento por post (30 barras)
- `<section class="filtros">`: 3 selects (tipo, tema, faixa de engajamento) que filtram a tabela abaixo
- `<section class="tabela">`: tabela com data, tipo, tema, legenda curta (primeiras 80 caracteres), curtidas, comentários
- `<section class="insights">`: bullets com os insights principais

Tudo em CSS inline e JS vanilla. Design system Fluxo Criativo: fundo `#000000`, surface `#111111`, borda `#252525`, texto `#e8e8e6`, muted `#a8a8a3`, neon `#c4ff5e` como cor de destaque principal. Fontes JetBrains Mono + Space Grotesk via Google Fonts. Cards com `border-top:2px solid`, sem sombra, sem border-radius.

**OBRIGATORIO:** os dados dos posts devem ser embutidos diretamente no HTML como variável JS (`var dados = [...];`), nunca via `fetch()` de arquivo externo. Arquivos abertos via `file://` bloqueiam `fetch()` por CORS na maioria dos browsers. O HTML deve ser autossuficiente.

### 5. Gerar o relatório escrito

Arquivo: `entregas/{ativo}/dados/instagram-{perfil}.md`

Estrutura:
```markdown
# Análise @{perfil}

Data: {data}
Posts analisados: {n}

## Visão geral
- Seguidores: {n}
- Taxa de engajamento: {%}
- Posts analisados: {n}
- Média de curtidas: {n}
- Média de comentários: {n}

## O que está funcionando (top 3)
1. {post 1 + por que}
2. {post 2 + por que}
3. {post 3 + por que}

## O que não está funcionando (bottom 3)
1. {post 1 + por que}
2. {post 2 + por que}
3. {post 3 + por que}

## Padrões identificados
- {padrão 1}
- {padrão 2}
- ...

## Insights acionáveis
1. {insight com ação específica}
2. ...

## Sugestões de conteúdo pra próxima semana
1. {sugestão baseada no que funciona + Urgências Ocultas do perfil do produto}
2. ...
```

### 6. Aprovação e entrega

Mostre o relatório resumido e o link do dashboard. Peça:
```
1. Aprovar e salvar
2. Quero ajustar algo
```

Após aprovação, salve os três arquivos e mostre:
```
Pronto. Análise do @{perfil} salva.

Dashboard:   entregas/{ativo}/dados/instagram-{perfil}.html
Relatório:   entregas/{ativo}/dados/instagram-{perfil}.md
Dados brutos: entregas/dados/instagram-{perfil}.json

Abra o dashboard no navegador pra ver os gráficos e filtros.

Próximos passos:
- Use os insights em /copy-carrossel pra criar conteúdo alinhado ao que funciona
- Rode /dados-nicho pra descobrir mais perfis de referência no seu nicho
```

**Regra de salvamento do JSON:** salvar `entregas/dados/instagram-{perfil}.json` somente quando os dados foram coletados via Estratégia A, B ou C (ou seja, quando o Passo 0 não encontrou dados existentes). Se o Passo 0 usou dados do `instagram-dashboard` ou de uma execução anterior, não sobrescrever o JSON existente.

## Regras

- Nunca usar scraping que viole termos de serviço do Instagram.
- Dashboard em HTML puro, sem libs externas. JS vanilla, gráficos em Canvas ou SVG.
- Filtros funcionam 100% no cliente.
- Relatório escrito precisa ter 5 a 10 insights acionáveis, não apenas descritivos.
- Se não conseguir coletar dados, não invente números. Avise o aluno e peça export manual.
- Não usar travessão em nenhum texto exibido.
