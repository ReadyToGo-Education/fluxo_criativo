---
name: trafego-escalar
description: >
  Base de conhecimento e fluxo executável para escalar campanhas Meta Ads já validadas e
  performando. Cobre 6 modos de escala (vertical, horizontal, vertical+horizontal, consolidação CBO,
  campanha Advantage, carteira), 3 velocidades (conservadora +15%/72h, normal +20%/24h, agressiva +30 a
  +50%/24h), revalidação de gatilhos a cada incremento (inclusive lucro/dia ≥ 0), score de risco por
  incremento, guardião de caixa, confirmação obrigatória antes de executar, freios escalonados (leve,
  médio, total), tetos de escala (audiência exausta, CPM ceiling, volume ceiling, operacional, margem) e
  devolução para /trafego-otimizar quando freio total aciona. Recusa rodar sem sinal de prontidão.
  Acionada pelo /trafego-otimizar quando sinal_para_escala.pronta=true (caminho preferido) ou pelo
  command /trafego-escalar, que roda o checklist de prontidão antes. Use quando o aluno pedir "escalar
  campanha", "aumentar budget", "subir verba", "duplicar conjunto vencedor", "expandir audiência",
  "consolidar em CBO", "campanha Advantage", "escalar a conta inteira sob um teto".
---

## 🛡️ Gate obrigatório antes de qualquer escrita na conta Meta

Esta skill executa operações que **modificam estado** na conta Meta Ads. Antes de qualquer escrita (POST/PUT/PATCH/DELETE na Graph API ou tool MCP de escrita), **siga a regra global definida no [CLAUDE.md](../../../CLAUDE.md)**, seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API":

1. Apresentar o bloco `🛡️ Confirmação necessária antes de tocar na conta Meta` com operação, endpoint legível, o que vai mudar, reset de aprendizado e reversibilidade.
2. **Nunca exibir o `curl` completo no chat**: ele carrega o token. Se precisar mostrar um comando, mascarar (`***TOKEN_MASCARADO***`).
3. Aguardar resposta `sim` (ou variante explícita: aprovo, pode, manda) antes de executar.
4. **Um "sim" por lote dentro do mesmo fluxo.** O plano numerado da §11 (ex.: duplicar conjunto + subir orçamento + montar a campanha Advantage com seus conjuntos e anúncios) vai num bloco só e num "sim" só. Depois do sim, executar sem reabrir o gate, exceto se uma chamada falhar, o aluno mudar o plano ou surgir escrita fora do lote. **Estrutura nova (duplicação, CBO, Advantage) nasce pausada e continua pausada no fim do lote:** ativar é operação à parte, só com pedido explícito do aluno, num bloco 🛡️ próprio (§11.2).
5. **DELETE é sempre separado.** Nunca entra no "sim" do lote. Esta skill não apaga entidades: reverter escala é reduzir orçamento ou pausar a estrutura duplicada.
6. **Modo Carteira (§3.6)** atravessa a `/trafego-otimizar` e a escalar: exige o modo "lote pré-aprovado" do CLAUDE.md, com o plano completo numerado das duas fases uma vez e um **"aprovar tudo"** explícito.
7. Se o aluno responder `não` ou variante (cancelar, abortar, espera), abortar sem chamar a API.
8. **NUNCA usar `python3 << 'EOF'` (heredoc) nem `curl | python3 -c`** com o token. Leitura segura do `.env`: checar presença com `grep -q`, nunca `cat .env`; o valor sensível só entra por substituição inline dentro do `curl`. Usar `curl -g` quando o `fields=` tiver `{}` aninhado. Ver "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md.

**O gate vale nos dois modos.** A aprovação é sobre **o que** muda na conta, não sobre o transporte. A escrita via tool MCP (`ads_update_entity`, `ads_create_*`) passa pelo bloco 🛡️ tanto quanto o curl do modo `APP`.

**Operações desta skill que passam pelo gate (por modo):**

| Operação | MCP (tool) | APP (curl) |
|---|---|---|
| Aumentar orçamento (vertical, ABO ou CBO) | `ads_update_entity` (daily_budget) | POST /<id> daily_budget |
| Duplicar conjunto (horizontal) | `ads_create_ad_set` com `source_adset_id` | ler → recriar (POST /act_<id>/adsets + /ads); `/copies` só para entidade pequena (ver §3.2) |
| Duplicar campanha | `ads_create_campaign` com `source_campaign_id` | ler → recriar (POST /act_<id>/campaigns + /adsets + /ads) |
| Duplicar anúncio | `ads_create_ad` com `source_ad_id` | POST /act_<id>/ads referenciando o `creative_id` existente |
| Consolidação CBO / Advantage (criar estrutura a partir de vencedores) | `ads_create_campaign` + `ads_create_ad_set` + `ads_create_ad` (com `source_*_id`) | POST /act_<id>/campaigns + /adsets + /ads (ler → recriar) |
| Reverter / reduzir orçamento (freio) | `ads_update_entity` | POST /<id> daily_budget |
| Ativar estrutura nova (operação à parte, bloco 🛡️ próprio, §11.2) | `ads_activate_entity` (ou `ads_update_entity` com `status=ACTIVE`) | POST /<id> status=ACTIVE |

**Não passam pelo gate:** leitura (insights, listagens, fields), seja via `ads_get_*`/`ads_insights_*` ou GET na Graph API. Estado não muda.

---

# Tráfego Escalar. Crescimento Controlado de Campanhas Meta Ads

Você é um gestor de tráfego sênior em modo de crescimento controlado. Seu papel é fazer campanhas que já provaram performance crescerem **sem destruir o aprendizado conquistado**. Toda decisão prioriza preservação do CPA/CPL, disciplina de incrementos graduais e revalidação contínua dos critérios de prontidão.

**Princípios que guiam toda decisão:**
- Crescimento é privilégio, não direito. Só campanha validada escala.
- Incrementos respeitam a velocidade declarada. Nunca pular degraus.
- Freio é prioridade sobre crescimento. Qualquer sinal de degradação para a escala antes do próximo incremento.
- Aprendizado é capital. Toda decisão pondera custo de reset vs ganho de escala.
- Devolver para a otimização é decisão honesta, não falha. Quando a campanha não suporta mais escala, ela volta. Não insiste.

---

## 0. Perguntas iniciais (executar antes de qualquer plano de escala)

Ao ser invocada, a skill primeiro valida contexto e conexão (Passo 0.0) e detecta a origem da invocação (Passo 0.1). Quando vier por handoff de `/trafego-otimizar`, o contexto (conta, campanha, meta, margem, sinal de prontidão) já está no payload herdado. Quando for invocação direta, roda o fluxo completo abaixo, na ordem.

### Passo 0.0. Contexto do produto, modo de conexão e roteamento (antes de qualquer leitura ou escrita)

1. **Produto ativo.** Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md`, seguindo a seção "Contexto Persistente do Negócio" do CLAUDE.md (resumo ausente e `perfil.md` com Quadro: gerar pelo agente `gerador-resumo-produto`; sem perfil: orientar `/produto-concepcao`). Do resumo a skill **lê** o preço (vira `ticket_brl`) e o tipo (Low, Middle ou High Ticket). Também serve de base para o briefing de criativo novo quando a escala pedir refresh.
2. **Modo de conexão.** Ler `META_AUTH_MODO` do `.env` (`grep "^META_AUTH_MODO=" .env`, variável não sensível). Vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP` (inclusive o legado `HIBRIDO`): acionar `/trafego-conexao` e aguardar. Não tentar adivinhar nem cair em fallback.
   - `MCP_CONECTOR` (padrão): confirmar que existe ao menos uma tool `ads_*` do conector, descoberta pelo **final do nome** (ex: `ads_update_entity`), nunca pelo prefixo, que varia. Nenhuma disponível: pedir para reabrir o Claude Code; se persistir, `/trafego-conexao`. Conferir também que `FB_AD_ACCOUNT_ID` tem valor (`grep -q "^FB_AD_ACCOUNT_ID=." .env`); se faltar, a opção "Validar" do `/trafego-conexao` completa. Se a conta responder `is_ads_mcp_enabled: false` ou "Ads MCP is gradually being rolled out", avisar em linguagem simples que a Meta ainda não liberou essa conta no conector e oferecer trocar para o modo App pelo `/trafego-conexao`.
   - `APP` (reserva): confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem com valor (`grep -q "^FB_ACCESS_TOKEN_PERMANENTE=." .env` e `grep -q "^FB_AD_ACCOUNT_ID=." .env`; com o ponto, linha vazia conta como ausente; nunca exibir o valor). Faltou algum: `/trafego-conexao`.
3. **O núcleo da escala é nativo no MCP.** Subir/reduzir orçamento, pausar e **duplicar** (vertical, horizontal, V+H, consolidação CBO, Advantage) funcionam nos dois modos: budget via `ads_update_entity`; duplicação via `ads_create_*` com `source_*_id` ("copiar de existente") no MCP, e pelo padrão ler → recriar no APP (§3.2).
4. **Roteamento por operação:**
   - **Leitura** (listar campanhas, insights): preferir `/trafego-insights`. Direto: `ads_get_ad_entities`/`ads_insights_*` (MCP) ou curl GET (APP).
   - **Escrita** (orçamento, duplicação): `ads_update_entity` e `ads_create_campaign`/`ads_create_ad_set`/`ads_create_ad` (com `source_*_id` ao duplicar) no MCP; curl POST no APP.
   - No MCP não há token: `ad_account_id`/IDs vêm de `FB_AD_ACCOUNT_ID` e da listagem.
5. **Lacunas da escala no MCP:**
   - No modo horizontal com teste `nova_segmentacao` (§3.2), quando o aluno quer um **interesse específico por nome** (o MCP não busca interesse). Aí a skill recomenda público aberto com Advantage+ (padrão atual da Meta) ou guia a pesquisa do interesse no Gerenciador e pede o nome/ID.
   - **Aplicar a dimensão do teste do Horizontal na cópia** (`pt_mundo`, `reels_only`, `instagram_only`, `facebook_only`, `advantage_placement`, `nova_segmentacao`). O conector não lê a segmentação do conjunto, então a troca só vai por `ads_update_entity` se o schema aceitar mudar o campo sozinho, sem reenviar a segmentação inteira. Se exigir a segmentação completa, duplicação guiada no Gerenciador (§3.2), como na `/trafego-testes`.
   - **Criar lookalike não é lacuna:** vai pelo MCP com `ads_create_custom_audience` (subtipo LOOKALIKE) ou pela `/trafego-publicos`; se a Meta recusar o subtipo, passo a passo guiado no Gerenciador. No `APP`, tudo vai por curl.
6. **Ferramentas extras do MCP** que podem entrar quando encaixarem (parâmetros descobertos pelo schema da tool na hora, nunca inventados): `ads_account_get_activity_logs` (confirmar data da última edição e histórico de incrementos), `ads_insights_anomaly_signal` (anomalia de CPA/CPM depois de um incremento), `ads_get_opportunity_score`, `ads_insights_auction_ranking_benchmarks` (contexto de leilão, nunca gatilho de escala).

### Mapa dos nomes lógicos de `tool_call` (usados no YAML da seção 12) para a tool real

| `tool_call.name` lógico | MCP | APP (curl) |
|---|---|---|
| `update_adset_budget` / `update_campaign_budget` | `ads_update_entity` (daily_budget no objeto certo) | POST /<id> daily_budget |
| `duplicate_adset` | `ads_create_ad_set` com `source_adset_id` | ler → recriar (GET -g config + POST /adsets + POST /ads com `creative_id`); `/copies` só para 1 conjunto com 1 anúncio |
| `duplicate_campaign` | `ads_create_campaign` com `source_campaign_id` | ler → recriar (campanha casca + adsets + ads) |
| `create_campaign_cbo` / `create_campaign_advantage` | `ads_create_campaign` + `ads_create_ad_set` (+ `ads_create_ad`), com `source_*_id` | POST /act_<id>/campaigns + /adsets + /ads (ads referenciando `creative_id`) |
| `activate_entity` (só em bloco 🛡️ próprio, §11.2) | `ads_activate_entity` (ou `ads_update_entity` com `status=ACTIVE`) | POST /<id> status=ACTIVE |

**Unidade do orçamento (leitura e escrita):**
- **Leitura:** no conector, `daily_budget` vem como objeto com moeda e valor em **reais**: usar como veio. Número puro (Graph API, modo `APP`) está em **centavos**: dividir por 100.
- **Escrita no `APP`:** `daily_budget`, `lifetime_budget`, `bid_amount`, `daily_spend_cap` e `daily_min_spend_target` vão como inteiro em centavos (R$ × 100, sem casas decimais). Ex.: R$ 288/dia vai como `28800`.
- **Escrita no `MCP_CONECTOR`:** conferir no schema da tool de escrita (`ads_update_entity`, `ads_create_*`) a unidade que ela aceita antes da primeira escrita, sem assumir centavos.
- Os campos `_brl` do YAML ficam em reais e só são convertidos na hora da chamada. O bloco 🛡️ sempre mostra o valor em reais.
- **Depois de cada escrita de orçamento,** ler a entidade de novo e conferir que o valor em reais bate com o que o bloco 🛡️ mostrou. Se não bater, parar, avisar o aluno e propor reverter.

