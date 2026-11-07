#!/usr/bin/env node
// SessionStart hook: liga a pasta meus-produtos/ de uma worktree à pasta de
// produtos do checkout principal, para a sessão enxergar os produtos do aluno.
//
// Por que existe: o Claude desktop abre cada sessão numa worktree nova, em
// <repo>/.claude/worktrees/<nome>/ (o Codex também trabalha em worktrees). A
// pasta meus-produtos/ fica fora do git, então a worktree nasce sem ela: a
// sessão não acha o produto ativo e o que for criado ali some quando a worktree
// é removida.
//
// O que faz, só numa worktree vinculada (git-dir diferente do git-common-dir):
//   1. acha o checkout principal (a pasta que contém o .git comum);
//   2. cria <principal>/meus-produtos se ainda não existir;
//   3. cria <worktree>/meus-produtos como atalho (symlink) para ela, quando
//      não há nada nesse caminho;
//   4. avisa o modelo de que a pasta é um atalho (additionalContext).
//
// Permissão: o Claude Code confere para onde o atalho leva, e a pasta do
// checkout principal fica fora da worktree. Se ela não estiver entre as pastas
// liberadas da sessão, ler e gravar em meus-produtos/ pede permissão ao aluno.
// O hook não mexe em permissão nenhuma; o aviso ao modelo explica o pedido.
//
// No checkout principal não faz nada. Nunca apaga nem sobrescreve: se a
// worktree já tem uma pasta meus-produtos de verdade, ou um atalho para outro
// lugar, só avisa.
//
// Windows: symlink de pasta, que pede o Modo de Desenvolvedor (ou rodar como
// administrador). Junction não serve, apesar de dispensar o administrador: o
// `git worktree remove` do Git para Windows entra na junction e apaga o
// conteúdo da pasta de destino, ou seja, os produtos do aluno. Sem o Modo de
// Desenvolvedor, o hook só avisa.
//
// Numa sessão em worktree do Claude desktop, o Claude Code lê os hooks do
// .claude/settings.json do checkout principal: este hook só passa a valer
// depois que o checkout principal estiver atualizado com ele.
//
// Qualquer erro termina com exit 0: o hook nunca trava a sessão.

'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const PASTA = 'meus-produtos';
const WINDOWS = process.platform === 'win32';

// A pasta da sessão vem no campo cwd da entrada. Não dá para usar o diretório
// atual do processo: numa sessão em worktree do Claude desktop, os hooks rodam
// na raiz do checkout principal.
lerEntrada((evento) => {
  const pastaDaSessao = (evento && typeof evento.cwd === 'string' && evento.cwd) || process.cwd();
  try {
    ligar(pastaDaSessao);
  } catch (e) {
    avisar(
      `Não deu para ligar a pasta ${PASTA} desta sessão à pasta principal (${e.code || e.message}).`,
      `Aviso do hook worktree-meus-produtos: não deu para ligar ${PASTA}/ ao checkout principal ` +
        `(${e.code || e.message}). Se ${PASTA}/ não existir aqui, avise o aluno antes de criar produto: ` +
        'o que for gravado nesta worktree se perde quando ela for removida.'
    );
  }
  process.exitCode = 0;
});

function lerEntrada(seguir) {
  if (process.stdin.isTTY) return seguir({}); // Rodado à mão no terminal.
  let dados = '';
  let feito = false;
  const fim = () => {
    if (feito) return;
    feito = true;
    process.stdin.destroy();
    let evento = {};
    try {
      evento = JSON.parse(dados || '{}');
    } catch (e) {
      // Entrada inválida: segue com o diretório atual.
    }
    seguir(evento);
  };
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (parte) => (dados += parte));
  process.stdin.on('end', fim);
  process.stdin.on('error', fim);
  setTimeout(fim, 3000).unref(); // Quem chamou não fechou a entrada: segue assim mesmo.
}

