# -*- coding: utf-8 -*-
"""210 EX Algèbre de Boole (+ corrigé 210 EX C) · TM1 – El DT 1 · semaine 2.
Partie A : fiche de synthèse à compléter pendant la présentation 200 (lois, 12 règles, De Morgan) ; reprend la structure de
l'ancienne fiche « Algèbre booléenne : lois, règles et théorème » (2005).
Partie B : exercices sur la ligne de remplissage (LZ_2225, LZ_2226). Équivalences et tables recalculées par verif.py."""
from moteur.fiche import RED, GREY, NAVY, TW, WD_ALIGN_PARAGRAPH

TITLE = "Algèbre de Boole"
S = CTX = None                        # fixés par produire(ctx)
LZ = lambda c: (c, S.lz_link(c))


def tdv(n):
    """Combinaisons des entrées, poids fort à gauche, dans l'ordre du comptage binaire."""
    return [[(i >> (n - 1 - j)) & 1 for j in range(n)] for i in range(1 << n)]


# fonctions de la fiche (recalculées indépendamment dans verif.py)
def n1(c, b, a):
    return (a | b) & (a | c), a | (b & c)


def n4(a, b, c):
    direct = (a & (1 - b)) | (a & b & (1 - c))
    simple = a & (1 - (b & c))
    return direct, simple


