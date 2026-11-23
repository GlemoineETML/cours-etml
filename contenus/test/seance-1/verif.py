# -*- coding: utf-8 -*-
"""Recalcul indépendant de la séance de test « Diviseur de tension » (REGLES 9.1), appelé par controle/controler.py.
Les calculs sont refaits ici sans passer par moteur/nombres.py ; on vérifie ensuite que la valeur arrondie est bien écrite
dans la présentation et dans le corrigé."""
import os, re

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "..", "sortie", "test", "seance-1")


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
    d = "\n".join(texte_docx(os.path.join(SORTIE, "110 EX C Diviseur de tension.docx")))
    f = os.path.join(SORTIE, "100 Diviseur de tension.pptx")
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

    # présentation : batterie 12 V, 22k / 10k
    u2 = 12 * 10 / (22 + 10); u1 = 12 * 22 / 32
    ok(f4(u2) == "3,75" and f4(u1) == "8,25" and abs(u1 + u2 - 12) < 1e-12, "100 : exemple 12 V")
    ok(abs(12 / 32e3 - 375e-6) < 1e-12, "100 : 375 µA")
    r1min = 14.4 * 10 / 5 - 10
    ok(f4(r1min) == "18,8", "100 : R1 min = 18,8 kΩ")
    ok(f4(14.4 * 10 / 32) == "4,5", "100 : 14,4 V → 4,5 V")
    ok(abs(14.4 / 32e3 - 450e-6) < 1e-12, "100 : 450 µA")
    r2l = 10 * 10 / 20; u2c = 12 * r2l / (22 + r2l)
    ok(f4(u2c) == "2,222" and f4((u2c - u2) / u2 * 100) == "−40,74", "100 : charge 10 kΩ")
    r2l = 10 * 100 / 110; u2c = 12 * r2l / (22 + r2l)
    ok(f4(r2l) == "9,091" and f4(u2c) == "3,509" and f4((u2c - u2) / u2 * 100) == "−6,433", "100 : charge 100 kΩ")
    ok(f4(0.45 * 0.45 * 32) == "6,48" or f4(14.4 ** 2 / 32) == "6,48", "100 : ticket 4, 6,48 W")
    for s in ["3,75 V", "8,25 V", "18,8 kΩ", "4,5 V", "450 µA", "2,222 V", "−40,74 %", "3,509 V", "−6,433 %", "6,48 W", "450 mA", "375 µA"]:
        cherche(pres, s, "100")

    # fiche, N°1 : 9 V, 4k7 / 2k2
    u2 = 9 * 2.2 / 6.9; i = 9 / 6.9e3; u1 = 9 * 4.7 / 6.9
    ok(abs(u1 + u2 - 9) < 1e-12 and abs(4.7e3 * i - u1) < 1e-12, "110 N°1 : loi des mailles")
    for s in [f4(u2) + " [V]", f4(i * 1e3) + " [mA]", f4(u1) + " V"]:
        cherche(doc, s, "110 N°1")
    # N°2 : 8,4 V max, 3,3 V, R2 = 10k
    r1min = 8.4 * 10 / 3.3 - 10
    e12 = [10, 12, 15, 18, 22, 27, 33]
    ok(min(r for r in e12 if r >= r1min) == 18, "110 N°2 : valeur E12")
    ok(8.4 * 10 / 28 <= 3.3, "110 N°2 : 3,3 V respectés")
    for s in [f4(r1min) + " [kΩ]", f4(8.4 * 10 / 28) + " [V]", f4(7.2 * 10 / 28) + " [V]", f4(8.4 * 18 / 28) + " V", f4(8.4 / 28e3 * 1e6) + " µA"]:
        cherche(doc, s, "110 N°2")
    # N°3 : 10 V, 10k / 10k, charges 10k et 100k
    cherche(doc, "5 [V]", "110 N°3 a")
    for rl in (10, 100):
        r2l = 10 * rl / (10 + rl); u2c = 10 * r2l / (10 + r2l)
        for s in [f4(r2l) + " kΩ", f4(u2c) + " V", f4((u2c - 5) / 5 * 100) + " %"]:
            cherche(doc, s, f"110 N°3 R_L = {rl} kΩ")
    # N°4 : multimètre 10 MΩ à la place de R2
    cherche(doc, f4(12 * 10e6 / (22e3 + 10e6)) + " V", "110 N°4 b")
    return E
