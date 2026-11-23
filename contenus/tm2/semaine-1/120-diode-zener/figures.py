# -*- coding: utf-8 -*-
"""Figures de la séance TM2 120 « Diode et diode Zener » (avec la LED) : jonction PN, polarisation, symboles CEI 60617-5
et boîtiers, caractéristiques I(U) de la diode au silicium et de la diode Zener, modèles, LED, schémas du fil rouge
(équipement de test) et circuits de l'exercice N°1.
Conventions de moteur/cei.py (REGLES 3.3) : flèches de tension bleues à droite, du + vers le − ; noms et valeurs à gauche.
Les modèles numériques ci-dessous servent aussi à la fiche 130 et à verif.py."""
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Polygon, Ellipse
from moteur.cei import (save, line, K, NAVY, BLUE, LBLUE, TINT, RED, GR, resistance, source_tension, masse, noeud, borne,
                        fleche_tension, fleche_courant, diode, fig_eq_txt)

# ---------------------------------------------------------------- modèles (repris par la fiche et par verif.py)
IS, N_UT, RS = 10e-9, 1.9 * 0.02585, 2.0       # diode Si d'exercice : courant de saturation [A], n·U_T [V], résistance série [Ω]


def u_diode(i):
    """Tension directe de la diode Si d'exercice pour un courant i [A] (Shockley + résistance série)."""
    return N_UT * math.log(i / IS + 1) + RS * i


UZ0, RZ = 5.05, 10.0                           # Zener d'exercice : U_Z = 5,1 V à 5 mA, r_Z = 10 Ω


def u_zener(i):
    """Tension inverse de la Zener d'exercice pour un courant inverse i [A] (droite de pente r_Z, coude sous 2 mA)."""
    return UZ0 + RZ * i - 0.08 * math.exp(-i / 1e-3)


P_TOT_Z = 0.5                                  # BZX55C5V1 : P_tot = 500 mW


# ---------------------------------------------------------------- 1. la jonction PN au repos
def _porteurs(ax, x0, x1, y0, y1, genre, n=10, graine=1, eviter=()):
    import random
    r = random.Random(graine)
    pts, ev = [], list(eviter)
    for _ in range(400):
        if len(pts) >= n:
            break
        x, y = r.uniform(x0 + 0.2, x1 - 0.2), r.uniform(y0 + 0.25, y1 - 0.25)
        if any((x - a) ** 2 + (y - b) ** 2 < 0.45 ** 2 for a, b in pts + ev):
            continue
        pts.append((x, y))
    for x, y in pts:
        if genre == "trou":
            ax.add_patch(Circle((x, y), 0.15, fc="white", ec=RED, lw=1.6, zorder=4))
            ax.text(x, y, "+", ha="center", va="center", fontsize=9, color=RED, fontweight="bold", zorder=5)
        else:
            ax.add_patch(Circle((x, y), 0.15, fc=BLUE, ec=NAVY, lw=1.2, zorder=4))
            ax.text(x, y, "−", ha="center", va="center", fontsize=9, color="white", fontweight="bold", zorder=5)


def _ions(ax, xg, xd, y0, y1):
    """Ions fixes de la zone de déplétion : négatifs côté p (à gauche), positifs côté n (à droite)."""
    xm = (xg + xd) / 2
    for y in [y0 + 0.35 + k * 0.55 for k in range(int((y1 - y0 - 0.3) / 0.55))]:
        for x, s, c in ((xg + (xm - xg) / 2, "−", NAVY), (xm + (xd - xm) / 2, "+", RED)):
            ax.add_patch(Rectangle((x - 0.13, y - 0.13), 0.26, 0.26, fc="white", ec=c, lw=1.3, zorder=4))
            ax.text(x, y, s, ha="center", va="center", fontsize=9, color=c, fontweight="bold", zorder=5)


