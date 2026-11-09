# Copy Variacao Post. Variacoes de Conteudo Validado pelo Algoritmo

## Quando Usar

- Quando o perfil ja tem historico de publicacoes e o dashboard foi gerado.
- Para criar novas versoes de posts que ja funcionaram, sem inventar angulos do zero.
- Como acelerador: em vez de partir das urgencias ocultas, parte de prova social do proprio algoritmo.

**Diferenca em relacao ao `/copy-carrossel`:**

| `/copy-carrossel` | `/copy-variacao-post` |
|---|---|
| Cria conteudo do zero a partir das urgencias ocultas | Cria variacoes de posts que ja tiveram alto engajamento |
| Qualquer perfil, qualquer nicho | Depende do `insights.json` gerado pelo `/instagram-dashboard` |
| Fonte: metodologia VTSD | Fonte: dados reais do algoritmo + metodologia VTSD |

## O Que Entrega

Para cada post selecionado: 3 variacoes com elementos literarios diferentes, formato escolhido pelo usuario, e caption com hashtags.

Salvo em: `meus-produtos/{ativo}/entregas/criativos/variacoes-[slug].md`

---

## Fluxo

### PASSO 0. Verificar insights.json

Leia `meus-produtos/{ativo}/entregas/instagram-dashboard/insights.json`.

Se nao existir:
```
O dashboard do Instagram ainda nao foi configurado ou nao gerou o arquivo de insights.

Use /instagram-dashboard para configurar e atualizar os dados primeiro.
```

Se existir, mostre o resumo:
```
Dashboard: @{perfil} — atualizado em {gerado_em}
Seguidores: {seguidores} | Engajamento medio: {avg_eng_pct}%
Formato top: {formato_top}

Top 10 posts por engajamento:

#1  [Reels] 12.28%  —  "caption truncada em 80 chars"
    Transcricao disponivel: "primeiras 15 palavras da transcricao..."
#2  [Carrossel] 2.86%  —  "caption truncada em 80 chars"
    Slides disponiveis: 3 para analise visual
#3  [Foto] 1.50%  —  "caption truncada em 80 chars"
    (somente caption disponivel)
...
```

Regra de exibicao: para cada post do top 10, mostre o indicador de conteudo disponivel:
- Reels com transcricao: exibir as primeiras 15 palavras da transcricao
- Carrossel com carouselSlides: exibir "Slides disponiveis: {N} para analise visual"
- Posts sem dados extras: exibir "(somente caption disponivel)"

### PASSO 1. Selecao dos Posts Base

```
Quais posts quer usar como base para as variacoes?

Digite os numeros separados por virgula (ex: 1, 3) ou "todos" para usar o top 5:
```

Aceitar: numeros individuais (1), lista (1,3,5), intervalo (1-3), "todos" (usa top 5).

```
--- Bloco 1/3 concluido ---
Posts selecionados: #{numeros} ({tipos})
Proximo: Formato de saida
---
```

### PASSO 2. Configuracao

**Bloco 2/3. Formato de saida:**

```
Em qual formato quer as variacoes?

1. Mesmo formato dos originais
2. Roteiro de Reels
3. Carrossel (slides)
4. Caption (post estatico ou foto)
5. Mix (cada variacao num formato diferente)

Digite o numero:
```

```
--- Bloco 2/3 concluido ---
Posts base: #{numeros}
Formato: {formato escolhido}
Proximo: Objetivo
---
```

**Bloco 3/3. Objetivo:**

```
Qual o objetivo principal das variacoes?

1. Educar (ensinar algo pratico — alto salvamento)
2. Engajar (gerar comentarios e compartilhamentos)
3. Vender (levar para pagina/checkout)
4. Atrair seguidores (crescer a base)

Digite o numero:
```

**Confirmacao antes de gerar:**

