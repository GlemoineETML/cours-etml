# -*- coding: utf-8 -*-
"""Pages interactives : une page HTML autonome par présentation (CSS, JS, logo et données intégrés).

Une page = deux fichiers de contenu : <num>-page.html (gabarit : texte et exercices) et <num>-page.js (leçons animées
« Comprendre », insérées à la place de __LESSONS__). Le moteur fournit moteur/pages/common.css et common.js.

Champs remplacés dans le gabarit :
  __CSS__ __COMMONJS__ __LESSONS__ __LOGO__ __DATA__   briques et données
  __CLASSE__ __ANNEE__ __MATIERE__ __CHAMPNOM__ __CHAMP__ (lien du champ) __FLNOTE__
  __FL<chapitre>__ (Floyd)  __NX<CLÉ>__ (nextecmedia)  __T<numéro>__ (fichier sur Teams)  __LZ<numéro>__ (lien du LZ)
Liens FutureMEM sans préfixe microsoft-edge: : dans le navigateur, l'ancre « # » est conservée (REGLES 6).
Le texte affiché du gabarit reçoit la typographie française (typo_html).

capture() photographie le haut de la page (1200 × 860 px, × 1,5) pour la diapositive « Page interactive » des présentations.
"""
import base64, json, os, re

ICI = os.path.dirname(os.path.abspath(__file__))
esc = lambda u: u.replace("&", "&amp;")


def champs(S, logo):
    sub = {
        "__LOGO__": logo, "__CHAMP__": esc(S.futuremem_champ or ""), "__CHAMPNOM__": S.champ,
        "__CLASSE__": S.classe, "__ANNEE__": S.annee, "__MATIERE__": S.matiere, "__FLNOTE__": S.floyd_note,
    }
    for c in S.floyd:
        sub[f"__FL{c}__"] = esc(S.floyd_url(c))
    for k, (url, _) in S.nextec.items():
        sub[f"__NX{k.upper()}__"] = esc(url)
    for num in S.fichiers:
        sub[f"__T{num}__"] = esc(S.teams_url(num))
    for code, v in S.lz.items():
        sub["__" + code.replace("_", "") + "__"] = esc(v[2])
    return sub


def typo_html(s):
    """Typographie française (moteur/typo.py) sur le texte affiché, hors balises, scripts et styles.
    Les textes écrits par les scripts des leçons ne sont pas touchés."""
    from moteur.typo import typo
    morceaux = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)", s, flags=re.S)
    return "".join(m if (k % 2 or not m.strip()) else typo(m) for k, m in enumerate(morceaux))


def produire(S, gabarit, lecons, sortie, logo_png, donnees):
    css = open(os.path.join(ICI, "pages", "common.css"), encoding="utf-8").read()
    js = open(os.path.join(ICI, "pages", "common.js"), encoding="utf-8").read()
    logo = "data:image/png;base64," + base64.b64encode(open(logo_png, "rb").read()).decode()
    sub = champs(S, logo)
    sub.update({"__CSS__": css, "__COMMONJS__": js, "__DATA__": json.dumps(donnees, ensure_ascii=False)})
    s = open(gabarit, encoding="utf-8").read()
    # bandeau « GABARIT » visible seulement quand on ouvre le gabarit tel quel : retiré de la page finale
    s = re.sub(r"<!--GABARIT-->.*?<!--/GABARIT-->\n?", "", s, flags=re.S)
    s = s.replace("__LESSONS__", open(lecons, encoding="utf-8").read() if os.path.exists(lecons) else "")
    for k in sorted(sub, key=len, reverse=True):
        s = s.replace(k, sub[k])
    s = typo_html(s)
    reste = sorted(set(re.findall(r"__[A-Z0-9]+__", s)))
    assert not reste, (os.path.basename(gabarit), reste)
    open(sortie, "w", encoding="utf-8").write(s)
    print("ok", os.path.basename(sortie), len(s) // 1024, "ko")


def capture(page, png, attente=20.0):
    """Haut de la page après `attente` secondes (la leçon animée a commencé), 1200 × 860 à 1,5 : 1800 × 1290 px."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path="/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None)
        pg = nav.new_page(viewport={"width": 1200, "height": 860}, device_scale_factor=1.5)
        pg.goto("file://" + os.path.abspath(page))
        pg.wait_for_timeout(int(attente * 1000))
        pg.screenshot(path=png)
        nav.close()
    from PIL import Image
    Image.open(png).convert("RGB").save(png)
