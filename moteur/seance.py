# -*- coding: utf-8 -*-
"""Lecture du fichier seance.yaml d'une séance et construction des liens (REGLES 2 et 6).

S = Seance("contenus/tm1/semaine-1")
S.classe, S.annee, S.matiere, S.champ, S.editeur, S.date, S.hors_reforme
S.fichier("110") → « 110 EX Familles de circuits logiques.docx »
S.lz_link("LZ_4255"), S.fm(url), S.floyd_url(3, 146), S.teams_url("110"), S.lien("floyd:3:146")
"""
import os
from urllib.parse import quote
import yaml

EDGE = "microsoft-edge:"      # Office pour Windows perd l'ancre « # » d'un lien https ; avec ce préfixe, l'URL complète arrive à Edge
GENRE = {".pptx": "p", ".docx": "w", ".xlsx": "x", ".mp4": "v", ".html": "u"}


class Seance:
    def __init__(self, dossier):
        self.dossier = os.path.abspath(dossier)
        self.d = d = yaml.safe_load(open(os.path.join(self.dossier, "seance.yaml"), encoding="utf-8"))
        manque = [k for k in ("classe", "annee", "matiere", "champ", "date", "editeur") if not d.get(k)]
        assert not manque, f"seance.yaml : il manque {', '.join(manque)} (REGLES 2 : à demander avant chaque édition)"
        self.classe, self.annee, self.matiere = str(d["classe"]), str(d["annee"]), d["matiere"]
        self.champ, self.date, self.editeur = str(d["champ"]), str(d["date"]), d["editeur"]
        self.hors_reforme = self.champ.lower() == "non"
        self.futuremem_champ = d.get("futuremem_champ")
        self.lz = {k: (v["niveau"], v["texte"], v["lien"]) for k, v in (d.get("lz") or {}).items()}
        self.floyd = {int(k): (v["lien"], v["decalage"], v["titre"]) for k, v in (d.get("floyd") or {}).items()}
        self.floyd_note = d.get("floyd_note", "")
        self.nextec = {k: (v["lien"], v["titre"]) for k, v in (d.get("nextec") or {}).items()}
        self.fichiers = {str(k): v for k, v in (d.get("fichiers") or {}).items()}
        self.versions = {str(k): str(v) for k, v in (d.get("versions") or {}).items()}
        self.artefacts = {str(k): v for k, v in (d.get("artefacts") or {}).items()}
        self.videos = {str(k): v for k, v in (d.get("videos") or {}).items()}
        self.teams_dossier = d.get("teams_dossier", "")
        self.teams_liens = {str(k): v for k, v in (d.get("teams_liens") or {}).items()}
        self.plan = d.get("plan")

    # ---------------------------------------------------------------- fichiers
    def module(self, nom):
        """Charge un fichier Python du dossier de la séance (ex. « figures » → figures.py)."""
        import importlib.util, sys
        cle = "contenu_" + os.path.basename(self.dossier).replace("-", "_") + "_" + nom.replace("-", "_")
        if cle not in sys.modules:
            spec = importlib.util.spec_from_file_location(cle, os.path.join(self.dossier, nom + ".py"))
            m = importlib.util.module_from_spec(spec); sys.modules[cle] = m; spec.loader.exec_module(m)
        return sys.modules[cle]

    def fichier(self, num):
        return self.fichiers[str(num)]

    # ---------------------------------------------------------------- liens
    def fm(self, url):
        """Lien FutureMEM avec ancre, pour un fichier Office : passe par Edge pour garder l'ancre."""
        return EDGE + url

    def lz_link(self, code):
        """Lien d'un LZ dans les présentations, les fiches et le plan : la fiche du LZ sur FutureMEM, via Edge."""
        return self.fm(self.lz[code][2])

    def floyd_url(self, chap, page=None):
        """Lien Teams du chapitre. Le lecteur PDF de Teams ignore #page= (test de Gaël, 11/16/2026) :
        le lien ouvre le chapitre, la page reste écrite dans le texte du lien."""
        return self.floyd[chap][0]

    def floyd_pdf_page(self, chap, page):
        """Page du fichier PDF pour une page imprimée du livre."""
        return page - self.floyd[chap][1]

    def teams(self, nom, genre):
        """Lien par chemin dans le dossier Teams du cours (valable une fois le fichier déposé sous ce nom)."""
        return self.teams_dossier.format(k=genre) + quote(nom) + "?csf=1&web=1"

    def teams_url(self, num):
        """Lien Teams d'un fichier de la séance : le lien « Copier le lien » s'il est connu, sinon le chemin."""
        num = str(num)
        if num in self.teams_liens:
            return self.teams_liens[num]
        nom = self.fichier(num)
        return self.teams(nom, GENRE[os.path.splitext(nom)[1]])

    def lien(self, ref):
        """« teams:110 », « floyd:3:146 », « nextec:fam », « lz:LZ_4255 » ou une URL."""
        genre, _, reste = ref.partition(":")
        if genre == "teams": return self.teams_url(reste)
        if genre == "floyd":
            chap, _, page = reste.partition(":")
            return self.floyd_url(int(chap), int(page) if page else None)
        if genre == "nextec": return self.nextec[reste][0]
        if genre == "lz": return self.lz_link(reste)
        return ref

    def texte(self, t):
        """Remplace {fichiers.<numéro>} par le nom du fichier."""
        for k, v in self.fichiers.items():
            t = t.replace("{fichiers.%s}" % k, v)
        return t

    # ---------------------------------------------------------------- données pour les présentations et les pages (JS)
    def pour_js(self, extra=None):
        data = {
            "CLASSE": self.classe, "ANNEE": self.annee, "MATIERE": self.matiere, "CHAMP": self.champ, "DATE_US": self.date,
            "HORS_REFORME": self.hors_reforme, "EDITEUR": self.editeur,
            "LZ": {k: list(v) for k, v in self.lz.items()},
            "FLOYD": {str(k): [self.floyd_url(k), v[1], v[2]] for k, v in self.floyd.items()},
            "FLOYD_PAGES": {}, "FLOYD_NOTE": self.floyd_note,
            "NEXTEC": {k: list(v) for k, v in self.nextec.items()},
            "FUTUREMEM_CHAMP": self.futuremem_champ, "EDGE": EDGE,
            "FILES": dict(self.fichiers), "TEAMS": {k: self.teams_url(k) for k in self.fichiers},
            "ART": dict(self.artefacts), "VERSIONS": dict(self.versions),
        }
        if extra:
            data.update(extra)
        return data