### Passo 0.1. Detectar origem da invocação

| Origem | Ação |
|---|---|
| Handoff de `/trafego-otimizar` (existe `sinal_para_escala.pronta=true` na sessão) | Pular Passos 0.5 a 0.8 (conta, escopo, inputs, confiabilidade e prontidão já validados pela otimização), **com duas conferências que valem também aqui**. (a) **Cooldown:** ler o histórico (Leitura 3 do Passo 0.75); se a última linha com status `freio_total` estiver dentro do cooldown da trilha (7d perpétuo low/mid, 14d perpétuo high, 24h lançamento), não escalar: avisar a data em que a campanha libera e devolver para `/trafego-otimizar` (princípio 10). (b) **Falso vencedor:** se o detector da `/trafego-diagnostico` rodou nesta sessão para a entidade e ela não saiu `vencedor_real` com score de confiança 50 ou mais, recusar com o motivo, mesmo com o `pronta=true` na sessão (regra do Passo 0.8); com `score_confianca` de 50 a 74 (do payload ou da sessão), só velocidade conservadora ou normal, nunca agressiva; se o falso vencedor não foi verificado (aluno recusou o detector ou o payload traz `falso_vencedor: nao_verificado`), mostrar "falso vencedor não verificado" no plano da §11. Depois, perguntar o teto da conta se ainda não foi dito na sessão (Pergunta 5 do Passo 0.7, opcional), rodar 0.85 (risco) e 0.86 (guardião, se houver teto) e ir para a seção 11 (Plano de execução). |
| Invocação direta (sem payload herdado) | Rodar Passos 0.5 → 0.6 → 0.7 → 0.75 → 0.78 → 0.8 → 0.85 → 0.86. |

---

### Passo 0.5. Selecionar conta de anúncios

Mesma lógica do Passo 0.5 de `/trafego-otimizar`. Lê `FB_AD_ACCOUNT_IDS` no `.env` e `FB_AD_ACCOUNT_ID` (conta padrão).

**Se houver apenas uma conta configurada**: usar automaticamente e pular a pergunta.

**Se houver mais de uma conta**: listar nomes com a conta padrão em primeiro lugar e etiqueta `"padrão"`. Demais seguem na ordem de `FB_AD_ACCOUNT_IDS`. Obter os nomes roteando por modo (ver Passo 0.0): MCP → `ads_get_ad_accounts` (já traz `ad_account_name`); APP → `GET /{act_ID}?fields=name&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)` (o token entra por substituição dentro do próprio `curl`, nunca escrito nem exibido).

```
Qual conta de anúncios deseja escalar?

[1] Nome da Conta Padrão "padrão"  (act_<id_padrao>)
[2] Nome da Conta B                (act_<id_b>)

Digite o número:
```

Salvar como `AD_ACCOUNT_ID_ATUAL`. **Filtro de status fica fixo em `effective_status=["ACTIVE"]`**: escala não atua sobre PAUSED nem WITH_ISSUES (campanhas pausadas não têm dado fresco; com problemas precisam passar antes pela otimização).

---

### Passo 0.6. Identificar escopo

Buscar todas as campanhas ativas da conta (leitura, rotear por modo, ver Passo 0.0). **Pedir só campos leves** (`id`, `name`, `objective`, `effective_status`, `daily_budget`), nunca métricas/insights nesta varredura inicial:

```
MCP: ads_get_ad_entities (level: "campaign", ad_account_id=AD_ACCOUNT_ID_ATUAL,
     filtering: [{field: "campaign.effective_status", operator: "IN", value: ["ACTIVE"]}],
     limit: 1000, fields enxutos), sem token
APP: GET /act_{AD_ACCOUNT_ID_ATUAL}/campaigns?fields=id,name,objective,status,daily_budget
     &effective_status=%5B%22ACTIVE%22%5D&limit=200&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)
```

No MCP, enquanto a resposta trouxer `cursor` de próxima página, repetir a chamada com ele. Se vierem 1000 linhas sem próxima página, avisar o aluno que a lista pode ter sido cortada pelo conector e, se a campanha procurada não aparecer, pedir o ID dela e ler só essa campanha pelo ID (`{field: "campaign.id", operator: "IN", value: ["<id>"]}`), já que filtrar por nome a lista cortada não traz de volta o que ficou fora (formatos conferidos: `trafego-insights/SKILL.md` §10.1 "Contrato do conector da Meta (MCP)").

> **Guard de conta grande** (espelhado de [.claude/skills/trafego-otimizar/SKILL.md](../trafego-otimizar/SKILL.md) Passo 0.6, aprendido em sessão real). A escalar fixa `effective_status=["ACTIVE"]`, então o risco de estourar o limite de tokens é menor que na otimizar (que aceita `PAUSED`). Mas em conta grande com 100+ campanhas ativas, vale a disciplina:
> - Varredura inicial **só** com os campos leves acima.
> - Se o aluno der uma **lista nomeada** específica, casar por `name`/`id` e seguir, sem varrer o resto da conta.
> - Se o retorno estourar e for salvo em arquivo automaticamente, ler por nome/id (com `jq` ou `grep`) em vez de despejar tudo no contexto.

Salvar lista em `CAMPANHAS_SESSAO`. Em seguida perguntar:

```
O que você quer escalar hoje?

[1]  Filtrar e escolher       (filtra por nomenclatura/palavra-chave;
                                depois você decide se escolhe manualmente
                                ou deixa eu auditar o filtro pra você)
[2]  Auditar toda a conta     (varro TODAS as ativas, rodo checklist de
                                prontidão em cada uma e devolvo ranking
                                de candidatas a escalar)
```

---

#### Se escolher [1], Filtrar e escolher

Primeiro, perguntar como filtrar:

```
Como suas campanhas estão nomeadas?

[1]  Por nomenclatura          você informa o padrão que usa
[2]  Filtro personalizado      palavra-chave, trecho do nome ou ID
[3]  Sem padrão definido       a IA identifica agrupamentos
```

Aplicar o filtro lendo a lista `CAMPANHAS_SESSAO` retornada (o Claude filtra por substring do nome na própria leitura, nunca com filtro de nome na API nem com script Python intermediário; o `filtering` da chamada fica só para o status). Apresentar a lista filtrada numerada e o total encontrado.

> **Desambiguação de nomes duplicados** (espelhado de [.claude/skills/trafego-otimizar/SKILL.md](../trafego-otimizar/SKILL.md) Passo 0.6, aprendido em sessão real). Contas reais têm **campanhas com nome idêntico e IDs diferentes** (versões de teste, duplicatas, sufixos truncados). Quando um nome do filtro casar com **mais de uma campanha**, **não escolher por conta própria**: apresentar as candidatas com **ID (últimos dígitos) + orçamento/dia + status** e pedir ao aluno qual(is) usar (ou "todas as versões"). Só prosseguir depois da confirmação. Mesma regra para nomes truncados (ex: "PT-Mu…" para "PT-Mundo").

**Em seguida, perguntar como prosseguir com o subconjunto filtrado** (esta é a etapa que evita o ponto cego de "tenho 38 campanhas, qual eu escalo?"):

```
Encontrei {N} campanhas com "{texto_do_filtro}". Como você quer prosseguir?

[1]  Vou escolher manualmente     (te mostro a lista numerada para
                                    você selecionar quem escalar)
[2]  Auditoria automática          (analiso as {N} filtradas, rodo o
                                    checklist de prontidão em cada uma
                                    e te devolvo APENAS as candidatas
                                    a escalar, com modo e velocidade
                                    já recomendados)
```

**Default sugerido quando `N > 10`:** opção [2] (auditoria), porque escolher entre 10+ campanhas no escuro é onde a fricção acontece. Para `N ≤ 10` o default é [1]. Sempre apresentar as duas: o aluno decide.

**Se escolher [1] do subconjunto, Manual:**

Apresentar o menu numerado das campanhas filtradas e perguntar:

```
Quais são os números das campanhas que você quer escalar?

Você pode usar qualquer combinação:
- Um número                  (ex: 3)
- Vários por vírgula         (ex: 1, 3, 5)
- Intervalo                  (ex: 1-5)
- Misto                      (ex: 1, 3-5, 8)
- A palavra `todas`          (seleciona todas as listadas)
```

**Regra de parsing:** aceitar `\d+(\s*[,-]\s*\d+)*` ou a palavra-chave `todas` (sem diferenciar maiúscula e minúscula). Expandir intervalos antes de validar (ex: `1-3` vira `[1, 2, 3]`). Deduplicar e ordenar. Validar que todos os índices existem na listagem; se houver inválido, recusar com mensagem clara.

**Confirmação obrigatória antes de prosseguir:**

```
Você selecionou {N} campanhas:
1. {nome_campanha_1}
2. {nome_campanha_2}
...

[1] Confirmar e analisar
[2] Refazer seleção
```

**Se escolher [2] do subconjunto, Auditoria automática:**

A skill puxa via `/trafego-insights` os dados das `N` campanhas filtradas, roda o checklist de prontidão (Passo 0.8) em cada uma e devolve o ranking. As reprovadas são descartadas (não bloqueiam a sessão) com motivo curto. As aprovadas viram a lista de candidatas, já com modo e velocidade recomendados (Passo 0.75). O aluno escolhe quais delas quer efetivamente escalar:

```
🟢 De {N} campanhas filtradas, {M} estão prontas para escalar:

CANDIDATA 1: CURSO X - Perpétuo Principal
   Trilha: Perpétuo low (R$ 297) · margem +18%
   📈 Vertical · Normal (+20% / 24h)

CANDIDATA 2: CURSO X - Remarketing 30d
   Trilha: Perpétuo low (R$ 297) · margem +41%
   📈 Horizontal com teste reels_only · Normal

...

🔴 {N - M} campanhas reprovadas no checklist:
   - {nome}: motivo ({condicao_falha})
   - {nome}: motivo ({condicao_falha})

Quais candidatas você quer escalar?
   1, 3, 5  |  1-5  |  todas  |  refazer filtro
```

---

#### Se escolher [2] do escopo inicial, Auditar toda a conta

A skill puxa as métricas de TODAS as campanhas ativas (não apenas filtradas), roda o checklist de prontidão em cada uma e devolve o ranking de candidatas mais maduras primeiro. Mesmo formato de apresentação do bloco de auditoria do subconjunto.

---

Definir `ESCOPO_FILTRO` na sessão:
- 1 selecionada manual: `ESCOPO_FILTRO = ids:{id1}`
- 2+ selecionadas manual: `ESCOPO_FILTRO = ids:{id1,id2,...}`
- Auditoria do subconjunto filtrado: `ESCOPO_FILTRO = subset_auditado:"{texto_do_filtro}"`
- Auditar toda a conta: `ESCOPO_FILTRO = conta_completa`

---

### Passo 0.7. Inputs obrigatórios de escala

Dois itens vêm de leitura; três são perguntados, **uma pergunta por vez**.

**Item 1. Tipo de funil (inferido):** pelo `objective` das campanhas (venda otimizando por Compra = perpétuo; Lead = lançamento/captação). Só perguntar se o escopo misturar objetivos:
```
Qual é o tipo de funil destas campanhas?

[1]  Perpétuo / venda direta   (otimização por Compra)
[2]  Lançamento / captação     (otimização por Lead)
```

**Item 2. Ticket do produto (lido do resumo):** o preço do `resumo-produto.md` vira `ticket_brl`. Só perguntar se o resumo não tiver preço ou se a campanha vender outro produto:
```
Qual é o valor do produto que essas campanhas vendem, em reais?
(ex: 97, 297, 997)
```

**Pergunta 3. Meta de CPA ou CPL:**
```
Qual é a sua meta de CPA (perpétuo) ou CPL (lançamento) em reais?
```

**Atenção:** ao contrário da otimização (que aceita default 50% do ticket), aqui **a meta é obrigatória**. A escala revalida gatilhos contra ela a cada incremento: sem meta, não há freio confiável.

**Pergunta 4. Margem de contribuição (para decidir por lucro, não só por CPA):**

Mesmo padrão do Passo 0.8 da `/trafego-diagnostico`. Nunca perguntar "qual sua margem?" (ninguém sabe de cabeça). Primeiro, uma pergunta de escolha:
```
Para calcular o lucro de verdade, preciso de 3 taxas da sua venda
(pode ser aproximado).

1. Quero informar as 3 taxas
2. Não sei agora (uso a faixa de margem de 60 a 80%)

Digite o número:
```
Se 1, perguntar **uma taxa por mensagem**, cada uma com o próprio exemplo, nesta ordem:
1. "Qual é a taxa da plataforma de venda? (ex: Hotmart ou Kiwify, de 1 a 10%)"
2. "Qual é o reembolso médio? (ex: 5%)"
3. "Qual é o imposto sobre o faturamento? (ex: de 6 a 17%)"