```
Resumo do que vou criar:

Posts base: {lista dos posts com tipo e engajamento}
Formato de saida: {formato}
Objetivo: {objetivo}
Variacoes por post: 3 (cada uma com elemento literario diferente)

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### PASSO 3. Transcricao de Reels (sob demanda)

Antes de analisar, identifique quais posts selecionados sao Reels com `transcricao` vazia no `insights.json`.

Se houver ao menos um:

```
Encontrei {N} Reel(s) sem transcricao nos posts selecionados.
Vou buscar o audio agora para melhorar a analise. Isso leva ~1 min por Reel.
```

Execute para cada shortcode de Reel sem transcricao:
```bash
python .claude/skills/copy-variacao-post/scripts/transcrever.py {shortcode1} {shortcode2} ...
```

Aguarde a conclusao e releia o `insights.json` atualizado antes de prosseguir.

Se nenhum Reel selecionado tiver transcricao vazia, pule direto para o PASSO 4.

### PASSO 4. Analise do Post Original

Para cada post selecionado, antes de gerar as variacoes, identifique internamente usando os dados disponiveis no insights.json:

**Se tipo = Reels e campo `transcricao` disponivel:**
- Ler a transcricao e identificar: abertura exata (primeiras 2-3 frases), argumento central, CTA final
- Classificar o tom: didatico, emocional, provocativo, humor, historia pessoal
- Identificar o gancho real: o que foi dito nos primeiros 3 segundos (geralmente as primeiras 1-2 frases da transcricao)
- Usar a transcricao como fonte primaria. A caption e secundaria.

**Se tipo = Carrossel ou Foto e campos `thumbnailPath` ou `carouselPaths` disponiveis:**
- Usar o Read tool nos caminhos de arquivo listados em `carouselPaths` (ou `thumbnailPath` se for Foto) para visualizar as imagens
- Analisar visualmente: tema visual, texto nos slides, sequencia de argumento, elementos graficos de destaque
- Combinar com a caption para entender a narrativa completa
- Identificar o angulo do primeiro slide (gancho visual) e o argumento que se desenvolve nos slides seguintes
- Os caminhos em `carouselPaths` sao relativos ao projeto. Construir o caminho absoluto concatenando a raiz do projeto (detectada pelo diretorio de trabalho atual) com o caminho relativo do arquivo. Exemplo: `Read("{raiz-do-projeto}/entregas/instagram-dashboard/imagens/slide-6-1.jpg")`
- Para saber o diretorio do projeto, ler `meus-produtos/.ativo` ou verificar o caminho do `insights.json` que foi lido no PASSO 0

**Se nenhum dado visual ou de transcricao disponivel (caption curta ou vaga):**
- Inferir o angulo central pela caption + engajamento + tipo de conteudo
- Hipotese sobre o motivo do alto engajamento: identificacao, curiosidade, utilidade, polemica suave, nostalgia

Em todos os casos, registrar internamente:
1. **Angulo central:** qual ideia ou tensao esta no nucleo do post
2. **Estrutura da abertura:** como comeca (afirmacao, confissao, dado, cena, revelacao)
3. **Tom:** humoristico, reflexivo, didatico, provocativo, emocional
4. **Por que funcionou:** hipotese sobre o motivo do alto engajamento

Essa analise interna guia as 3 variacoes: cada uma preserva o angulo central mas muda a estrutura de abertura, o tom e o elemento literario aplicado.

### PASSO 5. Geracao das Variacoes

Para cada post selecionado, gere 3 variacoes numeradas.

**Estrutura de cada variacao:**

```
--- Variacao {N} do Post #{posicao_original} ---
Elemento literario: {nome do elemento}
Formato: {Reels / Carrossel / Caption}
Objetivo: {objetivo escolhido}

[CONTEUDO COMPLETO AQUI]

