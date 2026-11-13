#!/usr/bin/env python3
"""
agente-ia. Monta, lê e mede o plugin do ChatGPT que entrega o agente ao aluno.

O plugin do ChatGPT substitui o GPT personalizado (que sai do ar em 11/12/2026).
O arquivo .zip tem sempre esta estrutura, a mesma dos plugins que o Plugin Creator
da OpenAI gera e instala:

    plugin.json
    .codex-plugin/plugin.json
    skills/<habilidade>/SKILL.md     (uma pasta por habilidade)

Uso:
    python3 montar-plugin.py montar --spec plugin-spec.json --saida pasta-do-agente
        Lê a ficha do plugin (JSON) e grava a pasta plugin/ e o arquivo <nome>.zip
        dentro de pasta-do-agente.

    python3 montar-plugin.py ler --zip arquivo.zip --spec plugin-spec.json
        Faz o caminho inverso: lê um .zip de plugin e grava a ficha em JSON,
        para atualizar um plugin que já existe.

    python3 montar-plugin.py contar --arquivo instrucoes.md
        Conta os caracteres de um texto (o campo de instruções da Hotmart
        aceita até 10.000 caracteres e o de descrição, até 2.000).

Ficha do plugin (plugin-spec.json):
{
  "nome": "personal-trainer-leitura10x",
  "versao": "1.0.0",
  "nome_exibido": "Personal Trainer Leitura10x",
  "descricao": "Uma frase sobre o que o plugin faz.",
  "descricao_curta": "Até 60 caracteres",
  "descricao_longa": "Duas ou três frases para a página do plugin.",
  "categoria": "Education & Research",
  "mensagem_inicial": "Quero começar meu treino de 15 minutos.",
  "autor": "Nome do infoprodutor",
  "habilidades": [
    {"nome": "montar-treino", "descricao": "Use quando ...", "conteudo": "# Título\\n\\n..."}
  ]
}
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
# Só as categorias já vistas em plugins que o ChatGPT aceitou.
CATEGORIAS = ["Education & Research", "Productivity"]
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
VERSAO = re.compile(r"^\d+\.\d+\.\d+$")
DATA_FIXA = (1980, 1, 1, 0, 0, 0)  # mesma data dos .zip que o ChatGPT gera


def erro(msg):
    print(json.dumps({"status": "erro", "erro": msg}, ensure_ascii=False))
    sys.exit(1)


def validar(spec):
    obrigatorios = ["nome", "versao", "nome_exibido", "descricao", "descricao_curta",
                    "descricao_longa", "mensagem_inicial", "autor", "habilidades"]
    faltando = [c for c in obrigatorios if not spec.get(c)]
    if faltando:
        erro("Faltam campos na ficha do plugin: " + ", ".join(faltando))
    if not SLUG.match(spec["nome"]):
        erro("O nome do plugin precisa ser minúsculo, sem acento, com hífen (ex: avaliador-de-redacao).")
    if not VERSAO.match(spec["versao"]):
        erro("A versão precisa ter o formato 1.0.0.")
    if not isinstance(spec["habilidades"], list) or not spec["habilidades"]:
        erro("O plugin precisa de pelo menos uma habilidade.")
    nomes = set()
    for h in spec["habilidades"]:
        for c in ["nome", "descricao", "conteudo"]:
            if not h.get(c):
                erro(f"A habilidade {h.get('nome', '(sem nome)')} está sem o campo {c}.")
        if not SLUG.match(h["nome"]):
            erro(f"O nome da habilidade {h['nome']} precisa ser minúsculo, sem acento, com hífen.")
        if h["nome"] in nomes:
            erro(f"Há duas habilidades com o nome {h['nome']}.")
        nomes.add(h["nome"])
    avisos = []
    if len(spec["descricao_curta"]) > 60:
        avisos.append("A descrição curta passou de 60 caracteres e pode aparecer cortada.")
    if spec.get("categoria", CATEGORIAS[0]) not in CATEGORIAS:
        avisos.append("Categoria fora da lista conhecida. Usei Education & Research.")
        spec["categoria"] = CATEGORIAS[0]
    return avisos


def interface(spec):
    # mensagem_inicial aceita um texto ou uma lista de textos (uma sugestão por habilidade).
    return {
        "capabilities": spec.get("capacidades", []),
        "category": spec.get("categoria", CATEGORIAS[0]),
        "defaultPrompt": spec["mensagem_inicial"],
        "developerName": spec["autor"],
        "displayName": spec["nome_exibido"],
        "longDescription": spec["descricao_longa"],
        "shortDescription": spec["descricao_curta"],
    }


def montar(args):
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    avisos = validar(spec)

    autor = {"name": spec["autor"]}
    if spec.get("email_autor"):
        autor["email"] = spec["email_autor"]
    raiz = {
        "$schema": SCHEMA,
        "author": autor,
        "description": spec["descricao"],
        "extensions": {"com.openai": {"interface": interface(spec)}},
        "name": spec["nome"],
        "version": spec["versao"],
    }
    codex = {
        "interface": interface(spec),
        "name": spec["nome"],
        "version": spec["versao"],
        "description": spec["descricao"],
        "author": autor,
        "keywords": [],
        "skills": "./skills",
    }

    # Mesmo formato do ChatGPT: JSON com acentos escapados.
    arquivos = {
        "plugin.json": json.dumps(raiz, indent=2) + "\n",
        ".codex-plugin/plugin.json": json.dumps(codex, indent=2) + "\n",
    }
    for h in spec["habilidades"]:
        descricao = h["descricao"].replace("\n", " ").strip()
        # Aspas só quando o texto tem algo que quebraria o cabeçalho (dois-pontos, aspas, #).
        if re.search(r'[:#"\']', descricao) or descricao[:1] in "-[{>|*&!%@`":
            descricao = json.dumps(descricao, ensure_ascii=False)
        corpo = h["conteudo"].strip() + "\n"
        arquivos[f"skills/{h['nome']}/SKILL.md"] = (
            f"---\nname: {h['nome']}\ndescription: {descricao}\n---\n\n{corpo}"
        )

    saida = Path(args.saida)
    pasta = saida / "plugin"
    for relativo, texto in arquivos.items():
        destino = pasta / relativo
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8", newline="\n")

    caminho_zip = saida / f"{spec['nome']}.zip"
    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for relativo, texto in arquivos.items():
            info = zipfile.ZipInfo(relativo, date_time=DATA_FIXA)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, texto.encode("utf-8"))

    print(json.dumps({
        "status": "ok",
        "zip": str(caminho_zip.resolve()),
        "pasta": str(pasta.resolve()),
        "versao": spec["versao"],
        "habilidades": [h["nome"] for h in spec["habilidades"]],
        "avisos": avisos,
    }, ensure_ascii=False, indent=2))


def ler(args):
    try:
        z = zipfile.ZipFile(args.zip)
    except (OSError, zipfile.BadZipFile):
        erro("Não consegui abrir o arquivo. Confira se é o .zip do plugin, sem descompactar.")
    nomes = z.namelist()
    if "plugin.json" not in nomes:
        erro("O arquivo não tem o plugin.json na raiz. Ele não parece um plugin do ChatGPT.")
    raiz = json.loads(z.read("plugin.json").decode("utf-8"))
    inter = raiz.get("extensions", {}).get("com.openai", {}).get("interface", {})
    mensagem = inter.get("defaultPrompt", "")
    habilidades = []
    for nome in sorted(nomes):
        m = re.match(r"^skills/([^/]+)/SKILL\.md$", nome)
        if not m:
            continue
        texto = z.read(nome).decode("utf-8")
        descricao, corpo = "", texto
        fm = re.match(r"^---\n(.*?)\n---\n\n?(.*)$", texto, re.S)
        if fm:
            corpo = fm.group(2)
            d = re.search(r"^description:\s*(.*)$", fm.group(1), re.M)
            if d:
                valor = d.group(1).strip()
                try:
                    descricao = json.loads(valor) if valor.startswith('"') else valor
                except json.JSONDecodeError:
                    descricao = valor.strip('"')
        habilidades.append({"nome": m.group(1), "descricao": descricao, "conteudo": corpo.strip()})
    versao = str(raiz.get("version", "1.0.0")).split("+")[0]
    spec = {
        "nome": raiz.get("name", ""),
        "versao": versao if VERSAO.match(versao) else "1.0.0",
        "nome_exibido": inter.get("displayName", ""),
        "descricao": raiz.get("description", ""),
        "descricao_curta": inter.get("shortDescription", ""),
        "descricao_longa": inter.get("longDescription", ""),
        "categoria": inter.get("category", CATEGORIAS[0]),
        "mensagem_inicial": mensagem,
        "autor": raiz.get("author", {}).get("name", inter.get("developerName", "")),
        "habilidades": habilidades,
    }
    if inter.get("capabilities"):
        spec["capacidades"] = inter["capabilities"]
    if raiz.get("author", {}).get("email"):
        spec["email_autor"] = raiz["author"]["email"]
    Path(args.spec).parent.mkdir(parents=True, exist_ok=True)
    Path(args.spec).write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "ok",
        "spec": str(Path(args.spec).resolve()),
        "nome": spec["nome"],
        "versao": spec["versao"],
        "habilidades": [h["nome"] for h in habilidades],
    }, ensure_ascii=False, indent=2))


def contar(args):
    texto = Path(args.arquivo).read_text(encoding="utf-8")
    print(json.dumps({"status": "ok", "caracteres": len(texto.strip())}, ensure_ascii=False))


def main():
    # No Windows o terminal usa outra codificação e estraga os acentos das mensagens.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Monta, lê e mede o plugin do ChatGPT do agente.")
    sub = p.add_subparsers(dest="acao", required=True)
    m = sub.add_parser("montar")
    m.add_argument("--spec", required=True)
    m.add_argument("--saida", required=True)
    m.set_defaults(func=montar)
    l = sub.add_parser("ler")
    l.add_argument("--zip", required=True)
    l.add_argument("--spec", required=True)
    l.set_defaults(func=ler)
    c = sub.add_parser("contar")
    c.add_argument("--arquivo", required=True)
    c.set_defaults(func=contar)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
