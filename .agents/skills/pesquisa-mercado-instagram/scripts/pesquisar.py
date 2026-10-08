#!/usr/bin/env python3
"""
Workshop Inteligente - Pesquisa de Nicho
Descobre perfis e conteudos de referencia do nicho via Apify Instagram Scraper.
Gera dashboard HTML com ranking de perfis, analise de conteudo e mapa de hashtags.
"""

import os
import sys
import json
import base64
import time
import argparse
import logging
import webbrowser
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

try:
    import requests
except ImportError:
    print("Erro: biblioteca 'requests' nao encontrada.")
    print("Instale com: pip install requests")
    sys.exit(1)

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

# ── Raiz do projeto ──────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent

def encontrar_raiz():
    p = SCRIPT_DIR
    for _ in range(10):
        if (p / '.env').exists():
            return p
        p = p.parent
    return SCRIPT_DIR

PROJECT_ROOT = encontrar_raiz()
ENV_FILE = PROJECT_ROOT / '.env'

def get_output_dir() -> Path:
    ativo_file = PROJECT_ROOT / 'meus-produtos' / '.ativo'
    if not ativo_file.exists():
        log.error('meus-produtos/.ativo nao encontrado.')
        sys.exit(1)
    ativo = ativo_file.read_text(encoding='utf-8').strip()
    if not ativo:
        log.error('meus-produtos/.ativo esta vazio.')
        sys.exit(1)
    output = PROJECT_ROOT / 'meus-produtos' / ativo / 'entregas' / 'pesquisa-nicho'
    output.mkdir(parents=True, exist_ok=True)
    return output

# ── .env parser ──────────────────────────────────────────────────────────────
def ler_env():
    env = {}
    if ENV_FILE.exists():
        for linha in ENV_FILE.read_text(encoding='utf-8').splitlines():
            linha = linha.strip()
            if linha and not linha.startswith('#') and '=' in linha:
                k, _, v = linha.partition('=')
                env[k.strip()] = v.strip()
    env.update({k: v for k, v in os.environ.items()})
    return env

# ── Apify ────────────────────────────────────────────────────────────────────
SCRAPER_URL = 'https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items'

def apify_post(token, payload, timeout=120, retries=3):
    url = f'{SCRAPER_URL}?token={token}&timeout={timeout}'
    for tentativa in range(1, retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=timeout + 60)
            if resp.status_code in (200, 201):
                return resp.json()
            if 400 <= resp.status_code < 500:
                body = resp.json() if resp.headers.get('content-type', '').startswith('application/json') else {}
                err = body.get('error', {})
                if err.get('message', '').startswith('Actor run did not succeed'):
                    log.warning(f'  Apify actor timeout (tentativa {tentativa}/{retries})')
                else:
                    log.warning(f'  Apify erro {resp.status_code} (tentativa {tentativa}/{retries}): {resp.text[:200]}')
            else:
                resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            log.warning(f'  Apify erro HTTP (tentativa {tentativa}/{retries}): {e}')
        except Exception as e:
            log.warning(f'  Apify erro (tentativa {tentativa}/{retries}): {e}')
        if tentativa < retries:
            espera = tentativa * 10
            log.info(f'  Aguardando {espera}s antes de tentar novamente...')
            time.sleep(espera)
    return []

# ── Etapa 1: Buscar posts por hashtags ───────────────────────────────────────
def buscar_hashtags(token, hashtags, limite_por_hashtag=50):
    """Busca posts de cada hashtag e retorna lista de posts com ownerUsername."""
    todos_posts = []
    for tag in hashtags:
        tag_clean = tag.strip().lstrip('#').lower()
        if not tag_clean:
            continue
        log.info(f'  Buscando #{tag_clean}...')
        url_tag = f'https://www.instagram.com/explore/tags/{tag_clean}/'
        data = apify_post(token, {
            'directUrls': [url_tag],
            'resultsType': 'posts',
            'resultsLimit': limite_por_hashtag,
        }, timeout=180)
        if data:
            for p in data:
                p['_hashtag_fonte'] = tag_clean
            todos_posts.extend(data)
            log.info(f'    {len(data)} posts encontrados')
        else:
            log.warning(f'    Nenhum post retornado para #{tag_clean}')
        time.sleep(3)  # respeitar rate limit
    return todos_posts

# ── Etapa 2: Extrair perfis unicos e enriquecer ─────────────────────────────
def extrair_perfis_unicos(posts_br, posts_mundo):
    """Extrai usernames unicos dos posts, marcando origem (BR/mundo)."""
    perfis = {}
    for p in posts_br:
        owner = p.get('ownerUsername', '')
        if owner and owner not in perfis:
            perfis[owner] = {'username': owner, 'origem': 'BR'}
    for p in posts_mundo:
        owner = p.get('ownerUsername', '')
        if owner and owner not in perfis:
            perfis[owner] = {'username': owner, 'origem': 'Mundo'}
    return perfis

