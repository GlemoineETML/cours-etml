# -*- coding: utf-8 -*-
"""Animation « Étoile ou triangle ? » – même récepteur (3 × 40 Ω), deux couplages sur 3 × 400/230 V.
Charte ETML : bande marine à droite avec logo blanc, couleurs 242852 / 297FD5 / ACCBF9, police Arial (Liberation Sans).
Les points qui bougent dans les fils représentent les charges : en alternatif elles vont et viennent ; l'amplitude du
mouvement est proportionnelle au courant efficace (ralenti : une période = 4 s). Les résistances rougissent selon leur puissance.
Sortie : MP4 1920×1080, 25 i/s, H.264. Aperçu : python3 anim_etoile_triangle.py <scène> <t>.
Valeurs : U = 400 V, U_ph = 231 V, R = 40 Ω → étoile I = 5,77 A, P = 4 kW ; triangle I_ph = 10 A, I = 17,3 A, P = 12 kW."""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 25
NAVY, BLUE, LBLUE, TINT, RED, GREY, WHITE = (36, 40, 82), (41, 127, 213), (172, 203, 249), (232, 239, 251), (238, 0, 0), (90, 100, 120), (255, 255, 255)
GREEN, HOT = (30, 140, 70), (255, 110, 30)
C1, C2, C3, CN = (139, 90, 43), (26, 26, 26), (122, 122, 122), (41, 127, 213)   # L1 brun, L2 noir, L3 gris, N bleu (CEI 60445)
PH = [C1, C2, C3]
BAND_X = 1776
FD = "/usr/share/fonts/truetype/liberation/"
_fc = {}

U, R = 400.0, 40.0
UPH = U / math.sqrt(3)
IY = UPH / R                 # 5,77 A
IPH_D = U / R                # 10 A
ID = IPH_D * math.sqrt(3)    # 17,3 A
PY, PD = 3 * UPH ** 2 / R, 3 * U ** 2 / R
RALENTI = 1.5                # 1.0 = vitesse normale ; 1.5 = 1,5 fois plus lent ; 2.0 = deux fois plus lent (tout le film)
TPER = 4.0                   # durée d'une période du va-et-vient des charges (s) ; plus grand = charges plus lentes
OM = 2 * math.pi / TPER
KDOT = 5.2                   # px par ampère efficace (amplitude du va-et-vient)
ANG_E = [90, -30, 210]       # tensions de phase
ANG_U = [120, 0, 240]        # U12, U23, U31 (éléments du triangle Z1, Z2, Z3)


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
def fr(x, n=1): return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def text(d, xy, s, size, color=NAVY, bold=False, mono=False, italic=False, anchor="la"):
    d.text(xy, s, font=F(size, bold, mono, italic), fill=color, anchor=anchor)


def rich(d, xy, parts, size, color=NAVY, bold=False, anchor="l"):
    """parts : liste de (texte, indice?) ; ancrage vertical au milieu. anchor 'l', 'm' ou 'r'."""
    widths = [F(int(size * (0.62 if s else 1)), bold).getlength(p) for p, s in parts]
    tot = sum(widths)
    x, y = xy
    if anchor == "m": x -= tot / 2
    elif anchor == "r": x -= tot
    for (p, s), w in zip(parts, widths):
        if s: d.text((x, y + size * 0.28), p, font=F(int(size * 0.62), bold), fill=color, anchor="lm")
        else: d.text((x, y), p, font=F(size, bold), fill=color, anchor="lm")
        x += w
    return tot


def wrap(s, size, width, bold=False):
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if F(size, bold).getlength(test) > width and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    if cur: lines.append(cur)
    return lines


def rbox(d, box, fill=None, outline=None, width=3, r=18):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def arrow(d, p0, p1, color=BLUE, width=6, head=22):
    L = math.dist(p0, p1)
    if L < 3: return
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    hs = min(head, L * 0.45)
    pe = (p1[0] - hs * 0.7 * math.cos(ang), p1[1] - hs * 0.7 * math.sin(ang))
    d.line((p0, pe), fill=color, width=width)
    a1 = (p1[0] - hs * math.cos(ang - 0.42), p1[1] - hs * math.sin(ang - 0.42))
    a2 = (p1[0] - hs * math.cos(ang + 0.42), p1[1] - hs * math.sin(ang + 0.42))
    d.polygon([p1, a1, a2], fill=color)


# ---------------------------------------------------------------- habillage ETML
LOGO = Image.open("logo_white_v.png").convert("RGBA")
LOGO = LOGO.resize((96, int(96 * LOGO.height / LOGO.width)), Image.LANCZOS)
_vt = Image.new("RGBA", (520, 80), (0, 0, 0, 0)); ImageDraw.Draw(_vt).text((260, 40), "Section électronique", font=F(36, True), fill=WHITE, anchor="mm")
VTXT = _vt.rotate(90, expand=True)


