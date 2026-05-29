# Sub-fluxo. Público por Evento Personalizado

Cria uma **Custom Audience** baseada em um evento personalizado que existe no pixel. Opcionalmente, cria também uma **Conversão Personalizada** apontando pro mesmo evento (pra ele virar coluna de relatório e objetivo de campanha).

⚠️ **Distinção importante (Meta tem nomenclatura ruim aqui):**

- **Evento Personalizado no pixel** = o evento que dispara quando o usuário interage com a página (ex: clica num botão, visita uma URL, chega por UTM). Criado MANUALMENTE pelo aluno: via Ferramenta de Configuração de Eventos no Gerenciador de Eventos (Caminho 1), via snippet `fbq('trackCustom', ...)` colado no HTML (Caminho 2), ou já existe no pixel (Caminho 3). **A skill NÃO cria via API — a Meta não tem endpoint pra DEFINIR/REGISTRAR previamente um evento personalizado.** Eventos personalizados nascem implicitamente a partir do primeiro disparo (`fbq trackCustom` no navegador, `POST /<pixel_id>/events` via Conversions API server-side, ou Event Setup Tool — que injeta `fbq trackCustom` automaticamente no clique do botão). A skill apenas guia o aluno no caminho escolhido.

- **Audience** = a lista de pessoas que dispararam o evento. **A skill cria via API.** É a saída principal desta sub-skill.

- **Conversão Personalizada** = uma "regra salva" no Gerenciador de Eventos que aponta pro evento. **Não é necessária pra audience funcionar.** Habilita: aparecer na lista de Conversões Personalizadas, ser usada como objetivo de otimização de campanha, virar coluna de métrica em relatórios. **A skill cria via API SE o aluno pedir** (passo 6.5 opcional).

## Perguntas que cobre

- "Crie um evento personalizado: clicou no botão X, e crie um público com isso"
- "Quero um público de quem visitou a página /precos"
- "Público de quem clicou no botão de WhatsApp"
- "Público de quem chegou no checkout pelo link da bio"
- "Crie um público de quem visualizou meu post Y no Instagram via link"
- "Já configurei o evento no Meta, só cria a audience usando ele"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `pixel_id` | primeiro pixel ativo | Em qual pixel criar o evento |
| `tipo_seletor` | obrigatório | `url`, `url_param`, `url_path`, `dom_click`, `parametro_evento` |
| `via_configuracao` | obrigatório (só se `dom_click`) | `event_setup_tool`, `fbq_codigo`, `ja_configurado` |
| `valor_seletor` | obrigatório | Conforme tipo: URL, regex, nome do evento, etc. |
| `nome_evento` | gerado ou anotado | Nome do custom event (ex: `ClickWhatsApp`) |
| `evento_base` | `PageView` | Evento padrão sobre o qual a regra incide |
| `janela_dias` | 30 | Janela da audience (máx. 180d para evento de pixel) |
| `nome_audience` | gerado | Sufixo descritivo do nome da audience |

### Tipos de seletor suportados

| Tipo | Como funciona | Exemplo |
|---|---|---|
| `url` | URL exata visitada | `https://meusite.com/precos` |
| `url_path` | Path do URL contém | `/precos` |
| `url_param` | Query string contém | `utm_source=instagram` |
| `dom_click` | Click em elemento. Configurado via Event Setup Tool (visual) OU via código `fbq trackCustom` — a skill conduz os 2 caminhos, mais um terceiro pra evento que já existe no pixel | nome do evento, ex: `ClickWhatsApp` |
| `parametro_evento` | Parâmetro custom enviado num evento existente | `content_name=ebook-x` |

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Esse fluxo tem jargão técnico — toda pergunta vem com **tradução em linguagem natural** + exemplo concreto.

### Ordem fixa

1. **Pixel.** Mesmo padrão de `publico-evento-padrao.md` passo 1 (confirma o pixel ativo único, ou lista se houver vários).

2. **O que essa audience deveria rastrear?** Pergunta numerada em linguagem natural (sem mencionar tipo técnico):
   ```
   O que essa audience deveria rastrear? Escolha o que parecer mais com o seu caso:

   1. Pessoas que VISITARAM uma página específica do site
      (ex: a página de preços, ou /obrigado)
   2. Pessoas que VIERAM POR um link específico (UTM)
      (ex: quem clicou no link da bio do Instagram com utm_source=instagram)
   3. Pessoas que CLICARAM num botão específico do site
      (ex: botão de WhatsApp, botão "Comprar Agora")
   4. Pessoas que dispararam um evento padrão COM um parâmetro específico
      (ex: ViewContent do produto X — uso avançado)

   Digite o número:
   ```
   Mapeamento interno (não exposto ao aluno):
   - 1 → `tipo_seletor: url_path` (ou `url` se aluno colar URL completa)
   - 2 → `tipo_seletor: url_param`
   - 3 → `tipo_seletor: dom_click` (segue pra bifurcação no passo 3)
   - 4 → `tipo_seletor: parametro_evento`

