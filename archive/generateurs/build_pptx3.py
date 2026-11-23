# -*- coding: utf-8 -*-
"""140 — Circuits mixtes et simplification (semaine 3, périodes 9 à 13)."""
from deck_helpers import *

OUT = "out/140 Circuits mixtes et simplification.pptx"

# =============================================================== 1. TITRE
s = new("title")
title_of(s, "Circuits mixtes\net simplification", 36)
sp = s.placeholders[1].text_frame
sp.clear()
fill(sp.paragraphs[0], "El Dim1 – Notions de base · semaine 3, périodes 9 à 13", 19, NAVY)
textbox(s, Inches(0.75), Inches(5.22), Inches(5.0), Inches(0.4),
        [("Version : 08.2026 / 1.0", 11, GREY, False)])
notes(s, "Cinq périodes : 9 à 11 la méthode et les calculs, 12 et 13 le dessin de "
         "schémas et les mesures. Objectifs LZ 1923, 1924, 1949, 1952, 7857, 7995.")

# =============================================================== 2. OBJECTIFS
s = new()
title_of(s, "Ce que tu sauras faire à la fin")
body_of(s, [
    (0, "Reconnaître ce qui est en série et ce qui est en parallèle dans un schéma",
     {"space": 8, "size": 18}),
    (0, "Réduire un circuit mixte pas à pas jusqu’à une seule résistance",
     {"space": 8, "size": 18}),
    (0, "Calculer U, I et P de chaque résistance, et contrôler avec les lois de Kirchhoff",
     {"space": 8, "size": 18}),
    (0, "Dessiner un schéma propre aux symboles CEI", {"space": 8, "size": 18}),
    (0, "Câbler le montage, mesurer, et remplir un protocole de mesure",
     {"space": 8, "size": 18}),
], box=(Inches(0.51), Inches(1.48), Inches(8.33), Inches(3.3)))
textbox(s, Inches(0.51), Inches(4.85), Inches(8.33), Inches(0.7),
        [("Objectifs évaluateurs : LZ 1923 · 1924 · 1949 · 1952 · 7857 · 7995", 14,
          GREY, True)])
notes(s, "Les cinq objectifs correspondent aux cinq LZ du chapitre. Ils sont repris "
         "en grille d’auto-évaluation à la fin de la fiche d’exercices : l’élève doit "
         "pouvoir se situer lui-même sur chacun.")

# =============================================================== 3. ACCROCHE
s = new()
title_of(s, "Combien de courant tire ce montage ?")
picture(s, "42_exemple_C.png", Inches(0.55), Inches(1.55), Inches(8.25), Inches(3.5))
body_of(s, [
    (0, "Cinq résistances. Ni tout en série, ni tout en parallèle. Par où commencer ?",
     {"nobullet": True, "size": 19, "bold": True, "color": RED}),
], box=(Inches(0.6), Inches(5.05), Inches(8.1), Inches(0.7)))
notes(s, "Laisser le malaise s’installer 30 secondes. Demander qui saurait faire, "
         "sans donner la réponse. Promettre qu’à la fin de la période ils sauront "
         "réduire ce schéma en trois lignes. On y revient à la diapositive 19.")

# =============================================================== 4. RAPPEL ACTIF
s = new()
title_of(s, "Rappel — sans les notes")
body_of(s, [
    (0, "Dessine deux résistances en série, puis deux résistances en parallèle, "
        "en symboles CEI.", {"space": 20, "size": 20}),
    (0, "Écris la formule de la résistance équivalente dans chaque cas.",
     {"space": 20, "size": 20}),
    (0, "Dans un montage série, qu’est-ce qui est identique pour les deux "
        "résistances ? Et en parallèle ?", {"space": 20, "size": 20}),
], box=(Inches(0.65), Inches(1.75), Inches(8.0), Inches(3.6)))
notes(s, "5 minutes, cahier fermé. Ces trois réponses sont le socle de tout le "
         "chapitre : si elles ne sont pas solides, la méthode pas à pas ne tiendra pas.")

# =============================================================== 5. RAPPEL CORRIGE
s = new()
title_of(s, "Rappel — les réponses")
picture(s, "eq_05_rappel.png", Inches(0.55), Inches(1.55), Inches(8.2))
body_of(s, [
    (0, "En série le COURANT est le même partout ; en parallèle c’est la TENSION.",
     {"nobullet": True, "size": 17, "bold": True, "color": RED}),
], box=(Inches(0.6), Inches(4.95), Inches(8.1), Inches(0.8)))
notes(s, "Le « produit sur somme » ne marche QUE pour deux résistances : c’est "
         "l’erreur la plus fréquente quand il y en a trois. Le faire écrire au "
         "formulaire avec cette restriction en toutes lettres.")

