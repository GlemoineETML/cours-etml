# -*- coding: utf-8 -*-
"""Fiche d'exercices + corrigé, gabarit ETML (à partir de modeles/modele.docx)."""
import os, re, shutil, zipfile, subprocess
from html import escape

SRC = "modeles/modele.docx"
WORK = "work_docx"
OUTDIR = "out"
RED = "EE0000"


# ------------------------------------------------------------------ briques XML
NBSP = "\u00a0"


def esc(t):
    for ch in ("?", "!", ";", ":", "»"):
        t = t.replace(" " + ch, NBSP + ch)
    t = t.replace("« ", "«" + NBSP)
    return escape(t, quote=False)


def run(t="", bold=False, color=None, sz=None, sub=False, sup=False,
        style=None, italic=False, tab=False, brk=False):
    rpr = ""
    if style:
        rpr += f'<w:rStyle w:val="{style}"/>'
    if bold:
        rpr += "<w:b/>"
    if italic:
        rpr += "<w:i/>"
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    if sz:
        rpr += f'<w:sz w:val="{sz}"/>'
    if sub:
        rpr += '<w:vertAlign w:val="subscript"/>'
    if sup:
        rpr += '<w:vertAlign w:val="superscript"/>'
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    inner = ""
    if tab:
        inner += "<w:tab/>"
    if brk:
        inner += '<w:br w:type="page"/>'
    if t:
        inner += f'<w:t xml:space="preserve">{esc(t)}</w:t>'
    return f"<w:r>{rpr}{inner}</w:r>"


SUBRE = re.compile(r"_\{([^}]*)\}|\^\{([^}]*)\}")


def rich(txt, **kw):
    """Transforme U_{0} et 10^{3} en indices / exposants."""
    out, pos = "", 0
    for m in SUBRE.finditer(txt):
        if m.start() > pos:
            out += run(txt[pos:m.start()], **kw)
        if m.group(1) is not None:
            out += run(m.group(1), sub=True, **kw)
        else:
            out += run(m.group(2), sup=True, **kw)
        pos = m.end()
    if pos < len(txt):
        out += run(txt[pos:], **kw)
    return out


def para(content="", after=None, before=None, tabs=None, style=None, jc=None,
         ind=None, keep=False, leader=None):
    ppr = ""
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if keep:
        ppr += "<w:keepNext/><w:keepLines/>"
    if tabs:
        # un entier negatif demande un taquet ALIGNE A DROITE a cette position
        ppr += "<w:tabs>" + "".join(
            f'<w:tab w:val="{"right" if p < 0 else "left"}" w:pos="{abs(p)}"/>'
            for p in tabs) + "</w:tabs>"
    if leader:
        ppr += ('<w:tabs><w:tab w:val="right" w:leader="underscore" '
                f'w:pos="{leader}"/></w:tabs>')
    if before is not None or after is not None:
        ppr += "<w:spacing"
        if before is not None:
            ppr += f' w:before="{before}"'
        if after is not None:
            ppr += f' w:after="{after}"'
        ppr += "/>"

    if ind is not None:
        ppr += f'<w:ind w:left="{ind}"/>'
    if jc:
        ppr += f'<w:jc w:val="{jc}"/>'
    ppr = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    return f"<w:p>{ppr}{content}</w:p>"


HR = para(run(tab=True, style="Accentuation") +
          '<w:r><w:rPr><w:rStyle w:val="Accentuation"/></w:rPr><w:pict>'
          '<v:rect style="width:453.6pt;height:1.5pt" o:hralign="center" '
          'o:hrstd="t" o:hr="t" fillcolor="#a0a0a0" stroked="f"/></w:pict></w:r>',
          tabs=[5670])
EMPTY = para(tabs=[5670])


def cell(w, content, jc="center"):
    return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>'
            f'<w:vAlign w:val="center"/></w:tcPr>'
            + para(content, style="Texte", jc=jc, ind=0) + "</w:tc>")


def table(cols, rows):
    """rows = [[(texte, {opts}) ...] ...] ; 1re ligne = en-tête."""
    grid = "".join(f'<w:gridCol w:w="{c}"/>' for c in cols)
    xml = ('<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/>'
           '<w:tblBorders>'
           + "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                     for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
           + '</w:tblBorders><w:tblLayout w:type="fixed"/>'
             '<w:tblCellMar><w:left w:w="57" w:type="dxa"/>'
             '<w:right w:w="57" w:type="dxa"/></w:tblCellMar>'
             '<w:tblLook w:val="0000"/></w:tblPr>'
           f'<w:tblGrid>{grid}</w:tblGrid>')
    for i, r in enumerate(rows):
        hdr = "<w:tblHeader/>" if i == 0 else ""
        xml += ('<w:tr><w:trPr><w:trHeight w:val="300"/><w:jc w:val="center"/>'
                + hdr + '</w:trPr>')
        for j, itm in enumerate(r):
            txt, opt = itm if isinstance(itm, tuple) else (itm, {})
            xml += cell(cols[j], rich(txt, bold=(i == 0) or opt.get("bold", False),
                                      color=opt.get("color")),
                        jc=opt.get("jc", "center"))
        xml += "</w:tr>"
    return xml + "</w:tbl>"


def image(rid, w_in, h_in, idx):
    cx, cy = int(w_in * 914400), int(h_in * 914400)
    return para(
        f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{100+idx}" name="Image{idx}"/>'
        f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{100+idx}" name="Image{idx}"/><pic:cNvPicPr/>'
        f'</pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}"/><a:stretch>'
        f'<a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/>'
        f'</a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
        f'</wp:inline></w:drawing></w:r>', jc="center", before=120, after=120)


