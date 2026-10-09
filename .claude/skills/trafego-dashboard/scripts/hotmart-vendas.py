# -*- coding: utf-8 -*-
"""Coletor de vendas da Hotmart para o dashboard de tráfego.

Lê as credenciais no .env (HOTMART_CLIENT_ID, HOTMART_CLIENT_SECRET e, se existir,
HOTMART_BASIC), busca as vendas aprovadas e os Pix ou boletos aguardando pagamento,
junta produto principal, order bump e upsell da mesma compradora num pedido e grava
a pasta banco/ que o Claude envia para o banco do artefato (ver SKILL.md, seção 6).

Uso:
  python hotmart-vendas.py --verificar
  python hotmart-vendas.py --listar-produtos
  python hotmart-vendas.py --config {pasta}/config.json --pasta {pasta}
"""
import argparse
import base64
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _vendas_comum as comum  # noqa: E402

URL_TOKEN = "https://api-sec-vlc.hotmart.com/security/oauth/token"
URL_API = "https://developers.hotmart.com/payments/api/v1"
APROVADAS = ["APPROVED", "COMPLETE"]
AGUARDANDO = ["WAITING_PAYMENT", "PRINTED_BILLET"]


def credenciais():
    env = comum.ler_env()
    cid, sec = comum.variavel("HOTMART_CLIENT_ID", env), comum.variavel("HOTMART_CLIENT_SECRET", env)
    basic = comum.variavel("HOTMART_BASIC", env)
    if not cid or not sec:
        raise SystemExit("ERRO_CREDENCIAIS: HOTMART_CLIENT_ID e HOTMART_CLIENT_SECRET não estão no .env.")
    if basic and basic.lower().startswith("basic "):
        basic = basic[6:].strip()
    return cid, sec, basic or base64.b64encode(f"{cid}:{sec}".encode()).decode()


def pedir(url, metodo="GET", cabecalhos=None):
    req = urllib.request.Request(url, method=metodo, headers=cabecalhos or {})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Hotmart respondeu {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from None
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


def periodo(dias):
    fim = datetime.now(timezone.utc)
    return int((fim - timedelta(days=dias)).timestamp() * 1000), int(fim.timestamp() * 1000)


def comissoes(ini, fim, tok):
    """Comissão de produtor em cada transação: o que a Hotmart repassa."""
    mapa = {}
    try:
        for st in APROVADAS:
            for it in paginar("/sales/commissions", {"start_date": ini, "end_date": fim, "transaction_status": st}, tok):
                minhas = [c for c in it.get("commissions") or [] if c.get("source") == "PRODUCER"]
                if minhas:
                    mapa[it.get("transaction")] = sum(float((c.get("commission") or {}).get("value") or 0) for c in minhas)
    except RuntimeError as e:
        print(f"AVISO: comissões indisponíveis ({e}). Valor líquido calculado pela taxa da Hotmart.", file=sys.stderr)
    return mapa


def listar_produtos():
    tok = token()
    ini, fim = periodo(90)
    cont = {}
    for st in APROVADAS:
        for it in paginar("/sales/history", {"start_date": ini, "end_date": fim, "transaction_status": st}, tok):
            pr = it.get("product") or {}
            k = str(pr.get("id"))
            cont.setdefault(k, {"id": k, "nome": pr.get("name") or k, "vendas": 0})["vendas"] += 1
    print(json.dumps(sorted(cont.values(), key=lambda x: -x["vendas"]), ensure_ascii=False, indent=2))


def coletar(cfg, pasta, dias):
    tok = token()
    cc = comum.config_checkout(cfg)
    tz = comum.fuso(cfg.get("fuso") or "America/Sao_Paulo")
    ini, fim = periodo(dias)
    brutas = []
    for st in APROVADAS:
        brutas += paginar("/sales/history", {"start_date": ini, "end_date": fim, "transaction_status": st}, tok)
    liquido = comissoes(ini, fim, tok)

    compras, vistos, produtos = [], set(), {}
    for it in brutas:
        pu = it.get("purchase") or {}
        tr = pu.get("transaction")
        pid = str((it.get("product") or {}).get("id"))
        if not tr or tr in vistos or not comum.do_funil(pid, cc):
            continue
        vistos.add(tr)
        produtos[pid] = (it.get("product") or {}).get("name") or pid
        bru = float((pu.get("price") or {}).get("value") or 0)
        liq = liquido.get(tr)
        if liq is None:
            liq = bru - float((pu.get("hotmart_fee") or {}).get("total") or 0)
        t = pu.get("tracking") or {}
        compradora = it.get("buyer") or {}
        compras.append({
            "id": tr, "pai": None, "pid": pid, "nome": produtos[pid], "bru": round(bru, 2), "liq": round(liq, 2),
            "quando": datetime.fromtimestamp((pu.get("approved_date") or pu.get("order_date")) / 1000, tz),
            "rt": comum.rastreio(t.get("source"), t.get("source_sck")),
            "quem": (compradora.get("ucode") or compradora.get("email") or tr).lower(),
        })
    pedidos = comum.agrupar(compras, cc)

    pendentes = []
    for st in AGUARDANDO:
        try:
            for it in paginar("/sales/history", {"start_date": ini, "end_date": fim, "transaction_status": st}, tok):
                pu = it.get("purchase") or {}
                pid = str((it.get("product") or {}).get("id"))
                quando = datetime.fromtimestamp((pu.get("order_date") or 0) / 1000, tz)
                if (cc["principais"] and pid not in cc["principais"]) or quando < datetime.now(tz) - timedelta(days=3):
                    continue  # Pix e boleto antigos já venceram
                t = pu.get("tracking") or {}
                pendentes.append({"t": quando.strftime("%Y-%m-%dT%H:%M:%S"), "rt": comum.rastreio(t.get("source"), t.get("source_sck")), "bru": round(float((pu.get("price") or {}).get("value") or 0), 2)})
        except RuntimeError:
            pass
    comum.gravar(pasta, "Hotmart", cfg, pedidos, pendentes, produtos, tz, dias)


def main():
    ap = argparse.ArgumentParser(description="Vendas da Hotmart para o dashboard de tráfego")
    ap.add_argument("--verificar", action="store_true", help="só confere se as credenciais funcionam")
    ap.add_argument("--listar-produtos", action="store_true", help="lista os produtos vendidos nos últimos 90 dias")
    ap.add_argument("--config", help="config.json do dashboard")
    ap.add_argument("--pasta", help="pasta do dashboard (recebe vendas.json e banco/)")
    ap.add_argument("--dias", type=int, default=32)
    a = ap.parse_args()
    if a.verificar:
        token()
        print("OK: credenciais da Hotmart funcionando.")
        return
    if a.listar_produtos:
        listar_produtos()
        return
    if not a.config or not a.pasta:
        ap.error("informe --config e --pasta")
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    try:
        coletar(cfg, a.pasta, a.dias)
    except RuntimeError as e:
        raise SystemExit(f"ERRO_VENDAS: {e}")


if __name__ == "__main__":
    main()
