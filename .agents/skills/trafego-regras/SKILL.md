---
name: trafego-regras
description: >
  Cria automações no Meta Ads: (1) regras automáticas que pausam, ajustam orçamento ou
  avisam por e-mail quando um gatilho bate (adrules_library, ações PAUSE, CHANGE_BUDGET,
  CHANGE_CAMPAIGN_BUDGET e NOTIFICATION, todas no mesmo mecanismo nativo da Meta) e
  (2) programação de liga e pausa de conjunto por hora e dia (adset_schedule), além da
  gestão das regras existentes. No modo MCP, a skill desenha a regra e o aluno cria no
  Gerenciador com passo a passo, porque o conector não tem regra automática; a programação
  de liga e pausa segue pelo MCP. No modo App, tudo pela Marketing API. Tudo roda na
  estrutura da Meta, sem depender do computador do aluno ligado. Use quando o aluno pedir
  "automatizar", "regra automática", "se CPA passar de X pause", "me avisa por e-mail se o
  gasto passar de R$ 500", "rodar campanha só em horário comercial", "programar liga e pausa".
user-invocable: true
---

# Tráfego Regras. Automação, Alertas e Programação

Você cria automações de tráfego em 3 frentes: regras automáticas da Meta (pausar, mexer no orçamento ou avisar por e-mail), programação de entrega por horário dos conjuntos e gestão das regras já criadas. Tudo passa por resumo e confirmação, e roda na estrutura da Meta, sem depender do computador do aluno.

---

## 🛡️ Gate obrigatório antes de qualquer escrita na conta

Toda escrita segue a seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API" do CLAUDE.md, nos dois modos:

1. **Resumo em linguagem natural** (sem ID, sem JSON, sem valor em centavos). O aluno confirma o plano.
2. **Bloco 🛡️ com o Preview YAML.** Um "sim" por lote: criar a regra e anexar o aviso por e-mail é um lote; aplicar a mesma programação em 5 conjuntos é um lote.
3. Executar sem reabrir o gate, a não ser que uma chamada falhe, o aluno mude o plano ou surja escrita fora do lote.
4. **Excluir regra nunca entra num lote** e nunca roda por `curl -X DELETE` direto (regra 7 do gate). A alternativa padrão é **desativar** a regra (status `DISABLED`), que é reversível. Se o aluno quiser mesmo apagar: bloco 🛡️ próprio e, depois do "sim", exclusão pelo Gerenciador ou por comando sem token que o próprio aluno roda (ver `sub-skills/gerir-regras.md`, Fluxo E).
5. Nunca exibir `curl` com token. Proibido heredoc Python e `curl | python3` com token.

**Quando a skill não escreve** (modo MCP, regra criada pelo aluno no Gerenciador): não há bloco 🛡️, porque quem aperta o botão é o aluno. A skill desenha a regra, revisa os limites de segurança e conduz o passo a passo.

**Não passam pelo gate:** leituras (listagem, histórico, campos), por tool `ads_get_*` ou `GET`.

| Operação | MCP (`MCP_CONECTOR`) | App (`curl`) |
|---|---|---|
| Criar regra automática | passo manual guiado no Gerenciador (Regras automatizadas) | `POST /act_<id>/adrules_library` |
| Listar regras e ver histórico | passo manual guiado no Gerenciador | `GET /act_<id>/adrules_library`, `GET /<rule_id>/history` |
| Ativar, desativar, editar regra | passo manual guiado no Gerenciador | `POST /<rule_id>` |
| Excluir regra (sempre à parte) | exclusão manual no Gerenciador | sem `curl -X DELETE` direto: Gerenciador ou comando sem token para o aluno rodar |
| Programar liga e pausa do conjunto | `ads_update_entity` (`adset_schedule` + `pacing_type`) | `POST /<adset_id>` |
| Trocar orçamento diário por total | `ads_update_entity` (`lifetime_budget` + `end_time`), costuma ser recusado em conjunto já publicado | `POST /<adset_id>`, mesma ressalva |
| Leituras de apoio (escopo, CBO ou ABO, orçamento) | `ads_get_ad_entities` | `GET` na Graph API |

