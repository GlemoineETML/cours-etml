# -*- coding: utf-8 -*-
"""Chapitre 500 — visuels de l'influence des appareils, avant / après.

Conventions :
  · COURANT  = pointe de flèche POSÉE SUR LE CONDUCTEUR, repère indicé + valeur.
  · TENSION  = flèche tracée À CÔTÉ du composant, du + vers le −, repère + valeur.
  · Une flèche de tension est d'une seule couleur, pointe comprise.
  · Toute grandeur affichée porte son unité.
"""
from figures import *
from make_svg3 import node, ih, iv, source
from make_svg5 import app, cadre_pointille

VERT = "#26663F"
MARK = {NAVY: "ar", RED: "arR", BLUE: "arB", VERT: "arV"}


def lab2(x, y, nom, val, size=17, col=NAVY, anchor="start", dy=20):
    """Repère au-dessus, valeur avec unité en dessous."""
    if anchor == "end":
        return (Tend(x, y, nom, size, col, style="italic", weight="bold")
                + T(x, y + dy, val, size - 2, col, anchor=anchor))
    return (T(x, y, nom, size, col, anchor=anchor, style="italic", weight="bold")
            + T(x, y + dy, val, size - 2, col, anchor=anchor))


def uv(x, y0, y1, nom, val, col=BLUE, side="right", size=17):
    """Flèche de tension verticale, du + vers le −, repère et valeur à côté."""
    s = (f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{col}" '
         f'stroke-width="2.4" marker-end="url(#{MARK[col]})"/>')
    tx = x + 12 if side == "right" else x - 12
    an = "start" if side == "right" else "end"
    cy = (y0 + y1) / 2
    s += (Tend(tx, cy - 2, nom, size, col, weight="bold") if an == "end"
          else T(tx, cy - 2, nom, size, col, anchor=an, weight="bold"))
    s += T(tx, cy + 18, val, size - 2, col, anchor=an)
    return s


def uh(x0, x1, y, nom, val, col=BLUE, size=17):
    """Flèche de tension horizontale, au-dessus du composant."""
    s = (f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{col}" '
         f'stroke-width="2.4" marker-end="url(#{MARK[col]})"/>')
    cx = (x0 + x1) / 2
    s += T(cx, y - 24, nom, size, col, weight="bold")
    s += T(cx, y - 7, val, size - 2, col)
    return s


def ih2(x, y, nom, val, col=NAVY, size=16, dessous=False):
    """Flèche de courant sur un fil horizontal, avec repère et valeur."""
    tri = f'<path d="M{x - 9},{y - 7} L{x + 9},{y} L{x - 9},{y + 7} Z" fill="{col}"/>'
    if dessous:
        return (tri + T(x, y + 24, nom, size, col, weight="bold")
                + T(x, y + 41, val, size - 2, col))
    return (tri + T(x, y - 30, nom, size, col, weight="bold")
            + T(x, y - 13, val, size - 2, col))


def iv2(x, y, nom, val, col=NAVY, size=16, left=True, dx=13):
    """Flèche de courant sur un fil vertical, avec repère et valeur."""
    tri = f'<path d="M{x - 7},{y - 9} L{x},{y + 9} L{x + 7},{y - 9} Z" fill="{col}"/>'
    tx = x - dx if left else x + dx
    an = "end" if left else "start"
    nomT = (Tend(tx, y - 2, nom, size, col, weight="bold") if an == "end"
            else T(tx, y - 2, nom, size, col, anchor=an, weight="bold"))
    return (tri + nomT + T(tx, y + 16, val, size - 2, col, anchor=an))


