# Efeitos de Botões

15+ efeitos pra botões e CTAs.

## Índice
gradient-slide · fill-up · fill-circle · arrow-expand · 3d-press · magnetic-btn · ripple-btn · glow-pulse · border-draw · sliding-text · loading-state · neon-flicker · split-half · gradient-border · iconswap · shimmer-loader

---

### btn-gradient-slide
**Visual:** Gradiente desliza horizontalmente no hover.
**Quando usar:** CTAs principais, "Começar agora", "Inscrever-se".
```css
.btn-gradient {
  padding: 14px 32px;
  border: none;
  border-radius: 10px;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  background: linear-gradient(90deg, #ff00cc, #3333ff, #00f0ff, #ff00cc);
  background-size: 300% 100%;
  transition: background-position 0.5s;
}
.btn-gradient:hover { background-position: 100% 0; }
```

### btn-fill-up
**Visual:** Cor preenche de baixo pra cima no hover, texto inverte.
**Quando usar:** CTAs sutis, botões secundários elegantes, outline buttons.
```css
.btn-fill-up {
  padding: 14px 32px;
  background: transparent;
  border: 2px solid #00f0ff;
  color: #00f0ff;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  z-index: 1;
  overflow: hidden;
  transition: color 0.4s;
}
.btn-fill-up::before {
  content: "";
  position: absolute; inset: 0;
  background: #00f0ff;
  transform: scaleY(0);
  transform-origin: bottom;
  transition: transform 0.4s ease;
  z-index: -1;
}
.btn-fill-up:hover { color: #000; }
.btn-fill-up:hover::before { transform: scaleY(1); }
```

### btn-fill-circle
**Visual:** Círculo de cor expande do centro preenchendo o botão.
**Quando usar:** Botões de tema dark mode, alternativa interessante ao fill-up.
```css
.btn-fill-circle {
  padding: 14px 32px;
  background: transparent;
  border: 2px solid #ff00cc;
  color: #ff00cc;
  position: relative;
  overflow: hidden;
  transition: color 0.4s;
  z-index: 1;
}
.btn-fill-circle::before {
  content: "";
  position: absolute;
  width: 0; height: 0;
  background: #ff00cc;
  border-radius: 50%;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.5s, height 0.5s;
  z-index: -1;
}
.btn-fill-circle:hover { color: #fff; }
.btn-fill-circle:hover::before { width: 300px; height: 300px; }
```

### btn-arrow-expand
**Visual:** Seta dentro do botão se desloca pra direita no hover, padding aumenta.
**Quando usar:** "Continuar", "Próximo", "Saiba mais", "Ver tudo".
```html
<button class="btn-arrow">Continuar</button>
```
```css
.btn-arrow {
  padding: 14px 50px 14px 24px;
  background: #1a0a2e;
  border: 1px solid #ff00cc;
  color: #fff;
  border-radius: 10px;
  position: relative;
  cursor: pointer;
  transition: padding 0.3s, background 0.3s;
}
.btn-arrow::after {
  content: "→";
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  transition: right 0.3s;
}
.btn-arrow:hover {
  padding-right: 60px;
  background: #ff00cc;
}
.btn-arrow:hover::after { right: 14px; }
```

### btn-3d-press
**Visual:** Botão tem profundidade 3D; afunda no clique.
**Quando usar:** Botões lúdicos, gaming, e-commerce de jovem público.
```css
.btn-3d {
  padding: 14px 32px;
  background: #ff6b6b;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 6px 0 #c44;
  transition: all 0.1s;
}
.btn-3d:active {
  transform: translateY(6px);
  box-shadow: 0 0 0 #c44;
}
```

