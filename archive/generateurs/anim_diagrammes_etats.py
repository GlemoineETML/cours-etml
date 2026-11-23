# -*- coding: utf-8 -*-
"""Animation « Diagrammes d'états » – Test et Mesure 1 – El DT 1 (ETML).
Théorie : Floyd, Systèmes numériques, 11e éd., chap. 9 « Compteurs »
  §9-1 Machines séquentielles (p. 484-485), §9-5 Conception de compteurs synchrones (p. 505-513),
  exemple 9-4 (p. 509-511), application « système de contrôle d'ascenseur » fig. 9-61 à 9-64 (p. 531-534).
Charte ETML : bande marine à droite avec logo blanc, couleurs 242852 / 297FD5 / ACCBF9, Arial (Liberation Sans).
Sortie : MP4 1920×1080, 25 i/s, H.264.  Aperçu : python3 anim.py <scene> <t>"""
import math, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 25
NAVY, BLUE, LBLUE, TINT, RED, GREY, WHITE = (36, 40, 82), (41, 127, 213), (172, 203, 249), (232, 239, 251), (238, 0, 0), (90, 100, 120), (255, 255, 255)
GREEN, LGREY, ORANGE = (30, 140, 70), (200, 206, 218), (230, 120, 20)
BAND_X = 1776
FD = "/usr/share/fonts/truetype/liberation/"
HERE = os.path.dirname(os.path.abspath(__file__))
_fc = {}


def F(size, bold=False, mono=False, italic=False):
    k = (size, bold, mono, italic)
    if k not in _fc:
        name = ("LiberationMono-" if mono else "LiberationSans-") + ("BoldItalic" if bold and italic else "Bold" if bold else "Italic" if italic else "Regular") + ".ttf"
        _fc[k] = ImageFont.truetype(FD + name, size)
    return _fc[k]


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def prog(t, a, b): return ease((t - a) / (b - a)) if b > a else float(t >= a)
def mix(c1, c2, p): return tuple(int(c1[i] + (c2[i] - c1[i]) * clamp(p)) for i in range(3))


def text(d, xy, s, size, color=NAVY, bold=False, mono=False, italic=False, anchor="la"):
    d.text(xy, s, font=F(size, bold, mono, italic), fill=color, anchor=anchor)


def wrap(s, size, width, bold=False, italic=False):
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if F(size, bold, italic=italic).getlength(test) > width and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    if cur: lines.append(cur)
    return lines


def para(d, xy, s, size, width, color=NAVY, bold=False, italic=False, spacing=1.3):
    x, y = xy
    for i, ln in enumerate(wrap(s, size, width, bold, italic)):
        text(d, (x, y + i * size * spacing), ln, size, color, bold, italic=italic)


def rbox(d, box, fill=None, outline=None, width=3, r=18):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- habillage ETML
LOGO = Image.open(os.path.join(HERE, "logo_white.png")).convert("RGBA").rotate(90, expand=True)
LOGO = LOGO.resize((int(360 * LOGO.width / LOGO.height), 360), Image.LANCZOS)
_vt = Image.new("RGBA", (440, 60), (0, 0, 0, 0)); ImageDraw.Draw(_vt).text((220, 30), "Section électronique", font=F(30, True), fill=WHITE, anchor="mm")
VTXT = _vt.rotate(90, expand=True)
FOOT = "Test et Mesure 1 – El DT 1 · Diagrammes d'états · Floyd, chap. 9"


def chrome(img, d, tag, title, num):
    d.rectangle((BAND_X, 0, W, H), fill=NAVY)
    img.paste(LOGO, (BAND_X + (W - BAND_X - LOGO.width) // 2, 40), LOGO)
    img.paste(VTXT, (BAND_X + (W - BAND_X - VTXT.width) // 2, 470), VTXT)
    if num:
        d.rectangle((BAND_X + 37, 980, BAND_X + 107, 1050), fill=LBLUE)
        text(d, (BAND_X + 72, 1015), num, 26, NAVY, True, anchor="mm")
    d.line((60, 1030, BAND_X - 50, 1030), fill=BLUE, width=2)
    text(d, (60, 1040), "Section électronique", 20, NAVY, italic=True)
    text(d, (BAND_X - 50, 1040), FOOT, 20, GREY, anchor="ra")
    if tag: text(d, (60, 42), tag, 24, BLUE, True)
    if title: text(d, (60, 78), title, 46, NAVY, True)


def caption(d, s, alpha=1.0):
    if not s: return
    col = mix(WHITE, NAVY, alpha)
    rbox(d, (60, 905, BAND_X - 50, 1005), fill=mix(WHITE, TINT, alpha), r=14)
    lines = wrap(s, 30, BAND_X - 160)
    y0 = 955 - (min(len(lines), 2) - 1) * 19
    for i, ln in enumerate(lines[:2]):
        text(d, (90, y0 + i * 38), ln, 30, col, anchor="lm")


def floyd_ref(d, s, x=BAND_X - 50, y=84):
    """Pastille de référence Floyd en haut à droite de la zone de contenu."""
    w = F(22, True).getlength(s) + 40
    rbox(d, (x - w, y - 4, x, y + 36), fill=TINT, outline=BLUE, width=2, r=18)
    text(d, (x - w / 2, y + 16), s, 22, NAVY, True, anchor="mm")


# ---------------------------------------------------------------- primitives diagramme d'états
def bez(p0, c, p1, s):
    return ((1 - s) ** 2 * p0[0] + 2 * (1 - s) * s * c[0] + s * s * p1[0], (1 - s) ** 2 * p0[1] + 2 * (1 - s) * s * c[1] + s * s * p1[1])


def head(d, tip, ang, color, size=20):
    a1 = (tip[0] - size * math.cos(ang - 0.42), tip[1] - size * math.sin(ang - 0.42))
    a2 = (tip[0] - size * math.cos(ang + 0.42), tip[1] - size * math.sin(ang + 0.42))
    d.polygon([tip, a1, a2], fill=color)


def carrow(d, p0, p1, r0=0, r1=0, bend=0.0, color=NAVY, width=4, draw=1.0, dashed=False):
    """Flèche courbe (bézier quadratique) d'un cercle de rayon r0 à un cercle de rayon r1. bend = décalage relatif."""
    if draw <= 0: return None
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    c = (mx - dy / L * bend * L, my + dx / L * bend * L)
    # paramètres de rognage aux cercles
    def trim(r, from_start):
        best = 0.0 if from_start else 1.0
        for i in range(201):
            s = i / 200 if from_start else 1 - i / 200
            q = bez(p0, c, p1, s)
            ref = p0 if from_start else p1
            if math.hypot(q[0] - ref[0], q[1] - ref[1]) >= r: return s
        return best
    s0, s1 = trim(r0, True), trim(r1 + 4, False)
    s_end = s0 + (s1 - s0) * clamp(draw)
    n = 40
    pts = [bez(p0, c, p1, s0 + (s_end - s0) * i / n) for i in range(n + 1)]
    if dashed:
        for i in range(0, n, 2): d.line((pts[i], pts[i + 1]), fill=color, width=width)
    else:
        d.line(pts, fill=color, width=width, joint="curve")
    if draw >= 1:
        q0, q1 = pts[-3], pts[-1]
        head(d, q1, math.atan2(q1[1] - q0[1], q1[0] - q0[0]), color, 16 + width)
    return bez(p0, c, p1, (s0 + s1) / 2)


def parrow(d, pts, color=NAVY, width=4, draw=1.0):
    """Flèche en ligne brisée."""
    if draw <= 0: return
    segs = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    tot = sum(segs) * clamp(draw); out = [pts[0]]
    for i, s in enumerate(segs):
        if tot >= s: out.append(pts[i + 1]); tot -= s
        else:
            f = tot / s; out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)); break
    d.line(out, fill=color, width=width, joint="curve")
    if draw >= 1:
        a, b = pts[-2], pts[-1]
        head(d, b, math.atan2(b[1] - a[1], b[0] - a[0]), color, 16 + width)


def state(d, c, r, label, sub=None, active=0.0, faded=False, warn=0.0, size=None):
    """Cercle d'état. active ∈ [0,1] : remplissage bleu ; warn : remplissage rouge (état parasite)."""
    x, y = c
    if faded:
        for k in range(36):
            if k % 2 == 0:
                d.arc((x - r, y - r, x + r, y + r), k * 10, k * 10 + 10, fill=LGREY, width=4)
        fill, tc = WHITE, (150, 158, 175)
    else:
        fill, tc = WHITE, NAVY
        d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE, outline=NAVY, width=4)
    if active > 0:
        if active > 0.3:
            g = int(10 * active)
            d.ellipse((x - r - g, y - r - g, x + r + g, y + r + g), outline=mix(WHITE, LBLUE, active), width=8)
        fill = mix(WHITE, BLUE, active); tc = mix(NAVY, WHITE, active)
        d.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=NAVY, width=4)
    if warn > 0:
        fill = mix(WHITE, RED, warn); tc = mix(NAVY, WHITE, warn)
        d.ellipse((x - r - 8, y - r - 8, x + r + 8, y + r + 8), outline=mix(WHITE, (255, 190, 190), warn), width=8)
        d.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=RED, width=4)
    lines = label.split("\n")
    sz = size or (30 if len(lines) == 1 else 22)
    for i, ln in enumerate(lines):
        text(d, (x, y + (i - (len(lines) - 1) / 2) * sz * 1.1 - (9 if sub else 0)), ln, sz, tc, True, mono=(size is None and len(lines) == 1), anchor="mm")
    if sub: text(d, (x, y + 22), sub, 20, tc, anchor="mm")


