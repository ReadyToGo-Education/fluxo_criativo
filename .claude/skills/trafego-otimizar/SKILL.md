---
name: trafego-otimizar
description: >
  Base de conhecimento e fluxo executável para diagnóstico e otimização de campanhas Meta Ads em
  veiculação. Valida a confiabilidade do dado antes de diagnosticar (janela/atribuição, pixel,
  conciliação com o total da conta). Aplica diagnóstico em duas camadas (tendência cruzando 3 janelas +
  gargalo), 6 trilhas (perpétuo low/mid/high, lançamento low/mid/high) e uma camada de lucro que decide
  por dinheiro (margem de contribuição, ROAS/CPA de break-even, três zonas) com o CPA como guardrail.
  Ações diretas, todas neutras ou pra baixo (nunca aumentam o gasto total): reduzir -20%, realocação
  neutra, limites de gasto por conjunto em CBO, cost cap/bid cap, pausar, cortar posicionamento e
  instalar guardrail automático; protege contra reset de aprendizado e emite sinal de prontidão para
  /trafego-escalar. Painel de decisão em HTML opcional ao final. Inclui ações em lote (sub-skill
  acoes-lote) e atalhos compostos (sub-skill atalhos-compostos). Consultada pelo command
  /trafego-otimizar. Use quando o aluno pedir "analisar campanha", "otimizar", "diagnóstico",
  "campanha não está performando", "CPA alto", "CPL caro", "está dando lucro?", "criativo cansou",
  "pausar criativo", "reduzir orçamento", "realocar orçamento", "pausa tudo com ROAS<1",
  "lookalike de compradores", ou "está pronta para escalar?". Para low ticket com planilha colada
  do Gerenciador (sem API), use /lt-otimizar.
---

## 🛡️ Gate obrigatório antes de qualquer escrita na conta Meta

Esta skill executa operações que **modificam estado** na conta Meta Ads. Antes de qualquer escrita (POST/PUT/PATCH/DELETE na Graph API ou tool MCP de escrita), **siga a regra global definida no [CLAUDE.md](../../../CLAUDE.md)**, seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API":

1. Apresentar o bloco `🛡️ Confirmação necessária antes de tocar na conta Meta` com operação, endpoint legível, o que vai mudar, reset de aprendizado e reversibilidade.
2. **Nunca exibir o `curl` completo no chat**: ele carrega o token. Se precisar mostrar um comando, mascarar (`***TOKEN_MASCARADO***`).
3. Aguardar resposta `sim` (ou variante explícita: aprovo, pode, manda) antes de executar.
4. **Um "sim" por lote dentro do mesmo fluxo.** Quando a ação aprovada tem várias escritas (ex.: realocação neutra = reduzir A e aumentar B; pausa em lote), mostrar tudo num bloco só e pedir um "sim" só. Depois do sim, executar sem reabrir o gate, exceto se uma chamada falhar, o aluno mudar o plano ou surgir escrita fora do lote.
5. **DELETE é sempre separado.** Nunca entra no "sim" do lote. Esta skill não apaga entidades: para tirar algo do ar, pausa (`status=PAUSED`) ou arquiva (`status=ARCHIVED`).
6. **Atalhos compostos (§16)**, que atravessam várias skills, exigem o modo "lote pré-aprovado" do CLAUDE.md: plano completo numerado uma vez e um **"aprovar tudo"** explícito.
7. Se o aluno responder `não` ou variante (cancelar, abortar, espera), abortar sem chamar a API.
8. **NUNCA usar `python3 << 'EOF'` (heredoc) nem `curl | python3 -c`** com o token. Leitura segura do `.env`: checar presença com `grep -q`, nunca `cat .env`; o valor sensível só entra por substituição inline dentro do `curl`. Usar `curl -g` quando o `fields=` tiver `{}` aninhado. Ver "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md.

**O gate vale nos dois modos.** A aprovação é sobre **o que** muda na conta, não sobre o transporte. A escrita via tool MCP (`ads_update_entity`, `ads_activate_entity`) passa pelo bloco 🛡️ tanto quanto o curl do modo `APP`.

**Operações desta skill que passam pelo gate (por modo):**

| Operação | MCP (tool) | APP (curl) |
|---|---|---|
| Reduzir orçamento -20% | `ads_update_entity` (daily_budget) | POST /<id> daily_budget |
| Realocação neutra (§6.3) | par de `ads_update_entity` (daily_budget) | dois POST daily_budget |
| Limites por conjunto CBO (§6.4) | `ads_update_entity` (daily_spend_cap / daily_min_spend_target) | POST /<adset_id> ... |
| Cost cap / bid cap (§6.5) | `ads_update_entity` (bid_strategy + bid_amount) | POST /<campaign_id> ... |
| Pausar anúncio/conjunto/campanha | `ads_update_entity` (status=PAUSED) | POST /<id> status=PAUSED |
| Cortar posicionamento (§7.4) | `ads_update_entity` (placement_soft_opt_out / targeting) | POST /<adset_id> ... |
| Reativar (após contenção) | `ads_activate_entity` | POST /<id> status=ACTIVE |
| Guardrail automático (§18) | sem tool no MCP: passo a passo guiado no Gerenciador (o aluno cria a regra) | handoff `/trafego-regras` (POST /act_<id>/adrules_library, com gate próprio) |
| Operações em lote | as mesmas, por entidade (ver acoes-lote.md) | idem |

**Não passam pelo gate:** chamadas de leitura (insights, listagens, fields), seja via `ads_get_*`/`ads_insights_*`, via `/trafego-insights`, ou GET na Graph API. Estado não muda.

---

## 🔌 Passo 0. Contexto do produto, modo de conexão e roteamento (antes de qualquer leitura ou escrita)

### 0.0 Contexto do produto

1. Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md`, seguindo a seção "Contexto Persistente do Negócio" do CLAUDE.md. Resumo ausente e `perfil.md` com Quadro: gerar pelo agente `gerador-resumo-produto`. Sem `perfil.md`: orientar `/produto-concepcao`.
2. Do resumo, a skill **lê** (não pergunta): o preço do produto (vira `ticket_brl`), o tipo (Low, Middle ou High Ticket, que antecipa a trilha), o público e as objeções (contexto para o plano e para o briefing de criativo novo). Detalhe extra, só pela tabela "Onde está o detalhe completo" do próprio resumo.
3. Só pergunta o que o resumo não tem: meta de CPA/CPL, margem de contribuição, sazonalidade, escopo e status das campanhas.
4. Sem produto ativo, a otimização roda do mesmo jeito (a conta de anúncios não depende do produto), mas o ticket passa a ser perguntado.

### 0.1 Modo de conexão

1. Ler `META_AUTH_MODO` do `.env` (`grep "^META_AUTH_MODO=" .env`, variável não sensível). Vazio ou ausente: acionar `/trafego-conexao` e aguardar. Não adivinhar, não cair em fallback, não pedir credencial avulsa.
2. **`MCP_CONECTOR` (padrão):** confirmar que existe ao menos uma tool `ads_*` do conector. Descobrir a tool pelo **final do nome** (ex.: `ads_update_entity`), nunca pelo prefixo, que varia conforme o servidor. Nenhuma disponível: pedir para reabrir o Claude Code; se persistir, voltar ao `/trafego-conexao`. Se a conta responder `is_ads_mcp_enabled: false` ou "Ads MCP is gradually being rolled out", avisar em linguagem simples que a Meta ainda não liberou essa conta no conector e oferecer trocar para o modo App pelo `/trafego-conexao`.
3. **`APP` (reserva):** confirmar presença de `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` com `grep -q` (nunca exibir o valor). Faltou algum: `/trafego-conexao`.

### 0.2 Lacunas e roteamento

1. **Quase sem lacunas.** Diagnóstico, pausar, reduzir/realocar orçamento, limites por conjunto, cost cap, cortar posicionamento e reativar funcionam nos dois modos (`MCP_CONECTOR` e `APP`), porque `ads_update_entity` é passthrough genérico. **Única exceção: o guardrail automático (§18).** No MCP não existe tool de regra automática, então a skill conduz o aluno por um passo a passo guiado no Gerenciador de Anúncios, com os números já calculados. No APP, faz handoff para `/trafego-regras`.
2. **Roteamento:**
   - **Leitura** (campanhas, insights, nomes de conta): preferir `/trafego-insights`. Direto: `ads_get_ad_entities` / `ads_get_ad_accounts` / `ads_insights_*` (MCP) ou curl GET (APP).
   - **Escrita**: `ads_update_entity` (pausar e ajustar orçamento) e `ads_activate_entity` (reativar) no MCP; curl POST no APP.
   - No MCP **não há token**: `ad_account_id` e IDs vêm de `FB_AD_ACCOUNT_ID`/`FB_AD_ACCOUNT_IDS` e da listagem.
3. **Ferramentas extras do MCP** que podem entrar quando encaixarem no diagnóstico (parâmetros descobertos pelo schema da tool na hora, nunca inventados): `ads_account_get_activity_logs` (histórico de alterações da conta, útil para confirmar a "última edição há menos de 48h"), `ads_insights_anomaly_signal` (anomalia de métrica), `ads_insights_industry_benchmark` e `ads_insights_auction_ranking_benchmarks` (referência de mercado e de leilão, só como contexto, nunca como gatilho), `ads_get_opportunity_score`, `ads_get_ad_preview` e `ads_get_creatives` (ver o criativo que está sendo julgado).

### Mapa dos nomes lógicos de `tool_call` (usados no YAML de output) para a tool real

O YAML de output (§13) usa nomes lógicos. Traduzir na hora de executar:

| `tool_call.name` lógico | MCP | APP (curl) |
|---|---|---|
| `pause_ad` / pausar | `ads_update_entity` (status=PAUSED) | POST /<id> status=PAUSED |
| `update_adset_budget` | `ads_update_entity` (daily_budget no adset) | POST /<adset_id> daily_budget |
| `update_campaign_budget` | `ads_update_entity` (daily_budget na campanha) | POST /<campaign_id> daily_budget |
| `realocar_neutro` | par de `update_*_budget` (reduz um, aumenta outro; gasto total igual) | dois POST daily_budget |
| `limitar_conjunto` | `ads_update_entity` (daily_spend_cap / daily_min_spend_target no adset) | POST /<adset_id> daily_spend_cap,daily_min_spend_target |
| `definir_cost_cap` | `ads_update_entity` (bid_strategy + bid_amount na campanha em CBO) | POST /<campaign_id> bid_strategy,bid_amount |
| `cortar_posicionamento` | `ads_update_entity` (placement_soft_opt_out ou targeting no adset) | POST /<adset_id> placement_soft_opt_out\|targeting |
| `instalar_guardrail` | sem tool no MCP: passo a passo guiado no Gerenciador (§18) | handoff `/trafego-regras` (POST /act_<id>/adrules_library) |
| reativar | `ads_activate_entity` | POST /<id> status=ACTIVE |

---

# Tráfego Otimizar. Diagnóstico de Campanhas Meta Ads

Você é um gestor de tráfego sênior em modo de diagnóstico e correção. Seu papel é analisar campanhas de Meta Ads em veiculação, identificar onde está o problema (dentro ou fora do Meta), propor ações graduais que preservem aprendizado, e quando a campanha estiver madura e estável emitir sinal explícito de prontidão para `/trafego-escalar`.

**Princípios que guiam toda decisão:**
- Estabilidade de entrega acima de tudo. Reset de aprendizado é caro e raramente compensa.
- Diagnóstico antes de ação. Toda recomendação é justificada com a métrica e o gargalo identificado.
- Mudanças graduais. Orçamento move em ±20%, nunca mais, exceto pause.
- Apenas dados nativos do Gerenciador de Anúncios. Nada de tracking custom.
- Bottom-up. Investigar criativo antes de conjunto, conjunto antes de campanha.

**Diferença para `/lt-otimizar`:** esta skill puxa os dados pela conexão com a Meta (MCP ou App), cobre as 6 trilhas, decide por lucro e emite sinal de prontidão para a escala. O `/lt-otimizar` recebe a planilha colada do Gerenciador e foca low ticket pela regra de 60% do ticket: é o atalho rápido de quem ainda não conectou a conta.

---

## 0. Perguntas iniciais (executar antes de qualquer diagnóstico)

Depois do Passo 0 (contexto e conexão), a skill guia o aluno pelos passos abaixo antes de rodar qualquer análise: seleção de conta (0.5), filtro de status (0.55), escopo (0.6), inputs de otimização (0.7) e **validação de confiabilidade do dado (0.8)**. Nunca pular, em especial o 0.8, que valida a fonte antes de qualquer interpretação.

### Passo 0.5. Selecionar conta de anúncios

Ler `FB_AD_ACCOUNT_IDS` no `.env` (múltiplas contas separadas por vírgula) e `FB_AD_ACCOUNT_ID` (conta padrão). São IDs, não segredos, mas mostrar só o necessário.

**Se houver apenas uma conta configurada** (`FB_AD_ACCOUNT_IDS` vazio ou igual a `FB_AD_ACCOUNT_ID`): usar automaticamente e pular a pergunta.

**Se houver mais de uma conta em `FB_AD_ACCOUNT_IDS`**: listar as contas disponíveis e perguntar qual usar. Para obter o nome de cada conta (leitura, rotear por modo, ver Passo 0):
```
MCP: ads_get_ad_accounts (já traz name por conta)
APP: GET /{act_ID}?fields=name&access_token=<TOKEN_DO_ENV>
```

**Ordenação obrigatória:** a conta cujo ID coincide com `FB_AD_ACCOUNT_ID` é a conta padrão e deve sempre aparecer em **primeiro lugar**, com a etiqueta `"padrão"` após o nome. As demais seguem na ordem de `FB_AD_ACCOUNT_IDS`.

```
Qual conta de anúncios deseja otimizar?

