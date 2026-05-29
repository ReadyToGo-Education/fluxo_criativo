# Sub-fluxo. Público por Engajamento de Vídeo

Cria Custom Audience baseada em quem assistiu X% de um vídeo nas plataformas Meta (Facebook ou Instagram). Não depende do pixel.

## Perguntas que cobre

- "Crie um público de quem viu 25% do meu vídeo"
- "Quero remarketing para quem assistiu meu Reel inteiro"
- "Público de quem viu 50% da minha VSL"
- "Lista de remarketing dos engajados com vídeo"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `video_id` | obrigatório | ID do vídeo no Meta (post ID do Facebook ou ID do Instagram media) |
| `percentual` | obrigatório | 25, 50, 75, 100 |
| `janela_dias` | 30 | 1 a 365 |
| `nome_extra` | nome curto do vídeo | Sufixo do nome da audience |

### Como o aluno informa o vídeo

A skill aceita 4 formas, todas com fuzzy match — aluno NUNCA digita `video_id` cru sem opção mais fácil. **Qualquer um dos namespaces de ID funciona** (IG Media ID 17 dígitos, Page Video ID 15-16 dígitos, FB-side video_id 16 dígitos) — o que importa é enviar `prefill=true` no POST (ver `## Endpoint`).

1. **Reels da Conta profissional do Instagram**: skill lista Reels e vídeos publicados nas Contas Profissionais do IG conectadas via `GET /<ig_business_account_id>/media?fields=id,media_type,media_url,caption,thumbnail_url,timestamp,permalink&limit=100`. Filtrar `media_type IN (VIDEO, REELS)`. Aplicar filtro temporal (últimos 30d default, `since`/`until` ajustáveis).

   `object_id` resultante = IG Media ID (17 dígitos).

   Apresentar como `[R1] caption resumida (~50 chars) — views totais — data`. Aluno escolhe pelo código.

   **Erro `code 1 — Please reduce the amount of data you're asking for`:** estreitar janela (90d → 30d → 7d) via `since`/`until`. Se mesmo com 7d vier vazio, oferecer outras fontes.

2. **Vídeos da Página do Facebook**: skill lista vídeos da Biblioteca de Vídeos das Páginas conectadas via `GET /<page_id>/videos?fields=id,title,length,created_time&limit=100`. Filtro temporal igual.

   `object_id` = Page Video ID (15-16 dígitos integer).

   Apresentar como `[FB1] título — duração — data`. Aluno escolhe pelo código.

   **Cenário coberto:** vídeos postados diretamente na Página do FB (orgânico) ou cross-postados do IG com a opção "Compartilhar em Página do Facebook" ativada na publicação do Reel.

   **Nota:** Páginas em "New Page Experience" exigem Page Access Token (não User Token) pra alguns endpoints. Se `GET /<page_id>/videos` retornar `code 1` ou `subcode 2069032`, indicar isso ao aluno.

3. **Vídeos que rodaram como anúncio (dark post)**: skill busca seus ads via `GET /act_<id>/ads?fields=id,name,status,effective_status,creative{id,object_story_id,effective_object_story_id,video_id,thumbnail_url,object_type}&limit=100&effective_status=['ACTIVE','PAUSED','IN_PROCESS','WITH_ISSUES']`.

   Para cada creative com `video_id` ou `object_type == 'VIDEO'`:
   - Resolver `effective_object_story_id` (formato `page_id_post_id`) via `GET /<effective_object_story_id>?fields=attachments{media,subattachments,target,description}`.
   - Extrair o `video_id` (FB-side, 16 dígitos).
   - Deduplicar por video_id.

   Apresentar como `[VA1] título do ad — campanha X — status`. Aluno escolhe pelo código.

   **Cenário coberto:** vídeo subido como criativo direto na campanha (dark post puro), sem post orgânico no IG nem na Página.