def label_box(d, xy, s, size=20, color=NAVY, anchor="mm", bg=WHITE, alpha=1.0):
    if alpha <= 0: return
    f = F(size, True); w = f.getlength(s); x, y = xy
    if anchor == "lm": x0 = x
    elif anchor == "rm": x0 = x - w - 16
    else: x0 = x - w / 2 - 8
    d.rounded_rectangle((x0, y - size * 0.75, x0 + w + 16, y + size * 0.75), radius=8, fill=bg)
    text(d, (x0 + 8 + w / 2, y), s, size, mix(bg, color, alpha), True, anchor="mm")


def leds(d, x, y, bits, names=("Q2", "Q1", "Q0"), r=30, gap=90):
    for j, b in enumerate(bits):
        cx = x + j * gap
        on = b == "1"
        if on: d.ellipse((cx - r - 9, y - r - 9, cx + r + 9, y + r + 9), fill=(255, 225, 225))
        d.ellipse((cx - r, y - r, cx + r, y + r), fill=RED if on else (245, 235, 235), outline=NAVY, width=3)
        text(d, (cx, y), b, 28, WHITE if on else GREY, True, mono=True, anchor="mm")
        text(d, (cx, y + r + 22), names[j], 22, NAVY, True, anchor="mm")


def display(d, box, label, value, vsize=54):
    rbox(d, box, fill=(30, 34, 60), outline=NAVY, width=4, r=14)
    x0, y0, x1, y1 = box
    if label: text(d, (x0 + 22, y0 + 16), label, 22, LBLUE)
    text(d, ((x0 + x1) / 2, y1 - (y1 - y0) * 0.36), value, vsize, (190, 255, 200), True, mono=True, anchor="mm")


def ring(cx, cy, R, n, start=-90):
    return [(cx + R * math.cos(math.radians(start + 360 * k / n)), cy + R * math.sin(math.radians(start + 360 * k / n))) for k in range(n)]


def tick_state(t, T0, DT, n):
    """Indice de transition courant (0 = avant le 1er front) et progression de l'animation du jeton."""
    if t < T0: return 0, 0.0
    k = min(int((t - T0) / DT) + 1, n)
    return k, prog(t, T0 + (k - 1) * DT, T0 + (k - 1) * DT + 0.5)


# ================================================================ SCÈNES
def s_intro(img, d, t):
    chrome(img, d, "", "", "")
    p = prog(t, 0.2, 1.2)
    text(d, (110, 190), "TEST ET MESURE 1 – EL DT 1 · ANIMATION", 30, mix(WHITE, BLUE, p), True)
    text(d, (110, 250), "Diagrammes d'états", 92, mix(WHITE, NAVY, p), True)
    text(d, (110, 370), "La carte d'un circuit qui se souvient", 44, mix(WHITE, GREY, p))
    items = [("1", "Du chronogramme au diagramme", "compteur 3 bits, comme au tableau"),
             ("2", "Table des états suivants", "compteur en code Gray"),
             ("3", "États inutilisés", "que se passe-t-il à la mise sous tension ?"),
             ("4", "États nommés et conditions", "la commande d'un ascenseur")]
    for i, (n, a, b) in enumerate(items):
        q = prog(t, 1.4 + i * 0.6, 2.0 + i * 0.6)
        if q <= 0: continue
        y = 480 + i * 95; x = 110 + (1 - q) * 60
        d.ellipse((x, y, x + 70, y + 70), fill=mix(WHITE, NAVY, q))
        text(d, (x + 35, y + 35), n, 36, WHITE, True, anchor="mm")
        text(d, (x + 100, y + 35), a, 38, mix(WHITE, NAVY, q), True, anchor="lm")
        text(d, (x + 760, y + 35), b, 32, mix(WHITE, GREY, q), anchor="lm")
    q = prog(t, 4.2, 5.0)
    text(d, (110, 880), "Théorie : Floyd, Systèmes numériques, chap. 9 « Compteurs » – § 9-1 et § 9-5", 30, mix(WHITE, BLUE, q), True)


# ---------------------------------------------------------------- 1 · compteur binaire 3 bits : chronogramme ↔ diagramme
S1_T0, S1_DT = 5.0, 2.3


