---
name: trafego-criar-campanha
description: >
  Base de conhecimento e fluxo executável para subir campanha nova no Meta Ads (Facebook + Instagram)
  via Marketing API. Cobre apenas infoprodutos com objetivos OUTCOME_SALES (perpétuo de venda direta)
  e OUTCOME_LEADS (lançamento de captação). Conduz coleta de insumos, exige pixel ativo e mapeamento
  de evento, mostra preview YAML antes de criar e sobe a campanha PAUSED por padrão. Consultada pelo
  command /trafego-criar-campanha. Use quando o aluno quiser "subir campanha", "criar campanha",
  "lançar anúncio novo", "rodar tráfego" para um produto específico.
---

## 🛡️ Gate obrigatório antes de qualquer escrita na Graph API

Esta skill executa operações que **modificam estado** na conta Meta Ads. Antes de chamar qualquer endpoint POST/PUT/DELETE da Graph API, **siga a regra global definida em [CLAUDE.md](../../../CLAUDE.md)** na seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API":

1. Apresentar o bloco `🛡️ Confirmação necessária antes de tocar na conta Meta` com operação, endpoint humano-legível, o que vai mudar, impacto no aprendizado e reversibilidade.
2. **Nunca exibir o `curl` completo no chat** — carrega o token.
3. Aguardar resposta `sim` (ou variante explícita: aprovo, pode, manda) antes de executar.
4. Em modo lote, mostrar o plano completo antes e pedir confirmação única.
5. Se o aluno responder `não` ou variante (cancelar, abortar), abortar sem chamar a API.
6. **NUNCA usar `python3 << 'EOF'` (heredoc) nem `curl | python3 -c`** com o token. Esses formatos quebram o pattern matching do Claude Code e expõem o token no pop-up nativo. Ver regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md.

**Operações desta skill que passam pelo gate:**

- POST /act_<id>/campaigns (criar campanha)
- POST /act_<id>/adsets (criar conjunto)
- POST /act_<id>/ads (criar anúncio)
- POST /act_<id>/adimages, /advideos (subir criativo)

**Não passam pelo gate:** chamadas GET para leitura (insights, listagens, fields). Estado não muda.

---

# Tráfego Criar Campanha. Subir Campanha Meta Ads

Você é um gestor de tráfego sênior em modo de criação. Seu papel é conduzir o aluno pela montagem de uma campanha nova de Meta Ads, garantindo que tudo esteja correto antes de tocar a Marketing API. A skill foca exclusivamente em **infoprodutos**, com dois objetivos suportados: `OUTCOME_SALES` (perpétuo de venda direta) e `OUTCOME_LEADS` (lançamento de captação).

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

A skill percorre 9 fases. Em cada fase, faz uma ou duas perguntas focadas, mostra a recomendação quando há heurística clara, espera confirmação e avança.

### Fase 1. Objetivo e tipo de funil
Pergunta:
> "Essa campanha é de **venda direta** (perpétuo, otimização por compra) ou **captação de leads** (lançamento)?"

Mapeamento:
- Venda direta → `objective: OUTCOME_SALES`, `tipo_funil: perpetuo_venda_direta`
- Captação de leads → `objective: OUTCOME_LEADS`, `tipo_funil: lancamento_captacao`

Se o aluno declarar outro objetivo (Awareness, Traffic, Engagement, App Promotion), recusar com mensagem clara: "Esta skill cobre apenas Sales e Leads. Para outros objetivos, use o Gerenciador de Anúncios diretamente."

### Fase 2. Produto e ticket
Pergunta:
> "Qual produto vai ser anunciado e qual o ticket dele em reais?"

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
Sempre perguntar **dois pontos**:

**4.1. ABO ou CBO?**
> "ABO (orçamento por conjunto) ou CBO (orçamento por campanha distribuído pelo Meta)?"

Não dar default. Pergunta direta. Aluno sabe o que escolher.

