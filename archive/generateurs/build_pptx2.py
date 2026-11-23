# -*- coding: utf-8 -*-
"""220 — Courbe caractéristique, marche à vide et court-circuit (périodes 16-17)."""
from deck_helpers import *          # prs, new(), title_of(), body_of(), picture(), notes()…

OUT = "out/220 Courbe caractéristique, marche à vide et court-circuit.pptx"

# =============================================================== 1. TITRE
s = new("title")
title_of(s, "Courbe caractéristique,\nmarche à vide et court-circuit", 30)
sp = s.placeholders[1].text_frame
sp.clear()
fill(sp.paragraphs[0], "El Dim1 – Notions de base · périodes 16-17", 20, NAVY)
textbox(s, Inches(0.75), Inches(5.22), Inches(5.0), Inches(0.4),
        [("Version : 08.2026 / 1.0", 11, GREY, False)])
notes(s, "Suite directe du chapitre « La source réelle et en charge ». "
         "Objectifs LZ 3850, LZ 3855, LZ 5580.")

# =============================================================== 2. OBJECTIFS
s = new()
title_of(s, "Ce que tu sauras faire à la fin")
body_of(s, [
    (0, "Relever une caractéristique point par point et la tracer", {"space": 10}),
    (0, "Décrire les deux régimes limites : marche à vide et court-circuit", {"space": 10}),
    (0, "Tracer la droite d’une source à partir de ces deux seuls points", {"space": 10}),
    (0, "Trouver le point de fonctionnement à l’intersection de deux caractéristiques",
     {"space": 10}),
    (0, "Exploiter la caractéristique d’une charge non linéaire (lampe)", {"space": 10}),
], box=(Inches(0.51), Inches(1.48), Inches(8.33), Inches(3.3)))
textbox(s, Inches(0.51), Inches(4.95), Inches(8.33), Inches(0.5),
        [("Objectifs évaluateurs : LZ 3850 · LZ 3855 · LZ 5580", 15, GREY, True)])
notes(s, "Annoncer que ce chapitre ne réexplique pas la source réelle : il l’exploite. "
         "Le nouveau, c’est le tracé, les deux régimes limites et le point de fonctionnement.")

# =============================================================== 3. RAPPEL ACTIF
s = new()
title_of(s, "Cinq minutes de rappel — sans les notes")
body_of(s, [
    (0, "Une source réelle, c’est quel modèle ? Fais le schéma en symboles CEI.",
     {"space": 20, "size": 20}),
    (0, "Écris la relation entre U, U_{0}, R_{i} et I.", {"space": 20, "size": 20}),
    (0, "Une source débite plus de courant : sa tension de sortie monte ou descend ? "
        "Pourquoi ?", {"space": 20, "size": 20}),
], box=(Inches(0.65), Inches(1.75), Inches(8.0), Inches(3.6)))
notes(s, "5 minutes, cahier fermé, réponses écrites individuellement. La récupération "
         "en mémoire vaut bien mieux qu’un rappel magistral. Passer dans les rangs pour "
         "repérer qui a perdu le fil avant d’attaquer la suite.")

# =============================================================== 4. CORRIGE RAPPEL
s = new()
title_of(s, "Rappel — les réponses")
picture(s, "02_source_reelle.png", Inches(0.55), Inches(1.45), Inches(4.75), Inches(3.1))
body_of(s, [
    (0, "Source idéale U_{0} en série avec R_{i}", {"size": 17, "space": 12}),
    (0, "U = U_{0} − R_{i} · I", {"size": 22, "bold": True, "space": 12}),
    (0, "La tension descend : plus I est grand, plus la chute interne R_{i} · I est grande.",
     {"size": 16, "color": RED, "bold": True}),
], box=(Inches(5.55), Inches(1.90), Inches(3.25), Inches(3.2)))
notes(s, "Corriger vite, sans reprendre tout le chapitre. Si plus d’un tiers de la classe "
         "sèche sur la relation, refaire l’exemple résolu du chapitre précédent avant "
         "de continuer.")

