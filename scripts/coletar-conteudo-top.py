#!/usr/bin/env python3
"""Coleta posts (caption, tipo, engajamento) dos top performers para analise estrategica."""
import json
import sys
import time
import logging
from pathlib import Path
from datetime import datetime, timezone

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / '.env'

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

PERFIS = [
    'ramsesgobbi',
    'karinabonadiu',
    'leidaatracao',
    'dra.proton',
    'bethrusso',
    'monicatavaresoficial',
    'gustavo.espiritismo',
]

def ler_env():
    env = {}
    for ln in ENV_FILE.read_text(encoding='utf-8').splitlines():
        ln = ln.strip()
        if not ln or ln.startswith('#') or '=' not in ln:
            continue
        k, _, v = ln.partition('=')
        env[k.strip()] = v.strip()
    return env

def headers(cookies, referer):
    return {
        'User-Agent': UA,
        'X-IG-App-ID': IG_APP_ID,
        'Cookie': '; '.join(f'{k}={v}' for k, v in cookies.items()),
        'Referer': referer,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9',
    }

def tipo_post(item):
    mt = item.get('media_type')
    if mt == 2:
        return 'Reel'
    if mt == 8:
        return 'Carrossel'
    return 'Foto'

def coletar(cookies, username, n=15):
    log.info(f'@{username}: buscando perfil...')
    r = requests.get(WEB_PROFILE_URL, params={'username': username},
                     headers=headers(cookies, f'https://www.instagram.com/{username}/'),
                     timeout=60)
    r.raise_for_status()
    user = r.json().get('data', {}).get('user') or {}
    user_id = user.get('id') or user.get('pk')
    seguidores = (user.get('edge_followed_by') or {}).get('count', 0)

    log.info(f'@{username}: buscando posts (alvo {n})...')
    items = []
    max_id = None
    while len(items) < n:
        params = {'count': 12}
        if max_id:
            params['max_id'] = max_id
        r2 = requests.get(FEED_USER_URL.format(user_id=user_id),
                          params=params,
                          headers=headers(cookies, f'https://www.instagram.com/{username}/'),
                          timeout=60)
        r2.raise_for_status()
        d = r2.json()
        novos = d.get('items', []) or []
        if not novos:
            break
        items.extend(novos)
        if not d.get('more_available'):
            break
        max_id = d.get('next_max_id')
        if not max_id:
            break
        time.sleep(0.5)
    items = items[:n]

    posts = []
    for it in items:
        cap = (it.get('caption') or {})
        caption_text = cap.get('text', '') if isinstance(cap, dict) else ''
        ts = it.get('taken_at') or 0
        data_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d') if ts else ''
        likes = it.get('like_count') or 0
        com   = it.get('comment_count') or 0
        views = it.get('play_count') or 0
        eng = round((likes + com) / max(seguidores, 1) * 100, 3)
        posts.append({
            'code': it.get('code'),
            'url': f'https://instagram.com/p/{it.get("code")}/' if it.get('code') else '',
            'tipo': tipo_post(it),
            'data': data_str,
            'likes': likes,
            'comentarios': com,
            'views': views,
            'engajamento': eng,
            'caption': caption_text,
        })
    return {
        'username': username,
        'seguidores': seguidores,
        'posts': posts,
    }

def main():
    env = ler_env()
    cookies = {
        'sessionid':  env.get('IG_COOKIE_SESSIONID', '').strip(),
        'ds_user_id': env.get('IG_COOKIE_DS_USER_ID', '').strip(),
        'csrftoken':  env.get('IG_COOKIE_CSRFTOKEN', '').strip(),
    }
    if not cookies['sessionid']:
        log.error('cookies IG_COOKIE_* nao encontrados no .env'); sys.exit(1)

    ativo = (PROJECT_ROOT / 'meus-produtos' / '.ativo').read_text(encoding='utf-8').strip()
    out_dir = PROJECT_ROOT / 'meus-produtos' / ativo / 'entregas' / 'dados' / 'concorrentes-IG'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'conteudo-top-performers.json'

    resultado = {'gerado_em': datetime.now().isoformat(), 'perfis': []}
    for u in PERFIS:
        try:
            r = coletar(cookies, u, n=15)
            resultado['perfis'].append(r)
            log.info(f'@{u}: {len(r["posts"])} posts coletados')
            time.sleep(2)
        except Exception as e:
            log.error(f'@{u} erro: {e}')
            resultado['perfis'].append({'username': u, 'erro': str(e)})

    out_file.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding='utf-8')
    log.info(f'salvo: {out_file}')

if __name__ == '__main__':
    main()
