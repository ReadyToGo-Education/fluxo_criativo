---
name: workshop-marketing:trafego-otimizar
description: Diagnostica e otimiza campanhas Meta Ads em veiculação. Valida a confiabilidade do dado antes de diagnosticar (janela/atribuição, pixel, conciliação). Aplica diagnóstico em 2 camadas (tendência cruzando 3 janelas + gargalo), classifica em 6 trilhas e decide por LUCRO em reais (margem de contribuição, ROAS/CPA de break-even, três zonas) com o CPA como guardrail. Ações neutras ou pra baixo (nunca aumentam o gasto total): reduzir -20%, realocação neutra, limites por conjunto em CBO, cost cap, pausar, cortar posicionamento, guardrail automático. Painel de decisão em HTML opcional. Emite sinal de prontidão para /trafego-escalar quando o ROAS sustentado passa do break-even. Use quando o aluno pedir "analisar campanha", "otimizar", "diagnóstico", "CPA alto", "CPL caro", "está dando lucro?", "criativo cansou", "frequência alta", "está pronta para escalar?", "realocar orçamento", "pausa tudo com ROAS<1". Para low ticket via planilha colada (sem API), use /lt-otimizar.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Trafego Otimizar. Diagnóstico de Campanhas Meta Ads

Diagnostica campanhas Meta Ads em veiculação, identifica onde está o problema (criativo, técnico, página, checkout, leilão, saturação) e propõe **8 alavancas** que **nunca aumentam o gasto total** da conta: todas neutras ou pra baixo. Decide por **lucro em reais** via margem de contribuição, com o CPA como guardrail. Quando a campanha está madura, estável e em zona verde, emite sinal explícito de prontidão para `/trafego-escalar`.

A especificação técnica completa está em `.claude/skills/trafego-otimizar/SKILL.md`. Este command é o orquestrador.

**Diferença vs `/lt-otimizar`:**
- `/trafego-otimizar` puxa dados pela conexão com a Meta (MCP ou App), cobre as 6 trilhas, decide por lucro e emite sinal de prontidão para escala.
- `/lt-otimizar` recebe planilha colada do Gerenciador, foca low ticket com a regra "60% do ticket". Atalho rápido de quem ainda não conectou a conta.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo`. Leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md, seção "Contexto Persistente do Negócio"). Do resumo saem o **ticket** (preço do produto) e o **tipo** (Low, Middle ou High Ticket), que antecipam a trilha. Não pergunte o que o resumo já tem.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia `META_AUTH_MODO` no `.env`.

- **Se vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive o legado `HIBRIDO`): acione `/trafego-conexao` antes de prosseguir. Não tente adivinhar nem cair em fallback. Esta verificação é o passo zero de toda skill `/trafego-*`.
- **Se `MCP_CONECTOR`:** confirmar que pelo menos uma tool `ads_*` do conector está disponível (descobrir pelo final do nome; o prefixo varia). Se nenhuma estiver, pedir ao aluno para reabrir o Claude Code (MCP recém-adicionado às vezes precisa de reload). Se persistir, voltar a `/trafego-conexao` para diagnosticar. Conferir também `FB_AD_ACCOUNT_ID` com valor (`grep -q "^FB_AD_ACCOUNT_ID=." .env`); se faltar, a opção "Validar" do `/trafego-conexao` completa. Se a Meta responder que a conta ainda não foi liberada no conector, avisar em linguagem simples e oferecer trocar para o modo App pelo `/trafego-conexao`.
- **Se `APP`:** confirmar com `grep -q "^NOME=." .env` que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem com valor no `.env` (nunca exibir o valor). Se faltar algum, acionar `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar. Única lacuna do MCP nesta skill: o **guardrail automático** (§18 da SKILL), que vai para a `/trafego-regras`; no MCP, ela guia a criação da regra no Gerenciador.

### 0.3 Selecionar conta de anúncios (multi-conta)

