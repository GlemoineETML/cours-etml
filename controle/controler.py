# -*- coding: utf-8 -*-
"""Contrôle avant livraison (REGLES 9.1) des fichiers produits pour une séance.

Usage : python3 controle/controler.py tm1/semaine-1 [--rendu] [--reference]
  1. validation : chaque fichier Office s'ouvre (zip, XML, python-docx / python-pptx / openpyxl) ;
  2. conventions de REGLES.md vérifiables automatiquement (voir CONVENTIONS) ;
  3. recalcul indépendant : contenus/<séance>/verif.py (fonction verifier() → liste d'erreurs) ;
  4. --rendu : conversion en PDF puis en images (LibreOffice, pdftoppm) dans sortie/_controle/<séance>/ pour la vérification visuelle ;
  5. --reference : comparaison avec reference/<séance>/ (controle/comparer.py).
Code de sortie 0 si aucune erreur. Les avertissements (⚠) sont à regarder, pas bloquants.
"""
import argparse, glob, html, os, re, subprocess, sys, zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)
from moteur.seance import Seance


# ---------------------------------------------------------------- extraction du texte
def texte_docx(chemin):
    """Paragraphes du corps (w:noBreakHyphen rendu par « ‑ »)."""
    x = zipfile.ZipFile(chemin).read("word/document.xml").decode("utf-8")
    paras = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", x, flags=re.S):
        t = re.sub(r"<w:noBreakHyphen/>", "‑", p)
        t = re.sub(r"<w:tab/>", "\t", t)
        paras.append(html.unescape("".join(re.findall(r"<[wm]:t(?: [^>]*)?>([^<]*)</[wm]:t>", t))))   # texte et équations
    return paras


def texte_pptx(chemin):
    """{numéro de diapositive : [paragraphes]} (notes non comprises)."""
    z = zipfile.ZipFile(chemin)
    out = {}
    for n in z.namelist():
        m = re.match(r"ppt/slides/slide(\d+)\.xml$", n)
        if m:
            x = z.read(n).decode("utf-8")
            out[int(m.group(1))] = [html.unescape("".join(re.findall(r"<a:t>([^<]*)</a:t>", p))) for p in re.findall(r"<a:p>.*?</a:p>", x, flags=re.S)]
    return dict(sorted(out.items()))


def liens_office(chemin):
    z = zipfile.ZipFile(chemin)
    urls = []
    for n in z.namelist():
        if n.endswith(".rels"):
            urls += [html.unescape(u) for u in re.findall(r'Target="([^"]+)"[^>]*TargetMode="External"', z.read(n).decode("utf-8"))]
    return urls


# ---------------------------------------------------------------- 1. validation
def valider(chemin):
    err = []
    try:
        z = zipfile.ZipFile(chemin)
        bad = z.testzip()
        if bad: err.append(f"partie corrompue : {bad}")
        from xml.dom import minidom
        for n in z.namelist():
            if n.endswith((".xml", ".rels")):
                try: minidom.parseString(z.read(n))
                except Exception as e: err.append(f"XML invalide : {n} ({e})")
        if chemin.endswith(".docx"):
            import docx; docx.Document(chemin)
        elif chemin.endswith(".pptx"):
            import pptx; pptx.Presentation(chemin)
        elif chemin.endswith(".xlsx"):
            import openpyxl; openpyxl.load_workbook(chemin)
    except Exception as e:
        err.append(f"ne s'ouvre pas : {e}")
    return err


