# -*- coding: utf-8 -*-
"""Figures de la séance de test « Diviseur de tension » : schémas CEI (moteur/cei.py) et équations en image (présentation)."""
import matplotlib.pyplot as plt
from moteur.cei import save, line, resistance, source_tension, masse, noeud, borne, fleche_tension, fleche_courant, fig_eq_txt


def diviseur(nom, r1=("$R_1$", None), r2=("$R_2$", None), u=("$U$", None), u2="$U_2$", charge=None, courant="$I$", u1=None):
    """Diviseur de tension alimenté par une source ; charge = (nom, valeur) ajoute une résistance de charge en parallèle sur R2.
    Conventions de moteur/cei.py : noms et valeurs à gauche des composants, flèches de tension à droite, en bleu."""
    larg = 6.6 if charge else 5.2
    fig, ax = plt.subplots(figsize=(larg * 0.95, 4.6)); ax.axis("off"); ax.set_aspect("equal")
    top, bas, xs, xr, xo = 4.0, 0.0, 0.0, 2.4, 3.9
    xd = xo + (1.4 if charge else 0)                         # extrémité droite du circuit
    source_tension(ax, xs, bas, top, u[1])
    line(ax, [(xs, top), (xr, top)]); line(ax, [(xs, bas), (xd, bas)])
    resistance(ax, xr, 2.0, top, *r1)
    resistance(ax, xr, bas, 2.0, *r2)
    noeud(ax, xr, 2.0); noeud(ax, xr, bas)
    line(ax, [(xr, 2.0), (xd, 2.0)])
    if charge:
        resistance(ax, xd, bas, 2.0, *charge)
    else:
        borne(ax, xo, 2.0); borne(ax, xo, bas)
    fleche_tension(ax, xs, bas, top, u[0])
    if u1:
        fleche_tension(ax, xr, 2.0, top, u1)
    fleche_tension(ax, xr, bas, 2.0, u2)
    if courant:
        fleche_courant(ax, 1.0, top, 1.7, top, courant, decal=(0.0, 0.3))
    masse(ax, xr, bas)                                         # sous le nœud du bas de R2
    ax.set_xlim(-1.3, xd + 0.9); ax.set_ylim(-0.6, top + 0.6)
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
