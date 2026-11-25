#!/usr/bin/env node
// Hook PreToolUse para Write/Edit/MultiEdit. Bloqueia gravar token, chave de API
// ou credencial com valor real em qualquer arquivo que não seja o .env.
// Regra global do CLAUDE.md: "Tokens e segredos apenas no .env".
// Placeholders (EAA..., <TOKEN>, ***TOKEN_MASCARADO***, ${VARIAVEL}) passam.

const path = require('path');

// Arquivos onde segredo real é permitido.
const ENV_PERMITIDO = /^\.env(\.(local|development|production|test))?$/i;

const PADROES = [
  { nome: 'token da Meta (Facebook/Instagram)', re: /\bEAA[A-Za-z0-9]{30,}/g },
  { nome: 'chave de API no formato sk- (OpenAI, Anthropic, OpenRouter)', re: /(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}/g },
  { nome: 'chave secreta do Stripe', re: /\b[sr]k_live_[A-Za-z0-9]{16,}/g },
  { nome: 'token do Slack', re: /\bxox[abprs]-[A-Za-z0-9-]{10,}/g },
  { nome: 'token de bot do Telegram', re: /\b\d{8,10}:AA[A-Za-z0-9_-]{30,}/g },
  { nome: 'token do GitHub', re: /\bgh[pousr]_[A-Za-z0-9]{36,}/g },
  { nome: 'chave de API do Google', re: /\bAIza[0-9A-Za-z_-]{35}/g },
  { nome: 'token da Apify', re: /\bapify_api_[A-Za-z0-9]{20,}/g },
  { nome: 'token JWT (Bearer, service_role)', re: /\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/g },
  { nome: 'access_token escrito na URL', re: /access_token=(?![$<{*])[A-Za-z0-9._-]{30,}/g },
];

// Exemplo de documentação marcado com sequência de "x" (ex: 123456789:AAFxxxxxxxx) não é segredo.
function pareceExemplo(valor) {
  return /x{5,}/i.test(valor);
}

// Mostra só o começo e o fim do valor, para a mensagem de bloqueio não vazar o segredo.
function mascarar(valor) {
  if (valor.length <= 12) return '***';
  return `${valor.slice(0, 4)}...${valor.slice(-4)}`;
}

function textosGravados(tool, params) {
  if (tool === 'Write') return [params.content];
  if (tool === 'Edit') return [params.new_string];
  if (tool === 'MultiEdit') return (params.edits || []).map(e => e && e.new_string);
  return [];
}

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const event = JSON.parse(input || '{}');
    const tool = event.tool_name || '';
    const params = event.tool_input || {};

    if (!['Write', 'Edit', 'MultiEdit'].includes(tool)) process.exit(0);

    const arquivo = params.file_path || '';
    if (ENV_PERMITIDO.test(path.basename(arquivo))) process.exit(0);

    const achados = [];
    for (const texto of textosGravados(tool, params)) {
      if (typeof texto !== 'string' || !texto) continue;
      // Imagens embutidas em base64 geram sequências aleatórias que imitam token.
      const limpo = texto.replace(/data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+/g, '');
      for (const { nome, re } of PADROES) {
        for (const m of limpo.matchAll(re)) {
          if (pareceExemplo(m[0])) continue;
          achados.push(`${nome}: ${mascarar(m[0])}`);
        }
      }
    }

    if (achados.length) {
      const msg = [
        'BLOQUEADO: segredo com valor real detectado fora do .env.',
        'Regra do CLAUDE.md: token, chave de API e credencial só podem ficar no .env.',
        'Troque o valor por leitura do .env (os.environ.get, process.env, source .env) ou por um placeholder (<TOKEN>, EAA..., ***TOKEN_MASCARADO***) e grave de novo.',
        '',
        `Arquivo: ${arquivo}`,
        'Ocorrências (mascaradas):',
        ...[...new Set(achados)].slice(0, 5).map(a => `- ${a}`)
      ].join('\n');
      console.error(msg);
      process.exit(2);
    }

    process.exit(0);
  } catch (err) {
    // Falha do hook não deve quebrar o fluxo.
    process.exit(0);
  }
});
