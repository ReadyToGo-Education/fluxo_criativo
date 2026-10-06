---
name: carrossel
description: Gera carrosséis virais para Instagram nos 9 estilos do workshop (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia da semana, Curiosidade, Editorial). Coleta o contexto do produto ativo + estilo escolhido, gera os slides de texto, os prompts visuais, a legenda revisada e oferece 3 caminhos para gerar as imagens (Manual, Claude in Chrome só no Desktop, API paralela). Opção "Gerar todos" cria os 9 carrosséis em sequência com aprovação em lotes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, Skill
model: sonnet
---

# Carrossel de Instagram

Gera carrossel viral em 1 dos 9 estilos do workshop, com texto + prompts visuais + legenda. O aluno escolhe o estilo, a skill conduz a entrevista guiada e entrega tudo pronto para postar.

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
  "pendentes": ["odeio", "erros", "amo", "ninguem-conta", "curiosidade", "editorial", "noticia"],
  "variaveis": {
    "handle": "@inglesatleta",
    "nicho_produto": "inglês para atletas, curso online de 12 semanas",
    "cores_marca": "DEFAULT",
    "tom_texto": "Clássica/profissional",
    "estilo_design": "Editorial e cinematográfico",
    "desejo_publico": "atender em inglês com fluência total",
    "objetivo_publico": "ganhar contratos no exterior",
    "curiosidade_tom": "Jornalístico",
    "editorial_cta_tipo": "ManyChat",
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
🔍 Próximo passo: gerar o carrossel completo (texto + prompts visuais + legenda revisada). Tempo estimado: 7 a 12 minutos (mais se você escolher o caminho Claude in Chrome ou aguardar geração de imagens).
```

Para a opção "Gerar todos", anuncie depois que o aluno escolher 10 no Passo 1:

```
🔍 Próximo passo: gerar os 9 carrosséis (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia da semana, Curiosidade, Editorial). Tempo estimado: 30 a 55 minutos.
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
7. Notícia da semana. 7 a 9 slides a partir de uma notícia recente do nicho (fluxo próprio, com busca na web e 5 perguntas diferentes da base padrão).
8. Curiosidade. 7 a 9 slides a partir de uma curiosidade atemporal do nicho, fato chocante ou dado contraintuitivo sem prazo de validade (fluxo próprio, com busca na web).
9. Editorial. 6 slides com narrativa de especialista (notícia real, pesquisa, polêmica, conta maluca, dados). Slide 1 abre com notícia/dado impactante; venda só no slide 6 (fluxo próprio, com escolha entre 10 ideias).
10. Gerar todos. Faz os 9 em sequência (fluxo longo, 12 perguntas e 30 a 55 minutos de geração).

Digite o número (ou digite "cancelar" para sair).
```

AGUARDE A RESPOSTA. Se a resposta for `cancelar`, `0`, `sair` ou variação clara, encerre. Caso contrário, salve como `estilo_carrossel` (valores: `nunca`, `sempre`, `odeio`, `erros`, `amo`, `ninguem-conta`, `noticia`, `curiosidade`, `editorial`, `todos`).

---

## Passo 2. Ramo do fluxo

### Nota. Output triplo nos 6 estilos clássicos (verbatim)

Os 6 estilos clássicos (`nunca`, `sempre`, `odeio`, `erros`, `amo`, `ninguem-conta`) executam o respectivo `prompt-{estilo}.md` verbatim, MAS o Passo 3.4 desses prompts foi deprecado. A skill assume o controle entre o Passo 3.3 (comando Cowork) e o Passo 4 (legenda) do prompt verbatim, e aciona `references/passo-output-triplo.md` a partir da seção 3.3:

1. **Verbatim Passo 2 do prompt**. Gera 6 slides com gate de aprovação interno (Manual da Copy + revisora silenciosamente antes do gate).
2. **Verbatim Passo 3.1 do prompt**. Mostra os 6 prompts visuais em inglês no chat, slide por slide.
3. **Verbatim Passo 3.2 do prompt**. Salva `prompts.txt` consolidado em `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/prompts.txt`.
4. **Verbatim Passo 3.3 do prompt**. Exibe o comando pronto pra colar no Cowork (Claude in Chrome).
5. **Interceptação da skill**. Aciona `references/passo-output-triplo.md` a partir da seção 3.3 (detecção de capacidades) e 3.4 (menu dinâmico). Passa `tem_prompts_txt = true` para que a seção 3.5 caminho API reaproveite o arquivo já salvo. O menu sempre mostra "Manual no ChatGPT", e mostra "Claude in Chrome (só imagens)" quando MCP do Chrome está presente, e mostra "API paralela (OpenRouter ou OpenAI)" sempre (com aviso quando indisponível).
6. **Execução conforme escolha** (seção 3.5 do `passo-output-triplo.md`). Manual = nada extra; Chrome = abre via MCP e roda os 6 prompts; API = `scripts/gerar-imagens-api.py` em paralelo gerando 6 PNGs.
7. **Verbatim Passo 4 do prompt**. Gera a legenda do Instagram localmente (Manual da Copy + revisora), salva `legenda.txt`, mostra com aprovação obrigatória (4 opções). Não há mais variável `legenda_origem` nem captura de legenda do ChatGPT — fluxo único, sempre local.

A nota acima aplica-se a todos os 6 ramos clássicos. Cada ramo abaixo apenas declara qual prompt usar.

### Se `estilo_carrossel == nunca`

1. **Carregue** `references/estilos/nunca.md` e `references/prompt-nunca.md`.
2. **Execute o Passo 1 do `prompt-nunca.md`** (Coleta: 5 perguntas — nicho/produto, @ do Instagram, cores, tom, estilo de design), uma pergunta por turno, cabeçalho "Pergunta X de 5" e micro-resumo entre cada uma. Pré-preencha cada pergunta com a sugestão correspondente do `perfil.md` / `.env` quando existir, no formato "Sugestão a partir do seu produto: {valor}. Confirme ou corrija."
3. **Vá para o Passo 2.5** (confirmação consolidada).
4. Após confirmação, **execute o `prompt-nunca.md` com a interceptação do output triplo** conforme a "Nota. Output triplo nos 6 estilos clássicos (verbatim)" acima. Sequência: Passo 2 do prompt → Passo 3.1, 3.2, 3.3 do prompt → menu dinâmico via `passo-output-triplo.md` → execução do caminho escolhido → Passo 4 do prompt (legenda).
5. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-nunca/` (`texto.md` + `prompts.txt` + `legenda.txt`; opcionalmente `imagens/` se o aluno escolheu API paralela).
6. **Vá direto para o Passo 6** (entrega).

### Se `estilo_carrossel == sempre`

1. **Carregue** `references/estilos/sempre.md` e `references/prompt-sempre.md`.
2. **Execute o Passo 1 do `prompt-sempre.md`** (Coleta: 5 perguntas — nicho/produto, @ do Instagram, cores, tom, estilo de design), uma pergunta por turno, cabeçalho "Pergunta X de 5" e micro-resumo entre cada uma. Pré-preencha sugestões do `perfil.md` / `.env` quando existir.
3. **Vá para o Passo 2.5** (confirmação consolidada).
4. Após confirmação, **execute o `prompt-sempre.md` com a interceptação do output triplo** conforme a "Nota. Output triplo nos 6 estilos clássicos (verbatim)" acima.
5. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-sempre/` (`texto.md` + `prompts.txt` + `legenda.txt`; opcionalmente `imagens/`).
6. **Vá direto para o Passo 6** (entrega).

### Se `estilo_carrossel == odeio`

1. **Carregue** `references/estilos/odeio.md` e `references/prompt-odeio.md`.
2. **Execute o Passo 1 do `prompt-odeio.md`** (Coleta: 5 perguntas), uma pergunta por turno, cabeçalho "Pergunta X de 5" e micro-resumo entre cada uma. Pré-preencha sugestões do `perfil.md` / `.env`.
3. **Vá para o Passo 2.5**.
4. Após confirmação, **execute o `prompt-odeio.md` com a interceptação do output triplo** conforme a "Nota. Output triplo nos 6 estilos clássicos (verbatim)" acima.
5. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-odeio/` (`texto.md` + `prompts.txt` + `legenda.txt`; opcionalmente `imagens/`).
6. **Vá direto para o Passo 6**.

### Se `estilo_carrossel == erros`

1. **Carregue** `references/estilos/erros.md` e `references/prompt-erros.md`.
2. **Execute o Passo 1 do `prompt-erros.md`** (Coleta: 6 perguntas — nicho/produto, @ do Instagram, cores, tom, estilo de design e desejo do público), uma pergunta por turno, cabeçalho "Pergunta X de 6" e micro-resumo entre cada uma. Pré-preencha sugestões do `perfil.md` / `idconsumidor.md` / `.env`. O desejo é derivado do Quadro do produto quando possível.
3. **Vá para o Passo 2.5**.
4. Após confirmação, **execute o `prompt-erros.md` com a interceptação do output triplo** conforme a "Nota. Output triplo nos 6 estilos clássicos (verbatim)" acima.
5. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-erros/` (`texto.md` + `prompts.txt` + `legenda.txt`; opcionalmente `imagens/`).
6. **Vá direto para o Passo 6**.

### Se `estilo_carrossel == amo`

1. **Carregue** `references/estilos/amo.md` e `references/prompt-amo.md`.
2. **Execute o Passo 1 do `prompt-amo.md`** (Coleta: 5 perguntas), uma pergunta por turno, cabeçalho "Pergunta X de 5" e micro-resumo entre cada uma. Pré-preencha sugestões do `perfil.md` / `.env`.
3. **Vá para o Passo 2.5**.
4. Após confirmação, **execute o `prompt-amo.md` com a interceptação do output triplo** conforme a "Nota. Output triplo nos 6 estilos clássicos (verbatim)" acima.
5. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-amo/` (`texto.md` + `prompts.txt` + `legenda.txt`; opcionalmente `imagens/`).
6. **Vá direto para o Passo 6**.

### Se `estilo_carrossel == ninguem-conta`

1. **Carregue** `references/estilos/ninguem-conta.md` e `references/prompt-ninguem-conta.md`.
2. **Execute o Passo 1 do `prompt-ninguem-conta.md`** (Coleta: 6 perguntas — nicho/produto, @ do Instagram, cores, tom, estilo de design e objetivo do público), uma pergunta por turno, cabeçalho "Pergunta X de 6" e micro-resumo entre cada uma. Pré-preencha sugestões do `perfil.md` / `idconsumidor.md` / `.env`. O objetivo é derivado do Quadro do produto quando possível.
3. **Vá para o Passo 2.5**.
4. Após confirmação, **execute o `prompt-ninguem-conta.md` com a interceptação do output triplo** conforme a "Nota. Output triplo nos 6 estilos clássicos (verbatim)" acima.
5. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-ninguem-conta/` (`texto.md` + `prompts.txt` + `legenda.txt`; opcionalmente `imagens/`).
6. **Vá direto para o Passo 6**.

### Se `estilo_carrossel == noticia`

1. **Carregue** `references/estilos/noticia.md` e `references/prompt-noticia.md`.
2. **Execute a Etapa 1 do `prompt-noticia.md`** (@ do Instagram, nicho, produto), uma pergunta por turno, cabeçalho "Pergunta X de 3" e micro-resumo entre cada uma. Pré-preencha cada pergunta com a sugestão correspondente do `perfil.md` / `.env` quando existir, no formato "Sugestão a partir do seu produto: {valor}. Confirme ou corrija."
3. **Vá para o Passo 2.5** (confirmação consolidada).
4. Após confirmação, **execute o `prompt-noticia.md` exatamente como está**, da Etapa 2 à Etapa 7, na sessão atual. Não reescreva nem resuma o prompt. A busca de notícias trend (Etapa 2) usa `WebSearch` com regra de frescor obrigatório (últimos 7 dias). A data para o nome do arquivo consolidado é calculada via `Bash` com `Get-Date -Format "yyyy-MM-dd"` (PowerShell).
5. O texto dos slides passa pelo **Manual da Copy + revisora** de forma silenciosa antes da Etapa 6. As regras de copy do prompt (sem travessão, sem exclamação, sem pergunta na capa) já estão alinhadas com o Manual.
6. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-noticia/` (`texto.md` + o arquivo consolidado `carrossel-noticia-{slug}-{data}.txt`).
7. **Vá direto para o Passo 6** (entrega).

> **Diferença para o `/programar-carrossel-noticia`.** Aquela skill (agendamento) continua usando o arquivo parametrizado `programar-carrossel-noticia/references/prompt-carrossel-noticia.md` com placeholders e configurações de categoria/modo/tom. Esta branch (`/carrossel` opção 7, geração imediata) usa o novo `references/prompt-noticia.md` interativo. Os dois arquivos coexistem por desenho: um pra Routine, outro pra sessão interativa.

### Se `estilo_carrossel == curiosidade`

1. **Carregue** `references/estilos/curiosidade.md` e `references/prompt-curiosidade.md`.
2. **Execute a Etapa 1 do `prompt-curiosidade.md`** (@ do Instagram, nicho, produto), uma pergunta por turno, com cabeçalho "Pergunta X de 3" e micro-resumo entre cada uma. Pré-preencha cada pergunta com o valor correspondente do `perfil.md` quando existir, no formato "Sugestão a partir do seu produto: {valor}. Confirme ou corrija."
3. **Vá para o Passo 2.5** (confirmação consolidada).
4. Após confirmação, **execute o `prompt-curiosidade.md` exatamente como está**, da Etapa 2 à Etapa 7, na sessão atual. Não reescreva nem resuma o prompt. A busca de curiosidades atemporais (Etapa 2) usa `WebSearch`. A data para o nome do arquivo consolidado é calculada via `Bash` com `Get-Date -Format "yyyy-MM-dd"` (PowerShell).
5. O texto dos slides passa pelo **Manual da Copy + revisora** de forma silenciosa antes da Etapa 6. As regras de copy do prompt já estão alinhadas com o Manual, então a revisão garante o padrão sem alterar o prompt.
6. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-curiosidade/` (`texto.md` + o arquivo consolidado `carrossel-curiosidade-{slug}-{data}.txt`).
7. **Vá direto para o Passo 6** (entrega).

### Se `estilo_carrossel == editorial`

1. **Carregue** `references/estilos/editorial.md` e `references/prompt-editorial.md`.
2. **Execute o Passo 1 do `prompt-editorial.md`** (Briefing: produto/serviço e público), uma pergunta por turno, cabeçalho "Pergunta X de 3" e micro-resumo entre cada uma. Pré-preencha cada pergunta com a sugestão correspondente do `perfil.md` / `idconsumidor.md` quando existir, no formato "Sugestão a partir do seu produto: {valor}. Confirme ou corrija."
3. **Execute o Passo 2 do prompt** (Tipo de CTA do slide 6: ManyChat, Seguir, Engajar, Salvar). Salve como `editorial_cta_tipo`.
4. **Vá para o Passo 2.5** (confirmação consolidada).
5. Após confirmação, **execute o `prompt-editorial.md` exatamente como está**, do Passo 3 ao Passo 5, na sessão atual. Não reescreva nem resuma o prompt. O Passo 3 gera as 10 ideias com ângulos variados (notícia real, polêmica, conta maluca, pesquisa científica, comparação) e pede a escolha; o Passo 4 entrega os 6 slides + a legenda do Instagram e pede aprovação; o Passo 5 entrega o prompt único pra colar no ChatGPT.
6. O texto dos 6 slides passa pelo **Manual da Copy + revisora** de forma silenciosa antes do gate de aprovação do Passo 4 do prompt. As regras de copy do prompt (sem travessão, dados específicos em negrito, corpo em fonte regular, compliance sem doença/remédio) já estão alinhadas com o Manual.
7. **Salve em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-editorial/` (`texto.md` com os 6 slides + legenda embutida + `prompt-chatgpt.txt` com o prompt único do Passo 5).
8. **Vá direto para o Passo 6** (entrega).

### Se `estilo_carrossel == todos`

**O fluxo "Gerar todos" usa aprovação em lotes (1 carrossel por vez na revisão) e cache de retomada.**

#### 2.A. Confirmação inicial

Exiba SOMENTE este bloco e pare:

```
Vou gerar os 9 carrosséis em sequência. Para isso, preciso coletar:

- 5 dados base (@, nicho/produto, paleta, tom default, estilo de design)
- 1 dado específico de Erros (desejo do público)
- 1 dado específico de Ninguém Conta (objetivo do público)
- 1 dado específico de Curiosidade (tom)
- 1 dado específico de Editorial (tipo de CTA do slide 6)
- 3 dados específicos de Notícia (categoria, modo, tom)

São 12 perguntas no total. Depois eu gero os textos e te mostro 1 carrossel por vez para você aprovar (você pode aprovar todos automaticamente também).

1. Sim, gerar todos os 9 (inclui Notícia da semana, Curiosidade e Editorial, com WebSearch quando necessário)
2. Pular Notícia (mais rápido, gera 8, ainda inclui Curiosidade e Editorial)
3. Cancelar

Digite o número.
```

AGUARDE A RESPOSTA. Se `2`, salve `pular_noticia = true`. Se `3`, encerre.

> A Curiosidade e o Editorial não são puláveis pela opção 2. A opção 2 pula apenas a Notícia da semana (busca de trend dos últimos 7 dias). A Curiosidade e o Editorial são atemporais e permanecem no lote.

#### 2.B. Coleta consolidada

Colete TODAS as variáveis necessárias em sequência, **uma pergunta por turno**, com cabeçalho "Pergunta X de 12" (ou X de 9 se pulou Notícia) e micro-resumo entre cada uma:

1. Handle (1.1 do `passo-coleta-base.md`)
2. Nicho e produto (1.2)
3. Cores da marca (1.3)
4. Tom default (1.4 versão base)
5. Estilo de design (1.5)
6. Desejo do público (extra de Erros)
7. Objetivo do público (extra de Ninguém Conta)
8. Curiosidade: tom (use as 7 opções de tom da Etapa 4 do `prompt-curiosidade.md`. Salve como `curiosidade_tom`)
9. Editorial: tipo de CTA do slide 6 (4 opções do Passo 2 do `prompt-editorial.md`: ManyChat, Seguir, Engajar, Salvar. Salve como `editorial_cta_tipo`)
10. Notícia: categoria (se não pulou)
11. Notícia: modo (se não pulou)
12. Notícia: tom (se não pulou)

> No modo "todos", o tema da Curiosidade e o tema do Editorial não são perguntados. A skill executa a busca da Etapa 2 do `prompt-curiosidade.md` e seleciona automaticamente a curiosidade mais forte das 5; e executa o Passo 3 do `prompt-editorial.md` e seleciona automaticamente a ideia mais forte das 10 (maior gancho com o público + dado mais sólido).

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
  "pendentes": ["nunca", "sempre", "odeio", "erros", "amo", "ninguem-conta", "curiosidade", "editorial", "noticia"],
  "variaveis": { ... }
}
```

(Remova `noticia` da lista de pendentes se `pular_noticia = true`. `curiosidade` e `editorial` nunca são removidos pela opção 2.)

Seja `{total}` o número de estilos na lista de pendentes (9 normalmente, 8 se pulou Notícia). Para cada estilo da lista, em ordem:

```
⏳ Passo {N}/{total}: gerando texto do carrossel "{Estilo}"...
```

1. Para os 6 estilos clássicos (`nunca`, `sempre`, `odeio`, `erros`, `amo`, `ninguem-conta`): execute o sub-fluxo do `references/estilos/{estilo}.md` no modo "Gerar todos" (pula o Passo 1 do respectivo `prompt-{estilo}.md` injetando os valores já coletados em 2.B; roda os Passos 2 a 4 sem gate interativo). Para Erros use o `desejo_publico` coletado em 2.B; para Ninguém Conta use o `objetivo_publico`.
2. Para `curiosidade`: execute o sub-fluxo do `references/estilos/curiosidade.md` no modo "Gerar todos" (busca via `WebSearch`, seleção automática do tema mais forte, tom = `curiosidade_tom`). Para `editorial`: execute o sub-fluxo do `references/estilos/editorial.md` no modo "Gerar todos" (gera as 10 ideias internamente, seleciona a mais forte, tipo de CTA = `editorial_cta_tipo`). Para `noticia`: execute o sub-fluxo do `references/estilos/noticia.md`.
3. Aplique o Manual da Copy + revisora silenciosamente.
4. Salve o `texto.md` em `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/texto.md`.
5. Atualize o arquivo de fila movendo o estilo de `pendentes` para `concluidos`.

#### 2.D. Aprovação em lotes (1 carrossel por vez)

Depois que os 8 (ou 7, se pulou Notícia) textos estiverem gerados, ofereça ao aluno:

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

(... até o último slide: 6 nos estilos atemporais, 7 a 9 na Notícia e na Curiosidade ...)

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
⏳ Passo {N}/{total}: gerando prompts visuais e legenda do carrossel "{Estilo}"...
```

