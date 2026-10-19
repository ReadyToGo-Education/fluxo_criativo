# Sub-skill. Diagnóstico Diferencial

Apresenta as **3 hipóteses mais prováveis** para o problema detectado, com peso de probabilidade, sinais que confirmam e refutam cada uma, o que se esperaria ver se fosse verdade, e o teste que desempata.

**Diferença da `/trafego-otimizar`:** a otimizar aponta UM gargalo e age. Aqui: estilo médico. Diagnóstico diferencial com hipóteses concorrentes. Nenhuma ação é executada.

## Contexto multi-produto

Quando a conta tem mais de 1 produto declarado, o diagnóstico diferencial roda **por produto** separadamente. Motivo: fadiga criativa no Produto A (perpétuo, R$ 2.500) pode coexistir com saturação de público no Produto B (lançamento, R$ 997). São problemas diferentes que exigem ações diferentes.

Cada produto gera suas **3 hipóteses independentes** com pesos próprios. O relatório apresenta uma seção por produto:

```
PRODUTO: Produto A (R$ 2.500, perpétuo high)
  Hipótese 1: fadiga criativa (65%)
  Hipótese 2: saturação de público (20%)
  Hipótese 3: atribuição frágil (15%)

PRODUTO: Produto B (R$ 997, perpétuo mid)
  Hipótese 1: oferta/funil (55%)
  Hipótese 2: fragmentação de orçamento (30%)
  Hipótese 3: criativo (15%)
```

**Exceção:** se um gargalo é compartilhado entre produtos (ex: CPM alto em toda a conta), destacar como "gargalo transversal" no topo.

---

## Quando é acionado

- Opção [2] do menu principal
- Automaticamente no Diagnóstico Completo (quarto e último módulo da sequência)
- Quando o aluno pergunta "onde está o problema?" ou "por que meu CPA subiu?"
- Quando `/trafego-escalar` aciona freio total e sugere investigação

## Dados necessários

Pedir à `/trafego-insights`:
- Campanha(s) específica(s) ou `escopo: conta_completa`
- Todos os níveis: `campaign` + `adset` + `ad`
- 3 janelas da trilha + período anterior (via `comparar_periodos`)
- Todas as métricas derivadas (connect rate, taxas de conversão, custos por etapa)
- `serie_diaria` das métricas-norte

Complementar (leitura pura, por modo, conforme a seção 3.1 do SKILL.md):
- Segmentação dos conjuntos (quando a hipótese de canibalização ou de remarketing for relevante).

Reforços opcionais no modo MCP (seção 3.2 do SKILL.md), quando as tools existirem na conta:
- `ads_account_get_activity_logs`: confirma ou descarta "orçamento aumentou recentemente" e "campanha perdeu estabilidade após mudança" com data e autor da alteração. Responde "o que mudou na conta?".
- `ads_insights_anomaly_signal`: anomalias que a Meta detectou no período. Entra como sinal adicional, nunca como causa sozinha.
- `ads_insights_auction_ranking_benchmarks`: classificação de qualidade, engajamento e conversão contra os concorrentes do leilão. Ajuda a separar "criativo" de "leilão/público".
- `ads_insights_industry_benchmark`: referência do setor para CTR, CPM e custo por resultado.

No modo `APP`, sem essas tools, o histórico de alterações vem do aluno (Histórico da conta no Gerenciador) quando a hipótese de orçamento depender dele.

## As 7 categorias de gargalo

Expandidas em relação à `/trafego-otimizar` (que tem 6: criativo, técnico, página, checkout, leilão_audiência, saturação):

| Categoria | O que investiga | Dentro ou fora do Meta |
|-----------|-----------------|------------------------|
| **criativo** | Fadiga criativa, poucos criativos com tração, hook fraco | Dentro |
| **oferta_funil** | CTR bom mas conversão pós-clique baixa, objeções de preço/confiança. Handoff: `/trafego-oferta-funil` para ler a página e diagnosticar oferta. | Fora |
| **publico_saturacao** | Público esgotado, frequência alta, alcance incremental zero | Dentro |
| **orcamento_distribuicao** | Escala agressiva que quebrou aprendizado, fragmentação, pulverização | Dentro |
| **estrutura_aprendizado** | Conta mal organizada impedindo o algoritmo de aprender | Dentro |
| **atribuicao_dados** | Resultado inflado pela atribuição, falso vencedor, dados frágeis | Dentro (percepção) / Fora (realidade) |
| **dados_insuficientes** | Pouco gasto, poucas conversões, janela curta demais | N/A |

**Categorias NOVAS vs otimizar:** `orcamento_distribuicao`, `estrutura_aprendizado` e `atribuicao_dados` não existem na otimizar.

