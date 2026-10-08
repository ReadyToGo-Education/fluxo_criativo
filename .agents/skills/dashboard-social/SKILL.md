---
name: dashboard-social
description: >
  Porta de entrada unificada para configurar e atualizar os dashboards de
  métricas do Instagram, TikTok, YouTube e LinkedIn. Verifica quais dashboards
  já existem, oferece apenas os que ainda não foram gerados, consulta o .env
  antes de pedir qualquer dado e executa os scripts na sequência. O token Apify
  é pedido uma só vez e vale para todas as plataformas.
---

# Dashboard. Central de Métricas das Redes Sociais

## Quando Usar

- Quando o aluno quiser gerar o dashboard de uma ou mais redes sociais.
- Quando quiser ver o estado geral de todos os dashboards.
- Quando quiser atualizar os dados de plataformas já configuradas.

**Alternativa:** cada plataforma também pode ser configurada individualmente pelas skills `instagram-dashboard`, `tiktok-dashboard`, `youtube-dashboard` e `linkedin-dashboard`.

---

## PASSO 0. Detectar Estado Atual (OBRIGATÓRIO — executar antes de qualquer outra coisa)

### 0a. Verificar Fila de Geracao Interrompida

Antes de qualquer coisa, verifique se o arquivo `meus-produtos/{ativo}/.dashboard-queue.json` existe.

**Se o arquivo existir:** houve uma geracao interrompida na sessao anterior. Leia o conteudo:

```json
{
  "pendentes": ["tiktok", "youtube"],
  "concluidos": ["instagram"],
  "criado_em": "2026-04-28T10:00:00"
}
```

Exiba a retomada e pergunte:

```
Encontrei uma geracao incompleta da sessao anterior.

Concluidos: Instagram
Pendentes: TikTok, YouTube

1. Continuar de onde parou
2. Comecar do zero (descarta a fila)
3. Cancelar
```

- Opcao 1: ir direto para a Etapa 5 (Execucao) com os pendentes da fila. Pular confirmacao.
- Opcao 2: deletar o arquivo e continuar o fluxo normal abaixo.
- Opcao 3: encerrar sem fazer nada.

**Se o arquivo NAO existir:** seguir o fluxo normal abaixo.

### 0b. Detectar Comando Python

Execute o seguinte comando para determinar qual executável Python usar:

```bash
python3 --version 2>&1 || py -3 --version 2>&1
```

- Se `python3` responder com versão: use `python3` em todos os scripts deste comando.
- Se `python3` falhar mas `py -3` funcionar: use `py -3`.

Guarde o resultado como `{python}` e use essa variável em todos os comandos Bash abaixo. Nunca hardcode `py -3` nem `python3` diretamente.

### 0c. Detectar Estado das Plataformas

Execute em paralelo:
1. Leia o `.env` na raiz do projeto e extraia: `IG_USER`, `TIKTOK_USER`, `YOUTUBE_CHANNEL`, `LINKEDIN_PROFILE`, `APIFY_API_TOKEN`
2. Verifique a existência dos quatro arquivos de dashboard usando glob (cada script salva dentro de uma subpasta com o username/handle):
   - `meus-produtos/{ativo}/entregas/instagram-dashboard/*/dashboard.html`
   - `meus-produtos/{ativo}/entregas/tiktok-dashboard/*/dashboard.html`
   - `meus-produtos/{ativo}/entregas/youtube-dashboard/*/dashboard.html`
   - `meus-produtos/{ativo}/entregas/linkedin-dashboard/*/dashboard.html`

Monte a tabela de estado interna:

| Plataforma | dashboard.html existe? | Username no .env? | Estado |
|---|---|---|---|
| Instagram | sim/não | IG_USER=valor ou ausente | — |
| TikTok | sim/não | TIKTOK_USER=valor ou ausente | — |
| YouTube | sim/não | YOUTUBE_CHANNEL=valor ou ausente | — |
| LinkedIn | sim/não | LINKEDIN_PROFILE=valor ou ausente | — |

**Regras de estado:**

- `GERADO` — `dashboard.html` existe
- `PENDENTE` — `dashboard.html` não existe

O username no `.env` é informação de apoio — nunca perguntar o que já está salvo.

### 0d. Bifurcacao. Meu perfil ou concorrente?

ANTES de exibir o Passo 1, pergunte ao aluno:

