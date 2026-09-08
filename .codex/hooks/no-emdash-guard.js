#!/usr/bin/env node
// Hook PreToolUse para Write/Edit. Bloqueia inser\u00e7\u00e3o de travess\u00e3o (—).
// Regra absoluta do CLAUDE.md: nada de — em nenhum texto gerado.
// S\u00f3 verifica conte\u00fado em arquivos .md e .html dentro de entregas/.

const fs = require('fs');

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const event = JSON.parse(input || '{}');
    const tool = event.tool_name || '';
    const params = event.tool_input || {};

    if (tool !== 'Write' && tool !== 'Edit') {
      process.exit(0);
    }

    const path = params.file_path || '';
    // S\u00f3 fiscaliza entregas (copy do aluno) e textos markdown/html.
    const isEntrega = path.replace(/\\\\/g, '/').includes('/entregas/');
    const isText = /\.(md|html|txt)$/i.test(path);
    if (!isEntrega || !isText) {
      process.exit(0);
    }

    const content = params.content || params.new_string || '';
    if (typeof content !== 'string') process.exit(0);

    if (content.includes('\u2014')) {
      const lines = content.split(/\r?\n/);
      const hits = [];
      lines.forEach((line, i) => {
        if (line.includes('\u2014')) hits.push(`linha ${i + 1}: ${line.trim().slice(0, 80)}`);
      });
      const msg = [
        'BLOQUEADO: travess\u00e3o (—) detectado.',
        'CLAUDE.md proibe travess\u00e3o em qualquer texto gerado.',
        'Substitua por ponto, dois pontos, v\u00edrgula, par\u00eanteses ou quebra de linha.',
        '',
        'Ocorr\u00eancias:',
        ...hits.slice(0, 5)
      ].join('\n');
      console.error(msg);
      process.exit(2);
    }

    process.exit(0);
  } catch (err) {
    // Falha do hook n\u00e3o deve quebrar o fluxo.
    process.exit(0);
  }
});
