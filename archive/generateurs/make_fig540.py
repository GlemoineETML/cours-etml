# -*- coding: utf-8 -*-
"""Test 540 — schémas CEI (cairosvg) et grilles de tracé (matplotlib)."""
import cairosvg, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["font.family"] = ["Carlito", "DejaVu Sans"]
rcParams["mathtext.fontset"] = "dejavusans"
NAVY, BLUE, RED, GREY = "#242852", "#297FD5", "#EE0000", "#7F8FA9"
FONT = "Carlito, Calibri, sans-serif"

# ------------------------------------------------------------------ SVG
def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{FONT}"><defs>'
            f'<marker id="ar" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
            f'<path d="M0,0 L10,4 L0,8 z" fill="{NAVY}"/></marker></defs>'
            '<rect width="100%" height="100%" fill="white"/>')

def W(pts, wd=2.6):
    d = " ".join(("M" if i == 0 else "L") + f"{x},{y}" for i, (x, y) in enumerate(pts))
    return f'<path d="{d}" stroke="{NAVY}" stroke-width="{wd}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'

def T(x, y, s, size=18, anchor="middle", style="normal", sub=None, weight="normal"):
    sb = (f'<tspan dy="5" font-size="{size*0.72:.1f}">{sub}</tspan>' if sub else "")
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{NAVY}" text-anchor="{anchor}" '
            f'font-style="{style}" font-weight="{weight}">{s}{sb}</text>')

def gen_v(cx, cy, r=26):
    """Générateur d'impulsions : cercle + impulsion rectangulaire stylisée."""
    p = [(cx-15, cy+8), (cx-7, cy+8), (cx-7, cy-8), (cx+7, cy-8), (cx+7, cy+8), (cx+15, cy+8)]
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" stroke="{NAVY}" stroke-width="2.6"/>'
            + W(p, 2.0))

def res_v(cx, cy, w=26, h=64):
    return (f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="white" '
            f'stroke="{NAVY}" stroke-width="2.6"/>')

def cap_h(cx, cy, gap=12, h=44):
    return (f'<line x1="{cx-gap/2}" y1="{cy-h/2}" x2="{cx-gap/2}" y2="{cy+h/2}" stroke="{NAVY}" stroke-width="3.4"/>'
            f'<line x1="{cx+gap/2}" y1="{cy-h/2}" x2="{cx+gap/2}" y2="{cy+h/2}" stroke="{NAVY}" stroke-width="3.4"/>')

def ind_h(x0, cy, n=4, r=11):
    """Inductance CEI 60617 : demi-cercles."""
    d = f"M{x0},{cy} " + " ".join(f"a{r},{r} 0 0 1 {2*r},0" for _ in range(n))
    return f'<path d="{d}" stroke="{NAVY}" stroke-width="2.6" fill="none"/>'

def masse(x, y):
    return (W([(x, y), (x, y+12)]) + W([(x-14, y+12), (x+14, y+12)])
            + W([(x-9, y+18), (x+9, y+18)]) + W([(x-4, y+24), (x+4, y+24)]))

def borne(x, y):
    return f'<circle cx="{x}" cy="{y}" r="4.5" fill="white" stroke="{NAVY}" stroke-width="2.2"/>'

