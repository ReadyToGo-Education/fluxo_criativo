---
name: workshop-marketing:trafego-escalar
description: Escala campanhas Meta Ads já validadas e performando, sem destruir aprendizado. Cobre 6 modos (vertical, horizontal, vertical+horizontal, consolidação CBO, campanha Advantage, carteira) e 3 velocidades (conservadora +15%/72h, normal +20%/24h, agressiva +30 a +50%/24h). Revalida critérios de gatilho a cada incremento (incluindo lucro/dia ≥ 0 quando a margem é coletada), calcula o risco de cada incremento, protege o caixa da conta sob teto, aplica freios escalonados (leve, médio, total) e devolve handoff para /trafego-otimizar quando o freio total aciona. Recusa rodar sem sinal de prontidão. Use quando o aluno pedir "escalar campanha", "aumentar budget", "subir verba", "duplicar conjunto vencedor", "expandir audiência", "consolidar em CBO", "campanha Advantage", ou quando /trafego-otimizar emitiu sinal_para_escala.pronta=true.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Trafego Escalar. Crescimento Controlado de Campanhas Meta Ads

> **Caminho recomendado:** rodar `/trafego-otimizar` primeiro. Quando a otimização emite `sinal_para_escala.pronta=true`, ela oferece montar o plano de escala na hora e, com o ok do aluno, aciona esta skill com o payload do diagnóstico: a escala recebe o bastão sem repetir a auditoria.
>
> **Invocação direta também funciona.** Se o aluno chamar `/trafego-escalar` sem ter rodado a otimização antes, a skill executa a validação do dado (Passo 0.78) e o checklist de prontidão (Passo 0.8) e só prossegue se a campanha passar. Caso contrário, devolve o que falta e encaminha pra `/trafego-otimizar`.

---

Escala campanhas Meta Ads já validadas, com incrementos graduais e revalidação contínua. Aplica freios escalonados quando a performance degrada, devolve handoff para `/trafego-otimizar` quando o freio total aciona. Não escala campanha sem sinal de prontidão.

A especificação técnica completa está em `.claude/skills/trafego-escalar/SKILL.md`. Este command é o orquestrador.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md, seção "Contexto Persistente do Negócio"). Do resumo saem o **ticket** (preço do produto) e o **tipo** (Low, Middle ou High Ticket). Não pergunte o que o resumo já tem.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia `META_AUTH_MODO` no `.env`.

- **Se vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive o legado `HIBRIDO`): acione `/trafego-conexao` e aguarde a conclusão. Não tente adivinhar nem cair em fallback. Esta verificação é o passo zero de toda skill `/trafego-*`.
- **Se `MCP_CONECTOR`:** confirmar que pelo menos uma tool `ads_*` do conector está disponível (descobrir pelo final do nome; o prefixo varia). Se nenhuma estiver, pedir ao aluno para reabrir o Claude Code (MCP recém-adicionado às vezes precisa de reload). Se persistir, voltar a `/trafego-conexao` para diagnosticar. Conferir também que `FB_AD_ACCOUNT_ID` tem valor (`grep -q "^FB_AD_ACCOUNT_ID=." .env`); se faltar, a opção "Validar" do `/trafego-conexao` completa. Se a Meta responder que a conta ainda não foi liberada no conector, avisar em linguagem simples e oferecer trocar para o modo App pelo `/trafego-conexao`.
- **Se `APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem com valor no `.env` (`grep -q "^FB_ACCESS_TOKEN_PERMANENTE=." .env` e `grep -q "^FB_AD_ACCOUNT_ID=." .env`; com o ponto, linha vazia conta como ausente; nunca exibir o valor). Se faltar algum, acionar `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

### 0.3 Seleção de conta de anúncio (multi-conta)

Após a validação da conexão, decidir qual conta tocar para escalar:

1. Ler `FB_AD_ACCOUNT_IDS` no `.env`. Lista de IDs separados por vírgula.
2. Se `FB_AD_ACCOUNT_IDS` não existe ou está vazio, usar `FB_AD_ACCOUNT_ID` direto.
3. Se `FB_AD_ACCOUNT_IDS` tem **1 conta**, usar `FB_AD_ACCOUNT_ID` direto sem perguntar.
4. Se `FB_AD_ACCOUNT_IDS` tem **2 ou mais contas**, perguntar:

   ```
   Qual conta de anúncio você quer escalar?

   1. {nome_conta_1} ({id_1})  ← padrão
   2. {nome_conta_2} ({id_2})
   3. {nome_conta_3} ({id_3})

   Digite o número ou aperte Enter para usar a padrão:
   ```

   Para mostrar nomes amigáveis: no MCP, `ads_get_ad_accounts` (nome em `ad_account_name`); no APP, uma chamada `GET /me/adaccounts?fields=id,account_id,name&limit=100` na Graph API com `access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)` dentro do próprio `curl` (o token nunca é escrito nem exibido; se precisar mostrar o comando, `access_token=***TOKEN_MASCARADO***`). Filtrar apenas as que estão em `FB_AD_ACCOUNT_IDS`. Marcar como "padrão" a que está em `FB_AD_ACCOUNT_ID`.

5. Salvar a conta escolhida em variável local da execução (`AD_ACCOUNT_ID_ATUAL`). Não sobrescrever o `.env`. A escala e os freios só atuam dentro da conta escolhida.

### 0.4 Ler especificações
Leia:
- `.claude/skills/trafego-escalar/SKILL.md`. Modos, velocidades, confiabilidade do dado, critérios de gatilho, risco por incremento, guardião de caixa, freios e tetos.
- `.claude/skills/trafego-otimizar/SKILL.md` (seção 12). Critérios de prontidão.

---

## Passo 1. Verificar prontidão (gate duro)

A skill **só atua** sobre campanhas que receberam sinal explícito de prontidão. Três caminhos:

### 1.1 Sinal vindo de `/trafego-otimizar`
Se o aluno acabou de rodar `/trafego-otimizar` e a saída tinha `sinal_para_escala.pronta: true`, usar esse bloco direto (conta, campanha, meta e margem já vêm no payload). Duas conferências valem mesmo assim (Passo 0.1 da SKILL):
- **Cooldown:** ler `meus-produtos/{ativo}/trafego/escalar/historico-{campaign_id}.md`. Se a última linha com status `freio_total` estiver dentro do cooldown da trilha (7d perpétuo low/mid, 14d perpétuo high, 24h lançamento), não escalar: avisar a data em que a campanha libera e devolver para `/trafego-otimizar`.
- **Falso vencedor:** se o detector da `/trafego-diagnostico` rodou nesta sessão e a entidade não saiu `vencedor_real` com score de confiança 50 ou mais, não escalar e explicar o motivo, mesmo com o `pronta: true`. Com `score_confianca` de 50 a 74 (do payload ou da sessão), só velocidade conservadora ou normal, nunca agressiva (2.1). Se não foi verificado, mostrar "falso vencedor não verificado" no plano do Passo 4.

### 1.2 Acionamento manual com auditoria automática
Se o aluno pediu escala sem rodar a otimização antes, executar internamente:

1. Inputs do Passo 0.7 da SKILL: tipo de funil (inferido do objetivo), ticket (do resumo), meta de CPA/CPL (obrigatória), margem de contribuição e teto (opcional).
2. Invocar `/trafego-insights` para puxar dados das 3 janelas da trilha.
3. Validar a confiabilidade do dado (Passo 0.78 da SKILL). Confiabilidade `baixa` bloqueia a escala.
4. Aplicar o checklist da seção 12 da skill `trafego-otimizar`:
   - CPA/CPL janela média ≤ target × 0,9
   - CPA/CPL janela longa ≤ target
   - Tendência: `estavel_performando`
   - Diagnóstico de gargalo: `nenhum`
   - ROAS sustentado ≥ break-even (lucro/dia ≥ 0)
   - Frequência ≤ 2,5 (perpétuo) ou 3,0 (lançamento)
   - Fora de fase de aprendizado
   - Pelo menos 1 criativo saudável
   - Última edição ≥ 48h
   - Histórico mínimo da trilha cumprido
   - Sem evento sazonal perturbador
   - ≥ 2 criativos saudáveis no conjunto
   - Cooldown ≥ 168h (7d perpétuo low/mid), ≥ 336h (14d perpétuo high) ou ≥ 24h (lançamento) desde o último handoff de descida (última linha `freio_total` do histórico da campanha; sem arquivo, não houve descida)
   - Falso vencedor: se o detector da `/trafego-diagnostico` rodou nesta sessão, a entidade saiu `vencedor_real` com score de confiança 50 ou mais (de 50 a 74, só escala gradual, sem velocidade agressiva). Se não rodou, oferecer o detector (`/trafego-diagnostico` opção [4], só leitura); se o aluno recusar, seguir com "falso vencedor não verificado" no plano do Passo 4

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
Se o aluno disser "estou em lançamento captação inicial/final" ou "Black Friday" ou "data comemorativa" ou "lançamento de concorrente relevante", aceitar critérios relaxados. Confirmar explicitamente:

```
Você está declarando contexto de [lançamento captação X | sazonal Y].
Vou aplicar critérios relaxados de prontidão e velocidade agressiva
(+30 a +50% / 24h). Confirma?

1. Sim, confirmo o contexto
2. Não, prefiro velocidade normal

Digite o número:
```

Com score de confiança do falso vencedor de 50 a 74, a velocidade agressiva fica de fora mesmo no contexto declarado (2.1): nesse caso, a mensagem acima oferece só os critérios relaxados de prontidão, com velocidade normal ou conservadora.

---

## Passo 2. Inputs

Confirmar com o aluno:

### 2.1 Velocidade
```
Velocidade de escala:

1. Conservadora (+15% a cada 72h). High ticket, audiência pequena.
2. Normal (+20% a cada 24h). Default. Perpétuo low/mid.
3. Agressiva (+30 a 50% a cada 24h). Lançamento captação ou sazonal
   declarado. Exige ≥3 criativos backup.

Digite o número:
```

Se o aluno escolher agressiva e não estiver em contexto declarado, recusar. Recusar a agressiva também quando o detector de falso vencedor deu score de confiança de 50 a 74 (do payload da otimização ou da sessão), mesmo em contexto declarado: nessa faixa a escala é só gradual. Perpétuo mid ticket respeita 72h entre ajustes mesmo na velocidade normal (§7.2 da SKILL).

### 2.2 Modo
Sugerir baseado nos dados (frequência, audiência, ciclo atual, anúncios vencedores espalhados), pela matriz do Passo 0.75 da SKILL. Mostrar:
```
Modo de escala:

Sugestão da skill: [vertical | horizontal | vertical_e_horizontal | cbo_consolidacao | advantage_plus_consolidacao]
Por quê: [justificativa baseada em frequência/audiência/ciclo/vencedores na conta]

1. Aceitar a sugestão
2. Vertical (mesmo conjunto, mais orçamento)
3. Horizontal (duplicar conjunto com nova segmentação ou teste)
4. Vertical + Horizontal alternado
5. Consolidação em CBO (3+ conjuntos vencedores)
6. Campanha Advantage (5+ anúncios vencedores em 1 estrutura Advantage+)
7. Carteira (cortar queimadores + escalar vencedores sob teto de gasto)

Digite o número:
```

> **Lembrete Advantage:** exige no mínimo 5 anúncios vencedores no mesmo produto/funil. Vencedor segue a definição única da SKILL (Passo 0.75.1, Leitura 1): 50 conversões em low e middle ticket ou 30 em high ticket na janela média da trilha, ou `validado` num teste da `/trafego-testes`. Abaixo disso, o algoritmo Advantage+ não tem espaço de iteração suficiente: sugerir produzir mais criativos (`/copy-anuncio` + `/criativo-estatico`) e validá-los antes via `/trafego-testes`.

> **Modo Carteira:** requer teto de gasto da conta declarado pelo aluno (sem teto declarado, a Carteira não roda: pedir o teto no 2.3). Gera plano em 2 fases: Fase 1 (handoff para `/trafego-otimizar`: cortes e realocações) + Fase 2 (escalar executa: incrementos nos vencedores). A escalar NÃO executa cortes diretamente. Como o plano atravessa duas skills, só roda com o plano completo numerado e um **"aprovar tudo"** explícito (modo lote pré-aprovado do CLAUDE.md). Ver §3.6 da SKILL.

### 2.3 Teto de gasto da conta (opcional; obrigatório no modo Carteira)
```
Tem um teto de gasto diário para a conta inteira (somando todas as
campanhas) que você não quer ultrapassar?
(ex: "máximo R$ 500/dia", ou pular para sem teto)
```

