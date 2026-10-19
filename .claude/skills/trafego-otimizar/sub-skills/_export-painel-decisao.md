# Sub-skill utilitária. Painel de Decisão (export HTML da /trafego-otimizar)

Sub-skill acionada **opcionalmente ao final** do diagnóstico da `/trafego-otimizar`. Transforma o diagnóstico + plano em um HTML standalone, no design system Fluxo Criativo, salvo no produto ativo. **Não** é um relatório (isso é a `/trafego-analise`) nem o dashboard ao vivo da conta (isso é o `/trafego-dashboard`). É um **painel de decisão**: centrado em dinheiro (camada de lucro, §3.6 da SKILL) e nas três zonas, terminando no plano de ação.

---

## 0. CONTRATO DE EXPORT (regra dura, ler antes de gerar qualquer HTML)

> Herdado do contrato da `/trafego-analise` (`.claude/skills/trafego-analise/sub-skills/_export-html.md`). Vale integralmente aqui.

**É PROIBIDO inventar um HTML novo.** O export SEMPRE parte do esqueleto da §3.1 + tokens da §3.2 do `_export-html.md` da análise (design system oficial com **3 temas**: Escuro, Terra e Claro Neutro, §3.2.a de lá; semânticas verde/amarelo/vermelho em todos). A escolha do tema segue a seção 1 do `_export-html.md` da análise (pergunta com opções na primeira vez, depois `EXPORT_TEMA` do `.env`). Nunca criar paleta própria fora dos 3 temas, nunca trocar a topbar/banner por improviso. Cores de SVG conforme a tabela CORES_GRAFICO (§3.2.c de lá).

**É OBRIGATÓRIO renderizar os 3 gráficos** desta sub-skill (§4), com geometria vinda do motor da análise. `{PY}` é o interpretador Python detectado na sessão (`python3` ou `py -3`, conforme o CLAUDE.md):
```
{PY} .claude/skills/trafego-analise/scripts/trafego_chart_geom.py <tipo> < /tmp/spec.json
```
O motor roda nos dois modos (`APP` e `MCP_CONECTOR`), não toca a API e não usa token. Os números vêm do **diagnóstico já calculado na sessão**, sem refazer fetch.

**Checklist de conformidade: rodar ANTES de declarar o painel pronto.** Substituir `<ARQ>`:
```bash
echo -n "svg=";        grep -c "<svg"          <ARQ>   # > 0 (gráficos presentes)
echo -n "chart-card="; grep -c "chart-card"    <ARQ>   # > 0
echo -n "topbar=";     grep -c 'class="topbar' <ARQ>   # >= 1 (design oficial)
echo -n "snap-warn=";  grep -c "snap-warn"     <ARQ>   # >= 1
echo -n "tema=";       grep -cE 'data-theme="(escuro|terra|claro)"' <ARQ> # = 1 (tema oficial declarado)
echo -n "bgok=";       grep -cE -- "--bg:(#000|#D8DDC8|#f4f6f8)" <ARQ>    # = 1 (tokens de tema oficial)
echo -n "zonas=";      grep -c "zona-legenda"  <ARQ>   # >= 1 (legenda das 3 zonas)
echo -n "lucro-kpi=";  grep -c "kpi-lucro"     <ARQ>   # >= 1 (KPI de lucro presente)
```
**Regra de bloqueio:** se qualquer linha falhar (`svg=0`, `chart-card=0`, `topbar=0`, `tema≠1`, `bgok≠1`, `zonas=0`, `lucro-kpi=0`), o painel está ERRADO: **não entregar.** Refazer a partir do esqueleto oficial. Só anunciar "painel salvo" depois que o checklist passar.

> Exceção legítima: se um gráfico depende de dado que não existe (ex: nenhuma campanha com compra, então sem lucro/dia), **omitir só aquele gráfico** e seguir com os demais. Nunca inventar número. `svg=0` total nunca é aceitável.

> Se a análise mudar os valores de tema (cores de `--bg`) ou o nome das classes do esqueleto, este checklist acompanha o `_export-html.md` da análise, que é a fonte única do design.

### 0.1 Montagem do HTML: substituição robusta a `R$`, `%` e `{}` (regra dura)

> **Por que existe (sessão real):** ao montar o HTML com `string % (...)` do Python (o padrão dos snippets de render herdados), a formatação **quebrou**: o texto tem `R$` (que confunde alguns métodos), muitos `%` (margem "80%", "100% das campanhas", `border-radius:50%`) e as `{}` do CSS. Resultado: `TypeError: not enough arguments for format string`. Atrito evitável.

Ao gerar o HTML por script Python (script gravado antes com Write, sem token, lendo só os números do diagnóstico):

