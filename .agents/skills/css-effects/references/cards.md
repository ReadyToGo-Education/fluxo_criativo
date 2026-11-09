# Efeitos de Cards / Containers

20+ efeitos pra cards, containers e blocos de conteúdo.

## Índice
glow · lift · border-anim · spotlight · tilt · shine · liquid-blob · scan-line · noise · gradient-fill · corner-accent · ripple · magnetic · particles · border-reveal · grid-pattern · flip-3d · morph-bg · pulse-ring · expand · stack · spotlight-grid

---

### card-glow
**Visual:** Brilho ciano envolvendo o card no hover.
**Quando usar:** CTAs, cards destacados, elementos clicáveis premium.
```css
.card-glow { transition: all 0.3s ease; }
.card-glow:hover {
  border-color: #00f0ff;
  box-shadow: 0 0 30px rgba(0,240,255,0.4), 0 0 60px rgba(0,240,255,0.2);
}
```

### card-lift
**Visual:** Eleva o card com sombra projetada no hover.
**Quando usar:** Cards de feature, listings, qualquer elemento clicável. Padrão sólido.
```css
.card-lift { transition: transform 0.2s, box-shadow 0.2s; }
.card-lift:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.6);
}
```

### card-border-anim
**Visual:** Borda gradiente em movimento contínuo (estilo Vercel).
**Quando usar:** Card de plano destacado, feature em destaque, badges premium. Use em 1 card só.
```css
.card-border-anim {
  position: relative;
  background: #141414;
  z-index: 1;
}
.card-border-anim::before {
  content: "";
  position: absolute; inset: -1px;
  background: linear-gradient(45deg, #ff00cc, #00f0ff, #3333ff, #ff00cc);
  background-size: 300% 300%;
  border-radius: inherit;
  z-index: -1;
  animation: borderMove 3s linear infinite;
}
.card-border-anim::after {
  content: "";
  position: absolute; inset: 1px;
  background: #141414;
  border-radius: inherit;
  z-index: -1;
}
@keyframes borderMove {
  0% { background-position: 0% 50%; }
  100% { background-position: 300% 50%; }
}
```

### card-spotlight
**Visual:** Luz suave seguindo o cursor sobre o card.
**Quando usar:** Cards de produto premium (estilo Apple, Linear). Combina muito com card-tilt.
```css
.card-spotlight { position: relative; overflow: hidden; }
.card-spotlight::before {
  content: "";
  position: absolute; inset: 0;
  background: radial-gradient(circle 200px at var(--x, 50%) var(--y, 50%), rgba(0,240,255,0.15), transparent 60%);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}
.card-spotlight:hover::before { opacity: 1; }
```
```js
document.querySelectorAll('.card-spotlight').forEach(el => {
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--x', `${e.clientX - r.left}px`);
    el.style.setProperty('--y', `${e.clientY - r.top}px`);
  });
});
```

