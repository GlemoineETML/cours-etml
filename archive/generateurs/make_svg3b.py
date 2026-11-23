# -*- coding: utf-8 -*-
"""Chapitre 140 — figure des deux lois de Kirchhoff (symboles CEI).

Courant : pointe de flèche sur le conducteur. Tension : flèche à côté du composant.
"""
from figures import *
from make_svg3 import node, lab, source, ih, iv, uh

w, h = 940, 330
s = head(w, h)

# ---------------------------------------------------------------- a) nœud
s += T(215, 34, "a)   loi des nœuds", 18, GREY, weight="bold")
s += W([(70, 170), (215, 170)])
s += W([(215, 170), (215, 100)]) + W([(215, 100), (355, 100)])
s += W([(215, 170), (215, 240)]) + W([(215, 240), (355, 240)])
s += node(215, 170)
s += ih(140, 170, "I₁", size=16)
s += ih(300, 100, "I₂", size=16)
s += ih(300, 240, "I₃", size=16)
s += T(215, 292, "I₁ = I₂ + I₃", 21, NAVY, weight="bold")

s += f'<line x1="430" y1="50" x2="430" y2="280" stroke="{LBLUE}" stroke-width="2"/>'

# ---------------------------------------------------------------- b) maille
s += T(700, 34, "b)   loi des mailles", 18, GREY, weight="bold")
XS, YT, YB = 560, 110, 250
XB = 840
s += source(XS, YT, YB, "U")
s += W([(XS, YT), (XB, YT)]) + W([(XS, YB), (XB, YB)])
s += res_h(700, YT) + lab(700, YT + 42, "R₁")
s += W([(XB, YT), (XB, 148)]) + res_v(XB, 180) + W([(XB, 212), (XB, YB)])
s += lab(XB - 34, 176, "R₂", anchor="end")
s += ih(628, YT, "I₁", size=16)
s += uh(666, 736, YT - 30, "U₁", 16)
s += varrow(886, 130, 232, "U₂", BLUE, side="right", size=16)
s += T(700, 292, "U = U₁ + U₂", 21, NAVY, weight="bold")

save("54_kirchhoff", s + TAIL)
