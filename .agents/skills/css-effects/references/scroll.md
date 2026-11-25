# Efeitos de Scroll

12+ efeitos baseados em scroll position.

## Índice
fade-up · fade-left · fade-right · fade-scale · stagger · parallax · sticky-scroll · horizontal-scroll · zoom-scroll · word-reveal · counter · rotate-on-scroll · scroll-progress · scroll-snap · reveal-mask

---

### fade-up (com IntersectionObserver)
**Visual:** Elemento sobe e aparece quando entra na viewport.
**Quando usar:** Padrão pra qualquer seção que entra na tela. É o efeito de scroll mais sólido.
```css
.fade-up {
  opacity: 0;
  transform: translateY(60px);
  transition: opacity 0.8s cubic-bezier(0.4,0,0.2,1), transform 0.8s cubic-bezier(0.4,0,0.2,1);
}
.fade-up.visible { opacity: 1; transform: translateY(0); }
```
```js
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) e.target.classList.add('visible');
  });
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });
document.querySelectorAll('.fade-up').forEach(el => obs.observe(el));
```

### fade-left / fade-right / fade-scale
**Visual:** Variações do fade-up — entrando da esquerda, direita, ou crescendo.
**Quando usar:** Linhas de feature alternadas (texto-imagem). Adiciona variedade.
```css
.fade-left { opacity: 0; transform: translateX(-60px); transition: 0.8s cubic-bezier(0.4,0,0.2,1); }
.fade-left.visible { opacity: 1; transform: translateX(0); }

.fade-right { opacity: 0; transform: translateX(60px); transition: 0.8s cubic-bezier(0.4,0,0.2,1); }
.fade-right.visible { opacity: 1; transform: translateX(0); }

.fade-scale { opacity: 0; transform: scale(0.85); transition: 0.8s cubic-bezier(0.4,0,0.2,1); }
.fade-scale.visible { opacity: 1; transform: scale(1); }
```
**JS:** mesmo do fade-up.

### stagger (cascata)
**Visual:** Filhos aparecem em sequência com delay progressivo.
**Quando usar:** Grids de cards, listas, qualquer conjunto de 3+ items relacionados.
```css
.stagger > *:nth-child(2) { transition-delay: 0.1s; }
.stagger > *:nth-child(3) { transition-delay: 0.2s; }
.stagger > *:nth-child(4) { transition-delay: 0.3s; }
.stagger > *:nth-child(5) { transition-delay: 0.4s; }
```
**Combine com qualquer fade-* acima.**

### parallax (multi-camadas)
**Visual:** Camadas de fundo movendo em velocidades diferentes do conteúdo.
**Quando usar:** Hero, seções decorativas. Cria sensação de profundidade real.
```html
<div class="parallax-section">
  <div class="parallax-bg" data-speed="0.3"></div>
  <div class="parallax-stars" data-speed="0.6"></div>
  <div class="parallax-content">conteúdo</div>
</div>
```
```css
.parallax-section { position: relative; height: 500px; overflow: hidden; }
.parallax-bg, .parallax-stars { position: absolute; inset: 0; will-change: transform; }
.parallax-content { position: relative; z-index: 2; }
```
```js
const section = document.querySelector('.parallax-section');
const layers = section.querySelectorAll('[data-speed]');
window.addEventListener('scroll', () => {
  const scrolled = -section.getBoundingClientRect().top;
  layers.forEach(l => {
    const speed = parseFloat(l.dataset.speed);
    l.style.transform = `translateY(${scrolled * speed}px)`;
  });
});
```

### sticky-scroll (visual fixo + texto rolando)
**Visual:** Visual à esquerda fica grudado enquanto o texto à direita rola e atualiza o conteúdo do visual.
**Quando usar:** Apresentar features de produto em etapas, tutoriais, processos. Padrão Apple/Stripe.
```html
<section class="sticky-section">
  <div class="sticky-container">
    <div class="sticky-left">
      <div class="sticky-visual" id="visual">🚀</div>
    </div>
    <div class="sticky-right">
      <div class="sticky-step active" data-icon="🚀">Etapa 1</div>
      <div class="sticky-step" data-icon="🎨">Etapa 2</div>
      <div class="sticky-step" data-icon="⚡">Etapa 3</div>
    </div>
  </div>
</section>
```
```css
.sticky-container { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: start; }
.sticky-left { position: sticky; top: 80px; }
.sticky-right { display: flex; flex-direction: column; gap: 200px; padding: 100px 0; }
.sticky-step { opacity: 0.3; transition: opacity 0.4s; }
.sticky-step.active { opacity: 1; }
@media (max-width: 768px) {
  .sticky-container { grid-template-columns: 1fr; }
  .sticky-left { position: static; }
  .sticky-right { gap: 60px; padding: 0; }
}
```
```js
const visual = document.getElementById('visual');
const steps = document.querySelectorAll('.sticky-step');
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      steps.forEach(s => s.classList.remove('active'));
      e.target.classList.add('active');
      visual.textContent = e.target.dataset.icon;
    }
  });
}, { threshold: 0.6 });
steps.forEach(s => obs.observe(s));
```