3. **Bifurcação (só para opção 3 = dom_click) OU valor do seletor (opções 1, 2, 4).**

   **Se 1, 2 ou 4:** pergunta direta do valor:
   - (1): "Qual a URL ou pedaço dela? (ex: `/precos`, `/obrigado`, ou URL completa)"
   - (2): "Qual o UTM? (ex: `utm_source=instagram`)"
   - (4): "Qual o nome do parâmetro e valor? (ex: `content_name=ebook-x`)"

   Depois pula direto pro passo 5 (nome do evento) → 6 (janela) → 7 (nome da audience).

   **Se 3 (dom_click):** apresentar a bifurcação:
   ```
   Pra rastrear cliques em botões, o pixel precisa estar "escutando" esse
   botão. Como você quer fazer?

   1. Event Setup Tool (sem código) — eu te ensino agora a configurar antes
      de continuar. Você seleciona o botão visualmente no site da Meta, dá
      um nome pro evento, e a gente continua a criação da audience daí.

   2. Linha de código no site (fbq trackCustom) — eu te dou o snippet pronto
      pra você (ou seu programador) colar no botão. Bom se você edita o HTML
      do site.

   3. Já está configurado, o evento existe no pixel — só preciso criar a
      audience apontando pro nome do evento que já existe.

   Digite o número:
   ```

   Seguir pro **Caminho 1, 2 ou 3** abaixo conforme escolha.

4. **(omitido — substituído pela bifurcação do passo 3 quando dom_click; senão, segue do passo 3 direto pro 5).**

5. **Nome do evento.** Comportamento varia por caminho:
   - **Caminho 1 (Event Setup Tool):** pedir o nome exato que o aluno anotou da ferramenta da Meta, com alerta de case sensitive (ver Caminho 1 abaixo).
   - **Caminho 2 (fbq código):** auto-gerado a partir do nome do botão, mostrado no snippet.
   - **Caminho 3 (já configurado):** vem da escolha na lista de custom events.
   - **Opções 1, 2, 4:** sugerir auto-gerado a partir do valor do seletor (ex: `ViewPrecos`, `FromInstagram`, `ViewedEbookX`) e perguntar "uso esse ou prefere outro?".

6. **Janela da audience.** Numerada:
   ```
   Por quanto tempo manter a pessoa nessa audience?

   1. 7 dias
   2. 30 dias (default)
   3. 60 dias
   4. 90 dias
   5. 180 dias (máximo)
   6. Outro (digito)

   Digite o número (Enter pra usar 2):
   ```

6.5. **Conversão Personalizada (opcional).** Pergunta numerada — vale pras 4 opções do passo 2 (URL, UTM, dom_click, parâmetro de evento):
   ```
   Você quer que eu crie uma CONVERSÃO PERSONALIZADA apontando pro evento
   "{nome_evento}" junto com a audience?

   A Conversão Personalizada NÃO é necessária pra audience funcionar.
   Ela é útil se você pretende:
   - Usar esse evento como objetivo de otimização numa campanha futura
   - Ver CPA/conversões por "{nome_evento}" em relatórios do Ads Manager
   - Encontrar o evento facilmente na lista de Conversões Personalizadas

   1. Não, criar SÓ a audience (default, mais simples)
      Bom se você só quer remarketing/lookalike de quem disparou o evento.
   2. Sim, criar Conversão Personalizada + Audience
      Recomendado se você pretende otimizar campanha pra esse evento.

   Digite o número (Enter pra usar 1):
   ```

7. **Nome da audience.** Auto-gerado seguindo `[FC] CustomEvent-{nome_evento}-{janela}d-{produto-slug}` e confirmação.

**Proibido:**
- Pedir `tipo_seletor`, `rule`, `event_source_id` ou qualquer chave da Marketing API direto ao aluno.
- Falar "data-attribute", "CSS selector", "fbq('trackCustom')" no fluxo principal sem traduzir antes.
- Agrupar 2+ inputs na mesma mensagem.

---

## Caminho 1. Event Setup Tool (sem código)

