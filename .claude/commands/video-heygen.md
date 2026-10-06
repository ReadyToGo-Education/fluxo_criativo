---
name: workshop-marketing:video-heygen
description: Criar video com avatar IA usando HeyGen com multiplas cenas, avatares rotacionados, backgrounds variados e direcao visual baseada em dados reais (Apify/dashboard) ou Urgencias Ocultas do perfil. Entrega video pronto com cenas diferentes, nao mais "avatar falando em fundo branco".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebFetch, AskUserQuestion, Skill, mcp__Claude_in_Chrome__tabs_context_mcp, mcp__Claude_in_Chrome__tabs_create_mcp, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__read_page, mcp__Claude_in_Chrome__get_page_text, mcp__Claude_in_Chrome__find, mcp__Claude_in_Chrome__form_input, mcp__Claude_in_Chrome__computer
model: opus
---

# Video com Avatar IA (HeyGen). Multi-Cena, Multi-Avatar, Multi-Background

Cria videos com avatar IA que NAO sao "avatares falando em fundo branco". Cada video e quebrado em 3 a 5 cenas, com combinacao de avatar, voz e background por cena, alinhada ao tipo de anuncio da Mandala VTSD e a direcao visual baseada em dados reais (dashboard/Apify) ou Urgencias Ocultas do perfil.

## O que mudou em relacao a versao antiga

1. **Multiplas cenas por video** usando o array `video_inputs` da API.
2. **Background configurado por cena** (cor solida, imagem ou video de b-roll) via campo `background`.
3. **Rotacao de avatares** quando fizer sentido (2 avatares no mesmo video, tipo corte entre narrador e testemunho).
4. **Pesquisa visual previa** inspirada na skill `criativo-estatico` para descobrir referencias virais do nicho antes de montar a direcao das cenas.
5. **Mapeamento Mandala para direcao visual**: cada um dos 18 tipos de anuncio tem sugestao automatica de cor, ritmo, tipo de background e combinacao de avatares.
6. **Variacao entre videos**: quando o usuario gera varias pecas da mesma campanha, a skill evita repetir a mesma combinacao de avatar + background.

## REGRA DE CUSTO

Este fluxo usa 1 API paga: HeyGen (~US$ 0,50/min de video). Cada cena adicional NAO gera cobranca extra, consome segundos do mesmo orcamento.

## Principios do Novo Fluxo

1. **Roteiro em cenas, nao em bloco.** O roteiro vira um array de 3 a 5 cenas antes de virar payload.
2. **Cada cena tem funcao narrativa.** Gancho, problema, virada, prova, CTA. Nao e so quebrar por tempo.
3. **Background nunca e branco liso.** Default da skill e cor solida da marca. Branco so se a direcao visual do Passo 3 mostrar que o nicho usa (ex: maternidade clean).
4. **Direcao visual vem da Mandala + pesquisa.** O tipo de anuncio define a base. A pesquisa viral ajusta ao tom atual do nicho.
5. **Produto nao aparece no lead.** Mesma regra VTSD. A Cena 1 fala da dor, desejo ou transformacao do leitor, nunca do produto.

## Regras de Copy Inegociaveis (aplicar em TODO texto do avatar)

- Nunca travessao
- Nunca ponto de exclamacao
- Nunca pergunta no gancho
- Nunca "Nao e X. E Y."
- Nunca mencionar o produto na cena 1
- Linguagem falada, frases curtas, pausas naturais
- Usar 1 a 3 elementos literarios por video (consultar skill `elementos-literarios`)

Antes de enviar qualquer texto para o payload, fazer varredura final eliminando esses itens.

---

## PASSO 0. Verificar Configuracao

Leia `.env` e verifique se `HEYGEN_API_KEY` existe e tem valor.

**Se a chave existir**, pule para o Passo 1.
**Se NAO tiver a chave**, conduza o setup interativo (mesmo fluxo da versao antiga):

Pergunte:

