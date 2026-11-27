# -*- coding: utf-8 -*-
"""Symboles et figures normalisés (CEI 60617), en PNG via matplotlib, aux couleurs ETML (REGLES 3.3) :
portes logiques (CEI 60617-12 : rectangle + qualificatif, cercle de négation), équations en notation du Floyd,
résistance, source de tension, alimentation (+5 V), masse (GND), terre, nœuds, fils avec sauts de fil, flèches de tension
(du + vers le −) et de courant (CEI 60617-2 et -4),
chronogrammes, contact à fermeture (CEI 60617-7), brochage DIP 14.
Les figures propres à une séance sont dans contenus/<matière>/<semaine>/figures.py et utilisent ces briques.
ecrire_dans(dossier) fixe le dossier où save() écrit les images."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
from moteur import logique as L

plt.rcParams["font.family"] = "Liberation Sans"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Liberation Sans"
plt.rcParams["mathtext.it"] = "Liberation Sans:italic"
plt.rcParams["mathtext.bf"] = "Liberation Sans:bold"
K, NAVY, BLUE, LBLUE, TINT, RED, GR = "black", "#242852", "#297FD5", "#ACCBF9", "#E8EFFB", "#EE0000", "#5A6478"
DPI = 220
_DOSSIER = "."


AVERTISSEMENTS = "avertissements_figures.txt"     # lu par controle/controler.py
TAILLES = "tailles_figures.json"                 # {figure : [largeur enregistrée en pouces, plus petit corps en pt, texte]}
KARNAUGH = "karnaugh_figures.json"               # géométrie des tableaux de Karnaugh, lue par controle/karnaugh.py (REGLES 3.5)


def ecrire_dans(dossier):
    global _DOSSIER
    os.makedirs(dossier, exist_ok=True)
    _DOSSIER = dossier
    open(os.path.join(dossier, AVERTISSEMENTS), "w", encoding="utf-8").close()
    open(os.path.join(dossier, TAILLES), "w", encoding="utf-8").write("{}")
    open(os.path.join(dossier, KARNAUGH), "w", encoding="utf-8").write("{}")


def textes_sur_courbes(fig):
    """Textes posés sur une courbe ou un trait de repère, dans les graphiques (axes visibles).
    Le contrôle de la présentation et des fiches ne voit pas l'intérieur des images : on vérifie ici, à l'enregistrement."""
    import numpy as np
    r = fig.canvas.get_renderer()
    out = []
    for ax in fig.axes:
        if not ax.axison:
            continue                                   # schémas : textes et fils sont placés à la main
        for t in ax.texts:
            if not t.get_visible() or not t.get_text().strip():
                continue
            bb = t.get_window_extent(r).expanded(1.0, 1.0)
            x0, y0, x1, y1 = bb.x0 + 1, bb.y0 + 1, bb.x1 - 1, bb.y1 - 1
            for ln in ax.lines:
                if not ln.get_visible() or ln.get_linewidth() < 1.0:
                    continue
                xy = ln.get_transform().transform(np.column_stack(ln.get_data()).astype(float))
                pts = [xy[0]]
                for a, b in zip(xy[:-1], xy[1:]):            # segments échantillonnés tous les ~2 px
                    n = max(1, int(np.hypot(*(b - a)) / 2))
                    pts += [a + (b - a) * k / n for k in range(1, n + 1)]
                if any(x0 < px < x1 and y0 < py < y1 for px, py in pts):
                    out.append(f"texte « {t.get_text().strip()[:40]} » posé sur une courbe ou un trait")
                    break
    from matplotlib.text import Annotation
    for ax in fig.axes:                                 # texte sur la pointe d'une flèche (annotate) : graphiques et schémas
        fl = [a.arrow_patch for a in ax.texts if isinstance(a, Annotation) and a.arrow_patch is not None]
        for t in [t for t in ax.texts if t.get_visible() and t.get_text().strip()]:
            bt = t.get_window_extent(r)
            y0, y1 = bt.y0 + 0.1 * bt.height, bt.y1 - 0.1 * bt.height      # sans l'interligne
            for f in fl:
                bf = f.get_window_extent(r)                  # le tracé d'une flèche est déjà en coordonnées écran
                if min(bt.x1, bf.x1) - max(bt.x0, bf.x0) > 1 and min(y1, bf.y1) - max(y0, bf.y0) > 0:
                    out.append(f"texte « {t.get_text().strip()[:40]} » posé sur une flèche")
                    break
    for ax in fig.axes:                                 # deux textes qui se chevauchent : graphiques et schémas
        ts = [t for t in ax.texts if t.get_visible() and t.get_text().strip()]
        bb = [t.get_window_extent(r) for t in ts]
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                a, b = bb[i], bb[j]
                lx = min(a.x1, b.x1) - max(a.x0, b.x0); ly = min(a.y1, b.y1) - max(a.y0, b.y0)
                # les boîtes incluent l'interligne : deux lignes serrées mais lisibles se recouvrent de ≈ 15 % ;
                # au-delà de 20 % de la plus petite hauteur, les lettres se touchent (étalonné sur R_1 / 1k et Cu / +1)
                if lx > 2 and ly > 0.2 * min(a.height, b.height):
                    out.append(f"textes « {ts[i].get_text().strip()[:25]} » et « {ts[j].get_text().strip()[:25]} » se chevauchent")
    return out


def plus_petit_texte(fig):
    """Plus petit corps (pt, à la taille de la figure) parmi les textes visibles : textes posés, graduations, titres d'axes."""
    ts = list(fig.texts)
    for ax in fig.axes:
        ts += list(ax.texts) + [ax.title, ax.xaxis.label, ax.yaxis.label]
        if ax.axison:
            ts += [t for t in ax.get_xticklabels() + ax.get_yticklabels()]
    ts = [t for t in ts if t.get_visible() and t.get_text().strip() and t.get_text().strip() not in ("+", "−", "-")]   # signes dans les porteurs : pictogrammes
    if not ts:
        return None, ""
    t = min(ts, key=lambda t: t.get_fontsize())
    return t.get_fontsize(), t.get_text().strip()[:30]


