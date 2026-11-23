# -*- coding: utf-8 -*-
"""Figures du cours « Arithmétique binaire, code Gray, compléments » — symboles logiques CEI 60617-12
(rectangle + symbole distinctif : « 1 » inverseur, « =1 » OU exclusif, cercle = négation)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge, Polygon
import numpy as np

plt.rcParams["font.family"] = "Liberation Sans"
K = "black"
G = "#8c8c8c"
DPI = 220


def save(fig, name):
    fig.savefig(name, dpi=DPI, transparent=False, facecolor="white", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


# ---------------------------------------------------------------- logo (wordmark ETML)
def logo():
    fig = plt.figure(figsize=(4.0, 1.0))
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 4); ax.set_ylim(0, 1)
    ax.text(0.02, 0.5, "ETML", fontsize=58, fontweight="bold", va="center", ha="left", color=K)
    ax.add_patch(Rectangle((2.78, 0.16), 0.05, 0.68, color=K))
    ax.text(2.92, 0.64, "École technique", fontsize=11, va="center", color=K)
    ax.text(2.92, 0.36, "École des métiers Lausanne", fontsize=11, va="center", color=K)
    fig.savefig("logo.png", dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


# ---------------------------------------------------------------- portes CEI
def gate(ax, x, y, w, h, sym, neg_out=False, ins=(), out=True, lw=1.6, fs=13):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=K, lw=lw))
    ax.text(x + w / 2, y + h * 0.72, sym, ha="center", va="center", fontsize=fs, color=K)
    r = 0.07
    if out:
        yo = y + h / 2
        if neg_out:
            ax.add_patch(Circle((x + w + r, yo), r, fill=False, ec=K, lw=lw))
            return (x + w + 2 * r, yo)
        return (x + w, yo)


def line(ax, pts, lw=1.6, c=K):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round")


def dot(ax, x, y):
    ax.add_patch(Circle((x, y), 0.045, color=K))


def fig_inverseurs():
    """Complément à 1 : 8 inverseurs CEI en parallèle (exemple 0010 1101b → 1101 0010b)."""
    a = "00101101"
    fig, ax = plt.subplots(figsize=(8.2, 3.2)); ax.axis("off"); ax.set_aspect("equal")
    for i, b in enumerate(a):
        x = i * 1.0
        ax.text(x + 0.3, 3.05, b, ha="center", fontsize=16, fontweight="bold")
        line(ax, [(x + 0.3, 2.95), (x + 0.3, 2.4)])
        ax.add_patch(Rectangle((x, 1.5), 0.6, 0.9, fill=False, ec=K, lw=1.6))
        ax.text(x + 0.3, 2.15, "1", ha="center", va="center", fontsize=13)
        ax.add_patch(Circle((x + 0.3, 1.43), 0.07, fill=False, ec=K, lw=1.6))
        line(ax, [(x + 0.3, 1.36), (x + 0.3, 0.85)])
        ax.text(x + 0.3, 0.45, str(1 - int(b)), ha="center", fontsize=16, fontweight="bold")
    ax.text(-0.55, 3.15, "A", fontsize=14, ha="right", style="italic")
    ax.text(-0.55, 0.55, "C1", fontsize=14, ha="right", style="italic")
    ax.text(0.3, 3.55, "MSB", ha="center", fontsize=10, color=G)
    ax.text(7.3, 3.55, "LSB", ha="center", fontsize=10, color=G)
    ax.set_xlim(-1.1, 8.0); ax.set_ylim(0.2, 3.8)
    save(fig, "fig_inverseurs.png")


def fig_gray_xor():
    """Binaire → Gray avec 3 portes OU exclusif CEI « =1 » (exemple 1011b → 1110)."""
    b = [1, 0, 1, 1]
    g = [b[0]] + [b[i] ^ b[i + 1] for i in range(3)]
    fig, ax = plt.subplots(figsize=(7.6, 4.2)); ax.axis("off"); ax.set_aspect("equal")
    ys = [3.6, 2.6, 1.6, 0.6]
    labels = ["b3", "b2", "b1", "b0"]
    xin = 0.6
    for i, y in enumerate(ys):
        ax.text(0.0, y, f"{labels[i][0]}", ha="right", va="center", fontsize=14, style="italic")
        ax.text(0.03, y - 0.12, labels[i][1], ha="left", va="center", fontsize=9, style="italic")
        ax.text(0.45, y + 0.22, str(b[i]), ha="center", fontsize=13, fontweight="bold")
    # g3 = b3
    line(ax, [(0.3, ys[0]), (5.6, ys[0])])
    # portes : entre lignes i et i+1, sortie au niveau de la ligne i+1
    gx = 3.2
    for k in range(3):
        yt, yb = ys[k], ys[k + 1]
        yg = yb  # sortie alignée sur la ligne i+1
        gy = yg - 0.45
        # entrée 1 : dérivation de la ligne du dessus
        xd = 1.3 + 0.55 * k
        dot(ax, xd, yt)
        line(ax, [(xd, yt), (xd, gy + 0.68), (gx, gy + 0.68)])
        line(ax, [(0.3, yb), (gx, yb - 0.22)]) if False else line(ax, [(0.3, yb), (2.85, yb), (2.85, gy + 0.22), (gx, gy + 0.22)])
        gate(ax, gx, gy, 1.1, 0.9, "=1")
        line(ax, [(gx + 1.1, yg), (5.6, yg)])
    for i, y in enumerate(ys):
        ax.text(6.25, y, "g", ha="right", va="center", fontsize=14, style="italic")
        ax.text(6.28, y - 0.12, labels[i][1], ha="left", va="center", fontsize=9, style="italic")
        ax.text(5.35, y + 0.22, str(g[i]), ha="center", fontsize=13, fontweight="bold")
    ax.text(0.2, 4.25, "Binaire", fontsize=12, color=G)
    ax.text(5.4, 4.25, "Gray", fontsize=12, color=G)
    ax.set_xlim(-0.6, 6.8); ax.set_ylim(0.0, 4.5)
    save(fig, "fig_gray_xor.png")


def fig_decalage():
    """× 2 = décalage d'un rang vers la gauche (22d → 44d → 88d)."""
    vals = [22, 44, 88]
    fig, ax = plt.subplots(figsize=(8.4, 3.6)); ax.axis("off"); ax.set_aspect("equal")
    W8 = [128, 64, 32, 16, 8, 4, 2, 1]
    for j, w in enumerate(W8):
        ax.text(j * 0.75 + 0.375, 3.65, str(w), ha="center", fontsize=10, color=G)
    for r, v in enumerate(vals):
        y = 2.7 - r * 1.15
        s = format(v, "08b")
        for j, c in enumerate(s):
            ax.add_patch(Rectangle((j * 0.75, y), 0.75, 0.7, fill=(c == "1"), fc="#ACCBF9", ec=K, lw=1.3))
            ax.text(j * 0.75 + 0.375, y + 0.35, c, ha="center", va="center", fontsize=15, fontweight="bold")
        ax.text(6.25, y + 0.35, f"= {v}d", va="center", fontsize=14)
        if r < 2:
            ax.annotate("", xy=(5.3, y - 0.42), xytext=(6.0, y - 0.1),
                        arrowprops=dict(arrowstyle="-|>", color=K, lw=1.4, connectionstyle="arc3,rad=-0.25"))
            ax.text(6.15, y - 0.32, "× 2 : tout se décale d'un rang à gauche, un 0 entre à droite", fontsize=10, va="center")
    ax.set_xlim(-0.1, 12.6); ax.set_ylim(0.2, 3.9)
    save(fig, "fig_decalage.png")