```
O que voce quer analisar?

1. Meu(s) proprio(s) perfil(is)
2. Um concorrente
```

- Se responder 1 (meu perfil): segue o fluxo normal abaixo (Passo 1 em diante).
- Se responder 2 (concorrente): pula para a secao "Fluxo Concorrente" no fim deste arquivo.

Excecao: se a Fila de Geracao Interrompida (0a) estiver ativa e for opcao "Continuar de onde parou", nao perguntar a bifurcacao. A fila ja sabe se era meu ou de concorrente (campo `tipo` no JSON).

---

## PASSO 1. Exibir Status e Perguntar o Que Fazer

Exiba o painel de estado:

```
Central de Dashboards

Instagram:  [GERADO @{IG_USER}]   ou   [PENDENTE]
TikTok:     [GERADO @{TIKTOK_USER}]   ou   [PENDENTE]
YouTube:    [GERADO {YOUTUBE_CHANNEL}]   ou   [PENDENTE]
LinkedIn:   [GERADO {LINKEDIN_PROFILE}]   ou   [PENDENTE]
```

**Regra: se todos os quatro estiverem GERADOS**, exibir apenas:

```
O que quer fazer?

1. Atualizar todos os dados agora
2. Abrir um dashboard
3. Ver o que cada dashboard mostra
```

**Regra: se houver pelo menos um PENDENTE**, exibir:

```
O que quer fazer?

1. Gerar os dashboards pendentes
2. Atualizar os que já existem
3. Abrir um dashboard
4. Ver o que cada dashboard mostra
```

**Regra: se todos estiverem PENDENTES (primeira vez)**, pular o menu e ir direto para o Fluxo de Geração abaixo.

---

## Opção: Gerar Dashboards Pendentes

### Etapa 1. Mostrar o que está pendente e perguntar quais gerar

Liste apenas as plataformas com estado PENDENTE, na ordem Instagram, TikTok, YouTube:

```
Dashboards ainda não gerados:

1. Instagram
2. TikTok
3. YouTube
4. LinkedIn

Quais quer gerar agora? (pode marcar mais de um)
Digite os números separados por vírgula (ex: 1,3) ou o número único:
```

Se o aluno escolher gerar uma só: aceitar normalmente.

### Etapa 2. Coletar usernames (verificar .env antes de perguntar)

Para cada plataforma selecionada, na ordem Instagram, TikTok, YouTube:

**Verificação obrigatória antes de perguntar:** se o username já existir no `.env`, usar diretamente sem perguntar nada.

Só perguntar quando o campo estiver AUSENTE no `.env`:

**Instagram (só se `IG_USER` não existir no .env):**
```
Qual o usuário do seu perfil no Instagram?
(só o nome, sem o arroba. Ex: meuperfil)
```
Normalize: remover @, lowercase. Salve `IG_USER=<username>` no `.env`.

**TikTok (só se `TIKTOK_USER` não existir no .env):**

Se `IG_USER` foi coletado nesta mesma etapa (nao veio do .env), pergunte primeiro:
```
Seu TikTok usa o mesmo usuário do Instagram?

1. Sim (@{ig_user})
2. Não, é outro
```
Se escolher 1: salve `TIKTOK_USER={ig_user}` no `.env` e siga sem perguntar mais nada.
Se escolher 2, ou se `IG_USER` ja estava no `.env`:
```
Qual o usuário do seu perfil no TikTok?
(só o nome, sem o arroba. Ex: meuperfil)
```
Normalize: remover @, lowercase. Salve `TIKTOK_USER=<username>` no `.env`.

**YouTube (só se `YOUTUBE_CHANNEL` não existir no .env):**
```
Qual o endereço do seu canal no YouTube?
(ex: @meuperfil  ou  https://www.youtube.com/@meuperfil)
```
Aceitar @handle, URL completa ou channel ID. Salve `YOUTUBE_CHANNEL=<valor>` no `.env`.

**LinkedIn (só se `LINKEDIN_PROFILE` não existir no .env):**
```
Qual o handle ou URL do seu perfil no LinkedIn?
(ex: leandroladeira  ou  https://www.linkedin.com/in/leandroladeira)
```
Aceitar handle puro, URL completa ou `/in/handle`. Normalize removendo `https://www.linkedin.com/in/` e trailing slash. Salve `LINKEDIN_PROFILE=<handle>` no `.env`.