```
Para criar videos com avatar IA, voce precisa de uma conta no HeyGen.

Voce ja tem conta no HeyGen?

1. Sim, tenho conta e plano Creator (ou superior)
2. Sim, mas estou no plano gratuito
3. Ainda nao tenho conta

Digite o numero:
```

Se opcao 1: guie a pegar a chave em app.heygen.com > Settings > API > Create API Key (Key Name: "Workshop Marketing", tipo: "Agent"). O usuario cola a chave no chat e a skill salva no `.env` com Edit. O usuario NUNCA abre o `.env` manualmente.

Se opcao 2: explique que o plano gratuito nao libera API. Recomendar plano Creator (US$ 24/mes anual). Depois seguir como opcao 1.

Se opcao 3: guiar a criar conta em heygen.com, testar gratis, depois upgrade e gerar a chave.

**Teste de conexao:**

```bash
curl -s "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $(grep HEYGEN_API_KEY .env | cut -d= -f2)" \
  | head -c 500
```

Se retornar avatares: "Conexao funcionando."
Se 401: "Chave invalida. Verifique se copiou sem espacos extras."
Se 403: "Sua conta nao tem acesso a API. Precisa do plano Creator ou superior."

---

## PASSO 1. Contexto do Produto

Leia, na ordem:

1. `meus-produtos/.ativo` (identificador do produto ativo)
2. `meus-produtos/{ativo}/resumo-produto.md` (resumo do produto; se não existir, gerar conforme "Contexto Persistente do Negócio" no CLAUDE.md) → Quadro, Furadeira, Decorados principais, Urgências Ocultas, identidades e público

Se faltar produto ativo ou perfil, pare e oriente o usuario a rodar `/produto-novo` ou `/produto-concepcao` primeiro.

---

## PASSO 2. Definir o Tipo da Mandala

**Pergunta 1.** E perpetuo ou pico de vendas?

**Pergunta 2.** Qual o objetivo?

```
1. Descoberta (atrair quem nao conhece)
2. Relacionamento (engajar base)
3. Conversao (vender)
4. RMKT (reconquistar quem viu a pagina)
```

**Pergunta 3.** Qual tipo da Mandala?

```
Qual tipo de anuncio combina com a mensagem?

1. Comparacao
2. Problema/Solucao
3. Explicacao
4. Curiosidade
5. Reflexao
6. Certo/Errado
7. Demonstracao
8. Procedimento
9. Impacto Visual
10. Oportunidade
11. Historia
12. Prova Social
13. Clickbait
14. Sensacao
15. Contraste
16. Ensino
17. Revelacao
18. Dilema

(Se nao souber, digite 0 que eu sugiro 3 baseados no produto)
```

Guardar na sessao: `tipo_mandala`, `objetivo`, `momento`.

---

## PASSO 3. Direcao Visual

Antes de escrever o roteiro, defina a direcao visual do video. O fluxo tem dois caminhos: o padrao (sempre funciona) e o avancado (dados reais do Instagram, recomendado).

### Caminho padrao. Dados existentes + Urgencias Ocultas

**Primeiro, verifique se ja tem dados do nicho no produto ativo:**

1. `meus-produtos/{ativo}/entregas/instagram-dashboard/insights.json` (dashboard do Instagram)
2. `meus-produtos/{ativo}/entregas/instagram-dashboard/imagens/` (thumbnails dos posts)
3. `meus-produtos/{ativo}/entregas/dados-nicho*.md` (relatorio do /dados-nicho)

**Se `insights.json` existir e tiver menos de 30 dias:**

- Leia os posts com maior engajamento (top 6 por likes + comentarios).
- Se a pasta `imagens/` existir com as thumbnails, leia as imagens dos top 6 posts para extrair paleta, composicao e estilo visual real.
- Se so tiver o JSON sem imagens, use as legendas e tipos de post (Reel, Foto, Carrossel) para inferir o ritmo e estilo dominante do nicho.
- Extraia os 4 elementos (ver abaixo) e siga para o resumo.

