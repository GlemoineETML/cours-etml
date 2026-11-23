# -*- coding: utf-8 -*-
"""Chapitre 140 — circuits mixtes. Schémas CEI, générateurs paramétrés.

Conventions respectées :
  · COURANT  = pointe de flèche POSÉE SUR LE CONDUCTEUR, repère indicé à côté.
               I₁ = courant total débité par la source, I₂, I₃… = courants de branche.
  · TENSION  = flèche tracée À CÔTÉ du composant, du + vers le −, repère indicé.
"""
from figures import *


def node(x, y, col=NAVY):
    return f'<circle cx="{x}" cy="{y}" r="5.5" fill="{col}"/>'


def lab(x, y, nom, val=None, size=17, col=NAVY, anchor="middle", dy=19):
    """Repère (R1) et valeur (120 Ω) l'un sous l'autre."""
    s = T(x, y, nom, size, col, anchor=anchor, style="italic", weight="bold")
    if val:
        s += T(x, y + dy, val, size - 2, col, anchor=anchor)
    return s


def ih(x, y, nom, dir=1, above=True, col=NAVY, size=15):
    """Flèche de courant SUR un fil horizontal, en (x ; y). dir=1 → vers la droite."""
    d = 1 if dir >= 0 else -1
    tri = (f'<path d="M{x - 8 * d},{y - 6.5} L{x + 8 * d},{y} L{x - 8 * d},{y + 6.5} Z" '
           f'fill="{col}"/>')
    return tri + T(x, y - 13 if above else y + 25, nom, size, col)


def iv(x, y, nom, dir=1, left=True, col=NAVY, size=15):
    """Flèche de courant SUR un fil vertical, en (x ; y). dir=1 → vers le bas."""
    d = 1 if dir >= 0 else -1
    tri = (f'<path d="M{x - 6.5},{y - 8 * d} L{x},{y + 8 * d} L{x + 6.5},{y - 8 * d} Z" '
           f'fill="{col}"/>')
    tx = x - 13 if left else x + 13
    return tri + T(tx, y + 5, nom, size, col, anchor="end" if left else "start")


def uh(x0, x1, y, nom, size=16):
    """Flèche de tension au-dessus d'un composant horizontal."""
    return ((f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{BLUE}" '
             f'stroke-width="2.2" marker-end="url(#arB)"/>')
            + T((x0 + x1) / 2, y - 8, nom, size, BLUE, weight="bold"))


def source(x, ytop, ybot, u=None, arrow=True):
    """Source de tension à gauche, borne + en haut."""
    cy = (ytop + ybot) // 2
    s = W([(x, ytop), (x, cy - 24)]) + W([(x, cy + 24), (x, ybot)]) + src_v(x, cy)
    s += T(x + 30, cy - 8, "+", 17, NAVY, anchor="start", weight="bold")
    s += T(x + 30, cy + 26, "−", 17, NAVY, anchor="start", weight="bold")
    if u and arrow:
        s += (f'<line x1="{x-44}" y1="{ytop+14}" x2="{x-44}" y2="{ybot-14}" '
              f'stroke="{BLUE}" stroke-width="2.2" marker-end="url(#arB)"/>')
        s += T(x - 44, ytop - 8, u, 17, BLUE, weight="bold")
    return s


# =========================================================== topologie 1
def topo_serie_par(nom, U, r1, r2, r3):
    """R1 en série avec (R2 // R3).  I₁ total, I₂ dans R2, I₃ dans R3."""
    w, h = 620, 360
    s = head(w, h)
    XS, YT, YB = 90, 100, 300
    XA, XB = 340, 480
    s += source(XS, YT, YB, U)
    s += W([(XS, YT), (XB, YT)]) + W([(XS, YB), (XB, YB)])
    s += res_h(210, YT) + lab(210, YT + 42, r1[0], r1[1])
    s += W([(XA, YT), (XA, 168)]) + W([(XA, 232), (XA, YB)]) + res_v(XA, 200)
    s += W([(XB, YT), (XB, 168)]) + W([(XB, 232), (XB, YB)]) + res_v(XB, 200)
    s += lab(XA - 32, 196, r2[0], r2[1], anchor="end")
    s += lab(XB + 32, 196, r3[0], r3[1], anchor="start")
    s += node(XA, YT) + node(XA, YB)
    s += T(XA, YT - 34, "A", 15, GREY, weight="bold")
    s += T(XA, YB + 26, "B", 15, GREY, weight="bold")
    s += ih(150, YT, "I₁")
    s += iv(XA, 140, "I₂", left=False)
    s += iv(XB, 140, "I₃")
    s += uh(176, 244, YT - 36, "U₁")
    s += varrow(410, YT + 14, YB - 14, "U₂₃", BLUE, side="right", size=16)
    save(nom, s + TAIL)


