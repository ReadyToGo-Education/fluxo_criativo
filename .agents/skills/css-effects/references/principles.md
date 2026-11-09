# Princípios de Combinação, Performance e Acessibilidade

Leia este arquivo ANTES de sugerir múltiplos efeitos juntos ou aplicar em sites maiores. Aqui estão as regras invisíveis que separam um site polido de um amador cheio de efeitos.

---

## 1. Hierarquia visual

Um site bem construído tem **camadas de atenção**. Cada efeito ocupa uma camada:

- **Camada 0 — Ambient (passa despercebido):** gradient-anim, dot-pattern, noise, grid sutil, fade-up
- **Camada 1 — Acento (nota se prestar atenção):** card-tilt, card-spotlight, img-hover-zoom, text-highlight
- **Camada 2 — Focal (chama atenção):** btn-glow-pulse, card-border-anim, text-fire/neon, scan-line
- **Camada 3 — Wow (impacto):** sticky-scroll, horizontal-scroll, zoom-scroll, scramble, matrix-rain

**Regra de pirâmide:** quanto mais alta a camada, menos vezes deve aparecer.

| Camada | Quantidade na página |
|---|---|
| Ambient | Quantos quiser |
| Acento | 5-15 instâncias |
| Focal | 1-3 instâncias |
| Wow | 1-2 momentos no site inteiro |

Se um site tem 5 efeitos "wow" diferentes, NENHUM deles é wow.

---

## 2. Combinação de efeitos no mesmo elemento

**Pode combinar:**
- card-tilt + card-spotlight (sutis e complementares)
- card-lift + card-shine (sutis)
- card-lift + img-hover-zoom (em cards de produto com imagem)
- btn-glow-pulse + btn-ripple (estado contínuo + feedback de clique)
- text-gradient-anim + word-reveal (anim contínua + revelação no scroll, não competem)
- input-glow-focus + input-floating-label (independentes, complementares)

**NÃO combine no mesmo elemento:**
- card-border-anim + card-glow + card-pulse (3 efeitos contínuos)
- text-glitch + text-fire (dois fortes, vira poluição)
- card-tilt + card-magnetic (dois movimentos por mouse, conflita)
- card-flip-3d + card-tilt (rotações conflitantes)
- btn-magnetic + cursor-magnetic (puxam um pro outro, vira caos)

**Teste prático:** se você precisa de 2 segundos pra entender o que tá acontecendo, é demais.

---

## 3. Performance

Efeitos parecem "leves" mas podem matar a fluidez do site. Categorize antes de usar:

### Ultra-leves (use à vontade)
- Todos os hover CSS-only (lift, glow, shine, fill)
- text-gradient (sem anim)
- fade-up via IntersectionObserver
- skeleton, shimmer

### Leves (até ~10 simultâneos)
- text-gradient-anim
- card-tilt (CSS transform, GPU)
- card-spotlight (uma camada radial)
- counter-animation
- scroll-progress

### Médios (limite 3-5 simultâneos)
- parallax (scroll listener — use throttle)
- horizontal-scroll
- sticky-scroll com mudança de visual
- card-particles
- aurora-gradient com filter blur
- matrix-rain

### Pesados (limite 1 por viewport)
- card-particles em vários cards
- canvas com mais de 50 partículas
- backdrop-filter blur em elementos grandes (caro em mobile)
- mix-blend-mode em elementos grandes
- multiple animations contínuas no mesmo viewport

### Regras de ouro de performance

1. **Use `will-change` SÓ no que está sendo animado AGORA** — não em tudo. Remova após a animação. `will-change` permanente come RAM.

2. **Anime APENAS `transform` e `opacity`** — anything else (top, left, width, height, color) força reflow/repaint, mata a frame rate. Para mover, use `translate`. Para mudar tamanho, use `scale`.

3. **IntersectionObserver > scroll listener** — pra qualquer "anima quando entra na tela", IntersectionObserver é 10x mais barato que scroll listener.

4. **Throttle scroll listeners** — se PRECISAR de scroll listener (parallax), use throttle ou rAF:
```js
let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      // sua lógica
      ticking = false;
    });
    ticking = true;
  }
});
```

5. **Canvas precisa de cleanup** — `cancelAnimationFrame` quando o elemento não está visível. Caso contrário, particles continuam rodando na CPU mesmo fora da tela.

6. **Mobile = pesado** — backdrop-filter, blur grande, mix-blend-mode são significativamente mais caros em mobile. Sempre teste no celular.

---

## 4. Acessibilidade (a11y)

Acessibilidade não é opcional. Cada efeito precisa passar nestes 5 testes:

### Teste 1 — `prefers-reduced-motion`
Pessoas com sensibilidade vestibular podem passar mal com animações. Sempre adicione no FINAL do CSS:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Para efeitos que dependem de animação pra fazer sentido (ex: word-reveal), forneça uma versão estática:
```css
@media (prefers-reduced-motion: reduce) {
  .reveal-text span { color: #fff; }  /* tudo já visível */
}
```