def s_binary(img, d, t):
    chrome(img, d, "1 · DU CHRONOGRAMME AU DIAGRAMME D'ÉTATS", "Compteur binaire 3 bits", "1/4")
    floyd_ref(d, "Floyd § 9-1, p. 484 · fig. 9-2")
    k, pk = tick_state(t, S1_T0, S1_DT, 8)
    cur = k % 8; prev = (k - 1) % 8
    # --- chronogramme (gauche)
    x0, pw, nper = 170, 64, 9
    rows = [("H", None), ("Q0", 0), ("Q1", 1), ("Q2", 2)]
    reveal = x0 + pw * clamp(k + pk if k >= 1 else prog(t, 1.0, 2.5), 0, nper)
    text(d, (60, 190), "Chronogramme", 28, BLUE, True)
    for r, (name, bit) in enumerate(rows):
        yb = 300 + r * 120; yh = yb - 60
        text(d, (70, yb - 30), name, 30, NAVY, True, anchor="lm")
        if bit is not None:
            text(d, (120, yb - 30), "2", 22, GREY, anchor="lm"); text(d, (133, yb - 40), str(bit), 15, GREY, anchor="lm")
        d.line((x0, yb, x0 + pw * nper + 10, yb), fill=LGREY, width=2)
        pts = []
        for per in range(nper):
            xa = x0 + per * pw
            if name == "H":
                seg = [(xa, yb), (xa, yh), (xa + pw / 2, yh), (xa + pw / 2, yb), (xa + pw, yb)]
            else:
                v = ((per % 8) >> bit) & 1; yy = yh if v else yb
                seg = [(xa, yy), (xa + pw, yy)]
            pts += seg
        # transitions verticales implicites entre segments
        clip = [p for p in pts if p[0] <= reveal]
        if clip and clip[-1][0] < reveal:
            nxt = next((p for p in pts if p[0] > reveal), None)
            if nxt: clip.append((reveal, clip[-1][1]))
        if len(clip) > 1: d.line(clip, fill=NAVY if name != "H" else BLUE, width=5, joint="curve")
        if name != "H":
            for per in range(nper):
                xa = x0 + per * pw
                if xa + pw / 2 <= reveal:
                    v = ((per % 8) >> bit) & 1
                    text(d, (xa + pw / 2, yb + 20), str(v), 18, GREY, anchor="mm")
    # lignes pointillées aux fronts
    for per in range(1, nper):
        xa = x0 + per * pw
        if xa <= reveal:
            for yy in range(225, 680, 14): d.line((xa, yy, xa, yy + 6), fill=LGREY, width=2)
    # état courant sous le chronogramme
    bits = format(cur, "03b")
    text(d, (60, 735), "État présent", 26, GREY)
    leds(d, 300, 760, bits)
    display(d, (560, 712, 790, 830), "", f"{cur}d", 50)
    # curseur sur le chronogramme
    cx = x0 + pw * (k + 0.5 if t >= S1_T0 else 0.5)
    rbox(d, (cx - pw / 2 + 2, 222, cx + pw / 2 - 2, 650), outline=mix(WHITE, BLUE, 0.8), width=3, r=8)
    # --- diagramme (droite)
    text(d, (880, 190), "Diagramme d'états", 28, BLUE, True)
    C = ring(1310, 535, 285, 8)
    reveal_d = prog(t, 0.5, 3.5)
    for j in range(8):
        a = carrow(d, C[j], C[(j + 1) % 8], 56, 56, -0.12, color=mix(WHITE, NAVY, reveal_d), width=4)
    if k >= 1 and t < S1_T0 + 8 * S1_DT + 1:
        hl = prog(t, S1_T0 + (k - 1) * S1_DT, S1_T0 + (k - 1) * S1_DT + 0.4) * (1 - prog(t, S1_T0 + k * S1_DT - 0.6, S1_T0 + k * S1_DT - 0.1))
        if hl > 0:
            m = carrow(d, C[prev], C[cur], 56, 56, -0.12, color=mix(NAVY, BLUE, hl), width=9)
            label_box(d, (m[0] + (m[0] - 1310) * 0.28, m[1] + (m[1] - 535) * 0.28), "front ↑", 20, BLUE, alpha=hl)
    for j in range(8):
        act = 0.0
        if j == cur: act = pk if k >= 1 else prog(t, 2.5, 3.5)
        if j == prev and k >= 1: act = 1 - pk
        state(d, C[j], 56, format(j, "03b"), f"{j}d", active=act * reveal_d if j == cur else act)
    text(d, (1310, 520), "1 front d'horloge", 26, mix(WHITE, BLUE, reveal_d), True, anchor="mm")
    text(d, (1310, 556), "= 1 flèche", 26, mix(WHITE, BLUE, reveal_d), True, anchor="mm")
    # légende
    q = prog(t, S1_T0 + 8 * S1_DT + 0.5, S1_T0 + 8 * S1_DT + 1.5)
    if q > 0:
        rbox(d, (880, 230, 1150, 330), fill=mix(WHITE, TINT, q), r=12)
        text(d, (900, 255), "cercle = état", 22, mix(WHITE, NAVY, q), True)
        text(d, (900, 290), "flèche = front d'horloge", 22, mix(WHITE, NAVY, q), True)
    if t < 2.5: cap = "Comme au tableau : trois bascules Q2 Q1 Q0. Elles mémorisent un nombre de 3 bits → 2³ = 8 états possibles."
    elif t < S1_T0: cap = "Un ÉTAT = une combinaison des bascules. On dessine chaque état dans un cercle : 000, 001 … 111."
    elif k <= 8 and t < S1_T0 + 8 * S1_DT:
        cap = f"Front d'horloge n° {k} : {format(prev, '03b')}b → {format(cur, '03b')}b ({prev}d → {cur}d). Sur le diagramme, on suit UNE flèche."
        if k == 4: cap = "Front n° 4 : 011b → 100b. Q0, Q1 et Q2 basculent ensemble – sur le diagramme, c'est toujours UNE seule flèche."
        if k == 8: cap = "Front n° 8 : 111b → 000b. Après le dernier état, le compteur recommence : le diagramme est une boucle."
    elif t < S1_T0 + 8 * S1_DT + 4.5: cap = "Le chronogramme montre QUAND les bits changent ; le diagramme d'états montre DANS QUEL ORDRE les états se suivent."
    else: cap = "Machine de Moore : sans autre entrée que l'horloge, l'état suivant dépend uniquement de l'état présent (Floyd § 9-1)."
    caption(d, cap)


# ---------------------------------------------------------------- 2 · code Gray : table des états suivants
GRAY = ["000", "001", "011", "010", "110", "111", "101", "100"]
S2_T0, S2_DT = 4.0, 2.4


