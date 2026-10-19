# Sub-skill utilitária. Export HTML de Análise

> **Caminho legado do dashboard.** Quem tem o conector MCP da Meta recebe o dashboard ao vivo do `/trafego-dashboard`. Esta sub-skill continua valendo para quem não usa o MCP (ver `.claude/skills/trafego-dashboard/references/legado-dashboard-estatico.md`) e para qualquer aluno, em qualquer modo, que peça para salvar uma análise como relatório (fotografia com gráficos).

Sub-skill compartilhada por TODOS os 10 outputs da `/trafego-analise`. Não tem opção própria no menu: é acionada ao final de um output, pelo caminho legado do `/trafego-dashboard` ou quando o aluno pede para salvar a análise.

**Propósito:** transformar o output narrado de uma análise em um HTML standalone usando o design system Fluxo Criativo, salvar no produto ativo e devolver o caminho absoluto pro aluno abrir no navegador.

---

## 0. CONTRATO DE EXPORT (regra dura: ler antes de gerar qualquer HTML)

> **Aprendido em produção (2026-05-29):** o Claude gerou dashboards "do zero", com tema próprio (roxo) e barras de CSS, **sem nenhum gráfico SVG** e **fora do design system**. Os recursos de gráfico (`trafego_chart_geom.py`, `serie_diaria_svg`) existiam e estavam íntegros, só não foram chamados. Este contrato existe para que isso **nunca mais** aconteça. Vale para TODOS os outputs e os dois modos (`MCP_CONECTOR` e `APP`).

**É PROIBIDO inventar um HTML novo.** O export SEMPRE parte do esqueleto da seção 3.1 + tokens da seção 3.2 (design system oficial). O design system tem **3 temas oficiais** (Escuro, Terra e Claro Neutro, seção 3.2.a); o aluno escolhe o tema, e o tema escolhido é aplicado copiando o bloco de tokens correspondente **sem alterar nenhum valor**. Nunca criar paleta própria fora dos 3 temas, nunca trocar `--accent` por outra cor, nunca substituir `.topbar`/`.snap-warn` por banner improvisado.

**É OBRIGATÓRIO renderizar os gráficos** que a sub-skill do output declara em "Gráficos obrigatórios". A geometria vem de:
- `serie_diaria_svg` e `health.dimensoes` → do `trafego_processar.py` (modo APP), **ou**
- **`trafego_chart_geom.py`** (receitas F a L): **roda em qualquer modo, não toca a API, não usa token.** No modo `MCP_CONECTOR`, onde os números foram processados à mão (sem os scripts de fetch), **é este helper que gera a geometria dos gráficos** a partir dos números já calculados. Passar o spec por arquivo: `{PY} .claude/skills/trafego-analise/scripts/trafego_chart_geom.py <tipo> < /tmp/spec.json` (`{PY}` = interpretador detectado na sessão, `python3` ou `py -3`).

**Checklist de conformidade: rodar ANTES de declarar o dashboard pronto.** Substituir `<ARQ>` pelo caminho do HTML recém-escrito:

```bash
echo -n "svg="      ; grep -c "<svg"        <ARQ>   # > 0 (gráficos presentes)
echo -n "chart-card="; grep -c "chart-card" <ARQ>   # > 0
echo -n "topbar="    ; grep -c 'class="topbar' <ARQ># = pelo menos 1 (design oficial)
echo -n "snap-warn=" ; grep -c "snap-warn"   <ARQ>  # = pelo menos 1
echo -n "tema="      ; grep -cE 'data-theme="(escuro|terra|claro)"' <ARQ> # = 1 (tema oficial declarado)
echo -n "bgok="      ; grep -cE -- "--bg:(#000|#D8DDC8|#f4f6f8)" <ARQ>   # = 1 (tokens de um tema oficial, não inventados)
```

**Regra de bloqueio:** se `svg=0`, ou `chart-card=0`, ou `topbar=0`, ou `tema=0`, ou `bgok=0`, o export está ERRADO, **não entregar.** Refazer a partir do esqueleto oficial + gráficos antes de mostrar ao aluno. Só anunciar "snapshot salvo" depois que o checklist passar.

> Exceção legítima de gráfico: se um gráfico específico depende de dado que a chamada não retornou (ex: breakdown vazio), **omitir só aquele gráfico** e seguir com os demais (nunca inventar número). Mas `svg=0` total nunca é aceitável quando a sub-skill declara gráficos obrigatórios.

---

## 1. Quando rodar

Esta sub-skill roda em três situações:

- **Caminho legado do dashboard:** o `/trafego-dashboard` encaminhou para cá (aluno sem o conector MCP ou sessão sem a ferramenta de artefato). O aluno já pediu o dashboard: não perguntar "quer salvar?" de novo, só resolver o tema (abaixo).
- **Pedido explícito do aluno** para salvar a análise como relatório (em qualquer modo): idem, só resolver o tema.
- **Oferta ao fim da análise**, quando fizer sentido oferecer a fotografia: usar as perguntas abaixo.

O tema depende de `EXPORT_TEMA` no `.env` (variável **não sensível**, pode ser lida e exibida normalmente; valores aceitos: `escuro`, `terra`, `claro`). Se o aluno já pediu o export e `EXPORT_TEMA` estiver vazio, perguntar só o tema (opções 1 a 3 do Caso 1).

**Caso 1: `EXPORT_TEMA` ausente ou vazio (primeira vez):**

```
Quer salvar essa análise como um dashboard HTML pra revisitar depois?

1. Sim, tema Escuro (fundo preto, números em destaque; bom pra telão)
2. Sim, tema Terra (claro terroso, com creme, terracota e verdes; bom pra leitura longa)
3. Sim, tema Claro Neutro (branco e azul; visual de relatório limpo)
4. Não, só o texto

Digite o número:

⚠️ Snapshot: o HTML gerado é uma "fotografia" dos dados deste momento.
   Métricas mudam, e este arquivo NÃO atualiza sozinho. Ele tem o timestamp
   no topo pra deixar claro quando foi gerado. Pra dado fresco, rode a
   análise de novo.
```

Se `1`/`2`/`3`: gravar `EXPORT_TEMA=escuro|terra|claro` no `.env` (criar a linha se não existir), confirmar em 1 linha ("Tema {nome} salvo como padrão dos seus dashboards. Pra trocar depois, é só pedir.") e rodar esta sub-skill com o tema escolhido. Se `4`/`n`/silêncio: encerrar normalmente.

**Caso 2: `EXPORT_TEMA` já configurado:**

```
Quer salvar essa análise como HTML no tema {Nome do tema}? (s/n)
(pra usar outro tema só desta vez: "sim, escuro" / "sim, terra" / "sim, claro")

⚠️ Snapshot: o HTML gerado é uma "fotografia" dos dados deste momento.
   Métricas mudam, e este arquivo NÃO atualiza sozinho.
```

Se `s`/`sim`: rodar esta sub-skill com o tema do `.env`. Se a resposta trouxer outro tema ("sim, terra"): usar o tema pedido **só nesta geração**, sem alterar o `.env`. Se o aluno pedir pra trocar o padrão ("troca meu tema pra claro"): regravar `EXPORT_TEMA` e confirmar. Se `n`/`não` ou silêncio: encerrar normalmente.

**Nunca rodar export sem confirmação explícita.** Aluno que só quer texto rápido não recebe arquivo.

---

## 2. Onde salvar

```
meus-produtos/{ativo}/trafego/analise/{slug-output}-{YYYY-MM-DD-HHMM}.html
```

**Componentes do nome:**
- `{ativo}`: lê de `meus-produtos/.ativo`. Se ausente, recusar e instruir `/produto-novo`.
- `{slug-output}`: nome curto do output. Tabela:

| Output | slug |
|---|---|
| [1] Diagnóstico Rápido | `diagnostico-rapido` |
| [2] Performance & Funil | `performance-funil` |
| [3] Criativos & Copy | `criativos-copy` |
| [4] Geo & Demografia | `geo-demografia` |
| [5] Timing & Sazonalidade | `timing-sazonalidade` |
| [6] Investigação Profunda | `investigacao-profunda` |
| [7] Lifecycle & Histórico | `lifecycle-historico` |
| [8] Problemas Ocultos | `problemas-ocultos` |
| [9] Orçamento & Projeção | `orcamento-projecao` |
| [10] Comparativo A x B | `comparativo-ab` |

- `{YYYY-MM-DD-HHMM}`: timestamp local do momento da geração. Ex: `2026-05-05-1432`.

Exemplos de caminho final:
- `meus-produtos/curso-tarot/trafego/analise/diagnostico-rapido-2026-05-05-1432.html`
- `meus-produtos/ingles-atletas/trafego/analise/lifecycle-historico-2026-05-04-0930.html`

