# -*- coding: utf-8 -*-
"""Données communes semaine 1 (TM1 – El DT 1) : références, portes logiques, valeurs des familles.
Une seule source pour les présentations 100 et 120 et les fiches 110 et 130."""
import json

CLASSE, ANNEE = "XLO1", "2026-2027"
MATIERE = "Test et Mesure 1 – El DT 1"
CHAMP = "LFB_El_DT1"
DATE_US = "11/16/2026"
EDITEUR = "Gaël Lemoine"

# ---------------------------------------------------------------- références
# Champ LFB_El_DT1 : page Semestre 1, onglet « Compétences opérationnelles et critères de performance » du champ (lien donné par Gaël
# le 11/16/2026). Chaque LZ a son propre lien (LZ[code][2]), confirmé par Gaël dans la feuille « Liens FutureMEM à fournir »
# (https://claude.ai/artifact/HGXbgDTE9qMZbPMj7BaMXj) le 11/16/2026.
FUTUREMEM_CHAMP = "https://skills.futuremem.swiss/fr/9999_et/2000_lfe_bfs_1/#comp%C3%A9tences-op%C3%A9rationnelles-et-crit%C3%A8res-de-performance"
# Office pour Windows (Excel, PowerPoint, Word) perd l'ancre « # » d'un lien https et ouvre la page FutureMEM en haut,
# donc sur le mauvais LZ (test de Gaël le 11/16/2026 dans PowerPoint et Word). Avec ce préfixe, l'URL complète arrive à Edge.
EDGE = "microsoft-edge:"


def fm(url):
    """Lien FutureMEM avec ancre, pour un fichier Office : passe par Edge pour garder l'ancre."""
    return EDGE + url


def lz_link(code):
    """Lien d'un LZ dans les présentations et les fiches : la fiche du LZ sur FutureMEM (lien donné par Gaël), via Edge."""
    return fm(LZ[code][2])
LZ = {   # code : (niveau, texte FutureMEM, lien exact relevé sur le site le 11/16/2026)
    "LZ_4255": ("C2", "Elles/Ils expliquent les niveaux numériques des familles de circuits logiques.",
                "https://skills.futuremem.swiss/fr/data/5000_lze_06/#232E8605-34F5-E24F-B206-CD3364F81EDB"),
    "LZ_4256": ("C1", "Elles/Ils citent les principales caractéristiques des familles actuelles de circuits logiques.",
                "https://skills.futuremem.swiss/fr/data/5000_lze_06/#C02F8B2C-E8DE-4B46-AFCF-136FB03F2EA6"),
    "LZ_4242": ("C3", "Elles/Ils dessinent des tables de vérité avec des variables d’entrée et de sortie.",
                "https://skills.futuremem.swiss/fr/data/5000_lze_06/#110D829B-238F-A646-BDF0-DA72F7DA82A6"),
    "LZ_2223": ("C1", "Elles/Ils citent des exemples de circuits intégrés tels que AND, OR, NOT.",
                "https://skills.futuremem.swiss/fr/data/5000_lze_04/#33DAE379-F86D-8949-BD47-E29587F2C195"),
    "LZ_130": ("C2", "Elles/Ils décrivent les portes logiques de base ET, OU, NON, NAND, NOR et connaissent leurs symboles.",
               "https://skills.futuremem.swiss/fr/data/5000_lze_01/#DCBD89FD-6D4A-5441-B4BC-4072FFACB3DC"),
    "LZ_27": ("C3", "Elles/Ils établissent la relation entre l'équation fonctionnelle, le tableau de valeurs et la représentation graphique d’une fonction.",
              "https://skills.futuremem.swiss/fr/data/5000_lze_00/#B73C7F1A-B86E-3C4F-9F00-D542352FC3CA"),
    "LZ_29": ("C4", "Elles/Ils différencient les fonctions logiques de base au moyen du symbole, de la table de vérité, de l'équation logique et du chronogramme.",
              "https://skills.futuremem.swiss/fr/data/5000_lze_00/#D3224C49-3D75-6549-B901-FF9677C3C301"),
}
_FDIR = ("https://eduvaud.sharepoint.com/:b:/r/sites/msteams_76c9d9/Documents%20partages/Documentation/"
         "Electronique%20num%C3%A9rique%20TMLO/10%20Floyd%20V11/10%20Floyd%20V11%20Basse%20d%C3%A9finition%20par%20chapitre/")
