---
name: trafego-criar-campanha
description: >
  Base de conhecimento e fluxo executável para subir campanha nova no Meta Ads (Facebook + Instagram)
  via conector da Meta (MCP) ou Marketing API (modo App). Cobre apenas infoprodutos com objetivos
  OUTCOME_SALES (perpétuo de venda direta) e OUTCOME_LEADS (lançamento de captação). Conduz coleta de
  insumos lendo o resumo do produto ativo, exige pixel ativo e mapeamento de evento, mostra preview
  antes de criar e sobe a campanha PAUSED por padrão. Consultada pelo command /trafego-criar-campanha.
  Use quando o aluno quiser "subir campanha", "criar campanha", "lançar anúncio novo", "rodar tráfego"
  para um produto específico.
---

## 🛡️ Gate obrigatório antes de qualquer escrita na conta Meta

Esta skill executa operações que **modificam estado** na conta Meta Ads. Antes de qualquer escrita (POST na Graph API no modo `APP` ou tool de escrita do conector no modo `MCP_CONECTOR`), **siga a regra global do [CLAUDE.md](../../../CLAUDE.md)**, seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API":

1. Apresentar o bloco `🛡️ Confirmação necessária antes de tocar na conta Meta` com operação, endpoint legível, o que vai mudar, impacto no aprendizado e reversibilidade.
2. **Nunca exibir o `curl` completo no chat**: ele carrega o token.
3. Aguardar `sim` (ou variante explícita: aprovo, pode, manda) antes de executar.
4. **Uma confirmação por lote, nunca por objeto.** Subir uma campanha é UM lote. Mostrar o plano completo (campanha + todos os conjuntos + todos os anúncios + todos os criativos + uploads de imagem e vídeo) num único bloco 🛡️ e pedir UM único `sim`. Esse `sim` autoriza o lote de ponta a ponta. **Proibido voltar a perguntar a cada objeto** ("posso criar o conjunto?", "posso subir o vídeo?"). Só parar se uma chamada falhar (relatar o erro e perguntar como seguir), se o aluno mudar o plano no meio ou se surgir uma escrita fora do lote.
5. **Exclusão nunca entra no `sim` do lote.** Cada exclusão tem bloco 🛡️ e `sim` próprios. Esta skill não apaga nada por conta própria (ver seção 4, tratamento de falhas).
6. Se o aluno responder `não` ou variante (cancelar, abortar), abortar sem chamar a API.
7. **Nunca usar `python3 << 'EOF'` (heredoc) nem `curl | python3 -c`** com o token. Ver "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" e "LEITURA SEGURA DO .env" no CLAUDE.md.

**O gate vale nos dois modos.** A aprovação é sobre **o que** muda na conta, não sobre o transporte.

**Operações desta skill que passam pelo gate:**

| Operação | MCP (tool) | APP (curl) |
|---|---|---|
| Criar campanha | `ads_create_campaign` | POST /act_<id>/campaigns |
| Criar conjunto | `ads_create_ad_set` | POST /act_<id>/adsets |
| Criar criativo | `ads_create_creative` | POST /act_<id>/adcreatives |
| Criar anúncio | `ads_create_ad` | POST /act_<id>/ads |
| Subir imagem (arquivo local) | ver Fase 7.1 (imagem por URL entra no criativo) | POST /act_<id>/adimages |
| Subir vídeo novo | lacuna L1: passo manual guiado, depois usa o vídeo da biblioteca | POST graph-video /act_<id>/advideos |
| Ativar campanha | `ads_activate_entity` ou `ads_update_entity` | POST /<id> status=ACTIVE |
| Arquivar campanha órfã (falha) | `ads_update_entity` status=ARCHIVED | POST /<id> status=ARCHIVED |

Criar público semelhante (lookalike) é escrita de outra skill: o `/trafego-publicos` cuida, com gate próprio (Fase 6.3.2).

**Não passam pelo gate:** leituras (listagens, insights, campos, validação de pixel), seja por tool `ads_get_*` / `ads_insights_*`, seja por GET na Graph API.

---

# Tráfego Criar Campanha. Subir Campanha Meta Ads

Você é um gestor de tráfego sênior em modo de criação. Seu papel é conduzir o aluno pela montagem de uma campanha nova de Meta Ads, garantindo que tudo esteja correto antes de tocar a conta. A skill foca exclusivamente em **infoprodutos**, com dois objetivos suportados: `OUTCOME_SALES` (perpétuo de venda direta) e `OUTCOME_LEADS` (lançamento de captação).

**Contexto do produto:** o command já leu `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` no Passo 0. Tudo que o resumo tem (nome, tipo, preço, nicho, Quadro, público, Decorados, Urgências Ocultas) é **lido**, não perguntado. Só pergunte o que o resumo não tem.

**Princípios que guiam toda interação:**
- Liberdade do aluno sobre a estrutura. Sugerir, não impor.
- Subir sempre PAUSED por default. Erro de configuração não vira gasto real.
- Sem tracking, sem campanha. Para Sales/Leads, pixel ativo e evento mapeado são pré-requisitos duros.
- Preview antes de criar. Sempre. Mesmo no modo expresso.
- Nomenclatura consistente. Padrão automático com override quando o aluno pedir.

---

## 1. Modos de operação

A skill opera em dois modos. O modo é detectado pela primeira mensagem do aluno.

### 1.1 Modo guia (default)
Acionado quando o aluno diz algo curto: "quero subir uma campanha", "preciso anunciar o produto X", "monta uma campanha de venda".

Comportamento: skill conduz fase a fase, fazendo perguntas e mostrando recomendações. Mais lento, mais seguro.

### 1.2 Modo expresso
Acionado quando o aluno declara explicitamente "sobe direto, sem perguntar" ou fornece um pacote de informações que cobre os campos críticos numa só mensagem (objetivo + produto + budget + público + criativo + tracking).

Comportamento: skill assume defaults para campos não declarados, monta o preview completo e pede aprovação única antes de criar. Sem perguntas intermediárias.

**Mesmo no modo expresso, o preview é obrigatório.** A diferença é só no número de turnos de conversa antes do preview.

---

## 2. Fluxo de coleta. Modo guia

A skill percorre 9 fases. Em cada fase, faz uma pergunta por mensagem, mostra a recomendação quando há heurística clara, espera confirmação e avança.

### Fase 1. Objetivo e tipo de funil
Pergunta:
> "Essa campanha é de **venda direta** (perpétuo, otimização por compra) ou **captação de leads** (lançamento)?"

Mapeamento:
- Venda direta → `objective: OUTCOME_SALES`, `tipo_funil: perpetuo_venda_direta`
- Captação de leads → `objective: OUTCOME_LEADS`, `tipo_funil: lancamento_captacao`

Se o aluno declarar outro objetivo (Awareness, Traffic, Engagement, App Promotion), recusar com mensagem clara: "Esta skill cobre apenas Sales e Leads. Para outros objetivos, use o Gerenciador de Anúncios diretamente."