Salvar em `teto_conta_diario_brl` (sempre o teto da conta inteira, nunca de uma campanha só; ver Pergunta 5 do Passo 0.7 da SKILL).

Com teto declarado (ou modo Carteira), o guardião de caixa roda no Passo 3, depois do risco (mesma ordem da SKILL: Passo 0.85 e depois 0.86).

### 2.4 Backup criativo
Confirmar que há criativos saudáveis disponíveis:
```
Quantos criativos saudáveis (CTR ≥ saudável) estão ativos no conjunto
hoje? Preciso de no mínimo 2 (ou 3 se a velocidade for agressiva).
```

Se faltar backup, sugerir produzir antes: copy em `/copy-anuncio`, imagem em `/criativo-estatico`, vídeo em `/video-heygen`, `/video-remotion` ou `/video-editar`.

---

## Passo 3. Calcular incremento e risco

🔍 Próximo passo: calcular o risco de cada incremento e, com teto declarado, conferir o caixa da conta. Tempo estimado: cerca de 75 segundos.

Aplicar a tabela da seção 4 da skill:

| Velocidade | Incremento | Janela entre ajustes |
|---|---|---|
| Conservadora | +15% | 72h |
| Normal | +20% | 24h |
| Agressiva | +30 a +50% | 24h |

Calcular novo orçamento:
- Vertical: `novo_orcamento = orcamento_atual × (1 + incremento_pct/100)`
- Horizontal: identificar audiência adjacente (lookalike de outra %, Advantage+, audiência fria similar) e duplicar o conjunto com mesmo orçamento e novo público.
- CBO: criar campanha CBO duplicando 3+ conjuntos vencedores.
- Advantage: identificar 5 a 50 anúncios vencedores do mesmo produto/funil/público-alvo declarado e montar 1 campanha Advantage+ (1 conjunto, todos os anúncios dentro). Validação obrigatória de coerência produto/funil antes de montar: anúncios de produtos diferentes na mesma estrutura Advantage geram otimização incoerente.

Calcular o **score de risco** de cada incremento (`sub-skills/risco-incremento.md`, Passo 0.85 da SKILL). Risco extremo sai do plano; risco alto entra com aviso e confirmação reforçada.

Com teto declarado (ou modo Carteira), rodar o guardião de caixa (`sub-skills/guardiao-caixa.md`, Passo 0.86 da SKILL) e verificar se o teto da conta (`teto_conta_diario_brl`) é violado. Com folga positiva menor que o incremento, reduzir o incremento até caber (guardião de caixa §5). Se o caixa estiver crítico, não escalar: recomendar cortar vazamentos primeiro pela `/trafego-otimizar`. **Exceção do modo Carteira:** a urgência é recalculada sobre o gasto projetado depois dos cortes da Fase 1, e os vazamentos que já estão na Fase 1 não contam para os "2 ou mais vazamentos". Se o caixa continuar crítico mesmo com os cortes, entregar só a Fase 1 (cortes pela `/trafego-otimizar`, no mesmo plano numerado), sem a Fase 2. O aluno nunca sai sem o plano.

---

## Passo 4. Mostrar plano e pedir aprovação (gate 🛡️)

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Plano de escala:

Campanha: [nome]
Trilha: [perpetuo_low | ...]
CPA/CPL atual: R$ [valor] (target: R$ [valor], margem: [X%] abaixo)
Lucro/dia hoje: R$ [valor] · projetado pós-incremento: ~R$ [valor] (margem [X]%)
Frequência atual: [X,X]
Modo escolhido: [vertical | horizontal | ...]
Velocidade: [conservadora | normal | agressiva]
Ciclo: [N] (incrementos já feitos nessa onda)

O que vai mudar:
- [Vertical] Subir orçamento do conjunto "[nome]" de R$ [atual] para
  R$ [novo] (+[X%]). Risco [score]/100.
- [Horizontal] Duplicar conjunto "[nome]" com [nova audiência ou teste], orçamento
  R$ [valor]/dia. Criado pausado: não gasta nada até você pedir a ativação,
  que é uma confirmação à parte. Risco [score]/100.
- [CBO] Criar nova campanha CBO consolidando os conjuntos vencedores X, Y, Z,
  orçamento R$ [valor]/dia na campanha. Criada pausada, como acima. Risco [score]/100.
