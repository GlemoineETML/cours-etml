# -*- coding: utf-8 -*-
"""Contrôle indépendant de toutes les valeurs du chapitre 500 / fiche 510.
Tout est recalculé depuis les seules données d'énoncé."""
E_, n = [], 0


def ck(nom, calc, ecrit, tol=2e-3):
    global n
    n += 1
    if abs(calc - ecrit) > tol * max(1.0, abs(ecrit)):
        E_.append("%s : calculé %.6g, écrit %.6g" % (nom, calc, ecrit))


def par(a, b):
    return a * b / (a + b)


def ecart(mes, vrai):
    return (mes - vrai) / vrai * 100


# ===================================================== COURS
# — sensibilité analogique : 20 kΩ/V (diapo 20)
ck("cours RV calibre 10 V", 20e3 * 10, 200e3)
ck("cours RV calibre 3 V", 20e3 * 3, 60e3)
ck("cours facteur 50", 10e6 / 200e3, 50)

# — exemple du voltmètre : U = 10 V, R1 = R2 = 5 MΩ, voltmètre numérique 10 MΩ
U, R1, R2, RV = 10.0, 5e6, 5e6, 10e6
ck("cours U2 vraie", U * R2 / (R1 + R2), 5.00)
R2V = par(R2, RV); ck("cours R2V", R2V, 3.33e6, tol=2e-3)
Um = U * R2V / (R1 + R2V); ck("cours U mesurée", Um, 4.00)
ck("cours U1", U - Um, 6.00)
ck("cours écart voltmètre", ecart(Um, 5.00), -20.0)
I1 = U / (R1 + R2V); ck("cours I1 avec voltmètre", I1, 1.20e-6, tol=2e-3)
ck("cours I1 sans voltmètre", U / (R1 + R2), 1.00e-6)
I2 = Um / R2; ck("cours I2", I2, 0.80e-6, tol=2e-3)
IV = Um / RV; ck("cours IV", IV, 0.40e-6, tol=2e-3)
ck("cours loi des nœuds", I2 + IV, I1)
ck("cours U1 + U2", (U - Um) + Um, 10.0)

# — la règle du voltmètre (diapo 10)
ck("règle R 10 kΩ", 100 * 10e3, 1e6)
ck("règle R 100 kΩ", 100 * 100e3, 10e6)
ck("règle R 5 MΩ", 100 * 5e6, 500e6)
ck("règle non tenue par 10 MΩ", 1 if 10e6 < 500e6 else 0, 1)

# — exemple de l'ampèremètre : U = 10 V, R = 180 Ω, RA = 20 Ω
U, R, RA = 10.0, 180.0, 20.0
Iv = U / R; ck("cours I vrai", Iv, 55.6e-3, tol=2e-3)
Im = U / (R + RA); ck("cours I mesuré", Im, 50e-3)
ck("cours écart courant", ecart(Im, Iv), -10.0)
UA = RA * Im; ck("cours UA", UA, 1.00)
UR = R * Im; ck("cours UR", UR, 9.00)
ck("cours loi des mailles", UA + UR, U)

# — à toi, 3 minutes : diviseur 470 kΩ / 470 kΩ sous 20 V
ck("à toi U vraie", 20 * 470e3 / 940e3, 10.0)
ck("à toi règle", 100 * 470e3, 47e6)
ck("à toi règle non respectée", 1 if 10e6 < 47e6 else 0, 1)

# — ohmmètre du cours : 12 kΩ en place, reste 4 kΩ
ck("cours R lue", par(12e3, 4e3), 3e3)
ck("cours écart ohmmètre", ecart(3.0, 12.0), -75.0)

# — précision : Fluke 87, fiche ETML (Users Manual 80 Series V, Table 12)
# échelle 6,000 V → résolution 0,001 V ; 60,00 V → 0,01 V ; V continu ±(0,05 % + 1)
ck("résolution de l'échelle 6 V", 6.000 / 6000, 0.001)
ck("résolution de l'échelle 60 V", 60.00 / 6000, 0.010)

# l'exemple de la fiche ETML : U_lue = 9,56 V sur l'échelle 60,00 V
dE = 0.0005 * 9.56 + 1 * 0.01
ck("exemple ETML terme en %", 0.0005 * 9.56, 4.78e-3, tol=2e-3)
ck("exemple ETML terme résolution", 1 * 0.01, 10e-3)
ck("exemple ETML précision", dE, 14.78e-3, tol=2e-3)
ck("exemple ETML borne basse", 9.56 - 0.015, 9.545)
ck("exemple ETML borne haute", 9.56 + 0.015, 9.575)
ck("exemple ETML : 60 V est la plus petite échelle qui contient 9,56 V",
   1 if 6.000 < 9.56 <= 60.00 else 0, 1)

# la même méthode sur notre mesure de 4,00 V, échelle 6,000 V
d6 = 0.0005 * 4.000 + 1 * 0.001
ck("Fluke 87 échelle 6 V", d6, 0.003)
ck("Fluke 87 échelle 6 V en %", d6 / 4.00 * 100, 0.075, tol=1e-2)
d60 = 0.0005 * 4.00 + 1 * 0.010
ck("Fluke 87 échelle 60 V", d60, 0.012)
ck("Fluke 87 échelle 60 V en %", d60 / 4.00 * 100, 0.30, tol=1e-2)
ck("l'échelle 6 V est 4 fois meilleure", d60 / d6, 4.0)

# — l'analogique, pour la comparaison de la diapositive 20
ck("analogique RV calibre 10 V", 20e3 * 10, 200e3)
ck("analogique classe 1,5 calibre 10 V", 0.015 * 10, 0.15)
ck("analogique en % sur 4,00 V", 0.015 * 10 / 4.00 * 100, 3.75)
ck("le numérique est 50 fois plus précis", (0.015 * 10 / 4.00) / (d6 / 4.00), 50.0)