4. **URL ou ID direto** (raro): aluno cola URL ou ID, skill detecta o namespace e valida:
   - **17 dígitos** → trata como IG Media ID, valida via `GET /<id>?fields=id,media_type,media_url,permalink,caption`.
   - **15-16 dígitos** → tenta `GET /<id>?fields=from,source,permalink_url,length,title` (FB-side). Se `from.id` for Página conectada → Page Video. Senão → ad creative.
   - **URL do IG (instagram.com/reel/...)** → extrai shortcode, resolve via Graph API pra obter o IG Media ID.
   - **URL do FB (facebook.com/.../videos/...)** → extrai numérico, valida como Page Video.

   **Bloquear apenas** se a Graph API retornar 404 (vídeo não existe ou não acessível pelo token).

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Aluno **nunca digita video_id cru** — sempre via listagem ou URL.

### Ordem fixa

1. **Vídeo.** Pergunta neutra:
   ```
   De qual vídeo você quer criar a audience?

   1. Reels da minha Conta profissional do Instagram (últimos 30 dias)
   2. Vídeos da minha Página do Facebook
   3. Vídeos que rodaram como anúncio em minhas campanhas (dark post)
   4. Colar URL ou ID direto (raro)

   Digite o número (Enter pra usar 1):
   ```
   - Se (1): lista Reels via `/<ig_business_account_id>/media`, apresenta `[R1] caption — views — data`. Aluno escolhe pelo código.
   - Se (2): lista vídeos via `/<page_id>/videos`, apresenta `[FB1] título — duração — data`.
   - Se (3): busca ads + resolve via dark post conforme item 3 da seção `### Como o aluno informa o vídeo`. Apresenta como `[VA1] título — campanha X — status`.
   - Se (4): aluno cola URL ou ID, skill detecta namespace (17 dígitos = IG Media, 15-16 = FB-side) e valida.

   **Bloqueio:** se o vídeo não está em página/perfil conectado ao BM (retorna 404 no GET), avisar e voltar.

2. **Percentual.** Numerada:
   ```
   Qual percentual assistido a pessoa precisa atingir pra entrar na audience?

   1. 25% (audience maior, mais quente que prospect frio)
   2. 50% (default — equilíbrio)
   3. 75% (audience menor, muito quente)
   4. 100% (assistiu o vídeo completo — audience pequena, super quente)

   Digite o número (Enter pra usar 2):
   ```
   Skill mapeia internamente:
   - 25 → `video_view_25_percent`
   - 50 → `video_view_50_percent`
   - 75 → `video_view_75_percent`
   - 100 → `video_view_95_percent` (Meta usa 95% como "completou")

3. **Janela.** Numerada (parecida com `publico-evento-padrao.md`):
   ```
   Por quanto tempo manter a pessoa na audience?

   1. 30 dias (default)
   2. 60 dias
   3. 90 dias
   4. 180 dias
   5. 365 dias (máximo — só recomendado pra vídeos high-value)
   6. Outro (digito)

   Digite o número (Enter pra usar 1):
   ```

4. **Vídeos extras (opcional).** Numerada:
   ```
   Quer adicionar mais vídeos? (audience inclui quem assistiu qualquer um deles)

   1. Não, só esse vídeo (default)
   2. Sim, vou escolher mais (até 10 no total)

   Digite o número:
   ```
   Se (2): voltar ao passo 1 pra mais vídeos. Repetir até aluno encerrar.

5. **Nome.** Auto-gerado seguindo `[FC] Video{%}pct-{nome_video_resumido}-{janela}d-{produto-slug}` e confirmação.

**Proibido:**
- Pedir `video_id`, `event_sources`, `retention_seconds`, `video_view_X_percent` direto ao aluno.
- Agrupar 2+ inputs na mesma mensagem.
- Pular pro Preview YAML sem passar pelos passos 1-5.

## Endpoint

> ⚠️ **3 campos obrigatórios pra audience de view via API (descoberto empiricamente em 2026-05-27 por engenharia reversa de 6 audiences populadas + 4 testes de POST):**
>
> 1. **`subtype=ENGAGEMENT`** (não VIDEO — apesar do SDK Python listar VIDEO, Meta v25 retorna erro 1870029 "sintaxe muito antiga" pra subtype=VIDEO).
> 2. **`retention_days`** (inteiro de dias, NÃO `retention_seconds`).
> 3. **`prefill=true`** ← campo crítico. Sem isso, a audience cria mas:
>    - NÃO pega histórico retroativo de viewers (só viewers futuros)
>    - Picker do Audiences Manager fica vazio (vínculo de asset não fecha)
>    - `data_source.creation_params` fica `"[]"` em vez de `"{\"prefill\":\"true\"}"`

