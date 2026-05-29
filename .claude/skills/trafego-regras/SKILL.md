---
name: trafego-regras
description: >
  Cria automações no Meta Ads via Marketing API: (1) regras automáticas que pausam,
  ajustam budget OU notificam por email quando trigger bate (adrules_library com ação
  PAUSE / CHANGE_BUDGET / CHANGE_CAMPAIGN_BUDGET / NOTIFICATION — todas no mesmo mecanismo nativo do Meta), e
  (2) schedule de liga/pausa de adset por hora/dia (adset_schedule). Tudo roda na
  infraestrutura do Meta, sem dependência do Mac do aluno. Cobre triggers como "se CPA
  > X pause", "se ROAS > Y aumenta budget %", "me avisa por email se gasto passar de
  R$ 500" e "rodar campanha só em horário comercial". Use quando o aluno pedir
  "automatizar", "criar regra", "alerta automático", "programar liga/pausa".
user-invocable: false
---

## 🛡️ Gate obrigatório antes de qualquer escrita na Graph API

Esta skill executa operações que **modificam estado** na conta Meta Ads. Antes de chamar qualquer endpoint POST/PUT/DELETE da Graph API, **siga a regra global definida em [CLAUDE.md](../../../CLAUDE.md)** na seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API":

1. Apresentar o bloco `🛡️ Confirmação necessária antes de tocar na conta Meta` com operação, endpoint humano-legível, o que vai mudar, impacto no aprendizado e reversibilidade.
2. **Nunca exibir o `curl` completo no chat** — carrega o token.
3. Aguardar resposta `sim` (ou variante explícita: aprovo, pode, manda) antes de executar.
4. Em modo lote, mostrar o plano completo antes e pedir confirmação única.
5. Se o aluno responder `não` ou variante (cancelar, abortar), abortar sem chamar a API.
6. **NUNCA usar `python3 << 'EOF'` (heredoc) nem `curl | python3 -c`** com o token. Esses formatos quebram o pattern matching do Claude Code e expõem o token no pop-up nativo. Ver regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md.

**Operações desta skill que passam pelo gate:**

- POST /act_<id>/adrules_library (criar regra automática)
- POST /<rule_id> com status (ativar/desativar regra)
- POST /<adset_id>/scheduled_changes (programar liga/pausa)

**Não passam pelo gate:** chamadas GET para leitura (insights, listagens, fields). Estado não muda.

---

# Tráfego Regras. Automação, Alertas e Agendamento

Você cria automações de tráfego em 3 dimensões: regras automáticas do Meta Ads (pausar/ajustar budget), alertas automáticos via email nativo do Meta e programação de delivery schedule de adsets. Toda criação passa por preview e confirmação. Tudo roda na infraestrutura do Meta, sem dependência do Mac do aluno estar ligado.

**Princípios:**
- Toda regra criada nasce **PAUSED**. Aluno ativa explicitamente após confirmar.
- Preview YAML obrigatório antes do POST.
- Cooldown mínimo de 24h entre execuções da mesma regra (evita pausar/reativar em loop).
- Toda regra tem rollback documentado (DELETE + comando de reversão).
- Todas as regras criadas vão para `meus-produtos/{ativo}/trafego/regras/INDEX.md`.

---

## 1. Sub-fluxos disponíveis

A skill é orquestrada pelo command `/trafego-regras`, que apresenta o menu:

```
[1] Regra automática Meta Ads          criar nova regra (trigger + ação)
[2] Programação liga/pausa adset       schedule de delivery por hora/dia da semana
[3] Gerir regras existentes            listar, ativar, pausar, editar, excluir, ver histórico
```

Cada sub-fluxo está documentado em:
- `sub-skills/regra-automatica.md` (cobre as 4 ações: PAUSE, CHANGE_BUDGET, CHANGE_CAMPAIGN_BUDGET, NOTIFICATION)
- `sub-skills/liga-pausa-schedule.md`
- `sub-skills/gerir-regras.md` (gestão completa de regras já criadas)

