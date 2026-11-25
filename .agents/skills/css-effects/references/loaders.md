# Loaders e Estados de Carregamento

10+ efeitos para loadings, spinners e estados.

## Índice
spinner-classic · spinner-dots · spinner-pulse · spinner-bars · skeleton · shimmer-placeholder · progress-bar · progress-ring · page-transition · loading-overlay

---

### spinner-classic
**Visual:** Círculo girando com gap (estilo iOS/Material).
**Quando usar:** Loading rápido (<2s), botões de submit, indicadores inline.
```html
<div class="spinner"></div>
```
```css
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255,255,255,0.1);
  border-top-color: #00f0ff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
```

### spinner-dots
**Visual:** 3 pontos pulando em sequência (loading conversacional).
**Quando usar:** Chat, "digitando...", micro feedback assíncrono.
```html
<div class="dots-loader">
  <span></span><span></span><span></span>
</div>
```
```css
.dots-loader {
  display: inline-flex;
  gap: 6px;
}
.dots-loader span {
  width: 10px;
  height: 10px;
  background: #00f0ff;
  border-radius: 50%;
  animation: dotBounce 1.4s ease-in-out infinite;
}
.dots-loader span:nth-child(2) { animation-delay: 0.2s; }
.dots-loader span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dotBounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}
```

### spinner-pulse
**Visual:** Círculo pulsando suavemente.
**Quando usar:** Loading lento mas previsível, notificações pendentes, indicador de status.
```css
.pulse-loader {
  width: 40px;
  height: 40px;
  background: #ff00cc;
  border-radius: 50%;
  animation: pulseLoad 1.5s ease-in-out infinite;
}
@keyframes pulseLoad {
  0%, 100% { transform: scale(0.5); opacity: 0.5; }
  50% { transform: scale(1); opacity: 1; }
}
```

### spinner-bars
**Visual:** 5 barras verticais pulando como equalizador.
**Quando usar:** Loading de áudio/vídeo, processamento, upload em andamento.
```html
<div class="bars-loader">
  <span></span><span></span><span></span><span></span><span></span>
</div>
```
```css
.bars-loader {
  display: inline-flex;
  gap: 4px;
  align-items: center;
  height: 30px;
}
.bars-loader span {
  width: 4px;
  height: 100%;
  background: #00f0ff;
  border-radius: 2px;
  animation: barJump 1s ease-in-out infinite;
}
.bars-loader span:nth-child(2) { animation-delay: 0.1s; }
.bars-loader span:nth-child(3) { animation-delay: 0.2s; }
.bars-loader span:nth-child(4) { animation-delay: 0.3s; }
.bars-loader span:nth-child(5) { animation-delay: 0.4s; }
@keyframes barJump {
  0%, 100% { transform: scaleY(0.4); }
  50% { transform: scaleY(1); }
}
```