---

## 🔌 Passo 0 obrigatório (antes de qualquer leitura ou escrita)

1. **Produto ativo.** Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md`, seguindo a seção "Contexto Persistente do Negócio" do CLAUDE.md. O resumo traz o **preço** (ticket) e o **tipo** (low, middle ou high ticket), usados nas validações de gatilho (ex: CPA menor que metade do ticket, janela mínima de high ticket). Só perguntar ao aluno o que o resumo não tem (CPA alvo, margem).
2. **Conexão Meta.** Ler `META_AUTH_MODO` com `grep "^META_AUTH_MODO=" .env | cut -d= -f2-`.
   - **Vazio:** acionar `/trafego-conexao`.
   - **`MCP_CONECTOR`:** confirmar uma tool cujo nome termina em `ads_get_ad_accounts` (descobrir sempre pelo final do nome). Conta não liberada no conector: explicar e oferecer o modo App pelo `/trafego-conexao`.
   - **`APP`:** confirmar com `grep -q` `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID`.
3. **Roteamento por sub-fluxo:**

| Sub-fluxo | Mecanismo Meta | No MCP | No App |
|---|---|---|---|
| **[1] Regra automática** (criar) | `adrules_library` | a skill desenha, o aluno cria no Gerenciador (passo manual guiado) | `curl` |
| **[2] Liga e pausa por horário** | `adset_schedule` (campo do conjunto) | `ads_update_entity` | `curl` |
| **[3] Gerir regras** (listar, ativar, desativar, editar, excluir, histórico) | `adrules_library` | passo manual guiado no Gerenciador | `curl` (excluir sem `DELETE` direto) |

4. **`adrules_library` não tem tool no MCP**, nem de leitura. No modo MCP a skill nunca monta `POST /adrules_library`: ela desenha a regra com o aluno (gatilho, ação, escopo, frequência, gasto mínimo), passa pelas validações e conduz a criação manual. A descoberta de administradores do Business (para quem recebe o e-mail) também não existe no MCP: no Gerenciador, o aluno escolhe as pessoas na própria tela da regra.
5. **Leituras de apoio** (listar campanhas e conjuntos, detectar CBO ou ABO, ler orçamento): `ads_get_ad_entities` no MCP ou `GET` no App.

**Princípios:**
- Toda regra criada nasce **desativada** (no App, `status: DISABLED`, que o Gerenciador mostra como "Pausada"; no MCP, o aluno desliga a regra logo depois de criar). O aluno ativa de forma explícita depois de revisar.
- Resumo e confirmação antes de criar.
- Intervalo mínimo de 24h entre ações da mesma regra (evita pausar e reativar em ciclo).
- Toda regra tem um jeito documentado de desfazer: desativar (reversível) ou excluir à parte.
- Todas as regras vão para `meus-produtos/_global/trafego/regras/INDEX.md`.

---

## 1. Sub-fluxos disponíveis

O command `/trafego-regras` apresenta o menu:

```
[1] Regra automática Meta Ads          criar regra nova (gatilho + ação)
[2] Liga e pausa por horário           programação de entrega por hora e dia da semana
[3] Gerir regras existentes            listar, ativar, desativar, editar, excluir, ver histórico
```

Documentação de cada um:
- `sub-skills/regra-automatica.md` (as 4 ações: PAUSE, CHANGE_BUDGET, CHANGE_CAMPAIGN_BUDGET, NOTIFICATION)
- `sub-skills/liga-pausa-schedule.md`
- `sub-skills/gerir-regras.md`

> **Nota de arquitetura:** o aviso por Telegram ou WhatsApp foi descartado. A rotina agendada do Claude não foi feita para carregar credenciais do `.env` no disparo remoto, o que prenderia o aviso ao computador do aluno ligado. O e-mail nativo da Meta cobre o mesmo caso e virou **uma das ações** da regra automática (sub-fluxo [1], ação 4). Para resumo semanal agendado (toda segunda às 8h, resumo da semana), usar o Gerenciador (Relatórios agendados). Para relatório diário pelo WhatsApp ou Telegram, o Severino tem `/ads-relatorio`.

---

## 2. Endpoints

### 2.1 Regra automática (modo App)

> No modo MCP não existe tool para `adrules_library`. Estes endpoints são só do modo App.

```
POST   /act_<id>/adrules_library
GET    /act_<id>/adrules_library
POST   /<rule_id>?execution_options=["execute_immediately"]   (executar uma vez sem esperar o gatilho)
POST   /<rule_id>  { "status": "DISABLED" }                    (desativar: forma de desfazer padrão)
GET    /<rule_id>/history                                      (histórico de execução)
```

API `v25.0`. Permissão: `ads_management`.

A mesma chamada (`POST /adrules_library`) cobre **4 ações** pelo campo `execution_spec.execution_type`:

| Ação (Marketing API) | O que faz | Quando usar |
|---|---|---|
| `PAUSE` | Pausa a entidade quando o gatilho bate | Cortar gasto ruim sozinho (ex: CPA estourou) |
| `CHANGE_BUDGET` | Ajusta o orçamento do **conjunto** em % (para mais ou para menos) | Escalar ou frear conjuntos com orçamento próprio (ABO). ⚠️ Não funciona em CBO: usar `CHANGE_CAMPAIGN_BUDGET` |
| `CHANGE_CAMPAIGN_BUDGET` | Ajusta o orçamento da **campanha** em % | Escalar ou frear a campanha inteira (CBO ou ABO). Único caminho automático para mexer em orçamento de CBO |
| `NOTIFICATION` | Envia e-mail para o administrador do Business | Só avisar, sem agir (monitoramento, oportunidade) |

O aviso chega por e-mail para o administrador do Business, por notificação no app do Gerenciador de Anúncios (se instalado) e no sino do business.facebook.com. **Não vai para Telegram nem WhatsApp.**

### 2.2 Gestão de regras (modo App)

```
GET    /act_<id>/adrules_library?fields=...          (listar)
POST   /<rule_id>  { status: ENABLED | DISABLED }    (ativar ou desativar)
POST   /<rule_id>  { evaluation_spec | execution_spec | ... }   (editar)
GET    /<rule_id>/history?fields=...                 (histórico)
```

Listar e histórico são leitura (sem gate). Ativar, desativar e editar passam pelo bloco 🛡️. **Excluir** não roda por `curl` direto: ver Fluxo E da `gerir-regras.md`.

### 2.3 Liga e pausa por horário (MCP e App)

> `adset_schedule` é campo do conjunto. MCP: `ads_update_entity` passando `adset_schedule` + `pacing_type`. App: o `curl` abaixo.

```
POST /<adset_id>
{
  "adset_schedule": [
    { "start_minute": 480, "end_minute": 1320, "days": [1,2,3,4,5] }
  ],
  "pacing_type": ["standard", "day_parting"]
}
```

- `start_minute` e `end_minute` são minutos desde a meia-noite (480 = 08:00, 1320 = 22:00).
- `days`: 0 = domingo, 1 = segunda, ..., 6 = sábado.

**`adset_schedule` exige orçamento total** (`lifetime_budget`), não funciona com orçamento diário. **Trocar orçamento diário por total num conjunto já publicado costuma ser recusado pela Meta.** A skill confere antes e explica as saídas (ver `sub-skills/liga-pausa-schedule.md`).

---

## 3. Convenção de nome

```
[WS] {tipo}-{descricao}-{produto-slug}
```

Exemplos:
- `[WS] AutoRule-PauseCPAGT40-curso-tarot`
- `[WS] AutoRule-Boost20PctROASGT3-curso-tarot`
- `[WS] AutoRule-AlertSpendGT500-curso-tarot`
- `[WS] Schedule-segxsex-8x22-curso-tarot`

O sufixo é o slug do produto ativo.

---

## 4. Intervalo entre ações e segurança

| Tipo de ação | Intervalo mínimo |
|---|---|
| Pausar conjunto ou anúncio | 24h (não reativa antes) |
| Aumentar orçamento % | 24h |
| Reduzir orçamento % | 24h |
| Só avisar | 1h |

A regra é **avaliada** a cada 30 minutos (padrão da Meta).

A skill **bloqueia** a criação se:
- O gatilho pode causar ciclo (ex: pausar se CPA > 40 e reativar se CPA < 30; a Meta não reativa sozinha, mas evitar configurações em conflito).
- O gatilho não tem janela mínima de avaliação (ex: CPA com janela "hoje" pode disparar com 2 conversões).
- A janela do gatilho tem gasto menor que 1 vez o CPA alvo (dado imaturo).

---

## 5. Saída

```yaml
operacao: criar_regra
sub_fluxo: regra_automatica | liga_pausa_schedule
modo: MCP_CONECTOR (criada pelo aluno no Gerenciador) | APP
ad_account_id: act_<id>

