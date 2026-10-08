#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Dashboard - Workshop Marketing IA
Coleta dados publicos do perfil e posts via Apify e gera dashboard HTML autossuficiente.

Atores Apify utilizados:
  - harvestapi~linkedin-profile-posts  (posts: texto, likes, comentarios, shares, data)
  - dev-fusion~linkedin-profile-scraper-no-cookies  (perfil: seguidores, headline, bio)

Uso:
  python atualizar.py [--abrir] [--perfil URL_OU_HANDLE]
"""

import os
import re
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
ATOR_POSTS   = "harvestapi~linkedin-profile-posts"
ATOR_PERFIL  = "harvestapi~linkedin-profile-scraper"
API_BASE     = "https://api.apify.com/v2"
TIMEOUT_SYNC = 300
MAX_POSTS    = 30
WORKERS_DOWN = 4

TIPOS_VALIDOS = {"Texto", "Imagem", "Video", "Documento", "Artigo", "Repost"}

CORES_TIPO = {
    "Texto":     "#c4ff5e",
    "Imagem":    "#7aa8c9",
    "Video":     "#f59e0b",
    "Documento": "#9a7bb5",
    "Artigo":    "#60b97e",
    "Repost":    "#a8a8a3",
}

# ---------------------------------------------------------------------------
# Utilitarios
# ---------------------------------------------------------------------------

def raiz_projeto() -> Path:
    # script fica em .claude/skills/linkedin-dashboard/scripts/ -- sobe 4 niveis
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


def salvar_no_env(chave: str, valor: str) -> None:
    """Salva (ou atualiza) uma chave no .env da raiz do projeto."""
    if not valor:
        return
    env_path = raiz_projeto() / ".env"
    linhas: list[str] = []
    achou = False
    if env_path.exists():
        with open(env_path, encoding="utf-8") as f:
            for linha in f:
                if linha.strip().startswith(f"{chave}="):
                    linhas.append(f"{chave}={valor}\n")
                    achou = True
                else:
                    linhas.append(linha if linha.endswith("\n") else linha + "\n")
    if not achou:
        linhas.append(f"{chave}={valor}\n")
    env_path.write_text("".join(linhas), encoding="utf-8")


def get_output_dir() -> Path:
    raiz = raiz_projeto()
    ativo_path = raiz / "meus-produtos" / ".ativo"
    if not ativo_path.exists():
        print("ERRO: meus-produtos/.ativo nao encontrado. Use /produto-novo para criar um produto.")
        sys.exit(1)
    slug = ativo_path.read_text(encoding="utf-8").strip()
    if not slug:
        print("ERRO: meus-produtos/.ativo esta vazio.")
        sys.exit(1)
    out = raiz / "meus-produtos" / slug / "entregas" / "linkedin-dashboard"
    out.mkdir(parents=True, exist_ok=True)
    return out


def configurar_log(output_dir: Path) -> logging.Logger:
    log_path = output_dir / "log.txt"
    logger = logging.getLogger("linkedin-dashboard")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


def normalizar_url_perfil(raw: str) -> str:
    s = raw.strip().strip('"').strip("'")
    # Extrai handle de qualquer variante de URL LinkedIn (www, regional como br., uk., etc.)
    m = re.search(r"linkedin\.com/in/([^/?#]+)", s)
    if m:
        return f"https://www.linkedin.com/in/{m.group(1).rstrip('/')}/"
    if s.startswith("/in/"):
        return "https://www.linkedin.com" + s.rstrip("/") + "/"
    handle = s.lstrip("@").rstrip("/")
    return f"https://www.linkedin.com/in/{handle}/"


def extrair_handle(url: str) -> str:
    m = re.search(r"/in/([^/?#]+)", url)
    return m.group(1) if m else url.rstrip("/").split("/")[-1]


def formatar_numero(n) -> str:
    n = int(n or 0)
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def formatar_data(ts: int) -> str:
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(ts).strftime("%d/%m/%Y")
    except Exception:
        return ""


def baixar_base64(url: str, log: logging.Logger, nome: str = "") -> str:
    if not url:
        return ""
    try:
        resp = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        ct = resp.headers.get("Content-Type", "image/jpeg").split(";")[0]
        b64 = base64.b64encode(resp.content).decode()
        return f"data:{ct};base64,{b64}"
    except Exception as e:
        log.warning(f"Falha ao baixar {nome}: {e}")
        return ""


# ---------------------------------------------------------------------------
# Apify
# ---------------------------------------------------------------------------

def chamar_apify(token: str, ator: str, payload: dict, log: logging.Logger,
                 timeout: int = TIMEOUT_SYNC, obrigatorio: bool = True) -> list:
    url = f"{API_BASE}/acts/{ator}/run-sync-get-dataset-items"
    max_tentativas = 3
    for tentativa in range(1, max_tentativas + 1):
        log.info(f"Apify [{ator}] tentativa {tentativa}/{max_tentativas}...")
        try:
            resp = requests.post(
                url,
                params={"token": token},
                json=payload,
                timeout=timeout + 30,
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
                log.info(f"  Retornou {len(dados)} itens.")
                return dados
            if isinstance(dados, dict):
                return [dados]
            log.error(f"Resposta inesperada: {type(dados)}")
            return []
        except requests.exceptions.Timeout:
            log.warning(f"Timeout na tentativa {tentativa}.")
        except Exception as e:
            log.warning(f"Erro na tentativa {tentativa}: {e}")
        if tentativa < max_tentativas:
            espera = tentativa * 10
            log.info(f"Aguardando {espera}s...")
            time.sleep(espera)
    log.error("Todas as tentativas falharam.")
    if obrigatorio:
        sys.exit(1)
    return []


def parse_data_iso(raw) -> int:
    if not raw:
        return 0
    s = str(raw).strip()
    # Tenta fromisoformat (cobre formatos ISO modernos com e sem timezone)
    try:
        return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())
    except Exception:
        pass
    # Fallback: tenta strptime na string completa
    for fmt in ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            return int(datetime.strptime(s, fmt).timestamp())
        except Exception:
            pass
    return 0


# ---------------------------------------------------------------------------
# Normalizacao -- Perfil
# ---------------------------------------------------------------------------

def normalizar_perfil(itens: list, url_perfil: str) -> dict:
    """Suporta resposta de harvestapi~linkedin-profile-scraper (campos: followerCount, firstName, etc.)."""
    vazio = {
        "nome": "", "headline": "", "bio": "", "seguidores": 0,
        "conexoes": 0, "localizacao": "", "perfil_url": url_perfil,
        "avatar_url": "", "avatar_b64": "",
    }
    if not itens:
        return vazio
    item = itens[0] if isinstance(itens, list) else itens
    # harvestapi usa followerCount; outros podem usar followers/followersCount
    seguidores = _to_int(item.get("followerCount") or item.get("followersCount") or item.get("followers"))
    conexoes_raw = str(item.get("connectionsCount") or item.get("connections") or "0")
    try:
        conexoes = int(conexoes_raw.replace("+", "").replace(",", "").strip())
    except Exception:
        conexoes = 0
    # harvestapi retorna firstName + lastName; alguns retornam fullName
    nome = (item.get("fullName") or
            f"{item.get('firstName', '')} {item.get('lastName', '')}".strip() or
            item.get("name") or "")
    # Avatar pode estar em profilePicture (string) ou profilePicture.url (objeto)
    avatar_raw = item.get("profilePicture") or item.get("profilePic") or ""
    if isinstance(avatar_raw, dict):
        avatar_url = avatar_raw.get("url") or avatar_raw.get("src") or ""
    else:
        avatar_url = avatar_raw
    # harvestapi pode devolver location como dict {linkedinText, parsed:{text}}
    loc_raw = item.get("location") or item.get("geo") or ""
    if isinstance(loc_raw, dict):
        loc_raw = (loc_raw.get("linkedinText")
                   or (loc_raw.get("parsed") or {}).get("text") or "")
    return {
        "nome":        nome,
        "headline":    item.get("headline") or item.get("title") or "",
        "bio":         (item.get("about") or item.get("summary") or "")[:300],
        "seguidores":  seguidores,
        "conexoes":    conexoes,
        "localizacao": loc_raw,
        "perfil_url":  item.get("linkedInUrl") or item.get("linkedinUrl") or url_perfil,
        "avatar_url":  avatar_url,
        "avatar_b64":  "",
    }


# ---------------------------------------------------------------------------
# Normalizacao -- Posts
# ---------------------------------------------------------------------------

def detectar_tipo(item: dict) -> str:
    tipo_raw = str(item.get("type") or item.get("postType") or "").upper()

    if item.get("isRepost") or "REPOST" in tipo_raw or "RESHARE" in tipo_raw:
        return "Repost"

    video = item.get("video") or {}
    doc   = item.get("document") or {}
    media = item.get("media") or item.get("images") or item.get("postImages") or []

    if "VIDEO" in tipo_raw or (isinstance(video, dict) and video) or item.get("videoUrl"):
        return "Video"
    if "DOCUMENT" in tipo_raw or "PDF" in tipo_raw or (isinstance(doc, dict) and doc.get("title")):
        return "Documento"
    if "ARTICLE" in tipo_raw or item.get("articleUrl"):
        return "Artigo"
    if "IMAGE" in tipo_raw or (isinstance(media, list) and len(media) > 0):
        return "Imagem"
    return "Texto"


def _to_int(v) -> int:
    """Converte valor para int de forma segura (handles dicts, None, strings)."""
    if v is None:
        return 0
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, str):
        try:
            return int(v)
        except (ValueError, TypeError):
            return 0
    return 0  # dicts, listas e outros tipos nao sao contagens


def normalizar_post(item: dict) -> dict:
    texto = item.get("text") or item.get("commentary") or item.get("content") or ""

    # harvestapi retorna engagement como objeto aninhado: {"likes": N, "comments": N, "shares": N}
    eng_obj = item.get("engagement") or {}
    if isinstance(eng_obj, dict):
        likes       = _to_int(eng_obj.get("likes"))   or _to_int(item.get("numLikes"))   or _to_int(item.get("likeCount"))   or 0
        comentarios = _to_int(eng_obj.get("comments")) or _to_int(item.get("numComments")) or _to_int(item.get("commentCount")) or 0
        shares      = _to_int(eng_obj.get("shares"))   or _to_int(item.get("numShares"))   or _to_int(item.get("shareCount"))   or 0
    else:
        likes       = _to_int(item.get("numLikes"))   or _to_int(item.get("likeCount"))   or 0
        comentarios = _to_int(item.get("numComments")) or _to_int(item.get("commentCount")) or 0
        shares      = _to_int(item.get("numShares"))   or _to_int(item.get("shareCount"))   or 0
    views = _to_int(item.get("numViews")) or _to_int(item.get("viewCount")) or _to_int(item.get("impressions")) or 0

    # harvestapi retorna a data em postedAt: {"timestamp": <ms>, "date": <ISO>}
    posted_at = item.get("postedAt") or {}
    if isinstance(posted_at, dict):
        data_raw = posted_at.get("date") or ""
        ts_ms = posted_at.get("timestamp")
    else:
        data_raw = posted_at
        ts_ms = None
    data_raw = (data_raw or item.get("postedDate") or item.get("createdAt") or
                item.get("date") or item.get("publishedAt") or "")
    ts = parse_data_iso(data_raw)
    if not ts and ts_ms:
        try:
            ts = int(int(ts_ms) / 1000)
        except (ValueError, TypeError):
            ts = 0

    url_post = (item.get("postUrl") or item.get("url") or item.get("shareUrl")
                or item.get("linkedinUrl") or item.get("shareLinkedinUrl") or "")

    imgs = []
    media = item.get("media") or item.get("images") or item.get("postImages") or []
    if isinstance(media, list):
        for m in media:
            u = m.get("url") or m.get("src") or (m if isinstance(m, str) else "")
            if u:
                imgs.append(u)
    elif isinstance(media, dict):
        u = media.get("url") or media.get("src") or ""
        if u:
            imgs.append(u)

    post_id = str(item.get("id") or item.get("postId") or item.get("urn") or "")
    tipo = detectar_tipo(item)

    return {
        "id":           post_id,
        "tipo":         tipo,
        "texto":        texto[:400],
        "create_time":  ts,
        "data_fmt":     formatar_data(ts),
        "likes":        likes,
        "comentarios":  comentarios,
        "shares":       shares,
        "views":        views,
        "url":          url_post,
        "_imgs_url":    imgs[:5],
        "thumbnail_b64":  "",
        "thumbnail_path": "",
        "engajamento":  0,
    }


# ---------------------------------------------------------------------------
# Metricas
# ---------------------------------------------------------------------------

def calcular_metricas(posts: list, perfil: dict) -> dict:
    if not posts:
        return {}

    seg = perfil.get("seguidores", 0)
    sem_seguidores = seg == 0
    seg_den = max(seg, 1)

    for p in posts:
        total_int = p["likes"] + p["comentarios"] + p["shares"]
        if sem_seguidores:
            # Sem seguidores conhecidos: usa interacoes absolutas (nao percentual)
            p["engajamento"] = float(total_int)
        else:
            p["engajamento"] = round(total_int / seg_den * 100, 2)

    total     = len(posts)
    media_eng = round(sum(p["engajamento"] for p in posts) / total, 2)

    def grupo(tipo): return [p for p in posts if p["tipo"] == tipo]
    def med(lst, campo): return round(sum(x[campo] for x in lst) / len(lst), 1) if lst else 0

    desempenho_tipo = {}
    for tipo in TIPOS_VALIDOS:
        g = grupo(tipo)
        desempenho_tipo[tipo] = {
            "count":        len(g),
            "media_likes":  med(g, "likes"),
            "media_coment": med(g, "comentarios"),
            "media_shares": med(g, "shares"),
            "media_eng":    med(g, "engajamento"),
        }

    ativos = [t for t in TIPOS_VALIDOS if desempenho_tipo[t]["count"] > 0]
    tipo_top = max(ativos, key=lambda t: desempenho_tipo[t]["count"]) if ativos else "-"

    # Melhores dias para postar
    dias_eng: list = [[] for _ in range(7)]
    for p in posts:
        if p["create_time"]:
            dt = datetime.fromtimestamp(p["create_time"])
            dias_eng[dt.weekday()].append(p["engajamento"])
    melhores_dias = [
        {
            "dia":       i,
            "media_eng": round(sum(dias_eng[i]) / len(dias_eng[i]), 2) if dias_eng[i] else 0,
            "count":     len(dias_eng[i]),
        }
        for i in range(7)
    ]

    # Frequencia semanal
    semanas: dict = defaultdict(list)
    for p in posts:
        if p["create_time"]:
            dt = datetime.fromtimestamp(p["create_time"])
            iso = dt.isocalendar()
            semanas[f"{iso[0]}-W{iso[1]:02d}"].append(p)
    semanas_data = [
        {
            "semana":    k,
            "count":     len(vs),
            "media_eng": round(sum(x["engajamento"] for x in vs) / len(vs), 2),
        }
        for k, vs in sorted(semanas.items())
    ]

    # Hashtags
    hash_eng: dict = {}
    hash_cnt: dict = {}
    for p in posts:
        tags = re.findall(r"#[\wÀ-ɏ]+", p["texto"])
        for tag in tags:
            t = tag.lower()
            hash_eng[t] = hash_eng.get(t, 0) + p["engajamento"]
            hash_cnt[t] = hash_cnt.get(t, 0) + 1
    top_hashtags = sorted(
        [{"tag": t, "media_eng": round(hash_eng[t] / hash_cnt[t], 2), "count": hash_cnt[t]} for t in hash_eng],
        key=lambda x: x["media_eng"],
        reverse=True,
    )[:10]

    # Tamanho do texto vs engajamento
    buckets: dict = {"curto": [], "medio": [], "longo": []}
    for p in posts:
        n = len(p["texto"])
        if n <= 100:
            buckets["curto"].append(p["engajamento"])
        elif n <= 300:
            buckets["medio"].append(p["engajamento"])
        else:
            buckets["longo"].append(p["engajamento"])
    texto_eng = {k: round(sum(vs) / len(vs), 2) if vs else 0 for k, vs in buckets.items()}
    texto_cnt = {k: len(vs) for k, vs in buckets.items()}

    top3     = sorted(posts, key=lambda x: (x["engajamento"], x["likes"]), reverse=True)[:3]
    timeline = sorted(posts, key=lambda x: x["create_time"])

    return {
        "total_posts":       total,
        "media_engajamento": media_eng,
        "sem_seguidores":    sem_seguidores,
        "total_likes":       sum(p["likes"] for p in posts),
        "total_comentarios": sum(p["comentarios"] for p in posts),
        "total_shares":      sum(p["shares"] for p in posts),
        "tipo_top":          tipo_top,
        "desempenho_tipo":   desempenho_tipo,
        "melhores_dias":     melhores_dias,
        "semanas":           semanas_data,
        "top_hashtags":      top_hashtags,
        "texto_eng":         texto_eng,
        "texto_cnt":         texto_cnt,
        "top3_ids":          [p["id"] for p in top3],
        "timeline_ids":      [p["id"] for p in timeline],
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
        "data":               datetime.now().strftime("%Y-%m-%d"),
        "timestamp":          int(time.time()),
        "seguidores":         perfil.get("seguidores", 0),
        "conexoes":           perfil.get("conexoes", 0),
        "media_engajamento":  metricas.get("media_engajamento", 0),
    }
    if historico and historico[-1].get("data") == snapshot["data"]:
        historico[-1] = snapshot
    else:
        historico.append(snapshot)
    hist_path.write_text(json.dumps(historico, ensure_ascii=False, indent=2), encoding="utf-8")
    return historico


# ---------------------------------------------------------------------------
# Download de imagens dos posts
# ---------------------------------------------------------------------------

def baixar_thumbnails(posts: list, output_dir: Path, log: logging.Logger) -> list:
    imagens_dir = output_dir / "imagens"
    imagens_dir.mkdir(exist_ok=True)

    insights_path = output_dir / "insights.json"
    cache: dict = {}
    if insights_path.exists():
        try:
            ant = json.loads(insights_path.read_text(encoding="utf-8"))
            for p in ant.get("posts", []):
                if p.get("thumbnail_path"):
                    cache[p["id"]] = p["thumbnail_path"]
        except Exception:
            pass

    def baixar_um(post, idx):
        pid = post["id"] or str(idx)
        if pid in cache:
            rel = cache[pid]
            abs_path = output_dir / rel
            if abs_path.exists():
                b64 = base64.b64encode(abs_path.read_bytes()).decode()
                return idx, f"data:image/jpeg;base64,{b64}", rel
        imgs = post.get("_imgs_url") or []
        url  = imgs[0] if imgs else ""
        if not url:
            return idx, "", ""
        try:
            resp = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            nome = f"post_{idx+1:02d}_{pid[:12]}.jpg"
            abs_path = imagens_dir / nome
            abs_path.write_bytes(resp.content)
            b64 = base64.b64encode(resp.content).decode()
            return idx, f"data:image/jpeg;base64,{b64}", f"imagens/{nome}"
        except Exception as e:
            log.warning(f"Falha imagem post {idx+1}: {e}")
            return idx, "", ""

    resultados = [""] * len(posts)
    caminhos   = [""] * len(posts)
    with ThreadPoolExecutor(max_workers=WORKERS_DOWN) as ex:
        futuros = {ex.submit(baixar_um, p, i): i for i, p in enumerate(posts)}
        for fut in as_completed(futuros):
            idx, b64, caminho = fut.result()
            resultados[idx] = b64
            caminhos[idx]   = caminho

    for i, p in enumerate(posts):
        p["thumbnail_b64"]  = resultados[i]
        p["thumbnail_path"] = caminhos[i]
    return posts


# ---------------------------------------------------------------------------
# Checagem de saude (deteta mudanca de schema do scraper)
# ---------------------------------------------------------------------------

def checar_saude_dados(posts: list, perfil: dict, log: logging.Logger) -> None:
    """Alerta no log quando o schema do scraper provavelmente mudou.

    Campo vazio em massa (todas as datas zeradas, todas as URLs vazias) e o
    sintoma classico de um campo renomeado na API do harvestapi. Sem este
    aviso, o script gera um dashboard quebrado em silencio. Com ele, quem
    rodar ve o alerta na hora e sabe que precisa revisar normalizar_post()."""
    n = len(posts)
    if not n:
        return
    sem_data  = sum(1 for p in posts if not p.get("create_time"))
    sem_url   = sum(1 for p in posts if not p.get("url"))
    com_img   = sum(1 for p in posts if p.get("_imgs_url"))
    sem_thumb = sum(1 for p in posts if p.get("_imgs_url") and not p.get("thumbnail_path"))

    if sem_data == n:
        log.warning(f"[CHECAGEM] Todos os {n} posts sem data. O campo de data do "
                    "scraper provavelmente mudou de nome. Revise normalizar_post().")
    if sem_url == n:
        log.warning(f"[CHECAGEM] Todos os {n} posts sem URL. O campo de link do "
                    "scraper provavelmente mudou de nome. Revise normalizar_post().")
    if com_img and sem_thumb == com_img:
        log.warning(f"[CHECAGEM] {com_img} posts tem imagem mas nenhuma thumbnail "
                    "baixou. Verifique a URL das imagens ou a conexao.")
    if not perfil.get("seguidores"):
        log.warning("[CHECAGEM] Perfil sem seguidores. O scraper de perfil pode ter "
                    "retornado vazio. Confira o input do harvestapi~linkedin-profile-scraper.")


# ---------------------------------------------------------------------------
# Salvar insights.json
# ---------------------------------------------------------------------------

def salvar_insights(output_dir: Path, perfil: dict, posts: list, metricas: dict):
    dados = {
        "gerado_em": datetime.now().isoformat(),
        "perfil":    {k: v for k, v in perfil.items() if k != "avatar_b64"},
        "posts":     [
            {k: v for k, v in p.items()
             if k != "thumbnail_b64" and not k.startswith("_")}
            for p in posts
        ],
        "metricas":  metricas,
    }
    (output_dir / "insights.json").write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

def gerar_html(perfil, posts, metricas, historico, handle, output_dir, log):
    agora  = datetime.now().strftime("%d/%m/%Y %H:%M")
    nome   = perfil.get("nome") or f"@{handle}"
    inicial = nome[0].upper() if nome else "L"

    posts_js = [
        {
            "id":           p["id"],
            "tipo":         p["tipo"],
            "texto":        p["texto"][:200],
            "data":         p["create_time"],
            "data_fmt":     p["data_fmt"],
            "likes":        p["likes"],
            "comentarios":  p["comentarios"],
            "shares":       p["shares"],
            "views":        p["views"],
            "engajamento":  p["engajamento"],
            "url":          p["url"],
            "thumbnail_b64": p["thumbnail_b64"],
        }
        for p in posts
    ]

    top3_ids  = set(metricas.get("top3_ids", []))
    top3_posts = [p for p in posts_js if p["id"] in top3_ids][:3]

    tl_ids = metricas.get("timeline_ids", [])
    tl_map = {p["id"]: p for p in posts_js}
    tl     = [tl_map[i] for i in tl_ids if i in tl_map]

    tem_historico  = "true" if len(historico) >= 2 else "false"
    hist_labels    = json.dumps([h["data"] for h in historico])
    hist_seg       = json.dumps([h["seguidores"] for h in historico])
    hist_eng       = json.dumps([h["media_engajamento"] for h in historico])

    sem        = metricas.get("semanas", [])
    sem_labels = json.dumps([s["semana"] for s in sem])
    sem_counts = json.dumps([s["count"] for s in sem])
    sem_eng    = json.dumps([s["media_eng"] for s in sem])

    dias_nomes   = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
    melhores_dias = metricas.get("melhores_dias", [])
    dias_labels  = json.dumps([dias_nomes[d["dia"]] for d in melhores_dias])
    dias_eng_data = json.dumps([d["media_eng"] for d in melhores_dias])

    tl_labels  = json.dumps([p["data_fmt"] for p in tl])
    tl_likes   = json.dumps([p["likes"]     for p in tl])
    tl_coments = json.dumps([p["comentarios"] for p in tl])
    tl_shares  = json.dumps([p["shares"]    for p in tl])
    tl_eng_js  = json.dumps([p["engajamento"] for p in tl])

    hashtags_json  = json.dumps(metricas.get("top_hashtags", []))
    posts_json     = json.dumps(posts_js, ensure_ascii=False)
    cores_json     = json.dumps(CORES_TIPO)
    desempenho_tipo = metricas.get("desempenho_tipo", {})
    texto_eng      = metricas.get("texto_eng", {})
    texto_cnt      = metricas.get("texto_cnt", {})
    sem_seg        = metricas.get("sem_seguidores", False)
    eng_suf        = "" if sem_seg else "%"
    eng_lbl        = "Interacoes Medias" if sem_seg else "Engajamento Medio"
    sem_seg_js     = "true" if sem_seg else "false"
    def fmt_eng(v): return f"{v:.0f}" if sem_seg else f"{v:.2f}%"

    avatar_tag = (
        f'<img class="avatar" src="{perfil["avatar_b64"]}" alt="avatar">'
        if perfil.get("avatar_b64")
        else f'<div class="avatar-fb">{inicial}</div>'
    )

    tipos_order = ["Texto", "Imagem", "Video", "Documento", "Artigo", "Repost"]
    tipo_cards  = ""
    for tipo in tipos_order:
        d = desempenho_tipo.get(tipo, {})
        if d.get("count", 0) == 0:
            continue
        cor = CORES_TIPO.get(tipo, "#c4ff5e")
        tipo_cards += (
            f'<div class="tipo-card" style="border-top-color:{cor}">'
            f'<div class="tipo-nome" style="color:{cor}">{tipo} ({d["count"]})</div>'
            f'<div class="tipo-mets">'
            f'<div><div class="met-lbl">Media likes</div><div class="met-val">{formatar_numero(d["media_likes"])}</div></div>'
            f'<div><div class="met-lbl">Media coment.</div><div class="met-val">{formatar_numero(d["media_coment"])}</div></div>'
            f'<div><div class="met-lbl">Media shares</div><div class="met-val">{formatar_numero(d["media_shares"])}</div></div>'
            f'<div><div class="met-lbl">Eng. medio</div><div class="met-val" style="color:{cor}">{d["media_eng"]}{eng_suf}</div></div>'
            f'</div></div>'
        )

    b_cls = ["badge-gold", "badge-silver", "badge-bronze"]
    b_txt = ["#1", "#2", "#3"]
    top3_html = ""
    for i, p in enumerate(top3_posts):
        cor    = CORES_TIPO.get(p["tipo"], "#c4ff5e")
        thumb  = (
            f'<img class="top3-thumb" src="{p["thumbnail_b64"]}" alt="">'
            if p.get("thumbnail_b64")
            else f'<div class="no-thumb" style="--cc:{cor}"><span class="tc-quote">"</span><span class="tc-txt">{p["texto"][:120]}</span></div>'
        )
        link   = f'<a class="vlink" href="{p["url"]}" target="_blank">Ver post</a>' if p.get("url") else ""
        texto  = p["texto"][:100] + "..." if len(p["texto"]) > 100 else p["texto"]
        top3_html += (
            f'<div class="top3-card">{thumb}'
            f'<div class="top3-body">'
            f'<span class="top3-badge {b_cls[i]}">{b_txt[i]}</span>'
            f'<span class="tipo-badge" style="border-color:{cor};color:{cor}">{p["tipo"]}</span>'
            f'<div class="top3-texto">{texto}</div>'
            f'<div class="top3-stats">'
            f'<span><b>{formatar_numero(p["likes"])}</b> likes</span>'
            f'<span><b>{formatar_numero(p["comentarios"])}</b> coment.</span>'
            f'<span><b>{formatar_numero(p["shares"])}</b> shares</span>'
            f'<span><b>{fmt_eng(p["engajamento"])}</b> eng.</span>'
            f'</div>'
            f'<div class="top3-data">{p["data_fmt"]}</div>'
            f'{link}</div></div>'
        )

    texto_html = ""
    for k, label in [("curto", "Curto (ate 100 char)"), ("medio", "Medio (101-300 char)"), ("longo", "Longo (301+ char)")]:
        v = texto_eng.get(k, 0)
        c = texto_cnt.get(k, 0)
        texto_html += (
            f'<div class="tit-card">'
            f'<div class="tit-label">{label}</div>'
            f'<div class="tit-val">{v}{eng_suf}</div>'
            f'<div class="tit-sub">eng. medio -- {c} posts</div>'
            f'</div>'
        )

    sec_ev_style = "" if len(historico) >= 2 else " style=\"display:none\""
    headline_html = f'<div class="headline">{perfil.get("headline","")}</div>' if perfil.get("headline") else ""
    bio_html = f'<div class="bio">{perfil.get("bio","")[:150]}</div>' if perfil.get("bio") else ""

    recharts_js = r"""
