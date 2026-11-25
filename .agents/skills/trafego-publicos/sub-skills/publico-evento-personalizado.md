# Sub-fluxo. Público por Evento Personalizado

Cria um **público personalizado** a partir de um evento personalizado do pixel. Se o aluno quiser, cria também uma **conversão personalizada** apontando para o mesmo evento (para virar coluna de relatório e objetivo de campanha).

Passo 0 (produto ativo, conexão, conta) e gate: ver `SKILL.md` desta skill.

⚠️ **Três coisas diferentes com nomes parecidos (a Meta não ajuda aqui):**

- **Evento personalizado no pixel** = o sinal que dispara quando a pessoa interage com a página (por exemplo, clica num botão). É criado **manualmente pelo aluno**: pela Ferramenta de Configuração de Eventos no Gerenciador de Eventos (Caminho 1), pelo código `fbq('trackCustom', ...)` colado no site (Caminho 2), ou já existe no pixel (Caminho 3). **A skill não cria evento personalizado pela API: a Meta não tem endpoint para registrar evento personalizado antes.** Ele nasce no primeiro disparo (`fbq trackCustom` no navegador, `POST /<pixel_id>/events` pela API de Conversões no servidor, ou a Ferramenta de Configuração de Eventos, que injeta o `fbq trackCustom` no clique). A skill só guia o aluno no caminho escolhido.
- **Público** = a lista de pessoas que dispararam o evento. **A skill cria.** É a saída principal deste sub-fluxo.
- **Conversão personalizada** = uma regra salva no Gerenciador de Eventos que aponta para o evento. **Não é necessária para o público funcionar.** Serve para usar o evento como objetivo de otimização, ver CPA por esse evento nos relatórios e achar o evento na lista de conversões personalizadas. **Só é criada se o aluno pedir** (passo 6.5).

**Página visitada, link com UTM e parâmetro de evento padrão (opções 1, 2 e 4 do passo 2) não usam evento personalizado.** Nada faz o pixel disparar um evento com nome próprio nesses casos: ele manda o `PageView` com o endereço (ou o evento padrão com o parâmetro). Por isso o público dessas opções filtra pelo evento que o pixel já manda mais o endereço ou o parâmetro (seção "2. Criar o público a partir do evento"), e o `{nome_evento}` delas serve só para dar nome ao público e à conversão. Só o clique em botão (opção 3) filtra pelo nome do evento personalizado.

## Roteamento por modo

| Parte | MCP (`MCP_CONECTOR`) | App (`curl`) |
|---|---|---|
| Listar os eventos personalizados que dispararam (Caminho 3) | `ads_get_dataset_stats` (pixel escolhido; pixels por `ads_get_datasets`) | `GET /<pixel_id>/stats?aggregation=event_total_counts` (últimos 30 dias, como no `/trafego-pixel`) |
| Marcar quais eventos já têm conversão personalizada (Caminho 3) | `ads_get_customconversions` (filtrar pela origem = pixel escolhido) | `GET /act_<id>/customconversions` |
| **Criar o público (saída principal)** | `ads_create_custom_audience` com `subtype="WEBSITE"` + `rule` | `POST /act_<id>/customaudiences` (sem `subtype`) |
| **Criar a conversão personalizada (6.5, opcional)** | passo manual guiado no Gerenciador de Eventos (seção "Conversão personalizada pelo Gerenciador") | `POST /act_<id>/customconversions` |

- **`MCP_CONECTOR`:** o público é criado pela tool normalmente. Se o aluno escolher a opção 2 do passo 6.5, a conversão personalizada é feita por ele no Gerenciador de Eventos, com o passo a passo desta sub-skill, e o público segue pela tool. Nunca montar `POST /customconversions` no modo MCP.
- O **evento personalizado no pixel** continua sendo criado manualmente pelo aluno em qualquer modo. *(Observação: as tools `ads_pixel_event_*` do MCP criam regras de evento sem código ligadas a eventos **padrão**; elas não cobrem evento personalizado com nome próprio.)*
- **`APP`:** tudo por `curl`, como nas seções abaixo.

## Perguntas que cobre

- "Crie um evento personalizado de quem clicou no botão X e um público com isso"
- "Quero um público de quem visitou a página /precos"
- "Público de quem clicou no botão do WhatsApp"
- "Público de quem chegou no checkout pelo link da bio"
- "Já configurei o evento na Meta, só cria o público usando ele"

## Inputs

| Input | Padrão | Descrição |
|---|---|---|
| `pixel_id` | primeiro pixel ativo | Pixel do evento |
| `tipo_seletor` | obrigatório | `url`, `url_param`, `url_path`, `dom_click`, `parametro_evento` |
| `via_configuracao` | obrigatório (só em `dom_click`) | `event_setup_tool`, `fbq_codigo`, `ja_configurado` |
| `valor_seletor` | obrigatório | URL, trecho de URL, UTM, nome do evento etc. |
| `nome_evento` | gerado ou anotado | Nome do evento personalizado (ex: `ClickWhatsApp`). Nas opções 1, 2 e 4 é só o nome curto do público e da conversão: não existe no pixel |
| `evento_base` | `PageView` (opções 1 e 2); perguntado na opção 4 | Evento que o pixel já manda e sobre o qual a regra do público incide (na opção 4, ex: `ViewContent`) |
| `janela_dias` | 30 | Janela do público (máximo 180 para evento do pixel) |
| `nome_audience` | gerado | Sufixo descritivo do nome |

### Tipos de seletor

