# Règles de production des supports de cours ETML

Seule référence pour produire les présentations, fiches, corrigés, tests, pages interactives et animations de la section électronique de l'ETML. Elle remplace les instructions du projet claude.ai, les règles de mise en page gardées en mémoire et l'ancienne `charte-graphique-ETML.md` (Calibri/Cambria, abandonnée depuis le 11/02/2026).

Éditeur des documents : Gaël Lemoine. Dates à l'américaine : MM/DD/YYYY (ex. 11/23/2026).

## 1. Public et pédagogie

- Apprentis électroniciens CFC, formation par compétences (réforme FutureMEM).
- Chaque séance : théorie, présentation diapositive par diapositive, exercices, avec les méthodes d'apprentissage les plus solides connues (activation des acquis, exemples travaillés, pratique espacée, auto-évaluation).
- Toute notion, tout exemple ou exercice nouveau arrive avec son contexte : à quoi ça sert, pourquoi on l'utilise, où on le retrouve dans le métier, pour que l'apprenti puisse se projeter. Pour TM1, le fil rouge est la situation de travail FutureMEM (ligne de remplissage de boissons) ; à partir de la série 120 (V2, 11/27/2026), les portes logiques s'appuient sur l'exercice TM1-A1-S2 du fascicule TM1 : le démarrage d'une voiture électrique (ceinture A et frein C actifs à 0, sélecteur B et mode service D actifs à 1, voyant S = B · (D + /(A + C)), câblé sur 74HC02, 74HC32 et 74HC08).

## 2. Avant chaque nouvelle édition : le cadrage part du plan de cours

Le plan de cours est l'entrée du cadrage. Il est préparé dans une discussion à part du projet claude.ai et rangé dans le dépôt (`plans/<module>/`, voir `plans/README.md`). Les discussions de cours le lisent sans jamais le modifier.

1. Gaël désigne la ligne du plan à traiter (ex. « TM2, 120 Diode et diode Zener »).
2. On lit dans le plan : classe, année, module, date de la semaine, périodes, LZ (colonne H), noms de fichiers (colonne Ressources), situation pratique (Remarques) ; dans l'onglet Export : texte et lien de chaque LZ ; dans l'onglet Couverture : ce que la théorie doit couvrir. Ces valeurs pré-remplissent `seance.yaml`.
3. Matière du cartouche : « Test et Mesure N – » suivi du champ de la colonne H (LFB_El_Dim4 → El Dim 4, LFB_El_DT2 → El DT 2), comme « Test et Mesure 1 – El DT 1 ». Classe en majuscules (XLO1) ; dates converties au format MM/DD/YYYY.
4. Références : si le plan n'a pas les liens Floyd ou nextecmedia de la ligne, les demander à Gaël. Aucun lien inventé.
5. On présente à Gaël une fiche de cadrage pré-remplie (objectifs, fil rouge, ce que la théorie doit couvrir, découpage sur les périodes, références) ; il corrige ou valide en un message, puis la phase contenu démarre.

Sans plan de cours (cours isolé), demander comme avant : la classe, l'année scolaire, le champ d'apprentissage, la matière et les références. Aucune valeur par défaut : la matière est toujours demandée.

Une discussion par ligne du plan (une présentation et sa fiche), pas une par semaine. Les lignes d'une même semaine se traitent l'une après l'autre : la première peut compléter le moteur (symboles, briques) dont les suivantes ont besoin.

Rangement : un dossier par ligne du plan, `contenus/<module>/semaine-<N>/<numéro>-<sujet>/` (ex. `contenus/tm2/semaine-1/120-diode-zener/`), avec sa propre `seance.yaml`. On génère et on sauve une ligne à la fois : `python3 build.py tm2/semaine-1/120-diode-zener --phase contenu`. La semaine 1 de TM1, faite avant cette règle, reste dans un seul dossier.

Si la réponse au champ d'apprentissage est « non », le cours est hors réforme : pas de champ, pas de LZ ni de lien FutureMEM, ni dans le cartouche des présentations, ni dans les fiches. Tout le reste des règles s'applique.

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
- Alimentation (+5 V, V_CC) : même symbole que la masse, retourné : court fil vertical vers le haut, trait horizontal, étiquette au-dessus du trait. Elle est toujours plus haut que les composants qu'elle alimente (demande de Gaël du 11/27/2026).
- Liaisons, comme dans Altium (demande de Gaël du 11/27/2026), sur les schémas comme sur les dessins de câblage des pages interactives (breadboard) :
  - un point de liaison (point plein) à chaque jonction en T, y compris sur un rail d'alimentation ; jamais de point sur un simple croisement ;
  - un croisement sans liaison se dessine avec un saut de fil (« jumpover ») : le tronçon horizontal saute le tronçon vertical par un petit demi-cercle.