```
POST /act_<id>/customaudiences
Parâmetros (form-urlencoded):
- name: "[FC] Video{percentual}pct-{nome_extra}-{janela}d-{produto-slug}"
- subtype: ENGAGEMENT
- retention_days: <janela_dias>
- prefill: true
- description: "Quem assistiu {percentual}% do(s) vídeo(s) {titulos} nos últimos {janela}d."
- rule: <JSON array, exemplo abaixo>
```

**Rule** (array plano de objetos `{event_name, object_id}`):

```json
[
  {"event_name": "video_view_50_percent", "object_id": <video_id_1>},
  {"event_name": "video_view_50_percent", "object_id": <video_id_2>}
]
```

> ⚠️ **Formatos que NÃO funcionam (testados e refutados):**
>
> 1. **Flex rule moderno** (`inclusions/filter/event_sources type=video`) → erro 1870049 "Formato de regra de público anterior".
> 2. **Pré-v3.0** (`{video: [{video_id, video_view_percentage}]}`) → erro 1870029 "Sintaxe muito antiga".
> 3. **`subtype=VIDEO`** → erro 1870029 (mesmo apesar de existir no SDK Python).
> 4. **`data_source[type]=...` via bracket notation** → POST aceita mas `creation_params` continua vazio (precisa do `prefill=true` top-level).
> 5. **PATCH `data_source.creation_params` em audience já criada** → POST retorna `{"success":true}` mas valor é ignorado (`creation_params` continua `"[]"`).

**Sobre `object_id`:** Meta aceita tanto integer quanto string no JSON. Multiplos vídeos = múltiplos itens no array (operador OR implícito).

**Eventos válidos:**
- `video_view_3_seconds`
- `video_view_10_seconds`
- `video_view_25_percent`
- `video_view_50_percent`
- `video_view_75_percent`
- `video_view_95_percent` (Meta usa 95% para "completou", mapeia 100→95)

A skill aceita `100` mas mapeia internamente para `video_view_95_percent`.

### Verificação pós-criação (recomendada)

Após o POST, ler `GET /<audience_id>?fields=data_source` e confirmar:

```json
"data_source": {
  "type": "EVENT_BASED",
  "sub_type": "ENGAGEMENT_EVENTS",
  "creation_params": "{\"prefill\":\"true\"}"   ← deve estar assim
}
```

Se `creation_params` vier `"[]"`, o `prefill=true` não foi enviado corretamente — a audience vai populá apenas com viewers futuros e o picker da UI fica vazio.

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

**Quando exibir:** sempre, após coletar inputs 1-5. Antes do Preview YAML.

**Formato fixo:**

```
📋 Antes de eu criar essa audience na sua conta, deixa eu te resumir:

Vou criar a audience "{nome}":

Quem entra:
   Pessoas que assistiram pelo menos {percentual em PT} do vídeo "{titulo_video}"
   (duração: {duracao}) nos últimos {janela} dias.
   {Se múltiplos vídeos:} Ou de qualquer um destes {N} vídeos: {lista de títulos}.

Tamanho estimado: ~{audience_size formatado, ex: "2,1 mil pessoas"}
   (Baseado em ~{N} views totais do vídeo × curva de retenção típica.)

⏰ Importante:
   - Audience só pega quem assistiu de AGORA em diante (não histórico — depende da política do Meta na criação).
   - Pra Reels curtos (< 10s), 50% e 75% pegam pouca gente. Usar 25% nesse caso.
   - Vídeo precisa estar em página/perfil conectado ao Business Manager.

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → procurar "[FC] Video..."

Tá certo? (sim segue pro YAML, não cancela aqui)
```

**Regras de tradução obrigatórias:**

