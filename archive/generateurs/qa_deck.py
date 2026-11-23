# -*- coding: utf-8 -*-
"""Contrôle géométrique d'un deck : débordements et chevauchements."""
import sys
from pptx import Presentation
from pptx.util import Emu

EMU_IN = 914400.0
prs = Presentation(sys.argv[1])
W, H = prs.slide_width / EMU_IN, prs.slide_height / EMU_IN
pb = []
for i, sl in enumerate(prs.slides, 1):
    boxes = []
    for sh in sl.shapes:
        if sh.left is None:
            continue
        x, y = sh.left / EMU_IN, sh.top / EMU_IN
        w, h = sh.width / EMU_IN, sh.height / EMU_IN
        nom = sh.shape_type
        if sh.has_text_frame and not sh.text_frame.text.strip() and sh.shape_type != 13:
            continue
        boxes.append((x, y, w, h, str(sh.name)))
        if sh.name.startswith("Title"):
            continue
        if y + h > H - 0.08 or x + w > 8.88 or x < 0.28 or y < -0.02:
            pb.append("diapo %2d : %-28s sort de la zone utile (bas=%.2f / droite=%.2f)"
                      % (i, sh.name, y + h, x + w))
    for a in range(len(boxes)):
        for b in range(a + 1, len(boxes)):
            x1, y1, w1, h1, n1 = boxes[a]
            x2, y2, w2, h2, n2 = boxes[b]
            ox = min(x1 + w1, x2 + w2) - max(x1, x2)
            oy = min(y1 + h1, y2 + h2) - max(y1, y2)
            if ox > 0.12 and oy > 0.12:
                pb.append("diapo %2d : %s ∩ %s  (%.2f × %.2f in)"
                          % (i, n1, n2, ox, oy))
print("\n".join(pb) if pb else "géométrie : aucun problème")
print("total :", len(pb))
