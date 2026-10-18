# Correção de cor automática por vídeo, medida no rosto e no quadro inteiro.
# 1) Balanço de branco: puxa a pele para a referência (R/G 1,28 e B/G 0,80), sem ir até o fim (70%).
#    Se o quadro tem área branca (camisa, parede), o branco neutro manda (90%): branco continua branco.
# 2) Exposição pelo rosto: preto no lugar, branco esticado com limite, meio-tom leva o rosto a ~150 de 255, sem estourar o vermelho da pele.
# 3) Acabamento Instagram: curva S leve, saturação +8% e nitidez leve, porque a compressão do Instagram achata e amacia a imagem.
# Uso como módulo: filtro_cor(lista_de_quadros_png, caixa_do_rosto) -> string de filtros do FFmpeg.
import numpy as np
from PIL import Image

PELE_RG, PELE_BG, FORCA = 1.28, 0.80, 0.7
ROSTO_ALVO = 150  # brilho do rosto (de 255) depois da correção

BRANCO_MIN = 0.02  # fração mínima do quadro com branco (camisa, parede) para usá-lo como referência
PESO_BRANCO = 0.9  # quando há branco, ele manda mais que a pele: branco tem que continuar branco (R025)

def medir(quadros, rosto):
    pele, lum, brancos, total = [], [], [], 0
    for q in quadros:
        x = np.asarray(Image.open(q).convert("RGB")).astype(float)
        x0, y0, x1, y1 = rosto
        pele.append(x[y0:y1, x0:x1].reshape(-1, 3).mean(0))
        y = 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]
        lum.append(y.ravel())
        # branco: claro, pouco saturado e sem estourar (camisa branca, parede branca)
        mascara = (y > 165) & (x.max(2) < 252) & ((x.max(2) - x.min(2)) < 45)
        brancos.append(x[mascara]); total += y.size
    brancos = np.concatenate(brancos)
    branco = brancos.mean(0) if len(brancos) > BRANCO_MIN * total else None
    return np.mean(pele, 0), np.concatenate(lum), branco

def filtro_cor(quadros, rosto, acabamento=True, quente=0.0):
    pele, lum, branco = medir(quadros, rosto)
    r, g, b = pele
    ganho_r = 1 + FORCA * ((PELE_RG * g / r) - 1)
    ganho_b = 1 + FORCA * ((PELE_BG * g / b) - 1) + quente
    if branco is not None:
        # o branco neutro é a referência mais confiável; a pele entra só como ajuste fino
        rb, gb, bb = branco
        ganho_r = PESO_BRANCO * (gb / rb) + (1 - PESO_BRANCO) * ganho_r
        ganho_b = PESO_BRANCO * (gb / bb) + (1 - PESO_BRANCO) * ganho_b + quente
    # exposição medida no ROSTO (o quadro inteiro engana: parede escura e camiseta preta puxam a média para baixo)
    p2, p995 = np.percentile(lum, 2), np.percentile(lum, 99.5)
    lo = max(p2 - 12, 0) / 255
    hi = min(max(p995 / 240, 0.85), 1.0)
    luz_rosto = (0.2126 * r * ganho_r + 0.7152 * g + 0.0722 * b * ganho_b) / 255
    m = (luz_rosto - lo) / (hi - lo)
    gama = float(np.clip(np.log(m) / np.log(ROSTO_ALVO / 255), 0.85, 1.4)) if 0 < m < 1 else 1.0  # >1 clareia o meio
    verm = (r * ganho_r / 255 - lo) / (hi - lo)  # trava: o vermelho da pele não passa de 0,92
    if 0 < verm < 1 and verm ** (1 / gama) > 0.92:
        gama = max(np.log(verm) / np.log(0.92), 0.85)
    f = [f"colorchannelmixer=rr={ganho_r:.3f}:bb={ganho_b:.3f}",
         f"colorlevels=rimin={lo:.3f}:gimin={lo:.3f}:bimin={lo:.3f}:rimax={hi:.3f}:gimax={hi:.3f}:bimax={hi:.3f}",
         f"eq=gamma={gama:.3f}"]
    if acabamento:
        f += ["curves=all='0/0 0.06/0.05 0.25/0.235 0.5/0.5 0.75/0.765 1/1'", "eq=saturation=1.08", "unsharp=5:5:0.45:5:5:0"]
    info = dict(pele=pele.round(1).tolist(), branco_ref=None if branco is None else branco.round(1).tolist(),
                ganho_r=round(ganho_r, 3), ganho_b=round(ganho_b, 3),
                preto=round(lo, 3), branco=round(hi, 3), gama=round(gama, 3))
    return ",".join(f), info