# =============================================================== 5. RELEVE
s = new()
title_of(s, "Relever une caractéristique")
picture(s, "12_releve.png", Inches(0.7), Inches(1.40), Inches(7.7), Inches(2.95))
body_of(s, [
    (0, "Le voltmètre AUX BORNES, l’ampèremètre EN SÉRIE avec la charge",
     {"size": 16, "space": 6}),
    (0, "On déplace la charge variable pas à pas et on note un couple (I ; U) à chaque fois",
     {"size": 16, "space": 6}),
    (0, "Chaque couple donne un point du graphique", {"size": 16, "bold": True}),
], box=(Inches(0.51), Inches(4.50), Inches(8.33), Inches(1.30)))
notes(s, "C’est le montage du chapitre précédent, mais l’objectif change : on ne cherche "
         "plus deux points pour calculer Rᵢ, on relève toute la courbe. "
         "Insister sur l’ordre : régler, attendre la stabilisation, puis lire les DEUX "
         "appareils en même temps.")

# =============================================================== 6. TABLEAU → GRAPHIQUE
s = new()
title_of(s, "Du tableau de mesures au graphique")
body_of(s, [
    (0, "I [A] :   0      0,5     1,0     1,5     2,0", {"nobullet": True, "size": 17,
                                                          "space": 4}),
    (0, "U [V] :  12     10       8        6        4", {"nobullet": True, "size": 17}),
], box=(Inches(0.70), Inches(1.32), Inches(8.0), Inches(0.72)))
picture(s, "18_nuage.png", Inches(1.15), Inches(2.14), Inches(7.0), Inches(3.62))
notes(s, "Faire porter les cinq points au tableau par un élève. Le fait qu’ils soient "
         "alignés n’est pas évident a priori : c’est un résultat expérimental, "
         "conséquence de U = U₀ − Rᵢ·I qui est une équation du premier degré.")

# =============================================================== 7. MARCHE A VIDE
s = new()
title_of(s, "Le premier régime limite : la marche à vide")
picture(s, "10_marche_a_vide.png", Inches(0.65), Inches(1.38), Inches(8.05), Inches(2.85))
body_of(s, [
    (0, "Rien n’est branché, ou l’interrupteur est ouvert : la charge est infinie",
     {"size": 16, "space": 5}),
    (0, "I = 0 A  →  aucune chute interne  →  U = U_{0}", {"size": 18, "bold": True,
                                                           "space": 5}),
    (0, "La puissance fournie est nulle : la source ne débite rien", {"size": 16}),
], box=(Inches(0.51), Inches(4.35), Inches(8.33), Inches(1.45)))
notes(s, "Vocabulaire allemand courant en atelier : Leerlauf. "
         "C’est la seule situation où le voltmètre lit vraiment U₀ — d’où l’importance "
         "de débrancher la charge pour mesurer la tension à vide.")

# =============================================================== 8. COURT-CIRCUIT
s = new()
title_of(s, "Le second régime limite : le court-circuit")
picture(s, "11_court_circuit.png", Inches(0.65), Inches(1.38), Inches(8.05), Inches(2.85))
body_of(s, [
    (0, "Les deux bornes sont reliées par une résistance nulle : R = 0 Ω",
     {"size": 16, "space": 5}),
    (0, "U = 0 V  →  I = I_{cc} = U_{0} / R_{i}, le courant maximal possible",
     {"size": 18, "bold": True, "color": RED, "space": 5}),
    (0, "La puissance dans la charge est nulle aussi : tout est dissipé dans R_{i}",
     {"size": 16}),
], box=(Inches(0.51), Inches(4.35), Inches(8.33), Inches(1.45)))
notes(s, "Kurzschluss. Un essai de court-circuit ne se fait que sur une source prévue "
         "pour, et brièvement : sur une batterie, c’est un accident, pas une mesure. "
         "Faire remarquer le paradoxe : les deux régimes limites donnent tous les deux "
         "une puissance nulle dans la charge. On y revient à la diapositive 17.")

