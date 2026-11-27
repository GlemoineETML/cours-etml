# -*- coding: utf-8 -*-
"""125 Portes logiques et tables de vérité – animation (TM1 – El DT 1, semaine 1, va avec la présentation 120 et la fiche 130 EX).
V2 (11/27/2026) : démarrage d'une voiture électrique (exercice TM1-A1-S2) à la place de la ligne de remplissage ; sortie notée S.
Tables de vérité : entrées du poids fort au poids faible (C B A, B A), puis la sortie. Symboles CEI 60617-12.
Données : moteur/logique.py (GATES, tdv, CHRONO_A/B). Rendu : python3 build.py tm1/semaine-1 --seulement animations · aperçu : voir en bas"""
import math, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))   # aperçu direct
from moteur.anim import *
from moteur import logique as D

ICI = os.path.dirname(os.path.abspath(__file__))

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


EQ = {"NON": [("S = ", False), ("A", True)], "ET": [("S = A · B", False)], "OU": [("S = A + B", False)],
      "NON-ET": [("S = ", False), ("A · B", True)], "NON-OU": [("S = ", False), ("A + B", True)],
      "OUX": [("S = A ⊕ B", False)], "NON-OUX": [("S = ", False), ("A ⊕ B", True)]}
SY = lambda t: re.sub(r"\bY\b", "S", t)        # règles de moteur/logique.py, écrites avec Y


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


# ================================================================ 1 · le démarrage d'une voiture électrique (TM1-A1-S2)
# Cahier des charges : A = 0 ceinture bouclée, B = 1 sélecteur sur P, C = 0 frein enfoncé, D = 1 mode service.
# S = 1 (voyant « démarrage ») : S = B · (D + /(A + C)).
def demarre(a, b, c, dd):
    return b & (dd | (1 - (a | c)))


# scénario (temps de la scène) : (début, A, B, C, D)
SC = [(0.0, 1, 0, 1, 0), (8.0, 0, 0, 1, 0), (11.5, 0, 1, 1, 0), (17.5, 0, 1, 0, 0), (24.0, 0, 1, 1, 0),
      (28.5, 1, 1, 1, 0), (33.5, 1, 1, 1, 1), (40.0, 1, 0, 1, 1), (51.0, 1, 1, 1, 1)]
S1_CHAIN = 46.0


def etat(t):
    cur = SC[0]
    for e in SC:
        if t >= e[0]: cur = e
    a, b, c, dd = cur[1:]
    return a, b, c, dd, demarre(a, b, c, dd)


CAR_FILL, SEAT, TYRE, HUB, DASH, LED_ON = TINT, (90, 100, 120), (58, 63, 82), (200, 206, 218), (213, 221, 223), (255, 90, 60)


