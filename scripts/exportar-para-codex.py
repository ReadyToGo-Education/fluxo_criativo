#!/usr/bin/env python3
"""Gera as pastas .agents/ e .codex/ a partir de .claude/.

Skills, commands, agentes e hooks do projeto são escritos uma vez só, em
.claude/. Este script monta a partir deles a versão que o Codex (e outros
agentes que seguem o padrão aberto .agents/skills) consegue ler:

    .claude/skills/{nome}/            -> .agents/skills/{nome}/  (cópia fiel)
    .claude/commands/**/{nome}/SKILL.md -> .agents/skills/{nome}/  (cópia fiel da pasta)
    .claude/commands/{nome}.md        -> .agents/skills/source-command-{nome}/SKILL.md
    .claude/agents/{nome}.md          -> .codex/agents/{nome}.toml
    hooks de .claude/settings.json    -> .codex/hooks.json  (aponta para .claude/hooks/)

O texto não é alterado. As referências a CLAUDE.md e a .claude/ continuam
valendo no Codex, porque o AGENTS.md manda consultar esses arquivos, e é no
CLAUDE.md que estão as regras globais (gate da Meta, abertura de sessão etc.).

As demais subpastas de .claude/commands (criativo-estatico/, references/ etc.)
não viram skills: os commands leem esses arquivos pelo caminho em .claude/.

Uso:
    python3 scripts/exportar-para-codex.py              gera ou atualiza as pastas
    python3 scripts/exportar-para-codex.py --verificar  só confere; sai com código 1
                                                         se algo estiver desatualizado

Nunca edite .agents/ nem .codex/ à mão: edite .claude/ e rode o script de novo.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = "scripts/exportar-para-codex.py"

ORIGEM_SKILLS = RAIZ / ".claude" / "skills"
ORIGEM_COMMANDS = RAIZ / ".claude" / "commands"
ORIGEM_AGENTES = RAIZ / ".claude" / "agents"
ORIGEM_SETTINGS = RAIZ / ".claude" / "settings.json"

DESTINO_SKILLS = RAIZ / ".agents" / "skills"
DESTINO_AGENTES = RAIZ / ".codex" / "agents"
DESTINO_HOOKS = RAIZ / ".codex" / "hooks.json"

PREFIXO_COMMAND = "source-command-"

# Lixo local que nunca entra na exportação.
IGNORAR_PASTAS = {"__pycache__"}
IGNORAR_ARQUIVOS = {".DS_Store", "Thumbs.db", "desktop.ini"}
IGNORAR_EXTENSOES = {".pyc"}

# Eventos de hook que o Codex reconhece. Os demais eventos do Claude Code ficam de fora.
EVENTOS_CODEX = {
    "SessionStart", "SessionEnd", "UserPromptSubmit", "PreToolUse",
    "PermissionRequest", "PostToolUse", "PreCompact", "PostCompact",
    "SubagentStart", "SubagentStop", "Stop", "Interrupt",
}

# "node .claude/hooks/x.js" ou "bash .claude/hooks/x.sh"
PADRAO_HOOK = re.compile(r"^(?P<programa>\S+)\s+(?P<caminho>\.claude/hooks/\S+)$")


# ─── leitura ─────────────────────────────────────────────────────────────────

def ler_texto(arquivo: Path) -> str:
    """Lê como UTF-8 (tolera BOM) e padroniza a quebra de linha em LF."""
    return arquivo.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def eh_lixo(relativo: Path) -> bool:
    return (
        any(parte in IGNORAR_PASTAS for parte in relativo.parts)
        or relativo.name in IGNORAR_ARQUIVOS
        or relativo.suffix in IGNORAR_EXTENSOES
    )


def listar_arquivos(pasta: Path) -> list[Path]:
    """Lista os arquivos de uma pasta de origem, sem o lixo local.

    Com o git disponível, entram os arquivos versionados e os novos ainda não
    adicionados, e ficam de fora os que o .gitignore ignora. Sem o git, a
    pasta é varrida inteira.
    """
    relativo_raiz = pasta.relative_to(RAIZ).as_posix()
    try:
        saida = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", relativo_raiz],
            cwd=RAIZ, capture_output=True, check=True,
        ).stdout
        candidatos = [RAIZ / p for p in saida.decode("utf-8").split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        candidatos = list(pasta.rglob("*"))

    # Arquivos apagados do disco, mas ainda no índice do git, ficam de fora no is_file().
    return sorted({c for c in candidatos if c.is_file() and not eh_lixo(c.relative_to(pasta))})


def tirar_aspas(valor: str) -> str:
    if len(valor) >= 2 and valor[0] == valor[-1] == '"':
        try:
            return json.loads(valor)
        except ValueError:
            return valor[1:-1]
    if len(valor) >= 2 and valor[0] == valor[-1] == "'":
        return valor[1:-1].replace("''", "'")
    return valor


def separar_frontmatter(texto: str) -> tuple[dict[str, str], str]:
    """Separa o cabeçalho YAML (entre as linhas ---) do corpo do arquivo.

    Cobre o que o projeto usa: "chave: valor", valores entre aspas e blocos
    "chave: >" com as linhas seguintes recuadas.
    """
    linhas = texto.split("\n")
    if not linhas or linhas[0].strip() != "---":
        return {}, texto
    fim = next((i for i in range(1, len(linhas)) if linhas[i].strip() == "---"), None)
    if fim is None:
        return {}, texto

    campos: dict[str, str] = {}
    atual = None
    for linha in linhas[1:fim]:
        par = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", linha)
        if par and not linha[:1].isspace():
            atual, valor = par.group(1), par.group(2).strip()
            campos[atual] = "" if valor in {">", "|", ">-", "|-", ">+", "|+"} else tirar_aspas(valor)
        elif atual and linha.strip():
            campos[atual] = (campos[atual] + " " + linha.strip()).strip()
    return campos, "\n".join(linhas[fim + 1:])


# ─── conversões ──────────────────────────────────────────────────────────────

def skill_de_command(arquivo: Path) -> bytes:
    nome = arquivo.stem
    campos, corpo = separar_frontmatter(ler_texto(arquivo))
    descricao = campos.get("description") or f"Roteiro do comando /{nome} do workshop."
    linhas = [
        "---",
        f"name: {json.dumps(PREFIXO_COMMAND + nome, ensure_ascii=False)}",
        f"description: {json.dumps(descricao, ensure_ascii=False)}",
        "---",
        "",
        f"# {PREFIXO_COMMAND}{nome}",
        "",
        f"Use esta skill quando o usuário pedir o comando `/{nome}` do workshop (ou `{nome}`, sem a barra).",
        "",
        f"<!-- Gerado por {SCRIPT} a partir de .claude/commands/{nome}.md."
        " Não edite aqui: edite o original e rode o script de novo. -->",
        "",
        "## Roteiro do comando",
        "",
        corpo.strip("\n"),
        "",
    ]
    return "\n".join(linhas).encode("utf-8")


def toml_texto(valor: str) -> str:
    # As escapes que o json gera são todas válidas numa string básica de TOML; falta só o DEL.
    return json.dumps(valor, ensure_ascii=False).replace("\x7f", "\\u007F")


def toml_texto_multilinha(valor: str) -> str:
    escapado = valor.replace("\\", "\\\\").replace('"""', '""\\"')
    # Caracteres de controle (menos tab e quebra de linha) precisam de escape em TOML.
    escapado = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", lambda m: "\\u%04X" % ord(m.group()), escapado)
    return '"""\n' + escapado + '\n"""'