regra_criada:
  id: <rule_id> | "criada no Gerenciador (sem ID registrado)"
  nome: "[WS] AutoRule-PauseCPAGT40-curso-tarot"
  tipo: meta_adrule | adset_schedule
  status: desativada                 # toda regra nasce desativada
  gatilho:
    metrica: cpa
    operador: greater_than
    valor: 40.0
    janela: "last_3d"
  acao:
    tipo: pause | adjust_budget | notify
    valor: -100% | +20% | null
  escopo:
    nivel: campaign | adset | ad
    filtro: "campanhas de vendas"
  intervalo_horas: 24
  como_desfazer: "desativar a regra (/trafego-regras → [3] → C) ou excluir à parte (Fluxo E)"
  como_ativar: "/trafego-regras → [3] → B, ou no Gerenciador"

invalidacoes:
  - cache_trafego_insights: stale (a regra pode mudar campanhas)

handoffs_sugeridos:
  - texto: "Revisar as campanhas afetadas pela regra"
    skill: /trafego-otimizar
```

---

## 6. Arquivos locais

Regras pertencem à conta de anúncios, não a um produto:

```
meus-produtos/_global/trafego/regras/
├── INDEX.md               (todas as regras criadas ou desenhadas pela skill)
└── {rule_id}.md           (uma por regra: configuração completa e histórico;
                            regra criada no Gerenciador usa o nome em vez do ID)
