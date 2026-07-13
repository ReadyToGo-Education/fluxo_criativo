# -*- coding: utf-8 -*-
"""Extrai o texto de todos os PDFs em referencias/livros/ para arquivos .txt
em referencias/livros/texto/, um por livro, com nome em slug ASCII.
Uso: python3 scripts/extrair-texto-livros.py
"""
import re
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader

RAIZ = Path(__file__).resolve().parent.parent
PASTA_PDF = RAIZ / "referencias" / "livros"
PASTA_TXT = PASTA_PDF / "texto"
PASTA_TXT.mkdir(exist_ok=True)


def slug(nome: str) -> str:
    nome = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("ascii")
    nome = nome.lower()
    nome = re.sub(r"[^a-z0-9]+", "-", nome).strip("-")
    return nome


def main() -> None:
    pdfs = sorted(PASTA_PDF.glob("*.pdf"))
    print(f"Encontrados {len(pdfs)} PDFs.")
    erros = []
    for pdf in pdfs:
        destino = PASTA_TXT / (slug(pdf.stem) + ".txt")
        if destino.exists() and destino.stat().st_size > 10_000:
            print(f"[pula] {destino.name} ja existe")
            continue
        try:
            reader = PdfReader(str(pdf))
            partes = []
            for i, pagina in enumerate(reader.pages):
                try:
                    txt = pagina.extract_text() or ""
                except Exception as e:  # pagina corrompida nao derruba o livro
                    txt = f"[erro na pagina {i + 1}: {e}]"
                partes.append(f"\n--- pagina {i + 1} ---\n{txt}")
            conteudo = "".join(partes)
            destino.write_text(conteudo, encoding="utf-8")
            print(f"[ok] {pdf.name} -> {destino.name} ({len(reader.pages)} paginas, {len(conteudo)//1000} mil caracteres)")
        except Exception as e:
            erros.append((pdf.name, str(e)))
            print(f"[ERRO] {pdf.name}: {e}")
    print(f"\nConcluido. {len(pdfs) - len(erros)} extraidos, {len(erros)} com erro.")
    if erros:
        for nome, erro in erros:
            print(f"  - {nome}: {erro}")
        sys.exit(1)


if __name__ == "__main__":
    main()
