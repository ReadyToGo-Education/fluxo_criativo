---
name: trafego-analise
description: >
  Análise narrada de tráfego pago Meta Ads com terminologia VTSD (Mandala de 18 tipos, Urgência
  Oculta, Quadro na Parede, Furadeira, Decorados, 3 Identidades, HOT/COLD/SUPERCOLD, Caixa Rápido,
  Pico vs Evergreen). Hub de menu com 10 outputs narrativos: Diagnóstico Rápido, Performance & Funil,
  Criativos & Copy, Geo & Demografia, Timing & Sazonalidade, Investigação Profunda, Lifecycle &
  Histórico, Problemas Ocultos, Orçamento & Projeção, Comparativo A x B. Aluno escolhe um output por vez, recebe
  análise completa pelo método VTSD com handoff para skill executora quando ação for necessária.
  Lê dados via /trafego-insights (com cache local em arquivo .md). Use quando o aluno pedir
  análise narrada, ranking, comparativo, diagnóstico, mapa do funil, ou quiser ensinar tráfego
  pelo método.
---

# Tráfego Análise. 10 Outputs Narrativos VTSD

Análise narrada de campanhas Meta Ads pela lente da metodologia VTSD (Venda Todo Santo Dia, Leandro Ladeira). Cada métrica de tráfego é o termômetro de um elemento do método. O propósito é conectar dado → método → decisão, e entregar análise pedagógica que serve tanto para operar quanto para ensinar.

**Diferença vs outras skills de tráfego:**
- `/trafego-insights` é a **fonte de dados** (lê e cacheia, não narra).
- `/trafego-otimizar` é **técnico**, calcula, executa pausa/ajuste de budget. Foca em **operação**.
- `/trafego-escalar` **escala** campanhas validadas com freios.
- `/trafego-regras`, `/trafego-publicos`, `/trafego-pixel`, `/trafego-testes` **executam** ações específicas.
- `/trafego-diagnostico`, `/trafego-criativos` e `/trafego-oferta-funil` aprofundam a investigação (hipóteses, criativo, página/oferta/checkout).
- `/trafego-dashboard` mostra os números da conta num painel ao vivo.
- `/trafego-analise` **narra** com terminologia VTSD. **Não executa edição.** Quando a análise sugere ação, ela faz handoff para a skill executora correspondente.

---

## Como funcionar

Ao ser invocada, carregar o contexto do produto, validar a conexão Meta, perguntar a conta de anúncios e apresentar o menu. Aguardar escolha antes de pedir período ou dado.

### Passo 0. Contexto do produto e conexão Meta

#### 0.1 Produto ativo

Seguir a seção "Contexto Persistente do Negócio" do CLAUDE.md:

1. Ler `meus-produtos/.ativo`. Se não existir, orientar o aluno a usar `/produto-novo` primeiro.
2. Ler `meus-produtos/{ativo}/resumo-produto.md` direto, sem conferir antes se ele existe.
   - Se não for encontrado e o `perfil.md` tiver o Quadro preenchido: anunciar `⏳ Preparando o resumo do seu produto (só na primeira vez).`, acionar o agente `gerador-resumo-produto` com o slug do produto e ler o resumo gravado.
   - Se nem o `perfil.md` existir (ou estiver sem Quadro): orientar `/produto-concepcao` primeiro.
3. Do resumo saem **preço/ticket, tipo de produto (low, middle ou high ticket), público-alvo, Quadro, Furadeira, Decorados, Urgências Ocultas, objeções e identidades**. As sub-skills leem esses dados do resumo e **não perguntam de novo**. Só perguntar ao aluno o que o resumo não tem (CPL-alvo, CPA meta, margem, período, escopo de campanhas, status). Para detalhe que o resumo não traz (ex.: baldes de público, objeções completas), ler só a seção indicada na tabela "Onde está o detalhe completo" no fim do resumo.

#### 0.2 Conexão Meta e estratégia de leitura por modo

Ler `META_AUTH_MODO` no `.env`. Se vazio, acionar `/trafego-conexao` antes de qualquer outra ação. No modo `MCP_CONECTOR`, confirmar que existe pelo menos uma tool terminada em `ads_get_ad_entities` (o prefixo do servidor varia); se nenhuma aparecer, pedir ao aluno para reabrir o Claude Code e, se persistir, voltar ao `/trafego-conexao`. No modo `APP`, confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem no `.env` (checar presença com `grep -q`, nunca `cat .env`); se faltar algum, acionar `/trafego-conexao`.

Esta skill é **100% leitura** (narra, não executa): **não tem gate de escrita**. O que muda por modo é **como os dados são buscados**:

| Modo | Como buscar os dados |
|---|---|
| **`MCP_CONECTOR`** (padrão, recomendado) | **Sem token e sem os scripts de busca.** Ler com `ads_get_ad_entities` (métricas por conta/campanha/conjunto/anúncio). Atenção: **dicionário de campos diferente da Graph API** e **retorno estoura em conta grande** (ver **Contrato anti-erros**). `ads_insights_performance_trend` é **só tendência temporal de conta/anúncio/conjunto: NÃO faz nível campanha nem serve para ranking/funil**. Descobrir a tool pelo **final do nome** (ex: `ads_get_ad_entities`), nunca pelo prefixo (pode ser UUID). |
| **`APP`** (reserva) | Scripts Python (`trafego_fetch.py`/`trafego_processar.py`) e/ou `curl` na Graph API com `FB_ACCESS_TOKEN_PERMANENTE` (caminho "Modo APP" das sub-skills). |

