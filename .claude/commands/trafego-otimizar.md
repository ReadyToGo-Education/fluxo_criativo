---
name: workshop-marketing:trafego-otimizar
description: Diagnostica e otimiza campanhas Meta Ads em veiculação. Aplica diagnóstico em 2 camadas (tendência cruzando 3 janelas + gargalo), classifica em 6 trilhas (perpétuo low/mid/high, lançamento low/mid/high), propõe ações graduais que preservam aprendizado (reduzir -20%, pausar criativo, refresh) e emite sinal de prontidão para /trafego-escalar quando aplicável. Use quando o aluno pedir "analisar campanha", "otimizar", "diagnóstico", "CPA alto", "CPL caro", "criativo cansou", "frequência alta", "está pronta para escalar?". Para low ticket via planilha colada (sem API), use /lt-otimizar.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Trafego Otimizar. Diagnóstico de Campanhas Meta Ads

Diagnostica campanhas Meta Ads em veiculação, identifica onde está o problema (criativo, técnico, página, checkout, leilão, saturação) e propõe ações graduais que preservam aprendizado. Quando a campanha está madura e estável, emite sinal explícito de prontidão para `/trafego-escalar`.

A especificação técnica completa está em `.claude/skills/trafego-otimizar/SKILL.md`. Este command é o orquestrador.

**Diferença vs `/lt-otimizar`:**
- `/trafego-otimizar` puxa dados via API (Marketing API ou MCP), cobre as 6 trilhas, emite sinal de prontidão para escala.
- `/lt-otimizar` recebe planilha colada do Gerenciador, foca low ticket com regra "60% do ticket". Atalho rápido.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo`. Leia `perfil.md` para inferir `ticket_brl` e `tipo_funil`.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia `META_AUTH_MODO` no `.env`.

- **Se vazio ou ausente:** acione `/trafego-conexao` antes de prosseguir. Não tente adivinhar nem cair em fallback. Esta verificação é o passo zero de toda skill `/trafego-*`.
- **Se `MCP_CONECTOR`:** confirmar que pelo menos uma tool com prefixo `mcp__*__ads_*` está disponível. Se nenhuma estiver, pedir ao aluno para reabrir o Claude Code (MCP recém-adicionado às vezes precisa de reload). Se persistir, voltar a `/trafego-conexao` para diagnosticar.
- **Se `APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem no `.env`. Se faltar algum, acionar `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

### 0.3 Selecao de conta de anuncio (multi-conta)

Apos a validacao da conexao, decidir qual conta otimizar:

1. Ler `FB_AD_ACCOUNT_IDS` no `.env`. Lista de IDs separados por virgula.
2. Se `FB_AD_ACCOUNT_IDS` nao existe ou esta vazio, usar `FB_AD_ACCOUNT_ID` direto.
3. Se `FB_AD_ACCOUNT_IDS` tem **1 conta**, usar `FB_AD_ACCOUNT_ID` direto sem perguntar.
4. Se `FB_AD_ACCOUNT_IDS` tem **2 ou mais contas**, perguntar:

   ```
   Qual conta de anuncio voce quer diagnosticar?

   1. {nome_conta_1} ({id_1})  ← padrao
   2. {nome_conta_2} ({id_2})
   3. {nome_conta_3} ({id_3})

   Digite o numero ou aperte Enter para usar a padrao:
   ```

   Para mostrar nomes amigaveis, fazer 1 chamada na Graph API:
   ```bash
   curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name&limit=100&access_token=TOKEN"
   ```
   Filtrar apenas as que estao em `FB_AD_ACCOUNT_IDS`. Marcar como "padrao" a que esta em `FB_AD_ACCOUNT_ID`.

5. Salvar a conta escolhida em variavel local da execucao (`AD_ACCOUNT_ID_ATUAL`). Nao sobrescrever o `.env`.

### 0.4 Ler especificações
Leia:
- `.claude/skills/trafego-otimizar/SKILL.md`. Lógica completa de diagnóstico.
- `.claude/skills/trafego-insights/SKILL.md`. Como puxar dados (a otimização não puxa dados sozinha, sempre via insights).

---

## Passo 1. Inputs obrigatórios

A skill recusa rodar sem os 3 inputs obrigatórios. Pergunte na ordem:

### 1.1 Escopo
```
O que você quer otimizar?

1. Uma campanha específica (você me dá o ID ou nome)
2. A conta inteira (varre todas as ativas e ranqueia urgência)

Digite o número:
```

### 1.2 Campanha (se opção 1)
```
Me passa o ID ou nome da campanha.
```

### 1.3 Tipo de funil
Se ainda não dá pra inferir do `objective` da campanha, perguntar:
```
Essa campanha é de:

1. Venda direta (perpétuo, otimização por compra)
2. Captação de leads (lançamento)

