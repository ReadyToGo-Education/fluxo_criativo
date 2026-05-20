---
name: workshop-marketing:trafego-escalar
description: Escala campanhas Meta Ads já validadas e performando, sem destruir aprendizado. Cobre 4 modos (vertical, horizontal, vertical+horizontal, consolidação CBO) e 3 velocidades (conservadora +15%/72h, normal +20%/48h, agressiva +30 a +50%/24h). Revalida critérios de gatilho a cada incremento, aplica freios escalonados (leve, médio, total) e devolve handoff para /trafego-otimizar quando freio total aciona. Recusa rodar sem sinal de prontidão. Use quando o aluno pedir "escalar campanha", "aumentar budget", "subir verba", "duplicar conjunto vencedor", "expandir audiência", "consolidar em CBO", ou quando /trafego-otimizar emitiu sinal_para_escala.pronta=true.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Trafego Escalar. Crescimento Controlado de Campanhas Meta Ads

> **Esta skill é acionada automaticamente pelo `/trafego-otimizar`**, não pelo usuário diretamente.
> O fluxo correto é: rodar `/trafego-otimizar` → quando a campanha estiver pronta, a skill de escala é invocada automaticamente com o sinal de prontidão preenchido.
>
> Se você chegou aqui diretamente, encerre e execute `/trafego-otimizar` primeiro.

---

Escala campanhas Meta Ads já validadas, com incrementos graduais e revalidação contínua. Aplica freios escalonados quando a performance degrada, devolve handoff para `/trafego-otimizar` quando freio total aciona. Não escala campanha sem sinal de prontidão.

A especificação técnica completa está em `.claude/skills/trafego-escalar/SKILL.md`. Este command é o orquestrador.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo` e `perfil.md`.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia `META_AUTH_MODO` no `.env`.

- **Se vazio ou ausente:** acione `/trafego-conexao` antes de prosseguir. Não tente adivinhar nem cair em fallback. Esta verificação é o passo zero de toda skill `/trafego-*`.
- **Se `MCP_CONECTOR`:** confirmar que pelo menos uma tool com prefixo `mcp__*__ads_*` está disponível. Se nenhuma estiver, pedir ao aluno para reabrir o Claude Code (MCP recém-adicionado às vezes precisa de reload). Se persistir, voltar a `/trafego-conexao` para diagnosticar.
- **Se `APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem no `.env`. Se faltar algum, acionar `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

### 0.3 Selecao de conta de anuncio (multi-conta)

Apos a validacao da conexao, decidir qual conta tocar para escalar:

1. Ler `FB_AD_ACCOUNT_IDS` no `.env`. Lista de IDs separados por virgula.
2. Se `FB_AD_ACCOUNT_IDS` nao existe ou esta vazio, usar `FB_AD_ACCOUNT_ID` direto.
3. Se `FB_AD_ACCOUNT_IDS` tem **1 conta**, usar `FB_AD_ACCOUNT_ID` direto sem perguntar.
4. Se `FB_AD_ACCOUNT_IDS` tem **2 ou mais contas**, perguntar:

   ```
   Qual conta de anuncio voce quer escalar?

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

5. Salvar a conta escolhida em variavel local da execucao (`AD_ACCOUNT_ID_ATUAL`). Nao sobrescrever o `.env`. A escala e os freios so atuam dentro da conta escolhida.

### 0.4 Ler especificações
Leia:
- `.claude/skills/trafego-escalar/SKILL.md`. Modos, velocidades, critérios de gatilho, freios e tetos.
- `.claude/skills/trafego-otimizar/SKILL.md` (seção 12). Critérios de prontidão.

---

## Passo 1. Verificar prontidão (gate duro)

A skill **só atua** sobre campanhas que receberam sinal explícito de prontidão. Três caminhos:

### 1.1 Sinal vindo de `/trafego-otimizar`
Se o aluno acabou de rodar `/trafego-otimizar` e a saída tinha `sinal_para_escala.pronta: true`, usar esse bloco direto.

