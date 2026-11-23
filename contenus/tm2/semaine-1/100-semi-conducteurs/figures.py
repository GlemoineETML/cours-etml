# -*- coding: utf-8 -*-
"""Figures de la séance TM2 100 « Semi-conducteurs » : échelle des résistivités, électrons de valence,
cristal de silicium (paire électron-trou, dopé n, dopé p), dérive dans un champ électrique, effet de la température.
Couleurs ETML ; axes avec grandeur et unité (REGLES 3.3)."""
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Polygon
from moteur.cei import save, line, K, NAVY, BLUE, LBLUE, TINT, RED, GR

# ---------------------------------------------------------------- données (reprises par la présentation, la fiche et verif.py)
RHO = {          # résistivité à 20 °C [Ω·m] (tables usuelles ; silicium et germanium purs : valeurs à 300 K)
    "Argent": 1.6e-8, "Cuivre": 1.78e-8, "Aluminium": 2.78e-8, "Nichrome": 1.1e-6,
    "Silicium dopé n": 5e-2, "Germanium pur": 0.46, "Silicium pur": 2.3e3,
    "Porcelaine": 1e12, "PVC": 1e13,
}
ALPHA_CU = 0.0039   # coefficient de température du cuivre [1/K]
EG_SI = 1.12        # largeur de la bande interdite du silicium [eV]
K_B = 8.617e-5      # constante de Boltzmann [eV/K]


def r_si_relatif(theta, ref=20.0):
    """Résistance du silicium pur rapportée à sa valeur à 20 °C : porteurs n_i ∝ T^1,5 · e^(−Eg/2kT),
    mobilité ∝ T^−2,4 (allure seulement)."""
    def sigma(t):
        T = t + 273.15
        return T ** 1.5 * math.exp(-EG_SI / (2 * K_B * T)) * T ** -2.4
    return sigma(ref) / sigma(theta)


# ---------------------------------------------------------------- 1. échelle des résistivités
def echelle_rho(nom="fig_echelle_rho.png"):
    fig, ax = plt.subplots(figsize=(10, 3.1))
    lo, hi = -9, 16
    zones = [(-9, -5, LBLUE, "Conducteurs"), (-5, 8, TINT, "Semi-conducteurs"), (8, 16, "#D9DCE6", "Isolants")]
    for a, b, c, t in zones:
        ax.add_patch(Rectangle((a, -0.35), b - a, 0.7, fc=c, ec="none"))
        ax.text((a + b) / 2, 0.0, t, ha="center", va="center", fontsize=14, fontweight="bold", color=NAVY)
    pts = [("Cuivre", "Cuivre", 1, 1.0), ("Nichrome", "Nichrome\n(fil chauffant)", -1, 1.0),
           ("Silicium dopé n", "Silicium\ndopé n", 1, 1.0), ("Germanium pur", "Germanium\npur", -1, 1.0),
           ("Silicium pur", "Silicium\npur", 1, 1.0), ("Porcelaine", "Porcelaine", -1, 1.0), ("PVC", "PVC", 1, 1.0)]
    for cle, lab, s, _ in pts:
        x = math.log10(RHO[cle])
        ax.plot([x, x], [s * 0.35, s * 0.75], color=K, lw=1.5)
        ax.plot(x, s * 0.35, marker="v" if s > 0 else "^", color=BLUE, ms=9)
        ax.text(x, s * 0.82, lab, ha="center", va="bottom" if s > 0 else "top", fontsize=11.5, color=K)
    ax.set_xlim(lo, hi); ax.set_ylim(-1.75, 1.75)
    ax.set_yticks([])
    ax.set_xticks(range(lo, hi + 1, 2))
    ax.set_xticklabels(["$10^{%d}$" % e for e in range(lo, hi + 1, 2)], fontsize=11)
    ax.set_xlabel("Résistivité ρ [Ω·m] (échelle logarithmique)", fontsize=12, color=NAVY)
    for sp in ("left", "right", "top"):
        ax.spines[sp].set_visible(False)
    ax.text(hi, -1.7, "limites des zones : ordres de grandeur", ha="right", va="bottom", fontsize=9.5, color=GR, style="italic")
    save(fig, nom)


