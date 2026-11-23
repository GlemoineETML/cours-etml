#!/usr/bin/env python3
"""Construit l'onglet « Export MM.JJ.AA » du plan de cours à partir de data.json (extract_futuremem.py).
Usage : python3 -I build_export.py classeur_entree.xlsx data.json classeur_sortie.xlsx [MM/JJ/AAAA]
Remplace un onglet « Export ... » existant ; laisse les autres onglets intacts.
"""
import sys, json, math, datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.utils import get_column_letter

src, dj, dst = sys.argv[1:4]
date = datetime.datetime.strptime(sys.argv[4], '%m/%d/%Y') if len(sys.argv) > 4 else datetime.date.today()
data = json.load(open(dj, encoding='utf-8'))

NAVY, BLUE, LIGHT, WHITE = 'FF242852', 'FF297FD5', 'FFACCBF9', 'FFFFFFFF'
EDGE = 'microsoft-edge:'          # Excel Windows perd l'ancre « # » sans ce préfixe (validé par Gaël)
M = Side(style='medium', color='FF000000')
NB = '\xa0'
f_norm = Font(name='Arial', size=11)
f_bold = Font(name='Arial', size=11, bold=True)
f_head = Font(name='Arial', size=11, bold=True, color=WHITE)
f_band = Font(name='Arial', size=11, bold=True, color=NAVY, underline='single')
f_note = Font(name='Arial', size=9, italic=True, color='FF595959')
fill_w = PatternFill('solid', fgColor=WHITE)
fill_n = PatternFill('solid', fgColor=NAVY)
fill_l = PatternFill('solid', fgColor=LIGHT)
top = Alignment(vertical='top', wrap_text=True)
LINK = InlineFont(rFont='Arial', sz=11, color=BLUE, u='single')
PLAIN = InlineFont(rFont='Arial', sz=11)

wb = openpyxl.load_workbook(src, rich_text=True)
for n in [s for s in wb.sheetnames if s.startswith('Export')]:
    del wb[n]
e = wb.create_sheet(f"Export {date:%m.%d.%y}")
WID = {'A': 38.3, 'B': 64.9, 'C': 60.1, 'D': 12.0, 'E': 70.0, 'F': 45.0, 'G': 62.0}
for k, v in WID.items():
    e.column_dimensions[k].width = v

def box(c, l=True, r=True, t=True, b=True):
    c.border = Border(left=M if l else None, right=M if r else None, top=M if t else None, bottom=M if b else None)

def link(c, url, tip):
    c.hyperlink = Hyperlink(ref=c.coordinate, target=EDGE + url, tooltip=tip)

def rich(c, code, prefix='', suffix=''):
    parts = ([TextBlock(PLAIN, prefix)] if prefix else []) + [TextBlock(LINK, code)] + ([TextBlock(PLAIN, suffix)] if suffix else [])
    c.value = CellRichText(parts)

heads = ['Lien', 'Objectifs d’apprentissage', 'Connaissances opérationnelles nécessaires', 'Périodes',
         'Didactique', 'Contrôles de compétence', 'Situation de travail et d’action typique']
for i, h in enumerate(heads, 1):
    c = e.cell(1, i, h); c.font = f_head; c.fill = fill_n; c.alignment = top; box(c)

def txt_didactique(f):
    out = []
    for d in f['didactique']:
        lab = d['approche'][0].upper() + d['approche'][1:]
        lines = [f'• {s} : {v}' for s, v in d['etapes'] if v.strip() not in ('', '-')]
        out.append(lab + '\n' + ('\n'.join(lines) if lines else '• (aucune indication sur le site)'))
    return '\n\n'.join(out)

def txt_controles(f):
    return '\n\n'.join(f"{i}. {c['nom'][0].upper()+c['nom'][1:]}\n{c['description']}" for i, c in enumerate(f['controles'], 1))

def txt_situation(f):
    s = f['situation']
    body, cond = (s.split('Conditions:', 1) if 'Conditions:' in s else (s.rstrip(' -'), ' -'))
    return body.strip() + '\n\nConditions : ' + cond.strip()

