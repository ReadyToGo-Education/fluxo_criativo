# Editor de Reels: bruto vertical -> Reel final.
# Cortes só nas pausas longas (com dissolvência curta), zoom suave contínuo ancorado no rosto,
# legenda Montserrat em maiúscula palavra por palavra, título + pílula nos 3 primeiros segundos
# e a capa no primeiro quadro (para a miniatura do WhatsApp).
# Uso: py -3 editar_reel.py _edicao_R0XX.json [--render]
# Sem --render, só monta o plano (cortes, zoom, título, legenda) e imprime o resumo.
import json, re, subprocess, sys, unicodedata
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FERR = Path(__file__).resolve().parent
sys.path.insert(0, str(FERR))
from ambiente import FONTES, TRABALHO, ambiente, deep_filter
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
# arquivos intermediários: por padrão em %LOCALAPPDATA%/reels-editar/trabalho/{código}, preenchidos pelo preparar.py
TRAB = Path(cfg.get("trabalho") or TRABALHO / cfg["codigo"]); TRAB.mkdir(parents=True, exist_ok=True)
cfg.setdefault("audio16k", str(TRAB / "audio16k.wav"))
cfg.setdefault("palavras", str(TRAB / "palavras.json"))
# bruto, capa, saída e cartões podem vir só com o nome do arquivo: valem a partir da pasta do Reel (onde fica o JSON)
PASTA = Path(sys.argv[1]).resolve().parent
na_pasta = lambda c: str(c if Path(c).is_absolute() else PASTA / c)
for k in ("bruto", "capa", "saida"):
    cfg[k] = na_pasta(cfg[k])
for c in cfg.get("cartoes", []):
    c["arquivo"] = na_pasta(c["arquivo"])

D = 0.12            # duração da dissolvência em cada corte
PAUSA_MIN = cfg.get("pausa_min", 1.0)    # só corta pausa maior que isso (padrão dos Reels publicados: pausa típica 0,7 a 0,8 s)
PAUSA_FICA = cfg.get("pausa_fica", 0.8)  # quanto da pausa cortada permanece
FPS = 30
INICIO, FIM = cfg["inicio"], cfg["fim"]
FX, FY = cfg["rosto"]

# takes descartados (erros e regravações aprovados pelo Rodrigo): [início, fim] no tempo do bruto
TAKES_FORA = sorted(tuple(x) for x in cfg.get("remover", []))
fora_do_take = lambda w: any(a - 0.05 <= w["s"] and w["e"] <= b + 0.05 for a, b in TAKES_FORA)
palavras = [w for w in json.load(open(cfg["palavras"], encoding="utf-8"))
            if INICIO - 0.6 <= w["s"] < FIM and not fora_do_take(w)]

# ---------- pausas reais do áudio ----------
txt = subprocess.run(["ffmpeg", "-hide_banner", "-i", cfg["audio16k"], "-af",
                      "silencedetect=noise=-32dB:d=0.15", "-f", "null", "-"], capture_output=True, text=True).stderr
silencios = [(float(a), float(a) + float(d)) for a, d in
             zip(re.findall(r"silence_start: ([\d.]+)", txt), re.findall(r"silence_duration: ([\d.]+)", txt))]
silencios = [(a, b) for a, b in silencios if a > INICIO and b < FIM]

manter = cfg.get("pausas_manter", [])        # pausas dramáticas que não são cortadas
especiais = cfg.get("pausas_especiais", {})  # pausa -> quanto fica
remover = []
for a, b in silencios:
    if any(abs(a - m) < 0.15 for m in manter):
        continue
    fica = next((v for k, v in especiais.items() if abs(a - float(k)) < 0.15), PAUSA_FICA)
    if b - a >= PAUSA_MIN and (b - a) - fica >= cfg.get("corte_minimo", 0.4):
        remover.append((a + fica / 2, b - fica / 2))

# junta os cortes de pausa com os takes descartados (sem sobreposição)
juntos = []
for a, b in sorted(remover + list(TAKES_FORA)):
    if juntos and a <= juntos[-1][1] + 0.05: juntos[-1][1] = max(juntos[-1][1], b)
    else: juntos.append([a, b])