### horizontal-scroll
**Visual:** Scroll vertical da página vira movimento lateral dos cards.
**Quando usar:** Galerias, portfolios, apresentação de cases. Truque "wow" clássico.
```html
<section class="horizontal-section">
  <div class="horizontal-wrapper">
    <div class="horizontal-track">
      <div class="card">1</div>
      <div class="card">2</div>
      <div class="card">3</div>
    </div>
  </div>
</section>
```
```css
.horizontal-section { height: 300vh; position: relative; }
.horizontal-wrapper {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
  display: flex;
  align-items: center;
}
.horizontal-track {
  display: flex;
  gap: 24px;
  padding: 0 30px;
  will-change: transform;
}
.horizontal-track > * { flex: 0 0 400px; }
```
```js
const section = document.querySelector('.horizontal-section');
const track = document.querySelector('.horizontal-track');
window.addEventListener('scroll', () => {
  const rect = section.getBoundingClientRect();
  const sectionH = section.offsetHeight - window.innerHeight;
  const scrolled = -rect.top;
  if (scrolled >= 0 && scrolled <= sectionH) {
    const progress = scrolled / sectionH;
    const max = track.scrollWidth - window.innerWidth + 60;
    track.style.transform = `translateX(${-progress * max}px)`;
  }
});
```

### zoom-scroll
**Visual:** Texto/elemento cresce de pequeno até gigante conforme scroll.
**Quando usar:** Transição entre seções, frase de impacto, brand statement.
```html
<section class="zoom-section">
  <div class="zoom-wrapper">
    <div class="zoom-content"><h2>BIG IDEA</h2></div>
  </div>
</section>
```
```css
.zoom-section { height: 200vh; position: relative; }
.zoom-wrapper {
  position: sticky; top: 0;
  height: 100vh;
  display: flex; align-items: center; justify-content: center;
}
.zoom-content { will-change: transform, opacity; }
```
```js
const section = document.querySelector('.zoom-section');
const content = document.querySelector('.zoom-content');
window.addEventListener('scroll', () => {
  const rect = section.getBoundingClientRect();
  const sectionH = section.offsetHeight - window.innerHeight;
  const scrolled = -rect.top;
  if (scrolled >= 0 && scrolled <= sectionH) {
    const p = scrolled / sectionH;
    content.style.transform = `scale(${0.5 + p * 1.5})`;
    content.style.opacity = p < 0.8 ? 1 : Math.max(0, 1 - (p - 0.8) * 5);
  }
});
```

### word-reveal
**Visual:** Cada palavra de um parágrafo pinta de branco progressivamente conforme o scroll passa.
**Quando usar:** Frase manifesto, missão, statement de marca, momentos cinematográficos.
```html
<p class="reveal-text" id="reveal">
  <span>Cada</span> <span>palavra</span> <span>aparece</span> <span>no</span> <span>tempo</span> <span>certo.</span>
</p>
```
```css
.reveal-text span {
  color: #2a2a2a;
  transition: color 0.4s ease;
}
.reveal-text span.highlighted { color: #fff; }
```
```js
const el = document.getElementById('reveal');
const words = el.querySelectorAll('span');
window.addEventListener('scroll', () => {
  const r = el.getBoundingClientRect();
  const start = window.innerHeight * 0.8;
  const end = window.innerHeight * 0.2;
  const progress = (start - r.top) / (start - end);
  const n = Math.floor(progress * words.length);
  words.forEach((w, i) => w.classList.toggle('highlighted', i < n));
});
```

### counter-animation
**Visual:** Número conta de 0 até o valor final com easing quando entra na tela.
**Quando usar:** Stats, métricas de impacto, "X clientes", "Y% de satisfação".
```html
<div class="stat-num" data-target="2547">0</div>
```
```js
const counters = document.querySelectorAll('.stat-num');
const obs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const target = parseInt(el.dataset.target);
      const duration = 1500;
      const start = performance.now();
      function update(now) {
        const elapsed = now - start;
        const p = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.floor(eased * target).toLocaleString('pt-BR');
        if (p < 1) requestAnimationFrame(update);
      }
      requestAnimationFrame(update);
      obs.unobserve(el);
    }
  });
}, { threshold: 0.5 });
counters.forEach(c => obs.observe(c));
```

### rotate-on-scroll
**Visual:** Elemento gira proporcionalmente à posição do scroll na página.
**Quando usar:** Decorativo, ícones de transição, marca/logo girando.
```js
const box = document.querySelector('.rotate-on-scroll');
window.addEventListener('scroll', () => {
  const r = box.getBoundingClientRect();
  const distance = r.top + r.height/2 - window.innerHeight/2;
  box.style.transform = `rotate(${distance * 0.3}deg)`;
});
```

### scroll-progress-bar
**Visual:** Barra fina no topo da página mostrando progresso do scroll.
**Quando usar:** Páginas longas, blogs, artigos, landing pages compridas.
```html
<div class="scroll-progress" id="progress"></div>
```
```css
.scroll-progress {
  position: fixed;
  top: 0; left: 0;
  height: 3px;
  background: linear-gradient(90deg, #ff00cc, #00f0ff);
  z-index: 9999;
  width: 0%;
}
```
```js
const progress = document.getElementById('progress');
window.addEventListener('scroll', () => {
  const p = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
  progress.style.width = p + '%';
});
```

### scroll-snap
**Visual:** Scroll trava em cada seção; sensação de slides verticais.
**Quando usar:** Apresentações, sites de uma página, portfolios.
```css
html { scroll-snap-type: y mandatory; }
section {
  height: 100vh;
  scroll-snap-align: start;
}
```
**Nota:** CSS puro, sem JS. Use com moderação — pode irritar usuários que querem scroll livre.

### reveal-mask (clip-path scroll)
**Visual:** Elemento aparece como se fosse "desmascarado" de baixo pra cima.
**Quando usar:** Imagens hero, headings importantes, transições cinemáticas.
```css
.reveal-mask {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 1s cubic-bezier(0.4,0,0.2,1);
}
.reveal-mask.visible { clip-path: inset(0 0 0 0); }
```
**JS:** mesmo do fade-up.
