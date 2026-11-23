# -*- coding: utf-8 -*-
"""Plan de cours (onglet PlanDeCours) : met à jour les lignes d'une semaine à partir de seance.yaml (clé « plan »).

Colonnes : B programme · C ressources (lien Teams) · D remarques (LZ concernés, lien vers le premier) ·
F Floyd (chapitre, page) · G nextecmedia · H à L un objectif FutureMEM par colonne.
Liens FutureMEM : préfixe microsoft-edge: + URL complète avec l'ancre (Excel pour Windows perd l'ancre sinon ;
version validée par Gaël, ne pas séparer l'ancre dans l'attribut location). Pas de préfixe pour les liens Floyd (REGLES 6).
Cours hors réforme : pas de colonne d'objectifs, pas de lien FutureMEM (REGLES 2).
"""
import os, re
import openpyxl
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.styles import Font, Alignment

EDGE = "microsoft-edge:"
LINKF = Font(name="Arial", size=11, color="FF0563C1", underline="single")
TOP = Alignment(vertical="top", wrap_text=True)


def setlink(cell, text, url, tip=None, edge=False):
    cell.value = text
    cell.hyperlink = Hyperlink(ref=cell.coordinate, target=(EDGE + url) if edge else url, tooltip=tip)
    cell.font = LINKF; cell.alignment = TOP


def produire(S, source, sortie):
    wb = openpyxl.load_workbook(source)
    ws = wb["PlanDeCours"]
    n = 0
    for L in S.plan["lignes"]:
        r = L["ligne"]
        ws.cell(r, 2).value = L["programme"]
        setlink(ws.cell(r, 3), S.texte(L["ressources"]), S.lien(L["ressources_lien"]), L.get("ressources_bulle"))
        if S.hors_reforme:
            ws.cell(r, 4).value = L.get("remarques")
        else:
            lz = re.search(r"LZ_\d+", L["remarques"]).group(0)
            setlink(ws.cell(r, 4), L["remarques"], S.lz[lz][2], f"{lz} sur FutureMEM", edge=True)
        ft, fu = L["floyd"]
        setlink(ws.cell(r, 6), ft, S.lien(fu), "Floyd sur Teams : le lien ouvre le chapitre, aller ensuite à la page indiquée")
        nt, nu = L["nextec"]
        setlink(ws.cell(r, 7), nt, S.lien(nu), "nextecmedia, Technique numérique")
        for c in range(8, 13):
            ws.cell(r, c).value = None; ws.cell(r, c).hyperlink = None
        for i, code in enumerate([] if S.hors_reforme else L.get("objectifs", [])):
            niv, _, lurl = S.lz[code]
            setlink(ws.cell(r, 8 + i), (f"{S.champ} : " if i == 0 else "") + f"{code} ({niv})", lurl, f"{code} sur FutureMEM", edge=True)
            n += 1
        ws.row_dimensions[r].height = 44
    wb.save(sortie)
    print("ok", os.path.basename(sortie), "· liens LZ :", n)
