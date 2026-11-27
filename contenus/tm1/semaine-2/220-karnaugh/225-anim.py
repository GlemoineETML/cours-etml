# -*- coding: utf-8 -*-
"""225 Simplification par Karnaugh – animation (TM1 – El DT 1, semaine 2, va avec la présentation 220 et la fiche 230 EX).
Sortie S, entrées A, B, C, D (REGLES 3.4). Tables : entrées du poids fort au poids faible (C B A). Tableaux de Karnaugh sur le
modèle de Gaël (moteur/cei.py : karnaugh), rendus par image_karnaugh pour être identiques à ceux de la présentation.
Rendu : python3 build.py tm1/semaine-2/220-karnaugh --seulement animations · aperçu : voir en bas."""
import sys, os, importlib.util
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", ".."))   # aperçu direct
from moteur.anim import *
from moteur import cei

_spec = importlib.util.spec_from_file_location("fig220", os.path.join(ICI, "figures.py"))
FIG = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(FIG)

FOOT[0] = "Test et Mesure 1 – El DT 1 · 225 Simplification par Karnaugh"
TOT = "3"
FS = 22

# ---------------------------------------------------------------- tableaux : une image par étape, même cadrage dans une scène
_cache = {}


def kimg(cle, n, valeurs, groupes, termes, limites, box):
    """Image du tableau, réduite pour tenir dans box = (largeur, hauteur) ; mise en cache."""
    if cle not in _cache:
        im, _ = cei.image_karnaugh(n, valeurs, groupes, termes, fs=FS, limites=limites)
        r = min(box[0] / im.width, box[1] / im.height)
        _cache[cle] = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    return _cache[cle]


def limites(nom, groupes, termes, vals=None):
    n = FIG.FONCTIONS[nom][0]
    _, bb = cei.image_karnaugh(n, vals or FIG.valeurs(nom), groupes, termes, fs=FS, px_case=20)
    return bb


def coller(img, im, x, y, alpha=1.0):
    if alpha >= 1:
        img.paste(im, (int(x), int(y))); return
    reg = img.crop((int(x), int(y), int(x) + im.width, int(y) + im.height))
    img.paste(Image.blend(reg, im, clamp(alpha)), (int(x), int(y)))


def table(d, x, y, heads, rows, colw=90, rowh=56, size=28, show=None, actif=None):
    n = len(heads); W_ = colw * n
    rbox(d, (x, y, x + W_, y + rowh), fill=LBLUE, r=8)
    for j, h in enumerate(heads):
        text(d, (x + colw * j + colw / 2, y + rowh / 2), h, size, NAVY, True, anchor="mm")
    d.line((x + colw * (n - 1), y + 6, x + colw * (n - 1), y + rowh * (len(rows) + 1) - 6), fill=NAVY, width=3)
    for i, r in enumerate(rows):
        yy = y + rowh * (i + 1)
        d.rectangle((x, yy, x + W_, yy + rowh), fill=(255, 244, 196) if i == actif else (PALE if i % 2 == 0 else WHITE))
        if show is not None and i >= show: continue
        for j, v in enumerate(r):
            out = j == n - 1
            text(d, (x + colw * j + colw / 2, yy + rowh / 2), str(v), size, BLUE if (out and v == 1) else NAVY, out and v == 1, mono=True, anchor="mm")
    d.rectangle((x, y, x + W_, y + rowh * (len(rows) + 1)), outline=NAVY, width=3)