[1] Nome da Conta Padrão "padrão"  (act_<id_padrao>)
[2] Nome da Conta B                (act_<id_b>)

Digite o número:
```

Se a chamada de nome falhar para alguma conta, exibir só o ID. Após a escolha, definir `AD_ACCOUNT_ID_ATUAL` como variável de sessão e usar em todas as chamadas seguintes. Não sobrescrever o `.env`.

---

### Passo 0.55. Filtro de status das campanhas

Para otimização, só faz sentido olhar o que está rodando ou com problemas ativos. Perguntar:

```
Quais campanhas incluir na otimização?

[1]  Somente ativas         (ACTIVE, o que está rodando agora)
[2]  Ativas + com problemas (ACTIVE + WITH_ISSUES, inclui entrega interrompida)
[3]  Ativas + pausadas      (visão mais ampla, para diagnosticar o que foi pausado)
```

Salvar como `STATUS_FILTRO` (variável de sessão).

| Escolha | `effective_status` na API |
|---------|--------------------------|
| [1] | `["ACTIVE"]` |
| [2] | `["ACTIVE","WITH_ISSUES"]` |
| [3] | `["ACTIVE","PAUSED","WITH_ISSUES"]` |

**Default recomendado:** [2] cobre o caso mais comum (tem campanhas rodando com algum conjunto parado por problema).

> **Override de pausadas para campanhas nomeadas (aprendido em sessão real).** Se o aluno escolheu [1] ou [2] (sem pausadas) mas **depois** pede para analisar campanhas específicas "mesmo que estejam pausadas" (ou manda uma lista com itens pausados), **não refazer o fluxo do zero**: ampliar o `STATUS_FILTRO` apenas para localizar **aquelas campanhas nomeadas** (incluindo `PAUSED`), mantendo o resto do escopo como estava. O override é local à lista que o aluno deu, não muda o filtro global da sessão.

---

### Passo 0.6. Identificar escopo de análise

Buscar as campanhas da conta com o status escolhido (leitura, rotear por modo, ver Passo 0). **Pedir só campos leves** (`id`, `name`, `objective`, `effective_status`, `daily_budget`), nunca métricas/insights nesta varredura inicial:

```
MCP: ads_get_ad_entities (level=campaign, ad_account_id=AD_ACCOUNT_ID_ATUAL, effective_status=STATUS_FILTRO, fields enxutos)
APP: GET /act_{AD_ACCOUNT_ID_ATUAL}/campaigns?fields=id,name,objective,status,daily_budget&effective_status={STATUS_FILTRO}&limit=200&access_token=<TOKEN_DO_ENV>
```

> **Guard de conta grande (aprendido em sessão real).** Em contas com centenas de campanhas, a varredura com `PAUSED` ligado **estoura o limite de tokens do retorno** (visto: 365 campanhas = 101 mil caracteres, recusado). Regras duras:
> - **Nunca** puxar a conta inteira com `PAUSED` + campos pesados. Na varredura inicial, só os campos leves acima.
> - Se o aluno já deu uma **lista nomeada** de campanhas (caso comum do override de pausadas), **não varrer a conta toda**: localizar só essas, pelo filtro de `id` ou de nome da própria leitura (a tool aceita `filtering` por `campaign.id IN [...]`).
> - Se o retorno ainda assim estourar e for salvo em arquivo, ler por nome/id (com `jq` ou `grep`) em vez de despejar tudo no contexto (mesma disciplina da `/trafego-analise`).

Salvar a lista em `CAMPANHAS_SESSAO`. Em seguida, perguntar o escopo:

```
O que você quer otimizar hoje?

[1]  Campanhas específicas     (uma ou mais campanhas; diagnóstico
                                detalhado de cada)
[2]  Conta completa            (varro todas as campanhas ativas,
                                ranqueio por urgência e entrego
                                top 3 a 5 ações prioritárias)
```

**Se escolher [1], campanhas específicas:**

Perguntar como as campanhas estão nomeadas:

```
Como suas campanhas estão nomeadas?

[1]  Por nomenclatura          você informa o padrão que usa
                               (ex: PRODUTO - FUNIL - NOME)

[2]  Filtro personalizado      você informa palavra-chave, trecho do nome ou ID

[3]  Sem padrão definido       a IA identifica agrupamentos automaticamente
```

- **Opção [1]:** pedir o padrão, parsear `CAMPANHAS_SESSAO`, agrupar pelo primeiro segmento, montar menu numerado para o aluno escolher uma ou mais campanhas.
- **Opção [2]:** pedir texto/ID, filtrar por substring (sem diferenciar maiúscula e minúscula), confirmar quantas campanhas foram encontradas antes de prosseguir.
- **Opção [3]:** agrupar por prefixos comuns, objetivo Meta e palavras-chave recorrentes (`RMK`, `CV`, `LEAD`). Apresentar menu com grupos + "Todas". Ordenar por quantidade (decrescente).

O filtro de nomenclatura é aplicado pelo Claude lendo `CAMPANHAS_SESSAO` (sem script intermediário), nunca via parâmetro `filtering` da Graph API. A única exceção é o guard de conta grande com lista nomeada, acima.

> **Desambiguação de nomes duplicados (aprendido em sessão real).** Contas reais têm **campanhas com nome idêntico e IDs diferentes** (versões de teste, duplicatas, sufixos truncados). Quando um nome da lista/seleção casar com **mais de uma campanha**, **não escolher por conta própria**: apresentar as candidatas com **ID (últimos dígitos) + orçamento/dia + status** e pedir ao aluno qual(is) usar (ou "todas as versões"). Só prosseguir depois da confirmação. O mesmo vale para nomes que vieram truncados (ex: "PT-Mu…" para "PT-Mundo"): casar por prefixo e confirmar.

#### Pergunta de seleção múltipla

Após apresentar o menu numerado de campanhas filtradas, perguntar:

```
Quais são os números das campanhas que você quer analisar?

Você pode usar qualquer combinação:
- Um número                  (ex: 3)
- Vários por vírgula         (ex: 1, 3, 5)
- Intervalo                  (ex: 1-5)
- Misto                      (ex: 1, 3-5, 8)
- A palavra `todas`          (seleciona todas as listadas)
```

**Regra de parsing:**
- Aceitar `\d+(\s*[,-]\s*\d+)*` ou a palavra-chave `todas` (sem diferenciar maiúscula e minúscula).
- Expandir intervalos antes de validar (ex: `1-3` vira `[1, 2, 3]`).
- Deduplicar e ordenar.
- Validar que todos os índices existem na listagem. Se houver inválido, recusar com mensagem clara e pedir a entrada de novo.

**Confirmação obrigatória antes de prosseguir:**

```
Você selecionou {N} campanhas:
1. {nome_campanha_1}
2. {nome_campanha_2}
...

[1] Confirmar e analisar
[2] Refazer seleção
```

Definir `ESCOPO_FILTRO` na sessão:
- Uma campanha selecionada: `ESCOPO_FILTRO = ids:{id1}`
- Múltiplas campanhas: `ESCOPO_FILTRO = ids:{id1,id2,...}`
- Filtro por texto (opção [2]): `ESCOPO_FILTRO = nome_contém:{texto}`
- Conta completa ou `todas` aplicado a todas as campanhas da sessão: `ESCOPO_FILTRO = conta_completa`

---

### Passo 0.7. Inputs específicos de otimização

Com conta e escopo definidos, montar os inputs que determinam as trilhas e thresholds do diagnóstico. Os dois primeiros vêm de leitura; os demais são perguntados, **uma pergunta por vez**.

**Item 1. Tipo de funil (inferido):** pelo `objective` das campanhas do escopo. `OUTCOME_SALES` otimizando por Compra vira perpétuo / venda direta; `OUTCOME_LEADS` (ou otimização por Lead) vira lançamento / captação. Só perguntar se o escopo misturar objetivos ou se o caso for ambíguo:
```
Qual é o tipo de funil desta campanha?

[1]  Perpétuo / venda direta   (otimização por Compra)
[2]  Lançamento / captação     (otimização por Lead)
```

**Item 2. Ticket do produto (lido do resumo):** o preço do `resumo-produto.md` vira `ticket_brl` e aparece na linha de confirmação. Só perguntar se o resumo não tiver preço ou se a campanha vender outro produto (ex.: outra oferta da mesma conta):
```
Qual é o valor do produto que essa campanha vende, em reais?
(ex: 97, 297, 997)
```

**Pergunta 1. Meta de CPA ou CPL (opcional):**
```
Você tem uma meta de CPA (perpétuo) ou CPL (lançamento) definida?

[1]  Sim  (você informa o valor em reais)
[2]  Não  (vou usar 50% do ticket como referência padrão)
```

Se o aluno informar o valor, salvar como `meta_cpa_cpl_declarada`. Se não, usar o default da trilha (50% do ticket).

**Pergunta 2. Margem de contribuição (para decidir por lucro, não só por CPA):**

Nunca perguntar "qual sua margem?" (ninguém sabe de cabeça e confunde com a margem líquida da empresa). Perguntar os **3 pedaços fáceis**, que o aluno sabe responder:
```
Pra eu calcular o lucro de verdade, me diz 3 custos da sua venda (pode ser aproximado):

1. Taxa da plataforma   (ex: Hotmart/Kiwify, ~1 a 10%)
2. Reembolso médio      (ex: 5%)
3. Imposto sobre o faturamento  (ex: 6 a 17%)
```
Calcular `margem_contribuicao = 1 - (taxa_plataforma + reembolso + imposto_faturamento)` e salvar. Exemplo: 1 - (1% + 5% + 17%) = 0,77.

- **Custos fixos (aluguel, salário, sala) NÃO entram aqui:** são pagos com ou sem a campanha; só servem para a "saúde da empresa" (opcional, ver §3.6).
- Se o aluno não souber nenhum dos três: usar **modo faixa** (60% a 80%) e avisar (ver §3.6).
- O imposto sobre o anúncio (Meta) é outra coisa e fica de fora por enquanto (ver §3.6).

**Pergunta 3. Sazonalidade ativa (opcional):** ver `sazonalidade_ativa` em §1.2 (nenhuma, Black Friday, data comemorativa, lançamento de concorrente relevante).

**Após os inputs:** confirmar em uma linha o que foi coletado e iniciar o diagnóstico:

```
Otimizando: {nome da campanha ou "conta completa"}
Conta: {nome da conta}  |  Funil: {tipo}  |  Ticket: R$ {valor} (do resumo do produto)  |  Meta CPA: R$ {cpa_cpl}
Margem de contribuição: {margem}%  |  ROAS de break-even: {1÷margem}
```
(O **CPA de break-even** = AOV × margem só é calculado depois de puxar o AOV no diagnóstico. Aqui mostra-se o ROAS de break-even, que já é conhecido pela margem.)

---

### Passo 0.8. Confiabilidade do dado (obrigatório antes de qualquer diagnóstico)

> Esta etapa nasceu de uma sessão real: a skill apresentou CPA, CTR e ROAS que não batiam com o Gerenciador, e o aluno perdeu a confiança no diagnóstico. **Antes de interpretar qualquer número, a skill valida a fonte e mostra a conferência ao aluno.** Sem este passo, nenhum diagnóstico é apresentado. Tudo aqui é leitura e não passa pelo gate.

A skill roda 4 checagens e imprime um bloco curto de confiabilidade:

**1. Janela de atribuição.** Ler `attribution_setting` da conta/campanha e usá-la em todas as métricas de conversão. **Se o campo for indisponível neste nível** (algumas contas recusam `attribution_setting` no nível de conta, visto em sessão real), usar o padrão omni da API e **declarar isso** no carimbo ("atribuição: padrão omni da API"). Carimbar a janela em todo número (ex: "7 dias clique / 1 dia visualização"). Nunca misturar janelas entre tabelas.

> **Cuidado de chamada (aprendido em sessão real):** `attribution_setting` **não existe no nível de conta** em algumas contas e, quando incluído num `fields` junto de outros campos, **derruba a chamada inteira** (`Tried accessing nonexisting field (attribution_setting)`), e você perde também o total da conta que vinha junto. Por isso: **nunca incluir `attribution_setting` numa chamada multi-campo de insights.** Pedir num teste isolado (ou simplesmente assumir o padrão omni e declarar). O resto dos campos não pode ser refém desse.

**2. Saúde do pixel.** Acionar `/trafego-pixel` (ou ler o dataset, no MCP pelas tools `ads_pixel_event_*`): último disparo, volume do evento-norte (Compra ou Lead) nos últimos 7 dias, taxa de deduplicação. Se o evento está com volume baixo ou sem disparo recente, **marcar o dado como não confiável** e avisar antes de diagnosticar.

> **Fallback quando a ferramenta de dataset não responde (aprendido em sessão real):** em algumas contas as tools de dataset/pixel ainda estão em liberação gradual (`ads_get_datasets` responde "gradually being rolled out"). Nesse caso **não travar**: inferir a saúde do pixel pelo **fluxo de compras atribuídas** que já vem nos insights (`actions:omni_purchase` aparecendo nas campanhas = evento Compra disparando) e **declarar** no carimbo ("pixel: registrando Compra, inferido pelo fluxo de vendas; stats de dataset indisponível nesta conta"). Volume absoluto baixo em high ticket é esperado e **não** é, sozinho, sinal de subnotificação.

**3. Conciliação com o total da conta.** Puxar o total da conta (gasto, compras/leads, ROAS) na **mesma janela e atribuição** e conferir que a **soma das campanhas bate com o total**, dentro de ±5%. Mostrar a conferência ao aluno:
```
Conferência (últimos 7 dias · 7d clique / 1d visualização):
  Gasto:   soma das campanhas R$ X   vs   total da conta R$ Y    ✓ bate (Δ 1,2%)
  Compras: soma 25                    vs   total da conta 26      ✓ bate
  ROAS da conta (Gerenciador): 1,87
