---
name: workshop-marketing:trafego-analise
description: Análise narrada de tráfego pago Meta Ads com terminologia VTSD (Mandala 18 tipos, Urgência Oculta, Quadro na Parede, Furadeira, Decorados, 3 Identidades, HOT/COLD/SUPERCOLD, Caixa Rápido, Pico vs Evergreen). 10 outputs narrativos: Diagnóstico Rápido, Performance & Funil, Criativos & Copy, Geo & Demografia, Timing & Sazonalidade, Investigação Profunda, Lifecycle & Histórico, Problemas Ocultos, Orçamento & Projeção, Comparativo A x B. Busca os dados pelo conector MCP da Meta (padrão) ou pela Graph API (modo App). Cada output entrega diagnóstico, causa provável, interpretação VTSD e ação recomendada com handoff para skill executora.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Tráfego Análise. Análise VTSD de Meta Ads

Análise narrada de campanhas Meta Ads pela lente da metodologia VTSD (Venda Todo Santo Dia, Leandro Ladeira). Cada métrica é o termômetro de um elemento do método: dado → método → decisão.

Esta skill **narra**, não executa edição. Quando a análise sugere ação, faz handoff para a skill executora correspondente.

A especificação completa (contrato anti-erros por modo, escopo das campanhas, scripts e regras de export) está em `.claude/skills/trafego-analise/SKILL.md`. Este command é o roteiro com o aluno.

---

## Passo 0. Contexto e conexão Meta

### 0.1 Produto ativo
Seguir a seção "Contexto Persistente do Negócio" do CLAUDE.md:

1. Ler `meus-produtos/.ativo`. Se não existir, orientar o aluno a usar `/produto-novo` primeiro.
2. Ler `meus-produtos/{ativo}/resumo-produto.md` direto, sem conferir antes se ele existe.
   - Se não for encontrado e o `perfil.md` tiver o Quadro preenchido: anunciar `⏳ Preparando o resumo do seu produto (só na primeira vez).`, acionar o agente `gerador-resumo-produto` com o slug do produto e ler o resumo gravado. Sem acesso a agentes, gerar o resumo seguindo a seção 3 de `.claude/skills/resumo-produto/SKILL.md` e gravar no mesmo caminho.
   - Se nem o `perfil.md` existir (ou estiver sem Quadro): orientar `/produto-concepcao` primeiro.
3. Preço, tipo de produto (low, middle ou high ticket), público, Quadro, Furadeira, Decorados, Urgências Ocultas e objeções saem do resumo. Não perguntar de novo ao aluno o que o resumo já tem.

### 0.2 Conexão Meta (gate duro)
Ler `META_AUTH_MODO` no `.env`.

- **Se vazio ou ausente:** acionar `/trafego-conexao` antes de prosseguir.
- **Se `MCP_CONECTOR`** (padrão): confirmar que pelo menos uma tool terminada em `ads_get_ad_entities` está disponível (o prefixo do servidor varia). Se nenhuma, pedir ao aluno para reabrir o Claude Code; se persistir, voltar ao `/trafego-conexao`.
- **Se `APP`** (reserva): confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem no `.env` (checar presença com `grep -q`, nunca `cat .env`). Se faltar algum, acionar `/trafego-conexao`.

**Conta não liberada no MCP:** se a tool responder `is_ads_mcp_enabled: false` ou o erro "Ads MCP is gradually being rolled out", explicar em linguagem simples que a Meta ainda não liberou o conector para essa conta de anúncios e oferecer trocar para o modo App pelo `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

**Interpretador Python:** nos comandos abaixo, `{PY}` é o interpretador detectado na sessão (`python3` ou `py -3`), conforme a seção "Execução de Scripts Python" do CLAUDE.md.

---

## Passo 1. Menu de outputs

Apresentar o menu imediatamente após validar a conexão:

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

[10] COMPARATIVO A x B          duas campanhas lado a lado: spend, CPA/CPL,
                                connect rate, hook rate, funil completo

[11] descrever em texto livre o que precisa
```

Se o aluno descreveu em texto livre, mapear para o output mais próximo e confirmar antes de prosseguir.

---

## Passo 2. Conta de anúncios (multi-conta)

