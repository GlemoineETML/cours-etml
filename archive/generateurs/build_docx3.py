# -*- coding: utf-8 -*-
"""150 EX — Circuits mixtes et simplification (élève + corrigé).

Corrigé : chaque réponse est développée en trois temps —
  ① forme algébrique   ② application numérique en puissances de 10   ③ notation ingénieur
Les expressions sont de vraies équations Word (OMML), pas du texte.
"""
import os, re, shutil, zipfile, subprocess
from docx_helpers import *
from mathml import omath

TITRE = "Circuits mixtes et simplification"
OUTDIR = "out"
WORK = "work_docx3"
GREY = "7F8FA9"
MSZ = 22          # taille des équations (demi-points) → 11 pt

GRILLES = [("rIdG1", "52_reconnaitre.png", "52_reconnaitre.png"),
           ("rIdG2", "44_ex2.png", "44_ex2.png"),
           ("rIdG3", "45_ex3.png", "45_ex3.png"),
           ("rIdG4", "46_ex4.png", "46_ex4.png"),
           ("rIdG5", "53_tordu_seul.png", "53_propre_seul.png"),
           ("rIdG6", "47_tp.png", "47_tp.png"),
           ("rIdG7", "54_kirchhoff.png", "54_kirchhoff.png"),
           ("rIdR3", "55_red_n3.png", "55_red_n3.png"),
           ("rIdR4", "56_red_n4.png", "56_red_n4.png"),
           ("rIdR5", "57_red_n5.png", "57_red_n5.png")]


