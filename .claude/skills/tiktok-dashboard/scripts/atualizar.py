#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Dashboard - Workshop Marketing IA
Coleta dados publicos do perfil e videos via Apify (clockworks~tiktok-scraper)
e gera um dashboard HTML autossuficiente.

Uso:
  python atualizar.py [--abrir] [--usuario USUARIO]
"""

import os
import sys
import json
import time
import base64
import logging
import argparse
import webbrowser
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    print("ERRO: requests nao instalado. Execute: pip install requests")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
ATOR_APIFY = "clockworks~tiktok-scraper"
API_BASE = "https://api.apify.com/v2"
TIMEOUT_SYNC = 300
MAX_VIDEOS = 28
WORKERS_DOWNLOAD = 5

HEADERS_TIKTOK = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.tiktok.com/",
}

# ---------------------------------------------------------------------------
# Utilitarios
# ---------------------------------------------------------------------------

def raiz_projeto() -> Path:
    # script fica em .claude/skills/tiktok-dashboard/scripts/ — sobe 4 niveis
    return Path(__file__).resolve().parents[4]


def carregar_env() -> dict:
    env_path = raiz_projeto() / ".env"
    resultado = {}
    if not env_path.exists():
        return resultado
    with open(env_path, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, _, valor = linha.partition("=")
            resultado[chave.strip()] = valor.strip().strip('"').strip("'")
    return resultado


def get_output_dir() -> Path:
    raiz = raiz_projeto()
    ativo_path = raiz / "meus-produtos" / ".ativo"
    if not ativo_path.exists():
        print("ERRO: meus-produtos/.ativo nao encontrado. Use /produto-novo para criar um produto.")
        sys.exit(1)
    slug = ativo_path.read_text(encoding="utf-8").strip()
    if not slug:
        print("ERRO: meus-produtos/.ativo esta vazio. Use /produto-novo para criar um produto.")
        sys.exit(1)
    out = raiz / "meus-produtos" / slug / "entregas" / "tiktok-dashboard"
    out.mkdir(parents=True, exist_ok=True)
    return out


def configurar_log(output_dir: Path) -> logging.Logger:
    log_path = output_dir / "log.txt"
    logger = logging.getLogger("tiktok-dashboard")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


def baixar_base64(url: str, log: logging.Logger, nome: str = "") -> str:
    if not url:
        return ""
    try:
        resp = requests.get(url, headers=HEADERS_TIKTOK, timeout=20)
        resp.raise_for_status()
        ct = resp.headers.get("Content-Type", "image/jpeg").split(";")[0]
        b64 = base64.b64encode(resp.content).decode()
        return f"data:{ct};base64,{b64}"
    except Exception as e:
        log.warning(f"Falha ao baixar {nome}: {e}")
        return ""


def formatar_numero(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def formatar_duracao(segundos: int) -> str:
    if segundos <= 0:
        return "0s"
    if segundos < 60:
        return f"{segundos}s"
    m, s = divmod(segundos, 60)
    if m < 60:
        return f"{m}min {s}s"
    h, m = divmod(m, 60)
    return f"{h}h {m}min"


def formatar_data(ts: int) -> str:
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(ts).strftime("%d/%m/%Y")
    except Exception:
        return ""

# ---------------------------------------------------------------------------
# Apify
# ---------------------------------------------------------------------------

def chamar_apify(token: str, usuario: str, log: logging.Logger) -> list:
    url = f"{API_BASE}/acts/{ATOR_APIFY}/run-sync-get-dataset-items"
    payload = {
        "profiles": [f"https://www.tiktok.com/@{usuario}"],
        "resultsPerPage": MAX_VIDEOS,
        "scrapeType": "user",
    }
    max_tentativas = 3
    for tentativa in range(1, max_tentativas + 1):
        log.info(f"Chamando Apify para @{usuario} (tentativa {tentativa}/{max_tentativas}, timeout {TIMEOUT_SYNC}s)...")
        try:
            resp = requests.post(
                url,
                params={"token": token},
                json=payload,
                timeout=TIMEOUT_SYNC + 30,
            )
            if resp.status_code == 401:
                log.error("Token Apify invalido. Verifique APIFY_API_TOKEN no .env")
                sys.exit(1)
            if resp.status_code == 402:
                log.error("Limite de uso do Apify atingido. Verifique seu plano em console.apify.com")
                sys.exit(1)
            resp.raise_for_status()
            dados = resp.json()
            if isinstance(dados, list):
                log.info(f"Apify retornou {len(dados)} itens.")
                return dados
            log.error(f"Resposta inesperada: {type(dados)}")
            return []
        except requests.exceptions.Timeout:
            log.warning(f"Timeout na tentativa {tentativa}.")
        except Exception as e:
            log.warning(f"Erro na tentativa {tentativa}: {e}")
        if tentativa < max_tentativas:
            espera = tentativa * 10
            log.info(f"Aguardando {espera}s antes de tentar novamente...")
            time.sleep(espera)
    log.error(f"Todas as {max_tentativas} tentativas falharam. Verifique sua conexao e tente novamente.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Normalizacao
# ---------------------------------------------------------------------------

def normalizar_perfil(itens: list) -> dict:
    author = {}
    for item in itens:
        am = item.get("authorMeta") or item.get("author") or {}
        if am:
            author = am
            break
    return {
        "username": author.get("name") or author.get("uniqueId") or author.get("nickName", ""),
        "nome_display": author.get("nickName") or author.get("name", ""),
        "seguidores": int(author.get("fans") or author.get("followerCount") or 0),
        "seguindo": int(author.get("following") or author.get("followingCount") or 0),
        "likes_totais": int(author.get("heart") or author.get("heartCount") or 0),
        "bio": author.get("signature") or author.get("bio", ""),
        "avatar_url": author.get("avatar") or author.get("avatarUrl") or author.get("avatarThumb", ""),
        "verificado": bool(author.get("verified", False)),
        "total_videos": int(author.get("videoCount") or 0),
        "avatar_b64": "",
    }


def normalizar_video(item: dict) -> dict:
    hashtags_raw = item.get("hashtags") or item.get("challenges") or []
    if hashtags_raw and isinstance(hashtags_raw[0], dict):
        hashtags = [h.get("name", "") for h in hashtags_raw]
    else:
        hashtags = [str(h) for h in hashtags_raw]

    video_obj = item.get("video") or {}
    video_meta = item.get("videoMeta") or {}
    thumbnail_url = (
        video_meta.get("coverUrl")
        or video_meta.get("originalCoverUrl")
        or video_obj.get("cover")
        or video_obj.get("originCover")
        or item.get("thumbnailUrl")
        or item.get("coverUrl")
        or ""
    )

    author_name = (item.get("authorMeta") or {}).get("name") or ""
    vid_id = str(item.get("id", ""))
    link = item.get("webVideoUrl") or (
        f"https://www.tiktok.com/@{author_name}/video/{vid_id}" if author_name and vid_id else ""
    )

    views = int(item.get("playCount") or item.get("videoPlayCount") or 0)
    likes = int(item.get("diggCount") or item.get("likesCount") or 0)
    comentarios = int(item.get("commentCount") or item.get("commentsCount") or 0)
    shares = int(item.get("shareCount") or item.get("sharesCount") or 0)
    saves = int(item.get("collectCount") or item.get("bookmarkCount") or 0)

    return {
        "id": vid_id,
        "texto": item.get("text") or item.get("desc") or "",
        "create_time": int(item.get("createTime") or 0),
        "views": views,
        "likes": likes,
        "comentarios": comentarios,
        "shares": shares,
        "saves": saves,
        "duracao": int((item.get("videoMeta") or {}).get("duration") or item.get("duration") or 0),
        "hashtags": hashtags,
        "thumbnail_url": thumbnail_url,
        "link": link,
        "engajamento": round((likes + comentarios + shares) / views * 100, 2) if views > 0 else 0,
        "thumbnail_b64": "",
        "thumbnail_path": "",
    }

# ---------------------------------------------------------------------------
# Metricas
# ---------------------------------------------------------------------------

def calcular_metricas(videos: list) -> dict:
    if not videos:
        return {}
    total = len(videos)
    media_views = sum(v["views"] for v in videos) / total
    media_eng = sum(v["engajamento"] for v in videos) / total

    # Desempenho por faixa de duracao
    faixas = {"ate_15s": [], "16_30s": [], "31_60s": [], "acima_60s": []}
    for v in videos:
        d = v["duracao"]
        if d <= 15:
            faixas["ate_15s"].append(v)
        elif d <= 30:
            faixas["16_30s"].append(v)
        elif d <= 60:
            faixas["31_60s"].append(v)
        else:
            faixas["acima_60s"].append(v)

    def med(lst, campo):
        return round(sum(x[campo] for x in lst) / len(lst), 2) if lst else 0

    desempenho_duracao = {
        k: {
            "count": len(lst),
            "media_views": round(med(lst, "views")),
            "media_eng": med(lst, "engajamento"),
            "media_likes": round(med(lst, "likes")),
        }
        for k, lst in faixas.items()
    }

    # Heatmap
    heatmap = [[0.0] * 24 for _ in range(7)]
    heatmap_cnt = [[0] * 24 for _ in range(7)]
    for v in videos:
        if v["create_time"]:
            dt = datetime.fromtimestamp(v["create_time"])
            heatmap[dt.weekday()][dt.hour] += v["engajamento"]
            heatmap_cnt[dt.weekday()][dt.hour] += 1
    for d in range(7):
        for h in range(24):
            if heatmap_cnt[d][h]:
                heatmap[d][h] = round(heatmap[d][h] / heatmap_cnt[d][h], 2)

    # Hashtags
    hash_eng: dict = {}
    hash_cnt: dict = {}
    for v in videos:
        for h in v["hashtags"]:
            if h:
                hash_eng[h] = hash_eng.get(h, 0) + v["engajamento"]
                hash_cnt[h] = hash_cnt.get(h, 0) + 1
    top_hashtags = sorted(
        [{"tag": t, "media_eng": round(hash_eng[t] / hash_cnt[t], 2), "count": hash_cnt[t]} for t in hash_eng],
        key=lambda x: x["media_eng"],
        reverse=True,
    )[:10]

    # Legenda vs engajamento
    buckets: dict = {"curta": [], "media": [], "longa": []}
    for v in videos:
        n = len(v["texto"])
        if n <= 50:
            buckets["curta"].append(v["engajamento"])
        elif n <= 150:
            buckets["media"].append(v["engajamento"])
        else:
            buckets["longa"].append(v["engajamento"])
    legenda_eng = {k: round(sum(vs) / len(vs), 2) if vs else 0 for k, vs in buckets.items()}

    # Top 3
    top3 = sorted(videos, key=lambda x: (x["engajamento"], x["views"]), reverse=True)[:3]

    # Semanas
    semanas: dict = defaultdict(list)
    for v in videos:
        if v["create_time"]:
            dt = datetime.fromtimestamp(v["create_time"])
            iso = dt.isocalendar()
            semanas[f"{iso[0]}-W{iso[1]:02d}"].append(v)
    semanas_data = [
        {
            "semana": k,
            "count": len(vs),
            "media_eng": round(sum(x["engajamento"] for x in vs) / len(vs), 2),
            "media_views": round(sum(x["views"] for x in vs) / len(vs)),
        }
        for k, vs in sorted(semanas.items())
    ]

    timeline = sorted(videos, key=lambda x: x["create_time"])

    return {
        "total_videos_coletados": total,
        "media_views": round(media_views),
        "media_engajamento": round(media_eng, 2),
        "total_likes": sum(v["likes"] for v in videos),
        "total_shares": sum(v["shares"] for v in videos),
        "total_saves": sum(v["saves"] for v in videos),
        "total_comentarios": sum(v["comentarios"] for v in videos),
        "desempenho_duracao": desempenho_duracao,
        "heatmap": heatmap,
        "top_hashtags": top_hashtags,
        "legenda_eng": legenda_eng,
        "top3_ids": [v["id"] for v in top3],
        "semanas": semanas_data,
        "timeline_ids": [v["id"] for v in timeline],
    }

# ---------------------------------------------------------------------------
# Historico
# ---------------------------------------------------------------------------

def atualizar_historico(output_dir: Path, perfil: dict, metricas: dict) -> list:
    hist_path = output_dir / "historico.json"
    historico = []
    if hist_path.exists():
        try:
            historico = json.loads(hist_path.read_text(encoding="utf-8"))
        except Exception:
            historico = []
    snapshot = {
        "data": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": int(time.time()),
        "seguidores": perfil.get("seguidores", 0),
        "likes_totais": perfil.get("likes_totais", 0),
        "media_engajamento": metricas.get("media_engajamento", 0),
        "media_views": metricas.get("media_views", 0),
    }
    if historico and historico[-1].get("data") == snapshot["data"]:
        historico[-1] = snapshot
    else:
        historico.append(snapshot)
    hist_path.write_text(json.dumps(historico, ensure_ascii=False, indent=2), encoding="utf-8")
    return historico

# ---------------------------------------------------------------------------
# Download de thumbnails
# ---------------------------------------------------------------------------

def baixar_thumbnails(videos: list, output_dir: Path, log: logging.Logger) -> list:
    imagens_dir = output_dir / "imagens"
    imagens_dir.mkdir(exist_ok=True)

    # Cache de thumbnails ja baixadas
    insights_path = output_dir / "insights.json"
    cache: dict = {}
    if insights_path.exists():
        try:
            ant = json.loads(insights_path.read_text(encoding="utf-8"))
            for v in ant.get("videos", []):
                if v.get("thumbnail_path"):
                    cache[v["id"]] = v["thumbnail_path"]
        except Exception:
            pass

    def baixar_um(video, idx):
        vid_id = video["id"] or str(idx)
        if vid_id in cache:
            rel = cache[vid_id]
            abs_path = output_dir / rel
            if abs_path.exists():
                b64 = base64.b64encode(abs_path.read_bytes()).decode()
                return idx, f"data:image/jpeg;base64,{b64}", rel
        url = video.get("thumbnail_url", "")
        if not url:
            return idx, "", ""
        try:
            resp = requests.get(url, headers=HEADERS_TIKTOK, timeout=20)
            resp.raise_for_status()
            nome = f"video_{idx+1:02d}_{vid_id[:12]}.jpg"
            abs_path = imagens_dir / nome
            abs_path.write_bytes(resp.content)
            b64 = base64.b64encode(resp.content).decode()
            return idx, f"data:image/jpeg;base64,{b64}", f"imagens/{nome}"
        except Exception as e:
            log.warning(f"Falha thumbnail video {idx+1}: {e}")
            return idx, "", ""

    resultados = [""] * len(videos)
    caminhos = [""] * len(videos)
    with ThreadPoolExecutor(max_workers=WORKERS_DOWNLOAD) as ex:
        futuros = {ex.submit(baixar_um, v, i): i for i, v in enumerate(videos)}
        for fut in as_completed(futuros):
            idx, b64, caminho = fut.result()
            resultados[idx] = b64
            caminhos[idx] = caminho

    for i, v in enumerate(videos):
        v["thumbnail_b64"] = resultados[i]
        v["thumbnail_path"] = caminhos[i]
    return videos

# ---------------------------------------------------------------------------
# Salvar insights.json
# ---------------------------------------------------------------------------

def salvar_insights(output_dir: Path, perfil: dict, videos: list, metricas: dict):
    dados = {
        "gerado_em": datetime.now().isoformat(),
        "perfil": {k: val for k, val in perfil.items() if k not in ("avatar_b64",)},
        "videos": [{k: val for k, val in v.items() if k != "thumbnail_b64"} for v in videos],
        "metricas": metricas,
    }
    path = output_dir / "insights.json"
    path.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------------------------------------------------------------------------
# Geracao do HTML
# ---------------------------------------------------------------------------

def gerar_html(perfil, videos, metricas, historico, usuario, output_dir, log):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    nome_exibicao = perfil.get("nome_display") or f"@{usuario}"
    inicial = nome_exibicao[0].upper() if nome_exibicao else "T"

    # Videos para JS (sem thumbnail_b64 gigante no loop — embutido inline)
    videos_js = []
    for v in videos:
        videos_js.append({
            "id": v["id"],
            "texto": v["texto"][:200],
            "data": v["create_time"],
            "data_fmt": formatar_data(v["create_time"]),
            "views": v["views"],
            "views_fmt": formatar_numero(v["views"]),
            "likes": v["likes"],
            "likes_fmt": formatar_numero(v["likes"]),
            "comentarios": v["comentarios"],
            "shares": v["shares"],
            "saves": v["saves"],
            "duracao": v["duracao"],
            "duracao_fmt": formatar_duracao(v["duracao"]),
            "hashtags": v["hashtags"],
            "engajamento": v["engajamento"],
            "link": v["link"],
            "thumbnail_b64": v["thumbnail_b64"],
        })

    top3_ids = set(metricas.get("top3_ids", []))
    top3_videos = [v for v in videos_js if v["id"] in top3_ids][:3]

    nomes_faixas = {
        "ate_15s": "Ate 15s",
        "16_30s": "16 a 30s",
        "31_60s": "31s a 1min",
        "acima_60s": "Acima de 1min",
    }
    ordem_faixas = ["ate_15s", "16_30s", "31_60s", "acima_60s"]

    legenda_eng = metricas.get("legenda_eng", {"curta": 0, "media": 0, "longa": 0})

    # Timeline ordenada
    tl_ids = metricas.get("timeline_ids", [])
    tl_map = {v["id"]: v for v in videos_js}
    tl = [tl_map[i] for i in tl_ids if i in tl_map]

    tem_historico = "true" if len(historico) >= 2 else "false"

    hist_labels = json.dumps([h["data"] for h in historico])
    hist_seg = json.dumps([h["seguidores"] for h in historico])
    hist_eng = json.dumps([h["media_engajamento"] for h in historico])

    sem = metricas.get("semanas", [])
    sem_labels = json.dumps([s["semana"] for s in sem])
    sem_counts = json.dumps([s["count"] for s in sem])
    sem_eng = json.dumps([s["media_eng"] for s in sem])

    tl_labels = json.dumps([v["data_fmt"] for v in tl])
    tl_views = json.dumps([v["views"] for v in tl])
    tl_likes = json.dumps([v["likes"] for v in tl])
    tl_eng_js = json.dumps([v["engajamento"] for v in tl])
    tl_saves = json.dumps([v["saves"] for v in tl])

    heatmap_json = json.dumps(metricas.get("heatmap", [[0]*24]*7))
    hashtags_json = json.dumps(metricas.get("top_hashtags", []))
    videos_json = json.dumps(videos_js, ensure_ascii=False)

    recharts_js = r"""