# =============================================================== 6. KIRCHHOFF
s = new()
title_of(s, "Les deux lois de Kirchhoff")
picture(s, "54_kirchhoff.png", Inches(1.15), Inches(1.22), Inches(6.95), Inches(2.42))
body_of(s, [
    (0, "Loi des nœuds : tout ce qui entre dans un nœud en ressort.",
     {"size": 15, "space": 4}),
    (0, "Loi des mailles : la somme des tensions des récepteurs = celle de la source.",
     {"size": 15, "space": 6}),
    (0, "Ces deux lois sont derrière tous les contrôles de ce chapitre.",
     {"nobullet": True, "size": 15, "bold": True, "color": RED}),
], box=(Inches(0.51), Inches(3.68), Inches(8.33), Inches(1.0)))
picture(s, "eq_06_kirchhoff.png", Inches(0.85), Inches(4.76), Inches(7.6))
notes(s, "Gustav Kirchhoff, 1845. Ce sont deux lois de conservation : la charge pour "
         "les nœuds, l’énergie pour les mailles. Ne pas les présenter comme des "
         "formules de plus : ce sont elles qui justifient que la somme des courants "
         "de branche fasse le courant total, et que la somme des chutes de tension "
         "fasse la tension de la source. Tout le chapitre repose dessus.")

# =============================================================== 7. PUISSANCE
s = new()
title_of(s, "Rappel : la puissance")
picture(s, "eq_07_puissance.png", Inches(1.9), Inches(1.55), Inches(5.6))
body_of(s, [
    (0, "Une seule loi, écrite de trois façons : on choisit celle dont on a les "
        "grandeurs.", {"nobullet": True, "size": 17, "space": 12, "italic": True}),
    (0, "Unité : le watt [W].  1 W = 1 V · 1 A", {"size": 17, "space": 10}),
    (0, "La somme des puissances de toutes les résistances = la puissance fournie "
        "par la source", {"size": 17, "space": 14}),
    (0, "Choisis la forme qui utilise les grandeurs que tu connais déjà.",
     {"nobullet": True, "size": 17, "bold": True, "color": RED}),
], box=(Inches(0.7), Inches(3.30), Inches(7.9), Inches(2.4)))
notes(s, "Les trois formes ne sont pas trois formules à mémoriser mais une seule, "
         "combinée à U = R · I. Faire remarquer que P = R · I² sert quand on connaît "
         "le courant, P = U²/R quand on connaît la tension. "
         "La puissance dissipée devient de la chaleur : c’est elle qui détermine si "
         "une résistance 0,25 W suffit ou non — on y reviendra au dimensionnement.")

# =============================================================== 8. RECONNAITRE
s = new()
title_of(s, "Reconnaître, avant de calculer")
body_of(s, [
    (0, "Deux résistances sont EN SÉRIE si :", {"bold": True, "size": 18, "space": 4}),
    (1, "elles se suivent sur un seul chemin, sans dérivation entre elles",
     {"size": 17, "space": 4}),
    (1, "le même courant les traverse", {"size": 17, "space": 16}),
    (0, "Deux résistances sont EN PARALLÈLE si :", {"bold": True, "size": 18,
                                                    "space": 4}),
    (1, "elles sont branchées entre les deux mêmes nœuds", {"size": 17, "space": 4}),
    (1, "elles ont la même tension à leurs bornes", {"size": 17, "space": 16}),
    (0, "Le critère sûr, c’est le nœud — pas la position sur le dessin.",
     {"nobullet": True, "size": 18, "bold": True, "color": RED}),
], box=(Inches(0.6), Inches(1.52), Inches(8.1), Inches(4.2)))
notes(s, "Un nœud est un point de connexion où arrivent au moins trois fils. "
         "Insister : un schéma peut être dessiné de dix façons différentes, seuls "
         "les nœuds ne mentent pas. C’est ce qui sauve devant un schéma mal dessiné.")

# =============================================================== 9. NOEUDS
s = new()
title_of(s, "Première chose à faire : repérer les nœuds")
picture(s, "40_exemple_A.png", Inches(0.5), Inches(1.45), Inches(5.1), Inches(4.1))
body_of(s, [
    (0, "Un nœud = au moins trois fils qui se rejoignent", {"size": 16, "space": 16}),
    (0, "Ici deux nœuds : A et B", {"size": 16, "space": 16}),
    (0, "R_{2} et R_{3} sont entre A et B → en parallèle",
     {"size": 16, "bold": True, "color": RED, "space": 16}),
    (0, "R_{1} n’a pas de dérivation à côté → en série avec le groupe",
     {"size": 16}),
], box=(Inches(5.75), Inches(1.75), Inches(3.05), Inches(3.9)))
notes(s, "Faire marquer les nœuds au crayon sur le schéma AVANT tout calcul. "
         "C’est un geste de méthode qui se note à l’évaluation pratique.")

