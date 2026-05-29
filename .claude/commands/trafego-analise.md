---
name: workshop-marketing:trafego-analise
description: Análise narrada de tráfego pago Meta Ads com terminologia VTSD (Mandala 18 tipos, Urgência Oculta, Quadro na Parede, Furadeira, Decorados, 3 Identidades, HOT/COLD/SUPERCOLD, Caixa Rápido, Pico vs Evergreen). 9 outputs narrativos: Diagnóstico Rápido, Performance & Funil, Criativos & Copy, Geo & Demografia, Timing & Sazonalidade, Investigação Profunda, Lifecycle & Histórico, Problemas Ocultos, Orçamento & Projeção. Busca dados diretamente na Graph API sem intermediários. Cada output entrega diagnóstico, causa provável, interpretação VTSD e ação recomendada com handoff para skill executora.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Tráfego Análise. Análise VTSD de Meta Ads

Análise narrada de campanhas Meta Ads pela lente da metodologia VTSD (Venda Todo Santo Dia, Leandro Ladeira). Cada métrica é o termômetro de um elemento do método: dado → método → decisão.

Esta skill **narra**, não executa edição. Quando a análise sugere ação, faz handoff para a skill executora correspondente.

---

## Passo 0. Contexto e conexão Meta

### 0.1 Produto ativo
Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/perfil.md`.

### 0.2 Conexão Meta (gate duro)
Ler `META_AUTH_MODO` no `.env`.

- **Se vazio ou ausente:** acionar `/trafego-conexao` antes de prosseguir.
- **Se `MCP_CONECTOR`:** confirmar que pelo menos uma tool com prefixo `mcp__*__ads_*` está disponível. Se nenhuma, pedir ao aluno para reabrir o Claude Code.
- **Se `APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem no `.env`. Se faltar algum, acionar `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

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

[10] COMPARATIVO A × B          duas campanhas lado a lado: spend, CPA/CPL,
                                connect rate, hook rate, funil completo

[11] descrever em texto livre o que precisa
```

Se o aluno descreveu em texto livre, mapear para o output mais próximo e confirmar antes de prosseguir.

---

## Passo 2. Conta de anúncios (multi-conta)

1. Ler `FB_AD_ACCOUNT_IDS` no `.env` (lista separada por vírgula).
2. Se ausente ou com exatamente 1 ID, usar `FB_AD_ACCOUNT_ID` direto, sem perguntar.
3. Se 2 ou mais IDs, buscar nomes amigáveis:

   **Modo APP:**
   ```bash
   curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name&limit=100&access_token={FB_ACCESS_TOKEN_PERMANENTE}"
   ```

   **Modo MCP_CONECTOR:** usar `mcp__*__ads_get_ad_accounts`.

   Filtrar apenas as IDs que estão em `FB_AD_ACCOUNT_IDS`. Marcar como "padrão" a que está em `FB_AD_ACCOUNT_ID`. Apresentar menu numerado e aguardar escolha.

4. Salvar a conta escolhida em `AD_ACCOUNT_ID_ATUAL` (variável local da execução, nunca sobrescreve `.env`).

---

## Passo 2.5. Filtro de status das campanhas

```
Quais campanhas incluir na análise?

[1]  Somente ativas      (ACTIVE — o que está rodando agora)
[2]  Somente pausadas    (PAUSED + WITH_ISSUES — o que está desligado)
[3]  Ativas + pausadas   (visão completa do presente)
[4]  Histórico completo  (inclui arquivadas — análise de longo prazo)
```

Salvar como `STATUS_FILTRO` (variável local da execução) e usar em todas as chamadas de API desta sessão:

| Escolha | `effective_status` na API |
|---------|--------------------------|
| [1] | `["ACTIVE"]` |
| [2] | `["PAUSED","WITH_ISSUES"]` |
| [3] | `["ACTIVE","PAUSED","WITH_ISSUES"]` |
| [4] | `["ACTIVE","PAUSED","WITH_ISSUES","ARCHIVED"]` |

**Alerta automático para output [8] Problemas Ocultos:** se `STATUS_FILTRO = ["ACTIVE"]` e o aluno escolher o output [8], alertar antes de rodar: "Você está analisando só campanhas ativas. Para ver ad sets quebrados e anúncios pausados por problema, reinicie e escolha [2] ou [3]."

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

## Passo 4. Busca direta na Graph API

🔍 Próximo passo: buscar métricas da conta. Tempo estimado: cerca de 30 segundos.

### Campos base (usados em todos os outputs)

```
spend,impressions,clicks,ctr,cpm,cpc,reach,frequency,
actions,action_values,cost_per_action_type,
video_play_actions,video_avg_time_watched_actions,
video_p25_watched_actions,video_p50_watched_actions,
video_p75_watched_actions,video_p95_watched_actions
```

### Parâmetros por output

> **Esta tabela é o ponto de partida, não o teto.** Cada sub-skill pode e deve fazer chamadas adicionais à Graph API sempre que o contexto da análise exigir dados não listados aqui. O critério é simples: o dado é necessário para responder uma pergunta do output? Se sim, buscar. O sub-skill correspondente define as chamadas completas que precisa — consultar `sub-skills/{N}-{nome}.md` para a lista exata de chamadas de cada output.