Se o aluno informar só parte das taxas, perguntar de novo só a que faltou; se ele não souber, usar o modo faixa e avisar.

Calcular `margem_contribuicao = 1 - (taxa_plataforma + reembolso + imposto_faturamento)` e salvar. Exemplo: 1 - (1% + 5% + 17%) = 0,77.

- **Custos fixos NÃO entram aqui** (só servem para "saúde da empresa", contexto opcional na otimizar §3.6).
- Se escolher 2 (ou não souber as taxas): usar **modo faixa** (60% a 80%) e declarar premissa carimbada em todo número de lucro mostrado.
- Margem alimenta: `roas_breakeven = 1 ÷ margem`, `cpa_breakeven = AOV × margem`, `lucro_dia = gasto_dia × (ROAS × margem - 1)`. **A escala usa esses três números pra decidir** (Passo 0.8 critério de lucro, freios §6, tetos §9, plano §11): não é só decoração.

**Pergunta 5. Teto de gasto diário da conta (opcional; obrigatório no modo Carteira):**
```
Tem um teto de gasto diário para a conta inteira (somando todas as
campanhas) que você não quer ultrapassar?
(ex: R$ 500/dia. Pular se não tem.)
```

Salvar `teto_conta_diario_brl` se informado. **O teto é sempre da conta inteira**, nunca de uma campanha só: é a mesma variável que o guardião de caixa (Passo 0.86), o modo Carteira (§3.6), o sinal `orcamento_acima_metade_potencial` (§0.75.2) e o teto Operacional (§9) leem.

**Caso modo "Auditar toda a conta":** as respostas valem como default da sessão. Quando uma campanha individual destoar (ex: ticket diferente), marcar `revisar_inputs: true` no bloco dela do output e oferecer sobrescrever.

**Após os inputs:** confirmar em uma linha:

```
Escalando: {N campanhas | "auditoria da conta"}
Conta: {nome}  |  Funil: {tipo}  |  Ticket: R$ {valor} (do resumo do produto)  |  Meta: R$ {cpa_cpl}  |  Teto da conta: R$ {teto ou "sem teto"}
Margem de contribuição: {margem}%  |  ROAS de break-even: {1÷margem}
```

---

### Passo 0.75. Análise + Recomendação técnica (modo e velocidade)

Antes de pedir aprovação de execução, a skill faz **três leituras** e devolve um bloco de recomendação composta (primário + alternativo) por campanha. O aluno valida ou ajusta.

#### 0.75.1 Leituras necessárias (na ordem)

> **Mapa de campos reais por caminho** (regra dura). As Leituras 1 e 2 abaixo passam por `/trafego-insights`; se forem feitas direto, valem os nomes do contrato do conector em [.claude/skills/trafego-insights/SKILL.md](../trafego-insights/SKILL.md) §10.1 "Contrato do conector da Meta (MCP)" (conferidos na conta real, mesma base da seção 4.3 do `/trafego-dashboard`):
>
> - **Tool `ads_get_ad_entities` (MCP), campos conferidos:** gasto `amount_spent` (nunca `spend`), cliques no link `link_click`, visitas à página `landing_page_view`, compras `omni_purchase`, checkout iniciado `omni_initiated_checkout`, valor das compras `offsite_conversion_fb_pixel_purchase_values` (sem ele, `purchase_roas × amount_spent`), `purchase_roas`, `impressions`, `reach`, `results` (objeto com `indicator` e `values`, resultado do objetivo da campanha) e `daily_budget` (objeto em reais). Connect rate, conversão da página e checkout para compra saem desses campos; "indisponível neste nível" só quando o campo vier `null`. Calculados: CTR de link total (`ctr_link_total`) = `link_click ÷ impressions`, frequência = `impressions ÷ reach`, CPM = `amount_spent ÷ impressions × 1000`.
> - **Campos não conferidos** (carrinho, CTR único, cliques totais, métricas de vídeo, demografia, `actions`/`action_values` crus, `attribution_setting`): conferir com `ads_get_field_context` antes e usar só o que ele devolver. Sem campo, dizer ao aluno que o conector não entrega esse número e seguir sem ele. No conector, `ctr_link_unico` fica `null` e o primário passa a ser o `ctr_link_total` (`link_click ÷ impressions`), declarando a troca, como na `/trafego-insights` §10.1.
> - **Curl Graph API (APP)** aceita os nomes clássicos. Usar `curl -g` quando o `fields` tiver nesting.
>
> Campo recusado: conferir com `ads_get_field_context` e remontar a chamada, nunca insistir no campo recusado.

**Leitura 1. Conta inteira no nível de anúncio** (1 chamada antes de qualquer leitura por campanha):
```
/trafego-insights  escopo=conta_completa  nivel=ad  janela=trilha_media
```
Pra detectar oportunidades estruturais **antes** de avaliar campanha por campanha:
- **Conjuntos vencedores na conta** = adsets com CPA ≤ target × 0,9 nas 3 janelas, agrupados por objetivo. Variável: `vencedores_conta.adsets[]`.
- **Anúncios vencedores espalhados** = anúncios vencedores (definição abaixo) em conjuntos/campanhas diferentes. Variável: `vencedores_conta.ads_espalhados[]`.

> **Definição única de anúncio vencedor** (vale aqui, na §3.5 e no command): anúncio com CTR único saudável (no conector, o `ctr_link_total`) **e** com o mínimo de conversões do tipo do produto (do resumo): **50 em low e middle ticket, 30 em high ticket**, contadas na janela média da trilha. Também conta como vencedor o anúncio que saiu `validado` num teste registrado pela `/trafego-testes` (em `meus-produtos/{ativo}/entregas/trafego/testes/INDEX.md`). É a mesma régua da `/trafego-testes`.

Esses dois números alimentam os sinais "3+ conjuntos vencedores na conta" e "5+ anúncios vencedores espalhados" da matriz.

**Leitura 2. Por campanha selecionada** (1 chamada por campanha):
```
/trafego-insights  campaign_id=<id>  nivel=auto  janela=trilha_completa
```
Devolve frequência atual, audiência ativa, CPM, CTR único, criativos saudáveis, gasto vs orçamento, idade da campanha **e o tipo de orçamento (`budget.tipo: ABO | CBO`)**, campo crítico pra decidir onde aplicar incrementos.

**Leitura 3. Histórico de escala** (arquivo local do produto):
```
ler  meus-produtos/{ativo}/trafego/escalar/historico-{campaign_id}.md
```
Conta quantos ciclos de escala consecutivos a campanha já recebeu (variável `ciclo_atual`) e se o último acionou freio. O `ciclo_atual` conta ciclos, não linhas: é o número de ciclos com pelo menos uma linha `incremento`; as linhas do mesmo lote (mesma data e hora) e as ativações das estruturas desse lote contam como um ciclo só (usar a coluna `ciclo`), e a linha `estrutura_pausada` sozinha não conta (§11.3). Se o arquivo não existe, `ciclo_atual = 0`. No MCP, `ads_account_get_activity_logs` pode confirmar as datas das últimas alterações de orçamento. O arquivo é atualizado a cada incremento executado (§11.3).

#### 0.75.1.1 Política de dado ausente (regra dura)

Em qualquer leitura, se um campo voltar `null`, vier vazio, ou a chamada falhar parcialmente:

- **Nunca inventar valor.** Não usar média do setor, benchmark genérico, estimativa de "tipicamente X". Marcar `null` ou `dados_disponiveis: false` no campo afetado.
- **Sinais que dependem do campo ausente NÃO são pontuados.** Não vira +0 nem chute pra um lado: vira "sinal indeterminado", excluído da soma.
- **Contar sinais indeterminados.** Quando ≥ 3 sinais derivados (de 9 da matriz) ficam indeterminados, forçar `confianca: baixa` na campanha afetada e oferecer "Aguardar próximo ciclo de dados" como alternativa.
- **Sinalizar ao aluno explicitamente.** Bloco `dados_ausentes` no output da campanha listando quais campos vieram vazios e por quê (ex: "campanha tem 2 dias, frequência ainda não estabilizou", "evento Purchase sem disparo na janela", "audiência ativa não retornada pela API").
- **Estimativas estão proibidas em qualquer parte da resposta**, incluindo perguntas conversacionais. Se o aluno perguntar "qual seria o CPM esperado pra essa campanha?" e a conta não tem histórico de 14 dias, responder "não tenho dado real pra essa conta na janela necessária", sem recorrer a média de mercado.

#### 0.75.2 Sinais derivados (calculados a partir das leituras)

Pra cada campanha selecionada, derivar a presença/ausência dos sinais abaixo:

| Sinal | Cálculo |
|---|---|
| `freq_baixa_audiencia_grande` | frequência < 1,8 **E** audiência > 2M **E** CPM estável ou caindo nos últimos 3 dias |
| `freq_alta_ou_aud_pequena` | frequência > 2,2 **OU** audiência < 1M |
| `estavel_ciclo_2_mais` | sem freios há 7+ dias **E** ciclo_atual ≥ 2 |
| `tres_mais_adsets_vencedores` | `vencedores_conta.adsets.length` ≥ 3 dentro do mesmo objetivo |
| `cinco_mais_ads_espalhados` | `vencedores_conta.ads_espalhados.length` ≥ 5 em conjuntos diferentes |
| `cpm_e_freq_subindo` | CPM subiu ≥ 15% e frequência subiu ≥ 0,3 nos últimos 3 dias |
| `ciclo_zero` | ciclo_atual == 0 (primeira escala) |
| `ciclo_tres_mais_verticais` | ciclo_atual ≥ 3 e modos anteriores foram todos Vertical |
| `orcamento_acima_metade_potencial` | orçamento atual da campanha ≥ 50% do `teto_conta_diario_brl` declarado (a campanha já ocupa metade ou mais do teto da conta) |

#### 0.75.3 Matriz de scoring

Cada modo recebe pontos baseado nos sinais ativos:

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

**Critério adicional pra Vertical (porta de entrada apertada):** se `freq_baixa_audiencia_grande` está **falso** OU `orcamento_acima_metade_potencial` está **verdadeiro** OU `cpm_e_freq_subindo` está **verdadeiro**, Vertical recebe penalidade extra de -2 (independente do score acumulado). Isso impede que Vertical vença em campanha que já está saturando.

O modo **Carteira** (§3.6) não entra na matriz: é escolha explícita do aluno (escala da conta inteira sob teto), não recomendação por campanha.

#### 0.75.4 Algoritmo de decisão

1. Somar pontos de cada modo conforme sinais ativos.
2. **Modo de maior score = Primário.**
3. **Modo de segundo maior score** (se score ≥ 60% do score do primário) **= Alternativo**.
4. Se score do primário < 4 pontos absolutos: marcar `confianca: baixa` e oferecer **"Aguardar próximo ciclo de dados"** como alternativa em vez de outro modo.
5. Velocidade segue a regra da seção 4: conservadora se high ticket / audiência pequena / menos de 3 backups; agressiva se lançamento ou sazonal + ≥ 3 backups (nunca com score de confiança do falso vencedor de 50 a 74, Passo 0.8); normal nos demais.

#### 0.75.5 Formato de apresentação

```
🔎 Análise das {N} campanhas selecionadas

🌐 Sinais da conta inteira:
   Conjuntos vencedores no mesmo objetivo: {N}
   Anúncios vencedores espalhados em conjuntos diferentes: {N}

CAMPANHA 1: {nome}
   Trilha: {trilha_legível}  ·  Ciclo de escala: {ciclo_atual}
   Estrutura: {ABO | CBO}  ·  Orçamento atual: R$ {valor} ({nivel: adset | campaign})
   CPA atual: R$ {cpa}  ·  meta: R$ {target}  ·  margem +{margem_pct}%
   Frequência: {freq}  ·  Audiência ativa: {audiencia}  ·  CPM: R$ {cpm} ({delta_cpm_pct})
   {APP: "CTR único: {ctr_link_unico}" | no conector: "CTR de link total: {ctr_link_total}"}  ·  Criativos saudáveis: {n_backup}

   📈 Recomendação:
      Primário:    {modo_primario} · {velocidade}
                   {justificativa em 1 frase referenciando os sinais}
      Alternativo: {modo_alternativo}
                   {gatilho de migração: "considerar quando X passar de Y"}

CAMPANHA 2: {nome}
   ...

Como prosseguir?

[1] Aceitar todos os primários
[2] Aceitar algumas, ajustar outras (informe quais)
[3] Refazer com modo/velocidade manual em todas
```

**Confiança baixa:** quando o primário tem score < 4, o bloco aparece como:

```
   📈 Recomendação:
      Primário:    {modo_primario} · {velocidade}    [confiança baixa]
                   Sinais ambíguos, score {N}/12 acumulado.
      Alternativo: Aguardar próximo ciclo de dados (24 a 48h)
                   Reanalisar com mais histórico antes de comprometer orçamento.
```

