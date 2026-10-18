# Confere o Reel renderizado: quadros-chave com as zonas seguras desenhadas, duração e volume.
# Uso: py -3 conferir.py R0XX
# Lê o plano.json que o editar_reel.py grava e salva conferencia.jpg na pasta de trabalho.
# Quadros: capa (1º quadro), título, cada cartão, cada clique das telas da aula, pico de cada zoom e o fim.
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente import FONTES, TRABALHO

trab = TRABALHO / sys.argv[1]
plano = json.load(open(trab / "plano.json", encoding="utf-8"))
saida, fps = plano["saida"], plano["fps"]
capa = 1 / fps  # o vídeo final começa com 1 quadro de capa

momentos = [("capa", 0.0), ("título", capa + 1.5)]
for k, (t0, t1) in enumerate(plano["cartoes"], 1):
    momentos.append((f"cartão {k}", capa + (t0 + t1) / 2))
for t0, n in plano.get("cliques", []):  # aula só de câmera: a tela de cada clique, já com a dissolvência feita
    momentos.append((f"clique {n}", capa + t0 + 0.6))
for _, t1 in plano.get("telas", []):  # a volta para o rosto depois de cada tela
    if t1 < plano["duracao"] - 1:
        momentos.append(("rosto", capa + t1 + 0.6))
picos = [t for (t, z), (_, z_ant) in zip(plano["zoom"][1:], plano["zoom"]) if z > 1.0 and z > z_ant]
momentos += [(f"zoom {k}", capa + t) for k, t in enumerate(picos, 1)]
momentos.append(("fim", plano["duracao"] - 0.5))
momentos.sort(key=lambda m: m[1])
HORIZONTAL = plano.get("formato") == "16:9"

fonte = ImageFont.truetype(str(FONTES / "Montserrat-Bold.ttf"), 34)
ims = []
for nome, t in momentos:
    q = trab / "conf.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(t, 0):.3f}", "-i", saida, "-frames:v", "1", str(q)], check=True)
    im = Image.open(q).convert("RGB")
    dr = ImageDraw.Draw(im, "RGBA")
    if HORIZONTAL:
        dr.line([(385, 0), (385, 1080)], fill=(0, 200, 255, 160), width=3)    # zona útil da tela
        dr.line([(1535, 0), (1535, 1080)], fill=(0, 200, 255, 160), width=3)
        dr.rectangle([10, 990, 1910, 1070], fill=(0, 0, 0, 180))
        dr.text((30, 1005), f"{nome}  {t:.2f}s", font=fonte, fill=(255, 255, 255))
        ims.append(im.resize((640, 360)))
        continue
    dr.rectangle([0, 0, 1080, 285], fill=(255, 0, 0, 40))       # fora do corte 4:5 do feed e do grid
    dr.rectangle([0, 1635, 1080, 1920], fill=(255, 0, 0, 40))
    dr.line([(0, 300), (1080, 300)], fill=(0, 200, 255, 200), width=3)    # limite de cima do título
    dr.line([(0, 1248), (1080, 1248)], fill=(0, 200, 255, 200), width=3)  # limite de baixo do título
    dr.rectangle([0, 1454, 1080, 1516], outline=(255, 255, 0, 200), width=3)  # faixa da legenda
    dr.rectangle([10, 1830, 1070, 1910], fill=(0, 0, 0, 180))
    dr.text((30, 1845), f"{nome}  {t:.2f}s", font=fonte, fill=(255, 255, 255))
    ims.append(im.resize((360, 640)))

col, (lw, lh) = (4, (650, 370)) if HORIZONTAL else (6, (370, 650))
folha = Image.new("RGB", (col * lw, ((len(ims) + col - 1) // col) * lh), (25, 25, 25))
for k, im in enumerate(ims):
    folha.paste(im, ((k % col) * lw, (k // col) * lh))
folha.save(trab / "conferencia.jpg", quality=88)

r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,width,height",
                    "-of", "compact", saida], capture_output=True, text=True).stdout
med = subprocess.run(["ffmpeg", "-hide_banner", "-i", saida, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                     capture_output=True, text=True, errors="ignore").stderr
lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", med)[-1]
pico = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", med)[-1]
print(r.strip())
print(f"volume integrado {lufs} LUFS (alvo -14), pico {pico} dBFS (limite -1,5)")
print(f"folha de conferência: {trab / 'conferencia.jpg'}")
