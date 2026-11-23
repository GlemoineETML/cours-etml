#!/usr/bin/env python3
"""Ajoute l'onglet « Couverture TM2 » au plan de cours.
Usage : python3 -I build_couverture.py plan_in.xlsx data.json build_fiche.py plan_out.xlsx"""
import sys, io, json, runpy, contextlib, datetime as dt
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.comments import Comment

src, data_p, fiche_p, out = sys.argv[1:5]
data = json.load(open(data_p, encoding='utf-8'))
# build_fiche.py lit sys.argv : on lui passe des arguments factices puis on récupère COUV
argv = sys.argv
sys.argv = [fiche_p, data_p, data_p.replace('data.json', 'co_cp.json')]
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(fiche_p)
sys.argv = argv
COUV = g['COUV']
STAT = {'OK': 'Couvert', 'PARTIEL': 'Partiel', 'NON': 'Non couvert'}
BASE = 'https://skills.futuremem.swiss/fr/9999_et/2000_lfe_bfs_2/'

NAVY, BLUE, LBLUE, TINT = 'FF242852', 'FF297FD5', 'FFACCBF9', 'FFE8EFFB'
YEL = 'FFFFF2CC'
F = lambda **k: Font(name='Arial', size=k.pop('sz', 11), **k)
fill = lambda c: PatternFill('solid', fgColor=c)
thin = Side(style='thin', color='FFA6A6A6')
box = Border(left=thin, right=thin, top=thin, bottom=thin)
top = Alignment(vertical='top', wrap_text=True)
ctr = Alignment(horizontal='center', vertical='top', wrap_text=True)

wb = openpyxl.load_workbook(src)
name = 'Couverture TM2'
if name in wb.sheetnames:
    del wb[name]
ws = wb.create_sheet(name)
ws.sheet_view.zoomScale = 90

today = dt.date(2026, 11, 16)
ws['A1'] = 'Test et Mesure 2 — couverture des objectifs d’apprentissage (théorie, exercices, situations pratiques)'
ws['A1'].font = F(b=True, sz=14, color=NAVY)
ws['A2'] = (f'Éditeur : Gaël Lemoine — {today:%m/%d/%Y}. Sources : onglet « Export 11.13.26 » (FutureMEM) et '
            'programme du module de pratique TM2 (situations non barrées seulement).')
ws['A2'].font = F(sz=9, color='FF595959')
ws['A3'] = ('À remplir (cellules jaunes) : colonne I = support de théorie et d’exercices ; colonne J = choix '
            '« Théorie seule » ou « Théorie + situation ». La colonne K se remplit seule : elle liste ce que la '
            'situation à créer doit couvrir quand on choisit « Théorie + situation » pour un objectif pas ou mal couvert.')
ws['A3'].font = F(sz=9, color='FF595959')
for r in (2, 3):
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    ws.cell(r, 1).alignment = Alignment(wrap_text=True, vertical='top')
ws.row_dimensions[3].height = 28

H = 5
heads = ['Champ', 'CO / CP (niveau, périodes)', 'LZ', 'Niv.', 'Objectif d’apprentissage (FutureMEM)',
         'Pratique TM2', 'Situations retenues', 'Ce qui manque en pratique',
         'Théorie et exercices (support)', 'Choix', 'Situation à créer — contenu à couvrir']
widths = [14, 30, 11, 9, 60, 13, 16, 48, 30, 19, 48]
for i, (h, w) in enumerate(zip(heads, widths), 1):
    c = ws.cell(H, i, h)
    c.font = F(b=True, color='FFFFFFFF'); c.fill = fill(NAVY); c.alignment = ctr; c.border = box
    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
ws.row_dimensions[H].height = 32

dv = DataValidation(type='list', formula1='"Théorie seule,Théorie + situation"', allow_blank=True,
                    showErrorMessage=True, errorTitle='Choix', error='Choisir « Théorie seule » ou « Théorie + situation ».')
ws.add_data_validation(dv)

r = H + 1
first = r
champ_rows = {}
for f in data:
    # bande du champ
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    c = ws.cell(r, 1, f"{f['code']} — {f['intro']} ({f['total_periodes']} L prévues)")
    c.font = F(b=True, color=NAVY, underline='single'); c.fill = fill(LBLUE)
    c.hyperlink = 'microsoft-edge:' + BASE + '#' + f['ancre']
    for col in range(1, 12):
        ws.cell(r, col).border = box; ws.cell(r, col).fill = fill(LBLUE)
    r += 1
    rows = []
    for ln in f['lignes']:
        cp = ln['cp'].replace('\xa0', ' ')
        for z in ln['lz']:
            st, ss, rem = COUV[z['code']]
            vals = [f['code'], f"CO {ln['co']} / CP {cp} — {ln['niveau_cible']}, {ln['periodes']} L",
                    z['code'], z['niveau'], z['texte'], STAT[st], ', '.join(ss) or '—',
                    '—' if st == 'OK' else rem, None, None]
            for col, v in enumerate(vals, 1):
                c = ws.cell(r, col, v); c.font = F(); c.alignment = top; c.border = box
            ws.cell(r, 3).hyperlink = 'microsoft-edge:' + z['url']
            ws.cell(r, 3).font = F(color=BLUE, underline='single')
            for col in (3, 4, 6):
                ws.cell(r, col).alignment = ctr
            for col in (9, 10):
                ws.cell(r, col).fill = fill(YEL)
            dv.add(f'J{r}')
            k = ws.cell(r, 11, f'=IF(AND(J{r}="Théorie + situation",F{r}<>"Couvert"),H{r},"")')
            k.font = F(color='FFC00000'); k.alignment = top; k.border = box
            rows.append(r)
            r += 1
    champ_rows[f['code']] = (rows[0], rows[-1])