# ---------------------------------------------------------------- 2. électrons de valence
def atome(ax, x, y, symbole, coeur, n_val, r=1.1):
    ax.add_patch(Circle((x, y), r, fill=False, ec=GR, lw=1.4, ls="--"))
    ax.add_patch(Circle((x, y), 0.48, fc=NAVY, ec=NAVY))
    ax.text(x, y + 0.08, symbole, ha="center", va="center", fontsize=18, color="white", fontweight="bold")
    ax.text(x, y - 0.23, coeur, ha="center", va="center", fontsize=12, color="white")
    for k in range(n_val):
        a = math.pi / 2 + 2 * math.pi * k / n_val
        ax.add_patch(Circle((x + r * math.cos(a), y + r * math.sin(a)), 0.13, fc=BLUE, ec=BLUE, zorder=4))


def valence(nom="fig_valence.png"):
    fig, ax = plt.subplots(figsize=(7.4, 3.6)); ax.axis("off"); ax.set_aspect("equal")
    for x, sym, coeur, n, t1, t2 in [(0, "Cu", "+1", 1, "Cuivre : 1 électron de valence", "très peu lié : il devient libre"),
                                    (6.0, "Si", "+4", 4, "Silicium : 4 électrons de valence", "chacun forme une liaison")]:
        atome(ax, x, 0, sym, coeur, n)
        ax.text(x, -1.6, t1, ha="center", va="center", fontsize=15, color=NAVY, fontweight="bold")
        ax.text(x, -2.05, t2, ha="center", va="center", fontsize=14, color=GR)
    ax.add_patch(Circle((-0.4, -2.75), 0.13, fc=BLUE, ec=BLUE)); ax.text(-0.2, -2.75, "électron de valence", va="center", fontsize=13, color=K)
    ax.add_patch(Circle((3.4, -2.75), 0.13, fc=NAVY, ec=NAVY)); ax.text(3.6, -2.75, "noyau et couches internes", va="center", fontsize=13, color=K)
    ax.set_xlim(-2.2, 8.2); ax.set_ylim(-3.1, 1.45)
    save(fig, nom)


