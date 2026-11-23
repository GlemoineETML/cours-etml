# -*- coding: utf-8 -*-
"""Feuille d'exercices + corrigé « Arithmétique binaire, code Gray et compléments ».
Charte ETML Rapport_Simple (A4, Arial) + couleurs ETML (marine 242852, bleu 297FD5, bleu clair ACCBF9), en-tête logo + « Section électronique »,
pied de page 3 colonnes). Réponses en rouge EE0000 dans le corrigé, vides dans la version élève."""
import os, re, datetime as dt
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

RED = RGBColor(0xEE, 0x00, 0x00)
GREY = RGBColor(0x5A, 0x64, 0x78)
NAVY = RGBColor(0x24, 0x28, 0x52)
HEX_NAVY, HEX_BLUE, HEX_LBLUE, HEX_TINT = "242852", "297FD5", "ACCBF9", "E8EFFB"
BASE = "etml_base.docx"   # = Rapport_Simple.dotx avec content-type template.main → document.main (voir prep_modele.py)
MODULE = "Test et Mesure 1 – El DT 1"
MATIERE = "Test et Mesure 1 – El DT 1"
CLASSE = "XLO1"
ANNEE = "2026-2027"
CHAMP = "LZ_4258"
FLOYD = "https://eduvaud.sharepoint.com/:b:/r/sites/msteams_76c9d9/Documents%20partages/Documentation/Electronique%20num%C3%A9rique%20TMLO/10%20Floyd%20V11/10%20Floyd%20V11%20Basse%20d%C3%A9finition%20par%20chapitre/Chap%2002%20-%20Syst%C3%A8mes%20de%20num%C3%A9ration,%20op%C3%A9rations%20et%20codes.pdf?d=w933f2237d1814185b6a6b02be82abe0b&csf=1&web=1&e=eHqofE"   # Floyd chap. 2 sur Teams (SharePoint)
TW = 21.0 - 2.0 - 1.5           # largeur utile en cm
TITLE = "Arithmétique binaire, code Gray et compléments"
NEXTEC_TOPIC = "https://app.nextecmedia.ch/resolve?courseProductReference=P108e2&issueProductReference=P108e7&contentType=topic&fileReference=F15614_2&contentId=5.1&contentReference=23060"
NEXTEC_GRAY = "https://app.nextecmedia.ch/resolve?courseProductReference=P108e2&issueProductReference=P108e7&contentType=exercise&exerciseGroup=16&contentId=&contentReference=24154"

b = lambda v, n: format(v, f"0{n}b")
sp = lambda s: " ".join(s[max(0, i - 4):i] for i in range(len(s), 0, -4))[::-1][::-1] if False else _sp(s)


def _sp(s):
    """Groupe par quartets depuis la droite : 01101101 → 0110 1101."""
    out = []
    while s:
        out.insert(0, s[-4:]); s = s[:-4]
    return " ".join(out)


def gray(v): return v ^ (v >> 1)


def gray2bin(g):
    v = 0
    while g:
        v ^= g; g >>= 1
    return v


def c2(v, n=8): return (-v) % (2 ** n)


# ------------------------------------------------------------------ briques XML
def set_cell_border(cell, **kw):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = tcPr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders"); tcPr.append(borders)
    for side, val in kw.items():
        e = OxmlElement(f"w:{side}")
        for k, v in val.items(): e.set(qn(f"w:{k}"), str(v))
        borders.append(e)


def tbl_no_borders(t):
    tblPr = t._tbl.tblPr; bd = OxmlElement("w:tblBorders")
    for sd in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{sd}"); e.set(qn("w:val"), "nil"); bd.append(e)
    tblPr.append(bd)


def p_border(p, sides, sz=4, color="297FD5"):
    pPr = p._p.get_or_add_pPr()
    bd = pPr.find(qn("w:pBdr"))
    if bd is None: bd = OxmlElement("w:pBdr"); pPr.append(bd)
    for sd in sides:
        e = OxmlElement(f"w:{sd}")
        for k, v in (("val", "single"), ("sz", sz), ("space", 4), ("color", color)): e.set(qn(f"w:{k}"), str(v))
        bd.append(e)


def field(p, code, cached, size=None, bold=False, italic=False, font=None):
    def r_(child):
        r = OxmlElement("w:r"); rp = OxmlElement("w:rPr")
        if font:
            rf = OxmlElement("w:rFonts"); rf.set(qn("w:ascii"), font); rf.set(qn("w:hAnsi"), font); rp.append(rf)
        if bold: rp.append(OxmlElement("w:b"))
        if italic: rp.append(OxmlElement("w:i"))
        if size:
            s = OxmlElement("w:sz"); s.set(qn("w:val"), str(int(size * 2))); rp.append(s)
        r.append(rp); r.append(child); p._p.append(r)
    fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin"); r_(fc)
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = f" {code} "; r_(it)
    fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "separate"); r_(fc)
    t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = cached; r_(t)
    fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "end"); r_(fc)


def hyperlink(p, url, text, size=None):
    part = p.part
    if not url.startswith("http"):
        from urllib.parse import quote
        url = quote(url)
    rid = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), rid)
    r = OxmlElement("w:r"); rp = OxmlElement("w:rPr")
    col = OxmlElement("w:color"); col.set(qn("w:val"), "297FD5"); rp.append(col)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rp.append(u)
    if size:
        s = OxmlElement("w:sz"); s.set(qn("w:val"), str(int(size * 2))); rp.append(s)
    r.append(rp); t = OxmlElement("w:t"); t.text = text; t.set(qn("xml:space"), "preserve"); r.append(t)
    h.append(r); p._p.append(h)


SUB = re.compile(r"_\{([^}]*)\}|\^\{([^}]*)\}|\*\*([^*]*)\*\*")


