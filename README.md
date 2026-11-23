# cours-etml

Supports de cours ETML (section électronique) produits à partir de contenus versionnés.

## Structure

```
REGLES.md      toutes les règles de production
moteur/        briques communes (charte, équations, symboles CEI, deck, fiche, page, animation, plan)
contenus/      un fichier par séance, rangé par matière et par semaine
controle/      validation, rendu, conventions, recalculs
modeles/       Rapport_Simple.dotx et logo ETML
reference/     sorties étalons : les fichiers réellement livrés (pour comparer après une modification)
sources/       anciens supports d'où l'on extrait des figures (100 d'origine, Circuits intégrés 2016, fiche Moser 2020)
archive/       anciens générateurs, gardés pour mémoire
sortie/        fichiers générés (non versionné)
```

## Utilisation

Prérequis : Python 3 (python-docx, openpyxl, matplotlib, Pillow, PyYAML, playwright), Node.js (pptxgenjs, jszip), ffmpeg, LibreOffice (contrôle).

```
python3 build.py tm1/semaine-1                       # tout : figures, fiches, vidéos, pages, présentations, plan
python3 build.py tm1/semaine-1 --seulement fiches    # une partie : figures, fiches, animations, pages, presentations, plan
python3 build.py tm1/semaine-1 --videos reference    # reprend les vidéos de reference/ (sinon 3 min de calcul)
python3 controle/controler.py tm1/semaine-1          # validation, conventions, recalcul (verif.py) ; --rendu, --reference
python3 controle/comparer.py produit.pptx etalon.pptx --diff
```

Une séance = un dossier `contenus/<matière>/<semaine>/` :

```
seance.yaml               classe, année, matière, champ, date, éditeur, LZ, liens Floyd / nextecmedia / Teams, fichiers, plan
figures.py                figures de la séance (briques : moteur/cei.py)
1x0-….slides.js           diapositives d'une présentation (moteur/deck.js)
1x0-ex.py                 fiche d'exercices et corrigé (moteur/fiche.py)
1x1-page.html, .js        page interactive : gabarit et leçons animées (moteur/page.py)
1x5-anim.py               animation (moteur/anim.py)
verif.py                  recalcul indépendant des résultats (controle/)
images/                   images reprises d'anciens supports (provenance dans SOURCES.md)
```

## État de la migration

Voir `MIGRATION.md`. Semaine 1 TM1 : régénérée à l'identique de `reference/`, puis écarts voulus appliqués (11/23/2026).