# =============================================================== 10. LA METHODE
s = new()
title_of(s, "La méthode pas à pas")
body_of(s, [
    (0, "1.  Repérer et nommer les nœuds", {"nobullet": True, "size": 19,
                                            "space": 10, "bold": True}),
    (0, "2.  Trouver le groupe le plus imbriqué : celui qui ne contient aucun "
        "autre groupe", {"nobullet": True, "size": 19, "space": 10, "bold": True}),
    (0, "3.  Le remplacer par sa résistance équivalente et REDESSINER le schéma",
     {"nobullet": True, "size": 19, "space": 10, "bold": True}),
    (0, "4.  Recommencer jusqu’à obtenir une seule résistance", {"nobullet": True,
                                                                 "size": 19,
                                                                 "space": 10,
                                                                 "bold": True}),
    (0, "5.  Remonter : calculer U et I de chaque résistance, du total vers le détail",
     {"nobullet": True, "size": 19, "space": 14, "bold": True}),
    (0, "Redessiner à chaque étape n’est pas une perte de temps : c’est ce qui "
        "évite les erreurs.", {"nobullet": True, "size": 17, "color": RED,
                               "bold": True}),
], box=(Inches(0.6), Inches(1.50), Inches(8.1), Inches(4.25)))
notes(s, "Cette diapositive est la colonne vertébrale du chapitre (LZ 1923). "
         "La faire recopier telle quelle dans le formulaire personnel. "
         "L’étape 3 est celle que les élèves sautent : ils veulent tout garder en tête.")

# =============================================================== 11. EXEMPLE A
s = new()
title_of(s, "Exemple A — on descend")
picture(s, "48_reduction.png", Inches(0.6), Inches(1.38), Inches(8.15), Inches(2.2))
picture(s, "eq_A1.png", Inches(0.55), Inches(3.80), Inches(8.2))
notes(s, "Avec U = 12 V, R1 = 120 Ω, R2 = 200 Ω, R3 = 300 Ω. Contrôle immédiat : "
         "R2//R3 = 120 Ω est plus petit que 200 Ω, la plus petite des deux — "
         "toujours vrai en parallèle. Exiger les trois lignes : formule littérale, "
         "nombres avec les puissances de dix, résultat en notation ingénieur.")

# =============================================================== A2
s = new()
title_of(s, "Exemple A — la résistance totale et le courant")
picture(s, "eq_A2.png", Inches(0.55), Inches(1.65), Inches(8.2))
notes(s, "Le passage aux puissances de dix n’est pas une coquetterie : 240 Ω écrit "
         "0,24·10³ Ω fait sortir le courant en 10⁻³ A, donc directement en mA. "
         "L’élève qui s’arrête à 0,05 A n’a pas fini son travail.")

# =============================================================== 12. REMONTEE A
s = new()
title_of(s, "Exemple A — on remonte")
body_of(s, [
    (0, "R_{1} porte tout le courant ; le groupe prend ce qui reste — loi des mailles.",
     {"nobullet": True, "size": 16, "italic": True}),
], box=(Inches(0.6), Inches(1.40), Inches(8.1), Inches(0.5)))
picture(s, "eq_A3.png", Inches(0.55), Inches(2.05), Inches(8.2))
notes(s, "Verbaliser la remontée EN NOMMANT la loi : c’est la loi des mailles qui "
         "donne la tension restante pour le groupe parallèle.")

# =============================================================== A4
s = new()
title_of(s, "Exemple A — les courants de branche")
body_of(s, [
    (0, "R_{2} et R_{3} ont la même tension à leurs bornes : 6 V.",
     {"nobullet": True, "size": 16, "italic": True}),
], box=(Inches(0.6), Inches(1.36), Inches(8.1), Inches(0.5)))
picture(s, "eq_A4.png", Inches(0.55), Inches(1.92), Inches(8.2))
notes(s, "Le contrôle par la loi des nœuds est obligatoire et se note. "
         "Contrôle de bon sens à faire AVANT de calculer : la plus petite résistance "
         "prend le plus grand courant.")

# =============================================================== 13. EXEMPLE B
s = new()
title_of(s, "Exemple B — l’autre couplage à trois")
picture(s, "41_exemple_B.png", Inches(0.45), Inches(1.42), Inches(3.85), Inches(3.3))
picture(s, "eq_B1.png", Inches(0.45), Inches(4.10), Inches(8.4))
notes(s, "Ici les deux résistances en série forment une BRANCHE, et c’est la branche "
         "entière qui est en parallèle avec R3. Les deux couplages à trois résistances "
         "sont maintenant vus : R1 + (R2//R3) et (R1+R2) // R3.")

# =============================================================== B2
s = new()
title_of(s, "Exemple B — les trois courants")
body_of(s, [
    (0, "Les deux branches sont sous la même tension U : chacune se calcule seule.",
     {"nobullet": True, "size": 16, "italic": True}),
], box=(Inches(0.6), Inches(1.36), Inches(8.1), Inches(0.5)))
picture(s, "eq_B2.png", Inches(0.55), Inches(1.90), Inches(8.2))
notes(s, "Différence essentielle avec l’exemple A : ici la tension de la source est "
         "directement aux bornes de chaque branche, il n’y a rien en série avant. "
         "On peut donc calculer les courants de branche sans passer par Rtot.")

# =============================================================== B3
s = new()
title_of(s, "Exemple B — les tensions et les contrôles")
picture(s, "eq_B3.png", Inches(0.55), Inches(1.55), Inches(8.2))
notes(s, "R1 et R2 sont traversées par I2, pas par I1 : c’est l’erreur la plus "
         "fréquente sur ce couplage. Les deux contrôles se font systématiquement.")

