#!/usr/bin/env python3
"""Couverture TM2 : ajoute la couverture avec TOUTES les situations (barrées incluses), colonnes L à N,
et les totaux correspondants dans le récapitulatif.
Usage : python3 -I maj_couverture_barrees.py in.xlsx out.xlsx"""
import sys, copy, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.dimensions import ColumnDimension

# statut avec toutes les situations, situations, commentaire (contrôle du 11/18/2026)
ALL = {
 'LZ_1879': ('Non couvert', '—', 'Aucune situation, même barrée : théorie seule.'),
 'LZ_4066': ('Non couvert', '—', 'Aucune situation, même barrée : théorie seule.'),
 'LZ_4067': ('Non couvert', '—', 'Aucune situation, même barrée : théorie seule.'),
 'LZ_2011': ('Couvert', 'A3-S1, A3-S2, A3-S3', 'Apporté par les situations A3 barrées (transistor en commutation).'),
 'LZ_4108': ('Partiel', 'A2-S1, A3-S3', 'A3-S3 (isolation galvanique) ajoute l’optocoupleur ; photodiode et phototransistor toujours absents.'),
 'LZ_4109': ('Partiel', 'A3-S3', 'Isolation galvanique dans A3-S3, mais la mesure du taux de transfert (CTR) n’est pas prévue.'),
 'LZ_5627': ('Couvert', 'A1-S2, A1-S3, A2-S2', 'Déjà couvert par les situations retenues.'),
 'LZ_5628': ('Couvert', 'A1-S2, A2-S1, A2-S3, A3-S1', 'A3-S1 ajoute le transistor de commutation.'),
 'LZ_1894': ('Couvert', 'A2-S1, A2-S3', 'Déjà couvert par les situations retenues.'),
 'LZ_2679': ('Couvert', 'A3-S1 à A3-S4, A4-S5, A4-S6', 'Apporté par les situations A3, A4-S5 et A4-S6 barrées.'),
 'LZ_4112': ('Non couvert', '—', 'Les situations A3 travaillent en commutation : l’émetteur commun en alternatif reste à la théorie.'),
 'LZ_9029': ('Partiel', 'A2-S1, A2-S2, A2-S3, A3-S1 à A3-S4', 'Transistor bipolaire et optocoupleur ajoutés par A3 ; le FET n’apparaît nulle part.'),
 'LZ_1949': ('Partiel', 'A1-S1, A2-S1, A2-S3, A3-S1 à A3-S4', 'On mesure des circuits mixtes, mais aucune situation ne simule.'),
 'LZ_9041': ('Couvert', 'A4-S2, A4-S3', 'A4-S2 (enregistreur à bascules D) apporte la mémoire 1 bit.'),
 'LZ_9042': ('Partiel', 'A4-S1, A4-S2, A4-S3', 'Bascules sur front seulement ; le déclenchement sur niveau n’est pas traité.'),
 'LZ_9043': ('Couvert', 'A4-S2, A4-S3', 'A4-S2 ajoute un second type de mémoire.'),
 'LZ_9044': ('Couvert', 'A4-S4', 'Apporté par la Minuterie de ventilation (A4-S4, barrée).'),
 'LZ_9045': ('Couvert', 'A4-S1, A4-S3', 'A4-S1 ajoute le compteur asynchrone à côté de l’Horloge.'),
 'LZ_9039': ('Non couvert', '—', 'Aucune situation ne simule. Piste : ajouter une partie simulation dans A4-S1 ou A4-S3.'),
}
for z in ['LZ_9205', 'LZ_9206', 'LZ_9207', 'LZ_9202', 'LZ_9203', 'LZ_9204', 'LZ_1362', 'LZ_9201']:
    ALL[z] = ('Non couvert', '—', 'Aucune situation réseau dans le programme TM2 : situation extra NEBA.')

