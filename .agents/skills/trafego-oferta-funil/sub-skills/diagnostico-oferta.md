# Sub-skill. Diagnóstico de Oferta

Avalia a força da oferta usando os elementos extraídos da página + as métricas de conversão. Checklist pontuado (0 a 100) com integração VTSD, usando o Quadro e a Furadeira reais do `resumo-produto.md`.

**Diagnóstico a partir dos números, não auditoria de copy.** A nota responde "a estrutura da oferta explica a conversão que os números mostram?". Ela não substitui o `/feedback-pagina` (ou o `/feedback-low-ticket`, em página low ticket), que faz a revisão completa de copy, estrutura 8D e design. Quando a nota ou o cruzamento apontar a oferta como causa provável, o próximo passo é a auditoria completa numa dessas duas skills.

## Quando é acionado

- Opção [5] do menu principal
- Automaticamente no Diagnóstico Completo (quarto módulo)
- Quando o aluno pergunta "a oferta é forte?" ou "por que a página não converte?"

## Dados necessários

- Elementos da página extraídos no módulo 2 (leitura da página)
- Métricas pós-clique do módulo 1 (conversão da página, Offer Rate)
- Score de congruência do módulo 3 (se desalinhamento foi detectado)

## Checklist de força da oferta (score 0-100)

| # | Elemento | Peso | 0 pts | Parcial | Máximo |
|---|----------|------|-------|---------|--------|
| 1 | **Clareza da promessa** | 15 | Genérica ("aprenda X") | Direcional ("consiga Y") | Específica e mensurável ("R$ X em Y dias") |
| 2 | **Mecanismo único** | 10 | Sem mecanismo | Método mencionado sem detalhe | Método nomeado, diferenciado, explicado |
| 3 | **Prova antes do CTA** | 15 | Sem prova | Prova presente, mas após o preço | Depoimentos/números ANTES do primeiro CTA |
| 4 | **Garantia** | 10 | Sem garantia | Garantia curta ou condicional | 30+ dias incondicional, visível |
| 5 | **Bônus** | 5 | Sem bônus ou genéricos | Bônus presentes | Bônus resolvem objeções específicas |
| 6 | **Ancoragem de preço** | 10 | Preço solto, sem referência | "De X por Y" | Ancoragem clara com valor percebido alto |
| 7 | **CTA** | 10 | Sem CTA ou genérico | CTA presente | CTA claro, urgente, múltiplos na página |
| 8 | **Urgência/escassez** | 5 | Sem urgência | Urgência genérica ("últimas vagas") | Urgência real e contextualizada |
| 9 | **FAQ/objeções** | 10 | Sem FAQ | FAQ presente mas superficial | Principais objeções respondidas com profundidade |
| 10 | **Estrutura** | 10 | Caótica ou muito curta | Ordem razoável | Fluxo lógico: problema → solução → prova → oferta → garantia → CTA |

## Integração VTSD no checklist

A régua é o produto real: Quadro, Furadeira, objeções e Urgências Ocultas lidos do `resumo-produto.md`.

| Elemento | Conceito VTSD | Avaliação VTSD |
|----------|---------------|----------------|
| Promessa | **Quadro na Parede** | A promessa da página é o Quadro registrado no resumo (literal ou fiel a ele)? O resultado é visual? O aluno se vê naquele quadro, ou é abstrato? |
| Mecanismo | **Furadeira** | A página apresenta a Furadeira do resumo (nome e macroetapas)? Está claro que é essa ferramenta que entrega o Quadro? |
| Prova | **Decorados** | Os depoimentos mostram transformação (Decorados) ou features? São pessoas parecidas com o público? |
| Urgência | **Urgência Oculta** | A urgência está conectada a uma Urgência Oculta do resumo (o custo de NÃO agir, a dor que continua) ou é contador falso? |
| CTA | **Identidade do Consumidor** | O CTA fala para a pessoa certa? Usa a linguagem do público-alvo? |
| Bônus | **Caixa Rápido** | Os bônus entregam resultado rápido (Caixa Rápido) ou são "PDF que ninguém lê"? |
| FAQ | **Objeções** | O FAQ responde às objeções principais do resumo, com argumento, ou só a dúvidas operacionais? |

**Regra:** a tradução VTSD complementa a leitura estrutural. Primeiro o elemento e a nota, depois a leitura pelo método.

## Regra de pontuação parcial

