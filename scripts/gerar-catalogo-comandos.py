#!/usr/bin/env python3
"""Gera o COMANDOS.md, a lista de comandos do projeto agrupada por categoria.

A lista vem do cabeçalho de cada arquivo em .claude/commands/*.md:
    description: o que o comando faz (vale a primeira frase)
    categoria:   em qual grupo ele aparece
    interno: true  deixa o comando fora da lista (aliases antigos, uso interno)

Também entram as skills sem comando que o aluno chama pelo nome e os agentes
especialistas, listados nas constantes abaixo.

O CLAUDE.md não carrega mais a lista: quando o aluno pede para ver os comandos,
o assistente lê o COMANDOS.md. Por isso a lista precisa estar sempre em dia. O
scripts/exportar-para-codex.py chama este script, e ele roda sempre que algo
muda em .claude/.

Uso:
    python3 scripts/gerar-catalogo-comandos.py              # grava o COMANDOS.md
    python3 scripts/gerar-catalogo-comandos.py --verificar  # só confere se está em dia
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
COMANDOS = RAIZ / ".claude" / "commands"
SKILLS = RAIZ / ".claude" / "skills"
AGENTES = RAIZ / ".claude" / "agents"
DESTINO = RAIZ / "COMANDOS.md"

# Ordem em que as categorias aparecem. Categoria nova vai para o fim.
ORDEM = [
    "Produto",
    "Copy",
    "Conteúdo e Criativos",
    "Low Ticket",
    "Tráfego Pago",
    "Dados e Automações",
    "Estratégia",
    "Estudo",
    "Comercial",
    "Vídeo",
    "Infraestrutura de Página",
    "Feedback",
    "Toolkit",
    "Configurações",
]

# Skills sem comando próprio que o aluno chama pelo nome.
SKILLS_SEM_COMANDO = {
    "dashboard-social": "Dados e Automações",
    "instagram-dashboard": "Dados e Automações",
    "tiktok-dashboard": "Dados e Automações",
    "youtube-dashboard": "Dados e Automações",
    "linkedin-dashboard": "Dados e Automações",
    "biblioteca-anuncios": "Dados e Automações",
    "programar-carrossel": "Conteúdo e Criativos",
    "gestor-pedagogico": "Estudo",
}

AGENTES_ESPECIALISTAS = [
    "estrategista-de-produto",
    "estrategista-low-ticket",
    "estrategista-middle-ticket",
    "estrategista-ht",
    "construtor-de-paginas",
    "criador-de-campanhas",
    "consultor-comercial",
    "copywriter",
    "video-maker",
    "executor-de-plano-de-acao",
]

LIMITE = 220  # Caracteres da descrição curta.


def cabecalho(arquivo: Path) -> dict[str, str]:
    """Campos do cabeçalho YAML, com suporte a texto dobrado (> e |)."""
    linhas = arquivo.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n")
    if not linhas or linhas[0].strip() != "---":
        return {}
    campos: dict[str, str] = {}
    chave = None
    for linha in linhas[1:]:
        if linha.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", linha)
        if m:
            chave, valor = m.group(1), m.group(2).strip()
            campos[chave] = "" if valor in (">", "|", ">-", "|-") else valor.strip('"').strip("'")
        elif chave and linha.startswith((" ", "\t")):
            campos[chave] = (campos[chave] + " " + linha.strip()).strip()
    return campos


def resumo(descricao: str) -> str:
    """Primeira frase da descrição, sem passar do limite."""
    texto = " ".join(descricao.split())
    m = re.search(r"^(.{25,}?[.!?])(\s|$)", texto)
    frase = m.group(1) if m else texto
    if len(frase) > LIMITE:
        frase = frase[: LIMITE - 1].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return frase


def montar() -> tuple[str, list[str]]:
    avisos: list[str] = []
    grupos: dict[str, list[str]] = {}

    for arquivo in sorted(COMANDOS.glob("*.md")):
        campos = cabecalho(arquivo)
        if campos.get("interno", "").lower() == "true":
            continue
        categoria = campos.get("categoria")
        if not categoria:
            avisos.append(f"{arquivo.relative_to(RAIZ).as_posix()} sem 'categoria:' no cabeçalho (ficou em Outros)")
            categoria = "Outros"
        descricao = resumo(campos.get("description", "")) or "Sem descrição."
        grupos.setdefault(categoria, []).append(f"- `/{arquivo.stem}`. {descricao}")

    for nome, categoria in SKILLS_SEM_COMANDO.items():
        arquivo = SKILLS / nome / "SKILL.md"
        if not arquivo.exists():
            avisos.append(f"skill {nome} listada no script, mas não existe")
            continue
        descricao = resumo(cabecalho(arquivo).get("description", "")) or "Sem descrição."
        grupos.setdefault(categoria, []).append(f"- `{nome}`. {descricao}")

    agentes = []
    for nome in AGENTES_ESPECIALISTAS:
        arquivo = AGENTES / f"{nome}.md"
        if not arquivo.exists():
            avisos.append(f"agente {nome} listado no script, mas não existe")
            continue
        agentes.append(f"- `{nome}`. {resumo(cabecalho(arquivo).get('description', ''))}")

    ordem = ORDEM + sorted(c for c in grupos if c not in ORDEM)
    partes = [
        "# Comandos do projeto",
        "",
        "<!-- Gerado por scripts/gerar-catalogo-comandos.py a partir do cabeçalho de cada",
        "     arquivo em .claude/commands/. Não edite aqui: edite o comando e rode o script. -->",
        "",
        "Lista de tudo que o assistente faz, por categoria. Os que começam com `/` são comandos;",
        "os outros são chamados pelo nome (\"usar o instagram-dashboard\").",
    ]
    for categoria in ordem:
        if categoria not in grupos:
            continue
        partes += ["", f"## {categoria}", "", *grupos[categoria]]
    if agentes:
        partes += ["", "## Agentes Especialistas (tarefas completas)", "", *agentes]
    return "\n".join(partes) + "\n", avisos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--verificar", action="store_true", help="só confere se o COMANDOS.md está em dia")
    args = parser.parse_args()

    conteudo, avisos = montar()
    for aviso in avisos:
        print(f"Aviso: {aviso}.")
    atual = DESTINO.read_text(encoding="utf-8-sig").replace("\r\n", "\n") if DESTINO.exists() else None

    if args.verificar:
        if atual == conteudo:
            print("COMANDOS.md em dia.")
            return 0
        print("COMANDOS.md desatualizado. Rode: python3 scripts/gerar-catalogo-comandos.py")
        return 1

    if atual == conteudo:
        print("COMANDOS.md já estava em dia.")
    else:
        DESTINO.write_bytes(conteudo.encode("utf-8"))
        print("COMANDOS.md gerado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
