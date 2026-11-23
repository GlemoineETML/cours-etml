# -*- coding: utf-8 -*-
"""Figures de la séance 200 Algèbre de Boole : règles au niveau des portes, De Morgan (symboles équivalents),
NON-ET universelle, schémas du convoyeur (avant / après simplification) ; sortie S, entrées A, B, C (REGLES 3.4), corrigés des schémas de la fiche 210 EX,
équations en image (secours des équations éditables de la présentation, equations.json).
Briques communes : moteur/cei.py (porte, fil, symboles CEI 60617-12)."""
import json, os, re
from moteur.cei import plt, save, line, porte, fil, noeud, fig_eq_txt, K, NAVY, BLUE, GR, RED

ICI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ équations : mini-syntaxe omml → mathtext
def mathtext(src):
    s = src
    while "\\bar{" in s:                       # \bar{…} → \overline{…} (accolades imbriquées)
        i = s.index("\\bar{"); j = i + 5; d = 1
        while d:
            d += {"{": 1, "}": -1}.get(s[j], 0); j += 1
        s = s[:i] + "\\overline{" + s[i + 5:j - 1] + "}" + s[j:]
    s = re.sub(r"\\u\{([^}]*)\}", r"\\mathrm{\1}", s).replace("\\f{", "\\frac{")
    return s


def equations():
    eqs = json.load(open(os.path.join(ICI, "equations.json"), encoding="utf-8"))
    for nom, src in eqs.items():
        if nom != "_":
            fig_eq_txt(mathtext(src), nom + ".png")


# ------------------------------------------------------------------ outils de dessin
def lab(ax, p, t, cote="g", fs=14, c=NAVY):
    """Étiquette d'une entrée (à gauche de la borne) ou d'une sortie (à droite)."""
    x, y = p
    ax.text(x - 0.08 if cote == "g" else x + 0.08, y, t, ha="right" if cote == "g" else "left", va="center",
            fontsize=fs, style="italic" if t.startswith("$") else "normal", color=c)


def cadre(ax, xmin, xmax, ymin, ymax):
    ax.axis("off"); ax.set_aspect("equal"); ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)


def panneaux(nom, cas):
    """Une rangée de petites portes : cas = [(fonction, entrée 2, sortie, titre)] ; l'entrée 1 vaut toujours A."""
    fig, axs = plt.subplots(1, len(cas), figsize=(2.35 * len(cas), 1.9))
    for ax, (f, e2, y, titre) in zip(axs, cas):
        cadre(ax, -0.9, 2.2, -0.35, 1.55)
        ent, s = porte(ax, 0.2, 0.0, f)
        lab(ax, ent[0], "$A$")
        lab(ax, ent[1], e2, c=BLUE if e2 in ("0", "1") else NAVY)
        lab(ax, s, y, cote="d", c=RED)
        ax.text(0.65, 1.38, titre, ha="center", va="center", fontsize=12, color=GR)
    save(fig, nom)


# ------------------------------------------------------------------ De Morgan : symboles équivalents
def demorgan():
    fig, ax = plt.subplots(figsize=(7.6, 3.6)); cadre(ax, -0.9, 8.4, -0.5, 3.7)
    for k, (f1, f2, t) in enumerate((("ET", "OU", r"$\overline{A\cdot B}=\overline{A}+\overline{B}$"),
                                     ("OU", "ET", r"$\overline{A+B}=\overline{A}\cdot\overline{B}$"))):
        y0 = 2.2 - k * 2.2
        ent, s = porte(ax, 0.2, y0, f1, neg=True)
        lab(ax, ent[0], "$A$"); lab(ax, ent[1], "$B$"); lab(ax, s, "$S$", "d")
        ax.text(2.55, y0 + 0.52, "=", ha="center", va="center", fontsize=26, color=BLUE, fontweight="bold")
        ent, s = porte(ax, 3.9, y0, f2, neg_in=(0, 1))
        lab(ax, ent[0], "$A$"); lab(ax, ent[1], "$B$"); lab(ax, s, "$S$", "d")
        ax.text(5.9, y0 + 0.52, t, ha="left", va="center", fontsize=15, color=NAVY)
    save(fig, "fig_demorgan.png")


