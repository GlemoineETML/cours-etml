# -*- coding: utf-8 -*-
"""105 Familles de circuits logiques – animation (TM1 – El DT 1, semaine 1, va avec la présentation 100 et la fiche 110).
Valeurs : moteur/logique.py, NIV (Floyd 3-8 p. 154, fiche M74HCT00), tPD = 12 ns (M74HCT00, VCC = 4,5 V).
Rendu : python3 build.py tm1/semaine-1 --seulement animations · aperçu : voir en bas"""
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))   # aperçu direct
from moteur.anim import *
from moteur import logique as D

FOOT[0] = "Test et Mesure 1 – El DT 1 · 105 Familles de circuits logiques · Floyd 3-8"
TOT = "5"
v_ = lambda x: f"{x:g}".replace(".", ",") + NB + "V"


# ================================================================ 1 · lire une référence
PARTS = [("SN", "fabricant", "Texas Instruments (chez ST : M, chez onsemi : MC)", GREY),
         ("74", "plage", "commerciale, 0 … 70 °C (54 : militaire, −55 … 125 °C)", NAVY),
         ("HCT", "technologie", "CMOS, entrées compatibles TTL", BLUE),
         ("00", "fonction", "4 portes NON-ET à 2 entrées", NAVY),
         ("N", "boîtier", "DIP 14 (D : SOIC 14)", GREY)]
S1_T0, S1_DT = 3.0, 4.5


def dip(d, x, y, mark, alpha=1.0, w=420, h=190):
    """Boîtier DIP 14 vu de dessus, encoche à gauche."""
    c = mix(WHITE, NAVY, alpha)
    for i in range(7):
        px = x + 35 + i * (w - 70) / 6
        d.rectangle((px - 12, y - 28, px + 12, y), fill=mix(WHITE, LGREY, alpha), outline=c, width=2)
        d.rectangle((px - 12, y + h, px + 12, y + h + 28), fill=mix(WHITE, LGREY, alpha), outline=c, width=2)
    d.rounded_rectangle((x, y, x + w, y + h), radius=10, fill=mix(WHITE, (52, 56, 70), alpha), outline=c, width=3)
    d.pieslice((x - 26, y + h / 2 - 26, x + 26, y + h / 2 + 26), 270, 90, fill=mix(WHITE, (30, 32, 44), alpha))
    d.ellipse((x + 24, y + h - 46, x + 44, y + h - 26), fill=mix(WHITE, (110, 116, 130), alpha))
    text(d, (x + w / 2, y + h / 2 - 8), mark, 38, mix(WHITE, (235, 238, 245), alpha), True, mono=True, anchor="mm")
    text(d, (x + 36, y + h + 52), "1", 22, c, True, anchor="mm")


def s_ref(img, d, t):
    chrome(img, d, "1 · LIRE UNE RÉFÉRENCE DE CI", "SN74HCT00N, partie par partie", f"1/{TOT}")
    ref_pill(d, "Floyd 3-8 p. 146 · présentation 100, diapo 5")
    bw, gap, x0 = 300, 22, 95
    for i, (code, role, det, col) in enumerate(PARTS):
        x = x0 + i * (bw + gap)
        on = prog(t, S1_T0 + i * S1_DT, S1_T0 + i * S1_DT + 0.8)
        cur = S1_T0 + i * S1_DT <= t < S1_T0 + (i + 1) * S1_DT and t < S1_T0 + 5 * S1_DT
        rbox(d, (x, 190, x + bw, 330), fill=mix(LGREY, col, max(on, 0.15)), outline=BLUE if cur else None, width=6, r=12)
        text(d, (x + bw / 2, 260), code, 74, WHITE, True, anchor="mm")
        if on > 0:
            text(d, (x + bw / 2, 362), role, 30, mix(WHITE, col if col != GREY else NAVY, on), True, anchor="mm")
            lines = wrap(det, 23, bw - 16)
            for k, ln in enumerate(lines):
                text(d, (x + bw / 2, 400 + k * 30), ln, 23, mix(WHITE, GREY, on), anchor="mm")
    # étiquette de tiroir + boîtier
    q = prog(t, 0.3, 1.5)
    dip(d, 170, 560, "SN74HCT00N", q)
    text(d, (380, 840), "vue de dessus · encoche et point = broche 1", 22, mix(WHITE, GREY, q), italic=True, anchor="mm")
    T2 = S1_T0 + 5 * S1_DT + 0.5
    q2 = prog(t, T2, T2 + 1.0)
    if q2 > 0:
        rbox(d, (780, 530, 1720, 880), fill=mix(WHITE, PALE, q2), outline=mix(WHITE, NAVY, q2), width=3, r=16)
        text(d, (810, 555), "Peut-on le remplacer par… ?", 28, mix(WHITE, BLUE, q2), True)
        rows = [("M74HCT00 (STMicroelectronics)", "même fonction, même famille, même brochage", True, T2 + 0.8),
                ("SN74HC00N", "même brochage, mais entrées CMOS : VIH = 3,5 V", None, T2 + 4.5),
                ("CD4011BE (série 4000)", "4 NON-ET aussi, mais un autre brochage", False, T2 + 8.0)]
        for k, (a, b, ok, t0) in enumerate(rows):
            r = prog(t, t0, t0 + 0.8)
            if r <= 0: continue
            y = 620 + k * 82
            if ok is None:
                d.ellipse((815, y, 865, y + 50), fill=mix(WHITE, ORANGE, r)); text(d, (840, y + 25), "?", 32, WHITE, True, anchor="mm")
            else:
                check(d, (840, y + 25), ok, 50, r)
            text(d, (890, y + 2), a, 27, mix(WHITE, NAVY, r), True)
            text(d, (890, y + 34), b, 23, mix(WHITE, GREY, r))
    caption(d, cap_at(t, [
        (0, "Sur le tiroir des pièces de rechange : SN74HCT00N. Chaque partie de la référence donne une information."),
        (S1_T0, "SN : le fabricant, ici Texas Instruments. Chez STMicroelectronics, la même puce s'appelle M74HCT00."),
        (S1_T0 + S1_DT, "74 : la série 74, plage commerciale de 0 à 70 °C. Un 54 au même endroit désigne la version militaire."),
        (S1_T0 + 2 * S1_DT, "HCT : la technologie. Structure CMOS, mais des entrées compatibles TTL, qui lisent un 1 dès 2 V."),
        (S1_T0 + 3 * S1_DT, "00 : la fonction. Dans toute la série 74, 00 = 4 portes NON-ET, 08 = 4 portes ET, 04 = 6 inverseurs."),
        (S1_T0 + 4 * S1_DT, "N : le boîtier. N = DIP 14, pour la breadboard. D = SOIC 14, pour une carte fabriquée en série."),
        (T2 + 0.8, "M74HCT00 : autre fabricant, mais même famille et même fonction. Il remplace le SN74HCT00 sans rien changer."),
        (T2 + 4.5, "SN74HC00N : même brochage, mais ses entrées exigent 3,5 V pour un 1. Sur une ancienne carte TTL, ça ne suffit pas."),
        (T2 + 8.0, "CD4011BE : 4 NON-ET aussi, mais série 4000. Les broches ne sont pas au même endroit : il faudrait refaire la carte."),
    ]))


