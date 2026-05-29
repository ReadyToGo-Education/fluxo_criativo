# Sub-fluxo. Engajamento Instagram / Facebook (orgânico)

Cria Custom Audience tipo `ENGAGEMENT` baseada em quem **interagiu organicamente** com Page do Facebook OU Conta Comercial do Instagram. Cobre interações em perfil, posts, anúncios e Lead Forms.

**Categoria oficial Meta, mas frequentemente ignorada por iniciantes** que só pensam em pixel. Captura quem demonstrou interesse mas ainda não converteu — público quente de remarketing **sem depender de pixel**.

## Diferenças vs `publico-video-view.md`

| Sub-fluxo | O que captura | Source type |
|---|---|---|
| `publico-video-view` | Quem assistiu X% de um vídeo específico | `video` |
| `engajamento-ig-fb` (esse) | Quem interagiu com perfil/posts/ads/Lead Form, **sem ser vídeo** | `page`, `ig_business`, `ad`, `lead_gen` |

Os dois podem coexistir — gera audiences complementares.

## Perguntas que cobre

- "Quem visitou meu perfil do Instagram nos últimos 30 dias"
- "Pessoas que curtiram ou salvaram meu post do Reels"
- "Audience de quem mandou DM no Instagram"
- "Quem abriu meu Lead Form mas não enviou"
- "Quem interagiu com minha página do Facebook"
- "Pessoas que clicaram em qualquer anúncio meu"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `tipo_fonte` | obrigatório | Page / Instagram / Ad / Lead Form / Evento |
| `fonte_id` | obrigatório | ID da Page, Conta IG, Ad, etc. — coletado via fuzzy match |
| `tipo_interacao` | obrigatório | Varia por fonte (ver tabela abaixo) |
| `janela_dias` | 30 | Janela da audience (varia por fonte; máx 365) |
| `nome_extra` | gerado | Sufixo do nome |

### Tipos de interação por fonte

| Fonte | Interações disponíveis |
|---|---|
| **Page Facebook** | Quem visitou a página, curtiu/comentou em qualquer post, salvou post, mandou mensagem, clicou em CTA |
| **Instagram Business** | Quem visitou o perfil, interagiu com posts/Reels (like/comentário/salvar), mandou DM, salvou story |
| **Anúncio** (específico) | Quem clicou, viu o anúncio, salvou |
| **Lead Form** | Abriu o form (sem enviar), enviou o form |
| **Evento Facebook** | Confirmou presença, interessado |

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Aluno **nunca digita IDs crus** — sempre via fuzzy match.

### Ordem fixa

1. **Tipo de fonte.** Pergunta numerada em linguagem natural:
   ```
   De onde você quer pegar o engajamento?

   1. Da minha Página do Facebook (curtidas, mensagens, visitas à página)
   2. Da minha Conta do Instagram (visitas no perfil, DMs, interação com posts/Reels)
   3. De um anúncio específico (quem clicou, viu, salvou)
   4. De um Lead Form (quem abriu ou enviou)
   5. De um Evento do Facebook (quem confirmou presença)

   Digite o número:
   ```
   Mapeamento interno:
   - 1 → `event_sources[{type: "page"}]`
   - 2 → `event_sources[{type: "ig_business"}]`
   - 3 → `event_sources[{type: "ad"}]`
   - 4 → `event_sources[{type: "lead_gen"}]`
   - 5 → `event_sources[{type: "event"}]`

2. **Fonte específica (fuzzy match).** Varia conforme passo 1:
   - **Se 1 (Page Facebook):** `GET /me/accounts?fields=id,name` (listar pages do aluno) → confirmar a única OU listar se múltiplas.
   - **Se 2 (Instagram):** `GET /<page_id>?fields=instagram_business_account{id,username}` → confirma conta IG conectada.
   - **Se 3 (Anúncio):** `GET /act_<id>/ads?fields=id,name,creative,created_time&limit=50&date_preset=last_30d` → lista numerada com nome+data+gasto.
   - **Se 4 (Lead Form):** `GET /<page_id>/leadgen_forms?fields=id,name,status` → lista numerada.
   - **Se 5 (Evento):** raro — pedir o ID ou URL do evento manualmente.

   Aluno escolhe pelo código curto (P1, P2 pra page; A1, A2 pra ad; L1, L2 pra Lead Form).

3. **Tipo de interação.** Numerada, varia conforme tipo de fonte:

   **Se 1/2 (Page/Instagram):**
   ```
   Que tipo de interação contar?

   1. Qualquer interação (visitas + posts + DMs + cliques) — audience maior, mais geral
   2. Só quem mandou mensagem (DM/Messenger) — muito qualificado
   3. Só quem engajou com posts (like/comentário/salvou) — quente
   4. Só quem visitou o perfil (sem interação direta) — frio mas relevante
   5. Só quem salvou post/anúncio — super qualificado

   Digite o número (Enter pra usar 1):
   ```

   **Se 3 (Anúncio):**
   ```
   Quem incluir desse anúncio?

   1. Quem viu/clicou no anúncio (qualquer interação)
   2. Só quem clicou
   3. Só quem viu (impressão)

   Digite o número:
   ```

   **Se 4 (Lead Form):**
   ```
   Quem incluir do Lead Form?

   1. Abriu o form mas NÃO enviou (audience de remarketing pra fechar a conversão)
   2. Enviou o form (já viraram lead — pode ser pra upsell ou nutrição)
   3. Os dois

   Digite o número:
   ```