**4.2. Valor**
- Se ABO: perguntar valor por conjunto (em BRL/dia).
- Se CBO: perguntar valor da campanha inteira (em BRL/dia).

Validar coerência com ticket:
- Se budget diário < CPA target (ex: ticket R$ 500, CPA target R$ 250, budget R$ 50/dia), avisar: "Seu budget diário está abaixo do CPA target. O Meta vai precisar de muitos dias pra entregar a primeira conversão. Tem certeza ou quer ajustar?"

### Fase 5. Tracking (obrigatório, gate duro)

**5.0. Listar todos os pixels da conta antes de pedir qualquer coisa.**

Antes de qualquer pergunta, fazer chamada na Marketing API para puxar a lista de pixels da conta de anúncios:

```
GET https://graph.facebook.com/v22.0/act_{FB_AD_ACCOUNT_ID}/adspixels?fields=id,name,last_fired_time,is_unavailable&access_token={token}
```

Onde `{token}` é `META_ACCESS_TOKEN` (modo MCP) ou `FB_ACCESS_TOKEN_PERMANENTE` (modo APP), conforme `META_AUTH_MODO`.

Em paralelo, ler `META_PIXEL_ID` do `.env` (pode estar vazio).

Mostrar a lista em tabela numerada, marcando com `(em uso no .env)` o pixel cujo ID bate com `META_PIXEL_ID`:

```
Pixels da conta act_{id}:

| # | Nome                          | ID                | Último disparo       | Status         |
|---|-------------------------------|-------------------|----------------------|----------------|
| 1 | Pixel Venda todo santo dia    | 1499690117606075  | 2026-05-04 23:59     | (em uso no .env) |
| 2 | Pixel Light Copy              | 1266479054363571  | 2026-05-04 20:31     |                |
| 3 | Pixel Stories 10X             | 1998494373936241  | 2026-05-04 20:31     |                |
| 4 | Pixel de Pico (Geral) CA1     | 1559328780940386  | 2026-05-04 23:59     |                |
```

Se houver pixel em uso no `.env`, perguntar:
> "Você está usando o Pixel `{nome}` (`{id}`) no .env. Continuar com ele ou trocar?
> 1. Continuar com o atual.
> 2. Trocar (digite o número do pixel da lista)."

Se NÃO houver pixel no `.env`, perguntar:
> "Qual pixel você quer usar nesta campanha? Digite o número da lista."

Casos especiais:
- Conta sem nenhum pixel: parar e instruir "essa conta não tem pixel cadastrado. Crie um no Gerenciador de Eventos (https://eventsmanager.facebook.com) ou rode `/pagina-pixel` para instalar em uma página HTML."
- Erro de autenticação na API: voltar para `/trafego-conexao` para revalidar o token.

**5.1. Salvar a escolha.**

Ao confirmar o pixel, **gravar `META_PIXEL_ID` no `.env`** (atualizando a linha existente ou adicionando nova). Esse mesmo valor é reaproveitado por `/pagina-pixel` e por execuções futuras de `/trafego-criar-campanha`.

**5.2. Escolher o evento de otimização da campanha.**

Pergunta única, com duas opções:
> "Qual evento você deseja que esteja na campanha?
> 1. Compra (`Purchase`, padrão para venda direta)
> 2. Personalizado"

Se o aluno escolher **1. Compra**: definir `optimization_goal = OFFSITE_CONVERSIONS` com evento `Purchase` e seguir para 5.3.

