# -*- coding: utf-8 -*-
"""Contrôle automatique de la mise en page (REGLES 9), lancé par controle/controler.py avec --rendu.

Présentations (.pptx, lecture du XML) :
  - texte qui déborde de son cadre (estimation : largeur moyenne des caractères Arial, interligne 1,2) ;
  - chevauchements entre zones de texte, et entre une zone de texte et une image.
Fiches et présentations (PDF rendu par LibreOffice, pdftotext -bbox-layout) :
  - page presque vide (fiche : page intermédiaire remplie à moins de 80 %, dernière page à moins de 25 % ; texte et images) ;
  - nombre séparé de son unité en fin de ligne (« 0,0039 » / « 1/K »).
Ce sont des estimations : chaque avertissement se vérifie sur le rendu, puis se corrige ou se justifie avant livraison."""
import html, math, os, re, subprocess, zipfile

EMU = 12700                                   # EMU par point
UNITE = r"^(?:V|mV|mA|A|µA|kV|W|mW|kW|Ω|kΩ|MΩ|GΩ|mΩ|µΩ|Ω·m|1/K|K|eV|°C|%|Hz|kHz|MHz|s|ms|µs|ns|m|mm|cm|m²|mm²|pF|nF|µF)[.,;:)]*$"


# ---------------------------------------------------------------- présentations
def _formes(xml):
    """Zones de texte, images et tableaux d'une diapositive : (genre, x, y, l, h, texte, paragraphes, rétrécir)."""
    xml = re.sub(r"<mc:Fallback>.*?</mc:Fallback>", "", xml, flags=re.S)      # équations : on garde la version éditable
    out = []
    for genre, bloc in re.findall(r"<p:(sp|pic|graphicFrame)>(.*?)</p:\1>", xml, flags=re.S):
        off = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"/>', bloc)
        if not off:
            continue
        x, y, l, h = (int(v) / EMU for v in off.groups())
        paras = []
        for p in re.findall(r"<a:p>(.*?)</a:p>", bloc, flags=re.S):
            tailles = [int(t) / 100 for t in re.findall(r'<a:rPr[^>]*\bsz="(\d+)"', p)] or [18.0]
            texte = html.unescape("".join(re.findall(r"<a:t>([^<]*)</a:t>", p)))
            if "<m:oMath" in p:
                texte = texte or "équation"
            gras = 'b="1"' in p
            paras.append((texte, max(tailles), gras, p.count("<a:br/>")))
        texte = " ".join(t for t, *_ in paras).strip()
        if "<m:oMath" in bloc:
            # équation éditable : PowerPoint l'affiche à sa taille de police (sz), centrée dans le cadre, sans la réduire ;
            # le rendu LibreOffice montre l'image de secours, ajustée au cadre : seule cette estimation voit le débordement.
            sz = max([int(t) / 100 for t in re.findall(r'<a:rPr[^>]*\bsz="(\d+)"', bloc)] or [18.0])
            car = len("".join(re.findall(r"<m:t[^>]*>([^<]*)</m:t>", bloc)))
            fr = bloc.count("<m:f>")
            hn = sz * (2.6 if fr else 1.3)                        # une fraction : numérateur + dénominateur ≈ 2,6 corps
            ln = sz * 0.55 * car * (0.6 if fr else 1.0)           # dans une fraction, numérateur et dénominateur se superposent
            cx, cy = x + l / 2, y + h / 2
            out.append(("eq", x, y, l, h, "équation", paras, False, (cx - max(l, ln) / 2, cy - max(h, hn) / 2, max(l, ln), max(h, hn), ln, hn)))
            continue
        out.append((genre, x, y, l, h, texte, paras, "<a:normAutofit" in bloc or "<a:spAutoFit" in bloc))
    return out


def _hauteur_texte(paras, largeur):
    """Hauteur estimée (pt) d'un texte Arial dans une largeur donnée (pt)."""
    tot = 0.0
    for texte, sz, gras, br in paras:
        if not texte:
            tot += sz * 1.2 * (1 + br)
            continue
        cw = sz * (0.55 if gras else 0.5)
        lignes, cur = 1, 0.0
        for mot in texte.split():
            w = (len(mot) + 1) * cw
            if cur + w > largeur and cur > 0:
                lignes += 1; cur = w
            else:
                cur += w
        tot += (lignes + br) * sz * 1.2 + 3
    return tot