# =============================================================== 14. A TOI
s = new()
title_of(s, "À toi — cinq minutes")
picture(s, "43_a_toi_intro.png", Inches(0.5), Inches(1.45), Inches(4.9), Inches(3.9))
body_of(s, [
    (0, "1.  R_{tot} = ……… Ω", {"nobullet": True, "size": 18, "space": 14}),
    (0, "2.  I_{1} = ……… mA", {"nobullet": True, "size": 18, "space": 14}),
    (0, "3.  U_{1} = ……… V", {"nobullet": True, "size": 18, "space": 14}),
    (0, "4.  I_{2} = ……… mA", {"nobullet": True, "size": 18, "space": 14}),
    (0, "5.  I_{3} = ……… mA", {"nobullet": True, "size": 18}),
], box=(Inches(5.55), Inches(1.75), Inches(3.25), Inches(3.9)))
notes(s, "En binôme, 5 minutes.\n"
         "Corrigé : R2//R3 = (200·600)/800 = 150 Ω ; Rtot = 100 + 150 = 250 Ω ; "
         "I₁ = 18/250 = 72 mA ; U₁ = 100·0,072 = 7,2 V ; U₂₃ = 10,8 V ; "
         "I2 = 10,8/200 = 54 mA ; I3 = 10,8/600 = 18 mA. Contrôle 54 + 18 = 72 ✓\n"
         "FIN DE LA PÉRIODE 9.")

# =============================================================== AT1
s = new()
title_of(s, "À toi — le corrigé (1)")
picture(s, "eq_AT.png", Inches(0.55), Inches(1.55), Inches(8.2))
notes(s, "Corriger en projetant, mais faire d’abord venir un élève au tableau écrire "
         "sa première ligne. Le point à vérifier : a-t-il écrit la formule littérale "
         "AVANT de mettre les nombres ?")

# =============================================================== AT2
s = new()
title_of(s, "À toi — le corrigé (2)")
picture(s, "eq_AT2.png", Inches(0.55), Inches(1.50), Inches(8.2))
notes(s, "FIN DE LA PÉRIODE 9. Le contrôle final 54 + 18 = 72 mA doit apparaître "
         "sur la copie, pas seulement dans la tête.")

# =============================================================== 15. RAPPEL ECLAIR
s = new()
title_of(s, "Rappel éclair")
body_of(s, [
    (0, "Quelles sont les cinq étapes de la méthode ?", {"space": 22, "size": 21}),
    (0, "En parallèle, la résistance équivalente est-elle plus grande ou plus "
        "petite que la plus petite des deux ?", {"space": 22, "size": 21}),
    (0, "Dans un groupe parallèle, qu’est-ce qui est identique dans chaque branche ?",
     {"space": 22, "size": 21}),
], box=(Inches(0.7), Inches(1.80), Inches(8.0), Inches(3.6)))
notes(s, "2 minutes à l’oral, en interrogeant nominativement. Puis enchaîner sur "
         "la mise en forme des calculs.")

# =============================================================== 16. DEUX REGLES
s = new()
title_of(s, "Remonter : deux règles, pas plus")
body_of(s, [
    (0, "Dans une branche SÉRIE — c’est la loi des mailles :",
     {"bold": True, "size": 18, "space": 4}),
    (1, "le courant est le même partout → on calcule les tensions avec U = R · I",
     {"size": 16, "space": 4}),
    (1, "et la somme de ces tensions redonne celle de la source",
     {"size": 16, "space": 16}),
    (0, "Dans un groupe PARALLÈLE — c’est la loi des nœuds :",
     {"bold": True, "size": 18, "space": 4}),
    (1, "la tension est la même partout → on calcule les courants avec I = U / R",
     {"size": 16, "space": 4}),
    (1, "et la somme de ces courants redonne le courant qui entre dans le nœud",
     {"size": 16, "space": 16}),
    (0, "Les deux règles de remontée ne sont rien d’autre que les deux lois de "
        "Kirchhoff appliquées.", {"nobullet": True, "size": 17, "bold": True,
                                  "color": RED}),
], box=(Inches(0.6), Inches(1.50), Inches(8.1), Inches(3.1)))
picture(s, "eq_16_regles.png", Inches(0.55), Inches(4.65), Inches(8.2))
notes(s, "Point clé du chapitre : faire le lien explicite avec la diapositive 6. "
         "Les élèves retiennent souvent deux recettes sans voir qu’il s’agit des deux "
         "lois vues au début. Les faire écrire au formulaire juste sous les cinq "
         "étapes, avec le nom de la loi en face de chaque règle.")

# =============================================================== 17. TABLEAU
s = new()
title_of(s, "Présenter ses calculs : le tableau")
body_of(s, [
    (0, "Une ligne par résistance, quatre colonnes : R, U, I, P",
     {"size": 18, "space": 10}),
    (0, "Une ligne « total » en bas", {"size": 18, "space": 10}),
    (0, "On remplit ce qu’on sait, puis on complète ligne par ligne",
     {"size": 18, "space": 10}),
    (0, "Chaque valeur avec son unité et son préfixe : 30 mA, pas 0,03",
     {"size": 18, "space": 10, "color": RED, "bold": True}),
    (0, "Le tableau n’est pas de la décoration : c’est lui qui rend les contrôles "
        "possibles.", {"nobullet": True, "size": 17, "italic": True}),
], box=(Inches(0.6), Inches(1.70), Inches(8.1), Inches(3.9)))
notes(s, "Exigence de présentation évaluée (LZ 1924). Montrer un tableau vide au "
         "tableau noir et le remplir avec eux sur l’exemple suivant.")

