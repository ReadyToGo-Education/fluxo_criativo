---
name: carrossel
description: Gera carrosséis virais para Instagram nos 7 estilos do workshop (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia da semana). Coleta o contexto do produto ativo + estilo escolhido, gera os 6 slides de texto, os prompts visuais em inglês, a legenda revisada e oferece 3 caminhos para gerar as imagens (Manual, Claude in Chrome só no Desktop, API paralela). Opção "Gerar todos" cria os 7 carrosséis em sequência com aprovação em lotes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, Skill
model: sonnet
---

# Carrossel de Instagram

Gera carrossel viral em 1 dos 7 estilos do workshop, com texto + prompts visuais + legenda. O aluno escolhe o estilo, a skill conduz a entrevista guiada e entrega tudo pronto para postar.

---

## ⚠ Antes de começar. Ambiente de execução

A skill funciona em 2 ambientes (CLI ou Desktop), mas com capacidades diferentes:

| Ambiente | Manual | API paralela | Claude in Chrome |
|---|---|---|---|
| **Claude Code no terminal (CLI)** | ✅ | ✅ se tiver `OPENROUTER_API_KEY` ou `OPENAI_API_KEY` no `.env` | ❌ Não disponível |
| **Claude Desktop (claude.ai pelo navegador)** | ✅ | ✅ se tiver a API key | ✅ se a extensão Claude in Chrome estiver conectada |

**Por que o Claude in Chrome não funciona pelo terminal?**

A extensão Claude in Chrome é um produto **Desktop-only**. Ela vive como uma extensão do navegador Chrome e se comunica apenas com sessões da claude.ai abertas no navegador. Quando o aluno está rodando esta skill pelo Claude Code no terminal/CLI, **mesmo tendo a extensão instalada no Chrome, ela NÃO se comunica com a sessão CLI** (são processos isolados).

A skill detecta isso em runtime checando se as tools `mcp__Claude_in_Chrome__*` estão presentes:
- Presentes → ambiente Desktop, oferece opção 2 (Chrome) no menu.
- Ausentes → ambiente CLI ou Desktop sem extensão, **não oferece** opção 2 e explica o motivo ao aluno.

Para usar a opção Chrome, o aluno precisa abrir o Claude Desktop, invocar `/carrossel` lá, e ter a extensão Claude in Chrome conectada.

Para usar a opção API paralela (recomendada no CLI), basta ter `OPENROUTER_API_KEY` no `.env`. A skill `/configurar-imagens` configura isso.

---

## REGRA DURA. Uma pergunta por turno

Esta skill é entrevista guiada. **Cada pergunta é exibida em UM turno separado e aguarda resposta antes da próxima.**

PROIBIDO: bulkar perguntas no mesmo turno, assumir default sem perguntar, pular para a geração antes de coletar tudo.

OBRIGATÓRIO: exibir 1 pergunta, parar, aguardar, salvar, exibir micro-resumo de progresso (ver `passo-coleta-base.md`), só então a próxima.

---

## Passo 0. Contexto e detecção de retomada

### 0.1. Contexto

Leia em paralelo:
- `meus-produtos/.ativo`
- `meus-produtos/{ativo}/perfil.md` (se existir)
- `meus-produtos/{ativo}/idconsumidor.md` (se existir)

Se não houver produto ativo, oriente o aluno a rodar `/produto-novo` primeiro e encerre.

### 0.2. Detecção de retomada (modo "Gerar todos")

Verifique se existe `meus-produtos/{ativo}/entregas/conteudo-social/.carrossel-queue.json`. Esse arquivo é gerado pelo modo "Gerar todos" e marca uma execução que pode ter sido interrompida.

**Se existir**, leia o conteúdo:

```json
{
  "modo": "todos",
  "pular_noticia": false,
  "criado_em": "2026-05-14T15:00:00",
  "concluidos": ["nunca", "sempre"],
  "pendentes": ["odeio", "erros", "amo", "ninguem-conta", "noticia"],
  "variaveis": {
    "handle": "@inglesatleta",
    "nicho_produto": "inglês para atletas, curso online de 12 semanas",
    "cores_marca": "DEFAULT",
    "tom_texto": "Clássica/profissional",
    "estilo_design": "Editorial e cinematográfico",
    "desejo_publico": "atender em inglês com fluência total",
    "objetivo_publico": "ganhar contratos no exterior",
    "noticia_categoria": "TREND",
    "noticia_modo": "MANUAL",
    "noticia_tom": "Aleatório"
  }
}
```

