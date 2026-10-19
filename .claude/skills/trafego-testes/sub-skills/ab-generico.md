# Sub-fluxo. A/B Genérico (uma dimensão por vez)

Cria um teste A/B disciplinado variando UMA dimensão: criativo, headline, audiência (inclui faixa etária), posicionamento, lance, estrutura ou CTA. A mecânica é a mesma para todas. O que muda entre elas: o nível onde o teste é criado (anúncio, conjunto, campanha), o campo que varia, a métrica principal da leitura e os avisos.

Passo 0 e gate: ver `SKILL.md` desta skill.

---

## ⚠️ Lições de campo (erros reais da API, ler antes de copiar)

> Aprendido numa sessão real (2026-06-09) montando um A/B de `faixa_etaria` na campanha inteira (CBO com vários públicos). O caminho "copiar a campanha com `deep_copy`" **falhou 4 vezes**, por motivos diferentes. O que funciona é **recriar a partir da leitura**, não copiar.

### Não confie no `POST /<id>/copies` para copiar estrutura de teste

| Erro (subcode) | Mensagem | Quando acontece |
|---|---|---|
| **1885194** | "A solicitação de cópia é muito grande" | `deep_copy=true` na campanha. A cópia **síncrona** aceita **menos de 3 objetos** no total (campanha, conjuntos e anúncios). Qualquer campanha real estoura. |
| **3858504** | "O criativo não deve incluir aprimoramentos padrão" | `deep_copy=true` no conjunto, ao **recriar** o criativo (os aprimoramentos padrão foram descontinuados). |
| **2446347** | "Falta o sinalizador use_existing_post" | `deep_copy=true` no conjunto cujo anúncio usa **post existente**. |
| **1870227** | "A sinalização de público Advantage é obrigatória" | criar ou copiar conjunto **sem** `targeting_automation.advantage_audience` (0 ou 1). |

### Padrão correto por modo

**Modo App: ler e recriar.**

1. **Ler a configuração do molde por `GET`** na Graph API:
   - `GET /<campaign_id>?fields=objective,buying_type,daily_budget,bid_strategy,special_ad_categories`
   - `GET -g /<adset_id>?fields=name,optimization_goal,billing_event,promoted_object,attribution_spec,destination_type,is_dynamic_creative,targeting`
   - `GET -g /<ad_id>?fields=name,creative{id}`
2. **Criar a campanha casca** (`POST /campaigns`) com o objetivo, o orçamento e a categoria lidos. Em CBO, o orçamento vai na campanha; os conjuntos **não** levam orçamento.
3. **Recriar cada conjunto** (`POST /adsets`) com o `targeting` lido (trocando só a dimensão testada) **e `targeting_automation: {advantage_audience: 0}`** (obrigatório). Em CBO, não mandar `daily_budget` nem `bid_strategy` no conjunto.
4. **Recriar cada anúncio apontando para o criativo existente:** `creative={"creative_id":<id_lido>}`. **Nunca** copiar o anúncio com `deep_copy`: apontar pelo ID pula a revalidação que quebra (3858504 e 2446347).
5. `POST /<id>/copies` só serve para **1 conjunto com 1 anúncio** (menos de 3 objetos).

**Modo MCP: copiar pelo conector, com plano B guiado.**

O `ads_get_ad_entities` **não devolve a segmentação do conjunto** (`targeting`, `age_min`, `age_max`, `promoted_object` respondem `Unsupported field(s)`). Por isso o "ler e recriar" acima **só funciona no App**. No MCP:

1. **Tentar copiar pelo conector:** `ads_create_ad_set` com `source_adset_id` (copiar conjunto) e `ads_create_ad` com `source_ad_id` (copiar anúncio), conforme o schema das tools. Para a campanha inteira, criar a campanha casca com `ads_create_campaign` e copiar os conjuntos um a um para dentro dela (se o schema permitir indicar a campanha de destino).
2. **Aplicar a variação** com `ads_update_entity`. Em dimensão que mexe na segmentação (audiência, faixa etária, posicionamento), só se o schema aceitar mudar o campo sozinho, sem reenviar a segmentação inteira (que o conector não lê). Se exigir a segmentação completa, a variação vai pelo passo guiado do item 3.
3. **Se a cópia falhar (ou a variação não puder ir pelo conector): duplicação guiada no Gerenciador.** O aluno duplica e muda a dimensão; a skill confere pela leitura (nome, status, orçamento) e registra:
   ```
   O conector não conseguiu copiar essa estrutura. Você faz em uns 3 minutos
   no Gerenciador:

   📋 Passo 1. Gerenciador de Anúncios → marque {a campanha | o conjunto} "{nome do molde}"
   📋 Passo 2. Clique em "Duplicar" → escolha {"Nova campanha" | "Campanha existente: {nome}"}
              → "Duplicar"
   📋 Passo 3. Na cópia, troque o nome para "{nome do teste}"
   📋 Passo 4. Mude SÓ isto: {dimensão em português, ex: "Idade: 25 a 34"}
   📋 Passo 5. Orçamento: R$ {valor}/dia
   📋 Passo 6. Deixe a cópia DESATIVADA (chave desligada) e clique em "Publicar"
              (ou "Fechar" para manter como rascunho)
   {Repetir para a variação B}

   🛟 Se algum nome de botão estiver diferente, me mande um print.

   Me avise com "feito" que eu confiro pela listagem.
   ```

### Duas falhas de fidelidade para vigiar

- **Idade real ≠ nome do conjunto.** O nome pode dizer "25-64" e o `targeting` ter `age_max: 55`. No App, fatiar sempre a partir do `targeting` lido, não do nome. No MCP (sem leitura da segmentação), pedir ao aluno para conferir a idade real no Gerenciador antes de definir as faixas.
- **`promoted_object` pode ser conversão personalizada.** O molde pode otimizar por `custom_conversion_id` + `pixel_rule` (filtro por produto), não só `pixel_id` + `custom_event_type: PURCHASE`. Ler o `promoted_object` inteiro e repetir **igual nos N lados**. Se simplificar (ex: cair para PURCHASE puro), aplicar a mesma simplificação nos dois lados e registrar em "Observações": o teste continua justo, mas não é cópia fiel.

> A `duplicar-variando` e a `campanha-remarketing` têm o mesmo risco ao copiar estrutura e seguem este padrão.

---

## Quando esta sub-skill é usada

Toda opção de [1] a [8] do menu da `/trafego-testes` cai aqui:

| Opção | `dimensao` |
|---|---|
| [1] A/B de criativo | `criativo` |
| [2] A/B de headline | `headline` |
| [3] A/B de audiência | `audiencia` |
| [4] A/B de faixa etária | `faixa_etaria` (caso particular de `audiencia`) |
| [5] A/B de posicionamento | `posicionamento` |
| [6] A/B de lance | `lance` |
| [7] A/B de estrutura | `estrutura` |
| [8] A/B de CTA | `cta` |

[9] (`duplicar-variando`), [10] (`campanha-remarketing`) e [11] (`leitura-resultado`) têm sub-skills próprias.

---

## Mapa das 8 dimensões (referência única)

| `dimensao` | Nível | Modelo recomendado | Campo(s) que mudam | Métrica principal | Conversões mín./lado |
|---|---|---|---|---|---|
| `criativo` | anúncio | `adsets_separados` (preferido) ou `ads_mesmo_adset` | `creative.image_hash` ou `creative.video_id` | CPA | 50 (low/mid), 30 (high) |
| `headline` | anúncio | `ads_mesmo_adset` (preferido) ou `adsets_separados` | `creative.object_story_spec.link_data.name` | CTR (CPA secundário) | 50 |
| `audiencia` | conjunto | `adsets_separados` (obrigatório) | `targeting.custom_audiences`, `targeting.interests`, `targeting.behaviors`, `targeting.geo_locations` | CPA | 50 |
| `faixa_etaria` | conjunto | `adsets_separados` (obrigatório) | `targeting.age_min`, `targeting.age_max` (o resto igual) | CPA | 50 |
| `posicionamento` | conjunto | `adsets_separados` (obrigatório) | `targeting.publisher_platforms`, `targeting.facebook_positions`, `targeting.instagram_positions` | CPA | 50 |
| `lance` | conjunto | `adsets_separados` (obrigatório) | `bid_strategy`, `bid_amount` | CPA + variação dia a dia | 50 |
| `estrutura` | campanha | `campanhas_separadas` (obrigatório) | `smart_promotion_type` (Advantage+) ou `objective` + `buying_type` | CPA + volume | 50 (janela de 14 dias) |
| `cta` | anúncio | `ads_mesmo_adset` (preferido) ou `adsets_separados` | `creative.object_story_spec.link_data.call_to_action.type` | CTR + taxa de conversão do anúncio | 50 |

**Regra de modelo:**
- `ads_mesmo_adset` só vale para variar algo dentro do criativo (headline, texto, CTA, imagem). Público define o leilão e exige conjunto próprio.
- `adsets_separados` é o padrão para qualquer outra dimensão.
- `campanhas_separadas` só para `estrutura` (Advantage+ é propriedade da campanha).

---

## Inputs comuns (toda dimensão)

| Input | Padrão | Descrição |
|---|---|---|
| `dimensao` | obrigatório | Uma das 8 acima |
| `campaign_id` ou `adset_id` | obrigatório | Molde (escolhido por nome ou lista) |
| `orcamento_diario` | obrigatório | Igual nos N lados |
| `hipotese` | obrigatório | "X performa Y% melhor que Z porque ___" |
| `produto_slug` | do `.ativo` | Entra no nome do teste |
| `janela_dias` | 7 (14 em `estrutura`) | Janela mínima até a leitura |
| `n_variacoes` | 2 (3 só em `headline` e `cta`) | Mais que isso dilui o orçamento |

## Inputs por dimensão

### `criativo`
| Input | Obrigatório | Descrição |
|---|---|---|
| `criativo_a` | sim | Pelo "Helper: escolha de criativos" abaixo. Nunca pedir hash ou ID |
| `criativo_b` | sim | Idem |
| `headline`, `texto_principal`, `cta` | iguais nos 2 | Para isolar o criativo |

Aceita `tipo_mandala_a` e `tipo_mandala_b` (nome do tipo, conforme `.claude/skills/mandala-de-anuncios/SKILL.md`) para registrar qual ângulo da Mandala está em teste. A skill só registra; o criativo vem pronto. Se o aluno não tiver o criativo B, encaminhar para `/criativo-estatico`, `/copy-anuncio` ou `/mandala-de-anuncios` (vídeo: `/video-heygen`, `/video-remotion`, `/video-editar`) e voltar com ele.

### `headline`
| Input | Obrigatório | Descrição |
|---|---|---|
| `headlines` | 2 a 3 | Textos (até 40 caracteres no Feed) |
| `criativo_id` | sim | Igual nos N anúncios, pelo Helper |
| `texto_principal`, `cta` | iguais | |

A skill pode propor 3 headlines em Light Copy a partir do resumo do produto (Quadro, Urgências Ocultas, Decorados), cada uma com 1 elemento literário diferente (ex: especificidade, contraste temporal, pergunta implícita). **Antes de mostrar**, aplicar a "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md (Manual da Copy em `.claude/skills/revisora/references/manual-copy.md` + skill `revisora`), sem mencionar a revisão. O aluno aprova ou edita. Para mais variações, `/copy-anuncio`.

### `audiencia`
| Input | Obrigatório | Descrição |
|---|---|---|
| `audiencia_a` | sim | Público personalizado ou semelhante já existente (nome), base salva pela `/trafego-publicos` ou interesses. Interesses só pelo "Helper: interesses" abaixo. **Nunca chutar termos** sem conferir na Meta |
| `audiencia_b` | sim | Idem |
| O resto (criativo, headline, texto, posicionamento, lance, idade, gênero) | igual | |

Pares com sentido VTSD: público quente vs frio, Intermediário vs Avançado (bases por nível), semelhante de compradores vs Iniciante.

### `faixa_etaria`
| Input | Obrigatório | Descrição |
|---|---|---|
| `idade_min_a`, `idade_max_a` | sim | Faixa A (ex: 25-34) |
| `idade_min_b`, `idade_max_b` | sim | Faixa B (ex: 35-44) |
| O resto | igual | |

### `posicionamento`
| Input | Obrigatório | Descrição |
|---|---|---|
| `posicionamento_a` | sim | `feed_only`, `reels_only`, `stories_only` ou `advantage_plus` |
| `posicionamento_b` | sim | Idem |
| O resto | igual | |

| Atalho | publisher_platforms | facebook_positions | instagram_positions |
|---|---|---|---|
| `feed_only` | `[facebook, instagram]` | `[feed]` | `[stream]` |
| `reels_only` | `[facebook, instagram]` | `[facebook_reels]` | `[reels]` |
| `stories_only` | `[facebook, instagram]` | `[facebook_stories]` | `[story]` |
| `advantage_plus` | `[facebook, instagram, audience_network, messenger]` | (vazio) | (vazio) |

