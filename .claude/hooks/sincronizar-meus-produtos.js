#!/usr/bin/env node
// Hook de SessionStart e Stop: mantém a pasta meus-produtos/ igual no checkout
// principal e em todas as worktrees do repositório.
//
// Por que existe: o Claude desktop abre cada sessão numa worktree nova, em
// <repo>/.claude/worktrees/<nome>/. A pasta meus-produtos/ fica fora do git,
// então a worktree nasce sem ela: a sessão não acha o produto ativo, e o que
// for criado ali some quando a worktree é removida. Um atalho (symlink) para a
// pasta principal resolveria, mas no Windows ele pede o Modo de Desenvolvedor,
// que quase nenhum aluno tem ligado. Por isso o hook copia.
//
// Como funciona:
//   - A pasta meus-produtos/ do checkout principal é a central.
//   - A cada execução (início de sessão e fim de cada resposta), cada worktree
//     é sincronizada com a central nos dois sentidos. Assim, o que muda numa
//     pasta chega a todas as outras.
//   - Arquivo que mudou dos dois lados: fica a versão mais recente.
//   - Arquivo apagado de um lado: a cópia do outro lado vai para
//     meus-produtos/.lixeira/<data>/ na central, nunca é apagada de vez. Para
//     saber o que foi apagado (e não apenas é novo do outro lado), o hook
//     guarda em meus-produtos/.sincronizacao/ o retrato da última sincronização
//     de cada worktree.
//   - meus-produtos/.ativo (o produto ativo) não é sincronizado: cada sessão
//     pode trabalhar num produto diferente. Uma worktree sem .ativo recebe o
//     da central.
//
// Qualquer erro termina com exit 0: o hook nunca trava a sessão.

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');

const PASTA = 'meus-produtos';
const LIXEIRA = '.lixeira';
const CONTROLE = '.sincronizacao';
const ATIVO = '.ativo';
const NAO_SINCRONIZAR = new Set([LIXEIRA, CONTROLE, ATIVO]);
const TOLERANCIA_MS = 2000; // Diferença de data que ainda conta como o mesmo arquivo.
const TRAVA_VENCIDA_MS = 60000;

lerEntrada((evento) => {
  const pastaDaSessao = (evento && typeof evento.cwd === 'string' && evento.cwd) || process.cwd();
  const inicio = evento && evento.hook_event_name === 'SessionStart';
  try {
    const resultado = sincronizarTudo(pastaDaSessao);
    if (inicio && resultado && resultado.sessaoEmWorktree) {
      contexto(
        `Esta sessão roda numa worktree. A pasta ${PASTA}/ daqui é uma cópia sincronizada ` +
          `automaticamente com a pasta de produtos do checkout principal (${resultado.central}) e com ` +
          'as outras worktrees, no início da sessão e ao fim de cada resposta. Pode ler e gravar ' +
          `normalmente em ${PASTA}/. Arquivo apagado aqui vai para ${PASTA}/${LIXEIRA}/ na pasta principal.`
      );
    }
  } catch (e) {
    if (inicio) {
      contexto(
        `Aviso do hook sincronizar-meus-produtos: a sincronização de ${PASTA}/ falhou ` +
          `(${e.code || e.message}). Se esta sessão estiver numa worktree, avise o aluno antes de ` +
          'criar produto: o que for gravado aqui pode não chegar à pasta principal.'
      );
    }
  }
  process.exitCode = 0;
});

function sincronizarTudo(pastaDaSessao) {
  let comum;
  try {
    const topo = git(pastaDaSessao, ['rev-parse', '--show-toplevel']);
    comum = path.resolve(topo, git(topo, ['rev-parse', '--git-common-dir']));
  } catch (e) {
    return null; // Fora de um repositório git (ou sem git): nada a fazer.
  }
  // Em layout incomum (submódulo, --separate-git-dir) não há checkout principal claro.
  if (path.basename(comum).toLowerCase() !== '.git') return null;
  const principal = path.dirname(comum);
  const central = path.join(principal, PASTA);

  const worktrees = listarWorktrees(principal).filter((w) => !mesmoCaminho(w, principal));
  const topoDaSessao = git(pastaDaSessao, ['rev-parse', '--show-toplevel']);
  const sessaoEmWorktree = !mesmoCaminho(topoDaSessao, principal);
  if (!worktrees.length) return { central, sessaoEmWorktree };

  fs.mkdirSync(path.join(central, CONTROLE), { recursive: true });
  const trava = travar(path.join(central, CONTROLE, 'trava'));
  if (!trava) return { central, sessaoEmWorktree }; // Outra sessão está sincronizando agora.
  try {
    const locais = [];
    for (const worktree of worktrees) {
      const local = path.join(worktree, PASTA);
      const info = lstatOuNulo(local);
      if (info && info.isSymbolicLink()) continue; // Atalho: já é a mesma pasta.
      if (info && !info.isDirectory()) continue;
      locais.push(local);
    }
    // Duas voltas: a primeira junta tudo na central, a segunda espalha para todas.
    for (let volta = 0; volta < 2; volta++) for (const local of locais) sincronizarPar(local, central);
    limparRetratosAntigos(central, locais);
  } finally {
    destravar(trava);
  }
  return { central, sessaoEmWorktree };
}

