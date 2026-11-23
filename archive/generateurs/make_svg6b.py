# -*- coding: utf-8 -*-
"""Test 320 série B — schémas CEI.

Même structure que la série A, valeurs entièrement nouvelles : aucune ne se
retrouve dans le test A, dans la fiche 310 ni dans le cours 300.
"""
from figures import *
from make_svg3 import node, lab, ih, iv, source
from make_svg4 import cap_h, cap_v, capw_h, switch_open

# ============================================================ B1 réseau (Q3)
# C1 en série avec [ C4 // (C2 série C3) ] — la topologie de la série A
w, h = 780, 330
s = head(w, h)
XA, XB, YM = 80, 700, 165
n1, n2 = 260, 560
s += T(XA - 14, YM + 6, "A", 16, NAVY, anchor="end")
s += T(XB + 14, YM + 6, "B", 16, NAVY, anchor="start")
s += capw_h(XA, n1, YM, "C_1", "18 µF", dy=-26)
s += W([(n1, YM), (n1, 65)]) + W([(n1, 65), (n1 + 40, 65)])
s += W([(n2, YM), (n2, 65)]) + W([(n2 - 40, 65), (n2, 65)])
s += capw_h(n1 + 40, n2 - 40, 65, "C_4", "22 µF", dy=-24)
s += W([(n1, YM), (n1, 275)]) + W([(n1, 275), (n1 + 30, 275)])
s += W([(n2, YM), (n2, 275)]) + W([(n2 - 30, 275), (n2, 275)])
mid = (n1 + n2) / 2
s += capw_h(n1 + 30, mid, 275, "C_2", "21 µF", dy=-24)
s += capw_h(mid, n2 - 30, 275, "C_3", "42 µF", dy=-24)
s += W([(n2, YM), (XB, YM)])
s += node(n1, YM) + node(n2, YM)
save("B1_reseau", s + TAIL)

# ============================================================ B2 circuit de charge (Q4)
w, h = 580, 300
s = head(w, h)
XL, XR, YT, YB = 90, 460, 85, 250
s += source(XL, YT, YB, "U = 9 V")
s += W([(XL, YT), (XL + 40, YT)])
s += switch_open(XL + 40, YT, nom="S")
s += W([(XL + 94, YT), (XL + 140, YT)])
s += res_h(XL + 180, YT, 74, 28)
s += lab(XL + 180, YT - 44, "R", "750 Ω", 16)
s += W([(XL + 217, YT), (XR, YT)])
s += W([(XR, YT), (XR, YT + 62)]) + W([(XR, YT + 78), (XR, YB)])
s += W([(XL, YB), (XR, YB)])
s += cap_v(XR, YT + 70)
s += T(XR + 22, YT + 60, "C_x", 16, NAVY, anchor="start", style="italic",
       weight="bold")
s += T(XR + 22, YT + 80, "?", 16, RED, anchor="start", weight="bold")
s += ih(XL + 290, YT, "i_C", above=True)
save("B2_circuit_charge", s + TAIL)

# ============================================================ B3 ouverture (Q5)
w, h = 700, 330
s = head(w, h)
XL, XM, XR, YT, YB = 90, 350, 560, 85, 275
s += source(XL, YT, YB, "E = 36 V")
s += W([(XL, YT), (XL + 110, YT)])
s += res_h(XL + 150, YT, 74, 28)
s += T(XL + 150, YT - 46, "R_1", 16, NAVY, style="italic", weight="bold")
s += T(XL + 150, YT - 27, "250 Ω", 14, NAVY)
s += W([(XL + 187, YT), (XL + 210, YT)])
s += switch_open(XL + 210, YT, nom="S")
s += W([(XL + 264, YT), (XR, YT)])
s += W([(XL, YB), (XR, YB)])
s += W([(XM, YT), (XM, YT + 56)]) + W([(XM, YT + 124), (XM, YB)])
s += res_v(XM, YT + 90, 28, 68)
s += T(XM - 24, YT + 86, "R_2", 16, NAVY, anchor="end", style="italic",
       weight="bold")
s += T(XM - 24, YT + 108, "200 Ω", 14, NAVY, anchor="end")
s += node(XM, YT)
s += W([(XR, YT), (XR, YT + 82)]) + W([(XR, YT + 98), (XR, YB)])
s += cap_v(XR, YT + 90)
s += T(XR + 24, YT + 80, "C", 16, NAVY, anchor="start", style="italic",
       weight="bold")
s += T(XR + 24, YT + 102, "25 µF", 14, NAVY, anchor="start")
s += iv(XR, YT + 40, "i_C", dir=1, left=True)
s += (f'<line x1="{XM+58}" y1="{YT+30}" x2="{XM+58}" y2="{YB-30}" stroke="{BLUE}" '
      f'stroke-width="2.2" marker-end="url(#arB)"/>')
s += T(XM + 68, (YT + YB) / 2, "u_C", 17, BLUE, anchor="start", weight="bold")
s += T(350, 318, "S est fermé depuis longtemps, puis ouvert à t = 0", 15, GREY)
save("B3_circuit_ouverture", s + TAIL)

print("schémas test 320 B : ok")
