#!/usr/bin/env python3
"""Fiche mémoire TM2 : champs d'apprentissage FutureMEM + couverture par le programme pratique.
Usage : python3 -I build_fiche.py data.json co_cp.json > fiche.md"""
import sys, json

data = json.load(open(sys.argv[1], encoding='utf-8'))
cocp = json.load(open(sys.argv[2], encoding='utf-8'))
BASE = 'https://skills.futuremem.swiss/fr/9999_et/2000_lfe_bfs_2/'

# Situations retenues (non barrées) du programme pratique TM2 ; (f) = grisée, facultative
SIT = {
    'A1-S1': 'Mesurer la caractéristique d’une résistance',
    'A1-S2': 'Mesurer la caractéristique d’une diode Zener',
    'A1-S3': 'Mesurer la caractéristique d’une diode Si (f)',
    'A1-S4': 'Représentation graphique à l’aide d’Excel (f)',
    'A2-S1': 'Lampe à LED',
    'A2-S2': 'Redresseur à diodes',
    'A2-S3': 'Adaptation d’alimentation à diode Zener',
    'A4-S3': 'Projet Horloge',
}
# Couverture : statut (OK / PARTIEL / NON), situations, commentaire
COUV = {
    'LZ_1879': ('NON', [], 'Aucune situation ne compare conducteur, isolant et semi-conducteur.'),
    'LZ_4066': ('NON', [], 'Effet de la température et du champ sur le semi-conducteur non traité (piste : caractéristique de la diode Si à deux températures dans A1-S3).'),
    'LZ_4067': ('NON', [], 'Monocristal, conduction intrinsèque, dopage n/p : théorie seule.'),
    'LZ_2011': ('NON', [], 'Transistor en interrupteur : toutes les situations A3 sont barrées.'),
    'LZ_4108': ('PARTIEL', ['A2-S1'], 'Valeurs limites de la LED seulement ; photodiode, phototransistor et optocoupleur absents.'),
    'LZ_4109': ('NON', [], 'Taux de transfert (CTR) d’un optocoupleur : aucune situation (l’isolation galvanique était dans A3, barrée).'),
    'LZ_5627': ('OK', ['A1-S2', 'A1-S3', 'A2-S2'], 'Caractéristique de diode et redressement.'),
    'LZ_5628': ('PARTIEL', ['A1-S2', 'A2-S1', 'A2-S3'], 'Zener et LED couverts ; transistor de commutation absent.'),
    'LZ_1894': ('OK', ['A2-S1', 'A2-S3'], 'Résistance série de LED, résistance de la Zener.'),
    'LZ_2679': ('NON', [], 'Applications de circuits à transistors : A3 barrée.'),
    'LZ_4112': ('NON', [], 'Montage émetteur commun (continu et alternatif) : aucune situation.'),
    'LZ_9029': ('PARTIEL', ['A2-S1', 'A2-S2', 'A2-S3'], 'Diodes, LED, Zener dimensionnées ; optocoupleur, FET et transistor bipolaire absents.'),
    'LZ_1949': ('PARTIEL', ['A1-S1', 'A2-S1', 'A2-S3'], 'Calcul et mesure de circuits mixtes avec diodes ; la simulation (CP ET b1 08) et les transistors manquent.'),
    'LZ_9041': ('PARTIEL', ['A4-S3'], 'Les bascules de l’horloge servent de compteurs ; la fonction mémoire 1 bit (A4-S2, barrée) n’est pas travaillée en tant que telle. À confirmer selon le cahier des charges de l’horloge.'),
    'LZ_9042': ('PARTIEL', ['A4-S3'], 'Bascules sur front utilisées ; la comparaison niveau / front n’apparaît nulle part.'),
    'LZ_9043': ('PARTIEL', ['A4-S3'], 'Un seul type de mémoire dans l’horloge (registre, bascule D, verrou absents).'),
    'LZ_9044': ('NON', [], 'Monostable / temporisateur : la Minuterie de ventilation (A4-S4) est barrée.'),
    'LZ_9045': ('PARTIEL', ['A4-S3'], 'Compteurs modulo de l’horloge ; la distinction asynchrone / synchrone (A4-S1, barrée) manque.'),
    'LZ_9039': ('NON', [], 'Aucune situation ne mentionne de simulation. À confirmer si le Projet Horloge passe par un simulateur.'),
}
for z in ['LZ_9205', 'LZ_9206', 'LZ_9207', 'LZ_9202', 'LZ_9203', 'LZ_9204', 'LZ_1362', 'LZ_9201']:
    COUV[z] = ('NON', [], 'Champ réseau absent du programme pratique.')

