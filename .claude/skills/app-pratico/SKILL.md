---
name: app-pratico
description: >
  Transforma a transcricao completa das aulas de um curso em um aplicativo
  web pratico de uso real, publicado direto na Vercel, com criacao do
  projeto e deploy feitos pela propria skill. O formato do app varia
  conforme o curso e nao e fixo em um numero de paineis: pode ser uma
  calculadora com formulas do curso, um checklist interativo, uma arvore de
  decisao, ou, para cursos com muitas aulas, um assistente conversacional
  que indexa o conteudo e indica ao aluno qual aula resolve a situacao dele
  (arquetipo tipo "Celestino"). Diferente da /app-saas (que gera PRD para o
  Lovable com login, banco de dados e 2 perfis de usuario), esta skill
  entrega o app pronto, construido em cima das formulas, protocolos e
  criterios que o proprio curso ensina, valida os calculos contra os
  exemplos numericos das aulas antes de publicar (quando aplicavel), e
  sempre comeca com uma pre avaliacao de objetivo antes de propor qualquer
  ideia de app. Use quando o aluno disser "quero um app a partir das aulas
  do meu curso", "transforma minhas aulas numa calculadora", "quero uma
  ferramenta pratica pro meu aluno usar no dia a dia", "faz um app que roda
  na Vercel com o conteudo do curso", "quero um assistente que indica qual
  aula ver", ou pedir para repetir o processo do app de indicadores ou do
  Celestino para outro curso.
---

# App Pratico. Da Transcricao das Aulas ao Aplicativo Publicado

Pega o conteudo real de um curso (aulas em video ou ja transcritas) e
devolve uma ferramenta pratica que o aluno do curso usa no dia a dia real de
trabalho, publicada com link proprio na Vercel. Nao e um SaaS com login e
banco de dados por usuario (isso e a `/app-saas`), e uma ferramenta
compartilhada sem conta de ninguem. O formato varia conforme o que o curso
ensina e o objetivo definido na pre avaliacao: pode ser um utilitario
totalmente estatico (calculadora, checklist, arvore de decisao, conversor,
simulador de caso, gerador de script), que e o caminho mais simples e sem
custo recorrente, ou, quando o curso tem muitas aulas e o problema do aluno
e mais "qual aula resolve isso" do que "quanto isso da", um assistente
conversacional que indexa as aulas (arquetipo descrito em
`references/exemplo-celestino-assistente.md`), que tem um backend leve e
custo recorrente pequeno.

## Quando Usar

- "Quero um app a partir das aulas do meu curso."
- "Transforma minha transcricao numa calculadora."
- "Meus alunos precisam de uma ferramenta pratica pra usar no trabalho, nao
  so o curso em video."
- Repetir, para um curso novo, o mesmo processo que ja gerou uma calculadora
  a partir de outro curso.

## Pre-requisitos

- Produto do curso ja cadastrado (`meus-produtos/{slug}/perfil.md`). Se nao
  existir, acione `/produto-novo` primeiro. Sem perfil, nao ha identidade
  visual nem publico pra guiar as ideias de app.
- Se as aulas estiverem no YouTube (nao listado ou publico) e for usar esse
  caminho para pegar a transcricao: `yt-dlp` instalado na maquina (mesma
  dependencia da skill `cortes-live`, ver `references/portabilidade.md`).
- Para publicar: `VERCEL_API_TOKEN` no `.env`. Se nao existir, a Etapa 10
  guia o cadastro. A propria skill cria o projeto na Vercel e faz o deploy,
  nao depende do aluno rodar nenhum outro command a parte.
- Nao depende de nenhuma outra credencial, MCP ou skill externa.

## O Que Fazer

### 0. Contexto

1. Ler `meus-produtos/.ativo`. Se nao houver produto ativo para o curso em
   questao, orientar `/produto-trocar` (se o produto ja existe) ou
   `/produto-novo` (se ainda nao existe) antes de continuar.
2. Ler `meus-produtos/{slug}/perfil.md` inteiro (Quadro, Furadeira, publico,
   nicho, paleta se houver) e `idconsumidor.md` se existir.
3. Verificar se `meus-produtos/{slug}/referencia-aulas/INDICE.md` ja existe.
   Se existir, pular a Etapa 2 e perguntar se quer reaproveitar o material
   ja reunido ou atualizar com aulas novas.

### 1. Pre avaliacao do objetivo do app

