# -*- coding: utf-8 -*-
"""Figures « Charge d'un condensateur » — schéma RC (symboles CEI 60617), courbes, écran d'oscilloscope.
Couleurs ETML : marine 242852, bleu 297FD5, bleu clair ACCBF9 ; réponses en rouge EE0000."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

NAVY, BLUE, LBLUE, RED, GREY = "#242852", "#297FD5", "#ACCBF9", "#EE0000", "#5A6478"
plt.rcParams.update({"font.family": "Liberation Sans", "mathtext.fontset": "custom",
                     "mathtext.rm": "Liberation Sans", "mathtext.it": "Liberation Sans:italic",
                     "mathtext.bf": "Liberation Sans:bold", "font.size": 12})
E = math.e


def arrow(ax, x0, y0, x1, y1, color=BLUE, lw=1.8):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=16, color=color, lw=lw))


# ------------------------------------------------------------------ schéma CEI du circuit de charge
def schema(path):
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.set_aspect("equal"); ax.axis("off")
    k = dict(color=NAVY, lw=2.2, solid_capstyle="round")
    # fils
    ax.plot([0, 0], [0, 1.05], **k); ax.plot([0, 0], [1.95, 3], **k)
    ax.plot([0, 0.9], [3, 3], **k); ax.plot([1.85, 2.6], [3, 3], **k); ax.plot([4.2, 6], [3, 3], **k)
    ax.plot([6, 6], [3, 1.62], **k); ax.plot([6, 6], [1.38, 0], **k); ax.plot([0, 6], [0, 0], **k)
    # source de tension idéale CEI : cercle traversé par un trait dans le sens du conducteur
    ax.add_patch(Circle((0, 1.5), 0.45, fill=False, ec=NAVY, lw=2.2)); ax.plot([0, 0], [1.05, 1.95], **k)
    ax.text(-0.25, 2.12, "+", fontsize=15, color=NAVY, ha="center", va="center", fontweight="bold")
    arrow(ax, -0.85, 2.05, -0.85, 0.95); ax.text(-1.15, 1.5, r"$U$", fontsize=17, color=BLUE, ha="right", va="center")
    # interrupteur S (contact à fermeture, CEI)
    ax.plot([0.9, 1.78], [3, 3.42], **k)
    ax.add_patch(Circle((0.9, 3), 0.05, color=NAVY)); ax.plot([1.85, 1.85], [3, 3.18], **k)
    ax.text(1.35, 3.62, "S", fontsize=15, color=NAVY, ha="center", fontweight="bold")
    # résistance CEI : rectangle
    ax.add_patch(Rectangle((2.6, 2.78), 1.6, 0.44, fill=False, ec=NAVY, lw=2.2))
    ax.text(3.4, 2.45, r"$R$", fontsize=16, color=NAVY, ha="center", va="center")
    arrow(ax, 2.65, 3.62, 4.15, 3.62); ax.text(3.4, 3.82, r"$u_\mathrm{R}$", fontsize=16, color=BLUE, ha="center")
    # courant
    arrow(ax, 4.75, 3, 5.35, 3, color=RED, lw=2.0); ax.text(5.05, 3.22, r"$i$", fontsize=16, color=RED, ha="center")
    # condensateur CEI : deux plaques parallèles
    ax.plot([5.5, 6.5], [1.62, 1.62], color=NAVY, lw=3.2); ax.plot([5.5, 6.5], [1.38, 1.38], color=NAVY, lw=3.2)
    ax.text(5.3, 1.5, r"$C$", fontsize=16, color=NAVY, ha="right", va="center")
    arrow(ax, 6.85, 2.05, 6.85, 0.95); ax.text(7.05, 1.5, r"$u_\mathrm{C}$", fontsize=17, color=BLUE, ha="left", va="center")
    ax.set_xlim(-1.7, 7.8); ax.set_ylim(-0.3, 4.1)
    fig.savefig(path, dpi=220, bbox_inches="tight", transparent=False, facecolor="white"); plt.close(fig)


# ------------------------------------------------------------------ courbes u_C(t) et i(t)
def courbes(path):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 2.9))
    t = [x / 100 for x in range(0, 601)]
    for a, y, lab, col, tit in ((a1, [1 - E ** -x for x in t], r"$u_\mathrm{C}$", BLUE, r"Tension $u_\mathrm{C}(t)$ : elle monte puis se stabilise"),
                                (a2, [E ** -x for x in t], r"$i$", RED, r"Courant $i(t)$ : maximal au départ, puis nul")):
        a.plot(t, y, color=col, lw=2.6)
        a.set_xlim(0, 6); a.set_ylim(0, 1.12)
        a.set_xticks(range(0, 7)); a.set_xticklabels(["0"] + [rf"${n}\tau$" if n > 1 else r"$\tau$" for n in range(1, 7)])
        a.grid(color=LBLUE, lw=0.8); a.set_axisbelow(True)
        for sp in ("top", "right"): a.spines[sp].set_visible(False)
        for sp in ("left", "bottom"): a.spines[sp].set_color(NAVY)
        a.tick_params(colors=NAVY)
        a.set_xlabel(r"temps $t$", color=NAVY); a.set_title(tit, color=NAVY, fontsize=11, loc="left")
    a1.set_yticks([0, 0.632, 1]); a1.set_yticklabels(["0", "63 %", r"$U$"])
    a1.axhline(1, color=NAVY, lw=1, ls="--")
    a2.set_yticks([0, 0.368, 1]); a2.set_yticklabels(["0", "37 %", r"$I_0=\frac{U}{R}$"])
    a1.text(4.3, 0.82, "chargé à 99 %\naprès 5τ", color=NAVY, fontsize=11, ha="center")
    a2.text(3.6, 0.45, "le condensateur plein\nbloque le courant continu", color=NAVY, fontsize=11, ha="center")
    fig.tight_layout(); fig.savefig(path, dpi=220, facecolor="white"); plt.close(fig)


# ------------------------------------------------------------------ les 5 tau (pourcentages)
def tau(path):
    fig, a = plt.subplots(figsize=(5.6, 3.6))
    t = [x / 100 for x in range(0, 551)]
    a.plot(t, [100 * (1 - E ** -x) for x in t], color=BLUE, lw=2.8)
    a.plot([0, 1], [0, 100], color=GREY, lw=1.3, ls="--")
    a.text(1.05, 101.5, "tangente à l'origine", color=GREY, fontsize=9.5, ha="left", va="bottom")
    for n in range(1, 6):
        v = 100 * (1 - E ** -n)
        a.plot([n, n], [0, v], color=NAVY, lw=1, ls=":"); a.plot(n, v, "o", color=NAVY, ms=6)
        a.text(n + 0.06, v - 7.5, f"{v:.0f} %".replace(".", ","), color=NAVY, fontsize=11, fontweight="bold")
    a.axhline(100, color=NAVY, lw=1, ls="--")
    a.set_xlim(0, 5.5); a.set_ylim(0, 112)
    a.set_xticks(range(0, 6)); a.set_xticklabels(["0", r"$\tau$", r"$2\tau$", r"$3\tau$", r"$4\tau$", r"$5\tau$"])
    a.set_yticks([0, 25, 50, 75, 100]); a.set_yticklabels(["0", "25 %", "50 %", "75 %", "100 %"])
    a.set_ylabel(r"$u_\mathrm{C}$ en % de $U$", color=NAVY); a.set_xlabel(r"temps $t$", color=NAVY)
    a.grid(color=LBLUE, lw=0.8); a.set_axisbelow(True)
    for sp in ("top", "right"): a.spines[sp].set_visible(False)
    a.tick_params(colors=NAVY)
    fig.tight_layout(); fig.savefig(path, dpi=220, facecolor="white"); plt.close(fig)


# ------------------------------------------------------------------ écran d'oscilloscope
def oscillo(path, U, tau_ms, tdiv, vdiv, construct=False, legend=True):
    """Grille 10 × 8 divisions, masse à -4 div (bas d'écran), départ de la charge à 1 div."""
    fig, a = plt.subplots(figsize=(6.4, 4.5))
    a.set_facecolor("#0E1A2E")
    for x in range(11): a.axvline(x, color="#3B5579", lw=0.8)
    for y in range(9): a.axhline(y, color="#3B5579", lw=0.8)
    for x in [i / 5 for i in range(51)]: a.plot([x, x], [3.9, 4.1], color="#5C7DA8", lw=0.6)
    for y in [i / 5 for i in range(41)]: a.plot([4.9, 5.1], [y, y], color="#5C7DA8", lw=0.6)
    t0 = 1.0
    xs = [i / 200 for i in range(0, 2001)]
    ys = [0 if x < t0 else (U * (1 - E ** (-(x - t0) * tdiv / tau_ms))) / vdiv for x in xs]
    a.plot(xs, ys, color="#FFD23F", lw=2.4)
    a.text(0.1, 0.15, "1 >", color="#FFD23F", fontsize=11, fontweight="bold")
    if construct:
        y63 = 0.632 * U / vdiv; xt = t0 + tau_ms / tdiv
        a.plot([0, 10], [U / vdiv, U / vdiv], color=RED, lw=1.4, ls="--")
        a.plot([t0, xt], [y63, y63], color=RED, lw=1.6); a.plot([xt, xt], [0, y63], color=RED, lw=1.6)
        a.plot([t0, xt], [0, U / vdiv], color=RED, lw=1.2, ls=":")
        a.text(xt + 0.1, 0.25, "τ", color=RED, fontsize=16, fontweight="bold")
        a.text(9.9, y63 + 0.1, f"63 % = {0.632 * U:.2f} V".replace(".", ","), color=RED, fontsize=11, ha="right", fontweight="bold")
    a.set_xlim(0, 10); a.set_ylim(0, 8); a.set_xticks([]); a.set_yticks([])
    for sp in a.spines.values(): sp.set_color(NAVY); sp.set_linewidth(2)
    if legend:
        f = lambda v: f"{v:g}".replace(".", ",")
        a.set_xlabel(f"CH1 : {f(vdiv)} V/div    Base de temps : {f(tdiv)} ms/div    Couplage DC    Masse en bas de l'écran",
                     color=NAVY, fontsize=10.5)
    fig.tight_layout(); fig.savefig(path, dpi=220, facecolor="white"); plt.close(fig)


if __name__ == "__main__":
    schema("fig_circuit.png"); courbes("fig_courbes.png"); tau("fig_tau.png")
    oscillo("fig_oscillo_demo.png", 10, 2, 1, 2, construct=True)          # diapositive 4
    oscillo("fig_oscillo_ex.png", 5, 4.7, 2, 1, construct=False)          # exercice N°6 (apprenti)
    oscillo("fig_oscillo_ex_corr.png", 5, 4.7, 2, 1, construct=True)      # exercice N°6 (corrigé)
    print("figures ok")
