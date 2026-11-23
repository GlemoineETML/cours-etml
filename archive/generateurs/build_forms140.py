# -*- coding: utf-8 -*-
"""140 — questionnaire noté pour Microsoft Forms.

Deux fichiers :
  · « 140 QUIZ Forms a importer.docx » — mise en page nue, verticale, sans
    équation, sans image, sans tableau : le convertisseur de Forms
    (forms.office.com → Importer → Charger depuis cet appareil) n'accepte que
    des choix multiples et des questions ouvertes.
  · « 140 QUIZ Forms cle de correction.docx » — bonne réponse et points de
    chaque question, à saisir dans Forms après l'import (Microsoft ne lit ni
    les réponses ni les points depuis le document source).
"""
import os, random
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUTDIR = "out"
NAVY = RGBColor(0x24, 0x28, 0x52)
RED = RGBColor(0xEE, 0x00, 0x00)
GREY = RGBColor(0x7F, 0x8F, 0xA9)

TITRE = "Circuits mixtes et simplification — test"
SOUS_TITRE = ("El Dim1 · semaine 3 · 22 questions à choix multiple et "
              "2 questions ouvertes · 26 points · calculette et formulaire "
              "personnel autorisés")

# ---------------------------------------------------------------------------
# Chaque entrée : (énoncé, [propositions], index de la bonne, points)
# L'ordre des propositions est celui du document ; la bonne réponse est
# repérée par son rang, jamais marquée dans le fichier importé.
# ---------------------------------------------------------------------------
SECTIONS = [
    ("Partie A — Reconnaître avant de calculer", [
        ("Qu'est-ce qu'un nœud dans un circuit ?", [
            "Un point où se rejoignent au moins trois fils",
            "Un point où le courant change de sens",
            "Chaque coude du schéma",
            "Une borne de la source"], 0, 1),
        ("Deux résistances sont en parallèle quand :", [
            "elles sont branchées entre les deux mêmes nœuds",
            "elles sont dessinées l'une au-dessus de l'autre",
            "elles ont la même valeur",
            "elles sont traversées par le même courant"], 0, 1),
        ("Dans un montage série, qu'est-ce qui est identique pour toutes les "
         "résistances ?", [
            "Le courant",
            "La tension",
            "La puissance",
            "Rien, tout change"], 0, 1),
        ("Sur un schéma, la flèche du courant se dessine :", [
            "sur le fil, avec un indice qui la nomme",
            "à côté du fil, comme un vecteur",
            "à l'intérieur du symbole de la résistance",
            "seulement pour le courant total"], 0, 1),
    ]),
    ("Partie B — Les deux lois de Kirchhoff et la puissance", [
        ("Un courant de 180 mA entre dans un nœud. Une branche en emporte "
         "110 mA. Que vaut le courant de l'autre branche ?", [
            "70 mA", "90 mA", "290 mA", "110 mA"], 0, 1),
        ("Trois résistances en série sous 30 V. La première a 12 V à ses "
         "bornes, la deuxième 6 V. Quelle tension reste-t-il pour la "
         "troisième ?", [
            "12 V", "18 V", "24 V", "6 V"], 0, 1),
        ("Laquelle de ces expressions de la puissance est FAUSSE ?", [
            "P égale I au carré divisé par R",
            "P égale U fois I",
            "P égale R fois I au carré",
            "P égale U au carré divisé par R"], 0, 1),
        ("Trois résistances sont en parallèle. Peut-on utiliser la formule "
         "produit sur somme ?", [
            "Non, elle ne vaut que pour deux résistances",
            "Oui, avec les trois valeurs au numérateur",
            "Oui, toujours",
            "Non, cette formule n'existe pas"], 0, 1),
    ]),
    ("Partie C — Réduire et calculer", [
        ("Une résistance de 100 ohms est en parallèle avec une de 400 ohms. "
         "Que vaut la résistance équivalente ?", [
            "80 ohms", "500 ohms", "250 ohms", "125 ohms"], 0, 1),
        ("Trois résistances de 600 ohms sont en parallèle. Que vaut la "
         "résistance équivalente ?", [
            "200 ohms", "1800 ohms", "300 ohms", "600 ohms"], 0, 1),
        ("Une résistance de 220 ohms est en série avec le groupe formé de "
         "330 ohms en parallèle avec 660 ohms. Que vaut la résistance "
         "totale ?", [
            "440 ohms", "1210 ohms", "330 ohms", "550 ohms"], 0, 1),
        ("Une source de 24 V alimente une résistance totale de 480 ohms. Que "
         "vaut le courant total ?", [
            "50 mA", "20 mA", "0,5 A", "5 mA"], 0, 1),
        ("Dans un groupe parallèle, une branche de 300 ohms est soumise à "
         "12 V. Quel courant la traverse ?", [
            "40 mA", "25 mA", "3,6 A", "400 mA"], 0, 1),
        ("Une résistance de 150 ohms est traversée par 40 mA. Quelle "
         "puissance dissipe-t-elle ?", [
            "240 mW", "6 W", "60 mW", "24 mW"], 0, 1),
        ("Dans un groupe de deux résistances en parallèle, laquelle prend le "
         "plus grand courant ?", [
            "La plus petite résistance",
            "La plus grande résistance",
            "Les deux prennent le même courant",
            "Cela dépend de la tension de la source"], 0, 1),
        ("Par quoi commence-t-on la réduction d'un circuit mixte ?", [
            "Par le groupe le plus imbriqué, le plus loin de la source",
            "Par la résistance la plus proche de la source",
            "Par la plus grande résistance",
            "Par n'importe quelle résistance, le résultat est le même"], 0, 1),
    ]),
    ("Partie D — Contrôler son résultat", [
        ("La résistance équivalente d'un groupe parallèle est toujours :", [
            "plus petite que la plus petite du groupe",
            "comprise entre les deux valeurs",
            "plus grande que la plus grande du groupe",
            "égale à la moyenne des valeurs"], 0, 1),
        ("Quel contrôle pose-t-on sur les courants d'un groupe parallèle ?", [
            "La somme des courants de branche est égale au courant total, "
            "c'est la loi des nœuds",
            "Les courants de branche sont égaux entre eux",
            "Le courant total est la somme des tensions divisée par la "
            "résistance totale",
            "Aucun contrôle n'est possible sur les courants"], 0, 1),
        ("Que vaut la somme des puissances dissipées par toutes les "
         "résistances d'un circuit ?", [
            "Elle est égale à la puissance fournie par la source",
            "Elle est plus grande que la puissance de la source",
            "Elle vaut la moitié de la puissance de la source",
            "Il n'y a aucun rapport entre les deux"], 0, 1),
    ]),
    ("Partie E — Dessiner et mesurer", [
        ("Comment se branche un ampèremètre ?", [
            "En série avec l'élément dont on mesure le courant",
            "En parallèle sur l'élément dont on mesure le courant",
            "Directement aux bornes de la source",
            "Peu importe, il s'adapte"], 0, 1),
        ("Comment se branche un voltmètre ?", [
            "En parallèle sur l'élément dont on mesure la tension",
            "En série avec l'élément dont on mesure la tension",
            "À la place de l'élément",
            "En série avec l'ampèremètre"], 0, 1),
        ("Tu mesures une tension qui s'écarte de 4 pour cent de ton calcul, "
         "avec des résistances de la série E12. Que conclus-tu ?", [
            "C'est normal, l'écart reste dans la tolérance de plus ou moins "
            "5 pour cent",
            "Il y a une erreur de montage",
            "Il y a une erreur de calcul",
            "L'appareil de mesure est en panne"], 0, 1),
    ]),
]

