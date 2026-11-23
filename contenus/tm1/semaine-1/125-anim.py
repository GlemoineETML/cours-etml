# -*- coding: utf-8 -*-
"""125 Portes logiques et tables de vérité – animation (TM1 – El DT 1, semaine 1, va avec la présentation 120 et la fiche 130 EX).
Tables de vérité : entrées du poids fort au poids faible (C B A, B A), puis la sortie. Symboles CEI 60617-12.
Données : moteur/logique.py (GATES, tdv, CHRONO_A/B). Rendu : python3 build.py tm1/semaine-1 --seulement animations · aperçu : voir en bas"""
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))   # aperçu direct
from moteur.anim import *
from moteur import logique as D

FOOT[0] = "Test et Mesure 1 – El DT 1 · 125 Portes logiques et tables de vérité · Floyd chap. 3"
TOT = "5"


def over_eq(d, x, y, parts, size, color=NAVY, anchor_mid=False):
    """Équation en notation Floyd : parts = [(texte, surligné ?)]. Renvoie la largeur."""
    f = F(size, True, italic=False)
    total = sum(f.getlength(p) for p, _ in parts)
    if anchor_mid: x -= total / 2
    for p, ov in parts:
        w = f.getlength(p)
        text(d, (x, y), p, size, color, True, anchor="lm")
        if ov:
            d.line((x + 2, y - size * 0.62, x + w - 2, y - size * 0.62), fill=color, width=max(3, size // 14))
        x += w
    return total


EQ = {"NON": [("Y = ", False), ("A", True)], "ET": [("Y = A · B", False)], "OU": [("Y = A + B", False)],
      "NON-ET": [("Y = ", False), ("A · B", True)], "NON-OU": [("Y = ", False), ("A + B", True)],
      "OUX": [("Y = A ⊕ B", False)], "NON-OUX": [("Y = ", False), ("A ⊕ B", True)]}


def table(d, x, y, heads, rows, colw=90, rowh=60, hl=None, size=30, alpha=1.0, outcols=1, show=None):
    """Table de vérité. rows = listes de valeurs (str ou None = vide). hl = indice de ligne surlignée.
    show = nombre de lignes affichées. Les dernières colonnes (outcols) sont les sorties."""
    n = len(heads)
    W_ = colw * n
    rbox(d, (x, y, x + W_, y + rowh), fill=mix(WHITE, LBLUE, alpha), r=8)
    for j, h in enumerate(heads):
        text(d, (x + colw * j + colw / 2, y + rowh / 2), h, size, mix(WHITE, NAVY, alpha), True, anchor="mm")
    d.line((x + colw * (n - outcols), y + 6, x + colw * (n - outcols), y + rowh * (len(rows) + 1) - 6), fill=mix(WHITE, NAVY, alpha), width=3)
    for i, r in enumerate(rows[: (len(rows) if show is None else show)]):
        yy = y + rowh * (i + 1)
        fill = TINT if hl == i else (PALE if i % 2 == 0 else WHITE)
        d.rectangle((x, yy, x + W_, yy + rowh), fill=mix(WHITE, fill, alpha))
        if hl == i: d.rectangle((x, yy, x + W_, yy + rowh), outline=mix(WHITE, BLUE, alpha), width=4)
        for j, v in enumerate(r):
            if v is None: continue
            out = j >= n - outcols
            col = (BLUE if str(v) == "1" else NAVY) if out else NAVY
            text(d, (x + colw * j + colw / 2, yy + rowh / 2), str(v), size, mix(WHITE, col, alpha), out, mono=True, anchor="mm")
    d.rectangle((x, y, x + W_, y + rowh * (len(rows) + 1)), outline=mix(WHITE, NAVY, alpha), width=3)


# ================================================================ 1 · la ligne de remplissage
def bottle_x(t, arrive, leave, start_t, x0=120, xn=615, speed=75):
    """Position (gauche) d'une bouteille : arrive sous le bec à « arrive », repart à « leave »."""
    if t < start_t: return None
    if t < arrive: return xn - (arrive - t) * speed
    if t < leave: return xn
    return xn + (t - leave) * speed


B1 = (8.0, 15.5, 1.0)        # arrivée, départ, apparition
B2 = (23.5, 39.5, 16.5)


def line_state(t):
    xb = [bottle_x(t, *B1), bottle_x(t, *B2)]
    b = int(any(x is not None and abs(x - 615) < 2 for x in xb))
    # niveau de la cuve (0..1), seuil du capteur N à 0,35
    if t < 8.5: lev = 0.62
    elif t < 15.0: lev = 0.62 - (t - 8.5) / 6.5 * 0.2
    elif t < 19.5: lev = 0.42 - (t - 15.0) / 4.5 * 0.14
    elif t < 31.0: lev = 0.28
    elif t < 34.0: lev = 0.28 + (t - 31.0) / 3.0 * 0.4
    elif t < 39.0: lev = 0.68 - (t - 34.0) / 5.0 * 0.15
    else: lev = 0.53
    n = int(lev >= 0.35)
    return xb, b, n, b & n, lev


def s_line(img, d, t):
    chrome(img, d, "1 · DES 0 ET DES 1", "La ligne de remplissage de boissons", f"1/{TOT}")
    ref_pill(d, "présentation 120, diapo 2 · Floyd 1-2 p. 5")
    xb, B, N, V, lev = line_state(t)
    # cuve
    tx0, ty0, tx1, ty1 = 520, 175, 760, 345
    d.rectangle((tx0, ty0, tx1, ty1), outline=NAVY, width=4, fill=WHITE)
    ly = ty1 - (ty1 - ty0) * lev
    d.rectangle((tx0 + 4, ly, tx1 - 4, ty1 - 4), fill=LBLUE)
    ys = ty1 - (ty1 - ty0) * 0.35
    d.rectangle((tx1, ys - 14, tx1 + 30, ys + 14), fill=NAVY)
    text(d, (tx1 + 44, ys), "N", 30, NAVY, True, anchor="lm")
    bitpill(d, (tx1 + 100, ys), N, 22)
    text(d, (640, ty0 - 20), "cuve", 24, GREY, True, anchor="mm")
    # tuyau + vanne
    d.rectangle((632, ty1, 648, 470), fill=LGREY, outline=NAVY, width=2)
    vx, vy = 640, 405
    col = BLUE if V else WHITE
    d.polygon([(vx - 30, vy - 20), (vx - 30, vy + 20), (vx, vy)], fill=col, outline=NAVY)
    d.polygon([(vx + 30, vy - 20), (vx + 30, vy + 20), (vx, vy)], fill=col, outline=NAVY)
    d.line((vx - 30, vy - 20, vx - 30, vy + 20), fill=NAVY, width=3); d.line((vx + 30, vy - 20, vx + 30, vy + 20), fill=NAVY, width=3)
    d.line((vx - 30, vy - 20, vx + 30, vy + 20), fill=NAVY, width=3); d.line((vx - 30, vy + 20, vx + 30, vy - 20), fill=NAVY, width=3)
    text(d, (vx - 50, vy), "V", 30, NAVY, True, anchor="rm")
    bitpill(d, (vx - 110, vy), V, 22)
    d.polygon([(626, 470), (654, 470), (646, 492), (634, 492)], fill=NAVY)
    if V:
        for k in range(6):
            yy = 500 + ((t * 220 + k * 25) % 120)
            d.ellipse((636, yy, 644, yy + 12), fill=BLUE)
    # convoyeur
    d.rounded_rectangle((90, 650, 1180, 690), radius=20, fill=LGREY, outline=NAVY, width=3)
    for k in range(12):
        cx = 110 + k * 95
        d.ellipse((cx - 12, 658, cx + 12, 682), outline=GREY, width=2)
    # capteur de bouteille (barrière lumineuse)
    d.rectangle((540, 560, 560, 620), fill=NAVY); d.rectangle((720, 560, 740, 620), fill=NAVY)
    d.line((560, 590, 720, 590), fill=RED if B else (255, 190, 190), width=3)
    text(d, (520, 590), "B", 30, NAVY, True, anchor="rm")
    bitpill(d, (470, 590), B, 22)
    # bouteilles
    fills = []
    for i, x in enumerate(xb):
        if x is None or x > 1130: continue
        arr, lea = (B1, B2)[i][:2]
        # niveau de la bouteille
        tt = [t for t in (t,)][0]
        f = 0.0
        if i == 0: f = clamp((min(tt, 14.0) - 8.6) / 5.4)
        else: f = clamp((min(tt, 37.5) - 31.6) / 5.9)
        d.rectangle((x, 525, x + 50, 650), fill=WHITE, outline=NAVY, width=3)
        d.rectangle((x + 15, 500, x + 35, 525), fill=WHITE, outline=NAVY, width=3)
        if f > 0: d.rectangle((x + 4, 646 - 117 * f, x + 46, 646), fill=(250, 170, 60))
    # voyant « cuve vide »
    lamp(d, (1060, 250), N == 0, 34, None, ORANGE)
    text(d, (1060, 310), "voyant", 22, NAVY, True, anchor="mm"); text(d, (1060, 336), "« cuve vide »", 22, NAVY, True, anchor="mm")
    text(d, (1060, 368), "= N̄", 24, GREY, True, anchor="mm")
    # panneau de droite
    X = 1230
    rbox(d, (X, 180, 1720, 520), fill=PALE, outline=NAVY, width=3, r=16)
    text(d, (X + 25, 200), "Variables binaires", 26, BLUE, True)
    rows = [("B", "bouteille sous le bec", B), ("N", "niveau de la cuve suffisant", N), ("V", "vanne de remplissage", V)]
    for i, (nm, lab, v) in enumerate(rows):
        y = 270 + i * 72
        text(d, (X + 30, y), nm, 34, NAVY, True, italic=True, anchor="lm")
        text(d, (X + 80, y), lab, 24, NAVY, anchor="lm")
        bitpill(d, (X + 440, y), v, 26)
    text(d, (X + 25, 480), "1 = vrai, actif · 0 = faux, inactif", 22, GREY, italic=True, anchor="lm")
    q = prog(t, 39.0, 40.0)
    rbox(d, (X, 550, 1720, 880), fill=mix(WHITE, TINT, max(q, 0.35)), r=16)
    ins, out = gate(d, X + 150, 600, "ET", 1.0, vin=(B, N), vout=V, labels=("B", "N"), out_label="V", lead=80)
    q2 = prog(t, 39.5, 40.5)
    if q2 > 0: over_eq(d, X + 245, 840, [("V = B · N", False)], 40, mix(TINT, NAVY, q2), anchor_mid=True)
    caption(d, cap_at(t, [
        (0, "Sur une ligne de remplissage, chaque capteur répond par oui ou par non. C'est une variable binaire : 1 ou 0."),
        (4.0, "B = 1 quand une bouteille coupe la barrière lumineuse sous le bec. N = 1 quand la cuve contient assez de liquide."),
        (8.0, "Bouteille sous le bec (B = 1) et cuve assez pleine (N = 1) : la vanne s'ouvre, V = 1."),
        (15.5, "La bouteille pleine repart : B = 0, la vanne se ferme."),
        (19.5, "Pendant ce temps, le niveau de la cuve est passé sous le capteur : N = 0. Le voyant « cuve vide » s'allume."),
        (23.5, "Une bouteille arrive : B = 1, mais N = 0. La vanne reste fermée : pas de remplissage avec une cuve vide."),
        (31.0, "On remplit la cuve. Dès que N = 1, les deux conditions sont vraies et la vanne s'ouvre."),
        (39.5, "La vanne s'ouvre seulement si B ET N valent 1 : c'est une porte ET. En équation : V = B · N."),
    ]))


# ================================================================ 2 · construire une table de vérité
S2_R0, S2_DR = 9.0, 2.0
S2_COL = 25.0
S2_EX = 34.0


def s_table(img, d, t):
    chrome(img, d, "2 · CONSTRUIRE UNE TABLE DE VÉRITÉ", "Toutes les combinaisons, dans l'ordre", f"2/{TOT}")
    ref_pill(d, "présentation 120, diapo 3 · Floyd 3-2")
    steps = ["Une colonne par entrée, du poids fort au poids faible, puis la sortie.",
             "n entrées → 2ⁿ lignes. 3 entrées → 8 lignes.",
             "On compte en binaire, de 000 à 111 : on n'oublie aucune ligne.",
             "Pour chaque ligne, on lit le cahier des charges et on écrit la sortie."]
    for i, s in enumerate(steps):
        q = prog(t, 1.0 + i * 2.0, 2.0 + i * 2.0)
        if q <= 0: continue
        y = 200 + i * 135
        d.ellipse((60, y, 110, y + 50), fill=mix(WHITE, NAVY, q))
        text(d, (85, y + 25), str(i + 1), 26, WHITE, True, anchor="mm")
        para(d, (130, y + 4), s, 27, 440, mix(WHITE, NAVY, q))
    ex = t >= S2_EX
    heads = ["E", "L", "U", "M"] if ex else ["C", "B", "A", "Y"]
    show = clamp(int((t - S2_R0) / S2_DR) + 1, 0, 8) if t >= S2_R0 else 0
    rows = []
    for v in range(8):
        c, b, a = (v >> 2) & 1, (v >> 1) & 1, v & 1
        m = None
        if ex:
            k = int((t - S2_EX - 2.0) / 1.2) + 1 if t >= S2_EX + 2.0 else 0
            m = (c & b & (1 - a)) if v < k else None
        rows.append([c, b, a, m if ex else "?"])
    tx, ty = 690, 200
    hl = None
    if S2_R0 <= t < S2_COL: hl = show - 1
    if ex and t >= S2_EX + 2.0:
        k = int((t - S2_EX - 2.0) / 1.2)
        hl = 6 if k >= 8 else min(k, 7)
    # bandeaux de colonne (fréquence de basculement)
    if S2_COL <= t < S2_EX:
        j = 2 if t < S2_COL + 3 else (1 if t < S2_COL + 6 else 0)
        d.rectangle((tx + 100 + j * 90, ty + 60, tx + 100 + (j + 1) * 90, ty + 60 * 9), fill=(255, 236, 214))
    for i in range(show):
        text(d, (tx + 50, ty + 60 * (i + 1) + 30), f"{i}", 24, GREY, True, anchor="mm")
    text(d, (tx + 50, ty + 30), "déc.", 20, GREY, True, anchor="mm")
    table(d, tx + 100, ty, heads, rows, 90, 60, hl, 30, show=show)
    if S2_COL <= t < S2_EX:
        j = 2 if t < S2_COL + 3 else (1 if t < S2_COL + 6 else 0)
        lab = ["change toutes les 4 lignes", "change toutes les 2 lignes", "change à chaque ligne"][j]
        label_box(d, (tx + 145 + j * 90, ty + 60 * 9 + 34), lab, 22, ORANGE)
    text(d, (tx + 100 + 135, ty + 60 * 9 + 80), ("poids fort  →  poids faible" if not ex else "E poids fort … U poids faible"), 22, GREY, italic=True, anchor="mm")
    # cahier des charges (exemple)
    q = prog(t, S2_EX, S2_EX + 1.0)
    if q > 0:
        X = 1150
        rbox(d, (X, 200, 1720, 560), fill=mix(WHITE, PALE, q), outline=mix(WHITE, NAVY, q), width=3, r=16)
        text(d, (X + 25, 222), "Cahier des charges (fiche 130 EX, N°1)", 24, mix(WHITE, BLUE, q), True)
        para(d, (X + 25, 270), "Le moteur M du convoyeur tourne si une bouteille attend (E = 1) et si la zone de remplissage est libre (L = 1). Jamais si l'arrêt d'urgence est actionné (U = 1).", 25, 520, mix(WHITE, NAVY, q))
        r = prog(t, S2_EX + 12.0, S2_EX + 13.0)
        if r > 0:
            rbox(d, (X, 600, 1720, 760), fill=mix(WHITE, TINT, r), r=16)
            over_eq(d, X + 285, 680, [("M = E · L · ", False), ("U", True)], 46, mix(WHITE, NAVY, r), anchor_mid=True)
    seq = [(0, "Une table de vérité donne la sortie pour toutes les combinaisons des entrées. Voici la méthode, en quatre règles."),
           (S2_R0, "Trois entrées C, B, A : C est le poids fort, A le poids faible. On écrit les lignes en comptant en binaire."),
           (S2_R0 + 4 * S2_DR, "Ligne 4 : 100. On compte comme en numération : la colonne de gauche vaut 4, celle du milieu 2, celle de droite 1."),
           (S2_COL, "Vérification rapide : A, le poids faible, change à chaque ligne…"),
           (S2_COL + 3, "… B change toutes les deux lignes…"),
           (S2_COL + 6, "… et C, le poids fort, toutes les quatre lignes. Si ce rythme est respecté, aucune ligne ne manque."),
           (S2_EX, "Exemple : le moteur du convoyeur. Mêmes colonnes, avec E en poids fort et U en poids faible."),
           (S2_EX + 2.0, "Pour chaque ligne, on se demande : le cahier des charges autorise-t-il le moteur ?"),
           (S2_EX + 11.6, "Une seule ligne donne M = 1 : E = 1, L = 1 et U = 0. D'où l'équation M = E · L · Ū.")]
    caption(d, cap_at(t, seq))


# ================================================================ 3 · lire un chronogramme
CA, CB = D.CHRONO_A, D.CHRONO_B
S3_T0, S3_DT = 7.0, 4.0


def s_chrono(img, d, t):
    chrome(img, d, "3 · LIRE UN CHRONOGRAMME", "Chaque intervalle correspond à une ligne de la table", f"3/{TOT}")
    ref_pill(d, "présentation 120, diapo 4 · Floyd 1-2 p. 9")
    k = int((t - S3_T0) / S3_DT) if t >= S3_T0 else -1
    k = min(k, 7)
    Yv = D.chrono("ET")
    x0, pw = 160, 120
    rowsy = {"A": 300, "B": 450, "Y": 620}
    for i in range(8):
        text(d, (x0 + i * pw + pw / 2, 205), str(i + 1), 26, GREY, True, anchor="mm")
    if k >= 0:
        xa = x0 + k * pw
        rbox(d, (xa + 4, 225, xa + pw - 4, 700), fill=TINT, outline=BLUE, width=3, r=10)
    for nm, sig in (("A", CA), ("B", CB), ("Y", Yv)):
        yb = rowsy[nm]; yh = yb - 80
        text(d, (x0 - 40, yb - 40), nm, 34, NAVY, True, italic=True, anchor="mm")
        d.line((x0, yb, x0 + 8 * pw, yb), fill=LGREY, width=2)
        n = 8 if nm != "Y" else (k + 1 if k >= 0 else 0)
        if nm == "Y" and k >= 0:
            # le segment en cours se dessine
            n = k + prog(t, S3_T0 + k * S3_DT + 1.5, S3_T0 + k * S3_DT + 2.5)
        pts = []
        full = int(n); frac = n - full
        for i in range(full):
            yy = yh if sig[i] else yb
            pts += [(x0 + i * pw, yy), (x0 + (i + 1) * pw, yy)]
        if full < 8 and frac > 0:
            yy = yh if sig[full] else yb
            pts += [(x0 + full * pw, yy), (x0 + full * pw + pw * frac, yy)]
        if len(pts) > 1: d.line(pts, fill=BLUE if nm == "Y" else NAVY, width=6, joint="curve")
        for i in range(8 if nm != "Y" else full):
            text(d, (x0 + i * pw + pw / 2, yb + 22), str(sig[i]), 20, GREY, anchor="mm")
    # table B A Y de la porte ET
    tdv = D.tdv("ET")
    hl = None; vis = set()
    for i in range(k + 1):
        r = [j for j, (b, a, y) in enumerate(tdv) if b == CB[i] and a == CA[i]][0]
        vis.add(r)
        if i == k: hl = r
    rows = [[b, a, (y if j in vis else None)] for j, (b, a, y) in enumerate(tdv)]
    X = 1220
    text(d, (X, 200), "Table de vérité de la porte ET", 26, BLUE, True)
    table(d, X + 40, 250, ["B", "A", "Y"], rows, 110, 68, hl, 32)
    gate(d, X + 110, 640, "ET", 0.75, vin=(CA[k], CB[k]) if k >= 0 else None, vout=Yv[k] if k >= 0 else None, lead=60)
    seq = [(0, "L'analyseur logique montre les signaux dans le temps. Le temps avance de gauche à droite, une ligne par variable."),
           (3.5, "On découpe le temps en intervalles où rien ne change. Dans chaque intervalle, on lit A et B, puis on cherche la ligne de la table.")]
    for i in range(8):
        txt = f"Intervalle {i + 1} : A = {CA[i]}, B = {CB[i]}. Dans la table, c'est la ligne B A = {CB[i]}{CA[i]}, donc Y = {Yv[i]}."
        if i == 4: txt = f"Intervalle 5 : A = {CA[i]}, B = {CB[i]}, la même combinaison qu'à l'intervalle 2. Même ligne de la table, même Y = {Yv[i]}."
        seq.append((S3_T0 + i * S3_DT, txt))
    seq.append((S3_T0 + 8 * S3_DT, "Un chronogramme parcourt la table de vérité dans l'ordre où les combinaisons arrivent. Ici, Y = 1 seulement quand A = B = 1."))
    caption(d, cap_at(t, seq))


# ================================================================ 4 · les sept portes
S4_T0, S4_DG = 3.0, 10.0
ORDER = D.ORDER


def s_gates(img, d, t):
    chrome(img, d, "4 · LES SEPT PORTES DE BASE", "Symbole CEI, table de vérité, équation", f"4/{TOT}")
    ref_pill(d, "présentation 120, diapo 5 à 12 · Floyd 3-1 à 3-6")
    j = clamp(int((t - S4_T0) / S4_DG), 0, 6) if t >= S4_T0 else 0
    key = ORDER[j]; g = D.GATES[key]; n = g[4]
    tg = t - (S4_T0 + j * S4_DG)
    # bandeau des sept portes
    for i, k in enumerate(ORDER):
        x = 60 + i * 238
        cur = i == j
        rbox(d, (x, 150, x + 225, 195), fill=BLUE if cur else (TINT if i < j else PALE), outline=NAVY if cur else None, width=2, r=10)
        text(d, (x + 112, 172), D.GATES[k][0], 21, WHITE if cur else NAVY, True, anchor="mm")
    tdv = D.tdv(key)
    nrow = len(tdv)
    dt = 7.2 / nrow
    r = int((tg - 1.2) / dt) if tg >= 1.2 else -1
    r = min(r, nrow - 1)
    vin = vout = None
    if r >= 0:
        row = tdv[r]
        if n == 1: vin, vout = (row[0],), row[1]
        else: vin, vout = (row[1], row[0]), row[2]        # (A, B)
    a = prog(tg, 0.0, 0.8) if t >= S4_T0 else prog(t, 0.3, 1.2)
    ins, out = gate(d, 330, 330 if n == 2 else 350, key, 1.45, vin=vin, vout=vout, alpha=a, lead=95)
    # interrupteurs d'entrée et lampe
    names = ["A"] if n == 1 else ["A", "B"]
    for i, p in enumerate(ins):
        v = vin[i] if vin else 0
        bitpill(d, (p[0] - 100, p[1]), v, 30, a)
    lamp(d, (out[0] + 110, out[1]), bool(vout) if vout is not None else False, 36, None, BLUE)
    text(d, (440, 760), f"Porte {g[0]} ({g[1]})", 40, mix(WHITE, NAVY, a), True, anchor="mm")
    # table B A Y
    X = 1120
    heads = ["A", "Y"] if n == 1 else ["B", "A", "Y"]
    rows = []
    for i, row in enumerate(tdv):
        vals = list(row)
        if i > r: vals[-1] = None
        rows.append(vals)
    table(d, X, 230, heads, rows, 110, 66, r if r >= 0 else None, 32, alpha=a)
    q = prog(tg, 1.2 + 7.2, 1.2 + 7.8)
    y0 = 230 + 66 * (nrow + 1) + 30
    rbox(d, (X - 20, y0, 1720, y0 + (230 if n == 2 else 300)), fill=mix(WHITE, TINT, q), r=14)
    over_eq(d, X + 10, y0 + 50, EQ[key], 40, mix(WHITE, NAVY, q))
    para(d, (X + 10, y0 + 95), g[8], 24, 560, mix(WHITE, NAVY, q))
    text(d, (X + 10, y0 + (190 if n == 2 else 170)), f"CI : {g[9]} ({g[11]})", 22, mix(WHITE, GREY, q), True)
    seq = [(0, "Sept portes de base. Pour chacune, on fait passer les combinaisons d'entrée, du poids fort au poids faible, et on lit la sortie Y.")]
    expl = {"NON": "NON (inverseur) : une seule entrée. La sortie est l'inverse de l'entrée. Le cercle sur la sortie signale cette inversion.",
            "ET": "ET : Y = 1 seulement si A et B valent 1. Le qualificatif & est dans le rectangle.",
            "OU": "OU : Y = 1 dès qu'une entrée vaut 1, ou les deux. Qualificatif ≥1 : au moins une entrée à 1.",
            "NON-ET": "NON-ET : le symbole du ET avec un cercle de négation. Y = 0 seulement si A = B = 1.",
            "NON-OU": "NON-OU : le symbole du OU avec un cercle. Y = 1 seulement si A = B = 0.",
            "OUX": "OU exclusif : Y = 1 quand les entrées sont différentes. Qualificatif =1 : exactement une entrée à 1.",
            "NON-OUX": "NON-OU exclusif : Y = 1 quand les deux entrées sont égales. C'est un détecteur d'égalité."}
    for i, k in enumerate(ORDER):
        seq.append((S4_T0 + i * S4_DG + 0.2, expl[k]))
    caption(d, cap_at(t, seq))


# ================================================================ 5 · du symbole au circuit intégré
PL = ["1A", "1B", "1Y", "2A", "2B", "2Y", "GND"]          # broches 1 à 7, à gauche
PR = ["VCC", "4B", "4A", "4Y", "3B", "3A", "3Y"]          # broches 14 à 8, à droite
S5 = {"B": 4.0, "N": 8.0, "V": 12.0, "VCC": 16.0, "GND": 19.5, "NC": 23.5, "DEMO": 28.0}


def s_ic(img, d, t):
    chrome(img, d, "5 · DU SYMBOLE AU CIRCUIT INTÉGRÉ", "Câbler la vanne V = B · N sur un 74HC08", f"5/{TOT}")
    ref_pill(d, "présentation 120, diapo 13 · fiche 130 EX N°4 · Floyd 3-8 p. 146")
    bx0, by0, bx1, by1 = 760, 190, 1060, 820
    pitch = (by1 - by0 - 60) / 6
    py = lambda i: by0 + 30 + i * pitch
    a = prog(t, 0.3, 1.3)
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=12, fill=mix(WHITE, (52, 56, 70), a), outline=mix(WHITE, NAVY, a), width=3)
    d.pieslice(((bx0 + bx1) / 2 - 30, by0 - 30, (bx0 + bx1) / 2 + 30, by0 + 30), 0, 180, fill=mix(WHITE, (30, 32, 44), a))
    text(d, ((bx0 + bx1) / 2, (py(2) + py(3)) / 2), "74HC08", 44, mix(WHITE, (235, 238, 245), a), True, mono=True, anchor="mm")
    text(d, ((bx0 + bx1) / 2, (py(3) + py(4)) / 2), "4 portes ET", 24, mix(WHITE, (200, 205, 220), a), anchor="mm")
    for i in range(7):
        y = py(i)
        d.rectangle((bx0 - 40, y - 14, bx0, y + 14), fill=mix(WHITE, LGREY, a), outline=mix(WHITE, NAVY, a), width=2)
        d.rectangle((bx1, y - 14, bx1 + 40, y + 14), fill=mix(WHITE, LGREY, a), outline=mix(WHITE, NAVY, a), width=2)
        text(d, (bx0 + 12, y), str(i + 1), 18, mix(WHITE, (170, 176, 192), a), True, anchor="lm")
        text(d, (bx1 - 12, y), str(14 - i), 18, mix(WHITE, (170, 176, 192), a), True, anchor="rm")
        text(d, (bx0 + 46, y), PL[i], 24, mix(WHITE, (235, 238, 245), a), True, anchor="lm")
        text(d, (bx1 - 46, y), PR[i], 24, mix(WHITE, (235, 238, 245), a), True, anchor="rm")
    # démonstration : B et N basculent
    demo = [(0, 0), (1, 0), (0, 1), (1, 1)]
    if t >= S5["DEMO"]:
        k = min(int((t - S5["DEMO"]) / 2.0), 3)
        Bv, Nv = demo[k]
    else:
        Bv, Nv = 1, 1
    Vv = Bv & Nv
    # sources à gauche
    def src(y, lab, sub, v):
        rbox(d, (90, y - 36, 330, y + 36), fill=TINT, outline=NAVY, width=2, r=10)
        text(d, (110, y - 8), lab, 28, NAVY, True, italic=True, anchor="lm")
        text(d, (110, y + 18), sub, 18, GREY, anchor="lm")
        bitpill(d, (300, y), v, 22)
    yB, yN, yV = py(0), py(1), py(2)
    q = prog(t, S5["B"] - 1, S5["B"])
    if q > 0:
        src(yB - 40, "B", "capteur bouteille", Bv)
        wire(d, [(330, yB - 40), (560, yB - 40), (560, yB), (bx0 - 40, yB)][: 2 + int(q * 2)], Bv, 4)
    q = prog(t, S5["N"] - 1, S5["N"])
    if q > 0:
        src(yN + 40, "N", "capteur niveau", Nv)
        wire(d, [(330, yN + 40), (600, yN + 40), (600, yN), (bx0 - 40, yN)][: 2 + int(q * 2)], Nv, 4)
    q = prog(t, S5["V"] - 1, S5["V"])
    if q > 0:
        wire(d, [(bx0 - 40, yV), (640, yV), (640, yV + 150), (330, yV + 150)][: 2 + int(q * 2)], Vv, 4)
        rbox(d, (90, yV + 114, 330, yV + 186), fill=mix(WHITE, BLUE, 0.15 if Vv else 0), outline=NAVY, width=2, r=10)
        text(d, (110, yV + 142), "V", 28, NAVY, True, italic=True, anchor="lm")
        text(d, (110, yV + 168), "vanne", 18, GREY, anchor="lm")
        lamp(d, (295, yV + 150), bool(Vv), 20, None, BLUE)
    # alimentation
    q = prog(t, S5["VCC"] - 1, S5["VCC"])
    if q > 0:
        y = py(0)
        d.line((bx1 + 40, y, bx1 + 140 * q + 40, y), fill=RED, width=5)
        if q >= 1: text(d, (bx1 + 190, y), "+5 V", 30, RED, True, anchor="lm")
    q = prog(t, S5["GND"] - 1, S5["GND"])
    if q > 0:
        y = py(6)
        d.line((bx0 - 40, y, bx0 - 40 - 80 * q, y), fill=NAVY, width=5)
        if q >= 1:
            gx = bx0 - 120
            d.line((gx, y, gx, y + 30), fill=NAVY, width=5)
            for k_, w in enumerate((30, 20, 10)): d.line((gx - w, y + 30 + k_ * 9, gx + w, y + 30 + k_ * 9), fill=NAVY, width=4)
    # entrées inutilisées à GND
    q = prog(t, S5["NC"] - 1, S5["NC"])
    if q > 0:
        for side, idx in (("L", 3), ("L", 4), ("R", 1), ("R", 2), ("R", 4), ("R", 5)):
            y = py(idx)
            x = bx0 - 40 if side == "L" else bx1 + 40
            dx = -1 if side == "L" else 1
            x2 = x + dx * (60 if side == "L" else 110)
            d.line((x, y, x2, y), fill=mix(WHITE, GREEN, q), width=4)
            d.line((x2, y - 12, x2, y + 12), fill=mix(WHITE, GREEN, q), width=4)
        label_box(d, (1400, py(3) - 10), "entrées inutilisées → GND", 22, GREEN, alpha=q)
    # symbole équivalent
    q = prog(t, S5["DEMO"] - 1, S5["DEMO"])
    if q > 0:
        rbox(d, (1300, 600, 1720, 880), fill=mix(WHITE, TINT, q), r=16)
        gate(d, 1430, 640, "ET", 0.8, vin=(Bv, Nv), vout=Vv, labels=("B", "N"), out_label="V", alpha=q, lead=60)
    caption(d, cap_at(t, [
        (0, "Le 74HC08 contient 4 portes ET à 2 entrées. On repère la broche 1 grâce à l'encoche, puis on compte dans le sens inverse des aiguilles d'une montre."),
        (S5["B"] - 1, "Porte 1 : le capteur de bouteille B arrive sur la broche 1 (entrée 1A)."),
        (S5["N"] - 1, "Le capteur de niveau N arrive sur la broche 2 (entrée 1B)."),
        (S5["V"] - 1, "La sortie 1Y, broche 3, commande la vanne V (en pratique à travers un transistor)."),
        (S5["VCC"] - 1, "Sans alimentation, rien ne marche : broche 14 au +5 V…"),
        (S5["GND"] - 1, "… et broche 7 à la masse (GND). Inverser les deux détruit le CI en quelques secondes."),
        (S5["NC"] - 1, "Les entrées des portes 2, 3 et 4 ne servent pas : on les relie à GND. Une entrée CMOS ne reste jamais en l'air."),
        (S5["DEMO"], "Essai : la vanne ne s'ouvre que quand B = 1 et N = 1, exactement comme le symbole CEI de la porte ET."),
    ]))


# ================================================================ cartes et habillage
def ill_line(img, d, t):
    d.rectangle((300, 300, 520, 430), outline=NAVY, width=4, fill=WHITE)
    d.rectangle((304, 360, 516, 426), fill=LBLUE)
    d.rectangle((402, 430, 418, 520), fill=LGREY, outline=NAVY, width=2)
    d.rounded_rectangle((90, 680, 740, 715), radius=16, fill=LGREY, outline=NAVY, width=3)
    for i in range(4):
        x = 90 + ((t * 50 + i * 170) % 650)
        d.rectangle((x, 560, x + 50, 680), fill=WHITE, outline=NAVY, width=3)
        d.rectangle((x + 15, 535, x + 35, 560), fill=WHITE, outline=NAVY, width=3)
    for k, (lab, v) in enumerate((("B", 1), ("N", 1), ("V", 1))):
        text(d, (560, 330 + k * 60), lab, 30, NAVY, True, italic=True, anchor="lm")
        bitpill(d, (630, 330 + k * 60), int((t * 1.2 + k) % 2), 24)


def ill_table(img, d, t):
    rows = [[(v >> 2) & 1, (v >> 1) & 1, v & 1, "?"] for v in range(8)]
    table(d, 200, 260, ["C", "B", "A", "Y"], rows, 90, 58, int(t * 1.5) % 8, 28)


def ill_scope(img, d, t):
    rbox(d, (110, 330, 720, 760), fill=(40, 44, 60), outline=NAVY, width=4, r=20)
    d.rectangle((150, 370, 600, 720), fill=(10, 30, 20))
    for k, (sig, col) in enumerate(((CA, (120, 255, 140)), (CB, (255, 230, 90)), (D.chrono("ET"), (120, 200, 255)))):
        yb = 470 + k * 100
        pts = []
        for i in range(8):
            y = yb - 50 if sig[i] else yb
            pts += [(160 + i * 54, y), (160 + (i + 1) * 54, y)]
        d.line(pts, fill=col, width=3)
    for k in range(4): d.ellipse((630, 400 + k * 75, 680, 450 + k * 75), outline=LGREY, width=3)


def ill_gates(img, d, t):
    for i, k in enumerate(ORDER):
        x = 110 + (i % 3) * 220; y = 280 + (i // 3) * 200
        gate(d, x, y, k, 0.5, labels=("", ""), out_label="", lead=30)
        text(d, (x + 40, y + 120), D.GATES[k][0], 20, NAVY, True, anchor="mm")


def ill_chip(img, d, t):
    d.rounded_rectangle((260, 330, 560, 760), radius=12, fill=(52, 56, 70), outline=NAVY, width=3)
    for i in range(7):
        y = 360 + i * 60
        d.rectangle((225, y - 12, 260, y + 12), fill=LGREY, outline=NAVY, width=2)
        d.rectangle((560, y - 12, 595, y + 12), fill=LGREY, outline=NAVY, width=2)
    text(d, (410, 545), "74HC08", 40, (235, 238, 245), True, mono=True, anchor="mm")
    d.pieslice((380, 300, 440, 360), 0, 180, fill=(30, 32, 44))


CARDS = [
    ("1", TOT, "Des 0 et des 1", "La ligne de remplissage de boissons", ill_line,
     "Une ligne remplit des bouteilles de boisson. Des capteurs surveillent la bouteille et le niveau de la cuve.",
     "Comment un circuit décide-t-il d'ouvrir la vanne ? C'est la question de départ de la présentation 120.",
     "On traduit chaque capteur et chaque actionneur en variable binaire : 1 ou 0.", "V = B · N"),
    ("2", TOT, "Construire une table de vérité", "Toutes les combinaisons, dans l'ordre", ill_table,
     "Le moteur du convoyeur dépend de trois capteurs : E, L et U.",
     "Comment être sûr de n'oublier aucun cas ?",
     "Une colonne par entrée, du poids fort au poids faible, et on compte en binaire.", "3 entrées → 8 lignes"),
    ("3", TOT, "Lire un chronogramme", "De l'analyseur logique à la table de vérité", ill_scope,
     "Au laboratoire, l'analyseur logique affiche les signaux A, B et Y d'une porte.",
     "Comment relier ce que l'écran montre à la table de vérité ?",
     "On lit le chronogramme intervalle par intervalle, comme les lignes de la table.", "1 intervalle = 1 ligne"),
    ("4", TOT, "Les sept portes de base", "Symboles CEI, tables de vérité, équations", ill_gates,
     "Toute commande numérique est faite de quelques portes de base, combinées entre elles.",
     "Comment reconnaître chaque porte par son symbole, sa table ou son équation ?",
     "On fait passer les combinaisons B A dans chaque porte et on lit Y.", "&   ≥1   =1   1"),
    ("5", TOT, "Du symbole au circuit intégré", "Câbler la vanne sur un 74HC08", ill_chip,
     "Sur breadboard, tu câbles la commande de la vanne V = B · N.",
     "Quel CI prendre, et sur quelles broches brancher B, N, V et l'alimentation ?",
     "On lit le brochage du 74HC08 et on relie chaque signal à sa broche.", "74HC08 : broches 1 et 2 → 3"),
]
CARD_DUR = 13.0

s_intro = intro_scene("TEST ET MESURE 1 – EL DT 1 · ANIMATION 125", "Portes logiques et tables de vérité",
                      "Des 0 et des 1, sept portes, quatre façons de les décrire",
                      [("1", "Des 0 et des 1", "la ligne de remplissage"), ("2", "Construire une table de vérité", "C B A, du poids fort au poids faible"),
                       ("3", "Lire un chronogramme", "un intervalle = une ligne"), ("4", "Les sept portes de base", "symboles CEI"),
                       ("5", "Du symbole au circuit intégré", "câbler un 74HC08")],
                      "Théorie : Floyd, chap. 3, 3-1 à 3-6 (p. 112-138) · nextecmedia 1.1 et 1.2.1")

s_outro = outro_scene(
    [("Variable", "1 = vrai, actif ; 0 = faux, inactif"), ("Table", "entrées du poids fort au poids faible, 2ⁿ lignes, comptage binaire"),
     ("Chronogramme", "chaque intervalle correspond à une ligne de la table"), ("7 portes", "NON, ET, OU, NON-ET, NON-OU, OU exclusif, NON-OU exclusif"),
     ("CI", "74HC08 ET · 74HC32 OU · 74HC04 NON · 74HC00 NON-ET")],
    "À toi de jouer",
    [("Fiche 130 EX, partie A", "les sept portes : table, équation, chronogramme", ""), ("Fiche 130 EX, N°1", "du cahier des charges à la table", ""),
     ("Fiche 130 EX, N°2 et N°3", "chronogrammes, reconnaître une porte", ""), ("Fiche 130 EX, N°4", "câbler la vanne sur un 74HC08", ""),
     ("Floyd, chap. 3, 3-1 à 3-6", "Inverseur à NON-OU exclusif", "p. 112-138"), ("Page interactive 121", "exercices sur des cas réels", "")],
    "Les liens du Floyd, de nextecmedia et de la présentation 120 sont dans la fiche 130 EX.")

SCENES = [(s_intro, 9.0), (make_card(CARDS, 0, CARD_DUR), CARD_DUR), (s_line, 46.0), (make_card(CARDS, 1, CARD_DUR), CARD_DUR), (s_table, 50.0),
          (make_card(CARDS, 2, CARD_DUR), CARD_DUR), (s_chrono, 44.0), (make_card(CARDS, 3, CARD_DUR), CARD_DUR), (s_gates, 75.0),
          (make_card(CARDS, 4, CARD_DUR), CARD_DUR), (s_ic, 38.0), (s_outro, 15.0)]

def produire(ctx):
    render(SCENES, ctx.sortie_de("125"))


if __name__ == "__main__":
    # aperçu d'une image : python3 contenus/tm1/semaine-1/125-anim.py <scène> <t> [image.png]
    i, t = int(sys.argv[1]), float(sys.argv[2])
    frame_at(SCENES, i, t).save(sys.argv[3] if len(sys.argv) > 3 else f"apercu_125.png")
