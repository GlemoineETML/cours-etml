# -*- coding: utf-8 -*-
"""Presentation 'La source reelle et en charge' - gabarit ETML El Dim1."""
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


# =============================================================== 1. TITRE
s = new("title")
title_of(s, "La source réelle et en charge", 40)
sp = s.placeholders[1].text_frame
sp.clear()
fill(sp.paragraphs[0], "El Dim1 – Notions de base · 2 périodes", 20, NAVY)
textbox(s, Inches(0.75), Inches(5.22), Inches(5.0), Inches(0.4),
        [("Version : 08.2026 / 1.0", 11, GREY, False)])
notes(s, "Chapitre : source de tension idéale vs réelle, résistance interne, "
         "comportement en charge. Objectifs LZ 4147, LZ 1915, LZ 1908.")

# =============================================================== 2. OBJECTIFS
s = new()
title_of(s, "Ce que tu sauras faire à la fin")
body_of(s, [
    (0, "Distinguer une source de tension idéale d’une source réelle", {"space": 10}),
    (0, "Expliquer le rôle de la résistance interne R_{i}", {"space": 10}),
    (0, "Calculer la tension aux bornes en charge : U = U_{0} − R_{i} · I", {"space": 10}),
    (0, "Tracer et exploiter la caractéristique U(I) d’une source", {"space": 10}),
    (0, "Déterminer R_{i} à partir de deux points de mesure", {"space": 10}),
], box=(Inches(0.51), Inches(1.48), Inches(8.33), Inches(3.3)))
textbox(s, Inches(0.51), Inches(4.95), Inches(8.33), Inches(0.5),
        [("Objectifs évaluateurs : LZ 4147 · LZ 1915 · LZ 1908", 15, GREY, True)])
notes(s, "Annoncer les objectifs et les garder visibles. Vérifier en fin de 2e période "
         "que chacun est atteint (auto-évaluation à main levée).")

# =============================================================== 3. ACCROCHE
s = new()
title_of(s, "Pourquoi les phares pâlissent au démarrage ?")
body_of(s, [
    (0, "Moteur à l’arrêt, phares allumés : le voltmètre sur la batterie indique 12,6 V.",
     {"nobullet": True, "size": 20, "space": 14}),
    (0, "Tu tournes la clé. Pendant que le démarreur tourne, les phares faiblissent "
        "nettement et le voltmètre tombe à 10,8 V.",
     {"nobullet": True, "size": 20, "space": 24}),
    (0, "La batterie est neuve. Alors, où sont passés les 1,8 V ?",
     {"nobullet": True, "size": 24, "bold": True, "color": RED}),
], box=(Inches(0.7), Inches(1.85), Inches(7.9), Inches(3.5)))
notes(s, "PRÉDIRE avant d’expliquer. 2 minutes : chaque élève écrit son hypothèse, "
         "on en relève trois ou quatre au tableau sans trancher. On y revient en fin "
         "de 1re période (diapositive 11). Ne pas donner la réponse ici.")

# =============================================================== 4. SOURCE IDEALE
s = new()
title_of(s, "La source de tension idéale")
body_of(s, [
    (0, "Elle garde U = U_{0} quel que soit le courant demandé"),
    (0, "Sa résistance interne est nulle : R_{i} = 0 Ω"),
    (0, "Elle peut débiter un courant infini"),
    (0, "Elle n’existe pas : c’est un modèle", {"bold": True, "color": RED}),
], box=(Inches(0.51), Inches(1.60), Inches(3.75), Inches(3.9)), sizes=(18, 16))
picture(s, "01_source_ideale.png", Inches(4.35), Inches(1.75), Inches(4.45), Inches(3.4))
notes(s, "Insister sur le mot MODÈLE : un outil de calcul, pas un objet. "
         "Rappeler le symbole CEI : cercle traversé d’un trait parallèle aux bornes.")

