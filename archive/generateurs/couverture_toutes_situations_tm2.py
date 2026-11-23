#!/usr/bin/env python3
"""Couverture TM2 : les colonnes F à H passent à l'analyse avec TOUTES les situations (barrées comprises)
et les colonnes L à N ajoutées le 11/18/2026 sont retirées (doublon).
Usage : python3 -I couverture_toutes_situations.py in.xlsx out.xlsx"""
import sys, openpyxl
from openpyxl.styles import PatternFill, Border, Font, Alignment
from openpyxl.formatting.formatting import ConditionalFormattingList

src, out = sys.argv[1:3]
wb = openpyxl.load_workbook(src); ws = wb['Couverture TM2']
assert ws.cell(5, 12).value == 'Avec les situations barrées'
ws.cell(5, 7).value = 'Situations (barrées comprises)'

n = 0
for r in range(6, 36):
    if isinstance(ws.cell(r, 3).value, str) and ws.cell(r, 3).value.startswith('LZ_'):
        st, sits, rem = (ws.cell(r, c).value for c in (12, 13, 14))
        ws.cell(r, 6).value = st
        ws.cell(r, 7).value = sits
        ws.cell(r, 8).value = '—' if st == 'Couvert' else rem
        n += 1
assert n == 27

# retirer L à N (valeurs, styles) et la mise en forme conditionnelle de L
empty = PatternFill(fill_type=None)
for r in range(1, ws.max_row + 1):
    for c in (12, 13, 14):
        cell = ws.cell(r, c)
        if type(cell).__name__ == 'MergedCell':
            continue
        cell.value = None; cell.fill = empty; cell.border = Border(); cell.font = Font(name='Arial', size=11)
for col in ('L', 'M', 'N'):
    if col in ws.column_dimensions:
        del ws.column_dimensions[col]
keep = ConditionalFormattingList()
for cf in ws.conditional_formatting:
    if not str(cf.sqref).startswith('L'):
        for rule in cf.rules:
            keep.add(str(cf.sqref), rule)
ws.conditional_formatting = keep

# récapitulatif : retirer les colonnes I à K ajoutées
rec = next(r for r in range(36, ws.max_row + 1) if ws.cell(r, 1).value == 'Champ')
for r in range(rec, rec + 5):
    for c in (9, 10, 11):
        cell = ws.cell(r, c); cell.value = None; cell.fill = empty; cell.border = Border()

# notes : mettre à jour et retirer les deux notes du 11/18 (fusions A:N)
for rng in [m for m in ws.merged_cells.ranges if m.max_col == 14]:
    r = rng.min_row
    ws.unmerge_cells(str(rng))
    ws.cell(r, 1).value = None
    ws.row_dimensions[r].height = None
for r in range(36, ws.max_row + 1):
    if isinstance(ws.cell(r, 1).value, str) and ws.cell(r, 1).value.startswith(("Hypothèse", "Contrôle du")):
        pass
for r in range(36, ws.max_row + 1):
    v = ws.cell(r, 1).value
    if isinstance(v, str) and v.startswith('Lecture : « Partiel »'):
        ws.cell(r, 1).value = ('Lecture : « Partiel » = l’objectif est abordé par au moins une situation du programme, mais pas en entier ; '
                               'la colonne H dit ce qui manque.')
    if isinstance(v, str) and v.startswith('Situations exclues car barrées'):
        ws.cell(r, 1).value = ('Contrôle du 11/18/2026 : TOUTES les situations du programme TM2 sont prises en compte, barrées comprises '
                               '(A3-S1 à A3-S4, A4-S1, A4-S2, A4-S4, A4-S5, A4-S6). Sources : table des matières du programme TM2 et '
                               'fascicule « 10 Fascicule Module TM2 » ; seules A1-S1, A1-S2, A1-S4, A2-S1 et A2-S2 y sont rédigées, '
                               'les autres situations sont jugées sur leur titre et leurs notions.')
    if isinstance(v, str) and v.startswith('Hypothèse : le Projet Horloge'):
        ws.cell(r, 1).value = ('Hypothèse : le Projet Horloge (A4-S3) = compteurs modulo à bascules, sans simulation ni monostable. '
                               'À corriger en colonnes F à H si son cahier des charges dit autre chose.')
wb.save(out); print('lignes mises à jour :', n, '| récap ligne', rec)