## Padrões de sinais por categoria

### Criativo (fadiga / força criativa)

| Sinal | Direção | Peso |
|-------|---------|------|
| CTR caindo na janela curta vs longa | confirma | alto |
| CPC subindo | confirma | alto |
| Frequência subindo (> 2.5) | confirma | médio |
| CPM estável ou subindo pouco | confirma (não é leilão) | médio |
| Poucos criativos ativos (< 3) | confirma | médio |
| 1 criativo com 70%+ do gasto | confirma (concentração) | médio |
| CPA subiu DEPOIS da queda de CTR | confirma (sequência causal) | alto |
| Criativos novos nos últimos 14 dias | refuta | alto |
| CPM disparou (> 40% acima do histórico) | refuta (pode ser leilão) | alto |

### Oferta / Funil

| Sinal | Direção | Peso |
|-------|---------|------|
| CTR bom (acima de saudável) | confirma (anúncio atrai) | alto |
| CPC aceitável | confirma | médio |
| Visitas à página (landing page views) ok | confirma (tráfego chega) | alto |
| Conversão pós-clique baixa | confirma (problema na página) | alto |
| CPA alto apesar de tráfego | confirma | alto |
| ROAS ruim com volume de cliques | confirma | alto |
| Connect rate < 60% | refuta parcialmente (pode ser técnico, não oferta) | médio |
| Produto novo / sem histórico | confirma (oferta não validada) | médio |

### Público / Saturação

| Sinal | Direção | Peso |
|-------|---------|------|
| CPM subindo consistentemente | confirma | alto |
| Frequência > 3.5 | confirma | alto |
| Alcance incremental próximo de zero | confirma | alto |
| Público estimado < 100k | confirma | médio |
| CTR estável mas CPA piorando | confirma (qualidade do público caindo) | alto |
| CPM estável | refuta | alto |
| Público amplo (> 1M) | refuta | médio |

### Orçamento / Distribuição

| Sinal | Direção | Peso |
|-------|---------|------|
| Orçamento aumentou > 30% recentemente (confirmar no histórico de alterações) | confirma | alto |
| CPA piorou logo após aumento | confirma (sequência temporal) | alto |
| Alta variação diária de CPA (CV > 0.50) | confirma | médio |
| Poucas conversões por conjunto (< 1/dia) | confirma (fragmentação) | alto |
| Muitos conjuntos com < R$ 30/dia | confirma (pulverização) | alto |
| Campanha perdeu estabilidade após mudança | confirma | alto |
| Orçamento estável há 14+ dias | refuta | alto |

### Estrutura / Aprendizado

| Sinal | Direção | Peso |
|-------|---------|------|
| > 10 campanhas ativas | confirma | médio |
| > 5 conjuntos por campanha com < R$ 50/dia cada | confirma | alto |
| Conjuntos em LEARNING_LIMITED | confirma | alto |
| Anúncios sem entrega (impressões = 0) | confirma | médio |
| Campanhas com objetivos conflitantes no mesmo público | confirma | alto |
| Criativos duplicados em campanhas diferentes | confirma | médio |
| Estrutura enxuta (3-5 campanhas, 2-3 conjuntos cada) | refuta | alto |

### Atribuição / Dados

| Sinal | Direção | Peso |
|-------|---------|------|
| ROAS alto com < 10 compras | confirma | alto |
| Resultado concentrado em remarketing | confirma | alto |
| Frequência alta (> 4.0) com ROAS alto | confirma | alto |
| Público pequeno com bom resultado | confirma | médio |
| Baixa consistência temporal (CV > 0.60) | confirma | alto |
| Dados de < 5 dias | confirma | médio |
| Mais de 30 compras, prospecção dominante, frequência < 2,5 | refuta | alto |

## Fluxo de investigação

1. **Puxar dados** via `/trafego-insights` (período atual + anterior)
2. **Comparar períodos** (via `comparar_periodos`): identificar quais métricas pioraram
3. **Para cada categoria**, calcular score de probabilidade:
   - Contar sinais que confirmam × peso
   - Subtrair sinais que refutam × peso
   - Normalizar para 0-100%
4. **Ranquear as 3 categorias com maior probabilidade**
5. **Para cada hipótese no top 3**, montar o bloco completo (ver output)
6. **Se no Diagnóstico Completo**, ajustar probabilidades conforme inteligência cruzada:
   - Score de confiança baixo → teto de 50% em todas as hipóteses
   - Auditoria flagrou fragmentação severa → elevar "estrutura_aprendizado"
   - Falso vencedor flagrou entidades → excluir do cálculo de "o que funciona"

## Explicação obrigatória no output (regra dura)

