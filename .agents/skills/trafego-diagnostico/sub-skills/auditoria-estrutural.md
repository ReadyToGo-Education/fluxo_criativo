# Sub-skill. Auditoria Estrutural

Avalia se a **arquitetura da conta** está sabotando o aprendizado do algoritmo do Meta. Não é "o que está quebrado" (isso é o output [8] Problemas Ocultos da `/trafego-analise`). É "o que está mal projetado".

**Diferença do output [8] Problemas Ocultos da análise:**
- Problemas Ocultos lista itens pontuais: conjuntos sem gasto, anúncios desaprovados, pixel morto
- Auditoria Estrutural avalia o **design** da conta: canibalização, fragmentação, coerência, densidade de aprendizado

## Contexto multi-produto

Diferente dos outros 3 módulos, a auditoria estrutural roda **globalmente** (não por produto). Motivo: canibalização de público, fragmentação de orçamento e incoerência de objetivos são problemas da **conta inteira**, não de um produto isolado. Duas campanhas de produtos diferentes competindo pelo mesmo público é canibalização que só aparece na visão global.

Porém, o contexto de produtos **enriquece** a análise:
- **Canibalização entre produtos:** campanhas do Produto A e do Produto B mirando o mesmo público de interesses é canibalização que o aluno pode não perceber
- **Fragmentação por produto:** 20 conjuntos do Produto A com R$ 20/dia cada vs 2 conjuntos do high ticket com R$ 500/dia cada = fragmentação concentrada no Produto A
- **Densidade por produto:** o Produto A pode ter 7 conversões/dia (aprendendo bem) enquanto o Produto B tem 0,3 conversão/dia (algoritmo cego)

No output, o score de saúde é global (0-100), mas os problemas encontrados são contextualizados por produto quando aplicável.

---

## Quando é acionado

- Opção [3] do menu principal
- Automaticamente no Diagnóstico Completo (segundo módulo da sequência)
- Quando o aluno pergunta "minha conta está bagunçada?"
- Quando `/trafego-escalar` atinge teto de audiência e sugere buscar espaço

## Dados necessários

Pedir à `/trafego-insights`:
- `escopo: conta_completa`
- `nivel: campaign + adset + ad`
- Janela: últimos 30d (para contexto suficiente de aprendizado)
- `effective_status` e `created_time` de cada entidade
- Conversões por conjunto (para densidade de aprendizado)
- `daily_budget` ou `lifetime_budget` por campanha/conjunto

Complementar (leitura pura, por modo, conforme a seção 3.1 do SKILL.md):
- Segmentação de cada conjunto ativo. `APP`: `curl -g` em `/{adset_id}?fields=targeting{...}`. `MCP_CONECTOR`: `ads_get_ad_entities` se `ads_get_field_context` confirmar o campo; para públicos personalizados, `ads_get_ad_account_custom_audiences` + `ads_get_custom_audience_adsets`.
- `objective` de cada campanha (já vem na insights quando incluído nos campos; no MCP, `ads_get_ad_entities`).
- Fase de aprendizado dos conjuntos (`learning_stage_info` no App; `effective_status` como alternativa no MCP).

Reforços opcionais no modo MCP (seção 3.2 do SKILL.md):
- `ads_get_opportunity_score`: recomendações e pontuação de oportunidade da própria Meta. Comparar com os 6 eixos abaixo; recomendação da Meta entra como sinal, nunca como ação automática.
- `ads_account_get_activity_logs`: mexidas recentes na estrutura (conjuntos criados, orçamentos alterados, pausas), úteis no eixo de idade e para explicar instabilidade.

## Os 6 eixos da auditoria

### Eixo 1. Canibalização de público

Campanhas ativas com targeting sobreposto competem entre si no leilão do Meta, inflando CPM e desperdiçando orçamento.

**Como detectar (sem API de overlap, que não existe):**
- Comparar a segmentação real dos conjuntos ativos (nunca inferir pelo nome)
- Flagrar quando 2+ conjuntos têm `interests`, `behaviors`, `custom_audiences` ou `lookalike_audiences` idênticos ou com sobreposição > 70% (mesmos IDs de interesse)
- Flagrar quando 2+ campanhas de conversão apontam para o mesmo público salvo (saved audience)
- Caso especial: campanha com público aberto (sem segmentação) + campanha segmentada → a aberta canibaliza porque o Meta prioriza quem paga mais

