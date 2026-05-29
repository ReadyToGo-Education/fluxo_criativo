# Arquitetura do Repositorio. Guia Tecnico Completo

Este documento explica como o repositorio `workshop_inteligente` esta estruturado e como inserir novas capacidades (commands, agents, skills, ferramentas). Escrito para ser lido por humanos e LLMs que precisem entender, manter ou expandir o projeto.

---

## 1. Visao Geral do Projeto

Este repositorio e um **toolkit de marketing digital para infoprodutores** que roda dentro do **Claude Code** (extensao do VSCode). Nao e um projeto de software tradicional com codigo executavel. e um sistema de prompts estruturados que transforma o Claude em um consultor de marketing.

**Cursor:** o mesmo toolkit funciona no **Cursor** com a pasta do projeto aberta. O runtime e o chat do Cursor; regras em `.cursor/rules/*.mdc` e `CLAUDE.md` substituem a extensao. Os arquivos em `.claude/commands/` **nao** viram slash automaticamente no Cursor: o agente deve **ler o `.md`** correspondente quando o usuario pedir o fluxo (ou usar `@` no arquivo).

**Stack:**
- Claude Code (extensao VSCode) ou Cursor como runtime do chat
- Arquivos Markdown como instrucoes (prompts)
- HTML/CSS como output (paginas de vendas)
- Metodologia VTSD (Venda Todo Santo Dia) como base de conhecimento

**O que o toolkit produz:**
- Paginas de vendas, captura e obrigado (HTML)
- Textos persuasivos (copy, headlines, VSL)
- Anuncios para Meta Ads e Google Ads
- Conteudo para redes sociais (carrosseis, Reels)
- Scripts comerciais (SPIN Selling)
- Sequencias de email
- Roteiros de video

---

## 2. Mapa Completo de Arquivos

```
workshop_inteligente/
│
├── CLAUDE.md                              ← ARQUIVO CENTRAL: papel do assistente, regras e comportamento
├── AGENTS.md                              ← Mapa rapido para agentes (Cursor / IDEs)
├── ARQUITETURA.md                         ← ESTE ARQUIVO (guia tecnico completo)
├── README.md                              ← Documentacao publica para o usuario final
├── COMO-USAR.md                           ← Guia passo a passo para o usuario
├── .env.example                           ← Modelo de chaves API (opcional)
├── .gitignore                             ← Protege .env, meus-produtos/ e dados do aluno
├── .cursor/rules/                         ← Regras Cursor (.mdc, alwaysApply ou globs)
│
├── .claude/                               ← NUCLEO DO SISTEMA Claude Code
│   ├── settings.json                      ← Permissoes de escrita/leitura/execucao
│   │
│   ├── commands/                          ← SLASH COMMANDS (~90 arquivos, atalhos /comando)
│   │   Organizados por categoria: /produto-*, /copy-*, /lt-*, /ht-*, /pagina-*,
│   │   /video-*, /toolkit-*, /configurar-*, /estrategia-*, /feedback-*, etc.
│   │
│   ├── agents/                            ← AGENTES AUTONOMOS (subprocessos)
│   │   Orquestradores e especialistas: estrategista-de-produto, estrategista-low-ticket,
│   │   estrategista-middle-ticket, construtor-de-paginas, clonador-de-bloco-visual,
│   │   criador-de-campanhas, copywriter, video-maker, consultor-comercial,
│   │   executor-de-plano-de-acao.
│   │
│   └── skills/                            ← BASE DE CONHECIMENTO
│       ├── vtsd-completo/                 ← Metodologia VTSD integral
│       ├── concepcao-produto/             ← Quadro, Furadeira, 3 Identidades, Urgencias
│       ├── paginas/                       ← Estrutura 8D, design system, referencias HTML
│       ├── anuncios/, anuncios-texto/, anuncios-video/ ← Mandala 18 tipos, formatos
│       ├── conteudo/                      ← Reels, carrosseis, elementos literarios
│       ├── trafego-pago/                  ← Campanhas, pixel, metricas
│       ├── revisora/                      ← Checklist Light Copy aplicado a todo output
│       ├── pesquisa-mercado/              ← Reclame Aqui, SEBRAE, concorrentes
│       ├── pagina-checkout/, pagina-pixel/, pagina-lovable/, pagina-performance/,
│       │   pagina-active/, pagina-precheckout/ ← Skills de infraestrutura de pagina
│       ├── instagram-dashboard/, tiktok-dashboard/, youtube-dashboard/ ← Dashboards
│       ├── dados-instagram/, dados-nicho/ ← Analise pontual de perfis e nicho
│       ├── furadeira-visual/, canvas-design/, ui-reverse-engineer/ ← Visuais
│       └── tutorial-ferramentas/, ferramentas/, agente-gpt/, app-saas/, etc.
│
├── scripts/                               ← UTILITARIOS PYTHON/POWERSHELL
│   ├── README-creative.md                 ← Processo de criacao de criativos
│   ├── painel-incremental.py              ← Gera/atualiza painel-entregas.html por secao
│   ├── painel_template.py                 ← Shell HTML e renderers do painel
│   ├── painel-atualizar.py                ← Regenera meus-produtos/index.js
│   ├── montar-pagina-copias.py            ← Monta HTML final de copias de secao
│   ├── playbook-montar.py                 ← Monta HTML do playbook comercial
│   ├── playbook-briefing.py               ← Gera briefing do playbook
│   ├── generate-avatar-video.py           ← Aciona HeyGen via API
│   ├── generate-creative.py               ← Geracao de criativos visuais
│   ├── generate-openrouter-nano-banana-images.py
│   └── relatorio-ads.ps1                  ← Rotina diaria Facebook Ads -> WhatsApp
│
├── meus-produtos/                         ← DADOS DO ALUNO (ignorado pelo git)
│   ├── .ativo                             ← Slug do produto ativo
│   ├── index.js                           ← Manifest gerado (alimenta seletor do painel-entregas.html)
│   └── {slug-do-produto}/                 ← Um diretorio por produto
│       ├── perfil.md                      ← Gerado por /produto-concepcao
│       ├── idconsumidor.md                ← Gerado automaticamente no fim do /produto-concepcao
│       ├── pesquisa-mercado.md, tipo.md, nome.txt (opcional)
│       ├── painel-entregas.html           ← Painel por produto
│       └── entregas/                      ← Output do assistente
│           ├── paginas/                   ← Arquivos .html
│           ├── copy-pagina/, emails/, criativos/,
│           │   comercial/, videos/, produto/, textos-de-venda/
│
├── docs/                                  ← PLANS E RASCUNHOS LOCAIS (ignorado pelo git)
│
└── _prompts-gpt/                          ← MATERIAL COMPLEMENTAR DO WORKSHOP
    ├── vtsd-completo.skill                ← Prompt original do GPT
    └── vtsd-extraido/                     ← Versao extraida
```