**Etapa obrigatoria. Nunca pular direto para reunir aulas ou propor ideias
sem isso.** O risco de construir a ferramenta errada (ex: um app publico de
captacao quando o aluno queria um bonus exclusivo, ou uma calculadora
grande quando ele queria algo simples e rapido) vem justamente de pular
esta etapa.

Pergunte, uma por vez, no padrao numerado:

**Pergunta 1. Qual e o objetivo principal desse app?**
```
1. Bônus exclusivo pra quem já comprou o curso (aumenta a percepção de valor, ajuda a reduzir reembolso)
2. Ferramenta de captação de leads novos (gratuita, pública, funciona como isca)
3. Apoio pro dia a dia de quem já é aluno (utilidade pura, sem intenção comercial direta)
4. Prévia ou demonstração do método, pra ajudar a vender o curso pra quem ainda não comprou
```

**Pergunta 2. Quem vai poder acessar o app?**
```
1. Só quem comprou (precisa de trava de senha ou código)
2. Qualquer pessoa, acesso público e aberto
3. Não decidi ainda, quero sua recomendação
```
Se a resposta for 3, recomende com base na Pergunta 1: objetivos 1 e 3
normalmente pedem trava; objetivos 2 e 4 normalmente pedem acesso publico.
Explique o motivo da recomendacao em 1 frase antes de seguir.

**Pergunta 3. Você já tem uma ideia do tipo de ferramenta (calculadora, checklist, árvore de decisão, conversor etc.) ou quer que eu sugira depois de ler as aulas?**
```
1. Já tenho uma ideia, vou te contar
2. Quero que você sugira depois de ler o conteúdo das aulas
```
Se a resposta for 1, anote a ideia e use como direcao nas etapas seguintes,
mas ainda valide contra o conteudo real das aulas na Etapa 4 antes de
assumir que e viavel do jeito que o aluno imaginou.

**Pergunta 4. Alguma urgência ou prazo pra esse app?**
(pergunta aberta, resposta livre; ex: "preciso pra um lancamento na proxima
semana". Se houver prazo apertado, considere entregar primeiro a versao com
1 ferramenta ou painel em vez do escopo completo, e avisar isso na Etapa 5).

Ao final, resuma e confirme antes de seguir:
```
Resumo do que entendi:
- Objetivo: {...}
- Acesso: {público / com trava de senha}
- Ideia de ferramenta: {a do aluno, ou "a definir depois de ler as aulas"}
- Prazo: {...}

1. Confirmar e seguir
2. Quero ajustar algo
```

Essas respostas alimentam a Etapa 4 (ideias) e a Etapa 5 (trava de senha e
tamanho do escopo), evitando perguntar tudo de novo mais pra frente.

### 2. Reunir a transcricao completa das aulas

Anuncie: `🔍 Próximo passo: reunir a transcrição completa das aulas do curso (4 passos). Tempo estimado: varia conforme a fonte, de 2 a 15 minutos.`

Pergunte (uma por vez):

**Pergunta 1. Onde estao as aulas do curso?**
```
1. Videos no YouTube (nao listados ou publicos)
2. Arquivos de video ou audio no computador
3. Ja tenho a transcricao em texto, PDF ou Word
4. A plataforma do curso (Hotmart, Kiwify, Eduzz etc.) tem exportacao de transcricao
```

Trate cada caminho:

**Opcao 1, YouTube.** Peça a lista de links, um por aula (aceita link de
playlist tambem, mas confirme a lista de videos extraida antes de seguir).
Para cada aula, rode:

```
python scripts/cortes_transcrever.py "{url-da-aula}" --out "{pasta-temporaria}"
```

Esse e o mesmo script usado pela skill `cortes-live`, ja disponivel no
projeto. Ele baixa so a legenda automatica (nunca o video inteiro) e gera
`transcricao.md` com timestamp por frase. Copie o conteudo de cada
`transcricao.md` para `meus-produtos/{slug}/referencia-aulas/aula-{NN}-{slug-da-aula}.txt`
e apague a pasta temporaria. Se uma aula nao tiver legenda em portugues
(`pt-orig` nem `pt`), marque como pendente e continue com as demais, sem
travar o processo inteiro.

**Opcao 2, arquivos locais de video ou audio.** Esta skill nao inclui
transcricao por IA de audio bruto (fora de escopo). Oriente duas saidas
praticas: (a) subir o video como nao listado no YouTube so para extrair a
legenda automatica pela Opcao 1, depois pode apagar de la; ou (b) se a
gravacao foi feita em Zoom, StreamYard, Loom ou Google Meet, essas
ferramentas costumam gerar transcricao propria exportavel, que cai na
Opcao 3.