### `lance`
| Input | Obrigatório | Descrição |
|---|---|---|
| `bid_strategy_a` | `LOWEST_COST_WITHOUT_CAP` (padrão) | Estratégia A |
| `bid_strategy_b` | `COST_CAP` ou `LOWEST_COST_WITH_BID_CAP` | Estratégia B |
| `valor_limite` | obrigatório se B tem limite | Em reais (a skill converte para centavos no `bid_amount`) |
| O resto | igual | |

### `estrutura`
| Input | Obrigatório | Descrição |
|---|---|---|
| `estrutura_a` | `MANUAL_ABO` (padrão) | Estrutura da campanha A |
| `estrutura_b` | `ADVANTAGE_PLUS_SHOPPING` (padrão) | Estrutura da campanha B |
| `criativos` | mínimo 4 se B é Advantage+ | O Advantage+ precisa de vários criativos |
| `objective` | `OUTCOME_SALES` ou `OUTCOME_LEADS` | Igual nas 2 |
| `pixel`, `evento_otimizado` | iguais | |

### `cta`
| Input | Obrigatório | Descrição |
|---|---|---|
| `cta_a` | sim | Ex: `LEARN_MORE` |
| `cta_b` | sim | Ex: `SHOP_NOW` |
| `cta_c` | opcional | Ex: `SIGN_UP` (máximo 3) |
| `criativo_id` | sim | Igual nos N anúncios, pelo Helper |
| `headline`, `texto_principal` | iguais | Para isolar o CTA |
| `link_destino` | igual | Mesma URL final |

CTAs mais usados em infoproduto:

| Código | Texto exibido | Quando usar |
|---|---|---|
| `LEARN_MORE` | "Saiba mais" | Topo de funil, descoberta |
| `SHOP_NOW` | "Comprar agora" | Fundo de funil, oferta direta |
| `SIGN_UP` | "Cadastre-se" | Captura de lead em lançamento |
| `GET_OFFER` | "Obter oferta" | Promoção ativa, escassez |
| `SUBSCRIBE` | "Assinar" | Recorrência |
| `BOOK_TRAVEL` | "Reservar" | Eventos, agendamento |
| `DOWNLOAD` | "Baixar" | Isca digital (e-book, planilha) |
| `WATCH_MORE` | "Assistir mais" | VSL, conteúdo em vídeo |
| `CONTACT_US` | "Fale conosco" | High ticket, qualificação |

A skill recusa CTA incompatível com o objetivo (ex: `BOOK_TRAVEL` em `OUTCOME_SALES` sem catálogo).

### Helper: escolha de criativos (para `criativo`, `headline`, `cta`)

O aluno **nunca digita hash de imagem nem ID de vídeo**. Sempre por camadas, **uma pergunta por mensagem**.

**Sub-passo 1. Como passar o criativo?**

```
Como você quer me passar o criativo {A | B | único}?

1. Da biblioteca (eu busco e você escolhe pelo nome), padrão
2. Arquivo do computador (você me passa o caminho)
3. Já tenho o código do criativo (cola direto)

Digite o número (Enter para usar 1):
```

**Sub-passo 2, se (1): período**

```
Quando esse criativo foi subido?

1. Últimos 7 dias
2. Últimos 30 dias (padrão)
3. Mais antigo, ou não sei (lista dos últimos 90 dias)

Digite o número (Enter para usar 2):
```

**Sub-passo 3, se (1): listagem com filtros**

- **MCP:** `ads_get_ad_images` (imagens) e `ads_get_ad_videos` (vídeos).
- **App:** `GET /act_<id>/adimages?fields=name,hash,created_time&limit=50` e `GET -g /act_<id>/advideos?fields=id,title,created_time,thumbnails{uri}&limit=50`.

Filtros (sem perguntar):
- `created_time` dentro do período escolhido.
- **Esconder ruído:** nomes começando com `Auto_Cropped`, `untitled`, contendo `(crop)`, vazios ou só espaço (são variações automáticas da Meta para outros formatos).
- Até 15 itens por tipo. Vídeos primeiro, imagens depois.
- Mais de 15 com nome válido: os 15 mais recentes + "tem mais N, quer filtrar por palavra?".

**Sub-passo 4, se (1): apresentação**

```
🎬 Vídeos com nome (últimos {N} dias)
[V1] 2026-05-07  AD - Vídeo de depoimento da aluna
                 id: <video_id>
[V2] 2026-04-14  [AD] [REELS] - os 3 erros de quem começa
                 id: <video_id>
...

🖼️ Imagens com nome (últimos {N} dias)
[I1] 2026-05-07  [AD-05] - Antes e depois feed.png
                 hash: <hash_da_imagem>
[I2] 2026-05-07  [AD-03] - Cronograma feed.png
                 hash: <hash_da_imagem>
...

(Escondi {N} variações automáticas da Meta. Para ver, peça "mostra os ocultos")

Qual é o criativo {A | B | único}? Me passe o código (ex: V2 ou I1):
```

- Mostrar o ID (vídeo) ou o hash (imagem) recuado abaixo do nome, para o aluno conferir no Gerenciador ou colar direto.
- Guardar o mapa `código → id/hash`. Aceitar também o ID ou hash colado.

**Sub-passo 5, se (1) e lista grande: filtro por palavra**

"filtra por X" ou "tem algum com X no nome": refazer a listagem com filtro (sem diferenciar maiúsculas) e mostrar de novo.

**Sub-passo 6, se (2): arquivo do computador**

- **App:**
  - O aluno passa o caminho. Tipo pela extensão: `.mp4`, `.mov`, `.webm` = vídeo; `.jpg`, `.jpeg`, `.png`, `.gif` = imagem.
  - Imagem: `POST /act_<id>/adimages` com o arquivo em multipart (ex: `-F "filename=@/caminho/imagem.png"`). Guardar o `hash` devolvido.
  - Vídeo: **sempre no host de vídeo** `https://graph-video.facebook.com/v25.0/act_<id>/advideos` com `-F "source=@/caminho/video.mp4" -F "name=<nome>"`. No host padrão, vídeos grandes devolvem **HTTP 413**. Usar `-w "\nHTTP_CODE:%{http_code}\n"` para não perder o erro de tamanho.
  - **Vídeo de anúncio exige miniatura.** Sem ela, o anúncio falha com erro `100` / subcode `1443226` ("Your ad needs a video thumbnail"). Depois do upload: `GET -g /<video_id>?fields=status,thumbnails{uri,is_preferred}`, esperar `status.video_status = "ready"`, pegar a miniatura com `is_preferred: true` e passar a `uri` como `image_url` no `video_data` do criativo.
  - O upload entra no lote do bloco 🛡️ do teste. Confirmar: "Subi '{nome do arquivo}'. Vou usar como criativo {A | B | único}."