# ------------------------------------------------------------------ tout avec des NON-ET
def nand_universel():
    fig, axs = plt.subplots(1, 3, figsize=(10.2, 2.8), gridspec_kw={"width_ratios": [2.4, 3.6, 3.6]})
    # NON : entrées reliées
    ax = axs[0]; cadre(ax, -1.0, 2.6, -0.6, 1.9)
    ent, s = porte(ax, 0.3, 0.0, "ET", neg=True)
    fil(ax, (ent[0][0], ent[0][1]), (ent[0][0], ent[1][1]))
    fil(ax, (ent[0][0] - 0.3, 0.52), (ent[0][0], 0.52), noeuds=[(ent[0][0], 0.52)])
    lab(ax, (ent[0][0] - 0.3, 0.52), "$A$"); lab(ax, s, r"$\overline{A}$", "d")
    ax.text(0.75, 1.65, "NON", ha="center", fontsize=13, color=BLUE, fontweight="bold")
    # ET : NON-ET puis NON-ET en inverseur
    ax = axs[1]; cadre(ax, -0.8, 4.3, -0.6, 1.9)
    e1, s1 = porte(ax, 0.2, 0.0, "ET", neg=True)
    lab(ax, e1[0], "$A$"); lab(ax, e1[1], "$B$")
    e2, s2 = porte(ax, 2.2, 0.0, "ET", neg=True)
    fil(ax, s1, (e2[0][0] - 0.15, s1[1]), noeuds=[(e2[0][0] - 0.15, s1[1])])
    fil(ax, (e2[0][0] - 0.15, e2[0][1]), (e2[0][0] - 0.15, e2[1][1]))
    fil(ax, (e2[0][0] - 0.15, e2[0][1]), e2[0]); fil(ax, (e2[0][0] - 0.15, e2[1][1]), e2[1])
    lab(ax, s2, r"$A\cdot B$", "d")
    ax.text(1.75, 1.65, "ET : 2 portes", ha="center", fontsize=13, color=BLUE, fontweight="bold")
    # OU : deux inverseurs NON-ET puis NON-ET (De Morgan)
    ax = axs[2]; cadre(ax, -0.8, 4.3, -1.3, 2.6)
    ea, sa = porte(ax, 0.2, 1.2, "ET", neg=True, h=0.9)
    eb, sb = porte(ax, 0.2, -0.9, "ET", neg=True, h=0.9)
    for e, t in ((ea, "$A$"), (eb, "$B$")):
        xj = e[0][0] - 0.12
        fil(ax, e[0], (xj, e[0][1]), (xj, e[1][1]), e[1]); fil(ax, (xj - 0.25, (e[0][1] + e[1][1]) / 2), (xj, (e[0][1] + e[1][1]) / 2),
                                                          noeuds=[(xj, (e[0][1] + e[1][1]) / 2)])
        lab(ax, (xj - 0.25, (e[0][1] + e[1][1]) / 2), t)
    ec, sc = porte(ax, 2.4, 0.13, "ET", neg=True)
    fil(ax, sa, (2.0, sa[1]), (2.0, ec[0][1]), ec[0]); fil(ax, sb, (2.0, sb[1]), (2.0, ec[1][1]), ec[1])
    lab(ax, sc, "$A+B$", "d")
    ax.text(1.75, 2.35, "OU : 3 portes", ha="center", fontsize=13, color=BLUE, fontweight="bold")
    save(fig, "fig_nand.png")


# ------------------------------------------------------------------ convoyeur : avant / après
def convoyeur_avant():
    fig, ax = plt.subplots(figsize=(6.8, 3.6)); cadre(ax, -1.2, 6.8, -0.3, 3.9)
    e1, s1 = porte(ax, 2.1, 2.4, "ET")                       # A · B
    lab(ax, e1[0], "$A$"); lab(ax, e1[1], "$B$")
    e2, s2 = porte(ax, 2.1, 0.0, "ET", n=3)                  # A · B barre · C
    lab(ax, e2[0], "$A$"); lab(ax, e2[2], "$C$")
    en, sn = porte(ax, -0.4, e2[1][1] - 0.45, "NON", n=1, neg=True)   # B barre, au niveau de l'entrée du milieu
    lab(ax, en[0], "$B$")
    fil(ax, sn, e2[1])
    e3, s3 = porte(ax, 4.4, 1.2, "OU")
    fil(ax, s1, (3.9, s1[1]), (3.9, e3[0][1]), e3[0]); fil(ax, s2, (3.9, s2[1]), (3.9, e3[1][1]), e3[1])
    lab(ax, s3, "$S$", "d")
    save(fig, "fig_conv_avant.png")