# =============================================================== 9. DEUX POINTS
s = new()
title_of(s, "Deux points suffisent")
picture(s, "13_deux_points.png", Inches(0.45), Inches(1.45), Inches(5.30), Inches(4.3))
body_of(s, [
    (0, "La caractéristique est une droite", {"size": 16, "bold": True, "space": 12}),
    (0, "Deux points définissent une droite", {"size": 16, "space": 12}),
    (0, "Et les deux plus faciles à obtenir sont les régimes limites :",
     {"size": 15, "space": 8}),
    (1, "à vide : (0 A ; U_{0})", {"size": 15, "space": 6}),
    (1, "en court-circuit : (I_{cc} ; 0 V)", {"size": 15}),
], box=(Inches(5.90), Inches(1.70), Inches(2.90), Inches(3.9)))
notes(s, "Méthode de tracé la plus rapide : placer U₀ sur l’axe vertical, Icc sur l’axe "
         "horizontal, tirer la règle. Aucun calcul intermédiaire.")

# =============================================================== 10. DEUX VOIES POUR Ri
s = new()
title_of(s, "Deux façons d’obtenir R_{i}")
body_of(s, [
    (0, "À partir des deux régimes limites :", {"size": 18, "bold": True, "space": 6}),
    (0, "R_{i} = U_{0} / I_{cc}", {"nobullet": True, "size": 26, "space": 18,
                                   "color": BLUE, "bold": True}),
    (0, "À partir de deux points quelconques de la droite :",
     {"size": 18, "bold": True, "space": 6}),
    (0, "R_{i} = ΔU / ΔI", {"nobullet": True, "size": 26, "space": 18,
                            "color": BLUE, "bold": True}),
    (0, "Les deux donnent le même résultat : c’est la même pente.",
     {"nobullet": True, "size": 17, "bold": True, "color": RED}),
], box=(Inches(0.9), Inches(1.70), Inches(7.6), Inches(3.9)))
notes(s, "La deuxième formule vient du chapitre précédent. La première est nouvelle et "
         "plus rapide quand on dispose des deux régimes limites. "
         "Bon réflexe de contrôle : calculer Rᵢ des deux façons doit donner la même valeur.")

# =============================================================== 11. EXEMPLE RESOLU
s = new()
title_of(s, "Exemple résolu")
body_of(s, [
    (0, "Sur une alimentation on mesure : à vide 12 V, en court-circuit 3 A.",
     {"nobullet": True, "bold": True, "space": 12, "size": 19}),
    (0, "1.  R_{i} = U_{0} / I_{cc} = 12 / 3 = 4 Ω",
     {"nobullet": True, "space": 10, "size": 19}),
    (0, "2.  Droite : de (0 A ; 12 V) à (3 A ; 0 V)",
     {"nobullet": True, "space": 10, "size": 19}),
    (0, "3.  Tension pour I = 1,5 A : U = 12 − 4 · 1,5 = 6 V",
     {"nobullet": True, "space": 14, "size": 19}),
    (0, "Contrôle sur le graphique : à 1,5 A on lit bien 6 V ✓",
     {"nobullet": True, "bold": True, "color": BLUE, "size": 18}),
], box=(Inches(0.7), Inches(1.60), Inches(8.0), Inches(4.0)))
notes(s, "Dérouler au tableau. Insister sur le contrôle final : le calcul et la lecture "
         "graphique doivent concorder — c’est ce qui permet à l’élève de se corriger seul.")

# =============================================================== 12. A TOI
s = new()
title_of(s, "À toi de compléter")
body_of(s, [
    (0, "Une autre alimentation donne : à vide 24 V, en court-circuit 8 A.",
     {"nobullet": True, "bold": True, "space": 16, "size": 19}),
    (0, "1.  R_{i} = ……… Ω", {"nobullet": True, "space": 12, "size": 19}),
    (0, "2.  U pour I = 2 A : ……… V", {"nobullet": True, "space": 12, "size": 19}),
    (0, "3.  U pour I = 6 A : ……… V", {"nobullet": True, "space": 16, "size": 19}),
    (0, "Sans calculer : à quel courant la tension vaut-elle exactement 12 V ?",
     {"nobullet": True, "bold": True, "color": RED, "size": 18}),
], box=(Inches(0.7), Inches(1.60), Inches(8.0), Inches(4.0)))
notes(s, "3 minutes en binôme.\n"
         "Corrigé : Rᵢ = 24 / 8 = 3 Ω ; U(2 A) = 24 − 6 = 18 V ; U(6 A) = 24 − 18 = 6 V.\n"
         "Dernière question : à la moitié de Icc, soit 4 A, la tension vaut la moitié de U₀. "
         "C’est une lecture directe sur la droite, sans calcul. FIN DE LA 1re PÉRIODE.")