Exiba:

```
Encontrei um "Gerar todos" interrompido da sessão anterior.

Concluídos: {lista_legivel}
Pendentes: {lista_legivel}

1. Continuar de onde parou
2. Começar do zero (descarta a fila)
3. Cancelar

Digite o número.
```

- Opção 1: pule a coleta (`Passo 2`) e vá direto pro `Passo 2.C` reaproveitando `variaveis`.
- Opção 2: delete o arquivo de fila e siga fluxo normal.
- Opção 3: encerre.

**Se NÃO existir o arquivo de fila**, siga para o Passo 1 normalmente.

---

## Anúncio inicial

Antes do Passo 1, anuncie:

```
🔍 Próximo passo: gerar o carrossel completo (texto + 6 prompts visuais + legenda revisada). Tempo estimado: 7 a 12 minutos (mais se você escolher o caminho Claude in Chrome ou aguardar geração de imagens).
```

Para a opção "Gerar todos", anuncie depois que o aluno escolher 8 no Passo 1:

```
🔍 Próximo passo: gerar os 7 carrosséis (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia da semana). Tempo estimado: 20 a 35 minutos.
```

---

## Passo 1. Escolha do estilo

Exiba SOMENTE este bloco e pare:

```
Qual carrossel você quer gerar?

1. Nunca. 5 proibições contraintuitivas + CTA. Tom de alerta.
2. Sempre. 5 ações contraintuitivas + CTA. Tom de ritual.
3. Odeio. 5 takes polêmicos defendidos + CTA tribal. Identificação por oposição.
4. Erros. 5 erros comuns que sabotam um desejo + CTA. Precisa do desejo do público.
5. Amo. 5 takes afirmativos defendidos + CTA tribal. Identificação por admiração.
6. Ninguém Conta. 5 verdades ocultas sobre um objetivo + CTA insider. Precisa do objetivo do público.
7. Notícia da semana. 7 a 9 slides a partir de uma notícia do nicho (fluxo próprio, com busca na web e 5 perguntas diferentes da base padrão).
8. Gerar todos. Faz os 7 em sequência (fluxo longo, 10 perguntas e 20 a 35 minutos de geração).

Digite o número (ou digite "cancelar" para sair).
```

AGUARDE A RESPOSTA. Se a resposta for `cancelar`, `0`, `sair` ou variação clara, encerre. Caso contrário, salve como `estilo_carrossel` (valores: `nunca`, `sempre`, `odeio`, `erros`, `amo`, `ninguem-conta`, `noticia`, `todos`).

---

## Passo 2. Ramo do fluxo

### Se `estilo_carrossel` está entre 1 e 6 (atemporais)

1. **Carregue** o arquivo do estilo em `references/estilos/{estilo}.md`.
2. **Carregue** `references/passo-coleta-base.md`.
3. **Execute as 5 perguntas base**, uma por turno, parando entre cada uma. Use o cabeçalho "Pergunta X de Y" com o total correto (5 ou 6 conforme o estilo).
4. **Após cada resposta**, exiba o **micro-resumo de progresso** documentado no `passo-coleta-base.md`.
5. Se o estilo substitui a pergunta de tom (caso de Odeio, Amo, Ninguém Conta), use a versão dele.
6. **Execute a pergunta extra** se aplicável (Erros: Desejo. Ninguém Conta: Objetivo).
7. **Vá para o Passo 2.5** (confirmação consolidada).

### Se `estilo_carrossel == noticia`

