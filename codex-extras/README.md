# codex-extras

O que vale **só no Codex** e não pode morar em `.claude/`, porque o Claude Code também lê aquela pasta.

O caso que criou esta pasta: o Claude Code não gera imagem, então os fluxos de `.claude/` terminam num prompt para o aluno colar no ChatGPT. O Codex gera a imagem com a ferramenta dele, pelo plano do ChatGPT do aluno. Essa diferença fica aqui.

O script `scripts/exportar-para-codex.py` junta esta pasta com `.claude/` e gera `.agents/` e `.codex/`:

| Origem | Vai para | Uso |
|---|---|---|
| `codex-extras/skills/{nome}/` | `.agents/skills/{nome}/` | Skill que só existe no Codex (ex.: `imagem-no-codex`) |
| `codex-extras/acrescimos/{caminho}` | colado no começo de `.agents/skills/{caminho}` | Aviso curto numa skill exportada, apontando o que muda no Codex |

## Regras

- O caminho dentro de `acrescimos/` repete o caminho do arquivo em `.agents/skills/`. Exemplo: `acrescimos/carrossel/references/passo-output-triplo.md` entra no começo de `.agents/skills/carrossel/references/passo-output-triplo.md`. Se o arquivo de destino não existir, o script para e avisa.
- Acréscimo é curto: diz o que muda e aponta para a skill do Codex que explica o resto. O passo a passo fica na skill, num lugar só.
- Uma skill daqui não pode ter o mesmo nome de uma skill ou command de `.claude/`.
- Depois de mexer aqui, rode `python3 scripts/exportar-para-codex.py`.
- A regra geral que manda o Codex usar estas skills fica no `AGENTS.md`, que só o Codex lê.