def save(fig, name, pad=0.05, fond="white"):
    import json
    fig.canvas.draw()
    av = textes_sur_courbes(fig)
    pt, quoi = plus_petit_texte(fig)
    if pt:
        larg = fig.get_tightbbox(fig.canvas.get_renderer()).width + 2 * pad      # largeur de l'image enregistrée [pouces]
        ft = os.path.join(_DOSSIER, TAILLES)
        d = json.load(open(ft, encoding="utf-8")) if os.path.exists(ft) else {}
        d[name] = [round(larg, 3), pt, quoi]
        json.dump(d, open(ft, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    if av:
        with open(os.path.join(_DOSSIER, AVERTISSEMENTS), "a", encoding="utf-8") as f:
            for a in av:
                f.write(f"{name} : {a}\n")
                print(f"⚠ figure {name} : {a}")
    # fond=None : image transparente (équations : l'équation éditable de PowerPoint n'a pas de fond, l'image de secours non plus)
    fig.savefig(os.path.join(_DOSSIER, name), dpi=DPI, facecolor=fond or "none", transparent=fond is None, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)


def line(ax, pts, lw=1.8, c=K, **kw):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round", **kw)


# ------------------------------------------------------------------ symbole CEI d'une porte
def gate_ax(ax, x, y, key, w=1.3, h=1.6, lw=2.0, fs=20, labels=("A", "B", "Y"), lab_fs=17, pin=0.55, dq=0.32):
    g = L.GATES[key]
    qual, neg, n = g[2], g[3], g[4]
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=K, lw=lw))
    ax.text(x + w / 2, y + h - dq, qual, ha="center", va="center", fontsize=fs, color=K)       # dq : qualificatif sous le bord haut
    ys = [y + h / 2] if n == 1 else [y + h * 0.72, y + h * 0.28]
    for i, yy in enumerate(ys):
        line(ax, [(x - pin, yy), (x, yy)], lw=lw)
        if labels:
            ax.text(x - pin - 0.08, yy, labels[i], ha="right", va="center", fontsize=lab_fs, style="italic")
    yo = y + h / 2; xo = x + w
    if neg:
        r = 0.12
        ax.add_patch(Circle((xo + r, yo), r, fill=False, ec=K, lw=lw)); xo += 2 * r
    line(ax, [(xo, yo), (xo + pin, yo)], lw=lw)
    if labels:
        ax.text(xo + pin + 0.08, yo, labels[-1], ha="left", va="center", fontsize=lab_fs, style="italic")


def fig_gate_mini(key, name=None, larg=0.62):
    """Symbole sans noms d'entrées, dessiné à sa taille d'emploi (larg en pouces) : qualificatif ≥ 8 pt dans un tableau."""
    fig = plt.figure(figsize=(larg, larg * 1.8 / 2.6)); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    gate_ax(ax, 0.55, 0.12, key, w=1.3, h=1.56, lw=1.1, fs=9.5, labels=None, pin=0.5, dq=0.5)
    ax.set_xlim(0, 2.6); ax.set_ylim(0, 1.8)
    save(fig, name or f"gate_{key}_mini.png", pad=0.0)


def fig_gate(key, name=None, labels=("A", "B", "Y")):
    """Symbole seul ; labels : entrées puis sortie (REGLES 3.4 : sortie S ; la semaine 1 de TM1 garde Y par défaut)."""
    fig, ax = plt.subplots(figsize=(3.2, 2.2)); ax.axis("off"); ax.set_aspect("equal")
    gate_ax(ax, 0.9, 0.2, key, labels=labels)
    ax.set_xlim(-0.05, 3.5); ax.set_ylim(0, 2.0)
    save(fig, name or f"gate_{key}.png")


# ------------------------------------------------------------------ équations (notation Floyd)
def fig_eq(key, color=NAVY, name=None, fs=30):
    fig = plt.figure(figsize=(4, 0.9)); fig.text(0.5, 0.5, "$" + L.GATES[key][6] + "$", ha="center", va="center", fontsize=fs, color=color)
    save(fig, name or f"eq_{key}.png", pad=0.08, fond=None)


def fig_eq_txt(tex, name, color=NAVY, fs=30):
    fig = plt.figure(figsize=(4, 0.9)); fig.text(0.5, 0.5, "$" + tex + "$", ha="center", va="center", fontsize=fs, color=color)
    save(fig, name, pad=0.08, fond=None)


# ------------------------------------------------------------------ chronogrammes
def chrono_fig(rows, name, n=8, ycol=BLUE, blank_last=False, highlight=None, width=7.6, numbers=True, last_label=None, ligne=0.95):
    """rows = [(nom, [bits] ou None)] ; la dernière ligne peut être vide (à compléter). ligne : hauteur d'une ligne (pouces)."""
    h = ligne * len(rows) + (0.45 if numbers else 0.1)
    fig, ax = plt.subplots(figsize=(width, h)); ax.axis("off")
    top = len(rows) * 1.0
    if highlight is not None:
        ax.add_patch(Rectangle((highlight, -0.25), 1, top + 0.15, fc=LBLUE, ec="none", alpha=0.55))
    for k in range(n + 1):
        ax.plot([k, k], [-0.25, top - 0.1], color="#b9c3d6", lw=0.9, ls=(0, (2, 3)))
    if numbers:
        for k in range(n):
            ax.text(k + 0.5, top + 0.02, str(k + 1), ha="center", va="bottom", fontsize=13, color=GR)
    for i, (lab, bits) in enumerate(rows):
        y0 = top - 1.0 - i * 1.0 + 0.1
        # corps choisis pour rester ≥ 8 pt (présentation) et ≥ 7 pt (fiche) une fois le chronogramme placé (REGLES 9.4)
        ax.text(-0.32, y0 + 0.3, lab, ha="right", va="center", fontsize=17, style="italic", color=NAVY)
        ax.text(-0.08, y0 + 0.62, "1", ha="right", va="center", fontsize=12.5, color=GR)
        ax.text(-0.08, y0 + 0.0, "0", ha="right", va="center", fontsize=12.5, color=GR)
        last = i == len(rows) - 1
        if bits is None:
            for lev in (0, 0.62):
                ax.plot([0, n], [y0 + lev, y0 + lev], color="#c8cfdb", lw=0.9, ls=(0, (1, 2)))
            continue
        col = ycol if (last and len(rows) > 1) else NAVY
        xs, ys = [], []
        for k, bt in enumerate(bits):
            xs += [k, k + 1]; ys += [y0 + 0.62 * bt] * 2
        ax.plot(xs, ys, color=col, lw=2.6, solid_joinstyle="miter")
    ax.set_xlim(-0.8, n + 0.05); ax.set_ylim(-0.35, top + (0.45 if numbers else 0.05))
    save(fig, name)