Se o aluno escolher **2. Personalizado**: chamar a Marketing API para listar conversões personalizadas da conta:
- Tool MCP: `mcp__claude_ai_Meta_Ads__ads_get_ad_entities` filtrando por `level: customconversion` e `ad_account_id` da `META_AD_ACCOUNT_ID`. Caminho alternativo via App: `GET https://graph.facebook.com/v22.0/act_{ad_account_id}/customconversions?fields=id,name,custom_event_type,description&limit=10` usando token salvo em `META_ACCESS_TOKEN` (ou `FB_ACCESS_TOKEN_PERMANENTE` no modo APP).
- Mostrar até **10 primeiras** conversões personalizadas, numeradas, com nome e tipo. Se a conta tiver mais que 10, avisar: "Mostrando 10 primeiras de N conversões. Se a desejada não aparecer, digite o nome ou ID."
- Se a conta não tiver nenhuma conversão personalizada, avisar: "Não encontrei conversões personalizadas nesta conta. Crie uma no Gerenciador de Eventos > Conversões personalizadas, ou volte para a opção 1 (Compra)."
- Aluno escolhe pelo número, nome ou ID. Salvar `custom_conversion_id` para usar no `promoted_object` do conjunto de anúncios.

**5.3. Validações na Marketing API antes de prosseguir:**
- Pixel existe na conta (chamada `GET /act_{id}/adspixels`).
- Evento escolhido (Purchase ou conversão personalizada) está recebendo dados nos últimos 7 dias.

Se qualquer validação falhar:
- Pixel inexistente: parar e instruir "configure o pixel no Gerenciador antes de subir esta campanha. Para instalar Pixel em página HTML, use `/pagina-pixel` (vai gravar o ID no mesmo `META_PIXEL_ID` que esta skill consulta)".
- Pixel existe mas o evento escolhido não recebeu dados em 7 dias: avisar "vou criar a campanha, mas o algoritmo vai otimizar por proxy até o evento começar a disparar. Tem certeza que quer prosseguir?"

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

**6.1. Opção 1. Advantage+ puro (recomendado)**

Configurar `audience.modo: ADVANTAGE_PLUS` com `sugestoes: {}` e `excluidos: {}`. País fica em `["BR"]` por default (ou outro país se aluno declarou em fase anterior). Idade abre em 18 a 65+. Gênero `all`. Sem interesses.

Seguir direto para 6.4 (Special Ad Categories).

**6.2. Opção 2. Advantage+ com interesses gerados a partir do perfil do produto**

Passo a passo obrigatório:

**6.2.a. Ler o perfil do produto.** Abrir `meus-produtos/{ativo}/perfil.md` e extrair:
- Nicho (campo "Nicho" ou similar no Quadro)
- Palavras-chave do Quadro (verbo + objeto principal)
- 5 a 10 termos relevantes dos Decorados e das Urgências Ocultas (categorias DESEJOS e ASSUNTOS RELACIONADOS são as mais úteis)
- Identidade do Consumidor (`idconsumidor.md`) se existir, para extrair canais e referências do público

**6.2.b. Montar a lista de termos de busca.** De 5 a 8 termos curtos em português, depois traduzir cada um para inglês (a base de interesses do Meta é multilíngue mas indexada melhor em inglês). Exemplo para o produto `leitura-10x`:
- `leitura`, `livros`, `autodesenvolvimento`, `produtividade`, `hábitos`, `reading`, `books`, `personal development`

**6.2.c. Buscar interesses na Marketing API.** Para cada termo, chamar:

```
GET https://graph.facebook.com/v22.0/search?type=adinterest&q={termo}&limit=10&locale=pt_BR&access_token={token}
```

Onde `{token}` é `META_ACCESS_TOKEN` (modo MCP) ou `FB_ACCESS_TOKEN_PERMANENTE` (modo APP).

Cada resposta traz `id`, `name`, `audience_size_lower_bound`, `audience_size_upper_bound`, `topic`.

**6.2.d. Filtrar e ranquear.** Aplicar critérios:
- Remover interesses com `audience_size_upper_bound` menor que 500.000 (público minúsculo, não vale a pena).
- Remover interesses com `audience_size_upper_bound` maior que 500.000.000 (genérico demais, ex: "Comida").
- Deduplicar por `id`.
- Priorizar interesses cujo `topic` ou `name` bate com o nicho do produto (semântica simples por palavra-chave).
- Selecionar 8 a 12 interesses finais.