**Classificação:**
- `sem_canibalizacao`: nenhum par de conjuntos com sobreposição relevante
- `canibalizacao_leve`: 1-2 pares com sobreposição, gasto combinado < 30% do total
- `canibalizacao_severa`: 3+ pares ou gasto combinado > 30% do total

### Eixo 2. Fragmentação de orçamento

Conjuntos que nunca saem da fase de aprendizado porque o orçamento é baixo demais para o volume de conversões necessário (Meta exige ~50 conversões em 7 dias para sair do aprendizado).

**Como detectar:**
- Para cada conjunto ativo: calcular `conversoes_por_dia = conversoes_30d / 30`
- Se `conversoes_por_dia < 1.0`: conjunto está em aprendizado perpétuo (algoritmo cego)
- Se `daily_budget < R$ 30`: risco de fragmentação (a menos que ticket seja muito baixo)
- Contar quantos conjuntos estão fragmentados vs total de conjuntos ativos

**Classificação:**
- `sem_fragmentacao`: < 20% dos conjuntos fragmentados
- `fragmentacao_moderada`: 20-50% dos conjuntos fragmentados
- `fragmentacao_severa`: > 50% dos conjuntos fragmentados

### Eixo 3. Incoerência de objetivos

Campanhas com objetivos conflitantes rodando no mesmo público confundem o algoritmo.

**Como detectar:**
- Mapear `objective` de cada campanha ativa
- Flagrar quando campanhas de `OUTCOME_ENGAGEMENT` / `OUTCOME_AWARENESS` e `OUTCOME_SALES` / `OUTCOME_LEADS` miram o mesmo público (cruzar targeting specs)
- Flagrar quando remarketing e aquisição estão na mesma campanha sem separação clara de conjuntos

**Classificação:**
- `coerente`: cada objetivo em público separado
- `parcialmente_incoerente`: 1 par com conflito
- `incoerente`: múltiplos conflitos ou remarketing misturado com aquisição

### Eixo 4. Idade da estrutura

Campanhas e criativos velhos que nunca foram renovados.

**Como detectar:**
- Para cada campanha/conjunto/ad ativo: calcular idade = hoje - `created_time`
- Campanhas com 60+ dias sem criativo novo (nenhum ad com `created_time` nos últimos 60 dias)
- Conjuntos com 90+ dias rodando contínuo
- Proporção de ads ativos com > 30 dias vs < 30 dias

**Classificação:**
- `estrutura_fresca`: > 50% dos ads ativos criados nos últimos 30 dias
- `estrutura_madura`: 30-50% dos ads com < 30 dias
- `estrutura_envelhecida`: < 30% dos ads com < 30 dias

### Eixo 5. Densidade de aprendizado

Conversões por conjunto por dia: o combustível do algoritmo.

**Como detectar:**
- Para cada conjunto ativo: `densidade = conversoes_30d / 30`
- Classificar cada conjunto:
  - `aprendendo_bem`: ≥ 7 conversões/dia (50/semana, Meta recomenda)
  - `aprendendo_lento`: 1-6 conversões/dia
  - `algoritmo_cego`: < 1 conversão/dia
- Cruzar com `effective_status`: conjuntos em `LEARNING_LIMITED` confirmam a leitura

**Classificação da conta:**
- `densidade_alta`: > 50% dos conjuntos com ≥ 7 conv/dia
- `densidade_media`: > 50% dos conjuntos com ≥ 1 conv/dia
- `densidade_baixa`: > 50% dos conjuntos com < 1 conv/dia

### Eixo 6. Clareza da nomenclatura

Nomes de campanhas, conjuntos e ads que permitem leitura rápida vs caos.

**Como detectar:**
- Verificar se campanhas seguem padrão reconhecível (ex: "Perpétuo - Produto - Público")
- Flagrar nomes genéricos: "Campaign 1", "Copy", "Test", nomes só com data
- Verificar se o nível de conjunto distingue público/targeting
- Verificar se ads distinguem criativo/formato

**Classificação:**
- `nomenclatura_clara`: > 70% dos nomes seguem padrão reconhecível
- `nomenclatura_parcial`: 40-70%
- `nomenclatura_caotica`: < 40%

