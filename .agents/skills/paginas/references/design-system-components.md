# Design System Compilado. Componentes CSS por Seção

Referência rápida com todos os padrões CSS pré-extraídos dos templates.
**Ler este arquivo UMA VEZ substitui a leitura de todos os templates individuais.**

---

## CSS Variables Base

### Tema Escuro (glass_escuro)

```css
:root {
  --bg: #000000;
  --surface-1: #0a0a0a;
  --surface-2: #111113;
  --surface-3: #1c1c1e;
  --border: rgba(255,255,255,0.08);
  --border-hover: rgba(255,255,255,0.15);
  --text-primary: #f8f8f8;
  --text-secondary: #a0a0a0;
  --text-tertiary: #6c6c6c;
  --accent: #c2956b; /* adaptar ao nicho */
  --accent-glow: rgba(194,149,107,0.15);
  --glass-bg: rgba(17,17,19,0.6);
  --glass-blur: 20px;
  --fail-red: #e05a5a;
  --fail-red-dim: rgba(224,90,90,0.12);
  --cta-color: #38a169; /* adaptar ao nicho */
}
```

### Tema Claro (flat_claro)

```css
:root {
  --bg: #fafafa;
  --surface: #f0f0f2;
  --ink: #18181b;
  --accent: #d4d4d8;
  --warm: #c2956b; /* adaptar ao nicho */
  --border-flat: 1.5px solid #18181b;
  --cta-color: #38a169;
}
body {
  background-color: #fafafa;
  background-image:
    radial-gradient(circle at 20% 50%, rgba(194,149,107,0.06) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(194,149,107,0.04) 0%, transparent 40%);
}
```

---

## Animações (reutilizar em todas as seções)

```css
@keyframes fadeUpIn {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes shimmer {
  0%, 100% { opacity: 0.4; width: 60px; }
  50% { opacity: 1; width: 90px; }
}

/* IntersectionObserver para scroll animations */
.scroll-reveal { opacity: 0; transform: translateY(32px); transition: all 0.7s ease; }
.scroll-reveal.visible { opacity: 1; transform: translateY(0); }
```

```js
// IntersectionObserver. adicionar no final do body
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }});
}, { threshold: 0.15 });
document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el));
```

---

## Componentes por Seção

### 1. Header (Glass Nav)

```css
.header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  padding: 1rem 2rem;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
}
.header-inner {
  max-width: 1200px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
}
.brand { font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }
.brand-dot { color: var(--accent); }
.header-cta {
  display: inline-flex; align-items: center; gap: 0.5rem;
  padding: 0.6rem 1.25rem; background: var(--accent); color: var(--bg);
  font-size: 0.875rem; font-weight: 600; border: none; border-radius: 8px;
  cursor: pointer; transition: all 0.3s ease;
}
```

### 2. Hero (Escuro com Gradiente)

**Headline com gradiente:**
```css
.hero-headline {
  font-size: clamp(2.5rem, 5vw, 3.5rem); font-weight: 800;
  line-height: 1.05; letter-spacing: -0.03em;
  background: linear-gradient(to bottom right, #ffffff 30%, rgba(255,255,255,0.5));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
```

**Checklist com ícones:**
```css
.checklist { display: flex; flex-direction: column; gap: 14px; list-style: none; }
.check-item { display: flex; align-items: center; gap: 14px; transition: transform 200ms ease; }
.check-item:hover { transform: translateX(4px); }
.check-icon {
  width: 28px; height: 28px; border-radius: 8px;
  border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  background: linear-gradient(135deg, var(--surface-2), var(--surface-3));
}
.check-icon .material-symbols-outlined { font-size: 16px; color: var(--accent); }
```