# =============================================================== 5. CONFRONTATION
s = new()
title_of(s, "Mais la mesure dit autre chose…")
body_of(s, [
    (0, "Pile AA neuve, voltmètre seul (à vide) :  U = 1,50 V", {"space": 12}),
    (0, "La même pile qui alimente une lampe :  U = 1,20 V", {"space": 12}),
    (0, "Écart : 0,30 V — et il grandit si la lampe consomme plus",
     {"space": 20, "bold": True, "color": RED}),
    (0, "Le modèle de la source idéale ne l’explique pas.",
     {"nobullet": True, "size": 21, "space": 6}),
    (0, "Il manque quelque chose à l’intérieur de la source.",
     {"nobullet": True, "size": 21, "bold": True}),
], box=(Inches(0.51), Inches(1.70), Inches(8.33), Inches(3.7)))
notes(s, "Conflit cognitif : la mesure contredit le modèle qu’on vient de poser. "
         "C’est le moteur de la suite. Si le matériel est là, faire la mesure en direct : "
         "pile + voltmètre, puis pile + lampe + voltmètre.")

# =============================================================== 6. ANALOGIE
s = new()
title_of(s, "L’analogie du réservoir")
picture(s, "03_analogie.png", Inches(0.9), Inches(1.45), Inches(7.5), Inches(3.1))
body_of(s, [
    (0, "Sans débit, la pression de sortie est maximale : c’est U_{0}", {"space": 6}),
    (0, "Dès qu’on tire du débit, l’étranglement interne fait chuter la pression disponible"),
], box=(Inches(0.51), Inches(4.60), Inches(8.33), Inches(1.15)), sizes=(17, 15))
notes(s, "Limite de l’analogie à dire à voix haute : l’eau finit par manquer, "
         "alors qu’on suppose ici U_0 constante. L’analogie explique la CHUTE, pas la décharge.")

# =============================================================== 7. MODELE REEL
s = new()
title_of(s, "Le modèle de la source réelle")
body_of(s, [
    (0, "Une source réelle = une source idéale U_{0} EN SÉRIE avec une résistance R_{i}",
     {"size": 18, "space": 4}),
    (0, "R_{i} n’est pas un composant qu’on peut souder : elle modélise tout ce qui freine "
        "le courant à l’intérieur (électrolyte, contacts, bobinages)", {"size": 16}),
], box=(Inches(0.51), Inches(1.42), Inches(8.33), Inches(1.05)))
picture(s, "02_source_reelle.png", Inches(0.9), Inches(2.45), Inches(7.5), Inches(3.3))
notes(s, "Le cadre pointillé est capital : on ne peut PAS accéder au point entre U_0 et R_i. "
         "On ne mesure que ce qui sort en A et B.")

# =============================================================== 8. EQUATION
s = new()
title_of(s, "L’équation à retenir")
tb = textbox(s, Inches(0.51), Inches(1.55), Inches(8.33), Inches(0.9),
             [("U = U_{0} − R_{i} · I", 40, NAVY, True)], align=PP_ALIGN.CENTER)
body_of(s, [
    (0, "U [V] — tension aux bornes, en charge : ce que lit le voltmètre", {"space": 8}),
    (0, "U_{0} [V] — tension à vide, sans charge branchée", {"space": 8}),
    (0, "R_{i} [Ω] — résistance interne de la source", {"space": 8}),
    (0, "I [A] — courant débité par la source", {"space": 14}),
    (0, "R_{i} · I  est la chute de tension interne : ce que la source perd chez elle",
     {"bold": True, "color": RED, "size": 18}),
], box=(Inches(0.9), Inches(2.75), Inches(7.6), Inches(2.9)), sizes=(18, 16))
notes(s, "Faire écrire la formule dans le formulaire personnel. Vérifier les unités. "
         "Faire remarquer le signe MOINS : la source ne peut que perdre de la tension.")