# ------------------------------------------------------------------ contact à fermeture (CEI 60617-7)
def switch(ax, x, y_top, y_bot, closed, lw=2.2):
    """Interrupteur vertical (contact à fermeture, CEI 60617-7) entre y_top et y_bot."""
    yl = y_bot + (y_top - y_bot) * 0.3; yh = y_bot + (y_top - y_bot) * 0.7
    line(ax, [(x, y_top), (x, yh)], lw=lw); line(ax, [(x, y_bot), (x, yl)], lw=lw)
    if closed:
        line(ax, [(x, yl), (x + 0.04, yh)], lw=lw)
    else:
        line(ax, [(x, yl), (x + 0.32, yh - 0.05)], lw=lw)



# ------------------------------------------------------------------ brochage DIP 14 (vue de dessus, brochages dans moteur/logique.py)
def fig_dip(ref):
    p = L.PINS[ref]
    fig, ax = plt.subplots(figsize=(3.6, 3.8)); ax.axis("off"); ax.set_aspect("equal")
    W, Hh = 1.6, 3.5
    ax.add_patch(Rectangle((0, 0), W, Hh, fc=TINT, ec=K, lw=1.8))
    ax.add_patch(matplotlib.patches.Arc((W / 2, Hh), 0.5, 0.5, theta1=180, theta2=360, lw=1.8))
    ax.add_patch(Circle((0.55, Hh - 0.25), 0.07, color=K))
    ax.text(W / 2, Hh / 2, ref, ha="center", va="center", rotation=90, fontsize=14, fontweight="bold", color=NAVY)
    for i in range(7):
        y = Hh - 0.35 - i * 0.47
        # côté gauche : broches 1 à 7 ; côté droit : 14 à 8
        ax.add_patch(Rectangle((-0.3, y - 0.09), 0.3, 0.18, fc="white", ec=K, lw=1.2))
        ax.add_patch(Rectangle((W, y - 0.09), 0.3, 0.18, fc="white", ec=K, lw=1.2))
        ax.text(0.08, y, str(i + 1), ha="left", va="center", fontsize=12.5, color=GR)
        ax.text(W - 0.08, y, str(14 - i), ha="right", va="center", fontsize=12.5, color=GR)
        lab_l, lab_r = p[i], p[13 - i]
        ax.text(-0.38, y, lab_l.replace("VCC", "V$_{CC}$"), ha="right", va="center", fontsize=11, fontweight="bold", color=NAVY)
        ax.text(W + 0.38, y, lab_r.replace("VCC", "V$_{CC}$"), ha="left", va="center", fontsize=11, fontweight="bold", color=NAVY)
    ax.set_xlim(-1.2, W + 1.2); ax.set_ylim(-0.2, Hh + 0.35)
    save(fig, f"dip_{ref}.png")


# ------------------------------------------------------------------ circuits (CEI 60617-2 et -4) : résistance, source, masse, terre, flèches
# Conventions (REGLES 3.3), imposées ici pour toutes les séances :
# - flèche de tension du + vers le −, toujours à droite de son composant, toujours en bleu ETML ;
#   récepteur : courant et tension dans le même sens ; source : sens contraires (convention générateur) ;
# - nom et valeur d'un composant à gauche de son symbole (la droite est réservée à la flèche de tension) ;
# - masse GND : trait horizontal relié au nœud par un court fil, étiquette « GND ».
def resistance(ax, x, y0, y1, nom=None, valeur=None, lw=2.0, w=0.32, h=0.85, cote="gauche", fs=15):
    """Résistance verticale (rectangle CEI) entre y0 et y1, avec son nom (R_1) et sa valeur (4k7) à côté."""
    ym = (y0 + y1) / 2
    line(ax, [(x, y0), (x, ym - h / 2)], lw=lw); line(ax, [(x, ym + h / 2), (x, y1)], lw=lw)
    ax.add_patch(Rectangle((x - w / 2, ym - h / 2), w, h, fill=True, fc="white", ec=K, lw=lw, zorder=3))
    s = 1 if cote == "droite" else -1
    ha = "left" if s > 0 else "right"
    if nom:
        ax.text(x + s * (w / 2 + 0.15), ym + 0.17 + 0.03 * (fs - 15), nom, ha=ha, va="center", fontsize=fs, color=NAVY)
    if valeur:
        ax.text(x + s * (w / 2 + 0.15), ym - 0.22 - 0.045 * (fs - 15), valeur, ha=ha, va="center", fontsize=fs - 2, color=GR)


def source_tension(ax, x, y0, y1, valeur=None, r=0.34, lw=2.0, fs=13):
    """Source de tension idéale (CEI 60617-2) : cercle traversé par le conducteur, entre y0 (−) et y1 (+) ; valeur à gauche."""
    ym = (y0 + y1) / 2
    if valeur:
        ax.text(x - r - 0.15, ym, valeur, ha="right", va="center", fontsize=fs, color=GR)
    line(ax, [(x, y0), (x, ym - r)], lw=lw); line(ax, [(x, ym + r), (x, y1)], lw=lw)
    ax.add_patch(Circle((x, ym), r, fill=True, fc="white", ec=K, lw=lw, zorder=3))
    line(ax, [(x, ym - r), (x, ym + r)], lw=lw, zorder=4)        # le conducteur traverse le cercle


def masse(ax, x, y, etiquette="GND", fil=0.35, lw=2.2, fs=12):
    """Masse GND posée sous le nœud (x, y) : court fil vertical et trait horizontal ; étiquette « GND » à droite."""
    yb = y - fil
    line(ax, [(x, y), (x, yb)], lw=lw)
    line(ax, [(x - 0.3, yb), (x + 0.3, yb)], lw=lw + 0.6)
    if etiquette:
        ax.text(x + 0.42, yb, etiquette, ha="left", va="center", fontsize=fs, color=GR)


def terre(ax, x, y, lw=2.2):
    """Terre (CEI 60617-2, 02-15-01) : trait horizontal et traits décroissants. Seulement pour une vraie liaison à la terre."""
    for k_, w_ in enumerate((0.3, 0.2, 0.1)):
        line(ax, [(x - w_, y - 0.1 * k_), (x + w_, y - 0.1 * k_)], lw=lw)


def noeud(ax, x, y, r=0.06):
    ax.add_patch(Circle((x, y), r, color=K, zorder=4))


def borne(ax, x, y, r=0.07, lw=1.8):
    ax.add_patch(Circle((x, y), r, fill=True, fc="white", ec=K, lw=lw, zorder=4))


