# -*- coding: utf-8 -*-
"""Contrôle indépendant des valeurs numériques du questionnaire 140."""
def par(*r):
    return 1.0 / sum(1.0 / x for x in r)

E, n = [], 0
def ck(nom, calc, ecrit):
    global n
    n += 1
    if abs(calc - ecrit) > 1e-9 * max(1.0, abs(ecrit)):
        E.append("%s : calculé %.6g, écrit %.6g" % (nom, calc, ecrit))

ck("noeud", 180e-3 - 110e-3, 70e-3)
ck("maille", 30 - 12 - 6, 12)
ck("100 // 400", par(100.0, 400.0), 80.0)
ck("trois fois 600 en parallele", par(600.0, 600.0, 600.0), 200.0)
ck("330 // 660", par(330.0, 660.0), 220.0)
ck("220 + (330 // 660)", 220 + par(330.0, 660.0), 440.0)
ck("24 V / 480 ohms", 24 / 480.0, 50e-3)
ck("12 V / 300 ohms", 12 / 300.0, 40e-3)
ck("150 ohms sous 40 mA", 150 * 0.040 ** 2, 240e-3)
# les distracteurs ne doivent jamais coincider avec la bonne reponse
ck("distracteur 100//400", 1 if 500.0 != 80.0 and 250.0 != 80.0 and 125.0 != 80.0 else 0, 1)
ck("distracteur 600 x3", 1 if 1800.0 != 200.0 and 300.0 != 200.0 and 600.0 != 200.0 else 0, 1)
ck("distracteur 220+groupe", 1 if 1210.0 != 440.0 and 330.0 != 440.0 and 550.0 != 440.0 else 0, 1)
ck("distracteur courant", 1 if 20e-3 != 50e-3 and 0.5 != 50e-3 and 5e-3 != 50e-3 else 0, 1)
ck("distracteur branche", 1 if 25e-3 != 40e-3 and 3.6 != 40e-3 and 400e-3 != 40e-3 else 0, 1)
ck("distracteur puissance", 1 if 6.0 != 240e-3 and 60e-3 != 240e-3 and 24e-3 != 240e-3 else 0, 1)
print("contrôles :", n, "| erreurs :", len(E))
for e in E:
    print("  -", e)
