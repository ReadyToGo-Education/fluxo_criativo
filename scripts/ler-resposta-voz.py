# -*- coding: utf-8 -*-
"""Hook Stop: lê em voz alta (TTS Windows, voz pt-BR Microsoft Maria) a última
resposta do assistente. Recebe o JSON do hook no stdin (campo transcript_path),
extrai o último texto do assistente, limpa a formatação e fala.
Não fala nada se não encontrar texto. Sai sempre com código 0.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

LIMITE_CARACTERES = 1200  # evita leituras de vários minutos


def extrair_ultimo_texto(transcript_path):
    ultimo = None
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                try:
                    obj = json.loads(linha)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") != "assistant":
                    continue
                msg = obj.get("message") or {}
                partes = []
                for bloco in msg.get("content") or []:
                    if isinstance(bloco, dict) and bloco.get("type") == "text":
                        partes.append(bloco.get("text") or "")
                texto = "\n".join(p for p in partes if p).strip()
                if texto:
                    ultimo = texto
    except OSError:
        return None
    return ultimo


def limpar_para_fala(texto):
    # remove blocos de código
    texto = re.sub(r"```.*?```", " ", texto, flags=re.S)
    texto = re.sub(r"`([^`]*)`", r"\1", texto)
    # links markdown: mantém só o rótulo
    texto = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texto)
    # cabeçalhos, ênfase, listas, tabelas
    texto = re.sub(r"^#{1,6}\s*", "", texto, flags=re.M)
    texto = re.sub(r"[*_#>|]", " ", texto)
    texto = re.sub(r"^\s*[-•]\s*", "", texto, flags=re.M)
    # URLs e caminhos de arquivo longos não valem a pena ouvir
    texto = re.sub(r"https?://\S+", "link", texto)
    texto = re.sub(r"[A-Za-z]:\\\S+", "caminho de arquivo", texto)
    # emojis e símbolos comuns do projeto
    texto = re.sub(r"[\U0001F000-\U0001FAFF☀-➿←-⇿⬀-⯿]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    if len(texto) > LIMITE_CARACTERES:
        corte = texto.rfind(".", 0, LIMITE_CARACTERES)
        if corte < 200:
            corte = LIMITE_CARACTERES
        texto = texto[: corte + 1]
    return texto


FALAR_PS1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "falar-texto.ps1")


def falar(texto):
    """Fala o texto com a voz Microsoft Daniel (pt-BR, masculina) via falar-texto.ps1."""
    with tempfile.NamedTemporaryFile(
        "w", suffix=".txt", delete=False, encoding="utf-8-sig"
    ) as tmp:
        tmp.write(texto)
        caminho = tmp.name
    try:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                FALAR_PS1,
                caminho,
            ],
            timeout=180,
            capture_output=True,
        )
    finally:
        try:
            os.unlink(caminho)
        except OSError:
            pass


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    transcript = payload.get("transcript_path")
    if not transcript or not os.path.exists(transcript):
        return
    texto = extrair_ultimo_texto(transcript)
    if not texto:
        return
    fala = limpar_para_fala(texto)
    if fala:
        falar(fala)


if __name__ == "__main__":
    main()
    sys.exit(0)