remover = [tuple(x) for x in juntos]
trechos, cur = [], INICIO
for a, b in remover:
    trechos.append((cur, a)); cur = b
trechos.append((cur, FIM))
offs, acc = [], 0.0
for i, (a, b) in enumerate(trechos):
    offs.append(acc); acc += (b - a) - D
DUR = acc + D

def mapa(t):
    for (a, b), o in zip(trechos, offs):
        if t < a: return o
        if t <= b: return o + (t - a)
    return DUR

def ajusta(w):
    s, e = w["s"], w["e"]
    for a, b in silencios:
        if a <= s < b: s = b
        if a < e <= b: e = a
        if s < a and e > b and a - s < 0.2: s = b
    s = max(s, INICIO)
    return s, max(e, s + 0.08)

itens = []
for w in palavras:
    s, e = ajusta(w)
    itens.append({"t": w["w"], "s": mapa(s), "e": mapa(e)})
juntados = []
for it in itens:
    t = it["t"]
    if juntados and (t in ("$", "%", "%,", "%.") or re.match(r"^[.,]\d", t) or t.startswith("-")):
        juntados[-1]["t"] += t; juntados[-1]["e"] = it["e"]; continue
    juntados.append(it)
itens = juntados
for troca in cfg.get("trocas", []):
    for it in itens:
        if it["t"].lower().strip(".,?!") == troca[0]:
            it["t"] = re.sub(re.escape(troca[0]), troca[1], it["t"], flags=re.I)

def com_separador(t):
    m = re.match(r"^(R\$)?(\d{4,})([.,%?!]*)$", t)
    if not m: return t
    n = f"{int(m.group(2)):,}".replace(",", ".")
    return (m.group(1) or "") + n + m.group(3)
for it in itens:
    it["t"] = com_separador(it["t"])

# número por extenso e em algarismo casam igual ("quatro bilhões" no JSON acha "4 bilhões" na fala, e vice-versa)
NUMEROS = {w: str(k) for k, ws in enumerate(["zero", "um uma", "dois duas", "tres", "quatro", "cinco", "seis", "sete",
           "oito", "nove", "dez", "onze", "doze", "treze", "quatorze catorze", "quinze", "dezesseis", "dezessete",
           "dezoito", "dezenove", "vinte"]) for w in ws.split()}
NUMEROS.update({"trinta": "30", "quarenta": "40", "cinquenta": "50", "cem": "100"})

def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = re.sub(r"[^a-z0-9 ]", "", "".join(c for c in t if unicodedata.category(c) != "Mn"))
    return " ".join(NUMEROS.get(w, w) for w in t.split())

def acha(frase, depois=0.0):
    alvo = norm(frase).split()
    ws = [norm(i["t"]) for i in itens]
    for k in range(len(ws) - len(alvo) + 1):
        if ws[k:k + len(alvo)] == alvo and itens[k]["s"] >= depois:
            return itens[k]["s"], itens[k + len(alvo) - 1]["e"]
    raise SystemExit(f"Frase não encontrada na fala: {frase}")

# frases corrigidas pelo sentido: [como saiu na fala, como deve ficar na legenda], palavra por palavra
for errado, certo in cfg.get("trocas_frase", []):
    s0, _ = acha(errado)
    k0 = next(k for k, it in enumerate(itens) if abs(it["s"] - s0) < 1e-6)
    for k, palavra in enumerate(certo.split()):
        itens[k0 + k]["t"] = palavra

