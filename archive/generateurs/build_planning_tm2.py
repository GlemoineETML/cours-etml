#!/usr/bin/env python3
"""Premier planning TM2 dans l'onglet PlanDeCours (tableau « Tableau1 »).
60 L (LFB_El_Dim4 + LFB_El_DT2) réparties sur 5 semaines (12 L / semaine) ; NEBA hors planning, semaine 6 en réserve.
Une ligne par séquence : titre (C), documents à générer (D), périodes (G), lien FutureMEM (H).
Usage : python3 -I build_planning_tm2.py in.xlsx data.json out.xlsx"""
import sys, json, datetime as dt
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo

src, data_p, out = sys.argv[1:4]
data = {f['code']: f for f in json.load(open(data_p, encoding='utf-8'))}
BASE = 'https://skills.futuremem.swiss/fr/9999_et/2000_lfe_bfs_2/'
# liens vers l'onglet « Compétences opérationnelles et critères de performance » du champ (demandé par Gael)
ANCRE_CO = {'LFB_El_DT2': 'comp%C3%A9tences-op%C3%A9rationnelles-et-crit%C3%A8res-de-performance',
            'LFB_El_Dim4': 'comp%C3%A9tences-op%C3%A9rationnelles-et-crit%C3%A8res-de-performance_1'}
from openpyxl.worksheet.hyperlink import Hyperlink
LZURL = {z['code']: z['url'] for f in data.values() for r in f['lignes'] for z in r['lz']}

