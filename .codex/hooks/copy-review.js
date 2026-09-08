#!/usr/bin/env node
// PostToolUse hook: revisa copy em arquivos .md de conteudo-social/
// Verifica: travessao, ponto de exclamacao, estrutura "Nao e X. E Y.",
//           "sem precisar", "mesmo que", pergunta no GANCHO, palavra duplicada.
// Nao bloqueia (exit 0 sempre). Reporta no stdout para o Claude ver.

const path = require('path');

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

    const filePath = (params.file_path || '').replace(/\\/g, '/');

    // Alvos de revisao:
    // 1. .md em conteudo-social/, anuncios/, emails/ ou copy-pagina/ (copy gerada)
    // 2. perfil.md, idconsumidor.md e pesquisa-mercado.md em meus-produtos/{slug}/
    //    (fontes do painel de entregas)
    const isCopy = /\/(conteudo-social|anuncios|emails|copy-pagina)\//.test(filePath);
    const isPainelFonte = /\/meus-produtos\/[^/]+\/(perfil|idconsumidor|pesquisa-mercado)\.md$/.test(filePath);
    const isMd = filePath.endsWith('.md');
    if ((!isCopy && !isPainelFonte) || !isMd) {
      process.exit(0);
    }

    const content = params.content || params.new_string || '';
    if (!content || typeof content !== 'string') process.exit(0);

    const lines = content.split(/\r?\n/);
    const issues = [];

    // 1. Travessao
    lines.forEach((line, i) => {
      if (line.includes('\u2014')) {
        issues.push(`[ERRO] L${i+1}: travessao — "${line.trim().slice(0, 70)}"`);
      }
    });

    // 2. Ponto de exclamacao
    lines.forEach((line, i) => {
      if (line.includes('!')) {
        issues.push(`[ERRO] L${i+1}: ponto de exclamacao — "${line.trim().slice(0, 70)}"`);
      }
    });

    // 3. Estrutura "Nao e X. E Y." / "Nao foi X. Foi Y."
    const naoERegex = /\bNao (e|foi|era|sao|eram|sou|somos)\b[^.\n]{0,100}\.\s+\b(E|Foi|Era|Sao|Eram|Sou|Somos)\b/g;
    let m;
    while ((m = naoERegex.exec(content)) !== null) {
      const lineNum = content.substring(0, m.index).split('\n').length;
      issues.push(`[ERRO] L~${lineNum}: "Nao e X. E Y." — "${m[0].slice(0, 70)}"`);
    }

    // 4. "sem precisar" e "mesmo que"
    lines.forEach((line, i) => {
      if (/sem precisar/i.test(line)) {
        issues.push(`[ERRO] L${i+1}: "sem precisar" proibido — "${line.trim().slice(0, 70)}"`);
      }
      if (/mesmo que/i.test(line)) {
        issues.push(`[AVISO] L${i+1}: "mesmo que" como muleta — "${line.trim().slice(0, 70)}"`);
      }
    });

    // 5. Pergunta no GANCHO (linhas seguintes ao marcador [0-3s])
    lines.forEach((line, i) => {
      if (/\[0-3s\]\s+GANCHO/i.test(line)) {
        for (let j = i + 1; j <= Math.min(i + 3, lines.length - 1); j++) {
          if (lines[j].includes('?')) {
            issues.push(`[ERRO] L${j+1}: pergunta no GANCHO — "${lines[j].trim().slice(0, 70)}"`);
            break;
          }
        }
      }
    });

    // 6. Palavras duplicadas acidentais (ex: "que que", "de de")
    const dupeRegex = /\b(\w{3,})\s+\1\b/gi;
    while ((m = dupeRegex.exec(content)) !== null) {
      const lineNum = content.substring(0, m.index).split('\n').length;
      issues.push(`[AVISO] L~${lineNum}: palavra duplicada — "${m[0]}"`);
    }

    // 7. Erros de digitacao comuns em copy
    const typos = [
      [/\bvoce\b(?!\s+(?:nao|pode|vai|tem|quer|e\b|ja|ainda))/g, null], // nao e um erro, so checamos padroes abaixo
      [/\bq\b/g, '"q" sozinho (deve ser "que")'],
      [/\bp\b(?!\s*\.)/g, '"p" sozinho (deve ser "para" ou "por")'],
      [/  +/g, 'espaco duplo'],
      [/[.,;:]\s*\n\s*\n/g, 'pontuacao antes de linha em branco dupla'],
    ];
    typos.forEach(([regex, label]) => {
      if (!label) return;
      let match;
      regex.lastIndex = 0;
      while ((match = regex.exec(content)) !== null) {
        const lineNum = content.substring(0, match.index).split('\n').length;
        issues.push(`[AVISO] L~${lineNum}: ${label} — "${match[0].trim().slice(0, 40)}"`);
      }
    });

    // 8. Palavras sem acento (pt_BR)
    // ERROS claros: forma sem acento quase nunca e valida em texto corrido
    const acentoErros = [
      [/\bnao\b/gi,        'nao -> nao'],
      [/\btambem\b/gi,     'tambem -> tambem'],
      [/\btres\b/gi,       'tres -> tres'],
      [/\bestrategia\b/gi, 'estrategia -> estrategia'],
      [/\bestrategias\b/gi,'estrategias -> estrategias'],
      [/\bduvida\b/gi,     'duvida -> duvida'],
      [/\bduvidas\b/gi,    'duvidas -> duvidas'],
      [/\bintroducao\b/gi, 'introducao -> introducao'],
      [/\bconclusao\b/gi,  'conclusao -> conclusao'],
      [/\bmetodo\b/gi,     'metodo -> metodo'],
      [/\bmetodos\b/gi,    'metodos -> metodos'],
      [/\banalise\b/gi,    'analise -> analise'],
      [/\banalises\b/gi,   'analises -> analises'],
      [/\bespecifico\b/gi, 'especifico -> especifico'],
      [/\bespecifica\b/gi, 'especifica -> especifica'],
      [/\bbasico\b/gi,     'basico -> basico'],
      [/\bbasica\b/gi,     'basica -> basica'],
      [/\bunico\b/gi,      'unico -> unico'],
      [/\bunica\b/gi,      'unica -> unica'],
      [/\bnumero\b/gi,     'numero -> numero'],
      [/\bnumeros\b/gi,    'numeros -> numeros'],
      [/\bcodigo\b/gi,     'codigo -> codigo'],
      [/\bcodigos\b/gi,    'codigos -> codigos'],
      [/\bpagina\b/gi,     'pagina -> pagina'],
      [/\bpaginas\b/gi,    'paginas -> paginas'],
      [/\bvideo\b/gi,      'video -> video'],
      [/\bvideos\b/gi,     'videos -> videos'],
      [/\bhistoria\b/gi,   'historia -> historia'],
      [/\bhistorias\b/gi,  'historias -> historias'],
      [/\bmemoria\b/gi,    'memoria -> memoria'],
      [/\bmemoriais\b/gi,  'memorias -> memorias'],
      [/\btecnica\b/gi,    'tecnica -> tecnica'],
      [/\btecnicas\b/gi,   'tecnicas -> tecnicas'],
      [/\bproximo\b/gi,    'proximo -> proximo'],
      [/\bproxima\b/gi,    'proxima -> proxima'],
      [/\bultimo\b/gi,     'ultimo -> ultimo'],
      [/\bultima\b/gi,     'ultima -> ultima'],
      [/\bpossivel\b/gi,   'possivel -> possivel'],
      [/\bimpossivel\b/gi, 'impossivel -> impossivel'],
      [/\bautomatico\b/gi, 'automatico -> automatico'],
      [/\binicio\b/gi,     'inicio -> inicio'],
      [/\bsessao\b/gi,     'sessao -> sessao'],
      [/\bdecisao\b/gi,    'decisao -> decisao'],
      [/\bopcao\b/gi,      'opcao -> opcao'],
      [/\bopcoes\b/gi,     'opcoes -> opcoes'],
      [/\bfuncao\b/gi,     'funcao -> funcao'],
      [/\bfuncoes\b/gi,    'funcoes -> funcoes'],
      [/\bacao\b/gi,       'acao -> acao'],
      [/\bacoes\b/gi,      'acoes -> acoes'],
      [/\breacao\b/gi,     'reacao -> reacao'],
      [/\bsolucao\b/gi,    'solucao -> solucao'],
      [/\bsolucoes\b/gi,   'solucoes -> solucoes'],
      [/\bsituacao\b/gi,   'situacao -> situacao'],
      [/\bvoce\b/gi,       'voce -> voce'],
      [/\bvoces\b/gi,      'voces -> voces'],
      [/\bestao\b/gi,      'estao -> estao'],
    ];
    // AVISOS ambiguos: forma sem acento pode ser valida em certos contextos
    const acentoAvisos = [
      [/\besta\b/gi,  'esta (verificar: esta = demonstrativo ou esta = verbo estar?)'],
      [/\bsao\b/gi,   'sao (verificar: sao = adjetivo ou Sao Paulo / sao = verbo ser?)'],
      [/\bindice\b/gi,'indice (verificar: indice ou indice = sem acento em slug?)'],
      [/\bfacil\b/gi, 'facil -> facil'],
    ];

    acentoErros.forEach(([regex, label]) => {
      let match2;
      regex.lastIndex = 0;
      while ((match2 = regex.exec(content)) !== null) {
        const lineNum = content.substring(0, match2.index).split('\n').length;
        const palavra = label.split(' -> ')[0];
        const correta = label.split(' -> ')[1];
        issues.push(`[ERRO] L~${lineNum}: palavra sem acento "${match2[0]}" (use "${correta}") — "${lines[lineNum - 1] ? lines[lineNum - 1].trim().slice(0, 60) : ''}"`);
      }
    });

    acentoAvisos.forEach(([regex, label]) => {
      let match3;
      regex.lastIndex = 0;
      while ((match3 = regex.exec(content)) !== null) {
        const lineNum = content.substring(0, match3.index).split('\n').length;
        issues.push(`[AVISO] L~${lineNum}: ${label} — "${lines[lineNum - 1] ? lines[lineNum - 1].trim().slice(0, 60) : ''}"`);
      }
    });

    // Relatorio
    const fileName = path.basename(filePath);
    if (issues.length === 0) {
      console.log(`COPY OK: ${fileName} — nenhum problema detectado.`);
    } else {
      const erros = issues.filter(x => x.startsWith('[ERRO]')).length;
      const avisos = issues.filter(x => x.startsWith('[AVISO]')).length;
      console.log(`REVISAO COPY: ${fileName}`);
      console.log(`${erros} erro(s), ${avisos} aviso(s):\n`);
      issues.slice(0, 12).forEach(issue => console.log('  ' + issue));
      if (issues.length > 12) {
        console.log(`  ... e mais ${issues.length - 12} ocorrencia(s).`);
      }
    }

    process.exit(0);
  } catch (_) {
    process.exit(0);
  }
});
