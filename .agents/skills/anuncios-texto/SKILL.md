---
name: anuncios-texto
description: >
  Base de conhecimento para criacao de anuncios estaticos (imagem + copy).
  Inclui formatos de imagem, estrutura de copy, exemplos de criativos e especificacoes
  tecnicas para Meta Ads e Google Ads. Focado em anuncios que nao usam video.
---

# Anuncios de Texto e Imagem. Base de Conhecimento

Criativos estaticos: imagem + copy. Para anuncios em video, consulte a skill `anuncios-video`.

## Quando Usar Esta Skill

- Anuncios de feed com imagem estatica
- Anuncios de carrossel (multiplas imagens)
- Anuncios da rede de pesquisa do Google (somente texto)
- Banners e criativos para remarketing
- Thumb chamativa (estilo YouTube thumbnail, expressao exagerada)
- Criativo estatico com design (peca grafica estruturada — headline + visual + CTA)
- Qualquer anuncio que NAO envolva video

## Tres Caminhos de Execucao para Imagens

**Caminho 1 — Geracao via Freepik (Magnific) AI (API automatica)**
Requer `FREEPIK_API_KEY` no `.env`.
O sistema gera o prompt e chama a API automaticamente apos aprovacao.

**Caminho 2 — Geracao via prompt em ferramenta externa**
O sistema gera o prompt no formato nativo da ferramenta escolhida.
Ferramentas suportadas: Midjourney (premium), DALL·E via Bing (gratis), Whisk, Ideogram, ImageFX, Leonardo, Krea.
Use `/criativo-estatico` (modo "prompt") para entregar um prompt consolidado em ingles pronto para colar.

**Caminho 3 — Direcao criativa para designer ou Canva**
O sistema entrega: briefing completo (conceito + composicao + paleta HEX + tipografia + instrucoes passo a passo para o Canva).
Inclui prompt de IA para gerar o visual de fundo separadamente, se necessario.

## Tipos de Criativo de Imagem

| Tipo | Descricao | Quando Usar |
|---|---|---|
| **Imagem para anuncio** | Feed (1:1 ou 4:5), Stories (9:16) | Anuncio pago Meta Ads |
| **Post Instagram** | Feed ou carrossel com identidade visual | Conteudo organico ou patrocinado |
| **Capa de conteudo** | YouTube, blog, modulo de produto | Thumbnails e capas digitais |
| **Banner de pagina** | Hero, secao especifica, CTA visual | Pagina de vendas |
| **Thumb chamativa** | Expressao exagerada, fundo colorido, texto bold curto | Thumbnail YouTube ou post de alto impacto |
| **Criativo estatico com design** | Peca grafica estruturada com hierarquia visual completa | Anuncio de alta qualidade |

## Os 18 Tipos de Anuncios VTSD (Aplicados a Imagem)

1. **Comparacao**. Imagem dividida: antes vs depois, errado vs certo
2. **Problema/Solucao**. Imagem de problema + solucao visual
3. **Explicacao**. Infografico ou imagem didatica
4. **Curiosidade**. Imagem intrigante + headline que gera duvida
5. **Reflexao**. Imagem minimalista + frase de impacto
6. **Certo/Errado**. Layout de duas colunas com X e check
7. **Demonstracao**. Screenshot, print de resultado, tutorial visual
8. **Procedimento**. Passo a passo visual, checklist
9. **Impacto Visual**. Imagem forte e impactante que para o scroll
10. **Oportunidade**. Imagem de dados/graficos + copy reveladora
11. **Historia**. Foto pessoal + copy narrativa
12. **Prova Social**. Print de depoimento, resultado, faturamento
13. **Clickbait**. Imagem chamativa + headline provocativa
14. **Sensacao**. Imagem sensorial que desperta emocao
15. **Contraste**. Imagem split-screen com contraste visual forte
16. **Ensino**. Conteudo didatico, dica util aplicada a imagem
17. **Revelacao**. Imagem que contradiz crenca popular ou revela algo inesperado
18. **Dilema**. Imagem com duas opcoes visuais

## Aplicação interna de Elementos Literários (OBRIGATÓRIO. não exibir ao usuário)

Depois que o tipo da Mandala estiver definido e ANTES de gerar a copy, acionar internamente a skill `elementos-literarios` e escolher de **1 a 3 elementos** que mais combinarem com o tipo de anúncio escolhido, com o perfil do consumidor e com o tom do produto.

