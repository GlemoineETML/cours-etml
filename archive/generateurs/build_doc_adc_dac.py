# -*- coding: utf-8 -*-
"""Feuille d'exercices + corrigé « Conversion analogique-numérique et numérique-analogique (CAN / CNA) ».
Part du modèle ETML Rapport_Simple.dotx (etml_base.docx, voir prep_modele.py) : police, styles, logo, en-tête, pied de page.
Couleurs ETML (marine 242852, bleu 297FD5, bleu clair ACCBF9). Réponses en rouge EE0000 dans le corrigé, vides pour l'apprenti.
Dates à l'américaine (MM/DD/YYYY). Éditeur : Gaël Lemoine."""
import os, re, math, datetime as dt
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree
from mathml import omath

RED = RGBColor(0xEE, 0x00, 0x00)
GREY = RGBColor(0x5A, 0x64, 0x78)
NAVY = RGBColor(0x24, 0x28, 0x52)
HEX_NAVY, HEX_BLUE, HEX_LBLUE, HEX_TINT = "242852", "297FD5", "ACCBF9", "E8EFFB"
BASE = "etml_base.docx"
MATIERE = "Test et Mesure 1 – El DT 1"
CLASSE, ANNEE, CHAMP = "XLO1", "2026-2027", "sur la vie, niveau 2"
EDITEUR = "Gaël Lemoine"
TITLE = "Conversion analogique-numérique et numérique-analogique"
SHORT = "Conversion A/N et N/A (CAN / CNA)"
# Références : à compléter — URL vide = emplacement « [lien à compléter] » visible dans le document
FLOYD, NEXTEC, NEXTEC_EX = "", "", ""
TW = 21.0 - 2.0 - 1.5
US = "%m/%d/%Y"


def b(v, n): return format(v, f"0{n}b")


def sp(s):
    out = []
    while s:
        out.insert(0, s[-4:]); s = s[:-4]
    return " ".join(out)


def fr(x, nd=3):
    """Nombre au format suisse/français : virgule décimale, espace des milliers."""
    s = f"{x:,.{nd}f}".replace(",", " ").replace(".", ",")
    return s


# ------------------------------------------------------------------ briques XML
def p_border(p, sides, sz=4, color=HEX_BLUE):
    pPr = p._p.get_or_add_pPr()
    bd = pPr.find(qn("w:pBdr"))
    if bd is None: bd = OxmlElement("w:pBdr"); pPr.append(bd)
    for sd in sides:
        e = OxmlElement(f"w:{sd}")
        for k, v in (("val", "single"), ("sz", sz), ("space", 4), ("color", color)): e.set(qn(f"w:{k}"), str(v))
        bd.append(e)


def hyperlink(p, url, text, size=None):
    if not url:
        r = p.add_run(text + " [lien à compléter]"); r.font.color.rgb = GREY
        if size: r.font.size = Pt(size)
        return
    rid = p.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), rid)
    r = OxmlElement("w:r"); rp = OxmlElement("w:rPr")
    col = OxmlElement("w:color"); col.set(qn("w:val"), HEX_BLUE); rp.append(col)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rp.append(u)
    if size:
        s = OxmlElement("w:sz"); s.set(qn("w:val"), str(int(size * 2))); rp.append(s)
    r.append(rp); t = OxmlElement("w:t"); t.text = text; t.set(qn("xml:space"), "preserve"); r.append(t)
    h.append(r); p._p.append(h)


# _{x} = indice, ^{x} = exposant, **x** = gras
SUB = re.compile(r"\$([^$]+)\$|_\{([^}]*)\}|\^\{([^}]*)\}|\*\*([^*]*)\*\*")
MNS = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


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
        if m.group(1) is not None:   # $...$ = équation Word native éditable (OMML)
            col = None if color is None else str(color)
            x = omath(m.group(1), color=col, sz=int(size * 2) if size else None)
            p._p.append(etree.fromstring(x.replace("<m:oMath>", "<m:oMath " + MNS + ">", 1)))
        elif m.group(2) is not None: add(m.group(2), sub=True)
        elif m.group(3) is not None: add(m.group(3), sup=True)
        else: add(m.group(4), bb=True)
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


