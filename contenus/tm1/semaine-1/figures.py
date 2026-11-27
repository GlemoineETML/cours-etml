# -*- coding: utf-8 -*-
"""Figures propres à la semaine 1 TM1 : chronogrammes des sept portes, chronogrammes de la fiche 130, sortie push-pull (100),
niveaux et marges de bruit (100), ligne de remplissage (130 V1), voiture électrique et commande de démarrage (120 V2 : entrées du fascicule, voyant actif à 1),
brochages DIP 14, équations en image (présentations).
120 V2 (11/27/2026) : sortie S (REGLES 3.4) ; les figures en Y restent pour les fichiers pas encore passés en V2.
Briques communes : moteur/cei.py ; données : moteur/logique.py."""
import re
import matplotlib
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon, Ellipse
from moteur import logique as D
from moteur.cei import (plt, save, line, fig_gate, fig_gate_mini, fig_eq, fig_eq_txt, chrono_fig, switch, fig_dip, porte, fil, noeud,
                        borne, diode, resistance, alimentation, masse, K, NAVY, BLUE, LBLUE, TINT, RED, GR)


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
        chrono_fig([("A", A), ("B", B), ("S", Y)], f"myst_{i}.png", ycol=NAVY)


# fiche 130, N°2 b) : chronogramme à compléter pour S = /(A + B) avec d'autres motifs
N2_A = [1, 0, 0, 1, 0, 1, 1, 0]
N2_B = [0, 0, 1, 1, 0, 0, 1, 1]


def fig_n2():
    Y = D.chrono("NON-OU", N2_A, N2_B)
    chrono_fig([("A", N2_A), ("B", N2_B), ("S", None)], "n2_q.png")
    chrono_fig([("A", N2_A), ("B", N2_B), ("S", Y)], "n2_corr.png", ycol=RED)


def fig_lecture():
    """Diapo « lire un chronogramme » : ET, intervalle 4 surligné."""
    A, B = D.CHRONO_A, D.CHRONO_B
    chrono_fig([("A", A), ("B", B), ("Y", D.chrono("ET"))], "chrono_lecture.png", highlight=3)


# ------------------------------------------------------------------ 120 V2 : sortie S (REGLES 3.4)
def figs_S():
    A, B = D.CHRONO_A, D.CHRONO_B
    for k in D.ORDER:
        n = D.GATES[k][4]
        fig_gate(k, f"gate_{k}_S.png", labels=("A", "S") if n == 1 else ("A", "B", "S"))
        fig_eq_txt(re.sub(r"^Y", "S", D.GATES[k][6]), f"eq_{k}_S.png")
        ins = [("A", A)] if n == 1 else [("A", A), ("B", B)]
        # largeur 5,6 pouces, comme fig_chronos : textes lisibles une fois placés (REGLES 9.4)
        chrono_fig(ins + [("S", D.chrono(k))], f"chrono_{k}_S.png", width=5.6, ligne=0.72)
        chrono_fig(ins + [("S", D.chrono(k))], f"chrono_{k}_S_corr.png", ycol=RED, width=5.6, ligne=0.72)
        chrono_fig(ins + [("S", None)], f"chrono_{k}_S_q.png", width=5.6, ligne=0.72)
    chrono_fig([("A", A), ("B", B), ("S", D.chrono("ET"))], "chrono_lecture_S.png", highlight=3)
    fig_eq_txt(r"S = B \cdot (D + \overline{A + C})", "eq_demarrage.png")


# ------------------------------------------------------------------ 120 V2 : la voiture électrique (diapositive 2)
DEM_ENTREES = (("A", "ceinture", "0 = bouclée"), ("B", "sélecteur", "1 = position P"),
               ("C", "frein", "0 = pédale enfoncée"), ("D", "mode service", "1 = actif"))     # entrées du fascicule ; voyant actif à 1


