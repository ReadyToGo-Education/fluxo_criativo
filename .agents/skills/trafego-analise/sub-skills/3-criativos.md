# Output [3] — Criativos & Copy

Análise completa dos criativos ativos: formato, retenção de vídeo, CTA, fadiga e engajamento de texto. Responde as 5 perguntas obrigatórias em sequência e traz Tier Ranking e DNA dos Winners como seções extras.

---

## Perguntas que cobre

1. "Qual formato performa melhor? Imagem, vídeo ou carrossel — quem ganha em ROAS, CTR e CPA?"
2. "Os vídeos estão sendo assistidos até o final? (Thumbstop, Hook Rate, Hold Rate, Play-Through)"
3. "Qual CTA converte mais? Saiba Mais, Compre Agora, Cadastre-se — quem tem melhor CTR e CPA?"
4. "Tem criativo acima de 50.000 impressões que pode estar saturado? (Fadiga Map)"
5. "Quais textos têm melhor taxa de engajamento? (ranking por CTR — spend acima de R$ 100)"

---

## REGRA OBRIGATÓRIA ANTES DE ENTREGAR QUALQUER BLOCO

> **Todas as 5 perguntas acima precisam ter resposta antes de montar qualquer bloco de output.**
> Não é permitido entregar a análise com "dados não disponíveis" como substituto a uma busca que poderia ter sido feita.
> Buscar TODOS os dados abaixo em paralelo ANTES de escrever qualquer parágrafo.

---

## Dados necessários

Pedir ao `/trafego-insights`:
- **Escopo: usar `ESCOPO_FILTRO` definido no Passo 0.6 do command principal.** Não forçar `conta_completa`. Se o aluno escolheu um grupo (ex: "VTSD"), só puxar criativos das campanhas desse grupo.
- **Status: usar `STATUS_FILTRO` definido no Passo 0.55** (ACTIVE, PAUSED+WITH_ISSUES, ambos, ou histórico completo). Não assumir só ACTIVE.
- Período: usar período definido no Passo 3. Não perguntar de novo.
- Breakdown `publisher_platform` para split vídeo x imagem x carrossel
- Métricas de vídeo por ad: `video_avg_time_watched_actions`, `video_p25_watched_actions` (Thumbstop), `video_thruplay_watched_actions` (Hook Rate 25%), `video_p50_watched_actions` (Hold Rate), `video_p100_watched_actions` (Play-Through)
- Métricas por anúncio: `inline_link_clicks`, `link_clicks`, `cost_per_inline_link_click`, `actions[purchase]`, `spend`, `impressions`, `frequency`, `quality_ranking`, `engagement_rate_ranking`, `conversion_rate_ranking`
- Para Fadiga Map: filtrar anúncios com `impressions > 50000` (status já filtrado pelo `STATUS_FILTRO` acima)
- Para ranking de CTR: filtrar anúncios com `spend > 100` no período

---

## O que entregar

### Bloco 1. Comparativo de formato (Q1)

```
📐 FORMATO — últimos Xd

┌─────────────────────────────────────────────────┐
│  VÍDEO              │  IMAGEM              │
│  ROAS X,Xx          │  ROAS X,Xx           │
│  CTR X,Xx%          │  CTR X,Xx%           │
│  CPA R$ X           │  CPA R$ X            │
│  N anúncios         │  N anúncios          │
└─────────────────────────────────────────────────┘

Vencedor: {formato} — CPA X% mais barato, CTR X× maior
Se carrossel existir: incluir coluna adicional
```

Critério de decisão: formato com menor CPA E maior CTR é o recomendado para próxima rodada.

---

### Bloco 2. Funil de retenção de vídeo (Q2)

Só para anúncios de vídeo. Se não houver vídeos ativos, informar e pular.

```
🎬 RETENÇÃO DE VÍDEO — {N} vídeos ativos

Thumbstop (25% assistido):  X%   benchmark > 70%
Hook Rate  (3s / impressões): X%   benchmark > 25%
Hold Rate  (50% / 3s):       X%   benchmark > 40%
Play-Through (100%):          X%   esperado 1-5%

Top 5 por Hold Rate:
# | Anúncio | Thumbstop | Hook | Hold | Play-Through
```

Leitura obrigatória após a tabela: identificar qual etapa do funil é o gargalo principal (ex: Thumbstop ok + Hook baixo = hook não ativa Urgência Oculta nos primeiros 3 segundos).

Para imagens (`object_type = PHOTO`, `LINK` ou `CAROUSEL`): calcular apenas CTR e CPA/CPL. Thumbstop, Hook, Hold e Play-Through marcados como `—`.

### Bloco 3. CTAs por conversão (Q3)

Se dados de CTA estiverem disponíveis na API:
```
🖱️ CTA — performance comparada

| CTA             | Impressões | CTR   | ILC   | CPA     |
|-----------------|-----------|-------|-------|---------|
| Saiba Mais      | ...       | ...   | ...   | ...     |
| Compre Agora    | ...       | ...   | ...   | ...     |
| Cadastre-se     | ...       | ...   | ...   | ...     |

Vencedor: {CTA} — CPA R$ X, ILC X%
```

