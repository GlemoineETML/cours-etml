# -*- coding: utf-8 -*-
"""Feuille d'exercices + corrigé « Le courant alternatif triphasé » (4e année CFC, XLO4).
Part du modèle ETML Rapport_Simple.dotx (etml_base.docx, voir prep_modele.py) : police, styles, logo, en-tête, pied de page.
Couleurs ETML (marine 242852, bleu 297FD5, bleu clair ACCBF9). Réponses en rouge EE0000 dans le corrigé, lignes vides pour l'apprenti.
Formules en équations Word natives (OMML, mathml.py). Dates à l'américaine. Éditeur : Gaël Lemoine. Symboles CEI 60617 / CEI 60027.
Tous les résultats viennent de calc_triphase.py."""
import os, re, datetime as dt
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree
from mathml import omath
from calc_triphase import R as V, fr

RED = RGBColor(0xEE, 0x00, 0x00)
GREY = RGBColor(0x5A, 0x64, 0x78)
NAVY = RGBColor(0x24, 0x28, 0x52)
HEX_NAVY, HEX_BLUE, HEX_LBLUE = "242852", "297FD5", "ACCBF9"
BASE = "etml_base.docx"
MATIERE = "Électrotechnique – triphasé"
CLASSE, ANNEE, CHAMP = "XLO4", "2026-2027", "Programme de la dernière ligne droite"
EDITEUR = "Gaël Lemoine"
TITLE = "Le courant alternatif triphasé"
SHORT = "Courant alternatif triphasé"
FASC = "https://eduvaud.sharepoint.com/:b:/r/sites/msteams_76c9d9/Documents%20partages/Documentation/Electrotechnique%20ELEC/FET%20Electrotechnique%203/ElectrotechniqueFascicule03_V2014_opt.pdf?d=w58dfaaa0153748aa92aceeae8e494206&csf=1&web=1&e=AtwPZK"
TW = 21.0 - 2.0 - 1.5
US = "%m/%d/%Y"


def f0(x): return fr(x, 0)
def f1(x): return fr(x, 1)
def f2(x): return fr(x, 2)


# ------------------------------------------------------------------ briques XML (reprises de build_doc_charge_rc.py)
def p_border(p, sides, sz=4, color=HEX_BLUE):
    pPr = p._p.get_or_add_pPr()
    bd = pPr.find(qn("w:pBdr"))
    if bd is None: bd = OxmlElement("w:pBdr"); pPr.append(bd)
    for sd in sides:
        e = OxmlElement(f"w:{sd}")
        for k, v in (("val", "single"), ("sz", sz), ("space", 4), ("color", color)): e.set(qn(f"w:{k}"), str(v))
        bd.append(e)