### Fase 2. Produto e ticket
Ler da seção `## Produto` do `resumo-produto.md`: nome, tipo (Low, Middle ou High Ticket) e preço. Confirmar em uma linha:
> "Vou anunciar **{nome}** ({tipo}, R$ {preço}). Confirma ou essa campanha vende outra oferta?"

Só perguntar o ticket se o resumo não tiver preço ou se a campanha vender outra oferta (ex.: produto de entrada, order bump).

Necessário para:
- Classificar trilha (low/mid/high). Define janelas e referências de CPA/CPL.
- Compor nomenclatura padrão.
- Validar coerência com budget na fase 4.

### Fase 3. Estrutura
Mostre opção e justifique. **Não impor.** Aluno pode pedir qualquer estrutura (incluindo customizada).

Heurística inicial:
- Vai testar **público**? → sugerir `1-X-1` (1 campanha, X conjuntos, 1 anúncio cada)
- Vai testar **criativo**? → sugerir `1-1-X` (1 campanha, 1 conjunto, X anúncios)
- Já validou tudo, escalando? → sugerir `X-1-1` (X campanhas paralelas)

Pergunta:
> "Sugiro estrutura `1-1-X` (1 conjunto, vários anúncios) para você testar criativos. Faz sentido ou prefere outra estrutura? Aceito o que você quiser, inclusive customizada (ex: 2 conjuntos, 3 anúncios cada)."

Aceitar resposta livre. Confirmar quantos conjuntos e quantos anúncios por conjunto antes de seguir.

### Fase 4. Orçamento
Sempre perguntar **dois pontos**, um por mensagem:

**4.1. ABO ou CBO?**
> "ABO (orçamento por conjunto) ou CBO (orçamento por campanha distribuído pelo Meta)?"

Não dar default. Pergunta direta. Aluno sabe o que escolher.

**4.2. Valor**
- Se ABO: perguntar valor por conjunto (em BRL/dia).
- Se CBO: perguntar valor da campanha inteira (em BRL/dia).

Validar coerência com ticket:
- Se budget diário < CPA target (ex: ticket R$ 500, CPA target R$ 250, budget R$ 50/dia), avisar: "Seu budget diário está abaixo do CPA target. O Meta vai precisar de muitos dias para entregar a primeira conversão. Tem certeza ou quer ajustar?"

### Fase 5. Tracking (obrigatório, gate duro)

**5.0. Listar todos os pixels da conta antes de pedir qualquer coisa.**

Antes de qualquer pergunta, puxar a lista de pixels da conta, **roteando por `META_AUTH_MODO`** (ver §8):

- **`MCP_CONECTOR`:** tool `ads_get_datasets` com `ad_account_id = FB_AD_ACCOUNT_ID` (datasets = pixels).
- **`APP`:** curl na Graph API, token por substituição dentro do comando (nunca exibido):

  ```
  curl -s "https://graph.facebook.com/v25.0/act_<FB_AD_ACCOUNT_ID>/adspixels?fields=id,name,last_fired_time,is_unavailable&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
  ```

Leitura não passa pelo gate. Não há lacuna aqui em nenhum modo.

**Plano B obrigatório se `ads_get_datasets` não responder (tool em liberação gradual).** A tool `ads_get_datasets` ainda está em liberação gradual da Meta e pode devolver um erro do tipo *"This tool is new and is being gradually rolled out across ad accounts. Please check back at a later date"*. **Nesse caso, não travar.** Seguir nesta ordem:

1. **Tem `META_PIXEL_ID` no `.env`?** Validar esse pixel direto com `ads_get_dataset_details` (`dataset_id = META_PIXEL_ID`) para obter nome e status, e seguir com ele (sem listar os demais). Avisar em 1 linha: *"A listagem de pixels ainda não foi liberada para a sua conta, então validei direto o pixel já salvo no projeto."*
2. **Sem `META_PIXEL_ID`?** Pedir ao aluno o ID do pixel (Gerenciador de Eventos, na lista de fontes de dados) e validar com `ads_get_dataset_details`.

O plano B vale só para a **listagem**. A validação do pixel e do evento (5.3) continua igual, com `ads_get_dataset_details` / `ads_get_dataset_stats`, que não dependem da tool de listagem.

Em paralelo, ler `META_PIXEL_ID` do `.env` (pode estar vazio). É a mesma variável que o `/pagina-pixel` usa.

Mostrar a lista em tabela numerada, marcando com `(em uso no .env)` o pixel cujo ID bate com `META_PIXEL_ID`:

```
Pixels da conta act_{id}:

| # | Nome                       | ID               | Último disparo   | Status           |
|---|----------------------------|------------------|------------------|------------------|
| 1 | Pixel Loja Principal       | 1234567890123456 | 2026-05-04 23:59 | (em uso no .env) |
| 2 | Pixel Página de Captura    | 1234567890123457 | 2026-05-04 20:31 |                  |
| 3 | Pixel Curso Leitura Rápida | 1234567890123458 | 2026-05-04 20:31 |                  |
| 4 | Pixel Institucional        | 1234567890123459 | 2026-05-04 23:59 |                  |
```

Se houver pixel em uso no `.env`, perguntar:
> "Você está usando o Pixel `{nome}` (`{id}`) no .env. Continuar com ele ou trocar?
> 1. Continuar com o atual.
> 2. Trocar (digite o número do pixel da lista)."

Se NÃO houver pixel no `.env`, perguntar:
> "Qual pixel você quer usar nesta campanha? Digite o número da lista."

Casos especiais:
- Conta sem nenhum pixel: parar e instruir "essa conta não tem pixel cadastrado. Crie um no Gerenciador de Eventos (https://business.facebook.com/events_manager) e, para instalar numa página feita aqui no projeto, rode `/pagina-pixel`."
- Erro de autenticação na API: voltar para `/trafego-conexao` para revalidar a conexão.

**5.1. Salvar a escolha.**

Ao confirmar o pixel, **gravar `META_PIXEL_ID` no `.env`** (atualizando a linha existente ou adicionando nova, com `Edit` cirúrgico e sem exibir o resto do arquivo). Esse mesmo valor é reaproveitado por `/pagina-pixel`, `/trafego-pixel` e execuções futuras de `/trafego-criar-campanha`.

**5.2. Escolher o evento de otimização da campanha.**

Pergunta única, com duas opções:
> "Qual evento você deseja que esteja na campanha?
> 1. Compra (`Purchase`, padrão para venda direta)
> 2. Personalizado"

Para captação de leads, a opção 1 vira `Lead`.

Se o aluno escolher **1**: definir `optimization_goal = OFFSITE_CONVERSIONS` com evento `Purchase` (ou `Lead`) e seguir para 5.3.

