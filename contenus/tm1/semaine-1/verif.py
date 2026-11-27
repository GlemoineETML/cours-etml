# -*- coding: utf-8 -*-
"""Recalcul indépendant des résultats de la semaine 1 (REGLES 9.1), appelé par controle/controler.py.
Les valeurs de référence sont réécrites ici à la main (Floyd, fiches techniques) : on ne réutilise pas le calcul du moteur.
verifier() → liste des erreurs (vide si tout est juste)."""
import os, re
from moteur import logique as L

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "..", "sortie", "tm1", "semaine-1")

# fonctions des portes, écrites indépendamment de moteur/logique.py
PORTES = {
    "NON": lambda a, b: int(not a), "ET": lambda a, b: int(a and b), "OU": lambda a, b: int(a or b),
    "NON-ET": lambda a, b: int(not (a and b)), "NON-OU": lambda a, b: int(not (a or b)),
    "OUX": lambda a, b: int(a != b), "NON-OUX": lambda a, b: int(a == b),
}
# Floyd 3-8 p. 154 (VCC = 5 V) et fiche M74HCT00 : VIL max, VIH min, VOL max, VOH min
FLOYD_NIV = {"TTL": (0.8, 2.0, 0.4, 2.4), "HC": (1.5, 3.5, 0.33, 4.4), "HCT": (0.8, 2.0, 0.33, 4.4)}
# fiches techniques 74HC08 et 74HC04 : (entrées) → sortie, alimentation
BROCHES = {"74HC08": {"portes": [((1, 2), 3), ((4, 5), 6), ((9, 10), 8), ((12, 13), 11)], "GND": 7, "VCC": 14},
           "74HC32": {"portes": [((1, 2), 3), ((4, 5), 6), ((9, 10), 8), ((12, 13), 11)], "GND": 7, "VCC": 14},
           "74HC02": {"portes": [((2, 3), 1), ((5, 6), 4), ((8, 9), 10), ((11, 12), 13)], "GND": 7, "VCC": 14},
           "74HC04": {"portes": [((1,), 2), ((3,), 4), ((5,), 6), ((9,), 8), ((11,), 10), ((13,), 12)], "GND": 7, "VCC": 14}}
CI_74HC = {"NON": "74HC04", "ET": "74HC08", "OU": "74HC32", "NON-ET": "74HC00", "NON-OU": "74HC02", "OUX": "74HC86", "NON-OUX": "74HC7266"}
v = lambda x: f"{x:g}".replace(".", ",") + " V"


def texte(nom):
    from controle.controler import texte_docx, texte_pptx
    f = os.path.join(SORTIE, nom)
    if nom.endswith(".docx"):
        return "\n".join(texte_docx(f))
    import zipfile, html
    z = zipfile.ZipFile(f)
    notes = [html.unescape("".join(re.findall(r"<a:t>([^<]*)</a:t>", z.read(n).decode("utf-8")))) for n in z.namelist() if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)]
    return "\n".join(p for ps in texte_pptx(f).values() for p in ps) + "\n" + "\n".join(notes)