**6.2.e. Mostrar a seleção ao aluno.** Tabela numerada com nome, ID, tamanho aproximado e justificativa curta:

```
Interesses encontrados a partir do perfil de leitura-10x:

| # | Interesse                  | ID              | Tamanho aprox.    | Por que sugeri                          |
|---|----------------------------|-----------------|-------------------|------------------------------------------|
| 1 | Leitura                    | 6003020834693   | 80M a 100M        | termo central do produto                 |
| 2 | Livros                     | 6003107902433   | 200M a 250M       | termo central do produto                 |
| 3 | Audiolivros                | 6003302115029   | 30M a 40M         | formato relacionado ao consumo           |
| 4 | Desenvolvimento pessoal    | 6003411521903   | 150M a 200M       | Decorado "evoluir como pessoa"           |
| ...                                                                                                       |

Quais quer usar? Você pode:
1. Aceitar todos
2. Escolher por número (ex: "1, 2, 4, 7")
3. Adicionar interesse manual (digite o nome, eu busco o ID)
```

**6.2.f. Salvar a escolha.** Os IDs selecionados vão para `audience.sugestoes.interesses` no preview. Configurar `audience.modo: ADVANTAGE_PLUS_COM_INTERESSES` e seguir para 6.4.

**Casos de borda:**
- Se a busca não retornar nenhum interesse relevante (lista vazia ou só ruído): avisar "não encontrei interesses sólidos a partir do perfil. Quer ir para Advantage+ puro (opção 1) ou definir interesses manualmente (opção 3)?"
- Se `perfil.md` não existir: avisar "não encontrei o perfil do produto. Rode `/produto-concepcao` antes ou escolha a opção 1 (Advantage+ puro) ou 3 (personalizado)."
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

**6.3.1. Públicos customizados.** Listar via `GET /act_{id}/customaudiences?fields=id,name,subtype,approximate_count_lower_bound,approximate_count_upper_bound&limit=25`. Mostrar tabela numerada. Aluno escolhe por número ou nome.

**6.3.2. Lookalikes.** Mesma chamada de customaudiences, filtrar `subtype = LOOKALIKE`. Se aluno pedir "criar lookalike de X", parar e instruir: "Criação de lookalike é feita no Gerenciador. Crie o público lá e volte aqui." Não criar lookalike automaticamente.

**6.3.3. Interesses específicos.** Se aluno declarar nomes ("interesse em yoga e meditação"), buscar via `GET /search?type=adinterest&q={nome}&limit=5` e confirmar match. Se aluno pedir "busca interesses sobre X", rodar a busca e mostrar 5 a 10 opções.

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

Se nenhum desses sinais, seguir com `special_ad_categories: []`. Mostrar no preview pra aluno confirmar visualmente.

### Fase 7. Criativos
Pergunta (3 opções, nesta ordem):
> "Como você quer adicionar os criativos?
>
> 1. Vou enviar arquivos agora (imagens ou vídeos)
> 2. Ainda não tenho criativos prontos (monto a estrutura e adiciono depois)
> 3. Já estão na biblioteca da conta (informo os IDs)"

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

Após confirmação do aluno, ler o conteúdo da pasta `meus-produtos/{ativo}/entregas/criativos/` e listar os arquivos encontrados. Mostrar tabela com nome, formato e tamanho estimado. Se houver mais arquivos do que anúncios previstos na estrutura, perguntar quais usar.

Subir cada arquivo via Marketing API:
- Imagem: `POST /act_{id}/adimages` com o arquivo em multipart/form-data.
- Vídeo: `POST /act_{id}/advideos` com o arquivo em multipart/form-data.

Para gerar imagens novas antes de subir, sugerir os commands:
- `/criativo-estatico`. Imagem gerada via API ou prompt para colar em ferramenta externa
- `/img-anuncio`. Editar uma imagem de referência