---

## 3. Conceitos Fundamentais

O sistema usa 5 tipos de componentes. Cada um tem um papel especifico:

### 3.1 CLAUDE.md (Role. Persona do Assistente)

**O que e:** Arquivo raiz que define QUEM o Claude e neste projeto. E carregado automaticamente em TODA conversa.

**O que contem:**
- Idioma (Portugues do Brasil)
- Persona (consultor de marketing, nao programador)
- Regras de comportamento (perguntar antes de gerar, Light Copy, nunca mostrar codigo)
- Padrao de UX da entrevista (perguntas numeradas, progresso visual, confirmacao)
- Metodologia base (VTSD. Quadro, Furadeira, Decorados, etc.)
- Contexto persistente (onde ler perfil.md e idconsumidor.md)
- Tabela de onde salvar cada tipo de entrega
- Padrao de qualidade para HTML
- Fluxo padrao de 6 passos (Contexto, Entrevista, Confirmacao, Geracao, Aprovacao, Entrega)
- Lista de todos os comandos disponiveis (apresentacao na primeira interacao)

**Impacto:** Tudo que esta aqui afeta TODOS os comandos e agentes. Alteracoes neste arquivo mudam o comportamento global.

### 3.2 Commands (Slash Commands. `/comando`)

**O que sao:** Atalhos que o usuario digita no chat (ex: `/produto-concepcao`, `/copy-anuncio`). Cada command e um arquivo `.md` na pasta `.claude/commands/`.

**Como o Claude Code encontra:** Automaticamente. qualquer `.md` dentro de `.claude/commands/` vira um slash command. O nome do arquivo (sem extensao) e o nome do comando.

**Como funciona na pratica:**
1. Usuario digita `/produto-concepcao` no chat
2. Claude Code carrega `.claude/commands/produto-concepcao.md`
3. O conteudo do arquivo e injetado como instrucao no contexto do Claude
4. O Claude segue as instrucoes do command + as regras do CLAUDE.md

### 3.3 Agents (Agentes Autonomos)

**O que sao:** Subprocessos especializados que executam tarefas complexas de forma autonoma, sem interacao do usuario. Cada agent e um arquivo `.md` na pasta `.claude/agents/`.

