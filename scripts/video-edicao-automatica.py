#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Edição automática da fala: legenda, corte de erros e corte de silêncios.

Usado pelo command /video-editar (opção "Edição automática da fala").

Roda no computador do aluno, só no processador (não precisa de placa de vídeo),
com o FFmpeg e o whisper.cpp que o Severino já usa. Não chama API paga e não
precisa de biblioteca Python extra: só a biblioteca padrão do Python.

Subcomandos:
  verificar          confere FFmpeg, whisper.cpp e o modelo de transcrição
  instalar-whisper   instala o whisper.cpp (Windows) e baixa o modelo
  preparar           transcreve, acha erros e pausas, monta o plano de cortes e a legenda
  renderizar         aplica os cortes e queima a legenda numa única codificação

Fluxo típico:
  python3 scripts/video-edicao-automatica.py preparar --video X.mp4 --pasta TEMP --legenda --erros --silencios
  (o Claude revisa os erros sugeridos e o texto; se precisar, roda de novo com ajustes)
  python3 scripts/video-edicao-automatica.py renderizar --video X.mp4 --pasta TEMP --saida X_editado.mp4 --queimar-legenda
"""

import argparse
import array
import json
import math
import operator
import os
import platform
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.request
import wave
import zipfile
from difflib import SequenceMatcher
from fractions import Fraction
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parent.parent
PASTA_WHISPER = RAIZ / ".claude" / "tools" / "whisper"
URL_WHISPER_WINDOWS = (
    "https://github.com/ggml-org/whisper.cpp/releases/download/v1.8.4/whisper-blas-bin-x64.zip"
)
URL_MODELO = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-{nome}.bin"
# Tamanho mínimo de cada modelo (o arquivo completo tem 488 MB e 148 MB): pega download cortado.
TAMANHO_MINIMO_MODELO = {"base": 145 * 1000 * 1000, "small": 480 * 1000 * 1000}

# Ritmo do corte de silêncio: pausas a partir de "pausa_min" segundos são cortadas,
# deixando "folga" segundos de respiro antes e depois da fala.
RITMOS = {
    "natural": {"pausa_min": 0.9, "folga": 0.25},
    "dinamico": {"pausa_min": 0.5, "folga": 0.15},
    "acelerado": {"pausa_min": 0.3, "folga": 0.08},
}

PASSO = 0.01  # a análise de volume trabalha em blocos de 10 ms

# Expressões que a pessoa fala quando erra e vai recomeçar a frase (sem acento, minúsculas).
# Fortes: viram corte quando a frase seguinte repete o começo da anterior OU quando a
# expressão está num trecho curto (ex.: "Não, peraí." sozinho).
# Fracas: também são fala normal ("Calma. Eu vou explicar."), então só viram corte
# quando a frase seguinte repete o começo da anterior.
MARCADORES_FORTES = [
    ("nao", "perai"), ("perai",), ("pera", "ai"), ("corta",), ("corta", "isso"), ("errei",),
    ("me", "enrolei"), ("enrolei",), ("comecar", "de", "novo"), ("comecando", "de", "novo"),
    ("vou", "repetir"), ("deixa", "eu", "repetir"), ("repetindo",), ("recomecando",),
    ("vamos", "de", "novo"),
]
MARCADORES_FRACOS = [
    ("pera",), ("de", "novo"), ("espera",), ("calma",), ("opa",), ("ops",), ("desculpa",),
    ("nao", "nao"), ("perdao",),
]
MARCADORES = sorted([(m, True) for m in MARCADORES_FORTES] + [(m, False) for m in MARCADORES_FRACOS],
                    key=lambda x: len(x[0]), reverse=True)

PONTUACAO_FINAL = (".", "?", "!", "…")


# ----------------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------------

def falhar(msg, codigo=1):
    print("ERRO: " + msg, file=sys.stderr)
    sys.exit(codigo)


def rodar(cmd, cwd=None):
    return subprocess.run(
        [str(c) for c in cmd], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace",
    )


def fmt(t):
    """Tempo em m:ss.d (ex.: 1:04.3)."""
    t = max(0.0, t)
    m = int(t // 60)
    return "%d:%04.1f" % (m, t - m * 60)


def fmt_srt(t):
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def fmt_ass(t):
    cs = int(round(max(0.0, t) * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return "%d:%02d:%02d.%02d" % (h, m, s, cs)


def normalizar(txt):
    t = unicodedata.normalize("NFD", txt.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", t)


def parecidas(a, b):
    if a == b:
        return True
    if len(a) >= 4 and len(b) >= 4:
        return SequenceMatcher(None, a, b).ratio() >= 0.75
    return False


def ffmpeg_ok():
    return shutil.which("ffmpeg") and shutil.which("ffprobe")


def versao_ffmpeg():
    r = rodar(["ffmpeg", "-version"])
    m = re.search(r"version\s+n?(\d+)\.", r.stdout)
    return int(m.group(1)) if m else 99  # versões de desenvolvimento são novas


def threads_padrao():
    # Computador comum: usa os núcleos que tiver, até 8 (mais que isso quase não acelera).
    return max(1, min(os.cpu_count() or 4, 8))


# ----------------------------------------------------------------------------
# Informações do vídeo
# ----------------------------------------------------------------------------

def info_video(caminho):
    r = rodar([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=index,codec_type,width,height,avg_frame_rate,r_frame_rate"
        ":stream_side_data=rotation:stream_tags=rotate",
        "-of", "json", caminho,
    ])
    if r.returncode != 0:
        falhar("não consegui ler o vídeo. Confira se o arquivo existe e se é um vídeo válido.")
    dados = json.loads(r.stdout or "{}")
    video = next((s for s in dados.get("streams", []) if s.get("codec_type") == "video"), None)
    audio = next((s for s in dados.get("streams", []) if s.get("codec_type") == "audio"), None)
    if not video:
        falhar("o arquivo não tem imagem de vídeo.")
    largura, altura = int(video.get("width", 0)), int(video.get("height", 0))
    rotacao = 0
    for sd in video.get("side_data_list", []) or []:
        if "rotation" in sd:
            rotacao = int(float(sd["rotation"]))
    if not rotacao and video.get("tags", {}).get("rotate"):
        rotacao = int(float(video["tags"]["rotate"]))
    if abs(rotacao) % 180 == 90:
        largura, altura = altura, largura
    fps = None
    for chave in ("avg_frame_rate", "r_frame_rate"):
        try:
            f = Fraction(video.get(chave, "0/0"))
            if 10 <= f <= 61:
                fps = f.limit_denominator(1001)
                break
        except (ZeroDivisionError, ValueError):
            continue
    if fps is None:
        fps = Fraction(30)
    duracao = float(dados.get("format", {}).get("duration", 0) or 0)
    return {
        "largura": largura, "altura": altura, "rotacao": rotacao,
        "fps": fps, "duracao": duracao, "tem_audio": audio is not None,
    }


# ----------------------------------------------------------------------------
# Whisper
# ----------------------------------------------------------------------------

def achar_whisper():
    candidatos = [
        PASTA_WHISPER / "Release" / "whisper-cli.exe",
        PASTA_WHISPER / "Release" / "whisper-cli",
        PASTA_WHISPER / "build" / "bin" / "whisper-cli",
        PASTA_WHISPER / "src" / "build" / "bin" / "whisper-cli",
    ]
    for c in candidatos:
        if c.is_file():
            return str(c)
    for nome in ("whisper-cli", "whisper-cpp"):
        w = shutil.which(nome)
        if w:
            return w
    return None


def caminho_modelo(nome):
    return PASTA_WHISPER / "models" / ("ggml-%s.bin" % nome)


def caminho_sem_acento(caminho):
    """No Windows, troca um caminho com acento pelo nome curto (8.3), que o whisper.cpp abre."""
    texto = str(caminho)
    if os.name != "nt" or all(ord(c) < 128 for c in texto):
        return texto
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(1024)
        if ctypes.windll.kernel32.GetShortPathNameW(texto, buf, 1024):
            return buf.value
    except Exception:
        pass
    return texto


def modelo_ok(nome):
    m = caminho_modelo(nome)
    return m.is_file() and m.stat().st_size >= TAMANHO_MINIMO_MODELO.get(nome, 50 * 1000 * 1000)


def baixar(url, destino):
    """Baixa com o curl (retoma de onde parou se a internet cair); sem curl, usa o Python."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    parcial = destino.with_name(destino.name + ".parcial")
    if shutil.which("curl"):
        for _ in range(5):
            r = subprocess.run(["curl", "-L", "--fail", "-sS", "-C", "-", "-o", str(parcial), url])
            if r.returncode == 0:
                parcial.replace(destino)
                return
    with urllib.request.urlopen(url) as resp, open(parcial, "wb") as f:
        shutil.copyfileobj(resp, f, 1024 * 1024)
    parcial.replace(destino)


