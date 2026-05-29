# Sub-fluxo. A/B Genérico (parametrizado por dimensão)

Cria teste A/B disciplinado variando UMA dimensão entre criativo, headline, audiência (inclui faixa etária), posicionamento, lance, estrutura ou CTA. Mesma mecânica para todas. O que muda entre as dimensões: o nível em que o teste é criado (ad, adset, campanha), o campo Marketing API que é variado, a métrica primária de leitura e os avisos específicos.

## Quando esta sub-skill é usada

Toda opção de [1] a [8] do menu de `/trafego-testes` cai aqui, com `dimensao` diferente:

| Opção do menu | `dimensao` |
|---|---|
| [1] A/B de criativo | `criativo` |
| [2] A/B de headline | `headline` |
| [3] A/B de audiência | `audiencia` |
| [4] A/B de faixa etária | `faixa_etaria` (caso particular de `audiencia`) |
| [5] A/B de posicionamento | `posicionamento` |
| [6] A/B de lance | `lance` |
| [7] A/B de estrutura | `estrutura` |
| [8] A/B de CTA | `cta` |

As opções [9] (`duplicar-variando`) e [10] (`campanha-remarketing`) têm sub-skills próprias e não passam por aqui.

---

## Mapa das 8 dimensões (referência única)

| `dimensao` | Nível onde varia | Modelo recomendado | Campo(s) Marketing API que mudam | Métrica primária | Conversões mín./lado |
|---|---|---|---|---|---|
| `criativo` | ad | `adsets_separados` (preferido) ou `ads_mesmo_adset` | `creative.image_hash` ou `creative.video_id` | CPA | 50 (low/mid), 30 (high) |
| `headline` | ad | `ads_mesmo_adset` (preferido) ou `adsets_separados` | `creative.object_story_spec.link_data.name` | CTR (CPA secundário) | 50 |
| `audiencia` | adset | `adsets_separados` (obrigatório) | `targeting.custom_audiences`, `targeting.interests`, `targeting.behaviors`, `targeting.geo_locations` | CPA | 50 |
| `faixa_etaria` | adset | `adsets_separados` (obrigatório) | `targeting.age_min`, `targeting.age_max` (resto idêntico) | CPA | 50 |
| `posicionamento` | adset | `adsets_separados` (obrigatório) | `targeting.publisher_platforms`, `targeting.facebook_positions`, `targeting.instagram_positions` | CPA | 50 |
| `lance` | adset | `adsets_separados` (obrigatório) | `bid_strategy`, `bid_amount` | CPA + desvio padrão dia a dia | 50 |
| `estrutura` | campaign | `campanhas_separadas` (obrigatório) | `smart_promotion_type` (Adv+) ou `objective` + buying_type | CPA + volume | 50 (janela 14d em vez de 7d) |
| `cta` | ad | `ads_mesmo_adset` (preferido) ou `adsets_separados` | `creative.object_story_spec.link_data.call_to_action.type` | CTR + taxa_conversao_anuncio | 50 |

**Regra de modelo:**
- `ads_mesmo_adset` só vale para variar coisa dentro do criativo (headline, primary_text, CTA, image_hash). Audience define leilão e exige adset próprio.
- `adsets_separados` é o default para qualquer outra dimensão.
- `campanhas_separadas` só para `estrutura` (Advantage+ Shopping é uma propriedade da campanha, não do adset).

---

## Inputs comuns (toda dimensão)

| Input | Default | Descrição |
|---|---|---|
| `dimensao` | obrigatório | Uma das 8 da tabela acima |
| `campaign_id` ou `adset_id` | obrigatório | Onde criar (varia conforme dimensão e modelo) |
| `budget_diario` | obrigatório | Mesmo nos N lados |
| `hipotese` | obrigatório | "X performa Y% melhor que Z porque ___" |
| `produto_slug` | produto ativo | Lê de `meus-produtos/.ativo` |
| `janela_dias` | 7 (14 para `estrutura`) | Janela mínima até a leitura |
| `n_variacoes` | 2 (3 permitido só em `headline`) | Mais que isso dilui orçamento |

## Inputs específicos por dimensão

### `dimensao = criativo`
| Input | Obrigatório | Descrição |
|---|---|---|
| `criativo_a` | sim | Coletado via "Helper: Coleta de criativos" abaixo (lista, upload ou ID). Não pedir hash/id direto ao aluno |
| `criativo_b` | sim | Idem |
| `headline`, `primary_text`, `cta` | iguais nos 2 | Para isolar criativo |

Aceita `tipo_mandala_a` e `tipo_mandala_b` (1 a 18) para registrar qual ângulo da Mandala VTSD está sendo testado. Skill apenas registra; o criativo em si é produzido por `/copy-anuncio` + `/criativo-estatico` ou `/video-heygen`.

### `dimensao = headline`
| Input | Obrigatório | Descrição |
|---|---|---|
| `headlines` | 2 a 3 | Lista de strings (≤ 40 chars Feed) |
| `criativo_id` | sim | Mesmo nos N ads. Coletado via "Helper: Coleta de criativos" abaixo (lista, upload ou ID) |
| `primary_text`, `cta` | iguais | |

Receita Light Copy: a skill pode propor 3 variações aplicando 3 elementos literários distintos (especificidade, contraste temporal, questionamento implícito) a partir do Quadro do produto. Aluno aprova ou edita.

### `dimensao = audiencia`
| Input | Obrigatório | Descrição |
|---|---|---|
| `audiencia_a` | sim | ID de custom audience/lookalike OU spec de targeting. Quando o aluno escolhe **compor com interesses**, rodar o "Helper: Coleta de interesses via âncora" abaixo. **Nunca chutar termos em português** sem validar via Marketing API |
| `audiencia_b` | sim | Idem |
| Restantes (criativo, headline, primary_text, posicionamento, bid_strategy, idade, gênero) | iguais | |

Pares com semântica VTSD recomendada: HOT vs COLD, Intermediário vs Avançado (das bases por nível), Comprador (LAL) vs Iniciante.