def chrome(img, d, tag, title, num):
    d.rectangle((BAND_X, 0, W, H), fill=NAVY)
    img.paste(LOGO, (BAND_X + (W - BAND_X - LOGO.width) // 2, 40), LOGO)
    img.paste(VTXT, (BAND_X + (W - BAND_X - VTXT.width) // 2, 470), VTXT)
    if num:
        d.rectangle((BAND_X + 22, 980, BAND_X + 122, 1050), fill=LBLUE)
        text(d, (BAND_X + 72, 1015), num, 26, NAVY, True, anchor="mm")
    d.line((60, 1030, BAND_X - 50, 1030), fill=BLUE, width=2)
    text(d, (60, 1040), "Section électronique", 20, NAVY, italic=True)
    text(d, (BAND_X - 50, 1040), "Électrotechnique – triphasé · Étoile ou triangle ? · XLO4", 20, GREY, anchor="ra")
    if tag: text(d, (60, 42), tag, 24, BLUE, True)
    if title: text(d, (60, 78), title, 46, NAVY, True)


def caption(d, s, alpha=1.0):
    if not s: return
    rbox(d, (60, 905, BAND_X - 50, 1005), fill=mix(WHITE, TINT, alpha), r=14)
    lines = wrap(s, 30, BAND_X - 170)
    y0 = 955 - (min(len(lines), 2) - 1) * 19
    for i, ln in enumerate(lines[:2]):
        text(d, (90, y0 + i * 38), ln, 30, mix(WHITE, NAVY, alpha), anchor="lm")


def cap_at(t, seq):
    cur = ""
    for t0, s in seq:
        if t >= t0: cur = s
    return cur


# ---------------------------------------------------------------- briques électriques
def poly_len(pts):
    return [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


def point_on(pts, segs, s):
    for i, L in enumerate(segs):
        if s <= L:
            a = s / L if L else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * a, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * a)
        s -= L
    return pts[-1]


def wire(d, pts, color, width=5):
    d.line(pts, fill=color, width=width, joint="curve")


def charges(d, pts, irms, phase_deg, t, color, spacing=34, r=6, scale=1.0):
    """Points de charge : position = KDOT·I·(−cos(ωt+φ)) le long du fil (va-et-vient alternatif)."""
    segs = poly_len(pts); L = sum(segs)
    if L <= 0: return
    off = KDOT * scale * irms * (-math.cos(OM * t + math.radians(phase_deg)))
    k0 = math.floor(-off / spacing) - 1
    k = k0
    while True:
        s = off + k * spacing
        if s > L: break
        if s >= 0:
            x, y = point_on(pts, segs, s)
            d.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=WHITE)
        k += 1


def resistor(d, p0, p1, heat=0.0, w=110, h=40, label=None, lab_side=1, lab_size=30, scale=1.0):
    """Résistance CEI (rectangle) centrée entre p0 et p1, avec fils ; heat 0..1 = couleur de chauffe."""
    w *= scale; h *= scale
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    L = math.dist(p0, p1); ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L; nx, ny = -uy, ux
    a = (mx - ux * w / 2, my - uy * w / 2); b = (mx + ux * w / 2, my + uy * w / 2)
    d.line((p0, a), fill=NAVY, width=max(3, int(5 * scale))); d.line((b, p1), fill=NAVY, width=max(3, int(5 * scale)))
    poly = [(a[0] + nx * h / 2, a[1] + ny * h / 2), (b[0] + nx * h / 2, b[1] + ny * h / 2),
            (b[0] - nx * h / 2, b[1] - ny * h / 2), (a[0] - nx * h / 2, a[1] - ny * h / 2)]
    if heat > 0:
        glow = [(mx + (x - mx) * 1.25, my + (y - my) * 1.25) for x, y in poly]
        d.polygon(glow, fill=mix(WHITE, (255, 205, 160), heat))
    d.polygon(poly, fill=mix(WHITE, HOT, heat), outline=NAVY, width=max(3, int(4 * scale)))
    if label:
        dist = (h / 2 + 34 * scale) * lab_side
        text(d, (mx + nx * dist, my + ny * dist), label, int(lab_size * scale), NAVY, True, anchor="mm")


def node(d, p, r=8):
    d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=NAVY)


def meter(d, box, label_parts, value, color=NAVY, sub=None, alpha=1.0):
    """Afficheur d'appareil de mesure."""
    x0, y0, x1, y1 = box
    rbox(d, box, fill=mix(WHITE, (30, 34, 60), alpha), outline=mix(WHITE, NAVY, alpha), width=3, r=12)
    if alpha < 0.5: return
    rich(d, (x0 + 18, y0 + 26), label_parts, 24, LBLUE)
    text(d, (x1 - 18, y1 - 30), value, 44, (190, 255, 200), True, mono=True, anchor="rm")
    if sub: text(d, (x0 + 18, y1 - 22), sub, 18, LBLUE, anchor="lm")


def plaque(d, x, y, mode, s=1.0, p=1.0, label=True):
    """Plaque à bornes CEI : U1 V1 W1 en haut, W2 U2 V2 en bas ; barrettes Y (horizontale) ou Δ (verticales)."""
    w, h = 300 * s, 190 * s
    rbox(d, (x, y, x + w, y + h), fill=(243, 245, 249), outline=NAVY, width=3, r=10)
    X = [x + 70 * s, x + 150 * s, x + 230 * s]
    yt, yb = y + 60 * s, y + 135 * s
    if p > 0:
        col = mix(WHITE, BLUE, p)
        if mode == "Y": d.line((X[0], yb, X[2], yb), fill=col, width=int(16 * s))
        else:
            for xx in X: d.line((xx, yt, xx, yb), fill=col, width=int(16 * s))
    for xx, a, b in zip(X, ("U1", "V1", "W1"), ("W2", "U2", "V2")):
        for yy, lab, dy in ((yt, a, -1), (yb, b, 1)):
            rr = 16 * s
            d.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), outline=NAVY, width=3, fill=None)
            text(d, (xx - 24 * s, yy), lab, int(17 * s), NAVY, True, anchor="rm")
    for xx, c, n in zip(X, PH, ("L1", "L2", "L3")):
        d.line((xx, y - 40 * s, xx, yt - 16 * s), fill=c, width=int(5 * s))
        text(d, (xx, y - 52 * s), n, int(20 * s), NAVY, True, anchor="mm")
    if label:
        text(d, (x + w / 2, y + h + 26 * s), "barrettes en étoile Y" if mode == "Y" else "barrettes en triangle Δ", int(22 * s), NAVY, True, anchor="mm")


