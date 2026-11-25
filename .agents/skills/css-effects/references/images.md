# Efeitos de Imagens e Mídia

10+ efeitos para imagens, galerias, vídeos.

## Índice
ken-burns · hover-zoom · color-reveal · grayscale-color · parallax-internal · blur-load · comparison-slider · mask-reveal · image-reveal-on-scroll · gallery-stack-hover

---

### img-ken-burns
**Visual:** Imagem fazendo zoom-in lento contínuo (efeito documentário).
**Quando usar:** Hero images, slideshow background, banners imersivos.
```html
<div class="ken-burns">
  <img src="..." alt="...">
</div>
```
```css
.ken-burns {
  width: 100%;
  height: 500px;
  overflow: hidden;
}
.ken-burns img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  animation: kenBurns 15s ease-in-out infinite alternate;
}
@keyframes kenBurns {
  0% { transform: scale(1) translate(0, 0); }
  100% { transform: scale(1.15) translate(-2%, -2%); }
}
```

### img-hover-zoom
**Visual:** Imagem dá zoom suave dentro do container no hover.
**Quando usar:** Cards de produto, galerias, blog post thumbnails.
```html
<div class="img-zoom">
  <img src="..." alt="...">
</div>
```
```css
.img-zoom {
  overflow: hidden;
  border-radius: 12px;
}
.img-zoom img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4,0,0.2,1);
}
.img-zoom:hover img { transform: scale(1.08); }
```

### img-color-reveal
**Visual:** Imagem em P&B; ganha cor no hover.
**Quando usar:** Portfolios, galerias artísticas, fotos editoriais.
```css
.img-color-reveal img {
  filter: grayscale(100%);
  transition: filter 0.6s ease;
}
.img-color-reveal:hover img {
  filter: grayscale(0%);
}
```

### img-grayscale-color
**Visual:** Variante com mais drama: P&B + leve blur, fica colorido + nítido no hover.
**Quando usar:** Apresentação de equipe, projetos, cases de cliente.
```css
.img-gray-color img {
  filter: grayscale(100%) blur(2px);
  transition: filter 0.5s ease;
}
.img-gray-color:hover img {
  filter: grayscale(0%) blur(0);
}
```

### img-parallax-internal
**Visual:** A imagem se move dentro do próprio container conforme o mouse.
**Quando usar:** Hero, banner único, destaque de produto. Cria sensação de profundidade.
```html
<div class="img-parallax">
  <img src="..." alt="...">
</div>
```
```css
.img-parallax {
  width: 100%;
  height: 400px;
  overflow: hidden;
  border-radius: 16px;
}
.img-parallax img {
  width: 110%;
  height: 110%;
  object-fit: cover;
  transition: transform 0.3s ease-out;
}
```
```js
document.querySelectorAll('.img-parallax').forEach(el => {
  const img = el.querySelector('img');
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect();
    const x = ((e.clientX - r.left) / r.width - 0.5) * 20;
    const y = ((e.clientY - r.top) / r.height - 0.5) * 20;
    img.style.transform = `translate(${-x}px, ${-y}px) scale(1.05)`;
  });
  el.addEventListener('mouseleave', () => {
    img.style.transform = 'translate(0, 0) scale(1)';
  });
});
```

### img-blur-load
**Visual:** Imagem aparece blurred e foca quando carrega completamente.
**Quando usar:** Imagens grandes, galerias, lazy loading. Padrão Medium/Unsplash.
```html
<div class="blur-load">
  <img src="thumb-pequeno.jpg" data-src="full-grande.jpg" alt="...">
</div>
```
```css
.blur-load { overflow: hidden; }
.blur-load img {
  width: 100%;
  filter: blur(20px);
  transition: filter 0.6s ease;
}
.blur-load img.loaded { filter: blur(0); }
```
```js
document.querySelectorAll('.blur-load img').forEach(img => {
  const fullImg = new Image();
  fullImg.src = img.dataset.src;
  fullImg.onload = () => {
    img.src = img.dataset.src;
    img.classList.add('loaded');
  };
});
```

### img-comparison-slider
**Visual:** Duas imagens sobrepostas; arrasta o slider pra revelar antes/depois.
**Quando usar:** Cases de design (antes/depois), edição de foto, transformações.
```html
<div class="compare">
  <div class="compare-after"><img src="depois.jpg"></div>
  <div class="compare-before"><img src="antes.jpg"></div>
  <div class="compare-handle"></div>
</div>
```
```css
.compare {
  position: relative;
  width: 100%;
  height: 400px;
  overflow: hidden;
  border-radius: 12px;
  cursor: ew-resize;
}
.compare img { width: 100%; height: 100%; object-fit: cover; }
.compare-after, .compare-before {
  position: absolute; inset: 0;
}
.compare-before {
  width: 50%;
  border-right: 3px solid #fff;
}
.compare-handle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40px;
  height: 40px;
  background: #fff;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  cursor: ew-resize;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.compare-handle::before {
  content: "↔";
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  color: #000;
  font-weight: bold;
}
```
```js
const compare = document.querySelector('.compare');
const before = compare.querySelector('.compare-before');
const handle = compare.querySelector('.compare-handle');
let dragging = false;
compare.addEventListener('mousedown', () => dragging = true);
window.addEventListener('mouseup', () => dragging = false);
compare.addEventListener('mousemove', e => {
  if (!dragging) return;
  const r = compare.getBoundingClientRect();
  const pct = ((e.clientX - r.left) / r.width) * 100;
  const clamped = Math.max(0, Math.min(100, pct));
  before.style.width = clamped + '%';
  handle.style.left = clamped + '%';
});
```

### img-mask-reveal
**Visual:** Imagem aparece sendo "desmascarada" de baixo pra cima.
**Quando usar:** Hero, transição cinemática, momento de impacto.
```css
.img-mask {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 1.2s cubic-bezier(0.4,0,0.2,1);
}
.img-mask.visible { clip-path: inset(0 0 0 0); }
```
**JS:** use IntersectionObserver (mesmo padrão do fade-up do scroll.md).

### img-reveal-on-scroll
**Visual:** Imagem entra com fade + scale leve quando entra na tela.
**Quando usar:** Galerias, blog, qualquer página com imagens.
```css
.img-scroll {
  opacity: 0;
  transform: scale(0.95);
  transition: all 0.8s cubic-bezier(0.4,0,0.2,1);
}
.img-scroll.visible {
  opacity: 1;
  transform: scale(1);
}
```

### gallery-stack-hover
**Visual:** Grid de imagens onde hover destaca uma e diminui as outras.
**Quando usar:** Galeria de portfolio, time, produtos relacionados.
```html
<div class="gallery-stack">
  <img src="1.jpg">
  <img src="2.jpg">
  <img src="3.jpg">
  <img src="4.jpg">
</div>
```
```css
.gallery-stack {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.gallery-stack img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
  transition: all 0.4s ease;
  filter: brightness(0.7);
}
.gallery-stack:hover img { filter: brightness(0.4) blur(2px); transform: scale(0.95); }
.gallery-stack img:hover { filter: brightness(1) blur(0); transform: scale(1.05); z-index: 2; }
```
