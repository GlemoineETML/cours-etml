# -*- coding: utf-8 -*-
"""Feuille d'exercices + corrigé « La charge d'un condensateur ».
Part du modèle ETML Rapport_Simple.dotx (etml_base.docx, voir prep_modele.py) : police, styles, logo, en-tête, pied de page.
Couleurs ETML (marine 242852, bleu 297FD5, bleu clair ACCBF9). Réponses en rouge EE0000 dans le corrigé, vides pour l'apprenti.
Dates à l'américaine (MM/DD/YYYY). Éditeur : Gaël Lemoine. Symboles et notations selon CEI 60617 / CEI 60027."""
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
HEX_NAVY, HEX_BLUE, HEX_LBLUE = "242852", "297FD5", "ACCBF9"
BASE = "etml_base.docx"
MATIERE = "Test et Mesure 1 – El DT 1"
CLASSE, ANNEE, CHAMP = "CLO1B", "2026-2027", "LZ_6969"
EDITEUR = "Gaël Lemoine"
TITLE = "La charge d'un condensateur"
SHORT = "Charge du condensateur"
FLOYD, NEXTEC = "", ""          # édition test : références citées sans lien
TW = 21.0 - 2.0 - 1.5
US = "%m/%d/%Y"
E = math.e


def fr(x, nd=2):
    s = f"{x:,.{nd}f}".replace(",", " ").replace(".", ",")
    return s


def uc(U, t, tau): return U * (1 - E ** (-t / tau))


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
        if m.group(1) is not None:
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


# ------------------------------------------------------------------ données et réponses (source unique)
N1 = [  # (R affiché, R en Ω, C affiché, C en F)
    ("10 kΩ", 10e3, "100 µF", 100e-6),
    ("1 kΩ", 1e3, "4,7 µF", 4.7e-6),
    ("220 Ω", 220, "1000 µF", 1000e-6),
    ("47 kΩ", 47e3, "10 nF", 10e-9),
    ("1 MΩ", 1e6, "2,2 µF", 2.2e-6),
]