# =============================================================== 9. EXEMPLE RESOLU
s = new()
title_of(s, "Exemple résolu")
body_of(s, [
    (0, "Pile : U_{0} = 6 V et R_{i} = 1 Ω. Lampe : R = 5 Ω.",
     {"nobullet": True, "bold": True, "space": 12, "size": 19}),
    (0, "1.  Circuit série → I = U_{0} / (R_{i} + R) = 6 / 6 = 1 A",
     {"nobullet": True, "space": 10, "size": 19}),
    (0, "2.  U = U_{0} − R_{i} · I = 6 − 1 · 1 = 5,0 V",
     {"nobullet": True, "space": 10, "size": 19}),
    (0, "3.  Chute interne = R_{i} · I = 1,0 V   (17 % de U_{0} !)",
     {"nobullet": True, "space": 14, "size": 19}),
    (0, "Contrôle : 5,0 V + 1,0 V = 6,0 V = U_{0} ✓",
     {"nobullet": True, "bold": True, "color": BLUE, "size": 18}),
], box=(Inches(0.7), Inches(1.60), Inches(8.0), Inches(4.0)))
notes(s, "Dérouler au tableau en même temps, en verbalisant chaque étape. "
         "L’étape 3 (contrôle) est la plus importante : elle donne un moyen de vérifier seul.")

# =============================================================== 10. A TOI
s = new()
title_of(s, "À toi de compléter")
body_of(s, [
    (0, "Même pile : U_{0} = 6 V, R_{i} = 1 Ω. Cette fois la lampe vaut R = 2 Ω.",
     {"nobullet": True, "bold": True, "space": 16, "size": 19}),
    (0, "1.  I = ……… A", {"nobullet": True, "space": 12, "size": 19}),
    (0, "2.  U = ……… V", {"nobullet": True, "space": 12, "size": 19}),
    (0, "3.  Chute interne = ……… V", {"nobullet": True, "space": 16, "size": 19}),
    (0, "Que constates-tu par rapport à l’exemple précédent ?",
     {"nobullet": True, "bold": True, "color": RED, "size": 18}),
], box=(Inches(0.7), Inches(1.60), Inches(8.0), Inches(4.0)))
notes(s, "3 minutes, en binôme, puis correction collective.\n"
         "Corrigé : I = 6 / 3 = 2 A ; U = 6 − 1·2 = 4,0 V ; chute = 2,0 V.\n"
         "Constat attendu : plus la charge tire de courant, plus la tension de sortie chute. "
         "C’est la réponse à la question des phares. FIN DE LA 1re PÉRIODE.")

# =============================================================== 11. RETOUR ACCROCHE
s = new()
title_of(s, "Retour sur les phares")
picture(s, "09_batterie.png", Inches(0.65), Inches(1.32), Inches(8.05), Inches(2.85))
body_of(s, [
    (0, "Batterie neuve : U_{0} = 12,6 V et R_{i} = 0,01 Ω. Le démarreur tire 180 A.",
     {"nobullet": True, "size": 17, "space": 8}),
    (0, "U = 12,6 − 0,01 · 180 = 12,6 − 1,8 = 10,8 V",
     {"nobullet": True, "size": 20, "bold": True, "color": BLUE, "space": 8}),
    (0, "Les 1,8 V manquants sont perdus DANS la batterie. Les phares, branchés sur "
        "10,8 V au lieu de 12,6 V, éclairent moins.",
     {"nobullet": True, "size": 16}),
], box=(Inches(0.6), Inches(4.25), Inches(8.1), Inches(1.55)))
notes(s, "Reprendre les hypothèses notées au tableau à la diapositive 3 et les valider "
         "ou les écarter une par une. Fin de la 1re période.")

# =============================================================== 12. RAPPEL ECLAIR
s = new()
title_of(s, "Rappel éclair — sans les notes")
body_of(s, [
    (0, "Que vaut R_{i} pour une source idéale ?", {"space": 18, "size": 21}),
    (0, "Écris la relation entre U, U_{0}, R_{i} et I", {"space": 18, "size": 21}),
    (0, "La charge tire plus de courant : la tension aux bornes monte ou descend ?",
     {"space": 18, "size": 21}),
], box=(Inches(0.7), Inches(1.85), Inches(8.0), Inches(3.4)))
notes(s, "2 minutes, cahier fermé, réponse écrite. La récupération en mémoire (retrieval) "
         "fixe bien mieux que la relecture. Correction rapide à l’oral, sans noter.")

