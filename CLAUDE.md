# cours-etml

Générateurs des supports de cours de la section électronique de l'ETML (Gaël Lemoine).

- Lire `REGLES.md` avant toute production : c'est la seule référence pour la mise en page, les normes et le nommage.
- Le contenu d'une séance est dans `contenus/<matière>/<semaine>/`. Le code commun est dans `moteur/`. Une retouche se fait dans le contenu, jamais dans un fichier produit.
- Ne jamais dupliquer un fichier de `moteur/` pour un cas particulier : on étend la brique existante.
- `sortie/` n'est pas versionné. `reference/` contient les sorties étalons servant à vérifier qu'une modification du moteur ne change rien d'imprévu.
- Générer : `python3 build.py <matière>/<semaine>` (voir README.md). Les fichiers sortent dans `sortie/`.
- Avant de livrer : `python3 controle/controler.py <matière>/<semaine> --rendu`, puis humanizer-fr, puis vérification visuelle de la mise en page (images dans `sortie/_controle/`).
- Livrer : régénérer avec `--sauver` (copie la génération dans `reference/<séance>/`), commiter et pousser, puis envoyer les fichiers à Gaël. `reference/` garde ainsi la dernière version livrée de chaque séance.
- Après une modification du moteur : comparer avec `reference/` (`--reference`) et expliquer chaque différence.
- Répondre en français.
