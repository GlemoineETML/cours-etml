# -*- coding: utf-8 -*-
"""300 — Champ électrique et condensateur (ELEO-MLO3, 3e année). 28 diapositives."""
from deck_helpers import *

OUT = "out/300 Champ électrique et condensateur.pptx"


def eq(slide, nom, x, y, w):
    return picture(slide, nom, x, y, w)


# =============================================================== 1. TITRE
s = new("title")
title_of(s, "Champ électrique\net condensateur", 36)
sp = s.placeholders[1].text_frame
sp.clear()
fill(sp.paragraphs[0], "ELEO-MLO3 · 3e année · révision avant le test n° 1", 19, NAVY)
textbox(s, Inches(0.75), Inches(5.22), Inches(5.0), Inches(0.4),
        [("Version : 09.2026 / 1.0  ·  durée 40 minutes", 11, GREY, False)])
notes(s, "Cours de révision de 40 minutes. Quatre blocs : la quantité d'électricité "
         "(5 min), le champ électrique (8 min), le condensateur (10 min), le régime "
         "transitoire (13 min), synthèse (4 min). La fiche d'exercices se fait "
         "ensuite, en autonomie.")

# =============================================================== 2. OBJECTIFS
s = new()
title_of(s, "Ce que le test demandera")
body_of(s, [
    (0, "Expliquer ce que représentent les lignes d’un champ électrique", {"space": 9}),
    (0, "Calculer la capacité équivalente d’un réseau de condensateurs", {"space": 9}),
    (0, "Retrouver une capacité inconnue à partir d’une courbe i_{C}(t)", {"space": 9}),
    (0, "Calculer τ, U_{C} max et I_{C} max, puis tracer u_{C}(t) et i_{C}(t) "
        "avec les axes gradués", {"space": 9}),
], box=(Inches(0.51), Inches(1.55), Inches(8.33), Inches(2.9)))
textbox(s, Inches(0.51), Inches(4.55), Inches(8.33), Inches(1.0),
        [("Matériel autorisé : calculette et formulaire personnel.", 16, NAVY, True),
         ("Le formulaire ne pense pas à ta place — la méthode, elle, s’apprend.",
          15, GREY, False)])
notes(s, "Annoncer d'emblée les quatre types de questions : c'est la structure du "
         "test. Chaque bloc du cours correspond à l'une d'elles.")

# =============================================================== 3. FIL ROUGE
s = new()
title_of(s, "Le fil rouge de la leçon")
body_of(s, [
    (0, "① La charge Q — ce qui circule et ce qui se stocke",
     {"space": 14, "size": 20, "nobullet": True}),
    (0, "② Le champ électrique E — ce qui pousse les charges",
     {"space": 14, "size": 20, "nobullet": True}),
    (0, "③ Le condensateur C — le composant qui stocke la charge",
     {"space": 14, "size": 20, "nobullet": True}),
    (0, "④ Le régime transitoire — ce qui se passe pendant qu’il se remplit "
        "ou se vide", {"space": 14, "size": 20, "nobullet": True}),
], box=(Inches(0.6), Inches(1.70), Inches(8.1), Inches(3.0)))
textbox(s, Inches(0.6), Inches(4.75), Inches(8.1), Inches(0.6),
        [("Les quatre questions du test suivent exactement cet ordre.", 16, RED, True)])
notes(s, "Donner la carte avant le voyage : les élèves de 3e année ont déjà vu ces "
         "notions séparément, l'enjeu est de les relier.")

# =============================================================== 4. LA CHARGE
s = new()
title_of(s, "① La quantité d’électricité")
eq(s, "eq_04_charge.png", Inches(0.72), Inches(1.62), Inches(7.9))
textbox(s, Inches(0.6), Inches(4.35), Inches(8.1), Inches(1.2),
        [("Ordre de grandeur : un accumulateur de smartphone de 3000 mAh stocke "
          "3 · 10³ · 10⁻³ · 3,6 · 10³ ≈ 1,1 · 10⁴ C.", 15, GREY, False)])
notes(s, "Insister : le coulomb n'est pas une unité exotique, c'est un ampère-seconde. "
         "Le mAh des batteries est un coulomb déguisé (1 mAh = 3,6 C).")

# =============================================================== 5. EXEMPLE 1
s = new()
title_of(s, "Exemple 1 — un chargeur débite 250 mA pendant 2 h")
eq(s, "eq_05_ex1.png", Inches(0.72), Inches(1.75), Inches(7.9))
textbox(s, Inches(0.6), Inches(3.55), Inches(8.1), Inches(1.6),
        [("Toujours dans cet ordre : la formule littérale, puis les nombres avec "
          "les puissances de dix, puis le résultat en notation ingénieur.",
          16, NAVY, True),
         ("Les secondes d’abord : 2 h = 2 · 3600 = 7,2 · 10³ s.", 15, GREY, False)])
