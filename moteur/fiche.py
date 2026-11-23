# -*- coding: utf-8 -*-
"""Fiches d'exercices, corrigés et tests (REGLES 4) : modèle ETML Rapport_Simple, en-tête, pied de page (dates US),
couleurs ETML, liens, équations Word natives (OMML), tableaux de réponses (rouge dans le corrigé, vides pour l'apprenti·e).
La fiche élève et le corrigé sortent du même contenu : Doc(corr=False) puis Doc(corr=True)."""
import os, re, datetime as dt
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml
from moteur.omml import omath
from moteur.typo import typo

RED = RGBColor(0xEE, 0x00, 0x00)
GREY = RGBColor(0x5A, 0x64, 0x78)
NAVY = RGBColor(0x24, 0x28, 0x52)
BLUE = RGBColor(0x29, 0x7F, 0xD5)
HEX_NAVY, HEX_BLUE, HEX_LBLUE, HEX_TINT = "242852", "297FD5", "ACCBF9", "E8EFFB"
TW = 21.0 - 2.0 - 1.5
NSD = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
SUB = re.compile(r"_\{([^}]*)\}|\^\{([^}]*)\}|\*\*([^*]*)\*\*")


def p_border(p, sides, sz=4, color="297FD5"):
    pPr = p._p.get_or_add_pPr()
    bd = pPr.find(qn("w:pBdr"))
    if bd is None: bd = OxmlElement("w:pBdr"); pPr.append(bd)
    for sd in sides:
        e = OxmlElement(f"w:{sd}")
        for k, v in (("val", "single"), ("sz", sz), ("space", 4), ("color", color)): e.set(qn(f"w:{k}"), str(v))
        bd.append(e)


def hyperlink(p, url, text, size=None, bold=False):
    rid = p.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), rid)
    r = OxmlElement("w:r"); rp = OxmlElement("w:rPr")
    if bold: rp.append(OxmlElement("w:b"))
    col = OxmlElement("w:color"); col.set(qn("w:val"), HEX_BLUE); rp.append(col)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rp.append(u)
    if size:
        s = OxmlElement("w:sz"); s.set(qn("w:val"), str(int(size * 2))); rp.append(s)
    r.append(rp); t = OxmlElement("w:t"); t.text = typo(text); t.set(qn("xml:space"), "preserve"); r.append(t)
    h.append(r); p._p.append(h)


def rich(p, txt, color=None, bold=False, italic=False, size=None, font=None):
    txt = typo(txt)      # espaces insécables (avant : ; ? !, nombre + unité, p. 5, N° 2…)
    pos = 0
    def add(t, sub=False, sup=False, bb=False):
        r = p.add_run(t); r.bold = bold or bb; r.italic = italic
        if "\u2011" in t:      # trait d'union insécable natif de Word (NON-ET ne se coupe pas)
            for el in r._r.findall(qn("w:t")): r._r.remove(el)
            for k, part in enumerate(t.split("\u2011")):
                if k: r._r.append(OxmlElement("w:noBreakHyphen"))
                if part:
                    te = OxmlElement("w:t"); te.text = part; te.set(qn("xml:space"), "preserve"); r._r.append(te)
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


