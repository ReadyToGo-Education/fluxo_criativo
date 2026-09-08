#!/usr/bin/env node
// PostToolUse hook: valida meus-produtos/{slug}/dados/pesquisa.json.
// Campos obrigatorios:
//   1. KPI "Tamanho do Mercado" com valor real
//   2. KPI "Crescimento Anual" com valor real
//   3. Pelo menos 5 concorrentes mapeados, cada um com nome e promessa
//
// Sai com exit 2 (bloqueante) quando o JSON salvo estiver invalido.
// A mensagem vai para stderr e o Claude a recebe como feedback.

'use strict';

const path = require('path');
const fs = require('fs');

const MIN_CONCORRENTES = 5;
const PLACEHOLDERS = new Set(['', 'a mapear', 'preencher', 'tbd', '-']);

let input = '';
process.stdin.on('data', (c) => (input += c));
process.stdin.on('end', () => {
  try {
    const event = JSON.parse(input || '{}');
    const tool = event.tool_name || '';
    if (tool !== 'Write' && tool !== 'Edit' && tool !== 'MultiEdit') {
      process.exit(0);
    }

    const params = event.tool_input || {};
    const filePath = String(params.file_path || '').replace(/\\/g, '/');

    // Alvo: .../meus-produtos/<slug>/dados/pesquisa.json
    if (!/\/meus-produtos\/[^/]+\/dados\/pesquisa\.json$/.test(filePath)) {
      process.exit(0);
    }

    const conteudo = obterConteudo(params, filePath);
    if (!conteudo) process.exit(0);

    let dados;
    try {
      dados = JSON.parse(conteudo);
    } catch (e) {
      fail([`JSON invalido: ${e.message}`]);
      return;
    }

    const schema = carregarSchema();
    const erros = validarPesquisa(dados, schema);
    if (erros.length === 0) process.exit(0);
    fail(erros);
  } catch (e) {
    // Em caso de erro inesperado, nao bloqueia (fail-open).
    process.exit(0);
  }
});

function obterConteudo(params, filePath) {
  // Write: params.content traz o conteudo novo.
  if (typeof params.content === 'string' && params.content.length > 0) {
    return params.content;
  }
  // Edit/MultiEdit: le o arquivo final do disco (ja salvo pelo PostToolUse).
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch (_) {
    return null;
  }
}

function carregarSchema() {
  // .claude/hooks/painel-validar.js -> sobe 2 niveis ate a raiz do projeto.
  const root = path.resolve(__dirname, '..', '..');
  const schemaPath = path.join(
    root,
    'assets',
    'templates',
    'painel-entregas',
    'schemas',
    'pesquisa.json'
  );
  try {
    return JSON.parse(fs.readFileSync(schemaPath, 'utf-8'));
  } catch (_) {
    return null;
  }
}

function valorReal(valor, valorModelo) {
  if (valor == null) return false;
  if (typeof valor !== 'string' && typeof valor !== 'number') return false;
  const s = String(valor).trim().toLowerCase();
  if (PLACEHOLDERS.has(s)) return false;
  if (valorModelo != null && s === String(valorModelo).trim().toLowerCase()) {
    return false;
  }
  return true;
}

function acharKpi(kpis, termos) {
  if (!Array.isArray(kpis)) return null;
  const low = termos.map((t) => t.toLowerCase());
  for (const item of kpis) {
    if (!item || typeof item !== 'object') continue;
    const label = String(item.label || '').toLowerCase();
    if (low.every((t) => label.includes(t))) return item;
  }
  return null;
}

function validarPesquisa(dados, schema) {
  const erros = [];
  const kpis = dados.kpis;
  const kpisModelo = (schema && schema.kpis) || [];

  function modeloValor(termos) {
    const item = acharKpi(kpisModelo, termos);
    return item ? item.valor : null;
  }

  // 1. Tamanho do Mercado
  const tm = acharKpi(kpis || [], ['tamanho', 'mercado']);
  if (!tm) {
    erros.push('KPI obrigatorio ausente: "Tamanho do Mercado".');
  } else if (!valorReal(tm.valor, modeloValor(['tamanho', 'mercado']))) {
    erros.push(
      `KPI "Tamanho do Mercado" sem valor real (recebido: ${JSON.stringify(
        tm.valor
      )}). Preencha com o dado concreto da pesquisa.`
    );
  }

  // 2. Crescimento Anual
  const ca = acharKpi(kpis || [], ['crescimento']);
  if (!ca) {
    erros.push('KPI obrigatorio ausente: "Crescimento Anual".');
  } else if (!valorReal(ca.valor, modeloValor(['crescimento']))) {
    erros.push(
      `KPI "Crescimento Anual" sem valor real (recebido: ${JSON.stringify(
        ca.valor
      )}). Preencha com o dado concreto da pesquisa.`
    );
  }

  // 3. Top 5 concorrentes
  const concs = dados.concorrentes;
  if (!Array.isArray(concs) || concs.length < MIN_CONCORRENTES) {
    const qtd = Array.isArray(concs) ? concs.length : 0;
    erros.push(
      `Lista de concorrentes incompleta: ${qtd} encontrados, minimo ${MIN_CONCORRENTES}.`
    );
  } else {
    const modeloC =
      (schema && Array.isArray(schema.concorrentes) && schema.concorrentes[0]) ||
      {};
    concs.forEach((c, i) => {
      const n = i + 1;
      if (!c || typeof c !== 'object') {
        erros.push(`Concorrente ${n}: formato invalido.`);
        return;
      }
      if (!valorReal(c.nome, modeloC.nome)) {
        erros.push(`Concorrente ${n}: campo "nome" vazio ou modelo.`);
      }
      if (!valorReal(c.promessa, modeloC.promessa)) {
        erros.push(`Concorrente ${n}: campo "promessa" vazio ou modelo.`);
      }
    });
  }

  return erros;
}

function fail(erros) {
  process.stderr.write(
    '[painel-validar] pesquisa.json reprovado. Corrija antes de montar o painel:\n'
  );
  for (const e of erros) {
    process.stderr.write(`  . ${e}\n`);
  }
  // Exit 2 sinaliza bloqueio ao Claude Code (PostToolUse convention).
  process.exit(2);
}