- Ces conventions sont imposées par `moteur/cei.py` (`fleche_tension`, `resistance`, `source_tension`, `masse`, `alimentation`, `fil` avec `noeuds` et `sauts`), dans les pages interactives par `moteur/pages/common.js` (`filP`, `liaison`, `alimG`, `masseG`) et dans les vidéos par `moteur/anim.py` (`masse`, `alimentation`, `noeud`) : un nouveau schéma les suit sans réglage.
- Graphiques : chaque axe porte la grandeur et son unité ; mêmes couleurs ETML que les documents.

### 3.4 Numérique

- Nombres : suffixe à la fin. Binaire `0101b`, décimal `89d`, hexadécimal `59h` (b et h minuscules), BCD `… BCD`.
- Tables de vérité : entrées du poids fort au poids faible, puis la sortie (C B A Y, B A Y, A Y). A est toujours le poids faible ; lignes dans l'ordre du comptage binaire. Dans une table « cahier des charges », la première variable écrite est le poids fort. Les symboles CEI et les chronogrammes (A en haut, puis B) ne changent pas.
- Équations logiques en notation Floyd (S = AB, S = A + B, barre = NON). La sortie s'appelle toujours S ; les entrées A, B, C, D… (jamais d'initiales comme M, P, V). Le sens de chaque lettre est donné dans une légende (« A : machine en marche »). Demande de Gaël du 11/23/2026 ; la semaine 1 de TM1, faite avant, garde Y.
- Niveaux et délais : notation des fiches techniques (V_IH, V_IL, V_OH, V_OL, t_PHL, t_PLH), avec un renvoi à la notation du Floyd (V_EH, V_EB, V_SH, V_SB, t_PHB, t_PBH).

### 3.5 Tableaux de Karnaugh

Modèle de Gaël (11/24/2026), dessiné par `moteur/cei.py` (`karnaugh`, `fig_karnaugh`, `image_karnaugh` pour les vidéos) et, dans les pages interactives, par `kmapSVG` (gabarit de la page 221) :
- Codes gris sur des bandes : colonnes BA (00, 01, 11, 10) en haut, lignes DC (00, 01, 11, 10) à gauche, texte tourné. A est le poids faible (k = 8·D + 4·C + 2·B + A).
- Zones jaunes : A en haut, B en bas, C à gauche, D à droite, lettre centrée dans sa zone. Lignes intérieures ocre ; celles qui bordent les zones A et C traversent la bande grise ; un trait foncé sépare les zones A et C de leur bande. Bord du tableau foncé.
- Coin : diagonale depuis le coin haut gauche ; BA au-dessus, DC à gauche, à la même distance de la diagonale (symétriques) ; la sortie S au bout de la diagonale.
- Groupes : un rectangle de couleur par groupe ; un groupe coupé par un bord s'ouvre vers l'extérieur (aucun côté sur le bord du tableau).
- Termes (présentations, fiches, vidéos) : chaque terme, de la couleur de son groupe, est relié à son groupe par un trait à 45° vers l'extérieur, puis horizontal. Le trait ne longe aucune ligne, ne passe ni sur un chiffre, ni sur une bande, une zone A ou C, une lettre ou le trait de S, et ne croise pas un autre trait. Un groupe sans coin libre part du milieu d'un côté de case (le trait passe entre deux chiffres) ; en dernier recours, le trait traverse la zone B ou D loin de sa lettre. Aucun terme sur le tableau, une bande ou une zone, ni sur un autre terme.
- `controle/karnaugh.py` vérifie ces points (bloquant) à partir de `karnaugh_figures.json`.

## 4. Documents Word (fiches, corrigés, tests)

- Toujours partir du modèle `modeles/Rapport_Simple.dotx` : police, styles, en-tête, pied de page, logo.
- A4 ; marges haut 2 cm, bas 1,75 cm, gauche 2 cm, droite 1,5 cm ; en-tête à 0,5 cm.
- Normal : Arial 11 pt justifié, interligne 1,5. Titre : Arial 20 pt gras centré. Titre 1 : Arial 14 pt gras numéroté.
- En-tête : logo à gauche ; « Section électronique » et « Nom - Type - Numéro » à droite. Pied de page sur 3 colonnes : auteur/modification, Page X sur Y, création/impression/nom de fichier.
- Couleurs ETML (thème T&M) : bleu marine `242852` dominant, bleu `297FD5`, bleu clair `ACCBF9`.
- Corrigé : réponses en rouge `EE0000`. La fiche élève et le corrigé sortent du même contenu ; on produit toujours les deux.
- Formules : équations natives éditables (voir 3.2).
- En-tête de fiche : titre centré ; ligne d'informations (fiche, matière, classe, année, puis champ et LZ sur une deuxième ligne) alignée à gauche ; « Nom : » et « Date : » avec une ligne pointillée pour écrire. Consignes, encadrés et questions alignés à gauche, jamais justifiés.
- Tableaux à remplir : lignes assez hautes pour écrire dans la fiche élève ; dans le corrigé, réponses longues alignées à gauche.
- Exercices : « N°1 », « N°2 »… suivis directement du titre, sans tabulation ni minutage aligné à droite.
- Lignes de réponse gardées sur la même page que leur question. Grille d'auto-évaluation dans la fiche élève seulement, pas dans le corrigé.

