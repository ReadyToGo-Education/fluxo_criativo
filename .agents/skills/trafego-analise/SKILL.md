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

# Tráfego Análise. 9 Outputs Narrativos VTSD

Análise narrada de campanhas Meta Ads pela lente da metodologia VTSD (Venda Todo Santo Dia, Leandro Ladeira). Cada métrica de tráfego é o termômetro de um elemento do método. O propósito é conectar dado → método → decisão, e entregar análise pedagógica que serve tanto para operar quanto para ensinar.

**Diferença vs outras skills de tráfego:**
- `/trafego-insights` é a **fonte de dados** (lê e cacheia, não narra).
- `/trafego-otimizar` é **técnico**, calcula, executa pausa/ajuste de budget. Foca em **operação**.
- `/trafego-escalar` **escala** campanhas validadas com freios.
- `/trafego-analise` **narra** com terminologia VTSD. **Não executa edição.** Quando a análise sugere ação, ela faz handoff para a skill executora correspondente.

---

## Como funcionar

Ao ser invocada, validar conexão Meta, perguntar a conta de anúncios e apresentar o menu. Aguardar escolha antes de pedir período ou dado.

### Passo 0. Validar conexão Meta
Ler `META_AUTH_MODO` no `.env`. Se vazio, acionar `/trafego-conexao` antes de qualquer outra ação.

### Passo 0.5. Selecionar conta de anúncios

Ler `FB_AD_ACCOUNT_IDS` no `.env` (campo com múltiplas contas separadas por vírgula, ex: `1234,5678,9012`). Também ler `FB_AD_ACCOUNT_ID` (conta padrão).

**Se houver apenas uma conta configurada** (`FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS` idênticos ou `FB_AD_ACCOUNT_IDS` vazio): usar automaticamente essa conta e pular a pergunta.

**Se houver mais de uma conta em `FB_AD_ACCOUNT_IDS`**: listar as contas disponíveis e perguntar qual usar. Para obter o nome de todas as contas **em uma única chamada batch**, fazer **uma chamada `Bash(curl ...)` direta** (sem heredoc Python — ver regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md):

Construir a string `act_<id1>,act_<id2>,...` a partir de `FB_AD_ACCOUNT_IDS` e disparar:

```
curl -s "https://graph.facebook.com/v21.0/?ids=act_1234567890,act_0987654321,act_1122334455,act_5566778899&fields=name&access_token=<TOKEN_DO_ENV>"
```

A resposta vem em JSON único:
```json
{
  "act_1234567890": {"name": "Conta A", "id": "act_1234567890"},
  "act_0987654321": {"name": "Conta B", "id": "act_0987654321"},
  ...
}
```

O Claude lê o JSON retornado como texto e monta o menu numerado. **Nunca fazer N chamadas separadas** — uma única chamada batch é o suficiente e conta como 1 contra o rate limit.

**Tratamento de erro:** se a chamada batch falhar, exibir só os IDs sem nome e continuar.

**Ordenação obrigatória:** a conta cujo ID coincide com `FB_AD_ACCOUNT_ID` é a conta padrão e deve sempre aparecer em **primeiro lugar** na lista, com a etiqueta `"padrão"` entre aspas após o nome. As demais contas seguem na ordem em que aparecem em `FB_AD_ACCOUNT_IDS`.

Montar o menu assim:
```
Qual conta de anúncios deseja analisar?

[1] Nome da Conta Padrão "padrão"  (act_1234567890)
[2] Nome da Conta B                (act_0987654321)
[3] Nome da Conta C                (act_1122334455)

Digite o número:
```
Se a chamada de nome falhar para alguma conta, exibir só o ID sem nome. A conta padrão ainda recebe a etiqueta `"padrão"` mesmo sem nome.

**Após a escolha:** definir `CONTA_ATIVA_ID` como variável de sessão (ex: `act_1234567890`). Usar esse ID em todas as chamadas subsequentes à Graph API desta sessão, inclusive ao chamar `/trafego-insights`.

### Passo 0.55. Filtro de status das campanhas

Antes de buscar os grupos, perguntar quais status incluir:

```
Quais campanhas incluir na análise?

[1]  Somente ativas      (ACTIVE — o que está rodando agora)
[2]  Somente pausadas    (PAUSED + WITH_ISSUES — o que está desligado)
[3]  Ativas + pausadas   (visão completa do presente)
[4]  Histórico completo  (inclui arquivadas — análise de longo prazo)
```