# ---------- cenas do OBS ----------
# Aulas gravadas no OBS alternam só rosto e tela dividida (a aula em cima, creme). Na tela dividida
# não tem zoom (cortaria a aula) e a legenda sobe para entre a tela e a cabeça.
CENAS_DIV = []  # janelas de tela dividida no tempo do bruto
if cfg.get("cenas_obs"):
    cache = TRAB / "cenas_divididas.json"
    if not cache.exists():
        import numpy as np
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", cfg["bruto"], "-vf", "fps=2,crop=1080:900:0:30,scale=108:90",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.uint8).reshape(-1, 90, 108, 3).astype(float)
        fracao = (np.abs(x - cfg.get("cor_tela", [247, 242, 232])).sum(3) < 40).reshape(len(x), -1).mean(1)
        creme = fracao > 0.30
        idx = np.where(creme)[0]
        for a, b in zip(idx[:-1], idx[1:]):
            if 1 < b - a <= 8: creme[a:b] = True  # buraco de até 4 s no meio da tela dividida
        jan, ini = [], None
        for i in range(len(creme) + 1):
            v = creme[i] if i < len(creme) else False
            if v and ini is None: ini = i
            if not v and ini is not None:
                if (i - ini) / 2 >= 1.5: jan.append([ini / 2, i / 2])
                ini = None
        json.dump(jan, open(cache, "w"))
    CENAS_DIV = json.load(open(cache))
    print("tela dividida (bruto):", ", ".join(f"{a:.0f}-{b:.0f}s" for a, b in CENAS_DIV))
def div_out():
    return [(mapa(a), mapa(b)) for a, b in CENAS_DIV if mapa(b) - mapa(a) > 0.2]
def na_cena_div(t):
    return any(a - 0.01 <= t < b for a, b in div_out())

# ---------- zoom suave (pontos-chave com transição em curva S) ----------
chaves = [(0.0, 1.0), (cfg.get("titulo_ate", 3.0), 1.0)]
base = cfg.get("zoom_base", [1.06, 1.0])
for k, z in enumerate(cfg["zoom"]):
    s, _ = acha(z["de"], chaves[-1][0] - 1)
    _, e = acha(z["ate"], s)
    volta = base[k % 2]
    if z.get("empurra"):  # aproximação lenta ao longo da frase inteira
        chaves += [(max(s - 0.1, chaves[-1][0] + 0.2), chaves[-1][1]), (e, z["zoom"]), (e + 1.0, volta)]
    else:
        chaves += [(max(s - 0.45, chaves[-1][0] + 0.2), chaves[-1][1]), (s + 0.05, z["zoom"]),
                   (e + 0.1, z["zoom"]), (e + 1.1, volta)]
chaves.append((DUR + 1, chaves[-1][1]))

def expr_zoom(desloc):
    t = f"(it+{desloc:.3f})"
    partes = [f"{chaves[0][1]:.3f}"]
    for (t0, z0), (t1, z1) in zip(chaves, chaves[1:]):
        if abs(z1 - z0) < 1e-6: continue
        c = f"clip(({t}-{t0:.3f})/{t1 - t0:.3f},0,1)"
        partes.append(f"{z1 - z0:+.3f}*{c}*{c}*(3-2*{c})")
    z = "".join(partes)
    if CENAS_DIV:  # na tela dividida do OBS o zoom fica em 1
        fora = "+".join(f"between({t},{a:.3f},{b:.3f})" for a, b in div_out())
        z = f"1+(({z})-1)*(1-min(1,{fora}))"
    return z

# ---------- título dos 3 primeiros segundos, no padrão da capa (PNG transparente) ----------
# Cartão menta com o selo verde espaçado e as linhas em preto (Inter 900), e a última linha
# em branco na tarja vermelha inclinada -2°, como nas capas da Linha Editorial.
def inter(peso, tam):
    f = ImageFont.truetype(str(FONTES / "Inter-Variable.ttf"), tam); f.set_variation_by_axes([peso, 0]); return f

def largura(dr, txt, f, esp):
    return sum(dr.textlength(c, font=f) for c in txt) + esp * (len(txt) - 1)

def escreve(dr, x, y, txt, f, esp, cor):
    for c in txt:
        dr.text((x, y), c, font=f, fill=cor); x += dr.textlength(c, font=f) + esp