4. **Janela.** Numerada:
   ```
   Por quanto tempo manter a pessoa nessa audience?

   1. 7 dias (audience pequena, super quente)
   2. 30 dias (default — equilíbrio)
   3. 60 dias
   4. 90 dias
   5. 180 dias (pra Page/IG — captura padrão sazonal)
   6. 365 dias (máximo — só pra fontes com baixo volume diário)

   Digite o número (Enter pra usar 2):
   ```

5. **Nome.** Sugerir auto-gerado seguindo `[FC] Engajamento{Fonte}-{Interacao}-{janela}d-{produto-slug}` (ex: `[FC] EngajamentoInsta-DM-30d-curso-tarot`).

**Proibido:**
- Pedir `event_sources[].id`, `event_sources[].type`, `filter` ou qualquer chave da Marketing API direto ao aluno.
- Agrupar 2+ inputs na mesma mensagem.
- Pular pro Preview YAML sem passar pelos passos 1-5.

## Endpoint

> ⚠️ **NÃO enviar campo `subtype` no POST.** A Meta v25.0 infere o subtype automaticamente a partir da estrutura da rule (aqui, `event_sources.type` em `page`, `ig_business`, `ad`, `lead_gen` ou `event`). Mandar `subtype` retorna `error_subcode 1870053 — O parâmetro 'subtipo' não é aceito na versão atual da API`. (Subtype continua aparecendo no GET pra leitura — apenas não enviar no POST.)

```
POST /act_<id>/customaudiences
{
  "name": "[FC] EngajamentoInsta-DM-30d-curso-tarot",
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
            "value": "ig_dm"
          }]
        }
      }]
    }
  }
}
```

### Eventos suportados por fonte

| Source type | Eventos comuns |
|---|---|
| `page` | `page_visit`, `post_engagement`, `page_message`, `page_cta_click`, `post_save` |
| `ig_business` | `ig_profile_visit`, `ig_post_engagement`, `ig_dm`, `ig_reel_save`, `ig_story_swipe_up` |
| `ad` | `ad_click`, `ad_impression`, `ad_save` |
| `lead_gen` | `lead_open` (abriu form), `lead_submit` (enviou) |
| `event` | `event_rsvp`, `event_interested` |

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

```
📋 Antes de eu criar essa audience na sua conta, deixa eu te resumir:

Vou criar a audience "{nome}":

Quem entra:
   Pessoas que {tipo_interacao em PT} {fonte em PT} nos últimos {janela} dias.

Exemplos de tradução:
   - "mandaram DM pro seu perfil do Instagram (@{username})"
   - "curtiram ou comentaram em algum post da sua Página '{nome_page}'"
   - "clicaram no seu anúncio '{nome_ad}'"
   - "abriram o seu Lead Form '{nome_form}' mas não enviaram"

Tamanho estimado: ~{audience_size formatado} pessoas.
   (Baseado nas interações dos últimos {janela} dias na sua fonte.)

⏰ Importante:
   - Audience só pega quem interagiu de AGORA em diante.
     {Se fonte = page ou ig_business:} Page/Instagram podem ter histórico parcial retroativo.
     {Se fonte = ad ou lead_gen:} Só pega interações futuras.
   - Atualiza sozinha a cada 24h.
   - **Não depende do pixel** — funciona mesmo se o pixel não estiver instalado.

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → procurar "[FC] Engajamento..."

Tá certo? (sim segue pro YAML, não cancela aqui)
```

**Regras de tradução obrigatórias:**

| Campo técnico | Tradução |
|---|---|
| `type: page` | "Página do Facebook '{nome}'" |
| `type: ig_business` | "Conta do Instagram (@{username})" |
| `type: ad` | "anúncio '{nome_ad}'" |
| `type: lead_gen` | "Lead Form '{nome_form}'" |
| `type: event` | "Evento '{nome_evento}'" |
| `event: ig_dm` | "mandou DM no Instagram" |
| `event: page_message` | "mandou mensagem no Messenger" |
| `event: post_engagement` | "curtiu, comentou ou salvou um post" |
| `event: ig_profile_visit` | "visitou o perfil do Instagram" |
| `event: page_visit` | "visitou a Página do Facebook" |
| `event: lead_open` | "abriu o Lead Form (sem enviar)" |
| `event: lead_submit` | "enviou o Lead Form (virou lead)" |
| `event: ad_click` | "clicou no anúncio" |
| `event: ad_impression` | "viu o anúncio (sem clicar necessariamente)" |
| `event: post_save` ou `ig_reel_save` | "salvou o post" |
| `retention_seconds: 2592000` | "30 dias" |
| `retention_seconds: 7776000` | "90 dias" |
| `subtype: ENGAGEMENT` | "audience de engajamento orgânico" |