### card-tilt
**Visual:** Card inclina em 3D ao contrário do movimento do mouse.
**Quando usar:** Cards de feature destacados, hero cards. Combina com spotlight.
```css
.card-tilt {
  transition: transform 0.2s ease-out;
  transform-style: preserve-3d;
  will-change: transform;
}
```
```js
document.querySelectorAll('.card-tilt').forEach(el => {
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect();
    const x = e.clientX - r.left, y = e.clientY - r.top;
    const rx = ((y - r.height/2) / (r.height/2)) * -8;
    const ry = ((x - r.width/2) / (r.width/2)) * 8;
    el.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg) scale(1.02)`;
  });
  el.addEventListener('mouseleave', () => {
    el.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
  });
});
```

### card-shine
**Visual:** Brilho diagonal atravessa o card no hover.
**Quando usar:** Cards de produto, banners premium, anúncios. Sutil e elegante.
```css
.card-shine { position: relative; overflow: hidden; }
.card-shine::before {
  content: "";
  position: absolute;
  top: 0; left: -75%;
  width: 50%; height: 100%;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left 0.6s ease;
}
.card-shine:hover::before { left: 125%; }
```

### card-liquid-blob
**Visual:** Mancha colorida flutuando no canto, em loop suave.
**Quando usar:** Background de cards, seções decorativas, criar movimento sutil sem distrair.
```css
.card-liquid { position: relative; overflow: hidden; }
.card-liquid::before {
  content: "";
  position: absolute;
  width: 250px; height: 250px;
  background: linear-gradient(45deg, #ff00cc, #00f0ff);
  border-radius: 50%;
  filter: blur(50px);
  top: -80px; right: -80px;
  opacity: 0.4;
  animation: blob 8s ease-in-out infinite;
}
@keyframes blob {
  0%, 100% { transform: translate(0,0) scale(1); }
  33% { transform: translate(-30px, 30px) scale(1.2); }
  66% { transform: translate(30px, -20px) scale(0.9); }
}
```

### card-scan-line
**Visual:** Linha horizontal de scanner percorrendo o card de cima a baixo.
**Quando usar:** Tema cyberpunk, gaming, sci-fi, dashboards futuristas.
```css
.card-scan { position: relative; overflow: hidden; }
.card-scan::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, #00f0ff, transparent);
  box-shadow: 0 0 20px #00f0ff;
  animation: scan 3s linear infinite;
}
@keyframes scan {
  0% { top: 0; }
  100% { top: 100%; }
}
```

### card-noise
**Visual:** Textura granulada estilo filme analógico.
**Quando usar:** Visual editorial, mood vintage/cinema, dar peso visual a cards muito limpos.
```css
.card-noise { position: relative; }
.card-noise::after {
  content: "";
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.6'/%3E%3C/svg%3E");
  opacity: 0.15;
  mix-blend-mode: overlay;
  pointer-events: none;
}
```

### card-gradient-fill
**Visual:** Fundo gradiente preenche no hover.
**Quando usar:** CTAs, cards de plano premium, elementos de upsell.
```css
.card-gradient-fill {
  background: linear-gradient(135deg, #1a0033, #001a33);
  position: relative;
}
.card-gradient-fill::before {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(135deg, #ff00cc, #3333ff);
  opacity: 0;
  transition: opacity 0.4s ease;
}
.card-gradient-fill:hover::before { opacity: 0.4; }
```

### card-corner-accent
**Visual:** Cantos iluminados (estilo brackets) aparecem no hover.
**Quando usar:** Tema tech/sci-fi, dashboards, cards selecionáveis.
```css
.card-corner { position: relative; }
.card-corner::before, .card-corner::after {
  content: "";
  position: absolute;
  width: 30px; height: 30px;
  border: 2px solid #00f0ff;
  transition: all 0.4s ease;
  opacity: 0;
}
.card-corner::before {
  top: 12px; left: 12px;
  border-right: none; border-bottom: none;
  border-radius: 12px 0 0 0;
}
.card-corner::after {
  bottom: 12px; right: 12px;
  border-left: none; border-top: none;
  border-radius: 0 0 12px 0;
}
.card-corner:hover::before, .card-corner:hover::after {
  width: 50px; height: 50px;
  opacity: 1;
}
```

### card-ripple
**Visual:** Onda circular expandindo a partir do ponto de clique.
**Quando usar:** Botões, cards clicáveis. Material Design clássico.
```css
.card-ripple { position: relative; overflow: hidden; cursor: pointer; }
.ripple-effect {
  position: absolute;
  border-radius: 50%;
  background: rgba(0, 240, 255, 0.3);
  transform: scale(0);
  animation: rippleAnim 0.8s ease-out;
  pointer-events: none;
}
@keyframes rippleAnim {
  to { transform: scale(4); opacity: 0; }
}
```
```js
document.querySelectorAll('.card-ripple').forEach(el => {
  el.addEventListener('click', e => {
    const r = el.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.classList.add('ripple-effect');
    const size = Math.max(r.width, r.height);
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (e.clientX - r.left - size/2) + 'px';
    ripple.style.top = (e.clientY - r.top - size/2) + 'px';
    el.appendChild(ripple);
    setTimeout(() => ripple.remove(), 800);
  });
});
```

### card-magnetic
**Visual:** Card é "atraído" pela posição do cursor.
**Quando usar:** Botões CTA importantes, ícones sociais. Use com moderação (1-2 elementos).
```css
.card-magnetic {
  transition: transform 0.3s ease-out;
  will-change: transform;
}
```
```js
document.querySelectorAll('.card-magnetic').forEach(el => {
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect();
    const x = (e.clientX - r.left - r.width/2) * 0.15;
    const y = (e.clientY - r.top - r.height/2) * 0.15;
    el.style.transform = `translate(${x}px, ${y}px)`;
  });
  el.addEventListener('mouseleave', () => {
    el.style.transform = 'translate(0, 0)';
  });
});
```

### card-particles
**Visual:** Rede de partículas conectadas em movimento dentro do card.
**Quando usar:** Hero, seção de tech, fundos de cards "wow". É pesado — limite a 1 elemento por viewport.
```html
<div class="card-particles">
  <canvas></canvas>
  <div class="content">conteúdo</div>
