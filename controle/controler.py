# -*- coding: utf-8 -*-
"""Contrôle avant livraison (REGLES 9.1) des fichiers produits pour une séance.

Usage : python3 controle/controler.py tm1/semaine-1 [--rendu] [--reference]
  1. validation : chaque fichier Office s'ouvre (zip, XML, python-docx / python-pptx / openpyxl) ;
  2. conventions de REGLES.md vérifiables automatiquement (voir CONVENTIONS) ;
  3. recalcul indépendant : contenus/<séance>/verif.py (fonction verifier() → liste d'erreurs) ;
  4. --rendu : conversion en PDF puis en images (LibreOffice, pdftoppm) dans sortie/_controle/<séance>/ pour la vérification visuelle ;
     puis contrôle de mise en page (controle/mise_en_page.py : débordements, chevauchements, pages presque vides, unités coupées) ;
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
        z = zipfile.ZipFile(chemin)
        lay = re.search(r'Target="\.\./slideLayouts/(slideLayout\d+\.xml)"', z.read("ppt/slides/_rels/slide1.xml.rels").decode("utf-8"))
        titre = diapos.get(1, []) + ([html.unescape(t) for t in re.findall(r"<a:t>([^<]*)</a:t>", z.read("ppt/slideLayouts/" + lay.group(1)).decode("utf-8"))] if lay else [])
        if not any(S.editeur in p and S.date in p for p in titre):
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


def lz_titres(S, fichiers):
    """REGLES 5 : chaque LZ de seance.yaml est écrit et cliquable sur la diapositive de titre d'au moins une présentation
    de la séance (une seule présentation par séance dans la nouvelle structure : elle les porte donc tous)."""
    if S.hors_reforme:
        return []
    trouves = set()
    for f in fichiers:
        if not f.endswith(".pptx"):
            continue
        z = zipfile.ZipFile(f)
        liens = [html.unescape(u) for u in re.findall(r'Target="([^"]+)"[^>]*TargetMode="External"', z.read("ppt/slides/_rels/slide1.xml.rels").decode("utf-8"))]
        texte = " ".join(texte_pptx(f).get(1, []))
        trouves |= {c for c, (_, _, lien) in S.lz.items() if c in texte and any(lien in u for u in liens)}
    return [f"{c} absent ou non cliquable sur la diapositive de titre (REGLES 5 : chaque objectif finit par son LZ)"
            for c in S.lz if c not in trouves]


# ---------------------------------------------------------------- 3 bis. lisibilité des figures
CORPS_MIN = {".pptx": 8.0, ".docx": 7.0}     # plus petit corps lisible une fois l'image placée : projeté en classe / imprimé


def corps_figures(fichiers, tailles):
    """Corps réel du plus petit texte de chaque figure, d'après sa largeur affichée dans la présentation ou la fiche."""
    import json
    if not os.path.exists(tailles):
        return []
    T = json.load(open(tailles, encoding="utf-8"))
    E = []
    for f in fichiers:
        ext = os.path.splitext(f)[1]
        if ext not in CORPS_MIN:
            continue
        z = zipfile.ZipFile(f)
        parties = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$|word/document\.xml$", n)]
        for n in parties:
            x = z.read(n).decode("utf-8")
            ou = f"diapo {re.search(r'(\d+)', n.split('/')[-1]).group(1)}" if ext == ".pptx" else "fiche"
            for bloc in re.findall(r"<p:pic>.*?</p:pic>|<w:drawing>.*?</w:drawing>", x, flags=re.S):
                nom = re.search(r'descr="([^"]+)"', bloc) or re.search(r'<pic:cNvPr[^>]*name="([^"]+)"', bloc)
                cx = re.search(r'<a:ext cx="(\d+)"', bloc) or re.search(r'<wp:extent cx="(\d+)"', bloc)
                if not (nom and cx) or os.path.basename(nom.group(1)) not in T:
                    continue
                larg, pt, quoi = T[os.path.basename(nom.group(1))]
                reel = pt * (int(cx.group(1)) / 914400) / larg
                if reel < CORPS_MIN[ext]:
                    E.append(f"{os.path.basename(f)} ({ou}) : figure {nom.group(1)} trop réduite : texte « {quoi} » à {reel:.1f} pt "
                             f"(minimum {CORPS_MIN[ext]:.0f} pt) : agrandir la figure ou ses textes")
    return E


