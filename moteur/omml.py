# -*- coding: utf-8 -*-
"""Équations natives éditables (OMML) à partir d'une mini-syntaxe LaTeX (REGLES 3.2).
Fusion de mathml.py et mathml_w1.py.

Syntaxe :
  \\f{num}{den}   fraction            \\sqrt{x}   racine carrée        \\bar{x}   barre de négation (logique)
  x_{i}  indice (en romain : indice descriptif, REGLES 3.1)            x^{2}  exposant
  \\u{texte}      texte droit (unités, mots ; ses espaces deviennent insécables)
  \\cdot \\oplus \\approx \\le …  symboles
Lettres : une lettre = une variable, en italique (A, B, U, R…). Lettres grecques minuscules en italique (variables), sauf µ et π.
sin, cos, tan, ln, log, exp : en romain."""
from html import escape

SYM = {"\\cdot": "·", "\\approx": "≈", "\\Delta": "Δ", "\\ohm": "Ω",
       "\\times": "×", "\\pm": "±", "\\infty": "∞", "\\to": "→",
       "\\ne": "≠", "\\le": "≤", "\\ge": "≥", "\\neq": "≠", "\\leq": "≤", "\\geq": "≥",
       "\\tau": "τ", "\\mu": "µ", "\\varepsilon": "ε", "\\epsilon": "ε",
       "\\Omega": "Ω", "\\pi": "π", "\\alpha": "α", "\\beta": "β",
       "\\Rightarrow": "⇒", "\\varphi": "φ", "\\omega": "ω", "\\eta": "η", "\\rho": "ρ", "\\oplus": "⊕"}
ITALIQUE = {"\\tau", "\\varepsilon", "\\epsilon", "\\alpha", "\\beta", "\\varphi", "\\omega", "\\eta", "\\rho"}
FONCTIONS = ("sin", "cos", "tan", "ln", "log", "exp")
_SYM_TRIES = sorted(SYM.items(), key=lambda kv: -len(kv[0]))


_CIBLE = ["docx"]      # « docx » (w:rPr, taille en demi-points) ou « pptx » (a:rPr, taille en centièmes de point)


def _arpr(color, sz, italic):
    a = '<a:rPr lang="fr-CH" i="%d"%s>' % (1 if italic else 0, ' sz="%d"' % sz if sz else "")
    if color: a += '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>' % color
    return a + '<a:latin typeface="Cambria Math" panose="02040503050406030204" pitchFamily="18" charset="0"/></a:rPr>'


def _rpr(color, sz, italic, nor=False):
    sty = '<m:rPr>%s<m:sty m:val="%s"/></m:rPr>' % ("<m:nor/>" if nor else "", "i" if italic else "p")
    if _CIBLE[0] == "pptx":
        return sty + _arpr(color, sz, italic)
    w = '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
    if color: w += '<w:color w:val="%s"/>' % color
    if sz: w += '<w:sz w:val="%d"/>' % sz
    return sty + w + "</w:rPr>"


def _run(txt, color, sz, italic, nor=False):
    return "<m:r>%s<m:t xml:space=\"preserve\">%s</m:t></m:r>" % (_rpr(color, sz, italic, nor), escape(txt, quote=False))


def _ctrl(color, sz):
    if _CIBLE[0] == "pptx":
        return "<m:ctrlPr>%s</m:ctrlPr>" % _arpr(color, sz, True)
    w = '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
    if color: w += '<w:color w:val="%s"/>' % color
    if sz: w += '<w:sz w:val="%d"/>' % sz
    return "<m:ctrlPr>%s</w:rPr></m:ctrlPr>" % w


def _brace(src, i):
    assert src[i] == "{", src[i:i + 20]
    depth, j = 0, i
    while j < len(src):
        if src[j] == "{": depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0: return src[i + 1:j], j + 1
        j += 1
    raise ValueError("accolade non fermée : " + src[i:i + 30])