Ler `FB_AD_ACCOUNT_IDS` e `FB_AD_ACCOUNT_ID` no `.env`. Se houver mais de uma, perguntar com a conta padrão em primeiro lugar e etiqueta `"padrão"` (nomes via `ads_get_ad_accounts` no MCP ou GET da Graph API no APP, ver Passo 0.5 da SKILL). Salvar como `AD_ACCOUNT_ID_ATUAL`. Não sobrescrever o `.env`.

### 0.4 Filtro de status das campanhas (Passo 0.55 da SKILL)
```
[1] Somente ativas         (ACTIVE)
[2] Ativas + com problemas (ACTIVE + WITH_ISSUES)  ← default
[3] Ativas + pausadas      (visão ampla)
```

> **Override de pausadas para lista nomeada:** se o aluno escolheu [1] ou [2] mas depois pede campanhas específicas que estão pausadas, ampliar `STATUS_FILTRO` **só pra aquelas**, sem refazer o fluxo. Ver SKILL Passo 0.55.

### 0.5 Identificar escopo (Passo 0.6 da SKILL)
```
[1] Campanhas específicas
[2] Conta completa
```

> **Guard de conta grande:** varredura inicial só com campos leves (id, name, objective, effective_status, daily_budget). Insights vêm depois.
> **Desambiguação de nomes duplicados:** se um nome casar com 2+ campanhas, mostrar IDs + orçamento + status e pedir confirmação.

### 0.6 Ler especificações
Leia:
- `.claude/skills/trafego-otimizar/SKILL.md`. Lógica completa, incluindo §3.5.1 (mapa de campos reais), §3.6 (camada de lucro), §6.3 a §6.5 (alavancas neutras), §7.4 (cortar posicionamento), §17 (painel HTML), §18 (guardrail).
- `.claude/skills/trafego-insights/SKILL.md`. Como puxar dados (a otimização não puxa dados sozinha, sempre via insights).

---

## Passo 1. Inputs (Passo 0.7 da SKILL, uma pergunta por vez)

### 1.1 Tipo de funil (inferido)
Inferir pelo `objective` das campanhas (venda por Compra = perpétuo; Lead = lançamento/captação). Só perguntar se o escopo misturar objetivos:
```
[1] Perpétuo / venda direta   (otimização por Compra)
[2] Lançamento / captação     (otimização por Lead)
```

### 1.2 Ticket (lido do resumo)
Usar o preço do `resumo-produto.md`. Só perguntar se o resumo não tiver preço ou se a campanha vender outro produto:
```
Qual é o valor do produto que essa campanha vende, em reais? (ex: 97, 297, 997)
```

### 1.3 Meta de CPA ou CPL (opcional)
```
[1] Sim  (informe o valor em reais)
[2] Não  (uso 50% do ticket como referência padrão)
```

### 1.4 Margem de contribuição (3 pedaços fáceis, uma pergunta por vez)
```
Para calcular o lucro de verdade, preciso de 3 taxas da sua venda:
plataforma, reembolso e imposto (pode ser aproximado).

1. Quero informar as 3 taxas
2. Não sei agora (uso a faixa de margem de 60 a 80%)

Digite o número:
```
Se 1, perguntar **uma taxa por mensagem**, cada uma com o próprio exemplo: taxa da plataforma de venda (ex: 9,9% na Hotmart; costuma ficar entre 1% e 10%), taxa média de reembolso (ex: 5%) e imposto sobre o faturamento (ex: 6% no Simples; pode chegar a 17%). Se o aluno informar só parte das taxas, perguntar de novo só a que faltou; se ele não souber, usar o modo faixa e avisar.

Calcula `margem_contribuicao = 1 - (taxa + reembolso + imposto)`. Custos fixos NÃO entram. Se 2, ou sem nenhuma das três: usar **modo faixa** 60 a 80%.

