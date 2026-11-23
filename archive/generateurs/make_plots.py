# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

NAVY, BLUE, RED, GREY, LBLUE = "#242852", "#297FD5", "#EE0000", "#7F8FA9", "#ACCBF9"
rcParams["font.family"] = ["Carlito", "DejaVu Sans"]
rcParams["axes.edgecolor"] = NAVY
rcParams["text.color"] = NAVY
rcParams["axes.labelcolor"] = NAVY
rcParams["xtick.color"] = NAVY
rcParams["ytick.color"] = NAVY


def frame(ax, xmax, ymax, xstep, ystep, xlab, ylab, minor=True):
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xticks([i * xstep for i in range(int(xmax / xstep) + 1)])
    ax.set_yticks([i * ystep for i in range(int(ymax / ystep) + 1)])
    if minor:
        ax.set_xticks([i * xstep / 5 for i in range(int(xmax / xstep) * 5 + 1)], minor=True)
        ax.set_yticks([i * ystep / 5 for i in range(int(ymax / ystep) * 5 + 1)], minor=True)
        ax.grid(which="minor", color=LBLUE, lw=0.5, alpha=0.7)
    ax.grid(which="major", color=GREY, lw=0.8, alpha=0.6)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.8)
    ax.spines["bottom"].set_linewidth(1.8)
    ax.set_xlabel(xlab, fontsize=13, fontweight="bold", loc="right")
    ax.set_ylabel(ylab, fontsize=13, fontweight="bold", loc="top")


# ------------------------------------------------- F4 caractéristique U(I)
fig, ax = plt.subplots(figsize=(7.0, 4.2), dpi=200)
frame(ax, 4.0, 7, 0.5, 1, "I [A]", "U [V]")
ax.plot([0, 4.0], [6, 6], "--", color=GREY, lw=2, label="source idéale (Rᵢ = 0)")
ax.plot([0, 3], [6, 0], "-", color=NAVY, lw=2.8, label="source réelle (U₀ = 6 V, Rᵢ = 2 Ω)")
ax.plot([0], [6], "o", color=NAVY, ms=8)
ax.plot([3], [0], "o", color=RED, ms=8)
ax.annotate("U₀ = 6 V\n(tension à vide)", xy=(0, 6), xytext=(0.22, 6.25),
            fontsize=12, color=NAVY, fontweight="bold")
ax.annotate("I$_{cc}$ = 3 A\n(court-circuit)", xy=(3.02, 0.06), xytext=(3.55, 1.15),
            fontsize=12, color=RED, fontweight="bold", ha="center",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
ax.plot([1.5], [3], "o", color=BLUE, ms=9)
ax.plot([0, 1.5], [3, 3], ":", color=BLUE, lw=1.6)
ax.plot([1.5, 1.5], [0, 3], ":", color=BLUE, lw=1.6)
ax.annotate("point de fonctionnement", xy=(1.5, 3), xytext=(1.66, 3.3),
            fontsize=11.5, color=BLUE, fontweight="bold")
ax.text(1.02, 4.42, "pente = −Rᵢ", fontsize=12.5, color=RED, fontweight="bold",
        rotation=-30, ha="center")
ax.legend(loc="lower left", fontsize=10.5, frameon=False, bbox_to_anchor=(0.02, 0.02))
fig.tight_layout()
fig.savefig("04_caracteristique.png", facecolor="white")
plt.close(fig)

# ------------------------------------------------- F5 source dure / molle
fig, ax = plt.subplots(figsize=(7.0, 3.3), dpi=200)
frame(ax, 10, 14, 2, 2, "I [A]", "U [V]")
ax.plot([0, 10], [12, 11.5], "-", color=NAVY, lw=3)
ax.plot([0, 10], [12, 7], "-", color=RED, lw=3)
ax.text(5.4, 12.45, "source dure  (Rᵢ = 0,05 Ω)", fontsize=12.5, color=NAVY,
        fontweight="bold", ha="center")
ax.text(4.5, 8.45, "source molle  (Rᵢ = 0,5 Ω)", fontsize=12.5, color=RED,
        fontweight="bold", ha="center")
ax.plot([0], [12], "o", color=NAVY, ms=8)
ax.text(0.2, 13.15, "même U₀ = 12 V", fontsize=12, color=NAVY, fontweight="bold")
fig.tight_layout()
fig.savefig("05_dure_molle.png", facecolor="white")
plt.close(fig)

# ------------------------------------------------- F8 grille exercice (vide + corrigé)
for name, drawn in (("08_grille_vide", False), ("08_grille_corrige", True)):
    fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=200)
    frame(ax, 4.0, 10, 0.5, 1, "I [A]", "U [V]")
    if drawn:
        ax.plot([0, 3], [9, 0], "-", color=RED, lw=2.8)
        ax.plot([0], [9], "o", color=RED, ms=8)
        ax.plot([3], [0], "o", color=RED, ms=8)
        ax.plot([2], [3], "o", color=RED, ms=9)
        ax.plot([0, 2], [3, 3], ":", color=RED, lw=1.6)
        ax.plot([2, 2], [0, 3], ":", color=RED, lw=1.6)
        ax.annotate("U₀ = 9 V", xy=(0, 9), xytext=(0.2, 9.25), fontsize=12,
                    color=RED, fontweight="bold")
        ax.annotate("I$_{cc}$ = 3 A", xy=(3.02, 0.06), xytext=(3.55, 1.2), fontsize=12,
                    color=RED, fontweight="bold", ha="center",
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
        ax.annotate("U = 3 V à I = 2 A", xy=(2, 3), xytext=(2.12, 3.5),
                    fontsize=11.5, color=RED, fontweight="bold")
    fig.tight_layout()
    fig.savefig(name + ".png", facecolor="white")
    plt.close(fig)
print("plots done")
