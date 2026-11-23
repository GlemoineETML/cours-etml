# -*- coding: utf-8 -*-
"""540 TEST — Régime impulsionnel RC, RL (élève + corrigé).

Deux exercices calqués sur les N°3 et N°4 de la fiche « 540 EX Régime
impulsionnel RC RL 1 », valeurs changées. 30 minutes, 20 points.
Corrigé : ① forme algébrique ② application numérique ③ notation ingénieur.
Résultats recalculés indépendamment dans verif540.py (formules + simulation).
"""
import os, re, shutil, zipfile, subprocess
from docx_helpers import *
from mathml import omath

TITRE = "Régime impulsionnel RC, RL"
NUMERO = "TEST"
ANNEE = "2026-2027"
TOTAL = 20
DUREE = "30 minutes"
OUTDIR = "out"
WORK = "work_test540"
GREY = "7F8FA9"
MSZ = 22
GRILLES = [("rIdT1", "E1_circuit.png", "E1_circuit.png"),
           ("rIdT2", "E1_grille.png", "E1c_grille.png"),
           ("rIdT3", "E2_circuit.png", "E2_circuit.png"),
           ("rIdT4", "E2_grille.png", "E2c_grille.png")]


def para_droite(gauche, droite, after=120, before=0, keep=False):
    ppr = "<w:keepNext/><w:keepLines/>" if keep else ""
    ppr += '<w:tabs><w:tab w:val="right" w:pos="9070"/></w:tabs>'
    ppr += '<w:spacing w:before="%d" w:after="%d"/>' % (before, after)
    return "<w:p><w:pPr>%s</w:pPr>%s%s%s</w:p>" % (ppr, gauche, run(tab=True), droite)


def pts_txt(p):
    return "%s pt%s" % (str(p).replace(".", ","), "s" if p > 1 else "")


