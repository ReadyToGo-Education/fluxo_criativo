# Aprimorar voz com IA (ClearerVoice, modelo MossFormer2_SE_48K), equivalente ao "Aprimorar voz" do CapCut.
# Roda no Python que tem o PyTorch com placa de vídeo (no computador do Rodrigo, o py -3.12).
# Uso: py -3.12 aprimorar_voz.py entrada.wav saida.wav [intensidade 0 a 100]
# A intensidade mistura a voz aprimorada com a original, como o controle do CapCut (padrão 75).
# O ClearerVoice grava o modelo em ./checkpoints da pasta atual; por isso a pasta atual vira
# %LOCALAPPDATA%\reels-editar\clearvoice, e o modelo (212 MB) é baixado uma vez só.
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente import CLEARVOICE

entrada, saida = (str(Path(a).resolve()) for a in sys.argv[1:3])
intensidade = float(sys.argv[3]) / 100 if len(sys.argv) > 3 else 0.75

import numpy as np
import soundfile as sf
from clearvoice import ClearVoice

CLEARVOICE.mkdir(parents=True, exist_ok=True)
os.chdir(CLEARVOICE)
cv = ClearVoice(task="speech_enhancement", model_names=["MossFormer2_SE_48K"])
aprimorado = np.asarray(cv(input_path=entrada, online_write=False)).squeeze()
original, sr = sf.read(entrada, dtype="float32")
if original.ndim > 1:
    original = original.mean(axis=1)
n = min(len(original), len(aprimorado))
mistura = intensidade * aprimorado[:n] + (1 - intensidade) * original[:n]
sf.write(saida, mistura, sr, subtype="PCM_24")
print(f"voz aprimorada ({intensidade:.0%}): {saida}")