1. Ler `FB_AD_ACCOUNT_IDS` no `.env` (lista separada por vírgula).
2. Se ausente ou com exatamente 1 ID, usar `FB_AD_ACCOUNT_ID` direto, sem perguntar.
3. Se 2 ou mais IDs, buscar nomes amigáveis:

   **Modo MCP_CONECTOR:** usar a tool terminada em `ads_get_ad_accounts`.

   **Modo APP:**
   ```bash
   curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name&limit=100&access_token={FB_ACCESS_TOKEN_PERMANENTE}"
   ```

   Filtrar apenas as IDs que estão em `FB_AD_ACCOUNT_IDS`. Marcar como "padrão" a que está em `FB_AD_ACCOUNT_ID`. Apresentar menu numerado e aguardar escolha.

4. Salvar a conta escolhida em `AD_ACCOUNT_ID_ATUAL` (variável local da execução, nunca sobrescreve `.env`).

---

## Passo 2.5. Filtro de status das campanhas

```
Quais campanhas incluir na análise?

[1]  Somente ativas      (ACTIVE: o que está rodando agora)
[2]  Somente pausadas    (PAUSED + WITH_ISSUES: o que está desligado)
[3]  Ativas + pausadas   (visão completa do presente)
[4]  Histórico completo  (inclui arquivadas: análise de longo prazo)
```

Salvar como `STATUS_FILTRO` (variável local da execução) e usar em todas as chamadas desta sessão:

| Escolha | `effective_status` na listagem | `--status` nos scripts (modo APP) |
|---------|-------------------------------|-----------------------------------|
| [1] | `["ACTIVE"]` | `ACTIVE` |
| [2] | `["PAUSED","WITH_ISSUES"]` | `PAUSED,WITH_ISSUES` |
| [3] | `["ACTIVE","PAUSED","WITH_ISSUES"]` | `ACTIVE,PAUSED,WITH_ISSUES` |
| [4] | `["ACTIVE","PAUSED","WITH_ISSUES","ARCHIVED"]` | `ACTIVE,PAUSED,WITH_ISSUES,ARCHIVED` |

`effective_status` só vale em `/campaigns`, `/adsets` e `/ads`. O `/insights` não aceita esse parâmetro: o filtro é feito cruzando os IDs da listagem com o retorno do `/insights` (no modo APP, o `trafego_fetch.py` faz isso sozinho quando recebe `--status`).

**Alerta automático para output [8] Problemas Ocultos:** se `STATUS_FILTRO = ["ACTIVE"]` e o aluno escolher o output [8], alertar antes de rodar: "Você está analisando só campanhas ativas. Para ver ad sets quebrados e anúncios pausados por problema, reinicie e escolha [2] ou [3]."

---

## Passo 2.6. Escopo das campanhas

Seguir o Passo 0.6 do `SKILL.md`: listar todas as campanhas com o status escolhido, perguntar como o aluno nomeia as campanhas (nomenclatura, filtro personalizado ou detecção automática) e definir `ESCOPO_FILTRO`.

---

## Passo 3. Período

```
Qual período da análise?

[1] últimos 7 dias
[2] últimos 14 dias
[3] últimos 30 dias
[4] customizado (informe data início e fim: YYYY-MM-DD a YYYY-MM-DD)
```

| Opção | Parâmetro na API |
|-------|-----------------|
| 1 | `date_preset=last_7d` |
| 2 | `date_preset=last_14d` |
| 3 | `date_preset=last_30d` |
| 4 | `time_range={"since":"YYYY-MM-DD","until":"YYYY-MM-DD"}` |

**Exceção:** output [7] Lifecycle & Histórico ignora esta escolha e sempre usa `time_range` de 6 meses atrás até hoje com `time_increment=monthly`.

---

## Passo 4. Buscar os dados

🔍 Próximo passo: buscar as métricas da conta. Tempo estimado: cerca de 30 a 60 segundos.

**Roteamento por modo** (detalhes no "Contrato anti-erros" do `SKILL.md`):

