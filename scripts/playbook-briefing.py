"""
playbook-briefing.py

Gera um BRIEFING COMPACTO (em Markdown) a partir do perfil.md + idconsumidor.md
do produto, com APENAS os dados que os 6 sub-agentes do playbook comercial
precisam para escrever as 6 seções criativas (4, 5, 6, 7, 10, 11).

Por que existe: rodar 6 agentes em paralelo, cada um lendo perfil.md (200+
linhas) e idconsumidor.md (300+ linhas) integralmente, é um desperdício de
tokens e de tempo. Este script extrai um briefing de ~60-80 linhas que cabe
inline no prompt de cada agente.

Saída padrão: scripts/.tmp-briefing-{slug}.md
Imprime no stdout o caminho do arquivo gerado.

Uso:
    py -3 scripts/playbook-briefing.py
    py -3 scripts/playbook-briefing.py --slug curso-tarot
    py -3 scripts/playbook-briefing.py --slug curso-tarot --stdout
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

# Garantir UTF-8 no Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
PASTA_PRODUTOS = RAIZ / "meus-produtos"
sys.path.insert(0, str(RAIZ / "scripts"))

# Reaproveita os parsers de playbook-montar.py
# (importação por path, já que o nome tem hífen)
import importlib.util

_montar_spec = importlib.util.spec_from_file_location(
    "playbook_montar",
    RAIZ / "scripts" / "playbook-montar.py",
)
if _montar_spec is None or _montar_spec.loader is None:
    raise SystemExit("Não consegui carregar playbook-montar.py")
_montar = importlib.util.module_from_spec(_montar_spec)
_montar_spec.loader.exec_module(_montar)
parse_perfil = _montar.parse_perfil
parse_idconsumidor = _montar.parse_idconsumidor
ler_produto = _montar.ler_produto


# ============================================================================
# Helpers de formatação
# ============================================================================


def _bullet(itens: list[str], limite: int | None = None) -> str:
    """Formata lista de itens como bullets MD. Aplica limite se passado."""
    if limite is not None:
        itens = itens[:limite]
    if not itens:
        return "- (vazio)"
    return "\n".join(f"- {item}" for item in itens if item)


def _aspa(texto: str) -> str:
    return f'"{texto.strip().strip(chr(8220)).strip(chr(8221)).strip()}"'


# ============================================================================
# Geração do briefing
# ============================================================================


def gerar_briefing(perfil: dict, idc: dict, slug: str) -> str:
    nome = perfil.get("nome_produto") or slug.replace("-", " ").title()
    quadro = perfil.get("quadro", "")
    preco = perfil.get("preco_texto", "")
    tipo = perfil.get("tipo", "")
    formato = perfil.get("formato", "")
    posicionamento = perfil.get("posicionamento", "")
    tom_voz = perfil.get("tom_voz", "")
    posicionamento_com = perfil.get("posicionamento_comunicador", "")

    # Furadeira
    etapas = perfil.get("furadeira_etapas", [])
    if etapas:
        furadeira_linhas = []
        for et in etapas:
            num = et.get("numero", "")
            nome_et = et.get("nome", "")
            prazo = et.get("prazo", "")
            resumo = et.get("resumo", "")
            cabecalho = f"- {num}. {nome_et}"
            if prazo:
                cabecalho += f" ({prazo})"
            if resumo:
                # limita a 1 linha curta
                resumo_curto = resumo[:200]
                cabecalho += f". {resumo_curto}"
            furadeira_linhas.append(cabecalho)
        furadeira_str = "\n".join(furadeira_linhas)
    else:
        furadeira_str = "- (Furadeira não cadastrada)"

    # Tom do comunicador
    mantras = perfil.get("mantras", [])
    palavras_conectar = perfil.get("palavras_conectar", [])
    palavras_afastar = perfil.get("palavras_afastar", [])

    # Consumidor (Público-alvo do perfil antigo, Para Quem É do idconsumidor ou Perfil do resumo)
    demograficos = perfil.get("demograficos", {})
    publico = (
        perfil.get("perfil_consumidor")
        or demograficos.get("Público-alvo")
        or demograficos.get("Publico-alvo", "")
    )
    paliativos = idc.get("paliativos_idc") or perfil.get("paliativos") or []
    frases = idc.get("frases_consumidor") or perfil.get("frases_publico") or []

    # Baldes (primeiro título de cada balde como recorte de público)
    baldes = idc.get("baldes", [])
    recortes = [b.get("titulo", "") for b in baldes if b.get("titulo")]

    # Dores e desejos top (limita a 5 cada para o briefing)
    dores = perfil.get("dores", [])
    desejos = perfil.get("desejos", [])
    urg = perfil.get("urgencias", {})
    quentes = urg.get("quentes", [])

    # Argumentos Incontestáveis (top 4)
    argumentos = perfil.get("argumentos_incontestaveis", [])

    # Diferenciais
    diferenciais = perfil.get("diferenciais", [])

    # Entregáveis (até 6, para a apresentação semana a semana)
    entregaveis = perfil.get("entregaveis", [])

    bloco = f"""# Briefing comercial — {nome}

> Briefing único compartilhado pelos 6 sub-agentes que escrevem as seções criativas
> do playbook (4. Outbound, 5. Inbound, 6. SPIN, 7. Preço, 10. Recuperação, 11. Follow-up).
> Tudo aqui veio de meus-produtos/{slug}/perfil.md e idconsumidor.md. Não invente fato fora
> dessa fonte.

