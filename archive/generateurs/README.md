# Générateurs — comment rebâtir les supports sans repartir de zéro

Les supports ne sont pas édités à la main : ils sont **produits par ces scripts**.
Pour toute retouche, on modifie le script et on relance, on ne bricole pas le
.pptx ou le .docx.

## Fichiers

| Script | Ce qu'il produit |
|---|---|
| `figures.py` | briques de dessin CEI (résistance rectangle, source, pile, voltmètre, ampèremètre, lampe, interrupteur, flèches de tension) |
| `make_svg.py` | les schémas : source idéale, source réelle, analogie, mesure de Rᵢ, planche de symboles, batterie/démarreur |
| `make_plots.py` | les graphiques matplotlib : caractéristique U(I), dure/molle, quadrillages d'exercice (vide + corrigé) |
| `build_pptx.py` | la présentation, à partir du gabarit ETML |
| `build_docx.py` | la fiche élève ET le corrigé, à partir du gabarit ETML |

## Prérequis dans la session

- `modeles/modele.pptx` et `modeles/modele.docx` = les gabarits ETML de Gael
  (à rattacher à la conversation ; voir `modeles/charte-graphique-ETML.md` pour
  leurs spécifications si les fichiers manquent)
- `fig/` = dossier de travail des images
- `pip install cairosvg --break-system-packages` ; `python-pptx`, `matplotlib`,
  `Pillow` sont déjà là. Police **Carlito** (métriquement compatible Calibri)
  pour que les images s'accordent au thème.

## Ordre d'exécution

```bash
cd fig && python3 make_svg.py && python3 make_plots.py && cd ..
python3 build_pptx.py
python3 build_docx.py          # écrit les deux versions, élève et corrigé
```

## Retouches courantes

- **Texte d'une diapo** : le bloc `# === n. NOM` correspondant dans `build_pptx.py`.
  `_{0}` produit un indice.
- **Position/taille d'une image** : l'appel `picture(s, "…png", x, y, w, h)`,
  en pouces. Zone utile : x de 0,51 à 8,84 ; y de 1,48 à 5,86.
- **Un schéma** : la section correspondante de `make_svg.py`, en coordonnées SVG.
- **Un graphique** : `make_plots.py`.
- **Un exercice** : le bloc `# --- N°n` de `build_docx.py`. `ans(texte, lignes)`
  écrit la réponse en rouge dans le corrigé et pose autant de lignes à remplir
  dans la version élève — les deux fichiers restent synchronisés d'office.

## Contrôles avant livraison

```bash
python3 <skill pptx>/scripts/office/validate.py sortie.pptx --original modeles/modele.pptx
python3 <skill docx>/scripts/office/validate.py sortie.docx --original modeles/modele.docx
```
puis rendu PDF → images des seules pages modifiées, et recalcul indépendant de
tous les résultats numériques.

## Règle importante

Si Gael retouche un fichier livré directement dans PowerPoint ou Word, le script
n'est plus la source de vérité : le relancer écraserait ses corrections. Dans ce
cas, repartir du fichier qu'il renvoie, ou lui redemander les modifications pour
les remettre dans le script.