# =============================================================== 13. CARACTERISTIQUE
s = new()
title_of(s, "La caractéristique U(I) de la source")
picture(s, "04_caracteristique.png", Inches(0.5), Inches(1.45), Inches(5.75), Inches(4.3))
body_of(s, [
    (0, "À vide :", {"size": 16, "space": 1, "bold": True}),
    (1, "U = U_{0}", {"size": 16, "space": 14}),
    (0, "En court-circuit :", {"size": 16, "space": 1, "bold": True}),
    (1, "I_{cc} = U_{0} / R_{i}", {"size": 16, "space": 14}),
    (0, "Pente :", {"size": 16, "space": 1, "bold": True}),
    (1, "−R_{i}", {"size": 16, "space": 16}),
    (0, "Plus la pente est raide,", {"size": 15, "space": 1, "color": RED, "bold": True}),
    (0, "plus R_{i} est grande", {"size": 15, "color": RED, "bold": True, "nobullet": True}),
], box=(Inches(6.35), Inches(1.70), Inches(2.45), Inches(3.9)))
notes(s, "Faire lire le graphique dans les deux sens : donner un I et lire U, puis l’inverse. "
         "Le point de fonctionnement est fixé par la charge branchée.")

# =============================================================== 14. COURT-CIRCUIT
s = new()
title_of(s, "Court-circuit : pourquoi c’est dangereux")
body_of(s, [
    (0, "I_{cc} = U_{0} / R_{i} — une petite R_{i} donne un courant énorme",
     {"space": 14, "size": 19}),
    (0, "Batterie 12 V avec R_{i} = 0,01 Ω  →  I_{cc} = 1200 A",
     {"space": 14, "size": 19, "bold": True, "color": RED}),
    (0, "Conséquences : conducteurs qui fondent, arc électrique, projections, brûlures",
     {"space": 14, "size": 18}),
    (0, "En atelier : jamais d’outil métallique en travers des bornes, "
        "protection par fusible dimensionné", {"size": 18}),
], box=(Inches(0.6), Inches(1.70), Inches(8.1), Inches(3.8)))
notes(s, "Lien direct avec les règles de sécurité du labo. Montrer une bague ou un tournevis : "
         "c’est le scénario réel d’accident sur batterie.")

# =============================================================== 15. DURE / MOLLE
s = new()
title_of(s, "Source dure ou source molle")
picture(s, "05_dure_molle.png", Inches(0.55), Inches(1.42), Inches(8.25), Inches(3.55))
body_of(s, [
    (0, "R_{i} faible → source dure : la tension tient sous charge (alimentation de labo)",
     {"size": 16, "space": 6}),
    (0, "R_{i} élevée → source molle : la tension s’effondre dès qu’on tire du courant "
        "(pile usée)", {"size": 16}),
], box=(Inches(0.51), Inches(5.00), Inches(8.33), Inches(0.85)))
notes(s, "Une pile qui vieillit ne perd presque pas de U_0 : c’est R_i qui augmente. "
         "C’est pour ça qu’un contrôle de pile au voltmètre seul ne veut rien dire.")

