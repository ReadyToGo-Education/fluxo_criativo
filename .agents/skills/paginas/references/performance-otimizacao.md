# Performance. Otimização para Páginas HTML Puras

Referência completa para auditoria e otimização de performance em páginas HTML estáticas (arquivo único, sem framework).
**Meta: 90+ no mobile e 100 no desktop no PageSpeed Insights / Lighthouse.**

**Atenção:** Este arquivo complementa a skill `/copy-pagina`. O visual da página NÃO pode ser alterado. layout, ordem de elementos, cores e espaçamentos devem permanecer intactos.

---

## FASE 1. Auditoria Completa

Ler o arquivo HTML indicado por completo. **Não alterar nada ainda.** Mapear todos os problemas nas categorias abaixo:

### Imagens e Mídia

- `<img>` sem atributos `width` e `height` explícitos (causa CLS)
- Imagens above-the-fold sem `fetchpriority="high"` e `decoding="async"`
- Imagens below-the-fold sem `loading="lazy"`
- Imagens grandes sem `srcset` e `sizes` para responsividade
- Iframes do YouTube/Vimeo carregando imediatamente (sem facade pattern)
- `<video>` sem `preload="none"` ou `preload="metadata"`
- Imagens decorativas sem `alt=""` (acessibilidade + SEO)
- Formato de imagem não otimizado (usar WebP/AVIF quando possível)

### CSS e Render Blocking

- CSS externo pesado bloqueando renderização (Tailwind CDN ~300KB+ de JS, AOS CSS, ícones)
- `@import` dentro de `<style>` (bloqueia render em cascata)
- CSS de bibliotecas de ícones carregando fonte inteira quando usa poucos ícones
- Fontes Google Fonts sem `display=swap` na URL
- Fontes sem `<link rel="preconnect">` para `fonts.googleapis.com` e `fonts.gstatic.com`
- CSS não-crítico carregando de forma síncrona (animações, ícones below-the-fold)
- Propriedades CSS pesadas: `background-attachment: fixed` (causa repaint constante no mobile)

### JavaScript e Carregamento

- Scripts no `<head>` sem `defer` ou `async`
- Tailwind CDN (`cdn.tailwindcss.com`). é um compilador JS de ~300KB que roda no browser
- Bibliotecas JS carregando antes do conteúdo (AOS, GSAP, Lucide)
- Scripts inline pesados executando no parse do HTML
- Event listeners em excesso sem delegação

### Layout Shifts (CLS)

- Imagens sem dimensões definidas (`width`/`height`)
- Fontes externas causando FOIT/FOUT sem `font-display: swap`
- Elementos dinâmicos (accordion, tabs) sem altura reservada
- Iframes sem `aspect-ratio` ou dimensões fixas
- Conteúdo injetado por JS acima de conteúdo existente

### Mobile Específico

- Elementos com largura > `100vw` (overflow horizontal)
- `background-attachment: fixed`. não funciona bem no iOS, causa jank
- Animações usando propriedades que causam repaint: `top`, `left`, `width`, `height`, `box-shadow`
- Touch targets menores que 48x48px
- Fontes abaixo de 16px (força zoom automático no iOS)
- Imagens grandes sem redimensionamento para telas menores

### Metadata e SEO

- `<title>` ausente ou genérico
- `<meta name="description">` ausente
- Open Graph tags ausentes (`og:title`, `og:description`, `og:image`)
- `<meta name="robots">` ausente
- `<link rel="canonical">` ausente
- Heading hierarchy quebrada (h1 → h3 sem h2)

---

## FASE 2. Diagnóstico Priorizado

Antes de qualquer alteração, apresentar:

```
CRÍTICO (maior impacto no score mobile):
- [problema] → [linha/trecho] → [solução]

ALTO:
- [problema] → [linha/trecho] → [solução]

MÉDIO:
- [problema] → [linha/trecho] → [solução]
```