src, out = sys.argv[1:3]
wb = openpyxl.load_workbook(src); ws = wb['Couverture TM2']
F = lambda **k: Font(name='Arial', size=k.pop('sz', 11), **k)
thin = Side(style='thin', color='FFA6A6A6'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
top = Alignment(vertical='top', wrap_text=True); ctr = Alignment(horizontal='center', vertical='top', wrap_text=True)

H = 5
heads = {12: 'Avec les situations barrées', 13: 'Situations (toutes, barrées incluses)',
         14: 'Ce que les situations barrées apportent / ce qui manque encore'}
for c, t in heads.items():
    cell = ws.cell(H, c, t)
    ref = ws.cell(H, 11)
    cell.font = copy.copy(ref.font); cell.fill = copy.copy(ref.fill); cell.alignment = copy.copy(ref.alignment); cell.border = box
for col, w in (('L', 16), ('M', 28), ('N', 55)):
    ws.column_dimensions[col] = ColumnDimension(ws, index=col, width=w)

rows = []
for r in range(H + 1, ws.max_row + 1):
    code = ws.cell(r, 3).value
    if isinstance(code, str) and code in ALL:
        st, sits, rem = ALL[code]
        for c, v in ((12, st), (13, sits), (14, rem)):
            cell = ws.cell(r, c, v); cell.font = F(); cell.border = box
            cell.alignment = ctr if c == 12 else top
        rows.append(r)
    elif isinstance(code, str) is False and isinstance(ws.cell(r, 1).value, str) and ws.cell(r, 1).value.startswith('LFB_') \
            and ws.cell(r, 1).fill.fill_type == 'solid' and r < (rows[-1] if rows else 10**6) + 2:
        pass
first, last = rows[0], rows[-1]
assert len(rows) == 27, len(rows)
# bandes des champs : prolonger la couleur jusqu'à N
for r in range(first - 1, last + 1):
    if r not in rows:
        band = ws.cell(r, 1)
        for c in (12, 13, 14):
            ws.cell(r, c).fill = copy.copy(band.fill); ws.cell(r, c).border = box

cf = lambda c: PatternFill(fill_type='solid', start_color=c, end_color=c, bgColor=c)
rng = f'L{first}:L{last}'
for txt, col in (('Couvert', 'FF92D050'), ('Partiel', 'FFFFC000'), ('Non couvert', 'FFFF5050')):
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'$L{first}="{txt}"'], fill=cf(col), stopIfTrue=True))

# récapitulatif : trois colonnes de plus (I à K)
rec = next(r for r in range(last, ws.max_row + 1) if ws.cell(r, 1).value == 'Champ')
for c, t in ((9, 'Couverts (avec barrées)'), (10, 'Partiels (avec barrées)'), (11, 'Non couverts (avec barrées)')):
    ref = ws.cell(rec, 8); cell = ws.cell(rec, c, t)
    cell.font = copy.copy(ref.font); cell.fill = copy.copy(ref.fill); cell.alignment = copy.copy(ref.alignment); cell.border = box
r = rec + 1
while ws.cell(r, 1).value not in (None, 'Total'):
    f_ = ws.cell(r, 3).value            # =COUNTIF(F7:F19,"Couvert")
    span = f_[f_.index('(') + 1:f_.index(',')].replace('F', 'L')
    for c, t in ((9, 'Couvert'), (10, 'Partiel'), (11, 'Non couvert')):
        cell = ws.cell(r, c, f'=COUNTIF({span},"{t}")')
        cell.font = copy.copy(ws.cell(r, 3).font); cell.alignment = copy.copy(ws.cell(r, 3).alignment); cell.border = box
    r += 1
tot = r
for c in (9, 10, 11):
    L = openpyxl.utils.get_column_letter(c); ref = ws.cell(tot, 8)
    cell = ws.cell(tot, c, f'=SUM({L}{rec + 1}:{L}{tot - 1})')
    cell.font = copy.copy(ref.font); cell.fill = copy.copy(ref.fill); cell.alignment = copy.copy(ref.alignment); cell.border = box

# notes
n = ws.max_row + 1
notes = [
 'Colonnes L à N (contrôle du 11/18/2026) : couverture si l’on reprend TOUTES les situations du programme TM2, barrées comprises. '
 'Couleurs : rouge = non couvert, orange = partiel, vert = couvert. Les colonnes F à K restent l’analyse avec les seules situations retenues.',
 'Sources : table des matières du programme TM2 (situation tm2.pdf) et fascicule « 10 Fascicule Module TM2 » ; seules A1-S1, A1-S2, A1-S4, A2-S1 et A2-S2 '
 'sont rédigées, les autres situations sont jugées sur leur titre et leurs notions.',
]
for t in notes:
    ws.cell(n, 1, t).font = F(sz=9, color='FF595959')
    ws.merge_cells(start_row=n, start_column=1, end_row=n, end_column=14)
    ws.cell(n, 1).alignment = Alignment(wrap_text=True, vertical='top'); ws.row_dimensions[n].height = 26
    n += 1
wb.save(out); print('lignes LZ', first, last, 'récap', rec, tot)
