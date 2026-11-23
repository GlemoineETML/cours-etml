# -*- coding: utf-8 -*-
"""Figures de la séance de test « Diviseur de tension » : schémas CEI (moteur/cei.py) et équations en image (présentation)."""
import matplotlib.pyplot as plt
from moteur.cei import (save, line, resistance, source_tension, masse, noeud, borne, fleche_tension, fleche_courant, fig_eq_txt,
                        K, NAVY, BLUE, RED, GR)


def diviseur(nom, r1=("$R_1$", None), r2=("$R_2$", None), u=("$U$", None), u2="$U_2$", charge=None, courant="$I$", u1=None):
    """Diviseur de tension alimenté par une source ; charge = (nom, valeur) ajoute une résistance de charge en parallèle sur R2."""
    larg = 6.4 if charge else 5.0
    fig, ax = plt.subplots(figsize=(larg * 0.95, 4.6)); ax.axis("off"); ax.set_aspect("equal")
    top, bas, xs, xr, xo = 4.0, 0.0, 0.0, 2.2, 3.7
    source_tension(ax, xs, bas, top)
    line(ax, [(xs, top), (xr, top)]); line(ax, [(xs, bas), (xo + (1.4 if charge else 0), bas)])
    resistance(ax, xr, 2.0, top, *r1)
    resistance(ax, xr, bas, 2.0, *r2)
    noeud(ax, xr, 2.0); noeud(ax, xr, bas)
    line(ax, [(xr, 2.0), (xo + (1.4 if charge else 0), 2.0)])
    if charge:
        noeud(ax, xo, 2.0); noeud(ax, xo, bas)
        resistance(ax, xo + 1.4, bas, 2.0, *charge)
        fleche_tension(ax, xo + 0.45, bas + 0.2, 2.0 - 0.2, u2)
    else:
        borne(ax, xo, 2.0); borne(ax, xo, bas)
        fleche_tension(ax, xo + 0.25, bas + 0.2, 2.0 - 0.2, u2)
    if u1:
        fleche_tension(ax, xr - 0.75, 2.2, top - 0.2, u1, couleur=GR, cote="gauche")
    fleche_tension(ax, xs - 0.6, bas + 0.4, top - 0.4, u[0], couleur=NAVY, cote="gauche")
    if u[1]:
        ax.text(xs + 0.5, (top + bas) / 2, u[1], ha="left", va="center", fontsize=13, color=GR)
    if courant:
        fleche_courant(ax, 0.7, top, 1.5, top, courant, decal=(0.0, 0.3))
    masse(ax, xr, bas)                                         # sous le nœud du bas de R2
    ax.set_xlim(-1.6, xo + (2.6 if charge else 1.3)); ax.set_ylim(-0.85, top + 0.6)
    save(fig, nom)


def produire(ctx):
    import moteur.cei as cei
    cei.ecrire_dans(ctx.images)
    diviseur("fig_diviseur.png", u1="$U_1$")
    diviseur("fig_batterie.png", r1=("$R_1$", "22k"), r2=("$R_2$", "10k"), u=("$U$", "12 V"))
    diviseur("fig_charge.png", r1=("$R_1$", "22k"), r2=("$R_2$", "10k"), u=("$U$", "12 V"), charge=(r"$R_\mathrm{L}$", "10k"), courant=None)
    fig_eq_txt(r"U_2 = U \cdot \frac{R_2}{R_1 + R_2}", "eq_diviseur.png")
    fig_eq_txt(r"I = \frac{U}{R_1 + R_2}", "eq_courant.png")
    fig_eq_txt(r"R_{2\mathrm{L}} = \frac{R_2 \cdot R_\mathrm{L}}{R_2 + R_\mathrm{L}}", "eq_parallele.png")
    fig_eq_txt(r"U_2 = 12\,[\mathrm{V}] \cdot \frac{10\,[\mathrm{k\Omega}]}{22\,[\mathrm{k\Omega}] + 10\,[\mathrm{k\Omega}]}", "eq_an.png")
    diviseur("fig_ex1.png", r1=("$R_1$", "4k7"), r2=("$R_2$", "2k2"), u=("$U$", "9 V"), u1="$U_1$")