# =========================================================== topologie 2
def topo_par_serie(nom, U, r1, r2, r3):
    """(R1 + R2) en parallèle avec R3.  I₁ total, I₂ branche série, I₃ dans R3."""
    w, h = 620, 360
    s = head(w, h)
    XS, YT, YB = 90, 100, 300
    XA, XB = 330, 480
    s += source(XS, YT, YB, U)
    s += W([(XS, YT), (XB, YT)]) + W([(XS, YB), (XB, YB)])
    s += W([(XA, YT), (XA, 138)]) + res_v(XA, 170) + W([(XA, 202), (XA, 220)])
    s += res_v(XA, 252) + W([(XA, 284), (XA, YB)])
    s += lab(XA - 32, 166, r1[0], r1[1], anchor="end")
    s += lab(XA - 32, 248, r2[0], r2[1], anchor="end")
    s += W([(XB, YT), (XB, 168)]) + res_v(XB, 200) + W([(XB, 232), (XB, YB)])
    s += lab(XB + 32, 196, r3[0], r3[1], anchor="start")
    s += node(XA, YT) + node(XA, YB)
    s += T(XA, YT - 34, "A", 15, GREY, weight="bold")
    s += T(XA, YB + 26, "B", 15, GREY, weight="bold")
    s += ih(200, YT, "I₁")
    s += iv(XA, 122, "I₂", left=False)
    s += iv(XB, 146, "I₃")
    s += varrow(XA + 34, 142, 198, "U₁", BLUE, side="right", size=16)
    s += varrow(XA + 34, 224, 280, "U₂", BLUE, side="right", size=16)
    s += varrow(XB - 28, 172, 228, "U₃", BLUE, side="left", size=16)
    save(nom, s + TAIL)


# =========================================================== topologie 3
def topo_cinq(nom, U, r1, r2, r3, r4, r5):
    """R1 + ( R2 // (R3 + R4) ) + R5.  I₁ total, I₂ dans R2, I₃ dans R3-R4."""
    w, h = 780, 380
    s = head(w, h)
    XS, YT, YB = 80, 106, 320
    XA, XB, XR = 260, 500, 700
    s += source(XS, YT, YB, U)
    s += W([(XS, YT), (XR, YT)]) + W([(XR, YT), (XR, YB)]) + W([(XS, YB), (XR, YB)])
    s += res_h(170, YT) + lab(170, YT + 40, r1[0], r1[1])
    s += res_h(380, YT) + lab(380, YT + 40, r2[0], r2[1])
    s += res_h(610, YT) + lab(610, YT + 40, r5[0], r5[1])
    YL = 220
    s += W([(XA, YT), (XA, YL)]) + W([(XA, YL), (XB, YL)]) + W([(XB, YL), (XB, YT)])
    s += res_h(330, YL) + lab(330, YL + 40, r3[0], r3[1])
    s += res_h(440, YL) + lab(440, YL + 40, r4[0], r4[1])
    s += node(XA, YT) + node(XB, YT)
    s += T(XA, YT - 36, "A", 15, GREY, weight="bold")
    s += T(XB, YT - 36, "B", 15, GREY, weight="bold")
    s += ih(126, YT, "I₁")
    s += ih(316, YT, "I₂")
    s += ih(664, YT, "I₁")
    s += iv(XA, 168, "I₃", left=False)
    s += uh(140, 200, YT - 38, "U₁", 15)
    s += uh(350, 410, YT - 38, "U₂", 15)
    s += uh(580, 640, YT - 38, "U₅", 15)
    s += uh(300, 360, YL - 28, "U₃", 15)
    s += uh(410, 470, YL - 28, "U₄", 15)
    save(nom, s + TAIL)


# =========================================================== figures du cours
topo_serie_par("40_exemple_A", "U = 12 V", ("R1", "120 Ω"), ("R2", "200 Ω"),
               ("R3", "300 Ω"))
topo_par_serie("41_exemple_B", "U = 12 V", ("R1", "100 Ω"), ("R2", "200 Ω"),
               ("R3", "600 Ω"))
topo_cinq("42_exemple_C", "U = 24 V", ("R1", "150 Ω"), ("R2", "300 Ω"),
          ("R3", "200 Ω"), ("R4", "400 Ω"), ("R5", "50 Ω"))
topo_serie_par("43_a_toi_intro", "U = 18 V", ("R1", "100 Ω"), ("R2", "200 Ω"),
               ("R3", "600 Ω"))