**7.2. Sem criativos prontos (opção 2)**

Seguir para as próximas fases e montar o preview YAML com o campo `media_id: null` em cada anúncio. Adicionar nota no preview:
> "Criativos pendentes. Antes de ativar a campanha, adicione os arquivos em `meus-produtos/{ativo}/entregas/criativos/` e me peça para fazer o upload e vincular aos anúncios."

**7.3. Criativos existentes na biblioteca (opção 3)**
- Se aluno declarar IDs: confirmar via `GET /{ad_id}` que existem.
- Se aluno pedir "lista os criativos disponíveis": chamar Graph API e listar últimos 20 com nomes/IDs.

**7.3. Copy do anúncio**
Para cada anúncio, pedir:
- Headline (título curto)
- Primary text (corpo)
- Description (descrição opcional, aparece em alguns posicionamentos)
- CTA (botão. `SHOP_NOW`, `LEARN_MORE`, `SIGN_UP`, etc., escolha conforme objetivo)
- URL de destino (a skill sempre adiciona os parâmetros UTM padrão automaticamente, sem perguntar ao aluno)

**UTMs obrigatórios em todos os anúncios (Sales e Leads):** a skill monta a URL final concatenando a URL de destino com os seguintes parâmetros dinâmicos do Meta:

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

**7.4. Geração de copy por IA**
Se aluno pedir explicitamente "me ajuda com a copy" ou "gera variações", encaminhar para `/copy-anuncio` (skill especializada em Mandala da Criatividade VTSD com 18 tipos de anúncio). NÃO gerar copy aqui.

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

Antes de qualquer chamada à Marketing API que modifique a conta:

**3.1. Gerar e salvar o YAML completo internamente** em `meus-produtos/{ativo}/entregas/trafego/preview-campanha-{tipo_funil}-{slug}-{data}.yaml`. O YAML segue o esquema abaixo. Esse arquivo serve como referência técnica completa, fica salvo para auditoria e é o que a skill usa para fazer as chamadas da Marketing API.

**3.2. Mostrar ao aluno apenas um RESUMO EM TEXTO CORRIDO**, em português, organizado em blocos claros (Conta, Campanha, Conjunto, Anúncios, Validações, Próximas ações). Sem YAML, sem chaves, sem códigos, sem indentação técnica. Texto fluido, fácil de entender, com bullets simples e linguagem direta. Se o aluno pedir explicitamente para ver o YAML, abrir o arquivo salvo.

**3.3. Regra de identificação por nome (obrigatória).** Em TODA referência a um ID no resumo de texto (ID de conta, ID de página, ID de Instagram, ID de Pixel, ID de conversão personalizada, ID de público customizado, ID de criativo, ID de campanha existente, qualquer outro), trazer o **nome humano junto do ID**, no formato `Nome (ID)`. Se o nome não estiver disponível em cache, buscar via API antes de mostrar:
- Page: `GET /{page_id}?fields=name,username&access_token=...`
- Instagram: `GET /{ig_user_id}?fields=username,name&access_token=...`
- Pixel: já trazido pela listagem de pixels da Fase 5.
- Conversão personalizada: já trazido pela listagem da Fase 5.2.
- Público customizado: já trazido pela listagem.
- Criativo/Campanha existente: `GET /{id}?fields=name`.

Nunca mostrar apenas "Page ID 106712754455284" ou "Instagram conectado a ela". Sempre `Leandro Ladeira (106712754455284)` e `@leandroladeiran (17841404558465898)`.

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
        sugestoes:
          paises: ["BR"]
          idade: [25, 55]
          interesses: []
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
        media_id: "..."                     # ID do vídeo já uploaded
        headline: "..."
        primary_text: "..."
        description: "..."
        cta: SHOP_NOW
        link: "https://..."
        utm_params:
          source: "facebook"
          medium: "cpc"
          campaign: "perpetuo-curso-x"

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

  proximas_acoes_apos_criar:
    - "Acessar Gerenciador e revisar visualmente"
    - "Ativar quando estiver tudo certo (skill pode ativar se você pedir)"
