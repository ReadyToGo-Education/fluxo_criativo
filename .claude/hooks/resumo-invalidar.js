#!/usr/bin/env node
// PostToolUse hook: quando o agente grava perfil.md, idconsumidor.md ou
// pesquisa-mercado.md de um produto, apaga o resumo-produto.md daquele produto.
// A próxima entrega não encontra o resumo e ele é gerado de novo, já atualizado
// (regra "Resumo do Produto" do CLAUDE.md e skill resumo-produto).
//
// Entende os dois formatos de edição:
//   - Claude Code: Write, Edit e MultiEdit trazem tool_input.file_path
//   - Codex: apply_patch traz o patch em tool_input.command, com linhas
//     "*** Add File: ...", "*** Update File: ..." e "*** Delete File: ..."
//
// Nunca bloqueia: qualquer erro termina com exit 0.

'use strict';

const fs = require('fs');
const path = require('path');

const ORIGINAIS = /(^|\/)meus-produtos\/[^/]+\/(perfil|idconsumidor|pesquisa-mercado)\.md$/i;

let input = '';
process.stdin.on('data', (c) => (input += c));
process.stdin.on('end', () => {
  try {
    const event = JSON.parse(input || '{}');
    const params = event.tool_input || {};
    const cwd = event.cwd || process.cwd();

    for (const arquivo of arquivosGravados(event.tool_name || '', params)) {
      const normalizado = arquivo.replace(/\\/g, '/');
      if (!ORIGINAIS.test(normalizado)) continue;
      const absoluto = path.isAbsolute(arquivo) ? arquivo : path.join(cwd, arquivo);
      try {
        fs.unlinkSync(path.join(path.dirname(absoluto), 'resumo-produto.md'));
      } catch (e) {
        // O resumo ainda não existia: nada a fazer.
      }
    }
  } catch (e) {
    // Fail-open: nunca atrapalha a gravação.
  }
  process.exit(0);
});

function arquivosGravados(tool, params) {
  if (tool === 'Write' || tool === 'Edit' || tool === 'MultiEdit') {
    return params.file_path ? [String(params.file_path)] : [];
  }
  if (tool === 'apply_patch' && typeof params.command === 'string') {
    const arquivos = [];
    const linha = /^\*\*\* (?:Add|Update|Delete) File: (.+)$/gm;
    let m;
    while ((m = linha.exec(params.command)) !== null) arquivos.push(m[1].trim());
    return arquivos;
  }
  return [];
}
