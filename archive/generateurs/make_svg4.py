# -*- coding: utf-8 -*-
"""Chapitre 300 — champ électrique et condensateur. Schémas CEI.

Conventions (identiques au chapitre 140) :
  · COURANT  = pointe de flèche POSÉE SUR LE CONDUCTEUR, repère indicé à côté.
  · TENSION  = flèche tracée À CÔTÉ du composant, du + vers le −, repère indicé.
"""
from figures import *
from make_svg3 import node, lab, ih, iv, uh, source

SMALL = 14


# --------------------------------------------------------------- composants
def cap_h(cx, cy, plate=34, gap=6, col=NAVY):
    """Condensateur CEI horizontal : deux armatures verticales, bornes en x."""
    h = plate / 2
    return (f'<line x1="{cx-gap}" y1="{cy-h}" x2="{cx-gap}" y2="{cy+h}" stroke="{col}" '
            f'stroke-width="3.4"/>'
            f'<line x1="{cx+gap}" y1="{cy-h}" x2="{cx+gap}" y2="{cy+h}" stroke="{col}" '
            f'stroke-width="3.4"/>')


def cap_v(cx, cy, plate=34, gap=6, col=NAVY):
    """Condensateur CEI vertical : deux armatures horizontales, bornes en y."""
    w = plate / 2
    return (f'<line x1="{cx-w}" y1="{cy-gap}" x2="{cx+w}" y2="{cy-gap}" stroke="{col}" '
            f'stroke-width="3.4"/>'
            f'<line x1="{cx-w}" y1="{cy+gap}" x2="{cx+w}" y2="{cy+gap}" stroke="{col}" '
            f'stroke-width="3.4"/>')


def capw_h(x0, x1, cy, nom=None, val=None, col=NAVY, dy=-26, sz=16, dyv=36):
    """Condensateur horizontal câblé de x0 à x1."""
    cx = (x0 + x1) / 2
    s = W([(x0, cy), (cx - 6, cy)], col, 2.6) + W([(cx + 6, cy), (x1, cy)], col, 2.6)
    s += cap_h(cx, cy, col=col)
    if nom:
        s += T(cx, cy + dy, nom, sz, col, style="italic", weight="bold")
    if val:
        s += T(cx, cy + dyv, val, sz - 2, col)
    return s


def capw_v(cy0, cy1, cx, nom=None, val=None, col=NAVY, side="right"):
    """Condensateur vertical câblé de cy0 à cy1."""
    cy = (cy0 + cy1) / 2
    s = W([(cx, cy0), (cx, cy - 6)], col, 2.6) + W([(cx, cy + 6), (cx, cy1)], col, 2.6)
    s += cap_v(cx, cy, col=col)
    tx = cx + 24 if side == "right" else cx - 24
    an = "start" if side == "right" else "end"
    if nom:
        s += T(tx, cy - 2, nom, 16, col, anchor=an, style="italic", weight="bold")
    if val:
        s += T(tx, cy + 17, val, 14, col, anchor=an)
    return s


def switch_open(x, y, col=NAVY, nom=None):
    """Interrupteur CEI ouvert, bornes en x et x+54."""
    s = (W([(x, y), (x + 8, y)], col) + W([(x + 8, y), (x + 40, y - 22)], col)
         + W([(x + 46, y), (x + 54, y)], col)
         + f'<circle cx="{x+8}" cy="{y}" r="3.4" fill="{col}"/>'
         + f'<circle cx="{x+46}" cy="{y}" r="3.4" fill="{col}"/>')
    if nom:
        s += T(x + 27, y - 32, nom, 16, col, style="italic", weight="bold")
    return s


def plus_moins(x, cy, col=NAVY):
    return (T(x, cy - 8, "+", 17, col, anchor="start", weight="bold")
            + T(x, cy + 26, "−", 17, col, anchor="start", weight="bold"))


# ============================================================ 60 lignes de champ
w, h = 900, 330
s = head(w, h)

# --- a) charge ponctuelle positive
cx, cy = 175, 175
s += T(175, 40, "a) charge ponctuelle positive", 16, GREY)
import math
for k in range(12):
    a = math.radians(k * 30)
    x0, y0 = cx + 26 * math.cos(a), cy + 26 * math.sin(a)
    x1, y1 = cx + 100 * math.cos(a), cy + 100 * math.sin(a)
    s += (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
          f'stroke="{BLUE}" stroke-width="2" marker-end="url(#arB)"/>')
