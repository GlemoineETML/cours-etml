# -*- coding: utf-8 -*-
"""Écriture des nombres (REGLES 3.1) : notation ingénieur, 4 chiffres significatifs sans zéros de fin,
virgule décimale, espace insécable, unité entre crochets dans les calculs.

ing(0.3243, "A")            → « 324,3 mA »
ing(2869.6, "Ω", crochets=True) → « 2,87 [kΩ] »
atelier(4700)               → « 4k7 » (valeur normalisée sur un schéma)
"""
import math

NB = " "
PREFIXES = {-12: "p", -9: "n", -6: "µ", -3: "m", 0: "", 3: "k", 6: "M", 9: "G"}


def chiffres(x, n=4):
    """x arrondi à n chiffres significatifs, écrit avec une virgule et sans zéros de fin."""
    if x == 0:
        return "0"
    e = math.floor(math.log10(abs(x)))
    t = f"{round(x, n - 1 - e):.{max(n - 1 - e, 0)}f}"
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t.replace(".", ",").replace("-", "−")


def ing(x, unite="", n=4, crochets=False):
    """Valeur en notation ingénieur avec préfixe (exposant multiple de 3)."""
    if x == 0:
        m, p = 0.0, 0
    else:
        p = 3 * math.floor(math.log10(abs(x)) / 3)
        m = x / 10 ** p
        if abs(float(chiffres(m, n).replace(",", ".").replace("−", "-"))) >= 1000:   # 999,96 → 1000 : préfixe suivant
            p += 3; m = x / 10 ** p
    p = max(min(p, 9), -12)
    u = PREFIXES[p] + unite
    v = chiffres(x / 10 ** p, n)
    if not u:
        return v
    return f"{v}{NB}[{u}]" if crochets else f"{v}{NB}{u}"


def atelier(r):
    """Notation atelier d'une valeur normalisée : 4700 → 4k7, 2200 → 2k2, 1.5e6 → 1M5, 100e-9 → 100n."""
    for p, s in ((6, "M"), (3, "k"), (0, "R"), (-3, "m"), (-6, "µ"), (-9, "n"), (-12, "p")):
        if abs(r) >= 10 ** p or p == -12:
            m = round(r / 10 ** p, 9)
            ent = int(m); dec = chiffres(m - ent, 3).replace("0,", "") if abs(m - ent) > 1e-9 else ""
            if s == "R" and not dec:
                return str(ent)
            return f"{ent}{s}{dec}"
    return str(r)


def ing_eq(x, unite, n=4):
    """Même valeur que ing(…, crochets=True), écrite pour une équation (moteur/omml.py) : 2,87\\u{ [V]}."""
    v = ing(x, unite, n, crochets=True)
    nombre, _, u = v.partition(NB)
    return nombre + "\\u{ " + u + "}"