# ================================================== V1 : dans un voltmètre
w, h = 900, 390
s = head(w, h)
CX, CY = 450, 175                 # centre géométrique du boîtier
BW, BH = 400, 250                 # boîtier : R_V doit tenir dedans
s += cadre_pointille(CX - BW / 2, CY - BH / 2, BW, BH)
s += T(CX, CY - BH / 2 - 14, "VOLTMÈTRE", 16, GREY, weight="bold")
XL, XR = CX - 150, CX + 150       # nœuds internes
s += W([(70, CY), (XL, CY)]) + W([(XR, CY), (830, CY)])
YV, YR = CY - 70, CY + 72         # branche du symbole, branche de R_V
s += W([(XL, CY), (XL, YV)]) + W([(XR, CY), (XR, YV)])
s += W([(XL, YV), (CX - 24, YV)]) + W([(CX + 24, YV), (XR, YV)])
s += app(CX, YV, "V")
s += W([(XL, CY), (XL, YR)]) + W([(XR, CY), (XR, YR)])
s += W([(XL, YR), (CX - 38, YR)]) + W([(CX + 38, YR), (XR, YR)])
s += res_h(CX, YR, 76, 28, RED)
s += T(CX, YR + 36, "R_V", 18, RED, style="italic", weight="bold")
s += node(XL, CY) + node(XR, CY)
s += T(70, CY - 20, "Borne positive (V)", 15, NAVY, anchor="start", weight="bold")
s += T(830, CY - 20, "Borne négative (COM)", 15, NAVY, anchor="end", weight="bold")
s += T(CX, 356, "Numérique : 10 MΩ, la même sur tous les calibres", 16, NAVY)
s += T(CX, 378, "Analogique : elle change avec le calibre", 16, NAVY)
save("V1_dans_voltmetre", s + TAIL)

# ================================================== V2 : avant / après (voltmètre)
w, h = 1420, 540
s = head(w, h)


def diviseur(x0, avec):
    """Diviseur 5 MΩ / 5 MΩ sous 10 V ; voltmètre numérique de 10 MΩ.

    Repères de résistance à l'intérieur de la maille, vecteurs de tension à
    l'extérieur. Le voltmètre est dessiné tel qu'il est : sa résistance interne
    R_V à gauche du symbole, l'ensemble entouré d'un traitillé.
    """
    YT, XS, XB = 110, x0 + 120, x0 + 300
    YN = YT + 140                 # nœud entre R1 et R2
    YB = YT + 280                 # rail du bas
    col = RED if avec else VERT
    g = source(XS, YT, YB, None, arrow=False)
    g += W([(XS, YT), (XB, YT)]) + W([(XS, YB), (XB, YB)])
    # la tension de la source, juste à côté d'elle
    g += uv(XS - 52, YT + 12, YB - 12, "U", "10,0 V", col=BLUE, side="left")
    # R1 en haut — repère à l'intérieur, vecteur à l'extérieur
    g += res_v(XB, YT + 70, 30, 66)
    g += W([(XB, YT), (XB, YT + 37)]) + W([(XB, YT + 103), (XB, YN)])
    g += lab2(XB - 26, YT + 62, "R_1", "5 MΩ", anchor="end")
    g += uv(XB + 36, YT + 37, YT + 103, "U_1", "6,00 V" if avec else "5,00 V",
            col=col, side="right")
    # R2 en bas
    g += res_v(XB, YT + 215, 30, 66)
    g += W([(XB, YN), (XB, YT + 182)]) + W([(XB, YT + 248), (XB, YB)])
    g += lab2(XB - 26, YT + 207, "R_2", "5 MΩ", anchor="end")
    if avec:
        XV, YM = XB + 210, YT + 210          # branche R_V, milieu du voltmètre
        XW = XV + 68                          # branche du symbole
        g += cadre_pointille(XV - 106, YN - 30, (XW + 42) - (XV - 106),
                             (YB + 30) - (YN - 30))
        g += T((XV + XW) / 2, YN - 42, "VOLTMÈTRE", 15, GREY, weight="bold")
        g += W([(XB, YN), (XW, YN)]) + W([(XB, YB), (XW, YB)])
        g += W([(XV, YN), (XV, YM - 33)]) + W([(XV, YM + 33), (XV, YB)])
        g += res_v(XV, YM, 30, 66, col=RED)
        g += W([(XW, YN), (XW, YM - 22)]) + W([(XW, YM + 22), (XW, YB)])
        g += app(XW, YM, "V")
        g += node(XV, YN) + node(XV, YB) + node(XB, YN) + node(XB, YB)
        g += lab2(XV - 20, YM - 10, "R_V", "10 MΩ", anchor="end", col=RED)
        g += iv2(XB, YT + 161, "I_2", "0,80 µA", left=True, dx=26)
        g += ih2(XB + 54, YN, "I_V", "0,40 µA", col=RED, dessous=True)
        g += ih2(XS + 100, YT, "I_1", "1,20 µA")
        # U2 à droite du voltmètre, hors du traitillé
        g += uv(XW + 62, YN + 6, YB - 6, "U_2", "4,00 V", col=RED, side="right")
    else:
        g += ih2(XS + 100, YT, "I_1", "1,00 µA")
        g += uv(XB + 36, YT + 182, YT + 248, "U_2", "5,00 V", col=VERT,
                side="right")
    return g