// Sincroniza uma worktree (local) com a central, nos dois sentidos.
function sincronizarPar(local, central) {
  fs.mkdirSync(local, { recursive: true });
  const arquivoRetrato = path.join(central, CONTROLE, `${idDaPasta(local)}.json`);
  const retrato = lerJson(arquivoRetrato);
  const daLocal = listar(local);
  const daCentral = listar(central);
  const caminhos = new Set([...daLocal.keys(), ...daCentral.keys(), ...Object.keys(retrato)]);
  const carimbo = new Date().toISOString().replace(/[:.]/g, '-');

  for (const rel of caminhos) {
    const l = daLocal.get(rel);
    const c = daCentral.get(rel);
    const antes = retrato[rel];
    const origemLocal = path.join(local, rel);
    const origemCentral = path.join(central, rel);

    if (l && c) {
      if (igual(l, c)) continue;
      if (l.mtimeMs > c.mtimeMs) copiar(origemLocal, origemCentral);
      else copiar(origemCentral, origemLocal);
    } else if (l && !c) {
      // Já esteve nas duas e saiu da central sem mudar aqui depois: foi apagado lá.
      if (antes && igual(l, antes)) paraLixeira(origemLocal, central, carimbo, rel);
      else copiar(origemLocal, origemCentral);
    } else if (!l && c) {
      if (antes && igual(c, antes)) paraLixeira(origemCentral, central, carimbo, rel);
      else copiar(origemCentral, origemLocal);
    }
  }

  // A worktree sem produto ativo recebe o da central.
  const ativoCentral = path.join(central, ATIVO);
  const ativoLocal = path.join(local, ATIVO);
  if (!lstatOuNulo(ativoLocal) && lstatOuNulo(ativoCentral)) copiar(ativoCentral, ativoLocal);

  removerPastasVazias(local);
  removerPastasVazias(central);

  // Retrato do que ficou igual nos dois lados, para a próxima vez.
  const novo = {};
  for (const [rel, info] of listar(local)) novo[rel] = { size: info.size, mtimeMs: info.mtimeMs };
  fs.writeFileSync(arquivoRetrato, JSON.stringify({ pasta: local, arquivos: novo }, null, 1));
}

function listar(raiz) {
  const mapa = new Map();
  const visitar = (pasta, prefixo) => {
    let itens;
    try {
      itens = fs.readdirSync(pasta, { withFileTypes: true });
    } catch (e) {
      return;
    }
    for (const item of itens) {
      if (!prefixo && NAO_SINCRONIZAR.has(item.name)) continue;
      const rel = prefixo ? `${prefixo}/${item.name}` : item.name;
      const completo = path.join(pasta, item.name);
      if (item.isSymbolicLink()) continue; // Não segue atalhos.
      if (item.isDirectory()) visitar(completo, rel);
      else if (item.isFile()) {
        const info = fs.statSync(completo);
        mapa.set(rel, { size: info.size, mtimeMs: info.mtimeMs });
      }
    }
  };
  visitar(raiz, '');
  return mapa;
}

function igual(a, b) {
  return a.size === b.size && Math.abs(a.mtimeMs - b.mtimeMs) < TOLERANCIA_MS;
}

function copiar(de, para) {
  fs.mkdirSync(path.dirname(para), { recursive: true });
  const temporario = `${para}.sincronizando`;
  fs.copyFileSync(de, temporario);
  const info = fs.statSync(de);
  fs.utimesSync(temporario, info.atime, info.mtime); // Mesma data dos dois lados.
  fs.renameSync(temporario, para);
}