## Score de saúde estrutural (0 a 100)

Cada eixo contribui com até ~17 pontos (6 eixos, total ~100):

| Eixo | Melhor caso (17 pts) | Caso médio (~9 pts) | Pior caso (0 pts) |
|------|---------------------|---------------------|-------------------|
| Canibalização | sem_canibalizacao | canibalizacao_leve | canibalizacao_severa |
| Fragmentação | sem_fragmentacao | fragmentacao_moderada | fragmentacao_severa |
| Coerência | coerente | parcialmente_incoerente | incoerente |
| Idade | estrutura_fresca | estrutura_madura | estrutura_envelhecida |
| Densidade | densidade_alta | densidade_media | densidade_baixa |
| Nomenclatura | nomenclatura_clara | nomenclatura_parcial | nomenclatura_caotica |

**Eixo não verificado:** quando a segmentação não pode ser lida (comum no modo MCP), os eixos de canibalização e coerência ficam `nao_verificado`. Cada um conta como caso médio (cerca de 9 pontos) e o relatório declara a limitação e o que o aluno pode conferir no Gerenciador (aba Público de cada conjunto).

**Faixas (enum YAML):**

| Score | Slug | Significado |
|-------|------|-------------|
| 80-100 | `saudavel` | Estrutura saudável. Algoritmo tem condições de aprender. |
| 60-79 | `razoavel` | Estrutura razoável. Alguns ajustes melhorariam o aprendizado. |
| 40-59 | `comprometida` | Estrutura comprometida. Impacto provável na performance. |
| 0-39 | `sabotando` | Estrutura sabotando o algoritmo. Priorizar limpeza antes de otimizar métricas. |

## Explicação obrigatória no output (regra dura)

O score de saúde sozinho não serve. **Cada eixo DEVE vir acompanhado de explicação em linguagem natural.** O aluno precisa entender: o que está errado, por que atrapalha, e o que fazer (em ordem de prioridade).

**Formato obrigatório por faixa geral:**

### Saudável (80-100)
```
Saúde da estrutura: {score}/100 (SAUDÁVEL)

O que significa: a conta está bem organizada. O algoritmo do
Meta tem condições de aprender e otimizar. Sem ações urgentes.

Destaques positivos: {listar 2-3 eixos fortes}
```

### Razoável (60-79)
```
Saúde da estrutura: {score}/100 (RAZOÁVEL)

O que significa: a conta funciona, mas tem pontos que podem
estar limitando seus resultados sem você perceber.

O que precisa de atenção: {listar eixos com pontuação baixa,
em ordem de impacto, com explicação simples}
Ex: "22 dos seus 34 conjuntos têm menos de 1 conversão por
dia. Isso significa que o algoritmo do Meta não tem dados
suficientes para aprender quem compra. Ele está otimizando
no escuro nesses conjuntos."

O que fazer (em ordem): {lista numerada de ações}
```

### Comprometida (40-59)
```
Saúde da estrutura: {score}/100 (COMPROMETIDA)

O que significa: a organização da conta provavelmente está
prejudicando seus resultados. Antes de otimizar criativos
ou mexer em orçamento, vale limpar a estrutura.

Problemas encontrados (do mais grave ao menos grave):

1. {eixo}: {explicação em 2-3 frases simples do problema}
   O que fazer: {ação concreta}

2. {eixo}: {explicação}
   O que fazer: {ação}

Por que isso importa: o algoritmo do Meta precisa de
estrutura limpa para aprender. Uma conta bagunçada é como
tentar cozinhar numa cozinha desarrumada: tudo demora mais
e o resultado sai pior.
```

### Sabotando (0-39)
```
Saúde da estrutura: {score}/100 (SABOTANDO O ALGORITMO)

O que significa: a estrutura da conta está ativamente
prejudicando seus resultados. Otimizar criativos ou
mexer em orçamento AGORA não vai resolver. Primeiro,
limpar a estrutura.

Problemas críticos (resolver ANTES de qualquer outra coisa):

1. {problema mais grave com explicação completa}
2. {segundo problema}
3. {terceiro problema}

O que NÃO fazer enquanto a estrutura estiver assim:
- Não escalar (vai amplificar o problema)
- Não criar mais campanhas (vai piorar a fragmentação)
- Não julgar criativos (dados distorcidos pela estrutura)

Próximo passo: /trafego-otimizar em modo lote para
consolidar conjuntos e limpar o que não funciona.
```

