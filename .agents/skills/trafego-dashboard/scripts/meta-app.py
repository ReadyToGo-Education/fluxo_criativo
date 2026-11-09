# -*- coding: utf-8 -*-
"""Coletor dos números da Meta pelo App, para o dashboard com dados gravados.

Serve para a conta de anúncios que a Meta ainda não liberou no conector (a liberação é
conta por conta). Lê o token FB_ACCESS_TOKEN_PERMANENTE no .env, busca na Graph API os
mesmos números que a página leria pelo conector e grava a pasta banco-meta/, que o
Claude envia para o banco do artefato (coleção "meta", ver SKILL.md, seção 5.1).

O token fica só no computador do aluno: entra apenas nas chamadas à Meta e nunca vai
para a página, para o banco do artefato, para os arquivos gravados nem para a tela.

Uso:
  python meta-app.py --verificar [--config {pasta}/config.json]
  python meta-app.py --config {pasta}/config.json --pasta {pasta}
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _vendas_comum as comum  # noqa: E402

VERSAO = "v25.0"
BASE = os.environ.get("META_GRAPH_BASE", "https://graph.facebook.com").rstrip("/")  # outro endereço só em teste
HORA = "hourly_stats_aggregated_by_advertiser_time_zone"
TAMANHO_LOTE = comum.TAMANHO_LOTE
LIMITE_DOC = 250_000  # bytes; o banco do artefato aceita até 256 KiB por documento
METRICAS = ["spend", "impressions", "inline_link_clicks", "actions", "action_values", "purchase_roas"]
CLIQUE = ["link_click"]
VISITA = ["landing_page_view", "omni_landing_page_view"]
CHECKOUT = ["omni_initiated_checkout", "offsite_conversion.fb_pixel_initiate_checkout", "initiate_checkout"]
COMPRA = ["omni_purchase", "purchase", "offsite_conversion.fb_pixel_purchase"]


class ErroMeta(Exception):
    def __init__(self, codigo, msg, cod_meta=None):
        super().__init__(msg)
        self.codigo, self.msg, self.cod_meta = codigo, msg, cod_meta


class Graph:
    """Chamadas GET à Graph API. O token nunca aparece em mensagem nem em saída."""

    def __init__(self, token):
        self._token = token
        self.chamadas = 0

    def _limpa(self, texto):
        return str(texto).replace(self._token, "***TOKEN_MASCARADO***")

    def get(self, caminho, params=None):
        q = {k: (json.dumps(v, separators=(",", ":")) if isinstance(v, (list, dict)) else v) for k, v in (params or {}).items()}
        q["access_token"] = self._token
        url = f"{BASE}/{VERSAO}/{caminho.lstrip('/')}?{urllib.parse.urlencode(q)}"
        for tentativa in range(3):
            self.chamadas += 1
            try:
                with urllib.request.urlopen(urllib.request.Request(url), timeout=90) as r:
                    return json.loads(r.read().decode("utf-8") or "{}")
            except urllib.error.HTTPError as e:
                corpo = e.read().decode("utf-8", "replace")
                try:
                    err = json.loads(corpo).get("error") or {}
                except ValueError:
                    err = {}
                cod = err.get("code")
                if (cod in (1, 2, 4, 17, 32, 613, 80004) or e.code >= 500) and tentativa < 2:
                    time.sleep(5 * (tentativa + 1))
                    continue
                if cod == 190 or e.code == 401:
                    raise ErroMeta("ERRO_TOKEN", "a Meta recusou o token do App (vencido, revogado ou sem permissão).", cod) from None
                msg = self._limpa(err.get("message") or corpo)[:300]
                raise ErroMeta("ERRO_META", f"a Meta respondeu {e.code} (código {cod}): {msg}", cod) from None
            except urllib.error.URLError as e:
                if tentativa < 2:
                    time.sleep(3)
                    continue
                raise ErroMeta("ERRO_META", f"sem conexão com a Meta: {self._limpa(e.reason)}") from None
        raise ErroMeta("ERRO_META", "a Meta não respondeu depois de 3 tentativas.")

    def todas(self, caminho, params):
        """Junta todas as páginas seguindo o cursor (nunca o link paging.next, que traz o token)."""
        out, after = [], None
        for _ in range(200):
            p = dict(params)
            if after:
                p["after"] = after
            r = self.get(caminho, p)
            out.extend(r.get("data") or [])
            pag = r.get("paging") or {}
            after = (pag.get("cursors") or {}).get("after")
            if not after or not pag.get("next"):
                break
        return out

    def por_ids(self, ids, campos):
        res = {}
        ids = list(ids)
        for i in range(0, len(ids), 50):
            res.update(self.get("", {"ids": ",".join(ids[i:i + 50]), "fields": campos}) or {})
        return res


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def acao(lista, tipos):
    if not isinstance(lista, list):
        return None
    por = {a.get("action_type"): num(a.get("value")) for a in lista if isinstance(a, dict)}
    for t in tipos:
        if por.get(t) is not None:
            return por[t]
    return None


def resultado(r):
    res = r.get("results")
    if isinstance(res, list):
        res = res[0] if res else None
    if isinstance(res, dict):
        vals = res.get("values") or []
        v = num(vals[0].get("value")) if vals and isinstance(vals[0], dict) else None
        return v or 0, res.get("indicator")
    return 0, None


def linha(r, extra):
    g = num(r.get("spend")) or 0
    vp = acao(r.get("action_values"), COMPRA)
    if vp is None:
        roas = acao(r.get("purchase_roas"), COMPRA)
        vp = roas * g if roas is not None else 0
    c = acao(r.get("actions"), CLIQUE)
    if c is None:
        c = num(r.get("inline_link_clicks")) or 0
    rs, tp = resultado(r)
    base = {"d": str(r.get("date_start") or "")[:10], "g": round(g, 2), "i": num(r.get("impressions")) or 0, "c": c,
            "v": acao(r.get("actions"), VISITA) or 0, "ic": acao(r.get("actions"), CHECKOUT) or 0,
            "cp": acao(r.get("actions"), COMPRA) or 0, "vp": round(vp or 0, 2), "rs": rs, "tp": tp}
    base.update(extra)
    return base


def orcamento(v):
    x = num(v)
    return round(x / 100, 2) if x else None  # a Graph API devolve orçamento em centavos


def id_conta(c):
    c = str(c).strip()
    return c if c.startswith("act_") else "act_" + c


def contas_do_dashboard(cfg, env):
    contas = [id_conta(c) for c in cfg.get("contas") or [] if str(c).strip()]
    if not contas:
        lista = comum.variavel("FB_AD_ACCOUNT_IDS", env) or comum.variavel("FB_AD_ACCOUNT_ID", env) or ""
        contas = [id_conta(c) for c in lista.split(",") if c.strip()]
    if not contas:
        raise SystemExit("ERRO_CONTA: nenhuma conta de anúncios no config.json nem no .env (FB_AD_ACCOUNT_ID).")
    return list(dict.fromkeys(contas))


def mascara(c):
    s = str(c)
    return s[:8] + "..." + s[-4:] if len(s) > 14 else s


class Coletor:
    def __init__(self, g):
        self.g = g
        self.com_resultado = True
        self.avisos = []

    def insights(self, conta, nivel, de, ate, campos, extra=None):
        base = {"level": nivel, "time_range": {"since": de, "until": ate}, "limit": 500}
        base.update(extra or {})
        if self.com_resultado:
            try:
                return self.g.todas(f"{conta}/insights", dict(base, fields=",".join(campos + ["results"])))
            except ErroMeta as e:
                if e.codigo != "ERRO_META" or e.cod_meta != 100:
                    raise
                self.com_resultado = False  # esta versão da API não tem o campo results: segue sem
                self.avisos.append("A Meta não informou o resultado do objetivo nesta conta. O modo resultados fica sem números.")
        return self.g.todas(f"{conta}/insights", dict(base, fields=",".join(campos)))


def coletar(g, contas, cfg):
    col = Coletor(g)
    infos = {c: g.get(c, {"fields": "name,currency,timezone_name,timezone_offset_hours_utc"}) for c in contas}
    primeira = infos[contas[0]]
    offset = num(primeira.get("timezone_offset_hours_utc"))
    agora = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=offset if offset is not None else -3)))
    hoje = agora.date()
    t = hoje.isoformat()
    inicio = (hoje - timedelta(days=30)).isoformat()
    janelas = [("hoje", t, t), ("ontem", (hoje - timedelta(days=1)).isoformat(), (hoje - timedelta(days=1)).isoformat()),
               ("7d", (hoje - timedelta(days=6)).isoformat(), t), ("14d", (hoje - timedelta(days=13)).isoformat(), t),
               ("30d", (hoje - timedelta(days=29)).isoformat(), t)]
    D = {"demo": False, "gravado": True, "fonte": "app", "hoje": t, "inicio": inicio, "horaAtual": agora.hour,
         "atualizadoEm": agora.strftime("%d/%m, %H:%M"), "geradoEmIso": agora.isoformat(timespec="seconds"),
         "moeda": cfg.get("moeda") or primeira.get("currency") or "BRL",
         "contas": [], "campanhas": [], "conjuntos": [], "anuncios": [], "metaDiaCamp": [], "metaDiaAd": [],
         "porHora": {}, "comprasHora": {}, "valorHora": {}, "porHoraC": {}, "alcance": {}, "avisos": []}
    for conta in contas:
        info = infos[conta]
        D["contas"].append({"id": conta, "nome": info.get("name") or conta, "moeda": info.get("currency") or D["moeda"]})
        dia = {"time_increment": 1}
        camps = {}
        for r in col.insights(conta, "campaign", inicio, t, ["campaign_id", "campaign_name", "date_start"] + METRICAS, dia):
            cid = str(r.get("campaign_id") or "")
            if not cid:
                continue
            camps.setdefault(cid, r.get("campaign_name") or cid)
            D["metaDiaCamp"].append(linha(r, {"conta": conta, "camp": cid}))
        meta_c = g.por_ids(camps, "name,effective_status,daily_budget") if camps else {}
        for cid, nome in camps.items():
            m = meta_c.get(cid) or {}
            D["campanhas"].append({"id": cid, "conta": conta, "nome": m.get("name") or nome, "status": m.get("effective_status"), "orcDia": orcamento(m.get("daily_budget"))})
        ads = {}
        for r in col.insights(conta, "ad", inicio, t, ["ad_id", "ad_name", "adset_id", "campaign_id", "date_start"] + METRICAS, dia):
            aid = str(r.get("ad_id") or "")
            if not aid:
                continue
            ads.setdefault(aid, {"id": aid, "campanha": str(r.get("campaign_id") or "") or None, "conjunto": str(r.get("adset_id") or "") or None, "nome": r.get("ad_name") or aid})
            D["metaDiaAd"].append(linha(r, {"conta": conta, "camp": ads[aid]["campanha"], "a": aid}))
        meta_a = g.por_ids(ads, "effective_status") if ads else {}
        for aid, a in ads.items():
            if a["campanha"]:
                D["anuncios"].append(dict(a, status=(meta_a.get(aid) or {}).get("effective_status")))
        for r in g.todas(f"{conta}/adsets", {"fields": "id,name,effective_status,daily_budget,campaign_id", "effective_status": ["ACTIVE"], "limit": 500}):
            D["conjuntos"].append({"id": str(r.get("id")), "campanha": str(r.get("campaign_id") or "") or None, "nome": r.get("name") or str(r.get("id")), "status": r.get("effective_status"), "orcDia": orcamento(r.get("daily_budget"))})
        for chave, de, ate in janelas:
            alvo = D["alcance"].setdefault(chave, {})
            for nivel, campo in (("campaign", "campaign_id"), ("ad", "ad_id")):
                for r in g.todas(f"{conta}/insights", {"level": nivel, "time_range": {"since": de, "until": ate}, "fields": f"{campo},reach", "limit": 500}):
                    rid, x = str(r.get(campo) or ""), num(r.get("reach"))
                    if rid and x is not None:
                        alvo[rid] = alvo.get(rid, 0) + x
        try:
            linhas_hora = g.todas(f"{conta}/insights", {"level": "account", "time_range": {"since": inicio, "until": t}, "time_increment": 1,
                                                      "breakdowns": HORA, "fields": "spend,actions,action_values,purchase_roas,date_start", "limit": 500})
        except ErroMeta as e:
            if e.codigo == "ERRO_TOKEN":
                raise
            linhas_hora = []
            col.avisos.append("A Meta não entregou a quebra por hora. O ritmo de hoje fica sem gráfico.")
        pc = {"g": {}, "cp": {}, "vp": {}}
        for r in linhas_hora:
            d = str(r.get("date_start") or "")[:10]
            try:
                h = int(str(r.get(HORA) or "").split(":")[0])
            except ValueError:
                continue
            if not d or not 0 <= h < 24:
                continue
            l = linha(r, {})
            for k in ("g", "cp", "vp"):
                pc[k].setdefault(d, [0] * 24)[h] += l[k]
        if linhas_hora:
            D["porHoraC"][conta] = pc
    if not D["metaDiaCamp"]:
        col.avisos.append("A Meta não devolveu gasto nos últimos 30 dias para " + ("estas contas." if len(contas) > 1 else "esta conta."))
    D["avisos"] = col.avisos
    return D


def gravar(pasta, D, token):
    """Grava banco-meta/: info.json com o que é pequeno e lote-N.json com as linhas por dia."""
    banco = Path(pasta) / "banco-meta"
    banco.mkdir(parents=True, exist_ok=True)
    for velho in banco.glob("*.json"):
        velho.unlink()
    itens = [("camp", x) for x in D["metaDiaCamp"]] + [("ad", x) for x in D["metaDiaAd"]] + [("anuncios", x) for x in D["anuncios"]]
    itens += [("alc", [k, rid, v]) for k, ids in D["alcance"].items() for rid, v in ids.items()]
    lotes, atual, tamanho = [], {}, 0
    for tipo, x in itens:
        tam = len(json.dumps(x, ensure_ascii=False)) + 1
        if atual and tamanho + tam > TAMANHO_LOTE:
            lotes.append(atual)
            atual, tamanho = {}, 0
        atual.setdefault(tipo, []).append(x)
        tamanho += tam
    if atual or not lotes:
        lotes.append(atual)
    info = {k: v for k, v in D.items() if k not in ("metaDiaCamp", "metaDiaAd", "anuncios", "alcance")}
    info["lotes"] = len(lotes)
    texto_info = json.dumps(info, ensure_ascii=False)
    if len(texto_info.encode("utf-8")) > LIMITE_DOC:
        raise SystemExit("ERRO_TAMANHO: a conta tem campanhas e conjuntos demais para um painel com dados gravados.")
    arquivos = {"info.json": texto_info}
    for n, lote in enumerate(lotes, 1):
        arquivos[f"lote-{n}.json"] = json.dumps(lote, ensure_ascii=False)
    for nome, texto in arquivos.items():
        if token in texto or "access_token" in texto:
            raise SystemExit("ERRO_SEGURANCA: o token apareceu nos dados. Nada foi gravado.")
    for nome, texto in arquivos.items():
        (banco / nome).write_text(texto, encoding="utf-8")
    return banco, len(lotes)


def main():
    ap = argparse.ArgumentParser(description="Números da Meta pelo App para o dashboard com dados gravados")
    ap.add_argument("--verificar", action="store_true", help="só confere se o token do App lê as contas")
    ap.add_argument("--config", help="config.json do dashboard")
    ap.add_argument("--pasta", help="pasta do dashboard (recebe banco-meta/)")
    a = ap.parse_args()
    env = comum.ler_env()
    token = comum.variavel("FB_ACCESS_TOKEN_PERMANENTE", env)
    if not token:
        raise SystemExit("ERRO_CREDENCIAIS: FB_ACCESS_TOKEN_PERMANENTE não está no .env. Configure o App pelo /trafego-conexao.")
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8")) if a.config else {}
    contas = contas_do_dashboard(cfg, env)
    g = Graph(token)
    try:
        if a.verificar:
            for c in contas:
                info = g.get(c, {"fields": "name,currency"})
                print(f"OK: o App lê a conta {info.get('name') or ''} ({mascara(c)}), moeda {info.get('currency') or '?'}.")
            return
        if not a.pasta:
            raise SystemExit("ERRO_USO: informe --pasta.")
        D = coletar(g, contas, cfg)
        banco, n = gravar(a.pasta, D, token)
    except ErroMeta as e:
        raise SystemExit(f"{e.codigo}: {e.msg}")
    print(f"OK: {len(D['campanhas'])} campanha(s), {len(D['anuncios'])} anúncio(s) e {len(D['conjuntos'])} conjunto(s) ativo(s) em {len(D['contas'])} conta(s), números de {D['atualizadoEm']}.")
    for av in D["avisos"]:
        print("AVISO: " + av)
    print(f"BANCO: coleção meta, documentos info e lote-1 a lote-{n}, arquivos em {banco}")


if __name__ == "__main__":
    main()