s += T(290, 46, "SANS voltmètre — ce que tu as calculé", 18, VERT, weight="bold")
s += diviseur(20, False)
s += T(1020, 46, "AVEC le voltmètre — ce qui existe vraiment", 18, RED,
       weight="bold")
s += diviseur(660, True)
s += (f'<line x1="{560}" y1="250" x2="{610}" y2="250" stroke="{RED}" '
      f'stroke-width="4" marker-end="url(#arR)"/>')
s += T(290, 512, "le voltmètre ne prend aucun courant", 16, VERT)
s += T(1020, 512, "il prend 0,40 µA — au nœud : 0,80 + 0,40 = 1,20 µA", 16, RED)
save("V2_avant_apres", s + TAIL, scale=2.0)

# ================================================== A1 : dans un ampèremètre
w, h = 940, 330
s = head(w, h)
CX, CY = 470, 160
BW, BH = 400, 140
s += cadre_pointille(CX - BW / 2, CY - BH / 2, BW, BH)
s += T(CX, CY - BH / 2 - 14, "AMPÈREMÈTRE", 16, GREY, weight="bold")
s += W([(70, CY), (CX - 130, CY)])
s += app(CX - 108, CY, "A")
s += W([(CX - 86, CY), (CX + 30, CY)])
s += res_h(CX + 68, CY, 76, 28, RED)
s += W([(CX + 106, CY), (870, CY)])
s += T(CX + 68, CY - 28, "R_A", 18, RED, style="italic", weight="bold")
s += ih2(180, CY, "I", "le courant à mesurer", col=NAVY)
s += T(70, CY + 34, "Borne d’entrée", 15, NAVY, anchor="start", weight="bold")
s += T(70, CY + 54, "(A / mA / µA)", 14, NAVY, anchor="start")
s += T(870, CY + 34, "Borne de sortie", 15, NAVY, anchor="end", weight="bold")
s += T(870, CY + 54, "(COM)", 14, NAVY, anchor="end")
s += T(CX, 312, "De quelques ohms à quelques dizaines d’ohms selon le calibre",
       16, NAVY)
save("A1_dans_amperemetre", s + TAIL)

# ================================================== A2 : avant / après (ampèremètre)
w, h = 1480, 480
s = head(w, h)


def boucle(x0, avec):
    """Boucle 10 V / 180 Ω ; l'ampèremètre a 20 Ω de résistance interne.

    R est dessinée verticalement, sur la branche de droite, avec son vecteur
    U_R tourné de même et placé à l'extérieur de la maille.
    """
    YT, YB, XS, XB = 170, 370, x0 + 90, x0 + 520
    YM = (YT + YB) / 2
    col = RED if avec else VERT
    g = source(XS, YT, YB, None, arrow=False)
    g += W([(XS, YB), (XB, YB)])
    g += uv(XS - 52, YT + 12, YB - 12, "U", "10,0 V", col=BLUE, side="left")
    # la résistance du circuit : verticale, à droite
    g += W([(XB, YT), (XB, YM - 33)]) + W([(XB, YM + 33), (XB, YB)])
    g += res_v(XB, YM, 30, 66)
    g += lab2(XB - 26, YM - 10, "R", "180 Ω", anchor="end")
    g += uv(XB + 42, YM - 42, YM + 42, "U_R", "9,00 V" if avec else "10,0 V",
            col=col, side="right")
    if avec:
        g += W([(XS, YT), (x0 + 180, YT)])
        g += cadre_pointille(x0 + 180, YT - 38, 230, 76)
        g += T(x0 + 218, YT + 60, "AMPÈREMÈTRE", 14, GREY, weight="bold")
        g += app(x0 + 226, YT, "A")
        g += W([(x0 + 248, YT), (x0 + 288, YT)])
        g += res_h(x0 + 326, YT, 76, 28, RED)
        g += T(x0 + 326, YT + 54, "R_A", 15, RED, style="italic", weight="bold")
        g += T(x0 + 326, YT + 72, "20 Ω", 13, RED)
        g += W([(x0 + 364, YT), (XB, YT)])
        # U_A dans le sens de R_A, à l'extérieur de la boucle
        g += uh(x0 + 288, x0 + 364, YT - 54, "U_A", "1,00 V", col=RED)
        g += ih2(x0 + 150, YT, "I", "50,0 mA", col=RED, dessous=True)
    else:
        g += W([(XS, YT), (XB, YT)])
        g += ih2(x0 + 260, YT, "I", "55,6 mA", col=VERT, dessous=True)
    return g


