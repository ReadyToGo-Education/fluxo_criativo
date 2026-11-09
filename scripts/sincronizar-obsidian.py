"""Sincroniza a base de fatos do Fluxo Criativo com o Obsidian e gera fontes para o NotebookLM.

Copia os arquivos de contexto de cada produto (perfil, identidade do consumidor, pesquisa,
transcrições, base de conhecimento) e as memórias do assistente para o vault do Obsidian,
e regenera o índice principal. Entregas (copy gerada) ficam de fora de propósito: são
saídas do assistente, não fonte da verdade.

Uso:
    python3 scripts/sincronizar-obsidian.py              # só Obsidian
    python3 scripts/sincronizar-obsidian.py --notebooklm # Obsidian + fontes do NotebookLM
"""

import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PRODUTOS_DIR = RAIZ / "meus-produtos"
MEMORIA_DIR = Path.home() / ".claude" / "projects" / "C--Users-luizh-Documents-fluxo-criativo" / "memory"
VAULT = Path.home() / "OneDrive" / "Notebook" / "Documents" / "Obsidian Vault" / "Fluxo Criativo"
NOTEBOOKLM_DIR = RAIZ / "notebooklm-fontes"

# slug -> (pasta no Obsidian, nome de exibição). Pastas antigas mantidas para não duplicar.
PRODUTOS = {
    "Mannah-quantec": ("Mannah QUANTEC", "Mannah QUANTEC"),
    "ativacao-kundalini": ("Ativação Kundalini", "Ativação da Kundalini"),
    "desafio-codigo-da-acao": ("Desafio Código da Ação", "Desafio Código da Ação"),
    "formacao-interface-quebra-magia-5d": ("Interface Quebra a Magia", "Formação Interface Quebra de Magia Holográfica 5D"),
    "imersao-maquina-fluxos-dinheiro": ("Imersão Máquina de Fluxos de Dinheiro", "Imersão Seja Uma Máquina de Criar Fluxos de Dinheiro"),
    "imersao-radiestesia-holografica-5d": ("Imersão Radiestesia Holográfica 5D", "Imersão Radiestesia Holográfica 5D"),
    "instituto-mannah": ("Instituto Mannah", "Instituto Mannah (dados do negócio)"),
    "manual-10-chaves-prosperidade": ("Manual 10 Chaves da Prosperidade", "Manual de Quebra de Contratos Invisíveis de Pobreza"),
    "seja-uma-ima-de-dinheiro": ("Seja uma Imã de Dinheiro", "Seja uma Imã de Dinheiro"),
    "workshop-magia-da-prosperidade": ("Workshop Magia da Prosperidade", "Workshop Magia da Prosperidade"),
    "Conteudo-Viral": ("Conteúdo Viral", "Conteúdo Viral (Instagram da Adriana)"),
    "renan-camboim": ("Renan Camboim", "Renan Camboim (cliente)"),
}

# Trechos de caminho ignorados: saídas geradas, mídia, curso de terceiros e material bruto duplicado.
IGNORAR = (
    "entregas/",
    "painel-assets/",
    "_vtt/",
    "node_modules/",
    "modelos-formato-criativo/",
    "materiais/Metodo-Audiencia",
    "referencias/adriana-silveira/",
)

ADRIANA_REF = PRODUTOS_DIR / "manual-10-chaves-prosperidade" / "referencias" / "adriana-silveira"
ADRIANA_ARQUIVOS = ("TOM-DE-VOZ.md", "INDICE.md", "README.md", "TODAS-TRANSCRICOES.txt")

SEGREDO = re.compile(r"EAA[A-Za-z0-9]{30,}|eyJ[A-Za-z0-9_-]{30,}|xox[bp]-[A-Za-z0-9-]{10,}|apify_api_[A-Za-z0-9]{20,}")

stats = {"novos": 0, "atualizados": 0, "iguais": 0, "bloqueados": 0}


def ler(caminho):
    return caminho.read_text(encoding="utf-8", errors="replace")


def gravar(destino, conteudo):
    if SEGREDO.search(conteudo):
        stats["bloqueados"] += 1
        print(f"  BLOQUEADO (parece conter token): {destino.name}")
        return
    if destino.exists():
        if ler(destino) == conteudo:
            stats["iguais"] += 1
            return
        stats["atualizados"] += 1
    else:
        stats["novos"] += 1
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")


def converter(origem, rel_origem):
    """Devolve (nome do arquivo .md, conteúdo). .txt vira .md com cabeçalho de origem."""
    texto = ler(origem)
    if origem.suffix == ".md":
        return origem.name, texto
    cabecalho = f"---\norigem: {rel_origem}\ntipo: transcricao-ou-texto-bruto\n---\n\n# {origem.stem}\n\n"
    return origem.stem + ".md", cabecalho + texto


def arquivos_do_produto(slug):
    base = PRODUTOS_DIR / slug
    saida = []
    for arq in sorted(base.rglob("*")):
        if not arq.is_file() or arq.suffix not in (".md", ".txt"):
            continue
        rel = arq.relative_to(base).as_posix()
        if any(trecho in rel for trecho in IGNORAR) or arq.name.startswith("painel"):
            continue
        saida.append((arq, rel))
    return saida


def descricao_memoria(texto):
    m = re.search(r"^description:\s*(.+)$", texto, re.MULTILINE)
    return m.group(1).strip() if m else ""


