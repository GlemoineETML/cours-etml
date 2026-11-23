# -*- coding: utf-8 -*-
"""Symboles et figures normalisés (CEI 60617), en PNG via matplotlib, aux couleurs ETML (REGLES 3.3) :
portes logiques (CEI 60617-12 : rectangle + qualificatif, cercle de négation), équations en notation du Floyd,
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
