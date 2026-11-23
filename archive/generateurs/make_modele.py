# -*- coding: utf-8 -*-
"""Reconstitue le gabarit Word ETML d'après modeles/charte-graphique-ETML.md
(à utiliser seulement si le vrai modele.docx n'est pas joint)."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

d = Document()
s = d.sections[0]
s.page_width, s.page_height = Inches(8.27), Inches(11.69)
s.left_margin, s.right_margin = Inches(0.79), Inches(0.59)
s.top_margin, s.bottom_margin = Inches(0.87), Inches(0.71)
s.header_distance, s.footer_distance = Inches(0.3), Inches(0.3)

st = d.styles["Normal"]
st.font.name = "Arial"; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
st.paragraph_format.space_after = Pt(0)

t = d.styles.add_style("Texte", WD_STYLE_TYPE.PARAGRAPH)
t.base_style = st; t.font.size = Pt(11)
a = d.styles.add_style("Accentuation", WD_STYLE_TYPE.CHARACTER)
a.font.italic = True; a.font.size = Pt(14)

def border(p, sz):
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", "1"), ("w:color", "000000")):
        bt.set(qn(k), v)
    b.append(bt); pPr.append(b)

def field(p, code):
    for typ in ("begin", None, "end"):
        r = OxmlElement("w:r")
        if typ is None:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = " %s " % code
            r.append(it)
            p._p.append(r)
            r2 = OxmlElement("w:r"); fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "separate"); r2.append(fc); p._p.append(r2)
            r3 = OxmlElement("w:r"); tt = OxmlElement("w:t"); tt.text = "1"; r3.append(tt); p._p.append(r3)
            continue
        fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), typ); r.append(fc); p._p.append(r)

h = s.header.paragraphs[0]
r = h.add_run("ETML"); r.bold = True; r.font.size = Pt(26); r.font.color.rgb = RGBColor(0x24, 0x28, 0x52)
r = h.add_run("   Formation des électroniciens"); r.bold = True; r.font.size = Pt(14)
border(h, 18)

f = s.footer.paragraphs[0]
f.paragraph_format.tab_stops.add_tab_stop(Inches(3.25), WD_TAB_ALIGNMENT.CLEAR)
f.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.CLEAR)
f.paragraph_format.tab_stops.add_tab_stop(Inches(6.89), WD_TAB_ALIGNMENT.RIGHT)
for x in ():
    pass
def frun(txt):
    rr = f.add_run(txt); rr.font.size = Pt(9); return rr
fp = f
field(fp, "FILENAME")
frun("\tPage "); field(fp, "PAGE"); frun(" / "); field(fp, "NUMPAGES")
for rr in fp._p.iter(qn("w:r")):
    rPr = rr.find(qn("w:rPr"))
    if rPr is None:
        rPr = OxmlElement("w:rPr"); rr.insert(0, rPr)
    if rPr.find(qn("w:sz")) is None:
        sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "18"); rPr.append(sz)
d.add_paragraph("")
z = d.settings.element.find(qn("w:zoom"))
if z is not None:
    z.set(qn("w:percent"), "100")
d.save("modeles/modele.docx")
print("modele ok")
