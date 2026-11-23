# -*- coding: utf-8 -*-
"""Animation « Dans un microcontrôleur » – addition, multiplication (× 5), code Gray, complément à 2.
Charte ETML : bande marine à droite avec logo blanc, couleurs 242852 / 297FD5 / ACCBF9, police Arial (Liberation Sans).
Sortie : MP4 1920×1080, 25 i/s, H.264. Lancer : python3 anim.py [scene]  (scene = 0..5 pour un aperçu PNG)."""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 25
NAVY, BLUE, LBLUE, TINT, RED, GREY, WHITE = (36, 40, 82), (41, 127, 213), (172, 203, 249), (232, 239, 251), (238, 0, 0), (90, 100, 120), (255, 255, 255)
GREEN = (30, 140, 70)
BAND_X = 1776
FD = "/usr/share/fonts/truetype/liberation/"
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
LOGO = Image.open("../logo_white_v.png").convert("RGBA")
LOGO = LOGO.resize((96, int(96 * LOGO.height / LOGO.width)), Image.LANCZOS)
_vt = Image.new("RGBA", (420, 80), (0, 0, 0, 0)); ImageDraw.Draw(_vt).text((210, 40), "Electronique", font=F(40, True), fill=WHITE, anchor="mm")
VTXT = _vt.rotate(90, expand=True)