def rich(p, txt, color=None, bold=False, italic=False, size=None, font=None):
    pos = 0
    def add(t, sub=False, sup=False, bb=False):
        r = p.add_run(t); r.bold = bold or bb; r.italic = italic
        if color is not None: r.font.color.rgb = color
        if size: r.font.size = Pt(size)
        if font: r.font.name = font; r._element.rPr.rFonts.set(qn("w:hAnsi"), font)
        if sub: r.font.subscript = True
        if sup: r.font.superscript = True
    for m in SUB.finditer(txt):
        if m.start() > pos: add(txt[pos:m.start()])
        if m.group(1) is not None: add(m.group(1), sub=True)
        elif m.group(2) is not None: add(m.group(2), sup=True)
        else: add(m.group(3), bb=True)
        pos = m.end()
    if pos < len(txt): add(txt[pos:])
    return p



ORD = {
 "pPr": "pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange".split(),
 "tcPr": "cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar textDirection tcFitText vAlign hideMark".split(),
 "tblPr": "tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize tblStyleColBandSize tblW jc tblCellSpacing tblInd tblBorders shd tblLayout tblCellMar tblLook tblCaption tblDescription".split(),
}
def reorder(root):
    for tag, order in ORD.items():
        for el in root.iter(qn("w:" + tag)):
            kids = list(el)
            key = lambda e: order.index(e.tag.split("}")[1]) if e.tag.split("}")[1] in order else 99
            kids.sort(key=key)
            for k in kids: el.remove(k)
            for k in kids: el.append(k)

