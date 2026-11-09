"""
trafego_chart_geom.py
Gerador de geometria SVG reutilizavel para os dashboards do /trafego-analise.

NAO toca na Graph API, NAO usa token. Matematica pura: recebe um spec JSON
no stdin e devolve no stdout a geometria pronta (points, rects, paths, labels)
para o gerador de HTML apenas COLAR no template. Mantem todos os graficos
deterministicos, sem o modelo plotar dezenas/centenas de pontos a mao.

Uso:
    echo '{...spec...}' | python3 trafego_chart_geom.py <tipo>

Tipos suportados:
    line        linha (1+ series, eixo simples ou duplo, area opcional)
    vbars       barras verticais (1 grupo por categoria)
    heatmap     matriz colorida linhas x colunas
    gauge       medidor semicircular com zonas de cor
    dual_funnel dois funis lado a lado (largura em escala log)
    scatter     dispersao com linhas de quadrante
    radar       radar de N eixos (generaliza a receita A)

Saida: sempre um JSON com viewbox + os campos especificos do tipo.

Valor ausente (null) ou não numérico: nunca vira traceback. Em line o ponto é
pulado; em vbars, divbars, radar e scatter o item é omitido; em dual_funnel vira
0; no gauge sai {"error": "valor_ausente"}. O que foi pulado ou omitido aparece
no campo "avisos". Spec gravado com BOM (UTF-8 com assinatura) é aceito.

Receitas que CONSOMEM esta saida estao na secao 3.2.1 do _export-html.md
(F line, G vbars, H heatmap, I gauge, J dual_funnel, K scatter, L radar).
"""

import sys
import json
import math


def _read_spec():
    raw = sys.stdin.buffer.read().decode("utf-8-sig")
    return json.loads(raw) if raw.strip() else {}


def _num(v):
    """Número (float) ou None quando o valor falta ou não é numérico."""
    if v is None or isinstance(v, bool):
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def _com_avisos(res, avisos):
    if res is not None and avisos:
        res["avisos"] = avisos
    return res


def _write(obj):
    sys.stdout.buffer.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))
    sys.stdout.buffer.write(b"\n")


def _r(n, d=1):
    return round(float(n), d)


def _dd_mm(iso):
    """YYYY-MM-DD -> DD/MM (passa direto se nao for ISO)."""
    if isinstance(iso, str) and len(iso) >= 10 and iso[4] == "-" and iso[7] == "-":
        return iso[8:10] + "/" + iso[5:7]
    return str(iso)


