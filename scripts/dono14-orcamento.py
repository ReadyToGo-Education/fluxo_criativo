#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dono14-orcamento.py — Orcamento real dos conjuntos da campanha viva do Dono 14%.

Existe porque a rotina das 02h vinha repetindo, desde 24/08, o aviso "nao foi
possivel confirmar via API se a reducao de orcamento ja esta ativa". A chamada
inline era barrada pelo detector de padroes do terminal; num script proprio, com
o token lido do .env, ela passa e a pendencia deixa de existir.

Somente leitura (GET). Uso: py -3 scripts/dono14-orcamento.py
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CAMPANHA = "120247419652220527"   # [DONO14] [CONV] [LEADS] ABO
# O plano agora e por data, porque os conjuntos rodam em janelas com fim programado.
# Vale a ultima linha cuja data ja chegou. Fonte: decisoes do Rodrigo registradas no
# scripts/dono14-autorun-prompt.md. Datas futuras saem dos fins ja programados na conta.
PLANO_POR_DATA = [
    ("2026-09-11", 300.00, "A39 + A43 + A44 + A45 + A46"),
    ("2026-09-12", 390.00, "A39 + A43 + A44 + A45 + A46 + LAL (LAL antecipado pelo Rodrigo)"),
    ("2026-09-13", 270.00, "A39 + A45 + A46 + LAL (A43 e A44 vencem em 12/09)"),
    ("2026-09-15", 150.00, "A39 a R$ 90 + A40 a R$ 60 (A45, A46 e LAL pausados pelo Rodrigo)"),
    ("2026-09-17", 200.00, "A39 a R$ 100 + conjunto A47+A48+A49 a R$ 100 (criativos do briefing, fim 23/09)"),
    ("2026-09-18", 140.00, "A47 sozinho a R$ 100 (sem data de fim) + A39 a R$ 40"),
    ("2026-09-19", 200.00, "A47 R$ 100 + A39 R$ 40 + A48 R$ 60 (teste do A48 de 19/09 a 25/09)"),
    ("2026-09-26", 200.00, "A47 R$ 100 + A39 R$ 40 + A49 R$ 60 (teste do A49 de 26/09 a 02/10)"),
    ("2026-09-30", 160.00, "A39 R$ 100 + A47 R$ 60 (Rodrigo aposentou o A49 em 30/09 as 11h34, "
                           "dois dias antes do fim da janela, e remanejou a verba as 23h35)"),
    ("2026-10-10", 280.00, "A39 R$ 100 + A47 R$ 60 + A50 R$ 60 + A51 R$ 60 (teste de 7 dias do A50 e do A51, "
                           "de 10/10 a 16/10, decisao do Rodrigo em 09/10)"),
    ("2026-10-11", 260.00, "A39 R$ 80 + A47 R$ 60 + A50 R$ 60 + A51 R$ 60 (o Rodrigo baixou o A39 de R$ 100 "
                           "para R$ 80 em 10/10 as 19h33, depois de seis dias sem cadastro)"),
    ("2026-10-17", 140.00, "A39 R$ 80 + A47 R$ 60 (A50 e A51 vencem em 16/10 as 23h59)"),
]

# Divisao esperada POR CONJUNTO, a partir da data em que passou a valer.
# Existe porque o total sozinho engana: em 26/09 a conta virou A39 R$ 80 + A47 R$ 60
# + A49 R$ 60, que soma os mesmos R$ 200 do plano e o script dizia "APLICADO" por
# tres dias seguidos enquanto as duas ancoras estavam com o orcamento TROCADO.
COMPOSICAO_POR_DATA = [
    ("2026-09-19", {"A47": 100.0, "A39": 40.0, "A48": 60.0}),
    ("2026-09-26", {"A47": 100.0, "A39": 40.0, "A49": 60.0}),
    # 30/09: conferido no registro de atividades da conta. As 11h34 o Rodrigo pausou o
    # conjunto e o anuncio do A49 e baixou o A47 para R$ 40; as 11h40 pausou os conjuntos
    # ja vencidos (A43, A44 e A48); as 23h35 subiu o A47 para R$ 60 e o A39 para R$ 100.
    # O A39 virou a ancora principal, que e o que os dados de perfil pediam.
    ("2026-09-30", {"A39": 100.0, "A47": 60.0}),
    # 09/10: o Rodrigo publicou o A50 e o A51, um anuncio por conjunto, R$ 60/dia cada,
    # inicio 10/10 00h01 e fim 16/10 23h59. Conferido pela API no mesmo dia.
    ("2026-10-10", {"A39": 100.0, "A47": 60.0, "A50": 60.0, "A51": 60.0}),
    ("2026-10-11", {"A39": 80.0, "A47": 60.0, "A50": 60.0, "A51": 60.0}),
    ("2026-10-17", {"A39": 80.0, "A47": 60.0}),
]


def token():
    for linha in (Path(__file__).resolve().parent.parent / ".env").read_text(encoding="utf-8").splitlines():
        if linha.startswith("FB_ACCESS_TOKEN_PERMANENTE="):
            return linha.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("FB_ACCESS_TOKEN_PERMANENTE nao encontrado no .env")


p = {"fields": "name,daily_budget,effective_status,start_time,end_time", "limit": 100,
     "access_token": token(), "_": str(int(time.time()))}