def jonction(ax, larg_zone, y0=0.0, titre=None, eviter=()):
    L, H = 8.0, 2.2
    xm = L / 2
    xg, xd = xm - larg_zone / 2, xm + larg_zone / 2
    ax.add_patch(Rectangle((0, y0), xg, H, fc=TINT, ec="none"))
    ax.add_patch(Rectangle((xd, y0), L - xd, H, fc=LBLUE, ec="none"))
    ax.add_patch(Rectangle((xg, y0), larg_zone, H, fc="white", ec=GR, lw=1.0, ls="--"))
    ax.add_patch(Rectangle((0, y0), L, H, fill=False, ec=NAVY, lw=1.8))
    _porteurs(ax, 0, xg, y0, y0 + H, "trou", n=int(2.2 * xg), graine=3, eviter=eviter)
    _porteurs(ax, xd, L, y0, y0 + H, "e", n=int(2.2 * (L - xd)), graine=5, eviter=eviter)
    _ions(ax, xg, xd, y0, y0 + H)
    ax.text(0.15, y0 + H + 0.2, "zone p", fontsize=14, color=NAVY, fontweight="bold", va="bottom")
    ax.text(L - 0.15, y0 + H + 0.2, "zone n", fontsize=14, color=NAVY, fontweight="bold", va="bottom", ha="right")
    if titre:
        ax.text(xm, y0 + H + 0.2, titre, fontsize=12.5, color=GR, ha="center", va="bottom")
    return L, H, xg, xd


def fig_jonction(nom="fig_jonction.png"):
    fig, ax = plt.subplots(figsize=(7.6, 3.6)); ax.axis("off"); ax.set_aspect("equal")
    L, H, xg, xd = jonction(ax, 1.6, titre="zone de déplétion")
    ax.annotate("", xy=(xg, -0.35), xytext=(xd, -0.35), arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.4))
    ax.text(L / 2, -0.55, "pas de porteurs libres : un isolant", ha="center", va="top", fontsize=12.5, color=NAVY)
    # légende
    for k, (x, txt) in enumerate([(0.2, "trou (zone p)"), (2.9, "électron libre (zone n)"), (6.1, "ion fixe")]):
        y = -1.55
        if k == 0:
            ax.add_patch(Circle((x, y), 0.15, fc="white", ec=RED, lw=1.6)); ax.text(x, y, "+", ha="center", va="center", fontsize=9, color=RED, fontweight="bold")
        elif k == 1:
            ax.add_patch(Circle((x, y), 0.15, fc=BLUE, ec=NAVY)); ax.text(x, y, "−", ha="center", va="center", fontsize=9, color="white", fontweight="bold")
        else:
            ax.add_patch(Rectangle((x - 0.13, y - 0.13), 0.26, 0.26, fc="white", ec=NAVY, lw=1.3))
        ax.text(x + 0.28, y, txt, va="center", fontsize=11.5, color=K)
    ax.set_xlim(-0.2, L + 0.2); ax.set_ylim(-1.9, H + 0.75)
    save(fig, nom)


def fig_jonction_pol(nom, sens):
    """Jonction avec une pile : « direct » (+ sur p, zone mince, courant) ou « inverse » (+ sur n, zone large, pas de courant)."""
    fig, ax = plt.subplots(figsize=(7.6, 3.5)); ax.axis("off"); ax.set_aspect("equal")
    L, H, xg, xd = jonction(ax, 0.5 if sens == "direct" else 3.0)
    # fils et pile
    yb = -1.1
    line(ax, [(0, H / 2), (-0.5, H / 2), (-0.5, yb), (3.2, yb)], lw=1.8); line(ax, [(3.2, yb), (4.8, yb)], lw=0.01, c="white")
    line(ax, [(L, H / 2), (L + 0.5, H / 2), (L + 0.5, yb), (4.8, yb)], lw=1.8)
    plus_gauche = sens == "direct"
    xp, xn = (3.2, 4.8) if plus_gauche else (4.8, 3.2)          # pile : trait long et fin = +, trait court et épais = −
    line(ax, [(xp, yb - 0.4), (xp, yb + 0.4)], lw=1.8); line(ax, [(xn, yb - 0.2), (xn, yb + 0.2)], lw=4.5)
    ax.text(xp, yb + 0.5, "+", ha="center", fontsize=16, color=RED, fontweight="bold")
    ax.text(xn, yb + 0.5, "−", ha="center", fontsize=16, color=NAVY, fontweight="bold")
    if sens == "direct":
        ax.annotate("", xy=(5.6, H + 0.75), xytext=(2.4, H + 0.75), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2), zorder=6)
        ax.text(4.0, H + 0.95, "courant $I$", ha="center", va="bottom", fontsize=12.5, color=RED, fontweight="bold")
        ax.text(L / 2, yb - 0.45, "sens direct : zone mince, le courant passe", ha="center", va="top", fontsize=12.5, color=NAVY, fontweight="bold")
    else:
        ax.text(L / 2, yb - 0.45, "sens inverse : zone large, pas de courant", ha="center", va="top", fontsize=12.5, color=NAVY, fontweight="bold")
    ax.set_xlim(-0.8, L + 0.8); ax.set_ylim(yb - 1.0, H + 1.4)
    save(fig, nom)