- [Advantage] Criar campanha Advantage+ "[nome]" com [N] anúncios vencedores
  do mesmo produto/funil. Conjunto único com público Advantage+, orçamento R$ [valor]/dia.
  Criada pausada, como acima. Risco [score]/100.
[Se o falso vencedor não foi verificado: "· falso vencedor não verificado" ao lado do risco]

Reset de aprendizado esperado: [não no vertical | sim nas estruturas novas]
Reversível? [sim: voltar o orçamento para R$ X / estrutura nova fica pausada, sem gasto, até a ativação]

Próxima revisão: [vertical: em [N]h | estrutura nova: [N]h depois da ativação]
Próxima reavaliação automática: [data/hora | estrutura nova: conta a partir da ativação]

1. Confirmar e aplicar tudo
2. Ajustar valores
3. Cancelar

Digite o número:
```

Um "sim" (opção 1) cobre o lote inteiro deste plano, inclusive todas as criações de uma estrutura nova. A ativação da estrutura nova não entra nesse "sim": é pedida depois, no Passo 6.1. Enquanto a estrutura nova estiver pausada, não há ciclo nem prazo correndo: a revisão, a maturação e o ciclo contam a partir da ativação. Nunca exibir o `curl` no chat.

---

## Passo 5. Execução

Anunciar com o tempo do modo escolhido (faixas de `.claude/rules/tempo-estimado.md`):
- Vertical: `🔍 Próximo passo: aplicar o incremento aprovado na conta de anúncios. Tempo estimado: cerca de 30 segundos.`
- Horizontal, CBO ou Advantage (estrutura nova): `🔍 Próximo passo: criar a estrutura nova aprovada na conta de anúncios, pausada. Tempo estimado: cerca de 90 segundos.`

Conforme o modo e a conexão:
- **Vertical:** `ads_update_entity` com `daily_budget` (MCP) ou `POST /<id>` com `daily_budget` (APP), no conjunto em ABO ou na campanha em CBO. Unidade: no APP, inteiro em centavos (R$ × 100); no MCP, a unidade do schema da tool, conferida antes da primeira escrita (Passo 0.0 da SKILL). Depois de gravar, ler a entidade de novo e conferir que o valor em reais bate com o bloco 🛡️; se não bater, parar, avisar e propor reverter.
- **Horizontal:** MCP: `ads_create_ad_set` com `source_adset_id`; conferir pela leitura se os anúncios vieram junto e, se não vieram, copiar cada anúncio ativo do molde com `ads_create_ad` + `source_ad_id`; aplicar a dimensão do teste com `ads_update_entity` só se o schema aceitar mudar o campo sozinho, senão duplicação guiada no Gerenciador (§3.2 da SKILL). APP: **ler → recriar** (ler a config do conjunto por GET, criar o conjunto novo trocando só a dimensão do teste e com `targeting_automation.advantage_audience`; sob ABO, com o orçamento do plano em centavos, a `bid_strategy` do molde e, com teto de custo ou de lance, o `bid_amount` lido; criar os anúncios referenciando o `creative_id` existente). `POST /<adset_id>/copies` só para 1 conjunto com 1 anúncio: cópia com 2 ou mais objetos falha (ver §3.2 da SKILL).
- **CBO:** MCP: `ads_create_campaign` (com orçamento na campanha) + `ads_create_ad_set` × N com `source_adset_id` (indicando a campanha nova como destino, se o schema permitir), com a mesma conferência de anúncios do Horizontal. APP: `POST /act_{id}/campaigns` (orçamento na campanha) + `POST /act_{id}/adsets` × N (sem orçamento próprio, com `campaign_id` da nova; com teto de custo ou de lance, o `bid_amount` vai em cada conjunto) + anúncios referenciando `creative_id`.
- **Advantage:** MCP: `ads_create_campaign` + 1 `ads_create_ad_set` (público Advantage+) + N `ads_create_ad` com `source_ad_id` dos vencedores (5 a 50). APP: mesma estrutura por POST, com os anúncios referenciando o `creative_id` de cada vencedor; se a campanha ficar sem orçamento próprio (ABO), mandar `is_adset_budget_sharing_enabled: false` (§3.2 da SKILL).

Estruturas novas nascem pausadas e **continuam pausadas no fim do lote**: nada é ativado aqui. Antes de encerrar, conferir que tudo foi criado e que cada conjunto novo tem pelo menos 1 anúncio (e, no Horizontal, a variação do teste aplicada). Em caso de falha, parar, registrar e devolver o erro detalhado, perguntando antes de seguir com o restante.

✅ Concluído: {incremento aplicado | estrutura nova criada e pausada}.

---

## Passo 6. Apresentar resultado

```
[Vertical: ✅ Escala aplicada (ciclo [N]).]
[Horizontal, CBO ou Advantage: ✅ Estrutura criada (pausada). O ciclo [N] começa
  quando ela for ativada (6.1).]