JS_SVG = r"""
(racine) => {
  const out = [];
  const pts = (el) => {                       // segments des traits (line, polyline) en coordonnées écran
    const m = el.getScreenCTM(); if (!m) return [];
    const P = (x, y) => { const p = new DOMPoint(x, y).matrixTransform(m); return [p.x, p.y]; };
    if (el.tagName === "line") return [[P(+el.getAttribute("x1"), +el.getAttribute("y1")), P(+el.getAttribute("x2"), +el.getAttribute("y2"))]];
    const v = el.getAttribute("points").trim().split(/\s+/).map((c) => c.split(",").map(Number));
    return v.slice(1).map((q, i) => [P(...v[i]), P(...q)]);
  };
  const coupe = (r, [[x1, y1], [x2, y2]]) => {  // le segment traverse-t-il le rectangle ?
    for (let k = 0; k <= 40; k++) { const x = x1 + (x2 - x1) * k / 40, y = y1 + (y2 - y1) * k / 40;
      if (x > r.left && x < r.right && y > r.top && y < r.bottom) return true; }
    return false;
  };
  const zone = racine ? document.querySelector(racine) : document;
  zone.querySelectorAll("svg").forEach((svg) => {
    if (!svg.getBoundingClientRect().width) return;
    if (!racine && svg.closest(".lesson")) return;                 // les animations sont vérifiées étape par étape
    const ts = [...svg.querySelectorAll("text")].filter((t) => t.textContent.trim() && getComputedStyle(t).opacity !== "0" && !(t.closest("[style*='opacity:0']")));
    const R = ts.map((t) => { const b = t.getBoundingClientRect(), h = b.height * 0.18;
      return { left: b.left + 1, right: b.right - 1, top: b.top + h, bottom: b.bottom - h, h: b.height, txt: t.textContent.trim() }; });
    const traits = [...svg.querySelectorAll("line, polyline")];
    const cercles = [...svg.querySelectorAll("circle")].map((c) => { const b = c.getBoundingClientRect(); return { x: b.left + b.width / 2, y: b.top + b.height / 2, r: b.width / 2 }; })
      .filter((c) => c.r >= 14);                                     // anneaux et symboles ; les porteurs (r ≈ 9) portent leur signe
    for (let i = 0; i < R.length; i++) {
      for (let j = i + 1; j < R.length; j++) {
        const a = R[i], b = R[j], lx = Math.min(a.right, b.right) - Math.max(a.left, b.left), ly = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (lx > 1 && ly > 1) out.push(`textes « ${a.txt.slice(0, 25)} » et « ${b.txt.slice(0, 25)} » se chevauchent`);
      }
      for (const l of traits) {
        const st = l.getAttribute("style") || "";
        if (/stroke:var\(--line\)/.test(st)) continue;              // quadrillage des graphiques : discret, les graduations le longent
        if (pts(l).some((sg) => coupe(R[i], sg))) { out.push(`texte « ${R[i].txt.slice(0, 30)} » posé sur un trait`); break; }
      }
      for (const c of cercles) {
        const r = R[i];
        if (c.x > r.left && c.x < r.right && c.y > r.top && c.y < r.bottom) continue;   // texte dans le cercle (signe d'un porteur)
        let touche = false;
        for (let k = 0; k < 64 && !touche; k++) { const x = c.x + c.r * Math.cos(k * Math.PI / 32), y = c.y + c.r * Math.sin(k * Math.PI / 32);
          touche = x > r.left && x < r.right && y > r.top && y < r.bottom; }
        if (touche) { out.push(`texte « ${r.txt.slice(0, 30)} » posé sur un cercle`); break; }
      }
    }
  });
  return [...new Set(out)];
}
"""


def controler_page(html):
    """Pages interactives : textes des dessins (exercices et chaque étape des animations) qui se chevauchent ou sont posés
    sur un trait. Même règle que les figures (REGLES 9.4) ; chaque défaut est bloquant."""
    from playwright.sync_api import sync_playwright
    nom, E = os.path.basename(html), []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": 1200, "height": 900})
        pg.goto("file://" + os.path.abspath(html)); pg.wait_for_timeout(1500)
        for b in pg.query_selector_all(".ls-play"):
            if "Pause" in b.inner_text(): b.click()                 # animations figées : on parcourt les étapes
        E += [f"{nom} (dessins des exercices) : {m}" for m in pg.evaluate(JS_SVG, None)]
        for k, ls in enumerate(pg.query_selector_all(".lesson")):
            for j, bt in enumerate(ls.query_selector_all(".ls-steps button")):
                for dt in (0.3, 2.5):                                  # début de l'étape et après les transitions
                    bt.click(); pg.evaluate(f"() => {{ const st = LESSONS[{k}]; st.t += {dt}; st.render(); }}")
                    E += [f"{nom} (animation {ls.get_attribute('id')}, étape {j + 1}) : {m}" for m in pg.evaluate(JS_SVG, "#" + ls.get_attribute("id"))]
        nav.close()
    return sorted(set(E))