def toml_de_agente(arquivo: Path) -> bytes:
    nome = arquivo.stem
    campos, corpo = separar_frontmatter(ler_texto(arquivo))
    instrucoes = corpo.strip("\n")
    conteudo = "\n".join([
        f"# Gerado por {SCRIPT} a partir de .claude/agents/{nome}.md.",
        "# Não edite aqui: edite o original e rode o script de novo.",
        f"name = {toml_texto(campos.get('name') or nome)}",
        f"description = {toml_texto(campos.get('description', ''))}",
        f"developer_instructions = {toml_texto_multilinha(instrucoes)}",
        "",
    ])

    # Confere o escape relendo o TOML (tomllib existe a partir do Python 3.11).
    try:
        import tomllib
    except ImportError:
        tomllib = None
    if tomllib is not None and tomllib.loads(conteudo)["developer_instructions"] != instrucoes + "\n":
        raise SystemExit(f"Erro ao converter o agente {nome}: o TOML gerado não bate com o original.")
    return conteudo.encode("utf-8")


def gerar_hooks(avisos: list[str]) -> tuple[bytes, int]:
    """Traduz os hooks do .claude/settings.json para o formato do Codex.

    Os scripts continuam em .claude/hooks/. No Mac e no Linux o caminho parte da
    raiz do git, como a documentação do Codex recomenda (o Codex pode ser aberto
    numa subpasta). No Windows vale o caminho relativo, igual ao do Claude Code.
    """
    configuracao = json.loads(ler_texto(ORIGEM_SETTINGS)).get("hooks", {})
    eventos: dict[str, list] = {}
    total = 0
    for evento, grupos in configuracao.items():
        if evento not in EVENTOS_CODEX:
            avisos.append(f"o evento de hook {evento} não existe no Codex e ficou de fora")
            continue
        for grupo in grupos:
            handlers = []
            for hook in grupo.get("hooks", []):
                comando = hook.get("command", "").strip()
                caminho = PADRAO_HOOK.match(comando)
                novo = {"type": hook.get("type", "command")}
                if caminho:
                    novo["command"] = f'{caminho["programa"]} "$(git rev-parse --show-toplevel)/{caminho["caminho"]}"'
                    novo["commandWindows"] = comando
                else:
                    novo["command"] = comando
                novo.update({k: v for k, v in hook.items() if k not in {"type", "command"}})
                handlers.append(novo)
            if handlers:
                bloco = {"matcher": grupo["matcher"]} if "matcher" in grupo else {}
                bloco["hooks"] = handlers
                eventos.setdefault(evento, []).append(bloco)
                total += len(handlers)

    conteudo = {
        "description": f"Gerado por {SCRIPT} a partir dos hooks de .claude/settings.json. Não edite à mão.",
        "hooks": eventos,
    }
    return (json.dumps(conteudo, indent=2, ensure_ascii=False) + "\n").encode("utf-8"), total


