# -*- coding: utf-8 -*-
"""Contrôle indépendant de toutes les valeurs du chapitre 300 / 310.
Recalcul depuis les données de l'énoncé, sans réutiliser les résultats écrits."""
from math import log, exp

E_, n = [], 0


def ck(nom, calc, ecrit, tol=2e-3):
    global n
    n += 1
    if abs(calc - ecrit) > tol * max(1.0, abs(ecrit)):
        E_.append("%s : calculé %.6g, écrit %.6g" % (nom, calc, ecrit))


def ser(*c):
    return 1.0 / sum(1.0 / x for x in c)


# ===================================================== COURS
# — exemple 1 : Q = I·t
ck("cours Q", 250e-3 * 2 * 3600, 1.8e3)
ck("cours 2h en s", 2 * 3600, 7.2e3)
ck("cours mAh", 3000e-3 * 3600, 1.08e4, tol=2e-2)

# — exemple 2 : champ
ck("cours E", 400 / 0.2e-3, 2e6)
ck("cours claquage 0,1 mm", 400 / 0.1e-3, 4e6)

# — énergie
ck("cours W", 0.5 * 10e-6 * 100 ** 2, 50e-3)

# — groupements de la figure
ck("fig parallele", 20e-6 + 30e-6, 50e-6)
ck("fig serie", ser(20e-6, 30e-6), 12e-6)

# — exemple 3 : reseau C1..C4
C1, C2, C3, C4 = 20e-6, 30e-6, 8e-6, 20e-6
C12 = ser(C1, C2); ck("cours C12", C12, 12e-6)
C123 = C12 + C3; ck("cours C123", C123, 20e-6)
CAB = ser(C4, C123); ck("cours CAB", CAB, 10e-6)
ck("cours CAB < plus petite serie", 1 if CAB < min(C4, C123) else 0, 1)

# — charge : E=12 V, R=2 kΩ, C=100 nF
tau = 2e3 * 100e-9; ck("cours tau charge", tau, 200e-6)
ck("cours I0 charge", 12 / 2e3, 6e-3)
ck("cours 63 %", 1 - exp(-1), 0.632, tol=1e-3)
ck("cours 37 %", exp(-1), 0.368, tol=2e-3)
for k, v in ((1, 63.2), (2, 86.5), (3, 95.0), (4, 98.2), (5, 99.3)):
    ck("cours %d tau" % k, (1 - exp(-k)) * 100, v, tol=1e-3)

# — exemple 4 : lecture inverse, U=20 V, R=1 kΩ, point (15 µs ; 10 mA)
I0 = 20 / 1e3; ck("cours I0 lecture", I0, 20e-3)
ck("cours demi-valeur", 10e-3 / I0, 0.5)
tau = 15e-6 / log(2); ck("cours tau lecture", tau, 21.6e-6, tol=3e-3)
ck("cours Cx", tau / 1e3, 21.6e-9, tol=3e-3)
ck("cours ln2", log(2), 0.693, tol=1e-3)

# — exemple 5 : E=20 V, R1=30, R2=20, C=4 µF
UC = 20 * 20 / (30 + 20); ck("cours UCmax", UC, 8.0)
ck("cours diviseur", 20 / 50, 0.4)
tau = 20 * 4e-6; ck("cours tau decharge", tau, 80e-6)
ck("cours ICmax", UC / 20, 0.4)
ck("cours 5tau", 5 * tau, 400e-6)
ck("cours uC(tau) decharge", UC * exp(-1), 2.94, tol=3e-3)
ck("cours iC(tau) decharge", UC / 20 * exp(-1) * 1e3, 147, tol=3e-3)

# ===================================================== FICHE 310
# — N°2 : U=250 V, d=0,5 mm
ck("ex2 E", 250 / 0.5e-3, 0.5e6)
ck("ex2 E kV/mm", 250 / 0.5e-3 / 1e6, 0.5)
ck("ex2 Umax", 15e3 * 0.5, 7.5e3)

# — N°3 : C=470 µF, U=25 V
Q = 470e-6 * 25; ck("ex3 Q", Q, 11.75e-3)
ck("ex3 W", 0.5 * 470e-6 * 25 ** 2, 146.9e-3, tol=1e-3)
ck("ex3 U carre", 25 ** 2, 625)
ck("ex3 t", Q / 5e-3, 2.35)

