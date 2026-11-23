# -*- coding: utf-8 -*-
"""Grille de l'exercice N°3 : u_C(t) pour U = 12 V, τ = 1 s (vierge / corrigé)."""
import math
from figs_charge_rc import plt, NAVY, BLUE, LBLUE, RED, GREY
def grille(path, corr):
    fig, a = plt.subplots(figsize=(7.0, 3.6))
    a.set_xlim(0, 5.5); a.set_ylim(0, 13)
    a.set_xticks([x / 2 for x in range(12)]); a.set_xticklabels([("%g" % (x / 2)).replace(".", ",") if x % 2 == 0 else "" for x in range(12)])
    a.set_yticks(range(0, 14)); a.set_yticklabels([str(y) if y % 2 == 0 else "" for y in range(14)])
    a.grid(color=LBLUE, lw=0.8); a.set_axisbelow(True)
    for sp in ("top", "right"): a.spines[sp].set_visible(False)
    a.tick_params(colors=NAVY)
    a.set_xlabel(r"$t$ en s", color=NAVY); a.set_ylabel(r"$u_\mathrm{C}$ en V", color=NAVY)
    if corr:
        t = [x / 100 for x in range(0, 551)]
        a.plot(t, [12 * (1 - math.e ** -x) for x in t], color=RED, lw=2.2)
        for n in range(6): a.plot(n, 12 * (1 - math.e ** -n), "o", color=RED, ms=6)
        a.axhline(12, color=RED, lw=1, ls="--")
    fig.tight_layout(); fig.savefig(path, dpi=220, facecolor="white"); plt.close(fig)
grille("fig_n3_vierge.png", False); grille("fig_n3.png", True); print("ok")