def build(corrige):
    B = []

    # ---------------------------------------------------------- mise en page
    def q(txt, after=60, keep=False):
        B.append(para(rich(txt), after=after, ind=340, keep=keep))

    def enonce(txt, after=120):
        B.append(para(rich(txt), after=after))

    def ex(num, titre):
        if B:
            B.extend([EMPTY, EMPTY, HR])
        B.append(para(rich(f"N°{num} {titre}"), tabs=[5103], after=120, keep=True))

    def etape(label, expr):
        """Une ligne : petite étiquette grise + équation rouge."""
        return para(run(label + "   ", sz="16", color=RED, italic=True)
                    + omath(expr, color=RED, sz=MSZ),
                    ind=567, before=40, after=40, keep=True)

    def sol(alg=None, num=None, ing=None, txt=None, lines=None):
        """Corrigé développé ; version élève : lignes à remplir."""
        if corrige:
            if txt:
                B.append(para(rich(txt, color=RED), after=60, ind=340))
            if alg:
                B.append(etape("algébrique", alg))
            if num:
                B.append(etape("numérique", num))
            if ing:
                B.append(etape("ingénieur", ing))
        else:
            n = lines if lines else (1 if txt and not alg else
                                     sum(1 for x in (alg, num, ing) if x))
            for _ in range(max(n, 1)):
                B.append(para(run(tab=True), leader=9350, before=70, after=70, ind=340))

    def sol_c(alg=None, num=None, ing=None, txt=None):
        """Développement visible uniquement dans le corrigé (l'élève remplit un tableau)."""
        if corrige:
            sol(alg, num, ing, txt)

    def bande(rid, w_in, h_in, idx):
        """Bande de réduction — corrigé seulement."""
        if corrige:
            B.append(image(rid, w_in, h_in, idx))

    def cell_rep(v):
        return (v if corrige else "", dict(color=RED))

    def boite_dessin(hauteur=4200):
        """Cadre vide pour que l'élève dessine son schéma."""
        bords = "".join(
            '<w:%s w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>' % b
            for b in ("top", "left", "bottom", "right"))
        return ('<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>'
                '<w:jc w:val="center"/><w:tblBorders>' + bords +
                '</w:tblBorders><w:tblLayout w:type="fixed"/>'
                '<w:tblLook w:val="0000"/></w:tblPr>'
                '<w:tblGrid><w:gridCol w:w="9070"/></w:tblGrid>'
                '<w:tr><w:trPr><w:trHeight w:val="%d"/>'
                '<w:jc w:val="center"/></w:trPr>'
                '<w:tc><w:tcPr><w:tcW w:w="9070" w:type="dxa"/></w:tcPr>'
                % hauteur + para() + '</w:tc></w:tr></w:tbl>')

    # ================================================================ N°1
    ex(1, "Reconnaître avant de calculer")
    enonce("Pour chacun des deux schémas, repère les nœuds au crayon, puis réponds.",
           after=60)
    B.append(image("rIdG1", 6.3, 2.17, 1))
    q("a)  Schéma a) : quelles résistances sont en série ? Lesquelles en parallèle ?")
    sol(txt="R₂ et R₃ sont en série. Leur groupe est en parallèle avec R₁.", lines=2)
    q("b)  Schéma a) : écris l’expression de la résistance totale.")
    sol(alg=r"R_{tot} = \f{(R_{2} + R_{3}) \cdot R_{1}}{R_{2} + R_{3} + R_{1}}", lines=2)
    q("c)  Schéma b) : quelles résistances sont en parallèle ?")
    sol(txt="R₃ et R₄, car elles sont branchées entre les deux mêmes nœuds.", lines=2)
    q("d)  Schéma b) : écris l’expression de la résistance totale.")
    sol(alg=r"R_{tot} = R_{1} + R_{2} + \f{R_{3} \cdot R_{4}}{R_{3} + R_{4}}", lines=2)

    # ================================================================ N°2
    ex(2, "Les deux lois de Kirchhoff et la puissance")
    enonce("Observe les deux schémas ci-dessous.", after=60)
    B.append(image("rIdG7", 6.3, 2.21, 7))
    q("a)  Énonce la loi des nœuds.")
    sol(txt="La somme des courants qui entrent dans un nœud est égale à la somme de "
            "ceux qui en sortent.", lines=2)
    q("b)  Sur le schéma a), I₁ = 250 mA et I₂ = 90 mA. Calcule I₃.")
    sol(alg=r"I_{3} = I_{1} - I_{2}",
        num=r"I_{3} = 250 \cdot 10^{-3} - 90 \cdot 10^{-3} = 160 \cdot 10^{-3} \u{ A}",
        ing=r"I_{3} = 160 \u{ mA}")
    q("c)  Énonce la loi des mailles.")
    sol(txt="Sur une boucle fermée, la somme des tensions aux bornes des récepteurs est "
            "égale à la tension de la source.", lines=2)
    q("d)  Sur le schéma b), U = 24 V et U₁ = 9 V. Calcule U₂.")
    sol(alg=r"U_{2} = U - U_{1}",
        num=r"U_{2} = 24 - 9 = 15 \u{ V}",
        ing=r"U_{2} = 15 \u{ V}")
    q("e)  Donne les trois expressions de la puissance dissipée dans une résistance.")
    sol(alg=r"P = U \cdot I = R \cdot I^{2} = \f{U^{2}}{R}", lines=2)
    q("f)  Toujours sur le schéma b), R₂ = 500 Ω. Calcule le courant du circuit, "
      "puis la puissance dissipée dans R₂.")
    sol(alg=r"I_{1} = \f{U_{2}}{R_{2}}",
        num=r"I_{1} = \f{15}{0,5 \cdot 10^{3}} = 30 \cdot 10^{-3} \u{ A}",
        ing=r"I_{1} = 30 \u{ mA}")
    sol(alg=r"P_{2} = U_{2} \cdot I_{1}",
        num=r"P_{2} = 15 \cdot 30 \cdot 10^{-3} = 450 \cdot 10^{-3} \u{ W}",
        ing=r"P_{2} = 450 \u{ mW}")

    # ================================================================ N°3
    ex(3, "Premier couplage à trois résistances")
    B.append(image("rIdG2", 5.0, 2.90, 2))
    q("a)  Calcule la résistance équivalente du groupe parallèle, puis R_{tot}.",
      keep=True)
    bande("rIdR3", 6.5, 1.55, 11)
    sol(alg=r"R_{23} = \f{R_{2} \cdot R_{3}}{R_{2} + R_{3}}",
        num=r"R_{23} = \f{0,15 \cdot 10^{3} \cdot 0,3 \cdot 10^{3}}"
            r"{0,15 \cdot 10^{3} + 0,3 \cdot 10^{3}} = "
            r"\f{0,045 \cdot 10^{6}}{0,45 \cdot 10^{3}} = 0,1 \cdot 10^{3} \u{ Ω}",
        ing=r"R_{23} = 100 \u{ Ω}")
    sol(alg=r"R_{tot} = R_{1} + R_{23}",
        num=r"R_{tot} = 0,1 \cdot 10^{3} + 0,1 \cdot 10^{3} = 0,2 \cdot 10^{3} \u{ Ω}",
        ing=r"R_{tot} = 200 \u{ Ω}")
    q("b)  Calcule le courant total I₁.")
    sol(alg=r"I_{1} = \f{U}{R_{tot}}",
        num=r"I_{1} = \f{15}{0,2 \cdot 10^{3}} = 75 \cdot 10^{-3} \u{ A}",
        ing=r"I_{1} = 75 \u{ mA}")
    q("c)  Calcule U₁ et la tension aux bornes du groupe parallèle.")
    sol(alg=r"U_{1} = R_{1} \cdot I_{1}",
        num=r"U_{1} = 0,1 \cdot 10^{3} \cdot 75 \cdot 10^{-3} = 7,5 \u{ V}",
        ing=r"U_{1} = 7,5 \u{ V}")
    sol(alg=r"U_{23} = U - U_{1}",
        num=r"U_{23} = 15 - 7,5 = 7,5 \u{ V}",
        ing=r"U_{23} = 7,5 \u{ V}")
    q("d)  Calcule I₂ et I₃.")
    sol(alg=r"I_{2} = \f{U_{23}}{R_{2}}",
        num=r"I_{2} = \f{7,5}{0,15 \cdot 10^{3}} = 50 \cdot 10^{-3} \u{ A}",
        ing=r"I_{2} = 50 \u{ mA}")
    sol(alg=r"I_{3} = \f{U_{23}}{R_{3}}",
        num=r"I_{3} = \f{7,5}{0,3 \cdot 10^{3}} = 25 \cdot 10^{-3} \u{ A}",
        ing=r"I_{3} = 25 \u{ mA}")
    q("e)  Pose le contrôle des courants et nomme la loi que tu utilises.")
    sol(txt="Loi des nœuds au nœud A :",
        alg=r"I_{1} = I_{2} + I_{3}",
        num=r"50 \cdot 10^{-3} + 25 \cdot 10^{-3} = 75 \cdot 10^{-3} \u{ A}",
        ing=r"75 \u{ mA} = I_{1}   \u{✓}", lines=3)

    # ================================================================ N°4
    ex(4, "Second couplage à trois résistances")
    B.append(image("rIdG3", 5.0, 2.90, 3))
    q("a)  Calcule R_{tot}.", keep=True)
    bande("rIdR4", 6.5, 1.55, 12)
    sol(alg=r"R_{12} = R_{1} + R_{2}",
        num=r"R_{12} = 0,2 \cdot 10^{3} + 0,4 \cdot 10^{3} = 0,6 \cdot 10^{3} \u{ Ω}",
        ing=r"R_{12} = 600 \u{ Ω}")
    sol(alg=r"R_{tot} = \f{R_{12} \cdot R_{3}}{R_{12} + R_{3}}",
        num=r"R_{tot} = \f{0,6 \cdot 10^{3} \cdot 0,3 \cdot 10^{3}}{0,9 \cdot 10^{3}} = "
            r"\f{0,18 \cdot 10^{6}}{0,9 \cdot 10^{3}} = 0,2 \cdot 10^{3} \u{ Ω}",
        ing=r"R_{tot} = 200 \u{ Ω}")
    q("b)  Calcule le courant total I₁ débité par la source.")
    sol(alg=r"I_{1} = \f{U}{R_{tot}}",
        num=r"I_{1} = \f{24}{0,2 \cdot 10^{3}} = 120 \cdot 10^{-3} \u{ A}",
        ing=r"I_{1} = 120 \u{ mA}")
    q("c)  Calcule I₂ (branche R₁R₂) et I₃ (branche R₃).")
    sol(alg=r"I_{2} = \f{U}{R_{12}}",
        num=r"I_{2} = \f{24}{0,6 \cdot 10^{3}} = 40 \cdot 10^{-3} \u{ A}",
        ing=r"I_{2} = 40 \u{ mA}")
    sol(alg=r"I_{3} = \f{U}{R_{3}}",
        num=r"I_{3} = \f{24}{0,3 \cdot 10^{3}} = 80 \cdot 10^{-3} \u{ A}",
        ing=r"I_{3} = 80 \u{ mA}")
    q("d)  Calcule U₁ et U₂.")
    sol(alg=r"U_{1} = R_{1} \cdot I_{2}",
        num=r"U_{1} = 0,2 \cdot 10^{3} \cdot 40 \cdot 10^{-3} = 8 \u{ V}",
        ing=r"U_{1} = 8 \u{ V}")
    sol(alg=r"U_{2} = R_{2} \cdot I_{2}",
        num=r"U_{2} = 0,4 \cdot 10^{3} \cdot 40 \cdot 10^{-3} = 16 \u{ V}",
        ing=r"U_{2} = 16 \u{ V}")
    q("e)  Pose deux contrôles en nommant la loi utilisée pour chacun.")
    sol(txt="Loi des nœuds :",
        alg=r"I_{1} = I_{2} + I_{3}",
        num=r"40 \cdot 10^{-3} + 80 \cdot 10^{-3} = 120 \cdot 10^{-3} \u{ A} = I_{1}   \u{✓}",
        lines=2)
    sol(txt="Loi des mailles sur la branche R₁R₂ :",
        alg=r"U = U_{1} + U_{2}",
        num=r"8 + 16 = 24 \u{ V} = U   \u{✓}", lines=2)

    # ================================================================ N°5
    ex(5, "Cinq résistances et le tableau complet")
    B.append(image("rIdG4", 6.1, 2.97, 4))
    q("a)  Réduis le circuit en indiquant chaque étape.", keep=True)
    bande("rIdR5", 6.7, 1.64, 13)
    sol(alg=r"R_{34} = R_{3} + R_{4}",
        num=r"R_{34} = 0,05 \cdot 10^{3} + 0,15 \cdot 10^{3} = 0,2 \cdot 10^{3} \u{ Ω}",
        ing=r"R_{34} = 200 \u{ Ω}")
    sol(alg=r"R_{234} = \f{R_{2} \cdot R_{34}}{R_{2} + R_{34}}",
        num=r"R_{234} = \f{0,2 \cdot 10^{3} \cdot 0,2 \cdot 10^{3}}{0,4 \cdot 10^{3}} = "
            r"\f{0,04 \cdot 10^{6}}{0,4 \cdot 10^{3}} = 0,1 \cdot 10^{3} \u{ Ω}",
        ing=r"R_{234} = 100 \u{ Ω}")
    sol(alg=r"R_{tot} = R_{1} + R_{234} + R_{5}",
        num=r"R_{tot} = 0,06 \cdot 10^{3} + 0,1 \cdot 10^{3} + 0,04 \cdot 10^{3} = "
            r"0,2 \cdot 10^{3} \u{ Ω}",
        ing=r"R_{tot} = 200 \u{ Ω}")
    q("b)  Calcule le courant total, puis complète le tableau. Attention aux unités "
      "et aux préfixes.")
    sol(alg=r"I_{1} = \f{U}{R_{tot}}",
        num=r"I_{1} = \f{20}{0,2 \cdot 10^{3}} = 100 \cdot 10^{-3} \u{ A}",
        ing=r"I_{1} = 100 \u{ mA}")
    if corrige:
        B.append(para(rich("On redescend ensuite élément par élément.", color=RED),
                      after=80, ind=340))
    sol_c(alg=r"U_{1} = R_{1} \cdot I_{1}",
          num=r"U_{1} = 0,06 \cdot 10^{3} \cdot 100 \cdot 10^{-3} = 6 \u{ V}",
          ing=r"U_{1} = 6 \u{ V}")
    sol_c(alg=r"U_{2} = R_{234} \cdot I_{1}",
          num=r"U_{2} = 0,1 \cdot 10^{3} \cdot 100 \cdot 10^{-3} = 10 \u{ V}",
          ing=r"U_{2} = 10 \u{ V}")
    sol_c(alg=r"U_{5} = R_{5} \cdot I_{1}",
          num=r"U_{5} = 0,04 \cdot 10^{3} \cdot 100 \cdot 10^{-3} = 4 \u{ V}",
          ing=r"U_{5} = 4 \u{ V}")
    sol_c(alg=r"I_{2} = \f{U_{2}}{R_{2}}",
          num=r"I_{2} = \f{10}{0,2 \cdot 10^{3}} = 50 \cdot 10^{-3} \u{ A}",
          ing=r"I_{2} = 50 \u{ mA}")
    sol_c(alg=r"I_{3} = \f{U_{2}}{R_{34}}",
          num=r"I_{3} = \f{10}{0,2 \cdot 10^{3}} = 50 \cdot 10^{-3} \u{ A}",
          ing=r"I_{3} = 50 \u{ mA}")
    sol_c(alg=r"U_{3} = R_{3} \cdot I_{3}",
          num=r"U_{3} = 0,05 \cdot 10^{3} \cdot 50 \cdot 10^{-3} = 2,5 \u{ V}",
          ing=r"U_{3} = 2,5 \u{ V}")
    sol_c(alg=r"U_{4} = R_{4} \cdot I_{3}",
          num=r"U_{4} = 0,15 \cdot 10^{3} \cdot 50 \cdot 10^{-3} = 7,5 \u{ V}",
          ing=r"U_{4} = 7,5 \u{ V}")
    if corrige:
        B.append(para(rich("Puis les puissances, avec P = U · I :", color=RED),
                      after=80, ind=340))
    sol_c(num=r"P_{1} = 6 \cdot 100 \cdot 10^{-3} = 600 \cdot 10^{-3} \u{ W}",
          ing=r"P_{1} = 600 \u{ mW}")
    sol_c(num=r"P_{2} = 10 \cdot 50 \cdot 10^{-3} = 500 \cdot 10^{-3} \u{ W}",
          ing=r"P_{2} = 500 \u{ mW}")
    sol_c(num=r"P_{3} = 2,5 \cdot 50 \cdot 10^{-3} = 125 \cdot 10^{-3} \u{ W}",
          ing=r"P_{3} = 125 \u{ mW}")
    sol_c(num=r"P_{4} = 7,5 \cdot 50 \cdot 10^{-3} = 375 \cdot 10^{-3} \u{ W}",
          ing=r"P_{4} = 375 \u{ mW}")
    sol_c(num=r"P_{5} = 4 \cdot 100 \cdot 10^{-3} = 400 \cdot 10^{-3} \u{ W}",
          ing=r"P_{5} = 400 \u{ mW}")
    lignes = [("R_{1}", "60 Ω", "6 V", "100 mA  (I₁)", "600 mW"),
              ("R_{2}", "200 Ω", "10 V", "50 mA  (I₂)", "500 mW"),
              ("R_{3}", "50 Ω", "2,5 V", "50 mA  (I₃)", "125 mW"),
              ("R_{4}", "150 Ω", "7,5 V", "50 mA  (I₃)", "375 mW"),
              ("R_{5}", "40 Ω", "4 V", "100 mA  (I₁)", "400 mW"),
              ("Total", "200 Ω", "20 V", "100 mA  (I₁)", "2,0 W")]
    rows = [["", "R", "U", "I", "P"]]
    for nom, r, u, i, p in lignes:
        rows.append([(nom, dict(bold=True)), (r, {}), cell_rep(u), cell_rep(i),
                     cell_rep(p)])
    B.append(table([1134, 1276, 1276, 1418, 1418], rows))
    B.append(EMPTY)
    q("c)  Pose les trois contrôles vus en cours, en nommant chaque loi.")
    sol(txt="Loi des mailles sur le chemin R₁ → groupe → R₅ :",
        alg=r"U = U_{1} + U_{2} + U_{5}",
        num=r"6 + 10 + 4 = 20 \u{ V} = U   \u{✓}", lines=2)
    sol(txt="Loi des nœuds au nœud A :",
        alg=r"I_{1} = I_{2} + I_{3}",
        num=r"50 \cdot 10^{-3} + 50 \cdot 10^{-3} = 100 \cdot 10^{-3} \u{ A} = I_{1}   \u{✓}",
        lines=2)
    sol(txt="Bilan des puissances :",
        alg=r"P_{tot} = P_{1} + P_{2} + P_{3} + P_{4} + P_{5} = U \cdot I_{1}",
        num=r"(600 + 500 + 125 + 375 + 400) \cdot 10^{-3} = 2 \u{ W} = "
            r"20 \cdot 100 \cdot 10^{-3}   \u{✓}", lines=2)

    # ================================================================ N°6
    ex(6, "Redessiner au propre")
    enonce("Ce schéma est juste, mais il est illisible. Redessine-le au propre en "
           "respectant les sept règles vues en cours. Les valeurs sont : "
           "U = 12 V, R₁ = 220 Ω, R₂ = 330 Ω, R₃ = 470 Ω.", after=60)
    B.append(image("rIdG5", 4.5, 2.97, 5))
    if corrige:
        B.append(para(rich("Le schéma redessiné au propre.", color=RED),
                      after=100, ind=340))
    else:
        B.append(para(rich("Ton schéma :"), after=100, ind=340, keep=True))
        B.append(boite_dessin())
        B.append(EMPTY)
    q("Quels défauts as-tu corrigés ?")
    sol(txt="Traits obliques remplacés par des angles droits, jonctions marquées par un "
            "point, repères et valeurs ajoutés, polarité de la source indiquée, flèches "
            "de courant et de tension nommées, source placée à gauche.", lines=3)

    # ================================================================ N°7
    ex(7, "Protocole de mesure")
    enonce("Montage à câbler : alimentation réglée sur 10 V, R₁ = 220 Ω, "
           "R₂ = 470 Ω, R₃ = 1 kΩ (série E12, tolérance ±5 %).", after=60)
    B.append(image("rIdG6", 4.9, 2.84, 6))
    B.append(para(rich("a)  Valeurs calculées AVANT la manipulation"), after=100,
                  ind=340, keep=True))
    if corrige:
        sol(alg=r"R_{23} = \f{R_{2} \cdot R_{3}}{R_{2} + R_{3}}",
            num=r"R_{23} = \f{0,47 \cdot 10^{3} \cdot 1 \cdot 10^{3}}{1,47 \cdot 10^{3}} "
                r"= \f{0,47 \cdot 10^{6}}{1,47 \cdot 10^{3}} = 0,3197 \cdot 10^{3} \u{ Ω}",
            ing=r"R_{23} \approx 320 \u{ Ω}")
        sol(alg=r"R_{tot} = R_{1} + R_{23}",
            num=r"R_{tot} = 0,22 \cdot 10^{3} + 0,3197 \cdot 10^{3} = "
                r"0,5397 \cdot 10^{3} \u{ Ω}",
            ing=r"R_{tot} \approx 540 \u{ Ω}")
        sol(alg=r"I_{1} = \f{U}{R_{tot}}",
            num=r"I_{1} = \f{10}{0,5397 \cdot 10^{3}} = 18,53 \cdot 10^{-3} \u{ A}",
            ing=r"I_{1} \approx 18,5 \u{ mA}")
        sol(alg=r"U_{1} = R_{1} \cdot I_{1}",
            num=r"U_{1} = 0,22 \cdot 10^{3} \cdot 18,53 \cdot 10^{-3} = 4,08 \u{ V}",
            ing=r"U_{1} \approx 4,08 \u{ V}")
        sol(alg=r"U_{23} = U - U_{1}",
            num=r"U_{23} = 10 - 4,08 = 5,92 \u{ V}",
            ing=r"U_{23} \approx 5,92 \u{ V}")
        sol(alg=r"I_{2} = \f{U_{23}}{R_{2}}",
            num=r"I_{2} = \f{5,92}{0,47 \cdot 10^{3}} = 12,60 \cdot 10^{-3} \u{ A}",
            ing=r"I_{2} \approx 12,6 \u{ mA}")
        sol(alg=r"I_{3} = \f{U_{23}}{R_{3}}",
            num=r"I_{3} = \f{5,92}{1 \cdot 10^{3}} = 5,92 \cdot 10^{-3} \u{ A}",
            ing=r"I_{3} \approx 5,92 \u{ mA}")
    calc = [("R_{23}", "320 Ω"), ("R_{tot}", "540 Ω"), ("I_{1}", "18,5 mA"),
            ("U_{1}", "4,08 V"), ("U_{23}", "5,92 V"), ("I_{2}", "12,6 mA"),
            ("I_{3}", "5,92 mA")]
    rows = [["Grandeur", "Valeur calculée", "Valeur mesurée", "Écart [%]"]]
    for nom, val in calc:
        rows.append([(nom, dict(bold=True)), cell_rep(val), "", ""])
    B.append(table([1701, 2268, 2268, 1701], rows))
    B.append(EMPTY)
    B.append(para(rich("b)  Matériel utilisé — à compléter pendant le TP"), after=100,
                  ind=340, keep=True))
    rows = [["Appareil", "Modèle", "N° d’inventaire"]]
    for a in ("Alimentation", "Multimètre 1", "Multimètre 2"):
        rows.append([(a, dict(jc="left")), "", ""])
    B.append(table([2551, 2835, 2835], rows))
    B.append(EMPTY)
    q("c)  Les écarts relevés sont-ils explicables par la tolérance des résistances ? "
      "Justifie.")
    sol(txt="Oui si l’écart reste de l’ordre de quelques pour-cent : avec ±5 % sur chaque "
            "résistance, R_{tot} peut varier d’environ ±5 %, donc le courant aussi. "
            "Un écart de plusieurs dizaines de pour-cent viendrait d’une erreur de montage "
            "ou de calibre.", lines=3)
    q("d)  Que vaudrait le courant total I₁ si on débranchait R₃ ?")
    sol(alg=r"I_{1} = \f{U}{R_{1} + R_{2}}",
        num=r"I_{1} = \f{10}{0,22 \cdot 10^{3} + 0,47 \cdot 10^{3}} = "
            r"\f{10}{0,69 \cdot 10^{3}} = 14,49 \cdot 10^{-3} \u{ A}",
        ing=r"I_{1} \approx 14,5 \u{ mA}")
    if corrige:
        B.append(para(rich("Le courant DIMINUE quand on enlève une branche parallèle : "
                           "la résistance totale augmente.", color=RED),
                      after=60, ind=340))
    q("e)  Un camarade branche l’ampèremètre en parallèle sur R₂. Que se passe-t-il ?")
    sol(txt="L’ampèremètre a une résistance quasi nulle : il court-circuite R₂. "
            "Le courant devient bien trop grand et le fusible de l’appareil fond.",
        lines=3)

    # ================================================================ auto-évaluation
    B.extend([EMPTY, EMPTY, HR])
    B.append(para(rich("Auto-évaluation — coche honnêtement, c’est pour toi"),
                  tabs=[5103], after=120, keep=True))
    crit = [("Je repère série et parallèle sur un schéma inhabituel", "LZ 1923"),
            ("Je réduis un circuit de 5 résistances en montrant chaque étape", "LZ 1923"),
            ("J’applique les lois des nœuds et des mailles pour contrôler", "LZ 1924"),
            ("Je pose mes calculs en trois temps : formule, nombres, résultat",
             "LZ 1924"),
            ("Mon tableau R/U/I/P est complet, avec unités et préfixes", "LZ 1924"),
            ("Mon schéma respecte les sept règles de dessin", "LZ 1952"),
            ("Je câble et je mesure sans faute de branchement", "LZ 1949"),
            ("Mon protocole est complet et ma conclusion justifie l’écart",
             "LZ 7857/7995")]
    rows = [["Je sais…", "Réf.", "Pas encore", "Presque", "Acquis"]]
    for c, lz in crit:
        rows.append([(c, dict(jc="left")), (lz, {}), "", "", ""])
    B.append(table([3685, 1418, 1276, 1134, 1134], rows))

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
    name = ("150 EX C Circuits mixtes.docx" if corrige
            else "150 EX Circuits mixtes.docx")
    out = os.path.join(OUTDIR, name)
    if os.path.exists(out):
        os.remove(out)
    subprocess.run(["zip", "-Xqr", os.path.abspath(out), "."], cwd=WORK, check=True)
    print("saved", out)
    return out


if __name__ == "__main__":
    make(True)
    make(False)