# =============================================================== 13. RAPPEL ECLAIR
s = new()
title_of(s, "Rappel éclair")
body_of(s, [
    (0, "Que vaut le courant en marche à vide ? Et la tension ?",
     {"space": 22, "size": 21}),
    (0, "Que vaut la tension en court-circuit ? Et le courant ?",
     {"space": 22, "size": 21}),
    (0, "Comment obtient-on R_{i} à partir de ces deux régimes ?",
     {"space": 22, "size": 21}),
], box=(Inches(0.7), Inches(1.90), Inches(8.0), Inches(3.4)))
notes(s, "2 minutes, à l’oral cette fois, en interrogeant nominativement. "
         "Enchaîner immédiatement sur la charge.")

# =============================================================== 14. POINT DE FONCTIONNEMENT
s = new()
title_of(s, "La charge aussi a sa caractéristique")
picture(s, "14_point_fonctionnement.png", Inches(0.45), Inches(1.45), Inches(5.30), Inches(4.3))
body_of(s, [
    (0, "Une résistance suit U = R · I :", {"size": 16, "space": 4}),
    (1, "une droite issue de l’origine", {"size": 16, "space": 16}),
    (0, "Les deux droites se croisent en un seul point :", {"size": 16, "space": 4}),
    (1, "le point de fonctionnement", {"size": 16, "bold": True, "color": RED,
                                       "space": 16}),
    (0, "Le seul couple (I ; U) qui convient aux deux à la fois.",
     {"size": 15, "nobullet": True, "italic": True}),
], box=(Inches(5.90), Inches(1.70), Inches(2.90), Inches(3.9)))
notes(s, "Idée clé du chapitre : la source impose une relation, la charge en impose une "
         "autre, et le circuit ne peut vivre qu’à l’endroit où les deux sont satisfaites. "
         "Faire varier R à l’oral : si R augmente, la droite de charge se redresse et le "
         "point remonte vers la marche à vide.")

# =============================================================== 15. VERIFICATION
s = new()
title_of(s, "Le graphique et le calcul disent la même chose")
body_of(s, [
    (0, "Lecture graphique : I = 1 A et U = 8 V",
     {"nobullet": True, "size": 19, "space": 14, "bold": True}),
    (0, "Par le calcul, circuit série :", {"nobullet": True, "size": 18, "space": 8}),
    (0, "I = U_{0} / (R_{i} + R) = 12 / (4 + 8) = 1 A",
     {"nobullet": True, "size": 19, "space": 8, "color": BLUE, "bold": True}),
    (0, "U = R · I = 8 · 1 = 8 V",
     {"nobullet": True, "size": 19, "space": 16, "color": BLUE, "bold": True}),
    (0, "Alors pourquoi tracer ? Parce que le calcul ne marche que si la charge est "
        "une vraie résistance.", {"nobullet": True, "size": 17, "bold": True,
                                  "color": RED}),
], box=(Inches(0.7), Inches(1.60), Inches(8.0), Inches(4.0)))
notes(s, "Question à poser avant d’afficher la dernière ligne : « si le calcul suffit, "
         "à quoi sert le graphique ? ». Laisser chercher, puis enchaîner sur la lampe.")

# =============================================================== 16. LAMPE
s = new()
title_of(s, "Quand le graphique devient indispensable")
picture(s, "15_lampe.png", Inches(0.45), Inches(1.45), Inches(5.30), Inches(4.3))
body_of(s, [
    (0, "Le filament chauffe, sa résistance augmente : la caractéristique se courbe",
     {"size": 15, "space": 12}),
    (0, "Plus de R constante à mettre dans la formule", {"size": 16, "space": 12}),
    (0, "L’intersection donne quand même le point de fonctionnement",
     {"size": 16, "bold": True, "color": RED}),
], box=(Inches(5.90), Inches(1.80), Inches(2.90), Inches(3.7)))
notes(s, "À froid, une lampe 12 V a une résistance environ dix fois plus faible qu’à "
         "chaud : c’est pourquoi elle grille souvent à l’allumage. "
         "Ici la méthode graphique est la seule praticable en 1re année.")