FLOYD = {   # chapitre : (lien Teams « Copier le lien », décalage page imprimée → page du PDF, titre) ; liens ch. 1 et 3 fournis par Gaël le 11/16/2026
    1: (_FDIR + "Chap%2001%20-%20Concepts%20num%C3%A9riques.pdf?d=w098062972a294c8d9838cc4a50cb26fa&csf=1&web=1&e=gBoXeN", 0, "chap. 1 Concepts numériques"),
    2: (_FDIR + "Chap%2002%20-%20Syst%C3%A8mes%20de%20num%C3%A9ration,%20op%C3%A9rations%20et%20codes.pdf?d=w933f2237d1814185b6a6b02be82abe0b&csf=1&web=1&e=eHqofE", 50,
        "chap. 2 Systèmes de numération, opérations et codes"),
    3: (_FDIR + "Chap%2003%20-%20Portes%20logiques.pdf?d=w0b4d71190cd446b9af28ab8cc4e69272&csf=1&web=1&e=O8tdfS", 110, "chap. 3 Portes logiques"),
}


def floyd_url(chap, page=None):
    """Lien Teams du chapitre. Test du 11/16/2026 (Gaël, depuis PowerPoint) : le lecteur PDF de Teams/SharePoint ignore #page=
    (ch. 3 #page=5 → p. 116-117, ch. 1 #page=26 → p. 3-4). Le lien ouvre donc le chapitre ; la page reste écrite dans le texte du lien."""
    return FLOYD[chap][0]


def floyd_pdf_page(chap, page):
    """Page du fichier PDF pour une page imprimée du livre (à taper dans le lecteur)."""
    return page - FLOYD[chap][1]


FLOYD_NOTE = ("le lien ouvre le chapitre sur Teams ; tape ensuite la page dans le lecteur PDF. "
              "Chap. 3 : page du livre − 110 = page du PDF (p. 115 → 5). Chap. 1 : mêmes numéros.")


NEXTEC = {
    "intro": ("https://app.nextecmedia.ch/resolve?courseProductReference=P108e2&issueProductReference=P108e3&contentType=topic&fileReference=F15610_2&contentId=1.1&contentReference=20992",
              "nextecmedia, Technique numérique, 1.1 Introduction à la technique numérique"),
    "repr": ("https://app.nextecmedia.ch/resolve?courseProductReference=P108e2&issueProductReference=P108e3&contentType=topic&fileReference=F15610_4&contentId=1.2.1&contentReference=25454",
             "nextecmedia, Technique numérique, 1.2.1 Formes de représentation des circuits numériques"),
    "fam": ("https://app.nextecmedia.ch/resolve?courseProductReference=P108e2&issueProductReference=P108e6&contentType=topic&fileReference=F15613_2&contentId=4.1&contentReference=22831",
            "nextecmedia, Technique numérique, 4.1 Familles de circuits"),
}
# Fichiers du cours sur Teams (dossier El_DT1/PMT&SBT, comme 100) : liens par chemin, valables une fois le fichier déposé sous ce nom
_TDIR = ("https://eduvaud.sharepoint.com/:{k}:/r/sites/msteams_084f74/Documents%20partages/Enseignement%20professionnel/"
         "ChampsDApprentissage/El_DT1/PMT%26SBT/")
TEAMS_100 = ("https://eduvaud.sharepoint.com/:p:/r/sites/msteams_084f74/Documents%20partages/Enseignement%20professionnel/ChampsDApprentissage/"
             "El_DT1/PMT%26SBT/100%20Familles%20de%20circuits%20logiques.pptx?d=w28411bfc763a4e079f3f438436a654a4&csf=1&web=1&e=1m7PWF")


def teams(name, kind):
    from urllib.parse import quote
    return _TDIR.format(k=kind) + quote(name) + "?csf=1&web=1"


F100 = "100 Familles de circuits logiques.pptx"
F110 = "110 EX Familles de circuits logiques.docx"
F110C = "110 EX C Familles de circuits logiques.docx"
F120 = "120 Portes logiques et tables de vérité.pptx"
F130 = "130 EX Portes logiques de base.docx"          # « 130 EX » comme « 110 EX » (demande de Gaël, 11/16/2026)
F130C = "130 EX C Portes logiques de base.docx"
# animations et pages interactives : à la fin des présentations (exercices → page interactive → vidéo)
F105 = "105 Familles de circuits logiques.mp4"
F101 = "101 Familles de circuits logiques.html"
F125 = "125 Portes logiques et tables de vérité.mp4"
F121 = "121 Portes logiques et tables de vérité.html"
# artefacts claude.ai (privés tant que Gaël ne les partage pas ; pour la classe, le fichier .html déposé sur Teams)
ART101 = "https://claude.ai/artifact/84x2BeiLvEZuFFMS314SBY"
ART121 = "https://claude.ai/artifact/6TyUyScUooioJZaEkrY1uo"