Salvar como `STATUS_FILTRO` (variável de sessão) e usar em todas as chamadas subsequentes:

| Escolha | `effective_status` na API |
|---------|--------------------------|
| [1] | `["ACTIVE"]` |
| [2] | `["PAUSED","WITH_ISSUES"]` |
| [3] | `["ACTIVE","PAUSED","WITH_ISSUES"]` |
| [4] | `["ACTIVE","PAUSED","WITH_ISSUES","ARCHIVED"]` |

**Alerta automático para output [8] Problemas Ocultos:** se `STATUS_FILTRO = ["ACTIVE"]` e o aluno escolher o output [8], alertar antes de rodar: "Você está analisando só campanhas ativas. Para ver ad sets quebrados e anúncios pausados por problema, reinicie e escolha [2] ou [3]."

---

### Passo 0.6. Identificar escopo de análise

Após definir `CONTA_ATIVA_ID` e `STATUS_FILTRO`, **sempre buscar todas as campanhas da conta** com o status escolhido — sem pré-filtrar por nome:

```
GET /act_{CONTA_ATIVA_ID}/campaigns
  ?fields=id,name,objective,status
  &effective_status={STATUS_FILTRO}
  &limit=200
  &access_token={token}
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

#### Opção [1] — Por nomenclatura

Perguntar:
```
Qual é o formato do nome das suas campanhas?
(ex: "PRODUTO - FUNIL - NOME DA CAMPANHA", "[PRODUTO][FUNIL] Nome")
```

Com o padrão informado, parsear todos os nomes em `CAMPANHAS_SESSAO` e extrair os segmentos. Agrupar pelo **primeiro segmento** (produto/marca). Montar menu:

```
Grupos encontrados pela nomenclatura "{padrão informado}":

[1]  VTSD                  38 campanhas
[2]  FX                    10 campanhas
[3]  NEWS                   2 campanhas
[4]  Todas as campanhas    50 campanhas (sem filtro de grupo)

Com qual grupo quer trabalhar?
```

Se nenhuma campanha bater com o padrão, informar: "Não consegui identificar grupos com esse padrão. Posso tentar automaticamente ou você prefere ver todas juntas?" — e oferecer as opções [3] e "Todas".

---

#### Opção [2] — Filtro personalizado

Perguntar:
```
Digite o trecho do nome, palavra-chave ou IDs de campanha que quer analisar:
(ex: "remarketing", "VSL", "120245199262", "VTSD - RMK")
```

Filtrar `CAMPANHAS_SESSAO` pelo texto informado (busca por substring, case-insensitive). Mostrar quantas campanhas foram encontradas e confirmar antes de prosseguir. Salvar como `ESCOPO_FILTRO = nome_contém:{texto}`.

---

#### Opção [3] — Sem padrão definido (auto-detecção)

Analisar `CAMPANHAS_SESSAO` e tentar agrupar por:
1. **Prefixos comuns** — sequências antes do primeiro espaço, hífen ou colchete. Prefixo com 2+ campanhas vira grupo.
2. **Objetivo Meta** — quando prefixos se confundem, agrupar por `objective` (`OUTCOME_SALES`, `OUTCOME_LEADS`, `LINK_CLICKS`, `OUTCOME_AWARENESS`).
3. **Palavras-chave recorrentes** — `RMK`, `CV`, `LEAD`, `ENGAJAMENTO`, `PUBLICO`.

Apresentar os grupos encontrados + sempre incluir "Todas as campanhas" como última opção:

```
Identifiquei os seguintes grupos (detecção automática):

[1]  VTSD — produto principal     46 campanhas · OUTCOME_SALES
[2]  FX — captação leads          10 campanhas · OUTCOME_LEADS
[3]  Publicações Instagram        20 campanhas · LINK_CLICKS
[4]  NEWS — newsletter             2 campanhas · OUTCOME_LEADS
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
- Grupo específico: `ESCOPO_FILTRO = nome_contém:{prefixo/texto}` — usado para filtrar em Python ao processar insights, não na API.
- "Todas as campanhas" / sem filtro: `ESCOPO_FILTRO = conta_completa`.
- IDs específicos: `ESCOPO_FILTRO = ids:{id1,id2,...}`.

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

[4]  GEO & DEMOGRAFIA           estado, cidade, idade, gênero,
                                capital vs interior, público mais barato

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
Aguardar escolha. Aceitar número (1 a 11) ou descrição livre. Se descrição livre, identificar qual output melhor cobre.