Cada elemento tem 3 faixas: **0** (ausente ou ruim), **metade do peso** (presente mas fraco) e **peso total** (forte). Não inventar valores intermediários.

Exemplo: Clareza da promessa (peso 15) → 0, 7 ou 15. Garantia (peso 10) → 0, 5 ou 10.

---

## Cruzamento com métricas

| Score oferta | Conversão página | Diagnóstico |
|-------------|-----------------|-------------|
| Alto (80+) | Alta | Oferta e tráfego alinhados. Funil saudável. |
| Alto (80+) | Baixa | Problema NÃO é a oferta. Investigar preço, público, checkout ou tráfego. |
| Razoável (50 a 79) | Baixa | Oferta é causa provável parcial. Priorizar os elementos de maior peso com nota baixa e seguir para a auditoria no `/feedback-pagina` (`/feedback-low-ticket` em página low ticket). |
| Razoável (50 a 79) | Alta | Oferta sustenta a conversão, mas tem pontos fracos. Melhorar os elementos de maior peso pode ampliar o resultado; não é a prioridade do funil. |
| Baixo (< 50) | Baixa | **Oferta é a causa provável.** Prioridade: melhorar os elementos com menor pontuação. |
| Baixo (< 50) | Alta | Oferta fraca mas converte (público muito qualificado). Melhorar oferta pode ampliar resultado. |

## Explicação obrigatória

> **Regra dura (seção 12 do SKILL.md): o gráfico de notas NUNCA sai sozinho.** Sempre acompanhado de uma tabela `Elemento | Nota | Por que essa nota`, justificando cada pontuação do checklist (por que essa nota, o que tirou pontos), no chat e no HTML. Sem isso, a pessoa vê "Furadeira 80" e não entende o que é nem por quê. Fechar com o lembrete: as notas cobrem só o que foi lido da página (texto), não o vídeo/VSL; e são leitura estrutural cruzada com os números, não a auditoria de copy (essa é do `/feedback-pagina`).

Cada elemento DEVE ter explicação por faixa:

### Score alto (80-100)
```
FORÇA DA OFERTA: {score}/100 (FORTE)

A página tem os elementos principais bem construídos.
Destaque: {2-3 elementos com pontuação máxima}.

Se a conversão da página é baixa MESMO com oferta forte,
o problema provavelmente está em: preço (acima do que o
público está disposto a pagar), público errado (tráfego não
qualificado), ou checkout (fricção no pagamento).
```

### Score médio (50-79)
```
FORÇA DA OFERTA: {score}/100 (RAZOÁVEL)

A oferta tem base, mas {N} elementos estão fracos:
- {elemento 1}: {pontuação}/{peso}. {problema específico}
- {elemento 2}: {pontuação}/{peso}. {problema específico}

Prioridade de melhoria (maior impacto primeiro):
1. {elemento com maior peso e menor pontuação}
2. {segundo}
```

### Score baixo (0-49)
```
FORÇA DA OFERTA: {score}/100 (FRACA)

A oferta tem problemas estruturais que provavelmente estão
impedindo a conversão. Mesmo com tráfego qualificado, a
página não sustenta a intenção gerada pelo anúncio.

Problemas críticos:
- {elementos com 0 pontos, em ordem de peso}

O que NÃO fazer: NÃO escalar tráfego com oferta fraca.
Mais verba = mais visitas que não convertem = mais dinheiro
desperdiçado.

Próximo passo: auditoria completa da página no /feedback-pagina
(/feedback-low-ticket em página low ticket).
```

## Output YAML

```yaml
diagnostico_oferta:
  score: 55
  faixa: razoavel

  checklist:
    - elemento: clareza_promessa
      peso: 15
      pontos: 7
      avaliacao: "Promessa direcional. 'Venda todo dia' sem o resultado mensurável do Quadro."
      vtsd: "Quadro na Parede fraco. A página não usa o Quadro do resumo; o aluno não se vê no resultado."
    - elemento: mecanismo
      peso: 10
      pontos: 10
      avaliacao: "Método nomeado e diferenciado. Bom."
    # ...

  cruzamento:
    score_oferta: razoavel
    conversao_pagina: baixa
    diagnostico: "Oferta é causa provável parcial. Priorizar clareza da promessa e prova."
    proximo_passo: "/feedback-pagina"

  prioridade_melhoria:
    - { elemento: "clareza_promessa", peso: 15, pontos: 7, gap: 8 }
    - { elemento: "prova_antes_cta", peso: 15, pontos: 0, gap: 15 }
```
