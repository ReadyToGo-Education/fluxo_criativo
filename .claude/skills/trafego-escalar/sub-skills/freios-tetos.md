# Freios e Tetos. Seções 6, 9 e 10 do /trafego-escalar

Esta sub-skill aprofunda os mecanismos de contenção da escala. Traz os gatilhos exatos dos 3 níveis de freio, os payloads reais de incremento e de reversão separados por ABO e CBO, a regra de dados imaturos, os 4 tetos e o protocolo de devolução para `/trafego-otimizar`.

**Freio tem prioridade sobre crescimento.** Qualquer sinal de degradação para a escala antes do próximo incremento.

Toda chamada usa `v25.0` e passa pelo gate de confirmação do `CLAUDE.md`.

---

## 1. Orçamento em centavos, e no nível certo

Duas regras que, juntas, respondem por quase todo erro de execução desta skill.

### 1.1 Centavos

A Marketing API recebe orçamento na menor unidade da moeda. Em BRL, centavos, inteiro.

| Intenção | Payload |
|---|---|
| R$ 288,00 por dia | `"daily_budget": 28800` |
| R$ 360,00 por dia | `"daily_budget": 36000` |

Converter sempre com `round(valor_brl * 100)`. Enviar `288` cria orçamento de R$ 2,88.

### 1.2 ABO ou CBO decide o objeto

| `budget.tipo` | Objeto alvo | Endpoint de incremento | Efeito |
|---|---|---|---|
| `ABO` | `adset_id` do conjunto vencedor | `POST /v25.0/{adset_id}` | Afeta só aquele conjunto |
| `CBO` | `campaign_id` | `POST /v25.0/{campaign_id}` | Afeta todos os conjuntos da campanha |

**A `tool_call.name` no output precisa bater com o tipo:** `update_adset_budget` se ABO, `update_campaign_budget` se CBO. Errar isso ou quebra a chamada, ou aplica o incremento em lugar diferente do que foi mostrado ao aluno no plano.

Se `budget.tipo` vier indeterminado, **não executar**. Devolver `acao: aguardar` com motivo "tipo de orçamento não detectado".

### 1.3 Payload de incremento

```
POST /v25.0/{adset_id}          # ABO
POST /v25.0/{campaign_id}       # CBO
```

```json
{ "daily_budget": 28800 }
```

Nada mais no payload. Não reenviar `targeting`, `status` nem `optimization_goal` num ajuste de orçamento: reenviar campo que não mudou é um caminho conhecido para reset de aprendizado.

---

## 2. Os 3 níveis de freio

Avaliar **antes de cada incremento** e **depois de cada incremento**, sempre respeitando a regra de dados imaturos da seção 3.

### 2.1 Freio leve. Pausar o próximo incremento

Gatilho, qualquer um:

| Condição | Medida |
|---|---|
| CPA ou CPL piorou de 10% a 20% | janela curta contra janela média |
| Frequência subiu 0,5 ou mais | no ciclo |
| CPM subiu 20% ou mais | no ciclo |

**Ação.** Não incrementar. Manter o orçamento atual. Reavaliar em 48h. Nada é chamado na API: o freio leve é uma decisão de não agir.

Registrar no histórico com `resultado_do_ciclo_anterior: freio_leve`, o que zera `ciclo_atual`.

### 2.2 Freio médio. Reverter o último incremento

Gatilho, qualquer um:

| Condição | Medida |
|---|---|
| CPA ou CPL piorou de 20% a 30% | sustentado por 48h |
| Frequência maior ou igual a 4 | sem refresh criativo na fila |
| CTR caiu 30% ou mais | nos anúncios principais |

**Ação.** Reduzir o orçamento em 20%, voltando ao patamar anterior. Acionar refresh criativo. Devolver diagnóstico para `/trafego-otimizar`.

```
POST /v25.0/{adset_id}     # ou {campaign_id} se CBO
{ "daily_budget": 24000 }
```

O valor de volta é o `orcamento_antes_brl` do último bloco do histórico, não um cálculo de -20% sobre o atual. Usar o registro é mais fiel do que recalcular, porque incrementos anteriores podem ter sido arredondados.

### 2.3 Freio total. Devolver para a otimização

Gatilho, qualquer um:

| Condição |
|---|
| CPA ou CPL piorou 30% ou mais |
| 2 ciclos consecutivos de incremento sem ganho líquido de volume |
| Saturação estrutural: frequência alta **e** CPM alto **e** CTR caindo, ao mesmo tempo |

**Ação.** Reverter ao último orçamento estável conhecido e emitir `handoff_para_otimizacao: true`. **A skill se desativa para essa campanha** até vencer o cooldown.

---

## 3. Dados imaturos. Quando não acionar freio

Depois de um incremento, **não interpretar piora** enquanto qualquer uma for verdadeira:

- Gasto pós-incremento abaixo de 50% do novo orçamento diário
- Menos de 24h desde o incremento
- Menos de 1.000 impressões novas

Nesses casos, emitir `acao: aguardar` e marcar a próxima reanálise. Acionar freio com dado imaturo é o erro mais caro desta skill: reverte uma escala que estava funcionando e ainda zera o ciclo por engano.

---

## 4. Escala horizontal. Duplicação

### 4.1 Duplicar conjunto (ABO)

```
POST /v25.0/{adset_id}/copies
```

```json
{
  "campaign_id": "120203456789",
  "deep_copy": true,
  "status_option": "PAUSED",
  "rename_options": { "rename_suffix": " - cópia pt_mundo" }
}
```

| Parâmetro | Efeito |
|---|---|
| `campaign_id` | Campanha de destino. Omitir mantém na mesma |
| `deep_copy: true` | Copia também os anúncios do conjunto. Sem isso vem conjunto vazio |
| `status_option: "PAUSED"` | A cópia nasce pausada, para revisão antes de gastar |
| `rename_options` | Evita dois conjuntos com nome idêntico no Gerenciador |