s += f'<circle cx="{cx}" cy="{cy}" r="19" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2.6"/>'
s += T(cx, cy + 7, "+", 22, NAVY, weight="bold")
s += T(175, 310, "les lignes s'écartent : le champ faiblit", 14, GREY)

# --- b) champ uniforme entre deux armatures
X0, X1, YT, YB = 420, 700, 90, 250
s += T(560, 40, "b) champ uniforme d'un condensateur plan", 16, GREY)
s += f'<rect x="{X0}" y="{YT-9}" width="{X1-X0}" height="9" fill="{NAVY}"/>'
s += f'<rect x="{X0}" y="{YB}" width="{X1-X0}" height="9" fill="{NAVY}"/>'
s += W([(X0 + 30, YT - 9), (X0 + 30, YT - 40)]) + W([(X0 + 30, YT - 40), (X0 - 40, YT - 40)])
s += W([(X0 + 30, YB + 9), (X0 + 30, YB + 40)]) + W([(X0 + 30, YB + 40), (X0 - 40, YB + 40)])
s += T(X0 - 48, YT - 34, "+", 20, NAVY, anchor="end", weight="bold")
s += T(X0 - 48, YB + 46, "−", 20, NAVY, anchor="end", weight="bold")
for k in range(7):
    x = X0 + 22 + k * 39
    s += (f'<line x1="{x}" y1="{YT+4}" x2="{x}" y2="{YB-4}" stroke="{BLUE}" '
          f'stroke-width="2" marker-end="url(#arB)"/>')
s += (f'<line x1="{X1+34}" y1="{YT}" x2="{X1+34}" y2="{YB+9}" stroke="{GREY}" '
      f'stroke-width="1.6"/>')
s += (f'<line x1="{X1+28}" y1="{YT}" x2="{X1+40}" y2="{YT}" stroke="{GREY}" stroke-width="1.6"/>'
      f'<line x1="{X1+28}" y1="{YB+9}" x2="{X1+40}" y2="{YB+9}" stroke="{GREY}" stroke-width="1.6"/>')
s += T(X1 + 48, (YT + YB) / 2 + 6, "d", 17, GREY, anchor="start", style="italic")
# charge d'essai et force
s += f'<circle cx="{X0+180}" cy="{(YT+YB)/2}" r="13" fill="#FFFFFF" stroke="{RED}" stroke-width="2.4"/>'
s += T(X0 + 180, (YT + YB) / 2 + 6, "+", 17, RED, weight="bold")
s += (f'<line x1="{X0+180}" y1="{(YT+YB)/2+16}" x2="{X0+180}" y2="{(YT+YB)/2+52}" '
      f'stroke="{RED}" stroke-width="2.6" marker-end="url(#arR)"/>')
s += T(X0 + 192, (YT + YB) / 2 + 46, "F = Q · E", 15, RED, anchor="start", weight="bold")
s += T(560, 310, "lignes parallèles et régulières : le champ est le même partout", 14, GREY)
save("60_lignes_champ", s + TAIL)

# ============================================================ 61 symboles CEI
w, h = 900, 200
s = head(w, h)
s += T(150, 40, "condensateur", 16, GREY)
s += capw_h(70, 230, 110, None, None)
s += T(150, 160, "non polarisé", 14, GREY)

s += T(450, 40, "condensateur polarisé", 16, GREY)
s += W([(370, 110), (444, 110)]) + W([(456, 110), (530, 110)])
s += (f'<line x1="{444}" y1="{110-17}" x2="{444}" y2="{110+17}" stroke="{NAVY}" '
      f'stroke-width="3.4"/>')
s += (f'<path d="M456,93 A 22 17 0 0 1 456,127" stroke="{NAVY}" stroke-width="3.4" '
      f'fill="none"/>')
s += T(432, 82, "+", 18, NAVY, weight="bold")
s += T(450, 160, "électrolytique — sens imposé", 14, GREY)