# ---------------------------------------------------------------- portes logiques (Floyd chap. 3, symboles CEI 60617-12)
# clé : (nom, nom anglais, qualificatif CEI, négation en sortie, nb d'entrées, fonction, équation (mathtext), équation (OMML mini-LaTeX),
#        règle « Y = 1 si… », CI 74HC, CI 4000, contenu du CI, section Floyd, page)
GATES = {
    "NON":    ("NON", "NOT", "1", True, 1, lambda a, b=0: 1 - a, r"Y = \overline{A}", r"Y=\bar{A}",
               "Y = 1 si A = 0 : la sortie est l'inverse de l'entrée.", "74HC04", "4069", "6 inverseurs", "3-1", 112),
    "ET":     ("ET", "AND", "&", False, 2, lambda a, b: a & b, r"Y = A \cdot B", r"Y=A\cdot B",
               "Y = 1 seulement si A = 1 et B = 1.", "74HC08", "4081", "4 portes ET à 2 entrées", "3-2", 115),
    "OU":     ("OU", "OR", "≥1", False, 2, lambda a, b: a | b, r"Y = A + B", r"Y=A+B",
               "Y = 1 si au moins une entrée vaut 1.", "74HC32", "4071", "4 portes OU à 2 entrées", "3-3", 122),
    "NON-ET": ("NON-ET", "NAND", "&", True, 2, lambda a, b: 1 - (a & b), r"Y = \overline{A \cdot B}", r"Y=\bar{A\cdot B}",
               "Y = 0 seulement si A = 1 et B = 1.", "74HC00", "4011", "4 portes NON-ET à 2 entrées", "3-4", 126),
    "NON-OU": ("NON-OU", "NOR", "≥1", True, 2, lambda a, b: 1 - (a | b), r"Y = \overline{A + B}", r"Y=\bar{A+B}",
               "Y = 1 seulement si A = 0 et B = 0.", "74HC02", "4001", "4 portes NON-OU à 2 entrées", "3-5", 131),
    "OUX":    ("OU exclusif", "XOR", "=1", False, 2, lambda a, b: a ^ b, r"Y = A \oplus B", r"Y=A\oplus B",
               "Y = 1 si les deux entrées sont différentes.", "74HC86", "4070", "4 portes OU exclusif à 2 entrées", "3-6", 135),
    "NON-OUX": ("NON-OU exclusif", "XNOR", "=1", True, 2, lambda a, b: 1 - (a ^ b), r"Y = \overline{A \oplus B}", r"Y=\bar{A\oplus B}",
                "Y = 1 si les deux entrées sont égales.", "74HC7266", "4077", "4 portes NON-OU exclusif à 2 entrées", "3-6", 135),
}
ORDER = ["NON", "ET", "OU", "NON-ET", "NON-OU", "OUX", "NON-OUX"]


def tdv(key):
    """Lignes de la table de vérité, entrées du poids fort au poids faible : (B, A, Y) ; (A, Y) pour NON."""
    g = GATES[key]
    if g[4] == 1:
        return [(a, g[5](a)) for a in (0, 1)]
    return [(b, a, g[5](a, b)) for b in (0, 1) for a in (0, 1)]


TDV_HEAD = lambda n: ["A", "Y"] if n == 1 else ["B", "A", "Y"]   # en-tête : poids fort → poids faible, puis la sortie



# ---------------------------------------------------------------- typographie (espaces insécables)
import re as _re
NB, NNB = "\u00a0", "\u202f"
_UNITS = r"(?:V|mV|mA|A|µA|ns|ms|µs|s|MHz|kHz|Hz|µW|mW|W|pJ|°C|%|min|L|cm|mm|lignes|portes|entrées|broches|bits|bytes|bouteilles|transistors|inverseurs)"