def verifier():
    E = []
    ok = lambda cond, msg: None if cond else E.append(msg)
    sp = lambda s: s.replace(" ", " ").replace(" ", " ").replace("‑", "-")

    # ---- portes : tables de vérité, chronogrammes, CI (moteur/logique.py)
    for k, f in PORTES.items():
        g = L.GATES[k]
        ok(g[9] == CI_74HC[k], f"{k} : CI {g[9]} au lieu de {CI_74HC[k]}")
        if k == "NON":
            ok(L.tdv(k) == [(a, f(a, 0)) for a in (0, 1)], f"table de vérité {k}")
        else:
            ok(L.tdv(k) == [(b, a, f(a, b)) for b in (0, 1) for a in (0, 1)], f"table de vérité {k} (ordre B A Y)")
            ok(L.chrono(k) == [f(a, b) for a, b in zip(L.CHRONO_A, L.CHRONO_B)], f"chronogramme {k}")
    ok(len({(a, b) for a, b in zip(L.CHRONO_A, L.CHRONO_B)}) == 4, "chronogramme du cours : les 4 combinaisons de A et B n'apparaissent pas")
    for ref, b in BROCHES.items():
        p = L.PINS[ref]
        ok(p[b["GND"] - 1] == "GND" and p[b["VCC"] - 1] == "VCC", f"{ref} : alimentation")
        for i, (ins, out) in enumerate(b["portes"], 1):
            ok(all(p[n - 1].startswith(str(i)) and p[n - 1][-1] in "AB" for n in ins) and p[out - 1] == f"{i}Y", f"{ref} : porte {i}")

    # ---- niveaux et marges (présentation 100, fiche 110)
    ok(L.NIV == FLOYD_NIV, "niveaux des familles différents du Floyd 3-8 p. 154")
    marge = lambda s, e: (round(FLOYD_NIV[s][3] - FLOYD_NIV[e][1], 2), round(FLOYD_NIV[e][0] - FLOYD_NIV[s][2], 2))
    ok(marge("TTL", "TTL") == (0.4, 0.4), "marges TTL")
    ok(marge("HC", "HC") == (0.9, 1.17), "marges 74HC")
    ok(marge("HC", "TTL") == (2.4, 0.47), "marges 74HC → TTL")
    t100 = sp(texte("100 Familles de circuits logiques.pptx"))
    for s_ in ["0,9 V et 1,17 V", "2,4 V et 0,47 V", "0,4 V et 0,4 V", "120 ns", "83 MHz"]:
        ok(s_ in t100, f"100 : « {s_} » introuvable")
    ok(round(1 / 12e-9 / 1e6) == 83, "12 ns ↔ 83 MHz")
    ok(10 * 12 == 120, "10 portes × 12 ns")

    # ---- fiche 110 EX C
    t110 = sp(texte("110 EX C Familles de circuits logiques.docx"))
    lab = {"TTL": "TTL", "HC": "74HC", "HCT": "74HCT"}
    for s_, e_ in (("TTL", "HC"), ("TTL", "HCT"), ("HC", "TTL"), ("HC", "HC")):
        voh, vih, vol, vil = FLOYD_NIV[s_][3], FLOYD_NIV[e_][1], FLOYD_NIV[s_][2], FLOYD_NIV[e_][0]
        nh, nl = round(voh - vih, 2), round(vil - vol, 2)
        compatible = voh >= vih and vol <= vil
        attendu = [f"{lab[s_]} → {lab[e_]}", sp(f"{v(voh)} {'≥' if voh >= vih else '<'} {v(vih)} : {'oui' if voh >= vih else 'non'}"),
                   sp(f"{v(vol)} {'≤' if vol <= vil else '>'} {v(vil)} : {'oui' if vol <= vil else 'non'}"),
                   sp(v(nh)) if nh >= 0 else "pas de marge", sp(v(nl)), "oui" if compatible else "non"]
        i = t110.find(attendu[0])
        lignes = t110[i:].split("\n")[:6] if i >= 0 else []
        ok(lignes == attendu, f"110 N°3 {attendu[0]} : {lignes} ≠ {attendu}")
    ok("48 ns" in t110 and "100 ms" in t110, "110 N°4 d) : 4 × 12 ns = 48 ns, 1 s / 10 = 100 ms")
    ok(4 * 12 == 48 and 1000 / 10 == 100, "retard de 4 portes")
    ok(5.5 < 6 < 7, "110 N°4 c)")
    for m, etat in ((0.3, "0"), (3.6, "1"), (1.5, "non garanti"), (2.2, "1"), (0.9, "non garanti")):
        attendu = "0" if m <= 0.8 else ("1" if m >= 2.0 else "non garanti")
        ok(attendu == etat, f"110 N°5 : {m} V")
        i = t110.find(sp(v(m)) + "\n" + etat + "\n")
        ok(i >= 0, f"110 N°5 : « {v(m)} → {etat} » introuvable dans le corrigé")

    # ---- fiche 130 EX C (V2 : démarrage de la voiture, TM1-A1-S2)
    t130 = sp(texte("130 EX C Portes logiques de base.docx"))
    # cahier des charges relu ici : ceinture bouclée ⇔ A = 0, sélecteur sur P ⇔ B = 1, frein enfoncé ⇔ C = 0, service ⇔ D = 1
    demarre = lambda d, c, b, a: int(b == 1 and (d == 1 or (a == 0 and c == 0)))
    T = [(d, c, b, a, demarre(d, c, b, a)) for d in (0, 1) for c in (0, 1) for b in (0, 1) for a in (0, 1)]
    ok([f"{d}{c}{b}{a}" for d, c, b, a, s_ in T if s_] == ["0010", "1010", "1011", "1110", "1111"], "130 N°1 : lignes où S = 1")
    ok("\n".join("\n".join(str(x) for x in t) for t in T) in t130, "130 N°1 : table de vérité de S introuvable dans le corrigé")
    ok(all(demarre(d, c, b, a) == PORTES["ET"](b, PORTES["OU"](d, PORTES["NON-OU"](a, c))) for d, c, b, a, _ in T), "130 N°1 d) : S = B · (D + /(A + C))")
    for s_ in ["0010, 1010, 1011, 1110 et 1111", "1,45 [kΩ]", "1,5 kΩ", "1,933 [mA]"]:
        ok(s_ in t130, f"130 : « {s_} » introuvable dans le corrigé")
    # LED : V_OH = 4,9 V, U_F = 2 V, I_F = 2 mA ; série E12 : 1,0 1,2 1,5 1,8 2,2 …
    R = (4.9 - 2) / 2e-3
    ok(round(R) == 1450 and min(x for x in (1000, 1200, 1500, 1800, 2200) if x >= R) == 1500, "130 N°4 c) : R = 1,45 kΩ → 1,5 kΩ")
    ok(round((4.9 - 2) / 1500 * 1e3, 3) == 1.933, "130 N°4 c) : contrôle 1,933 mA")
    import importlib.util
    spec = importlib.util.spec_from_file_location("fig_s1", os.path.join(ICI, "figures.py")); F = importlib.util.module_from_spec(spec); spec.loader.exec_module(F)
    deux = [k for k in PORTES if k != "NON"]
    for i, (k, A, B) in enumerate(F.MYST, 1):
        Y = [PORTES[k](a, b) for a, b in zip(A, B)]
        possibles = [g for g in deux if [PORTES[g](a, b) for a, b in zip(A, B)] == Y]
        ok(possibles == [k], f"130 N°3 chronogramme {i} : portes compatibles {possibles} (une seule attendue : {k})")
    Y2 = [PORTES["NON-OU"](a, b) for a, b in zip(F.N2_A, F.N2_B)]
    ok(Y2 == L.chrono("NON-OU", F.N2_A, F.N2_B), "130 N°2 b) : chronogramme de S = /(A + B)")
    return E