**Quando dispara:** aluno escolheu opção 1 da bifurcação do passo 3.

### Sequência

**a. URL do site.** Pergunta única:
```
Qual a URL do site onde está o botão?
(ex: https://meusite.com/precos)
```

**b. Nome do botão (referência humana).** Pergunta única:
```
Qual o nome desse botão como ele aparece pro usuário?
(ex: "WhatsApp", "Comprar agora", "Falar com vendedor")

Esse nome é só pra eu identificar de qual botão a gente tá falando. O nome
do evento (que vai pra audience) você define dentro da ferramenta da Meta
no próximo passo.
```

**c. Tutorial.** Mostrar a seção `## Tutorial. Event Setup Tool (sem código)` (mais abaixo neste arquivo). O tutorial ensina a configurar o botão no Meta e instrui o aluno a anotar o nome do evento que ele criar na ferramenta.

**d. Aguardar confirmação.** Aluno responde "feito", "pronto", "configurei" ou similar.

**e. Pedir o nome do evento.** Pergunta única, com alerta importante:
```
Beleza. Qual nome você usou pro evento dentro da ferramenta da Meta?
(ex: ClickWhatsApp)

⚠️ Atenção: esse nome precisa bater EXATAMENTE com o que você digitou na
ferramenta (case sensitive — ClickWhatsApp é diferente de clickwhatsapp).
Se digitar diferente aqui, a audience fica vazia mesmo com gente clicando.
```

**f. Seguir pro passo 6 (janela)** da coleta principal.

---

## Caminho 2. Snippet fbq trackCustom (código)

**Quando dispara:** aluno escolheu opção 2 da bifurcação do passo 3.

### Sequência

**a. Nome do evento.** Pergunta única, sugerindo auto a partir do nome do botão se já foi mencionado:
```
Qual nome você quer dar pro evento?
(ex: ClickWhatsApp, ClickComprar, ClickBio)

Esse nome vai aparecer:
   - no código que vou te dar pra colar no site
   - no Gerenciador de Eventos (Conversões Personalizadas)
   - no nome da audience aqui no Workshop
```

**b. URL do site (obrigatória).** Pergunta única:
```
Qual a URL da página onde o botão fica?
(ex: https://meusite.com/precos, ou https://meusite.com se o botão estiver
em todas as páginas)

Preciso disso pra montar a regra da Conversão Personalizada — a Meta exige
evento + URL juntos (rule só com evento dá erro 1760020).
```

**c. Mostrar o snippet** (ver seção `## Snippet fbq trackCustom (código)` abaixo) com 3 variantes:
- Link `<a>` com `onclick`
- Botão `<button>` com `onclick`
- `addEventListener` em JavaScript separado (frameworks)

**d. Aviso técnico:**
```
⚠️ Importante: esse snippet precisa estar DEPOIS do código do pixel no seu
site (o pixel é carregado no <head>, geralmente). Se o snippet rodar antes
do pixel carregar, o clique não dispara nada. Em sites normais isso já
acontece automático; em sites com framework (React, Vue, Next) confirma
com seu programador.

Se você não tem acesso ao HTML do site, volta uma etapa e escolhe o
caminho 1 (Event Setup Tool — visual, sem código).
```

**e. Aguardar confirmação.** Aluno responde "feito", "ok", "colei" ou similar.

**f. Seguir pro passo 6 (janela)** da coleta principal.

---

## Caminho 3. Evento já configurado no pixel

**Quando dispara:** aluno escolheu opção 3 da bifurcação do passo 3.

### Sequência

**a. Listar custom events configurados.** Chamar:
```
GET /act_<id>/customconversions?fields=name,event_source_id,custom_event_type,description,rule&limit=100
```

Filtrar resultado pelo `event_source_id` que casa com o `pixel_id` escolhido no passo 1 da coleta.

Excluir eventos padrão do Meta (se aparecerem como custom_event_type não-CUSTOM):
`PageView, ViewContent, AddToCart, InitiateCheckout, AddPaymentInfo, Purchase, Lead, CompleteRegistration, Search, AddToWishlist, Contact, CustomizeProduct, Donate, FindLocation, Schedule, StartTrial, SubmitApplication, Subscribe`.

**b. Apresentar lista numerada.**
```
Esses são os eventos personalizados que já existem no pixel "{nome_pixel}":

1. ClickWhatsApp     — criado em 14/05/2026
2. CompraConcluida   — criado em 02/04/2026
3. ViewedPrecos      — criado em 20/03/2026

Qual deles a audience deveria usar?
Digite o número, ou digite o nome se o evento ainda não disparou e não
apareceu na lista (eventos só aparecem aqui depois do primeiro disparo):
```

