# -*- coding: utf-8 -*-
"""130 EX Portes logiques de base (+ corrigé 130 EX C) · TM1 – El DT 1 · semaine 1.
Partie A : fiche à compléter pour les 7 portes (symbole CEI, table de vérité, équation, règle, chronogramme, CI, exemple réel).
Partie B : exercices sur la ligne de remplissage (LZ_4242, LZ_27, LZ_29, LZ_2223).
Remplace l'ancienne fiche « Portes logiques de base » (C. Moser, 2020). Valeurs calculées par moteur/logique.py et figures.py."""
from moteur.fiche import RED, GREY, NAVY, BLUE, TW, WD_ALIGN_PARAGRAPH, Pt, Cm, hyperlink, rich, p_border
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from moteur import logique as L

TITLE = "Portes logiques de base"
S = CTX = None                        # fixés par produire(ctx)
T120 = None
MYST = N2_A = N2_B = None             # chronogrammes de figures.py
fl = lambda *a: S.floyd_url(*a)
LZ = lambda c: (c, S.lz_link(c))      # lien propre à chaque LZ, via Edge
EXEMPLES = {
    "NON": "Voyant « cuve vide » : il s'allume (Y = 1) quand le capteur de niveau N vaut 0.",
    "ET": "Vanne de remplissage : elle s'ouvre seulement si une bouteille est sous le bec (B = 1) et si le niveau de la cuve est suffisant (N = 1).",
    "OU": "Voyant « défaut » : il s'allume si la pompe ou le convoyeur est en défaut (ou les deux).",
    "NON-ET": "Voyant « remplir » : il s'allume dès qu'une des deux cuves (sirop ou eau) manque de liquide.",
    "NON-OU": "Autorisation du convoyeur : il peut tourner seulement si aucun des deux arrêts d'urgence n'est actionné.",
    "OUX": "Éclairage d'escalier en va-et-vient : chaque interrupteur change l'état de la lampe. L'OU exclusif sert aussi à additionner deux bits (semaine 4).",
    "NON-OUX": "Deux capteurs de niveau redondants : le signal « capteurs cohérents » vaut 1 quand les deux donnent la même valeur.",
}
SLIDE = {"NON": 5, "ET": 6, "OU": 7, "NON-ET": 8, "NON-OU": 9, "OUX": 10, "NON-OUX": 11}


def shade(c, fill):
    tcPr = c._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), fill); tcPr.append(sh)