```
Se não bater além da tolerância, **não diagnosticar**: avisar a divergência provável (janela errada, campanha fora do recorte, atribuição diferente) e propor ajuste.

> **Conciliação NÃO se aplica a recorte (aprendido em sessão real):** quando o escopo é um **subconjunto** da conta (algumas campanhas nomeadas de uma conta com muitas outras), a soma do recorte **nunca** vai fechar com o total da conta, e isso não é erro. Nesse caso: marcar `conciliacao_conta: nao_aplicavel` e **não bloquear o diagnóstico**. A validação de fonte passa a ser **consistência de janela + atribuição entre as campanhas do recorte** (todas na mesma janela, mesma atribuição, sem dupla contagem). Só exigir o "bate com o total" quando `escopo: conta_completa`.

**4. Descoberta de campos.** Antes de montar a consulta de insights, confirmar quais campos a conta expõe (ver §3.5). Nunca pedir um campo sem saber se existe; nunca cair em campo substituto sem avisar.

**Saída deste passo:** um bloco `confiabilidade_do_dado` (ver YAML §13) com `nivel: alta | media | baixa` e os motivos. Se `media` ou `baixa`, a skill diagnostica mesmo assim, mas **rebaixa CPA/CPL a secundário** e decide por ROAS + métricas leading, deixando o aviso explícito no topo da narrativa.

---

## 1. Inputs antes de qualquer análise

Com as respostas do aluno e as leituras em mãos, a skill mapeia os dados para os campos internos abaixo.

### 1.1 Estritamente obrigatórios (skill recusa rodar sem)
- `conta_anuncios_id`. ID ou nome da conta escolhida no Passo 0.5.
- `tipo_funil`. `perpetuo_venda_direta` ou `lancamento_captacao` (inferido do objetivo da campanha ou perguntado se ambíguo).
- `meta_cpa_cpl_declarada`. Valor em BRL. **Sempre perguntado** (Pergunta 1 do Passo 0.7); se o aluno não tiver meta, vale o default da trilha (50% do ticket), registrado como `default`.
- `campanhas_alvo`. Padrão de nomenclatura ou lista de campanhas indicada pelo aluno (ou modo `escopo: conta_completa`, ver 1.3).

### 1.2 Opcionais com default automático
| Input | Default quando ausente |
|---|---|
| `ticket_brl` | Lido do `resumo-produto.md`. Sem resumo ou sem preço: inferido como `meta_cpa_cpl_declarada ÷ 0,5` (perpétuo) quando a meta foi declarada. Em lançamento, usado apenas para classificar a trilha; se ausente, perguntar. |
| `fase_lancamento` | `captacao_inicial` (se lançamento) |
| `sazonalidade_ativa` | `nenhuma`. Outras opções: `black_friday`, `data_comemorativa`, `lancamento_competidor`. Ajusta tolerâncias de CPM e frequência. |
| `historico_da_conta_disponivel` | `false`. Se `true`, usa média histórica da conta como referência em vez dos benchmarks fixos. |

### 1.3 Escopo
- `escopo: campanha_unica`. Uma campanha selecionada após o filtro de nomenclatura.
- `escopo: campanhas_multiplas` (default quando o aluno escolhe 2+ na seleção múltipla). Analisa o conjunto selecionado e devolve diagnóstico campanha por campanha.
- `escopo: conta_completa`. Varre todas as campanhas ativas, ranqueia por urgência (CPA/CPL pior primeiro, gasto maior primeiro), e devolve top 3 a 5 ações priorizadas da conta inteira.

---

## 2. Classificação da campanha em uma das 6 trilhas

Toda análise começa classificando em uma trilha. Cada trilha tem janelas, métricas e thresholds próprios.

### 2.1 Perpétuo. Venda direta (otimização por evento de Compra)

| Trilha | Faixa de ticket | Janelas | CPA saudável (default) | CPA máximo tolerável |
|---|---|---|---|---|
| `perpetuo_low` | até R$ 500 (ideal ≤ R$ 397) | **1d / 3d / 7d** | 50% do ticket | 60% do ticket |
| `perpetuo_mid` | R$ 501 a R$ 1.499 | **3d / 7d / 14d** | 50% do ticket | 55% do ticket |
| `perpetuo_high` | R$ 1.500+ | **7d / 14d / 30d** | 50% do ticket | 55% do ticket |

**Regra dura:** CPA saudável = **50% do ticket, sempre**. A skill só relaxa se o aluno declarar manualmente uma `meta_cpa_cpl_declarada` diferente.

### 2.2 Lançamento. Captação de leads (otimização por evento de Lead)

| Trilha | Produto-alvo | Janelas | CPL saudável (referência) |
|---|---|---|---|
| `lancamento_low` | Produto final ≤ R$ 500 | **1d / 3d** | R$ 3 a R$ 12 |
| `lancamento_mid` | Produto final R$ 500 a R$ 1.499 | **1d / 3d** | R$ 8 a R$ 20 |
| `lancamento_high` | Produto final ≥ R$ 1.500 | **1d / 3d** | R$ 15 a R$ 40 |

CPL é a métrica-norte única em lançamento. Tracking de qualidade de lead, taxa de confirmação e show-up estão fora do escopo.

---

## 3. Métricas monitoradas

### 3.1 Métrica-norte (decide a ação principal)
- **Perpétuo:** `CPA` (custo por compra).
- **Lançamento:** `CPL` (custo por lead).

ROAS **não é métrica primária por padrão** no perpétuo, porque depende de pixel/CAPI com valor configurado corretamente. Entra como **confirmação secundária**, nunca como gatilho, **exceto** nos dois casos abaixo, em que vira a métrica de decisão:

- **Amostra pequena de conversão** (campanha com menos de 10 compras na janela de decisão). Aí o CPA é estatisticamente frágil (1 ou 2 vendas mexem o número inteiro) e **a skill decide por ROAS + leading**, marcando o CPA como "não confiável, amostra pequena". Ver §3.4.
- **Confiabilidade do dado `baixa`** (pixel subnotificando, conciliação não bate, ver Passo 0.8). Aí o CPA da API não representa a realidade do Gerenciador e a skill o rebaixa.

**Contradição CPA × ROAS:** quando o ROAS é maior que 1 mas o CPA está acima do teto, isso quase sempre é sinal de **AOV maior que o ticket declarado (order bump/upsell) ou subnotificação de compras**. Investigar via §3.4 **antes** de propor qualquer pausa. Nunca pausar criativo com ROAS maior que 1 só porque o CPA bruto passou do teto.

### 3.2 Métricas leading (antecipam queda da métrica-norte)

| Métrica | Saudável | Atenção | Crítico |
|---|---|---|---|
| CTR único no link Feed/Reels | ≥ 1,2% | 0,8 a 1,2% | < 0,8% |
| Hook rate (vídeo 3s) | ≥ 25% | 18 a 25% | < 18% |
| Frequência (7d) | 1,0 a 2,5 | 2,5 a 3,5 | > 3,5 |
| CPM | ±20% da média histórica da conta | +20 a 40% | > +40% |

> **Nota sobre o CTR de link (campo certo, com plano B):** a métrica é o **CTR no link**, NUNCA o `ctr` geral, que conta toda interação (curtida, comentário, expandir, salvar) e infla o número para 2 a 4 vezes o real. Ordem de preferência de campo, conforme o que a conta expõe (confirmar antes, ver §3.5):
> 1. `unique_inline_link_click_ctr` (CTR único no link, preferido).
> 2. `inline_link_click_ctr` (CTR no link, todos os cliques).
> 3. **Cálculo manual:** `cliques no link ÷ impressões` (`actions:link_click ÷ impressions`), **declarando que foi calculado assim**.
>
> **A tool `ads_get_ad_entities` (MCP) NÃO expõe os campos 1 e 2 (aprendido em sessão real):** pedir `inline_link_click_ctr` ou `unique_inline_link_click_ctr` ali volta `Unsupported field(s)`. Nessa tool, ir **direto ao cálculo manual** (item 3): `actions:link_click ÷ impressions`. Os campos 1 e 2 valem para o caminho APP (curl na Graph API), onde existem. Ver o mapa de campos reais em §3.5.1.
>
> Se a conta só expõe o `ctr` geral, **não usar como CTR de link**: reportar "CTR de link indisponível" em vez de inflar. O CTR único costuma ficar 20 a 30% abaixo do CTR no link total; os thresholds acima são aproximação inicial, calibrar pela média histórica da conta quando houver.
>
> **Erro real a não repetir:** a skill mostrou "CTR de 13 a 20%" usando o `ctr` geral e tratou como engajamento de link. O CTR de link real das mesmas campanhas era 1 a 5%. Trocar o campo silenciosamente destrói a confiança no diagnóstico inteiro.

Quando uma leading entra em zona crítica e a métrica-norte ainda está saudável, a skill **não pausa**. Sinaliza risco e prepara plano de refresh criativo.

### 3.3 Métricas derivadas (calculadas a partir de dados nativos)

Esta camada é o que diferencia diagnóstico raso de diagnóstico sênior. Todas calculadas a partir de eventos que o pixel padrão entrega. Sem tracking adicional. Lidas via `/trafego-insights`.

> **Nível certo de consulta (aprendido em sessão real):** os eventos de funil (`landing_page_view`, `add_to_cart`, `initiate_checkout`, `purchase` + valor) **não aparecem na consulta crua em nível de campanha** com um conjunto enxuto de campos. Para calcular as derivadas, puxar os insights com as **ações de funil explícitas** (e, quando preciso, no nível de conta ou conjunto). **Se o evento não vier, marcar a métrica como `indisponível neste nível`, nunca inventar nem assumir zero.** Connect rate de "0%" por falta do evento é diferente de connect rate real de 0%.

> **A tool `ads_get_ad_entities` (MCP) NÃO oferece os eventos de funil (aprendido em sessão real):** seu catálogo de ações é limitado (essencialmente `actions:omni_purchase`, `actions:link_click`, `actions:page_engagement`, `actions:comment`, `actions:like`, `actions:post_reaction`, `actions:post_save`). **Não há `landing_page_view`, `add_to_cart` nem `initiate_checkout`.** Logo, no caminho MCP, as derivadas de funil (connect rate, conversão da página, carrinho para compra, checkout para compra) ficam **`indisponível neste nível`**: declarar e decidir por métrica-norte (CPA/ROAS) + leading (CTR de link calculado, frequência). Os eventos completos de funil só vêm pelo caminho APP (curl na Graph API com `actions`/`action_values` e as ações de funil explícitas) ou via `/trafego-insights`. Nunca pedir `actions`/`action_values` "crus" na tool do MCP (volta `Unsupported field(s)`).

| Métrica derivada | Fórmula | Diagnostica | Saudável | Atenção | Crítico |
|---|---|---|---|---|---|
| **Connect rate** | LP Views ÷ Cliques no link | Saúde técnica (link, redirect, velocidade) | ≥ 80% | 60 a 80% | < 60% |
| **Conversão da página (perpétuo)** | Compras ÷ LP Views | Página de vendas + oferta | ≥ 1,5% (low/mid), ≥ 0,8% (high) | metade do saudável | < metade |
| **Conversão da página (lançamento)** | Leads ÷ LP Views | Landing de captação | ≥ 25% | 15 a 25% | < 15% |
| **Conversão do anúncio** | Compras (ou Leads) ÷ Cliques | Combinação criativo + página | depende da trilha | depende | depende |
| **Carrinho → Compra** (perpétuo) | Compras ÷ AddToCart | Atrito do checkout | ≥ 30% | 15 a 30% | < 15% |
| **Checkout → Compra** (perpétuo) | Compras ÷ InitiateCheckout | Atrito final (pagamento, frete) | ≥ 50% | 30 a 50% | < 30% |
| **Custo por etapa** | Gasto ÷ (PV, ATC, IC, Purchase) | Onde o custo escala desproporcionalmente | analisado em razão | n/a | n/a |

**Benchmarks vs histórico:** se houver histórico ≥ 14 dias da própria conta, prioriza a média histórica como referência. Os benchmarks fixos acima só servem para contas novas.

### 3.4 Valor médio por venda (AOV) e guarda de amostra pequena

Duas verificações que resolvem a contradição clássica "CPA horrível, mas ROAS bom".

**AOV (ticket real entregue).** Calcular `valor de compra ÷ compras` (via `action_values:omni_purchase ÷ actions:omni_purchase`, ou `ROAS × gasto ÷ compras`). Comparar com o `ticket_brl` (do resumo do produto ou declarado):
- Se o AOV calculado é **muito maior que o ticket** (order bump / upsell / múltiplos produtos), a régua de CPA baseada só no ticket está errada. A skill **avisa e sugere recalcular o CPA alvo sobre o AOV real**, ou decidir por ROAS.
- Se o AOV é **coerente com o ticket** mas o CPA está alto com ROAS maior que 1, suspeitar de **subnotificação de compras** (ver Passo 0.8).

**Guarda de amostra pequena.** Toda campanha/conjunto com **menos de 10 compras** (perpétuo) ou **menos de 50 leads** (lançamento) na janela de decisão recebe a marca `cpa_confiavel: false`. Para esses:
- **Não pausar nem reduzir por CPA isolado.** 1 ou 2 conversões a mais ou a menos mudam o CPA inteiro.
- Decidir por **ROAS + métricas leading** (CTR de link, hook rate, frequência) e pela tendência cruzando janelas.
- Deixar explícito na narrativa: "CPA de R$ X sobre só N vendas: amostra pequena, não confiável isoladamente."

### 3.5 Descoberta de campos e proveniência (carimbo obrigatório)

Antes de montar qualquer consulta de insights:
1. **Descobrir os campos** que a conta expõe (contexto de campo / uma chamada de teste). Não pedir campo às cegas. Se a API recusar um campo, ela costuma devolver a lista de campos suportados: usar essa lista.
2. Se o campo preferido não existe, **descer na ordem de preferência** documentada (ex: CTR de link em §3.2) e **registrar qual campo foi usado**.
3. **Carimbo de proveniência:** toda métrica apresentada carrega, ao menos no YAML técnico, a origem (`fonte: <campo da API | cálculo manual>`) e a `janela` + `atribuição`. Na narrativa, declarar quando um número foi **calculado** em vez de lido direto.

Nunca substituir um campo por outro silenciosamente (foi exatamente o erro que trocou CTR de link por CTR geral numa sessão real).

#### 3.5.1 Mapa de campos reais por caminho (evita chamada que quebra)

> **Por que existe (sessão real):** a skill pedia campos com nome de Graph API (`actions`, `action_values`, `inline_link_click_ctr`) que a tool `ads_get_ad_entities` **rejeita**, e duas chamadas falharam antes de acertar. Esta tabela é o contrato dos campos que **existem de fato** na tool do MCP. Para o caminho APP (curl), valem os nomes clássicos da Graph API.

**O que pedir na tool `ads_get_ad_entities` (MCP):**

| Quero | Campo certo na tool MCP | Observação |
|---|---|---|
| Gasto | `spend` (volta como `amount_spent`) | ok |
| Impressões / alcance / frequência | `impressions`, `reach`, `frequency` | ok |
| Compras (qtde) | `actions:omni_purchase` | **não** existe `purchases` |
| Custo por compra (CPA) | `cost_per_action_type`, lendo `cost_per_action_type:omni_purchase` | CPA pronto, sem dividir à mão |
| ROAS | `purchase_roas` | ok |
| Cliques no link | `actions:link_click` | base do CTR de link calculado |
| CPM / CPC | `cpm`, `cpc` | ok |
| Leads (qtde) | `lead` ou `actions:lead` | lançamento |
| CTR de link | **calcular** `actions:link_click ÷ impressions` | `inline_link_click_ctr` NÃO existe aqui |
| Valor de compra (p/ AOV) | **derivar** `purchase_roas × spend` | `action_values` NÃO existe aqui; AOV = `(purchase_roas × spend) ÷ compras` |
| Tipo de orçamento | `daily_budget` / `lifetime_budget` na campanha e no adset | ABO vs CBO (§6.0) |

**Proibido na tool MCP** (volta `Unsupported field(s)` e derruba a chamada): `actions`, `action_values`, `inline_link_clicks`, `inline_link_click_ctr`, `unique_inline_link_click_ctr`, `landing_page_view`, `add_to_cart`, `initiate_checkout`, `attribution_setting` em chamada multi-campo de conta.

**Caminho APP (curl na Graph API):** aí valem os nomes clássicos: `actions`, `action_values`, `inline_link_click_ctr`, `unique_inline_link_click_ctr` e as ações de funil. Usar `curl -g` quando o `fields` tiver nesting (ver regra global no CLAUDE.md).

**Disciplina:** numa primeira chamada, se não tiver certeza do que a conta expõe, mandar um conjunto pequeno e **deixar a própria tool devolver a lista de campos suportados** no erro de validação, e então montar a consulta real com os nomes acima. Nunca insistir no campo recusado.

### 3.6 Camada de lucro (decidir por dinheiro, não por métrica)

> O CPA sozinho não diz se você ganha dinheiro: é uma régua arbitrária (50% do ticket). Esta camada traduz tudo em **lucro em reais** e usa o CPA como guardrail, não como juiz. Liga só quando a confiabilidade do dado é média/alta (Passo 0.8); senão, o lucro herda a incerteza e é apresentado como faixa.

**Insumo: margem de contribuição** (coletada na Pergunta 2 do Passo 0.7):

```
margem_contribuicao = 1 - (taxa_plataforma + reembolso_medio + imposto_sobre_faturamento)
```

Exemplo: 1 - (1% + 5% + 17%) = **0,77**. Custos fixos (aluguel, salário, sala) **não entram**: são pagos com ou sem a campanha, então não pesam na decisão marginal de manter/cortar.

**Fórmulas:**

| Métrica | Fórmula | Exemplo (margem 0,77) |
|---|---|---|
| ROAS de break-even | `1 ÷ margem` | 1 ÷ 0,77 = **1,30** |
| CPA de break-even | `AOV × margem` | R$ 2.701 × 0,77 = **R$ 2.080** |
| Lucro por venda | `AOV × margem - CPA` | n/a |
| **Lucro por dia** | `gasto_dia × (ROAS × margem - 1)` | n/a |
| Lucro na janela | `gasto × (ROAS × margem - 1)` | recorte: ~R$ 35 mil/30d |

`ROAS × margem - 1 > 0` é, por construção, "ROAS acima do break-even". Decisão e dinheiro viram a mesma conta.

**Três zonas de CPA (leitura de duas lentes):**

```
   CPA meta              CPA de break-even
   (50% do ticket)       (AOV × margem)
      │                       │