def fleche_tension(ax, x, y_moins, y_plus, nom, ecart=0.45, retrait=0.18, fs=15):
    """Flèche de tension aux bornes du composant d'axe x, entre ses nœuds y_plus (+) et y_moins (−) :
    toujours à droite du composant (x + ecart), du + vers le −, en bleu ETML, nom à droite de la flèche."""
    xf = x + ecart
    s = 1 if y_plus > y_moins else -1
    ax.annotate("", xy=(xf, y_moins + s * retrait), xytext=(xf, y_plus - s * retrait),
                arrowprops=dict(arrowstyle="-|>,head_length=0.6,head_width=0.3", color=BLUE, lw=2.0))
    ax.text(xf + 0.12, (y_moins + y_plus) / 2, nom, ha="left", va="center", fontsize=fs, color=BLUE, fontweight="bold")


def fleche_courant(ax, x0, y0, x1, y1, nom, couleur=RED, fs=14, decal=(0.12, 0.0)):
    """Pointe de flèche de courant posée sur un conducteur, de (x0, y0) vers (x1, y1)."""
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>,head_length=0.7,head_width=0.32", color=couleur, lw=2.0))
    ax.text((x0 + x1) / 2 + decal[0], (y0 + y1) / 2 + decal[1], nom, ha="left", va="center", fontsize=fs, color=couleur, fontweight="bold")


# ------------------------------------------------------------------ diodes (CEI 60617-5) : diode, diode Zener, LED
def diode(ax, x, y0, y1, sens="bas", genre="diode", nom=None, valeur=None, lw=2.0, t=0.30, fs=15, ym=None):
    """Diode verticale entre y0 et y1 (y0 < y1), à l'axe x.
    sens « bas » : anode en haut, cathode en bas (le courant direct descend) ; « haut » : l'inverse.
    genre : « diode » (CEI 05-03-01, triangle ouvert traversé par le conducteur), « zener » (05-03-06, trait de cathode
    avec un retour), « led » (05-03-02, deux flèches de rayonnement sortantes).
    Nom et valeur à gauche du symbole (la droite est réservée à la flèche de tension, REGLES 3.3).
    Retourne (y_anode, y_cathode) du symbole."""
    ym = (y0 + y1) / 2 if ym is None else ym
    s = -1 if sens == "bas" else 1                    # direction anode → cathode
    ya, yk = ym - s * t, ym + s * t                   # base du triangle (anode), pointe et trait (cathode)
    line(ax, [(x, y0), (x, y1)], lw=lw)
    ax.add_patch(Polygon([(x - t, ya), (x + t, ya), (x, yk)], closed=True, fill=True, fc="white", ec=K, lw=lw, zorder=3))
    line(ax, [(x, ya), (x, yk)], lw=lw, zorder=4)
    line(ax, [(x - t, yk), (x + t, yk)], lw=lw + 0.4, zorder=4)
    if genre == "zener":
        line(ax, [(x + t, yk), (x + t, yk - s * 0.16)], lw=lw + 0.4, zorder=4)
    if genre == "led":
        for dy in (0.02, -0.22):
            x0_, y0_ = x + 0.30, ym + dy + 0.10
            ax.annotate("", xy=(x0_ + 0.42, y0_ + 0.30), xytext=(x0_, y0_),
                        arrowprops=dict(arrowstyle="-|>,head_length=0.45,head_width=0.22", color=K, lw=1.5), zorder=4)
    if nom:
        ax.text(x - t - 0.15, ym + 0.17 + 0.03 * (fs - 15), nom, ha="right", va="center", fontsize=fs, color=NAVY)
    if valeur:
        ax.text(x - t - 0.15, ym - 0.22 - 0.045 * (fs - 15), valeur, ha="right", va="center", fontsize=fs - 2, color=GR)
    return ya, yk


# ------------------------------------------------------------------ schémas logiques (CEI 60617-12)
QUAL = {"ET": "&", "OU": "≥1", "NON": "1", "OUX": "=1"}


def porte(ax, x, y, fonction, n=2, neg=False, neg_in=(), w=0.9, h=None, lw=1.8, fs=14, pin=0.35, r=0.09):
    """Porte logique CEI posée avec son coin bas gauche en (x, y) : rectangle + qualificatif (« & », « ≥1 », « 1 », « =1 »),
    cercle de négation en sortie (neg) et sur les entrées d'indice neg_in (0 = entrée du haut).
    fonction : « ET », « OU », « NON », « OUX » ou un qualificatif. Retourne (entrées [(x, y)…] du haut vers le bas, sortie (x, y))."""
    qual = QUAL.get(fonction, fonction)
    h = h or max(0.9, 0.42 * n + 0.2)
    ax.add_patch(Rectangle((x, y), w, h, fill=True, fc="white", ec=K, lw=lw, zorder=3))
    ax.text(x + w / 2, y + h - 0.24, qual, ha="center", va="center", fontsize=fs, color=K, zorder=4)
    ys = [y + h / 2] if n == 1 else [y + h - (h / n) * (i + 0.5) for i in range(n)]
    entrees = []
    for i, yy in enumerate(ys):
        xb = x
        if i in neg_in:
            ax.add_patch(Circle((x - r, yy), r, fill=True, fc="white", ec=K, lw=lw, zorder=4)); xb = x - 2 * r
        line(ax, [(xb - pin, yy), (xb, yy)], lw=lw)
        entrees.append((xb - pin, yy))
    yo, xo = y + h / 2, x + w
    if neg:
        ax.add_patch(Circle((xo + r, yo), r, fill=True, fc="white", ec=K, lw=lw, zorder=4)); xo += 2 * r
    line(ax, [(xo, yo), (xo + pin, yo)], lw=lw)
    return entrees, (xo + pin, yo)


def fil(ax, *pts, lw=1.8, noeuds=(), sauts=(), r=0.09):
    """Liaison orthogonale passant par les points donnés (REGLES 3.3).
    noeuds : points de liaison à poser (jonctions en T) ; sauts : autres fils (listes de points) que celui-ci croise sans
    liaison : ses tronçons horizontaux sautent leurs tronçons verticaux (demi-cercle de rayon r, comme le « jumpover » d'Altium)."""
    import math
    verts = [(a, b) for q in sauts for a, b in zip(q[:-1], q[1:]) if a[0] == b[0]]
    out = [pts[0]]
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        if y1 == y2:
            s = 1 if x2 > x1 else -1
            xs = sorted({a[0] for a, b in verts if min(a[1], b[1]) < y1 < max(a[1], b[1]) and min(x1, x2) + r < a[0] < max(x1, x2) - r},
                        key=lambda x: s * x)
            for xc in xs:
                th = [math.pi * (1 - k / 12) if s > 0 else math.pi * k / 12 for k in range(13)]
                out += [(xc + r * math.cos(t), y1 + r * math.sin(t)) for t in th]
        out.append((x2, y2))
    line(ax, out, lw=lw)
    for p in noeuds:
        noeud(ax, *p)