**Botão CTA (glassmorphism):**
```css
.cta-button {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 16px 40px; font-size: 1rem; font-weight: 500;
  color: var(--text-primary);
  background: rgba(194,149,107,0.12);
  border: 1px solid rgba(194,149,107,0.25);
  border-radius: 12px; cursor: pointer;
  backdrop-filter: blur(16px);
  transition: all 0.35s cubic-bezier(0.25,0.46,0.45,0.94);
  position: relative; overflow: hidden;
}
.cta-button::before {
  content: ''; position: absolute; inset: 0; border-radius: 12px;
  opacity: 0; background: var(--text-primary);
  transition: opacity 0.35s ease; z-index: 0;
}
.cta-button:hover { border-color: rgba(255,255,255,0.4); transform: translateY(-2px);
  box-shadow: 0 0 24px rgba(194,149,107,0.15); }
.cta-button:hover::before { opacity: 1; }
.cta-button:hover span { color: var(--bg); }
```

**Botão CTA (verde/conversão. para seções claras):**
```css
.cta-verde {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 18px 48px; font-size: 1.1rem; font-weight: 700;
  color: #fff; background: var(--cta-color);
  border: none; border-radius: 12px; cursor: pointer;
  transition: all 0.3s ease; box-shadow: 0 4px 20px rgba(56,161,105,0.3);
}
.cta-verde:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(56,161,105,0.4); }
```

**Video card com chrome (browser dots):**
```css
.video-card {
  border-radius: 16px; border: 1px solid var(--border);
  overflow: hidden; background: var(--surface-1); position: relative;
}
.video-card::before { /* shimmer line no topo */
  content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%);
  width: 60%; max-width: 300px; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(143,143,143,0.5), transparent);
  z-index: 2;
}
.video-chrome {
  height: 48px; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; padding: 0 18px; gap: 8px;
}
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot-red { background: #e5484d; }
.dot-yellow { background: #f5d90a; }
.dot-green { background: #30a46c; }
.video-embed { position: relative; width: 100%; aspect-ratio: 16/9; }
```

### 3. Shimmer Line (separador decorativo)

```css
.shimmer-line {
  width: 60px; height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  margin: 0 auto 2rem; border-radius: 2px;
  animation: shimmer 3s ease-in-out infinite;
}
```

### 4. Section Header (headline + subtítulo)

```css
.section-label {
  text-align: center; font-size: 0.75rem; font-weight: 500;
  letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-tertiary);
  margin-bottom: 1.5rem;
}
.section-headline {
  text-align: center; font-size: clamp(2rem, 5vw, 3.25rem);
  font-weight: 700; line-height: 1.15; letter-spacing: -0.03em;
  margin-bottom: 1.25rem;
}
.gradient-text {
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent) 50%, var(--text-primary) 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  animation: gradientShift 6s ease infinite;
}
@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
.section-subtitle {
  text-align: center; font-size: 1.1rem; font-weight: 400;
  color: var(--text-secondary); max-width: 640px; margin: 0 auto 4rem; line-height: 1.7;
}
```

### 5. Pain/Dor Cards (glassmorphism)

```css
.pain-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
.pain-card {
  position: relative; background: var(--glass-bg);
  backdrop-filter: blur(16px); border: 1px solid var(--border);
  border-radius: 16px; padding: 2rem;
  transition: all 0.4s cubic-bezier(0.25,0.46,0.45,0.94); overflow: hidden;
}
.pain-card::before { /* glow line on top */
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-glow), transparent);
  opacity: 0; transition: opacity 0.4s ease;
}
.pain-card:hover {
  background: rgba(28,28,30,0.7); border-color: var(--border-hover);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 30px var(--accent-glow);
}
.pain-card:hover::before { opacity: 1; }
.pain-card-icon {
  display: inline-flex; align-items: center; justify-content: center;
  width: 48px; height: 48px; border-radius: 12px;
  background: rgba(194,149,107,0.08); border: 1px solid rgba(194,149,107,0.12);
  margin-bottom: 1.25rem;
}
.pain-card-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem; line-height: 1.35; }
.pain-card-text { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.7; }

/* Ênfase no final */
.pain-emphasis { margin-top: 3.5rem; text-align: center; }
.pain-emphasis-text { font-size: 1.15rem; font-weight: 500; color: var(--text-secondary); max-width: 600px; margin: 0 auto; }
.pain-emphasis-text strong { color: var(--accent); font-weight: 600; }

@media (max-width: 768px) { .pain-grid { grid-template-columns: 1fr; } }
```

