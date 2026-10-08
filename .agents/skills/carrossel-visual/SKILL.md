---
name: carrossel-visual
description: Orquestra geração de carrossel Instagram com foto IA por card. Dois modos: Criação (sem referência) conduz 9 etapas clássicas; Replicação (com imagem de referência) aplica análise pixel-level de 10 fases para reconstrução fiel. Ambos geram JSON config e executam gerar-carrossel-foto.py.
allowed-tools: Read, Write, Bash
---

# Carrossel Visual com Foto IA

Gera carrossel para Instagram com foto real por card. Dois modos de operação conforme disponibilidade de referência visual.

## Referências obrigatórias

Antes de qualquer geração de prompt de imagem, carregar:
- `.claude/skills/carrossel-visual/references/hooks-imagem-disruptiva.md`
- `.claude/skills/carrossel-visual/references/skill-referencia-visual.md`

---

## Passo 0. Contexto

Leia `meus-produtos/.ativo`, depois `meus-produtos/{ativo}/perfil.md` e `meus-produtos/{ativo}/idconsumidor.md` se existir.

Extrair internamente (não mostrar ao usuário):
- Urgências Ocultas completas (70 itens, 7 categorias)
- Decorados (50 benefícios)
- Quadro (transformação principal)
- Nicho, público-alvo e handle do produto
- Paleta de cores do produto (se especificada no perfil)

Verificar carrosséis anteriores em `meus-produtos/{ativo}/entregas/criativos/` para evitar ângulos repetidos.

---

## Passo 1. Escolha do modo

```
Você tem uma imagem de referência de design para o carrossel?

1. Não — vou criar do zero (fluxo guiado)
2. Sim — quero replicar o estilo de uma referência (análise pixel-level)

Digite o número:
```

---

# MODO A — CRIAÇÃO (sem referência)

Fluxo guiado de 9 etapas para carrossel original.

## Etapa 00. Quantidade de cards

```
Quantas páginas no carrossel? (2 a 10)
```

- N = 1: redirecionar para banner estático
- N = 2 a 10: guardar N e seguir

---

## Etapa 01. Tema

Listar 8 Urgências Ocultas mais fortes do produto (Dores, Urgências Quentes e Inusitadas em prioridade):

```
Qual situação vai inspirar o carrossel?

1. [Urgência 1]
2. [Urgência 2]
...
8. [Urgência 8]

(ou descreva outro ângulo)
```

---

## Etapa 02. Tom de voz

```
Quem narra o carrossel?

1. Você mesmo (voz do criador, direto e próximo)
2. Repórter (jornalístico, dados e fatos)
3. Professor (didático, explicativo)
```

---

## Etapa 03. Tipo de conteúdo

```
Qual formato narrativo?

1. Explicativo (ensina um conceito)
2. Problema-Solução (apresenta dor e resolve)
3. Certo e Errado (contrasta comportamentos)
4. História (narrativa com personagem)
5. Mito (desmonta crenças falsas)
6. Comparativo (dois lados frente a frente)
7. Curiosidade (revela algo inesperado)
8. Dilema (escolha difícil para debate)
9. Apelo Emocional (medo, sonho, conquista)
10. Demonstração (mostra como fazer na prática)
11. Outro (descreva)
```

---

## Etapa 04. Hook da capa

### Passo 1. Buscar na base
Consultar Urgências Ocultas do produto. Identificar a dor mais forte, o dado mais impactante e o gatilho mais relevante.

### Passo 2. Escolher estilo de hook visual
Ler `.claude/skills/carrossel-visual/references/hooks-imagem-disruptiva.md` e escolher o estilo mais adequado ao tema.

Estilos disponíveis: Esquisito, Exagero, Reflexão, Polêmica, Comparação, Famosos, Notícia, Curiosidade, Listas, Controvérsia.

### Passo 3. Propor 3 opções

Para cada opção mostrar:
- Headline da capa (ALL CAPS)
- Subheadline
- Estilo de hook visual
- Por que vai parar o scroll (1 linha)