- **MCP (o conector não sobe arquivo):**
  - **Imagem:** se estiver numa URL pública, usar direto no criativo (`ads_create_creative` com `image_url`). Se não, passo manual guiado:
    ```
    📋 Gerenciador de Anúncios → menu "Mídia" (ou "Biblioteca de mídia" da conta)
    📋 Clique em "Carregar" e envie "{nome do arquivo}"
    Me avise com "feito" que eu acho a imagem na biblioteca.
    ```
    Depois, listar com `ads_get_ad_images` e seguir.
  - **Vídeo novo:** sempre pelo passo manual guiado (mesma biblioteca de mídia, "Carregar vídeo"). Depois, `ads_get_ad_videos`. Vídeo já postado na Página também serve pelo ID.
  - A miniatura obrigatória vale igual: usar a miniatura do vídeo da biblioteca como `image_url` no criativo.

**Sub-passo 7, se (3): código direto**

- Hash (32 caracteres) ou ID de vídeo (16 dígitos).
- Conferir pela leitura da biblioteca (MCP) ou por `GET` (App).
- "Achei: '{nome}'. É esse?"

**Para `criativo`:** rodar o Helper **duas vezes** (A, depois B), nunca na mesma mensagem.

**Aviso na listagem:** se houver pares FEED e REELS do mesmo criativo (ex: `[AD] [FEED] X` e `[AD] [REELS] X`), avisar: "você tem vídeos em par FEED e REELS. Para testar formato, a opção [5] (posicionamento) é melhor. Para A/B de criativo, escolha 2 criativos diferentes no mesmo formato."

### Helper: interesses (para `audiencia`)

> **O Helper canônico** de interesses do Severino fica em [`trafego-publicos/sub-skills/bases-niveis.md`](../../trafego-publicos/sub-skills/bases-niveis.md), seção "Helper canônico: interesses conferidos na Meta". A versão abaixo é a variação por âncoras para A/B de audiência. Se houver divergência, vale a da `bases-niveis.md`.

> ⚠️ **No MCP não existe busca de interesse.** Preferir públicos e semelhantes que já existem (pelo nome, sem lacuna) ou as bases salvas pela `/trafego-publicos`. Se o aluno insistir em interesses, seguir o passo manual guiado da `bases-niveis.md` (o aluno confere no Gerenciador) e, como a segmentação nova não pode ser aplicada pelo conector sem a segmentação completa, montar os conjuntos pela duplicação guiada. Nunca montar `/search` no MCP.

**Vale quando:** o aluno escolheu A/B de `audiencia` e quer compor por interesses.

**Por quê:** chutar termos em português ("Copywriting", "Negócio online") e conferir um a um rende muitos vazios: a Meta tem catálogo fixo. O caminho mais certeiro é:
1. Pegar 1 ou 2 **âncoras** (marcas, plataformas, figuras que existem no catálogo) da página de vendas do produto.
2. Pedir à Meta as **sugestões relacionadas** dessas âncoras por `/search?type=adinterestsuggestion`, que só devolve interesses que existem.

**Sub-passo 1. Página de vendas**

```
Para montar interesses que existem de verdade na Meta, preciso ler a página de vendas
do produto e tirar 1 ou 2 marcas ou plataformas como ponto de partida.

Qual o link da página de vendas?
(ex: https://meusite.com/curso-x)
```

- Tentar primeiro achar no molde: `creative.object_story_spec.link_data.link` ou `asset_feed_spec.link_urls[0].website_url`. Achou: "Achei o link '{url}' no molde. Uso esse?".
- Sem link no molde (anúncio de vídeo sem link), perguntar como acima.

**Sub-passo 2. Ler a página e achar as âncoras**

- Ler a página (WebFetch, ou a página do Severino em `meus-produtos/{ativo}/entregas/paginas/` se for a mesma).
- Procurar:
  - **Plataformas de infoproduto no Brasil:** Hotmart, Eduzz, Kiwify, Cakto, Monetizze, Edools, Pepper, Doppus.
  - **Plataformas globais:** Udemy, Coursera, Teachable, Kajabi, ClickFunnels.
  - **Marcas e figuras do nicho citadas** (concorrentes, referências, métodos com nome próprio). Os concorrentes da `## Pesquisa de mercado (síntese)` do resumo também servem.
- Mostrar de 3 a 5 âncoras numeradas; o aluno confirma ou edita.

**Sub-passo 3. Conferir as âncoras (App)**

```
GET /search?type=adinterest&q=<ancora>&locale=pt_BR&limit=3
```

- Resultado com tamanho razoável (100 mil ou mais para infoproduto no Brasil): âncora aceita, guardar `id` e `name`.
- Vazio: descartar e tentar a próxima.
- "Âncoras conferidas: {Hotmart, Eduzz}".

**Sub-passo 4. Pacotes de interesses**

| Pacote | Âncoras típicas | Tamanho do pacote |
|---|---|---|
| **A, amplo** | termos gerais do nicho ("Empreendedorismo", "Marketing", "Educação") | 8 a 15 interesses, 5 milhões ou mais cada |
| **B, intermediário** | plataformas e ferramentas (Hotmart, Eduzz, Kiwify) | 8 a 15 interesses, de 500 mil a 5 milhões |
| **C, cirúrgico** | produtos e figuras do nicho | 5 a 10 interesses, de 50 mil a 500 mil |

Para cada pacote:
```
GET /search?type=adinterestsuggestion&interest_list=["<ancora1>","<ancora2>"]&locale=pt_BR&limit=25
```

Devolve `[{id, name, audience_size_lower_bound, audience_size_upper_bound, path, topic}]`, só com interesses que existem.

**Sub-passo 5. Mostrar ao aluno (uma mensagem por pacote)**

```
📦 Pacote {A | B | C}: {amplo | intermediário | cirúrgico}
   Âncoras: {Hotmart, Eduzz}

[1]  Marketing de afiliados        ~10 milhões     id <id>
[2]  Empreendedorismo              ~715 mil        id <id>
[3]  Marketing digital             ~149 milhões    id <id>
...

Escolha de 3 a 6 interesses (ex: "1, 2, 5"):
```