Digite o número:
```

### 1.4 Ticket
Inferir do `perfil.md`. Se não der:
```
Qual o ticket do produto que essa campanha vende?
(ex: R$47, R$497, R$1.997)
```

### 1.5 Meta CPA/CPL declarada (opcional)
```
Qual o CPA/CPL alvo? Por padrão uso 50% do ticket.

(Pode digitar o valor em reais, ou pular para usar o default)
```

### 1.6 Sazonalidade ativa (opcional)
```
Tem evento sazonal afetando a entrega agora?

1. Nenhum (default)
2. Black Friday
3. Data comemorativa
4. Lançamento de competidor relevante

Digite o número:
```

---

## Passo 2. Puxar dados via /trafego-insights

🔍 Próximo passo: puxar métricas das 3 janelas da trilha e calcular derivadas. Tempo estimado: cerca de 30 segundos.

A otimização **não puxa dados sozinha.** Invocar `/trafego-insights` com:
- `campaign_id` (ou `escopo: conta_completa`)
- `tipo_funil`
- `ticket_brl`
- `nivel: auto` (retorna campanha + conjuntos + anúncios)

Se modo conta completa, drill-down nas top 5 piores.

✅ Concluído: dados puxados.

---

## Passo 3. Classificar trilha

Aplicar a tabela da seção 2 da skill:

- Perpétuo + ticket ≤ R$ 500 → `perpetuo_low` (janelas 1d/3d/7d)
- Perpétuo + ticket R$ 501 a 1.499 → `perpetuo_mid` (janelas 3d/7d/14d)
- Perpétuo + ticket ≥ R$ 1.500 → `perpetuo_high` (janelas 7d/14d/30d)
- Lançamento qualquer → `lancamento_low/mid/high` (janelas 1d/3d)

Calcular `cpa_target` ou `cpl_target` (50% do ticket por default, ou valor declarado pelo aluno).

---

## Passo 4. Verificar maturação

Aplicar regras da seção 4 da skill. Se todos os ativos estiverem imaturos, retornar:

```
Os dados ainda estão imaturos para diagnóstico:

- [Lista do que tá imaturo: campanha < X dias, conjunto com gasto < CPA target, etc.]

Próxima reanálise sugerida: [data/hora].

Roda /trafego-otimizar de novo depois desse prazo, ou me peça um
diagnóstico parcial sabendo que a confiabilidade é baixa.
```

Se há ativos maduros, prosseguir.

---

## Passo 5. Diagnóstico de tendência (3 janelas)

Aplicar tabela da seção 5.1 da skill. Cruzar curta × média × longa para classificar:
- `estavel_performando`
- `esfriando_ou_ruido`
- `recuperando`
- `ruim_estrutural`
- `saturacao`
- `entrega_limitada`

---

## Passo 6. Diagnóstico de gargalo (cadeia de causa)

Aplicar a árvore de decisão da seção 5.2 da skill. Subir do criativo até o checkout, identificando onde quebra:
- `criativo` (CTR baixo)
- `tecnico` (Connect Rate < 70%)
- `pagina` (Conversão da Página crítica)
- `checkout` (Carrinho → Compra ou Checkout → Compra crítico, perpétuo)
- `leilao_audiencia` (CPM alto)
- `saturacao` (Frequência > 3,5)
- `nenhum` (tudo saudável → avaliar prontidão para escala)

---

## Passo 7. Montar plano de ações

Para cada ativo (anúncio, conjunto, campanha), montar `acoes_recomendadas` conforme seções 6 e 7 da skill:

- **Reduzir –20%** se CPA/CPL na média 1,3 a 1,7× target ou gargalo fora do Meta + gasto improdutivo
- **Pausar anúncio** se gargalo é criativo e gasto ≥ 1,5× CPA sem conversão (ou CTR < 0,5%, hook < 15%, etc.)
- **Pausar conjunto** se CPA/CPL longa ≥ 1,7× target
- **Pausar campanha** se ≥ 70% conjuntos pausados ou CPA/CPL ≥ 2× target nas 3 janelas
- **Refresh criativo** se saturação (frequência > 3,5)
- **Alertar usuário** (sem ação no Meta) se gargalo é página, checkout ou técnico
- **Aguardar** se ativo imaturo

Cada ação carrega:
- `nivel`: ad | adset | campaign | alerta_usuario
- `tool_call`: nome + parâmetros prontos para a Marketing API
- `justificativa`: texto curto referenciando o gargalo identificado
- `prioridade`: alta | media | baixa
- `aguardar_horas_apos`

Bloqueios à mudança de orçamento:
- Conjunto em fase de aprendizado ativa
- Última edição < 48h
- Gasto do dia < 50% do orçamento

---

## Passo 8. Avaliar prontidão para escala

Se `diagnostico_tendencia: estavel_performando` E `diagnostico_gargalo: nenhum`, aplicar checklist completo da seção 12 da skill. Se todas as condições passam, emitir bloco `sinal_para_escala.pronta: true` com:
- `modo_recomendado` (vertical, horizontal, vertical_e_horizontal)
- `velocidade_sugerida` (conservadora, normal, agressiva)
- `janela_referencia`
- `margem_de_seguranca`
- `riscos_observados`
- `criativos_de_backup_disponiveis`

---

## Passo 9. Apresentar diagnóstico ao aluno

Mostrar em formato legível (não YAML cru):

```
🔍 DIAGNÓSTICO. [Nome da Campanha]