# =============================================================== 16. MESURER Ri
s = new()
title_of(s, "Mesurer la résistance interne")
picture(s, "06_mesure_ri.png", Inches(0.5), Inches(1.50), Inches(5.55), Inches(3.3))
body_of(s, [
    (0, "Deux points de mesure (U_{1} ; I_{1}) et (U_{2} ; I_{2})",
     {"size": 16, "space": 10}),
    (0, "R_{i} = ΔU / ΔI", {"size": 22, "bold": True, "space": 10}),
    (0, "Exemple : 9,0 V à 0 A puis 8,4 V à 2 A", {"size": 15, "space": 6}),
    (0, "R_{i} = 0,6 / 2 = 0,3 Ω", {"size": 17, "bold": True, "color": BLUE}),
], box=(Inches(6.15), Inches(1.80), Inches(2.65), Inches(3.5)))
notes(s, "Méthode utilisée en labo TM. Attention : mesurer vite sur une pile, "
         "sinon elle chauffe et R_i change. Le voltmètre se met AUX BORNES, "
         "l’ampèremètre EN SÉRIE.")

# =============================================================== 17. PIEGES
s = new()
title_of(s, "Les quatre pièges classiques")
body_of(s, [
    (0, "Confondre U_{0} (à vide) et U (en charge) : ce ne sont pas les mêmes valeurs",
     {"space": 14, "size": 18}),
    (0, "Croire que R_{i} est une résistance qu’on pourrait dessouder",
     {"space": 14, "size": 18}),
    (0, "Juger une pile au voltmètre à vide : une pile morte affiche encore presque U_{0}",
     {"space": 14, "size": 18}),
    (0, "Oublier que R_{i} augmente quand la pile vieillit ou refroidit",
     {"size": 18}),
], box=(Inches(0.6), Inches(1.70), Inches(8.1), Inches(3.8)))
notes(s, "Ces quatre erreurs sont celles qui reviennent aux TE. Les faire noter dans le "
         "formulaire personnel.")

# =============================================================== 18. SYMBOLES
s = new()
title_of(s, "Symboles CEI utilisés")
picture(s, "07_symboles_cei.png", Inches(0.6), Inches(1.60), Inches(8.15), Inches(3.4))
textbox(s, Inches(0.6), Inches(5.15), Inches(8.15), Inches(0.5),
        [("Flèche de tension : elle pointe du + vers le −", 15, GREY, True)])
notes(s, "Rappeler qu’aux TE seuls les symboles CEI sont acceptés. "
         "Ne pas utiliser le zigzag américain pour la résistance.")

# =============================================================== 19. SYNTHESE
s = new()
title_of(s, "L’essentiel en cinq lignes")
body_of(s, [
    (0, "Source idéale : R_{i} = 0 Ω, donc U = U_{0} en toutes circonstances", {"space": 13}),
    (0, "Source réelle : U = U_{0} − R_{i} · I", {"space": 13, "bold": True}),
    (0, "Court-circuit : I_{cc} = U_{0} / R_{i}", {"space": 13}),
    (0, "Caractéristique : une droite, ordonnée à l’origine U_{0}, pente −R_{i}", {"space": 13}),
    (0, "Mesure : R_{i} = ΔU / ΔI sur deux points", {"space": 13}),
], box=(Inches(0.6), Inches(1.75), Inches(8.1), Inches(3.6)), sizes=(19, 17))
notes(s, "Faire reformuler par deux élèves avant d’afficher les lignes une à une. "
         "Ces cinq lignes vont au formulaire.")

# =============================================================== 20. EXERCICES
s = new()
title_of(s, "À vous : fiche 210 EX")
body_of(s, [
    (0, "Six exercices, du plus simple au plus complet", {"space": 12}),
    (0, "Matériel : formulaire, calculatrice, règle pour le tracé", {"space": 12}),
    (0, "L’exercice 5 se fait sur le quadrillage fourni", {"space": 12}),
    (0, "L’exercice 6 est une situation d’atelier : justifie ta conclusion en une phrase",
     {"space": 12}),
], box=(Inches(0.6), Inches(1.80), Inches(8.1), Inches(3.2)))
notes(s, "Circuler et repérer qui bloque sur le passage 'circuit série' de l’exercice 3. "
         "Correction : distribuer le corrigé ou projeter.")

import os
os.makedirs("out", exist_ok=True)
prs.save(OUT)
print("saved", OUT, len(prs.slides.__iter__.__self__._sldIdLst), "slides")
