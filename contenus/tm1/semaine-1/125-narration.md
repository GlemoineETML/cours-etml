# 125 Portes logiques et tables de vérité – texte de la voix off

Ton : tonique, énergique, tutoiement. Chaque réplique commence au temps indiqué (secondes depuis le début de la vidéo, 5 min 58) et doit être finie avant la suivante. La synthèse lit « = » comme « égale » et « 74HC02 » comme « septante-quatre H C zéro deux » (moteur/voix.py).

| Début | Scène | Texte |
|---|---|---|
| 0,5 | Introduction | Des 0 et des 1, sept portes, et une voiture qui ne démarre que si tout est en ordre. C'est parti ! |
| 8,5 | Carte 1 | Premier défi : la voiture démarre seulement si la ceinture est bouclée, le sélecteur sur P et le frein enfoncé. Comment un circuit décide-t-il d'allumer le voyant ? |
| 19,5 | Voiture | Chaque capteur répond par oui ou par non : 1 ou 0. Attention : la ceinture A et le frein C sont actifs à zéro ! |
| 27,0 | Voiture | Ceinture bouclée : A passe à zéro. |
| 30,5 | Voiture | Sélecteur sur P : B = 1. Le voyant reste éteint : pas de frein. |
| 36,5 | Voiture | Frein enfoncé : C = 0. Tout est bon : S = 1, le voyant s'allume ! |
| 43,0 | Voiture | On relâche le frein : le voyant s'éteint. |
| 47,5 | Voiture | Au garage, le mécanicien ne boucle pas sa ceinture : A = 1. |
| 52,5 | Voiture | Mode service : D = 1. Ni ceinture, ni frein, et pourtant S = 1 ! |
| 59,0 | Voiture | Mais le sélecteur reste obligatoire : hors de P, S retombe à zéro. |
| 65,0 | Voiture | En portes : une NON-OU pour A et C, une OU avec D, puis une ET avec B. |
| 70,0 | Voiture | Sélecteur sur P : S = 1. Et la barre sur A plus C ? C'est la porte NON-OU ! |
| 76,5 | Carte 2 | Deuxième défi : sans le mode service, il reste trois capteurs. Comment être sûr de n'oublier aucun cas ? |
| 87,5 | Table | Une table de vérité, c'est toutes les combinaisons des entrées. Une colonne par entrée, du poids fort au poids faible, puis la sortie. |
| 96,0 | Table | Trois entrées, donc deux puissance trois : huit lignes. On compte en binaire, de zéro zéro zéro à un un un. |
| 104,0 | Table | Ligne quatre : un zéro zéro. C vaut quatre, B vaut deux, A vaut un. |
| 112,0 | Table | Vérifie le rythme : A change à chaque ligne, B toutes les deux lignes, C toutes les quatre. |
| 121,0 | Table | Exemple : le démarrage sans le mode service. Ligne par ligne, le cahier des charges autorise-t-il le démarrage ? |
| 132,6 | Table | Une seule ligne donne S = 1. D'où S égale C barre, B, A barre. |
| 140,5 | Carte 3 | Troisième défi : l'analyseur logique affiche A, B et S. Comment relier l'écran à la table de vérité ? |
| 151,5 | Chronogramme | Le temps avance vers la droite. Chaque intervalle où rien ne change, c'est une ligne de la table. |
| 158,0 | Chronogramme | Intervalle un : A et B à zéro, S = 0. |
| 162,0 | Chronogramme | Intervalle deux : A = 1, B = 0. Toujours S = 0. |
| 170,0 | Chronogramme | Intervalle quatre : A et B à 1, S = 1 ! |
| 174,0 | Chronogramme | Intervalle cinq : la même combinaison qu'au deux. Même ligne, même S. |
| 182,0 | Chronogramme | Intervalle sept : encore A et B à 1, et S = 1. |
| 190,0 | Chronogramme | Le chronogramme parcourt la table dans l'ordre où les combinaisons arrivent. |
| 194,5 | Carte 4 | Quatrième défi : sept portes à reconnaître, par leur symbole, leur table ou leur équation. |
| 205,5 | Sept portes | Sept portes, c'est parti ! |
| 208,2 | Sept portes | NON, l'inverseur : une seule entrée, et la sortie est l'inverse. Le petit cercle, c'est l'inversion. |
| 218,2 | Sept portes | ET : S = 1 seulement si A et B valent 1. |
| 228,2 | Sept portes | OU : S = 1 dès qu'une entrée vaut 1. Au moins une ! |
| 238,2 | Sept portes | NON-ET : le ET avec un cercle. S = 0 seulement si les deux entrées valent 1. |
| 248,2 | Sept portes | NON-OU : le OU avec un cercle. S = 1 seulement si les deux entrées valent zéro. C'est la porte de la ceinture et du frein ! |
| 258,2 | Sept portes | OU exclusif : S = 1 quand les entrées sont différentes. |
| 268,2 | Sept portes | NON-OU exclusif : S = 1 quand les entrées sont égales. Un détecteur d'égalité ! |
| 279,5 | Carte 5 | Dernier défi : tu câbles le démarrage sur trois CI. Sur quelles broches ? Et où est le piège ? |
| 290,5 | Circuit intégré | Voici le 74HC02 : quatre portes NON-OU. |
| 296,0 | Circuit intégré | La ceinture A sur la broche deux. |
| 300,0 | Circuit intégré | Le frein C sur la broche trois. |
| 304,0 | Circuit intégré | Le piège : la sortie est la broche 1, avant les entrées ! Elle part vers le 74HC32. |
| 312,0 | Circuit intégré | Broche quatorze au plus cinq volts… |
| 315,5 | Circuit intégré | … et broche sept à la masse. Inverser grille le CI ! |
| 319,5 | Circuit intégré | Les entrées inutilisées vont à la masse : une entrée CMOS ne reste jamais en l'air. |
| 327,0 | Circuit intégré | Essai : la sortie vaut 1 seulement si A et C valent zéro. Ceinture bouclée, frein enfoncé ! |
| 336,0 | Circuit intégré | Le 74HC32 et le 74HC08 ? Sortie sur la broche trois ! |
| 343,5 | Récapitulatif | À retenir : 1 ou 0, des tables complètes, sept portes, et le brochage avant de câbler. À toi de jouer avec la fiche 130 ! |
