# -*- coding: utf-8 -*-
"""Monta a página do dashboard de tráfego a partir do modelo da skill.

Copia assets/dashboard.html e troca só o bloco CONFIG (entre /*CONFIG_INICIO*/ e
/*CONFIG_FIM*/) pelas escolhas do aluno gravadas no config.json do dashboard.
Nenhum dado da conta entra na página: ela busca os números na Meta quando abre (fonte
"conector") ou lê os números gravados no banco do artefato pelo meta-app.py (fonte "app").
O token do App nunca entra na página.

A exceção é a fotografia para o analisador (--fotografia): uma página fixa, sem conector e
sem banco, que leva dentro dela os números que o painel guardou na coleção "fotografia" do
banco do artefato (baixada com o ArtifactData, opção out_dir).

Uso:
  python montar-dashboard.py --config meus-produtos/_dashboard-trafego/{slug}/config.json --saida meus-produtos/_dashboard-trafego/{slug}/index.html
  python montar-dashboard.py --config .../config.json --fotografia .../fotografia-dados/fotografia --saida .../fotografia.html
  python montar-dashboard.py --demo --saida caminho/demo.html
"""
import argparse
import json
import re
from pathlib import Path

MODELO = Path(__file__).resolve().parent.parent / "assets" / "dashboard.html"
PADRAO = {"roas_bom": 1.5, "ctr_link_minimo": 0.8, "frequencia_maxima": 2.5}


def config_da_pagina(cfg, demo):
    ck = cfg.get("checkout") or None
    return {
        "nome": cfg.get("nome") or "Dashboard de Tráfego",
        "demo": bool(demo),
        "fonte": "app" if cfg.get("fonte") == "app" else "conector",
        "conector": cfg.get("conector") or "Meta MCP",
        "contas": [str(c) for c in cfg.get("contas") or []],
        "moeda": cfg.get("moeda") or "BRL",
        "janelaDias": 30,
        "metas": {**PADRAO, **(cfg.get("metas") or {})},
        "checkout": {
            "plataforma": ck.get("plataforma") or "Hotmart",
            "bumps": [{"id": str(b["id"]), "nome": b.get("nome") or str(b["id"])} for b in ck.get("bumps") or []],
            "upsell": {"nome": ck["upsell"].get("nome"), "janela_horas": float(ck["upsell"].get("janela_horas") or 24)} if ck.get("upsell") else None,
        } if ck else None,
    }


def ler_documento(arquivo):
    """Corpo de um documento salvo pelo ArtifactData (puro ou envolto em "data")."""
    doc = json.loads(arquivo.read_text(encoding="utf-8"))
    if isinstance(doc, dict) and isinstance(doc.get("data"), dict) and "texto" not in doc and "geracao" not in doc:
        return doc["data"]
    return doc


def ler_fotografia(pasta):
    """Junta as partes da geração para a qual o "info" aponta e devolve os números do painel."""
    pasta = Path(pasta)
    arq_info = pasta / "info.json"
    if not arq_info.exists():
        raise SystemExit(f"ERRO_FOTOGRAFIA: {arq_info} não existe. O painel ainda não guardou os números.")
    info = ler_documento(arq_info)
    partes = []
    for n in range(1, int(info.get("partes") or 0) + 1):
        arq = pasta / f"{info.get('geracao')}-{n}.json"
        if not arq.exists():
            raise SystemExit(f"ERRO_FOTOGRAFIA: falta a parte {n} de {info.get('partes')}.")
        partes.append(ler_documento(arq).get("texto") or "")
    try:
        dados = json.loads("".join(partes))
    except ValueError:
        raise SystemExit("ERRO_FOTOGRAFIA: as partes não formam os números completos.")
    if dados.get("demo"):
        raise SystemExit("ERRO_FOTOGRAFIA: os números guardados são da demonstração, não da conta do aluno.")
    return dados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--fotografia", help="pasta com o info.json e as partes da coleção fotografia")
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8")) if a.config else {}
    html = MODELO.read_text(encoding="utf-8")
    bloco = "/*CONFIG_INICIO*/\nconst CONFIG = " + json.dumps(config_da_pagina(cfg, a.demo), ensure_ascii=False, indent=2) + ";\n"
    if a.fotografia:
        dados = json.dumps(ler_fotografia(a.fotografia), ensure_ascii=False, separators=(",", ":"))
        # "</script>" ou "<!--" num nome de campanha quebraria a tag script no meio dos dados.
        bloco += "CONFIG.fotografia = " + dados.replace("<", "\\u003c") + ";\n"
    bloco += "/*CONFIG_FIM*/"
    novo, n = re.subn(r"/\*CONFIG_INICIO\*/.*?/\*CONFIG_FIM\*/", lambda _: bloco, html, flags=re.S)
    if n != 1:
        raise SystemExit("ERRO: bloco CONFIG não encontrado no modelo.")
    if a.fotografia:
        # Título da página publicada: no Claude, não pode se confundir com o painel ao vivo.
        titulo = (cfg.get("nome") or "Dashboard de Tráfego") + " (fotografia)"
        novo = re.sub(r"<title>.*?</title>", lambda _: "<title>" + titulo.replace("&", "&amp;").replace("<", "&lt;") + "</title>", novo, count=1, flags=re.S)
    saida = Path(a.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(novo, encoding="utf-8")
    print(f"OK: {'fotografia' if a.fotografia else 'dashboard'} montado em {saida}")


if __name__ == "__main__":
    main()