s += T(750, 40, "condensateur variable", 16, GREY)
s += capw_h(670, 830, 110, None, None)
s += (f'<line x1="{718}" y1="{136}" x2="{782}" y2="{84}" stroke="{NAVY}" stroke-width="2.4" '
      f'marker-end="url(#ar)"/>')
s += T(750, 160, "ajustable", 14, GREY)
save("61_symboles_condo", s + TAIL)

# ============================================================ 62 condensateur plan
w, h = 860, 300
s = head(w, h)
X0, X1, YT, YB = 250, 560, 90, 220
s += f'<rect x="{X0}" y="{YT-10}" width="{X1-X0}" height="10" fill="{NAVY}"/>'
s += f'<rect x="{X0}" y="{YB}" width="{X1-X0}" height="10" fill="{NAVY}"/>'
s += f'<rect x="{X0}" y="{YT}" width="{X1-X0}" height="{YB-YT}" fill="{LBLUE}" opacity="0.55"/>'
for k in range(8):
    x = X0 + 20 + k * 39
    s += (f'<line x1="{x}" y1="{YT+4}" x2="{x}" y2="{YB-4}" stroke="{BLUE}" '
          f'stroke-width="1.8" marker-end="url(#arB)"/>')
s += T((X0 + X1) / 2, YT - 24, "surface en regard  A", 16, NAVY)
s += T((X0 + X1) / 2, (YT + YB) / 2 + 6, "isolant  ε_{r}", 16, NAVY)
s += (f'<line x1="{X1+34}" y1="{YT}" x2="{X1+34}" y2="{YB+10}" stroke="{GREY}" '
      f'stroke-width="1.6"/>'
      f'<line x1="{X1+28}" y1="{YT}" x2="{X1+40}" y2="{YT}" stroke="{GREY}" stroke-width="1.6"/>'
      f'<line x1="{X1+28}" y1="{YB+10}" x2="{X1+40}" y2="{YB+10}" stroke="{GREY}" stroke-width="1.6"/>')
s += T(X1 + 48, (YT + YB) / 2 + 6, "d", 18, GREY, anchor="start", style="italic")
s += W([(X0 + 40, YT - 10), (X0 + 40, YT - 46)]) + W([(X0 + 40, YT - 46), (X0 - 60, YT - 46)])
s += W([(X0 + 40, YB + 10), (X0 + 40, YB + 46)]) + W([(X0 + 40, YB + 46), (X0 - 60, YB + 46)])
s += T(X0 - 70, YT - 40, "+", 20, NAVY, anchor="end", weight="bold")
s += T(X0 - 70, YB + 52, "−", 20, NAVY, anchor="end", weight="bold")
s += T(430, 285, "plus la surface est grande et l'isolant mince, plus C est grand", 15, GREY)
save("62_condo_plan", s + TAIL)

# ============================================================ 63 groupements
w, h = 900, 300
s = head(w, h)
# --- parallèle
s += T(215, 40, "en parallèle", 17, NAVY, weight="bold")
XA, XB, YM = 70, 360, 150
s += T(XA - 14, YM + 6, "A", 16, NAVY, anchor="end")
s += T(XB + 14, YM + 6, "B", 16, NAVY, anchor="start")
s += W([(XA, YM), (120, YM)]) + W([(XB, YM), (310, YM)])
s += W([(120, 90), (310, 90)]) + W([(120, 210), (310, 210)])
s += W([(120, 90), (120, 210)]) + W([(310, 90), (310, 210)])
s += capw_h(150, 280, 90, "C_1", "20 µF", dy=-24)
s += capw_h(150, 280, 210, "C_2", "30 µF", dy=-24)
s += node(120, YM) + node(310, YM)
s += T(163, 268, "C_{AB}", 18, RED, anchor="start", weight="bold")
s += T(206, 268, "= 50 µF", 18, RED, anchor="start", weight="bold")
# --- série
s += T(680, 40, "en série", 17, NAVY, weight="bold")
XA, XB, YM = 540, 830, 150
s += T(XA - 14, YM + 6, "A", 16, NAVY, anchor="end")
s += T(XB + 14, YM + 6, "B", 16, NAVY, anchor="start")
s += capw_h(XA, 685, YM, "C_1", "20 µF", dy=-24)
s += capw_h(685, XB, YM, "C_2", "30 µF", dy=-24)
s += T(628, 268, "C_{AB}", 18, RED, anchor="start", weight="bold")
s += T(671, 268, "= 12 µF", 18, RED, anchor="start", weight="bold")
save("63_groupements", s + TAIL)