### Teste 2 — Contraste em estados hover
Hover effects que mudam cor precisam manter contraste WCAG AA (4.5:1 pra texto normal, 3:1 pra texto grande). Texto branco virando ciano em fundo preto: ok. Texto cinza virando cinza claro: provavelmente falha.

### Teste 3 — Navegação por teclado
Todo efeito de hover deve funcionar com `:focus-visible` também. Adicione:
```css
.btn-fill-up:hover,
.btn-fill-up:focus-visible { /* mesmo estado */ }
```

### Teste 4 — Touch (sem hover)
Em mobile, hovers não disparam (ou disparam de forma estranha). Use `@media (hover: hover)` pra restringir efeitos que assumem mouse:
```css
@media (hover: hover) {
  .card-tilt:hover { transform: ... }
}
```

### Teste 5 — Cursor custom + acessibilidade
Cursores custom escondem o cursor nativo. Pessoas com baixa visão usam cursors aumentados do SO. NUNCA esconda cursor em forms, áreas de leitura longa, ou se o site tem muito texto. Use só em portfolios/sites curtos. E sempre tenha:
```css
@media (hover: none), (prefers-reduced-motion: reduce) {
  .cursor, .cursor-follow { display: none; }
  body { cursor: auto; }
}
```

---

## 5. Tom: combinando efeitos com identidade da marca

Cada efeito carrega um "tom" implícito. Combine só com o tom da marca:

| Efeito | Tom |
|---|---|
| text-fire, text-neon, text-glitch | Energético, jovem, gaming, edgy |
| text-scramble, matrix-rain, scan-line | Tech, hacker, sci-fi |
| text-metallic, card-shine, gradient-orbs | Premium, luxo, sofisticado |
| text-shimmer, mesh-gradient, fade-up | Corporativo, fintech, SaaS |
| text-highlight, scroll-progress, dot-pattern | Editorial, blog, conteúdo |
| heart-like, confetti, btn-3d-press | Lúdico, casual, social |
| card-tilt, card-spotlight, btn-magnetic | Moderno, premium, polido |
| cursor-blob, image-trail, scramble | Criativo, experimental, portfolio |

**Tradução prática:**
- Cliente é advogado → use editorial + corporativo. Nunca gaming.
- Cliente é gaming → use energético + tech. Nunca corporativo conservador.
- Cliente é fintech → use corporativo + premium. Nunca lúdico ou edgy.
- Cliente é restaurante moderno → premium + lúdico. Evite tech.

---

## 6. Mobile-first considerations

Em ordem de prioridade pra ajustar em mobile:

1. **Desativar cursor custom** — sempre. `@media (hover: none)`.
2. **Desativar tilt em cards** — touch faz tilt feio. Substitua por `card-lift` simples.
3. **Sticky-scroll vira lista vertical** — abandone o split em 2 colunas.
4. **Horizontal-scroll vira scroll lateral nativo** — `overflow-x: auto` + `scroll-snap`.
5. **Reduzir partículas pela metade** — em mobile, 30 partículas viram 15.
6. **Backdrop-filter mais leve** — `blur(20px)` vira `blur(10px)`.
7. **Parallax mais sutil** — speeds menores ou desativar.

Padrão de bloco mobile que vai no FINAL do CSS:
```css
@media (max-width: 768px) {
  .card-tilt:hover { transform: translateY(-4px) !important; }  /* sem rotação */
  .cursor, .cursor-follow { display: none; }
  body { cursor: auto; }
  .matrix-bg { display: none; }  /* poupar bateria */
}
```

---

## 7. Quando dizer não

A skill deve avisar o usuário se ele tá pedindo algo problemático:

- "Quero glitch no nome do meu escritório de advocacia" → não combina com o tom. Sugerir text-stroke ou text-3d sutil.
- "Quero matrix rain em toda página" → vai matar performance e parecer 2003. Sugerir grid-pattern ambient.
- "Quero tilt em todos os 50 cards do catálogo" → custo de CPU + parece exagero. Sugerir tilt só nos 3-4 cards de destaque (above the fold), resto card-lift.
- "Quero efeito X no botão de submit do formulário de cadastro" (efeito chamativo) → forms exigem feedback funcional, não show. Sugerir btn-loading-state.

Sempre ofereça uma alternativa quando recusar. Nunca apenas "não dá".

---

## Checklist final antes de entregar código

- [ ] As cores estão adaptadas à paleta do usuário (não magenta+ciano padrão)?
- [ ] O efeito tem `prefers-reduced-motion` se for animação contínua?
- [ ] Foi testado mentalmente em mobile? Tem fallback?
- [ ] Combina com o tom da marca?
- [ ] Não compete com outros efeitos da mesma viewport?
- [ ] Performance: tá animando só transform/opacity?
- [ ] Acessibilidade: contraste e teclado funcionam?
- [ ] Tem comentário explicando os pontos de customização?

Se uma das respostas é "não", revise antes de entregar.