1. **Carregue** `references/estilos/noticia.md`.
2. **Execute o fluxo de coleta da Notícia** (@ + nicho/produto + categoria + modo + tom), com cabeçalho "Pergunta X de 5" e micro-resumo entre cada uma.
3. **Vá para o Passo 2.5** (confirmação consolidada).
4. Após confirmação, **carregue o prompt-base** em `.claude/skills/programar-carrossel-noticia/references/prompt-carrossel-noticia.md`, monte com placeholders, calcule data atual via `Bash` com `Get-Date -Format "yyyy-MM-dd"`, e execute o prompt na sessão atual via `WebSearch`.
5. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-noticia/`.
6. **Vá direto para o Passo 6** (entrega).

### Se `estilo_carrossel == todos`

**O fluxo "Gerar todos" usa aprovação em lotes (1 carrossel por vez na revisão) e cache de retomada.**

#### 2.A. Confirmação inicial

Exiba SOMENTE este bloco e pare:

```
Vou gerar os 7 carrosséis em sequência. Para isso, preciso coletar:

- 5 dados base (@, nicho/produto, paleta, tom default, estilo de design)
- 1 dado específico de Erros (desejo do público)
- 1 dado específico de Ninguém Conta (objetivo do público)
- 3 dados específicos de Notícia (categoria, modo, tom)

São 10 perguntas no total. Depois eu gero os textos e te mostro 1 carrossel por vez para você aprovar (você pode aprovar todos automaticamente também).

1. Sim, gerar todos os 7 (inclui Notícia da semana, com WebSearch)
2. Pular Notícia (mais rápido, gera 6)
3. Cancelar

Digite o número.
```

AGUARDE A RESPOSTA. Se `2`, salve `pular_noticia = true`. Se `3`, encerre.

#### 2.B. Coleta consolidada

Colete TODAS as variáveis necessárias em sequência, **uma pergunta por turno**, com cabeçalho "Pergunta X de 10" (ou X de 7 se pulou Notícia) e micro-resumo entre cada uma:

1. Handle (1.1 do `passo-coleta-base.md`)
2. Nicho e produto (1.2)
3. Cores da marca (1.3)
4. Tom default (1.4 versão base)
5. Estilo de design (1.5)
6. Desejo do público (extra de Erros)
7. Objetivo do público (extra de Ninguém Conta)
8. Notícia: categoria (se não pulou)
9. Notícia: modo (se não pulou)
10. Notícia: tom (se não pulou)

#### 2.C. Geração silenciosa dos textos + criação da fila

Antes de começar a geração, salve o arquivo de fila em:

```
meus-produtos/{ativo}/entregas/conteudo-social/.carrossel-queue.json
```

Com:
```json
{
  "modo": "todos",
  "pular_noticia": {true ou false},
  "criado_em": "{ISO}",
  "concluidos": [],
  "pendentes": ["nunca", "sempre", "odeio", "erros", "amo", "ninguem-conta", "noticia"],
  "variaveis": { ... }
}
```

(Remova `noticia` da lista de pendentes se `pular_noticia = true`.)

Para cada estilo da lista de pendentes, em ordem:

```
⏳ Passo {N}/7: gerando texto do carrossel "{Estilo}"...
```

1. Aplique o critério central do estilo.
2. Aplique o Manual da Copy + revisora silenciosamente.
3. Salve o `texto.md` em `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/texto.md`.
4. Atualize o arquivo de fila movendo o estilo de `pendentes` para `concluidos`.

#### 2.D. Aprovação em lotes (1 carrossel por vez)

Depois que os 6 (ou 7) textos estiverem gerados, ofereça ao aluno:

```
Textos dos {N} carrosséis gerados. Como você quer revisar?

1. Aprovar todos automaticamente (eu gero prompts visuais e legendas sem mostrar os slides agora)
2. Revisar um por um (eu mostro o primeiro, você aprova, mostro o próximo)

Digite o número.
```

AGUARDE A RESPOSTA.

**Se 1**: pule para o Passo 2.E.

**Se 2**: para cada carrossel da lista, mostre os slides no formato individual:

```
═══════════════════════════════════════
CARROSSEL {N} DE {total}. {ESTILO}
═══════════════════════════════════════

SLIDE 1
Título: {...}
Subtítulo: {...}

(... até slide 6 ...)

═══════════════════════════════════════

1. Aprovar este e ver o próximo
2. Quero ajustar algo neste
3. Aprovar este E todos os próximos sem revisar (modo expresso)
4. Cancelar tudo

