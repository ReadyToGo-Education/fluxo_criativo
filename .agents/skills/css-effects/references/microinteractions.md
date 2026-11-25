# Microinterações

10+ efeitos de feedback rápido em ações do usuário.

## Índice
heart-like · copy-feedback · success-flash · error-flash · confetti-burst · star-rating · badge-pulse · counter-increment · drag-feedback · scroll-to-top

---

### heart-like
**Visual:** Coração escala + muda cor + emite partículas no clique.
**Quando usar:** Botões de like (Instagram-style), favoritar produto, salvar item.
```html
<button class="heart-btn">
  <svg viewBox="0 0 24 24" class="heart-icon">
    <path d="M12 21s-7-4.5-9.5-9C1 9 2 5 6 5c2 0 3.5 1 4 2 0.5-1 2-2 4-2 4 0 5 4 3.5 7-2.5 4.5-9.5 9-9.5 9z"/>
  </svg>
  <span class="heart-count">42</span>
</button>
```
```css
.heart-btn {
  background: transparent;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #888;
  position: relative;
}
.heart-icon {
  width: 24px; height: 24px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.heart-btn.liked .heart-icon {
  fill: #ff3366;
  stroke: #ff3366;
  animation: heartPop 0.4s ease;
}
.heart-btn.liked { color: #ff3366; }
@keyframes heartPop {
  0% { transform: scale(1); }
  40% { transform: scale(1.4); }
  100% { transform: scale(1); }
}
.heart-particle {
  position: absolute;
  width: 6px; height: 6px;
  background: #ff3366;
  border-radius: 50%;
  pointer-events: none;
  animation: heartParticle 0.6s ease-out forwards;
}
@keyframes heartParticle {
  to {
    transform: translate(var(--dx), var(--dy)) scale(0);
    opacity: 0;
  }
}
```
```js
document.querySelectorAll('.heart-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('liked');
    const count = btn.querySelector('.heart-count');
    if (btn.classList.contains('liked')) {
      count.textContent = parseInt(count.textContent) + 1;
      // partículas
      for (let i = 0; i < 6; i++) {
        const p = document.createElement('span');
        p.className = 'heart-particle';
        const angle = (i / 6) * Math.PI * 2;
        p.style.setProperty('--dx', Math.cos(angle) * 30 + 'px');
        p.style.setProperty('--dy', Math.sin(angle) * 30 + 'px');
        btn.appendChild(p);
        setTimeout(() => p.remove(), 600);
      }
    } else {
      count.textContent = parseInt(count.textContent) - 1;
    }
  });
});
```

### copy-feedback
**Visual:** Botão copiar mostra "Copiado!" com check animado.
**Quando usar:** Códigos de cupom, links de compartilhamento, comandos de terminal.
```html
<button class="copy-btn" data-text="conteudo aqui">
  <span class="copy-default">📋 Copiar</span>
  <span class="copy-done">✓ Copiado!</span>
</button>
```
```css
.copy-btn {
  position: relative;
  padding: 10px 20px;
  background: #1a1a1a;
  border: 1px solid #333;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
  overflow: hidden;
  min-width: 130px;
}
.copy-btn span {
  display: block;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.copy-btn .copy-done {
  position: absolute;
  inset: 10px 20px;
  color: #00ff88;
  transform: translateY(150%);
}
.copy-btn.copied .copy-default { transform: translateY(-150%); }
.copy-btn.copied .copy-done { transform: translateY(0); }
```
```js
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(btn.dataset.text);
    btn.classList.add('copied');
    setTimeout(() => btn.classList.remove('copied'), 1800);
  });
});
```

### success-flash
**Visual:** Elemento pisca verde rapidamente confirmando ação.
**Quando usar:** Confirmação inline (item salvo, mensagem enviada, copiado).
```css
.success-flash {
  animation: successPulse 0.6s ease;
}
@keyframes successPulse {
  0% { box-shadow: 0 0 0 0 rgba(0,255,136,0); }
  30% { box-shadow: 0 0 0 8px rgba(0,255,136,0.4); background: rgba(0,255,136,0.1); }
  100% { box-shadow: 0 0 0 0 rgba(0,255,136,0); }
}
```
```js
function flashSuccess(el) {
  el.classList.add('success-flash');
  setTimeout(() => el.classList.remove('success-flash'), 600);
}
```

### error-flash
**Visual:** Elemento balança levemente + pisca vermelho.
**Quando usar:** Validação inválida, ação bloqueada, login errado.
```css
.error-flash {
  animation: errorShake 0.5s ease;
}
@keyframes errorShake {
  0%, 100% { transform: translateX(0); background: transparent; }
  20%, 60% { transform: translateX(-8px); background: rgba(255,51,102,0.1); }
  40%, 80% { transform: translateX(8px); }
}
```
```js
function flashError(el) {
  el.classList.add('error-flash');
  setTimeout(() => el.classList.remove('error-flash'), 500);
}
```