def build(corrige):
    B, bareme = [], []

    def exercice(num, titre, pts):
        bareme.append((num, titre, pts))
        if B:
            B.extend([EMPTY, HR])
        # préférence Gael : pas de tabulation après « N°n », le titre suit directement
        B.append(para_droite(run("N°%d  " % num, bold=True) + rich(titre, bold=True),
                             run(pts_txt(pts), sz="18"), after=120, keep=True))

    def enonce(txt, after=100, keep=False):
        B.append(para(rich(txt), after=after, keep=keep))

    def q(txt, pts, keep=True):
        B.append(para_droite(rich(txt), run(pts_txt(pts), sz="18", color=GREY),
                             after=60, before=60, keep=keep))

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
                B.append(para(rich(note, sz="16", color=GREY, italic=True), ind=567, after=80))
        else:
            n = lines if lines else (1 if txt and not alg else sum(1 for x in (alg, num, ing) if x))
            for _ in range(max(n, 1)):
                B.append(para(run(tab=True), leader=9350, before=90, after=90, ind=340))

    # ================================================================ N°1
    exercice(1, "Impulsion appliquée à un circuit RC (sortie sur R)", 10)
    enonce("L’impulsion de la grille ci-dessous (U = 15 V, durée 8 ms) est appliquée au "
           "circuit. État initial : le condensateur est déchargé, u_{s} = 0 V. "
           "Le front descendant a lieu à t = 8 ms. Le générateur est idéal "
           "(résistance interne nulle).", keep=True)
    B.append(image("rIdT1", 3.9, 3.9 * 0.4821, 1))

    q("a)  Calcule la constante de temps τ.", 1)
    sol(alg=r"\tau = R_{1} \cdot C_{1}",
        num=r"\tau = 1,5 \cdot 10^{3} \cdot 2,2 \cdot 10^{-6} = 3,3 \cdot 10^{-3} \u{ [s]}",
        ing=r"\tau = 3,3 \u{ [ms]}", note="Barème : 1 pt.")

    q("b)  Donne la valeur de la crête positive de u_{s} et l’instant où elle se "
      "produit. Justifie en une phrase.", 1)
    sol(txt="u_{s} = +15 V à t = 0 : la tension d’un condensateur ne peut pas varier "
            "instantanément, u_{C} reste à 0 V et tout le saut de 15 V se retrouve "
            "sur R_{1}.", lines=2,
        note="Barème : 0,5 pt pour la valeur, 0,5 pt pour la justification.")

    q("c)  Calcule u_{s} à t_{1} = 7,999 ms (juste avant le front descendant).", 2)
    sol(alg=r"u_{s}(t_{1}) = U \cdot e^{\minus\f{t_{1}}{\tau}}",
        num=r"u_{s}(t_{1}) = 15 \cdot e^{\minus\f{7,999 \cdot 10^{-3}}{3,3 \cdot 10^{-3}}}"
            r" = 15 \cdot 0,08857 = 1,329 \u{ [V]}",
        ing=r"u_{s}(t_{1}) = 1,329 \u{ [V]}",
        note="Barème : 2 pts — 1 formule, 1 calcul avec unité. Variante acceptée : "
             "u_{s} = U − u_{C} = 15 − 15 · (1 − e^{−t/τ}), même résultat.")

    q("d)  Calcule u_{s} à t_{2} = 8,001 ms (juste après le front descendant). "
      "C’est la crête négative.", 2)
    sol(txt="Au front descendant, u_{e} chute de 15 V d’un coup ; u_{C} ne change pas, "
            "donc u_{s} chute aussi de 15 V.",
        alg=r"u_{s}(t_{2}) = u_{s}(t_{1}) \minus U",
        num=r"u_{s}(t_{2}) = 1,329 \minus 15 = \minus13,67 \u{ [V]}",
        ing=r"u_{s}(t_{2}) = \minus13,67 \u{ [V]}", lines=3,
        note="Barème : 2 pts — 1 pt pour le raisonnement (saut de −15 V), 1 pt pour la valeur "
             "et le signe. Le signe négatif oublié = 1 pt au maximum. La décroissance "
             "pendant les 2 µs entre 8,000 et 8,001 ms est négligeable (−13,668 V).")

    q("e)  Calcule l’instant t_{3} où u_{s} remonte à −200 mV.", 2)
    sol(alg=r"\Delta t = \tau \cdot \u{ln}\f{u_{s}(t_{2})}{u_{s}(t_{3})}",
        num=r"\Delta t = 3,3 \cdot 10^{-3} \cdot \u{ln}\f{\minus13,67}{\minus0,2}"
            r" = 3,3 \cdot 10^{-3} \cdot 4,225 = 13,94 \cdot 10^{-3} \u{ [s]}",
        ing=r"\Delta t = 13,94 \u{ [ms]} ;   t_{3} = t_{2} + \Delta t \approx 8 + 13,94 = 21,94 \u{ [ms]}", lines=4,
        note="Barème : 2 pts — 1 pt pour Δt, 1 pt pour avoir ajouté t₂ ≈ 8 ms "
             "(Δt se compte depuis le front descendant, t₃ depuis le début de l’impulsion).")

    q("f)  Dessine u_{s} sur la grille, par-dessus u_{e}. Reporte les valeurs "
      "calculées en c), d) et e).", 2)
    B.append(image("rIdT2", 6.3, 6.3 * 0.5305, 2))
    if corrige:
        B.append(para(rich("Barème : 2 pts — 0,5 pt pour le saut 0 → +15 V à t = 0 puis la décroissance "
                          "jusqu’à 1,329 V, 0,5 pt pour le saut vertical de −15 V (jusqu’à −13,67 V) "
                          "à t = 8 ms, 0,5 pt pour la remontée exponentielle vers 0 sans dépasser 0 V, "
                          "0,5 pt pour les valeurs reportées. Repères de contrôle à 1 τ : 5,52 V à "
                          "3,3 ms et −5,03 V à 11,3 ms (37 % de la valeur de départ).", sz="16", color=GREY,
                          italic=True), ind=567, after=80))

    # ================================================================ N°2
    exercice(2, "Impulsion appliquée à un circuit RL (sortie sur R)", 10)
    enonce("L’impulsion de la grille (U = 20 V, durée t_{p} = 6 ms) est appliquée au "
           "circuit ci-dessous. La bobine et le générateur sont idéaux. "
           "État initial : i = 0 A, u_{s} = 0 V.", keep=True)
    B.append(image("rIdT3", 3.9, 3.9 * 0.4821, 3))

    q("a)  Calcule la constante de temps τ et le courant maximal I que le circuit "
      "atteindrait en régime établi.", 2)
    sol(alg=r"\tau = \f{L_{1}}{R_{1}}",
        num=r"\tau = \f{150 \cdot 10^{-3}}{56} = 2,679 \cdot 10^{-3} \u{ [s]}",
        ing=r"\tau = 2,679 \u{ [ms]}", lines=2)
    sol(alg=r"I = \f{U}{R_{1}}",
        num=r"I = \f{20}{56} = 357,1 \cdot 10^{-3} \u{ [A]}",
        ing=r"I = 357,1 \u{ [mA]}", lines=1,
        note="Barème : 1 pt pour τ, 1 pt pour I.")

    q("b)  Calcule la tension maximale de sortie (à la fin de l’impulsion).", 3)
    sol(txt="Le régime n’est pas établi : 6 ms < 5τ = 13,4 ms. La tension maximale est "
            "atteinte à t = 6 ms.",
        alg=r"i(t) = I \cdot (1 \minus e^{\minus\f{t}{\tau}})",
        num=r"i = 357,1 \cdot 10^{-3} \cdot (1 \minus e^{\minus\f{6 \cdot 10^{-3}}"
            r"{2,679 \cdot 10^{-3}}}) = 357,1 \cdot 10^{-3} \cdot 0,8935 = 319,1 \cdot 10^{-3} \u{ [A]}",
        ing=r"i = 319,1 \u{ [mA]}", lines=4)
    sol(alg=r"u_{s max} = R_{1} \cdot i",
        num=r"u_{s max} = 56 \cdot 319,1 \cdot 10^{-3} = 17,87 \u{ [V]}",
        ing=r"u_{s max} = 17,87 \u{ [V]}", lines=1,
        note="Barème : 3 pts — 0,5 pt pour avoir vu que 5τ > 6 ms, 1,5 pt pour i, "
             "1 pt pour u_{s}. Répondre 20 V = 0 pt (régime établi supposé à tort).")

    q("c)  Calcule la valeur de R_{1} pour que u_{s} atteigne pratiquement 20 V "
      "(régime établi) à la fin de l’impulsion. Contrôle ensuite u_{s} à t = 6 ms.", 2)
    sol(txt="Le régime est considéré comme établi après 5τ.",
        alg=r"5 \tau = t_{p} \Rightarrow \tau = \f{t_{p}}{5} ;   R_{1} = \f{L_{1}}{\tau}",
        num=r"\tau = \f{6 \cdot 10^{-3}}{5} = 1,2 \cdot 10^{-3} \u{ [s]} ;   "
            r"R_{1} = \f{150 \cdot 10^{-3}}{1,2 \cdot 10^{-3}} = 125 \u{ [}\ohm\u{]}",
        ing=r"R_{1} = 125 \u{ [}\ohm\u{]}", lines=3)
    sol(txt="Contrôle : à t = t_{p} = 5τ, il reste e^{−5} = 0,7 % à parcourir.",
        alg=r"u_{s}(t_{p}) = U \cdot (1 \minus e^{\minus\f{t_{p}}{\tau}}) = U \cdot (1 \minus e^{\minus5})",
        num=r"u_{s}(t_{p}) = 20 \cdot (1 \minus 0,00674) = 19,87 \u{ [V]}",
        lines=2,
        note="Barème : 2 pts — 1,5 pt pour R₁ = 125 Ω, 0,5 pt pour le contrôle "
             "(99,3 % de 20 V).")

    q("d)  On ne trouve que des résistances de la série E12. Choisis la valeur à "
      "monter et justifie.", 1)
    sol(txt="R_{1} = 150 Ω. Il faut τ ≤ 1,2 ms, donc R_{1} ≥ 125 Ω. Avec 150 Ω : "
            "τ = 1 ms et 5τ = 5 ms < 6 ms. Avec 120 Ω : 5τ = 6,25 ms > 6 ms, trop lent.",
        lines=3,
        note="Barème : 1 pt — 0,5 pt pour 150 Ω, 0,5 pt pour la justification. "
             "« La plus proche » (120 Ω) sans contrôle = 0 pt.")

    q("e)  Pour R_{1} = 56 Ω, dessine u_{s} sur la grille, par-dessus u_{e}. "
      "Reporte u_{s max} et τ.", 2)
    B.append(image("rIdT4", 6.3, 6.3 * 0.4483, 4))
    if corrige:
        B.append(para(rich("Barème : 2 pts — 1 pt pour la montée (63 % = 12,64 V à τ = 2,68 ms, 17,87 V à 6 ms), "
                          "1 pt pour la descente exponentielle depuis 17,87 V (37 % = 6,57 V à "
                          "8,68 ms, ≈ 0 vers 19,4 ms). La courbe est continue à 6 ms : le courant "
                          "dans la bobine ne peut pas varier instantanément, donc u_{s} ne saute pas.", sz="16", color=GREY, italic=True),
                      ind=567, after=80))

    # ---------------------------------------------------------- récapitulatif
    if corrige:
        B.extend([EMPTY, HR])
        B.append(para(rich("Récapitulatif du barème"), after=120, keep=True))
        rows = [["Exercice", "Sujet", "Points"]]
        for num, titre, pts in bareme:
            rows.append([("N°%d" % num, {}), (titre, dict(jc="left")), (str(pts), {})])
        rows.append([("", {}), ("Total", dict(jc="left", bold=True)), (str(TOTAL), dict(bold=True))])
        B.append(table([1560, 5800, 1560], rows))
        B.append(para(rich("Note = 1 + 5 · points obtenus / %d, arrondie au dixième." % TOTAL),
                      before=160, after=60))
        B.append(para(rich("Durée prévue : %s. Seuil de suffisance (note 4) : 12 points." % DUREE),
                      after=60))
    return "".join(B)