Regras:
- Esse processo é silencioso. **Não mencionar ao usuário** quais elementos foram escolhidos, nem que a skill foi consultada.
- Os 1 a 3 elementos selecionados devem ser efetivamente aplicados na copy gerada (gancho, desenvolvimento ou CTA), não apenas listados.
- A escolha precisa fazer sentido com o tipo da Mandala (ex.: Comparacao combina com antitese; Historia combina com setup/punchline; Reflexao combina com aforismo; Curiosidade combina com neologismo ou jogo de palavras; Sensacao combina com hiperbole controlada).
- Continuar respeitando todas as proibicoes de Light Copy.
- Nao exibir rotulos como "elemento usado: X" no entregavel final.

## Estrutura de Copy para Anuncio Estatico

**Texto principal (Light Copy):**
- Gancho (premissa nao obvia) — 1 a 2 linhas fortes
- Desenvolvimento — MINIMO 2 paragrafos substanciais. Cada paragrafo deve aprofundar o argumento com especificidade, dado concreto ou insight nao obvio. O leitor precisa aprender ou se reconhecer so de ler o texto, mesmo sem clicar. Raso, curto e generico sao proibidos.
- CTA direto — 1 linha

**Regras VTSD (Light Copy):**
- Sem ponto de exclamacao
- Sem perguntas no gancho
- Sem "mesmo que" / "sem precisar" como muletas
- Sem promessas vagas
- Sem premissa obvia para quem ja esta no nicho
- Argumentativo e logico
- Baseado em premissas, nao promessas
- Sem travessão longo (. ): substituir por vírgula, ponto ou reformulação
- Sem estrutura "Não é X. É Y.": reformular de forma mais elaborada
- Sem frases genéricas de vendedor: "Transforme sua vida", "Descubra o segredo"
- O produto não aparece nos primeiros parágrafos
- Sem emojis na copy
- Nomear conceitos: criar nomes próprios quando possível ("Negociação Terapêutica" > "Método Exclusivo")
- Especificidade: usar números concretos, situações reais. "R$ 1.600" > "muito dinheiro"

**Checklist obrigatório. revisar antes de entregar qualquer copy:**

Antes de entregar, revise e substitua:
- Travessão (. ) → reescreva a frase sem ele
- Estrutura "Não é X. É Y." → desenvolva o argumento de outra forma
- Frases genéricas de vendedor → substitua por dado ou situação concreta
- Menção ao produto nos primeiros parágrafos → remova ou reescreva focando no leitor
- Emojis → remova sem substituição
- Desenvolvimento com menos de 2 parágrafos → expanda com argumento concreto e valor real

- [ ] Nenhum travessão no texto
- [ ] Nenhuma estrutura "Não é X. É Y."
- [ ] Nenhuma frase genérica de vendedor
- [ ] Desenvolvimento tem mínimo 2 parágrafos com valor real entregado

**Regra do Gancho. NUNCA pergunta, NUNCA obvio:**

ERRADO:
- "Voce ja sentiu dificuldade de..." (pergunta)
- "Aprender [tema] e dificil." (obvio)

CERTO:
- Afirmacao que surpreende quem ja esta no universo do produto
- Premissa contra-intuitiva ou revelacao inesperada

**Headline:** maximo 40 caracteres
**Descricao:** maximo 90 caracteres
**Texto visivel sem "ver mais":** ate 125 caracteres

## Formatos e Especificacoes Tecnicas

### Meta Ads (Facebook/Instagram)

| Formato | Dimensao | Uso |
| --- | --- | --- |
| Feed quadrado | 1080x1080 | Post patrocinado, carrossel |
| Feed paisagem | 1200x628 | Link ads, remarketing |
| Stories | 1080x1920 | Anuncios de stories |
| Carrossel | 1080x1080 (cada card) | Ate 10 cards |

**Zona segura de texto:** Manter texto nos 80% centrais da imagem (evitar cortes no mobile).

**Regra de texto na imagem:** Facebook permite texto, mas criativos com menos de 20% de texto performam melhor.

### Google Ads (Rede de Pesquisa)

| Elemento | Quantidade | Limite |
| --- | --- | --- |
| Titulos | ate 15 | max 30 chars cada |
| Descricoes | ate 4 | max 90 chars cada |
| URL de exibicao | 2 caminhos | max 15 chars cada |

**Palavras-chave negativas obrigatorias:** gratis, download, torrent, emprego, vaga

**Tipos de correspondencia:**
- Exata: [palavra]. maior controle
- Frase: "palavra". equilibrio
- Ampla: palavra. maior alcance (usar com cuidado)

## Exemplos de Criativos Estaticos

### Carrossel de Dores (5 slides)
1. Headline de impacto
2. Dor 1 com descricao emocional
3. Dor 2 com consequencia
4. Dor 3 com agitacao
5. Solucao + CTA

### Antes x Depois
- Lado esquerdo: situacao de dor (visual cinza)
- Lado direito: resultado (visual colorido)
- Headline conectando os dois

