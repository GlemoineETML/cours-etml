# -*- coding: utf-8 -*-
"""Figures propres à la semaine 1 TM1 : chronogrammes des sept portes, chronogrammes de la fiche 130, sortie push-pull (100),
niveaux et marges de bruit (100), ligne de remplissage (120, 130), brochages DIP 14, équations en image (présentations).
Briques communes : moteur/cei.py ; données : moteur/logique.py."""
import matplotlib
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
from moteur import logique as D
from moteur.cei import plt, save, line, fig_gate, fig_gate_mini, fig_eq, fig_eq_txt, chrono_fig, switch, fig_dip, K, NAVY, BLUE, LBLUE, TINT, RED, GR


def fig_chronos():
    A, B = D.CHRONO_A, D.CHRONO_B
    for k in D.ORDER:
        Y = D.chrono(k)
        ins = [("A", A)] if D.GATES[k][4] == 1 else [("A", A), ("B", B)]
        # largeur 5,6 pouces : placés à 9,6 cm (fiche) ou 4,75 pouces (présentation), les textes restent lisibles (REGLES 9.4)
        chrono_fig(ins + [("Y", Y)], f"chrono_{k}.png", width=5.6, ligne=0.72)
        chrono_fig(ins + [("Y", Y)], f"chrono_{k}_corr.png", ycol=RED, width=5.6, ligne=0.72)
        chrono_fig(ins + [("Y", None)], f"chrono_{k}_q.png", width=5.6, ligne=0.72)


# chronogrammes « mystère » (fiche 130, N°3) : autres motifs que le chronogramme du cours
MYST = [("NON-OU", [1, 0, 0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 1, 0, 0]),
        ("OUX", [0, 1, 1, 0, 0, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0, 0]),
        ("NON-ET", [1, 1, 0, 0, 1, 0, 1, 1], [0, 1, 1, 0, 1, 1, 1, 0])]


def fig_myst():
    for i, (k, A, B) in enumerate(MYST, 1):
        Y = D.chrono(k, A, B)
        chrono_fig([("A", A), ("B", B), ("Y", Y)], f"myst_{i}.png", ycol=NAVY)


# fiche 130, N°2 b) : chronogramme à compléter pour Y = A + B avec d'autres motifs
N2_A = [1, 0, 0, 1, 0, 1, 1, 0]
N2_B = [0, 0, 1, 1, 0, 0, 1, 1]


def fig_n2():
    Y = D.chrono("NON-OU", N2_A, N2_B)
    chrono_fig([("A", N2_A), ("B", N2_B), ("Y", None)], "n2_q.png")
    chrono_fig([("A", N2_A), ("B", N2_B), ("Y", Y)], "n2_corr.png", ycol=RED)


def fig_lecture():
    """Diapo « lire un chronogramme » : ET, intervalle 4 surligné."""
    A, B = D.CHRONO_A, D.CHRONO_B
    chrono_fig([("A", A), ("B", B), ("Y", D.chrono("ET"))], "chrono_lecture.png", highlight=3)




def fig_pushpull():
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.6))
    for ax, (y, haut) in zip(axs, ((1, True), (0, False))):
        ax.axis("off"); ax.set_aspect("equal")
        x = 1.0
        ax.text(x, 3.45, "+V$_{CC}$", ha="center", va="bottom", fontsize=14, color=NAVY)
        line(ax, [(x - 0.3, 3.4), (x + 0.3, 3.4)], lw=2.4)
        switch(ax, x, 3.4, 2.0, haut)
        switch(ax, x, 2.0, 0.6, not haut)
        ax.add_patch(Circle((x, 2.0), 0.06, color=K))
        line(ax, [(x, 2.0), (x + 1.3, 2.0)])
        ax.add_patch(Circle((x + 1.3, 2.0), 0.07, fill=False, ec=K, lw=1.8))
        ax.text(x + 1.5, 2.0, f"Y = {y}", ha="left", va="center", fontsize=16, fontweight="bold", color=(BLUE if y else NAVY))
        # masse (CEI : trait horizontal + traits décroissants)
        for k_, w_ in enumerate((0.3, 0.2, 0.1)):
            line(ax, [(x - w_, 0.6 - 0.1 * k_), (x + w_, 0.6 - 0.1 * k_)], lw=2.2)
        ax.text(x - 0.45, 2.75, "transistor\ndu haut", ha="right", va="center", fontsize=10.5, color=GR)
        ax.text(x - 0.45, 1.3, "transistor\ndu bas", ha="right", va="center", fontsize=10.5, color=GR)
        ax.text(x + 0.45, 2.75, "conduit" if haut else "bloqué", ha="left", va="center", fontsize=11, fontweight="bold",
                color=(BLUE if haut else GR))
        ax.text(x + 0.45, 1.3, "conduit" if not haut else "bloqué", ha="left", va="center", fontsize=11, fontweight="bold",
                color=(NAVY if not haut else GR))
        ax.set_xlim(-0.6, 3.4); ax.set_ylim(0.2, 3.9)
    save(fig, "fig_pushpull.png")