| Tipo | Como funciona | Exemplo |
|---|---|---|
| `url` | URL exata visitada | `https://meusite.com/precos` |
| `url_path` | Endereço contém | `/precos` |
| `url_param` | Link contém o parâmetro | `utm_source=instagram` |
| `dom_click` | Clique em elemento, configurado pela Ferramenta de Configuração de Eventos (visual) ou pelo código `fbq trackCustom`; a skill conduz os dois caminhos e um terceiro para evento que já existe | nome do evento, ex: `ClickWhatsApp` |
| `parametro_evento` | Parâmetro enviado num evento existente | `content_name=ebook-x` |

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**. Este fluxo tem termos técnicos: toda pergunta vem com tradução em linguagem simples e exemplo.

### Ordem fixa

1. **Pixel.** Mesmo padrão de `publico-evento-padrao.md`, passo 1.

2. **O que o público deve rastrear?**
   ```
   O que esse público deve rastrear? Escolha o que mais parece com o seu caso:

   1. Pessoas que VISITARAM uma página específica do site
      (ex: a página de preços, ou /obrigado)
   2. Pessoas que VIERAM por um link específico (UTM)
      (ex: quem clicou no link da bio do Instagram com utm_source=instagram)
   3. Pessoas que CLICARAM num botão específico do site
      (ex: botão do WhatsApp, botão "Comprar agora")
   4. Pessoas que dispararam um evento padrão COM um parâmetro específico
      (ex: ViewContent do produto X, uso avançado)

   Digite o número:
   ```
   Mapeamento interno (não mostrar ao aluno):
   - 1 → `tipo_seletor: url_path` (ou `url` se o aluno colar a URL completa)
   - 2 → `tipo_seletor: url_param`
   - 3 → `tipo_seletor: dom_click` (segue para a bifurcação do passo 3)
   - 4 → `tipo_seletor: parametro_evento`

3. **Bifurcação (só na opção 3) ou valor do seletor (opções 1, 2 e 4).**

   **Opções 1, 2 ou 4:** perguntar o valor direto:
   - (1) "Qual a URL ou o pedaço dela? (ex: `/precos`, `/obrigado` ou a URL completa)"
   - (2) "Qual o UTM? (ex: `utm_source=instagram`)"
   - (4) "Qual o nome do parâmetro e o valor? (ex: `content_name=ebook-x`)"

   **Só na opção 4, na mensagem seguinte:** perguntar em qual evento o parâmetro vem (é o `evento_base` da regra):
   ```
   Esse parâmetro vem junto com qual evento do pixel?

   1. ViewContent (viu produto ou página)
   2. AddToCart (adicionou ao carrinho)
   3. InitiateCheckout (iniciou o checkout)
   4. Purchase (comprou)
   5. Lead (virou lead)
   6. Outro (digito o nome)

   Digite o número (Enter para usar 1):
   ```
   O nome do parâmetro precisa ser exatamente o que o pixel manda (mesmas maiúsculas e minúsculas). Se o aluno não tiver certeza, pedir que confira no Gerenciador de Eventos (evento → parâmetros recebidos) antes de seguir. O formato do campo na regra é conferido na conta antes do resumo ("Conferência do formato do parâmetro", na seção "2. Criar o público a partir do evento").

   Depois segue para o passo 5 (nome do evento), 6 (janela) e 7 (nome do público).

   **Opção 3 (clique em botão):**
   ```
   Para rastrear cliques num botão, o pixel precisa estar "escutando" esse botão.
   Como você quer fazer?

   1. Ferramenta de Configuração de Eventos (sem código). Eu te ensino agora:
      você seleciona o botão no próprio site, pela ferramenta da Meta, dá um nome
      ao evento e a gente continua.

   2. Linha de código no site (fbq trackCustom). Eu te dou o código pronto para
      você (ou seu programador) colar no botão. Bom se você edita o HTML do site.

   3. Já está configurado: o evento existe no pixel e só falta o público.

   Digite o número:
   ```
   Seguir para o **Caminho 1, 2 ou 3** abaixo.

4. *(não existe: a bifurcação do passo 3 substitui este passo no clique em botão; nas outras opções o fluxo vai do 3 direto para o 5)*

5. **Nome do evento.**
   - **Caminho 1:** pedir o nome exato que o aluno digitou na ferramenta, com o alerta de maiúsculas e minúsculas (ver Caminho 1).
   - **Caminho 2:** gerado a partir do nome do botão e mostrado no código.
   - **Caminho 3:** vem da escolha na lista.
   - **Opções 1, 2 e 4:** sugerir a partir do valor do seletor (ex: `ViewPrecos`, `FromInstagram`, `ViewedEbookX`) e perguntar "uso esse ou prefere outro?". Esse nome serve só para dar nome ao público e à conversão: nenhum evento com esse nome é criado no pixel, e a regra do público filtra pelo `evento_base` mais o endereço, o UTM ou o parâmetro.

6. **Janela do público.**
   ```
   Por quanto tempo a pessoa fica nesse público?

   1. 7 dias
   2. 30 dias (padrão)
   3. 60 dias
   4. 90 dias
   5. 180 dias (máximo)
   6. Outro (digito)

   Digite o número (Enter para usar 2):
   ```

6.5. **Conversão personalizada (opcional).** Vale para as 4 opções do passo 2:
   ```
   Quer que eu crie também uma CONVERSÃO PERSONALIZADA "{nome_evento}",
   que conta quem {tradução do seletor}?

   Ela NÃO é necessária para o público funcionar. Ela serve se você pretende:
   - usar esse evento como objetivo de otimização numa campanha
   - ver CPA e conversões de "{nome_evento}" nos relatórios
   - achar o evento fácil na lista de conversões personalizadas

   1. Não, criar SÓ o público (padrão, mais simples)
   2. Sim, conversão personalizada + público
      (no modo MCP, a conversão você cria no Gerenciador de Eventos, com o meu passo a passo)

   Digite o número (Enter para usar 1):
   ```