def over_eq(d, x, y, parts, size, color=NAVY, alpha=1.0):
    """Équation : parts = [(texte, surligné ?)]."""
    f = F(size, True); col = mix(WHITE, color, alpha)
    for p, ov in parts:
        w = f.getlength(p)
        text(d, (x, y), p, size, col, True, anchor="lm")
        if ov: d.line((x + 2, y - size * 0.62, x + w - 2, y - size * 0.62), fill=col, width=max(3, size // 14))
        x += w


# ================================================================ 1 · remplir le tableau (buse de rinçage)
RINC = FIG.valeurs("rinc")
G_RINC, T_RINC = FIG.FONCTIONS["rinc"][3], FIG.TERMES["rinc"]
LIM_RINC = None
BOX = (900, 700)
RT = 3.2            # secondes par ligne


def code_case(k):
    c, b, a = (k >> 2) & 1, (k >> 1) & 1, k & 1
    return f"ligne C = {c}, colonne BA = {b}{a}"


def s_remplir(img, d, t):
    global LIM_RINC
    chrome(img, d, "1 · REMPLIR LE TABLEAU", "Une case par ligne de la table", f"1/{TOT}")
    LIM_RINC = LIM_RINC or limites("rinc", G_RINC, T_RINC)
    k = int(clamp((t - 2) / RT, 0, 8)) if t >= 2 else -1
    nf = clamp(k + 1 if t >= 2 + 0.4 else 0, 0, 8) if t >= 2 else 0
    nf = min(8, int(clamp((t - 2 - 0.9) / RT + 1, 0, 8))) if t >= 2.9 else 0
    rows = [[(i >> 2) & 1, (i >> 1) & 1, i & 1, RINC[i]] for i in range(8)]
    table(d, 110, 210, ["C", "B", "A", "S"], rows, colw=88, rowh=66, actif=k if 0 <= k < 8 else None)
    vals = [RINC[i] if i < nf else None for i in range(8)]
    im = kimg(("rinc", nf), 3, vals, (), None, LIM_RINC, BOX)
    coller(img, im, 720, 200)
    if 0 <= k < 8:
        text(d, (110, 830), f"{(k >> 2) & 1}{(k >> 1) & 1}{k & 1}  →  {code_case(k)}", 34, BLUE, True)
    caption(d, cap_at(t, [(0, "La table de la buse de rinçage a 8 lignes : le tableau de Karnaugh a 8 cases, une par ligne."),
                          (2, "On place chaque ligne avec les codes gris : la ligne C donne la rangée, les bits B et A donnent la colonne."),
                          (2 + 3 * RT, "Attention à l'ordre des colonnes : 00, 01, 11, 10. La ligne 011 tombe dans la 3e colonne, pas dans la 4e."),
                          (2 + 6 * RT, "Les zones jaunes disent la même chose : la case 101 est dans les zones C et A, hors de la zone B.")]))


# ================================================================ 2 · regrouper et lire
def s_lire(img, d, t):
    global LIM_RINC
    chrome(img, d, "2 · REGROUPER ET LIRE", "Garder ce qui ne change pas", f"2/{TOT}")
    LIM_RINC = LIM_RINC or limites("rinc", G_RINC, T_RINC)
    ng = 0 if t < 4 else (1 if t < 15 else 2)
    im = kimg(("rinc_g", ng), 3, RINC, G_RINC[:ng], T_RINC[:ng], LIM_RINC, BOX)
    coller(img, im, 80, 200)
    X = 1060
    lignes = [(4, "Groupe vert : 4 cases", GREEN), (6, "C : à cheval  →  disparaît", NAVY), (7.5, "A : à cheval  →  disparaît", NAVY),
              (9, "B : dans la zone  →  B", NAVY),
              (15, "Groupe rouge : 2 cases", RED), (17, "C : dans la zone  →  C", NAVY), (18.5, "A : dans la zone  →  A", NAVY),
              (20, "B : à cheval  →  disparaît", NAVY)]
    for i, (t0, s, col) in enumerate(lignes):
        q = prog(t, t0, t0 + 0.8)
        if q <= 0: continue
        y = 230 + i * 58 + (30 if i >= 4 else 0)
        text(d, (X + (0 if col != NAVY else 30), y), s, 34, mix(WHITE, col, q), col != NAVY, anchor="lm")
    q = prog(t, 24, 25)
    if q > 0:
        rbox(d, (X - 20, 760, BAND_X - 60, 860), fill=mix(WHITE, TINT, q), r=16)
        over_eq(d, X + 10, 810, [("S = B + A · C", False)], 56, alpha=q)
    caption(d, cap_at(t, [(0, "On entoure les 1 par rectangles de 1, 2, 4 ou 8 cases, les plus grands possible. Un 1 peut servir deux fois."),
                          (4, "Groupe vert : C et A changent dans le groupe, ils disparaissent. Le groupe est entièrement dans la zone B : il reste B."),
                          (15, "Groupe rouge : entièrement dans les zones C et A, à cheval sur B. Il reste A · C."),
                          (24, "On additionne les termes : S = B + A · C. Cinq produits au départ, deux portes à câbler.")]))


# ================================================================ 3 · quatre variables et cas X
K4 = FIG.valeurs("k4")
G_K4, T_K4 = FIG.FONCTIONS["k4"][3], FIG.TERMES["k4"]
VID = FIG.valeurs("vid")
G_VID, T_VID = FIG.FONCTIONS["vid"][3], FIG.TERMES["vid"]
LIM = {}


def s_quatre(img, d, t):
    chrome(img, d, "3 · QUATRE VARIABLES, CAS X", "Les bords se touchent", f"3/{TOT}")
    if t < 24:
        LIM.setdefault("k4", limites("k4", G_K4, T_K4))
        ng = 0 if t < 5 else (1 if t < 13 else 2)
        im = kimg(("k4", ng), 4, K4, G_K4[:ng], T_K4[:ng], LIM["k4"], (800, 760))
        coller(img, im, 80, 190)
        q = prog(t, 18, 19)
        if q > 0:
            rbox(d, (1000, 640, BAND_X - 60, 760), fill=mix(WHITE, TINT, q), r=16)
            over_eq(d, 1030, 700, [("S = ", False), ("A", True), (" · ", False), ("C", True), (" + A · C", False)], 56, alpha=q)
        caption(d, cap_at(t, [(0, "Tableau de 16 cases : A en haut, B en bas, C à gauche, D à droite."),
                              (5, "Le haut touche le bas, la gauche touche la droite : les quatre coins forment un seul groupe, ouvert vers l'extérieur."),
                              (9, "Les coins sont hors des zones A et C, à cheval sur B et sur D : il reste Ā · C̄."),
                              (13, "Le carré du centre est dans les zones A et C : il reste A · C."),
                              (18, "B et D ont disparu des deux termes : ces deux capteurs ne servent à rien dans cette commande.")]))
    else:
        u = t - 24
        LIM.setdefault("vid", limites("vid", G_VID, T_VID))
        ng = 0 if u < 6 else (1 if u < 13 else 2)
        im = kimg(("vid", ng), 3, VID, G_VID[:ng], T_VID[:ng], LIM["vid"], (900, 620))
        coller(img, im, 80, 230)
        q = prog(u, 18, 19)
        if q > 0:
            rbox(d, (1060, 640, BAND_X - 60, 760), fill=mix(WHITE, TINT, q), r=16)
            over_eq(d, 1090, 700, [("S = C + ", False), ("A", True), (" · B", False)], 56, alpha=q)
        caption(d, cap_at(u, [(0, "Pompe de vidange : le capteur haut (C) ne peut pas être mouillé si le capteur bas (B) est sec. Ces deux cases valent X."),
                              (6, "Un X compte comme 1 s'il agrandit un groupe : avec les deux X, toute la zone C forme un groupe de 4. Il reste C."),
                              (13, "Le 1 restant s'allie à la case voisine : hors de A, dans la zone B, à cheval sur C. Il reste Ā · B."),
                              (18, "S = C + Ā · B. Sans les X, il faudrait B · C au lieu de C : un terme plus long.")]))


# ================================================================ cartes, introduction, récapitulatif
def ill_remplir(img, d, t):
    vals = [RINC[i] if i < 3 else None for i in range(8)]
    lim = LIM_RINC or limites("rinc", G_RINC, T_RINC)
    coller(img, kimg(("ill1",), 3, vals, (), None, lim, (700, 520)), 60, 340)


def ill_lire(img, d, t):
    lim = LIM_RINC or limites("rinc", G_RINC, T_RINC)
    coller(img, kimg(("ill2",), 3, RINC, G_RINC, T_RINC, lim, (700, 520)), 60, 340)


def ill_quatre(img, d, t):
    LIM.setdefault("k4", limites("k4", G_K4, T_K4))
    coller(img, kimg(("ill3",), 4, K4, G_K4[:1], T_K4[:1], LIM["k4"], (600, 600)), 110, 260)


CARDS = [
    ("1", TOT, "Remplir le tableau", "Une case par ligne de la table", ill_remplir,
     "Sur une ancienne machine de la ligne, la buse de rinçage s'ouvre pour cinq lignes de sa table de vérité.",
     "Comment reporter la table dans le tableau sans se tromper de case ?",
     "Les codes gris et les zones jaunes : chaque ligne trouve sa case.", "ligne C · colonne BA"),
    ("2", TOT, "Regrouper et lire", "Garder ce qui ne change pas", ill_lire,
     "Cinq produits : câblée telle quelle, la commande demande une douzaine de portes.",
     "Comment trouver l'équation la plus courte sans calcul ?",
     "Les groupes de 1, 2, 4 ou 8 cases, et la lecture dans / hors / à cheval.", "S = B + A · C"),
    ("3", TOT, "Quatre variables, cas X", "Les bords se touchent", ill_quatre,
     "Un collègue a branché quatre capteurs sur une commande. La pompe de vidange a des combinaisons impossibles.",
     "Que deviennent les coins du tableau, et les combinaisons qui n'arrivent jamais ?",
     "Les groupes qui passent par les bords, et les X qui agrandissent les groupes.", "S = C + Ā · B"),
]
CARD_DUR = 13.0

s_intro = intro_scene("TEST ET MESURE 1 – EL DT 1 · ANIMATION 225", "Simplification par Karnaugh",
                      "Trouver la plus courte équation en regroupant des cases",
                      [("1", "Remplir le tableau", "une case par ligne"), ("2", "Regrouper et lire", "dans, hors, à cheval"),
                       ("3", "Quatre variables, cas X", "les bords se touchent")],
                      "Va avec la présentation 220 et la fiche 230 EX")

s_outro = outro_scene(
    [("Remplir", "chaque ligne dans sa case : codes gris ou zones jaunes"), ("Regrouper", "rectangles de 1, 2, 4, 8 cases, les plus grands possible"),
     ("Lire", "dans la zone : la variable ; hors : barrée ; à cheval : elle disparaît"), ("Bords", "le haut touche le bas, la gauche touche la droite"),
     ("Cas X", "compte comme 1 s'il agrandit un groupe, sinon on l'ignore")],
    "À toi de jouer",
    [("Fiche 230 EX, N°1 et N°2", "somme de produits, remplir et lire", ""), ("Fiche 230 EX, N°3", "quatre variables", ""),
     ("Fiche 230 EX, N°4", "la pompe de vidange (cas X)", ""), ("Fiche 230 EX, N°5", "comparer avec l'algèbre", ""),
     ("Page interactive 221", "cinq exercices corrigés tout de suite", "")],
    "Chaque terme se relit en français : contrôle toujours le résultat avec la table de vérité.")

SCENES = [(s_intro, 9.0), (make_card(CARDS, 0, CARD_DUR), CARD_DUR), (s_remplir, 2 + 8 * RT + 5), (make_card(CARDS, 1, CARD_DUR), CARD_DUR),
          (s_lire, 32.0), (make_card(CARDS, 2, CARD_DUR), CARD_DUR), (s_quatre, 50.0), (s_outro, 15.0)]


def produire(ctx):
    render(SCENES, ctx.sortie_de("225"))
    from moteur import voix                       # voix off calée sur 225-narration.md (demande de Gaël, 11/24/2026)
    voix.produire(os.path.join(ICI, "225-narration.md"), ctx.sortie_de("225"))


if __name__ == "__main__":
    # aperçu d'une image : python3 contenus/tm1/semaine-2/220-karnaugh/225-anim.py <scène> <t> [image.png]
    i, t = int(sys.argv[1]), float(sys.argv[2])
    frame_at(SCENES, i, t).save(sys.argv[3] if len(sys.argv) > 3 else "apercu_225.png")