# — N°4 : C1=15, C2=6, C3=3, C4=8, C5=4 µF
c1, c2, c3, c4, c5 = 15e-6, 6e-6, 3e-6, 8e-6, 4e-6
c23 = ser(c2, c3); ck("ex4 C23", c23, 2e-6)
ck("ex4 C2+C3", c2 + c3, 9e-6)
c234 = c23 + c4; ck("ex4 C234", c234, 10e-6)
c1234 = ser(c1, c234); ck("ex4 C1234", c1234, 6e-6)
ck("ex4 C1+C234", c1 + c234, 25e-6)
cab = c1234 + c5; ck("ex4 CAB", cab, 10e-6)
ck("ex4 CAB >= C5", 1 if cab >= c5 else 0, 1)

# — N°5 : U=10 V, R=1 kΩ, point (33 µs ; 5 mA)
i0 = 10 / 1e3; ck("ex5 I0", i0, 10e-3)
ck("ex5 rapport", 5e-3 / i0, 0.5)
tau = 33e-6 / log(2); ck("ex5 tau", tau, 47.6e-6, tol=3e-3)
cx = tau / 1e3; ck("ex5 Cx", cx, 47.6e-9, tol=3e-3)
ck("ex5 E12", min([10e-9, 22e-9, 33e-9, 47e-9, 68e-9, 100e-9],
                  key=lambda v: abs(v - cx)), 47e-9)

# — N°6 : E=10 V, R=5 kΩ, C=2 µF
tau = 5e3 * 2e-6; ck("ex6 tau", tau, 10e-3)
ck("ex6 I0", 10 / 5e3, 2e-3)
ck("ex6 uC(tau)", 10 * (1 - exp(-1)), 6.32, tol=1e-3)
t5 = tau * log(2); ck("ex6 t pour 5 V", t5, 6.93e-3, tol=2e-3)
ck("ex6 verif 5 V", 10 * (1 - exp(-t5 / tau)), 5.0)
ck("ex6 5tau", 5 * tau, 50e-3)

# — N°7 : E=18 V, R1=20, R2=40, C=2,5 µF
UC = 18 * 40 / (20 + 40); ck("ex7 UCmax", UC, 12.0)
ck("ex7 diviseur", 40 / 60, 0.667, tol=1e-3)
tau = 40 * 2.5e-6; ck("ex7 tau", tau, 100e-6)
ck("ex7 ICmax", UC / 40, 0.3)
ck("ex7 5tau", 5 * tau, 500e-6)
ck("ex7 uC(tau) arrondi", round(UC * exp(-1), 1), 4.4)
ck("ex7 iC(tau) arrondi", round(UC / 40 * exp(-1) * 1e3), 110)

# ===================================================== TEST EN ANNEXE (couverture)
# Q2 du test : C6=60, C4=40, C3=30, C1=10 (mF)
t23 = ser(40e-3, 30e-3)
ck("test Q2 CAB", 60e-3 + 10e-3 + t23, 87.14e-3, tol=1e-3)
# Q3 du test : U=15 V, R=500 Ω, point (25 µs ; 15 mA)
ti0 = 15 / 500; ck("test Q3 I0", ti0, 30e-3)
ttau = 25e-6 / log(2); ck("test Q3 tau", ttau, 36.07e-6, tol=2e-3)
ck("test Q3 Cx", ttau / 500, 72.1e-9, tol=2e-3)
# Q4 du test : E=15 V, R1=10, R2=5, C=2 µF
tuc = 15 * 5 / 15; ck("test Q4 UCmax", tuc, 5.0)
ck("test Q4 tau", 5 * 2e-6, 10e-6)
ck("test Q4 ICmax", tuc / 5, 1.0)

# ===================================================== valeurs distinctes du test
paires = [("champ", 250 / 0.5e-3, 0.0), ]
distinct = [(0.5e-3, 2e-6), (1e3, 500.0), (10.0, 15.0), (18.0, 15.0),
            (40.0, 5.0), (2.5e-6, 2e-6)]
n += 1
if any(a == b for a, b in distinct):
    E_.append("des valeurs de la fiche coïncident avec celles du test")

print("contrôles :", n, "| erreurs :", len(E_))
for e in E_:
    print("  -", e)