### Etapa 3. Token Apify (uma vez para todas)

Se `APIFY_API_TOKEN` já estiver no `.env`: usar diretamente, sem perguntar.

Se não estiver: execute a skill `configurar-apify` e retorne aqui após concluir. O token vale para todas as plataformas.

### Etapa 4. Confirmação antes de gerar

Exiba o resumo e peça confirmação:

```
Pronto para gerar:

{para cada plataforma selecionada}
- {Plataforma}: @{username}
{/para}
- Token Apify: configurado

Custo estimado por geração completa: menos de US$ 0,60 no plano gratuito do Apify.

1. Tudo certo, gerar agora
2. Quero ajustar algo
```

**Apos o aluno confirmar (opcao 1), ANTES de executar qualquer script:**

Crie o arquivo `meus-produtos/{ativo}/.dashboard-queue.json` com as plataformas selecionadas:

```json
{
  "pendentes": ["instagram", "tiktok", "youtube"],
  "concluidos": [],
  "criado_em": "{timestamp ISO 8601}"
}
```

Inclua apenas as plataformas que o aluno selecionou. Este arquivo garante que, se o contexto for perdido durante a geracao, a proxima chamada ao comando retome de onde parou.

### Etapa 5. Execução

**Quando 2 ou mais plataformas foram selecionadas**, pergunte antes de iniciar:

```
Quer gerar os dashboards ao mesmo tempo ou um por vez?

1. Ao mesmo tempo (mais rapido, termina em cerca de 10 minutos no total)
2. Um por vez (mais facil de acompanhar)
```

Nota interna (nao exibir ao usuario): gerar as quatro plataformas ao mesmo tempo e seguro no plano gratuito do Apify.

---

**Modo: ao mesmo tempo (paralelo)**

Anuncie:
```
Iniciando os dashboards ao mesmo tempo.
Cada um pode levar ate 10 minutos. Aviso quando todos terminarem.
```

Execute os scripts como chamadas Bash em paralelo (numa mesma mensagem de tool calls). Nao use `| tail` nem background — rode cada script direto com `2>&1` para capturar a saida completa.

| Plataforma | Script |
|---|---|
| Instagram | `{python} .claude/skills/instagram-dashboard/scripts/atualizar.py 2>&1` |
| TikTok | `{python} .claude/skills/tiktok-dashboard/scripts/atualizar.py 2>&1` |
| YouTube | `{python} .claude/skills/youtube-dashboard/scripts/atualizar.py 2>&1` |
| LinkedIn | `{python} .claude/skills/linkedin-dashboard/scripts/atualizar.py 2>&1` |

Apos todos concluirem, leia a saida de cada um e informe:

```
Concluido.

Instagram (@leandroladeiran): 30 posts coletados. Engajamento: X%
TikTok (@leandroladeiran): 30 videos. Seguidores: X. Engajamento: X%
YouTube (@VTSD): 30 videos. Inscritos: X. Engajamento: X%
LinkedIn (leandroladeira): 30 posts coletados. Engajamento: X%
```

Se algum falhar, exiba o erro em linguagem simples (sem traceback Python) e oriente o que fazer.

---

**Modo: um por vez (sequencial)**

Para cada plataforma selecionada, na ordem Instagram → TikTok → YouTube → LinkedIn:

Anuncie antes de cada uma:
```
Gerando dashboard do Instagram (@{IG_USER}).
Isso costuma levar entre 5 e 10 minutos. Aviso quando terminar.
```

Execute o script correspondente em primeiro plano, sem `| tail` e sem background:
```bash
{python} .claude/skills/instagram-dashboard/scripts/atualizar.py 2>&1
```

Aguarde a conclusao. Leia a saida completa para confirmar sucesso ou erro. Informe o resultado em linguagem simples antes de seguir para a proxima plataforma.

---

**Apos confirmar sucesso de cada plataforma** (em ambos os modos), execute:

1. Atualize `.dashboard-queue.json` movendo a plataforma de `pendentes` para `concluidos` (Edit cirurgico no arquivo JSON).

2. Atualize a secao Dashboards do painel de entregas:
```bash
{python} scripts/painel-incremental.py --secao dashboards
```