### btn-magnetic
**Visual:** Botão é atraído suavemente pelo cursor próximo.
**Quando usar:** CTA hero, botão único de destaque. NÃO usar em formulários.
```css
.btn-magnetic { transition: transform 0.3s ease-out; will-change: transform; }
```
```js
document.querySelectorAll('.btn-magnetic').forEach(btn => {
  btn.addEventListener('mousemove', e => {
    const r = btn.getBoundingClientRect();
    const x = (e.clientX - r.left - r.width/2) * 0.3;
    const y = (e.clientY - r.top - r.height/2) * 0.3;
    btn.style.transform = `translate(${x}px, ${y}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = 'translate(0, 0)';
  });
});
```

### btn-ripple
**Visual:** Onda Material Design no clique a partir do ponto clicado.
**Quando usar:** Botões clicáveis em geral. Feedback tátil clássico.
```css
.btn-ripple {
  padding: 14px 32px;
  background: #00f0ff;
  color: #000;
  border: none;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.btn-ripple .ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.6);
  transform: scale(0);
  animation: rippleBtn 0.6s linear;
  pointer-events: none;
}
@keyframes rippleBtn { to { transform: scale(4); opacity: 0; } }
```
```js
document.querySelectorAll('.btn-ripple').forEach(btn => {
  btn.addEventListener('click', e => {
    const r = btn.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.classList.add('ripple');
    const size = Math.max(r.width, r.height);
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (e.clientX - r.left - size/2) + 'px';
    ripple.style.top = (e.clientY - r.top - size/2) + 'px';
    btn.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});
```

### btn-glow-pulse
**Visual:** Brilho pulsando ao redor do botão chamando atenção.
**Quando usar:** CTA principal de landing, "ofertas", botões de destaque urgente.
```css
.btn-glow-pulse {
  padding: 14px 32px;
  background: #ff00cc;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  animation: glowPulse 2s ease-in-out infinite;
}
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 20px rgba(255,0,204,0.5); }
  50% { box-shadow: 0 0 40px rgba(255,0,204,0.9), 0 0 60px rgba(255,0,204,0.5); }
}
```

### btn-border-draw
**Visual:** Borda é desenhada (perímetro) no hover, partindo de um canto.
**Quando usar:** Botões secundários, links de menu importantes, tema editorial.
```html
<button class="btn-border-draw">Hover me</button>
```
```css
.btn-border-draw {
  position: relative;
  padding: 14px 32px;
  background: transparent;
  color: #fff;
  border: none;
  cursor: pointer;
}
.btn-border-draw::before, .btn-border-draw::after {
  content: "";
  position: absolute;
  background: #00f0ff;
  transition: all 0.4s ease;
}
.btn-border-draw::before {
  top: 0; left: 0;
  width: 0; height: 2px;
}
.btn-border-draw::after {
  bottom: 0; right: 0;
  width: 2px; height: 0;
}
.btn-border-draw:hover::before { width: 100%; }
.btn-border-draw:hover::after { height: 100%; }
```
**Nota:** Versão completa precisaria 4 elementos (uma por borda). Esta é a versão "L".

### btn-sliding-text
**Visual:** Texto desliza pra cima revelando outro texto embaixo.
**Quando usar:** Botões de download/comprar, mostrar CTA + preço, CTA + benefício.
```html
<button class="btn-slide">
  <span class="default">Comprar</span>
  <span class="hover">R$ 199</span>