### skeleton-loader
**Visual:** Forma do conteúdo com cinza pulsando até o conteúdo carregar.
**Quando usar:** Cards, listas, perfis. Padrão moderno (Facebook, LinkedIn).
```html
<div class="skeleton skeleton-card">
  <div class="skeleton-line short"></div>
  <div class="skeleton-line"></div>
  <div class="skeleton-line"></div>
</div>
```
```css
.skeleton-card {
  padding: 20px;
  background: #141414;
  border-radius: 12px;
}
.skeleton-line {
  height: 14px;
  background: linear-gradient(90deg, #1a1a1a 0%, #252525 50%, #1a1a1a 100%);
  background-size: 200% 100%;
  border-radius: 4px;
  margin-bottom: 10px;
  animation: skeletonShine 1.5s linear infinite;
}
.skeleton-line.short { width: 60%; }
@keyframes skeletonShine {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### shimmer-placeholder
**Visual:** Brilho diagonal atravessando placeholder de imagem/conteúdo.
**Quando usar:** Imagens de produto/avatar carregando, cards de feed.
```css
.shimmer-placeholder {
  width: 100%;
  height: 200px;
  background: linear-gradient(90deg, #1a1a1a 25%, #2a2a2a 50%, #1a1a1a 75%);
  background-size: 200% 100%;
  animation: shimmerLoad 1.5s linear infinite;
  border-radius: 12px;
}
@keyframes shimmerLoad {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### progress-bar-animated
**Visual:** Barra de progresso linear com listras animadas.
**Quando usar:** Upload, instalação, multi-step forms, dia/mês de progresso.
```html
<div class="progress-bar"><div class="progress-fill" style="width: 65%;"></div></div>
```
```css
.progress-bar {
  width: 100%;
  height: 12px;
  background: #222;
  border-radius: 6px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff00cc, #00f0ff);
  background-size: 200% 100%;
  border-radius: 6px;
  transition: width 0.6s ease;
  animation: progressShine 2s linear infinite;
  position: relative;
}
.progress-fill::after {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(45deg, transparent 25%, rgba(255,255,255,0.2) 25%, rgba(255,255,255,0.2) 50%, transparent 50%, transparent 75%, rgba(255,255,255,0.2) 75%);
  background-size: 20px 20px;
  animation: progressStripes 1s linear infinite;
}
@keyframes progressShine {
  to { background-position: 200% 0; }
}
@keyframes progressStripes {
  to { background-position: 20px 0; }
}
```

### progress-ring
**Visual:** Círculo SVG animando preenchimento com gradiente + número no centro.
**Quando usar:** Stats, % completo, feedback visual de meta atingida.
```html
<div class="ring">
  <svg width="150" height="150">
    <defs>
      <linearGradient id="gr" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#ff00cc"/>
        <stop offset="100%" stop-color="#00f0ff"/>
      </linearGradient>
    </defs>
    <circle class="bg" cx="75" cy="75" r="70"/>
    <circle class="fg" cx="75" cy="75" r="70"/>
  </svg>
  <div class="ring-text">75%</div>
</div>
```
```css
.ring {
  width: 150px; height: 150px;
  position: relative;
}
.ring svg { transform: rotate(-90deg); }
.ring circle {
  fill: none;
  stroke-width: 8;
}
.ring .bg { stroke: #1f1f3a; }
.ring .fg {
  stroke: url(#gr);
  stroke-linecap: round;
  stroke-dasharray: 440;
  stroke-dashoffset: 440;
  animation: ringFill 2s ease-out forwards;
}
@keyframes ringFill { to { stroke-dashoffset: 110; } }  /* 110 = 75% preenchido */
.ring-text {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  font-weight: 800;
}
```
**Nota:** Calcule `stroke-dashoffset` como `440 - (440 * (porcentagem/100))`.

### page-transition
**Visual:** Cortina de cor sobe ao trocar de página, revelando o novo conteúdo.
**Quando usar:** Sites multi-página com client-side routing, portfolios.
```html
<div class="page-transition" id="transition"></div>
```
```css
.page-transition {
  position: fixed;
  inset: 0;
  background: linear-gradient(180deg, #ff00cc, #00f0ff);
  transform: translateY(100%);
  z-index: 9999;
  transition: transform 0.6s cubic-bezier(0.7, 0, 0.3, 1);
  pointer-events: none;
}
.page-transition.entering { transform: translateY(0); }
.page-transition.leaving { transform: translateY(-100%); }
```
```js
function navigateTo(url) {
  const t = document.getElementById('transition');
  t.classList.add('entering');
  setTimeout(() => {
    window.location.href = url;
  }, 600);
}
```

### loading-overlay
**Visual:** Overlay fullscreen com blur do background + spinner central.
**Quando usar:** Operações que bloqueiam UI (salvar, deletar, processar).
```html
<div class="loading-overlay" id="overlay">
  <div class="spinner"></div>
  <p>Processando...</p>
</div>
```
```css
.loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10,10,10,0.7);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  z-index: 9999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}
.loading-overlay.active {
  opacity: 1;
  visibility: visible;
}
.loading-overlay p { color: #fff; font-weight: 500; }
```