def fig_voiture():
    """Voiture vue de côté (avant à droite) avec les repères A, B, C, D, S ; légende dessous, en deux colonnes."""
    fig, ax = plt.subplots(figsize=(6.6, 4.4)); ax.axis("off"); ax.set_aspect("equal")
    dx = 0.75
    P = lambda pts: [(x + dx, y) for x, y in pts]
    ax.add_patch(Polygon(P([(0.25, 0.62), (0.2, 1.45), (1.25, 1.62), (2.05, 2.42), (3.95, 2.48), (4.85, 1.72), (6.05, 1.52), (6.25, 1.05), (6.2, 0.62)]),
                         closed=True, fc=TINT, ec=NAVY, lw=2.0))
    ax.add_patch(Polygon(P([(2.2, 1.72), (2.3, 2.3), (3.85, 2.33), (4.5, 1.74)]), closed=True, fc="white", ec=NAVY, lw=1.4))
    for xr in (1.45, 5.0):
        ax.add_patch(Circle((xr + dx, 0.62), 0.43, fc="#3A3F52", ec=K, lw=1.4, zorder=3))
        ax.add_patch(Circle((xr + dx, 0.62), 0.16, fc="#C8CEDA", ec=K, lw=1.0, zorder=4))
    # siège et ceinture (A)
    line(ax, P([(2.95, 0.98), (2.78, 2.05)]), lw=7, c="#5A6478")
    line(ax, P([(2.95, 0.98), (3.65, 1.02)]), lw=7, c="#5A6478")
    line(ax, P([(2.86, 1.92), (3.52, 1.06)]), lw=3.2, c=NAVY)
    ax.add_patch(Rectangle((3.47 + dx, 0.98), 0.16, 0.13, fc=NAVY, ec=NAVY, zorder=4))
    # volant, tableau de bord avec le voyant S
    line(ax, P([(4.05, 1.32), (4.25, 1.78)]), lw=4, c=K)
    ax.add_patch(Rectangle((4.32 + dx, 1.42), 0.62, 0.22, fc="#D5DDDF", ec=K, lw=1.2))
    ax.add_patch(Circle((4.63 + dx, 1.53), 0.07, fc="#FF5A3C", ec=K, lw=1.0, zorder=4))
    # sélecteur (B), pédale de frein (C), commutateur de service (D)
    ax.add_patch(Rectangle((3.75 + dx, 0.98), 0.32, 0.2, fc="white", ec=K, lw=1.2))
    line(ax, P([(3.91, 1.18), (3.91, 1.36)]), lw=2.6, c=K)
    ax.add_patch(Circle((3.91 + dx, 1.38), 0.06, fc=K, ec=K))
    line(ax, P([(4.75, 0.8), (4.95, 1.15)]), lw=4, c=K)
    ax.add_patch(Rectangle((5.25 + dx, 1.12), 0.3, 0.18, fc="white", ec=K, lw=1.2))

    def sq(x, y, lab, col, rounded=False):
        if rounded:
            ax.add_patch(FancyBboxPatch((x - 0.17, y - 0.17), 0.34, 0.34, boxstyle="round,pad=0,rounding_size=0.08", fc=col, ec=col, zorder=5))
        else:
            ax.add_patch(Rectangle((x - 0.17, y - 0.17), 0.34, 0.34, fc=col, ec=col, zorder=5))
        ax.text(x, y, lab, ha="center", va="center", fontsize=13, fontweight="bold", color="white", zorder=6)

    def repere(x, y, xc, yc, lab, col=BLUE, rounded=False):
        line(ax, [(x + dx, y), (xc + dx, yc)], lw=1.2, c=GR)
        sq(x + dx, y, lab, col, rounded)

    repere(2.45, 2.85, 3.15, 1.62, "A")
    repere(3.55, 2.85, 3.91, 1.38, "B")
    repere(3.95, 0.28, 4.78, 0.86, "C")
    repere(5.85, 0.28, 5.4, 1.12, "D")
    repere(4.95, 2.85, 4.63, 1.6, "S", NAVY, True)
    # légende : entrées à gauche, sortie à droite
    ax.plot([0.1, 7.9], [-0.18, -0.18], color=LBLUE, lw=1.2)
    ax.text(0.15, -0.5, "Entrées", fontsize=13, fontweight="bold", color=BLUE, va="center")
    for i, (l, nom, niv) in enumerate(DEM_ENTREES):
        y = -0.98 - i * 0.45; sq(0.32, y, l, BLUE)
        ax.text(0.63, y, f"{nom} : {niv}", fontsize=12.5, va="center", color=K)
    x0 = 4.85
    ax.text(x0, -0.5, "Sortie", fontsize=13, fontweight="bold", color=NAVY, va="center")
    sq(x0 + 0.17, -0.98, "S", NAVY, True)
    ax.text(x0 + 0.48, -0.98, "voyant « démarrage »", fontsize=12.5, va="center", color=K)
    ax.text(x0 + 0.48, -1.43, "allumé si S = 1", fontsize=12.5, va="center", color=K)
    ax.set_xlim(0.0, 8.0); ax.set_ylim(-2.55, 3.1)
    save(fig, "fig_voiture.png")