Trilha: [perpetuo_low | ...]
Métrica-norte: [CPA | CPL]
Target: R$ [valor]
Atual (janela média): R$ [valor]   ([+/-X% do target])

Tendência: [estavel_performando | ...]
Gargalo: [criativo | tecnico | pagina | checkout | leilao_audiencia | saturacao | nenhum]
Gargalo dentro do Meta: [Sim | Não]

═══════════════════════════════════════
AÇÕES RECOMENDADAS (em ordem de prioridade)
═══════════════════════════════════════

🔴 ALTA
1. [Pausar anúncio "[nome]" / Reduzir orçamento conjunto X em 20% / etc.]
   Por quê: [justificativa baseada no gargalo]
   Aguardar [N]h antes da próxima ação no mesmo objeto.

🟡 MÉDIA
2. ...

🟢 BAIXA / OBSERVAR
3. ...

[Se há alertas fora do Meta]
═══════════════════════════════════════
ALERTAS (gargalo fora do Meta)
═══════════════════════════════════════
- [Página / Checkout / Técnico]: [descrição do problema]
  Sugestão: [/feedback-pagina | /pagina-checkout | /pagina-performance]
  Não pausar a campanha enquanto isso. Reduzir –20% como contenção.

[Se sinal_para_escala.pronta=true]
═══════════════════════════════════════
✅ PRONTA PARA ESCALAR
═══════════════════════════════════════
- Modo recomendado: [vertical | horizontal | ...]
- Velocidade sugerida: [conservadora | normal | agressiva]
- Margem de segurança: [X%] abaixo do target
- Backup de criativos saudáveis: [N]
- Riscos a monitorar: [...]

→ Para escalar agora: /trafego-escalar
```

---

## Passo 10. Aprovação e execução das ações

Pedir aprovação:
```
Quer que eu aplique as ações de prioridade ALTA agora?

1. Sim, aplicar todas
2. Só algumas (eu escolho)
3. Não, só queria o diagnóstico

Digite o número:
```

- **Opção 1:** executar cada `tool_call` na ordem de prioridade. Aguardar entre ações se a janela mínima exigir.
- **Opção 2:** listar as ações com checkbox e deixar aluno escolher.
- **Opção 3:** encerrar com diagnóstico salvo.

Para cada execução:
- Anunciar: `⏳ Aplicando: [ação]...`
- Após sucesso: `✅ [ação] aplicada.`
- Em caso de erro: `⚠️ [ação] falhou: [motivo]. Continuando com as demais.`

---

## Passo 11. Salvar diagnóstico

Salvar em:
```
meus-produtos/{ativo}/entregas/trafego/diagnostico-{campanha-slug}-{YYYY-MM-DD}.md
```

Conteúdo: o diagnóstico completo + ações aplicadas + próximas observações.

Caminho absoluto: `{raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\diagnostico-{...}.md`

---

## Passo 12. Próximos passos

Mostrar ao aluno o bloco recomendado, escolhendo o ramo conforme o sinal `sinal_para_escala.pronta` calculado no Passo 9:

**Se `sinal_para_escala.pronta = true`:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-escalar
A campanha emitiu sinal de prontidão. Use modo {modo_recomendado}
e velocidade {velocidade_sugerida} (vieram no diagnóstico).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Se `sinal_para_escala.pronta = false`:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: aguardar 48h e voltar pra /trafego-analise
A campanha ainda não está pronta pra escalar. Aguarde 48h após as
ações aplicadas e rode /trafego-analise pra ver se as métricas se
recuperaram. Motivos da não prontidão: {motivo_se_nao_pronta}.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Em seguida, listar alternativas pra contextos específicos:

```
Outras opções conforme o contexto:

- Para ver dados atualizados antes do prazo: /trafego-insights
- Se o gargalo é página, checkout ou técnico: /feedback-pagina,
  /pagina-checkout ou /pagina-performance.
```

---

## Princípios que este command nunca viola

1. **Diagnóstico antes de ação.** Sempre roda tendência + gargalo antes de propor.
2. **Mudanças graduais.** Orçamento move em ±20%, nunca mais.
3. **Aguardar 48h** entre ajustes no mesmo objeto.
4. **Não pausa por gargalo fora do Meta.** Alerta o aluno, mantém estrutura viva.
5. **Bottom-up.** Investigar criativo antes de conjunto, conjunto antes de campanha.
6. **Não escala.** Quem cresce orçamento é `/trafego-escalar`. Aqui só emite sinal de prontidão.
7. **Cooldown de 7d (low/mid e lançamento) ou 14d (high)** após handoff de descida da escala.
8. **Apenas dados nativos do Gerenciador.** Sem tracking custom.