| Campo técnico | Tradução |
|---|---|
| `video_view_25_percent` | "25% do vídeo" |
| `video_view_50_percent` | "metade do vídeo (50%)" |
| `video_view_75_percent` | "três quartos do vídeo (75%)" |
| `video_view_95_percent` | "vídeo inteiro (95%+)" |
| `subtype: ENGAGEMENT` | "audience de engajamento" |
| `event_sources[{id, type: video}]` | título do vídeo (nunca o id) |
| `retention_seconds: 2592000` | "30 dias" |
| `retention_seconds: 31536000` | "365 dias (um ano)" |

**Proibido:**
- Mostrar `video_id`, `retention_seconds` em número cru, `video_view_X_percent` literal.
- Pular esse resumo pra ir direto pro YAML.

## Preview YAML

```yaml
sub_fluxo: publico_video_view
video:
  id: 1234567890_9876543210
  titulo: "VSL Curso de Tarot — versão 2"
  duracao: "8:32"
  views_totais: 12.480
percentual: 50
evento_meta: video_view_50_percent
janela_dias: 30
retention_seconds: 2592000
nome_final: "[FC] Video50pct-VSL-30d-curso-tarot"
tamanho_estimado: ~2.100 (estimativa baseada em 50% de retenção média do vídeo)

confirma? (digite SIM)
```

## Estimativa de tamanho

Antes de confirmar, a skill estima o tamanho da audience usando uma de duas abordagens, na ordem de preferência:

### Abordagem A (preferida): usar `video_pXX_watched_actions` dos ads

Quando o `video_id` escolhido tem insights agregados disponíveis nos ads que o usam:

```
SE existem ads com esse video_id:
    pega insights agregados via GET /act_<id>/insights?fields=video_p25_watched_actions,
        video_p50_watched_actions,video_p75_watched_actions,video_p95_watched_actions
        &filtering=[{field:'creative.video_id',operator:'EQUAL',value:<video_id>}]
    soma_views_pct = soma(video_pXX_watched_actions[value]) pelos ads
    SE numero_de_ads_com_mesmo_video > 3:
        fator_overlap = 1.5 a 2.0  (média típica de sobreposição em ads paralelos)
    SENÃO:
        fator_overlap = 1.0
    estimativa = soma_views_pct / fator_overlap
```

### Abordagem B (fallback): curva heurística

Quando não há insights disponíveis (vídeo orgânico só, ou conta sem histórico de ads pra esse video_id):

```
estimativa = plays_totais * curva_retencao(percentual)
```

**Curva ajustada (média de mercado em contas com vídeo rodando em múltiplos ads, com sobreposição):**

| Percentual | % dos plays totais |
|---|---|
| 25% | 5% a 8% |
| 50% | 3% a 5% |
| 75% | 1,5% a 3% |
| 95% (=100%) | 0,8% a 1,5% |

> ⚠️ **Atenção:** a curva acima usa **plays totais** (somatório de visualizações nos ads + orgânico). Em conta com **um único ad** rodando o vídeo (sem sobreposição), os plays totais ≈ plays únicos, e a curva de retenção real é maior:
>
> | Percentual | % dos plays únicos |
> |---|---|
> | 25% | 40% a 60% |
> | 50% | 20% a 35% |
> | 75% | 10% a 18% |
> | 95% | 4% a 8% |
>
> A skill DEVE detectar quantos ads usam o `video_id` antes de aplicar a curva. Mais de 3 ads → usar curva ajustada (sobreposição). Até 3 ads → curva de plays únicos.

### Validação empírica (caso real 2026-05-27)

Conta `act_1234567890`, vídeo `NomeDoVideo` rodando em 6 ads:
- Plays totais: 53.207 em 90d
- Audience real (25%): ~1.800-2.000 pessoas
- Taxa real: 3,4% dos plays totais (cai dentro da curva ajustada)

A curva antiga (60% dos plays totais = 31.924) **superestimava em 16x** porque não considerava sobreposição.

Esses valores são apenas estimativa. Tamanho real é calculado pelo Meta após criação (24-48h).

## Após criar

```
✅ Audience criada: [FC] Video50pct-VSL-30d-curso-tarot
   ID: 6123456791

Tamanho estimado: ~2.100 pessoas. Tamanho real disponível no Audiences Manager em ~24h.

Próximo passo:
- Para criar lookalike a partir dela: /trafego-publicos opção 5
- Para usar em retargeting de vídeo: /trafego-criar-campanha
```

