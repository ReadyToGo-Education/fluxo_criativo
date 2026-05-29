# Sub-fluxo. Programação Liga/Pausa de Adset (Delivery Schedule)

Configura o adset_schedule do Meta Ads para que o adset entregue apenas em horários/dias específicos da semana. Útil para pausar o adset fora do horário comercial, fim de semana ou madrugada.

## Perguntas que cobre

- "Programa pra ligar minhas campanhas na segunda e pausar no domingo"
- "Pausa anúncios entre meia-noite e 6h da manhã"
- "Quero rodar só de segunda a sexta, das 8h às 22h"
- "Pausa minha campanha no fim de semana inteiro"
- "Roda só nos horários de pico do meu público (18h às 23h)"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `adset_id` | obrigatório | Adset alvo (pode ser múltiplos) |
| `dias_semana` | seg a sex | 0=dom, 1=seg, ..., 6=sáb |
| `hora_inicio` | 08:00 | Horário em que entrega começa |
| `hora_fim` | 22:00 | Horário em que entrega termina |
| `timezone` | da ad account | Timezone usada pelo Meta |

## Pré-requisito crítico: lifetime_budget

`adset_schedule` **só funciona** com adset que tem `lifetime_budget` (orçamento total). Não funciona com `daily_budget`.

A skill verifica antes de aplicar:

```python
adset = GET /<adset_id>?fields=daily_budget,lifetime_budget,...
if adset.daily_budget is not None:
    # Bloqueia
    return "⚠️ Esse adset usa orçamento diário (daily_budget). adset_schedule só funciona com orçamento total (lifetime_budget). Quer que eu converta? (não muda o valor, só a forma de cobrança)."
```

Se aluno autoriza converter:
1. Calcular `lifetime_budget = daily_budget × dias_da_campanha`
2. Pedir `end_time` se a campanha não tem (lifetime_budget exige `end_time`)
3. Aplicar conversão **antes** do schedule

## Endpoint

```
POST /<adset_id>
{
  "adset_schedule": [
    { "start_minute": 480, "end_minute": 1320, "days": [1, 2, 3, 4, 5] }
  ],
  "pacing_type": ["standard", "day_parting"]
}
```

`start_minute` e `end_minute` são minutos desde meia-noite. Conversões úteis:
- 0 = 00:00
- 360 = 06:00
- 480 = 08:00
- 720 = 12:00
- 1080 = 18:00
- 1320 = 22:00
- 1440 = 24:00 (= dia seguinte)

Múltiplos blocos no mesmo array são permitidos (ex: rodar 8h-12h e 14h-18h):
```json
[
  { "start_minute": 480,  "end_minute": 720,  "days": [1,2,3,4,5] },
  { "start_minute": 840,  "end_minute": 1080, "days": [1,2,3,4,5] }
]
```

## Receitas pré-configuradas

A skill oferece atalhos:

### Receita 1. Horário comercial (seg a sex, 8h-22h)
```yaml
days: [1,2,3,4,5]
start_minute: 480  # 08:00
end_minute: 1320   # 22:00
```

### Receita 2. Sem fim de semana (seg a sex, 24h)
```yaml
days: [1,2,3,4,5]
start_minute: 0
end_minute: 1440
```

### Receita 3. Sem madrugada (todo dia, 6h-23h)
```yaml
days: [0,1,2,3,4,5,6]
start_minute: 360   # 06:00
end_minute: 1380    # 23:00
```

### Receita 4. Só fim de semana (sáb e dom, 9h-23h)
```yaml
days: [0,6]
start_minute: 540   # 09:00
end_minute: 1380    # 23:00
```

### Receita 5. Custom
Aluno define dias e horários manualmente.

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Reforça a regra global do CLAUDE.md.

### Ordem fixa