# ============================================================ 64 réseau du cours
def reseau(x0, y0, etat, sz=16):
    """C4 en série avec [ C3 // (C1 série C2) ]. etat = 'complet' | 'g1' | 'g2' | 'fin'."""
    XA, XB = x0, x0 + 470
    YM = y0 + 90
    g = T(XA - 14, YM + 6, "A", sz, NAVY, anchor="end")
    g += T(XB + 14, YM + 6, "B", sz, NAVY, anchor="start")
    if etat == "fin":
        g += capw_h(XA, XB, YM, "C_{AB}", "10 µF", col=RED, dy=-26, sz=sz)
        return g
    n1, n2 = x0 + 190, XB
    g += capw_h(XA, n1, YM, "C_4", "20 µF", dy=-26, sz=sz)
    if etat == "complet":
        g += W([(n1, YM), (n1, y0 + 20)]) + W([(n1, y0 + 20), (n1 + 40, y0 + 20)])
        g += W([(n2, YM), (n2, y0 + 20)]) + W([(n2 - 40, y0 + 20), (n2, y0 + 20)])
        g += capw_h(n1 + 40, n2 - 40, y0 + 20, "C_3", "8 µF", dy=-24, sz=sz)
        g += W([(n1, YM), (n1, y0 + 160)]) + W([(n1, y0 + 160), (n1 + 30, y0 + 160)])
        g += W([(n2, YM), (n2, y0 + 160)]) + W([(n2 - 30, y0 + 160), (n2, y0 + 160)])
        mid = (n1 + n2) / 2
        g += capw_h(n1 + 30, mid, y0 + 160, "C_1", "20 µF", dy=-24, sz=sz)
        g += capw_h(mid, n2 - 30, y0 + 160, "C_2", "30 µF", dy=-24, sz=sz)
    elif etat == "g1":
        g += W([(n1, YM), (n1, y0 + 20)]) + W([(n1, y0 + 20), (n1 + 40, y0 + 20)])
        g += W([(n2, YM), (n2, y0 + 20)]) + W([(n2 - 40, y0 + 20), (n2, y0 + 20)])
        g += capw_h(n1 + 40, n2 - 40, y0 + 20, "C_3", "8 µF", dy=-24, sz=sz)
        g += W([(n1, YM), (n1, y0 + 160)]) + W([(n1, y0 + 160), (n1 + 30, y0 + 160)])
        g += W([(n2, YM), (n2, y0 + 160)]) + W([(n2 - 30, y0 + 160), (n2, y0 + 160)])
        g += capw_h(n1 + 30, n2 - 30, y0 + 160, "C_{12}", "12 µF", col=RED, dy=-24, sz=sz)
    else:  # g2
        g += W([(n1, YM), (n1, y0 + 90)]) + W([(n2, YM), (n2, y0 + 90)])
        g += capw_h(n1, n2, YM, "C_{123}", "20 µF", col=RED, dy=-26, sz=sz)
    g += node(n1, YM)
    return g


w, h = 620, 300
s = head(w, h) + reseau(75, 50, "complet")
save("64_reseau", s + TAIL)

w, h = 1900, 320
s = head(w, h)
s += T(70, 34, "① C_1 et C_2 en série", 26, GREY, anchor="start")
s += reseau(75, 60, "g1", sz=26)
s += (f'<line x1="{592}" y1="150" x2="{640}" y2="150" stroke="{RED}" stroke-width="4" '
      f'marker-end="url(#arR)"/>')
s += T(700, 34, "② le groupe en parallèle avec C_3", 26, GREY, anchor="start")
s += reseau(705, 60, "g2", sz=26)
s += (f'<line x1="{1222}" y1="150" x2="{1270}" y2="150" stroke="{RED}" stroke-width="4" '
      f'marker-end="url(#arR)"/>')
s += T(1330, 34, "③ le tout en série avec C_4", 26, GREY, anchor="start")
s += reseau(1335, 60, "fin", sz=26)
save("64b_reduction", s + TAIL, scale=1.8)

