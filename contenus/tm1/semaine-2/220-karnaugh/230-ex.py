# -*- coding: utf-8 -*-
"""230 EX Simplification par Karnaugh (+ corrigé 230 EX C) · TM1 – El DT 1 · semaine 2.
Exercices sur la ligne de remplissage (LZ_2225). Sortie S, entrées A, B, C, D avec légende (REGLES 3.4).
Fonctions logiques et regroupements : figures.py (FONCTIONS) ; recalcul indépendant : verif.py."""
from moteur.fiche import RED, GREY, NAVY, TW, WD_ALIGN_PARAGRAPH

TITLE = "Simplification par Karnaugh"
S = CTX = FIG = None
LZ = lambda c: (c, S.lz_link(c))


def ligne_table(x, nom, entrees, sortie_donnee=True, height=0.45):
    """Table de vérité à 3 variables (C B A, puis S). sortie_donnee : S écrite ; sinon S à compléter (rouge dans le corrigé)."""
    v = FIG.valeurs(nom)
    rows = [entrees + ["S"]]
    for k in range(8):
        r = [str((k >> 2) & 1), str((k >> 1) & 1), str(k & 1)]
        r.append(str(v[k]) if sortie_donnee else ("R", str(v[k])))
        rows.append(r)
    x.TABLE([1.3, 1.3, 1.3, 1.6], rows, height=height, size=10.5, first_left=False)


def schema(x, corr, img, largeur_q, largeur_c):
    """Corrigé : image du tableau regroupé, termes reliés ; fiche élève : tableau vide à remplir."""
    x.IMG(img if corr else img.replace("_c", "_q"), largeur_c if corr else largeur_q, after=2)


