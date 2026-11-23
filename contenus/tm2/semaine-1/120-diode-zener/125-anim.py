# -*- coding: utf-8 -*-
"""125 Diode et diode Zener – animation (TM2 – El Dim 4, semaine 1, va avec la présentation 120, la page 121 et la fiche 130).
Quatre démonstrations reprises de la présentation : la jonction PN, la caractéristique, la Zener, la LED.
Modèles des courbes identiques à figures.py. Niveau voulu par Gaël : expliquer (C2).
Rendu : python3 build.py tm2/semaine-1/120-diode-zener --seulement animations · aperçu : voir en bas"""
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))   # aperçu direct
from moteur.anim import *

FOOT[0] = "Test et Mesure 2 – El Dim 4 · 125 Diode et diode Zener"
TOT = "4"
X0, X1 = 60, BAND_X - 50          # zone utile
INK = (29, 33, 64)


# ================================================================ modèles (identiques à figures.py)
def u_diode(i): return 1.9 * 0.02585 * math.log(i / 10e-9 + 1) + 2.0 * i


def i_diode(u):
    if u <= 0: return 0.0
    a, b = 0.0, 1.0
    for _ in range(60):
        m = (a + b) / 2
        a, b = (a, m) if u_diode(m) > u else (m, b)
    return a


def u_zener(i): return 5.05 + 10 * i - 0.08 * math.exp(-i / 1e-3)


def i_zener(ue, r=2200):
    if ue <= u_zener(0): return 0.0
    a, b = 0.0, 0.2
    for _ in range(60):
        m = (a + b) / 2
        a, b = (a, m) if r * m + u_zener(m) > ue else (m, b)
    return a


def vir(x, n=2): return f"{x:.{n}f}".replace(".", ",")


# ================================================================ briques de dessin
def lab(d, xy, base, sub, size, color=NAVY, italic=True, bold=False, anchor="lm"):
    """Grandeur avec indice droit (U avec F en indice) ; anchor « lm » (gauche) ou « rm » (droite). Renvoie la largeur."""
    fb, fs = F(size, bold, italic=italic), F(size * 0.68, bold)
    w = fb.getlength(base) + fs.getlength(sub)
    x, y = xy
    if anchor == "rm": x -= w
    if anchor == "mm": x -= w / 2
    d.text((x, y), base, font=fb, fill=color, anchor="lm")
    d.text((x + fb.getlength(base), y + size * 0.28), sub, font=fs, fill=color, anchor="lm")
    return w


def trou(d, x, y, r=15, a=1.0):
    d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE, outline=mix(WHITE, RED, a), width=4)
    text(d, (x, y - 1), "+", int(r * 1.4), mix(WHITE, RED, a), True, anchor="mm")


def electron(d, x, y, r=15, a=1.0):
    d.ellipse((x - r, y - r, x + r, y + r), fill=mix(WHITE, BLUE, a), outline=mix(WHITE, NAVY, a), width=3)
    text(d, (x, y - 2), "−", int(r * 1.5), WHITE, True, anchor="mm")


