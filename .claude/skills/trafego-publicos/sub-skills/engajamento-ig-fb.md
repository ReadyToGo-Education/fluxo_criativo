# Sub-fluxo. Engajamento com Instagram e Facebook (orgânico)

Cria um público personalizado do tipo `ENGAGEMENT` de quem **interagiu** com a Página do Facebook ou com a conta profissional do Instagram: visitas ao perfil, interação com posts, anúncios e formulários de cadastro (Lead Form).

Categoria oficial da Meta, mas pouco usada por quem só pensa em pixel. Junta quem mostrou interesse e ainda não comprou: público quente de remarketing **sem depender de pixel**.

Passo 0 (produto ativo, conexão, conta) e gate: ver `SKILL.md` desta skill.

## Diferença para `publico-video-view.md`

| Sub-fluxo | O que junta | Fonte |
|---|---|---|
| `publico-video-view` | Quem assistiu X% de um vídeo específico | vídeo |
| `engajamento-ig-fb` (este) | Quem interagiu com perfil, posts, anúncios ou formulário, **sem ser vídeo** | `page`, `ig_business`, `ad`, `lead_gen` |

Os dois podem existir juntos: geram públicos que se completam.

## Perguntas que cobre

- "Quem visitou meu perfil do Instagram nos últimos 30 dias"
- "Pessoas que curtiram ou salvaram meu Reel"
- "Público de quem mandou DM no Instagram"
- "Quem abriu meu formulário de cadastro e não enviou"
- "Quem interagiu com a minha Página do Facebook"
- "Pessoas que clicaram em qualquer anúncio meu"

## Inputs

| Input | Padrão | Descrição |
|---|---|---|
| `tipo_fonte` | obrigatório | Página, Instagram, Anúncio, Formulário de cadastro, Evento |
| `fonte_id` | obrigatório | Escolhido por nome ou listagem (o aluno nunca digita ID) |
| `tipo_interacao` | obrigatório | Varia por fonte (tabela abaixo) |
| `janela_dias` | 30 | Até 365 (varia por fonte) |
| `nome_extra` | gerado | Sufixo do nome |

### Interações por fonte

| Fonte | Interações |
|---|---|
| **Página do Facebook** | Visitou a Página, curtiu ou comentou post, salvou post, mandou mensagem, clicou no botão de ação |
| **Instagram profissional** | Visitou o perfil, interagiu com posts ou Reels (curtida, comentário, salvar), mandou DM, salvou post ou anúncio |
| **Anúncio** (específico) | Clicou, viu (quem salvou anúncio entra pela Página ou pelo Instagram, opção "Só quem salvou post ou anúncio") |
| **Formulário de cadastro** | Abriu sem enviar, enviou |
| **Evento do Facebook** | Confirmou presença, marcou interesse |

## Roteamento por modo (ler primeiro)

- **`MCP_CONECTOR` (padrão):**
  1. **Descobrir a fonte** com as tools de leitura (ler o schema antes): Páginas por `ads_get_ad_account_pages` (Página que não vier ali: `ads_get_user_pages` ou `ads_get_pages_for_business`); conta do Instagram por `ads_get_ig_accounts`; anúncios por `ads_get_ad_entities`. O ID enviado na fonte `ig_business` é o da **conta profissional** do Instagram, o mesmo que o App lê em `instagram_business_account`: conferir pelo schema e por `ads_get_field_context` que é esse o ID antes de criar (ID de outro tipo faz a Meta recusar ou criar um público vazio). Formulário de cadastro e Evento: o MCP não lista; pedir ao aluno o nome e seguir pelo passo manual guiado, ou usar o link que ele colar.
  2. **Criar** com `ads_create_custom_audience` usando o subtipo de engajamento. Ler o schema da tool antes e preencher a fonte, a interação e a janela nos campos que ele pedir (não inventar parâmetro). A regra do modo App (abaixo) é a referência do conteúdo.
  3. **Conferir** com `ads_get_custom_audience` (regra e `delivery_status`). Se a Meta recusar a fonte ou a regra pelo conector, seguir pelo passo manual guiado.
- **`APP`:** descoberta e criação por `curl` (endpoints abaixo).

### Passo manual guiado (fonte que o MCP não lista, ou recusa)