# ---- figures des exercices
topo_serie_par("44_ex2", "U = 15 V", ("R1", "100 Ω"), ("R2", "150 Ω"), ("R3", "300 Ω"))
topo_par_serie("45_ex3", "U = 24 V", ("R1", "200 Ω"), ("R2", "400 Ω"), ("R3", "300 Ω"))
topo_cinq("46_ex4", "U = 20 V", ("R1", "60 Ω"), ("R2", "200 Ω"), ("R3", "50 Ω"),
          ("R4", "150 Ω"), ("R5", "40 Ω"))
topo_serie_par("47_tp", "U = 10 V", ("R1", "220 Ω"), ("R2", "470 Ω"), ("R3", "1 kΩ"))

# =========================================================== réduction pas à pas
w, h = 900, 250
s = head(w, h)
s += T(150, 26, "① le circuit", 16, GREY, weight="bold")
s += W([(40, 70), (260, 70)]) + W([(40, 190), (260, 190)]) + W([(40, 70), (40, 190)])
s += res_h(100, 70) + T(100, 52, "R1", 14, NAVY, style="italic")
s += W([(180, 70), (180, 105)]) + res_v(180, 130, 22, 50) + W([(180, 155), (180, 190)])
s += W([(260, 70), (260, 105)]) + res_v(260, 130, 22, 50) + W([(260, 155), (260, 190)])
s += T(160, 134, "R2", 14, NAVY, anchor="end", style="italic")
s += T(280, 134, "R3", 14, NAVY, anchor="start", style="italic")
s += T(150, 222, "R2 // R3 = 120 Ω", 15, RED, weight="bold")
s += f'<line x1="320" y1="130" x2="380" y2="130" stroke="{RED}" stroke-width="3" marker-end="url(#arR)"/>'
s += T(500, 26, "② on remplace le groupe", 16, GREY, weight="bold")
s += W([(410, 70), (620, 70)]) + W([(410, 190), (620, 190)]) + W([(410, 70), (410, 190)])
s += res_h(470, 70) + T(470, 52, "R1", 14, NAVY, style="italic")
s += W([(620, 70), (620, 105)]) + res_v(620, 130, 22, 50) + W([(620, 155), (620, 190)])
s += T(645, 134, "R23", 14, RED, anchor="start", style="italic", weight="bold")
s += T(500, 222, "R1 + R23 = 240 Ω", 15, RED, weight="bold")
s += f'<line x1="680" y1="130" x2="730" y2="130" stroke="{RED}" stroke-width="3" marker-end="url(#arR)"/>'
s += T(800, 26, "③ une seule résistance", 16, GREY, weight="bold")
s += W([(750, 70), (850, 70)]) + W([(750, 190), (850, 190)]) + W([(750, 70), (750, 190)])
s += W([(850, 70), (850, 105)]) + res_v(850, 130, 22, 50) + W([(850, 155), (850, 190)])
s += T(828, 134, "R", 15, RED, anchor="end", style="italic", weight="bold")
s += T(800, 222, "I₁ = U / R = 50 mA", 15, RED, weight="bold")
save("48_reduction", s + TAIL)

# =========================================================== schéma tordu / propre
w, h = 900, 340
s = head(w, h)
s += T(215, 30, "à ne pas rendre", 17, RED, weight="bold")
s += W([(60, 120), (140, 90)]) + W([(140, 90), (200, 120)])
s += res_h(250, 120) + W([(200, 120), (218, 120)]) + W([(282, 120), (330, 120)])
s += W([(330, 120), (300, 200)]) + res_v(300, 228, 24, 56) + W([(300, 256), (330, 290)])
s += W([(330, 120), (392, 175)]) + res_v(392, 203, 24, 56) + W([(392, 231), (330, 290)])
s += W([(330, 290), (150, 290)]) + W([(150, 290), (60, 240)]) + W([(60, 120), (60, 240)])
s += src_v(60, 180, 22)
s += T(250, 100, "R1", 14, NAVY, style="italic")
s += T(272, 233, "R2", 14, NAVY, anchor="end", style="italic")
s += T(420, 208, "R3", 14, NAVY, anchor="start", style="italic")
s += T(215, 322, "traits obliques, jonctions floues, ni valeurs ni flèches", 14, RED)
s += T(700, 30, "à rendre", 17, "#2C7A4B", weight="bold")
XS, YT, YB, XA, XB = 530, 122, 292, 710, 820
s += source(XS, YT, YB, None, arrow=False)
s += (f'<line x1="{XS-32}" y1="{YT+14}" x2="{XS-32}" y2="{YB-14}" stroke="{BLUE}" '
      f'stroke-width="2" marker-end="url(#arB)"/>')
