# -*- coding: utf-8 -*-
"""Figures du cours « Conversion analogique-numérique (CAN) et numérique-analogique (CNA) ».
Symboles selon CEI 60617-13 (convertisseurs : rectangle + symbole distinctif « ∩/# » pour CAN, « #/∩ » pour CNA ;
∩ = grandeur analogique, # = grandeur numérique) et CEI 60617-2/-4 (masse, résistance rectangulaire).
Couleurs ETML : marine 242852, bleu 297FD5, bleu clair ACCBF9."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon
import numpy as np

plt.rcParams["font.family"] = "Liberation Sans"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Liberation Sans"
plt.rcParams["mathtext.it"] = "Liberation Sans:italic"
NAVY, BLUE, LBLUE, TINT, GREY, RED = "#242852", "#297FD5", "#ACCBF9", "#E8EFFB", "#5A6478", "#EE0000"
K = "black"
DPI = 220


def save(fig, name):
    fig.savefig(name, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def arrow(ax, x0, y0, x1, y1, c=K, lw=1.6):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=14, color=c, lw=lw))


def block(ax, x, y, w, h, title, sub=None, fc="white", ec=K, fs=12, sym=None):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.6))
    if sym:  # symbole distinctif CEI en haut du rectangle
        ax.text(x + w / 2, y + h * 0.66, sym, ha="center", va="center", fontsize=fs + 5, color=K)
        ax.text(x + w / 2, y + h * 0.24, title, ha="center", va="center", fontsize=fs - 1, color=NAVY, fontweight="bold")
    else:
        ax.text(x + w / 2, y + h * (0.6 if sub else 0.5), title, ha="center", va="center", fontsize=fs, color=NAVY, fontweight="bold")
        if sub:
            ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center", fontsize=fs - 3, color=GREY)


# ---------------------------------------------------------------- 1. chaîne d'acquisition et de commande
def fig_chaine():
    fig, ax = plt.subplots(figsize=(11, 3.3)); ax.axis("off"); ax.set_aspect("equal")
    y, h = 1.0, 1.4
    B = [(0.0, 1.7, "Capteur", "température,\nson, lumière"),
         (2.3, 1.7, "Adaptation", "amplifier,\nfiltrer"),
         (4.6, 1.5, "CAN", None),
         (6.7, 1.7, "Micro-\ncontrôleur", None),
         (9.0, 1.5, "CNA", None),
         (11.1, 1.7, "Actionneur", "haut-parleur,\nmoteur")]
    for x, w, t, s in B:
        if t == "CAN":
            block(ax, x, y, w, h, "CAN", sym="∩/#", fc=TINT)
        elif t == "CNA":
            block(ax, x, y, w, h, "CNA", sym="#/∩", fc=TINT)
        else:
            block(ax, x, y, w, h, t, s)
    for i in range(len(B) - 1):
        x0 = B[i][0] + B[i][1]; x1 = B[i + 1][0]
        arrow(ax, x0 + 0.05, y + h / 2, x1 - 0.05, y + h / 2)
    # étiquettes analogique / numérique
    ax.add_patch(Rectangle((-0.15, 2.75), 5.45, 0.42, fc=LBLUE, ec="none"))
    ax.text(2.57, 2.96, "monde analogique (∩) : tension continue", ha="center", va="center", fontsize=11, color=NAVY)
    ax.add_patch(Rectangle((5.35, 2.75), 4.4, 0.42, fc=NAVY, ec="none"))
    ax.text(7.55, 2.96, "monde numérique (#) : nombres binaires", ha="center", va="center", fontsize=11, color="white")
    ax.add_patch(Rectangle((9.8, 2.75), 3.15, 0.42, fc=LBLUE, ec="none"))
    ax.text(11.37, 2.96, "analogique (∩)", ha="center", va="center", fontsize=11, color=NAVY)
    for xm, t, mono in ((4.3, "1,72 V", False), (6.4, "0110 1101b", True), (8.7, "1001 0010b", True), (10.8, "2,86 V", False)):
        ax.text(xm, 0.6, t, ha="center", fontsize=10.5, color=BLUE, family=("Liberation Mono" if mono else "Liberation Sans"))
    ax.set_xlim(-0.3, 13.0); ax.set_ylim(0.3, 3.3)
    save(fig, "fig_chaine.png")


# ---------------------------------------------------------------- 2. analogique → échantillonné → numérique
def fig_signal():
    t = np.linspace(0, 1, 600)
    u = 2.5 + 1.8 * np.sin(2 * np.pi * t) + 0.5 * np.sin(6 * np.pi * t)
    ts = np.arange(0, 1.0001, 1 / 16)
    us = 2.5 + 1.8 * np.sin(2 * np.pi * ts) + 0.5 * np.sin(6 * np.pi * ts)
    q = 5 / 8
    N = np.floor(us / q).clip(0, 7)
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.4), sharey=True)
    for ax in axs:
        ax.set_ylim(0, 5.2); ax.set_xlim(0, 1)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_xticks([]); ax.set_xlabel("t", fontsize=12, style="italic", loc="right")
    axs[0].plot(t, u, color=NAVY, lw=2.2)
    axs[0].set_title("1. Signal analogique\ninfinité de valeurs, à chaque instant", fontsize=11, color=NAVY)
    axs[0].set_ylabel("u (V)", fontsize=12)
    axs[1].plot(t, u, color=LBLUE, lw=1.6)
    axs[1].vlines(ts, 0, us, color=BLUE, lw=1.2)
    axs[1].plot(ts, us, "o", color=NAVY, ms=5)
    axs[1].set_title("2. Échantillonnage\non mesure à intervalles réguliers $T_\mathrm{e}$", fontsize=11, color=NAVY)
    axs[2].plot(t, u, color=LBLUE, lw=1.4)
    for k in range(9):
        axs[2].axhline(k * q, color="#d5dbe6", lw=0.7, zorder=0)
    axs[2].step(ts, N * q, where="post", color=NAVY, lw=2.0)
    axs[2].plot(ts, N * q, "s", color=NAVY, ms=4)
    for x, n in zip(ts[::4], N[::4]):
        axs[2].text(x + 0.01, n * q + 0.12, format(int(n), "03b"), fontsize=8.5, color=BLUE, family="Liberation Mono")
    axs[2].set_title("3. Quantification\nchaque mesure devient un code (ici 3 bits)", fontsize=11, color=NAVY)
    fig.tight_layout()
    save(fig, "fig_signal.png")


# ---------------------------------------------------------------- 3. escalier de conversion CAN 3 bits
def fig_escalier(uref=8.0, n=3, name="fig_escalier.png", ue_mark=None):
    q = uref / 2 ** n
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    xs = np.linspace(0, uref, 2000)
    N = np.floor(xs / q).clip(0, 2 ** n - 1)
    ax.step(xs, N, where="post", color=NAVY, lw=2.4)
    ax.plot([0, uref], [0, 2 ** n], color=BLUE, lw=1.0, ls="--")
    ax.set_xticks(np.arange(0, uref + 0.01, q)); ax.set_xticklabels([f"{v:g}" for v in np.arange(0, uref + 0.01, q)], fontsize=10)
    ax.set_yticks(range(2 ** n)); ax.set_yticklabels([format(k, f"0{n}b") + "b" for k in range(2 ** n)], fontsize=10, family="Liberation Mono")
    ax.set_xlabel("Tension d'entrée $U_\mathrm{e}$ (V)", fontsize=12); ax.set_ylabel("Code de sortie N", fontsize=12)
    ax.grid(color="#e1e6ef", lw=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(0, uref); ax.set_ylim(-0.3, 2 ** n)
    # quantum
    ax.annotate("", xy=(3 * q, 1.5), xytext=(2 * q, 1.5), arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=1.5))
    ax.text(2.5 * q, 1.18, "q = 1 LSB", ha="center", fontsize=11, color=RED, fontweight="bold")
    if ue_mark is not None:
        nm = int(np.floor(ue_mark / q))
        ax.plot([ue_mark, ue_mark], [-0.3, nm], color=BLUE, lw=1.4, ls=":")
        ax.plot([0, ue_mark], [nm, nm], color=BLUE, lw=1.4, ls=":")
        ax.plot(ue_mark, nm, "o", color=BLUE, ms=7)
        ax.text(ue_mark + 0.1, nm - 0.55, "$U_\\mathrm{e}$" + f" = {ue_mark:g} V → N = {format(nm, f'0{n}b')}b", fontsize=10.5, color=BLUE)
    save(fig, name)


# ---------------------------------------------------------------- 4. échantillonnage : assez vite / trop lent
def fig_shannon():
    t = np.linspace(0, 1, 1000)
    f = 5
    u = np.sin(2 * np.pi * f * t)
    fig, axs = plt.subplots(1, 2, figsize=(12, 3.2), sharey=True)
    for ax, fe, ttl, good in ((axs[0], 40, "$f_\mathrm{e}$ = 40 Hz  > 2 × 5 Hz : la forme est retrouvée", True),
                               (axs[1], 6, "$f_\mathrm{e}$ = 6 Hz  < 2 × 5 Hz : on « voit » un faux signal lent", False)):
        ts = np.arange(0, 1.0001, 1 / fe)
        us = np.sin(2 * np.pi * f * ts)
        ax.plot(t, u, color=LBLUE, lw=2)
        ax.plot(ts, us, "o", color=NAVY, ms=6, zorder=3)
        if good:
            ax.plot(ts, us, color=NAVY, lw=1.4)
        else:
            ax.plot(t, np.sin(2 * np.pi * (f - fe) * t), color=RED, lw=2, ls="--")
        ax.set_title(ttl, fontsize=11.5, color=NAVY if good else RED)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 1)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_xlabel("t (signal réel de 5 Hz en bleu clair)", fontsize=10, color=GREY)
    fig.tight_layout()
    save(fig, "fig_shannon.png")


# ---------------------------------------------------------------- 5. approximations successives (4 bits, Uref 5 V, Ue 3,3 V)
def fig_sar(uref=5.0, ue=3.3, n=4, name="fig_sar.png"):
    q = uref / 2 ** n
    code = 0; steps = []
    for k in range(n - 1, -1, -1):
        test = code | (1 << k)
        keep = test * q <= ue
        steps.append((test, test * q, keep))
        if keep: code = test
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    for i, (test, ut, keep) in enumerate(steps):
        ax.bar(i, ut, width=0.55, color=(NAVY if keep else "white"), ec=NAVY, lw=1.6, hatch=None if keep else "//")
        ax.text(i, ut - (0.4 if keep else 0.8), format(test, f"0{n}b"), ha="center", fontsize=12, fontweight="bold", family="Liberation Mono",
                color=("white" if keep else NAVY), bbox=(None if keep else dict(fc="white", ec="none", pad=1)))
        ax.text(i, ut - (0.85 if keep else 1.25), f"{ut:.4g} V".replace(".", ","), ha="center", fontsize=10, color=("white" if keep else GREY),
                bbox=(None if keep else dict(fc="white", ec="none", pad=1)))
        ax.text(i, -0.55, ("≤ $U_\mathrm{e}$ → garder 1" if keep else "> $U_\mathrm{e}$ → remettre 0"), ha="center", fontsize=10,
                color=(BLUE if keep else RED))
        ax.text(i, -0.95, f"essai {i + 1}", ha="center", fontsize=10, color=GREY)
    ax.axhline(ue, color=RED, lw=2, ls="--")
    ax.text(-0.55, ue + 0.1, ("$U_\\mathrm{e}$" + f" = {ue:g} V").replace(".", ","), color=RED, fontsize=12, fontweight="bold", ha="left")
    ax.set_ylim(-1.15, uref + 0.2); ax.set_xlim(-0.6, n - 0.4)
    ax.set_xticks([]); ax.set_ylabel("Tension d'essai (V)", fontsize=11)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.axhline(0, color=K, lw=0.8)
    save(fig, name)
    return code


# ---------------------------------------------------------------- 6. CNA : compteur → escalier (4 bits, Uref 3,2 V)
def fig_cna(uref=3.2, n=4, name="fig_cna.png", blank=False):
    q = uref / 2 ** n
    codes = list(range(2 ** n))
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    if not blank:
        ax.step(range(2 ** n + 1), [c * q for c in codes] + [codes[-1] * q], where="post", color=NAVY, lw=2.4)
    ax.set_xticks([c + 0.5 for c in codes])
    ax.set_xticklabels([format(c, f"0{n}b") for c in codes], rotation=90, fontsize=9, family="Liberation Mono")
    ax.set_yticks(np.arange(0, uref + 0.001, q * 2))
    ax.set_yticklabels([f"{v:.1f}".replace(".", ",") for v in np.arange(0, uref + 0.001, q * 2)], fontsize=10)
    ax.set_xlim(0, 2 ** n); ax.set_ylim(0, uref)
    ax.grid(color="#d5dbe6", lw=0.7)
    ax.set_xlabel("Code d'entrée N (un nouveau code toutes les 1 ms)", fontsize=11)
    ax.set_ylabel("$U_\mathrm{s}$ (V)", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    if not blank:
        ax.annotate("", xy=(9, 9 * q), xytext=(9, 8 * q), arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=1.4))
        ax.text(9.25, 8.3 * q, "q = 0,2 V", color=RED, fontsize=10.5, fontweight="bold")
        ax.text(14.9, 15 * q - 0.12, "3,0 V = $U_\mathrm{ref}$ − q", ha="right", fontsize=10, color=BLUE)
    save(fig, name)


# ---------------------------------------------------------------- 7. symboles CEI 60617-13
def fig_symboles():
    fig, ax = plt.subplots(figsize=(10, 3.0)); ax.axis("off"); ax.set_aspect("equal")
    def conv(x, sym, lab, inlab, outlab, bus_in, bus_out):
        ax.add_patch(Rectangle((x, 0.6), 1.6, 1.6, fc="white", ec=K, lw=1.8))
        ax.text(x + 0.8, 1.72, sym, ha="center", va="center", fontsize=19)
        # entrée
        ax.plot([x - 0.9, x], [1.4, 1.4], color=K, lw=1.8)
        ax.plot([x + 1.6, x + 2.5], [1.4, 1.4], color=K, lw=(4.0 if bus_out else 1.8))
        if bus_in:
            ax.plot([x - 0.9, x], [1.4, 1.4], color=K, lw=4.0)
        if bus_out or bus_in:
            xs = x + 2.05 if bus_out else x - 0.45
            ax.plot([xs - 0.12, xs + 0.12], [1.22, 1.58], color=K, lw=1.4)
            ax.text(xs + 0.05, 1.68, "n", fontsize=11, style="italic")
        ax.text(x - 0.95, 1.55, inlab, ha="left", fontsize=11, color=BLUE, style="italic")
        ax.text(x + 2.5, 1.55, outlab, ha="right", fontsize=11, color=BLUE, style="italic")
        ax.text(x + 0.8, 0.22, lab, ha="center", fontsize=12, color=NAVY, fontweight="bold")
    conv(1.0, "∩/#", "CAN (ADC)", "$U_\mathrm{e}$", "N", False, True)
    conv(5.6, "#/∩", "CNA (DAC)", "N", "$U_\mathrm{s}$", True, False)
    ax.set_xlim(-0.2, 9.0); ax.set_ylim(0, 2.5)
    save(fig, "fig_symboles.png")


# ---------------------------------------------------------------- 8. application LM35 → CAN 10 bits
def fig_lm35():
    fig, ax = plt.subplots(figsize=(11, 3.0)); ax.axis("off"); ax.set_aspect("equal")
    y, h = 0.9, 1.4
    block(ax, 0.0, y, 2.1, h, "LM35", "10 mV / °C")
    block(ax, 3.1, y, 1.6, h, "CAN", sym="∩/#", fc=TINT)
    block(ax, 5.8, y, 2.2, h, "Calcul", "N × q ÷ 10 mV")
    block(ax, 9.0, y, 2.0, h, "Affichage", None)
    ax.text(10.0, y + 0.42, "24,9 °C", ha="center", fontsize=13, family="Liberation Mono", color=BLUE, fontweight="bold")
    for x0, x1 in ((2.1, 3.1), (4.7, 5.8), (8.0, 9.0)):
        arrow(ax, x0 + 0.05, y + h / 2, x1 - 0.05, y + h / 2)
    ax.text(2.6, y + h / 2 + 0.2, "0,250 V", ha="center", fontsize=10.5, color=BLUE)
    ax.text(5.25, y + h / 2 + 0.2, "N = 51", ha="center", fontsize=10.5, color=BLUE)
    ax.text(8.5, y + h / 2 + 0.2, "249 mV", ha="center", fontsize=10.5, color=BLUE)
    ax.text(1.05, 2.55, "25,0 °C réels", ha="center", fontsize=11, color=NAVY, fontweight="bold")
    ax.text(3.9, 0.45, "10 bits · $U_\mathrm{ref}$ = 5 V · q = 4,88 mV", ha="center", fontsize=10, color=GREY)
    ax.set_xlim(-0.2, 11.2); ax.set_ylim(0.2, 2.8)
    save(fig, "fig_lm35.png")


if __name__ == "__main__":
    fig_chaine(); fig_signal(); fig_escalier(); fig_escalier(name="fig_escalier_ex.png", ue_mark=5.5)
    fig_shannon(); fig_sar(); fig_cna(); fig_cna(name="fig_cna_vierge.png", blank=True)
    fig_symboles(); fig_lm35()
    print("figures ok")
