# Migration vers cours-etml : feuille de route

Document de travail pour reprendre la migration dans une nouvelle discussion. À supprimer une fois la migration terminée.

## Fait

- Étape 2 : squelette, REGLES.md (validé par Gaël le 11/23/2026), modèle Rapport_Simple et logo.
- Étape 3 : `reference/tm1/semaine-1/` (fichiers réellement livrés) et `sources/tm1/semaine-1/` (anciens supports pour les figures).
- Anciens scripts copiés tels quels dans `archive/generateurs/` (les 107 fichiers du dossier `generateurs/` du projet claude.ai).
- Étape 4 : moteur (`moteur/`), une brique par rôle.
- Étape 5 : contenus de la semaine 1 TM1 (`contenus/tm1/semaine-1/`).
- Étape 6 : `build.py`, `controle/` et comparaison avec `reference/` (11/23/2026).

## Résultat de la comparaison avec reference/ (avant les écarts voulus)

Avec `python3 build.py tm1/semaine-1 --date "11/16/2026 23:04:03"` :

- présentations 100 et 120, fiches 110 EX et 110 EX C, pages 101 et 121 : identiques partie par partie ;
- fiches 130 EX et 130 EX C : identiques, sauf la date d'impression (1 s d'écart, l'original avait été généré une seconde plus tard) ;
- vidéos 105 et 125 recalculées : identiques image par image (PSNR infini sur toute la durée) ;
- plan de cours : identique, sauf trois lignes vides (25 à 27) qu'openpyxl n'écrit plus ;
- seules les captures des pages interactives (diapositives « Page interactive ») sont refaites : même cadrage, autre instant de l'animation.

## Écarts appliqués ensuite (un commit chacun)

- Fiches : typographie aussi dans les titres d'exercices, les Titre 1, « Nom : / Date : », les titres A.x et les unités dans les équations (`\u{ ns}`).
- 110 EX C : grille d'auto-évaluation retirée du corrigé (REGLES 4 : fiche élève seulement).
- Présentations : ligne « Gaël Lemoine · date · version » au bas de la diapositive de titre (REGLES 5) ; titres de diapositive et NON‑ET avec la typographie de `typo.py`.
- Pages interactives : typographie française sur le texte affiché du gabarit.
- Équations éditables dans les présentations : prêtes (`--equations omml`), mais **pas encore par défaut** : à ouvrir dans PowerPoint pour valider (voir ci-dessous).

`python3 controle/controler.py tm1/semaine-1` : 0 erreur, 0 avertissement.

## Différences avec le découpage prévu

- `tpl_101.html` et `tpl_121.html` contiennent tout le texte des exercices : ce sont des contenus (`contenus/tm1/semaine-1/101-page.html`, `121-page.html`), pas du moteur. `moteur/pages/` ne garde que `common.css` et `common.js`.
- Nouvelle brique `moteur/seance.py` : lecture de `seance.yaml` et construction de tous les liens (Teams, Floyd, FutureMEM, nextecmedia).
- Les données de cours sur les portes logiques (`moteur/logique.py`) servent aussi aux pages interactives (`pour_page()`) et aux présentations (`pour_js()`).
- Les brochages DIP 14 sont dans `moteur/logique.py` ; `moteur/cei.py` dessine.
- Le plan de cours : `moteur/plan.py` met à jour les lignes de la semaine dans un classeur existant (par défaut celui de `reference/`, sinon `--plan`). Les modifications de structure faites une fois en novembre (suppression d'une ligne, colonnes F à L, note) sont déjà dans le classeur.
- Les images reprises des anciens supports sont dans `contenus/tm1/semaine-1/images/` (provenance : `images/SOURCES.md`).

## Reste à faire

1. **Équations dans PowerPoint** : Gaël ouvre le fichier de test (120 avec `--equations omml`) dans PowerPoint pour Windows. Si les équations s'affichent et se modifient sans message de réparation, passer `--equations` à `omml` par défaut dans `build.py` et régénérer.
2. Bascule du projet claude.ai (étape 7) : remplacer les instructions du projet par un renvoi au dépôt (REGLES.md, CLAUDE.md) ; ne garder dans le projet que la fiche mémoire, les références et les synthèses ; retirer les générateurs du projet une fois la bascule validée.
3. Vrai test sur une nouvelle séance (étape 7) : créer `contenus/tm1/semaine-2/` à partir de la semaine 1, avec les informations de REGLES 2 demandées à Gaël.
4. Typographie des textes écrits par les scripts des pages interactives (leçons animées) : pas encore traitée (seul le texte du gabarit l'est).
