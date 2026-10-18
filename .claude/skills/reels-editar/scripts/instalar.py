# Instalação de primeira vez do editor de Reels (e conferência nas vezes seguintes).
# Uso: py -3 instalar.py               confere e instala o que faltar
#      py -3 instalar.py --verificar   só confere; sai com código 1 se faltar algo
# O que entra (nada disso vai para o git):
#   1. FFmpeg no PATH (conferido, não instalado: winget install ffmpeg)
#   2. deep-filter v0.5.6 (DeepFilterNet), baixado do GitHub oficial, com conferência do SHA-256
#   3. faster-whisper + bibliotecas CUDA (nvidia-cublas-cu12, nvidia-cudnn-cu12) neste Python
#   4. ClearerVoice (pip install clearvoice) no Python que tem PyTorch com CUDA
import hashlib, json, os, shutil, subprocess, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente import ARQ_AMBIENTE, BASE, BIN, DEEP_FILTER

SO_VERIFICAR = "--verificar" in sys.argv
DF_URL = "https://github.com/Rikorose/DeepFilterNet/releases/download/v0.5.6/deep-filter-0.5.6-x86_64-pc-windows-msvc.exe"
DF_SHA256 = "75e11fa16445f560cb6b021521ddb89e89270d13b83089705d98776f58fd7915"
faltou = []


def ok(msg): print(f"✅ {msg}")
def falta(msg): print(f"❌ {msg}"); faltou.append(msg)


def roda(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, errors="ignore", timeout=600)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


# 1. FFmpeg
if shutil.which("ffmpeg") and shutil.which("ffprobe"):
    ok("FFmpeg encontrado")
else:
    falta("FFmpeg ausente. Instale com: winget install ffmpeg (e abra um terminal novo)")

# 2. deep-filter
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()

if DEEP_FILTER.exists() and sha256(DEEP_FILTER) == DF_SHA256:
    ok(f"deep-filter v0.5.6 em {DEEP_FILTER}")
elif SO_VERIFICAR or os.name != "nt":
    falta(f"deep-filter ausente em {DEEP_FILTER}" + ("" if os.name == "nt" else " (baixe a versão do seu sistema em github.com/Rikorose/DeepFilterNet/releases/tag/v0.5.6)"))
else:
    BIN.mkdir(parents=True, exist_ok=True)
    tmp = DEEP_FILTER.with_suffix(".baixando")
    print("baixando o deep-filter v0.5.6 do GitHub oficial (26 MB)...")
    urllib.request.urlretrieve(DF_URL, tmp)
    if sha256(tmp) != DF_SHA256:
        tmp.unlink()
        falta("deep-filter baixado não confere com o SHA-256 esperado; arquivo descartado")
    else:
        tmp.replace(DEEP_FILTER)
        ok(f"deep-filter v0.5.6 baixado em {DEEP_FILTER}")

# 3. Whisper neste Python
TESTE_WHISPER = "import faster_whisper, nvidia.cublas, nvidia.cudnn, PIL, numpy; print('ok')"
r = roda([sys.executable, "-c", TESTE_WHISPER])
if not (r and "ok" in r.stdout) and not SO_VERIFICAR:
    print("instalando faster-whisper e as bibliotecas CUDA...")
    roda([sys.executable, "-m", "pip", "install", "-q", "faster-whisper", "nvidia-cublas-cu12", "nvidia-cudnn-cu12", "pillow", "numpy"])
    r = roda([sys.executable, "-c", TESTE_WHISPER])
if r and "ok" in r.stdout:
    ok(f"faster-whisper com bibliotecas CUDA em {sys.executable}")
else:
    falta(f"faster-whisper ausente em {sys.executable}")

# 4. Python com PyTorch CUDA para o ClearerVoice
candidatos = [["py", "-3.12"], ["py", "-3.11"], ["py", "-3.10"], ["py", "-3"], ["python3"], ["python"]] if os.name == "nt" \
    else [["python3.12"], ["python3.11"], ["python3"]]
TESTE_TORCH = "import torch; print('cuda' if torch.cuda.is_available() else 'cpu')"
voz = None
for c in candidatos:
    r = roda(c + ["-c", TESTE_TORCH])
    if r and r.stdout.strip() == "cuda":
        voz = c
        break
if not voz:
    falta("Nenhum Python com PyTorch e placa de vídeo. Instale no Python 3.12: "
          "py -3.12 -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124")
else:
    TESTE_CV = "import clearvoice, soundfile; print('ok')"
    r = roda(voz + ["-c", TESTE_CV])
    if not (r and "ok" in r.stdout) and not SO_VERIFICAR:
        print(f"instalando o ClearerVoice em {' '.join(voz)}...")
        roda(voz + ["-m", "pip", "install", "-q", "clearvoice", "soundfile"])
        r = roda(voz + ["-c", TESTE_CV])
    if r and "ok" in r.stdout:
        ok(f"ClearerVoice com PyTorch CUDA em {' '.join(voz)}")
    else:
        falta(f"ClearerVoice ausente em {' '.join(voz)}")

if not SO_VERIFICAR and voz:
    BASE.mkdir(parents=True, exist_ok=True)
    ARQ_AMBIENTE.write_text(json.dumps({"whisper": [sys.executable], "voz": voz}, indent=1), encoding="utf-8")
    ok(f"ambiente salvo em {ARQ_AMBIENTE}")

if faltou:
    print(f"\nFaltam {len(faltou)} itens.")
    sys.exit(1)
print("\nTudo pronto. O modelo do Whisper (1,6 GB) e o do aprimorar voz (212 MB) são baixados no primeiro Reel.")