**Opcao 3 e 4, texto/PDF/Word ja existente.** Peca para anexar os arquivos
no chat. Use a skill nativa `anthropic-skills:pdf` para PDFs e
`anthropic-skills:docx` para Word. Extraia o texto de cada arquivo e salve
como `meus-produtos/{slug}/referencia-aulas/aula-{NN}-{slug-da-aula}.txt`.

Ao final, gere `meus-produtos/{slug}/referencia-aulas/INDICE.md` listando
todas as aulas reunidas, uma linha de resumo por aula, e um aviso claro
sobre quais aulas ficaram pendentes (se houver).

**Regra dura: nunca inventar conteudo de aula que nao foi fornecido.** Se
faltar transcricao de uma aula, o app so pode usar o que estiver
efetivamente disponivel nas aulas reunidas.

### 3. Leitura e mapeamento do conteudo pratico

Anuncie: `🔍 Próximo passo: ler as aulas, propor ideias de app e fechar o escopo (3 passos). Tempo estimado: 3 a 6 minutos.`

`⏳ Passo 1/3: ler as aulas e mapear o conteúdo prático.`

Leia o `INDICE.md` e as aulas completas (todas, mesmo em cursos longos; se
forem muitas, leia em lotes, sem pular nenhuma). Enquanto le, extraia e
organize:

- Formulas, calculos, conversoes, tabelas de referencia, faixas e limites.
- Checklists, protocolos passo a passo, arvores de decisao.
- Scripts, frases prontas, modelos de atendimento ou de conversa.
- Erros comuns e sinais de alerta que o curso ensina a evitar.

Para cada item extraido, guarde de qual aula ele veio (rastreabilidade),
porque isso alimenta a validacao da Etapa 7 e evita que uma formula erre por
falta de contexto do proprio curso.

### 4. Propor ideias de app

Anuncie: `⏳ Passo 2/3: montar as ideias de app a partir do que as aulas ensinam e do objetivo definido na etapa 1.`

Gere de 6 a 10 ideias de ferramenta pratica, priorizando o que o publico do
curso usaria no momento real de trabalho (nao um dashboard administrativo)
e filtrando pelo objetivo da Etapa 1: se o objetivo e captacao publica,
priorize ferramentas simples e independentes; se e bonus exclusivo, pode
propor algo mais completo com varios paineis. Se o aluno ja trouxe uma
ideia na Pergunta 3 da Etapa 1, inclua ela como opcao 1 (ja validada contra
o que as aulas realmente ensinam) e complemente com outras.

Tipos validos: calculadora, checklist interativo, arvore de decisao ou
triagem, conversor de unidades, gerador de script ou resposta pronta, guia
de referencia rapida, simulador de caso, e, quando o curso tiver muitas
aulas (20 ou mais) cobrindo situacoes variadas, um assistente conversacional
que indexa as aulas e indica qual delas resolve a situacao do aluno (ver
`references/exemplo-celestino-assistente.md`). Este ultimo tipo so deve
entrar na lista de ideias quando o conteudo do curso realmente favorecer
esse formato (muitas aulas, problema navegacional), nao como opcao padrao.

Formato obrigatorio:

```
## Ideias de app pratico para [nome do curso]

**1. [Nome da ferramenta]**
O que faz: [1 linha]
Vem de quais aulas: [aula 3, aula 7...]
Por que ajuda no momento real de uso: [1 linha]
Encaixa no objetivo definido (bônus / captação / apoio / prévia): [sim/como]

**2. ...**
```

Pergunte:
```
Qual ideia voce quer desenvolver?
Digite o numero, peca uma mistura (ex: "juntar a 2 com a 5") ou peca novas ideias.
```

### 5. Especificacao rapida e aprovacao do escopo

Anuncie: `⏳ Passo 3/3: detalhar como cada cálculo, checklist ou (se for o caso) o assistente vai funcionar.`

Monte a especificacao do app escolhido. O formato da especificacao muda
conforme o arquetipo escolhido na Etapa 4:

**Se for do arquetipo padrao (calculadora, checklist, arvore de decisao,
conversor, simulador, gerador de script):**
- Nome do app.
- Paineis ou abas, se houver mais de uma ferramenta dentro do mesmo app (o
  numero de paineis varia conforme o curso, nao e fixo em 3; pode ser 1
  painel unico ou varios, agrupados por tema). Se a Etapa 1 sinalizou prazo
  apertado, proponha uma versao reduzida (1 painel primeiro) como
  alternativa.