</button>
```
```css
.btn-slide {
  position: relative;
  padding: 14px 32px;
  background: #00f0ff;
  color: #000;
  border: none;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  display: inline-block;
  height: 50px;
}
.btn-slide span {
  display: block;
  transition: transform 0.4s ease;
}
.btn-slide .hover {
  position: absolute;
  top: 100%; left: 0;
  width: 100%;
  padding: 14px 32px;
}
.btn-slide:hover .default,
.btn-slide:hover .hover { transform: translateY(-100%); }
```

### btn-loading-state
**Visual:** Botão vira spinner ao clicar; indica loading sem mudar tamanho.
**Quando usar:** Forms de submit, botões de ação assíncrona (login, salvar, enviar).
```html
<button class="btn-loading">Enviar</button>
```
```css
.btn-loading {
  padding: 14px 32px;
  background: #ff00cc;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  min-width: 140px;
  position: relative;
}
.btn-loading.loading {
  color: transparent;
  pointer-events: none;
}
.btn-loading.loading::after {
  content: "";
  position: absolute;
  width: 18px; height: 18px;
  top: 50%; left: 50%;
  margin: -9px 0 0 -9px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spinBtn 0.8s linear infinite;
}
@keyframes spinBtn { to { transform: rotate(360deg); } }
```
```js
document.querySelectorAll('.btn-loading').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.add('loading');
    setTimeout(() => btn.classList.remove('loading'), 2000);
  });
});
```

### btn-neon-flicker
**Visual:** Borda neon piscando ocasionalmente (estilo letreiro velho).
**Quando usar:** Tema retrô, gaming, eventos noturnos.
```css
.btn-neon {
  padding: 14px 32px;
  background: transparent;
  border: 2px solid #00f0ff;
  color: #00f0ff;
  font-weight: 700;
  text-shadow: 0 0 10px #00f0ff;
  box-shadow: 0 0 10px rgba(0,240,255,0.5), inset 0 0 10px rgba(0,240,255,0.2);
  animation: flicker 4s linear infinite;
}
@keyframes flicker {
  0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
    opacity: 1;
    text-shadow: 0 0 10px #00f0ff;
  }
  20%, 24%, 55% { opacity: 0.4; text-shadow: none; }
}
```

### btn-split-half
**Visual:** Botão dividido em 2 metades que separam levemente no hover.
**Quando usar:** Visual experimental, tema editorial moderno.
```html
<button class="btn-split"><span>Cli</span><span>que</span></button>
```
```css
.btn-split {
  display: inline-flex;
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 700;
}
.btn-split span {
  padding: 14px 20px;
  background: #ff00cc;
  color: #fff;
  transition: transform 0.3s ease;
}
.btn-split span:first-child { border-radius: 10px 0 0 10px; }
.btn-split span:last-child { border-radius: 0 10px 10px 0; }
.btn-split:hover span:first-child { transform: translateX(-6px); }
.btn-split:hover span:last-child { transform: translateX(6px); }
```

### btn-gradient-border
**Visual:** Borda gradiente animada ao redor do botão.
**Quando usar:** CTA premium, plano destacado, "edição limitada".
```css
.btn-gradient-border {
  position: relative;
  padding: 14px 32px;
  background: #141414;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  z-index: 1;
}
.btn-gradient-border::before {
  content: "";
  position: absolute; inset: -2px;
  background: linear-gradient(45deg, #ff00cc, #00f0ff, #3333ff, #ff00cc);
  background-size: 300% 300%;
  border-radius: inherit;
  z-index: -1;
  animation: borderGrad 3s linear infinite;
}
@keyframes borderGrad { to { background-position: 300% 50%; } }
```

### btn-iconswap
**Visual:** Ícone troca por outro no hover (rotação).
**Quando usar:** Botões de toggle (play/pause, mostrar/esconder), seguir/seguindo.
```html
<button class="btn-iconswap">
  <span class="icon-default">♡</span>
  <span class="icon-hover">♥</span>
  Curtir
</button>
```
```css
.btn-iconswap {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #1a0a2e;
  color: #fff;
  border: 1px solid #ff00cc;
  border-radius: 10px;
  cursor: pointer;
}
.btn-iconswap .icon-default,
.btn-iconswap .icon-hover {
  display: inline-block;
  transition: transform 0.3s ease, opacity 0.3s ease;
  width: 16px;
}
.btn-iconswap .icon-hover {
  position: absolute;
  opacity: 0;
  color: #ff00cc;
  transform: rotate(-90deg);
}
.btn-iconswap:hover .icon-default {
  opacity: 0;
  transform: rotate(90deg);
}
.btn-iconswap:hover .icon-hover {
  opacity: 1;
  transform: rotate(0);
}
```

### btn-shimmer-loader
**Visual:** Brilho deslizante ao longo do botão (estilo loading skeleton de luxo).
**Quando usar:** Botões "carregando" ou inalcançáveis temporariamente, premium.
```css
.btn-shimmer {
  padding: 14px 32px;
  background: linear-gradient(90deg, #2a0050, #4a0080, #2a0050);
  background-size: 200% 100%;
  color: #fff;
  border: none;
  border-radius: 10px;
  animation: shimmerBtn 2s linear infinite;
}
@keyframes shimmerBtn {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```