# ---------------------------------------------------------------- schémas animés
def star_geom(ox, oy, s):
    P = lambda x, y: (ox + x * s, oy + y * s)
    yl = [0, 70, 140]; xs = [360, 500, 640]; ystar = 470; yn = 590
    lines = [[P(0, yl[k]), P(xs[k], yl[k])] for k in range(3)]
    elems = [(P(xs[k], yl[k]), P(xs[k], ystar)) for k in range(3)]
    star = [P(xs[0], ystar), P(xs[2], ystar)]
    neutral = [P(0, yn), P(xs[1], yn), P(xs[1], ystar)]
    return P, yl, xs, ystar, yn, lines, elems, star, neutral


def draw_star(d, t, ox, oy, s=1.0, neutre=True, alpha=1.0, flow=True, labels=True, heat=None):
    P, yl, xs, ystar, yn, lines, elems, star, neutral = star_geom(ox, oy, s)
    for k in range(3):
        wire(d, lines[k], PH[k], max(3, int(6 * s)))
        text(d, (P(-18, yl[k])), f"L{k + 1}", int(28 * s), PH[k], True, anchor="rm")
    if neutre:
        wire(d, neutral, CN, max(3, int(6 * s)))
        text(d, P(-18, yn), "N", int(28 * s), CN, True, anchor="rm")
    wire(d, star, NAVY, max(3, int(5 * s)))
    h = (PY / 3 / (PD / 3)) if heat is None else heat
    for k in range(3):
        resistor(d, elems[k][0], elems[k][1], heat=h * prog(t, 0.5, 2.5), label=f"Z{k + 1}" if labels else None, lab_side=-1, scale=s)
        node(d, elems[k][0], 7 * s); node(d, elems[k][1], 7 * s)
    node(d, P(xs[1], ystar), 7 * s)
    text(d, P(xs[2] + 30, ystar + 4), "point étoile", int(22 * s), GREY, anchor="lm")
    if flow:
        for k in range(3):
            path = [P(0, yl[k]), P(xs[k], yl[k]), P(xs[k], ystar)]
            charges(d, path, IY, ANG_E[k], t, mix(WHITE, PH[k], alpha) if k != 1 else mix(WHITE, (70, 70, 70), alpha), r=max(4, int(7 * s)), scale=s, spacing=34 * s)
        if neutre:
            charges(d, neutral, 0.0, 0, t, CN, r=max(4, int(7 * s)), scale=s, spacing=34 * s)
    return P


def tri_geom(ox, oy, s):
    P = lambda x, y: (ox + x * s, oy + y * s)
    A, B, C = P(500, 210), P(330, 500), P(670, 500)          # A → L1, B → L2, C → L3
    lines = [[P(0, 0), P(500, 0), A], [P(0, 70), P(260, 70), P(260, 500), B], [P(0, 140), P(740, 140), P(740, 500), C]]
    elems = [(A, B), (B, C), (C, A)]                         # Z1 : L1-L2, Z2 : L2-L3, Z3 : L3-L1
    return P, A, B, C, lines, elems


def draw_tri(d, t, ox, oy, s=1.0, flow=True, labels=True, heat=1.0, show_lines_flow=True):
    P, A, B, C, lines, elems = tri_geom(ox, oy, s)
    for k in range(3):
        wire(d, lines[k], PH[k], max(3, int(6 * s)))
        text(d, P(-18, [0, 70, 140][k]), f"L{k + 1}", int(28 * s), PH[k], True, anchor="rm")
    sides = [1, 1, 1]
    for k in range(3):
        resistor(d, elems[k][0], elems[k][1], heat=heat * prog(t, 0.5, 2.5), label=f"Z{k + 1}" if labels else None, lab_side=[-1, 1, 1][k], scale=s)
    for p in (A, B, C): node(d, p, 8 * s)
    if flow:
        cols = [PH[0], (70, 70, 70), PH[2]]
        for k in range(3):
            charges(d, list(elems[k]), IPH_D, ANG_U[k], t, mix(WHITE, HOT, 0.85), r=max(4, int(7 * s)), scale=s, spacing=30 * s)
        if show_lines_flow:
            for k in range(3):
                charges(d, lines[k], ID, ANG_E[k], t, cols[k], r=max(4, int(7 * s)), scale=s, spacing=34 * s)
    return P, A, B, C


# ---------------------------------------------------------------- diagramme vectoriel
def phasors(d, c, rad, t, rotate=True, show=(1, 1, 1), uline=0.0, uph=0.0, thick=7, labels=True):
    rot = math.degrees(OM * t) if rotate else 0
    tips = []
    for k in range(3):
        a = math.radians(ANG_E[k] + rot)
        tips.append((c[0] + rad * math.cos(a), c[1] - rad * math.sin(a)))
    if uline > 0:
        col = mix(WHITE, BLUE, uline)
        for i in range(3): d.line((tips[i], tips[(i + 1) % 3]), fill=col, width=4)
    for k in range(3):
        if show[k]: arrow(d, c, tips[k], PH[k], thick, 30)
        if labels and show[k]:
            a = math.radians(ANG_E[k] + rot)
            text(d, (c[0] + (rad + 42) * math.cos(a), c[1] - (rad + 42) * math.sin(a)), f"L{k + 1}", 28, PH[k], True, anchor="mm")
    d.ellipse((c[0] - 9, c[1] - 9, c[0] + 9, c[1] + 9), fill=CN)
    return tips


