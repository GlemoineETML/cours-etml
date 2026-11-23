# -*- coding: utf-8 -*-
"""Briques communes des animations 105 et 125 (TM1 – El DT 1, semaine 1).
Reprend le cadre de generateurs/anim_diagrammes_etats.py : 1920×1080, 25 i/s, H.264, charte ETML
(bande marine à droite avec logo blanc, couleurs 242852 / 297FD5 / ACCBF9), Liberation Sans (métrique d'Arial).
Symboles de portes selon CEI 60617-12 (rectangle, qualificatif, cercle de négation).
Aperçu d'une image : python3 anim_10x.py <scène> <t>"""
import math, os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 25
NAVY, BLUE, LBLUE, TINT, RED, GREY, WHITE = (36, 40, 82), (41, 127, 213), (172, 203, 249), (232, 239, 251), (238, 0, 0), (90, 100, 120), (255, 255, 255)
GREEN, LGREY, ORANGE, PALE = (30, 140, 70), (200, 206, 218), (230, 120, 20), (247, 249, 253)
PINK, LGREEN = (255, 228, 228), (222, 244, 228)
BAND_X = 1776
FD = "/usr/share/fonts/truetype/liberation/"
HERE = os.path.dirname(os.path.abspath(__file__))
NB = " "
_fc = {}


def F(size, bold=False, mono=False, italic=False):
    k = (int(size), bold, mono, italic)
    if k not in _fc:
        name = ("LiberationMono-" if mono else "LiberationSans-") + ("BoldItalic" if bold and italic else "Bold" if bold else "Italic" if italic else "Regular") + ".ttf"
        _fc[k] = ImageFont.truetype(FD + name, int(size))
    return _fc[k]


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def prog(t, a, b): return ease((t - a) / (b - a)) if b > a else float(t >= a)
def mix(c1, c2, p): return tuple(int(c1[i] + (c2[i] - c1[i]) * clamp(p)) for i in range(3))


def text(d, xy, s, size, color=NAVY, bold=False, mono=False, italic=False, anchor="la"):
    d.text(xy, s, font=F(size, bold, mono, italic), fill=color, anchor=anchor)


import re as _re


def nb(s):
    """Espaces insécables : nombre + unité, avant : ; ? !, « A = 1 », plages « 0 … 70 »."""
    s = _re.sub(r"(\d) (?=(V|°C|ns|ms|mA|µA|%|s|L)\b)", "\\1" + NB, s)
    s = _re.sub(r"(\d) (?=°C)", "\\1" + NB, s)
    s = _re.sub(r" ([:;?!»])", NB + "\\1", s).replace("« ", "«" + NB)
    s = _re.sub(r"(\d) … (\d|−)", "\\1" + NB + "…" + NB + "\\2", s)
    s = _re.sub(r"(\b\w{1,3}) = (\w{1,3}\b)", "\\1" + NB + "=" + NB + "\\2", s)
    s = _re.sub(r"(\d) (?=[a-zà-ÿ])", "\\1" + NB, s)
    s = _re.sub(r"(\w) · (\w)", "\\1" + NB + "·" + NB + "\\2", s)
    return s


def wrap(s, size, width, bold=False, italic=False):
    s = nb(s)
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
    lines = wrap(s, size, width, bold, italic)
    for i, ln in enumerate(lines):
        text(d, (x, y + i * size * spacing), ln, size, color, bold, italic=italic)
    return y + len(lines) * size * spacing


def rbox(d, box, fill=None, outline=None, width=3, r=18):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- habillage ETML
LOGO = Image.open(os.path.join(HERE, "logo_white_v.png")).convert("RGBA")
LOGO = LOGO.resize((int(360 * LOGO.width / LOGO.height), 360), Image.LANCZOS)
_vt = Image.new("RGBA", (440, 60), (0, 0, 0, 0)); ImageDraw.Draw(_vt).text((220, 30), "Section électronique", font=F(30, True), fill=WHITE, anchor="mm")
VTXT = _vt.rotate(90, expand=True)
FOOT = ["Test et Mesure 1 – El DT 1"]