1. Gere os 6 prompts visuais em inglês (usando `template-prompt-imagem.md` + ajustes do estilo) e mostre-os no chat. **Não salve `prompts.txt` em disco.**
   - Exceção `noticia`, `curiosidade` e `editorial`: os prompts visuais já são gerados pelo prompt-base do estilo (3 modos em português para Notícia e Curiosidade; UM prompt único para Editorial). Salve no formato próprio do estilo. Não use o `template-prompt-imagem.md` para esses três.
2. Gere a legenda do Instagram (Manual da Copy + revisora silenciosamente). Para `noticia` e `curiosidade`, a legenda já vem embutida no slide CTA final, não gere `legenda.txt` separado. Para `editorial`, a legenda é gerada junto com os 6 slides no Passo 4 do `prompt-editorial.md` e fica dentro do `texto.md`, sem `legenda.txt` separado.
3. Salve `legenda.txt` (estilos clássicos).

#### 2.F. Entrega consolidada

Após gerar tudo, **delete o arquivo `.carrossel-queue.json`** e exiba:

```
✅ {N} carrosséis gerados.

Cada carrossel tem: texto + prompts visuais + legenda (nos estilos atemporais a legenda é revisada à parte; na Notícia e na Curiosidade ela já vem no slide CTA final).

Pastas criadas em:
meus-produtos/{ativo}/entregas/conteudo-social/
├── carrossel-nunca/
├── carrossel-sempre/
├── carrossel-odeio/
├── carrossel-erros/
├── carrossel-amo/
├── carrossel-ninguem-conta/
├── carrossel-curiosidade/
├── carrossel-editorial/
└── carrossel-noticia/ (se você não pulou)

Em cada pasta:
- texto.md (slides do carrossel; no Editorial inclui a legenda do Instagram embutida)
- legenda.txt (legenda revisada, estilos clássicos)
- carrossel-curiosidade-{slug}-{data}.txt (arquivo consolidado, só na pasta da Curiosidade)
- prompt-chatgpt.txt (prompt único pra colar no ChatGPT, só na pasta do Editorial)

Os prompts visuais de cada carrossel já foram exibidos no chat durante a geração. Para gerar as imagens, copie-os e cole no ChatGPT (ou outra ferramenta), OU configure a `OPENROUTER_API_KEY` no `.env` rodando `/configurar-imagens` para usar a opção 3 (API paralela) na próxima execução. A Curiosidade também tem o arquivo consolidado `carrossel-curiosidade-{slug}-{data}.txt` na pasta dela.

Digite /carrossel para gerar outro, ou /programar-carrossel para agendar.
```