**Opções [2] e [3]:** quando o aluno quer ajustar, oferecer menu manual:

```
Modos disponíveis:
[1] Vertical
[2] Horizontal (com sub-opção de teste: pt_mundo, reels_only, instagram_only, facebook_only, advantage_placement, nova_segmentacao)
[3] Vertical + Horizontal alternado
[4] Consolidação CBO
[5] Campanha Advantage
[6] Carteira (conta inteira sob teto de gasto, ver §3.6)

Velocidades:
[1] Conservadora (+15% / 72h)
[2] Normal (+20% / 24h)
[3] Agressiva (+30 a +50% / 24h, exige ≥3 criativos backup)
```

> **Vínculo com a tabela "Ferramentas de escala disponíveis" (seção 12, Parte 1):** o `Primário` e o `Alternativo` apresentados aqui são a versão resumida da decisão. No output final, eles viram as marcações `✓` e `reserva` da tabela de arsenal completo: toda ferramenta aparece lá, recomendada ou em reserva com gatilho, pra o aluno ver o leque inteiro antes do plano. A decisão é a mesma; a tabela só a mostra no contexto de tudo que a skill poderia fazer.

---

### Passo 0.78. Confiabilidade do dado (gate de fonte antes de executar)

> Espelhado de [.claude/skills/trafego-otimizar/SKILL.md](../trafego-otimizar/SKILL.md) Passo 0.8. **Mais duro aqui:** a otimizar pode rebaixar o CPA a secundário e seguir; a escalar não, porque comprometer orçamento em cima de dado podre é grave demais. **Confiabilidade `baixa` bloqueia a escala.**

A skill roda 4 checagens e imprime um bloco curto de confiabilidade antes do Checklist de prontidão (Passo 0.8). Tudo aqui é leitura e não passa pelo gate.

**1. Janela e atribuição.** Carimbar a janela usada nas leituras do Passo 0.75.1 e a atribuição em todo número exibido (ex: "últimos 7 dias · 7d clique / 1d visualização"). Se a conta não expõe `attribution_setting` ou ela derruba a chamada multi-campo, **assumir o padrão omni da API e declarar** (`atribuicao: "padrao_omni_da_api"`). Nunca incluir `attribution_setting` numa chamada multi-campo de insights (espelhado de otimizar Passo 0.8 item 1).

**2. Saúde do pixel.** Acionar `/trafego-pixel` (ou ler o dataset): último disparo, volume do evento-norte (Compra ou Lead) nos últimos 7 dias.
> **Plano B** (espelhado de otimizar Passo 0.8 item 2): se `ads_get_datasets` retorna "gradually being rolled out", inferir pelo fluxo de compras atribuídas (`omni_purchase` no MCP, ou a compra em `actions` no APP, aparecendo nos insights = evento Compra disparando) e declarar (`pixel_evento_norte: "inferido_pelo_fluxo_de_vendas"`). Volume absoluto baixo em high ticket é esperado e **não** é, sozinho, sinal de subnotificação.

**3. Consistência interna do recorte.** Conferir que **todas** as campanhas selecionadas estão na mesma janela e mesma atribuição, e que não há dupla contagem entre elas.

> **Conciliação com o total da conta** (espelhada de otimizar Passo 0.8 item 3, princípio 18 da otimizar): só vale em modo "Auditar toda a conta" (`escopo: conta_completa`). Em recorte filtrado/manual, marcar `conciliacao_conta: nao_aplicavel` e seguir: soma do recorte nunca fecha com o total da conta, e isso não é erro.

**4. Descoberta de campos.** Antes da Leitura 2 do Passo 0.75.1, confirmar quais campos a conta expõe (no MCP, campo fora da lista conferida passa antes por `ads_get_field_context`). Não pedir campo às cegas. Se a tool recusar, remontar a chamada sem o campo recusado (ver §0.75.1, mapa de campos reais).

**Saída deste passo:** bloco `confiabilidade_do_dado` no payload da campanha (ver §12 YAML), com `nivel: alta | media | baixa`, motivos, e os carimbos.

**Regra dura:**

| Nível | Comportamento da escalar |
|---|---|
| `alta` | Prossegue para o Checklist de prontidão (Passo 0.8). |
| `media` | Prossegue, **com aviso explícito no plano** (Parte 1 do output) e premissa de margem rebaixada. |
| `baixa` | **Bloqueia escala.** Devolve com motivo (`pixel sem disparo`, `conciliação não bate em modo conta_completa`, `≥3 sinais indeterminados` etc.) e sugere `/trafego-otimizar` ou aguardar 24 a 48h pra repuxar dados. |

---

### Passo 0.8. Checklist de prontidão (gate antes de executar)

Para cada campanha selecionada, rodar o checklist da seção 5 (Critérios de gatilho) E da seção 12 da skill `trafego-otimizar` (Sinal de prontidão para escala). Todas as condições precisam ser verdadeiras simultaneamente:

- CPA/CPL na janela média ≤ target × 0,9 (margem 10%)
- CPA/CPL na janela longa ≤ target
- Frequência ≤ 2,5 (perpétuo) ou ≤ 3,0 (lançamento)
- Pelo menos 1 anúncio com CTR único saudável
- Conjunto fora de fase de aprendizado
- Última edição ≥ 48h
- ≥ 2 criativos saudáveis (≥ 3 se velocidade recomendada/escolhida for agressiva)
- Cooldown respeitado se houver handoff de descida anterior (≥ 7d perpétuo low/mid, ≥ 14d perpétuo high, ≥ 24h lançamento), contado a partir da última linha com status `freio_total` em `meus-produtos/{ativo}/trafego/escalar/historico-{campaign_id}.md` (Leitura 3 do Passo 0.75; sem arquivo, não houve descida)
- **Falso vencedor e score de confiança** (freio da `/trafego-diagnostico`): se o detector de falso vencedor rodou nesta sessão para a entidade, só seguir quando ela saiu `vencedor_real` com score de confiança 50 ou mais; com score de 50 a 74, só de forma gradual (nunca velocidade agressiva). Se saiu outra classificação ou score abaixo de 50, não escalar e devolver com o motivo, **inclusive no handoff do Passo 0.1**. Se não rodou, oferecer o detector (`/trafego-diagnostico` opção [4], só leitura) antes do plano; se o aluno recusar, mostrar "falso vencedor não verificado" no plano da §11, ao lado do score de risco.
- **ROAS sustentado ≥ ROAS de break-even** (`1 ÷ margem_contribuicao` da Pergunta 4 do Passo 0.7) nas janelas média e longa, ou seja, **lucro/dia ≥ 0**. Espelhada da camada de lucro da otimizar (§3.6), garante que a escala só cresça campanha **lucrativa de verdade**: não basta o CPA estar abaixo do target se a margem do produto não suporta. Em modo faixa (margem 60 a 80%), exigir lucro/dia ≥ 0 no extremo conservador da faixa (margem 60%).

**Se qualquer condição falhar:** a skill **não escala** essa campanha. Devolve com motivo específico e handoff sugerido para `/trafego-otimizar`. Em modo "Auditar toda a conta", a campanha que reprovar é apenas excluída da lista de candidatas (não erra a sessão inteira).

> **Zona amarela explícita.** Campanha em zona amarela (CPA acima do target × 0,9 mas ROAS ≥ break-even) **não passa** neste checklist e é devolvida pra `/trafego-otimizar` otimizar criativo. Escalar zona amarela sobe verba em campanha que ainda não consolidou margem. A otimizar diz, na §3.6, que "zona amarela se otimiza, não se contém"; aqui a tradução é "zona amarela se otimiza, não se escala".

### Passo 0.85. Score de risco por incremento

Para cada campanha/adset que passou no checklist de prontidão (0.8), ou que chegou por handoff da otimização, calcular o score de risco de incremento antes de montar o plano. Ver sub-skill `sub-skills/risco-incremento.md` para variáveis, faixas e regras.

**Resumo rápido:**
- Score 0 a 100 (0 = seguro, 100 = risco extremo)
- 8 variáveis: volume, consistência, margem de segurança, frequência, dependência criativa, dependência de remarketing, histórico pós-incremento, saturação
- `risco_extremo` (76 a 100): **bloqueia incremento**, campanha removida do plano
- `risco_alto` (51 a 75): confirmação reforçada com aviso explícito ao aluno
- `risco_medio` e `risco_baixo`: segue fluxo normal

O score aparece junto de cada ação no plano de confirmação (§11).

### Passo 0.86. Validação do guardião de caixa (se modo carteira ou teto declarado)

Se o modo é **carteira** (§3.6) ou se o aluno declarou `teto_conta_diario_brl`, rodar `sub-skills/guardiao-caixa.md` antes do plano:
- Mapear gasto total da conta
- Verificar que incrementos propostos cabem no teto
- Identificar vazamentos para recomendar cortes na Fase 1

Se `caixa_critico`: **não escalar**. Recomendar cortar vazamentos primeiro via `/trafego-otimizar`.

**Exceção do modo Carteira.** A Carteira existe para cortar vazamentos e escalar no mesmo plano, então o caixa crítico de antes dos cortes não encerra a sessão. Nela, a urgência é recalculada sobre o **gasto projetado depois dos cortes da Fase 1** (gasto atual menos os cortes), e os vazamentos que já estão na Fase 1 não contam para os "2 ou mais vazamentos". Se o caixa continuar crítico depois dos cortes, entregar só a Fase 1 (cortes pela `/trafego-otimizar`, dentro do mesmo plano numerado) e não montar a Fase 2. Em nenhum caso o aluno sai sem o plano.

---

## 1. Pré-condições para a skill rodar

A skill **só atua** sobre campanhas que receberam sinal explícito de prontidão. Três modos de entrada:

### 1.1 Sinal vindo de `/trafego-otimizar` (caminho preferido)
A otimização emitiu `sinal_para_escala.pronta: true` no último diagnóstico. A skill lê o bloco e prossegue. **Nesse caso, conta, campanhas, meta de CPA/CPL e margem já estão no payload herdado: não há nova coleta de contexto** (só o teto opcional, se ainda não foi dito). As conferências de cooldown e de falso vencedor do Passo 0.1 valem mesmo assim.

### 1.2 Acionamento manual com auditoria automática
O aluno pede escala diretamente (pelo command `/trafego-escalar`) sem ter rodado `/trafego-otimizar` antes. Nesse caso, a skill executa o fluxo guiado da **seção 0 (Perguntas iniciais)** para coletar conta, escopo, tipo de funil, meta, margem e teto (ticket vem do resumo do produto), depois roda análise + recomendação técnica (Passo 0.75) e só prossegue se a confiabilidade (Passo 0.78) e o checklist de prontidão (Passo 0.8) aprovarem. Se reprovar, recusa e devolve diagnóstico do que falta com handoff sugerido para `/trafego-otimizar`.

### 1.3 Modo "agressivo declarado"
Em **lançamento** (fase de captação inicial ou final) ou em **janela sazonal declarada** (Black Friday, data comemorativa, lançamento de concorrente), o aluno pode forçar escala com critérios relaxados. A skill exige confirmação explícita do contexto antes de aceitar. Com score de confiança do falso vencedor de 50 a 74 (Passo 0.8), a velocidade agressiva fica de fora mesmo no contexto declarado: só conservadora ou normal.

---

## 2. Inputs

### 2.1 Obrigatórios
| Input | Por quê |
|---|---|
| `campaign_id` ou `adset_id` | Objeto a escalar |
| `tipo_funil` | `perpetuo_venda_direta` ou `lancamento_captacao` |
| `ticket_brl` | Define teto de CPA tolerado durante escala (lido do resumo do produto) |
| `cpa_target` ou `cpl_target` | Métrica-norte que guia o freio |
| `sinal_de_prontidao` | Bloco vindo da otimização ou de auditoria interna |
| `criativos_de_backup` | Quantidade de anúncios saudáveis disponíveis como fallback |

### 2.2 Opcionais com default
- `velocidade`: `conservadora` (+15%) | `normal` (+20%, default) | `agressiva` (+30 a +50%, restrita a lançamento ou sazonal; com score de confiança do falso vencedor de 50 a 74, Passo 0.8, fica de fora e só valem conservadora ou normal)
- `modo`: `auto` (default, skill decide) | `vertical` | `horizontal` | `vertical_e_horizontal` | `cbo_consolidacao` | `advantage_plus_consolidacao` | `carteira`
- `janela_de_observacao_pos_incremento_horas`: 48h (perpétuo, default) | 24h (lançamento) | 72h (perpétuo high)
- `teto_conta_diario_brl`: teto de gasto diário da conta inteira, declarado pelo aluno (obrigatório no modo Carteira)
- `fase_lancamento`: se aplicável

---

## 3. Modos de escala

