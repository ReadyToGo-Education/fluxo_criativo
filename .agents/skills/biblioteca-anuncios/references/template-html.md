# Template HTML (compartilhado)

> Estrutura do `criativos-escalados.html` gerado pelo `/biblioteca-anuncios`.
> Light theme, self-contained, Inter via Google Fonts, JS inline para filtro de mercado.

---

## Paleta obrigatória (light theme)

| Variável | Hex | Uso |
|---|---|---|
| `--bg` | `#ffffff` | Fundo principal |
| `--bg-soft` | `#f7f9fc` | Fundo de cards e seções secundárias |
| `--text` | `#1a2238` | Texto principal |
| `--text-soft` | `#5b6478` | Texto secundário, meta info |
| `--border` | `#e5eaf2` | Bordas suaves |
| `--accent` | `#2563eb` | Links, headers de seção, badges neutros |
| `--accent-soft` | `#dbeafe` | Fundo de blocos "Padrão Identificado" |
| `--hot` | `#dc2626` | 20+ anúncios escalados (cor do número grande) |
| `--warm` | `#ea580c` | 10-19 anúncios escalados |
| `--cool` | `#2563eb` | 5-9 anúncios escalados |
| `--base` | `#6b7280` | 3-4 anúncios escalados (mínimo da escala) |
| `--empty` | `#fef3c7` | Fundo do empty-state (concorrentes sem escala) |
| `--empty-border` | `#fbbf24` | Borda do empty-state |

---

## Tipografia

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-weight: 400;
  color: var(--text);
}
```

Pesos:
- 400 — texto corrido
- 500 — meta info, datas
- 600 — labels e nomes de seção
- 700 — H2, H3, números de escala
- 800 — H1, "X" da escala em destaque

---

## Estrutura HTML (11 blocos)

### 1. `<head>` + estilos

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Criativos Escalados. Inteligência de Tráfego</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    /* paleta CSS variables */
    /* reset + base + componentes */
  </style>
</head>
```

### 2. Header

```html
<header class="hero">
  <div class="eyebrow">Inteligência de Tráfego</div>
  <h1>Criativos Escalados na Biblioteca da Meta</h1>
  <p class="subtitle">Nicho: <strong>{nicho}</strong>. Concorrentes investigados: <strong>{N}</strong>.</p>
  <div class="chips">
    <span class="chip">Data: {data}</span>
    <span class="chip">Critério: <strong>≥3 ads por criativo</strong></span>
    <span class="chip">Mercados: {lista_mercados}</span>
    <span class="chip status-{status}">{status_legivel}</span>
  </div>
</header>
```

### 3. Stats em 4 cards

```html
<section class="stats">
  <div class="stat-card">
    <div class="stat-label">Concorrentes investigados</div>
    <div class="stat-value">{N_concorrentes}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Criativos escalados encontrados</div>
    <div class="stat-value">{N_criativos}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Maior escala individual</div>
    <div class="stat-value">{max_escala}</div>
    <div class="stat-meta">{nome_do_competidor}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Maior escala fora do BR</div>
    <div class="stat-value">{max_escala_internacional}</div>
    <div class="stat-meta">{nome} ({mercado})</div>
  </div>
</section>
```

### 4. Filtro de mercado

```html
<section class="filter">
  <button class="filter-btn active" data-filter="all">Todos</button>
  <button class="filter-btn" data-filter="br">🇧🇷 Brasil</button>
  <button class="filter-btn" data-filter="en">🇺🇸 English</button>
  <button class="filter-btn" data-filter="es">🌎 Español</button>
</section>
```

### 5. Nav sticky

```html
<nav class="sticky-nav">
  <a href="#nome-do-concorrente">{nome} <span class="count-badge">{N}</span></a>
  <a href="#resumo">Resumo Estratégico</a>
</nav>
```

### 6. Cards de concorrente

```html
<section class="competitor" id="erico-rocha" data-region="br">
  <header class="competitor-header">
    <h2>🇧🇷 Erico Rocha</h2>
    <div class="competitor-meta">
      Foco: <strong>Lançamento de cursos online</strong>
      <span class="badge">{N} criativos escalados</span>
    </div>
  </header>

  <div class="creatives">
    <!-- bloco 6.1: card de criativo individual -->
    <article class="creative-card scale-hot">
      <div class="scale-number">42</div>
      <div class="creative-body">
        <div class="creative-label">anúncios usam este criativo</div>
        <h3 class="creative-hook">{primeira_linha_da_copy_ou_hook}</h3>
        <p class="creative-desc">{descricao_curta_do_visual_ou_angulo}</p>
        <div class="creative-meta">
          <code class="library-id">Library ID: {id}</code>
          <a class="link-ad" href="{url_biblioteca}" target="_blank" rel="noopener">Ver anúncio</a>
        </div>
      </div>
    </article>

    <!-- bloco 6.2: Padrão identificado -->
    <div class="pattern-box">
      <h4>Padrão Identificado</h4>
      <p>{texto_descrevendo_o_que_o_concorrente_repete}</p>
    </div>
  </div>
</section>
```

