---
name: trafego-pago
description: >
  Base de conhecimento para tráfego pago. estrutura de campanhas Meta Ads e Google Ads,
  métricas, métricas derivadas de criativo, pixel, API de conversão, otimização e mapa das skills
  de tráfego do projeto. Usado pelos commands /copy-anuncio e /estrategia-lancamento e consultado
  pelas skills /trafego-* quando precisam de referência de estrutura, métricas e boas práticas.
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

## Métricas Derivadas de Inteligência Criativa

Métricas calculadas pelas skills do projeto (não são campos nativos da API):

| Métrica | Fórmula | Skill que calcula |
|---------|---------|-------------------|
| Hook Rate | video_3sec_views / impressions | `/trafego-criativos`, `/trafego-analise` [3] |
| Hold Rate | video_p50_watched / video_3sec_views | `/trafego-criativos`, `/trafego-analise` [3] |
| Story Rate | video_p75_watched / video_p25_watched | `/trafego-criativos` |
| Completion Rate | video_p95_watched / video_plays | `/trafego-criativos` |
| Cost per Hook | spend / video_3sec_views | `/trafego-criativos` |
| Cost per Hold | spend / video_p50_watched | `/trafego-criativos` |
| Intent Rate | landing_page_views / video_3sec_views | `/trafego-criativos` |
| Click-to-LPV Rate | landing_page_views / inline_link_clicks | `/trafego-criativos` |
| Offer Rate | (leads ou initiate_checkout) / landing_page_views | `/trafego-criativos` |
| Purchase Rate | purchases / landing_page_views | `/trafego-criativos` |
| Creative Conversion Rate | purchases / video_3sec_views | `/trafego-criativos` |
| Connect Rate | lp_views / link_clicks | `/trafego-insights` |

## Pixel e API de Conversão

**Pixel do Facebook:**
- Instalar na página de captura, vendas e obrigado (páginas feitas no projeto: `/pagina-pixel`)
- Eventos: PageView, Lead, Purchase, AddToCart
- Usar domínio verificado
- Diagnóstico de pixel e eventos na conta: `/trafego-pixel`

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
3. **CTR alto mas CPA alto?** Possível curiosidade vazia: o anúncio atrai clique de quem não compra. Verificar Click-to-LPV Rate e Offer Rate antes de culpar a página
4. **CPA subindo?** Fadiga de criativo. Criar novos (`/copy-anuncio`, `/criativo-estatico`)
5. **CTR baixo mas CPA bom?** Criativo qualificado: filtra o público antes do clique. Não cortar por CTR baixo

## Mapa das Skills de Tráfego do Projeto

| Skill | Função |
|-------|--------|
| `/trafego-conexao` | Conectar a conta Meta ao Claude (conector MCP recomendado, App de reserva) |
| `/trafego-criar-campanha` | Subir campanha Sales/Leads, sempre pausada e com preview |
| `/trafego-insights` | Fonte única de dados e métricas derivadas |
| `/trafego-analise` | Análise narrada VTSD com menu de outputs |
| `/trafego-dashboard` | Painel da conta de anúncios, com vendas do checkout quando configurado |
| `/trafego-otimizar` | Diagnóstico operacional e ajustes da campanha |
| `/trafego-escalar` | Escala controlada (acionada pelo otimizar quando a campanha está pronta) |
| `/trafego-diagnostico` | Investigação estratégica: hipóteses, falso vencedor, auditoria estrutural, score de confiança |
| `/trafego-criativos` | Inteligência criativa: atenção, intenção e conversão, briefing de testes |
| `/trafego-oferta-funil` | Diagnóstico pós-clique: página, congruência copy e página, oferta e checkout |
| `/trafego-publicos` | Criar e gerenciar públicos (inclui lookalike) |
| `/trafego-regras` | Automações e agendamento |
| `/trafego-testes` | Testes A/B disciplinados |
| `/trafego-pixel` | Diagnóstico de pixels e eventos |

Low ticket com planilha do Gerenciador: `/lt-otimizar`. Relatório diário por WhatsApp ou Telegram: `/ads-relatorio`.
