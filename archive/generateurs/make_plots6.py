# -*- coding: utf-8 -*-
"""Test 320 — courbes : lecture de C_x et grilles de tracé du régime transitoire."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

rcParams["font.family"] = ["Carlito", "DejaVu Sans"]
rcParams["mathtext.fontset"] = "dejavusans"
NAVY, BLUE, RED, GREY = "#242852", "#297FD5", "#EE0000", "#7F8FA9"


def cadre(ax, xl, yl, xmax, ymax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(NAVY)
        ax.spines[sp].set_linewidth(1.6)
    ax.tick_params(colors=NAVY, labelsize=11)
    ax.set_xlabel(xl, color=NAVY, fontsize=12, loc="right")
    ax.set_ylabel(yl, color=NAVY, fontsize=12, loc="top", rotation=0, labelpad=-10)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.grid(True, color="#E4E9F2", linewidth=0.8)
    ax.set_axisbelow(True)


def save(fig, nom):
    fig.savefig(nom + ".png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("ok", nom)


# ============================================= T4 : courbe lue (question 4)
U, R = 24.0, 1.2e3
I0 = U / R * 1e3                 # 20 mA
tl, il = 28.0, 10.0              # point relevé : 28 µs ; 10 mA
tau = tl / np.log(I0 / il)       # 40,4 µs
t = np.linspace(0, 5 * tau, 600)
for nom, corrige in (("T4_courbe", False), ("T4c_courbe", True)):
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    cadre(ax, "t [µs]", "$i_C$ [mA]", 5 * tau, I0 * 1.14)
    ax.plot(t, I0 * np.exp(-t / tau), color=RED, lw=2.8)
    ax.plot([0, tl], [il, il], color=NAVY, ls=":", lw=1.6)
    ax.plot([tl, tl], [0, il], color=NAVY, ls=":", lw=1.6)
    ax.plot([tl], [il], "o", color=NAVY, ms=7)
    ax.set_xticks([0, 28, 50, 100, 150, 200])
    ax.set_yticks([0, 5, 10, 15, 20])
    if corrige:
        ax.annotate("i = I₀ / 2  →  t = τ · ln 2", (tl, il), (tl + 22, il + 5.2),
                    color=NAVY, fontsize=11.5,
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.3))
        ax.plot([tau], [I0 * np.exp(-1)], "o", color=RED, ms=6)
        ax.text(tau + 6, I0 * np.exp(-1) + 1.0, "τ = 40,4 µs", color=RED, fontsize=11)
    fig.tight_layout()
    save(fig, nom)

# ============================================= T5 : grilles de tracé (question 5)
E, R1, R2, C = 30.0, 50.0, 100.0, 2e-6
UC = E * R2 / (R1 + R2)          # 20 V
tau = R2 * C                     # 200 µs
IC = UC / R2                     # 0,2 A


def grilles(nom, corrige):
    t = np.linspace(0, 5 * tau, 600)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.4))
    for ax in (a1, a2):
        ax.set_xlim(0, 5 * tau * 1e6)
        ax.set_ylim(0, 1.15)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(NAVY)
            ax.spines[sp].set_linewidth(1.6)
        ax.grid(True, color="#DCE3EE", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_xticks(np.arange(0, 1001, 100))
        ax.set_yticks(np.arange(0, 1.01, 0.1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(colors=NAVY, length=4)
    if corrige:
        a1.plot(t * 1e6, np.exp(-t / tau), color=BLUE, lw=2.6)
        a1.set_yticklabels(["%g" % v for v in np.arange(0, 20.1, 2)], fontsize=9.5)
        a1.set_xticklabels(["%d" % v for v in np.arange(0, 1001, 100)], fontsize=9.5)
        a1.set_xlabel("t [µs]", color=NAVY, fontsize=11, loc="right")
        a1.set_ylabel("$u_C$ [V]", color=NAVY, fontsize=11, loc="top", rotation=0,
                      labelpad=-8)
        a1.plot([tau * 1e6], [np.exp(-1)], "o", color=RED, ms=6)
        a1.text(tau * 1e6 + 14, np.exp(-1) + 0.03, "τ = 200 µs  →  7,36 V",
                color=RED, fontsize=10.5)
        a1.text(8, 1.04, "$U_C$ max = 20 V", color=GREY, fontsize=10.5)
        a2.plot(t * 1e6, np.exp(-t / tau), color=RED, lw=2.6)
        a2.set_yticklabels(["%g" % v for v in np.arange(0, 201, 20)], fontsize=9.5)
        a2.set_xticklabels(["%d" % v for v in np.arange(0, 1001, 100)], fontsize=9.5)
        a2.set_xlabel("t [µs]", color=NAVY, fontsize=11, loc="right")
        a2.set_ylabel("$i_C$ [mA]", color=NAVY, fontsize=11, loc="top", rotation=0,
                      labelpad=-8)
        a2.plot([tau * 1e6], [np.exp(-1)], "o", color=RED, ms=6)
        a2.text(tau * 1e6 + 14, np.exp(-1) + 0.03, "τ = 200 µs  →  73,6 mA",
                color=RED, fontsize=10.5)
        a2.text(8, 1.04, "$I_C$ max = 200 mA", color=GREY, fontsize=10.5)
    fig.tight_layout()
    save(fig, nom)


grilles("T5_grilles", False)
grilles("T5c_grilles", True)
print("courbes test 320 : ok")