### Depoimento em Destaque
- Foto do cliente ou screenshot
- Headline: resultado especifico
- Trecho do depoimento entre aspas
- CTA: "Quero o mesmo resultado"

### Lista de Beneficios
- Headline chamativa
- 5-7 beneficios com icones
- Destaque no beneficio principal
- CTA no rodape

### Revelacao/Segredo
- Headline: "O que [autoridades] nao te contam sobre [tema]"
- Imagem intrigante
- Texto parcial que gera curiosidade
- CTA: "Descubra o metodo completo"

### Comparacao Visual
- Coluna 1: "O jeito comum" (X com problemas)
- Coluna 2: "O [Seu Metodo]" (check com beneficios)
- Headline: "Ainda fazendo do jeito antigo?"

### Thumb Chamativa (alto impacto)
- Expressao facial exagerada (surpresa, choque, incredulidade)
- Fundo solido de cor forte (amarelo, vermelho, azul-eletrico)
- Texto maximo 5 palavras em bold, fonte sem serifa, tamanho gigante
- Elemento de atencao: seta, circulo, ponto de interrogacao grande
- Rosto em close ou 3/4

### Criativo Estatico com Design (peca grafica estruturada)
- Hierarquia visual clara: headline principal + subhead + CTA
- Composicao definida (ex: "60% imagem a esquerda, 40% texto fundo escuro a direita")
- Paleta consistente com identidade do produto (HEX definido)
- Texto overlay com fonte bold, contraste alto
- Indicacao de montagem no Canva ou Adobe Express

## Diretrizes de Design

**Cores por objetivo:**
- Vermelho/Laranja: urgencia, CTAs, promocoes
- Azul: confianca, autoridade
- Verde: saude, dinheiro, resultados
- Amarelo: atencao, destaque
- Preto/Dourado: premium, exclusividade

**Tipografia:**
- Titulos: bold, grande, sem serifa
- Corpo: legivel, minimo 16pt para mobile
- Maximo 2 fontes por criativo

**Regra dos 3 Segundos:**
Em 3 segundos o espectador decide se para ou continua scrollando. Ele precisa:
1. Entender PARA QUEM e
2. Sentir que e RELEVANTE
3. Ter CURIOSIDADE de saber mais

## CTAs por Fase (Mandala da Criatividade)

| Objetivo | Definicao | CTA tipico |
| --- | --- | --- |
| Descoberta | Atrair novas pessoas que ainda nao conhecem o produto | Seguir, curtir, comentar, compartilhar |
| Relacionamento | Criar conexao e autoridade com quem ja segue | Comentar, DM, salvar, lives |
| Conversao | Vender | Comprar agora, garantir vaga, quero comecar |
| RMKT | Converter quem ja viu a pagina de vendas | Comprar agora, retomar oferta, ultima chance |

---

## Geracao Automatica de Imagens (Freepik (Magnific) API)

O comando `/copy-anuncio` gera a copy e, se configurado, cria as imagens automaticamente via Freepik (Magnific).

### Configuracao necessaria no `.env`

```
FREEPIK_API_KEY=sua_chave_aqui
```

Para obter: freepik.com/api > Create API Key

### Parametros de tamanho por formato

| Formato | Parametro `size` |
| --- | --- |
| Feed quadrado (1:1) | `square_1_1` |
| Stories / Reels (9:16) | `portrait_9_16` |
| Feed horizontal (1.91:1) | `landscape_16_9` |

### Estrutura do prompt de imagem

Para cada variacao, o prompt deve descrever:
1. **Estilo fotografico**: foto real de pessoa, fundo clean, mockup, infografico, flat design
2. **Composicao**: plano americano, close, vista aerea, split-screen
3. **Paleta**: cores alinhadas ao nicho do produto
4. **Texto overlay**: headline da variacao, centralizado, fonte bold
5. **Mood**: profissional, acolhedor, urgente, premium (baseado no objetivo)

Exemplo de prompt bem formado:
```
Professional lifestyle photo of a woman studying at a clean desk, natural light from window, warm tones, text overlay "Aprenda [Tema do Produto] em 30 dias" in bold white font centered, minimal background, Instagram feed format, 1:1 aspect ratio, soft shadow, high quality
```

### Carrossel. um prompt por card

Cada card deve ter prompt individual com identidade visual consistente entre todos os slides:
- **Card 1 (Gancho)**: elemento visual de impacto, headline grande, fundo de contraste
- **Cards do meio (Conteudo)**: layout limpo, texto legivel, icone ou ilustracao simples
- **Card final (CTA)**: cor de destaque, call to action centralizado, logotipo ou nome do produto

**Regra de consistencia**: incluir no prompt de cada card a mesma descricao de paleta e estilo para manter identidade visual uniforme no carrossel.
