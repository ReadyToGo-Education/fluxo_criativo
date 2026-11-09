# -*- coding: utf-8 -*-
"""Coletor de vendas da Kiwify para o dashboard de tráfego.

Lê as credenciais no .env (KIWIFY_CLIENT_ID, KIWIFY_CLIENT_SECRET e KIWIFY_ACCOUNT_ID),
busca as vendas pagas e os Pix ou boletos aguardando pagamento, junta produto principal,
order bump e upsell da mesma compradora num pedido e grava a pasta banco/ que o Claude
envia para o banco do artefato (ver SKILL.md, seção 6).

Valores da Kiwify chegam em centavos. Bump e upsell são ligados ao pedido de origem
pelo parent_order_id quando a Kiwify informa; senão, pela mesma compradora e pelo horário.

Uso:
  python kiwify-vendas.py --verificar
  python kiwify-vendas.py --listar-produtos
  python kiwify-vendas.py --config {pasta}/config.json --pasta {pasta}
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _vendas_comum as comum  # noqa: E402

URL = "https://public-api.kiwify.com/v1"
PAGAS = {"paid", "approved"}
AGUARDANDO = {"waiting_payment"}
POR_PAGINA = 100


def credenciais():
    env = comum.ler_env()
    cid, sec, conta = (comum.variavel(k, env) for k in ("KIWIFY_CLIENT_ID", "KIWIFY_CLIENT_SECRET", "KIWIFY_ACCOUNT_ID"))
    if not cid or not sec or not conta:
        raise SystemExit("ERRO_CREDENCIAIS: KIWIFY_CLIENT_ID, KIWIFY_CLIENT_SECRET e KIWIFY_ACCOUNT_ID precisam estar no .env.")
    return cid, sec, conta


def pedir(req):
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Kiwify respondeu {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"Sem conexão com a Kiwify: {e.reason}") from None


def token():
    cid, sec, conta = credenciais()
    corpo = urllib.parse.urlencode({"client_id": cid, "client_secret": sec}).encode()
    req = urllib.request.Request(f"{URL}/oauth/token", data=corpo, method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        r = pedir(req)
    except RuntimeError as e:
        raise SystemExit(f"ERRO_TOKEN: a Kiwify recusou as credenciais. {e}")
    if not r.get("access_token"):
        raise SystemExit("ERRO_TOKEN: a Kiwify não devolveu o token de acesso.")
    return r["access_token"], conta


def vendas(dias, tok, conta):
    """Todas as vendas do período, com os detalhes (rastreio, valores, pedido de origem)."""
    fim = datetime.now(timezone.utc).date() + timedelta(days=1)
    ini = fim - timedelta(days=min(dias, 89))  # a Kiwify aceita até 90 dias por consulta
    cab = {"Authorization": f"Bearer {tok}", "x-kiwify-account-id": conta}
    # A documentação não fixa o formato da data: tenta AAAA-MM-DD e, se recusar, data e hora ISO.
    for formato in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.000Z"):
        itens, pagina = [], 1
        try:
            while True:
                q = urllib.parse.urlencode({"start_date": ini.strftime(formato), "end_date": fim.strftime(formato), "view_full_sale_details": "true", "page_size": POR_PAGINA, "page_number": pagina})
                r = pedir(urllib.request.Request(f"{URL}/sales?{q}", headers=cab))
                lote = r.get("data") or []
                itens.extend(lote)
                total = (r.get("pagination") or {}).get("count")
                if len(lote) < POR_PAGINA or (isinstance(total, int) and len(itens) >= total) or pagina >= 500:
                    return itens
                pagina += 1
        except RuntimeError as e:
            if "respondeu 400" in str(e) and formato == "%Y-%m-%d":
                continue
            raise
    return []


def quando(texto, tz):
    if not texto:
        return None
    return datetime.fromisoformat(texto.replace("Z", "+00:00")).astimezone(tz)


def centavos(v):
    try:
        return round(float(v) / 100, 2)
    except (TypeError, ValueError):
        return 0.0


def rastreio(v):
    t = v.get("tracking") or {}
    principal = comum.rastreio(t.get("src"), t.get("sck"))
    if principal:
        return principal
    utm = "_".join(x for x in (t.get("utm_source"), t.get("utm_campaign"), t.get("utm_content")) if x)
    return comum.rastreio(utm)


def listar_produtos():
    tok, conta = token()
    cont = {}
    for v in vendas(89, tok, conta):
        if (v.get("status") or "").lower() not in PAGAS:
            continue
        pr = v.get("product") or {}
        k = str(pr.get("id"))
        cont.setdefault(k, {"id": k, "nome": pr.get("name") or k, "vendas": 0})["vendas"] += 1
    print(json.dumps(sorted(cont.values(), key=lambda x: -x["vendas"]), ensure_ascii=False, indent=2))


def coletar(cfg, pasta, dias):
    tok, conta = token()
    cc = comum.config_checkout(cfg)
    tz = comum.fuso(cfg.get("fuso") or "America/Sao_Paulo")
    agora = datetime.now(tz)
    compras, pendentes, produtos = [], [], {}
    for v in vendas(dias, tok, conta):
        pr = v.get("product") or {}
        pid = str(pr.get("id"))
        status = (v.get("status") or "").lower()
        if not comum.do_funil(pid, cc):
            continue
        pg = v.get("payment") or {}
        if status in AGUARDANDO:
            criado = quando(v.get("created_at"), tz)
            if criado and criado >= agora - timedelta(days=3) and (not cc["principais"] or pid in cc["principais"]):
                pendentes.append({"t": criado.strftime("%Y-%m-%dT%H:%M:%S"), "rt": rastreio(v), "bru": centavos(pg.get("charge_amount") or pg.get("product_base_price"))})
            continue
        if status not in PAGAS:
            continue
        momento = quando(v.get("approved_date") or v.get("created_at"), tz)
        if not momento:
            continue
        produtos[pid] = pr.get("name") or pid
        cliente = v.get("customer") or {}
        compras.append({
            "id": v.get("id"), "pai": v.get("parent_order_id"), "pid": pid, "nome": produtos[pid], "quando": momento,
            "bru": centavos(pg.get("charge_amount") or pg.get("product_base_price")),
            "liq": centavos(pg.get("net_amount") if pg.get("net_amount") is not None else v.get("net_amount")),
            "rt": rastreio(v),
            "quem": str(cliente.get("id") or cliente.get("email") or v.get("id")).lower(),
        })
    comum.gravar(pasta, "Kiwify", cfg, comum.agrupar(compras, cc), pendentes, produtos, tz, dias)


def main():
    ap = argparse.ArgumentParser(description="Vendas da Kiwify para o dashboard de tráfego")
    ap.add_argument("--verificar", action="store_true", help="só confere se as credenciais funcionam")
    ap.add_argument("--listar-produtos", action="store_true", help="lista os produtos vendidos nos últimos 90 dias")
    ap.add_argument("--config", help="config.json do dashboard")
    ap.add_argument("--pasta", help="pasta do dashboard (recebe vendas.json e banco/)")
    ap.add_argument("--dias", type=int, default=32)
    a = ap.parse_args()
    if a.verificar:
        token()
        print("OK: credenciais da Kiwify funcionando.")
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