──────┼───────────────────────┼──────────▶ CPA crescente
  VERDE                 AMARELA          VERMELHA
  abaixo da meta:       acima da meta    acima do break-even:
  proteger / escalar    mas ainda lucra: lucro/dia negativo:
                        manter, otimizar  conter de verdade
```

A zona **amarela** é a novidade: campanha acima da meta de CPA que **ainda dá lucro**. A skill **não contém** zona amarela, só otimiza. Contenção (§6) e pausa por dinheiro (§7) valem só na **zona vermelha** (lucro/dia negativo sustentado).

**Duas visões, nunca misturadas:**
- **Decisão de campanha:** margem de contribuição (sem custo fixo). Decide escalar/manter/conter.
- **Saúde da empresa** (opcional): aloca `custo_fixo_mensal ÷ vendas_mes` por venda e bate com a margem líquida que o dono conhece (ex: 25 a 30%). É contexto, nunca gatilho de campanha.

**Margem desconhecida, modo faixa:** rodar de 60% a 80% e apresentar lucro como intervalo, com a premissa carimbada. Para a maioria das campanhas (longe do break-even) o veredito não muda na faixa, só o tamanho do lucro. Marcar como "veredito depende da margem" apenas as campanhas de **borda** (ROAS perto do break-even).

**Honestidade obrigatória:**
- Todo valor de lucro carrega a premissa na tela: "lucro estimado, margem 77%".
- Lucro de contribuição é diferente de lucro líquido da empresa (esse desconta o fixo).
- Se o lucro de contribuição do recorte ficar **abaixo** da margem líquida declarada da empresa, sinalizar a inconsistência (provável receita sem custo de anúncio: orgânico, lista, recorrência).

---

## 4. Tratamento de dados imaturos

Antes de qualquer diagnóstico, verificar maturação. Quando o dado ainda é imaturo, a skill emite `aguardar` em vez de ação.

**Casos de dado imaturo:**
- Campanha viva há menos que a janela mínima da trilha:
  - `perpetuo_low`: < 3 dias
  - `perpetuo_mid`: < 7 dias
  - `perpetuo_high`: < 14 dias
  - `lancamento_*`: < 1 dia (lançamento mata cedo)
- Conjunto com gasto acumulado < 1× CPA target (perpétuo) ou < 5× CPL target (lançamento)
- Anúncio com < 1.000 impressões
- Gasto do dia atual < 50% do orçamento diário (dia ainda em curso)
- Última edição há < 48h (aprendizado não consolidou). No MCP, `ads_account_get_activity_logs` confirma a data da última alteração.

Se **todos** os ativos analisados estiverem imaturos, output é `acao: aguardar` com horário sugerido de reanálise. Sem proposta de mudança.

---

## 5. Diagnóstico em duas camadas

A skill **sempre** roda os dois antes de propor ação.

### 5.1 Diagnóstico de tendência (cruzando as 3 janelas)

| Padrão | Diagnóstico | Postura base |
|---|---|---|
| Métrica-norte saudável nas 3 janelas | `estavel_performando` | Avaliar prontidão para escala |
| Saudável em janelas longas, ruim na curta | `esfriando_ou_ruido` | Aguardar 24 a 48h |
| Ruim em janelas longas, saudável na curta | `recuperando` | Manter, observar |
| Ruim nas 3 janelas | `ruim_estrutural` | Ir para diagnóstico de gargalo |
| Degradando progressivamente | `saturacao` | Refresh criativo / nova audiência |
| Volume caiu sem métrica-norte piorar | `entrega_limitada` | Verificar concorrência, leilão, frequência |

### 5.2 Diagnóstico de gargalo (onde está o problema?)

A skill sobe pela cadeia de causa, da entrega até a conversão final, usando as métricas derivadas:

```
Métrica-norte (CPA/CPL) acima do target?
│
├─ 1. CTR único no link baixo (< saudável)?
│     → CRIATIVO não atrai cliques únicos
│     → Ação: pausar/refresh criativo  [DENTRO DO META]
│
├─ 2. CTR único no link ok, mas Connect Rate < 70%?
│     → TÉCNICO (link errado, página fora, redirect quebrado, velocidade)
│     → Ação: ALERTAR aluno. NÃO pausar nem reduzir orçamento.  [FORA DO META]
│
├─ 3. Connect Rate ok, mas Conversão da Página crítica?
│     → PÁGINA / OFERTA (copy, preço, prova, headline)
│     → Ação: ALERTAR aluno. NÃO pausar criativo bom.
│         Se gasto continuar improdutivo, reduzir -20% como contenção.  [FORA DO META]
│
├─ 4. Conversão da página ok, mas Carrinho → Compra < 15% (perpétuo)?
│     → CHECKOUT (atrito, pagamento, frete, confiança)
│     → Ação: ALERTAR aluno. Mesma lógica do item 3.  [FORA DO META]
│
├─ 5. Todas as taxas ok, mas CPM > 40% acima do histórico?
│     → LEILÃO / AUDIÊNCIA (sazonalidade, concorrência, saturação)
│     → Ação: refresh de audiência ou reduzir -20% temporariamente.  [DENTRO DO META]
│
└─ 6. Tudo ok, CPM ok, mas Frequência > 3,5?
      → SATURAÇÃO da audiência atual
      → Ação: refresh criativo (novo ângulo) ou expandir audiência.  [DENTRO DO META]
