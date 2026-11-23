# -*- coding: utf-8 -*-
"""110 EX Diviseur de tension (+ corrigé 110 EX C) · séance de test du workflow, hors réforme.
Fil rouge : un robot de démonstration dont le microcontrôleur surveille la batterie. Valeurs recalculées par verif.py."""
from moteur.fiche import RED, GREY, NAVY, TW, WD_ALIGN_PARAGRAPH
from moteur.nombres import ing, ing_eq

TITLE = "Diviseur de tension"
S = CTX = None                        # fixés par produire(ctx)
k = 1e3


def div(u, r1, r2):
    return u * r2 / (r1 + r2)


def par(a, b):
    return a * b / (a + b)


def build(corr, out):
    x = CTX.doc(corr, out, TITLE, "Corrigé" if corr else "Exercices",
                "110 EX Diviseur de tension – " + ("Corrigé" if corr else "Exercices"), f"{S.matiere} – {S.classe} – {S.annee}")
    x.head(TITLE,
           [(f"Fiche d'exercices · {S.matiere} · Classe {S.classe} · {S.annee} · cours hors réforme", None)],
           ["Déroulement (enseignant·e) : 40 min, seul·e ou en binôme, après la présentation 100.",
            "Temps indicatifs : N°1 8 min, N°2 12 min, N°3 12 min, N°4 8 min.",
            "Correction : exiger les quatre étapes (formule, application numérique, résultat, contrôle) ; ramasser l'auto-évaluation."],
           ["**Consignes :** pour chaque calcul, écris la formule, l'application numérique avec les unités, le résultat avec son unité, "
            "puis un contrôle (loi des mailles ou ordre de grandeur)."],
           [("Présentation : ", [(S.fichier("100"), S.teams_url("100")), (" (diapositives 2 à 6)", None)])])
    x.CTX("tu équipes un robot de démonstration pour les journées portes ouvertes de l'école. Son microcontrôleur doit surveiller "
          "la batterie et lire des tensions de capteurs. Aucune de ses entrées analogiques ne supporte plus de 3,3 V.")

    # ---------------------------------------------------------------- N°1
    u, r1, r2 = 9, 4.7 * k, 2.2 * k
    u2, i, u1 = div(u, r1, r2), u / (r1 + r2), div(u, r2, r1)
    x.EX(1, "Calculer un diviseur (≈ 8 min)", [("Présentation diapositives 2 à 4", S.teams_url("100"))])
    x.CTX("le capteur de position du bras du robot est alimenté par une pile de 9 V à travers un diviseur.")
    x.IMG("fig_ex1.png", 7.0, keep=True, after=2)
    x.Q("a)", "Calcule la tension $U_{2}$.")
    x.ANS("$U_{2}=U\\cdot \\f{R_{2}}{R_{1}+R_{2}}=9\\u{ [V]}\\cdot \\f{2,2\\u{ [kΩ]}}{4,7\\u{ [kΩ]}+2,2\\u{ [kΩ]}}$\n"
          f"$U_{{2}}={ing_eq(u2, 'V')}$", 2)
    x.Q("b)", "Calcule le courant I qui traverse les deux résistances.")
    x.ANS("$I=\\f{U}{R_{1}+R_{2}}=\\f{9\\u{ [V]}}{6,9\\u{ [kΩ]}}=" + ing_eq(i, "A") + "$", 1)
    x.Q("c)", "Contrôle ton résultat avec la loi des mailles.")
    x.ANS(f"$U_{{1}}=U-U_{{2}}$ = {ing(u1, 'V')}, ou $U_{{1}}=R_{{1}}\\cdot I$ = 4,7 kΩ · {ing(i, 'A')} = {ing(r1 * i, 'V')} : "
          f"les deux calculs donnent la même valeur, et {ing(u1, 'V')} + {ing(u2, 'V')} = 9 V.", 2)

    # ---------------------------------------------------------------- N°2
    ub, ubmax, umax, r2 = 7.2, 8.4, 3.3, 10 * k
    r1min = ubmax * r2 / umax - r2
    r1 = 18 * k
    x.HR(); x.EX(2, "Surveiller la batterie du robot (≈ 12 min)", [("Présentation diapositive 5", S.teams_url("100"))])
    x.CTX("la batterie du robot (deux éléments lithium-ion) fournit 7,2 V et monte à 8,4 V en fin de charge. "
          "Elle est surveillée par une entrée analogique qui accepte de 0 à 3,3 V. On choisit R_{2} = 10 kΩ.")
    x.Q("a)", "Quelle tension de batterie faut-il prendre pour dimensionner le diviseur ? Pourquoi ?")
    x.ANS("8,4 V, la tension la plus haute : c'est elle qui risque de dépasser 3,3 V sur l'entrée.", 1)
    x.Q("b)", "Calcule la valeur minimale de R_{1}, puis choisis une valeur de la série E12 (10, 12, 15, 18, 22, 27, 33…).")
    x.ANS("$U_{2}=U\\cdot \\f{R_{2}}{R_{1}+R_{2}}\\le 3,3\\u{ V}$ donne $R_{1}\\ge \\f{U\\cdot R_{2}}{3,3\\u{ V}}-R_{2}$\n"
          f"$R_{{1}}\\ge \\f{{8,4\\u{{ [V]}}\\cdot 10\\u{{ [kΩ]}}}}{{3,3\\u{{ [V]}}}}-10\\u{{ [kΩ]}}$ = {ing(r1min, 'Ω', crochets=True)}\n"
          "On prend 18 kΩ, la première valeur E12 au-dessus (15 kΩ est trop faible).", 3)
    x.Q("c)", "Avec R_{1} = 18 kΩ, calcule U_{2} pour la batterie chargée (8,4 V) et pour la tension nominale (7,2 V). Contrôle un des deux résultats.")
    x.ANS(f"8,4 V : $U_{{2}}=8,4\\u{{ [V]}}\\cdot \\f{{10\\u{{ [kΩ]}}}}{{28\\u{{ [kΩ]}}}}$ = {ing(div(ubmax, r1, r2), 'V', crochets=True)} ≤ 3,3 V\n"
          f"7,2 V : $U_{{2}}=7,2\\u{{ [V]}}\\cdot \\f{{10\\u{{ [kΩ]}}}}{{28\\u{{ [kΩ]}}}}$ = {ing(div(ub, r1, r2), 'V', crochets=True)}\n"
          f"Contrôle : $U_{{1}}$ = 8,4 V · 18 kΩ / 28 kΩ = {ing(div(ubmax, r2, r1), 'V')} et {ing(div(ubmax, r2, r1), 'V')} + {ing(div(ubmax, r1, r2), 'V')} = 8,4 V.", 3)
    x.Q("d)", "Quel courant le diviseur prend-il à la batterie chargée ? Est-ce gênant ?")
    x.ANS(f"I = 8,4 V / 28 kΩ = {ing(ubmax / (r1 + r2), 'A')}. C'est négligeable devant la consommation des moteurs du robot.", 1)

    # ---------------------------------------------------------------- N°3
    u, r1, r2 = 10, 10 * k, 10 * k
    x.HR(); x.EX(3, "Brancher une charge sur le diviseur (≈ 12 min)", [("Présentation diapositive 6", S.teams_url("100"))])
    x.CTX("un diviseur R_{1} = R_{2} = 10 kΩ, alimenté en 10 V, fournit une tension de référence à un circuit de mesure. "
          "Ce circuit se comporte comme une résistance R_{L} branchée entre la sortie et la masse.")
    x.Q("a)", "Que vaut U_{2} sans charge ?")
    x.ANS(f"$U_{{2}}=10\\u{{ [V]}}\\cdot \\f{{10\\u{{ [kΩ]}}}}{{20\\u{{ [kΩ]}}}}$ = {ing(div(u, r1, r2), 'V', crochets=True)}", 1)
    x.Q("b)", "Complète le tableau pour deux charges. Écart = (U_{2} chargé − U_{2} à vide) / U_{2} à vide.")
    rows = [["Charge R_{L}", "R_{2} // R_{L}", "U_{2}", "Écart"]]
    u20 = div(u, r1, r2)
    for rl in (10 * k, 100 * k):
        r2l = par(r2, rl); u2 = div(u, r1, r2l)
        rows.append([ing(rl, "Ω"), ("R", ing(r2l, "Ω")), ("R", ing(u2, "V")), ("R", ing((u2 - u20) / u20 * 100, "") + " %")])
    x.TABLE([3.6, 4.4, 4.0, TW - 12.0 - 0.02], rows, height=0.6, size=10)
    x.Q("c)", "Quelle règle en tires-tu pour choisir la charge d'un diviseur ?")
    x.ANS("Une charge en parallèle sur R_{2} fait toujours baisser U_{2}. Si R_{L} ≥ 10 · R_{2}, l'écart reste de quelques pour cent.", 2)
    x.BOX(["Si difficulté",
           "Redessine le schéma avec R_{L} : R_{2} et R_{L} sont en parallèle. Calcule d'abord leur résistance équivalente, "
           "puis utilise la formule du diviseur avec cette résistance à la place de R_{2}."], only_corr=False)

    # ---------------------------------------------------------------- N°4
    x.HR(); x.EX(4, "Dépannage (≈ 8 min)", [("Présentation diapositives 2 et 6", S.teams_url("100"))])
    x.CTX("sur un autre robot, le diviseur 22 kΩ / 10 kΩ de la surveillance de batterie (12 V) donne des valeurs bizarres. "
          "Tu mesures U_{2} au multimètre (résistance interne 10 MΩ).")
    x.Q("a)", "Pour chaque mesure, dis si le diviseur fonctionne et, sinon, donne deux pannes possibles.")
    rows = [["U_{2} mesurée", "Fonctionne ?", "Pannes possibles"],
            ["3,75 V", ("R", "oui"), ("R", "aucune : 12 V · 10 kΩ / 32 kΩ = 3,75 V")],
            ["12 V", ("R", "non"), ("R", "R_{2} coupée, ou R_{1} en court-circuit")],
            ["0 V", ("R", "non"), ("R", "R_{1} coupée, ou R_{2} en court-circuit")]]
    x.TABLE([3.0, 2.8, TW - 5.8 - 0.02], rows, height=0.6, size=10)
    x.Q("b)", "R_{2} est coupée. Pourquoi le multimètre affiche-t-il presque 12 V et pas une valeur quelconque ?")
    x.ANS("Le multimètre remplace R_{2} : il forme un diviseur 22 kΩ / 10 MΩ, "
          f"qui donne 12 V · 10 MΩ / 10,022 MΩ = {ing(div(12, 22 * k, 10e6), 'V')}, presque toute la tension.", 2)

    # ---------------------------------------------------------------- auto-évaluation (fiche élève seulement, REGLES 4)
    if not corr:
        x.P("**Auto-évaluation**", keep=True, after=1, before=10, color=NAVY)
        x.P("Après la correction : ✓ je sais seul·e · ~ avec une aide · ✗ à revoir (reprends la diapositive indiquée).", keep=True, size=10)
        x.TABLE([TW / 4 - 0.01] * 4, [["Calculer un diviseur (N°1, diapo 4)", "Dimensionner (N°2, diapo 5)", "Effet d'une charge (N°3, diapo 6)",
                                       "Dépanner (N°4, diapos 2 et 6)"], ["", "", "", ""]], height=0.75, size=9, first_left=False)
    x.finish()


def produire(ctx):
    global S, CTX
    S, CTX = ctx.S, ctx
    build(False, ctx.sortie_de("110"))
    build(True, ctx.sortie_de("110C"))
