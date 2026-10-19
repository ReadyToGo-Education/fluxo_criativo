# Sub-skill utilitária. Export HTML de Inteligência Criativa

Sub-skill compartilhada pelos 6 módulos da `/trafego-criativos`. Acionada opcionalmente ao final de cada módulo, quando o aluno responde "sim" à pergunta de export (tema conforme a seção 15 do SKILL.md).

---

## 0. Contrato de export (regra dura)

**É PROIBIDO inventar HTML novo.** Sempre partir do esqueleto e dos tokens do design system oficial em `.claude/skills/trafego-analise/sub-skills/_export-html.md` (só leitura: esta sub-skill não edita aquele arquivo). O design system tem **3 temas oficiais** (Escuro, Terra, Claro Neutro); a escolha do tema segue a seção 1 do `_export-html.md` da análise (pergunta com opções na primeira vez, depois `EXPORT_TEMA` do `.env`). Nunca criar paleta própria fora dos 3 temas. Cores de SVG conforme a tabela CORES_GRAFICO (seção 3.2.c de lá).

**É OBRIGATÓRIO renderizar os gráficos** declarados por módulo abaixo. Geometria via `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py` (sem token, em qualquer modo), com o spec passado por arquivo e o interpretador detectado na sessão (`python3` ou `py -3`):

```bash
python3 .claude/skills/trafego-analise/scripts/trafego_chart_geom.py <tipo> < /tmp/spec.json
```

O formato do spec de cada tipo (`line`, `vbars`, `gauge`, `scatter`, `radar`, `divbars`) está na seção 3.2.1.2 do `_export-html.md` da análise. As barras usam a chave `bars` (lista de `{label, value, color}`).

**É OBRIGATÓRIO registrar no INDEX** depois de salvar: adicionar a linha em `meus-produtos/{ativo}/entregas/trafego/criativos/INDEX.md` com data, módulo, conta, produto, urgência e link para o arquivo (formato na seção 14 do SKILL.md).

**É OBRIGATÓRIO incluir texto explicativo** (`<div class="chart-explain">`) em cada gráfico, com "O que é", "Como ler" e "O que fazer". Gráfico sem explicação é proibido.

**Checklist de conformidade:**

```bash
echo -n "svg="       ; grep -c "<svg"          <ARQ>
echo -n "chart-card="; grep -c "chart-card"    <ARQ>
echo -n "explain="   ; grep -c "chart-explain" <ARQ>
echo -n "topbar="    ; grep -c 'class="topbar' <ARQ>
echo -n "tema="      ; grep -cE 'data-theme="(escuro|terra|claro)"' <ARQ>
echo -n "bgok="      ; grep -cE -- "--bg:(#000|#D8DDC8|#f4f6f8)" <ARQ>
```

Regra de bloqueio: se `svg=0`, `chart-card=0`, `explain=0`, `topbar=0`, `tema=0` ou `bgok=0`, o export está errado. Refazer antes de mostrar ao aluno.

---

## 1. Gráficos obrigatórios por módulo

### Leitura de Atenção
- **Curva de retenção por criativo:** `line` com uma série por criativo de vídeo (até 5, os de maior gasto), eixo X = Impressões, p25, p50, p75, p95 (via `x_labels`) e eixo Y = % do público que ainda assiste. A queda fica visível na inclinação. Geometria: `trafego_chart_geom.py line`.
- **Gauge de Cost per Hook:** arco semicircular, menor é melhor (zonas invertidas: verde no começo do arco). Geometria: `trafego_chart_geom.py gauge`.

### Intenção Criativa
- **Scatter de qualidade de intenção:** eixo X = CTR, eixo Y = Click-to-LPV Rate, linhas de quadrante no benchmark de CTR da conta e em 70% de visita. Quadrante superior direito = visita qualificada. Inferior direito = curiosidade vazia. Geometria: `trafego_chart_geom.py scatter`.

### Conversão Criativa
- **Barras cold vs warm:** para cada criativo, duas barras lado a lado com o CPA em cold e o CPA em warm (cores diferentes por temperatura). Geometria: `trafego_chart_geom.py vbars`.
- **Ranking por formato (obrigatório):** além do comparativo agregado vídeo, imagem e carrossel, renderizar **três tabelas separadas** lado a lado (`.card-grid-3`, ou empilhadas no celular): Top vídeos, Top imagens/cards, Top carrosséis. Cada uma ordenada por ROAS (depois CPA), com a coluna de vendas e ⚠️ em todo item com menos de 4 vendas. Nunca um ranking único misturando formatos (seções 5.1 e 5.2 do SKILL.md). Cada tabela com seu `chart-explain`.

### Diagnóstico Criativo
- **Mapa de diagnóstico:** tabela visual com 4 colunas (Atenção, Intenção, Conversão, Consistência) e uma linha por criativo. Cada célula verde (OK), amarela (zona cinza) ou vermelha (FAIL). HTML puro + 1 SVG `gauge` com a confiança geral.

### DNA Criativo
- **Radar de perfis:** um `radar` por perfil comportamental (uma chamada por perfil), com 5 eixos (Hook Rate, Hold Rate, CTR, CPA invertido, Consistência) normalizados de 0 a 100. Geometria: `trafego_chart_geom.py radar`.
- **Tipos da Mandala × perfil:** tabela HTML com tipo, quantidade, % do gasto, perfil dominante, CPA médio e temperatura em que vence, mais um `vbars` com o % do gasto por tipo.

### Briefing Criativo
- **Barras de prioridade:** barras verticais ordenadas pelo impacto potencial (gasto desperdiçado por dia). Geometria: `trafego_chart_geom.py vbars`.

### Inteligência Completa
- Todos os gráficos acima + sumário executivo no topo com urgência criativa e selo.

---

## 2. Onde salva

```
meus-produtos/{ativo}/entregas/trafego/criativos/{slug-do-modulo}-{YYYY-MM-DD-HHMM}.html
```

Criar a pasta se não existir. `{ativo}` vem de `meus-produtos/.ativo`.

| Módulo | Slug |
|--------|------|
| Inteligência completa | `completa` |
| Leitura de atenção | `atencao` |
| Intenção criativa | `intencao` |
| Conversão criativa | `conversao` |
| Diagnóstico criativo | `diagnostico` |
| DNA criativo | `dna` |
| Briefing criativo | `briefing` |

---

## 3. Abrir no navegador

Abrir sempre depois de salvar, com o script `scripts/abrir-html.py` da raiz do projeto. Caminhos **absolutos** do script e do HTML (o diretório atual do shell pode ter mudado com um `cd` anterior):

```bash
python3 "{RAIZ_PROJETO}/scripts/abrir-html.py" "{RAIZ_PROJETO}/meus-produtos/{ativo}/entregas/trafego/criativos/{arquivo}.html"
```

Trocar `python3` por `py -3` se esse for o interpretador da sessão. Em qualquer caso, devolver o caminho absoluto no chat como texto copiável:

```
✅ Concluído: análise criativa exportada. Caminho: {raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\criativos\{arquivo}.html
```

---

## 4. Estrutura do HTML

1. **Topbar** com título, data e hora, conta e produto.
2. **Snap-warn** com selo de urgência criativa.
3. **Seções** com as 7 seções do relatório humano.
4. **Gráficos** com `.chart-card` + SVG + `.chart-explain` obrigatório.
5. **Rodapé** com data e hora, skill e o aviso de nível de análise ("Análise baseada em métricas comportamentais; conclusões sobre gancho e narrativa são hipóteses").

**Dados sensíveis:** aplicar a seção 6 do `_export-html.md` da análise (IDs mascarados, nunca token).
