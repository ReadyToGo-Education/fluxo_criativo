# Video Hero Scroll-Controlled

Hero de página onde o vídeo MP4 é o elemento principal e a progressão dos frames é controlada pelo scroll do usuário (scrubbing). Padrão usado por Apple, Stripe, Vercel.

## Índice
video-hero-scroll-scrub · video-hero-bottom-fade · video-hero-side-text · video-hero-mobile-fallback · mp4-keyframe-optimization

---

### video-hero-scroll-scrub
**Visual:** Vídeo full-screen no topo da página. Conforme o usuário rola, o vídeo avança frame a frame até o último frame. Depois disso, a página continua nas próximas seções normalmente.
**Quando usar:** Hero impactante de SaaS, landing de produto premium, página de manifesto. Funciona quando o vídeo conta uma micro-narrativa (~10 a 30 segundos) que vale ser "lida" pelo scroll.
**Quando NÃO usar:** vídeos longos (>40s), páginas onde o usuário precisa converter rápido (e-commerce checkout), sites de conteúdo informativo onde o scroll precisa ser ágil.

**Estrutura HTML:**
```html
<div class="sect-hero">
  <div class="scroll-driver">
    <div class="sticky-stage">
      <video class="hero-video" muted playsinline preload="auto" src="assets/video-scrub.mp4"></video>
      <div class="hero-overlay"></div>
      <div class="hero-bottom-fade"></div>
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-headline">Headline aqui.</h1>
          <p class="hero-subhead">Subhead curta de apoio.</p>
        </div>
      </div>
      <span class="scroll-hint">Role para continuar</span>
    </div>
  </div>
</div>
```

**CSS:**
```css
.sect-hero { background: #000; }

.sect-hero .scroll-driver {
  position: relative;
  /* Calibrar entre 400vh (rapido) e 1200vh (lento/cinematografico).
     800vh e bom ponto de partida pra video de 20-30s. */
  height: 800vh;
  background: #000;
}

.sect-hero .sticky-stage {
  position: sticky;
  top: 0;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: #000;
}

.sect-hero .hero-video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
  background: #000;
  will-change: contents;
}

.sect-hero .hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    rgba(0,0,0,0.78) 0%,
    rgba(0,0,0,0.55) 30%,
    rgba(0,0,0,0.18) 65%,
    rgba(0,0,0,0) 100%
  );
  pointer-events: none;
  z-index: 1;
}

.sect-hero .hero-content {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  padding: 0 6vw;
  z-index: 2;
}

.sect-hero .hero-text {
  max-width: 620px;
  color: #FFF;
  font-family: 'Inter', system-ui, sans-serif;
}

.sect-hero .hero-headline {
  font-size: clamp(38px, 5.4vw, 72px);
  font-weight: 700;
  line-height: 1.04;
  letter-spacing: -0.035em;
  margin: 0 0 24px 0;
}

.sect-hero .hero-subhead {
  font-size: clamp(15px, 1.25vw, 19px);
  line-height: 1.55;
  color: rgba(255,255,255,0.78);
  margin: 0;
  max-width: 520px;
}

.sect-hero .scroll-hint {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(255,255,255,0.5);
  font-size: 11.5px;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  z-index: 2;
  animation: scrollHintFloat 2.4s ease-in-out infinite;
}
@keyframes scrollHintFloat {
  0%, 100% { transform: translate(-50%, 0); opacity: 0.5; }
  50% { transform: translate(-50%, 6px); opacity: 0.85; }
}

@media (max-width: 768px) {
  .sect-hero .hero-content { align-items: flex-end; padding: 0 24px 96px; }
  .sect-hero .hero-headline { font-size: clamp(30px, 7.6vw, 44px); }
  .sect-hero .scroll-hint { display: none; }
}

@media (prefers-reduced-motion: reduce) {
  .sect-hero .scroll-driver { height: 100vh; }
  .sect-hero .scroll-hint { animation: none; }
}
```