def hyperlink(p, url, text, size=None):
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
        if t.text == "Nom -": t.text = f"Triphasé · {kind} · Électrotechnique"
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
    P(f"Feuille d'exercices · {MATIERE} · Classe {CLASSE} · {ANNEE} · {CHAMP}", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, after=2)
    P(f"Éditeur : {EDITEUR} · {now.strftime(US)}", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=10, color=GREY, after=8)
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.paragraph_format.space_after = Pt(0)
    r = p.add_run("Corrigé" if corr else "Version apprenti·e"); r.bold = True
    if corr: r.font.color.rgb = RED
    p.add_run("\tNom :")
    p = d.add_paragraph(); p.paragraph_format.tab_stops.add_tab_stop(Cm(11.5)); p.add_run("\tDate :")
    p_border(p, ["bottom"], 4)

    if corr:
        BOX(["Plan de séance (enseignant·e) : 2 × 45 min d'exercices après la présentation",
             "N°1 à N°3 en classe (plaque signalétique, tensions, borne de recharge). N°4 à N°7 en binôme : ce sont des situations de dépannage, faire verbaliser le diagnostic avant le calcul. N°8 et N°9 en autonomie (compensation, chute de tension). N°10 est l'exercice mélangé de révision : le donner une semaine plus tard, en début de cours, sans la fiche.",
             "Différenciation : les encadrés « Si difficulté » proposent une autre explication ; les apprenti·e·s rapides font les questions Bonus.",
             "Exiger à chaque calcul : formule, valeurs avec unités, résultat arrondi raisonnablement, puis contrôle (ordre de grandeur, plaque signalétique, rapport √3)."])

    P("**Conventions :** symboles selon CEI 60617. U = tension réseau (entre deux conducteurs polaires), U_{ph} = tension de phase (entre un conducteur polaire et le neutre), I = courant de ligne, I_{ph} = courant dans un élément du récepteur. Réseau : 3 × 400/230 V – 50 Hz, sauf indication contraire. Écris toujours la formule, le calcul avec les unités, puis le contrôle.", after=4)
    pr_ = P("**Ressource :** ", after=6, size=10); hyperlink(pr_, FASC, "Électrotechnique, fascicule 03, chapitre 11 « Courant alternatif triphasé »", size=10)

    # ================= AIDE-MÉMOIRE
    d.add_heading("Aide-mémoire", level=1)
    TABLE([3.6, TW - 3.6 - 5.2 - 0.02, 5.2], [
        ["Notion", "Formule / règle", "Exemple"],
        ["Tensions", "$U=\\sqrt{3}\\cdot U_{\\u{ph}}$", "400 V = √3 × 231 V"],
        ["Étoile Y", "$U_{\\u{ph}}=\\f{U}{\\sqrt{3}}$ et $I=I_{\\u{ph}}$", "chaque élément sous 230 V"],
        ["Triangle Δ", "$U_{\\u{ph}}=U$ et $I=\\sqrt{3}\\cdot I_{\\u{ph}}$", "chaque élément sous 400 V"],
        ["Puissances (équilibré)", "$P=\\sqrt{3}\\cdot U\\cdot I\\cdot \\u{cos}\\u{ }\\varphi$ ; $Q=\\sqrt{3}\\cdot U\\cdot I\\cdot \\u{sin}\\u{ }\\varphi$ ; $S=\\sqrt{3}\\cdot U\\cdot I$", "Y et Δ : même formule"],
        ["Déséquilibré", "$P=P_{1}+P_{2}+P_{3}$ ; $I_{\\u{N}}=\\sqrt{I_{1}^{2}+I_{2}^{2}+I_{3}^{2}-I_{1}I_{2}-I_{1}I_{3}-I_{2}I_{3}}$", "même cos φ sur les trois phases"],
        ["Compensation", "$Q_{\\u{C}}=P\\cdot(\\u{tan}\\u{ }\\varphi_{1}-\\u{tan}\\u{ }\\varphi_{2})$ ; $C=\\f{Q_{\\u{C1}}}{U^{2}\\cdot \\omega}$", "condensateurs en Δ, Q_{C1} = Q_{C} / 3"],
        ["Chute de tension", "$\\Delta U=\\sqrt{3}\\cdot R_{\\u{c}}\\cdot I$ ; $P_{\\u{l}}=3\\cdot R_{\\u{c}}\\cdot I^{2}$ ; $R_{\\u{c}}=\\f{\\rho\\cdot l}{A}$", "longueur simple, ρ_{Cu} = 0,0175 Ω·mm²/m"],
        ["Ordre de manœuvre", "Déconnecter : L1 → L2 → L3 → N → PE · Connecter : PE → N → L1 → L2 → L3", "le neutre : en dernier, puis en premier"],
    ], height=0.7, size=9.5)

    d.add_heading("Exercices", level=1)

    # ---- N°1 Plaque signalétique
    EX(1, "Lire une plaque signalétique et coupler le moteur", "Méthode : diapositives 4 à 6 · fascicule p. 11.7 à 11.9",
       "tu mets en service un moteur de ventilateur dans un atelier alimenté en 3 × 400/230 V. Avant de raccorder, tu lis sa plaque.")
    PIC("fig_plaque_moteur.png", 8.5, keep=True)
    Q("a)", "Quel couplage dois-tu réaliser ? Justifie.")
    ANS("Étoile Y. La plus petite tension de la plaque (230 V) est celle d'un enroulement. En étoile sur 400 V, chaque enroulement reçoit $U_{\\u{ph}}=\\f{400\\u{ V}}{\\sqrt{3}}=231\\u{ V}$ ✓.", 2)
    Q("b)", "Dessine les barrettes sur la plaque à bornes.")
    PIC("fig_plaque_Y_corr.png" if corr else "fig_plaque_vide.png", 5.0)
    Q("c)", "Calcule la puissance électrique absorbée (la plaque indique la puissance mécanique utile).")
    ANS(f"$P_{{1}}=\\f{{P_{{2}}}}{{\\eta}}=\\f{{4000\\u{{ W}}}}{{0,86}}$ = {f0(V['m_Pabs'])} W ≈ 4,65 kW", 1)
    Q("d)", "Calcule le courant de ligne. Compare avec la plaque.")
    ANS(f"$I=\\f{{P_{{1}}}}{{\\sqrt{{3}}\\cdot U\\cdot \\u{{cos}}\\u{{ }}\\varphi}}=\\f{{4651\\u{{ W}}}}{{\\sqrt{{3}}\\cdot 400\\u{{ V}}\\cdot 0,82}}$ = {f2(V['m_I'])} A. La plaque indique 8,2 A ✓.", 2)
    Q("e)", "Quels sont le courant et la tension d'un enroulement ?")
    ANS(f"En étoile : I_{{ph}} = I = {f2(V['m_I'])} A ; U_{{ph}} = 231 V.", 1)
    Q("f)", "Calcule les puissances apparente et réactive.")
    ANS(f"$S=\\sqrt{{3}}\\cdot U\\cdot I$ = √3 × 400 V × {f2(V['m_I'])} A = {f0(V['m_S'])} VA ≈ 5,67 kVA\nsin φ = 0,572 → $Q=S\\cdot \\u{{sin}}\\u{{ }}\\varphi$ = {f0(V['m_Q'])} var ≈ 3,25 kvar", 2)
    Q("g)", "Un collègue a posé les barrettes en triangle. Que risque le moteur ?")
    ANS("Chaque enroulement reçoit 400 V au lieu de 230 V, soit √3 fois trop. Le courant et l'échauffement augmentent fortement : la protection déclenche ou l'isolation des enroulements brûle.", 2)

    # ---- N°2 Tensions
    HR(); EX(2, "Contrôler les tensions d'un tableau", "Méthode : diapositive 3 · fascicule p. 11.5 et 11.6",
       "avant une mise en service, on contrôle les tensions au multimètre (catégorie CAT III au minimum) sur les bornes d'arrivée du tableau.")
    Q("a)", "Tu mesures 232 V entre L1 et N. Quelle tension attends-tu entre L1 et L2 ?")
    ANS(f"$U=\\sqrt{{3}}\\cdot U_{{\\u{{ph}}}}$ = √3 × 232 V = {f0(V['t_U'])} V", 1)
    Q("b)", "Dans une ferme en bout de ligne, tu mesures 386 V entre deux phases. Que vaut la tension phase-neutre ?")
    ANS(f"$U_{{\\u{{ph}}}}=\\f{{U}}{{\\sqrt{{3}}}}=\\f{{386\\u{{ V}}}}{{\\sqrt{{3}}}}$ = {f0(V['t_Uph'])} V", 1)
    Q("c)", "Le schéma d'une machine indique « 3 × 400 V – 50 Hz » et celui d'une autre « 3 × 400/230 V – 50 Hz ». Combien de conducteurs actifs faut-il dans chaque cas ?")
    ANS("3 × 400 V : trois conducteurs polaires, sans neutre (+ PE). 3 × 400/230 V : trois conducteurs polaires et le neutre (+ PE). La plus grande tension indiquée est la tension réseau.", 2)
    Q("d)", "Donne la couleur des conducteurs L1, L2, L3, N et PE.")
    ANS("L1 brun, L2 noir, L3 gris, N bleu clair, PE vert-jaune.", 1)

    # ---- N°3 Borne de recharge
    HR(); EX(3, "Situation professionnelle : borne de recharge pour voiture électrique", "Méthode : diapositive 6",
       "un client hésite entre une borne monophasée et une borne triphasée pour son garage. Tu dois lui expliquer la différence avec des chiffres. Charges résistives : cos φ = 1.")
    Q("a)", "Calcule le courant par phase d'une borne de 11 kW raccordée en 3 × 400 V.")
    ANS(f"$I=\\f{{P}}{{\\sqrt{{3}}\\cdot U}}=\\f{{11000\\u{{ W}}}}{{\\sqrt{{3}}\\cdot 400\\u{{ V}}}}$ = {f1(V['ve_I11'])} A → protection 16 A", 1)
    Q("b)", "Même question pour une borne de 22 kW.")
    ANS(f"I = {f1(V['ve_I22'])} A → protection 32 A", 1)
    Q("c)", "Quelle puissance obtient-on en monophasé 230 V avec 16 A ?")
    ANS(f"P = 230 V × 16 A = {fr(V['ve_Pmono'] / 1000, 2)} kW", 1)
    Q("d)", "La voiture doit recharger 36 kWh (batterie de 60 kWh, de 20 % à 80 %). Calcule la durée de recharge dans les deux cas (a et c), sans tenir compte des pertes.")
    ANS(f"Monophasé : 36 kWh / 3,68 kW = {f1(V['ve_tmono'])} h. Triphasé : 36 kWh / 11 kW = {f1(V['ve_ttri'])} h.", 2)
    Q("e)", "Explique au client, en deux phrases, pourquoi on obtient trois fois plus de puissance avec le même courant par conducteur.")
    ANS("La borne triphasée utilise trois conducteurs polaires : chacun fournit 230 V × 16 A, comme la prise. Trois phases donnent donc trois fois la puissance d'une seule ($\\sqrt{3}\\cdot 400=3\\cdot 230,9$).", 2)

    # ---- N°4 Dépannage chauffe-eau
    HR(); EX(4, "Dépannage : contrôler les résistances d'un chauffe-eau", "Méthode : diapositives 4 et 8 · fascicule p. 11.22 à 11.24",
       "un chauffe-eau triphasé de 9 kW, couplé en triangle sur 3 × 400 V, chauffe mal. Tu coupes l'alimentation et tu contrôles les éléments à l'ohmmètre.")
    Q("a)", "Calcule le courant de ligne en fonctionnement normal.")
    ANS(f"$I=\\f{{P}}{{\\sqrt{{3}}\\cdot U}}=\\f{{9000\\u{{ W}}}}{{\\sqrt{{3}}\\cdot 400\\u{{ V}}}}$ = {f1(V['c_I'])} A", 1)
    Q("b)", "Calcule le courant dans un élément.")
    ANS(f"$I_{{\\u{{ph}}}}=\\f{{I}}{{\\sqrt{{3}}}}$ = {f2(V['c_Iph'])} A", 1)
    Q("c)", "Calcule la résistance d'un élément.")
    ANS(f"Chaque élément : 3000 W sous 400 V → $R=\\f{{U^{{2}}}}{{P_{{\\u{{R}}}}}}=\\f{{(400\\u{{ V}})^{{2}}}}{{3000\\u{{ W}}}}$ = {f1(V['c_R'])} Ω", 1)
    Q("d)", "Les barrettes sont en place. Quelle valeur l'ohmmètre doit-il afficher entre U1 et V1 si tout est en ordre ?")
    ANS(f"On mesure un élément en parallèle avec les deux autres en série : $R_{{\\u{{mes}}}}=\\f{{R\\cdot 2R}}{{3R}}=\\f{{2}}{{3}}\\cdot R$ = {f1(V['c_Rmes'])} Ω", 2)
    Q("e)", f"Tu mesures : U1-V1 = 107 Ω, V1-W1 = 53 Ω, W1-U1 = 53 Ω. Quel élément est défectueux ? Quelle puissance le chauffe-eau fournit-il encore ?")
    ANS(f"L'élément raccordé entre U1 et V1 (U1-U2) est coupé : entre U1 et V1 on ne mesure plus que les deux autres en série (2R = {f0(V['c_Rdef'])} Ω), et entre les autres bornes un seul élément (R). Il reste deux éléments sous 400 V : P = 2 × 3000 W = {f0(V['c_Pdef'])} W, soit 2/3 de la puissance.", 3)
    BOX(["Si difficulté",
         "Dessine le triangle des trois résistances et barre celle qui est coupée. Entre deux bornes, cherche tous les chemins possibles pour le courant de l'ohmmètre : s'il en reste un seul, tu lis directement sa résistance."])

    # ---- N°5 Répartition des charges
    HR(); EX(5, "Répartir des charges monophasées et calculer le courant de neutre", "Méthode : diapositive 7 · fascicule p. 11.11 à 11.13",
       "dans un petit atelier, les récepteurs monophasés sont branchés entre phase et neutre : L1 un radiateur de 2300 W, L2 un four de 1380 W, L3 l'éclairage, 920 W. Tous sont résistifs et sous 230 V.")
    Q("a)", "Calcule le courant dans chaque conducteur polaire.")
    TABLE([3.0, 4.0, TW - 7.02], [["Phase", "Puissance", "Courant $I=\\f{P}{U_{\\u{ph}}}$"],
                                  ["L1", "2300 W", ("R", "10,0 A")], ["L2", "1380 W", ("R", "6,0 A")], ["L3", "920 W", ("R", "4,0 A")]], height=0.55)
    Q("b)", "Construis le courant de neutre sur la grille (vecteurs bout à bout, décalés de 120°, I_{1} vers le haut). Mesure I_{N}.")
    PIC("fig_IN_ex_corr.png" if corr else "fig_IN_ex.png", 8.0)
    ANS("Le vecteur qui referme la figure mesure environ 2,6 carreaux, soit I_{N} ≈ 5,3 A.", 1)
    Q("c)", "Vérifie par le calcul.")
    ANS(f"$I_{{\\u{{N}}}}=\\sqrt{{10^{{2}}+6^{{2}}+4^{{2}}-10\\cdot 6-10\\cdot 4-6\\cdot 4}}=\\sqrt{{28}}$ = {f2(V['n_IN'])} A", 1)
    Q("d)", "Calcule la puissance active totale.")
    ANS("P = 2300 + 1380 + 920 = 4600 W", 1)
    Q("e)", "Comment l'installateur aurait-il pu réduire le courant de neutre ?")
    ANS("En répartissant les groupes pour que chaque phase porte à peu près la même puissance (environ 1,5 kW chacune). Avec trois phases égales, I_{N} = 0.", 2)

    # ---- N°6 Neutre ouvert
    HR(); EX(6, "Dépannage : un neutre desserré dans le tableau", "Méthode : diapositive 8 · fascicule p. 11.17 et 11.18",
       "une cliente se plaint : quand le radiateur est en marche, la lampe du bureau éclaire très fort puis grille. Dans le tableau, la borne du neutre est desserrée.")
    PIC("fig_neutre_ex.png", 10.0, keep=True)
    Q("a)", "Calcule la résistance du radiateur (2000 W / 230 V) et celle de la lampe (100 W / 230 V).")
    ANS(f"$R=\\f{{U_{{\\u{{ph}}}}^{{2}}}}{{P}}$ : radiateur = 230² / 2000 = {f2(V['nc_Ra'])} Ω ; lampe = 230² / 100 = {f0(V['nc_Rb'])} Ω", 1)
    Q("b)", "Le neutre est ouvert. Calcule le courant et la tension aux bornes de chaque appareil.")
    ANS(f"Les deux appareils sont en série sous 400 V : $I=\\f{{400\\u{{ V}}}}{{26,5\\u{{ Ω}}+529\\u{{ Ω}}}}$ = {fr(V['nc_I'], 3)} A\nU_{{radiateur}} = 26,45 Ω × 0,720 A = {f0(V['nc_Ua'])} V ; U_{{lampe}} = 529 Ω × 0,720 A = {f0(V['nc_Ub'])} V", 3)
    Q("c)", "Explique ce que la cliente a observé.")
    ANS("La lampe reçoit 381 V au lieu de 230 V : elle éclaire trop fort et grille. Le radiateur, sous 19 V, reste presque froid. C'est toujours le petit appareil qui reçoit la surtension.", 2)
    Q("d)", "Donne l'ordre de déconnexion et de connexion des conducteurs pour intervenir sur la ligne.")
    ANS("Déconnecter : L1 → L2 → L3 → N → PE. Connecter : PE → N → L1 → L2 → L3.", 1)
    Q("e)", "Bonus : en schéma TN-C, le neutre et le conducteur de protection forment un seul conducteur PEN. Quel danger supplémentaire une coupure du PEN crée-t-elle ?")
    ANS("Les carcasses métalliques reliées au PEN peuvent se retrouver sous tension : danger d'électrisation pour les personnes.", 1)

    # ---- N°7 Fusible fondu
    HR(); EX(7, "Dépannage : un fusible de ligne a fondu", "Méthode : diapositive 8 · fascicule p. 11.24",
       "un chauffe-eau triphasé comprend trois résistances de 120 Ω couplées en triangle sur 3 × 400 V. Le client dit que l'eau met deux fois plus de temps à chauffer.")
    Q("a)", "Calcule la puissance nominale et le courant de ligne.")
    ANS(f"$P=3\\cdot \\f{{U^{{2}}}}{{R}}=3\\cdot \\f{{(400\\u{{ V}})^{{2}}}}{{120\\u{{ Ω}}}}$ = {f0(V['f_PD'])} W ; $I=\\sqrt{{3}}\\cdot \\f{{400\\u{{ V}}}}{{120\\u{{ Ω}}}}$ = {f2(V['f_ID'])} A", 2)
    Q("b)", "Le fusible de L3 a fondu. Calcule la nouvelle puissance.")
    ANS(f"Entre L1 et L2 : une résistance sous 400 V, en parallèle avec deux résistances en série sous 400 V.\n$P=\\f{{400^{{2}}}}{{120}}+\\f{{400^{{2}}}}{{240}}$ = 1333 + 667 = {f0(V['f_PDcut'])} W, soit la moitié : l'eau chauffe deux fois plus lentement ✓", 3)
    Q("c)", "Quels courants affiche une pince ampèremétrique sur L1, L2 et L3 ? Comment confirmes-tu le diagnostic ?")
    ANS(f"L1 et L2 : 400/120 + 400/240 = {f1(V['f_IDcut'])} A ; L3 : 0 A. En fonctionnement normal on lirait {f2(V['f_ID'])} A sur les trois lignes.", 2)
    Q("d)", "Bonus : les mêmes résistances couplées en étoile. Calcule la puissance normale, puis avec un fil de ligne coupé.")
    ANS(f"$P=3\\cdot \\f{{(231\\u{{ V}})^{{2}}}}{{120\\u{{ Ω}}}}$ = {f0(V['f_PY'])} W ; fil coupé : deux résistances en série sous 400 V → {f0(V['f_PYcut'])} W (la moitié).", 2)

    # ---- N°8 Compensation
    HR(); EX(8, "Situation professionnelle : compenser une menuiserie", "Méthode : diapositive 9 · fascicule p. 11.27 à 11.31",
       "une menuiserie (scies, raboteuse, aspiration) absorbe 48 kW avec cos φ = 0,72 sur 3 × 400 V – 50 Hz. Le distributeur facture l'énergie réactive au-dessous de cos φ = 0,95. On installe une batterie de condensateurs.")
    Q("a)", "Calcule le courant de ligne sans compensation.")
    ANS(f"$I_{{1}}=\\f{{48000\\u{{ W}}}}{{\\sqrt{{3}}\\cdot 400\\u{{ V}}\\cdot 0,72}}$ = {f1(V['k_I1'])} A", 1)
    Q("b)", "Calcule la puissance réactive de la batterie pour atteindre cos φ = 0,95.")
    ANS(f"tan φ_{{1}} = {fr(V['k_t1'], 3)} ; tan φ_{{2}} = {fr(V['k_t2'], 3)}\n$Q_{{\\u{{C}}}}=P\\cdot(\\u{{tan}}\\u{{ }}\\varphi_{{1}}-\\u{{tan}}\\u{{ }}\\varphi_{{2}})$ = 48 kW × ({fr(V['k_t1'], 3)} − {fr(V['k_t2'], 3)}) = {f1(V['k_QC'] / 1000)} kvar", 2)
    Q("c)", "Les trois condensateurs sont couplés en triangle. Sous quelle tension sont-ils ? Calcule la capacité d'un condensateur.")
    ANS(f"En triangle, chaque condensateur est sous 400 V. Q_{{C1}} = {f1(V['k_QC'] / 1000)} / 3 = {f2(V['k_QC1'] / 1000)} kvar\n$C=\\f{{Q_{{\\u{{C1}}}}}}{{U^{{2}}\\cdot \\omega}}=\\f{{{f0(V['k_QC1'])}\\u{{ var}}}}{{(400\\u{{ V}})^{{2}}\\cdot 314\\u{{ s}}^{{-1}}}}$ = {f0(V['k_C'] * 1e6)} µF", 3)
    Q("d)", "Calcule le courant de ligne après compensation. De combien les pertes dans les câbles diminuent-elles ?")
    ANS(f"$I_{{2}}=\\f{{48000\\u{{ W}}}}{{\\sqrt{{3}}\\cdot 400\\u{{ V}}\\cdot 0,95}}$ = {f1(V['k_I2'])} A. Les pertes varient avec I² : ({f1(V['k_I2'])} / {f1(V['k_I1'])})² = {fr((V['k_I2'] / V['k_I1']) ** 2, 2)} → environ {f0(100 - 100 * (V['k_I2'] / V['k_I1']) ** 2)} % de pertes en moins.", 2)
    Q("e)", "Pourquoi la batterie possède-t-elle plusieurs échelons commandés par un régulateur ?")
    ANS("La puissance réactive varie selon les machines en marche. Le régulateur enclenche juste ce qu'il faut, sans rendre l'installation capacitive quand les moteurs s'arrêtent.", 2)

    # ---- N°9 Chute de tension
    HR(); EX(9, "Situation professionnelle : alimenter une pompe éloignée", "Méthode : diapositive 10 · fascicule p. 11.32 et 11.33",
       "une pompe de 7,5 kW (puissance utile), rendement 0,88, cos φ = 0,85, est alimentée en 3 × 400 V par un câble en cuivre de 4 mm², long de 60 m. Le cahier des charges limite la chute de tension à 3 %. ρ_{Cu} = 0,0175 Ω·mm²/m.")
    Q("a)", "Calcule la résistance d'un conducteur polaire.")
    ANS(f"$R_{{\\u{{c}}}}=\\f{{\\rho\\cdot l}}{{A}}=\\f{{0,0175\\cdot 60}}{{4}}$ = {fr(V['d_Rc'], 3)} Ω (longueur simple)", 1)
    Q("b)", "Calcule le courant de ligne.")
    ANS(f"P_{{1}} = 7500 / 0,88 = {f0(V['d_P1'])} W → $I=\\f{{{f0(V['d_P1'])}\\u{{ W}}}}{{\\sqrt{{3}}\\cdot 400\\u{{ V}}\\cdot 0,85}}$ = {f1(V['d_I'])} A", 1)
    Q("c)", "Calcule la chute de tension en volts et en %. Le câble convient-il ?")
    ANS(f"$\\Delta U=\\sqrt{{3}}\\cdot R_{{\\u{{c}}}}\\cdot I$ = √3 × {fr(V['d_Rc'], 3)} Ω × {f1(V['d_I'])} A = {f2(V['d_dU'])} V, soit {f2(V['d_pc'])} % ≤ 3 % : le câble convient.", 2)
    Q("d)", "Calcule la puissance perdue dans la ligne.")
    ANS(f"$P_{{\\u{{l}}}}=3\\cdot R_{{\\u{{c}}}}\\cdot I^{{2}}$ = 3 × {fr(V['d_Rc'], 3)} × {f1(V['d_I'])}² = {f0(V['d_Pl'])} W", 1)
    Q("e)", "Quelle tension faut-il au départ de la ligne pour que la pompe reçoive 400 V ?")
    ANS(f"U_{{1}} ≈ U_{{2}} + ΔU = 400 + {f1(V['d_dU'])} = {f0(V['d_U1'])} V", 1)

    # ---- N°10 Mélange
    HR(); EX(10, "Exercice mélangé (révision une semaine plus tard, sans la fiche)", None)
    Q("a)", "Un four comprend trois résistances de 40 Ω couplées en étoile sur 3 × 400 V. Calcule le courant de ligne et la puissance.")
    ANS(f"U_{{ph}} = 231 V ; I = 231 / 40 = {f2(V['x_IY'])} A ; P = 3 × 231² / 40 = {f0(V['x_PY'])} W", 1)
    Q("b)", "Même four couplé en triangle. Calcule le courant dans un élément, le courant de ligne et la puissance.")
    ANS(f"I_{{ph}} = 400 / 40 = {f0(V['x_Iph'])} A ; I = √3 × 10 = {f1(V['x_ID'])} A ; P = {f0(V['x_PD'])} W (3 fois plus qu'en étoile)", 1)
    Q("c)", "Méthode des deux wattmètres : W1 indique 3,2 kW ; W2 dévie à l'envers et indique 0,6 kW après inversion de son circuit tension. Puissance du récepteur ?")
    ANS("P = 3,2 − 0,6 = 2,6 kW (la lecture inversée se soustrait).", 1)
    Q("d)", "Vrai ou faux ? Justifie. « En triangle, le courant de ligne vaut 3 fois le courant dans un élément. »")
    ANS("Faux : I = √3 · I_{ph}, car les courants s'additionnent vectoriellement (décalage de 120°).", 1)
    Q("e)", "Vrai ou faux ? Justifie. « Pour intervenir sur une ligne, on peut couper le neutre en premier. »")
    ANS("Faux : couper le neutre avant les phases peut mettre des récepteurs sous 400 V. On coupe L1, L2, L3, puis N, puis PE.", 1)
    Q("f)", "Auto-évaluation : pour chaque objectif, note ✓ (je sais seul·e), ~ (avec la fiche) ou ✗ (à revoir).")
    TABLE([TW / 5 - 0.01] * 5, [["U et U_{ph}", "Couplage Y ou Δ", "I, P, Q, S", "Rôle du neutre", "Compensation et chute de tension"], ["", "", "", "", ""]],
          height=0.8, size=9.5, first_left=False)

    last = [e for e in body if e.tag == qn("w:p")]
    if last and not "".join(last[-1].itertext()).strip() and last[-1].getnext() is not None and last[-1].getnext().tag == qn("w:sectPr"):
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
