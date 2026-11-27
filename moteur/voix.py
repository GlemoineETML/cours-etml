# -*- coding: utf-8 -*-
"""Voix off des animations : synthèse vocale (Piper, voix française fr-siwis-medium) à partir d'un texte calé,
<num>-narration.md (tableau « | Début | Scène | Texte | », début en secondes), puis mixage sur la vidéo.

Le modèle de voix n'est pas versionné : il est cherché dans ~/.cache/etml-voix/ (ou $ETML_VOIX) et téléchargé au besoin
depuis https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-fr-siwis-medium.tar.gz (pip install piper-tts).
Débit : LONGUEUR < 1 accélère (voix tonique). Une réplique qui déborde sur la suivante est une erreur bloquante."""
import os, re, subprocess, tempfile, wave

MODELE = "fr-siwis-medium.onnx"
URL = "https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-fr-siwis-medium.tar.gz"
LONGUEUR, VARIATION, VARIATION_W = 0.86, 0.75, 0.9      # débit, expressivité de la voix, variation du rythme
DOSSIER = os.environ.get("ETML_VOIX", os.path.expanduser("~/.cache/etml-voix"))

# écritures que la synthèse lit mal : remplacées avant la lecture (le texte affiché ne change pas)
DIRE = [(r" = ", " égale "), (r"\b74HC0(\d)\b", r"septante-quatre H C zéro \1"), (r"\b74HC(\d+)\b", r"septante-quatre H C \1"),
        (r"\bNON-OU\b", "non ou"), (r"\bNON-ET\b", "non et"), (r"\bCMOS\b", "cé mosse"),   # « 74 » : septante (Suisse romande)
        (r"\bles 1\b", "les uns"), (r"\bLe 1\b", "Le un"), (r"\b1, 2, 4 ou 8\b", "un, deux, quatre ou huit"),
        (r"\b1\b", "un"), (r"\bX\b", "iks"), (r"\bfiche 230\b", "fiche deux cent trente"), (r"\bpage 221\b", "page deux cent vingt et un")]


def modele():
    m = os.path.join(DOSSIER, MODELE)
    if not os.path.exists(m):
        os.makedirs(DOSSIER, exist_ok=True)
        tgz = os.path.join(DOSSIER, "voix.tar.gz")
        subprocess.run(["curl", "-sL", "-o", tgz, URL], check=True)
        subprocess.run(["tar", "xzf", tgz, "-C", DOSSIER], check=True)
    return m


def repliques(md):
    """[(début en s, scène, texte)] lus dans le tableau du fichier de narration."""
    out = []
    for l in open(md, encoding="utf-8"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) == 3 and re.match(r"^\d+([,.]\d+)?$", c[0]):
            out.append((float(c[0].replace(",", ".")), c[1], c[2]))
    return out


def duree(wav):
    with wave.open(wav) as w:
        return w.getnframes() / w.getframerate()


def produire(md, mp4, sortie=None):
    """Ajoute la voix off à mp4 (remplacé, ou écrit dans sortie). Renvoie [(début, fin, texte)] ; lève une erreur si une réplique déborde."""
    R = repliques(md)
    tmp = tempfile.mkdtemp()
    m = modele()
    for i, (t0, _, txt) in enumerate(R):
        dit = txt
        for a, b in DIRE:
            dit = re.sub(a, b, dit)
        subprocess.run(["python3", "-m", "piper", "-m", m, "--length-scale", str(LONGUEUR), "--noise-scale", str(VARIATION),
                        "--noise-w-scale", str(VARIATION_W), "--sentence-silence", "0.15", "-f", os.path.join(tmp, f"r{i:02d}.wav")],
                       input=dit.encode("utf-8"), check=True, stderr=subprocess.DEVNULL)
    fin_video = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                                     capture_output=True, text=True).stdout)
    calage, erreurs = [], []
    for i, (t0, sc, txt) in enumerate(R):
        t1 = t0 + duree(os.path.join(tmp, f"r{i:02d}.wav"))
        limite = R[i + 1][0] if i + 1 < len(R) else fin_video
        if t1 > limite - 0.1:
            erreurs.append(f"réplique à {t0} s ({sc}) : finit à {t1:.1f} s, après {limite} s : raccourcir le texte")
        calage.append((t0, t1, txt))
    if erreurs:
        raise ValueError("voix off trop longue :\n" + "\n".join(erreurs))
    # mixage : chaque réplique placée à son début, voix compressée et normalisée (−16 LUFS, niveau d'une vidéo pédagogique)
    entrees, filtres = [], []
    for i, (t0, _, _) in enumerate(R):
        entrees += ["-i", os.path.join(tmp, f"r{i:02d}.wav")]
        filtres.append(f"[{i + 1}:a]adelay={int(t0 * 1000)}|{int(t0 * 1000)}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(R))) + f"amix=inputs={len(R)}:normalize=0,acompressor=threshold=-20dB:ratio=3:attack=5:release=80," \
          f"loudnorm=I=-16:TP=-1.5:LRA=7,apad[voix]"
    out = sortie or mp4 + ".voix.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4] + entrees +
                   ["-filter_complex", ";".join(filtres + [mix]), "-map", "0:v", "-map", "[voix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    if not sortie:
        os.replace(out, mp4)
    return calage