Se a pasta `trafego/analise/` não existir, criar.

**Não sobrescrever.** Cada export gera arquivo novo com timestamp próprio. Histórico fica disponível pra comparação depois.

---

## 3. Estrutura do HTML standalone

O arquivo é **autossuficiente**: CSS embedado em `<style>`, fontes via Google Fonts, zero dependência externa além disso. Aluno abre direto no navegador, sem servidor.

### 3.1 Esqueleto

```html
<!doctype html>
<html lang="pt-BR" data-theme="{escuro|terra|claro}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>[{N}] {nome do output} · Tráfego Análise</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  {link-de-fontes-do-tema}
  <style>
    {bloco-de-tokens-do-tema-3.2.a}
    {css-de-componentes-3.2.b}
  </style>
</head>
<body>

  <!-- Topbar escura com info do snapshot -->
  <div class="topbar">
    <div>
      <div class="topbar-title">[{N}] {nome do output} · Tráfego Análise</div>
      <div class="topbar-meta">
        SNAPSHOT · {DD/MM/YYYY HH:MM} &nbsp;|&nbsp; {janela} &nbsp;|&nbsp; {act_id mascarado} ({nome da conta})
      </div>
    </div>
    <div class="topbar-right">{escopo, ex: CURSO X · 38 campanhas ativas}</div>
  </div>

  <!-- Banner de dado expira -->
  <div class="snap-warn">
    Fotografia dos dados em <strong>{DD/MM HH:MM}</strong>.
    Métricas mudam continuamente. Para dado atualizado, rode a análise novamente.
  </div>

  <div class="container">

    <!-- KPIs globais -->
    <div class="stats-grid">
      {kpis-globais}
    </div>

    <!-- Blocos do output (ver mapeamento na seção 4) -->
    {blocos-renderizados}

    <!-- Rodapé com handoffs -->
    <div class="page-foot">
      <div class="section-h">PRÓXIMOS PASSOS</div>
      <div class="terms">
        {handoffs-em-pills}
      </div>
    </div>

  </div>
</body>
</html>
```

### 3.2 Tokens do design system (embedar em todo arquivo)

O design system tem **3 temas oficiais**. O CSS de componentes (3.2.b) é o MESMO para os três: toda cor sai de variável, zero hexadecimal solto. O que muda entre temas é apenas o bloco de tokens (3.2.a). Montagem do `<style>`: **bloco do tema escolhido (3.2.a) + CSS de componentes (3.2.b)**. Proibido alterar valores de token, misturar temas ou criar variável nova fora das listadas.

#### 3.2.a Blocos de tema (copiar UM, conforme a escolha do aluno)

**TEMA ESCURO** (`data-theme="escuro"`): o visual clássico preto/azul, baseado no `dashboard-criativos.html`:

```css
:root {
  --bg:#000; --bg-alt:#000; --card:#111; --card-hover:#1a1a1a;
  --border:#1f1f1f; --border-light:#181818;
  --text:#ffffff; --text-mid:#ededea; --text-muted:#d1d5db;
  --accent:#3b82f6; --accent-deep:#1d3a6e; --on-accent:#fff;
  --green:#10b981; --yellow:#f59e0b; --red:#ef4444; --orange:#f97316;
  --accent-soft:#111d35; --accent-faint:#1a2234;
  --green-soft:#0d1f16; --yellow-soft:#1f1600; --red-soft:#1f0d0d;
  --green-deep:#0d3a2a; --red-deep:#3b1515;
  --tier-s-bg:#14532d; --tier-s-fg:#4ade80; --tier-a-bg:#1a3a5c; --tier-a-fg:#60a5fa;
  --tier-b-bg:#422006; --tier-b-fg:#fbbf24; --tier-c-bg:#3b1515; --tier-c-fg:#fca5a5;
  --tier-d-bg:#1f1f1f; --tier-d-fg:#d1d5db;
  --tag-video-bg:#1d3a6e; --tag-video-fg:#93c5fd; --tag-imagem-bg:#4a1942; --tag-imagem-fg:#f0abfc;
  --radius:12px; --shadow:0 1px 3px rgba(0,0,0,.4),0 1px 2px rgba(0,0,0,.3);
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI","Inter",sans-serif;
  --font-heading:var(--font);
  --font-mono:"JetBrains Mono","SF Mono","Fira Code",monospace;
}
html { color-scheme: dark; }
```

Fontes (tema Escuro e Claro Neutro):
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
```

**TEMA TERRA** (`data-theme="terra"`): claro terroso (creme, terracota e verdes), derivado do Design System Terra. Fundo sage vivo, cartão creme calmo, sombra âmbar, terracota como cor de ação:

```css
:root {
  --bg:#D8DDC8; --bg-alt:#FAF9F4; --card:#FAF9F4; --card-hover:#F5F4EF;
  --border:#DBC1B3; --border-light:#E9E8E3;
  --text:#1B1C19; --text-mid:#554338; --text-muted:#887366;
  --accent:#E26A2C; --accent-deep:#974800; --on-accent:#fff;
  --green:#496547; --yellow:#C9922E; --red:#BA1A1A; --orange:#974800;
  --accent-soft:#FFDBC7; --accent-faint:#F7E8DC;
  --green-soft:#C8E9C2; --yellow-soft:#F3E5BE; --red-soft:#FFDAD6;
  --green-deep:#2E4B2C; --red-deep:#93000A;
  --tier-s-bg:#C8E9C2; --tier-s-fg:#2E4B2C; --tier-a-bg:#B9ECEE; --tier-a-fg:#234B4D;
  --tier-b-bg:#F3E5BE; --tier-b-fg:#6B4E14; --tier-c-bg:#FFDAD6; --tier-c-fg:#93000A;
  --tier-d-bg:#E9E8E3; --tier-d-fg:#887366;
  --tag-video-bg:#B9ECEE; --tag-video-fg:#234B4D; --tag-imagem-bg:#E7D9E9; --tag-imagem-fg:#8A6A8F;
  --radius:20px; --shadow:0 4px 12px rgba(151,72,0,.08);
  --font:'Inter',system-ui,-apple-system,sans-serif;
  --font-heading:'Plus Jakarta Sans',var(--font);
  --font-mono:"JetBrains Mono","SF Mono","Fira Code",monospace;
}
html { color-scheme: light; }
```

Fontes (tema Terra):
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
```

**TEMA CLARO NEUTRO** (`data-theme="claro"`): branco e azul, visual de relatório limpo. Mesma cor de marca do tema Escuro (azul), fundo cinza-claro, cartões brancos:

```css
:root {
  --bg:#f4f6f8; --bg-alt:#ffffff; --card:#ffffff; --card-hover:#f8fafc;
  --border:#e2e8f0; --border-light:#eef2f6;
  --text:#0f172a; --text-mid:#334155; --text-muted:#64748b;
  --accent:#2563eb; --accent-deep:#1e40af; --on-accent:#fff;
  --green:#059669; --yellow:#d97706; --red:#dc2626; --orange:#ea580c;
  --accent-soft:#dbeafe; --accent-faint:#eff6ff;
  --green-soft:#d1fae5; --yellow-soft:#fef3c7; --red-soft:#fee2e2;
  --green-deep:#065f46; --red-deep:#991b1b;
  --tier-s-bg:#d1fae5; --tier-s-fg:#065f46; --tier-a-bg:#dbeafe; --tier-a-fg:#1e40af;
  --tier-b-bg:#fef3c7; --tier-b-fg:#92400e; --tier-c-bg:#fee2e2; --tier-c-fg:#991b1b;
  --tier-d-bg:#e2e8f0; --tier-d-fg:#64748b;
  --tag-video-bg:#dbeafe; --tag-video-fg:#1e40af; --tag-imagem-bg:#fae8ff; --tag-imagem-fg:#86198f;
  --radius:12px; --shadow:0 1px 3px rgba(15,23,42,.08),0 1px 2px rgba(15,23,42,.05);
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI","Inter",sans-serif;
  --font-heading:var(--font);
  --font-mono:"JetBrains Mono","SF Mono","Fira Code",monospace;
}
html { color-scheme: light; }
```

#### 3.2.b CSS de componentes (idêntico para os 3 temas: copiar inteiro após o bloco do tema)

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); background: var(--bg); color: var(--text); font-size: 14px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
.topbar-title, .section-title, .stat-card .value, .fi-value, .fmt-metric .mv, .df-name { font-family: var(--font-heading); letter-spacing: -.01em; }
::selection { background: var(--accent); color: var(--on-accent); }