- **NÃO usar** `"...html..." % (...)` nem `str.format(...)` no template inteiro: o `%` colide com os `%` literais do texto/CSS, e o `.format` colide com as `{}` do CSS.
- **Usar `string.Template` com `.safe_substitute(...)`** (placeholders `$nome`): ignora `%` e `{}`. O `safe_substitute` ainda tolera o `$` de `R$ ` (trata como inválido e deixa intacto), enquanto substitui os `$nome` válidos. Os pedaços grandes (CSS, SVG dos gráficos, linhas de tabela) entram como **valores** dos placeholders, nunca como parte do template formatável.
- Conferir, depois de gravar, que **não sobrou placeholder** (`grep -oE '\$[a-z_]+' <ARQ>` sem nomes de variável remanescentes) e que os `R$ {valor}` continuam intactos.
- Formatar milhar em pt_BR: `"R$ " + "{:,.0f}".format(v).replace(",",".")` (vira `R$ 1.011`, não `R$ 1011`).
- Gravar em UTF-8 sem BOM. Todo texto visível do painel em português com acentuação correta.

---

## 1. Quando rodar

Após a entrega do diagnóstico narrado + YAML (Parte 1 e 2 da §13 da SKILL), oferecer o export **seguindo a seção 1 do `_export-html.md` da análise** (mesma mecânica de tema):

- **`EXPORT_TEMA` ausente no `.env` (primeira vez):** pergunta numerada com os 3 temas + "Não" (1. Sim, tema Escuro / 2. Sim, tema Terra / 3. Sim, tema Claro Neutro / 4. Não), adaptando o enunciado: "Quer salvar esse diagnóstico como um painel visual (HTML)?". Se 1/2/3: gravar `EXPORT_TEMA` no `.env` (variável não sensível), confirmar em 1 linha e rodar esta sub-skill.
- **`EXPORT_TEMA` já configurado:** "Quer salvar esse diagnóstico como um painel visual (HTML) no tema {Nome}? (s/n)" com a dica de tema pontual ("sim, terra" usa o tema só desta vez, sem alterar o `.env`).

Em ambos os casos, manter o aviso de snapshot:

```
⚠️ Snapshot: o painel é uma "fotografia" dos dados deste momento. Métricas mudam,
   e o arquivo NÃO atualiza sozinho. Tem o horário no topo. Pra dado fresco,
   rode a otimização de novo.
```

Se `n`/`não` ou silêncio: encerrar normalmente. **Nunca rodar sem confirmação explícita.**

Ao aceitar, anunciar: `🔍 Próximo passo: montar o painel de decisão com o mapa das 3 zonas, o lucro por campanha e a confiabilidade do dado. Tempo estimado: cerca de 90 segundos.`

---

## 2. Onde salvar

```
meus-produtos/{ativo}/entregas/trafego/otimizar/painel-decisao-{YYYY-MM-DD-HHMM}.html
```

- `{ativo}`: lido de `meus-produtos/.ativo`. Sem produto ativo, orientar `/produto-novo` antes de salvar.
- Criar a pasta se não existir. **Não sobrescrever**: cada export é arquivo novo com horário próprio (histórico para comparação). `{YYYY-MM-DD-HHMM}` é o horário local da geração.

---

## 3. Layout do painel (de cima pra baixo)

1. **Topbar + banner de snapshot** (esqueleto §3.1 da análise): conta mascarada, janela, escopo, horário.
2. **Premissa carimbada** logo abaixo do banner: `Lucro estimado · margem de contribuição {margem}% · ROAS de break-even {1÷margem}`.
3. **Faixa de KPIs** (`stat-card`): Lucro de contribuição no período · Lucro/dia · ROAS vs break-even · CPA médio vs meta · Confiabilidade do dado · nº de campanhas por zona. **Pelo menos um `stat-card` recebe a classe extra `kpi-lucro`** (exigido no gate).
4. **Seção 1. Mapa das 3 zonas** (`scatter`) + bloco `zona-legenda` (verde/amarela/vermelha explicadas).
5. **Seção 2. Lucro/dia por campanha** (`divbars`) + tabela de duas lentes (Campanha | CPA | vs meta | ROAS | Lucro/dia | Zona | Veredito).
6. **Seção 3. Confiabilidade do dado** (`gauge`) + a conciliação (gasto/compras soma vs total da conta).
7. **Seção 4. Plano de ação** (cards priorizados, em ordem) + handoffs em pills: `/trafego-escalar`, `/trafego-pixel`, `/trafego-publicos`, `/trafego-oferta-funil` (quando o gargalo é fora do Meta) e `/copy-anuncio` (quando o plano pede criativo novo).

Cabeçalhos de tabela em português (mapa da §13.1 da SKILL). Token de cor por zona: verde `--green`, amarela `--yellow`, vermelha `--red`.

---

## 4. Os 3 gráficos obrigatórios (spec + chamada do motor)

Cada gráfico: montar o spec JSON, salvar em `/tmp/spec.json`, chamar o motor, receber a geometria, embrulhar no SVG dentro de um `.chart-card`.

### 4.1 Mapa das 3 zonas (`scatter`)

x = CPA, y = ROAS, raio da bolha proporcional ao gasto (escalar para ~4 a 16), cor pela zona. Linhas de quadrante: vertical no **CPA meta**, horizontal no **ROAS de break-even**.

