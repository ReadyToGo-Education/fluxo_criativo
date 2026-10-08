# Backgrounds Animados

10+ efeitos para fundos de seções e páginas.

## Índice
aurora-gradient · mesh-gradient · animated-grid · gradient-orbs · dot-pattern · noise-bg · stars-field · matrix-rain · waves-bg · particles-network

---

### aurora-gradient
**Visual:** Gradiente colorido fluido em movimento (estilo aurora boreal).
**Quando usar:** Hero modernos, seções premium, fundos de SaaS (OpenAI, Anthropic).
```css
.aurora {
  position: relative;
  overflow: hidden;
  background: #0a0a0a;
}
.aurora::before {
  content: "";
  position: absolute;
  inset: -50%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(255,0,204,0.4), transparent 40%),
    radial-gradient(circle at 70% 60%, rgba(0,240,255,0.4), transparent 40%),
    radial-gradient(circle at 50% 80%, rgba(51,51,255,0.3), transparent 40%);
  filter: blur(80px);
  animation: auroraMove 20s ease-in-out infinite;
}
@keyframes auroraMove {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(-10%, 5%) rotate(120deg); }
  66% { transform: translate(5%, -10%) rotate(240deg); }
}
```

### mesh-gradient
**Visual:** Gradiente multicor estático mas fluido (estilo Stripe).
**Quando usar:** Hero corporativo moderno, sites de fintech, dashboards. Mais sóbrio que aurora.
```css
.mesh {
  background: 
    radial-gradient(at 20% 20%, #ff00cc 0px, transparent 50%),
    radial-gradient(at 80% 0%, #00f0ff 0px, transparent 50%),
    radial-gradient(at 0% 80%, #3333ff 0px, transparent 50%),
    radial-gradient(at 80% 80%, #ff0080 0px, transparent 50%),
    #0a0a0a;
}
```

### animated-grid
**Visual:** Grade que se move suavemente em diagonal.
**Quando usar:** Tema tech, sci-fi, dashboards, fundos de hero estilo Linear.
```css
.grid-bg {
  position: relative;
  overflow: hidden;
  background: #0a0a0a;
}
.grid-bg::before {
  content: "";
  position: absolute;
  inset: -50%;
  background-image:
    linear-gradient(rgba(0,240,255,0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,240,255,0.1) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 20s linear infinite;
}
@keyframes gridMove {
  to { transform: translate(40px, 40px); }
}
```

### gradient-orbs
**Visual:** Bolas grandes coloridas com blur flutuando lentamente.
**Quando usar:** Hero abstrato, página de manifesto, design criativo.
```css
.orbs-bg {
  position: relative;
  overflow: hidden;
  background: #0a0a0a;
}
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  animation: orbFloat 15s ease-in-out infinite;
}
.orb:nth-child(1) {
  width: 400px; height: 400px;
  background: #ff00cc;
  top: 10%; left: 20%;
}
.orb:nth-child(2) {
  width: 350px; height: 350px;
  background: #00f0ff;
  top: 50%; right: 15%;
  animation-delay: -5s;
}
.orb:nth-child(3) {
  width: 300px; height: 300px;
  background: #3333ff;
  bottom: 10%; left: 40%;
  animation-delay: -10s;
}
@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0); }
  33% { transform: translate(-80px, 60px); }
  66% { transform: translate(60px, -80px); }
}
```
```html
<div class="orbs-bg">
  <div class="orb"></div>
  <div class="orb"></div>
  <div class="orb"></div>
  <div class="content">conteúdo aqui</div>
</div>
```

### dot-pattern
**Visual:** Padrão de pontos sutil no fundo, com fade radial.
**Quando usar:** Fundo neutro mas com textura, alternativa ao grid.
```css
.dot-bg {
  position: relative;
  background: #0a0a0a;
}
.dot-bg::before {
  content: "";
  position: absolute; inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.08) 1px, transparent 1px);
  background-size: 24px 24px;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
}
```

### noise-bg
**Visual:** Textura de ruído/grão sobreposta no fundo.
**Quando usar:** Visual editorial, vintage, dar peso a designs muito limpos.
```css
.noise-bg {
  position: relative;
  background: #0a0a0a;
}
.noise-bg::after {
  content: "";
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.4'/%3E%3C/svg%3E");
  opacity: 0.1;
  pointer-events: none;
}
```