def cmd_verificar(a):
    tudo_ok = True
    if ffmpeg_ok():
        print("FFmpeg: ok (versão %s)" % versao_ffmpeg())
    else:
        print("FFmpeg: FALTA")
        tudo_ok = False
    w = achar_whisper()
    print("whisper.cpp: " + ("ok" if w else "FALTA"))
    print("Modelo de transcrição (%s): %s" % (a.modelo, "ok" if modelo_ok(a.modelo) else "FALTA"))
    print("Processador: %d núcleos (o whisper vai usar %d)" % (os.cpu_count() or 0, threads_padrao()))
    print("Sistema: " + platform.system())
    if not tudo_ok:
        sys.exit(2)
    if not w or not modelo_ok(a.modelo):
        sys.exit(3)


def cmd_instalar_whisper(a):
    sistema = platform.system()
    w = achar_whisper()
    if not w:
        if sistema == "Windows":
            print("Baixando o whisper.cpp (cerca de 17 MB)...")
            destino_zip = PASTA_WHISPER / "whisper-bin.zip"
            baixar(URL_WHISPER_WINDOWS, destino_zip)
            with zipfile.ZipFile(destino_zip) as z:
                z.extractall(PASTA_WHISPER)
            destino_zip.unlink()
            w = achar_whisper()
        else:
            print("O whisper.cpp ainda não está instalado neste computador.")
            if sistema == "Darwin":
                print("No Mac, instale com o Homebrew: brew install whisper-cpp")
            else:
                print("No Linux, compile o whisper.cpp: "
                      "git clone https://github.com/ggml-org/whisper.cpp .claude/tools/whisper/src && "
                      "cmake -S .claude/tools/whisper/src -B .claude/tools/whisper/src/build && "
                      "cmake --build .claude/tools/whisper/src/build -j --config Release")
            print("Depois rode este comando de novo para baixar o modelo.")
            sys.exit(2)
    if not w:
        falhar("a instalação do whisper.cpp não funcionou.")
    if not modelo_ok(a.modelo):
        tamanho = "466 MB" if a.modelo == "small" else "148 MB"
        print("Baixando o modelo de transcrição em português (%s, só na primeira vez)..." % tamanho)
        baixar(URL_MODELO.format(nome=a.modelo), caminho_modelo(a.modelo))
    if not modelo_ok(a.modelo):
        falhar("o modelo não foi baixado por inteiro. Confira a internet e o espaço em disco.")
    teste = rodar([w, "--help"])
    if teste.returncode not in (0, 1) and "usage" not in (teste.stdout + teste.stderr).lower():
        falhar("o whisper.cpp foi instalado, mas não abriu neste computador.")
    print("whisper.cpp pronto.")


def transcrever(wav, pasta, modelo, threads, prompt):
    exe = achar_whisper()
    if not exe:
        falhar("o whisper.cpp não está instalado. Rode o subcomando instalar-whisper.", 3)
    if not modelo_ok(modelo):
        falhar("o modelo de transcrição não está baixado. Rode o subcomando instalar-whisper.", 3)
    # O áudio e a saída usam nomes simples dentro da pasta de trabalho (cwd), e o modelo
    # usa o nome curto do Windows quando o caminho tem acento (ex.: C:\Users\João).
    base = [
        exe, "-m", caminho_sem_acento(caminho_modelo(modelo)), "-f", wav.name, "-l", "pt", "-t", str(threads),
        "-ojf", "-of", "transcricao", "-np", "-sns",
    ]
    if prompt:
        base += ["--prompt", prompt]
    # O alinhamento DTW dá o tempo certo de cada palavra; ele exige a "flash attention"
    # desligada (-nfa). Versões antigas do whisper.cpp não têm essas opções: tenta sem elas.
    tentativas = [base + ["-dtw", modelo, "-nfa"], base + ["-dtw", modelo], base]
    r = None
    for cmd in tentativas:
        r = rodar(cmd, cwd=str(pasta))
        if r.returncode == 0 and (pasta / "transcricao.json").is_file():
            return
    falhar("a transcrição falhou. Detalhe técnico: " + (r.stderr or r.stdout)[-600:])


