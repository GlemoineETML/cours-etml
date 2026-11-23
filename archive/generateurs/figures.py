# -*- coding: utf-8 -*-
"""Figures CEI pour le cours "La source reelle et en charge" - ETML El Dim1."""
import os, cairosvg

NAVY = "#242852"
BLUE = "#297FD5"
LBLUE = "#ACCBF9"
RED = "#EE0000"
GREY = "#7F8FA9"
FONT = "Carlito, Calibri, sans-serif"

def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{FONT}">'
            '<defs>'
            f'<marker id="ar" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
            f'<path d="M0,0 L10,4 L0,8 z" fill="{NAVY}"/></marker>'
            f'<marker id="arR" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
            f'<path d="M0,0 L10,4 L0,8 z" fill="{RED}"/></marker>'
            f'<marker id="arB" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
            f'<path d="M0,0 L10,4 L0,8 z" fill="{BLUE}"/></marker>'
            f'<marker id="arV" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
            f'<path d="M0,0 L10,4 L0,8 z" fill="#26663F"/></marker>'
            '</defs>')

TAIL = '</svg>'

_SUB = __import__("re").compile(r"_\{([^}]*)\}|_([A-Za-z0-9]+)")


def _xml(t):
    """Echappe les caracteres interdits dans un noeud texte SVG."""
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def indices(txt, size=17):
    """Transforme C_{AB} ou C_1 en veritable indice typographique."""
    txt = _xml(txt)
    out, pos = [], 0
    sz = round(size * 0.72, 1)
    dy = round(size * 0.26, 1)
    for m in _SUB.finditer(txt):
        if m.start() > pos:
            out.append(txt[pos:m.start()])
        idx = m.group(1) if m.group(1) is not None else m.group(2)
        out.append('<tspan dy="%s" font-size="%s">%s</tspan>' % (dy, sz, idx))
        out.append('<tspan dy="-%s" font-size="%s">' % (dy, size))
        pos = m.end()
        out.append("__CLOSE__")
    out.append(txt[pos:])
    body = "".join(out)
    return body.replace("__CLOSE__", "") + "</tspan>" * body.count("__CLOSE__")


def T(x, y, s, size=17, col=NAVY, anchor="middle", weight="normal", style="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}">{indices(str(s), size)}</text>')


_SUBFIN = __import__("re").compile(r"_(?:\{([^}]*)\}|([A-Za-z0-9]+))$")


def Tend(x, y, s, size=17, col=NAVY, weight="normal", style="normal"):
    """Texte aligne a droite dont l'indice final est place a la main.

    cairosvg positionne mal un tspan d'indice dans un texte ancre a droite :
    on coupe donc la chaine en deux textes distincts.
    """
    s = str(s)
    m = _SUBFIN.search(s)
    if not m:
        return T(x, y, s, size, col, "end", weight, style)
    base = s[:m.start()]
    sub = m.group(1) if m.group(1) is not None else m.group(2)
    sz = round(size * 0.72, 1)
    dy = round(size * 0.26, 1)
    sw = round(0.58 * sz * len(sub), 1)
    return (T(x - sw, y, base, size, col, "end", weight, style)
            + T(x - sw, y + dy, sub, sz, col, "start", weight, style))


def W(pts, col=NAVY, wd=2.6):
    d = " ".join(("M" if i == 0 else "L") + f"{p[0]},{p[1]}" for i, p in enumerate(pts))
    return f'<path d="{d}" stroke="{col}" stroke-width="{wd}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'

def res_h(cx, cy, w=64, h=26, col=NAVY):
    """Resistance CEI : rectangle, bornes horizontales."""
    return (f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="#FFFFFF" '
            f'stroke="{col}" stroke-width="2.6"/>')

def res_v(cx, cy, w=26, h=64, col=NAVY):
    return (f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="#FFFFFF" '
            f'stroke="{col}" stroke-width="2.6"/>')

def src_h(cx, cy, r=24, col=NAVY):
    """Source de tension ideale CEI : cercle + trait PARALLELE a l'axe des bornes."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{col}" stroke-width="2.6"/>'
            f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="{col}" stroke-width="2.6"/>')

def src_v(cx, cy, r=24, col=NAVY):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{col}" stroke-width="2.6"/>'
            f'<line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}" stroke="{col}" stroke-width="2.6"/>')

def isrc_v(cx, cy, r=24, col=NAVY):
    """Source de courant ideale : trait PERPENDICULAIRE aux bornes."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{col}" stroke-width="2.6"/>'
            f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="{col}" stroke-width="2.6"/>')

def pile_v(cx, cy, col=NAVY):
    """Accumulateur CEI : trait long fin (+) et trait court epais (-)."""
    return (f'<line x1="{cx-20}" y1="{cy-8}" x2="{cx+20}" y2="{cy-8}" stroke="{col}" stroke-width="2.6"/>'
            f'<line x1="{cx-10}" y1="{cy+8}" x2="{cx+10}" y2="{cy+8}" stroke="{col}" stroke-width="6"/>')

def lampe(cx, cy, r=20, col=NAVY):
    k = r * 0.707
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{col}" stroke-width="2.6"/>'
            f'<line x1="{cx-k}" y1="{cy-k}" x2="{cx+k}" y2="{cy+k}" stroke="{col}" stroke-width="2.6"/>'
            f'<line x1="{cx-k}" y1="{cy+k}" x2="{cx+k}" y2="{cy-k}" stroke="{col}" stroke-width="2.6"/>')

def meter(cx, cy, letter, r=20, col=NAVY):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{col}" stroke-width="2.6"/>'
            + T(cx, cy + 7, letter, 20, col, weight="bold"))

def varres_h(cx, cy, col=NAVY):
    return (res_h(cx, cy, 64, 26, col)
            + f'<line x1="{cx-32}" y1="{cy+22}" x2="{cx+30}" y2="{cy-22}" stroke="{col}" '
              f'stroke-width="2.6" marker-end="url(#ar)"/>')

def switch(x, y, col=NAVY):
    return (W([(x, y), (x + 8, y)], col) + W([(x + 8, y), (x + 38, y - 20)], col)
            + W([(x + 46, y), (x + 54, y)], col)
            + f'<circle cx="{x+8}" cy="{y}" r="3.2" fill="{col}"/>'
            + f'<circle cx="{x+46}" cy="{y}" r="3.2" fill="{col}"/>')

def varrow(x, y1, y2, label, col=NAVY, side="right", size=17):
    """Fleche de tension verticale (du + vers le -)."""
    a = (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{col}" stroke-width="2.2" '
         f'marker-end="url({"#arR" if col==RED else "#arB" if col==BLUE else "#ar"})"/>')
    tx = x + 10 if side == "right" else x - 10
    an = "start" if side == "right" else "end"
    return a + T(tx, (y1 + y2) / 2 + 6, label, size, col, anchor=an)

def harrow(y, x1, x2, label, col=NAVY, above=True, size=17):
    a = (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="2.2" '
         f'marker-end="url({"#arR" if col==RED else "#arB" if col==BLUE else "#ar"})"/>')
    return a + T((x1 + x2) / 2, y - 9 if above else y + 20, label, size, col)

OUT = os.path.dirname(os.path.abspath(__file__))

def save(name, svg, scale=2.6):
    p = os.path.join(OUT, name + ".svg")
    open(p, "w", encoding="utf-8").write(svg)
    cairosvg.svg2png(url=p, write_to=os.path.join(OUT, name + ".png"), scale=scale,
                     background_color="white")
    print("ok", name)
