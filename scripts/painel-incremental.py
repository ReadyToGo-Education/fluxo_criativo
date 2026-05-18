"""
painel-incremental.py

Atualiza o painel de entregas de um produto de forma incremental, secao a
secao. Na primeira execucao, cria o shell HTML com placeholders "Em breve".
Em execucoes seguintes, troca apenas o bloco da secao pedida, preservando o
resto.

Uso:
    py -3 scripts/painel-incremental.py --secao quadro
    py -3 scripts/painel-incremental.py --secao pesquisa --slug meu-produto

Secoes validas (ids que aparecem na sidebar e marcadores SECTION):
    pesquisa
    quadro
    furadeira
    decorados
    urgencias
    identidade-produto
    identidade-consumidor
    identidade-comunicador
    copy-pagina
    comercial-playbook   (exclusivo de /comercial-playbook)

O painel vive em:
    meus-produtos/{slug}/painel-entregas.html

Quando o slug nao e informado, o script le meus-produtos/.ativo.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import painel_template as tmpl  # noqa: E402

PRODUTOS_DIR = REPO_ROOT / "meus-produtos"
ATIVO_FILE = PRODUTOS_DIR / ".ativo"
PAINEL_NOME = "painel-entregas.html"
PAINEL_ASSETS_SRC = SCRIPT_DIR / "painel-assets"
PAINEL_ASSETS_NOME = "painel-assets"


def garantir_assets(produto_dir: Path) -> None:
    """Copia os assets do design Fluxo Criativo (logo do gorila, banner) da
    pasta do template (scripts/painel-assets/) para a pasta do produto.
    Faz apenas se o arquivo destino ainda nao existir, para nao sobrescrever
    eventuais customizacoes do usuario."""
    if not PAINEL_ASSETS_SRC.is_dir():
        return
    destino = produto_dir / PAINEL_ASSETS_NOME
    destino.mkdir(exist_ok=True)
    for arquivo in PAINEL_ASSETS_SRC.iterdir():
        if not arquivo.is_file():
            continue
        alvo = destino / arquivo.name
        if alvo.exists():
            continue
        shutil.copy2(arquivo, alvo)

SECOES_VALIDAS = sorted(tmpl.SECOES_RENDERIZAVEIS)


# ----- leitura de arquivos -----

def ler_ativo() -> str | None:
    if not ATIVO_FILE.exists():
        return None
    txt = ATIVO_FILE.read_text(encoding="utf-8").strip()
    return txt or None


def ler_arquivo(p: Path) -> str:
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def normalizar_tipo(conteudo: str) -> str:
    """Extrai apenas "Low Ticket" ou "Middle Ticket" do conteudo do tipo.md.

    O arquivo deveria conter so uma linha (Low Ticket ou Middle Ticket),
    mas em casos antigos pode vir com header markdown, justificativa e
    formato escolhido. Esta funcao varre o texto e devolve a primeira
    ocorrencia de Low/Middle Ticket que encontrar, ignorando o resto.
    Se nao achar nenhuma, devolve "a definir".
    """
    if not conteudo:
        return "a definir"
    texto = conteudo.strip()
    if not texto:
        return "a definir"
    match = re.search(r"\b(low\s+ticket|middle\s+ticket|high\s+ticket)\b", texto, re.IGNORECASE)
    if not match:
        return "a definir"
    bruto = match.group(1).lower()
    if "low" in bruto:
        return "Low Ticket"
    if "middle" in bruto:
        return "Middle Ticket"
    return "High Ticket"


# ----- helpers de parsing do markdown -----

_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def extrair_secao(texto: str, titulo: str) -> str:
    """Extrai o conteudo entre o H2 titulo e o proximo H2 (ou fim do arquivo)."""
    if not texto:
        return ""
    # localiza H2 com o titulo (case-insensitive)
    pad = re.compile(
        rf"^##\s+{re.escape(titulo)}\s*$", re.IGNORECASE | re.MULTILINE
    )
    m = pad.search(texto)
    if not m:
        # permitir sufixos (ex: "## Furadeira (Metodo)")
        pad2 = re.compile(
            rf"^##\s+{re.escape(titulo)}\b[^\n]*$", re.IGNORECASE | re.MULTILINE
        )
        m = pad2.search(texto)
    if not m:
        # permitir prefixo numerico (ex: "## 1. Tamanho de Mercado")
        pad3 = re.compile(
            rf"^##\s+[\d.]+\s+{re.escape(titulo)}\b[^\n]*$", re.IGNORECASE | re.MULTILINE
        )
        m = pad3.search(texto)
    if not m:
        return ""
    inicio = m.end()
    fim_match = _H2_RE.search(texto, pos=inicio)
    fim = fim_match.start() if fim_match else len(texto)
    return texto[inicio:fim].strip()


def extrair_subsecao(texto: str, titulo: str) -> str:
    """Extrai conteudo entre H3 titulo e proximo H3 ou H2."""
    if not texto:
        return ""
    pad = re.compile(
        rf"^###\s+{re.escape(titulo)}\s*$", re.IGNORECASE | re.MULTILINE
    )
    m = pad.search(texto)
    if not m:
        pad2 = re.compile(
            rf"^###\s+{re.escape(titulo)}\b[^\n]*$", re.IGNORECASE | re.MULTILINE
        )
        m = pad2.search(texto)
    if not m:
        return ""
    inicio = m.end()
    fim_match = re.search(r"^(?:##|###)\s", texto[inicio:], re.MULTILINE)
    fim = inicio + fim_match.start() if fim_match else len(texto)
    return texto[inicio:fim].strip()


def bullets(texto: str) -> list[str]:
    """Extrai itens de lista de bullets (- ou *) OU lista numerada (1., 2., ...)."""
    if not texto:
        return []
    out = []
    for linha in texto.splitlines():
        linha = linha.rstrip()
        m = re.match(r"^\s*[-*]\s+(.+?)\s*$", linha) \
            or re.match(r"^\s*\d+\.\s+(.+?)\s*$", linha)
        if m:
            out.append(m.group(1).strip())
    return out


def kv_bullets(texto: str) -> dict[str, str]:
    """Le bullets no formato '- **Chave:** valor' e retorna dict."""
    out: dict[str, str] = {}
    if not texto:
        return out
    for linha in texto.splitlines():
        m = re.match(r"^\s*[-*]\s+\*\*(.+?)\s*:\*\*\s*(.+?)\s*$", linha)
        if m:
            out[m.group(1).strip()] = m.group(2).strip()
    return out


def valor_label(texto: str, label: str) -> str:
    """Busca '**Label:** valor' (em bullet ou linha comum) e retorna valor."""
    if not texto:
        return ""
    pad = re.compile(
        rf"\*\*{re.escape(label)}\s*:\*\*\s*(.+?)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    m = pad.search(texto)
    return m.group(1).strip() if m else ""


def extrair_titulo_produto(perfil_texto: str, slug: str) -> str:
    """Reusa heuristica de painel-atualizar para descobrir nome amigavel."""
    nome_via_label = valor_label(perfil_texto, "Nome")
    if nome_via_label:
        return nome_via_label
    m = re.search(r"^#\s+(.+?)\s*$", perfil_texto, re.MULTILINE)
    if m:
        titulo = m.group(1).strip()
        for sep in (" \u2014 ", " \u2013 ", " - ", ": "):
            if sep in titulo:
                return titulo.split(sep, 1)[1].strip()
        if not titulo.lower().startswith("perfil"):
            return titulo
    return slug.replace("-", " ").title()


# ----- parsers por secao -----

def parse_quadro(perfil: str) -> dict:
    bloco = extrair_secao(perfil, "Quadro (Transformacao Principal)") \
        or extrair_secao(perfil, "Quadro")
    # primeiro paragrafo nao vazio
    texto = ""
    for linha in bloco.splitlines():
        if linha.strip():
            texto = linha.strip()
            break
    return {"quadro": texto}


def parse_furadeira(perfil: str, produto_dir: Path) -> dict:
    bloco = extrair_secao(perfil, "Furadeira (Metodo)") \
        or extrair_secao(perfil, "Furadeira")
    nome_metodo = valor_label(bloco, "Nome do Metodo") or valor_label(bloco, "Nome do Método")
    mecanica = ""
    eficiencia = ""

    macro = []
    for m in re.finditer(
        r"^\d+\.\s+\*\*(.+?)\*\*\s*\.?\s*(.+?)$",
        bloco,
        re.MULTILINE,
    ):
        macro.append({"titulo": m.group(1).strip(), "descricao": m.group(2).strip()})

    # checa existencia da imagem PNG (gerada por /furadeira-visual)
    furadeira_png = ""
    png_path = produto_dir / "entregas" / "furadeira" / "furadeira.png"
    if png_path.exists():
        furadeira_png = "entregas/furadeira/furadeira.png"

    return {
        "nome_metodo": nome_metodo,
        "mecanica": mecanica,
        "eficiencia": eficiencia,
        "macroetapas": macro,
        "furadeira_png": furadeira_png,
    }


def parse_decorados(perfil: str) -> dict:
    bloco = extrair_secao(perfil, "Decorados (Beneficios)") \
        or extrair_secao(perfil, "Decorados")
    categorias: dict[str, list[str]] = {}
    for cat in ["Financeiro", "Tempo", "Autoestima", "Reputacao", "Reputação", "Crescimento"]:
        itens = bullets(extrair_subsecao(bloco, cat))
        if itens:
            key = "Reputacao" if cat in ("Reputação", "Reputacao") else cat
            categorias[key] = itens
    return {"decorados": categorias}


def parse_urgencias(perfil: str) -> dict:
    bloco = extrair_secao(perfil, "Urgencias Ocultas") \
        or extrair_secao(perfil, "Urgências Ocultas")
    mapa = [
        ("Dores", ["Dores", "Dores (o que incomoda)"]),
        ("Duvidas", ["Duvidas", "Dúvidas", "Duvidas (o que pergunta)", "Dúvidas (o que pergunta)"]),
        ("Desejos", ["Desejos", "Desejos (o que sonha)"]),
        ("Assuntos Relacionados", ["Assuntos Relacionados", "Assuntos Relacionados (o que interessa)"]),
        ("Urgencias Quentes", ["Urgencias Quentes", "Urgências Quentes", "Urgencias Quentes (alta intencao)", "Urgências Quentes (alta intenção)"]),
        ("Urgencias Frias", ["Urgencias Frias", "Urgências Frias", "Urgencias Frias (atracao)", "Urgências Frias (atração)"]),
        ("Urgencias Inusitadas", ["Urgencias Inusitadas", "Urgências Inusitadas", "Urgencias Inusitadas (angulo diferente)", "Urgências Inusitadas (ângulo diferente)"]),
    ]
    out: dict[str, list[str]] = {}
    for chave, variantes in mapa:
        for v in variantes:
            itens = bullets(extrair_subsecao(bloco, v))
            if itens:
                out[chave] = itens
                break
    return {"urgencias": out}


def parse_identidade_produto(perfil: str) -> dict:
    ip = extrair_secao(perfil, "Identidade do Produto")
    kv = kv_bullets(ip)
    args = bullets(extrair_secao(perfil, "Argumentos Incontestaveis") or extrair_secao(perfil, "Argumentos Incontestáveis"))
    return {
        "diferencial": kv.get("Diferencial", ""),
        "formato": kv.get("Formato", ""),
        "nome": kv.get("Nome", ""),
        "preco": kv.get("Preco", "") or kv.get("Preço", ""),
        "argumentos_incontestaveis": args,
        "objecoes": [],
    }


_ORDEM_ARGS = [
    "Argumento Incontestavel",
    "Argumento Logico",
    "Argumento por Analogia",
    "Argumento por Exemplificacao",
    "Argumento de Valor",
    "Argumento de Consequencia",
    "Argumento de Contradicao",
]


def parse_objecoes_do_idconsumidor(idc_texto: str | None) -> list[dict]:
    if not idc_texto:
        return []
    bloco = extrair_secao(idc_texto, "Objecoes de Compra (Framework dos 7 Argumentos)") \
        or extrair_secao(idc_texto, "Objeções de Compra (Framework dos 7 Argumentos)") \
        or extrair_secao(idc_texto, "Objecoes de Compra") \
        or extrair_secao(idc_texto, "Objeções de Compra") \
        or extrair_secao(idc_texto, "Objecoes") \
        or extrair_secao(idc_texto, "Objeções")
    if not bloco:
        return []
    # Divide em objecoes via H3 "Objecao N:"
    objecoes = []
    partes = re.split(
        r"^###\s+Obje[cç][aã]o\s+\d+:\s*(.+?)\s*$",
        bloco,
        flags=re.MULTILINE,
    )
    # partes alterna: [prefixo, texto_obj_1, corpo_obj_1, texto_obj_2, corpo_obj_2, ...]
    for i in range(1, len(partes), 2):
        texto_obj = partes[i].strip()
        corpo = partes[i + 1] if i + 1 < len(partes) else ""
        argumentos = []
        # cada argumento comeca com **N. Nome...**
        blocos_arg = re.split(r"^\*\*(\d+)\.\s+([^\n]+?)\*\*\s*$", corpo, flags=re.MULTILINE)
        for j in range(1, len(blocos_arg), 3):
            titulo = f"{blocos_arg[j]}. {blocos_arg[j + 1].strip()}"
            corpo_arg = blocos_arg[j + 2] if j + 2 < len(blocos_arg) else ""
            paragrafos = [p.strip() for p in re.split(r"\n\s*\n", corpo_arg) if p.strip()]
            # remove paragrafos que sao na verdade marcadores
            paragrafos = [re.sub(r"^\[|\]$", "", p) for p in paragrafos if not p.startswith("###")]
            argumentos.append({"titulo": titulo.upper(), "paragrafos": paragrafos})
        objecoes.append({"texto": texto_obj, "argumentos": argumentos})
    return objecoes


def parse_identidade_consumidor(perfil: str, idc: str) -> dict:
    fonte = idc or perfil
    # Para quem e
    para_quem = ""
    pq_bloco = extrair_secao(fonte, "Para Quem E") or extrair_secao(fonte, "Para Quem É")
    if pq_bloco:
        # primeira frase entre aspas ou primeiro paragrafo significativo
        for p in re.split(r"\n\s*\n", pq_bloco):
            p = p.strip()
            if p:
                para_quem = p.strip('"\'')
                break

    # Perfil demografico vem do bloco "Identidade do Consumidor" no idconsumidor ou no perfil
    ic_bloco = extrair_secao(idc, "Identidade do Consumidor")
    if not ic_bloco:
        ic_bloco = extrair_secao(perfil, "Identidade do Consumidor")
    # Extrai pares chave-valor no formato inline: **Chave:** valor | **Chave2:** valor2
    kv: dict[str, str] = {}
    for linha in (ic_bloco or "").splitlines():
        for mi in re.finditer(r"\*\*(.+?)\s*:\*\*\s*(.+?)(?=\s*\|\s*\*\*|\s*$)", linha):
            k = mi.group(1).strip()
            v = mi.group(2).strip().rstrip("|").strip()
            if k not in kv:
                kv[k] = v
    # Complementa com bullets no formato padrao: - **Chave:** valor
    for k, v in kv_bullets(ic_bloco).items():
        if k not in kv:
            kv[k] = v

    perfil_demo = {
        "Idade": kv.get("Idade", ""),
        "Genero": kv.get("Genero", "") or kv.get("Gênero", ""),
        "Profissao": kv.get("Profissao", "") or kv.get("Profissão", ""),
        "Renda": kv.get("Renda", ""),
        "Localizacao": kv.get("Localizacao", "") or kv.get("Localização", ""),
        "Nivel de consciencia": kv.get("Nivel de consciencia", "")
            or kv.get("Nível de consciência", ""),
    }
    comportamento = {
        "Onde busca info": kv.get("Onde busca informacao", "") or kv.get("Onde busca informação", ""),
        "Comportamento": kv.get("Comportamento", ""),
        "Objecoes": kv.get("Objecoes tipicas", "") or kv.get("Objeções típicas", ""),
    }

    # paliativos
    paliativos = bullets(
        extrair_secao(
            idc,
            "Paliativos (somente Middle Ticket - ferramentas e solucoes concorrentes do mercado que resolvem o problema parcialmente)",
        )
        or extrair_secao(idc, "Paliativos")
    )

    # sonho
    sonho = (extrair_secao(idc, "Sonho") or "").strip().strip('"').strip("'")

    # frases que a pessoa diria
    frases_bloco = extrair_secao(idc, "Frases que essa pessoa diria") or ""
    frases = bullets(frases_bloco)
    if not frases:
        frases = [
            re.sub(r"^\d+\.\s+\"?", "", ln).strip().strip('"')
            for ln in frases_bloco.splitlines()
            if re.match(r"^\d+\.\s+", ln.strip())
        ]

    # baldes — suporta dois formatos:
    # 1) formato original: seta Pra quem e - Nome\n1. item...
    # 2) formato novo: **Balde N – Nome**\nDescricao paragraph
    baldes = []
    if idc:
        baldes_txt = (
            extrair_secao(idc, "Baldes de Para Quem E")
            or extrair_secao(idc, "Baldes de Para Quem \u00c9")
            or ""
        )
        if not baldes_txt:
            # busca flexivel: qualquer H2 que contenha "Baldes"
            m_sec = re.search(r"^##[^\n]*Baldes[^\n]*$", idc, re.MULTILINE | re.IGNORECASE)
            if not m_sec:
                m_sec = re.search(
                    r"^##\s+Para quem[^\n]+\([^\n]*Baldes[^\n]*\)\s*$",
                    idc,
                    re.MULTILINE | re.IGNORECASE,
                )
            if m_sec:
                inicio = m_sec.end()
                fim_m = _H2_RE.search(idc, pos=inicio)
                baldes_txt = idc[inicio: fim_m.start() if fim_m else len(idc)].strip()

        if baldes_txt:
            # formato 1: seta + "Pra quem \u00e9" + separador (- ou \u2014 ou \u2013 ou :) + nome + itens numerados
            for m in re.finditer(
                r"[\u27a4\u279c\u27a2]\s*Pra quem [e\u00e9]\s*[-\u2013\u2014:]\s*(.+?)\n\n?((?:\d+\.\s+[^\n]+\n?)+)",
                baldes_txt,
                re.IGNORECASE,
            ):
                nome = m.group(1).strip().strip("[]")
                itens = [
                    re.sub(r"^\d+\.\s+", "", ln).strip()
                    for ln in m.group(2).splitlines()
                    if ln.strip()
                ]
                baldes.append({"nome": nome, "descricao": "", "itens": itens})

            # formato 2: **Balde N – Nome**\nDescricao
            if not baldes:
                for m in re.finditer(
                    r"\*\*Balde\s+\d+\s*[-\u2013\u2014]\s*(.+?)\*\*\n+(.+?)(?=\n\n\*\*Balde|\Z)",
                    baldes_txt,
                    re.DOTALL,
                ):
                    nome = m.group(1).strip()
                    descricao = m.group(2).strip()
                    baldes.append({"nome": nome, "descricao": descricao, "itens": []})

            # formato 3: ### Balde N: Nome (gerado pelo gerador-idconsumidor)
            if not baldes:
                for m in re.finditer(
                    r"^###\s+Balde\s+\d+:\s*(.+?)\s*$\n+(.*?)(?=^###\s+Balde\s+\d+:|\Z)",
                    baldes_txt,
                    re.MULTILINE | re.DOTALL,
                ):
                    nome = m.group(1).strip()
                    corpo = m.group(2).strip()
                    desc_m = re.search(
                        r"\*\*Descri[cç][aã]o:\*\*\s*(.+?)(?=\n\n|\*\*Como|\Z)",
                        corpo,
                        re.DOTALL,
                    )
                    if desc_m:
                        descricao = desc_m.group(1).strip()
                    else:
                        descricao = ""
                        for p in re.split(r"\n\s*\n", corpo):
                            p = p.strip()
                            if p and not p.startswith("**Como"):
                                descricao = p
                                break
                    baldes.append({"nome": nome, "descricao": descricao, "itens": []})
    return {
        "para_quem_e": para_quem,
        "perfil_demo": {k: v for k, v in perfil_demo.items() if v},
        "comportamento": {k: v for k, v in comportamento.items() if v},
        "paliativos": paliativos,
        "sonho": sonho,
        "frases": frases,
        "baldes": baldes,
    }


def parse_identidade_comunicador(perfil: str, idc: str) -> dict:
    bloco = extrair_secao(perfil, "Identidade do Comunicador")
    kv = kv_bullets(bloco)

    def _listar(valor: str) -> list[str]:
        if not valor:
            return []
        partes = re.split(r"[,;]\s*|\s*\|\s*", valor)
        return [p.strip() for p in partes if p.strip()]

    def _listar_frases(valor: str) -> list[str]:
        """Divide por | ou ; mas nunca por vírgula (mantras podem ter vírgulas internas)."""
        if not valor:
            return []
        partes = re.split(r"\s*[|;]\s*|\n+", valor)
        return [p.strip().strip('"\'') for p in partes if p.strip().strip('"\'')]

    # regex tolerante com bold markers (**Key:** ou Key:)
    _KV_RE = r"^[-*]\s+\*{{0,2}}{chave}\*{{0,2}}\s*:\*{{0,2}}\s*(.+?)$"

    comunicar_idc = extrair_secao(idc, "Como se Comunicar")
    conectam = []
    afastam = []
    if comunicar_idc:
        m_c = re.search(
            _KV_RE.format(chave="Palavras que conectam"),
            comunicar_idc,
            re.MULTILINE | re.IGNORECASE,
        )
        m_a = re.search(
            _KV_RE.format(chave="Palavras que afastam"),
            comunicar_idc,
            re.MULTILINE | re.IGNORECASE,
        )
        if m_c:
            conectam = _listar(m_c.group(1))
        if m_a:
            afastam = _listar(m_a.group(1))

    if not conectam:
        conectam = _listar(kv.get("Vocabulario base", "") or kv.get("Vocabulário base", ""))
    if not afastam:
        afastam = _listar(kv.get("Evitar na comunicacao", "") or kv.get("Evitar na comunicação", ""))

    return {
        "nome": kv.get("Nome", ""),
        "especialidade": kv.get("Especialidade", ""),
        "valores": _listar(kv.get("Valores", "")),
        "mantras": _listar_frases(kv.get("Mantras/Jargoes proprios", "")
                                   or kv.get("Mantras/Jargões próprios", "")),
        "formatos": _listar(kv.get("Formatos que combinam mais", "")),
        "elementos_visuais": _listar(kv.get("Elementos visuais recomendados", "")),
        "tom_de_voz": kv.get("Tom de voz", ""),
        "posicionamento": kv.get("Posicionamento pessoal", ""),
        "palavras_conectam": conectam,
        "palavras_afastam": afastam,
    }


def parse_youtube_rich(sec_yt: str) -> list[dict]:
    """Parse formato ### Vídeo X em lista de dicts ricos (comentarios, thumbnail, lacuna)."""
    videos = []
    blocks = re.split(r'\n###\s+V[íi]deo\s+\d+', "\n" + sec_yt, flags=re.IGNORECASE)
    for block in blocks:
        if not block.strip():
            continue
        v: dict = {}
        m = re.search(r'\*\*T[ií]tulo:\*\*\s*(.+)', block)
        v["titulo"] = m.group(1).strip() if m else ""
        m = re.search(r'\*\*Canal:\*\*\s*(.+)', block)
        v["canal"] = m.group(1).strip() if m else ""
        m = re.search(r'\*\*Link:\*\*\s*(https?://\S+)', block)
        v["link"] = m.group(1).strip().rstrip(").,") if m else ""
        m = re.search(r'\*\*Visualiza[çc][oõ]es:\*\*\s*(.+)', block, re.IGNORECASE)
        v["views"] = m.group(1).strip() if m else ""
        m = re.search(r'\*\*Data de publica[çc][aã]o:\*\*\s*(.+)', block, re.IGNORECASE)
        v["data"] = m.group(1).strip() if m else ""
        m = re.search(r'\*\*[Âa]ngulo.*?:\*\*\s*(.+)', block)
        v["angulo"] = m.group(1).strip() if m else ""
        m = re.search(r'\*\*Lacuna.*?:\*\*\s*(.+)', block)
        v["lacuna"] = m.group(1).strip() if m else ""
        v["comentarios"] = [c.strip() for c in re.findall(r'"([^"]{10,200})"', block)][:5]
        thumb: dict = {}
        for field, pat in [
            ("cores", r'- \*?Cores[:\*]*\s*(.+)'),
            ("expressao", r'- \*?Express[aã]o[:\*]*\s*(.+)'),
            ("texto", r'- \*?Texto em destaque[:\*]*\s*(.+)'),
            ("elementos", r'- \*?Elementos visuais[:\*]*\s*(.+)'),
            ("composicao", r'- \*?Composi[çc][aã]o[:\*]*\s*(.+)'),
        ]:
            m2 = re.search(pat, block, re.IGNORECASE)
            if m2:
                thumb[field] = m2.group(1).strip()
        v["thumbnail"] = thumb
        if v["titulo"] or v["canal"]:
            videos.append(v)
    return videos