# ─── montagem e comparação ───────────────────────────────────────────────────

def montar_esperado(avisos: list[str]) -> tuple[dict[Path, tuple[bytes, Path | None]], dict[str, int]]:
    """Calcula tudo o que deve existir em .agents/ e .codex/.

    Cada entrada guarda o conteúdo e, nas cópias fiéis, o arquivo de origem
    (para copiar também a permissão de execução).
    """
    esperado: dict[Path, tuple[bytes, Path | None]] = {}
    contagem = {"skills": 0, "commands": 0, "agentes": 0, "hooks": 0}

    skills = set()
    for arquivo in listar_arquivos(ORIGEM_SKILLS):
        relativo = arquivo.relative_to(ORIGEM_SKILLS)
        skills.add(relativo.parts[0])
        esperado[DESTINO_SKILLS / relativo] = (arquivo.read_bytes(), arquivo)
    # Skills completas guardadas dentro de .claude/commands (ex.: Skill VSL/skills/vsl-video-vendas).
    for skill_md in sorted(ORIGEM_COMMANDS.rglob("SKILL.md")):
        pasta_origem = skill_md.parent
        if pasta_origem.name in skills:
            raise SystemExit(f"Conflito de nome: a skill {pasta_origem.name} existe em .claude/skills e em .claude/commands.")
        skills.add(pasta_origem.name)
        for arquivo in listar_arquivos(pasta_origem):
            esperado[DESTINO_SKILLS / pasta_origem.name / arquivo.relative_to(pasta_origem)] = (arquivo.read_bytes(), arquivo)
    contagem["skills"] = len(skills)

    for arquivo in sorted(ORIGEM_COMMANDS.glob("*.md")):
        pasta = PREFIXO_COMMAND + arquivo.stem
        if pasta in skills:
            raise SystemExit(f"Conflito de nome: já existe a skill .claude/skills/{pasta}.")
        esperado[DESTINO_SKILLS / pasta / "SKILL.md"] = (skill_de_command(arquivo), None)
        contagem["commands"] += 1

    for arquivo in sorted(ORIGEM_AGENTES.glob("*.md")):
        esperado[DESTINO_AGENTES / f"{arquivo.stem}.toml"] = (toml_de_agente(arquivo), None)
        contagem["agentes"] += 1

    hooks, contagem["hooks"] = gerar_hooks(avisos)
    esperado[DESTINO_HOOKS] = (hooks, None)
    return esperado, contagem