s += T(330, 48, "SANS ampèremètre — ce que tu as calculé", 18, VERT,
       weight="bold")
s += boucle(40, False)
s += T(1090, 48, "AVEC l’ampèremètre — ce qui existe vraiment", 18, RED,
       weight="bold")
s += boucle(800, True)
s += (f'<line x1="{700}" y1="270" x2="{744}" y2="270" stroke="{RED}" '
      f'stroke-width="4" marker-end="url(#arR)"/>')
s += T(330, 452, "toute la tension arrive sur R", 16, VERT)
s += T(1090, 452, "la maille se partage : 1,00 + 9,00 = 10,0 V", 16, RED)
save("A2_avant_apres", s + TAIL, scale=2.0)

# ================================================== O1 : comment mesure un ohmmètre
w, h = 820, 320
s = head(w, h)
CX, CY = 270, 155
BW, BH = 310, 150
XG, XD = CX - BW / 2, CX + BW / 2
YH, YBs = CY - 45, CY + 45
s += cadre_pointille(XG, CY - BH / 2, BW, BH)
s += T(CX, CY - BH / 2 - 16, "OHMMÈTRE", 16, GREY, weight="bold")
s += W([(XG + 40, YH), (XD, YH)]) + W([(XG + 40, YBs), (XD, YBs)])
s += W([(XG + 40, YH), (XG + 40, YBs)])
XI, XV = CX - 50, CX + 60
for xb in (XI, XV):
    s += W([(xb, YH), (xb, CY - 22)]) + W([(xb, CY + 22), (xb, YBs)])
s += isrc_v(XI, CY, 22)
s += app(XV, CY, "V", r=22)
s += node(XI, YH) + node(XI, YBs) + node(XV, YH) + node(XV, YBs)
XR0 = 650
s += W([(XD, YH), (XR0, YH)]) + W([(XD, YBs), (XR0, YBs)])
s += W([(XR0, YH), (XR0, CY - 24)]) + W([(XR0, CY + 24), (XR0, YBs)])
s += res_v(XR0, CY, 30, 48)
s += T(XR0 + 26, CY + 4, "R", 18, NAVY, anchor="start", style="italic",
       weight="bold")
s += ih2(550, YH, "I", "imposé", col=BLUE)
s += T(410, 300, "Il impose un courant connu et lit la tension : R = U / I",
       16, NAVY)
save("O1_dans_ohmmetre", s + TAIL)

# ================================================== AN1 : analogique / numérique
w, h = 980, 390
s = head(w, h)
s += T(245, 42, "voltmètre ANALOGIQUE  20 kΩ/V", 17, NAVY, weight="bold")
s += T(735, 42, "multimètre NUMÉRIQUE", 17, NAVY, weight="bold")
base, ech = 300, 0.00020
for i, (cal, rv, txt) in enumerate([(3, 60e3, "60 kΩ"), (10, 200e3, "200 kΩ"),
                                    (30, 600e3, "600 kΩ")]):
    x = 130 + i * 115
    ht = 18 + rv * ech
    s += (f'<rect x="{x - 34}" y="{base - ht}" width="68" height="{ht}" '
          f'fill="{LBLUE}" stroke="{NAVY}" stroke-width="2"/>')
    s += T(x, base - ht - 10, txt, 15, NAVY, weight="bold")
    s += T(x, base + 22, "calibre %d V" % cal, 14, GREY)