# ---------------------------------------------------------------- 2. circuits élémentaires (polarisation, exercice N°1)
def _element(ax, x, y0, y1, el, fs=15):
    """el = (« R », nom, valeur) ou (« D », sens, genre, nom, valeur)."""
    if el[0] == "R":
        resistance(ax, x, y0, y1, el[1], el[2], fs=fs)
    else:
        diode(ax, x, y0, y1, sens=el[1], genre=el[2], nom=el[3], valeur=el[4], fs=fs)


def circuit(nom, haut, bas, u="9 V", inverse=False, fleches=(), courant=None, titre=None, ecart_led=0.95, fs=19):
    """Source à gauche, deux éléments en série dans la branche de droite (haut puis bas).
    fleches : [(élément « haut » ou « bas », nom de la tension, sens « bas » si le + est en haut)] ;
    inverse : source retournée (+ en bas)."""
    fig, ax = plt.subplots(figsize=(3.9, 4.6)); ax.axis("off"); ax.set_aspect("equal")
    top, bot, xs, xr = 4.0, 0.0, 0.0, 2.6
    source_tension(ax, xs, bot, top, u, fs=fs - 1)
    yp, ym_ = (bot, top) if inverse else (top, bot)
    fleche_tension(ax, xs, ym_, yp, "$U$", fs=fs)
    ax.text(xs - 0.22, yp + (-0.38 if not inverse else 0.38), "+", ha="center", va="center", fontsize=15, color=RED, fontweight="bold")
    line(ax, [(xs, top), (xr, top)]); line(ax, [(xs, bot), (xr, bot)])
    _element(ax, xr, 2.0, top, haut, fs); _element(ax, xr, bot, 2.0, bas, fs)
    for qui, nom_u, sens in fleches:
        y0, y1 = (2.0, top) if qui == "haut" else (bot, 2.0)
        el = haut if qui == "haut" else bas
        ec = ecart_led if (el[0] == "D" and el[2] == "led") else 0.55
        if sens == "bas":
            fleche_tension(ax, xr, y0, y1, nom_u, ecart=ec, fs=fs)
        else:
            fleche_tension(ax, xr, y1, y0, nom_u, ecart=ec, fs=fs)
    if courant:
        fleche_courant(ax, 0.9, top, 1.6, top, courant, decal=(0.0, 0.5), fs=fs - 1)
    if titre:
        ax.text(1.3, -0.45, titre, ha="center", va="top", fontsize=17, color=NAVY, fontweight="bold")
    ax.set_xlim(-1.9, xr + 2.2); ax.set_ylim(-1.0 if titre else -0.4, top + 0.9)
    save(fig, nom)