### 1.5 Sazonalidade ativa (opcional)
```
[1] Nenhum (default)
[2] Black Friday
[3] Data comemorativa
[4] Lançamento de competidor relevante
```

**Confirmação:**
```
Otimizando: {nome} | Funil: {tipo} | Ticket: R$ {valor} (do resumo do produto) | Meta CPA: R$ {alvo}
Margem de contribuição: {margem}% | ROAS de ponto de equilíbrio: {1÷margem}
```

---

## Passo 2. Confiabilidade do dado (Passo 0.8 da SKILL, obrigatório)

🔍 Próximo passo: validar a fonte dos números antes de qualquer interpretação (4 passos). Tempo estimado: cerca de 30 segundos.

Rodar as 4 checagens da SKILL Passo 0.8:
1. **Janela e atribuição.** Carimbar em todo número. Se `attribution_setting` derruba a chamada multi-campo, assumir padrão omni e declarar.
2. **Saúde do pixel.** Acionar `/trafego-pixel` ou inferir pelo fluxo de compras. Plano B se o dataset estiver em liberação gradual.
3. **Conciliação.** Em `escopo: conta_completa`, a soma das campanhas tem que bater com o total da conta (±5%). Em recorte, marcar `nao_aplicavel` e seguir.
4. **Descoberta de campos.** Confirmar quais campos a conta expõe antes de pedir.

Imprimir o bloco `Confiabilidade do dado` ao aluno (Parte 1 do output, SKILL §13).

| Nível | Comportamento |
|---|---|
| `alta` | Prossegue normalmente. |
| `media` | Prossegue, **rebaixa CPA a secundário**, decide por ROAS e sinais antecipados (CTR de link, frequência). Aviso explícito. |
| `baixa` | Avisa a divergência e propõe ajuste antes de seguir. Nunca emite prontidão para escala. |

✅ Concluído: confiabilidade do dado {nivel}.

---

## Passo 3. Puxar dados via /trafego-insights

🔍 Próximo passo: puxar as métricas das 3 janelas da trilha, as ações de funil e o valor médio por venda. Tempo estimado: cerca de 30 segundos.

A otimização **não puxa dados sozinha.** Invocar `/trafego-insights` com:
- `campaign_id` (ou `escopo: conta_completa`)
- `tipo_funil`
- `ticket_brl`
- `nivel: auto` (retorna campanha + conjuntos + anúncios)
- janela conforme a trilha (1d/3d/7d, 3d/7d/14d, 7d/14d/30d, ou lançamento 1d/3d)

Se modo conta completa, drill-down nas 5 piores.

> **Mapa de campos reais (§3.5.1 da SKILL, contrato do conector em `trafego-insights/SKILL.md` §10.1):** no MCP, `ads_get_ad_entities` **não aceita** `actions`, `action_values`, `inline_link_click_ctr`, `initiate_checkout` (o checkout iniciado é `omni_initiated_checkout`). Pedir gasto com `amount_spent`, cliques no link com `link_click`, visitas à página com `landing_page_view`, checkout iniciado com `omni_initiated_checkout`, compras com `omni_purchase`, valor das compras com `offsite_conversion_fb_pixel_purchase_values` (sem ele, `purchase_roas × amount_spent`), ROAS com `purchase_roas` e CTR de link **calculado** (`link_click ÷ impressions`). Carrinho (`add_to_cart`) não foi conferido: checar com `ads_get_field_context` antes. No APP via curl, valem os nomes clássicos (com `curl -g` quando houver `{}` no `fields`).

✅ Concluído: dados puxados e valor médio por venda calculado.

---

## Passo 4. Classificar trilha + verificar maturação

Aplicar a tabela §2 da SKILL:

- Perpétuo + ticket ≤ R$ 500: `perpetuo_low` (1d/3d/7d, CPA máximo 60% do ticket)
- Perpétuo + ticket R$ 501 a 1.499: `perpetuo_mid` (3d/7d/14d, máximo 55%)
- Perpétuo + ticket ≥ R$ 1.500: `perpetuo_high` (7d/14d/30d, máximo 55%)
- Lançamento: `lancamento_low/mid/high` (1d/3d)