s += T(XS - 32, YT - 6, "U", 14, BLUE, weight="bold")
s += W([(XS, YT), (XB, YT)]) + W([(XS, YB), (XB, YB)])
s += res_h(625, YT) + lab(625, YT + 32, "R1", "120 Ω", 14)
s += W([(XA, YT), (XA, 170)]) + res_v(XA, 202) + W([(XA, 234), (XA, YB)])
s += W([(XB, YT), (XB, 170)]) + res_v(XB, 202) + W([(XB, 234), (XB, YB)])
s += lab(XA - 26, 198, "R2", "200 Ω", 14, anchor="end")
s += lab(XB + 26, 198, "R3", "300 Ω", 14, anchor="start")
s += node(XA, YT) + node(XA, YB)
s += ih(578, YT, "I₁", size=13)
s += iv(XA, 146, "I₂", left=False, size=13)
s += iv(XB, 146, "I₃", size=13)
s += uh(600, 650, YT - 26, "U₁", 13)
s += varrow(765, YT + 12, YB - 12, "U₂₃", BLUE, side="right", size=13)
s += T(700, 322, "angles droits, jonctions marquées, repères, valeurs et flèches",
       14, "#2C7A4B")
save("49_tordu_propre", s + TAIL)

# =========================================================== montage de mesure
w, h = 800, 370
s = head(w, h)
XS, YT, YB, XA, XB = 90, 100, 300, 390, 530
s += source(XS, YT, YB, "U = 10 V")
s += W([(XS, YT), (170, YT)]) + W([(210, YT), (XB, YT)]) + meter(190, YT, "A")
s += W([(XS, YB), (XB, YB)])
s += res_h(310, YT) + lab(310, YT + 42, "R1", "220 Ω")
s += W([(XA, YT), (XA, 168)]) + res_v(XA, 200) + W([(XA, 232), (XA, YB)])
s += W([(XB, YT), (XB, 168)]) + res_v(XB, 200) + W([(XB, 232), (XB, YB)])
s += lab(XA - 32, 196, "R2", "470 Ω", anchor="end")
s += lab(XB + 32, 196, "R3", "1 kΩ", anchor="start")
s += node(XA, YT) + node(XA, YB)
s += W([(XB, YT), (650, YT)]) + W([(650, YT), (650, 168)])
s += meter(650, 200, "V")
s += W([(650, 232), (650, YB)]) + W([(XB, YB), (650, YB)])
s += ih(250, YT, "I₁")
s += iv(XA, 140, "I₂", left=False)
s += iv(XB, 140, "I₃")
s += uh(278, 342, YT - 36, "U₁")
s += varrow(455, YT + 14, YB - 14, "U₂₃", BLUE, side="right", size=16)
s += T(190, 60, "en série", 15, "#2C7A4B", weight="bold")
s += T(682, 196, "en parallèle", 15, "#2C7A4B", anchor="start", weight="bold")
s += T(390, 352, "Ampèremètre EN SÉRIE · voltmètre EN PARALLÈLE", 18, NAVY, weight="bold")
save("50_montage_mesure", s + TAIL)

# =========================================================== le piège
w, h = 780, 330
s = head(w, h)
XS, YT, YB, XA, XB = 90, 80, 270, 330, 460
s += source(XS, YT, YB, None, arrow=False)
s += W([(XS, YT), (XB, YT)]) + W([(XS, YB), (XB, YB)])
s += res_h(210, YT) + lab(210, YT - 22, "R1", "220 Ω")
s += W([(XA, YT), (XA, 140)]) + res_v(XA, 172) + W([(XA, 204), (XA, YB)])
s += lab(XA - 30, 168, "R2", "470 Ω", anchor="end")
s += node(XA, YT) + node(XA, YB)
s += W([(XB, YT), (XB, 152)], RED, 3.4) + meter(XB, 175, "A", 22, RED)
s += W([(XB, 198), (XB, YB)], RED, 3.4)
s += iv(XB, 124, "I₃", left=False, col=RED, size=15)
s += T(500, 162, "COURT-CIRCUIT !", 17, RED, anchor="start", weight="bold")
s += T(500, 186, "toute la source passe", 15, RED, anchor="start")
s += T(500, 206, "dans l’appareil", 15, RED, anchor="start")
s += T(310, 310, "Ampèremètre en parallèle = fusible grillé", 18, RED, weight="bold")
save("51_piege", s + TAIL)

