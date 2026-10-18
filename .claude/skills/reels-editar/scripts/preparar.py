# Prepara um Reel para edição: acha os arquivos da pasta, transcreve a fala e tira os quadros do rosto.
# Uso: py -3 preparar.py "caminho/da/pasta/R0XX - Nome" [--horizontal] [--sem-transcrever]
# Aula gravada no OBS nas duas saídas ("... - Bruta - Vertical.mp4" e "... - Horizontal.mp4"): sem --horizontal
# prepara o vertical (trabalho em R0XXV); com --horizontal, o horizontal (R0XXH).
# Grava em %LOCALAPPDATA%/reels-editar/trabalho/R0XX/:
#   audio16k.wav, palavras.json (cada palavra com início, fim e confiança),
#   rosto_grade.jpg (3 quadros da bruta com grade de 10% e as zonas seguras), preparo.json (resumo).
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente import FONTES, SCRIPTS, TRABALHO, ambiente

pasta = Path(sys.argv[1]).resolve()
m = re.match(r"(R\d{3})", pasta.name)
if not m:
    raise SystemExit(f"A pasta precisa começar pelo código do Reel (ex.: R028 - Nome): {pasta.name}")
codigo = m.group(1)

# ---------- arquivos da pasta ----------
videos = [v for v in pasta.glob("*.mp4") if not v.name.startswith("_") and "editado" not in v.name.lower()]
videos += [v for v in pasta.glob("*.mov") if not v.name.startswith("_")]
if not videos:
    raise SystemExit("SEM_BRUTO: nenhum vídeo bruto na pasta (o .mp4 gravado, sem _ no começo e sem 'editado' no nome).")
orientados = {o: [v for v in videos if o in v.name.lower()] for o in ("vertical", "horizontal")}
if orientados["vertical"] or orientados["horizontal"]:  # aula com as duas saídas do OBS
    lado = "horizontal" if "--horizontal" in sys.argv else "vertical"
    if not orientados[lado]:
        raise SystemExit(f"SEM_BRUTO: não achei o bruto {lado} na pasta.")
    bruto = max(orientados[lado], key=lambda v: v.stat().st_size)
    codigo += "H" if lado == "horizontal" else "V"
else:
    bruto = max(videos, key=lambda v: v.stat().st_size)
trab = TRABALHO / codigo
trab.mkdir(parents=True, exist_ok=True)
capas = sorted(pasta.glob("CAPA_*.png"))
roteiros = sorted(pasta.glob("Reels_*.html"))
cartoes = sorted(pasta.glob("TELA_*.png"))
telas_html = sorted(pasta.glob("_TELA_*.html"))  # aula gravada só com a câmera: as telas saem daqui

def sonda(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:stream_side_data=rotation:format=duration", "-of", "json", str(arq)],
                       capture_output=True, text=True)
    return json.loads(r.stdout)

info = sonda(bruto)
duracao = float(info["format"]["duration"])

# ---------- áudio e transcrição ----------
audio16k = trab / "audio16k.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bruto), "-vn", "-ac", "1", "-ar", "16000",
                "-c:a", "pcm_s16le", str(audio16k)], check=True)
palavras_arq = trab / "palavras.json"
if "--sem-transcrever" not in sys.argv or not palavras_arq.exists():
    subprocess.run(ambiente()["whisper"] + [str(SCRIPTS / "transcrever.py"), str(audio16k), str(palavras_arq)], check=True)
palavras = json.load(open(palavras_arq, encoding="utf-8"))
# segunda transcrição, fala por fala: separa duas tentativas da mesma frase que a transcrição inteira funde
# (R026). Serve para ACHAR erros e regravações; a legenda continua saindo da transcrição inteira.
por_fala_arq = trab / "palavras_por_fala.json"
if "--sem-transcrever" not in sys.argv or not por_fala_arq.exists():
    subprocess.run(ambiente()["whisper"] + [str(SCRIPTS / "transcrever_por_fala.py"), str(audio16k), str(por_fala_arq)],
                   check=True)
por_fala = json.load(open(por_fala_arq, encoding="utf-8"))
blocos, cur = [], []
for w in por_fala:
    if cur and w["s"] - cur[-1]["e"] > 0.6:
        blocos.append(cur); cur = []
    cur.append(w)
if cur: blocos.append(cur)
(trab / "fala_por_fala.txt").write_text("\n".join(f"[{b[0]['s']:6.2f}-{b[-1]['e']:6.2f}] " + " ".join(x["w"] for x in b)
                                                   for b in blocos) + "\n", encoding="utf-8")