### Passo 3. Pergunta período
```
Qual período da análise?

[1] últimos 7 dias
[2] últimos 14 dias
[3] últimos 30 dias
[4] customizado (você informa data início e fim)
```

### Passo 4. Buscar dados via scripts Python (padrão obrigatório)

**Nunca usar `curl` diretamente.** O quoting de arrays JSON (`["ACTIVE"]`) é instável no shell (Windows e Mac). O endpoint `/insights` não aceita `effective_status`. Toda chamada à Graph API passa pelo par de scripts abaixo.

**Script 1 — fetch (busca e cache):**

```bash
python3 .claude/skills/trafego-analise/scripts/trafego_fetch.py \
  --account {CONTA_ATIVA_ID} \
  --filtro "{ESCOPO_FILTRO_TEXTO}" \
  --periodo {PERIODO} \
  --status "{STATUS_FILTRO_LISTA}" \
  --output {SLUG_OUTPUT} \
  --project-root . \
  --cache-dir skill-analise/cache
```

**Mapeamento de `--status` a partir do `STATUS_FILTRO` escolhido no Passo 0.55:**

| Escolha do Passo 0.55 | Valor de `--status` |
|---|---|
| [1] Somente ativas | `ACTIVE` |
| [2] Somente pausadas | `PAUSED,WITH_ISSUES` |
| [3] Ativas + pausadas | `ACTIVE,PAUSED,WITH_ISSUES` |
| [4] Histórico completo | `ACTIVE,PAUSED,WITH_ISSUES,ARCHIVED` |

Se o aluno não passou pelo Passo 0.55 (ex: chamada direta sem menu), default do script é `ACTIVE,PAUSED,WITH_ISSUES`.

Faz 5 chamadas em sequência: (0) lista IDs de campanhas com `effective_status` aplicado, (1a) métricas do período filtradas pelos IDs permitidos, (1b) comparativo WoW com mesmo filtro, (1c) reusa lista da Chamada 0 (orçamentos), (1d) gasto de hoje com mesmo filtro. Tudo com retry em rate limit. Salva em `skill-analise/cache/`. O nome do cache inclui slug do status (ex: `_apw_` para `ACTIVE,PAUSED,WITH_ISSUES`) pra evitar colisão entre filtros diferentes.

**Script 2 — processar (KPIs e sinais):**

```bash
python3 .claude/skills/trafego-analise/scripts/trafego_processar.py \
  --account {CONTA_ATIVA_ID} \
  --filtro "{ESCOPO_FILTRO_TEXTO}" \
  --periodo {PERIODO} \
  --output {SLUG_OUTPUT} \
  --cache-dir skill-analise/cache \
  --ticket {PRECO_DO_PRODUTO}
```

Lê o cache e calcula: ROAS, CPA, connect rate (`landing_page_view / link_click`), Health Score (5 dimensões), queimadoras (top 5), fadiga, saturação, alertas de budget. Saída JSON estruturada via stdout UTF-8.

**Erros que esses scripts eliminam:**
- `UnicodeEncodeError` no Windows: `sys.stdout.buffer.write(...encode('utf-8'))` em vez de `print()`
- HTTP 400 por `landing_page_views` no topo: o campo fica dentro de `actions` como `landing_page_view`
- Rate limit por múltiplas chamadas: um processo, quatro chamadas sequenciais com retry
- `effective_status` no `/insights`: válido só em `/campaigns`, nunca em `/insights`
- Connect Rate errado: usa `link_click` (outbound), não `clicks` (total incluindo engajamento no post)

### Passo 5. Lê o sub-skill correspondente
Ler `sub-skills/{N}-{nome}.md` e executar o protocolo daquele output específico.

### Passo 6. Entrega análise narrada
Aplicar protocolo padrão (Diagnóstico → Causa provável → No VTSD isso significa → Ação recomendada). Se ação exige execução, apontar para a skill executora certa.

### Passo 7. Pergunta o que fazer a seguir (dashboard + próximo output em uma só pergunta)

Após entregar a análise narrada, sempre apresentar as opções em uma única mensagem:

```
O que quer fazer agora?

[1]  Salvar como dashboard com os dados desta análise
[2]  Rodar outra análise  — digite o número (1 a 11)
[3]  Encerrar
```

**Se escolher [1] — Dashboard:**
Acionar `sub-skills/_export-html.md`, que gera o arquivo em `meus-produtos/{ativo}/trafego/analise/{slug-output}-{YYYY-MM-DD-HHMM}.html` e abre no navegador. Devolver o caminho absoluto. Depois perguntar se quer rodar outra análise ou encerrar (opções [2] e [3] acima).

