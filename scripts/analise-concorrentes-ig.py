#!/usr/bin/env python3
"""
Analise de concorrentes no Instagram via Web API com cookies.
Le IG_COOKIE_* do .env, busca perfil + ate 30 posts de cada username,
calcula engajamento, formato dominante e frequencia de postagem.
Salva snapshot JSON e relatorio markdown em entregas/dados/concorrentes-IG/.
"""

import os
import sys
import json
import time
import argparse
import logging
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean, median

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
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

def ler_env():
    env = {}
    if ENV_FILE.exists():
        for ln in ENV_FILE.read_text(encoding='utf-8').splitlines():
            ln = ln.strip()
            if not ln or ln.startswith('#') or '=' not in ln:
                continue
            k, _, v = ln.partition('=')
            env[k.strip()] = v.strip()
    return env

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

def buscar_perfil(cookies, username):
    resp = requests.get(
        WEB_PROFILE_URL,
        params={'username': username},
        headers=montar_headers(cookies, f'https://www.instagram.com/{username}/'),
        timeout=60,
    )
    resp.raise_for_status()
    user = (resp.json().get('data') or {}).get('user') or {}
    if not user:
        raise RuntimeError(f'Perfil @{username} sem dados')
    return user

def buscar_posts(cookies, username, user_id, alvo=30):
    items = []
    max_id = None
    referer = f'https://www.instagram.com/{username}/'
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

def tipo_post(item):
    mt = item.get('media_type')
    if mt == 2:
        return 'Reel'
    if mt == 8:
        return 'Carrossel'
    return 'Foto'

def analisar(cookies, username):
    log.info(f'Coletando @{username}...')
    user = buscar_perfil(cookies, username)
    user_id = user.get('id') or user.get('pk')
    nome = user.get('full_name', '')
    bio = (user.get('biography') or '').strip()
    seguidores = (user.get('edge_followed_by') or {}).get('count', 0)
    seguindo = (user.get('edge_follow') or {}).get('count', 0)
    total_posts = (user.get('edge_owner_to_timeline_media') or {}).get('count', 0)
    is_private = bool(user.get('is_private'))
    is_verified = bool(user.get('is_verified'))

    posts = []
    if not is_private:
        try:
            time.sleep(1)
            raw = buscar_posts(cookies, username, user_id, alvo=30)
            for it in raw:
                posts.append({
                    'tipo': tipo_post(it),
                    'likes': it.get('like_count') or 0,
                    'comentarios': it.get('comment_count') or 0,
                    'views': it.get('play_count') or 0,
                    'taken_at': it.get('taken_at') or 0,
                    'code': it.get('code'),
                })
        except Exception as e:
            log.warning(f'  Falha ao puxar posts: {e}')

    engajamentos = []
    likes_l = []
    com_l = []
    views_l = []
    tipos = {'Reel': 0, 'Carrossel': 0, 'Foto': 0}
    timestamps = []
    for p in posts:
        likes = max(p['likes'], 0)
        com = p['comentarios']
        likes_l.append(likes)
        com_l.append(com)
        if p['views']:
            views_l.append(p['views'])
        tipos[p['tipo']] = tipos.get(p['tipo'], 0) + 1
        if seguidores > 0:
            engajamentos.append((likes + com) / seguidores * 100)
        if p['taken_at']:
            timestamps.append(p['taken_at'])

    eng_medio = round(mean(engajamentos), 3) if engajamentos else 0
    eng_mediana = round(median(engajamentos), 3) if engajamentos else 0
    likes_medio = round(mean(likes_l), 1) if likes_l else 0
    com_medio = round(mean(com_l), 1) if com_l else 0
    views_medio = round(mean(views_l), 1) if views_l else 0

    formato_top = max(tipos, key=tipos.get) if posts else '-'

    freq_semana = 0
    periodo_dias = 0
    primeiro = ''
    ultimo = ''
    if timestamps:
        ts_max = max(timestamps)
        ts_min = min(timestamps)
        periodo_dias = max((ts_max - ts_min) / 86400, 1)
        freq_semana = round(len(timestamps) / periodo_dias * 7, 2)
        primeiro = datetime.fromtimestamp(ts_min, tz=timezone.utc).strftime('%Y-%m-%d')
        ultimo = datetime.fromtimestamp(ts_max, tz=timezone.utc).strftime('%Y-%m-%d')

    dias_desde_ultimo = ''
    if timestamps:
        agora = datetime.now(tz=timezone.utc).timestamp()
        dias_desde_ultimo = round((agora - max(timestamps)) / 86400, 1)

    return {
        'username': username,
        'nome': nome,
        'bio': bio,
        'verificado': is_verified,
        'privado': is_private,
        'seguidores': seguidores,
        'seguindo': seguindo,
        'total_posts': total_posts,
        'posts_coletados': len(posts),
        'tipos': tipos,
        'formato_dominante': formato_top,
        'eng_medio_pct': eng_medio,
        'eng_mediana_pct': eng_mediana,
        'likes_medio': likes_medio,
        'comentarios_medio': com_medio,
        'views_medio': views_medio,
        'freq_post_por_semana': freq_semana,
        'periodo_amostra_dias': round(periodo_dias, 1),
        'primeiro_post_amostra': primeiro,
        'ultimo_post_amostra': ultimo,
        'dias_desde_ultimo_post': dias_desde_ultimo,
    }