```
Você cria em 2 minutos no Gerenciador:

📋 Passo 1. Gerenciador de Anúncios → menu "Públicos" → "Criar público" →
           "Público personalizado"
📋 Passo 2. Em "Fontes da Meta", escolha "{Instagram | Página do Facebook |
           Formulário de cadastro | Evento}" e clique em "Avançar"
📋 Passo 3. Origem: {conta @usuario | Página "nome" | formulário "nome"}
📋 Passo 4. Eventos: "{interação em português, ex: Pessoas que enviaram uma
           mensagem para sua conta profissional}"
📋 Passo 5. Retenção: {janela} dias
📋 Passo 6. Nome do público: {nome}
📋 Passo 7. Clique em "Criar público"

🛟 Se algum nome de botão estiver diferente, me mande um print.

Me avise com "feito" que eu confiro pela listagem.
```

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**. O aluno **nunca digita ID**.

### Ordem fixa

1. **Fonte.**
   ```
   De onde você quer pegar o engajamento?

   1. Da minha Página do Facebook (curtidas, mensagens, visitas)
   2. Do meu Instagram profissional (visitas ao perfil, DMs, interação com posts e Reels)
   3. De um anúncio específico (quem clicou ou viu)
   4. De um formulário de cadastro (quem abriu ou enviou)
   5. De um Evento do Facebook (quem confirmou presença)

   Digite o número:
   ```
   Mapeamento interno: 1 → `page`; 2 → `ig_business`; 3 → `ad`; 4 → `lead_gen`; 5 → `event`.

2. **Fonte específica.**
   - **1 (Página):** MCP `ads_get_ad_account_pages` (se a Página não vier: `ads_get_user_pages` ou `ads_get_pages_for_business`); App `GET /me/accounts?fields=id,name`. Confirmar a única ou listar.
   - **2 (Instagram):** MCP `ads_get_ig_accounts` (usar o ID da conta profissional, o mesmo de `instagram_business_account` no App); App `GET -g /<page_id>?fields=instagram_business_account{id,username}`.
   - **3 (Anúncio):** MCP `ads_get_ad_entities`; App `GET /act_<id>/ads?fields=id,name,creative,created_time&limit=50&date_preset=last_30d`. Lista numerada com nome, data e gasto.
   - **4 (Formulário):** App `GET /<page_id>/leadgen_forms?fields=id,name,status`. MCP: pedir o nome do formulário e seguir pelo passo manual guiado.
   - **5 (Evento):** raro; pedir o link do evento.

   O aluno escolhe pelo código curto (P1, P2 para Página; A1, A2 para anúncio; L1, L2 para formulário).

3. **Interação.**

   **Página ou Instagram:**
   ```
   Que tipo de interação contar?

   1. Qualquer interação (visitas, posts, mensagens, cliques): público maior e mais geral
   2. Só quem mandou mensagem (DM ou Messenger): muito qualificado
   3. Só quem engajou com posts (curtiu, comentou, salvou): quente
   4. Só quem visitou o perfil (sem interação direta): mais frio, mas relevante
   5. Só quem salvou post ou anúncio: muito qualificado

   Digite o número (Enter para usar 1):
   ```

   **Anúncio:**
   ```
   Quem incluir desse anúncio?

   1. Quem viu ou clicou (qualquer interação)
   2. Só quem clicou
   3. Só quem viu

   Digite o número:
   ```

   **Formulário de cadastro:**
   ```
   Quem incluir do formulário?

   1. Abriu mas NÃO enviou (remarketing para fechar o cadastro)
   2. Enviou (já é lead: upsell ou nutrição)
   3. Os dois (quem abriu, tenha enviado ou não)

   Digite o número:
   ```

   Cada opção desses três menus tem uma regra fixa na tabela "Opção do menu → evento da regra" (abaixo). Nunca improvisar o evento.

