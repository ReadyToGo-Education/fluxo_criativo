# Sub-skill utilitária. Export HTML de Análise

Sub-skill compartilhada por TODOS os 9 outputs da `/trafego-analise`. Não tem opção própria no menu — é acionada opcionalmente ao final de cada output, quando o aluno responde "sim" à pergunta de export.

**Propósito:** transformar o output narrado de uma análise em um HTML standalone usando o design system Fluxo Criativo, salvar no produto ativo e devolver o caminho absoluto pro aluno abrir no navegador.

---

## 1. Quando rodar

Após o Passo 6 do SKILL.md raiz (entrega da análise narrada), perguntar:

```
Quer salvar essa análise como HTML pra revisitar depois? (s/n)

⚠️ Snapshot: o HTML gerado é uma "fotografia" dos dados deste momento.
   Métricas mudam, e este arquivo NÃO atualiza sozinho. Ele tem o timestamp
   no topo pra deixar claro quando foi gerado. Pra dado fresco, rode a
   análise de novo.
```

Se `s`/`sim`: rodar esta sub-skill. Se `n`/`não` ou silêncio: encerrar normalmente.

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
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>[{N}] {nome do output} — Tráfego Análise</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    {tokens-e-componentes-do-design-system}
  </style>
</head>
<body>

  <!-- Topbar escura com info do snapshot -->
  <div class="topbar">
    <div>
      <div class="topbar-title">[{N}] {nome do output} — Tráfego Análise</div>
      <div class="topbar-meta">
        SNAPSHOT · {DD/MM/YYYY HH:MM} &nbsp;|&nbsp; {janela} &nbsp;|&nbsp; {act_id mascarado} ({nome da conta})
      </div>
    </div>
    <div class="topbar-right">{escopo — ex: VTSD - CV · 38 campanhas ativas}</div>
  </div>

  <!-- Banner de dado expira -->
  <div class="snap-warn">
    Fotografia dos dados em <strong>{DD/MM HH:MM}</strong>.
    Métricas mudam continuamente — para dado atualizado, rode a análise novamente.
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

Design baseado no estilo `dashboard-criativos.html` em dark mode — cards legíveis, números em bold,
seções numeradas, tabelas limpas, cores semânticas (verde/amarelo/vermelho).

Copiar este bloco inteiro dentro de `<style>`:

```css
:root {
  --bg:#000; --bg-alt:#000; --card:#111; --card-hover:#1a1a1a;
  --border:#1f1f1f; --border-light:#181818;
  --text:#ffffff; --text-mid:#ededea; --text-muted:#d1d5db;
  --accent:#3b82f6; --green:#10b981; --yellow:#f59e0b; --red:#ef4444; --orange:#f97316;
  --radius:12px; --shadow:0 1px 3px rgba(0,0,0,.4),0 1px 2px rgba(0,0,0,.3);
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI","Inter",sans-serif;
  --font-mono:"JetBrains Mono","SF Mono","Fira Code",monospace;

}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { color-scheme: dark; }
body { font-family: var(--font); background: var(--bg); color: var(--text); font-size: 14px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
::selection { background: var(--accent); color: #fff; }

/* Topbar */
.topbar { background: var(--bg-alt); border-bottom: 1px solid var(--border); padding: 16px 32px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.topbar-title { font-size: 1rem; font-weight: 700; color: var(--text); letter-spacing: -.3px; }
.topbar-meta { font-size: .78rem; color: var(--text-muted); font-family: var(--font-mono); margin-top: 2px; }
.topbar-right { font-size: .78rem; color: var(--text-muted); text-align: right; }

/* Banner snapshot */
.snap-warn { background: #1a2234; border-left: 3px solid var(--accent); padding: 10px 32px; font-size: .78rem; color: var(--text-muted); font-family: var(--font-mono); }
.snap-warn strong { color: var(--text-mid); font-weight: 400; }

/* Container */
.container { max-width: 1280px; margin: 0 auto; padding: 28px 32px; }

/* Stats grid — KPIs globais */
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
.section-num { background: var(--accent); color: #fff; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: .85rem; font-weight: 700; flex-shrink: 0; }
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
.tier-s { background: #14532d; color: #4ade80; font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tier-a { background: #1a3a5c; color: #60a5fa; font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tier-b { background: #422006; color: #fbbf24; font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tier-c { background: #3b1515; color: #fca5a5; font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tier-d { background: #1f1f1f; color: var(--text-muted); font-size: .72rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tag-video { background: #1d3a6e; color: #93c5fd; font-size: .68rem; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
.tag-imagem { background: #4a1942; color: #f0abfc; font-size: .68rem; font-weight: 600; padding: 2px 8px; border-radius: 999px; }

/* Diagnostic boxes */
.diag-box { border-left: 3px solid var(--accent); background: #1a2234; border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 14px 0; font-size: .85rem; color: var(--text-mid); line-height: 1.65; }
.diag-box.green { background: #0d1f16; border-color: var(--green); }
.diag-box.yellow { background: #1f1600; border-color: var(--yellow); }
.diag-box.red { background: #1f0d0d; border-color: var(--red); }
.diag-box::before { content: "NO VTSD · "; font-family: var(--font-mono); font-size: .68rem; color: var(--accent); letter-spacing: .2em; display: block; margin-bottom: 6px; font-weight: 600; font-style: normal; }
.diag-box.green::before { color: var(--green); content: "DIAGNÓSTICO · "; }
.diag-box.yellow::before { color: var(--yellow); content: "ATENÇÃO · "; }
.diag-box.red::before { color: var(--red); content: "ALERTA · "; }

/* Action box */
.action-box { border: 1px solid var(--accent); background: #111d35; border-radius: var(--radius); padding: 16px 20px; margin: 14px 0; font-size: .85rem; color: var(--text-mid); line-height: 1.65; }
.action-box::before { content: "AÇÃO RECOMENDADA"; display: block; font-family: var(--font-mono); font-size: .68rem; color: var(--accent); letter-spacing: .2em; margin-bottom: 8px; font-weight: 600; }

/* Mini bar */
.mini-bar-wrap { background: var(--border); border-radius: 4px; height: 6px; width: 80px; display: inline-block; vertical-align: middle; margin-right: 6px; }
.mini-bar { height: 100%; border-radius: 4px; background: var(--accent); }

/* Handoff pills */
.terms { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.term { font-family: var(--font-mono); font-size: .75rem; padding: 4px 12px; border: 1px solid var(--border); border-radius: 999px; color: var(--text-muted); }
.term.next { color: var(--accent); border-color: #1d3a6e; background: #111d35; }

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
```

