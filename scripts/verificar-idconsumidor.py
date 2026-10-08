"""
Verificar Identidade do Consumidor
====================================
Valida estrutura e Light Copy do idconsumidor.md do produto ativo.
Roda apos o sub-agente salvar o arquivo, antes de reconstruir o painel.

Uso:
  py -3 scripts/verificar-idconsumidor.py
  py -3 scripts/verificar-idconsumidor.py --slug meu-produto

Saida:
  Exit 0 — tudo ok
  Exit 1 — um ou mais problemas encontrados
"""
import re, sys, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUTOS = ROOT / "meus-produtos"


def get_slug():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", default=None)
    args = parser.parse_args()
    if args.slug:
        return args.slug
    ativo = PRODUTOS / ".ativo"
    if ativo.exists():
        return ativo.read_text(encoding="utf-8").strip()
    print("Erro: nenhum produto ativo. Use --slug ou crie meus-produtos/.ativo")
    sys.exit(1)


# ── estrutura ─────────────────────────────────────────────────────────

BALDE_FORMATOS = [
    ("canonico ### Balde N:", re.compile(r"^###\s+Balde\s+\d+\s*:", re.MULTILINE | re.IGNORECASE)),
    ("legado seta Pra quem", re.compile(r"[➤➜➢]\s*Pra quem", re.IGNORECASE)),
    ("legado **Balde N -**", re.compile(r"\*\*Balde\s+\d+\s*[-–—]", re.IGNORECASE)),
]


def contar_baldes(text):
    for nome, rx in BALDE_FORMATOS:
        n = len(rx.findall(text))
        if n:
            return n, nome
    return 0, "nenhum"


def ler_tipo(slug):
    """Retorna 'low', 'middle', 'high' ou None, lendo meus-produtos/{slug}/tipo.md."""
    path = PRODUTOS / slug / "tipo.md"
    if not path.exists():
        return None
    t = path.read_text(encoding="utf-8").lower()
    for chave in ("low", "middle", "high"):
        if chave in t:
            return chave
    return None


def check_estrutura(text, tipo=None):
    ok = []
    prob = []

    # Para quem e
    if re.search(r"^## Para Quem", text, re.MULTILINE | re.IGNORECASE):
        ok.append("Para Quem E: presente")
    else:
        prob.append("Para Quem E: secao nao encontrada")

    # Campos demograficos
    for campo in ["Idade", "Genero|Gênero", "Profissao|Profissão", "Renda"]:
        pattern = rf"\*\*(?:{campo}):\*\*\s*.+"
        if re.search(pattern, text, re.IGNORECASE):
            ok.append(f"Campo {campo.split('|')[0]}: presente")
        else:
            prob.append(f"Campo {campo.split('|')[0]}: nao encontrado ou vazio")

    # Objecoes
    objs = re.findall(r"^### Objeção \d+:", text, re.MULTILINE | re.IGNORECASE)
    if not objs:
        objs = re.findall(r"^### Objecao \d+:", text, re.MULTILINE | re.IGNORECASE)
    n_obj = len(objs)
    if n_obj == 5:
        ok.append(f"Objecoes: {n_obj}/5")
    else:
        prob.append(f"Objecoes: {n_obj}/5 (esperado 5)")

    # Argumentos por objecao (7 cada = 35 total)
    args_total = re.findall(r"^\*\*\d+\.\s+Argumento", text, re.MULTILINE | re.IGNORECASE)
    n_args = len(args_total)
    esperado = n_obj * 7
    if n_args == esperado:
        ok.append(f"Argumentos: {n_args}/{esperado}")
    else:
        prob.append(f"Argumentos: {n_args}/{esperado} (esperado {esperado})")

    # Paliativos: obrigatorio so em Middle Ticket. Low Ticket nao tem.
    tem_paliativos = re.search(r"^## Paliativos", text, re.MULTILINE | re.IGNORECASE)
    if tipo == "low":
        if tem_paliativos:
            prob.append("Paliativos: secao presente, mas Low Ticket nao tem paliativos (remover)")
        else:
            ok.append("Paliativos: ausente (correto para Low Ticket)")
    elif tipo == "middle":
        if tem_paliativos:
            ok.append("Paliativos: presente (Middle Ticket)")
        else:
            prob.append("Paliativos: secao nao encontrada (obrigatoria em Middle Ticket)")
    else:
        ok.append("Paliativos: tipo.md ausente ou desconhecido, verificacao pulada")

    # Baldes: formato canonico e "### Balde N: Nome" (gerador-idconsumidor).
    # Formatos legados continuam aceitos na leitura, mesma ordem do parser do painel.
    n_baldes, formato = contar_baldes(text)
    if 3 <= n_baldes <= 5:
        ok.append(f"Baldes: {n_baldes} (ok, formato {formato})")
    else:
        prob.append(f"Baldes: {n_baldes} (esperado 3-5)")

    # Frases que essa pessoa diria
    if re.search(r"^## Frases que", text, re.MULTILINE | re.IGNORECASE):
        ok.append("Frases: presente")
    else:
        prob.append("Frases: secao nao encontrada")

    # Como se comunicar
    if re.search(r"^## Como se Comunicar", text, re.MULTILINE | re.IGNORECASE):
        ok.append("Como se Comunicar: presente")
    else:
        prob.append("Como se Comunicar: secao nao encontrada")

    return ok, prob