Se dados de CTA não estiverem disponíveis (limite de requisições ou breakdowns não suportados):
- Informar claramente e sugerir ação concreta: "Duplicar o winner atual trocando apenas o CTA duplicando entidade no Gerenciador (variando 1 dimensão)" com o CTA alternativo recomendado.
- Nunca deixar o bloco vazio sem a sugestão de ação.

Benchmark CPA: inferir do `perfil.md` conforme tabela de output [1] (low/mid/high ticket).

### Bloco 4. Fadiga Map (Q4)

Filtrar anúncios com `impressions > 50.000` e status ACTIVE. Score de fadiga 0 a 5:

| Sinal | Peso |
|---|---|
| Frequência >= 3.0 cold / >= 5.0 retarget | 1 |
| CTR caiu > 15% WoW | 1 |
| CPA subiu > 25% vs baseline | 1 |
| 2+ rankings below_average | 1 |
| CPA >= 2× baseline (crítico) | 2 |

Veredicto: `0` saudável / `1-2` monitorar / `3-4` substituir em breve / `5` pausar agora.

```
🔥 FADIGA MAP — criativos com +50k impressões

| Veredicto | Score | Anúncio | Freq | Impressões | CPA | Below Avg |
```

---

### Bloco 5. Textos com melhor engajamento (Q5)

Filtrar anúncios com `spend > R$ 100` no período, ordenar por CTR decrescente.

```
✍️ TOP TEXTOS POR CTR — spend > R$ 100

# | Anúncio | CTR | ILC | CPA | Tier
```

Leitura: identificar se CTR alto está convertendo (ILC alto + CPA real) ou apenas atraindo clique sem compra (CTR alto + ILC baixo + sem CPA).

---

### Extra A. Distribuição por Tier S/A/B/C/D

Aplicar fórmula de score composto da Análise 3.2 em todos os anúncios ativos:

**Para vídeos (peso dos componentes):**
- Hook Rate: 30% — (valor / 25%) × 30, máx 30
- Hold Rate: 20% — (valor / 40%) × 20, máx 20
- CTR: 25% — (valor / 1,5%) × 25, máx 25
- CPR invertido: 25% — (benchmark / valor) × 25, máx 25

**Para imagens (sem métricas de vídeo):**
- CTR: 40%
- CPR invertido: 35%
- Thumbstop: 25%

| Tier | Score | Diagnóstico | Ação |
|---|---|---|---|
| S | 85-100 | Top performer | Duplicar, escalar, criar variações |
| A | 70-84 | Sólido | Manter, monitorar fadiga |
| B | 55-69 | Médio | Testar novo CTA ou ângulo |
| C | 40-54 | Abaixo | Pausar em 7 dias se não melhorar |
| D | 0-39 | Não funciona | Pausar agora |

Entregar: distribuição numérica (N por tier) + gasto total em cada tier + alerta se Tier C ou D concentrar mais de 30% do budget.

---

### Extra B. DNA dos Winners

Para os top 3 por volume de conversões (com CPA real disponível):

```
🧬 DNA DOS WINNERS — top 3 por conversão

Tier | Formato | Anúncio | Spend | Compras | CPA | ROAS | Hook
```

Extrair o padrão comum: formato, estrutura do título, presença de número, tipo de promessa. Gerar briefing para próxima rodada criativa baseado na gramática vencedora.

---

## Protocolo padrão (obrigatório)

1. **Diagnóstico** — números brutos dos 5 blocos.
2. **Causa provável** — qual elemento VTSD está falhando ou performando bem (Hook Rate baixo = Urgência Oculta fraca no hook / Hold Rate alto = Decorados percebidos / CTR alto sem ILC = promessa do ad não alinhada com a página).
3. **No VTSD, isso significa…** — conexão explícita com o método:
   - Hook Rate < 25% = Urgência Oculta não está no primeiro segundo
   - Hold Rate < 40% = Decorados e Furadeira não estão sendo percebidos
   - CTR alto + ILC baixo = Identidade do Produto não está clara na página de destino
   - Tier C > 30% do budget = diversidade criativa baixa, só um perfil de Identidade do Consumidor sendo atingido
4. **Ação recomendada** — handoffs específicos.

---

## Mandala VTSD (referência para Gap Finder)

Após identificar tipos de criativos ativos, listar os ausentes e sugerir ângulo concreto para cada tipo faltante.

### Resposta 1. "Qual formato performa melhor: imagem estática, vídeo ou carrossel?"

Gap Finder: tipos ausentes = portas fechadas para perfis diferentes de Identidade do Consumidor.

---

## Handoffs típicos

| Achado | Para onde |
|---|---|
| Formato perdedor com gasto significativo | `/trafego-otimizar` (reduzir budget do formato) |
| Hook Rate < 25% | Duplicar entidade no Gerenciador (variando 1 dimensão) (ab-criativo: mesmo vídeo, hooks diferentes) + `/copy-anuncio` (reescrever abertura com Urgência Oculta mais forte) |
| Criativo Tier D ou Fadiga score >= 4 | `/trafego-otimizar` (pausar) |
| Winner com ROAS > 3x e freq < 3 | `/trafego-escalar` (vertical) + Duplicar entidade no Gerenciador (variando 1 dimensão) (duplicar variando CTA ou público) |
| Gap na Mandala (tipo ausente) | `/copy-anuncio` (criar anúncio no tipo faltante) |
| Budget > 30% em Tier C | `/trafego-otimizar` (redistribuição) |
