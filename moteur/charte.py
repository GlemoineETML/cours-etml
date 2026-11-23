# -*- coding: utf-8 -*-
"""Charte ETML (REGLES 4 et 5) : couleurs, et préparation du modèle Word et des logos à partir de modeles/.

prepare(dossier) écrit dans `dossier` :
  etml_base.docx      le modèle Rapport_Simple.dotx enregistré comme document (base de toutes les fiches)
  logo.png            logo du modèle (word/media/image1.png, wordmark ETML noir)
  logo_white_v.png    logo blanc, vertical : bande bleue des présentations
  logo_white_h.png    logo blanc, horizontal, 72 px de haut : bandeau des pages interactives
"""
import io, os, zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELE = os.path.join(RACINE, "modeles", "Rapport_Simple.dotx")

NAVY, BLUE, LBLUE, TINT, RED, GREY = "242852", "297FD5", "ACCBF9", "E8EFFB", "EE0000", "5A6478"


def prepare(dossier, modele=MODELE):
    from PIL import Image
    os.makedirs(dossier, exist_ok=True)
    raw = open(modele, "rb").read()
    z = zipfile.ZipFile(io.BytesIO(raw))
    data = {i.filename: z.read(i.filename) for i in z.infolist()}   # lire tout AVANT d'écrire (writestr modifie les ZipInfo)
    o = zipfile.ZipFile(os.path.join(dossier, "etml_base.docx"), "w", zipfile.ZIP_DEFLATED)
    for name, d in data.items():
        if name == "[Content_Types].xml": d = d.replace(b"template.main+xml", b"document.main+xml")
        o.writestr(name, d)
    o.close()
    logo = os.path.join(dossier, "logo.png")
    open(logo, "wb").write(data["word/media/image1.png"])
    im = Image.open(logo).convert("RGBA")
    blanc = Image.new("RGBA", im.size, (255, 255, 255, 0)); blanc.putalpha(im.split()[3])
    blanc.rotate(90, expand=True).save(os.path.join(dossier, "logo_white_v.png"))
    h = 72
    blanc.resize((round(im.size[0] * h / im.size[1]), h), Image.LANCZOS).save(os.path.join(dossier, "logo_white_h.png"))
    return dossier
