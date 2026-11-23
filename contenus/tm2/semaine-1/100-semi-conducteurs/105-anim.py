# -*- coding: utf-8 -*-
"""105 Semi-conducteurs – animation (TM2 – El Dim 4, semaine 1, va avec la présentation 100, la page 101 et la fiche 110).
Quatre démonstrations reprises de la présentation : trois familles, le cristal et la chaleur, le champ électrique, le dopage.
Niveau voulu par Gaël : comprendre et savoir que ça existe, sans calcul.
Rendu : python3 build.py tm2/semaine-1/100-semi-conducteurs --seulement animations · aperçu : voir en bas"""
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))   # aperçu direct
from moteur.anim import *

FOOT[0] = "Test et Mesure 2 – El Dim 4 · 105 Semi-conducteurs"
TOT = "4"
X0, X1 = 60, BAND_X - 50          # zone utile


# ================================================================ briques de dessin
def electron(d, x, y, r=16, alpha=1.0):
    d.ellipse((x - r, y - r, x + r, y + r), fill=mix(WHITE, BLUE, alpha), outline=mix(WHITE, NAVY, alpha), width=3)
    text(d, (x, y - 2), "−", int(r * 1.5), mix(WHITE, WHITE, alpha), True, anchor="mm")


def trou(d, x, y, r=16, alpha=1.0):
    d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE, outline=mix(WHITE, RED, alpha), width=4)
    text(d, (x, y - 1), "+", int(r * 1.4), mix(WHITE, RED, alpha), True, anchor="mm")


BONDS = [(1, 1, "h"), (0, 0, "v"), (1, 0, "h"), (2, 1, "v"), (0, 2, "h"), (1, 1, "v"), (0, 1, "h"), (2, 0, "v"), (1, 2, "h"), (0, 1, "v"), (0, 0, "h"), (1, 0, "v")]


def cristal(d, ox, oy, s, t=0.0, pairs=0, centre="Si", alpha=1.0):
    """Cristal de silicium à plat, 3 × 3 atomes ; pairs = liaisons rompues ; centre = Si, P (électron en trop) ou B (trou)."""
    eb = s * 0.05
    P = lambda i, j: (ox + i * s, oy + j * s)
    ecol, lcol = mix(WHITE, BLUE, alpha), mix(WHITE, GREY, alpha)

    def e(x, y):
        d.ellipse((x - eb, y - eb, x + eb, y + eb), fill=ecol)
    for i in range(3):
        for j in range(3):
            x, y = P(i, j)
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if 0 <= i + dx < 3 and 0 <= j + dy < 3:
                    continue
                d.line((x, y, x + dx * s * 0.42, y + dy * s * 0.42), fill=lcol, width=3)
                e(x + dx * s * 0.3 - dy * s * 0.065, y + dy * s * 0.3 + dx * s * 0.065)
                e(x + dx * s * 0.3 + dy * s * 0.065, y + dy * s * 0.3 - dx * s * 0.065)
    rompues = {BONDS[k] for k in range(pairs)}
    if centre == "B":
        rompues.add((1, 1, "h"))
    trous, libres = [], []
    for i in range(3):
        for j in range(3):
            for k, dx, dy in (("h", 1, 0), ("v", 0, 1)):
                if i + dx > 2 or j + dy > 2:
                    continue
                (x0, y0), (x1, y1) = P(i, j), P(i + dx, j + dy)
                mx, my, nx, ny = (x0 + x1) / 2, (y0 + y1) / 2, -dy * s * 0.065, dx * s * 0.065
                d.line((x0, y0, x1, y1), fill=lcol, width=3)
                e(mx + nx, my + ny)
                if (i, j, k) in rompues:
                    trous.append((mx - nx, my - ny))
                    if not (centre == "B" and (i, j, k) == (1, 1, "h")):
                        libres.append((mx, my, len(libres)))
                else:
                    e(mx - nx, my - ny)
    for x, y in trous:
        trou(d, x, y, s * 0.075, alpha)
    for i in range(3):
        for j in range(3):
            x, y = P(i, j)
            sym = centre if (i, j) == (1, 1) else "Si"
            r = s * 0.2
            d.ellipse((x - r, y - r, x + r, y + r), fill=mix(WHITE, BLUE if sym != "Si" else NAVY, alpha))
            text(d, (x, y), sym, int(s * 0.17), WHITE, True, anchor="mm")
    if centre == "P":
        libres.append((ox + s * 1.5, oy + s * 0.5, 7))
    for x, y, k in libres:
        electron(d, x + math.sin(t * 2.1 + k) * s * 0.18, y - s * 0.2 + math.cos(t * 1.7 + k * 1.3) * s * 0.14, s * 0.08, alpha)


