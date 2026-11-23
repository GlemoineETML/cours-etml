# -*- coding: utf-8 -*-
"""310 EX — Champ électrique et condensateur (élève + corrigé).

Corrigé : chaque réponse est développée en trois temps —
  ① forme algébrique   ② application numérique en puissances de 10   ③ notation ingénieur
Les expressions sont de vraies équations Word (OMML), pas du texte.
"""
import os, re, shutil, zipfile, subprocess
from docx_helpers import *
from mathml import omath

TITRE = "Champ électrique et condensateur"
OUTDIR = "out"
WORK = "work_docx4"
GREY = "7F8FA9"
MSZ = 22          # taille des équations (demi-points) → 11 pt

GRILLES = [("rIdG1", "60_lignes_champ.png", "60_lignes_champ.png"),
           ("rIdG2", "62_condo_plan.png", "62_condo_plan.png"),
           ("rIdG3", "69_ex4_reseau.png", "69_ex4_reseau.png"),
           ("rIdG4", "68_ex5_circuit.png", "68_ex5_circuit.png"),
           ("rIdG5", "84_ex5_courbe.png", "84c_ex5_courbe.png"),
           ("rIdG6", "65_circuit_charge.png", "65_circuit_charge.png"),
           ("rIdG7", "67_ex7_circuit.png", "67_ex7_circuit.png"),
           ("rIdG8", "85_grilles.png", "85c_grilles.png")]