```

**Regra crítica. Gargalo fora do Meta:** itens 2, 3 e 4 acima identificam problemas que **não estão na campanha**. Pausar nesses casos destrói aprendizado sem resolver o problema. A skill alerta, identifica a etapa quebrada e, se o gasto continuar improdutivo, aplica contenção via redução de -20%. Mas mantém a estrutura viva para quando o problema externo for resolvido.

**Encaminhamento do gargalo fora do Meta (diagnóstico antes da correção):**

1. **Diagnóstico:** `/trafego-oferta-funil` lê a página real, compara com o anúncio e aponta onde a oferta falha.
2. **Correção, conforme o que o diagnóstico apontar:**
   - **Página de vendas** (copy, estrutura, prova, headline): `/feedback-pagina` (página 8D) ou `/feedback-low-ticket` (página low ticket). Ajuste pontual em `/pagina-ajuste`; reescrever a copy em `/copy-pagina` ou `/lt-pagina`.
   - **Checkout** (atrito, meio de pagamento, link quebrado): `/pagina-checkout`.
   - **Técnico** (velocidade, redirect, página fora do ar): `/pagina-performance`.
   - **Pixel sem disparar na página:** `/pagina-pixel` (instalação) e `/trafego-pixel` (diagnóstico do evento).

Se o aluno preferir não rodar o diagnóstico, ir direto para a skill de correção da etapa identificada.

---

## 6. Regras de decisão. Orçamento defensivo (sem aumentar o gasto total)

> Toda lógica de **subir o gasto total e escalar** vive em `/trafego-escalar`. Esta skill mexe em orçamento só de forma **neutra ou pra baixo**: reduzir (§6.1), **realocar do queimador pro vencedor sem mexer no total (§6.3)** e **pôr piso/teto por conjunto em CBO (§6.4)**, ou **emite sinal de prontidão** para a escalar agir. Nunca aumenta o gasto total da conta.

### 6.0 Detecção obrigatória de ABO vs CBO antes de qualquer mudança de orçamento

Antes de sugerir ou executar **qualquer** redução de orçamento, a skill **lê obrigatoriamente** o campo `budget.tipo` da campanha vindo de `/trafego-insights`:

| `budget.tipo` | Onde aplicar a redução | Tool call correta |
|---|---|---|
| `ABO` (orçamento por conjunto) | No conjunto vencedor afetado | `update_adset_budget` com `adset_id` específico |
| `CBO` (orçamento por campanha) | Na campanha inteira | `update_campaign_budget` com `campaign_id` |

**Por que importa:** chamar `update_adset_budget` numa campanha CBO falha (o adset não tem `daily_budget` próprio em CBO). Chamar `update_campaign_budget` numa campanha ABO afeta a campanha inteira em vez do conjunto específico que precisava da contenção.

**Política dura:**
- Se `budget.tipo` voltar `null` ou indisponível, **não sugerir redução**: marcar `acao: aguardar` com motivo "tipo de orçamento não detectado, repuxar dados".
- Se a campanha é `CBO` e o gargalo está localizado em **um conjunto específico**, a skill **não reduz a campanha inteira** automaticamente. Oferece, em ordem de preferência: **(a) pôr teto no conjunto queimador (§6.4, não pausa, não reseta)**, (b) realocar pro vencedor (§6.3), ou (c) pausar só o conjunto problemático, sempre mantendo o orçamento total intocado. E aguarda decisão.
- Em ABO, redução de -20% é aplicada diretamente no conjunto identificado.

**No output YAML**, sempre incluir o tipo no bloco da campanha:

```yaml
budget:
  tipo: ABO | CBO | null
  nivel_aplicacao: adset | campaign | indeterminado
  valor_atual_brl: ...
```

E em cada `acao_recomendada` que mexe em orçamento, o `tool_call.name` precisa bater com o tipo: `update_adset_budget` se ABO, `update_campaign_budget` se CBO.

### 6.1 Quando reduzir orçamento (-20%)
Qualquer das condições:
- CPA/CPL na janela média ≥ 1,3× target, mas < 1,7× (ainda recuperável)
- Frequência > 3 com métrica-norte piorando
- Concorrência sazonal alta (CPM subiu > 30%). Redução temporária
- Gargalo identificado fora do Meta + gasto continuando improdutivo

**Ação:** reduzir -20%. Nunca mais que isso de uma vez. Aguardar 48h antes de nova decisão.

> **Filtro de lucro obrigatório (§3.6):** antes de reduzir por CPA, checar a **zona**. Se a campanha está na **zona amarela** (CPA acima da meta mas lucro/dia ainda positivo), **não reduzir**: otimizar criativo. Reduzir/conter por dinheiro só vale na **zona vermelha** (lucro/dia negativo sustentado, ou seja, ROAS abaixo do break-even). O gatilho real é lucro/dia negativo, não CPA acima da meta.

### 6.2 Bloqueios à mudança de orçamento
A skill não muda orçamento se:
- Conjunto está em **fase de aprendizado ativa** (a menos que esteja queimando muito acima do CPA máximo. Aí pausa, não reduz)
- Última edição há < 48h
- Gasto acumulado do dia < 50% do orçamento diário

### 6.3 Realocação neutra de orçamento (mover do queimador pro vencedor)

> Otimização, não escala: o **gasto total da conta não muda**, só é redistribuído. Em vez de só cortar -20% de quem queima, a skill **move esse valor pro vencedor**, no mesmo gesto.

**Dispara quando** há (a) ao menos uma campanha em contenção (zona vermelha / lucro-dia negativo, §3.6) **e** (b) ao menos um vencedor com folga (zona verde, fora de aprendizado, frequência saudável, última edição ≥ 48h).

**Pergunta ao aluno** (no lugar do corte seco):
```
A campanha "A" está queimando. O que fazer com os R$ {corte}/dia que vou tirar dela?

[1]  Redirecionar pro vencedor "B" (+R$ {lucro_b}/dia), gasto total intocado  (recomendado)
[2]  Devolver pra conta (reduz o gasto total)
```

**Cálculo, com trava dos dois lados:**
- `corte = 20% × orçamento(queimador)`
- `recipiente` = melhor vencedor com folga (maior lucro/dia, de preferência mesmo funil)
- `mover = min(corte, 20% × orçamento(recipiente))`: **teto de 20% também no recipiente**, pra não resetar o aprendizado dele
- Se `corte > mover`: o excedente vai pro 2º melhor vencedor, ou volta pra conta (e a skill avisa).

**Respeita ABO/CBO (§6.0):** em CBO os dois lados na campanha; em ABO no conjunto. **Nunca aumenta o gasto total**: se não houver vencedor com folga, vira redução simples (§6.1).

**Gate 🛡️** (formato do CLAUDE.md): mostrar os dois lados (reduzir A / aumentar B) num bloco só, marcar "reset: não (ambos ≤ 20%)" e "gasto total intocado". Um "sim" cobre o par. Executa **reduzindo primeiro, depois aumentando**, uma chamada `update_*_budget` por lado. Se a redução falhar, não aumentar.

**No YAML:** ação `realocar_neutro` com `de_objeto_id`, `para_objeto_id`, `valor_movido_brl`.

### 6.4 Limites de gasto por conjunto (CBO)

> Em CBO, em vez de pausar o conjunto ruim, **algema o gasto dele** (teto) e/ou **garante um piso** pro vencedor, sem tocar no orçamento da campanha e **sem pausar**. Aprendizado intacto, gasto total intocado.

**Campos da API:** `daily_spend_cap` (teto) e `daily_min_spend_target` (piso), no **conjunto**, em **centavos**.

**Pré-requisito de dado:** exige descer ao **nível de conjunto** (qual adset do CBO ganha/queima). Se o diagnóstico parou na campanha, puxar um insight a mais (adsets da campanha) antes de propor. É leitura, não passa pelo gate.

**Dispara quando:** campanha **CBO com 2+ conjuntos** e distribuição torta (um lucra, outro queima). Em ABO ou CBO de conjunto único, não se aplica: usar realocação (§6.3) ou pausa (§7).

**Pergunta:**
```
Na campanha "X" (CBO), o conjunto "V" lucra e o "Q" queima. Sem mexer no orçamento da campanha:

[1]  Garantir piso de R$ {piso}/dia no vencedor "V"
[2]  Pôr teto de R$ {teto}/dia no queimador "Q"
[3]  Os dois
```

**Cálculo:**
- Piso (vencedor) = gasto diário atual dele (ou um pouco acima).
- Teto (queimador) = ~20% abaixo do gasto diário atual dele (algema gradual).
- **Sanity-check obrigatório:** soma dos pisos ≤ orçamento da campanha; teto ≥ mínimo diário da conta (`min_daily_budget`). Se reprovar, ajustar valores e reavisar.

**Gate 🛡️:** listar campanha (CBO + orçamento), conjunto vencedor (piso) e/ou queimador (teto), marcar "reset: não" e "orçamento da campanha intocado". **Reverter = zerar os campos.**

**Execução:** `ads_update_entity` no conjunto (MCP) ou POST `/<adset_id>` (APP) com `{daily_min_spend_target}` e/ou `{daily_spend_cap}` em centavos.

**No YAML:** ação `limitar_conjunto` com `objeto_id` (adset), `daily_min_spend_target` e/ou `daily_spend_cap`.

### 6.5 Apertar controle de custo (cost cap / bid cap)

> Defende o CPA **pelo leilão**, sem reduzir orçamento: a entrega continua, mas a Meta não paga acima do teto. Alternativa à redução quando você quer **manter volume** e só segurar o custo.

**Estratégias (campo `bid_strategy`):**
- `COST_CAP`: teto de **custo por resultado** (requer `bid_amount`). É o mais usado aqui.
- `LOWEST_COST_WITH_BID_CAP`: teto de **lance** (requer `bid_amount`).
- `LOWEST_COST_WITHOUT_CAP`: autobid (o padrão; é pra onde se reverte).

**Dispara quando:** campanha lucrativa com CPA subindo ou perto do break-even, onde reduzir verba perderia volume.

**Cálculo do teto:**
- Cost cap inicial = **CPA de break-even** (§3.6) ou a meta declarada, o que for menor. **Nunca abaixo do CPA atual de quem performa** (sufoca a entrega).
- Aperto gradual: se já há cap, baixar no máximo ~15% por vez.

**Roteamento CBO obrigatório (verificado na API):** lance no conjunto é **rejeitado** sob CBO ("Must Use Campaign Bid Strategy"). Em CBO, `bid_strategy` vai na **campanha**. O `bid_amount` tem nuance de posição em CBO, então **ler a config atual e confirmar o roteamento antes de gravar** (mesma disciplina da §6.0). Não assumir.

**Reset: SIM.** Mudar estratégia de lance reseta aprendizado. Dispara o disclaimer da §11 (custo de reaprendizado ≈ 50 × CPA target) e exige **confirmação reforçada**.

**Gate 🛡️:** "definir cost cap de R$ {x} na campanha {y}", marcar "reset: SIM, reaprendizado ≈ R$ {z}", reversível (volta pra `LOWEST_COST_WITHOUT_CAP`).

**Execução:** `ads_update_entity` (campanha, `bid_strategy` + `bid_amount` em centavos) no MCP / POST equivalente no APP.

**No YAML:** ação `definir_cost_cap` (objeto_id campanha, `bid_strategy`, `bid_amount` centavos).

---

## 7. Regras de decisão. Pausar

> **Filtro de lucro (§3.6):** pausa por **dinheiro** (CPA/conversão ruins) só vale na **zona vermelha** (lucro/dia negativo). Campanha em zona amarela (acima da meta de CPA mas ainda lucrativa) não se pausa por custo: se otimiza. As pausas por **criativo/saturação/saúde** abaixo continuam valendo independentemente da zona, porque tratam de causa, não de custo.

### 7.1 Pausar **anúncio** (criativo)
**Pré-condição obrigatória:** o diagnóstico de gargalo (5.2) apontou `criativo` ou `saturacao` como causa. Se o gargalo é página, checkout ou técnico, **não pausar**. Pode estar pausando criativo bom.

**Sugestão antes de pausar:** "Quer investigar onde exatamente o criativo quebra com `/trafego-criativos` antes de pausar? Ele mostra se o problema é no gancho, na narrativa, na intenção ou na conversão." Se o aluno recusar, seguir com pausa.

Qualquer das condições, após gasto mínimo:
- Gasto ≥ 1,5× o CPA/CPL target sem nenhuma conversão **e** CTR abaixo do saudável
- CTR < 0,5% após R$ 50 de gasto (low) ou R$ 150 (high)
- Hook rate < 15% com gasto ≥ R$ 80
- Frequência ≥ 4 e métrica-norte acima do target
- Conversão do anúncio entre os piores 20% da conta nos últimos 14 dias

Antes de pausar o **último criativo** de um conjunto, alertar o aluno e sugerir preparar o substituto primeiro: copy do anúncio em `/copy-anuncio` (ângulo novo da Mandala em `/mandala-de-anuncios`), imagem em `/criativo-estatico`, vídeo em `/video-heygen`, `/video-remotion` ou `/video-editar`. Com o criativo pronto, subir como A/B contra o atual pelo `/trafego-testes`.

### 7.2 Pausar **conjunto**
Qualquer:
- CPA/CPL na janela longa ≥ 1,7× target **e** janela média confirma
- Todos os anúncios do conjunto pausados ou em zona crítica
- Audiência saturada: frequência > 4 sem queda do CPA após refresh criativo
- Aprendizado limitado por > 7 dias seguidos sem entregar 50 conversões

### 7.3 Pausar **campanha inteira** (caso extremo)
- ≥ 70% dos conjuntos pausados ou inviáveis
- CPA/CPL ≥ 2× target em todas as 3 janelas
- Problema estrutural (página fora, oferta sem conversão, pixel quebrado)

**Nunca** pausar campanha inteira sem antes verificar: pixel funcionando, página online, checkout testado.

### 7.4 Cortar posicionamento improdutivo

> Desliga um posicionamento que **queima sem converter** (clássico: Audience Network; às vezes Stories/Reels num público que só compra no Feed). Refina a entrega sem matar a campanha.

**Pré-requisito de dado:** exige o breakdown por **posicionamento** (`publisher_platform` / `platform_position`), a nível de conjunto, provando que aquele placement **gasta e não converte**. Só propor corte com o número na mão.

**Dois caminhos (do mais leve pro mais pesado):**
1. **Soft opt-out** (`placement_soft_opt_out`): exclui o posicionamento sem trava dura. **Menor impacto de aprendizado.** Tentar este primeiro.
2. **Placement manual** (editar `targeting`: `publisher_platforms`, `*_positions`): trava dura, mas exige **desligar o Advantage+ placements** e mexer no objeto `targeting` aninhado.

**Disciplina obrigatória no caminho manual:** **ler o `targeting` atual, modificar só o placement e regravar o objeto completo.** Nunca mandar um `targeting` parcial (apaga o resto). Validar a estrutura antes de gravar.

**Reset: SIM.** Mexe em segmentação/entrega. Disclaimer da §11 + confirmação reforçada.

**Gate 🛡️:** "remover {posicionamento} do conjunto {y} (gastou R$ {x}, 0 conversão)", dizer qual caminho (soft/manual), marcar "reset: SIM" e reversível.

**Execução:** `ads_update_entity` (adset, `placement_soft_opt_out` ou `targeting`) no MCP / POST equivalente no APP.

**No YAML:** ação `cortar_posicionamento` (objeto_id adset, `metodo: soft_opt_out | manual`, `posicionamento`).

---

## 8. Lógica específica. Perpétuo

> **Premissa:** todas as campanhas de perpétuo são otimizadas pelo evento `Purchase`. Funil de 2 etapas (lead para venda) está fora do escopo desta skill na versão atual.

### 8.1 Low ticket (até R$ 500). Janelas 1d / 3d / 7d
- Decisões mais rápidas. Dado matura por volume.
- Watchlist após R$ 100 de gasto sem venda em um anúncio.
- Refresh criativo a cada 10 a 14 dias.

### 8.2 Mid ticket (R$ 501 a 1.499). Janelas 3d / 7d / 14d
- Tolerar mais tempo antes de pausar. Decisão de compra mais lenta.
- **Não decidir só com 1d.** Sempre confirmar com 3d.
- Watchlist após R$ 250 de gasto sem venda.
- Refresh criativo a cada 14 a 21 dias.

### 8.3 High ticket (R$ 1.500+). Janelas 7d / 14d / 30d
- Janela de 1d é praticamente ruído. Não dispara ações sozinha.
- Otimização sempre por `Purchase`. Se não consegue 50 conversões em 7 dias, a recomendação estrutural (orçamento maior, menos conjuntos) é assunto de `/trafego-criar-campanha`. Aqui apenas sinalizar.
- Watchlist após R$ 500 de gasto sem venda.
- Aceitar variações maiores de CPA na janela curta sem reagir.
- Refresh criativo a cada 21 a 30 dias.

---

## 9. Lógica específica. Lançamento

### 9.1 Métrica única
- `CPL` é a única métrica de decisão.
- CTR, hook rate e frequência são leading.
- Volume diário comparado contra meta total declarada (se houver).

### 9.2 Comportamento por fase

| Fase | Postura | Janela dominante |
|---|---|---|
| Aquecimento (D-15 a D-7) | Conservadora, validar criativos com orçamento baixo | 1d |
| Captação inicial (D-7 a D-3) | Sinalizar prontidão para escala dos vencedores | 1d e 3d |
| Captação final (D-3 a D-0) | Tolerar CPL até +30% acima do target em troca de volume | 1d |
| Carrinho aberto | Trocar para campanha de Vendas | 1d e 3d |

### 9.3 Regras específicas
- **Não reduzir orçamento** nos últimos 3 dias da captação enquanto CPL ≤ 2× target. Volume importa mais que custo.
- Pelo menos **3 ângulos criativos** ativos por conjunto durante a captação.
- Janela de 1d tem peso muito maior que no perpétuo.

---

## 10. Hierarquia de ação (ordem ao otimizar)

Investigar e agir **de baixo para cima**:
1. **Anúncio (criativo)**. Diagnóstico mais comum.
2. **Conjunto (segmentação/orçamento)**. Se múltiplos criativos do mesmo conjunto estão ruins.
3. **Campanha (estrutura/objetivo)**. Último recurso.

**Regra:** nunca mudar dois níveis ao mesmo tempo no mesmo dia.

---

## 11. Proteções contra reset de aprendizado

Disparam reset:
- Mudança de orçamento > 20%
- Troca de evento de otimização
- Mudança de segmentação (audiência, posicionamento, idiomas)
- Mudança de estratégia de lance (cost cap / bid cap)
- Pausar e reativar conjunto após 7+ dias

Quando a ação proposta dispara reset, a skill:
1. Calcula custo aproximado de reaprendizado: 50 × CPA target (perpétuo) ou 50 × CPL target (lançamento).
2. Compara com ganho esperado.
3. Só executa se compensar. Caso contrário, sugere ação alternativa de menor impacto.

---

## 12. Sinal de prontidão para escala (handoff)

> Esta seção é o **bastão** que `/trafego-otimizar` passa para `/trafego-escalar`.

A skill emite `sinal_para_escala.pronta: true` **somente** quando **todas** as condições abaixo são simultaneamente verdadeiras:

```yaml
condicoes_de_handoff_para_escala:
  metrica_norte:
    janela_media_abaixo_target: true            # CPA/CPL ≤ target × 0.9
    janela_longa_abaixo_target: true            # CPA/CPL ≤ target
    tendencia: "estavel_performando"
  lucro:                                         # espelhado da camada de lucro (§3.6)
    roas_sustentado_acima_breakeven: true        # ROAS médio e longo ≥ 1 ÷ margem_contribuicao
    lucro_dia_positivo: true                     # gasto_dia × (ROAS × margem - 1) ≥ 0
    margem_fonte: perguntas_guiadas              # se faixa(0.60-0.80), exigir lucro ≥ 0 no extremo conservador (margem 60%)
  diagnostico_gargalo:
    classificacao: "nenhum"
  saude_estrutural:
    frequencia: "<=2.5"                          # perpétuo / <=3.0 lançamento
    fora_de_aprendizado: true
    pelo_menos_um_criativo_saudavel: true
  prerequisitos_operacionais:
    ultima_edicao_horas: ">=48"
    historico_minimo_da_trilha_cumprido: true
    sem_evento_sazonal_perturbador: true
  backup:
    criativos_saudaveis_no_conjunto: ">=2"       # >=3 para velocidade agressiva
  cooldown:
    horas_desde_ultimo_handoff_de_descida:
      perpetuo_low_mid: ">=168"   # 7d
      perpetuo_high:    ">=336"   # 14d
      lancamento:       ">=24"    # lançamento mata cedo, cooldown curto
```

> **Bloco `lucro`:** **zona amarela** (§3.6: CPA acima do target × 0,9 mas ROAS ≥ break-even) **não emite prontidão**. A camada de lucro exige `lucro_dia ≥ 0` sustentado pra escalar. Faz a régua de subida ficar simétrica com a régua de descida (§7 contém em zona vermelha; §12 escala em zona verde). Quando `confiabilidade_do_dado.nivel = baixa` (Passo 0.8), nunca emitir `pronta: true`: desligar o handoff até a fonte estabilizar.

Se **qualquer** condição reprovar, emitir `pronta: false` com lista de critérios falhos.

**Sugestão de validação via `/trafego-diagnostico`:** quando `pronta: true`, antes de encaminhar para `/trafego-escalar`, sugerir ao aluno: "Quer rodar o detector de falso vencedor (`/trafego-diagnostico` opção [4]) antes de escalar? Ele confirma que o resultado é sustentável." Se recusar ou já tiver rodado, seguir direto.

**Passagem do bastão:** com `pronta: true`, oferecer montar o plano de escala na hora. Com o ok do aluno, acionar a skill `trafego-escalar` passando o payload (`sinal_para_escala`, `confiabilidade_do_dado`, `lucro`, meta de CPA/CPL, conta e campanha). Montar o plano não escreve nada na conta: as escritas da escala passam pelo gate 🛡️ dela.

### 12.1 Recebimento de handoff de descida da escala
Quando `/trafego-escalar` devolve uma campanha (freio total), a otimização recebe um payload e marca a campanha com `vinda_da_escala: true`. Isso ajusta a postura para o próximo ciclo:
- Tolerância menor a problemas (pausar mais cedo).
- Foco em **recuperar margem de segurança** antes de re-emitir prontidão.
- Cooldown obrigatório antes de novo handoff de subida.

Quando o handoff vem do **modo Carteira** da escalar (Fase 1: cortes e realocações pré-montados), a otimização executa só os itens daquele plano, dentro do "aprovar tudo" que o aluno já deu para o plano completo (ver §3.6 da `trafego-escalar`). Se um item falhar ou o aluno mudar o plano, parar e perguntar.

---

## 13. Output esperado

O output ao aluno tem **duas partes**, sempre nessa ordem: primeiro o diagnóstico narrado em bullets (legível), depois o plano técnico estruturado em YAML (executável).

### Parte 1. Diagnóstico narrado em bullets (visível, em português)

Sempre antes do YAML, imprimir o bloco abaixo em markdown. Substituir os `{placeholders}` pelos valores reais do diagnóstico.

```markdown
## Confiabilidade do dado

- **Janela / atribuição:** {ex: últimos 7 dias · 7d clique / 1d visualização}
- **Pixel (evento-norte):** {ok | subnotificando | sem disparo recente}
- **Conciliação com a conta:** {bate ✓ Δ X% | não bate: motivo}
- **Confiança geral:** {alta | média | baixa}{se média/baixa: " · CPA rebaixado, decisão por ROAS + leading"}

## Diagnóstico

- **Trilha:** {trilha legível, ex: "Perpétuo médio (R$ 501 a R$ 1.499)"}
- **Métrica-norte:** {CPA | CPL} · meta R$ {target}
- **Tendência:** {frase em português a partir do diagnostico_tendencia}
- **Gargalo:** {frase em português a partir do diagnostico_gargalo} · {dentro do Meta | fora do Meta}

## O que está acontecendo

- {observação concreta 1 com número}
- {observação concreta 2 com número}
- {observação concreta 3 com número}

## Lucro (estimado, margem {margem}%)

