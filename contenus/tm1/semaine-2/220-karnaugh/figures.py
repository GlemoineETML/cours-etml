# -*- coding: utf-8 -*-
"""Figures de la séance 220 Simplification par Karnaugh : tableaux sur le modèle de Gaël (codes BA, DC et zones jaunes), groupes reliés à leurs termes (moteur/cei.py : karnaugh, fig_karnaugh), schéma de la rinceuse,
équations en image (secours des équations éditables, equations.json).
Les fonctions logiques de la séance sont définies ici (FONCTIONS) : la fiche 230 EX et verif.py les reprennent.
Index d'une combinaison : A poids faible (k = 8·D + 4·C + 2·B + A). Sortie S, entrées A, B, C, D (REGLES 3.4)."""
import json, os, re
from moteur.cei import plt, save, porte, fil, fig_eq_txt, fig_karnaugh, NAVY, RED

ICI = os.path.dirname(os.path.abspath(__file__))
NOT = lambda x: 1 - x
bit = lambda k, i: (k >> i) & 1          # i = 0 : A, 1 : B, 2 : C, 3 : D


def table(n, f, x=()):
    """Valeurs de S pour les 2^n combinaisons ; x : indices des cas indifférents."""
    return ["X" if k in x else f(*[bit(k, i) for i in range(n)]) for k in range(1 << n)]


# (nombre de variables, fonction (A, B, C, D), cas indifférents, groupes du corrigé, équation simplifiée (fonction))
FONCTIONS = {
    "rinc": (3, lambda a, b, c: (NOT(a) & b & NOT(c)) | (a & b & NOT(c)) | (a & NOT(b) & c) | (NOT(a) & b & c) | (a & b & c), (),
             [[2, 3, 6, 7], [5, 7]], lambda a, b, c: b | (a & c)),
    "k4": (4, lambda a, b, c, d: int((a, c) in ((0, 0), (1, 1))), (), [[0, 2, 8, 10], [5, 7, 13, 15]], lambda a, b, c, d: (NOT(a) & NOT(c)) | (a & c)),
    "vid": (3, lambda a, b, c: c | (NOT(a) & b), (4, 5), [[4, 5, 6, 7], [2, 6]], lambda a, b, c: c | (NOT(a) & b)),
    "vid0": (3, lambda a, b, c: (b & c) | (NOT(a) & b) if not (c and not b) else 0, (), [[6, 7], [2, 6]], lambda a, b, c: (b & c) | (NOT(a) & b)),
    "t1": (3, lambda a, b, c: NOT(b), (), [[0, 1, 4, 5]], lambda a, b, c: NOT(b)),
    "t2": (3, lambda a, b, c: (a & b) | (b & c), (), [[3, 7], [6, 7]], lambda a, b, c: (a & b) | (b & c)),
    "t3": (4, lambda a, b, c, d: (NOT(c) & NOT(d)) | (a & NOT(b) & c), (), [[0, 1, 2, 3], [5, 13]], lambda a, b, c, d: (NOT(c) & NOT(d)) | (a & NOT(b) & c)),
    "ejec": (4, lambda a, b, c, d: NOT(a) | (NOT(b) & NOT(d)) | (NOT(c) & NOT(d)), (), [[0, 2, 4, 6, 8, 10, 12, 14], [0, 1, 4, 5], [0, 1, 2, 3]],
             lambda a, b, c, d: NOT(a) | (NOT(b) & NOT(d)) | (NOT(c) & NOT(d))),
    "conv": (3, lambda a, b, c: (a & b) | (a & NOT(b) & c), (), [[3, 7], [5, 7]], lambda a, b, c: a & (b | c)),
    # fiche 230 EX
    "n1": (3, lambda a, b, c: (a & NOT(b) & NOT(c)) | (a & b & NOT(c)) | (a & b & c), (), [[1, 3], [3, 7]], lambda a, b, c: (a & NOT(c)) | (a & b)),
    "n3": (4, lambda a, b, c, d: int(a == c), (), [[0, 2, 8, 10], [5, 7, 13, 15]], lambda a, b, c, d: (NOT(a) & NOT(c)) | (a & c)),
    "n5": (3, lambda a, b, c: (a & NOT(b)) | (a & b & NOT(c)), (), [[1, 3], [1, 5]], lambda a, b, c: (a & NOT(b)) | (a & NOT(c))),
}