**Conta não liberada no MCP:** se a tool responder `is_ads_mcp_enabled: false` ou o erro "Ads MCP is gradually being rolled out", explicar em linguagem simples que a Meta ainda não liberou o conector para essa conta de anúncios e oferecer trocar para o modo App pelo `/trafego-conexao`. Nunca pedir token no chat.

**Regra dura:** no `MCP_CONECTOR`, **nunca** chamar `trafego_fetch.py`/`trafego_processar.py` nem `curl` com token: eles dependem de `FB_ACCESS_TOKEN_PERMANENTE`, que não existe nesse modo. A renderização de HTML (`_export-html.md`) e a geometria de gráficos (`trafego_chart_geom.py`) **não tocam a API** e rodam em qualquer modo.

**Interpretador Python:** nos comandos desta skill, `{PY}` é o interpretador detectado na sessão (`python3` ou `py -3`), conforme a seção "Execução de Scripts Python" do CLAUDE.md. Caminhos sempre a partir da raiz do projeto.

#### Contrato anti-erros (aprendido em produção em 2026-05-29, conta grande com 100+ campanhas)

Seis regras duras que evitam os erros reais já cometidos. Valem para TODOS os 10 outputs.

**1. Dicionário de campos: MCP ≠ Graph API.** São listas diferentes; pedir campo do dicionário errado dá `error_code 100 (Unsupported field)`.
- **Graph API (`curl`, modo `APP`):** aceita `actions`, `action_values`, `outbound_clicks`, `cost_per_action_type`, `video_p25_watched_actions` etc. (eventos de funil saem dentro do array `actions`).
- **Tool `ads_get_ad_entities` (modo `MCP_CONECTOR`):** **NÃO** aceita `actions`/`action_values`/`outbound_clicks`. Usar: `purchase_roas` (ROAS pronto), `actions:omni_purchase` (compras), `actions:link_click`, `result_values`, `results`, `cost_per_result`, `cost_per_action_type`, `cpm`, `ctr`, `spend`, `impressions`, `reach`, `frequency`, `video_p25_watched_actions`. Sempre incluir `id` e `name`. Em dúvida sobre um campo, chamar `ads_get_field_context` antes. Nunca chutar.

**2. Conta grande estoura o retorno da tool.** `ads_get_ad_entities` com muitos campos × 100+ campanhas excede o limite de tokens e é salvo em arquivo automaticamente. Prevenir e tratar:
- Sempre passar **whitelist enxuta de campos** + `limit` explícito.
- Se mesmo assim o retorno for salvo em arquivo, **processar o arquivo com python/jq** (ele não tem token, é seguro). Não tentar reler tudo no contexto.
- No modo `APP`, uma chamada `/insights?level=campaign&date_preset=...` traz as 100+ campanhas em JSON único, sem esse problema.

**3. `ads_insights_performance_trend` é só tendência.** Faz série temporal de conta/anúncio/conjunto. **Não faz nível campanha** e **não serve para ranking, funil ou comparativo por campanha**: retorna vazio em `analysis_level=CAMPAIGN`. Para isso, usar `ads_get_ad_entities` (MCP) ou `/insights?level=campaign` (`curl`, modo APP).

**4. Ancorar datas no retorno, nunca em "hoje" assumido.** O relógio do ambiente, do conector e da Graph API podem divergir. Para o período atual usar `date_preset` (`last_7d`/`last_14d`/`last_30d`) e **ler o `date_start`/`date_stop` que voltou**. Para o período anterior (comparativo WoW), calcular a janela **a partir desse `date_start`** (ex: 30 dias imediatamente antes), nunca de uma data fixa chutada.

**5. Disciplina de saída (evita corte e embaralho do terminal).** Scripts de processamento **gravam JSON num arquivo** (`/tmp/...`) e a leitura é feita com `Read` em fatias ou imprimindo **uma linha JSON por vez**. **Nunca** despejar tabela multilinha grande no stdout: o terminal trunca, embaralha e gera retrabalho. Um número por linha curta é confiável; tabelão não é.

**6. `curl -g` quando o `fields` tem nesting** (`campaign{name}`, `creative{...}`), conforme a regra global do CLAUDE.md. Sem `-g` o `curl` quebra a URL silenciosamente (200 sem os campos). Nunca exibir o `curl` com o token no chat: mascarar como `***TOKEN_MASCARADO***`.

> **Validação cruzada obrigatória:** ao filtrar um escopo (ex: 10 campanhas de uma lista), conferir que a soma dos recortes (posição, idade, gênero) bate aproximadamente com o total das campanhas. Breakdowns não reconciliam 100%: declarar isso ao aluno e tratar recortes como **direcionais**, nunca inventar para "fechar a conta".

### Passo 0.5. Selecionar conta de anúncios