def typo(t):
    """Espaces insécables : nombre + unité, avant « : ; ? ! » et à l'intérieur des guillemets français."""
    if not isinstance(t, str) or "://" in t:
        return t
    t = _re.sub(r" ([:;?!»])", NB + r"\1", t)
    t = t.replace("« ", "«" + NB)
    t = _re.sub(r"(\d) (?=" + _UNITS + r"\b)", r"\1" + NB, t)
    t = _re.sub(r"(\d) (?=°C)", r"\1" + NB, t)
    t = _re.sub(r"\b(N°|n°|p\.|chap\.|diapositives?|LZ|Floyd) (?=\d)", lambda m: m.group(1) + NB, t)
    t = _re.sub(r"(\d) … (\d|−)", r"\1" + NB + "…" + NB + r"\2", t)
    for _ in range(2):   # « A = 1 », « A = B = 1 » ne se coupent pas
        t = _re.sub(r"(^|[\s(])(\w{1,3}) = ([\w−]{1,3})(?=$|[\s,.;:)!?])", r"\1\2" + NB + "=" + NB + r"\3", t)
    t = _re.sub(r"(\d) ou (\d)", r"\1" + NB + "ou" + NB + r"\2", t)
    t = _re.sub(r"(\d) (?=[a-zà-ÿ])", r"\1" + NB, t)      # « 4 portes », « 8 lignes »
    t = _re.sub(r"\bNON-(ET|OU)\b", "NON\u2011\\1", t)      # trait d'union insécable (docx : w:noBreakHyphen)
    return t


# chronogramme standard du cours : 8 intervalles, les 4 combinaisons de A et B apparaissent deux fois
CHRONO_A = [0, 1, 0, 1, 1, 0, 1, 0]
CHRONO_B = [0, 0, 1, 1, 0, 1, 1, 0]


def chrono(key, A=CHRONO_A, B=CHRONO_B):
    f = GATES[key][5]
    return [f(a, b) for a, b in zip(A, B)]


# ---------------------------------------------------------------- niveaux logiques (Floyd 3-8 p. 154, VCC = 5 V ; HCT : fiche M74HCT00)
NIV = {   # famille : (VIL max, VIH min, VOL max, VOH min)
    "TTL": (0.8, 2.0, 0.4, 2.4),
    "HC":  (1.5, 3.5, 0.33, 4.4),
    "HCT": (0.8, 2.0, 0.33, 4.4),
}


def compat(src, dst):
    """Sortie de src → entrée de dst : (ok haut, ok bas, marge haute, marge basse)."""
    vil, vih = NIV[dst][0], NIV[dst][1]
    vol, voh = NIV[src][2], NIV[src][3]
    return voh >= vih, vol <= vil, round(voh - vih, 2), round(vil - vol, 2)


if __name__ == "__main__":
    for k in ORDER:
        print(k, tdv(k), chrono(k))
    for s in NIV:
        for d_ in NIV:
            print(s, "→", d_, compat(s, d_))
    json.dump({"LZ": {k: list(v) for k, v in LZ.items()}, "FLOYD": {k: [floyd_url(k), v[1], v[2]] for k, v in FLOYD.items()},
               "FLOYD_NOTE": FLOYD_NOTE, "FLOYD_PAGES": {k: floyd_url(int(k[0]), int(k[2:])) for k in ["1-5", "1-26", "1-11", "3-111", "3-112", "3-146", "3-150", "3-152", "3-154"]},
               "NEXTEC": NEXTEC, "FUTUREMEM_CHAMP": FUTUREMEM_CHAMP, "EDGE": EDGE, "TEAMS_100": TEAMS_100,
               "FILES": {"F100": F100, "F105": F105, "F110": F110, "F110C": F110C, "F101": F101, "F120": F120, "F125": F125, "F130": F130, "F130C": F130C, "F121": F121},
               "TEAMS": {"F110": teams(F110, "w"), "F130": teams(F130, "w"), "F105": teams(F105, "v"), "F125": teams(F125, "v"), "F101": teams(F101, "u"), "F121": teams(F121, "u")},
               "ART": {"101": ART101, "121": ART121},
               "GATES": {k: [v[0], v[1], v[2], v[3], v[4], v[8], v[9], v[10], v[11], v[12], v[13], floyd_url(3, v[13]), tdv(k), chrono(k)] for k, v in GATES.items()},
               "ORDER": ORDER, "CHRONO_A": CHRONO_A, "CHRONO_B": CHRONO_B, "NIV": NIV,
               "CLASSE": CLASSE, "ANNEE": ANNEE, "MATIERE": MATIERE, "CHAMP": CHAMP, "DATE_US": DATE_US},
              open("w1_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("w1_data.json ok")