# ---------------------------------------------------------------- 3. symboles et boîtiers
def fig_symboles(nom="fig_symboles.png"):
    fig, ax = plt.subplots(figsize=(7.4, 3.3)); ax.axis("off"); ax.set_aspect("equal")
    for k, (genre, titre) in enumerate([("diode", "diode"), ("zener", "diode Zener"), ("led", "LED")]):
        x = 1.2 + k * 3.0
        diode(ax, x, 0.4, 2.6, sens="bas", genre=genre)
        ax.text(x - 0.25, 2.55, "A", ha="right", va="center", fontsize=15, color=NAVY, fontweight="bold")
        ax.text(x - 0.25, 0.45, "K", ha="right", va="center", fontsize=15, color=NAVY, fontweight="bold")
        ax.text(x, -0.05, titre, ha="center", va="top", fontsize=14, color=K, fontweight="bold")
    ax.text(4.2, -0.65, "A : anode · K : cathode · la pointe du triangle montre le sens du courant direct",
            ha="center", va="top", fontsize=11, color=GR)
    ax.set_xlim(-0.3, 8.8); ax.set_ylim(-1.1, 2.9)
    save(fig, nom)


def fig_boitiers(nom="fig_boitiers.png"):
    fig, ax = plt.subplots(figsize=(7.4, 3.3)); ax.axis("off"); ax.set_aspect("equal")
    # diode axiale : corps noir, anneau gris côté cathode
    y = 1.6
    line(ax, [(0.0, y), (1.0, y)], lw=2.2, c=GR); line(ax, [(3.0, y), (4.0, y)], lw=2.2, c=GR)
    ax.add_patch(FancyBboxPatch((1.0, y - 0.35), 2.0, 0.7, boxstyle="round,pad=0.02,rounding_size=0.15", fc="#2B2B2B", ec="#2B2B2B"))
    ax.add_patch(Rectangle((2.55, y - 0.36), 0.22, 0.72, fc="#C9CED8", ec="none"))
    ax.text(0.0, y + 0.3, "A", fontsize=16, color=NAVY, fontweight="bold"); ax.text(3.85, y + 0.3, "K", fontsize=16, color=NAVY, fontweight="bold")
    ax.text(2.0, y - 0.65, "l'anneau marque la cathode", ha="center", va="top", fontsize=14, color=K)
    # LED 5 mm : dôme, collerette avec méplat côté cathode, patte longue = anode
    xc = 7.6
    ax.add_patch(Rectangle((xc - 0.55, 1.6), 1.1, 1.0, fc="#F4A6A6", ec=RED, lw=1.5))
    ax.add_patch(Ellipse((xc, 2.6), 1.1, 0.9, fc="#F4A6A6", ec=RED, lw=1.5))
    ax.add_patch(Rectangle((xc - 0.55, 2.55), 1.1, 0.1, fc="#F4A6A6", ec="none"))
    ax.add_patch(Rectangle((xc - 0.7, 1.45), 1.3, 0.18, fc="#E58C8C", ec=RED, lw=1.2))   # collerette, méplat à droite (cathode)
    line(ax, [(xc - 0.25, 1.45), (xc - 0.25, 0.0)], lw=2.2, c=GR)                         # anode : patte longue
    line(ax, [(xc + 0.25, 1.45), (xc + 0.25, 0.45)], lw=2.2, c=GR)                        # cathode : patte courte
    ax.text(xc - 0.45, 0.25, "A", ha="right", fontsize=16, color=NAVY, fontweight="bold")
    ax.text(xc + 0.45, 0.6, "K", ha="left", fontsize=16, color=NAVY, fontweight="bold")
    ax.text(xc + 0.85, 1.55, "méplat\n= cathode", ha="left", va="center", fontsize=13, color=K)
    ax.text(xc - 0.75, 0.85, "patte longue\n= anode", ha="right", va="center", fontsize=13, color=K)
    ax.set_xlim(-0.3, 10.0); ax.set_ylim(-0.1, 3.2)
    save(fig, nom)


# ---------------------------------------------------------------- 4. caractéristiques
def _lisible(ax, graduations=13, axes=15):
    """Graduations et titres d'axes lisibles une fois la figure réduite (fiche : 8,6 cm ; présentation : 4,6")."""
    ax.tick_params(labelsize=graduations)
    ax.xaxis.label.set_fontsize(axes); ax.yaxis.label.set_fontsize(axes)


def _axes_croix(ax):
    ax.spines["left"].set_position("zero"); ax.spines["bottom"].set_position("zero")
    for sp in ("right", "top"):
        ax.spines[sp].set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])