def parse_pesquisa(texto: str) -> dict:
    """Extracao pragmatica: os campos mais comuns de pesquisa-mercado.md.
    Estrutura do arquivo varia, entao usamos heuristicas tolerantes."""
    if not texto:
        return {}

    tamanho = (
        valor_label(texto, "Tamanho do mercado")
        or valor_label(texto, "Tamanho estimado")
    )
    crescimento = valor_label(texto, "Crescimento") or valor_label(texto, "Crescimento anual")
    ticket = valor_label(texto, "Ticket medio") or valor_label(texto, "Ticket médio")

    # Fallbacks para formato numerado (## 1. Tamanho de Mercado, ## 3. Faixa de Preço, etc.)
    _sec_tam = ""
    if not tamanho:
        _sec_tam = (
            extrair_secao(texto, "Tamanho de Mercado")
            or extrair_secao(texto, "Tamanho do Mercado")
        )
        if _sec_tam:
            m_val = re.search(
                r"((?:USD|R\$)\s*[\d,.]+\s*(?:bi(?:lh[aã]o(?:es)?)?|milh[aã]o|tri)?)",
                _sec_tam, re.IGNORECASE,
            )
            tamanho = m_val.group(1).strip() if m_val else (bullets(_sec_tam) or [""])[0][:50]
    if not crescimento:
        _sec_t = _sec_tam or extrair_secao(texto, "Tamanho de Mercado") or ""
        m_cagr = re.search(r"CAGR\s+de\s+([\d,.]+%?)", _sec_t, re.IGNORECASE)
        if m_cagr:
            crescimento = "+" + m_cagr.group(1) + " a.a."
        else:
            m_pct = re.search(r"crescendo?\s+(?:a\s+)?([\d,.]+%)", _sec_t, re.IGNORECASE)
            if m_pct:
                crescimento = "+" + m_pct.group(1) + " a.a."
    if not ticket:
        _sec_prec = (
            extrair_secao(texto, "Faixa de Preço Praticada")
            or extrair_secao(texto, "Faixa de Preco Praticada")
            or extrair_secao(texto, "Preço Praticado")
            or extrair_secao(texto, "Precos Praticados")
        )
        if _sec_prec:
            m_merc = re.search(r"[Mm]ercado principal[^:]*:\s*([^\n]+)", _sec_prec)
            if m_merc:
                ticket = re.sub(r"\s*\(.*?\)", "", m_merc.group(1))
                ticket = re.sub(r"[\*_`]", "", ticket).strip()[:50]
            else:
                m_prec = re.search(r"R\$\s*[\d,.]+(?:\s+a\s+R\$\s*[\d,.]+)?", _sec_prec)
                ticket = m_prec.group(0) if m_prec else ""

    # Oportunidades
    opo_bloco = (
        extrair_secao(texto, "Oportunidades Identificadas")
        or extrair_secao(texto, "Oportunidades")
        or extrair_subsecao(texto, "Oportunidades de posicionamento")
    )
    oportunidades = bullets(opo_bloco) if opo_bloco else []
    if not oportunidades:
        _angulo = (
            extrair_secao(texto, "Ângulo Estratégico Recomendado")
            or extrair_secao(texto, "Angulo Estrategico Recomendado")
            or extrair_secao(texto, "Ângulo Estratégico")
            or extrair_secao(texto, "Angulo Estrategico")
        )
        if _angulo:
            oportunidades = [
                s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", _angulo)
                if len(s.strip()) > 20
            ][:7]

    # Cuidados
    cuidados_bloco = (
        extrair_secao(texto, "Cuidados e Riscos")
        or extrair_secao(texto, "Alertas e Riscos")
        or extrair_secao(texto, "Cuidados")
        or extrair_secao(texto, "Riscos Regulatórios")
        or extrair_secao(texto, "Riscos Regulatorios")
        or extrair_secao(texto, "Riscos")
    )
    cuidados = bullets(cuidados_bloco) if cuidados_bloco else []

    # Reclame Aqui
    rec_bloco = (
        extrair_secao(texto, "Reclame Aqui")
        or extrair_secao(texto, "Padroes de Reclamacao")
        or extrair_secao(texto, "Reclamacoes")
        or extrair_secao(texto, "Reclamações")
        or extrair_secao(texto, "Objeções Reais")
        or extrair_secao(texto, "Objecoes Reais")
    )
    # fallback: subseção dentro de Objeções Reais com título Reclame Aqui
    if not rec_bloco:
        m_obj = re.search(
            r'^##[^\n]*Obje[çc][õo]es Reais[^\n]*\n(.*?)(?=^##\s|\Z)',
            texto, re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if m_obj:
            objecoes_bloco = m_obj.group(1)
            rec_bloco = (
                extrair_subsecao(objecoes_bloco, "Levantamento do Reclame Aqui")
                or extrair_subsecao(objecoes_bloco, "Reclame Aqui")
            )
    reclamacoes = bullets(rec_bloco) if rec_bloco else []

    # Concorrentes: busca a primeira tabela markdown
    concorrentes = parse_tabela_concorrentes(texto)

    # Fontes
    fontes_bloco = extrair_secao(texto, "Fontes") or extrair_secao(texto, "Fontes Consultadas")
    fontes = bullets(fontes_bloco) if fontes_bloco else []

    # YouTube top 10 — tenta formato rico ### Vídeo X primeiro
    sec_yt = (
        extrair_secao(texto, "Top 10 Vídeos")
        or extrair_secao(texto, "Top 10 Videos")
        or extrair_secao(texto, "Top 10 YouTube")
        or extrair_secao(texto, "YouTube")
    )
    # fallback: header ## N. YouTube... (padrão da skill pesquisa-mercado)
    if not sec_yt:
        m_yt = re.search(
            r'^##[^\n]*YouTube[^\n]*\n(.*?)(?=^##\s|\Z)',
            texto, re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if m_yt:
            sec_yt = m_yt.group(1).strip()
    youtube: list[dict] = []
    if sec_yt:
        rich = parse_youtube_rich(sec_yt)
        if rich:
            youtube = rich
        else:
            # fallback: bullets simples (cada item é um título de vídeo)
            _yt_empty = {"canal": "", "link": "", "views": "", "data": "",
                         "angulo": "", "lacuna": "", "comentarios": [], "thumbnail": {}}
            youtube = [dict(_yt_empty, titulo=t) for t in bullets(sec_yt)[:10]]

    # Público-Alvo Real (seção ## 4. Público-Alvo Real)
    sec_publico = (
        extrair_secao(texto, "4. Público-Alvo Real")
        or extrair_secao(texto, "4. Publico-Alvo Real")
        or extrair_secao(texto, "Público-Alvo Real")
        or extrair_secao(texto, "Publico-Alvo Real")
    )
    if not sec_publico:
        m_pa = re.search(
            r'^##[^\n]*P[uú]blico[- ]Alvo[^\n]*\n(.*?)(?=^##\s|\Z)',
            texto, re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if m_pa:
            sec_publico = m_pa.group(1).strip()
    publico_alvo: dict = {}
    if sec_publico:
        demo = bullets(extrair_subsecao(sec_publico, "Demografic") or extrair_subsecao(sec_publico, "Perfil"))
        comport = bullets(extrair_subsecao(sec_publico, "Comportamento") or extrair_subsecao(sec_publico, "Comportamental"))
        consci = bullets(
            extrair_subsecao(sec_publico, "Consciência")
            or extrair_subsecao(sec_publico, "Nivel de Consciencia")
            or extrair_subsecao(sec_publico, "Schwartz")
        )
        publico_alvo = {"demo": demo, "comportamento": comport, "consciencia": consci}
        if not any(publico_alvo.values()):
            publico_alvo = {"raw": bullets(sec_publico)}

    # Assuntos Quentes e Ângulos Virais (seção 6)
    sec_assuntos = (
        extrair_secao(texto, "6. Assuntos Quentes e Ângulos Virais")
        or extrair_secao(texto, "Assuntos Quentes e Ângulos Virais")
        or extrair_secao(texto, "Assuntos Quentes")
        or extrair_secao(texto, "Assuntos Virais")
        or extrair_secao(texto, "Tendências")
    )
    if not sec_assuntos:
        m_aq = re.search(
            r'^##[^\n]*(?:Assuntos Quentes|Assuntos Virais|Tend[êe]ncias)[^\n]*\n(.*?)(?=^##\s|\Z)',
            texto, re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if m_aq:
            sec_assuntos = m_aq.group(1).strip()
    assuntos_quentes: dict = {}
    if sec_assuntos:
        termos_sub = extrair_subsecao(sec_assuntos, "Termos em alta") or extrair_subsecao(sec_assuntos, "Termos em Alta")
        virais_sub = extrair_subsecao(sec_assuntos, "Conteúdos virais recentes") or extrair_subsecao(sec_assuntos, "Conteudos virais recentes")
        ganchos_sub = extrair_subsecao(sec_assuntos, "Ganchos que estão performando") or extrair_subsecao(sec_assuntos, "Ganchos")
        def _bullets_e_numerados(txt: str) -> list[str]:
            out = []
            for ln in txt.splitlines():
                ln = ln.rstrip()
                m = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.+?)\s*$", ln)
                if m:
                    out.append(m.group(1).strip())
            return out
        assuntos_quentes = {
            "termos": bullets(termos_sub) if termos_sub else [],
            "virais": _bullets_e_numerados(virais_sub) if virais_sub else [],
            "ganchos": bullets(ganchos_sub) if ganchos_sub else [],
        }
        # fallback: seção plana sem subseções — trata todos os bullets como virais
        if not any(assuntos_quentes.values()):
            assuntos_quentes = {
                "termos": [],
                "virais": _bullets_e_numerados(sec_assuntos),
                "ganchos": [],
            }

    # Biblioteca de Anúncios (seção 8)
    sec_bibl = (
        extrair_secao(texto, "8. Biblioteca de Anúncios (insights)")
        or extrair_secao(texto, "Biblioteca de Anúncios")
        or extrair_secao(texto, "Biblioteca de Anuncios")
    )
    if not sec_bibl:
        m_bibl = re.search(
            r'^##[^\n]*Biblioteca de An[uú]ncios[^\n]*\n(.*?)(?=^##\s|\Z)',
            texto, re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if m_bibl:
            sec_bibl = m_bibl.group(1).strip()
    biblioteca_anuncios: dict = {}
    if sec_bibl:
        headlines_sub = extrair_subsecao(sec_bibl, "Padrões de headline") or extrair_subsecao(sec_bibl, "Padroes de headline")
        oferta_sub = extrair_subsecao(sec_bibl, "Padrões de oferta") or extrair_subsecao(sec_bibl, "Padroes de oferta")
        criativos_sub = extrair_subsecao(sec_bibl, "Criativos ativos no nicho") or extrair_subsecao(sec_bibl, "Criativos ativos")
        obs_sub = extrair_subsecao(sec_bibl, "Observações") or extrair_subsecao(sec_bibl, "Observacoes")
        biblioteca_anuncios = {
            "headlines": bullets(headlines_sub) if headlines_sub else [],
            "padroes_oferta": bullets(oferta_sub) if oferta_sub else [],
            "criativos": bullets(criativos_sub) if criativos_sub else [],
            "observacoes": bullets(obs_sub) if obs_sub else [],
        }
        # fallback: seção plana sem subseções — bullets viram headlines
        if not any(biblioteca_anuncios.values()):
            biblioteca_anuncios = {
                "headlines": bullets(sec_bibl),
                "padroes_oferta": [], "criativos": [], "observacoes": [],
            }

    return {
        "tamanho_mercado": tamanho,
        "crescimento": crescimento,
        "ticket_medio": ticket,
        "oportunidades": oportunidades,
        "cuidados": cuidados,
        "reclamacoes": reclamacoes,
        "concorrentes": concorrentes,
        "fontes": fontes,
        "youtube": youtube,
        "publico_alvo": publico_alvo,
        "assuntos_quentes": assuntos_quentes,
        "biblioteca_anuncios": biblioteca_anuncios,
    }


def parse_tabela_concorrentes(texto: str) -> list[dict]:
    """Extrai tabelas markdown que contenham concorrentes. Tolerante a variacoes."""
    out: list[dict] = []
    # localiza blocos de tabela simples
    tabelas = re.findall(
        r"(^\|.+\|\s*\n\|[\s\-:\|]+\|\s*\n(?:\|.+\|\s*\n?)+)",
        texto,
        re.MULTILINE,
    )
    for tab in tabelas:
        linhas = [ln.strip() for ln in tab.strip().splitlines() if ln.strip().startswith("|")]
        if len(linhas) < 2:
            continue
        header = [c.strip().lower() for c in linhas[0].strip("|").split("|")]
        # heuristica: precisa ter alguma coluna de nome/concorrente/produto
        if not any("nome" in h or "concorrente" in h or "marca" in h or "produto" in h for h in header):
            continue
        col_nome = next((i for i, h in enumerate(header) if "nome" in h or "concorrente" in h or "marca" in h or "produto" in h), 0)
        col_insta = next((i for i, h in enumerate(header) if "instagram" in h or "insta" in h), None)
        col_pagina = next((i for i, h in enumerate(header) if "pagina" in h or "página" in h or "site" in h or "link" in h), None)
        col_preco = next((i for i, h in enumerate(header) if "preco" in h or "preço" in h or "valor" in h), None)
        col_promessa = next((i for i, h in enumerate(header) if "promessa" in h), None)
        col_formato = next((i for i, h in enumerate(header) if "formato" in h), None)
        col_diferencial = next((i for i, h in enumerate(header) if "diferencial" in h), None)

        for linha in linhas[2:]:
            celulas = [c.strip() for c in linha.strip("|").split("|")]
            if len(celulas) <= col_nome or not celulas[col_nome]:
                continue
            def _cel(idx):
                if idx is None or idx >= len(celulas):
                    return ""
                return _limpa_link(celulas[idx])
            out.append({
                "nome": _limpa_texto(celulas[col_nome]),
                "promessa": _limpa_texto(_cel(col_promessa)),
                "formato": _limpa_texto(_cel(col_formato)),
                "preco": _limpa_texto(_cel(col_preco)),
                "diferencial": _limpa_texto(_cel(col_diferencial)),
                "pagina": _extrai_url(_cel(col_pagina)),
                "instagram": _extrai_url(_cel(col_insta)),
            })
        if out:
            break  # primeira tabela valida e suficiente
    # fallback: concorrentes em prosa com headings **Nome** dentro de seção Concorrentes
    if not out:
        m_conc = re.search(
            r'^##[^\n]*Concorrentes?[^\n]*\n(.*?)(?=^##\s|\Z)',
            texto, re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if m_conc:
            bloco = m_conc.group(1)
            for m in re.finditer(r'^\*\*([^*\n]{3,80})\*\*\s*$', bloco, re.MULTILINE):
                nome = m.group(1).strip()
                preco = ""
                pos = m.end()
                preco_m = re.search(
                    r'[-*]\s*Pre[çc]o[:\s]+([^\n]+)',
                    bloco[pos:pos + 400],
                    re.IGNORECASE,
                )
                if preco_m:
                    preco = _limpa_texto(preco_m.group(1))
                out.append({
                    "nome": nome, "promessa": "", "formato": "",
                    "preco": preco, "diferencial": "", "pagina": "", "instagram": "",
                })
    return out


def _limpa_texto(s: str) -> str:
    if not s:
        return ""
    # remove markdown simples
    return re.sub(r"[\*_`]", "", s).strip()


def _limpa_link(s: str) -> str:
    return s.strip()


def _extrai_url(s: str) -> str:
    if not s:
        return ""
    m = re.search(r"\[.*?\]\((https?://[^\s)]+)\)", s)
    if m:
        return m.group(1)
    m2 = re.search(r"https?://\S+", s)
    if m2:
        return m2.group(0).rstrip("),.")
    return s.strip() if s.startswith("http") else ""


def parse_dashboards(produto_dir: Path) -> dict:
    """Detecta quais dashboards HTML existem e le usernames do .env."""
    env_path = REPO_ROOT / ".env"
    env_vars: dict[str, str] = {}
    if env_path.exists():
        for linha in env_path.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if "=" in linha and not linha.startswith("#"):
                k, _, v = linha.partition("=")
                env_vars[k.strip()] = v.strip()

    plataformas = []

    def _achar_dashboard(pasta: str, preferido: str = "") -> str:
        """Retorna o caminho relativo ao produto_dir do dashboard.html encontrado.
        Se `preferido` for informado, tenta primeiro a subpasta com esse nome."""
        base = produto_dir / "entregas" / pasta
        if not base.exists():
            return ""
        direto = base / "dashboard.html"
        if direto.exists():
            return f"entregas/{pasta}/dashboard.html"
        if preferido:
            cand = base / preferido / "dashboard.html"
            if cand.exists():
                return f"entregas/{pasta}/{preferido}/dashboard.html"
        for sub in sorted(base.iterdir()):
            if sub.is_dir():
                candidato = sub / "dashboard.html"
                if candidato.exists():
                    return f"entregas/{pasta}/{sub.name}/dashboard.html"
        return ""

    def _handle_do_caminho(caminho_rel: str) -> str:
        """Extrai o handle de `entregas/{pasta}/{handle}/dashboard.html`."""
        partes = caminho_rel.split("/")
        return partes[2] if len(partes) >= 4 else ""

    def _extrair_metricas_cmp(caminho_rel: str) -> dict:
        """Le insights.json da plataforma e devolve dict compacto pra comparacao.
        Inline assim, evita fetch via file:// que e bloqueado pelo browser."""
        import json as _json
        if not caminho_rel:
            return {}
        insights_path = produto_dir / caminho_rel.replace("dashboard.html", "insights.json")
        if not insights_path.exists():
            return {}
        try:
            data = _json.loads(insights_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

        perfil = data.get("perfil") or data.get("canal") or {}
        metricas = data.get("metricas") or {}
        posts = data.get("posts") or data.get("videos") or []

        # Top 3 por engajamento, so campos essenciais
        top3 = sorted(posts, key=lambda p: p.get("engajamento", 0), reverse=True)[:3]
        top3_slim = [
            {
                "tipo": p.get("tipo", "-"),
                "texto": (p.get("texto") or p.get("legenda") or p.get("titulo") or "")[:120],
                "likes": p.get("likes") or p.get("numLikes") or 0,
                "engajamento": p.get("engajamento", 0),
                "views": p.get("views") or p.get("numViews") or 0,
            }
            for p in top3
        ]

        # Fallback: se nao tiver bloco "metricas" no insights.json (caso do Instagram),
        # computa as basicas a partir dos posts.
        from collections import Counter as _Counter
        media_eng = metricas.get("media_engajamento")
        if media_eng is None and posts:
            engs = [p.get("engajamento", 0) for p in posts]
            media_eng = round(sum(engs) / len(engs), 2) if engs else 0

        tipo_top = metricas.get("tipo_mais_postado") or metricas.get("tipo_top")
        if not tipo_top and posts:
            tipos_cnt = _Counter(p.get("tipo", "-") for p in posts)
            tipo_top = tipos_cnt.most_common(1)[0][0] if tipos_cnt else "-"

        desempenho_tipo = metricas.get("desempenho_por_tipo") or metricas.get("desempenho_tipo") or {}
        if not desempenho_tipo and posts:
            # Agrupa engajamento por tipo
            grupos: dict = {}
            for p in posts:
                t = p.get("tipo", "-")
                grupos.setdefault(t, []).append(p.get("engajamento", 0))
            desempenho_tipo = {
                t: {"engajamento": round(sum(es) / len(es), 2), "count": len(es)}
                for t, es in grupos.items()
            }

        return {
            "seguidores": perfil.get("seguidores") or perfil.get("followersCount") or 0,
            "conexoes": perfil.get("conexoes") or 0,
            "inscritos": perfil.get("inscritos") or 0,
            "likes_totais": perfil.get("likes_totais") or 0,
            "total_views": perfil.get("total_views") or perfil.get("total_views_canal") or 0,
            "media_engajamento": media_eng or 0,
            "tipo_mais_postado": tipo_top or "-",
            "total_posts": len(posts),
            "desempenho_por_tipo": desempenho_tipo,
            "desempenho_por_duracao": metricas.get("desempenho_por_duracao") or metricas.get("desempenho_duracao") or {},
            "top3": top3_slim,
        }

    ig_caminho = _achar_dashboard("instagram-dashboard", env_vars.get("IG_USER", ""))
    if ig_caminho:
        user = env_vars.get("IG_USER", "") or _handle_do_caminho(ig_caminho)
        plataformas.append({
            "id": "instagram",
            "label": "Instagram",
            "user": f"@{user}" if user else "",
            "caminho": ig_caminho,
            "metricas_cmp": _extrair_metricas_cmp(ig_caminho),
        })

    tt_caminho = _achar_dashboard("tiktok-dashboard", env_vars.get("TIKTOK_USER", ""))
    if tt_caminho:
        user = env_vars.get("TIKTOK_USER", "") or _handle_do_caminho(tt_caminho)
        plataformas.append({
            "id": "tiktok",
            "label": "TikTok",
            "user": f"@{user}" if user else "",
            "caminho": tt_caminho,
            "metricas_cmp": _extrair_metricas_cmp(tt_caminho),
        })

    yt_caminho = _achar_dashboard("youtube-dashboard", env_vars.get("YOUTUBE_CHANNEL", ""))
    if yt_caminho:
        channel = env_vars.get("YOUTUBE_CHANNEL", "") or _handle_do_caminho(yt_caminho)
        plataformas.append({
            "id": "youtube",
            "label": "YouTube",
            "user": channel,
            "caminho": yt_caminho,
            "metricas_cmp": _extrair_metricas_cmp(yt_caminho),
        })

    li_caminho = _achar_dashboard("linkedin-dashboard", env_vars.get("LINKEDIN_PROFILE", ""))
    if li_caminho:
        user = env_vars.get("LINKEDIN_PROFILE", "") or _handle_do_caminho(li_caminho)
        plataformas.append({
            "id": "linkedin",
            "label": "LinkedIn",
            "user": f"@{user}" if user else "",
            "caminho": li_caminho,
            "metricas_cmp": _extrair_metricas_cmp(li_caminho),
        })

    # Concorrentes: entregas/concorrentes/{slug}/{plataforma}/dashboard.html
    concorrentes: list[dict] = []
    concorrentes_dir = produto_dir / "entregas" / "concorrentes"
    if concorrentes_dir.exists():
        labels_plat = {
            "instagram": "Instagram",
            "tiktok": "TikTok",
            "youtube": "YouTube",
            "linkedin": "LinkedIn",
        }
        for sub in sorted(concorrentes_dir.iterdir()):
            if not sub.is_dir():
                continue
            slug = sub.name
            # le meta.json (nome bonito + data); se nao existir, usa fallbacks
            meta_path = sub / "meta.json"
            nome = slug
            atualizado_em = ""
            handle_por_plat: dict[str, str] = {}
            if meta_path.exists():
                try:
                    import json as _json
                    meta = _json.loads(meta_path.read_text(encoding="utf-8"))
                    nome = meta.get("nome") or slug
                    atualizado_em = meta.get("atualizado_em", "")
                    handle_por_plat = meta.get("handles", {}) or {}
                except Exception:
                    pass

            plats_concorrente = []
            for pid, plabel in labels_plat.items():
                cand = sub / pid / "dashboard.html"
                if cand.exists():
                    handle = handle_por_plat.get(pid, "")
                    cam_rel = f"entregas/concorrentes/{slug}/{pid}/dashboard.html"
                    plats_concorrente.append({
                        "id": pid,
                        "label": plabel,
                        "user": f"@{handle}" if handle else "",
                        "caminho": cam_rel,
                        "metricas_cmp": _extrair_metricas_cmp(cam_rel),
                    })

            if not plats_concorrente:
                continue

            # se nao tem data no meta.json, usa o mtime do arquivo mais recente
            if not atualizado_em:
                try:
                    from datetime import datetime as _dt
                    arquivos = list(sub.rglob("dashboard.html"))
                    if arquivos:
                        ts = max(a.stat().st_mtime for a in arquivos)
                        atualizado_em = _dt.fromtimestamp(ts).strftime("%d/%m/%Y %H:%M")
                except Exception:
                    pass

            concorrentes.append({
                "slug": slug,
                "nome": nome,
                "atualizado_em": atualizado_em,
                "plataformas": plats_concorrente,
            })

    return {"minhas": plataformas, "concorrentes": concorrentes}


def parse_comercial_playbook(slug: str, produto_dir: Path) -> dict:
    """Detecta se o playbook comercial foi gerado e devolve metadados para
    o renderer. Fonte da verdade: existencia do HTML em entregas/comercial/.
    Nunca e preenchido por /produto-concepcao, so por /comercial-playbook."""
    from datetime import datetime

    arquivo = produto_dir / "entregas" / "comercial" / f"playbook-{slug}.html"
    if not arquivo.exists():
        return {"existe": False}

    try:
        mtime = arquivo.stat().st_mtime
        gerado_em = datetime.fromtimestamp(mtime).strftime("%d/%m/%Y as %H:%M")
    except OSError:
        gerado_em = ""

    caminho_rel = arquivo.relative_to(produto_dir).as_posix()
    return {
        "existe": True,
        "caminho": caminho_rel,
        "nome_arquivo": arquivo.name,
        "gerado_em": gerado_em,
    }


# ----- monta dados por secao -----

def montar_dados(secao: str, produto_dir: Path, slug: str) -> tuple[dict, str]:
    perfil = ler_arquivo(produto_dir / "perfil.md")
    idc = ler_arquivo(produto_dir / "idconsumidor.md")
    pesquisa = ler_arquivo(produto_dir / "pesquisa-mercado.md")
    nome_produto = extrair_titulo_produto(perfil, slug)

    if secao == "quadro":
        return parse_quadro(perfil), nome_produto
    if secao == "furadeira":
        return parse_furadeira(perfil, produto_dir), nome_produto
    if secao == "decorados":
        return parse_decorados(perfil), nome_produto
    if secao == "urgencias":
        return parse_urgencias(perfil), nome_produto
    if secao == "identidade-produto":
        dados = parse_identidade_produto(perfil)
        idc_json_path = produto_dir / "idconsumidor.json"
        if idc_json_path.exists():
            try:
                idc_json = json.loads(idc_json_path.read_text(encoding="utf-8"))
                if "objecoes" in idc_json:
                    dados["objecoes"] = idc_json["objecoes"]
                else:
                    dados["objecoes"] = parse_objecoes_do_idconsumidor(idc)
            except (json.JSONDecodeError, OSError):
                dados["objecoes"] = parse_objecoes_do_idconsumidor(idc)
        else:
            dados["objecoes"] = parse_objecoes_do_idconsumidor(idc)
        return dados, nome_produto
    if secao == "identidade-consumidor":
        dados_idc = parse_identidade_consumidor(perfil, idc)
        idc_json_path = produto_dir / "idconsumidor.json"
        if idc_json_path.exists():
            try:
                idc_json = json.loads(idc_json_path.read_text(encoding="utf-8"))
                if "objecoes" in idc_json:
                    dados_idc["objecoes"] = idc_json["objecoes"]
                else:
                    dados_idc["objecoes"] = parse_objecoes_do_idconsumidor(idc)
                if "baldes" in idc_json:
                    dados_idc["baldes"] = idc_json["baldes"]
            except (json.JSONDecodeError, OSError):
                dados_idc["objecoes"] = parse_objecoes_do_idconsumidor(idc)
        else:
            dados_idc["objecoes"] = parse_objecoes_do_idconsumidor(idc)
        return dados_idc, nome_produto
    if secao == "identidade-comunicador":
        return parse_identidade_comunicador(perfil, idc), nome_produto
    if secao == "pesquisa":
        dados_p = parse_pesquisa(pesquisa)
        json_path = produto_dir / "pesquisa-mercado.json"
        if json_path.exists():
            try:
                extras = json.loads(json_path.read_text(encoding="utf-8"))
                for k in ("serie_crescimento", "reclamacoes_categorias", "precos_por_formato"):
                    if k in extras:
                        dados_p[k] = extras[k]
            except (json.JSONDecodeError, OSError):
                pass
        return dados_p, nome_produto
    if secao == "copy-pagina":
        return tmpl.parse_copy_pagina(produto_dir, slug, REPO_ROOT), nome_produto
    if secao == "comercial-playbook":
        return parse_comercial_playbook(slug, produto_dir), nome_produto
    if secao == "dashboards":
        return parse_dashboards(produto_dir), nome_produto
    if secao == "analise-trafego":
        # Conteúdo gerenciado pelo painel-trafego.py. Retorna dict vazio
        # para que render_analise_trafego entregue o placeholder inicial.
        return {}, nome_produto
    raise ValueError(f"Secao desconhecida: {secao}")


# ----- visao geral (derivada) -----

def secoes_preenchidas(html_txt: str) -> list[str]:
    """Lista de secoes ja preenchidas no HTML atual (sem ser placeholder)."""
    prontas: list[str] = []
    rotulo_por_id = {
        "quadro": "Quadro",
        "furadeira": "Furadeira",
        "decorados": "Decorados",
        "urgencias": "Urgencias ocultas",
        "identidade-produto": "Identidade do produto",
        "identidade-consumidor": "Identidade do consumidor",
        "identidade-comunicador": "Identidade do comunicador",
        "pesquisa": "Pesquisa de mercado",
        "copy-pagina": "Copy da pagina",
        "comercial-playbook": "Playbook comercial",
    }
    for sid, rotulo in rotulo_por_id.items():
        bloco = extrair_bloco_secao(html_txt, sid)
        if bloco and "placeholder-title" not in bloco:
            prontas.append(rotulo)
    return prontas


def montar_visao_geral(html_txt: str, perfil: str, slug: str, tipo: str) -> dict:
    quadro_bloco = (
        extrair_secao(perfil, "Quadro (Transformacao Principal)")
        or extrair_secao(perfil, "Quadro")
    )
    quadro = ""
    for linha in quadro_bloco.splitlines():
        if linha.strip():
            quadro = linha.strip()
            break

    ip = extrair_secao(perfil, "Identidade do Produto")
    kv_ip = kv_bullets(ip)
    ic = extrair_secao(perfil, "Identidade do Consumidor")
    kv_ic = kv_bullets(ic)

    preco = kv_ip.get("Preco", "") or kv_ip.get("Preço", "")
    diferencial = kv_ip.get("Diferencial", "")
    nicho = (
        kv_ip.get("Nicho", "")
        or kv_ic.get("Nicho", "")
        or kv_ic.get("Publico-alvo", "")
        or kv_ic.get("Público-alvo", "")
    )

    return {
        "nome_produto": extrair_titulo_produto(perfil, slug),
        "tipo": tipo,
        "preco": preco,
        "quadro": quadro or "Quadro ainda nao definido.",
        "nicho": nicho,
        "diferencial": diferencial,
        "secoes_prontas": secoes_preenchidas(html_txt),
    }


# ----- manipulacao do HTML -----

def extrair_bloco_secao(html_txt: str, secao: str) -> str:
    pat = re.compile(
        rf"<!--\s*SECTION:{re.escape(secao)}\s*-->(.*?)<!--\s*/SECTION:{re.escape(secao)}\s*-->",
        re.DOTALL,
    )
    m = pat.search(html_txt)
    return m.group(0) if m else ""


def substituir_secao(html_txt: str, secao: str, novo: str) -> str:
    pat = re.compile(
        rf"<!--\s*SECTION:{re.escape(secao)}\s*-->.*?<!--\s*/SECTION:{re.escape(secao)}\s*-->",
        re.DOTALL,
    )
    if pat.search(html_txt):
        return pat.sub(lambda m: novo, html_txt, count=1)
    # Se o marcador nao existe (painel legado), nao mexe
    return html_txt


# ----- CLI -----

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--secao",
        required=True,
        choices=SECOES_VALIDAS,
        help="Secao a atualizar",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="Slug do produto (default: le meus-produtos/.ativo)",
    )
    parser.add_argument(
        "--rebuild-shell",
        action="store_true",
        help="Forca a recriacao do shell mesmo que o painel ja exista (uso raro)",
    )
    parser.add_argument(
        "--gerando",
        action="store_true",
        help="Marca secao identidade-consumidor como 'Gerando...' (usado enquanto agente background roda)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Abre o painel no navegador apos gerar",
    )
    args = parser.parse_args()

    slug = args.slug or ler_ativo()
    if not slug:
        print("Nenhum produto ativo. Use /produto-novo ou --slug.", file=sys.stderr)
        return 1

    produto_dir = PRODUTOS_DIR / slug
    if not produto_dir.is_dir():
        print(f"Produto nao encontrado: {produto_dir}", file=sys.stderr)
        return 1

    painel_path = produto_dir / PAINEL_NOME

    perfil = ler_arquivo(produto_dir / "perfil.md")
    tipo_md = normalizar_tipo(ler_arquivo(produto_dir / "tipo.md"))
    nome_produto = extrair_titulo_produto(perfil, slug)

    # Garante que os assets do design Fluxo Criativo (logo do gorila, banner)
    # estejam na pasta do produto, para que o CSS relativo funcione.
    garantir_assets(produto_dir)

    # Cria shell se nao existir ou se o existente nao tem marcadores (legado)
    existente = painel_path.read_text(encoding="utf-8") if painel_path.exists() else ""
    tem_markers = "<!-- SECTION:" in existente
    criou_shell = False
    if not existente or args.rebuild_shell or not tem_markers:
        existente = tmpl.build_shell(nome_produto)
        criou_shell = True

    # Auto-upgrade: se o painel existe mas nao tem a secao pedida (pq o template
    # ganhou seccao nova depois da criacao do painel), reconstroi o shell
    # preservando todos os blocos ja preenchidos.
    marcador_pedido = f"<!-- SECTION:{args.secao} -->"
    if not criou_shell and marcador_pedido not in existente:
        preservados: dict[str, str] = {}
        for sid in list(tmpl.SECOES_RENDERIZAVEIS) + ["visao-geral"]:
            bloco = extrair_bloco_secao(existente, sid)
            if bloco and "placeholder-title" not in bloco:
                preservados[sid] = bloco
        existente = tmpl.build_shell(nome_produto)
        for sid, bloco in preservados.items():
            existente = substituir_secao(existente, sid, bloco)
        criou_shell = True  # sinaliza no print final

    # Atualiza secao pedida
    dados, _ = montar_dados(args.secao, produto_dir, slug)
    if args.secao == "identidade-consumidor" and args.gerando:
        dados["_gerando"] = True
    render = tmpl.RENDERS[args.secao]
    novo_bloco = render(dados)
    existente = substituir_secao(existente, args.secao, novo_bloco)

    # Atualiza visao-geral (derivada)
    vg_dados = montar_visao_geral(existente, perfil, slug, tipo_md)
    existente = substituir_secao(existente, "visao-geral", tmpl.render_visao_geral(vg_dados))

    # Atualiza nome do produto na sidebar se o perfil mudou desde a criacao
    existente = re.sub(
        r'(<div class="sidebar-product">).*?(</div>)',
        lambda m: f"{m.group(1)}{nome_produto}{m.group(2)}",
        existente,
        count=1,
    )

    painel_path.write_text(existente, encoding="utf-8")

    caminho_rel = painel_path.relative_to(REPO_ROOT)
    if criou_shell:
        print(f"Painel criado em {caminho_rel}")
    print(f"Secao atualizada: {args.secao}")
    print(f"Caminho: {caminho_rel}")

    if args.open:
        import webbrowser, urllib.request
        url = painel_path.resolve().as_uri() + "#sala-dos-agentes"
        webbrowser.open(url)
        print(f"Painel aberto no navegador.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