4. **Janela.** As opções dependem da fonte escolhida no passo 1 (limites na seção "Limites e pegadinhas").

   **Página, Instagram ou Anúncio:**
   ```
   Por quanto tempo a pessoa fica nesse público?

   1. 7 dias (pequeno e muito quente)
   2. 30 dias (padrão, equilíbrio)
   3. 60 dias
   4. 90 dias
   5. 180 dias (Página e Instagram, pega o padrão sazonal)
   6. 365 dias (máximo, só para fontes com pouco volume por dia)

   Digite o número (Enter para usar 2):
   ```

   **Formulário de cadastro** (limite da Meta: 90 dias):
   ```
   Por quanto tempo a pessoa fica nesse público?

   1. 7 dias (pequeno e muito quente)
   2. 30 dias (padrão, equilíbrio)
   3. 60 dias
   4. 90 dias (máximo para formulário)

   Digite o número (Enter para usar 2):
   ```

   **Evento do Facebook:** o limite é o fim do evento mais 30 dias. Oferecer 7, 30, 60 e 90 dias; janela maior só depois de conferir a data do evento.

   Se a janela passar do limite da fonte, voltar a esta pergunta antes do bloco 🛡️.

5. **Nome.** Sugerir `[WS] Engajamento{Fonte}-{Interacao}-{janela}d-{produto-slug}` (ex: `[WS] EngajamentoInsta-DM-30d-curso-tarot`).

**Proibido:** pedir `event_sources[].id`, `event_sources[].type`, `filter` ou qualquer chave da Marketing API; agrupar inputs; pular para o bloco 🛡️ sem os passos 1 a 5.

## Endpoint (modo App)

> ⚠️ **NÃO enviar `subtype` no `curl`.** A Meta v25 infere pela regra (`event_sources.type` em `page`, `ig_business`, `ad`, `lead_gen` ou `event`). Enviar devolve `error_subcode 1870053`. (Na tool do MCP, o subtipo é obrigatório.)

```
POST /act_<id>/customaudiences
{
  "name": "[WS] EngajamentoInsta-DM-30d-curso-tarot",
  "description": "Quem mandou DM no Instagram nos últimos 30 dias.",
  "rule": {
    "inclusions": {
      "operator": "or",
      "rules": [{
        "event_sources": [{"id": "<ig_business_id>", "type": "ig_business"}],
        "retention_seconds": 2592000,
        "filter": {
          "operator": "and",
          "filters": [{
            "field": "event",
            "operator": "eq",
            "value": "ig_user_messaged_business"
          }]
        }
      }]
    }
  }
}
```

### Opção do menu → evento da regra

Cada opção dos menus do passo 3 tem uma regra fixa. Os nomes **são conferidos na conta antes da primeira criação de cada fonte** (seção seguinte). Se a conta mostrar outro nome de evento ou outro `type` de fonte, vale o da conta.

| Fonte | Opção do menu | Regra |
|---|---|---|
| `page` | 1. Qualquer interação | `event eq page_engaged` |
| `page` | 2. Só quem mandou mensagem | `event eq page_messaged` |
| `page` | 3. Só quem engajou com posts | `event eq page_post_interaction` |
| `page` | 4. Só quem visitou | `event eq page_visited` |
| `page` | 5. Só quem salvou post ou anúncio | `event eq page_or_post_save` |
| `ig_business` | 1. Qualquer interação | `event eq ig_business_profile_all` |
| `ig_business` | 2. Só quem mandou mensagem (DM) | `event eq ig_user_messaged_business` |
| `ig_business` | 3. Só quem engajou com posts ou Reels | `event eq ig_business_profile_engaged` |
| `ig_business` | 4. Só quem visitou o perfil | `event eq ig_business_profile_visit` |
| `ig_business` | 5. Só quem salvou post ou anúncio | `event eq ig_business_profile_ad_saved` |
| `lead_gen` | 1. Abriu mas NÃO enviou | `event eq lead_generation_dropoff` (desistência: abriu e não enviou). Se a conferência mostrar que esse evento não existe: `inclusions` com `lead_generation_opened` e um bloco `exclusions` com `lead_generation_submitted` |
| `lead_gen` | 2. Enviou | `event eq lead_generation_submitted` |
| `lead_gen` | 3. Os dois | `event eq lead_generation_opened` (quem abriu, tenha enviado ou não) |
| `ad` | 1. Quem viu ou clicou | duas regras em `inclusions` (`operator: "or"`): `ad_impression` e `ad_click` |
| `ad` | 2. Só quem clicou | `event eq ad_click` |
| `ad` | 3. Só quem viu | `event eq ad_impression` |
| `event` | Confirmou presença / marcou interesse | `event eq event_rsvp` / `event eq event_interested` |

### Conferência dos nomes de evento (antes da primeira criação de cada fonte)