# ================================================================ 2 · niveaux d'entrée
VIL, VIH = D.NIV["HCT"][0], D.NIV["HCT"][1]
MEAS = [0.3, 3.6, 1.5, 2.2, 0.9]
S2_T0, S2_DT = 7.0, 6.0
SY0, SY1 = 200, 820            # 5 V en haut, 0 V en bas
VY = lambda v: SY1 - v / 5 * (SY1 - SY0)


def lu(v):
    if v <= VIL: return "0", f"{v_(v)} ≤ {v_(VIL)} : la porte lit un 0."
    if v >= VIH: return "1", f"{v_(v)} ≥ {v_(VIH)} : la porte lit un 1."
    return "?", f"{v_(v)} est entre {v_(VIL)} et {v_(VIH)} : l'état n'est pas garanti."


def scale(d, x, alpha, title, vil, vih, w=130, labels=True):
    c = lambda col: mix(WHITE, col, alpha)
    d.rectangle((x, VY(5), x + w, VY(vih)), fill=c(BLUE))
    d.rectangle((x, VY(vih), x + w, VY(vil)), fill=c((213, 219, 228)))
    d.rectangle((x, VY(vil), x + w, VY(0)), fill=c(NAVY))
    d.rectangle((x, VY(5), x + w, VY(0)), outline=c(NAVY), width=3)
    text(d, (x + w / 2, (VY(5) + VY(vih)) / 2), "1", 54, c(WHITE), True, anchor="mm")
    text(d, (x + w / 2, (VY(vil) + VY(0)) / 2), "0", 40 if VY(0) - VY(vil) > 60 else 26, c(WHITE), True, anchor="mm")
    text(d, (x + w / 2, VY(5) - 30), title, 26, c(NAVY), True, anchor="mm")
    if labels:
        for v in (0, vil, vih, 5):
            text(d, (x - 14, VY(v)), v_(v), 22, c(GREY), anchor="rm")