**Proibido:**
- Mostrar IDs de Page/IG/Ad/Form, `rule` JSON, `event_sources[]` literal.
- Pular esse resumo pra ir direto pro YAML.

## Preview YAML

```yaml
sub_fluxo: engajamento_ig_fb
fonte:
  tipo: Instagram Business
  conta: "@meu_produto"
  id: 17841401234567890 (oculto do aluno, registrado no INDEX local)
tipo_interacao: DM (Direct Message)
janela_dias: 30
retention_seconds: 2592000
nome_final: "[FC] EngajamentoInsta-DM-30d-curso-tarot"
tamanho_estimado: ~840 pessoas

confirma? (digite SIM)
```

## Após criar

```
✅ Audience criada: "[FC] EngajamentoInsta-DM-30d-curso-tarot"

Tamanho estimado: ~{audience_size formatado} pessoas
   (Tamanho real disponível no Gerenciador em ~24h.)

⏰ A partir de agora, toda nova interação do tipo "{tipo_interacao em PT}" na
   {fonte em PT} entra na audience automaticamente.

Onde gerenciar:
   Gerenciador de Anúncios → Públicos → procurar "[FC] Engajamento..."

⚠️ IMPORTANTE — bug visual conhecido da UI da Meta:
   Se você clicar nessa audience no Gerenciador e abrir "Editar":
   - Os dropdowns "Origem" e "Eventos" vão aparecer VAZIOS.
   - Isso é bug COSMÉTICO. A regra está íntegra no banco (confirmada via API).
   - NUNCA clique em "Atualizar público" com os campos vazios — isso
     sobrescreveria a regra com vazio e quebraria a audience.
   - Se abrir por engano, feche pelo "Cancelar" ou pelo "X".

   O painel "Resumo" da direita mostra a Conta IG e a Janela corretamente,
   mas TAMBÉM omite o filtro de evento (ex: DM). Pra confirmar o filtro real,
   use /trafego-publicos opção 8 (Listar) ou peça a releitura via API.

Próximos passos:

🎯 Remarketing pra quem engajou
   /trafego-criar-campanha → usar essa audience como targeting principal.
   Especialmente potente pra DM, Lead Form aberto (sem enviar) e quem salvou anúncio.

🎯 Lookalike de quem engajou
   /trafego-publicos → opção Lookalike → escolher essa audience como source.
   Não tão potente quanto LAL de Customer Match (compradores), mas melhor que LAL fria.

🎯 Combinar com outras audiences (próxima rodada da skill)
   Quando o sub-fluxo de Combinação existir: "Engajou no IG E não comprou ainda"
   pra remarketing limpo.

📝 Registrado em: meus-produtos/{ativo}/trafego/publicos/{audience_id}.md
```

## Limites e pegadinhas

- **Page do Facebook precisa estar conectada ao Business Manager.** Se for página pessoal/perfil pessoal: Meta rejeita o POST.
- **Instagram Business precisa estar conectada à Page do Facebook** (via Business Manager). Conta IG pessoal não funciona.
- **Janela máxima por source type:**
  - `page` / `ig_business`: 365 dias
  - `ad`: 365 dias (mas só conta período em que o ad rodou)
  - `lead_gen`: 90 dias (limite Meta)
  - `event`: até o fim do evento + 30 dias
- **Anúncios deletados não entram.** Se aluno apagar o ad, audience baseada nele para de receber interações novas (mantém o histórico).
- **Audience expira em 90 dias sem atualização.** Mas como fonte é orgânica e contínua, raramente expira.
- **Não popula com histórico anterior à criação da audience** pra `ad` e `lead_gen`. Pra `page` e `ig_business`, Meta tenta puxar alguns dias retroativos (varia).
- **Bug da UI da Meta — dropdown vazio no modal de edição.** Audiences criadas via API com `type: ig_business` (e também `video`) abrem o modal de "Editar público" com os campos "Origem" e "Eventos" em branco, mesmo com a regra íntegra no banco. Confirmado em 2026-05-27 em audience criada via API com `type: ig_business`: GET na API retorna `event_sources` e `filter` corretos, mas modal renderiza vazio. Painel "Resumo" da direita mostra a Conta + Janela mas omite o evento. **Nunca clicar "Atualizar público" com dropdown vazio** — sobrescreve a regra. Fechar pelo "Cancelar". Único critério de saúde confiável é a API (`GET /<audience_id>?fields=rule,delivery_status,operation_status`).

## Casos de uso VTSD

- **Quadro do produto** → quem engajou com posts que falam do Quadro = audience qualificada de aquisição.
- **Mandala de 18 tipos (Tipos 1-6 de topo de funil)** → "quem viu/curtiu posts educativos" vira fonte de remarketing pra anúncios de meio de funil.
- **Lead Form aberto sem enviar** → audience cirúrgica pra Tipo 14 (Urgência) ou Tipo 16 (Prova Social) — gente quase pronta pra converter.
- **DM no Instagram** → audience super quente pra Tipo 17 (Convite Pessoal) ou Tipo 18 (Pergunta Direta).
