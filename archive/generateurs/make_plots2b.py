# -*- coding: utf-8 -*-
"""Chapitre 220 — du tableau de mesures au graphique."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

NAVY, BLUE, RED, GREY, LBLUE = "#242852", "#297FD5", "#EE0000", "#7F8FA9", "#ACCBF9"
rcParams["font.family"] = ["Carlito", "DejaVu Sans"]
for k in ("axes.edgecolor", "text.color", "axes.labelcolor", "xtick.color", "ytick.color"):
    rcParams[k] = NAVY

I = [0, 0.5, 1.0, 1.5, 2.0]
U = [12, 10, 8, 6, 4]

fig, ax = plt.subplots(figsize=(6.9, 4.3), dpi=200)
ax.set_xlim(0, 3.5)
ax.set_ylim(0, 13)
ax.set_xticks([i * 0.5 for i in range(8)])
ax.set_yticks(list(range(14)))
ax.set_xticks([i * 0.1 for i in range(36)], minor=True)
ax.set_yticks([i * 0.2 for i in range(66)], minor=True)
ax.grid(which="minor", color=LBLUE, lw=0.5, alpha=0.7)
ax.grid(which="major", color=GREY, lw=0.8, alpha=0.6)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(1.8)
ax.spines["bottom"].set_linewidth(1.8)
ax.set_xlabel("I [A]", fontsize=13, fontweight="bold", loc="right")
ax.set_ylabel("U [V]", fontsize=13, fontweight="bold", loc="top")

ax.plot([0, 3], [12, 0], "-", color=NAVY, lw=2.4, zorder=2)
ax.plot(I, U, "o", color=RED, ms=11, zorder=4)
ax.text(1.15, 10.6, "les points mesurés sont alignés :", fontsize=12.5,
        color=RED, fontweight="bold")
ax.text(1.15, 9.6, "la caractéristique d’une source", fontsize=12.5,
        color=NAVY, fontweight="bold")
ax.text(1.15, 8.6, "est une DROITE", fontsize=12.5, color=NAVY, fontweight="bold")
fig.tight_layout()
fig.savefig("18_nuage.png", facecolor="white")
print("ok 18_nuage")
