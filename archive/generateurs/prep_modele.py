# -*- coding: utf-8 -*-
"""Prépare le modèle ETML pour les générateurs.
Source : le fichier du projet « ETML_modele.zip » (contient « _Rapport Simple.dotx »), récupéré avec
Projects.project_read("ETML_modele.zip") → octets exacts dans un fichier local. Ne plus utiliser la copie
charte/ETML_Rapport_Simple.dotx.b64 (texte trop long pour être recopié sans erreur).
Produit : etml_base.docx (content-type document), logo.png (noir) et logo_white_v.png (blanc, vertical, bande bleue des présentations).
Usage : python3 prep_modele.py <chemin du zip ou du .dotx>"""
import sys, io, zipfile
from PIL import Image

src = sys.argv[1]
raw = open(src, "rb").read()
z = zipfile.ZipFile(io.BytesIO(raw))
dotx = [n for n in z.namelist() if n.lower().endswith(".dotx") and not n.startswith("__MACOSX")]
if dotx:                                   # zip contenant le .dotx
    raw = z.read(dotx[0]); z = zipfile.ZipFile(io.BytesIO(raw))
open("Rapport_Simple.dotx", "wb").write(raw)
data = {i.filename: z.read(i.filename) for i in z.infolist()}   # lire tout AVANT d'écrire (writestr modifie les ZipInfo)
o = zipfile.ZipFile("etml_base.docx", "w", zipfile.ZIP_DEFLATED)
for name, d in data.items():
    if name == "[Content_Types].xml": d = d.replace(b"template.main+xml", b"document.main+xml")
    o.writestr(name, d)
o.close()
open("logo.png", "wb").write(data["word/media/image1.png"])
im = Image.open("logo.png").convert("RGBA"); w = Image.new("RGBA", im.size, (255, 255, 255, 0)); w.putalpha(im.split()[3])
w.rotate(90, expand=True).save("logo_white_v.png")
print("ok : etml_base.docx, logo.png, logo_white_v.png")