def make(corrige):
    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    with zipfile.ZipFile(SRC) as z:
        z.extractall(WORK)
    os.makedirs(f"{WORK}/word/media", exist_ok=True)
    rels = f"{WORK}/word/_rels/document.xml.rels"
    t = open(rels, encoding="utf8").read()
    add = ""
    for rid, fe, fc in GRILLES:
        shutil.copy("fig/" + (fc if corrige else fe), f"{WORK}/word/media/{rid}.png")
        add += ('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/'
                'officeDocument/2006/relationships/image" Target="media/%s.png"/>' % (rid, rid))
    open(rels, "w", encoding="utf8").write(t.replace("</Relationships>", add + "</Relationships>"))
    ct = f"{WORK}/[Content_Types].xml"
    t = open(ct, encoding="utf8").read()
    if 'Extension="png"' not in t:
        t = t.replace('<Default Extension="rels"',
                      '<Default Extension="png" ContentType="image/png"/><Default Extension="rels"')
    open(ct, "w", encoding="utf8").write(t)

    doc = f"{WORK}/word/document.xml"
    t = open(doc, encoding="utf8").read()
    sectpr = re.search(r"<w:sectPr .*?</w:sectPr>", t, re.S).group(0)
    entete = (
        para(run("%s    %s" % (NUMERO, ANNEE), style="Accentuation", sz="32")
             + run(tab=True, style="Accentuation") + run("Date :", style="Accentuation"),
             tabs=[6237], after=60)
        + para((run("Corrigé — " + TITRE, style="Accentuation", color=RED) if corrige
                else run(TITRE, style="Accentuation"))
               + run(tab=True, style="Accentuation") + run("Nom :", style="Accentuation"),
               tabs=[6237], after=60)
        + para(run("Matériel : calculette et formulaire personnel", sz="20") + run(tab=True)
               + run("Points :          / %d" % TOTAL, sz="20"), tabs=[6237], after=60)
        + HR)
    body = entete + build(corrige) + sectpr
    t = re.sub(r"<w:body>.*</w:body>", "<w:body>" + body + "</w:body>", t, flags=re.S)
    open(doc, "w", encoding="utf8").write(t)
    os.makedirs(OUTDIR, exist_ok=True)
    name = ("540 TEST C Regime impulsionnel RC RL.docx" if corrige
            else "540 TEST Regime impulsionnel RC RL.docx")
    out = os.path.join(OUTDIR, name)
    if os.path.exists(out):
        os.remove(out)
    subprocess.run(["zip", "-Xqr", os.path.abspath(out), "."], cwd=WORK, check=True)
    print("saved", out)


if __name__ == "__main__":
    make(True)
    make(False)