def porteurs(d, x0, x1, y0, y1, genre, graine, dx=0.0, pas=56):
    cols, rows = max(1, int((x1 - x0 - 20) // pas)), max(1, int((y1 - y0 - 20) // pas))
    larg = cols * pas
    for c in range(cols):
        for r in range(rows):
            h = (math.sin(graine * 12.9898 + (c * 7 + r) * 78.233) * 43758.5453) % 1
            if h > 0.55: continue
            x = x0 + 10 + pas / 2 + c * pas + (h - 0.27) * 16
            y = y0 + 10 + pas / 2 + r * pas + (h - 0.27) * 14
            if dx: x = x0 + 10 + ((x - x0 - 10) + dx) % larg
            (trou if genre == "trou" else electron)(d, x, y)


def jonction(d, x, y, w, h, k, t=0.0, flux=False):
    zw, xm = 110 * k, x + w / 2
    xg, xd = xm - zw / 2, xm + zw / 2
    dx = t * 70 if flux else 0.0
    d.rectangle((x, y, xg, y + h), fill=TINT); d.rectangle((xd, y, x + w, y + h), fill=LBLUE)
    d.rectangle((xg, y, xd, y + h), fill=WHITE)
    for yy in range(int(y), int(y + h), 18): d.line((xg, yy, xg, yy + 9), fill=GREY, width=2); d.line((xd, yy, xd, yy + 9), fill=GREY, width=2)
    xi = max(zw * 0.25, 20)                              # demi-écart des ions : jamais collés aux porteurs
    porteurs(d, x, min(xg, xm - xi - 30), y, y + h, "trou", 3, dx)
    porteurs(d, max(xd, xm + xi + 30), x + w, y, y + h, "e", 5, -dx)
    for j in range(3):
        yy = y + 50 + j * (h - 100) / 2
        for xx, s_, c in ((xm - xi, "−", NAVY), (xm + xi, "+", RED)):
            d.rectangle((xx - 15, yy - 15, xx + 15, yy + 15), fill=WHITE, outline=c, width=3)
            text(d, (xx, yy - 1), s_, 26, c, True, anchor="mm")
    d.rectangle((x, y, x + w, y + h), outline=NAVY, width=4)
    text(d, (x + 8, y - 34), "zone p", 34, NAVY, True); text(d, (x + w - 8, y - 34), "zone n", 34, NAVY, True, anchor="ra")
    return xg, xd


def pile(d, x, y, w, yb, direct):
    """Fils des extrémités du barreau vers une pile placée sous le barreau ; trait long et fin = +."""
    cx = x + w / 2
    d.line([(x, y), (x - 30, y), (x - 30, yb), (cx - 34, yb)], fill=INK, width=5)
    d.line([(x + w, y), (x + w + 30, y), (x + w + 30, yb), (cx + 34, yb)], fill=INK, width=5)
    xp, xn = (cx - 34, cx + 34) if direct else (cx + 34, cx - 34)
    d.line((xp, yb - 44, xp, yb + 44), fill=INK, width=5); d.rectangle((xn - 7, yb - 24, xn + 7, yb + 24), fill=INK)
    text(d, (xp, yb - 70), "+", 44, RED, True, anchor="mm"); text(d, (xn, yb - 70), "−", 44, NAVY, True, anchor="mm")


def diode_v(d, x, y1, y2, sens="bas", genre="diode", t=30, col=INK):
    ym, s = (y1 + y2) / 2, (1 if sens == "bas" else -1)
    ya, yk = ym - s * t, ym + s * t
    d.line((x, y1, x, y2), fill=col, width=6)
    d.polygon([(x - t, ya), (x + t, ya), (x, yk)], fill=WHITE, outline=col, width=6)
    d.line((x, ya, x, yk), fill=col, width=6)
    d.line((x - t, yk, x + t, yk), fill=col, width=8)
    if genre == "zener": d.line((x + t, yk, x + t, yk - s * 16), fill=col, width=8)
    if genre == "led":
        for dd in (0, 24):
            x0, y0 = x + t + 8, ym - 4 + dd
            arrow(d, (x0, y0), (x0 + 34, y0 - 26), col, 4)


def resist_v(d, x, y1, y2, nom, val):
    ym = (y1 + y2) / 2
    d.line((x, y1, x, y2), fill=INK, width=6)
    d.rectangle((x - 20, ym - 52, x + 20, ym + 52), fill=WHITE, outline=INK, width=6)
    lab(d, (x - 40, ym - 18), nom, "1", 38, NAVY, anchor="rm")
    text(d, (x - 40, ym + 30), val, 32, GREY, anchor="rm")


def source_v(d, x, y1, y2, val):
    ym = (y1 + y2) / 2
    d.line((x, y1, x, y2), fill=INK, width=6)
    d.ellipse((x - 40, ym - 40, x + 40, ym + 40), fill=WHITE, outline=INK, width=6)
    d.line((x, ym - 40, x, ym + 40), fill=INK, width=6)
    text(d, (x - 56, ym), val, 34, GREY, anchor="rm")
    text(d, (x - 30, y1 + 46), "+", 40, RED, True, anchor="mm")


def fleche_u(d, x, yh, yb, base, sub=""):
    """Flèche de tension bleue du + (haut) vers le − (bas), nom à droite (REGLES 3.3)."""
    arrow(d, (x, yh + 10), (x, yb - 4), BLUE, 6)
    if sub: lab(d, (x + 18, (yh + yb) / 2), base, sub, 40, BLUE)
    else: text(d, (x + 18, (yh + yb) / 2), base, 40, BLUE, italic=True, anchor="lm")


def borne(d, x, y):
    d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=WHITE, outline=INK, width=5)


def noeud(d, x, y):
    d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=INK)


