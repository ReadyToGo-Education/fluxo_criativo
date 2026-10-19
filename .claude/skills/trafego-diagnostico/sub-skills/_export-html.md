# Sub-skill utilitária. Export HTML de Diagnóstico

Sub-skill compartilhada pelos 4 módulos da `/trafego-diagnostico`. Não tem opção própria no menu. Acionada opcionalmente ao final de cada módulo, quando o aluno responde "sim" à pergunta de export (mecânica de tema na seção 14 do SKILL.md).

**Propósito:** transformar o diagnóstico em HTML standalone usando o design system da `/trafego-analise`, salvar em `meus-produtos/{ativo}/entregas/trafego/diagnostico/` e abrir no navegador.

---

## 0. Contrato de export (regra dura)

**É PROIBIDO inventar um HTML novo.** O export SEMPRE parte do esqueleto e dos tokens do design system oficial em `.claude/skills/trafego-analise/sub-skills/_export-html.md` (só leitura: esta sub-skill não edita aquele arquivo). O design system tem **3 temas oficiais** (Escuro, Terra, Claro Neutro); a escolha do tema segue a seção 1 do `_export-html.md` da análise (pergunta com opções na primeira vez, depois `EXPORT_TEMA` do `.env`). Nunca criar paleta própria fora dos 3 temas, nunca trocar `--accent` por outra cor, nunca substituir `.topbar`/`.snap-warn` por faixa improvisada. Cores de SVG conforme a tabela CORES_GRAFICO (seção 3.2.c de lá).

**É OBRIGATÓRIO renderizar os gráficos** que cada módulo declara em "Gráficos obrigatórios" abaixo. A geometria vem de `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py` (roda em qualquer modo, não toca a API, não usa token). Usar sempre caminhos absolutos: `{RAIZ_PROJETO}` = caminho absoluto da raiz do projeto (não confiar no diretório atual, que pode ter mudado com um `cd` anterior) e `{PY}` = interpretador detectado na sessão (`python3` ou `py -3`).

Passar o spec por arquivo: gravar com a ferramenta Write em `{RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/tmp/spec-{tipo}.json` e chamar o motor pelo Bash, um gráfico por vez (gravar, rodar e só então gravar o próximo). Não usar `/tmp`: no Windows, a ferramenta Write e o Bash resolvem `/tmp` para pastas diferentes, e o motor leria um arquivo inexistente ou um spec antigo.

```bash
{PY} "{RAIZ_PROJETO}/.claude/skills/trafego-analise/scripts/trafego_chart_geom.py" <tipo> < "{RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/tmp/spec-{tipo}.json"
```

Apagar os arquivos `spec-*.json` dessa pasta ao final do export.

Formato dos specs usados aqui (detalhes na seção 3.2.1.2 do `_export-html.md` da análise):
- `vbars`: `{"bars": [{"label": "...", "value": 65, "color": "#..."}]}`
- `gauge`: `{"value": 62, "max": 100, "label": "...", "unit": "", "zones": [{"upto": 0.25, "color": "#..."}, ...]}`
- `scatter`: `{"points": [{"x": 20, "y": 0.4, "label": "...", "color": "#..."}], "x_label": "...", "y_label": "..."}`

**Checklist de conformidade (rodar ANTES de declarar o HTML pronto):**

```bash
echo -n "svg="       ; grep -c "<svg"          <ARQ>
echo -n "chart-card="; grep -c "chart-card"    <ARQ>
echo -n "explain="   ; grep -c "chart-explain" <ARQ>
echo -n "topbar="    ; grep -c 'class="topbar' <ARQ>
echo -n "snap-warn=" ; grep -c "snap-warn"     <ARQ>
echo -n "tema="      ; grep -cE 'data-theme="(escuro|terra|claro)"' <ARQ>
echo -n "bgok="      ; grep -cE -- "--bg:(#000|#D8DDC8|#f4f6f8)" <ARQ>
```

**Regra de bloqueio:** se `svg=0`, `chart-card=0`, `explain=0`, `topbar=0`, `tema=0` ou `bgok=0`, o export está ERRADO. **Não entregar.** Refazer a partir do esqueleto oficial antes de mostrar ao aluno.