1. **Adset alvo.** Pergunta neutra: "Qual adset você quer programar liga/pausa? (digite o nome — completo ou parcial — ou peça pra eu listar)". Aceita 3 modos (mesmo padrão da [`ab-generico` Helper de molde](../../trafego-testes/sub-skills/ab-generico.md#padrão-de-coleta-de-inputs-uma-pergunta-por-mensagem)):
   - **(a) Nome (total ou parcial):** `GET /act_<id>/adsets?fields=name,status,effective_status,daily_budget,lifetime_budget` → match case-insensitive `contains`. 1 match: confirma. Múltiplos: lista numerada filtrada.
   - **(b) Listar:** "lista", "não lembro" → mostra adsets ACTIVE/PAUSED dos últimos 90d, numerados, com nome + status + budget atual.
   - **(c) ID direto** (raro): valida e confirma.

   **Aluno nunca digita ID cru sem ter sido pedido.**

2. **Receita.** Mostrar as 5 receitas numeradas. Aluno digita o número.

3. **Dias.** *Só se receita = 5 (custom).* Lista numerada: seg-sex (1-5), todos os dias (0-6), só fim de semana (0,6), customizado. Se customizado: pedir os números (0=dom até 6=sáb) separados por vírgula.

4. **Horários.** *Só se receita = 5.* Em sequência (1 pergunta cada):
   - Hora de início (formato HH:MM, ex: 08:00)
   - Hora de fim (formato HH:MM, ex: 22:00)

5. **Conversão de budget (condicional).** *Só se o adset escolhido tem `daily_budget` (e não `lifetime_budget`).* `adset_schedule` exige `lifetime_budget`. Mostrar:
   ```
   ⚠️ O adset "{nome}" usa orçamento diário (R$ X/dia).
   Pra programar liga/pausa, preciso converter pra orçamento total.

   Não muda o valor do que você gasta, só a forma de cobrança.
   Cálculo: R$ X/dia × {N dias} = R$ Y total.

   1. Pode converter
   2. Não, prefiro deixar como está (cancelo o schedule)

   Digite o número:
   ```
   Se (1) e o adset não tem `end_time`: pedir "Até quando essa campanha deve rodar? (data)".

6. **Escopo de aplicação.** Numerada:
   ```
   Quer aplicar essa programação:
   1. Só nesse adset
   2. Em todos os adsets ativos da campanha {nome}
   3. Em todos os adsets ativos da conta (cuidado, reset em todos)

   Digite o número:
   ```

**Proibido:**
- Pedir `start_minute`, `end_minute`, `pacing_type`, ou qualquer chave da Marketing API direto ao aluno (sempre converter HH:MM internamente).
- Agrupar 2+ inputs na mesma mensagem.
- Pular pro Preview YAML sem passar pelos passos 1-6.

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

**Quando exibir:** sempre, depois de coletar todos os inputs (passos 1-6 da seção "Padrão de coleta"). ANTES do Preview YAML.

**Por que existe:** o Preview YAML mostra `start_minute: 480`, `end_minute: 1320`, `days: [1,2,3,4,5]`, `pacing_type` — números arbitrários que o aluno precisa decodificar. Esse resumo traduz pro português corrente.

**Formato fixo:**

```
📋 Antes de eu mexer no adset, deixa eu te resumir o plano:

O que vai acontecer:
  O adset "{nome}" vai entregar apenas:
  - {Dias em português, ex: "segunda a sexta"}
  - {Janela horária em português, ex: "das 08:00 às 22:00"}
  - Timezone: {timezone, ex: "horário de Brasília"}

  Fora desses horários, o adset fica pausado automaticamente.

Cobertura: {N horas semanais} de entrega vs 168h (semana inteira) → {%}% do tempo.

{Se houve conversão de budget:}
Antes disso, vou converter seu orçamento de R$ X/dia para R$ Y total
(porque programação só funciona com orçamento total). Não muda o que
você gasta, só a forma de cobrança.

Efeito colateral: isso vai disparar reset de aprendizado do adset.
Não use se a campanha tá em fase de aprendizado ativa, exceto se a
perda de dado compensar.

Para reverter (voltar a entregar 24/7): te passo o comando depois.

Tá certo? (sim segue pro YAML, não cancela aqui)
```

**Regras de tradução obrigatórias:**

| Campo técnico | Tradução pro resumo |
|---|---|
| `days: [1,2,3,4,5]` | "segunda a sexta" |
| `days: [0,6]` | "sábado e domingo" |
| `days: [0,1,2,3,4,5,6]` | "todos os dias" |
| `start_minute: 480` | "08:00" |
| `end_minute: 1320` | "22:00" |
| `start_minute: 0` + `end_minute: 1440` | "24 horas (dia inteiro)" |
| `lifetime_budget: 500000` (centavos) | "R$ 5.000 total" |
| `daily_budget: 5000` (centavos) | "R$ 50/dia" |
| `pacing_type: day_parting` | "entrega controlada por horário" |

**Proibido neste resumo:**
- Mostrar minutos desde meia-noite, dias como `[1,2,3,4,5]`, valores em centavos, chaves da Marketing API.
- Pular esse resumo pra ir direto pro YAML.

**Comportamento depois:**
- "sim" → segue pro Preview YAML.
- "não" → "1. Quer ajustar algo, 2. cancelar de vez?". Se ajustar, volta ao passo da coleta correspondente.

## Preview YAML

```yaml
sub_fluxo: liga_pausa_schedule
adset_id: 6123456789
adset_nome: "[Adset] LAL1pct - 25-44"
adset_budget_atual: lifetime_budget = R$ 5.000

schedule:
  dias: [1, 2, 3, 4, 5]                # seg a sex
  janela: 08:00 às 22:00               # 14h por dia
  timezone: America/Sao_Paulo
  total_horas_semanais: 70             # vs 168 (full week) → 41% do tempo

efeitos_esperados:
  - delivery_paused_em_outros_horarios: sim
  - reset_aprendizado: SIM (mudança de pacing)
  - novo_orcamento_diario_efetivo: R$ 5000 / 7 dias / (70/168) = R$ 1714/dia equivalente

confirma aplicar? (digite SIM)
```

## Após aplicar

```
✅ Schedule aplicado: [Adset] LAL1pct - 25-44
   Adset ID: 6123456789

Agora o adset entrega apenas:
- Segunda a sexta
- 08:00 às 22:00 (horário Brasília)

Reset de aprendizado disparado.
Próxima reanálise sugerida: 48h após primeira execução do schedule.

Para reverter (voltar a rodar 24/7):
   POST /6123456789 { "adset_schedule": [], "pacing_type": ["standard"] }

Para ver entrega ao longo do dia depois de 7d:
   /trafego-analise → opção [5] Timing & Sazonalidade
```

## Múltiplos adsets de uma vez

A skill aceita aplicar o mesmo schedule a vários adsets:

```
Quer aplicar essa programação:
[1] Só nesse adset
[2] Em todos os adsets ativos da campanha {nome}
[3] Em todos os adsets ativos da conta (cuidado, vai gerar reset em todos)

Digite o número:
```

## Avisos

- **Reset de aprendizado obrigatório.** Toda mudança de adset_schedule reseta. Não use em campanha em fase de aprendizado ativa, exceto se a perda de dado compensa.
- **Timezone é da ad account**, não do produto. Se a conta foi criada em outro timezone, conferir com `GET /act_<id>?fields=timezone_name`.
- **lifetime_budget exige end_time.** Se adset não tem, a skill pergunta data de término ou não aplica.
- **Delivery não é instantâneo.** Pode levar até 30 min após o `start_minute` para entrega começar (Meta otimiza por leilão).
- **Schedule não funciona com Advantage Campaign Budget (CBO).** Se o adset estiver dentro de campanha CBO, o budget é da campanha e não pode ter `lifetime_budget` por adset. Nesse caso, a skill avisa e sugere mudar a campanha para ABO antes.