### 6. Paliativo Cards (soluções concorrentes do mercado)

```css
.paliativo-section::before { /* radial glow vermelho sutil */
  content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%);
  width: 480px; height: 480px;
  background: radial-gradient(circle, var(--fail-red-dim) 0%, transparent 70%);
  pointer-events: none;
}
.paliativo-grid { display: grid; grid-template-columns: 1fr; gap: 20px; }
@media (min-width: 640px) { .paliativo-grid { grid-template-columns: 1fr 1fr; } }

.paliativo-card {
  background: var(--glass-bg); backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--border); border-radius: 16px; padding: 32px 28px;
  transition: all 0.35s ease;
}
.paliativo-card:hover {
  border-color: var(--border-hover);
  box-shadow: 0 0 32px rgba(224,90,90,0.08), 0 8px 32px rgba(0,0,0,0.4);
  transform: translateY(-2px);
}
.fail-icon {
  width: 48px; height: 48px; border-radius: 12px;
  background: var(--fail-red-dim);
  display: flex; align-items: center; justify-content: center;
}
.fail-icon .material-symbols-outlined { font-size: 24px; color: var(--fail-red); }

/* Imagem no topo do card */
.card-img-wrap {
  position: relative; overflow: hidden;
  margin: -32px -28px 20px; border-radius: 16px 16px 0 0;
}
.card-img-wrap img { display: block; width: 100%; height: 160px; object-fit: cover; filter: brightness(0.4); }
.card-img-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, transparent 30%, rgba(17,17,19,0.8) 100%);
}

/* Bridge text no final */
.paliativo-bridge { text-align: center; margin-top: 64px; }
.paliativo-bridge strong { color: var(--accent); font-weight: 600; }
```

### 7. Método/Solução Cards (passos numerados com imagem)

```css
.metodo-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; }
.metodo-card {
  position: relative; background: rgba(255,255,255,0.03);
  border: 1px solid var(--border); border-radius: 16px;
  overflow: hidden; backdrop-filter: blur(16px);
  transition: all 0.35s ease; display: flex; flex-direction: column;
}
.metodo-card:hover {
  border-color: var(--border-hover); transform: translateY(-4px);
  box-shadow: 0 0 32px rgba(194,149,107,0.08);
}
.metodo-card-image { position: relative; width: 100%; height: 200px; overflow: hidden; }
.metodo-card-image img { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.35); }
.metodo-card-image::after {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 80px;
  background: linear-gradient(to top, rgba(10,10,10,1), transparent);
}
.metodo-card-body { padding: 28px; flex: 1; display: flex; flex-direction: column; }
.metodo-step-number { font-size: 3rem; font-weight: 700; color: var(--accent); line-height: 1; margin-bottom: 12px; }
.metodo-step-title { font-size: 1.1875rem; font-weight: 600; line-height: 1.3; margin-bottom: 16px; }
.metodo-microsteps { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.metodo-microsteps li {
  font-size: 0.95rem; color: var(--text-secondary); padding-left: 16px; position: relative; line-height: 1.5;
}
.metodo-microsteps li::before {
  content: ''; position: absolute; left: 0; top: 8px;
  width: 4px; height: 4px; border-radius: 50%; background: var(--accent); opacity: 0.6;
}
```

### 8. Depoimentos (carrossel com cards)