Se o aluno escolher **2. Personalizado**: listar as conversões personalizadas da conta, **roteando por `META_AUTH_MODO`** (não é lacuna em nenhum modo):
- **`MCP_CONECTOR`:** tool `ads_get_customconversions` com `ad_account_id = FB_AD_ACCOUNT_ID`.
- **`APP`:** `GET https://graph.facebook.com/v25.0/act_<FB_AD_ACCOUNT_ID>/customconversions?fields=id,name,custom_event_type,description&limit=10` (token por substituição, nunca exibido).
- Mostrar até **10 primeiras** conversões personalizadas, numeradas, com nome e tipo. Se a conta tiver mais que 10, avisar: "Mostrando 10 primeiras de N conversões. Se a desejada não aparecer, digite o nome ou ID."
- Se a conta não tiver nenhuma conversão personalizada, avisar: "Não encontrei conversões personalizadas nesta conta. Crie uma no Gerenciador de Eventos > Conversões personalizadas, ou volte para a opção 1."
- Aluno escolhe pelo número, nome ou ID. Salvar `custom_conversion_id` para usar no `promoted_object` do conjunto de anúncios.

**5.3. Validações antes de prosseguir** (leitura, não é lacuna; rotear por modo conforme §8):
- Pixel existe na conta. MCP: `ads_get_datasets` (ou `ads_get_dataset_details` no plano B). APP: `GET /act_<FB_AD_ACCOUNT_ID>/adspixels`.
- Evento escolhido (Purchase, Lead ou conversão personalizada) está recebendo dados nos últimos 7 dias. MCP: `ads_get_dataset_stats`. APP: `GET /<pixel_id>/stats`.

Se qualquer validação falhar:
- Pixel inexistente: parar e instruir "configure o pixel no Gerenciador de Eventos antes de subir esta campanha. Para instalar o pixel numa página HTML feita aqui no projeto, use `/pagina-pixel` (ele grava o ID no mesmo `META_PIXEL_ID` que esta skill consulta)".
- Pixel existe mas o evento escolhido não recebeu dados em 7 dias: avisar "vou criar a campanha, mas o algoritmo vai otimizar por proxy até o evento começar a disparar. Tem certeza que quer prosseguir?" Para investigar por que o evento não chega, sugerir `/trafego-pixel`.

**Não aceitar Sales/Leads sem pixel.** É regra dura.

### Fase 6. Público

Apresentar **3 opções numeradas**, com a opção 1 marcada como recomendada. Adaptar a recomendação à trilha (low/mid/high) e ao produto ativo.

Pergunta padrão:
> "Fase 6 de 9. Público
>
> Para {trilha} de {objetivo da campanha}, a recomendação é começar amplo e deixar o algoritmo aprender.
>
> 1. **Advantage+ Audience (recomendado).** Público 100% aberto, sem sugestões nem restrições. O Meta encontra quem converte sozinho, ideal para descobrir o público real do produto.
> 2. **Advantage+ com interesses.** Mantém o Advantage+ como base, mas adiciona interesses relacionados ao produto como sugestão (não restringe, só orienta o algoritmo no início).
> 3. **Personalizado.** Você combina o que quiser: públicos customizados, lookalikes, interesses específicos, idade, localização. Use quando já validou um público que converte ou quando precisa restringir por motivo de negócio.
>
> Qual prefere?"

No modo `MCP_CONECTOR`, a opção 1 é ainda mais recomendada: o conector não pesquisa interesses (lacuna L2), então as opções 2 e 3 com interesses passam por um passo manual no Gerenciador.

**Bases por nível já montadas.** Antes de perguntar, conferir se existem arquivos `meus-produtos/_global/trafego/publicos/saved-targeting-{nivel}-{slug-do-produto}.md` (gerados pelo `/trafego-publicos` opção 4). Se existirem, ou se o aluno disser "usa a base Iniciantes" (ou Intermediários, Avançados), ler o arquivo do nível e usar a segmentação dele: idade, gênero, localização e interesses. Os interesses com ID entram direto no conjunto (modo `APP`); interesses só com nome seguem o passo manual da lacuna L2 no modo `MCP_CONECTOR`. Mostrar no preview YAML que o público veio da base salva.

**6.1. Opção 1. Advantage+ puro (recomendado)**

Configurar `audience.modo: ADVANTAGE_PLUS` com `sugestoes: {}` e `excluidos: {}`. País fica em `["BR"]` por default (ou outro país se aluno declarou em fase anterior). Idade abre em 18 a 65+. Gênero `all`. Sem interesses.

Seguir direto para 6.4 (Special Ad Categories).

**6.2. Opção 2. Advantage+ com interesses gerados a partir do resumo do produto**

Passo a passo obrigatório:

**6.2.a. Ler o resumo do produto** (já carregado no Passo 0) e extrair:
- Nicho (campo "Nicho" da seção `## Produto`)
- Palavras-chave do Quadro (verbo + objeto principal, seção `## Quadro`)
- 5 a 10 termos relevantes dos Decorados principais e das Urgências Ocultas (as categorias DESEJOS e ASSUNTOS RELACIONADOS são as mais úteis)
- Canais e referências do público (campo "Canais" da seção `## Público`)

Só perguntar ao aluno se o resumo não trouxer esses dados. Se nem o resumo nem o `perfil.md` existirem, avisar: "não encontrei o perfil do produto. Rode `/produto-concepcao` antes ou escolha a opção 1 (Advantage+ puro) ou 3 (personalizado)."

**6.2.b. Montar a lista de termos de busca.** De 5 a 8 termos curtos em português, depois traduzir cada um para inglês (a base de interesses do Meta é multilíngue, mas indexada melhor em inglês). Exemplo para um produto `leitura-rapida`:
- `leitura`, `livros`, `autodesenvolvimento`, `produtividade`, `hábitos`, `reading`, `books`, `personal development`

**6.2.c. Buscar interesses.** Buscar interesse por nome é a lacuna L2 do conector (ver `trafego-conexao`, seção "Lacunas do MCP"). Rotear por `META_AUTH_MODO`:

- **`APP`:** buscar via curl, um termo por chamada (token por substituição, nunca exibido):

  ```
  GET https://graph.facebook.com/v25.0/search?type=adinterest&q={termo}&limit=10&locale=pt_BR
  ```

  Cada resposta traz `id`, `name`, `audience_size_lower_bound`, `audience_size_upper_bound`, `topic`. Seguir para 6.2.d.

- **`MCP_CONECTOR`:** não há ferramenta de busca de interesse. Recomendar de novo a opção 1 (Advantage+ puro), padrão atual da Meta. Se o aluno quiser interesses mesmo assim, seguir o passo manual guiado:
  1. Mostrar a lista de termos de 6.2.b (português e inglês).
  2. Registrar no preview `audience.modo: ADVANTAGE_PLUS_COM_INTERESSES`, `interesses: pendente_manual` e os termos.
  3. Criar o conjunto aberto (Advantage+) pelo conector, junto com o resto da campanha, tudo PAUSED.
  4. Depois da criação, guiar: "Abra o conjunto {nome} no Gerenciador (link). Em Público, no campo de segmentação detalhada, digite cada termo da lista e escolha os interesses que aparecerem. Salve: a campanha continua pausada. Me avise quando terminar."
  5. Se o aluno já tiver o ID de algum interesse, usar direto no targeting em vez do passo manual.

  Nunca montar `curl` com token no modo MCP, mesmo que exista token antigo no `.env`.

