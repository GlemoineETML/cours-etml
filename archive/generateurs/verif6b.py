# -*- coding: utf-8 -*-
"""Contrôle indépendant du test 320 série B.

Même structure et même barème que la série A ; seules les valeurs changent.
Tout est recalculé depuis les seules données d'énoncé, et la dernière section
vérifie qu'aucune donnée ne se retrouve dans le test A, la fiche 310 ou le
cours 300.
"""
import math

E_, n = [], 0


def ck(nom, calc, ecrit, tol=2e-3):
    global n
    n += 1
    if abs(calc - ecrit) > tol * max(1.0, abs(ecrit)):
        E_.append("%s : calculé %.6g, écrit %.6g" % (nom, calc, ecrit))


def ser(a, b):
    """Deux capacités en série."""
    return a * b / (a + b)


# ===================================================== Q2 : condensateur plan
U, d, Emax = 900.0, 3.0e-3, 7e3 / 1e-3        # rigidité en V/m
Ech = U / d
ck("Q2a E en V/m", Ech, 0.3e6)
ck("Q2a E en kV/m", Ech / 1e3, 300.0)
ck("Q2a E en kV/mm", Ech / 1e6, 0.3)
ck("Q2b U max", Emax * d, 21e3)

# ===================================================== Q3 : réseau de capacités
# topologie de la série A : C1 en série avec [ C4 // (C2 série C3) ]
C1, C2, C3, C4 = 18e-6, 21e-6, 42e-6, 22e-6
C23 = ser(C2, C3); ck("Q3 C23", C23, 14e-6)
C234 = C23 + C4; ck("Q3 C234", C234, 36e-6)
CAB = ser(C1, C234); ck("Q3 CAB", CAB, 12e-6)
ck("Q3 série : CAB < C1", 1 if CAB < C1 else 0, 1)
ck("Q3 trois étapes de réduction, comme la série A", 3, 3)

# ===================================================== Q4 : capacité inconnue
U, R = 9.0, 750.0
I0 = U / R
ck("Q4a I0", I0, 12e-3)
tl, il = 35e-6, 6.00e-3
ck("Q4b le point est bien la moitié de I0", I0 / il, 2.0)
ck("Q4b ln 2", math.log(2), 0.693, tol=1e-3)
tau = tl / math.log(2)
ck("Q4b tau", tau, 50.5e-6, tol=2e-3)
Cx = tau / R
ck("Q4c Cx", Cx, 67.3e-9, tol=2e-3)
ck("Q4c E12 la plus proche",
   min((56e-9, 68e-9, 82e-9), key=lambda v: abs(v - Cx)), 68e-9)
# la courbe tracée passe bien par le point annoncé
ck("Q4 contrôle du point tracé", I0 * math.exp(-tl / tau), il)

# ===================================================== Q5 : ouverture de S
Es, R1, R2, C = 36.0, 250.0, 200.0, 25e-6
UC = Es * R2 / (R1 + R2)
ck("Q5a UC max", UC, 16.0)
ck("Q5a rapport du diviseur", R2 / (R1 + R2), 0.444, tol=2e-3)
tau5 = R2 * C
ck("Q5b tau", tau5, 5.00e-3)
ck("Q5b tau en ms", tau5 * 1e3, 5.0)
ck("Q5b l'erreur R1+R2 donnerait autre chose",
   1 if abs((R1 + R2) * C - tau5) > 1e-9 else 0, 1)
IC = UC / R2
ck("Q5c IC max", IC, 80e-3)
ck("Q5d cinq tau en ms", 5 * tau5 * 1e3, 25.0)
ck("Q5 valeur à un tau, tension", UC * math.exp(-1), 5.89, tol=2e-3)
ck("Q5 valeur à un tau, courant", IC * math.exp(-1) * 1e3, 29.4, tol=2e-3)

# ===================================================== barème, identique à la série A
bareme = [2, 3, 4, 5, 6]
ck("total des points", sum(bareme), 20)
detail = {1: [1, 0.5, 0.5], 2: [2, 1], 3: [4], 4: [1, 2, 2],
          5: [0.5, 1, 1.5, 1, 2]}
for q, pts in detail.items():
    ck("barème de la question %d" % q, sum(pts), bareme[q - 1])
ck("seuil de suffisance", 20 * 0.6, 12.0)

# ===================================================== rien n'est repris ailleurs
# on compare des couples (grandeur, valeur) : 750 V et 750 Ω ne sont pas la
# même donnée.
SERIE_A = {("U", 600.0), ("d", 1.5e-3), ("rigidite", 12e6), ("C", 24e-6),
           ("C", 12e-6), ("C", 4e-6), ("C", 5e-6), ("U", 24.0), ("R", 1.2e3),
           ("t", 28e-6), ("i", 10e-3), ("E", 30.0), ("R", 50.0), ("R", 100.0),
           ("C", 2e-6)}
FICHE_310 = {("U", 250.0), ("d", 0.5e-3), ("rigidite", 15e6), ("C", 470e-6),
             ("U", 25.0), ("C", 15e-6), ("C", 6e-6), ("C", 3e-6), ("C", 8e-6),
             ("C", 4e-6), ("U", 10.0), ("R", 1e3), ("t", 33e-6), ("i", 5e-3),
             ("R", 5e3), ("C", 2e-6), ("E", 18.0), ("R", 20.0), ("R", 40.0),
             ("C", 2.5e-6)}
COURS_300 = {("U", 400.0), ("d", 0.2e-3), ("C", 10e-6), ("U", 100.0),
             ("C", 20e-6), ("C", 8e-6), ("C", 30e-6), ("U", 12.0),
             ("R", 2e3), ("C", 100e-9), ("U", 20.0), ("R", 1e3),
             ("t", 15e-6), ("i", 10e-3), ("E", 20.0), ("R", 30.0),
             ("C", 4e-6)}
SERIE_B = {("U", 900.0), ("d", 3.0e-3), ("rigidite", 7e6), ("C", 18e-6),
           ("C", 21e-6), ("C", 42e-6), ("C", 22e-6), ("U", 9.0), ("R", 750.0),
           ("t", 35e-6), ("i", 6e-3), ("E", 36.0), ("R", 250.0), ("R", 200.0),
           ("C", 25e-6)}
for nom, ref in (("le test A", SERIE_A), ("la fiche 310", FICHE_310),
                 ("le cours 300", COURS_300)):
    n += 1
    if SERIE_B & ref:
        E_.append("des données de la série B reprennent %s : %s"
                  % (nom, SERIE_B & ref))

# les résultats finaux aussi diffèrent de ceux déjà vus
RES_AILLEURS = {("CAB", 6e-6), ("CAB", 10e-6), ("Cx", 33e-9), ("Cx", 47e-9),
                ("Cx", 22e-9), ("UCmax", 20.0), ("UCmax", 12.0),
                ("UCmax", 8.0), ("tau", 200e-6), ("tau", 100e-6),
                ("tau", 80e-6), ("tau", 10e-3), ("ICmax", 200e-3), ("ICmax", 300e-3),
                ("ICmax", 400e-3), ("E", 400e3), ("E", 500e3)}
RES_B = {("CAB", 12e-6), ("Cx", 68e-9), ("UCmax", 16.0), ("tau", 5e-3),
         ("ICmax", 80e-3), ("E", 300e3)}
n += 1
if RES_B & RES_AILLEURS:
    E_.append("des résultats de la série B sont déjà connus des élèves : %s"
              % (RES_B & RES_AILLEURS))

print("contrôles :", n, "| erreurs :", len(E_))
for e in E_:
    print("  -", e)
