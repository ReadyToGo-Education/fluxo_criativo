# Sub-skill. Risco de Incremento

Score numérico de 0 a 100 específico para cada decisão de escala. Avalia "qual o risco de colocar mais dinheiro aqui agora?".

**Diferente do `confianca` existente:** a escalar já tem `confianca: alta/media/baixa` por modo (Passo 0.75, matriz 9×5). O risco de incremento é por **decisão individual** ("+20% NESTA campanha hoje"), não por modo geral. Complementa, não substitui.

**Diferente do score de confiança da `/trafego-diagnostico`:** aquele avalia "posso confiar nesse dado?". Este avalia "qual o risco financeiro de aumentar gasto neste objeto agora?".

Tudo aqui é leitura e cálculo: não passa pelo gate 🛡️. O score entra no plano da §11 da escalar, que é onde o gate acontece.

## Quando é calculado

Passo 0.85 da escalar: depois do checklist de prontidão (0.8) passar, ou depois de receber o handoff de prontidão da `/trafego-otimizar`, e antes do plano ser montado. Para cada campanha/adset candidato a escala.

## As 8 variáveis do score

Cada variável contribui de 0 a 12,5 pontos (total máximo 100). Score ALTO = MAIS risco.

| # | Variável | 0 pts (risco mínimo) | 6 pts (risco médio) | 12,5 pts (risco máximo) |
|---|----------|---------------------|---------------------|------------------------|
| 1 | **Volume de conversões** | ≥ 30 conversões na janela | 10 a 29 | < 10 |
| 2 | **Consistência (CV diário)** | CV < 0,30 (estável) | CV 0,30 a 0,60 | CV > 0,60 (caótico) |
| 3 | **Margem de segurança CPA** | CPA ≤ target × 0,7 (30%+ de folga) | CPA entre target × 0,7 e × 0,9 | CPA > target × 0,9 (quase no limite) |
| 4 | **Frequência** | < 2,0 | 2,0 a 3,5 | > 3,5 (saturando) |
| 5 | **Dependência criativa** | Top 1 anúncio concentra < 40% do gasto | 40 a 70% | > 70% (um anúncio sustenta tudo) |
| 6 | **Dependência de remarketing** | < 30% do resultado em público quente | 30 a 60% | > 60% (resultado inflado) |
| 7 | **Histórico pós-incremento** | 2+ ciclos anteriores bem-sucedidos | 1 ciclo ou sem histórico | Último incremento acionou freio |
| 8 | **Saturação de audiência** | Alcance incremental estável | Alcance desacelerando | Alcance estagnado ou CPM subindo 20%+ |

A variável 7 sai do histórico do produto, em `meus-produtos/{ativo}/trafego/escalar/historico-{campaign_id}.md` (Leitura 3 do Passo 0.75 da escalar). Conta ciclos, não linhas: as linhas do mesmo lote e as ativações das estruturas dele são um ciclo só.

## Cálculo

Para cada variável, atribuir 0, 6 ou 12,5 pontos. Somar. Score = soma (0 a 100).

**Variável ausente:** se não há dado para calcular (ex: sem histórico de ciclos), assumir 6 pts (risco médio) e listar em `variaveis_sem_dado`. É uma postura conservadora sobre o risco, não uma estimativa de métrica: o número que falta continua `null` no payload, como manda o princípio 12 da escalar.

## As 4 faixas

| Faixa | Score | Significado | Ação |
|-------|-------|-------------|------|
| `risco_baixo` | 0 a 25 | Condições favoráveis para escala | Seguir com o incremento |
| `risco_medio` | 26 a 50 | Condições razoáveis, com ressalvas | Seguir com cautela, monitorar de perto |
| `risco_alto` | 51 a 75 | Múltiplos sinais de fragilidade | Confirmação reforçada com aviso explícito |
| `risco_extremo` | 76 a 100 | Condições hostis para escala | **Bloquear incremento.** Não escalar até resolver. |

## Regras de bloqueio

- `risco_extremo` (76 a 100): incremento **bloqueado**. A skill não apresenta o plano de escala para essa campanha. Devolve com motivo e handoff para `/trafego-otimizar`.
- `risco_alto` (51 a 75): incremento permitido, mas com aviso explícito:

```
⚠️ RISCO ALTO: incremento de +{X}% em "{nome}" tem risco {score}/100

Sinais de fragilidade:
- {variável 1}: {valor}, {risco}
- {variável 2}: {valor}, {risco}

Quer prosseguir mesmo assim?

1. Sim, aceito o risco
2. Não, prefiro esperar mais dados
3. Reduzir incremento para +{X/2}% (mais conservador)
```

## Explicação obrigatória

Cada score DEVE vir com texto explicativo:

```
RISCO DE INCREMENTO: +20% em "Campanha A Perpétuo", risco 30/100 (MÉDIO)

O que significa: as condições são razoáveis para escalar, mas
há sinais que pedem atenção.

Por que está nesse nível:
- Dependência criativa média (1 anúncio concentra 65% do gasto): se
  esse criativo cansar, a campanha inteira cai.
- Margem de segurança moderada (CPA a 88% do target): folga
  limitada para absorver oscilação pós-incremento.

Para reduzir o risco antes de escalar:
- Subir 1 ou 2 criativos novos (diversificar a dependência):
  /copy-anuncio + /criativo-estatico, com A/B no /trafego-testes
- Aguardar mais 3 dias para o CPA estabilizar abaixo de 80% do target

Se escalar agora: monitorar diariamente. Freio leve se o CPA
subir 15%+ nas primeiras 48h.
```

## Output YAML

```yaml
risco_incremento:
  campanha_id: "<id>"
  campanha_nome: "<nome>"
  incremento_proposto: "+20%"
  score: 30
  faixa: risco_medio
  variaveis:
    volume_conversoes: { valor: 22, pontos: 6 }
    consistencia_cv: { valor: 0.28, pontos: 0 }
    margem_seguranca_cpa: { valor: 0.12, pontos: 6 }
    frequencia: { valor: 1.8, pontos: 0 }
    dependencia_criativa: { valor: 0.65, pontos: 6 }
    dependencia_remarketing: { valor: 0.25, pontos: 0 }
    historico_incremento: { valor: "1_ciclo_ok", pontos: 6 }
    saturacao_audiencia: { valor: "desacelerando", pontos: 6 }
  variaveis_sem_dado: []
  o_que_reduz_risco:
    - "Diversificar criativos (reduz dependência)"
    - "Aguardar +3 dias (estabilizar margem)"
  acao: seguir | cautela | confirmacao_reforcada | bloqueado
```

## Integração com o plano de confirmação (§11 da escalar)

O score aparece junto de cada ação no plano, dentro do bloco 🛡️:

```
[1] VERTICAL: subir "Campanha A Perpétuo" de R$ 200 para R$ 240 (+20%)
    Risco: 30/100 (médio), dependência criativa + margem moderada
    Motivo: CPA 12% abaixo do target, frequência 1,8

[2] HORIZONTAL: duplicar "Campanha A Perpétuo" com teste LAL 2%
    Risco: 24/100 (baixo), base sólida, público novo
```

Se qualquer ação tem `risco_extremo`, ela não aparece no plano (bloqueada, mas listada como reprovada com o motivo, sem sumir). Se `risco_alto`, aparece com a tag ⚠️.