def _fonction(src, i):
    """Nom de fonction (sin, ln…) qui commence en i et n'est pas suivi d'une autre lettre."""
    for f in FONCTIONS:
        if src.startswith(f, i) and (i + len(f) == len(src) or not src[i + len(f)].isalpha()) and (i == 0 or not src[i - 1].isalpha()):
            return f
    return None


def _parse(src, color, sz, up=False):
    """up = True dans un indice : les lettres y sont droites (indices descriptifs)."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith("\\bar{", i):
            arg, j = _brace(src, i + 4)
            out.append('<m:bar><m:barPr><m:pos m:val="top"/>%s</m:barPr><m:e>%s</m:e></m:bar>' % (_ctrl(color, sz), _parse(arg, color, sz, up)))
            i = j; continue
        if src.startswith("\\f{", i):
            num, j = _brace(src, i + 2); den, j = _brace(src, j)
            out.append("<m:f><m:fPr>%s</m:fPr><m:num>%s</m:num><m:den>%s</m:den></m:f>"
                       % (_ctrl(color, sz), _parse(num, color, sz), _parse(den, color, sz)))
            i = j; continue
        if src.startswith("\\sqrt{", i):
            arg, j = _brace(src, i + 5)
            out.append('<m:rad><m:radPr><m:degHide m:val="1"/>%s</m:radPr><m:deg/><m:e>%s</m:e></m:rad>'
                       % (_ctrl(color, sz), _parse(arg, color, sz, up)))
            i = j; continue
        if src.startswith("\\u{", i):
            txt, j = _brace(src, i + 2)
            out.append(_run(txt.replace(" ", "\u00a0"), color, sz, False, nor=True)); i = j; continue   # \u{ ns} : espace insécable avant l'unité
        hit = None
        for k, v in _SYM_TRIES:
            if src.startswith(k, i): hit = (k, v); break
        if hit:
            out.append(_run(hit[1], color, sz, hit[0] in ITALIQUE and not up))
            i += len(hit[0]); continue
        if c in "_^" and i + 1 < n and src[i + 1] == "{":
            grp, j = _brace(src, i + 1)
            base = out.pop() if out else _run("", color, sz, False)
            tag, part = ("m:sSub", "m:sub") if c == "_" else ("m:sSup", "m:sup")
            out.append("<%s><%sPr>%s</%sPr><m:e>%s</m:e><%s>%s</%s></%s>"
                       % (tag, tag, _ctrl(color, sz), tag, base, part, _parse(grp, color, sz, up=(c == "_")), part, tag))
            i = j; continue
        if c.isalpha():
            f = _fonction(src, i)
            if f:
                out.append(_run(f, color, sz, False)); i += len(f); continue
            # une lettre = une variable (A, B, Y…) : runs séparés pour que la barre ne couvre que ce qu'il faut
            out.append(_run(c, color, sz, not up)); i += 1; continue
        j = i
        while j < n and not src[j].isalpha() and src[j] not in "_^\\": j += 1
        if j == i: j = i + 1
        out.append(_run(src[i:j], color, sz, False)); i = j
    return "".join(out)


def omath(src, color=None, sz=None, cible="docx"):
    """cible « docx » : sz en demi-points ; cible « pptx » : sz en centièmes de point (2400 = 24 pt)."""
    _CIBLE[0] = cible
    try:
        return "<m:oMath>%s</m:oMath>" % _parse(src, color, sz)
    finally:
        _CIBLE[0] = "docx"


# ---------------------------------------------------------------- taille réelle dans PowerPoint et Word
# PowerPoint affiche l'équation éditable à sa taille de police, sans la réduire au cadre (l'image de secours, seule visible dans
# LibreOffice et dans l'aperçu de claude.ai, est, elle, ajustée au cadre). On mesure donc l'équation comme Office la compose :
# police Cambria Math (chasse ≈ Times × 1,05, mesurée sur Liberation Serif), espaces autour des opérateurs (binaire 4/18 em,
# relation 5/18 em de chaque côté), fraction empilée, barre, indices à 70 %. Résultat en em (multiplier par la taille en pt).
_POLICES = {}
_BIN, _REL = set("+−-·×⊕±"), set("=≈≠≤≥→⇒")
_M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"


def _police(ital):
    if ital not in _POLICES:
        from PIL import ImageFont
        f = "LiberationSerif-Italic.ttf" if ital else "LiberationSerif-Regular.ttf"
        _POLICES[ital] = ImageFont.truetype("/usr/share/fonts/truetype/liberation/" + f, 1000)
    return _POLICES[ital]


def _chasse(t, ital):
    w = 0.0
    for ch in t:
        if ch in _BIN: w += 0.62 + 2 * 4 / 18
        elif ch in _REL: w += 0.62 + 2 * 5 / 18
        elif ch in " \u00a0": w += 0.25
        else: w += _police(ital).getlength(ch) / 1000 * 1.05
    return w


def _boite(el):
    """(largeur, hauteur au-dessus de la ligne de base, profondeur) en em d'un élément OMML."""
    tag = el.tag.replace(_M, "")
    enf = lambda nom: el.find(_M + nom)
    if tag == "r":
        t = "".join(x.text or "" for x in el.iter(_M + "t"))
        sty = el.find(f"{_M}rPr/{_M}sty")
        return _chasse(t, sty is None or sty.get(_M + "val") == "i"), 0.75, 0.25
    if tag == "bar":
        w, a, d = _suite(enf("e"))
        return w, a + 0.18, d
    if tag == "f":
        n, d_ = _suite(enf("num")), _suite(enf("den"))
        return max(n[0], d_[0]) + 0.25, n[1] + n[2] + 0.35, d_[1] + d_[2] + 0.1
    if tag in ("sSub", "sSup"):
        b = _suite(enf("e")); x = _suite(enf("sub" if tag == "sSub" else "sup"))
        return b[0] + 0.7 * x[0] + 0.05, b[1] + (0.35 if tag == "sSup" else 0), b[2] + (0.25 if tag == "sSub" else 0)
    if tag == "rad":
        w, a, d = _suite(enf("e"))
        return w + 0.7, a + 0.2, d
    if tag == "d":
        w, a, d = _suite(el)
        return w + 0.8, a, d
    return _suite(el)


