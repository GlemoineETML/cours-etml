# -*- coding: utf-8 -*-
"""Chapitre 500 — appareils de mesure et leur influence. Schémas CEI.

Conventions de la série :
  · COURANT  = pointe de flèche POSÉE SUR LE CONDUCTEUR, repère indicé à côté.
  · TENSION  = flèche tracée À CÔTÉ du composant, du + vers le −, repère indicé.
"""
from figures import *
from make_svg3 import node, lab, ih, iv, uh, source
from make_svg4 import switch_open

SMALL = 14


def app(cx, cy, lettre, r=22, col=NAVY):
    """Appareil de mesure CEI : cercle + lettre (V, A, Ω)."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{col}" '
            f'stroke-width="2.6"/>' + T(cx, cy + 7, lettre, 20, col, weight="bold"))


def cadre_pointille(x, y, w_, h_, col=GREY):
    return (f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="none" '
            f'stroke="{col}" stroke-width="1.8" stroke-dasharray="7 5" rx="6"/>')


def rv(x, y0, y1, nom, val=None, col=NAVY):
    """Résistance verticale câblée de y0 à y1, repère à droite."""
    cy = (y0 + y1) / 2
    s = W([(x, y0), (x, cy - 32)], col, 2.6) + W([(x, cy + 32), (x, y1)], col, 2.6)
    s += res_v(x, cy, 28, 64, col)
    s += T(x + 26, cy - 2, nom, 16, col, anchor="start", style="italic", weight="bold")
    if val:
        s += T(x + 26, cy + 18, val, 14, col, anchor="start")
    return s


# ============================================================ 90 passerelle 140
w, h = 900, 340
s = head(w, h)
XL, XR, YT, YB = 90, 700, 90, 280
s += source(XL, YT, YB, "U")
s += W([(XL, YT), (XL + 120, YT)])
s += res_h(XL + 160, YT, 74, 28)
s += T(XL + 160, YT - 26, "R_1", 16, NAVY, style="italic", weight="bold")
s += W([(XL + 197, YT), (XL + 260, YT)])
s += app(XL + 284, YT, "A")
s += W([(XL + 308, YT), (XR, YT)])
s += W([(XL, YB), (XR, YB)])
s += rv(XR, YT, YB, "R_2")
s += ih(XL + 235, YT, "I_1", above=True)
# voltmètre en parallèle sur R2
s += W([(XR, YT), (XR + 110, YT)]) + W([(XR, YB), (XR + 110, YB)])
s += W([(XR + 110, YT), (XR + 110, YT + 63)]) + W([(XR + 110, YT + 107), (XR + 110, YB)])
s += app(XR + 110, YT + 85, "V")
s += node(XR, YT) + node(XR, YB)
s += T(450, 322, "Le montage du TP : ampèremètre en série, voltmètre en parallèle",
       15, GREY)
s += T(450, 46, "et si les appareils eux-mêmes modifiaient le circuit ?", 16, RED,
       weight="bold")
save("90_passerelle", s + TAIL)

# ============================================================ 91 voltmètre réel
w, h = 900, 310
s = head(w, h)
YH, YL = 112, 232                 # rails haut et bas, symétriques autour de 172
CYV = (YH + YL) / 2

# a) idéal — le symbole est centré dans son cadre, lui-même centré sur la maille
s += T(250, 40, "voltmètre idéal", 17, NAVY, weight="bold")
s += W([(90, YH), (410, YH)]) + W([(90, YL), (410, YL)])
s += W([(250, YH), (250, CYV - 22)]) + W([(250, CYV + 22), (250, YL)])
s += app(250, CYV, "V")
s += cadre_pointille(250 - 90, YH - 24, 180, (YL + 24) - (YH - 24))
s += T(250, 284, "résistance interne infinie : il ne prend aucun courant",
       15, GREY)

# b) réel — le symbole et R_V forment une paire centrée dans le cadre
s += T(660, 40, "voltmètre réel", 17, NAVY, weight="bold")
s += W([(500, YH), (820, YH)]) + W([(500, YL), (820, YL)])
s += W([(605, YH), (605, CYV - 22)]) + W([(605, CYV + 22), (605, YL)])
s += app(605, CYV, "V")
s += W([(715, YH), (715, CYV - 26)]) + W([(715, CYV + 26), (715, YL)])
s += res_v(715, CYV, 28, 52, RED)
s += T(741, CYV + 4, "R_V", 16, RED, anchor="start", style="italic",
       weight="bold")
s += node(605, YH) + node(605, YL) + node(715, YH) + node(715, YL)
s += cadre_pointille(660 - 140, YH - 24, 280, (YL + 24) - (YH - 24))
s += T(660, 284, "résistance interne finie : il prend un peu de courant au "
                 "circuit", 14, RED)
save("91_voltmetre", s + TAIL)

# ============================================================ 92 effet de charge
w, h = 1450, 380
s = head(w, h)


def diviseur(x0, y0, mesure, equiv=False):
    """Diviseur R1 / R2 ; mesure = None | 'V' | 'equiv'."""
    XL, XR, YT, YB = x0, x0 + 270, y0, y0 + 210
    g = source(XL, YT, YB, None, arrow=False)
    g += W([(XL, YT), (XR, YT)]) + W([(XL, YB), (XR, YB)])
    g += res_v(XR, YT + 52, 28, 64)
    g += W([(XR, YT), (XR, YT + 20)]) + W([(XR, YT + 84), (XR, YT + 105)])
    g += T(XR + 26, YT + 50, "R_1", 16, NAVY, anchor="start", style="italic",
           weight="bold")
    if equiv:
        g += res_v(XR, YT + 158, 28, 64, RED)
        g += W([(XR, YT + 105), (XR, YT + 126)]) + W([(XR, YT + 190), (XR, YB)])
        g += T(XR + 26, YT + 156, "R_2 // R_V", 16, RED, anchor="start",
               style="italic", weight="bold")
    else:
        g += res_v(XR, YT + 158, 28, 64)
        g += W([(XR, YT + 105), (XR, YT + 126)]) + W([(XR, YT + 190), (XR, YB)])
        g += T(XR + 26, YT + 156, "R_2", 16, NAVY, anchor="start", style="italic",
               weight="bold")
    if mesure == "V":
        g += W([(XR, YT + 105), (XR + 120, YT + 105)]) + W([(XR, YB), (XR + 120, YB)])
        g += W([(XR + 120, YT + 105), (XR + 120, YT + 133)])
        g += W([(XR + 120, YT + 177), (XR + 120, YB)])
        g += app(XR + 120, YT + 155, "V")
        g += node(XR, YT + 105) + node(XR, YB)
    return g


s += T(150, 40, "① le circuit calculé", 16, GREY)
s += diviseur(70, 80, None)
s += T(150, 350, "tension calculée : 5,00 V", 17, NAVY, weight="bold")

s += (f'<line x1="{390}" y1="180" x2="{440}" y2="180" stroke="{RED}" stroke-width="4" '
      f'marker-end="url(#arR)"/>')
s += T(620, 40, "② on branche le voltmètre", 16, GREY)
s += diviseur(490, 80, "V")
s += T(620, 350, "il consomme du courant", 17, RED, weight="bold")

s += (f'<line x1="{920}" y1="180" x2="{968}" y2="180" stroke="{RED}" stroke-width="4" '
      f'marker-end="url(#arR)"/>')
s += T(1130, 40, "③ le circuit réellement mesuré", 16, GREY)
s += diviseur(1000, 80, None, equiv=True)
s += T(1130, 350, "tension mesurée : moins de 5,00 V", 16, RED, weight="bold")
save("92_effet_charge", s + TAIL, scale=1.9)

# ============================================================ 93 ampèremètre réel
w, h = 900, 300
s = head(w, h)
s += T(230, 40, "ampèremètre idéal", 17, NAVY, weight="bold")
s += W([(90, 150), (208, 150)]) + W([(252, 150), (370, 150)])
s += app(230, 150, "A")
s += T(230, 240, "résistance interne nulle : aucune chute de tension", 15, GREY)
s += cadre_pointille(160, 106, 140, 88)

s += T(660, 40, "ampèremètre réel", 17, NAVY, weight="bold")
s += W([(520, 150), (578, 150)]) + W([(622, 150), (700, 150)])
s += app(600, 150, "A")
s += res_h(760, 150, 64, 28, RED)
s += W([(792, 150), (830, 150)])
s += T(760, 124, "R_A", 16, RED, style="italic", weight="bold")
s += (f'<line x1="{578}" y1="{214}" x2="{792}" y2="{214}" stroke="{BLUE}" '
      f'stroke-width="2.2" marker-end="url(#arB)"/>')
s += T(685, 236, "U_A", 16, BLUE, weight="bold")
s += ih(540, 150, "I", above=True)
s += T(660, 272, "résistance interne faible mais pas nulle : elle vole un peu de tension", 14, RED)
s += cadre_pointille(560, 106, 250, 88)
save("93_amperemetre", s + TAIL)

# ============================================================ 94 ohmmètre
w, h = 940, 330
s = head(w, h)
YT, YB, CYO = 104, 226, 165       # rails de raccordement et axe de l'appareil


def ohmmetre(xo, xr):
    """Ohmmètre relié par ses deux pointes de touche au composant en xr."""
    g = app(xo, CYO, "Ω")
    g += W([(xo, CYO - 22), (xo, YT)]) + W([(xo, YT), (xr, YT)])
    g += W([(xo, CYO + 22), (xo, YB)]) + W([(xo, YB), (xr, YB)])
    g += T(xo, YB + 30, "pointes de touche", 13, GREY)
    return g


s += T(230, 40, "a) résistance isolée", 16, GREY)
s += ohmmetre(150, 300)
s += W([(300, YT), (300, CYO - 26)]) + W([(300, CYO + 26), (300, YB)])
s += res_v(300, CYO, 28, 52)
s += T(326, CYO + 4, "R", 16, NAVY, anchor="start", style="italic", weight="bold")
s += T(230, 296, "on mesure R : correct", 15, NAVY)

s += T(700, 40, "b) résistance encore dans le circuit", 16, GREY)
s += ohmmetre(520, 800)
s += W([(660, YT), (660, CYO - 26)]) + W([(660, CYO + 26), (660, YB)])
s += res_v(660, CYO, 28, 52)
s += T(634, CYO + 4, "R", 16, NAVY, anchor="end", style="italic", weight="bold")
s += W([(800, YT), (800, CYO - 26)]) + W([(800, CYO + 26), (800, YB)])
s += res_v(800, CYO, 28, 52, RED)
s += T(826, CYO - 6, "reste du", 15, RED, anchor="start")
s += T(826, CYO + 12, "circuit", 15, RED, anchor="start")
s += node(660, YT) + node(660, YB)
s += T(700, 296, "on mesure R // reste : toujours plus petit", 15, RED)
save("94_ohmmetre", s + TAIL)

# ============================================================ 95 calibres
import math
w, h = 900, 370
s = head(w, h)
CX, CY, R0 = 450, 296, 230


def arc(r, a0, a1, col, wd):
    x0 = CX + r * math.cos(math.radians(180 - a0))
    y0 = CY - r * math.sin(math.radians(180 - a0))
    x1 = CX + r * math.cos(math.radians(180 - a1))
    y1 = CY - r * math.sin(math.radians(180 - a1))
    big = 1 if abs(a1 - a0) > 180 else 0
    return (f'<path d="M{x0:.1f},{y0:.1f} A {r} {r} 0 {big} 1 {x1:.1f},{y1:.1f}" '
            f'stroke="{col}" stroke-width="{wd}" fill="none"/>')


s += arc(R0, 0, 180, NAVY, 3)
s += arc(R0 - 16, 0, 60, RED, 14)
s += arc(R0 - 16, 60, 120, "#F0B429", 14)
s += arc(R0 - 16, 120, 180, "#26663F", 14)
for k in range(11):
    a = math.radians(180 - k * 18)
    x0, y0 = CX + (R0 - 30) * math.cos(a), CY - (R0 - 30) * math.sin(a)
    x1, y1 = CX + R0 * math.cos(a), CY - R0 * math.sin(a)
    s += W([(x0, y0), (x1, y1)], NAVY, 1.8)
# aiguille dans le dernier tiers
a = math.radians(180 - 150)
s += W([(CX, CY), (CX + (R0 - 44) * math.cos(a), CY - (R0 - 44) * math.sin(a))], NAVY, 4)
s += f'<circle cx="{CX}" cy="{CY}" r="8" fill="{NAVY}"/>'
s += T(CX - 150, CY + 30, "premier tiers", 14, RED)
s += T(CX - 150, CY + 48, "lecture imprécise", 13, RED)
s += T(CX + 155, CY + 30, "dernier tiers", 14, "#26663F")
s += T(CX + 155, CY + 48, "lecture précise", 13, "#26663F")
s += T(CX, 40, "Sur un appareil analogique, l'incertitude est un pourcentage",
       16, NAVY, weight="bold")
s += T(CX, 62, "de la PLEINE ÉCHELLE, pas de la lecture", 16, NAVY, weight="bold")
save("95_calibres", s + TAIL)

# ============================================================ 96 exercice 1
w, h = 860, 330
s = head(w, h)
XL, XR, YT, YB = 90, 620, 90, 270
s += source(XL, YT, YB, "U = 24 V")
s += W([(XL, YT), (XL + 150, YT)])
s += res_h(XL + 190, YT, 74, 28)
s += lab(XL + 190, YT - 44, "R_1", "330 Ω", 16)
s += W([(XL + 227, YT), (XR, YT)])
s += W([(XL, YB), (XR, YB)])
s += rv(XR, YT, YB, "R_2", "470 Ω")
s += node(XR, YT) + node(XR, YB)
s += T(430, 312, "Place un ampèremètre pour le courant total et un voltmètre pour "
                 "la tension de la deuxième résistance", 15, GREY)
save("96_ex1_placement", s + TAIL)

# ====================================================== 96c corrigé exercice 1
w, h = 900, 340
s = head(w, h)
XL, XR, YT, YB = 90, 640, 95, 285
s += source(XL, YT, YB, "U = 24 V")
s += W([(XL, YT), (XL + 100, YT)])
s += app(XL + 122, YT, "A")
s += W([(XL + 144, YT), (XL + 200, YT)])
s += res_h(XL + 240, YT, 74, 28)
s += lab(XL + 240, YT - 44, "R_1", "330 Ω", 16)
s += W([(XL + 277, YT), (XR, YT)])
s += W([(XL, YB), (XR, YB)])
s += rv(XR, YT, YB, "R_2", "470 Ω")
s += ih(XL + 180, YT, "I", above=True)
s += W([(XR, YT), (XR + 140, YT)]) + W([(XR, YB), (XR + 140, YB)])
s += W([(XR + 140, YT), (XR + 140, YT + 68)])
s += W([(XR + 140, YT + 112), (XR + 140, YB)])
s += app(XR + 140, YT + 90, "V")
s += node(XR, YT) + node(XR, YB)
# la tension mesurée, à droite du voltmètre
s += (f'<line x1="{XR+196}" y1="{YT+8}" x2="{XR+196}" y2="{YB-8}" stroke="{RED}" '
      f'stroke-width="2.4" marker-end="url(#arR)"/>')
s += T(XR + 208, YT + 88, "U_2", 17, RED, anchor="start", weight="bold")
s += T(XR + 208, YT + 108, "14,1 V", 15, RED, anchor="start")
s += T(430, 326, "A en série sur le fil, V en parallèle aux bornes de la deuxième "
                 "résistance", 15, RED)
save("96c_ex1_corrige", s + TAIL)

# ============================================================ 97 exercice 3
w, h = 820, 360
s = head(w, h)
XL, XR, YT, YB = 90, 400, 80, 290
s += source(XL, YT, YB, "U = 18 V")
s += W([(XL, YT), (XR, YT)]) + W([(XL, YB), (XR, YB)])
s += res_v(XR, YT + 55, 28, 64)
s += W([(XR, YT), (XR, YT + 23)]) + W([(XR, YT + 87), (XR, YT + 110)])
s += lab(XR - 60, YT + 50, "R_1", "2 MΩ", 16, anchor="end")
s += res_v(XR, YT + 165, 28, 64)
s += W([(XR, YT + 110), (XR, YT + 133)]) + W([(XR, YT + 197), (XR, YB)])
s += lab(XR - 60, YT + 160, "R_2", "2,5 MΩ", 16, anchor="end")
s += W([(XR, YT + 110), (XR + 180, YT + 110)]) + W([(XR, YB), (XR + 180, YB)])
s += W([(XR + 180, YT + 110), (XR + 180, YT + 143)])
s += W([(XR + 180, YT + 187), (XR + 180, YB)])
s += app(XR + 180, YT + 165, "V")
s += node(XR, YT + 110) + node(XR, YB)
s += T(XR + 208, YT + 158, "voltmètre numérique", 14, RED, anchor="start")
s += T(XR + 208, YT + 178, "10 MΩ", 15, RED, anchor="start", weight="bold")
s += T(410, 342, "Quelle tension le voltmètre affiche-t-il ?", 15, GREY)
save("97_ex3_diviseur", s + TAIL)

# ============================================================ 98 exercice 4
w, h = 760, 280
s = head(w, h)
XL, XR, YT, YB = 90, 620, 80, 230
s += source(XL, YT, YB, "U = 12 V")
s += W([(XL, YT), (XL + 130, YT)])
s += app(XL + 152, YT, "A")
s += W([(XL + 174, YT), (XL + 250, YT)])
s += res_h(XL + 290, YT, 74, 28)
s += lab(XL + 290, YT - 44, "R", "470 Ω", 16)
s += W([(XL + 327, YT), (XR, YT)])
s += W([(XR, YT), (XR, YB)]) + W([(XL, YB), (XR, YB)])
s += ih(XL + 215, YT, "I", above=True)
s += T(380, 265, "L'ampèremètre a une résistance interne de 30 Ω", 15, GREY)
save("98_ex4_serie", s + TAIL)

# ============================================================ 99 exercice 5
w, h = 780, 320
s = head(w, h)
# l'ohmmètre est relié par ses deux pointes de touche, comme au cours
YT5, YB5, CY5 = 92, 214, 153
s += app(140, CY5, "Ω")
s += W([(140, CY5 - 22), (140, YT5)]) + W([(140, YT5), (300, YT5)])
s += W([(140, CY5 + 22), (140, YB5)]) + W([(140, YB5), (300, YB5)])
s += T(140, YB5 + 28, "pointes de touche", 13, GREY)
s += W([(300, YT5), (300, CY5 - 26)]) + W([(300, CY5 + 26), (300, YB5)])
s += res_v(300, CY5, 28, 52)
s += lab(274, CY5 - 4, "R_x", "22 kΩ", 16, anchor="end")
s += W([(300, YT5), (520, YT5)]) + W([(300, YB5), (520, YB5)])
s += W([(520, YT5), (520, CY5 - 26)]) + W([(520, CY5 + 26), (520, YB5)])
s += res_v(520, CY5, 28, 52, RED)
s += T(546, CY5 - 6, "reste du circuit", 15, RED, anchor="start")
s += T(546, CY5 + 14, "33 kΩ", 15, RED, anchor="start")
s += node(300, YT5) + node(300, YB5)
s += T(390, 278, "L'ohmmètre est branché sans avoir dessoudé la résistance", 15, GREY)
save("99_ex5_ohmmetre", s + TAIL)

print("schémas 500 : ok")