Digite o número.
```

- **Opção 1**: marque este como aprovado e mostre o próximo.
- **Opção 2**: pergunte o que ajustar, refaça (passando pela revisora), mostre de novo o mesmo carrossel.
- **Opção 3**: marca este + todos os restantes como aprovados, pula direto pro Passo 2.E.
- **Opção 4**: encerra deixando a fila como está (aluno pode retomar depois).

#### 2.E. Geração silenciosa de prompts visuais + legendas

Para cada carrossel aprovado:

```
⏳ Passo {N}/7: gerando prompts visuais e legenda do carrossel "{Estilo}"...
```

1. Gere os 6 prompts visuais em inglês (usando `template-prompt-imagem.md` + ajustes do estilo) e mostre-os no chat. **Não salve `prompts.txt` em disco.**
2. Gere a legenda do Instagram (Manual da Copy + revisora silenciosamente).
3. Salve `legenda.txt`.

#### 2.F. Entrega consolidada

Após gerar tudo, **delete o arquivo `.carrossel-queue.json`** e exiba:

```
✅ {N} carrosséis gerados.

Cada carrossel tem: texto + 6 prompts visuais + legenda revisada.

Pastas criadas em:
meus-produtos/{ativo}/entregas/conteudo-social/
├── carrossel-nunca/
├── carrossel-sempre/
├── carrossel-odeio/
├── carrossel-erros/
├── carrossel-amo/
├── carrossel-ninguem-conta/
└── carrossel-noticia/ (se você não pulou)

Em cada pasta:
- texto.md (slides 1 a 6)
- legenda.txt (legenda revisada do Instagram)

Os 6 prompts visuais de cada carrossel já foram exibidos no chat durante a geração. Para gerar as imagens, copie-os e cole no ChatGPT (ou outra ferramenta), OU configure a `OPENROUTER_API_KEY` no `.env` rodando `/configurar-imagens` para usar a opção 3 (API paralela) na próxima execução.

Digite /carrossel para gerar outro, ou /programar-carrossel para agendar.
```

---

## Passo 2.5. Confirmação consolidada (modo individual e Notícia)

> Aplica para `estilo_carrossel` entre 1 e 6 e para Notícia. NÃO aplica para "todos" (que tem fluxo próprio).

Depois de coletar todas as respostas, antes de gerar qualquer coisa, exiba o resumo:

```
Resumo do que vou criar:

Estilo: {Estilo escolhido}
@ do Instagram: {handle}
Nicho e produto: {nicho_produto}
Paleta: {cores_marca} (ou nome do default do estilo)
Tom da copy: {tom_texto}
Estilo de design visual: {estilo_design}
{se Erros} Desejo do público: {desejo_publico}
{se Ninguém Conta} Objetivo do público: {objetivo_publico}
{se Notícia} Categoria: {categoria} / Modo: {modo} / Tom: {tom_noticia}

Vou gerar:
- 6 slides de texto (estilos atemporais) ou 7 a 9 slides (Notícia)
- 6 prompts visuais em inglês para ChatGPT
- 1 legenda do Instagram revisada
- 1 prompt opcional para Claude in Chrome

1. Tudo certo, gerar
2. Ajustar algo (diga qual campo)
3. Cancelar

Digite o número.
```

AGUARDE A RESPOSTA.

- **Opção 1**: prossiga para o Passo 3 (modo individual) ou para a execução da Notícia (modo Notícia).
- **Opção 2**: pergunte qual campo ajustar, refaça aquela pergunta, volte para mostrar o resumo de novo.
- **Opção 3**: encerre sem gerar.

---

## Passo 3. Geração dos 6 slides de texto (estilos atemporais individuais)

> Aplica APENAS para `estilo_carrossel` entre 1 e 6 (modo individual). Para `todos` use o Passo 2.D. Para `noticia` o fluxo é outro.

Anuncie:

```
⏳ Etapa 1/3: gerando os 6 slides de texto do carrossel "{Estilo}"...
```

> Numeração visível ao aluno (1/3, 2/3, 3/3) cobre os 3 momentos de geração depois da coleta. Os Passos 0, 1, 2 e 2.5 são coleta (já encerrados); Passo 6 é entrega final (sem anúncio Nível 2).

Aplicando o que está no arquivo do estilo (`references/estilos/{estilo}.md`):

1. Aplique o **critério central** do estilo.
2. Use o **tom escolhido** no Passo 2 para adaptar o estilo de escrita.
3. Estruture os slides conforme o estilo (lead "Nunca…", "Sempre…", "Eu odeio quem…", "Erro #N:", "Eu amo quem…", "Ninguém te conta que…").
4. CTA do slide 6 com verbo diferente do lead + motivo claro + relação com os 5 slides + geração de desejo.
5. **Aplicar o Manual da Copy** (`.claude/skills/revisora/references/manual-copy.md`) frase por frase antes de mostrar:
   - Zero travessões, zero exclamações, zero "Não é X. É Y.", zero perguntas no slide 1.
   - Toda afirmação com tese, dado, prazo ou cena concreta.
   - Especificidade, não generalização.
6. **Acionar a skill `revisora`** passando o texto dos 6 slides. Aplique correções DIRETO no texto.

Apresente os 6 slides em formato:

```
SLIDE 1
Título: {título}
Subtítulo: {subtítulo}

