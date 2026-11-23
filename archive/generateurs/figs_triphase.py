# -*- coding: utf-8 -*-
"""Figures « Courant alternatif triphasé » — schémas CEI 60617, diagrammes vectoriels, plaques à bornes.
Couleurs ETML : marine 242852, bleu 297FD5, bleu clair ACCBF9 ; réponses en rouge EE0000.
Convention : L1 en haut (90°), L2 à −30°, L3 à 210° (ordre des phases L1 → L2 → L3)."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

NAVY, BLUE, LBLUE, RED, GREY = "#242852", "#297FD5", "#ACCBF9", "#EE0000", "#5A6478"
C1, C2, C3 = "#8B5A2B", "#1A1A1A", "#7A7A7A"          # brun / noir / gris : couleurs des conducteurs L1 L2 L3 (CEI 60445)
PH = [C1, C2, C3]
plt.rcParams.update({"font.family": "Liberation Sans", "mathtext.fontset": "custom",
                     "mathtext.rm": "Liberation Sans", "mathtext.it": "Liberation Sans:italic",
                     "mathtext.bf": "Liberation Sans:bold", "font.size": 12})
K = dict(color=NAVY, lw=2.0, solid_capstyle="round")
ANG = [90, -30, 210]


def arrow(ax, x0, y0, x1, y1, color=BLUE, lw=1.8, ms=15):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw, shrinkA=0, shrinkB=0))


def pol(r, deg):
    return r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg))


def save(fig, path):
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white"); plt.close(fig)
    from PIL import Image; Image.open(path).convert("RGB").save(path)


def res_h(ax, x, y, w=1.0, h=0.34, lab=None, lab_dy=0.38):
    """Résistance / impédance CEI horizontale centrée sur (x, y)."""
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fill=True, fc="white", ec=NAVY, lw=2.0, zorder=3))
    if lab: ax.text(x, y + lab_dy, lab, ha="center", va="center", fontsize=13, color=NAVY)


def res_v(ax, x, y, w=1.0, h=0.34, lab=None, side=1):
    ax.add_patch(Rectangle((x - h / 2, y - w / 2), h, w, fill=True, fc="white", ec=NAVY, lw=2.0, zorder=3))
    if lab: ax.text(x + side * 0.42, y, lab, ha="left" if side > 0 else "right", va="center", fontsize=13, color=NAVY)


def dot(ax, x, y, r=0.06): ax.add_patch(Circle((x, y), r, color=NAVY, zorder=4))


def borne(ax, x, y, r=0.09): ax.add_patch(Circle((x, y), r, fc="white", ec=NAVY, lw=1.6, zorder=4))


# ------------------------------------------------------------------ 1. système triphasé : sinusoïdes + vecteurs
def systeme(path):
    fig = plt.figure(figsize=(9.0, 3.3))
    a = fig.add_axes([0.04, 0.3, 0.6, 0.62]); b = fig.add_axes([0.68, 0.04, 0.3, 0.92])
    t = [i / 400 * 360 for i in range(401)]
    for k, (c, n) in enumerate(zip(PH, ["L1", "L2", "L3"])):
        a.plot(t, [math.sin(math.radians(x - 120 * k)) for x in t], color=c, lw=2.4, label=f"$u_{{{n}}}$".replace("L", "\\mathrm{L}"))
    a.axhline(0, color=NAVY, lw=1)
    for x in (120, 240):
        a.annotate("", xy=(x, 1.12), xytext=(x - 120, 1.12), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.3))
        a.text(x - 60, 1.2, "120°", ha="center", color=BLUE, fontsize=11, fontweight="bold")
    a.annotate("", xy=(120, 1.12), xytext=(0, 1.12), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.3))
    a.text(60, 1.2, "120°", ha="center", color=BLUE, fontsize=11, fontweight="bold")
    a.set_xlim(0, 360); a.set_ylim(-1.15, 1.42); a.set_yticks([]); a.set_xticks([0, 90, 180, 270, 360])
    a.set_xticklabels(["0", r"$T/4$", r"$T/2$", r"$3T/4$", r"$T$"])
    a.set_xlabel("temps (une période T = 20 ms à 50 Hz)", color=NAVY, fontsize=10.5)
    for sp in ("top", "right", "left"): a.spines[sp].set_visible(False)
    a.legend(loc="upper left", ncol=3, frameon=False, fontsize=11, bbox_to_anchor=(0.0, -0.2))
    b.set_aspect("equal"); b.axis("off")
    for k, (c, n) in enumerate(zip(PH, ["1", "2", "3"])):
        x, y = pol(1, ANG[k]); arrow(b, 0, 0, x, y, color=c, lw=2.6, ms=18)
        lx, ly = pol(1.25, ANG[k]); b.text(lx, ly, rf"$\underline{{U}}_\mathrm{{L{n}}}$", ha="center", va="center", fontsize=13, color=c)
    b.add_patch(matplotlib.patches.Arc((0, 0), 0.7, 0.7, theta1=-30, theta2=90, color=BLUE, lw=1.3))
    b.text(0.42, 0.4, "120°", color=BLUE, fontsize=10.5)
    b.text(0, -1.0, "somme vectorielle = 0", ha="center", color=NAVY, fontsize=10.5, fontweight="bold")
    b.set_xlim(-1.45, 1.45); b.set_ylim(-1.15, 1.45)
    save(fig, path)


# ------------------------------------------------------------------ 2. tension de phase / tension réseau
def tensions(path):
    fig, a = plt.subplots(figsize=(4.6, 4.2)); a.set_aspect("equal"); a.axis("off")
    P = [pol(2.3, d) for d in ANG]
    for k in range(3):
        arrow(a, 0, 0, *P[k], color=PH[k], lw=2.4, ms=16)
    a.plot(*zip(P[0], P[1]), color=BLUE, lw=2.4); a.plot(*zip(P[1], P[2]), color=BLUE, lw=2.4); a.plot(*zip(P[2], P[0]), color=BLUE, lw=2.4)
    names = ["L1", "L2", "L3"]
    for k in range(3):
        lx, ly = pol(2.62, ANG[k]); a.text(lx, ly, names[k], ha="center", va="center", fontsize=14, fontweight="bold", color=PH[k])
    a.text(0.12, 0.95, r"$U_\mathrm{ph}$", fontsize=14, color=C1)
    a.text(1.32, 0.95, r"$U$", fontsize=16, color=BLUE, fontweight="bold")
    a.text(-0.2, -0.25, "N", fontsize=14, fontweight="bold", color=NAVY)
    dot(a, 0, 0)
    a.add_patch(matplotlib.patches.Arc(P[0], 0.9, 0.9, theta1=-90, theta2=-60, color=RED, lw=1.5))
    a.text(P[0][0] + 0.12, P[0][1] - 0.72, "30°", color=RED, fontsize=11)
    a.text(0, -2.05, r"$U=\sqrt{3}\cdot U_\mathrm{ph}$" + "\n400 V = 1,73 × 231 V", ha="center", fontsize=13, color=NAVY)
    a.set_xlim(-2.6, 2.6); a.set_ylim(-2.55, 2.85)
    save(fig, path)


# ------------------------------------------------------------------ 3. couplage étoile (avec ou sans neutre)
def _etoile_draw(a, neutre, labels):
    """Les trois lignes arrivent par la gauche ; chaque impédance est verticale ; point étoile en bas."""
    yL = [3.4, 3.0, 2.6]; yN = 0.2
    xz = [2.6, 3.8, 5.0]
    for k in range(3):
        a.plot([0.4, xz[k]], [yL[k], yL[k]], color=PH[k], lw=2.2)
        a.text(0.25, yL[k], f"L{k + 1}", ha="right", va="center", fontsize=13, fontweight="bold", color=PH[k])
        a.plot([xz[k], xz[k]], [yL[k], 2.1], **K)
        res_v(a, xz[k], 1.6, lab=(rf"$Z_{k + 1}$" if labels else None))
        a.plot([xz[k], xz[k]], [1.1, 0.75], **K)
        if k: pass
    a.plot([xz[0], xz[2]], [0.75, 0.75], **K)
    for k in range(3): dot(a, xz[k], yL[k] if False else 0.75)
    for k in range(3): dot(a, xz[k], yL[k])
    if neutre:
        a.plot([0.4, 3.8], [yN, yN], color=BLUE, lw=2.2); a.plot([3.8, 3.8], [yN, 0.75], color=BLUE, lw=2.2)
        a.text(0.25, yN, "N", ha="right", va="center", fontsize=13, fontweight="bold", color=BLUE)
        if labels:
            arrow(a, 1.4, yN, 2.1, yN, color=RED, lw=1.8); a.text(1.75, yN + 0.2, r"$I_\mathrm{N}$", color=RED, ha="center", fontsize=12)
    a.text(5.55, 0.75, "point étoile", fontsize=10.5, color=GREY, va="center")
    if labels:
        arrow(a, 0.8, 3.4, 1.5, 3.4, color=RED, lw=1.8); a.text(1.15, 3.6, r"$I$", color=RED, ha="center", fontsize=13)
        arrow(a, 2.05, 2.3, 2.05, 0.9, color=C1, lw=1.5); a.text(1.95, 1.6, r"$U_\mathrm{ph}$", color=C1, fontsize=12, ha="right", va="center")
        arrow(a, 1.85, 3.4, 1.85, 3.0, color=BLUE, lw=1.5, ms=11); a.text(1.95, 3.2, r"$U$", color=BLUE, fontsize=12, va="center")
    a.set_xlim(-0.4, 6.6); a.set_ylim(-0.05, 3.75)


# ------------------------------------------------------------------ 4. couplage triangle
def triangle(path, labels=True):
    fig, a = plt.subplots(figsize=(5.4, 3.9)); a.set_aspect("equal"); a.axis("off")
    A, Bl, Cr = (3.6, 3.3), (2.0, 0.55), (5.2, 0.55)      # A → L1, Bl → L2, Cr → L3
    def branch(P, Q, lab, side=1):
        mx, my = (P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2
        ang = math.degrees(math.atan2(Q[1] - P[1], Q[0] - P[0]))
        L = math.dist(P, Q); w = 1.0
        ux, uy = (Q[0] - P[0]) / L, (Q[1] - P[1]) / L
        a.plot([P[0], mx - ux * w / 2], [P[1], my - uy * w / 2], **K)
        a.plot([mx + ux * w / 2, Q[0]], [my + uy * w / 2, Q[1]], **K)
        r = Rectangle((mx - w / 2, my - 0.17), w, 0.34, fc="white", ec=NAVY, lw=2.0, zorder=3)
        r.set_transform(matplotlib.transforms.Affine2D().rotate_deg_around(mx, my, ang) + a.transData); a.add_patch(r)
        if labels:
            nx, ny = -uy * side, ux * side
            a.text(mx + nx * 0.5, my + ny * 0.5, lab, ha="center", va="center", fontsize=13, color=NAVY)
    branch(A, Bl, r"$Z_1$", -1); branch(Bl, Cr, r"$Z_2$", 1); branch(Cr, A, r"$Z_3$", -1)
    a.plot([0.4, A[0]], [3.75, 3.75], color=C1, lw=2.2); a.plot([A[0], A[0]], [3.75, A[1]], color=C1, lw=2.2)
    a.plot([0.4, 1.3], [-0.1, -0.1], color=C2, lw=2.2); a.plot([1.3, 1.3], [-0.1, 0.55], color=C2, lw=2.2); a.plot([1.3, 2.0], [0.55, 0.55], color=C2, lw=2.2)
    a.plot([0.4, 5.9], [-0.45, -0.45], color=C3, lw=2.2); a.plot([5.9, 5.9], [-0.45, 0.55], color=C3, lw=2.2); a.plot([5.2, 5.9], [0.55, 0.55], color=C3, lw=2.2)
    for P in (A, Bl, Cr): dot(a, *P)
    for y, n, c in ((3.75, "L1", C1), (-0.1, "L2", C2), (-0.45, "L3", C3)):
        a.text(0.25, y, n, ha="right", va="center", fontsize=13, fontweight="bold", color=c)
    if labels:
        arrow(a, 0.8, 3.75, 1.5, 3.75, color=RED, lw=1.8); a.text(1.15, 3.95, r"$I$", color=RED, ha="center", fontsize=13)
        arrow(a, 3.05, 3.15, 2.55, 2.3, color=RED, lw=1.5); a.text(2.45, 2.85, r"$I_\mathrm{ph}$", color=RED, ha="right", fontsize=12)
        a.text(6.0, 2.6, r"$U_\mathrm{ph}=U$", ha="center", fontsize=12, color=BLUE)
    a.set_xlim(-0.4, 6.8); a.set_ylim(-0.75, 4.1)
    save(fig, path)


# ------------------------------------------------------------------ 5. plaque à bornes Y / Δ (barrettes)
def plaque(path, mode="Y", vide=False, title=True):
    fig, a = plt.subplots(figsize=(3.6, 2.8)); a.set_aspect("equal"); a.axis("off")
    a.add_patch(Rectangle((0, 0), 3.5, 2.1, fc="#F3F5F9", ec=NAVY, lw=1.8))
    X = (0.95, 1.95, 2.95)
    for (n, x) in zip(("U1", "V1", "W1"), X):
        a.add_patch(Circle((x, 1.45), 0.2, fc="white", ec=NAVY, lw=1.8, zorder=3)); a.text(x - 0.3, 1.45, n, ha="right", va="center", fontsize=10.5, color=NAVY, fontweight="bold")
    for (n, x) in zip(("W2", "U2", "V2"), X):
        a.add_patch(Circle((x, 0.65), 0.2, fc="white", ec=NAVY, lw=1.8, zorder=3)); a.text(x, 0.2, n, ha="center", va="center", fontsize=10.5, color=NAVY, fontweight="bold")
    if not vide:
        col = RED if mode.endswith("corr") else BLUE
        bar = dict(color=col, lw=7, solid_capstyle="round", alpha=0.85, zorder=5)
        if mode[0] == "Y": a.plot([X[0], X[2]], [0.65, 0.65], **bar)
        else:
            for x in X: a.plot([x, x], [0.65, 1.45], **bar)
    for x, c, n in zip(X, PH, ("L1", "L2", "L3")):
        a.plot([x, x], [1.65, 2.55], color=c, lw=2.4, zorder=2)
        a.text(x, 2.68, n, ha="center", fontsize=11, fontweight="bold", color=NAVY)
    if title and not vide:
        lab = {"Y": "couplage étoile Y", "D": "couplage triangle Δ"}[mode[0]]
        a.text(1.75, -0.35, lab, ha="center", fontsize=12, color=NAVY, fontweight="bold")
    a.set_xlim(-0.1, 3.6); a.set_ylim(-0.55, 2.95)
    save(fig, path)


# ------------------------------------------------------------------ 6. courant de neutre (déséquilibre)
def neutre_vect(path, I=(10, 6, 4), corr=True, grid_only=False):
    fig, a = plt.subplots(figsize=(4.6, 4.4)); a.set_aspect("equal")
    a.set_xticks([i for i in range(-12, 13, 2)]); a.set_yticks([i for i in range(-10, 13, 2)])
    a.grid(color=LBLUE, lw=0.7); a.tick_params(labelsize=8, colors=GREY)
    for sp in a.spines.values(): sp.set_visible(False)
    a.axhline(0, color=GREY, lw=0.6); a.axvline(0, color=GREY, lw=0.6)
    if not grid_only:
        x = y = 0
        pts = []
        for k in range(3):
            dx, dy = pol(I[k], ANG[k])
            if corr or k == 0:
                arrow(a, x, y, x + dx, y + dy, color=PH[k], lw=2.4, ms=15)
                lx, ly = x + dx / 2, y + dy / 2
                off = pol(0.9, ANG[k] + 90)
                a.text(lx + off[0], ly + off[1], rf"$I_{k + 1}$ = {I[k]} A", fontsize=10.5, color=PH[k], ha="center", va="center", fontweight="bold")
            x, y = x + dx, y + dy
        if corr:
            arrow(a, x, y, 0, 0, color=RED, lw=2.6, ms=17)
            In = math.hypot(x, y)
            a.text(x / 2 + 0.6, y / 2 - 0.6, rf"$I_\mathrm{{N}}$ ≈ {In:.1f} A".replace(".", ","), color=RED, fontsize=12, fontweight="bold")
    a.set_xlim(-11, 11); a.set_ylim(-3, 12)
    a.set_xlabel("échelle : 1 carreau = 2 A", color=NAVY, fontsize=10)
    save(fig, path)


# ------------------------------------------------------------------ 7. neutre interrompu
def neutre_coupe(path, Pa="2000 W", Pb="100 W", na="radiateur", nb="lampe"):
    fig, a = plt.subplots(figsize=(6.0, 3.6)); a.set_aspect("equal"); a.axis("off")
    ys = [3.0, 2.5, 2.0]
    for k in range(3):
        a.plot([0.3, 6.6], [ys[k], ys[k]], color=PH[k], lw=2.2)
        a.text(0.15, ys[k], f"L{k + 1}", ha="right", va="center", fontsize=12, fontweight="bold", color=PH[k])
    a.plot([0.3, 1.2], [0.3, 0.3], color=BLUE, lw=2.2); a.plot([1.7, 6.6], [0.3, 0.3], color=BLUE, lw=2.2)
    a.plot([1.2, 1.62], [0.3, 0.62], color=BLUE, lw=2.2); dot(a, 1.2, 0.3, 0.05); dot(a, 1.7, 0.3, 0.05)
    a.text(0.15, 0.3, "N", ha="right", va="center", fontsize=12, fontweight="bold", color=BLUE)
    a.text(1.45, 0.85, "neutre\nouvert", ha="center", fontsize=10, color=RED, fontweight="bold", va="bottom")
    for x, y, P, nm in ((2.8, ys[0], Pa, na), (5.0, ys[1], Pb, nb)):
        dot(a, x, y); a.plot([x, x], [y, 1.8], **K); res_v(a, x, 1.4, w=0.8)
        a.text(x + 0.3, 1.4, f"{nm}\n{P}", fontsize=10.5, color=NAVY, va="center")
        a.plot([x, x], [1.0, 0.3], **K); dot(a, x, 0.3)
    a.text(3.9, -0.05, "→ les deux appareils sont en série sous 400 V", fontsize=10, color=RED, ha="center", va="top")
    a.set_xlim(-0.3, 6.8); a.set_ylim(-0.5, 3.3)
    save(fig, path)


# ------------------------------------------------------------------ 8. mesure de puissance : 1 et 2 wattmètres
def wattmetre(ax, x, y, lab):
    ax.add_patch(Circle((x, y), 0.32, fc="white", ec=NAVY, lw=2.0, zorder=4))
    ax.text(x, y, "W", ha="center", va="center", fontsize=12, fontweight="bold", color=NAVY, zorder=5)
    ax.text(x, y + 0.5, lab, ha="center", fontsize=11, color=BLUE, fontweight="bold")


def deux_wattmetres(path):
    fig, a = plt.subplots(figsize=(5.4, 2.9)); a.set_aspect("equal"); a.axis("off")
    ys = [2.4, 1.4, 0.4]
    for k in range(3):
        a.plot([0.3, 5.2], [ys[k], ys[k]], color=PH[k], lw=2.2)
        a.text(0.15, ys[k], f"L{k + 1}", ha="right", va="center", fontsize=12, fontweight="bold", color=PH[k])
    a.add_patch(Rectangle((5.2, 0.1), 1.2, 2.6, fc=TINT_HEX, ec=NAVY, lw=2.0))
    a.text(5.8, 1.4, "récepteur\ntriphasé\nquelconque", ha="center", va="center", fontsize=9.5, color=NAVY)
    for x, y, lab in ((1.6, ys[0], r"$P_1$"), (2.9, ys[1], r"$P_2$")):
        wattmetre(a, x, y, lab)
        a.plot([x, x], [y - 0.32, ys[2]], color=GREY, lw=1.3, ls="--"); dot(a, x, ys[2], 0.05)
    a.text(3.4, -0.2, "circuits tension ramenés sur L3", fontsize=9, color=GREY, ha="center")
    save(fig, path)


TINT_HEX = "#E8EFFB"


# ------------------------------------------------------------------ 9. batterie de compensation en triangle
def compensation(path):
    fig, a = plt.subplots(figsize=(5.2, 3.0)); a.set_aspect("equal"); a.axis("off")
    ys = [2.6, 2.2, 1.8]
    for k in range(3):
        a.plot([0.3, 6.0], [ys[k], ys[k]], color=PH[k], lw=2.2)
        a.text(0.15, ys[k], f"L{k + 1}", ha="right", va="center", fontsize=12, fontweight="bold", color=PH[k])
    a.add_patch(Rectangle((6.0, 1.5), 1.1, 1.4, fc=TINT_HEX, ec=NAVY, lw=2.0)); a.text(6.55, 2.2, "atelier\nmoteurs", ha="center", va="center", fontsize=9.5, color=NAVY)
    # triangle de condensateurs
    A, B, C = (3.0, 1.2), (4.2, -0.6), (1.8, -0.6)
    def cap(P, Q):
        mx, my = (P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2
        L = math.dist(P, Q); ux, uy = (Q[0] - P[0]) / L, (Q[1] - P[1]) / L; nx, ny = -uy, ux; g = 0.09
        a.plot([P[0], mx - ux * g], [P[1], my - uy * g], **K); a.plot([mx + ux * g, Q[0]], [my + uy * g, Q[1]], **K)
        for s in (-1, 1):
            cx, cy = mx + s * ux * g, my + s * uy * g
            a.plot([cx - nx * 0.3, cx + nx * 0.3], [cy - ny * 0.3, cy + ny * 0.3], color=NAVY, lw=3.2)
    cap(A, B); cap(B, C); cap(C, A)
    a.plot([A[0], A[0]], [A[1], ys[0]], color=C1, lw=2); dot(a, A[0], ys[0])
    a.plot([B[0], 4.6, 4.6], [B[1], B[1], ys[1]], color=C2, lw=2); dot(a, 4.6, ys[1])
    a.plot([C[0], 1.2, 1.2], [C[1], C[1], ys[2]], color=C3, lw=2); dot(a, 1.2, ys[2])
    for P in (A, B, C): dot(a, *P)
    a.text(5.0, 0.2, "batterie de\ncompensation\ncouplée en Δ", fontsize=10, color=BLUE, fontweight="bold")
    a.set_xlim(-0.3, 7.3); a.set_ylim(-1.3, 3.0)
    save(fig, path)


# ------------------------------------------------------------------ 10. plaque signalétique moteur
def plaque_signal(path):
    fig, a = plt.subplots(figsize=(4.8, 2.5)); a.axis("off")
    a.add_patch(Rectangle((0, 0), 4.8, 2.5, fc="#E9ECEF", ec=NAVY, lw=2.2))
    for x, y in ((0.15, 0.15), (4.65, 0.15), (0.15, 2.35), (4.65, 2.35)): a.add_patch(Circle((x, y), 0.07, fc="#B0B6BE", ec=NAVY, lw=0.8))
    L = [("3~ Mot.", "IEC 60034", True), ("4,0 kW", "S1", True), ("230 Δ / 400 Y V", "50 Hz", True),
         ("14,2 / 8,2 A", "cos φ 0,82", True), ("1440 min⁻¹", "IP55 · Th. Cl. F", False), ("η 86 %", "IE3", False)]
    for i, (l, r, b) in enumerate(L):
        y = 2.1 - i * 0.33
        a.text(0.35, y, l, fontsize=11.5, fontweight="bold" if b else "normal", color=NAVY, family="DejaVu Sans Mono", va="center")
        a.text(4.45, y, r, fontsize=10.5, color=NAVY, family="DejaVu Sans Mono", va="center", ha="right")
    a.set_xlim(-0.05, 4.85); a.set_ylim(-0.05, 2.55)
    save(fig, path)


if __name__ == "__main__":
    systeme("fig_systeme.png"); tensions("fig_tensions.png")
    fig, a = plt.subplots(figsize=(5.4, 3.9)); a.set_aspect("equal"); a.axis("off"); _etoile_draw(a, True, True); save(fig, "fig_etoile.png")
    fig, a = plt.subplots(figsize=(5.4, 3.9)); a.set_aspect("equal"); a.axis("off"); _etoile_draw(a, False, True); save(fig, "fig_etoile_sansN.png")
    triangle("fig_triangle.png")
    plaque("fig_plaque_Y.png", "Y"); plaque("fig_plaque_D.png", "D")
    plaque("fig_plaque_vide.png", "Y", vide=True); plaque("fig_plaque_Y_corr.png", "Y_corr"); plaque("fig_plaque_D_corr.png", "D_corr")
    neutre_vect("fig_IN_demo.png", (10, 6, 4), corr=True)
    neutre_vect("fig_IN_ex_corr.png", (10, 6, 4), corr=True); neutre_vect("fig_IN_ex.png", (10, 6, 4), grid_only=True)
    neutre_coupe("fig_neutre_coupe.png", "800 W", "3000 W", "plaque", "radiateur")
    neutre_coupe("fig_neutre_ex.png", "2000 W", "100 W", "radiateur", "lampe")
    deux_wattmetres("fig_2w.png"); compensation("fig_comp.png"); plaque_signal("fig_plaque_moteur.png")
    print("figures ok")