**Diferenca entre Command e Agent:**
- **Command:** Conversa interativa. O Claude faz perguntas, espera respostas, gera o material passo a passo.
- **Agent:** Autonomo. Recebe a tarefa, le os arquivos necessarios, executa tudo sozinho e entrega o resultado final.

**Como o Claude Code encontra:** Automaticamente. qualquer `.md` dentro de `.claude/agents/` fica disponivel como agente.

**Como funciona na pratica:**
1. O CLAUDE.md ou outro command aciona o agente pelo nome
2. Claude Code cria um subprocesso com o conteudo do agent como instrucao
3. O agente executa autonomamente (le arquivos, gera output, salva)
4. Retorna o resultado para a conversa principal

### 3.4 Skills (Base de Conhecimento)

**O que sao:** Documentos de referencia que contem conhecimento especializado. Ficam em `.claude/skills/`. NAO sao acionados diretamente pelo usuario. sao consultados pelos commands e agents.

**Estrutura de uma skill:**
```
skills/
└── nome-da-skill/
    ├── SKILL.md              ← Documento principal (obrigatorio)
    └── references/           ← Material de apoio (opcional)
        ├── exemplos.md
        └── templates.md
```

**Relacao com commands/agents:** Os commands e agents referenciam as skills nos seus textos (ex: "Leia `.claude/skills/paginas/SKILL.md`"). A skill fornece o conhecimento; o command/agent fornece o fluxo de trabalho.

---

## 4. Fluxo de Dados entre Componentes

```
USUARIO
  │
  ├── digita /comando ──────────► COMMAND (.claude/commands/X.md)
  │                                  │
  │                                  ├── le ► meus-produtos/{ativo}/perfil.md (contexto do produto)
  │                                  ├── le ► meus-produtos/{ativo}/idconsumidor.md (contexto do publico)
  │                                  ├── consulta ► SKILL (base de conhecimento)
  │                                  │
  │                                  └── salva ► meus-produtos/{ativo}/entregas/[tipo]/[arquivo]
  │
  └── (ou agente e acionado) ───► AGENT (.claude/agents/X.md)
                                     │
                                     ├── le ► meus-produtos/{ativo}/perfil.md
                                     ├── le ► meus-produtos/{ativo}/idconsumidor.md
                                     ├── consulta ► SKILL (base de conhecimento)
                                     ├── le ► .env (chaves opcionais)
                                     │
                                     └── salva ► meus-produtos/{ativo}/entregas/[tipo]/[arquivo]
```

**Ordem recomendada de uso:**
1. `/produto-concepcao` → gera `meus-produtos/{ativo}/perfil.md`, `idconsumidor.md` e `painel-entregas.html` em fluxo unico
2. Qualquer outro comando → le perfil.md e idconsumidor.md como contexto

---

## 5. Como Adicionar um Novo COMMAND (Slash Command)

### Passo 1. Criar o arquivo

Crie um arquivo `.md` em `.claude/commands/` com o nome do comando.

**Exemplo:** Para criar o comando `/webinar`, crie `.claude/commands/webinar.md`.

### Passo 2. Estrutura obrigatoria do arquivo

```markdown
---
name: workshop-marketing:webinar
description: Criar estrutura completa de webinar. roteiro, slides, CTA e follow-up.
---

# Webinar. Estrutura Completa

Cria roteiro de webinar com [descricao do que faz].

## Usage

```
/webinar
```

## O Que Fazer

### 1. Contexto
Leia `meus-produtos/{ativo}/perfil.md`. Se nao existir, oriente a usar `/produto-concepcao` primeiro.

### 2. Entrevista (UMA pergunta por vez, com progresso visual)

**Bloco 1/N. [Tema]:**

Pergunta 1:
```
[Pergunta com opcoes numeradas OU pergunta aberta com exemplo]
```

[... mais perguntas ...]

```
--- Bloco 1/N concluido ---
[Resumo do que foi coletado]
Proximo: [nome do proximo bloco]
---
```

### 3. Confirmacao
```
Resumo do que vou criar:
- [item 1]
- [item 2]
- [item 3]

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 4. Gerar Entregavel
[Instrucoes detalhadas de como gerar o material]
Salvar em `meus-produtos/{ativo}/entregas/[pasta]/[nome-arquivo].md`

