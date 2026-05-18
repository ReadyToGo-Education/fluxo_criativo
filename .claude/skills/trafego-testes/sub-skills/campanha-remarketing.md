# Sub-fluxo. Campanha de Remarketing (Fluxo Composto)

Cria uma campanha de remarketing completa em um único fluxo. Orquestra `/trafego-publicos` (criar audience de remarketing) + `/trafego-criar-campanha` (campanha usando essa audience).

## Perguntas que cobre

- "Cria uma campanha de remarketing pra quem visitou o site nos últimos 30 dias"
- "Quero remarketing pros que abandonaram o carrinho"
- "Campanha pros engajados com vídeo que ainda não compraram"
- "Remarketing dos compradores antigos (upsell)"

## Fluxo composto

```
[1] Aluno define a audience-alvo (descritivo, ex: "carrinho abandonado 30d")
[2] Skill verifica se audience já existe (lista via /trafego-publicos)
    ├── Se SIM: usa a audience existente
    └── Se NÃO: aciona /trafego-publicos para criar
[3] Aluno define a oferta da campanha de remarketing (criativo + headline + cta + link)
[4] Aluno define budget e duração
[5] Skill aciona /trafego-criar-campanha com a audience da etapa 2
[6] Devolve campaign_id + audience_id + handoff para acompanhamento
```

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `descricao_audiencia` | obrigatório | Descrição livre. Ex: "visitantes 30d", "carrinho abandonado", "viu 50% do vídeo X" |
| `objective` | `OUTCOME_SALES` | ou `OUTCOME_LEADS` |
| `criativo_id` | obrigatório | Criativo da campanha de remarketing |
| `headline` | obrigatório | |
| `primary_text` | obrigatório | |
| `cta` | `LEARN_MORE` | |
| `budget_diario` | obrigatório | |
| `duracao_dias` | indefinido (ACTIVE) | |
| `excluir_compradores` | `true` | Excluir audience de compradores das últimas 90d (boa prática) |

## Receitas pré-configuradas

A skill oferece 5 receitas comuns:

### Receita R1. Carrinho abandonado
- Audience: `AddToCart 30d AND NOT Purchase 30d`
- Criativo sugerido: Mandala Tipo 7 (Garantia/Risco Reverso) ou Tipo 14 (Urgência)
- Headline sugerida: "Você esqueceu algo no seu carrinho"
- CTA: SHOP_NOW

### Receita R2. Visitantes do site
- Audience: `PageView 30d AND NOT Purchase 90d`
- Criativo: Mandala Tipo 1 (Apresentação) ou Tipo 5 (Autoridade)
- Headline: específica do produto
- CTA: LEARN_MORE

### Receita R3. Engajados com vídeo (não compradores)
- Audience: `Video50pct AND NOT Purchase 90d`
- Criativo: Tipo 16 (Depoimento) — eles já viram o conteúdo, agora prova social
- CTA: LEARN_MORE

### Receita R4. Upsell para compradores antigos
- Audience: `Purchase 90d to 365d` (compraram há mais de 90 dias)
- Criativo: anúncio de produto complementar ou de continuação
- CTA: SHOP_NOW

### Receita R5. Lead que não comprou
- Audience: `Lead 30d AND NOT Purchase`
- Criativo: oferta + escassez
- CTA: SIGN_UP ou SHOP_NOW

## Endpoint (orquestração)

```
# Passo A — verificar/criar audience
GET  /act_<id>/customaudiences            # listar
POST /act_<id>/customaudiences            # criar se não existir (via /trafego-publicos)

# Passo B — criar campanha
POST /act_<id>/campaigns
{
  "name": "[WS-RMK] {descricao}-{produto}",
  "objective": "OUTCOME_SALES",
  "status": "PAUSED"
}

POST /act_<id>/adsets
{
  "name": "[WS-RMK] adset-{descricao}-{produto}",
  "campaign_id": "<id>",
  "targeting": {
    "custom_audiences": [<audience_remarketing>],
    "excluded_custom_audiences": [<audience_compradores_90d>]   # boa prática
  },
  ...
}

POST /act_<id>/ads (com criativo da etapa 3)
```

## Preview YAML

```yaml
sub_fluxo: campanha_remarketing
nome_campanha: "[WS-RMK] carrinho-abandonado-curso-tarot"
receita: R1 (Carrinho abandonado)

audience_origem:
  status: criar (não existe)
  spec:
    nome: "[FC] CarrinhoAbandonado-30d-curso-tarot"
    inclusions: AddToCart 30d
    exclusions: Purchase 30d

audience_excluir: "[FC] Purchase-90d-curso-tarot" (já existe, ID 6123456789)

campanha:
  objective: OUTCOME_SALES
  optimization: PURCHASE
  budget_diario: 50 BRL
  duracao: indefinida (continua até pausar)

ad:
  criativo: imagem (Mandala Tipo 7 - Garantia)
  headline: "Você esqueceu algo no seu carrinho. Garantia de 7 dias incluída."
  primary_text: "..."
  cta: SHOP_NOW
  link: https://meusite.com/checkout

status_inicial: PAUSED

orquestracao:
  passo_1: criar_audience -> /trafego-publicos
  passo_2: criar_campanha -> /trafego-criar-campanha

confirma criar audience + campanha? (digite SIM)
```

## Após criar

```
✅ Audience criada: [FC] CarrinhoAbandonado-30d-curso-tarot
   ID: 6123456800

✅ Campanha de remarketing criada (PAUSED): [WS-RMK] carrinho-abandonado-curso-tarot
   Campaign ID: 9876543210
   Adset ID:    9876543211
   Ad ID:       9876543212

A audience leva ~24h para popular. A campanha pode ser ativada agora, mas vai entregar
muito pouco até a audience ter pelo menos ~500 pessoas.

Para ativar quando estiver pronta:
   POST /9876543210 { "status": "ACTIVE" }

Para acompanhar:
   /trafego-insights → campanha 9876543210
```

## Dicas VTSD

- **Excluir compradores recentes** (Purchase 90d) é prática padrão para evitar gastar com quem já comprou. Skill faz isso por default; aluno pode desativar.
- **Frequência alvo em remarketing**: 3 a 6 (mais alto que prospect porque a audience é menor e quente).
- **Janela curta** = audience pequena mas muito quente. **Janela longa** = audience maior mas mais fria.
- **Budget conservador**. Audiences pequenas saturam rápido. Começar com R$ 30-50/dia para audience de 5K-20K pessoas.
- **Criativo diferente do prospect**. Quem está em remarketing já viu seu anúncio principal. Use ângulo da Mandala diferente: prova social, urgência, garantia, oferta agressiva.

## Avisos

- **Audience nova (recém-criada) não popula instantaneamente.** Campanha sobe PAUSED. Aluno ativa em ~24h.
- **Mínimo de 1.000 pessoas** na audience para o algoritmo otimizar. Skill avisa se a estimativa é menor.
- **Audience muito pequena (< 500)** = preço por impressão sobe muito. Recomendado ampliar janela ou trocar evento.
- **Para o primeiro remarketing do produto**, recomendar começar com Receita R2 (visitantes) que tem audience maior, e depois R1 (carrinho).
