# -*- coding: utf-8 -*-
"""230 EX — Courbe caractéristique, marche à vide et court-circuit (élève + corrigé)."""
import os, re, shutil, zipfile, subprocess
from docx_helpers import *      # esc, run, rich, para, HR, EMPTY, table, image, SRC, RED…

TITRE = "Courbe caractéristique, marche à vide et court-circuit"
OUTDIR = "out"
WORK = "work_docx2"

# quadrillages : (identifiant de relation, fichier élève, fichier corrigé)
GRILLES = [("rIdG1", "17a_vide.png", "17a_corrige.png"),
           ("rIdG2", "17b_vide.png", "17b_corrige.png"),
           ("rIdG3", "17c_vide.png", "17c_corrige.png")]


def build(corrige):
    B = []

    def ans(txt, lines=1):
        if corrige:
            B.append(para(rich(txt, color=RED), after=60, ind=340))
        else:
            for _ in range(lines):
                B.append(para(run(tab=True), leader=9350, before=70, after=70, ind=340))

    def q(txt, after=60, keep=False):
        B.append(para(rich(txt), after=after, ind=340, keep=keep))

    def enonce(txt, after=120):
        B.append(para(rich(txt), after=after))

    def ex(num, titre):
        if B:
            B.extend([EMPTY, EMPTY, HR])
        B.append(para(rich(f"N°{num} {titre}"), tabs=[5103], after=120, keep=True))

    # ---------------------------------------------------------------- N°1
    ex(1, "Les deux régimes limites")
    enonce("Complète le tableau pour une source de tension à vide U_{0} et de "
           "résistance interne R_{i}.")
    rep = [("Marche à vide", "0 A", "U_{0}", "infinie", "0 W"),
           ("Court-circuit", "U_{0} / R_{i}", "0 V", "0 Ω", "0 W")]
    rows = [["Régime", "Courant I", "Tension U", "Charge R", "Puissance dans R"]]
    for nom, i, u, r, p in rep:
        rows.append([(nom, {}),
                     (i if corrige else "", dict(color=RED)),
                     (u if corrige else "", dict(color=RED)),
                     (r if corrige else "", dict(color=RED)),
                     (p if corrige else "", dict(color=RED))])
    B.append(table([1701, 1418, 1418, 1276, 1985], rows))
    B.append(EMPTY)
    q("a)  Écris la relation qui donne le courant de court-circuit :")
    ans("I_{cc} = U_{0} / R_{i}")
    q("b)  Donne les deux façons de calculer R_{i} :")
    ans("R_{i} = U_{0} / I_{cc}    et    R_{i} = ΔU / ΔI")

    # ---------------------------------------------------------------- N°2
    ex(2, "Application directe")
    enonce("Sur une alimentation, on mesure une tension à vide de 15 V et un courant "
           "de court-circuit de 6 A.")
    q("a)  Calcule sa résistance interne.")
    ans("R_{i} = U_{0} / I_{cc} = 15 / 6 = 2,5 Ω", 2)
    q("b)  Quelle tension lit-on aux bornes pour I = 2 A ?")
    ans("U = 15 − 2,5 · 2 = 10,0 V", 2)
    q("c)  Et pour I = 4 A ?")
    ans("U = 15 − 2,5 · 4 = 5,0 V", 2)

    # ---------------------------------------------------------------- N°3
    ex(3, "Exploiter un relevé de mesures")
    enonce("Voici le relevé effectué sur une source :")
    B.append(table([1418, 1276, 1276, 1276, 1276],
                   [["I [A]", "0", "1", "2", "3"],
                    ["U [V]", "20,0", "18,5", "17,0", "15,5"]]))
    B.append(EMPTY)
    q("a)  Quelle est la tension à vide de cette source ? Comment le sais-tu ?")
    ans("U_{0} = 20,0 V : c’est la valeur mesurée pour I = 0, donc en marche à vide.", 2)
    q("b)  Calcule la résistance interne.")
    ans("R_{i} = ΔU / ΔI = (20,0 − 15,5) / 3 = 4,5 / 3 = 1,5 Ω", 2)
    q("c)  Calcule le courant de court-circuit.")
    ans("I_{cc} = U_{0} / R_{i} = 20,0 / 1,5 = 13,3 A", 2)
    q("d)  Les points de ce relevé sont-ils alignés ? Justifie sans tracer.")
    ans("Oui : la tension baisse chaque fois de 1,5 V quand le courant augmente de 1 A. "
        "L’écart est constant, donc les points sont sur une droite.", 2)

    # ---------------------------------------------------------------- N°4
    ex(4, "Tracer la caractéristique d’une source")
    enonce("Une source donne 10 V à vide et 4 A en court-circuit.")
    q("a)  Calcule sa résistance interne.")
    ans("R_{i} = 10 / 4 = 2,5 Ω")
    q("b)  Place les deux points limites et trace la caractéristique sur le quadrillage.",
      keep=True)
    B.append(image("rIdG1", 5.3, 3.56, 1))
    q("c)  Lis sur ton tracé la tension aux bornes pour I = 2 A.")
    ans("U = 5,0 V")
    q("d)  Quelle résistance de charge donne ce point de fonctionnement ?")
    ans("R = U / I = 5,0 / 2,0 = 2,5 Ω")

    # ---------------------------------------------------------------- N°5
    ex(5, "Point de fonctionnement")
    enonce("On branche une charge R = 7,5 Ω sur la source de l’exercice 4. Sa "
           "caractéristique est déjà tracée sur le quadrillage.")
    q("a)  Trace la caractéristique de la charge, puis marque le point de fonctionnement.",
      keep=True)
    B.append(image("rIdG2", 5.3, 3.56, 2))
    q("b)  Relève les coordonnées de ce point.")
    ans("I = 1,0 A  et  U = 7,5 V", 2)
    q("c)  Vérifie ce résultat par le calcul.")
    ans("I = U_{0} / (R_{i} + R) = 10 / (2,5 + 7,5) = 1,0 A  puis  U = R · I "
        "= 7,5 · 1,0 = 7,5 V ✓", 2)
    q("d)  Quelle puissance reçoit la charge ?")
    ans("P = U · I = 7,5 · 1,0 = 7,5 W", 2)

    # ---------------------------------------------------------------- N°6
    ex(6, "Une charge non linéaire : la lampe")
    enonce("On a relevé la caractéristique d’une petite lampe à incandescence :")
    B.append(table([1418, 992, 992, 992, 992, 992, 992],
                   [["I [A]", "0,2", "0,4", "0,6", "0,8", "1,0", "1,2"],
                    ["U [V]", "0,5", "1,4", "2,7", "4,2", "6,0", "8,0"]]))
    B.append(EMPTY)
    enonce("Cette lampe est alimentée par une source de 9 V dont la résistance interne "
           "vaut 3 Ω. Son courant de court-circuit sort du quadrillage : place le point "
           "à vide, puis calcule un second point (par exemple pour I = 1 A) pour tracer "
           "sa droite.")
    q("a)  Trace les deux caractéristiques sur le quadrillage.", keep=True)
    B.append(image("rIdG3", 5.3, 3.56, 3))
    q("b)  Relève le point de fonctionnement.")
    ans("I = 1,0 A  et  U = 6,0 V", 2)
    q("c)  Calcule la résistance de la lampe à ce point, puis à I = 0,4 A.")
    ans("À 1,0 A : R = 6,0 / 1,0 = 6,0 Ω     à 0,4 A : R = 1,4 / 0,4 = 3,5 Ω", 2)
    q("d)  Pourquoi ne peut-on pas trouver ce point de fonctionnement par un simple "
      "calcul, comme à l’exercice 5 ?")
    ans("Parce que la résistance de la lampe n’est pas constante : le filament chauffe "
        "quand le courant augmente, donc sa résistance augmente. Il n’y a pas de valeur "
        "de R unique à mettre dans la formule.", 3)
    q("e)  Quelle puissance la lampe consomme-t-elle à ce point ?")
    ans("P = U · I = 6,0 · 1,0 = 6,0 W")

    return "".join(B)


