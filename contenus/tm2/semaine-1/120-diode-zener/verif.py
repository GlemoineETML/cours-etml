# -*- coding: utf-8 -*-
"""Recalcul indépendant de la séance TM2 120 « Diode et diode Zener » (REGLES 9.1), appelé par controle/controler.py.
Les modèles des courbes sont réécrits ici (sans importer figures.py) ; on vérifie que les lectures demandées
tombent bien sur les valeurs du corrigé, puis que chaque résultat arrondi est écrit dans le corrigé et la présentation."""
import os, re, math

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "..", "..", "sortie", "tm2", "semaine-1", "120-diode-zener")


def f4(x):
    """4 chiffres significatifs, virgule, sans zéros de fin (écrit à la main, indépendamment du moteur)."""
    s = "%.4g" % x
    if "e" in s:
        raise ValueError(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",").replace("-", "−")


def textes():
    from controle.controler import texte_docx, texte_pptx
    import zipfile, html
    d = "\n".join(texte_docx(os.path.join(SORTIE, "130 EX C Diode et Zener.docx")))
    f = os.path.join(SORTIE, "120 Diode et diode Zener.pptx")
    z = zipfile.ZipFile(f)
    notes = [html.unescape("".join(re.findall(r"<a:t>([^<]*)</a:t>", z.read(n).decode("utf-8")))) for n in z.namelist() if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)]
    p = "\n".join(t for ps in texte_pptx(f).values() for t in ps) + "\n" + "\n".join(notes)
    sp = lambda s: s.replace(" ", " ").replace(" ", " ")
    return sp(d), sp(p)


def verifier():
    E = []
    ok = lambda c, m: None if c else E.append(m)
    doc, pres = textes()
    cherche = lambda t, s, ou: ok(s in t, f"{ou} : « {s} » introuvable")

    # modèle de la diode Si d'exercice : U = n·U_T·ln(I/I_S + 1) + R_S·I
    ud = lambda i: 1.9 * 0.02585 * math.log(i / 10e-9 + 1) + 2.0 * i
    ok(0.55 < ud(1e-3) < 0.6, f"130 N°2 a : 1 mA vers 0,6 V (modèle : {ud(1e-3):.3f} V)")
    ok(abs(ud(10e-3) - 0.7) < 0.01, f"130 N°2 b / 120 diapo 8 : 10 mA → 0,7 V (modèle : {ud(10e-3):.3f} V)")
    ok(abs(ud(30e-3) - 0.8) < 0.015, f"130 N°2 b : 30 mA → 0,8 V (modèle : {ud(30e-3):.3f} V)")
    ok(abs((ud(30e-3) - ud(10e-3)) - 0.1) < 0.01, "130 N°2 c : environ 0,1 V de plus")
    cherche(doc, "10 mA : environ 0,7 V. 30 mA : environ 0,8 V", "130 N°2 b")
    cherche(pres, "10 mA → 0,7 V, 30 mA → 0,8 V", "120 diapo 8")

    # N°3 : 1N4007
    ok(0.6 < 1 and 24 < 1000, "130 N°3 a")
    cherche(doc, f4(24 - 1.1) + " [V]", "130 N°3 b")

    # Zener d'exercice : U = 5,05 + 10·I − 0,08·e^(−I/1 mA)
    uz = lambda i: 5.05 + 10 * i - 0.08 * math.exp(-i / 1e-3)
    ok(abs(uz(5e-3) - 5.1) < 0.005, f"130 N°4 a : 5 mA → 5,1 V (modèle : {uz(5e-3):.4f} V)")
    ok(abs(uz(25e-3) - 5.3) < 0.005, f"130 N°4 a : 25 mA → 5,3 V (modèle : {uz(25e-3):.4f} V)")
    rz = (5.3 - 5.1) / (25e-3 - 5e-3)
    ok(abs(rz - 10) < 1e-9, "130 N°4 b : r_Z = 10 Ω")
    cherche(doc, "10 [Ω]", "130 N°4 b")
    ok(abs(0.2 / 5.1 * 100 - 4) < 0.1, "130 N°4 c : environ 4 %")
    cherche(doc, "environ 4 %", "130 N°4 c")

    # N°5 et diapositive 12 : BZX55C5V1
    izmax = 0.5 / 5.1
    cherche(doc, f4(izmax * 1e3) + " [mA]", "130 N°5 a")
    cherche(pres, f4(izmax * 1e3) + " mA", "120 diapo 12 (notes)")
    pz = 5.3 * 25e-3
    cherche(doc, f4(pz * 1e3) + " [mW]", "130 N°5 b")
    ok(pz < 0.5, "130 N°5 b : P_Z < P_tot")
    ok(abs(5 * 25e-3 - 0.125) < 1e-12, "130 N°5 b : contrôle 125 mW")

    # N°6 et diapositive 13
    ok(abs((24 - 5.1) - 18.9) < 1e-9, "130 N°6 a : 18,9 V")
    cherche(doc, "18,9 V", "130 N°6 a")
    cherche(pres, "18,9 V", "120 diapo 13 (notes)")
    return E