def ler_palavras(arquivo):
    """Monta a lista de palavras a partir do JSON completo do whisper.cpp.

    O tempo de cada palavra vem do alinhamento DTW (t_dtw), que acompanha a fala de perto.
    Sem DTW, usa o tempo dos tokens, que costuma adiantar a primeira palavra de cada frase;
    a função ajustar_tempos corrige isso com o volume do áudio."""
    bruto = arquivo.read_bytes().decode("utf-8", errors="surrogateescape")
    dados = json.loads(bruto)
    palavras = []

    def fechar(tokens, seg_id):
        if not tokens:
            return
        texto = "".join(t["text"] for t in tokens)
        texto = texto.encode("utf-8", errors="surrogateescape").decode("utf-8", errors="replace").strip()
        if not texto or not normalizar(texto):
            if palavras and texto and palavras[-1]["seg"] == seg_id:
                palavras[-1]["texto"] += texto  # pontuação solta gruda na palavra anterior
            return
        if re.search(r"(\w)\1{4,}", texto):
            return  # "Beeeeee", "Hmmmmm": som que não é fala (apito, música, ruído)
        dtw = tokens[0].get("t_dtw", -1)
        palavras.append({
            "texto": texto, "seg": seg_id,
            "ini_tok": tokens[0]["offsets"]["from"] / 1000.0,
            "fim_tok": tokens[-1]["offsets"]["to"] / 1000.0,
            "dtw": dtw / 100.0 if isinstance(dtw, (int, float)) and dtw >= 0 else None,
        })

    for seg_id, seg in enumerate(dados.get("transcription", [])):
        texto_seg = (seg.get("text") or "").strip()
        if re.fullmatch(r"[\[\(].*[\]\)]", texto_seg):
            continue  # [Música], (risos) e afins
        atual = []
        for tok in seg.get("tokens", []):
            t = tok.get("text", "")
            if t.startswith("[_") or "offsets" not in tok:
                continue
            if t.startswith(" ") and atual:
                fechar(atual, seg_id)
                atual = []
            atual.append(tok)
        fechar(atual, seg_id)

    usa_dtw = bool(palavras) and all(p["dtw"] is not None for p in palavras)
    for p in palavras:
        # O DTW marca a palavra uns 0,1 s depois de ela começar.
        p["ini"] = max(0.0, p["dtw"] - 0.1) if usa_dtw else p["ini_tok"]
        p["fim"] = p["ini"] + 0.05
        p["norm"] = normalizar(p["texto"])
    return palavras, usa_dtw


def dentro_de_pausa(t, silencios, margem=0.05):
    for s, e in silencios:
        if s + margem < t < e - margem:
            return (s, e)
    return None


def remover_alucinacoes(palavras, silencios):
    """O whisper às vezes 'ouve' frases no silêncio (ex.: "Obrigado.", "Legendas pela
    comunidade..."). Descarta a frase inteira quando todas as palavras dela caem em pausa longa."""
    longos = [(s, e) for s, e in silencios if e - s >= 0.8]
    por_seg = {}
    for p in palavras:
        por_seg.setdefault(p["seg"], []).append(p)
    descartar = {seg for seg, ps in por_seg.items()
                 if all(dentro_de_pausa(p["ini"], longos, 0.15) for p in ps)}
    return [p for p in palavras if p["seg"] not in descartar]


def ajustar_tempos(palavras, silencios, duracao):
    """Acerta início e fim de cada palavra usando o volume do áudio."""
    inicios_fala = [e for s, e in silencios if e < duracao - 0.02]
    for i, p in enumerate(palavras):
        if i:
            p["ini"] = max(p["ini"], palavras[i - 1]["ini"] + 0.02)
        pausa = dentro_de_pausa(p["ini"], silencios)
        if pausa and pausa[1] - p["ini"] <= 1.5 and pausa[1] < duracao - 0.02:
            p["ini"] = pausa[1]  # palavra marcada no meio da pausa: vai para onde a fala começa
        elif inicios_fala:
            perto = min(inicios_fala, key=lambda o: abs(o - p["ini"]))
            if abs(perto - p["ini"]) <= 0.25:
                p["ini"] = perto
        if i:
            p["ini"] = max(p["ini"], palavras[i - 1]["ini"] + 0.02)
    for i, p in enumerate(palavras):
        limite = palavras[i + 1]["ini"] if i + 1 < len(palavras) else min(duracao, p["ini"] + 1.0)
        fim = limite
        for s, e in silencios:
            if s >= p["ini"] + 0.08 and s < limite and e - s >= 0.15:
                fim = s  # a palavra termina onde começa a pausa
                break
        p["fim"] = max(p["ini"] + 0.05, fim)
    return palavras


# ----------------------------------------------------------------------------
# Volume e silêncios
# ----------------------------------------------------------------------------

def extrair_audio(video, wav):
    r = rodar([
        "ffmpeg", "-y", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000",
        "-af", "aresample=async=1:first_pts=0", "-c:a", "pcm_s16le", wav,
    ])
    if r.returncode != 0:
        falhar("não consegui extrair o áudio do vídeo. Detalhe técnico: " + r.stderr[-400:])


def volume_por_bloco(wav):
    with wave.open(str(wav)) as w:
        taxa = w.getframerate()
        dados = array.array("h", w.readframes(w.getnframes()))
    if sys.byteorder == "big":
        dados.byteswap()
    tam = max(1, int(taxa * PASSO))
    db = []
    for i in range(0, len(dados) - tam + 1, tam):
        bloco = dados[i:i + tam]
        soma = sum(map(operator.mul, bloco, bloco))
        rms = math.sqrt(soma / tam)
        db.append(20 * math.log10(rms / 32768.0) if rms > 0 else -100.0)
    return db


def achar_silencios(db):
    """Devolve (silêncios em segundos, limiar, ruído, fala)."""
    if not db:
        return [], -40.0, -60.0, -20.0
    ordenado = sorted(db)
    ruido = ordenado[int(0.05 * (len(ordenado) - 1))]
    fala = ordenado[int(0.95 * (len(ordenado) - 1))]
    limiar = ruido + max(6.0, 0.3 * (fala - ruido))
    limiar = min(limiar, fala - 10.0)
    eh_fala = [v >= limiar for v in db]
    # Estalos curtos (menos de 60 ms) no meio do silêncio não contam como fala.
    minimo_fala = int(round(0.06 / PASSO))
    i = 0
    while i < len(eh_fala):
        if eh_fala[i]:
            j = i
            while j < len(eh_fala) and eh_fala[j]:
                j += 1
            if j - i < minimo_fala:
                for k in range(i, j):
                    eh_fala[k] = False
            i = j
        else:
            i += 1
    silencios = []
    i = 0
    while i < len(eh_fala):
        if not eh_fala[i]:
            j = i
            while j < len(eh_fala) and not eh_fala[j]:
                j += 1
            silencios.append((i * PASSO, j * PASSO))
            i = j
        else:
            i += 1
    return silencios, limiar, ruido, fala


