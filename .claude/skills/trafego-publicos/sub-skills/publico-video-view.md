# Sub-fluxo. Público de Quem Viu Vídeo

Cria um público personalizado de quem assistiu X% de um vídeo no Facebook ou no Instagram. Não depende do pixel.

Passo 0 (produto ativo, conexão, conta) e gate: ver `SKILL.md` desta skill.

## Perguntas que cobre

- "Crie um público de quem viu 25% do meu vídeo"
- "Quero remarketing para quem assistiu meu Reel inteiro"
- "Público de quem viu 50% da minha VSL"
- "Lista de remarketing dos engajados com vídeo"

## Inputs

| Input | Padrão | Descrição |
|---|---|---|
| `video_id` | obrigatório | Vídeo escolhido pela listagem (nunca digitado pelo aluno) |
| `percentual` | 50 | 25, 50, 75 ou 100 |
| `janela_dias` | 30 | 1 a 365 |
| `nome_extra` | nome curto do vídeo | Sufixo do nome do público |

## Roteamento por modo (ler primeiro)

O MCP é o caminho padrão. Se a Meta recusar pelo MCP, o aluno cria pelo Gerenciador com o passo a passo desta sub-skill.

- **`MCP_CONECTOR`:**
  1. **Descobrir o vídeo** com as tools de leitura: vídeos que rodaram em anúncios (`ads_get_ad_entities` e `ads_get_creatives`, pegando o vídeo do criativo) e vídeos da biblioteca da conta (`ads_get_ad_videos`). Reels e vídeos publicados só no perfil ou na Página, sem anúncio: o MCP não lista; seguir pelo **passo manual guiado** (o seletor de vídeos do Gerenciador mostra Reels e vídeos da Página).
  2. **Ler o schema da `ads_create_custom_audience`** antes de chamar e montar o pedido com o subtipo de engajamento de vídeo que o schema oferecer, o evento do percentual (`video_view_XX_percent`) e os vídeos escolhidos. Não inventar parâmetro.
  3. **Histórico:** se o schema não tiver opção equivalente ao `prefill` (que faz o público pegar quem já assistiu antes da criação), avisar o aluno antes do bloco 🛡️: "pelo conector, esse público pode juntar só quem assistir daqui para frente. Pelo Gerenciador, ele já nasce com quem assistiu nos últimos {janela} dias." e perguntar:
     ```
     Como prefere seguir?

     1. Criar pelo conector mesmo assim (junta quem assistir a partir de agora)
     2. Criar pelo Gerenciador com o meu passo a passo (já nasce com o histórico)

     Digite o número:
     ```
  4. **Depois de criar, conferir** com `ads_get_custom_audience` (regra, `data_source`, `delivery_status`). Se a Meta recusar o subtipo ou a regra, não insistir: seguir pelo passo manual guiado.
- **`APP`:** `curl` no endpoint abaixo (formato conferido na prática, com `prefill=true`). A listagem de vídeos é leitura e roda normalmente.

## Como o aluno escolhe o vídeo

O aluno **nunca digita `video_id`**. A skill aceita 4 formas. Qualquer um dos tipos de ID funciona (ID de mídia do Instagram com 17 dígitos, ID de vídeo da Página com 15 ou 16 dígitos, ID de vídeo do anúncio com 16 dígitos); no modo App, o que importa é enviar `prefill=true` (ver "Endpoint").

1. **Reels da conta profissional do Instagram.**
   - App: `GET /<ig_business_account_id>/media?fields=id,media_type,media_url,caption,thumbnail_url,timestamp,permalink&limit=100`, filtrando `media_type` em (VIDEO, REELS), últimos 30 dias por padrão (`since`/`until` ajustáveis). Mostrar como `[R1] legenda resumida (~50 caracteres), visualizações, data`.
   - Erro `code 1, Please reduce the amount of data you're asking for`: estreitar a janela (90d → 30d → 7d). Se vier vazio mesmo com 7 dias, oferecer as outras fontes.
   - MCP: passo manual guiado (abaixo).