def normalizar(conteudo: bytes) -> bytes:
    """Ignora a diferença CRLF x LF nos arquivos de texto (o git converte no Windows)."""
    return conteudo if b"\0" in conteudo else conteudo.replace(b"\r\n", b"\n")


def arquivos_existentes() -> set[Path]:
    existentes = set()
    for pasta in (DESTINO_SKILLS, DESTINO_AGENTES):
        if pasta.exists():
            existentes.update(p for p in pasta.rglob("*") if p.is_file() and not eh_lixo(p.relative_to(pasta)))
    if DESTINO_HOOKS.exists():
        existentes.add(DESTINO_HOOKS)
    return existentes


def remover_pastas_vazias(pasta: Path) -> None:
    if not pasta.exists():
        return
    for atual, _, _ in sorted(os.walk(pasta), key=lambda item: len(item[0]), reverse=True):
        caminho = Path(atual)
        if caminho != pasta and not any(caminho.iterdir()):
            caminho.rmdir()


def relativo(caminho: Path) -> str:
    return caminho.relative_to(RAIZ).as_posix()


def escondidos_pelo_gitignore(caminhos: list[Path]) -> list[Path]:
    """Arquivos gerados que o .gitignore deixaria fora do repositório."""
    entrada = "\0".join(relativo(c) for c in caminhos).encode("utf-8")
    try:
        saida = subprocess.run(
            ["git", "check-ignore", "--no-index", "-z", "--stdin"],
            cwd=RAIZ, input=entrada, capture_output=True,
        ).stdout
    except OSError:
        return []
    return sorted({RAIZ / p for p in saida.decode("utf-8").split("\0") if p})


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    parser = argparse.ArgumentParser(description="Gera .agents/ e .codex/ a partir de .claude/.")
    parser.add_argument("--verificar", action="store_true",
                        help="só confere se as pastas estão em dia, sem gravar nada")
    args = parser.parse_args()

    avisos: list[str] = []
    esperado, contagem = montar_esperado(avisos)
    existentes = arquivos_existentes()

    novos = sorted(p for p in esperado if p not in existentes)
    alterados = sorted(
        p for p in esperado
        if p in existentes and normalizar(p.read_bytes()) != normalizar(esperado[p][0])
    )
    sobrando = sorted(existentes - set(esperado))
    escondidos = escondidos_pelo_gitignore(sorted(esperado))

    for aviso in avisos:
        print(f"Aviso: {aviso}.")
    if escondidos:
        print(
            f"Aviso: o .gitignore deixa {len(escondidos)} arquivo(s) gerado(s) fora do repositório "
            f"(ex.: {relativo(escondidos[0])}). Libere .agents/ e .codex/ no .gitignore."
        )

    if args.verificar:
        pendencias = (
            [("novo", p) for p in novos] + [("alterado", p) for p in alterados]
            + [("sobrando", p) for p in sobrando] + [("ignorado pelo git", p) for p in escondidos]
        )
        if not pendencias:
            print("Tudo em dia: .agents/ e .codex/ batem com .claude/.")
            return 0
        print(f"{len(pendencias)} arquivo(s) desatualizado(s) em .agents/ ou .codex/:")
        for tipo, caminho in pendencias[:20]:
            print(f"  {tipo}: {relativo(caminho)}")
        if len(pendencias) > 20:
            print(f"  e mais {len(pendencias) - 20}.")
        print(f"Rode: python3 {SCRIPT}")
        return 1

    for caminho in novos + alterados:
        conteudo, origem = esperado[caminho]
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_bytes(conteudo)
        if origem is not None:
            shutil.copymode(origem, caminho)
    for caminho in sobrando:
        caminho.unlink()
    remover_pastas_vazias(DESTINO_SKILLS)
    remover_pastas_vazias(DESTINO_AGENTES)

    print(
        f"Exportação concluída: {contagem['skills']} skills, {contagem['commands']} commands, "
        f"{contagem['agentes']} agentes e {contagem['hooks']} hooks."
    )
    print(f"Arquivos criados: {len(novos)}. Alterados: {len(alterados)}. Removidos: {len(sobrando)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