def make(corrige):
    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    with zipfile.ZipFile(SRC) as z:
        z.extractall(WORK)
    for root, _, files in os.walk(WORK):
        for f in files:
            p = os.path.join(root, f)
            if os.path.islink(p):
                os.remove(p)

    os.makedirs(f"{WORK}/word/media", exist_ok=True)
    rels = f"{WORK}/word/_rels/document.xml.rels"
    t = open(rels, encoding="utf8").read()
    add = ""
    for rid, f_eleve, f_corr in GRILLES:
        src = "fig/" + (f_corr if corrige else f_eleve)
        shutil.copy(src, f"{WORK}/word/media/{rid}.png")
        add += ('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/'
                'officeDocument/2006/relationships/image" Target="media/%s.png"/>'
                % (rid, rid))
    open(rels, "w", encoding="utf8").write(
        t.replace("</Relationships>", add + "</Relationships>"))

    ct = f"{WORK}/[Content_Types].xml"
    t = open(ct, encoding="utf8").read()
    if 'Extension="png"' not in t:
        t = t.replace('<Default Extension="rels"',
                      '<Default Extension="png" ContentType="image/png"/>'
                      '<Default Extension="rels"')
    open(ct, "w", encoding="utf8").write(t)

    doc = f"{WORK}/word/document.xml"
    t = open(doc, encoding="utf8").read()
    sectpr = re.search(r"<w:sectPr .*?</w:sectPr>", t, re.S).group(0)
    entete = (
        para(run(TITRE, style="Accentuation", sz="32")
             + run(tab=True, style="Accentuation") + run("Nom :", style="Accentuation"),
             tabs=[6237], after=60)
        + para((run("Corrigé", style="Accentuation", color=RED) if corrige
                else run("", style="Accentuation"))
               + run(tab=True, style="Accentuation") + run("Date :", style="Accentuation"),
               tabs=[6237], after=60)
        + HR)
    body = entete + build(corrige) + EMPTY + sectpr
    t = re.sub(r"<w:body>.*</w:body>", "<w:body>" + body + "</w:body>", t, flags=re.S)
    open(doc, "w", encoding="utf8").write(t)

    os.makedirs(OUTDIR, exist_ok=True)
    name = ("230 EX C Courbe caractéristique.docx" if corrige
            else "230 EX Courbe caractéristique.docx")
    out = os.path.join(OUTDIR, name)
    if os.path.exists(out):
        os.remove(out)
    subprocess.run(["zip", "-Xqr", os.path.abspath(out), "."], cwd=WORK, check=True)
    print("saved", out)
    return out


if __name__ == "__main__":
    make(True)
    make(False)