# =============================================================== 17. PUISSANCE
s = new()
title_of(s, "La puissance dans la charge")
picture(s, "16_puissance.png", Inches(0.45), Inches(1.45), Inches(5.30), Inches(4.3))
body_of(s, [
    (0, "P = U · I : c’est l’aire du rectangle sous le point",
     {"size": 15, "space": 12}),
    (0, "À vide comme en court-circuit, l’aire est nulle", {"size": 15, "space": 12}),
    (0, "Le maximum est entre les deux, quand R = R_{i}",
     {"size": 15, "bold": True, "color": RED}),
], box=(Inches(5.90), Inches(1.90), Inches(2.90), Inches(3.5)))
notes(s, "Réponse au paradoxe posé à la diapositive 8. Ne pas démontrer : faire constater "
         "sur les trois rectangles. Notion reprise plus tard sous le nom d’adaptation. "
         "Attention : au maximum de puissance, la moitié est perdue dans Rᵢ — "
         "ce n’est donc pas le réglage le plus économique.")

# =============================================================== 18. PIEGES
s = new()
title_of(s, "Les quatre pièges classiques")
body_of(s, [
    (0, "Lire U_{0} au voltmètre sans avoir débranché la charge",
     {"space": 14, "size": 18}),
    (0, "Tracer la droite de charge en partant de U_{0} au lieu de l’origine",
     {"space": 14, "size": 18}),
    (0, "Chercher le point de fonctionnement par le calcul sur une charge non linéaire",
     {"space": 14, "size": 18}),
    (0, "Confondre la pente de la source (négative) et celle de la charge (positive)",
     {"size": 18}),
], box=(Inches(0.6), Inches(1.70), Inches(8.1), Inches(3.8)))
notes(s, "Les faire noter dans le formulaire personnel. Le deuxième piège est le plus "
         "fréquent au TE.")

# =============================================================== 19. SYNTHESE
s = new()
title_of(s, "L’essentiel en cinq lignes")
body_of(s, [
    (0, "Marche à vide : I = 0, U = U_{0}, P = 0", {"space": 13}),
    (0, "Court-circuit : U = 0, I = I_{cc} = U_{0} / R_{i}, P = 0", {"space": 13}),
    (0, "Ces deux points suffisent à tracer la droite de la source", {"space": 13}),
    (0, "R_{i} = U_{0} / I_{cc} = ΔU / ΔI", {"space": 13, "bold": True}),
    (0, "Point de fonctionnement = intersection des deux caractéristiques", {"space": 13}),
], box=(Inches(0.6), Inches(1.75), Inches(8.1), Inches(3.6)), sizes=(19, 17))
notes(s, "Faire reformuler avant d’afficher. Ces cinq lignes vont au formulaire, "
         "à la suite de celles du chapitre précédent.")

# =============================================================== 20. EXERCICES
s = new()
title_of(s, "À vous : fiche 230 EX")
body_of(s, [
    (0, "Six exercices, du vocabulaire au diagnostic", {"space": 12}),
    (0, "Matériel : formulaire, calculatrice, règle", {"space": 12}),
    (0, "Les exercices 4, 5 et 6 se font sur les quadrillages fournis", {"space": 12}),
    (0, "L’exercice 6 porte sur une lampe : lecture graphique obligatoire",
     {"space": 12}),
], box=(Inches(0.6), Inches(1.80), Inches(8.1), Inches(3.2)))
notes(s, "Circuler et vérifier que la droite de charge part bien de l’origine à "
         "l’exercice 5. Correction projetée ou corrigé distribué.")

import os
os.makedirs("out", exist_ok=True)
prs.save(OUT)
print("saved", OUT)