notes(s, "C'est la première application des trois temps. Les rappeler à voix haute "
         "à chaque exemple du cours — c'est ce qui sera exigé au test.")

# =============================================================== 6. LE CHAMP
s = new()
title_of(s, "② Le champ électrique")
picture(s, "60_lignes_champ.png", Inches(0.60), Inches(1.48), Inches(8.15), Inches(3.1))
body_of(s, [
    (0, "Un champ existe là où une charge subit une force. Il se dessine par des "
        "lignes de champ.", {"nobullet": True, "size": 18}),
], box=(Inches(0.6), Inches(4.70), Inches(8.1), Inches(0.8)))
notes(s, "Le champ n'est pas visible : les lignes sont une représentation. "
         "Elles servent à lire d'un coup d'œil la direction, le sens et l'intensité.")

# =============================================================== 7. LIGNES DE CHAMP
s = new()
title_of(s, "Les lignes de champ — la réponse attendue")
body_of(s, [
    (0, "Elles montrent la DIRECTION de la force qu’une charge subirait : la force "
        "est tangente à la ligne.", {"space": 10, "size": 18}),
    (0, "Leur flèche donne le SENS de la force sur une charge POSITIVE.",
     {"space": 10, "size": 18}),
    (0, "Leur DENSITÉ donne l’intensité : serrées = champ fort, écartées = champ "
        "faible.", {"space": 10, "size": 18}),
    (0, "Elles partent du + et arrivent au −, et sont perpendiculaires aux surfaces "
        "conductrices.", {"space": 10, "size": 18}),
    (0, "Elles ne se croisent jamais : en un point, la force n’a qu’une direction.",
     {"space": 10, "size": 18}),
], box=(Inches(0.51), Inches(1.55), Inches(8.33), Inches(3.5)))
textbox(s, Inches(0.51), Inches(5.05), Inches(8.33), Inches(0.6),
        [("Au test, deux de ces cinq points bien formulés suffisent pour les 2 points.",
          15, RED, True)])
notes(s, "Question 1 du test. Faire écrire la réponse en une phrase par chacun, "
         "puis lire deux ou trois copies à voix haute. La formulation compte.")

# =============================================================== 8. CHAMP UNIFORME
s = new()
title_of(s, "Le champ uniforme d’un condensateur plan")
picture(s, "62_condo_plan.png", Inches(1.75), Inches(1.30), Inches(6.5), Inches(2.05))
eq(s, "eq_08_champ.png", Inches(1.05), Inches(3.45), Inches(6.8))
notes(s, "Entre deux armatures planes le champ est le même partout : c'est le seul "
         "cas où E = U/d s'applique directement. Le rappeler, sinon ils l'utilisent "
         "partout.")

# =============================================================== 9. EXEMPLE 2
s = new()
title_of(s, "Exemple 2 — 400 V sur un isolant de 0,2 mm")
eq(s, "eq_09_ex2.png", Inches(0.72), Inches(1.70), Inches(7.9))
textbox(s, Inches(0.6), Inches(3.50), Inches(8.1), Inches(1.8),
        [("La rigidité diélectrique de l’air vaut environ 3 MV/m.", 17, NAVY, True),
         ("2 MV/m reste en dessous : l’isolant tient. À 0,1 mm on serait à 4 MV/m — "
          "claquage.", 16, RED, False),
         ("C’est pour cela qu’un condensateur porte toujours une tension maximale.",
          15, GREY, False)])
notes(s, "Faire le lien avec le composant réel : la tension de service imprimée sur "
         "un condensateur vient directement de cette limite.")

# =============================================================== 10. LE CONDENSATEUR
s = new()
title_of(s, "③ Le condensateur")
picture(s, "61_symboles_condo.png", Inches(0.75), Inches(1.42), Inches(7.6), Inches(1.55))
eq(s, "eq_10_condo.png", Inches(0.72), Inches(3.10), Inches(7.7))
notes(s, "Symboles CEI. Insister sur le polarisé : inversé, un électrolytique "
         "chauffe puis explose. C'est la faute de câblage la plus fréquente au labo.")