/* Topbar */
.topbar { background: var(--bg-alt); border-bottom: 1px solid var(--border); padding: 16px 32px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.topbar-title { font-size: 1rem; font-weight: 700; color: var(--text); letter-spacing: -.3px; }
.topbar-meta { font-size: .78rem; color: var(--text-muted); font-family: var(--font-mono); margin-top: 2px; }
.topbar-right { font-size: .78rem; color: var(--text-muted); text-align: right; }

/* Banner snapshot */
.snap-warn { background: var(--accent-faint); border-left: 3px solid var(--accent); padding: 10px 32px; font-size: .78rem; color: var(--text-muted); font-family: var(--font-mono); }
.snap-warn strong { color: var(--text-mid); font-weight: 400; }

/* Container */
.container { max-width: 1280px; margin: 0 auto; padding: 28px 32px; }

/* Stats grid: KPIs globais */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(160px,1fr)); gap: 14px; margin-bottom: 32px; }
.stat-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; }
.stat-card .label { font-size: .72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: .5px; margin-bottom: 6px; font-family: var(--font-mono); }
.stat-card .value { font-size: 1.5rem; font-weight: 800; color: var(--text); line-height: 1; }
.stat-card .sub { font-size: .72rem; color: var(--text-muted); margin-top: 4px; }
.stat-card .value.green { color: var(--green); }
.stat-card .value.yellow { color: var(--yellow); }
.stat-card .value.red { color: var(--red); }

/* Sections */
.section { margin-bottom: 40px; }
.section-header { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 20px; }
.section-num { background: var(--accent); color: var(--on-accent); border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: .85rem; font-weight: 700; flex-shrink: 0; }
.section-title { font-size: 1.1rem; font-weight: 700; color: var(--text); }
.section-question { font-size: .85rem; color: var(--text-muted); margin-top: 2px; font-style: italic; }
.section-h { font-family: var(--font-mono); font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--text-muted); padding-bottom: 10px; margin: 32px 0 16px; border-bottom: 1px solid var(--border); }

/* Cards */
.card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; margin-bottom: 16px; }
.card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.card-grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; }
.card-label { font-size: .78rem; font-weight: 600; color: var(--text-muted); margin-bottom: 14px; text-transform: uppercase; letter-spacing: .4px; }

/* Comparativo de formato */
.fmt-compare { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.fmt-box { border: 1px solid var(--border); border-radius: 10px; padding: 16px; text-align: center; background: var(--bg); }
.fmt-tipo { font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .5px; color: var(--text-muted); margin-bottom: 12px; }
.fmt-metric { margin-bottom: 10px; }
.fmt-metric .ml { font-size: .72rem; color: var(--text-muted); }
.fmt-metric .mv { font-size: 1.25rem; font-weight: 800; color: var(--text); }

/* Funil de métricas */
.funnel-row { display: flex; gap: 10px; margin-bottom: 16px; }
.funnel-item { flex: 1; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 14px; text-align: center; }
.fi-label { font-size: .68rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: .5px; margin-bottom: 6px; font-family: var(--font-mono); }
.fi-value { font-size: 1.3rem; font-weight: 800; }
.fi-sub { font-size: .68rem; color: var(--text-muted); margin-top: 3px; }

/* Tabelas */
table { width: 100%; border-collapse: collapse; font-size: .85rem; }
thead tr { background: var(--bg); }
th { padding: 10px 12px; text-align: left; font-weight: 600; color: var(--text-muted); font-size: .72rem; text-transform: uppercase; letter-spacing: .4px; border-bottom: 1px solid var(--border); font-family: var(--font-mono); }
td { padding: 10px 12px; border-bottom: 1px solid var(--border-light); vertical-align: middle; color: var(--text-mid); }
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--card-hover); color: var(--text); }
.num { text-align: right; font-family: var(--font-mono); font-size: .82rem; font-variant-numeric: tabular-nums; }
.rank { color: var(--text-muted); font-weight: 700; font-size: .78rem; text-align: center; width: 36px; font-family: var(--font-mono); }
.ad-name { font-weight: 600; font-size: .82rem; max-width: 340px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: block; color: var(--text); }

