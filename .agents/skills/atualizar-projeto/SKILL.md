---
name: atualizar-projeto
description: Atualiza o projeto Fluxo Criativo com as últimas mudanças do repositório git de forma segura. Faz fetch, compara a branch local com o GitHub, guarda alterações locais em stash, aplica o pull e conduz resolução guiada de conflitos sem usar comandos destrutivos. Use quando o usuário pedir para "atualizar o projeto", "baixar as últimas mudanças", "sincronizar com o GitHub" ou "pegar a versão mais nova".
---

# Atualizar Projeto (Fluxo Criativo)

Atualiza o projeto Fluxo Criativo com as últimas mudanças do repositório.
Siga exatamente este passo a passo, sem pular nenhuma etapa e sem pedir confirmação.

## Passo a passo

1. Confirme que está dentro de um repositório git rodando:
   `git rev-parse --is-inside-work-tree`

2. Verifique se você está no repositório principal e não numa cópia paralela (worktree):
   `git rev-parse --git-dir`
   `git rev-parse --git-common-dir`
   - Se os dois caminhos forem IGUAIS: prossiga para o passo 3.
   - Se forem DIFERENTES: pare imediatamente e responda ao usuário com a mensagem abaixo, SEM executar mais nenhum comando:
     "Notei que essa conversa está rodando numa cópia paralela do projeto (worktree). Pra atualizar do jeito certo, faça o seguinte:
     1. Abra o menu de configurações do Claude Code aqui da conversa.
     2. Procure a opção de 'worktree' (pode aparecer como 'isolation: worktree' ou 'rodar em worktree separado').
     3. Desmarque ou desligue essa opção.
     4. Feche essa conversa e abra uma nova.
     5. Cole esse mesmo comando de novo.
     Assim a atualização vai chegar direto na pasta principal do Fluxo Criativo, do jeito que precisa."

3. Confirme que você está dentro do projeto certo (Fluxo Criativo):
   `git remote get-url origin`
   - Se o endereço retornado CONTIVER o texto "fluxo_criativo": prossiga para o passo 4.
   - Se NÃO contiver, ou se o comando der erro: pare imediatamente e responda, SEM executar mais nenhum comando:
     "Essa conversa parece estar aberta num projeto diferente do Fluxo Criativo. Pra atualizar do jeito certo, abra a pasta do Fluxo Criativo no Claude Code e cole esse mesmo comando lá dentro. Se não souber qual pasta é, me chama que eu te ajudo a achar."

4. Descubra o nome da branch atual e guarde esse nome para usar nos próximos passos:
   `git rev-parse --abbrev-ref HEAD`

5. Guarde o commit atual antes de qualquer mudança:
   `git rev-parse HEAD`

6. Busque as atualizações do repositório remoto:
   `git fetch --all --prune`
   - Se o comando der erro (sem internet ou sem acesso ao repositório): pule para o passo 14 (mensagem de erro).

7. Compare o commit local com o do GitHub na mesma branch. Use o nome da branch capturado no passo 4 no lugar de `<branch>`:
   `git rev-list --count HEAD..origin/<branch>`
   - Se o comando der erro (a sua branch ainda não existe no GitHub): pare aqui e responda:
     "Sua versão de trabalho ainda não está ligada ao GitHub, então não há o que sincronizar agora. Pode usar o projeto normalmente. Se precisar conectar, me chama."
   - Se o número for 0: o projeto já está atualizado. Pare aqui e responda:
     "Tudo certo. Seu projeto já está na versão mais recente. Pode usar normalmente."
   - Se o número for maior que 0: antes de seguir, verifique se você tem trabalho local que ainda não foi para o GitHub:
     `git rev-list --count origin/<branch>..HEAD`
     - Se esse segundo número for 0: siga para o passo 8.
     - Se esse segundo número for MAIOR que 0: a sua versão e a do GitHub seguiram caminhos diferentes. Não tente atualizar sozinho. Pare aqui e responda:
       "Sua versão do projeto e a versão do GitHub seguiram caminhos um pouco diferentes. Tem coisa nova dos dois lados. Não vou mexer pra não bagunçar nada, está tudo guardado e seguro. Me chama que a gente junta as duas versões juntos, é rápido."

8. Verifique se existem alterações locais não commitadas:
   `git status --porcelain`
   - Se a saída estiver VAZIA: pule direto para o passo 10.
   - Se tiver QUALQUER linha: siga para o passo 9.

9. Guarde as alterações locais num bolso temporário antes de atualizar:
   `git stash push -u -m "auto-stash-pre-update"`
   Marque internamente que foi feito stash (vai precisar saber disso nos passos 11 e 12).

10. Baixe as atualizações:
    `git pull --ff-only`
    - Se o comando der erro: pule para o passo 14 (mensagem de erro).
    - Se rodar com sucesso: siga para o passo 11.