```json
{
  "viewbox": [720, 360],
  "points": [
    {"x": 771,  "y": 3.64, "r": 12, "color": "#10b981", "label": "Campanha A"},
    {"x": 1606, "y": 1.78, "r": 11, "color": "#f59e0b", "label": "Campanha B"},
    {"x": 2326, "y": 0.93, "r": 8,  "color": "#ef4444", "label": "Campanha C"}
  ],
  "x_mid": 1250, "y_mid": 1.30,
  "x_label": "CPA (R$)", "y_label": "ROAS"
}
```
Cor de cada ponto = zona (calculada na SKILL, não pelo motor): verde se CPA ≤ meta; amarela se meta < CPA ≤ break-even (ROAS ainda ≥ break-even); vermelha se ROAS < break-even. `tipo = scatter`.

### 4.2 Lucro/dia por campanha (`divbars`)

Barras divergentes, ordenadas do maior lucro ao maior prejuízo. Verde pra quem lucra, vermelho pra quem queima.

```json
{
  "viewbox": [720, 280],
  "bars": [
    {"label": "Campanha A", "value": 278, "color": "#10b981"},
    {"label": "Campanha B", "value": 40,  "color": "#f59e0b"},
    {"label": "Campanha C", "value": -27, "color": "#ef4444"}
  ]
}
```
`tipo = divbars`. Desenhar a linha do zero em `zero_y`. Rótulo do valor em reais acima/abaixo da barra.

### 4.3 Confiabilidade do dado (`gauge`)

```json
{
  "viewbox": [320, 200], "value": 2, "max": 3,
  "label": "Confiabilidade", "unit": "",
  "zones": [
    {"upto": 0.34, "color": "#ef4444"},
    {"upto": 0.67, "color": "#f59e0b"},
    {"upto": 1.0,  "color": "#10b981"}
  ]
}
```
`value`: 1=baixa, 2=média, 3=alta (de `confiabilidade_do_dado.nivel`). `tipo = gauge`.

> Embrulho SVG: cada geometria retornada (points/rects/paths/arcs) vai dentro de `<svg viewBox="{viewbox}">` num `<div class="chart-card">`. Linhas de quadrante do scatter como `<line>` tracejada; barras do divbars como `<rect>`; arcos do gauge como `<path>`. Reusar o mesmo padrão de render SVG já usado nos dashboards da `/trafego-analise`.

---

## 5. Honestidade embutida (regras)

- **Snapshot:** banner padrão "fotografia do momento, não atualiza sozinho".
- **Premissa de margem sempre visível** no topo (item 2 do layout). Se `margem_fonte = faixa`, escrever "lucro em faixa (margem 60 a 80%)" e mostrar os lucros como intervalo.
- **Confiabilidade baixa/média:** destacar o aviso e marcar os números de lucro como estimativa frouxa (não cravar).
- **Lucro de contribuição é diferente de lucro líquido da empresa.** Se houver a visão empresa (custo fixo), separar em card próprio, rotulado.
- **Gráfico sem dado:** omitir só aquele, nunca inventar (regra do contrato §0).
- **Token nunca aparece** no HTML (IDs públicos ok; conta sempre mascarada na topbar).

---

## 6. Fechamento (abrir no navegador automaticamente)

Mesma mecânica da `/trafego-analise`: depois do gate (§0) passar, **abrir no navegador automaticamente** com o script cross-platform do projeto. Roda em duas fases.

**FASE 1. Salvar + gate.** Gravar o HTML (UTF-8, sem BOM) e rodar o checklist da §0. **Não abrir o navegador nem anunciar "salvo" enquanto o gate não passar.**

**FASE 2. Abrir no navegador.**
1. Construir o caminho **absoluto** do painel: `{RAIZ_PROJETO}/meus-produtos/{ativo}/entregas/trafego/otimizar/painel-decisao-{horario}.html`.
2. Abrir com o script (tanto o caminho do script quanto o do HTML precisam ser **absolutos**: não confiar no `cwd`, que pode estar contaminado por um `cd` anterior):
   ```bash
   {PY} "{RAIZ_PROJETO}/scripts/abrir-html.py" "{caminho-absoluto-do-painel}"
   ```
   Fallback, se o script falhar: `start "" "..."` (Windows), `open "..."` (Mac), `xdg-open "..."` (Linux).
3. Devolver ao aluno a mensagem abaixo, **sempre com o caminho absoluto no chat** (texto copiável), mesmo que o navegador abra, porque o sistema pode bloquear a abertura:
   ```
   ✅ Concluído: painel de decisão salvo. Caminho: meus-produtos/{ativo}/entregas/trafego/otimizar/painel-decisao-{horario}.html
   🌐 Abrindo no navegador...

   Caso o navegador não abra sozinho, copie o caminho e abra manualmente:
   {caminho-absoluto-do-painel}

   ⚠️ É um snapshot (fotografia do momento): não atualiza sozinho.
   Para acompanhar a conta ao vivo, use o /trafego-dashboard.
   ```

Não ecoar o HTML no chat.