Aguardar aprovação antes de continuar.

---

## Etapa 05. Copy completa + prompts

Após hook aprovado, gerar todos os N cards de uma vez para aprovação.

### Formato card de conteúdo (Cards 2 a N-1):

```
Card [N] — [NOME DO PONTO]
Tema: Escuro / Claro
Label: [ex: "Ponto 1"]
Título: [1 linha impactante]
Parágrafos (mín. 4 linhas):
  1. [...]
  2. [...]
  3. [...]
  4. [...]
Destaques: [trecho para cor de destaque]

Prompt (EN — para API):
> [prompt em inglês com elemento disruptivo]

Tradução (PT — conferência):
> [tradução fiel]
```

### Formato card CTA (Card N):

```
Card [N] — CTA
Tema: Claro (sempre)
Label: [ex: "Agora você sabe"]
Título: [resultado principal em destaque]
Parágrafos (CTA direto, 2-3 linhas):
  1. [...]
  2. [...]
  3. [link na bio / próximo passo]
```

### Regras de copy:
- Sem travessão (—) em qualquer card
- Sem ponto de exclamação
- Sem pergunta no gancho
- Mínimo 4 linhas por card de conteúdo
- Produto não aparece antes do card CTA
- Toda copy passa pela revisora antes de ser mostrada ao usuário

### Regras dos prompts de imagem (Modo A):
- `anatomically correct` obrigatório
- `no distorted limbs`, `no distorted fingers`, `no text, no watermark`
- Composição variada entre cards (nunca repetir enquadramento ou cenário)
- O estilo disruptivo escolhido na Etapa 04 deve aparecer descrito no prompt
- Proibido prompt genérico: "pessoa estudando", "profissional sorrindo", "mãos no teclado" sem elemento de ruptura concreto

### Fórmula obrigatória do prompt fotográfico (EN)

```
[ENQUADRAMENTO] of [SUJEITO + CARACTERÍSTICA FÍSICA CONCRETA], [AÇÃO OU EXPRESSÃO ESPECÍFICA DO HOOK],
[ELEMENTO DISRUPTIVO DO ESTILO ESCOLHIDO],
[LUZ E AMBIENTE: direção, temperatura e mood da luz],
[CENÁRIO ESPECÍFICO com detalhe de textura ou cor],
shallow depth of field, [COMPOSIÇÃO: bokeh / over-the-shoulder / split-screen / etc.]
```

O script adiciona automaticamente ao final: câmera, lente, f/2.0, color grading, resolução 8K e termos negativos. Não repita esses termos no `prompt_en`.

Apresentar copy + prompts completos aguardando:

```
1. Aprovar e continuar
2. Ajustar um card (indique qual e o que muda)
```

---

## Etapa 05.5. Referência visual

```
Vai usar alguma imagem de referência para a capa ou algum card?

1. Sim
2. Não
```

Se Sim: consultar `.claude/skills/carrossel-visual/references/skill-referencia-visual.md` e seguir o fluxo para cada card indicado.

---

## Etapa 05.6. Esquema de cores

```
Como prefere as cores dos cards de conteúdo?

1. Escuro (fundo escuro, destaques vibrantes)
2. Claro (fundo claro, destaques em cor de destaque)
3. Alternado (card 2 claro, card 3 escuro, card 4 claro...)
```

Regras fixas:
- Card 1 (Capa): sempre foto full-bleed
- Card N (CTA): sempre fundo claro

Derivar cores de destaque do produto ativo. Se o `perfil.md` não especifica paleta, usar `#FF6B01` (escuro) e `#8B5CF6` (claro) como padrão. Apresentar e perguntar se quer manter ou trocar.

---

Após Etapa 05.6, seguir para **Geração card a card** (seção compartilhada ao final deste arquivo).

---

# MODO B — REPLICAÇÃO (com imagem de referência)

# CAROUSEL REPLICATION ENGINE — V2