O público de cada pacote é a **união** dos escolhidos.

**Sub-passo 6. Os 2 pacotes do teste**

"Quer testar o pacote A contra o C, A contra B, ou B contra C?" Rodar o sub-passo 5 para os 2 escolhidos, **um por mensagem**. Resultado: `audiencia_a` = união do pacote X; `audiencia_b` = união do pacote Y.

**Se a leitura da página falhar:**

```
Não consegui ler a página de vendas. Me passe 1 ou 2 marcas ou plataformas que
aparecem no seu produto ou que o seu público provavelmente segue.

(ex: "Hotmart, Eduzz" para infoproduto; "Smart Fit, Gympass" para fitness)
```

**Proibido neste Helper:**
- Chutar termos em português e oferecer sem conferir.
- Mostrar interesse com tamanho zero ou ausente (código antigo sem entrega).
- Misturar pacotes na mesma mensagem.

---

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**.

A coleta parte de uma **campanha molde**: o aluno escolhe uma campanha existente, a skill pega dela o que precisa (criativo, público, posicionamento, lance) e só pergunta o **valor novo da dimensão**, o orçamento e a hipótese. O aluno nunca digita ID.

### Ordem fixa

1. **Campanha molde.** "Qual campanha vai servir de molde? (digite o nome, completo ou em parte, ou peça para eu listar)":
   - **(a) Nome:** listar campanhas (MCP `ads_get_ad_entities`; App `GET -g /act_<id>/campaigns?fields=name,status,effective_status,insights.date_preset(last_7d){spend}`) e procurar o trecho, sem diferenciar maiúsculas. 1 resultado: "Achei: '{nome}'. É essa?". Vários: lista numerada. Nenhum: oferecer listar todas.
   - **(b) Listar:** campanhas ativas e pausadas dos últimos 90 dias, com nome, status e gasto de 7 dias.
   - **(c) ID direto:** conferir pela leitura e confirmar.

   **Bloqueio:** conta sem nenhuma campanha: "Você ainda não tem campanha nessa conta. Antes do A/B, precisa da primeira para servir de molde. Te levo para `/trafego-criar-campanha`." Encerrar.

2. **Escopo do teste.** Sempre (mesmo com 1 conjunto, a opção 2 vale como "campanha contra campanha"):
   ```
   Como você quer testar essa dimensão?

   1. Num conjunto da campanha (teste isolado num público: 2 conjuntos novos)
   2. Na campanha inteira (copio a estrutura toda para cada variação: 2 campanhas novas)

   Sugestão: opção 2 quando a campanha é CBO com vários públicos que se completam
   (quente, morno, frio); opção 1 quando você quer isolar a dimensão num público só.

   Digite o número:
   ```

   Define o modelo:
   - **Escopo 1 (1 conjunto):** `adsets_separados`, 2 conjuntos novos. Segue para os passos 3 e 4.
   - **Escopo 2 (campanha inteira):** `campanhas_separadas`, 2 campanhas novas, cada uma com **todos** os conjuntos do molde (mesmo público e criativo) e o valor novo da dimensão em todos. **Pula os passos 3 e 4.**
     - ⚠️ **NÃO usar `POST /<campaign_id>/copies` com `deep_copy=true`**: estoura o limite de menos de 3 objetos (1885194) e quebra na revalidação do criativo (3858504, 2446347). Seguir a seção "Lições de campo" no topo: no App, ler e recriar; no MCP, campanha casca e conjuntos copiados um a um por `source_adset_id`, e duplicação guiada se falhar.

3. **Conjunto base.** *Só no escopo 1.* Campanha com mais de 1 conjunto ativo: lista numerada com nome, CPA de 7 dias e gasto de 7 dias. Com 1 conjunto: usar direto.

4. **Onde criar os conjuntos do teste.** *Só no escopo 1.* Padrão 2:
   ```
   Onde coloco os 2 conjuntos novos do teste?

   1. Dentro da campanha molde (viram irmãos dos que já estão lá)
   2. Numa campanha nova [WS-AB] só para o teste (mais limpo, recomendado)

   Digite o número (Enter para usar 2):
   ```
   (1): os conjuntos novos entram na campanha do molde.
   (2): criar campanha nova repetindo objetivo, pixel e categoria especial do molde, com nome `[WS-AB] {dimensao}-{slug}`. Os 2 conjuntos vão para ela.

5. **Confirmar o que vem do molde:**
   - Escopo 1: "Vou aproveitar do conjunto '{nome}': criativo, público, posicionamento e lance. Vou mudar só **{dimensão}**. Confirma?".
   - Escopo 2: "Vou copiar a campanha '{nome}' inteira ({N} conjuntos) em 2 campanhas novas, com a nova **{dimensão}** em todos os conjuntos de cada uma. Confirma?".

   Sim ou não. Se não, oferecer refazer a escolha.

6. **Valor novo da dimensão**, na ordem de "Inputs por dimensão" (ex: `faixa_etaria`: "Qual a faixa A?" e depois "Qual a faixa B?", uma por mensagem).

7. **Orçamento diário** (R$/dia, igual nos N lados).
   - Escopo 1: por conjunto. Sugerir o orçamento do conjunto molde.
   - Escopo 2: por campanha. Sugerir o orçamento total do molde (`daily_budget` da campanha em CBO, ou a soma dos conjuntos em ABO).

8. **Hipótese** ("X performa Y% melhor que Z porque ___").

9. **Número de variações**, só em `headline` e `cta` (aceita 3). Nas outras, 2.

10. **Janela**, só se o aluno quiser mudar o padrão (7 dias, ou 14 em `estrutura`).

**Proibido:**
- Pedir `creative_id`, ID de público, `targeting` ou qualquer ID ao aluno. Sempre a partir do molde.
- Listar 3 ou mais perguntas pendentes de uma vez.
- Misturar pergunta principal com sub-opção na mesma mensagem.
- Pular para o resumo sem os passos que se aplicam (1, 2, 5 a 8 sempre; 3 e 4 só no escopo 1).

---

## Aviso de viés do teste paralelo (só criativo, headline e CTA)

**Quando:** depois da coleta e antes do resumo, só se `dimensao` for `criativo`, `headline` ou `cta`.

