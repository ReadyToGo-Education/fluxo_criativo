# Onde ficam as ferramentas pesadas do editor de Reels, fora do git e fora do OneDrive.
# %LOCALAPPDATA%\reels-editar\
#   bin\deep-filter.exe        reduzir ruído (DeepFilterNet v0.5.6, baixado pelo instalar.py)
#   clearvoice\checkpoints\    modelo MossFormer2_SE_48K do aprimorar voz (baixado na primeira execução)
#   trabalho\R0XX\             arquivos intermediários de cada Reel (áudio, transcrição, quadros)
#   ambiente.json              quais Pythons usar (gravado pelo instalar.py)
import json, os, shutil, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SCRIPTS = SKILL / "scripts"
FONTES = SKILL / "fonts"
BASE = Path(os.environ.get("REELS_EDITAR_HOME") or Path(os.environ.get("LOCALAPPDATA", Path.home() / ".cache")) / "reels-editar")
BIN = BASE / "bin"
CLEARVOICE = BASE / "clearvoice"
TRABALHO = BASE / "trabalho"
ARQ_AMBIENTE = BASE / "ambiente.json"
DEEP_FILTER = BIN / ("deep-filter.exe" if os.name == "nt" else "deep-filter")


def ambiente():
    """Comandos de Python: 'whisper' (faster-whisper) e 'voz' (ClearerVoice com PyTorch CUDA)."""
    padrao = {"whisper": [sys.executable], "voz": ["py", "-3.12"] if os.name == "nt" else ["python3"]}
    if ARQ_AMBIENTE.exists():
        padrao.update(json.loads(ARQ_AMBIENTE.read_text(encoding="utf-8")))
    return padrao


def deep_filter():
    if DEEP_FILTER.exists():
        return str(DEEP_FILTER)
    achado = shutil.which("deep-filter")
    if achado:
        return achado
    raise SystemExit("deep-filter não encontrado. Rode a instalação de primeira vez: scripts/instalar.py")
