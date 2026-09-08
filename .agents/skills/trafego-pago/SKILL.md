---
name: trafego-pago
description: >
  Base de conhecimento para tráfego pago. estrutura de campanhas Meta Ads e Google Ads,
  métricas, pixel, API de conversão e otimização. Usado pelos commands /copy-anuncio e /estrategia-lancamento.
  Inclui segurança e boas práticas de investimento em mídia paga.
user-invocable: false
---

# Tráfego Pago. Base de Conhecimento

## Estrutura de Campanhas (VTSD)

### Meta Ads. 3 Campanhas Base

**Campanha 1. Descoberta (Topo de Funil):**
- Objetivo: Alcance ou Engajamento
- Público: Interesses amplos do nicho
- Criativos: Conteúdo de valor (educar, entreter)
- Orçamento: 20-30% do total
- Métrica principal: CPM e alcance

**Campanha 2. Conversão (Meio de Funil):**
- Objetivo: Conversões (cadastro ou venda)
- Público: Engajados (7-30 dias) + Lookalike de compradores
- Criativos: Anúncios focados em resultado
- Orçamento: 50-60% do total
- Métrica principal: CPA e taxa de conversão

**Campanha 3. Remarketing (Fundo de Funil):**
- Objetivo: Conversões
- Público: Visitantes do site (30-90 dias) + Carrinho abandonado
- Criativos: Urgência, prova social, objeções
- Orçamento: 10-20% do total
- Métrica principal: ROAS

### Google Ads. Rede de Pesquisa

- Campanhas por intenção de busca
- Palavras-chave: exata > frase > ampla
- Negativas obrigatórias: grátis, download, torrent, emprego

## Métricas e KPIs

| Métrica | O que é | Meta |
| --- | --- | --- |
| CPM | Custo por mil impressões | Quanto menor, melhor |
| CTR | Taxa de clique | > 5% |
| CPC | Custo por clique | R$1-5 (infoprodutos) |
| CPA | Custo por aquisição | Depende do ticket |
| ROAS | Retorno sobre investimento | > 3x |
| Taxa de Conversão (LP) | Cadastros/visitantes | 25-45% (captura) |
| Taxa de Conversão (Vendas) | Vendas/visitantes | 1-3% |

## Pixel e API de Conversão

**Pixel do Facebook:**
- Instalar na página de captura, vendas e obrigado
- Eventos: PageView, Lead, Purchase, AddToCart
- Usar domínio verificado

**API de Conversão (CAPI):**
- Complementa o Pixel (dados server-side)
- Mais precisa que Pixel sozinho
- Configurar via plataforma (Hotmart, Kiwify fazem automaticamente)

## Segurança em Tráfego Pago

- Começar com orçamento baixo e escalar gradualmente
- Nunca mexer em anúncios que estão dando resultado
- Duplicar conjuntos para testar (nunca editar o original)
- Manter 3-5 criativos ativos por conjunto
- Analisar resultados após 3-5 dias (nunca antes)
- Definir CPA máximo antes de começar

## Otimização

1. **Criativo não converte?** Teste novo gancho (primeiros 3 segundos)
2. **CTR baixo?** Problema no criativo ou segmentação
3. **CTR alto mas CPA alto?** Problema na landing page
4. **CPA subindo?** Fadiga de criativo. criar novos