VERDE, MENTA, TINTA = (15, 92, 46, 255), (213, 236, 221, 248), (10, 23, 18, 255)
ALERTA, PAPEL = (179, 38, 26, 255), (255, 253, 246, 255)
def hexa(h, a=255): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)
FUNDO = hexa(cfg["titulo_fundo"], 248) if "titulo_fundo" in cfg else MENTA  # cor de fundo da capa do Reel
COR_SELO = hexa(cfg["titulo_selo"]) if "titulo_selo" in cfg else VERDE
TT = cfg.get("titulo_tamanho", 78)
f_tag, f_tit = inter(800, round(TT * 0.40)), inter(900, TT)
esp_tag, esp_tit = TT * 0.40 * 0.22, -TT * 0.03
linhas = [l.upper() for l in cfg["titulo"]]
pretas, vermelha = linhas[:-1], linhas[-1]
med = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
larg_cartao = max([largura(med, cfg["pilula"].upper(), f_tag, esp_tag)] +
                  [largura(med, l, f_tit, esp_tit) for l in pretas]) + 2 * round(TT * 0.6)
pad, passo = round(TT * 0.36), round(TT * 1.04)
alt_tag = round(TT * 0.40) + round(TT * 0.3)
alt_cartao = pad + alt_tag + passo * len(pretas) + round(TT * 0.95)

# tarja vermelha desenhada à parte e girada
lv = largura(med, vermelha, f_tit, esp_tit)
bx, bt, bb = round(TT * 0.38), round(TT * 0.18), round(TT * 0.22)
tarja = Image.new("RGBA", (round(lv + 2 * bx + 20), round(TT * 1.0 + bt + bb + 20)), (0, 0, 0, 0))
dt = ImageDraw.Draw(tarja)
dt.rounded_rectangle([10, 10, 10 + lv + 2 * bx, 10 + TT * 1.0 + bt + bb], radius=round(TT * 0.18), fill=ALERTA)
escreve(dt, 10 + bx, 10 + bt - round(TT * 0.06), vermelha, f_tit, esp_tit, PAPEL)
tarja = tarja.rotate(2, resample=Image.BICUBIC, expand=True)

alt_total = alt_cartao + tarja.height // 2
y0 = max(300, min(cfg.get("titulo_y", 900), 1240 - alt_total))  # entre y 300 (grid 4:5 e cabeçalho) e 1248 (zona segura do Reels)
ov = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
x0 = (1080 - larg_cartao) / 2
dr.rounded_rectangle([x0, y0, x0 + larg_cartao, y0 + alt_cartao], radius=round(TT * 0.3), fill=FUNDO)
y = y0 + pad
lt = largura(dr, cfg["pilula"].upper(), f_tag, esp_tag)
escreve(dr, (1080 - lt) / 2, y, cfg["pilula"].upper(), f_tag, esp_tag, COR_SELO)
y += alt_tag
for l in pretas:
    w = largura(dr, l, f_tit, esp_tit)
    escreve(dr, (1080 - w) / 2, y - round(TT * 0.1), l, f_tit, esp_tit, TINTA); y += passo
ov.alpha_composite(tarja, (round((1080 - tarja.width) / 2), round(y0 + alt_cartao - tarja.height / 2)))
ov.save(TRAB / "titulo.png")
print(f"título: y {y0} a {y0 + alt_total}")

# ---------- legenda ASS ----------
def ts(t):
    t = max(t, 0); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
blocos, atual = [], []
for it in itens:
    atual.append(it)
    if re.search(r"[.,?!]$", it["t"]) or len(atual) >= 3 or sum(len(x["t"]) for x in atual) >= 15:
        blocos.append(atual); atual = []
if atual: blocos.append(atual)
limpa = lambda t: re.sub(r"(?<!\d)[.,]|[.,](?!\d)|[!?]", "", t).upper()  # tira pontuação, mas mantém 1.500 e 2,5

# janelas dos cartões de prova (calculadas antes, porque a legenda muda de lugar na tela dividida)
cartoes = cfg.get("cartoes", [])
tempos = []
for c in cartoes:
    s0, _ = acha(c["palavra"], tempos[-1][0] if tempos else 0)
    tempos.append([s0, s0 + c.get("dura", 3.0)])
for k in range(len(tempos) - 1):
    tempos[k][1] = min(tempos[k][1], tempos[k + 1][0])
