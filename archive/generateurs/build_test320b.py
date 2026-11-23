# -*- coding: utf-8 -*-
"""320 TEST B — Champ électrique et condensateur (élève + corrigé).

Deuxième série, STRICTEMENT la même structure et le même niveau que la série A
— mêmes questions, même barème, même durée. Seules les valeurs changent, et
aucune ne se retrouve dans le test A, dans la fiche 310 ni dans le cours 300.

Durée prévue : 25 minutes, 20 points. Mise en page reprise du test ETML
« 1920 xLO3Test 1 » : en-tête TEST No, matériel autorisé, barème à droite de
chaque question. Les titres de question ne portent AUCUNE tabulation après le
numéro — seul le barème est aligné à droite.

Corrigé : chaque réponse est développée en trois temps —
  ① forme algébrique   ② application numérique en puissances de 10   ③ notation ingénieur
Les expressions sont de vraies équations Word (OMML), pas du texte.
"""
import os, re, shutil, zipfile, subprocess
from docx_helpers import *
from mathml import omath

TITRE = "Champ électrique et condensateur"
NUMERO = "TEST No 2 B"
ANNEE = "2026-2027"
TOTAL = 20
DUREE = "25 minutes"
OUTDIR = "out"
WORK = "work_test320b"
GREY = "7F8FA9"
MSZ = 22          # taille des équations (demi-points) → 11 pt

GRILLES = [("rIdT1", "B1_reseau.png", "B1_reseau.png"),
           ("rIdT2", "B2_circuit_charge.png", "B2_circuit_charge.png"),
           ("rIdT3", "B4_courbe.png", "B4c_courbe.png"),
           ("rIdT4", "B3_circuit_ouverture.png", "B3_circuit_ouverture.png"),
           ("rIdT5", "B5_grilles.png", "B5c_grilles.png")]


def para_droite(gauche, droite, after=120, before=0, keep=False):
    """Paragraphe avec un texte à gauche et le barème aligné à droite."""
    # l'ordre des éléments de w:pPr est imposé par le schéma OOXML :
    # keepNext et keepLines avant w:tabs, w:spacing après.
    ppr = "<w:keepNext/><w:keepLines/>" if keep else ""
    ppr += '<w:tabs><w:tab w:val="right" w:pos="9070"/></w:tabs>'
    ppr += '<w:spacing w:before="%d" w:after="%d"/>' % (before, after)
    return ("<w:p><w:pPr>%s</w:pPr>%s%s%s</w:p>"
            % (ppr, gauche, run(tab=True), droite))


