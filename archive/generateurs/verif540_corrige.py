# Double contrôle : chaque valeur AFFICHÉE dans le corrigé, recalculée
# (a) en exact, (b) avec les valeurs arrondies que l'élève reporte d'une étape à l'autre.
from math import exp, log
ok = True
def chk(nom, affiche, exact, tol_rel=6e-4):
    global ok
    e = abs(affiche-exact)/abs(exact)
    flag = "OK " if e <= tol_rel else "ERR"
    if flag == "ERR": ok = False
    print(f"{flag} {nom:38s} affiché {affiche:<10g} calculé {exact:.6g}")
print("— N°1 —")
chk("tau [ms]", 3.3, 1.5e3*2.2e-6*1e3)
chk("e^(-7,999/3,3)", 0.08857, exp(-7.999/3.3))
chk("us(t1) [V]", 1.329, 15*exp(-7.999/3.3))
chk("us(t2) arrondi élève [V]", -13.67, 1.329-15)
chk("us(t2) exact à 8,001 ms [V]", -13.67, (15*exp(-8/3.3)-15)*exp(-0.001/3.3))
chk("ln(13,67/0,2)", 4.225, log(13.67/0.2))
chk("dt [ms]", 13.94, 3.3*4.225)
chk("dt exact [ms]", 13.94, 3.3*log((15-15*exp(-8/3.3))/0.2), 1e-3)
chk("t3 [ms]", 21.94, 8+13.94)
chk("t3 exact (sim) [ms]", 21.94, 21.9416)
print("— N°2 —")
chk("tau [ms]", 2.679, 0.15/56*1e3)
chk("I [mA]", 357.1, 20/56*1e3)
chk("5 tau [ms]", 13.4, 5*0.15/56*1e3, 3e-3)
chk("1-e^(-6/2,679)", 0.8935, 1-exp(-6/2.679))
chk("i(6 ms) élève [mA]", 319.1, 357.1*0.8935)
chk("i(6 ms) exact [mA]", 319.1, 20/56*(1-exp(-6/(0.15/56*1e3)))*1e3)
chk("us max élève [V]", 17.87, 56*319.1e-3)
chk("us max exact [V]", 17.87, 20*(1-exp(-6*56/150)))
chk("tau requis [ms]", 1.2, 6/5)
chk("R requis [ohm]", 125, 0.15/1.2e-3)
chk("us(6 ms) R=125 [V]", 19.87, 20*(1-exp(-5)))
chk("pourcentage", 99.3, 100*(1-exp(-5)))
chk("tau R=150 [ms]", 1.0, 0.15/150*1e3)
chk("5tau R=120 [ms]", 6.25, 5*0.15/120*1e3)
chk("63 % de 20 V", 12.6, 20*(1-exp(-1)), 3e-3)
chk("fin descente 6+5tau [ms]", 19.4, 6+5*0.15/56*1e3, 3e-3)
print("— barème —")
n1 = [1,1,2,2,2,2]; n2 = [2,3,2,1,2]
print("N°1", sum(n1), "N°2", sum(n2), "total", sum(n1)+sum(n2), "seuil note 4 :", (4-1)/5*20)
print("TOUT JUSTE" if ok else "ERREUR(S)")