DIVIDIDA = cfg.get("tela_dividida", True)
janelas = []  # cartões colados viram uma janela só de tela dividida
for t0, t1 in tempos:
    if janelas and t0 - janelas[-1][1] < 0.05: janelas[-1][1] = t1
    else: janelas.append([t0, t1])
na_divisao = lambda t: DIVIDIDA and any(j0 - 0.01 <= t < j1 for j0, j1 in janelas)

# cores da legenda: cada vídeo tem a sua cor de destaque; palavras-chave ficam coloridas o tempo todo
CORES = {"amarelo": "&H0000E6FF&", "verde": "&H0084DC3D&", "vermelho": "&H005A5AFF&", "laranja": "&H00248CFF&"}
mudancas = sorted((acha(m["de"])[0], CORES[m["cor"]]) for m in cfg.get("cores_legenda", []))
COR_VIDEO = CORES[cfg.get("cor_legenda", "amarelo")]  # uma cor de destaque por vídeo, fixa do começo ao fim
def cor_em(t):
    cor = COR_VIDEO
    for t0, c in mudancas:
        if t >= t0 - 0.01: cor = c
    return cor
chave = set()
for frase in cfg.get("palavras_chave", []):
    s0, e0 = acha(frase)
    chave |= {id(it) for it in itens if s0 - 0.01 <= it["s"] <= e0}

ev = []
for bi, bl in enumerate(blocos):
    prox = blocos[bi + 1][0]["s"] if bi + 1 < len(blocos) else bl[-1]["e"] + 0.4
    cor = cor_em(bl[0]["s"])
    for wi, w in enumerate(bl):
        ini = w["s"] if wi else bl[0]["s"]
        fim = bl[wi + 1]["s"] if wi + 1 < len(bl) else (prox if prox - bl[-1]["e"] < 0.35 else bl[-1]["e"] + 0.15)
        partes_l = []
        for k, x in enumerate(bl):
            if k == wi:
                partes_l.append(r"{\c" + cor + r"\fscx108\fscy108}" + limpa(x["t"]) + r"{\c&HFFFFFF&\fscx100\fscy100}")
            elif id(x) in chave:
                partes_l.append(r"{\c" + cor + "}" + limpa(x["t"]) + r"{\c&HFFFFFF&}")
            else:
                partes_l.append(limpa(x["t"]))
        if na_divisao(ini): pos = r"{\an5\pos(540,962)}"  # tela dividida com cartão: legenda na linha da divisão
        elif na_cena_div(ini): pos = r"{\an2\pos(540,%d)}" % cfg.get("legenda_div_y", 1130)  # tela dividida do OBS
        else: pos = ""  # na tela dividida, a legenda fica na linha da divisão
        ev.append(f"Dialogue: 0,{ts(ini)},{ts(fim)},Leg,,0,0,0,,{pos}" + " ".join(partes_l))
