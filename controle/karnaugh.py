# -*- coding: utf-8 -*-
"""Contrôle des tableaux de Karnaugh (REGLES 3.5), à partir de la géométrie écrite par moteur/cei.fig_karnaugh
dans sortie/_travail/<séance>/karnaugh_figures.json. Erreurs bloquantes :
  - un terme manque (groupe sans terme) ;
  - le trait d'un terme n'est pas à 45° puis horizontal ;
  - un terme chevauche le tableau, une bande des codes, une zone jaune, une lettre ou un autre terme ;
  - un trait passe dans une région interdite (bandes, zones A et C, lettres) ou croise un autre trait ;
  - un trait passe sur un chiffre du tableau (moins de 0,25 case du centre) ;
  - un groupe a un côté posé sur le bord du tableau (un groupe coupé par un bord doit s'ouvrir vers l'extérieur)."""
import json, os


def _croise(p1, p2, p3, p4):
    o = lambda a, b, c: (lambda v: (v > 1e-9) - (v < -1e-9))((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
    return o(p1, p2, p3) * o(p1, p2, p4) < 0 and o(p3, p4, p1) * o(p3, p4, p2) < 0


def _dans(p, q, r):
    return any(r[0] < p[0] + (q[0] - p[0]) * k / 40 < r[2] and r[1] < p[1] + (q[1] - p[1]) * k / 40 < r[3] for k in range(41))


def _chev(a, b):
    return a[0] < b[2] - 1e-6 and b[0] < a[2] - 1e-6 and a[1] < b[3] - 1e-6 and b[1] < a[3] - 1e-6


def _dist(c, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = 0 if dx == dy == 0 else max(0, min(1, ((c[0] - a[0]) * dx + (c[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return ((c[0] - a[0] - t * dx) ** 2 + (c[1] - a[1] - t * dy) ** 2) ** 0.5


def verifier(travail):
    f = os.path.join(travail, "karnaugh_figures.json")
    if not os.path.exists(f):
        return []
    E = []
    for nom, r in json.load(open(f, encoding="utf-8")).items():
        u, T = r["cote"], r["tableau"]
        x0, Y1, X1, y0 = T
        err = lambda m: E.append(f"Karnaugh · {nom} : {m}")
        for g in r["groupes"]:
            for b in g["blocs"]:
                for (p, q) in b["segments"]:
                    if (abs(p[0] - q[0]) < 1e-6 and min(abs(p[0] - x0), abs(p[0] - X1)) < 1e-6) or \
                       (abs(p[1] - q[1]) < 1e-6 and min(abs(p[1] - y0), abs(p[1] - Y1)) < 1e-6):
                        err(f"le groupe {g['k']} a un côté sur le bord du tableau (il doit s'ouvrir vers l'extérieur)")
        if r.get("avec_termes") and len(r["termes"]) < len(r["groupes"]):
            err(f"{len(r['groupes']) - len(r['termes'])} groupe(s) sans terme")
        traits = []
        for t in r["termes"]:
            P, S, E_, F = t["depart"], t["sortie"], t["coude"], t["fin"]
            if abs(abs(E_[0] - P[0]) - abs(E_[1] - P[1])) > 1e-3 * u or abs(F[1] - E_[1]) > 1e-6:
                err(f"le trait du terme {t['terme']} n'est pas à 45° puis horizontal")
            bx = t["cadre"]
            for z in [T] + r["zones"] + r["zones_traversables"]:
                if _chev(bx, z):
                    err(f"le terme {t['terme']} chevauche le tableau, une bande, une zone ou une lettre"); break
            if any(_dans(a, b, z) for a, b in ((S, E_), (E_, F)) for z in r["zones"]):
                err(f"le trait du terme {t['terme']} passe sur une bande, une zone A ou C ou une lettre")
            if any(_dist(c, P, S) < 0.25 * u for c in r["textes"]):
                err(f"le trait du terme {t['terme']} passe sur un chiffre du tableau")
            for (a, b) in ((P, E_), (E_, F)):
                if any(_croise(a, b, c, d) for c, d in traits):
                    err(f"le trait du terme {t['terme']} croise un autre trait")
            traits += [(P, E_), (E_, F)]
        cadres = [t["cadre"] for t in r["termes"]]
        for i in range(len(cadres)):
            for j in range(i + 1, len(cadres)):
                if _chev(cadres[i], cadres[j]):
                    err(f"les termes {r['termes'][i]['terme']} et {r['termes'][j]['terme']} se chevauchent")
    return E
