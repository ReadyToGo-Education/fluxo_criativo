# Criativos e Upload. Fase 7 do /trafego-criar-campanha

Esta sub-skill aprofunda a Fase 7 (Criativos) do `/trafego-criar-campanha`. Cobre os 3 caminhos de origem do criativo, o upload real de imagem e vídeo na Marketing API, a montagem do `AdCreative` e a aplicação dos UTMs.

Toda chamada usa `v25.0`. Upload é operação de escrita, então passa pelo gate de confirmação do `CLAUDE.md`.

---

## 1. Os 3 caminhos

```
Como você quer adicionar os criativos?

1. Vou enviar arquivos agora (imagens ou vídeos)
2. Ainda não tenho criativos prontos (monto a estrutura e adiciono depois)
3. Já estão na biblioteca da conta (informo os IDs)
```

| Caminho | O que acontece | Campanha sobe? |
|---|---|---|
| 1 | Upload via API, gera `image_hash` ou `video_id` | Sim, completa |
| 2 | Estrutura sobe com `media_id: null`, anúncios ficam pendentes | Campanha e conjuntos sim, anúncios não |
| 3 | Valida os IDs informados e reusa | Sim, completa |

---

## 2. Caminho 1. Upload de arquivos novos

### 2.1 Pasta e specs

Instruir o aluno a colocar os arquivos em `meus-produtos/{ativo}/entregas/criativos/`.

| Tipo | Formatos | Limite | Resoluções recomendadas |
|---|---|---|---|
| Imagem | JPG, PNG | 30 MB | 1080x1080 (Feed quadrado), 1080x1350 (Feed vertical 4:5), 1080x1920 (Reels e Stories 9:16) |
| Vídeo | MP4, MOV | 4 GB, ideal abaixo de 1 GB | 1080x1080 ou 1080x1920. Até 60s para Reels, até 120s para Feed |

Depois da confirmação, listar o que foi encontrado na pasta com nome, formato e tamanho. Se houver mais arquivos que anúncios previstos na estrutura, perguntar quais usar.

Para gerar imagem antes de subir, encaminhar para `/criativo-estatico` ou `/img-anuncio`. Esta skill não gera criativo.

### 2.2 Upload de imagem

```
POST /v25.0/act_{ad_account_id}/adimages
Content-Type: multipart/form-data
```

Enviar o arquivo em campo cujo nome é o próprio nome do arquivo. Com `curl`:

```
curl -X POST "https://graph.facebook.com/v25.0/act_{id}/adimages" \
  -F "criativo-dor.jpg=@/caminho/criativo-dor.jpg" \
  -F "access_token={token}"
```

Retorno:

```json
{ "images": { "criativo-dor.jpg": { "hash": "a1b2c3...", "url": "https://..." } } }
```

**O que interessa é o `hash`**, não a `url`. O `hash` é o que entra em `image_hash` no `AdCreative`. Guardar a associação nome do arquivo para hash, porque o retorno é indexado pelo nome enviado.

### 2.3 Upload de vídeo

```
POST /v25.0/act_{ad_account_id}/advideos
Content-Type: multipart/form-data
```

```
curl -X POST "https://graph.facebook.com/v25.0/act_{id}/advideos" \
  -F "source=@/caminho/video-dor.mp4" \
  -F "access_token={token}"
```

Retorno: `{ "id": "1234567890" }`.

**Gate de processamento, obrigatório.** O vídeo não pode ser usado num anúncio enquanto o Meta não terminar de processar. Criar o `AdCreative` antes disso falha com erro de mídia indisponível.

```
GET /v25.0/{video_id}?fields=status
```

Aguardar `status.video_status` chegar em `ready`. Enquanto estiver em `processing`, esperar e checar de novo. Avisar o aluno que o processamento leva de alguns segundos a poucos minutos conforme o tamanho.

**Thumbnail.** `video_data` exige uma imagem de capa. Buscar as geradas pelo Meta:

```
GET /v25.0/{video_id}/thumbnails
```

Usar o `uri` do thumbnail marcado como `is_preferred`, ou perguntar ao aluno se ele quer enviar capa própria (aí sobe como imagem pelo fluxo 2.2 e usa `image_hash`).

---

## 3. Caminho 2. Sem criativos prontos

Montar o preview com `media_id: null` em cada anúncio e registrar a pendência:

```
Criativos pendentes. A campanha e os conjuntos sobem normalmente, mas os
anúncios não são criados sem mídia. Quando tiver os arquivos, coloque em
meus-produtos/{ativo}/entregas/criativos/ e me peça para subir e vincular.
```

Criar campanha e conjuntos. **Não criar anúncios.** Retornar `status: criado_parcialmente` com a pendência explícita.

---

## 4. Caminho 3. Criativos existentes na biblioteca

Se o aluno informar IDs, validar cada um antes de usar:

```
GET /v25.0/{creative_id}?fields=id,name,object_story_spec,effective_object_story_id
```

Se ele pedir a lista:

```
GET /v25.0/act_{id}/adcreatives?fields=id,name,thumbnail_url&limit=20
```

Mostrar em tabela numerada com nome junto do ID. Nunca inventar ID. Se um ID informado não existir, dizer qual falhou e oferecer a listagem.

---

## 5. Copy do anúncio

Pedir, por anúncio:

| Campo | Onde aparece | Limite prático |
|---|---|---|
| Primary text (`message`) | Corpo, acima da mídia | Cerca de 125 caracteres antes do "ver mais" |
| Headline (`name`) | Título, abaixo da mídia | Cerca de 40 caracteres |
| Description (`description`) | Subtítulo, só em alguns posicionamentos | Cerca de 30 caracteres |
| CTA (`call_to_action.type`) | Botão | Enum fechado, ver 5.1 |
| URL de destino (`link`) | Destino do clique | URL válida e ativa |

**A skill nunca escreve a copy.** Se o aluno pedir ajuda ou variações, encaminhar para `/copy-anuncio`, que aplica a Mandala da Criatividade com os 18 tipos. Voltar com o texto pronto.

### 5.1 CTAs válidos por objetivo

| Objetivo | CTAs que fazem sentido |
|---|---|
| `OUTCOME_SALES` | `SHOP_NOW`, `BUY_NOW`, `ORDER_NOW`, `GET_OFFER`, `LEARN_MORE`, `SIGN_UP` |
| `OUTCOME_LEADS` | `SIGN_UP`, `SUBSCRIBE`, `DOWNLOAD`, `LEARN_MORE`, `GET_QUOTE` |

Enviar um CTA fora do enum faz o `POST /adcreatives` falhar. Na dúvida entre dois, `LEARN_MORE` é o mais seguro e serve nos dois objetivos.

---

## 6. UTMs

**Sempre aplicados, nunca perguntados ao aluno, nunca digitados por ele.**

O campo canônico é `url_tags`, no nível do `AdCreative`. Ele mantém o `link` limpo e o Meta anexa os parâmetros na entrega, o que evita erro de concatenação e URL quebrada.

```
url_tags=utm_source=meta-ads&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}
```

Regras:

- `url_tags` **não** começa com `?` nem com `&`. Só os pares.
- Se a URL de destino já tiver query string própria, ela é preservada. O Meta faz a junção.
- Os `{{...}}` são macros dinâmicas do Meta, resolvidas na entrega. Não substituir por valores fixos.
- Nunca perguntar se o aluno quer UTM. Nunca deixar ele digitar manualmente.

---

## 7. Montagem do AdCreative

### 7.1 Criativo de imagem

```
POST /v25.0/act_{ad_account_id}/adcreatives
```

```json
{
  "name": "AD - Dor - Imagem",
  "object_story_spec": {
    "page_id": "{FB_PAGE_ID}",
    "instagram_user_id": "{FB_INSTAGRAM_USER_ID}",
    "link_data": {
      "image_hash": "a1b2c3...",
      "link": "https://meusite.com/curso-x",
      "message": "texto principal do anúncio",
      "name": "headline curta",
      "description": "descrição opcional",
      "call_to_action": {
        "type": "SHOP_NOW",
        "value": { "link": "https://meusite.com/curso-x" }
      }
    }
  },
  "url_tags": "utm_source=meta-ads&utm_campaign={{campaign.name}}|{{campaign.id}}&..."
}
```

### 7.2 Criativo de vídeo

Mesma estrutura, trocando `link_data` por `video_data`:

```json
{
  "video_data": {
    "video_id": "1234567890",
    "image_hash": "hash-da-capa",
    "message": "texto principal do anúncio",
    "title": "headline curta",
    "call_to_action": {
      "type": "SHOP_NOW",
      "value": { "link": "https://meusite.com/curso-x" }
    }
  }
}
```

Diferenças que costumam derrubar a chamada:

- Em `video_data` a headline é `title`. Em `link_data` é `name`.
- `video_data` exige capa (`image_hash` ou `image_url`). `link_data` não tem capa.
- O `link` de destino em vídeo vive só dentro de `call_to_action.value.link`.

### 7.3 Regras comuns

- `page_id` é obrigatório sempre. Sem ele a API rejeita com erro 200.
- `instagram_user_id` só é obrigatório quando houver posicionamento de Instagram, mas incluir sempre que existir melhora a apresentação do anúncio.
- O retorno traz `id`, que é o `creative_id` usado no `POST /ads`.

---

## 8. Casos de borda

| Situação | Ação |
|---|---|
| Mais de 5 anúncios no mesmo conjunto | Avisar que eles disputam aprendizado entre si e sugerir 3 a 5 ângulos. Não bloquear |
| Imagem com muito texto | Apenas avisar que Reels tende a performar pior. A regra dos 20% foi descontinuada, não bloqueia |
| Vídeo ainda em `processing` | Aguardar. Nunca criar o `AdCreative` antes de `ready` |
| Posicionamento de Instagram sem `FB_INSTAGRAM_USER_ID` | Parar e acionar `/trafego-conexao`, opção 4 |
| Arquivo acima do limite | Recusar antes de tentar o upload e pedir compressão. Upload de 4 GB que falha no fim desperdiça muito tempo |
| Upload retorna hash mas o anúncio falha | O hash é por conta de anúncio. Confirmar que o upload foi na mesma conta em que a campanha está sendo criada |
| URL de destino sem pixel instalado | Avisar que a conversão não será atribuída e oferecer `/pagina-pixel` |

---

## 9. Checklist antes de fechar a Fase 7

- [ ] Todo `image_hash` e `video_id` veio de upload real ou de ID validado na conta
- [ ] Vídeo com `video_status: ready` antes de montar o criativo
- [ ] Vídeo com capa definida
- [ ] CTA dentro do enum do objetivo da campanha
- [ ] `url_tags` montado, sem `?` inicial, com as macros intactas
- [ ] `page_id` presente em todo criativo
- [ ] Copy veio do aluno ou de `/copy-anuncio`, nunca gerada aqui