# (semaine, titre, documents, périodes, champ, [LZ], remarque)
S = [
 (1, 'Matériaux semi-conducteurs : conducteur, isolant, semi-conducteur, cristal, dopage n et p, effet de la température',
  '01 Semi-conducteurs – présentation\n01 EX Semi-conducteurs + 01 EX C (corrigé)', 4, 'LFB_El_Dim4',
  ['LZ_1879', 'LZ_4066', 'LZ_4067'], 'Pratique : TM2-A1-S1 à S4 (caractéristiques résistance, Zener, diode Si)'),
 (1, 'La diode et la diode Zener : fonctionnement, caractéristique I(U), résistance dynamique',
  '02 Diode et diode Zener – présentation\n02 EX Diode et Zener + 02 EX C', 4, 'LFB_El_Dim4',
  ['LZ_5627', 'LZ_5628'], ''),
 (1, 'Circuits série résistance + diode et LED : calcul et dimensionnement de la résistance série',
  '03 Circuits avec diodes et LED – présentation\n03 EX Résistance série + 03 EX C', 4, 'LFB_El_Dim4',
  ['LZ_1894', 'LZ_9029'], 'Pratique : TM2-A2-S1 Lampe à LED'),
 (2, 'Redressement (simple et double alternance) et stabilisation par diode Zener',
  '04 Redressement et stabilisation – présentation\n04 EX Redresseur et Zener + 04 EX C', 4, 'LFB_El_Dim4',
  ['LZ_9029', 'LZ_1894'], 'Pratique : TM2-A2-S2 Redresseur, TM2-A2-S3 Zener'),
 (2, 'Optoélectronique : LED, photodiode, phototransistor, optocoupleur, taux de transfert (CTR), lecture de fiches techniques',
  '05 Optoélectronique – présentation\n05 EX Optocoupleur et fiches techniques + 05 EX C', 5, 'LFB_El_Dim4',
  ['LZ_4108', 'LZ_4109'], 'Pas de situation pratique retenue'),
 (2, 'Le transistor bipolaire en commutation (1/2) : principe, saturation, blocage',
  '06 Transistor en commutation – présentation\n06 EX Transistor interrupteur + 06 EX C', 3, 'LFB_El_Dim4',
  ['LZ_2011', 'LZ_5628'], 'Séquence 240-250 sur deux semaines (3 + 2 L). Pas de situation pratique retenue (A3 barrée)'),
 (3, 'Le transistor bipolaire en commutation (2/2) : transistor de commutation, exercices de dimensionnement',
  'Suite de 06 (même présentation et même fiche)', 2, 'LFB_El_Dim4',
  ['LZ_2011', 'LZ_5628'], 'Suite de la semaine 2'),
 (3, 'Applications des transistors : commande de relais, de LED et de moteur ; dimensionnement avec transistor bipolaire et FET',
  '07 Applications des transistors – présentation\n07 EX Dimensionner une commande + 07 EX C', 5, 'LFB_El_Dim4',
  ['LZ_2679', 'LZ_9029'], ''),
 (3, 'Montage émetteur commun : grandeurs en continu (polarisation) et comportement en alternatif',
  '08 Montage émetteur commun – présentation\n08 EX Émetteur commun + 08 EX C', 5, 'LFB_El_Dim4',
  ['LZ_4112'], ''),
 (4, 'Simulation de circuits mixtes avec diodes et transistors (logiciel de simulation)',
  '09 Simulation de circuits mixtes – guide pas à pas\n09 EX Simulation + 09 EX C (fichiers de simulation)', 4, 'LFB_El_Dim4',
  ['LZ_1949'], ''),
 (4, 'Bascules RS et D : la mémoire 1 bit',
  '10 Bascules et mémoire 1 bit – présentation\n10 EX Bascules RS et D + 10 EX C', 2, 'LFB_El_DT2',
  ['LZ_9041'], ''),
 (4, 'Bascules déclenchées sur niveau et sur front d’horloge : D, JK, T, chronogrammes',
  '11 Bascules sur niveau et sur front – présentation\n11 EX Chronogrammes + 11 EX C', 3, 'LFB_El_DT2',
  ['LZ_9042'], 'Pratique : TM2-A4-S3 Projet Horloge'),
 (4, 'Registres à décalage et circuits mémoires dans un circuit numérique',
  '12 Registres et mémoires – présentation\n12 EX Registres + 12 EX C', 3, 'LFB_El_DT2',
  ['LZ_9043'], ''),
 (5, 'Compteurs asynchrones et synchrones, modulo N',
  '13 Compteurs – présentation\n13 EX Compteurs + 13 EX C', 4, 'LFB_El_DT2',
  ['LZ_9045'], 'Pratique : TM2-A4-S3 Projet Horloge'),
 (5, 'Monostable et temporisateur (minuterie)',
  '14 Monostable et temporisateur – présentation\n14 EX Temporisations + 14 EX C', 3, 'LFB_El_DT2',
  ['LZ_9044'], 'Pas de situation pratique retenue (A4-S4 barrée)'),
 (5, 'Simulation de bascules, compteurs et monostables',
  '15 Simulation de circuits séquentiels – guide pas à pas\n15 EX Simulation + 15 EX C (fichiers de simulation)', 5, 'LFB_El_DT2',
  ['LZ_9039'], ''),
]
import re
def renumber(S):
    out, seen, k = [], {}, {}
    for s in S:
        w, titre, docs, per, champ, lz, rem = s
        m = re.match(r'(\d\d) ', docs)
        if m:
            k[w] = k.get(w, 0) + 1
            P = w * 100 + 20 * (k[w] - 1); E = P + 10
            seen[m.group(1)] = (P, E)
            l1, l2 = docs.split('\n')
            l1 = re.sub(r'^\d\d ', f'{P} ', l1)
            l2 = re.sub(r'\b\d\d EX', f'{E} EX', l2)
            docs = l1 + '\n' + l2
        else:  # suite d'une séquence commencée la semaine précédente
            P, E = seen['06']
            docs = f'Suite de {P} (présentation) et {E} EX / {E} EX C'
        out.append((w, titre, docs, per, champ, lz, rem))
    return out
S = renumber(S)
# contrôle des périodes : par champ (= FutureMEM) et par semaine
PLAN = ('LFB_El_Dim4', 'LFB_El_DT2')   # LFB_Ns_NEBA : hors planning, situation extra
for code in PLAN:
    f = data[code]
    tot = sum(s[3] for s in S if s[4] == code)
    assert tot == f['total_periodes'], (code, tot)
week = {w: sum(s[3] for s in S if s[0] == w) for w in range(1, 6)}
assert sum(week.values()) == 60 and set(week.values()) == {12}, week

wb = openpyxl.load_workbook(src)
ws = wb['PlanDeCours']
F = lambda **k: Font(name='Arial', size=11, **k)
top = Alignment(vertical='top', wrap_text=True)

# vider l'ancien corps du tableau (lignes 10 et suivantes, colonnes A à H)
for r in range(10, ws.max_row + 1):
    for c in range(1, 9):
        cell = ws.cell(r, c); cell.value = None; cell.hyperlink = None
    ws.row_dimensions[r].height = None

ws['G9'] = 'Périodes'
ws['H9'] = 'Champ d’apprentissage (FutureMEM)'
for a in ('G9', 'H9'):
    ws[a].font = F(b=True); ws[a].alignment = Alignment(vertical='center', wrap_text=True)