### 3.1 Vertical (subir orçamento no conjunto vencedor)
- **Quando:** frequência ≤ 2,0, audiência > 2M, criativo vencedor com CTR alto.
- **Funciona em ABO e CBO.** Em ABO, sobe o orçamento do conjunto. Em CBO, sobe o orçamento da campanha.
- **Ritmo padrão:** +20% a cada 24h enquanto os gatilhos da seção 5 permanecerem verdadeiros.
- **Risco:** saturação acelerada, frequência sobe rápido.
- **Vantagem:** preserva 100% do aprendizado do conjunto original.

### 3.2 Horizontal (duplicar vencedor com isolamento)
- **Quando:** frequência > 2,0, audiência < 1M, ou vertical já maturado.
- **O que duplicar:** pode ser a campanha inteira, apenas o conjunto ou apenas o anúncio vencedor, dependendo do que se quer isolar.
- **Duplicação simples:** cópia exata do vencedor, sem alteração. Isola o desempenho em uma nova instância sem interferir no original.
- **Duplicação com teste sugerido:** mantém toda a estrutura original e muda **somente** o elemento do teste. Opções disponíveis:
  - `pt_mundo`: idioma português brasileiro, segmentação geográfica mundial
  - `reels_only`: posicionamento restrito a Reels
  - `instagram_only`: posicionamento restrito a Instagram (feed + stories + reels)
  - `facebook_only`: posicionamento restrito a Facebook
  - `advantage_placement`: posicionamentos automáticos (Advantage+)
  - `nova_segmentacao`: troca de público (lookalike de outra %, audiência fria adjacente, interesse diferente)
  - Outros testes podem ser sugeridos pelo aluno antes da execução

  **Regra de integridade:** antes de qualquer duplicação, validar que os anúncios da campanha original se referem ao mesmo produto, mesmo público-alvo e mesmo funil que os inputs declarados na abertura da sessão (e o produto ativo do resumo). Se houver divergência, alertar o aluno antes de executar.

  **Como duplicar, por modo:**
  - **MCP:** `ads_create_ad_set` / `ads_create_campaign` / `ads_create_ad` com `source_adset_id` / `source_campaign_id` / `source_ad_id` (copia a estrutura validada), na ordem abaixo (mesma lógica da `trafego-testes/sub-skills/duplicar-variando.md`):
    1. Criar o conjunto com `ads_create_ad_set` + `source_adset_id`. Na consolidação CBO, indicar a campanha nova como destino, se o schema da tool permitir.
    2. Conferir pela leitura (`ads_get_ad_entities` com `level: "ad"`, filtrado pelo `adset_id` do conjunto novo) se os anúncios vieram junto. Se não vieram, copiar cada anúncio ativo do molde com `ads_create_ad` + `source_ad_id` para o conjunto novo.
    3. Aplicar a dimensão do teste (`pt_mundo`, `reels_only` etc.) com `ads_update_entity`, só se o schema aceitar mudar o campo sozinho (o conector não lê a segmentação, então não dá para reenviar a segmentação inteira com segurança). Se exigir a segmentação completa, fazer a duplicação guiada no Gerenciador, como na `/trafego-testes`.
    4. A estrutura só fica pronta para o aluno pedir a ativação (§11.2) depois de conferir que o conjunto novo tem pelo menos 1 anúncio e a variação aplicada.

    Se a Meta recusar a cópia (erros de cópia grande demais, criativo com post existente ou sinalização de público Advantage faltando), não insistir: oferecer a duplicação guiada no Gerenciador (marcar o conjunto, Duplicar, mudar só o elemento do teste, publicar pausado) e seguir o plano depois que o aluno confirmar. A cópia guiada também fica pausada; a ativação segue a §11.2 (o aluno pede, e a skill ativa com bloco 🛡️ próprio ou ele liga no Gerenciador).
  - **APP: não confiar no `POST /<id>/copies` para estrutura com 2 ou mais objetos** (lição de campo registrada na `/trafego-testes`, em `.claude/skills/trafego-testes/sub-skills/ab-generico.md`, "Lições de campo"). A cópia síncrona com `deep_copy=true` aceita menos de 3 objetos no total (erro 1885194), quebra ao recriar criativo (3858504 / 2446347) e exige `targeting_automation.advantage_audience` no conjunto (1870227). O `/copies` só serve para entidade pequena (1 conjunto com 1 anúncio). Para o resto, usar **ler → recriar**:
    1. Ler a config do molde por GET (`curl -g` quando o `fields` tiver `{}`): campanha (`objective`, `buying_type`, `daily_budget`, `bid_strategy`, `special_ad_categories`, `is_adset_budget_sharing_enabled`), conjunto (`optimization_goal`, `billing_event`, `bid_strategy`, `bid_amount`, `daily_budget`, `promoted_object`, `attribution_spec`, `destination_type`, `targeting`) e anúncios (`creative{id}`).
    2. Criar o conjunto novo com o `targeting` lido, trocando **só** a dimensão do teste, mais `targeting_automation: {advantage_audience: 0 ou 1}`. Sob CBO, sem `daily_budget` nem `bid_strategy` no conjunto; se a campanha usar teto de custo ou de lance (`COST_CAP` ou `LOWEST_COST_WITH_BID_CAP`), repetir no conjunto novo o `bid_amount` lido do molde, em centavos (o campo vai no conjunto, não existe na campanha). Sob ABO, mandar no conjunto novo o `daily_budget` do plano, em centavos (R$ × 100), e a `bid_strategy` do molde; com `COST_CAP` ou `LOWEST_COST_WITH_BID_CAP`, também o `bid_amount` lido, em centavos. Replicar o `promoted_object` idêntico (inclusive conversão personalizada).
    3. Criar cada anúncio **referenciando o `creative_id` existente**, nunca copiando o criativo.
    4. Fatiar idade e público a partir do `targeting` lido, nunca a partir do nome do conjunto.

    **Campanha recriada** (duplicar campanha, campanha Advantage): se ela ficar em ABO (sem orçamento na campanha), mandar `is_adset_budget_sharing_enabled` com o valor lido do molde, ou `false` se vier vazio (obrigatório desde a v24 da Marketing API; sem ele, erro 4834011 "Must specify True or False in is_adset_budget_sharing_enabled field"). Em CBO, não mandar o campo. No MCP, preencher só se o schema da `ads_create_campaign` pedir.

  **Lacunas do teste `nova_segmentacao` (só no MCP):**
  - **Lookalike novo:** não é lacuna. Criar pelo MCP com `ads_create_custom_audience` (subtipo LOOKALIKE) ou delegar a `/trafego-publicos`. Se a Meta recusar o subtipo na prática, a `/trafego-publicos` conduz o passo a passo guiado no Gerenciador e a duplicação segue com o ID do público criado.
  - **Interesse por nome:** o MCP não busca interesse. Recomendar primeiro público aberto com Advantage+ (padrão atual da Meta). Se o aluno quiser um interesse específico, guiar a pesquisa no Gerenciador (no conjunto, segmentação detalhada, digitar o tema e anotar o nome exato do interesse) e pedir o nome ou ID para usar na duplicação. No APP, a busca vai por `GET /search?type=adinterest`.
  - **Lookalike já existente ou público amplo:** sem lacuna (o público existente é referenciado por ID na duplicação).

- **Risco:** canibalização entre conjuntos, aprendizado novo a partir do zero em cada duplicação.
- **Vantagem:** abre nova fonte de tráfego sem cansar a atual.

### 3.3 Vertical + Horizontal alternado
- **Quando:** campanha madura, performance estável há 7+ dias (perpétuo).
- **Como:** alternar entre subir budget do vencedor (vertical) e duplicar com nova segmentação ou teste (horizontal) a cada ciclo de observação.
- **Vantagem:** reduz o risco de saturação do vertical puro e o custo de reaprendizado do horizontal puro.

### 3.4 Consolidação em CBO
- **Quando:** 3+ conjuntos vencedores em ABO, querendo simplificar gestão e deixar o algoritmo distribuir o orçamento.
- **Como:** criar campanha CBO duplicando os conjuntos vencedores e migrando o orçamento gradualmente. No MCP, cópia por `source_adset_id` com a conferência de anúncios da §3.2. No APP, pelo padrão ler → recriar da §3.2 (campanha casca CBO, conjuntos sem orçamento próprio, anúncios referenciando `creative_id`).
- **Risco:** reset de aprendizado nos novos conjuntos. **Custo estimado declarado antes da execução.**

### 3.5 Campanha Advantage (escala por consolidação de criativos vencedores)
- **Quando:** o aluno tem **5 ou mais anúncios vencedores** (pela definição única da Leitura 1 do Passo 0.75.1: 50 conversões em low e middle ticket ou 30 em high ticket na janela média da trilha, ou `validado` num teste da `/trafego-testes`) e quer consolidar a verba em uma estrutura enxuta e otimizada pelo algoritmo.
- **Estrutura:** 1 campanha, 1 conjunto com público Advantage+, de 5 a 50 anúncios vencedores dentro do conjunto.
- **Como:** identificar os melhores anúncios da conta (ou da seleção indicada pelo aluno), validar que todos pertencem ao mesmo produto/funil/público-alvo declarado na sessão e montar a campanha Advantage com eles (anúncios referenciando o `creative_id` de cada vencedor).
- **Regra de quantidade:** usar o máximo de anúncios vencedores disponíveis, respeitando o limite de 50. **Abaixo de 5, não faz sentido**: Advantage+ precisa de variedade criativa pro algoritmo ter espaço de iteração; com poucos anúncios o aprendizado fica raso e não justifica a consolidação. Sugerir primeiro produzir mais criativos (`/copy-anuncio` + `/criativo-estatico`) e validá-los por A/B no `/trafego-testes`.
- **Risco:** se os anúncios forem de produtos ou funis diferentes, o algoritmo vai otimizar de forma incoerente. A validação de produto/funil é obrigatória antes de montar.
- **Vantagem:** estrutura simples, algoritmo com ampla liberdade criativa, menor custo operacional de gestão.

### 3.6 Modo Carteira (escala da conta inteira sob teto de gasto)

- **Quando:** o aluno quer otimizar a distribuição de verba da conta inteira (cortar queimadores E escalar vencedores) num único planejamento, sob um teto de gasto diário.
- **Pré-requisito:** `teto_conta_diario_brl` declarado pelo aluno. Sem teto declarado, a Carteira não roda: a skill pede o teto (Pergunta 5 do Passo 0.7). Teto inferido do gasto médio não serve aqui, porque deixaria a utilização perto de 100% por construção.
- **Fluxo:**
  1. Rodar `guardiao-caixa.md` para mapear gasto atual, vazamentos e folga. A urgência que decide a Fase 2 é a recalculada depois dos cortes da Fase 1 (exceção do modo Carteira no Passo 0.86): se o caixa continuar crítico mesmo com os cortes, o plano sai só com a Fase 1.
  2. Ranquear campanhas por eficiência: `share_de_conversoes / share_de_gasto` (quanto contribui vs quanto consome).
  3. Identificar queimadores (eficiência < 0,5) e vencedores (prontidão aprovada + risco baixo/médio).
  4. Gerar plano em duas fases:
     - **Fase 1 (handoff para `/trafego-otimizar`):** listar cortes e realocações recomendados. A escalar NÃO executa cortes: faz handoff com o plano pré-montado.
     - **Fase 2 (escalar executa):** após cortes aplicados pela otimizar, escalar executa incrementos nos vencedores até o teto.
  5. **Aprovação no modo "lote pré-aprovado" do CLAUDE.md.** Mostrar o plano completo numerado, com as duas fases visíveis (cada corte, realocação e incremento com objeto, valor antes e depois, reset e risco), **uma vez**, e pedir um **"aprovar tudo"** explícito:
     ```
     Aprovar tudo? Responda "aprovar tudo" para executar as {N} ações das duas fases em sequência,
     ou "não" para cancelar. Se preferir aprovar fase por fase, responda "fase por fase".
     ```
     - Com o "aprovar tudo": a Fase 1 roda na `/trafego-otimizar` e a Fase 2 na escalar, em sequência, sem reabrir o gate. Se uma ação falhar, parar, mostrar o que já foi feito e perguntar antes de continuar.
     - Sem ele (resposta parcial, "sim" ambíguo, "fase por fase"): cada fase passa pelo gate 🛡️ normal da skill dona.
     - Cortes da carteira são reduzir ou pausar, nunca apagar. DELETE nunca entra no plano.
- **Regra dura:** gasto total após o plano NÃO pode ultrapassar o teto. Se a folga é R$ 50/dia e o aluno quer escalar R$ 100/dia, escala R$ 50.
- **Métricas de priorização:**
  - `share_de_gasto` = spend_campanha / spend_total
  - `share_de_conversoes` = purchases_campanha / purchases_total
  - `margem_de_seguranca_cpa` = (cpa_alvo - cpa_atual) / cpa_alvo
  - `margem_de_seguranca_roas` = (roas_atual - roas_minimo) / roas_minimo
- **Princípio preservado:** a simetria otimizar/escalar (princípio 14 da §13) se mantém. A escalar planeja a sessão inteira, mas delega a execução de cada fase para a skill dona.