**Se `dados-nicho*.md` existir:** leia o relatorio e extraia padroes visuais mencionados (tipos de conteudo, estilos, formatos que dominam no nicho).

**Se não tiver nenhum dado externo**, derive a direção visual do que já existe no `resumo-produto.md`:

1. Leia as **Urgencias Ocultas** (dores, desejos, urgencias quentes).
2. Leia as **3 Identidades** (comunicador, consumidor, produto).
3. Combine com a **tabela da Mandala** do Passo 5 (linha do tipo escolhido no Passo 2) para derivar a direcao visual.

Regras de derivacao:

- **Paleta:** use as cores da marca do resumo-produto.md. Se não tiver, use a paleta base da tabela da Mandala para o tipo escolhido.
- **Ritmo:** se o publico e jovem ou o nicho e dinamico (fitness, marketing, tech), corte rapido. Se e reflexivo ou premium (terapia, coaching executivo, investimentos), corte lento.
- **Cenario:** derive do contexto das dores. Se as dores mencionam "escritorio", "computador", "rotina", o cenario e interno profissional. Se mencionam "corpo", "espelho", "academia", o cenario e lifestyle.
- **Retencao:** use a urgencia quente mais forte como base do gancho visual (rosto + frase de impacto derivada da urgencia).

### Caminho avancado (recomendado). Apify + analise visual real

Se o caminho padrao usou apenas Urgencias Ocultas (sem dados do dashboard ou dados-nicho), verifique se `APIFY_API_TOKEN` existe no `.env`.

**Se o token existir**, oferca ao usuario:

```
Pra deixar a direcao visual mais precisa, posso analisar os posts reais de 2 a 3 perfis de referencia do seu nicho. Isso me da a paleta de cores, ritmo e estilo que ta funcionando agora no Instagram.

Quer usar essa opcao?

1. Sim, quero (vou informar os perfis)
2. Nao, segue com o que ja tem

Digite o numero:
```

Se opcao 1: pergunte os perfis e siga o fluxo abaixo.
Se opcao 2: siga para o resumo com os dados do caminho padrao.

**Se o token NAO existir**, mencione a opcao sem travar o fluxo:

```
Dica: se voce configurar o Apify (/configurar-apify), da proxima vez eu consigo analisar os posts reais dos concorrentes pra definir cores e estilo do video com mais precisao. Por enquanto, vou usar as Urgencias Ocultas do seu produto.
```

E siga para o resumo.

**Fluxo do Apify (quando o usuario aceitar):**

1. Pergunte os perfis:

```
Quais perfis do Instagram sao referencia no seu nicho?
(ex: @fulano, @ciclano, @beltrano)
```

2. Use o Apify Instagram Scraper para cada perfil:

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token=$APIFY_API_TOKEN&timeout=120" \
  -H "Content-Type: application/json" \
  -d '{
    "directUrls": ["https://www.instagram.com/{perfil}/"],
    "resultsType": "posts",
    "resultsLimit": 12
  }'
```

3. Dos posts retornados, baixe as thumbnails dos 6 com mais engajamento:

```bash
curl -s -o "thumbnail_{n}.jpg" "{displayUrl}" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://www.instagram.com/"
```

4. Leia as imagens baixadas com o Read (Claude e multimodal) e analise visualmente: paleta de cores dominante, composicao, tipo de cenario, presenca de texto sobreposto, estilo de iluminacao.

5. Extraia os 4 elementos e siga para o resumo.

### Os 4 elementos que toda fonte deve extrair

Independente do caminho usado, o resultado final e sempre:

- **Paleta dominante.** 2 a 3 cores HEX que definem o tom visual do video.
- **Ritmo.** Cortes rapidos (menos de 2s por cena) ou lentos (mais de 4s por cena).
- **Tipo de cenario.** Interno neutro, ambiente real, grafico/texto em tela, ou mistura.
- **Elemento de retencao.** O que segura nos primeiros 2 segundos (rosto + texto grande, b-roll + voz off, etc).

### Resumo para o usuario

Guarde em memoria da sessao como `pesquisa_visual`. Mostre ao usuario:

```
Direcao visual definida. Resumo:

- Fonte: [insights.json do dashboard / Apify @perfil1 @perfil2 / Urgencias Ocultas do perfil]
- Paleta: [cores HEX]
- Ritmo: [corte rapido / lento]
- Cenario: [descricao]
- Gancho visual: [descricao]

Vou usar isso para montar as cenas.
```

---

## PASSO 4. Roteiro

O usuario pode fornecer o roteiro de 3 formas. O diferencial da nova versao: o roteiro SEMPRE vira cenas, nunca bloco unico.

### Opcao A. Texto colado
O usuario cola o texto. Siga para o Passo 5.

### Opcao B. Link de video
Use `tabs_context_mcp` + `navigate` + `get_page_text` para extrair legenda. Confirme com o usuario se o audio bate com a legenda. Nao mande o usuario sair do chat para transcrever. Siga para o Passo 5.

### Opcao C. Criar do zero (integrado com Mandala)
Gere roteiro VTSD do tipo escolhido no Passo 2:

```
[0-2s]   GANCHO      Premissa contra-intuitiva baseada em Urgencia Oculta do perfil.
[3-5s]   TEASE       Frase que expande o gancho.
[6-25s]  ENTREGA     Ensina/demonstra/conta a historia real.
[26-30s] REGANCHO    Sintese da ideia central.
[31-35s] CTA         Convite compativel com o objetivo.
```

Aplicar as regras de copy inegociaveis (topo deste arquivo).

**Mostrar roteiro ao usuario e pedir aprovacao:**

```
Roteiro do video:

---
[texto completo com marcacoes de tempo]
---

Duracao estimada: ~[X] segundos ([Y] palavras)

