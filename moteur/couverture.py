# -*- coding: utf-8 -*-
"""Image de couverture d'une vidéo pour les présentations : l'image à 7 s (carte d'introduction),
un bouton lecture et la durée, aux couleurs ETML."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/truetype/liberation/"


def produire(mp4, png, duree, instant=7):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(instant), "-i", mp4, "-frames:v", "1", "-vf", "scale=1280:720", png], check=True)
    im = Image.open(png).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    cx, cy, r = 1092, 370, 74
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(36, 40, 82, 215))
    d.polygon([(cx - 26, cy - 40), (cx - 26, cy + 40), (cx + 44, cy)], fill=(255, 255, 255, 255))
    f = ImageFont.truetype(FD + "LiberationSans-Bold.ttf", 34)
    d.rounded_rectangle((cx - 80, cy + r + 18, cx + 80, cy + r + 70), radius=12, fill=(36, 40, 82, 215))
    d.text((cx, cy + r + 44), duree, font=f, fill=(255, 255, 255, 255), anchor="mm")
    Image.alpha_composite(im, ov).convert("RGB").save(png)
    print("ok", os.path.basename(png))