Ler `FB_AD_ACCOUNT_IDS` no `.env` (campo com múltiplas contas separadas por vírgula, ex: `<id1>,<id2>,<id3>`). Também ler `FB_AD_ACCOUNT_ID` (conta padrão).

**Se houver apenas uma conta configurada** (`FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS` idênticos ou `FB_AD_ACCOUNT_IDS` vazio): usar automaticamente essa conta e pular a pergunta.

**Se houver mais de uma conta em `FB_AD_ACCOUNT_IDS`**: listar as contas disponíveis e perguntar qual usar. Obter o nome de cada conta **roteando por modo** (ver Passo 0.2):

- **`MCP_CONECTOR`:** chamar a tool `ads_get_ad_accounts` (já traz `name` de cada conta, sem token).
- **`APP`:** uma única chamada `Bash(curl ...)` batch (sem heredoc Python, ver regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md). Construir a string `act_<id1>,act_<id2>,...` a partir de `FB_AD_ACCOUNT_IDS` e disparar:

```
curl -s "https://graph.facebook.com/v25.0/?ids=act_<id1>,act_<id2>,act_<id3>&fields=name&access_token=<TOKEN_DO_ENV>"
```

A resposta vem em JSON único:
```json
{
  "act_<id1>": {"name": "Conta A", "id": "act_<id1>"},
  "act_<id2>": {"name": "Conta B", "id": "act_<id2>"},
  ...
}
```

O Claude lê o JSON retornado como texto e monta o menu numerado. **Nunca fazer N chamadas separadas**: uma única chamada batch é o suficiente e conta como 1 contra o rate limit.

**Tratamento de erro:** se a chamada batch falhar, exibir só os IDs sem nome e continuar.

**Ordenação obrigatória:** a conta cujo ID coincide com `FB_AD_ACCOUNT_ID` é a conta padrão e deve sempre aparecer em **primeiro lugar** na lista, com a etiqueta `"padrão"` entre aspas após o nome. As demais contas seguem na ordem em que aparecem em `FB_AD_ACCOUNT_IDS`.

Montar o menu assim:
```
Qual conta de anúncios deseja analisar?

[1] Nome da Conta Padrão "padrão"  (act_<id1>)
[2] Nome da Conta B                (act_<id2>)
[3] Nome da Conta C                (act_<id3>)

Digite o número:
```
Se a chamada de nome falhar para alguma conta, exibir só o ID sem nome. A conta padrão ainda recebe a etiqueta `"padrão"` mesmo sem nome.

**Após a escolha:** definir `AD_ACCOUNT_ID_ATUAL` como variável de sessão (ex: `act_<id1>`). Usar esse ID em todas as chamadas subsequentes desta sessão, inclusive ao chamar `/trafego-insights`.

### Passo 0.55. Filtro de status das campanhas

Antes de buscar os grupos, perguntar quais status incluir:

```
Quais campanhas incluir na análise?

[1]  Somente ativas      (ACTIVE: o que está rodando agora)
[2]  Somente pausadas    (PAUSED + WITH_ISSUES: o que está desligado)
[3]  Ativas + pausadas   (visão completa do presente)
[4]  Histórico completo  (inclui arquivadas: análise de longo prazo)
```

Salvar como `STATUS_FILTRO` (variável de sessão) e usar em todas as chamadas subsequentes:

| Escolha | `effective_status` na API | Valor de `--status` nos scripts (modo APP) |
|---------|--------------------------|--------------------------------------------|
| [1] | `["ACTIVE"]` | `ACTIVE` |
| [2] | `["PAUSED","WITH_ISSUES"]` | `PAUSED,WITH_ISSUES` |
| [3] | `["ACTIVE","PAUSED","WITH_ISSUES"]` | `ACTIVE,PAUSED,WITH_ISSUES` |
| [4] | `["ACTIVE","PAUSED","WITH_ISSUES","ARCHIVED"]` | `ACTIVE,PAUSED,WITH_ISSUES,ARCHIVED` |

`effective_status` só vale nos endpoints de listagem (`/campaigns`, `/adsets`, `/ads`). O `/insights` **não aceita** esse parâmetro: o filtro de status é aplicado listando as campanhas com o status escolhido e cruzando os IDs com o retorno do `/insights`. No modo APP, o `trafego_fetch.py` já faz isso (Chamada 0) quando recebe `--status`. Se o aluno não passou por este passo (chamada direta, sem menu), o padrão do script é `ACTIVE,PAUSED,WITH_ISSUES`.

**Alerta automático para output [8] Problemas Ocultos:** se `STATUS_FILTRO = ["ACTIVE"]` e o aluno escolher o output [8], alertar antes de rodar: "Você está analisando só campanhas ativas. Para ver ad sets quebrados e anúncios pausados por problema, reinicie e escolha [2] ou [3]."

---

### Passo 0.6. Identificar escopo de análise

Após definir `AD_ACCOUNT_ID_ATUAL` e `STATUS_FILTRO`, **sempre buscar todas as campanhas da conta** com o status escolhido, sem pré-filtrar por nome. Rotear por modo (ver Passo 0.2):