7. **Nome do público.** Sugerir `[WS] CustomEvent-{nome_evento}-{janela}d-{produto-slug}` e confirmar.

**Proibido:**
- Pedir `tipo_seletor`, `rule`, `event_source_id` ou qualquer chave da Marketing API ao aluno.
- Falar "data-attribute", "seletor CSS" ou "fbq('trackCustom')" no fluxo principal sem traduzir antes.
- Agrupar 2 ou mais inputs na mesma mensagem.

---

## Caminho 1. Ferramenta de Configuração de Eventos (sem código)

**Quando:** opção 1 da bifurcação do passo 3.

**a. URL do site.**
```
Qual a URL do site onde está o botão?
(ex: https://meusite.com/precos)
```

**b. Nome do botão (referência para a conversa).**
```
Qual o nome desse botão como ele aparece para o visitante?
(ex: "WhatsApp", "Comprar agora", "Falar com vendedor")

Esse nome é só para eu saber de qual botão estamos falando. O nome do evento
(que vai para o público) você define dentro da ferramenta da Meta no próximo passo.
```

**c. Tutorial.** Mostrar a seção "Tutorial. Ferramenta de Configuração de Eventos" abaixo.

**d. Aguardar** "feito", "pronto", "configurei" ou parecido.

**e. Pedir o nome do evento:**
```
Qual nome você deu ao evento dentro da ferramenta da Meta?
(ex: ClickWhatsApp)

⚠️ Atenção: o nome precisa ser EXATAMENTE igual ao que você digitou na ferramenta,
com as mesmas maiúsculas e minúsculas (ClickWhatsApp é diferente de clickwhatsapp).
Se ficar diferente, o público fica vazio mesmo com gente clicando.
```

**f. Seguir para o passo 6 (janela).**

---

## Caminho 2. Código fbq trackCustom

**Quando:** opção 2 da bifurcação do passo 3.

**a. Nome do evento.**
```
Qual nome você quer dar ao evento?
(ex: ClickWhatsApp, ClickComprar, ClickBio)

Esse nome vai aparecer:
   - no código que vou te passar para colar no site
   - no Gerenciador de Eventos
   - no nome do público aqui no projeto
```

**b. URL do site (obrigatória).**
```
Qual a URL da página onde o botão fica?
(ex: https://meusite.com/precos, ou https://meusite.com se o botão estiver
em todas as páginas)

Preciso disso para montar a regra da conversão personalizada: a Meta exige
evento e URL juntos (regra só com evento dá erro 1760020).
```

**c. Mostrar o código** (seção "Código fbq trackCustom" abaixo), nas 3 variações.

**d. Aviso técnico:**
```
⚠️ Importante: esse código precisa ficar DEPOIS do código do pixel no site
(o pixel costuma ser carregado no <head>). Se o código rodar antes do pixel
carregar, o clique não dispara nada. Em sites comuns isso já acontece sozinho;
em sites com framework (React, Vue, Next), confirme com quem programa o site.

Se você não tem acesso ao HTML do site, volte uma etapa e escolha o caminho 1
(ferramenta visual, sem código).
```

**e. Aguardar** "feito", "ok", "colei" ou parecido.

**f. Seguir para o passo 6 (janela).**

---

## Caminho 3. Evento já configurado no pixel

**Quando:** opção 3 da bifurcação do passo 3.

**a. Listar os eventos personalizados que dispararam no pixel** (a fonte dos nomes é o disparo, não a lista de conversões):
- MCP: `ads_get_dataset_stats` do pixel escolhido no passo 1, últimos 30 dias.
- App: `GET /<pixel_id>/stats?aggregation=event_total_counts&start_time=<30 dias atrás>&end_time=<agora>` (totais por evento, como no `/trafego-pixel`).

Tirar da lista os eventos padrão da Meta (`PageView, ViewContent, AddToCart, InitiateCheckout, AddPaymentInfo, Purchase, Lead, CompleteRegistration, Search, AddToWishlist, Contact, CustomizeProduct, Donate, FindLocation, Schedule, StartTrial, SubmitApplication, Subscribe`).

Cruzar com as conversões personalizadas da conta (MCP: `ads_get_customconversions`; App: `GET /act_<id>/customconversions?fields=name,event_source_id,custom_event_type,description,rule,creation_time&limit=100`, só as que têm origem no pixel escolhido) **só para marcar** quais eventos já têm conversão, o que permite reaproveitá-la no passo 6.5. O nome do evento sai sempre do valor de `event.eq` da `rule` da conversão, nunca do `name` dela (a conversão pode ter outro nome). Se o aluno citar uma conversão pelo nome, usar como `{nome_evento}` o `event.eq` da `rule` dela. Se essa `rule` for de um evento padrão com filtro de endereço (ex: `PageView` com "URL contém"), o caso é de página visitada: voltar ao passo 2 e seguir pela opção 1.

**b. Lista numerada:**
```
Estes são os eventos personalizados que dispararam no pixel "{nome_pixel}"
nos últimos 30 dias:

1. ClickWhatsApp     (312 disparos; já tem conversão personalizada)
2. CompraConcluida   (48 disparos)
3. ViewedPrecos      (1.204 disparos)

Qual deles o público deve usar?
Digite o número, ou o nome exato se o evento não disparou nos últimos 30 dias
e por isso não aparece na lista:
```

