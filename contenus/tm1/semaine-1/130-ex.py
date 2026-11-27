# -*- coding: utf-8 -*-
"""130 EX Portes logiques de base (+ corrigé 130 EX C) · TM1 – El DT 1 · semaine 1.
Partie A : fiche à compléter pour les 7 portes (symbole CEI, table de vérité, équation, règle, chronogramme, CI, exemple réel).
Partie B : exercices sur le démarrage d'une voiture électrique (exercice TM1-A1-S2 du fascicule TM1) (LZ_4242, LZ_27, LZ_29, LZ_2223).
V2 (11/27/2026) : la voiture remplace la ligne de remplissage ; sortie S (REGLES 3.4) ; entrées du fascicule (A = 0 ceinture bouclée,
B = 1 sur P, C = 0 frein enfoncé, D = 1 service), voyant actif à 1 : S = B · (D + /(A + C)).
Remplace l'ancienne fiche « Portes logiques de base » (C. Moser, 2020). Valeurs calculées par moteur/logique.py et figures.py."""
import re
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
    "NON": "Ceinture : le capteur donne A = 0 quand elle est bouclée. Un inverseur donne 1 pour « ceinture bouclée ».",
    "ET": "Démarrage : le sélecteur sur P (B = 1) et les autres conditions remplies, en même temps : le voyant s'allume (S = 1).",
    "OU": "Démarrage : le mode service (D = 1) ou la ceinture et le frein en ordre suffisent.",
    "NON-ET": "Voyant « portière ouverte » : chaque contact donne 1 quand sa portière est fermée ; le voyant s'allume dès qu'une portière est ouverte.",
    "NON-OU": "Ceinture bouclée (A = 0) et frein enfoncé (C = 0) : la NON-OU donne 1 seulement dans ce cas.",
    "OUX": "Éclairage d'escalier en va-et-vient : chaque interrupteur change l'état de la lampe. L'OU exclusif sert aussi à additionner deux bits (semaine 4).",
    "NON-OUX": "Deux capteurs redondants sur la pédale de frein : le signal « capteurs cohérents » vaut 1 quand les deux donnent la même valeur.",
}
SY = lambda t: re.sub(r"\bY\b", "S", t)          # données du moteur écrites avec Y (semaine 1 V1) → sortie S (REGLES 3.4)
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
    f.page_break_before = idx in (3, 5, 7)   # deux portes par page ; la partie A commence en page 2 (chronogrammes lisibles, REGLES 9.4)
    rich(p, f"A.{idx} Porte {nom} ({en})", bold=True, size=12, color=NAVY)
    q = x.P("", italic=True, size=9, color=GREY, keep=True, after=3)
    hyperlink(q, fl(3, g[13]), f"Floyd {g[12]} p. {g[13]}", size=9); rich(q, " · ", size=9, color=GREY)
    hyperlink(q, T120, f"Présentation 120, diapositive {SLIDE[key]}", size=9)
    # tableau : symbole | table de vérité | équation et règle
    tdv = L.tdv(key)
    ins = ["A"] if n == 1 else ["B", "A"]      # du poids fort au poids faible ; L.tdv() donne (B, A, sortie)
    cols = 1 + len(ins) + 1 + 1
    wsym, wv = 4.4, 1.15
    weq = TW - wsym - wv * (len(ins) + 1) - 0.02
    widths = [wsym] + [wv] * (len(ins) + 1) + [weq]
    nrows = 1 + len(tdv) + 2          # en-tête, table de vérité, chronogramme, CI et exemple (un seul tableau : il ne se coupe pas)
    t = x.d.add_table(rows=nrows, cols=cols); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    heads = ["Symbole CEI"] + ins + ["S", "Équation et règle"]
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
    x.IMG(f"gate_{key}_S.png", 3.5, parent=sym, after=0)
    eq.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = eq.paragraphs[0]; p.paragraph_format.space_after = Pt(4); p.paragraph_format.space_before = Pt(2)
    rich(p, "Équation : ", bold=True, size=10)
    if corr:
        x.EQ(p, SY(g[7]), "EE0000", 24)
    else:
        dots(p, weq - 0.4)
    p2 = eq.add_paragraph(); p2.paragraph_format.space_after = Pt(2)
    rich(p2, "Règle : ", bold=True, size=10)
    if corr:
        rich(p2, SY(g[8]), color=RED, size=10)
    else:
        dots(p2, weq - 0.4)
        p3 = eq.add_paragraph(); p3.paragraph_format.space_after = Pt(2); dots(p3, weq - 0.4)
    # chronogramme
    p = chr_.paragraphs[0]; p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(0)
    rich(p, "Chronogramme : ", bold=True, size=10); rich(p, "S en rouge." if corr else "dessine S.", size=10)
    x.IMG(f"chrono_{key}_S_{'corr' if corr else 'q'}.png", 9.6, parent=chr_, after=2)
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
    if idx + 1 not in (3, 5, 7):      # pas d'espaceur avant un saut de page (sinon page blanche)
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
           ["**Consignes :** partie A, pendant la présentation 120, complète pour chaque porte la colonne S, l'équation, la règle et le chronogramme (le CI et l'exemple réel sont donnés). Partie B, travail en binôme, 45 min. "
            "Écris toujours la règle ou l'intervalle qui justifie ta réponse.",
            "**Conventions :** 1 = niveau HAUT, 0 = niveau BAS ; le cahier des charges dit si une entrée est active à 1 ou à 0. Équations notées comme dans le Floyd : point = ET, plus = OU, "
            "barre au-dessus = NON, ⊕ = OU exclusif. Les entrées s'appellent A, B, C, D, la sortie S. "
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
    x.H1("Partie A : les sept portes de base", page_break=True)
    for i, k in enumerate(L.ORDER, 1):
        gate_block(x, k, i)

    # ================= PARTIE B
    x.H1("Partie B : exercices sur la voiture électrique", page_break=True)
    x.CTX("le démarrage d'une voiture électrique de la présentation 120 (diapositive 2), exercice TM1-A1-S2 du fascicule TM1. "
          "Attention : la ceinture (A) et la pédale de frein (C) sont actives à 0 ; le sélecteur (B), le mode service (D) et le voyant (S) sont actifs à 1.")
    x.IMG("fig_voiture.png", 12.0, after=4)

    # ---- N°1
    x.EX(1, "Du cahier des charges à la table de vérité (≈ 12 min)", [(f"Présentation 120, diapositives 2, 3 et 13", T120), ("Floyd 1-2 p. 5", fl(1, 5)), LZ("LZ_4242")])
    x.P("Cahier des charges : trois capteurs sont simulés par des entrées logiques. Le capteur de la ceinture de sécurité (A) fournit un 0 si la ceinture est bouclée. "
        "Le capteur du sélecteur de vitesse (B) fournit un 1 si le sélecteur est sur la position P. Le capteur de la pédale des freins (C) fournit un 0 si elle est enfoncée. "
        "Pour que la voiture puisse démarrer, il faut que la ceinture soit bouclée, que le sélecteur soit sur P et que la pédale des freins soit enfoncée. "
        "Une entrée D, active à 1, permet au service de démarrer la voiture sans les contraintes de la ceinture et de la pédale des freins ; "
        "le capteur du sélecteur reste actif pour des raisons de sécurité. Le voyant (LED) s'allume quand le démarrage est autorisé : S = 1.", keep=True, after=3)
    x.Q("a)", "Complète le tableau des entrées et des sorties.")
    x.TABLE([2.4, 4.4, TW - 6.8 - 0.02], [["Variable", "Entrée ou sortie ?", "Elle vaut 1 quand…"],
                                         ["A", ("R", "entrée (capteur)"), ("R", "la ceinture n'est pas bouclée (0 = bouclée)")],
                                         ["B", ("R", "entrée (capteur)"), ("R", "le sélecteur est sur la position P")],
                                         ["C", ("R", "entrée (capteur)"), ("R", "la pédale de frein est relâchée (0 = enfoncée)")],
                                         ["D", ("R", "entrée (service)"), ("R", "le mode service est actif")],
                                         ["S", ("R", "sortie (voyant)"), ("R", "le démarrage est autorisé : la LED s'allume")]], height=0.55, size=10)
    x.Q("b)", "Combien de lignes compte la table de vérité ? Pourquoi ?")
    x.ANS("4 entrées → $2^{4}=16$ lignes : toutes les combinaisons de D, C, B et A.", 1)
    x.Q("c)", "Dessine la table de vérité : colonnes D C B A (D poids fort, A poids faible), lignes dans l'ordre du comptage binaire (0000 à 1111), puis la sortie S.")
    rows = [["D", "C", "B", "A", "S"]]
    for v in range(16):
        d_, c_, b_, a_ = (v >> 3) & 1, (v >> 2) & 1, (v >> 1) & 1, v & 1
        rows.append([("R", str(d_)), ("R", str(c_)), ("R", str(b_)), ("R", str(a_)), ("R", str(b_ & (d_ | (1 - (a_ | c_)))))])
    x.TABLE([1.4] * 5, rows, height=0.42, size=10.5, first_left=False)
    x.Q("d)", "Écris l'équation de S. Quelles portes de la partie A utilises-tu ?")
    x.ANS("$S=B\\cdot (D+\\bar{A+C})$ : une porte NON-OU (1 seulement si A = 0 et C = 0), une porte OU avec D, puis une porte ET avec B. "
          "S = 1 sur cinq lignes (D C B A) : 0010, 1010, 1011, 1110 et 1111.", 2)
    x.BOX(["Si difficulté (N°1)",
           "Commence par les lignes où B = 0 : la voiture ne démarre jamais, S = 0. Avec B = 1, S = 1 si D = 1, ou si A = 0 et C = 0."], only_corr=False)

    # ---- N°2
    x.HR(); x.EX(2, "Table de vérité, équation et chronogramme (≈ 10 min)", [("Présentation 120, diapositives 4 et 12", T120), ("Floyd 3-5 et 3-6 p. 131-138", fl(3, 131)), LZ("LZ_27")])
    x.Q("a)", "Une porte inconnue a la table de vérité ci-dessous. Nomme-la, écris son équation et sa règle.")
    rows = [["B", "A", "S"]] + [[str(b_), str(a), str(y)] for b_, a, y in L.tdv("NON-OUX")]
    x.TABLE([1.6] * 3, rows, height=0.48, size=11, first_left=False)
    x.ANS("Porte NON-OU exclusif (XNOR) : $S=\\bar{A\\oplus B}$. S = 1 quand les deux entrées sont égales.", 2)
    x.Q("b)", "Pour l'équation $S=\\bar{A+B}$, complète la table de vérité, puis le chronogramme.")
    rows = [["B", "A", "S"]] + [[str(b_), str(a), ("R", str(y))] for b_, a, y in L.tdv("NON-OU")]
    x.TABLE([1.6] * 3, rows, height=0.48, size=11, first_left=False, keep_after=True)
    x.IMG("n2_corr.png" if corr else "n2_q.png", 13.0, after=4)

    # ---- N°3
    x.HR(); x.EX(3, "Reconnaître une porte à son chronogramme (≈ 8 min)", [("Présentation 120, diapositive 12", T120), ("Floyd 3-6 p. 135-138", fl(3, 135)), LZ("LZ_29")])
    x.CTX("au laboratoire, l'analyseur logique affiche les entrées A, B et la sortie S de trois portes inconnues.")
    x.P("Pour chaque chronogramme, nomme la porte et justifie avec un ou plusieurs intervalles.", keep=True, after=2)
    for i, (k, A, B) in enumerate(MYST, 1):
        Y = L.chrono(k, A, B)
        x.P(f"**Chronogramme {i}**", keep=True, after=1, size=10.5)
        x.IMG(f"myst_{i}.png", 12.0, keep=True, after=1)
        iv = lambda cond: [str(t + 1) for t in range(8) if cond(A[t], B[t], Y[t])]
        if k == "NON-OU":
            just = f"Porte NON-OU : S = 1 seulement quand A = 0 et B = 0 (intervalles {', '.join(iv(lambda a, b, y: y == 1))})."
        elif k == "OUX":
            just = (f"Porte OU exclusif : S = 1 quand A ≠ B (intervalles {', '.join(iv(lambda a, b, y: y == 1))}). "
                    f"Dans les intervalles {' et '.join(iv(lambda a, b, y: a == 1 and b == 1))}, A = B = 1 et S = 0 : ce n'est donc pas un OU.")
        else:
            just = f"Porte NON-ET : S = 0 seulement quand A = 1 et B = 1 (intervalles {', '.join(iv(lambda a, b, y: y == 0))}) ; partout ailleurs S = 1."
        x.ANS(just, 2)

    # ---- N°4
    x.HR(); x.EX(4, "Câbler le démarrage sur trois CI (≈ 8 min)", [("Présentation 120, diapositives 13 et 14", T120), ("Floyd 3-8 p. 146-149", fl(3, 146)), LZ("LZ_2223")])
    x.CTX("tu câbles sur breadboard la commande du démarrage : une porte NON-OU (A, C), une porte OU (avec D), une porte ET (avec B). "
          "Le magasin a des 74HC02, des 74HC32 et des 74HC08. La LED du voyant (2 mA, tension directe 2 V) est branchée entre la sortie S et GND, avec une résistance R en série.")
    t = x.d.add_table(rows=1, cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for j, (ref, txt) in enumerate((("74HC02", "4 portes NON-OU à 2 entrées"), ("74HC08", "4 portes ET ; le 74HC32 (OU) a le même brochage"))):
        c = t.cell(0, j); c.width = Cm(TW / 2)
        x.IMG(f"dip_{ref}.png", 6.0, parent=c, after=0)
        cp = c.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rich(cp, f"{ref} : {txt} (vue de dessus)", italic=True, size=9, color=GREY)
    x.P("", after=2)
    x.Q("a)", "Pour chaque porte, indique le CI et les broches (porte 1 de chaque CI), puis l'alimentation.")
    x.ANS("NON-OU : 74HC02, A → broche 2 (1A), C → broche 3 (1B), sortie 1Y → broche 1. "
          "OU : 74HC32, sortie du 74HC02 → broche 1 (1A), D → broche 2 (1B), sortie 1Y → broche 3. "
          "ET : 74HC08, sortie du 74HC32 → broche 1 (1A), B → broche 2 (1B), S → broche 3 (1Y).\n"
          "Alimentation des trois CI : broche 14 = +5 V, broche 7 = GND.", 3)
    x.Q("b)", "En quoi le brochage du 74HC02 diffère-t-il de celui du 74HC08 ? Quelle erreur faut-il éviter ?")
    x.ANS("Sur le 74HC02, la sortie de chaque porte vient avant ses entrées : 1Y = broche 1, 1A = broche 2, 1B = broche 3 (sorties sur 1, 4, 10 et 13). "
          "Sur le 74HC08 et le 74HC32, les sorties sont sur 3, 6, 8 et 11. Câbler le 74HC02 comme un 74HC08 relie deux sorties entre elles.", 2)
    x.Q("c)", "Calcule la résistance R de la LED (I_{F} = 2 mA, U_{F} = 2 V ; à l'état haut, la sortie vaut V_{OH} = 4,9 V), choisis la valeur de la série E12 et fais le contrôle.")
    x.ANS("$R=\\f{V_{OH}-U_{F}}{I_{F}}=\\f{4,9\\u{ [V]}-2\\u{ [V]}}{2\\u{ [mA]}}=1,45\\u{ [kΩ]}$ → valeur E12 juste au-dessus : 1,5 kΩ.\n"
          "Contrôle : $I=\\f{2,9\\u{ [V]}}{1,5\\u{ [kΩ]}}=1,933\\u{ [mA]}$, pas plus de 2 mA.", 3)
    x.Q("d)", "Que fais-tu des entrées des portes inutilisées ? Pourquoi ?")
    x.ANS("On les relie à GND (ou à $V_{CC}$). Une entrée CMOS en l'air prend une tension quelconque : la porte peut basculer au hasard et le CI chauffer (présentation 100, diapositive 11).", 2)

    # ---- N°5
    x.HR(); x.EX(5, "Quelle porte pour quelle situation ? (≈ 7 min)", [("Présentation 120, diapositives 5 à 12", T120), ("Floyd 3-1 à 3-6 p. 112-138", fl(3, 112))])
    x.P("Pour chaque situation, choisis la porte, écris l'équation et donne un CI de la série 74HC.", keep=True, after=2)
    rows = [["Situation", "Porte", "Équation", "CI"],
            ["Le plafonnier s'allume si la portière A ou la portière B est ouverte (1 = ouverte).", ("R", "OU"), ("R", "$S=A+B$"), ("R", "74HC32")],
            ["Poste de soudage de l'atelier : l'arc n'est autorisé que si l'écran de protection est fermé (A = 1) et la pièce serrée (B = 1).", ("R", "ET"), ("R", "$S=A\\cdot B$"), ("R", "74HC08")],
            ["Verrouillage automatique : il se fait seulement si aucune des deux portières A, B n'est ouverte (1 = ouverte).", ("R", "NON-OU"), ("R", "$S=\\bar{A+B}$"), ("R", "74HC02")],
            ["La lampe de l'escalier de la cave est commandée par deux interrupteurs en va-et-vient, A en haut et B en bas.", ("R", "OU exclusif"), ("R", "$S=A\\oplus B$"), ("R", "74HC86")],
            ["Le signal « capteurs cohérents » vaut 1 quand les deux capteurs A et B de la pédale de frein donnent la même valeur.", ("R", "NON-OU exclusif"), ("R", "$S=\\bar{A\\oplus B}$"), ("R", "74HC7266")]]
    x.TABLE([8.6, 2.9, 3.6, TW - 15.1 - 0.02], rows, height=0.9, size=9.5, bold_first=False)

    # ---- auto-évaluation (fiche seulement : la grille reste vide dans le corrigé)
    if not corr:
        auto_eval(x)
    x.finish()


def auto_eval(x):
    x.P("**Auto-évaluation**", keep=True, after=1, before=10, color=NAVY)
    x.P("Après la correction : ✓ je sais seul·e · ~ avec une aide · ✗ à revoir (reprends la diapositive indiquée).", keep=True, size=10)
    x.TABLE([TW / 5 - 0.01] * 5, [["Table de vérité (N°1, diapo 3)", "Équation ↔ table ↔ chronogramme (N°2, diapo 4)", "Reconnaître une porte (N°3, diapo 12)",
                                   "Câbler le démarrage (N°4, diapos 13 et 14)", "Choisir la porte (N°5)"], ["", "", "", "", ""]],
            height=0.75, size=9, first_left=False)


def produire(ctx):
    global S, CTX, T120, MYST, N2_A, N2_B
    S, CTX = ctx.S, ctx
    T120 = S.teams_url("120")
    F = S.module("figures"); MYST, N2_A, N2_B = F.MYST, F.N2_A, F.N2_B
    build(False, ctx.sortie_de("130"))
    build(True, ctx.sortie_de("130C"))
