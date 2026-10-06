---
name: furadeira-visual
description: Apoio tecnico para o command /furadeira-visual. Le a Furadeira ja gerada no perfil.md, decide automaticamente o layout visual mais adequado (mecanica + nicho), e monta um prompt em ingles rico em descricao textual para o aluno colar no ChatGPT e gerar a imagem PNG. Sem entrevista.
---

# Skill. Furadeira Visual (Prompt para Imagem)

Apoio técnico do command `/furadeira-visual`. A skill lê a Furadeira já existente no `perfil.md` (gerada por `/gerar-furadeira`), decide o layout visual sozinha com base na mecânica e no nicho, monta o prompt em inglês e o entrega ao aluno para colar no ChatGPT. Depois recebe o PNG de volta e salva no projeto.

Sem entrevista. Sem perguntas opcionais. A imagem retornada será embutida no painel de entregas e na seção Método da página de vendas.

## Pré-requisitos

- `meus-produtos/{ativo}/perfil.md` precisa ter a seção "Furadeira (Método)" preenchida com **Mecânica(s)** declarada(s).
- Se faltar, parar e redirecionar para `/gerar-furadeira`. Não tentar adivinhar.

## Decisão automática do layout

A skill cruza **mecânica registrada** + **nicho** + **estilo do consumidor** e escolhe o layout visual que melhor representa o método. Ver `.claude/skills/furadeira-visual/references/metodo-visual.md` para a descrição completa de cada layout.

### Tabela de mapeamento mecânica → layout

| Mecânica registrada no perfil | Layouts compatíveis (ordem de preferência) |
|---|---|
| **Fases e Sequências** | Roadmap Vertical, Linear Horizontal, Hexágonos em Cadeia, Trilha Ondulada, Pirâmide Invertida |
| **Lógica Condicional** | Fluxograma Condicional, Régua de Comportamento |
| **Enquadramento** | Grid de Categorias, Quadrantes 2x2, Hub Numerado com Quadrantes |
| **Listas** | Hub Central / Diamante, Roda Eneagrama, Roda Octogonal, Mandala Concêntrica |
| **Empecilhos** (combinada com Fases) | Roadmap Vertical com caixas de obstáculo lateral, Linear Horizontal com bloqueios marcados |
| **Dinâmica de Entrega** (combinada) | Curva Exponencial, Régua de Comportamento, Trilha Ondulada com marcação de frequência |

### Critério de desempate por nicho

Quando mais de um layout couber, usar o nicho para decidir:

| Nicho | Preferência visual |
|---|---|
| Espiritual (tarô, astrologia, terapias) | Mandala, Roda, Hub Central. Estilo etéreo |
| Corporativo (vendas, gestão, finanças) | Linear Horizontal, Hub Numerado. Estilo limpo |
| Feminino (autoestima, maternidade) | Trilha Ondulada, Grid Categorias. Cores quentes |
| Esportivo / Saúde | Roadmap Vertical, Curva Exponencial. Cores fortes |
| Educação / Idiomas | Hexágonos em Cadeia, Pirâmide. Estilo acadêmico |
| Criativo (arte, design, escrita) | Mandala, Hub Central. Cores vibrantes |

## Paleta inferida pelo nicho

A skill escolhe a paleta sem perguntar. Cada paleta tem 1 cor dominante + 1 cor de acento + 1 cor de texto.

