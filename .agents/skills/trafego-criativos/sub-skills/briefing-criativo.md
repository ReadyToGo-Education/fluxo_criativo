# Sub-skill. Briefing Criativo

Transforma os diagnósticos criativos em **briefings dos próximos testes**, prontos para produzir e testar. Cada briefing tem hipótese, variação, critério de sucesso e critério de morte, e aponta o tipo da Mandala e a skill que produz a peça.

**Esta sub-skill não produz o criativo.** Ela diz O QUE testar e por quê. A produção vai para as skills de criação do Severino (seção "Quem produz" abaixo) e o teste A/B para a `/trafego-testes`.

## Contexto multi-produto

Roda **por produto**. Cada produto pode precisar de testes diferentes (high ticket pode precisar de novo gancho, low ticket de nova oferta).

## Quando é acionado

- Opção [7] do menu principal.
- Automaticamente na Inteligência Completa (sexto e último módulo).
- Quando o aluno pergunta "que criativos devo testar agora?".

## Dados necessários

**Não busca dados novos.** Consome os resultados dos módulos anteriores:
- Diagnóstico criativo (módulo 4): veredictos por criativo.
- DNA criativo (módulo 5): fórmula vencedora, perfis e tipos da Mandala que vendem na conta.
- Leitura de atenção (módulo 1): perfis de atenção, pontos de queda.
- Intenção criativa (módulo 2): curiosidade vazia, mapa de intenção.
- Conversão criativa (módulo 3): falsos conversores, gap atenção-conversão.

Do `resumo-produto.md`: Quadro, Furadeira, Urgências Ocultas, Decorados principais e público (para ancorar cada hipótese em material real do produto).

Se rodado isoladamente (fora da completa), buscar as métricas mínimas para gerar um briefing básico.

## Quem produz (handoff de produção)

| O briefing pede | Skill que produz |
|---|---|
| Copy de anúncio (gancho + desenvolvimento + CTA) num tipo da Mandala | `/copy-anuncio` |
| Ganchos de um tipo específico da Mandala (12 ideias para escolher) | `/mandala-de-anuncios` |
| Peça em imagem (estático, feed ou stories) | `/criativo-estatico` |
| Vídeo novo com avatar | `/video-heygen` |
| Vídeo novo para Meta Ads (animado) | `/video-remotion` |
| Reaproveitar um vídeo que já existe (trocar só o gancho, cortar o meio, novo CTA no fim) | `/video-editar` |
| Rodar o A/B da peça nova contra a atual | `/trafego-testes` |

## Os 3 tipos de briefing

### Tipo 1: Briefing de novo gancho

Acionado quando: diagnóstico = `falha_gancho`, perfil `atencao_baixa` ou `falha_intencao` (inclui curiosidade vazia: CTR alto + visita à página baixa, onde a promessa do gancho precisa ser realinhada).

```
BRIEFING #1: NOVO GANCHO
Prioridade: ALTA (R$ {gasto_desperdicado}/dia em criativos com gancho fraco)

Problema detectado: {N} criativos com Hook Rate abaixo de 15%.
O público não para de rolar a tela nos primeiros 3 segundos.

Hipótese: o gancho atual não ativa uma Urgência Oculta. Não há
nada nos primeiros 2 segundos que faça o público parar.

Variação sugerida:
- Manter o corpo do vídeo (pode estar bom; ainda não sabemos)
- Trocar APENAS os primeiros 3 a 5 segundos
- Testar 2 abordagens:
  a) Abrir com uma afirmação direta sobre uma Urgência Oculta
     do resumo do produto (ex.: a Dor nº {N}: "{dor literal}")
  b) Abrir com um resultado concreto e real (número, antes e depois)
- Tipo da Mandala sugerido: {tipo que já vende na conta, segundo o DNA,
  ou um tipo ainda não testado que combine com a Urgência escolhida}

Métrica principal: Hook Rate (video_3sec_views / impressions)
Métrica secundária: Hold Rate (para garantir que o gancho novo
  não atrai curiosos que abandonam no meio)
Critério de sucesso: Hook Rate > 25% com 5.000+ impressões em 72h
Critério de morte: Hook Rate < 15% com 5.000+ impressões
Dados mínimos: 72h, 5.000 impressões por variação

Produção: /mandala-de-anuncios (ganchos do tipo sugerido) ou
/copy-anuncio; vídeo existente: /video-editar
Teste: /trafego-testes (A/B de criativo)
```

