# -*- coding: utf-8 -*-
"""205 Algèbre de Boole – animation (TM1 – El DT 1, semaine 2, va avec la présentation 200 et la fiche 210 EX).
Sortie S, entrées A, B, C (REGLES 3.4). Tables : entrées du poids fort au poids faible (C B A). Symboles CEI 60617-12.
Rendu : python3 build.py tm1/semaine-2/200-algebre-boole --seulement animations · aperçu : voir en bas."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))   # aperçu direct
from moteur.anim import *

FOOT[0] = "Test et Mesure 1 – El DT 1 · 205 Algèbre de Boole"
TOT = "3"
NOT = lambda x: 1 - x


def over_eq(d, x, y, parts, size, color=NAVY, anchor_mid=False, alpha=1.0):
    """Équation : parts = [(texte, surligné ?)] ; renvoie la largeur."""
    f = F(size, True)
    total = sum(f.getlength(p) for p, _ in parts)
    if anchor_mid: x -= total / 2
    col = mix(WHITE, color, alpha)
    for p, ov in parts:
        w = f.getlength(p)
        text(d, (x, y), p, size, col, True, anchor="lm")
        if ov: d.line((x + 2, y - size * 0.62, x + w - 2, y - size * 0.62), fill=col, width=max(3, size // 14))
        x += w
    return total


def table(d, x, y, heads, rows, colw=90, rowh=56, size=28, outcols=1, show=None, bad=()):
    n = len(heads); W_ = colw * n
    rbox(d, (x, y, x + W_, y + rowh), fill=LBLUE, r=8)
    for j, h in enumerate(heads):
        text(d, (x + colw * j + colw / 2, y + rowh / 2), h, size - 4 if len(h) > 3 else size, NAVY, True, anchor="mm")
    d.line((x + colw * (n - outcols), y + 6, x + colw * (n - outcols), y + rowh * (len(rows) + 1) - 6), fill=NAVY, width=3)
    for i, r in enumerate(rows):
        yy = y + rowh * (i + 1)
        d.rectangle((x, yy, x + W_, yy + rowh), fill=PALE if i % 2 == 0 else WHITE)
        if show is not None and i >= show: continue
        for j, v in enumerate(r):
            out = j >= n - outcols
            col = (BLUE if v == 1 else NAVY) if out else NAVY
            text(d, (x + colw * j + colw / 2, yy + rowh / 2), str(v), size, col, out, mono=True, anchor="mm")
    d.rectangle((x, y, x + W_, y + rowh * (len(rows) + 1)), outline=NAVY, width=3)


def gate3(d, x, y, s=1.0, labels=("A", "B", "C"), neg_in=(), out_label=""):
    """ET à 3 entrées (74HC11) ; neg_in : entrées avec cercle de négation."""
    w, h, L = 150 * s, 220 * s, 70 * s
    ys = [y + h * f for f in (0.22, 0.5, 0.78)]
    for i, yy in enumerate(ys):
        wire(d, [(x - L, yy), (x, yy)], None, int(4 * s) + 1)
        text(d, (x - L - 10 * s, yy), labels[i], int(30 * s), NAVY, True, italic=True, anchor="rm")
    d.rectangle((x, y, x + w, y + h), fill=WHITE, outline=NAVY, width=max(3, int(5 * s)))
    text(d, (x + w / 2, y + 14 * s), "&", int(40 * s), NAVY, True, anchor="ma")
    wire(d, [(x + w, y + h / 2), (x + w + L, y + h / 2)], None, int(4 * s) + 1)
    if out_label: text(d, (x + w + L + 10 * s, y + h / 2), out_label, int(30 * s), NAVY, True, italic=True, anchor="lm")
    return [(x - L, yy) for yy in ys], (x + w + L, y + h / 2)


def neg_in(d, pt, s=1.0, lead=70):
    """Cercle de négation sur une entrée d'une porte de moteur/anim.gate (pt = début du fil d'entrée)."""
    r = 12 * s; x = pt[0] + lead * s - 2 * r
    d.ellipse((x, pt[1] - r, x + 2 * r, pt[1] + r), fill=WHITE, outline=NAVY, width=max(3, int(4 * s)))


# ================================================================ 1 · les règles sur une porte
RULES = [("OU", "0", "A", [("A + 0 = A", False)]), ("OU", "1", "1", [("A + 1 = 1", False)]),
         ("ET", "0", "0", [("A · 0 = 0", False)]), ("ET", "1", "A", [("A · 1 = A", False)]),
         ("OU", "A", "A", [("A + A = A", False)]), ("OU", "nA", "1", [("A + ", False), ("A", True), (" = 1", False)]),
         ("ET", "A", "A", [("A · A = A", False)]), ("ET", "nA", "0", [("A · ", False), ("A", True), (" = 0", False)])]
RCAP = ["Règle 1 : un OU avec une entrée à 0. La sortie suit A : l'entrée à 0 ne change rien.",
        "Règle 2 : un OU avec une entrée à 1. La sortie reste à 1, quelle que soit A.",
        "Règle 3 : un ET avec une entrée à 0. La sortie reste bloquée à 0.",
        "Règle 4 : un ET avec une entrée à 1. La porte laisse passer A : c'est un signal de validation.",
        "Règle 5 : A sur les deux entrées d'un OU. La sortie redonne A.",
        "Règle 6 : A et son inverse sur un OU. L'un des deux vaut toujours 1 : la sortie reste à 1.",
        "Règle 7 : A sur les deux entrées d'un ET. La sortie redonne A.",
        "Règle 8 : A et son inverse sur un ET. Ils ne valent jamais 1 en même temps : la sortie reste à 0."]
RD = 7.0


def s_rules(img, d, t):
    chrome(img, d, "1 · LES RÈGLES SUR UNE PORTE", "Une entrée à 0, à 1, ou reliée à A", f"1/{TOT}")
    if t < 8 * RD:
        k = int(t // RD); u = t - k * RD; a = 0 if (u % 3.5) < 1.75 else 1
        key, e2, res, eq = RULES[k]
        b = {"0": 0, "1": 1, "A": a, "nA": 1 - a}[e2]
        s = a & b if key == "ET" else a | b
        lab2 = {"0": "0", "1": "1", "A": "A", "nA": "Ā"}[e2]
        text(d, (260, 230), f"règle {k + 1}", 34, GREY, True)
        ins, out = gate(d, 400, 300, key, 1.6, (a, b), s, ("A", lab2), out_label="S")
        bitpill(d, (170, ins[0][1]), a, 34); bitpill(d, (170, ins[1][1]), b, 34)
        over_eq(d, 1080, 360, eq, 72)
        text(d, (1080, 470), f"A = {a}  →  S = {s}", 48, NAVY, mono=True, anchor="lm")
        text(d, (1080, 560), "S suit A." if res == "A" else f"S reste à {res}.", 40, BLUE if res != "A" else GREY, True, anchor="lm")
        for i in range(8):
            x = 260 + i * 160
            rbox(d, (x, 790, x + 140, 850), fill=BLUE if i == k else (WHITE if i > k else TINT), outline=LBLUE, width=3, r=10)
            text(d, (x + 70, 820), str(i + 1), 28, WHITE if i == k else NAVY, True, anchor="mm")
        caption(d, RCAP[k])
    else:   # règle 9 : deux inverseurs en série
        u = t - 8 * RD; a = 0 if (u % 3) < 1.5 else 1
        text(d, (260, 230), "règle 9", 34, GREY, True)
        i1, o1 = gate(d, 330, 360, "NON", 1.2, (a,), 1 - a, ("A",), out_label="")
        i2, o2 = gate(d, o1[0] + 84, 360, "NON", 1.2, (1 - a,), a, ("",), out_label="S")
        bitpill(d, (160, i1[0][1]), a, 34)
        over_eq(d, 1180, 420, [("A", True)], 72)
        d.line((1182, 420 - 72 * 0.62 - 14, 1180 + F(72, True).getlength("A") - 2, 420 - 72 * 0.62 - 14), fill=NAVY, width=5)
        text(d, (1180 + F(72, True).getlength("A") + 10, 420), " = A", 72, NAVY, True, anchor="lm")
        caption(d, "Règle 9 : deux inverseurs en série. Deux barres s'annulent : la sortie redonne A.")


# ================================================================ 2 · De Morgan
def dm_form(d, x, y, p, vers, size=110):
    """vers = "ET" : barre(A · B) → Ā + B̄ ; "OU" : barre(A + B) → Ā · B̄ ; p de 0 à 1."""
    xa, xo, xb = x, x + 150, x + 300
    text(d, (x - 280, y), "S =", size, NAVY, True, anchor="lm")
    text(d, (xa, y), "A", size, NAVY, True, italic=True, anchor="mm")
    text(d, (xb, y), "B", size, NAVY, True, italic=True, anchor="mm")
    o1, o2 = ("·", "+") if vers == "ET" else ("+", "·")
    q = prog(p, 0.45, 0.75)
    text(d, (xo, y), o1, size, mix(WHITE, NAVY, 1 - q), True, anchor="mm")
    text(d, (xo, y), o2, size, mix(WHITE, BLUE, q), True, anchor="mm")
    c = prog(p, 0.0, 0.45); yb = y - size * 0.62
    d.line((xa - 40, yb, xa + 40 + (xb - xa) * (1 - c), yb), fill=NAVY, width=8)
    d.line((xb - 40 - (xb - xa) * (1 - c), yb, xb + 40, yb), fill=NAVY, width=8)


def s_morgan(img, d, t):
    chrome(img, d, "2 · LE THÉORÈME DE DE MORGAN", "Casse la barre, change le signe", f"2/{TOT}")
    if t < 26:
        vers = "ET" if t < 13 else "OU"
        p = prog(t, 3 if vers == "ET" else 16, 9 if vers == "ET" else 22)
        dm_form(d, 760, 420, p, vers)
        if p > 0.75: text(d, (880, 620), "casse la barre, change le signe", 46, BLUE, True, anchor="mm")
        caption(d, cap_at(t, [(0, "Première forme : la barre couvre A · B, toute l'expression."),
                              (3, "On casse la barre : chaque variable garde sa propre barre, et le point devient un plus."),
                              (13, "Seconde forme : la barre couvre A + B."),
                              (16, "On la casse, et le plus devient un point. « Ni A ni B » : c'est l'autorisation des arrêts d'urgence.")]))
    else:
        u = t - 26
        rows = [[b, a, NOT(a & b), NOT(a) | NOT(b)] for b in (0, 1) for a in (0, 1)]
        table(d, 120, 230, ["B", "A", "(A·B)'", "Ā + B̄"], rows, colw=140, rowh=74, show=int(clamp((u - 1) / 1.2, 0, 4)), outcols=2)
        # remplace l'en-tête (A·B)' par une vraie barre
        d.rectangle((120 + 2 * 140 + 4, 234, 120 + 3 * 140 - 4, 300), fill=LBLUE)
        over_eq(d, 120 + 2.5 * 140, 267, [("A · B", True)], 28, anchor_mid=True)
        q = prog(u, 7, 8)
        if q > 0:
            ins, out = gate(d, 960, 260, "NON-ET", 1.0, labels=("A", "B"), out_label="S", alpha=q)
            text(d, (1330, 355), "=", 80, mix(WHITE, BLUE, q), True, anchor="mm")
            ins2, out2 = gate(d, 1480, 260, "OU", 1.0, labels=("A", "B"), out_label="S", alpha=q)
            if q > 0.5:
                for pt in ins2: neg_in(d, pt)
            text(d, (1300, 560), "NON-ET  =  OU aux entrées inversées", 40, mix(WHITE, NAVY, q), True, anchor="mm")
        caption(d, cap_at(u, [(0, "Contrôle par la table : les deux colonnes de droite sont identiques sur les quatre lignes."),
                              (7, "Sur un schéma, les deux dessins représentent la même porte. Le cercle à l'entrée signale une entrée active à 0."),
                              (13, "Avec De Morgan, on peut tout construire avec un seul type de porte : le 74HC00 et ses quatre NON-ET.")]))


# ================================================================ 3 · le convoyeur : simplifier, contrôler, dessiner
CONV = lambda c, b, a: (a & b) | (a & NOT(b) & c)
SIMP = lambda c, b, a: a & (b | c)
STEPS = [(8, [("S = A · B + A · ", False), ("B", True), (" · C", False)], ""),
         (20, [("S = A · (B + ", False), ("B", True), (" · C)", False)], "distributivité : A est commun"),
         (32, [("S = A · (B + C)", False)], "règle 11")]


def s_conv(img, d, t):
    chrome(img, d, "3 · LE CONVOYEUR DE SORTIE", "Simplifier, contrôler, dessiner", f"3/{TOT}")
    if t < 8:
        q = prog(t, 0.3, 1.3)
        para(d, (120, 230), "Le convoyeur de sortie tourne si la machine est en marche et qu'une bouteille pleine est détectée ; "
             "ou si la machine est en marche, qu'aucune bouteille pleine n'est détectée et que le bouton de vidange est appuyé.", 40, 1500, mix(WHITE, NAVY, q))
        q2 = prog(t, 2.5, 3.5)
        for i, (l, s) in enumerate([("S", "le convoyeur tourne"), ("A", "machine en marche"), ("B", "bouteille pleine détectée"), ("C", "bouton de vidange appuyé")]):
            text(d, (160, 520 + i * 70), l, 44, mix(WHITE, BLUE, q2), True, italic=True, anchor="lm")
            text(d, (230, 520 + i * 70), ": " + s, 38, mix(WHITE, NAVY, q2), anchor="lm")
        caption(d, "Le cahier des charges, et la légende : la sortie s'appelle S, les entrées A, B et C.")
    elif t < 44:
        for i, (t0, parts, why) in enumerate(STEPS):
            q = prog(t, t0, t0 + 1.2)
            if q <= 0: continue
            y = 260 + i * 120
            over_eq(d, 120, y, parts, 64, alpha=q)
            if why: text(d, (1050, y), why, 36, mix(WHITE, BLUE, q), italic=True, anchor="lm")
        if t < 20:   # schéma câblé tel quel
            q = prog(t, 10, 11)
            if q > 0:
                ins, o1 = gate(d, 420, 380, "ET", 0.75, labels=("A", "B"), out_label="", alpha=q)
                i3, o3 = gate3(d, 420, 560, 0.6, labels=("A", "", "C"))
                insn, on = gate(d, 120, i3[1][1] - 75 * 0.5, "NON", 0.5, labels=("B",), out_label="")
                wire(d, [on, i3[1]], None, 4)
                insor, oo = gate(d, 980, 470, "OU", 0.75, labels=("", ""), out_label="S")
                wire(d, [o1, (insor[0][0] - 20, o1[1]), (insor[0][0] - 20, insor[0][1]), insor[0]], None, 4)
                wire(d, [o3, (insor[0][0] - 20, o3[1]), (insor[0][0] - 20, insor[1][1]), insor[1]], None, 4)
                text(d, (1300, 541), "4 portes · 4 CI", 44, mix(WHITE, NAVY, q), True, anchor="lm")
        caption(d, cap_at(t, [(8, "L'équation s'écrit comme le cahier des charges : un terme par condition. Câblée telle quelle, elle demande 4 portes."),
                              (20, "A est commun aux deux termes : on le met en évidence (distributivité)."),
                              (32, "Dans la parenthèse, on reconnaît la règle 11 : B + B̄ · C = B + C. Le résultat se relit : en marche, et bouteille pleine ou vidange.")]))
    elif t < 60:
        u = t - 44
        rows = [[c, b, a, CONV(c, b, a), SIMP(c, b, a)] for c in (0, 1) for b in (0, 1) for a in (0, 1)]
        table(d, 120, 210, ["C", "B", "A", "avant", "après"], rows, colw=130, rowh=74, outcols=2, show=int(clamp((u - 0.5) / 1.1, 0, 8)))
        if u > 10:
            for i in range(8): check(d, (120 + 5 * 130 + 50, 210 + 74 * (i + 1) + 37), True, 34)
            para(d, (1000, 400), "Les deux colonnes sont identiques : S = 1 sur les lignes 011, 101 et 111.", 40, 700, GREEN, True)
        caption(d, cap_at(u, [(0, "Contrôle : on calcule S avec l'équation de départ et avec le résultat, pour les 8 combinaisons de C, B et A."),
                              (10, "Les deux colonnes sont identiques sur toutes les lignes : la simplification est juste. Ce contrôle écrit fait partie de l'évaluation.")]))
    else:
        u = t - 60
        q = prog(u, 0.3, 1.3)
        over_eq(d, 120, 260, [("S = A · (B + C)", False)], 64, alpha=q)
        io, oo = gate(d, 420, 420, "OU", 1.0, labels=("B", "C"), out_label="", alpha=q)
        ia, oa = gate(d, oo[0] + 120, 330, "ET", 1.0, labels=("A", ""), out_label="S", alpha=q)
        wire(d, [oo, (oo[0] + 30, oo[1]), (oo[0] + 30, ia[1][1]), ia[1]], None, 5)
        q2 = prog(u, 3, 4)
        rbox(d, (1250, 330, BAND_X - 80, 640), fill=mix(WHITE, TINT, q2), r=18)
        text(d, (1290, 380), "Avant : 4 portes · 4 CI", 38, mix(WHITE, GREY, q2), True, anchor="lm")
        text(d, (1290, 460), "Après : 2 portes · 2 CI", 44, mix(WHITE, BLUE, q2), True, anchor="lm")
        text(d, (1290, 540), "74HC32 et 74HC08", 34, mix(WHITE, NAVY, q2), anchor="lm")
        caption(d, cap_at(u, [(0, "On dessine une porte par opération, en commençant par la parenthèse : d'abord B + C, puis le ET avec A."),
                              (6, "Même table de vérité, deux fois moins de portes : une carte plus petite, moins chère, et moins de pannes possibles.")]))


# ================================================================ cartes, introduction, récapitulatif
def ill_rules(img, d, t):
    gate(d, 260, 380, "ET", 1.3, (1, 1), 1, ("A", "1"), out_label="S")
    over_eq(d, 230, 760, [("A · 1 = A", False)], 64)


def ill_morgan(img, d, t):
    over_eq(d, 200, 520, [("S = ", False), ("A · B", True)], 84)
    text(d, (200, 680), "= ?", 84, BLUE, True, anchor="lm")


def ill_conv(img, d, t):
    over_eq(d, 90, 480, [("S = A · B + A · ", False), ("B", True), (" · C", False)], 52)
    text(d, (90, 640), "4 portes · 4 CI", 52, GREY, True, anchor="lm")


CARDS = [
    ("1", TOT, "Les règles sur une porte", "Une entrée à 0, à 1, ou reliée à A", ill_rules,
     "Une porte ET ou OU reçoit A sur une entrée. L'autre entrée est fixée à 0 ou à 1, ou reliée à A.",
     "Que devient la sortie S quand A change ?",
     "Les règles 1 à 9 de l'algèbre de Boole, vues sur une porte.", "A · 1 = A"),
    ("2", TOT, "Le théorème de De Morgan", "Casse la barre, change le signe", ill_morgan,
     "La ligne a deux arrêts d'urgence A et B. Le convoyeur est autorisé si aucun n'est actionné.",
     "Comment enlever la grande barre d'une expression ?",
     "Les deux formes du théorème, contrôlées par la table, puis les symboles équivalents.", "S = Ā · B̄"),
    ("3", TOT, "Le convoyeur de sortie", "Simplifier, contrôler, dessiner", ill_conv,
     "Un collègue a câblé la commande du convoyeur telle qu'il l'a écrite : 4 portes sur 4 CI.",
     "Peut-on obtenir le même fonctionnement avec moins de portes ?",
     "La méthode en quatre étapes : écrire, mettre en évidence, appliquer les règles, contrôler.", "S = A · (B + C)"),
]
CARD_DUR = 13.0

s_intro = intro_scene("TEST ET MESURE 1 – EL DT 1 · ANIMATION 205", "Algèbre de Boole",
                      "Calculer avec des 0 et des 1 pour simplifier un circuit",
                      [("1", "Les règles sur une porte", "règles 1 à 9"), ("2", "Le théorème de De Morgan", "casse la barre, change le signe"),
                       ("3", "Le convoyeur de sortie", "simplifier, contrôler, dessiner")],
                      "Va avec la présentation 200 et la fiche 210 EX")

s_outro = outro_scene(
    [("Lois", "commutativité, associativité, distributivité"), ("Règles", "12 règles : avec 0 et 1, avec A et son inverse, l'absorption"),
     ("De Morgan", "casse la barre, change le signe"), ("Méthode", "écrire, mettre en évidence, appliquer les règles, contrôler"),
     ("Schéma", "une porte par opération, en commençant par la parenthèse")],
    "À toi de jouer",
    [("Fiche 210 EX, partie A", "les lois, les 12 règles, De Morgan", ""), ("Fiche 210 EX, N°1 et N°2", "vérifier et appliquer les règles", ""),
     ("Fiche 210 EX, N°3", "De Morgan", ""), ("Fiche 210 EX, N°4 et N°5", "du cahier des charges au 74HC00", ""),
     ("Page interactive 201", "cinq exercices corrigés tout de suite", "")],
    "La sortie s'appelle toujours S, les entrées A, B, C : une légende donne le sens de chaque lettre.")

SCENES = [(s_intro, 9.0), (make_card(CARDS, 0, CARD_DUR), CARD_DUR), (s_rules, 8 * RD + 6), (make_card(CARDS, 1, CARD_DUR), CARD_DUR),
          (s_morgan, 46.0), (make_card(CARDS, 2, CARD_DUR), CARD_DUR), (s_conv, 72.0), (s_outro, 15.0)]


def produire(ctx):
    render(SCENES, ctx.sortie_de("205"))


if __name__ == "__main__":
    # aperçu d'une image : python3 contenus/tm1/semaine-2/200-algebre-boole/205-anim.py <scène> <t> [image.png]
    i, t = int(sys.argv[1]), float(sys.argv[2])
    frame_at(SCENES, i, t).save(sys.argv[3] if len(sys.argv) > 3 else "apercu_205.png")