OUVERTES = [
    ("Explique en une phrase pourquoi un ampèremètre ne doit jamais être "
     "branché en parallèle sur une résistance.",
     "Sa résistance interne est quasi nulle : branché en parallèle il "
     "court-circuite l'élément et la source, ce qui fait grimper le courant "
     "et grille le fusible ou l'appareil.", 2),
    ("Cite trois des sept règles d'un schéma propre.",
     "Trois parmi : symboles CEI normalisés · traits horizontaux et verticaux "
     "seulement · nœuds marqués par un point · chaque composant repéré et sa "
     "valeur indiquée · flèches de courant sur le fil avec leur indice · "
     "flèches de tension à côté du composant, du plus vers le moins · "
     "pas de croisement inutile, schéma aéré.", 2),
]


def melange():
    """Mélange les propositions une fois pour toutes, de façon reproductible.

    Dans les listes ci-dessus la bonne réponse est toujours écrite en premier ;
    on la déplace ici pour qu'elle ne soit pas toujours au même rang dans le
    document importé. La graine est fixe : le document et sa clé restent
    cohérents d'une génération à l'autre."""
    rnd = random.Random(140)
    out = []
    for titre, questions in SECTIONS:
        qs = []
        for enonce, choix, bonne, pts in questions:
            juste = choix[bonne]
            ordre = list(choix)
            rnd.shuffle(ordre)
            qs.append((enonce, ordre, ordre.index(juste), pts))
        out.append((titre, qs))
    return out