**JavaScript (com lerp/smoothing pra evitar jitter):**
```js
(function () {
  const driver = document.querySelector('.sect-hero .scroll-driver');
  const video  = document.querySelector('.sect-hero .hero-video');
  const hint   = document.querySelector('.sect-hero .scroll-hint');
  if (!driver || !video) return;

  const isTouch = matchMedia('(hover: none) and (pointer: coarse)').matches;
  const isiOS   = /iPad|iPhone|iPod/.test(navigator.userAgent);
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Mobile / iOS / reduced motion: scrubbing por scroll e instavel.
  // Fallback: autoplay loop muted, sem driver alto.
  if (isTouch || isiOS || reduced) {
    video.setAttribute('autoplay', '');
    video.setAttribute('loop', '');
    video.muted = true;
    video.playsInline = true;
    const tryPlay = () => video.play().catch(() => {});
    if (video.readyState >= 2) tryPlay();
    else video.addEventListener('loadeddata', tryPlay, { once: true });
    driver.style.height = '100vh';
    return;
  }

  // Desktop: scroll-controlled scrubbing com lerp.
  video.muted = true;
  video.playsInline = true;
  video.preload = 'auto';
  video.pause();

  let ready = false, duration = 0;
  let target = 0, current = 0, lastSet = -1, running = false;

  // Smoothing: 0.05 = lazy/cinematografico, 0.18 = responsivo. 0.07-0.12 e o ideal.
  const SMOOTH = 0.07;

  function onMeta() {
    if (!isFinite(video.duration) || video.duration <= 0) return;
    duration = video.duration;
    ready = true;
    readTarget();
    current = target;
    start();
  }
  if (video.readyState >= 1) onMeta();
  else video.addEventListener('loadedmetadata', onMeta, { once: true });

  function readTarget() {
    const rect = driver.getBoundingClientRect();
    const total = driver.offsetHeight - window.innerHeight;
    if (total <= 0) { target = 0; return; }
    target = Math.max(0, Math.min(1, -rect.top / total));
  }

  function tick() {
    const delta = target - current;
    current += delta * SMOOTH;
    if (Math.abs(delta) < 0.0005) { current = target; running = false; }

    if (ready) {
      const t = current * duration;
      // So seta currentTime se a diferenca for maior que 1 frame (~33ms).
      if (Math.abs(t - lastSet) > 0.033) {
        lastSet = t;
        try { video.currentTime = t; } catch (e) {}
      }
    }
    if (hint) hint.style.opacity = current > 0.04 ? '0' : '';
    if (running) requestAnimationFrame(tick);
  }
  function start() {
    if (!running) { running = true; requestAnimationFrame(tick); }
  }
  function onScroll() { if (ready) { readTarget(); start(); } }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
})();
```

**Pontos de calibração:**
- `height: 800vh` no `.scroll-driver` controla o quanto o usuário precisa rolar pra ver o vídeo todo. Mais alto = vídeo mais lento, mais cinematográfico.
- `SMOOTH = 0.07` controla a inércia. Menor = mais lazy, maior = mais responsivo.
- O `33ms` no threshold de `lastSet` evita seeks desnecessários (1 frame a 30fps).

**Importante:** o MP4 precisa estar otimizado pra scrubbing (keyframe em todo frame). Ver `mp4-keyframe-optimization` abaixo.

---

### video-hero-bottom-fade
**Visual:** Gradiente vertical no rodapé do hero que desaparece na cor de fundo da próxima seção.
**Quando usar:** sempre que o vídeo hero está acima de uma seção com fundo de cor diferente do preto. Cria quebra homogênea sem linha de corte visível.

```css
.sect-hero .hero-bottom-fade {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  height: 38vh;
  background: linear-gradient(
    180deg,
    rgba(10,10,13,0) 0%,
    rgba(10,10,13,0.45) 45%,
    rgba(10,10,13,0.85) 80%,
    #0A0A0D 100%
  );
  pointer-events: none;
  z-index: 1;
}
```