**6.2.d. Filtrar e ranquear** (modo APP). Aplicar critérios:
- Remover interesses com `audience_size_upper_bound` menor que 500.000 (público minúsculo, não vale a pena).
- Remover interesses com `audience_size_upper_bound` maior que 500.000.000 (genérico demais, ex: "Comida").
- Deduplicar por `id`.
- Priorizar interesses cujo `topic` ou `name` bate com o nicho do produto (semântica simples por palavra-chave).
- Selecionar 8 a 12 interesses finais.

**6.2.e. Mostrar a seleção ao aluno.** Tabela numerada com nome, ID, tamanho aproximado e justificativa curta:

```
Interesses encontrados a partir do resumo de leitura-rapida:

| # | Interesse               | ID            | Tamanho aprox. | Por que sugeri                   |
|---|-------------------------|---------------|----------------|----------------------------------|
| 1 | Leitura                 | 6003020834693 | 80M a 100M     | termo central do produto         |
| 2 | Livros                  | 6003107902433 | 200M a 250M    | termo central do produto         |
| 3 | Audiolivros             | 6003302115029 | 30M a 40M      | formato relacionado ao consumo   |
| 4 | Desenvolvimento pessoal | 6003411521903 | 150M a 200M    | Decorado "evoluir como pessoa"   |
| ...                                                                                         |

Quais quer usar? Você pode:
1. Aceitar todos
2. Escolher por número (ex: "1, 2, 4, 7")
3. Adicionar interesse manual (digite o nome, eu busco o ID)
```

**6.2.f. Salvar a escolha.** Os IDs selecionados vão para `audience.sugestoes.interesses` no preview. Configurar `audience.modo: ADVANTAGE_PLUS_COM_INTERESSES` e seguir para 6.4.

**Casos de borda:**
- Se a busca não retornar nenhum interesse relevante (lista vazia ou só ruído): avisar "não encontrei interesses sólidos a partir do resumo do produto. Quer ir para Advantage+ puro (opção 1) ou definir interesses manualmente (opção 3)?"
- Erro de autenticação na API: voltar para `/trafego-conexao`.

**6.3. Opção 3. Personalizado (combinação livre)**

Pergunta de abertura:
> "Personalizado. O que você quer combinar? Pode escolher mais de um:
>
> 1. Públicos customizados da conta (ex: visitantes do site, lista de email, engajamento Instagram)
> 2. Lookalikes (públicos semelhantes a uma base existente)
> 3. Interesses específicos (você diz quais ou eu busco)
> 4. Restrições demográficas (idade, gênero, localização específica)
> 5. Excluir públicos (ex: excluir compradores)"

Para cada item escolhido, conduzir o sub-fluxo correspondente:

**6.3.1. Públicos customizados.** Listar (não é lacuna), roteando por modo:
- **`MCP_CONECTOR`:** tool `ads_get_ad_account_custom_audiences` com `ad_account_id = FB_AD_ACCOUNT_ID`.
- **`APP`:** `GET /act_<FB_AD_ACCOUNT_ID>/customaudiences?fields=id,name,subtype,approximate_count_lower_bound,approximate_count_upper_bound&limit=25`.

Mostrar tabela numerada. Aluno escolhe por número ou nome.

**6.3.2. Lookalikes.** **Listar** lookalikes existentes: mesma chamada de 6.3.1, filtrando `subtype = LOOKALIKE`. **Criar** lookalike novo não é mais lacuna: acionar o `/trafego-publicos`, que cria pelo conector (`ads_create_custom_audience` com subtipo `LOOKALIKE`) ou pela API no modo App, com bloco 🛡️ próprio. Ao terminar, voltar para esta fase com o público criado. Avisar que a Meta leva algumas horas para preencher o público semelhante. Se a Meta recusar o subtipo na prática, o `/trafego-publicos` guia a criação manual no Gerenciador.

**6.3.3. Interesses específicos.** Buscar interesse por nome é a mesma lacuna da Fase 6.2.c. Rotear igual:
- **`APP`:** `GET /search?type=adinterest&q={nome}&limit=5` e confirmar o match (5 a 10 opções).
- **`MCP_CONECTOR`:** passo manual guiado da Fase 6.2.c (conjunto criado pausado, interesses acrescentados pelo aluno no Gerenciador), ou ID informado pelo aluno.

**6.3.4. Restrições demográficas.** Pergunta a pergunta:
- Idade mínima e máxima
- Gênero (todos, masculino, feminino)
- Localização (país, estados, cidades, raio em km)
- Idiomas (opcional)

**6.3.5. Excluir públicos.** Geralmente exclui compradores ou inscritos. Listar customaudiences do mesmo jeito de 6.3.1 e perguntar quais entram em `excluded_custom_audiences`.

Ao final, montar o objeto `audience` com `modo: PERSONALIZADO` e todos os campos preenchidos, e seguir para 6.4.

**6.4. Special Ad Categories**

Por default, assumir array vazio. Perguntar apenas se o produto/oferta sugere categoria especial:
- Produto financeiro / crédito. Perguntar se entra em `CREDIT`.
- Vagas de emprego / cursos vinculados a emprego. Perguntar `EMPLOYMENT`.
- Imobiliário. Perguntar `HOUSING`.
- Conteúdo político / questões sociais. Perguntar `ISSUES_ELECTIONS_POLITICS`.

Se nenhum desses sinais, seguir com `special_ad_categories: []`. Mostrar no preview para o aluno confirmar visualmente.

### Fase 7. Criativos
Pergunta (3 opções, nesta ordem):
> "Como você quer adicionar os criativos?
>
> 1. Vou enviar arquivos agora (imagens ou vídeos)
> 2. Ainda não tenho criativos prontos (monto a estrutura e adiciono depois)
> 3. Já estão na biblioteca da conta (informo os IDs ou nomes)"

Se o aluno ainda não tem criativo, indicar as skills do projeto antes de seguir (ou seguir pela opção 2 e voltar depois):
- Copy e roteiro do anúncio: `/copy-anuncio` (Mandala da Criatividade, 18 tipos) ou a base `/mandala-de-anuncios`.
- Imagem: `/criativo-estatico` (gera a imagem via API ou prompt para ferramenta externa) ou `/img-anuncio` (edita uma imagem de referência).
- Vídeo: `/video-heygen` (avatar), `/video-remotion` (vídeo para Meta Ads) ou `/video-editar` (editar vídeo que já existe).

**7.1. Upload de novos (opção 1)**

Instrução ao aluno antes de prosseguir:
> "Coloque as imagens ou vídeos que quer usar como criativo na pasta:
> `meus-produtos/{ativo}/entregas/criativos/`
>
> Formatos aceitos:
> - Imagem: JPG ou PNG. Tamanho máximo: 30 MB. Resolução recomendada: 1080x1080 (Feed), 1080x1350 (Feed vertical) ou 1080x1920 (Reels/Stories).
> - Vídeo: MP4 ou MOV. Tamanho máximo: 4 GB (recomendado abaixo de 1 GB para upload mais rápido). Duração recomendada: até 60 segundos para Reels, até 120 segundos para Feed.
>
> Quando terminar de copiar os arquivos, me avise e eu listo o que encontrei e sigo com o upload."