def disk(ax, codes, title):
    """Disque codeur 3 pistes, 8 secteurs : piste intérieure = MSB."""
    radii = [(0.35, 0.6), (0.6, 0.85), (0.85, 1.1)]  # MSB intérieur ... LSB extérieur
    for s, code in enumerate(codes):
        a0 = 90 - s * 45 - 45; a1 = 90 - s * 45
        for t, (r0, r1) in enumerate(radii):
            bit = code[t]
            ax.add_patch(Wedge((0, 0), r1, a0, a1, width=r1 - r0, fc=("#242852" if bit == "1" else "white"), ec=K, lw=1.0))
        am = np.radians((a0 + a1) / 2)
        ax.text(1.3 * np.cos(am), 1.3 * np.sin(am), code, ha="center", va="center", fontsize=11, fontweight="bold")
    ax.add_patch(Circle((0, 0), 0.12, color=K))
    ax.set_title(title, fontsize=13, pad=4)
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.set_aspect("equal"); ax.axis("off")


def fig_disques():
    binc = [format(i, "03b") for i in range(8)]
    gray = [format(i ^ (i >> 1), "03b") for i in range(8)]
    fig, axs = plt.subplots(1, 2, figsize=(8.0, 4.0))
    disk(axs[0], binc, "Binaire naturel")
    disk(axs[1], gray, "Code Gray")
    save(fig, "fig_disques.png")


