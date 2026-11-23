# Migration vers cours-etml : feuille de route

Document de travail pour reprendre la migration dans une nouvelle discussion. À supprimer une fois la migration terminée.

## Fait

- Étape 2 : squelette, REGLES.md (validé par Gaël le 11/23/2026), modèle Rapport_Simple et logo.
- Étape 3 : `reference/tm1/semaine-1/` (fichiers réellement livrés) et `sources/tm1/semaine-1/` (anciens supports pour les figures).

## Constat sur les générateurs de la semaine 1 (11/23/2026)

- Les présentations (`build_deck_familles_ci.js`, `build_deck_120_portes_body.js`) sont mises en page à la main, diapositive par diapositive (positions en pouces). Un format YAML générique ferait perdre cette mise en page.
- Les fiches (`build_doc_110_familles.py`, `build_doc_130_portes.py`) sont déjà presque du contenu pur, posé sur `docw1.py` ; certains blocs (fiche d'une porte) sont des mises en page propres.
- `w1_data.py` mélange trois choses : les métadonnées de la séance (classe, LZ, liens), des données de cours réutilisables (portes logiques, niveaux des familles) et la typographie.

## Découpage retenu (à confirmer par Gaël)

| Ancien fichier | Nouveau |
|---|---|
| en-tête de `build_deck_familles_ci.js` (masques, typo, squeeze, helpers, diapositives exercices/page/vidéo, écriture) | `moteur/deck.js` |
| corps des présentations (diapositives 1 à n) | `contenus/tm1/semaine-1/100-familles-ci.slides.js`, `120-portes.slides.js` |
| `docw1.py` | `moteur/fiche.py` |
| `build_doc_110_familles.py`, `build_doc_130_portes.py` | `contenus/tm1/semaine-1/110-ex.py`, `130-ex.py` |
| `mathml.py` + `mathml_w1.py` | `moteur/omml.py` (fusion : \bar, \oplus, \sqrt, grecques, indices droits, sin/cos/ln droits) |
| `prep_modele.py` | `moteur/charte.py` |
| métadonnées de `w1_data.py` | `contenus/tm1/semaine-1/seance.yaml` |
| portes, tables de vérité, chronogrammes, niveaux des familles | `moteur/logique.py` |
| typographie (`typo`, `TY`) | `moteur/typo.py` + `moteur/typo.js` (mêmes règles) |
| `figs_w1.py` | `moteur/cei.py` (symboles) + `contenus/.../figures.py` (figures propres à la séance) |
| `build_pages_w1.py`, `pages/common.*`, `tpl_*.html` | `moteur/page.py`, `moteur/pages/` |
| `lessons_101.js`, `lessons_121.js` | `contenus/tm1/semaine-1/101-page.js`, `121-page.js` |
| `anim_common.py` | `moteur/anim.py` ; `anim_105.py`, `anim_125.py` → `contenus/.../105-anim.py`, `125-anim.py` |
| `make_covers.py` | `moteur/couverture.py` |
| `maj_plan_tm1_s1.py` | `moteur/plan.py` + données dans `seance.yaml` |
| `rebuild_all_w1.sh` | `build.py` (plus d'assemblage du 120 par découpage de texte) |

Les anciens scripts sont copiés tels quels dans `archive/generateurs/` avant toute modification.

## Écarts voulus par rapport à la référence

- Ligne « Gaël Lemoine · date » sur la diapositive de titre (REGLES 5).
- Formules éditables (OMML) dans les présentations (REGLES 3.2).

## Reste à faire

4. Moteur (tableau ci-dessus), 5. Contenus, 6. `build.py` + `controle/` + comparaison avec `reference/`, 7. bascule du projet claude.ai et vrai test sur une nouvelle séance.