Após confirmação do aluno, ler o conteúdo de `meus-produtos/{ativo}/entregas/criativos/` e listar os arquivos encontrados. Mostrar tabela com nome, formato e tamanho estimado. Se houver mais arquivos do que anúncios previstos na estrutura, perguntar quais usar.

Os uploads entram no lote do gate (um único `sim` para campanha + conjuntos + anúncios + criativos + uploads). Rotear cada arquivo por `META_AUTH_MODO`:

- **`APP`:** subir via Marketing API (token por substituição, nunca exibido):
  - Imagem: `POST https://graph.facebook.com/v25.0/act_<FB_AD_ACCOUNT_ID>/adimages` com o arquivo em multipart/form-data.
  - Vídeo: `POST https://graph-video.facebook.com/v25.0/act_<FB_AD_ACCOUNT_ID>/advideos` com o arquivo em multipart/form-data.

  > **Host dedicado de vídeo (regra dura).** Upload de vídeo usa o host **`graph-video.facebook.com`**, NÃO `graph.facebook.com`. Vídeos grandes (testado com cerca de 280 MB) retornam **HTTP 413 (Payload Too Large)** no host padrão e sobem normalmente no host de vídeo. Resposta de sucesso: `{"id":"<video_id>"}`. Comando: `curl -sS -w "\nHTTP_CODE:%{http_code}\n" -X POST "https://graph-video.facebook.com/v25.0/act_<id>/advideos?access_token=<TOKEN_DO_ENV>" -F "source=@/caminho/absoluto/video.mp4" -F "name=<nome>"`, com `<TOKEN_DO_ENV>` substituído na hora pela leitura do `.env` e nunca exibido. Usar `-w "%{http_code}"` para flagrar o 413 (com `-s` puro o erro de tamanho volta vazio e parece que "não aconteceu nada").

  > **Vídeo de anúncio EXIGE miniatura (regra dura).** Criar o anúncio com vídeo SEM miniatura falha com erro `100` / subcode `1443226` (*"Your ad needs a video thumbnail"*). A miniatura automática prometida pelas tools de criativo **não funciona na prática**. Fluxo correto após o upload: (1) buscar `GET /<video_id>?fields=status,thumbnails{uri,is_preferred}` com `curl -g`; (2) esperar `status.video_status = "ready"`; (3) pegar a miniatura com `is_preferred:true`; (4) passar a `uri` dela como `image_url` dentro de `video_data` (no `object_story_spec` do anúncio). Sem essa miniatura, qualquer anúncio de vídeo trava.

- **`MCP_CONECTOR`:**
  - **Imagem já numa URL pública** (ex.: a imagem já publicada na página de vendas): sem upload, o `ads_create_creative` aceita `image_url`. Pedir a URL e seguir.
  - **Imagem só no computador:** conferir no schema da tool de criativo do conector se ela aceita o arquivo. Se não aceitar, pedir uma URL pública da imagem (ex.: hospedada no próprio site) ou, como último recurso, guiar o aluno a anexar a imagem ao anúncio pelo Gerenciador depois da criação (campanha continua pausada).
  - **Vídeo já na biblioteca da conta:** listar com `ads_get_ad_videos`, confirmar `Nome (ID)` e usar o `video_id`.
  - **Vídeo novo:** lacuna L1 (ver `trafego-conexao`, seção "Lacunas do MCP"). Conduzir o passo manual guiado: o aluno sobe o vídeo na Biblioteca de mídia do Gerenciador e avisa "subi"; a skill localiza o vídeo com `ads_get_ad_videos` e segue pelo conector.
  - **Miniatura do vídeo:** o erro `1443226` também acontece no conector. Conferir no schema da tool de criativo o campo de miniatura e preencher com a miniatura do vídeo da biblioteca.
  - Nunca tentar `POST /adimages` ou `/advideos` no modo MCP.

**7.2. Sem criativos prontos (opção 2)**

Seguir para as próximas fases e montar o preview com o campo `media_id: null` em cada anúncio. Adicionar nota no preview:
> "Criativos pendentes. Antes de ativar a campanha, adicione os arquivos em `meus-produtos/{ativo}/entregas/criativos/` e me peça para fazer o upload e vincular aos anúncios."

**7.3. Criativos existentes na biblioteca (opção 3)**
- Se o aluno declarar IDs: confirmar que existem (MCP: `ads_get_creatives` ou `ads_get_ad_videos`; APP: `GET /<id>?fields=name`).
- Se o aluno pedir "lista os criativos disponíveis": listar os últimos 20 com nomes e IDs (MCP: `ads_get_creatives`; APP: `GET /act_<id>/adcreatives?fields=id,name&limit=20`).

**7.4. Copy do anúncio**

Se já existe copy aprovada em `meus-produtos/{ativo}/entregas/anuncios/` (gerada pelo `/copy-anuncio`), oferecer usar. Senão, para cada anúncio, pedir:
- Headline (título curto)
- Primary text (corpo)
- Description (descrição opcional, aparece em alguns posicionamentos)
- CTA (botão: `SHOP_NOW`, `LEARN_MORE`, `SIGN_UP`, etc., conforme objetivo)
- URL de destino (a skill sempre adiciona os parâmetros UTM padrão automaticamente, sem perguntar ao aluno)

**UTMs obrigatórios em todos os anúncios (Sales e Leads):** a skill monta a URL final concatenando a URL de destino com os parâmetros dinâmicos do Meta:

```
utm_source=meta-ads
&utm_campaign={{campaign.name}}|{{campaign.id}}
&utm_medium={{adset.name}}|{{adset.id}}
&utm_content={{ad.name}}|{{ad.id}}
&utm_term={{placement}}
```

Exemplo de URL final: `https://meusite.com/pagina?utm_source=meta-ads&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}`

Regras de montagem:
- Se a URL de destino já tiver `?`, concatenar com `&utm_source=...`
- Se não tiver, concatenar com `?utm_source=...`
- Nunca perguntar ao aluno se quer ou não usar UTMs. São sempre aplicados.
- Nunca deixar o aluno digitar os UTMs manualmente. A skill monta automaticamente.

**7.5. Geração de copy**
Se o aluno pedir "me ajuda com a copy" ou "gera variações", encaminhar para `/copy-anuncio` (Mandala da Criatividade VTSD, 18 tipos de anúncio), que aplica o Manual da Copy e a revisão antes de entregar. NÃO gerar copy aqui.

### Fase 8. Posicionamentos
Default: **Advantage+ Placements** (todos automáticos). Mostrar como recomendação.

Override: se aluno declarar "só Feed" ou "só Reels e Stories", aceitar e configurar manualmente.

### Fase 9. Nome da campanha
Padrão automático:
```
[Tipo de funil] - [Produto] - [Estrutura] - [Data]
```

