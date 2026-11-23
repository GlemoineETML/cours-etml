#!/usr/bin/env python3
"""PlanDeCours : un lien par objectif (fiche LZ sur FutureMEM), colonnes H à J.
Usage : python3 -I maj_liens_lz.py in.xlsx data.json out.xlsx"""
import sys, json, re, copy, openpyxl
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Font, Alignment
src, data_p, out = sys.argv[1:4]
LZ = {z['code']: z for f in json.load(open(data_p, encoding='utf-8')) for r in f['lignes'] for z in r['lz']}
wb = openpyxl.load_workbook(src); ws = wb['PlanDeCours']
hdr = ws['H9']
heads = {8: 'Objectif FutureMEM 1', 9: 'Objectif FutureMEM 2', 10: 'Objectif FutureMEM 3'}
for c, t in heads.items():
    cell = ws.cell(9, c, t); cell.font = copy.copy(hdr.font); cell.alignment = copy.copy(hdr.alignment)
for col, w in (('H', 26), ('I', 22), ('J', 22)):
    ws.column_dimensions[col] = ColumnDimension(ws, index=col, width=w)
last = max(t.ref for t in ws.tables.values()).split(':')[1]
last_row = int(re.sub(r'\D', '', last))
n = 0
for r in range(10, last_row + 1):
    v = ws.cell(r, 8).value
    if not (isinstance(v, str) and ' : ' in v):
        continue
    champ, codes = v.split(' : ')
    codes = [c.strip() for c in codes.split(',')]
    for i in range(3):
        cell = ws.cell(r, 8 + i); cell.hyperlink = None; cell.value = None
        if i < len(codes):
            z = LZ[codes[i]]
            url, anc = z['url'].split('#')
            cell.value = (f'{champ} : ' if i == 0 else '') + f"{z['code']} ({z['niveau']})"
            cell.hyperlink = Hyperlink(ref=cell.coordinate, target='microsoft-edge:' + url, location=anc)
            cell.font = Font(name='Arial', size=11, color='FF0563C1', underline='single')
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            n += 1
old = list(ws.tables.values())[0]; st = old.tableStyleInfo; name = old.displayName
del ws.tables[old.name]
t = Table(displayName=name, ref=f'A9:J{last_row}')
t.tableStyleInfo = TableStyleInfo(name=st.name, showFirstColumn=st.showFirstColumn, showLastColumn=st.showLastColumn,
                                  showRowStripes=st.showRowStripes, showColumnStripes=st.showColumnStripes)
ws.add_table(t)
# note sous le tableau
for r in range(last_row + 1, ws.max_row + 1):
    v = ws.cell(r, 3).value
    if isinstance(v, str) and 'Le lien de la colonne H' in v:
        ws.cell(r, 3).value = v.replace('Le lien de la colonne H ouvre la fiche du champ sur FutureMEM.',
                                        'Les colonnes H à J ouvrent la fiche de chaque objectif (LZ) sur FutureMEM.')
wb.save(out); print('liens LZ :', n, 'tableau A9:J%d' % last_row)
