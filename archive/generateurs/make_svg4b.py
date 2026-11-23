# -*- coding: utf-8 -*-
"""Chapitre 300 — circuit de l'exemple 5 du cours, avec ses valeurs."""
from figures import *
from make_svg3 import node, iv, source
from make_svg4 import cap_v, switch_open

w, h = 700, 340
s = head(w, h)
XL, XM, XR, YT, YB = 90, 350, 560, 90, 285
s += source(XL, YT, YB, "E = 20 V")
s += W([(XL, YT), (XL + 110, YT)])
s += res_h(XL + 150, YT, 74, 28)
s += T(XL + 150, YT - 46, "R_1", 16, NAVY, style="italic", weight="bold")
s += T(XL + 150, YT - 27, "30 Ω", 14, NAVY)
s += W([(XL + 187, YT), (XL + 210, YT)])
s += switch_open(XL + 210, YT, nom="S")
s += W([(XL + 264, YT), (XR, YT)])
s += W([(XL, YB), (XR, YB)])
s += W([(XM, YT), (XM, YT + 56)]) + W([(XM, YT + 124), (XM, YB)])
s += res_v(XM, YT + 90, 28, 68)
s += T(XM - 24, YT + 86, "R_2", 16, NAVY, anchor="end", style="italic", weight="bold")
s += T(XM - 24, YT + 108, "20 Ω", 14, NAVY, anchor="end")
s += node(XM, YT)
s += W([(XR, YT), (XR, YT + 82)]) + W([(XR, YT + 98), (XR, YB)])
s += cap_v(XR, YT + 90)
s += T(XR + 24, YT + 80, "C", 16, NAVY, anchor="start", style="italic", weight="bold")
s += T(XR + 24, YT + 102, "4 µF", 14, NAVY, anchor="start")
s += iv(XR, YT + 40, "i_C", dir=1, left=True)
s += (f'<line x1="{XM+58}" y1="{YT+30}" x2="{XM+58}" y2="{YB-30}" stroke="{BLUE}" '
      f'stroke-width="2.2" marker-end="url(#arB)"/>')
s += T(XM + 68, (YT + YB) / 2, "u_C", 17, BLUE, anchor="start", weight="bold")
s += T(350, 326, "S fermé depuis longtemps, puis ouvert à t = 0", 15, GREY)
save("66b_exemple5", s + TAIL)
print("ok 66b")