def inicio_de_fala_proximo(t, silencios, duracao, tolerancia=0.35):
    melhor = None
    for s, e in silencios:
        if e >= duracao - 0.02:
            continue
        d = abs(e - t)
        if d <= tolerancia and (melhor is None or d < melhor[0]):
            melhor = (d, s, e)
    return (melhor[1], melhor[2]) if melhor else None


def ponto_de_corte(t_palavra, silencios, duracao, folga):
    """Ponto de corte logo antes de uma palavra: dentro da pausa, com a folga antes da fala."""
    achado = inicio_de_fala_proximo(t_palavra, silencios, duracao)
    if achado:
        s, e = achado
        return max(e - folga, (s + e) / 2.0)
    return max(0.0, t_palavra - 0.03)


# ----------------------------------------------------------------------------
# Trechos e erros
# ----------------------------------------------------------------------------

def ha_pausa_entre(a, b, silencios, minimo=0.3):
    if b["ini"] - a["fim"] >= minimo:
        return True
    m1 = (a["ini"] + a["fim"]) / 2.0
    m2 = (b["ini"] + b["fim"]) / 2.0
    for s, e in silencios:
        if e - s >= minimo and m1 <= (s + e) / 2.0 <= m2:
            return True
    return False


def montar_trechos(palavras, silencios):
    trechos, atual = [], []
    for i, p in enumerate(palavras):
        if atual:
            ant = palavras[i - 1]
            if ant["texto"].endswith(PONTUACAO_FINAL) or ha_pausa_entre(ant, p, silencios):
                trechos.append(atual)
                atual = []
        atual.append(i)
    if atual:
        trechos.append(atual)
    return [{"id": "T%d" % (n + 1), "palavras": idx} for n, idx in enumerate(trechos)]


def casamento(a, b):
    """Maior sequência em comum entre duas listas de palavras (aceita palavra parecida).
    Devolve os índices de 'a' que casaram."""
    n, m = len(a), len(b)
    tab = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if parecidas(a[i], b[j]):
                tab[i][j] = tab[i + 1][j + 1] + 1
            else:
                tab[i][j] = max(tab[i + 1][j], tab[i][j + 1])
    casados, i, j = [], 0, 0
    while i < n and j < m:
        if parecidas(a[i], b[j]) and tab[i][j] == tab[i + 1][j + 1] + 1:
            casados.append(i)
            i += 1
            j += 1
        elif tab[i + 1][j] >= tab[i][j + 1]:
            i += 1
        else:
            j += 1
    return casados


def detectar_erros(palavras, trechos):
    """Acha tomadas ruins: a pessoa erra e recomeça. Devolve faixas (k, j) de palavras:
    corta da palavra k até antes da palavra j (onde começa a tomada que fica)."""
    n = len(palavras)
    norm = [p["norm"] for p in palavras]
    trecho_de = {}
    for t, tr in enumerate(trechos):
        for i in tr["palavras"]:
            trecho_de[i] = t
    faixas = []

    # 1) Marcadores de recomeço ("não, peraí", "vou começar de novo"...)
    i = 0
    while i < n:
        achou, forte = None, False
        for marc, eh_forte in MARCADORES:
            if tuple(norm[i:i + len(marc)]) == marc:
                achou, forte = marc, eh_forte
                break
        if not achou:
            i += 1
            continue
        m, r = i, i + len(achou)
        inicio = None
        if r + 1 < n:
            for k in range(m - 1, max(-1, m - 31), -1):
                if palavras[m]["ini"] - palavras[k]["ini"] > 20:
                    break
                if k + 1 < m and norm[k] == norm[r] and norm[k + 1] == norm[r + 1]:
                    inicio = k
                    break
        t = trecho_de[m]
        idx_trecho = trechos[t]["palavras"]
        curto = len(idx_trecho) - len(achou) <= 2
        if inicio is None and curto and forte:
            if idx_trecho[0] == m and t > 0:
                inicio = trechos[t - 1]["palavras"][0]
            else:
                inicio = idx_trecho[0]
        if inicio is not None:
            faixas.append((inicio, r, "recomeço depois de \"%s\"" % " ".join(
                palavras[x]["texto"].strip(",.!?") for x in range(m, r))))
        i = r

    # 2) Frase repetida: a pessoa recomeça a mesma frase (fica a última tomada).
    # A tomada ruim começa no início de um trecho ou depois de pontuação, e não
    # atravessa o fim de outra frase.
    inicios_trecho = {tr["palavras"][0] for tr in trechos}
    k = 0
    while k < n - 2:
        if not (k == 0 or k in inicios_trecho or re.search(r"[,.;:?!…]$", palavras[k - 1]["texto"])):
            k += 1
            continue
        achou = False
        for j in range(k + 2, min(n - 1, k + 31)):
            tam = j - k
            mm = 3 if tam >= 3 else 2
            if j + mm > n:
                break
            if palavras[j]["ini"] - palavras[k]["ini"] > 20:
                break
            if any(palavras[x]["texto"].endswith(PONTUACAO_FINAL) for x in range(k, j - 1)):
                break
            if norm[j:j + mm] != norm[k:k + mm]:
                continue
            ruim = norm[k:j]
            seguinte = norm[j:j + tam + 8]
            casados = casamento(ruim, seguinte)
            if len(casados) / float(tam) < 0.75:
                continue
            soltos = [x for x in range(tam) if x not in casados]
            fecha_frase = palavras[j - 1]["texto"].endswith(PONTUACAO_FINAL)
            if soltos and fecha_frase:
                # Frases paralelas ("Você não precisa de X. Você não precisa de Y."): as duas
                # são completas, têm tamanho parecido e trocam uma palavra de verdade.
                tam_seguinte = 0
                for x in range(j, min(n, j + tam + 8)):
                    tam_seguinte += 1
                    if palavras[x]["texto"].endswith(PONTUACAO_FINAL):
                        break
                if min(soltos) >= 0.6 * tam or 0.75 <= tam_seguinte / float(tam) <= 1.34:
                    continue
            faixas.append((k, j, "frase repetida, fica a última tomada"))
            k = j
            achou = True
            break
        if not achou:
            k += 1

    # Junta faixas que se encostam
    faixas.sort()
    juntas = []
    for k, j, motivo in faixas:
        if juntas and k <= juntas[-1][1]:
            pk, pj, pm = juntas[-1]
            motivos = pm if motivo in pm else pm + "; " + motivo
            juntas[-1] = (pk, max(pj, j), motivos)
        else:
            juntas.append((k, j, motivo))
    return juntas


