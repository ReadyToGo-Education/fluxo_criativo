# Comandos do projeto

<!-- Gerado por scripts/gerar-catalogo-comandos.py a partir do cabeçalho de cada
     arquivo em .claude/commands/. Não edite aqui: edite o comando e rode o script. -->

Lista de tudo que o assistente faz, por categoria. Os que começam com `/` são comandos;
os outros são chamados pelo nome ("usar o instagram-dashboard").

## Produto

- `/app-saas`. Lê o perfil do produto ativo, sugere 10 ideias de mini-SaaS relevantes para os alunos do infoprodutor e, após a escolha, gera o PRD completo com schema, telas, user stories e prompt técnico pronto para colar no…
- `/criar-agente`. Criar o agente de IA do produto para entregar aos alunos como bônus, order bump ou produto.
- `/furadeira-visual`. Gerar a imagem PNG da Furadeira do produto ativo.
- `/gerar-furadeira`. Gerar a Furadeira (método) do produto ativo no perfil.md.
- `/painel-atualizar`. Atualizar o manifest meus-produtos/index.js que alimenta o painel global painel/index.html.
- `/produto-concepcao`. Cadastrar produto/negócio do aluno com Quadro, Furadeira, Decorados e 3 Identidades da metodologia VTSD.
- `/produto-excluir`. Excluir um produto cadastrado e todas as suas entregas e pastas.
- `/produto-novo`. Porta de entrada do projeto.
- `/produto-trocar`. Listar os produtos cadastrados e trocar o produto ativo.
- `/produto-zerar`. Apaga todas as informações de contexto pessoal de negócio.

## Copy

- `/copy-anuncio`. Criar pacotes completos de anúncios para Meta Ads e Google Ads usando a Mandala de 18 Tipos de Anúncios da metodologia VTSD.
- `/copy-bullets`. Gerar 110 bullets de copy do produto ativo (frases curtas de curiosidade sobre uma entrega concreta do produto) nas 11 técnicas de bullet, mais os 10 bullets quentes para headline, assunto de e-mail e abertura de…
- `/copy-pagina`. Criar copy completa e/ou página HTML de vendas, captura ou obrigado.
- `/copy-roteiro`. Criar roteiros de vídeo para os 3 formatos principais.
- `/elementos-literarios`. Aplicar os 26 Elementos Literários (Ladeirísticos) do Light Copy em copy existente ou criar trechos do zero.

## Conteúdo e Criativos

- `/avat-whisk`. Gerar briefings visuais prontos para o Whisk (Google Labs).
- `/carrossel`. Gera carrossel para Instagram com foto real por card via IA (OpenRouter/Freepik (Magnific)).
- `/copy-social`. Criar conteúdo para redes sociais.
- `/copy-variacao-post`. Criar variações de posts que já tiveram alto engajamento, a partir do insights.json gerado pelo dashboard do Instagram.
- `/criativo-estatico`. Gera criativo estático de anúncio (imagem) para Instagram.
- `/criativo`. Criar criativos visuais para o produto ativo.
- `/img-anuncio`. Edita uma imagem de referência que o usuário já tem.
- `/programar-carrossel-noticia`. Programa tarefa recorrente que gera carrossel de notícia para Instagram automaticamente (via /schedule do Claude).
- `programar-carrossel`. Programa uma tarefa recorrente que gera carrossel para Instagram automaticamente, em 1 dos 9 estilos (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia da semana, Curiosidade, Editorial).

## Low Ticket

- `/lt-criar-produto`. Cria o conteúdo real do produto digital de entrada.
- `/lt-funil`. Criar produto low ticket completo usando a metodologia low ticket do VTSD.
- `/lt-otimizar`. Analisar planilhas exportadas do Gerenciador de Anúncios do Meta Ads e recomendar ações práticas de otimização para campanhas de produtos low ticket.
- `/lt-pagina`. Criar a página de vendas low ticket pela régua v16 do time de criativos.
- `/lt-quiz`. Gerar quiz de vendas completo para o Low Ticket.

## Tráfego Pago