### ⚠️ Aviso obrigatório a entregar ao aluno após criação

Incluir SEMPRE na mensagem final, depois do bloco `✅ Audience criada`:

```
⚠️ Se for abrir o modal de edição dessa audience no Gerenciador de Públicos,
NUNCA clica em "Atualizar público" se o card "Selecionar vídeos" aparecer vazio.
Sempre fecha pelo "Cancelar". Clicar em "Atualizar" com o picker vazio
sobrescreve a regra com lista vazia e zera a audience (perde o vínculo do
vídeo e o populamento).

O picker vazio NÃO é problema — audience funciona em campanhas mesmo assim
(ver seção "Sintoma pós-criação" da skill se quiser entender o porquê).
```

## Tratamento de erro 2654/1713216

Se ao executar o POST a Meta responder com erro `2654` (subcode `1713216`) e mensagem contendo `"isn't associated with a Page or New Page Experience"`, a skill DEVE:

1. Abortar a criação (não tentar de novo com o mesmo vídeo).
2. Informar ao aluno em linguagem clara:
   ```
   Esse vídeo é um ad creative puro (subido direto pra biblioteca de criativos
   sem virar post de Página). A Meta não permite criar audience de view de
   ad creatives. Pra criar essa audience, você precisa primeiro publicar o
   vídeo como post da sua Página (Facebook ou Instagram comercial) e depois
   usar o post na criação.
   ```
3. Sugerir alternativa: "Quer que eu liste os vídeos elegíveis (já publicados em Página)?"

## Sintoma pós-criação: picker "Selecionar vídeo" vazio

Verificar primeiro: `GET /<audience_id>?fields=data_source,delivery_status,operation_status`.

**Critério de saúde definitivo:**
- `data_source.creation_params == "{\"prefill\":\"true\"}"` E
- `delivery_status.code == 200`
- → **vínculo permanente e íntegro, audience funciona em campanhas normalmente**, independente do que a UI mostra.

**Se `creation_params == "[]"`:** faltou `prefill=true` no POST original. PATCH não corrige (Meta aceita mas ignora). A correção é **deletar a audience e recriar** com `prefill=true` no payload.

**Se `creation_params == "{\"prefill\":\"true\"}"` mas o picker do Audiences Manager mostra "Selecionar vídeo (0)":**

⚠️ **Esse picker pode levar horas, dias OU NUNCA atualizar visualmente.** Confirmado empiricamente em 4 audiences consecutivas numa mesma conta de produção, todas com `creation_params=prefill:true`, rule íntegra, audience populada com milhares de pessoas, e card visualmente vazio mesmo após horas.

**NÃO é bloqueante.** Audience funciona em campanhas (entrega, otimização, exclusão) normalmente. É puramente um bug/limitação de exibição da UI da Meta.

**NÃO tentar "consertar" abrindo o modal de edição e clicando "Atualizar público"** — ver aviso na seção `## Após criar`.

## Avisos

- **`prefill=true` é obrigatório.** Sem ele, audience só pega viewers futuros e picker fica vazio. Ver `## Endpoint` pra payload completo.
- **Janela máxima 365 dias** pra video view audience (mais ampla que pixel — máx 180).
- **Vídeos curtos (< 10s)** geralmente não geram volume relevante em 50%/75%. Para Reels rápidos, recomendar percentual 25.
- **Audience não popula retroativamente para criações novas** sob certas condições (Meta tem mudado regras). Para histórico longo, criar antes de publicar mais conteúdo do mesmo tipo.
- **Janela máxima**: 365 dias para vídeo (mais longa que website).

## Casos especiais

### Múltiplos vídeos
A skill aceita lista de até 10 vídeos numa única audience (operador `OR`). Cria uma audience só com a regra:
```
quem viu X% de qualquer um dos vídeos A, B ou C
```
Útil para "público de quem engajou com qualquer vídeo da campanha".

### Cruzamento com outro evento
Não suportado nesta skill no MVP. Se aluno pedir "viu 50% do vídeo E adicionou ao carrinho", encaminhar para criação manual no Audiences Manager (Meta exige rule mais elaborada).
