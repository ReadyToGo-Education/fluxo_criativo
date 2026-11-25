# Recursos CDN Gratuitos para Páginas HTML Profissionais

Referência completa de recursos que funcionam em ARQUIVO HTML ÚNICO, sem build tools.
**Atenção:** Este arquivo complementa a skill `/copy-pagina`. As Regras Críticas de Qualidade (#1 a #6) da skill têm precedência.

---

## 1. CSS FRAMEWORKS (via CDN)

### Tailwind CSS v4 (Browser CDN)

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

- Funciona direto no navegador, sem build
- Apenas para desenvolvimento/protótipos
- Suporta todas as classes utilitárias do Tailwind

### Tailwind CSS v3 (Play CDN)

```html
<script src="https://cdn.tailwindcss.com"></script>
```

- Versão estável e amplamente testada
- Permite configuração inline via `tailwind.config`

### Pico CSS (~7KB gzipped). Classless

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
```

- Estiliza HTML semântico automaticamente
- Sem classes necessárias
- Temas claro/escuro automáticos
- Ideal para páginas simples e rápidas

### Water.css (~2KB gzipped). Classless

```html
<!-- Tema automático (claro/escuro) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css">
<!-- Apenas escuro -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css">
<!-- Apenas claro -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/light.min.css">
```

### Normalize.css (CSS Reset clássico)

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css">
```

---

## 2. BIBLIOTECAS DE ÍCONES (via CDN)

### Phosphor Icons (6000+ ícones, 6 estilos)

```html
<!-- Regular -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css">
<!-- Bold -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/bold/style.css">
<!-- Fill -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/fill/style.css">
<!-- Light -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/light/style.css">
```

Uso: `<i class="ph ph-house"></i>` | `<i class="ph-bold ph-house"></i>` | `<i class="ph-fill ph-house"></i>`

### Lucide Icons (1500+ ícones, leves)

```html
<script src="https://unpkg.com/lucide@latest"></script>
```

Uso: `<i data-lucide="home"></i>` + `<script>lucide.createIcons();</script>`

### Tabler Icons (5900+ ícones, MIT)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css">
```

Uso: `<i class="ti ti-home"></i>`

### Bootstrap Icons

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
```

Uso: `<i class="bi bi-house"></i>`

### Font Awesome Free

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
```

Uso: `<i class="fa-solid fa-house"></i>`

### Recomendação para páginas de vendas:

1. **Phosphor Icons**. mais versátil, 6 estilos, excelente qualidade
2. **Lucide**. moderno, leve, combina com Tailwind
3. **Tabler Icons**. maior quantidade, estilo consistente

---

## 3. GOOGLE FONTS. COMBINAÇÕES POR NICHO

**REGRA CRÍTICA: Body text SEMPRE sans-serif.** Fontes serifadas são apenas para headings em nichos específicos.

### Como incluir (template):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=FONTE1:wght@400;700&family=FONTE2:wght@400;600&display=swap" rel="stylesheet">
```

### Combinação 1: Finanças/Business (solidez)

```
Heading: Montserrat (600, 700, 800)
Body: Source Sans 3 (400, 600)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
```

### Combinação 2: Saúde/Bem-estar (acolhedora)

```
Heading: Nunito (700, 800)
Body: Nunito Sans (400, 600)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800&family=Nunito+Sans:wght@400;600&display=swap" rel="stylesheet">
```

### Combinação 3: Marketing/Lançamentos (impacto bold)

```
Heading: Bebas Neue (400)
Body: DM Sans (400, 500, 700)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
```

### Combinação 4: Artesanato/Feminino (heading serif elegante, body sans)

```
Heading: Playfair Display (700, 800)
Body: DM Sans (400, 500)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
```

### Combinação 5: Tech/Produtividade (moderna e limpa)

```
Heading: Space Grotesk (500, 700)
Body: Outfit (400, 500, 600)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
```

### Combinação 6: Coaching/Dev Pessoal (moderna e confiável)

```
Heading: Plus Jakarta Sans (600, 700, 800)
Body: Plus Jakarta Sans (400, 500)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

### Combinação 7: Educação/Cursos (impacto + legibilidade)

```
Heading: Fjalla One (400)
Body: Nunito (400, 600, 700)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Fjalla+One&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
```

### Combinação 8: Premium/High Ticket (heading serif, body sans)

```
Heading: Instrument Serif (400)
Body: Manrope (400, 500, 600)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
```

### Combinação 9: Lifestyle/Feminino alternativa (heading serif vintage, body sans)

```
Heading: Fraunces (700, 800)
Body: DM Sans (400, 500)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@700;800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
```

### Combinação 10: Premium alternativa (luxo acessível)

```
Heading: Prata (400)
Body: Manrope (400, 500, 600)
```

```html
<link href="https://fonts.googleapis.com/css2?family=Prata&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
```

### FONTES PROIBIDAS COMO BODY TEXT

**NUNCA** usar estas fontes no body (difíceis de ler em tela, cara de blog antigo ou de IA genérica):

- Lora
- Source Serif 4 / Source Serif Pro
- Merriweather
- Libre Baskerville (body)
- Inter (como heading. é a fonte padrão de IA)
- Roboto (cara de template genérico)
- Arial (sem personalidade)

---

## 4. IMAGENS. REGRAS OBRIGATÓRIAS

**LER `SKILL.md` → seção "Imagens Contextuais" antes de qualquer página.** Regra curta:

- ❌ `picsum.photos` (qualquer variante, incluindo `/seed/...`) é **proibido**. devolve imagem aleatória
- ❌ `source.unsplash.com` é proibido. serviço desligado
- ✅ Placeholder visual em HTML/CSS (gradiente + emoji + label da copy) é o padrão
- ✅ Unsplash com **ID específico** (`images.unsplash.com/photo-{ID}?...`) só quando o ID comprovadamente combina com a copy
- ✅ `i.pravatar.cc` para rostos de depoimento

### Fundos de Seção (sem foto aleatória)

```css
/* Opção 1: Overlay escuro sobre foto de Unsplash com ID específico */
.section-com-imagem {
  background:
    linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
    url('https://images.unsplash.com/photo-ID-ESPECIFICO?w=1920&q=80');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  color: #fff;
}

/* Opção 2: Overlay de marca sobre foto com ID específico */
.section-com-imagem-colorida {
  background:
    linear-gradient(135deg, rgba(45,24,16,0.85), rgba(74,44,26,0.9)),
    url('https://images.unsplash.com/photo-ID-ESPECIFICO?w=1920&q=80');
  background-size: cover;
  background-position: center;
  color: #fff;
}

/* Opção 3: CSS gradient artístico (sem imagem externa) */
.section-atmosferica {
  background-color: #0a0a0a;
  background-image:
    radial-gradient(at 20% 50%, hsla(28,100%,74%,0.15) 0px, transparent 50%),
    radial-gradient(at 80% 20%, hsla(189,100%,56%,0.08) 0px, transparent 50%),
    radial-gradient(at 50% 80%, hsla(355,85%,60%,0.06) 0px, transparent 50%);
}
```

**Temas de imagem por nicho:**

- Finanças: escritório, gráficos, paisagem urbana
- Saúde: natureza, alimentos, exercício
- Educação: livros, sala de aula, formatura
- Artesanato: mãos trabalhando, tecidos, ateliê, linhas coloridas
- Marketing: laptop, café, workspace criativo
- Feminino: flores, lifestyle, moda

### UI Faces (Avatares para depoimentos)

```
https://i.pravatar.cc/150?img=1
https://i.pravatar.cc/150?img=2
https://i.pravatar.cc/150?img=3
```

Gera avatares aleatórios. Ideal para depoimentos em páginas de vendas.

### DiceBear (Avatares SVG gerados)

```
https://api.dicebear.com/7.x/avataaars/svg?seed=Maria
https://api.dicebear.com/7.x/initials/svg?seed=VM
```

---

## 5. ANIMAÇÕES (CSS/JS via CDN)

### AOS. Animate on Scroll (~5.7KB)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css">
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
<script>AOS.init({ duration: 800, once: true });</script>
```

Uso em elementos: `<div data-aos="fade-up">Conteúdo</div>`
Animações disponíveis: fade-up, fade-down, fade-left, fade-right, zoom-in, zoom-out, flip-up, slide-up

### GSAP (Animações profissionais. gratuito para uso pessoal)

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
```

O mais poderoso, usado em sites premiados.

### Recomendação para páginas de vendas:

1. **AOS**. Melhor custo-benefício. Fácil de usar, leve, efeito profissional
2. **CSS puro com IntersectionObserver**. Zero dependência, máximo controle
3. **GSAP + ScrollTrigger**. Para páginas que precisam impressionar muito

### Animação CSS Pura (sem bibliotecas):

```css
/* Fade-in ao scroll com IntersectionObserver */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.active {
  opacity: 1;
  transform: translateY(0);
}
```

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('active');
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

---

## 6. UTILITÁRIOS CSS

### Modern CSS Reset (Josh Comeau. inline)

```css
*, *::before, *::after { box-sizing: border-box; }
* { margin: 0; }
body { line-height: 1.6; -webkit-font-smoothing: antialiased; }
img, picture, video, canvas, svg { display: block; max-width: 100%; }
input, button, textarea, select { font: inherit; }
p, h1, h2, h3, h4, h5, h6 { overflow-wrap: break-word; }
```

### Smooth Scroll

```css
html { scroll-behavior: smooth; }
```

### CSS Variables Base para Páginas de Vendas

```css
:root {
  /* Sistema de espaçamento (base 8px) */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;
  --space-4xl: 80px;
  --space-5xl: 120px;

  /* Tipografia. BODY SEMPRE SANS-SERIF */
  --font-heading: 'Playfair Display', serif;
  --font-body: 'DM Sans', sans-serif;

  /* Escala tipográfica */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;
  --text-5xl: 3rem;
  --text-6xl: 3.75rem;

  /* Bordas e sombras */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.1);
}
```

### Gradientes CSS Prontos para Uso

```css
/* Degradês premium para seções */
.gradient-ocean     { background: linear-gradient(135deg, #2b6cb0 0%, #2c5282 50%, #1a365d 100%); }
.gradient-warm      { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.gradient-nature    { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.gradient-dark      { background: linear-gradient(135deg, #0c0c1d 0%, #1a1a2e 50%, #16213e 100%); }
.gradient-gold      { background: linear-gradient(135deg, #f2c94c 0%, #d4a574 50%, #c4603c 100%); }
.gradient-trust     { background: linear-gradient(135deg, #1e3a5f 0%, #2b6cb0 100%); }

/* Mesh gradient (fundo atmosférico) */
.mesh-bg {
  background-color: #0a0a0a;
  background-image:
    radial-gradient(at 40% 20%, hsla(28,100%,74%,0.15) 0px, transparent 50%),
    radial-gradient(at 80% 0%, hsla(189,100%,56%,0.1) 0px, transparent 50%),
    radial-gradient(at 0% 50%, hsla(355,100%,93%,0.1) 0px, transparent 50%);
}
```

---

## 7. PADRÕES DE DESIGN. O QUE EVITAR E O QUE APLICAR

### PROIBIDO. Cara de IA/Lovable/v0 (EVITAR):

1. **Fonte serifada no body**. Lora, Source Serif no texto corrido
2. **Inter/Roboto como heading**. são as fontes padrão que toda IA usa
3. **Gradiente roxo-azul em fundo branco**. o clichê #1 de IA
4. **Cards brancos idênticos em fundo bege/cinza**. padrão Lovable
5. **Ícones em quadrados arredondados com fundo pastel**. padrão Lovable
6. **Espaçamento uniforme e previsível**. sem ritmo visual
7. **Todas as seções com mesmo padrão visual**. fundo claro → card → fundo claro → card
8. **Tudo flat sem texturas**. sem imagens de fundo, sem profundidade
9. **Paleta pastel sem contraste**. cores tímidas, sem personalidade
10. **Layout simétrico e genérico**. sem surpresa visual

### OBRIGATÓRIO. Cara de profissional (APLICAR):

1. **Body SEMPRE sans-serif**. DM Sans, Nunito, Source Sans 3, Outfit, Manrope
2. **Heading com personalidade**. Playfair, Fraunces, Bebas Neue, Fjalla One (conforme nicho)
3. **Paleta com cor dominante forte**. regra 60-30-10 (base-suporte-destaque)
4. **Seções visualmente DIFERENTES**. alternar 4+ tipos de fundo
5. **Imagens de fundo em 2+ seções**. Picsum + overlay ou CSS artístico
6. **Espaçamento generoso e irregular**. seções com 80-120px de gap, ritmo variado
7. **Texturas e profundidade**. sombras suaves, gradientes em camadas
8. **Hierarquia tipográfica dramática**. 15px body vs 48-56px heading
9. **Hover states que surpreendem**. não só mudar cor (mover, escalar, revelar)
10. **CTA com contraste máximo**. botão que se destaca contra o fundo
11. **Header com logo**. toda página começa com logotipo
12. **Texto em pt-BR com acentos**. SEMPRE

### Divisores entre Seções (usar pelo menos 2 tipos):

```css
/* SVG wave no topo da seção */
.section-wave::before {
  content: '';
  display: block;
  height: 60px;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 1200 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 60V30c200-30 400 0 600 0s400-30 600 0v30z' fill='%23ffffff'/%3E%3C/svg%3E") no-repeat center;
  background-size: cover;
  margin-top: -60px;
}

/* Linha decorativa com ícone */
.divider-icon {
  text-align: center;
  padding: 40px 0;
}
.divider-icon::before {
  content: '✦';
  font-size: 1.5rem;
  color: var(--color-accent);
  display: block;
}
```

---

## 8. TEMPLATE HTML BASE PARA PÁGINAS DE VENDAS

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nome do Produto. Transformação Principal</title>

  <!-- Fonts (escolher combinação por nicho) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">

  <!-- Icons (escolher UM) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/bold/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/fill/style.css">

  <!-- Animações -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css">

  <style>
    /* Reset + Variables + CSS aqui */
    /* REGRA: --font-body SEMPRE sans-serif */
    /* REGRA: cards min-width 320px, padding 28px+ */
    /* REGRA: entregáveis em 2 colunas, NÃO 3 */
    /* REGRA: pelo menos 4 tipos de fundo diferentes */
    /* REGRA: pelo menos 2 seções com imagem de fundo */
  </style>
</head>
<body>

  <!-- HEADER COM LOGO (obrigatório) -->
  <header class="site-header">
    <div class="container">
      <span class="logo-text">Nome do Produto</span>
      <!-- [Insira seu logotipo aqui. 180x50px] -->
    </div>
  </header>

  <!-- HERO (fundo escuro com gradiente) -->
  <!-- PROBLEMA (fundo claro) -->
  <!-- PALIATIVO (fundo com IMAGEM + overlay) -->
  <!-- CTA INTERMEDIÁRIO (fundo cor vibrante) -->
  <!-- MÉTODO (fundo claro com textura) -->
  <!-- PARA QUEM (fundo escuro) -->
  <!-- ENTREGÁVEIS (fundo claro, grid 2 colunas) -->
  <!-- BÔNUS (fundo gradiente) -->
  <!-- STACK DE VALOR (fundo escuro premium) -->
  <!-- DEPOIMENTOS (fundo com IMAGEM + overlay) -->
  <!-- GARANTIA (fundo claro) -->
  <!-- FAQ (fundo neutro) -->
  <!-- CTA FINAL (fundo escuro com gradiente) -->
  <!-- FOOTER -->

  <!-- Scripts no final -->
  <script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
  <script>AOS.init({ duration: 800, once: true });</script>
</body>
</html>
```

---

## 9. CHECKLIST PRÉ-ENTREGA DE PÁGINA

**Texto e idioma:**

- [ ] TODOS os textos em português com acentos corretos
- [ ] Nenhuma palavra sem acento na página inteira
- [ ] Revisar headlines, parágrafos, botões, FAQs, footer, labels

**Estrutura:**

- [ ] Header com logotipo no topo
- [ ] HTML válido, semântico, `lang="pt-BR"`, `charset="UTF-8"`

**Design e layout:**

- [ ] Fonte do body é SANS-SERIF (DM Sans, Nunito, Source Sans 3, Outfit, Manrope)
- [ ] Fonte serifada (se usada) é APENAS no heading
- [ ] Cards com min-width >= 320px no grid
- [ ] Texto em cards com font-size >= 0.95rem
- [ ] Padding interno de cards >= 28px
- [ ] Entregáveis/módulos em grid de 2 colunas (NÃO 3)
- [ ] NÃO parece design Lovable/v0 (sem cards idênticos em fundo bege)

**Variedade visual:**

- [ ] Pelo menos 4 tipos diferentes de fundo entre seções
- [ ] Pelo menos 2 seções com imagem de fundo (Picsum + overlay)
- [ ] Seções visualmente distintas (não repetir mesmo padrão)
- [ ] Pelo menos 1 divisor decorativo (wave SVG, linha, mudança abrupta)
- [ ] Pelo menos 3 animações de scroll (AOS ou CSS puro)

**Conversão:**

- [ ] Paleta com cor dominante forte (não pastéis tímidos)
- [ ] Botão CTA com contraste máximo contra o fundo
- [ ] Depoimentos com avatar (pravatar.cc)
- [ ] FAQ com accordion funcional em JS
- [ ] Smooth scroll ativado
- [ ] Mobile responsivo (testar em 375px)
- [ ] CTA flutuante no mobile