### 3.3 Casca compartilhada (`index.html`) — wrapper simples

A pasta `meus-produtos/{ativo}/trafego/analise/` ganha um arquivo **`index.html`** que serve de porta de entrada. Estrutura: **sem sidebar, sem navegação** — apenas um iframe full-screen que carrega o snapshot mais recente do output gerado.

**Regra:** o `index.html` é **regenerado a cada export individual**, apontando sempre para o snapshot recém-criado.

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Tráfego Análise — {Produto}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { height: 100%; background: #000; color-scheme: dark; }
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

Cada um dos 9 outputs tem blocos próprios descritos na sua sub-skill respectiva. Regra de mapeamento:

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
4. Nunca inventar cor fora da paleta — usar apenas as variáveis `--text`, `--text-mid`, `--text-muted`, `--green`, `--yellow`, `--red`, `--accent`.
5. Fundo é `--bg` (#000 — preto puro). Texto principal é `--text` (#ffffff — branco puro).

---

## 5. Algoritmo de geração

A skill executa **três fases**: gera o snapshot individual, atualiza o painel de entregas do produto e abre o painel no navegador.

```
FASE 1 — Gerar snapshot individual

1. Capturar payload narrado que acabou de ser entregue ao aluno (Blocos 1, 2, 3, 4...).
2. Identificar slug do output ([1] → diagnostico-rapido, etc).
3. Ler produto ativo de meus-produtos/.ativo.
4. Calcular timestamp atual em formato YYYY-MM-DD-HHMM (local).
5. Calcular caminho final: meus-produtos/{ativo}/trafego/analise/{slug}-{timestamp}.html
6. Criar pasta trafego/analise/ se não existir.
7. Carregar template HTML da seção 3.1 + tokens da seção 3.2.
8. Substituir variáveis do header: {Output}, {N}, {janela}, {act_id mascarado}, {DD/MM/YYYY HH:MM}.
9. Para cada bloco do output narrado, mapear para componente HTML conforme seção 4 e injetar.

   **Regra obrigatória de estrutura:** cada bloco "Resposta N" do output narrado deve ser envolvido em um `.section-q`. A estrutura de cada seção de resposta é:

   ```html
   <div class="section-q">
     <div class="section-q-header">
       <div class="section-q-num">{N}</div>
       <div>
         <div class="section-q-title">{texto exato da pergunta, extraído do título ### Resposta N. "..."}</div>
       </div>
     </div>
     <!-- conteúdo da resposta: .table, .kpi-grid, .bar-row, etc. conforme mapeamento da seção 4 -->
   </div>
   ```

   O texto da pergunta é extraído literalmente do título `### Resposta N. "..."` do output narrado — sem parafrasear, sem abreviar. Uma `.section-q` por resposta, na mesma ordem do output. Blocos "Análise adicional" NÃO usam `.section-q` — usam `.section-h` normalmente.
10. Para cada handoff sugerido, criar .term.next dentro do rodapé.
11. Salvar arquivo do snapshot (encoding UTF-8, sem BOM).

FASE 2 — Atualizar painel de entregas do produto (OBRIGATÓRIO — nunca pular)

12. Executar o script painel-trafego.py IMEDIATAMENTE após salvar o snapshot.
    Esta etapa é obrigatória em 100% das gerações. Não há exceção.

    python3 "{RAIZ_PROJETO}/scripts/painel-trafego.py" --slug {ativo}

    O script varre meus-produtos/{ativo}/trafego/analise/, lê todos os snapshots HTML,
    gera uma lista cronológica agrupada por dia e substitui a seção analise-trafego
    no painel. O novo snapshot gerado no passo 11 já aparece no topo da lista.

    Se o painel não tiver a seção analise-trafego (produto sem /produto-concepcao concluído):
    registrar aviso no stderr e seguir para a FASE 3 sem travar.

    Se o script falhar por qualquer motivo: reportar o erro ao usuário e não
    fingir que o painel foi atualizado.

FASE 3 — Abrir index e painel de entregas no navegador

13. Construir os dois caminhos absolutos:
    - Index:   {RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/analise/index.html
    - Painel:  {RAIZ_PROJETO}/meus-produtos/{ativo}/painel-entregas.html

14. Abrir os dois arquivos em sequência (cada um abre em aba separada do navegador padrão):

    python3 "{RAIZ_PROJETO}/scripts/abrir-html.py" "{caminho-absoluto-index}"
    python3 "{RAIZ_PROJETO}/scripts/abrir-html.py" "{caminho-absoluto-painel}"

    Abrir o index primeiro (porta de entrada que carrega o snapshot recém-gerado via iframe) e depois o painel (histórico de entregas).
    Ver seção 9 para fallback cross-platform caso o script falhe.

15. Devolver ao aluno a mensagem abaixo — SEMPRE incluir os dois caminhos absolutos no chat,
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

1. **Nunca sem confirmação.** Aluno precisa dizer "sim" pra gerar HTML.
2. **Snapshot, não live.** Banner de aviso explícito no topo + timestamp visível.
3. **Standalone.** CSS embedado, fontes via Google Fonts, zero dependência local.
4. **Naming determinístico.** `{slug}-{YYYY-MM-DD-HHMM}.html` permite ordenação cronológica e múltiplos exports do mesmo output sem sobrescrever.
5. **Pasta por produto.** Sempre `meus-produtos/{ativo}/trafego/analise/`. Nunca em pasta global, nunca na raiz.
6. **Mascara IDs.** ad_account_id, IDs internos sempre truncados.
7. **Usa só o design system Fluxo Criativo.** Sem inventar cores, fontes ou componentes fora do que está nas seções 3 e 4.
8. **Não atualiza arquivos antigos.** Cada export é arquivo novo. Histórico preservado.
9. **Mensagem final padrão:** sempre informa caminho absoluto + sugere abrir no navegador. Nunca devolve só "salvo".
10. **`index.html` regenerado a cada export.** Aponta para o snapshot recém-criado, garantindo que abrir o index sempre mostra o output mais recente.
11. **Snapshots individuais são páginas standalone completas.** Sem sidebar, sem casca externa. Abrem direto no navegador com todo o conteúdo e design embutidos.
12. **Sempre abrir o navegador no `index.html`** (a porta de entrada). O index carrega o snapshot via iframe em tela cheia.

---

## 9. Comando de abertura no navegador (cross-platform)

**Sempre executado** no fim da Fase 3 do algoritmo. Aponta para o `index.html` (não para o snapshot individual).

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

**Tanto o caminho do script `abrir-html.py` quanto o caminho do HTML alvo precisam ser ABSOLUTOS.** Não confiar no `cwd` do shell — ele pode estar contaminado por algum `cd` anterior na sessão.

**Forma correta (recomendada — usa o script Python helper):**

```bash
python3 "{RAIZ_PROJETO}/scripts/abrir-html.py" "{caminho-absoluto-do-index.html}"
```

Onde `{RAIZ_PROJETO}` é o caminho absoluto da raiz do workspace (descoberta no início da sessão e usada sempre — nunca relativo, nunca `./scripts/...`).

**Exemplo concreto (com placeholders):**

```bash
python3 "{RAIZ_PROJETO}/scripts/abrir-html.py" "{RAIZ_PROJETO}/meus-produtos/<seu-produto>/trafego/analise/index.html"
```

`{RAIZ_PROJETO}` é resolvido em runtime para o caminho absoluto onde o repositório foi clonado (qualquer pasta, qualquer disco, qualquer SO). Nunca presumir que está em `Documents/GitHub/...` ou em qualquer estrutura fixa.

**Forma alternativa (sem o script, comando nativo direto):**

```bash
# Windows Bash
start "" "{RAIZ_PROJETO}/meus-produtos/<seu-produto>/trafego/analise/index.html"
```

**Erros comuns a evitar:**

| ❌ Errado | ✅ Certo | Motivo |
|---|---|---|
| `python3 scripts/abrir-html.py "..."` | `python3 "{RAIZ}/scripts/abrir-html.py" "..."` | cwd pode ter sido alterado por `cd` anterior |
| `cd meus-produtos/{ativo}/...; python3 abrir-html.py` | usar caminho absoluto pro script direto | `cd` contamina cwd pra próximas chamadas |
| `python3 ./scripts/abrir-html.py` | absoluto sempre | `./` depende de cwd |
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