# =============================================================== 11. GÉOMÉTRIE
s = new()
title_of(s, "De quoi dépend la capacité")
eq(s, "eq_11_geometrie.png", Inches(0.72), Inches(1.60), Inches(7.9))
body_of(s, [
    (0, "Grande surface en regard → grand C", {"space": 9, "size": 18}),
    (0, "Isolant mince → grand C (mais tension maximale plus faible)",
     {"space": 9, "size": 18}),
    (0, "Bon diélectrique (ε_{r} élevé) → grand C", {"space": 9, "size": 18}),
], box=(Inches(0.6), Inches(3.15), Inches(8.1), Inches(1.9)))
textbox(s, Inches(0.6), Inches(5.05), Inches(8.1), Inches(0.6),
        [("Toujours un compromis : plus de capacité, moins de tenue en tension.",
          15, RED, True)])
notes(s, "Trois leviers, un compromis. Cela explique pourquoi un 470 µF fait la "
         "taille d'un dé et un 10 nF celle d'une lentille.")

# =============================================================== 12. ÉNERGIE
s = new()
title_of(s, "L’énergie stockée")
eq(s, "eq_12_energie.png", Inches(0.72), Inches(1.55), Inches(7.9))
textbox(s, Inches(0.6), Inches(4.35), Inches(8.1), Inches(1.0),
        [("Un condensateur chargé reste dangereux après la coupure : "
          "il faut le décharger avant d’intervenir.", 16, RED, True)])
notes(s, "Exemple chiffré : 10 µF sous 100 V. Rappeler la consigne de sécurité du "
         "labo — décharger avec une résistance, jamais avec un tournevis.")

# =============================================================== 13. GROUPEMENTS
s = new()
title_of(s, "Grouper des condensateurs")
picture(s, "63_groupements.png", Inches(0.60), Inches(1.40), Inches(8.15), Inches(2.15))
eq(s, "eq_13_groupements.png", Inches(1.15), Inches(3.60), Inches(6.5))
notes(s, "Lire la figure d'abord, la formule ensuite. Les deux condensateurs ont "
         "les mêmes valeurs dans les deux montages : 50 µF en parallèle, 12 µF en "
         "série. Le contraste frappe.")

# =============================================================== 14. L'INVERSE
s = new()
title_of(s, "Attention : c’est l’inverse des résistances")
body_of(s, [
    (0, "Résistances en série : on additionne. Condensateurs en série : "
        "somme des inverses.", {"space": 14, "size": 19}),
    (0, "Résistances en parallèle : somme des inverses. Condensateurs en "
        "parallèle : on additionne.", {"space": 14, "size": 19}),
    (0, "En parallèle, les surfaces s’ajoutent → C augmente. En série, les épaisseurs "
        "s’ajoutent → C diminue.", {"space": 14, "size": 19, "color": BLUE}),
], box=(Inches(0.6), Inches(1.70), Inches(8.1), Inches(2.9)))
textbox(s, Inches(0.6), Inches(4.70), Inches(8.1), Inches(0.9),
        [("Le moyen sûr de ne pas se tromper : revenir à la géométrie, "
          "pas à la formule.", 16, RED, True)])
notes(s, "C'est l'erreur numéro un du chapitre. L'explication par la géométrie est "
         "ce qui reste : deux condensateurs côte à côte, c'est une plus grande "
         "surface ; l'un derrière l'autre, c'est un isolant plus épais.")

# =============================================================== 15. EXEMPLE 3 énoncé
s = new()
title_of(s, "Exemple 3 — capacité équivalente entre A et B")
picture(s, "64_reseau.png", Inches(1.05), Inches(1.55), Inches(7.9), Inches(2.9))
body_of(s, [
    (0, "Même méthode qu’avec les résistances : on part du groupe le plus imbriqué "
        "et on remonte.", {"nobullet": True, "size": 18, "bold": True}),
], box=(Inches(0.6), Inches(4.65), Inches(8.1), Inches(0.8)))
notes(s, "Laisser 60 secondes : par quoi commencer ? Réponse attendue : C1 et C2, "
         "les seuls qui n'ont rien d'autre entre eux.")

# =============================================================== 16. EXEMPLE 3 calcul
s = new()
title_of(s, "Exemple 3 — la réduction, étape par étape")
picture(s, "64b_reduction.png", Inches(0.38), Inches(1.30), Inches(8.4), Inches(1.35))
eq(s, "eq_16_ex3.png", Inches(0.45), Inches(2.85), Inches(8.4))
notes(s, "Trois étapes, trois lignes. Faire remarquer que le résultat (10 µF) est "
         "plus petit que la plus petite capacité mise en série — c'est un contrôle "
         "de bon sens.")

