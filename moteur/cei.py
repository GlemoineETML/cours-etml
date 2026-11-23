# -*- coding: utf-8 -*-
"""Symboles et figures normalisés (CEI 60617), en PNG via matplotlib, aux couleurs ETML (REGLES 3.3) :
portes logiques (CEI 60617-12 : rectangle + qualificatif, cercle de négation), équations en notation du Floyd,
résistance, source de tension, masse, nœuds, flèches de tension et de courant (CEI 60617-2 et -4),
chronogrammes, contact à fermeture (CEI 60617-7), brochage DIP 14.
Les figures propres à une séance sont dans contenus/<matière>/<semaine>/figures.py et utilisent ces briques.
ecrire_dans(dossier) fixe le dossier où save() écrit les images."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
from moteur import logique as L

plt.rcParams["font.family"] = "Liberation Sans"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Liberation Sans"
plt.rcParams["mathtext.it"] = "Liberation Sans:italic"
plt.rcParams["mathtext.bf"] = "Liberation Sans:bold"
K, NAVY, BLUE, LBLUE, TINT, RED, GR = "black", "#242852", "#297FD5", "#ACCBF9", "#E8EFFB", "#EE0000", "#5A6478"
DPI = 220
_DOSSIER = "."


def ecrire_dans(dossier):
    global _DOSSIER
    os.makedirs(dossier, exist_ok=True)
    _DOSSIER = dossier


def save(fig, name, pad=0.05):
    fig.savefig(os.path.join(_DOSSIER, name), dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=pad)
    plt.close(fig)


def line(ax, pts, lw=1.8, c=K, **kw):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round", **kw)


# ------------------------------------------------------------------ symbole CEI d'une porte
def gate_ax(ax, x, y, key, w=1.3, h=1.6, lw=2.0, fs=20, labels=("A", "B", "Y"), lab_fs=17, pin=0.55):
    g = L.GATES[key]
    qual, neg, n = g[2], g[3], g[4]
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=K, lw=lw))
    ax.text(x + w / 2, y + h - 0.32, qual, ha="center", va="center", fontsize=fs, color=K)
    ys = [y + h / 2] if n == 1 else [y + h * 0.72, y + h * 0.28]
    for i, yy in enumerate(ys):
        line(ax, [(x - pin, yy), (x, yy)], lw=lw)
        if labels:
            ax.text(x - pin - 0.08, yy, labels[i], ha="right", va="center", fontsize=lab_fs, style="italic")
    yo = y + h / 2; xo = x + w
    if neg:
        r = 0.12
        ax.add_patch(Circle((xo + r, yo), r, fill=False, ec=K, lw=lw)); xo += 2 * r
    line(ax, [(xo, yo), (xo + pin, yo)], lw=lw)
    if labels:
        ax.text(xo + pin + 0.08, yo, labels[-1], ha="left", va="center", fontsize=lab_fs, style="italic")


def fig_gate(key, name=None):
    fig, ax = plt.subplots(figsize=(3.2, 2.2)); ax.axis("off"); ax.set_aspect("equal")
    gate_ax(ax, 0.9, 0.2, key)
    ax.set_xlim(-0.05, 3.5); ax.set_ylim(0, 2.0)
    save(fig, name or f"gate_{key}.png")


# ------------------------------------------------------------------ équations (notation Floyd)
def fig_eq(key, color=NAVY, name=None, fs=30):
    fig = plt.figure(figsize=(4, 0.9)); fig.text(0.5, 0.5, "$" + L.GATES[key][6] + "$", ha="center", va="center", fontsize=fs, color=color)
    save(fig, name or f"eq_{key}.png", pad=0.08)


def fig_eq_txt(tex, name, color=NAVY, fs=30):
    fig = plt.figure(figsize=(4, 0.9)); fig.text(0.5, 0.5, "$" + tex + "$", ha="center", va="center", fontsize=fs, color=color)
    save(fig, name, pad=0.08)


# ------------------------------------------------------------------ chronogrammes
def chrono_fig(rows, name, n=8, ycol=BLUE, blank_last=False, highlight=None, width=7.6, numbers=True, last_label=None):
    """rows = [(nom, [bits] ou None)] ; la dernière ligne peut être vide (à compléter)."""
    h = 0.95 * len(rows) + (0.45 if numbers else 0.1)
    fig, ax = plt.subplots(figsize=(width, h)); ax.axis("off")
    top = len(rows) * 1.0
    if highlight is not None:
        ax.add_patch(Rectangle((highlight, -0.25), 1, top + 0.15, fc=LBLUE, ec="none", alpha=0.55))
    for k in range(n + 1):
        ax.plot([k, k], [-0.25, top - 0.1], color="#b9c3d6", lw=0.9, ls=(0, (2, 3)))
    if numbers:
        for k in range(n):
            ax.text(k + 0.5, top + 0.02, str(k + 1), ha="center", va="bottom", fontsize=10.5, color=GR)
    for i, (lab, bits) in enumerate(rows):
        y0 = top - 1.0 - i * 1.0 + 0.1
        ax.text(-0.25, y0 + 0.3, lab, ha="right", va="center", fontsize=15, style="italic", color=NAVY)
        ax.text(-0.08, y0 + 0.62, "1", ha="right", va="center", fontsize=8, color=GR)
        ax.text(-0.08, y0 + 0.0, "0", ha="right", va="center", fontsize=8, color=GR)
        last = i == len(rows) - 1
        if bits is None:
            for lev in (0, 0.62):
                ax.plot([0, n], [y0 + lev, y0 + lev], color="#c8cfdb", lw=0.9, ls=(0, (1, 2)))
            continue
        col = ycol if (last and len(rows) > 1) else NAVY
        xs, ys = [], []
        for k, bt in enumerate(bits):
            xs += [k, k + 1]; ys += [y0 + 0.62 * bt] * 2
        ax.plot(xs, ys, color=col, lw=2.6, solid_joinstyle="miter")
    ax.set_xlim(-0.7, n + 0.05); ax.set_ylim(-0.35, top + (0.45 if numbers else 0.05))
    save(fig, name)



# ------------------------------------------------------------------ contact à fermeture (CEI 60617-7)
def switch(ax, x, y_top, y_bot, closed, lw=2.2):
    """Interrupteur vertical (contact à fermeture, CEI 60617-7) entre y_top et y_bot."""
    yl = y_bot + (y_top - y_bot) * 0.3; yh = y_bot + (y_top - y_bot) * 0.7
    line(ax, [(x, y_top), (x, yh)], lw=lw); line(ax, [(x, y_bot), (x, yl)], lw=lw)
    if closed:
        line(ax, [(x, yl), (x + 0.04, yh)], lw=lw)
    else:
        line(ax, [(x, yl), (x + 0.32, yh - 0.05)], lw=lw)



# ------------------------------------------------------------------ brochage DIP 14 (vue de dessus, brochages dans moteur/logique.py)
def fig_dip(ref):
    p = L.PINS[ref]
    fig, ax = plt.subplots(figsize=(3.6, 3.8)); ax.axis("off"); ax.set_aspect("equal")
    W, Hh = 1.6, 3.5
    ax.add_patch(Rectangle((0, 0), W, Hh, fc=TINT, ec=K, lw=1.8))
    ax.add_patch(matplotlib.patches.Arc((W / 2, Hh), 0.5, 0.5, theta1=180, theta2=360, lw=1.8))
    ax.add_patch(Circle((0.55, Hh - 0.25), 0.07, color=K))
    ax.text(W / 2, Hh / 2, ref, ha="center", va="center", rotation=90, fontsize=14, fontweight="bold", color=NAVY)
    for i in range(7):
        y = Hh - 0.35 - i * 0.47
        # côté gauche : broches 1 à 7 ; côté droit : 14 à 8
        ax.add_patch(Rectangle((-0.3, y - 0.09), 0.3, 0.18, fc="white", ec=K, lw=1.2))
        ax.add_patch(Rectangle((W, y - 0.09), 0.3, 0.18, fc="white", ec=K, lw=1.2))
        ax.text(0.08, y, str(i + 1), ha="left", va="center", fontsize=9, color=GR)
        ax.text(W - 0.08, y, str(14 - i), ha="right", va="center", fontsize=9, color=GR)
        lab_l, lab_r = p[i], p[13 - i]
        ax.text(-0.38, y, lab_l.replace("VCC", "V$_{CC}$"), ha="right", va="center", fontsize=11, fontweight="bold", color=NAVY)
        ax.text(W + 0.38, y, lab_r.replace("VCC", "V$_{CC}$"), ha="left", va="center", fontsize=11, fontweight="bold", color=NAVY)
    ax.set_xlim(-1.2, W + 1.2); ax.set_ylim(-0.2, Hh + 0.35)
    save(fig, f"dip_{ref}.png")


# ------------------------------------------------------------------ circuits (CEI 60617-2 et -4) : résistance, source, masse, flèches
# Convention (REGLES 3.3) : la flèche de tension pointe vers le potentiel le plus élevé ; récepteur : courant et tension
# en sens contraires ; source : même sens (convention générateur).
def resistance(ax, x, y0, y1, nom=None, valeur=None, lw=2.0, w=0.32, h=0.85, cote="droite", fs=15):
    """Résistance verticale (rectangle CEI) entre y0 et y1, avec son nom (R_1) et sa valeur (4k7) à côté."""
    ym = (y0 + y1) / 2
    line(ax, [(x, y0), (x, ym - h / 2)], lw=lw); line(ax, [(x, ym + h / 2), (x, y1)], lw=lw)
    ax.add_patch(Rectangle((x - w / 2, ym - h / 2), w, h, fill=True, fc="white", ec=K, lw=lw, zorder=3))
    s = 1 if cote == "droite" else -1
    ha = "left" if s > 0 else "right"
    if nom:
        ax.text(x + s * (w / 2 + 0.15), ym + 0.17, nom, ha=ha, va="center", fontsize=fs, color=NAVY)
    if valeur:
        ax.text(x + s * (w / 2 + 0.15), ym - 0.22, valeur, ha=ha, va="center", fontsize=fs - 2, color=GR)


def source_tension(ax, x, y0, y1, r=0.34, lw=2.0):
    """Source de tension idéale (CEI 60617-2) : cercle traversé par le conducteur, entre y0 (−) et y1 (+)."""
    ym = (y0 + y1) / 2
    line(ax, [(x, y0), (x, ym - r)], lw=lw); line(ax, [(x, ym + r), (x, y1)], lw=lw)
    ax.add_patch(Circle((x, ym), r, fill=True, fc="white", ec=K, lw=lw, zorder=3))
    line(ax, [(x, ym - r), (x, ym + r)], lw=lw, zorder=4)        # le conducteur traverse le cercle


def masse(ax, x, y, lw=2.2):
    """Masse : trait horizontal et traits décroissants."""
    for k_, w_ in enumerate((0.3, 0.2, 0.1)):
        line(ax, [(x - w_, y - 0.1 * k_), (x + w_, y - 0.1 * k_)], lw=lw)


def noeud(ax, x, y, r=0.06):
    ax.add_patch(Circle((x, y), r, color=K, zorder=4))


def borne(ax, x, y, r=0.07, lw=1.8):
    ax.add_patch(Circle((x, y), r, fill=True, fc="white", ec=K, lw=lw, zorder=4))


def fleche_tension(ax, x, y_moins, y_plus, nom, couleur=BLUE, fs=15, cote="droite"):
    """Flèche de tension verticale, pointe vers le potentiel le plus élevé (y_plus)."""
    ax.annotate("", xy=(x, y_plus), xytext=(x, y_moins),
                arrowprops=dict(arrowstyle="-|>,head_length=0.6,head_width=0.3", color=couleur, lw=2.0))
    ax.text(x + (0.12 if cote == "droite" else -0.12), (y_moins + y_plus) / 2, nom, ha="left" if cote == "droite" else "right",
            va="center", fontsize=fs, color=couleur, fontweight="bold")


def fleche_courant(ax, x0, y0, x1, y1, nom, couleur=RED, fs=14, decal=(0.12, 0.0)):
    """Pointe de flèche de courant posée sur un conducteur, de (x0, y0) vers (x1, y1)."""
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>,head_length=0.7,head_width=0.32", color=couleur, lw=2.0))
    ax.text((x0 + x1) / 2 + decal[0], (y0 + y1) / 2 + decal[1], nom, ha="left", va="center", fontsize=fs, color=couleur, fontweight="bold")