(function () {
  var R = window.Recharts;
  if (!R || !window.React) { console.error('Recharts nao encontrado'); return; }
  var h = React.createElement;
  var TT_STYLE = { background: 'hsl(240,10%,4%)', border: '1px solid hsl(240,4%,16%)', borderRadius: 8, boxShadow: '0 4px 6px -1px rgba(0,0,0,.6)', fontSize: 12, fontFamily: '"Inter",sans-serif', color: 'hsl(0,0%,98%)', padding: '8px 12px' };
  var TICK = { fontSize: 11, fontFamily: '"Inter",sans-serif', fill: 'hsl(240,5%,65%)' };
  function renderLinha(id, labels, data, cor, fmtFn) {
    var el = document.getElementById(id);
    if (!el || !labels || !labels.length) return;
    var d = labels.map(function (l, i) { return { x: l, v: data[i] }; });
    ReactDOM.createRoot(el).render(
      h(R.ResponsiveContainer, { width: '100%', height: 170 },
        h(R.LineChart, { data: d, margin: { top: 8, right: 40, left: 10, bottom: 20 } },
          h(R.CartesianGrid, { strokeDasharray: '4 4', stroke: 'hsl(240,4%,16%)', vertical: false }),
          h(R.XAxis, { dataKey: 'x', stroke: 'hsl(240,4%,16%)', tick: TICK, interval: 'preserveStartEnd' }),
          h(R.YAxis, { stroke: 'hsl(240,4%,16%)', tick: TICK, tickFormatter: fmtFn, width: 52 }),
          h(R.Tooltip, { contentStyle: TT_STYLE, formatter: function (v) { return [fmtFn(v)]; } }),
          h(R.Line, { type: 'monotone', dataKey: 'v', stroke: cor, strokeWidth: 2,
            dot: { r: 3, fill: cor, strokeWidth: 0 }, activeDot: { r: 5 }, connectNulls: true })
        )
      )
    );
  }
  function renderBarra(id, labels, data, cor) {
    var el = document.getElementById(id);
    if (!el || !labels || !labels.length) return;
    var d = labels.map(function (l, i) { return { x: l, v: data[i] }; });
    ReactDOM.createRoot(el).render(
      h(R.ResponsiveContainer, { width: '100%', height: 150 },
        h(R.BarChart, { data: d, margin: { top: 8, right: 20, left: 10, bottom: 30 } },
          h(R.CartesianGrid, { strokeDasharray: '4 4', stroke: 'hsl(240,4%,16%)', vertical: false }),
          h(R.XAxis, { dataKey: 'x', stroke: 'hsl(240,4%,16%)', tick: TICK, interval: 0, angle: -45, textAnchor: 'end' }),
          h(R.YAxis, { stroke: 'hsl(240,4%,16%)', tick: TICK, width: 40 }),
          h(R.Tooltip, { contentStyle: TT_STYLE }),
          h(R.Bar, { dataKey: 'v', fill: cor || 'hsl(220,70%,50%)', radius: [4, 4, 0, 0] })
        )
      )
    );
  }
  function fmtK(v) { return v >= 1e6 ? (v / 1e6).toFixed(1) + 'M' : v >= 1e3 ? (v / 1e3).toFixed(0) + 'K' : String(v); }
  function fmtPct(v) { return v.toFixed(1) + '%'; }
  function fmtSeg(v) { return v >= 1000 ? (v / 1000).toFixed(1) + 'K' : String(Math.round(v)); }
  window.renderRechartsAll = function () {
    if (typeof TEM !== 'undefined' && TEM && typeof HL !== 'undefined' && HL.length >= 2) {
      renderLinha('c-seg', HL, HS, 'hsl(220,70%,50%)', fmtSeg);
      renderLinha('c-eh', HL, HE, 'hsl(280,65%,60%)', fmtPct);
    }
    if (typeof SL !== 'undefined' && SL.length) renderBarra('c-freq', SL, SC, 'hsl(220,70%,50%)');
    if (typeof TL !== 'undefined' && TL.length > 1) {
      renderLinha('c-tv', TL, TV, 'hsl(220,70%,50%)', fmtK);
      renderLinha('c-tl', TL, TLk, 'hsl(30,80%,55%)', fmtK);
      renderLinha('c-te', TL, TE, 'hsl(280,65%,60%)', fmtPct);
      renderLinha('c-ts', TL, TS, 'hsl(160,60%,45%)', fmtK);
    }
  };
})();
"""

    badges = [("badge-gold", "#1"), ("badge-silver", "#2"), ("badge-bronze", "#3")]

    def top3_card(v, i):
        bc, bt = badges[i]
        thumb = (
            f'<img class="top3-thumb" src="{v["thumbnail_b64"]}" alt="thumb">'
            if v.get("thumbnail_b64")
            else '<div class="top3-thumb no-thumb">Sem imagem</div>'
        )
        texto = v["texto"][:80] + "..." if len(v["texto"]) > 80 else v["texto"]
        link_tag = f'<a class="vlink" href="{v["link"]}" target="_blank">Ver no TikTok</a>' if v.get("link") else ""
        return f"""<div class="top3-card">{thumb}<div class="top3-body">