SLIDE 2
Título: {título}
Subtítulo: {subtítulo}

(... até o slide 6 ...)
```

Pergunte:

```
1. Aprovar e seguir
2. Quero ajustar algo (diga o que)
3. Regenerar tudo do zero
4. Cancelar

Digite o número.
```

- **Opção 1**: salve `texto.md` imediatamente (formato abaixo) e siga para o Passo 4.
- **Opção 2**: pergunte o que ajustar (ex: "ajustar slide 2", "trocar CTA", "tom mais agressivo"), aplique a mudança passando pela revisora, mostre de novo. Loop.
- **Opção 3**: regenere os 6 slides do zero (mesmo input, prompt diferente). Volta a perguntar.
- **Opção 4**: encerre.

### Salvar texto.md imediatamente após aprovação

```markdown
# Carrossel {Estilo}

Produto: {nome do produto}
Handle: {handle}
Tom: {tom_texto}
Estilo de design: {estilo_design}
Gerado em: {data}

## Slide 1
- Título: {título}
- Subtítulo: {subtítulo}

## Slide 2
- Título: {título}
- Subtítulo: {subtítulo}

(... até o slide 6 ...)
```

---

## Passo 4. Prompts visuais (output triplo)

Anuncie:

```
⏳ Etapa 2/3: gerando os 6 prompts visuais em inglês...
```

Carregue `references/passo-output-triplo.md` e execute as ações documentadas:

1. **Mostrar os 6 prompts no chat** (em inglês, usando `template-prompt-imagem.md` com ajustes do estilo). Os prompts ficam visíveis no chat para o aluno copiar. **Não salve `prompts.txt` em disco** (evita gravação de arquivo grande duplicando o que já está no chat).
2. **Detectar capacidades da sessão** (Passo 3.3 do `passo-output-triplo.md`):
   - **3.3.A**. Disponibilidade do MCP `mcp__Claude_in_Chrome__*`. Salva `tem_chrome_mcp = true | false`. **Nota Desktop-only**: o MCP do Claude in Chrome só existe na versão Desktop do Claude (app claude.ai pelo navegador). Se o aluno está rodando esta skill pelo Claude Code no terminal/CLI, `tem_chrome_mcp` sempre será `false`. A skill explica esse motivo ao aluno no menu.
   - **3.3.B**. Presença de `OPENROUTER_API_KEY` ou `OPENAI_API_KEY` no `.env`. Salva `tem_api_imagem = true | false` + `provider_api`.
3. **Oferecer caminhos** conforme as capacidades detectadas. **Renumere as opções dinamicamente, sem buracos** (o aluno nunca vê "1, 3" pulando o "2"). Mantenha um mapa interno `{numero_visivel → caminho_logico}` para interpretar a resposta:
   - Sempre: caminho **Manual** (1 no menu).
   - Se `tem_chrome_mcp == true`: caminhos **Chrome só imagens** (próximo número) e **Chrome imagens + legenda** (próximo número).
   - Caminho **API paralela OpenRouter** sempre exibido (próximo número). Se `tem_api_imagem == false`, descreva o item com aviso "Indisponível agora, precisa configurar `OPENROUTER_API_KEY` no `.env` rodando `/configurar-imagens` antes de escolher".
   - Quando o caminho Chrome não está disponível (CLI ou Desktop sem extensão), exiba **abaixo do menu** o aviso explicativo (Chrome só funciona no Claude Desktop com a extensão). Não numere a opção ausente.

   Exemplo de menu em sessão CLI sem API:
   ```
   1. Manual no ChatGPT...
   2. Automatizado via API (OpenRouter)... — Indisponível agora, precisa configurar OPENROUTER_API_KEY no .env rodando /configurar-imagens.
   ```

   Exemplo de menu em Desktop com Chrome MCP e com API:
   ```
   1. Manual no ChatGPT...
   2. Automatizado via Claude in Chrome (só imagens, sequencial)...
   3. Automatizado via Claude in Chrome (imagens + legenda)...
   4. Automatizado via API (OpenRouter, paralela)...
   ```

4. **Executar conforme escolha** (use o mapa interno do passo 3 para resolver o número visível):
   - Manual: seta `legenda_origem = LOCAL`. Os prompts já estão no chat; o aluno copia direto. Não grava arquivo extra.
   - Chrome sequencial: executa via MCP (navigate → enviar 6 prompts em sequência → aguardar cada imagem). Seta `legenda_origem = LOCAL`.
   - Chrome + legenda: executa Chrome sequencial + envia Parte 3 (instrução de legenda) → captura legenda via `get_page_text` → passa pela revisora → salva em `legenda.txt`. Seta `legenda_origem = CHATGPT`.
   - API paralela com `tem_api_imagem == true`: roda `scripts/gerar-imagens-api.py` com `concurrent.futures` disparando as 6 chamadas em paralelo. Salva `slide-1.png` até `slide-6.png` na subpasta `imagens/`. Seta `legenda_origem = LOCAL`.
   - API paralela com `tem_api_imagem == false`: pare e instrua o aluno a rodar `/configurar-imagens` antes. Não tente executar.

A variável `legenda_origem` é lida no Passo 5 para decidir se a legenda local deve ser gerada ou se a do ChatGPT já basta.

---

## Passo 5. Geração da legenda

Anuncie:

```
⏳ Etapa 3/3: processando a legenda do Instagram...
```

Carregue `references/passo-legenda.md` e execute o **gate inicial** (seção 4.0):

### Se `legenda_origem == LOCAL` (caminho 1 manual OU 2a só imagens)

Gera a legenda local seguindo o passo-legenda.md:

1. Aplique o **Manual da Copy** + estrutura de gancho/desenvolvimento/pico/virada/ponte/CTA/hashtags.
2. Acione a **revisora** e aplique correções direto.
3. **Mostre a legenda** no chat em bloco copiável.
4. **Salve em `legenda.txt`** na mesma pasta.
5. **Aprovação OBRIGATÓRIA com as 4 opções abaixo. Não simplifique para 2 opções, mesmo que pareça que tudo deu certo:**

```
1. Aprovar e salvar
2. Quero ajustar algo (diga o que)
3. Regenerar do zero
4. Cancelar