# ------------------------------------------------------------------ document
def build(corr, out):
    d = Document(BASE)   # modèle ETML Rapport_Simple (.dotx → .docx) : styles, police, en-tête, pied de page
    body = d.element.body
    for el in list(body):
        if el.tag != qn("w:sectPr"): body.remove(el)
    now = dt.datetime.now()
    kind = "Corrigé" if corr else "Exercices"
    title_doc = f"{TITLE} – {kind}"
    cp = d.core_properties
    cp.title = title_doc; cp.author = "Gaël Lemoine"; cp.last_modified_by = "Gaël Lemoine"; cp.created = now; cp.modified = now; cp.last_printed = now
    cp.revision = 1; cp.subject = f"{MATIERE} – {CLASSE} – {ANNEE}"
    sec = d.sections[0]
    # en-tête du modèle : « Nom - Type - Numéro » → titre – type – matière ; textes en bleu marine
    for t in sec.header._element.iter(qn("w:t")):
        if t.text == "Nom -": t.text = f"Arithmétique binaire et code Gray – {kind} – El DT 1"
        elif t.text in (" ", "Type - Numéro"): t.text = ""
    for r in sec.header._element.iter(qn("w:r")):
        if r.find(qn("w:t")) is not None and (r.find(qn("w:t")).text or "").strip():
            rPr = r.find(qn("w:rPr"))
            if rPr is None: rPr = OxmlElement("w:rPr"); r.insert(0, rPr)
            c = OxmlElement("w:color"); c.set(qn("w:val"), HEX_NAVY); rPr.append(c)
    # valeurs affichées des champs du pied de page (Word les met à jour à l'ouverture / impression)
    vals = {"AUTHOR": "Gaël Lemoine", "LASTSAVEDBY": "Gaël Lemoine", "SAVEDATE": now.strftime("%d.%m.%Y %H:%M"),
            "CREATEDATE": now.strftime("%d.%m.%Y"), "PRINTDATE": now.strftime("%d.%m.%Y %H:%M"),
            "FILENAME": os.path.basename(out), "TITLE": title_doc}
    for part in (sec.footer._element, sec.header._element):
        cur = None; state = None
        for r in list(part.iter(qn("w:r"))):
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
                if cur == "_done": t.text = ""
                else: t.text = vals[cur]; cur = "_done"
    # couleurs ETML sur les titres (police et tailles = celles du modèle)
    for name in ("Title", "Heading 1", "Heading 2"):
        try:
            st_ = d.styles[name]; st_.font.color.rgb = NAVY; st_.paragraph_format.keep_with_next = True
        except KeyError:
            pass

    # ---------------- helpers de contenu
    def P(txt="", after=3, before=0, align=None, keep=False, **kw):
        p = d.add_paragraph(); f = p.paragraph_format
        f.space_after = Pt(after); f.space_before = Pt(before); f.keep_with_next = keep
        if align is not None: p.alignment = align
        if kw.get("size") and kw["size"] <= 10: f.line_spacing = 1.15   # contextes et renvois : interligne serré
        rich(p, txt, **kw); return p

    def EX(n, title, ref=None):
        p = d.add_paragraph(); f = p.paragraph_format
        f.space_before = Pt(8); f.space_after = Pt(2); f.keep_with_next = True
        r = p.add_run(f"N°{n} {title}"); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = NAVY
        if ref:
            if "Floyd" in ref:
                i0 = ref.index("Floyd"); i1 = ref.find(" · ", i0); i1 = len(ref) if i1 < 0 else i1
                q = P(ref[:i0], italic=True, size=9, color=GREY, keep=True, after=3)
                hyperlink(q, FLOYD, ref[i0:i1], size=9)
                if ref[i1:]: rich(q, ref[i1:], italic=True, size=9, color=GREY)
            else:
                q = P(ref, italic=True, size=9, color=GREY, keep=True, after=3)

    def HR():
        p = d.add_paragraph(); p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
        p_border(p, ["bottom"], 4)

    def Q(lbl, txt):
        p = d.add_paragraph(); f = p.paragraph_format
        f.left_indent = Cm(0.7); f.first_line_indent = Cm(-0.7); f.space_before = Pt(3); f.space_after = Pt(2)
        f.tab_stops.add_tab_stop(Cm(0.7)); f.keep_with_next = True
        r = p.add_run(lbl + "\t"); r.bold = True
        rich(p, txt); return p

    def ANS(txt, lines=1, mono=False):
        if corr:
            for i, t in enumerate(txt.split("\n")):
                p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7)
                p.paragraph_format.space_after = Pt(1 if i < len(txt.split("\n")) - 1 else 4)
                rich(p, t, color=RED, font="Courier New" if mono else None, size=10.5 if mono else None)
        else:
            for _ in range(lines):
                p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7); p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.tab_stops.add_tab_stop(Cm(TW), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
                p.add_run("\t")

    def BOX(lines, only_corr=True):
        if only_corr and not corr: return
        for i, t in enumerate(lines):
            p = d.add_paragraph(); f = p.paragraph_format
            f.left_indent = Cm(0.2); f.right_indent = Cm(0.2)
            f.space_before = Pt(4 if i == 0 else 0); f.space_after = Pt(6 if i == len(lines) - 1 else 0)
            f.keep_with_next = i < len(lines) - 1
            p_border(p, ["top", "left", "bottom", "right"], 4)
            rich(p, t, bold=(i == 0), italic=(i > 0), size=9.5)

    def cell_txt(c, txt, bold=False, italic=False, color=None, size=10, align="center", mono=False, shade=None):
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]; f = p.paragraph_format; f.space_after = Pt(0); f.space_before = Pt(0); f.line_spacing = 1.0
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if align == "center" else WD_ALIGN_PARAGRAPH.LEFT
        rich(p, txt, color=color, bold=bold, italic=italic, size=size, font="Courier New" if mono else None)
        if shade:
            tcPr = c._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
            sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), shade); tcPr.append(sh)

    def TABLE(widths, rows, header=True, height=0.6, size=10, first_left=True, mono_cols=()):
        """('R', txt) = réponse : rouge dans le corrigé, vide pour l'élève. ('G', txt) = texte grisé fixe."""
        t = d.add_table(rows=len(rows), cols=len(widths)); t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
        for i, row in enumerate(rows):
            tr = t.rows[i]; tr.height = Cm(height)
            for j, v in enumerate(row):
                c = tr.cells[j]; c.width = Cm(widths[j])
                hdr_ = header and i == 0
                al = "left" if (first_left and j == 0) else "center"
                mono = j in mono_cols and not hdr_
                if isinstance(v, tuple) and v[0] == "R":
                    cell_txt(c, v[1] if corr else "", color=RED if corr else None, bold=True, size=size, align=al, mono=mono)
                elif isinstance(v, tuple) and v[0] == "S":   # fond gris (ligne résultat)
                    cell_txt(c, v[1], size=size, align=al, mono=mono, shade=HEX_TINT, bold=True)
                else:
                    cell_txt(c, v, italic=hdr_, bold=(first_left and j == 0 and not hdr_), size=size, align=al, mono=mono,
                             shade=HEX_LBLUE if hdr_ else None, color=NAVY if hdr_ else None)
        for j, w in enumerate(widths): t.columns[j].width = Cm(w)
        for i, tr in enumerate(t.rows):
            tr._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
            if i < len(t.rows) - 1:
                for c in tr.cells:
                    for pp in c.paragraphs: pp.paragraph_format.keep_with_next = True
        spc = d.add_paragraph(); spc.paragraph_format.space_after = Pt(2); spc.paragraph_format.line_spacing = 1.0
        return t

    def ADD(a, bb, n, label):
        """Tableau d'addition en colonnes avec retenues. n = nombre de bits des opérandes."""
        W = [2 ** i for i in range(n, -1, -1)]
        carry = [""] * (n + 1); c = 0
        for i in range(n):
            s_ = ((a >> i) & 1) + ((bb >> i) & 1) + c; c = s_ >> 1
            if c: carry[n - i - 1] = "1"
        s = b(a + bb, n + 1)
        cw = 1.2
        widths = [2.4] + [cw] * (n + 1) + [TW - 2.4 - cw * (n + 1) - 0.02]
        rows = [[label] + [str(w) for w in W] + ["Contrôle décimal"],
                ["Retenues"] + [("R", x) for x in carry] + [""],
                ["A"] + [""] + list(b(a, n)) + [f"{a}d"],
                ["+ B"] + [""] + list(b(bb, n)) + [f"{bb}d"],
                ["= Somme"] + [("R", x) for x in s] + [("R", f"{a + bb}d")]]
        TABLE(widths, rows, height=0.55, size=11, mono_cols=tuple(range(1, n + 2)))

    # ================= TITRE
    d.add_paragraph(TITLE, style="Title")
    P(f"Feuille d'exercices – {MATIERE} · Classe {CLASSE} · {ANNEE} · Champ d'apprentissage {CHAMP}", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, after=8)
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.paragraph_format.space_after = Pt(0)
    r = p.add_run("Corrigé" if corr else "Version apprenti·e"); r.bold = True
    if corr: r.font.color.rgb = RED
    p.add_run("\tNom :")
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.add_run("\tDate :")
    p_border(p, ["bottom"], 4)

    if corr:
        BOX(["Plan de séance (enseignant·e) – 2 × 45 min",
             "Séance 1 : N°1 à N°3 (addition, × 2 par décalage, multiplication). Séance 2 : N°4 à N°10 (Gray, bouton rotatif, compléments, nombres signés). N°11 = exercice mélangé pour la révision espacée : à donner une semaine plus tard, en début de cours, sans la fiche.",
             "Différenciation : les encadrés « Si difficulté » donnent un deuxième chemin d'explication à proposer à l'apprenti·e qui bloque ; les apprentis rapides font les questions « Bonus » puis l'exercice Nextec sur le code Gray.",
             "Chaque exercice se termine par un contrôle (décimal, table, ou nombre + C2 = 0) : exiger qu'il soit écrit, c'est la compétence visée (vérifier son propre résultat)."])

    P("**Convention :** suffixe à la fin du nombre – **b** binaire (0101b), **d** décimal (5d), **Gray** pour le code Gray (0111 Gray). Les nombres de 8 bits sont écrits par groupes de 4 bits (0110 1101b). Pas de calculatrice : on écrit le raisonnement et on contrôle chaque résultat.", after=4)
    P("**Ressources :** ", after=1, keep=True)
    pr_ = P("Nextec Media : ", after=1, size=10); hyperlink(pr_, NEXTEC_TOPIC, "chapitre 5.1 – Systèmes de numération et codes", size=10)
    pr_ = P("Nextec Media : ", after=1, size=10); hyperlink(pr_, NEXTEC_GRAY, "exercice complémentaire sur le code Gray", size=10)
    pr_ = P("Floyd, Systèmes numériques : ", after=6, size=10)
    hyperlink(pr_, FLOYD, "chapitre 2 (PDF) – Systèmes de numération, opérations et codes", size=10)
    rich(pr_, " : §2-4 Arithmétique binaire (p. 60-63) · §2-5 Compléments (p. 63-65) · §2-6 Nombres signés (p. 65-68) · §2-7 Opérations avec nombres signés (p. 71-73) · §2-11 Code Gray (p. 90-92).", size=10)

    # ================= AIDE-MÉMOIRE
    d.add_heading("Aide-mémoire", level=1)
    TABLE([3.3, TW - 3.3 - 4.2 - 0.02, 4.2], [
        ["Opération", "Méthode", "Exemple"],
        ["Addition", "Colonne par colonne, de droite à gauche. 0+0 = 0 · 0+1 = 1 · 1+1 = 0 retenue 1 · 1+1+1 = 1 retenue 1.", "0011b + 0001b = 0100b"],
        ["× 2ⁿ   ÷ 2", "× 2 = décaler d'un rang à gauche (un 0 entre à droite). × 2ⁿ = n rangs. ÷ 2 = un rang à droite (le LSB est perdu).", "0000 0101b × 4 = 0001 0100b"],
        ["Multiplication", "Produits partiels : bit 1 → recopier le nombre, bit 0 → des zéros ; décaler d'un rang à chaque ligne, puis additionner.", "101b × 11b = 1111b"],
        ["Binaire → Gray", "Recopier le MSB, puis bits binaires voisins différents → 1, identiques → 0 (OU exclusif).", "1011b → 1110 Gray"],
        ["Gray → binaire", "Recopier le MSB, puis bit binaire trouvé ⊕ bit Gray suivant.", "1101 Gray → 1001b"],
        ["Complément à 1", "Inverser tous les bits (sur le nombre de bits fixé).", "0010 1101b → 1101 0010b"],
        ["Complément à 2", "C1 + 1 (ou : recopier de droite jusqu'au premier 1 inclus, inverser le reste). Contrôle : nombre + C2 = 0.", "0010 1101b → 1101 0011b"],
        ["Nombre signé (8 bits)", "En C2, le MSB pèse −128. Étendue : −128d à +127d. Soustraire = additionner le C2, retenue finale rejetée.", "1101 0011b = −45d"],
    ], height=0.7, size=9.5)

    # ================= EXERCICES
    d.add_heading("Exercices", level=1)

    # ---- N°1 Addition
    EX(1, "Addition binaire avec retenues", "Méthode : diapositives 4 à 6 · Floyd §2-4 p. 60-61, problème 15")
    P("Contexte : l'unité de calcul (UAL) de tout microcontrôleur additionne ainsi. Exemple d'atelier : un automate compte les pièces sorties de deux lignes de production et additionne les deux compteurs (question d).", italic=True, size=10, keep=True)
    P("Effectue chaque addition en écrivant toutes les retenues, puis contrôle en décimal.", keep=True)
    for lbl, a_, b_, n in (("a)", 6, 3, 4), ("b)", 11, 7, 4), ("c)", 78, 53, 8), ("d)", 217, 108, 8)):
        Q(lbl, f"{_sp(b(a_, n))}b + {_sp(b(b_, n))}b")
        ADD(a_, b_, n, "Poids")
    Q("e)", "Pour d) : la ligne 1 a produit 217 pièces, la ligne 2 en a produit 108. L'automate range le total dans un registre de 8 bits. Le résultat tient-il ? Qu'affiche l'automate ?")
    ANS("Non : 325d > 255d, il faut 9 bits. Le registre ne garde que les 8 bits de droite 0100 0101b = 69d (= 325d − 256d). C'est un dépassement (overflow) : la retenue finale est perdue et l'automate affiche 69 pièces au lieu de 325. Il faudrait un registre de 16 bits.", 2)
    BOX(["Si difficulté – 2e son de cloche",
         "Faire l'addition en décimal avec des « paquets de 2 » : dans chaque colonne on ne peut écrire que 0 ou 1 ; dès qu'on a 2, on écrit 0 et on passe 1 paquet à la colonne de gauche ; avec 3, on écrit 1 et on passe 1 paquet. Toujours écrire les poids au-dessus des colonnes."])

    # ---- N°2 ×2 et décalages (vient avant les produits partiels : chaque produit partiel est une copie décalée)
    HR(); EX(2, "Multiplier par 2, 4, 8… par décalage", "Méthode : diapositive 7")
    P("Contexte : dans un microcontrôleur, un décalage d'un rang (instruction « shift ») prend un seul cycle d'horloge ; c'est la façon la plus rapide de multiplier ou diviser par 2, 4, 8… On l'utilise par exemple pour mettre à l'échelle une mesure de capteur.", italic=True, size=10, keep=True)
    Q("a)", "Complète le tableau (registre de 8 bits) à partir de 0000 0111b = 7d.")
    TABLE([3.0, 4.0, 3.0, TW - 10.0 - 0.02], [
        ["Opération", "Résultat (8 bits)", "Décimal", "Nombre de décalages et sens"],
        ["0000 0111b", "0000 0111b", "7d", "—"],
        ["× 2", ("R", "0000 1110b"), ("R", "14d"), ("R", "1 rang à gauche")],
        ["× 4", ("R", "0001 1100b"), ("R", "28d"), ("R", "2 rangs à gauche")],
        ["× 8", ("R", "0011 1000b"), ("R", "56d"), ("R", "3 rangs à gauche")],
        ["× 16", ("R", "0111 0000b"), ("R", "112d"), ("R", "4 rangs à gauche")],
        ["÷ 2", ("R", "0000 0011b"), ("R", "3d"), ("R", "1 rang à droite, le LSB (1) est perdu : 7d = 2 × 3d + 1")],
    ], height=0.55, size=10, mono_cols=(1,))
    Q("b)", "Le registre contient 0110 0000b. On le multiplie par 4 par décalage. Que contient le registre ? Est-ce le bon résultat ?")
    ANS("0110 0000b = 64 + 32 = 96d. Deux décalages à gauche : 1 1000 0000b = 256 + 128 = 384d, mais le registre ne garde que 8 bits → 1000 0000b = 128d. Faux : le bit de poids 256 est sorti du registre, c'est un dépassement (384d > 255d).", 2)
    BOX(["Si difficulté – 2e son de cloche",
         "En décimal, × 10 ajoute un zéro à droite (37 → 370) parce que la base est 10. En binaire, la base est 2 : ajouter un zéro à droite multiplie par 2. Faire glisser physiquement une bande de papier avec les bits sous une grille de 8 cases : ce qui sort à gauche tombe hors du registre."])

    # ---- N°3 Multiplication par produits partiels (grille alignée par poids)
    HR(); EX(3, "Multiplication binaire par produits partiels", "Méthode : diapositives 8 à 10 · Floyd §2-4 p. 62, problème 17")
    P("Pose chaque multiplication dans la grille : une ligne par bit du multiplicateur (bit à 1 → copie du multiplicande, bit à 0 → ligne de 0), chaque ligne décalée d'un rang de plus, puis additionne les lignes avec les retenues. Contrôle en décimal.", keep=True)
    def MULT(x, y):
        nb = len(b(x * y, 1)); ny = len(b(y, 1)); nx = len(b(x, 1))
        W = [2 ** i for i in range(nb - 1, -1, -1)]
        def row(v, shift, length):
            out = []
            for p in range(nb - 1, -1, -1):
                if p < shift: out.append("0")
                elif p >= shift + length: out.append("")
                else: out.append(str((v >> (p - shift)) & 1))
            return out
        lines = [((y >> k) & 1, (x if (y >> k) & 1 else 0) << k) for k in range(ny)]
        carry = [""] * nb; c = 0
        for p in range(nb):
            t = sum((v >> p) & 1 for _, v in lines) + c; c = t >> 1
            assert c <= 1
            if c and p + 1 < nb: carry[nb - 2 - p] = "1"
        widths = [3.4] + [1.05] * nb + [TW - 3.4 - 1.05 * nb - 0.02]
        rows = [["", *[str(w) for w in W], "Explication"],
                ["Multiplicande", *row(x, 0, nx), f"{x}d"],
                ["× multiplicateur", *row(y, 0, ny), f"{y}d"]]
        for k, (bit, v) in enumerate(lines):
            rows.append([f"Ligne {k + 1} (poids {2 ** k})", *[("R", d) for d in row(x if bit else 0, k, nx)],
                         ("R", f"bit = {bit} → {'copie' if bit else 'ligne de 0'}" + (f", décalée de {k} rang{'s' if k > 1 else ''}" if k else ""))])
        rows.append(["Retenues", *[("R", d) for d in carry], ""])
        rows.append(["= Produit", *[("R", d) for d in b(x * y, nb)], ("R", f"= {x * y}d ✓ ({x}d × {y}d)")])
        TABLE(widths, rows, height=0.6, size=10, mono_cols=tuple(range(1, nb + 1)))
    for lbl, x, y in (("a)", 6, 3), ("b)", 14, 5), ("c)", 13, 10)):
        Q(lbl, f"{b(x, 1)}b × {b(y, 1)}b")
        MULT(x, y)
    Q("d)", "Calcule 25d × 6d uniquement avec des décalages et une addition (indice : 6d = 110b = 4d + 2d). Écris les nombres en binaire sur 8 bits.")
    ANS("25d = 0001 1001b. 25d × 4d → 2 décalages : 0110 0100b = 64 + 32 + 4 = 100d. 25d × 2d → 1 décalage : 0011 0010b = 32 + 16 + 2 = 50d.\n0110 0100b + 0011 0010b = 1001 0110b = 128 + 16 + 4 + 2 = 150d = 100d + 50d ✓", 3)
    Q("e)", "Un microcontrôleur lit la valeur 0001 0111b sur un capteur. Pour la convertir en millivolts, il doit la multiplier par 5. Calcule-le avec un décalage et une addition (5d = 4d + 1d), comme à la diapositive 10.")
    ANS("0001 0111b = 16 + 4 + 2 + 1 = 23d. 23d × 4d → 2 décalages : 0101 1100b = 64 + 16 + 8 + 4 = 92d. On ajoute 23d : 0101 1100b + 0001 0111b = 0111 0011b = 64 + 32 + 16 + 2 + 1 = 115d = 23d × 5d ✓ → 115 mV.", 3)
    Q("f)", "Bonus : comment multiplier par 10 avec des décalages ? Applique à 0000 1001b.")
    ANS("10d = 1010b = 8d + 2d : (n × 8) + (n × 2). 9d × 8d → 3 décalages : 0100 1000b = 64 + 8 = 72d ; 9d × 2d → 1 décalage : 0001 0010b = 16 + 2 = 18d ; somme = 0101 1010b = 64 + 16 + 8 + 2 = 90d ✓", 2)
    BOX(["Si difficulté",
         "La table de multiplication binaire n'a que 4 cases (0×0 = 0, 0×1 = 0, 1×0 = 0, 1×1 = 1) : dans une ligne, on ne calcule jamais rien, on recopie le multiplicande ou on écrit des 0. Faire écrire les poids en haut de la grille : chaque ligne commence une colonne plus à gauche que la précédente. La seule vraie difficulté est l'addition finale, colonne par colonne avec les retenues (N°1)."])

    # ---- N°4 Binaire → Gray
    HR(); EX(4, "Convertir binaire → Gray", "Méthode : diapositive 14 · Floyd §2-11 p. 90-91, exemple 2-37, problème 56")
    P("Contexte : pour graver le disque d'un codeur absolu ou contrôler ses sorties au banc de test, il faut connaître le code Gray de chaque position.", italic=True, size=10, keep=True)
    vals = [("0110b", 0b0110, 4), ("1010b", 0b1010, 4), ("0111b", 0b0111, 4), ("1 1010b", 0b11010, 5), ("1100 0110b", 0b11000110, 8)]
    TABLE([3.0, 3.2, 4.0, TW - 10.2 - 0.02], [["Binaire", "Décimal", "Code Gray", "Détail (MSB recopié, puis comparaisons)"]] +
          [[lab, ("R", f"{v}d"), ("R", _sp(b(gray(v), n)) + " Gray"),
            ("R", " · ".join([b(v, n)[0] + " recopié"] + [b(v, n)[i] + ("≠" if b(v, n)[i] != b(v, n)[i + 1] else "=") + b(v, n)[i + 1] + "→" + ("1" if b(v, n)[i] != b(v, n)[i + 1] else "0") for i in range(n - 1)]))] for lab, v, n in vals],
          height=0.6, size=10, mono_cols=(0, 2))
    P("Contrôle : pour les nombres de 4 bits, vérifie ton résultat avec la table Gray de la diapositive 13.", italic=True, size=10)

    # ---- N°5 Gray → binaire
    HR(); EX(5, "Convertir Gray → binaire", "Méthode : diapositive 15 · Floyd §2-11 p. 91, problème 57")
    P("Contexte : le microcontrôleur d'un bras de robot lit le code Gray de son codeur ; pour calculer l'angle, il doit d'abord le convertir en binaire.", italic=True, size=10, keep=True)
    gv = [("0111 Gray", 0b0111, 4), ("1111 Gray", 0b1111, 4), ("1000 Gray", 0b1000, 4), ("1 1101 Gray", 0b11101, 5), ("1010 1111 Gray", 0b10101111, 8)]
    TABLE([3.6, 4.0, 3.0, TW - 10.6 - 0.02], [["Code Gray", "Binaire", "Décimal", "Contrôle : reconvertir en Gray"]] +
          [[lab, ("R", _sp(b(gray2bin(g), n)) + "b"), ("R", f"{gray2bin(g)}d"), ("R", _sp(b(gray(gray2bin(g)), n)) + " Gray ✓")] for lab, g, n in gv],
          height=0.6, size=10, mono_cols=(0, 1))
    Q("a)", "Un codeur absolu de 4 bits divise le tour en 16 positions de 22,5° chacune. Il lit 1111 Gray. Quel est l'angle de l'axe ?")
    ANS("1111 Gray → 1010b = 10d (voir le tableau) → 10 × 22,5° = 225°.", 1)
    BOX(["Si difficulté",
         "Erreur typique : comparer deux bits Gray voisins (on retrouve alors la règle binaire → Gray, qui est l'autre sens). Faire dessiner les flèches en diagonale : chaque nouveau bit binaire vient du bit binaire de gauche ET du bit Gray du dessus. Contrôle systématique : reconvertir le résultat en Gray."])

    # ---- N°6 Codeur rotatif
    HR(); EX(6, "Le codeur absolu 3 bits", "Méthode : diapositives 11 à 13 · Floyd §2-11 p. 91-92, fig. 2-7, problème 55 · ")
    hyperlink(d.paragraphs[-1], NEXTEC_GRAY, "exercice Nextec Media sur le code Gray", size=9)
    P("Contexte : sur un axe de moteur ou l'articulation d'un robot, la position doit être juste dès la mise sous tension. On utilise un disque codeur à 3 pistes et 8 secteurs. Trois capteurs optiques lisent les pistes (piste intérieure = MSB, secteur foncé = 1).", keep=True)
    Q("a)", "Construis la table du code Gray à 3 bits avec la méthode du miroir.")
    TABLE([3.0] + [1.75] * 8, [["Secteur (d)"] + [str(i) for i in range(8)],
                               ["Binaire"] + [b(i, 3) for i in range(8)],
                               ["Gray"] + [("R", b(gray(i), 3)) for i in range(8)],
                               ["Angle (°)"] + [("R", f"{i * 45}–{i * 45 + 45}") for i in range(8)]],
          header=True, height=0.55, size=10, mono_cols=tuple(range(1, 9)))
    Q("b)", "Colorie en foncé les cases à 1 du disque en code Gray (piste intérieure = MSB, extérieure = LSB).")
    d.add_picture("fig_disque_corr.png" if corr else "fig_disque_vierge.png", width=Cm(5.5))
    d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    Q("c)", "Avec un disque en binaire naturel, l'axe passe du secteur 3 au secteur 4. Combien de bits changent ? Les capteurs n'étant pas parfaitement alignés, quelles valeurs fausses peuvent être lues brièvement ?")
    ANS("011 → 100 : les 3 bits changent. Chaque capteur peut basculer avant ou après les autres : on peut lire brièvement n'importe quelle combinaison intermédiaire, soit 000, 001, 010, 101, 110 ou 111 (6 lectures fausses possibles, par ex. 111 = secteur 7 !).", 2)
    Q("d)", "Même question avec le disque en code Gray. Conclusion ?")
    ANS("010 → 110 : un seul bit change (le MSB). On lit soit 010 (secteur 3), soit 110 (secteur 4) : aucune lecture fausse. C'est pour cela que les codeurs angulaires utilisent le code Gray.", 2)
    Q("e)", "Le capteur lit 101 Gray. Dans quel secteur est l'axe, et quel est son angle ?")
    ANS("101 Gray → binaire 110b = 6d → secteur 6, entre 270° et 315°.", 1)

    # ---- N°7 Bouton rotatif (codeur incrémental, Gray 2 bits)
    HR(); EX(7, "Le bouton de volume (codeur incrémental)", "Méthode : diapositive 12")
    P("Contexte : le bouton de volume d'un autoradio ou la molette d'une souris ne tourne pas un potentiomètre, mais un codeur incrémental. Deux contacts A et B donnent la suite 00 → 01 → 11 → 10 → 00 (code Gray à 2 bits). Le microcontrôleur lit A et B et ajoute 1 au volume à chaque cran dans le sens horaire, ou enlève 1 dans le sens antihoraire.", italic=True, size=10, keep=True)
    Q("a)", "Complète la suite lue en tournant dans le sens horaire, à partir de 00, puis indique quel contact change à chaque cran.")
    TABLE([3.0] + [2.9] * 5, [["Cran", "0", "1", "2", "3", "4"],
                             ["A B (horaire)", "00", ("R", "01"), ("R", "11"), ("R", "10"), ("R", "00")],
                             ["Contact qui change", "—", ("R", "B"), ("R", "A"), ("R", "B"), ("R", "A")]],
          height=0.55, size=10, mono_cols=(1, 2, 3, 4, 5))
    Q("b)", "Le microcontrôleur lit successivement 11 → 10 → 00. Dans quel sens tourne le bouton ?")
    ANS("Sens horaire : dans la suite horaire 00 → 01 → 11 → 10 → 00, on trouve bien 11 → 10 → 00.", 1)
    Q("c)", "Il lit ensuite 01 → 00 → 10. Dans quel sens tourne le bouton ?")
    ANS("Sens antihoraire : c'est la suite horaire 10 → 00 → 01 lue à l'envers.", 1)
    Q("d)", "Le volume vaut 0001 0100b. On tourne le bouton de 3 crans dans le sens horaire. Calcule le nouveau volume en binaire et en décimal.")
    ANS("0001 0100b + 0000 0011b = 0001 0111b. Contrôle : 20d + 3d = 23d = 16 + 4 + 2 + 1 ✓", 1)
    Q("e)", "Pourquoi n'utilise-t-on pas le binaire naturel 00 → 01 → 10 → 11 pour ce bouton ?")
    ANS("De 01 à 10, les deux contacts changent en même temps. Comme ils ne basculent jamais exactement au même instant, le microcontrôleur lirait brièvement 00 ou 11 et croirait que le bouton a tourné dans l'autre sens ou a sauté un cran. En Gray, un seul contact change à la fois : aucune lecture fausse.", 2)

    # ---- N°7 Compléments
    HR(); EX(8, "Complément à 1 et complément à 2 (8 bits)", "Méthode : diapositives 16 et 17 · Floyd §2-5 p. 63-65, problèmes 21 et 22")
    P("Contexte : l'unité de calcul obtient le C1 avec des inverseurs et le C2 en ajoutant 1 avec son additionneur ; c'est ainsi qu'elle prépare chaque soustraction et chaque nombre négatif.", italic=True, size=10, keep=True)
    cv = [0b00010110, 0b00111101, 0b10110000, 0b00000001, 0b00000000]
    TABLE([3.3, 3.6, 3.6, TW - 10.5 - 0.02], [["Nombre", "Complément à 1", "Complément à 2", "Contrôle : nombre + C2"]] +
          [[_sp(b(v, 8)) + "b", ("R", _sp(b(v ^ 0xFF, 8)) + "b"), ("R", _sp(b(c2(v), 8)) + "b"),
            ("R", (_sp(b(v + c2(v), 9)) if v + c2(v) > 255 else _sp(b(v + c2(v), 8))) + " → 0000 0000 ✓")] for v in cv],
          height=0.6, size=10, mono_cols=(0, 1, 2))
    Q("a)", "Que remarques-tu pour la dernière ligne (0000 0000b) ?")
    ANS("C1 = 1111 1111b ; C1 + 1 = 1 0000 0000b → sur 8 bits, la retenue est rejetée : C2 = 0000 0000b. Le zéro n'a qu'une seule écriture en C2 (alors qu'en C1 il en a deux : 0000 0000 et 1111 1111).", 2)
    BOX(["Si difficulté",
         "Toujours écrire d'abord les 8 bits complets (avec les 0 de gauche), sinon le complément est faux. Pour vérifier un C2 sans refaire le calcul : méthode rapide (recopier jusqu'au premier 1 depuis la droite, inverser le reste), ou addition nombre + C2 qui doit donner 0 sur 8 bits."])

    # ---- N°8 Nombres signés
    HR(); EX(9, "Nombres signés en complément à 2 (8 bits)", "Méthode : diapositive 18 · Floyd §2-6 p. 66-68, problèmes 25 et 28")
    Q("a)", "Écris chaque nombre décimal en binaire signé (complément à 2) sur 8 bits.")
    sv = [12, -12, -68, 101, -125, -1]
    TABLE([2.6, 4.0, TW - 6.6 - 0.02], [["Décimal", "Complément à 2 (8 bits)", "Démarche"]] +
          [[f"{v:+d}d".replace("-", "−"), ("R", _sp(b(v % 256, 8)) + "b"),
            ("R", "positif : binaire direct" if v >= 0 else f"{-v}d = {_sp(b(-v, 8))}b → C1 {_sp(b((-v) ^ 0xFF, 8))}b → + 1")] for v in sv],
          height=0.55, size=10, mono_cols=(1,))
    Q("b)", "Donne la valeur décimale de chaque nombre signé (MSB = −128).")
    dv = [0b10011001, 0b01110100, 0b11111111, 0b10000000]
    def sval(v): return v - 256 if v & 0x80 else v
    def dem(v):
        parts = [("−128" if i == 0 else str(2 ** (7 - i))) for i, c in enumerate(b(v, 8)) if c == "1"]
        return " + ".join(parts).replace("+ −", "− ")
    TABLE([3.6, 2.6, TW - 6.2 - 0.02], [["Binaire signé", "Décimal", "Somme des poids"]] +
          [[_sp(b(v, 8)) + "b", ("R", f"{sval(v):+d}d".replace("-", "−")), ("R", dem(v) + f" = {sval(v)}".replace("-", "−"))] for v in dv],
          height=0.55, size=10, mono_cols=(0,))
    Q("c)", "Quelle est l'étendue des nombres signés sur 8 bits ? Pourquoi peut-on écrire −128d mais pas +128d ?")
    ANS("De −128d (1000 0000b) à +127d (0111 1111b) : 256 valeurs. Avec le bit de signe à 0, il ne reste que 7 bits de grandeur, donc +127d au maximum ; le zéro occupe une des 128 combinaisons « positives ».", 2)
    Q("d)", "Le capteur de température numérique d'une serre envoie ses mesures en complément à 2 sur 8 bits (1 bit = 1 °C). Quelle température correspond à chaque mesure ?")
    tv = [0b00011001, 0b11110110, 0b11100010]
    TABLE([3.6, 3.0, TW - 6.6 - 0.02], [["Mesure reçue", "Température", "Somme des poids"]] +
          [[_sp(b(v, 8)) + "b", ("R", f"{sval(v):+d} °C".replace("-", "−")), ("R", dem(v) + f" = {sval(v)}".replace("-", "−"))] for v in tv],
          height=0.55, size=10, mono_cols=(0,))

    # ---- N°9 Soustraction
    HR(); EX(10, "Soustraire en additionnant le complément à 2", "Méthode : diapositive 18 · Floyd §2-7 p. 72-73, problème 34")
    P("Contexte : un processeur n'a pas de soustracteur : il additionne le C2. C'est ainsi qu'il calcule un écart de mesure, par exemple la différence entre deux températures (question d).", italic=True, size=10, keep=True)
    P("Pour chaque soustraction : prends le C2 du nombre à soustraire, additionne, rejette la retenue finale, puis contrôle en décimal.", keep=True)
    subs = [("a)", 51, 16), ("b)", 20, 33), ("c)", 101, -24), ("d)", 25, -10)]
    for lbl, x, y in subs:
        if lbl == "d)":
            Q(lbl, "Dans la serre, il fait +25 °C à midi et −10 °C la nuit (mesures de la N°9 d). Calcule l'écart en binaire : 0001 1001b − 1111 0110b.")
        else:
            Q(lbl, f"{_sp(b(x % 256, 8))}b − {_sp(b(y % 256, 8))}b   ({x:+d}d − ({y:+d}d))".replace("-", "−"))
        neg = (-y) % 256; s_ = x % 256 + neg; res = (x - y)
        txt_ = (f"C2 du diminuteur : {_sp(b(y % 256, 8))}b → {_sp(b(neg, 8))}b ({-y:+d}d)\n"
                f"{_sp(b(x % 256, 8))}b + {_sp(b(neg, 8))}b = {_sp(b(s_, 9)) if s_ > 255 else _sp(b(s_, 8))}b"
                + (f" → retenue rejetée → {_sp(b(s_ % 256, 8))}b" if s_ > 255 else " (pas de retenue finale)")
                + f" = {res:+d}d ✓")
        ANS(txt_.replace("(-", "(−").replace("= -", "= −"), 2)
    BOX(["Si difficulté – 2e son de cloche",
         "Analogie du compteur kilométrique à 3 chiffres : reculer de 1 depuis 000 affiche 999. En C2 sur 8 bits, reculer de 1 depuis 0000 0000 donne 1111 1111 = −1. Soustraire, c'est « faire le tour » du compteur : c'est pour cela que la retenue finale se jette."])

    # ---- N°10 Mélange
    HR(); EX(11, "Exercice mélangé (révision une semaine plus tard, sans la fiche)", "Toutes les méthodes")
    Q("a)", "Calcule 0101b + 0011b, puis convertis le résultat en code Gray.")
    ANS("0101b + 0011b = 1000b (5d + 3d = 8d) → 1100 Gray.", 1)
    Q("b)", "Multiplie 0000 0011b par 4 par décalage, puis écris l'opposé du résultat en complément à 2 (8 bits).")
    ANS("0000 0011b × 4 = 0000 1100b = 12d → −12d = 1111 0100b.", 1)
    Q("c)", "Un codeur lit 0110 Gray. Quelle est la position en décimal ? Double cette valeur par décalage et donne le résultat en binaire.")
    ANS("0110 Gray → 0100b = 4d → × 2 : 1000b = 8d.", 1)
    Q("d)", "Vrai ou faux ? Justifie. « Sur 8 bits, le complément à 2 de 1000 0000b est 1000 0000b. »")
    ANS("Vrai : C1 = 0111 1111b, + 1 = 1000 0000b. −128d n'a pas d'opposé positif sur 8 bits (+128d dépasse +127d).", 2)
    Q("e)", "Auto-évaluation : pour chaque thème, note ✓ (je sais seul·e), ~ (avec la fiche) ou ✗ (à revoir).")
    TABLE([TW / 4 - 0.01] * 4, [["Addition", "× 2 et multiplication", "Code Gray", "Compléments à 1 et 2"], ["", "", "", ""]],
          height=0.8, size=10, first_left=False)

    sec2 = d.sections[0]
    for part in (d.element, sec2.header._element, sec2.footer._element): reorder(part)
    z = d.settings.element.find(qn("w:zoom"))
    if z is not None: z.set(qn("w:percent"), "100")
    d.save(out); print("ok", out)


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    build(False, "out/EX Arithmétique binaire, code Gray et compléments.docx")
    build(True, "out/EX C Arithmétique binaire, code Gray et compléments.docx")