Cada hipótese DEVE vir com explicação em linguagem natural. O aluno precisa entender: **o que está acontecendo** (não a métrica, o fenômeno), **por que provavelmente é isso** (evidência simples), **o que fazer** (ação concreta) e **como confirmar** (teste rápido).

**Formato obrigatório por hipótese:**

```
HIPÓTESE 1: {nome em linguagem simples} ({probabilidade}%)

O que está acontecendo:
{Explicação do fenômeno em 2-3 frases para leigo. Sem jargão técnico.}
Ex: "Seus anúncios estão cansando o público. As mesmas pessoas estão
vendo os mesmos criativos muitas vezes e pararam de clicar."

Por que provavelmente é isso:
- {Sinal 1 traduzido}: "{métrica} → {o que isso significa na prática}"
  Ex: "O CTR caiu 28% em 7 dias → menos gente está clicando nos seus anúncios"
- {Sinal 2 traduzido}
- {Sinal 3 traduzido}

O que descarta outras causas:
- {Sinal que refuta outra hipótese, traduzido}
  Ex: "O CPM está estável → o leilão não ficou mais caro, então o
  problema não é concorrência"

O que fazer:
{Ação concreta em 1-2 frases}
Ex: "Subir 2 criativos novos com ângulos diferentes. Pode ser vídeo
com gancho diferente ou imagem com abordagem oposta."

Como confirmar (teste rápido):
- Teste: {descrição simples}
- Funciona se: {critério de sucesso em linguagem simples}
- Não funciona se: {critério de morte}
- Quanto tempo: {prazo}
```

**Para hipóteses com probabilidade < 20%:** explicação mais curta (2-3 linhas), sem bloco de teste completo. Focar na hipótese principal.

**Para categorias descartadas:** uma frase explicando por que não é isso. Ex: "Oferta/funil descartada: o funil está funcionando (82% de quem clica chega na página, 2.1% compra). O problema é antes do clique, não depois."

---

## Output

```yaml
diagnostico_diferencial:
  hipoteses:
    - rank: 1
      categoria: criativo
      probabilidade_pct: 65
      label_humano: "Fadiga criativa provável"
      sinais_que_confirmam:
        - "CTR caiu 28% (de 1.8% para 1.3%) na janela curta vs longa"
        - "CPC subiu 22% no mesmo período"
        - "Frequência subiu de 1.9 para 3.1"
        - "CPA subiu 35% APÓS a queda de CTR (sequência causal)"
      sinais_que_refutam:
        - "CPM estável (variação < 5%): leilão não é a causa"
      o_que_esperaria_se_fosse_verdade:
        - "CPC continuaria subindo nos próximos 3-5 dias"
        - "Hook rate dos vídeos cairia junto com CTR"
        - "Criativo novo teria CTR significativamente melhor que os atuais"
      teste_para_confirmar:
        hipotese: "A fadiga criativa é a causa principal da deterioração"
        teste: "Subir 2 criativos novos (ângulos diferentes) no conjunto vencedor"
        criterio_sucesso: "CTR do criativo novo > 1.5% em 72h com 5k+ impressões"
        criterio_morte: "CTR do criativo novo < 1.0% com 5k+ impressões"
        dados_minimos: "72h, 5.000 impressões por criativo"

    - rank: 2
      categoria: publico_saturacao
      probabilidade_pct: 20
      ...

    - rank: 3
      categoria: atribuicao_dados
      probabilidade_pct: 15
      ...

  descartadas:
    - categoria: oferta_funil
      motivo: "Connect rate 82% e conversão de página 2,1%: funil está funcional"
    - categoria: orcamento_distribuicao
      motivo: "Orçamento estável há 21 dias, sem mudança recente"
```

## Relatório humano

Usar as 7 seções completas. Exemplo de narrativa da seção 3 (Hipótese Central):

```
HIPÓTESE CENTRAL (confiança: 65%)

A causa mais provável é fadiga criativa. Evidência: CTR caiu 28% na janela curta,
CPC subiu 22%, frequência saltou de 1.9 para 3.1, e o CPA só piorou DEPOIS da
queda de CTR (sequência causal clássica de fadiga).

CPM estável descarta leilão como causa (se fosse leilão, CPM teria subido junto).

Hipóteses alternativas:
- Saturação de público (20%): frequência alta confirma, mas público estimado > 500k refuta parcialmente.
- Fragilidade de atribuição (15%): possível, mas 22 compras em 7 dias com CV 0.35 é amostra razoável.

TESTE PARA DESEMPATAR: subir 2 criativos novos. Se CTR voltar para > 1.5% em 72h,
confirma fadiga. Se não, investigar público e página.

Para investigação criativa detalhada (onde exatamente o criativo quebra,
qual perfil funciona, que teste criar): rode /trafego-criativos.
```