def s_gray(img, d, t):
    chrome(img, d, "2 · LIRE UN DIAGRAMME D'ÉTATS", "Compteur en code Gray → table des états suivants", "2/4")
    floyd_ref(d, "Floyd § 9-5, p. 505-506 · fig. 9-26 · tab. 9-8")
    k, pk = tick_state(t, S2_T0, S2_DT, 8)
    cur, prev = k % 8, (k - 1) % 8
    # --- diagramme (droite)
    text(d, (1000, 190), "Étape 1 · diagramme d'états", 28, BLUE, True)
    C = ring(1340, 565, 250, 8)
    rv = prog(t, 0.3, 2.0)
    for j in range(8): carrow(d, C[j], C[(j + 1) % 8], 58, 58, -0.12, color=mix(WHITE, NAVY, rv), width=4)
    if 1 <= k and t < S2_T0 + 8 * S2_DT:
        hl = prog(t, S2_T0 + (k - 1) * S2_DT, S2_T0 + (k - 1) * S2_DT + 0.4)
        carrow(d, C[prev], C[cur], 58, 58, -0.12, color=mix(NAVY, BLUE, hl), width=9)
    for j in range(8):
        act = (pk if j == cur else (1 - pk) if j == prev else 0) if k >= 1 else (prog(t, 1.5, 2.5) if j == 0 else 0)
        state(d, C[j], 58, GRAY[j], active=act)
    # --- table (gauche)
    text(d, (60, 190), "Étape 2 · table des états suivants", 28, BLUE, True)
    X = [110, 180, 250, 420, 490, 560]
    rbox(d, (70, 235, 620, 290), fill=NAVY, r=10)
    text(d, (180, 250), "État présent", 22, WHITE, True, anchor="mm")
    text(d, (490, 250), "État suivant", 22, WHITE, True, anchor="mm")
    for i, h in enumerate(["Q2", "Q1", "Q0", "Q2", "Q1", "Q0"]):
        text(d, (X[i], 276), h, 20, LBLUE, True, anchor="mm")
    for r in range(8):
        y = 300 + r * 54
        filled = k >= r + 1
        lit = (k == r + 1 and t < S2_T0 + 8 * S2_DT)
        rbox(d, (70, y, 620, y + 48), fill=TINT if lit else (WHITE if r % 2 else (247, 249, 253)), outline=BLUE if lit else None, width=3, r=8)
        a = GRAY[r]; b = GRAY[(r + 1) % 8]
        for i in range(3): text(d, (X[i], y + 24), a[i], 28, NAVY, True, mono=True, anchor="mm")
        text(d, (335, y + 24), "→", 28, mix(WHITE, BLUE, 1 if filled else 0.25), True, anchor="mm")
        if filled:
            q = prog(t, S2_T0 + r * S2_DT + 0.3, S2_T0 + r * S2_DT + 0.9)
            for i in range(3):
                ch = a[i] != b[i]
                if ch: d.rounded_rectangle((X[3 + i] - 22, y + 4, X[3 + i] + 22, y + 44), radius=8, fill=mix(WHITE, (255, 225, 225), q))
                text(d, (X[3 + i], y + 24), b[i], 28, mix(WHITE, RED if ch else NAVY, q), True, mono=True, anchor="mm")
    # méthode de conception
    TM = S2_T0 + 8 * S2_DT + 1.0
    q = prog(t, TM, TM + 0.8)
    if q > 0:
        rbox(d, (660, 225, 1000, 750), fill=mix(WHITE, WHITE, q), outline=mix(WHITE, NAVY, q), width=3, r=16)
        text(d, (680, 245), "Méthode (Floyd p. 509)", 22, mix(WHITE, BLUE, q), True)
        steps = ["Diagramme d'états", "Table des états suivants", "Tableau des transitions", "Diagrammes de Karnaugh", "Équations des entrées", "Schéma du compteur"]
        for i, s in enumerate(steps):
            y = 300 + i * 72; qi = prog(t, TM + 0.3 + i * 0.25, TM + 0.8 + i * 0.25)
            done = i < 2
            d.ellipse((680, y, 724, y + 44), fill=mix(WHITE, GREEN if done else LGREY, qi))
            if done: d.line([(690, y + 23), (699, y + 32), (715, y + 13)], fill=WHITE, width=5, joint="curve")
            else: text(d, (702, y + 22), str(i + 1), 24, WHITE, True, anchor="mm")
            para(d, (736, y + 2), s, 21, 250, mix(WHITE, NAVY if done else GREY, qi), done)
    if t < 2.0: cap = "Le Floyd part de ce diagramme : un compteur dont la séquence suit le code Gray sur 3 bits (figure 9-26)."
    elif t < S2_T0: cap = "Lire un diagramme d'états : partir d'un cercle (état présent), suivre la flèche, noter l'état d'arrivée (état suivant)."
    elif k <= 8 and t < S2_T0 + 8 * S2_DT:
        a, b = GRAY[prev], GRAY[cur]
        bit = 2 - [i for i in range(3) if a[i] != b[i]][0]
        cap = f"État présent {a} → état suivant {b} : on écrit une ligne de la table. Seul Q{bit} change (en rouge)."
        if k == 8: cap = "Dernière ligne : 100 → 000. La boucle est fermée : 8 états, 8 lignes, un seul bit change à chaque fois."
    elif t < TM + 4: cap = "La table des états suivants est l'étape 2 de la méthode de conception d'un compteur synchrone."
    else: cap = "Avec les étapes 3 à 6 (transitions J-K ou D, Karnaugh), on obtient le schéma – c'est le travail des problèmes 20 à 23."
    caption(d, cap)


# ---------------------------------------------------------------- 3 · séquence irrégulière et états inutilisés (exemple 9-4)
S3 = {1: (1290, 290), 2: (1500, 500), 5: (1290, 710), 7: (1080, 500), 6: (1560, 250), 0: (880, 250), 3: (880, 500), 4: (880, 750)}
NEXT3 = {1: 2, 2: 5, 5: 7, 7: 1, 6: 1, 0: 3, 3: 4, 4: 7}
# chronologie : (t, état) ; les états marqués d'un « ! » sont des états parasites à la mise sous tension
S3_EVENTS = [(0.0, 1), (4.0, 2), (6.4, 5), (8.8, 7), (11.2, 1), (17.5, "!6"), (20.5, 1), (23.5, "!0"), (26.0, 3), (28.4, 4), (30.8, 7), (33.2, 1)]


def s3_state_at(t):
    cur, t_since, prev = 1, t, None
    for i, (te, s) in enumerate(S3_EVENTS):
        if t >= te:
            prev = cur; cur = s; t_since = t - te
    return cur, prev, t_since