<span class="top3-badge {bc}">{bt}: {v["duracao_fmt"]}</span>
<div class="top3-texto">{texto}</div>
<div class="top3-stats">
  <span><b>{v["views_fmt"]}</b> views</span>
  <span><b>{formatar_numero(v["likes"])}</b> likes</span>
  <span><b>{formatar_numero(v["comentarios"])}</b> coment.</span>
  <span><b>{formatar_numero(v["shares"])}</b> shares</span>
  <span><b>{formatar_numero(v["saves"])}</b> saves</span>
  <span><b>{v["engajamento"]:.1f}%</b> eng.</span>
</div>{link_tag}</div></div>"""

    top3_html = "\n".join(top3_card(v, i) for i, v in enumerate(top3_videos))

    duracao_cards = ""
    for k in ordem_faixas:
        d = metricas.get("desempenho_duracao", {}).get(k, {})
        mv = formatar_numero(d.get("media_views", 0))
        me = d.get("media_eng", 0)
        cnt = d.get("count", 0)
        duracao_cards += f"""<div class="dur-card">
<div class="dur-label">{nomes_faixas[k]}</div>
<div class="dur-views">{mv}</div>
<div class="dur-sub">media de views</div>
<div class="dur-sub">{me:.1f}% eng. — {cnt} videos</div>
</div>"""

    legenda_html = ""
    for k, label in [("curta", "Curta (ate 50 char)"), ("media", "Media (51-150 char)"), ("longa", "Longa (151+ char)")]:
        legenda_html += f"""<div class="leg-card">