# =============================================================== 18. CONTROLES
s = new()
title_of(s, "Cinq contrôles qui sauvent")
body_of(s, [
    (0, "En série, R_{tot} est plus GRANDE que la plus grande des résistances",
     {"size": 17, "space": 10}),
    (0, "En parallèle, R_{tot} est plus PETITE que la plus petite",
     {"size": 17, "space": 10}),
    (0, "Loi des mailles : la somme des tensions sur un chemin = celle de la source",
     {"size": 17, "space": 10}),
    (0, "Loi des nœuds : la somme des courants des branches = le courant entrant",
     {"size": 17, "space": 10}),
    (0, "La somme des puissances = U · I de la source", {"size": 17, "space": 14}),
    (0, "Un seul de ces contrôles qui échoue = un calcul faux quelque part.",
     {"nobullet": True, "size": 17, "bold": True, "color": RED}),
], box=(Inches(0.6), Inches(1.58), Inches(8.1), Inches(4.1)))
notes(s, "Les deux premiers contrôles se font AVANT tout calcul détaillé, en "
         "quelques secondes : ils attrapent la majorité des erreurs de formule. "
         "Les trois autres se font à la fin, sur le tableau.")

# =============================================================== 19. EXEMPLE C
s = new()
title_of(s, "Exemple résolu — le montage du début")
picture(s, "42_exemple_C.png", Inches(0.6), Inches(1.45), Inches(8.15), Inches(3.9))
body_of(s, [
    (0, "Groupe le plus imbriqué : R_{3} + R_{4}. On le réduit en premier.",
     {"nobullet": True, "size": 17, "bold": True, "color": RED}),
], box=(Inches(0.6), Inches(5.15), Inches(8.1), Inches(0.6)))
notes(s, "C’est le schéma de la diapositive 3 : boucler la promesse du début. "
         "Faire identifier le groupe le plus imbriqué par la classe avant de "
         "l’afficher — c’est l’étape 2 de la méthode, la seule qui demande du jugement.")

# =============================================================== C1
s = new()
title_of(s, "Exemple résolu — la réduction")
picture(s, "eq_C1.png", Inches(0.55), Inches(1.55), Inches(8.2))
notes(s, "Trois réductions successives, chacune en trois lignes. "
         "Contrôle immédiat à chaque étape : R234 = 200 Ω est plus petit que 300 Ω, "
         "la plus petite des deux résistances mises en parallèle.")

# =============================================================== C2
s = new()
title_of(s, "Exemple résolu — le courant et les tensions")
picture(s, "eq_C2.png", Inches(0.55), Inches(1.48), Inches(8.2))
notes(s, "R1, le groupe et R5 sont en série : tous les trois portent I1. "
         "Les trois tensions se calculent donc de la même façon.")

# =============================================================== C3
s = new()
title_of(s, "Exemple résolu — dans le groupe parallèle")
picture(s, "eq_C3.png", Inches(0.55), Inches(1.48), Inches(8.2))
notes(s, "U2 = 12 V est la tension commune aux deux branches du groupe. "
         "R3 et R4 sont en série : elles portent le même courant I3, "
         "et c’est ce courant qui donne U3 et U4.")

# =============================================================== C4
s = new()
title_of(s, "Exemple résolu — les puissances")
picture(s, "eq_C4.png", Inches(0.55), Inches(1.60), Inches(8.2))
notes(s, "Le bilan des puissances est le troisième contrôle. "
         "Faire remarquer que toutes les puissances sont des dizaines ou des "
         "centaines de milliwatts : des résistances 1/4 W suffisent largement.")

