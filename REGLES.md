# Règles de production des supports de cours ETML

Seule référence pour produire les présentations, fiches, corrigés, tests, pages interactives et animations de la section électronique de l'ETML. Elle remplace les instructions du projet claude.ai, les règles de mise en page gardées en mémoire et l'ancienne `charte-graphique-ETML.md` (Calibri/Cambria, abandonnée depuis le 11/02/2026).

Éditeur des documents : Gaël Lemoine. Dates à l'américaine : MM/DD/YYYY (ex. 11/23/2026).

## 1. Public et pédagogie

- Apprentis électroniciens CFC, formation par compétences (réforme FutureMEM).
- Chaque séance : théorie, présentation diapositive par diapositive, exercices, avec les méthodes d'apprentissage les plus solides connues (activation des acquis, exemples travaillés, pratique espacée, auto-évaluation).
- Toute notion, tout exemple ou exercice nouveau arrive avec son contexte : à quoi ça sert, pourquoi on l'utilise, où on le retrouve dans le métier, pour que l'apprenti puisse se projeter. Pour TM1, le fil rouge est la situation de travail FutureMEM (ligne de remplissage de boissons).

## 2. Avant chaque nouvelle édition

Demander, sans exception : la classe, l'année scolaire, le champ d'apprentissage, la matière et les références (liens) à utiliser. Ces informations vont dans l'en-tête du fichier de contenu de la séance.

Matière par défaut pour TM1 : « Test et Mesure 1 – El DT 1 ». Ne plus écrire « IntElect » ni « El Dim1 ».

## 3. Normes et notations

- Symboles électriques et logiques : norme CEI (CEI 60617). Portes logiques : symboles européens seulement (rectangle + qualificatif, cercle de négation).
- Nombres : suffixe à la fin. Binaire `0101b`, décimal `89d`, hexadécimal `59h` (b et h minuscules), BCD `… BCD`.
- Tables de vérité : entrées du poids fort au poids faible, puis la sortie (C B A Y, B A Y, A Y). A est toujours le poids faible ; lignes dans l'ordre du comptage binaire. Dans une table « cahier des charges », la première variable écrite est le poids fort. Les symboles CEI et les chronogrammes (A en haut, puis B) ne changent pas.
- Équations logiques en notation Floyd (X = AB, X = A + B, barre = NON), sortie notée Y.
- Niveaux et délais : notation des fiches techniques (V_IH, V_IL, V_OH, V_OL, t_PHL, t_PLH), avec un renvoi à la notation du Floyd (V_EH, V_EB, V_SH, V_SB, t_PHB, t_PBH).
- Indices descriptifs en romain (U_R, R_i) ; variables en italique.

## 4. Documents Word (fiches, corrigés, tests)

- Toujours partir du modèle `modeles/Rapport_Simple.dotx` : police, styles, en-tête, pied de page, logo.
- A4 ; marges haut 2 cm, bas 1,75 cm, gauche 2 cm, droite 1,5 cm ; en-tête à 0,5 cm.
- Normal : Arial 11 pt justifié, interligne 1,5. Titre : Arial 20 pt gras centré. Titre 1 : Arial 14 pt gras numéroté.
- En-tête : logo à gauche ; « Section électronique » et « Nom - Type - Numéro » à droite. Pied de page sur 3 colonnes : auteur/modification, Page X sur Y, création/impression/nom de fichier.
- Couleurs ETML (thème T&M) : bleu marine `242852` dominant, bleu `297FD5`, bleu clair `ACCBF9`.
- Corrigé : réponses en rouge `EE0000`. La fiche élève et le corrigé sortent du même contenu ; on produit toujours les deux.
- Formules : équations Word natives et éditables (OMML, `moteur/omml.py`), jamais en texte simple ni en image.
- Exercices : « N°1 », « N°2 »… suivis directement du titre, sans tabulation ni minutage aligné à droite.
- Lignes de réponse gardées sur la même page que leur question. Grille d'auto-évaluation dans la fiche élève seulement, pas dans le corrigé.

## 5. Présentations

- Même police que le modèle Word (Arial), couleurs ETML, format 16:10 (10 × 6,25 pouces).
- Bande bleue verticale à droite avec le logo en blanc, « Section électronique » et le numéro de page.
- Ordre de fin : d'abord les exercices, puis la page interactive, puis la vidéo d'animation.
- Cartouche des diapositives de titre : classe, année, matière, champ (lien), version. Depuis la génération TM1 semaine 1 (11/16/2026), sans ligne « éditeur · date » sur les diapositives (le pied de page Word garde l'auteur).

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
