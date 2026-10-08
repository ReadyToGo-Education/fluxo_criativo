# Efeitos de Navegação

10+ efeitos para navbars, menus e links.

## Índice
nav-underline · nav-fill · hamburger-morph · sidebar-slide · navbar-shrink-on-scroll · mobile-menu-fullscreen · breadcrumb-hover · dropdown-fade · pill-active-indicator · navbar-blur

---

### nav-link-underline
**Visual:** Linha embaixo do link cresce de fora pra dentro no hover.
**Quando usar:** Padrão pra navbars, menus principais. Sutil e elegante.
```css
.nav-link {
  position: relative;
  color: #fff;
  text-decoration: none;
  padding: 8px 0;
}
.nav-link::after {
  content: "";
  position: absolute;
  bottom: 0; left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #ff00cc, #00f0ff);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.4s ease;
}
.nav-link:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}
.nav-link.active::after { transform: scaleX(1); }
```

### nav-link-fill
**Visual:** Cor de fundo desliza por baixo do link no hover.
**Quando usar:** Menus com items de mesmo peso, sidebars, pills.
```css
.nav-fill {
  position: relative;
  padding: 10px 18px;
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  overflow: hidden;
  z-index: 1;
}
.nav-fill::before {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(90deg, #ff00cc, #00f0ff);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
  z-index: -1;
}
.nav-fill:hover::before { transform: scaleX(1); }
.nav-fill:hover { color: #000; }
```

### hamburger-morph
**Visual:** Ícone hambúrguer (3 linhas) vira X com animação suave.
**Quando usar:** Menu mobile, sidebar toggle.
```html
<button class="hamburger">
  <span></span>
  <span></span>
  <span></span>
</button>
```
```css
.hamburger {
  width: 36px; height: 36px;
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  padding: 0;
}
.hamburger span {
  width: 24px;
  height: 2px;
  background: #fff;
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  transform-origin: center;
}
.hamburger.active span:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.hamburger.active span:nth-child(2) {
  opacity: 0;
  transform: scaleX(0);
}
.hamburger.active span:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}
```
```js
document.querySelector('.hamburger').addEventListener('click', e => {
  e.currentTarget.classList.toggle('active');
});
```

### sidebar-slide
**Visual:** Sidebar desliza da esquerda quando aberto.
**Quando usar:** Dashboards, painéis admin, menus mobile compridos.
```html
<aside class="sidebar" id="sidebar">conteúdo</aside>
<button onclick="document.getElementById('sidebar').classList.toggle('open')">≡</button>
```
```css
.sidebar {
  position: fixed;
  top: 0; left: 0;
  width: 280px;
  height: 100vh;
  background: #0a0a0a;
  border-right: 1px solid #222;
  transform: translateX(-100%);
  transition: transform 0.4s cubic-bezier(0.4,0,0.2,1);
  z-index: 1000;
}
.sidebar.open { transform: translateX(0); }
```

### navbar-shrink-on-scroll
**Visual:** Navbar fica menor (padding e fonte) ao rolar pra baixo.
**Quando usar:** Sites longos, header de blog/landing, mostrar mais conteúdo no scroll.
```css
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  padding: 24px 40px;
  background: rgba(10,10,10,0.7);
  backdrop-filter: blur(10px);
  transition: padding 0.3s ease, background 0.3s ease;
  z-index: 100;
}
.navbar.scrolled {
  padding: 12px 40px;
  background: rgba(10,10,10,0.95);
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
```
```js
window.addEventListener('scroll', () => {
  const nav = document.querySelector('.navbar');
  nav.classList.toggle('scrolled', window.scrollY > 50);
});
```

