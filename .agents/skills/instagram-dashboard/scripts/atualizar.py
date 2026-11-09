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
from concurrent.futures import ThreadPoolExecutor, as_completed

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
SCRAPER_URL      = 'https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items'
SCRAPER_RUN_URL  = 'https://api.apify.com/v2/acts/apify~instagram-scraper/runs'
APIFY_RUNS_BASE  = 'https://api.apify.com/v2/actor-runs'

def apify_post(token, url_ator, payload, timeout=60, retries=3):
    url = f'{url_ator}?token={token}&timeout={timeout}'
    for tentativa in range(1, retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=timeout + 60)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
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

def apify_async(token, payload, max_wait=1200, poll_interval=30):
    """Dispara run async no Apify e faz polling ate concluir. Evita timeout de conexao HTTP."""
    url = f'{SCRAPER_RUN_URL}?token={token}'
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    run = resp.json().get('data', {})
    run_id = run.get('id')
    dataset_id = run.get('defaultDatasetId')
    if not run_id:
        raise RuntimeError('Apify nao retornou runId')
    log.info(f'  Run iniciado: {run_id}. Aguardando conclusao (max {max_wait}s)...')
    elapsed = 0
    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval
        status_resp = requests.get(f'{APIFY_RUNS_BASE}/{run_id}?token={token}', timeout=30)
        status_resp.raise_for_status()
        status = status_resp.json().get('data', {}).get('status', '')
        log.info(f'  [{elapsed}s] Status: {status}')
        if status == 'SUCCEEDED':
            items_resp = requests.get(
                f'https://api.apify.com/v2/datasets/{dataset_id}/items?token={token}&clean=true',
                timeout=60
            )
            items_resp.raise_for_status()
            return items_resp.json()
        if status in ('FAILED', 'ABORTED', 'TIMED-OUT'):
            raise RuntimeError(f'Apify run {run_id} terminou com status: {status}')
    raise RuntimeError(f'Apify run {run_id} nao concluiu em {max_wait}s')

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
    log.info('  Usando modo async (polling) para evitar timeout de conexao...')
    data = apify_async(token, {
        'directUrls': [f'https://www.instagram.com/{ig_user}/'],
        'resultsType': 'posts',
        'resultsLimit': 30,
    }, max_wait=1200, poll_interval=30)
    if not data:
        raise ValueError('Apify nao retornou posts')
    visiveis = [p for p in data if p.get('likesCount', -1) != -1]
    ocultos  = [p for p in data if p.get('likesCount', -1) == -1]
    log.info(f'  {len(data)} posts — {len(visiveis)} com likes visiveis, {len(ocultos)} ocultos')
    return visiveis[:30] + ocultos[:max(0, 30 - len(visiveis[:30]))]

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

# ── Metricas (extraido de gerar_html para reuso) ─────────────────────────────
def calcular_metricas(perfil, posts):
    seg = perfil['seguidores'] or 1
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

    return {
        'engMedio':   eng_medio,
        'formatoTop': formato_top,
        'totalShares': sum(p['shares'] for p in posts),
        'reels': {
            'count':            len(reels),
            'mediaLikes':       media(reels, 'likes'),
            'mediaComentarios': media(reels, 'comentarios'),
            'mediaShares':      media(reels, 'shares'),
            'totalViews':       sum(p['views'] for p in reels),
        },
        'carrosseis': {
            'count':            len(carrosseis),
            'mediaLikes':       media(carrosseis, 'likes'),
            'mediaComentarios': media(carrosseis, 'comentarios'),
            'mediaShares':      media(carrosseis, 'shares'),
        },
        'fotos': {
            'count':            len(fotos),
            'mediaLikes':       media(fotos, 'likes'),
            'mediaComentarios': media(fotos, 'comentarios'),
            'mediaShares':      media(fotos, 'shares'),
        },
    }

# ── Historico (snapshots acumulativos entre execucoes) ────────────────────────
def atualizar_historico(base_dir, perfil, metricas):
    hist_file = base_dir / 'historico.json'
    historico = []
    if hist_file.exists():
        try:
            historico = json.loads(hist_file.read_text(encoding='utf-8'))
            if not isinstance(historico, list):
                historico = []
        except Exception:
            historico = []
    hoje = datetime.now().strftime('%Y-%m-%d')
    username = perfil.get('username', '')
    snapshot = {
        'data':        datetime.now().isoformat(),
        'username':    username,
        'seguidores':  perfil['seguidores'],
        'engMedio':    metricas['engMedio'],
        'totalPosts':  perfil['totalPosts'],
        'totalShares': metricas['totalShares'],
    }
    # Substitui snapshot do mesmo perfil + mesmo dia em vez de duplicar
    historico = [h for h in historico if not (h.get('data', '')[:10] == hoje and h.get('username', '') == username)]
    historico.append(snapshot)
    hist_file.write_text(json.dumps(historico, ensure_ascii=False, indent=2), encoding='utf-8')
    # Retorna apenas snapshots do perfil atual
    hist_perfil = [h for h in historico if h.get('username', '') == username]
    log.info(f'historico.json atualizado ({len(historico)} snapshots, {len(hist_perfil)} do @{username})')
    return hist_perfil

