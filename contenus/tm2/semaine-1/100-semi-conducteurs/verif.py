# -*- coding: utf-8 -*-
"""Recalcul indépendant de la séance TM2 100 « Semi-conducteurs » (REGLES 9.1), appelé par controle/controler.py.
Les calculs sont refaits ici sans passer par moteur/nombres.py ; on vérifie ensuite que la valeur arrondie est bien écrite
dans la présentation et dans le corrigé."""
import os, re, math

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "..", "..", "sortie", "tm2", "semaine-1", "100-semi-conducteurs")


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
    d = "\n".join(texte_docx(os.path.join(SORTIE, "110 EX C Semi-conducteurs.docx")))
    f = os.path.join(SORTIE, "100 Semi-conducteurs.pptx")
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

    # présentation (notes) : ordres de grandeur cités
    ok(abs(0.0039 * 100 - 0.4) < 0.02, "100 : cuivre ≈ 0,4 % par °C")
    cherche(pres, "0,4 % par °C", "100")
    ni, n_si = 1.5e10, 5e22                     # [cm⁻³] à 300 K
    ok(2.5e12 < n_si / ni < 4e12, "100 : un électron libre pour environ 3 000 milliards d'atomes")
    cherche(pres, "3 000 milliards", "100")
    nd = 1e15                                   # dopage [cm⁻³]
    ok(abs(n_si / nd - 50e6) < 1, "100 : 1 atome pour 50 millions")
    rho_i = 1 / (1.602e-19 * ni * (1350 + 480)) / 100
    rho_n = 1 / (1.602e-19 * nd * 1350) / 100
    ok(1e4 < rho_i / rho_n < 1e5, f"100 : résistivité divisée par plusieurs dizaines de milliers (calcul : {rho_i / rho_n:.3g})")
    cherche(pres, "plusieurs dizaines de milliers", "100")

    # fiche N°1 b : X ≈ cuivre, Y ÷ 4 = 2² en 20 °C
    alpha = (10.8 - 10) / (10 * 20)
    ok(0.0035 < alpha < 0.0045, "110 N°1 b : X se comporte comme le cuivre")
    ok(1.2e3 / 300 == 4 == 2 ** (20 / 10), "110 N°1 b : Y divisée par 4 = 2²")
    # N°3
    ok(abs(0.0039 * 40 * 100 - 15.6) < 1e-9, "110 N°3 a : environ 16 %")
    cherche(doc, "environ 16 %", "110 N°3 a")
    ok(2 ** (40 / 10) == 16, "110 N°3 b : 16 fois")
    cherche(doc, "16 fois", "110 N°3 b")
    cherche(doc, f4((0.65 - 0.002 * 40) * 1e3) + " [mV]", "110 N°3 c")
    return E