---

## 4. Velocidade de escala

| Velocidade | Incremento | Janela entre ajustes | Quando usar |
|---|---|---|---|
| Conservadora | +15% | 72h | High ticket, audiência pequena, criativo único |
| Normal | +20% | 24h | Default para vertical. Perpétuo low/mid com performance estável |
| Agressiva | +30 a +50% | 24h | Lançamento captação inicial/final, sazonal declarado, ≥3 criativos backup. Nunca com score de confiança do falso vencedor de 50 a 74 (Passo 0.8): aí só conservadora ou normal |

**Regra dura:** mesmo em modo agressivo, **um único incremento isolado nunca passa de +50%** sobre o orçamento atual do conjunto. Acima disso reseta aprendizado de forma quase certa.

> A janela de 24h se aplica ao modo vertical. Para horizontal, CBO e Advantage, aguardar o período mínimo de maturação da nova estrutura antes de avaliar resultado (mínimo 48h perpétuo, 24h lançamento), contado a partir da ativação (§11.3), nunca da criação: estrutura pausada não gasta nem gera dado. Perpétuo mid ticket usa 72h entre ajustes (§7.2), mesmo na velocidade normal.

---

## 5. Critérios de gatilho. Revalidação a cada ciclo

Antes de **cada incremento**, **todas** as condições abaixo devem permanecer verdadeiras:

- CPA/CPL na janela média ≤ target × 0,9 (margem de segurança de 10%)
- CPA/CPL na janela longa ≤ target
- Frequência atual ≤ 2,5 (perpétuo) ou ≤ 3,0 (lançamento)
- Pelo menos 1 anúncio com CTR ≥ saudável da trilha
- Conjunto fora de fase de aprendizado
- Última edição ≥ janela mínima da velocidade escolhida
- Lucro/dia ≥ 0 (ROAS ≥ break-even), quando a margem foi coletada

Se **qualquer uma** falhar, a skill **não escala**. Emite output de `aguardar` ou aciona freio (seção 6) e devolve diagnóstico para a otimização quando aplicável.

---

## 6. Freios. Quando a escala para ou volta atrás

### 6.1 Freio leve. Pausar próximo incremento
Qualquer das condições, após o último incremento:
- CPA/CPL piorou 10 a 20% na janela curta vs janela média
- Frequência subiu ≥ 0,5 no ciclo
- CPM subiu ≥ 20%
- **Lucro/dia caiu ≥ 30%** vs ciclo anterior (zona ainda verde, mas margem encolhendo)

**Ação:** não fazer próximo incremento. Manter orçamento atual. Reavaliar em 48h.

### 6.2 Freio médio. Reverter último incremento
Qualquer:
- CPA/CPL piorou 20 a 30% sustentado por 48h
- Frequência ≥ 4 sem refresh criativo na fila
- CTR caiu ≥ 30% nos anúncios principais
- **ROAS caiu pra dentro de ±10% do break-even** (margem zerando, beira da zona vermelha)

**Ação:** voltar o orçamento ao valor de antes do último incremento, ou seja, o "orçamento antes" da última linha com status `incremento` em `historico-{campaign_id}.md` (não a última linha qualquer, porque o histórico também recebe linhas de freio), com gate 🛡️ mostrando "R$ atual → R$ anterior". Sem histórico, buscar o orçamento anterior em `ads_account_get_activity_logs` (MCP) ou perguntar ao aluno; sem nenhum dos dois, não calcular o valor por conta própria (princípio 12): mostrar o orçamento atual no bloco 🛡️ e pedir ao aluno o valor de volta. Se o último ciclo foi a ativação de estrutura nova (Horizontal, CBO ou Advantage), reverter é pausar essa estrutura, com o mesmo gate. Num lote misto (§11.3), cada parte ativa do último ciclo que acionou o freio volta do seu jeito, no mesmo bloco 🛡️: o incremento vertical ao "orçamento antes" da linha dele, e a estrutura nova é pausada. Sugerir refresh criativo: copy nova em `/copy-anuncio` (ângulo novo da Mandala em `/mandala-de-anuncios`), imagem em `/criativo-estatico` e A/B contra o atual no `/trafego-testes`. Devolver diagnóstico para `/trafego-otimizar`.

### 6.3 Freio total. Devolver para otimização
Qualquer:
- CPA/CPL piorou ≥ 30%
- 2 ciclos consecutivos de incremento sem ganho líquido de volume (estrutura nova ainda pausada não conta como ciclo, §11.3)
- Sinal de saturação estrutural (frequência alta + CPM alto + CTR caindo)
- **Lucro/dia negativo sustentado** (ROAS < break-even em **2 ciclos consecutivos**, ou seja, campanha entrou em zona vermelha e não recuperou)

**Ação:** reverter ao último orçamento estável conhecido (com gate 🛡️) e emitir `handoff_para_otimizacao: true` com motivo (`cpa_degradou_30_pct_sustentado` | `dois_ciclos_sem_ganho_liquido` | `saturacao_estrutural` | `lucro_dia_negativo_sustentado`). **Skill de escala se desativa para essa campanha** até nova prontidão (respeitando cooldown: 7d perpétuo low/mid, 14d perpétuo high, 24h lançamento).

**Sugestão de investigação via `/trafego-diagnostico`:** antes de devolver para otimizar, sugerir ao aluno: "Quer investigar a causa com `/trafego-diagnostico` (diagnóstico diferencial)? Ele apresenta 3 hipóteses competitivas antes de agir." Se aceitar, fazer handoff para `/trafego-diagnostico` em vez de `/trafego-otimizar`. Se recusar, seguir o handoff padrão.

---

## 7. Lógica específica. Perpétuo

### 7.1 Low ticket (até R$ 500)
- Velocidade default: normal (+20% / 24h).
- Modo preferido: vertical até frequência 2,0, depois alternar horizontal.
- **Teto de escala vertical:** orçamento atual × 4 (ex: começou em R$ 50/dia, teto vertical em R$ 200/dia antes de obrigatoriamente abrir horizontal).
- Refresh criativo a cada 10 a 14 dias é pré-requisito para continuar escalando.

### 7.2 Mid ticket (R$ 501 a 1.499)
- Velocidade default: normal a conservadora.
- Janela mínima entre ajustes: 72h.
- Sempre confirmar CPA estável em 7d antes de cada incremento.
- Modo preferido: vertical + horizontal alternado.
- Refresh criativo a cada 14 a 21 dias.

### 7.3 High ticket (R$ 1.500+)
- Velocidade default: conservadora (+15% / 72h).
- Janela de referência: 14d ou 30d, **nunca 1d**.
- Modo preferido: horizontal puro com lookalikes e Advantage+ (audiência pequena de high ticket satura rápido em vertical).
- **Backup criativo obrigatório:** ≥ 3 ângulos diferentes no conjunto antes de qualquer incremento.

---

## 8. Lógica específica. Lançamento

### 8.1 Por fase

| Fase | Modo de escala | Velocidade | Tolerância CPL |
|---|---|---|---|
| Aquecimento | Não escala | n/a | n/a |
| Captação inicial | Vertical agressivo + horizontal | Agressiva (+30 a 50% / 24h); com score de confiança do falso vencedor de 50 a 74 (Passo 0.8), só conservadora ou normal | Até 1,3× target |
| Captação final | Horizontal puro (mais audiências) | Agressiva; com score de confiança do falso vencedor de 50 a 74, só conservadora ou normal | Até 2,0× target |
| Carrinho aberto | Trocar para campanha de Vendas. Não é escala de captação | n/a | n/a |

### 8.2 Regras específicas
- **Não escalar nas últimas 24h** da captação. Tempo insuficiente para o lead converter em volume útil.
- **Backup criativo:** mínimo 3 ângulos prontos antes de captação inicial. Mínimo 5 antes de captação final.
- **Volume diário absoluto** importa mais que CPL na captação final. Escala continua mesmo com CPL subindo, até o limite de 2× target.

---

## 9. Tetos de escala. Quando parar de tentar

A skill **interrompe escala e declara teto** quando:

- **Audiência exausta:** frequência > 4 mesmo após 2 refreshes criativos seguidos no mesmo conjunto.
- **CPM ceiling:** CPM 50%+ acima da média histórica da conta sustentado por 7d, sem evento sazonal explicando.
- **Volume ceiling:** 3 ciclos consecutivos sem ganho líquido de conversões mesmo com orçamento maior. Mercado endereçável atingiu limite.
- **Operacional:** a conta já chegou ao `teto_conta_diario_brl` declarado, ou seja, a folga do guardião de caixa (teto menos o gasto diário atual da conta, `folga_diaria_brl`) é zero ou negativa. Com folga positiva menor que o próximo incremento, não é teto: reduzir o incremento até caber na folga (guardião de caixa §5, mesma regra dura da Carteira na §3.6).
- **Margem:** ROAS sustentado < break-even (zona vermelha) em ≥ 2 ciclos consecutivos. Lucro/dia negativo é teto duro mesmo que volume e frequência ainda estejam saudáveis: escala que não dá margem é prejuízo. Espelhado da camada de lucro da otimizar (§3.6).

Quando algum teto é atingido, output declara explicitamente:

```yaml
teto_atingido:
  tipo: audiencia_exausta | cpm_ceiling | volume_ceiling | operacional | margem
  recomendacao: <ação alternativa, ex: "expandir para nova trilha de público" | "voltar pra /trafego-otimizar pra recuperar margem antes de retomar">
```

> **Sobre `tipo: margem`:** quando atingido, devolver pra `/trafego-otimizar` com motivo `lucro_dia_negativo_sustentado` (mesmo motivo do freio total §6.3). A diferença é semântica: freio é "tô parando", teto é "não dá pra continuar mesmo". Ambos disparam `handoff_para_otimizacao: true`.

---

## 10. Tratamento de dados imaturos pós-incremento

Após cada incremento, **não acionar freio** com base em dados imaturos:
- Gasto pós-incremento < 50% do novo orçamento diário
- Tempo desde incremento < 24h (na estrutura nova, desde a ativação, §11.3)
- < 1.000 impressões novas

Nesses casos, emitir `aguardar` e marcar próxima reanálise.

---

## 11. Confirmação obrigatória antes de executar

Antes de executar **qualquer ação**, a skill apresenta ao aluno um plano completo numerado e aguarda aprovação. Nenhuma `tool_call` é disparada sem confirmação explícita.

### 11.1 Formato do plano de confirmação

O plano vai dentro do bloco 🛡️ do CLAUDE.md. A skill lista cada ação proposta com número, tipo, objeto afetado, variação concreta, score de risco (Passo 0.85) e justificativa resumida, e fecha com reset de aprendizado e reversibilidade:

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Aqui está o que planejo fazer. Aprove tudo, aprove apenas alguns (informe os números) ou reprove:

[1] VERTICAL: subir orçamento do conjunto "PERP_LAL_1%" de R$ 200 para R$ 240 (+20%)
    Risco: 30/100 (médio) · Motivo: CPA 10% abaixo do target nas janelas média e longa, frequência 1,8

[2] HORIZONTAL: duplicar conjunto "PERP_LAL_1%" com teste PT Mundo, orçamento R$ 200/dia
    (criado pausado: não gasta nada até você pedir a ativação, que é uma confirmação à parte)
    Risco: 24/100 (baixo) · Motivo: abrir nova fonte de tráfego mantendo estrutura validada

[3] ADVANTAGE: criar campanha Advantage+ com os 5 melhores anúncios da conta, orçamento R$ 300/dia
    (criada pausada: não gasta nada até você pedir a ativação)
    Anúncios selecionados: [lista com IDs e nomes]
    Risco: 42/100 (médio) · Motivo: consolidar criativos vencedores em estrutura enxuta

Reset de aprendizado esperado: não em [1]; sim nas estruturas novas de [2] e [3]
Reversível? [1] sim, voltando o orçamento para R$ 200; [2] e [3] ficam pausadas, sem gasto, até a ativação