[Vertical: Conjunto "[nome]" agora com R$ [novo]/dia (+[X%])]
[Horizontal: Novo conjunto criado e PAUSADO: "[nome novo]" com R$ [valor]/dia,
  audiência [descrição]. Ainda não gasta nada.]
[CBO: Nova campanha CBO "[nome]" criada e PAUSADA com N conjuntos consolidados.
  Ainda não gasta nada.]
[Advantage: Nova campanha Advantage+ "[nome]" criada e PAUSADA com [N] anúncios
  vencedores do produto/funil [...]. Ainda não gasta nada.]

Riscos a monitorar:
- [frequência subindo, monitorar próximo ciclo]
- [audiência horizontal precisa maturar antes de novo ciclo]
- [...]

[Vertical: Próxima revisão: [data/hora] (em [N]h).]
[Estrutura nova: Próxima revisão: [N]h depois da ativação. Enquanto
  estiver pausada, não há prazo correndo.]

Antes do próximo incremento, vou revalidar:
- CPA/CPL na janela média ≤ target × 0,9
- Lucro/dia ≥ 0 (ROAS acima do break-even)
- Frequência ≤ 2,5 (perpétuo) ou ≤ 3,0 (lançamento)
- Tendência ainda estável
- Sem freio leve/médio acionado

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-analise
Após D+7 (perpétuo low/mid e lançamento) ou D+14 (perpétuo high),
contados do incremento ou, na estrutura nova, da ativação,
volte pra /trafego-analise pra confirmar se a escala se sustentou
e identificar o próximo movimento.

Em caso de freio total acionado nesta sessão: o handoff
automático aponta pra /trafego-otimizar. Siga por lá.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para ver dados antes do prazo: /trafego-insights.
Para acompanhar a conta ao vivo num painel: /trafego-dashboard.
```

### 6.1 Ativar a estrutura nova (só com pedido explícito)

Quando o lote criou estrutura nova (Horizontal, CBO ou Advantage), perguntar:

```
A estrutura nova está criada e pausada. Quer ativar agora?

1. Sim, quero ativar agora
2. Não, vou revisar no Gerenciador antes (peço a ativação depois)

Digite o número:
```

Se 1, mostrar um **bloco 🛡️ próprio** de ativação (§11.2 da SKILL) e aguardar o "sim":

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: ativar estrutura nova
Endpoint: POST /<id> com status=ACTIVE, um por objeto da lista (no conector: ads_activate_entity)
Objeto: [campanha, conjuntos e anúncios criados neste lote, com nomes e IDs]
O que vai mudar:
  - status PAUSED → ACTIVE em [lista]
  - passa a gastar R$ [valor]/dia, somado aos R$ [valor]/dia que a conta já gasta
    (os conjuntos e anúncios originais seguem rodando)
Reset de aprendizado esperado: não nos originais; a estrutura nova começa a fase de aprendizado quando for ativada
Reversível? sim, pausando a estrutura nova

Pode aplicar? Responda "sim" para confirmar, "não" para cancelar.
```

Ao ativar uma campanha criada pela skill, ativar também os conjuntos e anúncios dela no mesmo lote. Com teto da conta declarado, conferir antes no guardião de caixa que o gasto novo cabe. Tool: `ads_activate_entity` (ou `ads_update_entity` com `status=ACTIVE`) no MCP; `POST /<id>` com `status=ACTIVE` no APP. Depois de ativar, anexar no `historico-{campaign_id}.md` a linha da ativação, com status `incremento`, a data e hora da ativação e o mesmo número de ciclo do lote que criou a estrutura (§11.3 da SKILL): é dela que contam a próxima revisão, a maturação e o ciclo. Se 2, a estrutura fica pausada e a ativação vira esse mesmo bloco quando o aluno pedir. Se o aluno ligar a estrutura direto no Gerenciador, a data da ativação é conferida no ciclo seguinte (Passo 7).

