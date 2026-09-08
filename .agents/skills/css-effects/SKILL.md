---
name: css-effects
description: Aplica efeitos visuais CSS e JavaScript em qualquer elemento de site — texto, cards, botões, formulários, navegação, modais, imagens, loaders, scroll, cursor, fundos, e microinterações. Use SEMPRE que o usuário pedir para "adicionar efeito", "deixar mais bonito", "animar", "modernizar", "tornar interativo", "estilizar", "deixar profissional", ou enviar print/screenshot/descrição de um elemento (botão, card, título, seção, navbar, hero, formulário, menu, modal) pedindo melhorias visuais. Também ativa em pedidos como "que efeito posso usar aqui", "sugere algo legal pra essa parte", "como deixar esse site mais interessante", "essa seção tá sem graça", "como faz aquele efeito do site X", ou qualquer pergunta sobre o que cada efeito CSS faz e como funciona. Use mesmo se o usuário não citar "CSS" explicitamente — qualquer pedido de melhoria visual em UI web aciona esta skill. Também ativa quando o usuário diz que está construindo um site, landing page, portfolio, dashboard, e quer torná-lo memorável ou competitivo.
---

# CSS Effects Skill

Catálogo curado de 100+ efeitos visuais (CSS + JavaScript) prontos pra aplicar em qualquer elemento de site. A skill sabe sugerir o efeito certo pro contexto, explicar o que cada efeito faz, gerar o código pronto, e montar combos coerentes.

## Fluxo de uso

Quando ativada, identifique em qual cenário você está e siga o fluxo:

### Cenário A — Usuário enviou print/screenshot

1. Analise a imagem: identifique o tipo de elemento (botão, card, hero, navbar, form, modal, footer, galeria, etc.) e o estilo geral (dark/light, moderno/clássico, denso/arejado, paleta de cores).
2. Faça **1 pergunta direta** se faltar contexto crítico (ex: "Esse card é clicável ou só decorativo?"). Não faça mais que 1 pergunta — siga com a melhor hipótese.
3. Sugira 2-3 efeitos do catálogo que se encaixam no estilo + função, explicando brevemente cada um.
4. Pergunte qual ele quer aplicar OU já entregue o código do mais óbvio se a escolha for clara.

### Cenário B — Usuário descreveu o elemento em texto

1. Identifique o tipo de elemento e a intenção (chamar atenção / decorar / dar feedback / guiar olhar).
2. Sugira 2-3 efeitos com nome + 1 frase de descrição.
3. Aguarde escolha ou entregue o melhor direto se for óbvio.

### Cenário C — Usuário perguntou o que um efeito específico faz

1. Consulte o catálogo da categoria correspondente.
2. Explique: como funciona visualmente (1-2 frases), quando usar, contexto ideal, tradeoffs.
3. Ofereça gerar uma demo pra ele ver funcionando.

### Cenário D — Usuário quer melhorar o site inteiro / pediu sugestão geral

1. Pergunte o tipo de site (landing, portfolio, SaaS, e-commerce, blog, dashboard, evento) — só essa pergunta.
2. Sugira um **combo curado** da seção "Combos por tipo de site" abaixo.
3. Mostre o combo como uma lista numerada de "onde aplicar o quê".

### Cenário E — Usuário quer reproduzir efeito de outro site ("igual ao do Linear/Stripe/Vercel/Apple")

1. Identifique qual efeito famoso ele provavelmente quer (veja "Efeitos famosos por referência" abaixo).
2. Confirme: "Você quer aquele efeito de [descrição]?"
3. Entregue o código do equivalente do catálogo.

## Mapa do catálogo (qual arquivo consultar)

A skill tem o catálogo dividido em arquivos por categoria. Leia o arquivo relevante quando for sugerir/gerar código:

- **`references/text.md`** — Efeitos em texto: gradiente, glitch, neon, fire, scramble, typing, wave, reveal, 3D stack, highlight, shimmer, stroke, rotate words, e mais (20+ efeitos)
- **`references/cards.md`** — Cards e containers: glow, lift, tilt, spotlight, shine, border anim, liquid blob, scan, noise, flip 3D, magnetic, ripple, particles, e mais (20+ efeitos)
- **`references/buttons.md`** — Botões: gradient slide, fill up, arrow expand, 3D press, magnetic, ripple, glow pulse, border draw, sliding text, loading state (15+ efeitos)
- **`references/scroll.md`** — Scroll: fade-up/left/right/scale, stagger, parallax, sticky, horizontal scroll, zoom, word reveal, counter, rotate on scroll, scroll progress (12+ efeitos)
- **`references/forms.md`** — Inputs e formulários: floating label, underline focus, glow focus, animated border, validation states, password strength (10+ efeitos)
- **`references/navigation.md`** — Navbar, menu, links: underline animado, hamburger morph, sidebar slide, sticky on scroll, mobile menu fullscreen (10+ efeitos)
- **`references/loaders.md`** — Loaders e estados: spinner, skeleton, dots, progress bar, percentage ring, shimmer placeholder, page transition (10+ efeitos)
- **`references/images.md`** — Imagens e mídia: kenburns, hover zoom, color reveal, parallax internal, blur load, comparison slider, mask reveal (10+ efeitos)
- **`references/video-hero.md`** — Hero com vídeo MP4 controlado por scroll (scrubbing): video-hero-scroll-scrub, bottom-fade pra próxima seção, side-text overlay, fallback mobile/iOS, mp4-keyframe-optimization (com script cross-platform `scripts/otimizar-video-scrub.py`)
- **`references/modals.md`** — Modais, tooltips, popovers: fade-in scale, slide-up, blur backdrop, drawer side, toast notification (8+ efeitos)
- **`references/backgrounds.md`** — Fundos animados: aurora, mesh gradient, animated grid, gradient orbs, dot pattern, noise, stars, matrix rain (10+ efeitos)
- **`references/cursor.md`** — Cursor customizado: dot+follower, magnetic cursor, image trail, blob cursor, blend mode (5+ efeitos)
- **`references/microinteractions.md`** — Micro: heart like, checkbox check, toggle switch, copy feedback, success/error flash, confetti (10+ efeitos)
- **`references/combos.md`** — Combos prontos por tipo de site (SaaS, portfolio, e-commerce, blog, evento, dashboard) com setup completo
- **`references/principles.md`** — Princípios de combinação, hierarquia, performance, acessibilidade — leia ANTES de sugerir múltiplos efeitos juntos

**Importante:** Sempre leia o arquivo de referência relevante antes de gerar código, mesmo que pareça lembrar. Os snippets nos arquivos são as versões testadas, com cores adaptáveis e correções de bugs comuns.

## Regras de ouro ao sugerir efeitos

1. **Função antes de forma** — pergunte "esse elemento serve pra quê?" antes de "como fica bonito?". Botão CTA precisa de glow/ripple. Card decorativo aceita morph. Texto de impacto pede word-reveal.

2. **No máximo 1 efeito chamativo por viewport** — animações contínuas (border-anim, pulse, scan, fire, gradient-anim, particles) competem por atenção. Use apenas 1 visível por vez.

3. **Combos sutis ganham de efeitos isolados fortes** — `card-tilt + card-spotlight` (ambos sutis) > `card-glow neon piscando` (sozinho gritante). Premium é sutileza acumulada.

4. **Match do tom** — site corporativo/saúde/jurídico não pode usar glitch, fire, neon, shake. Site de gaming/evento aceita tudo. Sempre filtre pelo contexto do negócio.

5. **Hover ≠ touch** — em mobile, hovers não disparam. Sempre proponha alternativa pra mobile (autoplay leve, intersection observer, ou simplesmente versão estática).

6. **Reduced motion sempre** — qualquer efeito com animação contínua precisa do bloco `@media (prefers-reduced-motion: reduce)` no final. Veja `references/principles.md`.

## Combos por tipo de site (resumo — detalhes em `references/combos.md`)