**Se aluno escolher opção 2 no passo 6.5 (criar Custom Conversion) E o evento foi digitado manualmente (não veio da listagem):** pedir também a URL onde o evento dispara, antes de seguir.
```
Qual a URL da página onde o evento "{nome_evento}" dispara?
(ex: https://meusite.com/precos)

A Meta exige evento + URL juntos na regra da Conversão Personalizada
(rule só com evento dá erro 1760020).
```

**Caso a lista venha vazia** (nenhum custom event ainda), a skill avisa:
```
Não encontrei nenhum evento personalizado configurado nesse pixel. Pode
ser que você ainda não tenha criado (volta uma etapa e escolhe o caminho
1 ou 2), ou que tenha criado mas o evento ainda não disparou nenhuma vez.

Se você tem certeza que configurou e quer usar mesmo assim, me passa o
nome exato do evento (case sensitive):
```

**c. (Opcional, se aluno quiser ver quais estão disparando):** chamar:
```
GET /<pixel_id>/stats?aggregation=event&start_time=<unix_30d_atras>&end_time=<unix_agora>
```

Mostra contagem de disparos por evento nos últimos 30 dias. Útil pra confirmar que o evento está vivo. Não é obrigatório no fluxo — só se aluno perguntar.

**d. Seguir pro passo 6 (janela)** da coleta principal.

---

## Tutorial. Event Setup Tool (sem código)

**Quando dispara:** aluno escolheu Caminho 1 da bifurcação do passo 3 (dom_click).

Apresentar este tutorial **antes de pausar o fluxo**. O aluno faz a configuração no Meta paralelamente e volta pra skill quando terminar.

```
Beleza. Vou te ensinar a abrir a Ferramenta de Configuração de Eventos no
Gerenciador de Eventos. São 4 passos, leva uns 3 minutos. Você faz isso
direto no site da Meta (não aqui no chat).

📋 Passo 1. Entrar no Gerenciador de Eventos

   • Abra o Gerenciador de Eventos da Meta. Dois caminhos:
     - Pelo Meta Business Suite (business.facebook.com) → menu lateral →
       "Todas as ferramentas" → "Gerenciador de Eventos"
     - Direto pela URL: https://eventsmanager.facebook.com
   • No menu da esquerda, clique em "Conjuntos de dados"
     (antes chamava "Fontes de dados" — a Meta renomeou)
   • Na lista de pixels, selecione "{nome_pixel}"

📋 Passo 2. Abrir a Ferramenta de Configuração de Eventos

   • Na tela do pixel, clique na aba "Configurações" (no topo, ao lado de
     "Visão geral", "Eventos de teste", "Ações", "Histórico")
   • Role a página até achar a seção "Configuração de eventos"
   • Clique no botão "Abrir a ferramenta de configuração de eventos"
   • Abre um modal chamado "Configurar eventos"

   ⚠️ Atenção: NÃO confunda com o botão verde "Adicionar eventos" da
   aba "Visão geral" — esse abre outro fluxo (criar conversão personalizada
   via aplicativo conectado), que é diferente da ferramenta visual.

📋 Passo 3. Apontar pro seu site

   • No campo "URL do site" do modal "Configurar eventos", cole:
     {url_do_aluno}
   • Clique em "Adicionar eventos" (botão azul à direita do campo)
   • Abre uma nova aba com seu site + uma barra flutuante da Meta no topo

📋 Passo 4. Selecionar o botão visualmente e concluir

   • Na barra flutuante, clique em "Acompanhar novo botão"
   • O cursor vira uma "mira" — clique visualmente no botão de
     "{nome_botao_do_aluno}"
   • A Meta vai perguntar: "que tipo de evento esse botão dispara?"
     Escolha "Evento personalizado" (Custom Event)
   • Dá um nome pro evento. ANOTA esse nome exatamente como você digitou —
     vou pedir ele em seguida e tem que bater letra por letra.
   • Clique em "Concluir configuração" na barra flutuante

⏰ Detalhe importante: a "escuta" só vale pra cliques que vão acontecer a
partir de agora. Cliques que aconteceram antes não voltam.

🛟 Se a interface da Meta tiver mudado de novo e você não achar algum
botão/seção que mencionei, manda print que a gente investiga juntos
(e eu atualizo essa skill).

Me avisa aqui quando terminar ("feito", "pronto" ou similar) que aí continuo
pedindo o nome do evento que você criou na ferramenta.
```