- Para cada calculo ou checklist: a formula ou regra exata (citando a aula
  de origem), os campos de entrada e unidades, e como o resultado deve ser
  interpretado (ex: faixas "bom / atencao / ruim", com cor).
- Os exemplos numericos que aparecem nas proprias aulas, que serao usados
  para validar o app antes de publicar.

**Se for do arquetipo assistente (ver `references/exemplo-celestino-assistente.md`):**
- Nome do app.
- Quais campos vao compor o indice de cada aula (titulo, resumo curto,
  resumo completo com numeros e situacoes, tags, palavras-chave, link de
  video quando houver).
- Qual modelo de LLM usar (priorizar um modelo barato) e aviso explicito ao
  aluno sobre o custo recorrente por conversa e a necessidade de configurar
  a chave de API como variavel de ambiente no painel da Vercel (nao so no
  `.env` local).
- O tom e as regras de resposta do assistente (nunca recomendar aula fora
  da lista de candidatas, sempre justificar com evidencia concreta,
  entrevistar o aluno no maximo 1 ou 2 perguntas por vez).

**Em ambos os casos:**
- Trava de senha: usar a decisao da Pergunta 2 da Etapa 1 como padrao,
  apenas confirmando aqui (nao perguntar de novo do zero).
- Identidade visual puxada de `perfil.md` (paleta, tom).

Mostre o resumo e pergunte:
```
1. Aprovar e construir o app
2. Quero ajustar algo
```

Nao avance para a Etapa 6 sem essa aprovacao.

### 6. Construir o app

Anuncie: `🔍 Próximo passo: construir e validar o aplicativo (2 passos). Tempo estimado: 2 a 4 minutos.`

`⏳ Passo 1/2: construir o app.`

**Se a Etapa 5 especificou o arquetipo assistente**, siga a arquitetura de
`references/exemplo-celestino-assistente.md` (frontend estatico com
indice das aulas e busca local, backend leve so de proxy pro LLM, chave de
API em variavel de ambiente) em vez das regras abaixo, que sao especificas
do arquetipo padrao.

Para o arquetipo padrao, gere um unico arquivo HTML com estas
caracteristicas obrigatorias:

- Arquivo unico. CSS em `<style>`, JS em `<script>`, zero dependencias
  externas (Google Fonts e opcional). Abre offline depois de carregado uma
  vez.
- Mobile-first. E pra ser usado no celular, muitas vezes no proprio local
  de trabalho do aluno.
- Calculo ao vivo, sem botao "calcular", sempre que fizer sentido (o
  resultado atualiza enquanto o usuario digita).
- Resultado em destaque, com a interpretacao textual do numero, nao so o
  numero cru.
- Quando um calculo depende do resultado de outro, ofereca um botao do tipo
  "puxar resultado anterior" em vez de pedir para o usuario digitar de
  novo.
- Se houver mais de uma ferramenta, organize em abas ou paineis navegaveis
  dentro do mesmo arquivo.
- Se a Etapa 5 definiu trava de senha: gere o hash SHA-256 da senha e grave
  so o hash no `<script>` (nunca a senha em texto). Ao acertar, salvar em
  `localStorage` para nao pedir de novo no mesmo aparelho. Deixe registrado
  no `SOBRE-O-APP.md` como trocar a senha depois.
- Paleta e tom puxados de `perfil.md`. Nenhuma cor inventada fora da
  identidade do curso.
- Ver `references/exemplo-caso-anterior.md` para um caso real de um app
  construido com este mesmo processo, usado como referencia de qualidade e
  de estrutura (paineis, botao de puxar valor, interpretacao do resultado).

### 7. Validar os calculos

Anuncie: `⏳ Passo 2/2: validar os cálculos contra os exemplos das próprias aulas.`

Esta etapa vale para o arquetipo padrao (calculadora, checklist etc). Para
o arquetipo assistente, a validacao equivalente e conferir se o assistente
so recomenda aulas da lista de candidatas e se as justificativas citam
evidencia concreta, testando com 2 ou 3 perguntas reais de exemplo antes de
publicar.

Rode, item por item, os exemplos numericos coletados na Etapa 3 contra a
logica implementada no HTML, conferindo se o resultado bate com o que a
aula ensinou. Liste essa validacao (formula, exemplo, resultado esperado,
resultado obtido) antes de seguir. Se algum exemplo nao bater, corrija a
formula e valide de novo antes de mostrar o app pronto.

