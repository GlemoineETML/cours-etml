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


if __name__ == "__main__":
    # pour moteur/deck.js : lit [[source, couleur, taille], …] en JSON sur l'entrée standard, écrit la liste des m:oMath (cible pptx)
    import json, sys
    print(json.dumps([omath(src, col, sz, "pptx") for src, col, sz in json.load(sys.stdin)]))