def _suite(el):
    W, A, D = 0.0, 0.75, 0.25
    if el is None:
        return W, A, D
    for c in el:
        if c.tag.endswith("Pr") or c.tag == _M + "deg":
            continue
        w, a, d = _boite(c)
        W += w; A = max(A, a); D = max(D, d)
    return W, A, D


def mesure(xml):
    """Largeur et hauteur (em) d'une équation OMML (<m:oMath>…</m:oMath>, préfixes m: a: w: acceptés)."""
    import xml.etree.ElementTree as ET
    ns = ('xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
          'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
          'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"')
    racine = ET.fromstring("<racine %s>%s</racine>" % (ns, xml))
    w, a, d = _suite(racine.find(_M + "oMath") if racine.find(_M + "oMath") is not None else racine)
    return w, a + d


def ajuster(src, color, sz, w_pt, h_pt):
    """Taille (centièmes de point) qui fait tenir l'équation dans son cadre w_pt × h_pt, au plus sz."""
    w, h = mesure(omath(src, color, 1000, "pptx"))
    return int(min(sz, w_pt / w * 100, h_pt / h * 100 * 1.05))


if __name__ == "__main__":
    # pour moteur/deck.js : lit [[source, couleur, taille], …] en JSON sur l'entrée standard, écrit la liste des m:oMath (cible pptx)
    import json, sys
    # avec la taille du cadre (pt), le corps est réduit pour que PowerPoint affiche l'équation dans son cadre (REGLES 9.4)
    out = []
    for e in json.load(sys.stdin):
        src, col, sz = e[:3]
        if len(e) > 4 and e[3] and e[4]:
            sz = ajuster(src, col, sz, e[3] * 0.97, e[4])
        out.append(omath(src, col, sz, "pptx"))
    print(json.dumps(out))