### stars-field
**Visual:** Campo de estrelas em movimento (parallax).
**Quando usar:** Sites espaciais, hero noturno, sci-fi.
```css
.stars-bg {
  position: relative;
  background: #000;
  overflow: hidden;
}
.stars-bg::before, .stars-bg::after {
  content: "";
  position: absolute; inset: 0;
  background-image:
    radial-gradient(2px 2px at 20% 30%, white, transparent),
    radial-gradient(1px 1px at 60% 70%, white, transparent),
    radial-gradient(2px 2px at 80% 20%, white, transparent),
    radial-gradient(1px 1px at 40% 80%, white, transparent),
    radial-gradient(2px 2px at 90% 50%, white, transparent),
    radial-gradient(1px 1px at 10% 60%, white, transparent);
  background-size: 200px 200px;
  animation: starsMove 20s linear infinite;
}
.stars-bg::after {
  background-size: 300px 300px;
  animation-duration: 30s;
  opacity: 0.5;
}
@keyframes starsMove { to { transform: translateY(-200px); } }
```

### matrix-rain
**Visual:** Chuva de caracteres verdes caindo (Matrix).
**Quando usar:** Tema hacker, gaming, intro dramática. Use raramente — é forte.
```html
<canvas id="matrix-canvas" class="matrix-bg"></canvas>
```
```css
.matrix-bg {
  position: absolute;
  inset: 0;
  opacity: 0.4;
}
```
```js
const c = document.getElementById('matrix-canvas');
const ctx = c.getContext('2d');
c.width = c.parentElement.offsetWidth;
c.height = c.parentElement.offsetHeight;
const chars = '01アイウエオカキクケコサシスセソ'.split('');
const fontSize = 14;
const cols = Math.floor(c.width / fontSize);
const drops = Array(cols).fill(1);
function drawMatrix() {
  ctx.fillStyle = 'rgba(0,0,0,0.05)';
  ctx.fillRect(0, 0, c.width, c.height);
  ctx.fillStyle = '#0f0';
  ctx.font = fontSize + 'px monospace';
  drops.forEach((y, i) => {
    const t = chars[Math.floor(Math.random() * chars.length)];
    ctx.fillText(t, i * fontSize, y * fontSize);
    if (y * fontSize > c.height && Math.random() > 0.975) drops[i] = 0;
    drops[i]++;
  });
}
setInterval(drawMatrix, 50);
```

### waves-bg
**Visual:** Ondas SVG animadas no fundo (rolando).
**Quando usar:** Hero de sites de bem-estar, meditação, água, surf, lifestyle.
```html
<div class="waves-bg">
  <svg viewBox="0 0 1440 320" preserveAspectRatio="none">
    <path d="M0,160L48,170.7C96,181,192,203,288,202.7C384,203,480,181,576,165.3C672,149,768,139,864,154.7C960,171,1056,213,1152,213.3C1248,213,1344,171,1392,149.3L1440,128L1440,320L0,320Z" fill="#00f0ff" opacity="0.3"/>
  </svg>
  <svg viewBox="0 0 1440 320" preserveAspectRatio="none">
    <path d="M0,160L48,170.7C96,181,192,203,288,202.7C384,203,480,181,576,165.3C672,149,768,139,864,154.7C960,171,1056,213,1152,213.3C1248,213,1344,171,1392,149.3L1440,128L1440,320L0,320Z" fill="#ff00cc" opacity="0.3"/>
  </svg>
</div>
```
```css
.waves-bg {
  position: relative;
  height: 300px;
  overflow: hidden;
}
.waves-bg svg {
  position: absolute;
  bottom: 0;
  width: 200%;
  height: 100%;
  animation: waveMove 10s linear infinite;
}
.waves-bg svg:nth-child(2) {
  animation-duration: 7s;
  animation-direction: reverse;
}
@keyframes waveMove {
  to { transform: translateX(-50%); }
}
```

### particles-network
**Visual:** Partículas conectadas por linhas, em movimento contínuo.
**Quando usar:** Hero de tech, fundo de seção "como funciona", IA. Pesado — limite a 1 por página.
**Veja em `cards.md` (card-particles)** — mesmo código, aplicar como background da seção.
