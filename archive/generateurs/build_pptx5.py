# -*- coding: utf-8 -*-
"""500 — Les appareils de mesure et leur influence (El Dim1, LZ 1951). 28 diapos.

Minutage : 1 h 30 en tout — environ 58 minutes de théorie et d'exemples résolus,
puis 30 minutes sur la fiche 510, correction comprise. Le minutage cumulé figure
dans les notes du présentateur.

Progression : l'influence des appareils d'abord (voltmètre, ampèremètre,
ohmmètre), la précision et l'écart seulement à la fin. Chaque exemple se termine
par son contrôle de Kirchhoff, et toute grandeur affichée porte son unité.
"""
from deck_helpers import *

OUT = "out/500 Appareils de mesure et influence.pptx"
VERT = RGBColor(0x26, 0x66, 0x3F)


def eq(slide, nom, x, y, w):
    return picture(slide, nom, x, y, w)


# =============================================================== 1. TITRE
s = new("title")
title_of(s, "Les appareils de mesure\net leur influence", 34)
sp = s.placeholders[1].text_frame
sp.clear()
fill(sp.paragraphs[0], "El Dim1 – Intelec · 2 périodes · semaine 5", 19, NAVY)
textbox(s, Inches(0.75), Inches(5.22), Inches(5.6), Inches(0.4),
        [("Version : 09.2026 / 2.4  ·  durée 1 h 30  ·  LZ 1951", 11, GREY, False)])
notes(s, "0 min. 58 minutes de théorie avec quatre exemples résolus, puis "
         "30 minutes sur la fiche 510, correction comprise ; les élèves "
         "terminent la fiche à la maison. La précision et l'écart sont "
         "traités en fin de leçon, une fois l'influence acquise.")

# =============================================================== 2. CE QUE L'ON SAIT
s = new()
title_of(s, "Ce que l’on sait aujourd’hui, après 5 semaines en Intelec", 26)
body_of(s, [
    (0, "Réduire un circuit mixte : série, parallèle, étape par étape",
     {"space": 10, "size": 19}),
    (0, "Poser les deux lois de Kirchhoff : nœuds et mailles",
     {"space": 10, "size": 19}),
    (0, "Brancher les appareils : ampèremètre en série, voltmètre en parallèle",
     {"space": 10, "size": 19}),
    (0, "Et au TP, on a comparé mesure et calcul… et trouvé un écart.",
     {"space": 10, "size": 19, "bold": True, "color": RED}),
], box=(Inches(0.51), Inches(1.62), Inches(8.33), Inches(3.1)))
textbox(s, Inches(0.51), Inches(4.80), Inches(8.33), Inches(0.9),
        [("Deux causes avaient été données : la tolérance des résistances et "
          "la précision de l’appareil.", 16, NAVY, True),
         ("Il en manquait une troisième — c’est le sujet du jour.", 16, RED, True)])
notes(s, "2 min. Rappel actif : faire énoncer les deux lois de Kirchhoff par la "
         "classe avant d'afficher la diapositive.")

# =============================================================== 3. OBJECTIFS
s = new()
title_of(s, "Ce que tu sauras faire à la fin")
body_of(s, [
    (0, "Dire ce qu’il y a dans un voltmètre, un ampèremètre et un ohmmètre",
     {"space": 9, "size": 18}),
    (0, "Calculer de combien un voltmètre fausse une mesure de tension",
     {"space": 9, "size": 18}),
    (0, "Calculer de combien un ampèremètre fausse une mesure de courant",
     {"space": 9, "size": 18}),
    (0, "Dire pourquoi une résistance mesurée en place se lit trop petite",
     {"space": 9, "size": 18}),
    (0, "Choisir l’appareil et le calibre, et chiffrer la précision obtenue",
     {"space": 9, "size": 18}),
], box=(Inches(0.51), Inches(1.55), Inches(8.33), Inches(3.3)))
textbox(s, Inches(0.51), Inches(4.90), Inches(8.33), Inches(0.7),
        [("Objectif évaluateur : LZ 1951", 14, GREY, True)])