r = 2
totals = []
for f in data:
    page_url = f"{f['page_url']}#{f['ancre']}"
    band = e.cell(r, 1, f"{f['code']} – {f['intro']} ({f['total_periodes']} L prévues)")
    e.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    for col in range(1, 8):
        e.cell(r, col).fill = fill_l
    band.font = f_band; band.alignment = top
    link(band, page_url, 'Ouvrir le champ sur FutureMEM')
    r += 1
    first, anchors = r, []
    for row in f['lignes']:
        n = len(row['lz']); h = max(3, 2 * n - 1); r0, r1 = r, r + h - 1
        anchors.append(r0)
        for rr in range(r0, r1 + 1):
            for col in range(1, 5):
                c = e.cell(rr, col); c.fill = fill_w; c.font = f_norm; c.alignment = top
            box(e.cell(rr, 1), t=(rr == r0), b=(rr == r1))
            box(e.cell(rr, 2), l=False, t=(rr == r0), b=(rr == r1))
        a = e.cell(r0, 1); rich(a, row['co'], f'CO:{NB}{NB}'); link(a, row['co_url'], f"CO {row['co']} sur FutureMEM")
        a = e.cell(r0 + 1, 1); rich(a, row['cp'], f'CP:{NB}{NB}'); link(a, row['cp_url'], f"CP {row['cp']} sur FutureMEM")
        e.cell(r0 + 2, 1, f"Niveau cible:{NB}{row['niveau_cible']}")
        for i, lz in enumerate(row['lz']):
            b = e.cell(r0 + 2 * i, 2)
            rich(b, lz['code'], '', f" - {lz['niveau']} - {lz['texte']}")
            link(b, lz['url'], f"{lz['code']} sur FutureMEM")
        c = e.cell(r0, 3, ' ; '.join(row['connaissances']))
        e.merge_cells(start_row=r0, start_column=3, end_row=r1, end_column=3)
        d = e.cell(r0, 4, row['periodes']); d.number_format = '0" L"'
        d.alignment = Alignment(horizontal='center', vertical='top')
        e.merge_cells(start_row=r0, start_column=4, end_row=r1, end_column=4)
        for rr in range(r0, r1 + 1):
            box(e.cell(rr, 3), r=False, t=(rr == r0), b=(rr == r1)); box(e.cell(rr, 4), t=(rr == r0), b=(rr == r1))
        r = r1 + 1
    last = r - 1
    for col, txt in ((5, txt_didactique(f)), (6, txt_controles(f)), (7, txt_situation(f))):
        for rr in range(first, last + 1):
            c = e.cell(rr, col); c.fill = fill_w; box(c)
        c = e.cell(first, col, txt); c.font = f_norm; c.alignment = top
        e.merge_cells(start_row=first, start_column=col, end_row=last, end_column=col)
    t = e.cell(r, 1, f"Total {f['code']}"); t.font = f_bold
    t.alignment = Alignment(horizontal='right', vertical='top')
    e.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    d = e.cell(r, 4, '=SUM(' + ','.join(f'D{x}' for x in anchors) + ')')
    d.font = f_bold; d.number_format = '0" L"'; d.alignment = Alignment(horizontal='center', vertical='top')
    for col in range(1, 8):
        c = e.cell(r, col); c.fill = fill_w; box(c, l=(col != 2 and col != 3), r=(col not in (1, 2)))
    totals.append(r); r += 1
# grand total
g = e.cell(r, 1, 'Total des périodes'); e.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
g.alignment = Alignment(horizontal='right', vertical='top')
d = e.cell(r, 4, '=SUM(' + ','.join(f'D{x}' for x in totals) + ')'); d.number_format = '0" L"'
for col in range(1, 8):
    c = e.cell(r, col); c.fill = fill_n; c.font = f_head; box(c, l=(col not in (2, 3)), r=(col not in (1, 2)))
grand = r
notes = [
    f"Source : {data[0]['page_url']} (plan de formation Électronicien/ne CFC, champs d'apprentissage école "
    f"professionnelle), consulté le {date:%m/%d/%Y}.",
    "Éditeur : Gaël Lemoine. Les liens (bandes bleu clair, CO, CP, LZ) ouvrent la fiche correspondante sur le site, "
    "via Microsoft Edge (préfixe microsoft-edge: pour garder l’ancre).",
    "Colonnes E à G : onglets « Didactique », « Contrôles de compétence » et « Situations de travail et d’action "
    "typiques » de chaque champ, repris du site tels quels. Les étapes didactiques notées « - » sont omises.",
]
for i, n in enumerate(notes):
    c = e.cell(grand + 2 + i, 1, n); c.font = f_note; c.alignment = top
    e.merge_cells(start_row=grand + 2 + i, start_column=1, end_row=grand + 2 + i, end_column=7)
link(e.cell(grand + 2, 1), data[0]['page_url'], 'Page FutureMEM')

# hauteurs de ligne : Arial 11 ≈ 15 pt par ligne ; les blocs fusionnés agrandissent leurs lignes
def nlines(text, col):
    cpl = WID[col] * 1.05
    return sum(max(1, math.ceil(len(p) / cpl)) for p in str(text).split('\n'))
merged = list(e.merged_cells.ranges)
inm = {(rr, cc) for m in merged for rr in range(m.min_row, m.max_row + 1) for cc in range(m.min_col, m.max_col + 1)}
H = {}
for rr in range(1, grand + 1):
    need = 1
    for cc in range(1, 8):
        v = e.cell(rr, cc).value
        if v is None or (rr, cc) in inm or str(v).startswith('='):
            continue
        need = max(need, nlines(v, get_column_letter(cc)))
    H[rr] = need * 15 + 4
for m in sorted(merged, key=lambda m: m.max_row - m.min_row):
    if m.min_row == m.max_row or m.max_row > grand:
        continue
    v = e.cell(m.min_row, m.min_col).value
    if not v:
        continue
    need = nlines(v, get_column_letter(m.min_col)) * 15 + 8
    rows = range(m.min_row, m.max_row + 1)
    have = sum(H[x] for x in rows)
    if need > have:
        for x in rows:
            H[x] += (need - have) / len(rows)
for rr, v in H.items():
    e.row_dimensions[rr].height = round(v, 1)
for rr in range(grand + 2, grand + 2 + len(notes)):
    e.row_dimensions[rr].height = 26

e.freeze_panes = 'A2'
e.page_setup.paperSize = e.PAPERSIZE_A3
e.page_setup.orientation = 'landscape'
e.sheet_properties.pageSetUpPr.fitToPage = True
e.page_setup.fitToWidth, e.page_setup.fitToHeight = 1, 0
wb.save(dst)
print(json.dumps({'onglet': e.title, 'lignes': grand, 'LZ': sum(len(r['lz']) for f in data for r in f['lignes']),
                  'periodes': sum(f['total_periodes'] for f in data)}, ensure_ascii=False))