**Como adaptar:**
- Trocar `#0A0A0D` (e os `rgba(10,10,13,...)`) pela cor exata da próxima seção (`#FFFFFF` se a próxima for clara, qualquer hex)
- Aumentar `height` (até 50vh) para fade mais gradual; diminuir (25vh) para fade mais discreto
- Os 4 stops (0/45/80/100) garantem fade longo sem linha visível. Não simplifique pra 2 stops.

---

### video-hero-side-text
**Visual:** Headline + subhead alinhados à esquerda do hero, sobrepostos ao vídeo, com gradient overlay garantindo contraste.
**Quando usar:** padrão dominante. Texto à esquerda + foco visual (do vídeo) à direita = leitura ocidental natural.

Já incluído no `video-hero-scroll-scrub` acima (`.hero-overlay` faz o gradient horizontal preto-pra-transparente da esquerda pra direita, e `.hero-content` posiciona o texto à esquerda).

**Variações:**
- **Texto centralizado:** trocar `padding: 0 6vw` → `padding: 0`, e `align-items: center` no `.hero-content`. Trocar `.hero-overlay` por gradient radial centralizado.
- **Texto embaixo:** mantém só na variação mobile do snippet (`align-items: flex-end`).

---

### video-hero-mobile-fallback
**Visual:** Em dispositivos touch e iOS, o vídeo roda em autoplay loop muted no lugar do scrubbing.
**Quando usar:** sempre. Já incluído no JS do `video-hero-scroll-scrub`.

**Por quê:** iOS Safari tem suporte limitado a `video.currentTime` em vídeos inline. Forçar scrubbing nesses dispositivos resulta em frames travados ou pular. Autoplay loop muted é uniforme, leve e mantém o efeito visual.

---

### mp4-keyframe-optimization
**Visual:** N/A (otimização técnica do arquivo MP4).
**Quando usar:** sempre que aplicar `video-hero-scroll-scrub`. Sem esse passo, o scrubbing fica travado em vídeos com keyframes esparsos (padrão de export de Premiere, After Effects, Final Cut).

**Por quê:** quando o JS faz `video.currentTime = X`, o navegador precisa achar o keyframe anterior e decodar todos os frames até o alvo. Em MP4 padrão (keyframe a cada 30 frames ou mais), isso causa stutter visível. A solução é re-encodar com **um keyframe em cada frame** (`keyint=1`), o que torna qualquer seek instantâneo.

**Solução cross-platform:** o projeto inclui `scripts/otimizar-video-scrub.py`. Roda em Windows, macOS e Linux sem o usuário instalar ffmpeg manualmente (usa `imageio-ffmpeg` como fallback bundled).

```bash
# Windows
py -3 scripts/otimizar-video-scrub.py meus-produtos/{slug}/entregas/paginas/assets/video.mp4

# macOS / Linux
python3 scripts/otimizar-video-scrub.py meus-produtos/{slug}/entregas/paginas/assets/video.mp4
```

Saída: `video-scrub.mp4` no mesmo diretório, com keyframe em todo frame.

**Trade-off:** o arquivo otimizado pode ser 10-30% maior que o original (cada frame agora é I-frame), mas em vídeos curtos (10-30s) a diferença é desprezível, e o `crf 22` no script equilibra bem qualidade/tamanho. Em alguns casos o arquivo até diminui se o original tinha bitrate mais alto.

**Comando ffmpeg manual** (caso queira customizar):
```
ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 22 \
  -g 1 -keyint_min 1 -sc_threshold 0 \
  -pix_fmt yuv420p -an -movflags +faststart \
  output-scrub.mp4
```

- `-g 1`: GOP size 1 (keyframe em todo frame)
- `-keyint_min 1`: intervalo mínimo entre keyframes
- `-sc_threshold 0`: desabilita scene-cut detection (já temos keyframe sempre)
- `-an`: remove áudio (vídeo de hero é sempre muted)
- `-movflags +faststart`: move o moov atom pro início, libera o vídeo pra começar a tocar antes de baixar inteiro
