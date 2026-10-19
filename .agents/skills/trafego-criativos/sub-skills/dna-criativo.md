# Sub-skill. DNA Criativo

Encontra padrões comportamentais entre criativos vencedores e perdedores. Diferente do "DNA dos Winners" do output [3] da `/trafego-analise` (que mostra o top 3 por conversão + o padrão comum), esta sub-skill **agrupa por perfil comportamental**, liga cada perfil aos **tipos da Mandala da Criatividade**, analisa o que funciona por temperatura de público, detecta safras criativas e sintetiza a fórmula vencedora da conta.

## Contexto multi-produto

Roda **por produto**. O DNA criativo pode ser completamente diferente entre produtos (high ticket pode ter DNA de "intenção silenciosa", low ticket de "gancho forte").

## Quando é acionado

- Opção [6] do menu principal.
- Automaticamente na Inteligência Completa (quinto módulo).
- Quando o aluno pergunta "o que os meus melhores criativos têm em comum?" ou "qual tipo da Mandala funciona na minha conta?".

## Dados necessários

Todas as métricas dos módulos 1 a 4 + `created_time` dos anúncios (análise de safras) + o texto de cada anúncio (corpo e título) para identificar o tipo da Mandala:
- `MCP_CONECTOR`: `ads_get_creatives` (ou o campo de criativo do `ads_get_ad_entities`, confirmado com `ads_get_field_context`).
- `APP`: `curl -g` em `/{ad_id}?fields=creative{body,title,object_story_spec,asset_feed_spec}`.

## Agrupamento por perfil comportamental

NÃO é ranking do melhor para o pior. É classificação pelo tipo de comportamento que o criativo gera:

| Perfil | Critérios | Descrição |
|--------|-----------|-----------|
| `criativo_de_atencao` | Hook Rate alto (> 25%) + Hold Rate alto (> 40%) + CTR baixo + CPA acima da meta | Entretém e prende, mas não vende. Bom para reconhecimento, fraco para conversão. |
| `criativo_de_intencao` | Hook moderado + CTR alto (> benchmark × 1,5) + CPA moderado | Gera muito clique. Pode ser qualificado ou curiosidade vazia (verificar Click-to-LPV). |
| `criativo_de_conversao` | Hook baixo ou moderado + CTR baixo ou moderado + CPA excelente (< meta × 0,8) | Filtra naturalmente: pouca gente clica, mas quem clica compra. O mais valioso por real investido. |
| `criativo_equilibrado` | 4 camadas OK no diagnóstico + CPA < meta | Raro e ideal. Captura atenção, gera intenção qualificada e converte. Candidato a escala. |
| `criativo_ineficiente` | Hook baixo + CTR baixo + CPA alto | Não captura, não converte. Candidato a pausa. |

**Distribuição:** mostrar quantos criativos estão em cada perfil + % do gasto total em cada um.

```
Distribuição por perfil comportamental:

| Perfil         | Qtd | % Gasto | CPA médio | Ação                    |
|----------------|-----|---------|-----------|-------------------------|
| Atenção        | 2   | 25%     | R$ 210    | Ajustar CTA/promessa    |
| Intenção       | 3   | 35%     | R$ 165    | Qualificar ou manter    |
| Conversão      | 1   | 10%     | R$ 72     | Proteger e escalar      |
| Equilibrado    | 1   | 20%     | R$ 95     | Criar variações         |
| Ineficiente    | 1   | 10%     | R$ 340    | Pausar                  |
```

## Ligação com a Mandala da Criatividade

Os nomes dos tipos vêm de `.claude/skills/mandala-de-anuncios/SKILL.md` (seção "Os 21 tipos de anúncio"). Os tipos de 1 a 18 são os 18 tipos da Mandala da Criatividade; os tipos 19 a 21 são extensões e também contam quando aparecerem:

| # | Tipo | # | Tipo | # | Tipo |
|---|------|---|------|---|------|
| 1 | Comparação | 7 | Visual | 13 | Ultra Segmentado |
| 2 | Apelo Emocional | 8 | Dilema | 14 | Reflexão |
| 3 | Certo vs Errado | 9 | Clickbait | 15 | Explicação |
| 4 | Curiosidade | 10 | Prova | 16 | Problema-Solução |
| 5 | Demonstração | 11 | Contraste | 17 | Sensação |
| 6 | Oportunidade | 12 | História | 18 | Mito |