# ---------------------------------------------------------------- 4. cristal de silicium (représentation plane)
def cristal(nom, centre="Si", mode=None, legende=None, grand=False):
    """mode : None (pur), « paire » (une liaison rompue), « n » (phosphore), « p » (bore).
    grand : étiquettes agrandies et sans légende, pour une figure affichée en petit (dopage n et p côte à côte)."""
    k = 1.6 if grand else 1.0
    fig, ax = plt.subplots(figsize=(5.2, 5.2)); ax.axis("off"); ax.set_aspect("equal")
    d = 2.0
    pos = [(i * d, j * d) for j in range(3) for i in range(3)]

    def paire(x0, y0, x1, y1, manque=None):
        """deux électrons sur la liaison ; manque = 0 ou 1 : électron absent (trou)."""
        dx, dy = x1 - x0, y1 - y0
        nx, ny = -dy / d * 0.13, dx / d * 0.13
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        line(ax, [(x0, y0), (x1, y1)], lw=1.0, c=GR)
        for k, s in enumerate((1, -1)):
            ex, ey = mx + s * nx, my + s * ny
            if manque == k:
                ax.add_patch(Circle((ex, ey), 0.15, fc="white", ec=RED, lw=2.0, zorder=5))
                ax.text(ex, ey, "+", ha="center", va="center", fontsize=10, color=RED, fontweight="bold", zorder=6)
                yield (ex, ey)
            else:
                ax.add_patch(Circle((ex, ey), 0.11, fc=BLUE, ec=BLUE, zorder=5))

    trou = None
    for (x, y) in pos:
        for (dx, dy) in ((d, 0), (0, d)):
            if (x + dx, y + dy) in pos:
                rompue = mode in ("paire", "p") and (x, y) == (d, d) and (dx, dy) == (d, 0)
                for t in paire(x, y, x + dx, y + dy, 1 if rompue else None):
                    trou = t
        for (dx, dy) in ((d, 0), (-d, 0), (0, d), (0, -d)):            # liaisons vers l'extérieur du morceau dessiné
            if (x + dx, y + dy) not in pos:
                line(ax, [(x, y), (x + dx * 0.42, y + dy * 0.42)], lw=1.0, c=GR)
                ax.add_patch(Circle((x + dx * 0.3 - dy * 0.065, y + dy * 0.3 + dx * 0.065), 0.11, fc=BLUE, ec=BLUE, zorder=5))
                ax.add_patch(Circle((x + dx * 0.3 + dy * 0.065, y + dy * 0.3 - dx * 0.065), 0.11, fc=BLUE, ec=BLUE, zorder=5))
    for (x, y) in pos:
        sym = centre if (x, y) == (d, d) else "Si"
        fc = BLUE if sym != "Si" else NAVY
        ax.add_patch(Circle((x, y), 0.42, fc=fc, ec=fc, zorder=6))
        ax.text(x, y, sym, ha="center", va="center", fontsize=16 * (1.3 if grand else 1), color="white", fontweight="bold", zorder=7)
    if mode == "paire":
        ex, ey = 2.9, 2.85
        ax.add_patch(Circle((ex, ey), 0.15, fc=BLUE, ec=NAVY, lw=1.5, zorder=8))
        ax.text(ex, ey, "−", ha="center", va="center", fontsize=10, color="white", fontweight="bold", zorder=9)
        ax.annotate("", xy=(ex, ey - 0.17), xytext=(3.0, 2.12), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.4, ls="--"), zorder=8)
        ax.text(2.3, 3.3, "électron libre", fontsize=14, color=NAVY, fontweight="bold", ha="left")
        ax.text(3.0, 1.45, "trou", fontsize=14 * k, color=RED, fontweight="bold", ha="center", va="center")
        ax.text(2.2, -0.95, "chaleur → une liaison se rompt :\nune paire électron-trou", ha="center", va="top", fontsize=14, color=K)
    if mode == "n":
        ex, ey = 1.45, 2.6
        ax.add_patch(Circle((ex, ey), 0.15, fc=BLUE, ec=NAVY, lw=1.5, zorder=8))
        ax.text(ex, ey, "−", ha="center", va="center", fontsize=10, color="white", fontweight="bold", zorder=9)
        ax.text(0.3 if grand else 0.35, 3.25, "libre" if grand else "5e électron\nlibre", fontsize=12.5 * k, color=NAVY, fontweight="bold", ha="left", va="center")
        if not grand:
            ax.text(2.0, -0.95, "phosphore (5 électrons de valence) :\nun électron en trop → libre", ha="center", va="top", fontsize=14, color=K)
    if mode == "p":
        ax.text(3.0, 1.45, "trou", fontsize=14 * k, color=RED, fontweight="bold", ha="center", va="center")
        if not grand:
            ax.text(2.0, -0.95, "bore (3 électrons de valence) :\nune liaison incomplète → un trou", ha="center", va="top", fontsize=14, color=K)
    if mode is None:
        ax.text(2.0, -0.95, "chaque atome partage ses 4 électrons\nde valence avec 4 voisins", ha="center", va="top", fontsize=14, color=K)
    ax.set_xlim(-1.0, 5.4); ax.set_ylim(-0.9 if grand else -1.9, 5.0)
    save(fig, nom)