**Gancho sem pergunta:** pela regra de Light Copy do Severino, o gancho é uma afirmação (premissa), nunca uma pergunta. A sugestão de abertura segue isso.

### Tipo 2: Briefing de nova narrativa

Acionado quando: diagnóstico = `falha_sustentacao` ou perfil = `gancho_forte_dev_fraco`.

```
BRIEFING #2: NOVA NARRATIVA
Prioridade: MÉDIA (o gancho funciona, mas o público abandona no meio)

Problema detectado: criativos com Hook Rate > 25% mas Hold Rate < 30%.
O gancho prende, mas o desenvolvimento perde o público.

Hipótese: o conteúdo entre o gancho e o CTA não sustenta o interesse.
Pode ser explicação longa demais, falta da Furadeira ou ausência
de prova ou história.

Variação sugerida:
- Manter o gancho (funciona)
- Manter o CTA (se a conversão do final é boa)
- Reescrever o meio:
  a) Versão mais curta (cortar de 60s para 30s)
  b) Adicionar história real ou prova social no meio
  c) Mostrar a Furadeira do produto (as macroetapas do resumo)
     como o caminho que resolve a dor do gancho
- Tipo da Mandala sugerido para o meio: História, Explicação ou
  Demonstração, conforme o que o DNA mostrar que retém nesta conta

Métrica principal: Hold Rate (video_p50 / video_3sec)
Métrica secundária: Story Rate (p75/p25), para confirmar que
  a narrativa se sustenta até o final
Critério de sucesso: Hold Rate > 40% com 3.000+ p25 em 5 dias
Critério de morte: Hold Rate < 25% com 3.000+ p25
Dados mínimos: 5 dias, 3.000 visualizações p25

Produção: /video-editar (reeditar o meio), /video-remotion ou
/video-heygen (nova versão); roteiro: /copy-anuncio
Teste: /trafego-testes (A/B de criativo)
```

### Tipo 3: Briefing de nova oferta criativa

Acionado quando: diagnóstico = `falha_qualificacao` (tráfego qualificado chega mas não compra), ou quando o Click-to-LPV Rate é bom (> 60%) mas o Purchase Rate é ruim.

**NÃO acionar para `falha_intencao` com curiosidade vazia** (CTR alto + visita à página baixa). Nesse caso, o problema é a promessa do anúncio, não a oferta: usar o Tipo 1 (novo gancho com promessa mais qualificada).

**NÃO acionar para `falha_pos_clique`** (Offer Rate abaixo de 2%): o problema é a página ou a oferta, não o criativo. Encaminhar para `/trafego-oferta-funil`.

```
BRIEFING #3: NOVA ABORDAGEM DE OFERTA NO CRIATIVO
Prioridade: ALTA (há tráfego qualificado, mas ele não converte)

Problema detectado: CTR acima da média e Click-to-LPV Rate > 70%
(tráfego qualificado chega), mas CPA acima da meta.

Hipótese: o criativo gera interesse real, mas a ponte entre a
promessa do anúncio e a oferta da página está fraca, ou o CTA
não está claro.

Variação sugerida:
- Manter gancho e desenvolvimento (atenção e intenção funcionam)
- Trocar o CTA e/ou os últimos 5 segundos:
  a) CTA mais direto, com verbo e objeto concreto
  b) Ancoragem de preço no vídeo, com o preço real do resumo
  c) Prova social real no final (depoimento com resultado e prazo)
  d) Urgência real (prazo ou vagas que existem de verdade)
- Tipo da Mandala sugerido para o fechamento: Prova

Métrica principal: CPA (custo por venda)
Métrica secundária: CTR (para garantir que o CTA novo não
  afasta quem já clicava)
Critério de sucesso: CPA ≤ meta com 10+ conversões em 7 dias
Critério de morte: CPA > meta × 2 com 10+ conversões
Dados mínimos: 7 dias, 10 conversões por variação

Produção: /copy-anuncio (CTA e fechamento); vídeo existente: /video-editar
Teste: /trafego-testes (A/B de criativo ou de CTA)
```

## Priorização por impacto

Ordenar os briefings pelo potencial de melhoria:

```
Prioridade dos testes criativos:

#1 ALTO IMPACTO: novo gancho para "AD - Genérico - 60s"
   Gasto desperdiçado: R$ 45/dia (Hook Rate 8%)
   Potencial: se o Hook subir para 25%, economia de cerca de R$ 30/dia

#2 ALTO IMPACTO: gancho mais qualificado para "AD - Polêmica - 15s"
   Gasto em curiosidade vazia: R$ 60/dia (CTR alto, visita à página baixa, CPA 2× a meta)
   Potencial: trocar a promessa curiosa por uma promessa qualificada pode cortar o CPA em 40%

#3 MÉDIO IMPACTO: nova narrativa para "AD - Dor - 30s"
   O gancho funciona, o Hold está baixo
   Potencial: reter mais 20% do público até o CTA
```

Fórmula de prioridade: `impacto = gasto_diario × (1 - eficiencia_atual)`. Quanto mais gasta e menos eficiente, mais prioritário.

## Regras duras

1. **Nunca sugerir "faça um criativo melhor".** Vago demais. Sempre especificar O QUE mudar.
2. **Cada briefing muda UMA dimensão.** Mesmo princípio do `/trafego-testes`. Trocar gancho E CTA ao mesmo tempo não permite atribuir o resultado.
3. **Máximo de 3 briefings por sessão.** Foco vale mais que quantidade. Se há 5 problemas, priorizar os 3 de maior impacto.
4. **Se não há falha clara, sugerir variação do vencedor.** Expandir o que funciona (novo ângulo, novo tipo da Mandala, novo formato do mesmo vídeo).
5. **Cada briefing termina com a skill que produz e com o teste em `/trafego-testes`.**
6. **O briefing não produz a peça.** Ele diz o que testar; a peça sai das skills da tabela "Quem produz".
7. **Ancorar no produto real.** Toda hipótese cita material do `resumo-produto.md` (Urgência Oculta, Decorado, Furadeira ou objeção). Nada de dor genérica do nicho.
8. **Nada inventado.** Número, depoimento, prazo ou escassez só se forem reais. Sem dado real, o briefing pede o dado ao aluno.

## Texto de anúncio dentro do briefing (auto-revisão obrigatória)

Se o briefing trouxer qualquer texto pronto para ir ao ar (exemplo de gancho, headline, frase de CTA, legenda), esse texto é copy e segue a regra "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md antes de ser mostrado: aplicar o Manual da Copy (`.claude/skills/revisora/references/manual-copy.md`) e a skill `revisora`, corrigir direto no texto e entregar só a versão final, sem mencionar a revisão. Sem travessão, sem exclamação, gancho sem pergunta, sem "mesmo que" ou "sem precisar", e o produto não aparece no gancho.

Quando o briefing só descreve a direção ("abrir com uma afirmação direta sobre a Dor nº 3"), não é copy e não passa pela revisora.

## Explicação obrigatória

Cada briefing DEVE explicar em linguagem simples:

```
POR QUE ESSE TESTE?

Você está gastando R$ 45 por dia num criativo que 92% do
público ignora nos primeiros 3 segundos. Se o gancho melhorar,
esses mesmos R$ 45 podem trazer 3× mais atenção e,
potencialmente, mais vendas.

O teste custa pouco (mesma verba, versão nova) e dá resultado
rápido (72h). Se funcionar, você tem um criativo novo mais forte.
Se não funcionar, você eliminou uma hipótese e pode testar a
próxima.
```

## Output YAML

```yaml
briefing_criativo:
  produto: "Produto A"
  total_briefings: 3
  urgencia_criativa: alta

  briefings:
    - numero: 1
      tipo: novo_gancho | nova_narrativa | nova_oferta_criativa
      prioridade: alta | media | baixa
      impacto_estimado_dia_brl: 30.00
      ad_referencia: { id: "<id>", nome: "<nome>" }
      problema: "<diagnóstico em 1 frase>"
      hipotese: "<o que achamos que está errado>"
      ancora_no_produto: "<Urgência Oculta, Decorado ou etapa da Furadeira usada>"
      tipo_mandala_sugerido: "<nome do tipo, conforme mandala-de-anuncios>"
      variacao: "<o que mudar especificamente>"
      metrica_principal: "<nome>"
      metrica_secundaria: "<nome>"
      criterio_sucesso: "<condição>"
      criterio_morte: "<condição>"
      dados_minimos: "<tempo + volume>"
      producao: "/copy-anuncio | /mandala-de-anuncios | /criativo-estatico | /video-heygen | /video-remotion | /video-editar"
      teste: "/trafego-testes"
```