---

## Passo 2.5. Confirmação consolidada (modo individual e Notícia)

> Aplica para todos os 9 estilos no modo individual (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia, Curiosidade, Editorial). NÃO aplica para "todos" (que tem fluxo próprio). Todos os 6 clássicos agora têm ramo próprio (verbatim) e passam por aqui antes de executar o respectivo prompt-base.

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
{se Curiosidade} Vou buscar 5 curiosidades atemporais do nicho na web. Você escolhe 1 e o tom logo depois.
{se Editorial} Produto/serviço: {produto_servico} / Público: {publico} / Tipo de CTA do slide 6: {editorial_cta_tipo}. Vou gerar 10 ideias editoriais (notícia real, polêmica, conta maluca, pesquisa, comparação) e você escolhe 1.

Vou gerar:
- 6 slides de texto (estilos clássicos e Editorial) ou 7 a 9 slides (Notícia e Curiosidade)
- prompts visuais (6 em inglês nos clássicos; 3 modos em português na Notícia e na Curiosidade; 1 prompt único em português no Editorial)
- 1 legenda do Instagram revisada (estilos clássicos; na Notícia e na Curiosidade a legenda já está no slide CTA; no Editorial a legenda vem junto com os slides)
- 1 prompt opcional para Claude in Chrome