Se o painel nao existir ainda, informe:
```
O painel de entregas ainda nao foi criado para este produto.
O dashboard foi salvo em entregas/{plataforma}-dashboard/{username}/dashboard.html.
Rode /produto-concepcao para criar o painel e ter acesso centralizado.
```

Exemplo do arquivo de fila apos o Instagram concluir:
```json
{
  "pendentes": ["tiktok", "youtube"],
  "concluidos": ["instagram"],
  "criado_em": "{timestamp}"
}
```

### Etapa 6. Entrega Final

Execute o update do painel uma ultima vez para garantir que todas as plataformas geradas aparecem:

```bash
{python} scripts/painel-incremental.py --secao dashboards
```

Exiba a mensagem de entrega:

```
Dashboards criados.

Acesse pelo Painel de Entregas (aba Dashboards):
meus-produtos/{ativo}/painel-entregas.html

Para atualizar os dados quando quiser, chame este comando de novo.
```

**Apos exibir a Entrega Final:** delete o arquivo `meus-produtos/{ativo}/.dashboard-queue.json`. A fila foi concluida e nao deve reaparecer na proxima sessao.

### Etapa 7. Oferecer as Plataformas que Ficaram de Fora (opcional)

Apos a Entrega Final, verifique se alguma plataforma PENDENTE nao foi selecionada pelo aluno.

**Pule este passo se:** todas as 4 plataformas foram geradas nesta sessao, ou se o aluno nao selecionou nenhuma (encerrou sem gerar).

**Se sobrou 1 plataforma nao gerada:**
```
Quer gerar o dashboard do {plataforma} tambem?
O token Apify ja esta pronto.

1. Sim
2. Depois
```

**Se sobraram 2 plataformas:**
```
Quer aproveitar e gerar os outros dashboards tambem?
O token Apify ja esta pronto.

1. {Plataforma A}
2. {Plataforma B}
3. Os dois em sequencia
4. Depois, por enquanto esta bom
```

Se o aluno aceitar: volta para a Etapa 2 (coletar usernames que faltam) e executa em sequencia.

---

## Opção: Atualizar os que Ja Existem

Para cada plataforma com estado GERADO (na ordem Instagram → TikTok → YouTube → LinkedIn):

```
Atualizando Instagram (@{IG_USER})...
```

Execute o script correspondente e aguarde. Leia as ultimas 5 linhas do log.

Apos cada plataforma, informe o resultado e siga para a proxima:

```
Instagram: atualizado. Engajamento medio: {X}%
TikTok: atualizando...
```

Ao final, exiba o resumo:

```
Atualizacao concluida.

Instagram:  atualizado   /   erro: {mensagem}
TikTok:     atualizado   /   erro: {mensagem}
YouTube:    atualizado   /   erro: {mensagem}
LinkedIn:   atualizado   /   erro: {mensagem}
```

---

## Opcao: Abrir Dashboard

```
Qual dashboard quer abrir?

1. Instagram (@{IG_USER})
2. TikTok (@{TIKTOK_USER})
3. YouTube ({YOUTUBE_CHANNEL})
4. LinkedIn ({LINKEDIN_PROFILE})
```

Exibir apenas as plataformas com estado GERADO.

Antes de abrir, localize o caminho real com glob (cada script salva dentro de uma subpasta com o username/handle):

- Instagram: `meus-produtos/{ativo}/entregas/instagram-dashboard/*/dashboard.html`
- TikTok: `meus-produtos/{ativo}/entregas/tiktok-dashboard/*/dashboard.html`
- YouTube: `meus-produtos/{ativo}/entregas/youtube-dashboard/*/dashboard.html`
- LinkedIn: `meus-produtos/{ativo}/entregas/linkedin-dashboard/*/dashboard.html`

Execute o comando de abertura para o sistema operacional detectado, usando o caminho encontrado pelo glob:

| OS | Comando |
|---|---|
| Windows | `start {caminho-real}/dashboard.html` |
| macOS | `open {caminho-real}/dashboard.html` |
| Linux | `xdg-open {caminho-real}/dashboard.html` |

---

## Opcao: Ver o Que Cada Dashboard Mostra