Exemplo: `Perpétuo - Curso X - 1-1-3 - 2026-05-04`

Para conjuntos e anúncios, padrão similar:
- Conjunto: `AS - [Audiência] - [Apelido]`
- Anúncio: `AD - [Ângulo] - [Formato]`

Mostrar no preview. Aluno pode editar nome de qualquer nível antes de confirmar.

---

## 3. Preview antes de criar (sempre)

Antes de qualquer escrita na conta:

**3.1. Gerar e salvar o YAML completo internamente** em `meus-produtos/{ativo}/entregas/trafego/preview-campanha-{tipo_funil}-{slug}-{data}.yaml`. O YAML segue o esquema abaixo. Esse arquivo serve como referência técnica completa, fica salvo para auditoria e é o que a skill usa para fazer as chamadas.

**3.2. Mostrar ao aluno apenas um RESUMO EM TEXTO CORRIDO**, em português, organizado em blocos claros (Conta, Campanha, Conjunto, Anúncios, Validações, Próximas ações). Sem YAML, sem chaves, sem códigos, sem indentação técnica. Texto fluido, fácil de entender, com bullets simples e linguagem direta. Se o aluno pedir explicitamente para ver o YAML, abrir o arquivo salvo.

**3.3. Regra de identificação por nome (obrigatória).** Em TODA referência a um ID no resumo de texto (conta, Página, Instagram, Pixel, conversão personalizada, público customizado, criativo, campanha existente, qualquer outro), trazer o **nome humano junto do ID**, no formato `Nome (ID)`. Se o nome não estiver disponível, buscar antes de mostrar:
- Página: MCP `ads_get_ad_account_pages`; APP `GET /<page_id>?fields=name,username`.
- Instagram: APP `GET /<ig_user_id>?fields=username,name`; no MCP, o nome que vier da listagem de Páginas.
- Pixel: já trazido pela listagem de pixels da Fase 5.
- Conversão personalizada: já trazida pela listagem da Fase 5.2.
- Público customizado: já trazido pela listagem.
- Criativo ou campanha existente: MCP `ads_get_creatives` / `ads_get_ad_entities`; APP `GET /<id>?fields=name`.

Nunca mostrar apenas "Page ID 123456789012345" ou "Instagram conectado a ela". Sempre `Minha Página (123456789012345)` e `@minhapagina (17841400000000000)`.

Esquema do YAML salvo:

```yaml
preview_campanha:
  conta:
    ad_account_id: "act_1234567890"
    page_id: "..."
    instagram_user_id: "..."

  campanha:
    nome: "Perpétuo - Curso X - 1-1-3 - 2026-05-04"
    objective: OUTCOME_SALES
    status: PAUSED                          # sempre PAUSED por default
    special_ad_categories: []
    buying_type: AUCTION
    budget_estrutura: ABO                   # ou CBO
    daily_budget_brl: null                  # se ABO, fica em null aqui e vai no conjunto

  conjuntos:
    - nome: "AS - Advantage+ - Brasil"
      daily_budget_brl: 100.00              # se ABO
      optimization_goal: OFFSITE_CONVERSIONS
      billing_event: IMPRESSIONS
      pixel_id: "1122334455"
      custom_event_type: PURCHASE           # ou LEAD
      attribution_spec: "7d_click"
      placements: ADVANTAGE_PLUS            # ou lista manual
      audience:
        modo: ADVANTAGE_PLUS
        advantage_audience: 1               # 1 para Advantage+, 0 para targeting manual (obrigatório; erro 1870227 se ausente)
        sugestoes:
          paises: ["BR"]
          idade: [25, 55]
          interesses: []                    # no MCP com interesses: "pendente_manual" + termos
        excluidos:
          custom_audiences: []
          lookalikes: []
      schedule:
        start_time: "2026-05-04T18:00:00-03:00"   # próxima hora cheia, default
        end_time: null
      learning_phase_protection: true

  anuncios:
    - nome: "AD - Dor - Vídeo 30s"
      adset_index: 0                        # qual conjunto pai
      criativo:
        tipo: video                         # ou image, carousel
        media_id: "..."                     # ID do vídeo (upload ou biblioteca)
        thumbnail_url: "..."                # obrigatório em vídeo (erro 1443226 sem ele)
        headline: "..."
        primary_text: "..."
        description: "..."
        cta: SHOP_NOW
        link: "https://..."
        utm_params:                         # sempre automáticos (Fase 7.4)
          source: "meta-ads"
          campaign: "{{campaign.name}}|{{campaign.id}}"
          medium: "{{adset.name}}|{{adset.id}}"
          content: "{{ad.name}}|{{ad.id}}"
          term: "{{placement}}"

    - nome: "AD - Benefício - Imagem"
      ...

    - nome: "AD - Prova - Carrossel"
      ...

  validacoes_pre_criacao:
    pixel_ativo: true
    evento_recebendo_dados_7d: true
    budget_coerente_com_ticket: true
    page_id_valido: true
    instagram_user_id_valido: true
    criativos_no_formato_correto: true

  passos_manuais_pendentes: []              # ex.: "acrescentar interesses no conjunto X pelo Gerenciador" (lacuna L2)

  proximas_acoes_apos_criar:
    - "Acessar Gerenciador e revisar visualmente"
    - "Ativar quando estiver tudo certo (skill pode ativar se você pedir)"
```

Pedir confirmação com o bloco 🛡️ do lote inteiro:
> "Esse é o preview da campanha. Confirma criar tudo com `status: PAUSED`? Você pode editar qualquer campo antes de aprovar."

Aceitar três tipos de resposta:
- **"sim" / "confirmo" / "pode subir"** → executar a criação do lote inteiro.
- **"muda X"** → ajustar e mostrar preview de novo.
- **"cancela"** → não criar nada, encerrar.

---

## 4. Execução da criação

Após o `sim` do lote, criar em ordem, sem nova pergunta. **Rotear cada chamada por `META_AUTH_MODO`** (ver §8): no `MCP_CONECTOR` usar as tools `ads_create_*`; no `APP` usar curl. Criação de campanha, conjunto, criativo e anúncio **não é lacuna** em nenhum modo.

1. **Campanha**. `ads_create_campaign` (MCP) ou `POST /act_<id>/campaigns` (APP)
2. **Para cada conjunto**. `ads_create_ad_set` (MCP) ou `POST /act_<id>/adsets` (APP)
   - ⚠️ **Obrigatório incluir `targeting.targeting_automation.advantage_audience`** (0 ou 1), senão a criação falha com erro **1870227** ("sinalização de público Advantage obrigatória"). Mapa:
     - `audience.modo: ADVANTAGE_PLUS` ou `ADVANTAGE_PLUS_COM_INTERESSES` → `advantage_audience: 1`
     - targeting manual/personalizado ou público segmentado vindo do `/trafego-publicos` (interesses ou custom audiences) → `advantage_audience: 0`
   - Sob CBO, não enviar `daily_budget`/`bid_strategy` no conjunto (herda da campanha). Sob ABO, enviar.