leg_y = cfg.get("legenda_base_y", 1516)
(TRAB / "legenda.ass").write_text(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Leg,Montserrat ExtraBold,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,4,3,2,60,60,{1920 - leg_y},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n", encoding="utf-8")

def ts_srt(t):
    ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
(TRAB / "legenda.srt").write_text("\n".join(
    f"{k}\n{ts_srt(bl[0]['s'] + 1 / FPS)} --> {ts_srt(bl[-1]['e'] + 1 / FPS)}\n{' '.join(limpa(x['t']) for x in bl)}\n"
    for k, bl in enumerate(blocos, 1)), encoding="utf-8")

# ---------- redução de respiração ----------
# Nos intervalos entre palavras o volume desce (padrão -12 dB) com rampas de 50 ms, sem encostar nas palavras.
# Em sala silenciosa nada cobre a respiração, e o compressor a traz para a frente (R024).
RESP_DB = cfg.get("respiracao_db", 0)  # o áudio D (IA) já abaixa a respiração; use -12 só se ainda aparecer
janelas_resp = []
if RESP_DB < 0:
    import wave
    import numpy as np
    wf = wave.open(cfg["audio16k"])
    amostras = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(float) / 32768
    def nivel(t):  # dB de um trecho de 10 ms
        q = amostras[int(t * 16000):int(t * 16000) + 160]
        return 20 * np.log10(np.sqrt((q ** 2).mean()) + 1e-9) if len(q) else -99
    FALA_DB = -24  # acima disso é fala, nunca abaixa
    tempos_pal = [ajusta(w) for w in palavras]
    for (s1, e1), (s2, e2) in zip(tempos_pal, tempos_pal[1:]):
        a0, b0 = e1 + 0.08, s2 - 0.06
        while a0 < b0 and nivel(a0 - 0.03) > FALA_DB: a0 += 0.01  # o Whisper às vezes encurta a palavra
        while b0 > a0 and nivel(b0 + 0.02) > FALA_DB: b0 -= 0.01
        if b0 - a0 >= 0.12 and max(nivel(t) for t in np.arange(a0, b0, 0.01)) <= FALA_DB:
            janelas_resp.append((a0, b0))
def expr_resp():
    g = 10 ** (RESP_DB / 20)
    termos = "+".join(f"clip((t-{a0:.3f})/0.05,0,1)*clip(({b0:.3f}-t)/0.05,0,1)" for a0, b0 in janelas_resp)
    return f"1-{1 - g:.4f}*({termos})" if termos else "1"
print(f"respiração: {len(janelas_resp)} intervalos abaixados em {RESP_DB} dB")

# ---------- cor (padrão C: balanço de branco e exposição pelo rosto + acabamento Instagram) ----------
FILTRO_COR = ""
if cfg.get("cor", "C") != "nenhuma":
    sys.path.insert(0, str(FERR))
    from cor import filtro_cor
    quadros = []
    rosto_jan, cur_r = [], INICIO  # trechos só de rosto (a tela creme da aula não pode virar referência de branco)
    for a, b in sorted(CENAS_DIV):
        if a > cur_r: rosto_jan.append((cur_r, min(a, FIM)))
        cur_r = max(cur_r, b)
    if cur_r < FIM: rosto_jan.append((cur_r, FIM))
    tot = sum(b - a for a, b in rosto_jan)
    def tempo_rosto(frac):
        alvo = frac * tot
        for a, b in rosto_jan:
            if alvo <= b - a: return a + alvo
            alvo -= b - a
        return rosto_jan[-1][1] - 1
    for k, frac in enumerate((0.2, 0.4, 0.6, 0.8)):
        q = TRAB / f"cor_{k}.png"
        t = tempo_rosto(frac)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", cfg["bruto"], "-frames:v", "1",
                        "-vf", "scale=1080:1920", str(q)], check=True)
        quadros.append(str(q))
    cx, cy = FX * 1080, FY * 1920
    rosto_caixa = tuple(int(v) for v in cfg.get("rosto_caixa", (cx - 70, cy - 200, cx + 70, cy - 20)))
    FILTRO_COR, info_cor = filtro_cor(quadros, rosto_caixa, acabamento=cfg.get("cor", "C") == "C",
                                      exposicao=cfg.get("cor_exposicao", not cfg.get("cenas_obs")))
    FILTRO_COR = "," + FILTRO_COR
    print("cor:", {k: (float(v) if not isinstance(v, list) else v) for k, v in info_cor.items()})

# ---------- filtro ----------
p = []
for i, ((a, b), o) in enumerate(zip(trechos, offs)):
    p.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps={FPS},"
             f"zoompan=z='{expr_zoom(o)}':x='{FX}*(iw-iw/zoom)':y='{FY}*(ih-ih/zoom)':d=1:s=1080x1920:fps={FPS}{FILTRO_COR},"
             f"setsar=1,format=yuv420p[v{i}]")
    p.append(f"[1:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{i}]")
uv, ua = "[v0]", "[a0]"
for i in range(1, len(trechos)):
    p.append(f"{uv}[v{i}]xfade=transition=fade:duration={D}:offset={offs[i]:.3f}[xv{i}]")
    p.append(f"{ua}[a{i}]acrossfade=d={D}:c1=tri:c2=tri[xa{i}]")
    uv, ua = f"[xv{i}]", f"[xa{i}]"