# =========================================================== reconnaître (exercice 1)
w, h = 900, 310
s = head(w, h)
s += T(215, 30, "a)", 18, NAVY, weight="bold", anchor="start")
XS, YT, YB, XA, XB = 80, 90, 260, 290, 400
s += source(XS, YT, YB, None, arrow=False)
s += W([(XS, YT), (XB, YT)]) + W([(XS, YB), (XB, YB)])
s += W([(XA, YT), (XA, 120)]) + res_v(XA, 148, 22, 50) + W([(XA, 173), (XA, 190)])
s += res_v(XA, 215, 22, 50) + W([(XA, 240), (XA, YB)])
s += T(XA - 24, 152, "R2", 14, NAVY, anchor="end", style="italic")
s += T(XA - 24, 220, "R3", 14, NAVY, anchor="end", style="italic")
s += W([(XB, YT), (XB, 148)]) + res_v(XB, 176, 22, 56) + W([(XB, 204), (XB, YB)])
s += T(XB + 24, 180, "R1", 14, NAVY, anchor="start", style="italic")
s += node(XA, YT) + node(XA, YB)
s += ih(180, YT, "I₁", size=14)
s += T(700, 30, "b)", 18, NAVY, weight="bold", anchor="start")
XS2, XA2, XB2 = 500, 760, 860
s += source(XS2, YT, YB, None, arrow=False)
s += W([(XS2, YT), (XB2, YT)]) + W([(XS2, YB), (XB2, YB)])
s += res_h(580, YT, 56, 24) + T(580, YT - 16, "R1", 14, NAVY, style="italic")
s += res_h(670, YT, 56, 24) + T(670, YT - 16, "R2", 14, NAVY, style="italic")
s += W([(XA2, YT), (XA2, 148)]) + res_v(XA2, 176, 22, 56) + W([(XA2, 204), (XA2, YB)])
s += W([(XB2, YT), (XB2, 148)]) + res_v(XB2, 176, 22, 56) + W([(XB2, 204), (XB2, YB)])
s += T(XA2 - 24, 180, "R3", 14, NAVY, anchor="end", style="italic")
s += T(XB2 + 24, 180, "R4", 14, NAVY, anchor="start", style="italic")
s += node(XA2, YT) + node(XA2, YB)
s += ih(534, YT, "I₁", size=14)
save("52_reconnaitre", s + TAIL)

# =========================================================== 53 : à redessiner
w, h = 500, 330
s = head(w, h)
s += W([(60, 120), (140, 90)]) + W([(140, 90), (200, 120)])
s += res_h(250, 120) + W([(200, 120), (218, 120)]) + W([(282, 120), (330, 120)])
s += W([(330, 120), (300, 200)]) + res_v(300, 228, 24, 56) + W([(300, 256), (330, 290)])
s += W([(330, 120), (392, 175)]) + res_v(392, 203, 24, 56) + W([(392, 231), (330, 290)])
s += W([(330, 290), (150, 290)]) + W([(150, 290), (60, 240)]) + W([(60, 120), (60, 240)])
s += src_v(60, 180, 22)
s += T(250, 100, "R1", 15, NAVY, style="italic")
s += T(272, 233, "R2", 15, NAVY, anchor="end", style="italic")
s += T(420, 208, "R3", 15, NAVY, anchor="start", style="italic")
save("53_tordu_seul", s + TAIL)

w, h = 520, 350
s = head(w, h)
XS, YT, YB, XA, XB = 100, 130, 305, 300, 420
s += source(XS, YT, YB, "U = 12 V")
s += W([(XS, YT), (XB, YT)]) + W([(XS, YB), (XB, YB)])
s += res_h(210, YT) + lab(210, YT + 40, "R1", "220 Ω", 15)
s += W([(XA, YT), (XA, 186)]) + res_v(XA, 218) + W([(XA, 250), (XA, YB)])
s += W([(XB, YT), (XB, 186)]) + res_v(XB, 218) + W([(XB, 250), (XB, YB)])
s += lab(XA - 28, 214, "R2", "330 Ω", 15, anchor="end")
s += lab(XB + 28, 214, "R3", "470 Ω", 15, anchor="start")
s += node(XA, YT) + node(XA, YB)
s += T(XA, YT - 34, "A", 14, GREY, weight="bold")
s += T(XA, YB + 24, "B", 14, GREY, weight="bold")
s += ih(160, YT, "I₁", size=14)
s += iv(XA, 160, "I₂", left=False, size=14)
s += iv(XB, 160, "I₃", size=14)
s += uh(180, 240, YT - 32, "U₁", 15)
s += varrow(360, YT + 14, YB - 14, "U₂₃", BLUE, side="right", size=15)
save("53_propre_seul", s + TAIL)

print("SVG chapitre 140 : ok")