1. Aprovar roteiro
2. Quero ajustar algo
```

---

## PASSO 5. Quebra em Cenas (CORE DA CORRECAO)

Este e o passo que resolve o "video todo igual". Pegue o roteiro aprovado e quebre em 3 a 5 cenas narrativas, cada uma com:

- Trecho de texto (o que o avatar fala)
- Funcao narrativa (gancho, desenvolvimento, prova, virada, CTA)
- Avatar escolhido (pode rotacionar entre 2 avatares)
- Voz (normalmente uma por avatar)
- Background (cor, imagem ou video)
- Duracao estimada (segundos)

### Regra de quebra por duracao

| Duracao total | N de cenas | Duracao por cena |
|---|---|---|
| Ate 20s | 3 cenas | 5 a 7s cada |
| 20 a 40s | 4 cenas | 6 a 10s cada |
| 40 a 60s | 5 cenas | 8 a 12s cada |
| Mais de 60s | 5 cenas, a ultima mais longa | variavel |

### Regra de quebra por funcao narrativa

Toda cena tem um papel. Mapeamento padrao para 4 cenas:

- **Cena 1. GANCHO.** Premissa contra-intuitiva. Avatar A. Background: cor forte da paleta, nunca branco liso. Foco total no rosto.
- **Cena 2. PROBLEMA/CONTEXTO.** Avatar A continua OU corta para b-roll. Background: imagem ou video do contexto (planilha, pessoa cansada, estoque parado).
- **Cena 3. VIRADA/PROVA/METODO.** Se disponivel, avatar B (testemunho, autoridade, outro angulo). Background: cor diferente da Cena 1, cria contraste. Sem avatar B, mantem Avatar A com background novo.
- **Cena 4. CTA.** Avatar A volta. Background: cor forte (geralmente complementar da Cena 1 ou cor de acao).

### Mapeamento Mandala para Direcao Visual (TABELA OBRIGATORIA)

Use esta tabela para a direcao base. Combine com a direcao visual do Passo 3 para ajustar ao nicho.

| Tipo da Mandala | Paleta base | Ritmo | Bg cena 1 | Bg cena do meio | Bg CTA | Avatares |
|---|---|---|---|---|---|---|
| Comparacao | Dividida (A vs B) | Medio | Cor A solida | Split visual (img A vs img B) | Cor B solida | 1 avatar, split no b-roll |
| Problema/Solucao | Escuro > claro | Medio | Cor escura (#1a1a1a) | Imagem do problema | Cor clara da marca | 1 avatar |
| Explicacao | Neutro + acento | Lento | Cor neutra | Grafico/diagrama em imagem | Acento da marca | 1 avatar |
| Curiosidade | Contraste alto | Rapido | Cor inusitada (roxo, verde neon) | Imagem enigmatica | Cor solida forte | 1 avatar |
| Reflexao | Tons frios | Lento | Cor profunda (#0d1b2a) | Imagem contemplativa | Mesma cor cena 1 | 1 avatar |
| Certo/Errado | Vermelho + verde | Medio | Vermelho (errado) | Imagem do erro | Verde (certo) | 1 avatar, 2 angulos |
| Demonstracao | Cor da marca | Rapido | Cor da marca | Video/imagem do produto em uso | Cor da marca | 1 avatar |
| Procedimento | Cor da marca + numeracao | Medio | Cor solida | Imagem do passo | Cor da marca | 1 avatar |
| Impacto Visual | Cores vibrantes | Rapido | Imagem forte | Imagem forte | Cor solida | 1 avatar |
| Oportunidade | Dourado/amarelo | Medio | Amarelo (#f5b800) | Imagem da oportunidade | Amarelo | 1 avatar |
| Historia | Cinematografico | Lento | Imagem de abertura (contexto) | Sequencia de imagens | Cor solida | 1 ou 2 avatares |
| Prova Social | Azul/verde confianca | Medio | Imagem da pessoa real | Depoimento em quote visual | Cor de confianca | **2 avatares** (narrador + testemunho) |
| Clickbait | Cores chocantes | Rapido | Cor forte (vermelho, amarelo) | Imagem inesperada | Cor solida | 1 avatar |
| Sensacao | Cor emocional | Lento | Imagem sensorial | Imagem sensorial | Cor solida | 1 avatar |
| Contraste | Preto + branco ou 2 cores | Medio | Cor A solida | Cor B solida (contraste) | Mix das duas | 1 avatar |
| Ensino | Cor neutra limpa | Medio | Cor neutra | Grafico/exemplo | Cor da marca | 1 avatar |
| Revelacao | Escuro > luz | Medio | Preto/escuro | Imagem que "revela" | Cor clara | 1 avatar |
| Dilema | 2 cores em conflito | Medio | Cor A | Cor B | Cor resolutiva | 1 avatar |

**Como usar a tabela:** pegar a linha do tipo escolhido, ajustar as cores com a paleta que veio da direcao visual do Passo 3. Se o nicho usa pasteis, traduzir "vermelho" para rosa-coral, "verde" para verde-menta, mantendo a ideia de contraste.

### Backgrounds: como decidir entre cor, imagem ou video

| Situacao | Usar |
|---|---|
| Gancho ou CTA | Cor solida (foco no rosto e na fala) |
| Contexto/problema | Imagem (mais barata que video, contextual) |
| Demonstracao com movimento | Video de b-roll (se o plano HeyGen permitir) |
| Plano Creator (sem b-roll video) | So cor + imagem |

**Como conseguir as imagens de background:**

1. **Cor solida:** basta mandar `{"type": "color", "value": "#HEXCODE"}` no payload.
2. **Imagem:**
   - **Opcao A (recomendada).** Acionar a skill `criativo-estatico` internamente para gerar 2 a 3 imagens de background (cenarios, contextos, SEM pessoas e SEM texto) que casam com o roteiro. Salvar em `meus-produtos/{ativo}/entregas/videos/backgrounds/video-{data}/`. Fazer upload no HeyGen e usar o `image_key` retornado.
   - **Opcao B.** Stock gratuito (Unsplash, Pexels) via WebFetch + download + upload.
3. **Video b-roll:** so se o plano permitir. Mesma logica.

### Exemplo concreto de quebra em cenas

Roteiro aprovado (tipo Problema/Solucao, nicho: produtividade para empreendedoras):

> "O cansaco da empreendedora nao vem do volume de trabalho. Vem da fragmentacao. Voce abre 14 abas, comeca tres tarefas, e a noite chega sem nada concluido. O problema nao e falta de tempo, e ausencia de estrutura. Quando a agenda e montada em blocos de decisao em vez de blocos de tempo, o dia termina com energia sobrando. Comenta BLOCOS que eu te mando o mapa de 20 minutos."

Saida da quebra:

```json
[
  {
    "cena": 1,
    "funcao": "gancho",
    "texto": "O cansaco da empreendedora nao vem do volume de trabalho. Vem da fragmentacao.",
    "avatar": "Selma",
    "voz": "pt-BR_Selma",
    "background": {"type": "color", "value": "#1a1a1a"},
    "duracao_est": 7
  },
  {
    "cena": 2,
    "funcao": "contexto",
    "texto": "Voce abre 14 abas, comeca tres tarefas, e a noite chega sem nada concluido.",
    "avatar": "Selma",
    "voz": "pt-BR_Selma",
    "background": {"type": "image", "image_asset_id": "ASSET_KEY_1"},
    "duracao_est": 8
  },
  {
    "cena": 3,
    "funcao": "virada",
    "texto": "O problema nao e falta de tempo, e ausencia de estrutura. Quando a agenda e montada em blocos de decisao em vez de blocos de tempo, o dia termina com energia sobrando.",
    "avatar": "Selma",
    "voz": "pt-BR_Selma",
    "background": {"type": "color", "value": "#f5b800"},
    "duracao_est": 13
  },
  {
    "cena": 4,
    "funcao": "cta",
    "texto": "Comenta BLOCOS que eu te mando o mapa de 20 minutos.",
    "avatar": "Selma",
    "voz": "pt-BR_Selma",
    "background": {"type": "color", "value": "#2b6cb0"},
    "duracao_est": 6
  }
]
```

Total: ~34 segundos, 4 cenas, 3 backgrounds diferentes, ritmo variado.

### Mostrar a quebra ao usuario antes de gerar

```
Montei o video em 4 cenas. Da uma olhada:

Cena 1 (gancho, 7s): fundo preto. Fala: "[texto]"
Cena 2 (contexto, 8s): imagem de contexto gerada por IA. Fala: "[texto]"
Cena 3 (virada, 13s): fundo amarelo. Fala: "[texto]"
Cena 4 (CTA, 6s): fundo azul. Fala: "[texto]"

Total: ~34s, avatar unico: Selma.

1. Aprovar e seguir para selecao de avatar
2. Quero trocar alguma cena
3. Quero dividir em mais cenas
4. Quero usar 2 avatares (narrador + testemunho)
```

---

## PASSO 6. Selecao de Avatares (com rotacao)

Busque avatares via API:

```bash
curl -s "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

**Regras novas:**

1. **Historico de uso.** Leia `meus-produtos/{ativo}/entregas/videos/.avatares-usados.json` (se existir). Essa lista tem os avatares usados nos ultimos 5 videos deste produto. Na listagem ao usuario, marque com asterisco os que ja foram usados e coloque os novos no topo.
2. **Diversidade.** Liste 8 avatares variados (genero, idade, estilo). Dos 8, pelo menos 4 devem ser novos.
3. **Filtro por tipo da Mandala.** Se o tipo pede mais de 1 avatar (ex: Prova Social), peca duas escolhas.

Formato da listagem:

```
Quem vai aparecer no video? (novos no topo, * = ja usado antes)

1. [Nome] - feminina, executiva, 30-40
2. [Nome] - masculino, casual, 25-35
3. [Nome] - feminina, coach, 40-50
...
8. * [Nome] - feminina, executiva (usado no video anterior)

9. Enviar minha foto propria (cria avatar customizado)
```

Apos escolher, buscar vozes pt-BR compativeis com o genero e listar 5 opcoes.

**Atualizar o historico:** apos gerar o video com sucesso, adicionar o avatar (ou avatares) escolhidos em `.avatares-usados.json` com a data. Manter so os 5 ultimos.

---

## PASSO 7. Gerar Backgrounds de Imagem (se houver)

Para cada cena que usa `background.type == "image"`:

**Opcao A. Usar criativo-estatico (recomendado):**
Acione a skill `criativo-estatico` em modo silencioso, passando:
- Produto ativo
- Briefing da cena ("cenario de [descricao], SEM pessoas, SEM texto, proporcao 9:16")
- Paleta da direcao visual do Passo 3

A skill gera a imagem. Salve em `meus-produtos/{ativo}/entregas/videos/backgrounds/video-{data}/cena-{n}.jpg`.

**Opcao B. Stock gratuito:**
Download direto de Unsplash ou Pexels via WebFetch. Salve no mesmo local.

**Upload para HeyGen:**

```bash
curl -X POST "https://upload.heygen.com/v1/asset" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: image/jpeg" \
  --data-binary "@meus-produtos/{ativo}/entregas/videos/backgrounds/video-{data}/cena-1.jpg"
```

Guarde o `image_key` retornado por cena. Esse e o valor que vai em `image_asset_id` no payload final.

---

## PASSO 8. Confirmacao Final

Mostre o resumo:

```
Resumo do video:

- Tipo (Mandala): [tipo]
- Cenas: 4
- Avatar(es): [nome(s)]
- Duracao estimada: ~[X]s
- Backgrounds: [descricao das combinacoes]
- Formato: 1080x1920 (9:16, Reels/Stories)
- Custo estimado: ~US$ [valor]

1. Gerar video
2. Quero ajustar algo
```

---

## PASSO 9. Payload Multi-Cena (CORE TECNICO)

Este e o payload correto da API v2 da HeyGen. O array `video_inputs` tem um objeto por cena. O campo `background` fica DENTRO de cada cena.

```bash
curl -X POST "https://api.heygen.com/v2/video/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [
      {
        "character": {
          "type": "avatar",
          "avatar_id": "AVATAR_ID_1",
          "avatar_style": "normal"
        },
        "voice": {
          "type": "text",
          "voice_id": "VOICE_ID_1",
          "input_text": "TEXTO DA CENA 1"
        },
        "background": {
          "type": "color",
          "value": "#1a1a1a"
        }
      },
      {
        "character": {
          "type": "avatar",
          "avatar_id": "AVATAR_ID_1",
          "avatar_style": "normal"
        },
        "voice": {
          "type": "text",
          "voice_id": "VOICE_ID_1",
          "input_text": "TEXTO DA CENA 2"
        },
        "background": {
          "type": "image",
          "image_asset_id": "IMAGE_KEY_UPLOADED"
        }
      },
      {
        "character": {
          "type": "avatar",
          "avatar_id": "AVATAR_ID_1",
          "avatar_style": "normal"
        },
        "voice": {
          "type": "text",
          "voice_id": "VOICE_ID_1",
          "input_text": "TEXTO DA CENA 3"
        },
        "background": {
          "type": "color",
          "value": "#f5b800"
        }
      },
      {
        "character": {
          "type": "avatar",
          "avatar_id": "AVATAR_ID_1",
          "avatar_style": "normal"
        },
        "voice": {
          "type": "text",
          "voice_id": "VOICE_ID_1",
          "input_text": "TEXTO DA CENA 4"
        },
        "background": {
          "type": "color",
          "value": "#2b6cb0"
        }
      }
    ],
    "dimension": {
      "width": 1080,
      "height": 1920
    }
  }'
```