# =============================================================== 20. TABLEAU C
s = new()
title_of(s, "Exemple résolu — le tableau complet")
body_of(s, [
    (0, "R_{1} = 150 Ω    U_{1} = 9 V      I_{1} = 60 mA    P_{1} = 540 mW",
     {"nobullet": True, "size": 17, "space": 8}),
    (0, "R_{2} = 300 Ω    U_{2} = 12 V    I_{2} = 40 mA    P_{2} = 480 mW",
     {"nobullet": True, "size": 17, "space": 8}),
    (0, "R_{3} = 200 Ω    U_{3} = 4 V      I_{3} = 20 mA    P_{3} = 80 mW",
     {"nobullet": True, "size": 17, "space": 8}),
    (0, "R_{4} = 400 Ω    U_{4} = 8 V      I_{3} = 20 mA    P_{4} = 160 mW",
     {"nobullet": True, "size": 17, "space": 8}),
    (0, "R_{5} = 50 Ω      U_{5} = 3 V      I_{1} = 60 mA    P_{5} = 180 mW",
     {"nobullet": True, "size": 17, "space": 12}),
    (0, "R_{4} porte I_{3} comme R_{3} : même branche. R_{5} porte I_{1} comme R_{1}.",
     {"nobullet": True, "size": 15, "italic": True, "space": 10}),
    (0, "Mailles : 9 + 12 + 3 = 24 V ✓        Nœuds : 40 + 20 = 60 mA ✓",
     {"nobullet": True, "size": 16, "bold": True, "color": BLUE}),
], box=(Inches(0.55), Inches(1.55), Inches(8.2), Inches(4.2)))
notes(s, "Dérouler la remontée à voix haute : U1 = 150·0,06 = 9 V ; le groupe "
         "parallèle prend 200·0,06 = 12 V ; U5 = 50·0,06 = 3 V. Puis dans le groupe : "
         "I2 = 12/300 = 40 mA, I34 = 12/600 = 20 mA, d’où U3 = 4 V et U4 = 8 V. "
         "Contrôle des puissances : 0,54+0,48+0,08+0,16+0,18 = 1,44 W = 24·0,06 ✓\n"
         "Nommer les lois à voix haute en corrigeant : 9+12+3 = 24 V c’est la "
         "loi des mailles, 40+20 = 60 mA c’est la loi des nœuds au nœud A.")

# =============================================================== 21. E12
s = new()
title_of(s, "Dans la vraie vie : E12 et tolérance")
body_of(s, [
    (0, "En classe on utilise des valeurs rondes pour apprendre la méthode",
     {"size": 17, "space": 10}),
    (0, "En atelier, les résistances existent en valeurs normalisées — série E12 :",
     {"size": 17, "space": 6}),
    (0, "100 · 120 · 150 · 180 · 220 · 270 · 330 · 390 · 470 · 560 · 680 · 820",
     {"nobullet": True, "size": 17, "bold": True, "color": BLUE, "space": 12}),
    (0, "…et leurs multiples : 1 kΩ, 2,2 kΩ, 47 kΩ…", {"size": 16, "space": 12}),
    (0, "Tolérance courante ±5 % : une 470 Ω vaut entre 446,5 et 493,5 Ω",
     {"size": 17, "space": 10, "color": RED, "bold": True}),
    (0, "Les résultats ne tombent donc jamais ronds. C’est normal.",
     {"nobullet": True, "size": 17, "italic": True}),
], box=(Inches(0.6), Inches(1.58), Inches(8.1), Inches(4.1)))
notes(s, "Prépare la comparaison mesure / calcul du TP. Montrer un anneau doré sur "
         "une vraie résistance. FIN DES PÉRIODES 10-11.")

# =============================================================== 22. SCHEMA PROPRE
s = new()
title_of(s, "Dessiner un schéma propre")
body_of(s, [
    (0, "Traits horizontaux et verticaux uniquement, angles droits",
     {"size": 17, "space": 8}),
    (0, "Symboles CEI, jamais le zigzag américain pour la résistance",
     {"size": 17, "space": 8}),
    (0, "Jonction de fils : un point bien noir. Croisement sans liaison : pas de point",
     {"size": 17, "space": 8}),
    (0, "Chaque composant a son repère (R_{1}, R_{2}…) ET sa valeur",
     {"size": 17, "space": 8}),
    (0, "Source à gauche, circuit qui se lit de gauche à droite",
     {"size": 17, "space": 8}),
    (0, "Flèches de tension et de courant orientées et nommées",
     {"size": 17, "space": 8}),
    (0, "Cartouche : nom, classe, date, titre du montage",
     {"size": 17, "space": 8, "bold": True}),
], box=(Inches(0.6), Inches(1.55), Inches(8.1), Inches(4.2)))
notes(s, "LZ 1952. Ces sept règles servent de grille de correction pour le schéma "
         "rendu au TP : un point par règle respectée.")

# =============================================================== 23. AVANT APRES
s = new()
title_of(s, "Le même circuit, deux dessins")
picture(s, "49_tordu_propre.png", Inches(0.45), Inches(1.55), Inches(8.45), Inches(3.4))
body_of(s, [
    (0, "Même circuit, mêmes nœuds, mêmes résultats. Mais un seul des deux se "
        "corrige, se vérifie et se transmet.", {"nobullet": True, "size": 17,
                                                "bold": True}),
], box=(Inches(0.6), Inches(5.05), Inches(8.1), Inches(0.7)))
notes(s, "Faire trouver les défauts du dessin de gauche par la classe avant de "
         "commenter : traits obliques, aucune valeur, jonctions non marquées, "
         "source sans polarité.")

# =============================================================== 24. PROTOCOLE
s = new()
title_of(s, "Le protocole de mesure")
body_of(s, [
    (0, "But de la mesure, en une phrase", {"size": 17, "space": 7}),
    (0, "Schéma du montage avec les points de mesure repérés", {"size": 17,
                                                                "space": 7}),
    (0, "Matériel utilisé, avec le numéro d’inventaire des appareils",
     {"size": 17, "space": 7}),
    (0, "Valeurs calculées AVANT la manipulation", {"size": 17, "space": 7,
                                                    "bold": True, "color": RED}),
    (0, "Tableau des valeurs mesurées", {"size": 17, "space": 7}),
    (0, "Écart entre mesure et calcul, et son explication", {"size": 17, "space": 7}),
    (0, "Conclusion, date, nom, visa", {"size": 17, "space": 7}),
], box=(Inches(0.6), Inches(1.60), Inches(8.1), Inches(4.1)))
notes(s, "LZ 7857 et 7995. Le point capital est de calculer AVANT de mesurer : "
         "sinon on ne mesure plus, on justifie après coup. Un protocole doit pouvoir "
         "être refait à l’identique par quelqu’un d’autre, des mois plus tard.")