### mobile-menu-fullscreen
**Visual:** Menu mobile abre em tela cheia com fade + items entrando em cascata.
**Quando usar:** Mobile menu de portfolios e sites criativos. Mais imersivo que sidebar.
```html
<nav class="fullscreen-menu" id="fsmenu">
  <ul>
    <li>Home</li>
    <li>Sobre</li>
    <li>Trabalhos</li>
    <li>Contato</li>
  </ul>
</nav>
```
```css
.fullscreen-menu {
  position: fixed; inset: 0;
  background: #0a0a0a;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.4s ease;
  z-index: 999;
}
.fullscreen-menu.open {
  opacity: 1;
  visibility: visible;
}
.fullscreen-menu ul {
  list-style: none;
  text-align: center;
  padding: 0;
}
.fullscreen-menu li {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 20px 0;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s cubic-bezier(0.4,0,0.2,1);
}
.fullscreen-menu.open li {
  opacity: 1;
  transform: translateY(0);
}
.fullscreen-menu.open li:nth-child(1) { transition-delay: 0.1s; }
.fullscreen-menu.open li:nth-child(2) { transition-delay: 0.2s; }
.fullscreen-menu.open li:nth-child(3) { transition-delay: 0.3s; }
.fullscreen-menu.open li:nth-child(4) { transition-delay: 0.4s; }
```

### breadcrumb-hover
**Visual:** Breadcrumb (pão de queijo) onde o item destaca ao passar mouse.
**Quando usar:** Sites com hierarquia profunda (e-commerce, docs, blog categorias).
```html
<nav class="breadcrumb">
  <a href="#">Home</a>
  <span>/</span>
  <a href="#">Categoria</a>
  <span>/</span>
  <a href="#" class="current">Página atual</a>
</nav>
```
```css
.breadcrumb {
  display: flex;
  gap: 8px;
  align-items: center;
  color: #888;
  font-size: 0.9rem;
}
.breadcrumb a {
  color: #888;
  text-decoration: none;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.3s ease;
}
.breadcrumb a:hover {
  color: #00f0ff;
  background: rgba(0,240,255,0.1);
}
.breadcrumb a.current { color: #fff; pointer-events: none; }
```

### dropdown-fade
**Visual:** Dropdown abre com fade + slide pra baixo no hover.
**Quando usar:** Menus de navegação com sub-items, perfil de usuário, configurações.
```html
<div class="dropdown">
  <button class="dropdown-trigger">Mais ▾</button>
  <ul class="dropdown-menu">
    <li>Perfil</li>
    <li>Configurações</li>
    <li>Sair</li>
  </ul>
</div>
```
```css
.dropdown { position: relative; }
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: #141414;
  border: 1px solid #222;
  border-radius: 10px;
  list-style: none;
  padding: 8px 0;
  margin: 8px 0 0;
  min-width: 180px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
}
.dropdown:hover .dropdown-menu,
.dropdown:focus-within .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
.dropdown-menu li {
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.2s;
}
.dropdown-menu li:hover { background: rgba(0,240,255,0.1); color: #00f0ff; }
```

### pill-active-indicator
**Visual:** Pílula colorida desliza entre os items ativos do menu.
**Quando usar:** Tabs, filtros, navegação por categoria. Padrão Apple.
```html
<nav class="pill-nav">
  <a href="#" class="active">Tab 1</a>
  <a href="#">Tab 2</a>
  <a href="#">Tab 3</a>
  <span class="pill-indicator"></span>
</nav>
```
```css
.pill-nav {
  display: inline-flex;
  background: #141414;
  border-radius: 999px;
  padding: 4px;
  position: relative;
}
.pill-nav a {
  position: relative;
  z-index: 2;
  padding: 8px 20px;
  color: #888;
  text-decoration: none;
  transition: color 0.3s;
  border-radius: 999px;
}
.pill-nav a.active { color: #fff; }
.pill-indicator {
  position: absolute;
  top: 4px;
  height: calc(100% - 8px);
  background: linear-gradient(90deg, #ff00cc, #00f0ff);
  border-radius: 999px;
  transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
  z-index: 1;
}
```
```js
const nav = document.querySelector('.pill-nav');
const indicator = nav.querySelector('.pill-indicator');
const links = nav.querySelectorAll('a');
function moveIndicator(el) {
  indicator.style.left = el.offsetLeft + 'px';
  indicator.style.width = el.offsetWidth + 'px';
}
moveIndicator(nav.querySelector('.active'));
links.forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    links.forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    moveIndicator(link);
  });
});
```

### navbar-blur
**Visual:** Navbar com glassmorphism (blur) sobre o conteúdo.
**Quando usar:** Sites premium, hero com imagem/vídeo de fundo, design moderno.
```css
.navbar-blur {
  position: fixed;
  top: 0; left: 0; right: 0;
  padding: 16px 40px;
  background: rgba(10,10,10,0.6);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  z-index: 100;
}
```