- **`MCP_CONECTOR`:** sem token e sem os scripts. Métricas por campanha, conjunto ou anúncio via tool terminada em `ads_get_ad_entities`, com whitelist de campos do dicionário do MCP (não aceita `actions`/`action_values`/`outbound_clicks`; usar `purchase_roas`, `actions:omni_purchase`, `actions:link_click`, `cost_per_result` etc.) e `limit` explícito. `ads_insights_performance_trend` só serve para tendência temporal (não tem nível campanha nem serve para ranking ou funil). Se um dado não vier pela tool, avisar o aluno e seguir sem ele.
- **`APP`:** a busca base (métricas do período, janela anterior, orçamentos, gasto de hoje e série diária) passa pelo par de scripts do Passo 4 do `SKILL.md`, sempre com `--status`:

  ```bash
  {PY} .claude/skills/trafego-analise/scripts/trafego_fetch.py --account {AD_ACCOUNT_ID_ATUAL} --filtro "{ESCOPO_FILTRO_TEXTO}" --periodo {PERIODO} --status "{STATUS_FILTRO_LISTA}" --output {SLUG_OUTPUT} --project-root . --cache-dir skill-analise/cache
  {PY} .claude/skills/trafego-analise/scripts/trafego_processar.py --account {AD_ACCOUNT_ID_ATUAL} --filtro "{ESCOPO_FILTRO_TEXTO}" --periodo {PERIODO} --status "{STATUS_FILTRO_LISTA}" --output {SLUG_OUTPUT} --cache-dir skill-analise/cache --ticket {PRECO_DO_PRODUTO}
  ```

  As chamadas extras de cada output (breakdowns, listagens) vão por `curl` direto, uma chamada `Bash(curl ...)` por vez, conforme a regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" do CLAUDE.md. Nunca exibir o `curl` com o token no chat.

### Campos base (modo APP)

```
spend,impressions,clicks,ctr,cpm,cpc,reach,frequency,
actions,action_values,cost_per_action_type,
video_play_actions,video_avg_time_watched_actions,
video_p25_watched_actions,video_p50_watched_actions,
video_p75_watched_actions,video_p95_watched_actions
```

`landing_page_views` nunca vai no `fields` (erro 400): o valor vem dentro de `actions` como `landing_page_view`.

### Parâmetros por output

> **Esta tabela é o ponto de partida, não o teto.** Cada sub-skill pode e deve fazer chamadas adicionais sempre que o contexto da análise exigir dados não listados aqui. O critério é simples: o dado é necessário para responder uma pergunta do output? Se sim, buscar. Consultar `sub-skills/{N}-{nome}.md` para a lista exata de chamadas de cada output.

| Output | level | breakdowns | chamadas mínimas (a sub-skill pode adicionar mais) |
|--------|-------|------------|-----------------|
| [1] Diagnóstico Rápido | campaign | sem breakdown | série diária (`time_increment=1`) para o gráfico de tendência |
| [2] Performance & Funil | campaign + ad | publisher_platform, platform_position | + 2ª chamada com período anterior equivalente para comparativo de CPM/ROAS |
| [3] Criativos & Copy | ad | publisher_platform | + buscar `name`, `creative` dos ads; + chamada WoW com `time_increment=7` |
| [4] Geo & Demografia | ad | age,gender | + 2ª chamada: region; + 3ª chamada: country |
| [5] Timing & Sazonalidade | campaign | hourly_stats_aggregated_by_advertiser_time_zone | + chamada diária com `time_increment=1`; + chamada mensal com `last_180d` e `time_increment=monthly` |
| [6] Investigação Profunda | ad | device_platform, impression_device, publisher_platform | + chamada com `time_increment=1` e `since/until` dos primeiros dias de cada campanha (análise das primeiras 24h) |
| [7] Lifecycle & Histórico | campaign | sem breakdown | + chamada com `time_range` 6 meses e `time_increment=monthly`; + listagem com `start_time` e `updated_time`; + listagem de campanhas `PAUSED`/`ARCHIVED` cruzada com o `/insights` |
| [8] Problemas Ocultos | adset + ad | sem breakdown | + ad sets `WITH_ISSUES/LIMITED`; + ads `DISAPPROVED/WITH_ISSUES`; + audiences (`approximate_count_lower_bound/upper_bound`); + estado do pixel; + budget por adset (ABO); diagnóstico aprofundado de pixel via `/trafego-pixel` |
| [9] Orçamento & Projeção | campaign | sem breakdown | + `daily_budget/lifetime_budget/spend_cap` das campanhas; + `daily_budget` dos adsets quando conta usa ABO |
| [10] Comparativo A x B | campaign + ad (por campanha) | sem breakdown | 2 chamadas separadas por `campaign_id` + métricas derivadas (connect rate, hook rate, funil completo por campanha) |

### Regra obrigatória de deduplicação de conversões

> Esta regra se aplica a TODOS os outputs. Violar ela causa duplicação silenciosa de compras e receita.

O Meta retorna a mesma conversão em múltiplos `action_type` na mesma resposta. **NUNCA somar tipos que representam o mesmo evento.**