def doc_nu(SECTIONS):
    """Document nu : pas d'en-tête, pas de tableau, pas d'image, pas d'équation."""
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)

    def p(txt, size=11, bold=False, color=None, after=6, before=0, colle=False):
        par = d.add_paragraph()
        par.paragraph_format.space_after = Pt(after)
        par.paragraph_format.space_before = Pt(before)
        par.paragraph_format.keep_together = True
        par.paragraph_format.keep_with_next = colle
        r = par.add_run(txt)
        r.font.size = Pt(size)
        r.bold = bold
        if color:
            r.font.color.rgb = color
        return par

    p(TITRE, size=20, bold=True, color=NAVY, after=4)
    p(SOUS_TITRE, size=11, color=GREY, after=18)

    n = 0
    for titre, questions in SECTIONS:
        p(titre, size=14, bold=True, color=NAVY, after=10, before=14, colle=True)
        for enonce, choix, _bonne, _pts in questions:
            n += 1
            p("%d. %s" % (n, enonce), size=11, bold=True, after=4, colle=True)
            for i, c in enumerate(choix):
                p(c, size=11, after=2, colle=(i < len(choix) - 1))
            p("", size=6, after=0)

    p("Partie F — Questions ouvertes", size=14, bold=True, color=NAVY,
      after=10, before=14, colle=True)
    for enonce, _rep, _pts in OUVERTES:
        n += 1
        p("%d. %s" % (n, enonce), size=11, bold=True, after=4)
        p("", size=6, after=0)

    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, "140 QUIZ Forms a importer.docx")
    d.save(out)
    print("saved", out, "|", n, "questions")
    return n


def doc_cle(SECTIONS, total_questions):
    """Clé de correction : ce que Gael saisit dans Forms après l'import."""
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Pt(56)

    def p(txt, size=10.5, bold=False, color=None, after=4, before=0, ind=0):
        par = d.add_paragraph()
        par.paragraph_format.space_after = Pt(after)
        par.paragraph_format.space_before = Pt(before)
        par.paragraph_format.left_indent = Pt(ind)
        r = par.add_run(txt)
        r.font.size = Pt(size)
        r.bold = bold
        if color:
            r.font.color.rgb = color
        return par

    p("Clé de correction — " + TITRE, size=17, bold=True, color=NAVY, after=4)
    p("À saisir dans Microsoft Forms après l'import : Forms ne lit ni les "
      "bonnes réponses ni les points depuis le document source.",
      size=10.5, color=GREY, after=6)
    p("Marche à suivre : forms.office.com → Importer → Charger depuis cet "
      "appareil → choisir « 140 QUIZ Forms a importer.docx » → sélectionner "
      "Questionnaire (Quiz). Puis, pour chaque question, cliquer sur la coche "
      "à droite de la bonne réponse et saisir les points ci-dessous.",
      size=10.5, color=GREY, after=14)

    tot = 0
    n = 0
    for titre, questions in SECTIONS:
        p(titre, size=12.5, bold=True, color=NAVY, after=6, before=12)
        for enonce, choix, bonne, pts in questions:
            n += 1
            tot += pts
            p("%d. %s" % (n, enonce), size=10.5, bold=True, after=2)
            p("Bonne réponse : %s" % choix[bonne], size=10.5, color=RED,
              after=1, ind=16)
            p("Rang dans la liste : %d sur %d   ·   %d point"
              % (bonne + 1, len(choix), pts), size=9.5, color=GREY,
              after=7, ind=16)

    p("Partie F — Questions ouvertes", size=12.5, bold=True, color=NAVY,
      after=6, before=12)
    for enonce, rep, pts in OUVERTES:
        n += 1
        tot += pts
        p("%d. %s" % (n, enonce), size=10.5, bold=True, after=2)
        p("Attendu : %s" % rep, size=10.5, color=RED, after=1, ind=16)
        p("Correction manuelle   ·   %d points" % pts, size=9.5, color=GREY,
          after=7, ind=16)

    p("Total : %d questions, %d points." % (n, tot), size=12, bold=True,
      color=NAVY, before=14)
    p("Réglages conseillés dans Forms : mélanger les questions désactivé "
      "(les parties suivent la progression du cours), une seule réponse par "
      "question, afficher les résultats automatiquement à la remise.",
      size=10, color=GREY, after=4)

    out = os.path.join(OUTDIR, "140 QUIZ Forms cle de correction.docx")
    d.save(out)
    print("saved", out, "|", n, "questions,", tot, "points")


if __name__ == "__main__":
    S = melange()
    doc_cle(S, doc_nu(S))
