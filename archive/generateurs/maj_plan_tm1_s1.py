# -*- coding: utf-8 -*-
"""Plan de cours TM1 (onglet PlanDeCours), semaine 1, à partir du classeur de Gaël (src.xlsx).
Semaine 1 en 4 lignes, dans l'ordre du cours (demande de Gaël, 11/16/2026) :
  1. présentation 100 (animation 105 intégrée) + page interactive 101
  2. fiche d'exercices 110 EX (+ corrigé)
  3. présentation 120 (animation 125 intégrée) + page interactive 121
  4. fiche d'exercices 130 EX (+ corrigé)
Colonne D « Remarques » : les LZ concernés, notés comme dans les autres semaines (« LZ_4255 p4 + LZ_4256 »).
L'ancienne 5e ligne de la semaine 1 est supprimée ; les semaines suivantes remontent d'une ligne (hauteurs et liens suivis).
Colonnes F (Floyd), G (nextecmedia), H à L (un objectif FutureMEM par colonne).
Liens FutureMEM : préfixe microsoft-edge: + URL complète avec l'ancre (Excel pour Windows perd l'ancre sinon ;
version validée par Gaël, ne pas séparer l'ancre dans l'attribut location).
Usage : python3 -I maj_plan_tm1_s1.py entree.xlsx sortie.xlsx"""
import os, sys, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.styles import Font, Alignment
import w1_data as D

src, out = sys.argv[1:3]
EDGE = "microsoft-edge:"
wb = openpyxl.load_workbook(src)
ws = wb["PlanDeCours"]
LINKF = Font(name="Arial", size=11, color="FF0563C1", underline="single")
TOP = Alignment(vertical="top", wrap_text=True)


def setlink(cell, text, url, tip=None, edge=False):
    cell.value = text
    cell.hyperlink = Hyperlink(ref=cell.coordinate, target=(EDGE + url) if edge else url, tooltip=tip)
    cell.font = LINKF; cell.alignment = TOP


# ---------------------------------------------------------------- semaine 1 : 5 lignes → 4 (suppression de la 5e)
assert str(ws["A14"].value) == "1" and str(ws["A15"].value) == "2", "le classeur source n'a plus la semaine 1 en lignes 10 à 14"
old = ws.tables["Tableau1"]; st = old.tableStyleInfo
last_row = int("".join(ch for ch in old.ref.split(":")[1] if ch.isdigit())) - 1
heights = {r: ws.row_dimensions[r].height for r in range(1, ws.max_row + 3)}
ws.delete_rows(14, 1)
for r in range(14, ws.max_row + 2):          # openpyxl ne déplace pas les hauteurs de ligne
    ws.row_dimensions[r].height = heights.get(r + 1)
for row in ws.iter_rows():                    # ni la référence des liens
    for c in row:
        if c.hyperlink is not None:
            c.hyperlink.ref = c.coordinate

# ---------------------------------------------------------------- en-têtes F à L
hdr = ws["E9"]
heads = {6: "Floyd (chapitre, page)", 7: "nextecmedia", 8: "Objectif FutureMEM 1", 9: "Objectif FutureMEM 2", 10: "Objectif FutureMEM 3",
         11: "Objectif FutureMEM 4", 12: "Objectif FutureMEM 5"}
for c, t in heads.items():
    cell = ws.cell(9, c, t); cell.font = copy.copy(hdr.font); cell.alignment = copy.copy(hdr.alignment)
for col, w in (("F", 30), ("G", 30), ("H", 26), ("I", 18), ("J", 18), ("K", 18), ("L", 18)):
    ws.column_dimensions[col] = ColumnDimension(ws, index=col, width=w)

