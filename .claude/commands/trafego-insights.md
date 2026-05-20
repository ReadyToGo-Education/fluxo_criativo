---
name: workshop-marketing:trafego-insights
description: Lê métricas de campanhas Meta Ads (Facebook + Instagram) com cálculo automático de métricas derivadas (connect rate, taxa de conversão por etapa, custo por etapa, hook rate). Modo campanha única ou conta completa com ranking de urgência. É a fonte única de leitura que /trafego-otimizar, /trafego-escalar e /trafego-analise consomem. Use quando o aluno pedir "como está performando", "me mostra os números", "qual o CPA", "quanto gastei", "puxar relatório", "quais campanhas estão ativas".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
user-invocable: false
---

# Trafego Insights. Leitura de Métricas Meta Ads

Lê dados de campanhas, conjuntos e anúncios do Meta Ads e calcula métricas derivadas que diferenciam diagnóstico raso de diagnóstico sênior. Não toma decisão. Apenas entrega dado bem formatado para o aluno olhar ou para outras skills (`/trafego-otimizar`, `/trafego-escalar`, `/trafego-analise`) consumirem.

A especificação técnica completa está em `.claude/skills/trafego-insights/SKILL.md`. Este command é o orquestrador que pede o contexto necessário, valida a conexão e invoca a skill.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo`. Se existir, leia também `meus-produtos/{ativo}/perfil.md` para inferir `ticket_brl` e `tipo_funil` quando o aluno não declarar.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia `META_AUTH_MODO` no `.env`.

- **Se vazio ou ausente:** acione `/trafego-conexao` antes de prosseguir. Não tente adivinhar nem cair em fallback. Esta verificação é o passo zero de toda skill `/trafego-*`.
- **Se `MCP_CONECTOR`:** confirmar que pelo menos uma tool com prefixo `mcp__*__ads_*` está disponível. Se nenhuma estiver, pedir ao aluno para reabrir o Claude Code (MCP recém-adicionado às vezes precisa de reload). Se persistir, voltar a `/trafego-conexao` para diagnosticar.
- **Se `APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem no `.env`. Se faltar algum, acionar `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

### 0.3 Selecao de conta de anuncio (multi-conta)

Apos a validacao da conexao, decidir qual conta usar:

1. Ler `FB_AD_ACCOUNT_IDS` no `.env`. Lista de IDs separados por virgula.
2. Se `FB_AD_ACCOUNT_IDS` nao existe ou esta vazio, usar `FB_AD_ACCOUNT_ID` direto.
3. Se `FB_AD_ACCOUNT_IDS` tem **1 conta**, usar `FB_AD_ACCOUNT_ID` direto sem perguntar.
4. Se `FB_AD_ACCOUNT_IDS` tem **2 ou mais contas**, perguntar:

   ```
   Qual conta de anuncio voce quer usar?

   1. {nome_conta_1} ({id_1})  ← padrao
   2. {nome_conta_2} ({id_2})
   3. {nome_conta_3} ({id_3})

   Digite o numero ou aperte Enter para usar a padrao:
   ```

   Para mostrar os nomes amigaveis das contas, fazer 1 chamada na Graph API:
   ```bash
   curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name&limit=100&access_token=TOKEN"
   ```
   Filtrar apenas as que estao em `FB_AD_ACCOUNT_IDS`. Marcar como "padrao" a que esta em `FB_AD_ACCOUNT_ID`.

5. Salvar a conta escolhida em variavel local da execucao (`AD_ACCOUNT_ID_ATUAL`). Nao sobrescrever o `.env`.

### 0.3 Ler especificação da skill
Leia `.claude/skills/trafego-insights/SKILL.md` para carregar a lógica completa de cálculo de métricas, janelas por trilha, métricas derivadas e formato de output. Esta skill é a fonte de verdade.

---

## Passo 1. Modo de leitura

Pergunte:

```
O que você quer ver?

1. Campanha específica (eu te dou o ID ou o nome)
2. Conta inteira (todas as campanhas ativas, com ranking de urgência)
3. Comparar duas campanhas

Digite o número:
```

- **Opção 1:** ir para Passo 2A.
- **Opção 2:** ir para Passo 2B.
- **Opção 3:** repetir Passo 2A duas vezes e gerar comparativo no Passo 4.

---

## Passo 2A. Identificar a campanha

```
Me passa o ID ou o nome da campanha.