Digite o número.
```

Loop até aprovação. As opções 3 (regenerar) e 4 (cancelar) são parte do contrato do aluno com a skill, não devem ser cortadas em nenhuma execução.

### Se `legenda_origem == CHATGPT` (caminho 2b com MCP automatizado)

A legenda já foi capturada do ChatGPT no Passo 4 e já passou pela revisora. **NÃO gere legenda local automaticamente.** Apenas confirme aprovação:

```
✅ Legenda do ChatGPT capturada e revisada (Manual da Copy aplicado).

{conteúdo da legenda}

Salva em legenda.txt.

1. Aprovar e seguir para a entrega
2. Quero ajustar algo na legenda do ChatGPT (refaço com revisora local)
3. Quero também gerar uma legenda LOCAL pra comparar (vou gerar agora)
4. Refazer a legenda no ChatGPT (reabro Claude in Chrome)

Digite o número.
```

Comportamento por opção:
- **1**: encerra Passo 5 e segue pra entrega.
- **2**: pergunta o que ajustar, refaz com a revisora local, mostra de novo.
- **3**: gera legenda local agora (executa 4.1 a 4.6 do passo-legenda.md), salva em `legenda-local.txt` (sem sobrescrever a do ChatGPT), mostra as duas lado a lado.
- **4**: reabre Chrome MCP e refaz captura.

---

## Passo 6. Entrega

Exiba:

```
✅ Carrossel "{Estilo}" gerado.