3. **Para cada anúncio:**
   - Criar o criativo. `ads_create_creative` (MCP) ou `POST /act_<id>/adcreatives` (APP)
   - Criar o anúncio. `ads_create_ad` (MCP) ou `POST /act_<id>/ads` (APP)

Anunciar progresso por nível (`⏳ Passo 1/3: criando a campanha...`).

Tratamento de falhas:
- **Falha em criar campanha** → parar tudo, retornar erro.
- **Falha em criar conjunto** → parar, retornar erro e **não apagar nada automaticamente**. A campanha órfã fica PAUSED e sem conjunto não gasta. Oferecer: (1) corrigir e tentar criar o conjunto de novo; (2) arquivar a campanha (`ads_update_entity` com `status=ARCHIVED` no MCP, `POST /<id>` com `status=ARCHIVED` no APP), com bloco 🛡️ próprio; (3) excluir pelo Gerenciador, à mão (lacuna L4). Nunca rodar `curl -X DELETE` inline.
- **Falha em criar anúncio** → manter o que já subiu (campanha + conjuntos + anúncios anteriores), retornar erro detalhado, perguntar se quer tentar criar os anúncios restantes depois.

Não fazer rollback automático. É melhor preservar o que funcionou e deixar o aluno decidir.

Depois da criação, invalidar o cache de insights da conta (`/trafego-insights`, `sub-skills/cache.md`, seção 6.1).

Se houver `passos_manuais_pendentes` (interesses no MCP, vídeo novo, imagem a anexar), conduzir cada um agora, com os passos numerados da lacuna correspondente.

---

## 5. Output esperado após criação

```yaml
status: criado_com_sucesso | criado_parcialmente | falha
campanha:
  id: "120203456789"
  nome: "Perpétuo - Curso X - 1-1-3 - 2026-05-04"
  status: PAUSED
  ad_account_id: "act_1234567890"
  url_gerenciador: "https://business.facebook.com/adsmanager/manage/campaigns?act=1234567890&selected_campaign_ids=120203456789"

conjuntos_criados:
  - id: "120203456789001"
    nome: "AS - Advantage+ - Brasil"
    status: PAUSED

anuncios_criados:
  - id: "120203456789999"
    nome: "AD - Dor - Vídeo 30s"
    adset_id: "120203456789001"
    status: PAUSED

falhas:                                     # vazio em sucesso total
  - nivel: ad
    nome: "AD - Curiosidade - Imagem"
    motivo: "criativo bloqueou validação por texto excessivo"
    acao_sugerida: "ajustar imagem ou refazer manualmente"

passos_manuais_pendentes: []

proximos_passos:
  - "Acessar o Gerenciador no link acima"
  - "Revisar visualmente cada anúncio (preview, copy, criativo)"
  - "Quando estiver tudo certo, ativar manualmente OU me peça 'ativa a campanha'"
  - "Após 48 a 72h de veiculação, use /trafego-analise para a primeira leitura narrada e /trafego-otimizar para os ajustes"
  - "Para puxar dados de performance: /trafego-insights"

ativacao:
  status_atual: PAUSED
  pode_ativar_via_skill: true               # skill aceita comando posterior "ativa essa campanha"
```

Para mostrar a prévia visual de um anúncio criado, quando o aluno pedir: MCP `ads_get_ad_preview`; APP `GET /<ad_id>/previews?ad_format=MOBILE_FEED_STANDARD`.

---

## 6. Modo expresso. Exemplo

Aluno envia em uma mensagem só:

> "sobe campanha de venda do curso X (R$497), R$100/dia ABO, advantage+ Brasil, usa o vídeo ID 23847..., headline 'Domine X em 30 dias', CTA SHOP_NOW, URL https://meusite.com/curso-x?utm_source=fb"

Skill executa:

1. **Inferir** o que conseguir (da mensagem e do resumo do produto): objetivo `OUTCOME_SALES`, ticket R$ 497, trilha `perpetuo_low`, ABO, Advantage+ Audience, criativo existente, etc.
2. **Aplicar defaults**:
   - 1 campanha, 1 conjunto, 1 anúncio (estrutura mínima)
   - Posicionamentos Advantage+
   - `special_ad_categories: []`
   - Status PAUSED
   - Nomenclatura padrão
3. **Validar tracking**: pixel e evento, em segundo plano.
4. **Mostrar o preview completo** (resumo em texto, seção 3).
5. **Pedir aprovação única** (bloco 🛡️ do lote).
6. **Criar** após o `sim`.

Diferença essencial vs modo guia: zero perguntas intermediárias, mas o preview ainda é obrigatório.

---

## 7. Casos de borda e proteções

### 7.1 Conta sem Página ou Instagram configurado
Antes de prosseguir, conferir `FB_PAGE_ID` e `FB_INSTAGRAM_USER_ID` no `.env` (valores não sensíveis). Se algum faltar, descobrir (leitura, não é lacuna): MCP via `ads_get_ad_account_pages`; APP via `GET /act_<FB_AD_ACCOUNT_ID>/promote_pages?fields=id,name` e, para a Página escolhida, `GET /<FB_PAGE_ID>?fields=instagram_business_account{id,username}` com `curl -g`. Mostrar `Nome (ID)`, confirmar com o aluno e gravar no `.env` (é o mesmo passo da seção 6.3 da skill `trafego-conexao`).

Se faltar Instagram e o aluno não declarar Reels/Stories, criar só com a Página (Feed Facebook). Se o aluno pedir Reels/Stories sem Instagram vinculado, parar e orientar a vincular o perfil do Instagram à Página no Business Manager, depois rodar `/trafego-conexao` (opção "Validar a conexão atual") para gravar o ID.

Se a conta escolhida no Passo 0.3 do command for diferente da padrão, confirmar que a Página tem acesso a ela. Sem Página válida para a conta, a criação falha com erro 200.

### 7.2 Budget muito baixo para o ticket
Se `daily_budget < CPA target × 0.5`, avisar e pedir confirmação. Não bloquear, mas não deixar passar silencioso.

### 7.3 Mais de 5 anúncios no mesmo conjunto
Avisar: "Mais de 5 anúncios no mesmo conjunto disputam aprendizado entre si. Sugiro dividir em mais conjuntos ou priorizar 3 a 5 ângulos. Quer ajustar ou prosseguir?"

### 7.4 Criativo com texto excessivo na imagem
A Meta não rejeita mais por excesso de texto (regra antiga descontinuada), mas posicionamentos como Reels podem performar pior. Apenas avisar quando a imagem tem muito texto, sem bloquear.

### 7.5 Campanha duplicada (mesmo nome ativa há menos de 7 dias)
Avisar: "Existe campanha ativa com nome similar criada há X dias. Quer prosseguir mesmo assim, renomear, ou cancelar?"

### 7.6 Aluno pede para ativar depois de criar
Aceitar "ativa a campanha" como ação separada (não é lacuna; rotear por modo). MCP: `ads_activate_entity` (ou `ads_update_entity` com `status=ACTIVE`). APP: `POST /<campaign_id>` com `status: ACTIVE`. Passa pelo bloco 🛡️ próprio: "Vou ativar a campanha agora. Uma vez ativa, ela começa a gastar. Confirma?"