# =============================================================== 25. BRANCHER
s = new()
title_of(s, "Brancher les appareils")
picture(s, "50_montage_mesure.png", Inches(0.45), Inches(1.42), Inches(8.45), Inches(3.35))
body_of(s, [
    (0, "Ampèremètre EN SÉRIE : il faut ouvrir le circuit pour l’insérer",
     {"size": 16, "space": 6}),
    (0, "Voltmètre EN PARALLÈLE : il se pose sur les bornes, sans rien ouvrir",
     {"size": 16, "space": 6}),
    (0, "Calibre le plus grand d’abord, puis on descend", {"size": 16, "bold": True}),
], box=(Inches(0.51), Inches(4.85), Inches(8.33), Inches(1.0)))
notes(s, "Faire le geste devant eux avec de vrais cordons. Rappeler la borne mA "
         "séparée sur la plupart des multimètres, et le fusible qui la protège.")

# =============================================================== 26. PIEGE
s = new()
title_of(s, "L’erreur à ne pas faire")
picture(s, "51_piege.png", Inches(0.55), Inches(1.50), Inches(8.25), Inches(3.5))
body_of(s, [
    (0, "Un ampèremètre a une résistance quasi nulle. En parallèle sur un "
        "composant, il court-circuite la source : fusible grillé, au mieux.",
     {"nobullet": True, "size": 17, "bold": True, "color": RED}),
], box=(Inches(0.6), Inches(5.05), Inches(8.1), Inches(0.75)))
notes(s, "C’est LA panne du labo. Avant chaque mise sous tension : « où est mon "
         "ampèremètre ? ». Faire vérifier le montage du voisin avant d’alimenter.")

# =============================================================== 27. ECART
s = new()
title_of(s, "Comparer la mesure et le calcul")
body_of(s, [
    (0, "", {"nobullet": True, "size": 8, "space": 60}),
    (0, "Un écart de quelques pour-cent est NORMAL :", {"size": 17, "space": 6}),
    (1, "tolérance des résistances (±5 %)", {"size": 16, "space": 4}),
    (1, "précision de l’appareil et du calibre", {"size": 16, "space": 4}),
    (1, "résistance propre des appareils et des cordons", {"size": 16, "space": 14}),
    (0, "Un écart de 30 % ou un signe inattendu : ce n’est pas la tolérance, "
        "c’est une erreur de montage ou de calcul.",
     {"nobullet": True, "size": 17, "bold": True, "color": RED}),
], box=(Inches(0.6), Inches(2.55), Inches(8.1), Inches(3.2)))
picture(s, "eq_27_ecart.png", Inches(1.4), Inches(1.50), Inches(6.4))
notes(s, "Distinguer clairement incertitude et erreur : la première s’explique et "
         "se chiffre, la seconde se corrige. C’est le cœur de la conclusion du "
         "protocole.")

# =============================================================== 28. MONTAGE TP
s = new()
title_of(s, "Le montage du jour")
picture(s, "47_tp.png", Inches(0.45), Inches(1.48), Inches(4.75), Inches(3.95))
body_of(s, [
    (0, "1.  Calcule R_{tot}, I_{1}, U_{1}, U_{23}, I_{2} et I_{3}",
     {"nobullet": True, "size": 16, "space": 10}),
    (0, "2.  Dessine le schéma au propre", {"nobullet": True, "size": 16,
                                            "space": 10}),
    (0, "3.  Câble le montage sur la platine", {"nobullet": True, "size": 16,
                                                "space": 10}),
    (0, "4.  Fais vérifier avant de mettre sous tension", {"nobullet": True,
                                                           "size": 16, "space": 10,
                                                           "bold": True,
                                                           "color": RED}),
    (0, "5.  Mesure, note, compare, conclus", {"nobullet": True, "size": 16}),
], box=(Inches(5.35), Inches(1.75), Inches(3.45), Inches(3.9)))
notes(s, "Valeurs E12 : R1 = 220 Ω, R2 = 470 Ω, R3 = 1 kΩ, alimentation 10 V. "
         "Courant total d’environ 18,5 mA : sans danger et bien lisible sur le "
         "calibre 200 mA. Puissance maximale dans une résistance : 75 mW, "
         "largement dans les 1/4 W.")