# ------------------------------------------------------------------ gabarit des niveaux et marges de bruit (100)
def fig_marges():
    fig, ax = plt.subplots(figsize=(8.6, 4.4)); ax.axis("off")
    VMAX = 5.0; H = 3.6
    Y = lambda v: 0.35 + v / VMAX * H
    cols = [("TTL", "TTL"), ("HC", "CMOS 74HC")]
    bw = 1.0
    for c, (fam, titre) in enumerate(cols):
        vil, vih, vol, voh = D.NIV[fam]
        x0 = 1.5 + c * 6.5
        ax.text(x0 + 1.85, Y(5) + 0.5, f"{titre} (V$_{{CC}}$ = 5 V)", ha="center", fontsize=16, fontweight="bold", color=NAVY)
        for j, (lab, lo, hi) in enumerate((("Sortie", vol, voh), ("Entrée", vil, vih))):
            x = x0 + j * 2.7
            ax.text(x + bw / 2, Y(5) + 0.15, lab, ha="center", fontsize=13.5, color=GR)
            ax.add_patch(Rectangle((x, Y(hi)), bw, Y(5) - Y(hi), fc=BLUE, ec="none"))
            ax.add_patch(Rectangle((x, Y(lo)), bw, Y(hi) - Y(lo), fc="#D5DDDF", ec="none"))
            ax.add_patch(Rectangle((x, Y(0)), bw, Y(lo) - Y(0), fc=NAVY, ec="none"))
            ax.add_patch(Rectangle((x, Y(0)), bw, Y(5) - Y(0), fill=False, ec=K, lw=1.0))
            ax.text(x + bw / 2, (Y(hi) + Y(5)) / 2, "1", ha="center", va="center", fontsize=19, fontweight="bold", color="white")
            ax.text(x + bw / 2, (Y(lo) + Y(hi)) / 2, "zone\ninterdite" if lab == "Entrée" else "non\ngarantie", ha="center", va="center", fontsize=11, color=GR)
            if Y(lo) - Y(0) > 0.28:
                ax.text(x + bw / 2, (Y(0) + Y(lo)) / 2, "0", ha="center", va="center", fontsize=13, fontweight="bold", color="white")
            sfx = ("OH", "OL") if lab == "Sortie" else ("IH", "IL")
            side = -1 if lab == "Sortie" else 1
            xt = x - 0.08 if side < 0 else x + bw + 0.08
            ha = "right" if side < 0 else "left"
            f = lambda v: f"{v:g}".replace(".", ",")
            ax.text(xt, Y(hi), f"V$_{{{sfx[0]}}}$ = {f(hi)} V", ha=ha, va="center", fontsize=12.5, color=NAVY)
            ax.text(xt, Y(lo), f"V$_{{{sfx[1]}}}$ = {f(lo)} V", ha=ha, va="center", fontsize=12.5, color=NAVY)
        # marges de bruit entre sortie et entrée
        xs, xe = x0 + bw, x0 + 2.7
        for a_, b_, lab in ((vih, voh, "N$_H$"), (vol, vil, "N$_L$")):
            ax.add_patch(Rectangle((xs + 0.02, Y(a_)), xe - xs - 0.04, Y(b_) - Y(a_), fc="#7FD07F", ec="none", alpha=0.75))
            m = round(b_ - a_, 2)
            ax.text((xs + xe) / 2, (Y(a_) + Y(b_)) / 2, f"{lab} = {m:g} V".replace(".", ","), ha="center", va="center", fontsize=11.5, fontweight="bold", color=K)
    ax.text(6.8, 0.02, "N$_H$ = V$_{OH}$ − V$_{IH}$     N$_L$ = V$_{IL}$ − V$_{OL}$     (valeurs garanties, Floyd 3-8 p. 154)",
            ha="center", va="bottom", fontsize=12.5, color=GR)
    ax.set_xlim(-0.2, 13.2); ax.set_ylim(-0.1, Y(5) + 0.8)
    save(fig, "fig_marges.png")