def tfmt(t):
    if t >= 1: return fr(t, 2).rstrip("0").rstrip(",") + " s"
    if t >= 1e-3: return fr(t * 1e3, 2).rstrip("0").rstrip(",") + " ms"
    return fr(t * 1e6, 1).rstrip("0").rstrip(",") + " µs"


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
    for t in sec.header._element.iter(qn("w:t")):
        if t.text == "Nom -": t.text = f"Charge du condensateur · {kind} · El DT 1"
        elif t.text in (" ", "Type - Numéro"): t.text = ""
    for r in sec.header._element.iter(qn("w:r")):
        tt = r.find(qn("w:t"))
        if tt is not None and (tt.text or "").strip():
            rPr = r.find(qn("w:rPr"))
            if rPr is None: rPr = OxmlElement("w:rPr"); r.insert(0, rPr)
            c = OxmlElement("w:color"); c.set(qn("w:val"), HEX_NAVY); rPr.append(c)
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

    def P(txt="", after=3, before=0, align=None, keep=False, **kw):
        p = d.add_paragraph(); f = p.paragraph_format
        f.space_after = Pt(after); f.space_before = Pt(before); f.keep_with_next = keep
        if align is not None: p.alignment = align
        if kw.get("size") and kw["size"] <= 10: f.line_spacing = 1.15
        rich(p, txt, **kw); return p

    def EX(n, title, ref=None, context=None):
        p = d.add_paragraph(); f = p.paragraph_format
        f.space_before = Pt(8); f.space_after = Pt(2); f.keep_with_next = True
        rich(p, f"N°{n} {title}", bold=True, size=12, color=NAVY)
        if ref: P(ref, italic=True, size=9, color=GREY, keep=True, after=3)
        if context: P("Contexte : " + context, italic=True, size=10, keep=True)

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

    def cell_txt(c, txt, bold=False, italic=False, color=None, size=10, align="center", shade=None):
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]; f = p.paragraph_format; f.space_after = Pt(0); f.space_before = Pt(0); f.line_spacing = 1.0
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if align == "center" else WD_ALIGN_PARAGRAPH.LEFT
        rich(p, txt, color=color, bold=bold, italic=italic, size=size)
        if shade:
            tcPr = c._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
            sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), shade); tcPr.append(sh)

    def TABLE(widths, rows, header=True, height=0.6, size=10, first_left=True):
        t = d.add_table(rows=len(rows), cols=len(widths)); t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
        for i, row in enumerate(rows):
            tr = t.rows[i]; tr.height = Cm(height)
            for j, v in enumerate(row):
                c = tr.cells[j]; c.width = Cm(widths[j])
                hdr_ = header and i == 0
                al = "left" if (first_left and j == 0) else "center"
                if isinstance(v, tuple) and v[0] == "R":
                    cell_txt(c, v[1] if corr else "", color=RED if corr else None, bold=True, size=size, align=al)
                else:
                    cell_txt(c, v, bold=hdr_ or (first_left and j == 0), size=size, align=al,
                             shade=HEX_LBLUE if hdr_ else None, color=NAVY if hdr_ else None)
        for j, w in enumerate(widths): t.columns[j].width = Cm(w)
        for i, tr in enumerate(t.rows):
            tr._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
            if i < len(t.rows) - 1:
                for c in tr.cells:
                    for pp in c.paragraphs: pp.paragraph_format.keep_with_next = True
        spc = d.add_paragraph(); spc.paragraph_format.space_after = Pt(2); spc.paragraph_format.line_spacing = 1.0
        return t

    def PIC(path, width, keep=False):
        d.add_picture(path, width=Cm(width)); p = d.paragraphs[-1]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = keep

    # ================= TITRE
    d.add_paragraph(TITLE, style="Title")
    P(f"Feuille d'exercices · {MATIERE} · Classe {CLASSE} · {ANNEE} · Champ d'apprentissage : {CHAMP}",
      align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, after=2)
    P(f"Éditeur : {EDITEUR} · {now.strftime(US)}", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=10, color=GREY, after=8)
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.paragraph_format.space_after = Pt(0)
    r = p.add_run("Corrigé" if corr else "Version apprenti·e"); r.bold = True
    if corr: r.font.color.rgb = RED
    p.add_run("\tNom :")
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.add_run("\tDate :")
    p_border(p, ["bottom"], 4)

    if corr:
        BOX(["Plan de séance (enseignant·e), 45 min d'exercices après la présentation",
             "N°1 à N°3 en classe (calcul de τ, lecture des courbes, tableau de charge), N°4 et N°5 en binôme, N°6 au laboratoire si un oscilloscope est disponible, sinon sur la figure. N°7 = situation professionnelle à discuter en commun. N°8 est l'exercice mélangé de révision : le donner une semaine plus tard, en début de cours, sans la fiche.",
             "Différenciation : les encadrés « Si difficulté » proposent une autre explication ; les apprenti·e·s rapides font les questions Bonus.",
             "Exiger à chaque calcul : formule, valeurs converties en puissances de 10, résultat avec l'unité, puis contrôle (ordre de grandeur, ou loi des mailles u_{R} + u_{C} = U)."])

    P("**Conventions :** symboles selon CEI 60617, grandeurs variables en minuscules (u_{C}, i), constantes en majuscules (U, I_{0}). Virgule décimale. Calculatrice autorisée. Écris toujours la formule, le calcul avec les unités, puis le contrôle.", after=4)
    P("**Ressources :**", after=1, keep=True)
    pr_ = P("Floyd : ", after=1, size=10); hyperlink(pr_, FLOYD, "chapitre sur les circuits RC", size=10)
    pr_ = P("Nextec Media : ", after=6, size=10); hyperlink(pr_, NEXTEC, "chapitre condensateur, charge et décharge", size=10)

    # ================= AIDE-MÉMOIRE
    d.add_heading("Aide-mémoire", level=1)
    PIC("fig_circuit.png", 9.5, keep=True)
    TABLE([3.4, TW - 3.4 - 5.0 - 0.02, 5.0], [
        ["Notion", "Formule / règle", "Exemple"],
        ["Constante de temps", "$\\tau=R\\cdot C$ (τ en s, R en Ω, C en F)", "10 kΩ × 100 µF = 1 s"],
        ["Charge complète", "après 5τ, u_{C} ≈ 99 % de U", "5 × 1 s = 5 s"],
        ["Tension", "$u_{\\u{C}}=U\\cdot(1-\\u{e}^{-\\f{t}{\\tau}})$", "t = τ → 63 % de U"],
        ["Courant", "$i=I_{0}\\cdot \\u{e}^{-\\f{t}{\\tau}}$ avec $I_{0}=\\f{U}{R}$", "12 V / 10 kΩ = 1,2 mA"],
        ["Loi des mailles", "$U=u_{\\u{R}}+u_{\\u{C}}$ à chaque instant", "u_{C} = 7,6 V → u_{R} = 4,4 V"],
        ["Repères", "τ : 63 % · 2τ : 86 % · 3τ : 95 % · 4τ : 98 % · 5τ : 99 %", ""],
        ["Préfixes", "k = 10^{3} · M = 10^{6} · m = 10^{−3} · µ = 10^{−6} · n = 10^{−9}", "4,7 µF = 4,7·10^{−6} F"],
    ], height=0.62, size=9.5)

    d.add_heading("Exercices", level=1)

    # ---- N°1 Calcul de τ
    EX(1, "Calculer τ et la durée de charge", "Méthode : diapositive 3",
       "quand on conçoit une temporisation ou qu'on dépanne une carte, on lit R et C sur les composants (avec leurs préfixes) et on estime en quelques secondes la vitesse de charge.")
    Q("a)", "Complète le tableau. Convertis d'abord R et C en puissances de 10.")
    rows = [["R", "C", "Calcul τ = R · C", "τ", "Charge complète 5τ"]]
    for rl, rv, cl, cv in N1:
        t = rv * cv
        rows.append([rl, cl, ("R", f"{rl} × {cl}"), ("R", tfmt(t)), ("R", tfmt(5 * t))])
    TABLE([2.2, 2.2, TW - 4.4 - 5.6 - 0.02, 2.6, 3.0], rows, height=0.55, size=10)
    Q("b)", "On double la valeur de R. Que devient τ ? Et si on double R et C ?")
    ANS("τ double (τ = R · C est proportionnel à R). Si on double R et C, τ est multiplié par 4.", 2)

    # ---- N°2 Comprendre les courbes
    HR(); EX(2, "Comprendre ce qui se passe pendant la charge", "Méthode : diapositive 2",
       "un technicien qui comprend le comportement d'un condensateur sait expliquer pourquoi une alimentation absorbe un fort courant à la mise sous tension (courant d'appel), puis presque plus rien.")
    Q("a)", "Juste après la fermeture de S (t = 0), que valent u_{C}, u_{R} et i ? Justifie avec la loi des mailles.")
    ANS("Condensateur vide : u_{C} = 0. Loi des mailles : u_{R} = U − u_{C} = U. Donc $i=I_{0}=\\f{U}{R}$, c'est le courant maximal.", 2)
    Q("b)", "Pourquoi le courant diminue-t-il pendant la charge ?")
    ANS("u_{C} augmente, donc u_{R} = U − u_{C} diminue ; avec i = u_{R} / R, le courant diminue aussi.", 2)
    Q("c)", "Le condensateur est chargé. Que valent u_{C}, u_{R} et i ? Par quoi peut-on remplacer le condensateur dans le schéma ?")
    ANS("u_{C} = U, u_{R} = 0, i = 0. En continu, le condensateur chargé se comporte comme un circuit ouvert (interrupteur ouvert).", 2)
    BOX(["Si difficulté",
         "Penser à un réservoir rempli par un tuyau étroit (la résistance) : au début l'eau entre vite, puis de plus en plus lentement à mesure que le niveau monte. Le niveau d'eau, c'est u_{C} ; le débit, c'est i. Quand le réservoir est plein, le débit s'arrête."])

    # ---- N°3 Tableau de charge
    HR(); EX(3, "Tableau de charge et tracé de la courbe", "Méthode : diapositives 2 et 3",
       "au laboratoire, on relève ou on calcule quelques points, puis on trace la courbe pour vérifier un montage et le comparer à la théorie.")
    P("Circuit de la diapositive 3 : U = 12 V, R = 10 kΩ, C = 100 µF, donc τ = 1 s.", keep=True)
    U3, R3, tau3 = 12, 10e3, 1.0
    rows = [["t", "u_{C} = U · (1 − e^{−t/τ})", "u_{R} = U − u_{C}", "i = u_{R} / R"]]
    for t in range(6):
        u = uc(U3, t, tau3)
        rows.append([f"{t} s", ("R", fr(u, 2) + " V"), ("R", fr(U3 - u, 2) + " V"), ("R", fr((U3 - u) / R3 * 1e3, 3) + " mA")])
    TABLE([2.0, TW - 2.0 - 4.0 - 4.0 - 0.02, 4.0, 4.0], rows, height=0.52, size=10)
    Q("a)", "Place les points de u_{C} sur la grille et trace la courbe.")
    PIC("fig_n3.png" if corr else "fig_n3_vierge.png", 9.5)
    Q("b)", "Contrôle : à t = 1 s, vérifie que u_{R} + u_{C} = U. Quel pourcentage de U a-t-on atteint ?")
    ANS(f"{fr(uc(U3, 1, 1), 2)} V + {fr(U3 - uc(U3, 1, 1), 2)} V = 12 V ✓. {fr(uc(U3, 1, 1), 2)} V / 12 V = 63,2 % : on retrouve le repère de τ.", 2)

    # ---- N°4 Instant quelconque
    HR(); EX(4, "Calculer u_{C} à un instant donné", "Méthode : diapositive 3",
       "un programme de microcontrôleur doit souvent attendre qu'une tension ait atteint une certaine valeur ; il faut donc savoir calculer u_{C} à n'importe quel instant, y compris entre les repères τ, 2τ, 3τ…")
    U4, R4, C4 = 5.0, 10e3, 22e-6; tau4 = R4 * C4
    P("U = 5 V, R = 10 kΩ, C = 22 µF. Utilise la touche e^{x} de ta calculatrice.", keep=True)
    Q("a)", "Calcule τ.")
    ANS("τ = 10·10^{3} Ω × 22·10^{−6} F = 0,22 s = 220 ms.", 1)
    Q("b)", "Calcule u_{C} à t = 100 ms.")
    ANS(f"$u_{{\\u{{C}}}}=5\\u{{ V}}\\cdot(1-\\u{{e}}^{{-\\f{{100}}{{220}}}})$ = 5 V × (1 − {fr(E ** (-100 / 220), 3)}) = {fr(uc(U4, 0.1, tau4), 2)} V", 2)
    Q("c)", "Calcule u_{C} à t = 440 ms, puis contrôle avec le tableau des repères.")
    ANS(f"t = 2τ → u_{{C}} = 5 V × (1 − e^{{−2}}) = {fr(uc(U4, 0.44, tau4), 2)} V. Contrôle : 86 % de 5 V = 4,3 V ✓.", 2)
    Q("d)", "Bonus : au bout de combien de temps u_{C} atteint-il la moitié de U ? (Indice : $t=\\tau\\cdot\\u{ln}\\u{ }2$)")
    ANS(f"t = 220 ms × 0,693 = {fr(tau4 * math.log(2) * 1e3, 0)} ms (environ 0,7τ).", 1)

    # ---- N°5 Reset microcontrôleur
    HR(); EX(5, "Situation professionnelle : le reset au démarrage", None,
       "à la mise sous tension, une alimentation met quelques millisecondes à se stabiliser. Pour que le microcontrôleur ne démarre pas trop tôt, on place un circuit RC sur sa broche RESET : il démarre quand u_{C} dépasse environ 63 % de 5 V, donc au bout d'environ τ.")
    Q("a)", "R = 10 kΩ et C = 1 µF. Quel est le délai de démarrage ?")
    ANS("τ = 10·10^{3} Ω × 1·10^{−6} F = 10 ms : le microcontrôleur démarre environ 10 ms après la mise sous tension.", 1)
    Q("b)", "La fiche technique de l'alimentation demande d'attendre au moins 40 ms. On garde R = 10 kΩ. Choisis C dans la série E6 (1 ; 1,5 ; 2,2 ; 3,3 ; 4,7 ; 6,8 µF) et calcule le délai obtenu.")
    ANS("Il faut $C\\geq\\f{\\tau}{R}=\\f{40\\u{ ms}}{10\\u{ kΩ}}=4\\u{ µF}$ → on prend 4,7 µF (valeur E6 juste au-dessus). Délai : 10 kΩ × 4,7 µF = 47 ms ≥ 40 ms ✓.", 2)
    Q("c)", "Un collègue propose C = 100 µF « pour être sûr ». Qu'en penses-tu ?")
    ANS("τ = 1 s : l'appareil mettrait une seconde à démarrer, ce qui est inutilement lent, avec un condensateur plus gros et plus cher. On dimensionne juste au-dessus du besoin.", 2)

    # ---- N°6 Oscilloscope
    HR(); EX(6, "Mesurer τ à l'oscilloscope", "Méthode : diapositive 4",
       "au laboratoire, le marquage d'un condensateur est illisible. On le monte avec une résistance connue de 1 kΩ, on alimente le circuit par un signal carré de 0 à 5 V et on relève u_{C} à l'oscilloscope.")
    PIC("fig_oscillo_ex_corr.png" if corr else "fig_oscillo_ex.png", 12.5, keep=True)
    Q("a)", "Lis la tension finale U (nombre de divisions × calibre).")
    ANS("5 div × 1 V/div = 5 V.", 1)
    Q("b)", "Calcule 63 % de U et repère ce niveau sur l'écran.")
    ANS("0,632 × 5 V = 3,16 V, soit environ 3,2 div au-dessus de la masse.", 1)
    Q("c)", "Lis le temps entre le début de la charge et le point à 63 %. Déduis τ.")
    ANS("Environ 2,35 div × 2 ms/div = 4,7 ms → τ ≈ 4,7 ms.", 1)
    Q("d)", "Calcule C. À quelle valeur normalisée correspond-elle ?")
    ANS("$C=\\f{\\tau}{R}=\\f{4,7\\u{ ms}}{1\\u{ kΩ}}=4,7\\u{ µF}$ : valeur normalisée 4,7 µF.", 1)
    Q("e)", "Quelle base de temps faut-il au minimum pour voir toute la charge (5τ) sur les 10 divisions ? Choisis dans la suite 1, 2, 5 des calibres.")
    ANS("5τ = 23,5 ms → 23,5 ms / 10 div = 2,35 ms/div au minimum → on règle 5 ms/div.", 2)

    # ---- N°7 Supercondensateur
    HR(); EX(7, "Situation professionnelle : sauvegarde par supercondensateur", None,
       "un enregistreur de données garde son horloge à l'heure pendant une coupure grâce à un supercondensateur de 1 F. Celui-ci est chargé sous 5 V à travers une résistance de 10 Ω.")
    Q("a)", "Calcule τ et la durée de charge complète.")
    ANS("τ = 10 Ω × 1 F = 10 s ; charge complète après 5τ = 50 s.", 1)
    Q("b)", "Calcule le courant au moment de la mise sous tension.")
    ANS("$I_{0}=\\f{U}{R}=\\f{5\\u{ V}}{10\\u{ Ω}}=0,5\\u{ A}$", 1)
    Q("c)", "À t = 0, quelle puissance dissipe la résistance ? Le plan prévoit une résistance de 0,25 W : est-ce acceptable ?")
    ANS("À t = 0, u_{R} = 5 V : P = U · I_{0} = 5 V × 0,5 A = 2,5 W. C'est 10 fois trop pour une résistance de 0,25 W : elle chaufferait au démarrage et risquerait de griller.", 2)
    Q("d)", "Propose une correction et indique ce qu'elle change pour la durée de charge.")
    ANS("Avec R = 100 Ω : I_{0} = 50 mA et P = 0,25 W, au départ seulement. C'est la limite, on choisit donc une résistance de 0,5 W par sécurité. En contrepartie, τ = 100 s et la charge complète prend environ 8 min, ce qui reste acceptable pour une sauvegarde.", 3)

    # ---- N°8 Mélange
    HR(); EX(8, "Exercice mélangé (révision une semaine plus tard, sans la fiche)", None)
    Q("a)", "R = 4,7 kΩ, C = 10 µF : calcule τ et la durée de charge.")
    ANS("τ = 4,7·10^{3} Ω × 10·10^{−6} F = 47 ms ; charge complète ≈ 5τ = 235 ms.", 1)
    Q("b)", "U = 24 V. Que vaut u_{C} après 3τ ?")
    ANS("95 % de 24 V = 22,8 V.", 1)
    Q("c)", "Vrai ou faux ? Justifie. « Si on augmente R, le condensateur se charge plus vite. »")
    ANS("Faux : τ = R · C augmente, la charge est plus lente (le courant est plus faible).", 1)
    Q("d)", "Vrai ou faux ? Justifie. « Un condensateur chargé en continu laisse passer le courant. »")
    ANS("Faux : une fois chargé, i = 0 ; il se comporte comme un circuit ouvert.", 1)
    Q("e)", "Auto-évaluation : pour chaque objectif, note ✓ (je sais seul·e), ~ (avec la fiche) ou ✗ (à revoir).")
    TABLE([TW / 4 - 0.01] * 4, [["u_{C} et i pendant la charge", "Calcul de τ et 5τ", "u_{C} à un instant t", "Mesure de τ à l'oscilloscope"], ["", "", "", ""]],
          height=0.8, size=10, first_left=False)

    last = [e for e in body if e.tag == qn("w:p")]
    if last and not "".join(last[-1].itertext()).strip() and last[-1].getnext() is not None and last[-1].getnext().tag == qn("w:sectPr"):
        # Word exige un paragraphe après un tableau final : on le réduit à 1 pt pour éviter une page blanche
        pf = d.paragraphs[-1].paragraph_format
        pf.space_before = Pt(0); pf.space_after = Pt(0); pf.line_spacing = Pt(1)
        d.paragraphs[-1].add_run("").font.size = Pt(1)
        pPr = last[-1].get_or_add_pPr(); rp = OxmlElement("w:rPr"); sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "2"); rp.append(sz); pPr.append(rp)
    for part in (d.element, sec.header._element, sec.footer._element): reorder(part)
    z = d.settings.element.find(qn("w:zoom"))
    if z is not None: z.set(qn("w:percent"), "100")
    d.save(out); print("ok", out)


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    build(False, f"out/EX {SHORT}.docx")
    build(True, f"out/EX C {SHORT}.docx")