Critérios de severidade:
- **CRÍTICO**: Tailwind CDN (JS render-blocking de 300KB+), imagens above-the-fold sem dimensões, CSS/JS bloqueando render, YouTube/Vimeo sem facade, `background-attachment: fixed` no mobile
- **ALTO**: imagens sem lazy load, fontes sem preconnect/swap, scripts sem defer, CLS > 0.1
- **MÉDIO**: metadata incompleta, acessibilidade, formatos de imagem não otimizados

---

## FASE 3. Implementação (CRÍTICO → ALTO → MÉDIO)

### Tailwind CDN → CSS Puro Inline

O problema mais comum nas páginas do workshop. O Tailwind CDN é um compilador JavaScript de ~300KB que:
1. Bloqueia a renderização enquanto carrega
2. Compila CSS no browser em tempo real
3. Destrói o score de performance no mobile

**Solução:** Converter todas as classes Tailwind para CSS puro dentro de `<style>`:

```html
<!-- ANTES (render-blocking, ~300KB de JS) -->
<script src="https://cdn.tailwindcss.com"></script>
<div class="flex items-center justify-center py-16 bg-gray-900 text-white">

<!-- DEPOIS (zero JS, CSS inline instantâneo) -->
<style>
  .hero { display: flex; align-items: center; justify-content: center; padding: 4rem 0; background: #1a202c; color: #fff; }
</style>
<div class="hero">
```

**Processo de conversão:**
1. Identificar todas as classes Tailwind usadas no HTML
2. Criar classes semânticas equivalentes em CSS puro (`.hero`, `.section-problem`, `.card`, `.btn-cta`)
3. Manter o visual 100% idêntico
4. Remover a tag `<script src="https://cdn.tailwindcss.com">` e qualquer `<script>` de config do Tailwind

### Imagens. Otimização Completa

```html
<!-- HERO (above-the-fold). carrega com prioridade -->
<img
  src="imagem.webp"
  alt="Descrição da imagem"
  width="800"
  height="600"
  fetchpriority="high"
  decoding="async"
>

<!-- BELOW-THE-FOLD. carrega sob demanda -->
<img
  src="imagem.webp"
  alt="Descrição da imagem"
  width="400"
  height="300"
  loading="lazy"
  decoding="async"
>

<!-- RESPONSIVO com srcset -->
<img
  src="imagem-800.webp"
  srcset="imagem-400.webp 400w, imagem-800.webp 800w, imagem-1200.webp 1200w"
  sizes="(max-width: 768px) 100vw, 800px"
  alt="Descrição"
  width="800"
  height="600"
  loading="lazy"
  decoding="async"
>
```

### YouTube/Vimeo. Facade Pattern (HTML Puro)

Substituir iframes por thumbnail clicável que carrega o player sob demanda:

```html
<style>
  .video-facade {
    position: relative;
    width: 100%;
    aspect-ratio: 16/9;
    background-size: cover;
    background-position: center;
    cursor: pointer;
    border-radius: 8px;
    overflow: hidden;
  }
  .video-facade::after {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 68px; height: 48px;
    background: rgba(0,0,0,.7);
    border-radius: 12px;
    /* Triângulo play via border */
  }
  .video-facade .play-icon {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 68px; height: 48px;
    display: flex; align-items: center; justify-content: center;
    background: rgba(255,0,0,.85);
    border-radius: 12px;
    transition: background .2s;
  }
  .video-facade:hover .play-icon { background: rgba(255,0,0,1); }
  .play-icon svg { fill: #fff; width: 24px; height: 24px; }
</style>

<div
  class="video-facade"
  style="background-image: url('https://img.youtube.com/vi/VIDEO_ID/hqdefault.jpg')"
  onclick="this.innerHTML='<iframe src=\'https://www.youtube.com/embed/VIDEO_ID?autoplay=1\' style=\'width:100%;height:100%;border:0\' allow=\'autoplay;encrypted-media\' allowfullscreen></iframe>'"
  aria-label="Reproduzir vídeo"
  role="button"
  tabindex="0"
>
  <div class="play-icon">
    <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
  </div>
</div>
```