# ================================================================ SCÈNES
def s_intro(img, d, t):
    chrome(img, d, "", "", "")
    p = prog(t, 0.2, 1.2)
    text(d, (110, 190), "ÉLECTROTECHNIQUE – TRIPHASÉ · ANIMATION", 30, mix(WHITE, BLUE, p), True)
    text(d, (110, 250), "Étoile ou triangle ?", 96, mix(WHITE, NAVY, p), True)
    text(d, (110, 380), "Le même chauffe-eau de 3 × 40 Ω, branché de deux façons sur 3 × 400/230 V", 40, mix(WHITE, GREY, prog(t, 0.8, 1.8)))
    q = prog(t, 1.8, 3.0)
    if q > 0:
        lay = Image.new("RGB", (BAND_X, H), WHITE); dl = ImageDraw.Draw(lay)
        draw_star(dl, t, 190, 500, 0.6, neutre=False, labels=False, heat=0.33)
        draw_tri(dl, t, 990, 500, 0.6, labels=False, heat=1.0)
        text(dl, (420, 470), "étoile Y", 40, BLUE, True, anchor="mm")
        text(dl, (1240, 470), "triangle Δ", 40, BLUE, True, anchor="mm")
        box = (60, 440, BAND_X - 40, 900)
        reg = lay.crop(box)
        img.paste(Image.blend(Image.new("RGB", reg.size, WHITE), reg, q), box[:2])
    if t > 4.0:
        caption(d, "Prédis avant de regarder : lequel chauffe le plus ? Combien de fois plus ?", prog(t, 4.0, 4.8))


def s_reseau(img, d, t):
    chrome(img, d, "1 · LE RÉSEAU", "Trois tensions décalées de 120°", "1/5")
    c, rad = (420, 540), 250
    tips = phasors(d, c, rad, t, uline=prog(t, 12, 13.5))
    text(d, (c[0], 850), f"ralenti : une période de 20 ms dure ici {fr(TPER * RALENTI, 0)} s", 22, GREY, italic=True, anchor="mm")
    if t > 7:
        q = prog(t, 7, 8)
        mid = ((c[0] + tips[0][0]) / 2, (c[1] + tips[0][1]) / 2)
        rbox(d, (mid[0] + 20, mid[1] - 26, mid[0] + 210, mid[1] + 26), fill=mix(WHITE, WHITE, q), outline=mix(WHITE, C1, q), width=3, r=10)
        rich(d, (mid[0] + 34, mid[1]), [("U", 0), ("ph", 1), (" = 231 V", 0)], 28, mix(WHITE, C1, q), True)
    if t > 12.5:
        q = prog(t, 12.5, 13.5)
        mid = ((tips[0][0] + tips[1][0]) / 2, (tips[0][1] + tips[1][1]) / 2)
        rbox(d, (mid[0] - 90, mid[1] - 26, mid[0] + 90, mid[1] + 26), fill=WHITE, outline=mix(WHITE, BLUE, q), width=3, r=10)
        text(d, mid, "U = 400 V", 28, mix(WHITE, BLUE, q), True, anchor="mm")
    # courbes
    x0, x1, y0, A = 900, 1700, 520, 190
    d.line((x0, y0, x1, y0), fill=GREY, width=2); d.line((x0, y0 - A - 30, x0, y0 + A + 30), fill=GREY, width=2)
    text(d, (x1, y0 + 30), "temps", 22, GREY, anchor="ra")
    for k in range(3):
        pts = []
        for i in range(0, 401):
            tt = t - (i / 400) * TPER * 1.5
            v = math.sin(OM * tt + math.radians(ANG_E[k]))
            pts.append((x0 + i / 400 * (x1 - x0), y0 - A * v))
        d.line(pts, fill=PH[k], width=5, joint="curve")
        d.ellipse((x0 - 9, pts[0][1] - 9, x0 + 9, pts[0][1] + 9), fill=PH[k])
        d.line((tips[k][0], tips[k][1], x0, pts[0][1]), fill=mix(WHITE, PH[k], 0.25), width=1)
    text(d, (x0 + 10, y0 - A - 50), "valeur instantanée (← maintenant)", 22, GREY)
    if t > 17:
        q = prog(t, 17, 18)
        rbox(d, (920, 770, 1700, 860), fill=mix(WHITE, TINT, q), r=14)
        rich(d, (950, 815), [("U = √3 · U", 0), ("ph", 1), ("   400 V = 1,73 × 231 V", 0)], 38, mix(TINT, NAVY, q), True)
    caption(d, cap_at(t, [(0, "Trois tensions de même valeur, décalées d'un tiers de période (120°). Elles tournent ensemble."),
                          (7, "Entre un conducteur polaire et le neutre : la tension de phase Uph = 231 V."),
                          (12.5, "Entre deux conducteurs polaires : la tension réseau U = 400 V. C'est la plus grande des deux."),
                          (17, "Le rapport vaut toujours √3. Tout le choix étoile / triangle se joue sur cette différence.")]))