# ---------------------------------------------------------------- 2. conventions (REGLES.md)
def conventions(S, chemin):
    """Retourne (erreurs, avertissements) pour un fichier produit."""
    E, A = [], []
    nom = os.path.basename(chemin)
    if chemin.endswith(".docx"):
        paras = texte_docx(chemin)
        lignes = [(f"§{i + 1}", p) for i, p in enumerate(paras)]
    elif chemin.endswith(".pptx"):
        lignes = [(f"diapo {k}", p) for k, ps in texte_pptx(chemin).items() for p in ps]
    elif chemin.endswith(".html"):
        s = open(chemin, encoding="utf-8").read()
        s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
        lignes = [("page", html.unescape(t)) for t in re.findall(r">([^<]+)<", s) if t.strip()]
    else:
        lignes = []
    tout = "\n".join(t for _, t in lignes)

    def cherche(rx, msg, grave=True):
        for ou, t in lignes:
            for m in re.finditer(rx, t):
                (E if grave else A).append(f"{nom} ({ou}) : {msg} : « {t[max(0, m.start() - 25):m.end() + 25].strip()} »")

    cherche(r"§\s*\d", "« § » devant un numéro de section (REGLES 6)")
    cherche(r"IntElect|El Dim1\b", "matière abandonnée (REGLES 2)")
    cherche(r"N°\d+\s*\t", "tabulation après le numéro d'exercice (REGLES 4)")
    cherche(r"(?<![\w.])\d+\.\d+\s?(?:V|A|mA|mV|Ω|kΩ|s|ms|µs|ns|Hz|kHz|MHz|W|mW)\b", "point décimal au lieu de la virgule (REGLES 3.1)")
    cherche(r"\b\d+(?:,\d+)? (?:V|mV|mA|A|µA|ns|ms|µs|Hz|kHz|MHz|W|mW|°C|Ω|kΩ)\b", "espace normale entre le nombre et l'unité (REGLES 3.1)", grave=False)
    cherche(r" [:;?!]", "espace normale avant : ; ? ! (REGLES 7)", grave=False)
    cherche(r"\bNON-(?:ET|OU)\b", "trait d'union sécable dans NON-ET / NON-OU (REGLES 7)", grave=False)
    cherche(r"\b[01]{2,}[dD]\b(?!\w)|\b0x[0-9A-Fa-f]+\b", "notation des nombres : suffixe b, d, h (REGLES 3.4)", grave=False)
    if S.hors_reforme and re.search(r"LZ_\d+|FutureMEM", tout):
        E.append(f"{nom} : cours hors réforme, mais LZ ou FutureMEM cité (REGLES 2)")

    # liens (REGLES 6)
    if chemin.endswith((".docx", ".pptx", ".xlsx")):
        for u in liens_office(chemin):
            if "futuremem" in u and "#" in u and not u.startswith("microsoft-edge:"):
                E.append(f"{nom} : lien FutureMEM sans microsoft-edge: ({u[:80]}…)")
            if "Floyd" in u and "sharepoint" in u and "d=" not in u:
                E.append(f"{nom} : lien Floyd reconstruit, pas le lien « Copier le lien » de Teams ({u[:80]}…)")
            if "Floyd" in u and u.startswith("microsoft-edge:"):
                E.append(f"{nom} : lien Floyd avec microsoft-edge: (REGLES 6)")

    # éditeur (REGLES 5) : seulement sur la diapositive de titre
    if chemin.endswith(".pptx"):
        diapos = texte_pptx(chemin)
        for k, ps in diapos.items():
            if k > 1 and any(S.editeur in p for p in ps):
                E.append(f"{nom} (diapo {k}) : l'éditeur n'apparaît que sur la diapositive de titre (REGLES 5)")
        if not any(S.editeur in p and S.date in p for p in diapos.get(1, [])):
            E.append(f"{nom} : ligne « {S.editeur} · {S.date} » absente de la diapositive de titre (REGLES 5)")

    # fiche élève / corrigé (REGLES 4)
    if chemin.endswith(".docx"):
        x = zipfile.ZipFile(chemin).read("word/document.xml").decode("utf-8")
        corrige = " EX C " in nom
        rouge = 'w:val="EE0000"' in x
        if corrige and not rouge: E.append(f"{nom} : corrigé sans réponse en rouge EE0000 (REGLES 4)")
        if not corrige and rouge and "Corrigé" not in tout: E.append(f"{nom} : texte rouge EE0000 dans la fiche élève (REGLES 4)")
        if corrige and "Auto-évaluation" in tout: E.append(f"{nom} : grille d'auto-évaluation dans le corrigé (REGLES 4 : fiche élève seulement)")
        if not corrige and "Auto-évaluation" not in tout: A.append(f"{nom} : pas de grille d'auto-évaluation")
        corr = chemin.replace(" EX ", " EX C ") if not corrige else None
        if corr and not os.path.exists(corr): E.append(f"{nom} : corrigé manquant (REGLES 4)")
    return E, A


# ---------------------------------------------------------------- 4. rendu
def rendu(chemin, dossier):
    os.makedirs(dossier, exist_ok=True)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", dossier, chemin], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pdf = os.path.join(dossier, os.path.splitext(os.path.basename(chemin))[0] + ".pdf")
    subprocess.run(["pdftoppm", "-r", "60", "-png", pdf, pdf[:-4]], check=True)
    return sorted(glob.glob(pdf[:-4] + "-*.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seance")
    ap.add_argument("--rendu", action="store_true")
    ap.add_argument("--reference", action="store_true")
    a = ap.parse_args()
    S = Seance(os.path.join(RACINE, "contenus", a.seance))
    sortie = os.path.join(RACINE, "sortie", a.seance)
    fichiers = sorted(f for f in glob.glob(os.path.join(sortie, "*")) if os.path.isfile(f))
    E, A = [], []
    attendus = set(S.fichiers.values()) | ({S.plan["fichier"]} if S.plan else set())
    for nom in sorted(attendus - {os.path.basename(f) for f in fichiers}):
        E.append(f"fichier manquant : {nom}")
    for f in fichiers:
        if f.endswith((".docx", ".pptx", ".xlsx")):
            E += [f"{os.path.basename(f)} : {e}" for e in valider(f)]
        e, w = conventions(S, f); E += e; A += w
    verif = os.path.join(S.dossier, "verif.py")
    if os.path.exists(verif):
        e = S.module("verif").verifier()
        E += [f"recalcul : {x}" for x in e]
        print("recalcul indépendant : verif.py,", "aucune erreur" if not e else f"{len(e)} erreur(s)")
    else:
        A.append("pas de verif.py : résultats numériques non recalculés")
    if a.reference:
        from controle.comparer import comparer
        ref = os.path.join(RACINE, "reference", a.seance)
        for f in fichiers:
            r = os.path.join(ref, os.path.basename(f))
            if os.path.exists(r) and not f.endswith(".mp4"):
                d = comparer(f, r)
                print(f"référence · {os.path.basename(f)} : {'identique' if not d else ', '.join(d)}")
    if a.rendu:
        dossier = os.path.join(RACINE, "sortie", "_controle", a.seance)
        for f in fichiers:
            if f.endswith((".docx", ".pptx")):
                print(f"rendu · {os.path.basename(f)} : {len(rendu(f, dossier))} page(s)")
    for x in A: print("⚠", x)
    for x in E: print("✗", x)
    print(f"{len(E)} erreur(s), {len(A)} avertissement(s)")
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main()