Calcular `cpa_target` (50% do ticket por default ou valor declarado), `cpa_breakeven = AOV × margem`, `roas_breakeven = 1 ÷ margem`.

Verificar maturação (§4 da SKILL). Se todos os ativos estiverem imaturos, retornar:

```
Os dados ainda estão imaturos para diagnóstico:

- [Lista do que está imaturo: campanha com menos de X dias, conjunto com gasto abaixo do CPA alvo, etc.]

Próxima reanálise sugerida: [data/hora].

Roda /trafego-otimizar de novo depois desse prazo, ou me peça um
diagnóstico parcial sabendo que a confiabilidade é baixa.
```

---

## Passo 5. Diagnóstico em 2 camadas + lucro

🔍 Próximo passo: diagnosticar a tendência, o gargalo e o lucro de cada campanha. Tempo estimado: 2 a 3 minutos (campanha única) ou 3 a 5 minutos (conta completa).

### 5.1 Tendência (§5.1 da SKILL): cruzar curta × média × longa
- `estavel_performando`
- `esfriando_ou_ruido`
- `recuperando`
- `ruim_estrutural`
- `saturacao`
- `entrega_limitada`

### 5.2 Gargalo (§5.2 da SKILL): bottom-up
- `criativo` (CTR baixo) [DENTRO do Meta]
- `tecnico` (Connect Rate < 70%) [FORA do Meta]
- `pagina` (conversão da página crítica) [FORA do Meta]
- `checkout` (Carrinho → Compra crítico, ou Checkout → Compra abaixo da metade do piso da faixa do ticket, tabela da §3.5 da `/trafego-oferta-funil`) [FORA do Meta]
- `leilao_audiencia` (CPM alto)
- `saturacao` (Frequência > 3,5)
- `nenhum` (tudo saudável: avaliar prontidão pra escala)

### 5.3 Camada de lucro (§3.6 da SKILL)

Calcular pra cada campanha:
- `roas_atual`
- `lucro_dia = gasto_dia × (ROAS × margem - 1)`
- **Zona** (testar nesta ordem): vermelha (lucro/dia < 0), verde (CPA ≤ meta), amarela (o resto: CPA > meta mas lucro/dia ≥ 0)

> **Filtro de lucro obrigatório:** zona amarela **não se contém**: se otimiza o criativo. Reduzir, conter ou pausar por dinheiro só vale na **zona vermelha**.

---

## Passo 6. Montar plano com 8 alavancas

A SKILL oferece 8 alavancas. Marcar cada uma como `✓` (recomendada agora, com motivo) ou `reserva` (com o gatilho que a ativaria). **Nenhum item evapora:** toda campanha vermelha aparece no plano OU como reserva com motivo explícito.

| Alavanca | Quando | Reset? |
|---|---|---|
| **Reduzir -20%** | zona vermelha + gargalo dentro do Meta | não |
| **Realocação neutra** (§6.3) | queimador + vencedor com folga (gasto total intocado) | não |
| **Limites por conjunto CBO** (§6.4) | CBO com 2+ conjuntos e distribuição torta (`daily_spend_cap` / `daily_min_spend_target`) | não |
| **Cost cap / bid cap** (§6.5) | lucrativa com CPA subindo, manter volume (CBO: estratégia na campanha e teto em cada conjunto ativo; ABO: os dois no conjunto) | **sim** |
| **Pausar** | criativo/saturação (gargalo dentro do Meta) ou conjunto/campanha em casos extremos | não |
| **Cortar posicionamento** (§7.4) | placement queima sem converter (Audience Network etc.) | **sim** |
| **Guardrail automático** (§18) | regra nativa que vigia 24h (CPA > break-even etc.), sempre pela `/trafego-regras` (sub-fluxo [1], com gasto mínimo): no MCP, ela guia a criação no Gerenciador; no APP, cria pela API. A regra nasce desligada até o aluno revisar | não |
| **Alertar o aluno** | gargalo fora do Meta (página, checkout, técnico): `/trafego-oferta-funil` e a skill de correção | n/a |