def fig_carac_complete(nom, zener=False):
    """Allure de la caractéristique complète (échelles différentes dans chaque quadrant)."""
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    _axes_croix(ax)
    ud = [k / 100 for k in range(0, 81)]
    ax.plot([u * 10 for u in ud], [3 * (math.exp(u / 0.06) - 1) / (math.exp(0.8 / 0.06) - 1) for u in ud], color=BLUE, lw=2.8)
    xc = -3.0 if zener else -6.0
    ax.plot([xc, 0.0], [-0.08, -0.03], color=BLUE, lw=2.8)
    ax.plot([xc - 0.25 * k / 20 for k in range(21)], [-0.08 - (k / 20) ** 2.5 * 2.4 for k in range(21)], color=RED if zener else BLUE, lw=2.8)
    ax.set_xlim(-7.4, 8.8); ax.set_ylim(-2.8, 3.3)
    ax.text(8.7, -0.18, "$U$ [V]", ha="right", va="top", fontsize=12, color=NAVY)
    ax.text(0.15, 3.25, "$I$ [mA]", ha="left", va="top", fontsize=12, color=NAVY)
    ax.plot([7.0, 7.0], [0, 0.1], color=NAVY, lw=1.2)
    ax.text(7.0, -0.18, "0,7", ha="center", va="top", fontsize=11, color=NAVY)
    ax.text(5.6, 2.3, "sens direct :\nla diode conduit", ha="right", va="center", fontsize=11.5, color=NAVY, fontweight="bold")
    ax.text(-0.4, 0.9, "sens inverse : bloquée\n(courant de fuite : µA ou nA)", ha="right", va="bottom", fontsize=11, color=NAVY)
    if zener:
        ax.text(xc + 0.15, 0.12, "$-U_\\mathrm{Z}$", ha="left", va="bottom", fontsize=12, color=RED, fontweight="bold")
        ax.text(xc - 0.45, -1.5, "claquage utilisé :\n$U$ reste ≈ $U_\\mathrm{Z}$", ha="right", va="center", fontsize=11.5, color=RED, fontweight="bold")
    else:
        ax.text(xc + 0.15, 0.12, "$-U_\\mathrm{BR}$", ha="left", va="bottom", fontsize=12, color=NAVY)
        ax.text(xc + 0.35, -1.5, "claquage :\ndiode détruite", ha="left", va="center", fontsize=11.5, color=RED, fontweight="bold")
    ax.text(-7.3, 3.2, "allure, échelles différentes", fontsize=10, color=GR, style="italic", va="top")
    save(fig, nom)


def fig_carac_directe(nom="fig_carac_directe.png", reperes=True):
    """Caractéristique directe de la diode Si d'exercice, à l'échelle, quadrillée pour les lectures."""
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    i = [k * 1e-5 for k in range(1, 4001)]
    ax.plot([u_diode(x) for x in i], [x * 1e3 for x in i], color=BLUE, lw=2.6)
    ax.plot([0, u_diode(1e-5)], [0, 0.01], color=BLUE, lw=2.6)
    ax.set_xlim(0, 1.0); ax.set_ylim(0, 40)
    ax.set_xticks([k / 10 for k in range(11)]); ax.set_xticklabels([("%.1f" % (k / 10)).replace(".", ",") for k in range(11)])
    ax.set_yticks(range(0, 41, 5))
    ax.grid(True, color="#D5DAE3", lw=0.7)
    ax.set_xlabel("$U_\\mathrm{F}$ [V]", fontsize=13, color=NAVY); ax.set_ylabel("$I_\\mathrm{F}$ [mA]", fontsize=13, color=NAVY)
    for sp in ("right", "top"):
        ax.spines[sp].set_visible(False)
    if reperes:
        u10 = u_diode(10e-3)
        ax.plot([u10, u10], [0, 10], color=RED, lw=1.4, ls="--"); ax.plot([0, u10], [10, 10], color=RED, lw=1.4, ls="--")
        ax.plot(u10, 10, "o", color=RED, ms=7)
        ax.text(u10 + 0.03, 9, "10 mA → 0,7 V", color=RED, fontsize=12, fontweight="bold", va="top")
        ax.text(0.05, 33, "en dessous de ≈ 0,6 V :\npresque pas de courant", fontsize=11.5, color=NAVY)
    _lisible(ax)
    save(fig, nom)