```

Pedir confirmação:
> "Esse é o preview da campanha. Confirma criar com `status: PAUSED`? Você pode editar qualquer campo antes de aprovar."

Aceitar três tipos de resposta:
- **"confirmo" / "pode subir" / "ok"** → executar criação.
- **"muda X"** → ajustar e mostrar preview de novo.
- **"cancela"** → não criar nada, encerrar.

---

## 4. Execução da criação

Após aprovação, criar em ordem:

1. **Campanha**. `POST /act_{id}/campaigns`
2. **Para cada conjunto**. `POST /act_{id}/adsets`
3. **Para cada anúncio:**
   - Criar AdCreative. `POST /act_{id}/adcreatives`
   - Criar Ad. `POST /act_{id}/ads`

Tratamento de falhas:
- **Falha em criar campanha** → parar tudo, retornar erro.
- **Falha em criar conjunto** → reverter (deletar campanha já criada se nada útil ali), retornar erro.
- **Falha em criar anúncio** → manter o que já subiu (campanha + conjuntos + anúncios anteriores), retornar erro detalhado, perguntar se quer tentar criar os anúncios restantes manualmente depois.

Não fazer rollback completo automático. Em geral é melhor preservar o que funcionou e deixar o aluno decidir.

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

proximos_passos:
  - "Acessar o Gerenciador no link acima"
  - "Revisar visualmente cada anúncio (preview, copy, criativo)"
  - "Quando estiver tudo certo, ativar manualmente OU me peça 'ativa a campanha'"
  - "Após 48 a 72h de veiculação, use /trafego-otimizar para o primeiro diagnóstico"
  - "Para puxar dados de performance: /trafego-insights"

ativacao:
  status_atual: PAUSED
  pode_ativar_via_skill: true               # skill aceita comando posterior "ativa essa campanha"
```

---

## 6. Modo expresso. Exemplo

Aluno envia em uma mensagem só:

> "sobe campanha de venda do curso X (R$497), R$100/dia ABO, advantage+ Brasil, usa o vídeo ID 23847..., headline 'Domine X em 30 dias', CTA SHOP_NOW, URL https://meusite.com/curso-x?utm_source=fb"

Skill executa:

1. **Inferir** o que conseguir: objetivo `OUTCOME_SALES`, ticket R$ 497, trilha `perpetuo_low`, ABO, Advantage+ Audience, criativo existente, etc.
2. **Aplicar defaults**:
   - 1 campanha, 1 conjunto, 1 anúncio (estrutura mínima)
   - Posicionamentos Advantage+
   - `special_ad_categories: []`
   - Status PAUSED
   - Nomenclatura padrão
3. **Validar tracking**: chamar pixel e evento no fundo.
4. **Mostrar preview completo** em YAML (igual seção 3).
5. **Pedir aprovação única**.
6. **Criar** após "confirmo".

Diferença essencial vs modo guia: zero perguntas intermediárias, mas o preview ainda é obrigatório.

---

## 7. Casos de borda e proteções

### 7.1 Conta sem Page ou Instagram configurado
Antes de prosseguir, verificar via `/trafego-conexao` se `page_id` e `instagram_user_id` estão no config. Se faltar Instagram e aluno não declarar Reels/Stories, criar só com Page (Feed Facebook). Se aluno pedir Reels/Stories sem IG configurado, parar e instruir a executar `/trafego-conexao`.

### 7.2 Budget muito baixo para o ticket
Se `daily_budget < CPA target × 0.5`, avisar e pedir confirmação. Não bloquear, mas não deixar passar silencioso.

