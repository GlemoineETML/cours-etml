# -*- coding: utf-8 -*-
"""Test 320 version B — courbes : lecture de C_x et grilles de tracé."""
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


# ===================================== B4 : courbe lue (question 4)
U, R = 9.0, 750.0
I0 = U / R * 1e3                  # 12,0 mA
tl, il = 35.0, 6.0                # point relevé : 35 µs ; 6,00 mA — la MOITIÉ de I0
tau = tl / np.log(I0 / il)        # 50,5 µs
t = np.linspace(0, 5 * tau, 600)
for nom, corrige in (("B4_courbe", False), ("B4c_courbe", True)):
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    cadre(ax, "t [µs]", "$i_C$ [mA]", 5 * tau, I0 * 1.18)
    ax.plot(t, I0 * np.exp(-t / tau), color=RED, lw=2.8)
    ax.plot([0, tl], [il, il], color=NAVY, ls=":", lw=1.6)
    ax.plot([tl, tl], [0, il], color=NAVY, ls=":", lw=1.6)
    ax.plot([tl], [il], "o", color=NAVY, ms=7)
    ax.set_xticks([0, 35, 100, 150, 200, 250])
    ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
    if corrige:
        ax.annotate("i = I₀ / 2  →  t = τ · ln 2", (tl, il), (tl + 30, il + 3.4),
                    color=NAVY, fontsize=11.5,
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.3))
        ax.plot([tau], [I0 * np.exp(-1)], "o", color=RED, ms=6)
        ax.text(tau + 8, I0 * np.exp(-1) + 0.7, "τ = 50,5 µs", color=RED,
                fontsize=11)
    fig.tight_layout()
    save(fig, nom)

# ===================================== B5 : grilles de tracé (question 5)
E, R1, R2, C = 36.0, 250.0, 200.0, 25e-6
UC = E * R2 / (R1 + R2)           # 16,0 V
tau = R2 * C                      # 5,00 ms
IC = UC / R2                      # 80,0 mA


def grilles(nom, corrige):
    t = np.linspace(0, 5 * tau, 600)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.4))
    for ax in (a1, a2):
        ax.set_xlim(0, 5 * tau * 1e3)          # en millisecondes : 0 à 25 ms
        ax.set_ylim(0, 1.08)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(NAVY)
            ax.spines[sp].set_linewidth(1.6)
        ax.grid(True, color="#DCE3EE", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_xticks(np.arange(0, 25.1, 2.5))
        # les graduations de l'ordonnée portent une pleine échelle ronde :
        # 20 V et 80 mA, la courbe de tension démarre donc à 0,8 de l'échelle
        ax.set_yticks(np.arange(0, 1.01, 0.1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(colors=NAVY, length=4)
    if corrige:
        a1.plot(t * 1e3, (UC / 20.0) * np.exp(-t / tau), color=BLUE, lw=2.6)
        a1.set_yticklabels(["%g" % v for v in np.arange(0, 20.1, 2)],
                           fontsize=9.5)
        a1.set_xticklabels([("%g" % v).replace(".", ",") for v in np.arange(0, 25.1, 2.5)],
                           fontsize=9.5)
        a1.set_xlabel("t [ms]", color=NAVY, fontsize=11, loc="right")
        a1.set_ylabel("$u_C$ [V]", color=NAVY, fontsize=11, loc="top",
                      rotation=0, labelpad=-8)
        a1.plot([tau * 1e3], [(UC / 20.0) * np.exp(-1)], "o", color=RED, ms=6)
        a1.text(tau * 1e3 + 0.4, (UC / 20.0) * np.exp(-1) + 0.03,
                "τ = 5,0 ms  →  5,89 V", color=RED, fontsize=10.5)
        a1.text(0.25, UC / 20.0 + 0.03, "$U_C$ max = 16,0 V", color=GREY,
                fontsize=10.5)
        a2.plot(t * 1e3, np.exp(-t / tau), color=RED, lw=2.6)
        a2.set_yticklabels(["%g" % v for v in np.arange(0, 80.1, 8)],
                           fontsize=9.5)
        a2.set_xticklabels([("%g" % v).replace(".", ",") for v in np.arange(0, 25.1, 2.5)],
                           fontsize=9.5)
        a2.set_xlabel("t [ms]", color=NAVY, fontsize=11, loc="right")
        a2.set_ylabel("$i_C$ [mA]", color=NAVY, fontsize=11, loc="top",
                      rotation=0, labelpad=-8)
        a2.plot([tau * 1e3], [np.exp(-1)], "o", color=RED, ms=6)
        a2.text(tau * 1e3 + 0.4, np.exp(-1) + 0.03,
                "τ = 5,0 ms  →  29,4 mA", color=RED, fontsize=10.5)
        a2.text(0.25, 1.02, "$I_C$ max = 80,0 mA", color=GREY, fontsize=10.5)
    fig.tight_layout()
    save(fig, nom)


grilles("B5_grilles", False)
grilles("B5c_grilles", True)
print("courbes test 320 B : ok")