from openpyxl.worksheet.dimensions import ColumnDimension
ws.column_dimensions['G'] = ColumnDimension(ws, index='G', width=10)   # l'original couvrait G à XFD
ws.column_dimensions['H'] = ColumnDimension(ws, index='H', width=40)

r = 10
first_of_week = {}
for w in range(1, 7):
    rows = [s for s in S if s[0] == w] or [(6, None, None, None, None, None, None)]
    for i, s in enumerate(rows):
        ws.cell(r, 1, w).font = F(); ws.cell(r, 1).alignment = Alignment(vertical='top')
        b = ws.cell(r, 2)
        if w == 1 and i == 0:
            b.value = dt.datetime(2026, 8, 17)
        elif i == 0:
            b.value = f'=B{first_of_week[w - 1]}+7'
        else:
            b.value = f'=B{first_of_week[w]}'
        if i == 0:
            first_of_week[w] = r
        b.number_format = 'dd/mm/yyyy;@'; b.font = F(); b.alignment = Alignment(vertical='top')
        if w == 6:
            ws.cell(r, 3, 'Semaine de réserve : rattrapage d’un retard, remédiation, révision ou travail supplémentaire')
            ws.cell(r, 5, 'Situations pratiques facultatives (grisées) possibles')
        else:
            _, titre, docs, per, champ, lz, rem = s
            f = data[champ]
            ws.cell(r, 3, f'{champ} – {f["intro"]}\n{titre}')
            ws.cell(r, 4, docs)
            ws.cell(r, 5, rem or None)
            ws.cell(r, 7, per).alignment = Alignment(horizontal='center', vertical='top')
            h = ws.cell(r, 8, f'{champ} : ' + ', '.join(lz))
            h.hyperlink = Hyperlink(ref=h.coordinate, target='microsoft-edge:' + BASE, location=ANCRE_CO[champ])
            h.font = F(color='FF0563C1', underline='single')
        for c in (3, 4, 5, 6, 8):
            ws.cell(r, c).alignment = top
            if c != 8:
                ws.cell(r, c).font = F()
        r += 1
last = r - 1

# tableau Excel : même nom et même style, étendu aux colonnes G et H et aux nouvelles lignes
old = ws.tables['Tableau1']
style = old.tableStyleInfo
del ws.tables['Tableau1']
t = Table(displayName='Tableau1', ref=f'A9:H{last}')
t.tableStyleInfo = TableStyleInfo(name=style.name, showFirstColumn=style.showFirstColumn,
                                  showLastColumn=style.showLastColumn, showRowStripes=style.showRowStripes,
                                  showColumnStripes=style.showColumnStripes)
ws.add_table(t)

# totaux sous le tableau
r = last + 2
ws.cell(r, 3, 'Total des périodes (LFB_El_Dim4 + LFB_El_DT2)').font = F(b=True)
ws.cell(r, 7, f'=SUM(G10:G{last})').font = F(b=True)
ws.cell(r + 1, 3, 'Moyenne par semaine (5 semaines, semaine 6 en réserve)').font = F()
ws.cell(r + 1, 7, f'=G{r}/5').font = F(); ws.cell(r + 1, 7).number_format = '0.0'
for w in range(1, 6):
    ws.cell(r + 1 + w, 3, f'Semaine {w}').font = F()
    ws.cell(r + 1 + w, 7, f'=SUMIF(A10:A{last},{w},G10:G{last})').font = F()
for rr in range(r, r + 7):
    ws.cell(rr, 7).alignment = Alignment(horizontal='center')
ws.cell(r + 9, 3, 'LFB_Ns_NEBA (Techniques de réseau, 8 L) : hors de ce planning. Traité en situation extra (théorie + pratique), '
        'un peu chaque semaine.').font = Font(name='Arial', size=9, color='FF595959')
ws.cell(r + 9, 3).alignment = Alignment(wrap_text=True, vertical='top')
ws.cell(r + 8, 3, 'Numérotation des documents : semaine N → N00 1re présentation, N10 exercices et corrigé (N10 EX, N10 EX C), N20 2e présentation, N30 exercices, etc. '
        'Le lien de la colonne H ouvre la fiche du champ sur FutureMEM.').font = Font(name='Arial', size=9, color='FF595959')
ws.cell(r + 8, 3).alignment = Alignment(wrap_text=True, vertical='top')
wb.save(out)
print('lignes', 10, last, 'semaines', week)
