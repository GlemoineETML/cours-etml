# -*- coding: utf-8 -*-
"""Non-régression du contrôle des équations (REGLES 9.4) : cas réels de la présentation 200 (11/27/2026) qui débordaient
dans PowerPoint alors que l'ancien contrôle ne disait rien. Lancé par controle/controler.py ; aussi : python3 controle/test_equations.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from moteur.omml import omath, mesure, ajuster

# (source, corps en pt, cadre en pt (largeur, hauteur)) : débordaient avec l'ancienne taille
DEBORDAIENT = [(r"S = A \cdot B + A \cdot \bar{B} \cdot C", 20, (178, 34)),
               (r"A + A \cdot B = A \cdot (1 + B) = A \cdot 1 = A", 20, (270, 27)),
               (r"S = A + B \cdot \bar{C}", 20, (109, 30))]


def tester():
    E = []
    for src, sz, (w, h) in DEBORDAIENT:
        l = mesure(omath(src, None, 1000, "pptx"))[0] * sz
        if l <= w:
            E.append(f"la mesure ne voit plus le débordement de « {src} » à {sz} pt dans {w} pt (mesure {l:.0f} pt)")
        t = ajuster(src, None, sz * 100, w * 0.97, h) / 100
        if mesure(omath(src, None, 1000, "pptx"))[0] * t > w:
            E.append(f"l'ajustement ne fait pas tenir « {src} » dans {w} pt")
    return E


if __name__ == "__main__":
    e = tester()
    print("\n".join(e) or "test des équations : ok")
    sys.exit(1 if e else 0)
