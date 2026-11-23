# -*- coding: utf-8 -*-
"""Figures CEI. Convention : flèche de tension du + vers le −."""
from figures import *


def pm(cx, cy, r=24, dx=32):
    """Signes + et − placés à droite du symbole de source (borne + en haut)."""
    return (T(cx + dx, cy - 10, "+", 19, NAVY, anchor="start", weight="bold")
            + T(cx + dx, cy + 26, "−", 19, NAVY, anchor="start", weight="bold"))


# ---------------------------------------------------------------- F1 source idéale
w, h = 560, 310
s = head(w, h)
s += W([(150, 70), (430, 70)]) + W([(150, 250), (430, 250)])
s += W([(150, 70), (150, 136)]) + W([(150, 184), (150, 250)])
s += src_v(150, 160) + pm(150, 160)
s += W([(430, 70), (430, 128)]) + W([(430, 192), (430, 250)])
s += res_v(430, 160) + T(462, 167, "R", 19, NAVY, anchor="start", style="italic")
s += varrow(96, 88, 236, "U₀", BLUE, side="left")
s += varrow(492, 88, 236, "U", BLUE, side="right")
s += harrow(50, 240, 320, "I", NAVY)
s += T(280, 292, "Source idéale : U = U₀ quel que soit I", 19, NAVY, weight="bold")
save("01_source_ideale", s + TAIL)

# ---------------------------------------------------------------- F2 source réelle
w, h = 640, 350
s = head(w, h)
s += (f'<rect x="48" y="52" width="228" height="232" fill="none" stroke="{GREY}" '
      f'stroke-width="2.2" stroke-dasharray="8 6" rx="8"/>')
s += T(162, 40, "Source réelle (modèle)", 17, GREY, weight="bold")
s += W([(110, 250), (110, 226)]) + W([(110, 174), (110, 154)]) + W([(110, 86), (110, 80)])
s += src_v(110, 200) + pm(110, 200)
s += res_v(110, 120)
s += T(84, 127, "Rᵢ", 19, NAVY, anchor="end", style="italic")
s += W([(110, 80), (276, 80)]) + W([(110, 250), (276, 250)])
s += f'<circle cx="276" cy="80" r="5.5" fill="{NAVY}"/><circle cx="276" cy="250" r="5.5" fill="{NAVY}"/>'
s += T(292, 72, "A", 17, NAVY, weight="bold", anchor="start") + T(292, 268, "B", 17, NAVY, weight="bold", anchor="start")
s += varrow(196, 180, 224, "U₀", BLUE, side="right", size=16)
s += varrow(196, 146, 96, "Rᵢ·I", RED, side="right", size=16)
s += W([(276, 80), (470, 80)]) + W([(276, 250), (470, 250)])
s += W([(470, 80), (470, 133)]) + W([(470, 197), (470, 250)])
s += res_v(470, 165) + T(502, 172, "R", 19, NAVY, anchor="start", style="italic")
s += varrow(320, 98, 232, "U", BLUE, side="right")
s += harrow(62, 350, 430, "I", NAVY)
s += T(330, 330, "U = U₀ − Rᵢ · I", 23, NAVY, weight="bold")
save("02_source_reelle", s + TAIL)

# ---------------------------------------------------------------- F3 analogie
w, h = 620, 340
s = head(w, h)
s += T(300, 34, "Plus le débit est grand, plus l’étranglement fait chuter la pression en sortie",
       16, GREY, weight="bold")
s += T(158, 74, "hauteur d’eau  =  U₀", 17, NAVY, weight="bold")
s += f'<rect x="68" y="88" width="180" height="180" fill="none" stroke="{NAVY}" stroke-width="3"/>'
s += f'<rect x="71" y="118" width="174" height="147" fill="{LBLUE}"/>'
s += (f'<path d="M248,206 L338,206 L360,217 L406,217 L428,206 L528,206 L528,234 '
      f'L428,234 L406,223 L360,223 L338,234 L248,234 Z" fill="{LBLUE}" stroke="{NAVY}" stroke-width="3"/>')
s += f'<line x1="46" y1="100" x2="46" y2="262" stroke="{NAVY}" stroke-width="2.2" marker-end="url(#ar)"/>'
s += f'<line x1="383" y1="166" x2="383" y2="202" stroke="{RED}" stroke-width="2.4" marker-end="url(#arR)"/>'
s += T(383, 156, "étranglement  =  Rᵢ", 17, RED, weight="bold")
s += harrow(272, 300, 400, "débit  =  I", NAVY, above=False, size=17)
s += T(300, 320, "", 1)
save("03_analogie", s + TAIL)

# ---------------------------------------------------------------- F6 mesure de Ri
w, h = 660, 330
s = head(w, h)
s += (f'<rect x="48" y="58" width="212" height="212" fill="none" stroke="{GREY}" '
      f'stroke-width="2.2" stroke-dasharray="8 6" rx="8"/>')