def get_output_dir():
    ativo_file = PROJECT_ROOT / 'meus-produtos' / '.ativo'
    if not ativo_file.exists():
        log.error('meus-produtos/.ativo nao encontrado')
        sys.exit(1)
    slug = ativo_file.read_text(encoding='utf-8').strip()
    out = PROJECT_ROOT / 'meus-produtos' / slug / 'entregas' / 'dados' / 'concorrentes-IG'
    out.mkdir(parents=True, exist_ok=True)
    return out

def gerar_relatorio_md(snapshot, ranking_eng, ranking_seg, output_dir):
    data = datetime.now().strftime('%Y-%m-%d %H:%M')
    md = []
    md.append(f'# Análise de concorrentes Instagram — {data}\n')
    md.append(f'Snapshot inicial. Crescimento de seguidores fica disponível quando o script for rodado uma segunda vez (a partir do mesmo arquivo de histórico).\n')

    md.append('## Tabela comparativa\n')
    md.append('| # | Perfil | Seguidores | Posts no perfil | Posts amostra | Engajamento médio | Formato dominante | Posts por semana | Último post |')
    md.append('|---|---|---|---|---|---|---|---|---|')
    for i, p in enumerate(ranking_eng, 1):
        md.append(
            f'| {i} | [@{p["username"]}](https://instagram.com/{p["username"]}) '
            f'| {p["seguidores"]:,} | {p["total_posts"]:,} | {p["posts_coletados"]} '
            f'| {p["eng_medio_pct"]}% | {p["formato_dominante"]} '
            f'| {p["freq_post_por_semana"]} | há {p["dias_desde_ultimo_post"]}d |'
        )
    md.append('\n*Tabela ordenada por engajamento médio.*\n')

    md.append('## Ranking por seguidores\n')
    for i, p in enumerate(ranking_seg, 1):
        md.append(f'{i}. [@{p["username"]}](https://instagram.com/{p["username"]}) — {p["seguidores"]:,} seguidores — {p["nome"]}')
    md.append('')

    md.append('## Ranking por engajamento médio\n')
    for i, p in enumerate(ranking_eng, 1):
        md.append(f'{i}. [@{p["username"]}](https://instagram.com/{p["username"]}) — {p["eng_medio_pct"]}% — {p["seguidores"]:,} seguidores')
    md.append('')

    md.append('## Detalhe por perfil\n')
    for p in ranking_seg:
        md.append(f'### [@{p["username"]}](https://instagram.com/{p["username"]})')
        md.append(f'**Nome:** {p["nome"] or "-"}  ')
        if p['bio']:
            bio_short = p['bio'].replace('\n', ' ').replace('|', ' ')[:300]
            md.append(f'**Bio:** {bio_short}  ')
        md.append(f'**Verificado:** {"Sim" if p["verificado"] else "Não"} · **Privado:** {"Sim" if p["privado"] else "Não"}  ')
        md.append(f'**Seguidores:** {p["seguidores"]:,} · **Seguindo:** {p["seguindo"]:,} · **Posts no perfil:** {p["total_posts"]:,}  ')
        md.append(f'**Engajamento médio (amostra):** {p["eng_medio_pct"]}% · **mediana:** {p["eng_mediana_pct"]}%  ')
        md.append(f'**Likes médios:** {p["likes_medio"]:,} · **Comentários médios:** {p["comentarios_medio"]:,} · **Views médios (Reels):** {p["views_medio"]:,}  ')
        md.append(f'**Formato dominante:** {p["formato_dominante"]} (Reels: {p["tipos"].get("Reel",0)}, Carrosséis: {p["tipos"].get("Carrossel",0)}, Fotos: {p["tipos"].get("Foto",0)})  ')
        md.append(f'**Frequência de postagem (na amostra):** {p["freq_post_por_semana"]} posts/semana  ')
        md.append(f'**Período da amostra:** {p["primeiro_post_amostra"]} a {p["ultimo_post_amostra"]} ({p["periodo_amostra_dias"]} dias)  ')
        md.append(f'**Último post:** há {p["dias_desde_ultimo_post"]} dias  ')
        md.append('')

    return '\n'.join(md)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--usernames', nargs='+', required=True, help='Lista de usernames')
    args = parser.parse_args()

    env = ler_env()
    cookies = {
        'sessionid':  env.get('IG_COOKIE_SESSIONID', '').strip(),
        'ds_user_id': env.get('IG_COOKIE_DS_USER_ID', '').strip(),
        'csrftoken':  env.get('IG_COOKIE_CSRFTOKEN', '').strip(),
    }
    if not cookies['sessionid']:
        log.error('IG_COOKIE_SESSIONID nao encontrado no .env'); sys.exit(1)

    output_dir = get_output_dir()

    resultados = []
    for u in args.usernames:
        u = u.strip().lstrip('@')
        try:
            r = analisar(cookies, u)
            resultados.append(r)
            log.info(f'  @{u}: {r["seguidores"]:,} seg., eng {r["eng_medio_pct"]}%, formato {r["formato_dominante"]}')
            time.sleep(2)
        except requests.exceptions.HTTPError as e:
            log.error(f'  @{u} HTTP {e.response.status_code if e.response else "?"}: {e}')
            resultados.append({'username': u, 'erro': f'HTTP {e.response.status_code if e.response else "?"}'})
        except Exception as e:
            log.error(f'  @{u} erro: {e}')
            resultados.append({'username': u, 'erro': str(e)})

    snapshot_file = output_dir / 'snapshot.json'
    historico_file = output_dir / 'historico.json'
    relatorio_file = output_dir / f'concorrentes-{datetime.now().strftime("%Y-%m-%d")}.md'

    snapshot = {
        'gerado_em': datetime.now().isoformat(),
        'perfis': resultados,
    }
    snapshot_file.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
    log.info(f'snapshot salvo: {snapshot_file}')

    if historico_file.exists():
        try:
            hist = json.loads(historico_file.read_text(encoding='utf-8'))
        except Exception:
            hist = []
    else:
        hist = []
    hist.append({
        'data': datetime.now().isoformat(),
        'perfis': [{'username': p['username'], 'seguidores': p.get('seguidores', 0)} for p in resultados],
    })
    historico_file.write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding='utf-8')

    ok = [p for p in resultados if 'erro' not in p]
    rank_seg = sorted(ok, key=lambda x: x['seguidores'], reverse=True)
    rank_eng = sorted(ok, key=lambda x: x['eng_medio_pct'], reverse=True)
    md = gerar_relatorio_md(snapshot, rank_eng, rank_seg, output_dir)
    relatorio_file.write_text(md, encoding='utf-8')
    log.info(f'relatorio salvo: {relatorio_file}')

if __name__ == '__main__':
    main()