| Output | level | breakdowns | chamadas mínimas — sub-skill pode adicionar mais |
|--------|-------|------------|-----------------|
| [1] Diagnóstico Rápido | campaign | — | — |
| [2] Performance & Funil | campaign + ad | publisher_platform, platform_position | + 2ª chamada com período anterior equivalente para comparativo de CPM/ROAS |
| [3] Criativos & Copy | ad | publisher_platform | + buscar `name`, `creative` dos ads ativos; + chamada WoW com `time_increment=7` |
| [4] Geo & Demografia | ad | age,gender | + 2ª chamada: region; + 3ª chamada: country |
| [5] Timing & Sazonalidade | campaign | hourly_stats_aggregated_by_advertiser_time_zone | + chamada diária com `time_increment=1`; + chamada mensal com `last_180d` e `time_increment=monthly` |
| [6] Investigação Profunda | ad | device_platform, impression_device, publisher_platform | + chamada com `time_increment=1` e `since/until` dos primeiros dias de cada campanha (análise das primeiras 24h) |
| [7] Lifecycle & Histórico | campaign | — | + chamada com `time_range` 6 meses e `time_increment=monthly`; + chamada com `start_time` e `updated_time`; + chamada `effective_status=["PAUSED","ARCHIVED"]` |
| [8] Problemas Ocultos | adset + ad | — | + ad sets `WITH_ISSUES/LIMITED`; + ads `DISAPPROVED/WITH_ISSUES`; + audiences (`approximate_count_lower_bound/upper_bound`); + dataset stats de pixel; + budget por adset (ABO); acionar Gerenciador de Eventos para diagnóstico de pixel |
| [9] Orçamento & Projeção | campaign | — | + `daily_budget/lifetime_budget/spend_cap` das campanhas; + `daily_budget` dos adsets quando conta usa ABO |
| [10] Comparativo A × B | campaign + ad (por campanha) | — | 2 chamadas separadas por `campaign_id` + métricas derivadas (connect rate, hook rate, funil completo por campanha) |

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

**Conversões customizadas** (`offsite_conversion.custom.*`) têm IDs de pixel específicos — nunca somar com as padrão acima. Verificar se o valor atribuído é plausível antes de incluir em qualquer cálculo de receita (valores de R$ milhões por evento indicam pixel misconfigured).

**Regra prática:** ao iterar sobre `actions` ou `action_values`, filtrar **exatamente** o tipo canônico listado acima. Se o tipo canônico não estiver presente na resposta para uma campanha, assumir zero para aquela campanha — nunca tentar alternativas da lista de duplicatas como fallback.

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

### Modo MCP_CONECTOR

Usar `mcp__*__ads_insights_performance_trend` ou `mcp__*__ads_get_ad_entities` com os parâmetros equivalentes.

### Chamadas adicionais para output [8] Problemas Ocultos

```bash
# Ad sets com problemas de entrega
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/adsets
  ?fields=id,name,status,effective_status,reach_estimate,targeting
  &filtering=[{"field":"effective_status","operator":"IN","value":["WITH_ISSUES","LIMITED"]}]
  &access_token={TOKEN}"

# Anúncios desaprovados ou com restrição
curl -s "https://graph.facebook.com/v25.0/act_{AD_ACCOUNT_ID_ATUAL}/ads
  ?fields=id,name,status,effective_status,review_feedback
  &filtering=[{"field":"effective_status","operator":"IN","value":["DISAPPROVED","WITH_ISSUES"]}]
  &access_token={TOKEN}"
```

Para diagnóstico de pixel dentro do output [8], acionar Gerenciador de Eventos (apenas leitura).

### Chamada extra para output [9] Orçamento & Projeção

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

1. **Diagnóstico** — o que os dados revelam objetivamente.
2. **Causa provável** — por que está acontecendo (hipótese baseada em padrões VTSD).
3. **No VTSD, isso significa…** — qual elemento do método está em jogo.
4. **Ação recomendada** — próximo passo concreto. Se exige execução, apontar para a skill executora.

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

## Passo 6. Export HTML (opcional)

Após entregar a análise narrada, perguntar:

```
Quer salvar essa análise como HTML pra revisitar depois? (s/n)

⚠️ Snapshot: o HTML é uma fotografia dos dados deste momento.
   Métricas mudam, e o arquivo NÃO atualiza sozinho.
```

Se `s`: acionar `.claude/skills/trafego-analise/sub-skills/_export-html.md`.
Salvar em `meus-produtos/{ativo}/trafego/analise/{slug-output}-{YYYY-MM-DD-HHMM}.html`.
Devolver caminho absoluto.

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
Outras skills executoras conforme o gargalo identificado:

- Escalar campanhas validadas: /trafego-escalar
- Criar regra automática ou alerta: Gerenciador (Regras automáticas)
- Criar audience custom/lookalike: Gerenciador de Audiences
- Diagnóstico aprofundado de pixel: Gerenciador de Eventos
- Montar teste A/B: Duplicar entidade no Gerenciador (variando 1 dimensão)
- Criar criativos novos: /copy-anuncio + /criativo-estatico
- Atacar gargalo de página: /feedback-pagina ou /pagina-performance
- Atacar gargalo de checkout: /pagina-checkout
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