Ações que **resetam aprendizado** (cost cap, cortar posicionamento) disparam o disclaimer da §11 (≈ 50 × CPA target) + confirmação reforçada.

> **Bloqueios à mudança de orçamento:** conjunto em fase de aprendizado, última edição há menos de 48h, gasto do dia abaixo de 50% do orçamento (§6.2 da SKILL). No MCP sem o campo de aprendizado (`NAO_VERIFICADO`), o conjunto segue na lista marcado "aprendizado não conferido": o bloco 🛡️ avisa que o conector não mostra essa fase e o aluno decide no "sim".
> **ABO vs CBO:** detectar `budget.tipo` antes de qualquer mudança de orçamento. Sem o tipo, marcar `acao: aguardar`.

---

## Passo 7. Avaliar prontidão para escala (§12 da SKILL)

Se `tendencia: estavel_performando` E `gargalo: nenhum` E **todas** as condições da §12 da SKILL passam (incluindo o **bloco `lucro`**: ROAS sustentado ≥ break-even, lucro/dia ≥ 0), emitir `sinal_para_escala.pronta: true` com modo recomendado, velocidade sugerida, janela de referência, margem de segurança, riscos observados e criativos de backup disponíveis.

> Zona amarela **não emite prontidão**: escala exige zona verde sustentada.
> Aprendizado não conferido pelo conector (MCP sem o campo) não reprova a prontidão: o critério aceita "não conferido" e o aviso vai em riscos observados (§12 da SKILL).

---

## Passo 8. Apresentar diagnóstico (Parte 1 na tela, Parte 2 no arquivo, §13 da SKILL)

Mostrar em formato legível (não YAML cru). A Parte 1 traz:
- **Confiabilidade do dado** (do Passo 2)
- **Diagnóstico** (trilha, métrica-norte, tendência, gargalo)
- **O que está acontecendo** (3 observações com número)
- **Lucro (estimado, margem X%)**: lucro do período, lucro/dia, ROAS de ponto de equilíbrio, CPA de ponto de equilíbrio (com uma frase do que significam), zona predominante
- **Ferramentas disponíveis pra otimizar**: tabela das 8 alavancas + handoffs `/trafego-escalar`, `/trafego-pixel` e `/trafego-oferta-funil`, marcadas `✓` ou `reserva` com motivo
- **Plano de ação**: ordem de prioridade, com a regra "nenhum item evapora"
- **Próximas observações**
- **Está pronta para escalar?** (Sim: modo + velocidade | Não: motivos)

Parte 2 (YAML técnico): não aparece na tela. Vai num bloco no fim do arquivo do Passo 11, com os blocos `confiabilidade_do_dado` e `lucro` completos, mais `acoes_recomendadas` com `reset_aprendizado` por ação. Só mostrar se o aluno pedir ("me mostra o YAML", "me dá só o YAML"). O gate 🛡️ do Passo 9 descreve as ações em português.

**Gargalo fora do Meta:** o alerta encaminha primeiro para `/trafego-oferta-funil` (diagnóstico da oferta) e, conforme o resultado, para a correção: `/feedback-pagina` ou `/feedback-low-ticket` (página), `/pagina-checkout` (checkout), `/pagina-performance` (técnico) ou `/pagina-pixel` (pixel na página). Não pausar a campanha enquanto isso; reduzir -20% só como contenção, e só em zona vermelha.

---

## Passo 9. Gate 🛡️ e execução

Antes de qualquer ação de escrita (reduzir, realocar, limitar, cost cap, pausar, cortar posicionamento, reativar), apresentar o bloco:

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: {verbo claro}
Endpoint: {humano-legível}
Objeto: {id ou nome}
O que vai mudar:
  - {linha por linha}