Caption:
[legenda completa com hashtags]
---
```

**Regra dos elementos literarios:** cada variacao usa um elemento diferente. Escolher entre os mais adequados ao objetivo:
- **Educar:** Paradoxo, Estatistica, Analogia, Antitese, Anafora
- **Engajar:** Confissao, Pergunta Retorica no corpo (nunca no gancho), Hiperbole controlada, Ironia
- **Vender:** Prova Social, Urgencia, Escassez Narrativa, Transformacao
- **Atrair seguidores:** Historia Pessoal, Revelacao, Identidade Compartilhada

**Regras de geracao (Light Copy):**

**Fonte unica e obrigatoria:** antes de escrever qualquer variacao, leia `.claude/skills/revisora/references/manual-copy.md`. Principio central, **15 principios**, **20 vicios proibidos** e **checklist Blocos A/B/C/D** vivem la. Toda variacao passa pelo `revisora` antes de ir ao usuario.

**Reforcos especificos de variacao de post:**
- **Preservar o angulo central do post original.** O que muda e a estrutura, o tom e o elemento literario. Se o angulo mudar, nao e variacao, e post novo.
- **Gancho nao pode ser pergunta nem frase obvia.** Cada variacao usa um elemento literario diferente na abertura (paradoxo, confissao, dado, cena, revelacao).
- **Entregar valor real dentro do proprio post/video.** Cada variacao ensina, revela ou provoca uma virada de perspectiva. Conteudo que so promete sem entregar nao e publicado.
- **Produto nao aparece nos primeiros slides / 3s.** So aparece depois de estabelecer a tese ou no slide/momento de CTA.
- **Uma ideia por variacao.** Cada variacao defende UMA tese e leva a UM CTA. Nao empilhar topicos.

**Profundidade obrigatoria:**
- Gancho: afirmacao nao obvia, contra-intuitiva ou especifica. NUNCA pergunta. NUNCA generico.
- Desenvolvimento: minimo 2 paragrafos substanciais com argumento, ensinamento ou insight concreto
- O conteudo entrega valor por si so: quem le aprende algo, tem virada de perspectiva ou se reconhece

**Estrutura por formato:**

Roteiro de Reels (~45-60s):
```
[0-3s]   GANCHO    — Afirmacao contra-intuitiva. Texto na tela + fala simultaneos.
[4-15s]  TEASE     — Expande o gancho, contextualiza o problema.
[16-42s] ENTREGA   — Ensina, demonstra ou revela algo concreto. Nunca so promete.
[43-48s] REGANCHO  — Texto na tela sintetizando a ideia central.
[49-55s] CTA       — Convite direto e leve.
```

Carrossel (7-10 slides):
- Slide 1: Gancho forte (elemento literario escolhido)
- Slides 2-8: conteudo que avanca o argumento, nao repete o anterior
- Slide final: CTA + identidade visual
- Caption: minimo 2 paragrafos + hashtags

Caption (post estatico):
- Abertura: gancho de 1-2 linhas
- Desenvolvimento: 2-3 paragrafos com o argumento completo
- CTA no final
- Hashtags

**Checklist antes de entregar cada variacao:** rodar pela `revisora` (Blocos A/B/C/D do `manual-copy.md`). Em caso de duvida, consultar diretamente `.claude/skills/revisora/references/manual-copy.md`.

### PASSO 6. Aprovacao e Salvamento

Apresente todas as variacoes geradas e pergunte:

```
1. Aprovar e salvar
2. Quero ajustar algo
```

Apos aprovacao, salve em:
`meus-produtos/{ativo}/entregas/criativos/variacoes-{slug-produto}-{data}.md`

Formato do arquivo:
```markdown
# Variacoes de Posts Validados — {nome do produto}
Gerado em: {data}
Dashboard base: @{perfil} ({gerado_em do insights.json})

---

## Post Base #1
Tipo: {tipo} | Engajamento original: {eng}% | Data: {data}
Caption original: "{caption}"
URL: {url}

### Variacao 1.1 — {Elemento Literario}
...

### Variacao 1.2 — {Elemento Literario}
...

### Variacao 1.3 — {Elemento Literario}
...

---

## Post Base #2
...
```

### PASSO 7. Proximo Passo

```
Variacoes salvas em meus-produtos/{ativo}/entregas/criativos/variacoes-{slug}-{data}.md

Proximos passos:
- /criativo-estatico para gerar as artes dos carrosseis
- /copy-anuncio para transformar os angulos validados em anuncios pagos
```

---

## Regras

- Nunca gerar variacao sem antes ler o `insights.json`. Sem ele, o fluxo nao tem base de dados.
- O angulo central do post original deve ser preservado nas 3 variacoes. O que muda e a estrutura, o tom e o elemento literario.
- Cada variacao precisa ser completamente diferente da anterior. Proibido trocar so palavras do gancho.
- Aplicar checklist Light Copy antes de mostrar qualquer variacao ao usuario.
- Nunca mostrar o mesmo elemento literario em duas variacoes do mesmo post.
- Se o post original tiver caption curta ou vaga, inferir o angulo central a partir do engajamento e do tipo de conteudo.