Extensões: 19 Pesquisa Científica, 20 Atualidades, 21 Atualidades Trend.

### Como descobrir o tipo de cada criativo (nesta ordem)

1. **Nome do anúncio** com o tipo escrito (convenção do aluno, ex.: "AD - Mito - Vídeo 30s"). Só vale se o nome trouxer um dos nomes da tabela.
2. **Texto do anúncio** (corpo e título, lidos pela API): ler o gancho e classificar no tipo mais provável, marcando `tipo_inferido_pelo_texto`. Em vídeo, o texto do anúncio não mostra o roteiro falado: confiança baixa, declarar.
3. **Sem nome nem texto:** `tipo_nao_identificado`. Não perguntar criativo por criativo. Se mais da metade do gasto ficar sem tipo, fazer uma pergunta só ao aluno:

```
Seus anúncios seguem alguma convenção de nome com o tipo da Mandala?

1. Sim (me diga o padrão, ex: "AD - {tipo} - {formato}")
2. Não, pode seguir sem o tipo

Digite o número:
```

### Cruzamento perfil comportamental × tipo da Mandala

O que esta sub-skill acrescenta à Mandala é **qual tipo produz qual comportamento nesta conta**:

```
Tipo da Mandala × perfil comportamental (Produto A, últimos 7 dias):

| Tipo              | Qtd | % Gasto | Perfil dominante      | CPA médio | Vence em |
|-------------------|-----|---------|-----------------------|-----------|----------|
| Mito              | 2   | 30%     | criativo_de_conversao | R$ 78     | cold     |
| Curiosidade       | 3   | 35%     | criativo_de_intencao  | R$ 170    | warm     |
| Prova             | 1   | 15%     | criativo_equilibrado  | R$ 92     | cold     |
| História          | 1   | 10%     | criativo_de_atencao   | R$ 215    | n/a      |
| (sem tipo)        | 1   | 10%     | n/a                   | R$ 140    | n/a      |

INSIGHT: nesta conta, Mito e Prova geram compra em público frio;
Curiosidade gera clique, mas só converte em remarketing.
```

**Regras:**
- **Volume manda:** só chamar um tipo de "vencedor" quando ele somar 15 vendas ou mais no período. Abaixo disso, é tendência e leva ⚠️.
- **Não duplicar o Gap Finder:** a lista de tipos **ausentes** é do output [3] da `/trafego-analise`. Aqui entram só os tipos presentes. Para os ausentes, uma linha remetendo ao output [3] e, se fizer sentido, um briefing de teste (sub-skill `briefing-criativo.md`).
- **Temperatura e objetivos da Mandala:** na leitura por temperatura, cold corresponde aos objetivos Descoberta e Conversão da Mandala, e warm ao objetivo RMKT.

## Perfil por temperatura (cold vs warm)

Qual tipo de criativo funciona em cada temperatura de público (sempre pela segmentação real, seção 4.5 do SKILL.md):

```
Perfil que funciona por temperatura:

COLD (público frio, prospecção):
  Vencedor: criativos de conversão (CPA R$ 72)
  Padrão: gancho menos agressivo, promessa mais direta, CTR moderado
  Tipos da Mandala que mais vendem aqui: Mito, Prova

WARM (remarketing):
  Vencedor: criativos de intenção (CPA R$ 28)
  Padrão: gancho forte, urgência, CTA direto
  Tipos da Mandala que mais vendem aqui: Curiosidade

INSIGHT: criativos de atenção funcionam em cold para reconhecimento,
mas não convertem. Criativos de conversão são os únicos que
vendem em cold de forma sustentável nesta conta.
```

## Safras criativas

Agrupar por período de criação (`created_time`):