def voiture(d, X0, Y0, k, a, b, c, dd, s, reperes=True, alpha=1.0):
    """Voiture vue de côté (avant à droite), dessin de la figure fig_voiture (figures.py), états des capteurs animés.
    (X0, Y0) : position de l'origine du dessin ; k : pixels par unité."""
    P = lambda x, y: (X0 + (x + 0.75) * k, Y0 - y * k)
    m = lambda c_: mix(WHITE, c_, alpha)
    w = lambda u: max(2, int(u * k / 145))
    d.line((P(-0.1, 0.19), P(7.1, 0.19)), fill=m(LGREY), width=w(3))
    d.polygon([P(*p) for p in [(0.25, 0.62), (0.2, 1.45), (1.25, 1.62), (2.05, 2.42), (3.95, 2.48), (4.85, 1.72), (6.05, 1.52), (6.25, 1.05), (6.2, 0.62)]],
              fill=m(CAR_FILL), outline=m(NAVY), width=w(4))
    d.polygon([P(*p) for p in [(2.2, 1.72), (2.3, 2.3), (3.85, 2.33), (4.5, 1.74)]], fill=m(WHITE), outline=m(NAVY), width=w(3))
    for xr in (1.45, 5.0):
        cx, cy = P(xr, 0.62)
        d.ellipse((cx - 0.43 * k, cy - 0.43 * k, cx + 0.43 * k, cy + 0.43 * k), fill=m(TYRE), outline=m(NAVY), width=w(2))
        d.ellipse((cx - 0.16 * k, cy - 0.16 * k, cx + 0.16 * k, cy + 0.16 * k), fill=m(HUB), outline=m(NAVY), width=w(2))
    # siège ; ceinture (A) : en travers du buste si bouclée (A = 0), pendante sinon
    d.line((P(2.95, 0.98), P(2.78, 2.05)), fill=m(SEAT), width=w(16))
    d.line((P(2.95, 0.98), P(3.65, 1.02)), fill=m(SEAT), width=w(16))
    bx0, by0 = P(3.47, 1.11); bx1, by1 = P(3.63, 0.98)
    if a == 0:
        d.line((P(2.86, 1.92), P(3.52, 1.08)), fill=m(NAVY), width=w(8))
        d.rectangle((bx0, by0, bx1, by1), fill=m(NAVY))
    else:
        d.line((P(2.86, 1.92), P(2.84, 1.32)), fill=m(NAVY), width=w(8))
        d.rectangle((bx0, by0, bx1, by1), outline=m(NAVY), width=w(3), fill=m(WHITE))
    # volant, tableau de bord et voyant S
    d.line((P(4.05, 1.32), P(4.25, 1.78)), fill=m(NAVY), width=w(6))
    d.rectangle((*P(4.32, 1.64), *P(4.94, 1.42)), fill=m(DASH), outline=m(NAVY), width=w(2))
    lx, ly = P(4.63, 1.53); r = 0.075 * k
    if s: d.ellipse((lx - 2.2 * r, ly - 2.2 * r, lx + 2.2 * r, ly + 2.2 * r), fill=m(mix(WHITE, LED_ON, 0.35)))
    d.ellipse((lx - r, ly - r, lx + r, ly + r), fill=m(LED_ON if s else (240, 242, 247)), outline=m(NAVY), width=w(2))
    # sélecteur (B) : levier droit sur P, incliné sur D (marche)
    sx0, sy0 = P(3.75, 1.2); sx1, sy1 = P(4.07, 0.98)
    d.rectangle((sx0, sy0, sx1, sy1), fill=m(WHITE), outline=m(NAVY), width=w(2))
    text(d, ((sx0 + sx1) / 2, (sy0 + sy1) / 2), "P" if b else "D", max(12, int(0.15 * k)), m(BLUE if b else GREY), True, anchor="mm")
    top = (3.91, 1.4) if b else (4.03, 1.37)
    d.line((P(3.91, 1.2), P(*top)), fill=m(NAVY), width=w(5))
    kx, ky = P(*top); d.ellipse((kx - 0.065 * k, ky - 0.065 * k, kx + 0.065 * k, ky + 0.065 * k), fill=m(NAVY))
    # pédale de frein (C) : enfoncée (C = 0) → poussée vers l'avant, pied dessus
    pad = (4.9, 0.8) if c == 0 else (4.75, 0.8)
    d.line((P(4.95, 1.15), P(*pad)), fill=m(NAVY), width=w(6))
    if c == 0:
        fx, fy = P(pad[0] - 0.12, pad[1] + 0.02)
        d.rounded_rectangle((fx - 0.24 * k, fy - 0.08 * k, fx + 0.08 * k, fy + 0.07 * k), radius=int(0.06 * k), fill=m(SEAT))
    # commutateur de service (D)
    tx0, ty0 = P(5.25, 1.3); tx1, ty1 = P(5.55, 1.12)
    d.rounded_rectangle((tx0, ty0, tx1, ty1), radius=int(0.08 * k), fill=m(BLUE if dd else WHITE), outline=m(NAVY), width=w(2))
    kx = tx1 - 0.09 * k if dd else tx0 + 0.09 * k
    d.ellipse((kx - 0.06 * k, (ty0 + ty1) / 2 - 0.06 * k, kx + 0.06 * k, (ty0 + ty1) / 2 + 0.06 * k), fill=m(WHITE), outline=m(NAVY), width=w(2))
    if not reperes: return
    sq = 0.34 * k

    def repere(x, y, xc, yc, lab, v, col=BLUE, rond=False):
        d.line((P(x, y), P(xc, yc)), fill=m(LGREY), width=w(2))
        cx, cy = P(x, y)
        if rond: d.rounded_rectangle((cx - sq / 2, cy - sq / 2, cx + sq / 2, cy + sq / 2), radius=int(sq * 0.25), fill=m(col))
        else: d.rectangle((cx - sq / 2, cy - sq / 2, cx + sq / 2, cy + sq / 2), fill=m(col))
        text(d, (cx, cy), lab, int(sq * 0.55), m(WHITE), True, anchor="mm")
        bitpill(d, (cx + sq / 2 + 0.2 * k, cy), v, int(0.15 * k), alpha)

    repere(2.45, 2.85, 3.15, 1.62, "A", a)
    repere(3.55, 2.85, 3.91, 1.4, "B", b)
    repere(3.95, 0.28, 4.8, 0.86, "C", c)
    repere(5.85, 0.28, 5.4, 1.12, "D", dd)
    repere(4.95, 2.85, 4.63, 1.6, "S", s, NAVY, True)


VARS = [("A", "ceinture de sécurité", "0 = bouclée", BLUE), ("B", "sélecteur de vitesse", "1 = position P", BLUE),
        ("C", "pédale de frein", "0 = enfoncée", BLUE), ("D", "mode service", "1 = actif", BLUE), ("S", "voyant « démarrage »", "1 = allumé", NAVY)]