# ============================================================ 65 circuit de charge
w, h = 640, 330
s = head(w, h)
XL, XR, YT, YB = 90, 520, 80, 270
s += source(XL, YT, YB, "U")
s += W([(XL, YT), (XL + 60, YT)])
s += switch_open(XL + 60, YT, nom="S")
s += W([(XL + 114, YT), (XL + 160, YT)])
s += res_h(XL + 200, YT, 70, 28)
s += W([(XL + 235, YT), (XR, YT)])
s += T(XL + 200, YT - 24, "R", 17, NAVY, style="italic", weight="bold")
s += W([(XR, YT), (XR, YT + 62)]) + W([(XR, YT + 78), (XR, YB)]) + W([(XL, YB), (XR, YB)])
s += cap_v(XR, YT + 70)
s += T(XR + 24, YT + 60, "C", 17, NAVY, anchor="start", style="italic", weight="bold")
s += ih(XL + 300, YT, "i_C", above=True)
s += (f'<line x1="{XR+62}" y1="{YT+20}" x2="{XR+62}" y2="{YB-20}" stroke="{BLUE}" '
      f'stroke-width="2.2" marker-end="url(#arB)"/>')
s += T(XR + 72, (YT + YB) / 2, "u_C", 17, BLUE, anchor="start", weight="bold")
s += T(320, 315, "à la fermeture de S : le condensateur se charge à travers R", 15, GREY)
save("65_circuit_charge", s + TAIL)

# ============================================================ 66 circuit à l'ouverture
w, h = 700, 340
s = head(w, h)
XL, XM, XR, YT, YB = 90, 350, 560, 80, 280
s += source(XL, YT, YB, "E")
s += W([(XL, YT), (XL + 110, YT)])
s += res_h(XL + 150, YT, 74, 28)
s += T(XL + 150, YT - 24, "R_1", 17, NAVY, style="italic", weight="bold")
s += W([(XL + 187, YT), (XL + 210, YT)])
s += switch_open(XL + 210, YT, nom="S")
s += W([(XL + 264, YT), (XR, YT)])
s += W([(XL, YB), (XR, YB)])
# R2 vertical au milieu
s += W([(XM, YT), (XM, YT + 56)]) + W([(XM, YT + 124), (XM, YB)])
s += res_v(XM, YT + 90, 28, 68)
s += T(XM - 24, YT + 96, "R_2", 17, NAVY, anchor="end", style="italic", weight="bold")
s += node(XM, YT)
# C à droite
s += W([(XR, YT), (XR, YT + 82)]) + W([(XR, YT + 98), (XR, YB)])
s += cap_v(XR, YT + 90)
s += T(XR + 24, YT + 80, "C", 17, NAVY, anchor="start", style="italic", weight="bold")
s += iv(XR, YT + 40, "i_C", dir=1, left=True)
s += (f'<line x1="{XM+58}" y1="{YT+30}" x2="{XM+58}" y2="{YB-30}" stroke="{BLUE}" '
      f'stroke-width="2.2" marker-end="url(#arB)"/>')
s += T(XM + 68, (YT + YB) / 2, "u_C", 17, BLUE, anchor="start", weight="bold")
s += T(350, 322, "S fermé depuis longtemps, puis ouvert : C se décharge dans R₂ seul", 15, GREY)
save("66_circuit_ouverture", s + TAIL)