notes(s, "4 min. Les cinq objectifs sont repris mot pour mot dans la grille "
         "d'auto-évaluation de la fiche 510.")

# =============================================================== 4. LA QUESTION
s = new()
title_of(s, "La question qui restait")
picture(s, "90_passerelle.png", Inches(0.45), Inches(1.40), Inches(8.4), Inches(3.15))
body_of(s, [
    (0, "L’appareil de mesure ne se contente pas de regarder : il fait partie "
        "du circuit.", {"nobullet": True, "size": 19, "bold": True, "color": RED}),
], box=(Inches(0.55), Inches(4.75), Inches(8.2), Inches(0.8)))
notes(s, "6 min. Laisser 60 secondes de silence sur la question. C'est le cœur "
         "du chapitre : la mesure perturbe ce qu'elle mesure.")

# =============================================================== 5. RÉSISTANCE INTERNE
s = new()
title_of(s, "Tout appareil a une résistance interne")
eq(s, "eq_05_internes.png", Inches(0.50), Inches(1.60), Inches(8.3))
textbox(s, Inches(0.55), Inches(4.35), Inches(8.2), Inches(1.1),
        [("Un appareil idéal ne prendrait rien au circuit : le voltmètre aucun "
          "courant, l’ampèremètre aucune tension.", 16, NAVY, False),
         ("Aucun appareil réel n’y arrive. Toute la question est : de combien "
          "s’en écarte-t-il ?", 16, RED, True)])
notes(s, "8 min. Poser le vocabulaire : R_V pour le voltmètre, R_A pour "
         "l'ampèremètre. Les deux idéaux sont opposés : l'infini d'un côté, "
         "le zéro de l'autre.")

# =============================================================== 6. DANS UN VOLTMÈTRE
s = new()
title_of(s, "Ce qu’il y a dans un voltmètre")
picture(s, "V1_dans_voltmetre.png", Inches(0.70), Inches(1.45), Inches(7.9), Inches(3.05))
body_of(s, [
    (0, "Entre ses deux bornes, un voltmètre est une résistance. Grande, "
        "mais finie.", {"nobullet": True, "size": 19, "bold": True}),
], box=(Inches(0.55), Inches(4.70), Inches(8.2), Inches(0.8)))
notes(s, "10 min. Insister sur le mot BORNES : ce que le circuit voit, c'est "
         "R_V entre deux bornes, rien d'autre. Le reste est de l'électronique "
         "interne dont on n'a pas besoin ici.")

# =============================================================== 7. CE QUI CHANGE
s = new()
title_of(s, "Ce qui change quand on le branche")
picture(s, "V2_avant_apres.png", Inches(0.38), Inches(1.32), Inches(8.45), Inches(3.35))
body_of(s, [
    (0, "Le courant total monte de 1,00 à 1,20 µA, et la tension mesurée tombe "
        "de 5,00 V à 4,00 V.", {"nobullet": True, "size": 18, "bold": True,
                                "color": RED}),
], box=(Inches(0.55), Inches(4.85), Inches(8.2), Inches(0.8)))
notes(s, "13 min. LA diapositive du chapitre. Faire lire les deux schémas par "
         "les élèves avant de commenter : qu'est-ce qui a changé ? Réponse "
         "attendue : une résistance de plus en parallèle sur R2, donc un groupe "
         "plus petit, donc moins de tension et plus de courant total.")

# =============================================================== 8. LE CALCUL
s = new()
title_of(s, "Le calcul, en deux étapes")
eq(s, "eq7_volt_methode.png", Inches(0.80), Inches(1.50), Inches(7.7))
textbox(s, Inches(0.55), Inches(4.62), Inches(8.2), Inches(1.0),
        [("Rien de nouveau : le voltmètre est une résistance de plus, "
          "en parallèle.", 17, NAVY, True),
         ("On réduit le groupe parallèle [Ω], puis on applique le diviseur "
          "de tension [V].", 16, GREY, False)])
