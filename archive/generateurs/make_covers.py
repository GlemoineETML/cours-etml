#!/usr/bin/env python3
"""Images de couverture des vidéos 105 et 125 pour les présentations : image de l'intro + bouton lecture + durée."""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
FD = "/usr/share/fonts/truetype/liberation/"
for num, mp4, dur in (("105", "out/105 Familles de circuits logiques.mp4", "4 min 48"), ("125", "out/125 Portes logiques et tables de vérité.mp4", "5 min 25")):
    if len(sys.argv) > 1 and num not in sys.argv[1:]: continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "7", "-i", mp4, "-frames:v", "1", "-vf", "scale=1280:720", f"cover_{num}.png"], check=True)
    im = Image.open(f"cover_{num}.png").convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    cx, cy, r = 1092, 370, 74
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(36, 40, 82, 215))
    d.polygon([(cx - 26, cy - 40), (cx - 26, cy + 40), (cx + 44, cy)], fill=(255, 255, 255, 255))
    f = ImageFont.truetype(FD + "LiberationSans-Bold.ttf", 34)
    d.rounded_rectangle((cx - 80, cy + r + 18, cx + 80, cy + r + 70), radius=12, fill=(36, 40, 82, 215))
    d.text((cx, cy + r + 44), dur, font=f, fill=(255, 255, 255, 255), anchor="mm")
    Image.alpha_composite(im, ov).convert("RGB").save(f"cover_{num}.png")
    print("ok cover", num)