| Nicho | Cor dominante | Acento | Texto principal |
|---|---|---|---|
| Espiritual | Roxo profundo `#5B2A86` ou Vinho `#7A2E4B` | Dourado `#E8A200` | Branco `#FFFFFF` |
| Corporativo | Azul navy `#1A3A6B` | Dourado `#E8A200` | Branco ou cinza claro |
| Feminino | Rosa terracota `#C97064` ou Pêssego `#F4A261` | Bordô `#823038` | Marrom escuro `#3D2B1F` |
| Esportivo | Preto `#0D0D0D` | Verde-limão `#A3FF00` ou Laranja `#FF6B00` | Branco |
| Saúde / Bem-estar | Verde sálvia `#7BA098` | Terracota `#C97064` | Marrom `#3D2B1F` |
| Educação | Azul royal `#2563EB` | Amarelo `#F5A623` | Cinza grafite `#1F2937` |
| Criativo | Magenta `#D946EF` | Turquesa `#06B6D4` | Preto |
| Finanças | Verde escuro `#16A34A` | Dourado `#E8A200` | Branco |
| Tecnologia / Marketing | Azul ciano `#0EA5E9` | Roxo `#7C3AED` | Branco |
| Genérico (sem encaixe claro) | Azul royal `#2563EB` | Dourado `#E8A200` | Branco |

## Estrutura do prompt em inglês

O prompt enviado ao ChatGPT precisa ser denso em descrição textual (sem imagem de referência). A estrutura obrigatória reforça 2 pontos críticos que modelos de imagem costumam errar: **transparência do fundo** (mencionada em 4 lugares distintos) e **acentuação portuguesa** (lista de palavras-chave + exemplos certo/errado).

```
Professional flat design infographic for a method called "{nome do método}".
CRITICAL: Transparent background, PNG with alpha channel. No background color whatsoever.
The output must be a PNG with checkered transparency pattern visible behind all empty areas of the canvas.

VISUAL STYLE:
{descrição textual do layout escolhido em 4 a 6 frases — estrutura, conexões, hierarquia, espaçamento}
The canvas itself has NO background fill — the only visible elements are the infographic shapes,
text and decorative particles. Empty space between elements shows transparency, not white or any color.

METHOD CONTENT — COPY EVERY WORD EXACTLY AS WRITTEN BELOW. Do not add, translate, rephrase or shorten any label. Do NOT include any text in the infographic that is not listed here:

{conteúdo específico da mecânica:
 - Fases: cada fase numerada com nome + 1 frase
 - Condicional: a decisão crítica + as ramificações com seus protocolos
 - Enquadramento: as categorias com nomes próprios
 - Listas: os pilares com seus nomes
 - Dinâmica: o ritual com frequência e duração}

CRITICAL TEXT FIDELITY (Portuguese accents and spelling):
You will render Brazilian Portuguese text. Common rendering mistakes you must avoid:
- WRONG: "Metodo"  RIGHT: "Método"
- WRONG: "Coracao" or "coraçao"  RIGHT: "Coração"
- WRONG: "Acao"  RIGHT: "Ação"
- WRONG: "Ritual" rendered as "Rllual" or "Rilual"  RIGHT: "Ritual"
- WRONG: "Diario" or "Didrio"  RIGHT: "Diário"
- WRONG: "Audio"  RIGHT: "Áudio"
- WRONG: "Aplicacao" or "Aplicaciao"  RIGHT: "Aplicação"
- WRONG: "Maos"  RIGHT: "Mãos"
- WRONG: "Simbolo" or "simbulo"  RIGHT: "Símbolo"
- WRONG: "Bia 14"  RIGHT: "Dia 14"
- When a number appears in a label (ex: "Dia 30"), always clarify: write the digit value in words AND show the digits explicitly to prevent confusion between visually similar digits (3 vs 9, 1 vs 7, 6 vs 0). Example: "Dia 30 (thirty, not ninety — digit THREE followed by ZERO: 30)"
- WRONG: "Reiri"  RIGHT: "Reiki"
- WRONG: "voitar a ler paz"  RIGHT: "voltar a ter paz"
- WRONG: "Reussio dos sinois"  RIGHT: "Revisão dos sinais"
Render every accent exactly: á à â ã é ê í ó ô õ ú ç. Letters in Portuguese words must spell the word correctly — do not invent letters or skip syllables.

LAYOUT: {nome do layout escolhido + posicionamento dos elementos}
ICON STYLE: {outline thin / filled solid / illustrative — escolher conforme nicho}
COLOR PALETTE: {dominant: HEX, accent: HEX, text: HEX} — exatamente como inferido pelo nicho
TYPOGRAPHY: {sans-serif moderna para texto / serif clássica para nicho premium / display bold para impacto}
TONE: {corporate sober / spiritual ethereal / vibrant modern / clean academic / minimalist premium}

HARD CONSTRAINTS (must all be satisfied — these are non-negotiable):
1. TRANSPARENT BACKGROUND. Output is a PNG with alpha channel. NO white fill, NO black fill, NO colored fill, NO gradient wash behind the canvas. The image, when opened in an image editor, must show the checkered transparency pattern in all areas not covered by infographic elements. This is the most common failure mode — verify the background is transparent before finishing.
2. All visible text must be in Brazilian Portuguese (pt-BR). Never translate names, phases, categories or labels into English. Every text label must appear exactly as written in the METHOD CONTENT section above. Do NOT invent or add any word not listed there.
3. Render every accented character correctly: ã, á, â, à, é, ê, í, ó, ô, õ, ú, ç. Spell every Portuguese word exactly as in the METHOD CONTENT section above. If you are unsure how to render a word, copy it letter by letter from this prompt — do not improvise spelling. Include product-specific WRONG/RIGHT pairs for every accent-bearing word that appears in the METHOD CONTENT (e.g., "vídeos", "Após", "exercício", "lê", "Método"). Never create a pair where WRONG = RIGHT.
4. No people, no faces, no photographs, no realistic scenes, no handwriting.
5. No logos, no watermarks, no decorative frames around the full canvas.
6. Aspect ratio 4:3, minimum width 1200px.
7. Output: clean professional infographic ready for presentation slide or sales page section.

FINAL CHECK before delivering: (1) Is the background transparent with alpha channel — no white or colored fill anywhere on the canvas? If no, regenerate. (2) Is every visible word spelled exactly as in the METHOD CONTENT section above, with correct accents? If no, regenerate.
```