```

`INDEX.md` é regravado a cada criação ou listagem. Ao criar ou ativar regra, marcar como desatualizado o cache do `/trafego-insights` da conta (regra em `.claude/skills/trafego-insights/sub-skills/cache.md`).

---

## 7. Princípios que esta skill nunca viola

1. **Toda regra nasce desativada.** O aluno ativa depois.
2. **Resumo e bloco 🛡️ antes de escrever.**
3. **Um "sim" por lote.** Exclusão sempre à parte, nunca por `curl -X DELETE` direto.
4. **Intervalo mínimo** entre ações para evitar ciclo.
5. **Jeito de desfazer documentado:** desativar primeiro, excluir só se o aluno insistir.
6. **Não cria regra com janela de dado imaturo.**
7. **Convenção de nome** `[WS] tipo-descricao-produto`.
8. **Programação por horário exige orçamento total.** A skill confere antes e explica a recusa comum da Meta na troca.
9. **O aviso usa o canal nativo da Meta** (e-mail, app do Gerenciador, sino do business.facebook.com).
10. **No modo MCP, a skill não finge que criou.** Ela desenha a regra, o aluno cria no Gerenciador e a skill registra o que foi combinado.
11. **Não inventa regra.** Pedido fora dos 3 sub-fluxos: encaminhar ao Gerenciador.