**Por quê:** nessas dimensões, o modelo paralelo (o que a skill monta) tem viés conhecido: a Meta começa distribuindo igual entre os anúncios e, em 24 a 48h, costuma favorecer um e "matar" o outro antes de o teste ter significância. Para teste 100% limpo, o caminho é o teste A/B oficial da Meta.

```
⚠️ Aviso sobre o teste paralelo

Você está testando {criativo | headline | CTA}. Nesse tipo de teste, o modelo
paralelo (o que eu monto) tem um problema conhecido: a Meta começa distribuindo
igual entre os anúncios e, em 24 a 48h, costuma favorecer um e deixar o outro
quase sem entrega antes de o teste dar resultado.

Para um teste 100% limpo, existe o teste A/B oficial da Meta, que divide o
público de forma garantida (ninguém vê os dois lados).

Como quer seguir?

1. Seguir com o teste paralelo (eu monto normalmente, ciente do viés)
2. {MCP:} Criar o teste A/B oficial da Meta por aqui
   {App:} Fazer o teste A/B oficial no Gerenciador (te passo o passo a passo)
3. Cancelar

Digite o número:
```

**Comportamento:**
- **(1):** seguir para "Montagem" + resumo + bloco 🛡️. O viés fica registrado em "Observações" do arquivo de hipótese.
- **(2), MCP:** conferir a elegibilidade com `ads_experiment_check_eligibility`; se a campanha puder, montar o teste com `ads_experiment_abtest_create_test` (parâmetros pelo schema da tool, sem inventar), com resumo e bloco 🛡️ como qualquer escrita. Registrar com `modelo: ab_oficial_meta`; a leitura do 7º dia usa `ads_experiment_abtest_get_test`. Se não for elegível, explicar o motivo devolvido e oferecer a opção 1.
- **(2), App:** encerrar sem criar nada e mostrar:
  ```
  Para criar o teste A/B oficial no Gerenciador:
  1. Abra business.facebook.com → Gerenciador de Anúncios
  2. Na barra de ferramentas da tabela, clique em "Teste A/B"
  3. Escolha a campanha de origem (o seu molde: '{nome}')
  4. Escolha o que comparar ({criativo | headline | CTA}) e avance
  5. Crie as variações, defina a janela (recomendo {janela_dias} dias) e publique

  A Meta calcula a significância sozinha. Resultado em cerca de {janela_dias} dias.
  Depois, rode /trafego-testes opção [11] que eu registro o aprendizado.
  ```

**Quando NÃO mostrar:** `faixa_etaria`, `audiencia`, `posicionamento`, `lance`, `estrutura` (viés baixo ou inexistente; o aviso seria ruído). Mesmo assim, o teste A/B oficial pode ser oferecido se o aluno pedir "divisão de público garantida".

---

## Resumo em linguagem natural (obrigatório, antes do bloco 🛡️)

```
📋 Antes de eu mexer na conta, um resumo do plano:

O que vou criar:
  {N} {conjuntos | campanhas} novos, PAUSADOS, comparando {dimensão em português}
  de {N} jeitos.

Variação A: {descrição curta, sem termo técnico}
Variação B: {descrição curta, sem termo técnico}
{Variação C, se houver}

Onde vai entrar:
  {Escopo 1, no molde}: "Dentro da sua campanha '{nome}' (viram irmãos dos {N}
                         conjuntos que já estão lá)"
  {Escopo 1, campanha nova}: "Numa campanha nova '[WS-AB] {nome do teste}' só
                              para o teste"
  {Escopo 2}: "Em 2 campanhas novas, cada uma com a estrutura inteira da '{nome}'
               ({N} conjuntos em cada lado)"

O que fica igual nos {N} lados (para isolar o teste):
  - Criativo: {nome do criativo}
  - Público: {descrição, ex: "semelhante 1% de compradores"}
  - Posicionamento: {Reels, Feed ou automático}
  - Lance: {"automático" ou "com limite de R$ X"}
  (sem a linha da dimensão testada: ela aparece nas variações)

Orçamento: R$ {X}/dia por {lado | campanha}, total de R$ {Y}/dia.
Janela mínima: {7 | 14} dias com {50 | 30} ou mais conversões por lado.

{MCP, se a cópia falhar:} Se o conector não conseguir copiar, eu te passo o
passo a passo para duplicar no Gerenciador e confiro depois.

Sua hipótese:
  "{frase exata do aluno}"

Próximo passo:
  Com o seu ok, mostro a confirmação final. Com "sim", eu crio tudo PAUSADO.
  Você ativa quando quiser.

Está certo? (sim segue, não cancela aqui)
```

**Tradução obrigatória (zero jargão da Marketing API):**

| Campo técnico | Tradução |
|---|---|
| `bid_strategy: LOWEST_COST_WITHOUT_CAP` | "lance automático" |
| `bid_strategy: COST_CAP` | "lance com limite de custo de R$ X" |
| `optimization_goal: OFFSITE_CONVERSIONS` + `custom_event_type: PURCHASE` | "otimizando para compra" |
| `optimization_goal: LEAD_GENERATION` | "otimizando para lead" |
| `objective: OUTCOME_SALES` | "objetivo: vendas" |
| `objective: OUTCOME_LEADS` | "objetivo: leads" |
| `instagram_positions: [reels]` | "Reels no Instagram" |
| posicionamento automático | "posicionamento automático (todos os lugares)" |
| `targeting.age_min: 25, age_max: 34` | "público de 25 a 34 anos" |
| `image_hash` | nome do criativo (ex: "imagem 'AD-05, antes e depois'") |
| `video_id` | nome do vídeo |
| `custom_audiences: [<id>]` | nome do público (ex: "semelhante 1% de compradores") |
| `daily_budget: 5000` (centavos) | "R$ 50/dia" |
| `smart_promotion_type: AUTOMATED_SHOPPING_ADS` | "Advantage+" |

**Proibido no resumo:** IDs, hashes, códigos da API, nomes de campos, valores em centavos, inglês técnico.

**Depois:** "sim" → bloco 🛡️ com o Preview YAML. "Não" → "1. Quer ajustar algo, 2. cancelar de vez?".

---

## Montagem (algoritmo genérico)

