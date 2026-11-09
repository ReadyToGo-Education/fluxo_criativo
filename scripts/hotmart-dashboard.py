#!/usr/bin/env python3
"""
Dashboard de faturamento Hotmart por produto e por mês.

Puxa da API da Hotmart as vendas aprovadas, os reembolsos, as comissões e o
detalhe de preço de cada venda, converte tudo para reais e gera um painel HTML
único (sem dependências externas) com filtro de ano, mês e produto.

Valores calculados por venda (sempre em R$):
- bruto: o que o cliente pagou (inclui juros de parcelamento e impostos)
- oferta: o preço da oferta (base sobre a qual a Hotmart calcula a taxa)
- taxa: taxa da Hotmart
- club: taxa do Hotmart Club (ADDON)
- repasse: comissões de coprodutores e afiliados
- recebido: comissão que cai na conta do Instituto (o valor recebido real)

Conversão: vendas em moeda estrangeira usam a real_conversion_rate da própria
Hotmart. Comissões pagas em dólar usam a PTAX de venda do Banco Central do dia
da aprovação.

Uso:
    python3 scripts/hotmart-dashboard.py            # atualiza os 2 últimos meses e gera o painel
    python3 scripts/hotmart-dashboard.py --tudo     # baixa tudo de novo
    python3 scripts/hotmart-dashboard.py --desde 2023
"""
import argparse
import importlib.util
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_DADOS = RAIZ / "meus-produtos" / "instituto-mannah" / "dados" / "hotmart"
PASTA_RAW = PASTA_DADOS / "raw"
SAIDA = RAIZ / "meus-produtos" / "instituto-mannah" / "entregas" / "dashboard-hotmart" / "dashboard-hotmart.html"
TEMPLATE = Path(__file__).resolve().parent / "hotmart_dashboard_template.html"

_spec = importlib.util.spec_from_file_location("mcp_hotmart", Path(__file__).resolve().parent / "mcp-hotmart.py")
hm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hm)

REEMBOLSOS = ",".join(hm.GRUPOS_STATUS["reembolsos"])
APROVADAS = "APPROVED,COMPLETE"