# ------------------------------------------------------------------ 120 V2 : la commande de démarrage, porte par porte (diapositive 13)
def fig_demarrage():
    """S = B · (D + /(A + C)) : NON-OU (74HC02), OU (74HC32), ET (74HC08) ; LED entre S et GND, allumée si S = 1."""
    fig, ax = plt.subplots(figsize=(6.6, 3.6)); ax.axis("off"); ax.set_aspect("equal")
    fs = 15
    (a_, c_), o1 = porte(ax, 1.0, 0.6, "OU", neg=True, fs=fs)             # NON-OU (74HC02)
    (d_, x1), o2 = porte(ax, 2.9, 0.86, "OU", fs=fs)                      # OU (74HC32)
    (b_, x2), o3 = porte(ax, 4.8, 1.12, "ET", fs=fs)                      # ET (74HC08)
    fil(ax, o1, x1); fil(ax, o2, x2)
    xg = 0.25                                                             # entrées, toutes à gauche
    fil(ax, (xg, b_[1] + 0.75), (b_[0] - 0.25, b_[1] + 0.75), (b_[0] - 0.25, b_[1]), b_)
    fil(ax, (xg, d_[1] + 0.6), (d_[0] - 0.25, d_[1] + 0.6), (d_[0] - 0.25, d_[1]), d_)
    fil(ax, (xg, a_[1]), a_); fil(ax, (xg, c_[1]), c_)
    for lab, y in (("B", b_[1] + 0.75), ("D", d_[1] + 0.6), ("A", a_[1]), ("C", c_[1])):
        ax.text(xg - 0.1, y, lab, ha="right", va="center", fontsize=fs + 1, style="italic", fontweight="bold", color=NAVY)
    for x, y, ci in ((1.45, 0.6, "74HC02"), (3.35, 0.86, "74HC32"), (5.25, 1.12, "74HC08")):
        ax.text(x, y - 0.2, ci, ha="center", va="center", fontsize=12.5, color=GR)
    # sortie S, résistance et LED vers GND (la LED s'allume quand S = 1)
    xl = 6.75
    fil(ax, o3, (xl, o3[1]), (xl, o3[1] - 0.1))
    ax.text((o3[0] + xl) / 2, o3[1] + 0.17, "S", ha="center", va="center", fontsize=fs + 1, style="italic", fontweight="bold", color=NAVY)
    resistance(ax, xl, o3[1] - 1.05, o3[1] - 0.1, nom="R", fs=14)
    diode(ax, xl, o3[1] - 2.0, o3[1] - 1.05, sens="bas", genre="led", nom="LED", fs=13)
    masse(ax, xl, o3[1] - 2.0, fs=12.5)
    ax.text(xl - 0.55, o3[1] - 2.2, "LED allumée si S = 1", ha="right", va="center", fontsize=12.5, color=NAVY)
    ax.set_xlim(-0.15, 7.9); ax.set_ylim(o3[1] - 2.5, o3[1] + 1.1)
    save(fig, "fig_demarrage.png")


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
    figs_S(); fig_voiture(); fig_demarrage()
    for r in D.PINS: fig_dip(r)
    # équation du convoyeur (fiche 130, N°1)
    fig_eq_txt(r"M = E \cdot L \cdot \overline{U}", "eq_convoyeur.png")
