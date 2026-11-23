# -*- coding: utf-8 -*-
"""Chapitre 220 — schémas CEI. Flèche de tension du + vers le −."""
from figures import *


def source_box(x0=48, y0=52, w=212, h=216, label="source"):
    return ((f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" '
             f'stroke="{GREY}" stroke-width="2.2" stroke-dasharray="8 6" rx="8"/>')
            + T(x0 + w / 2, y0 - 12, label, 17, GREY, weight="bold"))


def source_branch(x=110, ytop=84, ybot=234):
    """Branche interne U0 + Ri, bornes en ytop / ybot."""
    s = W([(x, ybot), (x, 224)]) + W([(x, 176), (x, 156)]) + W([(x, 124), (x, ytop)])
    s += src_v(x, 200) + T(x + 32, 190, "+", 18, NAVY, anchor="start", weight="bold")
    s += T(x + 32, 226, "−", 18, NAVY, anchor="start", weight="bold")
    s += res_v(x, 140) + T(x - 26, 147, "Rᵢ", 18, NAVY, anchor="end", style="italic")
    return s


# ------------------------------------------------------- F10 marche à vide
w, h = 640, 320
s = head(w, h)
s += source_box(label="source")
s += source_branch()
s += W([(110, 84), (260, 84)]) + W([(110, 234), (260, 234)])
s += f'<circle cx="260" cy="84" r="5.5" fill="{NAVY}"/><circle cx="260" cy="234" r="5.5" fill="{NAVY}"/>'
s += T(276, 76, "A", 16, NAVY, anchor="start", weight="bold")
s += T(276, 250, "B", 16, NAVY, anchor="start", weight="bold")
# voltmètre entre les bornes
s += W([(260, 84), (330, 84)]) + W([(330, 84), (330, 138)])
s += meter(330, 158, "V")
s += W([(330, 178), (330, 234)]) + W([(260, 234), (330, 234)])
# branche de charge ouverte
s += W([(330, 84), (470, 84)]) + switch(470, 84) + W([(524, 84), (560, 84)])
s += W([(560, 84), (560, 127)]) + res_v(560, 159) + W([(560, 191), (560, 234)])
s += W([(330, 234), (560, 234)])
s += T(590, 166, "R", 18, NAVY, anchor="start", style="italic")
s += T(497, 52, "interrupteur ouvert", 15, RED, weight="bold")
s += T(497, 32, "I = 0 A", 20, RED, weight="bold")
s += T(325, 296, "Marche à vide : le voltmètre lit U₀", 19, NAVY, weight="bold")
save("10_marche_a_vide", s + TAIL)

# ------------------------------------------------------- F11 court-circuit
w, h = 640, 320
s = head(w, h)
s += source_box(label="source")
s += source_branch()
s += W([(110, 84), (260, 84)]) + W([(110, 234), (260, 234)])
s += f'<circle cx="260" cy="84" r="5.5" fill="{NAVY}"/><circle cx="260" cy="234" r="5.5" fill="{NAVY}"/>'
s += T(276, 76, "A", 16, NAVY, anchor="start", weight="bold")
s += T(276, 250, "B", 16, NAVY, anchor="start", weight="bold")
# ampèremètre en travers des bornes = court-circuit
s += W([(260, 84), (430, 84)], RED, 3.4) + W([(430, 84), (430, 139)], RED, 3.4)
s += meter(430, 159, "A", 20, RED)
s += W([(430, 179), (430, 234)], RED, 3.4) + W([(260, 234), (430, 234)], RED, 3.4)
s += varrow(300, 100, 218, "U = 0 V", BLUE, side="right", size=17)
s += f'<line x1="300" y1="58" x2="375" y2="58" stroke="{RED}" stroke-width="2.6" marker-end="url(#arR)"/>'
s += T(296, 44, "I = I", 20, RED, weight="bold", anchor="end") + T(297, 50, "cc", 14, RED, anchor="start", weight="bold")
s += T(500, 150, "liaison de", 15, RED, anchor="start", weight="bold")
s += T(500, 170, "résistance nulle", 15, RED, anchor="start", weight="bold")
s += T(325, 296, "Court-circuit : U tombe à 0, I atteint son maximum", 19, NAVY, weight="bold")
save("11_court_circuit", s + TAIL)

# ------------------------------------------------------- F12 relevé point par point
w, h = 660, 320
s = head(w, h)
s += source_box(label="source à relever")
s += source_branch()
s += W([(110, 84), (300, 84)]) + W([(110, 234), (300, 234)])
s += f'<circle cx="260" cy="84" r="5.5" fill="{NAVY}"/><circle cx="260" cy="234" r="5.5" fill="{NAVY}"/>'
s += W([(300, 84), (338, 84)]) + W([(378, 84), (490, 84)]) + meter(358, 84, "A")
s += W([(300, 84), (300, 138)]) + W([(300, 178), (300, 234)]) + meter(300, 158, "V")
s += W([(490, 84), (490, 127)]) + W([(490, 191), (490, 234)]) + W([(300, 234), (490, 234)])
s += res_v(490, 159)
s += f'<line x1="462" y1="190" x2="520" y2="128" stroke="{NAVY}" stroke-width="2.6" marker-end="url(#ar)"/>'
s += T(534, 152, "on fait varier", 15, NAVY, anchor="start")
s += T(534, 172, "la charge", 15, NAVY, anchor="start")
s += T(330, 296, "On note un couple (I ; U) par position de la charge", 18, NAVY, weight="bold")
save("12_releve", s + TAIL)
print("SVG chapitre 220 : ok")