1. Na listagem da conta (MCP: `ads_get_ad_account_custom_audiences`; App: `GET /act_<id>/customaudiences?fields=name,subtype`), procurar um público de engajamento (`ENGAGEMENT`) da mesma fonte, de preferência criado pelo Gerenciador.
2. Ler a regra dele (MCP: `ads_get_custom_audience`; App: `GET /<audience_id>?fields=rule`) e usar o `type` da fonte e os nomes de evento que a Meta gravou lá. No MCP, conferir também o schema da `ads_create_custom_audience`, se ele listar os eventos aceitos.
3. Sem público de referência: usar os nomes da tabela e ler a regra gravada logo depois de criar. Se a Meta recusar o nome do evento, não tentar outro nome por conta própria: seguir pelo passo manual guiado e, depois do "feito", ler a regra do público criado no Gerenciador para usar os nomes certos nas próximas vezes.
4. Em qualquer caso, depois de criar, conferir se a regra gravada traz o evento da opção escolhida. Se vier diferente, avisar o aluno antes de entregar.

## Resumo em linguagem natural (obrigatório, antes do bloco 🛡️)

```
📋 Antes de eu criar esse público na sua conta, um resumo:

Vou criar o público "{nome}".

Quem entra:
   Pessoas que {interação em português} {fonte em português} nos últimos {janela} dias.

Exemplos:
   - "mandaram DM para o seu Instagram (@{usuario})"
   - "curtiram ou comentaram algum post da sua Página '{nome_pagina}'"
   - "clicaram no seu anúncio '{nome_anuncio}'"
   - "abriram o seu formulário '{nome_form}' e não enviaram"

Tamanho estimado: a Meta calcula depois da criação. Por enquanto aparece como
   "calculando" (o tamanho aparece no Gerenciador em até 24h).

⏰ Importante:
   - {Página ou Instagram:} a Meta costuma puxar alguns dias de histórico.
   - {Anúncio ou formulário:} só junta interações daqui para frente.
   - Atualiza sozinho a cada 24h.
   - **Não depende do pixel.** Funciona mesmo sem pixel instalado.

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → procurar "[WS] Engajamento..."

Está certo? (sim segue para a confirmação final, não cancela aqui)
```

**Tradução obrigatória:**

| Campo técnico | Tradução |
|---|---|
| `type: page` | "Página do Facebook '{nome}'" |
| `type: ig_business` | "Instagram (@{usuario})" |
| `type: ad` | "anúncio '{nome_anuncio}'" |
| `type: lead_gen` | "formulário '{nome_form}'" |
| `type: event` | "Evento '{nome_evento}'" |
| `event: page_engaged` ou `ig_business_profile_all` | "interagiu de qualquer jeito com a Página (ou com a conta do Instagram)" |
| `event: ig_user_messaged_business` | "mandou DM no Instagram" |
| `event: page_messaged` | "mandou mensagem no Messenger" |
| `event: page_post_interaction` ou `ig_business_profile_engaged` | "curtiu, comentou ou salvou um post" |
| `event: ig_business_profile_visit` | "visitou o perfil do Instagram" |
| `event: page_visited` | "visitou a Página do Facebook" |
| `event: lead_generation_dropoff` (ou abriu sem o envio, pelo bloco de exclusão) | "abriu o formulário e não enviou" |
| `event: lead_generation_opened` | "abriu o formulário (tenha enviado ou não)" |
| `event: lead_generation_submitted` | "enviou o formulário (virou lead)" |
| `event: ad_click` | "clicou no anúncio" |
| `event: ad_impression` | "viu o anúncio" |
| `event: page_or_post_save` ou `ig_business_profile_ad_saved` | "salvou um post ou anúncio" |
| `retention_seconds: 2592000` | "30 dias" |
| `retention_seconds: 7776000` | "90 dias" |
| `subtype: ENGAGEMENT` | "público de engajamento" |

**Proibido no resumo:** IDs de Página, Instagram, anúncio ou formulário; JSON da regra; `event_sources[]` literal.

## Preview YAML (dentro do bloco 🛡️)