def fig_carac_zener(nom="fig_carac_zener.png", reperes=False):
    """Zone de claquage de la Zener d'exercice, sens inverse (U_Z et I_Z comptés positifs), quadrillée pour les lectures."""
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    i = [k * 1e-5 for k in range(0, 4001)]
    ax.plot([u_zener(x) for x in i], [x * 1e3 for x in i], color=RED, lw=2.6)
    ax.plot([4.75, u_zener(0)], [0, 0], color=RED, lw=2.6)
    ax.set_xlim(4.8, 5.6); ax.set_ylim(0, 40)
    xt = [4.8 + k / 10 for k in range(9)]
    ax.set_xticks(xt); ax.set_xticklabels([("%.1f" % x).replace(".", ",") for x in xt])
    ax.set_yticks(range(0, 41, 5))
    ax.grid(True, color="#D5DAE3", lw=0.7)
    ax.set_xlabel("$U_\\mathrm{Z}$ [V] (sens inverse)", fontsize=13, color=NAVY); ax.set_ylabel("$I_\\mathrm{Z}$ [mA]", fontsize=13, color=NAVY)
    for sp in ("right", "top"):
        ax.spines[sp].set_visible(False)
    if reperes:
        for ii in (5e-3, 25e-3):
            u = u_zener(ii)
            ax.plot([u, u], [0, ii * 1e3], color=NAVY, lw=1.3, ls="--"); ax.plot([4.8, u], [ii * 1e3, ii * 1e3], color=NAVY, lw=1.3, ls="--")
            ax.plot(u, ii * 1e3, "o", color=NAVY, ms=7)
        ax.text(5.24, 31, "$\\Delta U_\\mathrm{Z}$ = 0,2 V\n$\\Delta I_\\mathrm{Z}$ = 20 mA", fontsize=12, color=NAVY, fontweight="bold", va="bottom", ha="right")
    _lisible(ax)
    save(fig, nom)


def fig_modeles(nom="fig_modeles.png"):
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.4))
    i = [k * 1e-5 for k in range(1, 3001)]
    for ax, (titre, us) in zip(axs, [("diode idéale", 0.0), ("diode avec seuil", 0.7)]):
        ax.plot([u_diode(x) for x in i], [x * 1e3 for x in i], color="#B8C0CE", lw=2.0, ls="--")
        ax.plot([-0.4, us, us], [0, 0, 30], color=BLUE, lw=3.0)
        ax.set_xlim(-0.4, 1.0); ax.set_ylim(-2, 30)
        ax.axhline(0, color=K, lw=0.8); ax.axvline(0, color=K, lw=0.8)
        ax.set_xticks([0, 0.7]); ax.set_xticklabels(["0", "0,7"], fontsize=12); ax.set_yticks([])
        ax.set_xlabel("$U$ [V]", fontsize=13, color=NAVY)
        ax.set_title(titre, fontsize=15, color=NAVY, fontweight="bold")
        for sp in ("right", "top", "left"):
            ax.spines[sp].set_visible(False)
    axs[1].text(-0.36, 22, "$U_\\mathrm{F}$ = 0,7 V\ndès que\nla diode\nconduit", fontsize=12, color=NAVY, va="top")
    for ax in axs:
        _lisible(ax)
    axs[0].text(0.05, 22, "interrupteur :\nfermé en direct,\nouvert en inverse", fontsize=12, color=NAVY, va="top")
    fig.tight_layout()
    save(fig, nom)