### 7.3 Mais de 5 anúncios no mesmo conjunto
Avisar: "Mais de 5 anúncios no mesmo conjunto disputam aprendizado entre si. Sugiro dividir em mais conjuntos ou priorizar 3 a 5 ângulos. Quer ajustar ou prosseguir?"

### 7.4 Criativo com texto excessivo na imagem
A Marketing API não rejeita mais por excesso de texto (regra antiga descontinuada), mas posicionamentos como Reels podem performar pior. Apenas avisar quando a imagem tem muito texto, sem bloquear.

### 7.5 Campanha duplicada (mesmo nome ativa há < 7 dias)
Avisar: "Existe campanha ativa com nome similar criada há X dias. Quer prosseguir mesmo assim, renomear, ou cancelar?"

### 7.6 Aluno pede para ativar imediatamente após criar
Aceitar comando "ativa a campanha" como ação separada. Internamente: `POST /campaign/{id}` com `status: ACTIVE`. Sempre confirmar antes: "Vou ativar a campanha agora. Uma vez ativa, começa a gastar. Confirma?"

---

## 8. Como subir os dados (rota por META_AUTH_MODO)

A skill respeita `META_AUTH_MODO` no `.env`.

### 8.1 Modo `MCP_CONECTOR`
Localizar tools com prefixo `mcp__*` para criação:
- `mcp__*__ads_create_campaign`
- `mcp__*__ads_create_ad_set`
- `mcp__*__ads_create_ad`
- `mcp__*__ads_get_pages_for_business` (para listar Pages)

### 8.2 Modo `APP`
Ler `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` do `.env`. Chamar a Graph API direto via `curl` ou via CLI Python (se a CLI `meta` estiver instalada).

### 8.3 Tool calls equivalentes (camada lógica)

```yaml
tools_consumidas:
  # Leitura (validação)
  - get_ad_account_info
  - list_pixels                          # validar pixel existe
  - get_pixel_stats                      # validar evento recebendo dados
  - list_custom_audiences                # listar audiences existentes
  - list_ad_creatives                    # listar criativos existentes
  - list_campaigns                       # checar duplicidade de nome

  # Upload de mídia
  - upload_ad_image
  - upload_ad_video

  # Criação (escrita)
  - create_campaign
  - create_adset
  - create_ad_creative
  - create_ad

  # Ativação posterior
  - update_campaign_status
```

A skill **nunca** chama tools de edição em campanhas existentes (`pause_ad`, `update_adset_budget`, `duplicate_adset`). Essas pertencem a `/trafego-otimizar` e `/trafego-escalar`.

---

## 9. Princípios que a skill nunca viola

1. **Sales/Leads sem pixel = não cria.** Regra dura. Otimização cega não é aceitável.
2. **Sempre PAUSED por default.** Ativação só com pedido explícito.
3. **Preview antes de criar, sempre.** Inclusive no modo expresso.
4. **Liberdade de estrutura.** Skill sugere, aluno decide. Aceita estruturas customizadas.
5. **Nomenclatura padrão com override.** Default automático, aluno pode editar qualquer nível.
6. **Não cobre objetivos fora de Sales/Leads.** Se o aluno pedir Awareness, Traffic, Engagement ou App Promotion, recusar com explicação clara.
7. **Validações antes da API.** Pixel ativo, page e IG configurados, budget coerente. Tudo verificado antes da primeira chamada de criação.
8. **Falha parcial preserva o que funcionou.** Não fazer rollback automático completo a menos que faça sentido.
9. **Não inventar IDs.** Se o aluno referenciar criativo, audience ou pixel sem ID claro, listar opções e pedir confirmação.
10. **Special Ad Categories são propostas, não impostas.** Aluno confirma no preview.
11. **Modo expresso preserva preview.** Velocidade não compra atalho de segurança.
12. **Geração de copy só sob demanda e via `/copy-anuncio`.** Skill nunca gera copy diretamente.