def sincronizar_obsidian():
    indice_produtos = []
    for slug, (pasta, nome) in PRODUTOS.items():
        if not (PRODUTOS_DIR / slug).exists():
            continue
        links = []
        for arq, rel in arquivos_do_produto(slug):
            nome_md, conteudo = converter(arq, f"meus-produtos/{slug}/{rel}")
            subpasta = Path(rel).parent
            destino = VAULT / "Produtos" / pasta / subpasta / nome_md
            gravar(destino, conteudo)
            alvo = (Path("Produtos") / pasta / subpasta / Path(nome_md).stem).as_posix()
            links.append(f"[[{alvo}|{(subpasta / Path(nome_md).stem).as_posix()}]]")
        indice_produtos.append((nome, links))

    adriana_links = []
    for nome_arq in ADRIANA_ARQUIVOS:
        arq = ADRIANA_REF / nome_arq
        if arq.exists():
            nome_md, conteudo = converter(arq, f"meus-produtos/manual-10-chaves-prosperidade/referencias/adriana-silveira/{nome_arq}")
            gravar(VAULT / "Adriana Silveira" / nome_md, conteudo)
            adriana_links.append(f"[[Adriana Silveira/{Path(nome_md).stem}|{Path(nome_md).stem}]]")

    memorias = []
    for arq in sorted(MEMORIA_DIR.glob("*.md")):
        if arq.name == "MEMORY.md":
            continue
        texto = ler(arq)
        gravar(VAULT / "Memórias" / arq.name, texto)
        memorias.append((arq.stem, descricao_memoria(texto)))

    gravar(VAULT / "Fluxo Criativo — Índice.md", montar_indice(indice_produtos, adriana_links, memorias))


def montar_indice(produtos, adriana_links, memorias):
    linhas = [
        "---",
        "tipo: indice-principal",
        "origem: Fluxo Criativo",
        f"atualizado: {date.today().isoformat()}",
        "tags: [fluxo-criativo, moc, memoria, fonte-da-verdade]",
        "---",
        "",
        "# 🧠 Fluxo Criativo. Memória do Negócio",
        "",
        "Fonte da verdade do assistente de marketing. Antes de escrever qualquer copy, o assistente "
        "consulta estas notas (e o NotebookLM do produto). Informação que não está aqui não entra na copy: "
        "vira pergunta para o Henrique.",
        "",
        "Gerado por `scripts/sincronizar-obsidian.py`. Não edite à mão: as alterações são sobrescritas "
        "na próxima sincronização. Para corrigir um fato, corrija o arquivo de origem em `meus-produtos/`.",
        "",
        "---",
        "",
        "## 📦 Produtos",
        "",
    ]
    for nome, links in produtos:
        linhas.append(f"### {nome}")
        linhas.extend(f"- {l}" for l in links)
        linhas.append("")
    linhas += ["---", "", "## 🎙️ Adriana Silveira (voz e lives)", ""]
    linhas.extend(f"- {l}" for l in adriana_links)
    linhas += ["", "---", "", "## 🧩 Memórias (fatos e regras confirmados)", ""]
    for stem, desc in memorias:
        linhas.append(f"- [[Memórias/{stem}|{stem}]]. {desc}" if desc else f"- [[Memórias/{stem}|{stem}]]")
    linhas += [
        "",
        "---",
        "",
        "## ⚙️ Sistema",
        "",
        "- [[Skills — Catálogo]]",
        "- [[Agentes Especialistas]]",
        "- [[Conexões e Integrações]]",
        "- [[Metodologia VTSD]]",
        "- [[Regras do Projeto]]",
        "",
    ]
    return "\n".join(linhas)


def gerar_notebooklm():
    """Um arquivo consolidado por produto, mais voz da Adriana e memórias, prontos para subir como fonte."""
    NOTEBOOKLM_DIR.mkdir(exist_ok=True)
    relatorio = []

    def salvar(nome_arq, titulo, partes):
        corpo = [f"# {titulo}", "", "Base de fatos exportada do Fluxo Criativo. Use apenas o que está escrito aqui.", ""]
        for rel, texto in partes:
            corpo += ["", f"## Arquivo: {rel}", "", texto.strip(), ""]
        conteudo = "\n".join(corpo)
        if SEGREDO.search(conteudo):
            print(f"  BLOQUEADO (parece conter token): {nome_arq}")
            return
        (NOTEBOOKLM_DIR / nome_arq).write_text(conteudo, encoding="utf-8")
        relatorio.append((nome_arq, len(conteudo.split())))

    for slug, (_, nome) in PRODUTOS.items():
        if (PRODUTOS_DIR / slug).exists():
            partes = [(rel, ler(arq)) for arq, rel in arquivos_do_produto(slug)]
            if partes:
                salvar(f"{slug}.md", f"{nome}. Base de fatos", partes)

    salvar(
        "adriana-silveira-voz-e-lives.md",
        "Adriana Silveira. Tom de voz e transcrições das lives",
        [(n, ler(ADRIANA_REF / n)) for n in ADRIANA_ARQUIVOS if (ADRIANA_REF / n).exists()],
    )
    salvar(
        "memorias-confirmadas.md",
        "Fatos e regras confirmados pelo Henrique",
        [(a.name, ler(a)) for a in sorted(MEMORIA_DIR.glob("*.md")) if a.name != "MEMORY.md"],
    )

    print("\nFontes do NotebookLM em notebooklm-fontes/ (limite de 500 mil palavras por fonte):")
    for nome_arq, palavras in relatorio:
        alerta = "  ATENÇÃO: acima do limite" if palavras > 500_000 else ""
        print(f"  {nome_arq}: {palavras:,} palavras{alerta}".replace(",", "."))


if __name__ == "__main__":
    if not VAULT.exists():
        raise SystemExit(f"Vault do Obsidian não encontrado em {VAULT}")
    sincronizar_obsidian()
    print(
        f"Obsidian: {stats['novos']} novos, {stats['atualizados']} atualizados, "
        f"{stats['iguais']} sem mudança, {stats['bloqueados']} bloqueados."
    )
    if "--notebooklm" in sys.argv:
        gerar_notebooklm()