ICON = {'OK': '✅ couvert', 'PARTIEL': '🟠 partiel', 'NON': '❌ non couvert'}
L = []
w = L.append
w('# TM2 — Fiche mémoire des champs d’apprentissage (FutureMEM)')
w('')
w('Module : Test et Mesure 2 (TM2) — champs LFB_El_Dim4, LFB_El_DT2, LFB_Ns_NEBA, 68 L au total.')
w(f'Source : [skills.futuremem.swiss, champs d’apprentissage école professionnelle (2000_lfe_bfs_2)]({BASE}), '
  'relu le 11/16/2026 ; texte identique à l’onglet « Export 11.13.26 » du plan de cours '
  '`000_2026-2027_Plan_de_cours_El_Dim_El_DT2_et_NEBA.xlsx`. Éditeur : Gaël Lemoine.')
w('')
w('**Usage :** référence pour écrire les cours et exercices TM2. Chaque support cite les LZ qu’il vise ; '
  'les LZ marqués ❌ ou 🟠 dans le programme pratique doivent être pris en charge par la théorie ou une nouvelle situation.')
w('')
w('Programme pratique TM2 de référence (`situation_tm2.pdf`, fascicule TM2, 11/16/2026) — situations retenues (non barrées), (f) = facultative :')
w('')
for k, v in SIT.items():
    w(f'- TM2-{k} {v}')
w('')
w('Barrées (exclues de l’analyse) : A3-S1 relais par transistor, A3-S2 variation LED par transistor, A3-S3 moteur DC, '
  'A3-S4 moteur deux sens, A4-S1 compteur asynchrone 4 bits à JK, A4-S2 enregistreur à bascules D, '
  'A4-S4 minuterie de ventilation, A4-S5 AmbianceLED, A4-S6 pilotage moteur DC.')
w('')
w('Niveaux taxonomiques : C2 comprendre, C3 appliquer, C4 analyser, C5 synthétiser. NP = niveau de performance cible de la CP.')
w('')

for f in data:
    code = f['code']
    w('---')
    w('')
    w(f"## [{code}]({BASE}#{f['ancre']}) — {f['intro']} ({f['total_periodes']} L)")
    w('')
    w('### Situation de travail et d’action typique')
    w('')
    sit = f['situation']
    cond = ''
    if 'Conditions:' in sit:
        sit, cond = sit.split('Conditions:', 1)
    w(sit.strip().rstrip(' -'))
    if cond.strip():
        w('')
        w(f'Prérequis (conditions) : {cond.strip()}')
    w('')
    w('### Compétences, objectifs et couverture pratique')
    w('')
    for r in f['lignes']:
        co, cp = r['co'], r['cp'].replace('\xa0', ' ')
        cot = cocp.get(co, {}).get('texte', r['co_titre']).lstrip(' —')
        cpt = cocp.get(cp, {}).get('texte', '')
        w(f"**[CO {co}]({cocp.get(co, {}).get('url', r['co_url'])})** {cot}  ")
        w(f"**[CP {cp}]({cocp.get(cp, {}).get('url', r['cp_url'])})** {cpt} — niveau cible {r['niveau_cible']} — **{r['periodes']} L**  ")
        w(f"Connaissances opérationnelles : {' ; '.join(r['connaissances'])}")
        w('')
        w('| LZ | Niv. | Objectif (texte FutureMEM) | Pratique TM2 | Situations | Remarque |')
        w('|---|---|---|---|---|---|')
        for z in r['lz']:
            st, ss, rem = COUV[z['code']]
            w(f"| [{z['code']}]({z['url']}) | {z['niveau']} | {z['texte']} | {ICON[st]} | "
              f"{', '.join(ss) or '—'} | {rem} |")
        w('')
    w('### Didactique')
    w('')
    for a in f['didactique']:
        w(f"**{a['approche'][0].upper() + a['approche'][1:]}**")
        for step, txt in a['etapes']:
            if txt and txt != '-':
                w(f'- {step} : {txt}')
        w('')
    w('### Contrôles de compétence')
    w('')
    for c in f['controles']:
        w(f"- **{c['nom'][0].upper() + c['nom'][1:]}** : {c['description']}")
    w('')

# Synthèse
w('---')
w('')
w('## Synthèse : LZ non couverts ou partiels dans le programme pratique')
w('')
for f in data:
    nons = [z for r in f['lignes'] for z in r['lz'] if COUV[z['code']][0] == 'NON']
    pars = [z for r in f['lignes'] for z in r['lz'] if COUV[z['code']][0] == 'PARTIEL']
    oks = [z for r in f['lignes'] for z in r['lz'] if COUV[z['code']][0] == 'OK']
    w(f"**{f['code']}** — {len(oks)} couverts, {len(pars)} partiels, {len(nons)} non couverts")
    if nons:
        w('- Non couverts : ' + ', '.join(f"{z['code']} ({z['niveau']})" for z in nons))
    if pars:
        w('- Partiels : ' + ', '.join(f"{z['code']} ({z['niveau']})" for z in pars))
    w('')
w('Hypothèse de lecture : seuls les titres et les notions du programme pratique sont connus. '
  'Le contenu du Projet Horloge (A4-S3) est supposé = compteurs modulo à bascules, sans simulation ni monostable ; à corriger si son cahier des charges dit autre chose.')
print('\n'.join(L))