**Função:** ANALISAR → DECOMPOR → MODELAR → RECONSTRUIR com fidelidade absoluta.

**Proibido:** reinterpretar, melhorar, simplificar, alterar grid, trocar tipografia, mudar proporções, inventar elementos.

---

## Fase 0. Entradas

Coletar antes de iniciar a análise:

```
Para configurar a replicação, preciso de:

1. A imagem de referência (cole ou informe o caminho)
2. Quantas páginas no carrossel? (2 a 10)
3. Qual o tema? (escolha entre as Urgências Ocultas abaixo ou descreva)

[listar as 8 Urgências Ocultas mais fortes]

4. Há algo que deve mudar em relação à referência? (copy, cores, elemento específico)
   Se não, deixe em branco.
```

---

## Fase 1 — Visual Forensics (leitura cirúrgica)

### Contexto

Extrair:
- tipo exato (carrossel, capa, anúncio, UI híbrida)
- objetivo (conversão, autoridade, educação, retenção)
- estágio do funil (atenção / interesse / desejo / ação)
- emoção dominante (urgência, curiosidade, tensão, confiança)

### Estilo visual (precisão obrigatória)

Mapear:
- estilo base: flat / semi-realista / 3D / render / híbrido
- estética: editorial / tech / SaaS / minimalista / denso
- contraste: baixo / médio / alto
- textura: limpa / granulação / blur / glassmorphism / noise
- profundidade: 2D / layered / depth illusion / real shadow
- nível: básico / refinado / premium / high-end

### Linguagem de câmera (se houver personagem)

- enquadramento: close / medium / wide
- ângulo: frontal / 3/4 / top / isométrico
- lente: wide / normal / tele (compressão visual)
- profundidade de campo: rasa / média / infinita
- direção de luz: frontal / lateral / backlight
- intensidade de luz

**Saída obrigatória:** lista estruturada de todos os elementos com coordenadas, camadas e relações.

---

## Fase 2 — Design Tokens (extração sistêmica)

### Cores (HEX obrigatório)

Extrair com aproximação HEX e proporção de uso (%):
- `primary`
- `secondary`
- `accent`
- `background`
- `surface`
- `text.primary`
- `text.secondary`
- `border`
- `highlight`

Mapear também gradientes (ângulo + lista de cores) e opacidades por elemento.

### Tipografia (análise profunda)

Para cada bloco de texto:
- família aproximada (ex: Inter / Helvetica / Poppins) + fallback provável
- pesos: bold / semibold / medium / regular
- escala real estimada: h1 / h2 / h3 / body / caption (px)
- line-height (%)
- letter-spacing
- transform (uppercase, capitalize, none)

Identificar padrão de contraste tipográfico entre níveis.

### Sistema de espaçamento

Escala base com multiplicador (ex: 4px, 8px, 12px, 16px, 24px...): xs / sm / md / lg / xl / 2xl

### Bordas e raios

- border-radius por elemento (px)
- espessura e cor de cada borda

### Efeitos

- sombra: x, y, blur, spread, opacidade
- blur de fundo (backdrop-filter)
- glow (cor, raio)
- noise/grain (textura, intensidade visual)

**Saída obrigatória:** bloco de tokens nomeados e documentados.

---

## Fase 3 — Linguagem Visual

### Composição
- distribuição de massa visual
- zonas de atenção (heatmap mental)
- eixo dominante (vertical / horizontal / diagonal)

### Hierarquia
- ordem de leitura (1º, 2º, 3º elemento que o olho visita)
- gatilhos visuais (tamanho, cor, contraste)
- elementos dominantes vs suporte

### Ritmo Visual
- repetição de padrões
- cadência entre elementos
- consistência entre blocos

### Contraste
- relação fundo vs texto (alto, médio, baixo)
- áreas de respiro (whitespace intencional)

---

## Fase 4 — Grid System (crítico)

Definir com precisão:
- margem externa (px)
- área útil
- número de colunas implícitas
- gutters
- alinhamentos (left / center / mixed)
- baseline vertical