```css
.carousel-wrapper { overflow: hidden; width: 100%; }
.carousel-track { display: flex; transition: transform 0.5s cubic-bezier(0.36,0.66,0.6,1); }
.carousel-slide { min-width: 100%; padding: 0 8px; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }

.testimonial-card {
  border-radius: 16px; border: 1px solid var(--border);
  background: var(--surface-1); padding: 28px;
  display: flex; flex-direction: column; gap: 18px;
  position: relative; transition: transform 0.2s ease;
}
.testimonial-card:hover { transform: translateY(-2px); border-color: rgba(255,255,255,0.12); }
.testimonial-card::before { /* shimmer top line */
  content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%);
  width: 50%; max-width: 120px; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(143,143,143,0.4), transparent);
}
.stars { display: flex; gap: 2px; }
.stars .material-symbols-outlined { font-size: 16px; color: var(--accent); font-variation-settings: 'FILL' 1; }
.quote { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6; font-style: italic; }
.author {
  display: flex; align-items: center; gap: 12px; margin-top: auto;
  padding-top: 16px; border-top: 1px solid var(--border);
}
.avatar {
  width: 40px; height: 40px; border-radius: 10px;
  background: linear-gradient(135deg, var(--surface-2), var(--surface-3));
  border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8125rem; font-weight: 600; color: var(--accent);
}

/* Controles do carrossel */
.nav-btn {
  width: 44px; height: 44px; border-radius: 12px;
  border: 1px solid var(--border); background: var(--surface-1);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: var(--text-secondary); transition: all 0.2s ease;
}
.nav-btn:hover { background: rgba(255,255,255,0.92); color: #000; }
.dot-indicator { width: 6px; height: 6px; border-radius: 50%; background: var(--text-tertiary); cursor: pointer; transition: all 0.3s ease; }
.dot-indicator.active { background: var(--text-primary); width: 20px; border-radius: 3px; }
```

```js
// Carrossel JS
const carousel = document.getElementById('carousel');
const slides = carousel.children;
let current = 0;
const total = slides.length;
function goTo(i) {
  current = i;
  carousel.style.transform = `translateX(-${current * 100}%)`;
  document.querySelectorAll('.dot-indicator').forEach((d, idx) => d.classList.toggle('active', idx === current));
}
function moveCarousel(dir) {
  let next = current + dir;
  if (next < 0) next = total - 1;
  if (next >= total) next = 0;
  goTo(next);
}
```

### 9. FAQ Accordion

```css
.faq-item { border-bottom: 1px solid var(--border); }
.faq-question {
  width: 100%; padding: 20px 0; display: flex; justify-content: space-between; align-items: center;
  background: none; border: none; cursor: pointer;
  font-size: 1.05rem; font-weight: 600; text-align: left; color: var(--text-primary);
}
.faq-question .material-symbols-outlined { transition: transform 0.3s ease; font-size: 20px; color: var(--text-tertiary); }
.faq-question.active .material-symbols-outlined { transform: rotate(180deg); }
.faq-answer { max-height: 0; overflow: hidden; transition: max-height 0.4s ease, padding 0.3s ease; }
.faq-answer.open { max-height: 500px; padding-bottom: 20px; }
.faq-answer p { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.7; }
```

```js
// FAQ Accordion
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const answer = btn.nextElementSibling;
    const isOpen = answer.classList.contains('open');
    document.querySelectorAll('.faq-answer').forEach(a => a.classList.remove('open'));
    document.querySelectorAll('.faq-question').forEach(q => q.classList.remove('active'));
    if (!isOpen) { answer.classList.add('open'); btn.classList.add('active'); }
  });
});
```

### 10. CTA Flutuante (Mobile)

```css
.floating-cta {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 90;
  padding: 12px 16px; background: rgba(0,0,0,0.95);
  backdrop-filter: blur(20px); border-top: 1px solid var(--border);
  display: none; /* mostrado via JS */
  transform: translateY(100%); transition: transform 0.3s ease;
}
.floating-cta.visible { transform: translateY(0); }
.floating-cta a {
  display: block; width: 100%; padding: 16px; text-align: center;
  background: var(--cta-color); color: #fff; font-weight: 700;
  border-radius: 10px; text-decoration: none; font-size: 1rem;
}
@media (min-width: 769px) { .floating-cta { display: none !important; } }
@media (max-width: 768px) { .floating-cta { display: block; } }
```

```js
// Floating CTA. aparece após hero, some perto do CTA final
const floatingCta = document.querySelector('.floating-cta');
const ctaFinal = document.querySelector('.cta-final-section');
if (floatingCta) {
  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    const showAfter = window.innerHeight;
    const hideNear = ctaFinal ? ctaFinal.offsetTop - window.innerHeight : Infinity;
    floatingCta.classList.toggle('visible', scrollY > showAfter && scrollY < hideNear);
  });
}
```

