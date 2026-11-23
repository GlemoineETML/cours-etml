# -*- coding: utf-8 -*-
"""Compare un fichier produit (.pptx, .docx, .xlsx, .html) avec sa version étalon de reference/.

Usage : python3 controle/comparer.py <produit> <étalon> [--diff]
Office : on compare chaque partie du paquet. Le XML est normalisé (dates de création et de modification,
identifiants aléatoires de pptxgenjs) ; les médias sont comparés octet par octet.
Code de sortie 0 si tout est identique, 1 sinon. --diff affiche les premières lignes qui diffèrent.
"""
import difflib, hashlib, re, sys, zipfile

VOLATIL = [
    (re.compile(rb"<dcterms:(created|modified)[^>]*>[^<]*</dcterms:\1>"), b"<dcterms:\\1/>"),
    (re.compile(rb'w:rsid\w*="[0-9A-F]+"'), b""),
    (re.compile(rb'\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}'), b"{GUID}"),
    (re.compile(rb'<p14:creationId [^>]*/>'), b""),
]


def normaliser(nom, data):
    if not nom.endswith((".xml", ".rels")):
        return data
    for rx, rep in VOLATIL:
        data = rx.sub(rep, data)
    return data


def parties(chemin):
    if chemin.endswith(".html"):
        return {"page": open(chemin, "rb").read()}
    z = zipfile.ZipFile(chemin)
    return {n: normaliser(n, z.read(n)) for n in z.namelist() if not n.endswith("/")}


def comparer(produit, etalon, diff=False):
    a, b = parties(produit), parties(etalon)
    ecarts = []
    for n in sorted(set(a) | set(b)):
        if n not in a:
            ecarts.append(f"manque dans le produit : {n}")
        elif n not in b:
            ecarts.append(f"en trop dans le produit : {n}")
        elif a[n] != b[n]:
            ecarts.append(f"différent : {n}")
            if diff and n.endswith((".xml", ".rels", "page")):
                ta = re.sub(rb">\s*<", b">\n<", a[n]).decode("utf-8", "replace").splitlines()
                tb = re.sub(rb">\s*<", b">\n<", b[n]).decode("utf-8", "replace").splitlines()
                for l in list(difflib.unified_diff(tb, ta, "étalon", "produit", n=0, lineterm=""))[:30]:
                    ecarts.append("    " + l[:220])
            elif diff:
                ecarts.append(f"    md5 {hashlib.md5(a[n]).hexdigest()} ≠ {hashlib.md5(b[n]).hexdigest()}")
    return ecarts


if __name__ == "__main__":
    e = comparer(sys.argv[1], sys.argv[2], "--diff" in sys.argv)
    print("\n".join(e) if e else "identique")
    sys.exit(1 if e else 0)