# ---------------------------------------------------------------- 5. la LED
def fig_led_principe(nom="fig_led_principe.png"):
    fig, ax = plt.subplots(figsize=(7.4, 3.4)); ax.axis("off"); ax.set_aspect("equal")
    L, H, xg, xd = jonction(ax, 0.5, eviter=[(4.0 + 0.5, 1.1), (4.0 - 0.5, 1.1)])
    xm = L / 2
    # un électron et un trou se rencontrent : lumière
    ax.add_patch(Circle((xm + 0.5, 1.1), 0.17, fc=BLUE, ec=NAVY, zorder=6)); ax.text(xm + 0.5, 1.1, "−", ha="center", va="center", fontsize=9, color="white", fontweight="bold", zorder=7)
    ax.add_patch(Circle((xm - 0.5, 1.1), 0.17, fc="white", ec=RED, lw=1.8, zorder=6)); ax.text(xm - 0.5, 1.1, "+", ha="center", va="center", fontsize=9, color=RED, fontweight="bold", zorder=7)
    xs = [xm + k / 40 * 1.2 for k in range(41)]
    ax.plot(xs, [H + 0.9 + 0.12 * math.sin(k / 40 * 6 * math.pi) for k in range(41)], color=RED, lw=2.2, zorder=6)
    ax.annotate("", xy=(xm + 1.45, H + 0.9), xytext=(xm + 1.2, H + 0.9), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2))
    ax.annotate("", xy=(xm + 0.05, H + 0.75), xytext=(xm, 1.35), arrowprops=dict(arrowstyle="-", color=GR, lw=1.2, ls=":"))
    ax.text(xm + 1.6, H + 0.9, "lumière", va="center", fontsize=14, color=RED, fontweight="bold")
    ax.text(xm, -0.25, "un électron retombe dans un trou : l'énergie sort en lumière", ha="center", va="top", fontsize=12.5, color=NAVY)
    ax.set_xlim(-0.2, L + 0.2); ax.set_ylim(-0.8, H + 1.4)
    save(fig, nom)


# ---------------------------------------------------------------- 6. schémas du fil rouge (équipement de test)
def fig_anti_inversion(nom="fig_anti_inversion.png"):
    fig, ax = plt.subplots(figsize=(4.4, 4.6)); ax.axis("off"); ax.set_aspect("equal")
    top, bot, xs, xr = 4.0, 0.0, 0.0, 2.6
    source_tension(ax, xs, bot, top, "24 V", fs=18)
    fleche_tension(ax, xs, bot, top, "$U$", fs=19)
    ax.text(xs - 0.22, top - 0.38, "+", ha="center", va="center", fontsize=15, color=RED, fontweight="bold")
    line(ax, [(xs, top), (xr, top)]); line(ax, [(xs, bot), (xr, bot)])
    diode(ax, xr, 2.6, top, sens="bas", nom="$D_1$", valeur="1N4007", fs=19)
    line(ax, [(xr, 2.6), (xr, 2.3)])
    ax.add_patch(Rectangle((xr - 0.75, 0.55), 1.5, 1.75, fc=TINT, ec=NAVY, lw=1.8))
    ax.text(xr, 1.42, "carte de\nl'équipe-\nment", ha="center", va="center", fontsize=15, color=NAVY)
    line(ax, [(xr, 0.55), (xr, bot)])
    fleche_courant(ax, 0.9, top, 1.6, top, "$I$", decal=(0.0, 0.3), fs=18)
    masse(ax, 1.3, bot, fs=15)
    ax.set_xlim(-2.0, xr + 1.4); ax.set_ylim(-0.6, top + 0.5)
    save(fig, nom)


def fig_zener_entree(nom="fig_zener_entree.png"):
    fig, ax = plt.subplots(figsize=(5.4, 4.6)); ax.axis("off"); ax.set_aspect("equal")
    top, bot, xs, xr, xo = 4.0, 0.0, 0.0, 2.6, 4.3
    source_tension(ax, xs, bot, top, "0 à 24 V", fs=17)
    fleche_tension(ax, xs, bot, top, "$U_\\mathrm{e}$", fs=19)
    line(ax, [(xs, top), (xr, top)]); line(ax, [(xs, bot), (xo, bot)])
    resistance(ax, xr, 2.0, top, "$R_1$", "2k2", fs=19)
    diode(ax, xr, bot, 2.0, sens="haut", genre="zener", nom="$D_\\mathrm{Z}$", valeur="5V1", fs=19)
    noeud(ax, xr, 2.0); noeud(ax, xr, bot)
    line(ax, [(xr, 2.0), (xo, 2.0)])
    borne(ax, xo, 2.0); borne(ax, xo, bot)
    fleche_tension(ax, xo, bot, 2.0, "$U_\\mathrm{s}$", ecart=0.4, fs=19)
    ax.text(xo + 0.15, 2.35, "vers l'entrée\ndu contrôleur", fontsize=15, color=GR, ha="center", va="bottom")
    masse(ax, xr, bot, fs=15)
    ax.set_xlim(-3.0, xo + 1.6); ax.set_ylim(-0.6, top + 0.5)
    save(fig, nom)