---

## Passo 7. Tratamento de freios (em ciclos seguintes)

Quando o aluno volta para um próximo incremento, antes de tudo:

1. Invocar `/trafego-insights` para puxar dados frescos (sem cache).
2. Ler **todas as linhas do último ciclo** no histórico da campanha, não só a última: num lote misto (ex.: Vertical + Horizontal), cada ação tem a sua linha, com a mesma data e hora da execução do lote, e cada ativação feita depois tem linha `incremento` própria (§11.3 da SKILL).
   - Para cada linha `estrutura_pausada` sem ativação registrada depois, ler o status da estrutura nova. Já ativa (ligada no Gerenciador): conferir a data da ativação em `ads_account_get_activity_logs` (MCP) ou perguntar ao aluno e anexar a linha `incremento` com essa data (§11.3 da SKILL).
   - **Nenhuma entidade do ciclo ativada** (todas as linhas são `estrutura_pausada` e as estruturas seguem pausadas): não há ciclo para avaliar; oferecer a ativação (6.1).
   - **Parte ativada** (ex.: o incremento vertical do mesmo lote, ou uma das estruturas novas): avaliar essa parte no item 3, cada uma só depois da sua maturação (o vertical a partir do incremento, a estrutura nova a partir da ativação), e oferecer ativar o resto (6.1).
   - **Tudo ativado:** avaliar o ciclo inteiro no item 3.
3. Comparar com o último ciclo (registrado no histórico da campanha):
   - CPA/CPL piorou 10 a 20% janela curta vs média, ou lucro/dia caiu ≥ 30%? → **freio leve** (não incrementar, manter, reavaliar 48h)
   - CPA/CPL piorou 20 a 30% sustentado por 48h, ou ROAS a ±10% do break-even? → **freio médio** (voltar ao orçamento de antes do último incremento, lido do histórico; sem histórico, do log de atividades no MCP ou informado pelo aluno, nunca calculado por conta própria; se o último ciclo foi a ativação de estrutura nova, reverter é pausar essa estrutura; no lote misto, cada parte ativa que acionou o freio volta do seu jeito, no mesmo bloco 🛡️ (§6.2 da SKILL); refresh criativo; devolver pra `/trafego-otimizar`)
   - CPA/CPL piorou ≥ 30% OU 2 ciclos sem ganho líquido OU saturação estrutural OU lucro/dia negativo em 2 ciclos? → **freio total** (reverter ao último orçamento estável, emitir handoff)
   - Frequência > 4 após 2 refreshes? → **teto de audiência** (parar, expandir trilha)
   - CPM 50%+ acima do histórico por 7d sem sazonal? → **CPM ceiling**
   - 3 ciclos sem ganho de conversões? → **volume ceiling**
   - A folga da conta (`teto_conta_diario_brl` declarado menos o gasto diário atual, como no guardião de caixa) é zero ou negativa? → **teto operacional**. Com folga positiva menor que o próximo incremento, não é teto: reduzir o incremento até caber na folga (guardião de caixa §5)
   - ROAS abaixo do break-even em 2+ ciclos? → **teto de margem**

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

1. Reverter o último incremento (orçamento volta para R$ [valor] |
   pausar a estrutura nova "[nome]", se o último ciclo foi a ativação dela |
   as duas coisas, no lote misto em que as duas partes acionaram o freio).
2. Sugerir refresh criativo via /copy-anuncio + /criativo-estatico
   (com A/B contra o atual no /trafego-testes).
3. Devolver diagnóstico para /trafego-otimizar.

Aplicar agora?

1. Sim, aplicar
2. Não, vou pensar

Digite o número:
```

A reversão do item 1 passa pelo bloco 🛡️ (reduzir orçamento é escrita).

### 7.3 Freio total
```
🔴 Freio total acionado.

[Motivo: CPA piorou 30%+ / 2 ciclos sem ganho / saturação estrutural / lucro/dia negativo sustentado]

