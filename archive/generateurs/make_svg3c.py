# -*- coding: utf-8 -*-
"""Chapitre 140 — bandes de réduction pas à pas pour le corrigé."""
from figures import *
from make_svg3 import node, source

SMALL = 13


def loop(x, y, w_, h_, src=True):
    """Cadre d'un mini-circuit : rail haut, rail bas, source à gauche."""
    s = W([(x, y), (x + w_, y)], NAVY, 2.2) + W([(x, y + h_), (x + w_, y + h_)], NAVY, 2.2)
    if src:
        cy = y + h_ // 2
        s += W([(x, y), (x, cy - 17)], NAVY, 2.2) + W([(x, cy + 17), (x, y + h_)], NAVY, 2.2)
        s += src_v(x, cy, 17)
    else:
        s += W([(x, y), (x, y + h_)], NAVY, 2.2)
    return s


def rh(x, y, nom, col=NAVY):
    """Résistance sur le rail haut."""
    return (res_h(x, y, 46, 20, col)
            + T(x, y - 12, nom, SMALL, col, style="italic", weight="bold"))


def rv(x, y, h_, nom, col=NAVY, side="right"):
    """Résistance verticale entre les deux rails, aux ordonnées y..y+h_."""
    cy = y + h_ // 2
    s = W([(x, y), (x, cy - 22)], NAVY, 2.2) + W([(x, cy + 22), (x, y + h_)], NAVY, 2.2)
    s += res_v(x, cy, 20, 44, col)
    tx = x + 17 if side == "right" else x - 17
    s += T(tx, cy + 5, nom, SMALL, col, style="italic", weight="bold",
           anchor="start" if side == "right" else "end")
    return s


def fleche(x, y):
    return (f'<line x1="{x}" y1="{y}" x2="{x + 46}" y2="{y}" stroke="{RED}" '
            f'stroke-width="3" marker-end="url(#arR)"/>')


def etape(x, y, num, txt):
    return (T(x, y, num, 14, GREY, weight="bold", anchor="start")
            + T(x + 22, y, txt, 14, GREY, anchor="start"))


def valeur(x, y, txt):
    return T(x, y, txt, 14, RED, weight="bold")


# ============================================================ N°3 : R1 + (R2 // R3)
w, h = 880, 210
s = head(w, h)
Y, H = 60, 110
s += etape(20, 34, "①", "le circuit")
s += loop(50, Y, 210, H) + rh(120, Y, "R1") + rv(200, Y, H, "R2", side="left") \
    + rv(258, Y, H, "R3")
s += valeur(150, 196, "R2 // R3 = 0,1 · 10³ Ω")
s += fleche(300, Y + H / 2)
s += etape(370, 34, "②", "le groupe remplacé")
s += loop(400, Y, 180, H) + rh(470, Y, "R1") + rv(578, Y, H, "R23")
s += valeur(490, 196, "R1 + R23 = 0,2 · 10³ Ω")
s += fleche(620, Y + H / 2)
s += etape(690, 34, "③", "une seule résistance")
s += loop(720, Y, 120, H) + rv(838, Y, H, "Rtot")
s += valeur(780, 196, "Rtot = 200 Ω")
save("55_red_n3", s + TAIL)

# ============================================================ N°4 : (R1 + R2) // R3
w, h = 880, 210
s = head(w, h)
s += etape(20, 34, "①", "le circuit")
s += loop(50, Y, 210, H)
cy = Y + H // 2
s += W([(200, Y), (200, Y + 16)], NAVY, 2.2) + res_v(200, Y + 36, 20, 40) \
    + W([(200, Y + 56), (200, Y + 62)], NAVY, 2.2)
s += res_v(200, Y + 82, 20, 40) + W([(200, Y + 102), (200, Y + H)], NAVY, 2.2)
s += T(183, Y + 42, "R1", SMALL, NAVY, style="italic", weight="bold", anchor="end")
s += T(183, Y + 88, "R2", SMALL, NAVY, style="italic", weight="bold", anchor="end")
s += rv(258, Y, H, "R3")
s += valeur(150, 196, "R1 + R2 = 0,6 · 10³ Ω")
s += fleche(300, cy)
s += etape(370, 34, "②", "la branche remplacée")
s += loop(400, Y, 180, H) + rv(520, Y, H, "R12", side="left") + rv(578, Y, H, "R3")
s += valeur(490, 196, "R12 // R3 = 0,2 · 10³ Ω")
s += fleche(620, cy)
s += etape(690, 34, "③", "une seule résistance")
s += loop(720, Y, 120, H) + rv(838, Y, H, "Rtot")
s += valeur(780, 196, "Rtot = 200 Ω")
save("56_red_n4", s + TAIL)

# ============================================================ N°5 : cinq résistances
w, h = 980, 240
s = head(w, h)
Y, H = 66, 112


def panneau5(x0, groupe):
    """R1 et R5 sur le rail haut, le groupe parallèle au milieu."""
    g = loop(x0, Y, 250, H) + rh(x0 + 55, Y, "R1") + rh(x0 + 220, Y, "R5")
    g += W([(x0 + 250, Y), (x0 + 250, Y + H)], NAVY, 2.2)
    g += rv(x0 + 120, Y, H, "R2", side="left")
    if groupe == "branche":
        xb = x0 + 170
        g += W([(xb, Y), (xb, Y + 20)], NAVY, 2.2) + res_v(xb, Y + 40, 20, 40)
        g += W([(xb, Y + 60), (xb, Y + 66)], NAVY, 2.2) + res_v(xb, Y + 86, 20, 40)
        g += W([(xb, Y + 106), (xb, Y + H)], NAVY, 2.2)
        g += T(xb + 17, Y + 46, "R3", SMALL, NAVY, style="italic", weight="bold",
               anchor="start")
        g += T(xb + 17, Y + 92, "R4", SMALL, NAVY, style="italic", weight="bold",
               anchor="start")
    else:
        g += rv(x0 + 170, Y, H, groupe)
    return g


s += etape(16, 36, "①", "R3 + R4 en série")
s += panneau5(25, "branche")
s += valeur(150, 224, "R3 + R4 = 0,2 · 10³ Ω")
s += fleche(292, Y + H / 2)
s += etape(342, 36, "②", "R2 // R34")
s += panneau5(350, "R34")
s += valeur(475, 224, "R2 // R34 = 0,1 · 10³ Ω")
s += fleche(617, Y + H / 2)
s += etape(667, 36, "③", "tout en série")
s += loop(675, Y, 250, H) + rh(730, Y, "R1") + rh(815, Y, "R234") + rh(895, Y, "R5")
s += W([(925, Y), (925, Y + H)], NAVY, 2.2)
s += valeur(800, 224, "Rtot = R1 + R234 + R5 = 0,2 · 10³ Ω")
save("57_red_n5", s + TAIL)

print("bandes de réduction : ok")