### 5. Proximo Passo
"Material salvo em [caminho]. Use `/[proximo-comando]` para [proxima acao sugerida]."
```

### Passo 3. Frontmatter obrigatorio

O frontmatter YAML no topo do arquivo deve conter:

| Campo | Formato | Exemplo |
|---|---|---|
| `name` | `workshop-marketing:[nome]` | `workshop-marketing:webinar` |
| `description` | Frase que descreve o que o comando faz | `Criar estrutura completa de webinar...` |

### Passo 4. Seguir o padrao de UX

Conforme definido no CLAUDE.md, TODOS os commands devem seguir:
- Perguntas com opcoes sempre numeradas
- Perguntas abertas com exemplo entre parenteses
- Progresso entre blocos (ex: `--- Bloco 2/6 concluido ---`)
- Confirmacao com resumo antes de gerar
- UMA pergunta por mensagem (nunca duas)

### Passo 5. Referenciar skills quando necessario

Se o command precisa de conhecimento especializado, adicione no final:

```markdown
## Referencias
ANTES de gerar, leia:
- `.claude/skills/[skill-relevante]/SKILL.md`
```

### Passo 6. Registrar no CLAUDE.md

Adicione o novo comando na lista de comandos disponiveis na secao "Primeira Interacao" do CLAUDE.md, na categoria adequada.

### Passo 7. Registrar no README.md e COMO-USAR.md

Adicione o comando nas tabelas de comandos disponiveis desses arquivos.

### Checklist de um novo command:

- [ ] Arquivo `.md` criado em `.claude/commands/`
- [ ] Frontmatter com `name` e `description`
- [ ] Secao `Usage` com o comando
- [ ] Passo 1: Contexto (ler perfil.md)
- [ ] Passo 2: Entrevista (perguntas uma por vez, com progresso)
- [ ] Passo 3: Confirmacao (resumo + opcoes 1/2)
- [ ] Passo 4: Geracao (instrucoes detalhadas)
- [ ] Passo 5: Entrega (salvar + sugerir proximo comando)
- [ ] Referencia a skills relevantes
- [ ] Registrado no CLAUDE.md (lista de comandos)
- [ ] Registrado no README.md
- [ ] Registrado no COMO-USAR.md

---

## 6. Como Adicionar um Novo AGENT (Agente Autonomo)

### Passo 1. Criar o arquivo

Crie um arquivo `.md` em `.claude/agents/` com o nome do agente (kebab-case).

**Exemplo:** `.claude/agents/planejador-de-webinar.md`

### Passo 2. Estrutura obrigatoria do arquivo

```markdown
---
name: planejador-de-webinar
description: Agente autonomo que cria estrutura completa de webinar. roteiro, slides, CTA e follow-up. Le o perfil do negocio e gera tudo sem intervencao.
tools: Read, Write, Edit
model: sonnet
---

# Planejador de Webinar. Agente Autonomo

Voce e um [especialidade]. Seu papel e [objetivo].

## Idioma
SEMPRE em Portugues do Brasil.

## Sua Missao
[Descricao clara do que o agente deve produzir]

## Como Trabalhar

### 1. Ler Contexto
- Leia `meus-produtos/{ativo}/perfil.md` para entender o produto
- Leia `meus-produtos/{ativo}/idconsumidor.md` para entender o publico
- Use Quadro, Furadeira, Decorados e Urgencias Ocultas como base

### 2. [Etapa especifica do agente]
[Instrucoes detalhadas]

### 3. [Outra etapa]
[Instrucoes detalhadas]

### N. Salvar
- Salvar em `meus-produtos/{ativo}/entregas/[pasta]/[nome-arquivo].[extensao]`

### N+1. Informar
NUNCA mostre codigo ao aluno.
Sugira: "Use `/[proximo-comando]` para [proxima acao]."