```
MCP: ads_get_ad_entities (level=campaign, ad_account_id=AD_ACCOUNT_ID_ATUAL,
     effective_status=STATUS_FILTRO), sem token
APP: GET /act_{AD_ACCOUNT_ID_ATUAL}/campaigns?fields=id,name,objective,status
     &effective_status={STATUS_FILTRO}&limit=200&access_token={FB_ACCESS_TOKEN_PERMANENTE}
```

Salvar a lista completa em memória de sessão (`CAMPANHAS_SESSAO`). Não filtrar ainda.

**Em seguida, perguntar como o aluno organiza as campanhas:**

```
Como suas campanhas estão nomeadas?

[1]  Por nomenclatura          você informa o padrão que usa
                               (ex: PRODUTO - FUNIL - NOME, [PRODUTO]-[FUNIL]-NOME)

[2]  Filtro personalizado      você informa palavra-chave, trecho do nome ou IDs

[3]  Sem padrão definido       a IA tenta identificar agrupamentos automaticamente
```

---

#### Opção [1]. Por nomenclatura

Perguntar:
```
Qual é o formato do nome das suas campanhas?
(ex: "PRODUTO - FUNIL - NOME DA CAMPANHA", "[PRODUTO][FUNIL] Nome")
```

Com o padrão informado, parsear todos os nomes em `CAMPANHAS_SESSAO` e extrair os segmentos. Agrupar pelo **primeiro segmento** (produto/marca). Montar menu:

```
Grupos encontrados pela nomenclatura "{padrão informado}":

[1]  CURSO X               38 campanhas
[2]  MENTORIA              10 campanhas
[3]  NEWS                   2 campanhas
[4]  Todas as campanhas    50 campanhas (sem filtro de grupo)

Com qual grupo quer trabalhar?
```

Se nenhuma campanha bater com o padrão, informar: "Não consegui identificar grupos com esse padrão. Posso tentar automaticamente ou você prefere ver todas juntas?" e oferecer as opções [3] e "Todas".

---

#### Opção [2]. Filtro personalizado

Perguntar:
```
Digite o trecho do nome, palavra-chave ou IDs de campanha que quer analisar:
(ex: "remarketing", "VSL", "<id da campanha>", "CURSO X - RMK")
```

Filtrar `CAMPANHAS_SESSAO` pelo texto informado (busca por substring, case-insensitive). Mostrar quantas campanhas foram encontradas e confirmar antes de prosseguir. Salvar como `ESCOPO_FILTRO = nome_contém:{texto}`.

---

#### Opção [3]. Sem padrão definido (auto-detecção)

Analisar `CAMPANHAS_SESSAO` e tentar agrupar por:
1. **Prefixos comuns**: sequências antes do primeiro espaço, hífen ou colchete. Prefixo com 2+ campanhas vira grupo.
2. **Objetivo Meta**: quando prefixos se confundem, agrupar por `objective` (`OUTCOME_SALES`, `OUTCOME_LEADS`, `LINK_CLICKS`, `OUTCOME_AWARENESS`).
3. **Palavras-chave recorrentes**: `RMK`, `CV`, `LEAD`, `ENGAJAMENTO`, `PUBLICO`.

Apresentar os grupos encontrados + sempre incluir "Todas as campanhas" como última opção:

```
Identifiquei os seguintes grupos (detecção automática):

[1]  CURSO X. Produto principal   46 campanhas · OUTCOME_SALES
[2]  MENTORIA. Captação de leads  10 campanhas · OUTCOME_LEADS
[3]  Publicações Instagram        20 campanhas · LINK_CLICKS
[4]  NEWS. Newsletter              2 campanhas · OUTCOME_LEADS
[5]  Todas as campanhas           78 campanhas (sem agrupamento)

Com qual grupo quer trabalhar?
```

Regras:
- Listar apenas grupos com 1+ campanha. Nunca mostrar grupo vazio.
- Ordenar por quantidade de campanhas (decrescente). "Todas as campanhas" sempre por último.
- Se a conta tiver padrão confuso demais (todos prefixos únicos), mostrar só "Todas as campanhas" diretamente, sem menu de grupos.
- Se a chamada à API falhar, pular este passo e seguir com `ESCOPO_FILTRO = conta_completa`, avisando o aluno.

---

**Após a escolha do grupo** (em qualquer das três opções):

Definir `ESCOPO_FILTRO` na sessão:
- Grupo específico: `ESCOPO_FILTRO = nome_contém:{prefixo/texto}`. Usado para filtrar em Python ao processar insights, não na API.
- "Todas as campanhas" / sem filtro: `ESCOPO_FILTRO = conta_completa`.
- IDs específicos: `ESCOPO_FILTRO = ids:{id1,id2,...}`.

`ESCOPO_FILTRO_TEXTO` é só o texto do filtro de nome (vazio quando `conta_completa`). É ele que vai no `--filtro` dos scripts. Para `ids:`, filtrar os IDs na leitura do resultado (os scripts filtram por nome).

**Regra importante:** o filtro é sempre aplicado em Python sobre `CAMPANHAS_SESSAO`, nunca via parâmetro `filtering` da Graph API (evita comportamentos inconsistentes da API com strings Unicode e caracteres especiais).

Usar `ESCOPO_FILTRO` em todas as chamadas subsequentes ao `/trafego-insights` desta sessão.