def chaine(d, x1, y1, s, a, b, c, dd, alpha=1.0):
    """NON-OU (A, C) → OU (avec D) → ET (avec B) → S, en escalier : chaque sortie entre tout droit dans l'entrée du haut de la porte suivante."""
    h, L, gap = 190 * s, 70 * s, 55
    nor = 1 - (a | c); ou = dd | nor; S = b & ou
    _, o1 = gate(d, x1, y1, "NON-OU", s, vin=(a, c), vout=nor, labels=("A", "C"), alpha=alpha, out_label="")
    x2 = o1[0] + gap + L; y2 = o1[1] - 0.28 * h
    wire(d, [o1, (x2 - L, o1[1])], nor, int(4 * s) + 1, alpha)
    _, o2 = gate(d, x2, y2, "OU", s, vin=(nor, dd), vout=ou, labels=("", "D"), alpha=alpha, out_label="")
    x3 = o2[0] + gap + L; y3 = o2[1] - 0.28 * h
    wire(d, [o2, (x3 - L, o2[1])], ou, int(4 * s) + 1, alpha)
    _, o3 = gate(d, x3, y3, "ET", s, vin=(ou, b), vout=S, labels=("", "B"), alpha=alpha, out_label="S")
    for x, y, nom in ((x1, y1, "NON-OU"), (x2, y2, "OU"), (x3, y3, "ET")):
        text(d, (x + 75 * s, y + h + 8), nom, 19, mix(WHITE, GREY, alpha), True, anchor="ma")
    return S