# ---------------------------------------------------------------- 5. dérive dans un champ électrique
def champ(nom="fig_champ.png"):
    fig, ax = plt.subplots(figsize=(7.6, 3.4)); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(Rectangle((0, 0), 6, 2.2, fc=TINT, ec=NAVY, lw=1.6))
    ax.add_patch(Rectangle((-0.35, -0.2), 0.35, 2.6, fc=GR, ec=GR)); ax.add_patch(Rectangle((6, -0.2), 0.35, 2.6, fc=GR, ec=GR))
    ax.text(-0.18, 2.75, "+", ha="center", fontsize=20, color=RED, fontweight="bold")
    ax.text(6.18, 2.75, "−", ha="center", fontsize=20, color=NAVY, fontweight="bold")
    for k, (x, y) in enumerate([(1.2, 1.6), (3.0, 1.75), (4.6, 1.55), (2.2, 1.45)]):
        ax.add_patch(Circle((x, y), 0.16, fc=BLUE, ec=NAVY, zorder=4)); ax.text(x, y, "−", ha="center", va="center", fontsize=10, color="white", fontweight="bold", zorder=5)
        ax.annotate("", xy=(x - 0.75, y), xytext=(x - 0.2, y), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6))
    for (x, y) in [(1.6, 0.6), (3.4, 0.5), (4.9, 0.7), (2.6, 0.75)]:
        ax.add_patch(Circle((x, y), 0.16, fc="white", ec=RED, lw=1.8, zorder=4)); ax.text(x, y, "+", ha="center", va="center", fontsize=10, color=RED, fontweight="bold", zorder=5)
        ax.annotate("", xy=(x + 0.75, y), xytext=(x + 0.2, y), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
    ax.text(6.6, 1.65, "électrons :\nvers le +", fontsize=11, color=BLUE, va="center", fontweight="bold")
    ax.text(6.6, 0.6, "trous :\nvers le −", fontsize=11, color=RED, va="center", fontweight="bold")
    ax.annotate("", xy=(5.0, -0.75), xytext=(1.0, -0.75), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2.0))
    ax.text(3.0, -1.05, "champ électrique E (du + vers le −) et sens conventionnel du courant I", ha="center", va="top", fontsize=10.5, color=NAVY)
    ax.set_xlim(-0.8, 8.4); ax.set_ylim(-1.6, 3.2)
    save(fig, nom)


# ---------------------------------------------------------------- 6. effet de la température
def temperature(nom="fig_temperature.png"):
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    th = [t / 2 for t in range(0, 201)]
    ax.semilogy(th, [1 + ALPHA_CU * (t - 20) for t in th], color=NAVY, lw=2.6, label="cuivre (métal) : R augmente")
    ax.semilogy(th, [r_si_relatif(t) for t in th], color=BLUE, lw=2.6, label="silicium pur : R diminue fortement")
    ax.axvline(20, color=GR, lw=0.8, ls=":"); ax.axhline(1, color=GR, lw=0.8, ls=":")
    ax.set_xlabel("Température θ [°C]", fontsize=13, color=NAVY)
    ax.set_ylabel("R / R₂₀ [–] (échelle log)", fontsize=13, color=NAVY)
    ax.set_xlim(0, 100); ax.set_ylim(0.004, 6)
    ax.set_yticks([0.005, 0.01, 0.1, 1, 5]); ax.set_yticklabels(["0,005", "0,01", "0,1", "1", "5"])
    ax.minorticks_off()
    ax.legend(loc="upper right", fontsize=12, frameon=False)
    ax.grid(True, which="major", color="#DDDDDD", lw=0.6)
    for sp in ("right", "top"):
        ax.spines[sp].set_visible(False)
    ax.text(2, 0.005, "allure", ha="left", va="bottom", fontsize=11, color=GR, style="italic")
    save(fig, nom)


def produire(ctx):
    import moteur.cei as cei
    cei.ecrire_dans(ctx.images)
    echelle_rho(); valence(); champ(); temperature()
    cristal("fig_paire.png", mode="paire")
    cristal("fig_dopage_n.png", centre="P", mode="n", grand=True)
    cristal("fig_dopage_p.png", centre="B", mode="p", grand=True)