### `dimensao = faixa_etaria` (caso particular de audiência)
| Input | Obrigatório | Descrição |
|---|---|---|
| `idade_min_a`, `idade_max_a` | sim | Faixa A (ex: 25-34) |
| `idade_min_b`, `idade_max_b` | sim | Faixa B (ex: 35-44) |
| Restantes (audience, criativo, headline, posicionamento, lance) | iguais | |

### `dimensao = posicionamento`
| Input | Obrigatório | Descrição |
|---|---|---|
| `posicionamento_a` | sim | Slug ou lista (`feed_only`, `reels_only`, `stories_only`, `advantage_plus`) |
| `posicionamento_b` | sim | Idem |
| Restantes | iguais | |

Combinações comuns:

| Slug | publisher_platforms | facebook_positions | instagram_positions |
|---|---|---|---|
| `feed_only` | `[facebook, instagram]` | `[feed]` | `[stream]` |
| `reels_only` | `[facebook, instagram]` | `[facebook_reels]` | `[reels]` |
| `stories_only` | `[facebook, instagram]` | `[facebook_stories]` | `[story]` |
| `advantage_plus` | `[facebook, instagram, audience_network, messenger]` | (vazio) | (vazio) |

### `dimensao = lance`
| Input | Obrigatório | Descrição |
|---|---|---|
| `bid_strategy_a` | `LOWEST_COST_WITHOUT_CAP` (default) | Estratégia A |
| `bid_strategy_b` | `COST_CAP` ou `LOWEST_COST_WITH_BID_CAP` | Estratégia B |
| `cap_value` | obrigatório se B usa cap | Valor em reais (skill converte para centavos no `bid_amount`) |
| Restantes | iguais | |

Estratégias Marketing API suportadas: `LOWEST_COST_WITHOUT_CAP`, `LOWEST_COST_WITH_BID_CAP`, `COST_CAP`.

### `dimensao = estrutura`
| Input | Obrigatório | Descrição |
|---|---|---|
| `estrutura_a` | `MANUAL_ABO` (default) | Estrutura da campanha A |
| `estrutura_b` | `ADVANTAGE_PLUS_SHOPPING` (default) | Estrutura da campanha B |
| `criativos_ids` | mín. 4 se B é Adv+ | Adv+ exige pool |
| `objective` | `OUTCOME_SALES` ou `OUTCOME_LEADS` | Mesmo nas 2 campanhas |
| `pixel_id`, `evento_otimizado` | mesmos | |

Estruturas suportadas: `MANUAL_ABO`, `MANUAL_CBO`, `ADVANTAGE_PLUS_SHOPPING`.

### `dimensao = cta`
| Input | Obrigatório | Descrição |
|---|---|---|
| `cta_a` | sim | Slug Marketing API do CTA da variação A (ex: `LEARN_MORE`) |
| `cta_b` | sim | Slug Marketing API do CTA da variação B (ex: `SHOP_NOW`) |
| `cta_c` | opcional | Terceira variação (ex: `SIGN_UP`). Limite: 3 variações |
| `criativo_id` | sim | Mesmo nos N ads. Coletado via "Helper: Coleta de criativos" abaixo |
| `headline`, `primary_text` | iguais | Para isolar o CTA como única variável |
| `link_destino` | mesmo | URL final idêntica nos N |

CTAs Marketing API mais usados em infoproduto:

| Slug API | Texto exibido | Quando usar |
|---|---|---|
| `LEARN_MORE` | "Saiba mais" | Topo de funil, descoberta |
| `SHOP_NOW` | "Compre agora" | Fundo de funil, oferta direta |
| `SIGN_UP` | "Cadastre-se" | Captura de lead em lançamento |
| `GET_OFFER` | "Aproveitar oferta" | Promoção ativa, escassez |
| `SUBSCRIBE` | "Assinar" | Recorrência |
| `BOOK_TRAVEL` | "Reservar" | Eventos, agendamento |
| `DOWNLOAD` | "Baixar" | Isca digital (e-book, planilha) |
| `WATCH_MORE` | "Assistir mais" | VSL, conteúdo em vídeo |
| `CONTACT_US` | "Fale conosco" | High ticket, qualificação |

A skill rejeita CTAs incompatíveis com o objetivo da campanha (ex: `BOOK_TRAVEL` em campanha `OUTCOME_SALES` sem catálogo).

### Helper: Coleta de criativos (para `criativo`, `headline`, `cta`)

Aluno **nunca digita image_hash ou video_id direto** — não conhece esses códigos. Sempre rodar este fluxo em camadas, **uma pergunta por mensagem**.

**Sub-passo 1: Como passar o criativo?**

```
Como você quer me passar o criativo {A|B|único}?

1. Lista (eu busco da sua biblioteca, você escolhe pelo nome) — default
2. Upload (você me dá o caminho de um arquivo local, eu subo pra biblioteca)
3. Já tenho o ID/hash (cola direto se já sabe)

Digite o número (Enter pra usar 1):
```

**Sub-passo 2 — se (1): Janela temporal**

```
Quando foi subido esse criativo?

1. Últimos 7 dias
2. Últimos 30 dias (default)
3. Mais antigo / não sei (lista últimos 90 dias)

Digite o número (Enter pra usar 2):
```

**Sub-passo 3 — se (1): Listagem com filtros automáticos**

Endpoints:
- `GET /act_<id>/adimages?fields=name,hash,created_time&limit=50`
- `GET /act_<id>/advideos?fields=id,title,created_time,thumbnails{uri}&limit=50`

Filtros aplicados (transparente pro aluno):
- `created_time >= now() - {7|30|90}d`
- **Esconder ruído**: itens com nome começando em `Auto_Cropped`, `untitled`, contendo `(crop)`, vazio ou só whitespace. São variantes auto-geradas pelo Meta pra diferentes aspect ratios — não interessam ao aluno.
- Limite de exibição: 15 itens por categoria. Vídeos primeiro, imagens depois.
- Se houver mais de 15 com nome válido: mostrar os 15 mais recentes + aviso "tem mais N itens, quer filtrar por palavra-chave?".

