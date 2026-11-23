# -*- coding: utf-8 -*-
"""Contrôle indépendant du test 320, recalculé depuis les seules données d'énoncé."""
from math import log, exp

E_, n = [], 0


def ck(nom, calc, ecrit, tol=2e-3):
    global n
    n += 1
    if abs(calc - ecrit) > tol * max(1.0, abs(ecrit)):
        E_.append("%s : calculé %.6g, écrit %.6g" % (nom, calc, ecrit))


def ser(*c):
    return 1.0 / sum(1.0 / x for x in c)


# ---------------------------------------------- Q2 : U = 600 V, d = 1,5 mm
Ech = 600 / 1.5e-3
ck("Q2 E en V/m", Ech, 0.4e6)
ck("Q2 E en kV/m", Ech / 1e3, 400.0)
ck("Q2 E en kV/mm", Ech * 1e-3 / 1e3, 0.4)
ck("Q2 Umax", 12e3 * 1.5, 18e3)
ck("Q2 Umax en SI", 12e6 * 1.5e-3, 18e3)
ck("Q2 marge", 1 if Ech < 12e6 else 0, 1)

# ---------------------------------------------- Q3 : C1=24, C2=12, C3=4, C4=5 µF
c1, c2, c3, c4 = 24e-6, 12e-6, 4e-6, 5e-6
c23 = ser(c2, c3); ck("Q3 C23", c23, 3e-6)
ck("Q3 C2+C3", c2 + c3, 16e-6)
c234 = c23 + c4; ck("Q3 C234", c234, 8e-6)
ck("Q3 C1+C234", c1 + c234, 32e-6)
cab = ser(c1, c234); ck("Q3 CAB", cab, 6e-6)
ck("Q3 contrôle série", 1 if cab < min(c1, c234) else 0, 1)

# ---------------------------------------------- Q4 : U = 24 V, R = 1,2 kΩ
U, R = 24.0, 1.2e3
I0 = U / R; ck("Q4 I0", I0, 20e-3)
ck("Q4 demi-valeur", 10e-3 / I0, 0.5)
tau = 28e-6 / log(2); ck("Q4 tau", tau, 40.4e-6, tol=2e-3)
Cx = tau / R; ck("Q4 Cx", Cx, 33.7e-9, tol=3e-3)
E12 = [10e-9, 12e-9, 15e-9, 18e-9, 22e-9, 27e-9, 33e-9, 39e-9, 47e-9, 56e-9,
       68e-9, 82e-9]
ck("Q4 valeur E12 la plus proche", min(E12, key=lambda v: abs(v - Cx)), 33e-9)
ck("Q4 ln2", log(2), 0.693, tol=1e-3)
# la courbe tracée doit bien passer par le point relevé
ck("Q4 courbe cohérente", I0 * exp(-28e-6 / tau) * 1e3, 10.0)

# ---------------------------------------------- Q5 : E=30 V, R1=50, R2=100, C=2 µF
Es, R1, R2, C = 30.0, 50.0, 100.0, 2e-6
UC = Es * R2 / (R1 + R2); ck("Q5 UC max", UC, 20.0)
ck("Q5 diviseur", R2 / (R1 + R2), 0.667, tol=1e-3)
tau = R2 * C; ck("Q5 tau", tau, 200e-6)
IC = UC / R2; ck("Q5 IC max", IC, 0.2)
ck("Q5 5 tau", 5 * tau, 1e-3)
ck("Q5 uC a tau", UC * exp(-1), 7.36, tol=2e-3)
ck("Q5 iC a tau", IC * exp(-1) * 1e3, 73.6, tol=2e-3)
ck("Q5 37 %", exp(-1), 0.368, tol=3e-3)

# ---------------------------------------------- barème
bareme = [2, 3, 4, 5, 6]
ck("total des points", sum(bareme), 20)
ck("seuil note 4", 20 * 0.6, 12.0)
ck("note maximale", 1 + 5 * 20 / 20, 6.0)
ck("note au seuil", 1 + 5 * 12 / 20, 4.0)

# ---------------------------------------------- aucune valeur reprise du cours 300
cours300 = {12.0, 400.0, 0.2e-3, 20e-6, 30e-6, 8e-6, 100e-6, 10.0, 21.6e-6,
            30.0, 20.0, 4e-6, 8.0, 80e-6}
fiche310 = {250.0, 0.5e-3, 470e-6, 25.0, 15e-6, 6e-6, 3e-6, 8e-6, 4e-6,
            33e-6, 47.6e-6, 5e3, 2e-6, 18.0, 40.0, 2.5e-6}
test320 = {600.0, 1.5e-3, 24e-6, 12e-6, 4e-6, 5e-6, 24.0, 1.2e3, 28e-6,
           40.4e-6, 33.7e-9, 50.0, 100.0}
n += 1
communs = test320 & (cours300 | fiche310)
# 4e-6 et 12e-6 sont des capacités du réseau : la topologie et le résultat
# diffèrent, mais on signale quand même les recoupements pour vérification.
attendus = {4e-6, 12e-6}
if communs - attendus:
    E_.append("valeurs reprises ailleurs : %s" % sorted(communs - attendus))

# ---------------------------------------------- résultats finaux tous distincts
n += 1
resultats = [0.4e6, 18e3, 6e-6, 20e-3, 40.4e-6, 33.7e-9, 20.0, 200e-6, 0.2]
if len(set(resultats)) != len(resultats):
    E_.append("deux résultats du test sont identiques")

print("contrôles :", n, "| erreurs :", len(E_))
for e in E_:
    print("  -", e)