**Pontos criticos:**

- `video_inputs` e um ARRAY. Cada item e uma cena.
- `background` fica DENTRO de cada cena, nao no topo. Isso permite variacao entre cenas.
- `background.type` aceita `color`, `image`, `video` (b-roll, so Team/Enterprise).
- Para cor: `{"type": "color", "value": "#HEX"}`.
- Para imagem: `{"type": "image", "image_asset_id": "KEY_DO_UPLOAD"}`.
- Se o plano for Creator e der 403 em background de imagem, cair para cor solida diferente e avisar o usuario.
- Para rotacionar avatares no mesmo video, basta trocar o `avatar_id` e `voice_id` em cenas especificas.

---

## PASSO 10. Polling e Download

Polling a cada 30 segundos:

```bash
curl -s "https://api.heygen.com/v1/video_status.get?video_id=VIDEO_ID" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Estados:
- `pending` ou `processing`: "Video sendo gerado, 2 a 5 minutos, normal."
- `completed`: baixar do `video_url`
- `failed`: mostrar erro e sugerir reducao de cenas ou troca de background

Download:

```bash
curl -o "meus-produtos/{ativo}/entregas/videos/video-heygen-{data}.mp4" "VIDEO_URL"
```

Salvar tambem:

- `meus-produtos/{ativo}/entregas/videos/roteiro-heygen-{data}.md` (roteiro aprovado + quebra em cenas + payload usado)
- Atualizar `meus-produtos/{ativo}/entregas/videos/.avatares-usados.json` com o(s) avatar(es) usados

---

## PASSO 11. Entrega e Proximo Passo

```
Video gerado.

Arquivo: meus-produtos/{ativo}/entregas/videos/video-heygen-{data}.mp4
Roteiro + direcao: meus-produtos/{ativo}/entregas/videos/roteiro-heygen-{data}.md
Duracao: [X]s
Cenas: 4 (gancho / contexto / virada / cta)
Avatar(es): [nome(s)]

Quer criar variacoes?

1. Mesmo roteiro, avatar diferente (teste A/B)
2. Mesmo avatar, outro tipo da Mandala (nova direcao visual)
3. Versao mais curta (30s) para Stories
4. Nao, esse esta bom

PROXIMO PASSO SUGERIDO:
- /copy-anuncio para montar a campanha Meta Ads com esse video
- /video-editar se quiser cortar, legendar ou comprimir
```

---

## CHECKPOINTS OBRIGATORIOS

| Etapa | Aprovacao? |
|---|---|
| Setup API (passo 0) | So na primeira vez |
| Tipo da Mandala (passo 2) | Sim |
| Pesquisa visual (passo 3) | Nao, so mostra resumo |
| Roteiro (passo 4) | Sim |
| Quebra em cenas (passo 5) | Sim, e o checkpoint mais importante |
| Avatar(es) (passo 6) | Sim |
| Confirmacao final (passo 8) | Sim |
| Gerar video (passo 9) | Consentimento implicito no passo 8 |

Nunca pule um checkpoint.

---

## DICAS DE ECONOMIA

- Videos de 30 a 45 segundos quebrados em 4 cenas sao o ponto ideal de custo/impacto.
- Backgrounds de cor solida nao consomem upload nem minutos extras. Use eles como default.
- Imagens de background custam so o tempo de geracao da `criativo-estatico`, nao somam no HeyGen.
- Um video de 35s custa ~US$ 0,30 na HeyGen. Rodar 5 variacoes por campanha sai ~US$ 1,50.
- O plano Creator (US$ 24/mes) inclui 15 minutos = ~25 videos de 35s.
- Para A/B, reaproveite o mesmo roteiro trocando so avatar ou so paleta. Evita reescrever texto.