ta = cfg.get("titulo_ate", 3.0)
p.append(f"[2:v]format=rgba,fade=t=in:st=0:d=0.2:alpha=1,fade=t=out:st={ta - 0.3}:d=0.3:alpha=1[tit]")
ult = "[vt]"
p.append(f"{uv}[tit]overlay=0:0:eof_action=pass[vt]")
FUNDO_DIV = cfg.get("fundo_divisao", "0x0A1712")
if DIVIDIDA and cartoes:
    # tela dividida: notícia na metade de cima, vídeo deslocado para baixo com o rosto inteiro
    corte_y = int(min(max(FY * 1920 - 0.3 * 960, 0), 960))
    p.append(f"[vt]split[vfull][vdiv]")
    p.append(f"[vdiv]crop=1080:960:0:{corte_y},pad=1080:1920:0:960:color={FUNDO_DIV}[vbase]")
    ult = "[vbase]"
    for k, (c, (t0, t1)) in enumerate(zip(cartoes, tempos)):
        larg = c.get("largura", 1000)
        p.append(f"[{4 + k}:v]format=rgba,scale={larg}:-1[c{k}]")
        p.append(f"{ult}[c{k}]overlay=x={(1080 - larg) // 2}:y='300+(640-h)/2':shortest=1:enable='between(t,{t0:.3f},{t1:.3f})'[vc{k}]")
        ult = f"[vc{k}]"
        print(f"cartão {k + 1}: {t0:.2f}s a {t1:.2f}s  ({Path(c['arquivo']).name})")
    cond = "+".join(f"between(t,{j0:.3f},{j1:.3f})" for j0, j1 in janelas)
    p.append(f"[vfull]{ult}overlay=0:0:shortest=1:enable='{cond}'[vsplit]")
    ult = "[vsplit]"
else:
    for k, (c, (t0, t1)) in enumerate(zip(cartoes, tempos)):
        seco_antes = k > 0 and abs(tempos[k - 1][1] - t0) < 0.05
        seco_depois = k + 1 < len(tempos) and abs(tempos[k + 1][0] - t1) < 0.05
        fades = ("" if seco_antes else f",fade=t=in:st={t0:.3f}:d=0.2:alpha=1") + \
                ("" if seco_depois else f",fade=t=out:st={t1 - 0.2:.3f}:d=0.2:alpha=1")
        larg = c.get("largura", 1000)
        p.append(f"[{4 + k}:v]format=rgba,scale={larg}:-1{fades}[c{k}]")
        p.append(f"{ult}[c{k}]overlay=x={(1080 - larg) // 2}:y={c.get('y', 500)}:shortest=1:enable='between(t,{t0:.3f},{t1:.3f})'[vc{k}]")
        ult = f"[vc{k}]"
        print(f"cartão {k + 1}: {t0:.2f}s a {t1:.2f}s  ({Path(c['arquivo']).name})")
p.append(f"{ult}subtitles=legenda.ass:fontsdir='{FONTES.as_posix().replace(':', '\\:')}'[vm]")
p.append(f"[3:v]scale=1080:1920,setsar=1,fps={FPS},format=yuv420p,trim=end_frame=1,setpts=PTS-STARTPTS[cv]")
p.append(f"anullsrc=r=48000:cl=mono,atrim=end={1 / FPS:.4f}[sil]")
p.append(f"{ua}afade=t=out:st={DUR - 0.6:.3f}:d=0.6[afim]")
p.append(f"[cv][sil][vm][afim]concat=n=2:v=1:a=1[vout][aout]")
(TRAB / "filtro.txt").write_text(";\n".join(p), encoding="utf-8")

print(f"{len(trechos)} trechos ({len(trechos) - 1} cortes), duração {DUR + 1 / FPS:.2f}s")
for (a, b), o in zip(trechos, offs):
    print(f"  {a:6.2f}-{b:6.2f} -> {o:6.2f}  " + " ".join(w["w"] for w in palavras if a - 0.05 <= ajusta(w)[0] < b)[:70])