Se o aluno escolher a opção 2 no passo 6.5 **e** o evento não tem conversão personalizada para reaproveitar, pedir também a URL onde o evento dispara:
```
Qual a URL da página onde o evento "{nome_evento}" dispara?
(ex: https://meusite.com/precos)

A Meta exige evento e URL juntos na regra da conversão personalizada
(regra só com evento dá erro 1760020).
```

**Lista vazia:**
```
Não apareceu nenhum disparo de evento personalizado nesse pixel nos últimos
30 dias. Pode ser que o evento ainda não tenha sido criado (volte uma etapa e
escolha o caminho 1 ou 2), que o código ou a configuração tenha saído do ar,
ou que ninguém tenha clicado nesse período.

Se você tem certeza de que configurou e quer usar mesmo assim, me passe o
nome exato do evento (com as mesmas maiúsculas e minúsculas):
```

**c. Nome digitado à mão (fora da lista):** avisar que esse evento não disparou nos últimos 30 dias, então o público começa vazio e só enche quando o evento disparar.

**d. Seguir para o passo 6 (janela).**

---

## Tutorial. Ferramenta de Configuração de Eventos

**Quando:** Caminho 1. Mostrar antes de pausar o fluxo; o aluno configura na Meta e volta.

```
Vou te ensinar a abrir a Ferramenta de Configuração de Eventos no Gerenciador
de Eventos. São 4 passos, leva uns 3 minutos, e você faz direto no site da Meta.

📋 Passo 1. Entrar no Gerenciador de Eventos

   • Abra o Gerenciador de Eventos. Dois caminhos:
     - Pelo Meta Business Suite (business.facebook.com) → menu lateral →
       "Todas as ferramentas" → "Gerenciador de Eventos"
     - Direto pelo endereço: https://eventsmanager.facebook.com
   • No menu da esquerda, clique em "Conjuntos de dados"
     (antes se chamava "Fontes de dados")
   • Na lista, selecione o pixel "{nome_pixel}"

📋 Passo 2. Abrir a Ferramenta de Configuração de Eventos

   • Na tela do pixel, clique na aba "Configurações" (no topo, ao lado de
     "Visão geral", "Eventos de teste", "Ações", "Histórico")
   • Role até a seção "Configuração de eventos"
   • Clique em "Abrir a ferramenta de configuração de eventos"
   • Abre uma janela chamada "Configurar eventos"

   ⚠️ NÃO confunda com o botão verde "Adicionar eventos" da aba "Visão geral":
   ele abre outro fluxo, diferente da ferramenta visual.

📋 Passo 3. Apontar para o seu site

   • No campo "URL do site" da janela "Configurar eventos", cole:
     {url_do_aluno}
   • Clique em "Adicionar eventos" (botão azul à direita do campo)
   • Abre uma nova aba com o seu site e uma barra da Meta no topo

📋 Passo 4. Selecionar o botão e concluir

   • Na barra da Meta, clique em "Acompanhar novo botão"
   • O cursor vira uma mira: clique no botão "{nome_botao_do_aluno}"
   • A Meta pergunta que tipo de evento esse botão dispara:
     escolha "Evento personalizado"
   • Dê um nome ao evento e ANOTE exatamente como digitou: vou pedir em seguida
     e precisa bater letra por letra
   • Clique em "Concluir configuração" na barra

⏰ A "escuta" vale só para cliques a partir de agora. Cliques anteriores não voltam.

🛟 Se a tela da Meta tiver mudado e você não achar algum botão ou seção, me mande
um print que a gente resolve junto.

Quando terminar, me avise ("feito", "pronto") que eu peço o nome do evento.
```

**Se o aluno desistir:** voltar à bifurcação do passo 3 e oferecer o Caminho 2 (código) ou abandonar o clique em botão.

---

## Código fbq trackCustom

**Quando:** Caminho 2. Mostrar as 3 variações com `{nome_evento}` substituído.

```
Aqui estão 3 jeitos de colocar isso no seu site. Escolha o que combina com o
seu caso e me avise quando terminar.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Variação 1. Link <a> (ex: link do WhatsApp)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   <!-- Cole no link do WhatsApp do seu site -->
   <a href="https://wa.me/SEUNUMERO"
      onclick="fbq('trackCustom', '{nome_evento}');">
     Falar no WhatsApp
   </a>

Troque SEUNUMERO pelo seu número com código do país (ex: 5511999999999).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Variação 2. Botão <button>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   <!-- Cole no botão "Comprar agora" do seu site -->
   <button onclick="fbq('trackCustom', '{nome_evento}');">
     Comprar agora
   </button>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Variação 3. addEventListener (para quem usa framework)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Se você usa React, Vue, Next ou outro framework e não pode editar o onclick
   direto, coloque isto num script (depois do código do pixel):

   document.getElementById('meu-botao').addEventListener('click', function() {
     fbq('trackCustom', '{nome_evento}');
   });

   Troque 'meu-botao' pelo id do seu botão.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Esse código precisa ficar DEPOIS do código do pixel no site. Se rodar antes
do pixel carregar, o clique não dispara nada.

Se você não tem acesso ao HTML do site, volte uma etapa e escolha o caminho 1
(ferramenta visual, sem código).

Me avise quando colar ("feito", "ok", "colei").
```

Se a página foi gerada pelo Severino (páginas em `meus-produtos/{ativo}/entregas/paginas/`), oferecer `/pagina-pixel` para instalar o pixel e o evento na própria página.

**Se o aluno desistir do código:** voltar à bifurcação e oferecer o Caminho 1 (visual) ou o Caminho 3 (já configurado).