### 4.2 Duplicar campanha

```
POST /v25.0/{campaign_id}/copies
```

```json
{ "deep_copy": true, "status_option": "PAUSED" }
```

### 4.3 Aplicar o teste na cópia

A cópia nasce idêntica. O teste é aplicado **depois**, com um segundo `POST` no conjunto copiado, mudando **um único elemento**:

| Teste | O que muda no conjunto copiado |
|---|---|
| `pt_mundo` | `targeting.geo_locations` para mundial, `locales: [6]` |
| `reels_only` | `instagram_positions: ["reels"]`, `publisher_platforms: ["instagram"]` |
| `instagram_only` | `publisher_platforms: ["instagram"]` |
| `facebook_only` | `publisher_platforms: ["facebook"]` |
| `advantage_placement` | Remover `publisher_platforms` e posições. Omissão ativa o automático |
| `nova_segmentacao` | Trocar público em `targeting`, mantendo o resto |

**Um elemento por cópia.** Duas mudanças na mesma cópia tornam o resultado ilegível: não dá para saber qual delas causou a diferença.

### 4.4 Validação de integridade antes de duplicar

Antes de qualquer duplicação, confirmar que os anúncios da campanha original tratam do **mesmo produto, mesmo público e mesmo funil** declarados na abertura da sessão. Se houver divergência, alertar o aluno antes de executar. Duplicar uma campanha que mistura produtos multiplica a incoerência.

---

## 5. Os 4 tetos

Quando um teto é atingido, a skill para de tentar escalar e declara explicitamente.

| Teto | Gatilho | Recomendação |
|---|---|---|
| `audiencia_exausta` | Frequência acima de 4 mesmo após 2 refreshes criativos seguidos no mesmo conjunto | Expandir para nova trilha de público, ou horizontal com segmentação diferente |
| `cpm_ceiling` | CPM 50% ou mais acima da média histórica da conta, sustentado por 7 dias, sem evento sazonal que explique | Aguardar normalização. Escalar agora compra tráfego caro |
| `volume_ceiling` | 3 ciclos consecutivos sem ganho líquido de conversões, mesmo com orçamento maior | Mercado endereçável atingido. Abrir outra fonte ou outro produto |
| `operacional` | Orçamento chegou ao `teto_de_orcamento_diario_brl` declarado | Decisão do aluno: elevar o teto ou parar |

Output:

```yaml
teto_atingido:
  tipo: audiencia_exausta | cpm_ceiling | volume_ceiling | operacional
  recomendacao: <ação alternativa concreta>
```

`cpm_ceiling` depende da média histórica da conta. Se a conta não tem 14 dias de histórico, o teto fica **indeterminado**, não falso. Ver a política de dado ausente em `sub-skills/matriz-scoring.md`, seção 6.

---

## 6. Handoff para `/trafego-otimizar`

Acionado por freio total ou por teto que a escala não resolve.

```yaml
handoff_para_otimizacao:
  ativo: true
  motivo: cpa_degradou_30_pct_sustentado | dois_ciclos_sem_ganho_liquido | saturacao_estrutural | teto_atingido_audiencia
  contexto:
    orcamento_revertido_brl: 240.00
    incrementos_revertidos: 1
    ultimo_orcamento_estavel_brl: 240.00
    ciclos_de_escala_completados: 3
  recomendacao_para_otimizacao:
    - "Frequência 4,2 com 2 refreshes já feitos. Investigar troca de ângulo, não só de criativo."
    - "CPM 38% acima da média da conta nos últimos 7 dias."
```

### Cooldown

Depois da devolução, a escala **não aceita nova prontidão** antes do prazo:

| Trilha | Cooldown |
|---|---|
| Perpétuo low e mid | 7 dias |
| Perpétuo high | 14 dias |
| Lançamento | 24 horas |

O cooldown conta a partir da data do freio registrada no histórico. Se `/trafego-otimizar` emitir `sinal_para_escala.pronta: true` antes do prazo, recusar e informar quantos dias faltam.

---

## 7. Registro no histórico após cada ação

Escrever no arquivo `meus-produtos/{ativo}/trafego/escalar/historico-{campaign_id}.md`, schema na seção 1 de `sub-skills/matriz-scoring.md`.

| Evento | `resultado_do_ciclo_anterior` | Efeito no `ciclo_atual` |
|---|---|---|
| Incremento executado e sustentado | `sustentou` | soma 1 |
| Freio leve | `freio_leve` | zera |
| Freio médio | `freio_medio` | zera |
| Freio total | `freio_total` | zera e inicia cooldown |
| Aguardando dado maturar | não escrever bloco | não altera |

**Só escrever depois da execução confirmada na API.** Histórico que registra incremento que não aconteceu corrompe a contagem de ciclo e, com ela, a recomendação do próximo ciclo.

---

## 8. Checklist antes de executar qualquer ação de escala

- [ ] Gate de confirmação apresentado no chat e respondido com "sim"
- [ ] `budget.tipo` detectado, e `tool_call.name` batendo com ele
- [ ] Orçamento convertido para centavos
- [ ] Payload de incremento contém só `daily_budget`
- [ ] Incremento dentro da velocidade declarada, e nunca acima de +50%
- [ ] Regra de dados imaturos checada antes de interpretar qualquer piora
- [ ] Duplicação com `deep_copy: true` e `status_option: "PAUSED"`
- [ ] Um único elemento de teste por cópia
- [ ] Cooldown respeitado, se houve devolução anterior
- [ ] Histórico atualizado depois da confirmação da API, nunca antes