### 11. Stack de Valor (ancoragem de preço)

```css
.stack-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 0; border-bottom: 1px solid var(--border);
  font-size: 1rem; color: var(--text-secondary);
}
.stack-item .stack-value { color: var(--text-tertiary); font-weight: 500; }
.stack-total {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 0; margin-top: 8px;
  font-size: 1.25rem; font-weight: 700; color: var(--text-primary);
}
.stack-total .stack-value { text-decoration: line-through; color: var(--text-tertiary); }
.price-real {
  text-align: center; margin: 32px 0;
}
.price-real .parcela { font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 700; color: var(--text-primary); }
.price-real .avista { font-size: 1rem; color: var(--text-tertiary); margin-top: 4px; }
```

### 12. Garantia (selo circular)

```css
.garantia-layout { display: flex; align-items: center; gap: 40px; max-width: 700px; margin: 0 auto; }
.garantia-selo {
  flex-shrink: 0; width: 120px; height: 120px; border-radius: 50%;
  border: 3px solid var(--accent); display: flex; flex-direction: column;
  align-items: center; justify-content: center;
}
.garantia-selo .dias { font-size: 2.5rem; font-weight: 800; color: var(--accent); line-height: 1; }
.garantia-selo .label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: var(--text-tertiary); }
.garantia-texto h3 { font-size: 1.5rem; font-weight: 700; margin-bottom: 12px; }
.garantia-texto p { font-size: 1rem; color: var(--text-secondary); line-height: 1.7; }
@media (max-width: 640px) {
  .garantia-layout { flex-direction: column; text-align: center; }
}
```

### 13. Selos de Confiança

```css
.trust-badges {
  display: flex; justify-content: center; gap: 24px; margin-top: 20px; flex-wrap: wrap;
}
.trust-badge {
  display: flex; align-items: center; gap: 6px;
  font-size: 0.8125rem; color: var(--text-tertiary);
}
.trust-badge .material-symbols-outlined { font-size: 16px; }
```

---

## Seção com Fundo Artístico (sem foto)

Para seções com fundo forte sem usar foto de banco de imagens (picsum/unsplash genérico são proibidos. ver `SKILL.md` → Imagens Contextuais), usar gradientes radiais sobrepostos. Dá profundidade sem imagem aleatória.

```css
.section-artistica {
  background-color: #0a0a0a;
  background-image:
    radial-gradient(at 20% 50%, hsla(28,100%,74%,0.15) 0px, transparent 50%),
    radial-gradient(at 80% 20%, hsla(189,100%,56%,0.08) 0px, transparent 50%);
  color: #fff;
  padding: 96px 24px;
}
```

Se for obrigatório usar foto de fundo real, só é permitido um ID específico de Unsplash comprovadamente ligado à copy:

```css
.section-img-bg {
  background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
    url('https://images.unsplash.com/photo-ID-ESPECIFICO?w=1920&q=80');
  background-size: cover; background-position: center;
  background-attachment: fixed; color: #fff;
  padding: 96px 24px;
}
```

---

## Responsive Padrão

```css
@media (max-width: 768px) {
  .header { padding: 0.875rem 1.25rem; }
  .header-nav { display: none; }
  section { padding: 64px 20px; }
  .hero-headline { font-size: 2.25rem; }
  .pain-grid, .metodo-steps { grid-template-columns: 1fr; }
  .card-grid { grid-template-columns: 1fr; }
  .garantia-layout { flex-direction: column; text-align: center; }
}
@media (max-width: 480px) {
  section { padding: 56px 16px; }
  .hero-headline { font-size: 1.75rem; }
  .cta-button { width: 100%; justify-content: center; }
}
```

---

## Template HTML Base (estrutura do arquivo)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Nome do Produto]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[Heading]+[Body]&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,300,0,0" rel="stylesheet">
  <style>
    /* Reset + Variables + Componentes (copiar dos blocos acima) */
  </style>
</head>
<body>
  <!-- 16 seções -->
  <script>
    /* IntersectionObserver + FAQ + Carrossel + Floating CTA */
  </script>
</body>
</html>
```