### 8. Aprovacao final

Mostre um resumo do que foi construido (paineis, ferramentas, se tem trava
de senha) e a validacao numerica. Pergunte:
```
1. Aprovar e salvar
2. Quero ajustar algo
```

### 9. Salvar

Apos aprovacao:

- Salvar o HTML em `meus-produtos/{slug}/entregas/aplicativo/{slug-do-app}.html`.
- Gerar `meus-produtos/{slug}/entregas/aplicativo/SOBRE-O-APP.md` com: o
  objetivo definido na Etapa 1, o que o app faz, formulas por painel (com a
  aula de origem), a validacao numerica da Etapa 7, controle de acesso (se
  houver senha, como trocar) e como atualizar o app depois.
- Informar o caminho absoluto do arquivo.

### 10. Publicar na Vercel

Anuncie: `🔍 Próximo passo: publicar o app na Vercel e devolver o link (6 passos). Tempo estimado: 1 a 2 minutos.`

Esta etapa e autossuficiente: a skill verifica a integracao, cria o projeto
quando necessario e faz o deploy, sem depender do aluno rodar nenhum outro
command a parte.

**Passo 1. Verificar integracao existente.**
- Ler `.env` e checar se `VERCEL_API_TOKEN` ja existe.
- Se existir, validar que ainda funciona chamando `GET https://api.vercel.com/v2/user` com o token. Se der erro de autenticacao, avisar que o token salvo expirou ou foi revogado e refazer o setup guiado abaixo.
- Se nao existir, mostrar o setup guiado: orientar o aluno a criar conta em vercel.com (se ainda nao tiver), ir em Settings > Tokens, gerar um token e colar no chat. Salvar no `.env` como `VERCEL_API_TOKEN` automaticamente, sem pedir pro aluno editar o arquivo. Nunca reexibir o token depois de salvo.

**Passo 2. Verificar se ja existe um projeto vinculado a este app.**
- Checar se `meus-produtos/{slug}/entregas/aplicativo/.vercel` ja existe com um `project_id` salvo (de uma publicacao anterior deste mesmo app). Se existir, pular direto para o Passo 4 no modo "nova versao do projeto existente".
- Se nao existir, perguntar o nome do projeto na Vercel (sugerir um nome baseado no slug do app, minusculo, sem acento, sem espaco; normalizar silenciosamente se vier fora do padrao) e se e conta pessoal ou time (se for time, pedir o slug do time).
- Antes de criar, checar se ja existe um projeto com esse nome na conta via `GET https://api.vercel.com/v9/projects/{nome}` (com `?teamId=...` se for time). Se ja existir e nao for este mesmo app, avisar a colisao e pedir outro nome.

**Passo 3. Confirmar antes de publicar.**
```
Projeto: {nome}
Conta: {pessoal | time "{slug}"}
Arquivo: {slug-do-app}.html
Modo: {novo projeto | nova versão do projeto existente}

1. Publicar
2. Cancelar
```

**Passo 4. Criar o projeto (se novo) e fazer o deploy.**
- Publicar via `curl` POST em `https://api.vercel.com/v13/deployments{?teamId=...}`, payload `{name, files: [{file: "index.html", data: "<conteudo>"}], target: "production"}`. Usar arquivo de payload temporario pra evitar problema de tamanho no comando, apagar depois. O primeiro deploy com um `name` novo cria o projeto automaticamente; se o projeto ja existir, sobe uma nova versao dele. Isso cobre tanto "criar projeto" quanto "fazer deploy" no mesmo passo, exatamente como a API da Vercel funciona.

**Passo 5. Aguardar o build.**
- Se retornar `QUEUED` ou `BUILDING`, fazer polling em `GET /v13/deployments/{id}{?teamId=...}` a cada poucos segundos ate virar `READY` (maximo 30 segundos). Tratar erros de API com ate 3 tentativas ajustando o payload; se persistir, mostrar o erro completo e perguntar como prosseguir.

**Passo 6. Salvar o historico e oferecer dominio proprio.**
- Salvar ou atualizar `meus-produtos/{slug}/entregas/aplicativo/.vercel` com `project_id`, nome do projeto, conta ou time e a URL publica. Isso e o que permite a proxima publicacao deste app pular direto para "nova versao", sem repetir as perguntas do Passo 2.
- Perguntar se o aluno tem dominio proprio pra apontar (ex: `app.seudominio.com.br`). Se sim, adicionar o dominio no projeto (`POST /v10/projects/{idOrName}/domains{?teamId=...}`) e orientar o CNAME apontando pra `cname.vercel-dns.com` no provedor de DNS dele.