- `/criar-aplicativo-analise-ads`. Guia passo a passo para criar um App no Facebook Developers com acesso à Marketing API, necessário para gerar o token de acesso ao Facebook Ads.
- `/gerar-token-permanente-facebook-ads`. Guia para gerar token permanente de acesso ao Facebook Ads via Usuário do Sistema no Business Manager.
- `/obter-id-conta-anuncios`. Guia para localizar o ID da conta de anúncios no Business Manager do Facebook e salvar em FB_AD_ACCOUNT_ID no .env.
- `/trafego-analise`. Análise narrada de tráfego pago Meta Ads com terminologia VTSD (Mandala 18 tipos, Urgência Oculta, Quadro na Parede, Furadeira, Decorados, 3 Identidades, HOT/COLD/SUPERCOLD, Caixa Rápido, Pico vs Evergreen).
- `/trafego-conexao`. Porta única de entrada para conectar o projeto com o Meta Ads (Facebook + Instagram).
- `/trafego-criar-campanha`. Subir campanha nova no Meta Ads (Facebook + Instagram) pelo conector da Meta (MCP) ou pela Marketing API (modo App).
- `/trafego-criativos`. Inteligência criativa por métricas de atenção, intenção e conversão para Meta Ads.
- `/trafego-dashboard-analisador`. Só para mandar o dashboard de tráfego ao analisador da Mentoria Fluxo.
- `/trafego-dashboard`. Abre, cria ou atualiza o dashboard de tráfego do Meta Ads.
- `/trafego-diagnostico`. Central de diagnóstico estratégico Meta Ads.
- `/trafego-escalar`. Escala campanhas Meta Ads já validadas e performando, sem destruir aprendizado.
- `/trafego-insights`. Lê métricas de campanhas Meta Ads (Facebook + Instagram) com cálculo automático de métricas derivadas (connect rate, taxa de conversão por etapa, custo por etapa, hook rate).
- `/trafego-oferta-funil`. Diagnóstico pós-clique, leitura da página e análise da oferta para Meta Ads, a partir dos números do funil.
- `/trafego-otimizar`. Diagnostica e otimiza campanhas Meta Ads em veiculação.
- `/trafego-pixel`. Diagnostica os pixels do Meta Ads (Meta Pixel / conjuntos de dados) da conta de anúncios.
- `/trafego-publicos`. Cria, lista e gerencia públicos (audiences) do Meta Ads pelo MCP da Meta (padrão) ou pela Marketing API (modo App).
- `/trafego-regras`. Cria automações no Meta Ads.
- `/trafego-testes`. Cria testes A/B disciplinados e variações estruturadas no Meta Ads, pelo MCP da Meta (padrão) ou pela Marketing API (modo App).

## Dados e Automações

- `/adaptar-plataforma`. Converte scripts e instruções Windows/PowerShell para Mac ou Linux.
- `/ads-relatorio`. Configura as credenciais e preferências do relatório de Facebook Ads (canal, métricas, filtro de campanhas) e oferece envio imediato via /enviar-relatorio-ads.
- `/dados-instagram`. Analisar um perfil do Instagram coletando dados públicos (bio, últimos posts, engajamento, temas recorrentes, horários).
- `/dashboard-concorrente-remover`. Remover um concorrente analisado anteriormente em /dashboard-social.
- `/enviar-relatorio-ads`. Busca as métricas do Facebook Ads e envia o relatório pelo Telegram ou WhatsApp.
- `/workshop-office`. Liga a Sala dos Agentes (live-office).
- `dashboard-social`. Porta de entrada unificada para configurar e atualizar os dashboards de métricas do Instagram, TikTok, YouTube e LinkedIn.
- `instagram-dashboard`. Configura dashboard HTML de métricas do Instagram via Apify.
- `tiktok-dashboard`. Configura dashboard HTML de métricas do TikTok via Apify.
- `youtube-dashboard`. Configura dashboard HTML de métricas do YouTube via Apify.
- `linkedin-dashboard`. Configura e gera o dashboard HTML de métricas do LinkedIn para o produto ativo.
- `biblioteca-anuncios`. Investiga criativos escalados na Biblioteca de Anúncios da Meta.

## Estratégia

- `/estrategia-funil`. Mapear funil de vendas completo.
- `/estrategia-lancamento`. Planejar lançamento ou evento completo.

## Estudo

- `gestor-pedagogico`. Gestor pedagógico. O mentorado manda um material de ensino (texto colado ou link do YouTube) e a skill pergunta o que ele quer gerar a partir dele, entre 8 entregáveis: transcrição, mapa mental, apostila, avaliação…

## Comercial

- `/comercial-playbook`. Gerar o playbook comercial completo de venda 1:1 por WhatsApp (middle e low ticket) do produto ativo.

## Vídeo

- `/video-editar`. Editar vídeos gravados com FFmpeg: edição automática da fala (legenda, corte de erros e corte de silêncios) e edições manuais (cortar, juntar, redimensionar, legendar, música, comprimir, extrair áudio, efeitos).
- `/video-efeitos`. Aplicar motion graphics animados em vídeos existentes usando GSAP + Puppeteer + FFmpeg.
- `/video-heygen`. Criar vídeo com avatar IA usando HeyGen com múltiplas cenas, avatares rotacionados, backgrounds variados e direção visual baseada em dados reais (Apify/dashboard) ou Urgências Ocultas do perfil.
- `/video-remotion`. Criar vídeo para Meta Ads com Remotion.