Classes de escala no card (aplicar em `scale-{nivel}`):
- `scale-hot` para 20+ (cor `--hot`)
- `scale-warm` para 10-19 (cor `--warm`)
- `scale-cool` para 5-9 (cor `--cool`)
- `scale-base` para 3-4 (cor `--base`)

### 7. Empty state (concorrente sem escala)

```html
<section class="competitor" id="alex-vargas" data-region="br">
  <header class="competitor-header">
    <h2>🇧🇷 Alex Vargas</h2>
  </header>
  <div class="empty-state">
    <strong>Sem criativos escalados nesta janela.</strong>
    <p>Motivo identificado: alta rotação de criativos sem repetição vertical. Veicula 30+ anúncios diferentes, cada um aparece em 1 a 2 ads no máximo.</p>
  </div>
</section>
```

Variações de motivo:
- "Alta rotação de criativos sem repetição vertical"
- "Pivotou para fora do nicho ({novo_nicho})"
- "Volume de ads excedeu a extração automática. Cheque manualmente."
- "Sem anúncios ativos na Biblioteca neste mercado"

### 8. Resumo Estratégico em 3 colunas

```html
<section class="summary" id="resumo">
  <h2>Resumo Estratégico</h2>
  <div class="summary-grid">
    <div class="summary-col">
      <h3>Quem mais escala um único criativo</h3>
      <ul>
        <li><strong>{nome}</strong> ({mercado}): {N} ads com a mesma copy</li>
        <!-- top 3 -->
      </ul>
    </div>
    <div class="summary-col">
      <h3>Sem escala (alta rotação)</h3>
      <ul>
        <li><strong>{nome}</strong>: {motivo curto}</li>
      </ul>
    </div>
    <div class="summary-col">
      <h3>Fora do nicho atual (pivot)</h3>
      <ul>
        <li><strong>{nome}</strong>: pivotou para {novo_nicho}</li>
      </ul>
    </div>
  </div>
</section>
```

### 9. Padrão comum + Diferenças entre mercados

```html
<section class="patterns">
  <div class="pattern-block gradient-blue">
    <h3>Padrão comum entre os que escalam</h3>
    <ul>
      <li>{bullet 1}</li>
      <li>{bullet 2}</li>
      <li>{bullet 3}</li>
      <li>{bullet 4}</li>
      <li>{bullet 5}</li>
    </ul>
  </div>
  <div class="pattern-block gradient-orange">
    <h3>Diferenças entre mercados</h3>
    <ul>
      <li>BR vs US: {bullet}</li>
      <li>EN vs ES: {bullet}</li>
      <li>BR vs ES: {bullet}</li>
      <li>{outro}</li>
      <li>{outro}</li>
    </ul>
  </div>
</section>
```

### 10. Footer

```html
<footer>
  <p>Relatório gerado em {data}. Critério de escala: 3 ou mais anúncios usando o mesmo criativo.</p>
  <p>Fonte: Biblioteca de Anúncios da Meta. Janela: ads ativos no momento da extração.</p>
</footer>
```

### 11. Script de filtro de mercado

```html
<script>
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.querySelectorAll('.competitor').forEach(c => {
        if (filter === 'all' || c.dataset.region === filter) {
          c.style.display = 'block';
        } else {
          c.style.display = 'none';
        }
      });
    });
  });
</script>
```

---

## Regras de qualidade

- **Mobile responsive**. Breakpoints em 640px e 768px. Stats viram 2x2 no mobile, 4x1 no desktop.
- **Hover suave** em cards de criativo (transform translateY -2px + box-shadow).
- **Scroll suave** nos links da nav (CSS `scroll-behavior: smooth`).
- **Filtro com transição** (display none/block, sem animação extra para performance).
- **Links em `target="_blank"` com `rel="noopener"`** sempre.
- **Sem dependências além do Google Fonts.** Zero CDN de framework. Zero JS externo.
- **Tudo inline.** O HTML é único arquivo de 1 a 3 MB no máximo. Pode ser enviado por e-mail ou aberto offline (exceto pelas fontes do Google, que carregam online se houver conexão).
- **Caminho do arquivo**: `meus-produtos/{ativo}/entregas/biblioteca-anuncios/criativos-escalados-{data}.html`.

---

## Regras de copy do HTML

- **Português brasileiro** com acentuação correta nos textos em pt-BR.
- **Inglês** correto nos labels que descrevem mercado en.
- **Espanhol** correto nos labels que descrevem mercado es.
- **Sem travessão** em qualquer texto.
- **Sem ponto de exclamação.**
- **Datas no formato DD/MM/AAAA** nos textos em pt-BR. Formato MM/DD/YYYY se o relatório for em inglês (decidido pelo aluno).