def s_car(img, d, t):
    chrome(img, d, "1 · DES 0 ET DES 1", "Le démarrage d'une voiture électrique", f"1/{TOT}")
    ref_pill(d, "présentation 120, diapo 2 et 13 · Floyd 1-2 p. 5")
    a, b, c, dd, S = etat(t)
    voiture(d, -57.75, 628, 145, a, b, c, dd, S)
    # variables binaires
    X = 1010
    rbox(d, (X, 160, 1726, 560), fill=PALE, outline=NAVY, width=3, r=16)
    text(d, (X + 25, 178), "Variables binaires", 26, BLUE, True)
    for i, (nm, lab, niv, col) in enumerate(VARS):
        y = 250 + i * 60
        if nm == "S": d.rounded_rectangle((X + 28, y - 20, X + 68, y + 20), radius=9, fill=col)
        else: d.rectangle((X + 28, y - 20, X + 68, y + 20), fill=col)
        text(d, (X + 48, y), nm, 24, WHITE, True, anchor="mm")
        text(d, (X + 90, y), lab, 25, NAVY, anchor="lm")
        text(d, (X + 390, y), niv, 25, ORANGE if niv.startswith("0") else NAVY, True, anchor="lm")
        bitpill(d, (X + 660, y), (a, b, c, dd, S)[i], 22)
    text(d, (X + 25, 535), "Attention : A et C sont actifs à 0.", 22, ORANGE, True, italic=True, anchor="lm")
    # voyant
    rbox(d, (X, 580, 1726, 880), fill=TINT, r=16)
    lamp(d, (X + 100, 680), bool(S), 50, None, LED_ON)
    text(d, (X + 185, 650), "voyant « démarrage »", 26, NAVY, True, anchor="lm")
    text(d, (X + 185, 700), "S = 1 : démarrage autorisé" if S else "S = 0 : démarrage bloqué", 26, BLUE if S else GREY, True, anchor="lm")
    q = prog(t, S1_CHAIN + 4.0, S1_CHAIN + 5.0)
    if q > 0:
        over_eq(d, X + 358, 820, [("S = B · (D + ", False), ("A + C", True), (")", False)], 40, mix(TINT, NAVY, q), anchor_mid=True)
    # conditions, puis les portes
    rbox(d, (60, 660, 990, 885), fill=WHITE, outline=LGREY, width=2, r=14)
    qc = 1 - prog(t, S1_CHAIN, S1_CHAIN + 1.0)
    if qc > 0:
        text(d, (85, 680), "Conditions pour démarrer", 22, mix(WHITE, BLUE, qc), True)
        conds = [("ceinture bouclée (A = 0)", a == 0), ("sélecteur sur P (B = 1)", b == 1), ("frein enfoncé (C = 0)", c == 0),
                 ("ou mode service (D = 1) : ceinture et frein inutiles", dd == 1)]
        for i, (txt, ok_) in enumerate(conds):
            y = 735 + i * 42
            check(d, (100, y), ok_, 30, qc)
            text(d, (130, y), txt, 24, mix(WHITE, NAVY, qc), anchor="lm")
    qg = prog(t, S1_CHAIN + 0.5, S1_CHAIN + 1.5)
    if qg > 0:
        chaine(d, 200, 672, 0.64, a, b, c, dd, qg)
    caption(d, cap_at(t, [
        (0, "Dans la voiture, chaque capteur répond par oui ou par non : c'est une variable binaire, 1 ou 0."),
        (4.0, "Attention : la ceinture A et le frein C sont actifs à 0. Le sélecteur B, le mode service D et le voyant S sont actifs à 1."),
        (8.0, "Le conducteur boucle sa ceinture : A passe à 0."),
        (11.5, "Il met le sélecteur sur P : B = 1. Le voyant reste éteint : le frein n'est pas enfoncé."),
        (17.5, "Il enfonce la pédale de frein : C = 0. Les trois conditions sont remplies : S = 1, le voyant s'allume."),
        (24.0, "Il relâche le frein : C = 1. Le voyant s'éteint."),
        (28.5, "Au garage, le mécanicien ne boucle pas sa ceinture : A = 1."),
        (33.5, "Il active le mode service : D = 1. Plus besoin de la ceinture ni du frein : S = 1."),
        (40.0, "Mais le sélecteur reste obligatoire : hors de P, B = 0 et S = 0, même en mode service."),
        (S1_CHAIN, "En portes : une NON-OU pour A et C, une OU avec D, puis une ET avec B."),
        (51.0, "Sélecteur sur P : B = 1, S = 1. La barre sur A + C vient de la porte NON-OU."),
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
    heads = ["C", "B", "A", "S"]
    show = clamp(int((t - S2_R0) / S2_DR) + 1, 0, 8) if t >= S2_R0 else 0
    rows = []
    for v in range(8):
        c, b, a = (v >> 2) & 1, (v >> 1) & 1, v & 1
        m = None
        if ex:
            k = int((t - S2_EX - 2.0) / 1.2) + 1 if t >= S2_EX + 2.0 else 0
            m = demarre(a, b, c, 0) if v < k else None
        rows.append([c, b, a, m if ex else "?"])
    tx, ty = 690, 200
    hl = None
    if S2_R0 <= t < S2_COL: hl = show - 1
    if ex and t >= S2_EX + 2.0:
        k = int((t - S2_EX - 2.0) / 1.2)
        hl = 2 if k >= 8 else min(k, 7)
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
    text(d, (tx + 100 + 135, ty + 60 * 9 + 80), "poids fort  →  poids faible", 22, GREY, italic=True, anchor="mm")
    # cahier des charges (exemple)
    q = prog(t, S2_EX, S2_EX + 1.0)
    if q > 0:
        X = 1180
        rbox(d, (X, 200, 1720, 560), fill=mix(WHITE, PALE, q), outline=mix(WHITE, NAVY, q), width=3, r=16)
        text(d, (X + 25, 222), "Cahier des charges (fiche 130 EX, N°1)", 24, mix(WHITE, BLUE, q), True)
        para(d, (X + 25, 270), "Sans le mode service (D = 0), la voiture démarre si la ceinture est bouclée (A = 0), le sélecteur sur P (B = 1) et la pédale de frein enfoncée (C = 0).", 25, 490, mix(WHITE, NAVY, q))
        r = prog(t, S2_EX + 12.0, S2_EX + 13.0)
        if r > 0:
            rbox(d, (X, 600, 1720, 760), fill=mix(WHITE, TINT, r), r=16)
            over_eq(d, X + 270, 680, [("S = ", False), ("C", True), (" · B · ", False), ("A", True)], 46, mix(WHITE, NAVY, r), anchor_mid=True)
    seq = [(0, "Une table de vérité donne la sortie pour toutes les combinaisons des entrées. Voici la méthode, en quatre règles."),
           (S2_R0, "Trois entrées C, B, A : C est le poids fort, A le poids faible. On écrit les lignes en comptant en binaire."),
           (S2_R0 + 4 * S2_DR, "Ligne 4 : 100. On compte comme en numération : la colonne de gauche vaut 4, celle du milieu 2, celle de droite 1."),
           (S2_COL, "Vérification rapide : A, le poids faible, change à chaque ligne…"),
           (S2_COL + 3, "… B change toutes les deux lignes…"),
           (S2_COL + 6, "… et C, le poids fort, toutes les quatre lignes. Si ce rythme est respecté, aucune ligne ne manque."),
           (S2_EX, "Exemple : le démarrage sans le mode service (D = 0). Il reste trois entrées : C, B et A."),
           (S2_EX + 2.0, "Pour chaque ligne, on se demande : le cahier des charges autorise-t-il le démarrage ?"),
           (S2_EX + 11.6, "Une seule ligne donne S = 1 : C = 0, B = 1 et A = 0. D'où l'équation S = C̄ · B · Ā.")]
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
    rowsy = {"A": 300, "B": 450, "S": 620}
    for i in range(8):
        text(d, (x0 + i * pw + pw / 2, 205), str(i + 1), 26, GREY, True, anchor="mm")
    if k >= 0:
        xa = x0 + k * pw
        rbox(d, (xa + 4, 225, xa + pw - 4, 700), fill=TINT, outline=BLUE, width=3, r=10)
    for nm, sig in (("A", CA), ("B", CB), ("S", Yv)):
        yb = rowsy[nm]; yh = yb - 80
        text(d, (x0 - 40, yb - 40), nm, 34, NAVY, True, italic=True, anchor="mm")
        d.line((x0, yb, x0 + 8 * pw, yb), fill=LGREY, width=2)
        n = 8 if nm != "S" else (k + 1 if k >= 0 else 0)
        if nm == "S" and k >= 0:
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
        if len(pts) > 1: d.line(pts, fill=BLUE if nm == "S" else NAVY, width=6, joint="curve")
        for i in range(8 if nm != "S" else full):
            text(d, (x0 + i * pw + pw / 2, yb + 22), str(sig[i]), 20, GREY, anchor="mm")
    # table B A S de la porte ET
    tdv = D.tdv("ET")
    hl = None; vis = set()
    for i in range(k + 1):
        r = [j for j, (b, a, y) in enumerate(tdv) if b == CB[i] and a == CA[i]][0]
        vis.add(r)
        if i == k: hl = r
    rows = [[b, a, (y if j in vis else None)] for j, (b, a, y) in enumerate(tdv)]
    X = 1220
    text(d, (X, 200), "Table de vérité de la porte ET", 26, BLUE, True)
    table(d, X + 40, 250, ["B", "A", "S"], rows, 110, 68, hl, 32)
    gate(d, X + 110, 640, "ET", 0.75, vin=(CA[k], CB[k]) if k >= 0 else None, vout=Yv[k] if k >= 0 else None, lead=60, out_label="S")
    seq = [(0, "L'analyseur logique montre les signaux dans le temps. Le temps avance de gauche à droite, une ligne par variable."),
           (3.5, "On découpe le temps en intervalles où rien ne change. Dans chaque intervalle, on lit A et B, puis on cherche la ligne de la table.")]
    for i in range(8):
        txt = f"Intervalle {i + 1} : A = {CA[i]}, B = {CB[i]}. Dans la table, c'est la ligne B A = {CB[i]}{CA[i]}, donc S = {Yv[i]}."
        if i == 4: txt = f"Intervalle 5 : A = {CA[i]}, B = {CB[i]}, la même combinaison qu'à l'intervalle 2. Même ligne de la table, même S = {Yv[i]}."
        seq.append((S3_T0 + i * S3_DT, txt))
    seq.append((S3_T0 + 8 * S3_DT, "Un chronogramme parcourt la table de vérité dans l'ordre où les combinaisons arrivent. Ici, S = 1 seulement quand A = 1 et B = 1."))
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
    ins, out = gate(d, 330, 330 if n == 2 else 350, key, 1.45, vin=vin, vout=vout, alpha=a, lead=95, out_label="S")
    # interrupteurs d'entrée et lampe
    names = ["A"] if n == 1 else ["A", "B"]
    for i, p in enumerate(ins):
        v = vin[i] if vin else 0
        bitpill(d, (p[0] - 100, p[1]), v, 30, a)
    lamp(d, (out[0] + 110, out[1]), bool(vout) if vout is not None else False, 36, None, BLUE)
    text(d, (440, 760), f"Porte {g[0]} ({g[1]})", 40, mix(WHITE, NAVY, a), True, anchor="mm")
    # table B A S
    X = 1120
    heads = ["A", "S"] if n == 1 else ["B", "A", "S"]
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
    para(d, (X + 10, y0 + 95), SY(g[8]), 24, 560, mix(WHITE, NAVY, q))
    text(d, (X + 10, y0 + (190 if n == 2 else 170)), f"CI : {g[9]} ({g[11]})", 22, mix(WHITE, GREY, q), True)
    seq = [(0, "Sept portes de base. Pour chacune, on fait passer les combinaisons d'entrée, du poids fort au poids faible, et on lit la sortie S.")]
    expl = {"NON": "NON (inverseur) : une seule entrée. La sortie est l'inverse de l'entrée. Le cercle sur la sortie signale cette inversion.",
            "ET": "ET : S = 1 seulement si A et B valent 1. Le qualificatif & est dans le rectangle.",
            "OU": "OU : S = 1 dès qu'une entrée vaut 1, ou les deux. Qualificatif ≥1 : au moins une entrée à 1.",
            "NON-ET": "NON-ET : le symbole du ET avec un cercle de négation. S = 0 seulement si A = B = 1.",
            "NON-OU": "NON-OU : le symbole du OU avec un cercle. S = 1 seulement si A = B = 0.",
            "OUX": "OU exclusif : S = 1 quand les entrées sont différentes. Qualificatif =1 : exactement une entrée à 1.",
            "NON-OUX": "NON-OU exclusif : S = 1 quand les deux entrées sont égales. C'est un détecteur d'égalité."}
    for i, k in enumerate(ORDER):
        seq.append((S4_T0 + i * S4_DG + 0.2, expl[k]))
    caption(d, cap_at(t, seq))


# ================================================================ 5 · du symbole au circuit intégré : la porte NON-OU sur un 74HC02
PL = D.PINS["74HC02"][:7]                  # broches 1 à 7, à gauche : 1Y 1A 1B 2Y 2A 2B GND (la sortie avant les entrées)
PR = D.PINS["74HC02"][7:][::-1]            # broches 14 à 8, à droite : VCC 4Y 4B 4A 3Y 3B 3A
S5 = {"A": 7.0, "C": 11.0, "Y": 15.0, "VCC": 23.0, "GND": 26.5, "NC": 30.5, "DEMO": 37.0, "FIN": 46.0}


def s_ic(img, d, t):
    chrome(img, d, "5 · DU SYMBOLE AU CIRCUIT INTÉGRÉ", "La porte NON-OU sur un 74HC02", f"5/{TOT}")
    ref_pill(d, "présentation 120, diapo 14 · fiche 130 EX N°4 · Floyd 3-8 p. 146")
    bx0, by0, bx1, by1 = 760, 230, 1060, 830
    pitch = (by1 - by0 - 60) / 6
    py = lambda i: by0 + 30 + i * pitch
    a = prog(t, 0.3, 1.3)
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=12, fill=mix(WHITE, (52, 56, 70), a), outline=mix(WHITE, NAVY, a), width=3)
    d.pieslice(((bx0 + bx1) / 2 - 30, by0 - 30, (bx0 + bx1) / 2 + 30, by0 + 30), 0, 180, fill=mix(WHITE, (30, 32, 44), a))
    text(d, ((bx0 + bx1) / 2, (py(2) + py(3)) / 2), "74HC02", 44, mix(WHITE, (235, 238, 245), a), True, mono=True, anchor="mm")
    text(d, ((bx0 + bx1) / 2, (py(3) + py(4)) / 2), "4 portes NON-OU", 24, mix(WHITE, (200, 205, 220), a), anchor="mm")
    for i in range(7):
        y = py(i)
        d.rectangle((bx0 - 40, y - 14, bx0, y + 14), fill=mix(WHITE, LGREY, a), outline=mix(WHITE, NAVY, a), width=2)
        d.rectangle((bx1, y - 14, bx1 + 40, y + 14), fill=mix(WHITE, LGREY, a), outline=mix(WHITE, NAVY, a), width=2)
        text(d, (bx0 + 12, y), str(i + 1), 18, mix(WHITE, (170, 176, 192), a), True, anchor="lm")
        text(d, (bx1 - 12, y), str(14 - i), 18, mix(WHITE, (170, 176, 192), a), True, anchor="rm")
        text(d, (bx0 + 46, y), PL[i], 24, mix(WHITE, (235, 238, 245), a), True, anchor="lm")
        text(d, (bx1 - 46, y), PR[i], 24, mix(WHITE, (235, 238, 245), a), True, anchor="rm")
    # démonstration : A et C basculent (ceinture, frein)
    demo = [(0, 0), (1, 0), (0, 1), (1, 1)]
    if S5["DEMO"] <= t < S5["FIN"]:
        Av, Cv = demo[min(int((t - S5["DEMO"]) / 2.0), 3)]
    else:
        Av, Cv = 0, 0
    Yv = 1 - (Av | Cv)

    def src(y, lab, sub, v):
        rbox(d, (90, y - 36, 330, y + 36), fill=TINT, outline=NAVY, width=2, r=10)
        text(d, (110, y - 8), lab, 28, NAVY, True, italic=True, anchor="lm")
        text(d, (110, y + 18), sub, 18, GREY, anchor="lm")
        bitpill(d, (300, y), v, 22)

    yY, yA, yC = py(0), py(1), py(2)
    q = prog(t, S5["A"] - 1, S5["A"])
    if q > 0:
        src(yA + 60, "A", "ceinture", Av)
        wire(d, [(330, yA + 60), (560, yA + 60), (560, yA), (bx0 - 40, yA)][: 2 + int(q * 2)], Av, 4)
    q = prog(t, S5["C"] - 1, S5["C"])
    if q > 0:
        src(yC + 140, "C", "frein", Cv)
        wire(d, [(330, yC + 140), (620, yC + 140), (620, yC), (bx0 - 40, yC)][: 2 + int(q * 2)], Cv, 4)
    q = prog(t, S5["Y"] - 1, S5["Y"])
    if q > 0:
        wire(d, [(bx0 - 40, yY), (520, yY), (520, yY - 75), (330, yY - 75)][: 2 + int(q * 2)], Yv, 4)
        rbox(d, (90, yY - 111, 330, yY - 39), fill=mix(WHITE, BLUE, 0.15 if Yv else 0), outline=NAVY, width=2, r=10)
        text(d, (110, yY - 83), "vers le 74HC32", 21, NAVY, True, anchor="lm")
        text(d, (110, yY - 57), "porte OU, broche 1", 18, GREY, anchor="lm")
        label_box(d, (bx0 - 125, yY + 42), "sortie 1Y = broche 1 !", 22, ORANGE, alpha=prog(t, S5["Y"], S5["Y"] + 0.6))
    # alimentation (CEI : miroir de la masse, au-dessus) et masse
    q = prog(t, S5["VCC"] - 1, S5["VCC"])
    if q > 0:
        y = py(0); xa = bx1 + 40 + 110 * q
        d.line((bx1 + 40, y, xa, y), fill=RED, width=5)
        if q >= 1: alimentation(d, xa, y, "+5 V", fil=45)
    q = prog(t, S5["GND"] - 1, S5["GND"])
    if q > 0:
        y = py(6); xg = bx0 - 40 - 80 * q
        d.line((bx0 - 40, y, xg, y), fill=NAVY, width=5)
        if q >= 1: masse(d, xg, y, "GND", fil=40)
    # entrées inutilisées à GND (portes 2, 3 et 4) : reliées par un fil commun, points de liaison aux jonctions en T
    q = prog(t, S5["NC"] - 1, S5["NC"])
    if q > 0:
        col = mix(WHITE, GREEN, q)
        xl = bx0 - 120
        for i in (4, 5):
            d.line((bx0 - 40, py(i), xl, py(i)), fill=col, width=4)
        d.line((xl, py(4), xl, py(6)), fill=col, width=4)
        noeud(d, xl, py(5), 7, GREEN, q); noeud(d, xl, py(6), 7, NAVY, q)
        xr = bx1 + 120
        for i in (2, 3, 5, 6):
            d.line((bx1 + 40, py(i), xr, py(i)), fill=col, width=4)
        d.line((xr, py(2), xr, py(6)), fill=col, width=4)
        for i in (3, 5): noeud(d, xr, py(i), 7, GREEN, q)
        noeud(d, xr, py(6), 7, NAVY, q)
        masse(d, xr, py(6), "GND", fil=40, alpha=q)
        label_box(d, (1440, py(1)), "entrées inutilisées → GND", 22, GREEN, alpha=q)
        label_box(d, (1440, py(1) + 40), "sorties 2Y, 3Y, 4Y : libres", 20, GREY, alpha=q)
    # symbole équivalent
    q = prog(t, S5["DEMO"] - 1, S5["DEMO"])
    if q > 0:
        rbox(d, (1300, 590, 1720, 880), fill=mix(WHITE, TINT, q), r=16)
        gate(d, 1420, 630, "NON-OU", 0.8, vin=(Av, Cv), vout=Yv, labels=("A", "C"), out_label="1Y", alpha=q, lead=60)
        text(d, (1510, 820), "porte 1 du 74HC02", 20, mix(WHITE, GREY, q), True, anchor="mm")
    caption(d, cap_at(t, [
        (0, "Le 74HC02 contient 4 portes NON-OU à 2 entrées. On repère la broche 1 grâce à l'encoche, puis on compte dans le sens inverse des aiguilles d'une montre."),
        (S5["A"] - 1, "Porte 1 : le capteur de ceinture A arrive sur la broche 2 (entrée 1A)."),
        (S5["C"] - 1, "Le capteur de frein C arrive sur la broche 3 (entrée 1B)."),
        (S5["Y"] - 1, "Piège : sur le 74HC02, la sortie 1Y est la broche 1, avant les entrées. Elle part vers la porte OU du 74HC32."),
        (S5["VCC"] - 1, "Sans alimentation, rien ne marche : broche 14 au +5 V…"),
        (S5["GND"] - 1, "… et broche 7 à la masse (GND). Inverser les deux détruit le CI en quelques secondes."),
        (S5["NC"] - 1, "Les entrées des portes 2, 3 et 4 ne servent pas : on les relie à GND. Une entrée CMOS ne reste jamais en l'air."),
        (S5["DEMO"], "Essai : la sortie 1Y vaut 1 seulement si A = 0 et C = 0, ceinture bouclée et frein enfoncé."),
        (S5["FIN"], "Le 74HC32 (OU) et le 74HC08 (ET) ont l'autre brochage : entrées sur les broches 1 et 2, sortie sur la broche 3."),
    ]))


# ================================================================ cartes et habillage
def ill_car(img, d, t):
    _, a, b, c, dd = SC[int(t / 1.6) % len(SC)]
    voiture(d, -5, 640, 100, a, b, c, dd, demarre(a, b, c, dd))


def ill_table(img, d, t):
    rows = [[(v >> 2) & 1, (v >> 1) & 1, v & 1, "?"] for v in range(8)]
    table(d, 200, 260, ["C", "B", "A", "S"], rows, 90, 58, int(t * 1.5) % 8, 28)


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
    text(d, (410, 545), "74HC02", 40, (235, 238, 245), True, mono=True, anchor="mm")
    d.pieslice((380, 300, 440, 360), 0, 180, fill=(30, 32, 44))


CARDS = [
    ("1", TOT, "Des 0 et des 1", "Le démarrage d'une voiture électrique", ill_car,
     "La voiture démarre si la ceinture est bouclée, le sélecteur sur P et la pédale de frein enfoncée.",
     "Comment un circuit décide-t-il d'allumer le voyant « démarrage » ?",
     "On traduit chaque capteur et le voyant en variable binaire : 1 ou 0.", "4 capteurs → 1 voyant S"),
    ("2", TOT, "Construire une table de vérité", "Toutes les combinaisons, dans l'ordre", ill_table,
     "Sans le mode service (D = 0), le démarrage dépend de trois capteurs : C, B et A.",
     "Comment être sûr de n'oublier aucun cas ?",
     "Une colonne par entrée, du poids fort au poids faible, et on compte en binaire.", "3 entrées → 8 lignes"),
    ("3", TOT, "Lire un chronogramme", "De l'analyseur logique à la table de vérité", ill_scope,
     "Au laboratoire, l'analyseur logique affiche les signaux A, B et S d'une porte.",
     "Comment relier ce que l'écran montre à la table de vérité ?",
     "On lit le chronogramme intervalle par intervalle, comme les lignes de la table.", "1 intervalle = 1 ligne"),
    ("4", TOT, "Les sept portes de base", "Symboles CEI, tables de vérité, équations", ill_gates,
     "Toute commande numérique est faite de quelques portes de base, combinées entre elles.",
     "Comment reconnaître chaque porte par son symbole, sa table ou son équation ?",
     "On fait passer les combinaisons B A dans chaque porte et on lit S.", "&   ≥1   =1   1"),
    ("5", TOT, "Du symbole au circuit intégré", "Câbler la porte NON-OU sur un 74HC02", ill_chip,
     "Sur breadboard, tu câbles le démarrage sur trois CI : 74HC02, 74HC32 et 74HC08.",
     "Sur quelles broches brancher A, C, la sortie et l'alimentation ? Où est le piège ?",
     "On lit le brochage du 74HC02 et on relie chaque signal à sa broche.", "74HC02 : broches 2 et 3 → 1"),
]
CARD_DUR = 13.0

s_intro = intro_scene("TEST ET MESURE 1 – EL DT 1 · ANIMATION 125", "Portes logiques et tables de vérité",
                      "Des 0 et des 1, sept portes, quatre façons de les décrire",
                      [("1", "Des 0 et des 1", "le démarrage d'une voiture électrique"), ("2", "Construire une table de vérité", "C B A, du poids fort au poids faible"),
                       ("3", "Lire un chronogramme", "un intervalle = une ligne"), ("4", "Les sept portes de base", "symboles CEI"),
                       ("5", "Du symbole au circuit intégré", "câbler un 74HC02")],
                      "Théorie : Floyd, chap. 3, 3-1 à 3-6 (p. 112-138) · nextecmedia 1.1 et 1.2.1")

s_outro = outro_scene(
    [("Variable", "1 ou 0 ; un capteur peut être actif à 0 (ceinture, frein)"), ("Table", "entrées du poids fort au poids faible, 2ⁿ lignes, comptage binaire"),
     ("Chronogramme", "chaque intervalle correspond à une ligne de la table"), ("7 portes", "NON, ET, OU, NON-ET, NON-OU, OU exclusif, NON-OU exclusif"),
     ("CI", f"74HC02{NB}NON-OU, 74HC32{NB}OU, 74HC08{NB}ET ; sur le 74HC02, la sortie 1Y est la broche{NB}1")],
    "À toi de jouer",
    [("Fiche 130 EX, partie A", "les sept portes : table, équation, chronogramme", ""), ("Fiche 130 EX, N°1", "le démarrage : du cahier des charges à la table", ""),
     ("Fiche 130 EX, N°2 et N°3", "chronogrammes, reconnaître une porte", ""), ("Fiche 130 EX, N°4", "câbler le démarrage sur trois CI", ""),
     ("Floyd, chap. 3, 3-1 à 3-6", "Inverseur à NON-OU exclusif", "p. 112-138"), ("Page interactive 121", "exercices sur des cas réels", "")],
    "Les liens du Floyd, de nextecmedia et de la présentation 120 sont dans la fiche 130 EX.")

SCENES = [(s_intro, 9.0), (make_card(CARDS, 0, CARD_DUR), CARD_DUR), (s_car, 58.0), (make_card(CARDS, 1, CARD_DUR), CARD_DUR), (s_table, 54.0),
          (make_card(CARDS, 2, CARD_DUR), CARD_DUR), (s_chrono, 44.0), (make_card(CARDS, 3, CARD_DUR), CARD_DUR), (s_gates, 75.0),
          (make_card(CARDS, 4, CARD_DUR), CARD_DUR), (s_ic, 54.0), (s_outro, 15.0)]

def produire(ctx):
    render(SCENES, ctx.sortie_de("125"))
    from moteur import voix                       # voix off calée sur 125-narration.md (demande de Gaël, 11/27/2026)
    voix.produire(os.path.join(ICI, "125-narration.md"), ctx.sortie_de("125"))


if __name__ == "__main__":
    # aperçu d'une image : python3 contenus/tm1/semaine-1/125-anim.py <scène> <t> [image.png]
    i, t = int(sys.argv[1]), float(sys.argv[2])
    frame_at(SCENES, i, t).save(sys.argv[3] if len(sys.argv) > 3 else f"apercu_125.png")