## Infraestrutura de Página

- `/pagina-active`. Conectar uma página de captura HTML ao ActiveCampaign via API.
- `/pagina-ajuste`. Ajustes pós-merge guiados por perguntas.
- `/pagina-checkout`. Conectar uma página HTML pronta ao checkout (Hotmart, Kiwify, Eduzz, Cakto, Pepper, Stripe ou link próprio).
- `/pagina-lovable`. Levar uma página HTML do projeto para o Lovable e devolver o link público.
- `/pagina-performance`. Auditar performance de uma página HTML pronta (peso, imagens, fontes, CSS/JS, Core Web Vitals estimados) e corrigir os problemas automaticamente.
- `/pagina-pixel`. Instalar Meta Pixel (Facebook Pixel) numa página HTML pronta.
- `/pagina-precheckout`. Criar uma página de pré-checkout leve que captura nome, email e WhatsApp antes de enviar o lead pro checkout real.
- `/pagina-vercel`. Publicar uma página HTML do projeto direto na Vercel via API e devolver o link público.
- `/pagina-visual`. Criar página de vendas a partir de prints de referência do aluno + copy aprovada.

## Feedback

- `/feedback-low-ticket`. Faz correção completa de página de vendas low ticket pela régua v16 do time de criativos.
- `/feedback-pagina`. Faz correção completa de página de vendas como Nav do Fluxo.

## Toolkit

- `/toolkit-anotar`. Registrar uma pendência, ideia ou lembrete no projeto ativo sem interromper o fluxo.
- `/toolkit-executar`. Executar a próxima etapa pendente do plano do projeto ativo.
- `/toolkit-novo`. Iniciar um novo projeto de marketing estruturado (lançamento, funil completo, reestruturação).
- `/toolkit-pausar`. Pausar o projeto ativo. Salva um resumo do estado e libera o produto para trabalhar em outra coisa sem perder contexto.
- `/toolkit-planejar`. Gerar o plano em etapas do projeto ativo a partir do roteiro.
- `/toolkit-progresso`. Mostrar o estado atual do projeto ativo.
- `/toolkit-retomar`. Retomar um projeto pausado do produto ativo.
- `/toolkit-verificar`. Conferir se o projeto entregou o que foi prometido no roteiro.

## Configurações

- `/configurar-apify`. Guia para criar conta no Apify, gerar o Personal API Token e salvar no .env como APIFY_API_TOKEN.
- `/configurar-heygen`. Guia para conectar uma conta do HeyGen ao projeto (vídeos com avatar IA).
- `/configurar-higgsfield`. Guia para conectar o Higgsfield ao Claude via conector personalizado (MCP), permitindo animar criativos direto pelo chat.
- `/configurar-imagens`. Guia para conectar uma API de geração de imagens (OpenRouter) ao projeto.
- `/configurar-replicate`. Guia para criar conta no Replicate (via GitHub), gerar o API Token e salvar no .env como REPLICATE_API_TOKEN.
- `/configurar-telegram`. Guia para criar um bot no Telegram via BotFather, obter o Chat ID e conectar ao Workshop para envio de relatórios e automações.
- `/configurar-zapi`. Guia para criar conta na Z-API, configurar uma instância e conectar o WhatsApp para envio de mensagens automatizadas.
- `/tutorial-ferramentas`. Gera a Trilha de Ferramentas do workshop em HTML.

## Agentes Especialistas (tarefas completas)

- `estrategista-de-produto`. Agente orquestrador de concepção de produto VTSD.
- `estrategista-low-ticket`. Agente orquestrador que conduz o aluno do zero ao funil de produto de entrada completo.
- `estrategista-middle-ticket`. Agente orquestrador que conduz o aluno do zero ao funil de produto principal completo.
- `estrategista-ht`. Agente orquestrador do funil completo de High Ticket (C10X).
- `construtor-de-paginas`. Agente orquestrador de páginas web.
- `criador-de-campanhas`. Agente orquestrador de campanhas de tráfego pago.
- `consultor-comercial`. Agente orquestrador de playbooks comerciais.
- `copywriter`. Agente orquestrador de copywriting Light Copy.
- `video-maker`. Agente orquestrador de produção de vídeo.
- `executor-de-plano-de-acao`. Agente autônomo que recebe a transcrição da última análise e a lista de tarefas do plano de ação, e executa cada tarefa acionando as skills e agentes necessários.