11. Se foi feito stash no passo 9, tente devolver as alterações locais:
    `git stash pop`
    Depois rode:
    `git diff --name-only --diff-filter=U`
    - Se a saída estiver VAZIA: deu tudo certo, siga para o passo 13.
    - Se listar um ou mais arquivos: houve conflito de verdade. NÃO pare nem mande o usuário se virar sozinho. Conduza a resolução guiada do passo 12.
    Se NÃO foi feito stash no passo 9, siga direto para o passo 13.

12. RESOLUÇÃO GUIADA DE CONFLITO (apenas se o passo 11 listou arquivos).
    O conflito acontece quando o usuário mexeu num arquivo do sistema (uma skill, um script, um arquivo de configuração) e a atualização também mexeu no mesmo arquivo. Os arquivos pessoais do usuário (a pasta dos produtos dele e o arquivo de credenciais) nunca entram aqui, estão sempre protegidos.

    Comece avisando, em tom calmo:
    "A atualização chegou, só que um ou outro arquivo seu coincidiu com uma mudança nova. Nada foi perdido. Vou te mostrar cada caso e você só me diz qual versão prefere manter."

    Para CADA arquivo listado no passo 11, faça o seguinte:
    a) Abra o arquivo e localize os trechos em conflito (marcados internamente pelo git). O trecho entre o marcador de topo e o marcador do meio é a VERSÃO ATUALIZADA do projeto. O trecho entre o marcador do meio e o marcador de baixo é a VERSÃO DO USUÁRIO.
    b) Mostre ao usuário, em linguagem simples, sem jargão técnico e sem mostrar os marcadores do git:
       "No arquivo '{nome amigável do arquivo}':
        - Na versão atualizada do projeto, esse trecho está assim:
          {conteúdo da versão atualizada, resumido se for longo}
        - Na sua versão atual, está assim:
          {conteúdo da versão do usuário, resumido se for longo}
        Qual você quer manter?
        1. A versão atualizada do projeto
        2. A minha versão"
    c) Aguarde a resposta do usuário. Se ele tiver dúvida, explique a diferença prática entre as duas em frases curtas. Não decida por ele.
    d) Aplique a escolha editando o arquivo: deixe somente o conteúdo escolhido e remova todos os marcadores de conflito do git. O arquivo final precisa ficar limpo, sem nenhum marcador.
    e) Marque o arquivo como resolvido:
       `git add "<caminho do arquivo>"`
    f) Repita para o próximo arquivo da lista.

    Quando todos os arquivos da lista estiverem resolvidos e adicionados, limpe o bolso temporário:
    `git stash drop`
    Depois siga para o passo 13.

13. Liste o que mudou entre o commit antigo (do passo 5) e o atual:
    `git log <commit_antigo>..HEAD --pretty=format:"- %s" --no-merges`
    Responda ao usuário no formato abaixo, em português brasileiro, tom amigável, sem termos técnicos, sem mostrar comandos git nem hashes:
    "Pronto. Seu projeto foi atualizado com sucesso.
    O que chegou de novo nesta atualização:
    {lista das mensagens de commit em linguagem natural, uma por linha começando com hífen}
    Tudo certo pra continuar usando."
    - Se o passo 12 foi executado (houve conflito resolvido), acrescente ao final:
      "Também ajustei junto com você os arquivos que tinham mudanças dos dois lados, então está tudo conciliado."

14. Mensagem de erro genérica (se algum passo crítico falhar):
    "Tive um problema ao atualizar. Tenta fechar e abrir o aplicativo de novo. Se continuar, me chama."

## Regras importantes

- Nunca use `git reset`, `git checkout --`, `git clean` ou qualquer comando destrutivo.
- Nunca force push, nunca rebase, nunca delete branch.
- Nunca descarte o stash sem ter feito pop com sucesso. Exceção única: no passo 12, depois de TODOS os conflitos terem sido resolvidos e adicionados, o `git stash drop` é permitido, porque nesse ponto o pop foi concluído manualmente.
- Para resolver conflito, nunca escolha o lado sozinho. Sempre mostre as duas versões ao usuário e deixe ele decidir.
- Resolva conflito editando o arquivo direto (escolhendo o conteúdo e limpando os marcadores). Não use `git checkout --ours` nem `git checkout --theirs`.
- Não mostre comandos git crus, marcadores de conflito nem hashes ao usuário final. Fale como um assistente, não como um terminal.
- Responda sempre em português do Brasil, com acentuação correta.

## Nota técnica de execução

No passo 13, em terminais que interpretam `%` de forma especial (PowerShell em alguns contextos), prefira rodar o `git log` pela ferramenta Bash, ou use a sintaxe de parada de parser do PowerShell antes dos argumentos. O objetivo é só listar as mensagens de commit; se o formato falhar, rode `git log <commit_antigo>..HEAD --no-merges --oneline` e leia as mensagens da saída.