**Passo extra, so para o arquetipo assistente.** Depois do primeiro deploy,
configurar a chave de API do LLM como variavel de ambiente do projeto
(`POST /v10/projects/{idOrName}/env{?teamId=...}`, ex: `OPENROUTER_API_KEY`).
Sem isso o backend (`api/chat.js`) responde erro 500 em producao mesmo com
o deploy `READY`. Testar com uma pergunta real antes de entregar o link ao
aluno.

### 11. Entrega final

```
✅ Concluído: app "{nome do app}" publicado.

Objetivo do app: {o definido na Etapa 1}
Arquivo local: {caminho absoluto do .html}
Link público: https://{projeto}.vercel.app
Senha de acesso: {senha, se houver} (repasse só para quem comprou o curso)

Próximos passos:
- Testar no celular antes de divulgar
- Repassar o link (e a senha, se houver) para os alunos do curso
- Para atualizar depois, edite o arquivo local e peça para republicar (a skill já sabe reaproveitar o mesmo projeto)
```

## Regras

- Nunca pular a Etapa 1 (pre avaliacao). Nenhuma ideia de app e proposta
  antes de entender objetivo, publico de acesso e prazo.
- Nunca inventar formula, protocolo ou dado que nao veio das aulas. Se o
  curso nao ensinou um numero de referencia, deixar o campo como entrada
  livre em vez de chutar um padrao.
- Sempre citar de qual aula cada formula ou regra vem, tanto na Etapa 5
  quanto no `SOBRE-O-APP.md` final. Rastreabilidade e obrigatoria.
- Sempre validar contra pelo menos um exemplo numerico do proprio curso
  antes de publicar (Etapa 7). Se o curso nao tiver nenhum exemplo
  numerico, avisar o aluno antes de prosseguir sem essa validacao.
- O arquetipo padrao desta skill e sempre um arquivo HTML unico, sem
  backend e sem login de usuario. O arquetipo assistente (ver
  `references/exemplo-celestino-assistente.md`) e a unica excecao
  permitida, e mesmo assim so tem um backend leve de proxy pro LLM, nunca
  login nem dado de usuario persistido. Se o pedido exigir persistencia de
  dados na nuvem, multiplos usuarios com conta propria ou area
  administrativa, isso foge do escopo desta skill: avisar e sugerir
  `/app-saas` em vez disso.
- O numero de paineis, abas ou telas do app varia conforme o curso. Nunca
  assumir que todo app tem 3 paineis so porque o caso de referencia
  (`exemplo-caso-anterior.md`) tinha 3. Pode ser 1 ferramenta unica, ou um
  assistente sem paineis nenhum.
- Nunca pular a aprovacao da Etapa 5 (escopo) nem da Etapa 8 (app pronto).
- Antes de criar um projeto novo na Vercel, sempre checar se ja existe um
  projeto vinculado a este app (`entregas/aplicativo/.vercel`) ou um nome
  colidindo na conta. Nunca criar um segundo projeto pro mesmo app.
- Nunca mostrar o `VERCEL_API_TOKEN` no chat, em log ou em qualquer arquivo
  fora do `.env`.
- Nao usar travessao em nenhum texto exibido.
- Acentuacao em portugues do Brasil correta em todo texto gerado, inclusive
  neste proprio arquivo de referencia quando for editado.

## Referencias

- `references/portabilidade.md`. O que precisa estar instalado para rodar
  esta skill em outra maquina ou outro projeto fluxo-criativo.
- `references/exemplo-caso-anterior.md`. Estudo de caso real de um app do
  arquetipo padrao (calculadora com paineis), usado como referencia de
  qualidade.
- `references/exemplo-celestino-assistente.md`. Estudo de caso real de um
  app do arquetipo assistente (indexa as aulas, indica qual assistir),
  usado quando o curso tem muitas aulas e o problema do aluno e
  navegacional em vez de computacional.
- `scripts/cortes_transcrever.py` (raiz do projeto, compartilhado com a
  skill `cortes-live`). Extrai a legenda automatica de um video do YouTube
  sem baixar o video inteiro.
- Command `/pagina-vercel`. Mesma tecnica de publicacao via API usada na
  Etapa 10, aqui adaptada para a pasta `entregas/aplicativo/` e com
  verificacao de integracao e criacao de projeto embutidas na propria
  skill.