Arquivos salvos em:
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/
├── texto.md (slides 1 a 6, já aprovados)
├── legenda.txt (legenda revisada do Instagram)
└── imagens/ (se você escolheu a opção 3 da API paralela)

{Se aluno usou caminho Chrome MCP, incluir o link da conversa do ChatGPT aqui}
Conversa do ChatGPT com as 6 imagens:
{url_chatgpt}

Legenda pronta pra colar no Instagram:

---
{conteúdo da legenda.txt inline}
---

Próximos passos:
- Os 6 prompts visuais já estão visíveis acima neste chat. Para gerar manualmente, copie cada bloco e cole no ChatGPT (ou outra ferramenta de imagem).
- Para automatizar tudo de uma vez no futuro, configure a `OPENROUTER_API_KEY` no `.env` rodando `/configurar-imagens` e use a opção 3.
- A legenda acima também está salva em legenda.txt na pasta do carrossel.

Quer gerar outro carrossel agora? Digite /carrossel.
Quer agendar carrosséis recorrentes? Digite /programar-carrossel.
```

**REGRA OBRIGATÓRIA. Exiba a legenda inline na entrega final, mesmo que ela já tenha sido mostrada antes no Passo 5.** O aluno acabou de aprovar os slides, ver os prompts visuais, talvez aguardar o Chrome rodar as imagens. O fluxo dele é longo e a legenda ficou no histórico do chat lá em cima. Repetir a legenda no bloco final é prática padrão pra ele copiar com 1 clique direto do último output da skill, sem precisar rolar a conversa nem abrir o `legenda.txt`.

Exiba os caminhos absolutos no formato copiável conforme regra do `CLAUDE.md` (texto, não link).

---

## Regras

- **Aprovação obrigatória** em Passo 2.5 (confirmação consolidada), Passo 3 (slides) e Passo 5 (legenda) no modo individual.
- **Aprovação em lotes** no modo "Gerar todos" (Passo 2.D), com opção "expresso" para aprovar todos automaticamente.
- **Manual da Copy + revisora** aplicados em TODO texto antes de mostrar.
- **Salvar `texto.md` imediatamente após aprovação dos slides** (Passo 3). Evita perda em caso de queda de sessão.
- **Cache de retomada** no modo "Gerar todos" via `.carrossel-queue.json`. Permite continuar de onde parou se o aluno sair no meio.
- **Anúncios Nível 2** em cada passo longo (`⏳ Passo X/Y:`). Aluno nunca fica olhando tela parada sem feedback.
- **"Cancelar"** disponível em toda aprovação. Aluno pode sair a qualquer momento.
- **Sem travessão, sem exclamação** em todo texto gerado.
- **Português brasileiro com acentuação correta** em todo texto exibido ao aluno.
- **Reaproveitar contexto** do produto ativo. Se `perfil.md` tem handle, nicho, produto, paleta, ofereça como sugestão.

---

## Quando NÃO usar esta skill

- O aluno quer **agendar carrosséis recorrentes** na nuvem. Use `/programar-carrossel`.
- O aluno quer só a **legenda** sem o carrossel inteiro. Rode a skill `revisora` direto no texto.
- O aluno ainda não cadastrou produto. Rode `/produto-novo` primeiro.

---

## Estrutura de pastas criadas pela skill

```
meus-produtos/{ativo}/entregas/conteudo-social/
├── .carrossel-queue.json  (só existe durante "Gerar todos" em andamento)
├── carrossel-nunca/
├── carrossel-sempre/
├── carrossel-odeio/
├── carrossel-erros/
├── carrossel-amo/
├── carrossel-ninguem-conta/
└── carrossel-noticia/
```

Cada pasta contém os arquivos descritos no Passo 6: `texto.md`, `legenda.txt` e (opcionalmente) a subpasta `imagens/` quando a opção 3 da API paralela é usada.
