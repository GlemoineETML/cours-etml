# -*- coding: utf-8 -*-
"""Génère tous les supports d'une séance.

Usage :
  python3 build.py tm1/semaine-1                        tout
  python3 build.py tm1/semaine-1 --seulement fiches     une partie : figures, fiches, animations, pages, presentations, plan
  python3 build.py tm1/semaine-1 --date "11/16/2026 23:04:03"   date figée (pied de page Word), pour comparer avec reference/
  python3 build.py tm1/semaine-1 --plan chemin.xlsx     classeur du plan de cours à mettre à jour (sinon : celui de reference/)
  python3 build.py tm1/semaine-1 --videos reference     reprend les vidéos de reference/ au lieu de les recalculer (long)

Sorties : sortie/<matière>/<semaine>/ ; fichiers intermédiaires (figures, logos, captures) : sortie/_travail/<matière>/<semaine>/.
Ordre : charte → figures → fiches → animations → couvertures → pages → captures → présentations → plan.
"""
import argparse, datetime as dt, functools, glob, os, shutil, subprocess, sys

RACINE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RACINE)
from moteur import charte
from moteur.seance import Seance
from moteur.fiche import Doc

ETAPES = ["figures", "fiches", "animations", "pages", "presentations", "plan"]


class Contexte:
    def __init__(self, seance, travail, sortie, reference, maintenant):
        self.S, self.travail, self.sortie, self.reference, self.maintenant = seance, travail, sortie, reference, maintenant
        self.images = travail
        self.base = os.path.join(travail, "etml_base.docx")
        self.doc = functools.partial(Doc, editeur=seance.editeur, base=self.base, images=self.images, maintenant=maintenant)

    def sortie_de(self, num):
        return os.path.join(self.sortie, self.S.fichier(num))


def contenus(dossier, motif):
    return sorted(glob.glob(os.path.join(dossier, motif)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seance")
    ap.add_argument("--seulement", default=",".join(ETAPES))
    ap.add_argument("--date")
    ap.add_argument("--plan")
    ap.add_argument("--videos", choices=["calculer", "reference"], default="calculer")
    a = ap.parse_args()
    etapes = a.seulement.split(",")
    dossier = os.path.join(RACINE, "contenus", a.seance)
    S = Seance(dossier)
    travail = os.path.join(RACINE, "sortie", "_travail", a.seance)
    sortie = os.path.join(RACINE, "sortie", a.seance)
    reference = os.path.join(RACINE, "reference", a.seance)
    os.makedirs(sortie, exist_ok=True)
    maintenant = dt.datetime.strptime(a.date, "%m/%d/%Y %H:%M:%S") if a.date else None
    ctx = Contexte(S, travail, sortie, reference, maintenant)

    charte.prepare(travail)
    for f in contenus(os.path.join(dossier, "images"), "*.*"):
        if not f.endswith(".md"):
            shutil.copyfile(f, os.path.join(travail, os.path.basename(f)))

    if "figures" in etapes or "presentations" in etapes or "fiches" in etapes:
        if os.path.exists(os.path.join(dossier, "figures.py")):
            S.module("figures").produire(ctx); print("figures ok")
    if "fiches" in etapes:
        for f in contenus(dossier, "*-ex.py"):
            S.module(os.path.basename(f)[:-3]).produire(ctx)


if __name__ == "__main__":
    main()