```
1. Carregar inputs comuns e da dimensão
2. Formato do criativo do molde (só em criativo, headline, cta):
     - object_story_spec.video_data ou link_data → criativo simples (mantém)
     - asset_feed_spec com 1 vídeo ou 1 imagem → criativo simples (extrai)
     - asset_feed_spec com vários vídeos ou imagens, ou asset_customization_rules:
       → AVISO: "Sua campanha molde usa Advantage+ Creative com {N} criativos e
         ajuste por posicionamento. Para testar de forma limpa, vou simplificar nas
         cópias: cada anúncio com 1 criativo só, sem ajuste por posicionamento (a Meta
         recorta sozinha). Texto, título, descrição e CTA iguais ao molde. Confirma?"
       → Sim: pegar bodies[0].text, titles[0].text, descriptions[0].text,
         link_urls[0].website_url, call_to_action_types[0], page_id,
         instagram_user_id, url_tags e montar criativo simples
         (object_story_spec + video_data, ou link_data para imagem).
       → Não: oferecer (a) /trafego-criar-campanha do zero, ou (b) cancelar.
3. Nível = anúncio | conjunto | campanha (tabela)
4. Modelo:
     - escopo 2: campanhas_separadas
     - headline com até 3 variações: ads_mesmo_adset
     - criativo, se o aluno preferir: ads_mesmo_adset
     - estrutura: campanhas_separadas
     - resto: adsets_separados
5. Para cada variação (A, B, [C]):
     a. Nome: [WS-AB-{slug}] {dimensao}-{variacao_slug}-{produto_slug}
     b. Montar a entidade pelo padrão da seção "Lições de campo":
        - App: a partir da configuração LIDA por GET
          (conjunto com targeting_automation.advantage_audience; sem orçamento e lance
           sob CBO; promoted_object e attribution_spec iguais ao molde;
           anúncio apontando para creative_id existente)
        - MCP: cópia por source_adset_id / source_ad_id e variação por
          ads_update_entity; se falhar, duplicação guiada no Gerenciador
     c. Trocar SÓ os campos da coluna "Campo(s) que mudam"
     d. status: PAUSED
6. Conferir a simetria: orçamento igual, público igual (exceto audiencia/faixa_etaria),
   posicionamento igual (exceto posicionamento), lance igual (exceto lance)
7. Resumo em linguagem natural e "sim"
8. Bloco 🛡️ com o Preview YAML
9. "sim" (um lote)
10. Criar as N entidades em sequência (e, em campanhas_separadas, os conjuntos e anúncios de cada uma)
11. Gravar o arquivo de hipótese em meus-produtos/{ativo}/entregas/trafego/testes/{teste-slug}.md
    e a linha no INDEX.md da pasta
12. Marcar como desatualizado o cache do /trafego-insights
13. Devolver: entidades criadas, como desfazer (arquivar ou apagar no Gerenciador)
    e a data de leitura (hoje + janela)
```

---

## Endpoints por modelo (modo App; no MCP, a tool equivalente)

> **MCP:** `POST /act_<id>/adsets` → `ads_create_ad_set`; `POST /act_<id>/ads` → `ads_create_ad`; `POST /act_<id>/campaigns` → `ads_create_campaign`. Ao copiar do molde: `source_adset_id` / `source_ad_id` na tool de criação e a variação por `ads_update_entity`. Se falhar, duplicação guiada (seção "Lições de campo").

### `ads_mesmo_adset` (criativo, headline, CTA)

> Mesmo com o molde em Advantage+ Creative (`asset_feed_spec`), o criativo do teste é montado como `object_story_spec.video_data` (1 vídeo por anúncio) ou `object_story_spec.link_data` (1 imagem por anúncio). Senão, a Meta escolhe entre vários criativos em cada lado e o teste fica contaminado. O passo 2 da Montagem cuida disso.

```
POST /act_<id>/ads (xN)
{
  "name": "[WS-AB-{slug}] {dimensao}-{variacao}-{produto}",
  "adset_id": "<adset_id>",
  "creative": { ... },
  "status": "PAUSED"
}
```

### `adsets_separados` (criativo, audiencia, faixa_etaria, posicionamento, lance)

```
POST /act_<id>/adsets (xN)
{
  "name": "[WS-AB-{slug}] adset-{dimensao}-{variacao}-{produto}",
  "campaign_id": "<campaign_id>",
  "targeting": {
    "...": "igual ao molde, exceto a dimensão testada",
    "targeting_automation": { "advantage_audience": 0 }
  },
  "daily_budget": <orcamento_em_centavos>,
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "promoted_object": { "...": "o do molde, inteiro" },
  "attribution_spec": [ "...o do molde..." ],
  "bid_strategy": "...",
  "status": "PAUSED"
}
```

- `targeting_automation.advantage_audience` é **obrigatório** (senão, erro 1870227).
- Sob campanha CBO, **não mandar** `daily_budget` nem `bid_strategy` (vêm da campanha).
- `promoted_object` pode ter `custom_conversion_id` ou `pixel_rule`: copiar inteiro.

Anúncio: apontar para o criativo existente, **nunca** recriar ou copiar com `deep_copy` (erros 3858504 e 2446347):
```
POST /act_<id>/ads (1 por conjunto)
{ "name": "...", "adset_id": "<novo_adset>", "creative": { "creative_id": "<id_lido_do_molde>" }, "status": "PAUSED" }
```

### `campanhas_separadas` (estrutura)
```
POST /act_<id>/campaigns (xN)
{
  "name": "[WS-AB-{slug}] campaign-{estrutura}-{produto}",
  "objective": "OUTCOME_SALES",
  "buying_type": "AUCTION",
  "smart_promotion_type": "AUTOMATED_SHOPPING_ADS",
  "special_ad_categories": [],
  "status": "PAUSED"
}

POST /act_<id>/adsets ...   (conjuntos da variação manual; o Advantage+ cria os dele)
POST /act_<id>/ads ...
```

(`smart_promotion_type` só na campanha Advantage+.)

---

## Preview YAML (dentro do bloco 🛡️)

