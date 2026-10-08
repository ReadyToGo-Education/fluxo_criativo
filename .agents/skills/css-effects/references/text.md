# Efeitos de Texto

20+ efeitos pra títulos, parágrafos e palavras-chave.

## Índice
gradient · gradient-anim · glitch · neon · stroke · typing · wave · reveal-hover · split · 3d-stack · shimmer · scramble · highlight · fire · ice · rotate-words · letter-fall · double-shadow · spotlight-text · clip-bars · metallic

---

### text-gradient
**Visual:** Gradiente colorido fixo no texto.
**Quando usar:** Títulos hero, headings principais. Versão segura e elegante.
```css
.text-gradient {
  background: linear-gradient(90deg, #ff00cc, #00f0ff);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### text-gradient-anim
**Visual:** Gradiente em movimento contínuo dentro do texto.
**Quando usar:** Títulos hero de SaaS modernos (Vercel, Linear). Não usar em textos longos.
```css
.text-gradient-anim {
  background: linear-gradient(90deg, #ff00cc, #00f0ff, #ff00cc);
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientText 3s linear infinite;
}
@keyframes gradientText { to { background-position: 200% center; } }
```

### text-glitch
**Visual:** Distorção digital RGB (canais ciano e magenta separando) no hover.
**Quando usar:** Sites de games, cyberpunk, tech edgy. NÃO usar em corporativo.
```html
<h2 class="text-glitch" data-text="GLITCH">GLITCH</h2>
```
```css
.text-glitch { position: relative; color: #fff; }
.text-glitch:hover { animation: glitchMove 0.3s infinite; }
.text-glitch::before, .text-glitch::after {
  content: attr(data-text);
  position: absolute; top: 0; left: 0; width: 100%;
  opacity: 0;
}
.text-glitch:hover::before { animation: glitch1 0.3s infinite; color: #ff00cc; opacity: 0.8; }
.text-glitch:hover::after { animation: glitch2 0.3s infinite; color: #00f0ff; opacity: 0.8; }
@keyframes glitchMove {
  0%,100% { transform: translate(0); }
  20% { transform: translate(-2px, 1px); }
  40% { transform: translate(2px, -1px); }
  60% { transform: translate(-1px, -2px); }
  80% { transform: translate(1px, 2px); }
}
@keyframes glitch1 {
  0%,100% { transform: translate(0); clip-path: inset(0 0 0 0); }
  50% { transform: translate(-3px, 0); clip-path: inset(20% 0 50% 0); }
}
@keyframes glitch2 {
  0%,100% { transform: translate(0); clip-path: inset(0 0 0 0); }
  50% { transform: translate(3px, 0); clip-path: inset(60% 0 10% 0); }
}
```

### text-neon
**Visual:** Brilho ao redor das letras estilo letreiro de neon.
**Quando usar:** Bares, eventos noturnos, gaming, tema retrowave. Funciona melhor em fundo escuro.
```css
.text-neon {
  color: #fff;
  text-shadow: 0 0 5px #fff, 0 0 10px #00f0ff, 0 0 20px #00f0ff, 0 0 40px #00f0ff;
}
```

### text-stroke
**Visual:** Apenas contorno do texto; preenche no hover.
**Quando usar:** Headings ousados, design editorial, fashion. Precisa fonte bold.
```css
.text-stroke {
  color: transparent;
  -webkit-text-stroke: 2px #00f0ff;
  transition: color 0.4s;
}
.text-stroke:hover { color: #00f0ff; }
```

### text-typing
**Visual:** Efeito máquina de escrever em loop com cursor piscando.
**Quando usar:** Hero de site de dev/terminal, mostrar lista de skills variando, demos de IA.
```css
.text-typing {
  overflow: hidden;
  white-space: nowrap;
  border-right: 3px solid #00f0ff;
  width: fit-content;
  animation: typing 3s steps(8) infinite, blink 0.7s step-end infinite;
}
@keyframes typing {
  0%, 90% { width: 100%; }
  45% { width: 0; }
}
@keyframes blink { 50% { border-color: transparent; } }
```
**Nota:** Ajuste `steps(N)` pro número de letras da palavra.

### text-wave
**Visual:** Letras subindo em onda contínua.
**Quando usar:** Tom divertido, infantil, lúdico. Não usar em corporativo.
```html
<h2 class="text-wave" id="wave">Wave</h2>
```
```css
.text-wave span {
  display: inline-block;
  animation: wave 2s ease-in-out infinite;
}
@keyframes wave {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); color: #00f0ff; }
}
```
```js
const el = document.getElementById('wave');
el.innerHTML = [...el.textContent].map((c,i) =>
  `<span style="animation-delay:${i*0.1}s">${c===' '?'&nbsp;':c}</span>`
).join('');
```

### text-reveal-hover
**Visual:** Texto sobe e revela outro embaixo no hover.
**Quando usar:** Botões, links de menu, CTAs com mudança de mensagem.
```html
<h2 class="text-reveal">
  <span class="original">Reveal</span>
  <span class="hover">Hello!</span>
</h2>
```
```css
.text-reveal {
  position: relative;
  overflow: hidden;
  display: inline-block;
}
.text-reveal span { display: inline-block; transition: transform 0.4s ease; }
.text-reveal .original { color: #fff; }
.text-reveal .hover {
  position: absolute; top: 100%; left: 0;
  color: #ff00cc;
}
.text-reveal:hover .original,
.text-reveal:hover .hover { transform: translateY(-100%); }
```

### text-split
**Visual:** Letras saltam individualmente no hover.
**Quando usar:** Títulos divertidos, portfolios criativos.
```css
.text-split span {
  display: inline-block;
  transition: transform 0.3s ease, color 0.3s;
}
.text-split:hover span {
  transform: translateY(-8px) rotate(-5deg);
  color: #00f0ff;
}
```
**Precisa do mesmo JS de text-wave pra dividir letras.**

### text-3d-stack
**Visual:** Camadas de sombra criando profundidade 3D.
**Quando usar:** Headings ousados, posters, retrô anos 80, tipografia experimental.
```css
.text-3d {
  color: #fff;
  text-shadow:
    1px 1px 0 #ff00cc, 2px 2px 0 #ff00cc,
    3px 3px 0 #00f0ff, 4px 4px 0 #00f0ff,
    5px 5px 10px rgba(0,0,0,0.5);
  transition: text-shadow 0.3s, transform 0.3s;
}
.text-3d:hover {
  transform: translate(-3px, -3px);
  text-shadow:
    2px 2px 0 #ff00cc, 4px 4px 0 #ff00cc,
    6px 6px 0 #00f0ff, 8px 8px 0 #00f0ff,
    10px 10px 20px rgba(0,0,0,0.5);
}
```

### text-shimmer
**Visual:** Brilho metálico atravessando o texto continuamente.
**Quando usar:** Loaders, placeholder, headings premium/luxo, cards de produtos high-end.
```css
.text-shimmer {
  background: linear-gradient(90deg, #555 0%, #fff 50%, #555 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }
```

### text-scramble
**Visual:** Caracteres embaralham e descriptografam até formar a palavra final.
**Quando usar:** Hero de tech/AI, hacker theme, momentos de impacto. Roda na entrada e em hover.
```html
<h2 class="text-scramble" data-text="SCRAMBLE" id="scramble">SCRAMBLE</h2>
```
```css
.text-scramble { font-family: 'Courier New', monospace; color: #00f0ff; }
```
```js
const el = document.getElementById('scramble');
const chars = '!<>-_\\/[]{}—=+*^?#________';
const final = el.dataset.text;
function scramble() {
  let i = 0;
  const interval = setInterval(() => {
    el.textContent = final.split('').map((l,idx) =>
      idx < i ? final[idx] : chars[Math.floor(Math.random()*chars.length)]
    ).join('');
    if (i >= final.length) clearInterval(interval);
    i += 0.5;
  }, 40);
}
el.addEventListener('mouseenter', scramble);
scramble();
```

### text-highlight
**Visual:** Marca-texto pintando atrás da palavra ao passar mouse.
**Quando usar:** Destacar palavras-chave em parágrafos, títulos editoriais, blogs.
```css
.text-highlight {
  display: inline;
  background-image: linear-gradient(120deg, #ff00cc 0%, #00f0ff 100%);
  background-repeat: no-repeat;
  background-size: 0% 40%;
  background-position: 0 88%;
  transition: background-size 0.5s ease;
  padding: 0 4px;
}
.text-highlight:hover { background-size: 100% 40%; }
```

### text-fire
**Visual:** Texto em chamas (gradiente amarelo→laranja→vermelho) com brilho oscilante.
**Quando usar:** Promoções "HOT", gaming, eventos quentes/intensos. Visual forte.
```css
.text-fire {
  background: linear-gradient(180deg, #fff700 0%, #ff8800 50%, #ff0000 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 10px #ff8800);
  animation: fireFlicker 0.5s ease-in-out infinite alternate;
}
@keyframes fireFlicker {
  from { filter: drop-shadow(0 0 10px #ff8800); }
  to { filter: drop-shadow(0 0 20px #ff4400); }
}
```

### text-ice
**Visual:** Gradiente azul gelado com glow.
**Quando usar:** Frescor, inverno, tecnologia "cool", produtos refrigerantes.
```css
.text-ice {
  background: linear-gradient(180deg, #e0f7ff 0%, #00f0ff 50%, #0080ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 8px #00f0ff);
}
```

### text-rotate-words
**Visual:** Palavras alternando verticalmente em loop ("Design / Code / Build").
**Quando usar:** Hero mostrando variações de feature/serviço/profissão.
```html
<h2 class="text-rotate">
  <div class="words">
    <span>Design</span>
    <span>Code</span>
    <span>Build</span>
    <span>Design</span>
  </div>
</h2>
```
```css
.text-rotate { height: 2.4rem; overflow: hidden; }
.text-rotate .words {
  display: flex; flex-direction: column;
  animation: rotateWords 6s ease-in-out infinite;
}
.text-rotate .words span { height: 2.4rem; line-height: 2.4rem; color: #00f0ff; }
@keyframes rotateWords {
  0%, 25% { transform: translateY(0); }
  33%, 58% { transform: translateY(-2.4rem); }
  66%, 91% { transform: translateY(-4.8rem); }
  100% { transform: translateY(-7.2rem); }
}
```

### text-letter-fall
**Visual:** Letras caem do topo uma por uma na entrada.
**Quando usar:** Hero animado, carregamento de página, primeira impressão.
```css
.text-fall span {
  display: inline-block;
  opacity: 0;
  transform: translateY(-30px);
  animation: fallIn 0.5s forwards;
}
@keyframes fallIn {
  to { opacity: 1; transform: translateY(0); }
}
```
**Precisa de JS pra dividir letras (mesmo do text-wave) e adicionar `animation-delay: ${i*0.05}s` em cada span.**

### text-double-shadow
**Visual:** Sombra colorida deslocada que se afasta no hover.
**Quando usar:** Headings retrô, design pop, tipografia experimental.
```html
<h2 class="text-double" data-text="Layered">Layered</h2>
```
```css
.text-double {
  position: relative;
  color: #fff;
}
.text-double::before {
  content: attr(data-text);
  position: absolute;
  top: 4px; left: 4px;
  color: #ff00cc;
  z-index: -1;
  transition: all 0.3s;
}
.text-double:hover::before {
  top: 8px; left: 8px;
  color: #00f0ff;
}
```

### text-spotlight
**Visual:** Luz seguindo o cursor sobre o texto, escurece o resto.
**Quando usar:** Headings de seções, momento dramático no hero. Funciona bem em fundo escuro.
```css
.text-spotlight {
  background: radial-gradient(circle 100px at var(--mx, 50%) var(--my, 50%), #fff 0%, #333 60%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}
```
```js
document.querySelectorAll('.text-spotlight').forEach(el => {
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', `${((e.clientX-r.left)/r.width)*100}%`);
    el.style.setProperty('--my', `${((e.clientY-r.top)/r.height)*100}%`);
  });
});
```

### text-clip-bars
**Visual:** Distorção em barras horizontais clipadas (variante mais sutil do glitch).
**Quando usar:** Tema cyberpunk leve, transições, hover em headings tech.
```css
.text-bars { position: relative; color: #fff; }
.text-bars:hover { animation: barsClip 0.5s steps(2) infinite; }
@keyframes barsClip {
  0% { clip-path: inset(20% 0 60% 0); transform: translateX(-2px); }
  50% { clip-path: inset(50% 0 20% 0); transform: translateX(2px); color: #00f0ff; }
  100% { clip-path: inset(0 0 0 0); transform: translateX(0); }
}
```

### text-metallic
**Visual:** Acabamento cromado/metálico (gradiente vertical com linha de luz).
**Quando usar:** Logo, headings premium/luxo, automotivo, cosméticos high-end.
```css
.text-metallic {
  background: linear-gradient(180deg, #fff 0%, #999 50%, #fff 51%, #666 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}
```

### text-flip-letters
**Visual:** Cada letra gira 360° individualmente no hover.
**Quando usar:** Logos curtos, palavras de impacto, microinteração lúdica.
```html
<h2 class="text-flip"><span>F</span><span>L</span><span>I</span><span>P</span></h2>
```
```css
.text-flip { perspective: 400px; }
.text-flip span {
  display: inline-block;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}
.text-flip:hover span {
  transform: rotateY(360deg);
  color: #00f0ff;
}
.text-flip span:nth-child(1) { transition-delay: 0s; }
.text-flip span:nth-child(2) { transition-delay: 0.05s; }
.text-flip span:nth-child(3) { transition-delay: 0.1s; }
.text-flip span:nth-child(4) { transition-delay: 0.15s; }
```
