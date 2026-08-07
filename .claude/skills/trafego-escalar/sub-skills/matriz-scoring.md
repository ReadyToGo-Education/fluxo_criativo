# Matriz de Scoring. Passo 0.75 do /trafego-escalar

Esta sub-skill aprofunda a análise e recomendação técnica do `/trafego-escalar`. Traz as 3 leituras obrigatórias, o schema do histórico de escala, as fórmulas exatas dos 9 sinais derivados, a matriz de pontuação, o algoritmo de decisão e um exemplo numérico completo.

Toda métrica usada aqui vem de leitura real. **Nada é estimado.** Ver seção 6.

---

## 1. As 3 leituras, na ordem

### Leitura 1. Conta inteira, nível ad

```
/trafego-insights  escopo=conta_completa  nivel=ad  janela=7d
```

Roda **uma vez por sessão**, antes de avaliar campanha por campanha. Alimenta dois sinais que só existem no plano da conta:

| Saída | Definição |
|---|---|
| `vencedores_conta.adsets[]` | Adsets com CPA menor ou igual a `target * 0,9` nas 3 janelas, agrupados por objetivo |
| `vencedores_conta.ads_espalhados[]` | Ads com CTR único saudável e pelo menos 50 conversões, em conjuntos ou campanhas diferentes |

Sem esta leitura, os sinais de consolidação (CBO e Advantage) ficam indeterminados. Não pule.

### Leitura 2. Por campanha selecionada

```
/trafego-insights  campaign_id=<id>  nivel=auto  janela=trilha_completa
```

Devolve frequência, audiência ativa, CPM e variação, CTR único, criativos saudáveis, gasto contra orçamento, idade da campanha e, criticamente, `budget.tipo` (`ABO` ou `CBO`).

**`budget.tipo` é bloqueante.** Sem ele detectado, a skill não executa: devolve `acao: aguardar` com motivo "tipo de orçamento não detectado". Aplicar incremento no nível errado ou quebra a chamada, ou altera o orçamento de todos os conjuntos quando a intenção era um só.

### Leitura 3. Histórico de escala, cache local

```
meus-produtos/{ativo}/trafego/escalar/historico-{campaign_id}.md
```

Se o arquivo não existir, `ciclo_atual = 0`. Esse é o caso normal da primeira escala.

#### Schema do histórico

Arquivo append-only, um bloco por incremento, mais recente no topo logo abaixo do cabeçalho.

```markdown
# Histórico de escala. {nome da campanha}

campaign_id: 120203456789
trilha: perpetuo_mid
ticket_brl: 997.00
target_brl: 300.00
budget_tipo: ABO
objeto_alvo: 120203456789001

---

## Ciclo 3. 2026-08-07 14:32

modo: vertical
velocidade: normal
orcamento_antes_brl: 240.00
orcamento_depois_brl: 288.00
incremento_pct: 20
cpa_no_momento_brl: 212.40
frequencia_no_momento: 2.1
resultado_do_ciclo_anterior: sustentou
observacao: CPM subiu 8 por cento, dentro do tolerado

---

## Ciclo 2. 2026-08-05 09:10
...
```

**Como contar `ciclo_atual`:** número de blocos consecutivos, do topo para baixo, sem nenhum `resultado_do_ciclo_anterior` igual a `freio_leve`, `freio_medio` ou `freio_total`. Qualquer freio zera a contagem. Um freio no meio do histórico significa que a onda de escala anterior terminou ali.

**Quando escrever.** Depois de cada incremento executado com sucesso, nunca antes. Registrar também os freios acionados, porque é o freio que zera o ciclo.

---

## 2. Os 9 sinais derivados

| Sinal | Fórmula exata | Fonte |
|---|---|---|
| `freq_baixa_audiencia_grande` | `frequencia < 1,8` **E** `audiencia_ativa > 2.000.000` **E** CPM estável ou caindo nos últimos 3 dias | Leitura 2 |
| `freq_alta_ou_aud_pequena` | `frequencia > 2,2` **OU** `audiencia_ativa < 1.000.000` | Leitura 2 |
| `estavel_ciclo_2_mais` | Sem freios há 7 dias ou mais **E** `ciclo_atual >= 2` | Leituras 2 e 3 |
| `tres_mais_adsets_vencedores` | `vencedores_conta.adsets.length >= 3` dentro do mesmo objetivo | Leitura 1 |
| `cinco_mais_ads_espalhados` | `vencedores_conta.ads_espalhados.length >= 5` em conjuntos diferentes | Leitura 1 |
| `cpm_e_freq_subindo` | CPM subiu 15% ou mais **E** frequência subiu 0,3 ou mais, nos últimos 3 dias | Leitura 2 |
| `ciclo_zero` | `ciclo_atual == 0` | Leitura 3 |
| `ciclo_tres_mais_verticais` | `ciclo_atual >= 3` **E** todos os modos anteriores foram Vertical | Leitura 3 |
| `orcamento_acima_metade_potencial` | `orcamento_atual >= teto_de_orcamento_diario_brl * 0,5` | Leitura 2 e input do aluno |