### Fontes. Carregamento Otimizado

```html
<!-- OBRIGATÓRIO: preconnect ANTES do link da fonte -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Carregar apenas os pesos usados + display=swap -->
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
```

**Regras:**
- Sempre incluir `display=swap` na URL (evita FOIT. texto invisível enquanto a fonte carrega)
- Carregar apenas os pesos efetivamente usados (cada peso extra = ~20-50KB)
- Preconnect DEVE vir antes do `<link>` da fonte no `<head>`

### CSS Não-Crítico. Carregamento Assíncrono

Para bibliotecas de ícones e animações usadas abaixo da dobra:

```html
<!-- Ícones: carregar de forma assíncrona -->
<link rel="preload" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css"></noscript>

<!-- AOS CSS: carregar de forma assíncrona -->
<link rel="preload" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css"></noscript>
```

**Alternativa: substituir AOS por CSS puro** (elimina 2 requests HTTP):

```html
<style>
  .reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity .6s ease, transform .6s ease;
  }
  .reveal.active {
    opacity: 1;
    transform: translateY(0);
  }
</style>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(function(el) { observer.observe(el); });
  });
</script>
```

### Scripts. Carregamento Correto

```html
<!-- ANTES: scripts bloqueiam parsing -->
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>

<!-- DEPOIS: defer carrega em paralelo, executa após parse -->
<script defer src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>

<!-- OU: mover para o final do body (antes de </body>) -->
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
<script>AOS.init({ duration: 800, once: true });</script>
</body>
```

**Regra de ouro:** Todo `<script>` com `src` externo deve ter `defer` (ou estar no final do body). Nunca no `<head>` sem `defer`/`async`.

### Preconnect para Domínios Externos

Adicionar no `<head>`, antes de qualquer recurso externo:

```html
<!-- Fontes Google -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- CDNs usados (jsdelivr, cdnjs, unpkg) -->
<link rel="dns-prefetch" href="//cdn.jsdelivr.net">
<link rel="dns-prefetch" href="//cdnjs.cloudflare.com">

<!-- Imagens (Picsum, Pravatar) -->
<link rel="dns-prefetch" href="//picsum.photos">
<link rel="dns-prefetch" href="//i.pravatar.cc">
```

### CLS. Estabilidade Visual

```css
/* Imagens: SEMPRE com aspect-ratio ou width/height */
img {
  max-width: 100%;
  height: auto;
}

/* Iframes de vídeo: container com aspect-ratio */
.video-container {
  position: relative;
  width: 100%;
  aspect-ratio: 16/9;
}
.video-container iframe {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  border: 0;
}

/* Fontes: fallback com métricas similares */
body {
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

### Mobile. Fixes Específicos

```css
/* PROIBIDO no mobile. causa jank e scroll travado */
/* background-attachment: fixed; */

/* CORRETO: remover parallax no mobile */
@media (max-width: 768px) {
  .section-com-imagem {
    background-attachment: scroll;
  }
}

/* Animações: usar APENAS transform e opacity (GPU-accelerated) */
.card:hover {
  /* RUIM: */
  /* box-shadow: 0 20px 40px rgba(0,0,0,.3); */
  /* left: -5px; top: -5px; */

  /* BOM: */
  transform: translateY(-4px);
  opacity: .95;
}

/* Touch targets: mínimo 48x48px */
.btn, a, button {
  min-height: 48px;
  min-width: 48px;
}

/* Fontes: mínimo 16px no mobile (evita zoom automático no iOS) */
input, select, textarea {
  font-size: 16px;
}