### Passo 1. Mostrar menu
```
╔══════════════════════════════════════════════════════════════╗
║  TRÁFEGO ANÁLISE. Análise VTSD de Meta Ads                   ║
╚══════════════════════════════════════════════════════════════╝

Que tipo de análise você quer hoje?

[1]  DIAGNÓSTICO RÁPIDO         visão geral em 60 segundos
                                queima de dinheiro, fadiga, gasto vs anterior

[2]  PERFORMANCE & FUNIL        ranking ROAS, comparativo CPM,
                                posicionamento (Feed/Stories/Reels), funil completo

[3]  CRIATIVOS & COPY           formato (estático/vídeo/carrossel),
                                tier S/A/B/C/D, fadiga, Mandala VTSD 18 tipos

[4]  GEO & DEMOGRAFIA           idade, gênero, público mais barato (por venda),
                                investimento e eficiência de clique por estado

[5]  TIMING & SAZONALIDADE      mês a mês, dia da semana, horário,
                                datas comemorativas, fim de semana

[6]  INVESTIGAÇÃO PROFUNDA      primeiras 24h vs depois do aprendizado,
                                dispositivo, tempo de vídeo, taxa de rejeição

[7]  LIFECYCLE & HISTÓRICO      campanhas com mais de 60 dias, evolução do CPA,
                                melhor mês de todos, candidatos a reativar

[8]  PROBLEMAS OCULTOS          ad sets quebrados, audiências micro,
                                anúncios desaprovados, pixel sem atividade

[9]  ORÇAMENTO & PROJEÇÃO       projeção até o fim do mês, candidatos a
                                escala, redistribuição de budget

[10] COMPARATIVO A x B          confronta duas campanhas lado a lado,
                                qual vence em cada etapa do funil, qual escalar

[11] descrever em texto livre o que precisa
```

### Passo 2. Aluno escolhe UM output
Aguardar escolha. Aceitar número (1 a 11) ou descrição livre. Se descrição livre, identificar qual output melhor cobre e confirmar antes de prosseguir.

### Passo 3. Pergunta período
```
Qual período da análise?

[1] últimos 7 dias
[2] últimos 14 dias
[3] últimos 30 dias
[4] customizado (você informa data início e fim)
```

### Passo 4. Buscar dados (o caminho depende do modo, ver Passo 0.2)

🔍 Próximo passo: buscar as métricas da conta. Tempo estimado: cerca de 30 a 60 segundos.

> **Roteamento obrigatório por `META_AUTH_MODO`** (ver também o **Contrato anti-erros** no Passo 0.2):
> - **`MCP_CONECTOR`:** **não usar os scripts Python nem `curl`.** Buscar métricas por campanha via `ads_get_ad_entities` (com whitelist de campos do **dicionário MCP** + `limit`; se o retorno for salvo em arquivo, processar com python/jq). **Não usar `ads_insights_performance_trend` para ranking/funil**: ela só faz tendência e não tem nível campanha. Aplicar o `STATUS_FILTRO` e o `ESCOPO_FILTRO` cruzando com `CAMPANHAS_SESSAO`. Se um dado não vier pela tool, avisar o aluno e seguir sem ele (nunca inventar).
> - **`APP`:** usar o par de scripts Python abaixo (busca + cache com `FB_ACCESS_TOKEN_PERMANENTE`), ou o `curl` Graph API direto nas chamadas extras das sub-skills.

O restante desta seção descreve o **caminho `APP`** (scripts Python). No `APP`, **nunca usar `curl` diretamente** para a busca principal: o quoting de arrays JSON (`["ACTIVE"]`) é instável no shell (Windows e Mac) e o endpoint `/insights` não aceita `effective_status`. Por isso a busca passa pelo par de scripts abaixo.

**Script 1. Fetch (busca e cache), modo APP:**

```bash
{PY} .claude/skills/trafego-analise/scripts/trafego_fetch.py \
  --account {AD_ACCOUNT_ID_ATUAL} \
  --filtro "{ESCOPO_FILTRO_TEXTO}" \
  --periodo {PERIODO} \
  --status "{STATUS_FILTRO_LISTA}" \
  --output {SLUG_OUTPUT} \
  --project-root . \
  --cache-dir skill-analise/cache
```

`{STATUS_FILTRO_LISTA}` é o valor da coluna "Valor de `--status`" da tabela do Passo 0.55. `{AD_ACCOUNT_ID_ATUAL}` pode ir com ou sem o prefixo `act_` (o script normaliza).

Faz 6 chamadas em sequência, com retry em rate limit: **(0)** lista as campanhas com `effective_status` aplicado e guarda os IDs permitidos (já filtrados pelo nome), **(1a)** métricas do período, **(1b)** janela anterior do mesmo tamanho (WoW), **(1c)** orçamentos (reaproveita a lista da Chamada 0), **(1d)** gasto de hoje e **(1e)** série diária (`time_increment=1`) para o gráfico de tendência. Todas as chamadas de `/insights` são filtradas pelos IDs permitidos. Salva em `skill-analise/cache/` (pasta ignorada pelo git). O nome do cache inclui o slug do status (ex: `_apw_` para `ACTIVE,PAUSED,WITH_ISSUES`) para não colidir entre filtros diferentes. Em chamadas seguintes da mesma sessão, reutiliza o cache sem chamar a API (use `--force` para buscar de novo).