**Sub-passo 4 — se (1): Apresentação**

Formato fixo:

```
🎬 Vídeos com nome identificável (últimos {N} dias)
[V1] 2026-05-07  AD - Lançamento Q2 - Vídeo
                 id: 1234567890123456
[V2] 2026-04-14  [AD] [REELS] - exemplo nome real do criativo
                 id: 1234567890987654
...

🖼️ Imagens com nome identificável (últimos {N} dias)
[I1] 2026-05-07  [AD-05] - A mágica acontece feed.png
                 hash: c926036f61e8d16d788b4fc9105ba3f9
[I2] 2026-05-07  [AD-03] - Cronograma feed.png
                 hash: b305ff3782090c36787ceb33e9c6b39d
...

(Escondi {N} variantes auto-geradas pelo Meta — pra ver, peça "mostra os ocultos")

Qual é o criativo {A|B|único}? Me passa o código (ex: V2 ou I1):
```

- **Exibir id (vídeo) ou hash (imagem)** indentado abaixo do nome. Permite ao aluno conferir no Gerenciador, copiar pra usar fora da skill, ou colar direto no lugar do código curto.
- Manter o mapeamento `código → id/hash` internamente também — aluno escolhe pelo código curto (V1, I1) na maioria das vezes.
- Se aluno colar id/hash direto em vez do código, aceitar e validar.

**Sub-passo 5 — se (1) e lista grande: Filtro por palavra-chave (sob demanda)**

Se o aluno responde "filtra por X" ou "tem alguma com X no nome": re-roda a listagem aplicando filtro case-insensitive `name contains X` no client side e re-apresenta.

**Sub-passo 6 — se (2): Upload de arquivo local**

- Aluno passa caminho absoluto ou expandido (`~/Desktop/criativo-a.mp4`).
- Skill detecta tipo pela extensão: `.mp4`, `.mov`, `.webm` → vídeo; `.jpg`, `.jpeg`, `.png`, `.gif` → imagem.
- `POST /act_<id>/adimages` (multipart, campo `bytes` = base64) para imagem.
- `POST /act_<id>/advideos` (multipart, campo `source` = arquivo) para vídeo.
- Captura `hash` (imagem) ou `id` (vídeo) retornado.
- Confirma: "Subi '{nome do arquivo}'. Vou usar como criativo {A|B|único}."

**Sub-passo 7 — se (3): ID/hash direto**

- Aluno cola hash (32 chars hex) ou video_id (16 dígitos).
- Valida via `GET /<hash>?fields=name` ou `GET /<video_id>?fields=title,id`.
- Confirma: "Achei: '{nome}'. É esse?"

**Para dimensão = criativo:** rodar este Helper **duas vezes** (Criativo A, depois Criativo B), nunca na mesma mensagem.

**Avisos durante a listagem:**
- Se detectar pares FEED/REELS do mesmo criativo (ex: `[AD] [FEED] X` e `[AD] [REELS] X`), avisar no fim da listagem: "noto que você tem vídeos pareados FEED/REELS — pra testar formato, melhor opção [5] A/B de posicionamento. Pra A/B de criativo, escolha 2 criativos diferentes no mesmo formato."

### Helper: Coleta de interesses via âncora (para `audiencia`)