### 1.2 Acionamento manual com auditoria automática
Se o aluno pediu escala sem rodar otimização antes, executar internamente o checklist de prontidão:

1. Invocar `/trafego-insights` para puxar dados das 3 janelas da trilha.
2. Aplicar a checklist da seção 12 da skill `trafego-otimizar`:
   - CPA/CPL janela média ≤ target × 0,9
   - CPA/CPL janela longa ≤ target
   - Tendência: `estavel_performando`
   - Diagnóstico de gargalo: `nenhum`
   - Frequência ≤ 2,5 (perpétuo) ou 3,0 (lançamento)
   - Fora de fase de aprendizado
   - Pelo menos 1 criativo saudável
   - Última edição ≥ 48h
   - Histórico mínimo da trilha cumprido
   - Sem evento sazonal perturbador
   - ≥ 2 criativos saudáveis no conjunto
   - Cooldown ≥ 168h (7d perpétuo low/mid e lançamento) ou 336h (14d perpétuo high) desde último handoff de descida

Se **qualquer** condição reprovar:
```
Não posso escalar essa campanha agora. Faltou:

- [Lista das condições reprovadas]

Recomendação: rodar /trafego-otimizar primeiro para resolver os
pontos acima. Quando a campanha estiver pronta, a otimização vai
emitir o sinal e a gente escala.
```

E encerrar.

### 1.3 Modo "agressivo declarado"
Se o aluno disser "estou em lançamento captação inicial/final" ou "Black Friday" ou "data comemorativa" ou "lançamento competidor relevante", aceitar critérios relaxados. Confirmar explicitamente:

```
Você está declarando contexto de [lançamento captação X | sazonal Y].
Vou aplicar critérios relaxados de prontidão e velocidade agressiva
(+30 a +50% / 24h). Confirma?

1. Sim, confirmo o contexto
2. Não, prefiro velocidade normal

Digite o número:
```

---

## Passo 2. Inputs

Confirmar com o aluno:

### 2.1 Velocidade
```
Velocidade de escala:

1. Conservadora (+15% a cada 72h). High ticket, audiência pequena.
2. Normal (+20% a cada 48h). Default. Perpétuo low/mid.
3. Agressiva (+30 a 50% a cada 24h). Lançamento captação ou sazonal
   declarado. Exige ≥3 criativos backup.

Digite o número:
```

Se aluno escolher agressiva e não estiver em contexto declarado, recusar.

### 2.2 Modo
Sugerir baseado nos dados (frequência, audiência, ciclo atual). Mostrar:
```
Modo de escala:

Sugestão da skill: [vertical | horizontal | vertical_e_horizontal]
Por quê: [justificativa baseada em frequência/audiência/ciclo]

1. Aceitar a sugestão
2. Vertical (mesmo conjunto, mais orçamento)
3. Horizontal (duplicar conjunto com nova segmentação)
4. Vertical + Horizontal alternado
5. Consolidação em CBO (3+ conjuntos vencedores)

Digite o número:
```

### 2.3 Teto operacional (opcional)
```
Tem um teto de orçamento diário operacional para essa campanha?
(ex: "máximo R$ 500/dia", ou pular para sem teto)
```

### 2.4 Backup criativo
Confirmar que há criativos saudáveis disponíveis:
```
Quantos criativos saudáveis (CTR ≥ saudável) estão ativos no conjunto
hoje? Preciso de mínimo 2 (ou 3 se velocidade agressiva).
```

---

## Passo 3. Calcular incremento

Aplicar a tabela da seção 4 da skill:

| Velocidade | Incremento | Janela entre ajustes |
|---|---|---|
| Conservadora | +15% | 72h |
| Normal | +20% | 48h |
| Agressiva | +30 a +50% | 24h |