def enriquecer_perfis(token, perfis_dict, batch_size=20):
    """Busca detalhes dos perfis em batch."""
    usernames = list(perfis_dict.keys())
    log.info(f'Enriquecendo {len(usernames)} perfis em batches de {batch_size}...')
    resultados = []
    for i in range(0, len(usernames), batch_size):
        batch = usernames[i:i + batch_size]
        log.info(f'  Batch {i // batch_size + 1}/{(len(usernames) - 1) // batch_size + 1} ({len(batch)} perfis)')
        urls = [f'https://www.instagram.com/{u}/' for u in batch]
        data = apify_post(token, {
            'directUrls': urls,
            'resultsType': 'details',
        }, timeout=180)
        if data:
            for p in data:
                username = p.get('username', '')
                if username and username in perfis_dict:
                    p['_origem'] = perfis_dict[username]['origem']
                resultados.append(p)
        time.sleep(3)
    return resultados

# ── Etapa 3: Buscar posts dos top perfis ─────────────────────────────────────
def buscar_posts_top_perfis(token, top_perfis, limite=30):
    """Busca posts recentes dos top perfis para analise de conteudo."""
    todos = {}
    for i, perfil in enumerate(top_perfis):
        username = perfil.get('username', '')
        log.info(f'  Buscando posts de @{username} ({i + 1}/{len(top_perfis)})...')
        data = apify_post(token, {
            'directUrls': [f'https://www.instagram.com/{username}/'],
            'resultsType': 'posts',
            'resultsLimit': limite,
        }, timeout=300)
        if data:
            todos[username] = data
            log.info(f'    {len(data)} posts')
        else:
            log.warning(f'    Nenhum post retornado')
        time.sleep(3)
    return todos

# ── Etapa 4: Baixar imagens ──────────────────────────────────────────────────
def baixar_b64(url, desc=''):
    if not url:
        return ''
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.instagram.com/',
        }
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200 and len(resp.content) > 500:
            return base64.b64encode(resp.content).decode('ascii')
    except Exception:
        pass
    return ''

def baixar_fotos_perfis(perfis, images_dir):
    """Baixa fotos de perfil em paralelo."""
    log.info(f'Baixando fotos de {len(perfis)} perfis...')
    def _baixar(perfil):
        username = perfil.get('username', '')
        pic_url = perfil.get('profilePicUrl', '') or perfil.get('profilePicUrlHD', '')
        b64 = baixar_b64(pic_url, f'foto @{username}')
        if b64:
            img_path = images_dir / f'{username}.jpg'
            img_path.write_bytes(base64.b64decode(b64))
            return username, b64, str(img_path.relative_to(images_dir.parent))
        return username, '', ''

    resultados = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(_baixar, p): p for p in perfis}
        for f in as_completed(futures):
            username, b64, path = f.result()
            resultados[username] = {'b64': b64, 'path': path}
    return resultados

# ── Etapa 5: Calcular metricas e rankings ────────────────────────────────────
def normalizar_perfil(raw, origem, foto_info):
    username = raw.get('username', '')
    seguidores = raw.get('followersCount', 0) or 0
    seguindo = raw.get('followsCount', 0) or 0
    posts_count = raw.get('postsCount', 0) or 0
    return {
        'username':    username,
        'nome':        raw.get('fullName', '') or username,
        'bio':         (raw.get('biography', '') or '')[:300],
        'seguidores':  seguidores,
        'seguindo':    seguindo,
        'totalPosts':  posts_count,
        'verificado':  raw.get('verified', False),
        'origem':      origem,
        'fotoB64':     foto_info.get('b64', ''),
        'fotoPath':    foto_info.get('path', ''),
        'url':         f'https://www.instagram.com/{username}/',
    }

def calcular_metricas_perfil(perfil, posts_raw):
    """Calcula engajamento medio e distribuicao de formato para um perfil."""
    seg = perfil['seguidores'] or 1
    posts = []
    tipos = defaultdict(int)
    total_likes = 0
    total_comments = 0
    total_views = 0
    hashtags_set = set()

    for p in posts_raw:
        likes = p.get('likesCount', 0) or 0
        if likes < 0:
            likes = 0
        comments = p.get('commentsCount', 0) or 0
        views = p.get('videoPlayCount', 0) or p.get('videoViewCount', 0) or 0
        tipo_raw = p.get('type', 'Image')
        tipo = 'Reel' if tipo_raw == 'Video' else ('Carrossel' if tipo_raw == 'Sidecar' else 'Foto')
        eng = round((likes + comments) / seg * 100, 2)

        tipos[tipo] += 1
        total_likes += likes
        total_comments += comments
        total_views += views

        for tag in (p.get('hashtags', []) or []):
            hashtags_set.add(tag.lower().strip())

        sc = p.get('shortCode') or p.get('shortcode', '')
        url_post = f'https://www.instagram.com/p/{sc}/' if sc else p.get('url', '')
        posts.append({
            'shortCode': sc,
            'tipo': tipo,
            'likes': likes,
            'comentarios': comments,
            'views': views,
            'engajamento': eng,
            'timestamp': p.get('timestamp', ''),
            'legenda': (p.get('caption', '') or '')[:300],
            'hashtags': p.get('hashtags', []),
            'url': url_post,
            'transcricao': '',
        })

    n = len(posts) or 1
    eng_medio = round(sum(p['engajamento'] for p in posts) / n, 2)
    formato_top = max(tipos, key=tipos.get) if tipos else '-'

    return {
        'engMedio': eng_medio,
        'mediaLikes': round(total_likes / n),
        'mediaComentarios': round(total_comments / n),
        'totalViews': total_views,
        'formatoTop': formato_top,
        'distribuicao': dict(tipos),
        'hashtags': list(hashtags_set)[:50],
        'posts': posts,
        'totalPosts': len(posts),
    }

