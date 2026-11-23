# -*- coding: utf-8 -*-
"""Fiche d'exercices + corrigé, gabarit ETML (à partir de modeles/modele.docx)."""
import os, re, shutil, zipfile, subprocess
from html import escape

SRC = "modeles/modele.docx"
WORK = "work_docx"
OUTDIR = "out"
RED = "EE0000"
TITRE = "Source réelle et en charge"

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
        ppr += "<w:tabs>" + "".join(
            f'<w:tab w:val="left" w:pos="{p}"/>' for p in tabs) + "</w:tabs>"
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
        xml += '<w:tr><w:trPr><w:trHeight w:val="300"/><w:jc w:val="center"/></w:trPr>'
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


# ------------------------------------------------------------------ contenu
def build(corrige):
    """Retourne le XML du corps. corrige=True → réponses en rouge."""
    C = dict(color=RED)          # style des réponses
    B = []

    def ans(txt, lines=1):
        """Réponse : en rouge dans le corrigé, ligne à remplir chez l'élève."""
        if corrige:
            B.append(para(rich(txt, color=RED), after=60, ind=340))
        else:
            for _ in range(lines):
                B.append(para(run(tab=True), leader=9350, before=70, after=70,
                              ind=340))

    def q(txt, after=60, keep=False):
        B.append(para(rich(txt), after=after, ind=340, keep=keep))

    def enonce(txt, after=120):
        B.append(para(rich(txt), after=after))

    def ex(num, titre):
        if B:
            B.extend([EMPTY, EMPTY, HR])
        B.append(para(rich(f"N°{num} {titre}"), tabs=[5103], after=120, keep=True))

    # ---------------------------------------------------------------- N°1
    ex(1, "Vocabulaire de la source réelle")
    enonce("Complète le tableau.")
    rows = [["Notation", "Ce que c’est", "Unité"]]
    data = [("U_{0}", "tension à vide, sans charge", "V"),
            ("R_{i}", "résistance interne de la source", "Ω"),
            ("U", "tension aux bornes, en charge", "V"),
            ("I_{cc}", "courant de court-circuit", "A")]
    for n, d, u in data:
        rows.append([(n, {}),
                     (d if corrige else "", dict(color=RED, jc="left")),
                     (u if corrige else "", dict(color=RED))])
    B.append(table([1418, 4536, 992], rows))
    B.append(EMPTY)
    q("a)  Écris la relation qui lie U, U_{0}, R_{i} et I :")
    ans("U = U_{0} − R_{i} · I")
    q("b)  Que vaut R_{i} pour une source idéale ?")
    ans("R_{i} = 0 Ω")

    # ---------------------------------------------------------------- N°2
    ex(2, "Application directe")
    enonce("Une source a une tension à vide U_{0} = 9 V et une résistance interne "
           "R_{i} = 1,5 Ω.")
    q("a)  Calcule la tension à ses bornes lorsqu’elle débite I = 0,5 A.")
    ans("U = 9 − 1,5 · 0,5 = 8,25 V", 2)
    q("b)  Même source, cette fois I = 2 A.")
    ans("U = 9 − 1,5 · 2 = 6,0 V", 2)
    q("c)  Quelle est la chute de tension interne dans le cas b) ?")
    ans("R_{i} · I = 1,5 · 2 = 3,0 V")

    # ---------------------------------------------------------------- N°3
    ex(3, "Source avec sa charge")
    enonce("Une pile (U_{0} = 4,5 V ; R_{i} = 0,5 Ω) alimente une lampe de "
           "résistance R = 4 Ω.")
    q("a)  Calcule le courant débité.")
    ans("Circuit série : I = U_{0} / (R_{i} + R) = 4,5 / 4,5 = 1,0 A", 2)
    q("b)  Calcule la tension aux bornes de la pile.")
    ans("U = 4,5 − 0,5 · 1,0 = 4,0 V", 2)
    q("c)  Quelle puissance reçoit la lampe ? Quelle puissance est perdue dans la pile ?")
    ans("P_{lampe} = U · I = 4,0 · 1,0 = 4,0 W    et    P_{perdue} = R_{i} · I² "
        "= 0,5 · 1,0² = 0,5 W", 2)

    # ---------------------------------------------------------------- N°4
    ex(4, "Déterminer la résistance interne")
    enonce("Sur une alimentation d’atelier, on relève deux points de mesure :")
    B.append(table([2268, 1701, 1701],
                   [["Mesure", "U [V]", "I [A]"],
                    ["à vide", "12,0", "0"],
                    ["en charge", "11,4", "3,0"]]))
    B.append(EMPTY)
    q("a)  Calcule la résistance interne de cette alimentation.")
    ans("R_{i} = ΔU / ΔI = (12,0 − 11,4) / 3,0 = 0,6 / 3,0 = 0,2 Ω", 2)
    q("b)  Calcule le courant de court-circuit.")
    ans("I_{cc} = U_{0} / R_{i} = 12,0 / 0,2 = 60 A", 2)
    q("c)  Quelle tension lirait-on aux bornes pour un courant de 5 A ?")
    ans("U = 12,0 − 0,2 · 5 = 11,0 V", 2)

    # ---------------------------------------------------------------- N°5
    ex(5, "Caractéristique U(I)")
    enonce("Une source a U_{0} = 9 V et R_{i} = 3 Ω.")
    q("a)  Calcule son courant de court-circuit.")
    ans("I_{cc} = 9 / 3 = 3 A")
    q("b)  Trace la caractéristique U(I) de cette source sur le quadrillage ci-dessous.", keep=True)
    B.append(image("rIdGraph", 5.5, 3.67, 1))
    q("c)  Lis sur ton tracé la tension aux bornes pour I = 2 A.")
    ans("U = 3,0 V")
    q("d)  Quelle résistance de charge donne ce point de fonctionnement ?")
    ans("R = U / I = 3,0 / 2,0 = 1,5 Ω")

    # ---------------------------------------------------------------- N°6
    ex(6, "Situation d’atelier : diagnostic de deux batteries")
    enonce("Deux batteries 12 V sont testées. Pour chacune, on mesure la tension à vide, "
           "puis la tension pendant un essai de démarrage qui appelle 180 A.")
    B.append(table([1701, 2268, 2268],
                   [["Batterie", "à vide [V]", "à 180 A [V]"],
                    ["A", "12,6", "10,8"],
                    ["B", "12,4", "7,0"]]))
    B.append(EMPTY)
    q("a)  Calcule la résistance interne de chaque batterie.")
    ans("Batterie A : R_{i} = (12,6 − 10,8) / 180 = 1,8 / 180 = 0,010 Ω", 2)
    ans("Batterie B : R_{i} = (12,4 − 7,0) / 180 = 5,4 / 180 = 0,030 Ω", 2)
    q("b)  Les deux batteries affichent presque la même tension à vide. Laquelle "
      "faut-il remplacer ? Justifie en une phrase.")
    ans("La batterie B : sa résistance interne est trois fois plus grande, donc sa "
        "tension s’effondre dès qu’on tire du courant. Un contrôle au voltmètre à vide "
        "ne suffit pas pour juger une batterie.", 2)
    q("c)  Calcule le courant de court-circuit de la batterie A et explique en une "
      "phrase pourquoi un court-circuit accidentel est dangereux.")
    ans("I_{cc} = 12,6 / 0,010 = 1260 A : les conducteurs fondent, il y a arc "
        "électrique et projections de métal en fusion.", 2)

    return "".join(B)