def bandeau(d, s, a, y=800):
    if a <= 0: return
    rbox(d, (X0, y, X1, y + 76), fill=mix(WHITE, NAVY, a), r=14)
    text(d, ((X0 + X1) / 2, y + 38), s, 34, mix(NAVY, WHITE, a), True, anchor="mm")


# ================================================================ 1 · la jonction PN
def s_jonction(img, d, t):
    chrome(img, d, "1 · LA JONCTION PN", "Sens direct, sens inverse", f"1/{TOT}")
    ref_pill(d, "présentation 120, diapos 3 à 5")
    x, y, w, h = 360, 250, 1000, 300
    k, direct, flux = 1.0, True, False
    if 10 <= t < 22: k, flux = 1 - 0.7 * prog(t, 10, 12.5), t > 12.5
    if t >= 22: direct, k = False, 1 + 1.6 * prog(t, 22, 24.5)
    xg, xd = jonction(d, x, y, w, h, k, t, flux)
    if t < 10:
        q = prog(t, 3, 4)
        if q > 0:
            arrow(d, (xg - 10, y + h + 50), (xd + 10, y + h + 50), mix(WHITE, NAVY, q), 4)
            arrow(d, (xd + 10, y + h + 50), (xg - 10, y + h + 50), mix(WHITE, NAVY, q), 4)
            text(d, ((xg + xd) / 2, y + h + 96), "zone de déplétion : plus de porteurs libres", 32, mix(WHITE, NAVY, q), True, anchor="mm")
    if t >= 10:
        pile(d, x, y + h / 2, w, y + h + 150, direct)
    if flux:
        q = prog(t, 12.5, 13.5)
        arrow(d, (x + 300, y - 80), (x + w - 300, y - 80), mix(WHITE, RED, q), 7)
        text(d, (x + w / 2, y - 120), "courant", 34, mix(WHITE, RED, q), True, anchor="mm")
    if 24 <= t < 34:
        q = prog(t, 24, 25)
        text(d, (x + w / 2, y - 100), "pas de courant", 38, mix(WHITE, NAVY, q), True, anchor="mm")
    bandeau(d, "Anode (zone p) vers cathode (zone n) : la diode conduit. Dans l'autre sens : elle bloque.", prog(t, 34, 35), 790)
    caption(d, cap_at(t, [(0, "Une zone p et une zone n dans le même cristal. À la frontière, il ne reste que des ions fixes."),
                          (10, "Sens direct : le + de la pile sur la zone p. La zone de déplétion devient mince."),
                          (14, "Au-dessus d'environ 0,7 V, les porteurs la traversent : le courant passe."),
                          (22, "Sens inverse : le + sur la zone n. La zone s'élargit : aucun courant ne passe."),
                          (34, "C'est le clapet anti-retour de l'électronique.")]))