def _inter(a, b):
    x0, y0 = max(a[1], b[1]), max(a[2], b[2])
    x1, y1 = min(a[1] + a[3], b[1] + b[3]), min(a[2] + a[4], b[2] + b[4])
    return max(0, x1 - x0) * max(0, y1 - y0)


def controler_pptx(chemin):
    A = []
    nom = os.path.basename(chemin)
    z = zipfile.ZipFile(chemin)
    diapos = sorted((int(m.group(1)), n) for n in z.namelist() if (m := re.match(r"ppt/slides/slide(\d+)\.xml$", n)))
    for k, n in diapos:
        formes = _formes(z.read(n).decode("utf-8"))
        for f in [f for f in formes if f[0] == "eq"]:
            ln, hn = f[8][4], f[8][5]
            if hn > f[4] + 4 or ln > f[3] + 4:
                A.append(f"{nom} (diapo {k}) : équation plus grande que son cadre dans PowerPoint (≈ {ln:.0f} × {hn:.0f} pt pour {f[3]:.0f} × {f[4]:.0f} pt)")
        formes = [(("sp",) + f[8][:4] + (f"équation {i + 1}", f[6], True)) if f[0] == "eq" else f for i, f in enumerate(formes)]
        textes = [f for f in formes if f[0] == "sp" and f[5]]
        for g, x, y, l, h, t, paras, retrecir in textes:
            if retrecir:
                continue
            besoin = _hauteur_texte(paras, l - 2)
            if besoin > h + 6:
                A.append(f"{nom} (diapo {k}) : texte trop long pour son cadre (≈ {besoin:.0f} pt pour {h:.0f} pt) : « {t[:60]} »")
        cibles = textes + [f for f in formes if f[0] == "pic"]
        for i, a in enumerate(textes):
            for b in cibles[i + 1:]:
                if b is a:
                    continue
                s = _inter(a, b)
                petit = min(a[3] * a[4], b[3] * b[4]) or 1
                if s / petit > 0.15:
                    quoi = "une image" if b[0] == "pic" else f"« {b[5][:30]} »"
                    A.append(f"{nom} (diapo {k}) : « {a[5][:30]} » chevauche {quoi}")
    return A


# ---------------------------------------------------------------- rendu PDF (fiches et présentations)
def _pages_pdf(pdf):
    """[(hauteur page, [lignes (yMin, yMax, [mots])])] d'après pdftotext -bbox-layout."""
    x = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
    pages = []
    for ph, corps in re.findall(r'<page width="[\d.]+" height="([\d.]+)">(.*?)</page>', x, flags=re.S):
        lignes = []
        for lg in re.findall(r"<line [^>]*>(.*?)</line>", corps, flags=re.S):
            mots = re.findall(r'<word xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">([^<]*)</word>', lg)
            if mots:
                lignes.append((float(mots[0][0]), max(float(m[1]) for m in mots), [html.unescape(m[2]) for m in mots]))
        pages.append((float(ph), lignes))
    return pages


def _images_pdf(pdf):
    """[[bas de chaque image (pt, depuis le haut)] par page] : une figure en fin de page compte comme contenu."""
    try:
        import pdfplumber
    except ImportError:
        return []
    with pdfplumber.open(pdf) as d:
        return [[float(im["bottom"]) for im in p.images] for p in d.pages]


def controler_pdf(pdf, fiche):
    A = []
    nom = os.path.basename(pdf)[:-4]
    pages = _pages_pdf(pdf)
    images = _images_pdf(pdf) if fiche else []
    for i, (ph, lignes) in enumerate(pages):
        # unité séparée de son nombre en fin de ligne
        for a, b in zip(lignes, lignes[1:]):
            if a[2] and b[2] and re.search(r"\d$", a[2][-1]) and re.match(UNITE, b[2][0]) and b[0] > a[0]:
                A.append(f"{nom} (page {i + 1}) : unité séparée de son nombre en fin de ligne : « {a[2][-1]} / {b[2][0]} »")
        if not fiche:
            continue
        haut, bas = 0.11 * ph, ph - 0.09 * ph                     # en-tête et pied de page du modèle Rapport_Simple
        corps = [l[1] for l in lignes if haut < l[0] < bas] + [b for b in (images[i] if i < len(images) else []) if haut < b < bas]
        if not corps:
            continue
        rempli = (max(corps) - haut) / (bas - haut)
        derniere = i == len(pages) - 1
        if (not derniere and rempli < 0.8) or (derniere and rempli < 0.25):
            A.append(f"{nom} (page {i + 1}) : page remplie à {rempli:.0%} seulement" + (" (dernière page)" if derniere else ""))
    return A