## Produto
- Nome: {nome}
- Quadro (transformação): {quadro or "(vazio)"}
- Preço: {preco or "(vazio)"}
- Tipo: {tipo or "(vazio)"}
- Formato (o que o cliente recebe): {formato or "(vazio)"}
- Posicionamento: {posicionamento or "(vazio)"}

## Furadeira (método em macroetapas)
{furadeira_str}

## Entregáveis principais
{_bullet(entregaveis, limite=8)}

## Diferenciais competitivos
{_bullet(diferenciais, limite=5)}

## Argumentos Incontestáveis (use como apoio em quebras e ancoragem)
{_bullet(argumentos, limite=6)}

## Tom do comunicador (voz que cada mensagem precisa carregar)
- Voz: {tom_voz or "(vazio)"}
- Posicionamento pessoal: {posicionamento_com or "(vazio)"}
- Palavras que CONECTAM (use): {", ".join(palavras_conectar[:14]) or "(vazio)"}
- Palavras que AFASTAM (evite): {", ".join(palavras_afastar[:12]) or "(vazio)"}
- Mantras do comunicador (cite com naturalidade quando couber):
{chr(10).join(f"  - {_aspa(m)}" for m in mantras[:5]) or "  - (vazio)"}

## Consumidor (com quem você está conversando)
- Perfil: {publico or "(vazio)"}
- Recortes (baldes de Para Quem É):
{chr(10).join(f"  - {r}" for r in recortes[:5]) or "  - (vazio)"}

### Frases reais que o consumidor usa (priorize palavras dele em cada bolha)
{_bullet([_aspa(f) for f in frases], limite=10)}

### Paliativos (concorrentes que ele já testou e abandonou — use em ancoragem)
{_bullet(paliativos, limite=8)}

## Dores quentes (use na seção Outbound, SPIN-Problema e Recuperação)
{_bullet(dores, limite=8)}

## Desejos quentes (use na seção SPIN-Necessidade e Apresentação)
{_bullet(desejos, limite=8)}

## Urgências quentes (use em ganchos de Outbound e Recuperação)
{_bullet(quentes, limite=6)}

---

## Regras de voz que TODO agente segue (não negociáveis)

1. Cada bolha = 1 mensagem curta de WhatsApp (máximo 2 a 3 linhas). Sem parágrafos.
2. Use palavras da lista CONECTAM. Nunca use palavras da lista AFASTAM.
3. Cite vocabulário, paliativos e frases concretas do consumidor. Proibido genérico.
4. Quando precisar inserir o que o lead acabou de dizer, escreva entre colchetes:
   `[NOME]`, `[palavra que o lead usou]`, `[dor descrita pelo lead]`.
5. Proibições absolutas em qualquer texto:
   - travessão (—)
   - ponto de exclamação (!)
   - estrutura "não é X. é Y."
   - perguntas no gancho ("você quer ...?")
   - promessas vagas sem dado concreto
   - "mesmo que", "sem precisar"
   - lero-lero genérico de nicho
6. Saída: APENAS um JSON plano, sem markdown, sem ```json, sem texto antes ou depois.
   Todas as chaves do schema são obrigatórias. Cada valor é uma string curta.
   Notas de condução são instruções para o vendedor (1 a 2 frases).
"""
    return bloco


# ============================================================================
# CLI
# ============================================================================


def descobrir_slug_ativo() -> str:
    arquivo = PASTA_PRODUTOS / ".ativo"
    if not arquivo.exists():
        raise SystemExit(
            "meus-produtos/.ativo não existe. Rode /produto-novo ou /produto-trocar primeiro."
        )
    slug = arquivo.read_text(encoding="utf-8").strip()
    if not slug:
        raise SystemExit("meus-produtos/.ativo está vazio. Rode /produto-trocar.")
    return slug


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", help="Slug do produto (default: .ativo)")
    parser.add_argument(
        "--saida",
        help="Caminho do arquivo MD de saída. Default: scripts/.tmp-briefing-{slug}.md",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Imprime o briefing no stdout em vez de salvar arquivo.",
    )
    args = parser.parse_args()

    slug = args.slug or descobrir_slug_ativo()
    pasta_produto = PASTA_PRODUTOS / slug
    if not pasta_produto.exists():
        raise SystemExit(f"Pasta não existe: {pasta_produto}")

    perfil_path = pasta_produto / "perfil.md"
    if not perfil_path.exists():
        raise SystemExit(
            f"perfil.md não encontrado em {pasta_produto}. Rode /produto-concepcao antes."
        )
    idc_path = pasta_produto / "idconsumidor.md"
    if not idc_path.exists():
        raise SystemExit(
            f"idconsumidor.md não encontrado em {pasta_produto}. Rode /produto-concepcao antes."
        )

    perfil, idc = ler_produto(pasta_produto)

    briefing = gerar_briefing(perfil, idc, slug)

    if args.stdout:
        sys.stdout.write(briefing)
        return 0

    if args.saida:
        destino = Path(args.saida)
    else:
        destino = RAIZ / "scripts" / f".tmp-briefing-{slug}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(briefing, encoding="utf-8")
    print(str(destino))
    return 0


if __name__ == "__main__":
    sys.exit(main())