last = r - 1

# couleurs du statut
# vert si couvert OU dès qu'un choix est fait en J (« Théorie seule » ou « Théorie + situation »), sinon orange / rouge.
# Mise en forme conditionnelle : Excel lit la couleur de fond dans bgColor (pas fgColor) ;
# on remplit les deux, et on garde le texte noir pour qu'il reste lisible partout.
cf = lambda c: PatternFill(fill_type='solid', start_color=c, end_color=c, bgColor=c)
rng = f'F{first}:F{last}'
ws.conditional_formatting.add(rng, FormulaRule(
    formula=[f'OR($F{first}="Couvert",$J{first}="Théorie seule",$J{first}="Théorie + situation")'], fill=cf('FF92D050'), stopIfTrue=True))
ws.conditional_formatting.add(rng, FormulaRule(
    formula=[f'$F{first}="Partiel"'], fill=cf('FFFFC000'), stopIfTrue=True))
ws.conditional_formatting.add(rng, FormulaRule(
    formula=[f'$F{first}="Non couvert"'], fill=cf('FFFF5050'), stopIfTrue=True))

# récapitulatif
r += 1
ws.cell(r, 1, 'Récapitulatif').font = F(b=True, sz=12, color=NAVY)
r += 1
rh = ['Champ', 'Objectifs (LZ)', 'Couverts', 'Partiels', 'Non couverts', 'Théorie seule', 'Théorie + situation', 'Choix à faire']
cols = [1, 2, 3, 4, 5, 6, 7, 8]
for col, h in zip(cols, rh):
    c = ws.cell(r, col, h); c.font = F(b=True, color='FFFFFFFF'); c.fill = fill(NAVY); c.alignment = ctr; c.border = box
r += 1
sr = []
for code, (a, b) in champ_rows.items():
    F_ = f'F{a}:F{b}'; J_ = f'J{a}:J{b}'
    vals = [code, f'=COUNTA(C{a}:C{b})', f'=COUNTIF({F_},"Couvert")', f'=COUNTIF({F_},"Partiel")',
            f'=COUNTIF({F_},"Non couvert")', f'=COUNTIF({J_},"Théorie seule")',
            f'=COUNTIF({J_},"Théorie + situation")', f'=B{r}-F{r}-G{r}']
    for col, v in zip(cols, vals):
        c = ws.cell(r, col, v); c.font = F(); c.alignment = ctr; c.border = box
    ws.cell(r, 1).alignment = top
    sr.append(r); r += 1
vals = ['Total'] + [f'=SUM({openpyxl.utils.get_column_letter(col)}{sr[0]}:{openpyxl.utils.get_column_letter(col)}{sr[-1]})' for col in cols[1:]]
for col, v in zip(cols, vals):
    c = ws.cell(r, col, v); c.font = F(b=True, color='FFFFFFFF'); c.fill = fill(NAVY); c.alignment = ctr; c.border = box
r += 2
notes = [
    'Couleurs de la colonne F : rouge = non couvert, orange = partiel, vert = couvert. Une ligne passe aussi au vert dès qu’un choix est fait en colonne J (« Théorie seule » ou « Théorie + situation ») : l’objectif est alors pris en charge.',
    'Lecture : « Partiel » = l’objectif est abordé par une situation retenue mais pas en entier ; la colonne H dit ce qui manque.',
    'Tous les objectifs doivent être couverts en théorie (cours + exercices). Le choix porte seulement sur l’ajout d’une situation pratique.',
    'Hypothèse : le Projet Horloge (A4-S3) = compteurs modulo à bascules, sans simulation ni monostable. À corriger en colonnes F à H si son cahier des charges dit autre chose.',
    'Situations exclues car barrées : A3-S1 à A3-S4 (transistors, moteur, isolation galvanique), A4-S1, A4-S2, A4-S4, A4-S5, A4-S6. Situations facultatives (grisées) : A1-S3, A1-S4.',
]
for t in notes:
    ws.cell(r, 1, t).font = F(sz=9, color='FF595959')
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    ws.cell(r, 1).alignment = Alignment(wrap_text=True, vertical='top')
    r += 1

ws.freeze_panes = f"D{H + 1}"
ws.auto_filter.ref = f'A{H}:K{last}'
ws.print_title_rows = f'{H}:{H}'
ws.page_setup.orientation = 'landscape'
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.sheet_properties.tabColor = '297FD5'
wb.save(out)
print('lignes LZ', first, last)