Vou:
1. Reverter ao último orçamento estável (R$ [valor]).
2. Devolver a campanha para /trafego-otimizar com handoff.
3. Desativar /trafego-escalar para essa campanha até o cooldown
   vencer ([7d perpétuo low/mid | 14d perpétuo high | 24h lançamento]).

Próximo passo: /trafego-otimizar para diagnóstico do que aconteceu.

Quer investigar a causa antes com /trafego-diagnostico (diagnóstico
diferencial)? Ele apresenta 3 hipóteses competitivas antes de agir.

1. Sim, reverter e investigar com /trafego-diagnostico
2. Sim, reverter e ir direto para /trafego-otimizar
3. Não, prefiro pausar e analisar manualmente
```

### 7.4 Teto atingido
```
🚫 Teto de escala atingido.

Tipo: [audiencia_exausta | cpm_ceiling | volume_ceiling | operacional | margem]

[Descrição do que foi observado]

Recomendação:
- [Audiência exausta] Expandir para nova trilha de público.
  Sugestão: criar campanha nova com audiência fria adjacente
  ou outra geografia via /trafego-criar-campanha.
- [CPM ceiling] Considerar pausa temporária e retomada em
  período de menor concorrência.
- [Volume ceiling] Mercado endereçável atingido. Buscar nova
  fonte de demanda (público novo, oferta nova).
- [Operacional] Teto declarado pelo aluno. Reabrir o teto se
  o retorno compensa, ou parar por aqui.
- [Margem] A campanha não dá lucro no volume atual. Voltar pra
  /trafego-otimizar pra recuperar a margem antes de retomar.

Quer rodar /trafego-diagnostico (auditoria estrutural) para
buscar espaço na conta antes de desistir?

Skill de escala desativada para essa campanha.
```

---

## Passo 8. Salvar registro

1. **Relatório do ciclo** em:
   ```
   meus-produtos/{ativo}/entregas/trafego/escalar/escala-{campanha-slug}-ciclo-{N}-{YYYY-MM-DD}.md
   ```
   Conteúdo: estado atual + ação aplicada + risco + riscos a monitorar + próxima revisão.

2. **Histórico da campanha** (uma linha por ação executada; num lote misto, as linhas do mesmo lote têm a mesma data e hora e o mesmo número de ciclo; o `ciclo_atual` da próxima vez conta ciclos, não linhas: as linhas do lote e as ativações das estruturas dele são um ciclo só, §11.3 e Leitura 3 da SKILL):
   ```
   meus-produtos/{ativo}/trafego/escalar/historico-{campaign_id}.md
   ```
   Estrutura nova: na criação, linha com status `estrutura_pausada` (não conta como ciclo); na ativação (6.1), linha `incremento` com a data e hora da ativação e o mesmo número de ciclo do lote que criou a estrutura. Regra completa na §11.3 da SKILL.

Mostrar o caminho absoluto como texto copiável: `{raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\escalar\escala-{...}.md`

---

## Princípios que este command nunca viola

1. **Recusa rodar sem sinal de prontidão.** Gate duro.
2. **Confiabilidade baixa do dado bloqueia a escala.**
3. **Só escala zona verde.** Lucro/dia ≥ 0 sustentado; zona amarela volta para a otimização.
4. **Incrementos respeitam velocidade declarada.** Nunca pular degraus.
5. **+50% é teto absoluto** de incremento único, mesmo em modo agressivo.
6. **Backup criativo obrigatório** para velocidade agressiva (≥ 3).
7. **Revalidar gatilho** antes de cada incremento. Não é piloto automático.
8. **Freio é prioridade sobre crescimento.** Qualquer degradação para a escala.
9. **Devolução clara para `/trafego-otimizar`** quando o freio total aciona.
10. **Cooldown de 7d/14d/24h** após handoff de descida.
11. **Não diagnostica gargalos fora da escala.** Devolve para a otimização.
12. **Tetos são declarados, não ignorados.** Atingir, parar, comunicar.
13. **Gate 🛡️ antes de toda escrita.** Um "sim" por lote; Carteira só com "aprovar tudo"; estrutura nova nasce e continua pausada, e ativar é operação à parte com bloco 🛡️ próprio (Passo 6.1); nunca apaga entidade; token nunca aparece no chat.
