# Sub-skill utilitária. Export HTML de Oferta e Funil

Acionada opcionalmente ao final de cada módulo da `/trafego-oferta-funil`, quando o aluno responde "sim" à pergunta de export (tema conforme a seção 15 do SKILL.md).

## Contrato de export

Reutilizar o design system de `.claude/skills/trafego-analise/sub-skills/_export-html.md` (só leitura: esta sub-skill não edita aquele arquivo), incluindo os **3 temas oficiais** (Escuro, Terra, Claro Neutro): a escolha do tema segue a seção 1 daquele arquivo (pergunta com opções na primeira vez, depois `EXPORT_TEMA` do `.env`), e as cores de SVG seguem a tabela CORES_GRAFICO (seção 3.2.c). Explicação obrigatória em cada gráfico (`<div class="chart-explain">` com "O que é", "Como ler" e "O que fazer").

**Checklist de conformidade (rodar antes de entregar; substituir `<ARQ>` pelo caminho do HTML):**

```bash
echo -n "svg="       ; grep -c "<svg"          <ARQ>
echo -n "chart-card="; grep -c "chart-card"    <ARQ>
echo -n "explain="   ; grep -c "chart-explain" <ARQ>
echo -n "topbar="    ; grep -c 'class="topbar' <ARQ>
echo -n "tema="      ; grep -cE 'data-theme="(escuro|terra|claro)"' <ARQ>
echo -n "bgok="      ; grep -cE -- "--bg:(#000|#D8DDC8|#f4f6f8)" <ARQ>
```

Regra de bloqueio: se `svg=0`, `chart-card=0`, `explain=0`, `topbar=0`, `tema=0` ou `bgok=0`, o export está errado. Refazer antes de mostrar ao aluno.

Exceções:
- No export só do módulo Leitura da página (slug `pagina`), que é um checklist em tabela HTML sem gráfico SVG, `svg` e `chart-card` podem dar zero. `explain` (a explicação do checklist, com "O que é", "Como ler" e "O que fazer"), `topbar`, `tema` e `bgok` continuam obrigatórios.
- Gráfico cujo dado não veio (ex.: funil sem a visita à página) é omitido só ele, sem inventar número, e o HTML mostra a lacuna e diz por quê (mesma exceção da seção 0 do `_export-html.md` da análise). Nos outros módulos, `svg=0` no total continua inaceitável.

Geometria via `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py` (sem token, em qualquer modo), com o interpretador detectado na sessão (`{PY}` = `python3` ou `py -3`). O spec vai por arquivo, sempre em caminho **absoluto** dentro da pasta de dados de trabalho do produto, porque `/tmp` aponta para pastas diferentes no Windows conforme a ferramenta (o Write e o Bash não enxergam o mesmo arquivo):

1. Gravar o spec com o Write em `{RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/tmp/spec-{grafico}.json` (um nome por gráfico, ex.: `spec-oferta-gauge.json`; criar a pasta se não existir).
2. Chamar o motor pelo Bash, com caminhos absolutos do script e do spec (o diretório atual pode ter mudado com um `cd` anterior):

```bash
{PY} "{RAIZ_PROJETO}/.claude/skills/trafego-analise/scripts/trafego_chart_geom.py" <tipo> < "{RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/tmp/spec-{grafico}.json"
```

3. Apagar os specs ao final do export.

Alternativa sem arquivo intermediário: quando o HTML é montado por um script Python, importar o motor com caminho absoluto (`sys.path.insert(0, "{RAIZ_PROJETO}/.claude/skills/trafego-analise/scripts")`, depois `import trafego_chart_geom as G` e `G.geom_vbars(spec)` etc.).

O formato do spec de cada tipo e o nome das funções no import estão na seção 3.2.1.2 do `_export-html.md` da análise (barras usam a chave `bars`; o funil duplo usa `a` e `b`).