**Script 2. Processar (KPIs e sinais):**

```bash
{PY} .claude/skills/trafego-analise/scripts/trafego_processar.py \
  --account {AD_ACCOUNT_ID_ATUAL} \
  --filtro "{ESCOPO_FILTRO_TEXTO}" \
  --periodo {PERIODO} \
  --status "{STATUS_FILTRO_LISTA}" \
  --output {SLUG_OUTPUT} \
  --cache-dir skill-analise/cache \
  --ticket {PRECO_DO_PRODUTO}
```

Passar os **mesmos** `--account`, `--filtro`, `--periodo`, `--status` e `--output` do fetch: o nome do cache é montado com a mesma regra nos dois scripts. Alternativa: passar `--cache-file` com o caminho que o fetch devolveu em `_cache_file`. `{PRECO_DO_PRODUTO}` vem do `resumo-produto.md` (Passo 0.1).

Lê o cache e calcula: ROAS, CPA, connect rate (`landing_page_view / link_click`), Health Score (5 dimensões), queimadoras (top 5), fadiga, saturação, alertas de budget, comparativo WoW (1a inteiro contra 1b inteiro) e a série diária com a geometria SVG pronta (`serie_diaria_svg`). Saída JSON estruturada via stdout UTF-8.

**Erros que esses scripts eliminam:**
- `UnicodeEncodeError` no Windows: `sys.stdout.buffer.write(...encode('utf-8'))` em vez de `print()`
- HTTP 400 por `landing_page_views` no `fields`: o campo fica dentro de `actions` como `landing_page_view`
- Rate limit por múltiplas chamadas: um processo, chamadas sequenciais com retry
- `effective_status` no `/insights`: válido só em `/campaigns`, nunca em `/insights` (por isso a Chamada 0)
- Connect Rate errado: usa `link_click` (outbound), não `clicks` (total incluindo engajamento no post)
- WoW falso: compara o período inteiro com a janela anterior inteira, sem fatiar a janela anterior ao meio

### Passo 5. Lê o sub-skill correspondente
Ler `sub-skills/{N}-{nome}.md` e executar o protocolo daquele output específico.

### Passo 6. Entrega análise narrada
Aplicar protocolo padrão (Diagnóstico → Causa provável → No VTSD isso significa → Ação recomendada). Se ação exige execução, apontar para a skill executora certa.

### Passo 7. Pergunta o que fazer a seguir (dashboard + próximo output em uma só pergunta)

Após entregar a análise narrada, sempre apresentar as opções em uma única mensagem:

```
O que quer fazer agora?

[1]  Ver meus números no dashboard
[2]  Rodar outra análise: digite o número (1 a 11)
[3]  Encerrar
```

**Se escolher [1]. Dashboard:**
Seguir o fluxo do `/trafego-dashboard` (`.claude/commands/trafego-dashboard.md`) desde o início: se o aluno já tem dashboard ao vivo, entrega o link; se não tem, cria (com o conector MCP da Meta). Quando o caminho for o legado (sem MCP ou sem a ferramenta de artefato), o dashboard estático é a fotografia desta análise: acionar `sub-skills/_export-html.md`, que gera o arquivo em `meus-produtos/{ativo}/trafego/analise/{slug-output}-{YYYY-MM-DD-HHMM}.html`, atualiza o painel de entregas do produto e abre no navegador, e devolver o caminho absoluto. Depois perguntar se quer rodar outra análise ou encerrar (opções [2] e [3] acima).

**Se o aluno pedir para salvar ESTA análise como relatório** (ex.: "salva essa análise", "quero o HTML dessa análise", "gera o relatório com gráficos"): acionar `sub-skills/_export-html.md` direto, em qualquer modo (o export não toca a API).

> **Regra dura do export (não negociável):** seguir o **Contrato de export (seção 0 do `_export-html.md`)**. O HTML SEMPRE usa o design system oficial (esqueleto 3.1 + tokens 3.2 no tema escolhido pelo aluno: Escuro, Terra ou Claro Neutro, controlado por `EXPORT_TEMA` no `.env`; `.topbar`, `.snap-warn`) e SEMPRE renderiza os **gráficos SVG obrigatórios** declarados na sub-skill do output (radar, funil, WoW, linha de tendência etc.), gerando a geometria com `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py` (roda em qualquer modo, sem token). **Proibido inventar HTML/tema próprio ou entregar dashboard sem gráfico.** Antes de anunciar "snapshot salvo", rodar o gate de conformidade (passo 10b do `_export-html.md`): se `svg=0`/`chart-card=0`/`topbar=0`/`tema=0`/`bgok=0`, refazer.

**Se escolher [2]. Outra análise:**
Aceitar o número do output (1 a 11) digitado junto ou na mensagem seguinte. Retornar ao Passo 3 (período) mantendo conta, status e escopo já definidos.

**Se escolher [3] ou "não" / "encerrar":**
Encerrar sem perguntar mais nada.

