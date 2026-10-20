# Sub-fluxo. Campanha de Remarketing (fluxo composto)

Monta uma campanha de remarketing completa num fluxo só. Junta a `/trafego-publicos` (público de remarketing) e a `/trafego-criar-campanha` (campanha com esse público).

Passo 0: ver `SKILL.md` desta skill. As skills chamadas fazem o próprio Passo 0 e o próprio roteamento por modo.

## ⚠️ Atravessa skills: modo lote pré-aprovado

Este fluxo escreve na conta por **duas skills diferentes**. Pela regra 8 do gate (seção "GATE EM CAMADA DE CHAT..." do CLAUDE.md), ele só encadeia as escritas sem novo gate no **modo "lote pré-aprovado"**:

1. Mostrar o **plano completo numerado UMA vez** (todas as escritas, nas duas skills).
2. Pedir **um "aprovar tudo" explícito** ("aprovar tudo? sim/não").
3. Com a aprovação, executar em sequência, devolvendo um resumo por item. As skills chamadas não repetem o bloco 🛡️ para os itens do plano.
4. **Se uma operação falhar no meio, parar e perguntar antes de continuar.**
5. Qualquer escrita fora do plano aprovado (ex: o aluno pede para trocar o público no meio) volta a pedir confirmação.
6. Exclusão nunca entra no plano.

Sem o "aprovar tudo", cada skill chamada pede o próprio bloco 🛡️ normalmente.

## Perguntas que cobre

- "Cria uma campanha de remarketing para quem visitou o site nos últimos 30 dias"
- "Quero remarketing para quem abandonou o carrinho"
- "Campanha para quem engajou com o vídeo e ainda não comprou"
- "Remarketing dos compradores antigos (upsell)"

## Fluxo composto

```
[1] O aluno define o público-alvo (ex: "carrinho abandonado 30d")
[2] A skill confere se o público já existe (listagem da /trafego-publicos)
    ├── Existe: usa o público existente
    └── Não existe: entra no plano criar pela /trafego-publicos
    Com excluir_compradores ligado, na mesma listagem confere também o público
    de compradores dos últimos 90 dias (o da exclusão)
    ├── Existe: usa esse público na exclusão
    └── Não existe: entra no plano, antes do conjunto, criar
        "[WS] Purchase-90d-{produto}" pela /trafego-publicos (atalho Compradores
        recentes); ou, se o aluno preferir, segue sem a exclusão (perguntar antes;
        na R4 a exclusão é obrigatória)
[3] O aluno define a oferta (criativo, headline, texto, CTA, link)
[4] O aluno define orçamento e duração
[5] Plano numerado e "aprovar tudo"
[6] Execução: /trafego-publicos (se preciso) e /trafego-criar-campanha
[7] Devolve o que foi criado e os próximos passos
```

## Inputs

| Input | Padrão | Descrição |
|---|---|---|
| `descricao_publico` | obrigatório | Ex: "visitantes 30d", "carrinho abandonado", "viu 50% do vídeo X" |
| `objective` | `OUTCOME_SALES` | ou `OUTCOME_LEADS` |
| `criativo` | obrigatório | Pelo Helper da `ab-generico.md` |
| `headline` | obrigatório | |
| `texto_principal` | obrigatório | |
| `cta` | `LEARN_MORE` | |
| `orcamento_diario` | obrigatório | |
| `duracao_dias` | sem fim (até pausar) | |
| `excluir_compradores` | sim | Excluir compradores dos últimos 90 dias (boa prática; obrigatório na R4). O público de exclusão é conferido no passo [2] e, se não existir, entra no plano |

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**.

1. **Público.** Antes de listar, oferecer as 5 receitas (R1 a R5) numeradas. O aluno escolhe uma ou descreve outro público.
2. **Objetivo** (1. Vendas, 2. Leads). Padrão: Vendas.
3. **Criativo.** "Helper: escolha de criativos" da [ab-generico.md](./ab-generico.md) (biblioteca, arquivo do computador ou código direto; nunca hash ou ID digitado). Sem criativo pronto: encaminhar para `/criativo-estatico`, `/copy-anuncio` ou `/mandala-de-anuncios` (vídeo: `/video-heygen`, `/video-remotion`, `/video-editar`) e voltar. Vídeo novo no MCP: passo manual guiado (biblioteca de mídia do Gerenciador).

   **Criativo com vários vídeos ou imagens (Advantage+ Creative):** simplificar para 1 criativo (`object_story_spec.video_data` ou `link_data`), como no passo 2 da Montagem da `ab-generico.md`. Raro em remarketing, mas vale conferir.