function paraLixeira(arquivo, central, carimbo, rel) {
  // Se a mesma versão já está na lixeira (apagada a partir de outra pasta), só remove.
  const info = fs.statSync(arquivo);
  if (jaNaLixeira(central, rel, info)) {
    fs.unlinkSync(arquivo);
    return;
  }
  const destino = path.join(central, LIXEIRA, carimbo, rel);
  fs.mkdirSync(path.dirname(destino), { recursive: true });
  try {
    fs.renameSync(arquivo, destino);
  } catch (e) {
    // Discos diferentes: copia e depois apaga.
    fs.copyFileSync(arquivo, destino);
    fs.unlinkSync(arquivo);
  }
}

function jaNaLixeira(central, rel, info) {
  let datas;
  try {
    datas = fs.readdirSync(path.join(central, LIXEIRA));
  } catch (e) {
    return false;
  }
  return datas.some((data) => {
    const copia = statOuNulo(path.join(central, LIXEIRA, data, rel));
    return copia && copia.isFile() && igual(copia, info);
  });
}

// Apaga o retrato de worktrees que não existem mais.
function limparRetratosAntigos(central, locais) {
  const validos = new Set(locais.map((l) => `${idDaPasta(l)}.json`));
  const pasta = path.join(central, CONTROLE);
  for (const nome of fs.readdirSync(pasta)) {
    if (nome.endsWith('.json') && !validos.has(nome)) fs.unlinkSync(path.join(pasta, nome));
  }
}

function removerPastasVazias(raiz) {
  const visitar = (pasta, ehRaiz) => {
    let itens;
    try {
      itens = fs.readdirSync(pasta, { withFileTypes: true });
    } catch (e) {
      return;
    }
    for (const item of itens) {
      if (ehRaiz && NAO_SINCRONIZAR.has(item.name)) continue;
      if (item.isDirectory() && !item.isSymbolicLink()) visitar(path.join(pasta, item.name), false);
    }
    if (!ehRaiz && fs.readdirSync(pasta).length === 0) fs.rmdirSync(pasta);
  };
  visitar(raiz, true);
}

function listarWorktrees(principal) {
  const saida = git(principal, ['worktree', 'list', '--porcelain']);
  const pastas = [];
  for (const bloco of saida.split(/\r?\n\r?\n/)) {
    const linhas = bloco.split(/\r?\n/);
    const linha = linhas.find((l) => l.startsWith('worktree '));
    if (!linha || linhas.includes('bare') || linhas.some((l) => l.startsWith('prunable'))) continue;
    const pasta = path.resolve(linha.slice('worktree '.length));
    if (statOuNulo(pasta)) pastas.push(pasta);
  }
  return pastas;
}

function idDaPasta(pasta) {
  const normal = process.platform === 'win32' || process.platform === 'darwin' ? pasta.toLowerCase() : pasta;
  return crypto.createHash('sha1').update(normal).digest('hex').slice(0, 16);
}

function lerJson(arquivo) {
  try {
    return JSON.parse(fs.readFileSync(arquivo, 'utf8')).arquivos || {};
  } catch (e) {
    return {};
  }
}

function travar(arquivo) {
  try {
    return fs.openSync(arquivo, 'wx') && arquivo;
  } catch (e) {
    const info = statOuNulo(arquivo);
    if (info && Date.now() - info.mtimeMs > TRAVA_VENCIDA_MS) {
      try {
        fs.unlinkSync(arquivo);
        return fs.openSync(arquivo, 'wx') && arquivo;
      } catch (e2) {
        return null;
      }
    }
    return null;
  }
}

function destravar(arquivo) {
  try {
    fs.unlinkSync(arquivo);
  } catch (e) {
    // Já foi removida.
  }
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
    return null;
  }
}

function statOuNulo(caminho) {
  try {
    return fs.statSync(caminho);
  } catch (e) {
    return null;
  }
}

// Windows e Mac costumam ter disco que não diferencia maiúsculas.
function mesmoCaminho(a, b) {
  const pa = path.resolve(a);
  const pb = path.resolve(b);
  return process.platform === 'win32' || process.platform === 'darwin'
    ? pa.toLowerCase() === pb.toLowerCase()
    : pa === pb;
}

function contexto(texto) {
  process.stdout.write(
    JSON.stringify({ hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: texto } }) + '\n'
  );
}

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