## Referencias
ANTES de gerar, leia:
- `.claude/skills/[skill]/SKILL.md`
```

### Passo 3. Frontmatter obrigatorio

| Campo | Formato | Obrigatorio | Descricao |
|---|---|---|---|
| `name` | kebab-case | Sim | Nome unico do agente |
| `description` | Texto descritivo | Sim | O que o agente faz (aparece na listagem) |
| `tools` | Lista separada por virgula | Sim | Ferramentas que o agente pode usar |
| `model` | `sonnet`, `opus`, `haiku` | Nao | Modelo a ser usado (padrao: herda do pai) |

**Tools disponiveis para agents:**
- `Read`. Ler arquivos do projeto
- `Write`. Criar novos arquivos
- `Edit`. Editar arquivos existentes

A maioria dos agents usa `tools: Read, Write, Edit`.

### Passo 4. Diferenca de design: Command vs Agent

| Aspecto | Command | Agent |
|---|---|---|
| Interatividade | Conversa com o usuario | Autonomo, sem interacao |
| Perguntas | 3-5 perguntas, uma por vez | No maximo 1-2 antes de executar |
| Fluxo | 5 passos (contexto, entrevista, confirmacao, geracao, entrega) | Le contexto e executa direto |
| Complexidade | Tarefa unica e focada | Tarefa completa multi-etapa |
| Quando usar | Usuario quer controle | Usuario quer resultado rapido |

### Passo 5. Registrar no CLAUDE.md

Adicione o agente na secao "Agentes Especialistas" da lista de comandos no CLAUDE.md.

### Checklist de um novo agent:

- [ ] Arquivo `.md` criado em `.claude/agents/`
- [ ] Frontmatter com `name`, `description`, `tools`
- [ ] Instrucoes de leitura de contexto (perfil.md, idconsumidor.md)
- [ ] Etapas claras de execucao
- [ ] Instrucoes de onde salvar o output
- [ ] Referencia a skills relevantes
- [ ] Regra "nunca mostrar codigo"
- [ ] Registrado no CLAUDE.md

---

## 7. Como Adicionar uma Nova SKILL (Base de Conhecimento)

### Passo 1. Criar a pasta e o arquivo

Crie uma pasta em `.claude/skills/` com o nome da skill (kebab-case).
Dentro dela, crie `SKILL.md` (obrigatorio, com esse nome exato).

**Exemplo:**
```
.claude/skills/webinars/
├── SKILL.md
└── references/           ← opcional
    └── exemplos-webinar.md
```

### Passo 2. Estrutura do SKILL.md

```markdown
---
name: webinars
description: >
  Base de conhecimento para criacao de webinars.
  Inclui estrutura de roteiro, formatos de apresentacao e CTAs.
  Acionada pelo command /webinar e agent planejador-de-webinar.
---

# Webinars. Base de Conhecimento

## [Topico 1]
[Conteudo de referencia detalhado]

## [Topico 2]
[Conteudo de referencia detalhado]

## [Topico N]
[Conteudo de referencia detalhado]
```

### Passo 3. Frontmatter obrigatorio

| Campo | Formato | Descricao |
|---|---|---|
| `name` | kebab-case | Nome unico da skill |
| `description` | Texto multi-linha (use `>`) | Descricao detalhada. IMPORTANTE: inclua palavras-chave que ativam a skill e quais commands/agents a usam |

### Passo 4. Pasta `references/` (opcional)

Use para material de apoio volumoso que nao cabe no SKILL.md principal:
- Exemplos de copy
- Templates HTML
- Listas de formatos
- Dados de referencia

**Convencao de nomes:** kebab-case, descritivo. Ex: `exemplos-criativos.md`, `formatos-meta-ads.md`.

### Passo 5. Conectar com commands/agents

Adicione referencia na secao `## Referencias` dos commands e agents que precisam dessa skill:

```markdown
## Referencias
ANTES de gerar, leia:
- `.claude/skills/webinars/SKILL.md`
```

### Principios para boas skills:

1. **Conteudo de referencia, nao instrucao.** A skill contem CONHECIMENTO (o que sao os 18 tipos de anuncio). O command/agent contem INSTRUCAO (como conduzir a entrevista e gerar o output).
2. **Atomica.** Uma skill = um dominio de conhecimento. Nao misture anuncios com paginas.
3. **Completa.** Tudo que o Claude precisa saber sobre o tema deve estar na skill ou nos references.
4. **Sem duplicacao.** Se a informacao ja esta em outra skill, referencie em vez de copiar.

---

## 8. Como Adicionar uma Nova Ferramenta/Integracao

### Passo 1. Adicionar chave no .env.example

Siga o padrao existente:

```bash
# ══════════════════════════════════════════
# NOME_DA_FERRAMENTA. Descricao curta
# ══════════════════════════════════════════
# Usado por: /comando, agent nome-do-agente
# Obter em: https://url-para-obter-chave
NOME_DA_CHAVE=
```

### Passo 2. Documentar na skill de ferramentas

Adicione a nova ferramenta em `.claude/skills/ferramentas/SKILL.md` seguindo o padrao:

```markdown
### Nome da Ferramenta. Descricao

**O que faz:** [descricao funcional]
**Usada por:** [lista de commands e agents]
**Chave necessaria:** `NOME_DA_CHAVE`

**Como configurar:**
1. [passo 1]
2. [passo 2]

**Como o toolkit usa:**
[explicacao de como o Claude usa a ferramenta]

**Sem a chave:** [comportamento fallback]
```

### Passo 3. Atualizar commands/agents que usam a ferramenta

Adicione a logica de verificacao de chave no command ou agent:

```markdown
### N. Integracao com [Ferramenta] (se configurado)
Apos [acao], leia `.env` e verifique se existe `NOME_DA_CHAVE`.
Se existir, [acao automatizada].
Se nao existir, informe: "[fallback manual]."
```