### confetti-burst
**Visual:** Explosão de confetes coloridos a partir de um ponto.
**Quando usar:** Conquistas (cadastro completo, compra confirmada, achievement, parabéns).
```css
.confetti {
  position: fixed;
  width: 8px;
  height: 14px;
  pointer-events: none;
  z-index: 9999;
  animation: confettiFall 1.5s ease-out forwards;
}
@keyframes confettiFall {
  0% { transform: translate(0, 0) rotate(0deg); opacity: 1; }
  100% { transform: translate(var(--dx), var(--dy)) rotate(720deg); opacity: 0; }
}
```
```js
function burstConfetti(x, y) {
  const colors = ['#ff00cc', '#00f0ff', '#3333ff', '#ffcc00', '#ff3366'];
  for (let i = 0; i < 30; i++) {
    const c = document.createElement('div');
    c.className = 'confetti';
    c.style.background = colors[Math.floor(Math.random() * colors.length)];
    c.style.left = x + 'px';
    c.style.top = y + 'px';
    const angle = Math.random() * Math.PI * 2;
    const dist = 100 + Math.random() * 100;
    c.style.setProperty('--dx', Math.cos(angle) * dist + 'px');
    c.style.setProperty('--dy', Math.sin(angle) * dist + Math.random() * 200 + 'px');
    document.body.appendChild(c);
    setTimeout(() => c.remove(), 1500);
  }
}
// Uso: burstConfetti(window.innerWidth/2, window.innerHeight/2);
```

### star-rating
**Visual:** Estrelas que preenchem ao hover; clique fixa a nota.
**Quando usar:** Avaliações de produto, feedback, ranking.
```html
<div class="rating">
  <span data-value="1">★</span>
  <span data-value="2">★</span>
  <span data-value="3">★</span>
  <span data-value="4">★</span>
  <span data-value="5">★</span>
</div>
```
```css
.rating {
  display: inline-flex;
  gap: 4px;
  font-size: 1.8rem;
  cursor: pointer;
}
.rating span {
  color: #333;
  transition: color 0.2s, transform 0.2s;
}
.rating span.hovered,
.rating span.active {
  color: #ffcc00;
  transform: scale(1.15);
  text-shadow: 0 0 10px rgba(255,204,0,0.5);
}
```
```js
document.querySelectorAll('.rating').forEach(rating => {
  const stars = rating.querySelectorAll('span');
  let active = 0;
  stars.forEach((star, i) => {
    star.addEventListener('mouseenter', () => {
      stars.forEach((s, j) => s.classList.toggle('hovered', j <= i));
    });
    star.addEventListener('click', () => {
      active = i + 1;
      stars.forEach((s, j) => s.classList.toggle('active', j < active));
    });
  });
  rating.addEventListener('mouseleave', () => {
    stars.forEach(s => s.classList.remove('hovered'));
  });
});
```

### badge-pulse
**Visual:** Badge de notificação com ponto pulsando.
**Quando usar:** Indicador de mensagens não lidas, notificações pendentes, status online.
```html
<button class="bell">
  🔔
  <span class="badge-dot"></span>
</button>
```
```css
.bell { position: relative; background: transparent; border: none; font-size: 1.5rem; cursor: pointer; }
.badge-dot {
  position: absolute;
  top: -2px; right: -2px;
  width: 10px; height: 10px;
  background: #ff3366;
  border-radius: 50%;
  border: 2px solid #0a0a0a;
}
.badge-dot::before {
  content: "";
  position: absolute; inset: -4px;
  background: #ff3366;
  border-radius: 50%;
  animation: badgePulse 1.5s ease-out infinite;
  z-index: -1;
}
@keyframes badgePulse {
  0% { transform: scale(0.8); opacity: 0.7; }
  100% { transform: scale(2); opacity: 0; }
}
```

### counter-increment
**Visual:** Número incrementa com animação flip (estilo contador de dígitos).
**Quando usar:** Contadores de likes, views, posts. Atualização em tempo real.
```html
<div class="counter-flip" data-value="0">0</div>
```
```css
.counter-flip {
  display: inline-block;
  transition: transform 0.3s ease;
}
.counter-flip.bumping {
  animation: counterBump 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes counterBump {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); color: #00f0ff; }
  100% { transform: scale(1); }
}
```
```js
function incrementCounter(el) {
  el.textContent = parseInt(el.textContent) + 1;
  el.classList.add('bumping');
  setTimeout(() => el.classList.remove('bumping'), 400);
}
```

### drag-feedback
**Visual:** Item dado drag fica semitransparente + escala leve.
**Quando usar:** Listas reordenáveis, kanban boards, upload por drag.
```css
.draggable {
  cursor: grab;
  transition: all 0.2s ease;
}
.draggable:active { cursor: grabbing; }
.draggable.dragging {
  opacity: 0.5;
  transform: scale(1.05) rotate(2deg);
  box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}
.drop-target {
  border: 2px dashed transparent;
  transition: all 0.2s;
}
.drop-target.drag-over {
  border-color: #00f0ff;
  background: rgba(0,240,255,0.05);
}
```

### scroll-to-top
**Visual:** Botão flutuante que aparece quando rola; animação smooth ao clicar.
**Quando usar:** Páginas longas (blogs, docs, e-commerce com muitos produtos).
```html
<button class="scroll-top" id="scrollTop">↑</button>
```
```css
.scroll-top {
  position: fixed;
  bottom: 30px; right: 30px;
  width: 50px; height: 50px;
  background: linear-gradient(135deg, #ff00cc, #00f0ff);
  color: #fff;
  border: none;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px);
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  z-index: 99;
}
.scroll-top.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
.scroll-top:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(255,0,204,0.4);
}
```
```js
const btn = document.getElementById('scrollTop');
window.addEventListener('scroll', () => {
  btn.classList.toggle('show', window.scrollY > 400);
});
btn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
```
