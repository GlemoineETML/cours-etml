# -*- coding: utf-8 -*-
"""Génère tous les supports d'une séance.

Usage :
  python3 build.py tm1/semaine-1                        tout
  python3 build.py tm1/semaine-1 --seulement fiches     une partie : figures, fiches, animations, pages, presentations, plan
  python3 build.py tm1/semaine-1 --date "11/16/2026 23:04:03"   date figée (pied de page Word), pour comparer avec reference/
  python3 build.py tm1/semaine-1 --plan chemin.xlsx     classeur du plan de cours à mettre à jour (sinon : celui de reference/)
  python3 build.py tm1/semaine-1 --videos reference     reprend les vidéos de reference/ au lieu de les recalculer (3 min)
  python3 build.py tm1/semaine-1 --equations omml       équations éditables dans les présentations (image en secours)

Sorties : sortie/<matière>/<semaine>/ ; fichiers intermédiaires (figures, logos, captures) : sortie/_travail/<matière>/<semaine>/.
Ordre : charte → figures → fiches → animations → couvertures → pages → captures → présentations → plan.
"""
import argparse, datetime as dt, functools, glob, json, os, shutil, subprocess, sys

RACINE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RACINE)
from moteur import charte
from moteur.seance import Seance
from moteur.fiche import Doc
from moteur import logique, page, couverture, plan

ETAPES = ["figures", "fiches", "animations", "pages", "presentations", "plan"]


class Contexte:
    def __init__(self, seance, travail, sortie, reference, maintenant):
        self.S, self.travail, self.sortie, self.reference, self.maintenant = seance, travail, sortie, reference, maintenant
        self.images = travail
        self.base = os.path.join(travail, "etml_base.docx")
        self.doc = functools.partial(Doc, editeur=seance.editeur, base=self.base, images=self.images, maintenant=maintenant)

    def sortie_de(self, num):
        return os.path.join(self.sortie, self.S.fichier(num))


def donnees_js(ctx):
    """Données de la séance pour les présentations et les pages (JSON)."""
    S = ctx.S
    gates = logique.pour_js()
    for k, g in gates.items():
        g[11] = S.floyd_url(3, g[10]) if 3 in S.floyd else None   # lien du chapitre 3 du Floyd, s'il est dans la séance
    return S.pour_js({"GATES": gates, "ORDER": logique.ORDER, "NIV": logique.NIV,
                      "CHRONO_A": logique.CHRONO_A, "CHRONO_B": logique.CHRONO_B})


def presentations(ctx, dossier):
    S = ctx.S
    fd = os.path.join(ctx.travail, "donnees.json")
    json.dump(donnees_js(ctx), open(fd, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for f in contenus(dossier, "*.slides.js"):
        num = os.path.basename(f)[:3]
        nom = S.fichier(num)
        cfg = {"donnees": fd, "diapositives": f, "titre": nom[len(num) + 1:-5], "version": S.versions[num],
               "travail": ctx.travail, "videos": ctx.sortie, "sortie": os.path.join(ctx.sortie, nom), "equations": ctx.equations}
        fc = os.path.join(ctx.travail, f"deck_{num}.json")
        json.dump(cfg, open(fc, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        subprocess.run(["node", os.path.join(RACINE, "moteur", "deck.js"), fc], check=True)


def pages(ctx, dossier, captures=True):
    for f in contenus(dossier, "*-page.html"):
        num = os.path.basename(f)[:3]
        html = ctx.sortie_de(num)
        page.produire(ctx.S, f, f[:-5] + ".js", html, os.path.join(ctx.travail, "logo_white_h.png"), logique.pour_page())
        if captures:
            page.capture(html, os.path.join(ctx.travail, f"shot_{num}.png"))


def animations(ctx, dossier, mode):
    for f in contenus(dossier, "*-anim.py"):
        num = os.path.basename(f)[:3]
        mp4 = ctx.sortie_de(num)
        if mode == "reference":
            shutil.copyfile(os.path.join(ctx.reference, ctx.S.fichier(num)), mp4); print("repris de reference/ :", os.path.basename(mp4))
        else:
            ctx.S.module(os.path.basename(f)[:-3]).produire(ctx)


def couvertures(ctx):
    for num, duree in ctx.S.videos.items():
        mp4 = ctx.sortie_de(num)
        if os.path.exists(mp4):
            couverture.produire(mp4, os.path.join(ctx.travail, f"cover_{num}.png"), duree)


def contenus(dossier, motif):
    return sorted(glob.glob(os.path.join(dossier, motif)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seance")
    ap.add_argument("--seulement", default=",".join(ETAPES))
    ap.add_argument("--date")
    ap.add_argument("--plan")
    ap.add_argument("--videos", choices=["calculer", "reference"], default="calculer")
    ap.add_argument("--equations", choices=["image", "omml"], default="image",
                    help="équations des présentations : image (actuel) ou omml (éditables, image en secours ; à valider dans PowerPoint)")
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
    ctx.equations = a.equations

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
    if "animations" in etapes:
        animations(ctx, dossier, a.videos)
    if "animations" in etapes or "presentations" in etapes:
        couvertures(ctx)
    if "pages" in etapes:
        pages(ctx, dossier)
    if "presentations" in etapes:
        presentations(ctx, dossier)
    if "plan" in etapes and S.plan:
        source = a.plan or os.path.join(reference, S.plan["fichier"])
        plan.produire(S, source, os.path.join(sortie, S.plan["fichier"]))


if __name__ == "__main__":
    main()
