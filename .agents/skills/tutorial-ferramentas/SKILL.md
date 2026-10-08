# Skill: Tutorial de Ferramentas

Gera a Trilha de Ferramentas do workshop como pagina HTML interativa.

## Quando usar

Sempre que o usuario rodar `/tutorial-ferramentas`.

## O que fazer

### Passo 1. Garantir a pasta de entregas

Verifique se a pasta `entregas/` existe na raiz do projeto. Se nao existir, crie.

### Passo 2. Gerar o HTML

Leia o arquivo `tutoriais/trilha-ferramentas.html` e salve uma copia em `entregas/trilha-ferramentas.html`.

Se o arquivo fonte nao existir, gere o HTML completo abaixo e salve em `entregas/trilha-ferramentas.html`.

### Passo 3. Informar o usuario

Apos salvar o arquivo, informe:

```
Trilha de Ferramentas gerada com sucesso.

Arquivo salvo em: entregas/trilha-ferramentas.html

Para abrir:
- No VS Code: clique com o botao direito no arquivo > Open with Live Server
- Pelo explorador de arquivos: duble-clique no arquivo
- Pelo Claude Code: diga "abre o arquivo entregas/trilha-ferramentas.html no navegador"

A pagina tem checklist interativo. Seu progresso fica salvo no navegador automaticamente.
```

---

## HTML completo (fallback)

