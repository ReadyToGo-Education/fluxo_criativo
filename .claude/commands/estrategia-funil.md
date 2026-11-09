---
name: workshop-marketing:estrategia-funil
description: Mapear funil de vendas completo. perpétuo ou lançamento. Inclui touchpoints, páginas, emails, anúncios e métricas. Baseado na estrutura de campanha VTSD.
---

# Funil de Vendas. Mapeamento Completo

Mapeia funil perpétuo ou de lançamento com todos os touchpoints.

## Usage

```
/estrategia-funil
```

## O Que Fazer

### 1. Contexto
Leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md).

### 2. Entrevista (UMA pergunta por vez, com progresso visual)

**Bloco 1/4. Tipo de Funil:**
```
Qual tipo de funil?

1. Perpétuo (vende todo dia no automático)
2. Lançamento (evento + abertura e fechamento de carrinho)
3. Low Ticket low ticket (quiz + oferta de entrada R$37-97)

Digite o número:
```

```
--- Bloco 1/4 concluído ---
Funil: [tipo escolhido]
Próximo: Produto
---
```

**Bloco 2/4. Produto:**
```
Qual o produto principal e o preço?
(ex: "Curso de inglês, R$497", "Mentoria, R$3.000")
```

```
--- Bloco 2/4 concluído ---
Funil: [tipo]
Produto: [nome] | Preço: R$ [valor]
Próximo: Isca digital
---
```

**Bloco 3/4. Isca Digital:**
```
Tem isca digital? Qual?

1. E-book
2. Aula gratuita
3. Checklist/planilha
4. Mini-curso
5. Não tenho isca ainda

Digite o número (ou descreva):
```

```
--- Bloco 3/4 concluído ---
Funil: [tipo]
Produto: [nome] | R$ [valor]
Isca: [isca]
Próximo: Ofertas complementares
---
```

**Bloco 4/4. Ofertas Complementares:**
```
Tem produtos de entrada (low ticket) ou upsell?
(ex: "E-book de R$47 como entrada", "Mentoria VIP de R$2k como upsell")
Se não tiver, digite "não".
```

**Confirmação antes de gerar:**
```
Resumo do funil:
- Tipo: [tipo de funil]
- Produto principal: [nome] | R$ [valor]
- Isca: [isca digital]
- Upsell/Low ticket: [ofertas complementares ou nenhum]

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 3. Geração

**Funil Perpétuo:**
```
Anúncio → Página de Captura → Isca Digital → Sequência de Emails → Página de Vendas → Checkout
                                                    ↓                                      ↓
                                              Remarketing → Página de Vendas          Order Bump
                                                                                           ↓
                                                                                       Upsell
                                                                                           ↓
                                                                                    (não comprou)
                                                                                           ↓
                                                                                      Downsell
```
- Detalhar cada etapa com métricas esperadas

**Funil de Lançamento:**
```
Anúncio → Página do Evento → Sequência Pré-Evento → Evento → Pitch → Carrinho Aberto → Checkout
                                                                           ↓                  ↓
                                                                    Remarketing + Emails   Upsell
```

**Funil low ticket (Low Ticket):**
```
Anúncio → Quiz → Página Final do Quiz (12 blocos) → Checkout Low Ticket → Upsell
                                                                              ↓
                                                                        (não comprou)
                                                                              ↓
                                                                          Downsell
```
- Para criar a página final do quiz, use `/lt-funil`

### 4. Mapear Ofertas Complementares (Módulo 7 VTSD)

Para TODOS os tipos de funil, pergunte e defina:

**Upsell (oferta pós-compra):**
- "Tem algo que complementa o produto principal e acelera o resultado?"
- Deve ser oferta que só faz sentido após a compra
- Preço sugerido: 30-50% do produto principal
- Apresentar imediatamente após a confirmação de compra

**Order Bump (impulso no checkout):**
- "Tem algo rápido e barato que pode adicionar no checkout?"
- Produto simples, baixo preço, decisão por impulso
- Preço sugerido: R$17-47
- Exemplos: checklist, template, planilha, acesso a grupo

**Downsell (oferta para quem não comprou):**
- "Se a pessoa não comprar, o que ofereceria como alternativa menor?"
- Produto mais acessível que mantém o relacionamento
- Preço sugerido: 20-30% do produto principal
- Apresentar na página de saída ou por email após abandono

Incluir no documento do funil:
- Nome e preço de cada oferta complementar
- Onde cada uma aparece no fluxo
- Métricas esperadas (taxa de conversão de upsell: 10-20%, order bump: 5-15%)

### 5. Salvar
`meus-produtos/{ativo}/entregas/textos-de-venda/funil-[tipo]-[produto].md`

### 6. Próximo Passo
"Funil mapeado com ofertas complementares. Comece criando os materiais: `/copy-pagina` para as páginas e `/copy-anuncio` para os anúncios."
