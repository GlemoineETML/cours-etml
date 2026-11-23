# -*- coding: utf-8 -*-
"""Équations Word natives (OMML) à partir d'une mini-syntaxe LaTeX (copie de generateurs/mathml.py).
Ajout : \\sqrt{...} (racine carrée), \\varphi."""
from html import escape

SYM = {"\\cdot": "·", "\\approx": "≈", "\\Delta": "Δ", "\\ohm": "Ω",
       "\\times": "×", "\\pm": "±", "\\infty": "∞", "\\to": "→",
       "\\ne": "≠", "\\le": "≤", "\\ge": "≥",
       "\\neq": "≠", "\\leq": "≤", "\\geq": "≥",
       "\\tau": "τ", "\\mu": "µ", "\\varepsilon": "ε", "\\epsilon": "ε",
       "\\Omega": "Ω", "\\pi": "π", "\\alpha": "α", "\\beta": "β",
       "\\Rightarrow": "⇒", "\\varphi": "φ", "\\omega": "ω", "\\eta": "η", "\\rho": "ρ"}


def _rpr(color, sz, italic):
    sty = '<m:rPr><m:sty m:val="%s"/></m:rPr>' % ("i" if italic else "p")
    w = '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
    if color: w += '<w:color w:val="%s"/>' % color
    if sz: w += '<w:sz w:val="%d"/>' % sz
    return sty + w + "</w:rPr>"


def _run(txt, color, sz, italic):
    return "<m:r>%s<m:t xml:space=\"preserve\">%s</m:t></m:r>" % (_rpr(color, sz, italic), escape(txt, quote=False))


def _ctrl(color, sz):
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


def _parse(src, color, sz):
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith("\\f{", i):
            num, j = _brace(src, i + 2); den, j = _brace(src, j)
            out.append("<m:f><m:fPr>%s</m:fPr><m:num>%s</m:num><m:den>%s</m:den></m:f>"
                       % (_ctrl(color, sz), _parse(num, color, sz), _parse(den, color, sz)))
            i = j; continue
        if src.startswith("\\sqrt{", i):
            arg, j = _brace(src, i + 5)
            out.append('<m:rad><m:radPr><m:degHide m:val="1"/>%s</m:radPr><m:deg/><m:e>%s</m:e></m:rad>'
                       % (_ctrl(color, sz), _parse(arg, color, sz)))
            i = j; continue
        if src.startswith("\\u{", i):
            txt, j = _brace(src, i + 2)
            out.append(_run(txt, color, sz, False)); i = j; continue
        hit = None
        for k, v in sorted(SYM.items(), key=lambda kv: -len(kv[0])):
            if src.startswith(k, i): hit = (k, v); break
        if hit:
            out.append(_run(hit[1], color, sz, hit[0] in ("\\varphi", "\\omega", "\\eta", "\\rho", "\\tau", "\\alpha", "\\beta")))
            i += len(hit[0]); continue
        if c in "_^" and i + 1 < n and src[i + 1] == "{":
            grp, j = _brace(src, i + 1)
            base = out.pop() if out else _run("", color, sz, False)
            tag, part = ("m:sSub", "m:sub") if c == "_" else ("m:sSup", "m:sup")
            out.append("<%s><%sPr>%s</%sPr><m:e>%s</m:e><%s>%s</%s></%s>"
                       % (tag, tag, _ctrl(color, sz), tag, base, part, _parse(grp, color, sz), part, tag))
            i = j; continue
        if c.isalpha():
            j = i
            while j < n and src[j].isalpha(): j += 1
            out.append(_run(src[i:j], color, sz, True)); i = j; continue
        j = i
        while j < n and not src[j].isalpha() and src[j] not in "_^\\": j += 1
        if j == i: j = i + 1
        out.append(_run(src[i:j], color, sz, False)); i = j
    return "".join(out)


def omath(src, color=None, sz=None):
    return "<m:oMath>%s</m:oMath>" % _parse(src, color, sz)
