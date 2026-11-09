# Sub-skill. Score de Confiança por Decisão

Calcula score numérico (0 a 100) de confiança para cada decisão ou conclusão do diagnóstico. Diferente do Passo 0.8 da `/trafego-otimizar` (que valida a fonte de dados como um todo), este módulo avalia **cada recomendação individual**: "pausar o conjunto X tem confiança 72, escalar a campanha Y tem confiança 45".

## Contexto multi-produto

Quando a conta tem mais de 1 produto declarado (Passo 0.6 do SKILL.md), o score é calculado **por produto** (cada grupo de campanhas mapeado a um produto no Passo 0.75). Motivo: um produto com R$ 5.000 de gasto e 30 conversões tem confiança alta, enquanto outro com R$ 200 e 2 conversões no mesmo período tem confiança baixa. Misturar infla o score do fraco e dilui o do forte.

O score geral da conta é a **média ponderada por gasto** dos scores (por produto, quando houver mais de um; por campanha ativa com gasto > 0, quando houver um só). Quem investe mais pesa mais.

No output, cada produto ganha seu bloco de score, seguido do score geral:

```yaml
score_por_produto:
  - produto: "Produto A"
    score: 72
    faixa: media_confianca
  - produto: "Produto B"
    score: 38
    faixa: baixa_confianca
score_geral_conta:
  score: 61
  faixa: media_confianca
  metodo: media_ponderada_por_gasto
```

---

## Quando é acionado

- Opção [5] do menu principal.
- Automaticamente no Diagnóstico Completo (primeiro módulo da sequência).
- Quando o aluno pergunta "posso confiar nesse resultado?".
- Como base para os outros 3 módulos (todos consomem o score).
- Como freio antes de `/trafego-escalar` (seção 12 do SKILL.md).

## Dados necessários

Pedir à `/trafego-insights`:
- `escopo: conta_completa`, `nivel: campaign + adset + ad` (o nível `ad` é o que dá o gasto por anúncio da variável 7).
- 3 janelas da trilha.
- `incluir_serie_diaria: true` para as métricas-norte (CPA ou CPL) de cada campanha e conjunto com gasto > 0 (de onde sai o CV).

**Variável 7 (concentração):** gasto do anúncio que mais gasta dividido pelo gasto da entidade (campanha ou conjunto), no mesmo período das outras variáveis. Para uma entidade de nível anúncio, a variável não se aplica: passar `null` (conta 0 ponto, aparece em `variaveis_indisponiveis` e o script não sugere diversificar criativos) e dizer no relatório que, para anúncio, o score vai no máximo até 90.

Complementar (leitura pura, por modo, conforme a seção 3.1 do SKILL.md):
- Fase de aprendizado dos conjuntos (`learning_stage_info`; no MCP, só se `ads_get_field_context` listar o campo, senão "aprendizado não verificado"). O `effective_status` não informa a fase de aprendizado.
- Segmentação dos conjuntos, para a variável 8 (remarketing vs prospecção), com a regra de inclusão, exclusão e semelhante da seção 3.1 do SKILL.md.
- Pixel e CAPI, para a variável 9 (qualidade da atribuição).

## As 10 variáveis do score

Cada variável contribui de 0 a 10 pontos para o score total (máximo 100):