# ── line ─────────────────────────────────────────────────────────────────────
def geom_line(spec):
    """Linha multi-serie com eixo simples ou duplo.

    spec = {
      "viewbox": [720, 240],            # opcional
      "pad": [54, 44, 16, 30],          # [left,right,top,bottom] opcional
      "x_labels": ["...", ...],         # rotulos do eixo X (datas ISO viram DD/MM); opcional
      "n_x_labels": 6,                  # quantos rotulos exibir (espacados); opcional
      "series": [
        {"name":"Gasto","color":"#3b82f6","axis":"left","values":[...],"area":true},
        {"name":"Vendas","color":"#10b981","axis":"right","values":[...],"dots":true}
      ]
    }
    Retorna: viewbox, baseline_y, plot_left, plot_right, grid_y, x_labels[],
    e por serie: points, area_points (se area), dots (se dots), axis, max, color, name.
    """
    vb_w, vb_h = spec.get("viewbox", [720, 240])
    pad_l, pad_r, pad_t, pad_b = spec.get("pad", [54, 44, 16, 30])
    series = spec.get("series", [])
    if not series:
        return None
    n = max(len(s.get("values", [])) for s in series)
    if n == 0:
        return None
    plot_w = vb_w - pad_l - pad_r
    plot_h = vb_h - pad_t - pad_b
    base_y = pad_t + plot_h
    num_left = [_num(v) for s in series if s.get("axis", "left") == "left" for v in s.get("values", [])]
    num_right = [_num(v) for s in series if s.get("axis") == "right" for v in s.get("values", [])]
    max_left = max([v for v in num_left if v is not None] + [0]) or 1.0
    max_right = max([v for v in num_right if v is not None] + [0]) or 1.0

    def px(i):
        return pad_l + (plot_w * i / (n - 1)) if n > 1 else pad_l + plot_w / 2.0

    def py(v, axis):
        mx = max_right if axis == "right" else max_left
        return pad_t + plot_h * (1 - v / mx)

    out_series = []
    avisos = []
    for s in series:
        axis = s.get("axis", "left")
        # (posição, valor numérico, valor original); ponto sem valor é pulado.
        vals = [(i, _num(v), v) for i, v in enumerate(s.get("values", []))]
        validos = [(i, f, v) for i, f, v in vals if f is not None]
        if len(validos) < len(vals):
            avisos.append("série {}: {} ponto(s) sem valor pulado(s)".format(
                s.get("name", ""), len(vals) - len(validos)))
        pts = " ".join("{},{}".format(_r(px(i)), _r(py(f, axis))) for i, f, _ in validos)
        item = {"name": s.get("name", ""), "color": s.get("color", "#3b82f6"), "axis": axis, "points": pts}
        if s.get("area"):
            item["area_points"] = "{},{} {} {},{}".format(_r(pad_l), _r(base_y), pts, _r(pad_l + plot_w), _r(base_y))
        if s.get("dots"):
            item["dots"] = [{"cx": _r(px(i)), "cy": _r(py(f, axis)), "v": v} for i, f, v in validos]
        out_series.append(item)

    n_lbl = spec.get("n_x_labels", min(6, n))
    raw_lbls = spec.get("x_labels", [])
    x_labels = []
    if raw_lbls:
        for k in range(min(n_lbl, n)):
            i = round(k * (n - 1) / (n_lbl - 1)) if n_lbl > 1 else 0
            if i < len(raw_lbls):
                x_labels.append({"x": _r(px(i)), "label": _dd_mm(raw_lbls[i])})

    grid_y = [_r(pad_t), _r(pad_t + plot_h / 2.0), _r(base_y)]
    return _com_avisos({
        "viewbox": "0 0 {} {}".format(vb_w, vb_h),
        "baseline_y": _r(base_y), "plot_left": _r(pad_l), "plot_right": _r(pad_l + plot_w),
        "grid_y": grid_y, "x_labels": x_labels,
        "max_left": _r(max_left, 2), "max_right": _r(max_right, 2),
        "series": out_series,
    }, avisos)


# ── vbars ────────────────────────────────────────────────────────────────────
def geom_vbars(spec):
    """Barras verticais. spec = {"viewbox":[w,h],"pad":[...],"bars":[{"label":..,"value":..,"color":..}]}."""
    vb_w, vb_h = spec.get("viewbox", [560, 240])
    pad_l, pad_r, pad_t, pad_b = spec.get("pad", [40, 16, 16, 34])
    avisos = []
    bars = []
    for b in spec.get("bars", []):
        f = _num(b.get("value", 0))
        if f is None:
            avisos.append("barra '{}' sem valor omitida".format(b.get("label", "")))
            continue
        bars.append((b, f))
    if not bars:
        return None
    plot_w = vb_w - pad_l - pad_r
    plot_h = vb_h - pad_t - pad_b
    base_y = pad_t + plot_h
    mx = max((f for _, f in bars), default=0) or 1.0
    n = len(bars)
    slot = plot_w / n
    bw = slot * 0.6
    out = []
    for i, (b, f) in enumerate(bars):
        h = plot_h * (f / mx)
        x = pad_l + slot * i + (slot - bw) / 2.0
        out.append({
            "x": _r(x), "y": _r(base_y - h), "w": _r(bw), "h": _r(h),
            "cx": _r(x + bw / 2.0), "label": b.get("label", ""),
            "color": b.get("color", "#3b82f6"), "value": b.get("value", 0),
        })
    return _com_avisos({
        "viewbox": "0 0 {} {}".format(vb_w, vb_h),
        "baseline_y": _r(base_y), "plot_left": _r(pad_l), "plot_right": _r(pad_l + plot_w),
        "max": _r(mx, 2), "bars": out,
    }, avisos)