### Passo 4. Atualizar permissoes se necessario

Se a ferramenta requer execucao de comandos bash, adicione a permissao em `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(nome-ferramenta *)"
    ]
  }
}
```

---

## 9. settings.json. Permissoes

O arquivo `.claude/settings.json` controla quais acoes o Claude Code pode executar sem pedir confirmacao ao usuario.

**Estrutura atual:**
```json
{
  "permissions": {
    "allow": [
      "Write(meus-produtos/{ativo}/entregas/**)",        ← Pode criar/editar arquivos em meus-produtos/{ativo}/entregas/
      "Write(meus-produtos/{ativo}/**)",     ← Pode criar/editar perfil.md e idconsumidor.md
      "Write(docs/**)",            ← Pode criar/editar documentacao
      "Read(.claude/commands/**)", ← Pode ler comandos
      "Read(.claude/skills/**)",   ← Pode ler skills
      "Read(scripts/**)",          ← Pode ler scripts
      "Read(meus-produtos/**)",    ← Pode ler produtos locais
      "Bash(ls *)",               ← Pode listar arquivos
      "Bash(vercel *)",           ← Pode fazer deploy
      "Bash(python3)"             ← Pode rodar Python quando necessario
    ]
  }
}
```

**Para adicionar permissao para uma nova ferramenta:**
Adicione uma nova linha no array `allow` com o padrao `"Bash(comando *)"`.

**Padroes de permissao:**
- `Write(pasta/**)`. Permite escrita recursiva na pasta
- `Read(pasta/**)`. Permite leitura recursiva apenas na pasta definida
- `Bash(comando *)`. Permite executar o comando com qualquer argumento
- Nao autorize `cat .env`, `curl *`, tokens em URL ou comandos amplos com segredos. Scripts devem ler o `.env` internamente e mascarar logs.

---

## 10. Onde Salvar Cada Tipo de Entrega

Esta tabela e definida no CLAUDE.md e deve ser respeitada por TODOS os commands e agents:

| Tipo de Material | Pasta | Formato | Exemplo de nome |
|---|---|---|---|
| Paginas (vendas, captura, obrigado) | `meus-produtos/{ativo}/entregas/paginas/` | `.html` | `vendas-curso-ingles.html` |
| Copy de pagina de vendas | `meus-produtos/{ativo}/entregas/copy-pagina/` | `.md` | `copy-curso-ingles.md` |
| Sequencias de email | `meus-produtos/{ativo}/entregas/emails/` | `.md` | `sequencia-pico-curso-ingles.md` |
| Anuncios (Meta, Google) | `meus-produtos/{ativo}/entregas/anuncios/` | `.md` | `anuncios-meta-curso-ingles.md` |
| Conteudo para redes sociais | `meus-produtos/{ativo}/entregas/conteudo-social/` | `.md` | `carrossel-curso-ingles.md` |
| Criativos e prompts de imagem | `meus-produtos/{ativo}/entregas/criativos/` | `.md` | `criativos-curso-ingles.md` |
| Scripts comerciais | `meus-produtos/{ativo}/entregas/comercial/` | `.html` | `playbook-curso-ingles.html` |
| Videos | `meus-produtos/{ativo}/entregas/videos/` | `.mp4`, `.md` | `roteiro-curso-ingles.md` |

**Se precisar de uma nova pasta de entrega:**
1. Crie a pasta em `meus-produtos/{ativo}/entregas/`
2. Adicione um `.gitkeep` dentro dela
3. Atualize a tabela no CLAUDE.md
4. Adicione a permissao `Write(meus-produtos/{ativo}/entregas/nova-pasta/**)` no settings.json (ja coberta por `Write(meus-produtos/{ativo}/entregas/**)`)

---

## 11. Convencoes e Padroes

### Nomenclatura de arquivos

| Componente | Convencao | Exemplo |
|---|---|---|
| Commands | kebab-case, singular | `pagina-de-vendas.md` |
| Agents | kebab-case, descritivo | `construtor-de-paginas.md` |
| Skills (pasta) | kebab-case | `playbook-comercial/` |
| Skills (arquivo) | Sempre `SKILL.md` (maiusculo) | `SKILL.md` |
| References | kebab-case, descritivo | `formatos-meta-ads.md` |
| Entregas | `[tipo]-[produto].[ext]` | `vendas-curso-ingles.html` |

### Idioma

- Todo conteudo visivel ao usuario: Portugues do Brasil
- Nomes de arquivos e pastas: sem acentos, kebab-case
- Frontmatter: pode ter acentos na description
- Codigo HTML/CSS: comentarios em portugues

