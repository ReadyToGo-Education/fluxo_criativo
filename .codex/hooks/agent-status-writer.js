#!/usr/bin/env node
// agent-status-writer.js, PostToolUse hook v4
// Grava o status do agente ativo em .claude/agents-memory/agents-status.json
// (lido pelo workshop-live-office.html via polling local em http://localhost:4000).
// Inclui produto ativo no _meta pro painel exibir.
// Opcionalmente faz POST pra API remota se WORKSHOP_TOKEN estiver no .env.

const fs = require('fs')
const path = require('path')
const https = require('https')
const http = require('http')

const stdinTimeout = setTimeout(() => process.exit(0), 10000)
let input = ''
process.stdin.setEncoding('utf8')
process.stdin.on('data', chunk => input += chunk)
process.stdin.on('end', () => {
  clearTimeout(stdinTimeout)
  try {
    const data = JSON.parse(input)
    const cwd = data.cwd || process.cwd()

    // Carrega .env (opcional, só pra POST remoto)
    const envPath = path.join(cwd, '.env')
    let token = process.env.WORKSHOP_TOKEN || ''
    let apiUrl = process.env.WORKSHOP_API_URL || 'https://workshop-office.vercel.app/api/status'

    if (fs.existsSync(envPath)) {
      const env = fs.readFileSync(envPath, 'utf8')
      for (const line of env.split('\n')) {
        const [k, ...v] = line.split('=')
        const key = (k || '').trim()
        const val = v.join('=').trim().replace(/^["']|["']$/g, '')
        if (key === 'WORKSHOP_TOKEN' && !process.env.WORKSHOP_TOKEN) token = val
        if (key === 'WORKSHOP_API_URL' && !process.env.WORKSHOP_API_URL) apiUrl = val
      }
    }

    const toolName = data.tool_name || data.tool || ''
    const toolInput = data.tool_input || {}
    const sessionId = data.session_id || ''

    // Lista de agentes válidos (também usada como fallback de pattern matching)
    const agentPatterns = [
      { id: 'copywriter',                patterns: ['copy', 'headline', 'lead', 'roteiro-copy', 'bullet', 'cta'] },
      { id: 'construtor-de-paginas',     patterns: ['pagina', 'landing', 'hero', 'checkout', 'pv', 'workshop-live-office', '8d'] },
      { id: 'criador-de-campanhas',      patterns: ['campanha', 'ads', 'trafego', 'meta-ads', 'criativo', 'anuncio'] },
      { id: 'estrategista-de-produto',   patterns: ['produto', 'vtsd', 'concepcao', 'idconsumidor', 'pesquisa-mercado', 'perfil.md', 'mercado', 'nicho', 'painel', 'scripts/'] },
      { id: 'video-maker',               patterns: ['video', 'vsl', 'heygen', 'remotion', 'avatar'] },
      { id: 'consultor-comercial',       patterns: ['comercial', 'playbook', 'spin', 'objecao', 'fechamento', 'whatsapp'] },
      { id: 'estrategista-low-ticket',   patterns: ['low-ticket', 'lt-', 'tripwire', 'quiz', 'low ticket'] },
      { id: 'estrategista-middle-ticket',patterns: ['middle-ticket', 'perpetuo', 'mt-', 'middle ticket'] },
      { id: 'estrategista-ht',           patterns: ['high-ticket', 'c10x', 'retiro', 'ht-', 'high ticket'] },
      { id: 'produtor-de-conteudo',      patterns: ['conteudo', 'carrossel', 'reels', 'editorial', 'social', 'instagram'] },
      { id: 'executor-de-plano-de-acao', patterns: ['plano', 'executor', 'todo', 'tarefa', 'toolkit'] },
    ]

    // Mapeamento direto skill -> agente + texto pronto pro painel
    const skillMap = {
      // Produto
      'produto-novo':              { agent: 'estrategista-de-produto', task: 'criando produto novo' },
      'produto-concepcao':         { agent: 'estrategista-de-produto', task: 'concebendo produto' },
      'produto-consumidor':        { agent: 'estrategista-de-produto', task: 'criando identidade do consumidor' },
      'produto-trocar':            { agent: 'estrategista-de-produto', task: 'trocando produto ativo' },
      'produto-zerar':             { agent: 'estrategista-de-produto', task: 'zerando produto' },
      'produto-excluir':           { agent: 'estrategista-de-produto', task: 'excluindo produto' },
      'pesquisa-mercado':          { agent: 'estrategista-de-produto', task: 'pesquisando mercado' },
      'concepcao-produto':         { agent: 'estrategista-de-produto', task: 'concebendo produto' },
      'furadeira-visual':          { agent: 'estrategista-de-produto', task: 'desenhando a Furadeira' },
      'vtsd-completo':             { agent: 'estrategista-de-produto', task: 'consultando metodologia VTSD' },

      // Páginas
      'copy-pagina':               { agent: 'construtor-de-paginas', task: 'escrevendo copy de pagina' },
      'pagina-de-vendas':          { agent: 'construtor-de-paginas', task: 'montando pagina de vendas' },
      'pagina-ajuste':             { agent: 'construtor-de-paginas', task: 'ajustando pagina' },
      'pagina-checkout':           { agent: 'construtor-de-paginas', task: 'configurando checkout' },
      'pagina-pixel':              { agent: 'construtor-de-paginas', task: 'instalando Pixel' },
      'pagina-performance':        { agent: 'construtor-de-paginas', task: 'otimizando pagina' },
      'pagina-precheckout':        { agent: 'construtor-de-paginas', task: 'criando pre-checkout' },
      'pagina-lovable':            { agent: 'construtor-de-paginas', task: 'publicando no Lovable' },
      'pagina-vercel':             { agent: 'construtor-de-paginas', task: 'publicando na Vercel' },
      'pagina-active':             { agent: 'construtor-de-paginas', task: 'conectando ActiveCampaign' },
      'feedback-pagina':           { agent: 'construtor-de-paginas', task: 'auditando pagina de vendas' },
      'feedback-low-ticket':       { agent: 'construtor-de-paginas', task: 'auditando pagina low ticket' },
      'feedback-de-pv':            { agent: 'construtor-de-paginas', task: 'auditando pagina de vendas' },
      'paginas':                   { agent: 'construtor-de-paginas', task: 'consultando referencias de pagina' },

      // Campanhas / Anúncios
      'copy-anuncio':              { agent: 'criador-de-campanhas', task: 'escrevendo anuncio' },
      'criativo-aida':             { agent: 'criador-de-campanhas', task: 'criando criativo AIDA' },
      'criativo-de-imagem':        { agent: 'criador-de-campanhas', task: 'criando criativo visual' },
      'img-anuncio':               { agent: 'criador-de-campanhas', task: 'gerando imagem do anuncio' },
      'avat-whisk':                { agent: 'criador-de-campanhas', task: 'briefando Whisk' },
      'imagem-prompt':             { agent: 'criador-de-campanhas', task: 'gerando prompt de imagem' },
      'ads-relatorio':             { agent: 'criador-de-campanhas', task: 'configurando relatorio Ads' },
      'enviar-relatorio-ads':      { agent: 'criador-de-campanhas', task: 'enviando relatorio Ads' },
      'lt-otimizar':               { agent: 'criador-de-campanhas', task: 'otimizando campanhas' },
      'estrategia-funil':          { agent: 'criador-de-campanhas', task: 'mapeando funil' },
      'estrategia-lancamento':     { agent: 'criador-de-campanhas', task: 'planejando lancamento' },
      'anuncios':                  { agent: 'criador-de-campanhas', task: 'consultando anuncios VTSD' },
      'anuncios-texto':            { agent: 'criador-de-campanhas', task: 'consultando anuncios estaticos' },
      'anuncios-video':            { agent: 'criador-de-campanhas', task: 'consultando anuncios em video' },
      'trafego-pago':              { agent: 'criador-de-campanhas', task: 'consultando trafego pago' },

      // Copy direta
      'copy-emails':               { agent: 'copywriter', task: 'escrevendo emails' },
      'elementos-literarios':      { agent: 'copywriter', task: 'aplicando elementos literarios' },
      'revisora':                  { agent: 'copywriter', task: 'revisando copy' },

      // Conteúdo
      'copy-social':               { agent: 'produtor-de-conteudo', task: 'criando conteudo social' },
      'copy-variacao-post':        { agent: 'produtor-de-conteudo', task: 'gerando variacoes de post' },
      'dados-instagram':           { agent: 'produtor-de-conteudo', task: 'analisando Instagram' },
      'instagram-dashboard':       { agent: 'produtor-de-conteudo', task: 'gerando dashboard do Instagram' },
      'dados-nicho':               { agent: 'produtor-de-conteudo', task: 'mapeando perfis do nicho' },
      'conteudo':                  { agent: 'produtor-de-conteudo', task: 'consultando linha de conteudo' },

      // Vídeo
      'copy-roteiro':              { agent: 'video-maker', task: 'escrevendo roteiro de video' },
      'video-heygen':              { agent: 'video-maker', task: 'criando video com avatar' },
      'video-remotion':            { agent: 'video-maker', task: 'criando video com Remotion' },
      'video-editar':              { agent: 'video-maker', task: 'editando video' },
      'vsl-video-vendas':          { agent: 'video-maker', task: 'escrevendo VSL' },
      'video-avancado':            { agent: 'video-maker', task: 'consultando formatos de video' },

      // Comercial
      'comercial-playbook':        { agent: 'consultor-comercial', task: 'montando playbook comercial' },
      'playbook-comercial':        { agent: 'consultor-comercial', task: 'montando playbook comercial' },

      // Low Ticket
      'lt-funil':                  { agent: 'estrategista-low-ticket', task: 'montando funil low ticket' },
      'lt-criar-produto':          { agent: 'estrategista-low-ticket', task: 'criando produto low ticket' },
      'lt-quiz':                   { agent: 'estrategista-low-ticket', task: 'gerando quiz' },
      'lt-pagina':                 { agent: 'estrategista-low-ticket', task: 'escrevendo copy low ticket' },
      'criacao-produto-low-ticket':{ agent: 'estrategista-low-ticket', task: 'criando conteudo do produto' },
      'app-saas':                  { agent: 'estrategista-low-ticket', task: 'planejando SaaS' },
      'criar-gpt':                 { agent: 'estrategista-low-ticket', task: 'criando agente GPT' },
      'agente-gpt':                { agent: 'estrategista-low-ticket', task: 'consultando agente GPT' },

      // High Ticket
      'ht-anuncios':               { agent: 'estrategista-ht', task: 'criando anuncios HT' },
      'ht-apresentacao-proposta':  { agent: 'estrategista-ht', task: 'preparando apresentacao da proposta' },
      'ht-big-idea':               { agent: 'estrategista-ht', task: 'criando Big Idea' },
      'ht-comunicacao-pre':        { agent: 'estrategista-ht', task: 'comunicacao pre evento' },
      'ht-conteudo':               { agent: 'estrategista-ht', task: 'roteirizando conteudo HT' },
      'ht-cronograma':             { agent: 'estrategista-ht', task: 'montando cronograma HT' },
      'ht-diagnostico':            { agent: 'estrategista-ht', task: 'roteiro de diagnostico' },
      'ht-fechamento':             { agent: 'estrategista-ht', task: 'script de fechamento HT' },
      'ht-follow-up':              { agent: 'estrategista-ht', task: 'follow-up HT' },
      'ht-objecoes':               { agent: 'estrategista-ht', task: 'mapeando objecoes' },
      'ht-oferta':                 { agent: 'estrategista-ht', task: 'estruturando oferta HT' },
      'ht-onboarding':             { agent: 'estrategista-ht', task: 'criando onboarding HT' },
      'ht-pagina-inscricao':       { agent: 'estrategista-ht', task: 'pagina de inscricao HT' },
      'ht-pitch-palco':            { agent: 'estrategista-ht', task: 'pitch de palco HT' },
      'ht-proposta':               { agent: 'estrategista-ht', task: 'proposta comercial HT' },
      'ht-repitch':                { agent: 'estrategista-ht', task: 'repitch HT' },
      'ht-spin':                   { agent: 'estrategista-ht', task: 'roteiro SPIN' },
      'ht-whatsapp':               { agent: 'estrategista-ht', task: 'fluxo WhatsApp HT' },

      // Toolkit / Executor
      'toolkit-novo':              { agent: 'executor-de-plano-de-acao', task: 'iniciando projeto' },
      'toolkit-planejar':          { agent: 'executor-de-plano-de-acao', task: 'planejando projeto' },
      'toolkit-executar':          { agent: 'executor-de-plano-de-acao', task: 'executando proxima etapa' },
      'toolkit-verificar':         { agent: 'executor-de-plano-de-acao', task: 'auditando projeto' },
      'toolkit-progresso':         { agent: 'executor-de-plano-de-acao', task: 'mostrando progresso' },
      'toolkit-anotar':            { agent: 'executor-de-plano-de-acao', task: 'anotando pendencia' },
      'toolkit-pausar':            { agent: 'executor-de-plano-de-acao', task: 'pausando projeto' },
      'toolkit-retomar':           { agent: 'executor-de-plano-de-acao', task: 'retomando projeto' },
      'painel-atualizar':          { agent: 'executor-de-plano-de-acao', task: 'atualizando painel global' },
      'tutorial-ferramentas':      { agent: 'executor-de-plano-de-acao', task: 'gerando trilha de ferramentas' },
      'adaptar-plataforma':        { agent: 'executor-de-plano-de-acao', task: 'adaptando para sua plataforma' },
    }

    const searchStr = (
      (toolInput.file_path || '') + ' ' +
      (toolInput.path || '') + ' ' +
      (toolInput.command || '') + ' ' +
      (toolInput.query || '') + ' ' +
      (toolInput.prompt || '') + ' ' +
      (toolInput.url || '') + ' ' +
      JSON.stringify(toolInput)
    ).toLowerCase()

    let activeAgent = null
    let directTaskDesc = null

    // Prioridade 1. Skill direto
    if (toolName === 'Skill' && toolInput.skill) {
      const entry = skillMap[toolInput.skill]
      if (entry) {
        activeAgent = entry.agent
        directTaskDesc = entry.task
      } else {
        directTaskDesc = 'rodando skill: ' + toolInput.skill
      }
    }

    // Prioridade 2. Agent (subagente) pelo subagent_type
    const subagentTaskMap = {
      'pesquisa-mercado':           'pesquisando mercado (9 eixos)',
      'gerador-decorados':          'gerando 50 Decorados',
      'gerador-urgencias-ocultas':  'gerando 70 Urgencias Ocultas',
      'gerador-idconsumidor':       'gerando Identidade do Consumidor',
      'revisor-perfil':             'revisando perfil do produto',
      'revisor-pesquisa':           'revisando pesquisa de mercado',
      'revisor-idconsumidor':       'revisando identidade do consumidor',
    }
    if (!activeAgent && (toolName === 'Agent' || toolName === 'Task') && toolInput.subagent_type) {
      const sub = toolInput.subagent_type
      if (agentPatterns.find(a => a.id === sub)) {
        activeAgent = sub
        directTaskDesc = 'agente em campo'
      } else if (subagentTaskMap[sub]) {
        activeAgent = 'estrategista-de-produto'
        directTaskDesc = subagentTaskMap[sub]
      }
    }

    // Prioridade 3. Detecção por palavra-chave
    if (!activeAgent) {
      for (const agent of agentPatterns) {
        if (agent.patterns.some(p => searchStr.includes(p))) {
          activeAgent = agent.id
          break
        }
      }
    }

    // Prioridade 4. Detecção pelo arquivo de memória
    const filePath = toolInput.file_path || toolInput.path || ''
    if (!activeAgent && filePath.includes('agents-memory/')) {
      const memFile = path.basename(filePath, '.md')
      if (agentPatterns.find(a => a.id === memFile)) activeAgent = memFile
    }

    // Fallback. Usa o último agente ativo em vez de fixar copywriter
    if (!activeAgent) activeAgent = prevMeta.lastActive || 'estrategista-de-produto'

    const toolDescriptions = {
      Write: 'escrevendo',
      Edit: 'editando',
      MultiEdit: 'editando',
      Read: 'lendo contexto',
      Bash: 'executando',
      Agent: 'acionando agente',
      Task: 'executando task',
      Skill: 'rodando skill',
      WebFetch: 'buscando referencia',
      WebSearch: 'pesquisando',
    }

    const fname = path.basename(filePath)

    function humanizeTask() {
      const cmd = (toolInput.command || '').trim().toLowerCase()

      if (filePath) {
        const p = filePath.toLowerCase()
        if (p.endsWith('/.ativo')) return 'ativando produto'
        if (p.endsWith('/tipo.md')) return 'definindo tipo do produto'
        if (p.endsWith('/nome.txt')) return 'salvando nome do produto'
        if (p.endsWith('/perfil.md')) return 'atualizando perfil do produto'
        if (p.endsWith('/idconsumidor.md')) return 'criando identidade do consumidor'
        if (p.endsWith('/pesquisa-mercado.md')) return 'salvando pesquisa de mercado'
        if (p.includes('/entregas/paginas/')) return 'construindo pagina'
        if (p.includes('/entregas/anuncios/')) return 'escrevendo anuncio'
        if (p.includes('/entregas/emails/')) return 'escrevendo email'
        if (p.includes('/entregas/copy-pagina/')) return 'escrevendo copy da pagina'
        if (p.includes('/entregas/conteudo-social/')) return 'criando conteudo social'
        if (p.includes('/entregas/criativos/')) return 'criando briefing visual'
        if (p.includes('/entregas/comercial/')) return 'montando playbook comercial'
        if (p.includes('/entregas/textos-de-venda/')) return 'escrevendo texto de venda'
        if (p.includes('/entregas/videos/')) return 'preparando video'
        if (p.includes('/.claude/hooks/')) return 'ajustando o painel'
        if (p.includes('/.claude/settings.json')) return 'ajustando configuracao'
        if (p.includes('/.claude/commands/')) return 'criando comando'
        if (p.includes('workshop-live-office')) return 'ajustando o painel'
        if (p.includes('/projeto/') && p.endsWith('roteiro.md')) return 'redigindo roteiro do projeto'
        if (p.includes('/projeto/') && p.endsWith('plano.md')) return 'montando plano de execucao'
        return (toolName === 'Write' ? 'criando' : 'ajustando') + ': ' + fname
      }

      if (cmd) {
        if (cmd.startsWith('mkdir')) return 'criando estrutura de pastas'
        if (/^(ls|find|grep|tree)\b/.test(cmd)) return 'explorando arquivos'
        if (/^(cat|head|tail|wc|less|more)\b/.test(cmd)) return 'lendo arquivo'
        if (cmd.startsWith('curl')) return 'testando servidor'
        if (cmd.includes('npx serve')) return 'subindo servidor local'
        if (cmd.includes('lsof')) return 'verificando porta'
        if (cmd.includes('--check')) return 'validando codigo'
        if (/^node\b/.test(cmd)) return 'rodando script'
        if (/^(python|python3|py)\b/.test(cmd)) return 'rodando script Python'
        if (cmd.startsWith('open ')) return 'abrindo no navegador'
        if (cmd.startsWith('echo ') && (cmd.includes('"cwd"') || cmd.includes('json'))) return 'testando integracao'
        if (cmd.startsWith('echo')) return 'verificando estado'
        if (/^git\b/.test(cmd)) return 'comando git'
        if (/^rm\b/.test(cmd)) return 'removendo arquivo'
        if (/^(cp|mv)\b/.test(cmd)) return 'organizando arquivos'
        if (cmd.startsWith('if ') || cmd.includes('then ')) return 'verificando estado'
        if (/^npm\b/.test(cmd) || /^npx\b/.test(cmd)) return 'gerenciando pacotes'
        // Fallback: mostra o comando truncado em vez de "rodando comando"
        const short = cmd.length > 38 ? cmd.slice(0, 35) + '...' : cmd
        return '$ ' + short
      }

      if (toolInput.query) {
        return 'pesquisando: ' + String(toolInput.query).slice(0, 50)
      }
      if (toolInput.url) {
        try {
          const u = new URL(toolInput.url)
          return 'lendo: ' + u.hostname
        } catch (e) {
          return 'lendo pagina externa'
        }
      }
      if (toolInput.subagent_type) {
        return 'agente em campo: ' + toolInput.subagent_type
      }
      if (toolInput.description) {
        return String(toolInput.description).slice(0, 50)
      }
      return toolDescriptions[toolName] || 'trabalhando'
    }

    const taskDesc = directTaskDesc || humanizeTask()

    // Lê produto ativo pra mostrar no painel
    let activeProduct = ''
    let activeProductName = ''
    let progress = {}
    try {
      const ativoPath = path.join(cwd, 'meus-produtos', '.ativo')
      if (fs.existsSync(ativoPath)) {
        activeProduct = fs.readFileSync(ativoPath, 'utf8').trim()
        if (activeProduct) {
          const productDir = path.join(cwd, 'meus-produtos', activeProduct)
          const nomePath = path.join(productDir, 'nome.txt')
          if (fs.existsSync(nomePath)) {
            activeProductName = fs.readFileSync(nomePath, 'utf8').trim()
          } else {
            activeProductName = activeProduct
          }

          // Mapeia o que já foi entregue
          const countMd = (dir) => {
            try {
              if (!fs.existsSync(dir)) return 0
              return fs.readdirSync(dir).filter(f => /\.(md|html|mp4|json)$/i.test(f)).length
            } catch (e) { return 0 }
          }
          // Verifica se uma seção do perfil.md tem conteúdo real (> 3 linhas não-vazias após o heading)
          const hasSection = (heading) => {
            try {
              const perfilPath = path.join(productDir, 'perfil.md')
              if (!fs.existsSync(perfilPath)) return false
              const lines = fs.readFileSync(perfilPath, 'utf8').split('\n')
              let inside = false, count = 0
              for (const line of lines) {
                if (line.startsWith('## ') && line.includes(heading)) { inside = true; continue }
                if (inside && line.startsWith('## ')) break
                if (inside && line.trim().length > 2) count++
              }
              return count >= 3
            } catch (e) { return false }
          }
          const ent = path.join(productDir, 'entregas')
          progress = {
            perfil: fs.existsSync(path.join(productDir, 'perfil.md')),
            pesquisa: fs.existsSync(path.join(productDir, 'pesquisa-mercado.md')),
            idconsumidor: fs.existsSync(path.join(productDir, 'idconsumidor.md')),
            furadeira: fs.existsSync(path.join(ent, 'furadeira-visual.html')),
            comunicador: hasSection('Identidade do Comunicador'),
            decorados: hasSection('Decorados'),
            urgencias: hasSection('Urgências Ocultas'),
            argumentos: hasSection('Argumentos Incontestáveis'),
            paginas: countMd(path.join(ent, 'paginas')),
            anuncios: countMd(path.join(ent, 'anuncios')),
            emails: countMd(path.join(ent, 'emails')),
            copyPagina: countMd(path.join(ent, 'copy-pagina')),
            conteudoSocial: countMd(path.join(ent, 'conteudo-social')),
            criativos: countMd(path.join(ent, 'criativos')),
            comercial: countMd(path.join(ent, 'comercial')),
            videos: countMd(path.join(ent, 'videos')),
          }
        }
      }
    } catch (e) {
      // silent fail
    }

    const now = new Date()
    const timeStr = now.toLocaleTimeString('pt-BR')
    const ts = Date.now()

    // ── Categorias da Sala (mapeia agente → 7 categorias visuais) ───────
    // prod, copy, pag, ad, vid, sales, data
    const agentCategoryMap = {
      'estrategista-de-produto':    'prod',
      'estrategista-low-ticket':    'prod',
      'estrategista-middle-ticket': 'prod',
      'executor-de-plano-de-acao':  'prod',
      'copywriter':                 'copy',
      'produtor-de-conteudo':       'copy',
      'construtor-de-paginas':      'pag',
      'criador-de-campanhas':       'ad',
      'video-maker':                'vid',
      'consultor-comercial':        'sales',
      'estrategista-ht':            'sales',
    }
    // Overrides por skill (quando a categoria correta diverge do agente)
    const skillCategoryOverride = {
      'dados-instagram':            'data',
      'dados-nicho':                'data',
      'instagram-dashboard':        'data',
      'tiktok-dashboard':           'data',
      'youtube-dashboard':          'data',
      'dashboard-social':           'data',
      'pesquisa-mercado-instagram': 'data',
      'pesquisa-mercado':           'data',
      'lt-otimizar':                'data',
      'ads-relatorio':              'data',
      'enviar-relatorio-ads':       'data',
    }
    // Sub-agentes de concepção que devem aparecer como Pesquisador (data)
    const subagentCategoryMap = {
      'pesquisa-mercado':           'data',
      'gerador-decorados':          'data',
      'gerador-urgencias-ocultas':  'data',
      'gerador-idconsumidor':       'data',
      'revisor-perfil':             'data',
      'revisor-pesquisa':           'data',
      'revisor-idconsumidor':       'data',
    }
    const skillId = (toolName === 'Skill' && toolInput.skill) ? toolInput.skill : ''
    const subType = ((toolName === 'Agent' || toolName === 'Task') && toolInput.subagent_type) ? toolInput.subagent_type : ''
    const activeCategory = skillCategoryOverride[skillId]
      || subagentCategoryMap[subType]
      || subagentCategoryMap[activeAgent]
      || agentCategoryMap[activeAgent]
      || 'prod'

    // Lê o JSON anterior pra preservar entradas de outros agentes
    const statusFile = path.join(cwd, '.claude', 'agents-memory', 'agents-status.json')
    let statusPayload = {}
    if (fs.existsSync(statusFile)) {
      try {
        statusPayload = JSON.parse(fs.readFileSync(statusFile, 'utf8'))
      } catch (e) {
        statusPayload = {}
      }
    }

    // Não força os outros pra idle. Cada agente carrega seu timestamp e o painel
    // decide se ainda está fresco (< 30s) ou se já expirou. Isso permite mostrar
    // múltiplos agentes em paralelo quando rodam simultaneamente.

    // Mantém lastSkill (preserva entre eventos pra usar como missão atual)
    const prevMeta = statusPayload._meta || {}
    let lastSkill = prevMeta.lastSkill || ''
    if (toolName === 'Skill' && toolInput.skill) {
      lastSkill = toolInput.skill
    }

    statusPayload._meta = {
      session: sessionId,
      lastTool: toolName,
      lastActive: activeAgent,
      lastCategory: activeCategory,
      lastTask: taskDesc,
      lastSkill,
      activeProduct,
      activeProductName,
      progress,
      updated: timeStr,
      timestamp: ts,
    }

    statusPayload[activeAgent] = {
      status: 'working',
      task: taskDesc,
      tool: toolName,
      category: activeCategory,
      skill: skillId || lastSkill || '',
      updated: timeStr,
      timestamp: ts,
    }

    // ── Agregação por categoria (consumo direto pela Sala) ────────────────
    // Mantém o histórico recente de cada categoria; bonecos da Sala são
    // pintados a partir disto, não dos agentes.
    if (!statusPayload.categories || typeof statusPayload.categories !== 'object') {
      statusPayload.categories = {}
    }
    statusPayload.categories[activeCategory] = {
      lastTool: toolName,
      lastTask: taskDesc,
      lastSkill: skillId || lastSkill || '',
      lastAgent: activeAgent,
      updated: timeStr,
      timestamp: ts,
    }

    // Grava local (essencial pro painel)
    try {
      fs.mkdirSync(path.dirname(statusFile), { recursive: true })
      const json = JSON.stringify(statusPayload, null, 2)
      fs.writeFileSync(statusFile, json)
      // Espelho .js: lido pelo painel via <script src> sem precisar de servidor.
      // Funciona em file:// (sem CORS) e via servidor estático.
      const jsFile = statusFile.replace(/\.json$/, '.js')
      fs.writeFileSync(
        jsFile,
        '// auto-gerado pelo agent-status-writer.js — não editar\nwindow.AGENTS_STATUS = ' + json + ';\n'
      )
    } catch (e) {
      // silent fail
    }

    // POST remoto opcional, só se token configurado
    if (token) {
      try {
        const body = JSON.stringify({ token, status: statusPayload })
        const url = new URL(apiUrl)
        const lib = url.protocol === 'https:' ? https : http
        const req = lib.request({
          hostname: url.hostname,
          port: url.port || (url.protocol === 'https:' ? 443 : 80),
          path: url.pathname,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(body),
          },
          timeout: 4000,
        }, () => {})
        req.on('error', () => {})
        req.on('timeout', () => req.destroy())
        req.write(body)
        req.end()
      } catch (e) {
        // silent fail
      }
    }
  } catch (e) {
    // silent fail
  }

  process.exit(0)
})
