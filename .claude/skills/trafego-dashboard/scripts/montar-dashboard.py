# -*- coding: utf-8 -*-
"""Monta a página do dashboard de tráfego a partir do modelo da skill.

Copia assets/dashboard.html e troca só o bloco CONFIG (entre /*CONFIG_INICIO*/ e
/*CONFIG_FIM*/) pelas escolhas do aluno gravadas no config.json do dashboard.
Nenhum dado da conta entra na página: ela busca os números na Meta quando abre.

Uso:
  python montar-dashboard.py --config meus-produtos/_dashboard-trafego/{slug}/config.json --saida meus-produtos/_dashboard-trafego/{slug}/index.html
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8")) if a.config else {}
    html = MODELO.read_text(encoding="utf-8")
    bloco = "/*CONFIG_INICIO*/\nconst CONFIG = " + json.dumps(config_da_pagina(cfg, a.demo), ensure_ascii=False, indent=2) + ";\n/*CONFIG_FIM*/"
    novo, n = re.subn(r"/\*CONFIG_INICIO\*/.*?/\*CONFIG_FIM\*/", lambda _: bloco, html, flags=re.S)
    if n != 1:
        raise SystemExit("ERRO: bloco CONFIG não encontrado no modelo.")
    saida = Path(a.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(novo, encoding="utf-8")
    print(f"OK: dashboard montado em {saida}")


if __name__ == "__main__":
    main()