Calcular novo orçamento:
- Vertical: `novo_orcamento = orcamento_atual × (1 + incremento_pct/100)`
- Horizontal: identificar audiência adjacente (lookalike outra %, advantage+, audiência fria similar) e duplicar conjunto com mesmo orçamento e novo público.
- CBO: criar campanha CBO duplicando 3+ conjuntos vencedores.

Verificar se algum teto operacional não é violado.

---

## Passo 4. Mostrar plano e pedir aprovação

```
Plano de escala:

Campanha: [nome]
Trilha: [perpetuo_low | ...]
CPA/CPL atual: R$ [valor] (target: R$ [valor], margem: [X%] abaixo)
Frequência atual: [X,X]
Modo escolhido: [vertical | horizontal | ...]
Velocidade: [conservadora | normal | agressiva]
Ciclo: [N] (incrementos já feitos nessa onda)

Ação:
- [Vertical] Subir orçamento do conjunto "[nome]" de R$ [atual] para
  R$ [novo] (+[X%]).
- [Horizontal] Duplicar conjunto "[nome]" com [nova audiência], orçamento
  R$ [valor].
- [CBO] Criar nova campanha CBO consolidando os conjuntos vencedores X, Y, Z.

Próxima revisão: em [N]h.
Próxima reavaliação automática: [data/hora].

1. Confirmar e aplicar
2. Ajustar valores
3. Cancelar

Digite o número:
```

---

## Passo 5. Execução

🔍 Próximo passo: aplicar incremento via Marketing API. Tempo estimado: cerca de 30 segundos.

Conforme modo:
- **Vertical:** `POST /adset/{id}` com `daily_budget` ou `lifetime_budget` atualizado.
- **Horizontal:** `POST /act_{id}/adsets` (duplicação) ou `POST /adset/{id}/copies` se a tool MCP tiver o equivalente.
- **CBO:** `POST /act_{id}/campaigns` (nova com `budget_optimization: true`) + `POST /act_{id}/adsets` × N (sem orçamento próprio, com `campaign_id` apontando pra nova).

Em caso de falha, registrar e devolver erro detalhado.

✅ Concluído: incremento aplicado.

---

## Passo 6. Apresentar resultado

```
✅ Escala aplicada (ciclo [N]).

[Vertical: Conjunto "[nome]" agora com R$ [novo]/dia (+[X%])]
[Horizontal: Novo conjunto criado: "[nome novo]" com R$ [valor]/dia,
  audiência [descrição]]
[CBO: Nova campanha CBO "[nome]" criada com N conjuntos consolidados]

Riscos a monitorar:
- [frequência subindo, monitorar próximo ciclo]
- [audiência horizontal precisa maturar antes de novo ciclo]
- [...]

Próxima revisão: [data/hora] (em [N]h).

Antes do próximo incremento, vou revalidar:
- CPA/CPL na janela média ≤ target × 0,9
- Frequência ≤ 2,5 (perpétuo) ou ≤ 3,0 (lançamento)
- Tendência ainda estável
- Sem freio leve/médio acionado

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-analise
Após D+7 (perpétuo low/mid e lançamento) ou D+14 (perpétuo high),
volte pra /trafego-analise pra confirmar se a escala se sustentou
e identificar o próximo movimento.

Em caso de freio total acionado nesta sessão: o handoff
automático aponta pra /trafego-otimizar — siga por lá.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para ver dados antes do prazo: /trafego-insights.
```

---

## Passo 7. Tratamento de freios (em ciclos seguintes)

Quando o aluno volta para um próximo incremento, antes de tudo:

1. Invocar `/trafego-insights` para puxar dados frescos (sem cache).
2. Comparar com último ciclo:
   - CPA/CPL piorou 10 a 20% janela curta vs média? → **freio leve** (não incrementar, manter, reavaliar 48h)
   - CPA/CPL piorou 20 a 30% sustentado por 48h? → **freio médio** (reverter –20%, refresh criativo, devolver pra `/trafego-otimizar`)
   - CPA/CPL piorou ≥ 30% OU 2 ciclos sem ganho líquido OU saturação estrutural? → **freio total** (reverter ao último orçamento estável, emitir handoff)
   - Frequência > 4 após 2 refreshes? → **teto de audiência** (parar, expandir trilha)
   - CPM 50%+ acima histórico por 7d sem sazonal? → **CPM ceiling**
   - 3 ciclos sem ganho de conversões? → **volume ceiling**
   - Atingiu `teto_de_orcamento_diario_brl` declarado? → **teto operacional**

### 7.1 Freio leve
```
🟡 Freio leve acionado.

CPA/CPL piorou [X%] na janela curta vs média. Não vou aplicar o
próximo incremento agora. Mantenho o orçamento atual e reavalio
em 48h.

Próxima reavaliação: [data/hora].
```

### 7.2 Freio médio
```
🟠 Freio médio acionado.

CPA/CPL piorou [X%] sustentado por 48h. Vou:

1. Reverter o último incremento (orçamento volta para R$ [valor]).
2. Sugerir refresh criativo via /copy-anuncio + /criativo-estatico.
3. Devolver diagnóstico para /trafego-otimizar.

Aplicar agora?

1. Sim, aplicar
2. Não, vou pensar

Digite o número:
```

### 7.3 Freio total
```
🔴 Freio total acionado.

[Motivo: CPA piorou 30%+ / 2 ciclos sem ganho / saturação estrutural]

Vou:
1. Reverter ao último orçamento estável (R$ [valor]).
2. Devolver a campanha para /trafego-otimizar com handoff.
3. Desativar /trafego-escalar para essa campanha até o cooldown
   vencer ([7d perpétuo low/mid | 14d perpétuo high | 24h lançamento]).

Próximo passo: /trafego-otimizar para diagnóstico do que aconteceu.

Confirma reverter e fazer handoff?

1. Sim
2. Não, prefiro pausar e analisar manualmente
```

### 7.4 Teto atingido
```
🚫 Teto de escala atingido.

Tipo: [audiencia_exausta | cpm_ceiling | volume_ceiling | operacional]

[Descrição do que foi observado]

Recomendação:
- [Audiência exausta] Expandir para nova trilha de público.
  Sugestão: criar campanha nova com audiência fria adjacente
  ou outra geografia via /trafego-criar-campanha.
- [CPM ceiling] Considerar pausa temporária e retomada em
  período de menor concorrência.
- [Volume ceiling] Mercado endereçável atingido. Buscar nova
  fonte de demanda (público novo, oferta nova).
- [Operacional] Teto declarado pelo aluno. Reabrir teto se
  o ROI compensa, ou parar por aqui.

Skill de escala desativada para essa campanha.
```

---

## Passo 8. Salvar registro

Salvar em:
```
meus-produtos/{ativo}/entregas/trafego/escala-{campanha-slug}-ciclo-{N}-{YYYY-MM-DD}.md
```

Conteúdo: estado atual + ação aplicada + riscos + próxima revisão.

Caminho absoluto: `{raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\escala-{...}.md`

---

## Princípios que este command nunca viola

1. **Recusa rodar sem sinal de prontidão.** Gate duro.
2. **Incrementos respeitam velocidade declarada.** Nunca pular degraus.
3. **+50% é teto absoluto** de incremento único, mesmo em modo agressivo.
4. **Backup criativo obrigatório** para velocidade agressiva (≥ 3).
5. **Revalidar gatilho** antes de cada incremento. Não é piloto automático.
6. **Freio é prioridade sobre crescimento.** Qualquer degradação para a escala.
7. **Devolução clara para `/trafego-otimizar`** quando freio total aciona.
8. **Cooldown de 7d/14d/24h** após handoff de descida.
9. **Não diagnostica gargalos fora da escala.** Devolve para a otimização.
10. **Tetos são declarados, não ignorados.** Atingir, parar, comunicar.