Se não explícito: inferir matematicamente a partir dos espaçamentos observados.

---

## Fase 5 — Figma Mode (absoluto)

Para cada elemento:

```
- type: frame | text | image | shape | group
- x: (%)
- y: (%)
- width: (%)
- height: (%)
- constraints: (left/right/center + top/bottom/center)
- padding: (top right bottom left em px)
- alignment: (dentro do grupo/frame pai)
- auto layout: (se aplicável: horizontal | vertical | gap em px)
- z-index: (ordem de camadas)
```

Sem descrição subjetiva. Tudo mensurável.

---

## Fase 6 — Personagem (se existir na referência)

- posição exata na grade (%)
- escala relativa ao frame (%)
- recorte: close / busto / cintura / corpo inteiro
- direção do olhar
- expressão
- key light: lado, ângulo, temperatura
- integração com fundo: overlay, recorte nítido, blend suave, sombra projetada

---

## Fase 7 — Arquitetura do carrossel

Definir sequência com base na referência e no N escolhido na Fase 0:

| Card | Papel | Descrição |
|------|-------|-----------|
| 01 | Hook | Impacto máximo, parada de scroll |
| 02-04 | Contexto | Construção do argumento |
| 05-N-1 | Valor | Entrega do conteúdo principal |
| N | CTA | Chamada para ação |

---

## Fase 8 — Consistência sistêmica

Validar antes de gerar os prompts:
- tokens iguais em todos os slides
- grid fixo
- spacing consistente
- tipografia consistente
- ritmo visual preservado

---

## Fase 9 — Reconstrução card a card

Para cada card gerar os quatro blocos:

### Bloco 1. Copy

Texto final adaptado ao tema (Fase 0), seguindo Light Copy:
- Sem travessão (—)
- Sem ponto de exclamação
- Sem pergunta no gancho
- Produto não aparece antes do card CTA
- Toda copy passa pela revisora antes de ser mostrada ao usuário

### Bloco 2. Estrutura Figma

Lista completa de elementos com coordenadas (Fase 5 aplicada a este card específico).

### Bloco 3. Descrição visual

Descrição fiel da cena: composição, luz, cenário, personagem, relação entre elementos. Referência interna para o prompt.

### Bloco 4. Prompt de imagem (crítico)

Formato obrigatório do `prompt_en`:

```
instagram carousel slide, 1080x1350, portrait 4:5

exact visual style replication:
[estilo completo extraído das Fases 1-3]

layout:
[elementos com posição exata — Fase 5]

typography:
[estilo e peso — Fase 2]

colors:
[hex — Fase 2]

lighting:
[direção + intensidade — Fase 6]

depth:
[2D / layered / shadow — Fase 1]

composition:
[estrutura — Fase 4]

DO NOT:
- change layout
- add elements
- redesign
```

Restrições obrigatórias em todos os prompts:
- `anatomically correct`
- `no distorted limbs`, `no distorted fingers`
- `no text, no watermark`

O script adiciona automaticamente câmera, lente, f/2.0, color grading, 8K e termos negativos. Não repita esses termos.

---

## Fase 10 — Controle de alterações

Aplicar somente as alterações declaradas na Fase 0.

Tudo que não foi listado permanece idêntico à referência.

---

## Output da Fase 9 (apresentar ao usuário para aprovação)

```
--- DESIGN TOKENS ---
[saída da Fase 2]

--- GRID SYSTEM ---
[saída da Fase 4]

--- LINGUAGEM VISUAL ---
[saída da Fase 3]

--- ESTRUTURA DO CARROSSEL ---
[saída da Fase 7]

--- CARDS ---
[para cada card:]
  COPY
  FIGMA STRUCTURE
  DESCRIÇÃO VISUAL
  PROMPT (EN + tradução PT)

---
1. Aprovar e gerar todos os cards
2. Ajustar um card específico (indique qual e o que muda)
3. Ajustar os design tokens
```