def analisar_conteudo_global(perfis_com_metricas):
    """Analisa padroes de conteudo entre todos os perfis."""
    formatos = defaultdict(lambda: {'count': 0, 'totalEng': 0})
    hashtags_global = defaultdict(lambda: {'count': 0, 'totalEng': 0})
    horarios = defaultdict(lambda: {'count': 0, 'totalEng': 0})

    for pm in perfis_com_metricas:
        for post in pm.get('metricas', {}).get('posts', []):
            # Formato
            tipo = post['tipo']
            formatos[tipo]['count'] += 1
            formatos[tipo]['totalEng'] += post['engajamento']

            # Hashtags
            for tag in post.get('hashtags', []):
                t = tag.lower().strip()
                if t:
                    hashtags_global[t]['count'] += 1
                    hashtags_global[t]['totalEng'] += post['engajamento']

            # Horarios
            ts = post.get('timestamp', '')
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    dia = (dt.weekday())  # 0=seg
                    hora = dt.hour
                    key = f'{dia}-{hora}'
                    horarios[key]['count'] += 1
                    horarios[key]['totalEng'] += post['engajamento']
                except Exception:
                    pass

    # Formato: media de engajamento por tipo
    formato_analise = {}
    for tipo, dados in formatos.items():
        n = dados['count'] or 1
        formato_analise[tipo] = {
            'count': dados['count'],
            'engMedio': round(dados['totalEng'] / n, 2),
        }

    # Top hashtags por engajamento medio (minimo 3 ocorrencias)
    top_hashtags = []
    for tag, dados in hashtags_global.items():
        if dados['count'] >= 3:
            top_hashtags.append({
                'tag': f'#{tag}',
                'count': dados['count'],
                'engMedio': round(dados['totalEng'] / dados['count'], 2),
            })
    top_hashtags.sort(key=lambda x: x['engMedio'], reverse=True)

    # Heatmap horarios
    heatmap = {}
    for key, dados in horarios.items():
        heatmap[key] = {
            'count': dados['count'],
            'engMedio': round(dados['totalEng'] / dados['count'], 2) if dados['count'] else 0,
        }

    return {
        'formatos': formato_analise,
        'topHashtags': top_hashtags[:20],
        'heatmap': heatmap,
    }

