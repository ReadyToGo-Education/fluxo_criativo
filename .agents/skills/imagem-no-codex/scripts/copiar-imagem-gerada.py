#!/usr/bin/env python3
"""Copia a imagem gerada pelo Codex para a pasta de entregas do workshop.

A ferramenta de imagem do Codex salva o arquivo em generated_images, dentro da
pasta do Codex ($CODEX_HOME, ou ~/.codex quando a variável não existe). Os
fluxos do workshop precisam da imagem na pasta do produto, com um nome certo
(ex.: meus-produtos/{ativo}/entregas/criativos/criativo-meme-3-feed.png).

Uso:
    python3 .agents/skills/imagem-no-codex/scripts/copiar-imagem-gerada.py --destino CAMINHO
    python3 .agents/skills/imagem-no-codex/scripts/copiar-imagem-gerada.py --destino CAMINHO --origem CAMINHO

Sem --origem, usa a imagem mais recente de generated_images, desde que ela
tenha sido criada há pouco tempo (30 minutos por padrão, ajustável com
--minutos). Assim o script não copia por engano uma imagem velha.

Mostra no fim a largura, a altura e a proporção da imagem salva, para conferir
se saiu no formato pedido (4:5, 9:16 etc.).
"""

from __future__ import annotations

import argparse
import os
import shutil
import struct
import sys
import time
from pathlib import Path

EXTENSOES = {".png", ".jpg", ".jpeg", ".webp"}

PROPORCOES = {
    "1:1": 1 / 1, "4:5": 4 / 5, "3:4": 3 / 4, "2:3": 2 / 3, "9:16": 9 / 16,
    "5:4": 5 / 4, "4:3": 4 / 3, "3:2": 3 / 2, "16:9": 16 / 9,
}


def pasta_do_codex() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser()


def imagem_mais_recente(pasta: Path, minutos: float) -> Path:
    if not pasta.is_dir():
        raise SystemExit(f"Não encontrei a pasta de imagens do Codex: {pasta}. Passe --origem com o caminho da imagem.")
    imagens = [p for p in pasta.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSOES]
    if not imagens:
        raise SystemExit(f"Nenhuma imagem em {pasta}. Passe --origem com o caminho da imagem.")
    recente = max(imagens, key=lambda p: p.stat().st_mtime)
    idade = (time.time() - recente.stat().st_mtime) / 60
    if idade > minutos:
        raise SystemExit(
            f"A imagem mais recente ({recente}) foi criada há {idade:.0f} minutos. "
            "Passe --origem com o caminho da imagem certa."
        )
    return recente


def tamanho(caminho: Path) -> tuple[int, int] | None:
    """Lê largura e altura. PNG direto do cabeçalho; os outros formatos só com o Pillow."""
    with caminho.open("rb") as arquivo:
        cabecalho = arquivo.read(24)
    if cabecalho[:8] == b"\x89PNG\r\n\x1a\n" and cabecalho[12:16] == b"IHDR":
        return struct.unpack(">II", cabecalho[16:24])
    try:
        from PIL import Image
    except ImportError:
        return None
    with Image.open(caminho) as imagem:
        return imagem.size


def descrever_proporcao(largura: int, altura: int) -> str:
    razao = largura / altura
    nome, alvo = min(PROPORCOES.items(), key=lambda item: abs(item[1] - razao))
    if abs(alvo - razao) / alvo <= 0.02:
        return nome
    return f"{razao:.2f} (a mais próxima é {nome})"


def copiar(origem: Path, destino: Path) -> Path:
    """Copia para o destino. Se os formatos diferem, converte com o Pillow quando existir."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    if origem.suffix.lower() == destino.suffix.lower():
        shutil.copy2(origem, destino)
        return destino
    try:
        from PIL import Image
    except ImportError:
        destino = destino.with_suffix(origem.suffix.lower())
        print(f"Aviso: a imagem veio em {origem.suffix} e o Pillow não está instalado para converter. Salvei como {destino.name}.")
        shutil.copy2(origem, destino)
        return destino
    with Image.open(origem) as imagem:
        imagem.save(destino)
    return destino


def main() -> int:
    # Saída de erro também em UTF-8: as mensagens do SystemExit vão por ela.
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Copia a imagem gerada pelo Codex para a pasta de entregas.")
    parser.add_argument("--destino", required=True, help="caminho final da imagem (ex.: meus-produtos/x/entregas/criativos/criativo-meme-1-feed.png)")
    parser.add_argument("--origem", help="caminho da imagem gerada, quando a ferramenta informar")
    parser.add_argument("--minutos", type=float, default=30, help="idade máxima da imagem mais recente, sem --origem (padrão: 30)")
    args = parser.parse_args()

    if args.origem:
        origem = Path(args.origem).expanduser()
        if not origem.is_file():
            raise SystemExit(f"A imagem informada em --origem não existe: {origem}")
    else:
        origem = imagem_mais_recente(pasta_do_codex() / "generated_images", args.minutos)

    destino = copiar(origem, Path(args.destino).expanduser())
    print(f"Imagem salva em {destino}")

    medidas = tamanho(destino)
    if medidas:
        largura, altura = medidas
        print(f"Tamanho: {largura}x{altura}, proporção {descrever_proporcao(largura, altura)}")
    else:
        print("Não consegui ler o tamanho da imagem. Confira a proporção olhando a imagem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
