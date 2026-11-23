# -*- coding: utf-8 -*-
"""110 EX Familles de circuits logiques (+ corrigé 110 EX C) · TM1 – El DT 1 · semaine 1.
Objectifs LZ_4255 et LZ_4256. Toutes les valeurs de niveaux viennent de moteur/logique.py, NIV (Floyd 3-8 p. 154, fiche M74HCT00)."""
from moteur.fiche import RED, GREY, NAVY, TW, WD_ALIGN_PARAGRAPH, Pt, Cm
from moteur import logique as L

TITLE = "Familles de circuits logiques"
S = CTX = None                        # fixés par produire(ctx)
fl = lambda *a: S.floyd_url(*a)
LZ = lambda c: (c, S.lz_link(c))      # lien propre à chaque LZ, via Edge
v = lambda x: f"{x:g}".replace(".", ",") + " V"


def build(corr, out):
    x = CTX.doc(corr, out, TITLE, "Corrigé" if corr else "Exercices",
            "110 EX Familles de circuits logiques – " + ("Corrigé" if corr else "Exercices") + " – El DT 1",
            f"{S.matiere} – {S.classe} – {S.annee}")
    x.head(TITLE,
           [(f"Fiche d'exercices · {S.matiere} · Classe {S.classe} · {S.annee} · Champ\u00a0", None), (S.champ, S.fm(S.futuremem_champ)),
            (" · Objectifs\u00a0", None), LZ("LZ_4255"), (", ", None), LZ("LZ_4256")],
           ["Déroulement (enseignant·e) : 45 min, en binôme, après la présentation 100 (diapositives 1 à 19).",
            "Temps indicatifs : N°1 8 min, N°2 8 min, N°3 12 min, N°4 10 min, N°5 7 min. Distribuer la fiche technique M74HCT00 (STMicroelectronics) avant le N°4.",
            "Toutes les tensions du N°3 sont les valeurs garanties du Floyd 3-8 p. 154 (V_{CC} = 5 V) ; le 74HCT a les seuils d'entrée TTL (fiche M74HCT00) et les sorties du 74HC.",
            "Correction : en plénière, en faisant justifier chaque réponse par une valeur. Ramasser l'auto-évaluation."],
           ["**Consignes :** travail en binôme, 45 min. Tu peux utiliser la présentation 100 et la fiche technique du M74HCT00. "
            "Justifie chaque réponse avec une valeur (tension, courant, température ou temps)."],
           [("Floyd, ", [("chap. 3 Portes logiques", fl(3)), (" : 3-8 Logique à fonction fixe : ", None), ("références 74xxyy p. 146", fl(3, 146)), (" · ", None),
                         ("familles p. 150", fl(3, 150)), (" · ", None), ("délai de propagation p. 152", fl(3, 152)), (" · ", None),
                         ("niveaux logiques p. 154", fl(3, 154))]),
            ("Floyd, ", [("chap. 1 Concepts numériques", fl(1)), (" : ", None), ("1-6 Circuits intégrés à fonction fixe, boîtiers (p. 26-28)", fl(1, 26))]),
            ("Pages du Floyd : ", [(S.floyd_note, None)]),
            ("Présentation : ", [(S.fichier("100"), S.teams_url("100")), (" (diapositives 3 à 18) · pour réviser : ", None),
                                 ("page interactive 101", S.teams_url("101")), (" (Edge ou Chrome) · ", None), ("animation 105", S.teams_url("105"))]),
            ("nextecmedia : ", [(S.nextec["fam"][1].replace("nextecmedia, ", ""), S.nextec["fam"][0])])])
    x.CTX("tu fais ton stage au service de maintenance d'une entreprise d'embouteillage. La ligne de remplissage de boissons "
          "est pilotée par des cartes électroniques de plusieurs générations : une ancienne carte en TTL, des cartes récentes en 74HC "
          "et un module à microcontrôleur alimenté en 3,3 V. Ton formateur te confie quelques vérifications.")

    # ---------------------------------------------------------------- N°1
    x.EX(1, "Lire une référence de CI (≈ 8 min)", [("Présentation diapositives 4 et 5", S.teams_url("100")), ("Floyd 3-8 p. 146", fl(3, 146))])
    x.CTX("au magasin de pièces de rechange, les tiroirs sont étiquetés avec la référence complète des CI.")
    x.Q("a)", "Décode les trois références. Aide : chez Texas Instruments, le boîtier N est un DIP en plastique, D un SOIC et J un DIP en céramique.")
    rows = [["Référence", "Fabricant", "Plage de température", "Technologie", "Fonction", "Boîtier"]]
    data = [("SN74HC08N", "Texas Instruments", "74 : commerciale", "HC : CMOS", "08 : 4 portes ET à 2 entrées", "N : DIP plastique"),
            ("SN74LS32D", "Texas Instruments", "74 : commerciale", "LS : TTL (bipolaire)", "32 : 4 portes OU à 2 entrées", "D : SOIC"),
            ("SN54HC04J", "Texas Instruments", "54 : militaire (−55 … 125 °C)", "HC : CMOS", "04 : 6 inverseurs", "J : DIP céramique")]
    for r_ in data:
        rows.append([r_[0]] + [("R", c) for c in r_[1:]])
    x.TABLE([2.6, 2.4, 3.1, 2.7, 3.4, TW - 14.2 - 0.02], rows, height=0.95, size=9)
    x.Q("b)", "Le tiroir des SN74HC00N est vide. Il reste des CD4011BE, qui contiennent aussi 4 portes NON-ET à 2 entrées. Peux-tu les monter à la place ? Pourquoi ?")
    x.ANS("Non. La fonction est la même, mais le CD4011 appartient à la série 4000 : son brochage est différent de celui de la série 74 "
          "(diapositive 4). Il faudrait modifier la carte.", 2)

    # ---------------------------------------------------------------- N°2
    x.HR(); x.EX(2, "Choisir le bon CI (≈ 8 min)", [("Présentation diapositives 3, 7 et 8", S.teams_url("100")), ("Floyd 3-8 p. 150", fl(3, 150))])
    x.Q("a)", "Sur l'ancienne carte TTL alimentée en 5 V, un 74LS00 est défectueux. Ses entrées sont pilotées par d'autres CI TTL. "
              "Le magasin propose un 74HC00, un 74HCT00 et un CD4011BE. Lequel choisis-tu ? Pourquoi pas les deux autres ?")
    x.ANS("Le 74HCT00 : même fonction, même brochage (série 74) et des entrées compatibles TTL ($V_{IH}$ = 2 V ≤ $V_{OH}$ = 2,4 V des sorties TTL).\n"
          "Le 74HC00 a $V_{IH}$ = 3,5 V : les 2,4 V d'une sortie TTL ne donnent pas un 1 garanti. Le CD4011BE n'a pas le même brochage.", 3)
    x.Q("b)", "Le capteur de niveau de la cuve est monté à l'extérieur du bâtiment : −20 °C en hiver, 40 °C en été. Quelle plage de température commandes-tu ?")
    x.ANS("La plage « Industrial » (−40 … 85 °C). La plage « Consumer » (0 … 70 °C) ne descend pas à −20 °C.", 1)
    x.Q("c)", "Un compteur de bouteilles portable fonctionne sur pile. Quelle technologie privilégies-tu ? Pourquoi ?")
    x.ANS("Le CMOS (par exemple 74HC) : sa consommation au repos est très faible, la pile dure plus longtemps qu'avec du TTL.", 1)

    # ---------------------------------------------------------------- N°3
    x.HR(); x.EX(3, "Les niveaux sont-ils compatibles ? (≈ 12 min)", [("Présentation diapositives 16 et 17", S.teams_url("100")), ("Floyd 3-8 p. 154", fl(3, 154))])
    x.CTX("le formateur veut relier entre elles des cartes de générations différentes. Avant de câbler, tu vérifies les niveaux logiques.")
    x.P("Valeurs garanties, V_{CC} = 5 V :", keep=True, size=10, after=2)
    nv = [["Famille", "V_{IL} max", "V_{IH} min", "V_{OL} max", "V_{OH} min"]]
    for fam, lab in (("TTL", "TTL"), ("HC", "74HC"), ("HCT", "74HCT")):
        a, b_, c, d_ = L.NIV[fam]
        nv.append([lab, v(a), v(b_), v(c), v(d_)])
    x.TABLE([3.0, 2.6, 2.6, 2.6, 2.6], nv, height=0.5, size=10)
    x.Q("a)", "Complète le tableau. Règle : la liaison est compatible si $V_{OH}$(sortie) ≥ $V_{IH}$(entrée) et $V_{OL}$(sortie) ≤ $V_{IL}$(entrée). "
              "Marges de bruit : $N_{H}=V_{OH}-V_{IH}$ et $N_{L}=V_{IL}-V_{OL}$.")
    rows = [["Sortie → entrée", "V_{OH} ≥ V_{IH} ?", "V_{OL} ≤ V_{IL} ?", "N_{H}", "N_{L}", "Compatible ?"]]
    LAB = {"TTL": "TTL", "HC": "74HC", "HCT": "74HCT"}
    for s_, e_ in (("TTL", "HC"), ("TTL", "HCT"), ("HC", "TTL"), ("HC", "HC")):
        okh, okl, nh, nl = L.compat(s_, e_)
        voh, vih = L.NIV[s_][3], L.NIV[e_][1]
        vol, vil = L.NIV[s_][2], L.NIV[e_][0]
        rows.append([f"{LAB[s_]} → {LAB[e_]}",
                     ("R", f"{v(voh)} {'≥' if okh else '<'} {v(vih)} : {'oui' if okh else 'non'}"),
                     ("R", f"{v(vol)} {'≤' if okl else '>'} {v(vil)} : {'oui' if okl else 'non'}"),
                     ("R", v(nh) if nh >= 0 else "pas de marge"), ("R", v(nl)),
                     ("R", "oui" if (okh and okl) else "non")])
    x.TABLE([2.9, 3.6, 3.6, 2.1, 2.1, TW - 14.3 - 0.02], rows, height=0.6, size=9.5)
    x.Q("b)", "Le module à microcontrôleur alimenté en 3,3 V doit commander une entrée de 74HC alimenté en 5 V. Sa sortie haute vaut au mieux 3,3 V. "
              "Le 1 est-il garanti ? Que proposes-tu ?")
    x.ANS(f"Non : 3,3 V < $V_{{IH}}$ = {v(L.NIV['HC'][1])}. On intercale un 74HCT ($V_{{IH}}$ = {v(L.NIV['HCT'][1])}, donc 3,3 V est un 1) ou un convertisseur de niveaux.", 2)
    x.Q("c)", "Dans l'autre sens, une sortie de 74HC alimenté en 5 V peut-elle aller directement sur une entrée du microcontrôleur 3,3 V ?")
    x.ANS(f"Non : un 1 vaut au moins {v(L.NIV['HC'][3])}, au-dessus de la tension maximale d'une entrée 3,3 V. L'entrée peut être détruite : il faut un convertisseur de niveaux (question de départ de la présentation 100).", 2)
    x.BOX(["Si difficulté",
           "Dessine les deux échelles de tension côte à côte, la sortie à gauche et l'entrée à droite, comme à la diapositive 17. "
           "La zone 1 de la sortie doit tomber entièrement dans la zone 1 de l'entrée, et la zone 0 dans la zone 0."], only_corr=False)

    # ---------------------------------------------------------------- N°4
    x.HR(); x.EX(4, "Lire la fiche technique du M74HCT00 (≈ 10 min)", [("Présentation diapositives 14 à 18", S.teams_url("100")), ("Floyd 3-8 p. 151-153", fl(3, 151))])
    x.CTX("la carte de commande de la vanne de remplissage utilise un M74HCT00 (4 portes NON-ET à 2 entrées). Tu prépares son remplacement.")
    x.TABLE([6.4, 5.0, TW - 11.4 - 0.02], [
        ["Extrait de la fiche", "Recommandé", "Limite absolue"],
        ["Tension d'alimentation V_{CC}", "4,5 … 5,5 V", "−0,5 … +7 V"],
        ["Température", "−55 … 125 °C", "stockage −65 … 150 °C"],
        ["Courant d'une sortie", "–", "± 25 mA"],
        ["V_{IH} min / V_{IL} max", "2 V / 0,8 V", "–"],
        ["t_{PD} typique (V_{CC} = 4,5 V)", "12 ns", "–"]], height=0.5, size=10, keep_after=True)
    x.IMG("fig_pinout.png", 3.8, keep=True, after=2)
    x.P("Brochage du M74HCT00 (vue de dessus)", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=9, color=GREY, after=4)
    x.Q("a)", "Sur quelles broches branches-tu l'alimentation ?")
    x.ANS("Broche 14 : $V_{CC}$ (+5 V). Broche 7 : GND.", 1)
    x.Q("b)", "Quelles broches correspondent aux entrées et à la sortie de la porte n° 3 ?")
    x.ANS("Entrées 3A = broche 9 et 3B = broche 10, sortie 3Y = broche 8.", 1)
    x.Q("c)", "L'alimentation de laboratoire est réglée par erreur sur 6 V. Le CI est-il détruit ? Fonctionne-t-il correctement ?")
    x.ANS("Il n'est pas détruit : 6 V reste sous la limite absolue de 7 V. Mais 6 V dépasse la valeur recommandée (5,5 V) : "
          "le fonctionnement n'est plus garanti. On règle 5 V avant de continuer.", 2)
    x.Q("d)", "Le signal du capteur de bouteille traverse 4 portes NON-ET en série. Calcule le retard typique. "
              "La ligne remplit 10 bouteilles par seconde : ce retard pose-t-il un problème ?")
    x.ANS("$4\\cdot 12\\u{ ns}=48\\u{ ns}$. Entre deux bouteilles, il s'écoule $\\f{1\\u{ s}}{10}=100\\u{ ms}$ : le retard est négligeable.", 2)
    x.Q("e)", "Peux-tu brancher directement le voyant « vanne ouverte », une LED de 20 mA, sur une sortie du CI ?")
    x.ANS("Non : 20 mA est presque la limite absolue de 25 mA, et les niveaux de sortie ne sont plus garantis à ce courant. "
          "On commande la LED avec un transistor (diapositive 8).", 2)

    # ---------------------------------------------------------------- N°5
    x.HR(); x.EX(5, "Dépannage : mesurer les niveaux (≈ 7 min)", [("Présentation diapositives 11 et 16", S.teams_url("100")), ("Floyd 3-8 p. 154", fl(3, 154))])
    x.CTX("le convoyeur s'arrête sans raison apparente. Sur la carte de commande (74HCT00, V_{CC} = 5 V), tu mesures au multimètre la tension de plusieurs entrées, par rapport à GND.")
    x.Q("a)", f"Quel état la porte lit-elle ? Rappel : $V_{{IL}}$ max = {v(L.NIV['HCT'][0])}, $V_{{IH}}$ min = {v(L.NIV['HCT'][1])}.")
    rows = [["Tension mesurée", "État lu (0, 1 ou non garanti)", "Justification"]]
    vil, vih = L.NIV["HCT"][0], L.NIV["HCT"][1]
    for m in (0.3, 3.6, 1.5, 2.2, 0.9):
        if m <= vil: st, js = "0", f"{v(m)} ≤ {v(vil)}"
        elif m >= vih: st, js = "1", f"{v(m)} ≥ {v(vih)}"
        else: st, js = "non garanti", f"entre {v(vil)} et {v(vih)}"
        rows.append([v(m), ("R", st), ("R", js)])
    x.TABLE([3.4, 5.6, TW - 9.0 - 0.02], rows, height=0.5, size=10)
    x.Q("b)", "L'entrée mesurée à 1,5 V n'est reliée à rien : un fil est coupé. Pourquoi est-ce un problème sur un CI CMOS ? Que faut-il faire ?")
    x.ANS("Une entrée CMOS en l'air prend une tension quelconque : la porte peut lire un 0 ou un 1 au hasard, et le CI peut chauffer. "
          "On répare la liaison. Une entrée inutilisée se relie toujours à $V_{CC}$ ou à GND.", 2)

    # ---------------------------------------------------------------- auto-évaluation (fiche élève seulement, REGLES 4)
    if not corr:
        x.P("**Auto-évaluation**", keep=True, after=1, before=10, color=NAVY)
        x.P("Après la correction : ✓ je sais seul·e · ~ avec une aide · ✗ à revoir (reprends la diapositive indiquée).", keep=True, size=10)
        x.TABLE([TW / 5 - 0.01] * 5, [["Lire une référence (N°1, diapo 5)", "Choisir une famille (N°2, diapos 3 et 8)", "Compatibilité des niveaux (N°3, diapo 17)",
                                       "Fiche technique (N°4, diapos 14 à 18)", "Mesurer un niveau (N°5, diapo 16)"], ["", "", "", "", ""]],
                height=0.75, size=9, first_left=False)
    x.finish()


def produire(ctx):
    global S, CTX
    S, CTX = ctx.S, ctx
    build(False, ctx.sortie_de("110"))
    build(True, ctx.sortie_de("110C"))