def thermo(d, x, y, h, th, tmin=20, tmax=60):
    f = clamp((th - tmin) / (tmax - tmin)); hh = h * (0.1 + 0.9 * f)
    d.rounded_rectangle((x - 18, y, x + 18, y + h), radius=18, fill=WHITE, outline=NAVY, width=4)
    d.rounded_rectangle((x - 9, y + h - hh, x + 9, y + h), radius=9, fill=RED)
    d.ellipse((x - 34, y + h - 10, x + 34, y + h + 58), fill=RED, outline=NAVY, width=4)
    text(d, (x + 50, y + h - hh), f"{th:.0f}{NB}°C", 40, NAVY, True, anchor="lm")


def barre(d, x, y, w, f, col, h=26):
    d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=LGREY)
    if f > 0.01:
        d.rounded_rectangle((x, y, x + max(h, w * clamp(f)), y + h), radius=h // 2, fill=col)


def bandeau(d, s, a, y=800):
    if a <= 0: return
    rbox(d, (X0, y, X1, y + 76), fill=mix(WHITE, NAVY, a), r=14)
    text(d, ((X0 + X1) / 2, y + 38), s, 34, mix(NAVY, WHITE, a), True, anchor="mm")


# ================================================================ 1 · trois familles
def s_familles(img, d, t):
    chrome(img, d, "1 · TROIS FAMILLES DE MATÉRIAUX", "Conducteur, semi-conducteur, isolant", f"1/{TOT}")
    ref_pill(d, "présentation 100, diapos 3 à 5")
    xa, xb, y = 120, 1700, 300
    X = lambda e: xa + (xb - xa) * (e + 9) / 25
    for k, (a, b, c, n) in enumerate([(-9, -5, LBLUE, "Conducteurs"), (-5, 8, TINT, "Semi-conducteurs"), (8, 16, LGREY, "Isolants")]):
        p = prog(t, 1 + k, 2 + k)
        if p <= 0: continue
        d.rectangle((X(a), y, X(b), y + 80), fill=mix(WHITE, c, p))
        text(d, ((X(a) + X(b)) / 2, y + 40), n, 34, mix(WHITE, NAVY, p), True, anchor="mm")
    p = prog(t, 0.5, 1.5)
    d.line((xa, y + 100, xb, y + 100), fill=mix(WHITE, NAVY, p), width=3)
    for e in range(-9, 17, 4):
        d.line((X(e), y + 92, X(e), y + 108), fill=mix(WHITE, NAVY, p), width=3)
        text(d, (X(e) - 8, y + 138), "10", 28, mix(WHITE, NAVY, p), anchor="mm")
        text(d, (X(e) + 22, y + 124), ("−" if e < 0 else "") + str(abs(e)), 19, mix(WHITE, NAVY, p), anchor="mm")
    text(d, ((xa + xb) / 2, y + 180), "résistivité ρ [Ω·m]  ·  chaque graduation multiplie par 10 000", 26, mix(WHITE, GREY, p), italic=True, anchor="mm")
    for n, e, t0 in (("cuivre", -7.75, 5), ("silicium pur", 3.36, 8), ("porcelaine", 12, 11)):
        q = prog(t, t0, t0 + 1)
        if q <= 0: continue
        d.line((X(e), y - 50 + 20 * (1 - q), X(e), y), fill=mix(WHITE, BLUE, q), width=6)
        head(d, (X(e), y), math.pi / 2, mix(WHITE, BLUE, q), 22)
        text(d, (X(e), y - 75), n, 34, mix(WHITE, NAVY, q), True, anchor="mm")
    f = prog(t, 18, 19.5)
    if f > 0:
        for k, (n, nb_, lab) in enumerate((("Métal", 40, "beaucoup d'électrons libres"), ("Semi-conducteur", 4, "très peu"), ("Isolant", 0, "aucun"))):
            bx, by, bw = 60 + k * 570, 540, 530
            rbox(d, (bx, by, bx + bw, by + 230), fill=mix(WHITE, PALE, f), outline=mix(WHITE, LGREY, f), width=3, r=16)
            text(d, (bx + 24, by + 34), n, 34, mix(WHITE, NAVY, f), True, anchor="lm")
            text(d, (bx + bw - 24, by + 34), lab, 24, mix(WHITE, GREY, f), anchor="rm")
            for q in range(nb_):
                ex = bx + 40 + (q * 7919 % 97) / 97 * (bw - 80) + math.sin(t * 2.3 + q * 1.9) * 14
                ey = by + 90 + (q * 104729 % 89) / 89 * 120 + math.cos(t * 2.9 + q) * 10
                d.ellipse((ex - 9, ey - 9, ex + 9, ey + 9), fill=mix(WHITE, BLUE, f))
    bandeau(d, "Semi-conducteur : un matériau dont on peut régler la conduction", prog(t, 34, 35), 790)
    caption(d, cap_at(t, [(0, "La résistivité dit si un matériau conduit bien. L'échelle est logarithmique."),
                          (5, "Le cuivre conduit très bien, la porcelaine pas du tout. Le silicium est entre les deux."),
                          (18, "Pourquoi ? Le métal a beaucoup d'électrons libres, le silicium très peu, l'isolant aucun."),
                          (34, "Le silicium a 4 électrons de valence, tous pris dans des liaisons. Mais on peut en libérer.")]))


# ================================================================ 2 · cristal et chaleur
def s_cristal(img, d, t):
    chrome(img, d, "2 · LE CRISTAL DE SILICIUM", "Monocristal et chaleur", f"2/{TOT}")
    ref_pill(d, "présentation 100, diapos 6 et 7")
    th = 20 + 40 * prog(t, 12, 34)
    k = 2 ** ((th - 20) / 10)
    cristal(d, 260, 290, 220, t, 0 if t < 12 else min(8, max(1, int(k))), alpha=prog(t, 0.3, 1.5))
    if t > 10:
        a = prog(t, 10, 11)
        thermo(d, 1020, 250, 420, th)
        text(d, (1240, 300), "Porteurs libres", 34, mix(WHITE, NAVY, a), True, anchor="lm")
        text(d, (1240, 370), "× " + f"{k:.1f}".replace(".", ","), 64, mix(WHITE, BLUE, a), True, anchor="lm")
        text(d, (1240, 430), "par rapport à 20 °C", 24, mix(WHITE, GREY, a), anchor="lm")
        text(d, (1240, 520), "Résistance", 34, mix(WHITE, NAVY, a), True, anchor="lm")
        barre(d, 1240, 560, 440, 1 / k, RED)
    c = prog(t, 40, 41)
    if c > 0:
        rbox(d, (1180, 660, X1, 820), fill=mix(WHITE, TINT, c), r=14)
        text(d, (1210, 705), "Cuivre (métal) : R monte un peu.", 32, mix(TINT, NAVY, c), True, anchor="lm")
        text(d, (1210, 770), "Silicium : R baisse fortement.", 32, mix(TINT, BLUE, c), True, anchor="lm")
    caption(d, cap_at(t, [(0, "Chaque atome partage ses 4 électrons de valence avec 4 voisins. Tout est rangé : c'est un monocristal."),
                          (12, "On chauffe : une liaison se rompt. Un électron devient libre et laisse un trou, qui se comporte comme une charge +."),
                          (22, "Plus il fait chaud, plus il y a de paires électron-trou : environ deux fois plus tous les 10 °C."),
                          (34, "Le silicium pur conduit par ces paires : c'est la conduction intrinsèque. Très peu, à température ambiante."),
                          (40, "Dans un métal, c'est l'inverse : la résistance monte un peu quand il chauffe.")]))


# ================================================================ 3 · champ électrique
def s_champ(img, d, t):
    chrome(img, d, "3 · LE CHAMP ÉLECTRIQUE", "Électrons vers le +, trous vers le −", f"3/{TOT}")
    ref_pill(d, "présentation 100, diapo 8")
    xa, xb, ya, yb = 260, 1360, 260, 600
    on, fort, fet = t >= 8, 26 <= t < 38, t >= 38
    d.rounded_rectangle((xa, ya, xb, yb), radius=10, fill=TINT, outline=NAVY, width=4)
    d.rectangle((xa - 40, ya - 30, xa, yb + 30), fill=GREY); d.rectangle((xb, ya - 30, xb + 40, yb + 30), fill=GREY)
    if on and not fet:
        text(d, (xa - 20, ya - 70), "+", 64, RED, True, anchor="mm"); text(d, (xb + 20, ya - 70), "−", 64, NAVY, True, anchor="mm")
    n = 14 + min(18, int((t - 26) * 5)) if fort else 8
    w = xb - xa - 80
    for q in range(n):
        base = (q * 197) % w
        drift = (60 if not fort else 260) * (t - 8) if on and not fet else 0
        jit = math.sin(t * 3 + q * 1.7) * 26
        ex = xa + 40 + ((base - drift + jit) % w)
        ey = ya + 60 + (q * 37) % 110 + math.cos(t * 2.5 + q) * 10
        hx = xa + 40 + ((base * 1.3 + drift - jit) % w)
        hy = ya + 210 + (q * 41) % 90 + math.sin(t * 2.2 + q) * 10
        electron(d, ex, ey, 18); trou(d, hx, hy, 18)
    if on and not fet:
        text(d, (xb + 90, ya + 110), "électrons", 32, BLUE, True, anchor="lm"); text(d, (xb + 90, ya + 150), "vers le +", 32, BLUE, anchor="lm")
        text(d, (xb + 90, ya + 260), "trous", 32, RED, True, anchor="lm"); text(d, (xb + 90, ya + 300), "vers le −", 32, RED, anchor="lm")
        arrow(d, (xa + 200, 670), (xb - 200, 670), NAVY, 5)
        text(d, ((xa + xb) / 2, 715), "champ électrique et sens conventionnel du courant", 26, GREY, anchor="mm")
        text(d, (xa, 785), "Courant", 32, NAVY, True, anchor="lm")
        barre(d, xa + 160, 770, 700, 1.0 if fort else 0.25, RED if fort else BLUE, 30)
        if fort: text(d, (xa + 900, 785), "claquage !", 36, RED, True, anchor="lm")
    if fet:
        a = prog(t, 38, 39)
        rbox(d, (xa + 250, ya - 70, xb - 250, ya - 20), fill=mix(WHITE, NAVY, a), r=8)
        text(d, ((xa + xb) / 2, ya - 45), "grille (électrode isolée)", 28, WHITE, True, anchor="mm")
        text(d, ((xa + xb) / 2, 700), "FET : le champ de la grille commande la conduction", 36, mix(WHITE, NAVY, a), True, anchor="mm")
    caption(d, cap_at(t, [(0, "Sans tension, les électrons libres et les trous s'agitent dans tous les sens : pas de courant."),
                          (8, "Avec une tension, le champ pousse les électrons vers le + et les trous vers le −. Les deux courants s'additionnent."),
                          (26, "Champ très fort : les liaisons cèdent, le courant monte d'un coup. C'est le claquage, utilisé par la diode Zener."),
                          (38, "Un champ peut aussi commander la conduction : c'est le transistor à effet de champ (FET).")]))


# ================================================================ 4 · dopage
def s_dopage(img, d, t):
    chrome(img, d, "4 · LE DOPAGE", "Type n et type p", f"4/{TOT}")
    ref_pill(d, "présentation 100, diapo 9")
    centre = "Si" if t < 8 else ("P" if t < 22 else "B")
    if t < 36:
        cristal(d, 260, 280, 220, t, centre=centre)
    else:
        a = prog(t, 36, 37)
        cristal(d, 170, 300, 150, t, centre="P", alpha=a); cristal(d, 620, 300, 150, t, centre="B", alpha=a)
        text(d, (320, 680), "type n", 34, mix(WHITE, NAVY, a), True, anchor="mm"); text(d, (770, 680), "type p", 34, mix(WHITE, NAVY, a), True, anchor="mm")

    def boite(y, a, t1, t2, t3):
        rbox(d, (1060, y, X1, y + 200), fill=mix(WHITE, TINT, a), r=16)
        text(d, (1090, y + 45), t1, 38, mix(TINT, BLUE, a), True, anchor="lm")
        text(d, (1090, y + 105), t2, 30, mix(TINT, NAVY, a), anchor="lm")
        text(d, (1090, y + 160), t3, 30, mix(TINT, NAVY, a), True, anchor="lm")
    if t >= 8: boite(240, prog(t, 8, 9), "Type n : phosphore", "5 électrons de valence : 1 en trop", "majoritaires : électrons")
    if t >= 22: boite(470, prog(t, 22, 23), "Type p : bore", "3 électrons de valence : 1 trou", "majoritaires : trous")
    bandeau(d, "Les deux restent neutres · zone p + zone n = jonction PN = la diode", prog(t, 36, 37), 740)
    caption(d, cap_at(t, [(0, "Silicium pur : toutes les liaisons sont complètes. Doper, c'est remplacer très peu d'atomes par un autre élément."),
                          (8, "Phosphore : 5 électrons de valence. Quatre forment les liaisons, le cinquième devient libre. Type n."),
                          (22, "Bore : 3 électrons de valence. Il manque un électron pour la 4e liaison : il reste un trou. Type p."),
                          (36, "Le morceau reste neutre. Une zone p collée à une zone n forme une jonction PN : la diode.")]))


# ================================================================ cartes, introduction, récapitulatif
def ill_materiaux(img, d, t):
    d.rectangle((90, 480, 330, 540), fill=(200, 120, 60), outline=NAVY, width=3); text(d, (210, 580), "cuivre", 28, NAVY, True, anchor="mm")
    d.ellipse((370, 420, 530, 580), fill=(120, 128, 150), outline=NAVY, width=3); text(d, (450, 620), "silicium", 28, NAVY, True, anchor="mm")
    for k in range(4): d.ellipse((600, 420 + k * 40, 720, 450 + k * 40), fill=WHITE, outline=NAVY, width=3)
    text(d, (660, 620), "porcelaine", 28, NAVY, True, anchor="mm")


def ill_armoire(img, d, t):
    rbox(d, (120, 360, 520, 800), fill=LGREY, outline=NAVY, width=4, r=10)
    for k in range(3): rbox(d, (160, 400 + k * 120, 480, 490 + k * 120), fill=(60, 140, 90), outline=NAVY, width=2, r=6)
    thermo(d, 640, 420, 260, 20 + 40 * (0.5 + 0.5 * math.sin(t)))


def ill_pile(img, d, t):
    d.rounded_rectangle((120, 500, 640, 600), radius=8, fill=TINT, outline=NAVY, width=3)
    d.rectangle((100, 480, 120, 620), fill=GREY); d.rectangle((640, 480, 660, 620), fill=GREY)
    text(d, (110, 440), "+", 50, RED, True, anchor="mm"); text(d, (650, 440), "−", 50, NAVY, True, anchor="mm")
    for q in range(5): electron(d, 170 + ((q * 120 - t * 60) % 440), 530, 14); trou(d, 170 + ((q * 120 + t * 60) % 440), 575, 14)


def ill_wafer(img, d, t):
    d.ellipse((140, 340, 660, 860), fill=(150, 156, 176), outline=NAVY, width=4)
    for i in range(-3, 4):
        for j in range(-3, 4):
            if i * i + j * j <= 9: d.rectangle((400 + i * 60 - 24, 600 + j * 60 - 24, 400 + i * 60 + 24, 600 + j * 60 + 24), outline=NAVY, width=2)


CARDS = [
    ("1", TOT, "Trois familles de matériaux", "Conducteur, semi-conducteur, isolant", ill_materiaux,
     "Tu prépares l'extension de l'équipement de test de la ligne : fils, isolants et composants.",
     "Pourquoi les diodes et les transistors sont-ils faits d'un matériau qui conduit « à moitié » ?",
     "On range les matériaux selon leur résistivité, puis on regarde leurs électrons libres.", "conducteur · semi · isolant"),
    ("2", TOT, "Le cristal de silicium", "Monocristal et chaleur", ill_armoire,
     "En été, l'armoire de l'équipement de test passe de 20 °C à 60 °C.",
     "Que se passe-t-il dans le silicium des composants quand il chauffe ?",
     "On chauffe un cristal de silicium et on compte les porteurs libres.", "chaleur → paires électron-trou"),
    ("3", TOT, "Le champ électrique", "Électrons, trous et claquage", ill_pile,
     "On branche un barreau de silicium dopé sur une alimentation.",
     "Dans quel sens partent les électrons et les trous ? Et si la tension devient très forte ?",
     "On applique une tension, puis une tension beaucoup plus forte.", "électrons → +   ·   trous → −"),
    ("4", TOT, "Le dopage", "Type n et type p", ill_wafer,
     "À la fabrication des puces, on ajoute très peu d'atomes d'un autre élément au silicium.",
     "Comment un atome sur 50 millions peut-il changer la conduction ?",
     "On remplace un atome de silicium par du phosphore, puis par du bore.", "n : électrons · p : trous"),
]
CARD_DUR = 13.0

s_intro = intro_scene("TEST ET MESURE 2 – EL DIM 4 · ANIMATION 105", "Les semi-conducteurs",
                      "Le matériau de tous les composants électroniques",
                      [("1", "Trois familles de matériaux", "conducteur, semi-conducteur, isolant"), ("2", "Le cristal de silicium", "monocristal et chaleur"),
                       ("3", "Le champ électrique", "électrons, trous, claquage"), ("4", "Le dopage", "type n et type p")],
                      "Va avec la présentation 100, la page interactive 101 et la fiche 110")

s_outro = outro_scene(
    [("Familles", "conducteur, semi-conducteur, isolant : le comportement à la chaleur tranche"),
     ("Cristal", "monocristal ; pur, il conduit par paires électron-trou"),
     ("Chaleur", "plus de porteurs : la résistance du silicium baisse"),
     ("Champ", "électrons vers le +, trous vers le − ; champ très fort : claquage"),
     ("Dopage", "n : électrons majoritaires · p : trous majoritaires")],
    "À toi de jouer",
    [("Fiche 110, N°1", "classer des matériaux", ""), ("Fiche 110, N°2 et N°3", "le cristal et la chaleur", ""),
     ("Fiche 110, N°4", "le champ électrique", ""), ("Fiche 110, N°5", "le dopage", ""),
     ("Page interactive 101", "quatre étapes, corrigées tout de suite", "")],
    "Prochaine étape : la jonction PN, c'est-à-dire la diode (présentation 120).")

SCENES = [(s_intro, 9.0), (make_card(CARDS, 0, CARD_DUR), CARD_DUR), (s_familles, 44.0), (make_card(CARDS, 1, CARD_DUR), CARD_DUR), (s_cristal, 50.0),
          (make_card(CARDS, 2, CARD_DUR), CARD_DUR), (s_champ, 48.0), (make_card(CARDS, 3, CARD_DUR), CARD_DUR), (s_dopage, 46.0), (s_outro, 15.0)]


def produire(ctx):
    render(SCENES, ctx.sortie_de("105"))


if __name__ == "__main__":
    # aperçu d'une image : python3 contenus/tm2/semaine-1/100-semi-conducteurs/105-anim.py <scène> <t> [image.png]
    i, t = int(sys.argv[1]), float(sys.argv[2])
    frame_at(SCENES, i, t).save(sys.argv[3] if len(sys.argv) > 3 else "apercu_105.png")