---

## Conversão personalizada pelo Gerenciador (modo MCP)

**Quando:** modo `MCP_CONECTOR` e opção 2 no passo 6.5. Mostrar depois que o público for criado pela tool (ou antes, se o aluno preferir).

```
O conector da Meta ainda não cria conversão personalizada. Você cria em
1 minuto no Gerenciador de Eventos:

📋 Passo 1. Abra o Gerenciador de Eventos (https://eventsmanager.facebook.com)
📋 Passo 2. No menu da esquerda, clique em "Conversões personalizadas" e depois
           em "Criar conversão personalizada"
📋 Passo 3. Preencha:
   • Nome: {nome_evento}
   • Conjunto de dados: o pixel "{nome_pixel}"
   {Clique em botão (opção 3):}
   • Evento de conversão: o evento "{nome_evento}"
     (ele só aparece na lista depois do primeiro disparo)
   • Regra: "URL contém" {trecho_estavel_da_url}
   {Página visitada ou link com UTM (opções 1 e 2):}
   • Evento de conversão: PageView
   • Regra: "URL contém" {valor_seletor} (ex: /precos ou utm_source=instagram)
   {Parâmetro de evento (opção 4):}
   • Evento de conversão: {evento_base}
   • Regra: o parâmetro {nome_parametro} igual a {valor_parametro}
📋 Passo 4. Clique em "Criar"

🛟 Se algum nome de botão estiver diferente, me mande um print.

Me avise com "feito" que eu confiro pela lista de conversões personalizadas.
```

Depois do "feito", conferir com `ads_get_customconversions` e registrar o ID da conversão no arquivo do público.

---

## Endpoints (1 ou 2 chamadas, conforme o passo 6.5)

### 1. Criar a conversão personalizada (só modo App, opção 2 no passo 6.5, e só se ainda não existir)

> No modo MCP, esta chamada não existe: o aluno cria pelo Gerenciador (seção acima). O público da chamada 2 segue normalmente pela tool.

```
POST /act_<id>/customconversions
{
  "name": "{nome_evento}",
  "event_source_id": "<pixel_id>",
  "rule": "{...regra_em_texto_json...}",
  "custom_event_type": "OTHER",
  "default_conversion_value": 0.0
}
```

> ⚠️ **`rule` é TEXTO JSON** (com aspas escapadas), não objeto JSON. No POST final ela aparece assim:
>
> ```
> "rule": "{\"and\":[{\"event\":{\"eq\":\"PageView\"}}]}"
> ```
>
> Os exemplos abaixo estão formatados para leitura; na chamada, transformar em texto. Mandar como objeto faz a Meta devolver `400 Invalid Parameter`.

**Endereço contém:**
```json
{"and": [{"event": {"eq": "PageView"}}, {"url": {"i_contains": "/precos"}}]}
```

**Clique em evento personalizado (ferramenta ou fbq trackCustom):**
```json
{"and":[{"event":{"eq":"{nome_evento}"}},{"URL":{"i_contains":"{trecho_da_url}"}}]}
```

> ⚠️ **Meta v25:** a regra precisa de **evento e URL** juntos. Só `{"event":{"eq":"..."}}` devolve `error_subcode 1760020, A conversion rule is required at creation time`. O `URL` vai **em maiúsculas** (é como a Meta guarda, mesmo com a documentação mostrando minúsculo). O `{trecho_da_url}` vem da URL coletada nos Caminhos 1, 2 ou 3 (ex: `meusite.com` ou `/precos`).

**UTM** (mesma chave de URL do "Endereço contém", com o trecho do UTM que o aluno passou):
```json
{"and": [{"event": {"eq": "PageView"}}, {"url": {"i_contains": "utm_source=instagram"}}]}
```

**Parâmetro de evento (opção 4):** o evento é o `{evento_base}` e o filtro usa o nome do parâmetro no formato conferido na conta (ver "Conferência do formato do parâmetro", na chamada 2):
```json
{"and": [{"event": {"eq": "{evento_base}"}}, {"{nome_parametro}": {"eq": "{valor_parametro}"}}]}
```
Se a Meta devolver `1760020` também aqui, parar, pedir ao aluno o trecho da URL onde o evento dispara e acrescentar o filtro de URL do exemplo do clique (`{"URL":{"i_contains":"{trecho_da_url}"}}`), mostrando o bloco 🛡️ de novo antes de tentar outra vez.

**Caminho 3:** se a conversão personalizada já existe (marcada na lista do passo a), pular esta chamada e reaproveitar.

### 2. Criar o público a partir do evento (sempre)

> MCP: `ads_create_custom_audience` com `subtype="WEBSITE"` (obrigatório na tool) e a regra abaixo. App: `curl` abaixo, **sem** `subtype`.

O público **não depende da conversão personalizada existir**. Os filtros mudam conforme o `tipo_seletor` (o resto da regra é igual):

| Opção do passo 2 | `filters` da regra |
|---|---|
| 1. Página visitada, endereço contém (`url_path`) | `[{"field":"event","operator":"eq","value":"PageView"},{"field":"url","operator":"i_contains","value":"{valor_seletor}"}]` |
| 1. Página visitada, URL completa (`url`) | igual à linha acima, com `"operator":"eq"` e a URL exata no filtro de `url` (ou `i_contains`, se o aluno aceitar variações do endereço) |
| 2. Link com UTM (`url_param`) | `[{"field":"event","operator":"eq","value":"PageView"},{"field":"url","operator":"i_contains","value":"utm_source=instagram"}]` (o trecho do UTM que o aluno passou) |
| 3. Clique em botão (`dom_click`) | `[{"field":"event","operator":"eq","value":"{nome_evento}"}]` (só aqui o público filtra pelo nome do evento personalizado) |
| 4. Parâmetro de evento (`parametro_evento`) | `[{"field":"event","operator":"eq","value":"{evento_base}"},{"field":"{nome_parametro}","operator":"eq","value":"{valor_parametro}"}]` |