def build(corrige):
    B = []

    def q(txt, after=60, keep=False):
        B.append(para(rich(txt), after=after, ind=340, keep=keep))

    def enonce(txt, after=120):
        B.append(para(rich(txt), after=after))

    def ex(num, titre):
        if B:
            B.extend([EMPTY, EMPTY, HR])
        B.append(para(rich(f"N°{num} {titre}"), tabs=[5103], after=120, keep=True))

    def etape(label, expr):
        return para(run(label + "   ", sz="16", color=RED, italic=True)
                    + omath(expr, color=RED, sz=MSZ),
                    ind=567, before=40, after=40, keep=True)

    def sol(alg=None, num=None, ing=None, txt=None, lines=None):
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

    # ================================================================ N°1
    ex(1, "Le champ électrique — ce que montrent les lignes")
    enonce("Observe les deux représentations ci-dessous.", after=60)
    B.append(image("rIdG1", 6.3, 2.31, 1))
    q("a)  Que représentent les lignes d’un champ électrique ? Réponds en une phrase.")
    sol(txt="Elles représentent la direction de la force qu’une charge subirait en "
            "chaque point : la force est tangente à la ligne.", lines=2)
    q("b)  Que donne le sens des flèches ? Et l’écartement entre deux lignes ?")
    sol(txt="Le sens de la force sur une charge POSITIVE ; l’écartement donne "
            "l’intensité — serrées : champ fort, écartées : champ faible.", lines=2)
    q("c)  Cite deux règles de tracé que les lignes respectent toujours.")
    sol(txt="Elles partent du + et arrivent au −, et elles ne se croisent jamais "
            "(en un point la force n’a qu’une direction). Elles sont aussi "
            "perpendiculaires aux surfaces conductrices.", lines=2)
    q("d)  Entre les deux armatures planes du schéma b), que peut-on dire du champ ?")
    sol(txt="Les lignes sont parallèles et régulièrement espacées : le champ est "
            "uniforme, il a la même valeur partout.", lines=2)

    # ================================================================ N°2
    ex(2, "Champ dans un condensateur plan")
    enonce("Un condensateur plan est soumis à U = 250 V. L’isolant a une épaisseur "
           "d = 0,5 mm.", after=60)
    B.append(image("rIdG2", 5.5, 1.92, 2))
    q("a)  Calcule l’intensité du champ électrique entre les armatures.")
    sol(alg=r"E = \f{U}{d}",
        num=r"E = \f{250}{0,5 \cdot 10^{-3}} = 0,5 \cdot 10^{6} \u{ V/m}",
        ing=r"E = 500 \u{ kV/m} = 0,5 \u{ kV/mm}")
    q("b)  L’isolant supporte au maximum 15 kV/mm. Quelle tension peut-on appliquer "
      "sans le percer ?")
    sol(alg=r"U_{max} = E_{max} \cdot d",
        num=r"U_{max} = 15 \cdot 10^{3} \cdot 0,5 = 7,5 \cdot 10^{3} \u{ V}",
        ing=r"U_{max} = 7,5 \u{ kV}")
    q("c)  Que se passe-t-il au-delà de cette tension ?")
    sol(txt="L’isolant claque : un arc le traverse et le condensateur est détruit. "
            "C’est pour cela qu’un condensateur porte une tension de service.",
        lines=2)

    # ================================================================ N°3
    ex(3, "Charge stockée, énergie et décharge")
    enonce("Un condensateur de C = 470 µF est chargé sous U = 25 V.", after=60)
    q("a)  Quelle quantité d’électricité a-t-il stockée ?")
    sol(alg=r"Q = C \cdot U",
        num=r"Q = 470 \cdot 10^{-6} \cdot 25 = 11,75 \cdot 10^{-3} \u{ C}",
        ing=r"Q = 11,75 \u{ mC}")
    q("b)  Quelle énergie contient-il ?")
    sol(alg=r"W = \f{1}{2} \cdot C \cdot U^{2}",
        num=r"W = 0,5 \cdot 470 \cdot 10^{-6} \cdot 625 = 146,9 \cdot 10^{-3} \u{ J}",
        ing=r"W = 146,9 \u{ mJ}")
    q("c)  On le décharge dans un circuit qui maintient un courant constant de 5 mA. "
      "Combien de temps met-il à se vider ?")
    sol(alg=r"t = \f{Q}{I}",
        num=r"t = \f{11,75 \cdot 10^{-3}}{5 \cdot 10^{-3}} = 2,35 \u{ s}",
        ing=r"t = 2,35 \u{ s}")
    q("d)  Pourquoi faut-il décharger un condensateur avant d’intervenir sur une carte ?")
    sol(txt="Parce qu’il garde sa charge et sa tension après la coupure de "
            "l’alimentation : il peut encore délivrer un courant dangereux.",
        lines=2)

    # ================================================================ N°4
    ex(4, "Capacité équivalente entre A et B")
    B.append(image("rIdG3", 6.0, 3.23, 3))
    q("a)  Quels condensateurs sont en série ? Lesquels sont en parallèle avec "
      "l’ensemble A–B ?", keep=True)
    sol(txt="C₂ et C₃ sont en série. C₅ est en parallèle avec tout le reste, "
            "entre A et B.", lines=2)
    q("b)  Réduis le montage étape par étape jusqu’à C_{AB}.")
    sol(alg=r"C_{23} = \f{C_{2} \cdot C_{3}}{C_{2} + C_{3}}",
        num=r"C_{23} = \f{6 \cdot 10^{-6} \cdot 3 \cdot 10^{-6}}"
            r"{9 \cdot 10^{-6}} = 2 \cdot 10^{-6} \u{ F}",
        ing=r"C_{23} = 2 \u{ µF}")
    sol(alg=r"C_{234} = C_{23} + C_{4}",
        num=r"C_{234} = 2 \cdot 10^{-6} + 8 \cdot 10^{-6} = 10 \cdot 10^{-6} \u{ F}",
        ing=r"C_{234} = 10 \u{ µF}")
    sol(alg=r"C_{1234} = \f{C_{1} \cdot C_{234}}{C_{1} + C_{234}}",
        num=r"C_{1234} = \f{15 \cdot 10^{-6} \cdot 10 \cdot 10^{-6}}"
            r"{25 \cdot 10^{-6}} = 6 \cdot 10^{-6} \u{ F}",
        ing=r"C_{1234} = 6 \u{ µF}")
    sol(alg=r"C_{AB} = C_{1234} + C_{5}",
        num=r"C_{AB} = 6 \cdot 10^{-6} + 4 \cdot 10^{-6} = 10 \cdot 10^{-6} \u{ F}",
        ing=r"C_{AB} = 10 \u{ µF}")
    q("c)  Contrôle de bon sens : C_{AB} peut-il être plus petit que C_{5} ? Pourquoi ?")
    sol(txt="Non. C₅ est en parallèle avec le reste, donc on lui ajoute quelque "
            "chose : C_AB ≥ C₅ = 4 µF.", lines=2)

    # ================================================================ N°5
    ex(5, "Retrouver une capacité inconnue")
    enonce("On ferme S à t = 0 et on relève le courant de charge à l’oscilloscope. "
           "On lit i_{C} = 5 mA à t = 33 µs.", after=60)
    B.append(image("rIdG4", 4.3, 2.30, 4))
    B.append(image("rIdG5", 5.6, 2.72, 5))
    q("a)  Calcule le courant au tout premier instant, I₀.", keep=True)
    sol(alg=r"I_{0} = \f{U}{R}",
        num=r"I_{0} = \f{10}{1 \cdot 10^{3}} = 10 \cdot 10^{-3} \u{ A}",
        ing=r"I_{0} = 10 \u{ mA}")
    q("b)  Que vaut le rapport i_{C} / I₀ au point lu ? Qu’en déduis-tu sur t ?")
    sol(txt="i / I₀ = 5 / 10 = 0,5 : le point lu est la demi-valeur, "
            "donc t = τ · ln 2.", lines=2)
    q("c)  Calcule la constante de temps τ.")
    sol(alg=r"\tau = \f{t}{\u{ln} 2}",
        num=r"\tau = \f{33 \cdot 10^{-6}}{0,693} = 47,6 \cdot 10^{-6} \u{ s}",
        ing=r"\tau = 47,6 \u{ µs}")
    q("d)  Calcule C_{x}, puis donne la valeur normalisée E12 la plus proche.")
    sol(alg=r"C_{x} = \f{\tau}{R}",
        num=r"C_{x} = \f{47,6 \cdot 10^{-6}}{1 \cdot 10^{3}} "
            r"= 47,6 \cdot 10^{-9} \u{ F}",
        ing=r"C_{x} = 47,6 \u{ nF} \approx 47 \u{ nF}")

    # ================================================================ N°6
    ex(6, "La charge d’un circuit RC")
    enonce("E = 10 V, R = 5 kΩ, C = 2 µF. On ferme S à t = 0, le condensateur est "
           "vide.", after=60)
    B.append(image("rIdG6", 4.8, 2.48, 6))
    q("a)  Calcule la constante de temps τ et le courant initial I₀.", keep=True)
    sol(alg=r"\tau = R \cdot C",
        num=r"\tau = 5 \cdot 10^{3} \cdot 2 \cdot 10^{-6} = 10 \cdot 10^{-3} \u{ s}",
        ing=r"\tau = 10 \u{ ms}")
    sol(alg=r"I_{0} = \f{E}{R}",
        num=r"I_{0} = \f{10}{5 \cdot 10^{3}} = 2 \cdot 10^{-3} \u{ A}",
        ing=r"I_{0} = 2 \u{ mA}")
    q("b)  Quelle tension le condensateur a-t-il atteint au bout d’un τ ?")
    sol(alg=r"u_{C}(\tau) = E \cdot (1 - e^{-1}) = 0,632 \cdot E",
        num=r"u_{C}(\tau) = 0,632 \cdot 10 = 6,32 \u{ V}",
        ing=r"u_{C}(\tau) = 6,32 \u{ V}")
    q("c)  Au bout de combien de temps atteint-il 5 V ?")
    sol(alg=r"5 = E \cdot (1 - e^{-t/\tau}) \to e^{-t/\tau} = 0,5 "
            r"\to t = \tau \cdot \u{ln} 2",
        num=r"t = 10 \cdot 10^{-3} \cdot 0,693 = 6,93 \cdot 10^{-3} \u{ s}",
        ing=r"t = 6,93 \u{ ms}")
    q("d)  Au bout de combien de temps considère-t-on la charge terminée ?")
    sol(alg=r"t = 5 \cdot \tau",
        num=r"t = 5 \cdot 10 \cdot 10^{-3} = 50 \cdot 10^{-3} \u{ s}",
        ing=r"t = 50 \u{ ms}")

    # ================================================================ N°7
    ex(7, "Régime établi, puis ouverture de S")
    enonce("S est fermé depuis longtemps : le condensateur est complètement chargé. "
           "À t = 0 on ouvre S.", after=60)
    B.append(image("rIdG7", 5.6, 2.72, 7))
    q("a)  En régime établi, que vaut i_{C} ? Qu’en déduis-tu pour U_{C} max ?",
      keep=True)
    sol(txt="i_C = 0 : le condensateur est un circuit ouvert. U_C max est donc la "
            "tension aux bornes de R₂, donnée par le diviseur R₁ – R₂.", lines=2)
    sol(alg=r"U_{C max} = E \cdot \f{R_{2}}{R_{1} + R_{2}}",
        num=r"U_{C max} = 18 \cdot \f{40}{20 + 40} = 18 \cdot 0,667",
        ing=r"U_{C max} = 12 \u{ V}")
    q("b)  Une fois S ouvert, dans quelle résistance le condensateur se décharge-t-il ? "
      "Justifie.")
    sol(txt="Dans R₂ seule : l’ouverture de S coupe la branche de E et de R₁, "
            "qui ne font plus partie du circuit.", lines=2)
    q("c)  Calcule la constante de temps τ.")
    sol(alg=r"\tau = R_{2} \cdot C",
        num=r"\tau = 40 \cdot 2,5 \cdot 10^{-6} = 100 \cdot 10^{-6} \u{ s}",
        ing=r"\tau = 100 \u{ µs}")
    q("d)  Calcule I_{C} max, le courant au tout premier instant de la décharge.")
    sol(alg=r"I_{C max} = \f{U_{C max}}{R_{2}}",
        num=r"I_{C max} = \f{12}{40} = 0,3 \u{ A}",
        ing=r"I_{C max} = 300 \u{ mA}")
    q("e)  Trace u_{C} = f(t) et i_{C} = f(t) sur les deux graphes. Gradue les axes, "
      "écris la grandeur et l’unité de chaque axe, et reporte τ, U_{C} max et "
      "I_{C} max.", keep=True)
    B.append(image("rIdG8", 6.5, 2.01, 8))
    if corrige:
        B.append(para(rich("Les deux courbes partent de leur maximum et décroissent. "
                           "À un τ = 100 µs il reste 37 % : 4,4 V et 110 mA. "
                           "Après 5 τ = 500 µs, tout est retombé à zéro.",
                           color=RED), ind=340, after=60))

    # ---------------------------------------------------------- auto-évaluation
    B.extend([EMPTY, EMPTY, HR])
    B.append(para(rich("Où j’en suis"), tabs=[5103], after=120, keep=True))
    B.append(para(rich("Coche honnêtement avant de regarder le corrigé."),
                  after=120))
    crit = [
        ("J’explique ce que représentent les lignes d’un champ électrique", "N°1"),
        ("J’applique E = U/d et je vérifie la tenue de l’isolant", "N°2"),
        ("Je calcule Q, W et un temps de décharge", "N°3"),
        ("Je réduis un réseau de condensateurs en montrant chaque étape", "N°4"),
        ("Je retrouve C à partir d’un point lu sur une courbe", "N°5"),
        ("Je calcule τ, I₀ et un temps de charge", "N°6"),
        ("Je pars du régime établi et je trouve la bonne résistance de décharge", "N°7"),
        ("Je pose mes calculs en trois temps : formule, nombres, résultat", "tous"),
        ("Mes graphes portent la grandeur, l’unité et les valeurs calculées", "N°7"),
    ]
    rows = [["Je sais…", "Réf.", "Pas encore", "Presque", "Acquis"]]
    for c, r in crit:
        rows.append([(c, dict(jc="left")), (r, {}), "", "", ""])
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
    fin = ('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="20" '
           'w:lineRule="exact"/><w:rPr><w:sz w:val="2"/></w:rPr></w:pPr></w:p>')
    body = entete + build(corrige) + fin + sectpr
    t = re.sub(r"<w:body>.*</w:body>", "<w:body>" + body + "</w:body>", t, flags=re.S)
    open(doc, "w", encoding="utf8").write(t)

    os.makedirs(OUTDIR, exist_ok=True)
    name = ("310 EX C Champ et condensateur.docx" if corrige
            else "310 EX Champ et condensateur.docx")
    out = os.path.join(OUTDIR, name)
    if os.path.exists(out):
        os.remove(out)
    subprocess.run(["zip", "-Xqr", os.path.abspath(out), "."], cwd=WORK, check=True)
    print("saved", out)
    return out


if __name__ == "__main__":
    make(True)
    make(False)