# ============================================================ 67 circuit de l'exercice 7
w, h = 700, 340
s = head(w, h)
s2 = s
XL, XM, XR, YT, YB = 90, 350, 560, 80, 280
s += source(XL, YT, YB, "E = 18 V")
s += W([(XL, YT), (XL + 110, YT)])
s += res_h(XL + 150, YT, 74, 28)
s += lab(XL + 150, YT - 44, "R_1", "20 Ω", 16)
s += W([(XL + 187, YT), (XL + 210, YT)])
s += switch_open(XL + 210, YT, nom="S")
s += W([(XL + 264, YT), (XR, YT)])
s += W([(XL, YB), (XR, YB)])
s += W([(XM, YT), (XM, YT + 56)]) + W([(XM, YT + 124), (XM, YB)])
s += res_v(XM, YT + 90, 28, 68)
s += T(XM - 24, YT + 88, "R_2", 16, NAVY, anchor="end", style="italic", weight="bold")
s += T(XM - 24, YT + 108, "40 Ω", 14, NAVY, anchor="end")
s += node(XM, YT)
s += W([(XR, YT), (XR, YT + 82)]) + W([(XR, YT + 98), (XR, YB)])
s += cap_v(XR, YT + 90)
s += T(XR + 24, YT + 80, "C", 16, NAVY, anchor="start", style="italic", weight="bold")
s += T(XR + 24, YT + 100, "2,5 µF", 14, NAVY, anchor="start")
s += iv(XR, YT + 40, "i_C", dir=1, left=True)
s += (f'<line x1="{XM+58}" y1="{YT+30}" x2="{XM+58}" y2="{YB-30}" stroke="{BLUE}" '
      f'stroke-width="2.2" marker-end="url(#arB)"/>')
s += T(XM + 68, (YT + YB) / 2, "u_C", 17, BLUE, anchor="start", weight="bold")
save("67_ex7_circuit", s + TAIL)

# ============================================================ 68 circuit exercice 5
w, h = 560, 300
s = head(w, h)
XL, XR, YT, YB = 90, 440, 80, 250
s += source(XL, YT, YB, "U = 10 V")
s += W([(XL, YT), (XL + 40, YT)])
s += switch_open(XL + 40, YT, nom="S")
s += W([(XL + 94, YT), (XL + 140, YT)])
s += res_h(XL + 180, YT, 74, 28)
s += lab(XL + 180, YT - 44, "R", "1 kΩ", 16)
s += W([(XL + 217, YT), (XR, YT)])
s += W([(XR, YT), (XR, YT + 62)]) + W([(XR, YT + 78), (XR, YB)]) + W([(XL, YB), (XR, YB)])
s += cap_v(XR, YT + 70)
s += T(XR + 22, YT + 60, "C_x", 16, NAVY, anchor="start", style="italic", weight="bold")
s += T(XR + 22, YT + 80, "?", 16, RED, anchor="start", weight="bold")
s += ih(XL + 280, YT, "i_C", above=True)
save("68_ex5_circuit", s + TAIL)

# ============================================================ 69 réseau exercice 4
w, h = 800, 430
s = head(w, h)
XA, XB, YM = 80, 720, 190
n1, n2 = 250, 560
s += T(XA - 14, YM + 6, "A", 16, NAVY, anchor="end")
s += T(XB + 14, YM + 6, "B", 16, NAVY, anchor="start")
s += capw_h(XA + 40, n1, YM, "C_1", "15 µF", dy=-26)
s += W([(XA, YM), (XA + 40, YM)])
s += W([(n1, YM), (n1, 70)]) + W([(n1, 70), (n1 + 40, 70)])
s += W([(n2, YM), (n2, 70)]) + W([(n2 - 40, 70), (n2, 70)])
s += capw_h(n1 + 40, n2 - 40, 70, "C_4", "8 µF", dy=-24)
s += W([(n1, YM), (n1, 300)]) + W([(n1, 300), (n1 + 30, 300)])
s += W([(n2, YM), (n2, 300)]) + W([(n2 - 30, 300), (n2, 300)])
mid = (n1 + n2) / 2
s += capw_h(n1 + 30, mid, 300, "C_2", "6 µF", dy=-24)
s += capw_h(mid, n2 - 30, 300, "C_3", "3 µF", dy=-24)
s += W([(n2, YM), (XB - 40, YM)])
s += node(n1, YM) + node(n2, YM)
# C5 en parallele sur l'ensemble A-B
s += W([(XA + 40, YM), (XA + 40, 385)]) + W([(XA + 40, 385), (XA + 130, 385)])
s += W([(XB - 40, YM), (XB - 40, 385)]) + W([(XB - 130, 385), (XB - 40, 385)])
s += capw_h(XA + 130, XB - 130, 385, "C_5", None, dy=-24)
s += T(mid + 30, 366, "4 µF", 14, NAVY, anchor="start")
s += W([(XB - 40, YM), (XB, YM)])
s += node(XA + 40, YM) + node(XB - 40, YM)
save("69_ex4_reseau", s + TAIL)

print("schémas 300 : ok")