def build(corr, out):
    T220 = S.teams_url("220")
    x = CTX.doc(corr, out, TITLE, "Corrigé" if corr else "Exercices",
                "230 EX Simplification par Karnaugh – " + ("Corrigé" if corr else "Exercices") + " – El DT 1",
                f"{S.matiere} – {S.classe} – {S.annee}")
    x.head(TITLE,
           [(f"Fiche d'exercices · {S.matiere} · Classe {S.classe} · {S.annee} · Champ ", None), (S.champ, S.fm(S.futuremem_champ)),
            (" · Objectif ", None), LZ("LZ_2225")],
           ["Déroulement (enseignant·e) : 45 min en binôme, après la présentation 220",
            "N°1 : 6 min ; N°2 : 10 min ; N°3 : 12 min ; N°4 : 10 min ; N°5 : 7 min.",
            "Exiger les cinq étapes : remplir, regrouper, lire chaque groupe, additionner, contrôler."],
           ["**Consignes :** en binôme, 45 min. Pour chaque tableau : remplis-le, entoure les groupes, lis chaque groupe, additionne les termes, "
            "puis contrôle le résultat avec la table de vérité.",
            "**Conventions :** sortie S, entrées A, B, C, D (sens donné par la légende). A est le poids faible. "
            "Dans le tableau, chaque variable vaut 1 dans sa zone jaune (A en haut, B en bas, C à gauche, D à droite), 0 ailleurs ; les codes gris (BA, DC) donnent la même chose. "
            "Relie chaque groupe à son terme par un trait. Le petit chiffre d'une case est le numéro de la combinaison."],
           [("Présentation : ", [(S.fichier("220"), T220), (" · pour réviser : ", None), ("page interactive 221", S.teams_url("221")),
                                 (" (Edge ou Chrome) · ", None), ("animation 225", S.teams_url("225"))]),
            ("Algèbre de Boole : ", [(S.fichier("200"), S.teams_url("200")), (" · ", None), (S.fichier("210"), S.teams_url("210"))])])

    x.CTX("la ligne de remplissage de boissons. Les tables de vérité ont été relevées au banc sur les anciennes commandes à relais. "
          "Les capteurs donnent 1 quand ce qu'ils surveillent est vrai ; un actionneur est en marche quand sa sortie vaut 1.")

    # ---- N°1 et N°2 : même table
    x.EX(1, "Écrire la somme de produits (≈ 6 min)", [("Présentation 220, diapositive 2", T220), LZ("LZ_2225")])
    x.CTX("voyant de contrôle de la vanne. S : voyant allumé, A : vanne ouverte, B : bouteille sous le bec, C : niveau de la cuve suffisant.")
    ligne_table(x, "n1", ["C", "B", "A"])
    x.Q("a)", "Combien de lignes valent 1 ? Combien de produits aura la somme de produits ?")
    x.ANS("3 lignes à 1 (001, 011, 111) : 3 produits.", 1)
    x.Q("b)", "Écris la somme de produits de S.")
    x.ANS("$S=A\\cdot \\bar{B}\\cdot \\bar{C}+A\\cdot B\\cdot \\bar{C}+A\\cdot B\\cdot C$", 2)

    x.HR(); x.EX(2, "Remplir, regrouper, lire (≈ 10 min)", [("Présentation 220, diapositives 3 à 7", T220), LZ("LZ_2225")])
    x.Q("a)", "Reporte la table du N°1 dans le tableau de Karnaugh, puis entoure les groupes.")
    schema(x, corr, "f_n1_c.png", 6.0, 7.0)
    x.Q("b)", "Lis chaque groupe et écris l'équation simplifiée.")
    x.ANS("Groupe 001 et 011 : dans la zone A, hors de la zone C, à cheval sur B → $A\\cdot \\bar{C}$. Groupe 011 et 111 : dans les zones A et B, à cheval sur C → $A\\cdot B$.\n"
          "$S=A\\cdot \\bar{C}+A\\cdot B$", 3)
    x.Q("c)", "Contrôle : sur quelles lignes ton équation donne-t-elle S = 1 ? Compare avec la table.")
    x.ANS("A · C̄ : lignes 001 et 011 ; A · B : lignes 011 et 111. Ensemble : 001, 011, 111, les trois lignes à 1 de la table.", 2)

    # ---- N°3 : quatre variables
    x.HR(); x.EX(3, "Quatre variables : quels capteurs servent ? (≈ 12 min)", [("Présentation 220, diapositives 8 et 9", T220), LZ("LZ_2225")])
    x.CTX("un collègue a branché quatre capteurs A, B, C, D sur la commande « capteurs cohérents » (S = 1 : tout va bien). "
          "La table relevée au banc donne S = 1 pour les combinaisons 0, 2, 5, 7, 8, 10, 13 et 15, et S = 0 pour les autres.")
    x.Q("a)", "Écris un 1 dans les cases de ces combinaisons (le petit chiffre est le numéro), un 0 dans les autres, puis entoure les groupes.")
    schema(x, corr, "f_n3_c.png", 7.0, 8.0)
    x.Q("b)", "Écris l'équation simplifiée.")
    x.ANS("Les quatre coins : hors de A et hors de C, à cheval sur B et sur D → $\\bar{A}\\cdot \\bar{C}$. Le carré du centre : dans les zones A et C → $A\\cdot C$.\n"
          "$S=\\bar{A}\\cdot \\bar{C}+A\\cdot C$", 3)
    x.Q("c)", "Quels capteurs ne servent à rien ? Que vérifie finalement cette commande ?")
    x.ANS("B et D disparaissent : on peut les débrancher. S = 1 quand A et C ont la même valeur : c'est une porte NON-OU exclusif (74HC7266), "
          "qui contrôle deux capteurs redondants.", 2)

    # ---- N°4 : cas indifférents
    x.HR(); x.EX(4, "La pompe de vidange : les cas indifférents (≈ 10 min)", [("Présentation 220, diapositive 12", T220), LZ("LZ_2225")])
    x.CTX("S : pompe de vidange en marche, A : machine en marche, B : capteur bas mouillé, C : capteur haut mouillé.")
    x.P("La pompe vide la cuve quand le niveau haut est atteint, ou quand la machine est arrêtée et qu'il reste du liquide (capteur bas mouillé).",
        keep=True, after=3)
    ligne_table(x, "vid", ["C", "B", "A"])
    x.Q("a)", "Pourquoi les lignes 100 et 101 valent-elles X ?")
    x.ANS("Le capteur haut ne peut pas être mouillé (C = 1) si le capteur bas est sec (B = 0) : ces combinaisons n'arrivent jamais.", 2)
    x.Q("b)", "Remplis le tableau (X compris), puis entoure les groupes en utilisant les X qui aident.")
    schema(x, corr, "f_n4_c.png", 5.6, 7.0)
    x.Q("c)", "Écris l'équation simplifiée. Relis-la en français.")
    x.ANS("Toute la zone C (avec les deux X) : $C$. Le groupe 010 et 110 : hors de A, dans la zone B, à cheval sur C → $\\bar{A}\\cdot B$.\n"
          "$S=C+\\bar{A}\\cdot B$ : la pompe tourne si le niveau haut est atteint, ou si la machine est arrêtée et que le capteur bas est mouillé.", 2)
    x.Q("d)", "Quelle équation obtiendrais-tu sans utiliser les X ? Laquelle est la plus simple ?")
    if corr:
        x.IMG("f_n4_c0.png", 6.0, after=2)
    x.ANS("Sans les X : $S=B\\cdot C+\\bar{A}\\cdot B$, un terme de deux variables au lieu d'une. Avec les X, l'équation est plus courte.", 2)

    # ---- N°5 : comparer avec l'algèbre
    x.HR(); x.EX(5, "Comparer avec l'algèbre (≈ 7 min)", [("Présentation 220, diapositive 13", T220), ("Fiche 210 EX, N°4", S.teams_url("210")), LZ("LZ_2225")])
    x.CTX("le voyant « défaut remplissage » de la fiche 210 EX, S = A · B̄ + A · B · C̄. S : voyant allumé, A : vanne ouverte, "
          "B : bouteille sous le bec, C : niveau de la cuve suffisant.")
    x.Q("a)", "Complète la colonne S de la table de vérité.")
    ligne_table(x, "n5", ["C", "B", "A"], sortie_donnee=False, height=0.5)
    x.Q("b)", "Remplis le tableau de Karnaugh, entoure les groupes et écris l'équation simplifiée.")
    schema(x, corr, "f_n5_c.png", 5.6, 7.0)
    x.ANS("$S=A\\cdot \\bar{B}+A\\cdot \\bar{C}$", 1)
    x.Q("c)", "Avec la distributivité puis De Morgan, retrouve le résultat de la fiche 210 EX.")
    x.ANS("$S=A\\cdot (\\bar{B}+\\bar{C})=A\\cdot \\bar{B\\cdot C}$ : le même résultat qu'avec l'algèbre (fiche 210 EX, N°4).", 2)

    if not corr:
        x.P("**Auto-évaluation**", keep=True, after=1, before=10, color=NAVY)
        x.P("Après la correction : ✓ je sais seul·e · ~ avec une aide · ✗ à revoir (reprends la diapositive indiquée).", keep=True, size=10)
        x.TABLE([TW / 5 - 0.01] * 5, [["Somme de produits (N°1, diapo 2)", "Remplir et regrouper (N°2, diapos 3 à 7)", "Quatre variables (N°3, diapos 8 et 9)",
                                       "Cas indifférents (N°4, diapo 12)", "Karnaugh et algèbre (N°5, diapo 13)"], ["", "", "", "", ""]],
                height=0.75, size=9, first_left=False)
    x.finish()


def produire(ctx):
    global S, CTX, FIG
    S, CTX = ctx.S, ctx
    FIG = S.module("figures")
    build(False, ctx.sortie_de("230"))
    build(True, ctx.sortie_de("230C"))