Reset de aprendizado esperado: {sim | não | parcial}
Reversível? {sim, com qual comando | não}

Pode aplicar? Responda "sim" pra confirmar, "não" pra cancelar.
```

**Regras:**
- **Nunca exibir o `curl` completo no chat.** Aguardar `sim` (ou variante: aprovo, pode, manda).
- **Um "sim" por lote no mesmo fluxo:** pedir aprovação por prioridade (ALTA primeiro); as ações aprovadas juntas vão num bloco só e num "sim" só. Depois do sim, executar sem reabrir o gate, exceto se uma chamada falhar, o aluno mudar o plano ou surgir escrita fora do lote.
- **Ações que resetam** (cost cap, cortar posicionamento) exigem confirmação reforçada com a conta de custo (§11 da SKILL).
- **Esta skill não apaga entidades.** Para tirar do ar, pausa ou arquiva.

Para cada ação aprovada:
- Anunciar: `⏳ Aplicando: [ação].`
- Sucesso: `✅ [ação] aplicada.`
- Erro: `⚠️ [ação] falhou: [motivo].` e parar para perguntar antes de seguir com o restante do lote.

**Ações em lote por filtro** ("pausa tudo com ROAS<1") seguem a sub-skill `sub-skills/acoes-lote.md`. **Atalhos compostos** (lookalike de compradores, faxina, refresh criativo) seguem `sub-skills/atalhos-compostos.md` e só rodam com o plano numerado e um **"aprovar tudo"** explícito (modo lote pré-aprovado do CLAUDE.md).

---

## Passo 10. Painel de decisão HTML opcional (§17 da SKILL)

**Só em trilha de perpétuo** (o lucro e as 3 zonas dependem de compra). Em lançamento, não oferecer: dizer em 1 linha que, na captação, a leitura é pelo CPL, que já está no diagnóstico. Em conta completa com objetivos misturados, o painel entra só com as campanhas de perpétuo e avisa quais ficaram de fora.

Após entregar a Parte 1 (a Parte 2 vai para o arquivo no Passo 11), **opcionalmente** oferecer (pergunta conforme o `EXPORT_TEMA` do `.env`, ver a sub-skill):
```
Quer salvar esse diagnóstico como um painel visual (HTML)? (s/n)

⚠️ Snapshot: o painel é uma "fotografia" dos dados deste momento. Métricas mudam,
   e o arquivo NÃO atualiza sozinho. Pra dado fresco, rode a otimização de novo.