**Se escolher [2] — Outra análise:**
Aceitar o número do output (1 a 11) digitado junto ou na mensagem seguinte. Retornar ao Passo 3 (período) mantendo conta e escopo já definidos.

**Se escolher [3] ou "não" / "encerrar":**
Encerrar sem perguntar mais nada.

**Regras desta etapa:**
- Nunca usar o termo "HTML" na pergunta. O aluno vê "dashboard com os dados", não detalhes técnicos.
- Nunca pular esta pergunta. Ela é obrigatória após cada análise entregue.
- Se o aluno responder com um número entre 1 e 11 sem escolher [1] explicitamente, interpretar como escolha de novo output (opção [2]).

---

## Roteamento por output

Cada escolha do menu carrega um sub-skill específico. Dependências de breakdowns também declaradas:

| Escolha | Sub-skill | Breakdowns que pede ao /trafego-insights |
|---|---|---|
| [1] Diagnóstico Rápido | `sub-skills/1-diagnostico-rapido.md` | base (sem breakdown) |
| [2] Performance & Funil | `sub-skills/2-performance-funil.md` | base + `publisher_platform`, `platform_position` |
| [3] Criativos & Copy | `sub-skills/3-criativos.md` | base + `publisher_platform` |
| [4] Geo & Demografia | `sub-skills/4-geo-demografia.md` | `age,gender`, `country`, `region`, `dma` |
| [5] Timing & Sazonalidade | `sub-skills/5-timing-sazonalidade.md` | `hourly_stats_aggregated_by_advertiser_time_zone` + base por dia |
| [6] Investigação Profunda | `sub-skills/6-investigacao-profunda.md` | `device_platform`, `impression_device`, `publisher_platform` |
| [7] Lifecycle & Histórico | `sub-skills/7-lifecycle-historico.md` | base por mês x 6 meses (`historico_mensal`) |
| [8] Problemas Ocultos | `sub-skills/8-problemas-ocultos.md` | base + diagnóstico de pixel (endpoint `/adspixels` direto) |
| [9] Orçamento & Projeção | `sub-skills/9-orcamento-projecao.md` | base |
| [10] Comparativo A x B | `sub-skills/10-comparativo.md` | base por campanha + métricas de vídeo (`video_p25/p50/p75/p95_watched_actions`) |
| [11] Livre | usa o sub-skill mais próximo da intenção identificada | conforme necessidade |

**Sub-skill compartilhada (Passo 6.5):** `sub-skills/_export-html.md` — gera HTML standalone do output usando o design system Fluxo Criativo, salvando em `meus-produtos/{ativo}/trafego/analise/`. Acionada apenas quando o aluno confirma o export.

**Total:** 10 outputs narrativos + 1 sub-skill utilitária de export. Cada output entrega análise completa em uma sessão. Aluno pode rodar quantos quiser em sequência.

---

## Protocolo padrão de cada output

Todo sub-skill entrega obrigatoriamente:

1. **Diagnóstico** — o que os dados revelam objetivamente.
2. **Causa provável** — por que está acontecendo (hipótese baseada em padrões VTSD).
3. **No VTSD, isso significa…** — interpretação dentro do método (qual elemento da metodologia está em jogo).
4. **Ação recomendada** — próximo passo concreto. Se exigir execução, apontar para skill executora:
   - Pausa/ajuste de campanha → `/trafego-otimizar`
   - Escala de winner → `/trafego-escalar`
   - Criar campanha nova → `/trafego-criar-campanha`

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
| **HOT** | Público quente (engajamento, video views, lista de leads) |
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
- Para ações de execução (pausar, mudar budget, criar regra, criar audience, criar teste), encaminhar para a skill executora correta. Esta skill **narra**, não executa edição.
- Sempre que possível, aproveitar o cache local em `meus-produtos/{ativo}/trafego/insights/` para evitar requisições redundantes à Graph API.
- Um output por vez. Não tentar entregar 3 outputs em uma resposta.
- **Export HTML é opcional e SEMPRE precedido por confirmação explícita do aluno.** Nunca gerar HTML automaticamente. Quando gerado, o arquivo SEMPRE traz banner de "snapshot" no topo com timestamp visível, deixando claro que não é dado live.
- HTML de export sempre vai para `meus-produtos/{ativo}/trafego/analise/`. Nunca em pasta global, nunca na raiz, nunca sobrescrever (cada export é arquivo novo com timestamp próprio).