# ------------------------------------------------------------------ ligne de remplissage (120, 130)
def fig_ligne():
    fig, ax = plt.subplots(figsize=(9.0, 3.9)); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(FancyBboxPatch((0.2, 0.45), 5.7, 0.35, boxstyle="round,pad=0,rounding_size=0.17", fc="#D5DDDF", ec=K, lw=1.4))
    for xx in (0.38, 5.72):
        ax.add_patch(Circle((xx, 0.625), 0.13, fc="white", ec=K, lw=1.2))
    ax.add_patch(Circle((6.45, 0.62), 0.33, fc="white", ec=NAVY, lw=2))
    ax.text(6.45, 0.62, "M", ha="center", va="center", fontsize=14, fontweight="bold", color=NAVY)
    line(ax, [(5.85, 0.62), (6.12, 0.62)], c=NAVY)
    for xb in (1.0, 3.0, 5.0):
        ax.add_patch(FancyBboxPatch((xb - 0.28, 0.82), 0.56, 1.0, boxstyle="round,pad=0,rounding_size=0.12", fc=TINT, ec=NAVY, lw=1.4))
        ax.add_patch(Rectangle((xb - 0.1, 1.82), 0.2, 0.28, fc=TINT, ec=NAVY, lw=1.4))
    ax.add_patch(Rectangle((2.3, 3.0), 1.4, 1.35, fc="white", ec=NAVY, lw=1.8))
    ax.add_patch(Rectangle((2.3, 3.0), 1.4, 0.8, fc=LBLUE, ec="none"))
    line(ax, [(3.0, 3.0), (3.0, 2.75)], c=NAVY)
    ax.add_patch(Polygon([(2.75, 2.75), (2.75, 2.35), (3.0, 2.55)], closed=True, fc="white", ec=NAVY, lw=1.6))
    ax.add_patch(Polygon([(3.25, 2.75), (3.25, 2.35), (3.0, 2.55)], closed=True, fc="white", ec=NAVY, lw=1.6))
    line(ax, [(3.0, 2.35), (3.0, 2.2)], c=NAVY)
    ax.add_patch(Rectangle((1.85, 0.88), 2.3, 1.55, fill=False, ec=GR, lw=1.2, ls=(0, (4, 3))))
    def sq(x, y, lab, col, rounded=False):
        if rounded:
            ax.add_patch(FancyBboxPatch((x - 0.17, y - 0.17), 0.34, 0.34, boxstyle="round,pad=0,rounding_size=0.08", fc=col, ec=col))
        else:
            ax.add_patch(Rectangle((x - 0.17, y - 0.17), 0.34, 0.34, fc=col, ec=col))
        ax.text(x, y, lab, ha="center", va="center", fontsize=11, fontweight="bold", color="white")
    sq(3.95, 3.6, "N", BLUE); sq(2.35, 1.35, "B", BLUE); sq(4.45, 1.6, "P", BLUE); sq(0.6, 3.6, "U", BLUE)
    ax.add_patch(Circle((0.6, 3.05), 0.2, fc="#EE0000", ec=K, lw=1.2))
    sq(3.55, 2.55, "V", NAVY, True)
    # légende
    x0 = 7.2
    ax.text(x0, 4.25, "Entrées (capteurs, boutons)", fontsize=11.5, fontweight="bold", color=BLUE, va="center")
    for i, (l, t) in enumerate((("B", "bouteille sous le bec"), ("N", "niveau de la cuve suffisant"), ("P", "porte de protection fermée"), ("U", "arrêt d'urgence actionné"))):
        y = 3.8 - i * 0.42; sq(x0 + 0.17, y, l, BLUE)
        ax.text(x0 + 0.5, y, t, fontsize=11, va="center", color=K)
    ax.text(x0, 1.85, "Sorties (actionneurs)", fontsize=11.5, fontweight="bold", color=NAVY, va="center")
    for i, (l, t) in enumerate((("V", "vanne de remplissage"), ("M", "moteur du convoyeur"))):
        y = 1.4 - i * 0.42; sq(x0 + 0.17, y, l, NAVY, True)
        ax.text(x0 + 0.5, y, t, fontsize=11, va="center", color=K)
    ax.set_xlim(0.0, 10.4); ax.set_ylim(0.15, 4.55)
    save(fig, "fig_ligne.png")


def produire(ctx):
    """Écrit toutes les figures de la séance dans ctx.images."""
    import moteur.cei as cei
    cei.ecrire_dans(ctx.images)
    for k in D.ORDER:
        fig_gate(k); fig_gate_mini(k); fig_eq(k); fig_eq(k, color=RED, name=f"eq_{k}_corr.png")
    fig_chronos(); fig_myst(); fig_n2(); fig_lecture()
    fig_pushpull(); fig_marges(); fig_ligne()
    for r in D.PINS: fig_dip(r)
    # équation du convoyeur (fiche 130, N°1)
    fig_eq_txt(r"M = E \cdot L \cdot \overline{U}", "eq_convoyeur.png")