- **SaaS / produto tech** → gradient-anim hero + tilt+spotlight nas features + counter nas stats + word-reveal no manifesto
- **Portfolio criativo** → scramble hero + horizontal-scroll galeria + cursor custom + word-reveal bio
- **Landing de evento** → fire/neon hero + glow+ripple no CTA + parallax + counter regressivo
- **Blog editorial** → highlight em palavras-chave + scroll-progress bar + fade-up imagens + reading-time animado
- **E-commerce** → lift+shine cards de produto + glow+ripple no "Comprar" + counter de avaliações + image-zoom em galeria
- **Dashboard** → counter nas métricas + skeleton loaders + fade-up em rows + grid-pattern background
- **Site único / link bio** → tilt no card central + magnetic em ícones sociais + spotlight de fundo
- **Página de vendas premium / produto físico / mentoria** → **video-hero-scroll-scrub** com texto à esquerda + bottom-fade pra próxima seção + tilt+spotlight nos cards + counter nas stats. Sempre passar o MP4 pelo `scripts/otimizar-video-scrub.py` antes (keyframe em todo frame)

## Efeitos famosos por referência (sites)

Quando o usuário menciona "igual ao site X", traduza assim:

- **Linear / Vercel** → tilt + spotlight + gradient-anim + grid-pattern + scroll-fade-up
- **Stripe** → sticky-scroll com visual mudando, parallax sutil, gradient-anim no hero
- **Apple (página de produto)** → sticky-scroll horizontal, image zoom on scroll, word-reveal, **video-hero-scroll-scrub** (vídeo do produto controlado pelo scroll na primeira dobra)
- **Tesla / NomadaToast / Emergent** → **video-hero-scroll-scrub** com texto à esquerda, bottom-fade pra próxima seção (ver `references/video-hero.md`)
- **GitHub (Copilot/landing)** → typing animation, gradient-anim, dark com particles
- **Notion** → hover-lift sutil, fade-up stagger, scroll-progress
- **Awwwards (genérico)** → cursor custom, horizontal-scroll, scramble, mix-blend-mode
- **OpenAI / Anthropic** → gradient orbs, fade-up, mesh gradient backgrounds
- **Framer (landing)** → tilt+spotlight, magnetic CTA, sticky horizontal

## Quando NÃO usar efeitos (importante)

Avise o usuário se o pedido for contraprodutivo:

- **Formulários e checkout** — animações distraem. Use só feedback (validation flash, focus glow). Nunca scramble/wave/glitch.
- **Conteúdo crítico** (médico, financeiro, jurídico) — sem fire, glitch, shake, neon. Mantenha sóbrio: fade-up sutil + highlight bem usado.
- **Texto que precisa ser lido rápido** (menus, navbar, instruções) — sem animação contínua na tipografia.
- **Múltiplos animados na mesma viewport** — causa náusea/distração. Reduza pra 1.
- **Páginas de erro / loading crítico** — só skeleton/spinner, nada de glitch (parece bug real).
- **Acessibilidade comprometida** — se o efeito esconde conteúdo ou prejudica leitura, sugira versão sutil.

Quando recusar, **sempre ofereça uma alternativa mais sóbria** que ainda traga personalidade.

## Como entregar o código

Sempre forneça:

1. **HTML** com a estrutura mínima necessária
2. **CSS** com cores adaptadas ao contexto do usuário (não use sempre magenta/ciano padrão — pergunte ou infira a paleta dele)
3. **JS** apenas se o efeito exigir (avise quais efeitos são CSS-puro vs precisam de JS)
4. **Comentário curto** explicando os pontos de customização (cores, durações, intensidade)
5. **Aviso de reduced-motion** se o efeito for animação contínua

Se o usuário tem várias seções no site, ofereça gerar **um arquivo HTML standalone** mostrando o efeito isolado pra ele testar antes de aplicar.

## Iteração

Depois de entregar, pergunte:

- "Esse efeito tá no nível que você queria, ou quer mais sutil/intenso?"
- "Quer aplicar em outros elementos da página também?"
- "Posso sugerir um efeito complementar pra essa seção?"

A meta é construir uma experiência coerente, não despejar efeitos soltos.