**Se o aluno desistir** ("ah, deixa pra lá", "complicado", etc.): voltar pra bifurcação do passo 3 e oferecer Caminho 2 (código) ou abandonar dom_click.

---

## Snippet fbq trackCustom (código)

**Quando dispara:** aluno escolheu Caminho 2 da bifurcação do passo 3.

Apresentar 3 variantes do snippet com `{nome_evento}` substituído pelo nome que o aluno escolheu.

```
Beleza. Aqui estão 3 jeitos de colar isso no seu site. Escolhe o que se
encaixa melhor no seu caso e me avisa quando terminar.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Variante 1. Link <a> (ex: link de WhatsApp)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   <!-- Cole no link de WhatsApp do seu site -->
   <a href="https://wa.me/SEUNUMERO"
      onclick="fbq('trackCustom', '{nome_evento}');">
     Falar no WhatsApp
   </a>

Troque SEUNUMERO pelo seu número com código do país (ex: 5511999999999).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Variante 2. Botão <button>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   <!-- Cole no botão "Comprar Agora" do seu site -->
   <button onclick="fbq('trackCustom', '{nome_evento}');">
     Comprar Agora
   </button>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Variante 3. addEventListener (pra quem usa framework)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Se você usa React, Vue, Next ou outro framework e não pode editar onclick
   inline, coloca isso em um script (depois do código do pixel):

   document.getElementById('meu-botao').addEventListener('click', function() {
     fbq('trackCustom', '{nome_evento}');
   });

   Troque 'meu-botao' pelo id do seu botão.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Importante: esse snippet precisa estar DEPOIS do código do pixel no seu
site (o pixel é carregado no <head>). Se o snippet rodar antes do pixel
carregar, o clique não dispara nada. Em sites estáticos isso já acontece
naturalmente; em sites com framework confirma com seu programador.

Se você não tem acesso ao HTML do site, volta uma etapa e escolhe o
caminho 1 (Event Setup Tool — visual, sem código).

Me avisa quando colar ("feito", "ok", "colei") que aí continuo.
```

**Se o aluno desistir do caminho de código:** voltar pra bifurcação do passo 3 e oferecer Caminho 1 (visual) ou Caminho 3 (já configurado).

---

## Listar custom events configurados no pixel

**Quando dispara:** internamente, no Caminho 3 (passo a).

### Endpoint autoritativo (Custom Conversions configuradas)

```
GET /act_<id>/customconversions?fields=name,event_source_id,custom_event_type,description,rule,creation_time&limit=100&access_token=<TOKEN_DO_ENV>
```

**Retorno relevante:**
```json
{
  "data": [
    {
      "id": "1234567890",
      "name": "ClickWhatsApp",
      "event_source_id": "1234567890123456",
      "custom_event_type": "OTHER",
      "description": "Click no botão WhatsApp",
      "creation_time": "2026-05-14T10:30:00+0000"
    }
  ]
}
```

**Filtro:** manter só `event_source_id == pixel_id` escolhido no passo 1.

**Vantagem:** lista o que está CONFIGURADO, independente de ter disparado ou não.

### Endpoint complementar (eventos que dispararam recentemente)

```
GET /<pixel_id>/stats?aggregation=event&start_time=<unix_30d>&end_time=<unix_now>&access_token=<TOKEN_DO_ENV>
```

**Retorno:**
```json
{
  "data": [
    {"event": "ClickWhatsApp", "value": 142},
    {"event": "PageView", "value": 8421}
  ]
}
```

**Uso:** só quando o aluno pergunta "esse evento ainda tá disparando?". Não é parte do fluxo principal.

### Eventos padrão Meta a excluir

`PageView, ViewContent, AddToCart, InitiateCheckout, AddPaymentInfo, Purchase, Lead, CompleteRegistration, Search, AddToWishlist, Contact, CustomizeProduct, Donate, FindLocation, Schedule, StartTrial, SubmitApplication, Subscribe`.

---

## Endpoints (sequência de 1 ou 2 chamadas, conforme escolha no passo 6.5)

### 1. Criar Custom Conversion (SÓ se aluno escolheu opção 2 no passo 6.5 E a Conversion ainda não existe)

```
POST /act_<id>/customconversions
{
  "name": "{nome_evento}",
  "event_source_id": "<pixel_id>",
  "rule": "{...rule_em_json_string...}",
  "custom_event_type": "OTHER",
  "default_conversion_value": 0.0
}
```