### Estilo de copy (Light Copy)

Todas as copys geradas devem seguir:
- Argumentativo, logico, conversacional
- Sem ponto de exclamacao
- Sem perguntas no gancho
- Sem promessas vagas
- Sem "mesmo que" ou "sem precisar" como muletas
- Sem travessao

### Padrao HTML para paginas

- Arquivo unico (CSS em `<style>`, JS em `<script>`)
- Zero dependencias externas (exceto Google Fonts)
- Mobile-first com media queries
- Paleta maxima: 3 cores + neutros
- Animacoes CSS sutis
- Botoes grandes com hover
- Placeholders de imagem: `[Sua foto aqui]`

---

## 12. O Que NAO Sobe Para o Git

Protegido pelo `.gitignore`:

| Item | Razao |
|---|---|
| `.env` | Chaves de API do usuario |
| `meus-produtos/{ativo}/perfil.md` | Dados do produto do usuario |
| `meus-produtos/{ativo}/idconsumidor.md` | Identidade do consumidor (cliente ideal) |
| `meus-produtos/{ativo}/entregas/` (conteudo) | Materiais gerados sao unicos de cada usuario |
| `_prompts-gpt/` | Prompts originais de referencia interna |
| `.claude/projects/`, `.claude/plans/`, etc. | Arquivos de runtime do Claude Code |

**O que SOBE para o git:**
- `.claude/commands/`, `.claude/agents/`, `.claude/skills/` (o sistema em si)
- `.claude/settings.json` (permissoes)
- `CLAUDE.md`, `README.md`, `COMO-USAR.md`, `ARQUITETURA.md`, `AGENTS.md` (documentacao)
- `.env.example` (modelo de chaves, sem valores)
- `scripts/` (utilitarios Python e PowerShell)
- `.gitkeep` dentro das pastas de entrega (mantem a estrutura)

---

## 13. Relacao entre Componentes. Mapa de Dependencias

```
CLAUDE.md (regras globais)
    │
    ├── /produto-concepcao ────► skill: concepcao-produto ──► salva: perfil.md, idconsumidor.md, painel-entregas.html
    │
    ├── /copy-pagina ──────────► skill: paginas ────────────► salva: entregas/paginas/*.html + entregas/copy-pagina/*.md
    ├── /copy-anuncio ─────────► skill: anuncios ───────────► salva: entregas/anuncios/*.md
    ├── /copy-carrossel ───────► skill: conteudo ───────────► salva: entregas/conteudo-social/*.md
    ├── /roteiro-de-video ─────► skill: conteudo ───────────► salva: entregas/videos/*.md
    ├── /estrategia-lancamento ► skill: vtsd-completo ──────► salva: entregas/
    ├── /estrategia-funil ─────► skill: trafego-pago ───────► salva: entregas/
    ├── /comercial-playbook ───► skill: playbook-comercial ► salva: entregas/comercial/*.html
    ├── /lt-funil ─────────────► skill: criacao-produto-lt ─► salva: entregas/ (multiplas pastas)
    ├── /criativo-estatico ────► skill: anuncios ───────────► salva: entregas/criativos/*.md
    │
    ├── agent: estrategista-de-produto ──► skill: concepcao-produto ► salva: perfil.md, idconsumidor.md
    ├── agent: construtor-de-paginas ────► skill: paginas ───────────► salva: entregas/paginas/*.html
    ├── agent: clonador-de-bloco-visual ► skill: ui-reverse-engineer ► salva: entregas/paginas/copias/
    ├── agent: criador-de-campanhas ─────► skill: anuncios + trafego ► salva: entregas/anuncios/*.md
    └── agent: consultor-comercial ──────► skill: playbook-comercial ► salva: entregas/comercial/*.html
```

---

## 14. Exemplo Completo: Adicionando a Capacidade "Webinar"

Para ilustrar todo o processo, veja como seria adicionar suporte completo a webinars:

### 14.1 Criar a skill

**Arquivo:** `.claude/skills/webinars/SKILL.md`

```markdown
---
name: webinars
description: >
  Base de conhecimento para criacao de webinars de vendas.
  Inclui estrutura de roteiro (abertura, conteudo, pitch, CTA),
  formatos de apresentacao e follow-up pos-webinar.
  Acionada pelo command /webinar e agent planejador-de-webinar.
---

# Webinars. Base de Conhecimento

## Estrutura do Roteiro (4 Atos)
1. **Abertura**. Promessa + contexto + "por que ouvir"
2. **Conteudo**. 3 blocos de valor (usar Furadeira)
3. **Transicao**. Ponte valor → oferta
4. **Pitch**. Oferta + stack de valor + CTA + garantia

## Formatos
- Webinar ao vivo (90 min)
- Webinar evergreen (gravado, 60 min)
- Mini-webinar (30 min, para trafego frio)

[... mais conteudo de referencia ...]
```