print("zoom:", ", ".join(f"{t:.2f}={z:.2f}" for t, z in chaves))
# plano salvo para o conferir.py escolher os quadros de conferência (tempos já no vídeo final, sem o quadro da capa)
json.dump({"duracao": DUR + 1 / FPS, "fps": FPS, "titulo_ate": cfg.get("titulo_ate", 3.0), "zoom": chaves[:-1],
           "cartoes": tempos, "cortes": offs[1:], "saida": cfg["saida"]},
          open(TRAB / "plano.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- render ----------
if "--render" in sys.argv:
    import time
    t_ini = time.time()
    if cfg.get("audio_limpo"):
        audio_base = cfg["audio_limpo"]
    else:  # padrão D, igual ao CapCut: reduzir ruído + aprimorar voz (75%); a normalização a -14 LUFS vem no fim
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", cfg["bruto"], "-vn", "-ac", "1", "-ar", "48000",
                        "-c:a", "pcm_s16le", "audio_bruto.wav"], cwd=TRAB, check=True)
        (TRAB / "df").mkdir(exist_ok=True)
        subprocess.run([deep_filter(), "-D", "-o", "df", "audio_bruto.wav"], cwd=TRAB, check=True,
                       capture_output=True)
        subprocess.run(ambiente()["voz"] + [str(FERR / "aprimorar_voz.py"), "df/audio_bruto.wav", "audio_ia.wav",
                        str(cfg.get("aprimorar_voz", 75))], cwd=TRAB, check=True, capture_output=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "audio_ia.wav", "-af", "highpass=f=70",
                        "-c:a", "pcm_s24le", "audio_d.wav"], cwd=TRAB, check=True)
        audio_base = str(TRAB / "audio_d.wav")
        print("áudio D pronto (reduzir ruído + aprimorar voz)")
    audio_in = audio_base
    if janelas_resp:
        (TRAB / "respiracao.txt").write_text(f"asetnsamples=n=240:p=0,volume='{expr_resp()}':eval=frame", encoding="utf-8")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", audio_base, "-filter_script:a", "respiracao.txt",
                        "-c:a", "pcm_s24le", "audio_resp.wav"], cwd=TRAB, check=True)
        audio_in = str(TRAB / "audio_resp.wav")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", cfg["bruto"], "-i", audio_in,
           "-loop", "1", "-t", str(ta), "-framerate", str(FPS), "-i", "titulo.png",
           "-loop", "1", "-t", "0.1", "-framerate", str(FPS), "-i", cfg["capa"]]
    for c in cartoes:
        cmd += ["-loop", "1", "-t", f"{DUR + 1:.2f}", "-framerate", str(FPS), "-i", c["arquivo"]]
    cmd += ["-filter_complex_script", "filtro.txt", "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264",
            "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "pcm_s24le", "montado.mkv"]
    subprocess.run(cmd, cwd=TRAB, check=True)
    # volume final linear: ganho fixo até -14 LUFS e limitador de pico em -1,5 dB.
    # (o loudnorm cai no modo dinâmico quando falta folga de pico e levanta pausas e respiração)
    med = subprocess.run(["ffmpeg", "-hide_banner", "-i", "montado.mkv", "-vn", "-af", "ebur128", "-f", "null", "-"],
                         cwd=TRAB, capture_output=True, text=True, errors="ignore").stderr
    integrado = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", med)[-1])
    ganho = -14.0 - integrado
    # o limitador segura parte do ganho (mais em vídeo longo): mede o resultado e corrige até 2 vezes
    for _ in range(3):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "montado.mkv", "-c:v", "copy", "-af",
                        f"volume={ganho:.2f}dB,alimiter=limit=0.841:attack=2:release=60:level=false,aresample=48000",
                        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", cfg["saida"]], cwd=TRAB, check=True)
        med = subprocess.run(["ffmpeg", "-hide_banner", "-i", cfg["saida"], "-vn", "-af", "ebur128", "-f", "null", "-"],
                             capture_output=True, text=True, errors="ignore").stderr
        final = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", med)[-1])
        if abs(final + 14.0) <= 0.3: break
        ganho += -14.0 - final
    print(f"volume final {final:.1f} LUFS")
    print(f"render pronto em {time.time() - t_ini:.0f}s: {cfg['saida']}")