> ⚠️ **Atenção:** `rule` é uma **STRING JSON** (serializada com aspas escapadas), **não objeto JSON nativo**. No payload final do POST a rule deve aparecer assim:
>
> ```
> "rule": "{\"and\":[{\"event\":{\"eq\":\"PageView\"}}]}"
> ```
>
> Os exemplos abaixo estão em JSON pretty-print só pra leitura humana — na hora da chamada, **serializar pra string** (ex: `JSON.stringify(rule)` em JavaScript, ou aspas escapadas direto no curl). Mandar como objeto JSON nativo faz a Meta retornar `400 Invalid Parameter`.

A `rule` segue formato Meta. Exemplos (pretty-print pra leitura — serializar antes de enviar):

**URL path contém:**
```json
{"and": [{"event": {"eq": "PageView"}}, {"url": {"i_contains": "/precos"}}]}
```

**Click em evento custom (Event Setup Tool ou fbq trackCustom):**
```json
{"and":[{"event":{"eq":"{nome_evento}"}},{"URL":{"i_contains":"{slug_da_url}"}}]}
```

> ⚠️ **Atenção (Meta v25.0):** a rule precisa de **evento + URL** juntos. Mandar apenas `{"event":{"eq":"..."}}` retorna `error_subcode 1760020 — A conversion rule is required at creation time`. Note que `URL` vai **em maiúsculas** (assim que a Meta armazena internamente, mesmo a doc mostrando minúsculo). O `{slug_da_url}` vem da URL coletada nos Caminhos 1, 2 ou 3 (ex: `meusite.com` ou `/precos` — qualquer pedaço estável da URL onde o botão fica).

**UTM:**
```json
{"and": [{"event": {"eq": "PageView"}}, {"utm_source": {"eq": "instagram"}}]}
```

**Caminho 3 (evento já configurado):** se a Custom Conversion já existe (apareceu na listagem), **pular esta chamada** e usar o `name` direto na audience.

### 2. Criar Custom Audience baseada no evento (sempre executada)

A audience filtra direto pelo nome do evento no pixel — **não depende da Conversão Personalizada existir**. A chamada é a mesma de `publico-evento-padrao.md`, com a `rule` apontando para o `nome_evento`:

> ⚠️ **NÃO enviar campo `subtype` no POST.** A Meta v25.0 infere `subtype=WEBSITE` automaticamente a partir da estrutura da rule (presença de `event_sources.type=pixel`). Mandar `subtype` retorna `error_subcode 1870053 — O parâmetro 'subtipo' não é aceito na versão atual da API`. Vale pra todas as audiences via pixel desta sub-skill e das suas irmãs (`publico-evento-padrao`, `publico-video-view`, `engajamento-ig-fb`).

```json
{
  "name": "{nome_audience}",
  "rule": {
    "inclusions": {
      "operator": "or",
      "rules": [{
        "event_sources": [{"id": "<pixel_id>", "type": "pixel"}],
        "retention_seconds": 2592000,
        "filter": {
          "operator": "and",
          "filters": [{
            "field": "event",
            "operator": "eq",
            "value": "{nome_evento}"
          }]
        }
      }]
    }
  }
}
```

---

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

**Quando exibir:** sempre, após coletar todos os inputs. Antes do Preview YAML.

**Formato fixo (varia leve por caminho):**

```
📋 Antes de eu mexer na sua conta, deixa eu te resumir:

Vou fazer {1 ou 2} coisas:

{Se aluno escolheu opção 1 no passo 6.5 — SÓ audience (default):}
1️⃣ Criar uma AUDIENCE baseada no evento "{nome_evento}"
   O evento dispara quando: {tradução natural do seletor}.
   Nome da audience: "{nome_audience}"
   Janela: {janela} dias (pessoa fica na audience por esse tempo após disparar o evento)
   (você optou por não criar Conversão Personalizada agora — pode criar
    depois manualmente se quiser usar como objetivo de campanha.)

{Se aluno escolheu opção 2 no passo 6.5 — Conversão Personalizada + Audience:}
1️⃣ Criar uma CONVERSÃO PERSONALIZADA chamada "{nome_evento}"
   Aponta pro evento "{nome_evento}" que você {configurou via Event Setup
   Tool / configurou via snippet fbq / já tinha no pixel (Caminho 3)}.
   O evento dispara quando: {tradução natural do seletor}.
   Vai aparecer no Gerenciador de Eventos → Conversões Personalizadas
   e permite usar como objetivo de campanha e coluna de relatório.

2️⃣ Criar uma AUDIENCE baseada nesse evento
   Nome: "{nome_audience}"
   Janela: {janela} dias (pessoa fica na audience por esse tempo após disparar o evento)

⏰ Importante:
   - A audience só começa a coletar pessoas a partir de AGORA (não pega histórico).
   - Se o evento não disparar nenhuma vez, a audience fica vazia.
   - {Se Caminho 1:} Você já configurou a "escuta" na ferramenta da Meta —
     audience deve começar a popular nos próximos cliques.
   - {Se Caminho 2:} Confirma que você colou o snippet no site. Sem o
     snippet ativo, audience fica vazia mesmo com gente clicando.

Onde elas vão aparecer:
   - {Se criou Conversão Personalizada:} Conversão Personalizada → Gerenciador de Eventos → Conversões Personalizadas
   - Audience → Gerenciador de Anúncios → Públicos → procurar "[FC] CustomEvent-..."
   - {Sempre:} Evento `{nome_evento}` → Gerenciador de Eventos → Visão Geral do pixel (lista de eventos disparados nos últimos dias)

Tá certo? (sim cria, não cancela)
```

