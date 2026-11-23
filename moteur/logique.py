# -*- coding: utf-8 -*-
"""Données de cours réutilisables en logique numérique : portes de base (Floyd chap. 3, symboles CEI 60617-12),
tables de vérité, chronogrammes, niveaux des familles, brochages DIP 14.
Tables de vérité : entrées du poids fort au poids faible, puis la sortie (REGLES 3.4)."""

# clé : (nom, nom anglais, qualificatif CEI, négation en sortie, nb d'entrées, fonction, équation (mathtext), équation (OMML mini-LaTeX),
#        règle « Y = 1 si… », CI 74HC, CI 4000, contenu du CI, section Floyd, page)
GATES = {
    "NON":    ("NON", "NOT", "1", True, 1, lambda a, b=0: 1 - a, r"Y = \overline{A}", r"Y=\bar{A}",
               "Y = 1 si A = 0 : la sortie est l'inverse de l'entrée.", "74HC04", "4069", "6 inverseurs", "3-1", 112),
    "ET":     ("ET", "AND", "&", False, 2, lambda a, b: a & b, r"Y = A \cdot B", r"Y=A\cdot B",
               "Y = 1 seulement si A = 1 et B = 1.", "74HC08", "4081", "4 portes ET à 2 entrées", "3-2", 115),
    "OU":     ("OU", "OR", "≥1", False, 2, lambda a, b: a | b, r"Y = A + B", r"Y=A+B",
               "Y = 1 si au moins une entrée vaut 1.", "74HC32", "4071", "4 portes OU à 2 entrées", "3-3", 122),
    "NON-ET": ("NON-ET", "NAND", "&", True, 2, lambda a, b: 1 - (a & b), r"Y = \overline{A \cdot B}", r"Y=\bar{A\cdot B}",
               "Y = 0 seulement si A = 1 et B = 1.", "74HC00", "4011", "4 portes NON-ET à 2 entrées", "3-4", 126),
    "NON-OU": ("NON-OU", "NOR", "≥1", True, 2, lambda a, b: 1 - (a | b), r"Y = \overline{A + B}", r"Y=\bar{A+B}",
               "Y = 1 seulement si A = 0 et B = 0.", "74HC02", "4001", "4 portes NON-OU à 2 entrées", "3-5", 131),
    "OUX":    ("OU exclusif", "XOR", "=1", False, 2, lambda a, b: a ^ b, r"Y = A \oplus B", r"Y=A\oplus B",
               "Y = 1 si les deux entrées sont différentes.", "74HC86", "4070", "4 portes OU exclusif à 2 entrées", "3-6", 135),
    "NON-OUX": ("NON-OU exclusif", "XNOR", "=1", True, 2, lambda a, b: 1 - (a ^ b), r"Y = \overline{A \oplus B}", r"Y=\bar{A\oplus B}",
                "Y = 1 si les deux entrées sont égales.", "74HC7266", "4077", "4 portes NON-OU exclusif à 2 entrées", "3-6", 135),
}
ORDER = ["NON", "ET", "OU", "NON-ET", "NON-OU", "OUX", "NON-OUX"]


def tdv(key):
    """Lignes de la table de vérité, entrées du poids fort au poids faible : (B, A, Y) ; (A, Y) pour NON."""
    g = GATES[key]
    if g[4] == 1:
        return [(a, g[5](a)) for a in (0, 1)]
    return [(b, a, g[5](a, b)) for b in (0, 1) for a in (0, 1)]


TDV_HEAD = lambda n: ["A", "Y"] if n == 1 else ["B", "A", "Y"]   # en-tête : poids fort → poids faible, puis la sortie

# chronogramme standard du cours : 8 intervalles, les 4 combinaisons de A et B apparaissent deux fois
CHRONO_A = [0, 1, 0, 1, 1, 0, 1, 0]
CHRONO_B = [0, 0, 1, 1, 0, 1, 1, 0]


def chrono(key, A=CHRONO_A, B=CHRONO_B):
    f = GATES[key][5]
    return [f(a, b) for a, b in zip(A, B)]


# niveaux logiques garantis (Floyd 3-8 p. 154, VCC = 5 V ; HCT : fiche M74HCT00)
NIV = {   # famille : (VIL max, VIH min, VOL max, VOH min)
    "TTL": (0.8, 2.0, 0.4, 2.4),
    "HC":  (1.5, 3.5, 0.33, 4.4),
    "HCT": (0.8, 2.0, 0.33, 4.4),
}


def compat(src, dst):
    """Sortie de src → entrée de dst : (ok haut, ok bas, marge haute, marge basse)."""
    vil, vih = NIV[dst][0], NIV[dst][1]
    vol, voh = NIV[src][2], NIV[src][3]
    return voh >= vih, vol <= vil, round(voh - vih, 2), round(vil - vol, 2)


# brochages DIP 14, broches 1 à 14 (fiches techniques 74HC)
PINS = {
    "74HC08": ["1A", "1B", "1Y", "2A", "2B", "2Y", "GND", "3Y", "3A", "3B", "4Y", "4A", "4B", "VCC"],
    "74HC04": ["1A", "1Y", "2A", "2Y", "3A", "3Y", "GND", "4Y", "4A", "5Y", "5A", "6Y", "6A", "VCC"],
}


def pour_js():
    """Les portes sous la forme utilisée par les présentations et les pages :
    [nom, anglais, qualificatif, négation, nb entrées, règle, CI 74HC, CI 4000, contenu, section, page, (lien Floyd), tdv, chrono, équation OMML]."""
    return {k: [v[0], v[1], v[2], v[3], v[4], v[8], v[9], v[10], v[11], v[12], v[13], None, tdv(k), chrono(k), v[7]] for k, v in GATES.items()}


def pour_page():
    """Données des pages interactives (moteur/page.py, __DATA__)."""
    gates = {k: {"nom": v[0], "en": v[1], "regle": v[8], "ci74": v[9], "ci4000": v[10], "contenu": v[11], "sec": v[12], "page": v[13]}
             for k, v in GATES.items()}
    return {"GATES": gates, "ORDER": ORDER, "NIV": NIV, "CHRONO_A": CHRONO_A, "CHRONO_B": CHRONO_B}
