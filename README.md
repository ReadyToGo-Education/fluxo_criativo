# Workshop Inteligente. Assistente de Marketing IA

Toolkit completo de marketing digital, copy e infoprodutos baseado nas metodologias **VTSD (Venda Todo Santo Dia)**, **Light Copy**, **C10X (High Ticket)** e **Low Ticket**. Roda dentro do **Claude Code** (VS Code) ou no **Cursor**, transformando o chat em um consultor especialista que entrega materiais prontos para uso.

Não é software tradicional: é um sistema de prompts estruturados (CLAUDE.md, regras, comandos, agentes, skills e scripts) que orquestra o assistente do início ao fim de um funil. Também é empacotado como app desktop (`Fluxo Criativo`, Electron) com instalador próprio para Windows e Mac, que provisiona Python, Git, Node e o app Claude automaticamente.

## Por onde começar

| Arquivo | Para quê serve |
|---|---|
| `COMO-USAR.md` | Guia passo a passo para o usuário final. Inclui seção Cursor. |
| `CLAUDE.md` | Instruções e regras do assistente. Autoritativo, lido em toda conversa. |
| `AGENTS.md` | Mapa rápido para agentes de IDEs (Cursor, etc.) |
| `ARQUITETURA.md` | Visão técnica da arquitetura. Como inserir novas capacidades. |
| `scripts/README-creative.md` | Processo de geração de criativos via `generate-creative.py`. |
| `painel/README.md` | Visual da Sala dos Agentes (espelho em tempo real do trabalho do Claude no projeto). |

## Onde roda

### Claude Code (VS Code)
Abra a pasta do projeto, instale a extensão Claude Code, use os slash commands `/copy-pagina`, `/lt-funil`, etc. Fluxo recomendado para quem desenvolve no toolkit.

### Cursor
Abra a pasta com **File → Open Folder**. As regras em `.cursor/rules/` e o `CLAUDE.md` passam a orientar o chat. No Cursor, a barra `/` não é equivalente à do Claude Code. Para seguir um fluxo, diga no chat "segue o comando copy-pagina" ou anexe o arquivo `.claude/commands/copy-pagina.md` com `@`.

### App desktop Fluxo Criativo (Electron)
Distribuição empacotada para alunos. O instalador (`instalador/script-windows.txt` para Inno Setup no Windows e `instalador/script-mac.sh` no Mac) baixa Python 3, Git, Node.js, o app oficial Claude e clona este repositório em `~/Documents/workshop-ia`. Ao abrir o app, o aluno vê o painel local (`painel/index.html`) com a Sala dos Agentes, que reflete em tempo real o que o Claude Code está executando via hook `agent-status-writer.js`. Build: `npm run build` (Mac) ou `npm run build:win` (Windows).

## Pré-requisitos

### Obrigatórios (o toolkit não funciona sem eles)