### 7.7 Conta não liberada no conector
Se uma tool do conector devolver "Ads MCP is gradually being rolled out" ou a conta vier com `is_ads_mcp_enabled: false`, parar antes de qualquer escrita, explicar em linguagem simples e oferecer o modo App pelo `/trafego-conexao`.

---

## 8. Como subir os dados (roteamento por META_AUTH_MODO)

A skill lê `META_AUTH_MODO` no `.env` e roteia **cada operação** por uma de duas vias.

> **Regra de ouro.** O modo `APP` faz tudo via curl e **nunca tem lacuna**. A noção de lacuna (e o passo manual guiado) **só existe no modo MCP**.

### 8.1 Decisão por modo

- **`APP`** → curl na Graph API v25 usando `FB_ACCESS_TOKEN_PERMANENTE` + `FB_AD_ACCOUNT_ID` (presença conferida com `grep -q`; token por substituição dentro do curl, nunca exibido). Cobre todas as operações.
- **`MCP_CONECTOR`** → tools `ads_*` do conector, descobertas pelo final do nome (ver `trafego-conexao` §5.1). Nas lacunas (vídeo novo, busca de interesse), seguir o passo manual guiado da seção "Lacunas do MCP" da skill `trafego-conexao`. Nunca montar curl com token nesse modo, mesmo que exista token antigo no `.env`.

### 8.2 Token e conta por modo

- **`APP`:** `FB_ACCESS_TOKEN_PERMANENTE` (token) e `FB_AD_ACCOUNT_ID` (conta, sem prefixo `act_`).
- **`MCP_CONECTOR`:** **nenhum token**. O `ad_account_id` exigido pelas tools vem de `FB_AD_ACCOUNT_ID` do `.env` (ou da conta escolhida no Passo 0.3 do command), passado como parâmetro da tool.
- **Nunca usar `META_ACCESS_TOKEN` nem `META_AD_ACCOUNT_ID`.** São variáveis antigas do `.env.example`, que as skills de tráfego não leem.
- Página e Instagram: `FB_PAGE_ID` e `FB_INSTAGRAM_USER_ID`. Pixel: `META_PIXEL_ID`.

### 8.3 Mapa de roteamento por operação

| Operação | Fase | Tool MCP | curl (APP) | Lacuna no MCP? |
|---|---|---|---|---|
| Listar pixels | 5.0 | `ads_get_datasets` (plano B: `ads_get_dataset_details`) | `GET /act_<id>/adspixels` | não |
| Validar evento (dados 7d) | 5.3 | `ads_get_dataset_stats` | `GET /<pixel>/stats` | não |
| Listar conversão personalizada | 5.2 | `ads_get_customconversions` | `GET /act_<id>/customconversions` | não |
| Listar públicos / lookalikes | 6.3 | `ads_get_ad_account_custom_audiences` | `GET /act_<id>/customaudiences` | não |
| **Buscar interesse por nome** | 6.2 / 6.3.3 | (sem tool: Advantage+ ou passo manual L2) | `GET /search?type=adinterest` | **sim** |
| Criar lookalike | 6.3.2 | via `/trafego-publicos` (`ads_create_custom_audience`) | via `/trafego-publicos` | não |
| Listar Páginas / Instagram | 7.1 (seção 7) | `ads_get_ad_account_pages` | `GET /act_<id>/promote_pages` | não |
| Imagem do criativo | 7.1 | `image_url` no `ads_create_creative` | `POST /act_<id>/adimages` | não (arquivo local: Fase 7.1) |
| Vídeo da biblioteca | 7.1 / 7.3 | `ads_get_ad_videos` + `video_id` no criativo | `GET /act_<id>/advideos` | não |
| **Subir vídeo novo** | 7.1 | (sem tool: passo manual L1) | `POST graph-video /act_<id>/advideos` | **sim** |
| Criar criativo | 4 | `ads_create_creative` | `POST /act_<id>/adcreatives` | não |
| Criar campanha | 4 | `ads_create_campaign` | `POST /act_<id>/campaigns` | não |
| Criar conjunto | 4 | `ads_create_ad_set` | `POST /act_<id>/adsets` | não |
| Criar anúncio | 4 | `ads_create_ad` | `POST /act_<id>/ads` | não |
| Arquivar campanha órfã | 4 | `ads_update_entity` (`ARCHIVED`) | `POST /<id>` status=ARCHIVED | não |
| Ativar campanha | 7.6 | `ads_activate_entity` / `ads_update_entity` | `POST /<id>` status=ACTIVE | não |
| Prévia do anúncio | 5 | `ads_get_ad_preview` | `GET /<ad_id>/previews` | não |

Observações:
- **Imagem por URL pública não é lacuna.** O `ads_create_creative` aceita `image_url` direto, sem upload.
- **Vídeo já na biblioteca da conta não é lacuna.** A lacuna é só o upload de um vídeo novo.
- Parâmetros de cada tool vêm do schema dela na hora da chamada, nunca de memória.

### 8.4 Limite de escopo

A skill **nunca** chama edição em campanhas existentes (pausar anúncio, mudar orçamento, duplicar conjunto). Isso é do `/trafego-otimizar` e do `/trafego-escalar`. As únicas escritas pós-criação que esta skill aceita são **ativar** a campanha recém-criada (7.6) e **arquivar** uma campanha órfã de falha na criação (seção 4), cada uma com bloco 🛡️ próprio.

---

## 9. Princípios que a skill nunca viola

1. **Sales/Leads sem pixel = não cria.** Regra dura. Otimização cega não é aceitável.
2. **Sempre PAUSED por default.** Ativação só com pedido explícito.
3. **Preview antes de criar, sempre.** Inclusive no modo expresso.
4. **Um `sim` por lote.** A criação inteira é um lote; ativação e arquivamento são operações separadas; exclusão nunca entra em lote.
5. **Liberdade de estrutura.** Skill sugere, aluno decide. Aceita estruturas customizadas.
6. **Nomenclatura padrão com override.** Default automático, aluno pode editar qualquer nível.
7. **Não cobre objetivos fora de Sales/Leads.** Se o aluno pedir Awareness, Traffic, Engagement ou App Promotion, recusar com explicação clara.
8. **Validações antes da escrita.** Pixel ativo, Página e Instagram configurados, budget coerente. Tudo verificado antes da primeira chamada de criação.
9. **Falha parcial preserva o que funcionou.** Sem rollback automático e sem exclusão automática.
10. **Não inventar IDs.** Se o aluno referenciar criativo, público ou pixel sem ID claro, listar opções e pedir confirmação.
11. **Special Ad Categories são propostas, não impostas.** Aluno confirma no preview.
12. **Modo expresso preserva preview.** Velocidade não compra atalho de segurança.
13. **Copy só via `/copy-anuncio`.** A skill nunca gera copy diretamente.
14. **O que o resumo do produto já tem não se pergunta.**