# ── light copy ────────────────────────────────────────────────────────

def check_light_copy(text):
    ok = []
    prob = []
    lines = text.splitlines()

    # Travessao
    hits = [(i + 1, l) for i, l in enumerate(lines) if "\u2014" in l]
    if hits:
        prob.append(f"Travessao (—): {len(hits)} ocorrencia(s)")
        for ln, line in hits[:3]:
            prob.append(f"  Linha {ln}: {line.strip()[:90]}")
    else:
        ok.append("Travessao: nenhum")

    # Ponto de exclamacao
    hits = [(i + 1, l) for i, l in enumerate(lines) if "!" in l]
    if hits:
        prob.append(f"Exclamacao (!): {len(hits)} ocorrencia(s)")
        for ln, line in hits[:3]:
            prob.append(f"  Linha {ln}: {line.strip()[:90]}")
    else:
        ok.append("Exclamacao: nenhuma")

    # Paragrafo que abre com pergunta
    hits = [
        (i + 1, l)
        for i, l in enumerate(lines)
        if re.match(r"^\s*[A-ZÁÉÍÓÚÂÊÎÔÛÃÕÀÈÌÒÙÇ].{5,}\?", l)
        and not l.strip().startswith("#")
        and not l.strip().startswith("-")
        and not l.strip().startswith("*")
    ]
    if hits:
        prob.append(f"Paragrafos abrindo com pergunta: {len(hits)} ocorrencia(s)")
        for ln, line in hits[:3]:
            prob.append(f"  Linha {ln}: {line.strip()[:90]}")
    else:
        ok.append("Perguntas retorias: nenhuma")

    # Estrutura "Nao e X. E Y."
    hits = [(i + 1, l) for i, l in enumerate(lines) if re.search(r"Não é .+\. É ", l)]
    if hits:
        prob.append(f"Estrutura 'Nao e X. E Y.': {len(hits)} ocorrencia(s)")
        for ln, line in hits[:2]:
            prob.append(f"  Linha {ln}: {line.strip()[:90]}")
    else:
        ok.append("Estrutura proibida 'Nao e X. E Y.': nenhuma")

    return ok, prob


# ── main ──────────────────────────────────────────────────────────────

def main():
    slug = get_slug()
    path = PRODUTOS / slug / "idconsumidor.md"

    if not path.exists():
        print(f"[!!] Arquivo nao encontrado: {path}")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")

    print(f"\nVERIFICANDO idconsumidor.md — {slug}")
    print("=" * 52)

    print("\nESTRUTURA")
    ok_e, prob_e = check_estrutura(text, ler_tipo(slug))
    for item in ok_e:
        print(f"  [OK] {item}")
    for item in prob_e:
        print(f"  [!!] {item}")

    print("\nLIGHT COPY")
    ok_c, prob_c = check_light_copy(text)
    for item in ok_c:
        print(f"  [OK] {item}")
    for item in prob_c:
        print(f"  [!!] {item}")

    total = len(prob_e) + len(prob_c)
    print()
    if total == 0:
        print("Resultado: OK — nenhum problema encontrado.")
    else:
        print(f"Resultado: {total} problema(s) encontrado(s).")
    sys.exit(0 if total == 0 else 1)


if __name__ == "__main__":
    main()