(Se não souber o ID, pode colar o nome que eu busco. Se quiser ver
a lista, eu listo as campanhas ativas da conta primeiro.)
```

- **Se aluno colar ID** (numérico, ~17 dígitos): seguir.
- **Se aluno colar nome:** chamar a skill em modo `escopo: conta_completa` apenas para listar campanhas e pedir confirmação do match.
- **Se aluno pedir lista:** chamar listagem rápida (Fase de listagem do modo conta completa, sem drill-down) e mostrar com IDs.

---

## Passo 2B. Conta completa

Pergunte:

```
Quer drill-down nas campanhas críticas?

1. Sim (puxa as 3 janelas e detalha conjuntos e anúncios das top 5
   piores. Mais demorado mas mais útil)
2. Não (só ranking de urgência, mais rápido)

Digite o número:
```

---

## Passo 3. Inputs derivados

Antes de chamar a skill, preencha os inputs:

### 3.1 `ticket_brl`
1. Se o aluno declarou explicitamente, usar.
2. Se não, tentar inferir do `perfil.md` do produto ativo.
3. Se não conseguir inferir, perguntar:
   ```
   Qual o ticket do produto que essa campanha vende?
   (ex: R$47, R$497, R$1.997)
   ```

### 3.2 `tipo_funil`
1. Se o aluno declarou (perpétuo, lançamento), usar.
2. Se não, tentar inferir do `objective` da campanha (`OUTCOME_SALES` → `perpetuo_venda_direta`, `OUTCOME_LEADS` → `lancamento_captacao`).
3. Se ainda ambíguo, perguntar:
   ```
   Essa campanha é de:

   1. Venda direta (perpétuo, otimização por compra)
   2. Captação de leads (lançamento)

   Digite o número:
   ```

### 3.3 `janela_atribuicao`
- Tentar detectar via `attribution_spec` da ad account.
- Default `7d_click` se não encontrar.
- Aceitar override se o aluno declarar (ex: "puxa com atribuição de 1 dia").

### 3.4 Janelas
- Derivar automaticamente da trilha (low/mid/high × perpétuo/lançamento).
- Se aluno pedir janela custom (`data_inicio` + `data_fim`), respeitar.

---

## Passo 4. Execução

🔍 Próximo passo: puxar dados da Graph API e calcular métricas derivadas. Tempo estimado: cerca de 30 segundos.

Aplicar a especificação da skill `.claude/skills/trafego-insights/SKILL.md`:

1. Detectar atribuição da conta.
2. Puxar as 3 janelas da trilha (em paralelo quando possível).
3. Calcular métricas derivadas (connect rate, taxa de conversão da página, taxa de conversão do anúncio, taxas de carrinho/checkout, custo por etapa).
4. Marcar `confiabilidade` (baixa/media/alta) por janela com base no volume de eventos.
5. Tratar denominadores zero como `null`.
6. Se modo conta completa, ranquear por urgência e fazer drill-down nas top 5.

✅ Concluído: dados puxados e métricas calculadas.

---

## Passo 5. Apresentar ao aluno

Apresentar em formato legível (não YAML cru). Estrutura sugerida:

### 5.1 Modo campanha única

```
📊 [Nome da Campanha]

Trilha: [perpetuo_low | perpetuo_mid | perpetuo_high | lancamento_*]
Janela de atribuição: [7d_click | 1d_click | ...]
Status: [ACTIVE | PAUSED]
Budget diário: R$ [valor]

═══════════════════════════════════════
JANELA CURTA ([1d|3d|7d])
═══════════════════════════════════════
Spend: R$ [valor]
[CPA | CPL]: R$ [valor] (target: R$ [valor], desvio: [+X% | -X%])
CTR link: [X,XX%]
Hook rate: [X,XX%]
Frequência: [X,X]
CPM: R$ [valor]

Eventos:
- Cliques no link: [N]
- LP Views: [N]
- Add to Cart: [N]
- Initiate Checkout: [N]
- Purchases: [N]

Métricas derivadas:
- Connect rate: [X,XX%]   (cliques que viram LP View)
- Conversão da página: [X,XX%]   (LP Views que viram compra/lead)
- Conversão do anúncio: [X,XX%]   (cliques que viram compra/lead)
- Carrinho → Compra: [X,XX%]   (só perpétuo)
- Checkout → Compra: [X,XX%]   (só perpétuo)

