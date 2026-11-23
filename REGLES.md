# Règles de production des supports de cours ETML

Seule référence pour produire les présentations, fiches, corrigés, tests, pages interactives et animations de la section électronique de l'ETML. Elle remplace les instructions du projet claude.ai, les règles de mise en page gardées en mémoire et l'ancienne `charte-graphique-ETML.md` (Calibri/Cambria, abandonnée depuis le 11/02/2026).

Éditeur des documents : Gaël Lemoine. Dates à l'américaine : MM/DD/YYYY (ex. 11/23/2026).

## 1. Public et pédagogie

- Apprentis électroniciens CFC, formation par compétences (réforme FutureMEM).
- Chaque séance : théorie, présentation diapositive par diapositive, exercices, avec les méthodes d'apprentissage les plus solides connues (activation des acquis, exemples travaillés, pratique espacée, auto-évaluation).
- Toute notion, tout exemple ou exercice nouveau arrive avec son contexte : à quoi ça sert, pourquoi on l'utilise, où on le retrouve dans le métier, pour que l'apprenti puisse se projeter. Pour TM1, le fil rouge est la situation de travail FutureMEM (ligne de remplissage de boissons).

## 2. Avant chaque nouvelle édition

Demander, sans exception : la classe, l'année scolaire, le champ d'apprentissage, la matière et les références (liens) à utiliser. Ces informations vont dans l'en-tête du fichier de contenu de la séance. Aucune valeur par défaut : la matière est toujours demandée.

Si la réponse au champ d'apprentissage est « non », le cours est hors réforme : pas de champ, pas de LZ ni de lien FutureMEM, ni dans le cartouche des présentations, ni dans les fiches, ni dans le plan de cours. Tout le reste des règles s'applique.

Ne plus écrire « IntElect » ni « El Dim1 ».

## 3. Normes et notations

### 3.1 Grandeurs, unités et nombres

- Unités SI, symboles des grandeurs selon CEI 60027 / ISO 80000 : variables en italique (U, I, R, t), unités en romain (V, A, Ω, s), indices descriptifs en romain (U_R, R_i, U_ph).
- Virgule décimale (2,5 V). Espace insécable entre le nombre et l'unité (12 V), et comme séparateur des milliers (10 000).
- Notation ingénieur : exposants multiples de 3 et préfixes usuels de l'atelier (G, M, k, m, µ, n, p). On écrit 30 [mA], pas 0,03 [A]. Dans un calcul détaillé, l'étape intermédiaire peut garder la puissance de dix (0,6 · 10³ [Ω]) avant le résultat avec préfixe (600 [Ω]).
- Sur les schémas, valeurs normalisées en notation atelier : 2k2, 4k7, 1M5, 100n (le préfixe tient lieu de virgule).
- Résultats en notation ingénieur, arrondis à 4 chiffres significatifs, sans écrire les zéros de fin : 3,456 [V] · 12,35 [kΩ] · 324 [mA] (et non 0,324 A ni 324,0 mA).
- Dans un calcul (application numérique et résultat), l'unité s'écrit entre crochets : I = 12 [V] / 37 [Ω] = 324 [mA]. Dans le texte courant, sans crochets (une pile de 1,5 V).

### 3.2 Formules et calculs

- Toute résolution suit le même ordre : formule littérale, puis application numérique avec les unités, puis résultat avec unité et préfixe, puis contrôle (ordre de grandeur, autre méthode ou vérification inverse). Le contrôle est écrit : c'est une compétence évaluée.
- Formules toujours éditables, dans Word comme dans PowerPoint : équations natives OMML (`moteur/omml.py`), jamais en texte simple ni en image. Dans les pages interactives : même écriture (italiques, indices, fractions). Jamais de « * » ni de « / » à la place d'une fraction dans une formule mise en avant.
- Multiplication : point médian (U = R · I) ; « × » seulement entre deux nombres (3 × 0,2 V).

### 3.3 Schémas et graphiques

- Symboles électriques et logiques : norme CEI 60617. Résistance en rectangle. Portes logiques : symboles européens seulement (rectangle + qualificatif, cercle de négation).
- Flèche de tension toujours du + vers le − (pointe du côté du potentiel le plus bas), toujours à droite de son composant et toujours en bleu ETML `297FD5`, nom de la tension à droite de la flèche. Convention récepteur (courant et tension dans le même sens), sauf pour les sources (convention générateur : sens contraires).
- Nom et valeur d'un composant (R_1, 4k7, 9 V) à gauche de son symbole : la droite est réservée à la flèche de tension.
- Masse (GND) : un trait horizontal relié par un court fil vertical à un nœud du circuit, avec l'étiquette « GND ». Le symbole de la terre (traits décroissants) est réservé à une vraie liaison à la terre.
- Ces conventions sont imposées par `moteur/cei.py` (`fleche_tension`, `resistance`, `source_tension`, `masse`) : un nouveau schéma les suit sans réglage.
- Graphiques : chaque axe porte la grandeur et son unité ; mêmes couleurs ETML que les documents.

### 3.4 Numérique