def build(corr, out):
    T200 = S.teams_url("200")
    x = CTX.doc(corr, out, TITLE, "Corrigé" if corr else "Fiche",
                "210 EX Algèbre de Boole – " + ("Corrigé" if corr else "Fiche et exercices") + " – El DT 1",
                f"{S.matiere} – {S.classe} – {S.annee}")
    x.head(TITLE,
           [(f"Fiche à compléter et exercices · {S.matiere} · Classe {S.classe} · {S.annee} · Champ ", None), (S.champ, S.fm(S.futuremem_champ)),
            (" · Objectifs ", None), LZ("LZ_2225"), (", ", None), LZ("LZ_2226")],
           ["Déroulement (enseignant·e) : partie A pendant la présentation 200, partie B en binôme",
            "Partie A : A.1 avec la diapositive 4, A.2 avec les diapositives 6 à 8, A.3 avec la diapositive 11 (≈ 15 min au total). "
            "Partie B : 45 min (N°1 : 8 min ; N°2 : 10 min ; N°3 : 8 min ; N°4 : 14 min ; N°5 : 5 min).",
            "Exiger à chaque simplification une étape par ligne avec la règle, puis le contrôle par la table de vérité."],
           ["**Consignes :** partie A, complète les lois, les règles et le théorème pendant la présentation 200. Partie B, en binôme, 45 min. "
            "Écris une étape par ligne et note à côté la loi ou le numéro de la règle utilisée, puis contrôle le résultat.",
            "**Conventions :** comme en semaine 1, point = ET, plus = OU, barre au-dessus = NON. Ordre des opérations : NON, puis ET, puis OU. "
            "Sortie S, entrées A, B, C (sens donné par la légende). "
            "Dans une table de vérité, les entrées vont du poids fort au poids faible, puis vient la sortie."],
           [("Présentations : ", [(S.fichier("200"), T200), (" · semaine 1 : ", None), (S.fichier("120"), S.teams_url("120")),
                                  (" · pour réviser : ", None), ("page interactive 201", S.teams_url("201")), (" (Edge ou Chrome) · ", None),
                                  ("animation 205", S.teams_url("205"))]),
            ("Semaine 1 : ", [(S.fichier("130"), S.teams_url("130")), (" (portes, tables de vérité, CI 74HC)", None)])])

    # ================= PARTIE A
    x.H1("Partie A : lois, règles et théorème")
    x.P("**A.1 Les trois lois** (présentation 200, diapositive 4)", keep=True, after=2, color=NAVY)
    x.TABLE([4.0, 6.0, TW - 10.0 - 0.02], [
        ["Loi", "Expression", "="],
        ["Commutativité", "$A+B$", ("R", "$B+A$")],
        ["", "$A\\cdot B$", ("R", "$B\\cdot A$")],
        ["Associativité", "$A+(B+C)$", ("R", "$(A+B)+C$")],
        ["", "$A\\cdot (B\\cdot C)$", ("R", "$(A\\cdot B)\\cdot C$")],
        ["Distributivité", "$A\\cdot (B+C)$", ("R", "$A\\cdot B+A\\cdot C$")]], height=0.55, size=11, height_eleve=0.7)
    x.P("**A.2 Les douze règles** (présentation 200, diapositives 6 à 8)", keep=True, after=2, color=NAVY)
    regles = [("$A+0$", "$A$"), ("$A+1$", "$1$"), ("$A\\cdot 0$", "$0$"), ("$A\\cdot 1$", "$A$"), ("$A+A$", "$A$"), ("$A+\\bar{A}$", "$1$"),
              ("$A\\cdot A$", "$A$"), ("$A\\cdot \\bar{A}$", "$0$"), ("$\\bar{\\bar{A}}$", "$A$"), ("$A+A\\cdot B$", "$A$"),
              ("$A+\\bar{A}\\cdot B$", "$A+B$"), ("$(A+B)\\cdot (A+C)$", "$A+B\\cdot C$")]
    w = (TW - 0.04) / 2
    rows = [["N°", "Expression", "=", "N°", "Expression", "="]]
    for i in range(6):
        g, d = regles[i], regles[i + 6]
        rows.append([str(i + 1), g[0], ("R", g[1]), str(i + 7), d[0], ("R", d[1])])
    x.TABLE([1.3, 4.0, w - 5.3, 1.3, 4.0, w - 5.3], rows, height=0.55, size=11, first_left=False, height_eleve=0.7)
    x.P("**A.3 Le théorème de De Morgan** (présentation 200, diapositive 11)", keep=True, after=2, color=NAVY)
    x.TABLE([6.0, TW - 6.0 - 0.02], [["Expression", "="], ["$\\bar{A\\cdot B}$", ("R", "$\\bar{A}+\\bar{B}$")],
                                     ["$\\bar{A+B}$", ("R", "$\\bar{A}\\cdot \\bar{B}$")]], height=0.7, size=11, first_left=False, height_eleve=0.8)
    x.P("Moyen mnémotechnique : on casse la barre et on change le signe.", italic=True, size=10, color=GREY)

    # ================= PARTIE B
    x.H1("Partie B : exercices sur la ligne de remplissage")
    x.CTX("la ligne de remplissage de boissons des présentations 120 et 200. Les capteurs donnent 1 quand ce qu'ils surveillent est vrai ; "
          "un actionneur est en marche quand sa sortie vaut 1.")

    # ---- N°1
    x.EX(1, "Vérifier une règle par la table de vérité (≈ 8 min)", [("Présentation 200, diapositive 5", T200), LZ("LZ_2225")])
    x.Q("a)", "Complète la table pour vérifier la règle 12 : $(A+B)\\cdot (A+C)=A+B\\cdot C$.")
    rows = [["C", "B", "A", "$A+B$", "$A+C$", "$(A+B)\\cdot (A+C)$", "$B\\cdot C$", "$A+B\\cdot C$"]]
    for c, b, a in tdv(3):
        g, d = n1(c, b, a)
        rows.append([str(c), str(b), str(a), ("R", str(a | b)), ("R", str(a | c)), ("R", str(g)), ("R", str(b & c)), ("R", str(d))])
    x.TABLE([1.1, 1.1, 1.1, 2.0, 2.0, 3.6, 2.0, TW - 12.9 - 0.02], rows, height=0.5, size=10.5, first_left=False)
    x.Q("b)", "La règle est-elle vérifiée ? Justifie.")
    x.ANS("Oui : les colonnes $(A+B)\\cdot (A+C)$ et $A+B\\cdot C$ sont identiques sur les 8 lignes.", 1)

    # ---- N°2
    x.HR(); x.EX(2, "Simplifier avec les règles (≈ 10 min)", [("Présentation 200, diapositives 6 à 10", T200), LZ("LZ_2225")])
    x.P("Simplifie chaque équation. Écris le résultat et les lois ou règles utilisées.", keep=True, after=2)
    rows = [["", "Équation", "Résultat", "Lois ou règles utilisées"],
            ["a)", "$S=A\\cdot 1+0$", ("R", "$S=A$"), ("R", "règle 4, puis règle 1")],
            ["b)", "$S=C\\cdot \\bar{C}+C$", ("R", "$S=C$"), ("R", "règle 8 (0 + C), puis règle 1")],
            ["c)", "$S=\\bar{A}\\cdot B+\\bar{A}\\cdot \\bar{B}$", ("R", "$S=\\bar{A}$"), ("R", "distributivité : Ā · (B + B̄), règles 6 et 4")],
            ["d)", "$S=B+B\\cdot C$", ("R", "$S=B$"), ("R", "règle 10 avec B à la place de A")],
            ["e)", "$S=\\bar{B}+B\\cdot C$", ("R", "$S=\\bar{B}+C$"), ("R", "règle 11 avec B̄ à la place de A (et règle 9)")],
            ["f)", "$S=(A+B)\\cdot (A+\\bar{C})$", ("R", "$S=A+B\\cdot \\bar{C}$"), ("R", "règle 12 avec C̄ à la place de C")]]
    x.TABLE([0.9, 4.6, 3.4, TW - 8.9 - 0.02], rows, height=0.72, size=10.5, first_left=False, gauche=(3,), height_eleve=0.95)
    x.BOX(["Si difficulté (N°2)",
           "Cherche d'abord une variable commune à tous les termes et mets-la en évidence. Ensuite, compare chaque morceau avec les règles 1 à 12 de la partie A."],
          only_corr=False)

    # ---- N°3
    x.HR(); x.EX(3, "De Morgan (≈ 8 min)", [("Présentation 200, diapositives 11 et 12", T200), LZ("LZ_2225")])
    x.Q("a)", "Applique De Morgan : $S=\\bar{A\\cdot B\\cdot C}$")
    x.ANS("$S=\\bar{A}+\\bar{B}+\\bar{C}$", 1)
    x.Q("b)", "Applique De Morgan, puis simplifie : $S=\\bar{\\bar{A}+B}$")
    x.ANS("$S=\\bar{\\bar{A}}\\cdot \\bar{B}=A\\cdot \\bar{B}$ (De Morgan, puis règle 9)", 1)
    x.Q("c)", "Applique De Morgan, puis simplifie : $S=\\bar{\\bar{A}\\cdot \\bar{B}}$. Quelle porte obtiens-tu ?")
    x.ANS("$S=\\bar{\\bar{A}}+\\bar{\\bar{B}}=A+B$ (De Morgan, puis règle 9) : une porte OU. C'est le OU construit avec des NON-ET (diapositive 13).", 2)
    x.Q("d)", "Une nouvelle ligne a trois arrêts d'urgence. A, B et C valent 1 quand l'arrêt correspondant est actionné. "
              "Le convoyeur est autorisé (S = 1) si aucun n'est actionné : $S=\\bar{A}\\cdot \\bar{B}\\cdot \\bar{C}$. Montre avec De Morgan qu'une seule porte suffit. Laquelle ?")
    x.ANS("$S=\\bar{A+B+C}$ : une porte NON-OU à 3 entrées (74HC27), au lieu de trois inverseurs et d'un ET à 3 entrées.", 2)

    # ---- N°4
    x.HR(); x.EX(4, "Le voyant « défaut remplissage » (≈ 14 min)", [("Présentation 200, diapositives 13 à 15", T200), LZ("LZ_2225"), LZ("LZ_2226")])
    x.CTX("cahier des charges du voyant « défaut remplissage », rédigé par un collègue. S : voyant allumé, A : vanne ouverte, "
          "B : bouteille sous le bec, C : niveau de la cuve suffisant.")
    x.P("Le voyant s'allume si la vanne est ouverte et qu'aucune bouteille n'est sous le bec ; ou si la vanne est ouverte, qu'une bouteille est sous le bec "
        "et que le niveau de la cuve est bas.", keep=True, after=3)
    x.Q("a)", "Écris l'équation de S telle que le cahier des charges la décrit (un terme par condition).")
    x.ANS("$S=A\\cdot \\bar{B}+A\\cdot B\\cdot \\bar{C}$", 1)
    x.Q("b)", "Combien de portes et de CI faut-il pour câbler cette équation telle quelle ?")
    x.ANS("5 portes : 2 inverseurs (B̄, C̄), 1 ET à 2 entrées, 1 ET à 3 entrées, 1 OU. 4 CI : 74HC04, 74HC08, 74HC11, 74HC32.", 2)
    x.Q("c)", "Simplifie S. Une étape par ligne, avec la loi ou la règle.")
    x.ANS("$S=A\\cdot (\\bar{B}+B\\cdot \\bar{C})$   distributivité (mise en évidence de A)\n"
          "$S=A\\cdot (\\bar{B}+\\bar{C})$   règle 11 avec B̄ à la place de A (et règle 9)\n"
          "$S=A\\cdot \\bar{B\\cdot C}$   De Morgan", 3)
    x.Q("d)", "Contrôle ta simplification : complète la table de vérité avec l'équation de a) et ton résultat de c).")
    rows = [["C", "B", "A", "S (équation a)", "S (équation c)"]]
    for c, b, a in tdv(3):
        d, s_ = n4(a, b, c)
        rows.append([str(c), str(b), str(a), ("R", str(d)), ("R", str(s_))])
    x.TABLE([1.3, 1.3, 1.3, 4.0, 4.0], rows, height=0.45, size=10.5, first_left=False)
    x.ANS("Les deux colonnes sont identiques : S = 1 pour C B A = 001, 011 et 101. La simplification est juste.", 1)
    x.Q("e)", "Dessine le schéma CEI de ton résultat de c).")
    if corr:
        x.IMG("fig_n4_corr.png", 5.5, after=2)
        x.ANS("2 portes : une NON-ET (74HC00) et un ET (74HC08).", 1)
    else:
        for _ in range(6): x.P("", after=6)
    x.Q("f)", "Le magasin n'a plus que des 74HC00. Réalise S avec un seul 74HC00 : dessine le schéma. Combien de portes utilises-tu ?")
    if corr:
        x.IMG("fig_n4_nand.png", 7.2, after=2)
        x.ANS("3 portes NON-ET : $\\bar{B\\cdot C}$, puis une NON-ET avec A, puis une NON-ET montée en inverseur (règle 9). "
              "Il reste une porte libre dans le 74HC00 : 1 CI au lieu de 4.", 2)
    else:
        for _ in range(6): x.P("", after=6)
        x.ANS("", 1)

    # ---- N°5
    x.HR(); x.EX(5, "Le convoyeur avec un seul 74HC00 (≈ 5 min)", [("Présentation 200, diapositives 11, 13 et 15", T200), LZ("LZ_2226")])
    x.CTX("le convoyeur de la présentation 200, S = A · (B + C). S : convoyeur, A : machine en marche, B : bouteille pleine, C : vidange.")
    x.Q("a)", "Développe S (distributivité).")
    x.ANS("$S=A\\cdot B+A\\cdot C$", 1)
    x.Q("b)", "Écris $S=\\bar{\\bar{S}}$ (règle 9), puis applique De Morgan sous la grande barre. Que reste-t-il ?")
    x.ANS("$S=\\bar{\\bar{A\\cdot B+A\\cdot C}}=\\bar{\\bar{A\\cdot B}\\cdot \\bar{A\\cdot C}}$ : trois NON-ET.", 2)
    x.Q("c)", "Dessine le schéma avec des portes NON-ET seulement.")
    if corr:
        x.IMG("fig_n5_corr.png", 5.2, after=2)
        x.ANS("3 portes d'un seul 74HC00, au lieu de 2 CI (74HC32 et 74HC08). Une somme de produits se câble toujours ainsi : NON-ET, puis NON-ET.", 2)
    else:
        for _ in range(6): x.P("", after=6)

    # ---- auto-évaluation (fiche seulement : REGLES 4)
    if not corr:
        x.P("**Auto-évaluation**", keep=True, after=1, before=10, color=NAVY)
        x.P("Après la correction : ✓ je sais seul·e · ~ avec une aide · ✗ à revoir (reprends la diapositive indiquée).", keep=True, size=10)
        x.TABLE([TW / 5 - 0.01] * 5, [["Vérifier par la table (N°1, diapo 5)", "Appliquer les règles (N°2, diapos 6 à 10)", "De Morgan (N°3, diapos 11 et 12)",
                                       "Simplifier et contrôler (N°4, diapo 14)", "Dessiner le schéma (N°4, N°5, diapos 13 et 15)"], ["", "", "", "", ""]],
                height=0.75, size=9, first_left=False)
    x.finish()


def produire(ctx):
    global S, CTX
    S, CTX = ctx.S, ctx
    build(False, ctx.sortie_de("210"))
    build(True, ctx.sortie_de("210C"))
