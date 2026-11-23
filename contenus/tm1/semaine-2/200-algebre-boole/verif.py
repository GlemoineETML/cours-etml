# -*- coding: utf-8 -*-
"""Recalcul indépendant de la séance 200 Algèbre de Boole (REGLES 9.1), appelé par controle/controler.py.
Chaque égalité annoncée dans la présentation et dans le corrigé est vérifiée sur toutes les combinaisons des entrées ;
les tables de vérité du corrigé sont comparées ligne à ligne ; les comptes de portes et de CI sont contrôlés."""
import itertools, os, re, zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "..", "..", "sortie", "tm1", "semaine-2", "200-algebre-boole")
NON = lambda x: 1 - x


def egal(f, g, n):
    return all(f(*v) == g(*v) for v in itertools.product((0, 1), repeat=n))


def verifier():
    E = []
    ok = lambda c, m: None if c else E.append(m)

    # lois et règles (présentation 200, fiche 210 partie A)
    ok(egal(lambda a, b: a | b, lambda a, b: b | a, 2) and egal(lambda a, b: a & b, lambda a, b: b & a, 2), "commutativité")
    ok(egal(lambda a, b, c: a | (b | c), lambda a, b, c: (a | b) | c, 3) and egal(lambda a, b, c: a & (b & c), lambda a, b, c: (a & b) & c, 3), "associativité")
    ok(egal(lambda a, b, c: a & (b | c), lambda a, b, c: (a & b) | (a & c), 3), "distributivité")
    regles = [(lambda a, b, c: a | 0, lambda a, b, c: a), (lambda a, b, c: a | 1, lambda a, b, c: 1), (lambda a, b, c: a & 0, lambda a, b, c: 0),
              (lambda a, b, c: a & 1, lambda a, b, c: a), (lambda a, b, c: a | a, lambda a, b, c: a), (lambda a, b, c: a | NON(a), lambda a, b, c: 1),
              (lambda a, b, c: a & a, lambda a, b, c: a), (lambda a, b, c: a & NON(a), lambda a, b, c: 0), (lambda a, b, c: NON(NON(a)), lambda a, b, c: a),
              (lambda a, b, c: a | (a & b), lambda a, b, c: a), (lambda a, b, c: a | (NON(a) & b), lambda a, b, c: a | b),
              (lambda a, b, c: (a | b) & (a | c), lambda a, b, c: a | (b & c))]
    for i, (f, g) in enumerate(regles, 1):
        ok(egal(f, g, 3), f"règle {i}")
    ok(egal(lambda a, b: NON(a & b), lambda a, b: NON(a) | NON(b), 2) and egal(lambda a, b: NON(a | b), lambda a, b: NON(a) & NON(b), 2), "De Morgan")

    # présentation : convoyeur, à toi, De Morgan, NON-ET universelle
    conv = lambda a, b, c: (a & b) | (a & NON(b) & c)
    ok(egal(conv, lambda a, b, c: a & (b | c), 3), "200 : convoyeur S = A·(B+C)")
    ok([c * 4 + b * 2 + a for c, b, a in itertools.product((0, 1), repeat=3) if conv(a, b, c)] == [3, 5, 7], "200 : lignes C B A = 011, 101, 111")
    ok(egal(conv, lambda a, b, c: NON(NON(a & b) & NON(a & c)), 3), "200 / 210 N°5 : NON-ET / NON-ET")
    ok(egal(lambda a, b: (a & b) | (a & NON(b)), lambda a, b: a, 2), "200 à toi 1")
    ok(egal(lambda b: NON(NON(b)) & 1 | 0, lambda b: b, 1), "200 à toi 2")
    ok(egal(lambda b, c: b | (NON(b) & c), lambda b, c: b | c, 2), "200 à toi 3")
    ok(egal(lambda a, b: NON(NON(a) & b), lambda a, b: a | NON(b), 2), "200 À toi De Morgan")
    ok(egal(lambda a, b: NON(a | b), lambda a, b: NON(a) & NON(b), 2), "200 : arrêts d'urgence")
    nand = lambda a, b: NON(a & b)
    ok(egal(lambda a: nand(a, a), lambda a: NON(a), 1), "NON en NON-ET")
    ok(egal(lambda a, b: nand(nand(a, b), nand(a, b)), lambda a, b: a & b, 2), "ET en NON-ET")
    ok(egal(lambda a, b: nand(nand(a, a), nand(b, b)), lambda a, b: a | b, 2), "OU en NON-ET")

    # fiche 210, partie B
    ok(egal(lambda a: a & 1 | 0, lambda a: a, 1), "N°2 a")
    ok(egal(lambda c: (c & NON(c)) | c, lambda c: c, 1), "N°2 b")
    ok(egal(lambda a, b: (NON(a) & b) | (NON(a) & NON(b)), lambda a, b: NON(a), 2), "N°2 c")
    ok(egal(lambda b, c: b | (b & c), lambda b, c: b, 2), "N°2 d")
    ok(egal(lambda b, c: NON(b) | (b & c), lambda b, c: NON(b) | c, 2), "N°2 e")
    ok(egal(lambda a, b, c: (a | b) & (a | NON(c)), lambda a, b, c: a | (b & NON(c)), 3), "N°2 f")
    ok(egal(lambda a, b, c: NON(a & b & c), lambda a, b, c: NON(a) | NON(b) | NON(c), 3), "N°3 a")
    ok(egal(lambda a, b: NON(NON(a) | b), lambda a, b: a & NON(b), 2), "N°3 b")
    ok(egal(lambda a, b: NON(NON(a) & NON(b)), lambda a, b: a | b, 2), "N°3 c")
    ok(egal(lambda x, y, z: NON(x) & NON(y) & NON(z), lambda x, y, z: NON(x | y | z), 3), "N°3 d")
    h = lambda a, b, c: (a & NON(b)) | (a & b & NON(c))
    ok(egal(h, lambda a, b, c: a & (NON(b) | (b & NON(c))), 3), "N°4 c étape 1")
    ok(egal(h, lambda a, b, c: a & (NON(b) | NON(c)), 3), "N°4 c étape 2")
    ok(egal(h, lambda a, b, c: a & NON(b & c), 3), "N°4 c étape 3")
    ok([c * 4 + b * 2 + a for c, b, a in itertools.product((0, 1), repeat=3) if h(a, b, c)] == [1, 3, 5], "N°4 d : lignes C B A = 001, 011, 101")
    ok(egal(h, lambda a, b, c: nand(nand(a, nand(b, c)), nand(a, nand(b, c))), 3), "N°4 f : trois NON-ET")

    # le corrigé contient bien les tables calculées (N°1 et N°4) : lecture des cellules rouges
    f = os.path.join(SORTIE, "210 EX C Algèbre de Boole.docx")
    if os.path.exists(f):
        x = zipfile.ZipFile(f).read("word/document.xml").decode("utf-8")
        tables = re.findall(r"<w:tbl>.*?</w:tbl>", x, flags=re.S)
        def lignes(t):
            return [[ "".join(re.findall(r"<[wm]:t(?: [^>]*)?>([^<]*)</[wm]:t>", c)) for c in re.findall(r"<w:tc>.*?</w:tc>", r, flags=re.S)]
                    for r in re.findall(r"<w:tr[ >].*?</w:tr>", t, flags=re.S)]
        t1 = next((lignes(t) for t in tables if "A+C" in "".join(lignes(t)[0]) if lignes(t)), None)
        ok(t1 is not None and len(t1) == 9, "210 N°1 : table introuvable")
        if t1:
            for row in t1[1:]:
                c, b, a = map(int, row[:3])
                att = [a | b, a | c, (a | b) & (a | c), b & c, a | (b & c)]
                ok([int(v) for v in row[3:]] == att, f"210 N°1 : ligne {c}{b}{a}")
        t4 = next((lignes(t) for t in tables if lignes(t) and lignes(t)[0][3:4] == ["S (équation a)"]), None)
        ok(t4 is not None and len(t4) == 9, "210 N°4 : table introuvable")
        if t4:
            for row in t4[1:]:
                c, b, a = map(int, row[:3])
                ok([int(row[3]), int(row[4])] == [h(a, b, c), a & NON(b & c)], f"210 N°4 : ligne {c}{b}{a}")
    else:
        E.append("corrigé 210 EX C absent : lancer build.py avant le contrôle")
    return E