**Regra por eixo:** cada eixo mostrado no output DEVE ter uma frase explicando o que significa para quem não é técnico. Exemplos:

| Eixo | Explicação obrigatória |
|------|----------------------|
| Canibalização | "Duas ou mais campanhas suas estão competindo pelo mesmo público no leilão do Meta. Isso encarece o custo porque você está disputando consigo mesmo." |
| Fragmentação | "Muitos conjuntos com orçamento pequeno demais. O Meta precisa de pelo menos 50 conversões por semana por conjunto para aprender. Com R$ 20/dia, dificilmente chega lá." |
| Incoerência | "Você tem campanhas de venda e de engajamento mirando o mesmo público. O Meta fica confuso sobre qual objetivo priorizar." |
| Idade | "Campanhas rodando há 60+ dias sem criativo novo. O público já viu seus anúncios muitas vezes e parou de prestar atenção." |
| Densidade | "Menos de 1 conversão por dia neste conjunto. O algoritmo está otimizando no escuro, sem dados suficientes para saber quem compra." |
| Nomenclatura | "Nomes como 'Campaign 1' e 'Teste' dificultam saber o que cada campanha faz. Nomenclatura clara acelera suas decisões." |

---

## Output

```yaml
auditoria_estrutural:
  score_saude: 58
  faixa: comprometida
  total_campanhas_ativas: 12
  total_adsets_ativos: 34
  total_ads_ativos: 78

  eixos:
    canibalizacao:
      classificacao: canibalizacao_leve
      pontos: 9
      pares_sobrepostos:
        - adset_a: { id: "<id>", nome: "<nome>" }
          adset_b: { id: "<id>", nome: "<nome>" }
          sobreposicao: "interesses idênticos: marketing digital, empreendedorismo"
    fragmentacao:
      classificacao: fragmentacao_severa
      pontos: 0
      adsets_fragmentados: 22
      adsets_total: 34
      pior_caso: { id: "<id>", nome: "<nome>", conversoes_dia: 0.1, orcamento_diario: 20.00 }
    coerencia:
      classificacao: coerente
      pontos: 17
    idade:
      classificacao: estrutura_envelhecida
      pontos: 3
      campanhas_sem_refresh_60d: 4
      ads_ativos_com_mais_de_30d_pct: 82
    densidade:
      classificacao: densidade_baixa
      pontos: 3
      adsets_algoritmo_cego: 19
      adsets_aprendendo_bem: 5
    nomenclatura:
      classificacao: nomenclatura_caotica
      pontos: 5
      exemplos_ruins: ["Campaign 1", "Copy teste", "2026-05-01"]

  limpezas_recomendadas:
    - prioridade: alta
      acao: "Consolidar 22 conjuntos fragmentados em 8-10 conjuntos com orçamento mínimo de R$ 50/dia"
      impacto: "Algoritmo sai do aprendizado em 5-7 dias"
    - prioridade: alta
      acao: "Subir 3 a 5 criativos novos nas 4 campanhas sem renovação há 60 dias ou mais"
      impacto: "Reduz fadiga e renova sinal para o algoritmo"
    - prioridade: media
      acao: "Padronizar nomenclatura: Tipo - Produto - Público - Criativo"
      impacto: "Leitura 3x mais rápida no Gerenciador"

  nao_fazer:
    - "Não criar mais campanhas antes de consolidar as existentes"
    - "Não aumentar orçamento de conjuntos com < 1 conversão/dia (jogar dinheiro em algoritmo cego)"
```

## Impacto no Diagnóstico Completo

Quando rodado como segundo módulo da sequência:
- Recebe o score de confiança geral do módulo 1 (se dados frágeis, auditoria opera com ressalva)
- Passa para o módulo 3 (falso vencedor): entidades em conjuntos fragmentados são automaticamente classificadas como `inconclusivo`
- Passa para o módulo 4 (diferencial): se score de saúde < 40, "estrutura_aprendizado" é adicionada como hipótese com peso elevado

## Relatório humano

Usar as 7 seções. Focar especialmente em seção 4 (alavancas, priorizadas por impacto na saúde) e seção 7 (limpezas recomendadas com ordem de execução).
