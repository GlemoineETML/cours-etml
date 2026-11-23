# -*- coding: utf-8 -*-
"""Chapitre 500 — blocs d'équations refaits.

Convention d'écriture : dès la ligne numérique, tout résultat porte son unité,
et l'unité s'écrit entre crochets — 50,0 [mA], 4,00 [V], 3,33·10⁶ [Ω].
Chaque exemple se termine par son contrôle : loi des nœuds pour le voltmètre,
loi des mailles pour l'ampèremètre.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eqimg import bloc, NAVY, BLUE, RED, GREY

A, N, I = "algébrique", "numérique", "ingénieur"
R_ = {"color": RED}
VERT = "#26663F"
V_ = {"color": VERT}

# ------------------------------------------------- le calcul du voltmètre
bloc("fig/eq7_volt_methode.png", [
    ("① le groupe mesuré", r"$R_{2V} = \frac{R_2 \cdot R_V}{R_2 + R_V}$"
                           r"      $[\Omega]$", {"size": 19}),
    (None, None),
    ("② le diviseur réel", r"$U_{mes} = U \cdot \frac{R_{2V}}{R_1 + R_{2V}}$"
                           r"      $[\mathrm{V}]$", {"size": 19}),
    (None, None),
    (None, r"deux formules déjà connues : un groupe parallèle, puis un "
           r"diviseur de tension", {"size": 16, "color": BLUE}),
], interligne=0.56, x_eq=0.215)

# ------------------------------------------------- l'exemple du voltmètre
bloc("fig/eq7_volt_exemple.png", [
    (A, r"$R_{2V} = \frac{R_2 \cdot R_V}{R_2 + R_V}$"),
    (N, r"$R_{2V} = \frac{5 \cdot 10^{6} \cdot 10 \cdot 10^{6}}"
        r"{15 \cdot 10^{6}} = 3{,}33 \cdot 10^{6}\ [\Omega]$"),
    (A, r"$U_{mes} = U \cdot \frac{R_{2V}}{R_1 + R_{2V}}$"),
    (N, r"$U_{mes} = 10 \cdot \frac{3{,}33 \cdot 10^{6}}"
        r"{8{,}33 \cdot 10^{6}} = 4{,}00\ [\mathrm{V}]$"),
    (I, r"$U_{mes} = 4{,}00\ [\mathrm{V}]$   au lieu de   "
        r"$5{,}00\ [\mathrm{V}]$", R_),
    ("contrôle · nœuds", r"$I_2 + I_V = 0{,}80 + 0{,}40 = 1{,}20\ "
                         r"[\mathrm{\mu A}] = I_1$", V_),
], interligne=0.55, x_eq=0.155)

# ------------------------------------------------- le calcul de l'ampèremètre
bloc("fig/eq7_amp_methode.png", [
    ("courant mesuré", r"$I_{mes} = \frac{U}{R + R_A}$      $[\mathrm{A}]$",
     {"size": 19}),
    (None, None),
    ("tension volée", r"$U_A = R_A \cdot I_{mes}$      $[\mathrm{V}]$",
     {"size": 19}),
    (None, None),
    (None, r"une simple somme série : la résistance de l'appareil s'ajoute "
           r"à celle du circuit", {"size": 16, "color": BLUE}),
], interligne=0.56, x_eq=0.185)

# ------------------------------------------------- l'exemple de l'ampèremètre
bloc("fig/eq7_amp_exemple.png", [
    (A, r"$I_{vrai} = \frac{U}{R}$          $I_{mes} = \frac{U}{R + R_A}$"),
    (N, r"$I_{vrai} = \frac{10}{180} = 55{,}6 \cdot 10^{-3}\ [\mathrm{A}]$      "
        r"$I_{mes} = \frac{10}{200} = 50{,}0 \cdot 10^{-3}\ [\mathrm{A}]$"),
    (I, r"$I_{mes} = 50{,}0\ [\mathrm{mA}]$   au lieu de   "
        r"$55{,}6\ [\mathrm{mA}]$", R_),
    (A, r"$U_A = R_A \cdot I_{mes} = 20 \cdot 50 \cdot 10^{-3} "
        r"= 1{,}00\ [\mathrm{V}]$"),
    ("contrôle · mailles", r"$U_A + U_R = 1{,}00 + 9{,}00 = 10{,}0\ "
                           r"[\mathrm{V}] = U$", V_),
], interligne=0.55, x_eq=0.165)

# ------------------------------------------------- les deux règles ensemble
bloc("fig/eq7_deux_regles.png", [
    ("voltmètre", r"$R_V \geq 100 \cdot R$      $[\Omega]$", {"size": 22}),
    (None, r"beaucoup PLUS GRAND que ce qu'il mesure",
     {"size": 16, "color": GREY, "x_eq": 0.155}),
    (None, None),
    ("ampèremètre", r"$R_A \leq \frac{R}{100}$      $[\Omega]$", {"size": 22}),
    (None, r"beaucoup PLUS PETIT que ce qu'il traverse",
     {"size": 16, "color": GREY, "x_eq": 0.155}),
], interligne=0.62, x_eq=0.155)

# ------------------------------------------------- l'ohmmètre en circuit
bloc("fig/eq7_ohm.png", [
    (None, r"$R_{lue} = \frac{R \cdot R_{reste}}{R + R_{reste}}$      "
           r"$[\Omega]$", {"size": 21}),
    (None, None),
    (N, r"$R_{lue} = \frac{12 \cdot 10^{3} \cdot 4 \cdot 10^{3}}"
        r"{16 \cdot 10^{3}} = 3 \cdot 10^{3}\ [\Omega]$"),
    (I, r"$R_{lue} = 3\ [\mathrm{k\Omega}]$   au lieu de   "
        r"$12\ [\mathrm{k\Omega}]$", R_),
], interligne=0.58, x_eq=0.135)

# ------------------------------------------------- l'écart, gardé pour la fin
bloc("fig/eq7_ecart.png", [
    (None, r"$\mathrm{\acute{e}cart} = \frac{\mathrm{mesure} - "
           r"\mathrm{valeur\ vraie}}{\mathrm{valeur\ vraie}} \cdot 100$"
           r"      $[\%]$", {"size": 19}),
    (None, None),
    ("le voltmètre", r"$\frac{4{,}00 - 5{,}00}{5{,}00} \cdot 100 = "
                     r"-20\ [\%]$", {"size": 18, "color": RED}),
    ("l'ampèremètre", r"$\frac{50{,}0 - 55{,}6}{55{,}6} \cdot 100 = "
                      r"-10\ [\%]$", {"size": 18, "color": RED}),
    (None, r"toujours négatif : un appareil ne peut que faire baisser ce "
           r"qu'il mesure", {"size": 16, "color": BLUE}),
], interligne=0.60, x_eq=0.155)

# ------------------------------------------------- l'exemple de la fiche ETML
bloc("fig/eq7_prec_fluke.png", [
    (None, r"$U_{lue} = 9{,}56\ [\mathrm{V}]$      échelle $60{,}00\ "
           r"[\mathrm{V}]$      résolution $0{,}01\ [\mathrm{V}]$",
     {"size": 18, "color": GREY}),
    (None, None),
    (None, r"Précision $= \pm(0{,}05\ \% \ \mathrm{de}\ U_{lue} + 1 "
           r"\times \mathrm{r\acute{e}solution})$", {"size": 19}),
    (None, r"$= \pm(0{,}05\ \%\ \mathrm{de}\ 9{,}56 + 1 \times 0{,}01)$",
     {"size": 19, "x_eq": 0.30}),
    (None, r"$= \pm(4{,}78 \cdot 10^{-3} + 10 \cdot 10^{-3}) "
           r"= \pm 14{,}78 \cdot 10^{-3}\ [\mathrm{V}]$",
     {"size": 19, "x_eq": 0.30}),
    (None, None),
    (None, r"$U_{mesur\acute{e}e} = 9{,}56\ [\mathrm{V}] \pm 15\ "
           r"[\mathrm{mV}]$", {"size": 20, "color": RED}),
    (None, r"la valeur vraie est entre $9{,}545\ [\mathrm{V}]$ et "
           r"$9{,}575\ [\mathrm{V}]$", {"size": 17, "color": VERT}),
], interligne=0.50, x_eq=0.20)

# ------------------------------------------------- précision n'est pas influence
bloc("fig/eq7_synthese.png", [
    (None, r"notre mesure de $4{,}00\ [\mathrm{V}]$, échelle $6{,}000\ "
           r"[\mathrm{V}]$, résolution $0{,}001\ [\mathrm{V}]$",
     {"size": 17, "color": GREY}),
    (None, None),
    ("précision", r"$\pm(0{,}05\ \%\ \mathrm{de}\ 4{,}00 + 1 \times 0{,}001) "
                  r"= \pm 3{,}00\ [\mathrm{mV}]$   soit   "
                  r"$\pm 0{,}075\ [\%]$", {"size": 18, "color": VERT}),
    (None, None),
    ("influence", r"$\frac{4{,}00 - 5{,}00}{5{,}00} \cdot 100 = -20\ [\%]$",
     {"size": 19, "color": RED}),
    (None, None),
    (None, r"l'influence est près de $270$ fois plus grande que la précision",
     {"size": 17, "color": BLUE}),
], interligne=0.54, x_eq=0.175)

# ------------------------------------------------- le formulaire
bloc("fig/eq7_formulaire.png", [
    ("voltmètre", r"$R_{2V} = \frac{R_2 \cdot R_V}{R_2 + R_V}$      "
                  r"$U_{mes} = U \cdot \frac{R_{2V}}{R_1 + R_{2V}}$      "
                  r"$R_V \geq 100\,R$", {"size": 18}),
    (None, None),
    ("ampèremètre", r"$I_{mes} = \frac{U}{R + R_A}$      "
                    r"$U_A = R_A \cdot I_{mes}$      "
                    r"$R_A \leq \frac{R}{100}$", {"size": 18}),
    (None, None),
    ("ohmmètre", r"$R_{lue} = \frac{R \cdot R_{reste}}{R + R_{reste}}$      "
                 r"analogique : $R_V = S \cdot U_{calibre}$", {"size": 18}),
    (None, None),
    ("précision", r"numérique : $\pm(p\ \%\ \mathrm{de}\ U_{lue} + n "
                  r"\times \mathrm{r\acute{e}solution})$      "
                  r"analogique : $\frac{\mathrm{classe}}{100} \cdot "
                  r"U_{calibre}$", {"size": 18}),
    (None, None),
    ("écart", r"$\mathrm{\acute{e}cart} = \frac{\mathrm{mesure} - "
              r"\mathrm{vraie}}{\mathrm{vraie}} \cdot 100$      $[\%]$",
     {"size": 18}),
    (None, None),
    (None, r"tout résultat s'écrit avec son unité entre crochets : "
           r"$4{,}00\ [\mathrm{V}]$,  $50{,}0\ [\mathrm{mA}]$,  "
           r"$3{,}33 \cdot 10^{6}\ [\Omega]$",
     {"size": 15, "color": GREY}),
], interligne=0.52, x_eq=0.135)

print("équations 500 refaites : ok")