2. **Vídeos da Página do Facebook.**
   - App: `GET /<page_id>/videos?fields=id,title,length,created_time&limit=100`. Mostrar como `[FB1] título, duração, data`. Cobre vídeos postados na Página e Reels compartilhados na Página.
   - Página na "Nova experiência de Páginas" pode exigir token da Página em alguns endpoints: se vier `code 1` ou `subcode 2069032`, avisar o aluno.
   - MCP: `ads_get_ad_videos` cobre a biblioteca da conta de anúncios; vídeo só da Página vai pelo passo manual guiado.
3. **Vídeos que rodaram como anúncio.**
   - App: `GET -g /act_<id>/ads?fields=id,name,status,effective_status,creative{id,object_story_id,effective_object_story_id,video_id,thumbnail_url,object_type}&limit=100&effective_status=['ACTIVE','PAUSED','IN_PROCESS','WITH_ISSUES']`. Para cada criativo com vídeo, resolver o `effective_object_story_id` (`GET -g /<effective_object_story_id>?fields=attachments{media,subattachments,target,description}`) e tirar o `video_id`. Remover repetidos.
   - MCP: `ads_get_ad_entities` (anúncios) e `ads_get_creatives` (vídeo do criativo).
   - Mostrar como `[VA1] nome do anúncio, campanha X, status`.
4. **Colar link ou ID** (raro). O aluno cola o link; a skill identifica o tipo (17 dígitos = mídia do Instagram, 15 ou 16 = vídeo do Facebook; link `instagram.com/reel/...` ou `facebook.com/.../videos/...`) e confere (no App, por `GET`). Bloquear só se a Meta devolver 404 (vídeo inexistente ou sem acesso).

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**.

### Ordem fixa

1. **Vídeo.**
   ```
   De qual vídeo você quer criar o público?

   1. Reels do meu Instagram profissional (últimos 30 dias)
   2. Vídeos da minha Página do Facebook
   3. Vídeos que rodaram como anúncio nas minhas campanhas
   4. Colar o link do vídeo (raro)

   Digite o número (Enter para usar 1):
   ```
   No modo MCP, as opções 1 e 2 levam ao passo manual guiado, a não ser que o vídeo também esteja na biblioteca da conta.

   **Bloqueio:** vídeo fora de Página ou perfil ligado ao Business (404 na leitura): avisar e voltar.

2. **Percentual.**
   ```
   Quanto do vídeo a pessoa precisa assistir para entrar no público?

   1. 25% (público maior, mais quente que o frio)
   2. 50% (padrão, equilíbrio)
   3. 75% (público menor, muito quente)
   4. 100% (assistiu tudo: público pequeno e muito quente)

   Digite o número (Enter para usar 2):
   ```
   Mapeamento interno: 25 → `video_view_25_percent`; 50 → `video_view_50_percent`; 75 → `video_view_75_percent`; 100 → `video_view_95_percent` (a Meta usa 95% como "completou").

3. **Janela.**
   ```
   Por quanto tempo a pessoa fica no público?

   1. 30 dias (padrão)
   2. 60 dias
   3. 90 dias
   4. 180 dias
   5. 365 dias (máximo, só para vídeos muito valiosos)
   6. Outro (digito)

   Digite o número (Enter para usar 1):
   ```

4. **Mais vídeos (opcional).**
   ```
   Quer incluir mais vídeos? (entra quem assistiu qualquer um deles)

   1. Não, só esse (padrão)
   2. Sim, vou escolher mais (até 10 no total)

   Digite o número:
   ```
   Se (2): voltar ao passo 1. Repetir até o aluno encerrar.

5. **Nome.** Sugerir `[WS] Video{%}pct-{nome_video_resumido}-{janela}d-{produto-slug}` e confirmar.

**Proibido:** pedir `video_id`, `event_sources`, `retention_seconds`, `video_view_X_percent` ao aluno; agrupar inputs; pular para o bloco 🛡️ sem os passos 1 a 5.

## Passo manual guiado no Gerenciador (MCP sem o vídeo, recusa da Meta ou escolha do aluno)

```
Você cria esse público em 2 minutos no Gerenciador:

📋 Passo 1. Gerenciador de Anúncios → menu "Públicos" → "Criar público" →
           "Público personalizado"
📋 Passo 2. Em "Fontes da Meta", escolha "Vídeo" e clique em "Avançar"
📋 Passo 3. Em "Engajamento", escolha "{texto do percentual, ex: Pessoas que
           assistiram a pelo menos 50% do seu vídeo}"
📋 Passo 4. Clique em "Escolher vídeos", selecione a origem (Página ou conta do
           Instagram) e marque: {lista de vídeos}
📋 Passo 5. Retenção: {janela} dias
📋 Passo 6. Nome do público: {nome}
📋 Passo 7. Clique em "Criar público"

🛟 Se algum nome de botão estiver diferente, me mande um print.

Me avise com "feito" que eu confiro o público pela listagem.
```