def fig_led_voyant(nom="fig_led_voyant.png"):
    circuit(nom, ("R", "$R_1$", "2k2"), ("D", "bas", "led", "$D_1$", "rouge"), u="24 V",
            fleches=[("bas", "$U_\\mathrm{F}$", "bas")], courant="$I_\\mathrm{F}$")


def produire(ctx):
    import moteur.cei as cei
    cei.ecrire_dans(ctx.images)
    fig_jonction(); fig_jonction_pol("fig_pol_directe.png", "direct"); fig_jonction_pol("fig_pol_inverse.png", "inverse")
    circuit("fig_circ_directe.png", ("R", "$R_1$", "1k"), ("D", "bas", "diode", "$D_1$", None),
            fleches=[("haut", "$U_\\mathrm{R}$", "bas"), ("bas", "$U_\\mathrm{F}$", "bas")], courant="$I$", titre="sens direct")
    circuit("fig_circ_inverse.png", ("R", "$R_1$", "1k"), ("D", "haut", "diode", "$D_1$", None),
            fleches=[("bas", "$U_\\mathrm{D}$", "bas")], courant="$I = 0$", titre="sens inverse")
    fig_symboles(); fig_boitiers()
    fig_carac_complete("fig_carac_diode.png"); fig_carac_complete("fig_carac_zener_allure.png", zener=True)
    fig_carac_directe(); fig_carac_directe("fig_carac_directe_ex.png", reperes=False)
    fig_carac_zener("fig_carac_zener.png", reperes=True); fig_carac_zener("fig_carac_zener_ex.png")
    fig_modeles(); fig_led_principe()
    fig_anti_inversion(); fig_zener_entree(); fig_led_voyant()
    # exercice N°1 : quatre circuits, la LED s'allume-t-elle ?
    circuit("fig_ex1_a.png", ("D", "bas", "diode", "$D_1$", None), ("D", "bas", "led", "$D_2$", None), titre="a)")
    circuit("fig_ex1_b.png", ("D", "haut", "diode", "$D_1$", None), ("D", "bas", "led", "$D_2$", None), titre="b)")
    circuit("fig_ex1_c.png", ("R", "$R_1$", "1k"), ("D", "haut", "led", "$D_1$", None), titre="c)")
    circuit("fig_ex1_d.png", ("R", "$R_1$", "1k"), ("D", "haut", "led", "$D_1$", None), inverse=True, titre="d)")
    # équations (image de secours des équations éditables de la présentation)
    fig_eq_txt(r"r_\mathrm{Z} = \frac{\Delta U_\mathrm{Z}}{\Delta I_\mathrm{Z}}", "eq_rz.png")
    fig_eq_txt(r"P_\mathrm{Z} = U_\mathrm{Z} \cdot I_\mathrm{Z}", "eq_pz.png")
    fig_eq_txt(r"I_\mathrm{Zmax} = \frac{P_\mathrm{tot}}{U_\mathrm{Z}}", "eq_izmax.png")
    fig_eq_txt(r"I_\mathrm{Zmax} = \frac{500\ [\mathrm{mW}]}{5{,}1\ [\mathrm{V}]} = 98{,}04\ [\mathrm{mA}]", "eq_izmax_an.png")
    fig_eq_txt(r"r_\mathrm{Z} = \frac{5{,}3\ [\mathrm{V}] - 5{,}1\ [\mathrm{V}]}{25\ [\mathrm{mA}] - 5\ [\mathrm{mA}]} = 10\ [\Omega]", "eq_rz_an.png")