(function () {
  var R = window.Recharts;
  if (!R || !window.React) { return; }
  var h = React.createElement;
  var TT = { background: '#141414', border: '1px solid #252525', borderRadius: 0, fontSize: 11, fontFamily: '"JetBrains Mono",monospace', color: '#e8e8e6' };
  var TK = { fontSize: 10, fontFamily: '"JetBrains Mono",monospace', fill: '#a8a8a3' };
  function linha(id, labels, data, cor, fmt) {
    var el = document.getElementById(id); if (!el || !labels.length) return;
    var d = labels.map(function(l,i){return{x:l,v:data[i]};});
    ReactDOM.createRoot(el).render(h(R.ResponsiveContainer,{width:'100%',height:170},
      h(R.LineChart,{data:d,margin:{top:8,right:40,left:10,bottom:20}},
        h(R.CartesianGrid,{strokeDasharray:'4 4',stroke:'#252525',vertical:false}),
        h(R.XAxis,{dataKey:'x',stroke:'#a8a8a3',tick:TK,interval:'preserveStartEnd'}),
        h(R.YAxis,{stroke:'#a8a8a3',tick:TK,tickFormatter:fmt,width:52}),
        h(R.Tooltip,{contentStyle:TT,formatter:function(v){return[fmt(v)];}}),
        h(R.Line,{type:'monotone',dataKey:'v',stroke:cor,strokeWidth:2,dot:{r:3,fill:cor,strokeWidth:0},activeDot:{r:5},connectNulls:true}))));
  }
  function barra(id, labels, data, cor, h2) {
    var el = document.getElementById(id); if (!el || !labels.length) return;
    var d = labels.map(function(l,i){return{x:l,v:data[i]};});
    ReactDOM.createRoot(el).render(h(R.ResponsiveContainer,{width:'100%',height:h2||150},
      h(R.BarChart,{data:d,margin:{top:8,right:20,left:10,bottom:30}},
        h(R.CartesianGrid,{strokeDasharray:'4 4',stroke:'#252525',vertical:false}),
        h(R.XAxis,{dataKey:'x',stroke:'#a8a8a3',tick:TK,interval:0,angle:-30,textAnchor:'end'}),
        h(R.YAxis,{stroke:'#a8a8a3',tick:TK,width:40}),
        h(R.Tooltip,{contentStyle:TT}),
        h(R.Bar,{dataKey:'v',fill:cor||'#c4ff5e',radius:[3,3,0,0]}))));
  }
  function fK(v){return v>=1e6?(v/1e6).toFixed(1)+'M':v>=1e3?(v/1e3).toFixed(0)+'K':String(v);}
  function fP(v){return v.toFixed(1)+'%';}
  function fS(v){return v>=1000?(v/1000).toFixed(1)+'K':String(Math.round(v));}
  window.renderRechartsAll = function() {
    if (typeof TEM!=='undefined' && TEM && typeof HL!=='undefined' && HL.length>=2) {
      linha('c-seg',HL,HS,'#c4ff5e',fS);
      linha('c-eh',HL,HE,'#0077b5',fP);
    }
    if (typeof DL!=='undefined' && DL.length) barra('c-dias',DL,DE,'#c4ff5e',170);
    if (typeof SL!=='undefined' && SL.length) barra('c-freq',SL,SC,'#7aa8c9',150);
    if (typeof TL!=='undefined' && TL.length>1) {
      linha('c-tl',TL,TLk,'#c4ff5e',fK);
      linha('c-tc',TL,TC,'#7aa8c9',fK);
      linha('c-ts',TL,TS,'#9a7bb5',fK);
      linha('c-te',TL,TE,'#f59e0b',fP);
    }
  };
})();
"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LinkedIn Dashboard - {nome}</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/prop-types/prop-types.min.js" crossorigin></script>
<script src="https://unpkg.com/recharts@2/umd/Recharts.js" crossorigin></script>
<style>
:root{{--bg:#000000;--sur:#111111;--bdr:#252525;--tx:#e8e8e6;--mu:#a8a8a3;--ac:#c4ff5e;--acl:#1a1a1a;--li:#0077b5}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Space Grotesk','Inter',sans-serif;background:var(--bg);color:var(--tx);padding-bottom:80px}}
.topbar{{background:#000;color:#fff;padding:14px 24px;display:flex;align-items:center;gap:12px;position:sticky;top:0;z-index:100;border-bottom:1px solid #1a1a1a}}
.topbar h1{{font-size:1.05rem;font-weight:600}}
.topbar .sub{{font-size:.78rem;color:#a8a8a3;margin-left:auto;font-family:'JetBrains Mono',monospace}}
.wrap{{max-width:1280px;margin:0 auto;padding:20px 16px}}
.sec{{background:var(--sur);border-top:2px solid #303030;border-bottom:1px solid var(--bdr);padding:20px;margin-bottom:18px}}
.sec-title{{font-size:.85rem;font-weight:600;color:var(--mu);text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px;font-family:'JetBrains Mono',monospace}}
.profile-row{{display:flex;align-items:center;gap:18px;flex-wrap:wrap}}
.avatar{{width:76px;height:76px;border-radius:50%;object-fit:cover;border:2px solid var(--ac);flex-shrink:0}}
.avatar-fb{{width:76px;height:76px;border-radius:50%;background:var(--li);display:flex;align-items:center;justify-content:center;font-size:1.8rem;font-weight:700;color:#fff;flex-shrink:0}}
.profile-info h2{{font-size:1.3rem;font-weight:700;color:#fff}}
.handle{{color:var(--ac);font-size:.85rem;margin-bottom:3px;font-family:'JetBrains Mono',monospace;word-break:break-all}}
.headline{{font-size:.88rem;color:var(--mu);max-width:540px;line-height:1.45;margin-top:3px}}
.bio{{font-size:.8rem;color:#a8a8a3;max-width:540px;line-height:1.4;margin-top:4px}}
.kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px}}
.kpi{{background:var(--acl);border-top:2px solid var(--ac);border-bottom:1px solid var(--bdr);padding:14px;text-align:center}}
.kpi-v{{font-size:1.7rem;font-weight:700;color:var(--ac)}}
.kpi-l{{font-size:.75rem;color:var(--mu);margin-top:3px;font-family:'JetBrains Mono',monospace}}
.tipos-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}}
.tipo-card{{background:var(--sur);border-top:2px solid #303030;border-bottom:1px solid var(--bdr);padding:14px}}
.tipo-nome{{font-size:.85rem;font-weight:700;margin-bottom:10px}}
.tipo-mets{{display:flex;gap:10px;flex-wrap:wrap}}
.met-lbl{{font-size:.72rem;color:var(--mu)}}
.met-val{{font-size:1.1rem;font-weight:700;color:#fff}}
.chart-row{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
@media(max-width:640px){{.chart-row{{grid-template-columns:1fr}}}}
.top3-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}
.top3-card{{border-top:2px solid #303030;overflow:hidden;background:var(--sur)}}
.top3-card:hover{{border-top-color:var(--ac)}}
.top3-thumb{{width:100%;aspect-ratio:1.5;object-fit:cover;background:#141414;display:block}}
.no-thumb{{display:flex;flex-direction:column;justify-content:flex-end;padding:10px;aspect-ratio:1.5;width:100%;background:linear-gradient(135deg,#141414 60%,#1e2a14 100%);border-bottom:2px solid var(--cc,#c4ff5e);overflow:hidden;position:relative}}
.no-thumb .tc-quote{{position:absolute;top:-4px;left:8px;font-size:3.5rem;color:var(--cc,#c4ff5e);opacity:.18;line-height:1;font-family:Georgia,serif;pointer-events:none}}
.no-thumb .tc-txt{{font-size:.7rem;color:#d8d8d4;line-height:1.35;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden;position:relative}}
.top3-body{{padding:12px}}
.top3-badge{{display:inline-block;font-size:.7rem;font-weight:700;padding:2px 8px;margin-bottom:4px;font-family:'JetBrains Mono',monospace;border:1px solid}}
.tipo-badge{{display:inline-block;font-size:.7rem;font-weight:600;padding:2px 8px;margin-left:4px;margin-bottom:4px;font-family:'JetBrains Mono',monospace;border:1px solid;background:transparent}}
.badge-gold{{border-color:#f59e0b;color:#f59e0b;background:transparent}}
.badge-silver{{border-color:#a8a8a3;color:#a8a8a3;background:transparent}}
.badge-bronze{{border-color:#9a7bb5;color:#9a7bb5;background:transparent}}
.top3-texto{{font-size:.8rem;color:var(--mu);margin:6px 0;line-height:1.4}}
.top3-stats{{display:flex;flex-wrap:wrap;gap:6px;font-size:.76rem;color:var(--mu)}}
.top3-stats b{{color:var(--tx)}}
.top3-data{{font-size:.7rem;color:#a8a8a3;margin-top:4px;font-family:'JetBrains Mono',monospace}}
.vlink{{display:inline-block;font-size:.74rem;font-weight:600;padding:5px 12px;border:1px solid var(--ac);color:var(--ac);background:transparent;text-decoration:none;font-family:'JetBrains Mono',monospace;margin-top:8px;transition:all .15s}}
.vlink:hover{{background:var(--ac);color:#000}}
.hb{{display:flex;align-items:center;gap:8px;margin-bottom:5px}}
.hb-name{{font-size:.8rem;color:var(--ac);min-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-family:'JetBrains Mono',monospace}}
.hb-track{{flex:1;height:14px;background:#1a1a1a;overflow:hidden}}
.hb-fill{{height:100%;background:var(--ac)}}
.hb-val{{font-size:.75rem;color:var(--mu);min-width:90px;text-align:right;font-family:'JetBrains Mono',monospace}}
.tit-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.tit-card{{border-top:2px solid #303030;border-bottom:1px solid var(--bdr);padding:14px;text-align:center;background:var(--sur)}}
.tit-label{{font-size:.78rem;color:var(--mu);margin-bottom:6px;font-family:'JetBrains Mono',monospace}}
.tit-val{{font-size:1.3rem;font-weight:700;color:var(--ac)}}
.tit-sub{{font-size:.72rem;color:#a8a8a3;margin-top:2px}}
.freq-insight{{background:var(--acl);border-top:2px solid var(--ac);padding:12px;font-size:.85rem;color:var(--ac);margin-top:12px;font-weight:500}}
.filtros{{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px}}
.fb{{padding:5px 13px;border:1px solid #303030;font-size:.78rem;cursor:pointer;background:var(--sur);transition:all .15s;color:var(--mu);font-family:'Space Grotesk',sans-serif}}
.fb.on{{background:var(--ac);color:#000;border-color:var(--ac)}}
.pg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}}
.pc{{border-top:2px solid #303030;overflow:hidden;background:var(--sur)}}
.pc:hover{{border-top-color:var(--ac)}}
.pt-wrap{{position:relative;aspect-ratio:1.5;background:#141414}}
.pt{{width:100%;height:100%;object-fit:cover;display:block}}
.pt-sem-img{{width:100%;height:100%;display:flex;flex-direction:column;justify-content:flex-end;padding:8px;background:linear-gradient(135deg,#141414 60%,#1e2a14 100%);border-bottom:2px solid var(--cc,#c4ff5e);overflow:hidden;position:relative}}
.pt-sem-img .tc-quote{{position:absolute;top:-4px;left:6px;font-size:3rem;color:var(--cc,#c4ff5e);opacity:.18;line-height:1;font-family:Georgia,serif;pointer-events:none}}
.pt-sem-img .tc-txt{{font-size:.65rem;color:#d8d8d4;line-height:1.3;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden;position:relative}}
.pt-tipo{{position:absolute;top:6px;left:6px;font-size:.65rem;font-weight:700;padding:2px 7px;font-family:'JetBrains Mono',monospace;border:1px solid;background:rgba(0,0,0,.7)}}
.pi{{padding:8px}}
.ptxt{{font-size:.73rem;color:var(--mu);margin-bottom:4px;line-height:1.3;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}
.pm{{font-size:.7rem;color:var(--mu);display:flex;flex-wrap:wrap;gap:3px;margin-top:2px}}
.plink{{display:inline-block;font-size:.7rem;font-weight:600;padding:4px 10px;border:1px solid var(--ac);color:var(--ac);background:transparent;text-decoration:none;font-family:'JetBrains Mono',monospace;margin-top:5px;transition:all .15s}}
.plink:hover{{background:var(--ac);color:#000}}
@media(max-width:480px){{.profile-row{{flex-direction:column;align-items:flex-start}}.tit-grid{{grid-template-columns:1fr}}.kpi-grid{{grid-template-columns:1fr 1fr}}}}
</style>
</head>
<body>
<div class="topbar">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="#0077b5"/></svg>
  <h1>LinkedIn Dashboard</h1>
  <span class="sub">Atualizado em {agora}</span>
</div>
<div class="wrap">

<div class="sec">
  <div class="profile-row">
    {avatar_tag}
    <div class="profile-info">
      <h2>{nome}</h2>
      <div class="handle">{perfil.get("perfil_url","")}</div>
      {headline_html}
      {bio_html}
    </div>
  </div>
</div>

<div class="sec">
  <div class="sec-title">Visao Geral</div>
  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-v">{formatar_numero(perfil.get("seguidores",0))}</div><div class="kpi-l">Seguidores</div></div>
    <div class="kpi"><div class="kpi-v">{formatar_numero(perfil.get("conexoes",0))}</div><div class="kpi-l">Conexoes</div></div>
    <div class="kpi"><div class="kpi-v" id="kpi-eng">{fmt_eng(metricas.get("media_engajamento",0))}</div><div class="kpi-l">{eng_lbl}</div></div>
    <div class="kpi"><div class="kpi-v" id="kpi-count">{metricas.get("total_posts",0)}</div><div class="kpi-l">Posts Analisados</div></div>
    <div class="kpi"><div class="kpi-v" style="font-size:1.1rem">{metricas.get("tipo_top","-")}</div><div class="kpi-l">Tipo mais postado</div></div>
  </div>
</div>

<div class="sec" id="sec-ev"{sec_ev_style}>
  <div class="sec-title">Evolucao ao Longo do Tempo</div>
  <div class="chart-row">
    <div><div id="c-seg"></div></div>
    <div><div id="c-eh"></div></div>
  </div>
</div>

<div class="sec">
  <div class="sec-title">Desempenho por Tipo de Post</div>
  <div class="tipos-grid">{tipo_cards}</div>
</div>

<div class="sec">
  <div class="sec-title">Melhores Dias para Postar</div>
  <div id="c-dias"></div>
</div>

<div class="sec">
  <div class="sec-title">Frequencia de Postagem</div>
  <div id="c-freq"></div>
  <div class="freq-insight" id="freq-insight"></div>
</div>

<div class="sec">
  <div class="sec-title">Top 3 Posts</div>
  <div class="top3-grid" id="top3-grid">{top3_html}</div>
</div>

<div class="sec">
  <div class="sec-title">Analise de Hashtags</div>
  <div id="hb-container"></div>
</div>

<div class="sec">
  <div class="sec-title">Tamanho do Texto vs Engajamento</div>
  <div class="tit-grid">{texto_html}</div>
</div>

<div class="sec">
  <div class="sec-title">Linha do Tempo</div>
  <div class="chart-row">
    <div><div id="c-tl"></div></div>
    <div><div id="c-tc"></div></div>
  </div>
  <div class="chart-row" style="margin-top:14px">
    <div><div id="c-ts"></div></div>
    <div><div id="c-te"></div></div>
  </div>
</div>

<div class="sec">
  <div class="sec-title">Filtrar Posts</div>
  <div class="filtros" id="ft">
    <button class="fb on" data-t="todos">Todos</button>
    <button class="fb" data-t="Texto">Texto</button>
    <button class="fb" data-t="Imagem">Imagem</button>
    <button class="fb" data-t="Video">Video</button>
    <button class="fb" data-t="Documento">Documento</button>
    <button class="fb" data-t="Artigo">Artigo</button>
    <button class="fb" data-t="Repost">Repost</button>
  </div>
  <div class="filtros" id="fp">
    <button class="fb on" data-p="0">Todos</button>
    <button class="fb" data-p="7">Ultimos 7 dias</button>
    <button class="fb" data-p="15">Ultimos 15 dias</button>
    <button class="fb" data-p="30">Ultimos 30 dias</button>
  </div>
</div>

<div class="sec">
  <div class="sec-title">Todos os Posts</div>
  <div class="pg" id="pg"></div>
</div>

</div>
<script>
const PD={posts_json};
const HL={hist_labels};const HS={hist_seg};const HE={hist_eng};
const TEM={tem_historico};
const SL={sem_labels};const SC={sem_counts};const SE={sem_eng};
const DL={dias_labels};const DE={dias_eng_data};
const TL={tl_labels};const TLk={tl_likes};const TC={tl_coments};const TS={tl_shares};const TE={tl_eng_js};
const TH={hashtags_json};
const CORES={cores_json};
const SEM_SEG={sem_seg_js};

function fmtN(n){{if(n>=1e6)return(n/1e6).toFixed(1)+'M';if(n>=1e3)return(n/1e3).toFixed(1)+'K';return String(n);}}
function fmtEng(v){{return SEM_SEG?String(Math.round(v)):v.toFixed(2)+'%';}}

(function(){{
  const c=document.getElementById('hb-container');
  if(!TH.length){{c.innerHTML='<p style="color:#a8a8a3;font-size:.83rem">Nenhuma hashtag encontrada.</p>';return;}}
  const mx=Math.max(...TH.map(h=>h.media_eng));
  c.innerHTML=TH.map(h=>{{
    const p=mx>0?(h.media_eng/mx*100).toFixed(1):0;
    return`<div class="hb"><span class="hb-name">${{h.tag}}</span><div class="hb-track"><div class="hb-fill" style="width:${{p}}%"></div></div><span class="hb-val">${{fmtEng(h.media_eng)}} (${{h.count}})</span></div>`;
  }}).join('');
}})();

let curT='todos',curP=0;

function renderGrade(posts){{
  const g=document.getElementById('pg');
  g.innerHTML=posts.map(p=>{{
    const cor=CORES[p.tipo]||'#c4ff5e';
    const th=p.thumbnail_b64
      ?`<img class="pt" src="${{p.thumbnail_b64}}" alt="">`
      :`<div class="pt-sem-img" style="--cc:${{CORES[p.tipo]||'#c4ff5e'}}"><span class="tc-quote">&ldquo;</span><span class="tc-txt">${{p.texto.substring(0,120)}}</span></div>`;
    const lk=p.url?`<a class="plink" href="${{p.url}}" target="_blank">Ver post</a>`:'';
    const tx=p.texto.length>120?p.texto.substring(0,120)+'...':p.texto;
    return`<div class="pc"><div class="pt-wrap">${{th}}<span class="pt-tipo" style="border-color:${{cor}};color:${{cor}}">${{p.tipo}}</span></div><div class="pi"><div class="ptxt">${{tx}}</div><div class="pm"><span>👍 ${{fmtN(p.likes)}}</span><span>💬 ${{fmtN(p.comentarios)}}</span><span>↗ ${{fmtN(p.shares)}}</span><span>${{fmtEng(p.engajamento)}}</span></div><div class="pm" style="margin-top:3px"><span>${{p.data_fmt}}</span></div>${{lk}}</div></div>`;
  }}).join('');
}}

function renderTop3(posts){{
  const el=document.getElementById('top3-grid');if(!el)return;
  const bCls=['badge-gold','badge-silver','badge-bronze'];
  const bTxt=['#1','#2','#3'];
  const top=[...posts].sort((a,b)=>b.engajamento-a.engajamento||b.likes-a.likes).slice(0,3);
  el.innerHTML=top.map((p,i)=>{{
    const cor=CORES[p.tipo]||'#c4ff5e';
    const th=p.thumbnail_b64?`<img class="top3-thumb" src="${{p.thumbnail_b64}}" alt="">`:`<div class="no-thumb" style="--cc:${{CORES[p.tipo]||'#c4ff5e'}}"><span class="tc-quote">"</span><span class="tc-txt">${{p.texto.substring(0,120)}}</span></div>`;
    const lk=p.url?`<a class="vlink" href="${{p.url}}" target="_blank">Ver post</a>`:'';
    const tx=p.texto.length>100?p.texto.substring(0,100)+'...':p.texto;
    return`<div class="top3-card">${{th}}<div class="top3-body"><span class="top3-badge ${{bCls[i]}}">${{bTxt[i]}}</span><span class="tipo-badge" style="border-color:${{cor}};color:${{cor}}">${{p.tipo}}</span><div class="top3-texto">${{tx}}</div><div class="top3-stats"><span><b>${{fmtN(p.likes)}}</b> likes</span><span><b>${{fmtN(p.comentarios)}}</b> coment.</span><span><b>${{fmtN(p.shares)}}</b> shares</span><span><b>${{fmtEng(p.engajamento)}}</b> eng.</span></div><div class="top3-data">${{p.data_fmt}}</div>${{lk}}</div></div>`;
  }}).join('');
}}

function filtrar(){{
  let posts=[...PD];
  if(curP>0){{const lim=Date.now()/1000-curP*86400;posts=posts.filter(p=>p.data>=lim);}}
  if(curT!=='todos'){{posts=posts.filter(p=>p.tipo===curT);}}
  renderGrade(posts);renderTop3(posts);
  if(posts.length){{
    const me=posts.reduce((s,p)=>s+p.engajamento,0)/posts.length;
    const ke=document.getElementById('kpi-eng');
    const kc=document.getElementById('kpi-count');
    if(ke)ke.textContent=fmtEng(me);
    if(kc)kc.textContent=posts.length;
  }}
  document.querySelectorAll('#ft .fb').forEach(b=>b.classList.toggle('on',b.dataset.t===curT));
  document.querySelectorAll('#fp .fb').forEach(b=>b.classList.toggle('on',parseInt(b.dataset.p)===curP));
}}

document.querySelectorAll('#ft .fb').forEach(b=>b.addEventListener('click',()=>{{curT=b.dataset.t;filtrar();}}));
document.querySelectorAll('#fp .fb').forEach(b=>b.addEventListener('click',()=>{{curP=parseInt(b.dataset.p);filtrar();}}));

(function(){{
  const el=document.getElementById('freq-insight');if(!el||!SC.length)return;
  const a3=SC.map((c,i)=>c>=3?SE[i]:null).filter(x=>x!==null);
  const ao=SC.map((c,i)=>c<3?SE[i]:null).filter(x=>x!==null);
  const avg=a=>a.length?(a.reduce((s,v)=>s+v,0)/a.length).toFixed(2):null;
  const v3=avg(a3),vo=avg(ao);
  const u=SEM_SEG?'interacoes medias':'% de engajamento medio';
  el.textContent=v3&&vo
    ?`Semanas com 3 ou mais posts tiveram ${{v3}} ${{u}}, contra ${{vo}} nas semanas com menos posts.`
    :v3?`Semanas com 3 ou mais posts: ${{v3}} ${{u}}.`
    :'Teste publicar 3 ou mais vezes por semana e observe o impacto no engajamento.';
}})();

window.addEventListener('DOMContentLoaded',()=>{{renderGrade(PD);renderTop3(PD);setTimeout(renderRechartsAll,100);}});
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

def atualizar_meta_concorrente(conc_dir: Path, slug: str, nome: str, plat: str, handle: str) -> None:
    """Cria ou atualiza meta.json com info do concorrente."""
    from datetime import datetime as _dt
    meta_path = conc_dir / "meta.json"
    meta: dict = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
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
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Dashboard - Workshop Marketing IA")
    parser.add_argument("--abrir", action="store_true", help="Abre o dashboard no navegador ao terminar")
    parser.add_argument("--perfil", help="URL ou handle do perfil LinkedIn (substitui LINKEDIN_PROFILE do .env)")
    parser.add_argument("--concorrente", help="Slug do concorrente. Salva em entregas/concorrentes/{slug}/linkedin/")
    parser.add_argument("--nome-bonito", dest="nome_bonito", help="Nome do concorrente para exibir no painel")
    args = parser.parse_args()

    env        = carregar_env()
    token      = env.get("APIFY_API_TOKEN", "")
    perfil_raw = args.perfil or env.get("LINKEDIN_PROFILE", "")

    if not token:
        print("ERRO: APIFY_API_TOKEN nao encontrado no .env")
        print("Configure em console.apify.com > Settings > Integrations > Personal API token")
        sys.exit(1)
    if not perfil_raw:
        print("ERRO: LINKEDIN_PROFILE nao encontrado no .env e nao foi passado via --perfil")
        print("Exemplo: python atualizar.py --perfil leandroladeira")
        sys.exit(1)

    perfil_url  = normalizar_url_perfil(perfil_raw)
    handle      = extrair_handle(perfil_url)
    handle_slug = re.sub(r"[^a-zA-Z0-9_-]", "", handle)[:50] or "perfil"

    # Se for meu perfil (nao concorrente) e handle for novo, salva no .env
    if not args.concorrente and handle and env.get("LINKEDIN_PROFILE", "") != handle:
        salvar_no_env("LINKEDIN_PROFILE", handle)

    # Resolver caminhos: meu vs concorrente
    # IMPORTANTE: para concorrente, computa o caminho ABSOLUTO a partir de raiz_projeto().
    # Nao usar .parent magic em cima de get_output_dir() (causou bug nos scripts irmaos onde
    # os arquivos foram pra leitura-10x/concorrentes/ em vez de leitura-10x/entregas/concorrentes/).
    if args.concorrente:
        raiz = raiz_projeto()
        ativo_path = raiz / "meus-produtos" / ".ativo"
        if not ativo_path.exists():
            print("ERRO: meus-produtos/.ativo nao encontrado."); sys.exit(1)
        ativo = ativo_path.read_text(encoding="utf-8").strip()
        if not ativo:
            print("ERRO: meus-produtos/.ativo esta vazio."); sys.exit(1)
        conc_root  = raiz / "meus-produtos" / ativo / "entregas" / "concorrentes" / args.concorrente
        output_dir = conc_root / "linkedin"
        base_dir   = output_dir
        # Sanity check: nunca deixar passar caminho fora de entregas/concorrentes
        assert "entregas" in output_dir.parts and "concorrentes" in output_dir.parts, \
            f"ERRO interno: caminho de concorrente invalido: {output_dir}"
    else:
        base_dir   = get_output_dir()
        output_dir = base_dir / handle_slug

    output_dir.mkdir(parents=True, exist_ok=True)
    log = configurar_log(output_dir)
    log.info(f"=== LinkedIn Dashboard iniciado para {perfil_url} ===")

    log.info("Buscando perfil e posts em paralelo...")
    perfil_raw_data: list = []
    posts_raw: list       = []

    def buscar_perfil_fn():
        # harvestapi~linkedin-profile-scraper usa o campo "queries" (URL ou handle)
        return chamar_apify(token, ATOR_PERFIL,
                            {"queries": [perfil_url]},
                            log, timeout=120, obrigatorio=False)

    def buscar_posts_fn():
        return chamar_apify(token, ATOR_POSTS,
                            {"profileUrls": [perfil_url], "maxPosts": MAX_POSTS},
                            log, timeout=TIMEOUT_SYNC, obrigatorio=True)

    with ThreadPoolExecutor(max_workers=2) as ex:
        fut_p = ex.submit(buscar_perfil_fn)
        fut_q = ex.submit(buscar_posts_fn)
        perfil_raw_data = fut_p.result()
        posts_raw       = fut_q.result()

    if not posts_raw:
        log.error("Nenhum post retornado. Verifique o handle e o token Apify.")
        sys.exit(1)

    log.info("Normalizando dados...")
    perfil = normalizar_perfil(perfil_raw_data, perfil_url)
    posts  = [normalizar_post(item) for item in posts_raw[:MAX_POSTS]]
    log.info(f"{len(posts)} posts coletados")

    # Fallback: extrai nome/headline/avatar a partir do autor dos posts que batem com o handle buscado
    if not perfil.get("nome"):
        for item in posts_raw:
            autor = item.get("author") or item.get("authorProfile") or {}
            if not isinstance(autor, dict):
                continue
            # Prioriza o autor cujo publicIdentifier bate com o handle
            pub_id = (autor.get("publicIdentifier") or "").lower().strip("/")
            if pub_id and pub_id != handle.lower():
                continue
            if autor.get("name") or autor.get("firstName"):
                nome_autor = autor.get("name") or f"{autor.get('firstName','')} {autor.get('lastName','')}".strip()
                perfil["nome"]     = nome_autor
                perfil["headline"] = perfil.get("headline") or autor.get("info") or autor.get("headline") or ""
                # avatar pode estar em autor.avatar.url (nested) ou como string direta
                av = autor.get("avatar") or autor.get("profilePicture") or autor.get("picture") or ""
                if isinstance(av, dict):
                    av = av.get("url") or av.get("src") or ""
                perfil["avatar_url"] = perfil.get("avatar_url") or av
                break

    log.info(f"Perfil: {perfil.get('nome') or handle} — {perfil.get('seguidores',0):,} seguidores")

    log.info("Baixando avatar...")
    perfil["avatar_b64"] = baixar_base64(perfil.get("avatar_url", ""), log, "avatar")

    log.info("Baixando imagens dos posts...")
    posts = baixar_thumbnails(posts, output_dir, log)
    checar_saude_dados(posts, perfil, log)

    log.info("Calculando metricas...")
    metricas = calcular_metricas(posts, perfil)
    _eng = metricas.get('media_engajamento', 0)
    _suf = "" if metricas.get("sem_seguidores") else "%"
    log.info(f"Engajamento medio: {_eng:.2f}{_suf}")

    historico = atualizar_historico(base_dir, perfil, metricas)
    log.info(f"Historico: {len(historico)} snapshots")

    salvar_insights(output_dir, perfil, posts, metricas)
    log.info("insights.json salvo")

    log.info("Gerando dashboard...")
    html_path = gerar_html(perfil, posts, metricas, historico, handle, output_dir, log)
    log.info(f"=== Pronto: {html_path} ===")

    if args.concorrente:
        atualizar_meta_concorrente(
            conc_root,
            args.concorrente,
            args.nome_bonito or args.concorrente,
            "linkedin",
            handle,
        )
        log.info(f"meta.json do concorrente atualizado: {conc_root}/meta.json")

    if args.abrir:
        webbrowser.open(html_path.as_uri())


if __name__ == "__main__":
    main()