# ================================================================ 2 · la caractéristique
def courbe_diode(d, x, y, w, h, u, marques=()):
    X = lambda v: x + w * v / 1.0
    Y = lambda i: y + h - h * min(i, 0.04) / 0.04
    for v in range(11):
        d.line((X(v / 10), y, X(v / 10), y + h), fill=LGREY, width=2)
        text(d, (X(v / 10), y + h + 30), vir(v / 10, 1), 28, GREY, anchor="mm")
    for i in range(0, 41, 5):
        d.line((x, Y(i / 1000), x + w, Y(i / 1000)), fill=LGREY, width=2)
        if i % 10 == 0: text(d, (x - 20, Y(i / 1000)), str(i), 28, GREY, anchor="rm")
    pts = []
    for kk in range(1001):
        v = kk / 1000; i = i_diode(v)
        if i > 0.04: break
        pts.append((X(v), Y(i)))
    d.line(pts, fill=BLUE, width=7, joint="curve")
    d.line((x, y + h, x + w, y + h), fill=INK, width=4); d.line((x, y, x, y + h), fill=INK, width=4)
    lab(d, (x + w - 120, y + h + 76), "U", "F", 36, NAVY); text(d, (x + w - 70, y + h + 76), "[V]", 34, NAVY, anchor="lm")
    lab(d, (x + 16, y - 30), "I", "F", 36, NAVY); text(d, (x + 50, y - 30), "[mA]", 34, NAVY, anchor="lm")
    for i, a in marques:
        if a <= 0: continue
        v = u_diode(i); col = mix(WHITE, RED, a)
        for k_ in range(0, int(X(v) - x), 24): d.line((x + k_, Y(i), x + min(k_ + 12, X(v) - x), Y(i)), fill=col, width=3)
        for k_ in range(0, int(y + h - Y(i)), 24): d.line((X(v), Y(i) + k_, X(v), Y(i) + min(k_ + 12, y + h - Y(i))), fill=col, width=3)
        text(d, (X(v) - 24, Y(i) - 30), f"{round(i * 1e3)} mA → {vir(v, 2)} V", 32, col, True, anchor="rm")
    if u is not None:
        i = i_diode(u)
        d.ellipse((X(u) - 15, Y(i) - 15, X(u) + 15, Y(i) + 15), fill=RED, outline=WHITE, width=3)


def s_carac(img, d, t):
    chrome(img, d, "2 · LA CARACTÉRISTIQUE", "Le courant en fonction de la tension", f"2/{TOT}")
    ref_pill(d, "présentation 120, diapos 7 à 9")
    u = None if t < 3 else (0.82 * prog(t, 3, 24) if t < 26 else None)
    courbe_diode(d, 220, 220, 980, 540, u, [(10e-3, prog(t, 26, 27)), (30e-3, prog(t, 28, 29))])
    if u is not None:
        i = i_diode(u)
        display(d, (1300, 260, 1700, 400), "tension", vir(u, 2) + " V", 54)
        display(d, (1300, 430, 1700, 570), "courant", ("≈ 0" if i < 1e-4 else vir(i * 1e3, 1)) + " mA", 54)
    q = prog(t, 30, 31)
    if q > 0:
        rbox(d, (1270, 300, 1720, 620), fill=mix(WHITE, TINT, q), r=16)
        text(d, (1300, 340), "Modèle avec seuil", 32, mix(TINT, BLUE, q), True)
        for kk, ln in enumerate(("Le courant triple,", "la tension monte", "d'à peine 0,1 V.")):
            text(d, (1300, 400 + kk * 46), ln, 32, mix(TINT, NAVY, q))
        lab(d, (1300, 560), "U", "F", 40, mix(TINT, NAVY, q), bold=True)
        text(d, (1360, 560), "≈ 0,7 V", 40, mix(TINT, NAVY, q), True, anchor="lm")
    caption(d, cap_at(t, [(0, "On augmente la tension de la diode au silicium et on lit son courant."),
                          (3, "Jusqu'à environ 0,6 V, presque pas de courant : la barrière de la jonction n'est pas franchie."),
                          (15, "Au-dessus du seuil, le courant monte très vite pour une petite hausse de tension."),
                          (26, "10 mA donnent 0,70 V ; 30 mA donnent 0,79 V. D'où le modèle : 0,7 V dès que la diode conduit."),
                          (34, "En sens inverse, une diode ordinaire bloque, jusqu'au claquage qui la détruit.")]))