s += W([(90, base), (470, base)], NAVY, 2.4)
s += T(245, base + 52, "elle change avec le calibre", 16, RED)

x, ht = 730, 200
s += (f'<rect x="{x - 60}" y="{base - ht}" width="120" height="{ht}" '
      f'fill="#D6E8F7" stroke="{NAVY}" stroke-width="2"/>')
s += T(x, base - ht - 10, "10 MΩ", 17, NAVY, weight="bold")
s += T(x, base + 22, "tous calibres", 14, GREY)
s += W([(560, base), (900, base)], NAVY, 2.4)
s += T(730, base + 52, "elle est constante, et 50 fois plus grande", 16, VERT)
s += T(490, 190, "≠", 30, GREY, weight="bold")
save("AN1_comparaison", s + TAIL)

print("visuels 500 : ok")

# ================================================== F1 : la fiche technique du Fluke 87
# Table 12 du Users Manual 80 Series V, colonne « Model 87 », reprise telle quelle.
w, h = 1300, 540
s = head(w, h)
COLS = [(50, 210), (210, 460), (460, 710), (710, 1250)]
ENTETE = ["Fonction", "Échelle (gamme)", "Résolution", "Précision — modèle 87"]
LIGNES = [("V (DC)", "6,000 V", "0,001 V", "± (0,05 % + 1)"),
          ("", "60,00 V", "0,01 V", "± (0,05 % + 1)"),
          ("", "600,0 V", "0,1 V", "± (0,05 % + 1)"),
          ("", "1000 V", "1 V", "± (0,05 % + 1)"),
          ("mV (DC)", "600,0 mV", "0,1 mV", "± (0,1 % + 1)")]
YH, HL = 66, 46                    # haut de l'en-tête, hauteur d'une ligne


def cell(x0, x1, y0, y1, txt, gras=False, col=NAVY, fond=None, size=17):
    g = ""
    if fond:
        g += (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
              f'fill="{fond}"/>')
    g += (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
          f'fill="none" stroke="{GREY}" stroke-width="1.4"/>')
    if txt:
        g += T((x0 + x1) / 2, (y0 + y1) / 2 + 6, txt, size, col,
               weight="bold" if gras else "normal")
    return g


for (x0, x1), e in zip(COLS, ENTETE):
    s += cell(x0, x1, YH, YH + HL, e, gras=True, fond="#EEF2F8", size=16)
for k, ligne in enumerate(LIGNES):
    y0 = YH + HL * (k + 1)
    for (x0, x1), txt in zip(COLS, ligne):
        rouge = (k == 0)            # l'échelle utilisée par notre exemple
        s += cell(x0, x1, y0, y0 + HL, txt,
                  gras=rouge, col=RED if rouge else NAVY,
                  fond="#FDEDED" if rouge else None)
YF = YH + HL * 6

# les quatre colonnes expliquées, comme sur la fiche ETML
NOTES = ["ce que l’on mesure", "le calibre choisi",
         "la plus petite valeur\nque l’appareil distingue",
         "elle dépend du modèle,\nde la fonction et de l’échelle"]
for (x0, x1), n_ in zip(COLS, NOTES):
    cx = (x0 + x1) / 2
    s += W([(cx, YF + 6), (cx, YF + 26)], GREY, 1.6)
    for j, bout in enumerate(n_.split("\n")):
        s += T(cx, YF + 46 + 19 * j, bout, 14, GREY)

s += (f'<rect x="50" y="{YF + 108}" width="1200" height="62" fill="none" '
      f'stroke="{RED}" stroke-width="2" rx="6"/>')
s += T(650, YF + 134, "Précision = ± ( pourcentage de la LECTURE  +  un nombre "
                      "de fois la RÉSOLUTION )", 18, RED, weight="bold")
s += T(650, YF + 158, "à 18–28 °C, humidité ≤ 90 %, dans l’année qui suit "
                      "l’étalonnage", 14, GREY)
save("F1_fiche_fluke87", s + TAIL, scale=1.7)

print("fiche technique 87 : ok")