</div>
```
```css
.card-particles { position: relative; overflow: hidden; background: #0a0a1a; }
.card-particles canvas { position: absolute; inset: 0; z-index: 1; }
.card-particles .content { position: relative; z-index: 2; }
```
```js
document.querySelectorAll('.card-particles canvas').forEach(canvas => {
  const ctx = canvas.getContext('2d');
  const parent = canvas.parentElement;
  const resize = () => { canvas.width = parent.offsetWidth; canvas.height = parent.offsetHeight; };
  resize();
  new ResizeObserver(resize).observe(parent);
  const particles = Array.from({length: 30}, () => ({
    x: Math.random() * canvas.width, y: Math.random() * canvas.height,
    vx: (Math.random()-0.5)*0.3, vy: (Math.random()-0.5)*0.3,
    r: Math.random()*1.5 + 0.5
  }));
  function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    particles.forEach((p,i) => {
      p.x += p.vx; p.y += p.vy;
      if (p.x<0||p.x>canvas.width) p.vx*=-1;
      if (p.y<0||p.y>canvas.height) p.vy*=-1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
      ctx.fillStyle = '#00f0ff';
      ctx.fill();
      particles.slice(i+1).forEach(p2 => {
        const d = Math.hypot(p.x-p2.x, p.y-p2.y);
        if (d < 80) {
          ctx.beginPath();
          ctx.moveTo(p.x,p.y); ctx.lineTo(p2.x,p2.y);
          ctx.strokeStyle = `rgba(0,240,255,${0.3*(1-d/80)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      });
    });
    requestAnimationFrame(draw);
  }
  draw();
});
```

### card-border-reveal
**Visual:** Linhas crescendo nas bordas opostas (top-esq → bottom-dir) no hover.
**Quando usar:** Cards de feature, listing de planos, tema minimalista.
```css
.card-border-reveal { position: relative; }
.card-border-reveal::before, .card-border-reveal::after {
  content: "";
  position: absolute;
  background: linear-gradient(90deg, transparent, #00f0ff, transparent);
  transition: transform 0.5s ease;
}
.card-border-reveal::before {
  top: 0; left: 0; width: 100%; height: 1px;
  transform: scaleX(0); transform-origin: left;
}
.card-border-reveal::after {
  bottom: 0; right: 0; width: 100%; height: 1px;
  transform: scaleX(0); transform-origin: right;
}
.card-border-reveal:hover::before,
.card-border-reveal:hover::after { transform: scaleX(1); }
```

### card-grid-pattern
**Visual:** Padrão de grade sutil no fundo, com fade nas bordas.
**Quando usar:** Background de cards/seções tech, dashboards, dar profundidade sem distrair.
```css
.card-grid-bg { position: relative; overflow: hidden; }
.card-grid-bg::before {
  content: "";
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(0,240,255,0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,240,255,0.08) 1px, transparent 1px);
  background-size: 20px 20px;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 70%);
  pointer-events: none;
}
```

### card-flip-3d
**Visual:** Card vira 180° revelando o verso no hover.
**Quando usar:** Cards de equipe (foto/bio), produto (frente/specs), perguntas/respostas.
```html
<div class="card-flip">
  <div class="flip-inner">
    <div class="flip-front">Frente</div>
    <div class="flip-back">Verso</div>
  </div>
</div>
```
```css
.card-flip { perspective: 1000px; }
.flip-inner {
  position: relative;
  width: 100%; min-height: 240px;
  transition: transform 0.7s;
  transform-style: preserve-3d;
}
.card-flip:hover .flip-inner { transform: rotateY(180deg); }
.flip-front, .flip-back {
  position: absolute; inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border-radius: 20px;
  padding: 32px;
}
.flip-back { transform: rotateY(180deg); }
```

### card-morph-bg
**Visual:** Forma orgânica colorida em mutação contínua no fundo.
**Quando usar:** Backgrounds decorativos, hero, criar movimento sutil.
```css
.card-morph { position: relative; overflow: hidden; }
.card-morph::before {
  content: "";
  position: absolute;
  width: 80%; height: 80%; top: 10%; left: 10%;
  background: linear-gradient(135deg, rgba(255,0,204,0.2), rgba(0,240,255,0.2));
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  animation: morph 8s ease-in-out infinite;
  filter: blur(30px);
}
@keyframes morph {
  0%,100% { border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }
  25% { border-radius: 58% 42% 75% 25% / 76% 46% 54% 24%; }
  50% { border-radius: 50% 50% 33% 67% / 55% 27% 73% 45%; }
  75% { border-radius: 33% 67% 58% 42% / 63% 68% 32% 37%; }
}
```

### card-pulse-ring
**Visual:** Anel ciano pulsando ao redor do card continuamente.
**Quando usar:** Notificações, CTAs urgentes, "novo!", chamar atenção pra um elemento.
```css
.card-pulse {
  animation: cardPulse 2s ease-in-out infinite;
}
@keyframes cardPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(0,240,255,0.4); }
  50% { box-shadow: 0 0 0 15px rgba(0,240,255,0); }
}
```

### card-expand
**Visual:** Card aumenta levemente e ocupa mais espaço no hover (push outros).
**Quando usar:** Galerias, listas de produtos, menu de planos onde quer destacar o focado.
```css
.card-expand { transition: flex 0.4s ease, transform 0.4s ease; flex: 1; }
.card-expand:hover { flex: 1.3; }
```
**Nota:** Funciona em flex container. Os outros cards naturalmente encolhem.

### card-stack
**Visual:** Cards empilhados levemente rotacionados; espalham no hover.
**Quando usar:** Coleções, "ver mais", grupos de imagens/depoimentos.
```html
<div class="card-stack">
  <div class="stack-item">1</div>
  <div class="stack-item">2</div>
  <div class="stack-item">3</div>
</div>
```
```css
.card-stack { position: relative; width: 250px; height: 320px; }
.stack-item {
  position: absolute;
  width: 100%; height: 100%;
  background: #141414;
  border: 1px solid #222;
  border-radius: 16px;
  transition: transform 0.4s ease;
}
.stack-item:nth-child(1) { transform: rotate(-4deg); }
.stack-item:nth-child(2) { transform: rotate(2deg); }
.stack-item:nth-child(3) { transform: rotate(-1deg); }
.card-stack:hover .stack-item:nth-child(1) { transform: rotate(-4deg) translateX(-30px); }
.card-stack:hover .stack-item:nth-child(2) { transform: rotate(2deg) translateY(-15px); }
.card-stack:hover .stack-item:nth-child(3) { transform: rotate(-1deg) translateX(30px); }
```

### card-spotlight-grid
**Visual:** Grid de cards onde só o que está sob o cursor fica iluminado, os outros escurecem.
**Quando usar:** Listagens de produto, features, plans. Foco no que o usuário olha.
```html
<div class="spotlight-grid">
  <div class="card">1</div>
  <div class="card">2</div>
  <div class="card">3</div>
</div>
```
```css
.spotlight-grid:hover .card { opacity: 0.4; transition: opacity 0.3s; }
.spotlight-grid .card:hover { opacity: 1; }
```