# fala em texto corrido, com o tempo no começo de cada linha (para casar com o roteiro)
linhas, atual = [], []
for w in palavras:
    atual.append(w)
    if len(atual) >= 10 or re.search(r"[.?!]$", w["w"]):
        linhas.append(f"[{atual[0]['s']:6.2f}] " + " ".join(x["w"] for x in atual)); atual = []
if atual:
    linhas.append(f"[{atual[0]['s']:6.2f}] " + " ".join(x["w"] for x in atual))
(trab / "fala.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")

# pausas acima de 1 s (as únicas que o editor corta)
txt = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(audio16k), "-af", "silencedetect=noise=-32dB:d=1.0",
                      "-f", "null", "-"], capture_output=True, text=True).stderr
pausas = [(round(float(a), 2), round(float(d), 2)) for a, d in
          zip(re.findall(r"silence_start: ([\d.]+)", txt), re.findall(r"silence_duration: ([\d.]+)", txt))]

# ---------- quadros do rosto com grade ----------
quadros = []
for k, frac in enumerate((0.25, 0.5, 0.75)):
    q = trab / f"rosto_{k}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{duracao * frac:.2f}", "-i", str(bruto), "-frames:v", "1",
                    "-vf", "scale=1080:1920", str(q)], check=True)
    quadros.append(q)
fonte = ImageFont.truetype(str(FONTES / "Montserrat-Bold.ttf"), 30)
folha = Image.new("RGB", (3 * 1080 + 40, 1920), (20, 20, 20))
for k, q in enumerate(quadros):
    im = Image.open(q).convert("RGB")
    dr = ImageDraw.Draw(im, "RGBA")
    for i in range(1, 10):  # grade de 10% (x e y em fração, como o campo "rosto" do JSON)
        dr.line([(i * 108, 0), (i * 108, 1920)], fill=(255, 255, 255, 90), width=2)
        dr.line([(0, i * 192), (1080, i * 192)], fill=(255, 255, 255, 90), width=2)
        dr.text((i * 108 + 4, 4), f"{i / 10:.1f}", font=fonte, fill=(255, 255, 0, 255))
        dr.text((4, i * 192 + 4), f"{i / 10:.1f}", font=fonte, fill=(255, 255, 0, 255))
    for y, cor, nome in ((285, (255, 60, 60, 220), "4:5 / 285"), (300, (60, 200, 255, 220), "título mín 300"),
                         (1248, (60, 200, 255, 220), "título máx 1248"), (1635, (255, 60, 60, 220), "4:5 / 1635")):
        dr.line([(0, y), (1080, y)], fill=cor, width=4)
        dr.text((700 if y in (300, 1248) else 380, y + 6), nome, font=fonte, fill=cor)
    folha.paste(im, (k * 1100, 0))
folha.resize((folha.width // 2, folha.height // 2)).save(trab / "rosto_grade.jpg", quality=88)

# ---------- resumo ----------
primeira = palavras[0] if palavras else None
resumo = {
    "codigo": codigo, "pasta": str(pasta), "trabalho": str(trab),
    "bruto": bruto.name, "duracao_bruto": round(duracao, 2),
    "capa": [c.name for c in capas], "roteiro": [r.name for r in roteiros], "cartoes": [c.name for c in cartoes], "tela_html": [t.name for t in telas_html],
    "palavras": len(palavras),
    "primeira_palavra": primeira and f"{primeira['s']:.2f} {primeira['w']}",
    # o fim do vídeo é o fim da última palavra real + 1 s de respiro; palavra de baixa confiança no fim
    # costuma ser conversa depois da gravação (ex.: "There we go" do R027) e fica de fora
    "ultimas_palavras": [f"{w['s']:.2f}-{w['e']:.2f} {w['w']} ({w['p']:.2f})" for w in palavras[-10:]],
    "inicio_sugerido": round(max(primeira["s"] - 0.1, 0), 2) if primeira else 0,
    "pausas_acima_de_1s": [f"{a:.2f} ({d:.2f} s)" for a, d in pausas],
    "rosto_grade": str(trab / "rosto_grade.jpg"),
    "fala": str(trab / "fala.txt"),
    "fala_por_fala": str(trab / "fala_por_fala.txt"),
}
json.dump(resumo, open(trab / "preparo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(resumo, ensure_ascii=False, indent=1))