### Exemplo (Método 3F, mecânica Fases, nicho Educação)

```
Professional flat design infographic for a method called "Método 3F".
Transparent background, PNG with alpha channel. No background color, no background fill.

VISUAL STYLE:
Roadmap horizontal with 3 connected hexagonal nodes representing sequential phases.
Each hexagon contains a numbered badge (01, 02, 03), an icon centered above the phase name,
and a short description label below. Hexagons are connected by thin solid arrows pointing
right. The composition is balanced with generous whitespace. Modern flat aesthetic with
subtle drop shadow under each hexagon for depth.

METHOD CONTENT (keep all text exactly in Brazilian Portuguese, do not translate):

Phase 1: "Fonética" — corrigir sotaque e treinar 3 sons fundamentais
Phase 2: "Fluência" — destravar conversação com IA e role-play
Phase 3: "Fixação" — revisão espaçada e construção de vocabulário ativo

LAYOUT: Three hexagonal cards aligned horizontally with arrows between them, centered on canvas.
ICON STYLE: Outline thin icons, single color (accent), centered above each phase name.
COLOR PALETTE: dominant Royal Blue #2563EB, accent Yellow #F5A623, text Graphite #1F2937.
TYPOGRAPHY: Bold sans-serif for phase names (similar to Poppins), regular weight for descriptions.
TONE: Clean academic, professional, balanced.

HARD CONSTRAINTS:
- Transparent background (PNG with alpha channel). No white fill behind the canvas.
- All visible text must be in Brazilian Portuguese (pt-BR). Never translate.
- Render all accented characters correctly: ã, á, â, é, ê, í, ó, ç.
- No people, no faces, no photographs.
- No logos, no watermarks.
- Aspect ratio 4:3, minimum width 1200px.
```

## Caminho de salvamento