def fig_disque_vierge():
    """Pour l'exercice : disque Gray 3 pistes à colorier (secteurs vides)."""
    fig, ax = plt.subplots(figsize=(3.6, 3.6))
    radii = [(0.35, 0.6), (0.6, 0.85), (0.85, 1.1)]
    for s in range(8):
        a0 = 90 - s * 45 - 45; a1 = 90 - s * 45
        for (r0, r1) in radii:
            ax.add_patch(Wedge((0, 0), r1, a0, a1, width=r1 - r0, fc="white", ec=K, lw=1.0))
        am = np.radians((a0 + a1) / 2)
        ax.text(1.28 * np.cos(am), 1.28 * np.sin(am), str(s), ha="center", va="center", fontsize=11)
    ax.add_patch(Circle((0, 0), 0.12, color=K))
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_aspect("equal"); ax.axis("off")
    save(fig, "fig_disque_vierge.png")


def fig_disque_corr():
    fig, ax = plt.subplots(figsize=(3.6, 3.6))
    disk(ax, [format(i ^ (i >> 1), "03b") for i in range(8)], "")
    save(fig, "fig_disque_corr.png")


if __name__ == "__main__":
    logo(); fig_inverseurs(); fig_gray_xor(); fig_decalage(); fig_disques(); fig_disque_vierge(); fig_disque_corr()
    print("figures ok")


def fig_quadrature():
    """Codeur incrémental (bouton rotatif) : 2 voies A et B décalées d'un quart de période → suite Gray 00 01 11 10."""
    fig, ax = plt.subplots(figsize=(8.0, 3.0)); ax.axis("off")
    states = ["00", "01", "11", "10", "00", "01", "11", "10"]
    A = [int(s[0]) for s in states]; B = [int(s[1]) for s in states]
    def wave(y0, v, lab):
        xs, ys = [0], [y0 + v[0] * 0.8]
        for i, b in enumerate(v):
            xs += [i, i + 1]; ys += [y0 + b * 0.8, y0 + b * 0.8]
        ax.step(range(len(v) + 1), [y0 + x * 0.8 for x in v] + [y0 + v[-1] * 0.8], where="post", color="#242852", lw=2.4)
        ax.text(-0.25, y0 + 0.4, lab, ha="right", va="center", fontsize=14, fontweight="bold", color="#242852")
    wave(2.0, A, "A"); wave(0.8, B, "B")
    for i, s in enumerate(states):
        ax.add_patch(Rectangle((i + 0.08, -0.35), 0.84, 0.6, fc="#ACCBF9" if i < 4 else "white", ec="#297FD5", lw=1.2))
        ax.text(i + 0.5, -0.05, s, ha="center", va="center", fontsize=13, fontweight="bold", family="Liberation Mono")
        ax.plot([i, i], [-0.4, 3.0], color="#c8cfdb", lw=0.8, ls=":")
    ax.annotate("", xy=(7.9, 3.15), xytext=(0.1, 3.15), arrowprops=dict(arrowstyle="-|>", color="#297FD5", lw=1.8))
    ax.text(4.0, 3.35, "on tourne le bouton dans le sens horaire", ha="center", fontsize=11, color="#297FD5")
    ax.text(4.0, -0.75, "A B lus à chaque cran : 00 → 01 → 11 → 10 → 00 … = code Gray à 2 bits (un seul bit change)", ha="center", fontsize=10.5, color="#5A6478")
    ax.set_xlim(-0.8, 8.1); ax.set_ylim(-1.0, 3.6)
    save(fig, "fig_quadrature.png")


if __name__ == "__main__":
    fig_quadrature()