# ── Dashboard HTML ────────────────────────────────────────────────────────────
def gerar_html(perfil, posts, metricas, historico=None, variacoes=None):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M')
    top3        = sorted(posts, key=lambda p: p['engajamento'], reverse=True)[:3]
    cronologico = sorted([p for p in posts if p['timestamp']], key=lambda p: p['timestamp'])

    # Campos limpos para JSON (sem _internos)
    def limpar_post(p):
        return {k: v for k, v in p.items() if not k.startswith('_')}

    dados_js = json.dumps({
        'perfil':            perfil,
        'posts':             [limpar_post(p) for p in posts],
        'top3':              [limpar_post(p) for p in top3],
        'postsCronologicos': [limpar_post(p) for p in cronologico],
        'metricas':          metricas,
        'historico':         historico or [],
        'variacoes':         variacoes or [],
        'atualizadoEm':      agora,
    }, ensure_ascii=False, default=str)

    recharts_js = r"""
(function () {
  if (typeof Recharts === 'undefined' || typeof React === 'undefined') {
    console.warn('Recharts ou React nao encontrado. Graficos nao serao renderizados via Recharts.');
    return;
  }
  var R = Recharts;
  var h = React.createElement;
  var TOOLTIP_STYLE = {
    background: 'hsl(240,10%,4%)', border: '1px solid hsl(240,4%,16%)', color: 'hsl(0,0%,98%)',
    fontFamily: "'Inter', sans-serif", fontSize: 12, borderRadius: 8, padding: '8px 12px',
    boxShadow: '0 4px 6px -1px rgba(0,0,0,.6)'
  };
  var TICK_STYLE = { fill: 'hsl(240,5%,65%)', fontSize: 11, fontFamily: "'Inter', sans-serif" };
  var COR = { Reel: 'hsl(220,70%,50%)', Carrossel: 'hsl(280,65%,60%)', Foto: 'hsl(160,60%,45%)' };

  function makeTimelineChart(containerId, data, height) {
    var container = document.getElementById(containerId);
    if (!container || !data.length) return;
    var tipos = ['Reel', 'Carrossel', 'Foto'].filter(function (t) {
      return data.some(function (d) { return d[t] !== null && d[t] !== undefined; });
    });
    var lines = tipos.map(function (tipo) {
      return h(R.Line, {
        key: tipo, type: 'monotone', dataKey: tipo,
        stroke: COR[tipo], strokeWidth: 2,
        dot: { r: 3, fill: COR[tipo], strokeWidth: 0 },
        activeDot: { r: 5 }, connectNulls: true, name: tipo
      });
    });
    var args = [R.LineChart, { data: data, margin: { top: 8, right: 40, left: 10, bottom: 20 } },
      h(R.CartesianGrid, { strokeDasharray: '4 4', stroke: 'hsl(240,4%,16%)', vertical: false }),
      h(R.XAxis, { dataKey: 'date', stroke: 'hsl(240,4%,16%)', tick: TICK_STYLE, interval: 'preserveStartEnd' }),
      h(R.YAxis, { stroke: 'hsl(240,4%,16%)', tick: TICK_STYLE, tickFormatter: fmt, width: 52 }),
      h(R.Tooltip, {
        contentStyle: TOOLTIP_STYLE,
        formatter: function (v, name) { return [fmt(v), name]; },
        labelStyle: { color: 'hsl(240,5%,65%)' }
      })
    ].concat(lines);
    var chart = h(R.ResponsiveContainer, { width: '100%', height: height },
      h.apply(null, args)
    );
    ReactDOM.createRoot(container).render(chart);
  }

  function makeHistChart(containerId, dataKey, hist) {
    var container = document.getElementById(containerId);
    if (!container) return;
    var data = hist.map(function (entry) {
      return { date: (entry.data || '').substring(0, 10), value: entry[dataKey] };
    });
    var chart = h(R.ResponsiveContainer, { width: '100%', height: 120 },
      h(R.LineChart, { data: data, margin: { top: 8, right: 40, left: 10, bottom: 20 } },
        h(R.CartesianGrid, { strokeDasharray: '4 4', stroke: 'hsl(240,4%,16%)', vertical: false }),
        h(R.XAxis, { dataKey: 'date', stroke: 'hsl(240,4%,16%)', tick: TICK_STYLE, interval: 'preserveStartEnd' }),
        h(R.YAxis, { stroke: 'hsl(240,4%,16%)', tick: TICK_STYLE, tickFormatter: fmt, width: 52 }),
        h(R.Tooltip, {
          contentStyle: TOOLTIP_STYLE,
          formatter: function (v) { return [fmt(v)]; },
          labelStyle: { color: 'hsl(240,5%,65%)' }
        }),
        h(R.Line, {
          type: 'monotone', dataKey: 'value',
          stroke: 'hsl(220,70%,50%)', strokeWidth: 2,
          dot: { r: 3, fill: 'hsl(220,70%,50%)', strokeWidth: 0 },
          activeDot: { r: 5 }
        })
      )
    );
    ReactDOM.createRoot(container).render(chart);
  }

  window.renderRechartsTimeline = function () {
    var posts = D.postsCronologicos;
    if (!posts || !posts.length) return;
    function buildData(getVal) {
      return posts.map(function (p, i) {
        var row = { date: p.data || String(i + 1) };
        row['Reel']      = p.tipo === 'Reel'      ? getVal(p) : null;
        row['Carrossel'] = p.tipo === 'Carrossel' ? getVal(p) : null;
        row['Foto']      = p.tipo === 'Foto'      ? getVal(p) : null;
        return row;
      });
    }
    makeTimelineChart('chartLikes',  buildData(function (p) { return Math.max(p.likes, 0); }), 160);
    makeTimelineChart('chartViews',  buildData(function (p) { return p.views || 0; }),          110);
    makeTimelineChart('chartEng',    buildData(function (p) { return p.engajamento || 0; }),    110);
    if (D.posts && D.posts.some(function (p) { return p.shares > 0; })) {
      makeTimelineChart('chartShares', buildData(function (p) { return p.shares || 0; }), 110);
    }
  };

  window.renderRechartsHistorico = function () {
    var hist = D.historico;
    if (!hist || hist.length < 2) return;
    makeHistChart('chartHistSeg', 'seguidores', hist);
    makeHistChart('chartHistEng', 'engMedio', hist);
  };
})();
"""

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard Instagram</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/prop-types/prop-types.min.js" crossorigin></script>
<script src="https://unpkg.com/recharts@2/umd/Recharts.js" crossorigin></script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --ink-0:#000000;--ink-1:#0a0a0a;--ink-2:#111111;--ink-3:#141414;--ink-4:#1a1a1a;--ink-5:#242424;
  --line-1:#1a1a1a;--line-2:#252525;--line-3:#303030;
  --text-hi:#ffffff;--text-mid:#e8e8e6;--text-dim:#cfcfcb;--text-faint:#a8a8a3;
  --neon:#c4ff5e;--neon-dim:#9acc2e;
  --reel:#c4ff5e;--carrossel:#9a7bb5;--foto:#7aa8c9;
  --accent:#c4ff5e;--accent-lt:#1a1a1a;--muted:#a8a8a3;
  --text:#e8e8e6;--bg:#000000;--card:#111111;--border:#252525;
  --r:0px;--r-sm:0px;--sh:none;--sh-md:none
}}
body{{font-family:'Space Grotesk','Inter',sans-serif;background:var(--ink-0);color:var(--text-mid)}}
.wrap{{max-width:1200px;margin:0 auto;padding:24px 16px}}
.hdr{{background:var(--ink-2);border-top:2px solid var(--neon);border-bottom:1px solid var(--line-2);padding:24px;display:flex;align-items:center;gap:20px;margin-bottom:24px}}
.avatar{{width:72px;height:72px;border-radius:50%;border:2px solid var(--neon);flex-shrink:0;background:var(--ink-3);display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700;color:var(--neon);overflow:hidden;font-family:'JetBrains Mono',monospace}}
.avatar img{{width:100%;height:100%;object-fit:cover}}
.hinfo h1{{font-size:20px;font-weight:700;color:var(--text-hi)}}
.hinfo .un{{color:var(--neon);font-size:14px;font-weight:500;font-family:'JetBrains Mono',monospace}}
.hinfo .bio{{color:var(--text-dim);font-size:13px;margin-top:4px;line-height:1.4}}
.hinfo .upd{{font-size:12px;color:var(--text-faint);margin-top:6px;font-family:'JetBrains Mono',monospace}}
.kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}}
.kpi{{background:var(--ink-2);border-top:2px solid var(--line-3);border-bottom:1px solid var(--line-2);padding:20px}}
.kpi-lbl{{font-size:11px;font-weight:500;color:var(--text-faint);text-transform:uppercase;letter-spacing:.5px;font-family:'JetBrains Mono',monospace}}
.kpi-val{{font-size:28px;font-weight:700;margin-top:4px;color:var(--text-hi)}}
.kpi-sub{{font-size:12px;color:var(--text-faint);margin-top:2px}}
.kpi-accent .kpi-val{{color:var(--neon)}}
.fmt-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px}}
.fmt-card{{background:var(--ink-2);border-top:2px solid var(--line-3);border-bottom:1px solid var(--line-2);padding:20px}}
.fmt-nome{{font-size:14px;font-weight:700;margin-bottom:12px;display:flex;align-items:center;gap:8px;color:var(--text-hi)}}
.dot{{width:10px;height:10px;border-radius:50%}}
.dot-r{{background:var(--reel)}}.dot-c{{background:var(--carrossel)}}.dot-f{{background:var(--foto)}}
.mets{{display:flex;gap:16px;flex-wrap:wrap}}
.met-lbl{{font-size:11px;color:var(--text-faint)}}
.met-val{{font-size:18px;font-weight:700;color:var(--text-hi)}}
.sec{{font-size:16px;font-weight:700;margin-bottom:16px;color:var(--text-hi)}}
.top3-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px}}
.t3c{{background:var(--ink-2);border-top:2px solid var(--line-3);overflow:hidden}}
.t3c img,.t3c .t3ph{{width:100%;aspect-ratio:1;object-fit:cover;display:block;background:var(--ink-3)}}
.t3c .t3ph{{display:flex;align-items:center;justify-content:center;font-size:12px;color:var(--text-faint)}}
.t3b{{padding:12px}}
.badge{{display:inline-block;padding:2px 8px;font-size:11px;font-weight:600;margin-bottom:8px;font-family:'JetBrains Mono',monospace;border:1px solid}}
.br{{border-color:var(--reel);color:var(--reel);background:transparent}}.bc{{border-color:var(--carrossel);color:var(--carrossel);background:transparent}}.bf{{border-color:var(--foto);color:var(--foto);background:transparent}}
.t3stats{{display:flex;gap:10px;font-size:13px;flex-wrap:wrap;margin-bottom:4px;color:var(--text-dim)}}
.t3sv{{font-weight:700;color:var(--text-hi)}}
.t3eng{{font-size:13px;font-weight:600;color:var(--neon)}}
.vlink{{display:inline-block;margin-top:6px;font-size:12px;color:var(--neon);text-decoration:none;font-weight:500;font-family:'JetBrains Mono',monospace}}
.vlink:hover{{text-decoration:underline}}
.chart-card{{background:var(--ink-2);border-top:2px solid var(--line-3);border-bottom:1px solid var(--line-2);padding:20px;margin-bottom:24px}}
.ch-title{{font-size:13px;font-weight:600;color:var(--text-faint);margin-bottom:8px;font-family:'JetBrains Mono',monospace}}
.ch-legend{{display:flex;gap:14px;margin-bottom:8px;flex-wrap:wrap}}
.leg{{display:flex;align-items:center;gap:5px;font-size:12px;color:var(--text-dim)}}
.ldot{{width:10px;height:10px;border-radius:50%}}
.recharts-wrapper{{overflow:visible}}
.pg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px;margin-bottom:24px}}
.pc{{background:var(--ink-2);border-top:2px solid var(--line-3);overflow:hidden}}
.pw{{position:relative;width:100%;aspect-ratio:1;background:var(--ink-3);cursor:pointer}}
.pw img{{width:100%;height:100%;object-fit:cover;display:block}}
.ci{{position:absolute;bottom:6px;right:6px;background:rgba(0,0,0,.75);color:var(--text-hi);font-size:10px;padding:2px 6px;font-family:'JetBrains Mono',monospace}}
.pb{{padding:10px}}
.pstats{{display:flex;gap:8px;font-size:12px;flex-wrap:wrap;color:var(--text-dim)}}
.psv{{font-weight:700;color:var(--text-hi)}}
.pdata{{font-size:11px;color:var(--text-faint);margin-top:3px;font-family:'JetBrains Mono',monospace}}
.pleg{{font-size:11px;color:var(--text-faint);margin-top:3px;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}}
.hist-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}}
.hist-card{{background:var(--ink-2);border-top:2px solid var(--line-3);border-bottom:1px solid var(--line-2);padding:20px}}
.heatmap-wrap{{overflow-x:auto;margin-bottom:24px}}
.heatmap{{display:grid;grid-template-columns:48px repeat(24,1fr);gap:2px;min-width:600px}}
.hm-lbl{{font-size:10px;color:var(--text-faint);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace}}
.hm-cell{{aspect-ratio:1;position:relative;cursor:default;min-width:16px}}
.hm-cell:hover .hm-tip{{display:block}}
.hm-tip{{display:none;position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);background:var(--ink-3);color:var(--text-hi);border:1px solid var(--line-2);padding:5px 8px;font-size:11px;white-space:nowrap;z-index:10;pointer-events:none;font-family:'JetBrains Mono',monospace}}
.freq-wrap{{background:var(--ink-2);border-top:2px solid var(--line-3);border-bottom:1px solid var(--line-2);padding:20px;margin-bottom:24px}}
.freq-bars{{display:flex;align-items:flex-end;gap:4px;height:120px;margin-top:12px}}
.freq-bar{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:2px;min-width:0;height:100%}}
.freq-bar-inner{{width:100%;transition:height .3s}}
.freq-bar-lbl{{font-size:9px;color:var(--text-faint);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;text-align:center;font-family:'JetBrains Mono',monospace}}
.freq-insight{{font-size:13px;color:var(--text-dim);margin-top:12px;line-height:1.5}}
.hash-wrap{{background:var(--ink-2);border-top:2px solid var(--line-3);border-bottom:1px solid var(--line-2);padding:20px;margin-bottom:24px}}
.hash-row{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}
.hash-tag{{font-size:12px;font-weight:600;min-width:120px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--text-hi);font-family:'JetBrains Mono',monospace}}
.hash-bar-wrap{{flex:1;height:20px;background:var(--ink-4);overflow:hidden}}
.hash-bar{{height:100%;background:var(--neon);transition:width .3s}}
.hash-stat{{font-size:11px;color:var(--text-faint);white-space:nowrap;min-width:100px;font-family:'JetBrains Mono',monospace}}
.cap-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:8px}}
.cap-card{{background:var(--ink-2);border-top:2px solid var(--neon);border-bottom:1px solid var(--line-2);padding:20px;text-align:center}}
.cap-label{{font-size:12px;color:var(--text-faint);margin-bottom:4px;font-family:'JetBrains Mono',monospace}}
.cap-val{{font-size:24px;font-weight:700;color:var(--neon)}}
.cap-count{{font-size:11px;color:var(--text-faint);margin-top:2px}}
.cap-insight{{font-size:13px;color:var(--text-dim);margin-bottom:24px;line-height:1.5}}
.var-wrap{{background:var(--ink-2);border-top:2px solid var(--line-3);border-bottom:1px solid var(--line-2);padding:20px;margin-bottom:24px}}
.var-post{{margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid var(--line-2)}}
.var-post:last-child{{margin-bottom:0;padding-bottom:0;border-bottom:none}}
.var-header{{display:flex;align-items:center;gap:12px;margin-bottom:12px}}
.var-thumb{{width:56px;height:56px;object-fit:cover;flex-shrink:0}}
.var-info{{flex:1}}
.var-info h4{{font-size:14px;font-weight:700;margin-bottom:2px;color:var(--text-hi)}}
.var-info .var-eng{{font-size:12px;color:var(--neon);font-weight:600}}
.var-chips{{display:flex;gap:6px;flex-wrap:wrap}}
.var-chip{{display:inline-block;padding:4px 10px;font-size:11px;font-weight:500;border:1px solid var(--line-3);color:var(--text-dim);font-family:'JetBrains Mono',monospace}}
.var-gancho{{font-size:12px;color:var(--text-faint);margin-top:4px;line-height:1.4}}
.filter-bar{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;align-items:center}}
.filter-group{{display:flex;gap:4px;align-items:center}}
.filter-group-lbl{{font-size:11px;color:var(--text-faint);font-weight:600;margin-right:4px;text-transform:uppercase;letter-spacing:.5px;font-family:'JetBrains Mono',monospace}}
.fbtn{{padding:5px 14px;border:1px solid var(--line-3);background:var(--ink-2);font-size:12px;font-weight:500;cursor:pointer;transition:all .15s;font-family:'Space Grotesk','Inter',sans-serif;color:var(--text-dim)}}
.fbtn:hover{{border-color:var(--neon);color:var(--neon)}}
.fbtn.active{{background:var(--neon);color:#000;border-color:var(--neon)}}
@media(max-width:768px){{
  .kpi-grid{{grid-template-columns:repeat(2,1fr)}}
  .fmt-grid,.top3-grid,.hist-grid,.cap-grid{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<div class="wrap">
  <div id="app"></div>
</div>
<script>
const D={dados_js};
let filterState={{type:'all',period:'all'}};

function fmt(n){{
  if(n===undefined||n===null||n<0)return'--';
  if(n>=1e6)return(n/1e6).toFixed(1)+'M';
  if(n>=1000)return(n/1000).toFixed(1)+'k';
  return n.toLocaleString('pt-BR');
}}
function bc(tipo){{return tipo==='Reel'?'br':tipo==='Carrossel'?'bc':'bf'}}
function dc(tipo){{return tipo==='Reel'?'dot-r':tipo==='Carrossel'?'dot-c':'dot-f'}}

function getFilteredPosts(){{
  let list=D.posts.slice();
  if(filterState.type!=='all'){{
    list=list.filter(p=>p.tipo===filterState.type);
  }}
  if(filterState.period!=='all'){{
    const days=parseInt(filterState.period,10);
    const cutoff=new Date();
    cutoff.setDate(cutoff.getDate()-days);
    list=list.filter(p=>{{
      if(!p.timestamp)return false;
      return new Date(p.timestamp)>=cutoff;
    }});
  }}
  list.sort((a,b)=>new Date(b.timestamp)-new Date(a.timestamp));
  return list;
}}

function recalcKPIs(posts){{
  const seg=D.perfil.seguidores||1;
  const total=posts.length;
  if(!total)return{{engMedio:0,totalShares:0,count:total}};
  const engMedio=Math.round(posts.reduce((s,p)=>s+p.engajamento,0)/total*100)/100;
  const totalShares=posts.reduce((s,p)=>s+(p.shares||0),0);
  return{{engMedio,totalShares,count:total}};
}}

function render(){{
  const{{perfil:p,posts,top3,postsCronologicos:crono,metricas:m,atualizadoEm}}=D;
  const fotoSrc=p.fotoPerfil?`data:image/jpeg;base64,${{p.fotoPerfil}}`:'';
  const avInner=fotoSrc?`<img src="${{fotoSrc}}" alt="">`:`${{(p.nome||p.username||'?')[0].toUpperCase()}}`;

  document.getElementById('app').innerHTML=`
  <div class="hdr">
    <div class="avatar">${{avInner}}</div>
    <div class="hinfo">
      <h1>${{p.nome||p.username}}${{p.verificado?' <svg style="display:inline-block;vertical-align:middle;margin-left:6px" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="10" cy="10" r="10" fill="#c4ff5e"/><path d="M6 10.5l2.5 2.5 5.5-5.5" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>':''}}</h1>
      <div class="un">@${{p.username}}</div>
      ${{p.bio?`<div class="bio">${{p.bio}}</div>`:''}}
      <div class="upd">Atualizado em ${{atualizadoEm}}</div>
    </div>
  </div>

  <div class="kpi-grid" id="kpiGrid">
    <div class="kpi"><div class="kpi-lbl">Seguidores</div><div class="kpi-val">${{fmt(p.seguidores)}}</div><div class="kpi-sub">${{fmt(p.seguindo)}} seguindo</div></div>
    <div class="kpi kpi-accent"><div class="kpi-lbl">Engajamento medio</div><div class="kpi-val" id="kpiEng">${{m.engMedio}}%</div><div class="kpi-sub">${{m.totalShares>0?fmt(m.totalShares)+' shares totais':'baseado em likes e comentarios'}}</div></div>
    <div class="kpi"><div class="kpi-lbl">Total de posts</div><div class="kpi-val" id="kpiCount">${{fmt(p.totalPosts)}}</div><div class="kpi-sub">no perfil</div></div>
    <div class="kpi"><div class="kpi-lbl">Formato mais postado</div><div class="kpi-val" style="font-size:22px">${{m.formatoTop}}</div><div class="kpi-sub">ultimos ${{posts.length}} posts</div></div>
  </div>

  <div id="historicoSection"></div>

  <div class="sec">Desempenho por Formato</div>
  <div class="fmt-grid">
    <div class="fmt-card">
      <div class="fmt-nome"><span class="dot dot-r"></span>Reels (${{m.reels.count}})</div>
      <div class="mets">
        <div><div class="met-lbl">Media de likes</div><div class="met-val">${{fmt(m.reels.mediaLikes)}}</div></div>
        <div><div class="met-lbl">Media comentarios</div><div class="met-val">${{fmt(m.reels.mediaComentarios)}}</div></div>
        <div><div class="met-lbl">Views totais</div><div class="met-val">${{fmt(m.reels.totalViews)}}</div></div>
        ${{m.reels.mediaShares>0?'<div><div class="met-lbl">Media de shares</div><div class="met-val">'+fmt(m.reels.mediaShares)+'</div></div>':''}}
      </div>
    </div>
    <div class="fmt-card">
      <div class="fmt-nome"><span class="dot dot-c"></span>Carrosseis (${{m.carrosseis.count}})</div>
      <div class="mets">
        <div><div class="met-lbl">Media de likes</div><div class="met-val">${{fmt(m.carrosseis.mediaLikes)}}</div></div>
        <div><div class="met-lbl">Media comentarios</div><div class="met-val">${{fmt(m.carrosseis.mediaComentarios)}}</div></div>
        ${{m.carrosseis.mediaShares>0?'<div><div class="met-lbl">Media de shares</div><div class="met-val">'+fmt(m.carrosseis.mediaShares)+'</div></div>':''}}
      </div>
    </div>
    <div class="fmt-card">
      <div class="fmt-nome"><span class="dot dot-f"></span>Fotos (${{m.fotos.count}})</div>
      <div class="mets">
        <div><div class="met-lbl">Media de likes</div><div class="met-val">${{fmt(m.fotos.mediaLikes)}}</div></div>
        <div><div class="met-lbl">Media comentarios</div><div class="met-val">${{fmt(m.fotos.mediaComentarios)}}</div></div>
        ${{m.fotos.mediaShares>0?'<div><div class="met-lbl">Media de shares</div><div class="met-val">'+fmt(m.fotos.mediaShares)+'</div></div>':''}}
      </div>
    </div>
  </div>

  <div id="heatmapSection"></div>
  <div id="frequencySection"></div>

  <div class="sec">Top 3 Posts</div>
  <div class="top3-grid" id="top3Grid">
    ${{top3.map(t=>`
    <div class="t3c">
      ${{t.imagem?`<img src="data:image/jpeg;base64,${{t.imagem}}" alt="">`:`<div class="t3ph">Sem imagem</div>`}}
      <div class="t3b">
        <span class="badge ${{bc(t.tipo)}}">${{t.tipo}}</span>
        <div class="t3stats">
          <span><span class="t3sv">${{fmt(t.likes)}}</span> likes</span>
          <span><span class="t3sv">${{fmt(t.comentarios)}}</span> com.</span>
          ${{t.tipo==='Reel'?`<span><span class="t3sv">${{fmt(t.views)}}</span> views</span>`:''}}
          <span><span class="t3sv">${{fmt(t.shares)}}</span> shares</span>
        </div>
        <div class="t3eng">${{t.engajamento}}% engajamento</div>
        ${{t.url?`<a class="vlink" href="${{t.url}}" target="_blank">Ver post original</a>`:''}}
      </div>
    </div>`).join('')}}
  </div>
  <div id="variacoesSection"></div>

  <div id="hashtagSection"></div>
  <div id="captionSection"></div>

  <div class="chart-card">
    <div class="sec" style="margin-bottom:12px">Linha do Tempo</div>
    <div class="ch-legend">
      <div class="leg"><div class="ldot" style="background:var(--reel)"></div>Reels</div>
      <div class="leg"><div class="ldot" style="background:var(--carrossel)"></div>Carrossel</div>
      <div class="leg"><div class="ldot" style="background:var(--foto)"></div>Foto</div>
    </div>
    <div class="ch-title">Curtidas</div>
    <div id="chartLikes" style="width:100%;height:160px"></div>
    <div class="ch-title" style="margin-top:20px">Visualizacoes (Reels)</div>
    <div id="chartViews" style="width:100%;height:110px"></div>
    <div class="ch-title" style="margin-top:20px">Engajamento (%)</div>
    <div id="chartEng" style="width:100%;height:110px"></div>
    ${{posts.some(p=>p.shares>0)?'<div class="ch-title" style="margin-top:20px">Compartilhamentos</div><div id="chartShares" style="width:100%;height:110px"></div>':''}}
  </div>

  <div id="filterBar"></div>
  <div class="sec" id="postsTitle">Todos os Posts (${{posts.length}})</div>
  <div class="pg" id="postsGrid"></div>
  `;

  renderFilterBar();
  renderPosts(posts);
  renderHistorico();
  renderHeatmap();
  renderFrequency();
  renderHashtags();
  renderCaptionAnalysis();
  renderVariacoes();
  setTimeout(renderRechartsTimeline,100);
}}

function renderFilterBar(){{
  const el=document.getElementById('filterBar');
  if(!el)return;
  el.innerHTML=`
  <div class="filter-bar">
    <div class="filter-group">
      <span class="filter-group-lbl">Tipo</span>
      <button class="fbtn ${{filterState.type==='all'?'active':''}}" data-ft="all">Todos</button>
      <button class="fbtn ${{filterState.type==='Reel'?'active':''}}" data-ft="Reel">Reel</button>
      <button class="fbtn ${{filterState.type==='Carrossel'?'active':''}}" data-ft="Carrossel">Carrossel</button>
      <button class="fbtn ${{filterState.type==='Foto'?'active':''}}" data-ft="Foto">Foto</button>
    </div>
    <div class="filter-group">
      <span class="filter-group-lbl">Periodo</span>
      <button class="fbtn ${{filterState.period==='all'?'active':''}}" data-fp="all">Todos</button>
      <button class="fbtn ${{filterState.period==='7'?'active':''}}" data-fp="7">7 dias</button>
      <button class="fbtn ${{filterState.period==='15'?'active':''}}" data-fp="15">15 dias</button>
      <button class="fbtn ${{filterState.period==='30'?'active':''}}" data-fp="30">30 dias</button>
    </div>
  </div>`;
  el.querySelectorAll('[data-ft]').forEach(btn=>{{
    btn.addEventListener('click',()=>{{
      filterState.type=btn.getAttribute('data-ft');
      applyFilters();
    }});
  }});
  el.querySelectorAll('[data-fp]').forEach(btn=>{{
    btn.addEventListener('click',()=>{{
      filterState.period=btn.getAttribute('data-fp');
      applyFilters();
    }});
  }});
}}

function applyFilters(){{
  const filtered=getFilteredPosts();
  const kpis=recalcKPIs(filtered);
  const kpiEng=document.getElementById('kpiEng');
  if(kpiEng)kpiEng.textContent=kpis.engMedio+'%';
  const title=document.getElementById('postsTitle');
  if(title)title.textContent='Todos os Posts ('+filtered.length+')';
  const grid=document.getElementById('postsGrid');
  if(grid)grid.innerHTML='';
  renderPosts(filtered);
  const top3Filtered=filtered.slice().sort((a,b)=>b.engajamento-a.engajamento).slice(0,3);
  const t3g=document.getElementById('top3Grid');
  if(t3g){{
    t3g.innerHTML=top3Filtered.map(t=>`
    <div class="t3c">
      ${{t.imagem?`<img src="data:image/jpeg;base64,${{t.imagem}}" alt="">`:`<div class="t3ph">Sem imagem</div>`}}
      <div class="t3b">
        <span class="badge ${{bc(t.tipo)}}">${{t.tipo}}</span>
        <div class="t3stats">
          <span><span class="t3sv">${{fmt(t.likes)}}</span> likes</span>
          <span><span class="t3sv">${{fmt(t.comentarios)}}</span> com.</span>
          ${{t.tipo==='Reel'?`<span><span class="t3sv">${{fmt(t.views)}}</span> views</span>`:''}}
          <span><span class="t3sv">${{fmt(t.shares)}}</span> shares</span>
        </div>
        <div class="t3eng">${{t.engajamento}}% engajamento</div>
        ${{t.url?`<a class="vlink" href="${{t.url}}" target="_blank">Ver post original</a>`:''}}
      </div>
    </div>`).join('');
  }}
  renderFilterBar();
}}

function renderPosts(posts){{
  const grid=document.getElementById('postsGrid');
  if(!grid)return;
  posts.forEach((post,idx)=>{{
    const div=document.createElement('div');
    div.className='pc';
    const allB64=[];
    if(post.imagem)allB64.push(post.imagem);
    (post.imagens||[]).forEach(b=>{{if(b)allB64.push(b)}});
    const multi=allB64.length>1;
    let cur=0;
    const uid='fp'+Math.random().toString(36).slice(2,8);
    div.innerHTML=`
    <div class="pw" id="pw${{uid}}">
      ${{allB64.length?`<img id="pimg${{uid}}" src="data:image/jpeg;base64,${{allB64[0]}}" alt="">`:`<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:11px;color:var(--muted)">Sem imagem</div>`}}
      ${{multi?`<span class="ci" id="pci${{uid}}">1/${{allB64.length}}</span>`:''}}
    </div>
    <div class="pb">
      <span class="badge ${{bc(post.tipo)}}">${{post.tipo}}</span>
      <div class="pstats">
        <span><span class="psv">${{fmt(post.likes)}}</span> likes</span>
        <span><span class="psv">${{fmt(post.comentarios)}}</span> com.</span>
        ${{post.tipo==='Reel'?`<span><span class="psv">${{fmt(post.views)}}</span> views</span>`:''}}
        <span><span class="psv">${{fmt(post.shares||0)}}</span> shares</span>
      </div>
      <div class="pdata">${{post.data||''}}</div>
      ${{post.legenda?`<div class="pleg">${{post.legenda.substring(0,120)}}</div>`:''}}
      ${{post.url?`<a class="vlink" href="${{post.url}}" target="_blank">Ver post original</a>`:''}}
    </div>`;
    if(multi){{
      div.querySelector('.pw').addEventListener('click',()=>{{
        cur=(cur+1)%allB64.length;
        document.getElementById('pimg'+uid).src='data:image/jpeg;base64,'+allB64[cur];
        document.getElementById('pci'+uid).textContent=(cur+1)+'/'+allB64.length;
      }});
    }}
    grid.appendChild(div);
  }});
}}

function renderHistorico(){{
  const el=document.getElementById('historicoSection');
  if(!el)return;
  const h=D.historico;
  if(!h||h.length<2)return;
  el.innerHTML=`
    <div class="sec">Evolucao Historica</div>
    <div class="hist-grid">
      <div class="hist-card">
        <div class="ch-title">Seguidores ao longo do tempo</div>
        <div id="chartHistSeg" style="width:100%;height:120px"></div>
      </div>
      <div class="hist-card">
        <div class="ch-title">Engajamento medio ao longo do tempo</div>
        <div id="chartHistEng" style="width:100%;height:120px"></div>
      </div>
    </div>`;
  setTimeout(renderRechartsHistorico,120);
}}


function renderHeatmap(){{
  const el=document.getElementById('heatmapSection');
  if(!el)return;
  const posts=D.posts;
  if(!posts.length)return;
  const dias=['Seg','Ter','Qua','Qui','Sex','Sab','Dom'];
  const grid=Array.from({{length:7}},()=>Array.from({{length:24}},()=>({{count:0,totalEng:0}})));
  posts.forEach(p=>{{
    if(!p.timestamp)return;
    const dt=new Date(p.timestamp);
    const day=(dt.getDay()+6)%7;
    const hour=dt.getHours();
    grid[day][hour].count++;
    grid[day][hour].totalEng+=p.engajamento||0;
  }});
  let maxAvg=0;
  grid.forEach(row=>row.forEach(cell=>{{
    if(cell.count>0){{
      const avg=cell.totalEng/cell.count;
      if(avg>maxAvg)maxAvg=avg;
    }}
  }}));
  if(!maxAvg)maxAvg=1;
  let html='<div class="sec">Melhores Horarios para Postar</div><div class="heatmap-wrap"><div class="heatmap">';
  html+='<div class="hm-lbl"></div>';
  for(let h=0;h<24;h++)html+=`<div class="hm-lbl">${{h}}</div>`;
  for(let d=0;d<7;d++){{
    html+=`<div class="hm-lbl">${{dias[d]}}</div>`;
    for(let h=0;h<24;h++){{
      const cell=grid[d][h];
      if(cell.count===0){{
        html+=`<div class="hm-cell" style="background:var(--accent-lt)"><div class="hm-tip">Nenhum post</div></div>`;
      }}else{{
        const avg=Math.round(cell.totalEng/cell.count*100)/100;
        const opacity=Math.max(0.15,avg/maxAvg);
        html+=`<div class="hm-cell" style="background:rgba(196,255,94,${{opacity.toFixed(2)}})"><div class="hm-tip">${{cell.count}} post${{cell.count>1?'s':''}} | ${{avg}}% eng</div></div>`;
      }}
    }}
  }}
  html+='</div></div>';
  el.innerHTML=html;
}}

function getISOWeek(d){{
  const dt=new Date(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate()));
  const dayNum=dt.getUTCDay()||7;
  dt.setUTCDate(dt.getUTCDate()+4-dayNum);
  const yearStart=new Date(Date.UTC(dt.getUTCFullYear(),0,1));
  return Math.ceil(((dt-yearStart)/86400000+1)/7);
}}

function renderFrequency(){{
  const el=document.getElementById('frequencySection');
  if(!el)return;
  const posts=D.posts.filter(p=>p.timestamp);
  if(!posts.length)return;
  const weeks={{}};
  posts.forEach(p=>{{
    const dt=new Date(p.timestamp);
    const yr=dt.getFullYear();
    const wk=getISOWeek(dt);
    const key=yr+'-W'+String(wk).padStart(2,'0');
    if(!weeks[key])weeks[key]={{count:0,totalEng:0,label:key}};
    weeks[key].count++;
    weeks[key].totalEng+=p.engajamento||0;
  }});
  const sorted=Object.values(weeks).sort((a,b)=>a.label.localeCompare(b.label));
  if(!sorted.length)return;
  const maxCount=Math.max(...sorted.map(w=>w.count),1);
  const highWeeks=sorted.filter(w=>w.count>=4);
  const lowWeeks=sorted.filter(w=>w.count<4);
  const avgHigh=highWeeks.length?Math.round(highWeeks.reduce((s,w)=>s+w.totalEng/w.count,0)/highWeeks.length*100)/100:0;
  const avgLow=lowWeeks.length?Math.round(lowWeeks.reduce((s,w)=>s+w.totalEng/w.count,0)/lowWeeks.length*100)/100:0;
  let bars=sorted.map(w=>{{
    const pct=Math.round(w.count/maxCount*100);
    const avg=w.count?Math.round(w.totalEng/w.count*100)/100:0;
    const shortLbl=w.label.split('-')[1];
    const px=Math.max(Math.round(pct/100*100),6);
    return`<div class="freq-bar"><div class="freq-bar-inner" style="height:${{px}}px;background:var(--accent)" title="${{w.count}} posts, ${{avg}}% eng"></div><div class="freq-bar-lbl">${{shortLbl}}</div></div>`;
  }}).join('');
  let insight='';
  if(highWeeks.length>0&&lowWeeks.length>0){{
    insight=`<div class="freq-insight">Semanas com 4+ posts: ${{avgHigh}}% engajamento medio vs ${{avgLow}}% com menos posts.</div>`;
  }}
  el.innerHTML=`<div class="freq-wrap"><div class="sec" style="margin-bottom:4px">Frequencia de Postagem</div><div class="freq-bars">${{bars}}</div>${{insight}}</div>`;
}}

function renderHashtags(){{
  const el=document.getElementById('hashtagSection');
  if(!el)return;
  const posts=D.posts;
  const tagMap={{}};
  posts.forEach(p=>{{
    const tags=(p.legenda||'').match(/#[\\w\\u00C0-\\u024F]+/g);
    if(!tags)return;
    tags.forEach(tag=>{{
      const t=tag.toLowerCase();
      if(!tagMap[t])tagMap[t]={{tag:t,totalEng:0,count:0}};
      tagMap[t].count++;
      tagMap[t].totalEng+=p.engajamento||0;
    }});
  }});
  const all=Object.values(tagMap).filter(t=>t.count>=1);
  if(!all.length){{
    el.innerHTML='<div class="hash-wrap"><div class="sec">Analise de Hashtags</div><div style="font-size:13px;color:var(--muted)">Nenhuma hashtag encontrada</div></div>';
    return;
  }}
  all.forEach(t=>t.avgEng=Math.round(t.totalEng/t.count*100)/100);
  const top10=all.sort((a,b)=>b.avgEng-a.avgEng).slice(0,10);
  const maxEng=top10[0].avgEng||1;
  const rows=top10.map(t=>{{
    const pct=Math.round(t.avgEng/maxEng*100);
    return`<div class="hash-row"><div class="hash-tag">${{t.tag}}</div><div class="hash-bar-wrap"><div class="hash-bar" style="width:${{pct}}%"></div></div><div class="hash-stat">${{t.avgEng}}% eng, ${{t.count}} post${{t.count>1?'s':''}}</div></div>`;
  }}).join('');
  el.innerHTML=`<div class="hash-wrap"><div class="sec">Analise de Hashtags (Top 10)</div>${{rows}}</div>`;
}}

function renderCaptionAnalysis(){{
  const el=document.getElementById('captionSection');
  if(!el)return;
  const posts=D.posts;
  const buckets={{curta:{{posts:[],label:'Curta (<100)'}},media:{{posts:[],label:'Media (100-300)'}},longa:{{posts:[],label:'Longa (300+)'}}}};
  posts.forEach(p=>{{
    const len=(p.legenda||'').length;
    if(len<100)buckets.curta.posts.push(p);
    else if(len<=300)buckets.media.posts.push(p);
    else buckets.longa.posts.push(p);
  }});
  const results=Object.entries(buckets).map(([k,v])=>{{
    const avg=v.posts.length?Math.round(v.posts.reduce((s,p)=>s+p.engajamento,0)/v.posts.length*100)/100:0;
    return{{key:k,label:v.label,avg,count:v.posts.length}};
  }});
  const withPosts=results.filter(r=>r.count>0);
  let insight='';
  if(withPosts.length>=2){{
    const best=withPosts.reduce((a,b)=>a.avg>b.avg?a:b);
    const worst=withPosts.reduce((a,b)=>a.avg<b.avg?a:b);
    if(best.key!==worst.key){{
      insight=`<div class="cap-insight">Legendas "${{best.label.split('(')[0].trim().toLowerCase()}}" tem ${{best.avg}}% de engajamento medio, contra ${{worst.avg}}% das "${{worst.label.split('(')[0].trim().toLowerCase()}}".</div>`;
    }}
  }}
  const cards=results.map(r=>`<div class="cap-card"><div class="cap-label">${{r.label}}</div><div class="cap-val">${{r.avg}}%</div><div class="cap-count">${{r.count}} post${{r.count!==1?'s':''}}</div></div>`).join('');
  el.innerHTML=`<div class="sec">Tamanho de Legenda vs Engajamento</div><div class="cap-grid">${{cards}}</div>${{insight}}`;
}}

function renderVariacoes(){{
  const el=document.getElementById('variacoesSection');
  if(!el||!D.variacoes||!D.variacoes.length)return;
  const postsMap={{}};
  D.posts.forEach(p=>{{postsMap[p.shortCode]=p;}});
  const items=D.variacoes.map(v=>{{
    const post=postsMap[v.shortCode];
    if(!post)return'';
    const thumbSrc=post.imagem?`data:image/jpeg;base64,${{post.imagem}}`:'';
    const thumbHtml=thumbSrc?`<img class="var-thumb" src="${{thumbSrc}}" alt="">`:
      `<div class="var-thumb" style="background:var(--accent-lt);display:flex;align-items:center;justify-content:center;font-size:11px;color:var(--muted)">${{post.tipo||'Post'}}</div>`;
    const caption=(post.legenda||'').substring(0,60);
    const chips=v.variacoes.map(vr=>
      `<div class="var-chip">${{vr.elemento}}</div>`
    ).join('');
    const ganchos=v.variacoes.map(vr=>
      `<div class="var-gancho"><strong>${{vr.elemento}}:</strong> "${{vr.gancho}}"</div>`
    ).join('');
    return`<div class="var-post">
      <div class="var-header">
        ${{thumbHtml}}
        <div class="var-info">
          <h4>${{caption}}...</h4>
          <div class="var-eng">${{v.engajamento}}% engajamento | ${{v.variacoes[0]?.formato||'Reels'}} | ${{v.variacoes[0]?.objetivo||''}}</div>
        </div>
      </div>
      <div class="var-chips">${{chips}}</div>
      ${{ganchos}}
    </div>`;
  }}).join('');
  if(!items)return;
  el.innerHTML=`<div class="var-wrap"><div class="sec">Variacoes de Conteudo</div>${{items}}</div>`;
}}

window.addEventListener('load',render);
</script>
<script>{recharts_js}</script>
</body>
</html>'''

# ── Download paralelo de imagens ─────────────────────────────────────────────
def _baixar_post_imgs(args):
    """Baixa thumbnail e slides de um post. Chamado em paralelo via ThreadPoolExecutor."""
    i, post, images_dir = args
    result = {'imagem': '', 'thumbnailPath': '', 'imagens': [], 'carouselPaths': []}

    b64 = baixar_b64(post['_displayUrl'], f'thumb post {i+1}')
    result['imagem'] = b64
    if b64:
        thumb_path = images_dir / f'post_{i+1:02d}_thumb.jpg'
        salvar_jpg(b64, thumb_path)
        result['thumbnailPath'] = f'imagens/post_{i+1:02d}_thumb.jpg'

    carousel_b64, carousel_paths = [], []
    for j, img_url in enumerate(post['_imgsUrl'][:10]):
        b = baixar_b64(img_url, f'slide {j+1} post {i+1}')
        if b:
            carousel_b64.append(b)
            sp = images_dir / f'post_{i+1:02d}_slide_{j+1:02d}.jpg'
            salvar_jpg(b, sp)
            carousel_paths.append(f'imagens/post_{i+1:02d}_slide_{j+1:02d}.jpg')
    result['imagens']       = carousel_b64
    result['carouselPaths'] = carousel_paths
    return i, result

# ── Concorrente meta.json helper ─────────────────────────────────────────────
def atualizar_meta_concorrente(conc_dir, slug: str, nome: str, plat: str, handle: str):
    """Cria ou atualiza meta.json com info do concorrente.
    `conc_dir` aponta para entregas/concorrentes/{slug}/ (Path)."""
    from datetime import datetime as _dt
    meta_path = conc_dir / 'meta.json'
    meta = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding='utf-8'))
        except Exception:
            meta = {}
    meta['slug'] = slug
    if nome and (not meta.get('nome') or meta.get('nome') == slug):
        meta['nome'] = nome
    meta['atualizado_em'] = _dt.now().strftime('%d/%m/%Y %H:%M')
    handles = meta.get('handles', {})
    handles[plat] = handle
    meta['handles'] = handles
    plats = meta.get('plataformas', [])
    if plat not in plats:
        plats.append(plat)
    meta['plataformas'] = plats
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--abrir', action='store_true')
    parser.add_argument('--usuario', help='Handle Instagram (substitui IG_USER do .env)')
    parser.add_argument('--concorrente', help='Slug do concorrente. Salva em entregas/concorrentes/{slug}/instagram/')
    parser.add_argument('--nome-bonito', dest='nome_bonito', help='Nome do concorrente para exibir no painel')
    args = parser.parse_args()

    env = ler_env()
    token   = env.get('APIFY_API_TOKEN', '')
    ig_user = args.usuario or env.get('IG_USER', '')

    # Resolver caminhos de output: meu vs concorrente
    if args.concorrente:
        ativo_file = PROJECT_ROOT / 'meus-produtos' / '.ativo'
        if not ativo_file.exists():
            print('ERRO: meus-produtos/.ativo nao encontrado.'); sys.exit(1)
        ativo = ativo_file.read_text(encoding='utf-8').strip()
        if not ativo:
            print('ERRO: meus-produtos/.ativo esta vazio.'); sys.exit(1)
        if not ig_user:
            print('ERRO: --usuario obrigatorio quando usar --concorrente.'); sys.exit(1)
        conc_root = PROJECT_ROOT / 'meus-produtos' / ativo / 'entregas' / 'concorrentes' / args.concorrente
        output_dir = conc_root / 'instagram'
        base_dir   = output_dir  # historico fica isolado dentro da pasta do concorrente
        # Sanity check: nunca deixar passar caminho fora de entregas/concorrentes
        assert 'entregas' in output_dir.parts and 'concorrentes' in output_dir.parts, \
            f'ERRO interno: caminho de concorrente invalido: {output_dir}'
    else:
        base_dir   = get_output_dir()
        output_dir = base_dir / ig_user if ig_user else base_dir

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

    # Imagens — download paralelo (5 workers, CDN do Instagram suporta sem rate limit)
    log.info(f'Baixando imagens de {len(posts)} posts em paralelo...')
    args_list = [(i, post, images_dir) for i, post in enumerate(posts)]
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(_baixar_post_imgs, a): a[0] for a in args_list}
        for future in as_completed(futures):
            i, result = future.result()
            posts[i].update(result)
            log.info(f'  Post {i+1}/{len(posts)} concluido')

    # Preservar transcricoes do insights.json anterior (geradas pelo /copy-variacao-post)
    transcricoes_prev = {}
    if insights_file.exists():
        try:
            prev = json.loads(insights_file.read_text(encoding='utf-8'))
            for p in prev.get('posts', []):
                sc = p.get('shortCode', '')
                tr = p.get('transcricao', '')
                if sc and tr:
                    transcricoes_prev[sc] = tr
            if transcricoes_prev:
                log.info(f'Preservando {len(transcricoes_prev)} transcricao(oes) do insights.json anterior')
        except Exception:
            pass

    # Metricas (antes do insights.json para engajamento estar calculado)
    metricas = calcular_metricas(perfil, posts)

    # insights.json (sem base64)
    def slim(p):
        s = {k: v for k, v in p.items() if k not in ('imagem', 'imagens') and not k.startswith('_')}
        # Restaurar transcricao anterior se existir e a nova estiver vazia
        sc = s.get('shortCode', '')
        if sc and not s.get('transcricao') and sc in transcricoes_prev:
            s['transcricao'] = transcricoes_prev[sc]
        return s
    insights = {
        'perfil':       {k: v for k, v in perfil.items() if not k.startswith('_') and k != 'fotoPerfil'},
        'posts':        [slim(p) for p in posts],
        'atualizadoEm': datetime.now().isoformat(),
    }
    insights_file.write_text(json.dumps(insights, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    log.info('insights.json salvo')
    historico = atualizar_historico(base_dir, perfil, metricas)

    # Variacoes (se existir variacoes.json na mesma pasta)
    variacoes_file = output_dir / 'variacoes.json'
    variacoes = []
    if variacoes_file.exists():
        try:
            variacoes = json.loads(variacoes_file.read_text(encoding='utf-8'))
            if not isinstance(variacoes, list):
                variacoes = []
        except Exception:
            variacoes = []

    # dashboard.html
    log.info('Gerando dashboard.html...')
    html = gerar_html(perfil, posts, metricas, historico, variacoes)
    dashboard_file.write_text(html, encoding='utf-8')
    log.info(f'dashboard.html salvo: {dashboard_file}')

    # Se for concorrente, atualiza meta.json
    if args.concorrente:
        atualizar_meta_concorrente(
            conc_root,
            args.concorrente,
            args.nome_bonito or args.concorrente,
            'instagram',
            ig_user,
        )
        log.info(f'meta.json do concorrente atualizado: {conc_root}/meta.json')

    log.info('=== Concluido com sucesso ===')

    if args.abrir:
        webbrowser.open(dashboard_file.as_uri())
        log.info('Dashboard aberto no navegador')

if __name__ == '__main__':
    main()