Se `tutoriais/trilha-ferramentas.html` nao existir, gere exatamente este conteudo:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trilha de Ferramentas. Mergulhando na IA</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600;700;900&family=Source+Code+Pro:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>
<style>
:root{
  --gray-25:#ffffff;
  --gray-50:#f8f8f8;
  --gray-75:#f3f3f3;
  --gray-100:#e9e9e9;
  --gray-200:#e1e1e1;
  --gray-300:#dadada;
  --gray-400:#c6c6c6;
  --gray-500:#8f8f8f;
  --gray-600:#717171;
  --gray-700:#505050;
  --gray-800:#292929;
  --gray-900:#131313;
  --blue-100:#f5f9ff;
  --blue-200:#e5f0fe;
  --blue-300:#cbe2fe;
  --blue-400:#accffd;
  --blue-500:#8eb9fc;
  --blue-600:#729efd;
  --blue-700:#5d89ff;
  --blue-800:#4b75ff;
  --blue-900:#3b63fb;
  --blue-1000:#274dea;
  --blue-1100:#1d3ecf;
  --red-100:#fff0f0;
  --red-400:#f15b5b;
  --red-500:#e21212;
  --red-600:#cc0000;
  --orange-100:#fef9e0;
  --orange-400:#d4b800;
  --orange-500:#9a8000;
  --orange-600:#6e5b00;
  --green-100:#edfcf1;
  --green-200:#d7f7e1;
  --green-400:#6be3a2;
  --green-500:#079755;
  --green-600:#036e45;
  --purple-500:#7c4dff;
  --indigo-500:#5c5ce0;
  --fuchsia-500:#d83790;
  --seafoam-500:#009c8b;
  --yellow-500:#f5c300;
  --bg:var(--gray-50);
  --panel:var(--gray-25);
  --ink:var(--gray-900);
  --ink-2:var(--gray-800);
  --ink-3:var(--gray-600);
  --line:var(--gray-100);
  --line-2:var(--gray-75);
  --brand:var(--blue-800);
  --brand-2:var(--blue-1000);
  --brand-soft:var(--blue-100);
  --ok:var(--green-500);
  --ok-soft:var(--green-100);
  --warn:var(--orange-500);
  --warn-soft:var(--orange-100);
  --danger:var(--red-500);
  --danger-soft:var(--red-100);
  --violet:var(--purple-500);
  --violet-soft:#ede8ff;
  --radius-s:4px;
  --radius-m:8px;
  --radius-l:12px;
  --radius-xl:16px;
  --radius-full:9999px;
  --radius:var(--radius-m);
  --sp-50:4px;
  --sp-100:8px;
  --sp-150:12px;
  --sp-200:16px;
  --sp-300:24px;
  --sp-400:32px;
  --sp-500:40px;
  --sp-600:48px;
  --sp-700:64px;
  --shadow-sm:0 1px 2px rgba(0,0,0,.05);
  --shadow-md:0 2px 6px rgba(0,0,0,.07), 0 0 1px rgba(0,0,0,.04);
  --shadow-lg:0 8px 20px rgba(0,0,0,.09), 0 1px 4px rgba(0,0,0,.05);
  --sans:"adobe-clean","Source Sans 3","Source Sans Pro",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  --mono:"adobe-clean-mono","Source Code Pro",ui-monospace,SFMono-Regular,Menlo,monospace;
  --t-heading-xxxl:48px;
  --t-heading-xxl:36px;
  --t-heading-xl:28px;
  --t-heading-l:22px;
  --t-heading-m:18px;
  --t-heading-s:16px;
  --t-heading-xs:14px;
  --t-body-xl:18px;
  --t-body-l:16px;
  --t-body-m:14px;
  --t-body-s:12px;
  --focus-ring:0 0 0 2px var(--gray-25), 0 0 0 4px var(--blue-800);
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:var(--t-body-m);line-height:1.5;-webkit-font-smoothing:antialiased;font-feature-settings:"ss01","cv01"}
a{color:var(--blue-1000);text-decoration:none;border-bottom:1px solid transparent;transition:border-color .13s,color .13s}
a:hover{color:var(--blue-1100);border-bottom-color:currentColor}
a:focus-visible{outline:none;border-radius:2px;box-shadow:var(--focus-ring)}
:focus-visible{outline:none}
.shell{display:grid;grid-template-columns:260px 1fr;min-height:100vh}
aside{position:sticky;top:0;height:100vh;overflow-y:auto;background:var(--panel);border-right:1px solid var(--line);padding:var(--sp-300) var(--sp-200)}
main{padding:var(--sp-600) var(--sp-500);max-width:960px}
aside::-webkit-scrollbar{width:6px}
aside::-webkit-scrollbar-thumb{background:var(--gray-300);border-radius:var(--radius-full)}
aside::-webkit-scrollbar-thumb:hover{background:var(--gray-400)}
.brand{display:flex;align-items:center;gap:10px;margin-bottom:var(--sp-300);padding:0 var(--sp-100)}
.brand-logo{width:32px;height:32px;border-radius:var(--radius-m);background:var(--blue-800);display:grid;place-items:center;color:#fff;flex-shrink:0}
.brand-logo .ph{font-size:20px}
.brand-name{font-weight:700;font-size:var(--t-body-m);letter-spacing:-.01em;color:var(--gray-900)}
.brand-sub{font-size:11px;color:var(--ink-3);text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin-top:1px}
.progress-wrap{background:var(--gray-75);border:1px solid var(--line);border-radius:var(--radius-l);padding:var(--sp-150) var(--sp-200);margin-bottom:var(--sp-300)}
.progress-label{display:flex;justify-content:space-between;align-items:baseline;font-size:var(--t-body-s);font-weight:700;color:var(--ink);margin-bottom:var(--sp-100)}
.progress-label #pct{color:var(--blue-800);font-size:var(--t-body-s);font-weight:800}
.progress-bar{height:4px;background:var(--gray-200);border-radius:var(--radius-full);overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--blue-800),var(--blue-700));width:0%;transition:width .35s cubic-bezier(.4,0,.2,1);border-radius:var(--radius-full)}
.progress-txt{font-size:11px;color:var(--ink-3);margin-top:var(--sp-100);font-weight:500}
.nav-title{font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--gray-500);margin:var(--sp-300) 0 var(--sp-100);padding:0 var(--sp-100)}
.nav-list{list-style:none;padding:0;margin:0}
.nav-item{display:flex;align-items:center;gap:10px;padding:var(--sp-100) var(--sp-150);border-radius:var(--radius-m);font-size:var(--t-body-m);color:var(--ink-3);cursor:pointer;transition:background .13s,color .13s;font-weight:500;position:relative;min-height:34px}
.nav-item:hover{background:var(--gray-75);color:var(--ink-2)}
.nav-item:focus-visible{box-shadow:var(--focus-ring)}
.nav-item.active{background:var(--blue-100);color:var(--blue-1000);font-weight:700}
.nav-item.active::before{content:"";position:absolute;left:0;top:8px;bottom:8px;width:3px;background:var(--blue-800);border-radius:0 var(--radius-full) var(--radius-full) 0}
.nav-dot{width:14px;height:14px;border-radius:50%;border:1.5px solid var(--gray-300);flex-shrink:0;display:grid;place-items:center;font-size:9px;transition:all .13s;background:var(--panel)}
.nav-item.done .nav-dot{background:var(--green-500);border-color:var(--green-500);color:#fff}
.nav-item.done .nav-dot::before{content:"✓";font-weight:700;font-size:8px}
.hero{margin-bottom:var(--sp-500);padding-bottom:var(--sp-400);border-bottom:1px solid var(--line)}
.hero-kicker{display:inline-flex;align-items:center;gap:6px;background:var(--blue-100);color:var(--blue-1000);padding:4px 12px;border-radius:var(--radius-full);font-size:11px;font-weight:800;margin-bottom:var(--sp-200);text-transform:uppercase;letter-spacing:.08em;border:1px solid var(--blue-300)}
.hero-kicker .ph{font-size:14px}
.hero h1{font-size:var(--t-heading-xxl);line-height:1.15;font-weight:700;margin:0 0 var(--sp-150);letter-spacing:-.025em;color:var(--gray-900)}
.hero-sub{font-size:var(--t-body-l);color:var(--ink-3);max-width:680px;line-height:1.6;margin:0}
.hero-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--sp-150);margin-top:var(--sp-400)}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius-l);padding:var(--sp-200) var(--sp-200);transition:border-color .13s,box-shadow .13s}
.stat:hover{border-color:var(--blue-400);box-shadow:var(--shadow-sm)}
.stat-value{font-size:var(--t-heading-l);font-weight:800;color:var(--gray-900);letter-spacing:-.025em;line-height:1.2}
.stat-label{font-size:var(--t-body-s);color:var(--ink-3);margin-top:4px;font-weight:500;line-height:1.4}
.callout{background:var(--gray-75);border:1px solid var(--gray-200);border-radius:var(--radius-l);padding:var(--sp-150) var(--sp-200);margin:var(--sp-200) 0;display:flex;gap:var(--sp-150);align-items:flex-start}
.callout .ph{color:var(--gray-500);flex-shrink:0;font-size:20px;margin-top:1px;line-height:1}
.callout.warn{background:var(--gray-75);border-color:var(--gray-200)}
.callout.warn .ph{color:var(--gray-600)}
.callout.ok{background:var(--gray-75);border-color:var(--gray-200)}
.callout.ok .ph{color:var(--gray-600)}
.callout b{color:var(--gray-900);font-weight:700}
.callout div{font-size:var(--t-body-m);color:var(--ink-2);line-height:1.5}
section{scroll-margin-top:var(--sp-300);margin-bottom:var(--sp-600)}
.section-head{display:flex;align-items:center;gap:var(--sp-200);margin-bottom:var(--sp-300);padding-bottom:var(--sp-200);border-bottom:2px solid var(--line)}
.section-num{min-width:36px;width:36px;height:36px;padding:0;border-radius:50%;background:var(--blue-800);color:#fff;display:grid;place-items:center;font-weight:800;font-size:14px;flex-shrink:0;letter-spacing:-.01em;box-shadow:0 0 0 4px var(--blue-100)}
.section-head h2{font-size:var(--t-heading-xl);margin:0;font-weight:700;letter-spacing:-.025em;color:var(--gray-900);line-height:1.2}
.section-head p{font-size:var(--t-body-m);color:var(--ink-3);margin:4px 0 0;line-height:1.5}
.tool{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius-l);padding:var(--sp-300);margin-bottom:var(--sp-200);scroll-margin-top:var(--sp-300);transition:border-color .15s,box-shadow .15s}
.tool:hover{border-color:var(--blue-400);box-shadow:var(--shadow-md)}
.tool-head{display:flex;align-items:flex-start;gap:var(--sp-200);margin-bottom:var(--sp-200)}
.tool-icon{width:44px;height:44px;border-radius:var(--radius-l);display:grid;place-items:center;flex-shrink:0;font-weight:800;font-size:18px;color:#fff;letter-spacing:-.02em}
.tool-icon.blue,.tool-icon.purple,.tool-icon.green,.tool-icon.pink,
.tool-icon.teal,.tool-icon.red,.tool-icon.indigo,.tool-icon.yellow,
.tool-icon.violet,.tool-icon.slate{background:var(--gray-700);color:#fff}
.tool-title{flex:1;min-width:0}
.tool-title h3{margin:0;font-size:var(--t-heading-m);font-weight:700;letter-spacing:-.015em;color:var(--gray-900);line-height:1.3}
.tool-title .sub{font-size:var(--t-body-m);color:var(--ink-3);margin-top:4px;line-height:1.55}
.checkbox-big{display:inline-flex;align-items:center;gap:var(--sp-100);padding:6px var(--sp-150);background:var(--panel);border:1px solid var(--gray-300);border-radius:var(--radius-m);font-size:var(--t-body-s);font-weight:600;color:var(--ink-3);cursor:pointer;transition:all .13s;user-select:none;flex-shrink:0}
.checkbox-big:hover{border-color:var(--gray-500);background:var(--gray-75);color:var(--ink-2)}
.checkbox-big:focus-within{box-shadow:var(--focus-ring)}
.checkbox-big input{display:none}
.checkbox-big .check-box{width:14px;height:14px;border:2px solid var(--gray-400);border-radius:3px;display:grid;place-items:center;font-size:10px;color:#fff;background:var(--panel);transition:all .13s}
.checkbox-big.checked{background:var(--green-100);border-color:var(--green-500);color:var(--green-600)}
.checkbox-big.checked .check-box{background:var(--green-500);border-color:var(--green-500)}
.checkbox-big.checked .check-box::before{content:"✓";font-weight:700;font-size:9px}
.tool-meta{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--sp-100);margin-bottom:var(--sp-200)}
.meta{background:var(--gray-75);border:1px solid var(--line);border-radius:var(--radius-m);padding:var(--sp-150)}
.meta-label{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--gray-500);font-weight:800;margin-bottom:4px}
.meta-value{font-size:var(--t-body-m);color:var(--gray-900);font-weight:600;line-height:1.3}
.meta-value.ok{color:var(--green-500)}
.meta-value.warn{color:var(--gray-700)}
.tool-section{margin:var(--sp-200) 0}
.tool-section h4{font-size:11px;font-weight:800;color:var(--gray-800);margin:0 0 var(--sp-150);text-transform:uppercase;letter-spacing:.1em;display:flex;align-items:center;gap:6px}
.tool-section h4 .ph{font-size:17px;color:var(--blue-800);line-height:1}
ol,ul{padding-left:20px;margin:var(--sp-100) 0}
ol li,ul li{margin-bottom:6px;font-size:var(--t-body-m);color:var(--ink-2);line-height:1.6}
ol li b,ul li b{color:var(--gray-900);font-weight:700}
.code{font-family:var(--mono);background:var(--gray-800);color:#f0f0f0;padding:var(--sp-150) var(--sp-200);border-radius:var(--radius-m);font-size:var(--t-body-m);line-height:1.6;overflow-x:auto;margin:var(--sp-150) 0;display:block;border:1px solid var(--gray-900)}
.code .c{color:var(--gray-500)}
.inline{font-family:var(--mono);background:var(--blue-100);color:var(--blue-1000);padding:2px 7px;border-radius:var(--radius-s);font-size:12.5px;border:1px solid var(--blue-300);font-weight:600}
.plans{display:grid;grid-template-columns:1fr 1fr;gap:var(--sp-150);margin:var(--sp-150) 0}
.plan{border:1px solid var(--line);border-radius:var(--radius-l);padding:var(--sp-200);background:var(--panel)}
.plan-free{background:var(--panel);border-color:var(--line)}
.plan-paid{background:var(--panel);border-color:var(--line)}
.plan-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:var(--sp-100);gap:var(--sp-100)}
.plan-name{font-weight:700;font-size:var(--t-body-m);letter-spacing:-.01em;color:var(--gray-900)}
.plan-price{font-weight:800;font-size:var(--t-heading-s);letter-spacing:-.02em}
.plan-free .plan-price{color:var(--green-500)}
.plan-paid .plan-price{color:var(--gray-700)}
.plan ul{margin:var(--sp-100) 0 0;padding-left:18px}
.plan ul li{font-size:var(--t-body-m);margin-bottom:3px}
.tag{display:inline-flex;align-items:center;padding:2px 8px;border-radius:var(--radius-full);font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.07em;margin-right:4px;border:1px solid transparent;line-height:1.6}
.tag-essential{background:var(--gray-75);color:var(--gray-800);border-color:var(--gray-300);font-weight:900}
.tag-optional{background:var(--gray-75);color:var(--gray-500);border-color:var(--gray-200)}
.tag-free{background:var(--gray-75);color:var(--gray-600);border-color:var(--gray-200)}
.tag-paid{background:var(--gray-75);color:var(--gray-600);border-color:var(--gray-200)}
.tag-freemium{background:var(--gray-75);color:var(--gray-600);border-color:var(--gray-200)}
.env-table{width:100%;border-collapse:collapse;font-size:var(--t-body-m);margin:var(--sp-200) 0;border:1px solid var(--line);border-radius:var(--radius-l);overflow:hidden}
.env-table th,.env-table td{padding:var(--sp-150) var(--sp-200);text-align:left;border-bottom:1px solid var(--line)}
.env-table tr:last-child td{border-bottom:none}
.env-table tr:hover td{background:var(--blue-100)}
.env-table th{background:var(--gray-75);font-weight:800;font-size:10px;text-transform:uppercase;color:var(--gray-500);letter-spacing:.1em}
.env-table td{font-size:13px;color:var(--ink-2)}
.env-table td.mono{font-family:var(--mono);color:var(--blue-1000);font-size:12.5px;font-weight:600}
footer{margin-top:var(--sp-700);padding-top:var(--sp-400);border-top:1px solid var(--line);text-align:center;color:var(--ink-3);font-size:var(--t-body-m)}
.menu-btn{display:none;position:fixed;top:var(--sp-200);right:var(--sp-200);width:40px;height:40px;background:var(--panel);border:1px solid var(--gray-300);border-radius:var(--radius-m);place-items:center;cursor:pointer;z-index:101;box-shadow:var(--shadow-md);transition:border-color .13s,background .13s}
.menu-btn:hover{background:var(--gray-75);border-color:var(--gray-500)}
.menu-btn:focus-visible{box-shadow:var(--shadow-md),var(--focus-ring)}
@media (max-width:900px){
  .shell{grid-template-columns:1fr}
  aside{position:fixed;top:0;left:-300px;z-index:100;transition:left .3s cubic-bezier(.4,0,.2,1);box-shadow:var(--shadow-lg);width:280px}
  aside.open{left:0}
  main{padding:var(--sp-300) var(--sp-200)}
  .hero h1{font-size:var(--t-heading-xl)}
  .hero-stats{grid-template-columns:repeat(2,1fr)}
  .tool-meta{grid-template-columns:1fr}
  .plans{grid-template-columns:1fr}
  .menu-btn{display:grid}
}
@media print{
  aside,.menu-btn,.checkbox-big{display:none}
  .shell{grid-template-columns:1fr}
  main{padding:20px;max-width:none}
  .tool{break-inside:avoid;box-shadow:none;border:1px solid #ddd}
  section{break-before:auto}
}
</style>
</head>
<body>

<button class="menu-btn" onclick="document.querySelector('aside').classList.toggle('open')">
  <i class="ph ph-list"></i>
</button>

<div class="shell">

<aside>
  <div class="brand">
    <div class="brand-logo"><i class="ph-fill ph-fill-waves"></i></div>
    <div>
      <div class="brand-name">Trilha de Ferramentas</div>
      <div class="brand-sub">Mergulhando na IA</div>
    </div>
  </div>

  <div class="progress-wrap">
    <div class="progress-label">
      <span>Seu progresso</span>
      <span id="pct">0%</span>
    </div>
    <div class="progress-bar"><div class="progress-fill" id="fill"></div></div>
    <div class="progress-txt" id="count">0 de 12 ferramentas configuradas</div>
  </div>

  <div class="nav-title">Essenciais</div>
  <ul class="nav-list">
    <li class="nav-item" data-target="claude"><span class="nav-dot"></span>Claude Code</li>
    <li class="nav-item" data-target="node"><span class="nav-dot"></span>Node.js</li>
  </ul>

  <div class="nav-title">Páginas e Publicação</div>
  <ul class="nav-list">
    <li class="nav-item" data-target="vercel"><span class="nav-dot"></span>Vercel</li>
    <li class="nav-item" data-target="lovable"><span class="nav-dot"></span>Lovable</li>
  </ul>

  <div class="nav-title">Conectores do Claude</div>
  <ul class="nav-list">
    <li class="nav-item" data-target="claude-chrome"><span class="nav-dot"></span>Claude in Chrome</li>
    <li class="nav-item" data-target="vercel-connector"><span class="nav-dot"></span>Conector Vercel</li>
  </ul>

  <div class="nav-title">Imagem e Vídeo</div>
  <ul class="nav-list">
    <li class="nav-item" data-target="heygen"><span class="nav-dot"></span>HeyGen</li>
    <li class="nav-item" data-target="freepik"><span class="nav-dot"></span>Freepik (Magnific)</li>
    <li class="nav-item" data-target="openrouter"><span class="nav-dot"></span>OpenRouter</li>
    <li class="nav-item" data-target="whisk"><span class="nav-dot"></span>Google Whisk</li>
    <li class="nav-item" data-target="canva"><span class="nav-dot"></span>Canva</li>
  </ul>

  <div class="nav-title">Automações</div>
  <ul class="nav-list">
    <li class="nav-item" data-target="apify"><span class="nav-dot"></span>Apify</li>
  </ul>

  <div class="nav-title">Referência</div>
  <ul class="nav-list">
    <li class="nav-item" data-target="env"><span class="nav-dot" style="border:none;background:var(--brand-soft);color:var(--brand)">.env</span>Arquivo de chaves</li>
    <li class="nav-item" data-target="custo"><span class="nav-dot" style="border:none;background:var(--brand-soft);color:var(--brand)">$</span>Quanto vou gastar</li>
  </ul>
</aside>

<main>

<div class="hero">
  <div class="hero-kicker">
    <i class="ph ph-lightning"></i>
    Guia oficial de setup
  </div>
  <h1>Tudo que você precisa instalar para rodar o Mergulhando na IA</h1>
  <p class="hero-sub">Esta é a trilha completa de ferramentas. Cada bloco mostra o que a ferramenta faz, qual plano assinar, quanto custa e como configurar. Marque cada item conforme avança. Seu progresso fica salvo neste navegador, mesmo que feche a aba.</p>

  <div class="hero-stats">
    <div class="stat"><div class="stat-value">12</div><div class="stat-label">Ferramentas no total</div></div>
    <div class="stat"><div class="stat-value">2</div><div class="stat-label">Essenciais e obrigatórias</div></div>
    <div class="stat"><div class="stat-value">9</div><div class="stat-label">Com plano gratuito</div></div>
  </div>
</div>

<div class="callout">
  <i class="ph ph-lightbulb"></i>
  <div><b>Como usar esta trilha.</b> Siga a ordem do menu lateral. Cada ferramenta tem um botão "marcar como feito" no topo. O sistema funciona 100% só com o Claude Code instalado. Os conectores e as demais ferramentas liberam automações específicas de cada comando do workshop.</div>
</div>

<div class="callout ok">
  <i class="ph ph-piggy-bank"></i>
  <div><b>Começa de graça.</b> Dá para fazer o workshop inteiro usando só os planos gratuitos. Depois que validar os primeiros resultados, você assina o que fizer sentido para o seu volume.</div>
</div>

<section id="essenciais">
  <div class="section-head">
    <div class="section-num">1</div>
    <div>
      <h2>Essenciais</h2>
      <p>O Claude Code é obrigatório. O Node entra só quando você for rodar geração de vídeo.</p>
    </div>
  </div>

  <div class="tool" id="claude">
    <div class="tool-head">
      <div class="tool-icon blue">C</div>
      <div class="tool-title">
        <h3>Claude Code</h3>
        <div class="sub">O cérebro do workshop. É o app da Anthropic para Mac e Windows que executa todos os comandos (barra), skills e agentes deste projeto, sem você precisar mexer em terminal.</div>
      </div>
      <label class="checkbox-big" data-item="claude"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-essential">Obrigatória</span></div></div>
      <div class="meta"><div class="meta-label">Plano</div><div class="meta-value warn">Pago (Claude Max)</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">Tudo</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-plus"></i>Criar conta na Anthropic</h4>
      <ol>
        <li>Acesse <a href="https://claude.ai" target="_blank">claude.ai</a></li>
        <li>Clique em <b>Sign up</b> no canto superior direito</li>
        <li>Crie a conta com email ou Google</li>
        <li>Confirme o email</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-credit-card"></i>Qual plano assinar</h4>
      <div class="plans">
        <div class="plan plan-free">
          <div class="plan-head"><div class="plan-name">Free</div><div class="plan-price">R$ 0</div></div>
          <ul>
            <li>Não serve para o Claude Code</li>
            <li>Apenas para testar o chat no site</li>
            <li>Bloqueia no primeiro comando pesado</li>
          </ul>
        </div>
        <div class="plan plan-paid">
          <div class="plan-head"><div class="plan-name">Max (recomendado)</div><div class="plan-price">R$ 550/mês</div></div>
          <ul>
            <li>Plano oficial do workshop</li>
            <li>Limite de uso adequado para rodar todos os comandos, agentes e skills sem travar</li>
            <li>Aguenta lançamento, múltiplos produtos em paralelo e geração de página pesada</li>
            <li>Evita o "uso esgotado" no meio de uma entrega</li>
          </ul>
        </div>
      </div>
      <p style="font-size:14px;color:var(--ink-3);margin-top:10px">Existe também o plano <b>Pro</b> por US$ 20/mês. Ele funciona, mas trava rápido quando você usa os agentes pesados do workshop (construtor de páginas, estrategista middle ticket, executor de plano de ação). Se vai levar o sistema a sério, já comece no Max.</p>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-download-simple"></i>Baixar o app desktop</h4>
      <ol>
        <li>Acesse <a href="https://claude.com/download" target="_blank">claude.com/download</a></li>
        <li>Escolha a versão certa para o seu sistema (<b>macOS</b> ou <b>Windows</b>)</li>
        <li>Clique em <b>Download</b> e espere o instalador baixar</li>
        <li>Abra o arquivo baixado e siga o instalador como em qualquer programa (no Mac, arraste o ícone para a pasta Applications; no Windows, clique em "Próximo" até terminar)</li>
        <li>Quando terminar, abra o <b>Claude</b> pelo menu iniciar (Windows) ou pelo Launchpad (Mac)</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-sign-in"></i>Entrar na sua conta</h4>
      <ol>
        <li>Na primeira abertura, o app mostra uma tela de boas-vindas</li>
        <li>Clique em <b>Entrar</b> e use a mesma conta Anthropic onde você assinou o Claude Max</li>
        <li>O app abre o navegador, você confirma o login e volta automaticamente</li>
        <li>Pronto. Você está dentro do Claude Code, com o chat principal já aberto</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-folder-open"></i>Abrir o projeto do workshop</h4>
      <ol>
        <li>Dentro do app, clique em <b>Open folder</b> (ou use o menu <b>File &gt; Open Folder</b>)</li>
        <li>Navegue até a pasta <span class="inline">workshop_inteligente</span> que você baixou</li>
        <li>Selecione a pasta e confirme</li>
        <li>O Claude Code carrega todos os comandos, skills e agentes do workshop. Agora é só digitar <span class="inline">/</span> no chat para ver a lista de comandos</li>
      </ol>
    </div>
    <div class="callout">
      <i class="ph ph-lightbulb-filament"></i>
      <div><b>Atalho.</b> Uma vez aberta a pasta, o app lembra dela. Das próximas vezes, basta abrir o Claude Code que ele reabre o último projeto sozinho.</div>
    </div>
  </div>

  <div class="tool" id="node">
    <div class="tool-head">
      <div class="tool-icon green">N</div>
      <div class="tool-title">
        <h3>Node.js</h3>
        <div class="sub">Ambiente técnico que permite rodar scripts de vídeo, automações e algumas integrações do workshop. O Claude Code desktop já vem com tudo que precisa, mas o Node libera funcionalidades extras como geração de vídeo com Remotion.</div>
      </div>
      <label class="checkbox-big" data-item="node"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-freemium">Recomendada</span></div></div>
      <div class="meta"><div class="meta-label">Custo</div><div class="meta-value ok">Gratuito</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">/video-remotion, scripts avançados</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-download-simple"></i>Passo a passo</h4>
      <ol>
        <li>Acesse <a href="https://nodejs.org" target="_blank">nodejs.org</a></li>
        <li>Baixe a versão <b>LTS</b> (a que aparece à esquerda, marcada como recomendada)</li>
        <li>Instale clicando em "Próximo" em todas as telas, sem mudar nada</li>
        <li>Pronto. O Claude Code já reconhece o Node automaticamente quando ele existe no sistema</li>
      </ol>
    </div>
    <div class="callout">
      <i class="ph ph-info"></i>
      <div><b>Pode pular por enquanto.</b> Se você não vai rodar geração de vídeo ainda, pode deixar o Node para depois. O resto do workshop funciona sem ele.</div>
    </div>
  </div>
</section>

<section id="paginas">
  <div class="section-head">
    <div class="section-num">2</div>
    <div>
      <h2>Páginas e Publicação</h2>
      <p>Ferramentas que transformam o HTML gerado pelo workshop em página no ar.</p>
    </div>
  </div>

  <div class="tool" id="vercel">
    <div class="tool-head">
      <div class="tool-icon slate">V</div>
      <div class="tool-title">
        <h3>Vercel</h3>
        <div class="sub">Publica as páginas HTML do workshop (vendas, captura, obrigado) na internet com URL própria em segundos.</div>
      </div>
      <label class="checkbox-big" data-item="vercel"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-freemium">Recomendada</span></div></div>
      <div class="meta"><div class="meta-label">Plano</div><div class="meta-value ok">Gratuito resolve</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">/pagina-vercel, /copy-pagina</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-plus"></i>Criar conta</h4>
      <ol>
        <li>Acesse <a href="https://vercel.com" target="_blank">vercel.com</a></li>
        <li>Clique em <b>Sign Up</b></li>
        <li>Escolha <b>Continue with GitHub</b>, <b>GitLab</b> ou email. Se não tiver GitHub, use o email mesmo</li>
        <li>Confirme o cadastro</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-credit-card"></i>Qual plano assinar</h4>
      <div class="plans">
        <div class="plan plan-free" style="grid-column:1/-1">
          <div class="plan-head"><div class="plan-name">Hobby (plano indicado)</div><div class="plan-price">R$ 0</div></div>
          <ul>
            <li>100 GB de banda por mês, mais que suficiente para qualquer página do workshop</li>
            <li>Páginas e projetos ilimitados</li>
            <li>Domínio <span class="inline">.vercel.app</span> grátis com HTTPS já configurado</li>
            <li>Deploy ilimitado</li>
            <li><b>Resolve sozinho para tudo que o aluno vai fazer.</b> Não precisa de plano pago</li>
          </ul>
        </div>
      </div>
      <p style="font-size:14px;color:var(--ink-3);margin-top:10px">Existem planos pagos (Pro, Enterprise), mas nenhum cenário do workshop exige. Se um dia sua página bater 100 GB de tráfego por mês, aí você pensa em migrar. Até lá, fica no gratuito.</p>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-plug"></i>Como conectar no Claude (forma recomendada)</h4>
      <p style="font-size:15px;color:var(--ink-2)">Em vez de mexer com token no arquivo .env, use o conector nativo do Claude:</p>
      <ol>
        <li>Dentro do Claude Code, digite:</li>
      </ol>
      <code class="code">/mcp</code>
      <ol start="2">
        <li>Escolha <b>Vercel</b> na lista</li>
        <li>O navegador abre pedindo autorização. Entre com sua conta Vercel e aceite</li>
        <li>Pronto. O Claude agora publica suas páginas direto, sem você precisar rodar nada no terminal</li>
      </ol>
      <p style="font-size:14px;color:var(--ink-3)">Detalhes do conector estão no bloco <b>Conector do Vercel no Claude</b>, na seção seguinte.</p>
    </div>
    <div class="callout">
      <i class="ph ph-lightbulb-filament"></i>
      <div><b>Alternativa via token.</b> Se preferir o fluxo antigo (comando <span class="inline">/pagina-vercel</span> lendo a variável <span class="inline">VERCEL_TOKEN</span> do .env), pegue o token em <b>Account Settings &gt; Tokens &gt; Create Token</b> no site do Vercel. Mas a forma recomendada hoje é o conector.</div>
    </div>
  </div>

  <div class="tool" id="lovable">
    <div class="tool-head">
      <div class="tool-icon pink">L</div>
      <div class="tool-title">
        <h3>Lovable.dev</h3>
        <div class="sub">Cria páginas interativas como quiz e aplicativos a partir de descrição em português. Usada nos fluxos de produto de entrada (low ticket).</div>
      </div>
      <label class="checkbox-big" data-item="lovable"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-freemium">Recomendada</span></div></div>
      <div class="meta"><div class="meta-label">Plano</div><div class="meta-value warn">Gratuito limitado</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">/lt-quiz, /app-saas, /pagina-lovable</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-plus"></i>Criar conta</h4>
      <ol>
        <li>Acesse <a href="https://lovable.dev" target="_blank">lovable.dev</a></li>
        <li>Clique em <b>Sign up</b> no canto superior direito</li>
        <li>Faça login com Google ou email</li>
        <li>Confirme o cadastro</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-credit-card"></i>Qual plano assinar</h4>
      <div class="plans">
        <div class="plan plan-free">
          <div class="plan-head"><div class="plan-name">Free</div><div class="plan-price">R$ 0</div></div>
          <ul>
            <li>5 mensagens por dia</li>
            <li>Serve só para testar rapidinho</li>
            <li>Não aguenta criar um quiz ou app inteiro</li>
          </ul>
        </div>
        <div class="plan plan-paid">
          <div class="plan-head"><div class="plan-name">Starter (recomendado)</div><div class="plan-price">US$ 5/mês</div></div>
          <ul>
            <li>Plano indicado para o workshop</li>
            <li>Créditos mensais suficientes para criar seu primeiro quiz ou SaaS</li>
            <li>Remove o limite diário apertado do Free</li>
            <li>Melhor custo-benefício para quem está começando o funil low ticket</li>
          </ul>
        </div>
      </div>
      <p style="font-size:14px;color:var(--ink-3);margin-top:10px">Existem planos maiores (Launch, Scale) para quem cria vários apps em paralelo. O Starter de US$ 5 resolve para o fluxo padrão do workshop.</p>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-rocket-launch"></i>Como usar no workshop</h4>
      <ol>
        <li>Rode <span class="inline">/lt-quiz</span> ou <span class="inline">/app-saas</span> no Claude Code</li>
        <li>O workshop gera um prompt técnico pronto para o Lovable</li>
        <li>Você cola esse prompt no Lovable, clica em <b>New Project</b> e gera</li>
        <li>Publica com um clique no botão <b>Publish</b> do Lovable</li>
        <li>Conecta a URL gerada ao resto do seu funil</li>
      </ol>
    </div>
  </div>
</section>

<section id="conectores">
  <div class="section-head">
    <div class="section-num">3</div>
    <div>
      <h2>Conectores do Claude</h2>
      <p>Integrações oficiais que dão mais poder para o Claude Code. Ele passa a ler páginas no seu navegador e publicar no Vercel direto, sem você sair do chat.</p>
    </div>
  </div>
  <div class="callout">
    <i class="ph ph-share-network"></i>
    <div><b>O que é um conector.</b> É uma ponte que liga o Claude a outra ferramenta. Depois de conectar, você pode pedir "Claude, abre essa página e me diz o que achou" ou "publica essa pasta no Vercel" e ele faz sozinho.</div>
  </div>

  <div class="tool" id="claude-chrome">
    <div class="tool-head">
      <div class="tool-icon red">C</div>
      <div class="tool-title">
        <h3>Claude in Chrome (MCP)</h3>
        <div class="sub">Extensão oficial da Anthropic para o Chrome. Permite que o Claude Code leia o conteúdo de páginas abertas no seu navegador, tire screenshots, clique em botões e navegue. Essencial para análise de concorrentes, feedback de páginas ao vivo e teste de funis.</div>
      </div>
      <label class="checkbox-big" data-item="claude-chrome"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-freemium">Altamente recomendada</span></div></div>
      <div class="meta"><div class="meta-label">Custo</div><div class="meta-value ok">Gratuito</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">Análise de link, feedback de página, pesquisa</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-download-simple"></i>Instalar a extensão</h4>
      <ol>
        <li>Abra o Google Chrome (se não tem, baixe em <a href="https://google.com/chrome" target="_blank">google.com/chrome</a>)</li>
        <li>Acesse a Chrome Web Store e busque por <b>Claude for Chrome</b> (ou use o link oficial da Anthropic em <a href="https://claude.ai/chrome" target="_blank">claude.ai/chrome</a>)</li>
        <li>Clique em <b>Adicionar ao Chrome</b> e confirme</li>
        <li>Vai aparecer um ícone do Claude na barra de extensões do Chrome</li>
        <li>Clique no ícone e faça login com a mesma conta Anthropic que você usa no Claude Code</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-plug"></i>Conectar ao Claude Code</h4>
      <ol>
        <li>Dentro do Claude Code (app desktop), digite:</li>
      </ol>
      <code class="code">/mcp</code>
      <ol start="2">
        <li>Você vai ver a lista de conectores disponíveis</li>
        <li>Procure por <b>Claude in Chrome</b> e ative</li>
        <li>Autorize a conexão no navegador quando ele abrir</li>
        <li>Pronto. Agora o Claude enxerga o que está na aba ativa do seu Chrome</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-play-circle"></i>Como usar no dia a dia</h4>
      <ul>
        <li><b>Análise de concorrente.</b> Abra a página do concorrente no Chrome, depois peça no Claude: "lê essa página aberta no meu Chrome e me diz qual é a oferta"</li>
        <li><b>Feedback ao vivo.</b> Depois de publicar sua página no Vercel, abra no Chrome e peça "lê essa página aberta e roda /feedback-pagina"</li>
        <li><b>Pesquisa de mercado.</b> Abra Instagram, YouTube ou Google com uma busca, peça o resumo dos resultados</li>
      </ul>
    </div>
    <div class="callout warn">
      <i class="ph ph-shield-check"></i>
      <div><b>Privacidade.</b> A extensão só lê a aba que você mandar. Nada sai automático. Mesmo assim, não use em páginas com dados sensíveis (banco, saúde, senha).</div>
    </div>
  </div>

  <div class="tool" id="vercel-connector">
    <div class="tool-head">
      <div class="tool-icon slate">V</div>
      <div class="tool-title">
        <h3>Conector do Vercel no Claude</h3>
        <div class="sub">Liga sua conta Vercel ao Claude via conectores nativos. Depois de ativo, você pede para o Claude publicar uma página e ele faz o deploy direto, sem você precisar copiar token para o arquivo .env.</div>
      </div>
      <label class="checkbox-big" data-item="vercel-connector"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-freemium">Recomendada</span></div></div>
      <div class="meta"><div class="meta-label">Custo</div><div class="meta-value ok">Gratuito</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">Publicação de páginas</div></div>
    </div>
    <div class="callout">
      <i class="ph ph-info"></i>
      <div><b>Pré-requisito.</b> Antes de ativar o conector, crie a conta Vercel (plano gratuito). Veja o bloco do Vercel logo acima.</div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-power"></i>Ativar o conector no Claude Code</h4>
      <ol>
        <li>Dentro do Claude Code, digite:</li>
      </ol>
      <code class="code">/mcp</code>
      <ol start="2">
        <li>Na lista que aparece, escolha <b>Vercel</b></li>
        <li>O navegador vai abrir pedindo autorização. Entre com sua conta Vercel e aceite as permissões</li>
        <li>Volte para o Claude Code. O conector já está ativo</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-cloud-arrow-up"></i>Como usar</h4>
      <p style="font-size:15px;color:var(--ink-2)">Depois de gerar uma página pelo workshop, basta pedir:</p>
      <code class="code">publica a pasta entregas/paginas/ no Vercel</code>
      <p style="font-size:14px;color:var(--ink-3)">O Claude cria o projeto, faz o deploy e devolve a URL pública. Sem terminal, sem token no .env, sem configuração extra.</p>
    </div>
    <div class="callout ok">
      <i class="ph ph-check-circle"></i>
      <div><b>Alternativa ao .env.</b> Se usar o conector, você não precisa da variável <span class="inline">VERCEL_TOKEN</span> no arquivo .env. O conector cuida da autenticação sozinho.</div>
    </div>
  </div>
</section>

<section id="imagem">
  <div class="section-head">
    <div class="section-num">4</div>
    <div>
      <h2>Imagem e Vídeo</h2>
      <p>Cinco ferramentas para gerar criativos, avatares e materiais visuais.</p>
    </div>
  </div>

  <div class="tool" id="heygen">
    <div class="tool-head">
      <div class="tool-icon slate">H</div>
      <div class="tool-title">
        <h3>HeyGen</h3>
        <div class="sub">Cria vídeos com avatares IA a partir de roteiro de texto. Você cola o script, escolhe o avatar e a voz, o vídeo sai pronto.</div>
      </div>
      <label class="checkbox-big" data-item="heygen"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-optional">Opcional</span></div></div>
      <div class="meta"><div class="meta-label">Plano</div><div class="meta-value warn">Gratuito com marca d'água</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">/video-heygen</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-plus"></i>Criar conta</h4>
      <ol>
        <li>Acesse <a href="https://app.heygen.com" target="_blank">app.heygen.com</a></li>
        <li>Clique em <b>Get Started Free</b></li>
        <li>Cadastre com email ou Google</li>
        <li>Confirme o email e faça login</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-credit-card"></i>Qual plano assinar</h4>
      <div class="plans">
        <div class="plan plan-free">
          <div class="plan-head"><div class="plan-name">Free</div><div class="plan-price">R$ 0</div></div>
          <ul>
            <li>3 vídeos de até 3 minutos por mês</li>
            <li>Marca d'água do HeyGen no canto</li>
            <li>Avatares públicos apenas</li>
            <li>Serve para testar</li>
          </ul>
        </div>
        <div class="plan plan-paid">
          <div class="plan-head"><div class="plan-name">Creator</div><div class="plan-price">US$ 29/mês</div></div>
          <ul>
            <li>Sem marca d'água</li>
            <li>15 minutos de vídeo por mês</li>
            <li>Libera criar avatar com seu rosto</li>
            <li>Mínimo recomendado para vender</li>
          </ul>
        </div>
      </div>
      <p style="font-size:14px;color:var(--ink-3);margin-top:10px">Para uso intenso (VSL, lançamento), o plano <b>Business</b> a partir de US$ 89/mês libera clonagem de voz e mais minutos. Comece no Creator.</p>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-key"></i>Pegar a chave de API (para automatizar pelo Claude Code)</h4>
      <ol>
        <li>Logado, clique no avatar do canto superior direito</li>
        <li>Vá em <b>Settings</b> (ou Configurações)</li>
        <li>Clique em <b>API</b> no menu lateral</li>
        <li>Clique em <b>Generate API Key</b>. Dê um nome qualquer</li>
        <li>Copie a chave que aparece</li>
        <li>Abra o <span class="inline">.env</span> na raiz do workshop e adicione:</li>
      </ol>
      <code class="code">HEYGEN_API_KEY=cole_sua_chave_aqui</code>
      <p style="font-size:14px;color:var(--ink-3)">Ou rode o comando <span class="inline">/configurar-heygen</span> dentro do Claude Code, ele faz esse processo guiado.</p>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-circle"></i>Criar seu avatar</h4>
      <ol>
        <li>Dentro do HeyGen, vá em <b>Avatars</b></li>
        <li>Clique em <b>Create Avatar</b></li>
        <li>Escolha <b>Instant Avatar</b> (para clonar a partir de vídeo de 2 minutos) ou <b>Photo Avatar</b> (a partir de foto)</li>
        <li>Siga as instruções de gravação</li>
        <li>Aguarde o processamento (pode levar de 10 minutos a algumas horas)</li>
      </ol>
    </div>
  </div>

  <div class="tool" id="freepik">
    <div class="tool-head">
      <div class="tool-icon blue">F</div>
      <div class="tool-title">
        <h3>Freepik (Magnific)</h3>
        <div class="sub">Banco de imagens, vetores e, principalmente, o Pikaso: gerador de imagem e vídeo com IA integrado. Usado para criar criativos de anúncio.</div>
      </div>
      <label class="checkbox-big" data-item="freepik"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-optional">Opcional</span></div></div>
      <div class="meta"><div class="meta-label">Plano</div><div class="meta-value warn">Gratuito limitado</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">/criativo-estatico</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-plus"></i>Criar conta</h4>
      <ol>
        <li>Acesse <a href="https://freepik.com" target="_blank">freepik.com</a></li>
        <li>Clique em <b>Sign up</b> no canto superior direito</li>
        <li>Cadastre com Google ou email</li>
        <li>Confirme o email</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-credit-card"></i>Qual plano assinar</h4>
      <div class="plans">
        <div class="plan plan-free">
          <div class="plan-head"><div class="plan-name">Free</div><div class="plan-price">R$ 0</div></div>
          <ul>
            <li>Limite diário baixo de downloads</li>
            <li>Créditos mínimos no Pikaso</li>
            <li>Com marca d'água em alguns formatos</li>
          </ul>
        </div>
        <div class="plan plan-paid">
          <div class="plan-head"><div class="plan-name">Premium</div><div class="plan-price">R$ 42/mês</div></div>
          <ul>
            <li>Downloads ilimitados</li>
            <li>Sem marca d'água</li>
            <li>Pikaso liberado com créditos generosos</li>
            <li>Recomendado para quem gera anúncios</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-key"></i>Pegar a chave de API</h4>
      <ol>
        <li>Logado, acesse <a href="https://www.freepik.com/api" target="_blank">freepik.com/api</a></li>
        <li>Clique em <b>Manage API Keys</b></li>
        <li>Gere uma nova chave</li>
        <li>Copie e adicione no arquivo <span class="inline">.env</span>:</li>
      </ol>
      <code class="code">FREEPIK_API_KEY=cole_sua_chave_aqui</code>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-sparkle"></i>Usar o Pikaso</h4>
      <ol>
        <li>No menu do Freepik (Magnific), vá em <b>AI Tools</b> e escolha <b>Pikaso</b></li>
        <li>Cole o prompt gerado pelo comando <span class="inline">/criativo-estatico</span> do workshop</li>
        <li>Escolha o formato (quadrado, vertical, horizontal)</li>
        <li>Gere e baixe a imagem</li>
      </ol>
    </div>
  </div>

  <div class="tool" id="openrouter">
    <div class="tool-head">
      <div class="tool-icon indigo">O</div>
      <div class="tool-title">
        <h3>OpenRouter</h3>
        <div class="sub">Acesso unificado a dezenas de modelos de IA para gerar imagens (Flux, DALL-E, Stable Diffusion) pelo mesmo token. Usado nos comandos de criativo.</div>
      </div>
      <label class="checkbox-big" data-item="openrouter"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-optional">Opcional</span></div></div>
      <div class="meta"><div class="meta-label">Plano</div><div class="meta-value warn">Pay-as-you-go</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">/criativo-estatico, assets de landing</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-plus"></i>Criar conta</h4>
      <ol>
        <li>Acesse <a href="https://openrouter.ai" target="_blank">openrouter.ai</a></li>
        <li>Clique em <b>Sign in</b> no canto superior direito</li>
        <li>Entre com Google, GitHub ou email</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-credit-card"></i>Como funciona o pagamento</h4>
      <p style="font-size:15px;color:var(--ink-2)">OpenRouter não tem mensalidade. Você adiciona crédito uma vez e vai gastando conforme gera imagem. Cada imagem custa centavos.</p>
      <ol>
        <li>No painel, clique em <b>Credits</b></li>
        <li>Adicione o valor que quiser (a partir de US$ 5)</li>
        <li>O crédito não vence</li>
      </ol>
      <p style="font-size:14px;color:var(--ink-3);margin-top:10px"><b>Custo médio por imagem:</b> Flux Schnell ~US$ 0.003, Flux Pro ~US$ 0.05, DALL-E 3 ~US$ 0.04. Com US$ 10 você gera centenas de criativos.</p>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-key"></i>Pegar a chave de API</h4>
      <ol>
        <li>No painel, clique em <b>Keys</b> no menu lateral</li>
        <li>Clique em <b>Create Key</b>, dê um nome</li>
        <li>Copie a chave (começa com <span class="inline">sk-or-</span>)</li>
        <li>No arquivo <span class="inline">.env</span> do workshop:</li>
      </ol>
      <code class="code">OPENROUTER_API_KEY=cole_sua_chave_aqui<br>OPENROUTER_IMAGE_MODEL=black-forest-labs/flux-1.1-pro</code>
      <p style="font-size:14px;color:var(--ink-3)">A segunda linha é opcional e define o modelo padrão. Se não colocar, o workshop escolhe.</p>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-brain"></i>Qual modelo escolher</h4>
      <ul>
        <li><b>Flux Schnell.</b> Testes rápidos e variações, custo muito baixo</li>
        <li><b>Flux 1.1 Pro.</b> Padrão recomendado para anúncio final</li>
        <li><b>DALL-E 3.</b> Quando precisa de texto legível na imagem</li>
        <li><b>Stable Diffusion 3.5.</b> Fotos realistas de pessoas</li>
      </ul>
    </div>
  </div>

  <div class="tool" id="whisk">
    <div class="tool-head">
      <div class="tool-icon teal">W</div>
      <div class="tool-title">
        <h3>Google Labs Whisk</h3>
        <div class="sub">Ferramenta do Google para gerar imagens combinando referências de estilo, cena e personagem. Usada para criar briefings visuais ricos.</div>
      </div>
      <label class="checkbox-big" data-item="whisk"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-optional">Opcional</span></div></div>
      <div class="meta"><div class="meta-label">Custo</div><div class="meta-value ok">Gratuito</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">/avat-whisk</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-plus"></i>Criar conta e acessar</h4>
      <ol>
        <li>Acesse <a href="https://labs.google/fx/tools/whisk" target="_blank">labs.google/fx/tools/whisk</a></li>
        <li>Faça login com sua conta Google</li>
        <li>Aceite os termos do Google Labs</li>
        <li>Pronto. Sem cadastro extra</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-info"></i>Disponibilidade</h4>
      <p style="font-size:15px;color:var(--ink-2)">O Whisk funciona no Brasil via acesso direto. Se não abrir, tente usar VPN para Estados Unidos.</p>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-rocket-launch"></i>Como usar no workshop</h4>
      <ol>
        <li>Rode <span class="inline">/avat-whisk</span> no Claude Code</li>
        <li>O workshop gera um briefing visual estruturado (Subject, Scene, Style)</li>
        <li>Cole cada bloco nos campos correspondentes do Whisk</li>
        <li>Gere as imagens e baixe</li>
      </ol>
    </div>
  </div>

  <div class="tool" id="canva">
    <div class="tool-head">
      <div class="tool-icon slate">C</div>
      <div class="tool-title">
        <h3>Canva</h3>
        <div class="sub">Editor visual para criar capas, carrosséis, posts e materiais gráficos. Integrado com a skill de design do workshop.</div>
      </div>
      <label class="checkbox-big" data-item="canva"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-optional">Opcional</span></div></div>
      <div class="meta"><div class="meta-label">Plano</div><div class="meta-value ok">Gratuito resolve</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">canvas-design, conteúdo social</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-plus"></i>Criar conta</h4>
      <ol>
        <li>Acesse <a href="https://canva.com" target="_blank">canva.com</a></li>
        <li>Clique em <b>Inscrever-se</b></li>
        <li>Use Google, Facebook ou email</li>
        <li>Confirme o email</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-credit-card"></i>Qual plano assinar</h4>
      <div class="plans">
        <div class="plan plan-free">
          <div class="plan-head"><div class="plan-name">Gratuito</div><div class="plan-price">R$ 0</div></div>
          <ul>
            <li>Milhares de templates</li>
            <li>5 GB de armazenamento</li>
            <li>Resolve para conteúdo orgânico</li>
          </ul>
        </div>
        <div class="plan plan-paid">
          <div class="plan-head"><div class="plan-name">Pro</div><div class="plan-price">R$ 34/mês</div></div>
          <ul>
            <li>Remove fundo de imagem com um clique</li>
            <li>Redimensiona projeto automaticamente</li>
            <li>Kit da marca (fontes e cores salvas)</li>
            <li>Útil para quem produz bastante</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-rocket-launch"></i>Como usar no workshop</h4>
      <ol>
        <li>Rode a skill <span class="inline">canvas-design</span> no Claude Code</li>
        <li>O workshop gera um briefing de design (textos, cores, layout)</li>
        <li>Abra o Canva, escolha o template correspondente</li>
        <li>Cole os textos e ajuste conforme o briefing</li>
      </ol>
    </div>
  </div>
</section>

<section id="automacoes">
  <div class="section-head">
    <div class="section-num">5</div>
    <div>
      <h2>Automações</h2>
      <p>Integrações que rodam tarefas no piloto automático.</p>
    </div>
  </div>

  <div class="tool" id="apify">
    <div class="tool-head">
      <div class="tool-icon yellow">A</div>
      <div class="tool-title">
        <h3>Apify</h3>
        <div class="sub">Coleta dados públicos do Instagram (seguidores, posts, engajamento) para alimentar o dashboard de métricas do workshop.</div>
      </div>
      <label class="checkbox-big" data-item="apify"><input type="checkbox"><span class="check-box"></span>Feito</label>
    </div>
    <div class="tool-meta">
      <div class="meta"><div class="meta-label">Status</div><div class="meta-value"><span class="tag tag-optional">Opcional</span></div></div>
      <div class="meta"><div class="meta-label">Plano</div><div class="meta-value warn">Créditos mensais</div></div>
      <div class="meta"><div class="meta-label">Usada por</div><div class="meta-value">/instagram-dashboard, /dados-instagram</div></div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-user-plus"></i>Criar conta</h4>
      <ol>
        <li>Acesse <a href="https://apify.com" target="_blank">apify.com</a></li>
        <li>Clique em <b>Sign up for free</b></li>
        <li>Cadastre com Google, GitHub ou email</li>
        <li>Confirme o email</li>
      </ol>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-credit-card"></i>Qual plano assinar</h4>
      <div class="plans">
        <div class="plan plan-free">
          <div class="plan-head"><div class="plan-name">Free</div><div class="plan-price">R$ 0</div></div>
          <ul>
            <li>US$ 5 de créditos por mês (renova)</li>
            <li>Dá para monitorar 1 perfil diariamente</li>
            <li>Suficiente para começar</li>
          </ul>
        </div>
        <div class="plan plan-paid">
          <div class="plan-head"><div class="plan-name">Starter</div><div class="plan-price">US$ 49/mês</div></div>
          <ul>
            <li>US$ 49 em créditos</li>
            <li>Monitorar vários perfis</li>
            <li>Só se precisar de volume</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-key"></i>Pegar a chave de API</h4>
      <ol>
        <li>Logado no Apify, clique no avatar e vá em <b>Settings</b></li>
        <li>Clique em <b>Integrations</b> no menu lateral</li>
        <li>Copie o <b>Personal API Token</b></li>
        <li>No <span class="inline">.env</span> do workshop, adicione:</li>
      </ol>
      <code class="code">APIFY_API_TOKEN=cole_seu_token_aqui</code>
      <p style="font-size:14px;color:var(--ink-3)">O comando <span class="inline">/configurar-apify</span> dentro do Claude Code faz esse processo guiado e já testa a conexão.</p>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-clock"></i>Agendamento automático</h4>
      <p style="font-size:15px;color:var(--ink-2)">O workshop configura o dashboard para rodar todo dia às 8h via Task Scheduler do Windows. Você acorda com as métricas atualizadas sem fazer nada.</p>
    </div>
  </div>
</section>

<section id="env">
  <div class="section-head">
    <div class="section-num">.env</div>
    <div>
      <h2>Referência do arquivo .env</h2>
      <p>Todas as chaves que você vai colar no arquivo <span class="inline">.env</span> na raiz do projeto.</p>
    </div>
  </div>
  <div class="callout warn">
      <i class="ph ph-lock-simple"></i>
      <div><b>Cuidado com suas chaves.</b> O arquivo <span class="inline">.env</span> é ignorado pelo Git automaticamente. Nunca poste essas chaves em grupo, print, post ou vídeo. Tratando como senha de banco.</div>
  </div>
  <div class="tool">
    <table class="env-table">
      <thead>
        <tr><th>Ferramenta</th><th>Chave no .env</th><th>Obrigatória</th></tr>
      </thead>
      <tbody>
        <tr><td>Claude Code</td><td class="mono">ANTHROPIC_API_KEY</td><td>Login via <span class="inline">claude</span></td></tr>
        <tr><td>Vercel</td><td class="mono">VERCEL_TOKEN</td><td>Opcional (use o conector)</td></tr>
        <tr><td>Vercel</td><td class="mono">VERCEL_PROJECT_ID</td><td>Opcional (use o conector)</td></tr>
        <tr><td>HeyGen</td><td class="mono">HEYGEN_API_KEY</td><td>Para <span class="inline">/video-heygen</span></td></tr>
        <tr><td>Freepik (Magnific)</td><td class="mono">FREEPIK_API_KEY</td><td>Para <span class="inline">/criativo-estatico</span></td></tr>
        <tr><td>OpenRouter</td><td class="mono">OPENROUTER_API_KEY</td><td>Para criativos IA</td></tr>
        <tr><td>OpenRouter</td><td class="mono">OPENROUTER_IMAGE_MODEL</td><td>Opcional</td></tr>
        <tr><td>Apify</td><td class="mono">APIFY_API_TOKEN</td><td>Para <span class="inline">/instagram-dashboard</span></td></tr>
      </tbody>
    </table>
    <div class="callout ok">
      <i class="ph ph-link-simple"></i>
      <div><b>Vercel via conector dispensa o .env.</b> Se você ativou o conector do Vercel no Claude (veja a seção <b>Conectores do Claude</b>), pode ignorar as duas linhas do Vercel na tabela acima.</div>
    </div>
    <div class="tool-section">
      <h4><i class="ph ph-file-text"></i>Exemplo de .env completo</h4>
      <code class="code"><span class="c"># Vídeo com avatar</span><br>HEYGEN_API_KEY=sua_chave_heygen<br><br><span class="c"># Imagens para anúncio</span><br>FREEPIK_API_KEY=sua_chave_freepik<br>OPENROUTER_API_KEY=sk-or-sua_chave<br>OPENROUTER_IMAGE_MODEL=black-forest-labs/flux-1.1-pro<br><br><span class="c"># Dashboard Instagram</span><br>APIFY_API_TOKEN=seu_token_apify<br><br><span class="c"># Vercel (só se não usar o conector)</span><br><span class="c"># VERCEL_TOKEN=seu_token_vercel</span><br><span class="c"># VERCEL_PROJECT_ID=seu_project_id</span></code>
    </div>
  </div>
</section>

<section id="custo">
  <div class="section-head">
    <div class="section-num">$</div>
    <div>
      <h2>Quanto vai gastar por mês</h2>
      <p>Investimento básico para rodar a imersão do começo ao fim.</p>
    </div>
  </div>
  <div class="tool">
    <div class="tool-section">
      <h4><i class="ph ph-piggy-bank"></i>Investimento base para a imersão</h4>
      <ul>
        <li>Claude Max: R$ 550/mês (plano oficial do workshop, obrigatório)</li>
        <li>Lovable Starter: US$ 5/mês (cerca de R$ 28, obrigatório para rodar quiz e SaaS do funil low ticket)</li>
        <li>Node.js, Claude in Chrome, Conector Vercel, Vercel, Whisk, Canva: gratuito</li>
        <li>HeyGen, Freepik (Magnific), Apify: começam nos planos gratuitos</li>
        <li>OpenRouter (API): <b>variável</b>, pague conforme usa. US$ 10 de crédito costumam durar 2 a 3 meses para quem roda /dados-instagram, /criar-gpt e automações esporádicas</li>
        <li><b>Total fixo: cerca de R$ 578/mês + variável da API</b></li>
      </ul>
      <p style="font-size:14px;color:var(--ink-3);margin-top:10px">Os dois pagos fixos são Claude Max e Lovable Starter. O OpenRouter é crédito pré-pago que você só coloca quando for usar comandos que consomem API externa (geralmente centavos por chamada). Tudo o mais que a trilha lista tem plano gratuito suficiente para você rodar a imersão inteira e entregar seu primeiro funil.</p>
    </div>
  </div>
  <div class="callout ok">
    <i class="ph ph-list-checks"></i>
    <div><b>Regra simples.</b> Assine Claude Max e Lovable Starter, e deixe todas as outras ferramentas no gratuito. Quando uma ferramenta específica começar a te atrapalhar (marca d'água, limite de cota, etc.), aí sim você avalia upgrade só dela. Nada mais precisa ser pago antes.</div>
  </div>
</section>

<footer>
  <p>Trilha de Ferramentas. Mergulhando na IA</p>
  <p style="margin-top:8px">Seu progresso está salvo neste navegador. Para imprimir como PDF, tecle <span class="inline">Ctrl+P</span> (ou Cmd+P no Mac) e escolha "Salvar como PDF".</p>
</footer>

</main>
</div>

<script>
const items = ["claude","node","claude-chrome","vercel-connector","vercel","lovable","heygen","freepik","openrouter","whisk","canva","apify"];
const KEY = "trilha-ferramentas-v1";

function loadState(){
  try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
  catch(e){ return {}; }
}
function saveState(s){ localStorage.setItem(KEY, JSON.stringify(s)); }

function updateProgress(){
  const s = loadState();
  const done = items.filter(i => s[i]).length;
  const pct = Math.round((done/items.length)*100);
  document.getElementById("pct").textContent = pct + "%";
  document.getElementById("fill").style.width = pct + "%";
  document.getElementById("count").textContent = done + " de " + items.length + " ferramentas configuradas";
  document.querySelectorAll(".nav-item").forEach(n => {
    const t = n.dataset.target;
    if (s[t]) n.classList.add("done"); else n.classList.remove("done");
  });
}

function initCheckboxes(){
  const s = loadState();
  document.querySelectorAll(".checkbox-big").forEach(cb => {
    const item = cb.dataset.item;
    const input = cb.querySelector("input");
    if (s[item]){ cb.classList.add("checked"); input.checked = true; }
    cb.addEventListener("click", e => {
      e.preventDefault();
      const s2 = loadState();
      s2[item] = !s2[item];
      saveState(s2);
      cb.classList.toggle("checked", s2[item]);
      input.checked = s2[item];
      updateProgress();
    });
  });
}

function initNav(){
  document.querySelectorAll(".nav-item").forEach(n => {
    n.addEventListener("click", () => {
      const t = n.dataset.target;
      const el = document.getElementById(t);
      if (el){
        el.scrollIntoView({behavior:"smooth", block:"start"});
        document.querySelectorAll(".nav-item").forEach(x => x.classList.remove("active"));
        n.classList.add("active");
        if (window.innerWidth < 900) document.querySelector("aside").classList.remove("open");
      }
    });
  });
}

initCheckboxes();
initNav();
updateProgress();
</script>

</body>
</html>
```