# ------------------------------------------------------------------ calculs (source unique des réponses)
def can(ue, uref, n):
    q = uref / 2 ** n
    N = min(int(math.floor(ue / q + 1e-9)), 2 ** n - 1)
    return q, N


def sar(ue, uref, n):
    q = uref / 2 ** n; code = 0; steps = []
    for k in range(n - 1, -1, -1):
        t = code | (1 << k); keep = t * q <= ue + 1e-12
        steps.append((t, t * q, keep))
        if keep: code = t
    return code, steps


# ------------------------------------------------------------------ document
def build(corr, out):
    d = Document(BASE)
    body = d.element.body
    for el in list(body):
        if el.tag != qn("w:sectPr"): body.remove(el)
    now = dt.datetime.now()
    kind = "Corrigé" if corr else "Exercices"
    title_doc = f"{TITLE} – {kind}"
    cp = d.core_properties
    cp.title = title_doc; cp.author = EDITEUR; cp.last_modified_by = EDITEUR
    cp.created = now; cp.modified = now; cp.last_printed = now; cp.revision = 1
    cp.subject = f"{MATIERE} – {CLASSE} – {ANNEE}"
    sec = d.sections[0]
    # en-tête du modèle : « Nom - Type - Numéro » → titre court – type – matière, en bleu marine
    for t in sec.header._element.iter(qn("w:t")):
        if t.text == "Nom -": t.text = f"CAN / CNA – {kind} – El DT 1"
        elif t.text in (" ", "Type - Numéro"): t.text = ""
    for r in sec.header._element.iter(qn("w:r")):
        tt = r.find(qn("w:t"))
        if tt is not None and (tt.text or "").strip():
            rPr = r.find(qn("w:rPr"))
            if rPr is None: rPr = OxmlElement("w:rPr"); r.insert(0, rPr)
            c = OxmlElement("w:color"); c.set(qn("w:val"), HEX_NAVY); rPr.append(c)
    # champs du pied de page : dates au format américain (MM/DD/YYYY) → commutateur \@ dans le champ + valeur affichée
    vals = {"AUTHOR": EDITEUR, "LASTSAVEDBY": EDITEUR, "SAVEDATE": now.strftime(US + " %H:%M"),
            "CREATEDATE": now.strftime(US), "PRINTDATE": now.strftime(US + " %H:%M"),
            "FILENAME": os.path.basename(out), "TITLE": title_doc}
    fmt = {"SAVEDATE": r'\@ "MM/dd/yyyy HH:mm"', "CREATEDATE": r'\@ "MM/dd/yyyy"', "PRINTDATE": r'\@ "MM/dd/yyyy HH:mm"'}
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
                if k in fmt: it.text = f" {k} {fmt[k]} "
                if k in vals: cur = k
            elif t is not None and state == "res" and cur:
                if cur == "_done": t.text = ""
                else: t.text = vals[cur]; cur = "_done"
    for name in ("Title", "Heading 1", "Heading 2"):
        try:
            st_ = d.styles[name]; st_.font.color.rgb = NAVY; st_.paragraph_format.keep_with_next = True
        except KeyError:
            pass

    # ---------------- helpers
    def P(txt="", after=3, before=0, align=None, keep=False, **kw):
        p = d.add_paragraph(); f = p.paragraph_format
        f.space_after = Pt(after); f.space_before = Pt(before); f.keep_with_next = keep
        if align is not None: p.alignment = align
        if kw.get("size") and kw["size"] <= 10: f.line_spacing = 1.15
        rich(p, txt, **kw); return p

    def EX(n, title, ref=None, context=None):
        p = d.add_paragraph(); f = p.paragraph_format
        f.space_before = Pt(8); f.space_after = Pt(2); f.keep_with_next = True
        r = p.add_run(f"N°{n} {title}"); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = NAVY
        if ref:
            q = P(ref + " · ", italic=True, size=9, color=GREY, keep=True, after=3)
            hyperlink(q, FLOYD, "Floyd, chapitre conversion A/N et N/A", size=9)
        if context:
            P("Contexte : " + context, italic=True, size=10, keep=True)

    def HR():
        p = d.add_paragraph(); p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
        p_border(p, ["bottom"], 4)

    def Q(lbl, txt):
        p = d.add_paragraph(); f = p.paragraph_format
        f.left_indent = Cm(0.7); f.first_line_indent = Cm(-0.7); f.space_before = Pt(3); f.space_after = Pt(2)
        f.tab_stops.add_tab_stop(Cm(0.7)); f.keep_with_next = True
        r = p.add_run(lbl + "\t"); r.bold = True
        rich(p, txt); return p

    def ANS(txt, lines=1):
        if corr:
            ls = txt.split("\n")
            for i, t in enumerate(ls):
                p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7)
                p.paragraph_format.space_after = Pt(1 if i < len(ls) - 1 else 4)
                rich(p, t, color=RED)
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
        """('R', txt) = réponse : rouge dans le corrigé, vide pour l'apprenti."""
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

    def PIC(path, width):
        d.add_picture(path, width=Cm(width)); d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ================= TITRE
    d.add_paragraph(TITLE, style="Title")
    P(f"Feuille d'exercices – {MATIERE} · Classe {CLASSE} · {ANNEE} · Champ d'apprentissage : {CHAMP}",
      align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, after=2)
    P(f"Éditeur : {EDITEUR} · {now.strftime(US)}", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=10, color=GREY, after=8)
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.paragraph_format.space_after = Pt(0)
    r = p.add_run("Corrigé" if corr else "Version apprenti·e"); r.bold = True
    if corr: r.font.color.rgb = RED
    p.add_run("\tNom :")
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.add_run("\tDate :")
    p_border(p, ["bottom"], 4)

    if corr:
        BOX(["Plan de séance (enseignant·e) – 2 × 45 min",
             "Séance 1 : N°1 à N°4 (quantum, tension → code, code → tension, approximations successives). Séance 2 : N°5 à N°8 (CNA, échantillonnage, multimètre, thermomètre LM35). N°9 = exercice mélangé pour la révision espacée : à donner une semaine plus tard, en début de cours, sans la fiche.",
             "Différenciation : les encadrés « Si difficulté » donnent un deuxième chemin d'explication ; les apprenti·e·s rapides font les questions « Bonus » puis les exercices Nextec.",
             "Chaque calcul se termine par un contrôle (N × q doit redonner la tension à moins d'un quantum près) : exiger qu'il soit écrit, c'est la compétence visée (vérifier son propre résultat)."])

    P("**Conventions :** binaire avec le suffixe **b** (0101b), décimal **d** si nécessaire (89d), hexadécimal **h** (59h). Virgule décimale. Calculatrice autorisée sauf indication contraire ; écris toujours la formule, le calcul avec les unités, puis le contrôle.", after=4)
    P("**Ressources :**", after=1, keep=True)
    pr_ = P("Floyd : ", after=1, size=10); hyperlink(pr_, FLOYD, "chapitre conversion analogique-numérique et numérique-analogique (PDF sur Teams)", size=10)
    pr_ = P("Nextec Media : ", after=1, size=10); hyperlink(pr_, NEXTEC, "chapitre sur les convertisseurs A/N et N/A", size=10)
    pr_ = P("Nextec Media : ", after=6, size=10); hyperlink(pr_, NEXTEC_EX, "exercices complémentaires", size=10)

    # ================= AIDE-MÉMOIRE
    d.add_heading("Aide-mémoire", level=1)
    TABLE([3.6, TW - 3.6 - 4.6 - 0.02, 4.6], [
        ["Notion", "Formule / règle", "Exemple"],
        ["Niveaux", "Un convertisseur de n bits a $2^{n}$ codes : de 0 à $2^{n}-1$.", "10 bits → 1024 codes"],
        ["Quantum q (1 LSB)", "$q=\\f{U_{\\u{ref}}}{2^{n}}$ (plus petite variation mesurable)", "5 V / 1024 = 4,883 mV"],
        ["CAN : tension → code", "$N=\\u{ent}(\\f{U_{\\u{e}}}{q})$ ; si $U_{\\u{e}}\\geq U_{\\u{ref}}$ → $N=2^{n}-1$ (saturation)", "2,00 V / 4,883 mV = 409,6 → 409"],
        ["CNA : code → tension", "$U_{\\u{s}}=N\\cdot q$ ; tension max $=U_{\\u{ref}}-q$", "4 bits, 3,2 V : 1010b → 2,0 V"],
        ["Poids des bits (CNA)", "MSB = U_{ref}/2, puis U_{ref}/4, U_{ref}/8 … LSB = q", "3,2 V : 1,6 – 0,8 – 0,4 – 0,2 V"],
        ["Approximations successives", "Du MSB au LSB : bit à 1 → essai ≤ U_{e} ? garder 1 : remettre 0", "4 essais pour 4 bits"],
        ["Échantillonnage", "Règle de Shannon : $f_{\\u{e}}>2\\cdot f_{\\u{max}}$", "voix 3,4 kHz → f_{e} = 8 kHz"],
        ["Multimètre", "$\\u{résolution}=\\f{\\u{calibre}}{\\u{nombre de points}}$ (3½ digits = 2000 points)", "calibre 2 V → 1 mV"],
    ], height=0.65, size=9.5)

    d.add_heading("Exercices", level=1)

    # ---- N°1 Résolution et quantum
    EX(1, "Résolution et quantum", "Méthode : diapositive 6",
       "en lisant la fiche technique d'un microcontrôleur ou d'une carte d'acquisition, le technicien vérifie d'abord la résolution : elle dit si le convertisseur est assez fin pour la mesure demandée.")
    Q("a)", "Complète le tableau (q avec 4 chiffres significatifs et l'unité adaptée).")
    cfg = [(3, 8.0), (8, 5.0), (10, 5.0), (12, 3.3), (16, 2.048)]
    def qtxt(q):
        if q >= 1: return fr(q, 3).rstrip("0").rstrip(",") + " V"
        if q >= 1e-3: return fr(q * 1e3, 3) + " mV"
        return fr(q * 1e6, 2) + " µV"
    TABLE([3.2, 3.4, 4.0, TW - 10.6 - 0.02], [["Bits n", "U_{ref}", "Nombre de codes 2^{n}", "Quantum q = U_{ref} / 2^{n}"]] +
          [[str(n), fr(u, 3).rstrip("0").rstrip(",") + " V", ("R", f"{2 ** n:,}".replace(",", " ")), ("R", qtxt(u / 2 ** n))] for n, u in cfg],
          height=0.55, size=10)
    Q("b)", "On veut mesurer une tension de 0 à 5 V en voyant des variations de 2 mV. Quel est le plus petit nombre de bits suffisant ? Justifie.")
    # 5/2^n <= 2 mV -> 2^n >= 2500 -> n = 12
    ANS("Il faut $q\\leq 2\\u{ mV}$ → $2^{n}\\geq\\f{5\\u{ V}}{2\\u{ mV}}=2500$. 2^{11} = 2048 (trop peu), 2^{12} = 4096 ✓ → 12 bits (q = 1,221 mV).", 2)
    Q("c)", "Un collègue dit : « Avec 10 bits et U_{ref} = 5 V, je mesure au millivolt près. » A-t-il raison ?")
    ANS("Non : q = 4,883 mV. Le CAN ne distingue pas des écarts de 1 mV ; il faudrait au moins 13 bits (5 V / 2^{13} = 0,61 mV).", 2)

    # ---- N°2 Tension → code
    HR(); EX(2, "Du signal au nombre : tension → code (CAN)", "Méthode : diapositives 7 à 9",
       "un CAN 8 bits avec U_{ref} = 5,12 V mesure la tension d'une sonde dans une machine de production ; le programme ne reçoit que le code N.")
    P("Le quantum vaut $q=\\f{5,12\\u{ V}}{256}=20\\u{ mV}$. Complète le tableau, puis contrôle avec N × q.", keep=True)
    rows = [["U_{e}", "U_{e} / q", "N (décimal)", "N (binaire 8 bits)", "N (hexa)", "Contrôle N × q"]]
    for ue in (0.50, 1.30, 2.56, 3.47, 4.00, 5.30):
        q, N = can(ue, 5.12, 8)
        ratio = fr(ue / q, 1).rstrip("0").rstrip(",")
        rows.append([fr(ue, 2) + " V", ("R", ratio + (" → saturation" if ue >= 5.12 else "")), ("R", str(N)),
                     ("R", sp(b(N, 8)) + "b"), ("R", format(N, "02x") + "h"), ("R", fr(N * q, 2) + " V")])
    TABLE([1.9, 3.4, 2.1, 3.6, 2.0, TW - 13.0 - 0.02], rows, height=0.55, size=10, mono_cols=(3, 4))
    Q("a)", "Pour 5,30 V, la valeur lue est-elle juste ? Que faut-il prévoir dans le montage ?")
    ANS("Non : 5,30 V dépasse U_{ref}, le CAN sature à 1111 1111b = 255 → 5,10 V. Il faut adapter le signal avant le CAN (diviseur de tension) pour rester sous 5,12 V.", 2)
    BOX(["Si difficulté – 2e son de cloche",
         "Faire compter des marches d'escalier de 20 mV : « combien de marches entières peut-on monter avec 1,30 V ? » → 65. Le code, c'est le numéro de la marche. Toujours convertir les deux tensions dans la même unité (1,30 V = 1300 mV) avant de diviser."])

    # ---- N°3 Code → tension
    HR(); EX(3, "Du nombre à la mesure : code → tension", "Méthode : diapositive 7",
       "un capteur de pression industriel délivre 0 V à 0 bar et 4,096 V à 10 bar. Il est relié à un CAN 10 bits avec U_{ref} = 4,096 V. Le programme lit N et doit afficher la pression.")
    P("Quantum : $q=\\f{4,096\\u{ V}}{1024}=4\\u{ mV}$.", keep=True)
    rows = [["N lu", "N (décimal)", "Tension N × q", "Pression (bar)"]]
    for N in (200, 512, 0b1100100000, 1023):
        lab = sp(b(N, 10)) + "b" if N in (0b1100100000,) else str(N)
        rows.append([lab, ("R", str(N)), ("R", fr(N * 0.004, 3) + " V"), ("R", fr(N * 0.004 / 4.096 * 10, 2) + " bar")])
    TABLE([3.6, 3.0, 4.0, TW - 10.6 - 0.02], rows, height=0.55, size=10, mono_cols=(0,))
    Q("a)", "Quelle est la plus petite variation de pression que le système peut détecter ?")
    ANS("1 quantum = 4 mV → $\\f{4\\u{ mV}}{4,096\\u{ V}}\\times 10\\u{ bar}=0,00977\\u{ bar}$ ≈ 0,01 bar (10 mbar).", 1)
    Q("b)", "Pourquoi la pression maximale affichée vaut-elle 9,99 bar et non 10,00 bar ?")
    ANS("Le code maximal est 2^{10} − 1 = 1023 : 1023 × 4 mV = 4,092 V = U_{ref} − q → 9,99 bar. La valeur U_{ref} elle-même n'a pas de code.", 2)

    # ---- N°4 Approximations successives
    HR(); EX(4, "Les approximations successives pas à pas", "Méthode : diapositive 10",
       "c'est ainsi que travaille le CAN intégré à chaque microcontrôleur (Arduino, STM32…). Comprendre ce principe aide à lire les chronogrammes des fiches techniques (une conversion = n étapes).")
    for lbl, ue in (("a)", 5.3), ("b)", 1.9)):
        code, steps = sar(ue, 8.0, 4)
        Q(lbl, f"CAN 4 bits, U_{{ref}} = 8 V (q = 0,5 V), U_{{e}} = {fr(ue, 1)} V. Complète le tableau des essais.")
        rows = [["Essai", "Code d'essai", "Tension d'essai", "Comparaison avec U_{e}", "Bit décidé"]]
        for i, (t, ut, keep) in enumerate(steps):
            rows.append([str(i + 1), ("R", b(t, 4) + "b"), ("R", fr(ut, 1) + " V"),
                         ("R", ("≤ " if keep else "> ") + fr(ue, 1) + " V → " + ("garder 1" if keep else "remettre 0")),
                         ("R", f"b{3 - i} = {1 if keep else 0}")])
        TABLE([1.6, 3.0, 3.2, TW - 10.6 - 0.02, 2.8], rows, height=0.52, size=10, mono_cols=(1,))
        ANS(f"Résultat : {b(code, 4)}b = {code} → {code} × 0,5 V = {fr(code * 0.5, 1)} V. Contrôle : {fr(ue, 1)} / 0,5 = {fr(ue / 0.5, 1)} → {code} ✓", 1)
    Q("c)", "Combien d'essais faut-il à un CAN 10 bits ? Et pour trouver le code en essayant toutes les valeurs une par une ?")
    ANS("Approximations successives : 10 essais (un par bit). Essais un par un : jusqu'à 1024. C'est pour cela que la méthode est si utilisée.", 2)
    BOX(["Si difficulté",
         "Jouer d'abord au « nombre mystère » entre 0 et 15 avec le voisin (réponses « plus » / « moins » seulement), en notant chaque question. Puis refaire l'exercice en remplaçant les nombres par des tensions : chaque nombre × 0,5 V."])

    # ---- N°5 CNA
    HR(); EX(5, "Le CNA : du code à la tension", "Méthode : diapositives 13 et 14",
       "un microcontrôleur pilote un CNA 4 bits avec U_{ref} = 3,2 V pour fabriquer une tension de consigne (par exemple la vitesse d'un ventilateur) ou une forme d'onde, comme un petit générateur de fonctions.")
    Q("a)", "Calcule q, puis le poids en volts de chaque bit.")
    TABLE([3.8] + [(TW - 3.8 - 0.02) / 4] * 4, [["", "b3 (MSB)", "b2", "b1", "b0 (LSB)"],
                                               ["Poids", ("R", "1,6 V"), ("R", "0,8 V"), ("R", "0,4 V"), ("R", "0,2 V = q")]],
          height=0.55, size=10)
    Q("b)", "Complète le tableau des tensions de sortie.")
    rows = [["Code", "Bits à 1", "Somme des poids", "U_{s} = N × q"]]
    for c in (0b0001, 0b0101, 0b1000, 0b1010, 0b1100, 0b1111):
        bits = [f"b{k}" for k in range(3, -1, -1) if (c >> k) & 1]
        poids = " + ".join(fr(3.2 / 2 ** (4 - k), 1) for k in range(3, -1, -1) if (c >> k) & 1)
        rows.append([b(c, 4) + "b", ("R", ", ".join(bits)), ("R", poids + " V"), ("R", f"{c} × 0,2 V = {fr(c * 0.2, 1)} V")])
    TABLE([2.6, 3.2, 5.2, TW - 11.0 - 0.02], rows, height=0.52, size=10, mono_cols=(0,))
    Q("c)", "Un compteur fait défiler les codes 0000b → 1111b, un nouveau code toutes les 1 ms. Dessine la tension de sortie U_{s} sur la grille.")
    PIC("fig_cna.png" if corr else "fig_cna_vierge.png", 12.5)
    Q("d)", "Quelle est la tension maximale ? Quel code faudrait-il pour obtenir 2,5 V ? Est-ce possible exactement ?")
    ANS("U_{s max} = 15 × 0,2 V = 3,0 V (= U_{ref} − q). 2,5 V / 0,2 V = 12,5 : pas de code entier → impossible exactement ; le plus proche est 1100b (2,4 V) ou 1101b (2,6 V). Il faudrait plus de bits.", 3)
    Q("e)", "Bonus : quelle tension d'escalier obtiendrait-on avec un CNA 8 bits, même U_{ref} ? Qu'est-ce que ça change pour un son ?")
    ANS("q = 3,2 V / 256 = 12,5 mV : 16 fois plus de marches, 16 fois plus petites. Le signal est plus lisse, le son moins « granuleux » (moins de bruit de quantification).", 2)

    # ---- N°6 Échantillonnage
    HR(); EX(6, "Échantillonner assez vite", "Méthode : diapositive 12",
       "le choix de la fréquence d'échantillonnage fixe la qualité d'un enregistrement et la quantité de mémoire nécessaire : c'est un choix de conception courant pour un électronicien.")
    Q("a)", "Le CD audio utilise f_{e} = 44,1 kHz. Quelle est la plus haute fréquence enregistrable ? Pourquoi ce choix, sachant que l'oreille humaine entend jusqu'à environ 20 kHz ?")
    ANS("$f_{\\u{max}}<\\f{f_{\\u{e}}}{2}=22,05\\u{ kHz}$. C'est un peu plus que 20 kHz : tout ce que l'oreille entend est bien reproduit.", 2)
    Q("b)", "La voix au téléphone est limitée à 3,4 kHz. Quelle fréquence d'échantillonnage minimale faut-il ?")
    ANS("$f_{\\u{e}}>2\\times 3,4\\u{ kHz}=6,8\\u{ kHz}$. On utilise 8 kHz en téléphonie.", 1)
    Q("c)", "Quelle mémoire faut-il pour 1 minute de musique au format CD (16 bits, 2 voies stéréo, 44,1 kHz) ? Donne le résultat en octets puis en Mo (1 Mo = 10^{6} octets).")
    ANS("44 100 échantillons/s × 2 voies × 2 octets (16 bits) × 60 s = 10 584 000 octets ≈ 10,6 Mo par minute.", 2)
    Q("d)", "Un thermostat mesure la température d'une pièce, qui varie en quelques minutes. Faut-il échantillonner à 44,1 kHz ? Propose une valeur.")
    ANS("Non : la température varie très lentement. 1 mesure par seconde (1 Hz) suffit largement ; échantillonner plus vite consommerait de l'énergie et de la mémoire pour rien.", 2)
    Q("e)", "Une roue tourne à 5 tours par seconde. Une caméra la filme à 6 images par seconde. Que voit-on à l'écran ? Comment s'appelle ce phénomène ?")
    ANS("6 Hz < 2 × 5 Hz : la règle de Shannon n'est pas respectée. On voit une rotation lente (ici 1 tour par seconde, parfois à l'envers) : c'est le repliement (aliasing).", 2)

    # ---- N°7 Multimètre
    HR(); EX(7, "Ton multimètre est un CAN", "Méthode : diapositive 16",
       "au laboratoire et sur le terrain, choisir le bon calibre du multimètre donne le plus de chiffres utiles ; noter le calibre dans un rapport de mesure permet de connaître la résolution de chaque valeur.")
    P("Multimètre 3½ digits (2000 points). Complète le tableau.", keep=True)
    rows = [["Calibre", "Résolution", "Affichage pour 1,5 V", "Affichage pour 12,6 V"]]
    for cal, res, a1, a2 in (("200 mV", "0,1 mV", "1 (OL : dépassement)", "1 (OL : dépassement)"),
                             ("2 V", "1 mV", "1,500", "1 (OL : dépassement)"),
                             ("20 V", "10 mV", "01,50", "12,60"),
                             ("200 V", "0,1 V", "001,5", "012,6")):
        rows.append([cal, ("R", res), ("R", a1), ("R", a2)])
    TABLE([2.8, 3.2, 5.3, TW - 11.3 - 0.02], rows, height=0.52, size=10)
    Q("a)", "Quel calibre choisis-tu pour mesurer une batterie de voiture (environ 12,6 V) ? Justifie.")
    ANS("Calibre 20 V : c'est le plus petit calibre qui ne sature pas ; résolution 10 mV, affichage 12,60 (4 chiffres utiles). Le calibre 200 V n'afficherait que 012,6.", 2)
    Q("b)", "Résolution et précision : est-ce la même chose ? Explique avec tes mots.")
    ANS("Non. La résolution est le plus petit pas affiché (ex. 1 mV). La précision dit de combien la valeur affichée peut s'écarter de la vraie valeur ; elle est donnée dans la notice (± % de la lecture ± digits). Un appareil peut afficher 1,500 V avec une erreur réelle de ± 10 mV.", 3)

    # ---- N°8 Situation complète
    HR(); EX(8, "Situation professionnelle : le thermomètre de la serre", "Méthode : diapositive 17",
       "ton entreprise réalise un thermomètre pour une serre avec un capteur LM35 (10 mV/°C) relié au CAN 10 bits d'un Arduino (U_{ref} = 5 V). Tu dois vérifier le calcul avant la mise en service.")
    PIC("fig_lm35.png", 15.5)
    q, N = can(0.25, 5.0, 10)
    Q("a)", "Quelle tension donne le capteur à 25,0 °C ? Quel code N le CAN fournit-il (décimal et binaire 10 bits) ?")
    ANS(f"U_{{e}} = 25,0 °C × 10 mV/°C = 0,250 V. q = 5 V / 1024 = 4,883 mV. N = 0,250 V / 4,883 mV = 51,2 → {N} = {sp(b(N, 10))}b.", 2)
    Q("b)", "Quelle température le programme affiche-t-il ? D'où vient l'écart ?")
    ANS(f"{N} × 4,883 mV = {fr(N * q * 1000, 1)} mV → {fr(N * q * 100, 1)} °C. L'écart vient de la quantification (troncature : on perd la partie 0,2 du quantum).", 2)
    Q("c)", "Quelle est la résolution du thermomètre en °C ?")
    ANS("$\\f{4,883\\u{ mV}}{10\\u{ mV/°C}}=0,49\\u{ °C}$ : on ne peut pas distinguer des écarts plus petits qu'environ 0,5 °C.", 1)
    Q("d)", "Le client veut une résolution de 0,1 °C, pour des températures jusqu'à 50 °C. On peut choisir U_{ref} = 1,1 V. Est-ce une bonne solution ? Calcule.")
    ANS("$q=\\f{1,1\\u{ V}}{1024}=1,074\\u{ mV}$ → 0,107 °C ≈ 0,1 °C ✓. Plage max : 1,1 V / 10 mV/°C = 110 °C > 50 °C ✓. Bonne solution : on a réduit la plage pour gagner en finesse.", 3)

    # ---- N°9 Mélange
    HR(); EX(9, "Exercice mélangé (révision une semaine plus tard, sans la fiche)", None)
    Q("a)", "CAN 8 bits, U_{ref} = 2,56 V. Calcule q, puis le code de 1,00 V en binaire.")
    q9, N9 = can(1.00, 2.56, 8)
    ANS(f"q = 2,56 V / 256 = 10 mV. N = 1,00 V / 10 mV = {N9} → {sp(b(N9, 8))}b.", 1)
    Q("b)", "CNA 8 bits, U_{ref} = 2,56 V. Quelle tension donne 1100 0000b ?")
    ANS("1100 0000b = 192 → 192 × 10 mV = 1,92 V (ou poids : 1,28 V + 0,64 V).", 1)
    Q("c)", "Un signal contient des fréquences jusqu'à 1 kHz. Peut-on l'échantillonner à 1,5 kHz ?")
    ANS("Non : il faut f_{e} > 2 × 1 kHz = 2 kHz. À 1,5 kHz on obtiendrait un faux signal (repliement).", 1)
    Q("d)", "Vrai ou faux ? Justifie. « Un CNA 4 bits avec U_{ref} = 5 V peut sortir exactement 5 V. »")
    ANS("Faux : U_{s max} = 15 × (5 V / 16) = 4,6875 V = U_{ref} − q.", 1)
    Q("e)", "Auto-évaluation : pour chaque thème, note ✓ (je sais seul·e), ~ (avec la fiche) ou ✗ (à revoir).")
    TABLE([TW / 5 - 0.01] * 5, [["Quantum", "Tension → code", "CNA", "Échantillonnage", "Multimètre"], ["", "", "", "", ""]],
          height=0.8, size=10, first_left=False)

    for part in (d.element, sec.header._element, sec.footer._element): reorder(part)
    z = d.settings.element.find(qn("w:zoom"))
    if z is not None: z.set(qn("w:percent"), "100")
    d.save(out); print("ok", out)


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    build(False, f"out/EX {SHORT.replace('/', '-')}.docx")
    build(True, f"out/EX C {SHORT.replace('/', '-')}.docx")