def s_etoile(img, d, t):
    chrome(img, d, "2 · COUPLAGE ÉTOILE Y", "Chaque élément entre une phase et le point étoile", "2/5")
    ox, oy = 170, 230
    P = draw_star(d, t, ox, oy, 1.0, neutre=True, heat=PY / PD)
    # voltmètre sur Z1
    if t > 5:
        q = prog(t, 5, 6)
        _, yl, xs, ystar, yn, *_ = star_geom(ox, oy, 1.0)
        vx = ox + xs[0] - 120
        top, bot = (ox + xs[0], oy + 160), (ox + xs[0], oy + 310)
        col = mix(WHITE, BLUE, q)
        d.line((top, (vx, top[1])), fill=col, width=2); d.line((bot, (vx, bot[1])), fill=col, width=2)
        d.line(((vx, top[1]), (vx, bot[1])), fill=col, width=2)
        cy = (top[1] + bot[1]) / 2
        d.ellipse((vx - 30, cy - 30, vx + 30, cy + 30), fill=WHITE, outline=col, width=4)
        text(d, (vx, cy), "V", 30, col, True, anchor="mm")
    # panneau droit : mesures
    X0 = 1010
    meter(d, (X0, 190, X0 + 340, 300), [("tension sur Z", 0), ("1", 1)], "231 V", alpha=prog(t, 5.5, 6.5))
    meter(d, (X0 + 370, 190, X0 + 710, 300), [("courant de ligne I", 0)], fr(IY, 2) + " A", alpha=prog(t, 10, 11))
    meter(d, (X0, 320, X0 + 340, 430), [("courant dans Z", 0), ("1", 1)], fr(IY, 2) + " A", alpha=prog(t, 12, 13))
    meter(d, (X0 + 370, 320, X0 + 710, 430), [("courant de neutre I", 0), ("N", 1)], "0,00 A", alpha=prog(t, 17, 18))
    if t > 6.5:
        q = prog(t, 6.5, 7.5)
        rich(d, (X0, 480), [("U", 0), ("ph", 1), (" = U / √3 = 400 / 1,73 = 231 V", 0)], 30, mix(WHITE, NAVY, q), True)
    if t > 13:
        q = prog(t, 13, 14)
        rich(d, (X0, 530), [("I = I", 0), ("ph", 1), (" = 231 V / 40 Ω = 5,77 A", 0)], 30, mix(WHITE, NAVY, q), True)
    # somme instantanée des courants
    if t > 17:
        q = prog(t, 17, 18)
        bx, by, bh = X0 + 20, 745, 95
        d.line((bx - 10, by, bx + 470, by), fill=mix(WHITE, GREY, q), width=2)
        vals = [math.sqrt(2) * IY * math.sin(OM * t + math.radians(a)) for a in ANG_E]
        for k, v in enumerate(vals):
            x = bx + k * 120
            hh = v / (IY * math.sqrt(2)) * bh
            d.rectangle((x, min(by, by - hh), x + 70, max(by, by - hh)), fill=mix(WHITE, PH[k], q))
            rich(d, (x + 35, by + bh + 25), [("i", 0), (str(k + 1), 1)], 26, mix(WHITE, PH[k], q), True, anchor="m")
        sx = bx + 380
        d.rectangle((sx, by - 3, sx + 70, by + 3), fill=mix(WHITE, RED, q))
        rich(d, (sx + 35, by + bh + 25), [("i", 0), ("N", 1), (" = 0", 0)], 26, mix(WHITE, RED, q), True, anchor="m")
        text(d, (bx, by - bh - 40), "valeurs instantanées", 22, mix(WHITE, GREY, q), italic=True)
    if t > 25:
        q = prog(t, 25, 26)
        lay = Image.new("RGB", (BAND_X, H), WHITE); dl = ImageDraw.Draw(lay)
        plaque(dl, 1030, 640, "Y", 0.85, prog(t, 26, 27))
        rbox(dl, (1340, 600, 1720, 860), fill=TINT, r=14)
        rich(dl, (1360, 640), [("Puissance", 0)], 26, BLUE, True)
        rich(dl, (1360, 690), [("P = 3 · U", 0), ("ph", 1), ("² / R", 0)], 28, NAVY, True)
        rich(dl, (1360, 740), [("= 3 · 231² / 40", 0)], 28, NAVY)
        text(dl, (1360, 800), "= 4 000 W", 40, NAVY, True, anchor="lm")
        box = (1000, 560, 1730, 880)
        reg = lay.crop(box); img.paste(Image.blend(Image.new("RGB", reg.size, WHITE), reg, q), box[:2])
    caption(d, cap_at(t, [(0, "En étoile, chaque élément relie un conducteur polaire au point étoile commun."),
                          (5, "Le voltmètre sur Z1 lit la tension de phase : 231 V. Chaque élément travaille sous 231 V."),
                          (10, "Les points représentent les charges : elles vont et viennent au rythme du réseau."),
                          (12, "Le même courant traverse le fil de ligne puis l'élément : I = Iph = 5,77 A."),
                          (17, "À chaque instant i1 + i2 + i3 = 0 : avec une charge équilibrée, le neutre ne transporte rien."),
                          (25, "Sur la plaque à bornes : une barrette horizontale relie W2, U2 et V2. Puissance : 4 kW.")]))


