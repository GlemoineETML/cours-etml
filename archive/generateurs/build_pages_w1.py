#!/usr/bin/env python3
"""Pages interactives 101 (Familles de circuits logiques) et 121 (Portes logiques et tables de vérité).
Une page HTML autonome par présentation : CSS, JS et logo intégrés ; données tirées de w1_data.py.
Liens FutureMEM sans préfixe microsoft-edge: (dans le navigateur, l'ancre « # » est conservée).
Usage : python3 build_pages_w1.py   →   pages/101 ….html, pages/121 ….html
"""
import base64, json, os
import w1_data as D

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pages")
css = open(os.path.join(P, "common.css"), encoding="utf-8").read()
js = open(os.path.join(P, "common.js"), encoding="utf-8").read()
logo = "data:image/png;base64," + base64.b64encode(open(os.path.join(HERE, "logo_white_h.png"), "rb").read()).decode()

GATES = {k: {"nom": v[0], "en": v[1], "regle": v[8], "ci74": v[9], "ci4000": v[10], "contenu": v[11], "sec": v[12], "page": v[13]}
         for k, v in D.GATES.items()}
DATA = {"GATES": GATES, "ORDER": D.ORDER, "NIV": D.NIV, "CHRONO_A": D.CHRONO_A, "CHRONO_B": D.CHRONO_B}

esc = lambda u: u.replace("&", "&amp;")
SUB = {
    "__CSS__": css, "__COMMONJS__": js, "__LOGO__": logo, "__DATA__": json.dumps(DATA, ensure_ascii=False),
    "__CHAMP__": esc(D.FUTUREMEM_CHAMP),
    "__FL1__": esc(D.floyd_url(1)), "__FL3__": esc(D.floyd_url(3)),
    "__FLNOTE__": D.FLOYD_NOTE,
    "__NXREPR__": esc(D.NEXTEC["repr"][0]), "__NXFAM__": esc(D.NEXTEC["fam"][0]),
    "__T100__": esc(D.TEAMS_100), "__T120__": esc(D.teams(D.F120, "p")),
}
for code, v in D.LZ.items():
    SUB["__" + code.replace("_", "") + "__"] = esc(v[2])

for tpl, les, out in (("tpl_101.html", "lessons_101.js", "101 Familles de circuits logiques.html"),
                      ("tpl_121.html", "lessons_121.js", "121 Portes logiques et tables de vérité.html")):
    s = open(os.path.join(P, tpl), encoding="utf-8").read()
    # bandeau « GABARIT » visible seulement quand on ouvre le gabarit tel quel (dans le projet) : retiré de la page finale
    s = __import__("re").sub(r"<!--GABARIT-->.*?<!--/GABARIT-->\n?", "", s, flags=__import__("re").S)
    # leçons animées (« Comprendre ») : un fichier JS par page, inséré à la fin du script de la page
    s = s.replace("__LESSONS__", open(os.path.join(P, les), encoding="utf-8").read() if os.path.exists(os.path.join(P, les)) else "")
    for k in sorted(SUB, key=len, reverse=True):
        s = s.replace(k, SUB[k])
    left = [w for w in set(__import__("re").findall(r"__[A-Z0-9]+__", s))]
    assert not left, (tpl, left)
    open(os.path.join(P, out), "w", encoding="utf-8").write(s)
    print("ok", out, len(s) // 1024, "ko")