# ================================================================ 3 · la Zener
def schema_zener(d, ox, oy, ue, us, iz):
    xs, xr, xo, yh, yn, yb = ox + 160, ox + 520, ox + 760, oy, oy + 230, oy + 470
    source_v(d, xs, yh, yb, vir(ue, 0) + " V"); fleche_u(d, xs + 70, yh + 70, yb - 70, "U", "e")
    d.line((xs, yh, xr, yh), fill=INK, width=6); d.line((xs, yb, xo, yb), fill=INK, width=6)
    resist_v(d, xr, yh, yn, "R", "2k2")
    diode_v(d, xr, yn, yb, "haut", "zener")
    text(d, (xr - 70, yn + 150), "5V1", 32, GREY, anchor="rm")
    d.line((xr, yn, xo, yn), fill=INK, width=6); noeud(d, xr, yn); noeud(d, xr, yb); borne(d, xo, yn); borne(d, xo, yb)
    fleche_u(d, xo + 50, yn + 20, yb - 20, "U", "s")
    text(d, (xo + 70, (yn + yb) / 2 + 56), vir(us, 2) + " V", 36, NAVY, True, anchor="lm")
    if iz > 5e-5:
        ym = (yn + yb) / 2
        for kk in range(0, 360, 20):
            a0, a1 = math.radians(kk), math.radians(kk + 10)
            d.arc((xr - 62, ym - 62, xr + 62, ym + 62), kk, kk + 10, fill=RED, width=5)
        text(d, (xr + 78, ym - 70), "elle conduit", 32, RED, True, anchor="lm")


def s_zener(img, d, t):
    chrome(img, d, "3 · LA DIODE ZENER", "Le claquage utilisé", f"3/{TOT}")
    ref_pill(d, "présentation 120, diapos 11 à 13")
    ue = 24 * prog(t, 4, 28)
    iz = i_zener(ue); us = u_zener(iz) if iz > 0 else ue
    schema_zener(d, 40, 220, ue, us, iz)
    x0, y0, w, h = 1150, 690, 560, 420
    X = lambda v: x0 + w * v / 24; Y = lambda v: y0 - h * v / 12
    d.line((x0, y0, x0 + w, y0), fill=INK, width=4); d.line((x0, y0, x0, y0 - h), fill=INK, width=4)
    for v in (0, 6, 12, 18, 24): text(d, (X(v), y0 + 26), str(v), 26, GREY, anchor="mm")
    for v, s_ in ((0, "0"), (5.1, "5,1"), (10, "10")): text(d, (x0 - 16, Y(v)), s_, 26, GREY, anchor="rm")
    for kk in range(0, w, 26): d.line((x0 + kk, Y(5.1), x0 + min(kk + 13, w), Y(5.1)), fill=GREY, width=2)
    lab(d, (x0 + w - 110, y0 + 62), "U", "e", 32, NAVY); text(d, (x0 + w - 66, y0 + 62), "[V]", 30, NAVY, anchor="lm")
    lab(d, (x0 + 14, y0 - h - 26), "U", "s", 32, NAVY); text(d, (x0 + 56, y0 - h - 26), "[V]", 30, NAVY, anchor="lm")
    pts, v = [], 0.0
    while v <= ue + 1e-9:
        i = i_zener(v); pts.append((X(v), Y(u_zener(i) if i > 0 else v))); v += 0.2
    if len(pts) > 1: d.line(pts, fill=RED, width=6, joint="curve")
    d.ellipse((X(ue) - 13, Y(us) - 13, X(ue) + 13, Y(us) + 13), fill=RED)
    bandeau(d, "Sous la tension Zener, la sortie suit l'entrée ; au-dessus, elle reste à environ 5,1 V.", prog(t, 33, 34), 820)
    caption(d, cap_at(t, [(0, "La protection d'entrée de l'équipement : R1 en série, une Zener 5V1 branchée en inverse."),
                          (4, "Sous 5,1 V, la Zener est bloquée : aucun courant, R1 ne prend rien. La sortie suit l'entrée."),
                          (12, "Au-dessus de 5,1 V, la Zener claque : elle conduit, et sa tension reste presque constante."),
                          (22, "C'est R1 qui prend la différence : à 24 V, environ 18,9 V. L'entrée du contrôleur est protégée."),
                          (33, "La Zener n'est pas détruite tant que sa puissance reste sous la limite de la fiche technique.")]))