def s_triangle(img, d, t):
    chrome(img, d, "3 · COUPLAGE TRIANGLE Δ", "Chaque élément entre deux phases", "3/5")
    ox, oy = 170, 230
    P, A, B, C = draw_tri(d, t, ox, oy, 1.0, heat=1.0, show_lines_flow=t > 10)
    if t > 5:
        q = prog(t, 5, 6)
        col = mix(WHITE, BLUE, q)
        # voltmètre en parallèle sur Z1 (entre A et B), décalé vers l'extérieur
        nx, ny = -(B[1] - A[1]), (B[0] - A[0]); L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
        pa = (A[0] + (B[0] - A[0]) * 0.18, A[1] + (B[1] - A[1]) * 0.18); pb = (A[0] + (B[0] - A[0]) * 0.82, A[1] + (B[1] - A[1]) * 0.82)
        off = 95
        qa = (pa[0] + nx * off, pa[1] + ny * off); qb = (pb[0] + nx * off, pb[1] + ny * off)
        d.line((pa, qa), fill=col, width=2); d.line((pb, qb), fill=col, width=2); d.line((qa, qb), fill=col, width=2)
        cx, cy = (qa[0] + qb[0]) / 2, (qa[1] + qb[1]) / 2
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=WHITE, outline=col, width=4)
        text(d, (cx, cy), "V", 30, col, True, anchor="mm")
    X0 = 1010
    meter(d, (X0, 190, X0 + 340, 300), [("tension sur Z", 0), ("1", 1)], "400 V", alpha=prog(t, 5.5, 6.5))
    meter(d, (X0, 320, X0 + 340, 430), [("courant dans Z", 0), ("1", 1)], fr(IPH_D, 2) + " A", alpha=prog(t, 8, 9))
    meter(d, (X0 + 370, 190, X0 + 710, 300), [("courant de ligne I", 0)], fr(ID, 2) + " A", alpha=prog(t, 11, 12))
    if t > 6.5:
        q = prog(t, 6.5, 7.5)
        rich(d, (X0 + 370, 345), [("U", 0), ("ph", 1), (" = U = 400 V", 0)], 30, mix(WHITE, NAVY, q), True)
    if t > 8.5:
        q = prog(t, 8.5, 9.5)
        rich(d, (X0 + 370, 395), [("I", 0), ("ph", 1), (" = 400 / 40 = 10 A", 0)], 30, mix(WHITE, NAVY, q), True)
    # Kirchhoff au nœud A : I1 = Iph(Z1) − Iph(Z3), construction vectorielle
    if 14 <= t < 27:
        q = prog(t, 14, 15)
        bx0, by0 = 1010, 460
        rbox(d, (bx0, by0, 1730, 880), fill=mix(WHITE, (246, 249, 255), q), outline=mix(WHITE, LBLUE, q), width=3, r=16)
        rich(d, (bx0 + 25, by0 + 40), [("Nœud A (L1) : I = I", 0), ("Z1", 1), (" − I", 0), ("Z3", 1), (" (addition vectorielle)", 0)], 28, mix(WHITE, NAVY, q), True)
        o = (bx0 + 230, by0 + 400); k = 18.0
        a1 = math.radians(ANG_U[0]); a3 = math.radians(ANG_U[2])
        p1 = (o[0] + k * IPH_D * math.cos(a1), o[1] - k * IPH_D * math.sin(a1))
        r2 = prog(t, 16.5, 18.5)
        p2 = (p1[0] - k * IPH_D * math.cos(a3) * r2, p1[1] + k * IPH_D * math.sin(a3) * r2)
        if prog(t, 15, 16) > 0: arrow(d, o, p1, mix(WHITE, NAVY, prog(t, 15, 16)), 6, 24)
        if r2 > 0: arrow(d, p1, p2, mix(WHITE, GREY, r2), 6, 24)
        if t > 15.5: rich(d, ((o[0] + p1[0]) / 2 - 20, (o[1] + p1[1]) / 2 + 10), [("I", 0), ("Z1", 1), (" = 10 A", 0)], 24, NAVY, True, anchor="r")
        if t > 18.5: rich(d, ((p1[0] + p2[0]) / 2 + 60, (p1[1] + p2[1]) / 2 + 5), [("−I", 0), ("Z3", 1), (" = 10 A", 0)], 24, GREY, True)
        r3 = prog(t, 19.5, 21)
        if r3 > 0:
            pe = (o[0] + (p2[0] - o[0]) * r3, o[1] + (p2[1] - o[1]) * r3)
            arrow(d, o, pe, RED, 8, 28)
        if t > 21:
            rich(d, (o[0] + 20, (o[1] + p2[1]) / 2 + 60), [("I = 17,3 A", 0)], 30, RED, True)
            text(d, (o[0] - 26, o[1] - 105), "30°", 22, RED, anchor="mm")
        if t > 22.5:
            q2 = prog(t, 22.5, 23.5)
            rbox(d, (bx0 + 450, by0 + 120, 1710, by0 + 330), fill=mix(WHITE, TINT, q2), r=14)
            rich(d, (bx0 + 495, by0 + 170), [("I = √3 · I", 0), ("ph", 1)], 34, mix(TINT, NAVY, q2), True)
            text(d, (bx0 + 495, by0 + 230), "= 1,73 × 10 A", 28, mix(TINT, NAVY, q2), anchor="lm")
            text(d, (bx0 + 495, by0 + 280), "pas 20 A ! (120°)", 26, mix(TINT, RED, q2), True, anchor="lm")
    if t >= 27:
        q = prog(t, 27, 28)
        lay = Image.new("RGB", (BAND_X, H), WHITE); dl = ImageDraw.Draw(lay)
        plaque(dl, 1030, 640, "D", 0.85, prog(t, 28, 29))
        rbox(dl, (1340, 600, 1720, 860), fill=TINT, r=14)
        rich(dl, (1360, 640), [("Puissance", 0)], 26, BLUE, True)
        rich(dl, (1360, 690), [("P = 3 · U² / R", 0)], 28, NAVY, True)
        rich(dl, (1360, 740), [("= 3 · 400² / 40", 0)], 28, NAVY)
        text(dl, (1360, 800), "= 12 000 W", 40, RED, True, anchor="lm")
        box = (1000, 470, 1730, 880)
        reg = lay.crop(box); img.paste(Image.blend(Image.new("RGB", reg.size, WHITE), reg, q), box[:2])
    caption(d, cap_at(t, [(0, "En triangle, chaque élément relie deux conducteurs polaires. Il n'y a ni point étoile ni neutre."),
                          (5, "Le voltmètre sur Z1 lit la tension réseau : 400 V au lieu de 231 V. Les éléments chauffent beaucoup plus."),
                          (8, "Courant dans un élément : 400 V / 40 Ω = 10 A."),
                          (10, "Dans les fils de ligne, les charges bougent encore plus : le courant de ligne vaut 17,3 A."),
                          (14, "Au nœud A arrivent deux courants d'éléments. Ils sont décalés de 120° : on les additionne en vecteurs."),
                          (21, "Résultat : I = √3 × 10 A = 17,3 A. Erreur classique : écrire 2 × 10 A ou 3 × 10 A."),
                          (27, "Sur la plaque à bornes : trois barrettes verticales. Puissance : 12 kW, trois fois plus qu'en étoile.")]))