url = f"https://graph.facebook.com/v21.0/{CAMPANHA}/adsets?" + urllib.parse.urlencode(p)
dados = json.loads(urllib.request.urlopen(url, timeout=90).read()).get("data", [])

print("=" * 62)
print("ORCAMENTO REAL NA CONTA (conjuntos ATIVOS)")
print("=" * 62)
SP = timezone(timedelta(hours=-3))
AGORA = datetime.now(SP)


def quando(s, campo):
    bruto = s.get(campo)
    if not bruto:
        return None
    try:
        return datetime.fromisoformat(bruto.replace("+0000", "+00:00")).astimezone(SP)
    except ValueError:
        return None


def ainda_nao_comecou(s):
    """Conjunto com inicio programado no futuro nao gasta hoje. A API ja o devolve
    como ACTIVE, e isso inflou o programado em R$ 90 em 12/09 (conjunto Lookalike
    marcado para comecar em 13/09), gerando alarme falso de divergencia."""
    ini = quando(s, "start_time")
    return bool(ini and ini > AGORA)


def venceu(s):
    """Conjunto com cronograma ja terminado nao entrega mais, mesmo que a API
    continue devolvendo effective_status ACTIVE. Em 09/09/2026 o A42 apareceu
    assim e inflou o programado em R$ 60, gerando alarme falso de divergencia."""
    bruto = s.get("end_time")
    if not bruto:
        return False
    try:
        return datetime.fromisoformat(bruto.replace("+0000", "+00:00")).astimezone(SP) < AGORA
    except ValueError:
        return False


total = 0.0
real_por_ad = {}
encerrados = []
agendados = []
for s in sorted(dados, key=lambda x: x.get("name", "")):
    if s.get("effective_status") != "ACTIVE":
        continue
    nome = (s.get("name") or "?")[:38]
    orc = int(s.get("daily_budget") or 0) / 100
    if venceu(s):
        encerrados.append((nome, orc, s.get("end_time")))
        continue
    if ainda_nao_comecou(s):
        agendados.append((nome, orc, quando(s, "start_time")))
        continue
    total += orc
    # Qualquer peca "A" seguida de dois digitos. Era uma lista fixa ate o A49, e em
    # 10/10/2026 o A50 e o A51 apareceram como "conta R$ 0" com o orcamento certo na conta.
    _m = re.match(r"A\d{2}", nome)
    if _m:
        real_por_ad[_m.group(0)] = real_por_ad.get(_m.group(0), 0.0) + orc
    fim = s.get("end_time")
    if fim:
        try:
            fim = datetime.fromisoformat(fim.replace("+0000", "+00:00")).astimezone(SP).strftime("  (termina %d/%m %Hh%M)")
        except ValueError:
            fim = ""
    print(f"  {nome:<40} R$ {orc:>7.2f}/dia{fim or ''}")

if agendados:
    print()
    print("  Ainda nao comecaram, entram no programado so na data (fora da soma de hoje):")
    for nome, orc, ini in agendados:
        print(f"    {nome:<38} R$ {orc:>7.2f}/dia, comeca em {ini.strftime('%d/%m %Hh%M')}")

if encerrados:
    print("\n  Cronograma ja vencido, nao entregam mais (fora da soma):")
    for nome, orc, fim in encerrados:
        print(f"    {nome:<38} R$ {orc:>7.2f}/dia, terminou em {str(fim)[:10]}")

pausados = sum(1 for s in dados if s.get("effective_status") != "ACTIVE")
print(f"\n  PROGRAMADO/DIA: R$ {total:.2f}   ({pausados} conjunto(s) pausado(s))")
hoje_iso = AGORA.strftime("%Y-%m-%d")
vigente = [x for x in PLANO_POR_DATA if x[0] <= hoje_iso] or [PLANO_POR_DATA[0]]
desde, PLANO_ATUAL, composicao = vigente[-1]
print(f"  PLANO COMBINADO: R$ {PLANO_ATUAL:.2f}/dia   (desde {desde[8:10]}/{desde[5:7]}: {composicao})")
vig_c = [x for x in COMPOSICAO_POR_DATA if x[0] <= hoje_iso]
esperado = vig_c[-1][1] if vig_c else {}
divergem = []
for sigla in sorted(set(esperado) | set(real_por_ad)):
    quer, tem = esperado.get(sigla, 0.0), real_por_ad.get(sigla, 0.0)
    if abs(quer - tem) >= 1:
        divergem.append((sigla, quer, tem))

if abs(total - PLANO_ATUAL) >= 1:
    print(f"  STATUS: DIVERGENTE NO TOTAL (conta em R$ {total:.0f}, plano R$ {PLANO_ATUAL:.0f}).")
    print("  Registrar no marcador e comparar o gasto com o valor REAL da conta.")
elif divergem:
    # O total bate e a divisao nao. Este ramo existe desde 29/09/2026: sem ele o
    # script dizia APLICADO com as ancoras trocadas.
    print("  STATUS: TOTAL BATE, DIVISAO DIVERGENTE. Conferir se foi decisao do Rodrigo.")
    for sigla, quer, tem in divergem:
        print(f"    {sigla}: plano R$ {quer:.0f}/dia, conta R$ {tem:.0f}/dia")
else:
    print("  STATUS: APLICADO (total e divisao). Comparar o gasto do dia com este valor.")