function ligar(pastaDaSessao) {
  let topo;
  let gitDir;
  let comum;
  try {
    topo = path.resolve(git(pastaDaSessao, ['rev-parse', '--show-toplevel']));
    [gitDir, comum] = git(topo, ['rev-parse', '--git-dir', '--git-common-dir'])
      .split(/\r?\n/)
      .map((p) => path.resolve(topo, p));
  } catch (e) {
    return; // Fora de um repositório git (ou sem git instalado): nada a fazer.
  }
  if (!gitDir || !comum) return;
  if (mesmoCaminho(real(gitDir) || gitDir, real(comum) || comum)) return; // Checkout principal.
  // O git trata a pasta que contém o .git comum como checkout principal. Em
  // layout incomum (repositório como submódulo, --separate-git-dir) não há
  // checkout principal claro: melhor não criar pasta em lugar errado.
  if (path.basename(comum).toLowerCase() !== '.git') return;

  const alvo = path.join(path.dirname(comum), PASTA);
  const atalho = path.join(topo, PASTA);

  if (!lstatOuNulo(alvo)) fs.mkdirSync(alvo, { recursive: true });
  const pastaAlvo = statOuNulo(alvo);
  if (!pastaAlvo || !pastaAlvo.isDirectory()) {
    avisar(
      `Não deu para ligar ${PASTA}: ${alvo} existe e não é uma pasta.`,
      `Aviso do hook worktree-meus-produtos: ${alvo} existe e não é uma pasta, então ${PASTA}/ desta ` +
        'worktree não foi ligada ao checkout principal. Avise o aluno antes de criar ou alterar produto.'
    );
    return;
  }

  let info = lstatOuNulo(atalho);
  if (!info) {
    try {
      fs.symlinkSync(alvo, atalho, 'dir'); // O tipo só vale no Windows.
    } catch (e) {
      if (WINDOWS && (e.code === 'EPERM' || e.code === 'EACCES')) {
        avisar(
          `Os produtos ficam em ${alvo} e esta sessão está numa cópia do projeto (worktree). Para ela ` +
            'enxergar os produtos, o Windows precisa do Modo de Desenvolvedor: abra Configurações, ' +
            'procure "Para desenvolvedores", ative o Modo de Desenvolvedor e comece uma nova sessão.',
          `Aviso do hook worktree-meus-produtos: o Windows não deixou criar o atalho ${PASTA}/ desta ` +
            `worktree para ${alvo} (falta o Modo de Desenvolvedor). Não crie produto aqui: o que for ` +
            `gravado em ${PASTA}/ nesta worktree se perde quando ela for removida. Oriente o aluno a ativar ` +
            'o Modo de Desenvolvedor (Configurações, "Para desenvolvedores") e começar uma nova sessão.'
        );
        return;
      }
      if (e.code !== 'EEXIST') throw e;
      // Outra sessão criou o atalho ao mesmo tempo: confere o que ficou lá.
    }
    info = lstatOuNulo(atalho);
  }

  if (info && info.isSymbolicLink()) {
    const destino = real(atalho);
    if (destino && mesmoCaminho(destino, real(alvo))) {
      contexto(
        `Esta sessão roda numa worktree. A pasta ${PASTA}/ daqui é um atalho para ${alvo} (a pasta ` +
          `de produtos do checkout principal): o que for lido ou gravado em ${PASTA}/ fica lá e não se ` +
          'perde quando a worktree for removida. Em comandos de terminal que não seguem atalho (find, ' +
          `ls -l, grep -r), escreva o caminho com a barra no fim: ${PASTA}/. Não apague o atalho. Se o ` +
          `Claude Code pedir permissão para ler ou gravar em ${PASTA}/ (o destino do atalho fica fora da ` +
          'worktree), explique ao aluno que é a pasta de produtos dele e peça para permitir nesta sessão.'
      );
      return;
    }
    const aponta = destino || lerAtalho(atalho);
    avisar(
      `A pasta ${PASTA} desta sessão é um atalho para ${aponta}, não para a pasta principal ` +
        `(${alvo}). Nada foi alterado.`,
      `Aviso do hook worktree-meus-produtos: ${atalho} é um atalho para ${aponta}, não para a pasta ` +
        `de produtos do checkout principal (${alvo}). O hook não mexeu nele. Avise o aluno antes de ` +
        'criar ou alterar produto.'
    );
    return;
  }

  if (info && info.isDirectory()) {
    avisar(
      `Esta sessão está numa cópia do projeto (worktree) que já tem uma pasta ${PASTA} própria, ` +
        `separada da pasta principal (${alvo}). Os produtos da pasta principal não aparecem aqui, e o ` +
        'que for criado nesta cópia se perde quando ela for removida. Nada foi apagado.',
      `Aviso do hook worktree-meus-produtos: ${atalho} é uma pasta de verdade, separada da pasta de ` +
        `produtos do checkout principal (${alvo}). O hook não mexeu nela. Antes de criar ou alterar ` +
        'produto, avise o aluno: o que ficar nesta pasta se perde quando a worktree for removida. Para ' +
        `unir, com o aluno de acordo, mova o conteúdo para ${alvo} e apague a pasta vazia daqui; o ` +
        'atalho é criado na próxima sessão.'
    );
    return;
  }

  avisar(
    `Não deu para ligar ${PASTA}: ${atalho} já existe e não é uma pasta.`,
    `Aviso do hook worktree-meus-produtos: ${atalho} já existe e não é uma pasta nem um atalho, então ` +
      `não foi ligado ao checkout principal (${alvo}). Avise o aluno antes de criar ou alterar produto.`
  );
}

function git(cwd, args) {
  return execFileSync('git', args, {
    cwd,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'ignore'],
    windowsHide: true,
    timeout: 5000,
  }).trim();
}

function lstatOuNulo(caminho) {
  try {
    return fs.lstatSync(caminho);
  } catch (e) {
    if (e.code === 'ENOENT') return null;
    throw e;
  }
}

function statOuNulo(caminho) {
  try {
    return fs.statSync(caminho);
  } catch (e) {
    return null; // Atalho quebrado ou sem permissão.
  }
}

function real(caminho) {
  try {
    return fs.realpathSync.native(caminho);
  } catch (e) {
    return null;
  }
}

function lerAtalho(caminho) {
  try {
    return fs.readlinkSync(caminho);
  } catch (e) {
    return 'um caminho que não existe';
  }
}

// Windows e Mac costumam ter disco que não diferencia maiúsculas.
function mesmoCaminho(a, b) {
  if (!a || !b) return false;
  return WINDOWS || process.platform === 'darwin' ? a.toLowerCase() === b.toLowerCase() : a === b;
}

function contexto(texto) {
  responder({ hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: texto } });
}

// systemMessage aparece para o aluno; additionalContext vai só para o modelo.
function avisar(paraAluno, paraModelo) {
  responder({
    systemMessage: paraAluno,
    hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: paraModelo },
  });
}

function responder(saida) {
  process.stdout.write(JSON.stringify(saida) + '\n');
}