| # | Variável | Chave JSON | 0 pontos (péssimo) | 5 pontos (médio) | 10 pontos (ótimo) |
|---|----------|-----------|---------------------|-------------------|-------------------|
| 1 | **Volume de gasto** | `gasto` | < R$ 50 | R$ 50 a 500 | > R$ 500 |
| 2 | **Número de conversões** | `conversoes` | 0 a 2 | 3 a 15 | > 15 |
| 3 | **Dias analisados** | `dias` | 1 a 2 dias | 3 a 6 dias | 7 dias ou mais |
| 4 | **Consistência entre dias** | `cv_metrica_norte` | CV > 0,60 (caótico) | CV 0,30 a 0,60 | CV < 0,30 (estável) |
| 5 | **Variação vs período anterior** | `variacao_periodo_pct` | > 40% de variação | 20% a 40% | < 20% |
| 6 | **Frequência** | `frequencia` | > 4,0 (saturado) | 2,0 a 4,0 | < 2,0 |
| 7 | **Concentração no anúncio que mais gasta** | `pct_gasto_top1_anuncio` | mais de 80% do gasto | 40% a 80% | < 40% (distribuído) |
| 8 | **Dependência de remarketing** | `pct_remarketing` | mais de 70% do resultado é remarketing | 40% a 70% | < 40% (prospecção dominante) |
| 9 | **Qualidade da atribuição** | `qualidade_atribuicao` | `sem_pixel` | `pixel_ativo` | `pixel_capi` |
| 10 | **Distância da meta** | `cpa_sobre_target` | > 2x a meta | 1,3x a 2x | até 1,3x |

**Valores aceitos em `qualidade_atribuicao`:** `pixel_capi` (10, pixel ativo com API de Conversões confirmada), `pixel_ativo` (5, pixel ativo, CAPI não verificada), `pixel_sem_capi` (3, pixel ativo e CAPI confirmadamente ausente ou com deduplicação muito baixa), `janela_desconhecida` (2, não foi possível ler a janela de atribuição) e `sem_pixel` (0).

**Percentuais entram como fração:** `variacao_periodo_pct: 0.18` significa 18%. O mesmo vale para `pct_gasto_top1_anuncio` e `pct_remarketing`. O script também aceita texto como `"18%"` e valores em reais como `"R$ 1.000"` ou `"R$ 1.234,56"`, e converte.

**Regra para variáveis ausentes:** se uma variável não estiver disponível (valor `null` ou chave ausente), recebe **0 ponto** e é listada em `variaveis_indisponiveis`. Dado faltante reduz a confiança, nunca a infla. Exemplo comum no modo MCP: sem leitura de segmentação, `pct_remarketing` fica `null`.

**CV** = coeficiente de variação, obtido da `serie_diaria` da `/trafego-insights` (campo `{metrica}_cv`).

## Cálculo do score

O score é calculado pelo script `calcular_score_confianca.py` para garantir precisão aritmética. O script só faz conta: não chama a Graph API, não lê o `.env` e não usa token. O Claude passa as 10 variáveis como JSON e recebe o score com o detalhamento.

Rodar com o interpretador detectado na sessão (`{PY}` = `python3` ou `py -3`, conforme a seção "Execução de Scripts Python" do CLAUDE.md) e o script por caminho absoluto (`{RAIZ_PROJETO}` = caminho absoluto da raiz do projeto; não confiar no diretório atual, que pode ter mudado com um `cd` anterior):

```bash
echo '{"gasto": 350, "conversoes": 8, "dias": 7, "cv_metrica_norte": 0.42, "variacao_periodo_pct": 0.18, "frequencia": 2.1, "pct_gasto_top1_anuncio": 0.55, "pct_remarketing": 0.25, "qualidade_atribuicao": "pixel_ativo", "cpa_sobre_target": 1.15}' | {PY} "{RAIZ_PROJETO}/.claude/skills/trafego-diagnostico/scripts/calcular_score_confianca.py"
```

O JSON só tem números, sem token, então o pipe não expõe segredo (a proibição do CLAUDE.md é para pipe que carrega token). Alternativa sem pipe, no mesmo espírito da "Exceção controlada" do CLAUDE.md: gravar o JSON com a ferramenta Write num caminho absoluto dentro do projeto, `{RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/tmp/score-entrada.json` (não usar `/tmp`: no Windows, a ferramenta Write e o Bash resolvem `/tmp` para pastas diferentes), e passar esse mesmo caminho como argumento (`{PY} "{RAIZ_PROJETO}/.claude/skills/trafego-diagnostico/scripts/calcular_score_confianca.py" "{RAIZ_PROJETO}/meus-produtos/{ativo}/trafego/tmp/score-entrada.json"`). Usar a alternativa se o Claude Code pedir confirmação para o pipe; apagar o arquivo no fim.