**Regras desta etapa:**
- Nunca usar o termo "HTML" na pergunta. O aluno vê "dashboard", não detalhes técnicos.
- Nunca pular esta pergunta. Ela é obrigatória após cada análise entregue.
- Se o aluno responder com um número entre 1 e 11 sem escolher [1] explicitamente, interpretar como escolha de novo output (opção [2]).

---

## Roteamento por output

Cada escolha do menu carrega um sub-skill específico. Dependências de breakdowns também declaradas:

| Escolha | Sub-skill | Breakdowns que pede ao /trafego-insights |
|---|---|---|
| [1] Diagnóstico Rápido | `sub-skills/1-diagnostico-rapido.md` | base (sem breakdown) + série diária |
| [2] Performance & Funil | `sub-skills/2-performance-funil.md` | base + `publisher_platform`, `platform_position` |
| [3] Criativos & Copy | `sub-skills/3-criativos.md` | base + `publisher_platform` |
| [4] Geo & Demografia | `sub-skills/4-geo-demografia.md` | `age,gender` (traz venda), `region` = estado (só gasto e clique, **sem venda por região**); cidade/`dma` indisponível para o Brasil |
| [5] Timing & Sazonalidade | `sub-skills/5-timing-sazonalidade.md` | `hourly_stats_aggregated_by_advertiser_time_zone` + base por dia |
| [6] Investigação Profunda | `sub-skills/6-investigacao-profunda.md` | `device_platform`, `impression_device`, `publisher_platform` |
| [7] Lifecycle & Histórico | `sub-skills/7-lifecycle-historico.md` | base por mês x 6 meses (`historico_mensal`) |
| [8] Problemas Ocultos | `sub-skills/8-problemas-ocultos.md` | base + diagnóstico de pixel (aprofundado via `/trafego-pixel`) |
| [9] Orçamento & Projeção | `sub-skills/9-orcamento-projecao.md` | base |
| [10] Comparativo A x B | `sub-skills/10-comparativo.md` | base por campanha + métricas de vídeo (`video_p25/p50/p75/p95_watched_actions`) |
| [11] Livre | usa o sub-skill mais próximo da intenção identificada | conforme necessidade |

**Sub-skill compartilhada (Passo 7):** `sub-skills/_export-html.md`. Gera HTML standalone do output usando o design system Fluxo Criativo, salvando em `meus-produtos/{ativo}/trafego/analise/`. É o caminho legado do dashboard (acionado pelo `/trafego-dashboard` quando o aluno não usa o conector MCP da Meta) e também o caminho para salvar uma análise como relatório quando o aluno pede.

**Total:** 10 outputs narrativos + 1 sub-skill utilitária de export. Cada output entrega análise completa em uma sessão. Aluno pode rodar quantos quiser em sequência.

---

## Protocolo padrão de cada output

Todo sub-skill entrega obrigatoriamente:

1. **Diagnóstico**: o que os dados revelam objetivamente.
2. **Causa provável**: por que está acontecendo (hipótese baseada em padrões VTSD).
3. **No VTSD, isso significa…**: interpretação dentro do método (qual elemento da metodologia está em jogo).
4. **Ação recomendada**: próximo passo concreto. Se exigir execução, apontar para skill executora:
   - Pausa/ajuste de campanha → `/trafego-otimizar`
   - Escala de winner → `/trafego-escalar`
   - Criar campanha nova → `/trafego-criar-campanha`
   - Criar regra automática ou alerta → `/trafego-regras`
   - Criar audience custom/lookalike → `/trafego-publicos`
   - Diagnóstico aprofundado de pixel → `/trafego-pixel` (instalar o pixel na página: `/pagina-pixel`)
   - Montar teste A/B → `/trafego-testes`
   - Investigação estratégica (hipóteses, falso vencedor) → `/trafego-diagnostico`
   - Por que o criativo não vende, DNA criativo, próximos testes → `/trafego-criativos`
   - Gargalo depois do clique (página, oferta, checkout) → `/trafego-oferta-funil` para o diagnóstico; correção em `/feedback-pagina`, `/feedback-low-ticket`, `/pagina-performance`, `/pagina-checkout`, `/pagina-ajuste`, `/copy-pagina` ou `/lt-pagina`
   - Criativo ou copy novo → `/copy-anuncio`, `/criativo-estatico`, `/mandala-de-anuncios` (vídeo: `/video-heygen`, `/video-remotion`, `/video-editar`)
   - Low ticket com planilha do Gerenciador → `/lt-otimizar`

Quando a análise sugerir texto de anúncio (gancho, headline, CTA, ângulo de Urgência Oculta), aplicar a regra "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md (Manual da Copy + skill `revisora`, de forma invisível) antes de mostrar.

---

## Fonte de Dados

**Opção A. Via `/trafego-insights` (recomendado):**
- Invocar `/trafego-insights` com escopo, período e breakdowns que o output exige.
- A skill consulta cache local em `meus-produtos/{ativo}/trafego/insights/` antes da API.
- Resultado é salvo no cache para próximas chamadas (mesma ou outras skills).

**Opção B. Entrada manual:**
- Solicitar CSV exportado do Gerenciador de Anúncios ou dados colados diretamente.
- Confirmar período: últimos 7, 14 ou 30 dias.

Ao iniciar qualquer output: confirmar a fonte se houver ambiguidade.