notes(s, "16 min. Écrire les deux formules au tableau pendant que la "
         "diapositive est affichée. Ce sont les deux seules du bloc voltmètre.")

# =============================================================== 9. L'EXEMPLE
s = new()
title_of(s, "L’exemple en entier")
textbox(s, Inches(0.55), Inches(1.26), Inches(8.2), Inches(0.5),
        [("U = 10 V · R_{1} = R_{2} = 5 MΩ · voltmètre numérique, "
          "R_{V} = 10 MΩ", 15, NAVY, True)])
eq(s, "eq7_volt_exemple.png", Inches(0.50), Inches(1.80), Inches(8.3))
notes(s, "19 min. La dernière ligne est le contrôle : les 1,20 µA se partagent "
         "en 0,80 µA dans R2 et 0,40 µA dans le voltmètre. La loi des nœuds "
         "sert de vérification. Même avec 10 MΩ — un bon appareil — la mesure "
         "est fausse de 20 %, parce que les résistances du diviseur sont "
         "grandes.")

# =============================================================== 10. LA RÈGLE
s = new()
title_of(s, "La règle du voltmètre")
eq(s, "eq_13_regle_v.png", Inches(0.50), Inches(1.50), Inches(8.3))
body_of(s, [
    (0, "R = 10 kΩ → il faudrait R_{V} ≥ 1 MΩ : n’importe quel appareil convient",
     {"space": 8, "size": 17, "nobullet": True}),
    (0, "R = 100 kΩ → il faudrait R_{V} ≥ 10 MΩ : seul un numérique tient",
     {"space": 8, "size": 17, "nobullet": True}),
    (0, "R = 5 MΩ → il faudrait R_{V} ≥ 500 MΩ : aucun appareil ne tient, "
        "l’écart est inévitable — c’était notre exemple, et il vaut −20 %",
     {"space": 8, "size": 17, "nobullet": True, "color": RED}),
], box=(Inches(0.55), Inches(4.05), Inches(8.2), Inches(1.6)))
notes(s, "22 min. Donner l'ordre de grandeur pratique : en dessous de 10 kΩ on "
         "ne se pose pas la question ; au-dessus de 100 kΩ on la pose toujours.")

# =============================================================== 11. À TOI
s = new()
title_of(s, "À toi — 3 minutes")
body_of(s, [
    (0, "Un diviseur de deux résistances de 470 kΩ est alimenté sous 20 V.",
     {"space": 14, "size": 19, "nobullet": True}),
    (0, "① Quelle tension y a-t-il vraiment sur la résistance du bas ?",
     {"space": 12, "size": 19, "nobullet": True}),
    (0, "② Ton voltmètre a 10 MΩ. La règle R_{V} ≥ 100 · R est-elle respectée ?",
     {"space": 12, "size": 19, "nobullet": True}),
    (0, "③ Sans calculer : l’appareil affichera-t-il plus ou moins que la vraie "
        "valeur ?", {"space": 12, "size": 19, "nobullet": True}),
], box=(Inches(0.55), Inches(1.65), Inches(8.2), Inches(3.2)))
textbox(s, Inches(0.55), Inches(4.95), Inches(8.2), Inches(0.7),
        [("Réponses : 10 V · non, il faudrait 47 MΩ · moins.", 16, RED, True)])
notes(s, "24 min. Laisser chercher 2 minutes, corriger en 1 minute. La "
         "réponse ③ se donne sans calcul : un voltmètre ne peut qu'abaisser la "
         "tension qu'il mesure.")

# =============================================================== 12. DANS UN AMPÈREMÈTRE
s = new()
title_of(s, "Ce qu’il y a dans un ampèremètre")
picture(s, "A1_dans_amperemetre.png", Inches(0.70), Inches(1.55), Inches(7.9), Inches(2.75))
body_of(s, [
    (0, "Entre ses deux bornes, un ampèremètre est aussi une résistance. "
        "Petite, mais pas nulle.", {"nobullet": True, "size": 19, "bold": True}),
], box=(Inches(0.55), Inches(4.55), Inches(8.2), Inches(0.8)))
notes(s, "28 min. Symétrique du voltmètre : l'un ajoute du parallèle, l'autre "
         "du série. Les deux erreurs vont dans le même sens.")

