# Cursor Customizado

5+ efeitos para personalizar o cursor do site.

## Quando usar (com cautela)
Cursor customizado é forte. Use em **portfolios, sites criativos, branding forte**. NUNCA use em sites com formulários longos, e-commerce, ou onde o usuário precisa do cursor padrão (textareas, edição de texto).

Sempre forneça fallback pro mobile (`@media (hover: none)` desativando o cursor custom).

## Índice
dot-follower · magnetic-cursor · image-trail · blob-cursor · blend-mode-cursor

---

### cursor-dot-follower
**Visual:** Ponto pequeno acompanha o mouse exatamente; círculo maior segue com delay suave.
**Quando usar:** Padrão clássico de portfolio criativo. Funciona em qualquer tema.
```html
<div class="cursor"></div>
<div class="cursor-follow"></div>
```
```css
@media (hover: hover) {
  body { cursor: none; }
}
.cursor {
  position: fixed;
  width: 10px; height: 10px;
  background: #00f0ff;
  border-radius: 50%;
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: difference;
  transition: width 0.2s, height 0.2s;
}
.cursor-follow {
  position: fixed;
  width: 40px; height: 40px;
  border: 2px solid #00f0ff;
  border-radius: 50%;
  pointer-events: none;
  z-index: 9998;
  transition: transform 0.3s ease, width 0.3s, height 0.3s, background 0.3s;
}
.cursor-follow.hover {
  width: 80px; height: 80px;
  background: rgba(0,240,255,0.1);
}
@media (hover: none) {
  .cursor, .cursor-follow { display: none; }
}
```
```js
const cursor = document.querySelector('.cursor');
const follow = document.querySelector('.cursor-follow');
let mx = 0, my = 0, fx = 0, fy = 0;
document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cursor.style.transform = `translate(${mx-5}px, ${my-5}px)`;
});
function loop() {
  fx += (mx - fx) * 0.15;
  fy += (my - fy) * 0.15;
  follow.style.transform = `translate(${fx-20}px, ${fy-20}px)`;
  requestAnimationFrame(loop);
}
loop();
document.querySelectorAll('a, button, .card, [data-cursor]').forEach(el => {
  el.addEventListener('mouseenter', () => follow.classList.add('hover'));
  el.addEventListener('mouseleave', () => follow.classList.remove('hover'));
});
```

### cursor-magnetic
**Visual:** Cursor "puxa" elementos próximos pra ele (combo de magnetismo + cursor custom).
**Quando usar:** Botões CTA principais em sites criativos. NÃO usar em vários elementos juntos.
```css
.magnetic-target {
  transition: transform 0.3s ease-out;
  will-change: transform;
}
```
```js
document.querySelectorAll('.magnetic-target').forEach(el => {
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect();
    const x = (e.clientX - r.left - r.width/2) * 0.4;
    const y = (e.clientY - r.top - r.height/2) * 0.4;
    el.style.transform = `translate(${x}px, ${y}px)`;
  });
  el.addEventListener('mouseleave', () => {
    el.style.transform = 'translate(0, 0)';
  });
});
```

### cursor-image-trail
**Visual:** Imagens aparecem em rastro conforme o mouse se move (ao passar sobre elementos específicos).
**Quando usar:** Galerias de portfolio, páginas de projeto, sites de fotografia.
```html
<div class="trail-container" data-images="img1.jpg,img2.jpg,img3.jpg">
  <h2>Passe o mouse aqui</h2>
</div>
```
```css
.trail-container {
  position: relative;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.trail-img {
  position: fixed;
  width: 200px;
  height: 280px;
  object-fit: cover;
  pointer-events: none;
  border-radius: 8px;
  opacity: 0;
  transform: scale(0.5);
  transition: opacity 0.3s, transform 0.3s;
  z-index: 9990;
}
.trail-img.show { opacity: 1; transform: scale(1); }
```
```js
document.querySelectorAll('.trail-container').forEach(container => {
  const images = container.dataset.images.split(',');
  let lastTime = 0;
  let imgIndex = 0;
  container.addEventListener('mousemove', e => {
    const now = Date.now();
    if (now - lastTime < 150) return;
    lastTime = now;
    const img = document.createElement('img');
    img.className = 'trail-img';
    img.src = images[imgIndex];
    img.style.left = (e.clientX - 100) + 'px';
    img.style.top = (e.clientY - 140) + 'px';
    document.body.appendChild(img);
    requestAnimationFrame(() => img.classList.add('show'));
    setTimeout(() => {
      img.classList.remove('show');
      setTimeout(() => img.remove(), 300);
    }, 600);
    imgIndex = (imgIndex + 1) % images.length;
  });
});
```

### cursor-blob
**Visual:** Cursor é uma bolha grande gelatinosa que se deforma ao mover.
**Quando usar:** Sites artísticos, design experimental, apresentação de marcas criativas.
```html
<div class="blob-cursor"></div>
```
```css
@media (hover: hover) {
  body { cursor: none; }
}
.blob-cursor {
  position: fixed;
  width: 60px; height: 60px;
  background: radial-gradient(circle, rgba(0,240,255,0.6), rgba(255,0,204,0.4));
  border-radius: 50%;
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: screen;
  filter: blur(8px);
  transition: width 0.3s, height 0.3s, transform 0.05s ease-out;
}
.blob-cursor.hover {
  width: 120px; height: 120px;
}
@media (hover: none) {
  .blob-cursor { display: none; }
}
```
```js
const blob = document.querySelector('.blob-cursor');
let mx = 0, my = 0, bx = 0, by = 0;
document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
});
function loop() {
  bx += (mx - bx) * 0.2;
  by += (my - by) * 0.2;
  blob.style.transform = `translate(${bx - 30}px, ${by - 30}px)`;
  requestAnimationFrame(loop);
}
loop();
document.querySelectorAll('a, button').forEach(el => {
  el.addEventListener('mouseenter', () => blob.classList.add('hover'));
  el.addEventListener('mouseleave', () => blob.classList.remove('hover'));
});
```

### cursor-blend-mode
**Visual:** Círculo grande com `mix-blend-mode: difference` que inverte cores onde passa.
**Quando usar:** Sites com tipografia grande e contraste forte. Visual editorial moderno.
```html
<div class="cursor-blend"></div>
```
```css
@media (hover: hover) {
  body { cursor: none; }
}
.cursor-blend {
  position: fixed;
  top: 0; left: 0;
  width: 50px; height: 50px;
  background: #fff;
  border-radius: 50%;
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: difference;
  transition: transform 0.1s ease-out, width 0.3s, height 0.3s;
  transform: translate(-50%, -50%);
}
.cursor-blend.hover {
  width: 100px; height: 100px;
}
@media (hover: none) {
  .cursor-blend { display: none; }
}
```
```js
const c = document.querySelector('.cursor-blend');
document.addEventListener('mousemove', e => {
  c.style.left = e.clientX + 'px';
  c.style.top = e.clientY + 'px';
});
document.querySelectorAll('a, button, h1, h2').forEach(el => {
  el.addEventListener('mouseenter', () => c.classList.add('hover'));
  el.addEventListener('mouseleave', () => c.classList.remove('hover'));
});
```

## Comparação rápida

| Efeito | Tom | Casos |
|---|---|---|
| dot-follower | Versátil | Padrão, qualquer portfolio |
| magnetic | Sutil | CTA único de destaque |
| image-trail | Forte | Galeria de portfolio |
| blob | Experimental | Sites artísticos, branding |
| blend-mode | Editorial | Tipografia grande, alto contraste |

**Regra:** No máximo 1 efeito de cursor por site. Não combine.