# =============================================================== 29. EVALUATION
s = new()
title_of(s, "Ce que l’évaluation vérifiera")
body_of(s, [
    (0, "Tu identifies série et parallèle sur un schéma non standard  (LZ 1923)",
     {"size": 16, "space": 9}),
    (0, "Tu réduis un circuit de 5 résistances en montrant chaque étape  (LZ 1923)",
     {"size": 16, "space": 9}),
    (0, "Ton tableau R/U/I/P est complet, avec unités et préfixes  (LZ 1924)",
     {"size": 16, "space": 9}),
    (0, "Tu poses au moins deux contrôles et tu les rends visibles  (LZ 1924)",
     {"size": 16, "space": 9}),
    (0, "Ton schéma respecte les sept règles de dessin  (LZ 1952)",
     {"size": 16, "space": 9}),
    (0, "Ton montage est câblé et mesuré sans faute de branchement  (LZ 1949)",
     {"size": 16, "space": 9}),
    (0, "Ton protocole est complet et ta conclusion justifie l’écart  (LZ 7857/7995)",
     {"size": 16, "space": 9}),
], box=(Inches(0.55), Inches(1.52), Inches(8.2), Inches(4.25)))
notes(s, "Afficher cette diapositive au début du TP et la laisser visible. "
         "Chaque ligne est un critère observable, repris tel quel dans la grille "
         "d’auto-évaluation en fin de fiche d’exercices : l’élève sait exactement "
         "sur quoi il est attendu.")

# =============================================================== 30. SYNTHESE
s = new()
title_of(s, "L’essentiel en cinq lignes")
body_of(s, [
    (0, "Repérer les nœuds avant de calculer quoi que ce soit", {"space": 13}),
    (0, "Réduire du plus imbriqué vers l’extérieur, en redessinant", {"space": 13}),
    (0, "Remonter : même I en série, même U en parallèle", {"space": 13,
                                                            "bold": True}),
    (0, "Contrôler : ΣU sur un chemin, ΣI à un nœud, ΣP au total", {"space": 13}),
    (0, "Mesurer : ampèremètre en série, voltmètre en parallèle", {"space": 13}),
], box=(Inches(0.6), Inches(1.55), Inches(8.1), Inches(2.6)), sizes=(18, 16))
picture(s, "eq_30_synthese.png", Inches(0.55), Inches(4.20), Inches(8.2))
notes(s, "Faire reformuler avant d’afficher. Ces cinq lignes et les quatre formules "
         "vont au formulaire personnel.")

# =============================================================== 31. GRILLE
s = new()
title_of(s, "La grille d’auto-évaluation")
body_of(s, [
    (0, "Je repère série et parallèle sur un schéma inhabituel   ·  LZ 1923",
     {"size": 15, "space": 7}),
    (0, "Je réduis un circuit de 5 résistances en montrant chaque étape   ·  LZ 1923",
     {"size": 15, "space": 7}),
    (0, "J’applique les lois des nœuds et des mailles pour contrôler   ·  LZ 1924",
     {"size": 15, "space": 7}),
    (0, "Mon tableau R/U/I/P est complet, avec unités et préfixes   ·  LZ 1924",
     {"size": 15, "space": 7}),
    (0, "Je pose au moins deux contrôles et je les rends visibles   ·  LZ 1924",
     {"size": 15, "space": 7}),
    (0, "Mon schéma respecte les sept règles de dessin   ·  LZ 1952",
     {"size": 15, "space": 7}),
    (0, "Je câble et je mesure sans faute de branchement   ·  LZ 1949",
     {"size": 15, "space": 7}),
    (0, "Mon protocole est complet et ma conclusion justifie l’écart   ·  LZ 7857/7995",
     {"size": 15, "space": 12}),
    (0, "Trois colonnes : pas encore · presque · acquis. Elle est en dernière page "
        "de ta fiche.", {"nobullet": True, "size": 16, "bold": True, "color": RED}),
], box=(Inches(0.55), Inches(1.50), Inches(8.25), Inches(4.25)))
notes(s, "Afficher la grille au moment de lancer les exercices, pas à la fin : "
         "l’élève doit savoir dès le départ sur quoi il sera jugé. "
         "Elle est identique, mot pour mot, aux critères de la diapositive 29 et à "
         "la dernière page de la fiche. La faire remplir AVANT de rendre le travail, "
         "puis comparer avec la correction : l’écart est l’information la plus utile.")

# =============================================================== 32. EXERCICES
s = new()
title_of(s, "À vous : fiche 150 EX")
body_of(s, [
    (0, "Exercices 1 à 5 : rappels, reconnaître, réduire, calculer, contrôler",
     {"space": 12}),
    (0, "Exercice 6 : redessiner un schéma au propre", {"space": 12}),
    (0, "Exercice 7 : le protocole de mesure, à remplir pendant le TP",
     {"space": 12}),
    (0, "En dernière page : la grille d’auto-évaluation. Remplis-la honnêtement, "
        "elle est pour toi.", {"space": 12, "bold": True}),
], box=(Inches(0.6), Inches(1.80), Inches(8.1), Inches(3.4)))
notes(s, "Les exercices 1 à 5 se font en périodes 10-11, le 6 et le 7 en 12-13. "
         "Ramasser la grille d’auto-évaluation avec le protocole : l’écart entre "
         "l’auto-évaluation et la correction est une information précieuse.")

import os
os.makedirs("out", exist_ok=True)
prs.save(OUT)
print("saved", OUT)