s += T(154, 46, "source à tester", 16, GREY, weight="bold")
s += W([(110, 246), (110, 229)]) + W([(110, 181), (110, 166)]) + W([(110, 102), (110, 90)])
s += src_v(110, 205) + res_v(110, 134)
s += T(84, 141, "Rᵢ", 18, NAVY, anchor="end", style="italic")
s += W([(110, 90), (310, 90)]) + W([(110, 246), (310, 246)])
s += f'<circle cx="260" cy="90" r="5.5" fill="{NAVY}"/><circle cx="260" cy="246" r="5.5" fill="{NAVY}"/>'
s += W([(310, 90), (340, 90)]) + W([(380, 90), (490, 90)]) + meter(360, 90, "A")
s += W([(310, 90), (310, 148)]) + W([(310, 188), (310, 246)]) + meter(310, 168, "V")
s += W([(490, 90), (490, 136)]) + W([(490, 200), (490, 246)]) + W([(310, 246), (490, 246)])
s += res_v(490, 168)
s += f'<line x1="462" y1="199" x2="520" y2="137" stroke="{NAVY}" stroke-width="2.6" marker-end="url(#ar)"/>'
s += T(536, 161, "charge", 15, NAVY, anchor="start") + T(536, 181, "variable", 15, NAVY, anchor="start")
s += T(330, 308, "2 points de mesure  →  Rᵢ = ΔU / ΔI", 20, NAVY, weight="bold")
save("06_mesure_ri", s + TAIL)

# ---------------------------------------------------------------- F7 planche symboles
w, h = 920, 300
s = head(w, h)
cells = [
    ("source de tension", "idéale", lambda x, y: src_h(x, y) + W([(x - 62, y), (x - 24, y)]) + W([(x + 24, y), (x + 62, y)])),
    ("pile /", "accumulateur", lambda x, y: pile_v(x, y) + W([(x, y - 42), (x, y - 8)]) + W([(x, y + 8), (x, y + 42)])),
    ("résistance", "", lambda x, y: res_h(x, y) + W([(x - 62, y), (x - 32, y)]) + W([(x + 32, y), (x + 62, y)])),
    ("résistance", "variable", lambda x, y: varres_h(x, y) + W([(x - 62, y), (x - 32, y)]) + W([(x + 32, y), (x + 62, y)])),
    ("lampe", "", lambda x, y: lampe(x, y) + W([(x - 62, y), (x - 20, y)]) + W([(x + 20, y), (x + 62, y)])),
    ("voltmètre", "", lambda x, y: meter(x, y, "V") + W([(x - 62, y), (x - 20, y)]) + W([(x + 20, y), (x + 62, y)])),
    ("ampèremètre", "", lambda x, y: meter(x, y, "A") + W([(x - 62, y), (x - 20, y)]) + W([(x + 20, y), (x + 62, y)])),
    ("interrupteur", "", lambda x, y: switch(x - 27, y) + W([(x - 62, y), (x - 27, y)]) + W([(x + 27, y), (x + 62, y)])),
]
for i, (l1, l2, fn) in enumerate(cells):
    cx = 118 + (i % 4) * 230
    cy = 78 + (i // 4) * 148
    s += fn(cx, cy) + T(cx, cy + 62, l1, 17, NAVY)
    if l2:
        s += T(cx, cy + 82, l2, 17, NAVY)
save("07_symboles_cei", s + TAIL)

# ---------------------------------------------------------------- F9 batterie / démarreur
w, h = 660, 320
s = head(w, h)
s += (f'<rect x="48" y="52" width="212" height="216" fill="none" stroke="{GREY}" '
      f'stroke-width="2.2" stroke-dasharray="8 6" rx="8"/>')
s += T(154, 40, "batterie 12 V", 17, GREY, weight="bold")
s += W([(110, 234), (110, 206)]) + W([(110, 190), (110, 156)]) + W([(110, 124), (110, 84)])
s += pile_v(110, 198)
s += T(146, 196, "12,6 V", 16, NAVY, anchor="start")
s += res_v(110, 140) + T(84, 147, "Rᵢ", 18, NAVY, anchor="end", style="italic")
s += W([(110, 84), (260, 84)]) + W([(110, 234), (260, 234)])
s += f'<circle cx="260" cy="84" r="5.5" fill="{NAVY}"/><circle cx="260" cy="234" r="5.5" fill="{NAVY}"/>'
s += W([(260, 84), (480, 84)]) + W([(260, 234), (480, 234)])
s += W([(480, 84), (480, 127)]) + W([(480, 191), (480, 234)])
s += res_v(480, 159)
s += T(512, 152, "démarreur", 16, NAVY, anchor="start") + T(512, 172, "≈ 0,06 Ω", 16, NAVY, anchor="start")
s += varrow(310, 100, 218, "U", BLUE, side="right")
s += harrow(66, 350, 440, "I ≈ 180 A", RED)
save("09_batterie", s + TAIL)
print("SVG done")
