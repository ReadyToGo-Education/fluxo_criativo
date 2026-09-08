#!/usr/bin/env python3
"""
Workshop Inteligente - Transcricao de Reels para copy-variacao-post
Transcreve o audio de Reels via tictechid~anoxvanzi-transcriber (Apify).
Atualiza o campo `transcricao` no insights.json do produto ativo.

Uso:
  python transcrever.py SHORTCODE1 SHORTCODE2 ...
"""

import os
import sys
import json
import time
import logging
from pathlib import Path

try:
    import requests
except ImportError:
    print("Erro: biblioteca 'requests' nao encontrada.")
    print("Instale com: pip install requests")
    sys.exit(1)

# ── Logging ───────────────────────────────────────────────────────────────────
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

# ── Apify ─────────────────────────────────────────────────────────────────────
TRANSCRIBER_URL = 'https://api.apify.com/v2/acts/tictechid~anoxvanzi-transcriber/run-sync-get-dataset-items'

# ── Helpers ───────────────────────────────────────────────────────────────────
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

def get_insights_file() -> Path:
    ativo_file = PROJECT_ROOT / 'meus-produtos' / '.ativo'
    if not ativo_file.exists():
        log.error('meus-produtos/.ativo nao encontrado. Use /produto-novo para criar um produto.')
        sys.exit(1)
    ativo = ativo_file.read_text(encoding='utf-8').strip()
    if not ativo:
        log.error('meus-produtos/.ativo esta vazio.')
        sys.exit(1)
    base = PROJECT_ROOT / 'meus-produtos' / ativo / 'entregas' / 'instagram-dashboard'
    # Tentar subpasta por perfil (IG_USER do .env)
    env = ler_env()
    ig_user = env.get('IG_USER', '')
    if ig_user and (base / ig_user / 'insights.json').exists():
        return base / ig_user / 'insights.json'
    # Fallback: raiz do dashboard
    insights = base / 'insights.json'
    if not insights.exists():
        log.error(f'insights.json nao encontrado em {base}')
        log.error('Execute o /instagram-dashboard primeiro para gerar os dados.')
        sys.exit(1)
    return insights

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
            log.warning(f'  Apify erro HTTP (tentativa {tentativa}/{retries}): {e}')
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

def transcrever_reel(token, shortcode):
    """Transcreve o audio de um Reel via tictechid~anoxvanzi-transcriber."""
    url_post = f'https://www.instagram.com/p/{shortcode}/'
    log.info(f'  Transcrevendo audio via anoxvanzi-transcriber: {url_post}')
    data = apify_post(token, TRANSCRIBER_URL, {
        'start_urls': url_post,
    }, timeout=180)
    if not data:
        return ''
    item = data[0] if isinstance(data, list) else data
    return item.get('text', item.get('transcript', item.get('transcription', '')))

def transcrever_posts(token, shortcodes, insights_file):
    """Transcreve os posts indicados e salva a transcricao no insights.json."""
    insights = json.loads(insights_file.read_text(encoding='utf-8'))
    # Suporta tanto insights do instagram-dashboard (posts na raiz)
    # quanto insights da pesquisa-nicho (topPosts + perfis[].posts)
    all_posts = insights.get('posts', [])
    all_posts += insights.get('topPosts', [])
    for perfil in insights.get('perfis', []):
        all_posts += perfil.get('posts', [])
    posts_map = {p['shortCode']: p for p in all_posts if p.get('shortCode')}

    atualizados = 0
    for shortcode in shortcodes:
        if shortcode not in posts_map:
            log.warning(f'  Shortcode {shortcode} nao encontrado no insights.json, pulando')
            continue

        post = posts_map[shortcode]
        if post.get('tipo') != 'Reel':
            log.info(f'  Post {shortcode} nao e Reel, pulando transcricao')
            continue

        if post.get('transcricao'):
            log.info(f'  Post {shortcode} ja tem transcricao, pulando')
            continue

        try:
            transcricao = transcrever_reel(token, shortcode)
            post['transcricao'] = transcricao
            atualizados += 1
            log.info(f'  Post {shortcode} transcrito ({len(transcricao)} chars)')
        except Exception as e:
            log.warning(f'  Falha ao transcrever {shortcode}: {e}')
            continue

    insights_file.write_text(json.dumps(insights, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    log.info(f'insights.json atualizado — {atualizados} transcricao(oes) adicionada(s)')

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Transcreve audio de Reels via Apify')
    parser.add_argument('shortcodes', nargs='+', help='ShortCodes dos Reels para transcrever')
    parser.add_argument('--insights', type=str, default=None,
                        help='Caminho customizado para o insights.json (ex: pesquisa-nicho)')
    args = parser.parse_args()

    shortcodes = args.shortcodes

    env = ler_env()
    token = env.get('APIFY_API_TOKEN', '')
    if not token:
        log.error('APIFY_API_TOKEN nao encontrado no .env')
        sys.exit(1)

    if args.insights:
        insights_file = Path(args.insights)
        if not insights_file.exists():
            log.error(f'insights.json nao encontrado: {insights_file}')
            sys.exit(1)
    else:
        insights_file = get_insights_file()
    log.info(f'=== Transcrevendo {len(shortcodes)} Reel(s): {shortcodes} ===')
    log.info(f'insights.json: {insights_file}')

    transcrever_posts(token, shortcodes, insights_file)
    log.info('=== Concluido ===')

if __name__ == '__main__':
    main()