Depois do "feito", conferir pela listagem (`ads_get_ad_account_custom_audiences`), gravar o registro local e seguir para "Depois de criar".

## Endpoint (modo App)

> ⚠️ **3 campos obrigatórios para público de vídeo pela API** (descobertos na prática em 2026-05-27, estudando 6 públicos que funcionavam e 4 testes de criação):
>
> 1. **`subtype=ENGAGEMENT`** (não VIDEO: apesar de existir no SDK Python, a Meta v25 devolve erro 1870029 "sintaxe muito antiga" para `subtype=VIDEO`).
> 2. **`retention_days`** (número inteiro de dias, NÃO `retention_seconds`).
> 3. **`prefill=true`**, o campo crítico. Sem ele, o público é criado mas:
>    - NÃO pega quem já assistiu (só futuros)
>    - o seletor de vídeos do Gerenciador fica vazio
>    - `data_source.creation_params` fica `"[]"` em vez de `"{\"prefill\":\"true\"}"`

```
POST /act_<id>/customaudiences
Parâmetros (form-urlencoded):
- name: "[WS] Video{percentual}pct-{nome_extra}-{janela}d-{produto-slug}"
- subtype: ENGAGEMENT
- retention_days: <janela_dias>
- prefill: true
- description: "Quem assistiu {percentual}% do(s) vídeo(s) {titulos} nos últimos {janela}d."
- rule: <lista JSON, exemplo abaixo>
```

**Regra** (lista simples de `{event_name, object_id}`):

```json
[
  {"event_name": "video_view_50_percent", "object_id": "<video_id_1>"},
  {"event_name": "video_view_50_percent", "object_id": "<video_id_2>"}
]
```

> ⚠️ **Formatos que NÃO funcionam (testados e descartados):**
>
> 1. Regra moderna (`inclusions/filter/event_sources type=video`): erro 1870049 "formato de regra de público anterior".
> 2. Formato antigo (`{video: [{video_id, video_view_percentage}]}`): erro 1870029 "sintaxe muito antiga".
> 3. `subtype=VIDEO`: erro 1870029.
> 4. `data_source[type]=...` entre colchetes: a Meta aceita, mas `creation_params` continua vazio (precisa do `prefill=true` no nível de cima).
> 5. Alterar `data_source.creation_params` depois de criado: a Meta responde `{"success":true}` mas ignora.

`object_id` pode ir como número ou texto. Vários vídeos = vários itens na lista (OU implícito).

**Eventos válidos:** `video_view_3_seconds`, `video_view_10_seconds`, `video_view_25_percent`, `video_view_50_percent`, `video_view_75_percent`, `video_view_95_percent` (100% vira 95%).

### Conferência depois de criar (recomendada)

`GET /<audience_id>?fields=data_source` (App) ou `ads_get_custom_audience` (MCP), esperando:

```json
"data_source": {
  "type": "EVENT_BASED",
  "sub_type": "ENGAGEMENT_EVENTS",
  "creation_params": "{\"prefill\":\"true\"}"
}
```

Se `creation_params` vier `"[]"`, o público só vai juntar quem assistir daqui para frente e o seletor do Gerenciador fica vazio.

## Resumo em linguagem natural (obrigatório, antes do bloco 🛡️)

```
📋 Antes de eu criar esse público na sua conta, um resumo:

Vou criar o público "{nome}".

Quem entra:
   Pessoas que assistiram pelo menos {percentual em português} do vídeo "{titulo_video}"
   (duração: {duracao}) nos últimos {janela} dias.
   {Se vários vídeos:} Ou de qualquer um destes {N} vídeos: {lista de títulos}.

Tamanho estimado: ~{tamanho formatado, ex: "2,1 mil pessoas"}
   (calculado a partir de ~{N} visualizações do vídeo e da curva de retenção típica)

⏰ Importante:
   - {Modo App, ou MCP com equivalente ao prefill:} o público já nasce com quem
     assistiu dentro da janela.
   - {MCP sem equivalente ao prefill:} o público junta quem assistir a partir de agora.
   - Em Reels curtos (menos de 10s), 50% e 75% pegam pouca gente. Use 25%.
   - O vídeo precisa estar em Página ou perfil ligado ao Business.

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → procurar "[WS] Video..."

Está certo? (sim segue para a confirmação final, não cancela aqui)
```

