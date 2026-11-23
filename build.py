# -*- coding: utf-8 -*-
"""Génère tous les supports d'une séance.

Usage :
  python3 build.py tm1/semaine-1 --phase contenu        boucles courtes : figures, fiches, présentation provisoire (~6 s)
  python3 build.py tm1/semaine-1 --phase medias         après validation du contenu : page interactive, vidéos, présentation finale
  python3 build.py tm1/semaine-1                        tout (--phase tout)
  python3 build.py tm1/semaine-1 --seulement fiches     étapes précises : figures, fiches, pages, animations, presentations (plan : ancien workflow)
  python3 build.py tm1/semaine-1 --date "11/16/2026 23:04:03"   date figée (pied de page Word), pour comparer avec reference/
  python3 build.py tm1/semaine-1 --plan chemin.xlsx     classeur du plan de cours à mettre à jour (sinon : celui de reference/)
  python3 build.py tm1/semaine-1 --videos reference     reprend les vidéos de reference/ au lieu de les recalculer (3 min)
  python3 build.py tm1/semaine-1 --equations image      équations en image dans les présentations (par défaut : éditables, image en secours)
  python3 build.py tm1/semaine-1 --sauver               après la génération, copie la sortie dans reference/<séance>/ (à commiter)

Sorties : sortie/<matière>/<semaine>/ ; fichiers intermédiaires (figures, logos, captures) : sortie/_travail/<matière>/<semaine>/.
Ordre : charte → figures → fiches → pages et captures → vidéos et couvertures → présentations (le rapide d'abord).
Le plan de cours n'est plus écrit ici : il est une entrée (plans/, REGLES 2).
"""
import argparse, datetime as dt, functools, glob, json, os, shutil, subprocess, sys

RACINE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RACINE)
from moteur import charte
from moteur.seance import Seance
from moteur.fiche import Doc
from moteur import logique, page, couverture, plan

ETAPES = ["figures", "fiches", "pages", "animations", "presentations"]   # rapide d'abord, vidéos juste avant les présentations
PHASES = {
    "contenu": ["figures", "fiches", "presentations"],        # boucles courtes : présentation provisoire, sans vidéo ni page
    "medias": ["figures", "pages", "animations", "presentations"],    # après validation du contenu : page, artefact, vidéos, présentation finale
    "tout": ETAPES,
}


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
               "travail": ctx.travail, "videos": ctx.sortie, "sortie": os.path.join(ctx.sortie, nom), "equations": ctx.equations,
               "medias": ctx.medias}
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
    ap.add_argument("--phase", choices=list(PHASES), default="tout",
                    help="contenu : figures, fiches, plan, présentation provisoire ; medias : page, vidéos, présentation finale ; tout")
    ap.add_argument("--seulement", help="étapes précises, séparées par des virgules (remplace --phase)")
    ap.add_argument("--date")
    ap.add_argument("--plan")
    ap.add_argument("--videos", choices=["calculer", "reference"], default="calculer")
    ap.add_argument("--sauver", action="store_true",
                    help="copie la génération dans reference/<séance>/ : la dernière version livrée, gardée dans GitHub")
    ap.add_argument("--equations", choices=["image", "omml"], default="omml",
                    help="équations des présentations : omml (éditables, image en secours ; validé dans PowerPoint le 11/23/2026) ou image")
    a = ap.parse_args()
    etapes = a.seulement.split(",") if a.seulement else PHASES[a.phase]
    if a.sauver and a.phase == "contenu":
        sys.exit("--sauver : seulement pour la version finale, après la phase medias")
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
    if "plan" in etapes and S.plan:      # ancien workflow (semaine 1 TM1) : seulement avec --seulement plan, le plan vit dans plans/
        source = a.plan or os.path.join(reference, S.plan["fichier"])
        plan.produire(S, source, os.path.join(sortie, S.plan["fichier"]))
    if "pages" in etapes:
        pages(ctx, dossier)
    if "animations" in etapes:
        animations(ctx, dossier, a.videos)
    ctx.medias = a.phase != "contenu"
    if "presentations" in etapes:
        if ctx.medias:
            couvertures(ctx)
        presentations(ctx, dossier)
        if not ctx.medias:
            print("présentation provisoire : page interactive et vidéo remplacées par des emplacements (phase medias à faire)")
    if a.sauver:
        sauver(sortie, reference)
    else:
        print("rappel : génération d'essai, gardée dans sortie/ seulement. Version finale ? Demander à Gaël, "
              "puis relancer avec --sauver et commiter (REGLES 10).")


def sauver(sortie, reference):
    """Remplace le contenu de reference/<séance>/ par la génération : dernière version livrée, versionnée dans GitHub."""
    os.makedirs(reference, exist_ok=True)
    garder = {f for f in os.listdir(sortie) if os.path.isfile(os.path.join(sortie, f))}
    for f in os.listdir(reference):
        if f not in garder and os.path.isfile(os.path.join(reference, f)):
            os.remove(os.path.join(reference, f))
    for f in sorted(garder):
        shutil.copyfile(os.path.join(sortie, f), os.path.join(reference, f))
    print(f"sauvé dans {os.path.relpath(reference, RACINE)}/ : {len(garder)} fichier(s) ; à commiter")


if __name__ == "__main__":
    main()