def chrome(img, d, tag, title, num):
    d.rectangle((BAND_X, 0, W, H), fill=NAVY)
    img.paste(LOGO, (BAND_X + (W - BAND_X - LOGO.width) // 2, 40), LOGO)
    img.paste(VTXT, (BAND_X + (W - BAND_X - VTXT.width) // 2, 520), VTXT)
    if num:
        d.rectangle((BAND_X + 37, 980, BAND_X + 107, 1050), fill=LBLUE)
        text(d, (BAND_X + 72, 1015), num, 26, NAVY, True, anchor="mm")
    d.line((60, 1030, BAND_X - 50, 1030), fill=BLUE, width=2)
    text(d, (60, 1040), "Section électronique", 20, NAVY, italic=True)
    text(d, (BAND_X - 50, 1040), "Test et Mesure 1 – El DT 1 · Arithmétique binaire, code Gray et compléments", 20, GREY, anchor="ra")
    if tag:
        text(d, (60, 42), tag, 24, BLUE, True)
    if title:
        text(d, (60, 78), title, 46, NAVY, True)


def caption(d, s, alpha=1.0):
    if not s: return
    col = mix(WHITE, NAVY, alpha)
    rbox(d, (60, 905, BAND_X - 50, 1005), fill=mix(WHITE, TINT, alpha), outline=None, r=14)
    lines = wrap(s, 30, BAND_X - 160)
    y0 = 955 - (len(lines) - 1) * 19
    for i, ln in enumerate(lines[:2]):
        text(d, (90, y0 + i * 38), ln, 30, col, anchor="lm")


def mcu(d, box, label="Microcontrôleur"):
    x0, y0, x1, y1 = box
    for i in range(7):  # broches
        yy = y0 + 60 + i * (y1 - y0 - 120) / 6
        d.rectangle((x0 - 18, yy - 7, x0, yy + 7), fill=GREY); d.rectangle((x1, yy - 7, x1 + 18, yy + 7), fill=GREY)
    rbox(d, box, fill=(246, 249, 255), outline=NAVY, width=4, r=22)
    d.rectangle((x0, y0, x1, y0 + 56), fill=NAVY)
    d.rounded_rectangle((x0, y0, x1, y0 + 56), radius=22, fill=NAVY)
    d.rectangle((x0, y0 + 30, x1, y0 + 56), fill=NAVY)
    text(d, (x0 + 24, y0 + 28), label, 28, WHITE, True, anchor="lm")


CELL, GAP = 72, 8
PITCH = CELL + GAP


def cells(d, x, y, bits, fill_on=LBLUE, hl=None, colors=None, alpha=None, size=40, faded=False):
    """Registre de bits ; hl = {index: couleur de cadre}, colors = {index: couleur du texte}."""
    for j, b in enumerate(bits):
        cx = x + j * PITCH
        a = 1.0 if alpha is None else alpha[j] if isinstance(alpha, (list, tuple)) else alpha
        if a <= 0:
            rbox(d, (cx, y, cx + CELL, y + CELL), fill=WHITE, outline=(205, 212, 226), width=2, r=10); continue
        fill = mix(WHITE, fill_on if b == "1" else WHITE, a)
        oc = (hl or {}).get(j, (205, 212, 226))
        rbox(d, (cx, y, cx + CELL, y + CELL), fill=fill, outline=oc, width=5 if j in (hl or {}) else 2, r=10)
        if b.strip():
            tc = mix(WHITE, (colors or {}).get(j, NAVY), a)
            text(d, (cx + CELL / 2, y + CELL / 2), b, size, tc, True, mono=True, anchor="mm")


def weights(d, x, y, ws, color=GREY, size=22):
    for j, w in enumerate(ws):
        text(d, (x + j * PITCH + CELL / 2, y), str(w), size, color, anchor="mm")


def arrow(d, p0, p1, color=BLUE, width=6):
    d.line((p0, p1), fill=color, width=width)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    a1 = (p1[0] - 22 * math.cos(ang - 0.45), p1[1] - 22 * math.sin(ang - 0.45))
    a2 = (p1[0] - 22 * math.cos(ang + 0.45), p1[1] - 22 * math.sin(ang + 0.45))
    d.polygon([p1, a1, a2], fill=color)


def display(d, box, label, value, color=NAVY):
    """Afficheur (écran LCD simplifié)."""
    rbox(d, box, fill=(30, 34, 60), outline=NAVY, width=4, r=14)
    x0, y0, x1, y1 = box
    text(d, (x0 + 22, y0 + 18), label, 24, LBLUE)
    text(d, ((x0 + x1) / 2, y1 - 44), value, 54, (190, 255, 200), True, mono=True, anchor="mm")


# ---------------------------------------------------------------- addition colonne par colonne
def add_steps(a, b, n=8):
    """Liste des colonnes de droite à gauche : (index colonne, bit a, bit b, retenue entrante, somme, retenue sortante)."""
    out, c = [], 0
    for i in range(n):
        x, y = (a >> i) & 1, (b >> i) & 1
        t = x + y + c
        out.append((n - 1 - i, x, y, c, t & 1, t >> 1)); c = t >> 1
    return out


def draw_addition(d, x, y, a, b, t, t0, dt, la="A", lb="+ B", da=None, db=None, show_rows=1.0):
    """Dessine A, B, retenues et somme avec progression colonne par colonne à partir de t0 (dt s par colonne)."""
    A, B = format(a, "08b"), format(b, "08b")
    steps = add_steps(a, b)
    k = int(clamp((t - t0) / dt, 0, 8.999)) if t >= t0 else -1
    done = [s for i, s in enumerate(steps) if t >= t0 + i * dt + dt * 0.45]
    carries = {}
    for i, s in enumerate(steps):
        if s[5] and t >= t0 + i * dt + dt * 0.7 and s[0] - 1 >= 0: carries[s[0] - 1] = "1"
    sumbits = [" "] * 8
    for s in done: sumbits[s[0]] = str(s[4])
    hl = {steps[k][0]: BLUE} if 0 <= k < 8 and t < t0 + 8 * dt else {}
    weights(d, x, y - 30, [128, 64, 32, 16, 8, 4, 2, 1])
    for j in range(8):  # retenues
        if j in carries:
            text(d, (x + j * PITCH + CELL / 2, y + 10), "1", 30, BLUE, True, mono=True, anchor="mm")
    text(d, (x - 20, y + 10), "retenues", 20, GREY, anchor="rm")
    cells(d, x, y + 34, A, hl=hl, alpha=show_rows)
    cells(d, x, y + 34 + PITCH, B, hl=hl, alpha=show_rows)
    text(d, (x - 20, y + 34 + CELL / 2), la, 30, NAVY, True, anchor="rm")
    text(d, (x - 20, y + 34 + PITCH + CELL / 2), lb, 30, NAVY, True, anchor="rm")
    if da: text(d, (x + 8 * PITCH + 14, y + 34 + CELL / 2), da, 24, GREY, anchor="lm")
    if db: text(d, (x + 8 * PITCH + 14, y + 34 + PITCH + CELL / 2), db, 24, GREY, anchor="lm")
    yl = y + 34 + 2 * PITCH + 6
    d.line((x - 60, yl, x + 8 * PITCH, yl), fill=NAVY, width=4)
    cells(d, x, yl + 14, "".join(sumbits), hl=hl, fill_on=(200, 230, 210))
    text(d, (x - 20, yl + 14 + CELL / 2), "=", 34, NAVY, True, anchor="rm")
    msg = ""
    if 0 <= k < 8 and t < t0 + 8 * dt:
        _, xa, xb, cin, sm, cout = steps[k]
        tot = xa + xb + cin
        expr = f"{xa} + {xb}" + (f" + {cin} (retenue)" if cin else "")
        msg = f"Colonne de poids {2 ** k} : {expr} = {tot} → on écrit {sm}" + (", retenue 1 vers la colonne suivante" if cout else "")
    return msg, yl + 14


# ================================================================ SCÈNES
def s_intro(img, d, t):
    chrome(img, d, "", "", "")
    p = prog(t, 0.2, 1.2)
    text(d, (110, 210), "TEST ET MESURE 1 – EL DT 1 · ANIMATION", 30, mix(WHITE, BLUE, p), True)
    text(d, (110, 270), "Dans un microcontrôleur", 92, mix(WHITE, NAVY, p), True)
    text(d, (110, 390), "4 notions de binaire, 4 usages réels", 44, mix(WHITE, GREY, p))
    items = [("1", "Addition", "compter les pièces d'une chaîne de production"),
             ("2", "Multiplication × 5", "convertir la mesure d'un capteur en millivolts"),
             ("3", "Code Gray", "lire le bouton de volume d'un autoradio"),
             ("4", "Complément à 2", "afficher une température négative")]
    for i, (n, a, b) in enumerate(items):
        q = prog(t, 1.4 + i * 0.6, 2.0 + i * 0.6)
        y = 520 + i * 100
        x = 110 + (1 - q) * 60
        if q <= 0: continue
        d.ellipse((x, y, x + 70, y + 70), fill=mix(WHITE, NAVY, q))
        text(d, (x + 35, y + 35), n, 36, WHITE, True, anchor="mm")
        text(d, (x + 100, y + 35), a, 40, mix(WHITE, NAVY, q), True, anchor="lm")
        text(d, (x + 520, y + 35), b, 34, mix(WHITE, GREY, q), anchor="lm")


def belt(d, x, y, w, t, speed, label, count):
    rbox(d, (x, y, x + w, y + 46), fill=(215, 220, 232), outline=GREY, width=2, r=23)
    for k in range(int(w / 60) + 1):
        cx = x + 23 + k * 60
        if cx < x + w - 10: d.ellipse((cx - 9, y + 14, cx + 9, y + 32), outline=GREY, width=2)
    off = (t * speed) % 110
    for k in range(-1, int(w / 110) + 1):
        px = x + 20 + k * 110 + off
        if x + 10 < px < x + w - 70: rbox(d, (px, y - 52, px + 52, y), fill=BLUE, outline=NAVY, width=2, r=6)
    sx = x + w - 30  # capteur
    d.polygon([(sx, y - 120), (sx - 22, y - 80), (sx + 22, y - 80)], fill=NAVY)
    d.line((sx, y - 80, sx, y - 4), fill=(238, 0, 0), width=2)
    text(d, (x, y + 70), label, 28, NAVY, True)
    text(d, (x + w, y + 70), f"{count} pièces", 30, BLUE, True, mono=True, anchor="ra")


def s_add(img, d, t):
    chrome(img, d, "1 · ADDITION BINAIRE", "Compter les pièces de deux lignes de production", "1/4")
    text(d, (60, 160), "Dans la vraie vie", 30, BLUE, True)
    c1 = int(round(91 * prog(t, 0.5, 4.0))); c2 = int(round(54 * prog(t, 0.5, 4.0)))
    belt(d, 60, 340, 640, t, 70 if t < 4 else 0, "Ligne 1", c1)
    belt(d, 60, 600, 640, t, 55 if t < 4 else 0, "Ligne 2", c2)
    T0, DT = 6.5, 1.55
    tot = "145 pièces" if t >= T0 + 8 * DT + 0.5 else "?"
    display(d, (60, 745, 700, 875), "Total affiché", tot)
    mcu(d, (820, 170, 1740, 870), "Microcontrôleur · unité de calcul (UAL)")
    p = prog(t, 4.0, 5.5)
    if p > 0:
        arrow(d, (710, 380), (816, 400), mix(WHITE, BLUE, p)); arrow(d, (710, 640), (816, 540), mix(WHITE, BLUE, p))
    msg, ys = draw_addition(d, 960, 340, 91, 54, t, T0, DT, "A", "+ B", "91d", "54d", show_rows=p)
    text(d, (960, 260), "Registres 8 bits", 26, GREY, italic=True)
    if t >= T0 + 8 * DT + 0.3:
        q = prog(t, T0 + 8 * DT + 0.3, T0 + 8 * DT + 1.3)
        text(d, (960 + 8 * PITCH + 14, ys + CELL / 2), "145d", 32, mix(WHITE, GREEN, q), True, anchor="lm")
        text(d, (960, ys + CELL + 40), "= 128 + 16 + 1 = 145d", 30, mix(WHITE, NAVY, q))
        arrow(d, (816, 800), (712, 810), mix(WHITE, BLUE, q))
    if t < 4: cap = "Deux capteurs comptent les pièces. Le microcontrôleur doit additionner les deux compteurs."
    elif t < T0: cap = "Les compteurs sont rangés en binaire dans deux registres de 8 bits : 91d = 0101 1011b, 54d = 0011 0110b."
    elif msg: cap = msg
    elif t < T0 + 8 * DT + 3: cap = "Résultat : 1001 0001b = 145d. Il tient dans 8 bits (maximum 255) : l'afficheur montre 145 pièces."
    else: cap = "L'UAL additionne toujours ainsi : colonne par colonne, de droite à gauche, avec les retenues."
    caption(d, cap)


def s_mul(img, d, t):
    chrome(img, d, "2 · MULTIPLICATION × 5", "Convertir la mesure d'un capteur en millivolts", "2/4")
    text(d, (60, 160), "Dans la vraie vie", 30, BLUE, True)
    rbox(d, (60, 230, 330, 400), fill=TINT, outline=NAVY, width=3)
    text(d, (195, 280), "Capteur", 32, NAVY, True, anchor="mm")
    text(d, (195, 340), "valeur 23", 30, BLUE, True, mono=True, anchor="mm")
    para(d, (60, 440), "1 pas = 5 mV, donc tension = valeur × 5.", 30, 680)
    para(d, (60, 540), "Ce microcontrôleur n'a pas d'instruction de multiplication : il décale et il additionne.", 28, 680, GREY)
    done = t >= 23.5
    display(d, (60, 745, 700, 875), "Tension", "115 mV" if done else "? mV")
    mcu(d, (820, 170, 1740, 870), "Microcontrôleur")
    arrow(d, (334, 315), (816, 315), mix(WHITE, BLUE, prog(t, 1.0, 2.5)))
    x, y = 960, 300
    weights(d, x, y - 30, [128, 64, 32, 16, 8, 4, 2, 1])
    val = 23
    # décalages
    stage_txt = ""; p = 1
    if t < 5:
        bits = format(val, "08b"); cells(d, x, y, bits, alpha=prog(t, 2.5, 3.5)); lab = "23d"
    elif t < 11:
        k = 0 if t < 8 else 1
        p = prog(t, 5.6 + 3 * k, 7.0 + 3 * k)
        cur = format(val << k, "08b")
        # cellules vides puis bits qui glissent
        cells(d, x, y, " " * 8)
        for j, bch in enumerate(cur):
            px = x + j * PITCH - p * PITCH
            if px < x - CELL * 0.5:
                a = clamp(1 - (x - px) / PITCH)
            else:
                a = 1
            if px < x - CELL * 0.6: continue
            rbox(d, (px, y, px + CELL, y + CELL), fill=mix(WHITE, LBLUE if bch == "1" else WHITE, a), outline=(205, 212, 226), width=2, r=10)
            text(d, (px + CELL / 2, y + CELL / 2), bch, 40, mix(WHITE, NAVY, a), True, mono=True, anchor="mm")
        nx = x + 7 * PITCH + (1 - p) * PITCH
        rbox(d, (nx, y, nx + CELL, y + CELL), fill=WHITE, outline=BLUE, width=4, r=10)
        text(d, (nx + CELL / 2, y + CELL / 2), "0", 40, BLUE, True, mono=True, anchor="mm")
        lab = f"{val << (k + (1 if p >= 1 else 0))}d"
        stage_txt = "× 2" if k == 0 else "× 4"
    else:
        cells(d, x, y, format(val << 2, "08b")); lab = "92d"
    if t >= 5:
        if t >= 11: text(d, (x - 20, y + CELL / 2), "23 × 4", 26, NAVY, True, anchor="rm")
    if not stage_txt or p >= 1 or p <= 0:
        text(d, (x + 8 * PITCH + 14, y + CELL / 2), lab, 30, GREY, anchor="lm")
    if stage_txt and t >= 5.6:
        text(d, (x, y + CELL + 30), "un 0 entre à droite, tout glisse d'un rang", 24, BLUE, italic=True)
    # addition
    if t >= 11:
        msg, ys = draw_addition(d, x, 470, 92, 23, t, 13.0, 1.1, "23 × 4", "+ 23", "92d", "23d", show_rows=prog(t, 11, 12.5))
        if t >= 13.0 + 8 * 1.1 + 0.3:
            q = prog(t, 22.2, 23.2)
            text(d, (x + 8 * PITCH + 14, ys + CELL / 2), "115d", 32, mix(WHITE, GREEN, q), True, anchor="lm")
            arrow(d, (816, 800), (712, 810), mix(WHITE, BLUE, q))
    else:
        msg = ""
    if t < 2.5: cap = "Le capteur envoie la valeur 23. Tension = 23 × 5 mV. Astuce : 5 = 4 + 1."
    elif t < 5: cap = "23d = 0001 0111b. Pour multiplier par 4, on décale deux fois d'un rang vers la gauche."
    elif t < 8: cap = "1er décalage : chaque bit glisse d'un rang à gauche, un 0 entre à droite → × 2 = 46d."
    elif t < 11: cap = "2e décalage → × 4 = 0101 1100b = 92d. Il reste à ajouter 23 une fois (le « + 1 » de 4 + 1)."
    elif t < 13: cap = "On additionne 23 × 4 et 23 : 92d + 23d."
    elif msg: cap = msg
    elif t < 26: cap = "0111 0011b = 64 + 32 + 16 + 2 + 1 = 115d → la tension affichée est 115 mV."
    else: cap = "× 5 = 2 décalages + 1 addition : c'est la méthode des produits partiels, sans multiplieur."
    caption(d, cap)


GRAY_SEQ = [("00", 0), ("01", +1), ("11", +1), ("10", +1), ("00", +1), ("10", -1), ("11", -1)]


def s_gray(img, d, t):
    chrome(img, d, "3 · CODE GRAY", "Lire le bouton de volume d'un autoradio", "3/4")
    text(d, (60, 160), "Dans la vraie vie", 30, BLUE, True)
    T0, DTC = 3.0, 2.3
    # état courant
    n = 0; p_rot = 0.0
    for i in range(1, len(GRAY_SEQ)):
        ts = T0 + (i - 1) * DTC
        if t >= ts: n = i - 1; p_rot = prog(t, ts, ts + 0.6)
    if t >= T0 + (len(GRAY_SEQ) - 1) * DTC: n = len(GRAY_SEQ) - 1; p_rot = 0
    idx = n if p_rot < 1 else n + 1
    idx = min(idx, len(GRAY_SEQ) - 1)
    angle = 0.0; vol = 20
    for i in range(1, idx + 1): angle += 30 * GRAY_SEQ[i][1]; vol += GRAY_SEQ[i][1]
    if 0 < p_rot < 1 and n + 1 < len(GRAY_SEQ): angle += 30 * GRAY_SEQ[n + 1][1] * p_rot - 0
    ab = GRAY_SEQ[idx][0]
    prev = GRAY_SEQ[idx - 1][0] if idx > 0 else None
    changed = {i for i in range(2) if prev and prev[i] != ab[i]}
    direction = GRAY_SEQ[idx][1] if idx > 0 else 0
    # bouton
    cx, cy, R = 250, 420, 150
    d.ellipse((cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14), fill=(215, 220, 232))
    for k in range(24):
        a = math.radians(angle + k * 15)
        d.line((cx + (R + 2) * math.cos(a), cy + (R + 2) * math.sin(a), cx + (R + 12) * math.cos(a), cy + (R + 12) * math.sin(a)), fill=GREY, width=3)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=NAVY)
    a = math.radians(angle - 90)
    d.line((cx + 30 * math.cos(a), cy + 30 * math.sin(a), cx + (R - 18) * math.cos(a), cy + (R - 18) * math.sin(a)), fill=WHITE, width=10)
    text(d, (cx, cy + R + 50), "bouton de volume", 26, GREY, anchor="mm")
    if 0 < p_rot < 1:
        text(d, (cx, cy - R - 45), "↻ horaire" if GRAY_SEQ[n + 1][1] > 0 else "↺ antihoraire", 30, BLUE, True, anchor="mm")
    # contacts A et B
    for i, lab in enumerate("AB"):
        x0 = 480 + i * 120
        on = ab[i] == "1"
        d.ellipse((x0, 330, x0 + 80, 410), fill=BLUE if on else WHITE, outline=NAVY, width=4)
        text(d, (x0 + 40, 370), ab[i], 36, WHITE if on else NAVY, True, mono=True, anchor="mm")
        text(d, (x0 + 40, 440), f"contact {lab}", 22, NAVY, anchor="mm")
    display(d, (60, 745, 700, 875), "Volume", f"{vol}")
    # microcontrôleur
    mcu(d, (820, 170, 1740, 870), "Microcontrôleur")
    arrow(d, (720, 370), (816, 330), BLUE)
    x = 960
    text(d, (x - 20, 300), "A B", 30, NAVY, True, anchor="rm")
    cells(d, x, 264, ab, hl={i: RED if False else BLUE for i in changed})
    if changed and t < T0 + (len(GRAY_SEQ) - 1) * DTC + 1:
        text(d, (x + 2 * PITCH + 20, 300), f"seul {'AB'[list(changed)[0]]} change", 28, BLUE, True, anchor="lm")
    # historique / chronogramme
    hist = [s for s, _ in GRAY_SEQ[:idx + 1]]
    text(d, (x - 20, 420), "suite lue", 24, GREY, anchor="rm")
    for k, s in enumerate(hist):
        bx = x + k * 92
        rbox(d, (bx, 392, bx + 82, 448), fill=TINT if GRAY_SEQ[k][1] >= 0 else (255, 235, 220), outline=BLUE, width=2, r=8)
        text(d, (bx + 41, 420), s, 28, NAVY, True, mono=True, anchor="mm")
    for row, lab in enumerate("AB"):
        y0 = 500 + row * 80
        text(d, (x - 20, y0 + 25), lab, 28, NAVY, True, anchor="rm")
        pts = []
        for k, s in enumerate(hist):
            yy = y0 + (0 if s[row] == "1" else 50)
            pts += [(x + k * 92, yy), (x + k * 92 + 92, yy)]
        if pts: d.line(pts, fill=NAVY, width=5, joint="curve")
    # registre volume
    text(d, (x - 20, 720), "volume", 26, NAVY, True, anchor="rm")
    cells(d, x, 684, format(vol, "08b"))
    text(d, (x + 8 * PITCH + 14, 720), f"{vol}d", 30, GREY, anchor="lm")
    if direction and 0 < (t - (T0 + (idx - 1) * DTC + 0.6)) < 1.2:
        text(d, (x, 790), "+1 : sens horaire" if direction > 0 else "−1 : sens antihoraire", 28, GREEN if direction > 0 else RED, True)
    # binaire naturel : la lecture fausse
    TB = T0 + (len(GRAY_SEQ) - 1) * DTC + 1.0
    if t >= TB:
        q = prog(t, TB, TB + 0.6)
        rbox(d, (836, 232, 1724, 860), fill=mix((246, 249, 255), WHITE, q), outline=mix((246, 249, 255), RED, q), width=4, r=18)
        if q > 0.5:
            text(d, (900, 280), "Et si on utilisait le binaire naturel ?", 34, NAVY, True)
            text(d, (900, 340), "01 → 10 : les deux contacts changent en même temps", 28, NAVY)
            ph = (t - TB - 1.0) % 3.0
            steps_b = [("01", NAVY, "avant"), ("11", RED, "lecture fausse : A bascule avant B !"), ("10", NAVY, "après")]
            for k, (s, col, lab) in enumerate(steps_b):
                show = ph >= k * 0.8
                bx = 900 + k * 260
                if show:
                    rbox(d, (bx, 430, bx + 200, 530), fill=(255, 225, 225) if col == RED else TINT, outline=col, width=4, r=12)
                    text(d, (bx + 100, 480), s, 50, col, True, mono=True, anchor="mm")
            if ph >= 0.8:
                para(d, (900, 580), "Le microcontrôleur lit brièvement 11 : il croit que le bouton a tourné à l'envers et le volume saute.", 28, 740, RED)
            para(d, (900, 740), "En code Gray, un seul contact change à chaque cran : jamais de lecture fausse.", 28, 780, GREEN, True)
    if t < T0: cap = "Le bouton tourne sans butée. Deux contacts A et B s'ouvrent et se ferment à chaque cran."
    elif t < T0 + 4 * DTC: cap = "Sens horaire : 00 → 01 → 11 → 10 → 00. C'est le code Gray à 2 bits : un seul bit change par cran. Volume + 1."
    elif t < TB: cap = "Sens antihoraire : la suite est lue à l'envers (00 → 10 → 11). Le microcontrôleur enlève 1 au volume."
    else: cap = "Le code Gray évite les lectures fausses : on le trouve dans les boutons rotatifs, molettes et codeurs d'angle."
    caption(d, cap)


def s_c2(img, d, t):
    chrome(img, d, "4 · COMPLÉMENT À 2", "Afficher une température négative", "4/4")
    text(d, (60, 160), "Dans la vraie vie", 30, BLUE, True)
    # serre + thermomètre
    d.polygon([(80, 420), (240, 280), (400, 420)], fill=TINT, outline=NAVY)
    d.rectangle((100, 420, 380, 600), fill=TINT, outline=NAVY, width=3)
    for k in range(3): d.line((100 + k * 93, 420, 100 + k * 93, 600), fill=LBLUE, width=2)
    text(d, (240, 640), "serre, la nuit", 26, GREY, anchor="mm")
    d.rounded_rectangle((470, 300, 510, 560), radius=20, fill=WHITE, outline=NAVY, width=3)
    d.ellipse((455, 540, 525, 610), fill=BLUE, outline=NAVY, width=3)
    lvl = 470 if t < 30 else 470
    d.rectangle((482, lvl, 498, 560), fill=BLUE)
    text(d, (540, 330), "capteur", 26, NAVY, True)
    text(d, (540, 365), "numérique", 26, NAVY, True)
    T1, T2, T3 = 3.0, 12.0, 22.0
    temp = "−10 °C" if t >= T1 + 7.5 else "? °C"
    lab2 = "Écart jour/nuit" if t >= T3 + 6 else "Température"
    val2 = "35 °C" if t >= T3 + 6 else temp
    display(d, (60, 745, 700, 875), lab2, val2)
    mcu(d, (820, 170, 1740, 870), "Microcontrôleur")
    x = 960
    frame = "11110110"
    # bits qui voyagent dans le fil
    if T1 - 2 < t < T1 + 1.5:
        p = prog(t, T1 - 2, T1 + 1.2)
        fx = 600 + p * 300
        text(d, (fx, 455), "1111 0110", 30, BLUE, True, mono=True, anchor="mm")
    d.line((600, 480, 816, 480), fill=BLUE, width=4)
    ws = ["−128", "64", "32", "16", "8", "4", "2", "1"]
    if t < T2:
        weights(d, x, 270, ws, color=NAVY, size=24)
        cells(d, x, 300, frame, alpha=prog(t, T1, T1 + 1.0))
        text(d, (x - 20, 336), "reçu", 28, NAVY, True, anchor="rm")
        # décodage progressif
        ones = [j for j, c in enumerate(frame) if c == "1"]
        parts = []
        for k, j in enumerate(ones):
            if t >= T1 + 1.5 + k * 0.9:
                parts.append(ws[j])
                rbox(d, (x + j * PITCH - 4, 296, x + j * PITCH + CELL + 4, 304 + CELL), outline=BLUE, width=4, r=12)
        if parts:
            s = " + ".join(parts).replace("+ −", "− ")
            text(d, (x, 440), s, 32, NAVY, True)
        if t >= T1 + 7.0:
            text(d, (x, 500), "= −10 → l'afficheur montre −10 °C", 34, GREEN, True)
        text(d, (x, 600), "Le bit de gauche pèse −128 : c'est le bit de signe.", 26, GREY, italic=True)
    elif t < T3:
        # fabriquer −10 : +10 → C1 → +1
        r1, r2, r3 = "00001010", "11110101", "11110110"
        text(d, (x, 230), "Comment le capteur écrit −10 ?", 30, NAVY, True)
        cells(d, x, 290, r1); text(d, (x - 20, 326), "+10", 28, NAVY, True, anchor="rm")
        p = prog(t, T2 + 2.0, T2 + 4.0)
        k = int(p * 8)
        inv = "".join(r2[j] if j < k else r1[j] for j in range(8))
        if t >= T2 + 2.0:
            cells(d, x, 400, inv, hl={j: BLUE for j in range(min(k + 1, 8))} if p < 1 else None)
            text(d, (x - 20, 436), "C1", 28, NAVY, True, anchor="rm")
            text(d, (x + 8 * PITCH + 14, 436), "inversé", 24, GREY, anchor="lm")
        if t >= T2 + 5.0:
            cells(d, x, 510, "0000000" + "1", alpha=prog(t, T2 + 5.0, T2 + 5.6))
            text(d, (x - 20, 546), "+ 1", 28, NAVY, True, anchor="rm")
            d.line((x - 60, 600, x + 8 * PITCH, 600), fill=NAVY, width=4)
        if t >= T2 + 6.5:
            cells(d, x, 614, r3, alpha=prog(t, T2 + 6.5, T2 + 7.3), fill_on=(200, 230, 210))
            text(d, (x - 20, 650), "C2", 28, NAVY, True, anchor="rm")
            text(d, (x + 8 * PITCH + 14, 650), "= −10", 30, GREEN, True, anchor="lm")
    else:
        text(d, (x, 230), "Écart : 25 − (−10) = 25 + 10", 30, NAVY, True)
        msg, ys = draw_addition(d, x, 330, 25, 10, t, T3 + 1.0, 0.6, "+25", "+10", "25d", "−(−10)", show_rows=prog(t, T3, T3 + 1))
        if t >= T3 + 6:
            text(d, (x + 8 * PITCH + 14, ys + CELL / 2), "35d", 32, GREEN, True, anchor="lm")
            text(d, (x, ys + CELL + 40), "soustraire = additionner le complément à 2", 28, NAVY, italic=True)
    if t < T1: cap = "La nuit, le capteur de la serre mesure une température négative et l'envoie en binaire sur 8 bits."
    elif t < T1 + 7.0: cap = "Le microcontrôleur reçoit 1111 0110b. En complément à 2, le bit de gauche vaut −128 : on additionne les poids des 1."
    elif t < T2: cap = "−128 + 64 + 32 + 16 + 4 + 2 = −10 : l'afficheur montre −10 °C."
    elif t < T2 + 5: cap = "Pour écrire −10, on part de +10 = 0000 1010b et on inverse chaque bit : c'est le complément à 1."
    elif t < T3: cap = "On ajoute 1 : 1111 0110b. C'est le complément à 2, exactement ce qu'envoie le capteur."
    elif t < T3 + 6: cap = "Midi : +25 °C. Écart = 25 − (−10) : le processeur additionne le complément à 2 de −10, soit +10."
    else: cap = "0010 0011b = 35d : l'écart jour/nuit est de 35 °C, calculé avec le seul additionneur."
    caption(d, cap)


def s_outro(img, d, t):
    chrome(img, d, "RÉCAPITULATIF", "Ce que fait le microcontrôleur", "")
    rows = [("Addition", "colonne par colonne avec retenues", "compteur de pièces"),
            ("× 2, × 4, × 5", "décaler + additionner", "mesure convertie en mV"),
            ("Code Gray", "un seul bit change à la fois", "bouton de volume, codeur d'angle"),
            ("Complément à 2", "inverser puis + 1 ; MSB = −128", "température négative, soustraction")]
    for i, (a, b, c) in enumerate(rows):
        q = prog(t, 0.3 + i * 0.5, 0.9 + i * 0.5)
        if q <= 0: continue
        y = 200 + i * 150
        rbox(d, (60, y, BAND_X - 50, y + 120), fill=mix(WHITE, TINT, q), r=16)
        d.ellipse((90, y + 25, 160, y + 95), fill=mix(WHITE, NAVY, q))
        text(d, (125, y + 60), str(i + 1), 36, WHITE, True, anchor="mm")
        text(d, (200, y + 60), a, 40, mix(WHITE, NAVY, q), True, anchor="lm")
        text(d, (620, y + 60), b, 32, mix(WHITE, NAVY, q), anchor="lm")
        text(d, (1200, y + 60), c, 30, mix(WHITE, BLUE, q), True, anchor="lm")
    caption(d, "À toi : feuille d'exercices N°1 à N°11 (Test et Mesure 1 – El DT 1).", prog(t, 2.5, 3.2))


# ================================================================ CARTES DE TRANSITION (titre + situation, le temps de lire)
def knob(d, cx, cy, R, angle):
    d.ellipse((cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14), fill=(215, 220, 232))
    for k in range(24):
        a = math.radians(angle + k * 15)
        d.line((cx + (R + 2) * math.cos(a), cy + (R + 2) * math.sin(a), cx + (R + 12) * math.cos(a), cy + (R + 12) * math.sin(a)), fill=GREY, width=3)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=NAVY)
    a = math.radians(angle - 90)
    d.line((cx + 30 * math.cos(a), cy + 30 * math.sin(a), cx + (R - 18) * math.cos(a), cy + (R - 18) * math.sin(a)), fill=WHITE, width=10)


def ill_add(d, t, a):
    belt(d, 80, 380, 620, t, 45, "Ligne 1", 91)
    belt(d, 80, 640, 620, t, 35, "Ligne 2", 54)
    display(d, (80, 750, 700, 885), "Total affiché", "91 + 54 = ?")


def ill_mul(d, t, a):
    rbox(d, (80, 250, 330, 400), fill=TINT, outline=NAVY, width=3)
    text(d, (205, 295), "Capteur", 32, NAVY, True, anchor="mm")
    text(d, (205, 350), "valeur 23", 30, BLUE, True, mono=True, anchor="mm")
    arrow(d, (334, 325), (440, 325))
    display(d, (450, 260, 720, 390), "Tension", "? mV")
    # escalier : 1 pas = 5 mV
    x0, y0, sx, sy = 150, 850, 82, 52
    d.line((x0, y0, x0 + 6 * sx + 40, y0), fill=NAVY, width=3); d.line((x0, y0, x0, y0 - 6 * sy - 30), fill=NAVY, width=3)
    n = min(6, 1 + int(max(t - 1.5, 0) * 0.9))
    pts = [(x0, y0)]
    for k in range(n):
        pts += [(x0 + k * sx, y0 - (k + 1) * sy), (x0 + (k + 1) * sx, y0 - (k + 1) * sy)]
    d.line(pts, fill=BLUE, width=6)
    for k in range(6):
        text(d, (x0 - 14, y0 - (k + 1) * sy), f"{5 * (k + 1)}", 22, GREY, anchor="rm")
        text(d, (x0 + k * sx + sx / 2, y0 + 24), str(k + 1), 22, GREY, anchor="mm")
    text(d, (x0 - 14, y0 - 6 * sy - 40), "mV", 22, GREY, True, anchor="rm")
    text(d, (x0 + 6 * sx + 45, y0), "pas", 22, GREY, True, anchor="lm")
    text(d, (x0 + 30, y0 - 6 * sy - 54), "1 pas = 5 mV", 28, BLUE, True)


def ill_gray(d, t, a):
    step = int(t / 1.6) % 4
    seq = ["00", "01", "11", "10"]
    ang = step * 30 + 30 * prog(t % 1.6, 0, 0.5)
    knob(d, 270, 520, 190, ang)
    text(d, (270, 760), "bouton de volume", 26, GREY, anchor="mm")
    ab = seq[(step + (1 if (t % 1.6) > 0.5 else 0)) % 4]
    for i, lab in enumerate("AB"):
        x0 = 540 + i * 110
        on = ab[i] == "1"
        d.ellipse((x0, 450, x0 + 84, 534), fill=BLUE if on else WHITE, outline=NAVY, width=4)
        text(d, (x0 + 42, 492), ab[i], 38, WHITE if on else NAVY, True, mono=True, anchor="mm")
        text(d, (x0 + 42, 562), f"contact {lab}", 22, NAVY, anchor="mm")
    display(d, (80, 800, 700, 890), "", "VOL  −  /  +")


def ill_c2(d, t, a):
    d.ellipse((560, 230, 640, 310), fill=(250, 220, 120))
    d.ellipse((585, 220, 665, 300), fill=WHITE)  # croissant de lune
    d.polygon([(100, 470), (290, 300), (480, 470)], fill=TINT, outline=NAVY)
    d.rectangle((120, 470, 460, 690), fill=TINT, outline=NAVY, width=3)
    for k in range(3): d.line((120 + k * 113, 470, 120 + k * 113, 690), fill=LBLUE, width=2)
    text(d, (290, 725), "serre, la nuit", 26, GREY, anchor="mm")
    d.rounded_rectangle((560, 380, 604, 650), radius=22, fill=WHITE, outline=NAVY, width=3)
    d.ellipse((544, 630, 620, 706), fill=BLUE, outline=NAVY, width=3)
    lvl = 560 + 40 * math.sin(t * 0.8) ** 2
    d.rectangle((575, lvl, 589, 650), fill=BLUE)
    text(d, (582, 365), "°C", 24, NAVY, True, anchor="mm")
    display(d, (80, 750, 700, 885), "Température", "−10 °C ?")


CARDS = [
    ("1", "Addition binaire", "Compter les pièces de deux lignes de production", ill_add,
     "Dans une usine, deux capteurs comptent les pièces qui passent sur deux tapis : 91 sur la ligne 1, 54 sur la ligne 2.",
     "Combien de pièces au total ? L'afficheur doit montrer la somme.",
     "Les deux compteurs sont additionnés en binaire, colonne par colonne, avec les retenues.", "91 + 54 = ?"),
    ("2", "Multiplication × 5", "Convertir la mesure d'un capteur en millivolts", ill_mul,
     "Un capteur envoie une valeur numérique : 23. Chaque pas de mesure vaut 5 mV.",
     "Quelle tension afficher ? Il faut calculer 23 × 5.",
     "Ce microcontrôleur n'a pas de multiplieur : il décale à gauche (× 2, × 4) puis il additionne.", "23 × 5 = 23 × 4 + 23"),
    ("3", "Code Gray", "Lire le bouton de volume d'un autoradio", ill_gray,
     "Le bouton tourne sans fin. À chaque cran, deux contacts A et B s'ouvrent ou se ferment.",
     "Comment savoir dans quel sens on tourne, sans jamais se tromper ?",
     "Il lit A et B : en code Gray, un seul contact change à chaque cran.", "00 → 01 → 11 → 10"),
    ("4", "Complément à 2", "Afficher une température négative", ill_c2,
     "La nuit, le capteur d'une serre mesure −10 °C et envoie la valeur sur 8 bits.",
     "Comment écrire un nombre négatif avec seulement des 0 et des 1 ?",
     "Le bit de gauche vaut −128 : c'est le complément à 2. Il sert aussi à soustraire.", "1111 0110b = ?"),
]
CARD_DUR = 12.0


def make_card(k):
    num, title, use, ill, situ, quest, mcu_txt, key = CARDS[k]

    def s_card(img, d, t):
        chrome(img, d, "", "", f"{num}/4")
        # bandeau titre
        p = prog(t, 0.0, 1.0)
        d.ellipse((60, 40, 150, 130), fill=mix(WHITE, NAVY, p))
        text(d, (105, 85), num, 50, WHITE, True, anchor="mm")
        text(d, (180, 40), f"DÉMONSTRATION {num} / 4", 24, mix(WHITE, BLUE, p), True)
        text(d, (180, 70), title, 60, mix(WHITE, NAVY, p), True)
        text(d, (180, 150), use, 34, mix(WHITE, GREY, prog(t, 0.6, 1.6)), italic=True)
        # illustration
        q = prog(t, 1.2, 2.4)
        lay = Image.new("RGB", (BAND_X, H), WHITE); dl = ImageDraw.Draw(lay)
        ill(dl, t, q)
        box = (40, 220, 760, 900)
        reg = lay.crop(box)
        img.paste(Image.blend(Image.new("RGB", reg.size, WHITE), reg, q), box[:2])
        # panneau de lecture
        X0 = 820
        rbox(d, (X0, 220, BAND_X - 50, 900), fill=mix(WHITE, TINT, prog(t, 1.5, 2.5)), r=20)
        blocks = [("La situation", situ, 2.0), ("La question", quest, 4.0), ("Dans le microcontrôleur", mcu_txt, 6.0)]
        y = 255
        for head, body, t0 in blocks:
            r = prog(t, t0, t0 + 1.0)
            text(d, (X0 + 40, y), head.upper(), 24, mix(TINT, BLUE, r), True)
            lines = wrap(body, 32, BAND_X - 50 - X0 - 80)
            for i, ln in enumerate(lines):
                text(d, (X0 + 40 + (1 - r) * 30, y + 40 + i * 42), ln, 32, mix(TINT, NAVY, r))
            y += 40 + len(lines) * 42 + 36
        r = prog(t, 7.8, 8.8)
        rbox(d, (X0 + 40, 770, BAND_X - 90, 860), fill=mix(TINT, WHITE, r), outline=mix(TINT, BLUE, r), width=3, r=14)
        text(d, ((X0 + BAND_X - 50) / 2, 815), key, 44, mix(TINT, NAVY, r), True, mono=True, anchor="mm")
        # barre d'attente
        r2 = prog(t, 2.0, 3.0)
        text(d, (60, 948), "L'animation démarre dans un instant…", 24, mix(WHITE, GREY, r2), italic=True)
        d.rounded_rectangle((60, 985, BAND_X - 50, 993), radius=4, fill=mix(WHITE, TINT, r2))
        fr = clamp((t - 2.0) / (CARD_DUR - 3.0))
        if fr > 0:
            d.rounded_rectangle((60, 985, 60 + (BAND_X - 110) * fr, 993), radius=4, fill=mix(WHITE, BLUE, r2))
    return s_card


SCENES = [(s_intro, 7.0), (make_card(0), CARD_DUR), (s_add, 28.0), (make_card(1), CARD_DUR), (s_mul, 30.0),
          (make_card(2), CARD_DUR), (s_gray, 35.0), (make_card(3), CARD_DUR), (s_c2, 34.0), (s_outro, 8.0)]
XF = 1.5      # fondu enchaîné entre deux scènes (s)
FADE = 0.6    # fondu depuis/vers le blanc au début et à la fin


def frame_at(i, t):
    img = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(img)
    SCENES[i][0](img, d, t)
    return img


def render(out="animation.mp4"):
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
        if len(act) > 1:
            img = Image.blend(img, frame_at(*act[1]), ease(act[1][1] / XF))
        a = min(1.0, tg / FADE, (total - tg) / FADE)
        if a < 1: img = Image.blend(white, img, max(a, 0))
        ff.stdin.write(img.tobytes())
    ff.stdin.close(); ff.wait()
    print("ok", out, f"{total:.0f} s")


if __name__ == "__main__":
    if len(sys.argv) > 2:   # aperçu : python3 anim.py scene t
        i, t = int(sys.argv[1]), float(sys.argv[2])
        frame_at(i, t).save(f"prev_{i}_{t}.png")
    else:
        render()