def alimentation(ax, x, y, etiquette="+5 V", fil=0.3, lw=2.2, fs=13):
    """Alimentation (+5 V, V_CC) posée au-dessus du nœud (x, y) : court fil vertical et trait horizontal, étiquette au-dessus
    du trait (miroir de la masse GND, REGLES 3.3) ; toujours plus haut que les composants qu'elle alimente."""
    yh = y + fil
    line(ax, [(x, y), (x, yh)], lw=lw)
    line(ax, [(x - 0.3, yh), (x + 0.3, yh)], lw=lw + 0.6)
    if etiquette:
        ax.text(x, yh + 0.2, etiquette, ha="center", va="center", fontsize=fs, color=NAVY)


# ------------------------------------------------------------------ tableau de Karnaugh
# Logique « à zones » (Gaël, 11/23/2026, d'après son ancien support) :
# - pas de codes 00, 01, 11, 10 : une barre par variable, au-dessus des colonnes (A, B) ou à gauche des lignes (C, D) où elle vaut 1,
#   la lettre centrée sur sa barre ; la sortie S reliée au coin ;
# - disposition : colonnes A̅B̅, AB̅, AB, A̅B, lignes C̅D̅, CD̅, CD, C̅D (une seule variable change entre deux cases voisines) ;
# - un groupe qui passe par un bord est dessiné ouvert vers l'extérieur (ses morceaux n'ont pas de côté sur le bord du tableau) ;
# - chaque terme, de la couleur de son groupe, est relié au groupe par un trait qui part d'un coin du groupe à 45° vers l'extérieur,
#   coudé à l'horizontale avant le terme ; le trait ne longe aucune ligne du tableau, ne touche ni une barre, ni sa lettre,
#   ni le trait de S, et ne remonte jamais vers les barres A et B ; un groupe sans coin libre (entouré par les barres ou par
#   d'autres groupes) part du milieu d'un côté de case : le trait passe alors entre les chiffres, sans en toucher ;
# - les termes ne se chevauchent pas et ne se posent jamais entre le tableau et ses barres.
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

GRAY2 = [0, 1, 3, 2]
KCOUL = ["#1E8C46", "#EE0000", "#297FD5", "#242852", "#E67814", "#7A3DB8"]     # vert, rouge, bleu, marine, orange, violet
KJAUNE, KOCRE, KGRIS = "#F3EBA6", "#D9AE45", "#E6E6E6"   # zones, lignes intérieures, bandes des codes (modèle de Gaël)
PT_UNITE = 0.95 * 72          # points par case dans fig_karnaugh (0,95 pouce par case)
KRAPPORT = []                 # géométrie de chaque tableau dessiné : karnaugh_figures.json, controle/karnaugh.py


def karnaugh_cases(n):
    """Disposition d'un tableau à n variables (2, 3 ou 4), A poids faible.
    Renvoie (codes des lignes, codes des colonnes, variables des lignes, variables des colonnes, case(l, c) → combinaison)."""
    if n == 2:
        return [0, 1], [0, 1], ["B"], ["A"], lambda l, c: 2 * l + c
    if n == 3:
        return [0, 1], GRAY2, ["C"], ["A", "B"], lambda l, c: 4 * l + c
    return GRAY2, GRAY2, ["C", "D"], ["A", "B"], lambda l, c: 4 * l + c


def _taille(t, fs, pt, gras=False, italique=False):
    """Largeur et hauteur d'un texte (mathtext compris), en unités de dessin."""
    fp = FontProperties(family="Liberation Sans", weight="bold" if gras else "normal", style="italic" if italique else "normal")
    e = TextPath((0, 0), t, size=fs, prop=fp).get_extents()
    return float(e.width) / pt, float(max(e.height, fs * 0.72)) / pt