> **Nota arquitetural:** versões anteriores da skill tinham um menu separado pra "alerta automático" via Telegram/WhatsApp (`/schedule` + canal externo). Isso foi descartado em 2026-05-16 porque o `/schedule` da Anthropic não foi projetado pra carregar credenciais locais (`.env`) no momento do disparo remoto, criando dependência do Mac do aluno estar ligado. A notificação por email do Meta, que cobre o mesmo caso de uso, foi consolidada como **uma das ações** da regra automática (sub-fluxo [1], opção 4 do passo "Ação"). Pra digest semanal agendado (toda segunda 8h, resumo da semana), usar a UI do BM (Configurações > Relatórios Agendados).

---

## 2. Endpoints e integrações

### 2.1 Regra automática (Marketing API)
```
POST   /act_<id>/adrules_library
GET    /act_<id>/adrules_library
POST   /<rule_id>?execution_options=["execute_immediately"]   (executar uma vez sem aguardar trigger)
DELETE /<rule_id>                                              (rollback)
GET    /<rule_id>/history                                      (histórico de execução)
```

API version: `v25.0`. Permissões: `ads_management`.

A mesma chamada (`POST /adrules_library`) cobre **4 ações possíveis** via campo `execution_spec.execution_type`:

| Ação (Marketing API) | O que faz | Quando usar |
|---|---|---|
| `PAUSE` | Pausa a entidade quando trigger bate | Cortar gasto ruim automaticamente (ex: CPA estourou) |
| `CHANGE_BUDGET` | Ajusta budget de **adset** em % (positivo ou negativo) | Escalar/desacelerar adsets ABO com budget próprio. ⚠️ Não funciona em CBO — usar `CHANGE_CAMPAIGN_BUDGET`. |
| `CHANGE_CAMPAIGN_BUDGET` | Ajusta budget de **campanha** em % (positivo ou negativo) | Escalar/desacelerar campanha inteira (CBO ou ABO). Único caminho automatizado de mexer em budget de CBO. |
| `NOTIFICATION` | Envia email pro admin do BM | Só alertar sem agir (monitoramento preventivo, oportunidade) |

Notificação chega por email pro admin do BM, push no Ads Manager mobile (se instalado) e sino do business.facebook.com. **Não vai pra Telegram/WhatsApp** (decisão arquitetural — ver nota acima do menu).

A skill `regra-automatica.md` cobre as 4 ações no mesmo fluxo. O aluno escolhe qual no passo "Ação".

### 2.2 Gestão de regras existentes (Marketing API)

```
GET    /act_<id>/adrules_library?fields=...        (listar todas)
POST   /<rule_id>  { status: ENABLED|DISABLED }   (ativar/pausar)
POST   /<rule_id>  { evaluation_spec|execution_spec|... }  (editar campo)
DELETE /<rule_id>                                  (excluir)
GET    /<rule_id>/history?fields=...               (histórico de execução)
```

Listagem e histórico são GET (não passam pelo gate). Ativar, pausar, editar e excluir são POST/DELETE (passam pelo gate 🛡️ obrigatório). Excluir exige confirmação dupla (texto "EXCLUIR" em maiúsculas + sim no gate).

Sub-skill `gerir-regras.md` cobre os 6 fluxos (listar/ativar/pausar/editar/excluir/histórico) reusando a tabela de tradução PT e o resumo natural da `regra-automatica.md`.

### 2.3 Liga/pausa schedule (Marketing API)
```
POST /<adset_id>
{
  "adset_schedule": [
    { "start_minute": 480, "end_minute": 1320, "days": [1,2,3,4,5] }
  ],
  "pacing_type": ["standard", "day_parting"]
}
```

- `start_minute`/`end_minute` são minutos desde meia-noite (480 = 08:00, 1320 = 22:00).
- `days`: 0=domingo, 1=segunda, ..., 6=sábado.

Importante: `adset_schedule` exige que o adset tenha `lifetime_budget` (não funciona com `daily_budget`). A skill avisa e pode ajudar a converter.

---

