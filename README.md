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

À compléter à l'étape 6 de la migration :

```
python build.py tm1/semaine-1
```

## État de la migration

1. Squelette et règles : fait
2. Référence semaine 1 TM1 : fait (fichiers livrés, 11/23/2026)
3. Moteur : à faire
4. Contenus semaine 1 : à faire
5. Génération et comparaison : à faire
6. Bascule du projet claude.ai : à faire