# ================================================================ 4 · la LED
def schema_led(img, d, ox, oy, r, direct, i, casse, mot, col):
    xs, xb, yh, ym, yb = ox + 160, ox + 520, oy, oy + 230, oy + 470
    source_v(d, xs, yh, yb, "24 V"); fleche_u(d, xs + 70, yh + 70, yb - 70, "U")
    d.line((xs, yh, xb, yh), fill=INK, width=6); d.line((xs, yb, xb, yb), fill=INK, width=6)
    if r: resist_v(d, xb, yh, ym, "R", "2k2")
    else:
        d.line((xb, yh, xb, ym), fill=INK, width=6); text(d, (xb - 30, (yh + ym) / 2), "sans résistance", 32, RED, True, anchor="rm")
    if not casse and i > 0:
        g = clamp(i / 0.02, 0.2, 1)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((xb - 90, (ym + yb) / 2 - 90, xb + 90, (ym + yb) / 2 + 90), fill=col + (int(110 * g),))
        img.paste(Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB"))
    diode_v(d, xb, ym, yb, "bas" if direct else "haut", "led")
    lab(d, (xb - 120, (ym + yb) / 2), "D", "1", 38, NAVY, anchor="rm")
    if casse:
        c = ((ym + yb) / 2)
        d.line((xb - 60, c - 60, xb + 60, c + 60), fill=RED, width=10); d.line((xb + 60, c - 60, xb - 60, c + 60), fill=RED, width=10)
        text(d, (xb + 90, c + 10), mot, 36, RED, True, anchor="lm")


def s_led(img, d, t):
    chrome(img, d, "4 · LA LED", "Une diode qui éclaire", f"4/{TOT}")
    ref_pill(d, "présentation 120, diapos 14 et 15")
    r, direct = 2200, True
    if 10 <= t < 18: r = 0
    if 18 <= t < 26: direct = False
    casse = (11 <= t < 18) or (19.5 <= t < 26)
    i = 0 if not direct else (1.0 if r == 0 else (24 - 1.9) / r)
    schema_led(img, d, 40, 220, r, direct, i, casse, "détruite" if r == 0 else "claquage", (229, 57, 53))
    x0 = 1060
    if t < 10 or t >= 26:
        display(d, (x0, 260, x0 + 420, 400), "courant", vir((24 - 1.9) / 2200 * 1e3, 1) + " mA", 54)
    if 18 <= t < 26:
        rbox(d, (x0, 260, X1, 420), fill=PINK, r=16)
        text(d, (x0 + 30, 300), "24 V en inverse", 36, RED, True)
        text(d, (x0 + 30, 360), "limite de la LED : 5 V", 34, RED)
    q = prog(t, 27, 28)
    if q > 0:
        rows = (("infrarouge", "≈ 1,3 V"), ("rouge", "≈ 1,9 V"), ("jaune", "≈ 2,1 V"), ("vert", "2,2 à 3 V"), ("bleu, blanc", "≈ 3,2 V"))
        rbox(d, (x0, 450, X1, 540 + 56 * len(rows) + 20), fill=mix(WHITE, TINT, q), r=16)
        text(d, (x0 + 30, 500), "Couleur", 30, mix(TINT, BLUE, q), True, anchor="lm"); lab(d, (x0 + 380, 500), "U", "F", 32, mix(TINT, BLUE, q), bold=True)
        for kk, (a, b) in enumerate(rows):
            text(d, (x0 + 30, 560 + 56 * kk), a, 32, mix(TINT, NAVY, q), anchor="lm")
            text(d, (x0 + 380, 560 + 56 * kk), b, 32, mix(TINT, NAVY, q), True, anchor="lm")
    caption(d, cap_at(t, [(0, "Une LED rouge et sa résistance de 2,2 kΩ sur 24 V : la LED prend environ 1,9 V et éclaire."),
                          (10, "Sans résistance, rien ne limite le courant : il dépasse vite la limite. La LED est détruite."),
                          (18, "LED à l'envers : elle bloque, mais elle reçoit 24 V en inverse. Sa limite est de 5 V : elle claque."),
                          (26, "La couleur dépend du matériau, et la tension directe avec elle : plus la lumière est bleue, plus elle est grande."),
                          (33, "À retenir : toujours une résistance en série, et jamais à l'envers sur plus de 5 V.")]))


# ================================================================ cartes, intro, fin
def ill_alim(img, d, t):
    rbox(d, (120, 380, 520, 720), fill=LGREY, outline=NAVY, width=4, r=12)
    text(d, (320, 450), "24 V", 60, NAVY, True, anchor="mm")
    for k_, (c, s_) in enumerate(((RED, "+"), (NAVY, "−"))):
        x = 230 + k_ * 180
        d.ellipse((x - 34, 560, x + 34, 628), fill=WHITE, outline=c, width=6); text(d, (x, 594), s_, 44, c, True, anchor="mm")
    a = 0.5 + 0.5 * math.sin(t * 3)
    text(d, (320, 780), "branchée à l'envers ?", 34, mix(WHITE, RED, a), True, anchor="mm")


def ill_mesure(img, d, t):
    rbox(d, (180, 330, 560, 820), fill=(250, 200, 40), outline=NAVY, width=5, r=26)
    display(d, (220, 380, 520, 520), "", vir(0.6 + 0.1 * (0.5 + 0.5 * math.sin(t)), 2) + " V", 60)
    d.ellipse((290, 600, 450, 760), fill=LGREY, outline=NAVY, width=5)
    d.line((370, 680, 370 + 60 * math.cos(-0.8), 680 + 60 * math.sin(-0.8)), fill=NAVY, width=8)


def ill_capteur(img, d, t):
    rbox(d, (90, 420, 330, 640), fill=TINT, outline=NAVY, width=4, r=14); text(d, (210, 530), "capteur", 34, NAVY, True, anchor="mm")
    rbox(d, (470, 420, 720, 640), fill=(60, 140, 90), outline=NAVY, width=4, r=14); text(d, (595, 530), "contrôleur", 32, WHITE, True, anchor="mm")
    d.line((330, 530, 470, 530), fill=NAVY, width=6)
    text(d, (400, 480), "0 à 24 V", 30, RED, True, anchor="mm"); text(d, (595, 690), "5 V au plus", 30, NAVY, True, anchor="mm")


def ill_voyants(img, d, t):
    rbox(d, (120, 380, 680, 760), fill=LGREY, outline=NAVY, width=4, r=12)
    for k_, c in enumerate(((229, 57, 53), (242, 183, 5), (47, 111, 228))):
        on = math.sin(t * 2 + k_ * 2) > -0.3
        x = 240 + k_ * 160
        d.ellipse((x - 44, 520, x + 44, 608), fill=c if on else mix(WHITE, c, 0.3), outline=NAVY, width=4)
    text(d, (400, 690), "voyants de l'équipement", 32, NAVY, True, anchor="mm")


CARDS = [
    ("1", TOT, "La jonction PN", "Sens direct, sens inverse", ill_alim,
     "Sur la ligne, quelqu'un peut brancher l'alimentation 24 V de l'équipement de test à l'envers.",
     "Pourquoi une diode laisse-t-elle passer le courant dans un sens seulement ?",
     "On branche une pile sur une jonction PN, dans un sens puis dans l'autre.", "anode → cathode : elle conduit"),
    ("2", TOT, "La caractéristique", "Seuil, conduction, claquage", ill_mesure,
     "En pratique (TM2-A1), tu relèves la caractéristique d'une diode au silicium.",
     "Combien de volts prend une diode qui conduit ?",
     "On augmente la tension et on suit le courant sur la courbe.", "silicium : environ 0,7 V"),
    ("3", TOT, "La diode Zener", "Le claquage utilisé", ill_capteur,
     "Un capteur de la ligne envoie 0 à 24 V ; l'entrée du contrôleur accepte 5 V au plus.",
     "Comment limiter la tension d'une entrée avec une seule diode ?",
     "On monte la tension du capteur et on regarde la sortie.", "la sortie s'arrête à 5,1 V"),
    ("4", TOT, "La LED", "Une diode qui éclaire", ill_voyants,
     "L'extension de l'équipement de test a besoin de voyants.",
     "Comment allumer une LED sans la détruire ?",
     "On retire la résistance, puis on retourne la LED.", "toujours une résistance en série"),
]
CARD_DUR = 12.0

s_intro = intro_scene("TEST ET MESURE 2 – EL DIM 4 · ANIMATION 125", "La diode et la diode Zener",
                      "et la LED : trois composants à jonction PN",
                      [("1", "La jonction PN", "sens direct, sens inverse"), ("2", "La caractéristique", "seuil, conduction, claquage"),
                       ("3", "La diode Zener", "le claquage utilisé"), ("4", "La LED", "la jonction qui éclaire")],
                      "Va avec la présentation 120, la page interactive 121 et la fiche 130")

s_outro = outro_scene(
    [("Jonction", "anode vers cathode : elle conduit ; dans l'autre sens : elle bloque"),
     ("Seuil", "silicium : environ 0,7 V dès que la diode conduit"),
     ("Zener", "branchée en inverse, sa tension reste à sa tension Zener (5,1 V pour une 5V1)"),
     ("LED", "toujours une résistance en série ; jamais à l'envers sur plus de 5 V")],
    "À toi de jouer",
    [("Fiche 130, N°1", "la LED s'allume-t-elle ?", ""), ("Fiche 130, N°2 et N°3", "la caractéristique, la fiche technique", ""),
     ("Fiche 130, N°4 et N°5", "la Zener : résistance dynamique et puissance", ""), ("Fiche 130, N°6", "l'équipement de test", ""),
     ("Page interactive 121", "quatre étapes, corrigées tout de suite", "")],
    "Prochaine étape : les circuits avec diodes et LED, et le calcul de la résistance série (présentation 140).")

SCENES = [(s_intro, 9.0), (make_card(CARDS, 0, CARD_DUR), CARD_DUR), (s_jonction, 40.0), (make_card(CARDS, 1, CARD_DUR), CARD_DUR), (s_carac, 40.0),
          (make_card(CARDS, 2, CARD_DUR), CARD_DUR), (s_zener, 40.0), (make_card(CARDS, 3, CARD_DUR), CARD_DUR), (s_led, 38.0), (s_outro, 15.0)]


def produire(ctx):
    render(SCENES, ctx.sortie_de("125"))


if __name__ == "__main__":
    # aperçu d'une image : python3 contenus/tm2/semaine-1/120-diode-zener/125-anim.py <scène> <t> [image.png]
    i, t = int(sys.argv[1]), float(sys.argv[2])
    frame_at(SCENES, i, t).save(sys.argv[3] if len(sys.argv) > 3 else "apercu_125.png")