Depois de salvar, registrar a linha no `meus-produtos/{ativo}/entregas/trafego/oferta-funil/INDEX.md` (formato na seção 14 do SKILL.md).

## Gráficos por módulo

| Módulo | Gráfico |
|--------|---------|
| Leitura pós-clique | Funil duplo: período atual (`a`) ao lado do anterior (`b`), etapa por etapa, com a etapa de quebra destacada em vermelho. `trafego_chart_geom.py dual_funnel` |
| Leitura da página | Checklist visual (tabela HTML com os elementos e a avaliação por cor) |
| Congruência | Barras com a nota de cada dimensão (promessa, tom, especificidade, CTA, público). `trafego_chart_geom.py vbars` |
| Diagnóstico de oferta | Gauge da nota de 0 a 100 + barras por elemento do checklist. `trafego_chart_geom.py gauge` + `vbars` |
| Diagnóstico de checkout | Barras de checkout iniciado e compra, com a taxa e a faixa do ticket. `trafego_chart_geom.py vbars` |
| Plano de correção | Barras de prioridade por impacto (R$/dia). `trafego_chart_geom.py vbars` |
| Completo | Todos acima + sumário executivo com urgência |

**Obrigatório em todo export (sincronizado com as seções 3.5 e 12 do SKILL.md):**
- O gráfico de notas da oferta vem SEMPRE com a tabela `Elemento | Nota | Por que essa nota` logo abaixo (seção 12), fechando com o lembrete de que a nota é leitura estrutural cruzada com os números e que a auditoria completa de copy é do `/feedback-pagina`.
- Funil e taxas vêm com a coluna de benchmark da faixa de ticket do aluno, com etiqueta de confiança (seção 3.5).
- O checkout usa o benchmark POR FAIXA, nunca um fixo de 30%, e exibe a ressalva da Hotmart e da Kiwify.
- O funil pós-clique inclui a visita à página e o checkout iniciado sempre que estiverem disponíveis (modo App, campos conferidos do conector `landing_page_view` e `omni_initiated_checkout`, ou números da leitura guiada no Gerenciador; seção 3 do SKILL.md). Se faltarem, o HTML mostra a lacuna e diz por quê.
- Quando houver upsell/downsell (Passo 0.97 do SKILL.md), incluir o take rate (quando o upsell tem evento próprio) ou o aviso de que ele só sai do relatório da Hotmart ou da Kiwify (seção 4.5).
- Cada correção recomendada aparece com a skill que a executa (`/feedback-pagina`, `/feedback-low-ticket`, `/pagina-ajuste`, `/pagina-performance`, `/pagina-checkout`, `/copy-pagina`, `/lt-pagina`).

**Dados sensíveis:** aplicar a seção 6 do `_export-html.md` da análise (IDs mascarados, nunca token).

## Onde salva

```
meus-produtos/{ativo}/entregas/trafego/oferta-funil/{slug}-{YYYY-MM-DD-HHMM}.html
```

Criar a pasta se não existir. Slugs: `completo`, `pos-clique`, `pagina`, `congruencia`, `oferta`, `checkout`, `plano-correcao`.

## Abrir no navegador

Abrir SEMPRE no navegador do sistema depois de salvar (o painel de prévia do aplicativo não abre o navegador sozinho). Usar o script `scripts/abrir-html.py` da raiz do projeto, com caminhos **absolutos** do script e do HTML:

```bash
{PY} "{RAIZ_PROJETO}/scripts/abrir-html.py" "{RAIZ_PROJETO}/meus-produtos/{ativo}/entregas/trafego/oferta-funil/{arquivo}.html"
```

`{PY}` é o interpretador da sessão (`python3` ou `py -3`). O script funciona em Windows, Mac e Linux e, se não conseguir abrir, imprime a instrução de abertura manual. Em qualquer caso, devolver o caminho absoluto no chat:

```
✅ Concluído: diagnóstico de oferta e funil exportado. Caminho: {raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\oferta-funil\{arquivo}.html
```
