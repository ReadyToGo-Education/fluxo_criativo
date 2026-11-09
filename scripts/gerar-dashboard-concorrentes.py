#!/usr/bin/env python3
"""
Gera dashboard.html interativo a partir do snapshot.json de concorrentes IG.
Self-contained: CSS e JS embutidos, sem dependencias externas.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_paths():
    ativo_file = PROJECT_ROOT / 'meus-produtos' / '.ativo'
    slug = ativo_file.read_text(encoding='utf-8').strip()
    base = PROJECT_ROOT / 'meus-produtos' / slug / 'entregas' / 'dados' / 'concorrentes-IG'
    return base / 'snapshot.json', base / 'dashboard.html'

def fmt_num(n):
    if n >= 1_000_000:
        return f'{n/1_000_000:.2f}M'.replace('.', ',')
    if n >= 1_000:
        return f'{n/1_000:.1f}k'.replace('.', ',')
    return f'{n:,}'.replace(',', '.')

def html_template(snapshot, dono_username='adrianasilveiraoficial1'):
    perfis = [p for p in snapshot['perfis'] if 'erro' not in p]
    perfis_seg  = sorted(perfis, key=lambda x: x['seguidores'], reverse=True)
    perfis_eng  = sorted(perfis, key=lambda x: x['eng_medio_pct'], reverse=True)
    perfis_view = sorted(perfis, key=lambda x: x['views_medio'], reverse=True)
    perfis_freq = sorted(perfis, key=lambda x: x['freq_post_por_semana'], reverse=True)

    gerado_em = snapshot.get('gerado_em', '')
    try:
        gerado_em_fmt = datetime.fromisoformat(gerado_em).strftime('%d/%m/%Y %H:%M')
    except Exception:
        gerado_em_fmt = gerado_em

    max_eng  = max(p['eng_medio_pct'] for p in perfis) or 1
    max_seg  = max(p['seguidores'] for p in perfis) or 1
    max_view = max(p['views_medio'] for p in perfis) or 1
    max_freq = max(p['freq_post_por_semana'] for p in perfis) or 1

    def linhas_tabela():
        rows = []
        for i, p in enumerate(perfis_eng, 1):
            destaque = ' class="dono"' if p['username'] == dono_username else ''
            rows.append(f'''
            <tr{destaque}>
              <td class="rank">{i}</td>
              <td><a href="https://instagram.com/{p["username"]}" target="_blank">@{p["username"]}</a><div class="nome">{p.get("nome","")}</div></td>
              <td class="num">{fmt_num(p["seguidores"])}</td>
              <td class="num">{fmt_num(p["total_posts"])}</td>
              <td class="num">{p["eng_medio_pct"]}%</td>
              <td class="num">{fmt_num(int(p["likes_medio"]))}</td>
              <td class="num">{fmt_num(int(p["comentarios_medio"]))}</td>
              <td class="num">{fmt_num(int(p["views_medio"]))}</td>
              <td class="num">{p["freq_post_por_semana"]}</td>
              <td>{p["formato_dominante"]}</td>
              <td class="num">há {p["dias_desde_ultimo_post"]}d</td>
            </tr>''')
        return '\n'.join(rows)

    def barras(perfis_ord, campo, sufixo='', escala_max=1, formatador=None):
        rows = []
        for p in perfis_ord:
            valor = p[campo]
            if formatador:
                valor_str = formatador(valor)
            else:
                valor_str = f'{valor}{sufixo}'
            larg = max(2, valor / escala_max * 100)
            destaque = ' bar-dono' if p['username'] == dono_username else ''
            rows.append(f'''
            <div class="bar-row">
              <div class="bar-label"><a href="https://instagram.com/{p["username"]}" target="_blank">@{p["username"]}</a></div>
              <div class="bar-track"><div class="bar-fill{destaque}" style="width:{larg}%"></div></div>
              <div class="bar-value">{valor_str}</div>
            </div>''')
        return '\n'.join(rows)

    cards = []
    for p in perfis_seg:
        destaque = ' card-dono' if p['username'] == dono_username else ''
        bio = (p.get('bio') or '').replace('\n', ' ')[:200]
        cards.append(f'''
        <div class="card{destaque}">
          <div class="card-head">
            <a href="https://instagram.com/{p["username"]}" target="_blank" class="card-title">@{p["username"]}{' ✓' if p.get('verificado') else ''}</a>
            <div class="card-name">{p.get("nome","")}</div>
          </div>
          <div class="card-bio">{bio}</div>
          <div class="card-grid">
            <div class="kv"><span>Seguidores</span><b>{fmt_num(p["seguidores"])}</b></div>
            <div class="kv"><span>Seguindo</span><b>{fmt_num(p["seguindo"])}</b></div>
            <div class="kv"><span>Posts no perfil</span><b>{fmt_num(p["total_posts"])}</b></div>
            <div class="kv"><span>Engajamento médio</span><b>{p["eng_medio_pct"]}%</b></div>
            <div class="kv"><span>Likes médios</span><b>{fmt_num(int(p["likes_medio"]))}</b></div>
            <div class="kv"><span>Comentários médios</span><b>{fmt_num(int(p["comentarios_medio"]))}</b></div>
            <div class="kv"><span>Views médios (Reels)</span><b>{fmt_num(int(p["views_medio"]))}</b></div>
            <div class="kv"><span>Posts por semana</span><b>{p["freq_post_por_semana"]}</b></div>
            <div class="kv"><span>Formato dominante</span><b>{p["formato_dominante"]}</b></div>
            <div class="kv"><span>Último post</span><b>há {p["dias_desde_ultimo_post"]}d</b></div>
          </div>
          <div class="card-mix">
            Reels {p["tipos"].get("Reel",0)} · Carrosséis {p["tipos"].get("Carrossel",0)} · Fotos {p["tipos"].get("Foto",0)} (amostra: {p["posts_coletados"]} posts)
          </div>
        </div>''')

    eng_dono = next((p['eng_medio_pct'] for p in perfis if p['username'] == dono_username), 0)
    seg_dono = next((p['seguidores'] for p in perfis if p['username'] == dono_username), 0)
    media_eng = sum(p['eng_medio_pct'] for p in perfis) / len(perfis) if perfis else 0

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Concorrentes Instagram — {gerado_em_fmt}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0a0e14;
    --surface: #11161f;
    --surface-2: #181f2c;
    --border: #1f2937;
    --text: #e5e7eb;
    --text-muted: #9ca3af;
    --accent: #d4a017;
    --accent-2: #f5d36e;
    --dono: #d4a017;
    --good: #22c55e;
    --warn: #f59e0b;
    --bad: #ef4444;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
    font-size: 14px;
  }}
  .container {{ max-width: 1280px; margin: 0 auto; padding: 32px 24px; }}
  header {{ margin-bottom: 32px; }}
  h1 {{ font-size: 28px; margin: 0 0 8px; font-weight: 700; }}
  .sub {{ color: var(--text-muted); font-size: 14px; }}
  .stats {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px; margin: 24px 0;
  }}
  .stat {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px;
  }}
  .stat-label {{ font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }}
  .stat-value {{ font-size: 24px; font-weight: 600; margin-top: 6px; }}
  .stat-detail {{ font-size: 12px; color: var(--text-muted); margin-top: 4px; }}
  .stat-dono .stat-value {{ color: var(--accent); }}

  section {{ margin-bottom: 40px; }}
  h2 {{ font-size: 20px; font-weight: 600; margin: 0 0 16px; }}
  h3 {{ font-size: 16px; font-weight: 600; margin: 0 0 12px; color: var(--text-muted); }}

  .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  @media (max-width: 800px) {{ .charts {{ grid-template-columns: 1fr; }} }}
  .chart {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px;
  }}
  .bar-row {{ display: grid; grid-template-columns: 180px 1fr 90px; gap: 12px; align-items: center; margin-bottom: 8px; }}
  .bar-label {{ font-size: 13px; }}
  .bar-label a {{ color: var(--text); text-decoration: none; }}
  .bar-label a:hover {{ color: var(--accent); }}
  .bar-track {{ background: var(--surface-2); border-radius: 4px; height: 22px; overflow: hidden; }}
  .bar-fill {{
    background: linear-gradient(90deg, #4b5563, #6b7280);
    height: 100%; transition: width 0.6s ease;
  }}
  .bar-fill.bar-dono {{ background: linear-gradient(90deg, var(--accent), var(--accent-2)); }}
  .bar-value {{ text-align: right; font-size: 13px; font-weight: 500; color: var(--text-muted); }}

  table {{ width: 100%; border-collapse: collapse; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
  th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid var(--border); font-size: 13px; }}
  th {{ background: var(--surface-2); font-weight: 600; color: var(--text-muted); text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
  tr:last-child td {{ border-bottom: none; }}
  tr.dono td {{ background: rgba(212, 160, 23, 0.08); }}
  td.rank {{ width: 40px; color: var(--text-muted); font-weight: 600; }}
  td.num {{ text-align: right; }}
  td a {{ color: var(--accent-2); text-decoration: none; font-weight: 500; }}
  td a:hover {{ text-decoration: underline; }}
  .nome {{ font-size: 11px; color: var(--text-muted); margin-top: 2px; }}
  .table-wrap {{ overflow-x: auto; }}

  .cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }}
  .card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px;
  }}
  .card-dono {{ border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }}
  .card-head {{ margin-bottom: 8px; }}
  .card-title {{ font-size: 16px; font-weight: 600; color: var(--accent-2); text-decoration: none; }}
  .card-title:hover {{ text-decoration: underline; }}
  .card-name {{ font-size: 12px; color: var(--text-muted); margin-top: 2px; }}
  .card-bio {{ font-size: 12px; color: var(--text-muted); margin-bottom: 16px; min-height: 36px; }}
  .card-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px 16px; }}
  .kv {{ display: flex; justify-content: space-between; font-size: 12px; padding: 4px 0; border-bottom: 1px solid var(--border); }}
  .kv span {{ color: var(--text-muted); }}
  .kv b {{ color: var(--text); font-weight: 600; }}
  .card-mix {{ font-size: 11px; color: var(--text-muted); margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border); }}

  .legend {{ font-size: 12px; color: var(--text-muted); margin-top: 8px; }}
  .badge-dono {{ display: inline-block; padding: 2px 8px; background: var(--accent); color: #000; border-radius: 4px; font-size: 11px; font-weight: 600; margin-left: 8px; }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>Análise de Concorrentes Instagram</h1>
    <div class="sub">Atualizado em {gerado_em_fmt} · {len(perfis)} perfis analisados · seu perfil em destaque dourado</div>
  </header>

  <section>
    <div class="stats">
      <div class="stat stat-dono">
        <div class="stat-label">Sua posição em engajamento</div>
        <div class="stat-value">#{perfis_eng.index(next(p for p in perfis_eng if p["username"]==dono_username))+1} de {len(perfis)}</div>
        <div class="stat-detail">{eng_dono}% (média do grupo {round(media_eng,2)}%)</div>
      </div>
      <div class="stat stat-dono">
        <div class="stat-label">Sua posição em seguidores</div>
        <div class="stat-value">#{perfis_seg.index(next(p for p in perfis_seg if p["username"]==dono_username))+1} de {len(perfis)}</div>
        <div class="stat-detail">{fmt_num(seg_dono)} seguidores</div>
      </div>
      <div class="stat">
        <div class="stat-label">Maior engajamento</div>
        <div class="stat-value">{perfis_eng[0]["eng_medio_pct"]}%</div>
        <div class="stat-detail">@{perfis_eng[0]["username"]}</div>
      </div>
      <div class="stat">
        <div class="stat-label">Maior base</div>
        <div class="stat-value">{fmt_num(perfis_seg[0]["seguidores"])}</div>
        <div class="stat-detail">@{perfis_seg[0]["username"]}</div>
      </div>
    </div>
  </section>

  <section>
    <h2>Visão comparativa</h2>
    <div class="charts">
      <div class="chart">
        <h3>Engajamento médio (%)</h3>
        {barras(perfis_eng, 'eng_medio_pct', sufixo='%', escala_max=max_eng)}
      </div>
      <div class="chart">
        <h3>Seguidores</h3>
        {barras(perfis_seg, 'seguidores', escala_max=max_seg, formatador=fmt_num)}
      </div>
      <div class="chart">
        <h3>Views médios em Reels</h3>
        {barras(perfis_view, 'views_medio', escala_max=max_view, formatador=lambda v: fmt_num(int(v)))}
      </div>
      <div class="chart">
        <h3>Frequência de postagem (posts por semana)</h3>
        {barras(perfis_freq, 'freq_post_por_semana', escala_max=max_freq, formatador=lambda v: f'{v}')}
      </div>
    </div>
  </section>

  <section>
    <h2>Tabela completa <span class="legend">(ordenada por engajamento)</span></h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th><th>Perfil</th><th>Seguidores</th><th>Posts perfil</th>
            <th>Eng. médio</th><th>Likes méd.</th><th>Coment. méd.</th>
            <th>Views méd.</th><th>P/sem</th><th>Formato top</th><th>Último</th>
          </tr>
        </thead>
        <tbody>
          {linhas_tabela()}
        </tbody>
      </table>
    </div>
  </section>

  <section>
    <h2>Ficha individual</h2>
    <div class="cards">
      {''.join(cards)}
    </div>
  </section>

  <footer style="text-align:center;color:var(--text-muted);font-size:11px;margin-top:32px;padding-top:24px;border-top:1px solid var(--border);">
    Dados extraídos via Instagram Web API · Atualize rodando <code>scripts/analise-concorrentes-ig.py</code>
  </footer>
</div>
</body>
</html>
'''

def main():
    snapshot_path, dashboard_path = get_paths()
    snapshot = json.loads(snapshot_path.read_text(encoding='utf-8'))
    html = html_template(snapshot)
    dashboard_path.write_text(html, encoding='utf-8')
    print(f'Dashboard salvo: {dashboard_path}')

if __name__ == '__main__':
    main()