**Regras de tradução obrigatórias:**

| Campo técnico | Tradução |
|---|---|
| `tipo_seletor: url_path`, valor `/precos` | "visitou uma página com `/precos` no endereço" |
| `tipo_seletor: url`, valor `https://X` | "visitou exatamente a página `https://X`" |
| `tipo_seletor: url_param`, valor `utm_source=instagram` | "chegou pelo link com UTM `utm_source=instagram` (ex: link da bio)" |
| `tipo_seletor: dom_click` (Caminho 1 ou 2) | "clicou no botão de `{nome_botao}` do site (a escuta foi configurada por {Event Setup Tool / código fbq})" |
| `tipo_seletor: dom_click` (Caminho 3) | "disparou o evento `{nome_evento}` no pixel (já estava configurado)" |
| `tipo_seletor: parametro_evento`, valor `content_name=ebook-x` | "visualizou o produto `ebook-x`" |
| `custom_event_type: OTHER` | (não exibir — detalhe técnico) |
| `default_conversion_value: 0.0` | (não exibir) |
| `retention_seconds: 2592000` | "30 dias" |

**Proibido:**
- Mostrar `rule` JSON, `event_source_id`, `custom_event_type` ou nomenclatura `dom_*` no resumo.
- Pular esse resumo pra ir direto pro YAML.

---

## Preview YAML

```yaml
sub_fluxo: publico_evento_personalizado
caminho: { event_setup_tool | fbq_codigo | ja_configurado | url | url_param | parametro_evento }

passo_1_evento:
  pixel: "{nome}" ({pixel_id})
  nome_evento: ClickWhatsApp
  tipo_seletor: dom_click
  via_configuracao: event_setup_tool       # ou fbq_codigo, ou ja_configurado
  url_aplicada: https://meusite.com         # se Caminho 1 ou 2
  nome_botao: "WhatsApp"                    # se Caminho 1 ou 2
  acao: { criar_custom_conversion | reutilizar_existente }
  rule: { ... }

passo_2_audience:
  nome_final: "[FC] CustomEvent-ClickWhatsApp-30d-curso-tarot"
  janela_dias: 30
  retention_seconds: 2592000
  tamanho_estimado: "calculando" (audience só popula quando o evento começar a disparar)

confirma? (digite SIM)
```

---

## Após criar

```
{Se aluno optou pela Conversão Personalizada:}
✅ Conversão Personalizada: ClickWhatsApp
   {Se criada agora:} Custom Conversion ID: 9876543210
   {Se reutilizada (Caminho 3):} Reutilizada a que já existia (ID 9876543210)

✅ Audience criada: [FC] CustomEvent-ClickWhatsApp-30d-curso-tarot
   Audience ID: 6123456790

A audience começa a popular assim que o evento dispara pela primeira vez no pixel.
Verifique no Gerenciador de Eventos se o evento aparece após o primeiro disparo.

⚠️ Atenção (possível bug visual da UI da Meta):
   Audiences criadas via API podem abrir o modal de "Editar público" com
   os campos "Pixel" e/ou "Evento" aparecendo VAZIOS, mesmo com a regra
   íntegra no banco. Já confirmado em audiences de vídeo e IG Business
   (ver publico-video-view.md e engajamento-ig-fb.md) e pode acontecer
   também em audiences de evento personalizado. Se acontecer:
   - NÃO clique em "Atualizar público" com os campos vazios — isso
     sobrescreveria a regra com vazio e quebraria a audience.
   - Fechar pelo "Cancelar" ou pelo "X".
   - Pra confirmar a regra real: /trafego-publicos opção 8 (Listar) ou
     GET /<audience_id>?fields=rule,delivery_status,operation_status.

Pra excluir se quiser:
   - {Se criou Conversão Personalizada:} Conversão Personalizada: Gerenciador de Eventos → Conversões Personalizadas → 3 pontos → Excluir
   - Audience: Gerenciador de Anúncios → Públicos → 3 pontos → Excluir
   - Evento Personalizado no pixel: Gerenciador de Eventos → Configurações → Ferramenta de Configuração de Eventos (se foi via Event Setup Tool) OU remover snippet do HTML (se foi via fbq)
   (Lembrar: Audience, Conversão Personalizada e Evento Personalizado são 3 itens INDEPENDENTES — apagar um não apaga os outros.)
```