**Tradução obrigatória:**

| Campo técnico | Tradução |
|---|---|
| `video_view_25_percent` | "25% do vídeo" |
| `video_view_50_percent` | "metade do vídeo (50%)" |
| `video_view_75_percent` | "três quartos do vídeo (75%)" |
| `video_view_95_percent` | "o vídeo inteiro (95% ou mais)" |
| `subtype: ENGAGEMENT` | "público de engajamento" |
| ID do vídeo | título do vídeo (nunca o ID) |
| `retention_days: 30` | "30 dias" |
| `retention_days: 365` | "365 dias (um ano)" |

**Proibido no resumo:** ID do vídeo, janela em segundos, `video_view_X_percent` literal.

## Preview YAML (dentro do bloco 🛡️)

```yaml
sub_fluxo: publico_video_view
modo: MCP_CONECTOR | APP
video:
  titulo: "VSL Curso de Tarot, versão 2"
  duracao: "8:32"
  visualizacoes_totais: 12.480
percentual: 50
evento_meta: video_view_50_percent
janela_dias: 30
prefill: true | "sem equivalente no conector (só futuros)"
nome_final: "[WS] Video50pct-VSL-30d-curso-tarot"
tamanho_estimado: ~2.100 (estimativa pela retenção média do vídeo)
```

## Estimativa de tamanho

Antes de confirmar, a skill estima o tamanho por uma de duas abordagens, nesta ordem:

### Abordagem A (preferida): `video_pXX_watched_actions` dos anúncios

Quando o vídeo escolhido rodou em anúncios:

> ⚠️ **NÃO filtrar insights por `creative.video_id`.** A Marketing API v25 recusa com `error code 100, Filtering field creative.video_id is invalid` (confirmado na prática em 2026-05-29). O caminho que funciona: descobrir os `ad.id` que usam cada vídeo (já vieram na listagem da coleta) e filtrar os insights por `ad.id IN [...]` no `level=ad`.

```
SE existem anúncios com esse vídeo:
    # 1. mapear ad_ids -> vídeo a partir da listagem de anúncios da coleta
    ad_ids = [anúncios cujo criativo usa o(s) vídeo(s) escolhido(s)]
    # 2. somar a retenção do percentual escolhido só desses anúncios
    insights level=ad, fields=ad_id,video_pXX_watched_actions (XX = percentual),
        date_preset=last_90d, filtering=[{field:'ad.id',operator:'IN',value:[<ad_ids>]}]
        (MCP: tool ads_insights_* com os mesmos filtros, conforme o schema;
         App: GET /act_<id>/insights; ou /trafego-insights)
    soma_views_pct = soma de video_pXX_watched_actions[value]
    SE mais de 3 anúncios com o mesmo vídeo:
        fator_sobreposicao = 1,5 a 2,0
    SENÃO:
        fator_sobreposicao = 1,0
    estimativa = soma_views_pct / fator_sobreposicao
```

> Anúncios sem gasto na janela podem não voltar no insights (normal). Somar só os que vierem. Com vários vídeos num público, juntar os `ad.id` de todos no mesmo filtro.

### Abordagem B (reserva): curva de retenção

Sem insights (vídeo só orgânico, ou conta sem anúncio com o vídeo):

```
estimativa = plays_totais * curva_retencao(percentual)
```

**Curva com sobreposição (vídeo rodando em vários anúncios):**

| Percentual | % dos plays totais |
|---|---|
| 25% | 5% a 8% |
| 50% | 3% a 5% |
| 75% | 1,5% a 3% |
| 95% (=100%) | 0,8% a 1,5% |