# ── heatmap ──────────────────────────────────────────────────────────────────
def _lerp_color(c1, c2, t):
    def hx(c):
        c = c.lstrip("#")
        return [int(c[i:i + 2], 16) for i in (0, 2, 4)]
    a, b = hx(c1), hx(c2)
    return "#" + "".join("{:02x}".format(int(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def geom_heatmap(spec):
    """Matriz colorida. spec = {
        "viewbox":[w,h],"pad":[...],"rows":["Dom",..],"cols":["0h",..],
        "matrix":[[v,..],..],            # rows x cols
        "scale":"intensity"|"good_low"|"good_high", "empty_fill":"#0d0d0d",
        "intensity_base":"#0d1f2d", "intensity_accent":"#3b82f6",   # tema (CORES_GRAFICO 3.2.c)
        "good_color":"#10b981", "bad_color":"#ef4444"               # tema (CORES_GRAFICO 3.2.c)
      }
    intensity: baixo->fundo, alto->accent. good_low: baixo=verde, alto=vermelho.
    good_high: baixo=vermelho, alto=verde. None/0 podem virar empty_fill.
    Defaults de cor = tema Escuro; nos temas Terra/Claro Neutro passar os valores do tema no spec.
    """
    vb_w, vb_h = spec.get("viewbox", [720, 300])
    pad_l, pad_r, pad_t, pad_b = spec.get("pad", [70, 12, 28, 12])
    rows = spec.get("rows", [])
    cols = spec.get("cols", [])
    matrix = spec.get("matrix", [])
    scale = spec.get("scale", "intensity")
    empty_fill = spec.get("empty_fill", "#0d0d0d")
    intensity_base = spec.get("intensity_base", "#0d1f2d")
    intensity_accent = spec.get("intensity_accent", "#3b82f6")
    good_color = spec.get("good_color", "#10b981")
    bad_color = spec.get("bad_color", "#ef4444")
    if not matrix or not rows or not cols:
        return None
    nr, nc = len(rows), len(cols)
    plot_w = vb_w - pad_l - pad_r
    plot_h = vb_h - pad_t - pad_b
    cw = plot_w / nc
    ch = plot_h / nr
    flat = [f for r in matrix for f in (_num(v) for v in r) if f is not None]
    vmin = min(flat) if flat else 0.0
    vmax = max(flat) if flat else 1.0
    span = (vmax - vmin) or 1.0

    def color(v):
        v = _num(v)
        if v is None:
            return empty_fill
        t = (v - vmin) / span
        if scale == "good_low":
            return _lerp_color(good_color, bad_color, t)
        if scale == "good_high":
            return _lerp_color(bad_color, good_color, t)
        return _lerp_color(intensity_base, intensity_accent, t)  # intensity

    cells = []
    for ri in range(nr):
        linha = matrix[ri] if ri < len(matrix) else []
        for ci in range(nc):
            v = linha[ci] if ci < len(linha) else None
            cells.append({
                "x": _r(pad_l + cw * ci), "y": _r(pad_t + ch * ri),
                "w": _r(cw - 1.5), "h": _r(ch - 1.5),
                "fill": color(v), "value": v, "row": ri, "col": ci,
            })
    col_labels = [{"x": _r(pad_l + cw * (ci + 0.5)), "label": c} for ci, c in enumerate(cols)]
    row_labels = [{"y": _r(pad_t + ch * (ri + 0.5) + 3), "label": r} for ri, r in enumerate(rows)]
    return {
        "viewbox": "0 0 {} {}".format(vb_w, vb_h),
        "cells": cells, "col_labels": col_labels, "row_labels": row_labels,
        "label_x": _r(pad_l - 8), "col_label_y": _r(pad_t - 10),
        "vmin": _r(vmin, 2), "vmax": _r(vmax, 2),
    }


# ── gauge ────────────────────────────────────────────────────────────────────
def _polar(cx, cy, r, deg):
    rad = math.radians(deg)
    return (cx + r * math.cos(rad), cy + r * math.sin(rad))


def _arc_path(cx, cy, r, a0, a1):
    """Arco de a0 a a1 graus (0=direita, 180=esquerda; semicirculo superior usa 180->360)."""
    x0, y0 = _polar(cx, cy, r, a0)
    x1, y1 = _polar(cx, cy, r, a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return "M {} {} A {} {} 0 {} {} {} {}".format(_r(x0), _r(y0), _r(r), _r(r), large, sweep, _r(x1), _r(y1))


def geom_gauge(spec):
    """Medidor semicircular (180deg). spec = {
        "viewbox":[w,h],"value":x,"max":y,"label":"...","unit":"%",
        "zones":[{"upto":0.5,"color":"#ef4444"},{"upto":0.8,"color":"#f59e0b"},{"upto":1.0,"color":"#10b981"}]
      }
    Semicirculo de 180deg (esquerda) a 360deg (direita) por cima.
    """
    vb_w, vb_h = spec.get("viewbox", [320, 200])
    cx = vb_w / 2.0
    cy = vb_h - 30
    r = min(vb_w / 2.0 - 24, vb_h - 60)
    value = _num(spec.get("value", 0))
    if value is None:
        return {"error": "valor_ausente", "tipo": "gauge"}
    mx = _num(spec.get("max", 1)) or 1.0
    frac = max(0.0, min(1.0, value / mx))
    zones = spec.get("zones", [{"upto": 1.0, "color": "#3b82f6"}])
    # Angulos: 180 (esq) -> 360 (dir), por cima.
    def ang(f):
        return 180 + 180 * f
    arcs = []
    prev = 0.0
    for z in zones:
        upto = min(1.0, z.get("upto", 1.0))
        arcs.append({"path": _arc_path(cx, cy, r, ang(prev), ang(upto)), "color": z.get("color", "#3b82f6")})
        prev = upto
    val_arc = _arc_path(cx, cy, r, ang(0.0), ang(frac))
    nx, ny = _polar(cx, cy, r, ang(frac))
    return {
        "viewbox": "0 0 {} {}".format(vb_w, vb_h),
        "cx": _r(cx), "cy": _r(cy), "r": _r(r),
        "track": _arc_path(cx, cy, r, 180, 360),
        "zone_arcs": arcs, "value_arc": val_arc,
        "needle": {"x": _r(nx), "y": _r(ny)},
        "value": value, "max": mx, "frac": _r(frac, 3),
        "label": spec.get("label", ""), "unit": spec.get("unit", ""),
    }


# ── dual_funnel ──────────────────────────────────────────────────────────────
def geom_dual_funnel(spec):
    """Dois funis lado a lado, largura em escala log do topo. spec = {
        "viewbox":[w,h],
        "a":{"name":"Camp A","stages":[{"label":"Impr","value":..},..]},
        "b":{"name":"Camp B","stages":[...]}
      }
    Retorna por lado: name + stages[{label,value,width_pct,meta_pct}].
    width_pct = log10(v)/log10(topo)*100 (mesma logica do funil B simples).
    meta_pct = v/estagio_anterior*100.
    """
    def build(side):
        stages = side.get("stages", [])
        if not stages:
            return None
        # Estágio sem valor conta como 0 (funil sem aquele evento).
        top = _num(stages[0].get("value", 0)) or 1
        log_top = math.log10(top) if top > 1 else 1.0
        out = []
        for i, st in enumerate(stages):
            v = _num(st.get("value", 0)) or 0
            w = (math.log10(v) / log_top * 100) if (v > 1 and log_top > 0) else (0.0 if v <= 1 else 100.0)
            meta = None
            if i > 0:
                prev = _num(stages[i - 1].get("value", 0)) or 0
                meta = _r(v / prev * 100, 1) if prev else None
            valor_original = st.get("value") if _num(st.get("value")) is not None else 0
            out.append({"label": st.get("label", ""), "value": valor_original, "width_pct": _r(max(8.0, w), 1), "meta_pct": meta})
        return {"name": side.get("name", ""), "stages": out}

    return {
        "viewbox": "0 0 {} {}".format(*spec.get("viewbox", [720, 300])),
        "a": build(spec.get("a", {})), "b": build(spec.get("b", {})),
    }


# ── scatter ──────────────────────────────────────────────────────────────────
def geom_scatter(spec):
    """Dispersao com linhas de quadrante. spec = {
        "viewbox":[w,h],"pad":[...],
        "points":[{"x":..,"y":..,"label":..,"color":..,"r":..}],
        "x_mid":..,"y_mid":..,    # linhas de quadrante (valor no dominio); opcional
        "x_label":"CPC","y_label":"Connect %"
      }
    Escala automatica para [min,max] de cada eixo (com 8% de folga). O x_mid e
    o y_mid entram no mínimo e no máximo: as linhas de quadrante ficam sempre
    dentro da área, mesmo com todos os pontos do mesmo lado.
    """
    vb_w, vb_h = spec.get("viewbox", [560, 320])
    pad_l, pad_r, pad_t, pad_b = spec.get("pad", [48, 18, 18, 34])
    avisos = []
    pts = []
    for p in spec.get("points", []):
        x, y = _num(p.get("x")), _num(p.get("y"))
        if x is None or y is None:
            avisos.append("ponto '{}' sem x ou y omitido".format(p.get("label", "")))
            continue
        pts.append(dict(p, x=x, y=y))
    if not pts:
        return None
    xs = [p["x"] for p in pts]
    ys = [p["y"] for p in pts]
    # Linhas de quadrante entram na escala: sem isso, com todos os pontos de um
    # lado da linha, ela cairia fora da área do gráfico.
    x_mid, y_mid = _num(spec.get("x_mid")), _num(spec.get("y_mid"))
    if x_mid is not None:
        xs.append(x_mid)
    if y_mid is not None:
        ys.append(y_mid)
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    xpad = (xmax - xmin) * 0.08 or 1.0
    ypad = (ymax - ymin) * 0.08 or 1.0
    xmin -= xpad; xmax += xpad; ymin -= ypad; ymax += ypad
    plot_w = vb_w - pad_l - pad_r
    plot_h = vb_h - pad_t - pad_b

    def sx(x):
        return pad_l + plot_w * (x - xmin) / ((xmax - xmin) or 1)

    def sy(y):
        return pad_t + plot_h * (1 - (y - ymin) / ((ymax - ymin) or 1))

    out_pts = [{
        "cx": _r(sx(p["x"])), "cy": _r(sy(p["y"])), "r": p.get("r", 4),
        "color": p.get("color", "#3b82f6"), "label": p.get("label", ""),
    } for p in pts]
    res = {
        "viewbox": "0 0 {} {}".format(vb_w, vb_h),
        "plot_left": _r(pad_l), "plot_right": _r(pad_l + plot_w),
        "plot_top": _r(pad_t), "plot_bottom": _r(pad_t + plot_h),
        "points": out_pts,
        "x_label": spec.get("x_label", ""), "y_label": spec.get("y_label", ""),
    }
    if x_mid is not None:
        res["x_mid_px"] = _r(sx(x_mid))
    if y_mid is not None:
        res["y_mid_px"] = _r(sy(y_mid))
    return _com_avisos(res, avisos)


# ── radar (N eixos) ──────────────────────────────────────────────────────────
def geom_radar(spec):
    """Radar de N eixos (generaliza a receita A para qualquer nº de dimensões).

    spec = {
      "viewbox":[360,320],"max":100,"rings":[100,50],
      "axes":[{"label":"...","value":0..max,"color":"#..."}]
    }
    Saída: grid_polys (anéis), axis_lines, data_points (polígono de dados),
    vertices[{x,y,color,value}], labels[{x,y,anchor,text}]. Primeiro eixo no topo.
    """
    vb_w, vb_h = spec.get("viewbox", [360, 320])
    avisos = []
    axes = []
    for a in spec.get("axes", []):
        f = _num(a.get("value", 0))
        if f is None:
            avisos.append("eixo '{}' sem valor omitido".format(a.get("label", "")))
            continue
        axes.append(dict(a, _v=f))
    mx = _num(spec.get("max", 100)) or 100.0
    rings = spec.get("rings", [mx, mx / 2.0])
    n = len(axes)
    if n < 3:
        return None
    cx, cy = vb_w / 2.0, vb_h / 2.0 + 6
    R = min(vb_w, vb_h) / 2.0 - 46

    def pt(frac, i):
        ang = math.radians(-90 + 360.0 * i / n)
        return (cx + R * frac * math.cos(ang), cy + R * frac * math.sin(ang))

    grid_polys = []
    for ring in rings:
        f = ring / mx
        grid_polys.append(" ".join("{},{}".format(_r(pt(f, i)[0]), _r(pt(f, i)[1])) for i in range(n)))
    axis_lines = []
    for i in range(n):
        x, y = pt(1.0, i)
        axis_lines.append({"x2": _r(x), "y2": _r(y)})
    data_pts = " ".join("{},{}".format(_r(pt(min(a["_v"] / mx, 1.0), i)[0]),
                                       _r(pt(min(a["_v"] / mx, 1.0), i)[1])) for i, a in enumerate(axes))
    vertices = []
    labels = []
    for i, a in enumerate(axes):
        f = min(a["_v"] / mx, 1.0)
        vx, vy = pt(f, i)
        vertices.append({"x": _r(vx), "y": _r(vy), "color": a.get("color", "#3b82f6"), "value": a.get("value", 0)})
        lx, ly = pt(1.18, i)
        anchor = "middle" if abs(lx - cx) < 12 else ("start" if lx > cx else "end")
        # Clamp: mantem o texto dentro do viewBox (estimativa ~6.6px/char em mono 11px),
        # senao rotulos longos ancorados a esquerda/direita saem cortados (ex: "Consistência").
        text = a.get("label", "")
        est = len(text) * 6.6
        if anchor == "end":
            lx = max(lx, est + 4)
        elif anchor == "start":
            lx = min(lx, vb_w - 4 - est)
        else:
            lx = min(max(lx, est / 2 + 4), vb_w - 4 - est / 2)
        ly = min(max(ly, 12), vb_h - 4)
        labels.append({"x": _r(lx), "y": _r(ly), "anchor": anchor, "text": text})
    return _com_avisos({
        "viewbox": "0 0 {} {}".format(vb_w, vb_h), "cx": _r(cx), "cy": _r(cy), "r": _r(R),
        "grid_polys": grid_polys, "axis_lines": axis_lines,
        "data_points": data_pts, "vertices": vertices, "labels": labels,
    }, avisos)


# ── divbars (barras divergentes +/- com linha do zero) ───────────────────────
def geom_divbars(spec):
    """Barras verticais divergentes (valores positivos e negativos, linha do zero).

    Usado pelo painel de decisao da /trafego-otimizar: lucro/dia por campanha,
    verde pra cima (lucra), vermelho pra baixo (queima). NAO altera geom_vbars.

    spec = {"viewbox":[w,h],"pad":[l,r,t,b],"bars":[{"label":..,"value":..,"color":..}]}
    Retorna zero_y + bars[{x,y,w,h,cx,label,color,value,sign}].
    """
    vb_w, vb_h = spec.get("viewbox", [560, 260])
    pad_l, pad_r, pad_t, pad_b = spec.get("pad", [40, 16, 18, 40])
    avisos = []
    bars = []
    for b in spec.get("bars", []):
        f = _num(b.get("value", 0))
        if f is None:
            avisos.append("barra '{}' sem valor omitida".format(b.get("label", "")))
            continue
        bars.append((b, f))
    if not bars:
        return None
    plot_w = vb_w - pad_l - pad_r
    plot_h = vb_h - pad_t - pad_b
    vals = [f for _, f in bars]
    vmax = max(vals + [0])
    vmin = min(vals + [0])
    rng = (vmax - vmin) or 1.0
    zero_y = pad_t + plot_h * (vmax / rng)
    n = len(bars)
    slot = plot_w / n
    bw = slot * 0.6
    out = []
    for i, (b, v) in enumerate(bars):
        x = pad_l + slot * i + (slot - bw) / 2.0
        h = plot_h * (abs(v) / rng)
        y = zero_y - h if v >= 0 else zero_y
        out.append({
            "x": _r(x), "y": _r(y), "w": _r(bw), "h": _r(h),
            "cx": _r(x + bw / 2.0), "label": b.get("label", ""),
            "color": b.get("color", "#3b82f6"), "value": b.get("value", 0),
            "sign": "pos" if v >= 0 else "neg",
        })
    return _com_avisos({
        "viewbox": "0 0 {} {}".format(vb_w, vb_h),
        "zero_y": _r(zero_y), "plot_left": _r(pad_l), "plot_right": _r(pad_l + plot_w),
        "vmax": _r(vmax, 2), "vmin": _r(vmin, 2), "bars": out,
    }, avisos)


DISPATCH = {
    "line": geom_line, "vbars": geom_vbars, "heatmap": geom_heatmap,
    "gauge": geom_gauge, "dual_funnel": geom_dual_funnel, "scatter": geom_scatter,
    "radar": geom_radar, "divbars": geom_divbars,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in DISPATCH:
        sys.stderr.write("Uso: echo '<spec json>' | python3 trafego_chart_geom.py <{}>\n".format("|".join(DISPATCH)))
        sys.exit(2)
    try:
        spec = _read_spec()
    except ValueError as e:
        _write({"error": "json_invalido", "tipo": sys.argv[1], "detalhe": str(e)[:200]})
        return
    try:
        out = DISPATCH[sys.argv[1]](spec)
    except (ValueError, TypeError, KeyError, AttributeError, ZeroDivisionError) as e:
        _write({"error": "spec_invalido", "tipo": sys.argv[1],
                "detalhe": "{}: {}".format(type(e).__name__, str(e)[:200])})
        return
    _write(out if out is not None else {"error": "spec_invalido_ou_vazio", "tipo": sys.argv[1]})


if __name__ == "__main__":
    main()