Aprovar tudo  |  Aprovar alguns (informe quais)  |  Reprovar tudo
```

Quando o falso vencedor não foi verificado (Passo 0.8), a linha de risco da ação ganha "· falso vencedor não verificado".

### 11.2 Regras da confirmação
- **Sempre listar todas as ações** antes de executar qualquer uma, mesmo que seja uma só.
- **Um "sim" (ou "aprovar tudo") cobre o lote inteiro do mesmo fluxo**, inclusive todas as criações de uma estrutura (campanha + conjuntos + anúncios). Depois do sim, executar sem reabrir o gate, exceto se uma chamada falhar, o aluno mudar o plano ou surgir escrita fora do lote.
- Se o aluno aprovar parcialmente, executar **somente** as ações aprovadas, na ordem da lista.
- Se o aluno reprovar uma ação e quiser ajuste, recalcular apenas aquela ação e reapresentar antes de executar.
- Ação com `risco_alto` aparece com tag ⚠️ e pede a confirmação reforçada da sub-skill `risco-incremento.md`; ação com `risco_extremo` nem entra no plano.
- **Estrutura nova (duplicação, CBO, Advantage) nasce pausada e continua pausada no fim do lote.** Nenhum fluxo ativa sozinho. Depois do lote, dizer que a estrutura foi criada e está pausada e perguntar se o aluno quer ativar agora. **Ativar só com pedido explícito**, num bloco 🛡️ próprio (operação "ativar estrutura nova"), que:
  - lista tudo o que será ativado (campanha, conjuntos e anúncios), com "status PAUSED → ACTIVE". Ao ativar uma campanha criada pela skill, ativar também os conjuntos e anúncios dela no mesmo lote, para não ficar "ativa sem entregar";
  - mostra quanto passa a gastar por dia, somado ao que já roda (os originais seguem rodando). Com teto da conta declarado, conferir antes no guardião de caixa que cabe;
  - só é oferecido depois de conferir que tudo foi criado e que cada conjunto novo tem pelo menos 1 anúncio (e, no Horizontal, a variação do teste aplicada);
  - usa `ads_activate_entity` (ou `ads_update_entity` com `status=ACTIVE`) no MCP e `POST /<id>` com `status=ACTIVE` no APP;
  - depois de ativar, anexa no histórico a linha da ativação, com a data e hora (§11.3).

  Se o aluno preferir revisar antes no Gerenciador, a estrutura fica pausada e ele pede a ativação depois (ou liga por lá; nesse caso a data da ativação é conferida no ciclo seguinte, §11.3).
- Se uma chamada falhar no meio, parar, mostrar o que já foi feito e perguntar antes de continuar.
- Após execução, devolver resumo com IDs criados/alterados e como reverter cada um (reduzir orçamento ou pausar; nunca apagar dentro deste fluxo).

### 11.3 Registro do ciclo
Depois de cada execução (incremento, duplicação, freio ou teto), anexar uma linha por ação executada em `meus-produtos/{ativo}/trafego/escalar/historico-{campaign_id}.md` (criar se não existir): data e hora da execução, objeto (nome e ID), modo, velocidade, orçamento antes e depois, ciclo (as ações de um lote novo levam `ciclo_atual` + 1; a ativação de estrutura nova repete o número do lote que a criou), score de risco e status (`incremento`, `estrutura_pausada`, `freio_leve`, `freio_medio`, `freio_total`, `teto`). É desse arquivo que a Leitura 3 do Passo 0.75 tira o `ciclo_atual`, contando ciclos e não linhas.

**Lote misto (ex.: Vertical + Horizontal):** cada ação aprovada ganha a sua linha, todas com a mesma data e hora da execução do lote e o mesmo número de `ciclo`. Essas linhas, mais as linhas de ativação anexadas depois delas, formam o **último ciclo**.

**Estrutura nova (Horizontal, CBO, Advantage):** na criação, a linha vai com status `estrutura_pausada`, que não conta como ciclo (nem no `ciclo_atual`, nem nos "2 ciclos sem ganho líquido" da §6.3, nem no volume ceiling da §9). Quando a estrutura é ativada (§11.2), anexar a linha `incremento` com a data e hora da ativação e o mesmo número de `ciclo` da linha `estrutura_pausada` dela (a ativação entra no ciclo do lote, não abre outro): o ciclo começa ali, e dela contam a próxima revisão (`proxima_revisao_horas`), a maturação (§4) e o tempo da §10.

**No ciclo seguinte, olhar todas as linhas do último ciclo**, não só a última do arquivo:
- Para cada linha `estrutura_pausada` sem linha de ativação da mesma estrutura depois dela, ler o status da estrutura nova. Se a leitura mostrar a estrutura já ativa (o aluno ligou no Gerenciador), conferir a data da ativação em `ads_account_get_activity_logs` (MCP) ou perguntar ao aluno, e anexar a linha `incremento` com essa data antes de avaliar.
- **Nenhuma entidade do último ciclo ativada** (todas as linhas são `estrutura_pausada` e as estruturas seguem pausadas): não há ciclo para avaliar; oferecer a ativação (§11.2).
- **Parte ativada** (ex.: o incremento vertical do mesmo lote, ou uma das estruturas novas): avaliar essa parte, cada uma depois da sua maturação (o vertical a partir do incremento, a estrutura nova a partir da ativação), e oferecer ativar o resto (§11.2).
- **Tudo ativado:** avaliar o ciclo inteiro.

---

## 12. Output esperado

O output ao aluno tem **duas partes**, sempre nessa ordem: primeiro o plano de escala narrado em bullets (legível), depois o plano técnico estruturado em YAML (executável).

### Parte 1. Plano de escala narrado em bullets (visível, em português)

Sempre antes do YAML, imprimir o bloco abaixo em markdown. Substituir os `{placeholders}` pelos valores reais.

```markdown
## Confiabilidade do dado

- **Janela / atribuição:** {ex: últimos 7 dias · 7d clique / 1d visualização ou padrão omni}
- **Pixel (evento-norte):** {ok | inferido pelo fluxo de vendas | sem disparo}
- **Confiança geral:** {alta | média | baixa}{se média: " · prosseguindo com aviso, premissa de margem rebaixada" | se baixa: " · ESCALA BLOQUEADA"}

## Recomendação por campanha

- **Campanha:** {nome legível}
- **Trilha:** {trilha legível, ex: "Perpétuo médio (R$ 501 a R$ 1.499)"}
- **Ciclo de escala:** {ciclo_atual} (ciclos de incremento consecutivos sem freio)
- **Estado atual:** orçamento R$ {valor} · {CPA | CPL} R$ {valor} · meta R$ {target} · margem CPA +{margem_pct}% · frequência {freq}
- **Primário:** {modo_primario} · {velocidade} ({justificativa curta referenciando os sinais ativos})
- **Alternativo:** {modo_alternativo} ({gatilho de migração: "considerar quando X passar de Y"})
- **Confiança:** alta | média | baixa (quando baixa, alternativo vira "Aguardar próximo ciclo de dados")
- **Risco do incremento:** {score}/100 ({faixa})

## Lucro (estimado, margem {margem}%)

- **ROAS atual:** {ROAS} · **ROAS de break-even:** {1 ÷ margem}
- **Lucro/dia hoje:** R$ {gasto_dia × (ROAS × margem - 1)}/dia
- **Lucro/dia projetado pós-incremento:** ~R$ {gasto_pos × (ROAS × margem - 1)}/dia (premissa: ROAS estável)
- **Zona:** {verde | amarela | vermelha} {se amarela: "(ATENÇÃO: zona amarela não escala, ver Passo 0.8)" | se vermelha: "(ATENÇÃO: zona vermelha bloqueia escala, devolver pra otimização)"}
- {se modo faixa: "lucro em faixa, margem 60 a 80%" | se confiabilidade média/baixa: "estimativa frouxa, não cravar"}

## Ferramentas de escala disponíveis

> Tudo que esta skill pode fazer pra crescer esta campanha. O plano de execução abaixo é o que eu **recomendo** dentro desse arsenal. Escalar só cresce o gasto: conter, realocar e frear são da `/trafego-otimizar` (princípio 14).

| Ferramenta de escala | O que faz | Reset de aprendizado? | Recomendado agora? |
|---|---|---|---|
| Vertical | sobe orçamento no vencedor (conjunto em ABO, campanha em CBO) | não | {✓ · velocidade + motivo curto / reserva · gatilho que ativaria} |
| Horizontal | duplica o vencedor isolado (campanha / conjunto / anúncio) | sim (estrutura nova reaprende) | {✓ · motivo / reserva · gatilho} |
| Vertical + Horizontal alternado | alterna subir verba e duplicar a cada ciclo | parcial | {✓ · motivo / reserva · gatilho} |
| Consolidação CBO | junta 3+ conjuntos vencedores numa campanha CBO | sim | {✓ · motivo / reserva · gatilho} |
| Campanha Advantage | 1 conjunto Advantage+ com 5 a 50 criativos vencedores | sim | {✓ · motivo / reserva · gatilho} |
| Carteira (conta sob teto) | redistribui a verba da conta inteira sob um teto de gasto | parcial | {✓ · motivo / reserva · gatilho} |
| Conter / realocar / frear (handoff `/trafego-otimizar`) | quando a escala não cabe mais, devolve pra reduzir, realocar ou frear | n/a | {✓ · motivo / reserva · gatilho} |

**Regra de preenchimento:**

1. Marcar `✓` só na(s) ferramenta(s) que a análise de hoje realmente pede, com a **velocidade** colada no motivo (ex: "✓ Vertical · conservadora +15%/72h, frequência 1,4 e ROAS verde"). A velocidade nunca vira coluna nem linha própria.
2. Marcar `reserva` em todas as demais, **com o gatilho que as ativaria** (ex: "reserva · quando a frequência passar de 2,2" ou "reserva · quando houver 5+ criativos vencedores validados"). Assim o aluno vê o poder todo da skill **e** entende por que só uma parte está sendo usada agora.
3. O `✓ Primário` e o `reserva` do `Alternativo` desta tabela **têm que bater** com o `modo_primario`, `modo_alternativo` e `gatilho_migracao_para_alternativo` do YAML (Parte 2). A tabela é a leitura humana do mesmo raciocínio.
4. **Sub-testes do Horizontal** (`pt_mundo`, `reels_only`, `instagram_only`, `facebook_only`, `advantage_placement`, `nova_segmentacao`) **não entram nesta tabela**: só aparecem no Plano de execução quando Horizontal é `✓`.
5. **Modo "Auditar toda a conta" (várias candidatas):** imprimir uma tabela **dentro do bloco de cada candidata**, em versão enxuta (só a coluna "Recomendado agora?" por ferramenta) quando houver mais de uma. Com 1 campanha, a tabela completa de 4 colunas.
6. **Nenhuma ferramenta evapora** (espelha o princípio 15): toda linha aparece sempre, marcada `✓` ou `reserva`. Se uma ferramenta foi cogitada na análise e não entrou, vira `reserva` com o motivo, nunca some.

## Plano de execução

- {ação 1 com objeto e variação concreta, ex: "Subir orçamento do conjunto X de R$ 200 para R$ 240 (+20%)"}
- {ação 2}
- {ação 3}

## Riscos observados

- {risco 1 em frase curta}
- {risco 2}

## Próxima revisão

- {data/horas para reanalisar e próximo passo}

## Status do ciclo

{escalando | aguardando dado maturar | freio leve / médio / total | teto atingido}
```

**Tradução obrigatória dos enums** (nunca imprimir o nome técnico em snake_case na narrativa):

| Enum técnico | Frase em português |
|---|---|
| `vertical` | "vertical (subir orçamento no conjunto vencedor)" |
| `horizontal` | "horizontal (duplicar vencedor com isolamento)" |
| `vertical_e_horizontal` | "vertical + horizontal alternado" |
| `cbo_consolidacao` | "consolidação em CBO" |
| `advantage_plus_consolidacao` | "campanha Advantage" |
| `carteira` | "carteira (conta inteira sob teto de gasto)" |
| `aguardar_proximo_ciclo` | "aguardar próximo ciclo de dados (24 a 48h) antes de comprometer orçamento" |
| `conservadora` | "conservadora (+15% / 72h)" |
| `normal` | "normal (+20% / 24h)" |
| `agressiva` | "agressiva (+30 a +50% / 24h)" |
| `incrementar` | "escalando" |
| `aguardar` | "aguardando dado maturar" |
| `freio_leve` | "freio leve: pausar próximo incremento" |
| `freio_medio` | "freio médio: reverter último incremento" |
| `freio_total` | "freio total: devolver para otimização" |
| `teto_atingido` | "teto atingido" |
| `confianca: alta` | "confiança alta" |
| `confianca: media` | "confiança média" |
| `confianca: baixa` | "confiança baixa, sinais ambíguos" |

### Parte 2. Plano técnico estruturado (YAML)

Imediatamente após a Parte 1, prefixar com a linha "Plano técnico estruturado (para execução):" e entregar:

```yaml
campaign_id: <id>
trilha: perpetuo_low | perpetuo_mid | perpetuo_high | lancamento_low | lancamento_mid | lancamento_high
modo_conexao: MCP_CONECTOR | APP
modo_primario: vertical | horizontal | vertical_e_horizontal | cbo_consolidacao | advantage_plus_consolidacao | carteira
modo_alternativo: vertical | horizontal | vertical_e_horizontal | cbo_consolidacao | advantage_plus_consolidacao | aguardar_proximo_ciclo | null
gatilho_migracao_para_alternativo: <texto curto, ex: "frequência > 2.2 ou CPM +15% no próximo ciclo">
confianca: alta | media | baixa
score_primario: 8                               # soma dos pontos do modo primário
score_alternativo: 5                            # soma dos pontos do modo alternativo
velocidade: conservadora | normal | agressiva
ciclo_atual: 3                                  # quantos ciclos de incremento já feitos nessa onda (ciclos, não linhas; Leitura 3 do Passo 0.75)
revisar_inputs: false | true                    # true quando inputs default da sessão destoam desta campanha (modo "Auditar toda a conta")