4. **Headline.**
5. **Texto principal.**

   Nos passos 4 e 5, se o aluno pedir que a skill escreva: gerar a partir do resumo do produto (objeções principais, Urgências Ocultas, Argumentos Incontestáveis) e do ângulo da receita, e **aplicar a "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md** (Manual da Copy + skill `revisora`) antes de mostrar, sem mencionar a revisão. Para várias versões ou outros formatos, `/copy-anuncio`.
6. **CTA** (os 4 ou 5 mais comuns, numerados, e "outro"). Sugerir o da receita.
7. **Orçamento diário** (R$/dia).
8. **Duração**, só se o aluno falar em prazo (padrão: sem fim).
9. **Excluir compradores**, só se o aluno questionar (padrão: sim).

**Proibido:** listar 3 ou mais perguntas de uma vez; misturar pergunta principal e sub-opção; pular para o plano sem os passos 1 a 7.

## Receitas prontas

Os tipos citados são os da Mandala de Anúncios do Severino (`.claude/skills/mandala-de-anuncios/SKILL.md`), com objetivo RMKT.

### R1. Carrinho abandonado
- Público: `AddToCart 30d E NÃO Purchase 30d`
- Ângulo sugerido: Prova ou Explicação (quebrando a objeção que travou a compra; objeções no resumo do produto)
- CTA: SHOP_NOW

### R2. Visitantes do site
- Público: `PageView 30d E NÃO Purchase 90d`
- Ângulo: Demonstração ou Problema-Solução
- CTA: LEARN_MORE

### R3. Engajados com vídeo (não compradores)
- Público: `Video50pct E NÃO Purchase 90d`
- Ângulo: Prova: já viram o conteúdo, agora a prova
- CTA: LEARN_MORE

### R4. Upsell para compradores antigos
- Público: `Purchase 180d`, com a exclusão de `Purchase 90d` no conjunto (entra quem comprou entre 90 e 180 dias; 180 dias é o máximo de evento do pixel). Aqui a exclusão de compradores de 90 dias é obrigatória: é ela que separa quem comprou há mais tempo.
- Para quem comprou há mais de 180 dias: usar a lista de clientes como origem (`/trafego-publicos` opção 6, com o CSV e a base legal pela LGPD). Nesse caso, o item 1 do plano numerado diz que o público vem da lista de clientes.
- Ângulo: produto complementar ou continuação (Oportunidade)
- CTA: SHOP_NOW

### R5. Lead que não comprou
- Público: `Lead 30d E NÃO Purchase`
- Ângulo: oferta com prazo real (Dilema ou Comparação)
- CTA: SIGN_UP ou SHOP_NOW

## Plano numerado e "aprovar tudo"

Depois da coleta, mostrar o resumo em linguagem natural e o plano:

```
📋 Plano da campanha de remarketing (aprovação única para tudo)

1. Criar o público "[WS] CarrinhoAbandonado-30d-curso-tarot"
   (quem adicionou ao carrinho e não comprou nos últimos 30 dias)
   → pela /trafego-publicos
{1b. Criar o público "[WS] Purchase-90d-curso-tarot" (compradores dos últimos
    90 dias, usado na exclusão) → pela /trafego-publicos, atalho Compradores
    recentes (só se ele ainda não existir)}
2. Criar a campanha "[WS-RMK] carrinho-abandonado-curso-tarot", objetivo vendas,
   PAUSADA → pela /trafego-criar-campanha
3. Criar o conjunto com o público do item 1, excluindo "[WS] Purchase-90d-curso-tarot"
   (compradores), R$ 50/dia, PAUSADO
4. Criar o anúncio com o criativo "{nome}", headline "{headline}" e botão
   "Comprar agora", PAUSADO
{5. Subir o arquivo "{nome}" (só se o criativo vier do computador, modo App)}

Nada é ativado. Nada é apagado.
Se alguma etapa falhar, eu paro e te pergunto antes de seguir.

Aprovar tudo? (sim/não)
```

O Preview YAML abaixo vai junto, recolhido, para quem quiser o detalhe técnico.

## Orquestração (o que cada skill faz)

> Esta sub-skill **não fala com a Graph API nem com o MCP diretamente.** Ela chama a `/trafego-publicos` (listar ou criar público) e a `/trafego-criar-campanha` (campanha), que já roteiam por `META_AUTH_MODO` (tool no MCP, `curl` no App). Os endpoints abaixo são só referência do que cada uma executa.