# =============================================================== 13. CE QUI CHANGE (A)
s = new()
title_of(s, "Ce qui change quand on le branche")
picture(s, "A2_avant_apres.png", Inches(0.38), Inches(1.35), Inches(8.45), Inches(3.1))
body_of(s, [
    (0, "Le courant tombe de 55,6 à 50,0 mA, et 1,00 V sur les 10,0 V reste "
        "dans l’appareil.", {"nobullet": True, "size": 18, "bold": True,
                             "color": RED}),
], box=(Inches(0.55), Inches(4.65), Inches(8.2), Inches(0.8)))
notes(s, "30 min. Le volt perdu dans l'appareil porte un nom dans les fiches "
         "techniques : la chute de tension de l'ampèremètre, ou burden voltage.")

# =============================================================== 14. LE CALCUL (A)
s = new()
title_of(s, "Le calcul et l’exemple")
eq(s, "eq7_amp_methode.png", Inches(1.75), Inches(1.20), Inches(5.8))
eq(s, "eq7_amp_exemple.png", Inches(0.95), Inches(3.42), Inches(7.4))
notes(s, "33 min. La dernière ligne est encore un contrôle : la loi des mailles "
         "boucle à 10,0 V. Insister — 10 % d'erreur sur le courant, pour un "
         "ampèremètre de 20 Ω dans un circuit de 180 Ω.")

# =============================================================== 15. LES DEUX RÈGLES
s = new()
title_of(s, "Les deux règles, côte à côte")
eq(s, "eq7_deux_regles.png", Inches(0.85), Inches(1.45), Inches(7.6))
textbox(s, Inches(0.55), Inches(4.78), Inches(8.2), Inches(0.9),
        [("Ce sont les deux seules formules du chapitre à connaître par cœur.",
          17, NAVY, True)])
notes(s, "36 min. Les faire noter côte à côte : c'est la synthèse du chapitre. "
         "Le facteur 100 donne moins de 1 % d'erreur dans les deux cas.")

# =============================================================== 16. LE PIÈGE
s = new()
title_of(s, "Le piège mortel")
body_of(s, [
    (0, "Un ampèremètre a une résistance quasi nulle.", {"space": 13, "size": 19}),
    (0, "Branché en parallèle sur une résistance, il la court-circuite.",
     {"space": 13, "size": 19}),
    (0, "Tout le courant de la source passe alors dans l’appareil : fusible "
        "grillé, au mieux.", {"space": 13, "size": 19, "color": RED,
                              "bold": True}),
    (0, "Et un fusible, ça coûte trois francs… sauf au Shopiguet, où ça coûte "
        "trois francs et vingt minutes de queue.",
     {"space": 13, "size": 17, "color": BLUE, "nobullet": True}),
], box=(Inches(0.55), Inches(1.62), Inches(8.2), Inches(2.9)))
textbox(s, Inches(0.55), Inches(4.62), Inches(8.2), Inches(1.0),
        [("Avant chaque mise sous tension : « où est mon ampèremètre ? »",
          18, RED, True),
         ("Et sur un multimètre : la fiche est-elle encore dans la borne A ?",
          16, NAVY, False)])
notes(s, "38 min. La borne A oubliée est la cause numéro un de fusibles grillés "
         "au labo. Ils ont maintenant l'explication quantitative — et la note "
         "de frais qui va avec.")