```yaml
sub_fluxo: ab_generico
modo: MCP_CONECTOR | APP
dimensao: criativo | headline | audiencia | faixa_etaria | posicionamento | lance | estrutura | cta
nome_teste: "[WS-AB] {dimensao}-{slug-A}-vs-{slug-B}-{produto}"
modelo: ads_mesmo_adset | adsets_separados | campanhas_separadas | ab_oficial_meta
nivel_criado: anuncio | conjunto | campanha
campanha_molde: "{nome}"
como_monta: ler_e_recriar (App) | copia_source_id (MCP) | duplicacao_guiada (MCP, plano B)

hipotese: "{X performa Y% melhor que Z porque ___}"

variacao_A:
  nome: "[WS-AB-A] {dimensao}-{slug}-{produto}"
  campos_variados:
    {campo_1}: {valor_A}
  orcamento_diario: 30 BRL
  tamanho_estimado: 2000000                   # só em audiencia e faixa_etaria

variacao_B:
  nome: "[WS-AB-B] {dimensao}-{slug}-{produto}"
  campos_variados:
    {campo_1}: {valor_B}
  orcamento_diario: 30 BRL

constantes:
  publico: ...                                # se a dimensão não for audiencia/faixa_etaria
  criativo: ...                               # se a dimensão não for criativo
  headline: ...                               # se a dimensão não for headline
  posicionamento: ...                         # se a dimensão não for posicionamento
  lance: ...                                  # se a dimensão não for lance
  otimizacao: compra
  pixel: "{nome do pixel}"

janela_minima_dias: 7                         # 14 em estrutura
conversoes_minimas_por_lado: 50               # 30 em high ticket
metrica_principal: CPA | CTR (headline)
data_leitura_em: 2026-05-12
status_inicial: PAUSED
```

O bloco 🛡️ diz: operação "criar teste A/B (N entidades pausadas)", reset de aprendizado "não (entidades novas)", reversível "sim: arquivar ou apagar no Gerenciador".

---

## Avisos por dimensão (mostrar antes do resumo)

### `criativo`
- Posicionamento Advantage+ mistura Feed, Reels e Stories. Para testar criativo numa superfície, fixar o posicionamento.
- Lance igual nos 2 lados, senão o teste vira criativo + lance.
- Orçamento suficiente para 50 conversões por lado em 7 dias.
- Molde com Advantage+ Creative (vários criativos): as cópias usam criativo simples (1 por anúncio), com confirmação do aluno (passo 2 da Montagem).
- Advantage+ Creative ≠ posicionamento Advantage+. O primeiro é do criativo; o segundo, do conjunto. Podem coexistir.

### `headline`
- Até 40 caracteres no Feed. Reels corta em cerca de 50 no celular.
- CTR é a métrica principal; o CPA confirma se a headline atrai a pessoa certa.
- Até 3 variações. Mais que isso dilui o orçamento.

### `audiencia`
- Público pequeno (menos de 50 mil) com orçamento alto satura rápido.
- Público enorme (mais de 50 milhões) vira aberto na prática.
- Não usar público Advantage+ num lado e segmentação manual no outro: vira teste de "expansão + público" misturados.

### `faixa_etaria`
- **Idade real do `targeting`, não do nome.** No App, ler pelo `GET ?fields=targeting`. No MCP, pedir ao aluno para conferir no Gerenciador.
- Faixas próximas (25-34 vs 30-39) se sobrepõem; o público efetivo fica menor.
- Faixas extremas (18-24 vs 55+) podem pedir criativos diferentes. Se o teste é só de idade, manter o criativo igual.

### `posicionamento`
- Vídeo 9:16 funciona em Reels e Stories; vídeo 1:1 fica cortado em Reels.
- Audience Network e Messenger baixam o CPA médio, mas convertem pior. Para Feed vs Reels limpo, tirar a Audience Network.

### `lance`
- Limite de lance muito baixo (menos de 70% do CPA alvo da trilha) faz o conjunto não entregar. A skill avisa.
- Limite de custo em low ticket costuma não compensar: o algoritmo precisa de margem.
- Mudar o lance de um conjunto existente reseta o aprendizado. Para teste limpo, conjuntos novos.

### `estrutura`
- Advantage+ precisa de no mínimo 4 anúncios variados. A skill bloqueia com menos.
- Advantage+ não permite exclusões finas (ex: excluir compradores). Funciona melhor em topo de funil novo.
- 7 dias podem não bastar para o Advantage+. Janela padrão: 14 dias.
- Mover orçamento entre as 2 estruturas reseta o aprendizado. Não desligar o "perdedor" cedo demais.

### `cta`
- A Graph API NÃO separa resultado por CTA. O teste é o único jeito de comparar.
- CTR é a métrica principal; a taxa de conversão do anúncio (compras ÷ cliques no link) confirma se o CTA atrai o clique certo. CTA agressivo (`SHOP_NOW`) pode subir o CTR e derrubar a conversão se o público não está pronto.
- Conferir objetivo × CTA antes de criar. `SHOP_NOW` em `OUTCOME_LEADS` desperdiça; `SIGN_UP` em `OUTCOME_SALES` confunde o algoritmo.
- Headline, texto, criativo e link iguais. Senão o teste vira CTA + outra coisa.
- O texto do botão é definido pela Meta (pelo idioma da pessoa). Só dá para escolher o código, não personalizar o texto.

---

## Depois de criar

```
✅ Teste A/B criado (PAUSADO):
   Variação A: {nível} "{nome_A}"
   Variação B: {nível} "{nome_B}"
   {variação C, se houver}

Hipótese salva em:
   meus-produtos/{ativo}/entregas/trafego/testes/{teste-slug}.md

Próximos passos:
1. Revise e ative as {N} entidades (no Gerenciador ou por aqui, com confirmação).
2. Aguarde {janela_dias} dias com {conversoes_minimas} ou mais conversões em cada lado.
3. Em {data_leitura}, rode /trafego-testes opção [11] "Ler resultado de teste":
   eu classifico, registro o aprendizado e sugiro o próximo teste.
   (Complemento: /trafego-analise, Criativos & Copy, para a leitura VTSD dos criativos.)

Para desfazer: as entidades já estão pausadas. Se quiser tirá-las da frente, eu
arquivo por aqui (com confirmação), ou você apaga pelo Gerenciador.
```

---

## Princípios desta sub-skill

1. **UMA dimensão por execução.** Pedido com 2 dimensões: recusar e oferecer 2 testes em sequência.
2. **Simetria obrigatória.** Conferir que o resto está igual antes do resumo.
3. **Modelo pela tabela.** Não deixar o aluno forçar `ads_mesmo_adset` em audiência ou posicionamento.
4. **Avisos da dimensão sempre** antes do resumo.
5. **Tudo nasce PAUSED.**
6. **Hipótese registrada** no arquivo antes de criar. Sem hipótese, sem teste.
7. **Métrica principal da dimensão** na leitura (CTR em `headline`, CPA no resto).
8. **Nome com `[WS-AB-{slug}]`** em toda entidade.
9. **Copy gerada passa pela auto-revisão** do CLAUDE.md antes de aparecer.
10. **Nunca `/copies` com `deep_copy`** em estrutura com mais de 2 objetos; no MCP, cópia por `source_*_id` e plano B guiado.
