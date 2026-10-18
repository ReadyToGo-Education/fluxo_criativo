# Transcreve o áudio com o tempo de cada palavra (faster-whisper).
# Usa a placa de vídeo NVIDIA quando as bibliotecas CUDA (pip nvidia-cublas-cu12 / nvidia-cudnn-cu12) estão instaladas.
# Uso: py -3 transcrever.py audio16k.wav palavras.json ["texto do roteiro para orientar a grafia"]
import json, os, sys, time, wave
from pathlib import Path

def _registrar_dlls_cuda():
    try:
        import nvidia
    except ImportError:
        return
    for base in nvidia.__path__:
        for pasta in Path(base).glob("*/bin"):
            os.add_dll_directory(str(pasta))
            os.environ["PATH"] = str(pasta) + os.pathsep + os.environ.get("PATH", "")

_registrar_dlls_cuda()
import numpy as np
from faster_whisper import WhisperModel

audio, saida = sys.argv[1], sys.argv[2]
prompt = sys.argv[3] if len(sys.argv) > 3 else None
t0 = time.time()

wf = wave.open(audio)
dados = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768

def rodar(device, compute):
    modelo = WhisperModel("large-v3-turbo", device=device, compute_type=compute)
    segs, _ = modelo.transcribe(dados, language="pt", word_timestamps=True, initial_prompt=prompt,
                                vad_filter=False, condition_on_previous_text=False)
    return [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)}
            for s in segs for w in s.words]

try:
    palavras, disp = rodar("cuda", "int8_float32"), "placa de vídeo"
except Exception as e:
    print("Placa de vídeo indisponível, usando o processador:", e)
    palavras, disp = rodar("cpu", "int8"), "processador"

json.dump(palavras, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"{len(palavras)} palavras em {time.time() - t0:.1f}s ({disp})")