| Artefato | Caminho |
|---|---|
| Prompt em markdown | `meus-produtos/{ativo}/entregas/furadeira/prompt-furadeira.md` |
| PNG retornado pelo aluno | `meus-produtos/{ativo}/entregas/furadeira/furadeira.png` (caminho fixo, sobrescreve) |

## Limitação conhecida do ChatGPT com texto em pt-BR

Modelos de imagem (ChatGPT, Gemini, etc.) têm dificuldade real de renderizar texto em português brasileiro com acentos e palavras técnicas. Em testes diretos com prompts reforçados 5 vezes, ainda saíram erros como "Metodo" no lugar de "Método", "Coracao" no lugar de "Coração", "Rilual" no lugar de "Ritual", "Bia 14" no lugar de "Dia 14". Isso é limitação fundamental do modelo, não do prompt.

**O que a skill faz a respeito:**

1. **Antes de exibir o prompt**, avisa o aluno em uma linha clara que o ChatGPT pode errar texto e que o resultado é "boa o suficiente para placeholder, mas nem sempre para produção final".
2. **Após receber a imagem**, oferece ao aluno 2 caminhos:
   - Aceitar como está (serve como rascunho visual + referência de layout para reproduzir no Canva)
   - Pedir regeneração no ChatGPT (raramente resolve, mas pode tentar)
3. **Não esconde o problema** nem promete que vai funcionar perfeito. Aluno vai usar a skill com expectativa calibrada.

**Para uso em produção (página de vendas, anúncios, slides públicos):** sugerir ao aluno usar a imagem como referência de layout e refazer no Canva ou Figma com texto correto. Tempo: ~15 minutos para reproduzir o layout com texto perfeito.

## Recepção da imagem

Após exibir o prompt, a skill aguarda. Duas formas válidas de o aluno entregar a imagem:

1. **Colar no chat.** O aluno arrasta o PNG na conversa. A skill identifica o caminho temporário, copia para `entregas/furadeira/furadeira.png`.
2. **Salvar manual.** O aluno salva direto na pasta `entregas/furadeira/` e diz "imagem salva". A skill confirma a existência do arquivo e segue.

**Após receber a imagem, sempre perguntar:**

```
Posso conferir a imagem com você. Os modelos de imagem do ChatGPT costumam errar acentos e algumas palavras em português. Como ficou?

1. Texto está OK, pode usar (vou salvar e atualizar o painel)
2. Tem erros aceitáveis (vou salvar como placeholder, mas você refaz no Canva pra produção)
3. Quero regenerar no ChatGPT
```

## Pós-recepção

Após salvar a PNG:

1. Rodar `py -3 scripts/painel-incremental.py --slug {ativo}` para o painel de entregas reconhecer a nova furadeira.
2. Mostrar caminho absoluto ao aluno.
3. Sugerir próximo passo (`/copy-pagina` para usar a Furadeira na seção Método da página de vendas).

## Erros comuns

| Sintoma | Causa | Correção |
|---|---|---|
| Prompt sai com texto em inglês no infográfico | Faltou reforço "keep all text exactly in Brazilian Portuguese" | Sempre incluir essa instrução em maiúscula + nas HARD CONSTRAINTS |
| ChatGPT gera fundo branco em vez de transparente | Faltou reforço de transparent background | Repetir "transparent background" em 4 lugares distintos: abertura, VISUAL STYLE, HARD CONSTRAINT #1 e FINAL CHECK |
| Acentos saem errados ("Acao" no lugar de "Ação") | Modelo de imagem omite acentos quando não instruído | Sempre incluir lista de acentos + exemplo concreto nas HARD CONSTRAINTS |
| Layout não combina com a mecânica | Pulou a tabela de mapeamento | Aplicar a tabela mecânica → layout antes de montar o prompt |
| Cores não combinam com o nicho | Usou paleta genérica | Aplicar a tabela de paleta por nicho |