def dots(p, width):
    p.paragraph_format.tab_stops.add_tab_stop(Cm(width), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    p.add_run("\t")


def gate_block(x, key, idx):
    g = L.GATES[key]
    nom, en, n = g[0], g[1], g[4]
    corr = x.corr
    # titre de la porte
    p = x.d.add_paragraph(); f = p.paragraph_format; f.space_before = Pt(10); f.space_after = Pt(3); f.keep_with_next = True
    f.page_break_before = idx in ((3, 5, 7) if corr else (2, 4, 6))   # deux portes par page ; corrigé : l'encadré enseignant repousse A.1 en page 2
    r = p.add_run(f"A.{idx} Porte {nom} ({en})"); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = NAVY
    q = x.P("", italic=True, size=9, color=GREY, keep=True, after=3)
    hyperlink(q, fl(3, g[13]), f"Floyd {g[12]} p. {g[13]}", size=9); rich(q, " · ", size=9, color=GREY)
    hyperlink(q, T120, f"Présentation 120, diapositive {SLIDE[key]}", size=9)
    # tableau : symbole | table de vérité | équation et règle
    tdv = L.tdv(key)
    ins = ["A"] if n == 1 else ["B", "A"]      # du poids fort au poids faible ; L.tdv() donne (B, A, Y)
    cols = 1 + len(ins) + 1 + 1
    wsym, wv = 4.4, 1.15
    weq = TW - wsym - wv * (len(ins) + 1) - 0.02
    widths = [wsym] + [wv] * (len(ins) + 1) + [weq]
    nrows = 1 + len(tdv) + 2          # en-tête, table de vérité, chronogramme, CI et exemple (un seul tableau : il ne se coupe pas)
    t = x.d.add_table(rows=nrows, cols=cols); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    heads = ["Symbole CEI"] + ins + ["Y", "Équation et règle"]
    for j, h in enumerate(heads):
        x.cell_txt(t.cell(0, j), h, bold=True, color=NAVY, shade="ACCBF9", size=10)
    for i, row in enumerate(tdv, start=1):
        for j, val in enumerate(row):
            c = t.cell(i, 1 + j)
            last = j == len(row) - 1
            if last:
                x.cell_txt(c, str(val) if corr else "", bold=True, color=RED if corr else None, size=11)
            else:
                x.cell_txt(c, str(val), size=11)
    nt = len(tdv)
    sym = t.cell(1, 0).merge(t.cell(nt, 0))
    eq = t.cell(1, cols - 1).merge(t.cell(nt, cols - 1))
    chr_ = t.cell(nt + 1, 0).merge(t.cell(nt + 1, cols - 1))
    inf = t.cell(nt + 2, 0).merge(t.cell(nt + 2, cols - 1))
    for c in (sym, eq, chr_, inf):
        for extra in c.paragraphs[1:]:
            extra._p.getparent().remove(extra._p)
    sym.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    x.IMG(f"gate_{key}.png", 3.5, parent=sym, after=0)
    eq.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = eq.paragraphs[0]; p.paragraph_format.space_after = Pt(4); p.paragraph_format.space_before = Pt(2)
    r = p.add_run("Équation : "); r.bold = True; r.font.size = Pt(10)
    if corr:
        x.EQ(p, g[7], "EE0000", 24)
    else:
        dots(p, weq - 0.4)
    p2 = eq.add_paragraph(); p2.paragraph_format.space_after = Pt(2)
    r = p2.add_run("Règle : "); r.bold = True; r.font.size = Pt(10)
    if corr:
        rich(p2, g[8], color=RED, size=10)
    else:
        dots(p2, weq - 0.4)
        p3 = eq.add_paragraph(); p3.paragraph_format.space_after = Pt(2); dots(p3, weq - 0.4)
    # chronogramme
    p = chr_.paragraphs[0]; p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(0)
    rich(p, "Chronogramme : ", bold=True, size=10); rich(p, "Y en rouge." if corr else "dessine Y.", size=10)
    x.IMG(f"chrono_{key}_{'corr' if corr else 'q'}.png", 9.6 if n == 2 else 6.2, parent=chr_, after=2)
    # CI et exemple
    p = inf.paragraphs[0]; p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(1); p.paragraph_format.line_spacing = 1.15
    rich(p, "CI : ", bold=True, size=10); rich(p, f"{g[9]} ({g[11]}) · série 4000 : {g[10]}", size=10)
    p = inf.add_paragraph(); p.paragraph_format.space_after = Pt(3); p.paragraph_format.line_spacing = 1.15
    rich(p, "Dans la vraie vie : ", bold=True, size=10, color=BLUE); rich(p, EXEMPLES[key], size=10)
    for j, w in enumerate(widths): t.columns[j].width = Cm(w)
    for k_, tr in enumerate(t.rows):
        tr._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        if 1 <= k_ <= nt: tr.height = Cm(0.85 if n == 1 else 0.62)   # NON : 2 lignes aussi hautes que le cadre équation
        if k_ < nrows - 1:
            for c in tr.cells:
                for pp in c.paragraphs: pp.paragraph_format.keep_with_next = True
    if idx + 1 not in ((3, 5, 7) if corr else (2, 4, 6)):      # pas d'espaceur avant un saut de page (sinon page blanche)
        spc = x.d.add_paragraph(); spc.paragraph_format.space_after = Pt(4)


def build(corr, out):
    x = CTX.doc(corr, out, TITLE, "Corrigé" if corr else "Fiche",
            "130 EX Portes logiques de base – " + ("Corrigé" if corr else "Fiche et exercices") + " – El DT 1",
            f"{S.matiere} – {S.classe} – {S.annee}")
    x.head(TITLE,
           [(f"Fiche à compléter et exercices · {S.matiere} · Classe {S.classe} · {S.annee} · Champ\u00a0", None), (S.champ, S.fm(S.futuremem_champ)), (" · Objectifs\u00a0", None),
            LZ("LZ_4242"), (", ", None), LZ("LZ_130"), (", ", None), LZ("LZ_29"), (", ", None), LZ("LZ_27"), (", ", None), LZ("LZ_2223")],
           ["Déroulement (enseignant·e) : partie A pendant la présentation 120, partie B en binôme",
            "Partie A : NON, ET et OU avec la classe (diapositives 5 à 7), NON-ET à NON-OU exclusif en autonomie (diapositives 8 à 11), correction avec la diapositive 12 (≈ 20 min). "
            "Partie B : 45 min (N°1 : 12 min ; N°2 : 10 min ; N°3, N°4 : 8 min chacun ; N°5 : 7 min)."],
           ["**Consignes :** partie A, pendant la présentation 120, complète pour chaque porte la colonne Y, l'équation, la règle et le chronogramme (le CI et l'exemple réel sont donnés). Partie B, travail en binôme, 45 min. "
            "Écris toujours la règle ou l'intervalle qui justifie ta réponse.",
            "**Conventions :** 1 = niveau HAUT = actif, 0 = niveau BAS. Équations notées comme dans le Floyd : point = ET, plus = OU, "
            "barre au-dessus = NON, ⊕ = OU exclusif. Les entrées s'appellent A et B, la sortie Y. "
            "Une table de vérité à n entrées compte 2^{n} lignes, rangées dans l'ordre du comptage binaire. "
            "Les colonnes d'entrée vont du poids fort au poids faible (B A, ou C B A ; A est toujours le poids faible), puis vient la sortie."],
           [("Floyd, ", [("chap. 1 Concepts numériques", fl(1)), (" : ", None), ("1-2 Niveaux logiques et chronogrammes (p. 5-10)", fl(1, 5)),
                         (" · ", None), ("1-3 Opérations logiques de base (p. 11-12)", fl(1, 11))]),
            ("Floyd, ", [("chap. 3 Portes logiques", fl(3)), (" : ", None), ("3-1 à 3-6 Inverseur à NON-OU exclusif (p. 112-138)", fl(3, 112)),
                         (" · ", None), ("3-8 CI de la série 74 (p. 146-149)", fl(3, 146))]),
            ("Pages du Floyd : ", [(S.floyd_note, None)]),
            ("nextecmedia : ", [("1.1 Introduction à la technique numérique", S.nextec["intro"][0]), (" · ", None),
                                ("1.2.1 Formes de représentation des circuits numériques", S.nextec["repr"][0])]),
            ("Présentations : ", [(S.fichier("120"), T120), (" · ", None), (S.fichier("100"), S.teams_url("100")), (" · pour réviser : ", None),
                                  ("page interactive 121", S.teams_url("121")), (" (Edge ou Chrome) · ", None), ("animation 125", S.teams_url("125"))])])

    # ================= PARTIE A
    h = x.d.add_heading("Partie A : les sept portes de base", level=1); h.paragraph_format.page_break_before = corr
    for i, k in enumerate(L.ORDER, 1):
        gate_block(x, k, i)

    # ================= PARTIE B
    h = x.d.add_heading("Partie B : exercices sur la ligne de remplissage", level=1); h.paragraph_format.page_break_before = True
    x.CTX("la ligne de remplissage de boissons de la présentation 120 (diapositive 2). Les capteurs donnent 1 quand ce qu'ils surveillent est vrai ; "
          "un actionneur est en marche quand sa sortie vaut 1.")
    x.IMG("fig_ligne.png", 15.0, after=4)

    # ---- N°1
    x.EX(1, "Du cahier des charges à la table de vérité (≈ 12 min)", [(f"Présentation 120, diapositives 2 et 3", T120), ("Floyd 1-2 p. 5", fl(1, 5)), LZ("LZ_4242")])
    x.P("Cahier des charges : le moteur M du convoyeur d'entrée doit tourner quand le capteur E détecte une bouteille en attente (E = 1) "
        "et que la zone de remplissage est libre (L = 1). Il ne doit jamais tourner quand l'arrêt d'urgence est actionné (U = 1).", keep=True, after=3)
    x.Q("a)", "Complète le tableau des entrées et des sorties.")
    x.TABLE([2.4, 4.4, TW - 6.8 - 0.02], [["Variable", "Entrée ou sortie ?", "Elle vaut 1 quand…"],
                                         ["E", ("R", "entrée (capteur)"), ("R", "une bouteille attend à l'entrée")],
                                         ["L", ("R", "entrée (capteur)"), ("R", "la zone de remplissage est libre")],
                                         ["U", ("R", "entrée (bouton)"), ("R", "l'arrêt d'urgence est actionné")],
                                         ["M", ("R", "sortie (actionneur)"), ("R", "le moteur du convoyeur tourne")]], height=0.55, size=10)
    x.Q("b)", "Combien de lignes compte la table de vérité ? Pourquoi ?")
    x.ANS("3 entrées → $2^{3}=8$ lignes : toutes les combinaisons de E, L et U.", 1)
    x.Q("c)", "Dessine la table de vérité : colonnes E L U (E poids fort, U poids faible), lignes dans l'ordre du comptage binaire (000 à 111), puis la sortie M.")
    rows = [["E", "L", "U", "M"]]
    for e in (0, 1):
        for l in (0, 1):
            for u in (0, 1):
                rows.append([("R", str(e)), ("R", str(l)), ("R", str(u)), ("R", str(e & l & (1 - u)))])
    x.TABLE([1.6] * 4, rows, height=0.48, size=11, first_left=False)
    x.Q("d)", "Écris l'équation de M. Quelles portes de la partie A utilises-tu ?")
    x.ANS("$M=E\\cdot L\\cdot \\bar{U}$ : une porte ET à 3 entrées et un inverseur (NON) sur U. M = 1 sur une seule ligne : E = 1, L = 1, U = 0.", 2)
    x.BOX(["Si difficulté (N°1)",
           "Commence par la seule ligne où le moteur doit tourner : bouteille présente, zone libre, pas d'arrêt d'urgence. Sur toutes les autres lignes, M = 0."], only_corr=False)

    # ---- N°2
    x.HR(); x.EX(2, "Table de vérité, équation et chronogramme (≈ 10 min)", [("Présentation 120, diapositives 4 et 12", T120), ("Floyd 3-5 et 3-6 p. 131-138", fl(3, 131)), LZ("LZ_27")])
    x.Q("a)", "Une porte inconnue a la table de vérité ci-dessous. Nomme-la, écris son équation et sa règle.")
    rows = [["B", "A", "Y"]] + [[str(b_), str(a), str(y)] for b_, a, y in L.tdv("NON-OUX")]
    x.TABLE([1.6] * 3, rows, height=0.48, size=11, first_left=False)
    x.ANS("Porte NON-OU exclusif (XNOR) : $Y=\\bar{A\\oplus B}$. Y = 1 quand les deux entrées sont égales.", 2)
    x.Q("b)", "Pour l'équation $Y=\\bar{A+B}$, complète la table de vérité, puis le chronogramme.")
    rows = [["B", "A", "Y"]] + [[str(b_), str(a), ("R", str(y))] for b_, a, y in L.tdv("NON-OU")]
    x.TABLE([1.6] * 3, rows, height=0.48, size=11, first_left=False, keep_after=True)
    x.IMG("n2_corr.png" if corr else "n2_q.png", 13.0, after=4)

    # ---- N°3
    x.HR(); x.EX(3, "Reconnaître une porte à son chronogramme (≈ 8 min)", [("Présentation 120, diapositive 12", T120), ("Floyd 3-6 p. 135-138", fl(3, 135)), LZ("LZ_29")])
    x.CTX("au laboratoire, l'analyseur logique affiche les entrées A, B et la sortie Y de trois portes inconnues.")
    x.P("Pour chaque chronogramme, nomme la porte et justifie avec un ou plusieurs intervalles.", keep=True, after=2)
    for i, (k, A, B) in enumerate(MYST, 1):
        Y = L.chrono(k, A, B)
        x.P(f"**Chronogramme {i}**", keep=True, after=1, size=10.5)
        x.IMG(f"myst_{i}.png", 12.0, keep=True, after=1)
        iv = lambda cond: [str(t + 1) for t in range(8) if cond(A[t], B[t], Y[t])]
        if k == "NON-OU":
            just = f"Porte NON-OU : Y = 1 seulement quand A = 0 et B = 0 (intervalles {', '.join(iv(lambda a, b, y: y == 1))})."
        elif k == "OUX":
            just = (f"Porte OU exclusif : Y = 1 quand A ≠ B (intervalles {', '.join(iv(lambda a, b, y: y == 1))}). "
                    f"Dans les intervalles {' et '.join(iv(lambda a, b, y: a == 1 and b == 1))}, A = B = 1 et Y = 0 : ce n'est donc pas un OU.")
        else:
            just = f"Porte NON-ET : Y = 0 seulement quand A = 1 et B = 1 (intervalles {', '.join(iv(lambda a, b, y: y == 0))}) ; partout ailleurs Y = 1."
        x.ANS(just, 2)

    # ---- N°4
    x.HR(); x.EX(4, "Choisir le CI et numéroter les broches (≈ 8 min)", [("Présentation 120, diapositive 13", T120), ("Floyd 3-8 p. 146-149", fl(3, 146)), LZ("LZ_2223")])
    x.CTX("tu câbles sur breadboard la commande de la vanne V = B · N et le voyant « cuve vide ». Le magasin a des 74HC08 et des 74HC04.")
    t = x.d.add_table(rows=1, cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for j, ref in enumerate(("74HC08", "74HC04")):
        c = t.cell(0, j); c.width = Cm(TW / 2)
        x.IMG(f"dip_{ref}.png", 5.2, parent=c, after=0)
        cp = c.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rich(cp, f"{ref} : {'4 portes ET à 2 entrées' if ref.endswith('08') else '6 inverseurs'} (vue de dessus)", italic=True, size=9, color=GREY)
    x.P("", after=2)
    x.Q("a)", "Quel CI utilises-tu pour la vanne V = B · N ? Indique les broches pour la porte 1 et pour l'alimentation.")
    x.ANS("74HC08 (porte ET). B → broche 1 (1A), N → broche 2 (1B), V → broche 3 (1Y). Alimentation : broche 14 = +5 V, broche 7 = GND.", 2)
    x.Q("b)", "Le voyant « cuve vide » s'allume quand N = 0. Quelle porte, quel CI, quelles broches ?")
    x.ANS("Un inverseur : $Y=\\bar{N}$. 74HC04, porte 1 : N → broche 1 (1A), voyant → broche 2 (1Y). Le voyant se branche par un transistor, ou directement si c'est une LED à faible courant.", 2)
    x.Q("c)", "Les portes 2, 3 et 4 du 74HC08 ne servent pas. Que fais-tu de leurs entrées ? Pourquoi ?")
    x.ANS("On les relie à GND (ou à $V_{CC}$). Une entrée CMOS en l'air prend une tension quelconque : la porte peut basculer au hasard et le CI chauffer (présentation 100, diapositive 11).", 2)

    # ---- N°5
    x.HR(); x.EX(5, "Quelle porte pour quelle situation ? (≈ 7 min)", [("Présentation 120, diapositives 5 à 12", T120), ("Floyd 3-1 à 3-6 p. 112-138", fl(3, 112))])
    x.P("Pour chaque situation, choisis la porte, écris l'équation et donne un CI de la série 74HC.", keep=True, after=2)
    rows = [["Situation", "Porte", "Équation", "CI"],
            ["Le voyant « défaut » s'allume si la pompe P ou le convoyeur C est en défaut.", ("R", "OU"), ("R", "$Y=P+C$"), ("R", "74HC32")],
            ["Poste de soudage de l'atelier : l'arc n'est autorisé que si l'écran de protection est fermé (E = 1) et la pièce serrée (S = 1).", ("R", "ET"), ("R", "$Y=E\\cdot S$"), ("R", "74HC08")],
            ["Le convoyeur n'est autorisé que si aucun des deux arrêts d'urgence U_{1}, U_{2} n'est actionné.", ("R", "NON-OU"), ("R", "$Y=\\bar{U_{1}+U_{2}}$"), ("R", "74HC02")],
            ["La lampe de l'escalier de la cave est commandée par deux interrupteurs en va-et-vient, H en haut et B en bas.", ("R", "OU exclusif"), ("R", "$Y=H\\oplus B$"), ("R", "74HC86")],
            ["Le signal « capteurs cohérents » vaut 1 quand les capteurs de niveau N_{1} et N_{2} donnent la même valeur.", ("R", "NON-OU exclusif"), ("R", "$Y=\\bar{N_{1}\\oplus N_{2}}$"), ("R", "74HC7266")]]
    x.TABLE([8.6, 2.9, 3.6, TW - 15.1 - 0.02], rows, height=0.9, size=9.5, bold_first=False)

    # ---- auto-évaluation (fiche seulement : la grille reste vide dans le corrigé)
    if not corr:
        auto_eval(x)
    x.finish()


def auto_eval(x):
    x.P("**Auto-évaluation**", keep=True, after=1, before=10, color=NAVY)
    x.P("Après la correction : ✓ je sais seul·e · ~ avec une aide · ✗ à revoir (reprends la diapositive indiquée).", keep=True, size=10)
    x.TABLE([TW / 5 - 0.01] * 5, [["Table de vérité (N°1, diapo 3)", "Équation ↔ table ↔ chronogramme (N°2, diapo 4)", "Reconnaître une porte (N°3, diapo 12)",
                                   "Choisir et câbler un CI (N°4, diapo 13)", "Choisir la porte (N°5)"], ["", "", "", "", ""]],
            height=0.75, size=9, first_left=False)


def produire(ctx):
    global S, CTX, T120, MYST, N2_A, N2_B
    S, CTX = ctx.S, ctx
    T120 = S.teams_url("120")
    F = S.module("figures"); MYST, N2_A, N2_B = F.MYST, F.N2_A, F.N2_B
    build(False, ctx.sortie_de("130"))
    build(True, ctx.sortie_de("130C"))