**Exceção snap-warn:** quando a urgência é `monitorar` ou `baixa`, o snap-warn pode conter apenas o selo de urgência (sem mensagem de alerta). O checklist aceita `snap-warn` de 1 para cima (o selo conta).

---

## 1. Gráficos obrigatórios por módulo

### Diagnóstico Diferencial

- **Barras verticais de probabilidade:** 3 barras (uma por hipótese), altura proporcional ao peso percentual, rótulo com o nome da categoria e o %.
- Geometria: `trafego_chart_geom.py vbars` (spec com `bars: [{label, value, color}]`).

### Auditoria Estrutural

- **Gauge de score de saúde (0 a 100):** arco semicircular, ponteiro no score, zonas: verde (80+), amarelo (60 a 79), laranja (40 a 59), vermelho (0 a 39).
- **Mapa de fragmentação:** scatter com um ponto por conjunto ativo, eixo X = orçamento diário, eixo Y = conversões por dia, cor pela faixa de densidade (verde 7 ou mais, amarelo 1 a 6, vermelho abaixo de 1).
- Geometria: `trafego_chart_geom.py gauge` e `trafego_chart_geom.py scatter`.

### Falso Vencedor

- **Tabela colorida:** uma linha por entidade avaliada, colunas: nome, classificação, score de confiança, ROAS, conversões, frequência, risco. Cor de fundo pela classificação: verde (`vencedor_real`), amarelo (`vencedor_promissor`), vermelho (`falso_vencedor_provavel`), cinza (`inconclusivo`). Tabela HTML pura. As entidades em `nao_candidatas` (CPA acima de 1,2 vez a meta) ficam fora da tabela, listadas abaixo dela com o motivo.
- **Barras de confiança por entidade:** uma barra vertical por entidade com o score de 0 a 100 (necessária também para passar no checklist de SVG).
- Geometria: `trafego_chart_geom.py vbars`.

### Score de Confiança

- **Gauge de confiança:** arco semicircular com o score geral da conta, ponteiro, zonas por faixa (verde 75+, amarelo 50 a 74, laranja 25 a 49, vermelho 0 a 24).
- **Barras de variáveis:** 10 barras verticais (uma por variável do score), altura proporcional à pontuação (0 a 10), rótulo com o nome e o valor.
- Geometria: `trafego_chart_geom.py gauge` e `trafego_chart_geom.py vbars`.

### Diagnóstico Completo

Todos os gráficos acima + seção de sumário executivo no topo com:
- Selo de urgência (cor por nível: vermelho, laranja, amarelo, verde, cinza).
- Bloco de proteção de caixa (R$/dia, projeção mensal).
- Score geral de confiança (gauge).

---

## 2. Onde salva

```
meus-produtos/{ativo}/entregas/trafego/diagnostico/{slug-do-modulo}-{YYYY-MM-DD-HHMM}.html
```

Criar a pasta se não existir. `{ativo}` vem de `meus-produtos/.ativo`.

| Módulo | Slug |
|--------|------|
| Diagnóstico completo | `completo` |
| Diagnóstico diferencial | `diferencial` |
| Auditoria estrutural | `auditoria-estrutural` |
| Falso vencedor | `falso-vencedor` |
| Score de confiança | `score-confianca` |

Exemplos:
- `meus-produtos/curso-tarot/entregas/trafego/diagnostico/completo-2026-06-02-1430.html`
- `meus-produtos/curso-tarot/entregas/trafego/diagnostico/falso-vencedor-2026-06-02-1430.html`

Depois de salvar, registrar a linha no `meus-produtos/{ativo}/entregas/trafego/diagnostico/INDEX.md` (formato na seção 13 do SKILL.md).

---

## 3. Abrir no navegador

Depois de salvar, abrir automaticamente com o script `scripts/abrir-html.py` da raiz do projeto (o mesmo da `/trafego-analise`). Caminho do script e do HTML **sempre absolutos** (o diretório atual do shell pode ter mudado com um `cd` anterior):

```bash
{PY} "{RAIZ_PROJETO}/scripts/abrir-html.py" "{RAIZ_PROJETO}/meus-produtos/{ativo}/entregas/trafego/diagnostico/{arquivo}.html"
```

`{PY}` é o interpretador da sessão (`python3` ou `py -3`). Se o script não conseguir abrir, ele mesmo imprime a instrução de abertura manual. Em qualquer caso, devolver no chat o caminho absoluto como texto copiável:

```
✅ Concluído: diagnóstico exportado. Caminho: {raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\diagnostico\{arquivo}.html
```

---

## 4. Regra de explicação obrigatória nos gráficos (regra dura)

**Todo gráfico no HTML DEVE ter texto explicativo imediatamente abaixo.** Gráfico sem explicação é proibido. O aluno que abre o HTML precisa entender cada número e gráfico sem voltar ao chat.

**Formato obrigatório por gráfico:**

```html
<div class="chart-card">
  <!-- SVG do gráfico -->
  <svg>...</svg>
  <!-- Explicação obrigatória -->
  <div class="chart-explain">
    <p class="chart-what"><strong>O que é:</strong> {explicação do que o gráfico mostra}</p>
    <p class="chart-read"><strong>Como ler:</strong> {como interpretar os valores}</p>
    <p class="chart-action"><strong>O que fazer:</strong> {ação recomendada com base no que o gráfico mostra}</p>
  </div>
</div>
```

**Exemplos por gráfico:**

| Gráfico | "O que é" | "Como ler" | "O que fazer" |
|---------|-----------|------------|---------------|
| Gauge confiança 62 | "Score de confiança dos seus dados: quanto mais alto, mais seguro é decidir com base neles." | "62 é confiança média. Ajustes de curto prazo podem ser feitos. Escalar só se a entidade também sair como vencedor real, e de forma gradual. Pausar a campanha inteira pede mais dados." | "Para chegar a 75 ou mais: acumular mais 8 conversões e manter as campanhas rodando por mais 3 dias." |
| Gauge saúde 38 | "Saúde da estrutura da conta: mede se a organização das campanhas está ajudando ou atrapalhando o algoritmo do Meta." | "38 é estrutura sabotando o algoritmo. Seus resultados podem estar sendo prejudicados pela forma como a conta está organizada, não pelos criativos." | "Prioridade: consolidar conjuntos fragmentados (22 dos 34 têm menos de 1 conversão por dia). Depois: subir criativos novos nas 4 campanhas sem renovação." |
| Barras hipóteses 65/20/15 | "Probabilidade de cada causa para o problema detectado. Funciona como diagnóstico médico: mais de uma causa é possível." | "65% de fadiga criativa significa que essa é a explicação mais provável, mas não certeza. 20% de saturação de público é uma possibilidade secundária." | "Testar a hipótese principal: subir 2 criativos novos. Se o CTR melhorar em 72h, era fadiga. Se não, investigar a segunda hipótese." |
| Tabela falso vencedor | "Avaliação de cada campanha: verifica se os resultados que parecem bons são reais ou podem estar enganando." | "Verde = vencedor real (pode confiar). Amarelo = promissor (esperar mais dados). Vermelho = falso vencedor (cuidado). Cinza = inconclusivo." | "Campanhas em vermelho: NÃO escalar. Rodar teste em prospecção pura antes." |

**Checklist adicional:** além de `svg` e `chart-card` maiores que zero, conferir `chart-explain` maior que zero. Se algum gráfico não tiver explicação, o export está incompleto.

---

## 5. Estrutura do HTML

Manter a mesma estrutura do design system da `/trafego-analise`:

1. **Topbar** com título do módulo, data e hora, conta de anúncios e produto.
2. **Snap-warn** com selo de urgência e proteção de caixa (quando aplicável).
3. **Seções** correspondendo às 7 seções do relatório humano.
4. **Gráficos** intercalados nas seções relevantes (chart-cards com SVG + `.chart-explain` obrigatório).
5. **Rodapé** com data e hora, skill que gerou e o aviso de atribuição ("ROAS atribuído pela Meta, não é lucro real").

**Regra de conteúdo:** o HTML reproduz o relatório humano integralmente. Não é resumo. É a versão visual completa do diagnóstico, incluindo "o que os dados NÃO dizem" e "o que NÃO fazer". Cada número e gráfico deve se explicar sozinho para quem abre o HTML sem ter visto o chat.

**Dados sensíveis:** aplicar a seção 6 do `_export-html.md` da análise antes de montar o HTML (conta de anúncios com os dígitos do meio ocultos, IDs de campanha, conjunto e anúncio só com os 4 últimos dígitos e o nome ao lado, e nunca token, app_id ou business_id).
