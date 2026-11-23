# -*- coding: utf-8 -*-
"""Systèmes de numération — fiche-mémo + exercices en groupe (élève + corrigé).
# Prérequis : etml_base.docx = Rapport_Simple.dotx dont [Content_Types].xml a template.main+xml remplacé par document.main+xml
Charte ETML « Rapport_Simple » reconstituée d'après les préférences de Gael (noir et blanc)."""
import re, os
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_TAB_ALIGNMENT, WD_ALIGN_PARAGRAPH, WD_TAB_LEADER, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
RED = RGBColor(0xEE, 0x00, 0x00)
TWcm = 21.0 - 2.0 - 1.5          # largeur utile
TW = TWcm / 2.54                  # en pouces
DOC_TITLE = "Systèmes de numération"
SUBTITLE = "Fiche-mémo et exercices en groupe – binaire, BCD, hexadécimal"


def build(corr, out):
    d = Document(os.path.join(HERE, "etml_base.docx"))   # modèle ETML Rapport_Simple (.dotx -> .docx)
    body = d.element.body
    for el in list(body):
        if el.tag != qn("w:sectPr"): body.remove(el)
    cp = d.core_properties
    cp.title = f"{DOC_TITLE} - {'Corrigé' if corr else 'Exercices'}"
    cp.author = "Gael"; cp.last_modified_by = "Gael"
    import datetime as _dt; now = _dt.datetime.now(); cp.created = now; cp.modified = now; cp.last_printed = now; cp.revision = 1
    s = d.sections[0]
    # en-tête du modèle : remplace « Nom - Type - Numéro » par le titre du document
    for t in s.header._element.iter(qn("w:t")):
        if t.text == "Nom -": t.text = cp.title
        elif t.text in (" ", "Type - Numéro"): t.text = ""
    # met à jour les valeurs affichées des champs du pied de page (auteur, dates, fichier)
    vals = {"AUTHOR": "Gael", "LASTSAVEDBY": "Gael", "SAVEDATE": now.strftime("%d/%m/%Y %H:%M"),
            "CREATEDATE": now.strftime("%d/%m/%Y"), "PRINTDATE": now.strftime("%d/%m/%Y %H:%M"),
            "FILENAME": os.path.basename(out)}
    for part in (s.footer._element, s.header._element):
        runs = list(part.iter(qn("w:r"))); cur = None; state = None
        for r in runs:
            fc = r.find(qn("w:fldChar")); it = r.find(qn("w:instrText")); t = r.find(qn("w:t"))
            if fc is not None:
                ty = fc.get(qn("w:fldCharType"))
                if ty == "begin": cur, state = None, "instr"
                elif ty == "separate": state = "res"
                elif ty == "end": cur, state = None, None
            elif it is not None and state == "instr":
                k = it.text.strip().split(" ")[0]
                if k in vals: cur = k
            elif t is not None and state == "res" and cur:
                t.text = vals[cur]; cur = "_done"; vals.setdefault("_done", "")
            elif t is not None and state == "res" and cur == "_done":
                t.text = ""
    for name in ("Title", "Heading 1", "Heading 2"):
        d.styles[name].paragraph_format.keep_with_next = True

    # ---------- briques XML ----------
    def border(pPr_owner, side, sz=4):
        pPr = pPr_owner.get_or_add_pPr()
        b = pPr.find(qn("w:pBdr"))
        if b is None: b = OxmlElement("w:pBdr"); pPr.append(b)
        for sd in ([side] if isinstance(side, str) else side):
            e = OxmlElement(f"w:{sd}")
            for k, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", "4"), ("w:color", "000000")): e.set(qn(k), v)
            b.append(e)

    def field(p, code, cached, size=None, bold=False, italic=False, font=None):
        def r_(child):
            r = OxmlElement("w:r"); rp = OxmlElement("w:rPr")
            if font:
                rf = OxmlElement("w:rFonts"); rf.set(qn("w:ascii"), font); rf.set(qn("w:hAnsi"), font); rp.append(rf)
            if bold: rp.append(OxmlElement("w:b"))
            if italic: rp.append(OxmlElement("w:i"))
            if size: sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(size * 2))); rp.append(sz)
            r.append(rp); r.append(child); p._p.append(r)
        fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin"); r_(fc)
        it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = f" {code} "; r_(it)
        fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "separate"); r_(fc)
        t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = cached; r_(t)
        fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "end"); r_(fc)

    def no_borders(tbl):
        tblPr = tbl._tbl.tblPr; bd = OxmlElement("w:tblBorders")
        for sd in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{sd}"); e.set(qn("w:val"), "nil"); bd.append(e)
        tblPr.append(bd)

    SUB = re.compile(r"_\{([^}]*)\}|\^\{([^}]*)\}|\*\*([^*]*)\*\*")

    def rich(p, txt, color=None, bold=False, italic=False, size=None, font=None):
        pos = 0
        def add(t, sub=False, sup=False, b=False):
            r = p.add_run(t); r.bold = bold or b; r.italic = italic
            if color: r.font.color.rgb = color
            if size: r.font.size = Pt(size)
            if font: r.font.name = font
            if sub: r.font.subscript = True
            if sup: r.font.superscript = True
        for m in SUB.finditer(txt):
            if m.start() > pos: add(txt[pos:m.start()])
            if m.group(1) is not None: add(m.group(1), sub=True)
            elif m.group(2) is not None: add(m.group(2), sup=True)
            else: add(m.group(3), b=True)
            pos = m.end()
        if pos < len(txt): add(txt[pos:])
        return p

    def P(txt="", after=2, before=0, align=None, keep=False, **kw):
        p = d.add_paragraph(); f = p.paragraph_format
        f.space_after = Pt(after); f.space_before = Pt(before); f.keep_with_next = keep
        if align: p.alignment = align
        rich(p, txt, **kw); return p

    def H(level, txt):
        return d.add_heading(txt, level=level)

    def STEP(lbl, txt, keep=False):
        """Étape de méthode : « 1. texte » avec retrait suspendu."""
        p = d.add_paragraph(); f = p.paragraph_format
        f.left_indent = Cm(1.0); f.first_line_indent = Cm(-0.6); f.space_after = Pt(0); f.keep_with_next = keep
        f.tab_stops.add_tab_stop(Cm(1.0))
        r = p.add_run(lbl + "\t"); r.bold = True
        rich(p, txt); return p

    def EXAMPLE(txt):
        p = d.add_paragraph(); f = p.paragraph_format
        f.left_indent = Cm(1.0); f.space_after = Pt(6); f.line_spacing = 1.15
        r = p.add_run("Exemple : "); r.italic = True; r.bold = True
        rich(p, txt, italic=True); return p

    def Q(lbl, txt):
        p = d.add_paragraph(); f = p.paragraph_format
        f.left_indent = Cm(0.7); f.first_line_indent = Cm(-0.7); f.space_before = Pt(4); f.space_after = Pt(2)
        f.tab_stops.add_tab_stop(Cm(0.7)); f.keep_with_next = True
        r = p.add_run(lbl + "\t"); r.bold = True
        rich(p, txt); return p

    def ANS(txt, lines=1):
        if corr:
            p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7); p.paragraph_format.space_after = Pt(4)
            rich(p, txt, color=RED)
        else:
            for _ in range(lines):
                p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7); p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.tab_stops.add_tab_stop(Inches(TW), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.LINES)
                p.add_run("\t")

    def BOX(lines, only_corr=True, title_bold=True):
        """Encadré (filet fin noir) — par défaut uniquement dans le corrigé (2e son de cloche)."""
        if only_corr and not corr: return
        for i, t in enumerate(lines):
            p = d.add_paragraph(); f = p.paragraph_format
            f.left_indent = Cm(0.3); f.right_indent = Cm(0.3); f.line_spacing = 1.15
            f.space_before = Pt(6 if i == 0 else 0); f.space_after = Pt(6 if i == len(lines) - 1 else 0)
            f.keep_with_next = i < len(lines) - 1; f.keep_together = True
            border(p._p, ["top", "left", "bottom", "right"], 4)
            rich(p, t, bold=(i == 0 and title_bold), italic=(i > 0), size=10)

    def HR():
        p = d.add_paragraph(); p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.0; border(p._p, "bottom", 4)

    def EX(n, title):
        p = d.add_paragraph(); f = p.paragraph_format
        f.space_before = Pt(6); f.space_after = Pt(2); f.keep_with_next = True; f.line_spacing = 1.0
        r = p.add_run(f"N°{n} {title}"); r.bold = True; r.font.size = Pt(12)

    def cell_txt(c, txt, bold=False, italic=False, color=None, size=10, align="center"):
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]; f = p.paragraph_format
        f.space_after = Pt(0); f.line_spacing = 1.0
        p.alignment = {"center": WD_ALIGN_PARAGRAPH.CENTER, "left": WD_ALIGN_PARAGRAPH.LEFT}[align]
        rich(p, txt, color=color, bold=bold, italic=italic, size=size)

    def TABLE(widths, rows, header=True, height=0.32, size=10, first_col_left=False):
        """('R', txt) = réponse : rouge dans le corrigé, vide pour l'élève. En-têtes en italique (charte)."""
        t = d.add_table(rows=len(rows), cols=len(widths)); t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
        for i, row in enumerate(rows):
            tr = t.rows[i]; tr.height = Inches(height)
            for j, v in enumerate(row):
                c = tr.cells[j]; c.width = Inches(widths[j])
                hdr = header and i == 0
                al = "left" if (first_col_left and j == 0) else "center"
                if isinstance(v, tuple):
                    cell_txt(c, v[1] if corr else "", color=RED if corr else None, bold=True, size=size, align=al)
                else:
                    cell_txt(c, v, italic=hdr, bold=(first_col_left and j == 0 and not hdr), size=size, align=al)
        for j, w in enumerate(widths): t.columns[j].width = Inches(w)
        for i, tr in enumerate(t.rows):
            tr._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
            if i < len(t.rows) - 1:
                for c in tr.cells:
                    for pp in c.paragraphs: pp.paragraph_format.keep_with_next = True
        sp = d.add_paragraph(); sp.paragraph_format.space_after = Pt(2); sp.paragraph_format.line_spacing = 1.0
        return t

    W8 = [128, 64, 32, 16, 8, 4, 2, 1]

    def BYTE(rows, label_w=1.6):
        widths = [label_w] + [0.5] * 8 + [TW - label_w - 4.0 - 0.05]
        body = [["Poids"] + [str(w) for w in W8] + ["Décimal"]]
        for lab, bits, val in rows:
            body.append([lab] + [("R", b) for b in bits] + [("R", val + "d")])
        TABLE(widths, body, first_col_left=True, height=0.32)

    # ================= TITRE =================
    d.add_paragraph(DOC_TITLE, style="Title")
    P(SUBTITLE, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, after=6)
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.paragraph_format.space_after = Pt(0)
    r = p.add_run("Corrigé" if corr else "Version élève"); r.bold = True
    if corr: r.font.color.rgb = RED
    p.add_run("\tNom :")
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.add_run("\tDate :")
    border(p._p, "bottom", 4)

    if corr:
        BOX(["Plan de séance (enseignant·e) – 40 à 50 min",
             "Fiche-mémo (chap. 1) : 5–10 min, lue ensemble, sans nouvelle théorie : c'est le rappel des méthodes déjà vues. N°1 : 15 min · N°2 : 8 min · N°3 : 6 min · N°4 : 5 min · N°5 : 8 min · Option : 5 min.",
             "Les réponses des N°1, N°2 a) et N°4 (deux dernières lignes) dépendent des élèves : le corrigé montre un exemple complet à reproduire au tableau si un groupe bloque."])

    # ================= 1 FICHE-MÉMO =================
    H(1, "Fiche-mémo")
    H(2, "Trois systèmes de numération et un code")
    TABLE([1.45, 0.75, 1.55, 1.55, 1.48], [
        ["", "Base", "Chiffres utilisés", "Exemple : 89", "Suffixe"],
        ["Décimal", "10", "0 à 9", "89d", "d"],
        ["Binaire", "2", "0 et 1", "0101 1001b", "b"],
        ["Hexadécimal", "16", "0 à 9, A à F", "59h", "h"],
        ["BCD", "—", "4 bits par chiffre", "1000 1001 BCD", "BCD"],
    ], first_col_left=True, height=0.3)
    P("**Convention du cours :** on écrit toujours le système à la fin du nombre : **b** pour binaire, **d** pour décimal, **h** pour hexadécimal, **BCD** pour le BCD. Exemple : 89d = 0101 1001b = 59h = 1000 1001 BCD.", after=2)
    P("Le BCD n'est pas une base : c'est un **code** qui écrit chaque chiffre décimal séparément en binaire.", after=4)

    H(2, "Le code BCD (Binary Coded Decimal)")
    P("**Principe :** on prend le nombre décimal chiffre par chiffre, et on code chaque chiffre sur 4 bits (un quartet), avec les poids **8 – 4 – 2 – 1**. On parle aussi de code « 8421 ».")
    P("**Combinaisons interdites :** avec 4 bits on a 16 combinaisons, mais seules 0000 à 1001 (0d à 9d) sont utilisées. Les 6 combinaisons **1010 à 1111** n'existent pas en BCD : si on en trouve une, il y a une erreur.")
    P("**Où le trouve-t-on ?** Partout où un nombre doit être affiché en décimal : afficheurs 7 segments, horloges, compteurs, multimètres, calculatrices. Chaque afficheur reçoit son propre quartet.")
    P("**Avantage :** très facile à afficher et à lire. **Inconvénient :** il faut plus de bits qu'en binaire et les calculs sont plus compliqués.", after=4)
    P("Comparaison des codes de 0 à 15 – à partir de 10, le binaire et le BCD ne s'écrivent plus pareil :", keep=True, after=2)
    hx = [format(i, "X") for i in range(16)]
    TABLE([0.95] + [0.369] * 16, [
        ["Décimal (d)"] + [str(i) for i in range(16)],
        ["Binaire (b)"] + [format(i, "04b") for i in range(16)],
        ["BCD"] + [format(i, "04b") for i in range(10)] + ["0001 " + format(i - 10, "04b") for i in range(10, 16)],
        ["Hexa (h)"] + hx,
    ], header=False, first_col_left=True, height=0.3, size=7)
    P("Exemple : 2026d → 0010 0000 0010 0110 BCD (16 bits) ; en binaire : 111 1110 1010b (11 bits).", italic=True, after=4)

    H(2, "Les passages de conversion")
    d.add_picture(os.path.join(HERE, "map.png"), width=Cm(13))
    d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    P("Toutes les méthodes ci-dessous utilisent le même nombre : **89d**.", after=4)

    P("**A. Binaire → décimal**", keep=True, after=0)
    STEP("1.", "Écrire les poids (128, 64, 32, 16, 8, 4, 2, 1) au-dessus des bits.", True)
    STEP("2.", "Additionner uniquement les poids qui sont au-dessus d'un « 1 ».", True)
    EXAMPLE("0101 1001b → 64 + 16 + 8 + 1 = 89d")

    P("**B. Décimal → binaire**", keep=True, after=0)
    STEP("1.", "Méthode des poids : prendre le plus grand poids ≤ au nombre → 1, soustraire, continuer avec le reste ; un poids trop grand → 0.", True)
    STEP("2.", "Ou méthode des divisions : diviser par 2 jusqu'à 0 et lire les restes **de bas en haut**.", True)
    EXAMPLE("89d − 64 = 25 ; 25 − 16 = 9 ; 9 − 8 = 1 ; 1 − 1 = 0 → 0101 1001b (poids 64, 16, 8, 1)")

    P("**C. Nombre de bits minimum**", keep=True, after=0)
    STEP("1.", "Chercher la première puissance de 2 **strictement plus grande** que le nombre : 2^{n} > N → n bits.", True)
    EXAMPLE("64 ≤ 89d < 128 = 2^{7} → 7 bits. Attention : 128d demande déjà 8 bits.")

    P("**D. Décimal → BCD**", keep=True, after=0)
    STEP("1.", "Séparer les chiffres décimaux.", True)
    STEP("2.", "Coder chaque chiffre sur 4 bits (même le 0 : 0000).", True)
    EXAMPLE("89d → 8 = 1000 et 9 = 1001 → 1000 1001 BCD")

    P("**E. BCD → décimal**", keep=True, after=0)
    STEP("1.", "Couper en quartets **en partant de la droite**.", True)
    STEP("2.", "Vérifier que chaque quartet est ≤ 1001, sinon le code est faux.", True)
    STEP("3.", "Traduire chaque quartet en un chiffre.", True)
    EXAMPLE("0001 0100 0111 BCD → 1 | 4 | 7 → 147d")

    P("**F. Binaire → BCD** et **G. BCD → binaire : toujours passer par le décimal**", keep=True, after=0)
    STEP("F.", "Binaire → décimal (A), puis décimal → BCD (D).", True)
    STEP("G.", "BCD → décimal (E), puis décimal → binaire (B).", True)
    EXAMPLE("0101 1001b → 89d → 1000 1001 BCD. Piège : recopier les bits ne fonctionne pas (0101 1001 lu en BCD donnerait 59d).")

    P("**H. Décimal → hexadécimal (via le binaire)**", keep=True, after=0)
    STEP("1.", "Convertir en binaire sur 8 bits (B).", True)
    STEP("2.", "Couper en 2 quartets : quartet fort (gauche) et quartet faible (droite).", True)
    STEP("3.", "Chaque quartet donne un chiffre hexa (tableau 1.2).", True)
    EXAMPLE("89d → 0101 1001b → 0101b = 5h et 1001b = 9h → 59h")

    P("**I. Hexadécimal → décimal (contrôle)** et **J. Hexadécimal ↔ binaire**", keep=True, after=0)
    STEP("I.", "Chiffre fort × 16 + chiffre faible.", True)
    STEP("J.", "Chaque chiffre hexa = exactement 4 bits, dans les deux sens.", True)
    EXAMPLE("59h → 5 × 16 + 9 = 89d ; C8h → 1100 1000b ; 7EAh → 0111 1110 1010b")

    H(2, "Poids des bits")
    TABLE([1.3] + [(TW - 1.3) / 10] * 10, [
        ["Puissance", "2^{9}", "2^{8}", "2^{7}", "2^{6}", "2^{5}", "2^{4}", "2^{3}", "2^{2}", "2^{1}", "2^{0}"],
        ["Poids", "512", "256", "128", "64", "32", "16", "8", "4", "2", "1"]], first_col_left=True, height=0.28)

    # ================= 2 EXERCICES =================
    pb = d.add_paragraph(); pb.add_run().add_break(__import__("docx").enum.text.WD_BREAK.PAGE)
    H(1, "Exercices en groupe")
    P("Travail par groupes de 2. Pas de calculatrice : on écrit le raisonnement. Chaque exercice se termine par un contrôle croisé avec ton/ta camarade. Les lettres A à J renvoient aux méthodes du chapitre 1.3.", italic=True, after=4)

    # ---- N°1
    EX(1, "La date de naissance de ton papa")
    P("Écris la date de naissance de ton papa au format JJ.MM.AA (année sur 2 chiffres). Si tu préfères, choisis la date d'une autre personne.")
    if corr: P("Exemple utilisé dans le corrigé : papa né le 23.07.1975 → 23.07.75", color=RED, bold=True)
    Q("a)", "Nombre de bits minimum (méthode C).")
    TABLE([2.55, 1.43, 1.43, 1.43], [
        ["", "Jour (JJ)", "Mois (MM)", "Année (AA)"],
        ["Ta valeur en décimal", ("R", "23d"), ("R", "07d"), ("R", "75d")],
        ["Nb de bits minimum pour TA valeur", ("R", "5 bits (16 ≤ 23d < 32)"), ("R", "3 bits (4 ≤ 7d < 8)"), ("R", "7 bits (64 ≤ 75d < 128)")],
        ["Plus grande valeur possible", ("R", "31d"), ("R", "12d"), ("R", "99d")],
        ["Nb de bits pour TOUTES les valeurs possibles", ("R", "5 bits"), ("R", "4 bits"), ("R", "7 bits")],
    ], first_col_left=True, height=0.38)
    Q("b)", "Convertis chaque valeur en binaire sur 8 bits (1 byte) – méthode B.")
    BYTE([("Jour", "00010111", "23"), ("Mois", "00000111", "7"), ("Année", "01001011", "75")])
    BOX(["Si difficulté – 2e son de cloche",
         "Méthode « porte-monnaie » : on paie 23d avec des pièces de 128, 64, 32, 16, 8, 4, 2, 1, chaque pièce au maximum une fois, de la plus grosse à la plus petite. 23 : pas de 32 → 0 ; 16 oui (reste 7) ; 8 non ; 4 oui (reste 3) ; 2 oui (reste 1) ; 1 oui → 0001 0111b.",
         "Divisions par 2 : 23/2 = 11 r 1 ; 11/2 = 5 r 1 ; 5/2 = 2 r 1 ; 2/2 = 1 r 0 ; 1/2 = 0 r 1 → on lit de bas en haut : 10111b.",
         "Nombre de bits : 31d < 32 = 2^{5} → 5 bits. Piège classique : 32d demande déjà 6 bits !"])
    Q("c)", "Échange : recopie tes 3 bytes sur un papier, sans le décimal, et donne-le à ton/ta camarade. Décode la date de naissance du papa de ton/ta camarade (méthode A).")
    BYTE([("Jour", "00001100", "12"), ("Mois", "00000101", "5"), ("Année", "01010010", "82")])
    Q("d)", "Rends le papier : ton/ta camarade confirme-t-il/elle la date ? Si non, cherchez ensemble l'erreur (codage ou décodage ?).")
    if corr: ANS("Exemple : 0000 1100b = 8 + 4 = 12d ; 0000 0101b = 4 + 1 = 5d ; 0101 0010b = 64 + 16 + 2 = 82d → 12.05.82")
    BOX(["Si difficulté – décoder un byte",
         "On n'additionne que les poids situés sous un « 1 ». Faire écrire les poids au-dessus des bits AVANT de commencer : la plupart des erreurs viennent d'un bit décalé d'une colonne."])

    # ---- N°2
    HR(); EX(2, "L'heure actuelle en BCD")
    Q("a)", "Relève l'heure actuelle (HH:MM) et code-la en BCD (méthode D).")
    if corr: P("Exemple : 08:35", color=RED, bold=True)
    TABLE([1.85, 1.22, 1.22, 1.22, 1.22], [
        ["", "Dizaines d'heures", "Unités d'heures", "Dizaines de minutes", "Unités de minutes"],
        ["Chiffre décimal", ("R", "0"), ("R", "8"), ("R", "3"), ("R", "5")],
        ["Code BCD (4 bits)", ("R", "0000"), ("R", "1000"), ("R", "0011"), ("R", "0101")],
    ], first_col_left=True, height=0.38)
    Q("b)", "Inversement : quelle heure est affichée (méthode E) ?")
    TABLE([3.4, 1.8], [
        ["Code BCD", "Heure (HH:MM)"],
        ["0001 0100 : 0101 1001", ("R", "14:59")],
        ["0010 0011 : 0000 0111", ("R", "23:07")],
        ["0000 1001 : 0100 0101", ("R", "09:45")],
        ["0001 0101 : 0011 1100", ("R", "impossible !")],
    ], height=0.3)
    Q("c)", "Que remarques-tu pour la dernière ligne ?")
    ANS("Le dernier quartet 1100b vaut 12d : il n'existe pas en BCD (seuls 0000 à 1001, soit 0d à 9d, sont autorisés). Les combinaisons 1010 à 1111 sont interdites.", 2)
    Q("d)", "Code l'année 2026d en BCD puis en binaire. Lequel utilise le moins de bits ?")
    ANS("BCD : 0010 0000 0010 0110 BCD (16 bits). Binaire : 2026d = 1024 + 512 + 256 + 128 + 64 + 32 + 8 + 2 = 111 1110 1010b (11 bits). Le binaire est plus compact.", 2)
    Q("e)", "Bonus : combien de bits faut-il au minimum pour afficher HH:MM en BCD si on ne garde que les bits utiles de chaque chiffre ?")
    ANS("Dizaines d'heures 0 à 2 → 2 bits ; unités 0 à 9 → 4 bits ; dizaines de minutes 0 à 5 → 3 bits ; unités → 4 bits. Total : 2 + 4 + 3 + 4 = 13 bits (au lieu de 16).", 2)
    BOX(["Si difficulté – 2e son de cloche",
         "Le BCD, c'est comme l'afficheur d'un réveil : chaque chiffre a son propre afficheur 7 segments, donc son propre paquet de 4 bits. On ne convertit jamais le nombre entier (35), mais le 3 puis le 5."])

    # ---- N°3
    HR(); EX(3, "Du binaire au BCD et retour (via le décimal)")
    Q("a)", "Binaire → BCD (méthode F).")
    TABLE([1.6, 1.0, 2.3, 1.3], [
        ["Binaire", "Décimal", "BCD", "Nb de bits BCD"],
        ["0010 1101b", ("R", "45d"), ("R", "0100 0101 BCD"), ("R", "8")],
        ["0101 1000b", ("R", "88d"), ("R", "1000 1000 BCD"), ("R", "8")],
        ["1001 0011b", ("R", "147d"), ("R", "0001 0100 0111 BCD"), ("R", "12")],
        ["1111 1111b", ("R", "255d"), ("R", "0010 0101 0101 BCD"), ("R", "12")],
    ], height=0.3)
    Q("b)", "BCD → binaire (méthode G).")
    TABLE([2.3, 1.0, 1.6, 1.3], [
        ["BCD", "Décimal", "Binaire (8 bits)", "Hexa"],
        ["0110 0100 BCD", ("R", "64d"), ("R", "0100 0000b"), ("R", "40h")],
        ["1001 1001 BCD", ("R", "99d"), ("R", "0110 0011b"), ("R", "63h")],
        ["0010 0101 0101 BCD", ("R", "255d"), ("R", "1111 1111b"), ("R", "FFh")],
    ], height=0.3)
    Q("c)", "Pourquoi 1001 0011b ne s'écrit-il pas 1001 0011 BCD ?")
    ANS("En BCD, 1001 0011 se lirait « 9 » et « 3 », donc 93d. Or 1001 0011b vaut 128 + 16 + 2 + 1 = 147d → 0001 0100 0111 BCD.", 2)
    BOX(["Si difficulté",
         "Faire passer systématiquement par la colonne « décimal » : c'est le pont entre les deux codes. Le BCD demande plus de bits que le binaire pour le même nombre (12 bits au lieu de 8 pour 147d)."])

    # ---- N°4
    HR(); EX(4, "Du décimal à l'hexadécimal (via le binaire)")
    P("Méthode H, puis contrôle avec la méthode I.", keep=True)
    TABLE([1.0, 1.45, 1.0, 1.0, 0.75, TW - 5.2 - 0.05], [
        ["Décimal", "Binaire (8 bits)", "Quartet fort", "Quartet faible", "Hexa", "Contrôle"],
        ["200d", ("R", "1100 1000b"), ("R", "1100b = Ch"), ("R", "1000b = 8h"), ("R", "C8h"), ("R", "12·16 + 8 = 200d")],
        ["77d", ("R", "0100 1101b"), ("R", "0100b = 4h"), ("R", "1101b = Dh"), ("R", "4Dh"), ("R", "4·16 + 13 = 77d")],
        ["171d", ("R", "1010 1011b"), ("R", "1010b = Ah"), ("R", "1011b = Bh"), ("R", "ABh"), ("R", "10·16 + 11 = 171d")],
        ["9d", ("R", "0000 1001b"), ("R", "0000b = 0h"), ("R", "1001b = 9h"), ("R", "09h"), ("R", "0·16 + 9 = 9d")],
        [("R", "ex. 142d"), ("R", "1000 1110b"), ("R", "1000b = 8h"), ("R", "1110b = Eh"), ("R", "8Eh"), ("R", "8·16 + 14 = 142d")],
        [("R", ""), ("R", ""), ("R", ""), ("R", ""), ("R", ""), ("R", "")],
    ], height=0.32)
    P("Les deux dernières lignes : ton/ta camarade choisit au hasard un nombre entre 0d et 255d, puis vous inversez les rôles.", italic=True, size=10)
    BOX(["Si difficulté",
         "Un chiffre hexa = exactement 4 bits : c'est pour ça qu'on passe par le binaire, la conversion devient une simple lecture du tableau. Contrôle : chiffre fort × 16 + chiffre faible."])

    # ---- N°5
    HR(); EX(5, "Le compteur 10 bits qui déborde")
    P("Un compteur binaire 10 bits affiche au départ la valeur 854d. On lui applique 300d impulsions d'horloge (CLK) ; il compte +1 à chaque impulsion.", keep=True)
    d.add_picture(os.path.join(HERE, "ctr10.png"), width=Cm(8.5))
    d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    Q("a)", "Combien d'états différents ce compteur peut-il prendre ? Quelle est sa valeur maximale ?")
    ANS("2^{10} = 1024 états, de 0d à 1023d. Valeur maximale : 1023d = 11 1111 1111b.")
    Q("b)", "Calcule 854d + 300d. Le compteur peut-il afficher ce résultat ?")
    ANS("854d + 300d = 1154d > 1023d : impossible, il faudrait 11 bits.")
    Q("c)", "Après combien d'impulsions le compteur atteint-il 1023d ? Que se passe-t-il à l'impulsion suivante ?")
    ANS("1023d − 854d = 169 impulsions. À la 170e, il repasse à 0d : c'est le débordement (overflow).")
    Q("d)", "Quelle valeur affiche-t-il après les 300 impulsions ?")
    ANS("Il reste 300 − 170 = 130 impulsions après le passage à 0 → il affiche 130d. Contrôle : 1154d − 1024d = 130d.")
    Q("e)", "Explique avec tes mots ce qui s'est passé.")
    ANS("Le compteur a dépassé sa capacité (1023d) : il a « fait le tour » et recommencé à 0. La valeur correcte (1154d) est perdue, il reste 1154d − 1024d = 130d. Il faudrait un 11e bit (ou un signal de débordement) pour la garder.", 2)
    BOX(["Si difficulté – 2e son de cloche",
         "Comparer avec le compteur kilométrique d'un vieux scooter à 3 chiffres : à 999 km, encore 1 km → 000. Le compteur 10 bits fait la même chose à 1023 → 0. Ou une horloge : 22 h + 5 h = 3 h, pas 27 h."])

    P("**Option (s'il reste du temps) : l'addition directement en binaire**", before=8, keep=True)
    Q("f)", "Écris 854d et 300d en binaire sur 10 bits, puis additionne-les en binaire (avec les retenues).")
    a, b = 854, 300
    car = [""] * 11; c = 0
    for i in range(10):
        t = ((a >> i) & 1) + ((b >> i) & 1) + c; c = t >> 1
        car[10 - (i + 1)] = str(c) if c else ""
    sa, sb, ss = format(a, "011b"), format(b, "011b"), format(a + b, "011b")
    widths = [1.25] + [0.45] * 11 + [TW - 1.25 - 0.45 * 11 - 0.05]
    TABLE(widths, [
        ["Poids", "1024", "512", "256", "128", "64", "32", "16", "8", "4", "2", "1", "Décimal"],
        ["Retenues"] + [("R", x) for x in car] + [""],
        ["854d"] + [""] + [("R", x) for x in sa[1:]] + ["854d"],
        ["+ 300d"] + [""] + [("R", x) for x in sb[1:]] + ["300d"],
        ["Résultat"] + [("R", x) for x in ss] + [("R", "1154d")],
        ["Affiché (10 bits)"] + [""] + [("R", x) for x in format((a + b) % 1024, "010b")] + [("R", "130d")],
    ], first_col_left=True, height=0.32, size=9)
    Q("g)", "Quel bit le compteur 10 bits « perd »-il ? Que vaut-il en décimal ?")
    ANS("Le 11e bit (poids 2^{10} = 1024d). Le supprimer revient à soustraire 1024d : 1154d − 1024d = 130d = 00 1000 0010b.", 2)
    BOX(["Si difficulté – addition binaire",
         "Règles : 0 + 0 = 0 ; 0 + 1 = 1 ; 1 + 1 = 0 retenue 1 ; 1 + 1 + 1 = 1 retenue 1. Faire écrire les retenues sur la ligne du haut, comme en primaire."])

    d.save(out); print("ok", out)


if __name__ == "__main__":
    o = "/mnt/user-data/outputs"
    build(False, f"{o}/EX Systemes de numeration - exercices en groupe.docx")
    build(True, f"{o}/EX C Systemes de numeration - exercices en groupe.docx")
