# Sub-skill. Plano de Correção do Funil

Transforma os diagnósticos em plano de ação priorizado, com briefings de teste de página. Equivalente ao `briefing-criativo` da `/trafego-criativos`, mas para página e oferta. Cada briefing termina apontando a skill do Severino que executa a correção (esta skill não modifica páginas nem escreve copy nova).

## Quando é acionado

- Opção [7] do menu principal
- Automaticamente no Diagnóstico Completo (sexto e último módulo)
- Quando o aluno pergunta "o que testar na página?" ou "como melhorar o funil?"

## Dados necessários

Consome resultados dos módulos anteriores (não busca dados novos):
- Etapa de quebra do funil (módulo 1)
- Elementos da página (módulo 2)
- Score de congruência (módulo 3)
- Score de oferta + checklist (módulo 4)
- Diagnóstico de checkout (módulo 5)

## Os 4 tipos de briefing de página

### Tipo 1: Briefing de primeira dobra

Acionado quando: etapa de quebra é LPV→Lead/ATC (visitante chega mas não engaja) OU score de congruência < 50 OU headline genérica no checklist.

```
BRIEFING #1: NOVA PRIMEIRA DOBRA
Prioridade: ALTA (R$ {gap_diario}/dia em visitas que não engajam)

Problema: {etapa de quebra + pontuação do elemento}
Ex: "92% das visitas saem sem engajar. A headline atual é
genérica e desalinhada com a promessa do anúncio."

Hipótese: a primeira dobra não sustenta a expectativa criada
pelo anúncio. Visitante chega, não reconhece a promessa, sai.

Teste recomendado:
- Nova headline alinhada com a promessa do anúncio top
- Subheadline com especificidade (número, prazo, resultado)
- Prova social acima do primeiro CTA
- CTA com texto mais direto

Métrica principal: taxa de cadastro ou carrinho (das visitas à página)
Critério de sucesso: aumento de 20% ou mais na taxa de visita à página → cadastro
Critério de morte: nenhuma melhoria depois de 500 visitas à página (coluna "Visualizações da página de destino" no Gerenciador)
Dados mínimos: 7 dias, 500 visitas à página na versão teste

Execução: /pagina-ajuste (página feita no Severino) ou a auditoria
do /feedback-pagina (/feedback-low-ticket em low ticket). Copy nova
da primeira dobra: /copy-pagina ou /lt-pagina.
```

### Tipo 2: Briefing de prova e oferta

Acionado quando: etapa de quebra é Lead→Checkout (interesse sem decisão) OU score de oferta < 60 OU prova posicionada depois do preço.

```
BRIEFING #2: REFORÇAR PROVA E OFERTA
Prioridade: {alta | media}

Problema: {checklist items com menor pontuação}
Ex: "3 depoimentos em texto sem foto, posicionados DEPOIS
do preço. Garantia de 7 dias condicional. Sem FAQ."

Hipótese: o visitante entende a promessa, mas não tem confiança
suficiente para agir. Falta prova social antes da decisão.

Teste recomendado:
- Mover depoimentos para ANTES do preço
- Adicionar foto/vídeo nos depoimentos
- Ampliar garantia para 30 dias incondicional
- Adicionar FAQ com as 5 objeções principais
- Reforçar ancoragem de preço

Métrica principal: taxa cadastro ou carrinho → checkout iniciado
Critério de sucesso: aumento de 15% ou mais na taxa
Critério de morte: nenhuma melhoria depois de 200 cadastros ou carrinhos

Execução: /feedback-pagina (/feedback-low-ticket em low ticket) para
prova, garantia e FAQ; as 5 objeções do resumo do produto são a base
do FAQ. Bloco pontual numa página do Severino: /pagina-ajuste.
```

### Tipo 3: Briefing de checkout

Acionado quando: diagnóstico de checkout = `friccao_provavel` ou `queda_abrupta`.

```
BRIEFING #3: REDUZIR FRICÇÃO NO CHECKOUT
Prioridade: ALTA (tráfego qualificado chega e abandona na última etapa)

Problema: conclusão de checkout (compras ÷ checkouts iniciados) de {X}% (bem abaixo do piso da faixa do ticket, seção 3.5 do SKILL.md; só aciona este briefing se for fricção real, não a queda natural do preço alto)

Hipótese: fricção na etapa final impede a conclusão da compra.

Teste recomendado (verificar na plataforma):
- Adicionar Pix como opção (se não tem)
- Simplificar formulário (menos campos)
- Adicionar selos de segurança no checkout
- Testar bump de valor menor (reduz percepção de risco)
- Verificar se checkout mobile funciona bem

Métrica principal: conclusão de checkout (compras ÷ checkouts iniciados)
Critério de sucesso: a taxa volta para dentro da faixa do ticket (seção 3.5 do SKILL.md)
Critério de morte: taxa não melhora depois de 50 checkouts iniciados

⚠️ Esta ação é FORA do Meta. A skill não modifica checkout.
Execução: /pagina-checkout (ligação da página com o checkout) e
os ajustes de pagamento direto na plataforma (Hotmart, Kiwify, Stripe).
```