```

Se `s`: rodar a sub-skill `sub-skills/_export-painel-decisao.md`. Salva em `meus-produtos/{ativo}/entregas/trafego/otimizar/painel-decisao-{YYYY-MM-DD-HHMM}.html` e abre no navegador via `scripts/abrir-html.py`. **Gate de conformidade obrigatório** antes de declarar pronto. Nunca rodar sem confirmação. Para acompanhar a conta ao vivo, o caminho é o `/trafego-dashboard`.

---

## Passo 11. Salvar diagnóstico textual

Salvar na mesma subpasta do painel e do lote:
```
meus-produtos/{ativo}/entregas/trafego/otimizar/otimizacao-{campanha-slug}-{YYYY-MM-DD}.md
```

Conteúdo: Parte 1 + ações aplicadas + próximas observações + Parte 2 (YAML técnico) num bloco no fim do arquivo.

Mostrar o caminho absoluto como texto copiável: `{raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\otimizar\otimizacao-{...}.md`

---

## Passo 12. Próximos passos

**Se `sinal_para_escala.pronta = true`:**

Antes de encaminhar para escala, sugerir ao aluno: "Quer rodar o detector de falso vencedor (`/trafego-diagnostico` opção [4]) antes de escalar? Ele confirma que o resultado é sustentável."
- Se o detector rodou nesta sessão e a campanha não saiu `vencedor_real` com score de confiança 50 ou mais: não passar o bastão. Trocar para `pronta: false` com esse motivo e seguir pelo bloco "Se `sinal_para_escala.pronta = false`", abaixo. Com `vencedor_real` e score de 50 a 74, seguir só com velocidade conservadora (escala gradual).
- Se o aluno recusar o detector: seguir para a escala, gravando `falso_vencedor: nao_verificado` no `sinal_para_escala`.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-escalar
A campanha está em zona verde com ROAS sustentado acima do ponto de equilíbrio.
Use modo {modo_recomendado} e velocidade {velocidade_sugerida}
(vieram no diagnóstico).

Quer que eu já monte o plano de escala?

1. Sim, montar agora
2. Agora não
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Se `1`: acionar a skill `trafego-escalar` passando o payload do diagnóstico (`sinal_para_escala`, com `falso_vencedor` e `score_confianca`, `confiabilidade_do_dado`, `lucro`, meta de CPA/CPL, conta e campanha). A escala pula a coleta de contexto (Passo 0.1 da SKILL dela) e vai direto para o risco, o guardião de caixa e o plano com gate 🛡️. Montar o plano não escreve nada na conta.

**Se `sinal_para_escala.pronta = false`:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: aguardar 48h e voltar pra /trafego-otimizar
Aguarde 48h após as ações aplicadas e rode a otimização de novo pra ver
se as métricas se recuperaram. Motivos da não prontidão: {motivo_se_nao_pronta}.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Em seguida, listar alternativas pra contextos específicos:

```
Outras opções conforme o contexto:

- Para ver dados atualizados antes do prazo: /trafego-insights
- Para acompanhar a conta ao vivo num painel: /trafego-dashboard
- Se o gargalo é página, checkout ou técnico: /trafego-oferta-funil para
  o diagnóstico; correção em /feedback-pagina, /feedback-low-ticket,
  /pagina-checkout ou /pagina-performance.
- Se o criativo cansou: /copy-anuncio + /criativo-estatico para as peças
  novas e /trafego-testes para o A/B.
- Para criar lookalike de compradores: /trafego-publicos (ou o atalho
  composto da otimização).
```

---

## Princípios que este command nunca viola (espelham os princípios da SKILL)

1. **Confiabilidade do dado antes do diagnóstico.** Sem o Passo 2 passar, não interpreta número.
2. **Decidir por lucro; CPA é guardrail.** Zona amarela se otimiza, zona vermelha contém. Custo fixo nunca entra.
3. **Mudanças graduais.** Orçamento move ±20%, exceto pause.
4. **Ações neutras ou pra baixo nunca aumentam o gasto total.** Subir o total é `/trafego-escalar`.
5. **Aguardar 48h** entre ajustes no mesmo objeto.
6. **Bottom-up.** Criativo, depois conjunto, depois campanha.
7. **Não pausa por gargalo fora do Meta.** Alerta o aluno, encaminha para `/trafego-oferta-funil` e para a correção, mantém a estrutura viva.
8. **Detectar ABO vs CBO** antes de mexer em orçamento.
9. **Não escala.** Quem cresce orçamento é `/trafego-escalar`.
10. **Cooldown** após handoff de descida da escala (7d perpétuo low/mid, 14d perpétuo high, 24h lançamento), lido de `meus-produtos/{ativo}/trafego/escalar/historico-{campaign_id}.md` (última linha `freio_total`), também entre sessões.
11. **Apenas dados nativos do Gerenciador.** Sem tracking custom. Sem inventar dado.
12. **Nenhum item evapora.** Toda campanha vermelha aparece no plano ou como reserva com motivo.
13. **Token nunca aparece no chat.** Sempre mascarado.
14. **Gate 🛡️ antes de toda escrita.** Nada executa sem `sim` explícito; atalho composto só com "aprovar tudo"; esta skill nunca apaga entidade.