# ----------------------------------------------------------------------------
# Plano de cortes
# ----------------------------------------------------------------------------

def unir(faixas):
    faixas = sorted((a, b) for a, b in faixas if b > a)
    out = []
    for a, b in faixas:
        if out and a <= out[-1][1] + 1e-6:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def trechos_mantidos(cortes, duracao, fps):
    cortes = unir([(max(0.0, a), min(duracao, b)) for a, b in cortes])
    manter, t = [], 0.0
    for a, b in cortes:
        if a - t > 0:
            manter.append((t, a))
        t = max(t, b)
    if duracao - t > 0:
        manter.append((t, duracao))
    f = float(fps)
    ajustado = []
    for a, b in manter:
        a2 = round(a * f) / f
        b2 = min(duracao, round(b * f) / f)
        if b2 - a2 >= max(0.1, 2.0 / f):
            if ajustado and a2 - ajustado[-1][1] < 1.5 / f:
                ajustado[-1] = (ajustado[-1][0], b2)  # corte menor que um quadro: ignora
            else:
                ajustado.append((a2, b2))
    return ajustado


def novo_tempo(t, manter):
    acumulado = 0.0
    for a, b in manter:
        if t < a:
            return None
        if t <= b:
            return acumulado + (t - a)
        acumulado += b - a
    return None


def remapear_palavras(palavras, manter):
    saida = []
    for p in palavras:
        meio = (p["ini"] + p["fim"]) / 2.0
        for a, b in manter:
            if a <= meio <= b:
                ini = novo_tempo(max(p["ini"], a), manter)
                fim = novo_tempo(min(p["fim"], b), manter)
                saida.append(dict(p, ini=ini, fim=max(fim, ini + 0.05)))
                break
    # Quando o corte tira o começo da frase, a tomada que fica pode começar em minúscula.
    for i, p in enumerate(saida):
        if (i == 0 or saida[i - 1]["texto"].endswith(PONTUACAO_FINAL)) and p["texto"][:1].islower():
            p["texto"] = p["texto"][:1].upper() + p["texto"][1:]
    return saida


def aplicar_trocas(palavras, trocas):
    """Corrige palavras da transcrição. Cada troca é 'errado=>certo' (aceita várias palavras)."""
    for troca in trocas:
        if "=>" not in troca:
            falhar("troca em formato inválido: %s (use errado=>certo)" % troca)
        errado, certo = [x.strip() for x in troca.split("=>", 1)]
        alvo = [normalizar(x) for x in errado.split() if normalizar(x)]
        if not alvo:
            continue
        i = 0
        while i <= len(palavras) - len(alvo):
            if [p["norm"] for p in palavras[i:i + len(alvo)]] == alvo:
                ultimo = palavras[i + len(alvo) - 1]
                pont = re.search(r"[,.!?…:;]+$", ultimo["texto"])
                nova = dict(palavras[i], texto=certo + (pont.group(0) if pont else ""),
                            fim=ultimo["fim"], norm=normalizar(certo))
                palavras[i:i + len(alvo)] = [nova]
            i += 1
    return palavras


def montar_blocos(palavras, max_palavras=3, max_letras=16):
    blocos, atual = [], []
    for i, p in enumerate(palavras):
        if atual:
            ant = atual[-1]
            texto = " ".join(x["texto"] for x in atual + [p])
            if (len(atual) >= max_palavras or len(texto) > max_letras
                    or p["ini"] - ant["fim"] > 0.5 or ant["texto"].endswith(PONTUACAO_FINAL)
                    or (ant["texto"].endswith(",") and len(atual) >= 2)):
                blocos.append(atual)
                atual = []
        atual.append(p)
    if atual:
        blocos.append(atual)
    cues = []
    for n, b in enumerate(blocos):
        ini = b[0]["ini"] - 0.05
        fim = b[-1]["fim"]
        if cues:
            ini = max(ini, cues[-1][1])
        prox = blocos[n + 1][0]["ini"] - 0.05 if n + 1 < len(blocos) else None
        if prox is not None and prox - fim < 0.35:
            fim = prox
        else:
            fim = fim + 0.15
        if fim - ini < 0.5:
            fim = ini + 0.5 if prox is None else min(ini + 0.5, max(prox, fim))
        cues.append((ini, fim, " ".join(x["texto"] for x in b)))
    return cues


def escrever_srt(cues, destino):
    linhas = []
    for n, (a, b, texto) in enumerate(cues, 1):
        linhas += [str(n), "%s --> %s" % (fmt_srt(a), fmt_srt(b)), texto, ""]
    destino.write_text("\n".join(linhas), encoding="utf-8")


def ler_srt(origem):
    texto = origem.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    cues = []
    for bloco in re.split(r"\n\s*\n", texto.strip()):
        linhas = [l for l in bloco.split("\n") if l.strip()]
        for idx, l in enumerate(linhas):
            m = re.match(r"\s*(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", l)
            if m:
                g = [int(x) for x in m.groups()]
                a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000.0
                b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000.0
                cues.append((a, b, " ".join(linhas[idx + 1:]).strip()))
                break
    return cues


# ----------------------------------------------------------------------------
# preparar
# ----------------------------------------------------------------------------