- Nombres : suffixe à la fin. Binaire `0101b`, décimal `89d`, hexadécimal `59h` (b et h minuscules), BCD `… BCD`.
- Tables de vérité : entrées du poids fort au poids faible, puis la sortie (C B A Y, B A Y, A Y). A est toujours le poids faible ; lignes dans l'ordre du comptage binaire. Dans une table « cahier des charges », la première variable écrite est le poids fort. Les symboles CEI et les chronogrammes (A en haut, puis B) ne changent pas.
- Équations logiques en notation Floyd (X = AB, X = A + B, barre = NON), sortie notée Y.
- Niveaux et délais : notation des fiches techniques (V_IH, V_IL, V_OH, V_OL, t_PHL, t_PLH), avec un renvoi à la notation du Floyd (V_EH, V_EB, V_SH, V_SB, t_PHB, t_PBH).

## 4. Documents Word (fiches, corrigés, tests)

- Toujours partir du modèle `modeles/Rapport_Simple.dotx` : police, styles, en-tête, pied de page, logo.
- A4 ; marges haut 2 cm, bas 1,75 cm, gauche 2 cm, droite 1,5 cm ; en-tête à 0,5 cm.
- Normal : Arial 11 pt justifié, interligne 1,5. Titre : Arial 20 pt gras centré. Titre 1 : Arial 14 pt gras numéroté.
- En-tête : logo à gauche ; « Section électronique » et « Nom - Type - Numéro » à droite. Pied de page sur 3 colonnes : auteur/modification, Page X sur Y, création/impression/nom de fichier.
- Couleurs ETML (thème T&M) : bleu marine `242852` dominant, bleu `297FD5`, bleu clair `ACCBF9`.
- Corrigé : réponses en rouge `EE0000`. La fiche élève et le corrigé sortent du même contenu ; on produit toujours les deux.
- Formules : équations natives éditables (voir 3.2).
- Exercices : « N°1 », « N°2 »… suivis directement du titre, sans tabulation ni minutage aligné à droite.
- Lignes de réponse gardées sur la même page que leur question. Grille d'auto-évaluation dans la fiche élève seulement, pas dans le corrigé.

## 5. Présentations

- Même police que le modèle Word (Arial), couleurs ETML, format 16:10 (10 × 6,25 pouces).
- Bande bleue verticale à droite avec le logo en blanc, « Section électronique » et le numéro de page.
- Ordre de fin : d'abord les exercices, puis la page interactive, puis la vidéo d'animation.
- Cartouche de la première diapositive (titre) : classe, année, matière, champ (lien, sauf cours hors réforme), version, et la ligne « Gaël Lemoine · date ». L'éditeur n'apparaît que là et dans le pied de page Word, sur aucune autre diapositive.

## 6. Liens

- Liens Floyd et Nextec toujours cliquables, dans tous les documents.
- Floyd : lien « Copier le lien » de Teams (paramètre `d=…`), jamais un chemin reconstruit. Le lien ouvre le chapitre ; la page est écrite dans le texte du lien (« Floyd 3-2 p. 115 »). Jamais de « § » devant le numéro de section. Les fiches ont une ligne « Pages du Floyd » (page du livre → page du PDF).
- FutureMEM : chaque LZ a son propre lien (fiche `5000_lze_NN` avec ancre). Dans Word, PowerPoint et Excel, préfixer l'URL complète par `microsoft-edge:` pour que l'ancre soit respectée (Windows + Edge seulement). Pas de préfixe pour les liens Floyd dans Excel.
- La liste des liens validés est dans le projet claude.ai (`references-liens.md`) ; chaque fichier de contenu reprend ceux de sa séance.

## 7. Typographie française

- Espaces insécables avant : ; ? ! » et après «, entre un nombre et son unité ou son mot, dans « A = 1 », « 0 ou 1 ».
- Trait d'union insécable dans NON-ET, NON-OU, OU-exclusif (Word : `w:noBreakHyphen`).
- Encadrés, liens et questions alignés à gauche.

## 8. Nommage des fichiers

- Semaine N : `N00` 1re présentation, `N10` exercices, `N20` 2e présentation, `N30` exercices… ; `N01`, `N21` pages interactives ; `N05`, `N25` animations.
- Fiches d'exercices : « 130 EX Titre » ; corrigé « 130 EX C Titre ». Même nom dans les renvois des présentations.

## 9. Avant de livrer

1. `controle/` passe sans erreur : validation des fichiers Office, rendu en images, conventions de ce document, recalcul indépendant de tous les résultats numériques.
2. Passer le skill humanizer-fr sur tout le texte rédigé.
3. Vérifier la mise en page sur le rendu (pages modifiées au minimum).

## 10. Règles de travail du dépôt

- On n'édite jamais un .docx ou un .pptx produit : on modifie le contenu (ou le moteur) et on relance. Si Gaël retouche un fichier livré à la main, on reporte la retouche dans le contenu avant toute nouvelle génération.
- Une seule version de chaque brique dans `moteur/`. Une amélioration demandée pour une séance profite à toutes : on ne copie jamais un fichier du moteur pour l'adapter.
- Chaque étape validée se termine par un commit.
- Version finale : après chaque génération, on demande à Gaël si c'est la version finale. Seulement s'il le confirme, la génération est copiée dans `reference/<matière>/<semaine>/` (`build.py --sauver`) et commitée : GitHub garde la dernière version finale de chaque séance, qui sert aussi d'étalon pour les comparaisons. Les générations d'essai restent dans `sortie/`, non versionné.