---

## Salvar registro local

Em `meus-produtos/{ativo}/trafego/publicos/{audience_id}.md` registrar **os dois IDs**: o do custom conversion + o da audience. Para que `/trafego-pixel` possa cruzar com a listagem de eventos depois.

Incluir no registro: `caminho` usado (`event_setup_tool` / `fbq_codigo` / `ja_configurado`), URL e nome do botão se aplicável.

---

## Avisos críticos

- **A skill NÃO cria o Evento Personalizado no pixel via API** — a Meta não expõe endpoint pra isso. O evento é criado manualmente pelo aluno (Event Setup Tool / snippet fbq / Conversion API server-side) ou já existe (Caminho 3).
- **Custom Conversions consomem cota** da conta (limite ~100 por ad account, confirmado na doc oficial). A skill avisa quando a conta passa de 80% do limite. **Só dispara se o aluno optou por criar Conversão Personalizada no passo 6.5.**
- **`rule` no POST /customconversions é STRING JSON serializada**, não objeto JSON nativo (ver nota nos Endpoints). Confirmado na doc oficial — se passar como objeto, Meta retorna 400.
- **Audiences geradas por custom event não populam retroativamente.** Só pegam disparos após a criação do evento.
- **Se a Conversão Personalizada já existe** no pixel (mesmo nome) e o aluno optou por criar, a skill **reutiliza** em vez de criar nova (Caminho 3 explícito, ou detecção automática nos outros caminhos via listagem prévia de `customconversions`).
- **Bug visual da UI da Meta — pode afetar audiences de evento personalizado.** Confirmado em vídeo e IG Business (modal de edição abrindo com campos vazios). Estruturalmente o mesmo padrão (POST `customaudiences` com `rule.inclusions.event_sources` + `filter`) é usado aqui, então pode ocorrer. **Nunca clicar "Atualizar público" com dropdowns vazios** — sobrescreve a regra. Critério de saúde confiável é a API.

### Notas de proveniência (transparência técnica)

Algumas afirmações desta sub-skill são **padrão operacional Meta v25.0 baseado em uso real**, não em citação direta da doc pública (que está mal indexada e muitas URLs retornam 404 ou vêm truncadas via WebFetch):

- Janela máx 180 dias para audience baseada em evento de pixel
- Filter `event eq <nome_custom>` direto na audience, sem precisar de Custom Conversion prévia
- Formato `retention_seconds` (não `retention_days`) dentro de `rule.inclusions.rules`
- Endpoint `GET /<pixel_id>/stats?aggregation=event`

Se a Meta mudar algum desses no futuro, a skill precisa de update. Quando o aluno testar ao vivo e algo retornar erro, atualizar memória persistente com a pegadinha descoberta.

**Validado na doc oficial** (em sessão de 2026-05-26): endpoint `POST /act_<id>/customconversions`, campos obrigatórios/opcionais, limite de 100, enum `custom_event_type` (OTHER válido), `rule` como string JSON serializada.
- **Caminho 1 (Event Setup Tool):** o nome do evento que o aluno anota DEVE bater exatamente com o que ele digitou na ferramenta da Meta (case sensitive). Erro de digitação aqui = audience vazia silenciosa.
- **Caminho 2 (fbq código):** snippet precisa estar depois do código do pixel no HTML. Em frameworks (React/Vue/Next), garantir que o pixel já carregou antes do botão renderizar.
- **Caminho 3 (já configurado):** se a listagem `customconversions` vier vazia, pode ser que o evento foi criado em outro ad account (cada ad account tem suas próprias Conversions, mesmo apontando pro mesmo pixel).