Após aprovação: derivar `accent_dark` e `accent_light` dos tokens extraídos e seguir para **Geração card a card**.

---

# GERAÇÃO CARD A CARD (compartilhado pelos dois modos)

## Geração do JSON config

Antes de executar qualquer card, salvar o JSON config completo em:
`meus-produtos/{ativo}/entregas/criativos/carrosseis/config-{slug}-{n}.json`

Schema:

```json
{
  "slug": "{slug-do-produto}",
  "handle": "@{handle-do-produto}",
  "output_dir": "meus-produtos/{ativo}/entregas/criativos/carrosseis/carrossel-{n}",
  "accent_dark": "{cor-destaque-escuro}",
  "accent_light": "{cor-destaque-claro}",
  "cards": [
    {
      "id": "01",
      "tipo": "capa",
      "headline": "HEADLINE EM CAIXA ALTA",
      "headline_highlight": "PALAVRA",
      "subheadline": "...",
      "prompt_en": "..."
    },
    {
      "id": "02",
      "tipo": "conteudo",
      "tema": "escuro",
      "label": "Ponto 1",
      "titulo": "Título do card",
      "paragrafos": ["linha 1", "linha 2", "linha 3", "linha 4"],
      "destaques": ["trecho em destaque"],
      "prompt_en": "..."
    },
    {
      "id": "0N",
      "tipo": "cta",
      "tema": "claro",
      "label": "Agora você sabe",
      "titulo": "CTA final",
      "paragrafos": ["linha 1", "linha 2", "link na bio"],
      "destaques": []
    }
  ]
}
```

---

## Execução: capa primeiro

Mostrar antes de executar:

```
CAPA — Resumo para aprovação

Hook: [headline + subheadline]
[Modo A: Estilo disruptivo escolhido]
[Modo B: Estilo extraído da referência]

Prompt (EN — enviado ao modelo):
> [prompt completo em inglês]

Tradução (PT — conferência):
> [tradução fiel]

Referência: [caminho da referência OU "sem referência"]

1. Aprovar e gerar
2. Ajustar o prompt
3. Trocar o estilo
```

Após aprovação, executar:

```bash
py -3 scripts/gerar-carrossel-foto.py --config [caminho-do-config] --only 01
```

---

## Execução: cards 2 a N (um por vez)

Para cada card:

1. Mostrar prompt (EN + tradução PT) para aprovação
2. Aguardar: 1. Aprovar e gerar / 2. Ajustar prompt / 3. Ajustar copy
3. Após aprovação, atualizar o JSON config e executar apenas o card:

```bash
py -3 scripts/gerar-carrossel-foto.py --config [caminho] --only [id]
```

4. Entregar e perguntar: 1. Aprovado / 2. Gerar nova versão / 3. Ajustes

---

## Revisão final

Checklist antes de declarar concluído:

- [ ] Setas `› › ›` presentes em todos os cards exceto o CTA
- [ ] Handle do produto presente em todos os cards
- [ ] Esquema de cores aplicado corretamente
- [ ] Headline da capa: ALL CAPS, ao menos 1 palavra na cor de destaque
- [ ] Mínimo 4 linhas de body em todos os cards de conteúdo
- [ ] Card N = CTA com fundo claro, sem setas
- [ ] Total de cards = N escolhido
- [ ] Copy aprovada pela revisora antes da entrega
- [ ] (Modo B) Nenhum elemento foi reinterpretado sem estar na lista de alterações

---

## Entrega final

```
Carrossel gerado.

Cards salvos em:
meus-produtos/{ativo}/entregas/criativos/carrosseis/carrossel-{n}/

Para publicar:
1. Abra a pasta
2. Suba os PNGs como carrossel no Instagram (na ordem: card-01, card-02, ...)

Próximos passos:
- Caption para o carrossel: /copy-social (opção Caption)
- Anúncio com a mesma urgência: /criativo-aida
- Mais carrosséis: /carrossel novamente
```
