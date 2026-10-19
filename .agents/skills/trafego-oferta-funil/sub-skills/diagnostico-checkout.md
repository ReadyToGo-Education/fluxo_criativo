# Sub-skill. Diagnóstico de Checkout

Usa eventos atribuídos pela Meta para identificar possível quebra na etapa final de conversão. Opera com a limitação dura de não ter acesso ao backend (gateway de pagamento, Pix, boleto, cartão).

## Quando é acionado

- Opção [6] do menu principal
- Automaticamente no Diagnóstico Completo (quinto módulo)
- Quando o aluno pergunta "checkout está quebrando?" ou "pessoa chega mas não compra"

## Dados necessários

Consumir via `/trafego-insights`:
- `actions[initiate_checkout]`, `actions[purchase]`, `cost_per_action_type`
- `serie_diaria` de initiate_checkout e purchase (para consistência temporal)
- `taxa_checkout_compra` (derivada: purchases / initiate_checkout)
- Período atual + anterior

**Disponibilidade (seção 3 do SKILL.md):** no `APP`, o `initiate_checkout` vem pela Graph API (`insights?fields=actions`) e o módulo roda normal. No `MCP_CONECTOR`, pedir no `ads_get_ad_entities` os campos conferidos `omni_initiated_checkout` (checkout iniciado) e `omni_purchase` (compra), conforme a seção 3 do SKILL.md. Se o checkout iniciado voltar `null`, oferecer a leitura guiada da coluna "Finalizações de compra iniciadas" no Gerenciador de Anúncios (sem troca de modo: o App é só para conta não liberada no conector). Só se o aluno não quiser a leitura guiada, o módulo vira `indisponivel`: declarar e pular. **Nunca pular sem tentar.**

## Os 5 diagnósticos possíveis

> **Benchmark por faixa de ticket (seção 3.5 do SKILL.md, ticket do resumo do produto), NUNCA fixo.** A conclusão de checkout esperada cai conforme o ticket sobe. Comparar a taxa IC→Purchase do aluno com a faixa do ticket DELE:
>
> | Faixa de ticket | Conclusão de checkout esperada |
> |---|---|
> | até R$ 297 | 25–45% |
> | até R$ 500 | 18–35% |
> | até R$ 1.000 | 12–25% |
> | até R$ 2.500 | 7–18% |
> | acima de R$ 2.500 | 5–15% |
>
> Esses números são 🔴 estimativa (só a direção e o teto da faixa alta têm lastro: luxo conclui ~18-22%, Baymard). **Ressalva da Hotmart e da Kiwify:** o `initiate_checkout` pode disparar mais "solto" que o "adicionar ao carrinho" dos estudos, deixando a taxa do aluno artificialmente baixa. Tratar como aproximação, nunca como prova de checkout quebrado.

| Diagnóstico | Critério (relativo à faixa do ticket) | Significado |
|-------------|----------|-------------|
| `checkout_saudavel` | dentro ou acima da faixa do ticket, estável | Etapa final ok para esse ticket. Problema está antes. |
| `checkout_atencao` | logo abaixo do piso da faixa | Abaixo do esperado pro ticket, mas não crítico. Monitorar. |
| `friccao_provavel` | bem abaixo do piso (menos da metade do piso da faixa) | Queda além do que o preço explica. Possíveis causas: pagamento, confiança, formulário. |
| `queda_abrupta` | IC→Purchase caiu > 30% vs período anterior | Algo mudou recentemente. Possível erro técnico, mudança de preço, ou gateway. |
| `volume_insuficiente` | < 10 ICs no período | Dados insuficientes para diagnosticar. |

## Árvore de decisão (ordem de prioridade)

Avaliar na ordem abaixo. O primeiro match é o diagnóstico final. **Os limiares são relativos à faixa de ticket do aluno (seção 3.5 do SKILL.md), não fixos.**

1. **`volume_insuficiente`**: se < 10 ICs no período, parar. Não diagnosticar.
2. **`queda_abrupta`**: se taxa caiu > 30% vs anterior, prevalece (algo mudou agora).
3. **`friccao_provavel`**: se taxa bem abaixo do piso da faixa do ticket (menos da metade do piso), sustentada.
4. **`checkout_atencao`**: se taxa logo abaixo do piso da faixa.
5. **`checkout_saudavel`**: se taxa dentro ou acima da faixa e estável.

**Regra:** nunca atribuir dois diagnósticos ao mesmo checkout. Um veredicto final.

**Exemplo real (por que o benchmark fixo enganava):** Produto A, ticket R$ 2.500, faixa esperada 7–18%. Taxa de 6,7% fica logo abaixo do piso → `checkout_atencao`. Com o benchmark fixo antigo (<20% = fricção), o mesmo 6,7% viraria `friccao_provavel`, um diagnóstico errado que mandaria mexer no checkout quando o número é normal pro ticket.

