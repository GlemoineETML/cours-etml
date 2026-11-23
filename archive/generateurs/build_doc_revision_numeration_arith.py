# -*- coding: utf-8 -*-
"""Fiche de révision individuelle (1 h 30) + corrigé : systèmes de numération, arithmétique binaire, code Gray et compléments.
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
BASE = "../etml_base.docx"   # = Rapport_Simple.dotx avec content-type template.main → document.main (voir prep_modele.py)
MODULE = "Test et Mesure 1 – LFB_Pr_Basis"
MATIERE = "Test et Mesure 1 – LFB_Pr_Basis"
CLASSE = "XLO1"
ANNEE = "2026-2027"
CHAMP = "LZ_2325, LZ_2326, LZ_4258, LZ_2229"
FLOYD = "https://eduvaud.sharepoint.com/:b:/r/sites/msteams_76c9d9/Documents%20partages/Documentation/Electronique%20num%C3%A9rique%20TMLO/10%20Floyd%20V11/10%20Floyd%20V11%20Basse%20d%C3%A9finition%20par%20chapitre/Chap%2002%20-%20Syst%C3%A8mes%20de%20num%C3%A9ration,%20op%C3%A9rations%20et%20codes.pdf?d=w933f2237d1814185b6a6b02be82abe0b&csf=1&web=1&e=eHqofE"   # Floyd chap. 2 sur Teams (SharePoint)
PPT = "https://eduvaud.sharepoint.com/:p:/r/sites/msteams_76c9d9/Documents%20partages/Enseignement%20professionnel/ChampsDApprentissage/El_DT1/Arithm%C3%A9tique%20binaire%20code%20Gray%20et%20compl%C3%A9ments.pptx?d=w94d1aa2ee1504c64802bdedccd556863&csf=1&web=1&e=fkAmuh"   # présentation sur Teams
FLOYD_OFFSET = 50   # page imprimée du Floyd − 50 = page du PDF du chapitre 2
TW = 21.0 - 2.0 - 1.5           # largeur utile en cm
TITLE = "Révision : systèmes de numération et arithmétique binaire"
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
        if t.text == "Nom -": t.text = f"Révision numération et arithmétique – {kind} – LFB_Pr_Basis"
        elif t.text in (" ", "Type - Numéro"): t.text = ""
    for r in sec.header._element.iter(qn("w:r")):
        if r.find(qn("w:t")) is not None and (r.find(qn("w:t")).text or "").strip():
            rPr = r.find(qn("w:rPr"))
            if rPr is None: rPr = OxmlElement("w:rPr"); r.insert(0, rPr)
            c = OxmlElement("w:color"); c.set(qn("w:val"), HEX_NAVY); rPr.append(c)
    # valeurs affichées des champs du pied de page (Word les met à jour à l'ouverture / impression)
    vals = {"AUTHOR": "Gaël Lemoine", "LASTSAVEDBY": "Gaël Lemoine", "SAVEDATE": now.strftime("%m/%d/%Y %H:%M"),
            "CREATEDATE": now.strftime("%m/%d/%Y"), "PRINTDATE": now.strftime("%m/%d/%Y %H:%M"),
            "FILENAME": os.path.basename(out), "TITLE": title_doc}
    for it_ in sec.footer._element.iter(qn("w:instrText")):
        it_.text = it_.text.replace("dd/MM/yyyy", "MM/dd/yyyy")   # dates à l'américaine
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
        f.line_spacing = 1.15 if (kw.get("size") and kw["size"] <= 10) else 1.25   # fiche d'exercices : interligne resserré
        rich(p, txt, **kw); return p

    def EX(n, title, ref=None):
        p = d.add_paragraph(); f = p.paragraph_format
        f.space_before = Pt(8); f.space_after = Pt(2); f.keep_with_next = True
        r = p.add_run(f"N°{n} {title}"); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = NAVY
        if ref:
            # segments séparés par « · » : « Floyd … p. NN » → lien vers la page NN du PDF ; « Présentation … » → lien PowerPoint
            q = P("", italic=True, size=9, color=GREY, keep=True, after=3)
            for k, seg in enumerate(ref.split(" · ")):
                if k: rich(q, " · ", italic=True, size=9, color=GREY)
                if seg.startswith("Floyd"):
                    m = re.search(r"p\. (\d+)", seg)
                    url = FLOYD + (f"#page={int(m.group(1)) - FLOYD_OFFSET}" if m else "")
                    hyperlink(q, url, seg, size=9)
                elif seg.startswith("Présentation"):
                    hyperlink(q, PPT, seg, size=9)
                else:
                    rich(q, seg, italic=True, size=9, color=GREY)

    def HR():
        p = d.add_paragraph(); p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
        p_border(p, ["bottom"], 4)

    def Q(lbl, txt):
        p = d.add_paragraph(); f = p.paragraph_format
        f.left_indent = Cm(0.7); f.first_line_indent = Cm(-0.7); f.space_before = Pt(3); f.space_after = Pt(2)
        f.tab_stops.add_tab_stop(Cm(0.7)); f.keep_with_next = True; f.line_spacing = 1.25
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

    def TABLE(widths, rows, header=True, height=0.6, size=10, first_left=True, mono_cols=(), keep_after=False):
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
            if i < len(t.rows) - 1 or keep_after:
                for c in tr.cells:
                    for pp in c.paragraphs: pp.paragraph_format.keep_with_next = True
        spc = d.add_paragraph(); spc.paragraph_format.space_after = Pt(2); spc.paragraph_format.line_spacing = 1.0; spc.paragraph_format.keep_with_next = keep_after
        return t

    def ADD(a, bb, n, label="Poids", la="A", lb="+ B", da=None, db=None, ds=None, keep_carry=True, hide_a=False, hide_b=False, keep_after=False):
        """Addition en colonnes avec retenues ; da/db/ds = textes de la colonne de contrôle."""
        W = [2 ** i for i in range(n, -1, -1)]
        carry = [""] * (n + 1); c = 0
        for i in range(n):
            s_ = ((a >> i) & 1) + ((bb >> i) & 1) + c; c = s_ >> 1
            if c: carry[n - i - 1] = "1"
        s = b(a + bb, n + 1)
        cw = 1.15
        widths = [2.6] + [cw] * (n + 1) + [TW - 2.6 - cw * (n + 1) - 0.02]
        rows = [[label] + [str(w) for w in W] + ["Contrôle"],
                ["Retenues"] + [("R", x) for x in carry] + [""],
                [la] + [""] + [("R", x) if hide_a else x for x in b(a, n)] + [("R", da or f"{a}d") if hide_a else (da or f"{a}d")],
                [lb] + [""] + [("R", x) if hide_b else x for x in b(bb, n)] + [db or f"{bb}d"],
                ["= Somme"] + [("R", x) for x in s] + [("R", ds or f"{a + bb}d")]]
        TABLE(widths, rows, height=0.55, size=11, mono_cols=tuple(range(1, n + 2)), keep_after=keep_after)

    # ---------------- équations Word natives (OMML)
    from docx.oxml import parse_xml
    from mathml import omath
    NSD = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

    def EQ(p, src, color=None, sz=None):
        p._p.append(parse_xml(omath(src, color, sz).replace("<m:oMath>", f"<m:oMath {NSD}>", 1)))

    def MIX(p, txt, color=None, size=None):
        """Texte avec segments $...$ rendus en équations natives."""
        for k, seg in enumerate(txt.split("$")):
            if not seg: continue
            if k % 2: EQ(p, seg, "EE0000" if color == RED else None, int(size * 2) if size else None)
            else: rich(p, seg, color=color, size=size)

    def ANS(txt, lines=1, keep=False):
        if corr:
            parts = txt.split("\n")
            for i, t in enumerate(parts):
                p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7)
                p.paragraph_format.space_after = Pt(1 if i < len(parts) - 1 else 4)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT; p.paragraph_format.line_spacing = 1.25; p.paragraph_format.keep_with_next = keep
                MIX(p, t, color=RED)
        else:
            for _ in range(lines):
                p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7); p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.tab_stops.add_tab_stop(Cm(TW), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
                p.paragraph_format.keep_with_next = keep; p.add_run("\t")

    def CTX(txt):
        P("Contexte : " + txt, italic=True, size=10, keep=True, color=GREY)

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
            rows.append([f"Ligne {k + 1} (poids {2 ** k})", *[("R", dd) for dd in row(x if bit else 0, k, nx)],
                         ("R", f"bit = {bit} → {'copie' if bit else 'ligne de 0'}" + (f", décalée de {k} rang{'s' if k > 1 else ''}" if k else ""))])
        rows.append(["Retenues", *[("R", dd) for dd in carry], ""])
        rows.append(["= Produit", *[("R", dd) for dd in b(x * y, nb)], ("R", f"= {x * y}d ({x}d × {y}d)")])
        TABLE(widths, rows, height=0.6, size=10, mono_cols=tuple(range(1, nb + 1)))

    S = _sp
    def B8(v): return S(b(v, 8)) + "b"
    def bcd(v): return " ".join(format(int(ch), "04b") for ch in str(v)) + " BCD"
    def sval(v): return v - 256 if v & 0x80 else v

    # ================= TITRE
    d.add_paragraph(TITLE, style="Title")
    P(f"Fiche de révision individuelle · {MATIERE} · Classe {CLASSE} · {ANNEE} · Champs d'apprentissage {CHAMP}", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, after=8)
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.paragraph_format.space_after = Pt(0)
    r = p.add_run("Corrigé" if corr else "Version apprenti·e"); r.bold = True
    if corr: r.font.color.rgb = RED
    p.add_run("\tNom :")
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.add_run("\tDate :")
    p_border(p, ["bottom"], 4)

    if corr:
        BOX(["Déroulement (enseignant·e) : 1 h 30, travail individuel",
             "Conditions du test : pas de calculatrice, pas d'aide-mémoire. Temps indicatifs : partie A 40 min (N°1 à N°5), partie B 20 min (N°6 et N°7), partie C 10 min (N°8), partie D 20 min (N°9 et N°10).",
             "Toutes les valeurs sont nouvelles par rapport aux deux fiches d'origine (« Systèmes de numération – exercices en groupe » et « Arithmétique binaire, code Gray et compléments »). Les lettres A à J renvoient aux méthodes de la fiche-mémo de numération (chapitre 1.3, p. 2 et 3), rappelées dans les ressources et à chaque question.",
             "Correction : faire corriger avec ce document en fin de séance, puis compléter le tableau d'auto-évaluation. Un thème noté ✗ = reprendre la fiche d'origine correspondante avant vendredi."])

    P("**Consignes :** travail individuel, 1 h 30 au maximum, sans calculatrice ni aide-mémoire, comme au test. Écris toujours le raisonnement, puis contrôle ton résultat. Suffixe à la fin du nombre : **b** binaire, **d** décimal, **h** hexadécimal, **BCD**, **Gray**. Les nombres de 8 bits s'écrivent par groupes de 4 bits (0110 1101b).", after=4)
    P("**Barème indicatif :** 60 points, indiqués à côté de chaque exercice. Suis les temps conseillés pour finir dans l'heure et demie.", after=4)
    P("**Ressources pour réviser :** ", after=1, keep=True)
    pr_ = P("Floyd, Systèmes numériques : ", after=1, size=10)
    hyperlink(pr_, FLOYD, "chapitre 2 (PDF), Systèmes de numération, opérations et codes", size=10)
    rich(pr_, " : 2-2 et 2-3 Binaire (p. 53-59) · 2-4 Arithmétique (p. 60-63) · 2-5 à 2-7 Compléments et nombres signés (p. 63-73) · 2-8 Hexadécimal (p. 78-83) · 2-10 BCD (p. 86-89) · 2-11 Code Gray (p. 90-92).", size=10)
    pr_ = P("Présentation du cours : ", after=1, size=10)
    hyperlink(pr_, PPT, "Arithmétique binaire, code Gray et compléments (PowerPoint)", size=10)
    rich(pr_, " : addition (diapositives 4 à 6), × 2 et multiplication (7 à 10), code Gray (11 à 15), compléments à 1 et à 2 et nombres négatifs (16 à 18), pièges classiques (19).", size=10)
    P("Méthodes A à J : fiche « Systèmes de numération – exercices en groupe » (distribuée en classe), fiche-mémo, chapitre 1.3 « Les passages de conversion », p. 2 et 3. A binaire → décimal · B décimal → binaire · C nombre de bits minimum · D décimal → BCD · E BCD → décimal · F binaire → BCD · G BCD → binaire · H décimal → hexadécimal · I contrôle hexadécimal → décimal · J hexadécimal ↔ binaire.", after=1, size=10)
    pr_ = P("Nextec Media : ", after=1, size=10); hyperlink(pr_, NEXTEC_TOPIC, "chapitre 5.1, Systèmes de numération et codes", size=10)
    pr_ = P("Nextec Media : ", after=6, size=10); hyperlink(pr_, NEXTEC_GRAY, "exercice complémentaire sur le code Gray", size=10)

    # ================= PARTIE A
    d.add_heading("Partie A : systèmes de numération (≈ 40 min)", level=1)

    # ---- N°1
    EX(1, "Horodatage d'un enregistreur de données (7 points · ≈ 10 min)", "Méthodes C, B et A : fiche-mémo numération, 1.3 p. 2 · Floyd 2-2 et 2-3 p. 53-59")
    CTX("un enregistreur de données de serre note chaque mesure avec sa date et son heure. Pour économiser la mémoire, chaque valeur est rangée dans le plus petit nombre de bits possible.")
    P("Mesure du 19 novembre à 17 h 42 : jour 19d, mois 11d, heure 17d, minutes 42d.", keep=not corr)
    Q("a)", "Complète le tableau (méthode C : nombre de bits minimum).")
    TABLE([5.2, 3.1, 3.1, 3.1, TW - 5.2 - 9.3 - 0.02], [
        ["", "Jour", "Mois", "Heure", "Minutes"],
        ["Valeur", "19d", "11d", "17d", "42d"],
        ["Nb de bits pour cette valeur", ("R", "5 bits"), ("R", "4 bits"), ("R", "5 bits"), ("R", "6 bits")],
        ["Plus grande valeur possible", ("R", "31d"), ("R", "12d"), ("R", "23d"), ("R", "59d")],
        ["Nb de bits pour toutes les valeurs", ("R", "5 bits"), ("R", "4 bits"), ("R", "5 bits"), ("R", "6 bits")],
    ], height=0.6, size=10)
    if corr:
        p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7); p.paragraph_format.space_after = Pt(4)
        MIX(p, "Contrôle pour les minutes : $2^{5} = 32 \\le 59 < 2^{6} = 64$ → 6 bits. Total : 5 + 4 + 5 + 6 = 20 bits au lieu de 4 bytes = 32 bits.", color=RED)
    Q("b)", "Convertis chaque valeur en binaire sur 8 bits (méthode B : décimal → binaire).")
    rows = [["Valeur", "128", "64", "32", "16", "8", "4", "2", "1"]]
    for lab, v in (("Jour 19d", 19), ("Mois 11d", 11), ("Heure 17d", 17), ("Minutes 42d", 42)):
        rows.append([lab] + [("R", ch) for ch in b(v, 8)])
    TABLE([3.4] + [(TW - 3.42) / 8] * 8, rows, height=0.55, size=11, mono_cols=tuple(range(1, 9)))
    Q("c)", "L'enregistreur affiche une autre mesure sous forme de 4 bytes. Décode-la (méthode A : binaire → décimal) et écris la date et l'heure.")
    rows = [["Byte reçu", "Calcul (poids des 1)", "Décimal"]]
    for lab, v in (("Jour", 28), ("Mois", 6), ("Heure", 9), ("Minutes", 59)):
        w = [str(2 ** (7 - i)) for i, ch in enumerate(b(v, 8)) if ch == "1"]
        rows.append([f"{lab} : {B8(v)}", ("R", " + ".join(w)), ("R", f"{v}d")])
    TABLE([5.4, TW - 5.4 - 3.0 - 0.02, 3.0], rows, height=0.55, size=10.5)
    ANS("Mesure du 28 juin à 9 h 59 (28.06, 09:59).", 1)
    BOX(["Si difficulté",
         "Nombre de bits : cherche la première puissance de 2 strictement plus grande que la valeur (19d < 32 = 2⁵ → 5 bits). Attention, 32d demande déjà 6 bits. Pour coder, utilise la méthode du porte-monnaie : les pièces 128, 64, 32, 16, 8, 4, 2, 1, chacune au plus une fois."])

    # ---- N°2
    HR(); EX(2, "Le BCD d'un multimètre (6 points · ≈ 8 min)", "Méthodes D et E : fiche-mémo numération, 1.3 p. 2 · Floyd 2-10 p. 86-89")
    CTX("l'afficheur d'un multimètre a 4 chiffres. Chaque chiffre reçoit son propre quartet BCD, qui commande un afficheur 7 segments.")
    Q("a)", "Le multimètre mesure 1,947 V. Code les 4 chiffres affichés en BCD (méthode D : décimal → BCD).")
    TABLE([4.2] + [(TW - 4.22) / 4] * 4, [
        ["Chiffre affiché", "1", "9", "4", "7"],
        ["Code BCD (4 bits)", ("R", "0001"), ("R", "1001"), ("R", "0100"), ("R", "0111")]], height=0.55, size=11, mono_cols=(1, 2, 3, 4))
    Q("b)", "Quelle valeur l'afficheur montre-t-il (méthode E : BCD → décimal) ?")
    TABLE([8.0, TW - 8.02], [
        ["Code BCD reçu", "Valeur affichée"],
        ["0011 0110 0000 1000 BCD", ("R", "3608")],
        ["1001 0010 0101 0001 BCD", ("R", "9251")],
        ["0100 1011 0010 0111 BCD", ("R", "impossible : 1011 = 11d n'existe pas en BCD")]], height=0.55, size=10.5, mono_cols=(0,))
    Q("c)", "Code l'année 2027d en BCD, puis en binaire. Combien de bits faut-il dans chaque cas ?")
    ANS(f"BCD : {bcd(2027)} (16 bits). Binaire : 2027d = 1024 + 512 + 256 + 128 + 64 + 32 + 8 + 2 + 1 = {S(format(2027, 'b'))}b (11 bits). Le binaire est plus compact, le BCD plus simple à afficher.", 2)

    # ---- N°3
    HR(); EX(3, "Binaire, BCD et hexadécimal (7 points · ≈ 8 min)", "Méthodes F, G et J : fiche-mémo numération, 1.3 p. 3 · Floyd 2-8 p. 78-83 et 2-10 p. 86-89")
    CTX("un microcontrôleur calcule en binaire, l'afficheur attend du BCD et le programmeur lit les registres en hexadécimal : le technicien doit passer de l'un à l'autre.")
    Q("a)", "Binaire → BCD : passe toujours par le décimal (méthode F : binaire → décimal → BCD).")
    rows = [["Binaire", "Décimal", "BCD", "Nb de bits BCD"]]
    for v in (58, 99, 200, 231):
        rows.append([B8(v), ("R", f"{v}d"), ("R", bcd(v)), ("R", str(4 * len(str(v))))])
    TABLE([4.0, 3.0, TW - 4.0 - 3.0 - 3.4 - 0.02, 3.4], rows, height=0.55, size=10.5, mono_cols=(0, 2))
    Q("b)", "BCD → binaire, puis hexadécimal (méthode G : BCD → décimal → binaire, puis méthode J : 4 bits = 1 chiffre hexa).")
    rows = [["BCD", "Décimal", "Binaire (8 bits)", "Hexa"]]
    for v in (57, 84, 190):
        rows.append([bcd(v), ("R", f"{v}d"), ("R", B8(v)), ("R", f"{v:X}h")])
    TABLE([5.2, 3.0, TW - 5.2 - 3.0 - 2.8 - 0.02, 2.8], rows, height=0.55, size=10.5, mono_cols=(0, 2))
    Q("c)", "Un collègue lit l'octet 0100 0111 comme du BCD et trouve 47. Quelle valeur aurait-il trouvée si l'octet était du binaire ? Pourquoi les deux résultats sont-ils différents ?")
    ANS("En binaire : 0100 0111b = 64 + 4 + 2 + 1 = 71d. En BCD, chaque quartet est un chiffre (4 et 7) ; en binaire, chaque bit a un poids. On ne peut donc jamais recopier les bits d'un code à l'autre.", 2)

    # ---- N°4
    HR(); EX(4, "Les couleurs d'une LED RGB (5 points · ≈ 6 min)", "Méthodes H, I et J : fiche-mémo numération, 1.3 p. 3 · Floyd 2-8 p. 78-83")
    CTX("une LED RGB, un écran ou une page web reçoivent leur couleur sous forme de 3 bytes : rouge, vert, bleu, de 0d à 255d chacun. On les note en hexadécimal, par exemple #2E8B57.")
    Q("a)", "Code la couleur rouge 46d, vert 139d, bleu 87d en hexadécimal, via le binaire (méthode H : décimal → hexadécimal), puis contrôle (méthode I : chiffre fort × 16 + chiffre faible).")
    rows = [["Canal", "Décimal", "Binaire (8 bits)", "Hexa", "Contrôle"]]
    for lab, v in (("Rouge", 46), ("Vert", 139), ("Bleu", 87)):
        rows.append([lab, f"{v}d", ("R", B8(v)), ("R", f"{v:02X}h"), ("R", f"{v >> 4}·16 + {v & 15} = {v}d")])
    TABLE([2.2, 2.2, 4.6, 2.2, TW - 11.2 - 0.02], rows, height=0.55, size=10.5, mono_cols=(2,))
    ANS("Code couleur : #2E8B57.", 1)
    Q("b)", "Le bleu marine de l'ETML a le code #242852. Retrouve les trois valeurs en décimal (méthode J : hexa → binaire, puis méthode A : binaire → décimal ; ou directement la méthode I).")
    rows = [["Canal", "Hexa", "Binaire (8 bits)", "Décimal"]]
    for lab, v in (("Rouge", 0x24), ("Vert", 0x28), ("Bleu", 0x52)):
        rows.append([lab, f"{v:02X}h", ("R", B8(v)), ("R", f"{v}d")])
    TABLE([3.0, 3.0, TW - 3.0 - 3.0 - 3.6 - 0.02, 3.6], rows, height=0.55, size=10.5, mono_cols=(2,))

    # ---- N°5
    HR(); EX(5, "Le compteur de bouteilles qui déborde (6 points · ≈ 8 min)", "Présentation diapositives 4 à 6 · Floyd 2-4 p. 60-61")
    CTX("sur une ligne d'embouteillage, un compteur 8 bits compte les bouteilles remplies. Il affiche 213d quand une palette de 60 bouteilles passe encore devant le capteur.")
    Q("a)", "Combien d'états différents ce compteur peut-il prendre ? Quelle est sa valeur maximale, en décimal et en binaire ?")
    ANS("$2^{8} = 256$ états, de 0d à 255d. Valeur maximale : 255d = 1111 1111b.", 1)
    Q("b)", "Après combien de bouteilles atteint-il 255d ? Que se passe-t-il à la bouteille suivante ?")
    ANS("255d − 213d = 42 bouteilles. À la 43e, il repasse à 0d : c'est le débordement (overflow).", 1)
    Q("c)", "Pose l'addition 213d + 60d en binaire (8 bits) avec les retenues. Qu'affiche le compteur après les 60 bouteilles ?")
    ADD(213, 60, 8, keep_after=True)
    ANS("273d ne tient pas sur 8 bits : le 9e bit (poids 256) est perdu. Le compteur affiche 0001 0001b = 17d. Contrôle : 273d − 256d = 17d, ou 60 − 43 = 17 bouteilles après le passage à 0.", 2)
    BOX(["Si difficulté",
         "Pense au compteur kilométrique d'un vieux scooter à 3 chiffres : à 999 km, encore 1 km, et il affiche 000. Un compteur 8 bits fait pareil à 255."])

    # ================= PARTIE B
    d.add_heading("Partie B : arithmétique binaire (≈ 20 min)", level=1)

    # ---- N°6
    EX(6, "Additions avec retenues (5 points · ≈ 8 min)", "Présentation diapositives 4 à 6 · Floyd 2-4 p. 60-61")
    CTX("une station de pompage additionne les litres mesurés par deux débitmètres pour connaître le volume total pompé.")
    Q("a)", f"{B8(108)} + {B8(75)}")
    ADD(108, 75, 8)
    Q("b)", f"{B8(57)} + {B8(29)}")
    ADD(57, 29, 8)

    # ---- N°7
    HR(); EX(7, "Décalages et multiplication (7 points · ≈ 12 min)", "Présentation diapositives 7 à 10 · Floyd 2-4 p. 62")
    CTX("un microcontrôleur sans multiplieur matériel multiplie par décalages et additions. C'est ce qu'il fait pour convertir une mesure en millivolts.")
    Q("a)", "Le registre contient 0001 1011b. Multiplie-le par 2, 4, 8 et 16 en décalant vers la gauche.")
    rows = [["Opération", "Résultat en binaire", "Décimal"]]
    for k in range(5):
        v = 27 << k
        res = (S(b(v, 9)) + "b (ne tient plus sur 8 bits)") if v > 255 else B8(v)
        rows.append([f"× {2 ** k}" + (" (départ)" if k == 0 else f" ({k} décalage{'s' if k > 1 else ''})"),
                     B8(v) if k == 0 else ("R", res), f"{v}d" if k == 0 else ("R", f"{v}d" + (" > 255d" if v > 255 else ""))])
    TABLE([4.4, TW - 4.4 - 4.0 - 0.02, 4.0], rows, height=0.55, size=10.5, mono_cols=(1,))
    Q("b)", "Pose la multiplication 1101b × 110b par produits partiels.")
    MULT(13, 6)
    Q("c)", "Un capteur envoie la valeur 0001 0011b. Un pas vaut 10 mV. Calcule la tension avec des décalages et une addition (10d = 8d + 2d).")
    ANS("0001 0011b = 19d. × 8 : 3 décalages → 1001 1000b = 152d. × 2 : 1 décalage → 0010 0110b = 38d.", 1, keep=True)
    ADD(152, 38, 8, la="19d × 8", lb="+ 19d × 2", da="152d", db="38d", ds="190d → 190 mV", hide_a=True, hide_b=True)

    # ================= PARTIE C
    d.add_heading("Partie C : code Gray (≈ 10 min)", level=1)
    EX(8, "La girouette d'une éolienne (6 points · ≈ 10 min)", "Présentation diapositives 11 à 15 · Floyd 2-11 p. 90-92")
    CTX("une éolienne s'oriente face au vent grâce à une girouette équipée d'un codeur absolu 4 bits en code Gray : 16 positions, de 0 à 15.")
    Q("a)", "Binaire → Gray.")
    rows = [["Binaire", "Décimal", "Gray"]]
    for v in (6, 11, 9):
        rows.append([S(b(v, 4)) + "b", ("R", f"{v}d"), ("R", b(gray(v), 4) + " Gray")])
    TABLE([5.0, 4.0, TW - 9.02], rows, height=0.55, size=11, mono_cols=(0, 2))
    Q("b)", "Gray → binaire.")
    rows = [["Gray", "Binaire", "Décimal"]]
    for g in (0b0111, 0b1100, 0b1010):
        v = gray2bin(g)
        rows.append([b(g, 4) + " Gray", ("R", b(v, 4) + "b"), ("R", f"{v}d")])
    TABLE([5.0, 4.0, TW - 9.02], rows, height=0.55, size=11, mono_cols=(0, 1))
    Q("c)", "Les 16 positions se partagent le tour complet. La girouette envoie 1010 Gray. Dans quelle direction pointe-t-elle (0° = nord, sens horaire) ?")
    ANS("Un pas vaut $\\f{360°}{16} = 22,5°$. 1010 Gray = 1100b = 12d, donc $12 \\cdot 22,5° = 270°$ : la girouette pointe vers l'ouest.", 2)
    Q("d)", "Entre les positions 7 et 8, combien de bits changent en binaire ? Et en code Gray ? Pourquoi le code Gray est-il plus sûr pour un codeur ?")
    ANS(f"Binaire : 0111b → 1000b, les 4 bits changent. Gray : {b(gray(7), 4)} → {b(gray(8), 4)} Gray, un seul bit change. Les contacts ne basculent jamais tous exactement en même temps : en binaire, le codeur pourrait lire une position fausse pendant la transition (par exemple 1111b = 15d). En Gray, la lecture est soit l'ancienne position, soit la nouvelle.", 3)

    # ================= PARTIE D
    d.add_heading("Partie D : compléments et nombres signés (≈ 20 min)", level=1)
    EX(9, "Compléments à 1 et à 2 (5 points · ≈ 8 min)", "Présentation diapositives 16 à 18 · Floyd 2-5 et 2-6 p. 63-68")
    CTX("un capteur de congélateur envoie la température en complément à 2 sur 8 bits, de −128 °C à +127 °C.")
    Q("a)", "Complète le tableau (8 bits).")
    rows = [["Nombre", "Binaire", "Complément à 1", "Complément à 2", "Valeur du C2"]]
    for v in (37, 100, 1):
        rows.append([f"+{v}d", B8(v), ("R", B8(v ^ 0xFF)), ("R", B8(c2(v))), ("R", f"−{v}d")])
    TABLE([2.4, 3.9, 3.9, 3.9, TW - 14.1 - 0.02], rows, height=0.55, size=10.5, mono_cols=(1, 2, 3))
    Q("b)", "Le capteur envoie les valeurs suivantes. Quelle température affiche le congélateur ?")
    rows = [["Valeur reçue", "Calcul (MSB = −128)", "Température"]]
    for v in (0xEC, 0x56, 0x81):
        w = [("−128" if i == 0 else str(2 ** (7 - i))) for i, ch in enumerate(b(v, 8)) if ch == "1"]
        rows.append([B8(v), ("R", " + ".join(w)), ("R", f"{sval(v):+d} °C".replace("-", "−"))])
    TABLE([4.0, TW - 4.0 - 3.6 - 0.02, 3.6], rows, height=0.55, size=10.5, mono_cols=(0,))
    BOX(["Si difficulté",
         "Contrôle d'un C2 : le nombre + son C2 doit donner 0 (la retenue finale est rejetée). Exemple : 0010 0101b + 1101 1011b = 1 0000 0000b → 0000 0000b."])

    HR(); EX(10, "Soustraire en additionnant (6 points · ≈ 12 min)", "Présentation diapositives 18 et 19 · Floyd 2-7 p. 71-73")
    CTX("l'unité de calcul d'un microcontrôleur n'a qu'un additionneur. Pour soustraire, elle additionne le complément à 2. Exemple : l'écart entre deux températures.")
    Q("a)", f"Calcule 75d − 28d en additionnant le complément à 2 de 28d.")
    ANS(f"28d = {B8(28)} → C1 = {B8(28 ^ 0xFF)} → C2 = {B8(c2(28))}.", 1, keep=True)
    ADD(75, c2(28), 8, la="75d", lb="+ C2(28d)", da="75d", db="−28d", ds="47d (retenue rejetée)", hide_b=True, keep_after=True)
    ANS("La 9e retenue est rejetée : 0010 1111b = 32 + 8 + 4 + 2 + 1 = 47d.", 1)
    Q("b)", "Il fait 18 °C le matin et 45 °C à midi dans la serre. Calcule 18d − 45d en complément à 2.")
    ANS(f"45d = {B8(45)} → C1 = {B8(45 ^ 0xFF)} → C2 = {B8(c2(45))}.", 1, keep=True)
    ADD(18, c2(45), 8, la="18d", lb="+ C2(45d)", da="18d", db="−45d", ds="−27d", hide_b=True, keep_after=True)
    ANS(f"Pas de 9e retenue, le MSB vaut 1 : le résultat est négatif. {B8((18 - 45) % 256)} → $−128 + 64 + 32 + 4 + 1 = −27$ → −27d (l'écart est de 27 °C).", 2)
    Q("c)", "Le microcontrôleur calcule +100d + 50d sur 8 bits signés. Le résultat est-il juste ? Explique.")
    ANS(f"Non. En 8 bits signés, l'étendue va de −128d à +127d et 150d dépasse +127d. Le résultat {B8(150)} a un MSB à 1 : il est lu comme $−128 + 16 + 4 + 2 = −106$, soit −106d. C'est un dépassement : deux nombres positifs donnent un résultat négatif.", 2)

    # ================= AUTO-ÉVALUATION
    P("**Auto-évaluation**", keep=True, after=1, before=10, color=NAVY)
    P("Après la correction : ✓ je sais seul·e · ~ avec une aide · ✗ à revoir (reprends alors la fiche d'origine).", keep=True, size=10)
    TABLE([TW / 5 - 0.01] * 5, [["Numération (N°1 à N°4)", "Débordement (N°5)", "Addition et multiplication (N°6 et N°7)", "Code Gray (N°8)", "Compléments (N°9 et N°10)"], ["", "", "", "", ""]],
          height=0.75, size=9, first_left=False)

    last = d.paragraphs[-1]   # paragraphe vide final : le plus petit possible pour ne pas créer de page blanche
    last.paragraph_format.space_after = Pt(0); last.paragraph_format.space_before = Pt(0); last.paragraph_format.line_spacing = Pt(1)
    last.add_run("").font.size = Pt(1)
    rpr = OxmlElement("w:rPr"); sz_ = OxmlElement("w:sz"); sz_.set(qn("w:val"), "2"); rpr.append(sz_); last._p.get_or_add_pPr().append(rpr)
    sec2 = d.sections[0]
    for part in (d.element, sec2.header._element, sec2.footer._element): reorder(part)
    z = d.settings.element.find(qn("w:zoom"))
    if z is not None: z.set(qn("w:percent"), "100")
    d.save(out); print("ok", out)


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    build(False, "out/EX Révision – numération et arithmétique binaire.docx")
    build(True, "out/EX C Révision – numération et arithmétique binaire.docx")