```
Safras criativas (por mês de criação):

| Safra       | Qtd | CPA médio | Hook médio | Status      |
|-------------|-----|-----------|------------|-------------|
| Mar/2026    | 3   | R$ 120    | 28%        | Fadigando   |
| Abr/2026    | 4   | R$ 95     | 32%        | Ativo       |
| Mai/2026    | 2   | R$ 85     | 35%        | Fresco      |

Tendência: safras mais novas performam melhor. Sinal de
fadiga geral. A conta precisa de renovação criativa contínua
(a cada 2 a 3 semanas) para manter resultados.
```

Três padrões de safra:
- `fadiga_progressiva`: safras novas sempre melhores que as antigas (precisa de renovação constante).
- `formula_estavel`: safras antigas e novas performam parecido (fórmula validada, sem renovação urgente).
- `safra_regressiva`: safras novas performam pior que as antigas (os últimos criativos não acertaram).

## Fórmula vencedora da conta

Sintetizar os limiares que separam vencedores de perdedores com base nos dados reais:

```
🧬 FÓRMULA VENCEDORA DESTA CONTA

Criativos que vendem nesta conta têm:
  Hook Rate > 28%
  Hold Rate > 42%
  CTR > 1,3%
  Click-to-LPV Rate > 65%
  CPA < R$ 130

Criativos abaixo desses limiares tendem a gerar atenção
ou curiosidade, mas não venda.

Perfil dominante: "conversão silenciosa", criativos com
CTR moderado mas alta qualificação do clique.

Tipos da Mandala dominantes entre os vencedores: Mito e Prova.

Padrão de gancho: ganchos que abrem com dor específica
(não genérica) performam 40% melhor em CPA.

Formato dominante: vídeo de 15 a 30s supera vídeo de 60s ou mais
nesta conta (o Hold Rate cai 35% depois dos 30s).
```

Os limiares são derivados dos dados reais (percentil 75 dos vencedores vs percentil 25 dos perdedores), não valores fixos.

## Explicação obrigatória

Cada perfil e achado DEVE ter explicação:

```
DNA CRIATIVO: CONVERSÃO SILENCIOSA

O que significa: os criativos que mais vendem nesta conta não
são os que mais chamam atenção. São os que menos atraem clique
curioso e mais qualificam o público.

Por que importa: se você criar criativos buscando CTR alto,
vai atrair curiosos. O DNA desta conta mostra que CPA bom
vem de CTR moderado com qualificação alta.

O que fazer: os próximos criativos devem focar em promessa
direta (não "descubra o segredo"), com prova concreta, nos
tipos da Mandala que já vendem aqui. A produção vai para
/copy-anuncio ou /mandala-de-anuncios.
```

## Output YAML

```yaml
dna_criativo:
  produto: "Produto A"
  total_analisados: 8

  distribuicao_perfis:
    - perfil: criativo_de_atencao
      quantidade: 2
      pct_gasto: 0.25
      cpa_medio: 210.00
    - perfil: criativo_de_conversao
      quantidade: 1
      pct_gasto: 0.10
      cpa_medio: 72.00
    # ...

  mandala:
    fonte_dos_nomes: ".claude/skills/mandala-de-anuncios/SKILL.md"
    tipos_presentes:
      - tipo: "Mito"
        quantidade: 2
        pct_gasto: 0.30
        perfil_dominante: criativo_de_conversao
        cpa_medio: 78.00
        vendas: 9
        vence_em: cold
        como_identificado: nome | tipo_inferido_pelo_texto
        volume_suficiente: false
    pct_gasto_sem_tipo: 0.10
    tipos_ausentes: "ver Gap Finder do output [3] da /trafego-analise"

  perfil_por_temperatura:
    cold_vencedor: criativo_de_conversao
    warm_vencedor: criativo_de_intencao

  safras:
    padrao: fadiga_progressiva | formula_estavel | safra_regressiva
    detalhe:
      - safra: "2026-03"
        qty: 3
        cpa_medio: 120.00

  formula_vencedora:
    hook_rate_min: 0.28
    hold_rate_min: 0.42
    ctr_min: 0.013
    click_to_lpv_min: 0.65
    cpa_max: 130.00
    perfil_dominante: "conversao_silenciosa"
    tipos_mandala_dominantes: ["Mito", "Prova"]
    formato_dominante: "video_15_30s"
```