### 14.2 Criar o command

**Arquivo:** `.claude/commands/webinar.md`

```markdown
---
name: workshop-marketing:webinar
description: Criar roteiro completo de webinar de vendas com estrutura de 4 atos, slides e follow-up.
---

# Webinar. Roteiro Completo

## Usage
```
/webinar
```

## O Que Fazer

### 1. Contexto
Leia `meus-produtos/{ativo}/perfil.md` e `meus-produtos/{ativo}/idconsumidor.md`.

### 2. Entrevista
[... perguntas seguindo o padrao ...]

### 3. Confirmacao
[... resumo + opcoes ...]

### 4. Gerar
[... instrucoes de geracao ...]
Salvar em `meus-produtos/{ativo}/entregas/textos-de-venda/webinar-[produto].md`

### 5. Proximo Passo
"Roteiro salvo. Use `/pagina-de-vendas` para criar a pagina de inscricao do webinar."

## Referencias
ANTES de gerar, leia:
- `.claude/skills/webinars/SKILL.md`
- `.claude/skills/vtsd-completo/SKILL.md`. Modulo sobre Light Copy
```

### 14.3 Criar o agent (opcional)

**Arquivo:** `.claude/agents/planejador-de-webinar.md`

```markdown
---
name: planejador-de-webinar
description: Agente autonomo que cria webinar completo. roteiro, estrutura de slides, emails de follow-up e anuncios de divulgacao.
tools: Read, Write, Edit
model: sonnet
---

# Planejador de Webinar. Agente Autonomo

[... instrucoes completas ...]

## Referencias
- `.claude/skills/webinars/SKILL.md`
```

### 14.4 Atualizar CLAUDE.md

Na secao de comandos, adicionar:
```
- `/webinar`. Criar roteiro completo de webinar de vendas
```

Na secao de agentes (se criou o agent):
```
- `planejador-de-webinar`. Cria webinar completo com roteiro, slides e follow-up
```

### 14.5 Atualizar README.md e COMO-USAR.md

Adicionar o novo comando nas tabelas e fluxos recomendados.

---

## 15. Troubleshooting

### Command nao aparece na lista

- Verifique se o arquivo esta em `.claude/commands/` (nao em subpasta)
- Verifique se a extensao e `.md`
- Verifique se o frontmatter YAML esta correto (delimitado por `---`)

### Agent nao e encontrado

- Verifique se o arquivo esta em `.claude/agents/`
- Verifique se o campo `name` no frontmatter corresponde ao nome usado na invocacao
- Verifique se `tools` esta definido no frontmatter

### Skill nao e consultada

- Skills NAO sao acionadas automaticamente. o command/agent precisa instruir explicitamente "Leia [caminho da skill]"
- Verifique se o caminho referenciado no command/agent esta correto

### Arquivo nao e salvo

- Verifique se a pasta de destino existe em `meus-produtos/{ativo}/entregas/`
- Verifique se a permissao `Write(meus-produtos/{ativo}/entregas/**)` esta no settings.json

### Ferramenta externa nao funciona

- Verifique se a chave existe no `.env` (nao no `.env.example`)
- Verifique se a permissao `Bash(ferramenta *)` esta no settings.json

---

## 16. Resumo Rapido para LLMs

Se voce e um LLM lendo este arquivo para entender o projeto:

1. **Leia `CLAUDE.md` primeiro**. contem todas as regras de comportamento, papel do assistente e fluxo padrao
2. **Commands** estao em `.claude/commands/*.md`. sao slash commands interativos
3. **Agents** estao em `.claude/agents/*.md`. sao subprocessos autonomos
4. **Skills** estao em `.claude/skills/*/SKILL.md`. sao base de conhecimento
5. **Dados do usuario** ficam em `meus-produtos/{ativo}/` (perfil.md e idconsumidor.md)
6. **Output** vai para `meus-produtos/{ativo}/entregas/` organizado por tipo
7. **Tudo segue a metodologia VTSD**. Quadro, Furadeira, Decorados, Light Copy, 8D, Mandala
8. **Idioma:** Sempre Portugues do Brasil para conteudo visivel ao usuario
9. **Nunca mostre codigo HTML** ao usuario. salve silenciosamente e informe o caminho
10. **Sempre leia perfil.md** antes de executar qualquer comando