# =============================================================== 17. TRANSITOIRE
s = new()
title_of(s, "④ Le condensateur en régime transitoire")
eq(s, "eq_17_transitoire.png", Inches(0.72), Inches(1.60), Inches(7.9))
textbox(s, Inches(0.6), Inches(4.10), Inches(8.1), Inches(1.3),
        [("Deux réflexes à avoir avant tout calcul :", 17, NAVY, True),
         ("· À t = 0, u_{C} garde la valeur qu’elle avait juste avant.", 16, NAVY, False),
         ("· En régime établi, i_{C} = 0 : le condensateur est un circuit ouvert.",
          16, NAVY, False)])
notes(s, "Ces deux réflexes résolvent la moitié de la question 4 du test avant "
         "même d'écrire une exponentielle.")

# =============================================================== 18. LA CHARGE
s = new()
title_of(s, "La charge à travers une résistance")
picture(s, "65_circuit_charge.png", Inches(1.75), Inches(1.38), Inches(6.5), Inches(2.05))
eq(s, "eq_18_charge.png", Inches(1.00), Inches(3.52), Inches(6.9))
notes(s, "τ = R·C : une résistance en ohms fois une capacité en farads donne des "
         "secondes. Le vérifier au tableau, cela évite les erreurs de préfixe.")

# =============================================================== 19. COURBES CHARGE
s = new()
title_of(s, "Les deux courbes de la charge")
picture(s, "80_charge.png", Inches(0.38), Inches(1.45), Inches(8.4), Inches(2.9))
body_of(s, [
    (0, "u_{C} part de zéro et monte ; i_{C} part de son maximum et descend. "
        "Toujours dans ce sens.", {"nobullet": True, "size": 17, "bold": True}),
], box=(Inches(0.6), Inches(4.75), Inches(8.1), Inches(0.8)))
notes(s, "Faire décrire les courbes avant de les commenter. Le point à τ (63 % et "
         "37 %) est celui qu'il faut savoir placer de mémoire.")

# =============================================================== 20. LES CINQ TAU
s = new()
title_of(s, "Combien de temps pour être chargé ?")
picture(s, "81_cinq_tau.png", Inches(0.40), Inches(1.42), Inches(8.4), Inches(2.85))
body_of(s, [
    (0, "Après 5 τ on considère le régime établi : il reste moins de 1 % d’écart.",
     {"nobullet": True, "size": 18, "bold": True}),
], box=(Inches(0.6), Inches(4.52), Inches(8.1), Inches(0.55)))
textbox(s, Inches(0.6), Inches(5.28), Inches(8.1), Inches(0.5),
        [("« S a été fermé suffisamment longtemps » dans un énoncé veut dire : "
          "plus de 5 τ.", 15, RED, True)])
notes(s, "La phrase de l'énoncé du test — « suffisamment longtemps pour que le "
         "condensateur se soit chargé complètement » — se traduit par : on part "
         "du régime établi.")

# =============================================================== 21. LA DÉCHARGE
s = new()
title_of(s, "La décharge")
eq(s, "eq_21_decharge.png", Inches(0.72), Inches(1.62), Inches(7.7))
textbox(s, Inches(0.6), Inches(3.90), Inches(8.1), Inches(1.5),
        [("La question qui coûte des points : dans QUELLE résistance le condensateur "
          "se vide-t-il ?", 17, RED, True),
         ("Quand un interrupteur s’ouvre, la source et les résistances qui étaient "
          "derrière lui ne comptent plus.", 16, NAVY, False)])
notes(s, "Erreur classique du test : prendre R1 + R2 ou R1 seul pour τ, alors que "
         "l'ouverture de S isole la maille de gauche.")

# =============================================================== 22. LECTURE INVERSE
s = new()
title_of(s, "Lire une courbe à l’envers")
eq(s, "eq_22_inverse.png", Inches(0.72), Inches(1.50), Inches(7.7))
textbox(s, Inches(0.6), Inches(4.85), Inches(8.1), Inches(0.7),
        [("Un seul point bien lu sur la courbe suffit à retrouver τ, donc C.",
          16, NAVY, True)])
notes(s, "C'est la question 3 du test. Le point le plus souvent proposé est la "
         "demi-valeur, parce qu'il se lit sans ambiguïté sur un graphe.")

# =============================================================== 23. EXEMPLE 4
s = new()
title_of(s, "Exemple 4 — retrouver C à partir de la courbe")
picture(s, "82_lecture.png", Inches(2.55), Inches(1.28), Inches(4.9), Inches(1.85))
eq(s, "eq_23_ex4.png", Inches(1.00), Inches(3.20), Inches(7.6))
notes(s, "U = 20 V, R = 1 kΩ. Insister sur l'étape 1 : I₀ ne se lit pas, il se "
         "calcule. Le résultat 21,6 nF s'arrondit à la valeur normalisée 22 nF.")