1. Tudo certo, gerar
2. Ajustar algo (diga qual campo)
3. Cancelar

Digite o número.
```

> Para Notícia e Curiosidade, exiba no resumo apenas os campos coletados (@, nicho e produto, mais o que for específico do estilo). Os campos de paleta, tom da copy e estilo de design não se aplicam a esses dois e podem ser omitidos.

AGUARDE A RESPOSTA.

- **Opção 1**: prossiga para a execução do prompt verbatim do estilo escolhido, a partir do passo correspondente do próprio prompt. Para os 6 clássicos (`nunca`, `sempre`, `odeio`, `erros`, `amo`, `ninguem-conta`) e para Notícia: a partir do Passo 2. Para Curiosidade: a partir da Etapa 2. Para Editorial: a partir do Passo 3.
- **Opção 2**: pergunte qual campo ajustar, refaça aquela pergunta, volte para mostrar o resumo de novo.
- **Opção 3**: encerre sem gerar.

---

## Passo 3. Geração dos 6 slides de texto (estilos atemporais individuais)

> **SEÇÃO LEGADA.** Nenhum estilo do modo individual usa o Passo 3 atualmente. Todos os 9 estilos (6 clássicos + Notícia + Curiosidade + Editorial) têm ramo próprio no Passo 2 que executa o respectivo prompt-base verbatim. Esta seção é mantida apenas como referência histórica do modelo leve que existia antes da migração. Para `todos` use o Passo 2.D.

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

> **SEÇÃO LEGADA.** Nenhum estilo do modo individual usa este Passo 4 atualmente. Os 9 estilos têm prompt verbatim que cuida do output dos prompts visuais (chat slide-a-slide + `prompts.txt` + comando Cowork), e a interceptação para o menu dinâmico é feita pela "Nota. Output triplo nos 6 estilos clássicos (verbatim)" acima, que chama `references/passo-output-triplo.md` a partir da seção 3.3. Esta seção é mantida apenas como referência para futuros estilos leves que não usem prompt verbatim.

Para estilos leves que não tenham prompt verbatim, anuncie:

```
⏳ Etapa 2/3: gerando os 6 prompts visuais em inglês...
```

E acione `references/passo-output-triplo.md` do começo (seção 3.1), passando `tem_prompts_txt = false`. O arquivo cuida de mostrar os 6 prompts no chat, detectar capacidades (Chrome MCP + API de imagem) e oferecer o menu dinâmico de 2 ou 3 opções (Manual / Chrome só imagens / API paralela). Não há mais variável `legenda_origem`, nem caminho "Chrome + legenda" (removido por desnecessário, já que a legenda sempre passa pelo Manual da Copy local).

---

## Passo 5. Geração da legenda

> **SEÇÃO LEGADA.** Nos 6 estilos clássicos verbatim, a legenda é gerada pelo Passo 4 do próprio `prompt-{estilo}.md`. Nos estilos Notícia, Curiosidade e Editorial, a legenda vem embutida no fluxo do prompt do estilo. Esta seção é mantida como referência para estilos leves futuros.

Para estilos leves que não tenham prompt verbatim, anuncie:

```
⏳ Etapa 3/3: processando a legenda do Instagram...
```

E acione `references/passo-legenda.md`. Fluxo único, sem branches:

1. Aplique o **Manual da Copy** + estrutura de gancho/desenvolvimento/pico/virada/ponte/CTA/hashtags.
2. Acione a **revisora** e aplique correções direto no texto.
3. **Mostre a legenda** no chat em bloco copiável.
4. **Salve em `legenda.txt`** na pasta do carrossel.
5. **Aprovação OBRIGATÓRIA com as 4 opções abaixo. Não simplifique para 2 opções, mesmo que pareça que tudo deu certo:**

```
1. Aprovar e salvar
2. Quero ajustar algo (diga o que)
3. Regenerar do zero
4. Cancelar

