# -*- coding: utf-8 -*-
"""Coletor de vendas da Hotmart para o dashboard de tráfego.

Lê as credenciais da Hotmart no .env (HOTMART_CLIENT_ID, HOTMART_CLIENT_SECRET e,
se existir, HOTMART_BASIC), busca as vendas aprovadas e os Pix ou boletos aguardando
pagamento, junta produto principal, order bump e upsell da mesma compradora num pedido
e grava o vendas.json que o dashboard publica junto da página.

O arquivo de saída não leva nome, e-mail nem documento de quem comprou: só horário,
valores, produtos e o rastreio do link (src ou sck).

Uso:
  python hotmart-vendas.py --verificar
  python hotmart-vendas.py --listar-produtos
  python hotmart-vendas.py --config caminho/config.json --saida caminho/vendas.json
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

URL_TOKEN = "https://api-sec-vlc.hotmart.com/security/oauth/token"
URL_API = "https://developers.hotmart.com/payments/api/v1"
APROVADAS = ["APPROVED", "COMPLETE"]
AGUARDANDO = ["WAITING_PAYMENT", "PRINTED_BILLET"]
JANELA_BUMP_MIN = 15  # bump é comprado no mesmo checkout: poucos minutos depois do principal


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


def credenciais():
    env = ler_env()
    cid = os.environ.get("HOTMART_CLIENT_ID") or env.get("HOTMART_CLIENT_ID")
    sec = os.environ.get("HOTMART_CLIENT_SECRET") or env.get("HOTMART_CLIENT_SECRET")
    basic = os.environ.get("HOTMART_BASIC") or env.get("HOTMART_BASIC")
    if not cid or not sec:
        raise SystemExit("ERRO_CREDENCIAIS: HOTMART_CLIENT_ID e HOTMART_CLIENT_SECRET não estão no .env.")
    if basic and basic.lower().startswith("basic "):
        basic = basic[6:].strip()
    if not basic:
        basic = base64.b64encode(f"{cid}:{sec}".encode()).decode()
    return cid, sec, basic


def pedir(url, metodo="GET", cabecalhos=None):
    req = urllib.request.Request(url, method=metodo, headers=cabecalhos or {})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")[:300]
        raise RuntimeError(f"Hotmart respondeu {e.code}: {corpo}") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"Sem conexão com a Hotmart: {e.reason}") from None


def token():
    cid, sec, basic = credenciais()
    q = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": cid, "client_secret": sec})
    try:
        r = pedir(f"{URL_TOKEN}?{q}", "POST", {"Authorization": f"Basic {basic}", "Content-Type": "application/json"})
    except RuntimeError as e:
        raise SystemExit(f"ERRO_TOKEN: a Hotmart recusou as credenciais. {e}")
    if not r.get("access_token"):
        raise SystemExit("ERRO_TOKEN: a Hotmart não devolveu o token de acesso.")
    return r["access_token"]


def paginar(caminho, params, tok):
    itens, pagina = [], None
    for _ in range(200):
        p = dict(params, max_results=200)
        if pagina:
            p["page_token"] = pagina
        r = pedir(f"{URL_API}{caminho}?{urllib.parse.urlencode(p)}", cabecalhos={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
        itens.extend(r.get("items") or [])
        pagina = (r.get("page_info") or {}).get("next_page_token")
        if not pagina:
            break
    return itens


def fuso(nome):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(nome)
    except Exception:
        return timezone(timedelta(hours=-3))  # Brasília, sem horário de verão desde 2019


def rastreio(purchase):
    t = purchase.get("tracking") or {}
    for v in (t.get("source_sck"), t.get("source")):
        v = (v or "").strip()
        if v and not re.match(r"^HOTMART", v, re.I):
            return v[:120]
    return ""


def valores(item, comissoes):
    pu = item.get("purchase") or {}
    bru = float((pu.get("price") or {}).get("value") or 0)
    liq = comissoes.get(pu.get("transaction"))
    if liq is None:
        liq = bru - float((pu.get("hotmart_fee") or {}).get("total") or 0)
    return round(bru, 2), round(liq, 2)


def comissoes_do_periodo(ini, fim, tok):
    """Comissão de quem é dono da conta em cada transação (o que a Hotmart repassa)."""
    mapa = {}
    try:
        for st in APROVADAS:
            for it in paginar("/sales/commissions", {"start_date": ini, "end_date": fim, "transaction_status": st}, tok):
                minhas = [c for c in it.get("commissions") or [] if c.get("source") in ("PRODUCER",)]
                if minhas:
                    mapa[it.get("transaction")] = sum(float((c.get("commission") or {}).get("value") or 0) for c in minhas)
    except RuntimeError as e:
        print(f"AVISO: comissões indisponíveis ({e}). Valor líquido calculado pela taxa da Hotmart.", file=sys.stderr)
    return mapa


def periodo(dias):
    fim = datetime.now(timezone.utc)
    ini = fim - timedelta(days=dias)
    return int(ini.timestamp() * 1000), int(fim.timestamp() * 1000)


def listar_produtos():
    tok = token()
    ini, fim = periodo(90)
    cont = {}
    for st in APROVADAS:
        for it in paginar("/sales/history", {"start_date": ini, "end_date": fim, "transaction_status": st}, tok):
            pr = it.get("product") or {}
            k = str(pr.get("id"))
            cont.setdefault(k, {"id": k, "nome": pr.get("name") or k, "vendas": 0})["vendas"] += 1
    lista = sorted(cont.values(), key=lambda x: -x["vendas"])
    print(json.dumps(lista, ensure_ascii=False, indent=2))


def coletar(cfg, saida, dias):
    tok = token()
    ck = cfg.get("checkout") or {}
    tz = fuso(cfg.get("fuso") or "America/Sao_Paulo")
    principais = {str(x) for x in ck.get("principais") or []}
    bumps = {str(b["id"]): b.get("nome") or str(b["id"]) for b in ck.get("bumps") or []}
    up = ck.get("upsell") or None
    up_id = str(up["id"]) if up and up.get("id") else None
    janela_up = timedelta(hours=float((up or {}).get("janela_horas") or 24))
    ini, fim = periodo(dias)

    brutas = []
    for st in APROVADAS:
        brutas += paginar("/sales/history", {"start_date": ini, "end_date": fim, "transaction_status": st}, tok)
    comissoes = comissoes_do_periodo(ini, fim, tok)

    vistos, compras = set(), []
    for it in brutas:
        pu = it.get("purchase") or {}
        tr = pu.get("transaction")
        if not tr or tr in vistos:
            continue
        vistos.add(tr)
        pid = str((it.get("product") or {}).get("id"))
        if principais and pid not in principais and pid not in bumps and pid != up_id:
            continue
        quando = datetime.fromtimestamp((pu.get("approved_date") or pu.get("order_date")) / 1000, tz)
        bru, liq = valores(it, comissoes)
        quem = ((it.get("buyer") or {}).get("ucode") or (it.get("buyer") or {}).get("email") or tr).lower()
        compras.append({"quando": quando, "pid": pid, "nome": (it.get("product") or {}).get("name") or pid, "bru": bru, "liq": liq, "rt": rastreio(pu), "quem": quem})
    compras.sort(key=lambda c: c["quando"])

    pedidos, ultimo_principal = [], {}
    for c in compras:
        pid = c["pid"]
        # Sem produto principal configurado, toda compra que não é bump nem upsell abre um pedido.
        if (pid in principais or not principais) and pid not in bumps and pid != up_id:
            ped = {"quando": c["quando"], "t": c["quando"].strftime("%Y-%m-%dT%H:%M:%S"), "rt": c["rt"], "liq": c["liq"], "bru": c["bru"], "p": True, "b": [], "u": False, "it": [c["nome"]]}
            pedidos.append(ped)
            ultimo_principal[c["quem"]] = ped
            continue
        ped = ultimo_principal.get(c["quem"])
        if c["pid"] in bumps and ped and c["quando"] - ped["quando"] <= timedelta(minutes=JANELA_BUMP_MIN):
            ped["b"].append(c["pid"]); ped["it"].append(c["nome"]); ped["liq"] += c["liq"]; ped["bru"] += c["bru"]
        elif c["pid"] == up_id and ped and c["quando"] - ped["quando"] <= janela_up and not ped["u"]:
            ped["u"] = True; ped["it"].append(c["nome"]); ped["liq"] += c["liq"]; ped["bru"] += c["bru"]
        else:
            pedidos.append({"quando": c["quando"], "t": c["quando"].strftime("%Y-%m-%dT%H:%M:%S"), "rt": c["rt"], "liq": c["liq"], "bru": c["bru"], "p": False, "b": [], "u": False, "it": [c["nome"]]})

    pendentes = []
    for st in AGUARDANDO:
        try:
            for it in paginar("/sales/history", {"start_date": ini, "end_date": fim, "transaction_status": st}, tok):
                pu = it.get("purchase") or {}
                pid = str((it.get("product") or {}).get("id"))
                if principais and pid not in principais:
                    continue
                quando = datetime.fromtimestamp((pu.get("order_date") or 0) / 1000, tz)
                if quando < datetime.now(tz) - timedelta(days=3):
                    continue  # Pix e boleto antigos já venceram
                pendentes.append({"t": quando.strftime("%Y-%m-%dT%H:%M:%S"), "rt": rastreio(pu), "bru": round(float((pu.get("price") or {}).get("value") or 0), 2)})
        except RuntimeError:
            pass

    for p in pedidos:
        p.pop("quando", None)
        p["liq"], p["bru"] = round(p["liq"], 2), round(p["bru"], 2)
    saida_json = {
        "geradoEm": datetime.now(tz).strftime("%d/%m às %H:%M"),
        "checkout": {"plataforma": "Hotmart", "bumps": [{"id": k, "nome": v} for k, v in bumps.items()], "upsell": {"nome": up.get("nome"), "janela_horas": float(up.get("janela_horas") or 24)} if up_id else None},
        "vendas": pedidos,
        "pendentes": pendentes,
    }
    Path(saida).parent.mkdir(parents=True, exist_ok=True)
    Path(saida).write_text(json.dumps(saida_json, ensure_ascii=False), encoding="utf-8")
    principais_n = sum(1 for p in pedidos if p["p"])
    print(f"OK: {len(pedidos)} pedidos ({principais_n} do produto principal) e {len(pendentes)} aguardando pagamento nos últimos {dias} dias. Arquivo: {saida}")


def main():
    ap = argparse.ArgumentParser(description="Vendas da Hotmart para o dashboard de tráfego")
    ap.add_argument("--verificar", action="store_true", help="só confere se as credenciais funcionam")
    ap.add_argument("--listar-produtos", action="store_true", help="lista os produtos vendidos nos últimos 90 dias")
    ap.add_argument("--config", help="config.json do dashboard")
    ap.add_argument("--saida", help="caminho do vendas.json")
    ap.add_argument("--dias", type=int, default=32)
    a = ap.parse_args()
    if a.verificar:
        token()
        print("OK: credenciais da Hotmart funcionando.")
        return
    if a.listar_produtos:
        listar_produtos()
        return
    if not a.config or not a.saida:
        ap.error("informe --config e --saida")
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    try:
        coletar(cfg, a.saida, a.dias)
    except RuntimeError as e:
        raise SystemExit(f"ERRO_VENDAS: {e}")


if __name__ == "__main__":
    main()