class Doc:
    """Un document ETML. corr = True → corrigé (réponses en rouge).
    base : etml_base.docx préparé par moteur/charte.py ; images : dossier des figures ; maintenant : date des champs du pied de page."""

    def __init__(self, corr, out, title, kind_label, header_name, subject, editeur, base, images, maintenant=None):
        self.corr, self.out, self.title, self.images = corr, out, title, images
        d = self.d = Document(base)
        body = d.element.body
        for el in list(body):
            if el.tag != qn("w:sectPr"): body.remove(el)
        now = maintenant or dt.datetime.now()
        cp = d.core_properties
        cp.title = f"{title} – {kind_label}"; cp.author = editeur; cp.last_modified_by = editeur
        cp.created = now; cp.modified = now; cp.last_printed = now; cp.revision = 1
        cp.subject = subject
        sec = d.sections[0]
        for t in sec.header._element.iter(qn("w:t")):
            if t.text == "Nom -": t.text = header_name
            elif t.text in (" ", "Type - Numéro"): t.text = ""
        for r in sec.header._element.iter(qn("w:r")):
            if r.find(qn("w:t")) is not None and (r.find(qn("w:t")).text or "").strip():
                rPr = r.find(qn("w:rPr"))
                if rPr is None: rPr = OxmlElement("w:rPr"); r.insert(0, rPr)
                c = OxmlElement("w:color"); c.set(qn("w:val"), HEX_NAVY); rPr.append(c)
        vals = {"AUTHOR": editeur, "LASTSAVEDBY": editeur, "SAVEDATE": now.strftime("%m/%d/%Y %H:%M"),
                "CREATEDATE": now.strftime("%m/%d/%Y"), "PRINTDATE": now.strftime("%m/%d/%Y %H:%M"),
                "FILENAME": os.path.basename(out), "TITLE": cp.title}
        for it_ in sec.footer._element.iter(qn("w:instrText")):
            it_.text = it_.text.replace("dd/MM/yyyy", "MM/dd/yyyy")
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
        for name in ("Title", "Heading 1", "Heading 2"):
            try:
                st_ = d.styles[name]; st_.font.color.rgb = NAVY; st_.paragraph_format.keep_with_next = True
            except KeyError:
                pass

    # ---------------------------------------------------------------- texte
    def P(self, txt="", after=3, before=0, align=None, keep=False, **kw):
        p = self.d.add_paragraph(); f = p.paragraph_format
        f.space_after = Pt(after); f.space_before = Pt(before); f.keep_with_next = keep
        if align is not None: p.alignment = align
        f.line_spacing = 1.15 if (kw.get("size") and kw["size"] <= 10) else 1.25
        rich(p, txt, **kw); return p

    def LINKS(self, prefix, items, size=10, after=1, keep=False):
        """prefix + liste de (texte, url ou None)."""
        p = self.P(prefix, after=after, size=size, keep=keep, align=WD_ALIGN_PARAGRAPH.LEFT)   # pas de justification : liens longs
        for txt, url in items:
            if url: hyperlink(p, url, txt, size=size)
            else: rich(p, txt, size=size)
        return p

    def EX(self, n, title, refs=()):
        p = self.d.add_paragraph(); f = p.paragraph_format
        f.space_before = Pt(8); f.space_after = Pt(2); f.keep_with_next = True
        rich(p, f"N°{n} {title}", bold=True, size=12, color=NAVY)
        if refs:
            q = self.P("", italic=True, size=9, color=GREY, keep=True, after=3, align=WD_ALIGN_PARAGRAPH.LEFT)
            for k, (txt, url) in enumerate(refs):
                if k: rich(q, " · ", italic=True, size=9, color=GREY)
                if url: hyperlink(q, url, txt, size=9)
                else: rich(q, txt, italic=True, size=9, color=GREY)

    def H1(self, txt, page_break=False):
        """Titre 1 du modèle (Arial 14 pt gras numéroté), avec la typographie française."""
        h = self.d.add_heading(typo(txt), level=1); h.paragraph_format.page_break_before = page_break
        return h

    def HR(self):
        p = self.d.add_paragraph(); p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
        p_border(p, ["bottom"], 4)

    def Q(self, lbl, txt):
        p = self.d.add_paragraph(); f = p.paragraph_format
        f.left_indent = Cm(0.7); f.first_line_indent = Cm(-0.7); f.space_before = Pt(3); f.space_after = Pt(2)
        f.tab_stops.add_tab_stop(Cm(0.7)); f.keep_with_next = True; f.line_spacing = 1.25; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(lbl + "\t"); r.bold = True
        self.MIX(p, txt); return p

    def CTX(self, txt):
        self.P("Contexte : " + txt, italic=True, size=10, keep=True, color=GREY, align=WD_ALIGN_PARAGRAPH.LEFT)

    def BOX(self, lines, only_corr=True):
        if only_corr and not self.corr: return
        for i, t in enumerate(lines):
            p = self.d.add_paragraph(); f = p.paragraph_format
            f.left_indent = Cm(0.2); f.right_indent = Cm(0.2)
            f.space_before = Pt(4 if i == 0 else 0); f.space_after = Pt(6 if i == len(lines) - 1 else 0)
            f.keep_with_next = i < len(lines) - 1; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_border(p, ["top", "left", "bottom", "right"], 4)
            rich(p, t, bold=(i == 0), italic=(i > 0), size=9.5)

    # ---------------------------------------------------------------- équations natives
    def EQ(self, p, src, color=None, sz=None):
        p._p.append(parse_xml(omath(src, color, sz).replace("<m:oMath>", f"<m:oMath {NSD}>", 1)))

    def MIX(self, p, txt, color=None, size=None, bold=False):
        """Texte avec segments $...$ rendus en équations natives."""
        for k, seg in enumerate(txt.split("$")):
            if not seg: continue
            if k % 2: self.EQ(p, seg, "EE0000" if color == RED else None, int(size * 2) if size else None)
            else: rich(p, seg, color=color, size=size, bold=bold)

    def ANS(self, txt, lines=1, keep=False):
        d = self.d
        if self.corr:
            parts = txt.split("\n")
            for i, t in enumerate(parts):
                p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7)
                p.paragraph_format.space_after = Pt(1 if i < len(parts) - 1 else 4)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT; p.paragraph_format.line_spacing = 1.25; p.paragraph_format.keep_with_next = keep or i < len(parts) - 1
                self.MIX(p, t, color=RED)
        else:
            for i in range(lines):      # les lignes restent avec la question (pas de ligne seule en haut de page)
                p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7); p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.tab_stops.add_tab_stop(Cm(TW), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
                p.paragraph_format.keep_with_next = keep or i < lines - 1; p.add_run("\t")

    # ---------------------------------------------------------------- tableaux
    def cell_txt(self, c, txt, bold=False, italic=False, color=None, size=10, align="center", shade=None):
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]; f = p.paragraph_format; f.space_after = Pt(0); f.space_before = Pt(0); f.line_spacing = 1.0
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if align == "center" else WD_ALIGN_PARAGRAPH.LEFT
        self.MIX(p, txt, color=color, size=size, bold=bold) if "$" in txt else rich(p, txt, color=color, bold=bold, italic=italic, size=size)
        if shade:
            tcPr = c._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
            sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), shade); tcPr.append(sh)

    def TABLE(self, widths, rows, header=True, height=0.6, size=10, first_left=True, keep_after=False, parent=None, bold_first=True):
        """('R', txt) = réponse : rouge dans le corrigé, vide pour l'apprenti·e."""
        d = self.d
        t = (parent or d).add_table(rows=len(rows), cols=len(widths)); t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
        for i, row in enumerate(rows):
            tr = t.rows[i]; tr.height = Cm(height)
            for j, v in enumerate(row):
                c = tr.cells[j]; c.width = Cm(widths[j])
                hdr_ = header and i == 0
                al = "left" if (first_left and j == 0 and not hdr_) else "center"
                if isinstance(v, tuple) and v[0] == "R":
                    self.cell_txt(c, v[1] if self.corr else "", color=RED if self.corr else None, bold=True, size=size, align=al)
                else:
                    self.cell_txt(c, v, italic=False, bold=hdr_ or (bold_first and first_left and j == 0), size=size, align=al,
                                  shade=HEX_LBLUE if hdr_ else None, color=NAVY if hdr_ else None)
        for j, w in enumerate(widths): t.columns[j].width = Cm(w)
        for i, tr in enumerate(t.rows):
            tr._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
            if i < len(t.rows) - 1 or keep_after:
                for c in tr.cells:
                    for pp in c.paragraphs: pp.paragraph_format.keep_with_next = True
        if parent is None:
            spc = d.add_paragraph(); spc.paragraph_format.space_after = Pt(2); spc.paragraph_format.line_spacing = 1.0
            spc.paragraph_format.keep_with_next = keep_after
        return t

    def IMG(self, path, width_cm, align=WD_ALIGN_PARAGRAPH.CENTER, keep=False, after=4, parent=None):
        p = (parent.paragraphs[0] if parent is not None and not parent.paragraphs[0].text and not parent.paragraphs[0].runs
             else (parent.add_paragraph() if parent is not None else self.d.add_paragraph()))
        p.alignment = align; p.paragraph_format.space_after = Pt(after); p.paragraph_format.keep_with_next = keep
        p.add_run().add_picture(os.path.join(self.images, path), width=Cm(width_cm))
        return p

    def finish(self):
        d = self.d
        last = d.paragraphs[-1]
        if last.text.strip() or last._p.findall(qn("m:oMath")):    # le dernier paragraphe a du contenu : on n'écrase pas son interligne
            last = d.add_paragraph()
        last.paragraph_format.space_after = Pt(0); last.paragraph_format.space_before = Pt(0); last.paragraph_format.line_spacing = Pt(1)
        last.add_run("").font.size = Pt(1)
        sec2 = d.sections[0]
        for part in (d.element, sec2.header._element, sec2.footer._element): reorder(part)
        z = d.settings.element.find(qn("w:zoom"))
        if z is not None: z.set(qn("w:percent"), "100")
        d.save(self.out); print("ok", os.path.basename(self.out))

    # ---------------------------------------------------------------- bloc d'en-tête commun
    def head(self, title, info_items, minutes_box, consignes, ressources):
        d = self.d
        d.add_paragraph(title, style="Title")
        p = self.P("", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, after=8, size=10)
        for txt, url in info_items:
            if url: hyperlink(p, url, txt, size=10)
            else: rich(p, txt, italic=True, size=10)
        p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.paragraph_format.space_after = Pt(0)
        r = p.add_run("Corrigé" if self.corr else "Version apprenti·e"); r.bold = True
        if self.corr: r.font.color.rgb = RED
        rich(p, "\tNom :")
        p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); rich(p, "\tDate :")
        p_border(p, ["bottom"], 4)
        self.BOX(minutes_box)
        for c in consignes:
            self.P(c, after=4)
        self.P("**Ressources :**", after=1, keep=True)
        for prefix, items in ressources:
            self.LINKS(prefix, items, size=10, after=1, keep=True)
        self.P("", after=4)
