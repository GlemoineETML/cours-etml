# -*- coding: utf-8 -*-
"""Recalcul indépendant de la séance 220 Simplification par Karnaugh (REGLES 9.1), appelé par controle/controler.py.
Pour chaque tableau : les fonctions sont réécrites ici à partir des équations annoncées (présentation, corrigé), puis comparées
à la table de figures.py sur toutes les combinaisons (cas X exclus) ; chaque groupe dessiné doit être un rectangle de 2^k cases
voisines, ne contenir que des 1 ou des X, et le terme qu'on en lit doit être celui annoncé."""
import itertools, os, re, zipfile, importlib.util

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "..", "..", "sortie", "tm1", "semaine-2", "220-karnaugh")
NOT = lambda x: 1 - x
GRAY = [0, 1, 3, 2]

# équations annoncées (réécrites ici, indépendamment de figures.py)
ANNONCE = {
    "rinc": lambda a, b, c: b | (a & c),
    "k4": lambda a, b, c, d: (NOT(a) & NOT(c)) | (a & c),
    "vid": lambda a, b, c: c | (NOT(a) & b),
    "t1": lambda a, b, c: NOT(b),
    "t2": lambda a, b, c: (a & b) | (b & c),
    "t3": lambda a, b, c, d: (NOT(c) & NOT(d)) | (a & NOT(b) & c),
    "conv": lambda a, b, c: a & (b | c),
    "ejec": lambda a, b, c, d: NOT(a) | (NOT(b) & NOT(d)) | (NOT(c) & NOT(d)),
    "n1": lambda a, b, c: (a & NOT(c)) | (a & b),
    "n3": lambda a, b, c, d: (NOT(a) & NOT(c)) | (a & c),
    "n5": lambda a, b, c: (a & NOT(b)) | (a & NOT(c)),
}
# lignes à 1 annoncées dans les textes (indices k = 4C + 2B + A)
LIGNES = {"ejec": [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14], "rinc": [2, 3, 5, 6, 7], "n1": [1, 3, 7], "n3": [0, 2, 5, 7, 8, 10, 13, 15], "conv": [3, 5, 7], "n5": [1, 3, 5]}


def coords(n, k):
    """(ligne, colonne) d'une combinaison dans le tableau, ordre 00, 01, 11, 10."""
    if n == 2: return (k >> 1) & 1, k & 1
    if n == 3: return (k >> 2) & 1, GRAY.index(k & 3)
    return GRAY.index(k >> 2), GRAY.index(k & 3)


def rectangle(n, cases):
    """Vrai si les cases forment un rectangle de 2^k cases voisines (bords reliés)."""
    nl, nc = (2, 2) if n == 2 else (2, 4) if n == 3 else (4, 4)
    pts = {coords(n, k) for k in cases}
    if len(pts) & (len(pts) - 1): return False
    ls, cs = {p[0] for p in pts}, {p[1] for p in pts}
    if len(ls) * len(cs) != len(pts): return False
    def suite(s, tot):
        return any(all(((d + i) % tot) in s for i in range(len(s))) for d in range(tot))
    return suite(ls, nl) and suite(cs, nc) and len(ls) in (1, 2, 4) and len(cs) in (1, 2, 4)


def terme(n, cases):
    """Fonction lue sur un groupe : produit des variables constantes."""
    fixes = [(i, (cases[0] >> i) & 1) for i in range(n) if len({(k >> i) & 1 for k in cases}) == 1]
    return lambda *v: int(all(v[i] == b for i, b in fixes))


def verifier():
    E = []
    ok = lambda c, m: None if c else E.append(m)
    spec = importlib.util.spec_from_file_location("fig220", os.path.join(ICI, "figures.py"))
    F = importlib.util.module_from_spec(spec); spec.loader.exec_module(F)
    for nom, (n, f, x, groupes, simp) in F.FONCTIONS.items():
        if nom == "vid0": continue
        vals = F.valeurs(nom)
        g = ANNONCE[nom]
        for k in range(1 << n):
            v = [(k >> i) & 1 for i in range(n)]
            if vals[k] != "X": ok(g(*v) == vals[k], f"{nom} : l'équation annoncée diffère de la table en k = {k}")
            ok(simp(*v) == g(*v) or vals[k] == "X", f"{nom} : FONCTIONS (simplifiée) ≠ équation annoncée en k = {k}")
        for grp in groupes:
            ok(rectangle(n, grp), f"{nom} : le groupe {grp} n'est pas un rectangle de 2^k cases voisines")
            ok(all(vals[k] in (1, "X") for k in grp), f"{nom} : le groupe {grp} contient un 0")
        ok(all(any(k in grp for grp in groupes) for k in range(1 << n) if vals[k] == 1), f"{nom} : un 1 n'est dans aucun groupe")
        lu = lambda *v: int(any(terme(n, grp)(*v) for grp in groupes))
        for k in range(1 << n):
            v = [(k >> i) & 1 for i in range(n)]
            if vals[k] != "X": ok(lu(*v) == vals[k], f"{nom} : les groupes lus ne redonnent pas la table en k = {k}")
        if nom in LIGNES:
            ok([k for k in range(1 << n) if vals[k] == 1] == LIGNES[nom], f"{nom} : lignes à 1 annoncées fausses")
    # sans les X (pompe de vidange) : S = B · C + Ā · B redonne les 1 sans couvrir de X inutile
    vals = F.valeurs("vid")
    sx = lambda a, b, c: (b & c) | (NOT(a) & b)
    ok(all(sx((k) & 1, (k >> 1) & 1, (k >> 2) & 1) == vals[k] for k in range(8) if vals[k] != "X"), "vid : équation sans X fausse")
    # convoyeur de la présentation 200 : départ et résultat
    ok(all(((a & b) | (a & NOT(b) & c)) == (a & (b | c)) for a, b, c in itertools.product((0, 1), repeat=3)), "conv : départ ≠ résultat")
    # le corrigé contient la colonne S du N°5
    f = os.path.join(SORTIE, "230 EX C Simplification par Karnaugh.docx")
    if os.path.exists(f):
        x = zipfile.ZipFile(f).read("word/document.xml").decode("utf-8")
        tabs = re.findall(r"<w:tbl>.*?</w:tbl>", x, flags=re.S)
        lignes = lambda t: [["".join(re.findall(r"<[wm]:t(?: [^>]*)?>([^<]*)</[wm]:t>", c)) for c in re.findall(r"<w:tc>.*?</w:tc>", r, flags=re.S)]
                            for r in re.findall(r"<w:tr[ >].*?</w:tr>", t, flags=re.S)]
        tables = [lignes(t) for t in tabs if lignes(t) and lignes(t)[0][:4] == ["C", "B", "A", "S"]]
        attendu = [str((a & NOT(b)) | (a & b & NOT(c))) for c in (0, 1) for b in (0, 1) for a in (0, 1)]
        ok(len(tables) == 3, f"230 : {len(tables)} tables C B A S au lieu de 3 (N°1, N°4, N°5)")
        if tables:
            lu = [r[3] for r in tables[-1][1:]]
            ok(lu == attendu, f"230 N°5 : colonne S du corrigé {''.join(lu)} ≠ {''.join(attendu)}")
    else:
        E.append("corrigé 230 EX C absent : lancer build.py avant le contrôle")
    return E
