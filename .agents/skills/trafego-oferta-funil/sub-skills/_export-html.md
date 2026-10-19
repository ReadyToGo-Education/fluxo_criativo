# Sub-skill utilitária. Export HTML de Oferta e Funil

Acionada opcionalmente ao final de cada módulo da `/trafego-oferta-funil`, quando o aluno responde "sim" à pergunta de export (tema conforme a seção 15 do SKILL.md).

## Contrato de export

Reutilizar o design system de `.claude/skills/trafego-analise/sub-skills/_export-html.md` (só leitura: esta sub-skill não edita aquele arquivo), incluindo os **3 temas oficiais** (Escuro, Terra, Claro Neutro): a escolha do tema segue a seção 1 daquele arquivo (pergunta com opções na primeira vez, depois `EXPORT_TEMA` do `.env`), e as cores de SVG seguem a tabela CORES_GRAFICO (seção 3.2.c). Explicação obrigatória em cada gráfico (`.chart-explain`). Rodar o checklist de conformidade da seção 0 daquele arquivo antes de entregar (svg, chart-card, chart-explain, topbar, tema e fundo maiores que zero; se algum der zero, refazer).

Geometria via `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py` (sem token, em qualquer modo), spec passado por arquivo, com o interpretador detectado na sessão (`python3` ou `py -3`):

```bash
python3 .claude/skills/trafego-analise/scripts/trafego_chart_geom.py <tipo> < /tmp/spec.json
```

O formato do spec de cada tipo está na seção 3.2.1.2 do `_export-html.md` da análise (barras usam a chave `bars`; o funil duplo usa `a` e `b`).

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
- O checkout usa o benchmark POR FAIXA, nunca um fixo de 30%, e exibe a ressalva da Hotmart.
- O funil pós-clique inclui a visita à página e o checkout iniciado sempre que estiverem disponíveis (modo App, campos descobertos no MCP com `ads_get_field_context` ou números da leitura guiada no Gerenciador). Se faltarem, o HTML mostra a lacuna e diz por quê.
- Quando houver upsell/downsell (Passo 0.97 do SKILL.md), incluir o take rate estimado (seção 4.5).
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
python3 "{RAIZ_PROJETO}/scripts/abrir-html.py" "{RAIZ_PROJETO}/meus-produtos/{ativo}/entregas/trafego/oferta-funil/{arquivo}.html"
```

Trocar `python3` por `py -3` se esse for o interpretador da sessão. O script funciona em Windows, Mac e Linux e, se não conseguir abrir, imprime a instrução de abertura manual. Em qualquer caso, devolver o caminho absoluto no chat:

```
✅ Concluído: diagnóstico de oferta e funil exportado. Caminho: {raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\oferta-funil\{arquivo}.html
```