Nas opções 1, 2 e 4, o `{nome_evento}` não entra na regra: ele só dá nome ao público e à conversão. Na opção 4, o valor que o aluno passou (ex: `content_name=ebook-x`) se divide em `{nome_parametro}` (`content_name`) e `{valor_parametro}` (`ebook-x`); o nome do parâmetro vai exatamente como o pixel manda, no formato de campo conferido abaixo.

#### Conferência do formato do parâmetro (opção 4, antes da primeira criação por parâmetro)

O campo do parâmetro na regra precisa estar no formato que a Meta casa com o que o pixel manda. Um formato que a Meta aceita mas não casa deixa o público vazio sem erro nenhum, e a leitura da regra gravada não pega isso (ela só repete o que foi enviado). Antes do resumo:

1. Na listagem da conta (MCP: `ads_get_ad_account_custom_audiences`; App: `GET /act_<id>/customaudiences?fields=name,subtype`), procurar um público de site (`WEBSITE`) que filtre por parâmetro de evento, de preferência criado pelo Gerenciador.
2. Ler a regra dele (MCP: `ads_get_custom_audience`; App: `GET /<audience_id>?fields=rule`) e repetir no público novo o formato do campo do parâmetro que a Meta gravou lá. São leituras: não passam pelo bloco 🛡️.
3. Sem público de referência, avisar o aluno e oferecer o Gerenciador:
   ```
   Não achei na sua conta nenhum público filtrado por parâmetro para eu copiar o
   formato que a Meta usa. Se o formato não bater, o público fica vazio sem dar
   erro. Como prefere seguir?

   1. Criar pelo Gerenciador com o meu passo a passo (mais seguro)
   2. Criar por aqui mesmo assim (formato não conferido)

   Digite o número:
   ```
   Se (1): seguir pelo "Público por parâmetro pelo Gerenciador" (abaixo). O resto do fluxo muda assim:
   - O público sai do resumo e do bloco 🛡️, porque quem cria é o aluno. Os dois ficam só com a conversão personalizada, quando o aluno pediu no passo 6.5 e o modo é App: ela é criada depois do "feito", já com o formato do campo lido no público que o aluno criou (no Preview YAML, só o `passo_1_evento`). No modo MCP, a conversão pedida segue pela "Conversão personalizada pelo Gerenciador", também sem bloco 🛡️.
   - Sem conversão para criar pelo App, não há resumo nem bloco 🛡️: nada é gravado na conta pelo Severino.
   - Depois do "feito", achar o público na listagem (MCP: `ads_get_ad_account_custom_audiences`; App: `GET /act_<id>/customaudiences?fields=name,subtype`), ler a regra dele e gravar o registro em `meus-produtos/_global/trafego/publicos/{audience_id}.md` (seção "Registro local"), com a origem "criado pelo aluno no Gerenciador", e atualizar o `INDEX.md`. Depois seguir para o resumo e o bloco 🛡️ da conversão, quando houver, e então para "Depois de criar".

   Se (2): usar `{"field":"{nome_parametro}",...}` como na tabela, registrar no arquivo do público que o formato não foi conferido e, no "Depois de criar", pedir que o aluno confira o tamanho em 24h pela opção 8; se ficar vazio com o evento disparando, recriar pelo Gerenciador.

**Público por parâmetro pelo Gerenciador:**
```
Você cria em 2 minutos no Gerenciador:

📋 Passo 1. Gerenciador de Anúncios → menu "Públicos" → "Criar público" →
           "Público personalizado"
📋 Passo 2. Escolha "Site" e clique em "Avançar"
📋 Passo 3. Origem: o pixel "{nome_pixel}"
📋 Passo 4. Eventos: "{evento_base}", refinar por parâmetro:
           {nome_parametro} igual a {valor_parametro}
📋 Passo 5. Retenção: {janela} dias
📋 Passo 6. Nome do público: {nome_audience}
📋 Passo 7. Clique em "Criar público"

🛟 Se algum nome de botão estiver diferente, me mande um print.

Me avise com "feito" que eu confiro pela listagem.
```
Depois do "feito", ler a regra do público criado no Gerenciador e usar esse formato do campo nas próximas criações por parâmetro (e na conversão personalizada pelo App, se ela foi pedida). O registro local e o resto do fluxo seguem o "Se (1)" da conferência acima.

> ⚠️ **No `curl`, NÃO enviar `subtype`.** A Meta v25 infere `subtype=WEBSITE` pela regra (`event_sources.type=pixel`). Enviar devolve `error_subcode 1870053`.

Exemplo completo (opção 1, endereço contém `/precos`):

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
          "filters": [
            {"field": "event", "operator": "eq", "value": "PageView"},
            {"field": "url", "operator": "i_contains", "value": "/precos"}
          ]
        }
      }]
    }
  }
}
```

**Depois de criar, conferir a regra gravada** (leitura, sem bloco 🛡️): `ads_get_custom_audience` no MCP ou `GET /<audience_id>?fields=rule` no App. A regra precisa trazer o evento e o filtro da tabela acima (endereço, UTM, parâmetro ou o nome do evento do clique). Se a Meta gravou outra coisa (por exemplo, sem o filtro de endereço), avisar o aluno antes de seguir, em vez de entregar um público que não vai encher. Na opção 4, essa leitura não substitui a "Conferência do formato do parâmetro" (acima).

---

## Resumo em linguagem natural (obrigatório, antes do bloco 🛡️)

```
📋 Antes de eu mexer na sua conta, um resumo:

Vou fazer {1 ou 2} coisas:

{Se opção 1 no passo 6.5, só o público:}
1️⃣ Criar um PÚBLICO de quem {tradução do seletor}
   Nome do público: "{nome_audience}"
   Janela: {janela} dias (a pessoa fica no público por esse tempo depois do evento)
   (Sem conversão personalizada agora. Dá para criar depois, se quiser usar o
    evento como objetivo de campanha.)

{Se opção 2 no passo 6.5:}
1️⃣ CONVERSÃO PERSONALIZADA "{nome_evento}"
   {Modo App:} eu crio, apontando para {o evento que você configurou pela
   ferramenta | o evento que você configurou pelo código | o evento que você já
   tinha no pixel | o evento padrão com o mesmo filtro do público (opções 1, 2 e 4)}.
   {Modo MCP:} você cria no Gerenciador de Eventos com o meu passo a passo.
   Conta quem: {tradução do seletor}.

2️⃣ PÚBLICO de quem {tradução do seletor}
   Nome: "{nome_audience}"
   Janela: {janela} dias

⏰ Importante:
   - {Clique em botão, Caminhos 1 e 2:} o público só junta pessoas a partir de
     AGORA (o evento é novo, não tem histórico).
   - {Clique em botão:} se o evento não disparar nenhuma vez, o público fica vazio.
   - {Clique em botão pelo Caminho 3, página visitada, link com UTM ou parâmetro
     de evento:} entra quem {tradução do seletor} nos últimos {janela} dias. A Meta
     calcula em até 24h. Sem {disparos do evento | visitas à página | chegadas pelo
     link | o evento {evento_base} com esse parâmetro} no pixel nesse período, o
     público começa vazio e enche conforme novas pessoas chegarem.
   - {Caminho 1:} a "escuta" já está configurada na ferramenta da Meta: o público
     deve começar a popular nos próximos cliques.
   - {Caminho 2:} confirme que o código está no site. Sem ele, o público fica
     vazio mesmo com gente clicando.

Onde aparecem:
   - {Se houver conversão:} Gerenciador de Eventos → Conversões personalizadas
   - Público: Gerenciador de Anúncios → Públicos → procurar "[WS] CustomEvent-..."
   - {Só no clique em botão:} Evento `{nome_evento}`: Gerenciador de Eventos → Visão geral do pixel

Está certo? (sim segue para a confirmação final, não cancela)
```

**Tradução obrigatória:**

| Campo técnico | Tradução |
|---|---|
| `url_path` com `/precos` | "visitou uma página com `/precos` no endereço" |
| `url` com `https://X` | "visitou exatamente a página `https://X`" |
| `url_param` com `utm_source=instagram` | "chegou pelo link com `utm_source=instagram` (ex: link da bio)" |
| `dom_click` (Caminho 1 ou 2) | "clicou no botão `{nome_botao}` do site (escuta configurada pela {ferramenta da Meta / código no site})" |
| `dom_click` (Caminho 3) | "disparou o evento `{nome_evento}` no pixel (já estava configurado)" |
| `parametro_evento` | "{ação do `evento_base`} com `{nome_parametro}` = `{valor_parametro}`" (tabela abaixo; nunca uma frase fixa) |
| `custom_event_type: OTHER` | (não mostrar) |
| `default_conversion_value: 0.0` | (não mostrar) |
| `retention_seconds: 2592000` | "30 dias" |

**Opção 4: a frase sai do `evento_base`.** Com `content_name`, o fim da frase pode virar "o produto `{valor_parametro}`". A mesma frase vai no resumo (1️⃣ e 2️⃣), na pergunta do passo 6.5 e no "Depois de criar".

| `evento_base` | Ação | Exemplo com `content_name=ebook-x` |
|---|---|---|
| ViewContent | "viu" | "viu o produto `ebook-x`" |
| AddToCart | "adicionou ao carrinho" | "adicionou ao carrinho o produto `ebook-x`" |
| InitiateCheckout | "iniciou o checkout" | "iniciou o checkout do produto `ebook-x`" |
| Purchase | "comprou" | "comprou o produto `ebook-x`" |
| Lead | "virou lead" | "virou lead com `content_name` = `ebook-x`" |
| Outro | "disparou o evento `{evento_base}`" | "disparou o evento `{evento_base}` com `content_name` = `ebook-x`" |

**Proibido no resumo:** JSON da regra, `event_source_id`, `custom_event_type`, termos `dom_*`.

---

## Preview YAML (dentro do bloco 🛡️)

```yaml
sub_fluxo: publico_evento_personalizado
caminho: event_setup_tool | fbq_codigo | ja_configurado | url | url_param | parametro_evento
modo: MCP_CONECTOR | APP

passo_1_evento:
  pixel: "{nome}"
  nome_evento: ClickWhatsApp
  tipo_seletor: dom_click
  via_configuracao: event_setup_tool       # ou fbq_codigo, ou ja_configurado
  url_aplicada: https://meusite.com        # Caminhos 1 e 2
  nome_botao: "WhatsApp"                   # Caminhos 1 e 2
  conversao_personalizada: nao_criar | criar_pela_api (App) | criar_no_gerenciador (MCP) | reutilizar_existente
  rule: { ... }

passo_2_audience:
  nome_final: "[WS] CustomEvent-ClickWhatsApp-30d-curso-tarot"
  filtro_do_publico: "evento ClickWhatsApp"   # opções 1 e 2: "PageView + endereço contém {valor}"; opção 4: "{evento_base} + {parâmetro} = {valor}"
  janela_dias: 30
  retention_seconds: 2592000
  tamanho_estimado: "calculando" (a Meta calcula em até 24h; no clique pelos Caminhos 1 e 2, começa vazio)
```