def planche_video(S, anim, dossier, pas=5.0):
    """Images clés d'une animation : une image toutes les `pas` secondes de chaque scène, 6 par planche.
    Le contrôle automatique ne lit pas les vidéos : ces planches sont relues en entier avant l'envoi (CLAUDE.md)."""
    from PIL import Image
    m = S.module(os.path.basename(anim)[:-3])
    ims = []
    for i, (_, dur) in enumerate(m.SCENES):
        t = 1.0
        while t < dur:
            ims.append(m.frame_at(m.SCENES, i, t).resize((960, 540))); t += pas
    num = os.path.basename(anim)[:3]
    sorties = []
    for k in range(0, len(ims), 6):
        pl = Image.new("RGB", (1920, 1620), "white")
        for j, im in enumerate(ims[k:k + 6]):
            pl.paste(im, ((j % 2) * 960, (j // 2) * 540))
        sorties.append(os.path.join(dossier, f"video-{num}-{k // 6 + 1}.png")); pl.save(sorties[-1])
    return sorties


def planche_figures(travail, dossier):
    """Toutes les figures de la séance sur une planche, pour la relecture visuelle obligatoire (CLAUDE.md)."""
    from PIL import Image
    import json
    fs = set(glob.glob(os.path.join(travail, "fig_*.png")))
    tailles = os.path.join(travail, "tailles_figures.json")       # toutes les figures passées par moteur/cei.save
    if os.path.exists(tailles):
        fs |= {os.path.join(travail, n) for n in json.load(open(tailles, encoding="utf-8"))
               if not n.startswith("eq_") and os.path.exists(os.path.join(travail, n))}
    fs = sorted(fs)
    if not fs:
        return None
    W = 900                                             # pages de 4 figures, lisibles à l'écran
    ims = [Image.open(f).convert("RGB") for f in fs]
    ims = [im.resize((W, max(1, int(im.size[1] * W / im.size[0])))) for im in ims]
    sortie = None
    for p0 in range(0, len(ims), 4):
        lot = ims[p0:p0 + 4]
        h = max(im.size[1] for im in lot)
        pl = Image.new("RGB", (2 * W + 20, 2 * h + 20), "white")
        for k, im in enumerate(lot):
            pl.paste(im, ((k % 2) * (W + 20), (k // 2) * (h + 20)))
        sortie = os.path.join(dossier, f"figures-{p0 // 4 + 1}.png")
        pl.save(sortie)
    return sortie


# ---------------------------------------------------------------- 4. rendu
def module_formules():
    """LibreOffice sans son module Math (paquet libreoffice-math) n'affiche aucune équation OMML dans le rendu."""
    return any(os.path.exists(p) for p in ("/etc/libreoffice/registry/math.xcd", "/usr/lib/libreoffice/share/registry/math.xcd",
                                           "/Applications/LibreOffice.app/Contents/Resources/registry/math.xcd"))


def rendu(chemin, dossier):
    os.makedirs(dossier, exist_ok=True)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", dossier, chemin], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pdf = os.path.join(dossier, os.path.splitext(os.path.basename(chemin))[0] + ".pdf")
    subprocess.run(["pdftoppm", "-r", "60", "-png", pdf, pdf[:-4]], check=True, stderr=subprocess.DEVNULL)
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
    E += lz_titres(S, fichiers)
    # figures (moteur/cei.save) : texte posé sur une courbe = erreur bloquante ; texte trop petit une fois l'image placée = erreur
    travail = os.path.join(RACINE, "sortie", "_travail", a.seance)
    fa = os.path.join(travail, "avertissements_figures.txt")
    if os.path.exists(fa):
        E += [f"figure · {l.strip()}" for l in open(fa, encoding="utf-8") if l.strip()]
    E += corps_figures(fichiers, os.path.join(travail, "tailles_figures.json"))
    from controle.karnaugh import verifier as verifier_karnaugh          # tableaux de Karnaugh (REGLES 3.5)
    E += verifier_karnaugh(travail)
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
        if not module_formules():
            A.append("LibreOffice n'a pas son module de formules (paquet libreoffice-math) : les équations manquent dans le rendu")
        dossier = os.path.join(RACINE, "sortie", "_controle", a.seance)
        from controle.mise_en_page import controler_pptx, controler_pdf
        for f in fichiers:
            if f.endswith((".docx", ".pptx")):
                print(f"rendu · {os.path.basename(f)} : {len(rendu(f, dossier))} page(s)")
                pdf = os.path.join(dossier, os.path.splitext(os.path.basename(f))[0] + ".pdf")
                MP = (controler_pptx(f) if f.endswith(".pptx") else []) + controler_pdf(pdf, f.endswith(".docx"))
                # une équation plus grande que son cadre est vue seulement ici (LibreOffice montre l'image de secours) : bloquant
                E += [f"mise en page · {m}" for m in MP if "équation" in m]
                A += [f"mise en page · {m}" for m in MP if "équation" not in m]
        for f in fichiers:
            if f.endswith(".html"):
                E += [f"page · {m}" for m in controler_page(f)]
        for f in glob.glob(os.path.join(S.dossier, "*-anim.py")):
            for pv in planche_video(S, f, dossier):
                print(f"images clés de la vidéo à relire : {os.path.relpath(pv, RACINE)}")
        pl = planche_figures(travail, dossier)
        if pl:
            print(f"planches des figures à relire : {os.path.relpath(os.path.dirname(pl), RACINE)}/figures-*.png")
    for x in A: print("⚠", x)
    for x in E: print("✗", x)
    print(f"{len(E)} erreur(s), {len(A)} avertissement(s)")
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main()
