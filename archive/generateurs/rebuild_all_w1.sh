#!/bin/sh
# Régénère toute la semaine 1 (données, deux présentations, fiches 110 EX et 130 EX, plan de cours).
# Les présentations finissent par : exercices → page interactive (101 / 121) → vidéo (105 / 125, intégrée).
# Prérequis : out/105 … .mp4 et out/125 … .mp4 (anim_105.py, anim_125.py), cover_105.png et cover_125.png (make_covers.py),
# shot_101.png et shot_121.png (captures des pages interactives, build_pages_w1.py puis capture).
set -e
cd "$(dirname "$0")"
python3 -I w1_data.py > /dev/null
python3 - <<'PY'
s = open('build_deck_familles_ci.js', encoding='utf-8').read()
a = s.index('const pptxgen = require("pptxgenjs");'); b = s.index("// Symbole CEI 60617-12 d'une porte NON-ET")
head = s[a:b].replace('pres.title = "Familles de circuits logiques";', 'pres.title = "Portes logiques et tables de vérité";') \
             .replace('const TOPIC = MATIERE + " · Familles de circuits logiques";', 'const TOPIC = MATIERE + " · Portes logiques et tables de vérité";') \
             .replace('VERSION = "1.3";', 'VERSION = "1.2";')
open('deck120_head.js', 'w', encoding='utf-8').write(head)
tail = s[s.index('// pptxgenjs écrit un <a:pPr> par run'):].replace('out/100 Familles de circuits logiques.pptx', 'out/120 Portes logiques et tables de vérité.pptx').replace('deck 100 ok', 'deck 120 ok')
open('deck120_tail.js', 'w', encoding='utf-8').write(tail)
PY
{ printf '%s\n' "// 120 Portes logiques et tables de vérité · v1.2 (11/16/2026 : fiche 130 EX ; fin : exercices, page interactive 121, animation 125) · 17 diapositives · charte ETML, Arial, 16:10" \
  "// Classe XLO1, 2026-2027, Test et Mesure 1 – El DT 1, champ LFB_El_DT1 (LZ_4242, LZ_130, LZ_27, LZ_29, LZ_2223)." \
  "// Données : w1_data.json (w1_data.py) ; figures : figs_w1.py. Va avec la fiche 130 EX Portes logiques de base. Tables : entrées du poids fort au poids faible."; \
  cat deck120_head.js build_deck_120_portes_body.js deck120_tail.js; } > build_deck_120.js
node build_deck_familles_ci.js
node build_deck_120.js
python3 -I build_doc_110_familles.py
python3 -I build_doc_130_portes.py
python3 -I maj_plan_tm1_s1.py /home/claude/plan/src.xlsx out/PlanDeCoursTheorie_TM1_Local.xlsx