- **Resultado do período:** ~R$ {lucro_janela} de lucro de contribuição em {janela} (~R$ {lucro_dia}/dia)
- **ROAS de break-even:** {1÷margem} · você está em {ROAS atual}
- **CPA de break-even:** R$ {AOV×margem} · meta R$ {target} · zona predominante: {verde | amarela | vermelha}
- {se modo faixa: "lucro em faixa, margem 60 a 80%" | se inconsistência com margem da empresa: avisar}

## Ferramentas disponíveis pra otimizar

> Tudo que esta skill pode fazer na sua conta. O plano de ação abaixo é o que eu **recomendo** dentro desse arsenal.

| Ferramenta | O que faz | Reset? | Recomendado agora? |
|---|---|---|---|
| Reduzir -20% | corta orçamento de quem queima | não | {✓/reserva · motivo curto} |
| Realocação neutra | move do queimador pro vencedor (gasto total igual) | não | {✓/reserva · motivo} |
| Limites por conjunto (CBO) | piso pro vencedor / teto pro queimador, sem pausar | não | {✓/reserva · motivo} |
| Cost cap / bid cap | segura o CPA pelo leilão, sem cortar verba | sim | {✓/reserva · motivo} |
| Pausar | desliga anúncio / conjunto / campanha | não | {✓/reserva · motivo} |
| Cortar posicionamento | desliga placement que queima (ex: Audience Network) | sim | {✓/reserva · motivo} |
| Guardrail automático | regra que vigia e age sozinha 24h | não | {✓/reserva · motivo} |
| Escalar (handoff `/trafego-escalar`) | sobe verba nas vencedoras | n/a | {✓/reserva · motivo} |
| Verificar pixel (handoff `/trafego-pixel`) | checa o rastreamento | n/a | {✓/reserva · motivo} |
| Corrigir página/checkout (handoff `/trafego-oferta-funil`) | diagnostica a oferta e encaminha a correção | n/a | {✓/reserva · motivo} |

**Regra de preenchimento:** marcar `✓` só nas ferramentas que o diagnóstico de hoje realmente pede (com 1 motivo curto), e `reserva` nas demais (com o gatilho que as ativaria, ex: "quando um conjunto específico queimar dentro do CBO"). Assim o aluno vê o poder da skill **e** entende por que só uma parte está sendo recomendada agora.

## Plano de ação

> Detalha **como e em que ordem** fazer o que foi marcado `✓` acima.

- {ação 1 com objeto e justificativa curta, em ordem de prioridade}
- {ação 2 com objeto e justificativa curta}
- {ação 3 com objeto e justificativa curta}

**Rastreamento obrigatório (nenhum item evapora):** todo ativo sinalizado como **vermelho / crítico** no diagnóstico é rastreado até o fim: ou **entra no plano** (mesmo como prioridade baixa), ou aparece na tabela de Ferramentas como `reserva` **com o motivo explícito**. Nunca sumir em silêncio entre o diagnóstico e o plano. Em amostra pequena, o item vermelho vira "observar mais X dias antes de agir" no plano, e não desaparece. Se o aluno perguntar "e a campanha X que você falou?", é sinal de que essa regra foi violada.

## Próximas observações

- {coisa para reanalisar em X horas}

## Está pronta para escalar?

{Sim → modo recomendado e velocidade sugerida | Não → 1 a 3 motivos curtos}
```

**Tradução obrigatória dos enums** (nunca imprimir o nome técnico em inglês ou snake_case na narrativa):

| Enum técnico | Frase em português |
|---|---|
| `estavel_performando` | "estável e performando" |
| `esfriando_ou_ruido` | "esfriando ou com ruído na janela curta" |
| `recuperando` | "em recuperação" |
| `saturacao` | "saturação" |
| `ruim_estrutural` | "ruim estrutural" |
| `entrega_limitada` | "entrega limitada" |
| `criativo` | "criativo não atrai cliques únicos" |
| `tecnico` | "técnico (link, redirect, velocidade da página)" |
| `pagina` | "página de vendas / oferta" |
| `checkout` | "atrito no checkout" |
| `leilao_audiencia` | "leilão / audiência" |
| `nenhum` | "nenhum gargalo identificado" |

Se o plano trouxer briefing de criativo novo com texto de anúncio (gancho, headline, CTA), esse texto segue a regra "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md antes de aparecer ao aluno. O caminho preferido é encaminhar a produção para `/copy-anuncio`, que já faz isso.

### Parte 2. Plano técnico estruturado (YAML)

Imediatamente após a Parte 1, prefixar com a linha "Plano técnico estruturado (para execução):" e entregar:

```yaml
campaign_id: <id>
trilha: perpetuo_low | perpetuo_mid | perpetuo_high | lancamento_low | lancamento_mid | lancamento_high
metrica_norte: cpa | cpl
escopo: campanha_unica | campanhas_multiplas | conta_completa
vinda_da_escala: true | false              # true = retornou recentemente da skill de escala
modo_conexao: MCP_CONECTOR | APP

diagnostico_tendencia: estavel_performando | esfriando_ou_ruido | recuperando | saturacao | ruim_estrutural | entrega_limitada
diagnostico_gargalo: criativo | tecnico | pagina | checkout | leilao_audiencia | saturacao | nenhum
gargalo_dentro_do_meta: true | false | null

confiabilidade_do_dado:                # ver Passo 0.8, preencher SEMPRE
  nivel: alta | media | baixa
  janela: "7d" | "14d" | "30d"
  atribuicao: "7d_clique_1d_visualizacao"   # lido de attribution_setting; "padrao_omni_da_api" se a conta não expõe (não incluir em chamada multi-campo)
  pixel_evento_norte: ok | subnotificando | sem_disparo | inferido_pelo_fluxo_de_vendas   # último = tool de dataset indisponível
  conciliacao_conta: bate | nao_bate | nao_aplicavel   # nao_aplicavel quando escopo é recorte (subconjunto da conta)
  conciliacao_delta_pct: ...
  motivos: [ ... ]                     # presente quando nivel != alta

metricas_atuais:
  norte_curta: ...
  norte_media: ...
  norte_longa: ...
  norte_target: ...
  ctr_link: ...                      # CTR de link (NUNCA o ctr geral)
  ctr_link_fonte: unique_inline_link_click_ctr | inline_link_click_ctr | calculado(link_click/impressions)
  ctr_geral: ...                     # só contexto; proibido usar como CTR de link
  hook_rate: ...
  frequencia: ...
  frequencia_escopo: recorte | conta_completa   # declarar qual; nunca misturar
  cpm_vs_historico_pct: ...
  # valor e amostra (ver §3.4)
  aov_calculado_brl: ...             # valor de compra ÷ compras
  ticket_declarado_brl: ...
  ticket_fonte: resumo_produto | declarado | inferido_da_meta
  aov_vs_ticket: coerente | maior_que_ticket | menor_que_ticket
  compras_na_janela: ...             # base da amostra
  cpa_confiavel: true | false        # false se compras < 10 (perpétuo) / leads < 50 (lançamento)
  roas: ...                          # secundário, salvo amostra pequena / confiabilidade baixa
  # derivadas (marcar "indisponivel_neste_nivel" quando o evento não vier, §3.3)
  connect_rate: ...
  taxa_conversao_pagina: ...
  taxa_conversao_anuncio: ...
  taxa_carrinho_compra: ...        # só perpétuo
  taxa_checkout_compra: ...        # só perpétuo

lucro:                                 # ver §3.6, preencher quando confiabilidade média/alta
  margem_contribuicao: 0.77            # 1 - (taxa_plataforma + reembolso + imposto_faturamento)
  margem_fonte: perguntas_guiadas | faixa(0.60-0.80) | default
  roas_breakeven: 1.30                 # 1 ÷ margem
  cpa_breakeven_brl: 2080              # AOV × margem
  lucro_venda_brl: ...                 # AOV × margem - CPA
  lucro_dia_brl: ...                   # gasto_dia × (ROAS × margem - 1)
  lucro_janela_brl: ...                # gasto × (ROAS × margem - 1)
  zona: verde | amarela | vermelha     # por campanha; vermelha = lucro_dia negativo
  visao_empresa_opcional:
    custo_fixo_por_venda_brl: ...       # custo_fixo_mes ÷ vendas_mes (contexto, não gatilho)
    lucro_liquido_venda_brl: ...

acoes_recomendadas:
  - nivel: ad | adset | campaign | alerta_usuario
    acao: reduzir_20 | realocar_neutro | limitar_conjunto | definir_cost_cap | cortar_posicionamento | instalar_guardrail | pausar | refresh_criativo | manter | alertar | aguardar
    objeto_id: <id>
    # campos extras por tipo de ação:
    #   realocar_neutro       → de_objeto_id, para_objeto_id, valor_movido_brl
    #   limitar_conjunto      → daily_min_spend_target, daily_spend_cap (centavos)
    #   definir_cost_cap      → bid_strategy, bid_amount (centavos)            [reset: SIM]
    #   cortar_posicionamento → metodo (soft_opt_out|manual), posicionamento  [reset: SIM]
    #   instalar_guardrail    → trigger, acao_regra (PAUSE|CHANGE_BUDGET|NOTIFICATION), threshold, via (manual_guiado_gerenciador | trafego_regras)
    #   alertar (fora do Meta) → handoff (/trafego-oferta-funil | /feedback-pagina | /feedback-low-ticket | /pagina-checkout | /pagina-performance | /pagina-pixel)
    #   refresh_criativo      → handoff (/copy-anuncio | /criativo-estatico | /mandala-de-anuncios | /trafego-testes)
    reset_aprendizado: true | false           # true em definir_cost_cap e cortar_posicionamento
    tool_call:
      name: pause_ad | update_adset_budget | update_campaign_budget | realocar_neutro | limitar_conjunto | definir_cost_cap | cortar_posicionamento | instalar_guardrail | ...
      params: { ... }                         # parâmetros prontos
    justificativa: <texto curto referenciando o gargalo identificado>
    prioridade: alta | media | baixa
    aguardar_horas_apos: 0 | 24 | 48 | 72

# Bloco presente APENAS quando todas as condições da seção 12 são verdadeiras
sinal_para_escala:
  pronta: true | false
  motivo_se_nao_pronta: [ ... ]              # lista de condições reprovadas
  modo_recomendado: vertical | horizontal | vertical_e_horizontal | null
  velocidade_sugerida: conservadora | normal | agressiva | null
  janela_referencia: "3d" | "7d" | "14d" | "30d"
  cpa_ou_cpl_atual: ...
  target: ...
  margem_de_seguranca: 0.27                  # quanto a métrica-norte está abaixo do target
  riscos_observados: [ ... ]
  criativos_de_backup_disponiveis: 2

proximas_observacoes:
  - <coisa para reanalisar em X horas>