# — précision n'est pas influence
ck("rapport influence / précision", 20.0 / (d6 / 4.00 * 100), 266.7, tol=5e-3)
ck("précision ≪ influence", 1 if d6 / 4.00 * 100 < abs(-20.0) else 0, 1)

# ===================================================== FICHE 510
# — N°1 : U = 24 V, R1 = 330 Ω, R2 = 470 Ω
U, R1, R2 = 24.0, 330.0, 470.0
ck("ex1 somme", R1 + R2, 800.0)
I = U / (R1 + R2); ck("ex1 I", I, 30e-3)
ck("ex1 U2", R2 * I, 14.1)

# — N°2 : jusqu'où le Fluke 87 (10 MΩ) tient la règle RV >= 100 R
ck("ex2 règle sur 10 kΩ", 100 * 10e3, 1e6)
ck("ex2 règle tenue", 1 if 100 * 10e3 <= 10e6 else 0, 1)
ck("ex2 règle sur 220 kΩ", 100 * 220e3, 22e6)
ck("ex2 règle non tenue", 1 if 100 * 220e3 > 10e6 else 0, 1)
ck("ex2 R maximale", 10e6 / 100, 100e3)

# — N°3 : U = 18 V, R1 = 2 MΩ, R2 = 2,5 MΩ, voltmètre numérique 10 MΩ
U, R1, R2, RV = 18.0, 2e6, 2.5e6, 10e6
U2 = U * R2 / (R1 + R2); ck("ex3 U2 vraie", U2, 10.00)
R2V = par(R2, RV); ck("ex3 R2V", R2V, 2.00e6)
Um = U * R2V / (R1 + R2V); ck("ex3 U mesurée", Um, 9.00)
ck("ex3 écart", ecart(Um, U2), -10.0)
I1 = U / (R1 + R2V); ck("ex3 I1", I1, 4.5e-6, tol=2e-3)
I2 = Um / R2; ck("ex3 I2", I2, 3.6e-6, tol=2e-3)
IV = Um / RV; ck("ex3 IV", IV, 0.9e-6, tol=2e-3)
ck("ex3 loi des nœuds", I2 + IV, I1)
ck("ex3 règle", 100 * 2.5e6, 250e6)
ck("ex3 règle non respectée", 1 if 10e6 < 250e6 else 0, 1)

# — N°4 : U = 12 V, R = 470 Ω, RA = 30 Ω
U, R, RA = 12.0, 470.0, 30.0
Iv = U / R; ck("ex4 I vrai", Iv, 25.53e-3, tol=1e-3)
Im = U / (R + RA); ck("ex4 I mesuré", Im, 24.0e-3)
UA = RA * Im; ck("ex4 UA", UA, 0.72)
UR = R * Im; ck("ex4 UR", UR, 11.28)
ck("ex4 loi des mailles", UA + UR, U)
ck("ex4 écart", ecart(Im, Iv), -6.0, tol=5e-3)
ck("ex4 règle RA", R / 100, 4.7)

# — N°5 : Rx = 22 kΩ, reste 33 kΩ
ck("ex5 R lue", par(22e3, 33e3), 13.2e3)
ck("ex5 écart", ecart(13.2, 22.0), -40.0)

# — N°6 : Fluke 87, ±(0,05 % + 1), lecture de 2,000 V sur deux échelles
e6 = 0.0005 * 2.000 + 1 * 0.001
ck("ex6 précision échelle 6 V", e6, 0.002)
ck("ex6 % échelle 6 V", e6 / 2.00 * 100, 0.10)
ck("ex6 bornes échelle 6 V", 2.000 - e6, 1.998)
ck("ex6 borne haute échelle 6 V", 2.000 + e6, 2.002)
e60 = 0.0005 * 2.00 + 1 * 0.010
ck("ex6 précision échelle 60 V", e60, 0.011)
ck("ex6 % échelle 60 V", e60 / 2.00 * 100, 0.55)
ck("ex6 bornes échelle 60 V", 2.000 - e60, 1.989)
ck("ex6 borne haute échelle 60 V", 2.000 + e60, 2.011)
ck("ex6 rapport des deux échelles", e60 / e6, 5.5)
ck("ex6 lecture distincte du cours", 1 if 2.000 != 4.000 else 0, 1)

# ===================================================== cohérences transverses
# le sens de l'erreur est toujours négatif : un appareil ne peut que faire baisser
for nom, val in (("cours volt", -20.0), ("cours amp", -10.0),
                 ("cours ohm", -75.0), ("ex3", -10.0), ("ex4", -6.0),
                 ("ex5", -40.0)):
    n += 1
    if val >= 0:
        E_.append("%s : l'écart devrait être négatif" % nom)

# aucune valeur de circuit de la fiche ne reprend une valeur du cours
# (le voltmètre numérique de 10 MΩ est volontairement le même des deux côtés :
#  c'est l'appareil du labo, pas une donnée d'énoncé)
cours = {5e6, 10.0, 180.0, 20.0, 20e3, 12e3, 4e3, 470e3, 4.000}
fiche = {330.0, 470.0, 2e6, 2.5e6, 18.0, 24.0, 30.0, 22e3, 33e3, 220e3,
         2.000}
n += 1
if cours & fiche:
    E_.append("des valeurs de la fiche reprennent celles du cours : %s"
              % (cours & fiche))

print("contrôles :", n, "| erreurs :", len(E_))
for e in E_:
    print("  -", e)