def s_unused(img, d, t):
    chrome(img, d, "3 · ÉTATS INUTILISÉS", "Séquence irrégulière 1 → 2 → 5 → 7 → 1", "3/4")
    floyd_ref(d, "Floyd exemple 9-4, p. 509-511 · fig. 9-30")
    cur, prev, ts = s3_state_at(t)
    warn = isinstance(cur, str)
    curn = int(cur[1:]) if warn else cur
    prevn = (int(prev[1:]) if isinstance(prev, str) else prev) if prev is not None else None
    # flèches valides
    for a in (1, 2, 5, 7): carrow(d, S3[a], S3[NEXT3[a]], 60, 60, -0.18, NAVY, 4)
    # flèches de récupération (dessinées quand on les découvre)
    rec = {6: 20.5, 0: 26.0, 3: 28.4, 4: 30.8}
    for a, tr in rec.items():
        q = prog(t, tr - 0.1, tr + 0.6)
        if q > 0: carrow(d, S3[a], S3[NEXT3[a]], 60, 60, 0.0 if a != 4 else 0.15, GREEN, 5, draw=q)
    if t >= 14.0:
        q = prog(t, 14.0, 15.0)
        for a in (0, 3, 4, 6):
            if t < rec[a] and a != curn: text(d, (S3[a][0], S3[a][1] - 82), "?", 34, mix(WHITE, ORANGE, q), True, anchor="mm")
    # jeton actif sur la transition
    if prevn is not None and ts < 0.6 and not warn and prevn in NEXT3 and NEXT3[prevn] == curn:
        hl = 1 - prog(ts, 0.3, 0.6)
        carrow(d, S3[prevn], S3[curn], 60, 60, -0.18 if prevn in (1, 2, 5, 7) else (0.15 if prevn == 4 else 0), BLUE, 9)
    for s, c in S3.items():
        unused = s in (0, 3, 4, 6)
        act = 0.0; wr = 0.0
        if s == curn and not warn: act = prog(ts, 0, 0.5) if prevn is not None else 1.0
        if s == curn and warn: wr = 0.6 + 0.4 * abs(math.sin(ts * 4))
        if s == prevn and not isinstance(prev, str) and s != curn: act = 1 - prog(ts, 0, 0.5)
        if s == prevn and isinstance(prev, str) and s != curn: wr = 1 - prog(ts, 0, 0.5)
        state(d, c, 60, format(s, "03b"), f"{s}d", active=act, faded=unused and wr == 0 and act == 0, warn=wr)
    # légende
    rbox(d, (1430, 760, 1730, 880), fill=TINT, r=12)
    d.line((1450, 795, 1510, 795), fill=NAVY, width=4); text(d, (1525, 795), "séquence voulue", 20, NAVY, True, anchor="lm")
    d.line((1450, 840, 1510, 840), fill=GREEN, width=5); text(d, (1525, 840), "retour au cycle", 20, GREEN, True, anchor="lm")
    # --- gauche : bascules + mise sous tension
    text(d, (60, 190), "Dans le circuit", 28, BLUE, True)
    bits = format(curn, "03b")
    leds(d, 120, 290, bits)
    display(d, (420, 240, 720, 350), "État", f"{curn}d", 48)
    rbox(d, (60, 410, 740, 600), fill=TINT, r=14)
    text(d, (85, 430), "3 bascules → 8 états", 26, NAVY, True)
    text(d, (85, 475), "utilisés :", 24, NAVY); text(d, (230, 475), "1, 2, 5, 7", 24, BLUE, True, mono=True)
    text(d, (85, 515), "inutilisés :", 24, NAVY); text(d, (230, 515), "0, 3, 4, 6", 24, GREY, True, mono=True)
    text(d, (85, 555), "→ cas « indifférents » (X) dans Karnaugh", 22, GREY, italic=True)
    if t >= 16.0:
        q = prog(t, 16.0, 17.0)
        rbox(d, (60, 630, 740, 880), fill=mix(WHITE, (255, 240, 235), q), outline=mix(WHITE, RED, q), width=3, r=14)
        # prise + éclair
        px, py = 110, 700
        d.rectangle((px, py, px + 50, py + 60), fill=mix(WHITE, NAVY, q)); d.line((px + 14, py - 22, px + 14, py), fill=mix(WHITE, NAVY, q), width=6); d.line((px + 36, py - 22, px + 36, py), fill=mix(WHITE, NAVY, q), width=6)
        d.polygon([(px + 90, py - 10), (px + 70, py + 35), (px + 92, py + 35), (px + 76, py + 80), (px + 120, py + 20), (px + 98, py + 20), (px + 112, py - 10)], fill=mix(WHITE, ORANGE, q))
        para(d, (250, 650), "À la mise sous tension (ou après un parasite), les bascules peuvent démarrer dans N'IMPORTE QUEL état.", 24, 470, mix(WHITE, NAVY, q))
        if t >= 23.5:
            text(d, (250, 820), "Départ en 0 : 0 → 3 → 4 → 7 → cycle", 24, mix(WHITE, GREEN, prog(t, 33.2, 33.8)) if t >= 33.2 else mix(WHITE, RED, 1), True)
        elif t >= 17.5:
            text(d, (250, 820), "Départ en 6 : 6 → 1 → cycle", 24, GREEN if t >= 20.5 else RED, True)
    if t < 4.0: cap = "Le compteur doit suivre 1 → 2 → 5 → 7 → 1. Il faut 3 bascules, car le plus grand état vaut 7 = 111b."
    elif t < 13.5: cap = "Chaque front d'horloge fait avancer le compteur d'une flèche. Les états 0, 3, 4 et 6 ne sont jamais visités."
    elif t < 16.0: cap = "Dans le diagramme du Floyd, ces 4 états n'ont pas de flèche. Mais le circuit, lui, aura bien un état suivant pour chacun !"
    elif t < 20.5: cap = "Mise sous tension : les bascules démarrent en 110b = 6. Que fait le compteur au prochain front ?"
    elif t < 23.5: cap = "Avec les équations de l'exemple 9-4, l'état 6 mène à 1 : le compteur rejoint tout seul la séquence voulue."
    elif t < 33.2: cap = "Autre départ : 000b. Le compteur passe par 0 → 3 → 4 → 7 avant de retrouver le cycle (Floyd, solution de l'exemple 9-4)."
    elif t < 37: cap = "Règle : on complète le diagramme avec les états inutilisés et on vérifie qu'aucun ne forme une boucle « piège »."
    else: cap = "Exercice connexe de l'exemple 9-4 : vérifier toi-même ces retours à partir des équations des entrées D."
    caption(d, cap)


# ---------------------------------------------------------------- 4 · ascenseur (fig. 9-61 simplifiée + compteur d'étage fig. 9-63)
E = {"ATT": (1285, 225), "AO": (1285, 495), "F": (1285, 775), "D": (965, 495), "M": (1605, 495)}
ELAB = {"ATT": "ATTENTE", "AO": "ARRÊT\nOUVRE", "F": "FERME", "D": "DESCEND", "M": "MONTE"}
ER = 78
# arcs : (de, vers, courbure, libellé, position du libellé)
EARCS = [("ATT", "D", 0.18, "APPEL < ÉTAGE", (1035, 315)), ("ATT", "M", -0.18, "APPEL > ÉTAGE", (1535, 315)),
         ("ATT", "AO", 0.0, "APPEL = ÉTAGE", (1300, 360)), ("D", "AO", 0.0, "ÉTAGE = cible", (1125, 465)),
         ("M", "AO", 0.0, "ÉTAGE = cible", (1445, 465)), ("AO", "F", 0.0, "T écoulé", (1300, 635)),
         ("F", "D", -0.18, "REQUÊTE < ÉTAGE", (1040, 690)), ("F", "M", 0.18, "REQUÊTE > ÉTAGE", (1530, 690))]
FA_PATH = [(1285 + ER, 775), (1735, 775), (1735, 225), (1285 + ER + 6, 225)]
# scénario : (t, état, étage, appel, requête, porte ouverte, arc emprunté)
EV4 = [(0.0, "ATT", 1, None, None, 0, None),
       (5.0, "M", 1, 5, None, 0, ("ATT", "M")),
       (11.6, "AO", 5, 5, None, 1, ("M", "AO")),
       (17.0, "F", 5, 5, 2, 0, ("AO", "F")),
       (19.5, "D", 5, 5, 2, 0, ("F", "D")),
       (24.0, "AO", 2, 5, 2, 1, ("D", "AO")),
       (28.0, "F", 2, 5, 2, 0, ("AO", "F")),
       (30.5, "ATT", 2, None, None, 0, ("F", "ATT"))]
FLOOR_T = [(6.4, 2), (7.6, 3), (8.8, 4), (10.0, 5), (20.6, 4), (21.8, 3), (23.0, 2)]


def s4_at(t):
    ev = EV4[0]
    for e in EV4:
        if t >= e[0]: ev = e
    floor = 1
    for tf, f in FLOOR_T:
        if t >= tf: floor = f
    # position continue de la cabine (interpolation linéaire entre images clés)
    KF = [(0, 1), (5.2, 1), (10.0, 5), (19.4, 5), (23.0, 2), (999, 2)]
    pos = 1.0
    for (ta, fa), (tb, fb) in zip(KF, KF[1:]):
        if ta <= t < tb: pos = fa + (fb - fa) * (t - ta) / (tb - ta); break
    return ev, floor, pos