def cmd_preparar(a):
    if not ffmpeg_ok():
        falhar("o FFmpeg não está instalado.", 2)
    video = Path(a.video).resolve()
    if not video.is_file():
        falhar("vídeo não encontrado: %s" % video)
    pasta = Path(a.pasta).resolve()
    pasta.mkdir(parents=True, exist_ok=True)
    info = info_video(video)
    if not info["tem_audio"]:
        falhar("o vídeo não tem áudio, então não dá para legendar nem achar erros e pausas.")
    ritmo = RITMOS[a.ritmo]
    folga = ritmo["folga"]
    duracao = info["duracao"]

    # Cache: só refaz áudio e transcrição se o vídeo ou o modelo mudarem.
    marca = {"video": str(video), "tamanho": video.stat().st_size,
             "data": int(video.stat().st_mtime), "modelo": a.modelo, "prompt": a.prompt or ""}
    arq_cache = pasta / "cache.json"
    cache = json.loads(arq_cache.read_text(encoding="utf-8")) if arq_cache.is_file() else {}
    wav = pasta / "audio.wav"
    arq_trans = pasta / "transcricao.json"
    mesmo_video = all(cache.get(k) == marca[k] for k in ("video", "tamanho", "data"))
    if not (mesmo_video and wav.is_file()):
        extrair_audio(video, wav)
        if arq_trans.is_file():
            arq_trans.unlink()
    db = volume_por_bloco(wav)
    silencios, limiar, ruido, fala = achar_silencios(db)

    precisa_texto = a.legenda or a.erros or bool(a.cortar_trechos)
    palavras = []
    if precisa_texto:
        if not (cache == marca and arq_trans.is_file()):
            transcrever(wav, pasta, a.modelo, a.threads or threads_padrao(), a.prompt)
        arq_cache.write_text(json.dumps(marca, ensure_ascii=False), encoding="utf-8")
        palavras, usa_dtw = ler_palavras(arq_trans)
        if usa_dtw:
            palavras = remover_alucinacoes(palavras, silencios)
        palavras = ajustar_tempos(palavras, silencios, duracao)
        palavras = aplicar_trocas(palavras, a.trocar or [])
    else:
        arq_cache.write_text(json.dumps(marca, ensure_ascii=False), encoding="utf-8")

    trechos = montar_trechos(palavras, silencios)
    cortes = []  # (ini, fim, tipo, id, texto)

    erros = []
    if a.erros and palavras:
        descartar = {x.strip().upper() for x in ",".join(a.manter_erros or []).split(",") if x.strip()}
        for n, (k, j, motivo) in enumerate(detectar_erros(palavras, trechos), 1):
            ini = ponto_de_corte(palavras[k]["ini"], silencios, duracao, folga)
            fim = ponto_de_corte(palavras[j]["ini"], silencios, duracao, folga) if j < len(palavras) else duracao
            if fim - ini < 0.1:
                continue
            e = {"id": "E%d" % n, "ini": ini, "fim": fim, "motivo": motivo,
                 "texto": " ".join(palavras[x]["texto"] for x in range(k, j)),
                 "palavras": [k, j], "aplicado": ("E%d" % n) not in descartar}
            erros.append(e)
            if e["aplicado"]:
                cortes.append((ini, fim, "erro", e["id"], e["texto"]))

    if a.cortar_trechos:
        pedidos = {x.strip().upper() for x in ",".join(a.cortar_trechos).split(",") if x.strip()}
        for tr in trechos:
            if tr["id"] in pedidos:
                k, j = tr["palavras"][0], tr["palavras"][-1] + 1
                ini = ponto_de_corte(palavras[k]["ini"], silencios, duracao, folga)
                fim = ponto_de_corte(palavras[j]["ini"], silencios, duracao, folga) if j < len(palavras) else duracao
                cortes.append((ini, fim, "manual", tr["id"], " ".join(palavras[x]["texto"] for x in range(k, j))))

    for faixa in a.cortar or []:
        m = re.fullmatch(r"\s*([\d.,]+)\s*-\s*([\d.,]+)\s*", faixa)
        if not m:
            falhar("faixa de corte inválida: %s (use 12.3-14.1, em segundos do vídeo original)" % faixa)
        ini, fim = float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        cortes.append((ini, fim, "manual", "faixa", ""))

    pausas = []
    if a.silencios:
        for s, e in silencios:
            if e - s < ritmo["pausa_min"]:
                continue
            ini = 0.0 if s <= 0.001 else s + folga
            fim = duracao if e >= min(duracao, len(db) * PASSO) - 0.02 else e - folga
            if fim - ini >= 0.05:
                pausas.append((ini, fim))
                cortes.append((ini, fim, "silencio", "", ""))

    manter = trechos_mantidos([(c[0], c[1]) for c in cortes], duracao, info["fps"])
    duracao_final = sum(b - a_ for a_, b in manter)

    # A legenda é sempre refeita junto com o plano: uma legenda antiga ficaria fora de tempo.
    legenda_srt = pasta / "legendas.srt"
    if legenda_srt.is_file():
        legenda_srt.unlink()
    if a.legenda and palavras:
        escrever_srt(montar_blocos(remapear_palavras(palavras, manter)), legenda_srt)
    else:
        legenda_srt = None

    plano = {
        "video": str(video), "duracao": duracao, "duracao_final": duracao_final,
        "fps": str(info["fps"]), "largura": info["largura"], "altura": info["altura"],
        "ritmo": a.ritmo, "etapas": {"legenda": a.legenda, "erros": a.erros, "silencios": a.silencios},
        "manter": [[round(x, 4), round(y, 4)] for x, y in manter],
        "erros": erros, "pausas_cortadas": len(pausas),
        "volume": {"limiar_db": round(limiar, 1), "ruido_db": round(ruido, 1), "fala_db": round(fala, 1)},
    }
    (pasta / "plano.json").write_text(json.dumps(plano, ensure_ascii=False, indent=1), encoding="utf-8")
    (pasta / "palavras.json").write_text(json.dumps({"palavras": palavras, "trechos": trechos},
                                                    ensure_ascii=False, indent=1), encoding="utf-8")

    # Resumo para o Claude ler
    print("RESUMO DA ANÁLISE")
    print("Vídeo: %s | %s | %dx%d | %s qps" % (video.name, fmt(duracao), info["largura"], info["altura"],
                                               round(float(info["fps"]), 2)))
    etapas = [n for n, v in (("legenda", a.legenda), ("erros", a.erros), ("silêncios", a.silencios)) if v]
    print("Etapas: " + ", ".join(etapas))
    if precisa_texto and not palavras:
        print("")
        print("AVISO: nenhuma fala foi reconhecida (vídeo sem voz ou só com música). "
              "Não há legenda nem erros para cortar.")
    if palavras:
        corte_de = {}
        for e in erros:
            for x in range(*e["palavras"]):
                corte_de[x] = e["id"] + ("" if e["aplicado"] else " (mantido)")
        print("")
        print("TRANSCRIÇÃO (por trecho, tempos do vídeo original)")
        for tr in trechos:
            idx = tr["palavras"]
            marcas = sorted({corte_de[x] for x in idx if x in corte_de})
            print("%s [%s a %s] %s%s" % (
                tr["id"], fmt(palavras[idx[0]]["ini"]), fmt(palavras[idx[-1]]["fim"]),
                " ".join(palavras[x]["texto"] for x in idx),
                ("   << erro " + ", ".join(marcas)) if marcas else ""))
    if a.erros:
        print("")
        print("ERROS ENCONTRADOS")
        if not erros:
            print("Nenhum recomeço ou frase repetida encontrado.")
        for e in erros:
            print("%s [%s a %s] %s%s: \"%s\"" % (
                e["id"], fmt(e["ini"]), fmt(e["fim"]), e["motivo"],
                "" if e["aplicado"] else " (MANTIDO, não será cortado)", e["texto"]))
    if a.silencios:
        total = sum(b - a_ for a_, b in pausas)
        print("")
        print("PAUSAS")
        nome_ritmo = {"dinamico": "dinâmico"}.get(a.ritmo, a.ritmo)
        print("%d pausas cortadas, somando %.1f s (ritmo %s: pausas a partir de %.2f s, folga de %.2f s)."
              % (len(pausas), total, nome_ritmo, ritmo["pausa_min"], folga))
    print("")
    print("RESULTADO")
    print("Duração: %s -> %s (%d trechos mantidos)" % (fmt(duracao), fmt(duracao_final), len(manter)))
    print("Plano: %s" % (pasta / "plano.json"))
    if legenda_srt:
        print("Legenda: %s" % legenda_srt)


