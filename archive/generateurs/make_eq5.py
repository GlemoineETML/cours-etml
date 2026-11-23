# -*- coding: utf-8 -*-
"""Chapitre 500 — blocs d'équations des diapositives, en typographie mathématique."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eqimg import bloc, NAVY, BLUE, RED, GREY

A, N, I = "algébrique", "numérique", "ingénieur"
R_ = {"color": RED}


def T3(alg, num, ing):
    """Les trois temps imposés : algébrique, puissances de dix, ingénieur."""
    return [(A, "$" + alg + "$"), (N, "$" + num + "$"), (I, "$" + ing + "$", R_)]


# ------------------------------------------------------- 05 résistances internes
bloc("fig/eq_05_internes.png", [
    ("voltmètre", r"$R_V \to \infty$   idéal          $R_V$  finie   en réalité",
     {"size": 19}),
    ("ampèremètre", r"$R_A \to 0$   idéal          $R_A$  non nulle   en réalité",
     {"size": 19}),
    (None, None),
    (None, r"aucun appareil n'est idéal : dès qu'il est branché, il fait partie "
           r"du circuit", {"size": 16, "color": BLUE}),
], interligne=0.56, x_eq=0.155)

# ------------------------------------------------------- 07 sensibilité
bloc("fig/eq_07_sensibilite.png", [
    (None, r"$R_V = S \cdot U_{calibre}$", {"size": 21}),
    (None, r"$S$ : sensibilité du voltmètre analogique, en $\mathrm{\Omega/V}$, "
           r"inscrite sur le cadran", {"size": 15, "color": GREY}),
    (None, None),
    (A, r"$R_V = S \cdot U_{calibre}$"),
    (N, r"$R_V = 20 \cdot 10^{3} \cdot 10$"),
    (I, r"$R_V = 200 \cdot 10^{3}\ \Omega = 200\ \mathrm{k\Omega}$", R_),
], interligne=0.46)

# ------------------------------------------------------- 09 effet de charge
bloc("fig/eq_09_charge.png", [
    ("① le groupe mesuré", r"$R_{2V} = \frac{R_2 \cdot R_V}{R_2 + R_V}$",
     {"size": 19}),
    ("② le diviseur réel", r"$U_{mes} = U \cdot \frac{R_{2V}}{R_1 + R_{2V}}$",
     {"size": 19}),
    (None, None),
    (None, r"le voltmètre se met en PARALLÈLE : c'est la réduction du chapitre 140",
     {"size": 16, "color": BLUE}),
], interligne=0.62, x_eq=0.205)

# ------------------------------------------------------- 10 exemple analogique
bloc("fig/eq_10_ex_ana.png", [
    (A, r"$R_{2V} = \frac{R_2 \cdot R_V}{R_2 + R_V}$"),
    (N, r"$R_{2V} = \frac{100 \cdot 10^{3} \cdot 200 \cdot 10^{3}}"
        r"{300 \cdot 10^{3}} = 66{,}7 \cdot 10^{3}\ \Omega$"),
    (A, r"$U_{mes} = U \cdot \frac{R_{2V}}{R_1 + R_{2V}}$"),
    (N, r"$U_{mes} = 10 \cdot \frac{66{,}7 \cdot 10^{3}}{166{,}7 \cdot 10^{3}}$"),
    (I, r"$U_{mes} = 4{,}00\ \mathrm{V}$   au lieu de   $5{,}00\ \mathrm{V}$", R_),
], interligne=0.58, x_eq=0.135)

# ------------------------------------------------------- 11 exemple numérique
bloc("fig/eq_11_ex_num.png", [
    (N, r"$R_{2V} = \frac{100 \cdot 10^{3} \cdot 10 \cdot 10^{6}}"
        r"{10{,}1 \cdot 10^{6}} = 99{,}0 \cdot 10^{3}\ \Omega$"),
    (N, r"$U_{mes} = 10 \cdot \frac{99{,}0 \cdot 10^{3}}{199{,}0 \cdot 10^{3}}$"),
    (I, r"$U_{mes} = 4{,}975\ \mathrm{V}$   au lieu de   $5{,}00\ \mathrm{V}$", R_),
], interligne=0.58, x_eq=0.135)

# ------------------------------------------------------- 12 écart et règle
bloc("fig/eq_12_ecart.png", [
    (None, r"$\mathrm{\acute{e}cart} = \frac{\mathrm{mesure} - \mathrm{valeur\ vraie}}"
           r"{\mathrm{valeur\ vraie}} \cdot 100\ \%$", {"size": 19}),
    (None, None),
    ("analogique", r"$\frac{4{,}00 - 5{,}00}{5{,}00} \cdot 100 = -20\ \%$",
     {"size": 18, "color": RED}),
    ("numérique", r"$\frac{4{,}975 - 5{,}00}{5{,}00} \cdot 100 = -0{,}5\ \%$",
     {"size": 18, "color": RED}),
], interligne=0.64, x_eq=0.145)

# ------------------------------------------------------- 13 règle du voltmètre
bloc("fig/eq_13_regle_v.png", [
    (None, r"$R_V \geq 100 \cdot R$", {"size": 24}),
    (None, r"$R$ : la résistance aux bornes de laquelle on mesure",
     {"size": 16, "color": GREY}),
    (None, None),
    (None, r"alors l'erreur due au voltmètre reste sous $1\ \%$",
     {"size": 17, "color": BLUE}),
], interligne=0.58)

# ------------------------------------------------------- 16 ampèremètre
bloc("fig/eq_16_amp.png", [
    ("courant mesuré", r"$I_{mes} = \frac{U}{R + R_A}$", {"size": 19}),
    ("chute de tension", r"$U_A = R_A \cdot I_{mes}$", {"size": 19}),
    (None, None),
    (None, r"l'ampèremètre se met en SÉRIE : sa résistance s'ajoute à celle "
           r"du circuit", {"size": 16, "color": BLUE}),
], interligne=0.60, x_eq=0.185)

# ------------------------------------------------------- 17 exemple ampèremètre
bloc("fig/eq_17_ex_amp.png", [
    (A, r"$I_{vrai} = \frac{U}{R}$          $I_{mes} = \frac{U}{R + R_A}$"),
    (N, r"$I_{vrai} = \frac{10}{180} = 55{,}6 \cdot 10^{-3}\ \mathrm{A}$      "
        r"$I_{mes} = \frac{10}{200} = 50 \cdot 10^{-3}\ \mathrm{A}$"),
    (I, r"$I_{vrai} = 55{,}6\ \mathrm{mA}$          "
        r"$I_{mes} = 50{,}0\ \mathrm{mA}$   soit   $-10\ \%$", R_),
    (None, None),
    (A, r"$U_A = R_A \cdot I_{mes} = 20 \cdot 50 \cdot 10^{-3} = 1{,}00\ \mathrm{V}$"),
], interligne=0.56, x_eq=0.135)

# ------------------------------------------------------- 18 règle de l'ampèremètre
bloc("fig/eq_18_regle_a.png", [
    (None, r"$R_A \leq \frac{R}{100}$", {"size": 24}),
    (None, None),
    (None, r"sinon l'ampèremètre freine le courant qu'il est censé mesurer",
     {"size": 17, "color": BLUE}),
], interligne=0.62)

# ------------------------------------------------------- 20 ohmmètre
bloc("fig/eq_20_ohm.png", [
    (None, r"$R_{lue} = \frac{R \cdot R_{reste}}{R + R_{reste}}$", {"size": 21}),
    (None, None),
    (N, r"$R_{lue} = \frac{12 \cdot 10^{3} \cdot 4 \cdot 10^{3}}{16 \cdot 10^{3}}$"),
    (I, r"$R_{lue} = 3\ \mathrm{k\Omega}$   au lieu de   $12\ \mathrm{k\Omega}$", R_),
], interligne=0.58, x_eq=0.135)

# ------------------------------------------------------- 24 précision analogique
bloc("fig/eq_24_prec_ana.png", [
    (None, r"$\Delta U = \frac{\mathrm{classe}}{100} \cdot U_{calibre}$", {"size": 21}),
    (None, r"l'incertitude ne dépend PAS de la lecture, seulement du calibre",
     {"size": 16, "color": BLUE}),
    (None, None),
    ("calibre 10 V", r"$\Delta U = 0{,}015 \cdot 10 = \pm 0{,}15\ \mathrm{V}$ "
                     r"  sur une lecture de $2\ \mathrm{V}$ :  $\pm 7{,}5\ \%$",
     {"size": 17, "color": RED}),
    ("calibre 3 V", r"$\Delta U = 0{,}015 \cdot 3 = \pm 0{,}045\ \mathrm{V}$ "
                    r"  sur la même lecture :  $\pm 2{,}25\ \%$",
     {"size": 17, "color": RED}),
], interligne=0.58, x_eq=0.135)

# ------------------------------------------------------- 25 précision numérique
bloc("fig/eq_25_prec_num.png", [
    (None, r"$\Delta U = \frac{p}{100} \cdot U_{lu} + n \cdot \mathrm{digit}$",
     {"size": 21}),
    (None, r"exemple d'une fiche technique : $\pm(0{,}5\ \%\ \mathrm{de\ la\ lecture} "
           r"+ 2\ \mathrm{digits})$", {"size": 15, "color": GREY}),
    (None, None),
    (N, r"$\Delta U = 0{,}005 \cdot 4{,}00 + 2 \cdot 0{,}01 = 0{,}020 + 0{,}020$"),
    (I, r"$\Delta U = \pm 0{,}040\ \mathrm{V}$   soit   $\pm 1{,}0\ \%$   "
        r"de la lecture", R_),
], interligne=0.56, x_eq=0.135)

# ------------------------------------------------------- 28 formulaire
bloc("fig/eq_28_formulaire.png", [
    (None, r"$R_V = S \cdot U_{calibre}$      "
           r"$R_{2V} = \frac{R_2 \cdot R_V}{R_2 + R_V}$      "
           r"$U_{mes} = U \cdot \frac{R_{2V}}{R_1 + R_{2V}}$", {"size": 19}),
    (None, None),
    (None, r"$I_{mes} = \frac{U}{R + R_A}$      "
           r"$U_A = R_A \cdot I_{mes}$      "
           r"$R_{lue} = \frac{R \cdot R_{reste}}{R + R_{reste}}$", {"size": 19}),
    (None, None),
    (None, r"$\mathrm{\acute{e}cart} = \frac{\mathrm{mesure} - \mathrm{vraie}}"
           r"{\mathrm{vraie}} \cdot 100\ \%$      "
           r"$R_V \geq 100\,R$      $R_A \leq \frac{R}{100}$", {"size": 19}),
], interligne=0.64)

print("équations 500 : ok")