> **Aviso de canonicidade:** o Helper canônico do curso pra coleta de interesses do Meta vive em [`trafego-publicos/sub-skills/bases-niveis.md`](../../trafego-publicos/sub-skills/bases-niveis.md#helper-canônico-coleta-de-interesses-via-âncora-para-todo-o-curso) (seção "Helper canônico"). A versão abaixo é uma cópia simplificada pra A/B de audiência — se houver divergência, a de `bases-niveis.md` prevalece. Atualizações futuras de algoritmo (ex: novos endpoints, mudança de defaults) devem ser feitas lá primeiro.


**Aplica-se quando:** o aluno escolheu A/B de `audiencia` e quer compor com interesses (em vez de usar custom audiences ou lookalikes já existentes).

**Por que existe:** chutar termos em português ("Copywriting", "Negócio online", "Infoproduto") e validar um a um via `/search?type=adinterest&q=<termo>` gera muitos retornos vazios — o Meta tem catálogo fixo de interesses e nem todo termo em PT-BR existe lá. O caminho correto é:
1. Pegar 1-2 **âncoras** (marcas/plataformas/figuras que sabidamente existem no catálogo do Meta) extraídas da página de vendas do produto.
2. Pedir ao Meta as **sugestões relacionadas** dessas âncoras via `/search?type=adinterestsuggestion`. O Meta só devolve interesses que existem de verdade.

**Sub-passo 1: Obter a URL da página de vendas**

```
Pra montar um pool de interesses que realmente existem no Meta, preciso
ler a página de vendas do produto e extrair 1-2 marcas/plataformas
como âncora.

Qual o link da página de vendas?
(ex: https://meusite.com/curso-x)
```

- Tentar primeiro extrair automaticamente do molde: `creative.object_story_spec.link_data.link` OU `asset_feed_spec.link_urls[0].website_url`. Se achar, confirmar com aluno: "Achei o link '{url}' no molde. Uso esse?".
- Se molde não tem link (anúncio de vídeo sem link_data), pedir abertamente como acima.

**Sub-passo 2: WebFetch + identificação de âncoras candidatas**

- `WebFetch` na URL fornecida.
- Extrair menções a:
  - **Plataformas BR de infoproduto**: Hotmart, Eduzz, Kiwify, Cakto, Monetizze, Edools, Pepper, Doppus.
  - **Plataformas globais**: Udemy, Coursera, Teachable, Kajabi, ClickFunnels.
  - **Marcas/figuras do nicho citadas no texto** (concorrentes mencionados, gurus, métodos com nome próprio).
- Mostrar 3-5 âncoras candidatas em lista numerada, aluno confirma ou edita.

**Sub-passo 3: Validar âncoras no catálogo do Meta**

Para cada âncora confirmada:
```
GET /search?type=adinterest&q=<ancora>&locale=pt_BR&limit=3
```

- Se retornar match com `audience_size` razoável (≥ 100k para infoproduto BR): âncora validada, guardar `id` e `name`.
- Se retornar vazio: descartar e tentar próxima da lista.
- Mostrar ao aluno: "âncoras validadas: {Hotmart, Eduzz}".

**Sub-passo 4: Buscar interesses sugeridos por Pacote**

3 pacotes, cada um com âncoras diferentes:

| Pacote | Âncoras típicas | Tamanho de pool sugerido |
|---|---|---|
| **A — Broad** | termos genéricos do nicho ("Empreendedorismo", "Marketing", "Educação") | 8-15 interesses, audience size 5M+ cada |
| **B — Intermediário** | plataformas e ferramentas (Hotmart, Eduzz, Kiwify) | 8-15 interesses, audience size 500k-5M |
| **C — Cirúrgico** | produtos/figuras específicas do nicho (gurus, métodos famosos) | 5-10 interesses, audience size 50k-500k |

Para cada Pacote:
```
GET /search?type=adinterestsuggestion&interest_list=["<ancora1>","<ancora2>"]&locale=pt_BR&limit=25
```

Retorna `[{id, name, audience_size_lower_bound, audience_size_upper_bound, path, topic}]`. Apenas interesses que **existem no catálogo do Meta**.

**Sub-passo 5: Apresentar pool ao aluno**

Formato fixo para cada Pacote (uma mensagem por Pacote):

```
📦 Pacote {A|B|C} — {Broad|Intermediário|Cirúrgico}
   Âncoras usadas: {Hotmart, Eduzz}

[1]  Marketing de afiliados (marketing)     ~10M     id 6003713996153
[2]  Empreendedorismo                       ~715k    id 6003114185392
[3]  Marketing digital (marketing)          ~149M    id 6003127206524
[4]  Negócios e empreendedorismo            ~3M      id 6003402305839
...

Escolha de 3 a 6 interesses (ex: "1, 2, 5"):
```

- **Exibir id**: aluno pode copiar pra usar fora da skill ou conferir no Gerenciador.
- **Exibir audience_size aproximado**: ajuda o aluno a entender o tamanho do interesse.
- Aluno responde com lista de números. Skill compõe a audience do Pacote como **união** dos selecionados.

**Sub-passo 6: Repetir para cada Pacote escolhido pro teste**

- Pergunta: "Quer testar Pacote A vs Pacote C, A vs B, ou B vs C?"
- Roda o Sub-passo 5 para os 2 Pacotes escolhidos (uma mensagem por Pacote, **nunca os 2 na mesma**).
- Resultado: `audiencia_a = união dos interesses do Pacote X`, `audiencia_b = união dos interesses do Pacote Y`.

**Fallback quando WebFetch falha ou retorna vazio:**

```
Não consegui ler a página de vendas. Me passa diretamente 1-2 marcas/plataformas
que aparecem no seu produto ou que o público dele provavelmente já segue.

(ex: "Hotmart, Eduzz" para infoproduto; "Mundo Fit, Cia Athletica" para fitness)
```

**Proibido neste Helper:**
- **Nunca** chutar termos em português e validar 1 a 1 via `/search?type=adinterest`. Sempre passar pelo `adinterestsuggestion` com âncoras validadas.
- **Nunca** apresentar interesses que vieram com `audience_size = 0` ou ausente — são códigos legados sem entrega.
- **Nunca** misturar Pacotes na mesma mensagem (A + B + C juntos viola "1 pergunta por mensagem").

---

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Reforça a regra global do CLAUDE.md ("NUNCA fazer duas perguntas na mesma mensagem").

A coleta é centrada em **campanha molde**: o aluno escolhe uma campanha existente como referência, a skill extrai automaticamente o que precisa (criativo, audience, posicionamento, lance) e só pede ao aluno o **novo valor da dimensão variada** + budget + hipótese. Aluno nunca digita ID de criativo, audience ou adset.

### Ordem fixa

1. **Campanha molde.** Pergunta neutra: "Qual campanha vai servir de molde? (você pode digitar o nome — completo ou parcial — ou pedir pra eu listar)". Aceita 3 modos:
   - **(a) Nome (total ou parcial):** `GET /act_<id>/campaigns?fields=name,status,effective_status,insights.date_preset(last_7d){spend}` → match case-insensitive `contains` no nome. 1 match: confirma "Achei: '{nome}'. É essa?". Múltiplos: mostra apenas os matches em lista numerada. Zero: avisa e oferece listar todas.
   - **(b) Listar:** se aluno responde "lista", "não lembro", "me mostra", ou similar → mostra campanhas ACTIVE/PAUSED dos últimos 90d, numeradas, com nome + status + gasto 7d.
   - **(c) ID direto:** valida via `GET /<id>?fields=name` e confirma.

   **Bloqueio:** se a conta não tem nenhuma campanha (`data: []`), responder: "Você ainda não tem nenhuma campanha nessa conta. Antes de fazer teste A/B, precisa criar a primeira pra servir de molde. Te encaminho pra `/trafego-criar-campanha`." Encerrar a sub-skill.

2. **Escopo do teste.** Pergunta numerada (passo sempre presente, mesmo se a campanha molde tem 1 só adset — nesse caso a opção 2 ainda faz sentido como "campanha vs campanha"):
   ```
   Como você quer testar essa dimensão?

   1. Em UM conjunto da campanha (teste isolado em 1 audience: 2 conjuntos novos)
   2. Na CAMPANHA INTEIRA (clono toda a estrutura de conjuntos pra cada variação: 2 campanhas novas)

   Sugestão: opção 2 quando a campanha é CBO com vários públicos
   complementares (HOT/WARM/COLD), opção 1 quando você quer
   isolar a dimensão dentro de UMA audience só.

   Digite o número:
   ```

   Define o modelo de implementação:
   - **Escopo 1 (1 conjunto):** modelo `adsets_separados` → 2 adsets novos. Segue para passos 3 e 4.
   - **Escopo 2 (campanha inteira):** modelo `campanhas_separadas` → 2 campanhas novas, cada uma clonando TODOS os adsets ativos da molde (deep_copy via `POST /<campaign_id>/copies`) e aplicando o novo valor da dimensão em todos os adsets clonados. **Pula passos 3 e 4** (não existe escolha de adset base nem "onde colocar"; já está decidido). Vai direto pro passo 5.

3. **Conjunto base (adset).** *Só executar se escopo = 1.* Se a campanha tem >1 adset ativo: lista numerada com nome + CPA 7d + gasto 7d, aluno escolhe. Se tem 1 adset: usa direto sem perguntar.

4. **Onde criar os conjuntos do teste.** *Só executar se escopo = 1.* Pergunta numerada, default 2:
   ```
   Onde vou colocar os 2 conjuntos novos do teste?

   1. Dentro da campanha molde (os 2 novos viram irmãos dos existentes)
   2. Numa campanha nova [WS-AB] dedicada ao teste (mais limpo, recomendado)

   Digite o número (Enter pra usar 2):
   ```
   Se (1): os adsets novos entram na própria `campaign_id` do molde.
   Se (2): criar campanha nova clonando o objective + pixel + special_ad_categories da molde, com nome `[WS-AB] {dimensao}-{slug}`. Os 2 adsets novos vão lá.

5. **Confirmar o que será reaproveitado do molde.** Apresentar em texto natural:
   - Escopo 1: "Vou aproveitar do conjunto '{nome}' do molde: criativo, audience, posicionamento, lance. Vou mudar só **{dimensão}**. Confirma?".
   - Escopo 2: "Vou clonar a campanha '{nome}' inteira ({N} conjuntos) em 2 campanhas novas, aplicando a nova **{dimensão}** em todos os conjuntos de cada clone. Confirma?".

   Sim/não. Se não, oferece refazer escolha.

6. **Novo valor da dimensão variada**, na ordem da tabela "Inputs específicos por dimensão". Ex: se `faixa_etaria`, pergunta "Qual a faixa A?" e depois "Qual a faixa B?" (cada uma em 1 mensagem; o par "25-34" conta como 1 input porque vem em 1 resposta natural).

7. **`budget_diario`** (R$/dia, mesmo nos N lados).
   - Escopo 1: budget por adset. Sugerir como default o budget do adset molde.
   - Escopo 2: budget por campanha. Sugerir como default o budget total da campanha molde (`daily_budget` da campanha se CBO, ou soma dos adsets se ABO).

8. **`hipotese`** (frase: "X performa Y% melhor que Z porque ___").

9. **`n_variacoes`** apenas quando dimensão é `headline` ou `cta` (aceita 3). Nas demais, fixo em 2.

10. **`janela_dias`** apenas se o aluno pedir override do default (7d, ou 14d em `estrutura`).

**Proibido**:
- Pedir `creative_id`, `audience_id`, `targeting` ou qualquer ID Marketing API diretamente ao aluno. Sempre extrair do molde.
- Listar 3+ perguntas pendentes em formato "responda os 5".
- Misturar pergunta principal + sub-opção condicional na mesma mensagem (ex: "qual criativo? (a) ID, (b) tipo de audiência"). Faça **primeiro** a escolha, **depois** o detalhe.
- Pular pro Preview YAML sem ter passado pelos passos aplicáveis (1, 2, 5-8 sempre; 3 e 4 só se escopo = 1).

Só monte o Resumo em linguagem natural (etapa 7) e depois o Preview YAML (etapa 8 da Construção do payload abaixo) quando TODOS os inputs estiverem respondidos um a um.

---

## Aviso de viés do teste paralelo (apenas criativo/headline/cta)

**Quando exibir:** depois de coletar todos os inputs (passos 1-10 acima) e ANTES de montar o Preview YAML, somente se `dimensao` ∈ {`criativo`, `headline`, `cta`}.

**Por que existe:** nessas dimensões, o modelo paralelo (que essa skill usa) tem viés conhecido — o algoritmo do Meta começa distribuindo impressões igualmente entre os ads e em 24-48h costuma favorecer um e "matar" o outro antes do teste virar significativo. Pra teste 100% limpo, o caminho é o Experimento nativo do Meta. A skill não suporta Experimentos hoje (decisão de MVP), então o aviso transfere a escolha ao aluno.

**Texto exibido:**

```
⚠️ Aviso de viés do teste paralelo

Você está testando {criativo|headline|cta}. Nesse tipo de dimensão, o
modelo paralelo (o que essa skill faz) tem um problema conhecido: o
algoritmo do Meta começa distribuindo impressões igual entre os ads e,
em 24-48h, costuma favorecer um e "matar" o outro antes do teste virar
significativo.

Pra teste 100% limpo dessa dimensão, o caminho recomendado é o
Experimento nativo do Meta, direto no Gerenciador de Anúncios
(menu lateral > Testes A/B). A skill não suporta Experimentos hoje.

Como quer seguir?

1. Continuo com teste paralelo (skill cria normalmente, ciente do viés)
2. Cancelo aqui e faço pelo Gerenciador (te passo um mini-passo-a-passo)

Digite o número:
```

**Comportamento:**
- **Se (1):** segue normalmente para a "Construção do payload" + Preview YAML + gate 🛡️ padrão. O viés fica registrado no campo `observacoes` do arquivo de hipótese.
- **Se (2):** encerra a sub-skill sem criar nada e exibe:
  ```
  Pra criar Experimento no Gerenciador:
  1. Abra business.facebook.com → Gerenciador de Anúncios
  2. No menu superior, clique em "Testes A/B"
  3. "Começar" → "Teste padrão"
  4. Selecione a campanha de origem (sua molde: '{nome}')
  5. Escolha o que comparar ({criativo|headline|cta}) e clique "Próximo"
  6. Crie as variações, defina janela (recomendo {janela_dias}d) e clique "Revisar e publicar"

  Meta calcula significância automaticamente. Resultado em ~{janela_dias} dias.
  ```

**Quando NÃO exibir:** `dimensao` ∈ {`faixa_etaria`, `audiencia`, `posicionamento`, `lance`, `estrutura`}. Nessas, o viés do paralelo é baixo ou inexistente, então o aviso seria ruído.

---

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

**Quando exibir:** sempre, em toda execução. DEPOIS de coletar todos os inputs (passos 1-10 da seção "Padrão de coleta"), DEPOIS do "Aviso de viés do teste paralelo" (quando aplicável), e ANTES do Preview YAML da próxima seção.

**Por que existe:** o Preview YAML é técnico e cheio de campos da Marketing API (`bid_strategy`, `optimization_goal`, `targeting.age_min`, IDs longos). O aluno trava ao ver o bloco direto. Esse resumo traduz o plano pra português natural, garantindo que o aluno entenda **o que vai ser criado** antes de ver o detalhe técnico.

**Formato fixo:**

```
📋 Antes de eu mexer na conta, deixa eu te resumir o plano:

O que eu vou criar:
  {N} {conjuntos|campanhas} novos em PAUSED, comparando {dimensão em português}
  de {N} formas diferentes.

Variação A: {descrição curta em português, sem jargão}
Variação B: {descrição curta em português, sem jargão}
{Variação C, se houver}

Onde vai entrar:
  {Escopo 1, dentro da molde}: "Dentro da sua campanha '{nome}' (vão virar
                                 irmãos dos {N} conjuntos que já estão lá)"
  {Escopo 1, campanha nova}:    "Numa campanha nova '[WS-AB] {nome do teste}'
                                 dedicada só pro teste"
  {Escopo 2, campanha inteira}: "Em 2 campanhas novas, cada uma com a
                                 estrutura inteira de público da '{nome}'
                                 ({N} conjuntos clonados em cada lado)"

O que vai ser igual nos {N} lados (pra isolar o teste):
  - Criativo: {nome do criativo molde, sem hash/id}
  - Público: {descrição da audience em português, ex: "LAL 1% Compradores"}
  - Posicionamento: {Reels/Feed/Auto, em português}
  - Lance: {"automático" ou "manual com cap de R$ X"}
  (omitir a linha onde a dimensão É a variável testada — ela aparece nas Variações)

Budget: R$ {X}/dia por {lado|campanha}, total R$ {Y}/dia.
Janela mínima: {7|14} dias com {50|30}+ conversões por lado.

Sua hipótese:
  "{frase exata que o aluno escreveu, entre aspas}"

Próximo passo:
  Se você confirmar, eu monto o bloco técnico (YAML) e te mostro mais uma
  vez. Aí, com sim, eu efetivamente crio as entidades na sua conta — todas
  em PAUSED. Você ativa quando quiser.

Tá certo? (sim segue pro YAML, não cancela aqui)
```

**Regras de tradução obrigatórias** (zero jargão da Marketing API neste resumo):

| Campo técnico | Tradução pro resumo |
|---|---|
| `bid_strategy: LOWEST_COST_WITHOUT_CAP` | "lance automático" |
| `bid_strategy: COST_CAP` | "lance manual com cap de R$ X" |
| `optimization_goal: OFFSITE_CONVERSIONS` + `custom_event_type: PURCHASE` | "otimizando pra compra" |
| `optimization_goal: LEAD_GENERATION` | "otimizando pra lead" |
| `objective: OUTCOME_SALES` | "objetivo: vendas" |
| `objective: OUTCOME_LEADS` | "objetivo: leads" |
| `targeting.publisher_platforms: [facebook, instagram]` + `instagram_positions: [reels]` | "Reels no Instagram" |
| `targeting.publisher_platforms: automatic` | "posicionamento automático (todos os feeds)" |
| `targeting.age_min: 25, age_max: 34` | "público de 25 a 34 anos" |
| `image_hash: <32 chars>` | nome do criativo (ex: "imagem 'AD-05 - A mágica acontece'") |
| `video_id: <16 dígitos>` | nome do vídeo (ex: "vídeo 'REELS - não faltam pessoas com problemas'") |
| `custom_audiences: [<id>]` | nome da audience (ex: "LAL 1% Compradores") |
| `daily_budget: 5000` (centavos) | "R$ 50/dia" |
| `smart_promotion_type: AUTOMATED_SHOPPING_ADS` | "Advantage+ Shopping" |

**Proibido neste resumo:**
- Mostrar IDs, hashes, slugs de API ou nomes de campos.
- Mostrar valores em centavos (sempre converter pra reais).
- Usar inglês técnico (`adset`, `bidding`, `optimization goal`).
- Pular esse resumo pra ir direto pro Preview YAML.

**Comportamento depois do resumo:**
- **Aluno responde "sim" (ou variante: pode, manda, aprovo)** → segue pro Preview YAML da próxima seção.
- **Aluno responde "não" (ou variante: cancela, espera)** → perguntar: "1. Quer ajustar algo, 2. cancelar de vez?". Se ajustar, voltar ao passo da coleta correspondente ao que ele quer mudar. Se cancelar, encerrar sem criar nada.

---

## Construção do payload (algoritmo genérico)

```
1. Carregar inputs comuns + inputs específicos da dimensão
2. Detectar shape do creative do molde (apenas se dimensao ∈ {criativo, headline, cta}):
     - Se molde.creative.object_story_spec.video_data ou link_data existe → single creative (mantém shape, extrai direto)
     - Se molde.creative.asset_feed_spec existe com 1 video OU 1 imagem → single creative (extrai)
     - Se molde.creative.asset_feed_spec existe com N>1 videos/imagens OU asset_customization_rules:
       → AVISO ao aluno: "Sua campanha molde usa Advantage+ Creative com {N} criativos
         e customização por posicionamento. Pra testar criativo de forma limpa,
         vou simplificar nos clones: cada ad terá 1 criativo só, sem placement
         customization (Meta vai usar auto-cropping). A copy (body, title,
         description) e CTA vão idênticos ao molde. Confirma? (sim/não)"
       → Se sim: extrair primeiro bodies[0].text, titles[0].text, descriptions[0].text,
         link_urls[0].website_url, call_to_action_types[0], object_story_spec.page_id,
         object_story_spec.instagram_user_id, url_tags. Montar creative simplificado
         com object_story_spec + video_data (ou link_data pra imagem).
       → Se não: oferecer 2 saídas:
         (a) usar /trafego-criar-campanha pra subir do zero (sem molde)
         (b) cancelar
3. Determinar nivel = ad | adset | campaign (tabela acima)
4. Determinar modelo:
     - se escopo == 2 (campanha inteira): campanhas_separadas (override)
     - se dimensao == headline e n_variacoes ≤ 3: ads_mesmo_adset
     - se dimensao == criativo e aluno preferiu: ads_mesmo_adset
     - se dimensao == estrutura: campanhas_separadas
     - caso contrário: adsets_separados
5. Para cada variação (A, B, [C]):
     a. Montar nome: [WS-AB-{slug}] {dimensao}-{variacao_slug}-{produto_slug}
     b. Clonar template do nivel (ad/adset/campaign) com defaults idênticos
     c. Sobrescrever APENAS os campos da coluna "Campo(s) Marketing API que mudam" da tabela
     d. status: PAUSED
6. Validar simetria: budget igual nos N lados, audience igual (exceto se dimensao=audiencia/faixa_etaria), posicionamento igual (exceto se dimensao=posicionamento), lance igual (exceto se dimensao=lance)
7. Mostrar Resumo em linguagem natural (formato fixo da seção anterior) e aguardar SIM
8. Gerar Preview YAML (formato abaixo)
9. Aguardar SIM
10. POST nas N entidades em sequência
11. Se modelo == campanhas_separadas: também POST adsets e ads de cada campanha
12. Salvar arquivo de hipótese em meus-produtos/{ativo}/trafego/testes/{teste-slug}.md
13. Invalidar cache do /trafego-insights
14. Devolver: IDs criados + comandos DELETE de rollback + data_leitura_em (today + janela_dias)
```

---

## Endpoint Marketing API por modelo

### `ads_mesmo_adset` (apenas `criativo` e `headline`)

> **Importante:** mesmo se o molde tinha `asset_feed_spec` (Advantage+ Creative),
> o `creative` dos ads do teste DEVE ser construído como `object_story_spec.video_data`
> (1 vídeo por ad) ou `object_story_spec.link_data` (1 imagem por ad). Senão o Meta
> escolhe dinamicamente entre múltiplos vídeos/imagens em cada lado e contamina o teste.
> O passo 2 da "Construção do payload" cuida da detecção e simplificação.

```
POST /act_<id>/ads (xN)
{
  "name": "[WS-AB-{slug}] {dimensao}-{variacao}-{produto}",
  "adset_id": "<adset_id>",
  "creative": { ... },             # varia por variação, sempre object_story_spec simplificado
  "status": "PAUSED"
}
```

### `adsets_separados` (criativo, audiencia, faixa_etaria, posicionamento, lance)
```
POST /act_<id>/adsets (xN)
{
  "name": "[WS-AB-{slug}] adset-{dimensao}-{variacao}-{produto}",
  "campaign_id": "<campaign_id>",
  "targeting": { ... },            # idêntico exceto na dimensão variada
  "daily_budget": <budget_em_centavos>,
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "promoted_object": { "pixel_id": "...", "custom_event_type": "PURCHASE" },
  "bid_strategy": "...",           # idêntico exceto se dimensao=lance
  "status": "PAUSED"
}

POST /act_<id>/ads (x1 por adset)  # criativo idêntico nos N
```

### `campanhas_separadas` (apenas `estrutura`)
```
POST /act_<id>/campaigns (xN)
{
  "name": "[WS-AB-{slug}] campaign-{estrutura}-{produto}",
  "objective": "OUTCOME_SALES",
  "buying_type": "AUCTION",
  "smart_promotion_type": "AUTOMATED_SHOPPING_ADS",   # APENAS para Adv+
  "special_ad_categories": [],
  "status": "PAUSED"
}

POST /act_<id>/adsets ...          # 1+ adsets para variação manual; Adv+ cria automaticamente
POST /act_<id>/ads ...
```

---

## Preview YAML padrão

```yaml
sub_fluxo: ab_generico
dimensao: criativo | headline | audiencia | faixa_etaria | posicionamento | lance | estrutura | cta
nome_teste: "[WS-AB] {dimensao}-{slug-A}-vs-{slug-B}-{produto}"
modelo: ads_mesmo_adset | adsets_separados | campanhas_separadas
nivel_criado: ad | adset | campaign
campaign_id: 6987654321                      # ou null se modelo=campanhas_separadas

hipotese: "{frase clara: X performa Y% melhor que Z porque ___}"

variacao_A:
  nome: "[WS-AB-A] {dimensao}-{slug}-{produto}"
  campos_variados:                            # apenas os da coluna da tabela
    {campo_1}: {valor_A}
    {campo_2}: {valor_A}
  budget_diario: 30 BRL
  tamanho_estimado: 2000000                   # apenas se dimensao=audiencia/faixa_etaria

variacao_B:
  nome: "[WS-AB-B] {dimensao}-{slug}-{produto}"
  campos_variados:
    {campo_1}: {valor_B}
    {campo_2}: {valor_B}
  budget_diario: 30 BRL

constantes:                                   # tudo que é igual nos 2 lados
  audience: ...                               # se dimensao != audiencia/faixa_etaria
  criativo: ...                               # se dimensao != criativo
  headline: ...                               # se dimensao != headline
  posicionamento: ...                         # se dimensao != posicionamento
  bid_strategy: ...                           # se dimensao != lance
  optimization_goal: PURCHASE
  pixel_id: ...

janela_minima_dias: 7                         # 14 se dimensao=estrutura
conversoes_minimas_por_lado: 50               # 30 se trilha=high
metrica_primaria: CPA | CTR (headline)
data_leitura_em: 2026-05-12

confirma criar {N} {ad|adset|campanha}(s) PAUSED? (digite SIM)
```

---

## Avisos por dimensão (apresentar ao aluno antes do preview)

### `criativo`
- Posicionamento Advantage+ mistura Feed/Reels/Stories. Para testar criativo em superfície específica, fixar posicionamento manualmente.
- Bidding strategy igual nos 2 lados, senão você está testando criativo + bidding ao mesmo tempo.
- Dimensione budget para garantir 50+ conversões por lado em 7d.
- Se o molde usa Advantage+ Creative (`asset_feed_spec`) com vários vídeos/imagens: os clones do teste vão usar `object_story_spec` simplificado (1 criativo cada). Isso é necessário pra isolar o teste do criativo. Senão o Meta escolhe entre múltiplos criativos em cada lado e o teste vira inconclusivo. Skill detecta isso no passo 2 da "Construção do payload" e pede confirmação ao aluno antes de simplificar.
- Advantage+ Creative ≠ Advantage+ Posicionamento. O primeiro é o `asset_feed_spec` do creative; o segundo é `publisher_platforms=automatic` no targeting do adset. São coisas diferentes e podem coexistir.

### `headline`
- Headlines em Feed ≤ 40 caracteres recomendado. Reels não tem limite mas trunca em ~50 no mobile.
- CTR é a métrica primária; CPA confirma se o headline atrai a pessoa certa.
- Limite recomendado: 3 variações. Mais que isso dilui orçamento por variação.

### `audiencia`
- Audience pequena (< 50K) com budget alto satura rápido.
- Audience muito grande (> 50M) vira broad de fato — algoritmo mistura tudo.
- Não use Advantage+ Audience num lado e segmentação manual no outro: vira teste de "expansão" + "audience" misturados.

### `faixa_etaria`
- Faixas próximas (ex: 25-34 vs 30-39) sobrepõem público; audience efetiva fica menor que a soma.
- Faixas extremas (18-24 vs 55+) podem precisar de criativo diferente. Se o aluno só quer testar idade, manter criativo igual mesmo se subótimo para uma das faixas.

### `posicionamento`
- Vídeo 9:16 funciona em Reels/Stories; vídeo 1:1 trunca em Reels.
- Audience Network e Messenger costumam puxar CPA pra baixo na média mas convertem pior. Para teste limpo Feed vs Reels, excluir Audience Network.

### `lance`
- Bid cap muito baixo (< 70% do CPA target da trilha) faz adset não entregar. Skill avisa.
- Cost cap em low ticket geralmente não compensa: algoritmo precisa de margem para otimizar.
- Mudar bidding em adset existente reseta aprendizado. Para teste limpo, criar adsets novos (modelo `adsets_separados`).

### `estrutura`
- Advantage+ exige pool de criativos (mínimo 4 ads de qualidade variada). Skill bloqueia se < 4.
- Adv+ não permite exclusões granulares (ex: excluir compradores). Funciona melhor para topo de funil novo.
- Comparação em 7d pode não bastar para Adv+. Janela default: 14d.
- Reset de aprendizado ao mover orçamento entre as 2 estruturas. Não deletar o "perdedor" muito cedo.

### `cta`
- A Graph API NÃO devolve breakdown por CTA. Por isso teste é a única forma de comparar (`SHOP_NOW` vs `LEARN_MORE` etc.).
- CTR é a métrica primária; `taxa_conversao_anuncio` (purchases ÷ link_clicks) confirma se o CTA atrai o clique certo. Um CTA agressivo (`SHOP_NOW`) pode subir CTR e derrubar conversão se o público ainda não está pronto pra comprar.
- Validar compatibilidade objetivo × CTA antes do POST. `SHOP_NOW` em `OUTCOME_LEADS` é desperdício; `SIGN_UP` em `OUTCOME_SALES` confunde o algoritmo.
- Manter headline, primary_text, criativo e link_destino idênticos. Senão você está testando CTA + outra coisa ao mesmo tempo.
- Texto que aparece ao lado do botão é definido pelo Meta (vem da localidade do usuário), não pela skill. Aluno não pode personalizar "Compre Agora" para "Adquirir Agora" via API — só escolher o slug.

---

## Após criar (mensagem padrão)

```
✅ Teste A/B criado (PAUSED):
   Variação A: {nivel} {id_A} ("{nome_A}")
   Variação B: {nivel} {id_B} ("{nome_B}")
   {variação C se houver}

Hipótese salva em:
   meus-produtos/{produto}/trafego/testes/{teste-slug}.md

Próximos passos:
1. Ativar as {N} entidades no Gerenciador (PAUSED → ACTIVE).
2. Aguardar {janela_dias} dias com {conversoes_minimas}+ conversões em cada lado.
3. Em {data_leitura}, rodar /trafego-analise opção [3] Criativos para ler resultado.

Para reverter (deletar as {N} entidades criadas):
   DELETE /{id_A}
   DELETE /{id_B}
   {DELETE /{id_C} se houver}
```

---

## Princípios desta sub-skill

1. **UMA dimensão por execução.** Se o aluno pedir 2 dimensões variando, recusar e oferecer rodar 2 testes em sequência.
2. **Simetria obrigatória.** Validar que tudo que NÃO é da dimensão variada está idêntico antes do preview.
3. **Modelo escolhido pela tabela.** Não deixar aluno forçar `ads_mesmo_adset` para `audiencia` ou `posicionamento`.
4. **Avisos da dimensão sempre apresentados** antes do preview.
5. **Toda criação é PAUSED.** Ativação manual após confirmação.
6. **Hipótese registrada** em arquivo .md antes do POST. Sem hipótese, sem teste.
7. **Métrica primária da dimensão usada** na leitura D+7 (CTR para `headline`, CPA para o resto).
8. **Convenção `[WS-AB-{slug}]`** no nome de toda entidade criada.