```
O que cada dashboard mostra:

INSTAGRAM
  Seguidores, engajamento medio, formato mais postado
  Desempenho por formato (Reel, Carrossel, Foto)
  Heatmap de melhores horarios para postar
  Top 3 posts, analise de hashtags, linha do tempo, grade completa de posts

TIKTOK
  Seguidores, likes totais, engajamento medio por views
  Desempenho por duracao do video (ate 15s, 16-30s, 31-60s, 60s+)
  Heatmap de melhores horarios para postar
  Top 3 videos, analise de hashtags, linha do tempo, grade completa de videos

YOUTUBE
  Inscritos, total de views do canal, engajamento medio
  Desempenho por duracao (Shorts, curto, medio, longo)
  Melhores dias para publicar
  Top 3 videos, analise de titulos, linha do tempo, grade completa de videos

LINKEDIN
  Seguidores, conexoes, engajamento medio, tipo de post mais publicado
  Desempenho por tipo (Texto, Imagem, Video, Documento/PDF, Artigo, Repost)
  Melhores dias para postar
  Top 3 posts, analise de hashtags, tamanho do texto vs engajamento, linha do tempo, grade completa de posts

Todos os dashboards abrem direto no navegador, funcionam offline e tem filtros interativos.
```

---

## Regras

- **Verificar o `.env` antes de pedir qualquer dado.** Se `IG_USER`, `TIKTOK_USER`, `YOUTUBE_CHANNEL`, `LINKEDIN_PROFILE` ou `APIFY_API_TOKEN` ja estiverem presentes, usar diretamente sem perguntar.
- **O indicador primario de estado e a existencia do `dashboard.html`.** Nao depender de flags para decidir o que oferecer.
- **Token Apify e pedido uma unica vez** mesmo quando multiplas plataformas estao sendo geradas.
- **Ordem de execucao sequencial:** Instagram, TikTok, YouTube, LinkedIn. No modo paralelo, as quatro plataformas rodam simultaneamente como chamadas Bash independentes numa mesma mensagem.
- **Sem agendamento automatico:** nao configurar CronCreate nem schtasks. O aluno roda manualmente.
- **Nao usar travessao** em nenhum texto exibido ao usuario.
- **Usernames sao salvos no `.env` imediatamente apos o aluno informar**, antes de executar qualquer script.
- **Fila de geracao (`.dashboard-queue.json`):** criada ANTES do primeiro script rodar, atualizada apos cada conclusao, deletada ao final. Nunca executar scripts sem criar a fila primeiro. Se o arquivo existir ao abrir o comando, e retomada de sessao anterior.

---

## Proximos Passos Apos Configurar

- `/copy-variacao-post` — criar variacoes dos posts do Instagram com mais engajamento
- `/copy-social` — criar conteudo baseado nos videos do TikTok que performaram melhor
- `/copy-roteiro` — criar roteiros baseados nos videos do YouTube com mais views
- `/copy-social` — criar conteudo para o LinkedIn baseado nos posts com mais engajamento
- `/dados-instagram` — analise profunda de um perfil concorrente no Instagram

---

## Fluxo Concorrente

Acionado quando a bifurcacao (0d) for opcao 2.

### Passo C1. Coletar dados do concorrente

Pergunte UMA pergunta por vez:

1. **Nome do concorrente** (texto livre, ex: "Erico Rocha"). Use para exibir no painel.
2. **Quais plataformas voce quer analisar?**
   ```
   1. Instagram
   2. TikTok
   3. YouTube
   4. LinkedIn

   Digite os numeros separados por virgula (ex: 1,3) ou um numero unico.
   ```
3. Para cada plataforma escolhida, pergunte o handle. Use uma pergunta por vez, na ordem Instagram, TikTok, YouTube, LinkedIn:

   - **Instagram:** "Qual o @ do Instagram dele? (ex: ericosanrocha)"

   - **TikTok:** se o aluno ja informou o Instagram nesta sessao, pergunte primeiro:
     ```
     O TikTok dele usa o mesmo @ do Instagram?

     1. Sim (@{instagram_handle})
     2. Nao, e outro
     ```
     Se "Sim", reaproveite o handle do Instagram. Se "Nao", pergunte: "Qual o @ do TikTok dele? (ex: ericorochaoficial)"
     Se o aluno NAO escolheu Instagram, pergunte direto: "Qual o @ do TikTok dele?"

   - **YouTube:** se o aluno ja informou Instagram ou TikTok, pergunte primeiro:
     ```
     O canal do YouTube dele usa o mesmo @ do {Instagram/TikTok}?

     1. Sim (@{handle_anterior})
     2. Nao, e outro
     ```
     Se "Sim", monte a URL como `https://www.youtube.com/@{handle}`. Se "Nao", pergunte: "Qual o @ ou URL do canal no YouTube? (ex: @ericorochaoficial)"

   - **LinkedIn:** mesmo padrao do YouTube. Se ja tem um handle anterior, pergunte se reaproveita; senao, pergunte direto: "Qual o handle ou URL do perfil no LinkedIn? (ex: ericorocha)"

   **Regra de prioridade do handle sugerido:** se o aluno escolheu varias plataformas, sugira sempre o handle da PRIMEIRA plataforma informada (geralmente Instagram). Se Instagram nao foi escolhido, use o TikTok. E assim por diante.