def s_compare(img, d, t):
    chrome(img, d, "4 · COMPARAISON", "Mêmes trois résistances, deux couplages", "4/5")
    draw_star(d, t, 150, 190, 0.6, neutre=False, labels=False, heat=PY / PD)
    draw_tri(d, t, 990, 190, 0.6, labels=False, heat=1.0)
    text(d, (390, 170), "étoile Y", 34, BLUE, True, anchor="mm")
    text(d, (1230, 170), "triangle Δ", 34, BLUE, True, anchor="mm")
    rows = [([("Tension sur un élément", 0)], "231 V", "400 V", "× √3"),
            ([("Courant dans un élément", 0)], "5,77 A", "10 A", "× √3"),
            ([("Courant de ligne", 0)], "5,77 A", "17,3 A", "× 3"),
            ([("Puissance totale", 0)], "4 kW", "12 kW", "× 3")]
    x0, y0, rh = 140, 545, 68
    cx = [140, 760, 1080, 1400, 1700]
    if t > 1.5:
        q = prog(t, 1.5, 2.5)
        d.rectangle((x0, y0, cx[4], y0 + 50), fill=mix(WHITE, LBLUE, q))
        for j, h in enumerate(["", "Étoile Y", "Triangle Δ", "Δ par rapport à Y"]):
            text(d, ((cx[j] + cx[j + 1]) / 2 if j else cx[0] + 20, y0 + 25), h, 26, mix(WHITE, NAVY, q), True, anchor="mm" if j else "lm")
    for i, (lab, a, b, k) in enumerate(rows):
        q = prog(t, 3 + i * 3.5, 4 + i * 3.5)
        if q <= 0: continue
        y = y0 + 50 + i * rh
        d.rectangle((x0, y, cx[4], y + rh), outline=mix(WHITE, NAVY, q), width=2)
        rich(d, (x0 + 20, y + rh / 2), lab, 28, mix(WHITE, NAVY, q), True)
        text(d, ((cx[1] + cx[2]) / 2, y + rh / 2), a, 34, mix(WHITE, NAVY, q), True, anchor="mm")
        text(d, ((cx[2] + cx[3]) / 2, y + rh / 2), b, 34, mix(WHITE, NAVY, q), True, anchor="mm")
        q2 = prog(t, 4.5 + i * 3.5, 5.5 + i * 3.5)
        text(d, ((cx[3] + cx[4]) / 2, y + rh / 2), k, 38, mix(WHITE, RED, q2), True, anchor="mm")
    caption(d, cap_at(t, [(0, "Côte à côte : regarde la couleur des résistances et l'amplitude du va-et-vient des charges."),
                          (3, "En triangle, chaque élément reçoit √3 fois plus de tension…"),
                          (6.5, "… donc √3 fois plus de courant dans chaque élément (loi d'Ohm)."),
                          (10, "Courant de ligne : √3 (tension) × √3 (nœud) = 3 fois plus."),
                          (13.5, "Puissance : P varie avec U², donc (√3)² = 3 fois plus. La formule P = √3 · U · I · cos φ reste la même pour les deux."),
                          (19, "La formule P = √3 · U · I · cos φ vaut pour les deux couplages. C'est le couplage qui fixe la tension de chaque élément, donc la puissance.")]))