> ⚠️ A curva acima usa **plays totais** (soma de visualizações nos anúncios e no orgânico). Com **um único anúncio** rodando o vídeo, plays totais ≈ plays únicos e a retenção real é maior:
>
> | Percentual | % dos plays únicos |
> |---|---|
> | 25% | 40% a 60% |
> | 50% | 20% a 35% |
> | 75% | 10% a 18% |
> | 95% | 4% a 8% |
>
> A skill confere quantos anúncios usam o vídeo antes de escolher a curva. Mais de 3 anúncios: curva com sobreposição. Até 3: curva de plays únicos.

### Exemplo real (2026-05-27)

Conta de exemplo, vídeo rodando em 6 anúncios:
- Plays totais: 53.207 em 90 dias
- Público real (25%): cerca de 1.800 a 2.000 pessoas
- Taxa real: 3,4% dos plays totais (dentro da curva com sobreposição)

A curva antiga (60% dos plays totais = 31.924) superestimava 16 vezes porque ignorava a sobreposição.

É só estimativa. O tamanho real a Meta calcula depois da criação (24 a 48h).

## Depois de criar

```
✅ Público criado: [WS] Video50pct-VSL-30d-curso-tarot

Tamanho estimado: ~2.100 pessoas. O tamanho real aparece no Gerenciador em até 24h.

Próximos passos:
- Criar um semelhante a partir dele: /trafego-publicos opção 5
- Usar em remarketing de vídeo: /trafego-criar-campanha
```

### ⚠️ Aviso obrigatório depois da criação

Sempre incluir, depois do bloco "✅ Público criado":

```
⚠️ Se abrir a edição desse público no Gerenciador, NUNCA clique em "Atualizar
público" se o quadro "Selecionar vídeos" aparecer vazio. Feche pelo "Cancelar".
Atualizar com o seletor vazio troca a regra por uma lista vazia e zera o público.

O seletor vazio NÃO é problema: o público funciona normalmente nas campanhas.
```

## Erro 2654 / 1713216

Se a Meta responder erro `2654` (subcode `1713216`) com a mensagem `"isn't associated with a Page or New Page Experience"`:

1. Parar (não tentar de novo com o mesmo vídeo).
2. Explicar:
   ```
   Esse vídeo foi subido direto como criativo de anúncio, sem virar post de Página.
   A Meta não permite público de visualização desse tipo de vídeo. Para criar,
   publique o vídeo como post da sua Página (Facebook ou Instagram profissional)
   e use o post na criação.
   ```
3. Oferecer: "Quer que eu liste os vídeos que já estão publicados em Página?"

## Seletor "Selecionar vídeo" vazio depois da criação

Conferir primeiro: `ads_get_custom_audience` (MCP) ou `GET /<audience_id>?fields=data_source,delivery_status,operation_status` (App).

**Critério de saúde definitivo:**
- `data_source.creation_params == "{\"prefill\":\"true\"}"` e
- `delivery_status.code == 200`
- → vínculo íntegro, o público funciona nas campanhas, não importa o que a tela mostra.

**`creation_params == "[]"`:** faltou `prefill=true` na criação. Alterar depois não resolve (a Meta aceita e ignora). A correção é criar de novo com `prefill=true` (e, se o aluno quiser, excluir o antigo pela opção 8, com confirmação própria).

**`creation_params` certo mas o Gerenciador mostra "Selecionar vídeo (0)":** o seletor pode levar horas, dias ou NUNCA atualizar. Confirmado na prática em 4 públicos seguidos numa mesma conta, todos com regra íntegra, milhares de pessoas e quadro vazio na tela. Não bloqueia nada: é limitação de exibição do Gerenciador. Não tentar "consertar" pela tela de edição.

## Avisos

- **No modo App, `prefill=true` é obrigatório.** Sem ele, só futuros e seletor vazio.
- **Janela máxima de 365 dias** para vídeo (mais que os 180 do pixel).
- **Vídeos curtos (menos de 10s):** 50% e 75% rendem pouco. Recomendar 25%.
- **A Meta muda as regras de histórico** de tempos em tempos. Para histórico longo, criar o público antes de publicar mais vídeos do mesmo tipo.

## Casos especiais

### Vários vídeos
Até 10 vídeos num público só (OU): "quem viu X% de qualquer um dos vídeos A, B ou C". Útil para "quem engajou com qualquer vídeo da campanha".

### Cruzar com outro evento
Não suportado aqui. "Viu 50% do vídeo E adicionou ao carrinho" exige regra mais elaborada: encaminhar para criação manual no Gerenciador.