## 3. Convenção de nomenclatura

Toda regra criada por esta skill segue padrão:

```
[FC] {tipo}-{descricao}-{produto-slug}
```

Exemplos:
- `[FC] AutoRule-PauseCPAGT40-curso-tarot`
- `[FC] AutoRule-Boost20PctROAS3-curso-tarot`
- `[FC] Resumo-segunda-8h-curso-tarot`
- `[FC] Schedule-segxsex-8x22-curso-tarot`

---

## 4. Cooldown e segurança

Toda regra criada tem **cooldown mínimo** para evitar oscilação:

| Tipo de ação | Cooldown |
|---|---|
| Pausar adset/ad | 24h (não reativa antes) |
| Aumentar budget % | 24h |
| Reduzir budget % | 24h |
| Notificar (sem ação) | 1h (pode notificar mais frequente) |

Frequência de **avaliação** da regra: a cada 30 minutos (default Meta).

A skill **bloqueia** criação de regra se:
- Trigger pode causar loop (ex: pausar se CPA > 40, reativar se CPA < 30 — Meta não tem reativação automática, mas evitar configurações conflitantes).
- Trigger sem janela mínima de avaliação (ex: avaliar CPA com janela "today" + lookback 1h pode disparar com 2 conversões).
- Janela do trigger com gasto < 1× CPA target (dado imaturo).

---

## 5. Output esperado

```yaml
operacao: criar_regra
sub_fluxo: regra_automatica | liga_pausa_schedule
ad_account_id: act_<id>

regra_criada:
  id: <rule_id>
  nome: "[FC] AutoRule-PauseCPAGT40-curso-tarot"
  tipo: meta_adrule | schedule_workshop | adset_schedule
  status: paused                 # toda regra nasce PAUSED
  trigger:
    metrica: cpa
    operador: greater_than
    valor: 40.0
    janela_lookback: "last_3d"
  acao:
    tipo: pause | adjust_budget | notify
    valor: -100% | +20% | null
  scope:
    nivel: campaign | adset | ad
    ids: [...]
    filtro: "campanhas com objective=OUTCOME_SALES"

  cooldown_horas: 24
  rollback_comando: "DELETE /<rule_id>"
  comando_para_ativar: "POST /<rule_id> { status: ENABLED }"

invalidacoes:
  - cache_trafego_insights: stale (regra pode mudar campanhas)

handoffs_sugeridos:
  - texto: "Para revisar campanhas afetadas pela regra"
    skill: /trafego-otimizar
  - texto: "Para ver histórico de execução da regra"
    comando: "GET /<rule_id>/history"
```

---

## 6. Arquivo local de regras

A skill mantém:
```
meus-produtos/{ativo}/trafego/regras/
├── INDEX.md               (lista de todas as regras criadas)
├── {rule_id}.md           (uma por regra, com payload completo + histórico de execução)
└── resumos/               (configurações dos resumos recorrentes)
    └── {schedule_id}.md
```

`INDEX.md` é regenerado a cada criação ou listagem.

---

## 7. Princípios que esta skill nunca viola

1. **Toda regra nasce PAUSED.** Aluno ativa depois.
2. **Preview obrigatório.** YAML antes do POST.
3. **Confirmação SIM.** Sem isso, não cria.
4. **Cooldown mínimo** para evitar oscilação.
5. **Rollback documentado** sempre.
6. **Não cria regra com janela de dado imaturo.**
7. **Convenção de nomenclatura** `[FC] tipo-descricao-produto`.
8. **Schedule de adset exige lifetime_budget.** Avisa antes de tentar.
9. **A ação "notificar" usa canal nativo do Meta.** Email pro admin do BM, push no Ads Manager mobile, sino do business.facebook.com. Não usa Telegram/WhatsApp (decisão arquitetural — ver nota acima do menu).
10. **Não inventa regra.** Se aluno pedir algo fora dos 3 sub-fluxos (criar regra automática + liga/pausa schedule + gerir regras existentes), encaminha para o Gerenciador de Anúncios.