<div class="leg-label">{label}</div>
<div class="leg-val">{legenda_eng.get(k, 0):.1f}%</div>
<div class="leg-sub">eng. medio</div>
</div>"""

    avatar_tag = (
        f'<img class="avatar" src="{perfil["avatar_b64"]}" alt="avatar">'
        if perfil.get("avatar_b64")
        else f'<div class="avatar-fb">{inicial}</div>'
    )
    verificado = '<span class="badge-ver">Verificado</span>' if perfil.get("verificado") else ""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TikTok Dashboard - @{usuario}</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/prop-types/prop-types.min.js" crossorigin></script>
<script src="https://unpkg.com/recharts@2/umd/Recharts.js" crossorigin></script>
<style>
:root{{--bg:#000000;--sur:#111111;--bdr:#252525;--tx:#e8e8e6;--mu:#a8a8a3;--ac:#c4ff5e;--acl:#1a1a1a;--tk:#c4ff5e;--r:0px;--sh:none}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Space Grotesk','Inter',sans-serif;background:var(--bg);color:var(--tx);padding-bottom:80px}}
.topbar{{background:#000000;color:#fff;padding:14px 24px;display:flex;align-items:center;gap:12px;position:sticky;top:0;z-index:100;border-bottom:1px solid #1a1a1a}}
.topbar h1{{font-size:1.05rem;font-weight:600}}
.topbar .sub{{font-size:.78rem;color:#a8a8a3;margin-left:auto;font-family:'JetBrains Mono',monospace}}
.wrap{{max-width:1280px;margin:0 auto;padding:20px 16px}}
.sec{{background:var(--sur);border-top:2px solid #303030;border-bottom:1px solid var(--bdr);padding:20px;margin-bottom:18px}}
.sec-title{{font-size:.85rem;font-weight:600;color:var(--mu);text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px;font-family:'JetBrains Mono',monospace}}
.profile-row{{display:flex;align-items:center;gap:18px}}
.avatar{{width:76px;height:76px;border-radius:50%;object-fit:cover;border:2px solid var(--ac);flex-shrink:0}}
.avatar-fb{{width:76px;height:76px;border-radius:50%;background:var(--ac);display:flex;align-items:center;justify-content:center;font-size:1.8rem;font-weight:700;color:#000;flex-shrink:0}}
.profile-info h2{{font-size:1.3rem;font-weight:700;color:#ffffff}}
.handle{{color:var(--ac);font-size:.88rem;margin-bottom:4px;font-family:'JetBrains Mono',monospace}}
.bio{{font-size:.83rem;color:var(--mu);max-width:560px;line-height:1.45;margin-top:4px}}
.badge-ver{{background:transparent;border:1px solid var(--ac);color:var(--ac);font-size:.7rem;font-weight:600;padding:2px 8px;margin-left:6px;font-family:'JetBrains Mono',monospace}}
.kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}}
.kpi{{background:var(--acl);border-top:2px solid var(--ac);border-bottom:1px solid var(--bdr);padding:14px;text-align:center}}
.kpi-v{{font-size:1.7rem;font-weight:700;color:var(--ac)}}
.kpi-l{{font-size:.75rem;color:var(--mu);margin-top:3px;font-family:'JetBrains Mono',monospace}}
.chart-row{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
@media(max-width:640px){{.chart-row{{grid-template-columns:1fr}}}}
.hm-wrap{{overflow-x:auto}}
.hm-table{{border-collapse:collapse;font-size:.7rem;width:100%}}
.hm-table td,.hm-table th{{padding:2px;text-align:center;min-width:22px}}
.hm-table th{{color:var(--mu);font-weight:500;font-family:'JetBrains Mono',monospace}}
.hm-rl{{color:var(--mu);font-size:.7rem;padding-right:6px;white-space:nowrap;font-family:'JetBrains Mono',monospace}}
.dur-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px}}
.dur-card{{border-top:2px solid #303030;border-bottom:1px solid var(--bdr);padding:12px;text-align:center;background:var(--sur)}}
.dur-label{{font-size:.78rem;font-weight:600;color:var(--mu);margin-bottom:6px;font-family:'JetBrains Mono',monospace}}
.dur-views{{font-size:1.3rem;font-weight:700;color:var(--ac)}}
.dur-sub{{font-size:.72rem;color:var(--mu);margin-top:2px}}
.top3-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}
.top3-card{{border-top:2px solid #303030;overflow:hidden;background:var(--sur)}}
.top3-card:hover{{border-top-color:var(--ac)}}
.top3-thumb{{width:100%;aspect-ratio:9/16;object-fit:cover;background:#141414;display:block;max-height:200px}}
.no-thumb{{display:flex;align-items:center;justify-content:center;color:#a8a8a3;font-size:.75rem}}
.top3-body{{padding:12px}}
.top3-badge{{display:inline-block;font-size:.7rem;font-weight:700;padding:2px 8px;margin-bottom:6px;font-family:'JetBrains Mono',monospace;border:1px solid}}
.badge-gold{{border-color:#f59e0b;color:#f59e0b;background:transparent}}
.badge-silver{{border-color:#a8a8a3;color:#a8a8a3;background:transparent}}
.badge-bronze{{border-color:#9a7bb5;color:#9a7bb5;background:transparent}}
.top3-texto{{font-size:.8rem;color:var(--mu);margin-bottom:8px;line-height:1.4}}
.top3-stats{{display:flex;flex-wrap:wrap;gap:6px;font-size:.76rem;color:var(--mu)}}
.top3-stats b{{color:var(--tx)}}
.vlink{{font-size:.76rem;color:var(--ac);text-decoration:none;display:block;margin-top:8px;font-family:'JetBrains Mono',monospace}}
.vlink:hover{{text-decoration:underline}}
.hb{{display:flex;align-items:center;gap:8px;margin-bottom:5px}}
.hb-name{{font-size:.8rem;color:var(--ac);min-width:110px;font-family:'JetBrains Mono',monospace}}
.hb-track{{flex:1;height:14px;background:#1a1a1a;overflow:hidden}}
.hb-fill{{height:100%;background:var(--ac)}}
.hb-val{{font-size:.75rem;color:var(--mu);min-width:80px;text-align:right;font-family:'JetBrains Mono',monospace}}
.leg-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.leg-card{{border-top:2px solid #303030;border-bottom:1px solid var(--bdr);padding:12px;text-align:center;background:var(--sur)}}
.leg-label{{font-size:.78rem;color:var(--mu);margin-bottom:4px;font-family:'JetBrains Mono',monospace}}
.leg-val{{font-size:1.25rem;font-weight:700;color:var(--ac)}}
.leg-sub{{font-size:.72rem;color:#a8a8a3}}
.filtros{{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px}}
.fb{{padding:5px 13px;border:1px solid #303030;font-size:.78rem;cursor:pointer;background:var(--sur);transition:all .15s;color:var(--mu);font-family:'Space Grotesk',sans-serif}}
.fb.on{{background:var(--ac);color:#000;border-color:var(--ac)}}
.vg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px}}
.vc{{border-top:2px solid #303030;overflow:hidden;cursor:pointer;background:var(--sur)}}
.vc:hover{{border-top-color:var(--ac)}}
.vt-wrap{{position:relative;aspect-ratio:9/16;max-height:190px;background:#141414}}
.vt{{width:100%;height:100%;object-fit:cover;display:block}}
.vdur{{position:absolute;bottom:3px;right:5px;background:rgba(0,0,0,.75);color:#fff;font-size:.62rem;padding:1px 5px;font-family:'JetBrains Mono',monospace}}
.vi{{padding:8px}}
.vtxt{{font-size:.73rem;color:var(--mu);margin-bottom:4px;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.vm{{font-size:.7rem;color:var(--mu);display:flex;flex-wrap:wrap;gap:3px}}
.vlink2{{font-size:.7rem;color:var(--ac);text-decoration:none;font-family:'JetBrains Mono',monospace}}
.freq-insight{{background:var(--acl);border-top:2px solid var(--ac);padding:12px;font-size:.85rem;color:var(--ac);margin-top:12px;font-weight:500}}
@media(max-width:480px){{.profile-row{{flex-direction:column;align-items:flex-start}}.leg-grid{{grid-template-columns:1fr}}.dur-grid{{grid-template-columns:1fr 1fr}}}}
</style>
</head>
<body>
<div class="topbar">
  <svg width="26" height="26" viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.17 8.17 0 004.78 1.52V6.76a4.85 4.85 0 01-1.01-.07z" fill="#69c9d0"/></svg>
  <h1>TikTok Dashboard</h1>
  <span class="sub">Atualizado em {agora}</span>
</div>
<div class="wrap">

<!-- 1. Perfil -->
<div class="sec">
  <div class="profile-row">
    {avatar_tag}
    <div class="profile-info">
      <h2>{nome_exibicao}{verificado}</h2>
      <div class="handle">@{usuario}</div>
      <div class="bio">{perfil.get("bio","")}</div>
    </div>
  </div>
</div>

<!-- 2. KPIs -->
<div class="sec">
  <div class="sec-title">Visao Geral</div>
  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-v">{formatar_numero(perfil.get("seguidores",0))}</div><div class="kpi-l">Seguidores</div></div>
    <div class="kpi"><div class="kpi-v">{formatar_numero(perfil.get("likes_totais",0))}</div><div class="kpi-l">Curtidas Totais</div></div>
    <div class="kpi"><div class="kpi-v" id="kpi-eng">{metricas.get("media_engajamento",0):.1f}%</div><div class="kpi-l">Engajamento Medio</div></div>
    <div class="kpi"><div class="kpi-v" id="kpi-views">{formatar_numero(metricas.get("media_views",0))}</div><div class="kpi-l">Media de Views</div></div>
    <div class="kpi"><div class="kpi-v" id="kpi-count">{metricas.get("total_videos_coletados",0)}</div><div class="kpi-l">Videos Analisados</div></div>
  </div>
</div>

<!-- 3. Evolucao -->
<div class="sec" id="sec-ev"{'' if len(historico)>=2 else ' style="display:none"'}>
  <div class="sec-title">Evolucao ao Longo do Tempo</div>
  <div class="chart-row">
    <div><div id="c-seg"></div></div>
    <div><div id="c-eh"></div></div>
  </div>
</div>

<!-- 4. Duracao -->
<div class="sec">
  <div class="sec-title">Desempenho por Duracao</div>
  <div class="dur-grid">{duracao_cards}</div>
</div>

<!-- 5. Heatmap -->
<div class="sec">
  <div class="sec-title">Melhores Horarios para Postar</div>
  <div class="hm-wrap">
    <table class="hm-table">
      <thead><tr><th></th>{''.join(f'<th>{h:02d}h</th>' for h in range(24))}</tr></thead>
      <tbody id="hm-body"></tbody>
    </table>
  </div>
</div>

<!-- 6. Frequencia -->
<div class="sec">
  <div class="sec-title">Frequencia de Postagem</div>
  <div id="c-freq"></div>
  <div class="freq-insight" id="freq-insight"></div>
</div>

<!-- 7. Top 3 -->
<div class="sec">
  <div class="sec-title">Top 3 Videos</div>
  <div class="top3-grid" id="top3-grid">{top3_html}</div>
</div>

<!-- 8. Hashtags -->
<div class="sec">
  <div class="sec-title">Analise de Hashtags</div>
  <div id="hb-container"></div>
</div>

<!-- 9. Legenda -->
<div class="sec">
  <div class="sec-title">Tamanho da Descricao vs Engajamento</div>
  <div class="leg-grid">{legenda_html}</div>
</div>

<!-- 10. Timeline -->
<div class="sec">
  <div class="sec-title">Linha do Tempo</div>
  <div class="chart-row">
    <div><div id="c-tv"></div></div>
    <div><div id="c-tl"></div></div>
  </div>
  <div class="chart-row" style="margin-top:14px">
    <div><div id="c-te"></div></div>
    <div><div id="c-ts"></div></div>
  </div>
</div>

<!-- 11. Filtros -->
<div class="sec">
  <div class="sec-title">Filtrar Videos</div>
  <div class="filtros" id="fd">
    <button class="fb on" data-d="todos">Todos</button>
    <button class="fb" data-d="ate_15s">Ate 15s</button>
    <button class="fb" data-d="16_30s">16 a 30s</button>
    <button class="fb" data-d="31_60s">31s a 1min</button>
    <button class="fb" data-d="acima_60s">Acima de 1min</button>
  </div>
  <div class="filtros" id="fp">
    <button class="fb on" data-p="0">Todos</button>
    <button class="fb" data-p="7">Ultimos 7 dias</button>
    <button class="fb" data-p="15">Ultimos 15 dias</button>
    <button class="fb" data-p="30">Ultimos 30 dias</button>
  </div>
</div>

<!-- 12. Grade -->
<div class="sec">
  <div class="sec-title">Todos os Videos</div>
  <div class="vg" id="vg"></div>
</div>

</div><!-- /wrap -->

<script>
const VD={videos_json};
const HM={heatmap_json};
const TH={hashtags_json};
const HL={hist_labels};const HS={hist_seg};const HE={hist_eng};
const TEM={tem_historico};
const SL={sem_labels};const SC={sem_counts};const SE={sem_eng};
const TL={tl_labels};const TV={tl_views};const TLk={tl_likes};const TE={tl_eng_js};const TS={tl_saves};
const DIAS=["Seg","Ter","Qua","Qui","Sex","Sab","Dom"];

function fmtN(n){{if(n>=1e6)return(n/1e6).toFixed(1)+'M';if(n>=1e3)return(n/1e3).toFixed(1)+'K';return n;}}

// Heatmap
(function(){{
  const tb=document.getElementById('hm-body');
  const mx=Math.max(...HM.flat());
  DIAS.forEach((d,di)=>{{
    const tr=document.createElement('tr');
    const th=document.createElement('th');th.className='hm-rl';th.textContent=d;tr.appendChild(th);
    for(let h=0;h<24;h++){{
      const td=document.createElement('td');
      const v=HM[di][h];const a=(0.08+((mx>0?v/mx:0)*0.92)).toFixed(2);
      td.style.cssText=`background:rgba(196,255,94,${{a}});height:17px;`;
      td.title=`${{d}} ${{h}}h: ${{v.toFixed(1)}}%`;tr.appendChild(td);
    }}
    tb.appendChild(tr);
  }});
}})();

// Hashtags
(function(){{
  const c=document.getElementById('hb-container');
  if(!TH.length){{c.innerHTML='<p style="color:#a8a8a3;font-size:.83rem">Nenhuma hashtag encontrada.</p>';return;}}
  const mx=Math.max(...TH.map(h=>h.media_eng));
  c.innerHTML=TH.map(h=>{{
    const p=mx>0?(h.media_eng/mx*100).toFixed(1):0;
    return`<div class="hb"><span class="hb-name">#${{h.tag}}</span><div class="hb-track"><div class="hb-fill" style="width:${{p}}%"></div></div><span class="hb-val">${{h.media_eng.toFixed(1)}}% (${{h.count}})</span></div>`;
  }}).join('');
}})();

// Grade
let curD='todos',curP=0;
function renderGrade(vids){{
  const g=document.getElementById('vg');
  g.innerHTML=vids.map(v=>{{
    const th=v.thumbnail_b64?`<img class="vt" src="${{v.thumbnail_b64}}" alt="">`:`<div class="vt" style="display:flex;align-items:center;justify-content:center;color:#a8a8a3;font-size:.72rem">Sem imagem</div>`;
    const lk=v.link?`<a class="vlink2" href="${{v.link}}" target="_blank">Ver no TikTok</a>`:'';
    const tx=v.texto.length>60?v.texto.substring(0,60)+'...':v.texto;
    return`<div class="vc"><div class="vt-wrap">${{th}}<span class="vdur">${{v.duracao_fmt}}</span></div><div class="vi"><div class="vtxt">${{tx}}</div><div class="vm"><span>👁 ${{v.views_fmt}}</span><span>❤ ${{v.likes_fmt}}</span><span>💬 ${{v.comentarios}}</span><span>↗ ${{v.shares}}</span><span>🔖 ${{v.saves}}</span></div><div class="vm" style="margin-top:3px"><span>${{v.engajamento.toFixed(1)}}% eng.</span><span>${{v.data_fmt}}</span></div>${{lk}}</div></div>`;
  }}).join('');
}}

function renderTop3(vids){{
  const el=document.getElementById('top3-grid');if(!el)return;
  const bCls=['badge-gold','badge-silver','badge-bronze'];
  const bTxt=['#1','#2','#3'];
  const top=[...vids].sort((a,b)=>b.engajamento-a.engajamento||b.views-a.views).slice(0,3);
  el.innerHTML=top.map((v,i)=>{{
    const th=v.thumbnail_b64?`<img class="top3-thumb" src="${{v.thumbnail_b64}}" alt="">`:'<div class="top3-thumb no-thumb">Sem imagem</div>';
    const tx=v.texto.length>80?v.texto.substring(0,80)+'...':v.texto;
    const lk=v.link?`<a class="vlink" href="${{v.link}}" target="_blank">Ver no TikTok</a>`:'';
    return`<div class="top3-card">${{th}}<div class="top3-body"><span class="top3-badge ${{bCls[i]}}">${{bTxt[i]}}: ${{v.duracao_fmt}}</span><div class="top3-texto">${{tx}}</div><div class="top3-stats"><span><b>${{v.views_fmt}}</b> views</span><span><b>${{fmtN(v.likes)}}</b> likes</span><span><b>${{fmtN(v.comentarios)}}</b> coment.</span><span><b>${{fmtN(v.shares)}}</b> shares</span><span><b>${{fmtN(v.saves)}}</b> saves</span><span><b>${{v.engajamento.toFixed(1)}}%</b> eng.</span></div>${{lk}}</div></div>`;
  }}).join('');
}}

function filtrar(){{
  let vids=[...VD];
  if(curP>0){{const lim=Date.now()/1000-curP*86400;vids=vids.filter(v=>v.data>=lim);}}
  const ranges={{ate_15s:[0,15],'16_30s':[16,30],'31_60s':[31,60],acima_60s:[61,1e9]}};
  if(curD!=='todos'){{const[mn,mx]=ranges[curD]||[0,1e9];vids=vids.filter(v=>v.duracao>=mn&&v.duracao<=mx);}}
  renderGrade(vids);
  renderTop3(vids);
  if(vids.length){{
    const me=vids.reduce((s,v)=>s+v.engajamento,0)/vids.length;
    const mv=vids.reduce((s,v)=>s+v.views,0)/vids.length;
    const ke=document.getElementById('kpi-eng');
    const kv=document.getElementById('kpi-views');
    const kc=document.getElementById('kpi-count');
    if(ke)ke.textContent=me.toFixed(1)+'%';
    if(kv)kv.textContent=fmtN(Math.round(mv));
    if(kc)kc.textContent=vids.length;
  }}
  document.querySelectorAll('#fd .fb').forEach(b=>b.classList.toggle('on',b.dataset.d===curD));
  document.querySelectorAll('#fp .fb').forEach(b=>b.classList.toggle('on',parseInt(b.dataset.p)===curP));
}}

document.querySelectorAll('#fd .fb').forEach(b=>b.addEventListener('click',()=>{{curD=b.dataset.d;filtrar();}}));
document.querySelectorAll('#fp .fb').forEach(b=>b.addEventListener('click',()=>{{curP=parseInt(b.dataset.p);filtrar();}}));

// Frequencia insight
(function(){{
  const el=document.getElementById('freq-insight');if(!el||!SC.length)return;
  const a4=SC.map((c,i)=>c>=4?SE[i]:null).filter(x=>x!==null);
  const ao=SC.map((c,i)=>c<4?SE[i]:null).filter(x=>x!==null);
  const avg=a=>a.length?(a.reduce((s,v)=>s+v,0)/a.length).toFixed(1):null;
  const v4=avg(a4),vo=avg(ao);
  el.textContent=v4&&vo?`Semanas com 4 ou mais videos tiveram ${{v4}}% de engajamento medio, contra ${{vo}}% nas semanas com menos posts.`:v4?`Semanas com 4 ou mais videos: ${{v4}}% de engajamento medio.`:'Aumente a frequencia para 4+ videos por semana e observe o impacto.';
}})();

// Graficos canvas puro
let _ttEl=null;
function lineChart(id,labels,datasets,opts={{}}){{
  const cv=document.getElementById(id);if(!cv)return;
  const ctx=cv.getContext('2d');
  const W=cv.offsetWidth||480,H=cv.height||170;cv.width=W;
  const pad={{t:18,r:16,b:36,l:52}};
  const w=W-pad.l-pad.r,h=H-pad.t-pad.b;
  ctx.clearRect(0,0,W,H);
  const all=datasets.flatMap(d=>d.data).filter(v=>v!=null);
  const minV=opts.min!=null?opts.min:Math.min(0,...all);
  const maxV=Math.max(...all)||1;const rng=maxV-minV||1;
  const xS=labels.length>1?w/(labels.length-1):w;
  const fmtY=opts.fmtY||(v=>v.toFixed(1));
  ctx.strokeStyle='#1a1a1a';ctx.lineWidth=1;
  for(let i=0;i<=4;i++){{const y=pad.t+(h/4)*i;ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(pad.l+w,y);ctx.stroke();ctx.fillStyle='#a8a8a3';ctx.font='10px "JetBrains Mono",monospace';ctx.textAlign='right';ctx.fillText(fmtY(maxV-(rng/4)*i),pad.l-3,y+4);}}
  const step=Math.ceil(labels.length/7);ctx.fillStyle='#a8a8a3';ctx.font='10px "JetBrains Mono",monospace';ctx.textAlign='center';
  labels.forEach((l,i)=>{{if(i%step===0||i===labels.length-1)ctx.fillText(l,pad.l+i*xS,H-6);}});
  const colors=['#c4ff5e','#9a7bb5','#f59e0b','#7aa8c9'];
  cv._pts=[];
  datasets.forEach((ds,di)=>{{
    const col=ds.color||colors[di%4];ctx.strokeStyle=col;ctx.lineWidth=2;ctx.lineJoin='round';ctx.beginPath();
    let st=false;ds.data.forEach((v,i)=>{{if(v==null)return;const x=pad.l+i*xS,y=pad.t+h-((v-minV)/rng)*h;st?(ctx.lineTo(x,y)):(ctx.moveTo(x,y),st=true);}});ctx.stroke();
    ctx.fillStyle=col;ds.data.forEach((v,i)=>{{if(v==null)return;const x=pad.l+i*xS,y=pad.t+h-((v-minV)/rng)*h;ctx.beginPath();ctx.arc(x,y,3,0,Math.PI*2);ctx.fill();cv._pts.push({{x,y,col,label:ds.label||'',val:fmtY(v),date:labels[i]||''}});}});
    if(ds.label){{ctx.fillStyle=col;ctx.font='10px "JetBrains Mono",monospace';ctx.textAlign='left';ctx.fillText(ds.label,pad.l,pad.t-4);}}
  }});
  if(!cv._tt){{cv._tt=true;cv.addEventListener('mousemove',e=>{{const r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;let cl=null,md=20;(cv._pts||[]).forEach(p=>{{const d=Math.hypot(mx-p.x,my-p.y);if(d<md){{md=d;cl=p;}}}});if(!cl){{if(_ttEl)_ttEl.style.display='none';return;}};if(!_ttEl){{_ttEl=document.createElement('div');_ttEl.style.cssText='position:fixed;background:#141414;color:#fff;border:1px solid #252525;padding:6px 10px;font-size:11px;font-family:"JetBrains Mono",monospace;pointer-events:none;z-index:9999';document.body.appendChild(_ttEl);}}_ttEl.innerHTML=`<b style="color:${{cl.col}}">${{cl.label}}</b><br>${{cl.val}} | ${{cl.date}}`;_ttEl.style.display='block';_ttEl.style.left=(e.clientX+14)+'px';_ttEl.style.top=(e.clientY-10)+'px';}});cv.addEventListener('mouseleave',()=>{{if(_ttEl)_ttEl.style.display='none';}});}}
}}

function barChart(id,labels,vals,color='#c4ff5e'){{
  const cv=document.getElementById(id);if(!cv)return;
  const ctx=cv.getContext('2d');const W=cv.offsetWidth||480,H=cv.height||150;cv.width=W;
  const pad={{t:16,r:16,b:44,l:40}};const w=W-pad.l-pad.r,h=H-pad.t-pad.b;
  ctx.clearRect(0,0,W,H);
  const mx=Math.max(...vals)||1;const bw=w/vals.length*.7,gap=w/vals.length;
  ctx.strokeStyle='#1a1a1a';ctx.lineWidth=1;
  for(let i=0;i<=4;i++){{const y=pad.t+(h/4)*i;ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(pad.l+w,y);ctx.stroke();ctx.fillStyle='#a8a8a3';ctx.font='10px "JetBrains Mono",monospace';ctx.textAlign='right';ctx.fillText((mx*(1-i/4)).toFixed(0),pad.l-3,y+4);}}
  vals.forEach((v,i)=>{{const x=pad.l+i*gap+(gap-bw)/2,bh=(v/mx)*h,y=pad.t+h-bh;ctx.fillStyle=color;ctx.beginPath();if(ctx.roundRect)ctx.roundRect(x,y,bw,bh,3);else ctx.rect(x,y,bw,bh);ctx.fill();ctx.fillStyle='#a8a8a3';ctx.font='9px "JetBrains Mono",monospace';ctx.textAlign='center';const l=(labels[i]||'').substring(0,8);ctx.fillText(l,x+bw/2,H-6);}});
}}


window.addEventListener('DOMContentLoaded',()=>{{renderGrade(VD);setTimeout(renderRechartsAll,100);}});
</script>
<script>{recharts_js}</script>
</body>
</html>"""

    out_path = output_dir / "dashboard.html"
    out_path.write_text(html, encoding="utf-8")
    log.info(f"Dashboard salvo: {out_path}")
    return out_path

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def atualizar_meta_concorrente(conc_dir, slug: str, nome: str, plat: str, handle: str):
    """Cria ou atualiza meta.json com info do concorrente."""
    import json as _json
    from datetime import datetime as _dt
    meta_path = conc_dir / "meta.json"
    meta = {}
    if meta_path.exists():
        try:
            meta = _json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
    meta["slug"] = slug
    if nome and (not meta.get("nome") or meta.get("nome") == slug):
        meta["nome"] = nome
    meta["atualizado_em"] = _dt.now().strftime("%d/%m/%Y %H:%M")
    handles = meta.get("handles", {})
    handles[plat] = handle
    meta["handles"] = handles
    plats = meta.get("plataformas", [])
    if plat not in plats:
        plats.append(plat)
    meta["plataformas"] = plats
    meta_path.write_text(_json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--abrir", action="store_true")
    parser.add_argument("--usuario")
    parser.add_argument("--concorrente", help="Slug do concorrente. Salva em entregas/concorrentes/{slug}/tiktok/")
    parser.add_argument("--nome-bonito", dest="nome_bonito", help="Nome do concorrente para exibir no painel")
    args = parser.parse_args()

    env = carregar_env()
    token = env.get("APIFY_API_TOKEN", "")
    usuario = args.usuario or env.get("TIKTOK_USER", "")

    if not token:
        print("ERRO: APIFY_API_TOKEN nao encontrado no .env")
        print("Configure em console.apify.com > Settings > Integrations > Personal API token")
        sys.exit(1)
    if not usuario:
        print("ERRO: TIKTOK_USER nao encontrado no .env e nao foi passado via --usuario")
        sys.exit(1)

    usuario = usuario.lstrip("@").lower()

    # Resolver caminhos: meu vs concorrente
    # IMPORTANTE: para concorrente, computa o caminho ABSOLUTO a partir de raiz_projeto().
    # Nao usar .parent magic em cima de get_output_dir() (causou bug onde os arquivos foram pra
    # leitura-10x/concorrentes/ em vez de leitura-10x/entregas/concorrentes/).
    if args.concorrente:
        raiz = raiz_projeto()
        ativo_path = raiz / "meus-produtos" / ".ativo"
        if not ativo_path.exists():
            print("ERRO: meus-produtos/.ativo nao encontrado."); sys.exit(1)
        ativo = ativo_path.read_text(encoding="utf-8").strip()
        if not ativo:
            print("ERRO: meus-produtos/.ativo esta vazio."); sys.exit(1)
        conc_root = raiz / "meus-produtos" / ativo / "entregas" / "concorrentes" / args.concorrente
        output_dir = conc_root / "tiktok"
        base_dir = output_dir  # historico fica isolado dentro da pasta da plataforma do concorrente
        # Sanity check: nunca deixar passar caminho fora de entregas/concorrentes
        assert "entregas" in output_dir.parts and "concorrentes" in output_dir.parts, \
            f"ERRO interno: caminho de concorrente invalido: {output_dir}"
    else:
        base_dir = get_output_dir()
        output_dir = base_dir / usuario

    output_dir.mkdir(parents=True, exist_ok=True)
    log = configurar_log(output_dir)
    log.info(f"=== TikTok Dashboard iniciado para @{usuario} ===")

    itens = chamar_apify(token, usuario, log)
    if not itens:
        log.error("Nenhum item retornado. Verifique o username e o token.")
        sys.exit(1)

    log.info("Normalizando dados...")
    perfil = normalizar_perfil(itens)
    videos = [normalizar_video(item) for item in itens[:MAX_VIDEOS]]
    log.info(f"@{perfil.get('username')} — {perfil.get('seguidores',0):,} seguidores — {len(videos)} videos")

    log.info("Baixando avatar...")
    perfil["avatar_b64"] = baixar_base64(perfil.get("avatar_url", ""), log, "avatar")

    log.info("Baixando thumbnails...")
    videos = baixar_thumbnails(videos, output_dir, log)

    log.info("Calculando metricas...")
    metricas = calcular_metricas(videos)
    log.info(f"Engajamento medio: {metricas.get('media_engajamento',0):.2f}%")

    historico = atualizar_historico(base_dir, perfil, metricas)
    log.info(f"Historico: {len(historico)} snapshots")

    salvar_insights(output_dir, perfil, videos, metricas)

    log.info("Gerando dashboard...")
    html_path = gerar_html(perfil, videos, metricas, historico, usuario, output_dir, log)
    log.info(f"=== Pronto: {html_path} ===")

    if args.concorrente:
        atualizar_meta_concorrente(
            conc_root,
            args.concorrente,
            args.nome_bonito or args.concorrente,
            "tiktok",
            usuario,
        )
        log.info(f"meta.json do concorrente atualizado: {conc_root}/meta.json")

    if args.abrir:
        webbrowser.open(html_path.as_uri())


if __name__ == "__main__":
    main()