def varrow(x, y1, y2, lab, sub, side="left"):
    a = (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{NAVY}" stroke-width="2.2" marker-end="url(#ar)"/>')
    tx = x - 30 if side == "left" else x + 10
    return a + T(tx, (y1+y2)/2+6, lab, 19, "start", "italic", sub)

def dot(x, y):
    return f'<circle cx="{x}" cy="{y}" r="4" fill="{NAVY}"/>'

def circuit(nom, comp, nomc, valc):
    w, h = 560, 270
    yt, yb, xs, xr, xo = 50, 220, 110, 400, 490
    s = head(w, h)
    s += gen_v(xs, 135)
    s += W([(xs, 109), (xs, yt), (215, yt)]) + W([(xs, 161), (xs, yb), (xo, yb)])
    if comp == "C":
        s += cap_h(255, yt) + W([(215, yt), (249, yt)]) + W([(261, yt), (xo, yt)])
    else:
        s += W([(215, yt), (211, yt)]) + ind_h(211, yt) + W([(299, yt), (xo, yt)])
    s += res_v(xr, 135) + W([(xr, yt), (xr, 103)]) + W([(xr, 167), (xr, yb)])
    s += dot(xr, yt) + dot(xr, yb) + borne(xo, yt) + borne(xo, yb) + masse(xr, yb)
    s += T(255, yt-30, nomc[0], 19, sub=nomc[1]) + T(255, yt+48 if comp=="C" else yt+38, valc, 17)
    s += T(xr+24, 130, "R", 19, "start", sub="1") + T(xr+24, 152, RV, 17, "start")
    s += varrow(xs-46, 105, 165, "u", "e") + varrow(xo+18, yt+20, yb-20, "u", "s", "right")
    s += "</svg>"
    open(f"fig/{nom}.svg", "w").write(s)
    cairosvg.svg2png(url=f"fig/{nom}.svg", write_to=f"fig/{nom}.png", scale=2.6, background_color="white")
    print("ok", nom)

RV = "1,5 kΩ"; circuit("E1_circuit", "C", ("C", "1"), "2,2 µF")
RV = "56 Ω";   circuit("E2_circuit", "L", ("L", "1"), "150 mH")

# ------------------------------------------------------------------ grilles
def grille(ax, x0, x1, dx, lx, y0, y1, dy, ly, ylab):
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_xticks(np.arange(x0, x1+1e-9, dx), minor=True)
    ax.set_yticks(np.arange(y0, y1+1e-9, dy), minor=True)
    ax.set_xticks(lx); ax.set_yticks(ly)
    ax.set_xticklabels([("%g" % v).replace(".", ",") for v in lx], fontsize=10)
    ax.set_yticklabels([("%g" % v).replace(".", ",").replace("-", "−") for v in ly], fontsize=10)
    ax.grid(True, which="minor", color="#C9D2E2", lw=0.6)
    ax.grid(True, which="major", color="#A9B6CC", lw=0.8)
    ax.set_axisbelow(True)
    for sp in ax.spines.values():
        sp.set_color(GREY); sp.set_linewidth(0.8)
    ax.axhline(0, color=NAVY, lw=1.4)
    ax.tick_params(colors=NAVY, which="both", length=0)
    ax.set_xlabel("t [ms]", color=NAVY, fontsize=11, loc="right")
    ax.set_ylabel(ylab, color=NAVY, fontsize=11, loc="top", rotation=0, labelpad=-4)

def save(fig, nom):
    fig.savefig(f"fig/{nom}.png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig); print("ok", nom)

# ===== Exercice 1 : RC dérivateur
U, tp, tau = 15.0, 8.0, 1.5e3*2.2e-6*1e3          # ms
v1 = U*np.exp(-7.999/tau); v2 = v1 - U
dt3 = tau*np.log(abs(v2)/0.2); t3 = tp + dt3
def repere(ax, x, y, x0=None):
    """Pointillés de lecture d'un point vers l'axe des temps."""
    ax.plot([x, x], [0, y], color=RED, lw=1.0, ls=":", zorder=4)
for nom, corr in (("E1_grille", False), ("E1c_grille", True)):
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    grille(ax, -2, 32, 1, list(range(0, 33, 4)), -16, 16, 1, [-15, -10, -5, 0, 5, 10, 15], "u [V]")
    ax.plot([-2, 0, 0, tp, tp, 32], [0, 0, U, U, 0, 0], color="black", lw=2.6, label="$u_e$")
    if corr:
        # saut 0 → +15 V à t = 0 (u_C ne peut pas varier instantanément)
        ax.plot([0, 0], [0, U], color=BLUE, lw=2.4, zorder=3)
        t = np.linspace(0, tp, 300); ax.plot(t, U*np.exp(-t/tau), color=BLUE, lw=2.4, label="$u_s$", zorder=3)
        ax.plot([tp, tp], [v1, v2], color=BLUE, lw=2.4, zorder=3)
        t = np.linspace(tp, 32, 400); ax.plot(t, v2*np.exp(-(t-tp)/tau), color=BLUE, lw=2.4, zorder=3)
        for (x, y) in ((0, U), (tp, v1), (tp, v2), (t3, -0.2)):
            ax.plot([x], [y], "o", color=RED, ms=5, zorder=5)
        # repères à 1 τ : 37 % de la valeur de départ
        ya, yb = U*np.exp(-1), v2*np.exp(-1)
        for (x, y) in ((tau, ya), (tp+tau, yb)):
            ax.plot([x], [y], "o", color=RED, ms=4, mfc="white", zorder=5); repere(ax, x, y)
        kw = dict(color=RED, fontsize=10.5)
        ax.annotate("+15 V  (t = 0⁺)", (0, U), (1.0, 13.2), **kw)
        ax.annotate("τ = 3,3 ms\n5,52 V (37 %)", (tau, ya), (0.8, -5.2),
                    arrowprops=dict(arrowstyle="->", color=RED), **kw)
        ax.annotate("1,329 V  (t₁)", (tp, v1), (9.0, 3.2), arrowprops=dict(arrowstyle="->", color=RED), **kw)
        ax.annotate("−13,67 V  (t₂)", (tp, v2), (8.8, -15.2), **kw)
        ax.annotate("t₂ + τ = 11,3 ms : −5,03 V (37 %)", (tp+tau, yb), (12.6, -11.0),
                    arrowprops=dict(arrowstyle="->", color=RED), **kw)
        ax.annotate("−200 mV à t₃ = 21,94 ms", (t3, -0.2), (19.0, -5.0),
                    arrowprops=dict(arrowstyle="->", color=RED), **kw)
        ax.legend(loc="upper right", fontsize=10, frameon=True)
    fig.tight_layout(); save(fig, nom)

# ===== Exercice 2 : RL
U, tp, L, R = 20.0, 6.0, 150e-3, 56.0
tau = L/R*1e3; I = U/R
vmax = U*(1-np.exp(-tp/tau))
for nom, corr in (("E2_grille", False), ("E2c_grille", True)):
    fig, ax = plt.subplots(figsize=(7.4, 3.3))
    grille(ax, -1, 21, 0.5, list(range(0, 21, 2)), -1, 22, 1, [0, 5, 10, 15, 20], "u [V]")
    ax.plot([-1, 0, 0, tp, tp, 21], [0, 0, U, U, 0, 0], color="black", lw=2.6, label="$u_e$")
    if corr:
        t = np.linspace(0, tp, 300); ax.plot(t, U*(1-np.exp(-t/tau)), color=BLUE, lw=2.4, label="$u_s$", zorder=3)
        t = np.linspace(tp, 21, 400); ax.plot(t, vmax*np.exp(-(t-tp)/tau), color=BLUE, lw=2.4, zorder=3)
        ya, yb = U*(1-np.exp(-1)), vmax*np.exp(-1)
        ax.plot([tp], [vmax], "o", color=RED, ms=5, zorder=5)
        for (x, y) in ((tau, ya), (tp+tau, yb)):
            ax.plot([x], [y], "o", color=RED, ms=4.5, zorder=5); repere(ax, x, y)
        ax.plot([tp+5*tau], [vmax*np.exp(-5)], "o", color=RED, ms=4, mfc="white", zorder=5)
        kw = dict(color=RED, fontsize=10.5)
        ax.annotate("17,87 V (t = 6 ms)", (tp, vmax), (6.6, 18.6), **kw)
        ax.annotate("τ = 2,68 ms\n12,64 V (63 %)", (tau, ya), (2.9, 5.2),
                    arrowprops=dict(arrowstyle="->", color=RED), **kw)
        ax.annotate("6 + τ = 8,68 ms : 6,57 V (37 %)", (tp+tau, yb), (9.6, 9.0),
                    arrowprops=dict(arrowstyle="->", color=RED), **kw)
        ax.annotate("6 + 5τ = 19,4 ms : ≈ 0 V (0,12 V)", (tp+5*tau, vmax*np.exp(-5)), (12.6, 3.2),
                    arrowprops=dict(arrowstyle="->", color=RED), **kw)
        ax.legend(loc="upper right", fontsize=10, frameon=True)
    fig.tight_layout(); save(fig, nom)
print("tau1", 3.3, "v1", v1, "t3", t3, "| tau2", tau, "vmax", vmax)