def deux_portes(nom, ent1, ent2, f1, neg1, f2, sortie, c=NAVY):
    """Porte 1 (deux entrées) suivie d'une porte 2 dont l'entrée du haut est ent2 : schémas S = A · (B + C) et S = A · (B · C) barré."""
    fig, ax = plt.subplots(figsize=(5.0, 2.4)); cadre(ax, -0.9, 4.6, -0.3, 2.3)
    e1, s1 = porte(ax, 0.2, 0.0, f1, neg=neg1)
    lab(ax, e1[0], ent1[0], c=c); lab(ax, e1[1], ent1[1], c=c)
    e2, s2 = porte(ax, 2.4, 0.5, f2)
    lab(ax, e2[0], ent2, c=c)
    fil(ax, s1, (1.95, s1[1]), (1.95, e2[1][1]), e2[1])
    lab(ax, s2, sortie, "d", c=c)
    save(fig, nom)


def n4_nand():
    """S avec un seul 74HC00 : trois portes NON-ET."""
    fig, ax = plt.subplots(figsize=(6.6, 2.4)); cadre(ax, -0.9, 6.6, -0.3, 2.3)
    e1, s1 = porte(ax, 0.2, 0.0, "ET", neg=True)
    lab(ax, e1[0], "$B$", c=RED); lab(ax, e1[1], "$C$", c=RED)
    e2, s2 = porte(ax, 2.4, 0.5, "ET", neg=True)
    lab(ax, e2[0], "$A$", c=RED)
    fil(ax, s1, (1.95, s1[1]), (1.95, e2[1][1]), e2[1])
    e3, s3 = porte(ax, 4.4, 0.5, "ET", neg=True)
    xj = e3[0][0] - 0.15
    fil(ax, s2, (xj, s2[1])); fil(ax, (xj, e3[0][1]), (xj, e3[1][1]), noeuds=[(xj, s2[1])])
    fil(ax, (xj, e3[0][1]), e3[0]); fil(ax, (xj, e3[1][1]), e3[1])
    lab(ax, s3, "$S$", "d", c=RED)
    save(fig, "fig_n4_nand.png")


def n5_corr():
    """S = A · B + A · C en NON-ET / NON-ET : trois portes d'un 74HC00."""
    fig, ax = plt.subplots(figsize=(5.0, 3.0)); cadre(ax, -0.9, 4.6, -0.3, 3.1)
    e1, s1 = porte(ax, 0.2, 1.8, "ET", neg=True)
    lab(ax, e1[0], "$A$", c=RED); lab(ax, e1[1], "$B$", c=RED)
    e2, s2 = porte(ax, 0.2, 0.0, "ET", neg=True)
    lab(ax, e2[0], "$A$", c=RED); lab(ax, e2[1], "$C$", c=RED)
    e3, s3 = porte(ax, 2.5, 0.9, "ET", neg=True)
    fil(ax, s1, (2.05, s1[1]), (2.05, e3[0][1]), e3[0]); fil(ax, s2, (2.05, s2[1]), (2.05, e3[1][1]), e3[1])
    lab(ax, s3, "$S$", "d", c=RED)
    save(fig, "fig_n5_corr.png")


def produire(ctx):
    import moteur.cei as cei
    cei.ecrire_dans(ctx.images)
    equations()
    panneaux("fig_regles_01.png", [("OU", "0", "$A$", "règle 1"), ("OU", "1", "1", "règle 2"),
                                   ("ET", "0", "0", "règle 3"), ("ET", "1", "$A$", "règle 4")])
    panneaux("fig_regles_aa.png", [("OU", "$A$", "$A$", "règle 5"), ("OU", r"$\overline{A}$", "1", "règle 6"),
                                   ("ET", "$A$", "$A$", "règle 7"), ("ET", r"$\overline{A}$", "0", "règle 8")])
    demorgan(); nand_universel(); convoyeur_avant()
    deux_portes("fig_conv_apres.png", ("$B$", "$C$"), "$A$", "OU", False, "ET", "$S$")
    deux_portes("fig_n4_corr.png", ("$B$", "$C$"), "$A$", "ET", True, "ET", "$S$", c=RED)
    n4_nand(); n5_corr()