## 5. Présentations

- Même police que le modèle Word (Arial), couleurs ETML, format 16:10 (10 × 6,25 pouces).
- Bande bleue verticale à droite avec le logo en blanc, « Section électronique » et le numéro de page.
- Ordre de fin : d'abord les exercices, puis la page interactive, puis la vidéo d'animation.
- Objectifs de la diapositive de titre : chaque objectif finit par son ou ses LZ cliquables (« … (LZ_4255) »), sauf cours hors réforme. Tous les LZ de `seance.yaml` y figurent ; `controle/` le vérifie et bloque sinon.
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
3. Mise en page : `controle/ --rendu` signale débordements, chevauchements, pages presque vides et unités coupées ; chaque avertissement est corrigé ou justifié. Puis relecture visuelle de toutes les pages à une résolution lisible (au moins 90 dpi), pas seulement des pages modifiées. Gaël ne doit pas avoir à demander une correction de mise en page.
4. Erreurs bloquantes de mise en page (ajoutées le 11/23/2026 après la séance TM2 120) :
   - Figures (`moteur/cei.save`) : un texte posé sur une courbe, un trait de repère ou une flèche, ou deux textes qui se chevauchent. S'applique aux graphiques comme aux schémas.
   - Lisibilité : une fois la figure placée, son plus petit texte fait au moins 8 pt dans une présentation et 7 pt dans une fiche. Sinon, on agrandit la figure ou ses textes.
   - Équations éditables : PowerPoint les affiche à leur taille de police, sans les réduire à leur cadre. LibreOffice et l'aperçu de claude.ai montrent l'image de secours, ajustée au cadre : ils ne voient pas le débordement. Depuis le 11/27/2026 (présentation 200 : 25 équations qui débordaient dans PowerPoint, invisibles au contrôle) :
     - `moteur/omml.py` (`mesure`) mesure chaque équation comme Office la compose : Cambria Math, espaces autour de =, +, ·, barres, fractions, indices. `moteur/deck.js` réduit le corps pour que l'équation tienne dans son cadre réel, lu dans le fichier final (après `squeeze`).
     - Le rendu de contrôle des présentations est une simulation PowerPoint (`controle/mise_en_page.simulation_powerpoint`) : chaque équation y a la taille que PowerPoint lui donnera. La relecture à 90 dpi se fait sur ce rendu.
     - Le contrôle bloque si une équation dépasse son cadre ; `controle/test_equations.py` vérifie que la mesure voit toujours le cas de la 200.
     - Images de secours des équations : fond transparent, comme l'équation éditable.
     - Ne jamais placer une équation avec une autre fonction que `eqImg` / `eqName` avec la taille de son cadre : sans cadre, aucun ajustement n'est possible.
5. Relecture des figures et des vidéos : `controle/ --rendu` produit des planches `sortie/_controle/<séance>/figures-*.png` (4 figures par page) et `video-*.png` (images clés des animations, une toutes les 5 s). Les pages interactives sont vérifiées automatiquement : textes des dessins qui se chevauchent ou posés sur un trait ou un cercle, dans les exercices et à chaque étape des animations. Chaque planche est lue en entier avant l'envoi : textes, flèches, étiquettes, porteurs. Le contrôle automatique ne remplace pas cette lecture.

## 10. Règles de travail du dépôt

- On n'édite jamais un .docx ou un .pptx produit : on modifie le contenu (ou le moteur) et on relance. Si Gaël retouche un fichier livré à la main, on reporte la retouche dans le contenu avant toute nouvelle génération.
- Une seule version de chaque brique dans `moteur/`. Une amélioration demandée pour une séance profite à toutes : on ne copie jamais un fichier du moteur pour l'adapter.
- Chaque étape validée se termine par un commit.
- Le plan de cours appartient à sa discussion « plan » : une discussion de cours le lit et ne l'écrit jamais. Une modification du plan (lien, titre, LZ) se demande dans la discussion « plan ».
- Deux phases de génération. Phase contenu (`build.py --phase contenu`) : figures, fiches, plan de cours et présentation provisoire, où la page interactive et la vidéo sont remplacées par des emplacements ; on boucle relecture et corrections jusqu'à ce que Gaël valide le contenu. Phase médias (`--phase medias`), seulement après cette validation : page interactive et publication de l'artefact, vidéos, présentation finale. Une correction de fond trouvée en phase médias se fait dans le contenu, puis on relance la phase médias.
- Version finale : après chaque génération, on demande à Gaël si c'est la version finale. Seulement s'il le confirme, la génération est copiée dans `reference/<matière>/<semaine>/` (`build.py --sauver`) et commitée : GitHub garde la dernière version finale de chaque séance, qui sert aussi d'étalon pour les comparaisons. Les générations d'essai restent dans `sortie/`, non versionné.