# ---------------------------------------------------------------- lignes de la semaine 1
LZ_FAM = "LZ_4255 p4 + LZ_4256"
LZ_PORTES = "LZ_4242 p8 + LZ_130 + LZ_27 + LZ_29 p20 + LZ_2223 p6"
W1 = [
    # ligne, programme, (ressources, lien, info-bulle), (remarques, LZ du lien), Floyd, nextecmedia, objectifs H → L
    (10, "- Niveaux numériques et familles de circuits logiques",
     (f"{D.F100} (v1.3, animation 105 intégrée)\n{D.F101} (page interactive)", D.TEAMS_100, "Présentation 100 sur Teams"),
     (LZ_FAM, "LZ_4255"), ("chap. 3, 3-8 Logique à fonction fixe (p. 146)", D.floyd_url(3, 146)),
     ("4.1 Familles de circuits", D.NEXTEC["fam"][0]), ["LZ_4255", "LZ_4256"]),
    (11, "- Niveaux numériques et familles de circuits logiques : exercices",
     (f"{D.F110}\n{D.F110C}", D.teams(D.F110, "w"), "Fiche d'exercices 110 EX sur Teams (dossier El_DT1/PMT&SBT)"),
     (LZ_FAM, "LZ_4255"), ("chap. 3, 3-8 Niveaux logiques (p. 154)", D.floyd_url(3, 154)),
     ("4.1 Familles de circuits", D.NEXTEC["fam"][0]), ["LZ_4255", "LZ_4256"]),
    (12, "- Table de vérité et portes logiques",
     (f"{D.F120} (v1.2, animation 125 intégrée)\n{D.F121} (page interactive)", D.teams(D.F120, "p"), "Présentation 120 sur Teams (dossier El_DT1/PMT&SBT)"),
     (LZ_PORTES, "LZ_4242"), ("chap. 3, 3-1 à 3-6 Portes logiques (p. 112)", D.floyd_url(3, 112)),
     ("1.2.1 Formes de représentation", D.NEXTEC["repr"][0]), ["LZ_4242", "LZ_130", "LZ_27", "LZ_29", "LZ_2223"]),
    (13, "- Table de vérité et portes logiques : exercices",
     (f"{D.F130}\n{D.F130C}", D.teams(D.F130, "w"), "Fiche d'exercices 130 EX sur Teams (dossier El_DT1/PMT&SBT)"),
     (LZ_PORTES, "LZ_4242"), ("chap. 3, 3-8 CI de la série 74 (p. 146)", D.floyd_url(3, 146)),
     ("1.1 Introduction à la technique numérique", D.NEXTEC["intro"][0]), ["LZ_4242", "LZ_130", "LZ_27", "LZ_29", "LZ_2223"]),
]
n = 0
for r, prog, (res, url, tip), (rem, lzr), (ft, fu), (nt, nu), objs in W1:
    ws.cell(r, 2).value = prog
    setlink(ws.cell(r, 3), res, url, tip)
    setlink(ws.cell(r, 4), rem, D.LZ[lzr][2], f"{lzr} sur FutureMEM", edge=True)
    setlink(ws.cell(r, 6), ft, fu, "Floyd sur Teams : le lien ouvre le chapitre, aller ensuite à la page indiquée")
    setlink(ws.cell(r, 7), nt, nu, "nextecmedia, Technique numérique")
    for c in range(8, 13):
        ws.cell(r, c).value = None; ws.cell(r, c).hyperlink = None
    for i, code in enumerate(objs):
        niv, _, lurl = D.LZ[code]
        setlink(ws.cell(r, 8 + i), (f"{D.CHAMP} : " if i == 0 else "") + f"{code} ({niv})", lurl, f"{code} sur FutureMEM", edge=True)
        n += 1
    ws.row_dimensions[r].height = 44

# ---------------------------------------------------------------- tableau étendu à L
del ws.tables["Tableau1"]
t = Table(displayName="Tableau1", ref=f"A9:L{last_row}")
t.tableStyleInfo = TableStyleInfo(name=st.name, showFirstColumn=st.showFirstColumn, showLastColumn=st.showLastColumn,
                                  showRowStripes=st.showRowStripes, showColumnStripes=st.showColumnStripes)
ws.add_table(t)
note = ws.cell(last_row + 2, 3, "Semaine 1, dans l'ordre du cours : présentation 100 et page interactive 101, fiche 110 EX, présentation 120 et page "
                                "interactive 121, fiche 130 EX (les animations 105 et 125 sont intégrées aux présentations). Remarques : les LZ concernés. "
                                "Colonnes F à L : liens Floyd (chapitre et page), nextecmedia et un objectif FutureMEM par colonne. Les liens FutureMEM "
                                "commencent par microsoft-edge: pour garder l'ancre. Les liens Floyd ouvrent le chapitre (le lecteur PDF de Teams ignore "
                                "les numéros de page ; chap. 3 : page du livre − 110 = page du PDF). Les liens des présentations et des fiches visent le "
                                "dossier El_DT1/PMT&SBT : ils fonctionnent une fois les fichiers déposés sous ces noms.")
note.font = Font(name="Arial", size=9, italic=True, color="FF595959"); note.alignment = TOP
ws.merge_cells(start_row=last_row + 2, start_column=3, end_row=last_row + 2, end_column=8)
ws.row_dimensions[last_row + 2].height = 60
wb.save(out)
print("liens LZ :", n, "· tableau A9:L%d" % last_row)