def s_demarrage(img, d, t):
    chrome(img, d, "5 · DANS LA VRAIE VIE", "Le démarrage étoile-triangle d'un moteur", "5/5")
    TSW = 9.0                                  # commutation Y → Δ
    mode = "Y" if t < TSW else "D"
    # moteur
    mx, my, mr = 330, 420, 150
    speed = 0.0
    if t > 1.5: speed = 0.85 * (1 - math.exp(-(t - 1.5) / 2.2))
    if t > TSW: speed = 0.85 + 0.15 * (1 - math.exp(-(t - TSW) / 0.8))
    ang = 0.0
    # angle = intégrale de la vitesse (approx. numérique simple)
    n = int(max(t, 0) * 20)
    for i in range(n):
        tt = i / 20; sp = 0 if tt < 1.5 else (0.85 * (1 - math.exp(-(tt - 1.5) / 2.2)) if tt < TSW else 0.85 + 0.15 * (1 - math.exp(-(tt - TSW) / 0.8)))
        ang += sp * 360 * 1.2 / 20
    d.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=(243, 245, 249), outline=NAVY, width=6)
    for k in range(3):
        a = math.radians(ang + k * 120)
        d.line((mx, my, mx + (mr - 25) * math.cos(a), my + (mr - 25) * math.sin(a)), fill=LBLUE, width=10)
    text(d, (mx, my - 10), "M", 70, NAVY, True, anchor="mm")
    text(d, (mx, my + 50), "3~", 34, NAVY, True, anchor="mm")
    text(d, (mx, my + mr + 40), "pompe, 400 Δ / 690 Y", 26, GREY, anchor="mm")
    # barre de vitesse
    d.rectangle((140, 690, 520, 720), outline=NAVY, width=2)
    d.rectangle((140, 690, 140 + 380 * speed, 720), fill=BLUE)
    text(d, (140, 670), "vitesse", 22, GREY, anchor="ls")
    # plaque
    plaque(d, 600, 330, mode, 0.9, 1.0, label=False)
    text(d, (735, 540), "Y : 231 V par enroulement" if mode == "Y" else "Δ : 400 V par enroulement", 24, BLUE if mode == "Y" else RED, True, anchor="mm")
    if TSW - 0.3 < t < TSW + 1.2:
        text(d, (735, 600), "commutation !", 30, RED, True, anchor="mm")
    # graphique courant
    gx0, gx1, gy0, gy1 = 960, 1700, 780, 230
    d.line((gx0, gy0, gx1, gy0), fill=NAVY, width=2); d.line((gx0, gy0, gx0, gy1), fill=NAVY, width=2)
    text(d, (gx1, gy0 + 34), "temps (s)", 22, GREY, anchor="ra")
    text(d, (gx0 - 10, gy1 - 20), "courant de ligne / courant nominal", 22, GREY, anchor="ls")
    Tmax = 16.0; Imax = 7.0
    X = lambda tt: gx0 + (gx1 - gx0) * tt / Tmax
    Y = lambda v: gy0 - (gy0 - gy1) * v / Imax
    for v in range(0, 8):
        d.line((gx0 - 8, Y(v), gx0, Y(v)), fill=NAVY, width=2)
        text(d, (gx0 - 14, Y(v)), str(v), 20, GREY, anchor="rm")
        if v: d.line((gx0, Y(v), gx1, Y(v)), fill=(232, 236, 244), width=1)
    d.line((gx0, Y(1), gx1, Y(1)), fill=GREEN, width=2)
    text(d, (gx1 - 4, Y(1) - 14), "nominal", 20, GREEN, anchor="rs")

    def i_direct(tt):
        if tt < 1.5: return 0
        return 1 + 5.0 * math.exp(-max(tt - 1.5 - 1.2, 0) / 1.0) if tt < 2.7 else 1 + 5.0 * math.exp(-(tt - 2.7) / 1.0)

    def i_yd(tt):
        if tt < 1.5: return 0
        if tt < TSW: return (1 + 5.0 * math.exp(-max(tt - 2.7, 0) / 1.0)) / 3 + 0.6 * (1 - math.exp(-(tt - 1.5) / 3)) * 0.5
        return 1 + 1.8 * math.exp(-(tt - TSW) / 0.5)

    if t > 3:
        q = prog(t, 3, 4)
        pts = [(X(tt / 20), Y(i_direct(tt / 20))) for tt in range(0, int(Tmax * 20) + 1)]
        for i in range(0, len(pts) - 1, 2):
            d.line((pts[i], pts[i + 1]), fill=mix(WHITE, GREY, q), width=3)
        text(d, (X(3.0) + 10, Y(5.6)), "démarrage direct en Δ", 22, mix(WHITE, GREY, q), anchor="lm")
    tc = min(t, Tmax)
    pts = [(X(tt / 20), Y(i_yd(tt / 20))) for tt in range(0, int(tc * 20) + 1)]
    if len(pts) > 1: d.line(pts, fill=BLUE, width=6, joint="curve")
    if pts: d.ellipse((pts[-1][0] - 8, pts[-1][1] - 8, pts[-1][0] + 8, pts[-1][1] + 8), fill=BLUE)
    if t > TSW: d.line((X(TSW), gy0, X(TSW), gy1 + 40), fill=RED, width=2)
    if t > TSW: text(d, (X(TSW) + 8, gy1 + 50), "Y → Δ", 22, RED, True, anchor="lm")
    if t > 5:
        q = prog(t, 5, 6)
        text(d, (X(3.4), Y(2.4)), "étoile : courant ÷ 3", 24, mix(WHITE, BLUE, q), True, anchor="lm")
    caption(d, cap_at(t, [(0, "Un moteur de 400 Δ doit tourner en triangle. Démarré directement, il appelle environ 6 fois son courant nominal."),
                          (3, "En pointillé : le démarrage direct en triangle. Ce pic fait chuter la tension du réseau et déclenche des protections."),
                          (5, "On démarre donc en étoile : chaque enroulement reçoit 231 V et le courant de ligne est divisé par 3."),
                          (9, "Quand le moteur a presque atteint sa vitesse, un contacteur passe en triangle : 400 V par enroulement, pleine puissance."),
                          (13, "On trouve ce démarrage sur les pompes, les ventilateurs et les compresseurs de quelques kW et plus.")]))


def s_outro(img, d, t):
    chrome(img, d, "À RETENIR", "Étoile ou triangle ?", "")
    rows = [("Lire la plaque", "la plus petite tension = tension d'un enroulement"),
            ("230 Δ / 400 Y", "sur 3 × 400 V → étoile (231 V par enroulement)"),
            ("400 Δ / 690 Y", "sur 3 × 400 V → triangle (400 V par enroulement)"),
            ("Erreur de couplage", "Y au lieu de Δ : 1/3 de la puissance ; Δ au lieu de Y : l'enroulement brûle")]
    for i, (a, b) in enumerate(rows):
        q = prog(t, 0.3 + i * 0.8, 0.9 + i * 0.8)
        if q <= 0: continue
        y = 200 + i * 160
        rbox(d, (60, y, BAND_X - 50, y + 130), fill=mix(WHITE, TINT, q), r=16)
        d.ellipse((90, y + 30, 160, y + 100), fill=mix(WHITE, NAVY, q))
        text(d, (125, y + 65), str(i + 1), 36, WHITE, True, anchor="mm")
        text(d, (200, y + 65), a, 40, mix(WHITE, NAVY, q), True, anchor="lm")
        text(d, (680, y + 65), b, 32, mix(WHITE, NAVY, q), anchor="lm")
    caption(d, "À toi : labo triphasé (artefact) puis fiche d'exercices N°1, N°4 et N°7.", prog(t, 3.5, 4.2))


SCENES = [(s_intro, 8.0), (s_reseau, 23.0), (s_etoile, 34.0), (s_triangle, 36.0), (s_compare, 25.0), (s_demarrage, 19.0), (s_outro, 10.0)]
SCENES = [(f, dur * RALENTI) for f, dur in SCENES]     # durées étirées par RALENTI
XF, FADE = 1.2, 0.6


def frame_at(i, t):
    img = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(img)
    SCENES[i][0](img, d, t / RALENTI)                  # le temps de la scène s'écoule RALENTI fois moins vite
    return img


def render(out="out/Etoile ou triangle – animation.mp4"):
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
    if len(sys.argv) > 2:
        i, t = int(sys.argv[1]), float(sys.argv[2])
        frame_at(i, t).save(f"/tmp/prev_{i}_{t}.png")
    else:
        render()