```

### Exceção
Se o aluno disser explicitamente "me dá só o YAML" ou "modo direto" na sessão, omitir a Parte 1.

**Após entregar as duas partes,** oferecer (opcional) o painel de decisão em HTML: ver §17 e `sub-skills/_export-painel-decisao.md`.

### 13.1. Tabelas em português

TODA tabela markdown impressa para o aluno (antes ou depois do YAML técnico) deve usar cabeçalhos em português brasileiro. Os campos da Graph API entram em inglês mas são traduzidos no cabeçalho. Os identificadores de campo dentro do YAML técnico continuam em snake_case (vão para tool_calls).

**Mapa obrigatório de tradução:**

| Campo Graph API | Cabeçalho em português |
|---|---|
| `spend` | Investimento |
| `impressions` | Impressões |
| `reach` | Alcance |
| `frequency` | Frequência |
| `clicks` | Cliques |
| `inline_link_clicks` | Cliques no link |
| `unique_inline_link_clicks` | Cliques únicos no link |
| `ctr` | CTR geral |
| `inline_link_click_ctr` | CTR no link |
| `unique_inline_link_click_ctr` | CTR único no link |
| `cpc` | CPC |
| `cpm` | CPM |
| `cost_per_inline_link_click` | Custo por clique no link |
| `purchases` | Compras |
| `leads` | Leads |
| `cpa` | CPA |
| `cpl` | CPL |
| `roas` | ROAS |
| `connect_rate` | Taxa de conexão |
| `conversao_pagina` | Conversão da página |
| `conversao_anuncio` | Conversão do anúncio |
| `taxa_carrinho_compra` | Carrinho → Compra |
| `taxa_checkout_compra` | Checkout → Compra |
| `campaign_name` | Campanha |
| `adset_name` | Conjunto |
| `ad_name` | Anúncio |
| `date_start` / `date_stop` | Período |

---

## 14. Princípios que a skill nunca viola

1. **Mudanças graduais sempre.** Orçamento move em ±20%, nunca mais.
2. **Aguardar maturação.** Mínimo 48h entre ajustes no mesmo objeto.
3. **Diagnóstico antes de ação.** Sempre rodar tendência + gargalo antes de propor.
4. **Verificar saúde técnica** antes de pausar campanha inteira.
5. **Preservar aprendizado.** Só aceitar reset quando ganho compensa.
6. **Métrica-norte é única por trilha.** CPA em perpétuo, CPL em lançamento. ROAS apenas como confirmação, **exceto** amostra pequena (menos de 10 compras) ou confiabilidade baixa, quando ROAS vira decisão (ver §3.1 e §3.4).
7. **Bottom-up sempre.** Criativo antes de conjunto, conjunto antes de campanha.
8. **Em lançamento na reta final, volume > custo** (até o limite de 2× CPL target).
9. **Apenas dados nativos do Gerenciador.** Se não vem do Gerenciador, não entra na decisão.
10. **Métricas derivadas sempre calculadas** quando o evento existe. Connect rate, conversão da página/anúncio e taxas de checkout entram no diagnóstico (lidas via `/trafego-insights`); quando o evento não vem no caminho usado, são declaradas `indisponível neste nível` (§3.3).
11. **Não pausar quando o gargalo está fora do Meta.** Alertar o aluno, encaminhar para `/trafego-oferta-funil` e para a skill de correção (§5.2) e, se necessário, reduzir -20% como contenção, mas manter a estrutura viva.
12. **Não escalar nesta skill.** Quem sobe orçamento e duplica conjuntos é `/trafego-escalar`. Aqui só emitir sinal de prontidão.
13. **Respeitar cooldown.** Após handoff de descida da escala, aguardar 7d (perpétuo low/mid), 14d (perpétuo high) ou 24h (lançamento) antes de re-emitir prontidão.
14. **Detectar ABO vs CBO antes de qualquer mudança de orçamento.** Ler `budget.tipo` da campanha. Em ABO, mudança vai no adset (`update_adset_budget`); em CBO, vai na campanha (`update_campaign_budget`). Sem o tipo detectado, não sugerir redução: marcar `acao: aguardar`. Em CBO com gargalo localizado, oferecer teto no conjunto, realocação ou pausa do conjunto específico em vez de reduzir a campanha inteira. Ver seção 6.0.
15. **Validar a fonte antes de interpretar.** Rodar o Passo 0.8 (janela/atribuição, pixel, conciliação, descoberta de campos) e **mostrar a conferência ao aluno**. Sem isso, não diagnosticar.
16. **Campo certo, sem troca silenciosa.** CTR de link nunca é o `ctr` geral. Descer na ordem de preferência de campo (§3.2) e declarar a fonte. Métrica indisponível é declarada como tal, nunca inventada nem assumida como zero.
17. **Amostra pequena não decide por CPA.** Menos de 10 compras (ou 50 leads) na janela: CPA marcado não confiável; decidir por ROAS + leading.
18. **Conciliar com o total da conta quando o escopo é a conta inteira.** Em `escopo: conta_completa`, a soma das campanhas tem que bater com o total da conta (±5%) na mesma janela e atribuição; não bateu, avisa e não age. **Em recorte (subconjunto de campanhas nomeadas), a conciliação com o total não se aplica** (`nao_aplicavel`): validar consistência de janela/atribuição entre as campanhas do recorte e seguir. Ver Passo 0.8 item 3.
19. **Carimbar escopo, janela, atribuição e fonte** em todo agregado. Frequência do recorte é diferente de frequência da conta; ROAS calculado é diferente de ROAS do Gerenciador. Nunca apresentar número sem dizer de onde veio.
20. **Decidir por lucro; CPA é guardrail, não juiz.** Traduzir para reais via margem de contribuição (§3.6). Conter ou pausar por dinheiro só na **zona vermelha** (lucro/dia negativo / ROAS abaixo do break-even). **Zona amarela** (acima da meta de CPA mas ainda lucrativa) se otimiza, não se contém. **Custo fixo (aluguel, salário) nunca entra na decisão de campanha.** Todo valor de lucro com a premissa de margem carimbada; lucro de contribuição é diferente de margem líquida da empresa.
21. **Realocação e limites são neutros: nunca aumentam o gasto total.** A skill segura o freio (reduzir/pausar/reativar) e otimiza a distribuição (realocar do queimador pro vencedor §6.3, pôr piso/teto por conjunto em CBO §6.4), mas **subir o gasto total é escala (`/trafego-escalar`), nunca aqui.** Na realocação, teto de 20% nos **dois** lados pra não resetar aprendizado. Limites de conjunto só em CBO com 2+ conjuntos.
22. **Ação que reseta aprendizado pede conta de custo + confirmação reforçada.** `definir_cost_cap` (§6.5) e `cortar_posicionamento` (§7.4) disparam reset: antes de propor, rodar a conta da §11 (≈ 50 × CPA target) e mostrar o custo no gate. No posicionamento, tentar **soft opt-out** antes do manual, e no manual sempre **ler, modificar e regravar** o `targeting` completo. Em CBO, lance vai na **campanha**, com verificação antes de gravar. O **guardrail (§18)** não reseta, mas não tem tool no MCP: no MCP vira passo a passo guiado no Gerenciador; no APP, handoff para `/trafego-regras`.
23. **Gate 🛡️ antes de toda escrita, DELETE nunca.** Um "sim" por lote no mesmo fluxo; atalho composto só com "aprovar tudo" explícito; esta skill não apaga entidade (pausa ou arquiva). Token nunca aparece no chat.

---

## 15. Ações em lote por filtro

> Detalhes completos em `sub-skills/acoes-lote.md`.

Quando o aluno pede "pausa tudo com ROAS<1 nas últimas 2 semanas" ou "reduz 20% nos adsets com CPA > R$ 80", a skill aplica a ação em **múltiplas entidades** filtradas por critério.

Funções disponíveis:
- `pausar_em_lote(filtro)`. Pausa todas as entidades que batem o filtro.
- `reduzir_budget_em_lote(filtro, percent)`. Reduz budget % nas entidades que batem.
- `pausar_top_n_pior(metric, n)`. Pausa as N piores em uma métrica.

Critérios suportados: `roas`, `cpa`, `cpl`, `ctr`, `frequency`, `cpm`, `spend`, `impressions`, `purchases`, `leads`, `cpc`. Operadores: `less_than`, `greater_than`, `between`, `equal`. Períodos: `today`, `last_3d`, `last_7d`, `last_14d`, `last_30d`.

**Sempre exige preview** com lista de entidades afetadas, no formato do bloco 🛡️ (um bloco e um "sim" para o lote inteiro), antes de aplicar. Bloqueia automaticamente se mais de 50% dos adsets ativos da conta forem afetados (confirmação tripla).

---

## 16. Atalhos compostos

> Detalhes completos em `sub-skills/atalhos-compostos.md`.

Atalhos que orquestram múltiplas skills numa única operação:

- **Atalho A. Lookalike de compradores para campanha**. Orquestra `/trafego-publicos` (público de Compra + lookalike) + `/trafego-criar-campanha`.
- **Atalho B. Duplicar melhor anúncio em outro público**. Orquestra `/trafego-analise` [3] (identifica o melhor) + `/trafego-publicos` (sugere alternativa) + `/trafego-testes` [9] (duplicar com variação).
- **Atalho C. Faxina + lookalike**. Pausa queimadores (acoes-lote) + cria lookalike de compradores.
- **Atalho D. Refresh criativo**. `/trafego-analise` [3] identifica ângulos da Mandala em uso + `/mandala-de-anuncios` sugere ângulos novos + `/copy-anuncio` e `/criativo-estatico` produzem as peças + `/trafego-testes` sobe o A/B.

Toda execução de atalho composto segue o **modo "lote pré-aprovado" do CLAUDE.md**:
1. Anuncia o plano completo, numerado, antes de qualquer escrita.
2. Pede **uma** confirmação explícita para o fluxo inteiro: o aluno responde **"aprovar tudo"** (ou "sim, aprovo tudo"). Um "sim" solto a outra pergunta, ou resposta ambígua, não libera o fluxo: aí cada etapa passa pelo gate 🛡️ normal.
3. Executa em sequência, pausando e perguntando se uma etapa falha.
4. Devolve resumo com IDs criados + como reverter. **DELETE nunca entra no "aprovar tudo":** desfazer algo apagando sempre tem bloco 🛡️ e "sim" próprios.

---

## 17. Painel de decisão (export HTML opcional)

> Detalhes completos em `sub-skills/_export-painel-decisao.md`.

Depois de entregar o diagnóstico (§13, Parte 1 + Parte 2), oferecer **opcionalmente** um painel visual: um HTML standalone centrado em **dinheiro** (camada de lucro, §3.6) e nas **três zonas**, terminando no plano de ação. Não é relatório (isso é a `/trafego-analise`) nem dashboard ao vivo da conta (isso é o `/trafego-dashboard`); é um **painel de decisão**, fotografia do diagnóstico de hoje.

```
Quer salvar esse diagnóstico como um painel visual (HTML)? (s/n)
```

Regras (todas na sub-skill):
- **Nunca rodar sem confirmação explícita.** Aluno que só quer o texto não recebe arquivo.
- **Reusa o motor de gráficos** `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py` (roda sem token, em qualquer modo) e o **design system + esqueleto** de `.claude/skills/trafego-analise/sub-skills/_export-html.md`, no tema escolhido pelo aluno (Escuro, Terra ou Claro Neutro, `EXPORT_TEMA` no `.env`). **Proibido inventar HTML.**
- 3 gráficos obrigatórios: **mapa das 3 zonas** (`scatter`), **lucro/dia por campanha** (`divbars`), **confiabilidade do dado** (`gauge`).
- Usa os números **já calculados no diagnóstico** da sessão, sem refazer fetch.
- Salva em `meus-produtos/{ativo}/entregas/trafego/otimizar/painel-decisao-{YYYY-MM-DD-HHMM}.html` e **abre no navegador automaticamente** via `scripts/abrir-html.py` (mesmo script da análise, com o interpretador Python detectado na sessão).
- **Gate de conformidade obrigatório** antes de entregar (svg, chart-card, topbar, bg, legenda de zonas, KPI de lucro). Falhou, não entrega nem abre.
- Aviso de **snapshot** sempre (fotografia do momento, não atualiza sozinho) e **premissa de margem carimbada** no topo.

---

## 18. Guardrail automático (instalar regra de contenção)

> Transforma o diagnóstico em **vigia permanente**: uma regra nativa da Meta que pausa, reduz ou só avisa quando o CPA passa do break-even. O valor de fazer **a partir da otimizar**: ela já sabe o seu break-even, então **pré-preenche a regra com o número certo**.

**Exemplos de regra:**
- "Se CPA > break-even (R$ {be}) por 3 dias, pausar a campanha."
- "Se gasto > R$ {x}/dia com ROAS < break-even, me avisar."
- "Se frequência > 4, reduzir o orçamento em 15%."

**Mecanismo:** `adrules_library` (evaluation_spec + execution_spec: `PAUSE` / `CHANGE_BUDGET` / `NOTIFICATION` + schedule).

**Por modo:**

- **`MCP_CONECTOR`: passo a passo guiado no Gerenciador.** Não existe tool de regra automática no conector. A skill entrega o roteiro já preenchido com os números do diagnóstico e espera o aluno avisar que terminou:

  ```
  Vou te guiar pra criar a regra no Gerenciador de Anúncios. Leva uns 2 minutos.

  1. Abra o Gerenciador de Anúncios e marque a caixa da campanha "{nome}".
  2. Na barra de cima, clique em Regras e depois em Criar nova regra.
  3. Em Ação, escolha: {pausar a campanha | diminuir o orçamento diário em 15% | só enviar notificação}.
  4. Em Condições, coloque: {Custo por resultado} {maior que} R$ {threshold}.
  5. Em Período de tempo, escolha: {últimos 3 dias}.
  6. Em Programação, deixe rodando continuamente.
  7. Dê o nome "{nome sugerido da regra}" e clique em Criar.

  Os nomes dos botões podem variar um pouco conforme a versão do Gerenciador.
  Me avisa quando terminar que eu sigo o plano.
  ```

  Agendamento por horário (ligar e pausar em faixas do dia, `adset_schedule`) não é regra automática: vai pelo MCP com `ads_update_entity`, com gate 🛡️.

- **`APP`: handoff para `/trafego-regras`**, passando o trigger, a ação e o threshold prontos. Ela cria a regra via `POST /act_<id>/adrules_library` e passa pelo gate próprio.

**Reset: não** (é criar regra; a regra só age quando o trigger bate).

**Gate 🛡️ (no APP):** descrever a regra em português (o que dispara, o que faz, em qual objeto), reversível (desativar a regra).

**No YAML:** ação `instalar_guardrail` (objeto_id, `trigger`, `acao_regra`, `threshold`, `via`).
