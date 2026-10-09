# -*- coding: utf-8 -*-
"""Partes comuns aos coletores de vendas do dashboard (Hotmart e Kiwify).

Cada coletor busca as vendas na plataforma e monta uma lista de compras no formato:
  {"id", "pai", "quando" (datetime com fuso), "pid", "nome", "bru", "liq", "rt", "quem"}
Este módulo junta produto principal, order bump e upsell da mesma compradora num pedido
e grava a saída que vai para o banco do artefato. Nada de nome, e-mail ou documento de
quem comprou sai daqui: "quem" serve só para agrupar e não é gravado.
"""
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

JANELA_BUMP_MIN = 15  # o bump é comprado no mesmo checkout, poucos minutos depois do principal
TAMANHO_LOTE = 200_000  # bytes por documento do banco (o limite do artefato é 256 KiB)


def ler_env():
    """Procura o .env subindo a partir da pasta atual e da pasta do script."""
    valores = {}
    for inicio in (Path.cwd(), Path(__file__).resolve().parent):
        cur = inicio
        while True:
            candidato = cur / ".env"
            if candidato.exists():
                for linha in candidato.read_text(encoding="utf-8").splitlines():
                    if "=" in linha and not linha.lstrip().startswith("#"):
                        k, v = linha.split("=", 1)
                        valores.setdefault(k.strip(), v.strip().strip('"').strip("'"))
                return valores
            if cur.parent == cur:
                break
            cur = cur.parent
    return valores


def variavel(nome, env):
    return os.environ.get(nome) or env.get(nome)


def fuso(nome):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(nome)
    except Exception:
        return timezone(timedelta(hours=-3))  # Brasília, sem horário de verão desde 2019


def rastreio(*valores):
    """Primeiro valor de rastreio preenchido, ignorando os padrões da própria plataforma."""
    for v in valores:
        v = (v or "").strip()
        if v and not re.match(r"^(HOTMART|KIWIFY)", v, re.I):
            return v[:120]
    return ""


def config_checkout(cfg):
    ck = cfg.get("checkout") or {}
    up = ck.get("upsell") or None
    return {
        "principais": {str(x) for x in ck.get("principais") or []},
        "bumps": {str(b["id"]): b.get("nome") or str(b["id"]) for b in ck.get("bumps") or []},
        "up_id": str(up["id"]) if up and up.get("id") else None,
        "up_nome": (up or {}).get("nome"),
        "janela_up": timedelta(hours=float((up or {}).get("janela_horas") or 24)),
    }


def do_funil(pid, cc):
    """Sem produto principal configurado, entram todos os produtos."""
    return not cc["principais"] or pid in cc["principais"] or pid in cc["bumps"] or pid == cc["up_id"]


def agrupar(compras, cc):
    pedidos, por_id, ultimo = [], {}, {}

    def novo(c, principal):
        return {"quando": c["quando"], "t": c["quando"].strftime("%Y-%m-%dT%H:%M:%S"), "rt": c["rt"], "liq": c["liq"], "bru": c["bru"], "p": principal, "b": [], "u": False, "i": [c["pid"]]}

    for c in sorted(compras, key=lambda x: x["quando"]):
        pid = c["pid"]
        if (pid in cc["principais"] or not cc["principais"]) and pid not in cc["bumps"] and pid != cc["up_id"]:
            ped = novo(c, True)
            pedidos.append(ped)
            ultimo[c["quem"]] = ped
            por_id[c["id"]] = ped
            continue
        ped = por_id.get(c.get("pai")) if c.get("pai") else None
        ligado = ped is not None  # a plataforma informou o pedido de origem
        ped = ped or ultimo.get(c["quem"])
        if pid in cc["bumps"] and ped and (ligado or c["quando"] - ped["quando"] <= timedelta(minutes=JANELA_BUMP_MIN)):
            ped["b"].append(pid); ped["i"].append(pid); ped["liq"] += c["liq"]; ped["bru"] += c["bru"]
        elif pid == cc["up_id"] and ped and not ped["u"] and (ligado or c["quando"] - ped["quando"] <= cc["janela_up"]):
            ped["u"] = True; ped["i"].append(pid); ped["liq"] += c["liq"]; ped["bru"] += c["bru"]
        else:
            pedidos.append(novo(c, False))
    for p in pedidos:
        p.pop("quando", None)
        p["liq"], p["bru"] = round(p["liq"], 2), round(p["bru"], 2)
    return pedidos


def gravar(pasta, plataforma, cfg, pedidos, pendentes, produtos, tz, dias):
    """Grava vendas.json (conferência local) e a pasta banco/ com os documentos do artefato."""
    cc = config_checkout(cfg)
    pasta = Path(pasta)
    banco = pasta / "banco"
    banco.mkdir(parents=True, exist_ok=True)
    for velho in banco.glob("*.json"):
        velho.unlink()
    lotes, atual, tamanho = [], [], 0
    for p in pedidos:
        t = len(json.dumps(p, ensure_ascii=False)) + 1
        if atual and tamanho + t > TAMANHO_LOTE:
            lotes.append(atual); atual, tamanho = [], 0
        atual.append(p); tamanho += t
    if atual or not lotes:
        lotes.append(atual)
    info = {
        "geradoEm": datetime.now(tz).strftime("%d/%m às %H:%M"),
        "geradoEmIso": datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%S"),  # o painel corta as métricas de venda nesta hora
        "plataforma": plataforma,
        "checkout": {
            "plataforma": plataforma,
            "bumps": [{"id": k, "nome": v} for k, v in cc["bumps"].items()],
            "upsell": {"nome": cc["up_nome"], "janela_horas": cc["janela_up"].total_seconds() / 3600} if cc["up_id"] else None,
        },
        "produtos": produtos,
        "pendentes": pendentes,
        "lotes": len(lotes),
    }
    (banco / "info.json").write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
    for n, lote in enumerate(lotes, 1):
        (banco / f"lote-{n}.json").write_text(json.dumps({"vendas": lote}, ensure_ascii=False), encoding="utf-8")
    (pasta / "vendas.json").write_text(json.dumps(dict(info, vendas=pedidos), ensure_ascii=False), encoding="utf-8")
    principais = sum(1 for p in pedidos if p["p"])
    print(f"OK: {len(pedidos)} pedidos ({principais} do produto principal) e {len(pendentes)} aguardando pagamento nos últimos {dias} dias.")
    print(f"BANCO: coleção vendas, documentos info e lote-1 a lote-{len(lotes)}, arquivos em {banco}")
