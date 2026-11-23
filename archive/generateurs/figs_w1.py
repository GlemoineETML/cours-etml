# -*- coding: utf-8 -*-
"""Figures semaine 1 (TM1 – El DT 1) : symboles CEI 60617-12, équations, chronogrammes, sortie push-pull,
gabarit des niveaux et marges de bruit, ligne de remplissage, brochages DIP 14.
Toutes les valeurs viennent de w1_data.py."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w1_data as D

plt.rcParams["font.family"] = "Liberation Sans"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Liberation Sans"
plt.rcParams["mathtext.it"] = "Liberation Sans:italic"
plt.rcParams["mathtext.bf"] = "Liberation Sans:bold"
K, NAVY, BLUE, LBLUE, TINT, RED, GR = "black", "#242852", "#297FD5", "#ACCBF9", "#E8EFFB", "#EE0000", "#5A6478"
DPI = 220


def save(fig, name, pad=0.05):
    fig.savefig(name, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=pad)
    plt.close(fig)


def line(ax, pts, lw=1.8, c=K, **kw):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round", **kw)


# ------------------------------------------------------------------ symbole CEI d'une porte
def gate_ax(ax, x, y, key, w=1.3, h=1.6, lw=2.0, fs=20, labels=("A", "B", "Y"), lab_fs=17, pin=0.55):
    g = D.GATES[key]
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
    fig = plt.figure(figsize=(4, 0.9)); fig.text(0.5, 0.5, "$" + D.GATES[key][6] + "$", ha="center", va="center", fontsize=fs, color=color)
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


def fig_chronos():
    A, B = D.CHRONO_A, D.CHRONO_B
    for k in D.ORDER:
        Y = D.chrono(k)
        ins = [("A", A)] if D.GATES[k][4] == 1 else [("A", A), ("B", B)]
        chrono_fig(ins + [("Y", Y)], f"chrono_{k}.png")
        chrono_fig(ins + [("Y", Y)], f"chrono_{k}_corr.png", ycol=RED)
        chrono_fig(ins + [("Y", None)], f"chrono_{k}_q.png")


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


# ------------------------------------------------------------------ sortie push-pull (100, diapo 2)
def switch(ax, x, y_top, y_bot, closed, lw=2.2):
    """Interrupteur vertical (contact à fermeture, CEI 60617-7) entre y_top et y_bot."""
    yl = y_bot + (y_top - y_bot) * 0.3; yh = y_bot + (y_top - y_bot) * 0.7
    line(ax, [(x, y_top), (x, yh)], lw=lw); line(ax, [(x, y_bot), (x, yl)], lw=lw)
    if closed:
        line(ax, [(x, yl), (x + 0.04, yh)], lw=lw)
    else:
        line(ax, [(x, yl), (x + 0.32, yh - 0.05)], lw=lw)


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
        ax.text(x0 + 0.5, y, t, fontsize=10.5, va="center", color=K)
    ax.text(x0, 1.85, "Sorties (actionneurs)", fontsize=11.5, fontweight="bold", color=NAVY, va="center")
    for i, (l, t) in enumerate((("V", "vanne de remplissage"), ("M", "moteur du convoyeur"))):
        y = 1.4 - i * 0.42; sq(x0 + 0.17, y, l, NAVY, True)
        ax.text(x0 + 0.5, y, t, fontsize=10.5, va="center", color=K)
    ax.set_xlim(0.0, 10.4); ax.set_ylim(0.15, 4.55)
    save(fig, "fig_ligne.png")


# ------------------------------------------------------------------ brochage DIP 14 (vue de dessus)
PINS = {
    "74HC08": ["1A", "1B", "1Y", "2A", "2B", "2Y", "GND", "3Y", "3A", "3B", "4Y", "4A", "4B", "VCC"],
    "74HC04": ["1A", "1Y", "2A", "2Y", "3A", "3Y", "GND", "4Y", "4A", "5Y", "5A", "6Y", "6A", "VCC"],
}


def fig_dip(ref):
    p = PINS[ref]
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


if __name__ == "__main__":
    for k in D.ORDER:
        fig_gate(k); fig_eq(k); fig_eq(k, color=RED, name=f"eq_{k}_corr.png")
    fig_chronos(); fig_myst(); fig_n2(); fig_lecture()
    fig_pushpull(); fig_marges(); fig_ligne()
    for r in PINS: fig_dip(r)
    # équation du convoyeur (fiche 130, N°1)
    fig_eq_txt(r"M = E \cdot L \cdot \overline{U}", "eq_convoyeur.png")
    print("figures ok")