---

## Módulo de referência rápida. Health Score (usado no output [1])

Componente do output [1] Diagnóstico Rápido. Detalhes completos no `sub-skills/1-diagnostico-rapido.md`.

### Cálculo do Score (0 a 100)

| Dimensão | Peso | Como medir |
|----------|------|------------|
| Diversidade criativa (cobertura da Mandala VTSD) | 20% | Tipos ativos / 18 tipos totais |
| Saúde de públicos (frequência, temperatura) | 20% | HOT/COLD/SUPERCOLD equilibrados, frequência < 4 |
| Eficiência de funil (etapas acima do threshold) | 25% | Nº de etapas saudáveis / 7 etapas totais |
| Performance financeira (ROAS, CPL vs benchmark) | 25% | Métricas dentro do range ideal |
| Consistência temporal (variação de CPL) | 10% | Desvio < 30% semana a semana |

### Classificação do Score

| Score | Classificação | O que significa |
|-------|--------------|-----------------|
| 85 a 100 | 🟢 Excelente | Conta saudável, foco em escala |
| 70 a 84 | 🟡 Boa | Funcionando bem, otimizações pontuais |
| 50 a 69 | 🟠 Regular | Problemas específicos a resolver antes de escalar |
| 0 a 49 | 🔴 Crítica | Parar escalada, diagnóstico profundo urgente |

---

## O método VTSD aplicado ao tráfego

Cada métrica de tráfego é **o termômetro de um elemento do método**:

| Elemento VTSD | Onde aparece no tráfego |
|---|---|
| **Urgência Oculta** | Hook Rate. Se a dor é ativada, o Hook sobe |
| **Identidade do Produto** | CTR. Se o produto está claro, o CTR responde |
| **Identidade do Consumidor** | CPL por público. Público certo, CPL baixa |
| **Decorados** | Hold Rate. Benefícios percebidos = retenção |
| **Furadeira** | Play-Through Rate. Método claro = assiste até o fim |
| **Oferta** | Offer Rate. Oferta clara = checkout acontece |
| **Quadro na Parede** | Connect Rate. Resultado desejado = venda fecha |
| **Orderbump + Upsell** | LTV Rate. VTSD completo = ticket médio sobe |

Leitura fundamental:
> "Cada métrica que cai indica um elemento do método que está falhando."

---

## Glossário VTSD essencial

| Termo VTSD | Significado no tráfego |
|------------|----------------------|
| **Urgência Oculta** | Dor que o público sente mas não verbaliza. Deve aparecer no hook do criativo |
| **Quadro na Parede** | Resultado final que o produto entrega. Deve estar claro na promessa do anúncio |
| **Furadeira** | Método do produto. Deve ser comunicado na página e nos criativos de meio/fundo |
| **Decorados** | Benefícios percebidos. Aumentam Hold Rate e reduzem abandono de checkout |
| **Identidade do Consumidor** | Público ideal. Define segmentação, temperatura e linguagem dos anúncios |
| **Identidade do Comunicador** | Tom, valores e estilo do criador. Define como a mensagem é dita nos anúncios |
| **Identidade do Produto** | Posicionamento. Define diferencial competitivo e angle dos criativos |
| **Pico de Vendas** | Período de lançamento. Maior concentração de budget em HOT e COLD |
| **Evergreen / Perpétuo** | Funil sempre ativo. Foco em eficiência e CPL/CPA estável |
| **Caixa Rápido** | Produto low ticket de conversão rápida. ROAS mínimo 3x |
| **HOT** | Público quente (engajamento, visualizações de vídeo, lista de leads) |
| **COLD** | Público frio (interesses, lookalike) |
| **SUPERCOLD** | Público aberto (sem segmentação específica) |
| **Mandala** | Sistema de 18 tipos de anúncio. Garante diversidade criativa |

---

## Regras Absolutas

- NUNCA inventar métricas. Se o dado não estiver disponível, informar e pedir.
- SEMPRE usar terminologia VTSD nas análises.
- NUNCA deixar uma análise sem ação recomendada concreta.
- SEMPRE identificar o gargalo principal antes de listar secundários.
- NUNCA usar jargão técnico sem explicar em linguagem do método.
- NUNCA perguntar ao aluno o que já está no `resumo-produto.md` (preço, tipo de produto, público, Quadro, objeções).
- Para ações de execução (pausar, mudar budget, criar regra, criar audience, criar teste), encaminhar para a skill executora correta. Esta skill **narra**, não executa edição.
- Sempre que possível, aproveitar o cache local em `meus-produtos/{ativo}/trafego/insights/` para evitar requisições redundantes à Graph API.
- Um output por vez. Não tentar entregar 3 outputs em uma resposta.
- **Export HTML é opcional e SEMPRE precedido por confirmação explícita do aluno.** Nunca gerar HTML automaticamente. Quando gerado, o arquivo SEMPRE traz banner de "snapshot" no topo com timestamp visível, deixando claro que não é dado ao vivo.
- HTML de export sempre vai para `meus-produtos/{ativo}/trafego/analise/`. Nunca em pasta global, nunca na raiz, nunca sobrescrever (cada export é arquivo novo com timestamp próprio).