/* Sem overflow horizontal */
html, body {
  overflow-x: hidden;
}
*, *::before, *::after {
  box-sizing: border-box;
}
```

### Metadata Completa

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nome do Produto. Transformação Principal</title>
  <meta name="description" content="Descrição de até 160 caracteres com a promessa principal do produto.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://seudominio.com/pagina">

  <!-- Open Graph (Facebook, WhatsApp, LinkedIn) -->
  <meta property="og:title" content="Nome do Produto. Transformação Principal">
  <meta property="og:description" content="Descrição curta da oferta.">
  <meta property="og:image" content="https://seudominio.com/imagem-og.jpg">
  <meta property="og:url" content="https://seudominio.com/pagina">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Nome do Produto">
  <meta name="twitter:description" content="Descrição curta da oferta.">
  <meta name="twitter:image" content="https://seudominio.com/imagem-og.jpg">
</head>
```

---

## Restrições Absolutas

1. **Visual intacto**. Proibido mudar layout, ordem de elementos, cores, espaçamentos ou tipografia. Se uma otimização exigir mudança visual, NÃO aplicar e documentar o motivo.

2. **Arquivo único**. A página deve continuar sendo um arquivo HTML único e autocontido. Não criar arquivos CSS/JS externos separados.

3. **Sem build tools**. Não exigir npm, webpack, vite ou qualquer ferramenta de build. Tudo funciona abrindo o HTML no navegador.

---

## FASE 4. Checklist Final

### Imagens e Mídia
- [ ] Todas as `<img>` com `width` e `height` explícitos
- [ ] Imagens above-the-fold com `fetchpriority="high"` e `decoding="async"`
- [ ] Imagens below-the-fold com `loading="lazy"`
- [ ] YouTube/Vimeo com facade pattern (carrega só no click)
- [ ] `<video>` com `preload="none"` ou `preload="metadata"`

### CSS e Fontes
- [ ] Tailwind CDN removido → CSS puro inline
- [ ] Fontes com `<link rel="preconnect">` antes do `<link>` da fonte
- [ ] `display=swap` na URL do Google Fonts
- [ ] Apenas pesos de fonte efetivamente usados
- [ ] CSS não-crítico (ícones, animações) carregado assincronamente
- [ ] Sem `@import` dentro de `<style>`
- [ ] `background-attachment: fixed` removido ou desativado no mobile

### JavaScript
- [ ] Todo `<script src>` com `defer` ou no final do body
- [ ] AOS substituído por IntersectionObserver CSS puro (quando possível)
- [ ] Nenhum script no `<head>` sem `defer`/`async`

### Layout Shifts (CLS)
- [ ] Todas as imagens com dimensões (zero CLS)
- [ ] Iframes com `aspect-ratio: 16/9`
- [ ] Sem overflow horizontal (`overflow-x: hidden` + `box-sizing: border-box`)
- [ ] Fontes com fallback de métricas similares

### Mobile
- [ ] `background-attachment: fixed` → `scroll` no mobile
- [ ] Animações via `transform`/`opacity` apenas
- [ ] Touch targets >= 48x48px
- [ ] Inputs com `font-size: 16px` (evita zoom iOS)
- [ ] Sem elementos > 100vw

### Metadata e SEO
- [ ] `<title>` descritivo
- [ ] `<meta name="description">` com até 160 caracteres
- [ ] Open Graph tags completas (title, description, image, url)
- [ ] `<meta name="robots">`
- [ ] `<link rel="canonical">`
- [ ] Hierarquia de headings correta (h1 → h2 → h3)

### Preconnect e DNS
- [ ] `preconnect` para fonts.googleapis.com e fonts.gstatic.com
- [ ] `dns-prefetch` para CDNs usados (jsdelivr, cdnjs, picsum, pravatar)

---

## Resultado Esperado

1. Diagnóstico documentado com problemas e severidade (CRÍTICO / ALTO / MÉDIO)
2. Código otimizado com todas as mudanças aplicadas
3. Checklist preenchido
4. Resumo das mudanças com impacto esperado no score

**Meta: 90+ mobile / 100 desktop no PageSpeed Insights.**