## Limitação dura (declarar SEMPRE)

```
⚠️ Limitação do diagnóstico de checkout

Esta análise usa eventos atribuídos pela Meta (checkout iniciado
e compra). NÃO tenho acesso ao sistema de pagamento.

O que posso dizer: "há possível fricção na etapa final"
O que NÃO posso dizer: "cartão foi recusado", "Pix não foi pago",
"boleto venceu", "erro técnico no gateway"

Para diagnóstico preciso de checkout: verificar diretamente na
plataforma de pagamento (Hotmart, Kiwify, Stripe etc.). A ligação
da página com o checkout é revisada com /pagina-checkout.
```

## Explicação obrigatória por diagnóstico

### checkout_atencao
```
CHECKOUT: ZONA DE ATENÇÃO ⚠️

Conclusão de checkout (compras ÷ checkouts iniciados): {X}% (logo abaixo do piso da faixa do ticket, seção 3.5)

O que significa: o checkout funciona, mas está abaixo do ideal.
{Y}% das pessoas que iniciam a compra não concluem.

Por que importa: não é urgente, mas há espaço para melhorar.
Pequenos ajustes (opção de Pix, selos de segurança, formulário
mais curto) podem trazer a taxa para dentro da faixa do ticket.

O que fazer: monitorar por 7 dias. Se continuar abaixo do piso
da faixa do ticket, considerar ajustes no checkout (/pagina-checkout
para a ligação da página com a plataforma; o resto, na própria plataforma).
```

### checkout_saudavel
```
CHECKOUT: SAUDÁVEL ✅

Conclusão de checkout (compras ÷ checkouts iniciados): {X}% (dentro ou acima da faixa do ticket, seção 3.5)

O que significa: de cada 100 pessoas que iniciam o checkout,
{X} completam a compra. Isso é saudável. Se o CPA está alto,
o problema está ANTES do checkout (página, oferta ou tráfego).
```

### friccao_provavel
```
CHECKOUT: FRICÇÃO PROVÁVEL ⚠️

Conclusão de checkout (compras ÷ checkouts iniciados): {X}% (bem abaixo do piso da faixa do ticket, seção 3.5)

O que significa: {Y} pessoas iniciaram o checkout, mas apenas
{Z} completaram ({X}%). Algo entre "clicar em comprar" e
"pagamento confirmado" está impedindo {W}% de fechar.

Possíveis causas (sem dados de backend, são hipóteses):
- Preço alto demais para o público
- Poucas opções de pagamento (só cartão? falta Pix?)
- Formulário longo ou confuso
- Falta de selos de segurança
- Página de checkout lenta

O que verificar na plataforma:
- Taxa de aprovação de cartão
- Boletos gerados vs pagos
- Pix gerados vs pagos
- Abandono por etapa no checkout (se disponível)

O que NÃO fazer: não aumentar tráfego. Mais pessoas no checkout
com fricção = mais abandono = mais dinheiro perdido.
```

### queda_abrupta
```
CHECKOUT: QUEDA ABRUPTA 🔴

Conclusão de checkout (compras ÷ checkouts iniciados): era {anterior}%, agora {atual}% (queda de {delta}%)

O que significa: algo mudou recentemente que piorou a taxa de
conclusão do checkout. Pode ser:
- Mudança de preço
- Problema técnico no gateway
- Mudança na plataforma de pagamento
- Nova oferta que atrai público menos qualificado

Ação urgente: verificar se o checkout está funcionando.
Testar uma compra manual agora.
```

## Comparação temporal

```
Evolução do checkout (7d atual vs 7d anterior):

                               Anterior    Atual     Variação
Checkouts iniciados            45          38        -15,6%
Compras                        18          10        -44,4%
Conclusão de checkout          40,0%       26,3%     -34,3% ⚠️
Custo por checkout iniciado    R$ 55,56    R$ 65,79  +18,4%
CPA                            R$ 138,89   R$ 250,00 +80,0%
```

## Output YAML

```yaml
diagnostico_checkout:
  diagnostico: checkout_saudavel | checkout_atencao | friccao_provavel | queda_abrupta | volume_insuficiente
  taxa_ic_purchase: 0.263
  volume_ic: 38
  volume_purchase: 10
  custo_por_ic: 65.79
  cpa: 250.00

  comparacao:
    anterior: { taxa: 0.40, ic: 45, purchase: 18 }
    atual: { taxa: 0.263, ic: 38, purchase: 10 }
    variacao_taxa: -0.343

  limitacao: "Sem dados de backend. Diagnóstico baseado em eventos Meta."
  confianca: alta | media | baixa | indisponivel_mcp
```
