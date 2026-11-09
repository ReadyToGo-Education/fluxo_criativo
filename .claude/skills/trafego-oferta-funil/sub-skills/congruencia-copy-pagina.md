# Sub-skill. Congruência Copy-Página

Compara o que o anúncio promete com o que a página entrega. Detecta desalinhamento de expectativa, que é uma das maiores causas de CPA alto com CTR bom. **Genuinamente novo:** nenhuma skill cruza texto do anúncio com conteúdo da página.

## Quando é acionado

- Opção [4] do menu principal
- Automaticamente no Diagnóstico Completo (terceiro módulo)
- Quando o aluno pergunta "o anúncio e a página estão alinhados?"

## Fontes de dados

1. **Texto do anúncio:** via API, só leitura (MCP: `ads_get_creatives`; App: `curl -g` em `creative{object_story_spec,asset_feed_spec}`; campos na seção 5 do SKILL.md)
2. **Texto da página:** extraído no módulo 2 (leitura da página)
3. **Métricas pós-clique:** consumidas do módulo 1

## Dimensões de congruência

Avaliar 5 dimensões:

| Dimensão | O que compara | Congruente se... | Desalinhado se... |
|----------|--------------|------------------|-------------------|
| **Promessa** | Headline/primary text do ad vs headline da página | Mesmo resultado prometido | Ad promete X, página fala de Y |
| **Tom/linguagem** | Nível de formalidade, energia, urgência | Consistente entre ad e página | Ad informal/urgente, página formal/institucional |
| **Especificidade** | Nível de detalhe da promessa | Mesmo grau de especificidade | Ad específico ("R$ 47k em 30 dias"), página genérica ("aprenda a vender") |
| **CTA** | O que o ad pede vs o que a página pede | Ad prepara para a ação da página | Ad diz "Saiba Mais", página pede "Compre Agora" (salto de intenção) |
| **Público-alvo** | Para quem o ad fala vs para quem a página fala | Mesmo perfil | Ad fala para iniciantes, página para avançados |

## Score de congruência (0-100)

Cada dimensão vale 20 pontos:

| Pontuação | Significado |
|-----------|-------------|
| 20 | Totalmente alinhado |
| 10 | Parcialmente alinhado (mesma direção, diferente grau) |
| 0 | Desalinhado |

Score total: soma das 5 dimensões.

| Faixa | Score | Significado |
|-------|-------|-------------|
| `congruente` | 80-100 | Anúncio e página contam a mesma história |
| `parcial` | 50-79 | Direção similar, detalhes divergem |
| `desalinhado` | 0-49 | Anúncio cria expectativa que a página não atende |

## Cruzamento com métricas

| Congruência | Conversão página | Diagnóstico provável |
|-------------|-----------------|---------------------|
| Alta | Alta | Funil funcional. Oferta e tráfego alinhados. |
| Alta | Baixa | Problema na oferta (preço, prova, checkout), não no alinhamento. |
| Baixa | Alta | Página forte apesar do desalinhamento (raro, pode mascarar problema futuro). |
| Baixa | Baixa | **Causa provável encontrada:** desalinhamento de expectativa. Prioridade alta. |

## Quando o criativo é vídeo

Se o criativo principal é vídeo e não há transcrição:
- Avaliar congruência apenas com campos textuais (primary_text, headline, description)
- Declarar: "Congruência avaliada com campos textuais do anúncio. O vídeo pode ter promessas adicionais não analisadas."
- Reduzir confiança do score de congruência

Se o nome do anúncio/campanha contiver pistas (ex: "AD - Dor - Vídeo 30s"), usar como contexto auxiliar (com cautela).

## Explicação obrigatória

```
CONGRUÊNCIA COPY-PÁGINA: score 40/100 (DESALINHADO)

PROMESSA (0/20):
- Anúncio: "O método que gerou R$ 47k em 30 dias"
- Página: "Aprenda a vender todos os dias usando IA"
- Problema: o anúncio promete resultado específico e mensurável.
  A página abre com promessa genérica. Quem clicou esperando
  "R$ 47k em 30 dias" encontra "aprenda a vender": quebra de
  expectativa imediata.

TOM (10/20):
- Anúncio: urgente, direto, com número
- Página: educativa, explicativa
- Parcialmente alinhado: mesma direção, energia diferente.

ESPECIFICIDADE (0/20):
- Anúncio: ultra-específico (R$ 47k, 30 dias, método)
- Página: genérica (vender, IA, todos os dias)
- Quem clicou por especificidade encontra generalidade.

O QUE FAZER:
Alinhar a headline da página com a promessa do anúncio
(e com o Quadro do resumo do produto). A headline nova sai
do /pagina-ajuste (página feita no Severino) ou da auditoria
do /feedback-pagina (/feedback-low-ticket em low ticket).
Esta skill aponta o desalinhamento; não escreve a copy nova.
```

## Output YAML

```yaml
congruencia_copy_pagina:
  score: 40
  faixa: desalinhado

  anuncio:
    primary_text: "..."
    headline: "..."
    description: "..."
    cta: "Saiba Mais"
    link: "https://..."

  pagina:
    headline: "..."
    subheadline: "..."
    cta: "..."

  dimensoes:
    promessa: { pontos: 0, ad: "...", pagina: "...", problema: "..." }
    tom: { pontos: 10, ad: "urgente", pagina: "educativa" }
    especificidade: { pontos: 0, ad: "ultra-específico", pagina: "genérica" }
    cta: { pontos: 10, ad: "Saiba Mais", pagina: "Quero Começar" }
    publico: { pontos: 20, ad: "empreendedor digital", pagina: "empreendedor digital" }

  cruzamento_metricas:
    congruencia: desalinhado
    conversao_pagina: baixa
    diagnostico: "Causa provável: desalinhamento de expectativa"

  confianca: alta | media | baixa
  limitacao_video: true | false
```