**`orcamento_acima_metade_potencial` fica indeterminado quando o aluno não declarou teto.** Não vale zero, não vale falso. Ver seção 6.

---

## 3. Matriz de pontuação

| Sinal | Vertical | Horizontal | V+H | CBO | Advantage |
|---|---|---|---|---|---|
| `freq_baixa_audiencia_grande` | +3 | 0 | +1 | 0 | 0 |
| `freq_alta_ou_aud_pequena` | 0 | +3 | +2 | 0 | 0 |
| `estavel_ciclo_2_mais` | +1 | +2 | +3 | +1 | +1 |
| `tres_mais_adsets_vencedores` | 0 | 0 | 0 | +3 | +1 |
| `cinco_mais_ads_espalhados` | 0 | 0 | 0 | +1 | +3 |
| `cpm_e_freq_subindo` | -2 | +2 | +1 | 0 | +1 |
| `ciclo_zero` | +2 | -1 | -1 | -1 | -1 |
| `ciclo_tres_mais_verticais` | -2 | +2 | +3 | +1 | +1 |
| `orcamento_acima_metade_potencial` | -1 | +1 | +1 | 0 | 0 |

### Penalidade extra do Vertical

Vertical leva **-2 adicionais**, independente do score acumulado, se qualquer uma for verdadeira:

- `freq_baixa_audiencia_grande` é **falso**
- `orcamento_acima_metade_potencial` é **verdadeiro**
- `cpm_e_freq_subindo` é **verdadeiro**

A porta de entrada do Vertical é estreita de propósito. Subir orçamento em campanha que já está saturando acelera a saturação e queima o aprendizado conquistado.

---

## 4. Algoritmo de decisão

1. Somar os pontos de cada modo, considerando só os sinais determinados.
2. Aplicar a penalidade extra do Vertical.
3. **Maior score é o primário.**
4. **Segundo maior é o alternativo, se tiver pelo menos 60% do score do primário.** Abaixo disso, não há alternativo real.
5. **Se o score do primário for menor que 4 em valor absoluto:** marcar `confianca: baixa` e trocar o alternativo por `aguardar_proximo_ciclo`.
6. Definir a velocidade pela regra da seção 4 do `SKILL.md`:

| Velocidade | Quando |
|---|---|
| Conservadora, +15% a cada 72h | High ticket, audiência pequena, menos de 3 criativos de backup |
| Normal, +20% a cada 24h | Default |
| Agressiva, +30% a +50% a cada 24h | Lançamento em captação, ou sazonal declarado, **e** pelo menos 3 criativos de backup |

**Teto absoluto:** um incremento isolado nunca passa de +50%, em nenhuma velocidade, em nenhuma circunstância.

### Empate

Se dois modos empatam no topo, desempatar nesta ordem:

1. O que preserva mais aprendizado (Vertical preserva 100%, Horizontal reinicia).
2. O de menor custo operacional para o aluno.
3. Vertical, se ainda empatado.

---

## 5. Exemplo numérico completo

**Cenário.** Perpétuo mid ticket, R$ 997. Meta de CPA R$ 300. Teto declarado R$ 600 por dia. Orçamento atual R$ 240 por dia em ABO. CPA atual R$ 212,40. Frequência 2,4. Audiência ativa 900 mil. CPM subiu 18% e frequência subiu 0,4 nos últimos 3 dias. `ciclo_atual = 3`, todos Vertical. Na conta: 2 adsets vencedores, 6 ads vencedores espalhados.

**Sinais ativos:**

| Sinal | Valor | Porquê |
|---|---|---|
| `freq_baixa_audiencia_grande` | falso | frequência 2,4 acima de 1,8 e audiência abaixo de 2M |
| `freq_alta_ou_aud_pequena` | **verdadeiro** | frequência 2,4 acima de 2,2, e audiência 900k abaixo de 1M |
| `estavel_ciclo_2_mais` | **verdadeiro** | ciclo 3, sem freios |
| `tres_mais_adsets_vencedores` | falso | só 2 |
| `cinco_mais_ads_espalhados` | **verdadeiro** | 6 |
| `cpm_e_freq_subindo` | **verdadeiro** | CPM +18% e frequência +0,4 |
| `ciclo_zero` | falso | ciclo 3 |
| `ciclo_tres_mais_verticais` | **verdadeiro** | 3 ciclos, todos Vertical |
| `orcamento_acima_metade_potencial` | falso | metade do teto é R$ 300, e o orçamento atual é R$ 240 |