O "sim" do bloco 🛡️ vale para as duas chamadas do modo App (conversão + público), que são um lote só.

---

## Depois de criar

```
{Se houve conversão personalizada:}
✅ Conversão personalizada: ClickWhatsApp
   {criada agora | reaproveitada a que já existia | criada por você no Gerenciador}

✅ Público criado: [WS] CustomEvent-ClickWhatsApp-30d-curso-tarot

{Clique em botão, Caminhos 1 e 2:} O público começa a popular quando o evento
disparar pela primeira vez. Confira no Gerenciador de Eventos se o evento
aparece depois do primeiro disparo.
{Clique em botão pelo Caminho 3, página visitada, link com UTM ou parâmetro de
evento:} Entra quem {tradução do seletor} nos últimos {janela} dias. A Meta
calcula em até 24h; sem disparos nesse período, o público começa vazio e enche
conforme novas pessoas chegarem.
{Parâmetro de evento com formato não conferido:} Confira o tamanho em 24h pela
/trafego-publicos opção 8. Se ficar vazio com o evento disparando, a gente
recria pelo Gerenciador.

⚠️ Atenção (possível falha visual do Gerenciador):
   A tela "Editar público" pode abrir com os campos "Pixel" e "Evento" VAZIOS,
   mesmo com a regra certa guardada. Se acontecer:
   - NÃO clique em "Atualizar público" com os campos vazios.
   - Feche pelo "Cancelar" ou pelo "X".
   - Para conferir a regra real: /trafego-publicos opção 8 (Listar).

Para desfazer:
   - Conversão personalizada: Gerenciador de Eventos → Conversões personalizadas → três pontos → Excluir
   - Público: /trafego-publicos opção 8 (exclusão com confirmação própria) ou Gerenciador → Públicos
   - Evento no pixel: Gerenciador de Eventos → Configurações → Ferramenta de Configuração de
     Eventos (se foi pela ferramenta) ou tirar o código do HTML (se foi pelo código)
   (Público, conversão personalizada e evento são 3 coisas INDEPENDENTES: apagar uma
    não apaga as outras.)
```

## Registro local

Em `meus-produtos/_global/trafego/publicos/{audience_id}.md`, registrar **os dois IDs** (conversão personalizada, quando houver, e público), para o `/trafego-pixel` cruzar com a lista de eventos depois. Incluir o caminho usado (`event_setup_tool`, `fbq_codigo`, `ja_configurado`), a URL e o nome do botão quando houver.

## Avisos importantes

- **A skill não cria o evento personalizado no pixel pela API**: a Meta não tem endpoint para isso. O aluno cria pela ferramenta, pelo código ou pela API de Conversões, ou o evento já existe (Caminho 3).
- **Conversões personalizadas têm limite** de cerca de 100 por conta de anúncios (confirmado na documentação oficial). A skill avisa quando a conta passa de 80% do limite. Só se aplica se o aluno escolheu criar a conversão.
- **`rule` no `POST /customconversions` é texto JSON**, não objeto (como objeto, a Meta devolve 400).
- **Público de evento personalizado não pega histórico.** Só disparos depois da criação do evento.
- **Conversão com o mesmo nome já existe:** reaproveitar em vez de criar outra (Caminho 3, ou detecção pela listagem prévia nos outros caminhos).
- **Falha visual do Gerenciador:** nunca clicar "Atualizar público" com campos vazios. A conferência confiável é pela leitura do público.
- **Caminho 1:** o nome anotado tem que bater exatamente com o da ferramenta. Erro de digitação = público vazio sem aviso.
- **Caminho 2:** o código tem que ficar depois do código do pixel.
- **Caminho 3:** a lista vem dos disparos do pixel nos últimos 30 dias. Lista vazia quer dizer que nenhum evento personalizado disparou nesse período (evento ainda não criado, código ou configuração fora do ar, ou nenhum clique). O nome usado na regra é sempre o do evento (`event.eq` da regra da conversão), nunca o nome da conversão.
- **Opções 1, 2 e 4 (página, UTM, parâmetro):** o público filtra pelo evento que o pixel já manda mais o endereço ou o parâmetro. Filtrar por `{nome_evento}` nesses casos deixa o público vazio para sempre, porque nenhum evento com esse nome dispara.

### Origem das informações técnicas

Algumas afirmações deste arquivo são padrão operacional da Meta v25.0 observado em uso real, não citação direta da documentação pública (que tem páginas fora do ar ou incompletas):

- Janela máxima de 180 dias para público de evento do pixel
- Filtro `event eq <nome_personalizado>` direto no público (clique em botão), sem precisar de conversão personalizada
- `retention_seconds` (não `retention_days`) dentro de `rule.inclusions.rules`
- Endpoint `GET /<pixel_id>/stats?aggregation=event_total_counts` (totais por evento, o mesmo do `/trafego-pixel`)

**Conferido na documentação oficial** (sessão de 2026-05-26): endpoint `POST /act_<id>/customconversions`, campos obrigatórios e opcionais, limite de 100, `custom_event_type` OTHER válido, `rule` como texto JSON.
