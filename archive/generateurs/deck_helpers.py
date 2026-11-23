# -*- coding: utf-8 -*-
"""Briques communes de construction des decks ETML. Extrait de build_pptx.py.
Presentation 'La source reelle et en charge' - gabarit ETML El Dim1."""
import re, copy
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image

NAVY = RGBColor(0x24, 0x28, 0x52)
BLUE = RGBColor(0x29, 0x7F, 0xD5)
RED = RGBColor(0xEE, 0x00, 0x00)
GREY = RGBColor(0x7F, 0x8F, 0xA9)

TPL = "modeles/modele.pptx"
OUT = "out/200 Source réelle et en charge.pptx"
FIG = "fig/"

CONTENT = dict(x=Inches(0.51), y=Inches(1.48), w=Inches(8.33), h=Inches(4.38))
SUB = re.compile(r"_\{([^}]*)\}")

prs = Presentation(TPL)

# --- supprimer les diapos du modèle -----------------------------------------
sldIdLst = prs.slides._sldIdLst
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
for sld in list(sldIdLst):
    prs.part.drop_rel(sld.get(RID))
    sldIdLst.remove(sld)

LAY_TITLE = prs.slide_layouts[0]
LAY_CONT = prs.slide_layouts[1]


def fill(par, text, size, color=NAVY, bold=False, italic=False):
    """Écrit le texte dans un paragraphe, _{x} devient un indice."""
    pos = 0
    for m in SUB.finditer(text):
        if m.start() > pos:
            _run(par, text[pos:m.start()], size, color, bold, italic, False)
        _run(par, m.group(1), size, color, bold, italic, True)
        pos = m.end()
    if pos < len(text):
        _run(par, text[pos:], size, color, bold, italic, False)


def _run(par, txt, size, color, bold, italic, sub):
    r = par.add_run()
    r.text = txt
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.italic = italic
    if sub:
        r.font._rPr.set("baseline", "-25000")


def title_of(slide, text, size=28):
    ph = slide.placeholders[0]
    tf = ph.text_frame
    tf.clear()
    fill(tf.paragraphs[0], text, size, NAVY, bold=False)
    return ph


def body_of(slide, items, box=None, sizes=(20, 17)):
    """items = [(niveau, texte, options)] ; options: bold/color/space."""
    ph = slide.placeholders[1]
    if box:
        ph.left, ph.top, ph.width, ph.height = box
    tf = ph.text_frame
    tf.clear()
    tf.word_wrap = True
    first = True
    for it in items:
        lvl, txt = it[0], it[1]
        opt = it[2] if len(it) > 2 else {}
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = lvl
        fill(p, txt, opt.get("size", sizes[min(lvl, len(sizes) - 1)]),
             opt.get("color", NAVY), opt.get("bold", False), opt.get("italic", False))
        p.space_after = Pt(opt.get("space", 8))
        if opt.get("nobullet"):
            pPr = p._pPr if p._pPr is not None else p._p.get_or_add_pPr()
            from pptx.oxml.ns import qn
            for tag in ("a:buChar", "a:buAutoNum", "a:buNone"):
                for e in pPr.findall(qn(tag)):
                    pPr.remove(e)
            pPr.append(pPr.makeelement(qn("a:buNone"), {}))
    return ph


def picture(slide, name, x, y, w=None, h=None):
    """Insère l'image en respectant son rapport, centrée dans la boîte (x,y,w,h)."""
    im = Image.open(FIG + name)
    ar = im.width / im.height
    if w and h:
        if w / h > ar:
            hh, ww = h, int(h * ar)
        else:
            ww, hh = w, int(w / ar)
    elif w:
        ww, hh = w, int(w / ar)
    else:
        hh, ww = h, int(h * ar)
    cx = x + (w - ww) // 2 if w else x
    cy = y + (h - hh) // 2 if h else y
    return slide.shapes.add_picture(FIG + name, cx, cy, ww, hh)


def notes(slide, txt):
    slide.notes_slide.notes_text_frame.text = txt


def new(kind="content"):
    return prs.slides.add_slide(LAY_TITLE if kind == "title" else LAY_CONT)


def textbox(slide, x, y, w, h, lines, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (txt, size, col, bold) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        fill(p, txt, size, col, bold)
    return tb




def nettoyer(presentation=None):
    """Supprime les emplacements réservés restés vides.

    Sans ce nettoyage, PowerPoint affiche « Cliquer pour ajouter du texte » sur
    toute diapositive dont on n'a pas rempli la zone de contenu du gabarit.
    """
    p = presentation if presentation is not None else prs
    n = 0
    for sl in p.slides:
        for ph in list(sl.placeholders):
            if ph.has_text_frame and not ph.text_frame.text.strip():
                ph._element.getparent().remove(ph._element)
                n += 1
    return n