/* Tier badges */
.tier-s { background: var(--tier-s-bg); color: var(--tier-s-fg); font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tier-a { background: var(--tier-a-bg); color: var(--tier-a-fg); font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tier-b { background: var(--tier-b-bg); color: var(--tier-b-fg); font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tier-c { background: var(--tier-c-bg); color: var(--tier-c-fg); font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tier-d { background: var(--tier-d-bg); color: var(--tier-d-fg); font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tag-video { background: var(--tag-video-bg); color: var(--tag-video-fg); font-size: .68rem; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
.tag-imagem { background: var(--tag-imagem-bg); color: var(--tag-imagem-fg); font-size: .68rem; font-weight: 600; padding: 2px 8px; border-radius: 999px; }

/* Diagnostic boxes */
.diag-box { border-left: 3px solid var(--accent); background: var(--accent-faint); border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 14px 0; font-size: .85rem; color: var(--text-mid); line-height: 1.65; }
.diag-box.green { background: var(--green-soft); border-color: var(--green); }
.diag-box.yellow { background: var(--yellow-soft); border-color: var(--yellow); }
.diag-box.red { background: var(--red-soft); border-color: var(--red); }
.diag-box::before { content: "NO VTSD · "; font-family: var(--font-mono); font-size: .68rem; color: var(--accent); letter-spacing: .2em; display: block; margin-bottom: 6px; font-weight: 600; font-style: normal; }
.diag-box.green::before { color: var(--green); content: "DIAGNÓSTICO · "; }
.diag-box.yellow::before { color: var(--yellow); content: "ATENÇÃO · "; }
.diag-box.red::before { color: var(--red); content: "ALERTA · "; }

/* Action box */
.action-box { border: 1px solid var(--accent); background: var(--accent-soft); border-radius: var(--radius); padding: 16px 20px; margin: 14px 0; font-size: .85rem; color: var(--text-mid); line-height: 1.65; }
.action-box::before { content: "AÇÃO RECOMENDADA"; display: block; font-family: var(--font-mono); font-size: .68rem; color: var(--accent); letter-spacing: .2em; margin-bottom: 8px; font-weight: 600; }

/* Mini bar */
.mini-bar-wrap { background: var(--border); border-radius: 4px; height: 6px; width: 80px; display: inline-block; vertical-align: middle; margin-right: 6px; }
.mini-bar { height: 100%; border-radius: 4px; background: var(--accent); }

/* Handoff pills */
.terms { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.term { font-family: var(--font-mono); font-size: .75rem; padding: 4px 12px; border: 1px solid var(--border); border-radius: 999px; color: var(--text-muted); }
.term.next { color: var(--accent); border-color: var(--accent-deep); background: var(--accent-soft); }

/* Footer */
.page-foot { margin-top: 48px; padding-top: 20px; border-top: 1px solid var(--border); }

@media (max-width: 768px) {
  .card-grid, .card-grid-3, .fmt-compare { grid-template-columns: 1fr; }
  .funnel-row { flex-wrap: wrap; }
  .container { padding: 16px; }
  .topbar { flex-direction: column; align-items: flex-start; }
  .stats-grid { grid-template-columns: 1fr 1fr; }
}
@media print {
  body { background: white; color: #111; }
  .topbar { background: #1e293b; }
  .card { background: white; border-color: #e2e8f0; }
  .stat-card { background: white; border-color: #e2e8f0; }
}

/* ── Gráficos (SVG / CSS inline, sem dependência externa) ── */
.charts-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(300px,1fr)); gap: 16px; margin-bottom: 16px; }
.chart-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px 24px; margin-bottom: 16px; }
.chart-title { font-family: var(--font-mono); font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 16px; }
.chart-svg { width: 100%; height: auto; display: block; }
/* Funil (decrescente, larguras em escala log para visibilidade) */
.funnel { display: flex; flex-direction: column; gap: 12px; }
.funnel-stage { text-align: center; }
.funnel-stage .fl { font-size: .75rem; color: var(--text-mid); margin-bottom: 4px; font-weight: 600; }
.funnel-bar { margin: 0 auto; height: 36px; border-radius: 6px; background: linear-gradient(90deg,var(--accent-deep),var(--accent)); display: flex; align-items: center; justify-content: center; color: var(--on-accent); font-weight: 700; font-size: .85rem; min-width: 84px; font-family: var(--font-mono); }
.funnel-meta { font-size: .7rem; color: var(--text-muted); margin-top: 3px; font-family: var(--font-mono); }
/* Barras pareadas WoW (atual vs anterior) */
.wow-chart { display: flex; gap: 14px; align-items: flex-end; justify-content: space-around; }
.wow-group { display: flex; flex-direction: column; align-items: center; gap: 8px; flex: 1; }
.wow-bars { display: flex; gap: 6px; align-items: flex-end; height: 130px; }
.wow-bar { width: 26px; border-radius: 4px 4px 0 0; }
.wow-bar.prev { background: var(--border); }
.wow-bar.cur { background: var(--accent); }
.wow-bar.cur.good { background: var(--green); }
.wow-bar.cur.bad { background: var(--red); }
.wow-label { font-size: .74rem; color: var(--text-mid); text-align: center; }
.wow-val { font-size: .64rem; color: var(--text-muted); font-family: var(--font-mono); }
/* Barras horizontais (alocação de verba: convertendo vs queimando) */
.hbar-row { display: grid; grid-template-columns: 210px 1fr 150px; gap: 12px; align-items: center; margin-bottom: 8px; }
.hbar-name { font-size: .78rem; color: var(--text-mid); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hbar-track { background: var(--bg); border-radius: 6px; height: 22px; overflow: hidden; }
.hbar-fill { height: 100%; border-radius: 6px; }
.hbar-fill.win { background: linear-gradient(90deg,var(--green-deep),var(--green)); }
.hbar-fill.burn { background: linear-gradient(90deg,var(--red-deep),var(--red)); }
.hbar-val { font-size: .74rem; color: var(--text-muted); font-family: var(--font-mono); text-align: right; }
/* Linha de tendência (legenda do eixo duplo) */
.chart-legend { display: flex; gap: 18px; justify-content: center; margin-top: 12px; font-size: .72rem; color: var(--text-muted); font-family: var(--font-mono); flex-wrap: wrap; }
.chart-legend .lg { display: inline-flex; align-items: center; gap: 6px; }
.chart-legend .sw { width: 14px; height: 3px; border-radius: 2px; display: inline-block; }
.chart-legend .sw.box { width: 12px; height: 12px; border-radius: 3px; }
/* Funil duplo lado a lado (receita J) */
.dual-funnel-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.dual-funnel-col .df-name { text-align: center; font-size: .8rem; font-weight: 700; color: var(--text); margin-bottom: 10px; }
/* Barras das 5 dimensões do Health Score (output [1]); cor do fill inline, pela faixa */
.dim-row { display: grid; grid-template-columns: 200px 1fr 64px; gap: 12px; align-items: center; margin-bottom: 10px; }
.dim-label { font-size: .8rem; color: var(--text-mid); }
.dim-track { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; height: 12px; overflow: hidden; }
.dim-fill { height: 100%; border-radius: 6px; background: var(--accent); }
.dim-score { font-family: var(--font-mono); font-size: .78rem; color: var(--text-muted); text-align: right; }
/* Heatmap (receita H), gauge (I), scatter (K), barras verticais (G) e linha genérica (F)
   são SVG inline: estilo vem nos atributos do próprio SVG, sem CSS adicional. */
```

> **Responsivo dos gráficos:** acrescentar ao bloco `@media (max-width: 768px)` as regras `.hbar-row { grid-template-columns: 110px 1fr 110px; gap: 8px; }` e `.dim-row { grid-template-columns: 110px 1fr 48px; gap: 8px; }` para os nomes não estourarem no celular.
>
> **`.dim-fill`:** a largura e a cor vão inline, ex: `<div class="dim-fill" style="width:72%;background:var(--yellow)"></div>`, com a cor pela faixa do Health Score (`--green` ≥ 85, `--yellow` 70 a 84, `--orange` 50 a 69, `--red` < 50).

#### 3.2.c Cores de gráfico por tema (tabela CORES_GRAFICO, regra dura)

Os SVGs levam cor **em atributo** (não em CSS), então o tema precisa entrar na hora de gerar a geometria/render. As **receitas A–L e os snippets abaixo estão escritos com os hexes do tema Escuro**; ao gerar em outro tema, substituir cada papel pelo equivalente da tabela. Proibido usar cor fora desta tabela dentro dos SVGs.

| Papel no SVG | Escuro | Terra | Claro Neutro |
|---|---|---|---|
| `GRID` (grade, eixos, trilho de gauge, linhas de quadrante) | `#1f1f1f` | `#E9E8E3` | `#e2e8f0` |
| `LABEL` (rótulos de eixo, textos pequenos) | `#d1d5db` | `#887366` | `#64748b` |
| `VALUE` (valor numérico sobre o gráfico) | `#ededea` | `#554338` | `#334155` |
| `ACCENT` (série principal, polígono de radar, barra neutra) | `#3b82f6` | `#E26A2C` | `#2563eb` |
| `ACCENT_AREA` (fill de área sob a linha) | `rgba(59,130,246,.22)` | `rgba(226,106,44,.18)` | `rgba(37,99,235,.15)` |
| `GREEN` (bom) | `#10b981` | `#496547` | `#059669` |
| `YELLOW` (atenção) | `#f59e0b` | `#C9922E` | `#d97706` |
| `ORANGE` (regular) | `#f97316` | `#974800` | `#ea580c` |
| `RED` (crítico) | `#ef4444` | `#BA1A1A` | `#dc2626` |
| `HEAT_BASE` (base do heatmap `intensity`) | `#0d1f2d` | `#F5F4EF` | `#eff6ff` |
| `HEAT_EMPTY` (célula sem dado) | `#0d0d0d` | `#E9E8E3` | `#f1f5f9` |

No `geom_heatmap`, passar pelo spec: `"empty_fill": HEAT_EMPTY`, `"intensity_base": HEAT_BASE`, `"intensity_accent": ACCENT`, e (nas escalas `good_low`/`good_high`) `"good_color": GREEN` e `"bad_color": RED` do tema ativo. Nos demais tipos (`line`, `vbars`, `gauge`, `scatter`, `radar`), a cor já vai no próprio spec (`color` por série/barra/zona/ponto): usar os valores da tabela.

### 3.2.1 Componentes de gráfico (SVG / CSS inline): receitas reprodutíveis

Todos os gráficos são desenhados direto no HTML, **sem biblioteca, sem CDN** (mantém o princípio standalone). Cada um tem uma receita determinística a partir do JSON do `trafego_processar.py`.

**A. Radar das 5 dimensões do Health Score** (usa `health.dimensoes`)

SVG `viewBox="0 0 360 300"`, centro `(cx,cy)=(180,160)`, raio `R=120` para score 100. As 5 dimensões ficam nos ângulos `θ_i = -90° + 72°·i` (i de 0 a 4), na ordem D1 Diversidade (topo), D2 Públicos, D3 Funil, D4 Financeira, D5 Consistência. Para cada ponto: `r = R · score/100`, `x = cx + r·cos(θ_i)`, `y = cy + r·sin(θ_i)`.

Camadas, nesta ordem: (1) 2 polígonos de grade faint (`stroke #1f1f1f`) em r=120 e r=60; (2) 5 linhas de eixo do centro às pontas externas; (3) polígono de dados `fill rgba(59,130,246,.25) stroke #3b82f6`; (4) um `circle r=3.5` em cada vértice de dado, **colorido pela mesma faixa da classificação do Health Score** (`#10b981` verde ≥85, `#f59e0b` amarelo 70–84, `#f97316` laranja 50–69, `#ef4444` vermelho <50), a cor de cada vértice deve bater com a cor da barra (`.dim-fill`) da mesma dimensão na Resposta 5; (5) um `text font-size=10 fill #d1d5db` por eixo com `Nome · score`.

Cos/sin já resolvidos para os 5 eixos: θ0 `(0,-1)` · θ1 `(0.9511,-0.3090)` · θ2 `(0.5878,0.8090)` · θ3 `(-0.5878,0.8090)` · θ4 `(-0.9511,-0.3090)`.

**B. Funil VTSD** (usa `agregado`: `impressions`, `link_clicks`, `lpv`, `purchases`)

4 estágios decrescentes (`.funnel` + `.funnel-stage` + `.funnel-bar`): Impressões → Cliques no link → Visitas à página (LPV) → Vendas. **Largura de cada barra em escala logarítmica** para todos os estágios ficarem visíveis (a queda de milhões para dezenas zera barras lineares): `width% = log10(valor) / log10(impressions) · 100`. Os números exibidos são os reais; em cada estágio (menos o primeiro) mostrar no `.funnel-meta` a taxa de conversão real **em relação ao estágio anterior** (CTR link, connect rate, taxa de compra).

**C. Barras pareadas mês/semana atual vs anterior** (usa `wow`)

4 grupos (`.wow-group`): Gasto, Vendas, ROAS, CPA. Em cada grupo, 2 barras (`.wow-bar.prev` anterior + `.wow-bar.cur` atual). Altura normalizada ao maior do par: `height_px = 130 · valor / max(atual, anterior)`. A barra atual recebe `.good` (verde) quando evoluiu na direção desejada (Vendas/ROAS ↑, CPA ↓), `.bad` (vermelho) quando piorou; Gasto fica neutro (accent). Legenda final explicando claro = anterior, colorido = atual.

**D. Alocação de verba: convertendo vs queimando** (usa `ranking_spend` + `sinais.queima`)

Barras horizontais (`.hbar-row`): top 5 campanhas que **venderam** (`purchases > 0`, classe `.win` verde) seguidas das top 5 **queimadoras** (`sinais.queima`, classe `.burn` vermelho). Largura `width% = spend / max_spend · 100` usando o maior gasto do conjunto como 100%. Cada linha: nome truncado · barra · `R$ {gasto} · {n} vendas`.

**E. Linha de tendência diária: gasto + vendas** (usa `serie_diaria_svg`, pré-calculado pelo `trafego_processar.py`)

Gráfico de linha de eixo duplo dentro de um `.chart-card` full-width, logo após o `.charts-grid` (radar + funil). **Toda a geometria já vem pronta** no objeto `serie_diaria_svg` do processador: o gerador do HTML **não calcula nenhum ponto à mão**, apenas injeta as strings. Isso mantém o gráfico 100% determinístico mesmo com ~30 dias de dados.

Campos de `serie_diaria_svg` e onde entram no SVG (`viewBox` = campo `viewbox`, fixo `0 0 720 240`):

| Campo | Uso no SVG |
|---|---|
| `area_points` | `<polygon>` da área de gasto, `fill="rgba(59,130,246,.12)" stroke="none"` |
| `spend_points` | `<polyline>` de gasto (azul), `stroke="#3b82f6" stroke-width="2" fill="none"`: escala do **eixo esquerdo** |
| `vendas_points` | `<polyline>` de vendas (verde), `stroke="#10b981" stroke-width="2" fill="none"`: escala do **eixo direito** |
| `vendas_dots` | um `<circle r="2.5" fill="#10b981">` por item com `v > 0` (`cx`/`cy` do item) |
| `x_labels` | um `<text y="228" text-anchor="middle" font-size="10" fill="#d1d5db">` por item, em `x` com o `label` (DD/MM) |
| `max_spend` | rótulo do topo do eixo esquerdo (formatar `R$ {x/1000} k`), com `0` na base (`y≈207`) |
| `max_vendas` | rótulo do topo do eixo direito, com `0` na base |
| `baseline_y`, `plot_left`, `plot_right` | linhas de grade horizontais (topo `y=16`, meio `y≈113`, base `baseline_y`) em `stroke="#1f1f1f"` |

Fechar com `.chart-legend` (azul = Gasto/dia eixo esq. · verde = Vendas/dia eixo dir.) e um `.funnel-meta` curto destacando o pico de gasto e o pico de vendas (datas vêm da `serie_diaria`). Se `serie_diaria_svg` for `null` (sem dados de série diária no cache, ex: cache antigo sem `1e`), **omitir o gráfico** sem quebrar o resto.

### 3.2.1.1 Helper de geometria para gráficos pesados/novos (receitas F a L)

Gráficos com muitos pontos (linha de N meses, heatmap de dezenas de células) ou geometria não trivial (gauge, funil duplo, scatter) **NÃO devem ser plotados à mão**: vira fonte de erro. Use o helper **`.claude/skills/trafego-analise/scripts/trafego_chart_geom.py`**: matemática pura, **sem token, sem Graph API**. Recebe um spec JSON no stdin e devolve a geometria pronta (points, rects, paths, labels) para colar no SVG. É a mesma filosofia do `serie_diaria_svg`, generalizada para qualquer output.

> Como o helper **não toca a API nem carrega token**, ele é exceção às restrições de `curl`/Python da Graph API (regra global EXECUÇÃO TÉCNICA). Padrão recomendado (evita dor de cabeça com aspas no shell): gravar o spec num arquivo temporário e redirecionar o stdin:
> ```bash
> {PY} .claude/skills/trafego-analise/scripts/trafego_chart_geom.py <tipo> < /tmp/spec_chart.json
> ```

Tipos: `line` (F), `vbars` (G), `heatmap` (H), `gauge` (I), `dual_funnel` (J), `scatter` (K), `radar` (L). Há também `divbars` (barras divergentes com linha do zero, usadas pelo painel de decisão do `/trafego-otimizar`).

**F. Linha genérica (1+ séries, eixo simples ou duplo)**: tendências mensais ([5] CPM, [7] CPA/CPL), série de audience ([8]), CTR ([10]). Versão reutilizável da receita E para qualquer output.

Spec: `{"viewbox":[720,240],"x_labels":[...],"series":[{"name","color","axis":"left|right","values":[...],"area":bool,"dots":bool}]}`. Saída: por série `points` (+ `area_points`, `dots`), `max_left`/`max_right`, `x_labels`, `grid_y`, `baseline_y`. Template = igual ao gráfico de tendência do [1]: `<polygon points="{area_points}">` + um `<polyline points="{points}">` por série + dots + grade horizontal em `grid_y` + labels de X. Legenda `.chart-legend` com `.sw` na cor de cada série. Datas ISO nos `x_labels` já saem como DD/MM.

**G. Barras verticais**: [5] CPA por faixa horária, [7] top 5 anúncios por venda. Spec: `{"bars":[{"label","value","color"}]}`. Saída: por barra `x,y,w,h,cx,color,label,value`. Template: `<rect x y width=w height=h rx=4 fill=color>` + `<text x=cx y=baseline+16 text-anchor=middle>{label}</text>`. Cor por semântica (verde bom, vermelho ruim, accent neutro).

**H. Heatmap (matriz linhas × colunas)**: [5] hora × dia da semana. Spec: `{"rows":[...],"cols":[...],"matrix":[[v|null,...]],"scale":"good_low|good_high|intensity"}`. `good_low` = baixo verde → alto vermelho (use para CPA/CPL, onde baixo é bom); `intensity` = fundo → accent (volume/conversões). Saída: `cells[{x,y,w,h,fill,value}]`, `row_labels[{y,label}]`, `col_labels[{x,label}]`, `label_x`, `col_label_y`. Template: um `<rect>` por célula com `fill`; `<text>` por rótulo de linha (em `label_x`) e coluna (em `col_label_y`); opcional `<text>` central nas células-chave. Célula sem dado vem com `empty_fill`.

**I. Gauge semicircular**: [9] headroom de escala do candidato principal. Spec: `{"value","max","label","unit","zones":[{"upto":frac,"color"}]}`. Saída: `track` (path do trilho), `zone_arcs[{path,color}]`, `value_arc` (path até o valor), `needle{x,y}`, `frac`, `cx,cy,r`. Template: `<path d="{track}" stroke="#1f1f1f" fill="none" stroke-width="14">` + um `<path d stroke=color fill=none stroke-width=14>` por zona + `<path d="{value_arc}" ... stroke-width=14 stroke-linecap="round">` + `<circle>` no `needle` + `<text>` central com valor+unidade e o `label`.

**J. Funil duplo (A vs B lado a lado)**: [10] Comparativo. Spec: `{"a":{"name","stages":[{"label","value"}]},"b":{...}}`. Saída: por lado `stages[{label,value,width_pct,meta_pct}]` (largura em escala log do topo, igual à receita B). Template: `.dual-funnel-grid` com 2 `.dual-funnel-col`; em cada, um `.df-name` + os estágios como `.funnel-stage`/`.funnel-bar` (`style="width:{width_pct}%"`) + `.funnel-meta` com `{meta_pct}% do estágio anterior`.

**K. Scatter / quadrante**: [6] CPC × Connect Rate. Spec: `{"points":[{"x","y","label","color","r"}],"x_mid","y_mid","x_label","y_label"}`. Saída: `points[{cx,cy,r,color,label}]`, `x_mid_px`/`y_mid_px` (linhas de quadrante), `plot_*`, `x_label`/`y_label`. Template: 2 `<line>` de quadrante (em `x_mid_px`/`y_mid_px`, `stroke="#1f1f1f" stroke-dasharray="3 3"`) + um `<circle>` por ponto + `<text>` do label ao lado + `<text>` dos eixos. Colorir cada ponto pela zona desejada (verde = quadrante bom).

**L. Radar de N eixos**: versão genérica da receita A para qualquer nº de dimensões (ex: [2] 5 etapas do funil, [8] 7 problemas). Spec: `{"viewbox":[420,360],"max":100,"rings":[100,50],"axes":[{"label","value","color"}]}`. Saída: `grid_polys` (anéis), `axis_lines[{x2,y2}]`, `data_points` (polígono de dados), `vertices[{x,y,color,value}]`, `labels[{x,y,anchor,text}]`, `cx,cy,r`. Template: um `<polygon>` por anel de grade (`stroke="#1f1f1f" fill="none"`) + um `<line>` do centro (`cx,cy`) a cada `axis_lines` + `<polygon points="{data_points}">` preenchido + um `<circle r="3.5">` por vértice na cor dele + um `<text>` por label com seu `anchor`. **Rótulos curtos** (≤12 chars) continuam recomendados, mas desde 2026-07-20 o helper faz clamp automático: rótulo que estouraria o viewBox é puxado pra dentro (nunca sai cortado). Alargue a largura do viewBox se tiver muitos eixos. Para "saúde" (maior=melhor) colora o vértice verde no alto; para "problemas" (maior=pior) colora verde no baixo e vermelho no alto.

### 3.2.1.2 Como CONSUMIR o `trafego_chart_geom.py` (correção de 2026-05-29: evita adivinhação)

> **Por que esta seção existe:** as receitas A a L acima descrevem o *spec de entrada* e o *template de saída*, mas não os **nomes das funções**, o **formato real do retorno** nem **como montar o spec sem os scripts de fetch** (modo `MCP_CONECTOR`). Sem isso, o gerador erra por tentativa (já aconteceu: chamou função inexistente, leu `viewbox` como lista, usou campo `label_x` que não existe). Esta seção fecha esses três buracos.

**A. Chamada do helper.** Duas formas equivalentes (ambas sem token, rodam em qualquer modo):

```bash
# via CLI (spec por arquivo pra não brigar com aspas do shell); {PY} = python3 ou py -3
{PY} .claude/skills/trafego-analise/scripts/trafego_chart_geom.py <tipo> < /tmp/spec.json
```
```python
# via import (quando o gerador do HTML é um script Python)
import sys; sys.path.insert(0, ".claude/skills/trafego-analise/scripts")
import trafego_chart_geom as G
geo = G.geom_radar(spec)   # spec é dict Python
```

**Tipo no CLI ≠ nome da função no import.** Mapa exato (errar aqui = `AttributeError`):

| CLI `<tipo>` | função no import | gráfico |
|---|---|---|
| `line` | `G.geom_line` | linha (tendência diária, CPM mês a mês) |
| `vbars` | `G.geom_vbars` | barras verticais |
| `heatmap` | `G.geom_heatmap` | matriz hora×dia |
| `gauge` | `G.geom_gauge` | medidor semicircular |
| `dual_funnel` | `G.geom_dual_funnel` | 2 funis lado a lado |
| `scatter` | `G.geom_scatter` | dispersão/quadrante |
| `radar` | `G.geom_radar` | radar de N eixos |
| `divbars` | `G.geom_divbars` | barras divergentes (lucro × queima) |

**B. Formato real do retorno (o que confunde).** A saída é sempre JSON. Detalhes que já causaram erro:
- `viewbox` volta como **string pronta** `"0 0 440 360"`: usar direto em `viewBox="{geo['viewbox']}"`. **Não** é lista; não fazer `W,H = geo["viewbox"]`.
- `geom_vbars` → cada barra tem `x, y, w, h, cx, color, label, value` e o objeto tem `baseline_y`. **Não existe `label_x`/`label_y`**: o rótulo vai centrado em `cx`, na linha `baseline_y + ~16`. O valor vai em `cx`, `y - 6`.
- `geom_radar` → `grid_polys` (lista de strings de `points`), `axis_lines[{x2,y2}]`, `data_points` (string), `vertices[{x,y,color,value}]`, `labels[{x,y,anchor,text}]`, mais `cx,cy,r`.
- `geom_line` → por série: `points` (string), `area_points` (se `area:true`), `dots` (se `dots:true`); mais `baseline_y`, `grid_y`, `x_labels[{x,label}]`, `max_left`, `max_right`.

**Snippets de render prontos** (colar a saída do helper; validados em produção 2026-05-29 e parametrizados por tema 2026-07-20). O dicionário `C` traz as cores do tema ativo conforme a tabela CORES_GRAFICO (3.2.c): o default abaixo é o tema Escuro:

```python
C = {"GRID":"#1f1f1f","LABEL":"#d1d5db","VALUE":"#ededea",
     "ACCENT":"#3b82f6","ACCENT_AREA":"rgba(59,130,246,.22)"}  # trocar pelos valores do tema ativo (3.2.c)

def radar_svg(geo, C=C):
    s=[f'<svg class="chart-svg" viewBox="{geo["viewbox"]}" xmlns="http://www.w3.org/2000/svg">']
    for poly in geo["grid_polys"]:      s.append(f'<polygon points="{poly}" stroke="{C["GRID"]}" fill="none"/>')
    for al in geo["axis_lines"]:        s.append(f'<line x1="{geo["cx"]}" y1="{geo["cy"]}" x2="{al["x2"]}" y2="{al["y2"]}" stroke="{C["GRID"]}"/>')
    s.append(f'<polygon points="{geo["data_points"]}" fill="{C["ACCENT_AREA"]}" stroke="{C["ACCENT"]}" stroke-width="2"/>')
    for v in geo["vertices"]:           s.append(f'<circle cx="{v["x"]}" cy="{v["y"]}" r="4" fill="{v["color"]}"/>')
    for l in geo["labels"]:             s.append(f'<text x="{l["x"]}" y="{l["y"]}" text-anchor="{l["anchor"]}" font-size="11" fill="{C["LABEL"]}" font-family="monospace">{l["text"]}</text>')
    return "\n".join(s)+"</svg>"

def vbars_svg(geo, unit="", C=C):
    base=geo["baseline_y"]
    s=[f'<svg class="chart-svg" viewBox="{geo["viewbox"]}" xmlns="http://www.w3.org/2000/svg">',
       f'<line x1="0" y1="{base}" x2="{geo["plot_right"]}" y2="{base}" stroke="{C["GRID"]}"/>']
    for b in geo["bars"]:
        s.append(f'<rect x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" rx="4" fill="{b["color"]}"/>')
        s.append(f'<text x="{b["cx"]}" y="{b["y"]-6}" text-anchor="middle" font-size="11" fill="{C["VALUE"]}" font-family="monospace">{b["value"]}{unit}</text>')
        s.append(f'<text x="{b["cx"]}" y="{base+16}" text-anchor="middle" font-size="10" fill="{C["LABEL"]}" font-family="monospace">{b["label"]}</text>')
    return "\n".join(s)+"</svg>"
```

**C. Montando o spec SEM os scripts de fetch (modo `MCP_CONECTOR`).** Quando os números foram processados à mão (sem `trafego_processar.py`), **não existem** `serie_diaria_svg`/`health.dimensoes` prontos: montar o spec do helper a partir dos números já calculados:

| Gráfico obrigatório | Como montar o spec com os números em mãos |
|---|---|
| Radar Health Score ([1]) | `geom_radar` com 5 `axes` = as 5 dimensões já pontuadas (0–100), cor por faixa (verde ≥85, amarelo 70–84, laranja 50–69, vermelho <50) |
| Radar funil vs benchmark ([2]) | `geom_radar` com cada etapa **normalizada ao benchmark**: `value = min(metrica/alvo, 1)*100`. Ex: CTR 2,42% / alvo 2% → 100; Connect 55,4% / alvo 70% → 79 |
| Barras posicionamento ([2]) | `geom_vbars`, um `bar` por posição com `value=ROAS`, cor por faixa |
| Funil (B) | é CSS puro (`.funnel`), **não** usa o helper: montar as `.funnel-bar` direto com largura log e os números reais |
| Linha de tendência diária (E) | `geom_line` com `series=[{name:"Gasto",axis:"left",area:true,values:[...por dia]},{name:"Vendas",axis:"right",dots:true,values:[...]}]` e `x_labels` = datas. **Exige série diária**: ver regra de busca na seção 5, passo 8c |

**Regra de cor por faixa (reuso):** verde `#10b981` (bom), amarelo `#f59e0b` (atenção), laranja `#f97316` (regular), vermelho `#ef4444` (crítico), valores do **tema Escuro**; nos temas Terra e Claro Neutro, usar os equivalentes `GREEN`/`YELLOW`/`ORANGE`/`RED` da tabela CORES_GRAFICO (3.2.c). Usar a MESMA cor no vértice do radar e na barra `.dim-fill` da dimensão correspondente.

---

### 3.3 Casca compartilhada (`index.html`): wrapper simples

A pasta `meus-produtos/{ativo}/trafego/analise/` ganha um arquivo **`index.html`** que serve de porta de entrada. Estrutura: **sem sidebar, sem navegação**: apenas um iframe full-screen que carrega o snapshot mais recente do output gerado.

**Regra:** o `index.html` é **regenerado a cada export individual**, apontando sempre para o snapshot recém-criado.

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Tráfego Análise · {Produto}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    /* {BG_TEMA} = valor de --bg do tema ativo; {SCHEME} = dark no Escuro, light no Terra/Claro Neutro */
    html, body { height: 100%; background: {BG_TEMA}; color-scheme: {SCHEME}; }
    body { display: flex; flex-direction: column; height: 100vh; }
    iframe { flex: 1; border: 0; display: block; width: 100%; }
  </style>
</head>
<body>
  <iframe src="{slug}-{YYYY-MM-DD-HHMM}.html"></iframe>
</body>
</html>
```

---

## 4. Mapeamento de blocos → componentes do design system

Cada um dos 10 outputs tem blocos próprios descritos na sua sub-skill respectiva. Regra de mapeamento:

| Tipo de conteúdo no output narrado | Componente HTML |
|---|---|
| KPIs globais (spend, ROAS, CPA, tier %) | `.stats-grid` com `.stat-card` por métrica (`.value.green/.yellow/.red` para cor semântica) |
| Seção de resposta obrigatória (Resposta N) | `.section` com `.section-header` (`.section-num` + `.section-title` + `.section-question`) |
| Sub-título de seção adicional | `.section-h` |
| Comparativo de formato imagem/vídeo | `.card` + `.fmt-compare` com `.fmt-box` por formato |
| Funil de retenção de vídeo | `.card` + `.funnel-row` com `.funnel-item` (`.fi-label` / `.fi-value` / `.fi-sub`) |
| Ranking top 5/10 por CPA, CTR, etc. | `table` com `th`/`td`, `.num` para colunas numéricas, `.rank` para posição, `.ad-name` para nome do ad |
| "No VTSD isso significa..." | `.diag-box` (azul padrão, sem modificador) |
| Diagnóstico positivo / sinal verde | `.diag-box.green` |
| Diagnóstico de atenção / sinal amarelo | `.diag-box.yellow` |
| Alerta crítico / sinal vermelho | `.diag-box.red` |
| Ação recomendada concreta | `.action-box` |
| Handoff para skill executora | `.term.next` dentro de `.terms` |
| Tier de criativo (S/A/B/C/D) | `.tier-s` / `.tier-a` / `.tier-b` / `.tier-c` / `.tier-d` |
| Tipo de criativo (vídeo/imagem) | `.tag-video` / `.tag-imagem` |
| Mini barra de progresso | `.mini-bar-wrap` + `.mini-bar` com `width` inline |

**Regras de mapeamento:**
1. Valores numéricos em tabela: usar classe `.num` (alinhamento direita + fonte mono).
2. Cor semântica nas métricas: `var(--green)` = positivo/acima do benchmark, `var(--yellow)` = atenção, `var(--red)` = crítico/abaixo.
3. Todo bloco de conteúdo narrativo principal vai dentro de um `.card` para manter a separação visual.
4. Nunca inventar cor fora da paleta: usar apenas as variáveis do bloco de tema (3.2.a): `--text*`, `--green`, `--yellow`, `--red`, `--orange`, `--accent` e as variantes `-soft`/`-faint`/`-deep`/`tier-*`/`tag-*`.
5. Fundo é sempre `--bg` e texto principal é `--text` do tema ativo (Escuro: preto/branco; Terra: sage/quase-preto; Claro Neutro: cinza-claro/azul-escuro). Nunca hardcodear o valor.

---

## 5. Algoritmo de geração

A skill executa **três fases**: gera o snapshot individual, atualiza o painel de entregas do produto e abre o painel no navegador.

```
FASE 1. Gerar snapshot individual

1. Capturar payload narrado que acabou de ser entregue ao aluno (Blocos 1, 2, 3, 4...).
2. Identificar slug do output ([1] → diagnostico-rapido, etc).
3. Ler produto ativo de meus-produtos/.ativo.
4. Calcular timestamp atual em formato YYYY-MM-DD-HHMM (local).
5. Calcular caminho final: meus-produtos/{ativo}/trafego/analise/{slug}-{timestamp}.html
   Criar a pasta trafego/analise/ se não existir.
5b. Resolver o TEMA: usar o tema pedido na resposta do aluno ou, na ausência, o EXPORT_TEMA do .env.
    Definir data-theme no <html>, o link de fontes, o bloco de tokens (3.2.a) e as cores de
    gráfico (tabela CORES_GRAFICO, 3.2.c) correspondentes.
6. Carregar template HTML da seção 3.1 + bloco do tema (3.2.a) + componentes (3.2.b).
7. Substituir variáveis do header: {Output}, {N}, {janela}, {act_id mascarado}, {DD/MM/YYYY HH:MM}.
8. Para cada bloco do output narrado, mapear para componente HTML conforme seção 4 e injetar.
8b. Se a sub-skill do output definir uma seção "Gráficos obrigatórios" (ex: `1-diagnostico-rapido.md`), renderizar esses gráficos em SVG/CSS inline conforme as receitas da seção 3.2.1, logo após o `.stats-grid` de KPIs, sob um `.section-h` "Visão visual". Sem biblioteca, sem CDN. **Como chamar o helper e ler o retorno: seção 3.2.1.2** (nomes das funções, formato da saída, snippets prontos, montagem do spec sem os scripts de fetch).
8c. **Gráfico de tendência diária (receita E): buscar o dado antes, não pular silenciosamente.** Se a série diária não estiver em cache (`serie_diaria_svg=null`, ou modo MCP onde os números foram processados à mão): antes de exportar, fazer **1 busca extra** da série diária no mesmo período e escopo (modo APP: insights `level=campaign&time_increment=1`; modo MCP: `ads_insights_performance_trend` com granularidade diária), agregar por dia e montar o spec do `geom_line`. Só omitir o gráfico se a busca também não retornar dados e, nesse caso, **dizer ao aluno que foi omitido e por quê**. Nunca deixar de fora sem avisar.

   **Regra obrigatória de estrutura:** cada bloco "Resposta N" do output narrado vira uma `.section` com `.section-header`. A estrutura de cada seção de resposta é:

   ```html
   <div class="section">
     <div class="section-header">
       <div class="section-num">{N}</div>
       <div>
         <div class="section-title">{título curto da resposta}</div>
         <div class="section-question">{texto exato da pergunta, extraído do título ### Resposta N. "..."}</div>
       </div>
     </div>
     <!-- conteúdo da resposta: .card + table, .stats-grid, .funnel-row, .dim-row etc. conforme o mapeamento da seção 4 e da sub-skill -->
   </div>
   ```

   O texto da pergunta é extraído literalmente do título `### Resposta N. "..."` do output narrado, sem parafrasear, sem abreviar. Uma `.section` por resposta, na mesma ordem do output. Blocos "Análise adicional" NÃO usam `.section-header`: usam `.section-h` normalmente.
9. Para cada handoff sugerido, criar .term.next dentro do rodapé.
10. Salvar arquivo do snapshot (encoding UTF-8, sem BOM).
10b. **GATE DE CONFORMIDADE (obrigatório, não pular).** Rodar o checklist da seção 0 sobre o arquivo recém-salvo. Se `svg=0` OU `chart-card=0` OU `topbar=0` OU `tema=0` OU `bgok=0`: o export não seguiu o design system, não tem gráficos ou usou tema inventado → **voltar ao passo 5b** (recarregar esqueleto 3.1 + tokens do tema 3.2.a + componentes 3.2.b), gerar a geometria dos gráficos via `trafego_chart_geom.py` e regravar. **Não avançar para a Fase 2 nem anunciar "snapshot salvo" enquanto o gate não passar.**
10c. Regenerar o `index.html` da pasta (seção 3.3), apontando para o snapshot recém-criado.

FASE 2. Atualizar painel de entregas do produto (OBRIGATÓRIO, nunca pular)

11. Executar o script painel-trafego.py IMEDIATAMENTE após salvar o snapshot.
    Esta etapa é obrigatória em 100% das gerações. Não há exceção.

    {PY} "{RAIZ_PROJETO}/scripts/painel-trafego.py" --slug {ativo}

    O script varre meus-produtos/{ativo}/trafego/analise/, lê todos os snapshots HTML,
    gera uma lista cronológica agrupada por dia e substitui a seção analise-trafego
    no painel. O novo snapshot gerado no passo 10 já aparece no topo da lista.

    Se o painel não tiver a seção analise-trafego (produto sem /produto-concepcao concluído):
    registrar aviso no stderr e seguir para a FASE 3 sem travar.

    Se o script falhar por qualquer motivo: reportar o erro ao usuário e não
    fingir que o painel foi atualizado.

FASE 3. Abrir index e painel de entregas no navegador

12. Construir os dois caminhos absolutos:
    - Index:   {RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/analise/index.html
    - Painel:  {RAIZ_PROJETO}/meus-produtos/{ativo}/painel-entregas.html

13. Abrir os dois arquivos em sequência (cada um abre em aba separada do navegador padrão):

    {PY} "{RAIZ_PROJETO}/scripts/abrir-html.py" "{caminho-absoluto-index}"
    {PY} "{RAIZ_PROJETO}/scripts/abrir-html.py" "{caminho-absoluto-painel}"

    Abrir o index primeiro (porta de entrada que carrega o snapshot recém-gerado via iframe) e depois o painel (histórico de entregas).
    Ver seção 9 para fallback cross-platform caso o script falhe.

14. Devolver ao aluno a mensagem abaixo. SEMPRE incluir os dois caminhos absolutos no chat,
    independentemente de o navegador ter aberto ou não. Se o navegador for bloqueado pelo SO,
    o aluno usa os caminhos para abrir manualmente:

    "✅ Snapshot salvo: {slug}-{timestamp}.html
     ✅ Painel de entregas atualizado.
     🌐 Abrindo análise e painel no navegador...

     Caso o navegador não abra automaticamente, copie o caminho e abra no navegador:

     Análise:
     {caminho-absoluto-index}

     Painel de entregas:
     {caminho-absoluto-painel}"
```

---

## 6. Mascarar dados sensíveis no HTML

- **`ad_account_id`**: mostrar só os 4 primeiros e 4 últimos dígitos. Ex: `act_1234******7890`.
- **IDs de campanha/adset/ad** que aparecem em rankings: mostrar últimos 4 dígitos (`...7890`) com nome legível ao lado.
- **Token de acesso, app_id, business_id**: nunca aparecer no HTML, em hipótese alguma.

A skill executa a mascaração antes de injetar no template.

---

## 7. Modo print (PDF)

O CSS já inclui `@media print` que clarifica fundo (HTML pra impressão fica branco com texto escuro). Aluno pode dar `Ctrl+P` no navegador e gerar PDF direto, sem precisar de skill adicional.

---

## 8. Princípios desta sub-skill

0. **Contrato de export (seção 0) é inegociável.** Nunca inventar HTML/tema próprio; sempre partir do esqueleto 3.1 + tokens 3.2; sempre renderizar os gráficos obrigatórios da sub-skill (via `trafego_chart_geom.py` quando não houver os scripts de fetch); rodar o gate de conformidade (passo 10b) antes de entregar.
1. **Nunca sem confirmação.** Aluno precisa dizer "sim" pra gerar HTML.
2. **Snapshot, não live.** Banner de aviso explícito no topo + timestamp visível.
3. **Standalone.** CSS embedado, fontes via Google Fonts, zero dependência local.
4. **Naming determinístico.** `{slug}-{YYYY-MM-DD-HHMM}.html` permite ordenação cronológica e múltiplos exports do mesmo output sem sobrescrever.
5. **Pasta por produto.** Sempre `meus-produtos/{ativo}/trafego/analise/`. Nunca em pasta global, nunca na raiz.
6. **Mascara IDs.** ad_account_id, IDs internos sempre truncados.
7. **Usa só o design system Fluxo Criativo.** Sem inventar cores, fontes ou componentes fora do que está nas seções 3 e 4. Os 3 temas oficiais (Escuro, Terra, Claro Neutro) são as únicas variações permitidas; o tema muda os tokens, nunca a estrutura.
7b. **Tema é escolha do aluno, com memória.** `EXPORT_TEMA` no `.env` guarda o padrão; resposta pontual ("sim, terra") vale só pra aquela geração.
8. **Não atualiza arquivos antigos.** Cada export é arquivo novo. Histórico preservado.
9. **Mensagem final padrão:** sempre informa caminho absoluto + sugere abrir no navegador. Nunca devolve só "salvo".
10. **`index.html` regenerado a cada export.** Aponta para o snapshot recém-criado, garantindo que abrir o index sempre mostra o output mais recente.
11. **Snapshots individuais são páginas standalone completas.** Sem sidebar, sem casca externa. Abrem direto no navegador com todo o conteúdo e design embutidos.
12. **Sempre abrir o navegador no `index.html`** (a porta de entrada). O index carrega o snapshot via iframe em tela cheia.

---

## 9. Comando de abertura no navegador (cross-platform)

**Sempre executado** no fim da Fase 3 do algoritmo. Aponta para o `index.html` (não para o snapshot individual) e depois para o `painel-entregas.html`.

### 9.1 Detecção do SO

Antes de chamar o comando, descobrir o SO atual:

```bash
case "$(uname -s 2>/dev/null || echo Windows)" in
  Linux*)   SO="linux" ;;
  Darwin*)  SO="mac" ;;
  CYGWIN*|MINGW*|MSYS*|Windows*) SO="windows" ;;
  *)        SO="unknown" ;;
esac
```

Em ambientes onde `uname` não existe (PowerShell puro), assumir `windows`.

### 9.2 Comando por SO

| SO | Comando |
|---|---|
| `windows` (Bash/Git Bash) | `start "" "{caminho-absoluto-index}"` (as aspas duplas vazias são título obrigatório do `start`) |
| `windows` (PowerShell) | `Invoke-Item "{caminho-absoluto-index}"` ou `Start-Process "{caminho}"` |
| `mac` | `open "{caminho-absoluto-index}"` |
| `linux` | `xdg-open "{caminho-absoluto-index}"` |

### 9.3 Caminho absoluto (regra dura)

**Tanto o caminho do script `abrir-html.py` quanto o caminho do HTML alvo precisam ser ABSOLUTOS.** Não confiar no `cwd` do shell: ele pode estar contaminado por algum `cd` anterior na sessão.

**Forma correta (recomendada: usa o script Python helper):**

```bash
{PY} "{RAIZ_PROJETO}/scripts/abrir-html.py" "{caminho-absoluto-do-index.html}"
```

Onde `{RAIZ_PROJETO}` é o caminho absoluto da raiz do workspace (descoberta no início da sessão e usada sempre: nunca relativo, nunca `./scripts/...`).

**Exemplo concreto (com placeholders):**

```bash
{PY} "{RAIZ_PROJETO}/scripts/abrir-html.py" "{RAIZ_PROJETO}/meus-produtos/<seu-produto>/trafego/analise/index.html"
```

`{RAIZ_PROJETO}` é resolvido em tempo de execução para o caminho absoluto onde o repositório foi clonado (qualquer pasta, qualquer disco, qualquer SO). Nunca presumir que está em `Documents/GitHub/...` ou em qualquer estrutura fixa.

**Forma alternativa (sem o script, comando nativo direto):**

```bash
# Mac
open "{RAIZ_PROJETO}/meus-produtos/<seu-produto>/trafego/analise/index.html"

# Windows Bash
start "" "{RAIZ_PROJETO}/meus-produtos/<seu-produto>/trafego/analise/index.html"
```

**Erros comuns a evitar:**

| ❌ Errado | ✅ Certo | Motivo |
|---|---|---|
| `{PY} scripts/abrir-html.py "..."` | `{PY} "{RAIZ}/scripts/abrir-html.py" "..."` | cwd pode ter sido alterado por `cd` anterior |
| `cd meus-produtos/{ativo}/...; {PY} abrir-html.py` | usar caminho absoluto pro script direto | `cd` contamina cwd pra próximas chamadas |
| `{PY} ./scripts/abrir-html.py` | absoluto sempre | `./` depende de cwd |
| `start "..."` sem aspas vazias antes | `start "" "..."` | no Bash do Windows, primeiro arg é título; sem `""` o caminho vira título |

**Princípio:** o agente descobre `{RAIZ_PROJETO}` no início da sessão (path absoluto do workspace) e usa esse prefixo em TODA chamada do script. Nunca depender de cwd.

### 9.4 Falha silenciosa

Se o comando de abertura falhar (sem display em servidor remoto, ferramenta ausente), a skill **não trava**. Apenas avisa:

```
✅ Snapshot gerado: {arquivo}
✅ Dashboard atualizado: {caminho-absoluto-do-index}
⚠️ Não consegui abrir o navegador automaticamente. Abra manualmente o arquivo acima.
```

### 9.5 Mensagem padrão de sucesso

```
✅ Snapshot gerado: diagnostico-rapido-2026-05-05-1432.html
✅ Dashboard atualizado: {raiz-do-projeto}\meus-produtos\curso-tarot\trafego\analise\index.html
🌐 Abrindo no navegador...
```