Digite o número.
```

Loop até aprovação. As opções 3 (regenerar) e 4 (cancelar) são parte do contrato do aluno com a skill, não devem ser cortadas em nenhuma execução.

---

## Passo 6. Entrega

Exiba:

```
✅ Carrossel "{Estilo}" gerado.

Arquivos salvos em:
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/
├── texto.md (slides do carrossel, já aprovados; no Editorial inclui a legenda embutida)
├── legenda.txt (legenda revisada do Instagram, estilos clássicos)
├── carrossel-curiosidade-{slug}-{data}.txt (arquivo consolidado, só na Curiosidade)
├── prompt-chatgpt.txt (prompt único pra colar no ChatGPT, só no Editorial)
└── imagens/ (se você escolheu a opção 3 da API paralela)

{Se aluno usou caminho Chrome MCP, incluir o link da conversa do ChatGPT aqui}
Conversa do ChatGPT com as 6 imagens:
{url_chatgpt}

Legenda pronta pra colar no Instagram:

---
{conteúdo da legenda.txt inline}
---

Próximos passos:
- Os prompts visuais já estão visíveis acima neste chat. Para gerar manualmente, copie cada bloco e cole no ChatGPT (ou outra ferramenta de imagem).
- Para automatizar tudo de uma vez no futuro, configure a `OPENROUTER_API_KEY` no `.env` rodando `/configurar-imagens` e use a opção 3.
- A legenda acima também está salva em legenda.txt na pasta do carrossel.