# =============================================================== 24. MÉTHODE OUVERTURE
s = new()
title_of(s, "Régime établi, puis ouverture : la méthode")
picture(s, "66_circuit_ouverture.png", Inches(1.85), Inches(1.30), Inches(6.3), Inches(1.95))
body_of(s, [
    (0, "① S fermé depuis longtemps : i_{C} = 0, donc U_{C} max = tension aux bornes "
        "de la résistance en parallèle avec C",
     {"space": 7, "size": 17, "nobullet": True}),
    (0, "② S ouvert : identifier dans quelle résistance C se décharge",
     {"space": 7, "size": 17, "nobullet": True}),
    (0, "③ τ = R · C avec CETTE résistance",
     {"space": 7, "size": 17, "nobullet": True}),
    (0, "④ I_{C} max = U_{C} max / R, puis tracer les deux courbes",
     {"space": 7, "size": 17, "nobullet": True}),
], box=(Inches(0.51), Inches(3.35), Inches(8.3), Inches(2.3)))
notes(s, "Quatre temps, toujours les mêmes. Les faire noter : c'est la méthode "
         "attendue à la question 4 du test.")

# =============================================================== 25. EXEMPLE 5 a
s = new()
title_of(s, "Exemple 5 — étape ① le régime établi")
picture(s, "66b_exemple5.png", Inches(1.95), Inches(1.25), Inches(6.1), Inches(1.9))
eq(s, "eq_25_ex5a.png", Inches(0.45), Inches(3.25), Inches(8.4))
notes(s, "Le condensateur ne consomme rien en régime établi : R1 et R2 forment un "
         "simple diviseur de tension. U_C max = 8 V.")

# =============================================================== 26. EXEMPLE 5 b
s = new()
title_of(s, "Exemple 5 — étapes ② à ④")
eq(s, "eq_26_ex5b.png", Inches(0.55), Inches(1.28), Inches(8.0))
picture(s, "83_decharge.png", Inches(0.38), Inches(4.32), Inches(8.4), Inches(1.78))
notes(s, "R1 et E disparaissent avec l'ouverture de S. τ = 80 µs, I_C max = 400 mA. "
         "Faire remarquer que le courant, lui, a bien sauté de 0 à 400 mA.")

# =============================================================== 27. PIÈGES
s = new()
title_of(s, "Les cinq pièges du test")
body_of(s, [
    (0, "Confondre mF, µF, nF et pF — écrire la puissance de dix, toujours",
     {"space": 9, "size": 18}),
    (0, "Prendre la mauvaise résistance pour τ après l’ouverture d’un interrupteur",
     {"space": 9, "size": 18}),
    (0, "Additionner les capacités en série comme des résistances",
     {"space": 9, "size": 18}),
    (0, "Croire que u_{C} peut sauter : elle ne saute jamais, i_{C} si",
     {"space": 9, "size": 18}),
    (0, "Rendre un graphe sans grandeur ni unité sur les axes — des points perdus "
        "pour rien", {"space": 9, "size": 18}),
], box=(Inches(0.51), Inches(1.55), Inches(8.33), Inches(3.4)))
textbox(s, Inches(0.51), Inches(5.00), Inches(8.33), Inches(0.7),
        [("Reporter TOUTES les valeurs calculées sur chacun des graphes : "
          "τ, U_{C} max, I_{C} max.", 16, RED, True)])
notes(s, "Reprendre mot pour mot la consigne du test : « N'oubliez pas de reporter "
         "la grandeur et l'unité de chaque axe ».")

# =============================================================== 28. FORMULAIRE
s = new()
title_of(s, "Le formulaire à emporter")
eq(s, "eq_27_formulaire.png", Inches(0.45), Inches(1.42), Inches(8.4))
textbox(s, Inches(0.6), Inches(5.02), Inches(8.1), Inches(1.05),
        [("À vous : fiche 310 EX, sept exercices calqués sur le test.", 18, NAVY, True),
         ("En dernière page, la grille d’auto-évaluation — remplissez-la avant de "
          "regarder le corrigé.", 16, GREY, False)])
notes(s, "Distribuer la fiche. Les exercices 1 à 4 couvrent les questions 1 à 2 du "
         "test, les exercices 5 à 7 les questions 3 et 4.")

import os
os.makedirs("out", exist_ok=True)
prs.save(OUT)
print("saved", OUT, "|", len(prs.slides.__iter__.__self__._sldIdLst), "diapositives")