def s_elevator(img, d, t):
    chrome(img, d, "4 · ÉTATS NOMMÉS ET CONDITIONS", "La commande d'un ascenseur", "4/4")
    floyd_ref(d, "Floyd application § 9-8, p. 531-534 · fig. 9-61 et 9-63")
    ev, floor, pos = s4_at(t)
    _, st, _, appel, req, door, arc = ev
    te = ev[0]
    # --- immeuble (gauche)
    bx0, bx1, top, fh = 90, 330, 205, 82
    d.rectangle((bx0 - 20, top - 30, bx1 + 20, top + 8 * fh), fill=(240, 243, 250), outline=NAVY, width=3)
    d.polygon([(bx0 - 40, top - 30), ((bx0 + bx1) / 2, top - 85), (bx1 + 40, top - 30)], fill=NAVY)
    for f in range(8):
        y = top + (7 - f) * fh
        d.line((bx0 - 20, y + fh, bx1 + 20, y + fh), fill=LGREY, width=2)
        text(d, (bx0 - 6, y + fh / 2), "S" if f == 0 else str(f), 22, GREY, True, anchor="rm")
        if appel == f and st in ("ATT", "M") and t >= 3.0:
            blink = 0.5 + 0.5 * math.sin(t * 6)
            d.ellipse((bx1 - 34, y + fh / 2 - 12, bx1 - 10, y + fh / 2 + 12), fill=mix(WHITE, ORANGE, blink), outline=NAVY, width=2)
    # cage + cabine
    sx0, sx1 = 150, 250
    d.rectangle((sx0, top, sx1, top + 8 * fh), outline=GREY, width=2)
    cy = top + (7 - pos) * fh
    d.rectangle((sx0 + 4, cy + 6, sx1 - 4, cy + fh - 4), fill=BLUE, outline=NAVY, width=3)
    op = 0.0
    if door:
        op = prog(t, te + 0.3, te + 1.2) * (1 - prog(t, te + 4.6 if st == "AO" else 99, te + 5.4))
    gap = 40 * op
    mx = (sx0 + sx1) / 2
    d.rectangle((sx0 + 8, cy + 10, mx - gap, cy + fh - 8), fill=LBLUE)
    d.rectangle((mx + gap, cy + 10, sx1 - 8, cy + fh - 8), fill=LBLUE)
    if op > 0.3: d.ellipse((mx - 9, cy + 22, mx + 9, cy + 40), fill=NAVY); d.rectangle((mx - 9, cy + 42, mx + 9, cy + fh - 10), fill=NAVY)
    # capteur d'étage
    for tf, f in FLOOR_T:
        if 0 <= t - tf < 0.5:
            yy = top + (7 - f) * fh + fh - 6
            d.polygon([(sx1 + 4, yy), (sx1 + 26, yy - 12), (sx1 + 26, yy + 12)], fill=RED)
            text(d, (sx1 + 34, yy), "impulsion", 18, RED, True, anchor="lm")
    # --- registres
    rx = 420
    text(d, (rx, 190), "Compteur d'étage", 24, BLUE, True)
    cells = format(floor, "03b")
    for j, b in enumerate(cells):
        x = rx + j * 70
        rbox(d, (x, 225, x + 60, 285), fill=LBLUE if b == "1" else WHITE, outline=NAVY, width=3, r=10)
        text(d, (x + 30, 255), b, 32, NAVY, True, mono=True, anchor="mm")
    display(d, (rx + 220, 220, rx + 360, 292), "", str(floor), 44)
    text(d, (rx, 300), "ÉTAGE", 20, GREY, True)
    # mini-diagramme du compteur d'étage (réversible)
    for f in range(8):
        cx = rx + 20 + f * 44; cyy = 360
        on = f == floor
        d.ellipse((cx - 17, cyy - 17, cx + 17, cyy + 17), fill=BLUE if on else WHITE, outline=NAVY, width=2)
        text(d, (cx, cyy), str(f), 18, WHITE if on else NAVY, True, anchor="mm")
        if f < 7:
            d.line((cx + 17, cyy - 6, cx + 27, cyy - 6), fill=GREEN, width=2)
            d.line((cx + 17, cyy + 6, cx + 27, cyy + 6), fill=RED, width=2)
    text(d, (rx, 392), "monte +1 / descend −1 (fig. 9-63)", 18, GREY, italic=True)
    for i, (lab, val) in enumerate([("APPEL", appel), ("REQUÊTE", req)]):
        y = 450 + i * 120
        text(d, (rx, y), lab, 24, BLUE, True)
        v = "---" if val is None else format(val, "03b")
        for j, b in enumerate(v):
            x = rx + j * 70
            rbox(d, (x, y + 35, x + 60, y + 95), fill=LBLUE if b == "1" else WHITE, outline=NAVY, width=3, r=10)
            text(d, (x + 30, y + 65), b, 32, NAVY if val is not None else LGREY, True, mono=True, anchor="mm")
        text(d, (rx + 230, y + 65), "" if val is None else f"= {val}", 30, NAVY, True, anchor="lm")
    # sorties
    text(d, (rx, 700), "Sorties vers moteur et porte", 24, BLUE, True)
    outs = [("MONTE", st == "M"), ("DESCEND", st == "D"), ("ARRÊT/OUVRE", st == "AO"), ("FERME", st == "F")]
    for i, (lab, on) in enumerate(outs):
        x = rx + (i % 2) * 185; y = 740 + (i // 2) * 60
        rbox(d, (x, y, x + 175, y + 48), fill=GREEN if on else WHITE, outline=NAVY, width=2, r=10)
        text(d, (x + 87, y + 24), lab, 19, WHITE if on else GREY, True, anchor="mm")
    # --- diagramme (droite)
    d.line((860, 180, 860, 880), fill=LGREY, width=2)
    rv = prog(t, 0.2, 1.5)
    for a, b, bend, lab, lp in EARCS:
        used = arc == (a, b) and t - te < 1.6
        carrow(d, E[a], E[b], ER, ER, bend, mix(WHITE, BLUE if used else NAVY, rv), 9 if used else 4)
    used_fa = arc == ("F", "ATT") and t - te < 1.6
    parrow(d, FA_PATH, mix(WHITE, BLUE if used_fa else NAVY, rv), 9 if used_fa else 4)
    for a, b, bend, lab, lp in EARCS:
        used = arc == (a, b) and t - te < 2.5
        label_box(d, lp, lab, 19, BLUE if used else NAVY, alpha=rv)
    for i, w in enumerate(("aucune", "requête")):
        label_box(d, (1728, 610 + i * 28), w, 19, BLUE if used_fa else NAVY, anchor="rm", alpha=rv)
    for k, c in E.items():
        act = 0.0
        if k == st: act = prog(t, te, te + 0.5) if te > 0 else 1.0
        state(d, c, ER, ELAB[k], active=act, size=22)
    label_box(d, (1285, 868), "cible = étage de l'APPEL ou de la REQUÊTE · T = temporisation de la porte", 18, GREY, alpha=rv)
    # légendes
    if t < 3.0: cap = "Ici, les cercles portent un NOM : ce que fait le système. Les flèches portent une CONDITION à vérifier."
    elif t < 5.0: cap = "L'ascenseur attend au 1er étage (ÉTAGE = 001b). Quelqu'un appelle depuis le 5e : APPEL = 101b."
    elif t < 6.4: cap = "APPEL > ÉTAGE (101b > 001b) : la flèche « APPEL > ÉTAGE » est vraie → état MONTE, le moteur tourne."
    elif t < 11.6: cap = "À chaque étage, le capteur envoie une impulsion : le compteur d'étage avance d'un état (2, 3, 4, 5)."
    elif t < 14.5: cap = "ÉTAGE = APPEL : on passe en ARRÊT/OUVRE. Le moteur s'arrête et la porte s'ouvre."
    elif t < 17.0: cap = "La personne entre et choisit le 2e étage : REQUÊTE = 010b. On reste dans l'état tant que T n'est pas écoulé."
    elif t < 19.5: cap = "T écoulé → FERME. La porte se referme."
    elif t < 24.0: cap = "REQUÊTE < ÉTAGE (2 < 5) → DESCEND. Le compteur d'étage compte maintenant à rebours : 4, 3, 2."
    elif t < 28.0: cap = "ÉTAGE = REQUÊTE → ARRÊT/OUVRE : la personne sort au 2e étage."
    elif t < 30.5: cap = "T écoulé → FERME."
    elif t < 34.5: cap = "Plus aucune requête → retour en ATTENTE, au 2e étage, jusqu'au prochain APPEL."
    else: cap = "Un diagramme d'états décrit tout système qui enchaîne des situations : ascenseur, feux, distributeur, machine à laver…"
    caption(d, cap)


# ---------------------------------------------------------------- récapitulatif + exercices Floyd
EXOS = [("Révision § 9-1, questions 1 à 3", "Moore ou Mealy ?", "p. 485"),
        ("Problèmes 1 et 2", "dessiner le diagramme d'un compteur à décade", "p. 537"),
        ("Exemple 9-4 + exercice connexe", "vérifier les états inutilisés", "p. 509-511"),
        ("Révision § 9-5, questions 1 à 3", "état présent → état suivant", "p. 513"),
        ("Problèmes 18 et 19", "trouver la séquence, dessiner le diagramme", "p. 540"),
        ("Problèmes 20 à 23", "du diagramme d'états au compteur", "p. 540"),
        ("Application ascenseur", "relire fig. 9-61 à 9-64", "p. 531-534")]


def s_outro(img, d, t):
    chrome(img, d, "RÉCAPITULATIF", "À retenir – et à t'exercer dans le Floyd", "")
    rows = [("État", "une combinaison des bascules (cercle)"), ("Flèche", "un front d'horloge (+ une condition)"),
            ("Table", "état présent → état suivant"), ("Vérifier", "les états inutilisés reviennent au cycle")]
    for i, (a, b) in enumerate(rows):
        q = prog(t, 0.3 + i * 0.4, 0.9 + i * 0.4)
        if q <= 0: continue
        y = 200 + i * 105
        rbox(d, (60, y, 820, y + 88), fill=mix(WHITE, TINT, q), r=14)
        text(d, (90, y + 44), a, 32, mix(WHITE, NAVY, q), True, anchor="lm")
        text(d, (260, y + 44), b, 26, mix(WHITE, NAVY, q), anchor="lm")
    q0 = prog(t, 1.8, 2.5)
    text(d, (880, 185), "Floyd, chap. 9 « Compteurs »", 30, mix(WHITE, BLUE, q0), True)
    for i, (a, b, p) in enumerate(EXOS):
        q = prog(t, 2.0 + i * 0.35, 2.6 + i * 0.35)
        if q <= 0: continue
        y = 235 + i * 92
        d.ellipse((880, y + 8, 930, y + 58), fill=mix(WHITE, NAVY, q))
        text(d, (905, y + 33), str(i + 1), 24, WHITE, True, anchor="mm")
        text(d, (950, y + 8), a, 27, mix(WHITE, NAVY, q), True)
        text(d, (950, y + 44), b, 22, mix(WHITE, GREY, q), italic=True)
        text(d, (BAND_X - 60, y + 22), p, 26, mix(WHITE, BLUE, q), True, anchor="ra")
    caption(d, "Réponses : problèmes impairs à la fin du livre. Le lien du chapitre numérisé est sur la page interactive.", prog(t, 5, 5.8))


# ================================================================ CARTES DE TRANSITION
def ill_pills(d, t, a):
    bx, by = 260, 470
    d.rounded_rectangle((bx, by, bx + 220, by + 300), radius=26, outline=NAVY, width=5, fill=(246, 249, 255))
    d.rectangle((bx + 60, by - 50, bx + 160, by + 4), outline=NAVY, width=5, fill=WHITE)
    n = min(25, int(t * 3))
    for i in range(n):
        x = bx + 30 + (i % 5) * 36; y = by + 262 - (i // 5) * 30
        d.ellipse((x, y, x + 30, y + 22), fill=BLUE)
    yy = 300 + (t * 300) % 170
    d.ellipse((bx + 92, yy, bx + 122, yy + 22), fill=BLUE)
    d.polygon([(bx + 30, 260), (bx + 190, 260), (bx + 130, 330), (bx + 90, 330)], fill=(215, 220, 232), outline=GREY)
    display(d, (520, 520, 740, 640), "comprimés", f"{n}/25", 40)


def ill_disc(d, t, a):
    cx, cy = 380, 560
    rot = t * 18
    for tr, R in enumerate([250, 190, 130]):
        bit = tr  # piste extérieure = Q0
        for s in range(8):
            g = GRAY[s]
            on = g[2 - bit] == "1"
            a0 = rot + s * 45 - 90
            d.pieslice((cx - R, cy - R, cx + R, cy + R), a0, a0 + 45, fill=NAVY if on else WHITE, outline=LGREY)
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=WHITE, outline=NAVY, width=3)
    text(d, (cx, cy), "Gray", 30, NAVY, True, anchor="mm")
    d.polygon([(cx + 270, cy), (cx + 300, cy - 18), (cx + 300, cy + 18)], fill=RED)
    text(d, (cx, cy + 290), "codeur d'angle à 3 pistes", 24, GREY, anchor="mm")


def ill_power(d, t, a):
    px, py = 170, 420
    d.rectangle((px, py, px + 90, py + 110), fill=NAVY)
    d.line((px + 25, py - 40, px + 25, py), fill=NAVY, width=10); d.line((px + 65, py - 40, px + 65, py), fill=NAVY, width=10)
    d.polygon([(px + 170, py - 20), (px + 130, py + 70), (px + 175, py + 70), (px + 145, py + 160), (px + 235, py + 40), (px + 190, py + 40), (px + 215, py - 20)], fill=ORANGE)
    import random
    random.seed(int(t * 2))
    bits = "".join(random.choice("01") for _ in range(3))
    leds(d, 400, 500, bits)
    text(d, (520, 600), "état au démarrage ?", 26, RED, True, anchor="mm")
    display(d, (200, 680, 700, 790), "séquence voulue", "1 → 2 → 5 → 7", 40)


def ill_lift(d, t, a):
    bx0, top, fh = 250, 300, 70
    d.rectangle((bx0, top, bx0 + 220, top + 8 * fh), fill=(240, 243, 250), outline=NAVY, width=3)
    d.polygon([(bx0 - 20, top), (bx0 + 110, top - 60), (bx0 + 240, top)], fill=NAVY)
    for f in range(8):
        d.line((bx0, top + f * fh, bx0 + 220, top + f * fh), fill=LGREY, width=2)
    pos = 3.5 + 3.4 * math.sin(t * 0.7)
    cy = top + (7 - pos) * fh
    d.rectangle((bx0 + 70, cy + 6, bx0 + 150, cy + fh - 4), fill=BLUE, outline=NAVY, width=3)
    for i, (s, x) in enumerate([("▲", 560), ("▼", 640)]):
        d.ellipse((x, 500, x + 64, 564), fill=WHITE, outline=NAVY, width=3)
        text(d, (x + 32, 532), s, 28, NAVY, True, anchor="mm")
    text(d, (632, 600), "APPEL", 24, GREY, True, anchor="mm")


CARDS = [
    ("1", "Du chronogramme au diagramme d'états", "Compteur binaire 3 bits – comme au tableau", ill_pills,
     "Floyd § 9-1 : une machine remplit des bouteilles de 25 comprimés. Un compteur avance d'un état à chaque comprimé.",
     "Comment représenter TOUTE la séquence d'un compteur sur une seule figure ?",
     "On dessine chaque état dans un cercle et chaque front d'horloge par une flèche.", "000 → 001 → … → 111"),
    ("2", "Lire un diagramme d'états", "Compteur en code Gray → table des états suivants", ill_disc,
     "Un codeur d'angle ou un compteur sans aléa utilise le code Gray : un seul bit change à la fois.",
     "Comment passer du dessin à un tableau qu'on peut utiliser pour concevoir le circuit ?",
     "Pour chaque état présent, on suit la flèche et on note l'état suivant.", "présent → suivant"),
    ("3", "États inutilisés", "Séquence irrégulière – exemple 9-4 du Floyd", ill_power,
     "Un séquenceur pilote 4 étapes d'une machine : 1 → 2 → 5 → 7. Avec 3 bascules, 4 états restent inutilisés.",
     "Et si, à la mise sous tension, le compteur démarre dans un état inutilisé ?",
     "On vérifie que chaque état inutilisé revient dans le cycle.", "0, 3, 4, 6 → ?"),
    ("4", "États nommés et conditions", "La commande d'un ascenseur – application du Floyd", ill_lift,
     "Un ascenseur attend, monte, descend, s'arrête, ouvre et ferme sa porte. Un compteur suit l'étage.",
     "Comment décrire un système qui réagit à des boutons et à des capteurs ?",
     "Chaque état a un nom ; chaque flèche porte une condition (APPEL > ÉTAGE…).", "ATTENTE → MONTE → …"),
]
CARD_DUR = 12.0


def make_card(k):
    num, title, use, ill, situ, quest, mtxt, key = CARDS[k]

    def s_card(img, d, t):
        chrome(img, d, "", "", f"{num}/4")
        p = prog(t, 0.0, 1.0)
        d.ellipse((60, 40, 150, 130), fill=mix(WHITE, NAVY, p))
        text(d, (105, 85), num, 50, WHITE, True, anchor="mm")
        text(d, (180, 40), f"DÉMONSTRATION {num} / 4", 24, mix(WHITE, BLUE, p), True)
        text(d, (180, 70), title, 56, mix(WHITE, NAVY, p), True)
        text(d, (180, 145), use, 32, mix(WHITE, GREY, prog(t, 0.6, 1.6)), italic=True)
        q = prog(t, 1.2, 2.4)
        lay = Image.new("RGB", (BAND_X, H), WHITE); dl = ImageDraw.Draw(lay)
        ill(dl, t, q)
        box = (40, 220, 780, 900)
        reg = lay.crop(box)
        img.paste(Image.blend(Image.new("RGB", reg.size, WHITE), reg, q), box[:2])
        X0 = 820
        rbox(d, (X0, 220, BAND_X - 50, 900), fill=mix(WHITE, TINT, prog(t, 1.5, 2.5)), r=20)
        blocks = [("La situation", situ, 2.0), ("La question", quest, 4.0), ("Dans le diagramme d'états", mtxt, 6.0)]
        y = 255
        for head_, body, t0 in blocks:
            r = prog(t, t0, t0 + 1.0)
            text(d, (X0 + 40, y), head_.upper(), 24, mix(TINT, BLUE, r), True)
            lines = wrap(body, 31, BAND_X - 50 - X0 - 80)
            for i, ln in enumerate(lines):
                text(d, (X0 + 40 + (1 - r) * 30, y + 40 + i * 40), ln, 31, mix(TINT, NAVY, r))
            y += 40 + len(lines) * 40 + 30
        r = prog(t, 7.8, 8.8)
        rbox(d, (X0 + 40, 775, BAND_X - 90, 865), fill=mix(TINT, WHITE, r), outline=mix(TINT, BLUE, r), width=3, r=14)
        text(d, ((X0 + BAND_X - 50) / 2, 820), key, 40, mix(TINT, NAVY, r), True, mono=True, anchor="mm")
        r2 = prog(t, 2.0, 3.0)
        text(d, (60, 948), "L'animation démarre dans un instant…", 24, mix(WHITE, GREY, r2), italic=True)
        d.rounded_rectangle((60, 985, BAND_X - 50, 993), radius=4, fill=mix(WHITE, TINT, r2))
        fr = clamp((t - 2.0) / (CARD_DUR - 3.0))
        if fr > 0: d.rounded_rectangle((60, 985, 60 + (BAND_X - 110) * fr, 993), radius=4, fill=mix(WHITE, BLUE, r2))
    return s_card


SCENES = [(s_intro, 7.0), (make_card(0), CARD_DUR), (s_binary, 34.0), (make_card(1), CARD_DUR), (s_gray, 34.0),
          (make_card(2), CARD_DUR), (s_unused, 40.0), (make_card(3), CARD_DUR), (s_elevator, 38.0), (s_outro, 12.0)]
XF, FADE = 1.5, 0.6


def frame_at(i, t):
    img = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(img)
    SCENES[i][0](img, d, t)
    return img


def render(out="diagrammes_etats.mp4"):
    starts, acc = [], 0.0
    for _, dur in SCENES:
        starts.append(acc); acc += dur - XF
    total = starts[-1] + SCENES[-1][1]
    nfr = int(total * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    white = Image.new("RGB", (W, H), WHITE)
    for f in range(nfr):
        tg = f / FPS
        act = [(i, tg - starts[i]) for i in range(len(SCENES)) if 0 <= tg - starts[i] < SCENES[i][1]]
        img = frame_at(*act[0])
        if len(act) > 1: img = Image.blend(img, frame_at(*act[1]), ease(act[1][1] / XF))
        a = min(1.0, tg / FADE, (total - tg) / FADE)
        if a < 1: img = Image.blend(white, img, max(a, 0))
        ff.stdin.write(img.tobytes())
    ff.stdin.close(); ff.wait()
    print("ok", out, f"{total:.0f} s")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        i, t = int(sys.argv[1]), float(sys.argv[2])
        frame_at(i, t).save(f"prev_{i}_{t}.png")
    else:
        render(sys.argv[1] if len(sys.argv) > 1 else "diagrammes_etats.mp4")