Custo por etapa:
- Por LP View: R$ [valor]
- Por Add to Cart: R$ [valor]
- Por Initiate Checkout: R$ [valor]
- Por Purchase: R$ [valor]

Confiabilidade: [baixa | media | alta]

═══════════════════════════════════════
JANELA MÉDIA / LONGA (mesma estrutura)
═══════════════════════════════════════

Conjuntos: [N] ativos
Anúncios: [N] ativos

[Se aluno pediu drill-down: listar conjuntos e anúncios com mesma estrutura]
```

### 5.2 Modo conta completa

```
📊 Conta inteira. [N] campanhas ativas, [N] drill-down

Janela de atribuição: [valor]
Total gasto no período: R$ [valor]

🔴 CRÍTICAS ([N]) — CPA/CPL ≥ 1,7× target
1. [Nome]   CPA R$ [valor] (target R$ [valor], +[X]%)
2. ...

🟡 ATENÇÃO ([N]) — CPA/CPL 1,3 a 1,7× target
1. [Nome]   ...

🟢 SAUDÁVEIS ([N]) — CPA/CPL ≤ target
1. [Nome]   ...

[Se drill-down: detalhar top 5 piores em sequência]
```

### 5.3 Modo comparativo

```
📊 [Campanha A] × [Campanha B]

                          A             B
Spend (7d)                R$ [valor]    R$ [valor]
CPA / CPL                 R$ [valor]    R$ [valor]
CTR link                  [X,XX%]       [X,XX%]
Hook rate                 [X,XX%]       [X,XX%]
Frequência                [X,X]         [X,X]
Connect rate              [X,XX%]       [X,XX%]
Conversão da página       [X,XX%]       [X,XX%]
Conversão do anúncio      [X,XX%]       [X,XX%]

Vencedora na métrica-norte: [A | B]
Diferença: [X% | X reais]
```

---

## Passo 6. Próximos passos

Após mostrar os dados, sugira:

```
Próximos passos:

- Para diagnosticar e propor ajustes: /trafego-otimizar
- Para escalar uma campanha que está performando: /trafego-escalar
- Para análise narrada com terminologia VTSD (Mandala, Furadeira,
  Identidades): /trafego-analise
- Para puxar os mesmos dados em outra janela: roda /trafego-insights
  de novo (cache de 5 min, então repete sem custo)
```

---

## Passo 7. Salvar (opcional)

Se o aluno quiser arquivar a leitura, perguntar:

```
Quer salvar essa leitura como referência?

1. Sim, salvar
2. Não, só queria ver

Digite o número:
```

Se sim, salvar em:
```
meus-produtos/{ativo}/entregas/trafego/insights-{campanha-ou-conta}-{YYYY-MM-DD}.md
```

Conteúdo: a apresentação do Passo 5 em markdown puro.

Caminho absoluto a exibir: `{raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\insights-{...}.md`

---

## Cache e re-execução

A skill mantém cache de 5 minutos por campanha (chave: `object_id` + `nivel` + `janelas` + `janela_atribuicao`). Se o aluno rodar `/trafego-insights` na mesma campanha duas vezes em menos de 5 min, retorna do cache.

Para forçar dado fresco, o aluno pode dizer "puxa de novo sem cache" ou "atualiza dados". Se outro command `/trafego-*` editou a campanha (pause, update budget, duplicate), o cache é invalidado automaticamente.

---

## Princípios que este command nunca viola

1. **Nunca seguir sem `META_AUTH_MODO` configurado.** Aciona `/trafego-conexao` antes.
2. **Nunca tomar decisão.** Só entrega dado. Diagnóstico mora em `/trafego-otimizar`.
3. **Sempre declarar a janela de atribuição** no output. Sem isso, dado não tem significado.
4. **Sempre cruzar 3 janelas da trilha** quando o tipo de funil e ticket são conhecidos.
5. **Nunca chamar tool de edição.** Leitura é leitura.
6. **Nunca inventar métricas.** Se a Graph API não retornou, marcar `null` ou `dados_disponiveis: false`.
7. **Em modo conta completa, falha parcial preserva o relatório das outras campanhas.**