# ── Dashboard HTML ───────────────────────────────────────────────────────────
def gerar_html(pesquisa_data):
    dados_js = json.dumps(pesquisa_data, ensure_ascii=False, default=str)
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pesquisa de Nicho</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#f8fafc;--card:#fff;--border:#e2e8f0;--text:#1e293b;--muted:#64748b;
  --accent:#4338ca;--accent-lt:#eef2ff;
  --br:#059669;--mundo:#0369a1;
  --reel:#7c3aed;--carrossel:#0369a1;--foto:#059669;
  --sh:0 1px 3px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.04);
  --sh-md:0 4px 6px -1px rgba(0,0,0,.07);
  --r:12px;--r-sm:8px
}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text)}}
.wrap{{max-width:1200px;margin:0 auto;padding:24px 16px}}
.hdr{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:24px;margin-bottom:24px;box-shadow:var(--sh)}}
.hdr h1{{font-size:22px;font-weight:700;margin-bottom:4px}}
.hdr .sub{{color:var(--muted);font-size:13px}}
.kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}}
.kpi{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;box-shadow:var(--sh)}}
.kpi-lbl{{font-size:11px;font-weight:500;color:var(--muted);text-transform:uppercase;letter-spacing:.5px}}
.kpi-val{{font-size:28px;font-weight:700;margin-top:4px}}
.kpi-sub{{font-size:12px;color:var(--muted);margin-top:2px}}
.kpi-accent .kpi-val{{color:var(--accent)}}
.sec{{font-size:16px;font-weight:700;margin-bottom:16px}}
.sec-sub{{font-size:13px;color:var(--muted);margin-bottom:16px;margin-top:-8px}}
.perfil-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-bottom:32px}}
.perfil-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:12px}}
.perfil-top{{display:flex;align-items:center;gap:12px}}
.perfil-avatar{{width:48px;height:48px;border-radius:50%;border:2px solid var(--accent);flex-shrink:0;background:var(--accent-lt);display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;color:var(--accent);overflow:hidden}}
.perfil-avatar img{{width:100%;height:100%;object-fit:cover}}
.perfil-info h3{{font-size:14px;font-weight:700}}
.perfil-info .un{{color:var(--accent);font-size:12px;font-weight:500}}
.perfil-bio{{font-size:12px;color:var(--muted);line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.perfil-stats{{display:flex;gap:12px;flex-wrap:wrap}}
.perfil-stat-lbl{{font-size:10px;color:var(--muted);text-transform:uppercase}}
.perfil-stat-val{{font-size:16px;font-weight:700}}
.perfil-link{{font-size:12px;color:var(--accent);text-decoration:none;font-weight:500}}
.perfil-link:hover{{text-decoration:underline}}
.badge-origem{{display:inline-block;padding:2px 8px;border-radius:99px;font-size:10px;font-weight:600}}
.badge-br{{background:#d1fae5;color:var(--br)}}
.badge-mundo{{background:#e0f2fe;color:var(--mundo)}}
.badge-verified{{display:inline-block;padding:2px 8px;border-radius:99px;font-size:10px;font-weight:600;background:var(--accent-lt);color:var(--accent);margin-left:4px}}
.fmt-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px}}
.fmt-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;box-shadow:var(--sh);text-align:center}}
.fmt-nome{{font-size:14px;font-weight:700;margin-bottom:8px;display:flex;align-items:center;justify-content:center;gap:8px}}
.dot{{width:10px;height:10px;border-radius:50%}}
.dot-r{{background:var(--reel)}}.dot-c{{background:var(--carrossel)}}.dot-f{{background:var(--foto)}}
.met-lbl{{font-size:11px;color:var(--muted)}}
.met-val{{font-size:22px;font-weight:700}}
.hash-wrap{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:24px;box-shadow:var(--sh)}}
.hash-row{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}
.hash-tag{{font-size:12px;font-weight:600;min-width:140px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.hash-bar-wrap{{flex:1;height:20px;background:var(--accent-lt);border-radius:4px;overflow:hidden}}
.hash-bar{{height:100%;background:var(--accent);border-radius:4px;transition:width .3s}}
.hash-stat{{font-size:11px;color:var(--muted);white-space:nowrap;min-width:110px}}
.heatmap-wrap{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:24px;box-shadow:var(--sh);overflow-x:auto}}
.heatmap{{display:grid;grid-template-columns:40px repeat(24,1fr);gap:2px}}
.hm-cell{{aspect-ratio:1;border-radius:3px;position:relative;cursor:pointer;min-width:14px}}
.hm-cell:hover .hm-tip{{display:block}}
.hm-lbl{{font-size:9px;color:var(--muted);display:flex;align-items:center;justify-content:center}}
.hm-tip{{display:none;position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);background:#1e293b;color:#fff;padding:5px 8px;border-radius:6px;font-size:11px;white-space:nowrap;z-index:10;pointer-events:none}}
.filter-bar{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;align-items:center}}
.filter-group{{display:flex;gap:4px;align-items:center}}
.filter-group-lbl{{font-size:11px;color:var(--muted);font-weight:600;margin-right:4px;text-transform:uppercase;letter-spacing:.5px}}
.fbtn{{padding:5px 14px;border-radius:99px;border:1px solid var(--border);background:var(--card);font-size:12px;font-weight:500;cursor:pointer;transition:all .15s;font-family:inherit;color:var(--text)}}
.fbtn:hover{{border-color:var(--accent);color:var(--accent)}}
.fbtn.active{{background:var(--accent);color:#fff;border-color:var(--accent)}}
.all-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-bottom:24px}}
.all-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r-sm);padding:14px;box-shadow:var(--sh);display:flex;align-items:center;gap:10px}}
.all-avatar{{width:36px;height:36px;border-radius:50%;background:var(--accent-lt);display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:var(--accent);overflow:hidden;flex-shrink:0}}
.all-avatar img{{width:100%;height:100%;object-fit:cover}}
.all-info{{flex:1;min-width:0}}
.all-info h4{{font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.all-info .all-meta{{font-size:11px;color:var(--muted)}}
.tp-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-bottom:24px}}
.tp-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;box-shadow:var(--sh)}}
.tp-rank{{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:var(--accent);color:#fff;font-size:12px;font-weight:700;margin-bottom:10px}}
.tp-owner{{font-size:12px;color:var(--accent);font-weight:500;margin-bottom:8px}}
.tp-leg{{font-size:13px;color:var(--text);line-height:1.5;margin-bottom:10px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}
.tp-stats{{display:flex;gap:12px;flex-wrap:wrap;font-size:12px}}
.tp-stat-val{{font-weight:700}}
.tp-eng{{font-size:14px;font-weight:700;color:var(--accent);margin-bottom:6px}}
.tp-link{{font-size:12px;color:var(--accent);text-decoration:none;font-weight:500;margin-top:8px;display:inline-block}}
.tp-link:hover{{text-decoration:underline}}
.badge{{display:inline-block;padding:2px 8px;border-radius:99px;font-size:11px;font-weight:600;margin-right:6px}}
.br{{background:#f3e8ff;color:var(--reel)}}.bc{{background:#e0f2fe;color:var(--carrossel)}}.bf{{background:#d1fae5;color:var(--foto)}}
@media(max-width:768px){{
  .kpi-grid{{grid-template-columns:repeat(2,1fr)}}
  .fmt-grid{{grid-template-columns:1fr}}
  .perfil-grid{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<div class="wrap">
  <div id="app"></div>
</div>
<script>
const D={dados_js};

function fmt(n){{
  if(n===undefined||n===null||n<0)return'--';
  if(n>=1e6)return(n/1e6).toFixed(1)+'M';
  if(n>=1000)return(n/1000).toFixed(1)+'k';
  return n.toLocaleString('pt-BR');
}}

function render(){{
  const perfis=D.perfis||[];
  const analise=D.analise||{{}};
  const config=D.config||{{}};
  const perfisBR=perfis.filter(p=>p.origem==='BR').sort((a,b)=>b.seguidores-a.seguidores);
  const perfisMundo=perfis.filter(p=>p.origem==='Mundo').sort((a,b)=>b.seguidores-a.seguidores);
  const todos=perfis.slice().sort((a,b)=>b.seguidores-a.seguidores);

  const totalPerfis=perfis.length;
  const mediaSeguidores=totalPerfis?Math.round(perfis.reduce((s,p)=>s+p.seguidores,0)/totalPerfis):0;
  const mediaEng=totalPerfis?Math.round(perfis.reduce((s,p)=>s+(p.engMedio||0),0)/totalPerfis*100)/100:0;
  const verificados=perfis.filter(p=>p.verificado).length;

  const app=document.getElementById('app');
  app.innerHTML=`
  <div class="hdr">
    <h1>Pesquisa de Nicho</h1>
    <div class="sub">Hashtags BR: ${{(config.hashtagsBR||[]).map(h=>'#'+h).join(', ')}} | Mundo: ${{(config.hashtagsMundo||[]).map(h=>'#'+h).join(', ')}}</div>
    <div class="sub">Atualizado em: ${{D.atualizadoEm||'--'}}</div>
  </div>

  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-lbl">Perfis descobertos</div><div class="kpi-val">${{fmt(totalPerfis)}}</div><div class="kpi-sub">${{perfisBR.length}} BR, ${{perfisMundo.length}} mundo</div></div>
    <div class="kpi kpi-accent"><div class="kpi-lbl">Media de seguidores</div><div class="kpi-val">${{fmt(mediaSeguidores)}}</div><div class="kpi-sub">entre os perfis analisados</div></div>
    <div class="kpi"><div class="kpi-lbl">Engajamento medio</div><div class="kpi-val">${{mediaEng}}%</div><div class="kpi-sub">media geral do nicho</div></div>
    <div class="kpi"><div class="kpi-lbl">Verificados</div><div class="kpi-val">${{verificados}}</div><div class="kpi-sub">perfis com selo</div></div>
  </div>

  ${{perfisBR.length?`
  <div class="sec">Top Perfis Brasil (${{perfisBR.length}})</div>
  <div class="perfil-grid">${{perfisBR.slice(0,12).map(p=>perfilCard(p)).join('')}}</div>
  `:''}}

  ${{perfisMundo.length?`
  <div class="sec">Top Perfis Mundo (${{perfisMundo.length}})</div>
  <div class="perfil-grid">${{perfisMundo.slice(0,12).map(p=>perfilCard(p)).join('')}}</div>
  `:''}}

  <div id="formatoSection"></div>
  <div id="hashtagSection"></div>
  <div id="heatmapSection"></div>
  <div id="topPostsSection"></div>

  <div class="sec">Todos os Perfis (${{todos.length}})</div>
  <div id="filterBar"></div>
  <div class="all-grid" id="allGrid">${{todos.map(p=>allCard(p)).join('')}}</div>
  `;

  renderFormatos(analise.formatos||{{}});
  renderHashtags(analise.topHashtags||[]);
  renderHeatmap(analise.heatmap||{{}});
  renderTopPosts();
  renderFilters(todos);
}}

function perfilCard(p){{
  const foto=p.fotoB64?`<img src="data:image/jpeg;base64,${{p.fotoB64}}">`:(p.nome||p.username).charAt(0).toUpperCase();
  const badge=p.origem==='BR'?'<span class="badge-origem badge-br">BR</span>':'<span class="badge-origem badge-mundo">Mundo</span>';
  const verified=p.verificado?'<span class="badge-verified">Verificado</span>':'';
  return`<div class="perfil-card">
    <div class="perfil-top">
      <div class="perfil-avatar">${{foto}}</div>
      <div class="perfil-info">
        <h3>${{p.nome||p.username}} ${{badge}}${{verified}}</h3>
        <div class="un">@${{p.username}}</div>
      </div>
    </div>
    <div class="perfil-bio">${{p.bio||''}}</div>
    <div class="perfil-stats">
      <div><div class="perfil-stat-lbl">Seguidores</div><div class="perfil-stat-val">${{fmt(p.seguidores)}}</div></div>
      <div><div class="perfil-stat-lbl">Engajamento</div><div class="perfil-stat-val">${{p.engMedio||0}}%</div></div>
      <div><div class="perfil-stat-lbl">Formato top</div><div class="perfil-stat-val">${{p.formatoTop||'-'}}</div></div>
    </div>
    <a class="perfil-link" href="${{p.url}}" target="_blank" rel="noopener">Ver perfil no Instagram</a>
  </div>`;
}}

function allCard(p){{
  const foto=p.fotoB64?`<img src="data:image/jpeg;base64,${{p.fotoB64}}">`:(p.nome||p.username).charAt(0).toUpperCase();
  const badge=p.origem==='BR'?'<span class="badge-origem badge-br">BR</span>':'<span class="badge-origem badge-mundo">Mundo</span>';
  return`<a class="all-card" href="${{p.url}}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit" data-origem="${{p.origem}}">
    <div class="all-avatar">${{foto}}</div>
    <div class="all-info">
      <h4>@${{p.username}} ${{badge}}</h4>
      <div class="all-meta">${{fmt(p.seguidores)}} seg | ${{p.engMedio||0}}% eng</div>
    </div>
  </a>`;
}}

function renderFormatos(formatos){{
  const el=document.getElementById('formatoSection');
  if(!el)return;
  const tipos=['Reel','Carrossel','Foto'];
  const cards=tipos.map(t=>{{
    const d=formatos[t]||{{count:0,engMedio:0}};
    const dotClass=t==='Reel'?'dot-r':t==='Carrossel'?'dot-c':'dot-f';
    return`<div class="fmt-card">
      <div class="fmt-nome"><span class="dot ${{dotClass}}"></span>${{t}} (${{d.count}})</div>
      <div class="met-lbl">Engajamento medio</div>
      <div class="met-val">${{d.engMedio}}%</div>
    </div>`;
  }}).join('');
  el.innerHTML=`<div class="sec">Desempenho por Formato</div><div class="fmt-grid">${{cards}}</div>`;
}}

function renderHashtags(topHashtags){{
  const el=document.getElementById('hashtagSection');
  if(!el||!topHashtags.length)return;
  const maxEng=topHashtags[0].engMedio||1;
  const rows=topHashtags.slice(0,15).map(t=>{{
    const pct=Math.round(t.engMedio/maxEng*100);
    return`<div class="hash-row"><div class="hash-tag">${{t.tag}}</div><div class="hash-bar-wrap"><div class="hash-bar" style="width:${{pct}}%"></div></div><div class="hash-stat">${{t.engMedio}}% eng, ${{t.count}} posts</div></div>`;
  }}).join('');
  el.innerHTML=`<div class="hash-wrap"><div class="sec" style="margin-bottom:12px">Top Hashtags do Nicho</div>${{rows}}</div>`;
}}

function renderHeatmap(heatmap){{
  const el=document.getElementById('heatmapSection');
  if(!el||!Object.keys(heatmap).length)return;
  const dias=['Seg','Ter','Qua','Qui','Sex','Sab','Dom'];
  let maxAvg=0;
  Object.values(heatmap).forEach(c=>{{if(c.engMedio>maxAvg)maxAvg=c.engMedio}});
  if(!maxAvg)maxAvg=1;
  let html='<div class="sec">Melhores Horarios para Postar</div><div class="heatmap-wrap"><div class="heatmap">';
  html+='<div class="hm-lbl"></div>';
  for(let h=0;h<24;h++)html+=`<div class="hm-lbl">${{h}}</div>`;
  for(let d=0;d<7;d++){{
    html+=`<div class="hm-lbl">${{dias[d]}}</div>`;
    for(let h=0;h<24;h++){{
      const key=d+'-'+h;
      const cell=heatmap[key];
      if(!cell||!cell.count){{
        html+=`<div class="hm-cell" style="background:var(--accent-lt)"><div class="hm-tip">Nenhum post</div></div>`;
      }}else{{
        const opacity=Math.max(0.15,cell.engMedio/maxAvg);
        html+=`<div class="hm-cell" style="background:rgba(67,56,202,${{opacity.toFixed(2)}})"><div class="hm-tip">${{cell.count}} posts | ${{cell.engMedio}}% eng</div></div>`;
      }}
    }}
  }}
  html+='</div></div>';
  el.innerHTML=html;
}}

function renderTopPosts(){{
  const el=document.getElementById('topPostsSection');
  if(!el)return;
  const tp=D.topPosts||[];
  if(!tp.length)return;
  function bc(tipo){{return tipo==='Reel'?'br':tipo==='Carrossel'?'bc':'bf'}}
  const cards=tp.map((p,i)=>{{
    const leg=(p.legenda||'').substring(0,200);
    return`<div class="tp-card">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
        <div class="tp-rank">${{i+1}}</div>
        <div>
          <div class="tp-owner">@${{p.ownerUsername||'?'}} (${{fmt(p.ownerSeguidores||0)}} seg)</div>
          <span class="badge ${{bc(p.tipo)}}">${{p.tipo}}</span>
          <span style="font-size:11px;color:var(--muted)">${{p.origem||''}}</span>
        </div>
      </div>
      <div class="tp-eng">${{p.engajamento||0}}% engajamento</div>
      <div class="tp-stats">
        <span><span class="tp-stat-val">${{fmt(p.likes)}}</span> likes</span>
        <span><span class="tp-stat-val">${{fmt(p.comentarios)}}</span> com.</span>
        ${{p.tipo==='Reel'?`<span><span class="tp-stat-val">${{fmt(p.views)}}</span> views</span>`:''}}
      </div>
      ${{leg?`<div class="tp-leg">${{leg}}</div>`:''}}
      ${{p.url?`<a class="tp-link" href="${{p.url}}" target="_blank" rel="noopener">Ver post original</a>`:''}}
    </div>`;
  }}).join('');
  el.innerHTML=`<div class="sec">Top 10 Posts do Nicho (por engajamento)</div><div class="sec-sub">Posts com maior engajamento entre todos os perfis analisados</div><div class="tp-grid">${{cards}}</div>`;
}}

let filterOrigem='all';
function renderFilters(todos){{
  const el=document.getElementById('filterBar');
  if(!el)return;
  el.innerHTML=`<div class="filter-bar">
    <div class="filter-group">
      <span class="filter-group-lbl">Origem</span>
      <button class="fbtn ${{filterOrigem==='all'?'active':''}}" data-fo="all">Todos</button>
      <button class="fbtn ${{filterOrigem==='BR'?'active':''}}" data-fo="BR">Brasil</button>
      <button class="fbtn ${{filterOrigem==='Mundo'?'active':''}}" data-fo="Mundo">Mundo</button>
    </div>
  </div>`;
  el.querySelectorAll('[data-fo]').forEach(btn=>btn.addEventListener('click',()=>{{
    filterOrigem=btn.getAttribute('data-fo');
    const grid=document.getElementById('allGrid');
    grid.querySelectorAll('.all-card').forEach(card=>{{
      const origem=card.getAttribute('data-origem');
      card.style.display=(filterOrigem==='all'||origem===filterOrigem)?'':'none';
    }});
    el.querySelectorAll('[data-fo]').forEach(b=>b.classList.toggle('active',b.getAttribute('data-fo')===filterOrigem));
  }}));
}}

window.addEventListener('load',render);
</script>
</body>
</html>'''

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Pesquisa de Nicho via Instagram')
    parser.add_argument('--abrir', action='store_true', help='Abrir dashboard no navegador')
    parser.add_argument('--config', type=str, help='Caminho para config.json com hashtags')
    args = parser.parse_args()

    base_dir = get_output_dir()
    env = ler_env()
    token = env.get('APIFY_API_TOKEN', '')

    if not token:
        log.error('APIFY_API_TOKEN nao encontrado no .env')
        sys.exit(1)

    # Ler config
    config_file = Path(args.config) if args.config else base_dir / 'config.json'
    if not config_file.exists():
        log.error(f'Arquivo de configuracao nao encontrado: {config_file}')
        log.error('Crie o config.json com hashtagsBR e hashtagsMundo.')
        sys.exit(1)

    config = json.loads(config_file.read_text(encoding='utf-8'))
    hashtags_br = config.get('hashtagsBR', [])
    hashtags_mundo = config.get('hashtagsMundo', [])
    slug = config.get('slug', 'geral')
    perfis_semente = config.get('perfisSemente', [])

    # Subpasta por slug do nicho
    output_dir = base_dir / slug
    images_dir = output_dir / 'imagens'
    images_dir.mkdir(parents=True, exist_ok=True)

    log_file = output_dir / 'log.txt'
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logging.getLogger().addHandler(file_handler)

    log.info('=== Iniciando pesquisa de nicho ===')
    log.info(f'Hashtags BR: {hashtags_br}')
    log.info(f'Hashtags Mundo: {hashtags_mundo}')
    log.info(f'Perfis semente: {perfis_semente}')
    log.info(f'Output: {output_dir}')

    # Etapa 1: Buscar posts por hashtags
    log.info('--- Etapa 1: Buscando posts por hashtags ---')
    posts_br = []
    posts_mundo = []
    if hashtags_br:
        log.info(f'Hashtags BR ({len(hashtags_br)}):')
        posts_br = buscar_hashtags(token, hashtags_br, limite_por_hashtag=50)
    if hashtags_mundo:
        log.info(f'Hashtags Mundo ({len(hashtags_mundo)}):')
        posts_mundo = buscar_hashtags(token, hashtags_mundo, limite_por_hashtag=50)

    log.info(f'Total posts BR: {len(posts_br)}, Mundo: {len(posts_mundo)}')

    # Etapa 2: Extrair e enriquecer perfis
    log.info('--- Etapa 2: Extraindo e enriquecendo perfis ---')
    perfis_dict = extrair_perfis_unicos(posts_br, posts_mundo)

    # Adicionar perfis semente
    for ps in perfis_semente:
        ps_clean = ps.strip().lstrip('@').lower()
        if ps_clean and ps_clean not in perfis_dict:
            perfis_dict[ps_clean] = {'username': ps_clean, 'origem': 'BR'}

    log.info(f'Perfis unicos encontrados: {len(perfis_dict)}')
    perfis_raw = enriquecer_perfis(token, perfis_dict)
    log.info(f'Perfis enriquecidos: {len(perfis_raw)}')

    # Baixar fotos de perfil
    fotos = baixar_fotos_perfis(perfis_raw, images_dir)

    # Filtrar perfis com minimo de seguidores
    min_seguidores = config.get('minSeguidores', 1000)
    perfis_filtrados = [p for p in perfis_raw if (p.get('followersCount', 0) or 0) >= min_seguidores]
    log.info(f'Perfis com {min_seguidores}+ seguidores: {len(perfis_filtrados)}')

    # Etapa 3: Buscar posts dos top perfis
    log.info('--- Etapa 3: Buscando posts dos top perfis ---')
    top_por_seguidores = sorted(perfis_filtrados, key=lambda p: p.get('followersCount', 0) or 0, reverse=True)[:15]
    posts_por_perfil = buscar_posts_top_perfis(token, top_por_seguidores, limite=30)

    # Etapa 4: Calcular metricas
    log.info('--- Etapa 4: Calculando metricas ---')
    perfis_finais = []
    for raw in perfis_filtrados:
        username = raw.get('username', '')
        origem = raw.get('_origem', 'BR')
        foto_info = fotos.get(username, {'b64': '', 'path': ''})
        perfil = normalizar_perfil(raw, origem, foto_info)

        posts_do_perfil = posts_por_perfil.get(username, [])
        if posts_do_perfil:
            metricas = calcular_metricas_perfil(perfil, posts_do_perfil)
            perfil['engMedio'] = metricas['engMedio']
            perfil['mediaLikes'] = metricas['mediaLikes']
            perfil['formatoTop'] = metricas['formatoTop']
            perfil['metricas'] = metricas
        else:
            perfil['engMedio'] = 0
            perfil['mediaLikes'] = 0
            perfil['formatoTop'] = '-'
            perfil['metricas'] = {}

        perfis_finais.append(perfil)

    # Analise global de conteudo
    analise = analisar_conteudo_global(perfis_finais)

    # Etapa 5: Gerar dashboard
    log.info('--- Etapa 5: Gerando dashboard ---')

    # Preparar dados para o dashboard (sem base64 pesado no JSON exportado)
    perfis_para_dash = []
    todos_posts_rankeados = []
    for p in perfis_finais:
        pd = {k: v for k, v in p.items() if k != 'metricas'}
        # Incluir top 15 posts individuais do perfil (para pesquisa profunda)
        posts_do_perfil = p.get('metricas', {}).get('posts', [])
        top_posts_perfil = sorted(posts_do_perfil, key=lambda x: x.get('engajamento', 0), reverse=True)[:15]
        pd['posts'] = top_posts_perfil
        perfis_para_dash.append(pd)
        # Acumular para ranking global
        for tp in top_posts_perfil:
            tp_global = dict(tp)
            tp_global['ownerUsername'] = p.get('username', '')
            tp_global['ownerSeguidores'] = p.get('seguidores', 0)
            tp_global['origem'] = p.get('origem', '')
            todos_posts_rankeados.append(tp_global)

    # Top 10 posts globais por engajamento (cruzando todos os perfis)
    top_posts_global = sorted(todos_posts_rankeados, key=lambda x: x.get('engajamento', 0), reverse=True)[:10]
    log.info(f'Top 10 posts globais selecionados (melhor: {top_posts_global[0]["engajamento"]}% de @{top_posts_global[0]["ownerUsername"]})' if top_posts_global else 'Nenhum post para ranking global')

    pesquisa_data = {
        'config': {
            'hashtagsBR': hashtags_br,
            'hashtagsMundo': hashtags_mundo,
            'slug': slug,
        },
        'perfis': perfis_para_dash,
        'topPosts': top_posts_global,
        'analise': analise,
        'atualizadoEm': datetime.now().strftime('%d/%m/%Y %H:%M'),
    }

    # insights.json (sem base64 para ficar leve)
    insights_data = {
        'config': pesquisa_data['config'],
        'perfis': [{k: v for k, v in p.items() if k != 'fotoB64'} for p in perfis_para_dash],
        'topPosts': top_posts_global,
        'analise': analise,
        'atualizadoEm': pesquisa_data['atualizadoEm'],
    }
    insights_file = output_dir / 'insights.json'
    insights_file.write_text(json.dumps(insights_data, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    log.info('insights.json salvo')

    # dashboard.html
    html = gerar_html(pesquisa_data)
    dashboard_file = output_dir / 'dashboard.html'
    dashboard_file.write_text(html, encoding='utf-8')
    log.info(f'dashboard.html salvo: {dashboard_file}')

    log.info('=== Pesquisa concluida com sucesso ===')

    if args.abrir:
        webbrowser.open(str(dashboard_file))
        log.info('Dashboard aberto no navegador')

if __name__ == '__main__':
    main()
