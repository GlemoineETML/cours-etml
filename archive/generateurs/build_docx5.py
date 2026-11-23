# -*- coding: utf-8 -*-
"""510 EX — Les appareils de mesure et leur influence (élève + corrigé).

Corrigé : chaque réponse est développée en trois temps —
  ① forme algébrique   ② application numérique en puissances de 10   ③ notation ingénieur
Les expressions sont de vraies équations Word (OMML), pas du texte.
"""
import os, re, shutil, zipfile, subprocess
from docx_helpers import *
from mathml import omath

TITRE = "Les appareils de mesure et leur influence"
OUTDIR = "out"
WORK = "work_docx5"
GREY = "7F8FA9"
MSZ = 22          # taille des équations (demi-points) → 11 pt

GRILLES = [("rIdG1", "96_ex1_placement.png", "96_ex1_placement.png"),
           ("rIdG2", "91_voltmetre.png", "91_voltmetre.png"),
           ("rIdG3", "97_ex3_diviseur.png", "97_ex3_diviseur.png"),
           ("rIdG4", "98_ex4_serie.png", "98_ex4_serie.png"),
           ("rIdG5", "99_ex5_ohmmetre.png", "99_ex5_ohmmetre.png"),
           ("rIdG7", "96_ex1_placement.png", "96c_ex1_corrige.png")]