Quer gerar outro carrossel agora? Digite /carrossel.
Quer agendar carrosséis recorrentes? Digite /programar-carrossel.
```

**REGRA OBRIGATÓRIA. Exiba a legenda inline na entrega final, mesmo que ela já tenha sido mostrada antes no Passo 5.** O aluno acabou de aprovar os slides, ver os prompts visuais, talvez aguardar o Chrome rodar as imagens. O fluxo dele é longo e a legenda ficou no histórico do chat lá em cima. Repetir a legenda no bloco final é prática padrão pra ele copiar com 1 clique direto do último output da skill, sem precisar rolar a conversa nem abrir o `legenda.txt`.

> **Notícia, Curiosidade e Editorial.** Esses três estilos não geram `legenda.txt` separado. Notícia e Curiosidade têm a legenda dentro do slide CTA final; Editorial tem a legenda dentro do próprio `texto.md` (gerada junto com os slides no Passo 4 do prompt). Na entrega, omita as linhas de `legenda.txt`. Para a Curiosidade, informe o caminho do arquivo consolidado `carrossel-curiosidade-{slug}-{data}.txt`. Para o Editorial, informe o caminho de `prompt-chatgpt.txt` (o prompt único pra colar no ChatGPT) e instrua o aluno a colar esse prompt no ChatGPT e pedir "cria o 1", "cria o 2", até o 6. A árvore de arquivos acima é o caso geral; ajuste-a para o estilo entregue.

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
├── carrossel-curiosidade/
├── carrossel-editorial/
└── carrossel-noticia/
```

Cada pasta contém os arquivos descritos no Passo 6: `texto.md`, `legenda.txt` e (opcionalmente) a subpasta `imagens/` quando a opção 3 da API paralela é usada. A pasta `carrossel-curiosidade/` também recebe o arquivo consolidado `carrossel-curiosidade-{slug}-{data}.txt` (prompts visuais delimitados para automações). A pasta `carrossel-editorial/` recebe o `prompt-chatgpt.txt` (prompt único pra colar no ChatGPT).