# =============================================================== 17. DANS UN OHMMÈTRE
s = new()
title_of(s, "Ce qu’il y a dans un ohmmètre")
picture(s, "O1_dans_ohmmetre.png", Inches(0.70), Inches(1.50), Inches(7.9), Inches(3.0))
body_of(s, [
    (0, "Il n’attend pas le courant : il le fabrique. C’est pour cela que le "
        "circuit doit être hors tension.",
     {"nobullet": True, "size": 18, "bold": True, "color": RED}),
], box=(Inches(0.55), Inches(4.70), Inches(8.2), Inches(0.8)))
notes(s, "40 min. Le point clé : l'ohmmètre est le seul appareil ACTIF des "
         "trois. Toute tension extérieure fausse sa mesure, ou le détruit.")

# =============================================================== 18. LES TROIS RÈGLES
s = new()
title_of(s, "Ohmmètre — trois règles absolues")
body_of(s, [
    (0, "Circuit HORS TENSION — il injecte son propre courant",
     {"space": 9, "size": 18}),
    (0, "Composant ISOLÉ — au moins une patte dessoudée", {"space": 9, "size": 18}),
    (0, "Ne pas tenir les deux pointes entre les doigts — le corps vaut "
        "quelques dizaines de kΩ", {"space": 9, "size": 18}),
], box=(Inches(0.51), Inches(1.55), Inches(8.33), Inches(1.8)))
picture(s, "94_ohmmetre.png", Inches(0.50), Inches(3.30), Inches(8.3), Inches(2.35))
notes(s, "42 min. La troisième règle surprend toujours. Elle devient visible "
         "dès qu'on mesure une résistance de 100 kΩ ou plus.")

# =============================================================== 19. EN CIRCUIT
s = new()
title_of(s, "Mesurer sans dessouder : ce qu’on lit vraiment")
textbox(s, Inches(0.55), Inches(1.26), Inches(8.2), Inches(0.5),
        [("R = 12 kΩ, encore montée ; le reste du circuit vu par l’ohmmètre "
          "vaut 4 kΩ", 16, NAVY, True)])
eq(s, "eq7_ohm.png", Inches(0.50), Inches(1.85), Inches(8.3))
textbox(s, Inches(0.55), Inches(4.30), Inches(8.2), Inches(1.1),
        [("Une résistance mesurée en place se lit TOUJOURS trop petite.",
          17, RED, True),
         ("Encore un groupe parallèle : 12 kΩ et 4 kΩ donnent 3 kΩ.",
          16, GREY, False)])
notes(s, "44 min. Faire remarquer la constante du chapitre : les trois "
         "appareils se ramènent tous à un groupe série ou parallèle.")

# =============================================================== 20. ANALOGIQUE / NUMÉRIQUE
s = new()
title_of(s, "Analogique ou numérique, sur la même mesure", 28)
picture(s, "AN1_comparaison.png", Inches(0.60), Inches(1.40), Inches(8.15), Inches(3.1))
textbox(s, Inches(0.51), Inches(4.66), Inches(8.33), Inches(1.3),
        [("Influence : R_{V} = S · U_{calibre} = 200 kΩ pour l’analogique, "
          "contre 10 MΩ fixes pour le Fluke 87.", 16, NAVY, True),
         ("Précision sur 4,00 V : ± 0,15 V (± 3,75 %) contre ± 0,003 V "
          "(± 0,075 %).", 16, NAVY, True),
         ("Le numérique gagne deux fois — mais aucun des deux ne supprime "
          "l’influence.", 16, RED, True)])
notes(s, "46 min. Sur un analogique, R_V CHANGE avec le calibre (S · calibre) ; "
         "sur un numérique elle est fixe. Ne pas le présenter comme meilleur "
         "en tout : pour régler un potentiomètre au maximum, l'aiguille bat "
         "le chiffre.")

# =============================================================== 21. L'ÉCART
s = new()
title_of(s, "Chiffrer ce que l’appareil a faussé : l’écart")
eq(s, "eq7_ecart.png", Inches(0.72), Inches(1.45), Inches(7.8))
textbox(s, Inches(0.55), Inches(4.72), Inches(8.2), Inches(1.0),
        [("Voilà la troisième cause d’écart, celle qui manquait au TP.",
          17, RED, True),
         ("Elle est calculable : ce n’est pas une incertitude, c’est une "
          "erreur systématique, toujours négative.", 16, NAVY, False)])