# ----------------------------------------------------------------------------
# renderizar
# ----------------------------------------------------------------------------

CORES = {
    "amarelo": "#FFE600", "verde": "#3DFF5A", "ciano": "#2EE6FF", "laranja": "#FF8A00",
    "rosa": "#FF4FB8", "branco": "#FFFFFF", "vermelho": "#FF3B3B",
}


def cor_ass(cor):
    hexa = CORES.get(cor.lower(), cor).lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", hexa):
        falhar("cor inválida: %s (use um nome da lista ou #RRGGBB)" % cor)
    r, g, b = hexa[0:2], hexa[2:4], hexa[4:6]
    return ("&H%s%s%s&" % (b, g, r)).upper()


def achar_fonte():
    """Copia uma fonte em negrito do sistema para a pasta de trabalho (Windows, Mac ou Linux)."""
    candidatos = [
        ("Arial", Path("C:/Windows/Fonts/arialbd.ttf")),
        ("Arial", Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")),
        ("Arial", Path("/Library/Fonts/Arial Bold.ttf")),
        ("DejaVu Sans", Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")),
        ("Liberation Sans", Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")),
    ]
    for nome, caminho in candidatos:
        if caminho.is_file():
            return nome, caminho
    return "Arial", None


def palavras_da_legenda(texto, maiusculas, manter_pontuacao):
    palavras = texto.split()
    saida = []
    for p in palavras:
        if not manter_pontuacao:
            p = re.sub(r"[,.;:…]+$", "", p)
        if maiusculas:
            p = p.upper()
        p = p.replace("\\", "/").replace("{", "(").replace("}", ")")
        if p:
            saida.append(p)
    return saida


def escrever_ass(cues, destino, largura, altura, a, fonte):
    vertical = altura >= largura
    tamanho = round(largura * 0.085) if vertical else round(altura * 0.065)
    contorno = max(2, round(tamanho * 0.09))
    sombra = max(1, round(tamanho * 0.04))
    if a.posicao == "centro":
        alinhamento, margem_v = 5, 0
    else:  # área segura do Reels e Stories: fora dos 35% de baixo
        alinhamento, margem_v = 2, round(altura * (0.35 if vertical else 0.08))
    margem_l = round(largura * 0.07)
    destaque = cor_ass(a.cor)
    cab = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: %d" % largura, "PlayResY: %d" % altura,
        "WrapStyle: 0", "ScaledBorderAndShadow: yes", "YCbCr Matrix: TV.709", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
        "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Legenda,%s,%d,&H00FFFFFF,&H000000FF,&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,%d,%d,%d,%d,%d,%d,1"
        % (fonte, tamanho, contorno, sombra, alinhamento, margem_l, margem_l, margem_v),
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    eventos = []
    for ini, fim, texto in cues:
        palavras = palavras_da_legenda(texto, a.maiusculas, a.manter_pontuacao)
        if not palavras:
            continue
        if a.estilo == "simples":
            eventos.append((ini, fim, " ".join(palavras)))
            continue
        # Destaque na palavra falada: o tempo do bloco é dividido pelo tamanho de cada palavra.
        pesos = [len(p) + 2 for p in palavras]
        total = float(sum(pesos))
        t = ini
        for i, p in enumerate(palavras):
            fim_p = fim if i == len(palavras) - 1 else t + (fim - ini) * pesos[i] / total
            texto_ev = " ".join(
                ("{\\c%s}%s{\\r}" % (destaque, w)) if k == i else w for k, w in enumerate(palavras))
            eventos.append((t, fim_p, texto_ev))
            t = fim_p
    linhas = cab + ["Dialogue: 0,%s,%s,Legenda,,0,0,0,,%s" % (fmt_ass(x), fmt_ass(y), z)
                    for x, y, z in eventos if y > x]
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def cmd_renderizar(a):
    if not ffmpeg_ok():
        falhar("o FFmpeg não está instalado.", 2)
    video = Path(a.video).resolve()
    pasta = Path(a.pasta).resolve()
    saida = Path(a.saida).resolve()
    if saida == video:
        falhar("a saída não pode ter o mesmo nome do vídeo original.")
    info = info_video(video)
    arq_plano = pasta / "plano.json"
    if arq_plano.is_file():
        plano = json.loads(arq_plano.read_text(encoding="utf-8"))
        if Path(plano.get("video", "")) != video:
            falhar("o plano.json desta pasta é de outro vídeo. Rode o preparar de novo.")
        fps = Fraction(plano.get("fps", "30"))
        manter = [tuple(x) for x in plano["manter"]] or [(0.0, info["duracao"])]
    else:
        # Sem plano: nenhum corte (ex.: o aluno já tem um .srt pronto e só quer queimar a legenda).
        pasta.mkdir(parents=True, exist_ok=True)
        fps = info["fps"]
        manter = [(0.0, info["duracao"])]
    largura, altura = info["largura"], info["altura"]

    filtros_v = ["fps=%s" % fps]
    if a.vertical and largura / float(altura) > 9 / 16.0 + 0.01:
        filtros_v.append("crop=trunc(ih*9/32)*2:ih,scale=1080:1920,setsar=1")
        largura, altura = 1080, 1920
    elif min(largura, altura) > a.max_resolucao:
        # Vídeo 4K vira 1080p: fica bem mais leve de codificar num computador comum.
        if largura <= altura:
            novo_l = a.max_resolucao
            novo_a = int(round(altura * a.max_resolucao / float(largura) / 2)) * 2
        else:
            novo_a = a.max_resolucao
            novo_l = int(round(largura * a.max_resolucao / float(altura) / 2)) * 2
        filtros_v.append("scale=%d:%d,setsar=1" % (novo_l, novo_a))
        largura, altura = novo_l, novo_a

    queimar = a.queimar_legenda
    if queimar:
        srt = pasta / "legendas.srt"
        if not srt.is_file():
            falhar("não há legenda para queimar. Rode o preparar com --legenda; se ele avisou que "
                   "não reconheceu fala, o vídeo não tem o que legendar.")
        nome_fonte, arq_fonte = achar_fonte()
        if arq_fonte:
            (pasta / "fontes").mkdir(exist_ok=True)
            shutil.copy(arq_fonte, pasta / "fontes" / arq_fonte.name)
        escrever_ass(ler_srt(srt), pasta / "legendas.ass", largura, altura, a, nome_fonte)
        pos = "ass=legendas.ass" + (":fontsdir=fontes" if arq_fonte else "") + ","
    else:
        pos = ""

    n = len(manter)
    linhas = [
        "[0:v]%s,split=%d%s" % (",".join(filtros_v), n, "".join("[vs%d]" % i for i in range(n))),
        "[0:a]aresample=48000:async=1:first_pts=0,asplit=%d%s" % (n, "".join("[as%d]" % i for i in range(n))),
    ]
    for i, (ini, fim) in enumerate(manter):
        dur = fim - ini
        fade = min(0.01, dur / 4.0)
        linhas.append("[vs%d]trim=start=%.4f:end=%.4f,setpts=PTS-STARTPTS[v%d]" % (i, ini, fim, i))
        linhas.append("[as%d]atrim=start=%.4f:end=%.4f,asetpts=PTS-STARTPTS,"
                      "afade=t=in:d=%.4f,afade=t=out:st=%.4f:d=%.4f[a%d]"
                      % (i, ini, fim, fade, max(0.0, dur - fade), fade, i))
    linhas.append("%sconcat=n=%d:v=1:a=1[vc][ac]" % ("".join("[v%d][a%d]" % (i, i) for i in range(n)), n))
    linhas.append("[vc]%sformat=yuv420p[vout]" % pos)
    (pasta / "filtro.txt").write_text(";\n".join(linhas) + "\n", encoding="utf-8")

    opcao_filtro = ["-/filter_complex", "filtro.txt"] if versao_ffmpeg() >= 7 else \
        ["-filter_complex_script", "filtro.txt"]
    saida.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-v", "error", "-i", str(video)] + opcao_filtro + [
        "-map", "[vout]", "-map", "[ac]", "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(saida),
    ]
    r = rodar(cmd, cwd=str(pasta))
    if r.returncode != 0 or not saida.is_file():
        falhar("o FFmpeg não conseguiu gerar o vídeo. Detalhe técnico: " + r.stderr[-800:])
    final = info_video(saida)
    print("VÍDEO PRONTO")
    print("Arquivo: %s" % saida)
    print("Duração: %s (antes: %s)" % (fmt(final["duracao"]), fmt(info["duracao"])))
    print("Formato: %dx%d" % (final["largura"], final["altura"]))
    print("Tamanho: %.1f MB" % (saida.stat().st_size / 1024.0 / 1024.0))
    print("Legenda queimada: %s" % ("sim" if queimar else "não"))


# ----------------------------------------------------------------------------
# Linha de comando
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Edição automática da fala: legenda, erros e silêncios.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("verificar")
    v.add_argument("--modelo", default="small", choices=["small", "base"])

    w = sub.add_parser("instalar-whisper")
    w.add_argument("--modelo", default="small", choices=["small", "base"])

    p = sub.add_parser("preparar")
    p.add_argument("--video", required=True)
    p.add_argument("--pasta", required=True, help="pasta de trabalho (temporária)")
    p.add_argument("--legenda", action="store_true")
    p.add_argument("--erros", action="store_true")
    p.add_argument("--silencios", action="store_true")
    p.add_argument("--ritmo", default="dinamico", choices=list(RITMOS))
    p.add_argument("--modelo", default="small", choices=["small", "base"])
    p.add_argument("--threads", type=int, default=0)
    p.add_argument("--prompt", default="", help="palavras do nicho para ajudar a transcrição")
    p.add_argument("--manter-erros", action="append", help="IDs de erros sugeridos que NÃO devem ser cortados (ex.: E2)")
    p.add_argument("--cortar-trechos", action="append", help="IDs de trechos a cortar (ex.: T5,T6)")
    p.add_argument("--cortar", action="append", help="faixa em segundos do vídeo original (ex.: 12.3-14.1)")
    p.add_argument("--trocar", action="append", help="correção de palavra: errado=>certo")

    r = sub.add_parser("renderizar")
    r.add_argument("--video", required=True)
    r.add_argument("--pasta", required=True)
    r.add_argument("--saida", required=True)
    r.add_argument("--queimar-legenda", action="store_true")
    r.add_argument("--estilo", default="destaque", choices=["destaque", "simples"])
    r.add_argument("--cor", default="amarelo", help="cor do destaque: nome ou #RRGGBB")
    r.add_argument("--posicao", default="segura", choices=["segura", "centro"])
    r.add_argument("--maiusculas", action="store_true")
    r.add_argument("--manter-pontuacao", action="store_true")
    r.add_argument("--vertical", action="store_true", help="converte vídeo deitado para 9:16 (corte central)")
    r.add_argument("--max-resolucao", type=int, default=1080)
    r.add_argument("--preset", default="veryfast")
    r.add_argument("--crf", type=int, default=20)

    a = ap.parse_args()
    {"verificar": cmd_verificar, "instalar-whisper": cmd_instalar_whisper,
     "preparar": cmd_preparar, "renderizar": cmd_renderizar}[a.cmd](a)


if __name__ == "__main__":
    main()
