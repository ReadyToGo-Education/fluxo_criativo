#!/usr/bin/env python3
"""
Workshop Inteligente - Instagram Dashboard via Web API com cookies de sessao
Usado quando os scrapers do Apify estao bloqueados pelo Instagram.
Le cookies do .env (IG_COOKIE_SESSIONID, IG_COOKIE_DS_USER_ID, IG_COOKIE_CSRFTOKEN)
e chama a API web do Instagram diretamente. Reaproveita helpers de atualizar.py.
"""

import os
import sys
import json
import time
import logging
import argparse
import webbrowser
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from atualizar import (
    PROJECT_ROOT, ler_env, get_output_dir,
    normalizar_perfil, normalizar_post, calcular_metricas,
    atualizar_historico, gerar_html, baixar_b64, _baixar_post_imgs,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

WEB_PROFILE_URL = 'https://i.instagram.com/api/v1/users/web_profile_info/'
FEED_USER_URL   = 'https://www.instagram.com/api/v1/feed/user/{user_id}/'

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
IG_APP_ID = '936619743392459'

def montar_headers(cookies, referer):
    cookie_str = '; '.join(f'{k}={v}' for k, v in cookies.items())
    return {
        'User-Agent': UA,
        'X-IG-App-ID': IG_APP_ID,
        'Cookie': cookie_str,
        'Referer': referer,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
    }

def buscar_perfil_web(cookies, ig_user):
    log.info(f'Buscando perfil via web API @{ig_user}...')
    resp = requests.get(
        WEB_PROFILE_URL,
        params={'username': ig_user},
        headers=montar_headers(cookies, f'https://www.instagram.com/{ig_user}/'),
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    user = data.get('data', {}).get('user') or {}
    if not user:
        raise RuntimeError('API do Instagram nao retornou dados do usuario')
    return user

def buscar_posts_web(cookies, ig_user, user_id, alvo=30):
    log.info(f'Buscando posts via feed/user (alvo {alvo})...')
    items = []
    max_id = None
    referer = f'https://www.instagram.com/{ig_user}/'
    pagina = 0
    while len(items) < alvo and pagina < 5:
        pagina += 1
        params = {'count': 12}
        if max_id:
            params['max_id'] = max_id
        resp = requests.get(
            FEED_USER_URL.format(user_id=user_id),
            params=params,
            headers=montar_headers(cookies, referer),
            timeout=60,
        )
        resp.raise_for_status()
        d = resp.json()
        novos = d.get('items', []) or []
        log.info(f'  Pagina {pagina}: {len(novos)} posts')
        if not novos:
            break
        items.extend(novos)
        if not d.get('more_available'):
            break
        max_id = d.get('next_max_id')
        if not max_id:
            break
        time.sleep(1)
    return items[:alvo]

def adaptar_perfil(raw_user):
    """Mapeia resposta web_profile_info para o formato Apify-like
    que `normalizar_perfil` espera."""
    return {
        'username':       raw_user.get('username', ''),
        'fullName':       raw_user.get('full_name', ''),
        'biography':      raw_user.get('biography', '') or '',
        'followersCount': (raw_user.get('edge_followed_by') or {}).get('count', 0),
        'followsCount':   (raw_user.get('edge_follow') or {}).get('count', 0),
        'postsCount':     (raw_user.get('edge_owner_to_timeline_media') or {}).get('count', 0),
        'verified':       bool(raw_user.get('is_verified')),
        'profilePicUrl':  raw_user.get('profile_pic_url_hd') or raw_user.get('profile_pic_url') or '',
    }

def melhor_imagem(versoes):
    if not versoes or not isinstance(versoes, list):
        return ''
    candidatos = [v for v in versoes if isinstance(v, dict) and v.get('url')]
    if not candidatos:
        return ''
    candidatos.sort(key=lambda v: (v.get('width', 0) or 0) * (v.get('height', 0) or 0), reverse=True)
    return candidatos[0].get('url', '')

def melhor_video(versoes):
    if not versoes or not isinstance(versoes, list):
        return ''
    candidatos = [v for v in versoes if isinstance(v, dict) and v.get('url')]
    if not candidatos:
        return ''
    candidatos.sort(key=lambda v: (v.get('width', 0) or 0) * (v.get('height', 0) or 0), reverse=True)
    return candidatos[0].get('url', '')

def adaptar_post(item):
    """Mapeia post da API feed/user para o formato Apify-like
    que `normalizar_post` espera."""
    media_type = item.get('media_type')
    is_video = (media_type == 2)
    is_carousel = (media_type == 8)
    tipo_str = 'video' if is_video else ('carousel' if is_carousel else 'image')

    likes = item.get('like_count')
    if likes is None:
        likes = -1

    cap_obj = item.get('caption') or {}
    caption_text = cap_obj.get('text', '') if isinstance(cap_obj, dict) else ''

    ts = item.get('taken_at') or 0
    timestamp_iso = ''
    if ts:
        try:
            timestamp_iso = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace('+00:00', 'Z')
        except Exception:
            timestamp_iso = ''

    display_url = ''
    video_url = ''
    child_posts = []

    if is_carousel:
        carousel = item.get('carousel_media') or []
        for cm in carousel:
            cm_type = cm.get('media_type')
            url_img = melhor_imagem((cm.get('image_versions2') or {}).get('candidates') or [])
            if cm_type == 2 and not url_img:
                url_img = melhor_imagem((cm.get('image_versions2') or {}).get('candidates') or [])
            if url_img:
                child_posts.append({'displayUrl': url_img})
        if child_posts:
            display_url = child_posts[0]['displayUrl']
    else:
        display_url = melhor_imagem((item.get('image_versions2') or {}).get('candidates') or [])
        if is_video:
            video_url = melhor_video(item.get('video_versions') or [])

    sc = item.get('code', '')
    raw = {
        'shortCode':       sc,
        'shortcode':       sc,
        'timestamp':       timestamp_iso,
        'likesCount':      likes,
        'commentsCount':   item.get('comment_count', 0) or 0,
        'videoViewCount':  item.get('play_count') or 0,
        'videoPlayCount':  item.get('play_count') or 0,
        'sharesCount':     0,
        'caption':         caption_text,
        'url':             f'https://www.instagram.com/p/{sc}/' if sc else '',
        'displayUrl':      display_url or '',
        'videoUrl':        video_url or '',
        'type':            tipo_str,
        'productType':     tipo_str,
        'isVideo':         bool(is_video),
    }
    if child_posts:
        raw['childPosts'] = child_posts
    return raw

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--abrir', action='store_true')
    args = parser.parse_args()

    base_dir = get_output_dir()
    env = ler_env()
    ig_user = env.get('IG_USER', '').strip()
    cookies = {
        'sessionid':  env.get('IG_COOKIE_SESSIONID', '').strip(),
        'ds_user_id': env.get('IG_COOKIE_DS_USER_ID', '').strip(),
        'csrftoken':  env.get('IG_COOKIE_CSRFTOKEN', '').strip(),
    }

    output_dir     = base_dir / ig_user if ig_user else base_dir
    images_dir     = output_dir / 'imagens'
    log_file       = output_dir / 'log.txt'
    insights_file  = output_dir / 'insights.json'
    dashboard_file = output_dir / 'dashboard.html'
    images_dir.mkdir(parents=True, exist_ok=True)

    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logging.getLogger().addHandler(fh)

    log.info('=== Instagram Dashboard via cookies ===')
    log.info(f'Output: {output_dir}')

    if not ig_user:
        log.error('IG_USER nao encontrado no .env'); sys.exit(1)
    if not cookies['sessionid']:
        log.error('IG_COOKIE_SESSIONID nao encontrado no .env'); sys.exit(1)
    if not cookies['ds_user_id']:
        log.error('IG_COOKIE_DS_USER_ID nao encontrado no .env'); sys.exit(1)
    if not cookies['csrftoken']:
        log.error('IG_COOKIE_CSRFTOKEN nao encontrado no .env'); sys.exit(1)

    log.info(f'Perfil: @{ig_user}')

    raw_user = buscar_perfil_web(cookies, ig_user)
    user_id  = raw_user.get('id') or raw_user.get('pk') or ''
    if not user_id:
        log.error('user_id nao encontrado na resposta do perfil'); sys.exit(1)

    raw_perfil = adaptar_perfil(raw_user)
    perfil = normalizar_perfil(raw_perfil)
    log.info(f'Perfil ok: {perfil["seguidores"]} seguidores, {perfil["totalPosts"]} posts')

    log.info('Baixando foto de perfil...')
    perfil['fotoPerfil'] = baixar_b64(perfil['_picUrl'], 'foto de perfil')

    items = buscar_posts_web(cookies, ig_user, user_id, alvo=30)
    log.info(f'{len(items)} posts coletados')

    raw_posts = [adaptar_post(it) for it in items]
    posts = [normalizar_post(r) for r in raw_posts]

    log.info(f'Baixando imagens de {len(posts)} posts em paralelo...')
    args_list = [(i, post, images_dir) for i, post in enumerate(posts)]
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(_baixar_post_imgs, a): a[0] for a in args_list}
        for future in as_completed(futures):
            i, result = future.result()
            posts[i].update(result)
            log.info(f'  Post {i+1}/{len(posts)} concluido')

    transcricoes_prev = {}
    if insights_file.exists():
        try:
            prev = json.loads(insights_file.read_text(encoding='utf-8'))
            for p in prev.get('posts', []):
                sc = p.get('shortCode', '')
                tr = p.get('transcricao', '')
                if sc and tr:
                    transcricoes_prev[sc] = tr
        except Exception:
            pass

    metricas = calcular_metricas(perfil, posts)

    def slim(p):
        s = {k: v for k, v in p.items() if k not in ('imagem', 'imagens') and not k.startswith('_')}
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

    variacoes_file = output_dir / 'variacoes.json'
    variacoes = []
    if variacoes_file.exists():
        try:
            variacoes = json.loads(variacoes_file.read_text(encoding='utf-8'))
            if not isinstance(variacoes, list):
                variacoes = []
        except Exception:
            variacoes = []

    log.info('Gerando dashboard.html...')
    html = gerar_html(perfil, posts, metricas, historico, variacoes)
    dashboard_file.write_text(html, encoding='utf-8')
    log.info(f'dashboard.html salvo: {dashboard_file}')

    log.info('=== Concluido com sucesso ===')

    if args.abrir:
        webbrowser.open(dashboard_file.as_uri())
        log.info('Dashboard aberto no navegador')

if __name__ == '__main__':
    main()