def chrome(img, d, tag, title, num):
    d.rectangle((BAND_X, 0, W, H), fill=NAVY)
    img.paste(LOGO, (BAND_X + (W - BAND_X - LOGO.width) // 2, 40), LOGO)
    img.paste(VTXT, (BAND_X + (W - BAND_X - VTXT.width) // 2, 470), VTXT)
    if num:
        d.rectangle((BAND_X + 37, 980, BAND_X + 107, 1050), fill=LBLUE)
        text(d, (BAND_X + 72, 1015), num, 26, NAVY, True, anchor="mm")
    d.line((60, 1030, BAND_X - 50, 1030), fill=BLUE, width=2)
    text(d, (60, 1040), "Section électronique", 20, NAVY, italic=True)
    text(d, (BAND_X - 50, 1040), FOOT[0], 20, GREY, anchor="ra")
    if tag: text(d, (60, 42), tag, 24, BLUE, True)
    if title: text(d, (60, 78), title, 46, NAVY, True)


def caption(d, s, alpha=1.0):
    """Bandeau de commentaire en bas (2 lignes au plus)."""
    if not s: return
    col = mix(WHITE, NAVY, alpha)
    rbox(d, (60, 905, BAND_X - 50, 1005), fill=mix(WHITE, TINT, alpha), r=14)
    lines = wrap(s, 30, BAND_X - 160)
    y0 = 955 - (min(len(lines), 2) - 1) * 19
    for i, ln in enumerate(lines[:2]):
        text(d, (90, y0 + i * 38), ln, 30, col, anchor="lm")


def cap_at(t, seq):
    """seq = [(t0, texte), …] trié : renvoie le texte en cours."""
    cur = ""
    for t0, s in seq:
        if t >= t0: cur = s
    return cur


def ref_pill(d, s, x=BAND_X - 50, y=84):
    w = F(22, True).getlength(s) + 40
    rbox(d, (x - w, y - 4, x, y + 36), fill=TINT, outline=BLUE, width=2, r=18)
    text(d, (x - w / 2, y + 16), s, 22, NAVY, True, anchor="mm")


def label_box(d, xy, s, size=20, color=NAVY, anchor="mm", bg=WHITE, alpha=1.0):
    if alpha <= 0: return
    f = F(size, True); w = f.getlength(s); x, y = xy
    x0 = x if anchor == "lm" else (x - w - 16 if anchor == "rm" else x - w / 2 - 8)
    d.rounded_rectangle((x0, y - size * 0.75, x0 + w + 16, y + size * 0.75), radius=8, fill=bg)
    text(d, (x0 + 8 + w / 2, y), s, size, mix(bg, color, alpha), True, anchor="mm")


def display(d, box, label, value, vsize=54, color=(190, 255, 200)):
    rbox(d, box, fill=(30, 34, 60), outline=NAVY, width=4, r=14)
    x0, y0, x1, y1 = box
    if label: text(d, (x0 + 22, y0 + 14), label, 22, LBLUE)
    text(d, ((x0 + x1) / 2, y1 - (y1 - y0) * (0.36 if label else 0.5)), value, vsize, color, True, mono=True, anchor="mm")


def bitpill(d, xy, v, size=26, alpha=1.0):
    """Pastille 0 / 1 : 1 en bleu plein, 0 en clair."""
    if alpha <= 0: return
    x, y = xy; r = size * 0.75
    on = v in (1, "1", True)
    d.rounded_rectangle((x - r, y - r, x + r, y + r), radius=int(r * 0.45), fill=mix(WHITE, BLUE if on else TINT, alpha),
                        outline=mix(WHITE, NAVY, alpha), width=2)
    text(d, (x, y), "1" if on else "0", size, mix(WHITE, WHITE if on else NAVY, alpha), True, mono=True, anchor="mm")


def check(d, xy, ok, size=40, alpha=1.0):
    x, y = xy
    col = mix(WHITE, GREEN if ok else RED, alpha)
    d.ellipse((x - size / 2, y - size / 2, x + size / 2, y + size / 2), fill=col)
    s = size * 0.22
    if ok:
        d.line([(x - s * 1.2, y), (x - s * 0.2, y + s), (x + s * 1.4, y - s * 1.1)], fill=WHITE, width=max(3, int(size / 9)), joint="curve")
    else:
        d.line((x - s, y - s, x + s, y + s), fill=WHITE, width=max(3, int(size / 9)))
        d.line((x - s, y + s, x + s, y - s), fill=WHITE, width=max(3, int(size / 9)))


def head(d, tip, ang, color, size=20):
    a1 = (tip[0] - size * math.cos(ang - 0.42), tip[1] - size * math.sin(ang - 0.42))
    a2 = (tip[0] - size * math.cos(ang + 0.42), tip[1] - size * math.sin(ang + 0.42))
    d.polygon([tip, a1, a2], fill=color)


def arrow(d, p0, p1, color=NAVY, width=4, draw=1.0):
    if draw <= 0: return
    x = p0[0] + (p1[0] - p0[0]) * clamp(draw); y = p0[1] + (p1[1] - p0[1]) * clamp(draw)
    d.line((p0, (x, y)), fill=color, width=width)
    if draw >= 1: head(d, p1, math.atan2(p1[1] - p0[1], p1[0] - p0[0]), color, 14 + width)


def wire(d, pts, v=None, width=5, alpha=1.0):
    """Fil logique : 1 en bleu épais, 0 en marine fin, inconnu en gris."""
    col = BLUE if v in (1, True) else (NAVY if v in (0, False) else GREY)
    d.line(pts, fill=mix(WHITE, col, alpha), width=width + (3 if v in (1, True) else 0), joint="curve")


# ---------------------------------------------------------------- symbole CEI 60617-12
QUAL = {"NON": "1", "ET": "&", "OU": "≥1", "NON-ET": "&", "NON-OU": "≥1", "OUX": "=1", "NON-OUX": "=1"}
NEG = {"NON": True, "ET": False, "OU": False, "NON-ET": True, "NON-OU": True, "OUX": False, "NON-OUX": True}


def gate(d, x, y, key, s=1.0, vin=None, vout=None, labels=("A", "B"), alpha=1.0, lead=70, out_label="Y", qsize=None):
    """Rectangle CEI à (x, y). vin = valeurs des entrées (A, B) ou None ; vout = valeur de sortie.
    Renvoie (points des entrées, point de sortie)."""
    n = 1 if key == "NON" else 2
    w, h = 150 * s, (150 if n == 1 else 190) * s
    L = lead * s
    ys = [y + h / 2] if n == 1 else [y + h * 0.28, y + h * 0.72]
    ins = []
    for i, yy in enumerate(ys):
        v = vin[i] if vin else None
        wire(d, [(x - L, yy), (x, yy)], v, int(4 * s) + 1, alpha)
        text(d, (x - L - 10 * s, yy), labels[i], int(30 * s), mix(WHITE, NAVY, alpha), True, italic=True, anchor="rm")
        ins.append((x - L, yy))
    d.rectangle((x, y, x + w, y + h), fill=WHITE, outline=mix(WHITE, NAVY, alpha), width=max(3, int(5 * s)))
    text(d, (x + w / 2, y + 14 * s), QUAL[key], int((qsize or 40) * s), mix(WHITE, NAVY, alpha), True, anchor="ma")
    xo = x + w
    if NEG[key]:
        r = 12 * s
        d.ellipse((xo, y + h / 2 - r, xo + 2 * r, y + h / 2 + r), fill=WHITE, outline=mix(WHITE, NAVY, alpha), width=max(3, int(4 * s)))
        xo += 2 * r
    wire(d, [(xo, y + h / 2), (xo + L, y + h / 2)], vout, int(4 * s) + 1, alpha)
    if out_label: text(d, (xo + L + 10 * s, y + h / 2), out_label, int(30 * s), mix(WHITE, NAVY, alpha), True, italic=True, anchor="lm")
    return ins, (xo + L, y + h / 2)


def lamp(d, xy, on, r=30, label=None, color=None):
    x, y = xy
    c = color or BLUE
    if on: d.ellipse((x - r - 10, y - r - 10, x + r + 10, y + r + 10), fill=mix(WHITE, c, 0.25))
    d.ellipse((x - r, y - r, x + r, y + r), fill=c if on else (240, 242, 247), outline=NAVY, width=3)
    if label: text(d, (x, y + r + 22), label, 22, NAVY, True, anchor="mm")


# ---------------------------------------------------------------- cartes de transition
def make_card(cards, k, dur):
    num, total, title, use, ill, situ, quest, mtxt, key = cards[k]

    def s_card(img, d, t):
        chrome(img, d, "", "", f"{num}/{total}")
        p = prog(t, 0.0, 1.0)
        d.ellipse((60, 40, 150, 130), fill=mix(WHITE, NAVY, p))
        text(d, (105, 85), num, 50, WHITE, True, anchor="mm")
        text(d, (180, 40), f"DÉMONSTRATION {num} / {total}", 24, mix(WHITE, BLUE, p), True)
        text(d, (180, 70), title, 56, mix(WHITE, NAVY, p), True)
        text(d, (180, 145), use, 32, mix(WHITE, GREY, prog(t, 0.6, 1.6)), italic=True)
        q = prog(t, 1.2, 2.4)
        lay = Image.new("RGB", (BAND_X, H), WHITE); dl = ImageDraw.Draw(lay)
        ill(lay, dl, t)
        box = (40, 220, 780, 900)
        reg = lay.crop(box)
        img.paste(Image.blend(Image.new("RGB", reg.size, WHITE), reg, q), box[:2])
        X0 = 820
        rbox(d, (X0, 220, BAND_X - 50, 900), fill=mix(WHITE, TINT, prog(t, 1.5, 2.5)), r=20)
        y = 255
        for head_, body, t0 in [("La situation", situ, 2.0), ("La question", quest, 4.5), ("Ce qu'on va voir", mtxt, 7.0)]:
            r = prog(t, t0, t0 + 1.0)
            text(d, (X0 + 40, y), head_.upper(), 24, mix(TINT, BLUE, r), True)
            lines = wrap(body, 31, BAND_X - 50 - X0 - 80)
            for i, ln in enumerate(lines):
                text(d, (X0 + 40 + (1 - r) * 30, y + 40 + i * 40), ln, 31, mix(TINT, NAVY, r))
            y += 40 + len(lines) * 40 + 28
        r = prog(t, 8.8, 9.8)
        rbox(d, (X0 + 40, 775, BAND_X - 90, 865), fill=mix(TINT, WHITE, r), outline=mix(TINT, BLUE, r), width=3, r=14)
        text(d, ((X0 + BAND_X - 50) / 2, 820), key, 38, mix(TINT, NAVY, r), True, anchor="mm")
        r2 = prog(t, 2.0, 3.0)
        text(d, (60, 948), "L'animation démarre dans un instant…", 24, mix(WHITE, GREY, r2), italic=True)
        d.rounded_rectangle((60, 985, BAND_X - 50, 993), radius=4, fill=mix(WHITE, TINT, r2))
        fr = clamp((t - 2.0) / (dur - 3.0))
        if fr > 0: d.rounded_rectangle((60, 985, 60 + (BAND_X - 110) * fr, 993), radius=4, fill=mix(WHITE, BLUE, r2))
    return s_card


def intro_scene(tag, title, sub, items, foot):
    def s_intro(img, d, t):
        chrome(img, d, "", "", "")
        p = prog(t, 0.2, 1.2)
        text(d, (110, 170), tag, 30, mix(WHITE, BLUE, p), True)
        text(d, (110, 225), title, 84, mix(WHITE, NAVY, p), True)
        text(d, (110, 335), sub, 42, mix(WHITE, GREY, p))
        for i, (n, a, b) in enumerate(items):
            q = prog(t, 1.4 + i * 0.6, 2.0 + i * 0.6)
            if q <= 0: continue
            y = 430 + i * 86; x = 110 + (1 - q) * 60
            d.ellipse((x, y, x + 64, y + 64), fill=mix(WHITE, NAVY, q))
            text(d, (x + 32, y + 32), n, 32, WHITE, True, anchor="mm")
            text(d, (x + 92, y + 32), a, 36, mix(WHITE, NAVY, q), True, anchor="lm")
            text(d, (x + 830, y + 32), b, 30, mix(WHITE, GREY, q), anchor="lm")
        q = prog(t, 5.0, 6.0)
        text(d, (110, 880), foot, 28, mix(WHITE, BLUE, q), True)
    return s_intro


def outro_scene(rows, exo_title, exos, last_caption):
    def s_outro(img, d, t):
        chrome(img, d, "RÉCAPITULATIF", "À retenir – et à t'exercer", "")
        for i, (a, b) in enumerate(rows):
            q = prog(t, 0.3 + i * 0.5, 0.9 + i * 0.5)
            if q <= 0: continue
            y = 190 + i * 112
            rbox(d, (60, y, 900, y + 94), fill=mix(WHITE, TINT, q), r=14)
            text(d, (90, y + 47), a, 30, mix(WHITE, NAVY, q), True, anchor="lm")
            para(d, (330, y + 16), b, 25, 550, mix(WHITE, NAVY, q))
        q0 = prog(t, 2.5, 3.2)
        text(d, (960, 185), exo_title, 30, mix(WHITE, BLUE, q0), True)
        for i, (a, b, p) in enumerate(exos):
            q = prog(t, 2.8 + i * 0.4, 3.4 + i * 0.4)
            if q <= 0: continue
            y = 235 + i * 96
            d.ellipse((960, y + 8, 1010, y + 58), fill=mix(WHITE, NAVY, q))
            text(d, (985, y + 33), str(i + 1), 24, WHITE, True, anchor="mm")
            text(d, (1030, y + 6), a, 27, mix(WHITE, NAVY, q), True)
            text(d, (1030, y + 42), b, 22, mix(WHITE, GREY, q), italic=True)
            if p: text(d, (BAND_X - 60, y + 20), p, 24, mix(WHITE, BLUE, q), True, anchor="ra")
        caption(d, last_caption, prog(t, 6, 7))
    return s_outro


# ---------------------------------------------------------------- rendu
XF, FADE = 1.5, 0.6
# Ralenti : 1 = vitesse du scénario ; 2 = deux fois plus lent. Gaël a essayé ×2 puis demandé « 2 fois plus vite »
# (11/16/2026) : réglage par défaut revenu à 1. Le temps du scénario avance de 1/(FPS·SLOW) par image, le mouvement
# reste fluide (pas d'images dupliquées). Autre vitesse : ANIM_SLOW=1.5 python3 anim_105.py …
SLOW = float(os.environ.get("ANIM_SLOW", "1"))


def frame_at(scenes, i, t):
    img = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(img)
    scenes[i][0](img, d, t)
    return img


def render(scenes, out):
    starts, acc = [], 0.0
    for _, dur in scenes:
        starts.append(acc); acc += dur - XF
    total = starts[-1] + scenes[-1][1]
    nfr = int(total * FPS * SLOW)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    white = Image.new("RGB", (W, H), WHITE)
    for f in range(nfr):
        tg = f / (FPS * SLOW)
        act =[(i, tg - starts[i]) for i in range(len(scenes)) if 0 <= tg - starts[i] < scenes[i][1]]
        img = frame_at(scenes, *act[0])
        if len(act) > 1: img = Image.blend(img, frame_at(scenes, *act[1]), ease(act[1][1] / XF))
        a = min(1.0, tg / FADE, (total - tg) / FADE)
        if a < 1: img = Image.blend(white, img, max(a, 0))
        ff.stdin.write(img.tobytes())
    ff.stdin.close(); ff.wait()
    print("ok", out, f"{total * SLOW:.0f} s (ralenti ×{SLOW:g})")
    return total