def build(corrige):
    B = []

    def q(txt, after=60, keep=False):
        B.append(para(rich(txt), after=after, ind=340, keep=keep))

    def enonce(txt, after=120):
        B.append(para(rich(txt), after=after))

    def ex(num, titre):
        if B:
            B.extend([EMPTY, EMPTY, HR])
        B.append(para(rich(f"N°{num} {titre}"), tabs=[-9070], after=120, keep=True))

    def etape(label, expr):
        return para(run(label + "   ", sz="16", color=RED, italic=True)
                    + omath(expr, color=RED, sz=MSZ),
                    ind=567, before=40, after=40, keep=True)

    def sol(alg=None, num=None, ing=None, txt=None, lines=None, note=None):
        """note = commentaire en prose APRÈS les trois temps.

        Les mots restent hors des équations : les rendus OMML rabotent les
        espaces autour d'un mot glissé entre deux crochets.
        """
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
                B.append(para(rich(note, color=RED), before=20, after=60,
                              ind=567))
        else:
            n = lines if lines else (1 if txt and not alg else
                                     sum(1 for x in (alg, num, ing) if x))
            for _ in range(max(n, 1)):
                B.append(para(run(tab=True), leader=9350, before=70, after=70, ind=340))

    def boite_dessin(hauteur=2600):
        """Cadre vide pour que l'élève complète un schéma."""
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

    B.append(para(rich("Six exercices, 45 minutes en tout. Les 30 premières "
                       "minutes se font en classe ; ce qui reste se termine à la "
                       "maison. Le minutage indiqué à droite de chaque titre est "
                       "une aide, pas une limite."), after=60))
    B.append(para(rich("Tout résultat s’écrit avec son unité entre crochets — "
                       "24,0 [mA], 9,00 [V], 2,00 [MΩ] — et se pose en trois "
                       "temps : formule, nombres, résultat.", color=RED),
                  after=160))

    # ================================================================ N°1
    ex(1, "Placer les appareils\t8 min")
    enonce("Voici le montage à mesurer.", after=60)
    B.append(image("rIdG1", 6.2, 2.38, 1))
    q("a)  Redessine le schéma en y ajoutant un ampèremètre qui mesure le courant "
      "total et un voltmètre qui mesure la tension aux bornes de R_{2}. Symboles "
      "CEI, flèches de courant sur le fil, vecteur de tension à côté du "
      "voltmètre.", keep=True)
    if corrige:
        B.append(image("rIdG7", 6.2, 2.34, 7))
        B.append(para(rich("L’ampèremètre se place EN SÉRIE sur le fil qui sort de la "
                           "source ; le voltmètre se place EN PARALLÈLE, directement "
                           "aux bornes de R₂, sans couper de fil. Le vecteur U₂ se "
                           "dessine à côté du voltmètre, du + vers le −.", color=RED),
                      after=60, ind=340))
    else:
        B.append(boite_dessin(2600))
    q("b)  Calcule le courant total et la tension U_{2} du circuit SANS appareils.")
    sol(alg=r"I = \f{U}{R_{1} + R_{2}}",
        num=r"I = \f{24}{0,8 \cdot 10^{3}} = 30 \cdot 10^{-3} \u{ [A]}",
        ing=r"I = 30 \u{ [mA]}")
    sol(alg=r"U_{2} = R_{2} \cdot I",
        num=r"U_{2} = 0,47 \cdot 10^{3} \cdot 30 \cdot 10^{-3} = 14,1 \u{ [V]}",
        ing=r"U_{2} = 14,1 \u{ [V]}")
    q("c)  Que se passe-t-il si tu branches l’ampèremètre en parallèle sur R_{2} ?")
    sol(txt="Sa résistance est quasi nulle : il court-circuite R₂. Presque tout le "
            "courant passe par l’appareil, le fusible saute.", lines=2)

    # ================================================================ N°2
    ex(2, "Jusqu’où le multimètre reste-t-il honnête ?\t5 min")
    enonce("Le multimètre numérique du labo, un Fluke 87, annonce une résistance "
           "d’entrée de 10 MΩ, la même sur tous les calibres. La règle du "
           "voltmètre demande R_{V} ≥ 100 · R.", after=60)
    B.append(image("rIdG2", 6.2, 2.14, 2))
    q("a)  Tu mesures aux bornes d’une résistance de 10 kΩ. La règle est-elle "
      "tenue ?", keep=True)
    sol(alg=r"R_{V} \geq 100 \cdot R",
        num=r"100 \cdot 10 \cdot 10^{3} = 1 \cdot 10^{6} \u{ [Ω]}",
        ing=r"1 \u{ [MΩ]} \leq 10 \u{ [MΩ]}",
        note="La règle est tenue : le multimètre est assez grand pour cette résistance.")
    q("b)  Et aux bornes d’une résistance de 220 kΩ ?")
    sol(alg=r"R_{V} \geq 100 \cdot R",
        num=r"100 \cdot 220 \cdot 10^{3} = 22 \cdot 10^{6} \u{ [Ω]}",
        ing=r"22 \u{ [MΩ]} > 10 \u{ [MΩ]}",
        note="La règle n’est PAS tenue : le voltmètre va faire baisser la tension mesurée.")
    q("c)  Quelle est la plus grande résistance sur laquelle ce multimètre tient "
      "encore la règle ?")
    sol(alg=r"R \leq \f{R_{V}}{100}",
        num=r"R \leq \f{10 \cdot 10^{6}}{100} = 100 \cdot 10^{3} \u{ [Ω]}",
        ing=r"R \leq 100 \u{ [kΩ]}")
    q("d)  Que fais-tu quand tu dois quand même mesurer au-delà ?")
    sol(txt="On mesure, mais on calcule l’écart attendu et on l’annonce avec le "
            "résultat. La mesure reste utilisable tant qu’on sait de combien "
            "elle est fausse — ce qui est faux, c’est de la donner sans le dire.",
        lines=3)

    # ================================================================ N°3
    ex(3, "L’effet de charge d’un voltmètre numérique\t12 min")
    enonce("Le diviseur ci-dessous est alimenté sous 18 V. On mesure la tension aux "
           "bornes de R_{2} avec le multimètre numérique, dont la résistance "
           "d’entrée vaut 10 MΩ.", after=60)
    B.append(image("rIdG3", 5.6, 2.46, 3))
    q("a)  Quelle tension y a-t-il vraiment aux bornes de R_{2}, sans appareil ?",
      keep=True)
    sol(alg=r"U_{2} = U \cdot \f{R_{2}}{R_{1} + R_{2}}",
        num=r"U_{2} = 18 \cdot \f{2,5 \cdot 10^{6}}{4,5 \cdot 10^{6}} = 10,00 \u{ [V]}",
        ing=r"U_{2} = 10,00 \u{ [V]}")
    q("b)  Calcule le groupe R_{2} // R_{V}, puis la tension réellement affichée.")
    sol(alg=r"R_{2V} = \f{R_{2} \cdot R_{V}}{R_{2} + R_{V}}",
        num=r"R_{2V} = \f{2,5 \cdot 10^{6} \cdot 10 \cdot 10^{6}}"
            r"{12,5 \cdot 10^{6}} = 2,00 \cdot 10^{6} \u{ [Ω]}",
        ing=r"R_{2V} = 2,00 \u{ [MΩ]}")
    sol(alg=r"U_{mes} = U \cdot \f{R_{2V}}{R_{1} + R_{2V}}",
        num=r"U_{mes} = 18 \cdot \f{2,00 \cdot 10^{6}}{4,00 \cdot 10^{6}} "
            r"= 9,00 \u{ [V]}",
        ing=r"U_{mes} = 9,00 \u{ [V]}")
    q("c)  Calcule le courant total I_{1}, puis les courants I_{2} dans R_{2} et "
      "I_{V} dans le voltmètre. Contrôle avec la loi des nœuds.")
    sol(alg=r"I_{1} = \f{U}{R_{1} + R_{2V}}",
        num=r"I_{1} = \f{18}{4,00 \cdot 10^{6}} = 4,5 \cdot 10^{-6} \u{ [A]}",
        ing=r"I_{1} = 4,5 \u{ [µA]}")
    sol(alg=r"I_{2} = \f{U_{mes}}{R_{2}}          I_{V} = \f{U_{mes}}{R_{V}}",
        num=r"I_{2} = \f{9,00}{2,5 \cdot 10^{6}} = 3,6 \cdot 10^{-6} \u{ [A]}      "
            r"I_{V} = \f{9,00}{10 \cdot 10^{6}} = 0,9 \cdot 10^{-6} \u{ [A]}",
        ing=r"I_{2} = 3,6 \u{ [µA]}          I_{V} = 0,9 \u{ [µA]}")
    sol(txt="Contrôle, loi des nœuds :",
        alg=r"I_{2} + I_{V} = I_{1}",
        num=r"3,6 + 0,9 = 4,5 \u{ [µA]}",
        ing=r"4,5 \u{ [µA]} = I_{1}", lines=3,
        note="Les nœuds bouclent : le calcul est bon.")
    q("d)  Calcule l’écart par rapport à la valeur vraie.")
    sol(alg=r"\u{écart} = \f{U_{mes} - U_{2}}{U_{2}} \cdot 100",
        num=r"\u{écart} = \f{9,00 - 10,00}{10,00} \cdot 100",
        ing=r"\u{écart} = -10,0 \u{ [%]}")
    q("e)  La règle R_{V} ≥ 100 · R est-elle respectée ? Que faudrait-il ?")
    sol(txt="Il faudrait R_{V} ≥ 100 × 2,5 MΩ = 250 MΩ. Le numérique n’en offre que "
            "10 MΩ : aucun appareil d’atelier ne tient cette règle sur un diviseur "
            "en mégohms. L’écart de 10 % est donc inévitable — il doit être "
            "annoncé avec la mesure, pas caché.", lines=3)

    # ================================================================ N°4
    ex(4, "La chute de tension de l’ampèremètre\t10 min")
    enonce("On mesure le courant du circuit ci-dessous avec un ampèremètre dont la "
           "résistance interne vaut 30 Ω.", after=60)
    B.append(image("rIdG4", 5.8, 2.14, 4))
    q("a)  Quel courant circulerait sans l’ampèremètre ?", keep=True)
    sol(alg=r"I_{vrai} = \f{U}{R}",
        num=r"I_{vrai} = \f{12}{0,47 \cdot 10^{3}} = 25,53 \cdot 10^{-3} \u{ [A]}",
        ing=r"I_{vrai} = 25,53 \u{ [mA]}")
    q("b)  Quel courant l’ampèremètre affiche-t-il réellement ?")
    sol(alg=r"I_{mes} = \f{U}{R + R_{A}}",
        num=r"I_{mes} = \f{12}{0,5 \cdot 10^{3}} = 24 \cdot 10^{-3} \u{ [A]}",
        ing=r"I_{mes} = 24,0 \u{ [mA]}")
    q("c)  Quelle est la chute de tension aux bornes de l’ampèremètre, et quelle "
      "tension reste-t-il pour R ? Contrôle avec la loi des mailles.")
    sol(alg=r"U_{A} = R_{A} \cdot I_{mes}",
        num=r"U_{A} = 30 \cdot 24 \cdot 10^{-3} = 0,72 \u{ [V]}",
        ing=r"U_{A} = 0,72 \u{ [V]}")
    sol(alg=r"U_{R} = R \cdot I_{mes}",
        num=r"U_{R} = 470 \cdot 24 \cdot 10^{-3} = 11,28 \u{ [V]}",
        ing=r"U_{R} = 11,28 \u{ [V]}")
    sol(txt="Contrôle, loi des mailles :",
        alg=r"U_{A} + U_{R} = U",
        num=r"0,72 + 11,28 = 12,00 \u{ [V]}",
        ing=r"12,00 \u{ [V]} = U", lines=3,
        note="La maille boucle : le calcul est bon.")
    q("d)  Calcule l’écart sur le courant, puis vérifie la règle R_{A} ≤ R/100.")
    sol(alg=r"\u{écart} = \f{I_{mes} - I_{vrai}}{I_{vrai}} \cdot 100",
        num=r"\u{écart} = \f{24,0 - 25,53}{25,53} \cdot 100",
        ing=r"\u{écart} = -6,0 \u{ [%]}")
    sol(txt="La règle demande R_{A} ≤ 470/100 = 4,7 Ω. Avec 30 Ω on est six fois "
            "trop haut : l’écart de 6 % était prévisible.", lines=2)

    # ================================================================ N°5
    ex(5, "L’ohmmètre sur un circuit monté\t5 min")
    enonce("Une résistance R_{x} de 22 kΩ est encore soudée sur la carte. Vue par "
           "l’ohmmètre, le reste du circuit se comporte comme une résistance de "
           "33 kΩ en parallèle.", after=60)
    B.append(image("rIdG5", 5.8, 2.23, 5))
    q("a)  Quelle valeur l’ohmmètre affiche-t-il, et quel est l’écart ?", keep=True)
    sol(alg=r"R_{lue} = \f{R_{x} \cdot R_{reste}}{R_{x} + R_{reste}}",
        num=r"R_{lue} = \f{22 \cdot 10^{3} \cdot 33 \cdot 10^{3}}"
            r"{55 \cdot 10^{3}} = 13,2 \cdot 10^{3} \u{ [Ω]}",
        ing=r"R_{lue} = 13,2 \u{ [kΩ]}")
    sol(alg=r"\u{écart} = \f{R_{lue} - R_{x}}{R_{x}} \cdot 100",
        num=r"\u{écart} = \f{13,2 - 22}{22} \cdot 100",
        ing=r"\u{écart} = -40 \u{ [%]}")
    q("b)  La valeur lue peut-elle être plus GRANDE que la vraie ? Justifie.")
    sol(txt="Non. Le reste du circuit se met en parallèle, et un groupe parallèle "
            "est toujours plus petit que la plus petite de ses résistances. Une "
            "lecture en place est donc toujours trop petite, jamais trop grande.",
        lines=3)
    q("c)  Cite les trois règles à respecter avant toute mesure à l’ohmmètre.")
    sol(txt="Circuit hors tension ; composant isolé, au moins une patte "
            "dessoudée ; ne pas tenir les deux pointes de touche entre les doigts.",
        lines=3)

    # ================================================================ N°6
    ex(6, "Précision et choix de l’échelle\t5 min")
    enonce("Extrait de la fiche technique du Fluke 87, fonction tension "
           "continue : échelle 6,000 V, résolution 0,001 V ; échelle 60,00 V, "
           "résolution 0,01 V. Précision annoncée pour les deux : "
           "±(0,05 % + 1). Tu lis 2,000 V.", after=120)
    q("a)  Quelle est la précision sur l’échelle 6,000 V, en volts puis en "
      "pour-cent de la lecture ?", keep=True)
    sol(alg=r"\u{Précision} = \pm (\f{p}{100} \cdot U_{lue} + n \cdot "
            r"\u{résolution})",
        num=r"\pm (0,0005 \cdot 2,000 + 1 \cdot 0,001) = \pm (1,00 \cdot "
            r"10^{-3} + 1,00 \cdot 10^{-3})",
        ing=r"\pm 2,00 \cdot 10^{-3} \u{ [V]} = \pm 2,00 \u{ [mV]}",
        note="soit ± 0,10 [%] de la lecture.")
    q("b)  Et sur l’échelle 60,00 V ?")
    sol(alg=r"\u{Précision} = \pm (\f{p}{100} \cdot U_{lue} + n \cdot "
            r"\u{résolution})",
        num=r"\pm (0,0005 \cdot 2,00 + 1 \cdot 0,01) = \pm (1,00 \cdot "
            r"10^{-3} + 10,0 \cdot 10^{-3})",
        ing=r"\pm 11,0 \cdot 10^{-3} \u{ [V]} = \pm 11,0 \u{ [mV]}",
        note="soit ± 0,55 [%] de la lecture.")
    q("c)  Entre quelles valeurs se trouve la tension vraie, sur chaque "
      "échelle ?")
    sol(txt="Échelle 6,000 V : entre 1,998 [V] et 2,002 [V]. "
            "Échelle 60,00 V : entre 1,989 [V] et 2,011 [V].", lines=2)
    q("d)  Quelle échelle choisis-tu, et qu’est-ce qui fait toute la "
      "différence entre les deux ?")
    sol(txt="L’échelle 6,000 V : cinq fois plus précise pour la même lecture. "
            "Le pourcentage ne change pas — il suit la LECTURE. C’est le "
            "« + 1 » qui change, parce qu’il vaut une fois la RÉSOLUTION, dix "
            "fois plus grosse sur l’échelle 60 V. D’où la règle : la plus "
            "petite échelle qui contient la mesure.", lines=4)

    # ---------------------------------------------------------- auto-évaluation
    B.extend([EMPTY, EMPTY, HR])
    B.append(para(rich("Où j’en suis"), tabs=[5103], after=120, keep=True))
    B.append(para(rich("Coche honnêtement avant de regarder le corrigé."),
                  after=120))
    crit = [
        ("J’explique ce qu’est la résistance interne d’un appareil et son effet",
         "N°1, 2"),
        ("Je vérifie avant de brancher jusqu’où mon multimètre est honnête",
         "N°2"),
        ("Je calcule la tension réellement affichée par un voltmètre", "N°3"),
        ("Je calcule le courant affiché et la chute de tension d’un ampèremètre",
         "N°4"),
        ("J’explique pourquoi une résistance mesurée en place se lit trop petite",
         "N°5"),
        ("Je calcule une incertitude et je choisis le bon calibre", "N°6"),
        ("Je vérifie les deux règles R_{V} ≥ 100 · R et R_{A} ≤ R/100", "N°3, 4"),
        ("Je contrôle mes résultats avec les lois des nœuds et des mailles",
         "N°3, 4"),
        ("Je pose mes calculs en trois temps : formule, nombres, résultat", "tous"),
        ("J’écris tout résultat avec son unité entre crochets : 24,0 [mA]",
         "tous"),
        ("Mes schémas respectent les symboles CEI et les flèches indicées", "N°1"),
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
    name = ("510 EX C Appareils de mesure.docx" if corrige
            else "510 EX Appareils de mesure.docx")
    out = os.path.join(OUTDIR, name)
    if os.path.exists(out):
        os.remove(out)
    subprocess.run(["zip", "-Xqr", os.path.abspath(out), "."], cwd=WORK, check=True)
    print("saved", out)
    return out


if __name__ == "__main__":
    make(True)
    make(False)
