# cours-etml

Générateurs des supports de cours de la section électronique de l'ETML (Gaël Lemoine).

- Lire `REGLES.md` avant toute production : c'est la seule référence pour la mise en page, les normes et le nommage.
- Le contenu d'une séance (une ligne du plan) est dans `contenus/<module>/semaine-<N>/<numéro>-<sujet>/` (REGLES 2). Le code commun est dans `moteur/`. Une retouche se fait dans le contenu, jamais dans un fichier produit.
- Ne jamais dupliquer un fichier de `moteur/` pour un cas particulier : on étend la brique existante.
- `sortie/` n'est pas versionné. `reference/` contient les sorties étalons servant à vérifier qu'une modification du moteur ne change rien d'imprévu.
- Cadrage (REGLES 2) : partir de la ligne du plan de cours (`plans/<module>/`), pré-remplir `seance.yaml`, ne demander que les liens Floyd ou nextecmedia manquants, puis faire valider une fiche de cadrage. Ne jamais modifier un plan de cours depuis une discussion de cours.
- Générer en deux phases (REGLES 10) : `python3 build.py <module>/semaine-<N>/<numéro>-<sujet> --phase contenu` pour les boucles courtes (figures, fiches, présentation provisoire), jusqu'à ce que Gaël valide le contenu ; puis `--phase medias` (page interactive, artefact claude.ai, vidéos, présentation finale). Ne jamais lancer la phase médias avant cette validation. Les fichiers sortent dans `sortie/`.
- Avant de livrer : `python3 controle/controler.py <module>/semaine-<N>/<numéro>-<sujet> --rendu` sans erreur, chaque avertissement « mise en page » corrigé ou justifié, puis humanizer-fr, puis relecture visuelle de toutes les pages à au moins 90 dpi (`pdftoppm -r 90` sur les PDF de `sortie/_controle/`). Gaël ne doit pas avoir à demander une correction de mise en page.
- Après chaque génération envoyée à Gaël : lui demander si c'est la version finale. Seulement s'il répond oui : régénérer avec `--sauver` (copie dans `reference/<séance>/`), commiter et pousser. Jamais de `--sauver` sans son accord : les essais restent dans `sortie/`.
- Après une modification du moteur : comparer avec `reference/` (`--reference`) et expliquer chaque différence.
- Répondre en français.