def _croise(p1, p2, p3, p4):
    o = lambda a, b, c: (lambda v: (v > 1e-9) - (v < -1e-9))((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
    return o(p1, p2, p3) * o(p1, p2, p4) < 0 and o(p3, p4, p1) * o(p3, p4, p2) < 0


def _dans(p, q, r):
    """Le segment p-q entre-t-il dans le rectangle r = (xa, ya, xb, yb) ?"""
    return any(r[0] < p[0] + (q[0] - p[0]) * k / 40 < r[2] and r[1] < p[1] + (q[1] - p[1]) * k / 40 < r[3] for k in range(41))


def _dseg(p1, p2, p3, p4):
    """Distance minimale entre deux segments (0 s'ils se croisent)."""
    if _croise(p1, p2, p3, p4):
        return 0.0
    def dp(p, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
        return ((p[0] - a[0] - t * dx) ** 2 + (p[1] - a[1] - t * dy) ** 2) ** 0.5
    return min(dp(p1, p3, p4), dp(p2, p3, p4), dp(p3, p1, p2), dp(p4, p1, p2))


def _chevauche(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def karnaugh(ax, n, valeurs, groupes=(), termes=None, x0=0.0, y0=0.0, cote=1.0, fs=18, vide=False, couleurs=KCOUL,
             indices=False, sortie="S", couleur_termes=None, pt=PT_UNITE, nom=None):
    """Dessine un tableau de Karnaugh à zones. valeurs : 2^n valeurs (0, 1, « X ») indexées par la combinaison (A poids faible).
    groupes : listes de combinaisons entourées ; termes : pour chaque groupe, texte mathtext du terme (ou (texte, côté), côté ignoré).
    vide : cases sans valeur ; indices : numéro de la combinaison dans le coin de chaque case (« centre » : au milieu, en gris).
    Renvoie l'encombrement (xmin, xmax, ymin, ymax) du dessin, termes compris."""
    u, lw = cote, 2.2
    L, C, vl, vc, case = karnaugh_cases(n)
    nl, nc = len(L), len(C)
    X1, Y1 = x0 + nc * u, y0 - nl * u          # coin bas droit
    pos, textes_cases = {}, []
    for i, l in enumerate(L):
        for j, c in enumerate(C):
            k = case(l, c); pos[k] = (i, j)
            x, y = x0 + j * u, y0 - (i + 1) * u
            ax.add_patch(Rectangle((x, y), u, u, fill=True, fc="white", ec="none", zorder=1))
            v = valeurs[k]
            if not vide and v is not None:
                textes_cases.append((x + u / 2, y + u / 2))
                ax.text(x + u / 2, y + u / 2, str(v), ha="center", va="center", fontsize=fs,
                        color=(BLUE if v == 1 else GR if v == "X" else NAVY), fontweight="bold" if v == 1 else "normal", zorder=3)
            if indices == "centre":           # tableau vide qui présente la numérotation : le numéro est le contenu
                textes_cases.append((x + u / 2, y + u / 2))
                ax.text(x + u / 2, y + u / 2, str(k), ha="center", va="center", fontsize=fs * 0.8, color=GR, zorder=3)
            elif indices:                       # repère dans le coin, la case reste libre pour écrire
                textes_cases.append((x + u * 0.8, y + u * 0.15))
                ax.text(x + u * 0.93, y + u * 0.07, str(k), ha="right", va="bottom", fontsize=fs * 0.6, color=GR, zorder=3)
    # cadre du modèle de Gaël (11/24/2026) : codes BA et DC sur des bandes grises ; zones jaunes A en haut, B en bas,
    # C à gauche, D à droite ; lignes intérieures ocre, prolongées à travers les bandes jusqu'aux zones A et C ; bord foncé
    hb, zb, lg = 0.5 * u, 0.42 * u, 1.4
    fcode, fz = fs * 0.9, fs * 0.9                     # corps des codes et des lettres de zone
    ax.add_patch(Rectangle((x0, y0), nc * u, hb, fc=KGRIS, ec="none", zorder=0.5))
    ax.add_patch(Rectangle((x0 - hb, Y1), hb, nl * u, fc=KGRIS, ec="none", zorder=0.5))
    for j, c in enumerate(C):
        ax.text(x0 + (j + 0.5) * u, y0 + hb / 2, "".join(str((c >> r) & 1) for r in reversed(range(len(vc)))),
                ha="center", va="center", fontsize=fcode, color=NAVY, zorder=3)
    for i, l in enumerate(L):
        ax.text(x0 - hb / 2, y0 - (i + 0.5) * u, "".join(str((l >> r) & 1) for r in reversed(range(len(vl)))),
                ha="center", va="center", fontsize=fcode, color=NAVY, rotation=90, zorder=3)
    for j in range(1, nc):
        ax.plot([x0 + j * u] * 2, [Y1, y0], color=KOCRE, lw=lg, zorder=2)
    for i in range(1, nl):
        ax.plot([x0, X1], [y0 - i * u] * 2, color=KOCRE, lw=lg, zorder=2)
    zc = [(vc[0], "haut", [j for j, c in enumerate(C) if c & 1]), (vl[0], "gauche", [i for i, l in enumerate(L) if l & 1])]
    if len(vc) > 1: zc.append((vc[1], "bas", [j for j, c in enumerate(C) if (c >> 1) & 1]))
    if len(vl) > 1: zc.append((vl[1], "droite", [i for i, l in enumerate(L) if (l >> 1) & 1]))
    lettres, souples, cadres = [], [], {}
    for v, cote_, idx in zc:
        a_, b_ = min(idx), max(idx) + 1
        if cote_ in ("haut", "bas"):
            xa, xb = x0 + a_ * u, x0 + b_ * u
            ya = y0 + hb if cote_ == "haut" else Y1 - zb
            r_, rot = (xa, ya, xb, ya + zb), 0
            if cote_ == "haut":
                for xx in (xa, xb):
                    ax.plot([xx, xx], [y0, y0 + hb], color=KOCRE, lw=lg, zorder=2)
                ax.plot([xa, xb], [y0 + hb] * 2, color=NAVY, lw=lw, zorder=3, solid_capstyle="butt")
        else:
            yh, ybas = y0 - a_ * u, y0 - b_ * u
            xa = x0 - hb - zb if cote_ == "gauche" else X1
            r_, rot = (xa, ybas, xa + zb, yh), (90 if cote_ == "gauche" else -90)
            if cote_ == "gauche":
                for yy in (yh, ybas):
                    ax.plot([x0 - hb, x0], [yy, yy], color=KOCRE, lw=lg, zorder=2)
                ax.plot([x0 - hb] * 2, [ybas, yh], color=NAVY, lw=lw, zorder=3, solid_capstyle="butt")
        ax.add_patch(Rectangle((r_[0], r_[1]), r_[2] - r_[0], r_[3] - r_[1], fc=KJAUNE, ec=KOCRE, lw=1.0, zorder=0.6))
        cx_, cy_ = (r_[0] + r_[2]) / 2, (r_[1] + r_[3]) / 2
        ax.text(cx_, cy_, v, ha="center", va="center", fontsize=fz, color=NAVY, fontweight="bold", rotation=rot, zorder=3)
        wv, hv = _taille(v, fz, pt, gras=True)
        if rot: wv, hv = hv, wv
        lettres.append((cx_ - wv / 2 - 0.12 * u, cy_ - hv / 2 - 0.12 * u, cx_ + wv / 2 + 0.12 * u, cy_ + hv / 2 + 0.12 * u))
        cadres[cote_] = r_
        if cote_ in ("bas", "droite"):
            souples.append(r_)                          # un trait de terme peut la traverser, loin de la lettre
    ax.plot([x0, X1, X1, x0, x0], [y0, y0, Y1, Y1, y0], color=NAVY, lw=lw, zorder=3, solid_joinstyle="miter")
    # coin : diagonale entre le nom des colonnes (BA) et celui des lignes (DC), sortie S au bout
    pointe = (x0 - hb - 0.2 * u, y0 + hb + 0.2 * u)
    ax.plot([pointe[0], x0], [pointe[1], y0], color=NAVY, lw=1.4, zorder=3)
    nom_c, nom_l = "".join(reversed(vc)), "".join(reversed(vl))
    fn = fs * 0.9
    wc, hc = _taille(nom_c, fn, pt, gras=True)
    wn, hn = _taille(nom_l, fn, pt, gras=True)
    ax.text(pointe[0] + 0.2 * u, y0 + hb + 0.05 * u, nom_c, ha="left", va="bottom", fontsize=fn, color=NAVY, fontweight="bold", zorder=3)
    # nom des lignes : symétrique de celui des colonnes par rapport à la diagonale (même écart, demande de Gaël 11/24/2026)
    ax.text(x0 - hb - 0.05 * u - hn / 2, y0 + hb - wn / 2, nom_l, ha="center", va="center", fontsize=fn, color=NAVY,
            fontweight="bold", rotation=90, zorder=3)
    ws, hs = _taille(sortie or "S", fs, pt, gras=True)
    if sortie:
        ax.text(pointe[0] - 0.03 * u, pointe[1], sortie, ha="right", va="bottom", fontsize=fs, color=NAVY, fontweight="bold", zorder=3)
    haut = max(y0 + hb + zb, y0 + hb + 0.05 * u + hc, pointe[1] + hs)
    gauche = min(x0 - hb - zb, x0 - hb - 0.05 * u - hn, pointe[0] - 0.03 * u - ws)
    # régions interdites aux traits et aux termes : tout le haut (bande, zone A, coin), tout le côté gauche (bande, zone C)
    zones = [(gauche - 0.06 * u, y0, X1 + 0.06 * u, haut + 0.06 * u), (gauche - 0.06 * u, Y1, x0, y0)] + lettres
    traits = []
    tableau = (x0, Y1, X1, y0)
    # groupes : un rectangle par bloc ; un bloc coupé par un bord du tableau est ouvert vers l'extérieur
    def blocs(vals, tot):
        s_ = sorted(set(vals))
        if len(s_) == tot or s_ == list(range(s_[0], s_[-1] + 1)):
            return [(s_, False, False)]
        bas, v = [], 0
        while v in s_: bas.append(v); v += 1
        return [(bas, True, False), ([v for v in s_ if v not in bas], False, True)]
    ov, ov2 = 0.12 * u, 0.05 * u                    # dépassement des groupes ouverts : moins vers les zones B et D (lettre proche)
    G = []
    for g, grp in enumerate(groupes):
        col = couleurs[g % len(couleurs)]
        cells = [pos[k] for k in grp]
        m = (0.07 + 0.045 * (g % 3)) * u
        bl = []
        for br, ot, ob in blocs([i for i, _ in cells], nl):
            for bc, og, od in blocs([j for _, j in cells], nc):
                xa = x0 - ov if og else x0 + min(bc) * u + m
                xb = X1 + ov2 if od else x0 + (max(bc) + 1) * u - m
                yb = y0 + ov if ot else y0 - min(br) * u - m
                ya = Y1 - ov2 if ob else y0 - (max(br) + 1) * u + m
                coins = [(xa, yb), (xb, yb), (xb, ya), (xa, ya)]          # haut gauche, haut droit, bas droit, bas gauche
                cotes = [not ot, not od, not ob, not og]                   # haut, droite, bas, gauche
                segs = [(coins[k], coins[(k + 1) % 4]) for k in range(4) if cotes[k]]
                if all(cotes):
                    ax.add_patch(Rectangle((xa, ya), xb - xa, yb - ya, fill=False, ec=col, lw=3.0, zorder=4))
                else:
                    d0 = next(k for k in range(4) if cotes[k] and not cotes[k - 1])
                    pts, k = [coins[d0]], d0
                    while cotes[k % 4] and len(pts) < 5:
                        pts.append(coins[(k + 1) % 4]); k += 1
                    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, lw=3.0, zorder=4, solid_capstyle="butt", solid_joinstyle="miter")
                bl.append(dict(br=br, bc=bc, coins=coins, cotes=cotes, ouvert=(ot, od, ob, og), segs=segs))
        cx = sum(x0 + (j + 0.5) * u for _, j in cells) / len(cells)
        G.append(dict(col=col, blocs=bl, cx=cx, k=grp))
    # termes : trait à 45° vers l'extérieur depuis un coin du groupe (ou, faute de mieux, depuis le milieu d'un côté de case :
    # le trait passe alors entre les chiffres), coude, puis le terme. On garde le tracé le moins coûteux : peu de tableau
    # traversé, pas de croisement, vers le bas plutôt que vers le haut, du côté où se trouve le groupe.
    places, rapport = [], []
    tous_segs = [(gi, bi, s_) for gi, g_ in enumerate(G) for bi, b in enumerate(g_["blocs"]) for s_ in b["segs"]]
    xc = (x0 + X1) / 2
    DIAG = [(-1, 1), (1, 1), (1, -1), (-1, -1)]                       # diagonale vers l'extérieur de chaque coin
    for gi, g_ in enumerate(G):
        if not termes or gi >= len(termes) or not termes[gi]:
            continue
        t = termes[gi][0] if isinstance(termes[gi], (tuple, list)) else termes[gi]
        w, h = _taille(t, fs, pt)
        cand = []                                                      # (bloc, départ, direction, coût de base)
        for bi, b in enumerate(g_["blocs"]):
            co, ct = b["coins"], b["cotes"]
            for k in range(4):
                if ct[k] or ct[k - 1]:
                    cand.append((bi, co[k], DIAG[k], 0.0))
            # milieu d'un côté de case, décalé de la marge du groupe : le trait franchit la ligne du tableau au milieu
            # d'un côté de case et passe ainsi à mi-distance de deux chiffres voisins (0,35 case)
            mx = [x0 + (j + 0.5) * u for j in b["bc"]]
            my = [y0 - (i + 0.5) * u for i in b["br"]]
            dh = abs(co[0][1] - (y0 - min(b["br"]) * u))       # marge du groupe
            if ct[0]: cand += [(bi, (x - d[0] * dh, co[0][1]), d, 0.15) for x in mx for d in ((-1, 1), (1, 1))]
            if ct[2]: cand += [(bi, (x - d[0] * dh, co[2][1]), d, 0.15) for x in mx for d in ((-1, -1), (1, -1))]
            if ct[1]: cand += [(bi, (co[1][0], y - d[1] * dh), d, 0.15) for y in my for d in ((1, 1), (1, -1))]
            if ct[3]: cand += [(bi, (co[3][0], y - d[1] * dh), d, 0.15) for y in my for d in ((-1, 1), (-1, -1))]
        best = None
        for bi, P, (sx, sy), base in cand:
            tx = (X1 - P[0]) if sx > 0 else (P[0] - x0)
            ty = (y0 - P[1]) if sy > 0 else (P[1] - Y1)
            le = max(0.0, min(tx, ty)) if (x0 < P[0] < X1 and Y1 < P[1] < y0) else 0.0
            S_ = (P[0] + sx * le, P[1] + sy * le)                    # sortie du tableau
            if sy > 0 and x0 + 1e-6 < P[0] + sx * max(0.0, y0 - P[1]) < X1 - 1e-6:
                continue                                                # monterait vers les barres A et B
            if any(_dseg(P, S_, c, c) < 0.27 * u for c in textes_cases):
                continue                                                # passerait sur un chiffre
            autres = [s_ for gj, bj, s_ in tous_segs if (gj, bj) != (gi, bi)]
            ecart = g_["cx"] - xc
            cote_pref = 0.12 if abs(ecart) < 1e-6 else (0.0 if ecart * sx > 0 else 0.35)
            for kk, Lx in enumerate((0.38, 0.7, 1.02, 1.34, 1.66)):
                E = (P[0] + sx * (le + Lx) * u, P[1] + sy * (le + Lx) * u)
                T = (E[0] + sx * 0.22 * u, E[1])
                bx = (T[0] + 0.05 * u, T[1] - h / 2 - 0.03 * u, T[0] + 0.05 * u + w, T[1] + h / 2 + 0.03 * u) if sx > 0 else \
                     (T[0] - 0.05 * u - w, T[1] - h / 2 - 0.03 * u, T[0] - 0.05 * u, T[1] + h / 2 + 0.03 * u)
                chemin = ((P, E), (E, T))
                if _chevauche(bx, (x0 - 0.03 * u, Y1 - 0.03 * u, X1 + 0.03 * u, y0 + 0.03 * u)): continue
                if any(_chevauche(bx, z) for z in zones + souples): continue
                if any(_chevauche(bx, (q[0] - 0.05 * u, q[1] - 0.05 * u, q[2] + 0.05 * u, q[3] + 0.05 * u)) for q in places): continue
                if any(_dans(a, b_, z) for a, b_ in ((S_, E), (E, T)) for z in zones): continue
                if any(_dans(a, b_, q) for a, b_ in chemin for q in places): continue
                if any(_dseg(a, b_, c, d) < 0.12 * u for a, b_ in chemin for c, d in traits): continue
                if any(_dans(c, d, bx) for c, d in traits + [s_ for _, _, s_ in tous_segs]): continue
                croisements = sum(1 for a, b_ in chemin for s_ in autres if _croise(a, b_, *s_))
                traverse_zone = sum(1 for a, b_ in ((S_, E), (E, T)) for z in souples if _dans(a, b_, z))
                # frôler un autre groupe (passer par son coin, longer son trait) prête à confusion
                frole = sum(1 for a, b_ in chemin for s_ in autres if not _croise(a, b_, *s_) and _dseg(a, b_, *s_) < 0.06 * u)
                cout = base + (0.5 if sy > 0 else 0.0) + cote_pref + 0.3 * kk + 2.0 * le + 1.0 * croisements + 1.5 * frole + 2.5 * traverse_zone
                if best is None or cout < best[0] - 1e-6:
                    best = (cout, P, E, T, bx, sx, le, S_, croisements, frole)
                break
        if best is None:
            raise ValueError(f"Karnaugh {nom} : pas de place pour le terme {t}")
        _, P, E, T, bx, sx, le, S_, cr, fr = best
        ax.plot([P[0], E[0], T[0]], [P[1], E[1], T[1]], color=NAVY, lw=1.6, zorder=5, solid_joinstyle="round")
        ax.plot([P[0]], [P[1]], marker="o", ms=4.5, color=NAVY, zorder=6)
        ax.text(T[0] + sx * 0.05 * u, T[1], t, ha="left" if sx > 0 else "right", va="center", fontsize=fs, color=couleur_termes or g_["col"], zorder=6)
        places.append(bx); traits += [(P, E), (E, T)]
        rapport.append(dict(groupe=gi, terme=t, depart=P, sortie=S_, coude=E, fin=T, cadre=bx, traverse=le / u,
                            interieur=le > 0.2 * u, croisements=cr, frolements=fr))
    KRAPPORT.append(dict(nom=nom, n=n, cote=u, tableau=tableau, zones=zones, zones_traversables=souples, textes=textes_cases, termes=rapport,
                         groupes=[dict(k=list(g_["k"]), blocs=[dict(ouvert=b["ouvert"], segments=b["segs"]) for b in g_["blocs"]]) for g_ in G]))
    zz = zones + souples
    xs = [z[0] for z in zz] + [z[2] for z in zz] + [x0 - ov - 0.1 * u, X1 + ov + 0.1 * u] + [q[0] for q in places] + [q[2] for q in places]
    ys = [z[1] for z in zz] + [z[3] for z in zz] + [Y1 - ov - 0.1 * u, y0 + ov + 0.1 * u] + [q[1] for q in places] + [q[3] for q in places]
    return min(xs), max(xs), min(ys), max(ys)


def fig_karnaugh(nom, n, valeurs, groupes=(), termes=None, vide=False, fs=18, indices=False, titre=None, sortie="S", couleur_termes=None):
    """Figure autonome d'un tableau de Karnaugh à zones (voir karnaugh) : 0,95 pouce par case, cadrage sur le dessin."""
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_aspect("equal")
    xmin, xmax, ymin, ymax = karnaugh(ax, n, valeurs, groupes, termes, fs=fs, vide=vide, indices=indices, sortie=sortie,
                                      couleur_termes=couleur_termes, nom=nom)
    if titre:
        ax.text((xmin + xmax) / 2, ymax + 0.1, titre, ha="center", va="bottom", fontsize=fs * 0.85, color=NAVY, fontweight="bold")
        ymax += 0.5
    fig.set_size_inches((xmax - xmin) * PT_UNITE / 72, (ymax - ymin) * PT_UNITE / 72)
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    save(fig, nom)
    import json
    fk = os.path.join(_DOSSIER, KARNAUGH)
    d = json.load(open(fk, encoding="utf-8")) if os.path.exists(fk) else {}
    d[nom] = dict(KRAPPORT[-1], avec_termes=bool(termes))
    json.dump(d, open(fk, "w", encoding="utf-8"), ensure_ascii=False)
    return xmin, xmax, ymin, ymax


def image_karnaugh(n, valeurs, groupes=(), termes=None, fs=18, limites=None, px_case=150, **kw):
    """Tableau de Karnaugh rendu en image PIL (animations) ; limites (xmin, xmax, ymin, ymax) : même cadrage pour toutes
    les étapes d'une même scène, pour que le tableau ne bouge pas quand un groupe ou un terme apparaît. Renvoie (image, limites)."""
    import io
    from PIL import Image
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_aspect("equal")
    bb = karnaugh(ax, n, valeurs, groupes, termes, fs=fs, **kw)
    xmin, xmax, ymin, ymax = limites or bb
    fig.set_size_inches((xmax - xmin) * PT_UNITE / 72, (ymax - ymin) * PT_UNITE / 72)
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=px_case / 0.95, facecolor="white"); plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB"), (xmin, xmax, ymin, ymax)