```
# Item 1 (e 1b). Conferir ou criar o público de remarketing e o de exclusão → /trafego-publicos
GET  /act_<id>/customaudiences            (listar)
POST /act_<id>/customaudiences            (criar, se não existir)

# Itens 2 a 4. Campanha → /trafego-criar-campanha
POST /act_<id>/campaigns
{
  "name": "[WS-RMK] {descricao}-{produto}",
  "objective": "OUTCOME_SALES",
  "is_adset_budget_sharing_enabled": false,
  "status": "PAUSED"
}

POST /act_<id>/adsets
{
  "name": "[WS-RMK] adset-{descricao}-{produto}",
  "campaign_id": "<id>",
  "daily_budget": <orcamento_em_centavos>,
  "targeting": {
    "custom_audiences": [<publico_remarketing>],
    "excluded_custom_audiences": [<publico_compradores_90d>],
    "targeting_automation": { "advantage_audience": 0 }
  },
  "status": "PAUSED"
}

POST /act_<id>/ads (com o criativo do passo 3, apontando para o creative_id quando já existe)
```

> ⚠️ **Esta sub-skill cria estrutura nova, não copia**, então não esbarra nos erros do `/copies` (seção "Lições de campo" da `ab-generico.md`). Mas o conjunto novo exige `targeting_automation.advantage_audience` (erro 1870227): ao chamar a `/trafego-criar-campanha`, deixar claro que o conjunto é de remarketing, com público personalizado e exclusão, sem expansão Advantage+. A campanha é ABO (orçamento no conjunto): no App, ela leva `"is_adset_budget_sharing_enabled": false` (obrigatório desde a v24, senão erro 4834011); no MCP, o campo só vai se o schema de `ads_create_campaign` pedir.

## Preview YAML

```yaml
sub_fluxo: campanha_remarketing
modo_aprovacao: lote_pre_aprovado
nome_campanha: "[WS-RMK] carrinho-abandonado-curso-tarot"
receita: R1 (Carrinho abandonado)

publico_origem:
  status: criar (não existe)
  spec:
    nome: "[WS] CarrinhoAbandonado-30d-curso-tarot"
    inclusao: AddToCart 30d
    exclusao: Purchase 30d

publico_excluir:
  nome: "[WS] Purchase-90d-curso-tarot"
  status: já existe | criar (item 1b do plano)

campanha:
  objetivo: OUTCOME_SALES
  otimizacao: compra
  estrutura_orcamento: ABO   # sem orçamento na campanha; o valor vai no conjunto
  duracao: sem fim (até pausar)

conjunto:
  orcamento_diario: 50 BRL   # ABO, orçamento no conjunto

anuncio:
  criativo: imagem (tipo Prova da Mandala)
  headline: "{headline aprovada}"
  texto_principal: "{texto aprovado}"
  cta: SHOP_NOW
  link: https://meusite.com/checkout

status_inicial: PAUSED

orquestracao:
  item_1: criar_publico -> /trafego-publicos
  item_1b: criar_publico_exclusao -> /trafego-publicos   # só se o público de exclusão não existir
  itens_2_a_4: criar_campanha -> /trafego-criar-campanha
```

## Depois de criar

```
✅ Público criado: [WS] CarrinhoAbandonado-30d-curso-tarot

✅ Campanha de remarketing criada (PAUSADA): [WS-RMK] carrinho-abandonado-curso-tarot
   1 conjunto e 1 anúncio, ambos pausados.

O público leva cerca de 24h para popular. Dá para ativar agora, mas a campanha vai
entregar muito pouco até o público ter pelo menos umas 500 pessoas.

Para ativar quando estiver pronta: no Gerenciador, ou me peça por aqui (com confirmação).

Para acompanhar: /trafego-insights (campanha "[WS-RMK] carrinho-abandonado-curso-tarot")
```

Registrar o plano e o resultado em `meus-produtos/{ativo}/entregas/trafego/testes/{slug}.md` (com `sub_fluxo: campanha_remarketing`) e marcar como desatualizado o cache do `/trafego-insights` da conta.

## Dicas VTSD

- **Excluir compradores recentes** (Purchase 90d) é prática padrão para não gastar com quem já comprou. A skill faz isso por padrão.
- **Frequência alvo em remarketing:** de 3 a 6 (maior que no público frio, porque o público é menor e quente).
- **Janela curta** = público pequeno e muito quente. **Janela longa** = público maior e mais frio.
- **Orçamento conservador.** Público pequeno satura rápido. Começar com R$ 30 a 50/dia para público de 5 a 20 mil pessoas.
- **Criativo diferente do usado no público frio.** Quem está no remarketing já viu o anúncio principal. Usar outro ângulo da Mandala: Prova, Explicação (quebrando a objeção que travou a compra), Oportunidade.

## Avisos

- **Público novo não popula na hora.** A campanha nasce pausada; o aluno ativa em cerca de 24h.
- **Mínimo de 1.000 pessoas** no público para o algoritmo otimizar. A skill avisa se a estimativa for menor.
- **Público muito pequeno (menos de 500)** = custo por impressão alto. Recomendado ampliar a janela ou trocar o evento.
- **No primeiro remarketing do produto**, começar pela R2 (visitantes, público maior) e depois a R1 (carrinho).
