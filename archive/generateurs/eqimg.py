# -*- coding: utf-8 -*-
"""Rend des blocs d'équations en PNG transparent pour les diapositives.

Typographie mathématique (fractions à barre horizontale, indices, exposants) via
mathtext, police Computer Modern — la forme attendue dans un cours de maths.

    bloc("fig/eq_a.png", [
        ("algébrique", r"R_{23} = \frac{R_2 \cdot R_3}{R_2 + R_3}"),
        ("numérique",  r"R_{23} = \frac{0{,}15 \cdot 10^{3} \cdot 0{,}3 \cdot 10^{3}}"
                       r"{0{,}45 \cdot 10^{3}}"),
        ("ingénieur",  r"R_{23} = 100\ \Omega"),
    ])
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = ["Carlito", "DejaVu Sans"]

NAVY = "#242852"
BLUE = "#297FD5"
RED = "#EE0000"
GREY = "#7F8FA9"

LARGEUR = 8.1          # pouces — largeur de la zone utile d'une diapositive
X_LABEL = 0.004
X_EQ = 0.105


def bloc(path, lignes, largeur=LARGEUR, taille=15, couleur=NAVY, dpi=260,
         interligne=0.42, x_eq=X_EQ, label_taille=None):
    """lignes = [(étiquette | None, latex | None), …] ; None crée une ligne vide."""
    n = len(lignes)
    hauteur = interligne * n + 0.10
    fig = plt.figure(figsize=(largeur, hauteur), dpi=dpi)
    fig.patch.set_alpha(0)
    lt = label_taille if label_taille else taille - 4
    for i, item in enumerate(lignes):
        lab, eq = item[0], item[1]
        opt = item[2] if len(item) > 2 else {}
        y = 1 - (i + 0.62) * interligne / hauteur
        if lab:
            fig.text(opt.get("x_label", X_LABEL), y, lab, fontsize=lt,
                     color=opt.get("label_color", GREY), style="italic",
                     va="center", ha="left")
        if eq:
            fig.text(opt.get("x_eq", x_eq if lab else X_LABEL), y, eq,
                     fontsize=opt.get("size", taille),
                     color=opt.get("color", couleur), va="center", ha="left")
    fig.savefig(path, transparent=True, dpi=dpi,
                bbox_inches=None, pad_inches=0)
    plt.close(fig)
    return path