**Fórmula:** soma das 10 variáveis (cada uma de 0 a 10, total de 0 a 100). Sem peso diferente entre elas.

## As 4 faixas

| Faixa | Score | Significado |
|-------|-------|-------------|
| `alta_confianca` | 75 a 100 | Dados robustos. Decisão pode ser tomada com segurança. |
| `media_confianca` | 50 a 74 | Dados razoáveis. Decisão possível, mas com ressalvas. Monitorar de perto. |
| `baixa_confianca` | 25 a 49 | Dados frágeis. Decisão arriscada. Preferir teste pequeno antes de agir. |
| `dados_insuficientes` | 0 a 24 | Dados insuficientes. Não tomar decisão estrutural. Aguardar mais dados. |

**Trava pelos dias:** com menos de 7 dias de dado, a faixa é `dados_insuficientes`, qualquer que seja o score (princípio 12 do SKILL.md). O script aplica essa trava sozinho: mantém o número do score, troca a faixa, marca o risco como `critico` e devolve o campo `aviso` com a faixa que o score daria sem a trava. No relatório, dizer isso ao aluno (ex.: "o score é 95, mas com 5 dias de dado ainda não dá para decidir; faltam 2 dias").

## Output por decisão

Para cada decisão ou entidade avaliada, retornar:

```yaml
score_confianca:
  entidade:
    id: "<id>"
    nome: "<nome>"
    nivel: campanha | conjunto | anuncio
  score: 70
  faixa: media_confianca
  variaveis:
    volume_gasto: { valor: 350.00, pontos: 5 }
    conversoes: { valor: 8, pontos: 5 }
    dias_analisados: { valor: 7, pontos: 10 }
    consistencia_cv: { valor: 0.42, pontos: 5 }
    variacao_periodo: { valor: 0.18, pontos: 10 }
    frequencia: { valor: 2.1, pontos: 5 }
    concentracao_top1: { valor: 0.55, pontos: 5 }
    dependencia_remarketing: { valor: 0.25, pontos: 10 }
    qualidade_atribuicao: { valor: "pixel_ativo", pontos: 5 }
    distancia_meta: { valor: 1.15, pontos: 10 }
  variaveis_indisponiveis: []
  o_que_aumentaria_confianca:
    - "+8 conversões (para amostra mais confiável)"
  risco_da_decisao: medio
```

## Explicação obrigatória no output (regra dura)

O número sozinho não serve. **Todo score DEVE vir acompanhado de explicação em linguagem natural.** O aluno precisa entender 3 coisas: o que o número significa, por que está nesse nível e o que fazer para melhorar.

**Formato obrigatório por faixa:**

### Alta confiança (75 a 100)
```
Score de confiança: {score}/100 (ALTA)

O que significa: os dados desta {entidade} são robustos.
Você tem volume suficiente de gasto, conversões e dias para
tomar decisões com segurança.

Por que está alta: {listar as 2 ou 3 variáveis com maior pontuação
e o que elas representam em linguagem simples}

Pode decidir: sim, com segurança. Pausar, escalar ou ajustar
com base nesses dados é uma decisão bem fundamentada.
```

### Média confiança (50 a 74)
```
Score de confiança: {score}/100 (MÉDIA)

O que significa: os dados são razoáveis, mas não completos.
Ajustes de curto prazo (ajustar orçamento, pausar um criativo)
podem ser feitos. Escalar só se a entidade também sair como
vencedor real no detector de falso vencedor, e de forma gradual.
Pausar a campanha inteira deve esperar mais dados.

Por que não está alta: {listar as 2 ou 3 variáveis com menor
pontuação e explicar em linguagem simples}
Ex: "Você tem 8 conversões no período. São poucas para ter
certeza de que o CPA vai se manter. Com 16 ou mais conversões,
a confiança sobe."

Para melhorar: {lista do campo o_que_aumentaria_confianca,
traduzida para a linguagem do aluno}
```