| Ferramenta | Como instalar | Para que serve |
|---|---|---|
| **Claude Code** | Extensão do VS Code (recomendado) ou `npm install -g @anthropic-ai/claude-code` | Runtime do assistente |
| **Python 3** | 3.10+. O assistente guia a instalação se necessário | Scripts do painel, playbook e páginas |
| **Git** | [git-scm.com](https://git-scm.com) | Clonar e atualizar o repositório |
| **Node.js** | 18+. Necessário se for empacotar o app Electron (`npm run build`) | Build do Fluxo Criativo |

### Opcionais (instalados automaticamente pelo assistente quando necessário)

| Ferramenta | Ativa |
|---|---|
| **Vercel CLI** | `/pagina-vercel` (publicar páginas) |
| **FFmpeg** | `/video-editar` (corte, legenda, compressão) |
| **Remotion** | `/video-remotion` (vídeo animado para Ads) |
| **whisper.cpp** | `/video-editar` (transcrição e legenda automática, instalado sob demanda em `.claude/tools/whisper/`) |

### APIs (todas opcionais. O toolkit funciona 100% sem nenhuma)

Copie `.env.example` para `.env` e preencha apenas o que for usar:

| Nível | O que preencher | O que desbloqueia |
|---|---|---|
| **Básico** | Nada | Todos os entregáveis em arquivo local |
| **Intermediário** | `VERCEL_TOKEN`, `FREEPIK_API_KEY` ou `OPENROUTER_API_KEY`, `APIFY_API_TOKEN` | Páginas publicadas, criativos automáticos, dashboards de redes |
| **Avançado** | `HEYGEN_API_KEY`, `FB_ACCESS_TOKEN_PERMANENTE` (ou MCP oficial Claude + Meta), `TELEGRAM_BOT_TOKEN`, `Z-API` | Vídeo com avatar IA, tráfego Meta Ads via API ou MCP, relatório diário automático |

Para configurar qualquer integração, use o comando correspondente no chat (`/configurar-heygen`, `/configurar-apify`, `/configurar-telegram`, `/configurar-zapi`, `/trafego-conexao`, etc.). Ele guia o processo completo, mascara tokens na exibição e grava sempre no `.env` (regra global do projeto: token nunca aparece hardcoded em outro arquivo).

## Metodologias base

- **VTSD (Venda Todo Santo Dia).** Quadro (transformação), Furadeira (método estruturado em macroetapas e microetapas), Decorados (50 benefícios em 5 categorias), 3 Identidades (Comunicador, Consumidor, Produto), Urgências Ocultas (7 categorias x 10 itens = 70 itens por produto), Mandala da Criatividade (18 tipos de anúncio x 4 objetivos x 3 momentos), Estrutura 8D (11 seções de página de vendas), VVV (vídeo de vendas), 26 Elementos Literários.
- **Light Copy.** Argumentativa, lógica, conversacional, não óbvia. Proibições duras codificadas em `.claude/rules/copy/checklist-light-copy.md` (12 itens): travessão, ponto de exclamação, pergunta no gancho, "Não é X. É Y.", "mesmo que", "sem precisar", nome do produto no lead, lero-lero, copy sem tese, sigla sem explicação, depoimento sem resultado, venda só do Quadro sem Decorado.
- **C10X (High Ticket).** Retiros online, webinar, pitch de palco, call SPIN, WhatsApp, proposta comercial, follow-up pós-evento. Disponível via skills globais do plugin C10X (`ht-big-idea`, `ht-oferta`, `ht-pitch-palco`, etc.) e via agente `estrategista-ht`.
- **Low Ticket.** Produto de entrada (R$37-97) com quiz ou página direta, desafio, agente GPT, copy para Hotmart/Kiwify, otimização de Ads via planilha colada do Gerenciador.

## Regras absolutas de estilo

1. **Nada de travessão (—)** em nenhum texto gerado. Sem exceção.
2. **Português do Brasil** em tudo que é visível ao usuário (com acentuação obrigatória validada pelo hook `scripts/verificar-acentuacao.py`).
3. **Nunca mostrar código HTML no chat.** Salvar silenciosamente e informar o caminho absoluto.
4. **Sempre pedir aprovação antes de salvar.** Resumo + opções numeradas.
5. **Uma pergunta por vez** nas entrevistas, com progresso visual entre blocos.
6. **Produto não aparece no lead.** Sem "curso", "treinamento", nome do produto ou sigla no início da copy.
7. **Tokens só no `.env`.** Proibido hardcoded em qualquer outro arquivo. Mascarados na exibição (`***TOKEN_MASCARADO***`).
8. **Operações de escrita na Graph API passam por gate no chat.** Antes de criar campanha, pausar adset, subir criativo etc., o assistente apresenta bloco de confirmação humano-legível e aguarda "sim".

Checklists completos (Light Copy + Design HTML) estão no topo do `CLAUDE.md` e em `.claude/rules/`.

## Arquitetura

4 tipos de componentes trabalham juntos:

| Componente | Local | Papel |
|---|---|---|
| **CLAUDE.md** | raiz | Persona, regras globais, fluxo padrão. Lido em toda conversa. |
| **Commands** | `.claude/commands/*.md` | Slash commands interativos (`/copy-pagina`, `/lt-funil`, etc.) |
| **Agents** | `.claude/agents/*.md` | Subprocessos autônomos (orquestradores e especialistas) |
| **Skills** | `.claude/skills/` | Base de conhecimento consultada por commands e agents |
| **Rules** | `.claude/rules/` | Regras compartilhadas (checklist Light Copy, tempos calibrados, etc.) |
| **Hooks** | `.claude/hooks/` | Scripts disparados por eventos (acentuação pt_BR, status de agentes para a Sala) |

**Fluxo típico:**
```
Usuário digita /comando
  → Command carrega .md correspondente
  → Lê meus-produtos/{ativo}/perfil.md e idconsumidor.md (contexto)
  → Consulta a skill relevante (conhecimento)
  → Roda entrevista (perguntas uma por vez)
  → Pede aprovação
  → Salva em meus-produtos/{ativo}/entregas/[tipo]/
  → Atualiza painel-entregas.html via painel-incremental.py
  → Sugere próximo comando
```

## Estrutura de pastas

```
workshop_inteligente/
├── CLAUDE.md                    Regras e papel do assistente (autoritativo)
├── AGENTS.md                    Mapa para IDEs
├── ARQUITETURA.md               Guia técnico completo
├── COMO-USAR.md                 Guia passo a passo
├── README.md                    Este arquivo
├── package.json                 Metadados Electron (Fluxo Criativo v1.0.2)
├── vercel.json                  Config Vercel para páginas publicadas
├── .env.example                 Modelo de chaves de API
│
├── .claude/                     Núcleo do assistente
│   ├── commands/                Slash commands (80+ arquivos .md)
│   ├── agents/                  Agentes orquestradores e especialistas
│   ├── skills/                  Base de conhecimento (50+ pastas)
│   ├── rules/                   Regras compartilhadas (Light Copy, tempos estimados)
│   ├── hooks/                   Hooks de sessão (verificar-acentuacao, agent-status-writer)
│   ├── settings.json            Permissões
│   └── settings.local.json      Permissões locais (não sobe, contém allow patterns)
│
├── .cursor/rules/               Regras específicas do Cursor (.mdc)
│
├── electron/                    App desktop Fluxo Criativo (Electron)
│   ├── main.js                  Processo principal Electron
│   ├── preload.js               Preload do app
│   ├── preload-panel.js         Preload da janela do painel
│   ├── installer.js             Lógica de provisionamento (Python, Git, Node, Claude)
│   └── setup.html               Tela de setup inicial
│
├── instalador/                  Scripts de instalação por SO
│   ├── script-windows.txt       Inno Setup script (gera workshop-ia-setup-windows.exe)
│   └── script-mac.sh            Shell script para Mac
│
├── painel/                      Sala dos Agentes (espelho visual em tempo real)
│   ├── index.html               Hub do painel
│   ├── skeleton-painel-entregas.html
│   ├── sala-assets/             Sprites e cenários da sala
│   └── README.md                Como funciona o polling de status
│
├── scripts/                     Utilitários Python e PowerShell
│
├── meus-produtos/               Produtos do aluno (ignorado pelo git)
│   ├── .ativo                   Slug do produto ativo
│   ├── index.js                 Manifest gerado pelo painel-atualizar.py
│   └── {slug-do-produto}/
│       ├── perfil.md            Quadro, Furadeira, Decorados, Urgências, Argumentos Incontestáveis, 3 Identidades
│       ├── idconsumidor.md      Identidade do consumidor (Para Quem É, Objeções com 7 Argumentos, Baldes, Tom)
│       ├── pesquisa-mercado.md  Pesquisa de nicho (9 eixos)
│       ├── tipo.md              Low/Middle/High ticket
│       ├── nome.txt             Nome amigável (opcional, override)
│       ├── painel-entregas.html Painel do produto (gerado por /produto-concepcao via painel-incremental.py)
│       ├── projeto/{slug}/      Estado dos projetos toolkit-* (roteiro, plano, estado)
│       └── entregas/            Output do assistente (por produto)
│           ├── paginas/         HTML de vendas, captura, obrigado
│           │   └── copias/      Cópias isoladas de seção geradas por /pagina-visual
│           ├── copy-pagina/     Copy markdown por bloco
│           ├── anuncios/        Pacotes de anúncios
│           ├── conteudo-social/ Posts, carrosséis, Reels
│           ├── criativos/       Prompts de imagem e referências
│           ├── comercial/       Scripts de venda 1:1 (HTML, exportável para PDF)
│           ├── videos/          HeyGen, Remotion, roteiros
│           └── produto/         E-book, checklist, mini-curso final
│
└── (build/, dist-electron/, assets/, node_modules/ — output e dependências, ignorados)
```

Observação: `meus-produtos/`, `.env`, `.claude/agents-memory/`, `.claude/projects/`, `.claude/worktrees/` e `.claude/tools/` (Whisper) são ignorados pelo git. Cada aluno gera os seus localmente.

## Painel de entregas

Cada produto tem seu `painel-entregas.html` em `meus-produtos/{slug}/`. O painel é gerado e atualizado seção a seção pelo `painel-incremental.py` conforme o aluno avança nos commands. Inclui um seletor de produto no sidebar para navegar entre todos os produtos cadastrados. O design vive em `scripts/painel_template.py` (shell HTML + CSS + renderers por seção) e não deve ser editado diretamente no HTML.

- **Gerar/atualizar uma seção:** `py -3 scripts/painel-incremental.py --secao quadro`
- **Atualizar o manifest:** `py -3 scripts/painel-atualizar.py` (ou `/painel-atualizar` no chat)
- **Validar estado do painel:** `py -3 scripts/painel-validar.py`
- **Revisar painel pelo chat:** `/painel-revisar` (skill que audita completude)

## Sala dos Agentes (Fluxo Criativo)

Espelho visual em tempo real do trabalho do Claude no projeto. Cada um dos 7 agentes do painel representa uma área do trabalho VTSD (PROD, COPY, PAG, AD, VID, SALES, DATA) e reage conforme o Claude executa skills. O hook `.claude/hooks/agent-status-writer.js` escreve em `.claude/agents-memory/agents-status.js` toda vez que um agente entra em ação. A página `painel/workshop-live-office.html` (embutida via iframe) faz polling a cada 1,5s, diferencia contra o estado anterior e dispara animações apenas para mudanças (`idle → trabalhando`, troca de skill, conclusão com `✅`). Sem hook, sem movimento.

## Comandos disponíveis

### Produto
- `/produto-novo`. Porta de entrada do projeto. Verifica produto ativo, cria um novo ou gera ideias de produto. Acionada automaticamente em toda nova conversa.
- `/produto-concepcao`. Fluxo unificado de Quadro, Furadeira, Decorados, Urgências Ocultas, 3 Identidades, Identidade do Consumidor e Painel de Entregas.
- `/produto-trocar`. Lista produtos cadastrados e troca o ativo.
- `/produto-novo`, `/produto-excluir`, `/produto-zerar`. Criação, exclusão e reset de perfil/idconsumidor.
- `/produto-consumidor`. Obsoleto, redireciona para `/produto-concepcao`.

### Copy
`/copy-pagina`, `/copy-anuncio`, `/copy-social`, `/copy-roteiro`, `/copy-variacao-post`, `/elementos-literarios`

Toda copy passa obrigatoriamente pela skill `revisora` (Manual da Copy + 4 blocos de checklist) antes de ser exibida ao usuário. Auto-revisão invisível.

### Imagem e vídeo
- `/criativo-estatico`. Orquestrador de criativos estáticos com 4 sub-formatos (`aida`, `caixinha-de-perguntas`, `criativo-surreal`, `promessa-simples`). Gera prompt para colar em ferramenta externa OU geração automática via API.
- `/criativo`. Briefing visual de criativo a partir do perfil.
- `/img-anuncio`. Edita imagem de referência do aluno (troca personagem, altera texto, edição pontual) via OpenRouter com visão multimodal.
- `/avat-whisk`. Briefings visuais prontos para o Whisk (Google Labs).
- `/gerar-furadeira`. Gera a Furadeira (método do produto) no `perfil.md` aplicando uma das 6 mecânicas (Fases, Lógica Condicional, Enquadramento, Listas, Empecilhos, Dinâmica de Entrega), escolhida automaticamente conforme o nicho.
- `/furadeira-visual`. Gera a imagem PNG da Furadeira a partir do que já está escrito no `perfil.md`. Decide o layout sozinho conforme mecânica + nicho, monta prompt em inglês para o aluno colar no ChatGPT, recebe a imagem de volta e salva no projeto + painel de entregas.
- `/video-heygen`. Vídeo com avatar IA via HeyGen, múltiplas cenas, avatares rotacionados, backgrounds variados, direção baseada em dados reais (Apify/dashboard) ou Urgências Ocultas.
- `/video-remotion`. Vídeo animado para Meta Ads via Remotion.
- `/video-editar`. Edita vídeos existentes com FFmpeg (corte, legenda via Whisper, compressão).
- `/video-efeitos`. Aplica efeitos visuais em vídeo (transições, scrub, otimização).

### Carrossel
- `/carrossel`. Gera carrosséis virais para Instagram em 7 estilos (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia da semana). Inclui 3 caminhos de geração de imagem (manual, Claude in Chrome, API paralela).
- `/programar-carrossel-noticia`. Programa tarefa recorrente no `/schedule` do Claude para gerar carrossel de notícia automaticamente.

### Low Ticket
- `/lt-funil`. Cria produto de entrada low ticket (quiz, desafio, agente GPT).
- `/lt-criar-produto`. Cria o conteúdo real do produto digital.
- `/lt-quiz`. Gera perguntas do quiz.
- `/lt-pagina`. Gera as 4 leads low ticket (incluindo Estrutura E — Categoria Padrão).
- `/lt-otimizar`. Analisa planilha do Gerenciador e otimiza campanhas low ticket.

### Tráfego Pago (Meta Ads via API ou MCP oficial)
- `/trafego-conexao`. Configura conexão com Meta Ads. Pergunta se quer usar o **conector oficial Claude + Meta (MCP via OAuth)** ou o caminho do **App Facebook Developers (token permanente no `.env`)**. Salva preferência em `META_AUTH_MODO`. Toda skill de tráfego depende dessa variável e aciona `/trafego-conexao` se ela não existir (Passo 0 obrigatório).
- `/trafego-insights`. Leitura de métricas (campanha única ou conta completa com ranking de urgência) com cálculo automático de derivadas (connect rate, taxa de conversão por etapa, custo por etapa, hook rate).
- `/trafego-criar-campanha`. Cria campanha via Marketing API. PAUSED por padrão, preview YAML obrigatório, gate de pixel ativo. Cobre objetivos OUTCOME_SALES (perpétuo) e OUTCOME_LEADS (lançamento).
- `/trafego-otimizar`. Diagnóstico em 2 camadas (tendência cruzando 3 janelas + gargalo). Classifica em 6 trilhas (perpétuo low/mid/high, lançamento low/mid/high). Propõe ações graduais que preservam aprendizado (reduzir -20%, pausar criativo, refresh) e emite sinal de prontidão para escala. Inclui sub-skill `acoes-lote` (em massa por filtro) e `atalhos-compostos` (orquestra `/trafego-publicos` + `/trafego-criar-campanha`).
- `/trafego-analise`. Análise narrada VTSD em 9 outputs (Diagnóstico Rápido, Performance & Funil, Criativos & Copy com Mandala 18 tipos, Geo & Demografia, Timing & Sazonalidade, Investigação Profunda, Lifecycle & Histórico, Problemas Ocultos, Orçamento & Projeção, Comparativo A x B).
- `/trafego-pixel`. Diagnóstico de pixels da conta (status, último disparo, eventos rastreados nos últimos 7 dias). Apenas leitura.
- `/trafego-publicos`. Cria audiences via API (Custom Audiences a partir de evento padrão do pixel, evento personalizado ou video view %, Lookalike 1% a 10%, Saved Audiences por nível iniciante/intermediário/avançado a partir do produto ativo). Toda criação passa por preview YAML e confirmação SIM.
- `/trafego-regras`. Cria automações no Meta Ads. Regra automática (`adrules_library`) com triggers de CPA/CPL/ROAS, resumo recorrente agendado por Telegram/WhatsApp, e programação liga/pausa de adsets (delivery schedule). Toda regra nasce PAUSED.
- `/trafego-testes`. Cria testes A/B disciplinados (criativo, headline, audiência, faixa etária, posicionamento, lance, estrutura), duplica entidade existente alterando UMA dimensão, e fluxo composto de campanha de remarketing. Hipótese documentada e handoff para `/trafego-analise` após D+7.

Skill interna acionada automaticamente: `trafego-escalar` (5 modos de escala, 3 velocidades, freios escalonados, tetos), invocada por `/trafego-otimizar` quando `sinal_para_escala.pronta: true`.

### Estratégia
`/estrategia-funil`, `/estrategia-lancamento`

### Comercial
`/comercial-playbook`. Cria scripts de venda 1:1 com SPIN Selling adaptado, scripts de fechamento, quebra de objeções e pitch comercial. Entrega em HTML pronto para PDF.

### Infraestrutura de página (após gerar o HTML)
`/pagina-ajuste`, `/pagina-performance`, `/pagina-pixel`, `/pagina-checkout`, `/pagina-active`, `/pagina-precheckout`, `/pagina-lovable`, `/pagina-vercel`, `/pagina-visual`

`/pagina-visual` cria a página a partir de prints de referência do aluno: cada print vira uma cópia HTML com design 100% preservado, e a montagem final concatena via `scripts/montar-pagina-copias.py`.

### Feedback e auditoria
`/feedback-pagina`, `/feedback-low-ticket`. Ambos fazem auditoria completa contra o Manual da Copy e podem editar o HTML de saída.

### Toolkit (projetos estruturados)
`/toolkit-novo`, `/toolkit-planejar`, `/toolkit-executar`, `/toolkit-verificar`, `/toolkit-progresso`, `/toolkit-anotar`, `/toolkit-pausar`, `/toolkit-retomar`

Fluxo proprietário para conduzir projetos grandes (lançamento, funil completo, reestruturação). Quebra o objetivo em etapas, aciona as skills certas uma a uma e mantém o estado em `meus-produtos/{ativo}/projeto/{slug}/` (roteiro.md, plano.md, estado.md) entre sessões. Não use para tarefa simples de uma skill só.

### Dados e automações
- `/ads-relatorio`. Cria rotina diária agendada na nuvem do Claude que busca métricas do Facebook Ads e envia relatório via WhatsApp (Z-API) ou Telegram.
- `/enviar-relatorio-ads`. Dispara o relatório agora.
- `/dados-instagram`. Análise pontual de perfil do Instagram (insights de copy + dashboard HTML com filtros).
- `/app-saas`. Gera PRD + prompt técnico de mini-SaaS relevante para os alunos do infoprodutor, pronto para colar no Lovable.dev.
- `/criar-gpt`. Gera agente GPT personalizado para infoprodutores com 10 ideias, metodologia e prompt final.
- `/adaptar-plataforma`. Converte scripts e instruções Windows/PowerShell para Mac ou Linux (Task Scheduler → cron/launchd).

### Dashboards de redes sociais
`/instagram-dashboard`, `/tiktok-dashboard`, `/youtube-dashboard`, `/linkedin-dashboard`, `/dashboard-concorrente-remover`

Dashboards HTML com métricas via Apify. Cada plataforma tem seu próprio script (download + render local). Orquestrador unificado em `dashboard-social` (skill) que verifica quais já existem e oferece apenas os que faltam. O token Apify é pedido uma única vez e vale para todas as plataformas.

### Configuração de integrações
- `/configurar-apify`. Guia para criar conta, gerar Personal API Token e salvar como `APIFY_API_TOKEN`.
- `/configurar-zapi`. Conecta Z-API para envio automatizado de WhatsApp.
- `/configurar-heygen`. Setup do HeyGen para vídeo com avatar IA.
- `/configurar-imagens`. Setup de provider de imagens (OpenRouter, Freepik) para anúncios e criativos.
- `/configurar-telegram`. Cria bot via BotFather, obtém Chat ID e conecta ao Workshop.
- `/gerar-token-permanente-facebook-ads`. Gera token que nunca expira via Usuário do Sistema no Business Manager.
- `/gerar-token-facebook-ads`. Token temporário (debug).
- `/obter-id-conta-anuncios`. Descobre `act_id` da conta de anúncios.
- `/criar-aplicativo-analise-ads`. Guia passo a passo para criar App no Facebook Developers com acesso à Marketing API.

### Tutorial e workshop
`/tutorial-ferramentas`, `/workshop-office`

A lista completa com descrições está no `CLAUDE.md`.

## Agentes especialistas

Orquestradores autônomos em `.claude/agents/` que executam tarefas completas acionando múltiplas skills. Cada agente carrega memória persistente em dois escopos no Passo 0 (`.claude/agents-memory/{agente}.md` global e `meus-produtos/{ativo}/agentes/{agente}.md` por produto) e anexa aprendizados antes de encerrar.

- `estrategista-de-produto`. Sessão completa de concepção VTSD.
- `estrategista-low-ticket`. Funil low ticket do zero à página publicável em uma sessão.
- `estrategista-middle-ticket`. Funil perpétuo de produto principal.
- `estrategista-ht`. Funil High Ticket C10X completo (captação + evento + venda 1:1 + consultoria).
- `construtor-de-paginas`. Páginas profissionais do zero usando design system VTSD.
- `clonador-de-bloco-visual`. Reproduz fielmente UMA seção de página a partir de UM print de referência + copy aprovada (usado por `/pagina-visual` em paralelo, uma chamada por seção).
- `criador-de-campanhas`. Campanha de tráfego completa (perpétua, lançamento, low ticket, high ticket, remarketing).
- `consultor-comercial`. Playbook comercial 1:1 (HT via `/ht-*` e WhatsApp middle/low ticket via `/comercial-playbook`).
- `copywriter`. Orquestrador de copy (página, anúncio, carrossel, variações de post).
- `video-maker`. Orquestrador de produção de vídeo (anúncio, VSL, conteúdo, lançamento).
- `executor-de-plano-de-acao`. Recebe transcrição de análise + plano de ação e executa cada tarefa acionando skills e agentes.
- `pesquisa-mercado`. Pesquisa de mercado completa em 9 eixos (tamanho, concorrentes, preço, público, objeções Reclame Aqui, virais, top 10 YouTube, biblioteca de anúncios Meta, riscos regulatórios).

**Agentes internos** (acionados automaticamente em paralelo, não invocados diretamente pelo usuário):
- Geradores: `gerador-decorados`, `gerador-urgencias-ocultas`, `gerador-idconsumidor`.
- Revisores: `revisor-perfil`, `revisor-pesquisa`, `revisor-idconsumidor`.

## Skills (base de conhecimento)

Em `.claude/skills/`. Não são acionadas diretamente pelo usuário: são consultadas por commands e agents quando precisam de conhecimento especializado.

**Metodologia VTSD**
- `vtsd-completo/`. Metodologia VTSD integral.
- `concepcao-produto/`. Quadro, Furadeira, 3 Identidades, Urgências Ocultas, Identidade do Consumidor, Painel de Entregas (fluxo unificado).
- `elementos-literarios/`. Os 26 elementos do Light Copy de Leandro Ladeira (hipérbole, metáfora, setup punchline, tríade cômica, anáfora, antítese, aforismo etc.).
- `revisora/`. Manual da Copy + checklist Light Copy aplicado a todo material gerado (auto-revisão obrigatória invisível).

**Páginas e copy**
- `paginas/`. Estrutura 8D, design system, referências de blocos atômicos.
- `ui-reverse-engineer/`, `usar-referencia-visual/`. Engenharia reversa de prints para reconstrução fiel.
- `carrossel/`, `carrossel-visual/`. Carrosséis de Instagram (texto + foto IA por card).
- `copy-variacao-post/`. Variações de conteúdo validado pelo algoritmo.
- `conteudo/`. Frameworks de copy, gatilhos, exemplos de VSL.
- `criacao-produto-low-ticket/`. Conteúdo real do produto LT (e-book, checklist, mini-curso, desafio, agente GPT, planilha).

**Anúncios e criativos**
- `anuncios/`, `anuncios-texto/`, `anuncios-video/`. Mandala da Criatividade, formatos Meta Ads e Google Ads, especificações técnicas.
- `biblioteca-anuncios/`. Investiga criativos escalados na Biblioteca de Anúncios da Meta (Apify ou Claude in Chrome) e identifica padrões.
- `banner-visual/`. Banner estático 1080x1350 com foto cinematográfica via OpenRouter (`gerar-banner-estatico.py`).
- `furadeira-visual/`, `gerar-furadeira/`. Geração da Furadeira textual e visual.
- `canvas-design/`, `css-effects/`. Design de peças e efeitos CSS.
- `video-avancado/`. Direção de vídeo avançada.

**Tráfego pago (Meta Ads)**
- `trafego-pago/`. Base geral (pixel, métricas, campanhas, regras).
- `trafego-conexao/`. Setup de conexão (MCP oficial ou App Facebook Developers).
- `trafego-insights/`. Fonte única de leitura da Graph API com cálculo de derivadas.
- `trafego-criar-campanha/`. Fluxo de criação com preview YAML.
- `trafego-otimizar/`. Diagnóstico em 2 camadas + 6 trilhas + sub-skills (acoes-lote, atalhos-compostos).
- `trafego-escalar/`. 5 modos de escala (vertical, horizontal, vertical+horizontal, consolidação CBO, Advantage).
- `trafego-analise/`. 9 outputs narrativos VTSD.
- `trafego-pixel/`. Diagnóstico de pixels (leitura).
- `trafego-publicos/`. Custom, Lookalike, Saved Audiences.
- `trafego-regras/`. Regras automáticas, resumos agendados, delivery schedule.
- `trafego-testes/`. Testes A/B disciplinados, remarketing.

**Pesquisa e dados**
- `pesquisa-mercado/`. 9 eixos completos.
- `pesquisa-mercado-instagram/`. Pesquisa específica via Instagram.
- `dados-instagram/`. Dashboard + relatório do perfil do aluno ou concorrente.
- `dados-nicho/`. 10 a 20 perfis de referência do nicho via WebSearch.

**Dashboards**
- `instagram-dashboard/`, `tiktok-dashboard/`, `youtube-dashboard/`, `linkedin-dashboard/`. Um por plataforma, via Apify.
- `dashboard-social/`. Orquestrador unificado.

**Programação de conteúdo**
- `programar-carrossel/`. Tarefa recorrente no `/schedule` do Claude para gerar carrossel automaticamente em 1 dos 7 estilos.
- `programar-carrossel-noticia/`. Variante focada em carrossel de notícia.

**Painel e suporte**
- `painel-revisar/`. Audita estado e completude do painel.
- `agente-gpt/`. Base para criar agentes GPT personalizados.
- `app-saas/`. Ideação e PRD de mini-SaaS para alunos do infoprodutor.
- `ferramentas/`. Integrações externas.
- `adaptar-plataforma/`. Adaptação cross-platform (Windows/Mac/Linux).
- `tutorial-ferramentas/`. Tutorial das ferramentas.

## Scripts principais

### Painel de entregas
```
py -3 scripts/painel-incremental.py --secao quadro
py -3 scripts/painel-atualizar.py
py -3 scripts/painel-validar.py
```
Atualiza seções individuais do `painel-entregas.html`, regenera o manifest `meus-produtos/index.js` (lista de produtos usada pelo seletor no painel) e valida completude. O design fica em `scripts/painel_template.py` (shell HTML + renderers por seção). Nunca editar o HTML diretamente.

### Páginas de vendas (fluxo visual)
```
py -3 scripts/montar-pagina-copias.py --slug {slug}
py -3 scripts/criar-tema-custom.py
py -3 scripts/abrir-html.py {arquivo}
```
Monta o HTML final a partir das cópias de seção geradas por `/pagina-visual` em `meus-produtos/{slug}/entregas/paginas/copias/`. `criar-tema-custom.py` cria tema customizado; `abrir-html.py` abre o resultado no navegador (multi-plataforma). Scripts antigos (`build-pagina-vendas.py`, `workshop-merge-pagina.py`) estão DEPRECATED — ver `ARQUITETURA.md`.

### Playbook comercial
```
py -3 scripts/playbook-briefing.py --slug {slug}
py -3 scripts/playbook-montar.py --slug {slug}
py -3 scripts/playbook-extrair-objecoes.py
py -3 scripts/playbook-aplicar-criativas.py
```
Gera briefing a partir do perfil, monta o HTML do playbook (exportável para PDF), extrai objeções e aplica criativas.

### Geração visual
- `generate-avatar-video.py`. HeyGen via API.
- `generate-creative.py`. Criativos via OpenRouter (ver `scripts/README-creative.md`).
- `generate-openrouter-nano-banana-images.py`. Imagens via modelo nano-banana.
- `gerar-banner-estatico.py`. Banner cinematográfico 1080x1350 (skill `banner-visual`).
- `gerar-carrossel-foto.py`. Carrossel com foto IA por card.
- `gerar-cards-entregaveis.py`. Cards visuais do painel.
- `gerar-icone.py`, `gerar-sprites-bonecos.py`. Ícones e personagens para a Sala dos Agentes.
- `recriar-imagem-estilo.py`. Re-estiliza imagem existente.
- `openrouter_model_router.py`. Roteador de modelos OpenRouter (escolhe modelo conforme tarefa).
- `otimizar-video-scrub.py`. Otimização de vídeo para pré-load (scrub fluido).

### Tráfego e relatórios
- `relatorio-ads.ps1` e `relatorio-ads-cli.py`. Rotina diária de relatório Facebook Ads. Envia via WhatsApp (Z-API) ou Telegram, agendado na nuvem do Claude.
- `painel-trafego.py`. Painel HTML de métricas de tráfego.
- `scripts/trafego-analysis/`. Pacote Python interno com testes, docs e CLI próprios.

### Verificadores
- `verificar-acentuacao.py`. Hook que valida pt_BR (acordo ortográfico 1990) ao fim de cada geração de texto.
- `verificar-idconsumidor.py`. Confere completude do `idconsumidor.md` antes do painel.

### Utilitários
- `abrir-html.py`. Abre HTML no navegador padrão (Windows/Mac/Linux).
- `workshop-copy-template-tema.py`. Copia templates de tema entre produtos.

## Integrações externas (opcionais)

Configuradas via `.env` (veja `.env.example`). Token sempre lido do `.env`, nunca hardcoded em script ou comando. Exibição mascarada por padrão.

| Integração | Finalidade | Comando de setup |
|---|---|---|
| Facebook Marketing API | Tráfego Meta Ads, relatórios, otimização | `/trafego-conexao` (porta de entrada, oferece MCP oficial **ou** App próprio), `/gerar-token-permanente-facebook-ads`, `/criar-aplicativo-analise-ads` |
| MCP Claude + Meta | Conector oficial via OAuth (sem token no `.env`) | `/trafego-conexao` |
| Z-API | Mensagens WhatsApp automatizadas | `/configurar-zapi` |
| Telegram Bot | Relatórios e automações via Telegram | `/configurar-telegram` |
| Apify | Coleta de dados de Instagram, TikTok, YouTube, LinkedIn, Biblioteca de Anúncios | `/configurar-apify` |
| HeyGen | Vídeo com avatar IA | `/configurar-heygen` |
| OpenRouter | Geração e edição de imagens (nano-banana, multimodal) | `/configurar-imagens` |
| Freepik AI | Geração alternativa de imagens | `/configurar-imagens` |
| Lovable / Vercel | Publicação de páginas | `/pagina-lovable`, `/pagina-vercel` |
| Hotmart, Kiwify, Eduzz, Cakto, Pepper, Stripe | Checkout das páginas | `/pagina-checkout` |
| ActiveCampaign | Lista de leads e automação de email | `/pagina-active` |

## Fluxos recomendados

### Começar a vender
1. `/produto-novo` ou `/produto-concepcao` (gera perfil + identidade do consumidor + painel)
2. `/copy-pagina`
3. `/copy-anuncio`

### Lançamento
1. `/produto-concepcao`
2. `/estrategia-lancamento`
3. `/copy-pagina` (evento + vendas)
4. `/copy-anuncio`
5. `/carrossel`

### Perpétuo
1. `/produto-concepcao`
2. `/estrategia-funil`
3. `/copy-pagina` (captura + vendas + obrigado)
4. `/copy-anuncio`

### Low Ticket
1. `/produto-concepcao`
2. `/lt-funil` (após framework Quiz vs. Página descrito no `CLAUDE.md`)
3. `/lt-criar-produto` (e-book, checklist, agente GPT, etc.)
4. `/lt-pagina` ou `/lt-quiz`
5. `/copy-anuncio` (formatos low ticket)
6. `/lt-otimizar` (com planilha do Gerenciador)

### Tráfego Pago (Meta Ads)
1. `/trafego-conexao` (uma vez, define MCP ou App, salva `META_AUTH_MODO`)
2. `/trafego-pixel` (diagnóstico de pixel)
3. `/trafego-publicos` (audiences base)
4. `/trafego-criar-campanha` (PAUSED por padrão)
5. `/trafego-insights` (após 48h rodando)
6. `/trafego-otimizar` (diagnóstico em 2 camadas + 6 trilhas)
7. `/trafego-analise` (análise narrada VTSD em 9 outputs)
8. `/trafego-testes` ou escala automática (`/trafego-otimizar` → `trafego-escalar` quando `sinal_para_escala.pronta: true`)

### High Ticket C10X
Use o agente `estrategista-ht` ou invoque diretamente as skills globais do plugin C10X. Fluxo típico:
1. `ht-big-idea`, `ht-oferta`, `ht-pagina-inscricao`
2. `ht-comunicacao-pre`, `ht-cronograma`, `ht-conteudo`
3. `ht-pitch-palco`
4. `ht-spin`, `ht-fechamento`, `ht-objecoes`, `ht-whatsapp`, `ht-apresentacao-proposta`, `ht-proposta`
5. `ht-follow-up`, `ht-onboarding`

## Fluxo padrão de qualquer comando (6 passos)

1. **Contexto.** Ler `meus-produtos/.ativo`, depois `perfil.md` e `idconsumidor.md`.
2. **Entrevista.** 3 a 5 perguntas, uma por vez, com progresso visual.
3. **Confirmação.** Resumo do que vai criar, pedir OK numerado.
4. **Geração.** Criar o entregável aplicando a metodologia VTSD. Para copy, aplicar o Manual da Copy + revisora antes de exibir.
5. **Aprovação.** Mostrar o resultado e perguntar `1. Aprovar e salvar / 2. Ajustar`.
6. **Entrega.** Salvar, informar caminho absoluto, sugerir próximo comando.

Antes de qualquer operação que demore mais de 10 segundos, o assistente anuncia o próximo passo com tempo estimado calibrado em `.claude/rules/tempo-estimado.md` (regra global "Pensar em voz alta").

## O que sobe para o git

**Sobe:** `.claude/commands/`, `.claude/agents/`, `.claude/skills/`, `.claude/rules/`, `.claude/hooks/`, `.claude/settings.json`, `CLAUDE.md`, `AGENTS.md`, `ARQUITETURA.md`, `README.md`, `COMO-USAR.md`, `.env.example`, `scripts/`, `electron/`, `instalador/`, `painel/` (sem `sala-assets` gerados), `package.json`, `vercel.json`.

**Não sobe:** `.env`, `meus-produtos/` (dados do aluno), `.claude/agents-memory/`, `.claude/projects/`, `.claude/worktrees/`, `.claude/tools/` (binários Whisper instalados sob demanda), `.claude/settings.local.json`, `dist-electron/`, `node_modules/` e demais arquivos de runtime.

## Adicionando novas capacidades

Para criar um novo command, agent, skill ou integração, siga o guia completo em `ARQUITETURA.md` (seções 5 a 8). Inclui frontmatter obrigatório, checklist e exemplo completo de como adicionar suporte a um novo domínio (ex: webinars).