notes(s, "49 min. Différence à marquer : la tolérance des résistances est "
         "aléatoire, l'effet de charge est systématique et toujours dans le "
         "même sens. Les deux valeurs affichées sont celles des deux exemples "
         "du jour : −20 % au voltmètre, −10 % à l'ampèremètre.")

# =============================================================== 22. LA FICHE TECHNIQUE
s = new()
title_of(s, "Lire la fiche technique : le Fluke 87 en tension continue", 27)
picture(s, "F1_fiche_fluke87.png", Inches(0.50), Inches(1.32), Inches(8.3), Inches(3.45))
textbox(s, Inches(0.51), Inches(4.98), Inches(8.33), Inches(0.9),
        [("Trois mots à retenir : l’ÉCHELLE qu’on choisit, la RÉSOLUTION "
          "qu’elle impose, la PRÉCISION qui en découle.", 16, NAVY, True),
         ("Source : Fluke, Users Manual 80 Series V, Table 12 — colonne "
          "Model 87.", 13, GREY, False)])
notes(s, "52 min. C'est la page que les élèves retrouveront au labo. Leur "
         "faire lire une ligne à voix haute : sur l'échelle 6,000 V, la "
         "résolution est de 0,001 V, donc le « + 1 » vaut 1 mV. Le mV continu "
         "est moins précis que le V continu : 0,1 % au lieu de 0,05 %.")

# =============================================================== 23. EXEMPLE DE CALCUL
s = new()
title_of(s, "Exemple de calcul de précision")
eq(s, "eq7_prec_fluke.png", Inches(1.50), Inches(1.30), Inches(7.0))
textbox(s, Inches(0.51), Inches(4.94), Inches(8.33), Inches(0.9),
        [("Le pourcentage suit la LECTURE, le « + 1 » suit l’ÉCHELLE — ici "
          "c’est lui qui pèse le plus.", 16, RED, True),
         ("On arrondit toujours la précision vers le haut : 14,78 mV devient "
          "15 mV.", 15, NAVY, False)])
notes(s, "55 min. L'exemple de la fiche ETML, repris tel quel. Faire refaire "
         "le même calcul sur l'échelle 6,000 V — impossible ici, 9,56 V n'y "
         "entre pas : c'est bien l'échelle 60,00 V la plus petite qui "
         "contienne la mesure.")

# =============================================================== 24. PRÉCISION ≠ INFLUENCE
s = new()
title_of(s, "Précision n’est pas influence")
eq(s, "eq7_synthese.png", Inches(1.35), Inches(1.35), Inches(7.3))
textbox(s, Inches(0.51), Inches(4.92), Inches(8.33), Inches(1.0),
        [("La précision, c’est l’erreur de l’affichage. L’influence, c’est "
          "l’erreur du branchement.", 17, NAVY, True),
         ("Un appareil très précis branché au mauvais endroit reste très "
          "faux — et aucune fiche technique ne le dit.", 16, RED, True)])
notes(s, "57 min. LA conclusion du chapitre, et la fin de la théorie. Le "
         "Fluke 87 donne sa mesure au millivolt près ; il ne dit pas que "
         "cette mesure n'est plus celle du circuit d'origine. Seule la règle "
         "R_V ≥ 100 · R, vérifiée AVANT de brancher, protège de ça.")