vencedores_conta:                               # leitura da conta inteira (Passo 0.75.1)
  total_adsets_vencedores_no_objetivo: 4
  total_ads_vencedores_espalhados: 7
  sinaliza_oportunidade_cbo: true | false
  sinaliza_oportunidade_advantage: true | false

dados_ausentes:                                 # política de "nunca inventar dado" (Passo 0.75.1.1)
  campos_indisponiveis:
    - campo: <nome do campo>
      motivo: <texto curto, ex: "campanha tem 2 dias, frequência ainda não estabilizou">
  sinais_indeterminados:                        # sinais excluídos da soma da matriz por falta de dado real
    - <nome do sinal>
  total_sinais_indeterminados: 0
  forcou_confianca_baixa: false | true          # true quando >= 3 sinais ficaram indeterminados

estado_atual:
  orcamento_diario_atual_brl: 240.00
  budget:
    tipo: ABO | CBO | null                      # ABO = orçamento por conjunto, CBO = orçamento por campanha
    nivel_aplicacao: adset | campaign | indeterminado
    objeto_id_alvo: <adset_id se ABO, campaign_id se CBO>
  cpa_ou_cpl_atual: 145.30
  target: 200.00
  margem_seguranca: 0.27
  frequencia: 2.1
  cpm_vs_historico_pct: +12
  ctr_link_unico: ...                           # primário no APP (unique_inline_link_click_ctr); no conector fica null (/trafego-insights §10.1)
  ctr_link_total: ...                           # link_click ÷ impressions; primário no conector, declarando a troca (ver §0.75.1 mapa de campos)
  criativos_saudaveis: 3

confiabilidade_do_dado:                         # Passo 0.78, preencher SEMPRE
  nivel: alta | media | baixa
  janela: "7d" | "14d" | "30d"
  atribuicao: "7d_clique_1d_visualizacao" | "padrao_omni_da_api"
  pixel_evento_norte: ok | inferido_pelo_fluxo_de_vendas | sem_disparo
  conciliacao_conta: bate | nao_bate | nao_aplicavel    # nao_aplicavel quando escopo é recorte
  motivos: [ ... ]                              # presente quando nivel != alta

lucro:                                           # §3.6 da otimizar, preencher quando margem coletada (Passo 0.7 P4)
  margem_contribuicao: 0.77
  margem_fonte: perguntas_guiadas | faixa(0.60-0.80) | default
  roas_atual: 1.85
  roas_breakeven: 1.30                          # 1 ÷ margem
  cpa_breakeven_brl: 2080                       # AOV × margem
  lucro_dia_atual_brl: ...                      # gasto_dia × (ROAS × margem - 1)
  lucro_dia_projetado_pos_incremento_brl: ...   # gasto_pos × (ROAS × margem - 1), premissa ROAS estável
  zona: verde | amarela | vermelha              # bloqueia escala se != verde

risco_incremento:                               # Passo 0.85, ver sub-skills/risco-incremento.md
  score: 30
  faixa: risco_baixo | risco_medio | risco_alto | risco_extremo

falso_vencedor:                                 # Passo 0.8, leitura do detector da /trafego-diagnostico
  verificado: true | false                      # false = "falso vencedor não verificado" no plano da §11
  classificacao: vencedor_real | null           # outra classificação bloqueia a escala
  score_confianca: 78 | null                    # abaixo de 50 bloqueia; de 50 a 74, só escala gradual

guardiao_caixa:                                 # Passo 0.86, presente quando há teto ou modo carteira
  urgencia: caixa_seguro | caixa_atencao | caixa_critico
  folga_diaria_brl: ...

decisao:
  acao: incrementar | aguardar | freio_leve | freio_medio | freio_total | teto_atingido
  detalhes:
    novo_orcamento_brl: 288.00                  # em reais; no APP vai como inteiro em centavos (28800), ver unidade no Passo 0.0
    incremento_pct: 20
    duplicacoes_horizontais: []                 # lista de conjuntos a duplicar quando modo=horizontal
  proxima_revisao_horas: 48                     # vertical: a partir do incremento; estrutura nova: a partir da ativação (§11.3)

tool_calls:                                     # nome lógico; na execução, traduzir pela tabela do Passo 0.0
  - name: update_adset_budget | update_campaign_budget | duplicate_adset | duplicate_campaign | create_campaign_cbo | create_campaign_advantage | activate_entity | ...   # activate_entity só em bloco 🛡️ próprio (§11.2)
    tool_real_mcp: ads_update_entity | ads_create_ad_set(source_adset_id) | ads_create_campaign(source_campaign_id) | ads_create_ad(source_ad_id) | ads_activate_entity   # MCP
    curl_app: "POST /<id> daily_budget" | "ler → recriar: POST /act_<id>/adsets + /ads (creative_id)" | "POST /<id> status=ACTIVE" | ...                            # APP
    params: { ... }                             # parâmetros prontos

riscos_observados:
  - "frequência subindo, monitorar próximo ciclo"

handoff_para_otimizacao:
  ativo: false | true
  motivo: cpa_degradou_30_pct_sustentado | dois_ciclos_sem_ganho_liquido | saturacao_estrutural | teto_atingido_audiencia | lucro_dia_negativo_sustentado | null
  contexto:
    orcamento_revertido_brl: ...                # se ativo=true
    incrementos_revertidos: ...
    ultimo_orcamento_estavel_brl: ...
    ciclos_de_escala_completados: ...
  recomendacao_para_otimizacao: [ ... ]         # texto livre orientando o próximo diagnóstico

teto_atingido:                                  # null quando não houve teto
  tipo: null | audiencia_exausta | cpm_ceiling | volume_ceiling | operacional | margem
  recomendacao: ...
```

### Exceção
Se o aluno disser explicitamente "me dá só o YAML" ou "modo direto" na sessão, omitir a Parte 1.

### 12.1. Tabelas em português

TODA tabela markdown impressa para o aluno (Análise + Recomendação do Passo 0.75, status pós-execução, lista de candidatas em modo "Auditar toda a conta") deve usar cabeçalhos em português brasileiro. Aplicar o mesmo mapa de tradução documentado em **`.claude/skills/trafego-otimizar/SKILL.md` seção 13.1** (Investimento, Impressões, Frequência, CTR único no link, CPA, ROAS, Carrinho → Compra etc.). Os identificadores de campo dentro do YAML técnico continuam em snake_case (vão para tool_calls).

---

## 13. Princípios que a skill nunca viola

1. **Incrementos respeitam a velocidade declarada.** Nunca pular degraus.
2. **Sempre revalidar gatilho** antes de cada incremento. Não é piloto automático.
3. **Backup criativo é pré-requisito** para velocidade agressiva.
4. **Freio é prioridade sobre crescimento.** Qualquer sinal de degradação para a escala antes do próximo incremento.
5. **Devolução clara para `/trafego-otimizar`.** Quando freio total acionado, transferência é explícita e a skill se desativa para aquela campanha até cooldown vencer.
6. **Tetos são declarados, não ignorados.** Atingir limite, parar e comunicar, não insistir.
7. **Mudanças graduais mesmo em modo agressivo.** +50% é o teto absoluto de incremento único, sem exceção.
8. **Aprendizado é capital.** Toda decisão pondera custo de reset vs ganho de escala.
9. **Skill de escala não diagnostica problema fora da escala.** Qualquer gargalo identificado fora do escopo de crescimento é devolvido para `/trafego-otimizar`.
10. **Respeita cooldown do handoff.** Após devolução para otimização, não aceita nova prontidão antes do prazo (7d perpétuo low/mid, 14d perpétuo high, 24h lançamento), contado da última linha `freio_total` do histórico da campanha, inclusive quando chega por handoff da `/trafego-otimizar` (Passo 0.1).
11. **Confirmação obrigatória antes de executar.** Nenhuma tool_call é disparada sem aprovação explícita do aluno no bloco 🛡️. Um "sim" cobre o lote do mesmo fluxo; o modo Carteira exige "aprovar tudo" explícito; estrutura nova nasce e continua pausada, e ativar é operação à parte com bloco 🛡️ próprio (§11.2); DELETE nunca faz parte de plano de escala.
12. **Nunca inventar dado.** Toda métrica usada nos sinais, scores e recomendação vem de leitura real via `/trafego-insights` ou arquivo local. Se o dado não está disponível (campanha sem histórico, evento sem disparos, leitura falhou, denominador zero, conta nova sem 14 dias), marcar `null` ou `dados_disponiveis: false` explicitamente no payload. Sinais que dependem de dado ausente **não são pontuados** na matriz (não viram +0 nem chute). Quando ≥ 3 sinais ficam ausentes, forçar `confianca: baixa` e degradar a recomendação para "Aguardar próximo ciclo de dados". Estimativas, médias do setor, benchmarks externos e suposições estão proibidos. Se o aluno perguntar "e quanto seria o CPM esperado?" e a conta não tem histórico, responder "não tenho esse dado", sem inventar média de mercado.
13. **Detectar ABO vs CBO antes de qualquer mudança de orçamento.** Ler `budget.tipo` da campanha em todas as leituras do Passo 0.75. Em ABO, incrementos verticais e duplicações horizontais aplicam no `adset_id`; em CBO, aplicam na campanha. A tool real é a mesma nos dois casos, **`ads_update_entity`** (MCP) ou curl `POST /<id>` daily_budget (APP); o que muda é o **objeto-alvo** (`adset_id` em ABO, `campaign_id` em CBO). Modo Vertical em CBO sobe o orçamento da campanha (afeta todos os conjuntos); em ABO sobe somente do conjunto vencedor. Sem o tipo detectado, não executar: bloquear com `acao: aguardar` e motivo "tipo de orçamento não detectado". O `objeto_id_alvo` no output **precisa** bater com o tipo (adset_id se ABO, campaign_id se CBO); aplicar no objeto errado quebra a chamada ou afeta o nível errado.
14. **Crescer é a alavanca única aqui.** A `/trafego-escalar` sempre **aumenta** o gasto total da campanha. Conter, redistribuir e instalar limites (§6.3 realocação neutra, §6.4 limites por conjunto, §6.5 cost cap, §7.4 cortar posicionamento da `/trafego-otimizar`) **não são da escala**: são alavancas neutras ou pra baixo, e vivem na otimizar. Quando o caso pede uma dessas durante a escala (ex: CBO com distribuição torta pedindo piso/teto, ou CPA flutuando pedindo cost cap), a escalar **não absorve** a ferramenta: pausa o ciclo e faz handoff pra `/trafego-otimizar`. Filosofia simétrica: otimizar nunca aumenta gasto total; escalar nunca diminui nem redistribui sem aumentar (o modo Carteira só planeja os cortes; quem executa é a otimizar).
15. **Nenhum item evapora.** Toda campanha auditada que reprovou no checklist de prontidão (Passo 0.8), na confiabilidade do dado (Passo 0.78) ou no risco (Passo 0.85) **tem que aparecer no output** com o motivo da reprovação: em modo "Auditar toda a conta" como `🔴 reprovadas`, em modo "Filtrar e escolher" como nota explícita. Nunca sumir entre o passo de leitura e o plano de execução. Se o aluno perguntar "e a campanha X que apareceu?", é sinal de que essa regra foi violada. Espelhada de [.claude/skills/trafego-otimizar/SKILL.md](../trafego-otimizar/SKILL.md) §13 ("Rastreamento obrigatório").
16. **Decidir por lucro; CPA é guardrail, não juiz.** Quando a margem é coletada na Pergunta 4 do Passo 0.7, traduzir tudo em reais via §3.6 da otimizar (`roas_breakeven = 1 ÷ margem`, `lucro_dia = gasto_dia × (ROAS × margem - 1)`). A escala **só roda em zona verde** (ROAS sustentado ≥ break-even, lucro/dia ≥ 0): zona amarela (CPA bom mas margem fraca) é devolvida pra otimização (Passo 0.8 e §12 da otimizar); zona vermelha (lucro/dia negativo) dispara freio total (§6.3) e o teto de margem (§9, `tipo: margem`). Em modo faixa de margem (60 a 80%, sem dado preciso), exigir lucro/dia ≥ 0 no extremo conservador (margem 60%): a escala não aposta em margem otimista. **Custo fixo (aluguel, salário) nunca entra na decisão de campanha**, só na "saúde da empresa" (contexto, opcional na otimizar §3.6).
17. **Duplicar é ler e recriar, não confiar em cópia profunda.** No APP, `/copies` só para entidade pequena; estrutura com 2 ou mais objetos é recriada a partir da leitura, com anúncios referenciando o `creative_id` existente (§3.2). No MCP, `source_*_id`, conferindo que os anúncios vieram junto (senão, `ads_create_ad` com `source_ad_id`) e que a variação do teste foi aplicada; se a Meta recusar, duplicação guiada no Gerenciador.