### Passo C2. Gerar slug e confirmar

Gere o `slug` a partir do nome (ASCII, minusculo, hifens):
- "Erico Rocha" -> `erico-rocha`
- "Joao da Silva" -> `joao-da-silva`

Confirme com o aluno:

```
Vou analisar:

Nome:        Erico Rocha
Plataformas: Instagram (@ericosanrocha), YouTube (@ericorochaoficial)
Pasta:       entregas/concorrentes/erico-rocha/

Tempo estimado: 3 a 6 minutos.

1. Pode comecar
2. Quero ajustar algo
```

Se o aluno aprovar, prossiga. Se ja existir uma pasta `entregas/concorrentes/{slug}/`, avisar que vai mesclar com os dados existentes (substituindo a(s) plataforma(s) analisada(s) agora).

### Passo C3. Verificar token Apify

Se `APIFY_API_TOKEN` nao estiver no `.env`, acione a skill `configurar-apify` e espere a conclusao.

### Passo C4. Criar fila de concorrente

Antes do primeiro script, crie `meus-produtos/{ativo}/.dashboard-queue.json` com:

```json
{
  "tipo": "concorrente",
  "slug": "erico-rocha",
  "nome": "Erico Rocha",
  "pendentes": ["instagram", "youtube"],
  "concluidos": [],
  "handles": {"instagram": "ericosanrocha", "youtube": "@ericorochaoficial"},
  "criado_em": "2026-05-11T14:30:00"
}
```

### Passo C5. Executar os scripts

Para cada plataforma da lista, rode o `atualizar.py` correspondente com `--concorrente <slug> --nome-bonito "<nome>"` e o flag de handle da plataforma. Cada script vai salvar em `entregas/concorrentes/{slug}/{plataforma}/dashboard.html` e atualizar o `meta.json`.

Mapeamento dos flags:

| Plataforma | Comando |
|---|---|
| Instagram | `{python} .claude/skills/instagram-dashboard/scripts/atualizar.py --usuario {handle} --concorrente {slug} --nome-bonito "{nome}" 2>&1` |
| TikTok | `{python} .claude/skills/tiktok-dashboard/scripts/atualizar.py --usuario {handle} --concorrente {slug} --nome-bonito "{nome}" 2>&1` |
| YouTube | `{python} .claude/skills/youtube-dashboard/scripts/atualizar.py --canal {handle} --concorrente {slug} --nome-bonito "{nome}" 2>&1` |
| LinkedIn | `{python} .claude/skills/linkedin-dashboard/scripts/atualizar.py --perfil {handle} --concorrente {slug} --nome-bonito "{nome}" 2>&1` |

Pode rodar em paralelo (uma chamada Bash por plataforma na mesma mensagem) ou sequencial. Pergunte ao aluno se ele preferir.

Apos cada script terminar, atualize a fila (mova da lista pendentes para concluidos). Ao final, delete o arquivo `.dashboard-queue.json`.

### Passo C6. Regerar a secao do painel

Execute:

```
{python} scripts/painel-incremental.py --secao dashboards --slug {produto-ativo}
```

Isso vai detectar o novo concorrente e adicionar na lista "Concorrentes" do hub do painel.

### Passo C7. Entrega final

```
Concluido. Concorrente "Erico Rocha" analisado.

Pasta: meus-produtos/{ativo}/entregas/concorrentes/erico-rocha/
Plataformas: Instagram, YouTube

Para ver no painel:
1. Abra o painel de entregas
2. Va na secao "Redes Sociais"
3. Clique em "Analise de concorrentes"
4. Clique no card "Erico Rocha"

Para remover este concorrente depois:
- /dashboard-concorrente-remover
```