def s_levels(img, d, t):
    chrome(img, d, "2 · LES NIVEAUX D'ENTRÉE", "Quand une tension devient un 0 ou un 1", f"2/{TOT}")
    ref_pill(d, "fiche M74HCT00 · Floyd 3-8 p. 154 · diapo 16")
    a = prog(t, 0.3, 1.5)
    scale(d, 300, a, "Entrée 74HCT00 (VCC = 5 V)", VIL, VIH, 150)
    # étiquettes des seuils
    for v, lab, col in ((VIH, f"VIH min = {v_(VIH)}", BLUE), (VIL, f"VIL max = {v_(VIL)}", NAVY)):
        q = prog(t, 3.0, 4.0)
        d.line((450, VY(v), 520, VY(v)), fill=mix(WHITE, col, q), width=3)
        text(d, (530, VY(v)), lab, 26, mix(WHITE, col, q), True, anchor="lm")
    q = prog(t, 3.0, 4.0)
    text(d, (530, (VY(VIH) + VY(VIL)) / 2), "zone interdite : état non garanti", 22, mix(WHITE, GREY, q), True, italic=True, anchor="lm")
    # mesure courante
    k = int((t - S2_T0) // S2_DT) if t >= S2_T0 else -1
    k = min(k, len(MEAS) - 1)
    if k >= 0:
        tk = S2_T0 + k * S2_DT
        prev = MEAS[k - 1] if k > 0 else 0.0
        v = prev + (MEAS[k] - prev) * prog(t, tk, tk + 1.2)
        y = VY(v)
        d.line((300, y, 450, y), fill=RED, width=4)
        d.polygon([(452, y), (492, y - 18), (492, y + 18)], fill=RED)
        # multimètre
        mx, my = 1060, 210
        rbox(d, (mx, my, mx + 520, my + 400), fill=(250, 196, 40), outline=NAVY, width=4, r=30)
        display(d, (mx + 50, my + 40, mx + 470, my + 180), "V DC", f"{MEAS[k]:.1f}".replace(".", ",") + " V" if t >= tk + 1.2 else f"{v:.1f}".replace(".", ",") + " V", 64)
        d.ellipse((mx + 190, my + 220, mx + 330, my + 360), fill=(60, 64, 80), outline=NAVY, width=4)
        d.line((mx + 260, my + 290, mx + 300, my + 240), fill=WHITE, width=6)
        st, js = lu(MEAS[k])
        r = prog(t, tk + 1.4, tk + 2.2)
        col = BLUE if st == "1" else (NAVY if st == "0" else ORANGE)
        rbox(d, (1000, 660, 1720, 860), fill=mix(WHITE, TINT, r), outline=mix(WHITE, col, r), width=4, r=16)
        text(d, (1030, 690), "État lu par la porte", 26, mix(WHITE, GREY, r), True)
        text(d, (1030, 722), "non garanti" if st == "?" else st, 52, mix(WHITE, col, r), True)
        para(d, (1030, 800), js, 25, 660, mix(WHITE, NAVY, r))
        # historique
        for j in range(k + 1):
            sj, _ = lu(MEAS[j])
            x = 700 + j * 66
            rbox(d, (x, 860 - 64, x + 58, 860), fill=TINT, r=8)
            text(d, (x + 29, 860 - 44), f"{MEAS[j]:g}".replace(".", ","), 20, NAVY, True, anchor="mm")
            text(d, (x + 29, 860 - 18), "?" if sj == "?" else sj, 22, ORANGE if sj == "?" else (BLUE if sj == "1" else NAVY), True, anchor="mm")
    seq = [(0, "Une entrée de porte ne lit pas une tension au millivolt près : elle la range dans une zone. Les seuils sont dans la fiche technique."),
           (3.0, f"Au-dessus de VIH min = {v_(VIH)}, le 74HCT00 lit un 1. En dessous de VIL max = {v_(VIL)}, il lit un 0. Entre les deux, rien n'est garanti.")]
    msg = {0.3: "Mesure 0,3 V : bien en dessous de 0,8 V. La porte lit un 0, avec une bonne réserve.",
           3.6: "Mesure 3,6 V : au-dessus de 2 V. La porte lit un 1.",
           1.5: "Mesure 1,5 V : dans la zone interdite. La porte peut lire un 0 ou un 1, au hasard. Souvent une entrée en l'air.",
           2.2: "Mesure 2,2 V : c'est encore un 1, mais avec peu de réserve. Un petit parasite et on retombe dans la zone interdite.",
           0.9: "Mesure 0,9 V : juste au-dessus de 0,8 V. On est déjà dans la zone interdite : ce n'est plus un 0 garanti."}
    for j, m in enumerate(MEAS):
        seq.append((S2_T0 + j * S2_DT + 1.4, msg[m]))
    seq.append((S2_T0 + len(MEAS) * S2_DT + 0.5, "En dépannage, on mesure l'entrée et on compare à VIH et VIL. Une entrée CMOS inutilisée se relie à GND ou à VCC."))
    caption(d, cap_at(t, seq))


# ================================================================ 3 · compatibilité et marge de bruit
CASES = [("TTL", "HC", "Sortie TTL → entrée 74HC"), ("TTL", "HCT", "Sortie TTL → entrée 74HCT"), ("HC", "HC", "Sortie 74HC → entrée 74HC")]
S3_T = [3.0, 17.0, 31.0]
NAME = {"TTL": "TTL", "HC": "74HC", "HCT": "74HCT"}


def s_compat(img, d, t):
    chrome(img, d, "3 · COMPATIBILITÉ ET MARGE DE BRUIT", "Ce que la sortie garantit, ce que l'entrée exige", f"3/{TOT}")
    ref_pill(d, "Floyd 3-8 p. 154 · diapo 17")
    k = 0
    for i, t0 in enumerate(S3_T):
        if t >= t0: k = i
    src, dst, title = CASES[k]
    # interpolation des niveaux entre deux cas
    def lev(i):
        s, e, _ = CASES[i]
        return D.NIV[s][2], D.NIV[s][3], D.NIV[e][0], D.NIV[e][1]
    cur = lev(k)
    if k > 0:
        p = prog(t, S3_T[k], S3_T[k] + 1.2)
        old = lev(k - 1)
        cur = tuple(o + (c - o) * p for o, c in zip(old, cur))
    vol, voh, vil, vih = cur
    a = prog(t, 0.3, 1.5)
    xs, xe, w = 290, 640, 140
    # barre de sortie : 1 garanti au-dessus de VOH, 0 garanti sous VOL
    c = lambda col: mix(WHITE, col, a)
    d.rectangle((xs, VY(5), xs + w, VY(voh)), fill=c(BLUE))
    d.rectangle((xs, VY(voh), xs + w, VY(vol)), fill=c((213, 219, 228)))
    d.rectangle((xs, VY(vol), xs + w, VY(0)), fill=c(NAVY))
    d.rectangle((xs, VY(5), xs + w, VY(0)), outline=c(NAVY), width=3)
    text(d, (xs + w / 2, (VY(5) + VY(voh)) / 2), "1", 46, c(WHITE), True, anchor="mm")
    text(d, (xs + w / 2, VY(5) - 30), f"Sortie {NAME[src]}", 28, c(NAVY), True, anchor="mm")
    text(d, (xs + w / 2, VY(0) + 30), "garantit", 22, c(GREY), italic=True, anchor="mm")
    d.rectangle((xe, VY(5), xe + w, VY(vih)), fill=c(BLUE))
    d.rectangle((xe, VY(vih), xe + w, VY(vil)), fill=c((213, 219, 228)))
    d.rectangle((xe, VY(vil), xe + w, VY(0)), fill=c(NAVY))
    d.rectangle((xe, VY(5), xe + w, VY(0)), outline=c(NAVY), width=3)
    text(d, (xe + w / 2, (VY(5) + VY(vih)) / 2), "1", 46, c(WHITE), True, anchor="mm")
    text(d, (xe + w / 2, VY(5) - 30), f"Entrée {NAME[dst]}", 28, c(NAVY), True, anchor="mm")
    text(d, (xe + w / 2, VY(0) + 30), "exige", 22, c(GREY), italic=True, anchor="mm")
    for v in (0, 5):
        text(d, (xs - 14, VY(v)), f"{v}" + NB + "V", 20, c(GREY), anchor="rm")
    # liaisons VOH → VIH et VOL → VIL
    nh, nl = voh - vih, vil - vol
    for (y1, y2, ok, lab, side) in ((VY(voh), VY(vih), nh >= -1e-9, f"VOH {v_(round(voh, 2))}", "h"), (VY(vol), VY(vil), nl >= -1e-9, f"VOL {v_(round(vol, 2))}", "l")):
        col = GREEN if ok else RED
        d.line((xs + w, y1, xe, y2), fill=col, width=4)
    lab_s = [(VY(voh), f"VOH min {v_(round(voh, 2))}"), (VY(vol), f"VOL max {v_(round(vol, 2))}")]
    lab_e = [(VY(vih), f"VIH min {v_(round(vih, 2))}"), (VY(vil), f"VIL max {v_(round(vil, 2))}")]
    for y_, s_ in lab_s:
        d.line((xs - 10, y_, xs, y_), fill=NAVY, width=2)
        text(d, (xs - 14, y_), s_, 22, NAVY, True, anchor="rm")
    for y_, s_ in lab_e:
        d.line((xe + w, y_, xe + w + 10, y_), fill=NAVY, width=2)
        text(d, (xe + w + 14, y_), s_, 22, NAVY, True, anchor="lm")
    # parasite sur la ligne (cas 74HC → 74HC)
    TN = S3_T[2] + 7.0
    if k == 2 and t >= TN:
        q = prog(t, TN, TN + 1.0)
        pts = []
        for i in range(0, xe - xs - w - 20, 4):
            x = xs + w + 10 + i
            vv = voh + 0.55 * math.sin(i / 9 + t * 5) * math.sin(i / 37 + 1.3)
            pts.append((x, VY(vv)))
        d.line(pts, fill=mix(WHITE, ORANGE, q), width=4)
        label_box(d, (xs + w + 130, VY(voh - 0.8)), "parasite ± 0,55 V", 20, ORANGE, alpha=q)
    # panneau de droite
    X = 1000
    rbox(d, (X, 190, 1720, 330), fill=PALE, outline=NAVY, width=3, r=16)
    text(d, (X + 30, 215), "Compatible si…", 26, BLUE, True)
    text(d, (X + 30, 255), "VOH(sortie) ≥ VIH(entrée)", 28, NAVY, True)
    text(d, (X + 30, 292), "et  VOL(sortie) ≤ VIL(entrée)", 28, NAVY, True)
    r = prog(t, S3_T[k] + 1.2, S3_T[k] + 2.2)
    rbox(d, (X, 360, 1720, 870), fill=mix(WHITE, TINT, r), r=16)
    text(d, (X + 30, 385), title, 32, mix(WHITE, NAVY, r), True)
    okh, okl, NH, NL = D.compat(src, dst)
    S, E = D.NIV[src], D.NIV[dst]
    lines = [(okh, f"VOH {v_(S[3])} {'≥' if okh else '<'} VIH {v_(E[1])}", 2.5),
             (okl, f"VOL {v_(S[2])} {'≤' if okl else '>'} VIL {v_(E[0])}", 4.5)]
    for j, (ok, s, dt) in enumerate(lines):
        q = prog(t, S3_T[k] + dt, S3_T[k] + dt + 0.8)
        if q <= 0: continue
        check(d, (X + 55, 470 + j * 70), ok, 46, q)
        text(d, (X + 95, 470 + j * 70), s, 30, mix(WHITE, NAVY, q), True, anchor="lm")
    q = prog(t, S3_T[k] + 6.5, S3_T[k] + 7.3)
    if q > 0:
        res = "compatible" if okh and okl else "pas compatible"
        text(d, (X + 30, 600), res.capitalize(), 40, mix(WHITE, GREEN if okh and okl else RED, q), True)
        if okh and okl:
            text(d, (X + 30, 660), f"Marges de bruit : NH = {v_(NH)} · NL = {v_(NL)}", 27, mix(WHITE, NAVY, q))
        else:
            text(d, (X + 30, 660), "Le 1 de la sortie n'est pas un 1 garanti pour l'entrée.", 27, mix(WHITE, NAVY, q))
            text(d, (X + 30, 700), "Solution : une entrée 74HCT (VIH = 2 V).", 27, mix(WHITE, BLUE, q), True)
    caption(d, cap_at(t, [
        (0, "Pour relier une sortie à une entrée, on compare deux fiches techniques : ce que la sortie garantit et ce que l'entrée exige."),
        (S3_T[0] + 1.5, "Cas 1 : ancienne carte TTL vers carte 74HC. La sortie TTL garantit un 1 dès 2,4 V. L'entrée 74HC exige au moins 3,5 V."),
        (S3_T[0] + 6.5, "2,4 V < 3,5 V : le 1 n'est pas garanti. La liaison peut marcher sur la table et échouer dans la machine."),
        (S3_T[1] + 1.5, "Cas 2 : même sortie TTL, mais entrée 74HCT. Ses entrées sont faites pour le TTL : elle lit un 1 dès 2 V."),
        (S3_T[1] + 6.5, "2,4 V ≥ 2 V et 0,4 V ≤ 0,8 V : compatible. Il reste 0,4 V de réserve de chaque côté : c'est la marge de bruit."),
        (S3_T[2] + 1.5, "Cas 3 : 74HC vers 74HC, même famille. La sortie donne au moins 4,4 V, l'entrée demande 3,5 V."),
        (S3_T[2] + 6.5, "NH = 4,4 − 3,5 = 0,9 V et NL = 1,5 − 0,33 = 1,17 V : de belles réserves."),
        (S3_T[2] + 8.5, "Un parasite de 0,55 V sur le câble : le niveau reste au-dessus de 3,5 V. La marge de bruit l'absorbe, la porte lit toujours un 1."),
    ]))


# ================================================================ 4 · convertisseur de niveaux
def board(d, box, title, sub, col, alpha=1.0):
    x0, y0, x1, y1 = box
    rbox(d, box, fill=mix(WHITE, col, alpha), outline=mix(WHITE, NAVY, alpha), width=4, r=18)
    text(d, ((x0 + x1) / 2, y0 + 50), title, 34, mix(WHITE, WHITE, alpha), True, anchor="mm")
    text(d, ((x0 + x1) / 2, y0 + 95), sub, 26, mix(WHITE, (225, 232, 245), alpha), anchor="mm")


S4_P = [2.0, 15.0, 27.0]


def s_shifter(img, d, t):
    chrome(img, d, "4 · LE CONVERTISSEUR DE NIVEAUX", "Arduino 5 V et capteur 3,3 V", f"4/{TOT}")
    ref_pill(d, "présentation 100, diapo 12 · fiche 110 N°3")
    ph = 0
    for i, t0 in enumerate(S4_P):
        if t >= t0: ph = i
    a = prog(t, 0.3, 1.3)
    left_sub = ["Arduino Uno", "entrée 74HC", "Arduino Uno"][ph]
    board(d, (90, 300, 520, 620), "Côté 5 V", left_sub, (40, 110, 150), a)
    board(d, (1240, 300, 1670, 620), "Côté 3,3 V", "capteur de température", (60, 140, 90), a)
    yL = 520
    if ph < 2:
        # liaison directe
        dirn = 1 if ph == 0 else -1
        tp = t - S4_P[ph] if t >= S4_P[0] else 0
        d.line((520, yL, 1240, yL), fill=NAVY, width=6)
        if t >= S4_P[0]:
            pos = (tp * 0.25) % 1
            x = 520 + (720 * pos if dirn > 0 else 720 * (1 - pos))
            d.ellipse((x - 14, yL - 14, x + 14, yL + 14), fill=BLUE)
            arrow(d, (800, yL - 50) if dirn > 0 else (960, yL - 50), (960, yL - 50) if dirn > 0 else (800, yL - 50), BLUE, 5)
            label_box(d, (880, yL - 95), "1 = 5 V" if dirn > 0 else "1 = 3,3 V", 28, BLUE)
        if ph == 0 and t >= S4_P[0] + 3:
            bl = 0.5 + 0.5 * math.sin(t * 6)
            rbox(d, (1240 - 20, 280, 1670 + 20, 640), outline=mix(WHITE, RED, bl), width=8, r=24)
            q = prog(t, S4_P[0] + 3, S4_P[0] + 4)
            rbox(d, (600, 650, 1680, 860), fill=mix(WHITE, PINK, q), outline=mix(WHITE, RED, q), width=3, r=16)
            text(d, (630, 675), "Trop de tension pour l'entrée du capteur", 30, mix(WHITE, RED, q), True)
            para(d, (630, 725), "Son entrée supporte au plus environ 3,6 V (3,3 V + 0,3 V, valeur limite absolue). 5 V la dépasse : l'entrée peut être détruite.", 26, 1020, mix(WHITE, NAVY, q))
        if ph == 1 and t >= S4_P[1] + 3:
            q = prog(t, S4_P[1] + 3, S4_P[1] + 4)
            rbox(d, (90, 650, 1170, 860), fill=mix(WHITE, (255, 240, 220), q), outline=mix(WHITE, ORANGE, q), width=3, r=16)
            text(d, (120, 675), "Le 1 n'est pas garanti", 30, mix(WHITE, ORANGE, q), True)
            para(d, (120, 725), "Une entrée 74HC alimentée en 5 V exige 3,5 V pour un 1 (VIH). Le capteur n'envoie que 3,3 V : 3,3 V < 3,5 V.", 26, 1020, mix(WHITE, NAVY, q))
    else:
        q = prog(t, S4_P[2], S4_P[2] + 1.2)
        rbox(d, (700, 380, 1060, 600), fill=mix(WHITE, BLUE, q), outline=mix(WHITE, NAVY, q), width=4, r=18)
        text(d, (880, 430), "Convertisseur", 30, mix(WHITE, WHITE, q), True, anchor="mm")
        text(d, (880, 470), "de niveaux", 30, mix(WHITE, WHITE, q), True, anchor="mm")
        text(d, (880, 520), "5 V  ↔  3,3 V", 30, mix(WHITE, WHITE, q), True, anchor="mm")
        text(d, (880, 565), "« level shifter »", 22, mix(WHITE, (225, 232, 245), q), italic=True, anchor="mm")
        d.line((520, yL, 700, yL), fill=mix(WHITE, NAVY, q), width=6)
        d.line((1060, yL, 1240, yL), fill=mix(WHITE, NAVY, q), width=6)
        tp = t - S4_P[2]
        if tp > 1.5:
            pos = ((tp - 1.5) * 0.3) % 1
            fwd = int((tp - 1.5) * 0.3) % 2 == 0
            if fwd:
                x = 520 + 180 * min(pos * 2, 1) if pos < 0.5 else 1060 + 180 * (pos - 0.5) * 2
                lab = "5 V" if pos < 0.5 else "3,3 V"
            else:
                x = 1240 - 180 * min(pos * 2, 1) if pos < 0.5 else 700 - 180 * (pos - 0.5) * 2
                lab = "3,3 V" if pos < 0.5 else "5 V"
            d.ellipse((x - 14, yL - 14, x + 14, yL + 14), fill=GREEN)
            label_box(d, (x, yL + 50), lab, 24, GREEN)
        r = prog(t, S4_P[2] + 4, S4_P[2] + 5)
        rbox(d, (90, 670, 1680, 860), fill=mix(WHITE, LGREEN, r), outline=mix(WHITE, GREEN, r), width=3, r=16)
        check(d, (140, 720), True, 50, r)
        text(d, (185, 720), "Chaque côté reçoit ses propres niveaux.", 30, mix(WHITE, NAVY, r), True, anchor="lm")
        para(d, (185, 760), "Unidirectionnel : un seul sens (sortie 5 V → entrée 3,3 V). Bidirectionnel : les deux sens, par exemple pour un bus I²C.", 26, 1440, mix(WHITE, NAVY, r))
    caption(d, cap_at(t, [
        (0, "La question de départ de la présentation 100 : peut-on relier directement un Arduino 5 V à un capteur alimenté en 3,3 V ?"),
        (S4_P[0], "Premier sens : l'Arduino envoie un 1, donc environ 5 V, sur une entrée du capteur."),
        (S4_P[0] + 3.5, "5 V dépasse la tension maximale de l'entrée 3,3 V. Le capteur peut être détruit, parfois au premier essai."),
        (S4_P[1], "Autre sens : le capteur envoie un 1, soit 3,3 V, vers une entrée 74HC alimentée en 5 V."),
        (S4_P[1] + 3.5, "L'entrée 74HC exige 3,5 V. 3,3 V reste sous ce seuil : ce 1 n'est pas garanti (diapositive 17 de la présentation 100)."),
        (S4_P[2], "Solution : on intercale un convertisseur de niveaux. Il traduit 5 V en 3,3 V dans un sens, et 3,3 V en 5 V dans l'autre."),
        (S4_P[2] + 6, "Dans la vraie vie : des modules à quelques francs entre Arduino et capteurs, écrans ou cartes SD. Un Raspberry Pi n'accepte que 3,3 V."),
    ]))


# ================================================================ 5 · temps de propagation
TP = 12.0                      # ns par porte (M74HCT00, VCC = 4,5 V)
S5_T0, NS_PER_S = 9.0, 3.0     # le front d'entrée part à t = 9 s ; 1 s d'animation = 3 ns


def s_prop(img, d, t):
    chrome(img, d, "5 · LE TEMPS DE PROPAGATION", "Quatre portes NON-ET en série, au ralenti", f"5/{TOT}")
    ref_pill(d, "fiche M74HCT00 · Floyd 3-8 p. 152 · diapo 18")
    ns = (t - S5_T0) * NS_PER_S if t >= S5_T0 else -1.0
    A = 1 if ns >= 0 else 0
    # sortie de chaque porte : départ stable avec A = 0 → Y1 = 1, Y2 = 0, Y3 = 1, Y4 = 0
    Y = []
    for k in range(4):
        init = 1 if k % 2 == 0 else 0
        Y.append(init if ns < TP * (k + 1) else 1 - init)
    xs = [300, 660, 1020, 1380]
    s = 0.62
    vals = [A] + Y
    prev_out = (130, None)
    for k, x in enumerate(xs):
        y = 210
        ins, out = gate(d, x, y, "NON-ET", s, vin=(vals[k], vals[k]), vout=vals[k + 1], labels=("", ""), out_label="", lead=40)
        xm, ym = ins[0][0], (ins[0][1] + ins[1][1]) / 2
        wire(d, [(xm, ins[0][1]), (xm, ins[1][1])], vals[k], 4)          # entrées reliées
        wire(d, [(prev_out[0], ym), (xm, ym)], vals[k], 4)
        d.ellipse((xm - 6, ym - 6, xm + 6, ym + 6), fill=BLUE if vals[k] else NAVY)
        # étiquette et valeur du signal qui entre dans la porte
        lx = (prev_out[0] + xm) / 2
        text(d, (lx, ym - 38), "A" if k == 0 else f"Y{k}", 26, NAVY, True, italic=True, anchor="mm")
        bitpill(d, (lx, ym + 40), vals[k], 22)
        text(d, (x + 46, y + 150), f"porte {k + 1}", 22, GREY, True, anchor="mm")
        prev_out = out
    wire(d, [out, (out[0] + 60, out[1])], Y[3], 4)
    text(d, (out[0] + 30, out[1] - 38), "Y4", 26, NAVY, True, italic=True, anchor="mm")
    bitpill(d, (out[0] + 30, out[1] + 40), Y[3], 22)
    # horloge du ralenti
    display(d, (1440, 390, 1720, 480), "temps", ("0" if ns < 0 else f"{min(ns, 60):.0f}") + " ns", 42)
    # chronogramme
    gx0, gx1, gy0 = 260, 1380, 500
    pxns = (gx1 - gx0) / 60.0
    names = ["A", "Y1", "Y2", "Y3", "Y4"]
    for r, nm in enumerate(names):
        yb = gy0 + 70 + r * 56; yh = yb - 36
        text(d, (gx0 - 30, yb - 20), nm, 26, NAVY, True, italic=True, anchor="rm")
        d.line((gx0, yb, gx1, yb), fill=LGREY, width=1)
        init = 0 if r == 0 else (1 if (r - 1) % 2 == 0 else 0)
        tchg = 0.0 if r == 0 else TP * r
        shown = min(max(ns, -1), 60)
        x_ch = gx0 + tchg * pxns
        x_now = gx0 + max(shown, 0) * pxns
        lvl = lambda v: yh if v else yb
        pts = [(gx0 - 10, lvl(init))]
        if shown >= tchg:
            pts += [(x_ch, lvl(init)), (x_ch, lvl(1 - init)), (x_now, lvl(1 - init))]
        else:
            pts += [(max(x_now, gx0), lvl(init))]
        d.line(pts, fill=BLUE if r else NAVY, width=5, joint="curve")
    for k in range(1, 5):
        x = gx0 + TP * k * pxns
        if ns >= TP * k:
            for yy in range(gy0 + 20, gy0 + 300, 14): d.line((x, yy, x, yy + 6), fill=LGREY, width=2)
            text(d, (x, gy0 + 320), f"{TP * k:g} ns", 22, BLUE, True, anchor="mm")
    if ns >= 0:
        x = gx0 + min(ns, 60) * pxns
        d.line((x, gy0 + 15, x, gy0 + 300), fill=RED, width=2)
    T_END = S5_T0 + 60 / NS_PER_S
    q = prog(t, T_END - 4, T_END - 3)
    if q > 0:
        rbox(d, (1440, 520, 1720, 860), fill=mix(WHITE, TINT, q), r=16)
        text(d, (1580, 560), "Retard total", 24, mix(WHITE, GREY, q), True, anchor="mm")
        text(d, (1580, 620), "4 × 12 ns", 34, mix(WHITE, NAVY, q), True, anchor="mm")
        text(d, (1580, 675), "= 48 ns", 44, mix(WHITE, BLUE, q), True, anchor="mm")
        r = prog(t, T_END + 2, T_END + 3)
        text(d, (1580, 760), "10 portes :", 24, mix(WHITE, GREY, r), True, anchor="mm")
        text(d, (1580, 805), "120 ns", 36, mix(WHITE, NAVY, r), True, anchor="mm")
    caption(d, cap_at(t, [
        (0, "Une porte ne répond pas tout de suite. Pour le 74HCT00, la sortie change environ 12 ns après l'entrée (tPD typique)."),
        (4.5, "Ici, quatre portes NON-ET dont les deux entrées sont reliées : chacune inverse le signal. On ralentit le temps : 1 s = 3 ns."),
        (S5_T0, "L'entrée A passe à 1. La porte 1 ne réagit pas encore…"),
        (S5_T0 + 12 / NS_PER_S, "12 ns : Y1 change. Le front repart dans la porte 2, qui attend elle aussi 12 ns."),
        (S5_T0 + 36 / NS_PER_S, "Chaque porte ajoute son retard. Les retards s'additionnent le long de la chaîne."),
        (S5_T0 + 48 / NS_PER_S, "48 ns plus tard, Y4 change enfin : 4 × 12 ns = 48 ns entre A et Y4."),
        (T_END + 1, "Entre deux bouteilles, il s'écoule 100 ms, soit 100 000 000 ns. Ici, 48 ns ne gênent pas."),
        (T_END + 5, "Dix portes en série font 120 ns de retard. Dans un circuit rapide, ce retard limite la fréquence maximale."),
    ]))


# ================================================================ cartes et habillage
def ill_drawers(img, d, t):
    for r in range(3):
        for c in range(3):
            x, y = 110 + c * 210, 300 + r * 150
            rbox(d, (x, y, x + 190, y + 130), fill=(236, 239, 245), outline=NAVY, width=3, r=10)
            d.rounded_rectangle((x + 70, y + 92, x + 120, y + 110), radius=6, fill=NAVY)
            lab = ["SN74HCT00N", "SN74HC08N", "CD4011BE", "SN74HC04N", "SN74LS32D", "M74HCT00", "SN74HC02N", "CD4081BE", "SN74HC86N"][r * 3 + c]
            rbox(d, (x + 15, y + 20, x + 175, y + 60), fill=WHITE, outline=GREY, width=2, r=6)
            text(d, (x + 95, y + 40), lab, 20, NAVY if r * 3 + c else BLUE, True, mono=True, anchor="mm")
    hl = 0.5 + 0.5 * math.sin(t * 3)
    rbox(d, (100, 290, 310, 440), outline=mix(WHITE, BLUE, hl), width=6, r=14)


def ill_meter(img, d, t):
    rbox(d, (180, 300, 560, 760), fill=(250, 196, 40), outline=NAVY, width=4, r=30)
    v = [0.3, 3.6, 1.5][int(t / 3) % 3]
    display(d, (220, 340, 520, 470), "V DC", f"{v:.1f}".replace(".", ",") + " V", 54)
    d.ellipse((300, 520, 440, 660), fill=(60, 64, 80), outline=NAVY, width=4)
    d.line((370, 590, 410, 540), fill=WHITE, width=6)
    d.line((240, 760, 160, 860), fill=RED, width=6); d.line((500, 760, 600, 860), fill=NAVY, width=6)


def ill_cards(img, d, t):
    for i, (lab, col) in enumerate((("TTL", (120, 90, 60)), ("74HC", (40, 110, 150)))):
        x = 100 + i * 360
        rbox(d, (x, 400, x + 260, 620), fill=col, outline=NAVY, width=3, r=12)
        text(d, (x + 130, 450), "carte", 26, WHITE, anchor="mm")
        text(d, (x + 130, 500), lab, 40, WHITE, True, anchor="mm")
    pts = [(360 + i * 3, 560 + 18 * math.sin(i / 6 + t * 4) * math.sin(i / 25)) for i in range(34)]
    d.line(pts, fill=ORANGE, width=5)
    text(d, (410, 660), "câble de la machine", 24, GREY, italic=True, anchor="mm")


def ill_arduino(img, d, t):
    rbox(d, (90, 360, 420, 600), fill=(0, 120, 140), outline=NAVY, width=3, r=10)
    text(d, (255, 420), "Arduino", 34, WHITE, True, anchor="mm"); text(d, (255, 470), "5 V", 34, WHITE, True, anchor="mm")
    for i in range(10): d.rectangle((110 + i * 30, 372, 126 + i * 30, 392), fill=(30, 30, 30))
    rbox(d, (520, 420, 720, 560), fill=(60, 140, 90), outline=NAVY, width=3, r=10)
    text(d, (620, 470), "capteur", 26, WHITE, True, anchor="mm"); text(d, (620, 515), "3,3 V", 30, WHITE, True, anchor="mm")
    d.line((420, 500, 520, 490), fill=NAVY, width=5)
    q = 0.5 + 0.5 * math.sin(t * 4)
    text(d, (470, 440), "?", 60, mix(WHITE, RED, q), True, anchor="mm")


def ill_bottles(img, d, t):
    d.rectangle((80, 650, 740, 680), fill=LGREY, outline=NAVY, width=3)
    for i in range(5):
        x = 80 + ((t * 60 + i * 150) % 700)
        if x > 700: continue
        d.rectangle((x, 540, x + 50, 650), fill=WHITE, outline=NAVY, width=3)
        d.rectangle((x + 15, 515, x + 35, 540), fill=WHITE, outline=NAVY, width=3)
    gate(d, 300, 300, "NON-ET", 0.6, labels=("", ""), out_label="", lead=40)
    text(d, (400, 470), "tPD = 12 ns", 30, BLUE, True, anchor="mm")


CARDS = [
    ("1", TOT, "Lire une référence de CI", "SN74HCT00N, partie par partie", ill_drawers,
     "Au magasin de pièces de rechange, chaque tiroir porte la référence complète d'un CI.",
     "Que veut dire chaque partie de SN74HCT00N ? Peut-on prendre un autre CI à la place ?",
     "On découpe la référence : fabricant, plage, technologie, fonction, boîtier.", "SN · 74 · HCT · 00 · N"),
    ("2", TOT, "Les niveaux d'entrée", "Quand une tension devient un 0 ou un 1", ill_meter,
     "Le convoyeur s'arrête sans raison. Tu mesures au multimètre les entrées d'un 74HCT00.",
     "Quel état la porte lit-elle pour 0,3 V, 1,5 V ou 3,6 V ?",
     "On place chaque mesure sur l'échelle des niveaux de la fiche technique.", "VIL max = 0,8 V · VIH min = 2 V"),
    ("3", TOT, "Compatibilité et marge de bruit", "TTL, 74HC et 74HCT", ill_cards,
     "Une ancienne carte TTL doit piloter une carte récente en 74HC, par un câble de la machine.",
     "La carte récente lira-t-elle bien les 1 de l'ancienne ? Et si le câble capte des parasites ?",
     "On compare ce que la sortie garantit à ce que l'entrée exige.", "VOH ≥ VIH  et  VOL ≤ VIL"),
    ("4", TOT, "Le convertisseur de niveaux", "Arduino 5 V et capteur 3,3 V", ill_arduino,
     "Ton Arduino Uno travaille en 5 V. Ton capteur de température est alimenté en 3,3 V.",
     "Peux-tu relier directement leurs broches ? C'est la question de départ de la présentation 100.",
     "On regarde les deux sens de la liaison, puis on intercale un convertisseur.", "5 V  ↔  3,3 V"),
    ("5", TOT, "Le temps de propagation", "Quatre portes NON-ET en série", ill_bottles,
     "Le signal du capteur de bouteille traverse 4 portes NON-ET avant d'arriver à la vanne.",
     "Combien de temps lui faut-il ? La ligne remplit 10 bouteilles par seconde : est-ce un problème ?",
     "On suit le front du signal, porte après porte, au ralenti.", "tPD = 12 ns par porte"),
]
CARD_DUR = 13.0

s_intro = intro_scene("TEST ET MESURE 1 – EL DT 1 · ANIMATION 105", "Familles de circuits logiques",
                      "Pourquoi deux CI ne se comprennent pas toujours",
                      [("1", "Lire une référence de CI", "SN74HCT00N"), ("2", "Les niveaux d'entrée", "0, 1 ou zone interdite"),
                       ("3", "Compatibilité et marge de bruit", "TTL, 74HC, 74HCT"), ("4", "Le convertisseur de niveaux", "5 V et 3,3 V"),
                       ("5", "Le temps de propagation", "12 ns par porte")],
                      "Théorie : Floyd, chap. 3, 3-8 Logique à fonction fixe (p. 146-155) · nextecmedia 4.1")

s_outro = outro_scene(
    [("Référence", "fabricant, plage, technologie, fonction, boîtier"), ("Niveaux", "VIH et VIL de l'entrée : 0, 1 ou zone interdite"),
     ("Compatible", "VOH(sortie) ≥ VIH(entrée) et VOL(sortie) ≤ VIL(entrée)"), ("5 V ↔ 3,3 V", "un convertisseur de niveaux entre les deux"),
     ("Retard", "12 ns par porte, les retards s'additionnent")],
    "À toi de jouer",
    [("Fiche 110, N°1 et N°2", "lire une référence, choisir le bon CI", ""), ("Fiche 110, N°3", "les niveaux sont-ils compatibles ?", ""),
     ("Fiche 110, N°4", "lire la fiche technique du M74HCT00", ""), ("Fiche 110, N°5", "dépannage : mesurer les niveaux", ""),
     ("Floyd, chap. 3, 3-8", "Logique à fonction fixe", "p. 146-155"), ("Page interactive 101", "exercices sur des cas réels", "")],
    "Les liens du Floyd, de nextecmedia et de la présentation 100 sont dans la fiche 110.")

SCENES = [(s_intro, 9.0), (make_card(CARDS, 0, CARD_DUR), CARD_DUR), (s_ref, 42.0), (make_card(CARDS, 1, CARD_DUR), CARD_DUR), (s_levels, 45.0),
          (make_card(CARDS, 2, CARD_DUR), CARD_DUR), (s_compat, 48.0), (make_card(CARDS, 3, CARD_DUR), CARD_DUR), (s_shifter, 40.0),
          (make_card(CARDS, 4, CARD_DUR), CARD_DUR), (s_prop, 40.0), (s_outro, 15.0)]

def produire(ctx):
    render(SCENES, ctx.sortie_de("105"))


if __name__ == "__main__":
    # aperçu d'une image : python3 contenus/tm1/semaine-1/105-anim.py <scène> <t> [image.png]
    i, t = int(sys.argv[1]), float(sys.argv[2])
    frame_at(SCENES, i, t).save(sys.argv[3] if len(sys.argv) > 3 else f"apercu_105.png")