### Tipo 4: Briefing técnico (connect rate)

Acionado quando: connect rate abaixo de 70% (clique acontece mas visitante não chega na página; abaixo de 70%, a primeira hipótese é técnica, seção 3.5 do SKILL.md) OU leitura da página detecta redirect/erro.

```
BRIEFING #4: RESOLVER PROBLEMA TÉCNICO DE ACESSO
Prioridade: ALTA (tráfego está sendo pago mas não chega na página)

Problema: connect rate de {X}% ({Y}% do tráfego pago não
chega na página).

Hipótese: problema técnico entre o clique e a página. Pode ser:
redirect lento, URL errada, página fora do ar intermitente,
ou carregamento muito lento em mobile.

Verificações recomendadas:
- Testar a URL do anúncio manualmente (clicar e cronometrar)
- Testar em mobile (Wi-Fi e 4G)
- Verificar se há redirects (301, 302) com ferramentas online
- Verificar se a página está online 24h (monitoramento)
- Conferir se o link no criativo é o correto

Métrica principal: connect rate (visitas à página ÷ cliques no link)
Critério de sucesso: connect rate sobe para 80% ou mais (faixa saudável, seção 3.5 do SKILL.md)
Critério de morte: nenhuma melhoria após corrigir o técnico

⚠️ Esta ação é FORA do Meta. Execução: /pagina-performance (velocidade
e peso da página) e conferência do link e da hospedagem.
```

---

## Priorização por impacto

Ordenar briefings pelo gap no funil:

```
Prioridade de correções no funil:

#1 ALTA: Nova primeira dobra
   Perda: visita à página → cadastro (92% de perda, R$ 328/dia desperdiçados)
   Potencial: se a taxa de cadastro subir de 8% para 15%, CPA cai ~47%

#2 MÉDIA: Reforçar prova e oferta
   Perda: cadastro → checkout iniciado (80% de perda)
   Potencial: mais confiança → mais decisões de compra

#3 ALTA: Reduzir fricção checkout
   Perda: conclusão de checkout (compras ÷ checkouts iniciados) caiu de 40% para 26%
   Potencial: recuperar 14 pontos de conversão = ~5 vendas/semana
```

**Fórmula de prioridade:** `impacto = volume_na_etapa × taxa_perda × custo_por_unidade`. Quanto mais gente perde e mais caro, mais prioritário.

## Regras duras

1. **Nunca sugerir "faça uma página melhor."** Vago. Sempre especificar O QUE mudar.
2. **Cada briefing muda UMA dimensão.** Trocar headline E preço E garantia ao mesmo tempo não permite atribuir resultado.
3. **Máximo 3 briefings por sessão.**
4. **Se funil está saudável, sugerir otimização incremental** (não revolução).
5. **A skill NÃO modifica páginas.** Toda mudança passa pela skill de correção indicada no briefing (ou pela edição do próprio aluno).
6. **A skill não escreve copy nova.** O briefing diz O QUE mudar; a copy nova sai de `/pagina-ajuste`, `/feedback-pagina`, `/feedback-low-ticket`, `/copy-pagina` ou `/lt-pagina`.

## Explicação obrigatória

```
POR QUE ESSE TESTE?

Você está gastando R$ 357 por dia em tráfego. Dessas visitas,
92% vão embora na primeira dobra da página. Se a headline
estiver mais alinhada com o anúncio e tiver prova antes do
CTA, a taxa de engajamento pode dobrar.

O teste custa zero (só mudar texto na página) e dá resultado
em 7 dias com 500 visitas. Se funcionar, seu CPA pode cair
quase pela metade.
```

## Output YAML

```yaml
plano_correcao_funil:
  total_briefings: 3
  urgencia_funil: alta

  briefings:
    - numero: 1
      tipo: primeira_dobra | prova_oferta | checkout | tecnico_connect
      prioridade: alta | media | baixa
      gap_diario_brl: 328.00
      etapa_quebra: "lpv_to_lead"
      problema: "92% das visitas saem sem engajar"
      hipotese: "Primeira dobra não sustenta expectativa do anúncio"
      teste: "Nova headline alinhada + prova antes do CTA"
      metrica_principal: "taxa de cadastro"
      criterio_sucesso: "+20% na taxa de visita à página → cadastro"
      criterio_morte: "Nenhuma melhoria depois de 500 visitas à página"
      dados_minimos: "7 dias, 500 visitas à página"
      execucao: "/pagina-ajuste | /feedback-pagina | /feedback-low-ticket | /copy-pagina | /lt-pagina | /pagina-checkout | /pagina-performance"
```
