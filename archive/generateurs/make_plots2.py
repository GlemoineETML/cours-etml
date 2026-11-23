# -*- coding: utf-8 -*-
"""Chapitre 220 — graphiques cours + quadrillages d'exercice."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

NAVY, BLUE, RED, GREY, LBLUE = "#242852", "#297FD5", "#EE0000", "#7F8FA9", "#ACCBF9"
GREEN = "#2C7A4B"
rcParams["font.family"] = ["Carlito", "DejaVu Sans"]
for k in ("axes.edgecolor", "text.color", "axes.labelcolor", "xtick.color", "ytick.color"):
    rcParams[k] = NAVY


def frame(ax, xmax, ymax, xstep, ystep):
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    n = int(round(xmax / xstep))
    m = int(round(ymax / ystep))
    ax.set_xticks([i * xstep for i in range(n + 1)])
    ax.set_yticks([i * ystep for i in range(m + 1)])
    ax.set_xticks([i * xstep / 5 for i in range(n * 5 + 1)], minor=True)
    ax.set_yticks([i * ystep / 5 for i in range(m * 5 + 1)], minor=True)
    ax.grid(which="minor", color=LBLUE, lw=0.5, alpha=0.7)
    ax.grid(which="major", color=GREY, lw=0.8, alpha=0.6)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.8)
    ax.spines["bottom"].set_linewidth(1.8)
    ax.set_xlabel("I [A]", fontsize=13, fontweight="bold", loc="right")
    ax.set_ylabel("U [V]", fontsize=13, fontweight="bold", loc="top")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(name + ".png", facecolor="white")
    plt.close(fig)
    print("ok", name)


# source du cours
U0, RI = 12.0, 4.0
ICC = U0 / RI          # 3 A

# ------------------------------------------------- 13 : deux points suffisent
fig, ax = plt.subplots(figsize=(6.9, 4.3), dpi=200)
frame(ax, 3.5, 13, 0.5, 1)
ax.plot([0, ICC], [U0, 0], "-", color=NAVY, lw=2.8, zorder=3)
ax.plot([0], [U0], "o", color=BLUE, ms=11, zorder=4)
ax.plot([ICC], [0], "o", color=RED, ms=11, zorder=4)
ax.annotate("marche à vide\n(0 A ; 12 V)", xy=(0, U0), xytext=(0.28, 11.0),
            fontsize=12, color=BLUE, fontweight="bold")
ax.annotate("court-circuit\n(3 A ; 0 V)", xy=(2.95, 0.12), xytext=(0.9, 1.2),
            fontsize=12, color=RED, fontweight="bold", ha="left",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
ax.text(1.42, 7.6, "ces deux points\nsuffisent à tracer\ntoute la droite",
        fontsize=12.5, color=NAVY, fontweight="bold", ha="left")
save(fig, "13_deux_points")

# ------------------------------------------------- 14 : point de fonctionnement
fig, ax = plt.subplots(figsize=(6.9, 4.3), dpi=200)
frame(ax, 3.5, 13, 0.5, 1)
ax.plot([0, ICC], [U0, 0], "-", color=NAVY, lw=2.8, label="source (12 V ; 4 Ω)")
ax.plot([0, 1.5], [0, 12], "-", color=GREEN, lw=2.8, label="charge R = 8 Ω")
ax.plot([1], [8], "o", color=RED, ms=11, zorder=5)
ax.plot([0, 1], [8, 8], ":", color=RED, lw=1.7)
ax.plot([1, 1], [0, 8], ":", color=RED, lw=1.7)
ax.annotate("point de fonctionnement\n(1 A ; 8 V)", xy=(1, 8), xytext=(1.45, 9.7),
            fontsize=12, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
ax.legend(loc="upper right", fontsize=11, frameon=False)
save(fig, "14_point_fonctionnement")

# ------------------------------------------------- 15 : charge non linéaire (lampe)
fig, ax = plt.subplots(figsize=(6.9, 4.3), dpi=200)
frame(ax, 3.5, 13, 0.5, 1)
k = 7.2 / 1.2 ** 1.6
i = np.linspace(0, 1.75, 300)
ax.plot([0, ICC], [U0, 0], "-", color=NAVY, lw=2.8, label="source (12 V ; 4 Ω)")
ax.plot(i, k * i ** 1.6, "-", color=GREEN, lw=2.8, label="lampe à incandescence")
ax.plot([1.2], [7.2], "o", color=RED, ms=11, zorder=5)
ax.plot([0, 1.2], [7.2, 7.2], ":", color=RED, lw=1.7)
ax.plot([1.2, 1.2], [0, 7.2], ":", color=RED, lw=1.7)
ax.annotate("(1,2 A ; 7,2 V)", xy=(1.2, 7.2), xytext=(1.5, 8.6),
            fontsize=12, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
ax.text(1.95, 4.2, "la caractéristique de la lampe\nest courbe : sa résistance\naugmente avec la température",
        fontsize=11, color=GREEN, fontweight="bold", ha="left")
ax.legend(loc="upper right", fontsize=11, frameon=False)
save(fig, "15_lampe")

# ------------------------------------------------- 16 : puissance = aire
fig, ax = plt.subplots(figsize=(6.9, 4.3), dpi=200)
frame(ax, 3.5, 13, 0.5, 1)
ax.plot([0, ICC], [U0, 0], "-", color=NAVY, lw=2.8, zorder=4)
pts = [(1.0, 8.0, "R = 8 Ω\nP = 8 W", GREY), (1.5, 6.0, "R = 4 Ω\nP = 9 W", RED),
       (2.0, 4.0, "R = 2 Ω\nP = 8 W", GREY)]
for x, y, lab, col in pts:
    ax.add_patch(plt.Rectangle((0, 0), x, y, facecolor=col,
                               alpha=0.30 if col == RED else 0.13, edgecolor=col,
                               lw=1.6, zorder=2))
    ax.plot([x], [y], "o", color=col, ms=9, zorder=5)
ax.text(0.28, 8.6, "R = 8 Ω → P = 8 W", fontsize=11.5, color=NAVY, fontweight="bold")
ax.text(1.62, 6.35, "R = Rᵢ = 4 Ω → P = 9 W", fontsize=11.5, color=RED, fontweight="bold")
ax.text(2.08, 4.25, "R = 2 Ω → P = 8 W", fontsize=11.5, color=NAVY, fontweight="bold")
ax.text(1.75, 11.2, "P = U · I = aire du rectangle", fontsize=13, color=NAVY,
        fontweight="bold", ha="center")
save(fig, "16_puissance")

# ------------------------------------------------- quadrillages d'exercice
# 17a : source 10 V / 2,5 Ω → Icc = 4 A
for name, drawn in (("17a_vide", False), ("17a_corrige", True)):
    fig, ax = plt.subplots(figsize=(6.4, 4.3), dpi=200)
    frame(ax, 5, 11, 0.5, 1)
    if drawn:
        ax.plot([0, 4], [10, 0], "-", color=RED, lw=2.8)
        ax.plot([0, 4], [10, 0], "o", color=RED, ms=8, ls="none")
        ax.plot([2], [5], "o", color=RED, ms=9)
        ax.plot([0, 2], [5, 5], ":", color=RED, lw=1.7)
        ax.plot([2, 2], [0, 5], ":", color=RED, lw=1.7)
        ax.annotate("U₀ = 10 V", xy=(0, 10), xytext=(0.2, 10.3), fontsize=12,
                    color=RED, fontweight="bold")
        ax.annotate("I$_{cc}$ = 4 A", xy=(4.02, 0.06), xytext=(4.5, 1.2), fontsize=12,
                    color=RED, fontweight="bold", ha="center",
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
        ax.annotate("U = 5 V à I = 2 A", xy=(2, 5), xytext=(2.15, 5.6),
                    fontsize=11.5, color=RED, fontweight="bold")
    save(fig, name)

# 17b : même source, droite déjà tracée ; l'élève ajoute la charge R = 7,5 Ω
for name, drawn in (("17b_vide", False), ("17b_corrige", True)):
    fig, ax = plt.subplots(figsize=(6.4, 4.3), dpi=200)
    frame(ax, 5, 11, 0.5, 1)
    ax.plot([0, 4], [10, 0], "-", color=NAVY, lw=2.6)
    ax.text(2.55, 4.4, "source", fontsize=11.5, color=NAVY, fontweight="bold",
            rotation=-30)
    if drawn:
        ax.plot([0, 1.4], [0, 10.5], "-", color=RED, lw=2.8)
        ax.plot([1], [7.5], "o", color=RED, ms=10, zorder=5)
        ax.plot([0, 1], [7.5, 7.5], ":", color=RED, lw=1.7)
        ax.plot([1, 1], [0, 7.5], ":", color=RED, lw=1.7)
        ax.annotate("charge 7,5 Ω", xy=(1.2, 9), xytext=(1.45, 9.6),
                    fontsize=11.5, color=RED, fontweight="bold")
        ax.annotate("(1 A ; 7,5 V)", xy=(1, 7.5), xytext=(1.6, 7.3),
                    fontsize=12, color=RED, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    save(fig, name)

# 17c : lampe 6 V sur source 9 V / 3 Ω → point (1,0 A ; 6,0 V)
ILAMP = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
ULAMP = [0.5, 1.4, 2.7, 4.2, 6.0, 8.0]
for name, drawn in (("17c_vide", False), ("17c_corrige", True)):
    fig, ax = plt.subplots(figsize=(6.4, 4.3), dpi=200)
    frame(ax, 1.4, 10, 0.2, 1)
    if drawn:
        ax.plot([0, 1.4], [9, 9 - 3 * 1.4], "-", color=NAVY, lw=2.6)
        ax.text(0.42, 8.1, "source 9 V / 3 Ω", fontsize=11, color=NAVY,
                fontweight="bold", rotation=-24)
        ax.plot(ILAMP, ULAMP, "-o", color=RED, lw=2.6, ms=6)
        ax.plot([1.0], [6.0], "o", color=RED, ms=11, zorder=5)
        ax.plot([0, 1.0], [6, 6], ":", color=RED, lw=1.7)
        ax.plot([1.0, 1.0], [0, 6], ":", color=RED, lw=1.7)
        ax.annotate("lampe", xy=(1.2, 8.0), xytext=(1.02, 9.1),
                    fontsize=11.5, color=RED, fontweight="bold")
        ax.annotate("(1,0 A ; 6,0 V)", xy=(1.0, 6.0), xytext=(0.32, 4.3),
                    fontsize=12, color=RED, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    save(fig, name)