```yaml
sub_fluxo: engajamento_ig_fb
modo: MCP_CONECTOR | APP
fonte:
  tipo: Instagram profissional
  conta: "@meu_produto"
tipo_interacao: DM (mensagem direta)
janela_dias: 30
retention_seconds: 2592000
nome_final: "[WS] EngajamentoInsta-DM-30d-curso-tarot"
tamanho_estimado: "calculando" (a Meta atualiza em até 24h)
```

## Depois de criar

Ler o público criado para conferir a regra (seção "Conferência dos nomes de evento", item 4) e a faixa de tamanho: MCP `ads_get_custom_audience` (se a leitura trouxer a faixa); App `GET /<audience_id>?fields=rule,approximate_count_lower_bound,approximate_count_upper_bound,delivery_status`. Sem faixa na leitura, mostrar "calculando".

```
✅ Público criado: "[WS] EngajamentoInsta-DM-30d-curso-tarot"

Tamanho: {faixa lida, ex: "de 800 a 950 pessoas" | "calculando"} (o tamanho real
aparece no Gerenciador em até 24h)

⏰ A partir de agora, toda nova interação do tipo "{interação em português}" na
   {fonte em português} entra no público automaticamente.

Onde gerenciar:
   Gerenciador de Anúncios → Públicos → procurar "[WS] Engajamento..."

⚠️ IMPORTANTE: falha visual conhecida do Gerenciador
   Se você abrir esse público e clicar em "Editar":
   - Os campos "Origem" e "Eventos" vão aparecer VAZIOS.
   - É só visual. A regra está certa na Meta (conferida pela leitura do público).
   - NUNCA clique em "Atualizar público" com os campos vazios: isso troca a regra
     por uma vazia e quebra o público.
   - Se abrir por engano, feche pelo "Cancelar" ou pelo "X".

   O painel "Resumo" da direita mostra a conta e a janela, mas também esconde o
   filtro de evento (ex: DM). Para conferir: /trafego-publicos opção 8 (Listar).

Próximos passos:

🎯 Remarketing para quem engajou
   /trafego-criar-campanha → usar esse público na segmentação.
   Muito forte para DM, formulário aberto sem envio e quem salvou anúncio.

🎯 Semelhante de quem engajou
   /trafego-publicos → opção 5 → escolher esse público como origem.
   Menos forte que o semelhante da lista de compradores, mas melhor que público frio.

📝 Registro em: meus-produtos/_global/trafego/publicos/{audience_id}.md
```

## Limites e pegadinhas

- **A Página precisa estar ligada ao Business.** Perfil pessoal não funciona (a Meta recusa).
- **O Instagram precisa estar ligado à Página** (pelo Business). Conta pessoal do Instagram não funciona.
- **Janela máxima por fonte:**
  - `page` e `ig_business`: 365 dias
  - `ad`: 365 dias (só conta o período em que o anúncio rodou)
  - `lead_gen`: 90 dias (limite da Meta)
  - `event`: até o fim do evento mais 30 dias
- **Anúncio apagado** para de alimentar o público (o histórico fica).
- **Sem histórico anterior** à criação para `ad` e `lead_gen`. Para `page` e `ig_business`, a Meta tenta puxar alguns dias para trás (varia).
- **Falha visual do Gerenciador:** públicos criados fora do Gerenciador com fonte `ig_business` (e também vídeo) abrem a edição com "Origem" e "Eventos" em branco, mesmo com a regra certa. Confirmado na prática em 2026-05-27: a leitura do público trazia `event_sources` e `filter` corretos, e a tela mostrava vazio. **Nunca clicar "Atualizar público" com campos vazios.** A conferência confiável é a leitura do público (`ads_get_custom_audience` no MCP, `GET /<audience_id>?fields=rule,delivery_status,operation_status` no App).

## Ligação com o método VTSD

- **Quadro do produto** → quem engajou com posts que falam do Quadro = público qualificado para aquisição.
- **Mandala da Criatividade** → quem viu ou curtiu posts de objetivo Descoberta e Relacionamento vira público de remarketing para anúncios de Conversão.
- **Formulário aberto sem envio** → público cirúrgico para anúncios de objetivo RMKT (ex: Prova, Explicação quebrando a objeção que travou o cadastro).
- **DM no Instagram** → público muito quente para anúncios de Conversão (ex: História, Dilema).
- Para produzir os anúncios: `/copy-anuncio`, `/criativo-estatico`, `/mandala-de-anuncios`.