### Baixa confiança (25 a 49)
```
Score de confiança: {score}/100 (BAIXA)

O que significa: os dados são frágeis. Qualquer conclusão
baseada nesses números pode estar errada. O resultado de hoje
pode ser completamente diferente na semana que vem.

Por que está baixa: {listar variáveis problemáticas}
Ex: "Apenas 3 conversões em 7 dias, com variação diária de
58%. Teve dia bom e dia péssimo sem padrão."

O que NÃO fazer: não pausar campanhas, não escalar, não
redistribuir orçamento com base nesses dados.

O que fazer: manter rodando mais {X} dias e reavaliar.
Se possível, {ações do campo o_que_aumentaria_confianca}.
```

### Dados insuficientes (0 a 24, ou menos de 7 dias de dado)
```
Score de confiança: {score}/100 (DADOS INSUFICIENTES)

O que significa: não há dados suficientes para qualquer
conclusão. Tomar decisão agora é decidir no escuro.

O que falta: {lista de variáveis zeradas ou muito baixas}
Ex: "2 conversões em 3 dias, gasto de R$ 80. É como
tentar ler o placar com 5 minutos de jogo."

Recomendação: aguardar pelo menos {X} dias e acumular
{Y} conversões antes de analisar.
```

**Regra dura:** nunca mostrar só o número e a faixa. Sempre incluir o bloco explicativo completo. Se o relatório tiver gauge de confiança (HTML), o texto explicativo fica imediatamente abaixo do gráfico.

---

## Impacto nos outros módulos

Quando rodado no Diagnóstico Completo (primeiro da sequência):

- **Faixa geral da conta `dados_insuficientes`** (score abaixo de 25 ou menos de 7 dias de dado, pela trava acima): todos os módulos seguintes rodam com o aviso "⚠️ Dados insuficientes. As conclusões abaixo são direcionais, não definitivas." Todas as probabilidades do diferencial recebem teto de 50%.
- **Faixa geral da conta `baixa_confianca`** (sempre depois da trava pelos dias): os módulos seguintes rodam com ressalva. Probabilidades do diferencial recebem teto de 70%.
- **Faixa geral da conta `media_confianca` ou `alta_confianca`** (sempre depois da trava pelos dias): os módulos seguintes rodam normalmente, sem teto artificial.

O score geral da conta é a média ponderada por gasto descrita no início (campanhas ativas com gasto > 0 no período).

## Relatório humano (seções aplicáveis)

Usar as seções 1 (contexto), 2 (diagnóstico real), 5 (riscos) e 7 (decisão recomendada) da estrutura de 7 seções do SKILL.md principal.

Exemplo de narrativa:
```
CONTEXTO: Analisei 8 campanhas ativas nos últimos 7 dias. Gasto total: R$ 2.840.

DIAGNÓSTICO: A confiança geral dos dados da conta é MÉDIA (score 62/100).
- Os dados dizem: 5 campanhas têm dados suficientes para diagnóstico confiável.
- Os dados NÃO dizem: 3 campanhas têm menos de 5 conversões no período. Qualquer conclusão sobre elas é frágil.
- Erro a evitar: tratar o ROAS dessas 3 campanhas como indicador confiável.

RISCOS: A campanha "Produto A Perpétuo" tem score 38 (baixa confiança). 2 conversões em 7 dias.
Qualquer decisão de pausar ou escalar com base nesses dados é prematura.

DECISÃO: Manter "Produto A Perpétuo" rodando por mais 7 dias antes de decidir.
NÃO pausar por CPA alto: com 2 conversões, CPA alto é ruído, não sinal.
```