def build(corrige):
    B = []
    bareme = []

    def q(txt, after=60, keep=False):
        B.append(para(rich(txt), after=after, ind=340, keep=keep))

    def enonce(txt, after=100):
        B.append(para(rich(txt), after=after))

    def question(num, titre, pts):
        bareme.append((num, titre, pts))
        if B:
            B.extend([EMPTY, HR])
        B.append(para_droite(
            run("%d : " % num, bold=True) + rich(titre, bold=True),
            run("%s pt%s" % (str(pts).replace(".", ","), "s" if pts > 1 else ""),
                sz="18"),
            after=120, keep=True))

    def etape(label, expr):
        return para(run(label + "   ", sz="16", color=RED, italic=True)
                    + omath(expr, color=RED, sz=MSZ),
                    ind=567, before=40, after=40, keep=True)

    def sol(alg=None, num=None, ing=None, txt=None, lines=None, note=None):
        if corrige:
            if txt:
                B.append(para(rich(txt, color=RED), after=60, ind=340))
            if alg:
                B.append(etape("algébrique", alg))
            if num:
                B.append(etape("numérique", num))
            if ing:
                B.append(etape("ingénieur", ing))
            if note:
                B.append(para(run(note, sz="16", color=GREY, italic=True),
                              ind=567, after=80))
        else:
            n = lines if lines else (1 if txt and not alg else
                                     sum(1 for x in (alg, num, ing) if x))
            for _ in range(max(n, 1)):
                B.append(para(run(tab=True), leader=9350, before=70, after=70,
                              ind=340))

    # ================================================================ 1
    question(1, "Les lignes d’un champ électrique", 2)
    q("Explique en une phrase ce que représentent les lignes d’un champ "
      "électrique, puis cite deux de leurs propriétés.")
    sol(txt="Elles représentent la direction de la force qu’une charge subirait "
            "en chaque point : la force est tangente à la ligne. — Deux "
            "propriétés parmi : la flèche donne le sens de la force sur une "
            "charge positive ; plus les lignes sont serrées, plus le champ est "
            "fort ; elles partent du + et arrivent au − ; elles ne se croisent "
            "jamais ; elles sont perpendiculaires aux surfaces conductrices.",
        lines=4,
        note="Barème : 1 pt pour la phrase, 0,5 pt par propriété correcte.")

    # ================================================================ 2
    question(2, "Champ dans un condensateur plan", 3)
    enonce("Un condensateur plan est soumis à U = 900 V. Son isolant a une "
           "épaisseur d = 3,0 mm et supporte au maximum 7 kV/mm.", after=80)
    q("a)  Calcule l’intensité du champ électrique entre les armatures.")
    sol(alg=r"E = \f{U}{d}",
        num=r"E = \f{900}{3,0 \cdot 10^{-3}} = 0,3 \cdot 10^{6} \u{ [V/m]}",
        ing=r"E = 300 \u{ [kV/m]} = 0,3 \u{ [kV/mm]}",
        note="Barème : 2 pts — 0,5 formule, 1 calcul, 0,5 unité correcte.")
    q("b)  Quelle tension maximale peut-on appliquer sans percer l’isolant ?")
    sol(alg=r"U_{max} = E_{max} \cdot d",
        num=r"U_{max} = 7 \cdot 10^{3} \cdot 3,0 = 21 \cdot 10^{3} \u{ [V]}",
        ing=r"U_{max} = 21 \u{ [kV]}",
        note="Barème : 1 pt.")

    # ================================================================ 3
    question(3, "Capacité équivalente entre A et B", 4)
    B.append(image("rIdT1", 5.8, 2.45, 1))
    q("Réduis le montage étape par étape et donne C_{AB}.", keep=True)
    sol(alg=r"C_{23} = \f{C_{2} \cdot C_{3}}{C_{2} + C_{3}}",
        num=r"C_{23} = \f{21 \cdot 10^{-6} \cdot 42 \cdot 10^{-6}}"
            r"{63 \cdot 10^{-6}} = 14 \cdot 10^{-6} \u{ [F]}",
        ing=r"C_{23} = 14 \u{ [µF]}", lines=2)
    sol(alg=r"C_{234} = C_{23} + C_{4}",
        num=r"C_{234} = 14 \cdot 10^{-6} + 22 \cdot 10^{-6} = 36 \cdot 10^{-6} "
            r"\u{ [F]}",
        ing=r"C_{234} = 36 \u{ [µF]}", lines=2)
    sol(alg=r"C_{AB} = \f{C_{1} \cdot C_{234}}{C_{1} + C_{234}}",
        num=r"C_{AB} = \f{18 \cdot 10^{-6} \cdot 36 \cdot 10^{-6}}"
            r"{54 \cdot 10^{-6}} = 12 \cdot 10^{-6} \u{ [F]}",
        ing=r"C_{AB} = 12 \u{ [µF]}", lines=3,
        note="Barème : 4 pts — 1 pt par étape correcte, 1 pt pour le résultat "
             "final avec son unité. Contrôle de bon sens : la capacité totale "
             "est plus petite que 18 µF, puisque le groupe est en série avec C₁.")

    # ================================================================ 4
    question(4, "Retrouver une capacité inconnue", 5)
    enonce("On ferme S à t = 0 et on relève le courant de charge à "
           "l’oscilloscope. La courbe ci-dessous donne i_{C} = 6,00 mA à "
           "t = 35 µs.", after=80)
    B.append(image("rIdT2", 4.6, 2.38, 2))
    B.append(image("rIdT3", 5.6, 2.65, 3))
    q("a)  Calcule le courant au tout premier instant, I_{0}.", keep=True)
    sol(alg=r"I_{0} = \f{U}{R}",
        num=r"I_{0} = \f{9}{750} = 12 \cdot 10^{-3} \u{ [A]}",
        ing=r"I_{0} = 12,0 \u{ [mA]}",
        note="Barème : 1 pt. I₀ ne se lit pas sur la courbe, il se calcule.")
    q("b)  Calcule la constante de temps τ.")
    sol(txt="Le point relevé vaut la moitié de I₀, donc t = τ · ln 2.",
        alg=r"\tau = \f{t}{\u{ln} 2}",
        num=r"\tau = \f{35 \cdot 10^{-6}}{0,693} = 50,5 \cdot 10^{-6} \u{ [s]}",
        ing=r"\tau = 50,5 \u{ [µs]}", lines=4,
        note="Barème : 2 pts — 1 pt pour avoir reconnu la demi-valeur, 1 pt "
             "pour le calcul.")
    q("c)  Calcule C_{x}, puis donne la valeur normalisée E12 la plus proche.")
    sol(alg=r"C_{x} = \f{\tau}{R}",
        num=r"C_{x} = \f{50,5 \cdot 10^{-6}}{750} = 67,3 \cdot 10^{-9} \u{ [F]}",
        ing=r"C_{x} = 67,3 \u{ [nF]} \approx 68 \u{ [nF]}",
        note="Barème : 2 pts — 1,5 pour le calcul, 0,5 pour la valeur E12.")

    # ================================================================ 5
    question(5, "Régime établi, puis ouverture de S", 6)
    enonce("S est fermé depuis longtemps : le condensateur est complètement "
           "chargé. À t = 0 on ouvre S.", after=80)
    B.append(image("rIdT4", 5.6, 2.64, 4))
    q("a)  Que vaut i_{C} en régime établi ? Qu’en déduis-tu pour U_{C} max ?",
      keep=True)
    sol(txt="i_{C} = 0 : le condensateur se comporte comme un circuit ouvert. "
            "U_{C} max est donc la tension aux bornes de R₂, donnée par le "
            "diviseur R₁ – R₂.", lines=2,
        note="Barème : 0,5 pt.")
    sol(alg=r"U_{C max} = E \cdot \f{R_{2}}{R_{1} + R_{2}}",
        num=r"U_{C max} = 36 \cdot \f{200}{450} = 36 \cdot 0,444",
        ing=r"U_{C max} = 16,0 \u{ [V]}",
        note="Barème : 1 pt.")
    q("b)  Dans quelle résistance le condensateur se décharge-t-il ? Justifie, "
      "puis calcule τ.")
    sol(txt="Dans R₂ seule : l’ouverture de S met hors circuit la source et R₁.",
        alg=r"\tau = R_{2} \cdot C",
        num=r"\tau = 200 \cdot 25 \cdot 10^{-6} = 5,00 \cdot 10^{-3} \u{ [s]}",
        ing=r"\tau = 5,00 \u{ [ms]}", lines=4,
        note="Barème : 1,5 pt — 0,5 pour la justification, 1 pour le calcul. "
             "Prendre R₁ + R₂ ou R₁ seul est l’erreur classique.")
    q("c)  Calcule I_{C} max, le courant au tout premier instant de la décharge.")
    sol(alg=r"I_{C max} = \f{U_{C max}}{R_{2}}",
        num=r"I_{C max} = \f{16,0}{200} = 80 \cdot 10^{-3} \u{ [A]}",
        ing=r"I_{C max} = 80,0 \u{ [mA]}",
        note="Barème : 1 pt.")
    q("d)  Trace u_{C} = f(t) et i_{C} = f(t) sur les deux graphes. Gradue les "
      "axes, indique la grandeur et l’unité de chacun, et reporte τ, U_{C} max "
      "et I_{C} max.", keep=True)
    B.append(image("rIdT5", 6.5, 2.01, 5))
    if corrige:
        B.append(para(rich("Les deux courbes partent de leur maximum et "
                           "décroissent. À un τ = 5,0 ms il reste 37 % : "
                           "5,89 V et 29,4 mA. Après 5 τ = 25 ms, tout est "
                           "retombé à zéro.", color=RED), ind=340, after=60))
        B.append(para(run("Barème : 2 pts — 0,5 par axe correctement nommé et "
                          "gradué, 1 pt pour les deux allures et les valeurs "
                          "reportées.", sz="16", color=GREY, italic=True),
                      ind=567, after=80))

    # ---------------------------------------------------------- récapitulatif
    if corrige:
        B.extend([EMPTY, HR])
        B.append(para(rich("Récapitulatif du barème"), tabs=[5103], after=120,
                      keep=True))
        rows = [["Question", "Sujet", "Points"]]
        for num, titre, pts in bareme:
            rows.append([(str(num), {}), (titre, dict(jc="left")),
                         (str(pts).replace(".", ","), {})])
        rows.append([("", {}), ("Total", dict(jc="left", bold=True)),
                     (str(TOTAL), dict(bold=True))])
        B.append(table([1560, 5100, 1560], rows))
        B.append(para(rich("Note = 1 + 5 · points obtenus / %d, arrondie au "
                           "dixième." % TOTAL), before=160, after=60))
        B.append(para(rich("Durée prévue : %s. Seuil de suffisance (note 4) : "
                           "%s points." % (DUREE, ("%.1f" % (TOTAL * 0.6))
                                           .replace(".", ","))), after=60))

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
        shutil.copy("fig/" + (f_corr if corrige else f_eleve),
                    f"{WORK}/word/media/{rid}.png")
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
        para(run("%s    %s" % (NUMERO, ANNEE), style="Accentuation", sz="32")
             + run(tab=True, style="Accentuation")
             + run("Date :", style="Accentuation"), tabs=[6237], after=60)
        + para((run("Corrigé — " + TITRE, style="Accentuation", color=RED) if corrige
                else run(TITRE, style="Accentuation"))
               + run(tab=True, style="Accentuation")
               + run("Nom :", style="Accentuation"), tabs=[6237], after=60)
        + para(run("Matériel : calculette et formulaire personnel", sz="20")
               + run(tab=True)
               + run("Points :          / %d" % TOTAL, sz="20"),
               tabs=[6237], after=60)
        + HR)
    fin = ('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="20" '
           'w:lineRule="exact"/><w:rPr><w:sz w:val="2"/></w:rPr></w:pPr></w:p>')
    body = entete + build(corrige) + fin + sectpr
    t = re.sub(r"<w:body>.*</w:body>", "<w:body>" + body + "</w:body>", t, flags=re.S)
    open(doc, "w", encoding="utf8").write(t)

    os.makedirs(OUTDIR, exist_ok=True)
    name = ("320 TEST B C Champ et condensateur.docx" if corrige
            else "320 TEST B Champ et condensateur.docx")
    out = os.path.join(OUTDIR, name)
    if os.path.exists(out):
        os.remove(out)
    subprocess.run(["zip", "-Xqr", os.path.abspath(out), "."], cwd=WORK, check=True)
    print("saved", out)
    return out


if __name__ == "__main__":
    make(True)
    make(False)