# =============================================================== 25. LES RÉFLEXES
s = new()
title_of(s, "Les cinq réflexes avant de mesurer")
body_of(s, [
    (0, "① Quelle grandeur ? Tension, courant ou résistance",
     {"space": 10, "size": 18, "nobullet": True}),
    (0, "② Où est ma fiche ? Borne V/Ω ou borne A",
     {"space": 10, "size": 18, "nobullet": True}),
    (0, "③ En série ou en parallèle ?", {"space": 10, "size": 18,
                                          "nobullet": True}),
    (0, "④ Le plus grand calibre d’abord", {"space": 10, "size": 18,
                                             "nobullet": True}),
    (0, "⑤ Mon appareil va-t-il fausser la mesure ? R_{V} ≥ 100 · R [Ω], "
        "R_{A} ≤ R/100 [Ω]", {"space": 10, "size": 18, "nobullet": True}),
], box=(Inches(0.51), Inches(1.60), Inches(8.33), Inches(3.4)))
textbox(s, Inches(0.51), Inches(5.05), Inches(8.33), Inches(0.6),
        [("Le cinquième est le nouveau. Les quatre premiers, tu les avais déjà.",
          15, GREY, True)])
notes(s, "57 min. Les faire recopier : c'est la liste à avoir en tête à chaque "
         "TP jusqu'à la fin de l'apprentissage.")

# =============================================================== 26. FORMULAIRE
s = new()
title_of(s, "Le formulaire du chapitre")
eq(s, "eq7_formulaire.png", Inches(1.70), Inches(1.28), Inches(6.6))
notes(s, "59 min. Neuf formules, dont aucune n'est nouvelle sur le fond : ce "
         "sont des groupes série et parallèle appliqués aux appareils de "
         "mesure. Toutes les grandeurs portent leur unité.")

# =============================================================== 27. AU TRAVAIL
s = new()
title_of(s, "Au travail — fiche 510, six exercices, 45 min")
body_of(s, [
    (0, "① Placer les appareils — 8 min          ④ La chute de tension de "
        "l’ampèremètre — 10 min", {"space": 12, "size": 17, "nobullet": True}),
    (0, "② Pourquoi le numérique ? — 5 min          ⑤ L’ohmmètre sur un circuit "
        "monté — 5 min", {"space": 12, "size": 17, "nobullet": True}),
    (0, "③ L’effet de charge d’un voltmètre numérique — 12 min          "
        "⑥ Précision et calibre — 5 min",
     {"space": 12, "size": 17, "nobullet": True}),
], box=(Inches(0.51), Inches(1.75), Inches(8.33), Inches(2.6)))
textbox(s, Inches(0.51), Inches(4.30), Inches(8.33), Inches(1.4),
        [("Les 30 premières minutes se font ici ; le reste se termine à la "
          "maison.", 17, RED, True),
         ("Tout résultat porte son unité entre crochets : 24,0 [mA], 9,00 [V], "
          "2,00 [MΩ].", 16, NAVY, True),
         ("Correction des exercices 1 à 3 dans les 5 dernières minutes.",
          15, GREY, False)])
notes(s, "60 min. 30 minutes de travail surveillé, 5 minutes de correction sur "
         "les trois premiers. Circuler et repérer ceux qui oublient de calculer "
         "la valeur vraie avant l'écart, et ceux qui oublient les crochets.")

# =============================================================== 28. AUTO-ÉVALUATION
s = new()
title_of(s, "Où j’en suis")
body_of(s, [
    (0, "La grille est en dernière page de la fiche. Remplis-la avant de "
        "regarder le corrigé.", {"space": 14, "size": 19, "nobullet": True}),
    (0, "Onze critères, ceux de la diapositive des objectifs, plus ceux sur la "
        "présentation des calculs, les unités entre crochets et les schémas.",
     {"space": 14, "size": 19, "nobullet": True}),
    (0, "L’écart entre ce que tu coches et ce que donne la correction est "
        "l’information la plus utile des deux.",
     {"space": 14, "size": 19, "nobullet": True, "color": BLUE}),
], box=(Inches(0.55), Inches(1.75), Inches(8.2), Inches(3.2)))
notes(s, "88 min. Ramasser la grille avec les exercices. L'auto-évaluation "
         "n'est pas notée : elle sert à repérer les élèves qui se surestiment.")

import os
vides = nettoyer()
os.makedirs("out", exist_ok=True)
prs.save(OUT)
print("saved", OUT, "|", len(prs.slides._sldIdLst), "diapositives",
      "|", vides, "réserves vides supprimées")