# ------------------------------------------------------------------ assemblage
def make(corrige):
    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    with zipfile.ZipFile(SRC) as z:
        z.extractall(WORK)
    for root, _, files in os.walk(WORK):
        for f in files:
            p = os.path.join(root, f)
            if os.path.islink(p):
                os.remove(p)

    # image du quadrillage
    os.makedirs(f"{WORK}/word/media", exist_ok=True)
    src_img = "fig/08_grille_corrige.png" if corrige else "fig/08_grille_vide.png"
    shutil.copy(src_img, f"{WORK}/word/media/grille.png")
    rels = f"{WORK}/word/_rels/document.xml.rels"
    t = open(rels, encoding="utf8").read()
    t = t.replace("</Relationships>",
                  '<Relationship Id="rIdGraph" Type="http://schemas.openxmlformats.org/'
                  'officeDocument/2006/relationships/image" Target="media/grille.png"/>'
                  "</Relationships>")
    open(rels, "w", encoding="utf8").write(t)
    ct = f"{WORK}/[Content_Types].xml"
    t = open(ct, encoding="utf8").read()
    if 'Extension="png"' not in t:
        t = t.replace("<Default Extension=\"rels\"",
                      "<Default Extension=\"png\" ContentType=\"image/png\"/>"
                      "<Default Extension=\"rels\"")
    open(ct, "w", encoding="utf8").write(t)

    # corps du document
    doc = f"{WORK}/word/document.xml"
    t = open(doc, encoding="utf8").read()
    sectpr = re.search(r"<w:sectPr .*?</w:sectPr>", t, re.S).group(0)

    entete = (
        para(run(TITRE, style="Accentuation", sz="36") + run(tab=True, style="Accentuation")
             + run("Nom :", style="Accentuation"), tabs=[5670], after=60)
        + para((run("Corrigé", style="Accentuation", color=RED) if corrige else run("", style="Accentuation"))
               + run(tab=True, style="Accentuation") + run("Date :", style="Accentuation"),
               tabs=[5670], after=60)
        + HR)

    body = entete + build(corrige) + EMPTY + sectpr
    t = re.sub(r"<w:body>.*</w:body>", "<w:body>" + body + "</w:body>", t, flags=re.S)
    open(doc, "w", encoding="utf8").write(t)

    os.makedirs(OUTDIR, exist_ok=True)
    name = ("210 EX C Source réelle et en charge.docx" if corrige
            else "210 EX Source réelle et en charge.docx")
    out = os.path.join(OUTDIR, name)
    if os.path.exists(out):
        os.remove(out)
    subprocess.run(["zip", "-Xqr", os.path.abspath(out), "."], cwd=WORK, check=True)
    print("saved", out)
    return out


if __name__ == "__main__":
    make(True)
    make(False)
