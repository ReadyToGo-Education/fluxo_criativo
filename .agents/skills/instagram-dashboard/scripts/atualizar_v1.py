#!/usr/bin/env python3
"""
Workshop Inteligente - Instagram Dashboard
Le APIFY_API_TOKEN e IG_USER do .env, coleta dados do perfil e gera dashboard.html
no produto ativo lido de meus-produtos/.ativo
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

try:
    import requests
except ImportError:
    print("Erro: biblioteca 'requests' nao encontrada.")
    print("Instale com: pip install requests")
    sys.exit(1)

# ── Logging basico (console) — FileHandler adicionado em main() apos resolver paths ──
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

# ── Raiz do projeto ───────────────────────────────────────────────────────────
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
        log.error('meus-produtos/.ativo nao encontrado. Use /produto-novo para criar um produto.')
        sys.exit(1)
    ativo = ativo_file.read_text(encoding='utf-8').strip()
    if not ativo:
        log.error('meus-produtos/.ativo esta vazio.')
        sys.exit(1)
    output = PROJECT_ROOT / 'meus-produtos' / ativo / 'entregas' / 'instagram-dashboard'
    output.mkdir(parents=True, exist_ok=True)
    return output

# ── .env parser ───────────────────────────────────────────────────────────────
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
WHISPER_URL = 'https://api.apify.com/v2/acts/apify~whisper-speech-to-text/run-sync-get-dataset-items'

def apify_post(token, url_ator, payload, timeout=60, retries=3):
    url = f'{url_ator}?token={token}&timeout={timeout}'
    for tentativa in range(1, retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=timeout + 60)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            # Erros 4xx sao permanentes - nao retentar
            if e.response is not None and 400 <= e.response.status_code < 500:
                raise
            log.warning(f'  Apify erro HTTP {e.response.status_code if e.response else "?"} (tentativa {tentativa}/{retries}): {e}')
            if tentativa < retries:
                espera = tentativa * 10
                log.info(f'  Aguardando {espera}s antes de tentar novamente...')
                time.sleep(espera)
        except Exception as e:
            log.warning(f'  Apify erro (tentativa {tentativa}/{retries}): {e}')
            if tentativa < retries:
                espera = tentativa * 10
                log.info(f'  Aguardando {espera}s antes de tentar novamente...')
                time.sleep(espera)
    raise RuntimeError(f'Apify falhou apos {retries} tentativas')

def buscar_perfil(token, ig_user):
    log.info(f'Buscando perfil @{ig_user}...')
    data = apify_post(token, SCRAPER_URL, {
        'directUrls': [f'https://www.instagram.com/{ig_user}/'],
        'resultsType': 'details',
    }, timeout=60)
    if not data:
        raise ValueError('Apify nao retornou dados de perfil')
    return data[0]

def buscar_posts(token, ig_user):
    log.info(f'Buscando posts @{ig_user}...')
    limite = 30
    todos = []
    for tentativa in range(1, 5):
        log.info(f'  Tentativa {tentativa} — resultsLimit={limite}')
        data = apify_post(token, SCRAPER_URL, {
            'directUrls': [f'https://www.instagram.com/{ig_user}/'],
            'resultsType': 'posts',
            'resultsLimit': limite,
        }, timeout=300)
        if not data:
            break
        todos = data
        visiveis = [p for p in data if p.get('likesCount', -1) != -1]
        ocultos  = [p for p in data if p.get('likesCount', -1) == -1]
        log.info(f'  {len(data)} posts — {len(visiveis)} com likes visiveis, {len(ocultos)} ocultos')
        if len(visiveis) >= 30 or limite >= 100:
            # Prioriza posts com likes visiveis
            return visiveis[:30] + ocultos[:max(0, 30 - len(visiveis[:30]))]
        limite = min(limite + 30, 100)
    return todos[:30]

def baixar_b64(url, desc=''):
    if not url:
        return ''
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.instagram.com/',
        }
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            return base64.b64encode(resp.content).decode('utf-8')
    except Exception as e:
        log.warning(f'Falha ao baixar {desc}: {e}')
    return ''

def salvar_jpg(b64, caminho: Path):
    if b64:
        try:
            caminho.write_bytes(base64.b64decode(b64))
        except Exception as e:
            log.warning(f'Falha ao salvar {caminho}: {e}')

def transcrever_reel(token, video_url):
    if not video_url:
        return ''
    try:
        log.info('  Transcrevendo reel...')
        data = apify_post(token, WHISPER_URL, {'videoUrl': video_url}, timeout=120)
        if data and isinstance(data, list) and data[0].get('text'):
            return data[0]['text']
    except Exception as e:
        log.warning(f'Falha ao transcrever: {e}')
    return ''

# ── Normalizacao ──────────────────────────────────────────────────────────────
def tipo_post(raw):
    t = str(raw.get('type', raw.get('productType', ''))).lower()
    if 'video' in t or 'reel' in t or raw.get('isVideo'):
        return 'Reel'
    if raw.get('childPosts') or 'carousel' in t or (isinstance(raw.get('images'), list) and len(raw['images']) > 1):
        return 'Carrossel'
    return 'Foto'

def normalizar_perfil(raw):
    return {
        'username':   raw.get('username', ''),
        'nome':       raw.get('fullName') or raw.get('username', ''),
        'bio':        raw.get('biography', ''),
        'seguidores': raw.get('followersCount', 0) or 0,
        'seguindo':   raw.get('followsCount', 0) or 0,
        'totalPosts': raw.get('postsCount', 0) or 0,
        'verificado': bool(raw.get('verified')),
        'fotoPerfil': '',
        '_picUrl':    raw.get('profilePicUrl') or raw.get('profilePicUrlHD', ''),
    }

def normalizar_post(raw):
    likes       = raw.get('likesCount', -1)
    comentarios = raw.get('commentsCount', 0) or 0
    views       = raw.get('videoViewCount') or raw.get('videoPlayCount') or 0

    # Imagens do carrossel
    imgs_url = []
    if raw.get('childPosts'):
        for cp in raw['childPosts']:
            u = cp.get('displayUrl', '')
            if u: imgs_url.append(u)
    elif isinstance(raw.get('images'), list):
        for img in raw['images']:
            u = img.get('src', img) if isinstance(img, dict) else img
            if u: imgs_url.append(u)

    # Data
    ts = raw.get('timestamp', '')
    data_str = ''
    if ts:
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            data_str = dt.strftime('%d/%m/%Y')
        except Exception:
            data_str = ts[:10]

    sc = raw.get('shortCode') or raw.get('shortcode', '')
    url_post = f'https://www.instagram.com/p/{sc}/' if sc else raw.get('url', '')

    return {
        'shortCode':     sc,
        'tipo':          tipo_post(raw),
        'timestamp':     ts,
        'data':          data_str,
        'likes':         likes,
        'comentarios':   comentarios,
        'views':         views,
        'shares':        raw.get('sharesCount', 0) or 0,
        'legenda':       (raw.get('caption', '') or '')[:500],
        'url':           url_post,
        '_displayUrl':   raw.get('displayUrl', ''),
        '_imgsUrl':      imgs_url,
        '_videoUrl':     raw.get('videoUrl', ''),
        'imagem':        '',
        'imagens':       [],
        'thumbnailPath': '',
        'carouselPaths': [],
        'transcricao':   '',
        'engajamento':   0,
    }

# ── Dashboard HTML ────────────────────────────────────────────────────────────
def gerar_html(perfil, posts):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M')
    seg   = perfil['seguidores'] or 1

    for p in posts:
        likes = max(p['likes'], 0)
        p['engajamento'] = round((likes + p['comentarios']) / seg * 100, 2)

    def grupo(tipo): return [p for p in posts if p['tipo'] == tipo]
    reels      = grupo('Reel')
    carrosseis = grupo('Carrossel')
    fotos      = grupo('Foto')

    def media(lst, campo):
        vals = [max(p[campo], 0) for p in lst]
        return round(sum(vals) / len(vals), 1) if vals else 0

    eng_medio   = round(sum(p['engajamento'] for p in posts) / len(posts), 2) if posts else 0
    contagem    = {'Reel': len(reels), 'Carrossel': len(carrosseis), 'Foto': len(fotos)}
    formato_top = max(contagem, key=contagem.get) if posts else '-'
    top3        = sorted(posts, key=lambda p: p['engajamento'], reverse=True)[:3]
    cronologico = sorted([p for p in posts if p['timestamp']], key=lambda p: p['timestamp'])

    metricas = {
        'engMedio':   eng_medio,
        'formatoTop': formato_top,
        'reels': {
            'count':            len(reels),
            'mediaLikes':       media(reels, 'likes'),
            'mediaComentarios': media(reels, 'comentarios'),
            'totalViews':       sum(p['views'] for p in reels),
        },
        'carrosseis': {
            'count':            len(carrosseis),
            'mediaLikes':       media(carrosseis, 'likes'),
            'mediaComentarios': media(carrosseis, 'comentarios'),
        },
        'fotos': {
            'count':            len(fotos),
            'mediaLikes':       media(fotos, 'likes'),
            'mediaComentarios': media(fotos, 'comentarios'),
        },
    }

    # Campos limpos para JSON (sem _internos)
    def limpar_post(p):
        return {k: v for k, v in p.items() if not k.startswith('_')}

    dados_js = json.dumps({
        'perfil':            perfil,
        'posts':             [limpar_post(p) for p in posts],
        'top3':              [limpar_post(p) for p in top3],
        'postsCronologicos': [limpar_post(p) for p in cronologico],
        'metricas':          metricas,
        'atualizadoEm':      agora,
    }, ensure_ascii=False, default=str)

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard Instagram</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#f8fafc;--card:#fff;--border:#e2e8f0;--text:#1e293b;--muted:#64748b;
  --accent:#4338ca;--accent-lt:#eef2ff;
  --reel:#7c3aed;--carrossel:#0369a1;--foto:#059669;
  --sh:0 1px 3px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.04);
  --sh-md:0 4px 6px -1px rgba(0,0,0,.07);
  --r:12px;--r-sm:8px
}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text)}}
.wrap{{max-width:1200px;margin:0 auto;padding:24px 16px}}
/* header */
.hdr{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:24px;display:flex;align-items:center;gap:20px;margin-bottom:24px;box-shadow:var(--sh)}}
.avatar{{width:72px;height:72px;border-radius:50%;border:3px solid var(--accent);flex-shrink:0;background:var(--accent-lt);display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700;color:var(--accent);overflow:hidden}}
.avatar img{{width:100%;height:100%;object-fit:cover}}
.hinfo h1{{font-size:20px;font-weight:700}}
.hinfo .un{{color:var(--accent);font-size:14px;font-weight:500}}
.hinfo .bio{{color:var(--muted);font-size:13px;margin-top:4px;line-height:1.4}}
.hinfo .upd{{font-size:12px;color:var(--muted);margin-top:6px}}
/* kpi */
.kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}}
.kpi{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;box-shadow:var(--sh)}}
.kpi-lbl{{font-size:11px;font-weight:500;color:var(--muted);text-transform:uppercase;letter-spacing:.5px}}
.kpi-val{{font-size:28px;font-weight:700;margin-top:4px}}
.kpi-sub{{font-size:12px;color:var(--muted);margin-top:2px}}
.kpi-accent .kpi-val{{color:var(--accent)}}
/* formatos */
.fmt-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px}}
.fmt-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;box-shadow:var(--sh)}}
.fmt-nome{{font-size:14px;font-weight:700;margin-bottom:12px;display:flex;align-items:center;gap:8px}}
.dot{{width:10px;height:10px;border-radius:50%}}
.dot-r{{background:var(--reel)}}.dot-c{{background:var(--carrossel)}}.dot-f{{background:var(--foto)}}
.mets{{display:flex;gap:16px;flex-wrap:wrap}}
.met-lbl{{font-size:11px;color:var(--muted)}}
.met-val{{font-size:18px;font-weight:700}}
/* secao */
.sec{{font-size:16px;font-weight:700;margin-bottom:16px}}
/* top3 */
.top3-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px}}
.t3c{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh)}}
.t3c img,.t3c .t3ph{{width:100%;aspect-ratio:1;object-fit:cover;display:block;background:var(--accent-lt)}}
.t3c .t3ph{{display:flex;align-items:center;justify-content:center;font-size:12px;color:var(--muted)}}
.t3b{{padding:12px}}
.badge{{display:inline-block;padding:2px 8px;border-radius:99px;font-size:11px;font-weight:600;margin-bottom:8px}}
.br{{background:#f3e8ff;color:var(--reel)}}.bc{{background:#e0f2fe;color:var(--carrossel)}}.bf{{background:#d1fae5;color:var(--foto)}}
.t3stats{{display:flex;gap:10px;font-size:13px;flex-wrap:wrap;margin-bottom:4px}}
.t3sv{{font-weight:700}}
.t3eng{{font-size:13px;font-weight:600;color:var(--accent)}}
.vlink{{display:inline-block;margin-top:6px;font-size:12px;color:var(--accent);text-decoration:none;font-weight:500}}
.vlink:hover{{text-decoration:underline}}
/* grafico */
.chart-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:24px;box-shadow:var(--sh)}}
.ch-title{{font-size:13px;font-weight:600;color:var(--muted);margin-bottom:8px}}
.ch-legend{{display:flex;gap:14px;margin-bottom:8px;flex-wrap:wrap}}
.leg{{display:flex;align-items:center;gap:5px;font-size:12px}}
.ldot{{width:10px;height:10px;border-radius:50%}}
canvas{{width:100%!important;display:block}}
/* grade posts */
.pg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px;margin-bottom:24px}}
.pc{{background:var(--card);border:1px solid var(--border);border-radius:var(--r-sm);overflow:hidden;box-shadow:var(--sh)}}
.pw{{position:relative;width:100%;aspect-ratio:1;background:var(--accent-lt);cursor:pointer}}
.pw img{{width:100%;height:100%;object-fit:cover;display:block}}
.ci{{position:absolute;bottom:6px;right:6px;background:rgba(0,0,0,.55);color:#fff;font-size:10px;padding:2px 6px;border-radius:99px}}
.pb{{padding:10px}}
.pstats{{display:flex;gap:8px;font-size:12px;flex-wrap:wrap}}
.psv{{font-weight:700}}
.pdata{{font-size:11px;color:var(--muted);margin-top:3px}}
.pleg{{font-size:11px;color:var(--muted);margin-top:3px;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}}
@media(max-width:768px){{
  .kpi-grid{{grid-template-columns:repeat(2,1fr)}}
  .fmt-grid,.top3-grid{{grid-template-columns:1fr}}
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
function bc(tipo){{return tipo==='Reel'?'br':tipo==='Carrossel'?'bc':'bf'}}
function dc(tipo){{return tipo==='Reel'?'dot-r':tipo==='Carrossel'?'dot-c':'dot-f'}}

function render(){{
  const{{perfil:p,posts,top3,postsCronologicos:crono,metricas:m,atualizadoEm}}=D;
  const fotoSrc=p.fotoPerfil?`data:image/jpeg;base64,${{p.fotoPerfil}}`:'';
  const avInner=fotoSrc?`<img src="${{fotoSrc}}" alt="">`:`${{(p.nome||p.username||'?')[0].toUpperCase()}}`;

  document.getElementById('app').innerHTML=`
  <div class="hdr">
    <div class="avatar">${{avInner}}</div>
    <div class="hinfo">
      <h1>${{p.nome||p.username}}${{p.verificado?' <svg style="display:inline-block;vertical-align:middle;margin-left:6px" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="10" cy="10" r="10" fill="#4338ca"/><path d="M6 10.5l2.5 2.5 5.5-5.5" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>':''}}</h1>
      <div class="un">@${{p.username}}</div>
      ${{p.bio?`<div class="bio">${{p.bio}}</div>`:''}}
      <div class="upd">Atualizado em ${{atualizadoEm}}</div>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-lbl">Seguidores</div><div class="kpi-val">${{fmt(p.seguidores)}}</div><div class="kpi-sub">${{fmt(p.seguindo)}} seguindo</div></div>
    <div class="kpi kpi-accent"><div class="kpi-lbl">Engajamento medio</div><div class="kpi-val">${{m.engMedio}}%</div><div class="kpi-sub">media dos ultimos posts</div></div>
    <div class="kpi"><div class="kpi-lbl">Total de posts</div><div class="kpi-val">${{fmt(p.totalPosts)}}</div><div class="kpi-sub">no perfil</div></div>
    <div class="kpi"><div class="kpi-lbl">Formato mais postado</div><div class="kpi-val" style="font-size:22px">${{m.formatoTop}}</div><div class="kpi-sub">ultimos ${{posts.length}} posts</div></div>
  </div>

  <div class="sec">Desempenho por Formato</div>
  <div class="fmt-grid">
    <div class="fmt-card">
      <div class="fmt-nome"><span class="dot dot-r"></span>Reels (${{m.reels.count}})</div>
      <div class="mets">
        <div><div class="met-lbl">Media de likes</div><div class="met-val">${{fmt(m.reels.mediaLikes)}}</div></div>
        <div><div class="met-lbl">Media comentarios</div><div class="met-val">${{fmt(m.reels.mediaComentarios)}}</div></div>
        <div><div class="met-lbl">Views totais</div><div class="met-val">${{fmt(m.reels.totalViews)}}</div></div>
      </div>
    </div>
    <div class="fmt-card">
      <div class="fmt-nome"><span class="dot dot-c"></span>Carrosseis (${{m.carrosseis.count}})</div>
      <div class="mets">
        <div><div class="met-lbl">Media de likes</div><div class="met-val">${{fmt(m.carrosseis.mediaLikes)}}</div></div>
        <div><div class="met-lbl">Media comentarios</div><div class="met-val">${{fmt(m.carrosseis.mediaComentarios)}}</div></div>
      </div>
    </div>
    <div class="fmt-card">
      <div class="fmt-nome"><span class="dot dot-f"></span>Fotos (${{m.fotos.count}})</div>
      <div class="mets">
        <div><div class="met-lbl">Media de likes</div><div class="met-val">${{fmt(m.fotos.mediaLikes)}}</div></div>
        <div><div class="met-lbl">Media comentarios</div><div class="met-val">${{fmt(m.fotos.mediaComentarios)}}</div></div>
      </div>
    </div>
  </div>

  <div class="sec">Top 3 Posts</div>
  <div class="top3-grid">
    ${{top3.map(t=>`
    <div class="t3c">
      ${{t.imagem?`<img src="data:image/jpeg;base64,${{t.imagem}}" alt="">`:`<div class="t3ph">Sem imagem</div>`}}
      <div class="t3b">
        <span class="badge ${{bc(t.tipo)}}">${{t.tipo}}</span>
        <div class="t3stats">
          <span><span class="t3sv">${{fmt(t.likes)}}</span> likes</span>
          <span><span class="t3sv">${{fmt(t.comentarios)}}</span> com.</span>
          ${{t.tipo==='Reel'?`<span><span class="t3sv">${{fmt(t.views)}}</span> views</span>`:''}}
        </div>
        <div class="t3eng">${{t.engajamento}}% engajamento</div>
        ${{t.url?`<a class="vlink" href="${{t.url}}" target="_blank">Ver post original</a>`:''}}
      </div>
    </div>`).join('')}}
  </div>

  <div class="chart-card">
    <div class="sec" style="margin-bottom:12px">Linha do Tempo</div>
    <div class="ch-legend">
      <div class="leg"><div class="ldot" style="background:var(--reel)"></div>Reels</div>
      <div class="leg"><div class="ldot" style="background:var(--carrossel)"></div>Carrossel</div>
      <div class="leg"><div class="ldot" style="background:var(--foto)"></div>Foto</div>
    </div>
    <div class="ch-title">Curtidas</div>
    <canvas id="cLikes" height="120"></canvas>
    <div class="ch-title" style="margin-top:20px">Visualizacoes (Reels)</div>
    <canvas id="cViews" height="80"></canvas>
    <div class="ch-title" style="margin-top:20px">Engajamento (%)</div>
    <canvas id="cEng" height="80"></canvas>
  </div>

  <div class="sec">Todos os Posts (${{posts.length}})</div>
  <div class="pg" id="postsGrid"></div>
  `;

  renderPosts(posts);
  setTimeout(renderCharts,100);
}}

function renderPosts(posts){{
  const grid=document.getElementById('postsGrid');
  posts.forEach((post,idx)=>{{
    const div=document.createElement('div');
    div.className='pc';
    const allB64=[];
    if(post.imagem)allB64.push(post.imagem);
    (post.imagens||[]).forEach(b=>{{if(b)allB64.push(b)}});
    const multi=allB64.length>1;
    let cur=0;
    div.innerHTML=`
    <div class="pw" id="pw${{idx}}">
      ${{allB64.length?`<img id="pimg${{idx}}" src="data:image/jpeg;base64,${{allB64[0]}}" alt="">`:`<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:11px;color:var(--muted)">Sem imagem</div>`}}
      ${{multi?`<span class="ci" id="pci${{idx}}">1/${{allB64.length}}</span>`:''}}
    </div>
    <div class="pb">
      <span class="badge ${{bc(post.tipo)}}">${{post.tipo}}</span>
      <div class="pstats">
        <span><span class="psv">${{fmt(post.likes)}}</span> likes</span>
        <span><span class="psv">${{fmt(post.comentarios)}}</span> com.</span>
        ${{post.tipo==='Reel'?`<span><span class="psv">${{fmt(post.views)}}</span> views</span>`:''}}
      </div>
      <div class="pdata">${{post.data||''}}</div>
      ${{post.legenda?`<div class="pleg">${{post.legenda.substring(0,120)}}</div>`:''}}
      ${{post.url?`<a class="vlink" href="${{post.url}}" target="_blank">Ver post original</a>`:''}}
    </div>`;
    if(multi){{
      div.querySelector('.pw').addEventListener('click',()=>{{
        cur=(cur+1)%allB64.length;
        document.getElementById('pimg'+idx).src='data:image/jpeg;base64,'+allB64[cur];
        document.getElementById('pci'+idx).textContent=(cur+1)+'/'+allB64.length;
      }});
    }}
    grid.appendChild(div);
  }});
}}

function renderCharts(){{
  const posts=D.postsCronologicos;
  if(!posts.length)return;
  const COR={{Reel:'#7c3aed',Carrossel:'#0369a1',Foto:'#059669'}};

  function draw(canvasId,getVal){{
    const canvas=document.getElementById(canvasId);
    if(!canvas)return;
    canvas.width=canvas.parentElement.offsetWidth||800;
    const W=canvas.width,H=canvas.height;
    const PAD={{t:10,r:20,b:28,l:52}};
    const cw=W-PAD.l-PAD.r,ch=H-PAD.t-PAD.b;
    const ctx=canvas.getContext('2d');
    ctx.clearRect(0,0,W,H);

    // grid
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1;
    for(let i=0;i<=4;i++){{
      const y=PAD.t+ch*(1-i/4);
      ctx.beginPath();ctx.moveTo(PAD.l,y);ctx.lineTo(PAD.l+cw,y);ctx.stroke();
    }}

    const series=['Reel','Carrossel','Foto'].map(tipo=>{{
      return{{tipo,pts:posts.filter(p=>p.tipo===tipo).map(p=>{{return{{ts:p.timestamp,v:getVal(p)}}}})}}
    }}).filter(s=>s.pts.length>0);

    const allV=series.flatMap(s=>s.pts.map(pt=>pt.v));
    const maxV=Math.max(...allV,1);
    const allTs=posts.map(p=>p.timestamp).sort();
    const t0=new Date(allTs[0]),t1=new Date(allTs[allTs.length-1]);
    const tRange=t1-t0||1;

    const xOf=ts=>PAD.l+((new Date(ts)-t0)/tRange)*cw;
    const yOf=v=>PAD.t+ch*(1-v/maxV);

    // eixo Y
    ctx.fillStyle='#64748b';ctx.font='11px Inter,sans-serif';ctx.textAlign='right';
    [0,0.5,1].forEach(f=>{{
      const v=maxV*f;
      ctx.fillText(fmt(v),PAD.l-5,yOf(v)+4);
    }});

    // eixo X
    ctx.textAlign='left';
    const fd=ts=>new Date(ts).toLocaleDateString('pt-BR',{{day:'2-digit',month:'2-digit'}});
    ctx.fillText(fd(allTs[0]),PAD.l,H-6);
    ctx.textAlign='right';
    ctx.fillText(fd(allTs[allTs.length-1]),PAD.l+cw,H-6);

    // linhas e pontos
    series.forEach(s=>{{
      const cor=COR[s.tipo]||'#999';
      ctx.strokeStyle=cor;ctx.fillStyle=cor;ctx.lineWidth=2;
      ctx.beginPath();
      s.pts.forEach((pt,i)=>{{
        const x=xOf(pt.ts),y=yOf(pt.v);
        i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
      }});
      ctx.stroke();
      s.pts.forEach(pt=>{{
        ctx.beginPath();ctx.arc(xOf(pt.ts),yOf(pt.v),4,0,Math.PI*2);ctx.fill();
      }});
    }});

    // Tooltip
    canvas._s=series;canvas._xOf=xOf;canvas._yOf=yOf;canvas._COR=COR;
    if(!canvas._tt){{
      canvas._tt=true;
      canvas.addEventListener('mousemove',e=>ttMove(canvas,e));
      canvas.addEventListener('mouseleave',ttHide);
    }}
  }}

  draw('cLikes',p=>Math.max(p.likes,0));
  draw('cViews',p=>p.views||0);
  draw('cEng',p=>p.engajamento||0);
}}

let ttEl=null;
function ttMove(canvas,e){{
  const r=canvas.getBoundingClientRect();
  const mx=e.clientX-r.left,my=e.clientY-r.top;
  let closest=null,minD=20;
  canvas._s.forEach(s=>s.pts.forEach(pt=>{{
    const x=canvas._xOf(pt.ts),y=canvas._yOf(pt.v);
    const d=Math.hypot(mx-x,my-y);
    if(d<minD){{minD=d;closest={{...pt,tipo:s.tipo}};}}
  }}));
  if(!closest)return ttHide();
  if(!ttEl){{
    ttEl=document.createElement('div');
    ttEl.style.cssText='position:fixed;background:#1e293b;color:#fff;padding:7px 11px;border-radius:8px;font-size:12px;font-family:Inter,sans-serif;pointer-events:none;z-index:9999';
    document.body.appendChild(ttEl);
  }}
  const dt=new Date(closest.ts).toLocaleDateString('pt-BR',{{day:'2-digit',month:'2-digit',year:'2-digit'}});
  ttEl.innerHTML=`<b style="color:${{canvas._COR[closest.tipo]||'#fff'}}">${{closest.tipo}}</b><br>${{fmt(closest.v)}} | ${{dt}}`;
  ttEl.style.display='block';
  ttEl.style.left=(e.clientX+14)+'px';
  ttEl.style.top=(e.clientY-10)+'px';
}}
function ttHide(){{if(ttEl)ttEl.style.display='none';}}

window.addEventListener('load',render);
window.addEventListener('resize',()=>renderCharts&&renderCharts());
</script>
</body>
</html>'''

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--abrir', action='store_true')
    args = parser.parse_args()

    # Resolver caminhos de output a partir do produto ativo
    output_dir    = get_output_dir()
    images_dir    = output_dir / 'imagens'
    log_file      = output_dir / 'log.txt'
    insights_file = output_dir / 'insights.json'
    dashboard_file = output_dir / 'dashboard.html'
    images_dir.mkdir(parents=True, exist_ok=True)

    # Adicionar FileHandler ao logger agora que temos o caminho
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logging.getLogger().addHandler(file_handler)

    log.info('=== Iniciando atualizacao do dashboard Instagram ===')
    log.info(f'Output: {output_dir}')

    env = ler_env()
    token   = env.get('APIFY_API_TOKEN', '')
    ig_user = env.get('IG_USER', '')

    if not token:
        log.error('APIFY_API_TOKEN nao encontrado no .env'); sys.exit(1)
    if not ig_user:
        log.error('IG_USER nao encontrado no .env'); sys.exit(1)

    log.info(f'Perfil: @{ig_user}')

    # Perfil
    raw_perfil = buscar_perfil(token, ig_user)
    perfil     = normalizar_perfil(raw_perfil)
    log.info('Baixando foto de perfil...')
    perfil['fotoPerfil'] = baixar_b64(perfil['_picUrl'], 'foto de perfil')

    # Posts (aguarda 5s para o plano gratuito Apify liberar concorrencia)
    log.info('Aguardando 5s antes de buscar posts...')
    time.sleep(5)
    raw_posts = buscar_posts(token, ig_user)
    log.info(f'{len(raw_posts)} posts selecionados')
    posts = [normalizar_post(r) for r in raw_posts]

    # Imagens
    for i, post in enumerate(posts):
        log.info(f'Baixando imagens post {i+1}/{len(posts)} ({post["tipo"]})...')
        b64 = baixar_b64(post['_displayUrl'], f'thumb post {i+1}')
        post['imagem'] = b64
        if b64:
            thumb_path = images_dir / f'post_{i+1:02d}_thumb.jpg'
            salvar_jpg(b64, thumb_path)
            post['thumbnailPath'] = f'imagens/post_{i+1:02d}_thumb.jpg'

        carousel_b64, carousel_paths = [], []
        for j, img_url in enumerate(post['_imgsUrl'][:10]):
            b = baixar_b64(img_url, f'slide {j+1} post {i+1}')
            if b:
                carousel_b64.append(b)
                sp = images_dir / f'post_{i+1:02d}_slide_{j+1:02d}.jpg'
                salvar_jpg(b, sp)
                carousel_paths.append(f'imagens/post_{i+1:02d}_slide_{j+1:02d}.jpg')
        post['imagens']       = carousel_b64
        post['carouselPaths'] = carousel_paths

        if post['tipo'] == 'Reel' and post.get('_videoUrl'):
            post['transcricao'] = transcrever_reel(token, post['_videoUrl'])

    # insights.json (sem base64)
    def slim(p):
        s = {k: v for k, v in p.items() if k not in ('imagem', 'imagens') and not k.startswith('_')}
        return s
    insights = {
        'perfil':       {k: v for k, v in perfil.items() if not k.startswith('_') and k != 'fotoPerfil'},
        'posts':        [slim(p) for p in posts],
        'atualizadoEm': datetime.now().isoformat(),
    }
    insights_file.write_text(json.dumps(insights, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    log.info('insights.json salvo')

    # dashboard.html
    log.info('Gerando dashboard.html...')
    html = gerar_html(perfil, posts)
    dashboard_file.write_text(html, encoding='utf-8')
    log.info(f'dashboard.html salvo: {dashboard_file}')

    log.info('=== Concluido com sucesso ===')

    if args.abrir:
        webbrowser.open(dashboard_file.as_uri())
        log.info('Dashboard aberto no navegador')

if __name__ == '__main__':
    main()