Cinco sinais ativos: `freq_alta_ou_aud_pequena`, `estavel_ciclo_2_mais`, `cinco_mais_ads_espalhados`, `cpm_e_freq_subindo`, `ciclo_tres_mais_verticais`. Os outros quatro são falsos e não somam.

**Soma, contando só os cinco ativos:**

| Modo | freq_alta | estavel | cinco_ads | cpm_freq | ciclo3vert | Subtotal | Penalidade | Total |
|---|---|---|---|---|---|---|---|---|
| Vertical | 0 | +1 | 0 | -2 | -2 | -3 | -2 | **-5** |
| Horizontal | +3 | +2 | 0 | +2 | +2 | +9 | 0 | **+9** |
| V+H | +2 | +3 | 0 | +1 | +3 | +9 | 0 | **+9** |
| CBO | 0 | +1 | +1 | 0 | +1 | +3 | 0 | **+3** |
| Advantage | 0 | +1 | +3 | +1 | +1 | +6 | 0 | **+6** |

Vertical leva a penalidade porque `freq_baixa_audiencia_grande` é falso **e** `cpm_e_freq_subindo` é verdadeiro. Duas condições atendidas, mas a penalidade é aplicada uma única vez.

Empate entre Horizontal e V+H em 9. O desempate pelo critério 1 favoreceria V+H, que preserva mais aprendizado ao longo da onda. Mas o problema imediato desta campanha é saturação (frequência 2,4, audiência 900 mil, CPM subindo 18%), e `cpm_e_freq_subindo` verdadeiro indica que ela já está no limite. Horizontal puro abre fonte nova de tráfego agora. V+H só faria sentido depois que a nova fonte estabilizasse.

**Decisão:** primário Horizontal, alternativo V+H (score 9, acima de 60% de 9). Velocidade normal. Confiança alta, score bem acima de 4.

**Gatilho de migração para o alternativo:** quando a frequência do conjunto duplicado cair abaixo de 2,0 e o CPM estabilizar, alternar para V+H.

---

## 6. Política de dado ausente. Regra dura

Quando um campo volta `null`, vazio, ou a leitura falha em parte:

1. **Nunca inventar valor.** Sem média de setor, sem benchmark genérico, sem "tipicamente é X".
2. **Sinal que depende do campo ausente não é pontuado.** Não vira +0 nem chute para um lado. Vira indeterminado e sai da soma.
3. **Contar os indeterminados.** Se 3 ou mais dos 9 ficarem indeterminados, forçar `confianca: baixa` e oferecer "Aguardar próximo ciclo de dados".
4. **Sinalizar ao aluno.** Bloco `dados_ausentes` no output, listando campo e motivo.
5. **A proibição vale para a conversa inteira.** Se o aluno perguntar "qual seria o CPM esperado?" e a conta não tem histórico na janela, a resposta é "não tenho esse dado". Nunca uma média de mercado.

Motivos comuns e como redigir:

| Campo ausente | Motivo a exibir |
|---|---|
| `frequencia` | "campanha tem 2 dias, frequência ainda não estabilizou" |
| `cpa` | "evento Purchase sem disparo na janela" |
| `audiencia_ativa` | "audiência ativa não retornada pela API" |
| `cpm_delta` | "sem 3 dias de histórico para comparar" |
| `teto_de_orcamento_diario_brl` | "aluno não declarou teto operacional" |

---

## 7. Checklist antes de recomendar

- [ ] Leitura 1 rodada uma vez, no nível ad da conta inteira
- [ ] Leitura 2 rodada por campanha, com `budget.tipo` detectado
- [ ] Leitura 3 feita, `ciclo_atual` contado pela regra do freio
- [ ] Os 9 sinais avaliados, os indeterminados marcados e excluídos da soma
- [ ] Penalidade extra do Vertical aplicada quando cabível
- [ ] Alternativo só existe se atingir 60% do score do primário
- [ ] `confianca: baixa` quando score menor que 4 ou 3 ou mais sinais indeterminados
- [ ] Velocidade agressiva só com 3 ou mais criativos de backup
- [ ] Nenhum número da recomendação foi estimado