# termes reliés aux groupes (mathtext, côté « g » ou « d »), dans l'ordre des groupes de FONCTIONS
O = lambda v: r"\overline{%s}" % v
TERMES = {
    "rinc": [(r"$B$", "d"), (r"$A\cdot C$", "d")],
    "k4": [(r"$%s\cdot %s$" % (O("A"), O("C")), "d"), (r"$A\cdot C$", "d")],
    "vid": [(r"$C$", "d"), (r"$%s\cdot B$" % O("A"), "d")],
    "vid0": [(r"$B\cdot C$", "d"), (r"$%s\cdot B$" % O("A"), "d")],
    "t1": [(r"$%s$" % O("B"), "d")],
    "t2": [(r"$A\cdot B$", "d"), (r"$B\cdot C$", "d")],
    "t3": [(r"$%s\cdot %s$" % (O("C"), O("D")), "d"), (r"$A\cdot %s\cdot C$" % O("B"), "d")],
    "ejec": [(r"$%s$" % O("A"), "g"), (r"$%s\cdot %s$" % (O("B"), O("D")), "d"), (r"$%s\cdot %s$" % (O("C"), O("D")), "d")],
    "conv": [(r"$A\cdot B$", "d"), (r"$A\cdot C$", "d")],
    "n1": [(r"$A\cdot %s$" % O("C"), "d"), (r"$A\cdot B$", "d")],
    "n3": [(r"$%s\cdot %s$" % (O("A"), O("C")), "d"), (r"$A\cdot C$", "d")],
    "n5": [(r"$A\cdot %s$" % O("C"), "d"), (r"$A\cdot %s$" % O("B"), "d")],
}


def valeurs(nom):
    n, f, x, *_ = FONCTIONS[nom]
    return table(n, f, x)


def mathtext(src):
    s = src
    while "\\bar{" in s:
        i = s.index("\\bar{"); j = i + 5; d = 1
        while d:
            d += {"{": 1, "}": -1}.get(s[j], 0); j += 1
        s = s[:i] + "\\overline{" + s[i + 5:j - 1] + "}" + s[j:]
    return re.sub(r"\\u\{([^}]*)\}", r"\\mathrm{\1}", s).replace("\\f{", "\\frac{")


def rinceuse(nom, c=NAVY):
    """S = B + A · C : un ET puis un OU."""
    fig, ax = plt.subplots(figsize=(5.0, 2.4)); ax.axis("off"); ax.set_aspect("equal"); ax.set_xlim(-0.9, 4.6); ax.set_ylim(-0.3, 2.3)
    e1, s1 = porte(ax, 0.2, 0.0, "ET")
    for p, t in zip(e1, ("$A$", "$C$")): ax.text(p[0] - 0.08, p[1], t, ha="right", va="center", fontsize=14, style="italic", color=c)
    e2, s2 = porte(ax, 2.4, 0.5, "OU")
    ax.text(e2[0][0] - 0.08, e2[0][1], "$B$", ha="right", va="center", fontsize=14, style="italic", color=c)
    fil(ax, s1, (1.95, s1[1]), (1.95, e2[1][1]), e2[1])
    ax.text(s2[0] + 0.08, s2[1], "$S$", ha="left", va="center", fontsize=14, style="italic", color=c)
    save(fig, nom)


FS_DIAPO = 24          # corps des tableaux de la présentation : au moins 8 pt une fois réduits (REGLES 9.4)


def produire(ctx):
    import moteur.cei as cei
    cei.ecrire_dans(ctx.images)
    for nom, src in json.load(open(os.path.join(ICI, "equations.json"), encoding="utf-8")).items():
        if nom != "_": fig_eq_txt(mathtext(src), nom + ".png")
    # présentation
    fig_karnaugh("k_idx3.png", 3, [None] * 8, vide=True, indices="centre", fs=FS_DIAPO)
    fig_karnaugh("k_idx4.png", 4, [None] * 16, vide=True, indices="centre", fs=FS_DIAPO)
    for nom in ("rinc", "k4", "vid", "t1", "t2", "t3", "conv", "ejec"):
        n, f, x, g, _ = FONCTIONS[nom]
        fig_karnaugh(f"k_{nom}_v.png", n, valeurs(nom), fs=FS_DIAPO)
        fig_karnaugh(f"k_{nom}.png", n, valeurs(nom), g, TERMES[nom], fs=FS_DIAPO)
    fig_karnaugh("k_vid0.png", 3, valeurs("vid"), FONCTIONS["vid0"][3], TERMES["vid0"], fs=FS_DIAPO)
    rinceuse("fig_rinceuse.png")
    # fiche 230 EX : tableaux vides (élève) et regroupés avec les termes (corrigé, en rouge)
    for nom in ("n1", "n3", "n5"):
        n, f, x, g, _ = FONCTIONS[nom]
        fig_karnaugh(f"f_{nom}_q.png", n, [None] * (1 << n), vide=True, indices=(n == 4), fs=24)
        fig_karnaugh(f"f_{nom}_c.png", n, valeurs(nom), g, TERMES[nom], fs=24)
    fig_karnaugh("f_n4_q.png", 3, [None] * 8, vide=True, fs=24)
    fig_karnaugh("f_n4_c.png", 3, valeurs("vid"), FONCTIONS["vid"][3], TERMES["vid"], fs=24)
    fig_karnaugh("f_n4_c0.png", 3, valeurs("vid"), FONCTIONS["vid0"][3], TERMES["vid0"], fs=24)
    rinceuse("f_n2_schema.png", c=RED)