| Métrica | Tipo canônico a usar | Tipos a IGNORAR (duplicatas) |
|---------|---------------------|------------------------------|
| Compras (contagem) | `offsite_conversion.fb_pixel_purchase` | `purchase`, `omni_purchase`, `onsite_web_purchase`, `web_in_store_purchase`, `onsite_web_app_purchase`, `web_app_in_store_purchase`, `offsite_purchase_add_20_s_calls` |
| Receita (valor) | `offsite_conversion.fb_pixel_purchase` (em `action_values`) | todos os outros tipos acima |
| Leads (contagem) | `offsite_conversion.fb_pixel_lead` | `lead`, `onsite_web_lead`, `offsite_lead_add_20_s_calls` |
| Checkouts (contagem) | `offsite_conversion.fb_pixel_initiate_checkout` | `initiate_checkout`, `omni_initiated_checkout`, `onsite_web_initiate_checkout` |
| Adicionar ao carrinho | `offsite_conversion.fb_pixel_add_to_cart` | `add_to_cart`, `omni_add_to_cart`, `onsite_web_add_to_cart`, `onsite_web_app_add_to_cart` |

No modo MCP, a tool `ads_get_ad_entities` entrega as compras em `actions:omni_purchase` (único tipo disponível nela): usar esse campo sozinho, sem somar com outro tipo de compra.

**Conversões customizadas** (`offsite_conversion.custom.*`) têm IDs de pixel específicos: nunca somar com as padrão acima. Verificar se o valor atribuído é plausível antes de incluir em qualquer cálculo de receita (valores de R$ milhões por evento indicam pixel mal configurado).

**Regra prática:** ao iterar sobre `actions` ou `action_values`, filtrar **exatamente** o tipo canônico listado acima. Se o tipo canônico não estiver presente na resposta para uma campanha, assumir zero para aquela campanha. Nunca tentar alternativas da lista de duplicatas como fallback.

### Endpoint base (Modo APP)

```bash
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/insights
  ?fields={CAMPOS_BASE}
  &level={LEVEL}
  &breakdowns={BREAKDOWNS}
  &{PERIOD_PARAM}
  &limit=500
  &access_token={FB_ACCESS_TOKEN_PERMANENTE}"
```

### Chamadas adicionais para output [8] Problemas Ocultos (Modo APP)

```bash
# Ad sets com problemas de entrega
curl -g -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/adsets
  ?fields=id,name,status,effective_status,targeting
  &filtering=[{"field":"effective_status","operator":"IN","value":["WITH_ISSUES","LIMITED"]}]
  &access_token={TOKEN}"

# Anúncios desaprovados ou com restrição
curl -g -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/ads
  ?fields=id,name,status,effective_status,review_feedback
  &filtering=[{"field":"effective_status","operator":"IN","value":["DISAPPROVED","WITH_ISSUES"]}]
  &access_token={TOKEN}"
```

No modo MCP, usar as tools terminadas em `ads_get_ad_entities` (ad sets e anúncios), `ads_get_ad_account_custom_audiences` (audiences) e `ads_get_datasets` (pixels). Para diagnóstico aprofundado de pixel dentro do output [8], acionar `/trafego-pixel` (apenas leitura).

### Chamada extra para output [9] Orçamento & Projeção (Modo APP)

```bash
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/campaigns
  ?fields=id,name,status,daily_budget,lifetime_budget,spend_cap
  &access_token={TOKEN}"
```

---

## Passo 5. Executar análise

Carregar o sub-skill correspondente e executar o protocolo com os dados obtidos no Passo 4:

| Output | Sub-skill |
|--------|-----------|
| [1] | `.claude/skills/trafego-analise/sub-skills/1-diagnostico-rapido.md` |
| [2] | `.claude/skills/trafego-analise/sub-skills/2-performance-funil.md` |
| [3] | `.claude/skills/trafego-analise/sub-skills/3-criativos.md` |
| [4] | `.claude/skills/trafego-analise/sub-skills/4-geo-demografia.md` |
| [5] | `.claude/skills/trafego-analise/sub-skills/5-timing-sazonalidade.md` |
| [6] | `.claude/skills/trafego-analise/sub-skills/6-investigacao-profunda.md` |
| [7] | `.claude/skills/trafego-analise/sub-skills/7-lifecycle-historico.md` |
| [8] | `.claude/skills/trafego-analise/sub-skills/8-problemas-ocultos.md` |
| [9] | `.claude/skills/trafego-analise/sub-skills/9-orcamento-projecao.md` |
| [10] | `.claude/skills/trafego-analise/sub-skills/10-comparativo.md` |
| [11] | Sub-skill mais próxima da intenção identificada |

### Protocolo padrão de todo output

Todo sub-skill entrega obrigatoriamente:

1. **Diagnóstico**: o que os dados revelam objetivamente.
2. **Causa provável**: por que está acontecendo (hipótese baseada em padrões VTSD).
3. **No VTSD, isso significa…**: qual elemento do método está em jogo.
4. **Ação recomendada**: próximo passo concreto. Se exige execução, apontar para a skill executora.

Quando a análise sugerir texto de anúncio (gancho, headline, CTA), aplicar a regra "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md antes de mostrar.

### Mapeamento VTSD × métrica

| Elemento VTSD | Métrica no tráfego |
|---|---|
| Urgência Oculta | Hook Rate (video_p25 / impressions) |
| Identidade do Produto | CTR |
| Identidade do Consumidor | CPL por público |
| Decorados | Hold Rate (video_p50 / video_p25) |
| Furadeira | Play-Through Rate (video_p95 / impressions) |
| Oferta | Offer Rate (cliques no checkout / cliques totais) |
| Quadro na Parede | Connect Rate (visitas na página / cliques no link) |
| Orderbump + Upsell | LTV Rate (ticket médio vs primeira compra) |

---

## Passo 6. Dashboard (opcional)

Após entregar a análise narrada, perguntar:

```
Quer ver seus números no dashboard? (s/n)
```

Se `s`: seguir o fluxo do `/trafego-dashboard` (`.claude/commands/trafego-dashboard.md`) desde o início. Se o aluno já tem dashboard ao vivo, entrega o link; se não tem, cria (com o conector MCP da Meta).

Quando o caminho for o legado (sem MCP), o dashboard estático é a fotografia desta análise. Avisar antes:

```
⚠️ Fotografia: o dashboard estático mostra os dados deste momento.
   Métricas mudam, e o arquivo NÃO atualiza sozinho.
```

Então acionar `.claude/skills/trafego-analise/sub-skills/_export-html.md`, salvar em `meus-produtos/{ativo}/trafego/analise/{slug-output}-{YYYY-MM-DD-HHMM}.html` e devolver o caminho absoluto.

Se o aluno pedir para salvar esta análise como relatório (fotografia com gráficos), acionar o `_export-html.md` direto, em qualquer modo: ele não toca a API.

---

## Passo 7. Handoff para execução

Se a análise sugerir ações executáveis, mostrar primeiro o bloco recomendado padrão:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-otimizar
Análise feita. Hora de executar as ações no Meta Ads (pausar
criativos, reduzir orçamento, refresh) ou emitir sinal de
prontidão pra escala.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Em seguida, listar alternativas conforme o gargalo identificado na análise:

```
Outras skills conforme o gargalo identificado:

- Investigação estratégica profunda (hipóteses, falso vencedor, confiança): /trafego-diagnostico
- Escalar campanhas validadas: /trafego-escalar
- Criar regra automática ou alerta: /trafego-regras
- Criar audience custom/lookalike: /trafego-publicos
- Diagnóstico aprofundado de pixel: /trafego-pixel
- Montar teste A/B: /trafego-testes
- Entender por que o criativo não vende: /trafego-criativos
- Criar criativos novos: /copy-anuncio + /criativo-estatico (vídeo: /video-heygen, /video-remotion)
- Diagnosticar gargalo de página, oferta ou checkout: /trafego-oferta-funil
- Corrigir a página: /feedback-pagina (low ticket: /feedback-low-ticket) ou /pagina-performance
- Corrigir o checkout: /pagina-checkout
```

---

## Passo 8. Próximo output

```
Quer rodar outro output? Digite o número (1 a 11) ou "não".
```

---

## Regras absolutas

1. NUNCA inventar métricas. Se o dado não estiver disponível, informar e pedir.
2. SEMPRE usar terminologia VTSD nas análises.
3. NUNCA deixar uma análise sem ação recomendada concreta.
4. SEMPRE identificar o gargalo principal antes de listar secundários.
5. NUNCA usar jargão técnico sem explicar em linguagem do método.
6. Esta skill **narra**, não executa edição. Para ações de execução, encaminhar para a skill executora correta.
7. Export HTML é opcional e SEMPRE precedido por confirmação explícita do aluno. Nunca gerar HTML automaticamente.
8. Um output por vez. Não entregar múltiplos outputs em uma resposta.
9. HTML de export sempre vai para `meus-produtos/{ativo}/trafego/analise/`. Nunca sobrescrever (cada export tem timestamp próprio).
10. NUNCA perguntar ao aluno o que já está no `resumo-produto.md` (preço, tipo de produto, público).
11. NUNCA exibir comando com token no chat. Mascarar como `***TOKEN_MASCARADO***`.
