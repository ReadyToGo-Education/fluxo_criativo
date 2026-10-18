# Telas da aula gravada só com a câmera: o editor cria as telas a partir do roteiro, sincronizadas com a fala.
#
# 1) exportar: abre o _TELA_R0XX_*.html no Chrome sem janela e grava um PNG por clique (?p=1, ?p=2, ...),
#    em 1920 × 1080 (horizontal, tela cheia) e no recorte da metade de cima do vertical (1080 × 960),
#    tirado em volta da zona útil (x 385 a 1535), com a altura inteira da tela.
#    Uso: py -3 telas.py exportar "_TELA_R0XX_Nome.html" "pasta de saída"
#
# 2) roteiro: lê a seção 1.1 do roteiro (Reels_0XX_*.html, tabela "deixas": fala, cena e clique, frase por frase)
#    e monta a lista "telas" do _edicao_R0XX.json: cada troca de cena e cada clique ancorados numa palavra falada.
#    Uso: py -3 telas.py roteiro "Reels_0XX_Nome.html" ["_edicao_R0XX.json" para gravar a lista nele]
import html, json, os, re, shutil, subprocess, sys
from pathlib import Path

ZONA = (385, 1535)          # zona útil da tela (a mesma do R023 em diante)
VERT = (1080, 960)          # metade de cima do vertical
PALAVRAS_ANCORA = 4         # palavras do começo da frase que ancoram a troca ou o clique


def chrome():
    for p in (os.environ.get("CHROME"),
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chrome")):
        if p and Path(p).exists():
            return p
    raise SystemExit("Chrome ou Edge não encontrado para exportar as telas.")


def total_cliques(html_tela):
    m = re.search(r"\bTOTAL\s*=\s*(\d+)", Path(html_tela).read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


def recorte_vertical(im, zona=ZONA):
    """Recorte 1080:960 em volta da zona útil, com a altura inteira (nada da tela fica de fora)."""
    from PIL import Image
    cx = (zona[0] + zona[1]) / 2
    w = max(zona[1] - zona[0], im.height * VERT[0] / VERT[1])
    h = min(im.height, w * VERT[1] / VERT[0])
    x0 = max(0, min(im.width - w, cx - w / 2)); y0 = (im.height - h) / 2
    return im.crop((round(x0), round(y0), round(x0 + w), round(y0 + h))).resize(VERT, Image.LANCZOS)


def exportar(html_tela, saida, zona=ZONA):
    """Grava tela_NN.png (1920 × 1080) e tela_v_NN.png (1080 × 960) para cada clique. Devolve o número de cliques."""
    from PIL import Image, ImageChops
    html_tela, saida = Path(html_tela).resolve(), Path(saida); saida.mkdir(parents=True, exist_ok=True)
    total = total_cliques(html_tela) or 60
    url = html_tela.as_uri()
    anterior = None
    for p in range(1, total + 1):
        h, v = saida / f"tela_{p:02d}.png", saida / f"tela_v_{p:02d}.png"
        if not (h.exists() and v.exists() and h.stat().st_mtime > html_tela.stat().st_mtime):
            # o tempo virtual deixa as transições (0,4 s) e as fontes do Google terminarem antes da foto
            subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                            "--window-size=1920,1080", "--virtual-time-budget=3000", f"--screenshot={h}", f"{url}?p={p}"],
                           capture_output=True, timeout=60)
            if not h.exists():
                raise SystemExit(f"O Chrome não gravou a tela do clique {p}.")
            im = Image.open(h).convert("RGB")
            if total_cliques(html_tela) is None and anterior is not None and not ImageChops.difference(im, anterior).getbbox():
                h.unlink(); return p - 1  # tela sem TOTAL: parou de mudar, acabaram os cliques
            recorte_vertical(im, zona).save(v)
            anterior = im
    return total


def _texto(celula):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", celula)).split())


def roteiro(html_roteiro):
    """Lista 'telas' a partir da tabela da seção 1.1: [{palavra, cena?, clique?}, ...] na ordem da fala."""
    t = Path(html_roteiro).read_text(encoding="utf-8")
    m = re.search(r'<table[^>]*class="[^"]*deixas[^"]*"[^>]*>(.*?)</table>', t, re.S)
    if not m:
        raise SystemExit("O roteiro não tem a tabela da seção 1.1 (class=\"deixas\").")
    telas, cena = [], None
    for linha in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S):
        cel = [_texto(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", linha, re.S)]
        if len(cel) < 4:
            continue
        _, fala, cena_txt, clique_txt = cel[:4]
        inicio = " ".join(fala.split()[:PALAVRAS_ANCORA])
        nova = "tela" if "tela" in cena_txt.lower() else "rosto" if "rosto" in cena_txt.lower() else None
        itens = []
        if nova and nova != cena:
            itens.append({"palavra": inicio, "cena": nova}); cena = nova
        # "clique 4" ou "clique 9 em "fora da ficha técnica", 10 em "ninguém anotou", ..."
        for num, aspas in re.findall(r"(\d+)(?:\s+em\s+[\"“]([^\"”]+)[\"”])?", clique_txt):
            palavra = aspas or inicio
            if itens and itens[-1]["palavra"] == palavra and "clique" not in itens[-1]:
                itens[-1]["clique"] = int(num)
            else:
                itens.append({"palavra": palavra, "clique": int(num)})
        telas += itens
    return telas


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) >= 4 and sys.argv[1] == "exportar":
        n = exportar(sys.argv[2], sys.argv[3])
        print(f"{n} telas exportadas em {sys.argv[3]}")
    elif len(sys.argv) >= 3 and sys.argv[1] == "roteiro":
        lista = roteiro(sys.argv[2])
        for it in lista:
            print(f"  {it.get('cena', ''):6} {('clique ' + str(it['clique'])) if 'clique' in it else '':10} \"{it['palavra']}\"")
        if len(sys.argv) >= 4:
            arq = Path(sys.argv[3])
            cfg = json.loads(arq.read_text(encoding="utf-8"))
            cfg["telas"] = lista
            arq.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"{len(lista)} marcas gravadas em {arq.name}")
    else:
        raise SystemExit(__doc__ if __doc__ else "uso: telas.py exportar|roteiro ...")
