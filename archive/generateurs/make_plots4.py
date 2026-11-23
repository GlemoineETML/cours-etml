# -*- coding: utf-8 -*-
"""Chapitre 300 — courbes du régime transitoire RC."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

rcParams["font.family"] = ["Carlito", "DejaVu Sans"]
rcParams["mathtext.fontset"] = "dejavusans"
rcParams["axes.formatter.use_locale"] = False
NAVY, BLUE, RED, GREY, LBLUE = "#242852", "#297FD5", "#EE0000", "#7F8FA9", "#ACCBF9"


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


# ====================================================== 80 charge : uc et i
E, R, C = 12.0, 2e3, 100e-9
tau = R * C                     # 200 µs
I0 = E / R                      # 6 mA
t = np.linspace(0, 5 * tau, 600)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.4, 3.5))

cadre(a1, "t     (τ = 200 µs)", "$u_C$ [V]", 5 * tau * 1e6, E * 1.12)
a1.plot(t * 1e6, E * (1 - np.exp(-t / tau)), color=BLUE, lw=2.6)
a1.axhline(E, color=GREY, ls="--", lw=1.2)
a1.plot([tau * 1e6, tau * 1e6], [0, 0.632 * E], color=RED, ls=":", lw=1.6)
a1.plot([0, tau * 1e6], [0.632 * E, 0.632 * E], color=RED, ls=":", lw=1.6)
a1.plot([tau * 1e6], [0.632 * E], "o", color=RED, ms=6)
a1.annotate("63 % de E", (tau * 1e6, 0.632 * E), (tau * 1e6 + 60, 0.632 * E - 2.6),
            color=RED, fontsize=11, arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
a1.text(5, E + 0.2, "E = 12 V", color=GREY, fontsize=11)
a1.set_xticks([0, 200, 400, 600, 800, 1000])
a1.set_xticklabels(["0", "τ", "2τ", "3τ", "4τ", "5τ"])

cadre(a2, "t     (τ = 200 µs)", "$i_C$ [mA]", 5 * tau * 1e6, I0 * 1e3 * 1.12)
a2.plot(t * 1e6, I0 * 1e3 * np.exp(-t / tau), color=RED, lw=2.6)
a2.plot([tau * 1e6, tau * 1e6], [0, 0.368 * I0 * 1e3], color=RED, ls=":", lw=1.6)
a2.plot([0, tau * 1e6], [0.368 * I0 * 1e3] * 2, color=RED, ls=":", lw=1.6)
a2.plot([tau * 1e6], [0.368 * I0 * 1e3], "o", color=RED, ms=6)
a2.annotate("37 % de I₀", (tau * 1e6, 0.368 * I0 * 1e3),
            (tau * 1e6 + 60, 0.368 * I0 * 1e3 + 1.4), color=RED, fontsize=11,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
a2.text(5, I0 * 1e3 + 0.1, "I₀ = E / R = 6 mA", color=GREY, fontsize=11)
a2.set_xticks([0, 200, 400, 600, 800, 1000])
a2.set_xticklabels(["0", "τ", "2τ", "3τ", "4τ", "5τ"])
fig.tight_layout()
save(fig, "80_charge")

# ====================================================== 81 les cinq tau
fig, ax = plt.subplots(figsize=(8.6, 3.2))
t = np.linspace(0, 5, 500)
cadre(ax, "t", "$u_C$", 5.4, 112)
ax.plot(t, 100 * (1 - np.exp(-t)), color=BLUE, lw=2.8)
ax.axhline(100, color=GREY, ls="--", lw=1.2)
for k, v in enumerate([63.2, 86.5, 95.0, 98.2, 99.3], start=1):
    ax.plot([k, k], [0, v], color="#C9D3E5", lw=1.1)
    ax.plot([k], [v], "o", color=RED, ms=5)
    ax.text(k, v + 3.5, ("%.1f" % v).replace(".", ",") + " %", color=RED,
            fontsize=10.5, ha="center")
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xticklabels(["τ", "2τ", "3τ", "4τ", "5τ"])
ax.set_yticks([0, 50, 100])
ax.set_yticklabels(["0", "50 %", "100 %"])
ax.text(2.55, 40, "on considère le régime établi après 5 τ", color=GREY, fontsize=11.5)
fig.tight_layout()
save(fig, "81_cinq_tau")

# ====================================================== 82 lecture (exemple du cours)
U, R = 20.0, 1e3
I0 = U / R * 1e3                 # 20 mA
tl, il = 15.0, 10.0              # point lu : 15 µs ; 10 mA
tau = tl / np.log(I0 / il)       # 21,64 µs
t = np.linspace(0, 5 * tau, 600)
fig, ax = plt.subplots(figsize=(7.4, 3.6))
cadre(ax, "t [µs]", "$i_C$ [mA]", 5 * tau, I0 * 1.14)
ax.plot(t, I0 * np.exp(-t / tau), color=RED, lw=2.8)
ax.plot([0, tl], [il, il], color=NAVY, ls=":", lw=1.6)
ax.plot([tl, tl], [0, il], color=NAVY, ls=":", lw=1.6)
ax.plot([tl], [il], "o", color=NAVY, ms=7)
ax.annotate("point lu :  15 µs ;  10 mA", (tl, il), (tl + 14, il + 3.4), color=NAVY,
            fontsize=11.5, arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.3))
ax.text(1.5, I0 + 0.7, "I₀ = U / R = 20 mA", color=GREY, fontsize=11)
ax.set_xticks([0, 15, 30, 60, 90])
fig.tight_layout()
save(fig, "82_lecture")

# ====================================================== 83 décharge (exemple du cours)
E, R1, R2, Cc = 20.0, 30.0, 20.0, 4e-6
UC = E * R2 / (R1 + R2)          # 8 V
tau = R2 * Cc                    # 80 µs
IC = UC / R2                     # 0,4 A
t = np.linspace(0, 5 * tau, 600)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.4, 3.5))
cadre(a1, "t [µs]", "$u_C$ [V]", 5 * tau * 1e6, UC * 1.15)
a1.plot(t * 1e6, UC * np.exp(-t / tau), color=BLUE, lw=2.6)
a1.plot([tau * 1e6], [0.368 * UC], "o", color=RED, ms=6)
a1.plot([tau * 1e6, tau * 1e6], [0, 0.368 * UC], color=RED, ls=":", lw=1.5)
a1.plot([0, tau * 1e6], [0.368 * UC] * 2, color=RED, ls=":", lw=1.5)
a1.text(tau * 1e6 + 12, 0.368 * UC + 0.5, "37 %  →  2,94 V", color=RED, fontsize=11)
a1.text(5, UC + 0.15, "$U_C$ max = 8 V", color=GREY, fontsize=11)
a1.set_xticks([0, 80, 160, 240, 320, 400])

cadre(a2, "t [µs]", "$i_C$ [mA]", 5 * tau * 1e6, IC * 1e3 * 1.15)
a2.plot(t * 1e6, IC * 1e3 * np.exp(-t / tau), color=RED, lw=2.6)
a2.plot([tau * 1e6], [0.368 * IC * 1e3], "o", color=RED, ms=6)
a2.plot([tau * 1e6, tau * 1e6], [0, 0.368 * IC * 1e3], color=RED, ls=":", lw=1.5)
a2.plot([0, tau * 1e6], [0.368 * IC * 1e3] * 2, color=RED, ls=":", lw=1.5)
a2.text(tau * 1e6 + 12, 0.368 * IC * 1e3 + 22, "37 % → 147 mA", color=RED, fontsize=11)
a2.text(5, IC * 1e3 + 8, "$I_C$ max = 400 mA", color=GREY, fontsize=11)
a2.set_xticks([0, 80, 160, 240, 320, 400])
fig.tight_layout()
save(fig, "83_decharge")

# ====================================================== 84 courbe de l'exercice 5
U, R = 10.0, 1e3
I0 = U / R * 1e3                 # 10 mA
tl, il = 33.0, 5.0
tau = tl / np.log(I0 / il)       # 47,61 µs
t = np.linspace(0, 5 * tau, 600)
for suffixe, corrige in (("84_ex5_courbe", False), ("84c_ex5_courbe", True)):
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    cadre(ax, "t [µs]", "$i_C$ [mA]", 5 * tau, I0 * 1.14)
    ax.plot(t, I0 * np.exp(-t / tau), color=RED, lw=2.8)
    ax.plot([0, tl], [il, il], color=NAVY, ls=":", lw=1.6)
    ax.plot([tl, tl], [0, il], color=NAVY, ls=":", lw=1.6)
    ax.plot([tl], [il], "o", color=NAVY, ms=7)
    ax.set_xticks([0, 33, 60, 120, 180, 240])
    ax.set_yticks([0, 5, 10])
    if corrige:
        ax.annotate("i = I₀ / 2  →  t = τ · ln 2", (tl, il), (tl + 24, il + 2.8),
                    color=NAVY, fontsize=11.5,
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.3))
        ax.plot([tau], [I0 * np.exp(-1)], "o", color=RED, ms=6)
        ax.text(tau + 6, I0 * np.exp(-1) + 0.5, "τ = 47,6 µs", color=RED, fontsize=11)
    fig.tight_layout()
    save(fig, suffixe)

# ====================================================== 85 grilles à compléter
def grille(nom, corrige):
    E, R1, R2, Cc = 18.0, 20.0, 40.0, 2.5e-6
    UC = E * R2 / (R1 + R2)      # 12 V
    tau = R2 * Cc                # 100 µs
    IC = UC / R2                 # 0,3 A
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
        ax.set_xticks(np.arange(0, 501, 50))
        ax.set_yticks(np.arange(0, 1.01, 0.1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(colors=NAVY, length=4)
    if corrige:
        a1.plot(t * 1e6, np.exp(-t / tau), color=BLUE, lw=2.6)
        a1.set_yticklabels(["%g" % v for v in np.arange(0, 12.1, 1.2)], fontsize=9.5)
        a1.set_xticklabels(["%d" % v for v in np.arange(0, 501, 50)], fontsize=9.5)
        a1.set_xlabel("t [µs]", color=NAVY, fontsize=11, loc="right")
        a1.set_ylabel("$u_C$ [V]", color=NAVY, fontsize=11, loc="top", rotation=0, labelpad=-8)
        a1.plot([100], [np.exp(-1)], "o", color=RED, ms=6)
        a1.text(112, np.exp(-1) + 0.03, "τ = 100 µs  →  4,4 V", color=RED, fontsize=10.5)
        a1.text(6, 1.04, "$U_C$ max = 12 V", color=GREY, fontsize=10.5)
        a2.plot(t * 1e6, np.exp(-t / tau), color=RED, lw=2.6)
        a2.set_yticklabels(["%g" % v for v in np.arange(0, 301, 30)], fontsize=9.5)
        a2.set_xticklabels(["%d" % v for v in np.arange(0, 501, 50)], fontsize=9.5)
        a2.set_xlabel("t [µs]", color=NAVY, fontsize=11, loc="right")
        a2.set_ylabel("$i_C$ [mA]", color=NAVY, fontsize=11, loc="top", rotation=0, labelpad=-8)
        a2.plot([100], [np.exp(-1)], "o", color=RED, ms=6)
        a2.text(112, np.exp(-1) + 0.03, "τ = 100 µs  →  110 mA", color=RED, fontsize=10.5)
        a2.text(6, 1.04, "$I_C$ max = 300 mA", color=GREY, fontsize=10.5)
    fig.tight_layout()
    save(fig, nom)


grille("85_grilles", False)
grille("85c_grilles", True)
print("courbes 300 : ok")