def log(msg):
    print(msg, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Coleta
# ---------------------------------------------------------------------------

def meses_do_periodo(ano_inicio):
    hoje = datetime.now(hm.FUSO)
    a, m, lista = ano_inicio, 1, []
    while (a, m) <= (hoje.year, hoje.month):
        lista.append((a, m))
        a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return lista


def baixar_mes(a, m):
    hoje = datetime.now(hm.FUSO)
    ini = datetime(a, m, 1, tzinfo=hm.FUSO)
    prox = datetime(a + (m == 12), 1 if m == 12 else m + 1, 1, tzinfo=hm.FUSO)
    fim = min(prox - timedelta(milliseconds=1), hoje)
    base = {"start_date": hm._ms(ini), "end_date": hm._ms(fim)}
    pag = lambda path, extra: hm.paginar(path, dict(base, **extra), limite=100000)
    dados = {
        "aprovadas": pag("/payments/api/v1/sales/history", {"transaction_status": APROVADAS}),
        "reembolsos": pag("/payments/api/v1/sales/history", {"transaction_status": REEMBOLSOS}),
        "comissoes": pag("/payments/api/v1/sales/commissions", {"transaction_status": APROVADAS}),
        "precos": pag("/payments/api/v1/sales/price/details", {"transaction_status": APROVADAS}),
    }
    # Dados pessoais do comprador não entram no cache
    for chave in ("aprovadas", "reembolsos"):
        for v in dados[chave]:
            v.pop("buyer", None)
    for c in dados["comissoes"]:
        for x in c.get("commissions") or []:
            (x.get("user") or {}).pop("email", None)
    return dados


def coletar(ano_inicio, tudo):
    PASTA_RAW.mkdir(parents=True, exist_ok=True)
    meses = meses_do_periodo(ano_inicio)
    recentes = set(meses[-2:])
    por_mes = {}
    for a, m in meses:
        arq = PASTA_RAW / ("%04d-%02d.json" % (a, m))
        if arq.exists() and not tudo and (a, m) not in recentes:
            por_mes[(a, m)] = json.loads(arq.read_text(encoding="utf-8"))
            continue
        log("Baixando %02d/%04d da Hotmart..." % (m, a))
        dados = baixar_mes(a, m)
        arq.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        por_mes[(a, m)] = dados
    return por_mes


def baixar_ptax(ano_inicio):
    """Cotação PTAX de venda do dólar por dia (Banco Central)."""
    ini = "12-15-%d" % (ano_inicio - 1)
    fim = datetime.now(hm.FUSO).strftime("%m-%d-%Y")
    url = ("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo("
           "dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='%s'"
           "&@dataFinalCotacao='%s'&$format=json" % (ini, fim))
    with urllib.request.urlopen(url, timeout=60) as r:
        valores = json.loads(r.read())["value"]
    ptax = {}
    for v in valores:
        ptax[v["dataHoraCotacao"][:10]] = float(v["cotacaoVenda"])
    (PASTA_DADOS / "ptax-usd.json").write_text(json.dumps(ptax), encoding="utf-8")
    return ptax


def ptax_do_dia(ptax, dia, _cache={}):
    if dia in _cache:
        return _cache[dia]
    d = datetime.strptime(dia, "%Y-%m-%d")
    for _ in range(15):
        chave = d.strftime("%Y-%m-%d")
        if chave in ptax:
            _cache[dia] = ptax[chave]
            return ptax[chave]
        d -= timedelta(days=1)
    valor = ptax[max(ptax)]
    _cache[dia] = valor
    return valor


# ---------------------------------------------------------------------------
# Processamento
# ---------------------------------------------------------------------------

def nome_limpo(nome):
    return " ".join(str(nome or "Sem nome").split())


def processar(por_mes, ptax):
    vendas, reembolsos, vistos = [], [], set()
    taxas_moeda = {}  # média da real_conversion_rate por moeda (para reembolsos)

    # Conta dona do painel: quem recebe a comissão de produtor na maioria das vendas
    contagem = {}
    for dados in por_mes.values():
        for c in dados["comissoes"]:
            for x in c.get("commissions") or []:
                if x.get("source") == "PRODUCER":
                    u = (x.get("user") or {}).get("ucode")
                    contagem[u] = contagem.get(u, 0) + 1
    dono = max(contagem, key=contagem.get) if contagem else None

    for (a, m), dados in sorted(por_mes.items()):
        precos = {p["transaction"]: p for p in dados["precos"]}
        coms = {c["transaction"]: c for c in dados["comissoes"]}
        for v in dados["aprovadas"]:
            p = v.get("purchase") or {}
            t = p.get("transaction")
            if not t or t in vistos:
                continue
            vistos.add(t)
            ms = p.get("approved_date") or p.get("order_date")
            dt = datetime.fromtimestamp(ms / 1000, hm.FUSO)
            dia = dt.strftime("%Y-%m-%d")
            moeda = (p.get("price") or {}).get("currency_code", "BRL")
            det = precos.get(t) or {}
            taxa_conv = 1.0 if moeda == "BRL" else float(det.get("real_conversion_rate") or 0) or None
            if moeda != "BRL" and taxa_conv:
                taxas_moeda.setdefault(moeda, []).append(taxa_conv)
            if taxa_conv is None:
                continue  # sem taxa de conversão não dá para converter com segurança

            def em_reais(valor, cod):
                valor = float(valor or 0)
                if cod == "BRL":
                    return valor
                if cod == "USD":
                    return valor * ptax_do_dia(ptax, dia)
                if cod == moeda:
                    return valor / taxa_conv
                return 0.0

            bruto = em_reais((det.get("total") or {}).get("value", (p.get("price") or {}).get("value")), moeda)
            oferta = em_reais((det.get("base") or {}).get("value", (p.get("hotmart_fee") or {}).get("base")), moeda)
            taxa = em_reais((p.get("hotmart_fee") or {}).get("total"), moeda)
            recebido = repasse = club = 0.0
            for x in (coms.get(t) or {}).get("commissions") or []:
                val = em_reais((x.get("commission") or {}).get("value"), (x.get("commission") or {}).get("currency_code"))
                if (x.get("user") or {}).get("ucode") == dono:
                    recebido += val
                elif x.get("source") == "ADDON":
                    club += val
                else:
                    repasse += val
            pagamento = (p.get("payment") or {}).get("type") or "OUTRO"
            vendas.append({
                "a": dt.year, "m": dt.month, "d": dt.day,
                "p": nome_limpo((v.get("product") or {}).get("name")),
                "pg": pagamento, "mo": moeda,
                "br": round(bruto, 2), "of": round(oferta, 2), "tx": round(taxa, 2),
                "cl": round(club, 2), "rp": round(repasse, 2), "rc": round(recebido, 2),
            })
        for v in dados["reembolsos"]:
            p = v.get("purchase") or {}
            t = p.get("transaction")
            if not t or ("R" + t) in vistos:
                continue
            vistos.add("R" + t)
            ms = p.get("order_date") or p.get("approved_date")
            dt = datetime.fromtimestamp(ms / 1000, hm.FUSO)
            reembolsos.append({"a": dt.year, "m": dt.month, "p": nome_limpo((v.get("product") or {}).get("name")),
                               "_v": float((p.get("price") or {}).get("value") or 0),
                               "_mo": (p.get("price") or {}).get("currency_code", "BRL")})

    medias = {k: sum(v) / len(v) for k, v in taxas_moeda.items()}
    for r in reembolsos:
        mo, val = r.pop("_mo"), r.pop("_v")
        r["v"] = round(val if mo == "BRL" else (val / medias[mo] if medias.get(mo) else 0), 2)
    return vendas, reembolsos


# ---------------------------------------------------------------------------
# Painel
# ---------------------------------------------------------------------------

def gerar_html(vendas, reembolsos):
    produtos = sorted({v["p"] for v in vendas} | {r["p"] for r in reembolsos})
    idx = {nome: i for i, nome in enumerate(produtos)}
    pagamentos = sorted({v["pg"] for v in vendas})
    pidx = {nome: i for i, nome in enumerate(pagamentos)}
    linhas = [[v["a"], v["m"], v["d"], idx[v["p"]], pidx[v["pg"]], 0 if v["mo"] == "BRL" else 1,
               v["br"], v["of"], v["tx"], v["cl"], v["rp"], v["rc"]] for v in vendas]
    reemb = [[r["a"], r["m"], idx[r["p"]], r["v"]] for r in reembolsos]
    agora = datetime.now(hm.FUSO)
    pacote = {
        "atualizado": agora.strftime("%d/%m/%Y às %H:%M"),
        "hoje": [agora.year, agora.month, agora.day],
        "produtos": produtos, "pagamentos": pagamentos,
        "vendas": linhas, "reembolsos": reemb,
    }
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("/*__DADOS__*/null", json.dumps(pacote, ensure_ascii=False, separators=(",", ":")))
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(html, encoding="utf-8")
    return SAIDA


def main():
    ap = argparse.ArgumentParser(description="Gera o dashboard de faturamento Hotmart.")
    ap.add_argument("--desde", type=int, default=2023, help="Ano inicial (padrão 2023)")
    ap.add_argument("--tudo", action="store_true", help="Baixa todos os meses de novo, ignorando o cache")
    args = ap.parse_args()
    try:
        por_mes = coletar(args.desde, args.tudo)
        ptax = baixar_ptax(args.desde)
        vendas, reembolsos = processar(por_mes, ptax)
        caminho = gerar_html(vendas, reembolsos)
    except hm.ErroHotmart as e:
        log("Erro: %s" % e)
        sys.exit(1)
    total = sum(v["rc"] for v in vendas)
    log("Vendas processadas: %d | Reembolsos: %d | Recebido total: R$ %s" % (
        len(vendas), len(reembolsos), "{:,.2f}".format(total).replace(",", "X").replace(".", ",").replace("X", ".")))
    log("Painel salvo em: %s" % caminho)


if __name__ == "__main__":
    main()
