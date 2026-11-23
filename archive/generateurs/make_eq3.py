# -*- coding: utf-8 -*-
"""Chapitre 140 — blocs d'équations des diapositives (typographie mathématique)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eqimg import bloc, NAVY, BLUE, RED, GREY

A = "algébrique"
N = "numérique"
I = "ingénieur"
R_ = {"color": RED}
B_ = {"color": BLUE}


def T3(nom, alg, num, ing):
    return [(A, "$" + alg + "$"), (N, "$" + num + "$"), (I, "$" + ing + "$", R_)]


# ------------------------------------------------------------------ rappels
bloc("fig/eq_05_rappel.png", [
    ("en série", r"$R = R_1 + R_2 + \dots$"),
    ("en parallèle", r"$\frac{1}{R} = \frac{1}{R_1} + \frac{1}{R_2} + \dots$"),
    ("deux seulement", r"$R = \frac{R_1 \cdot R_2}{R_1 + R_2}$"),
    ("n égales", r"$R = \frac{R_1}{n}$", B_),
], interligne=0.62, taille=17, x_eq=0.16)

bloc("fig/eq_06_kirchhoff.png", [
    ("loi des nœuds", r"$\sum I_{\mathrm{entrants}} = \sum I_{\mathrm{sortants}}"
                      r"\qquad\rightarrow\qquad I_1 = I_2 + I_3$"),
    ("loi des mailles", r"$\sum U_{\mathrm{r\acute{e}cepteurs}} = U"
                        r"\qquad\rightarrow\qquad U = U_1 + U_2$"),
], interligne=0.50, taille=16, x_eq=0.135, couleur=BLUE)

bloc("fig/eq_07_puissance.png", [
    (None, r"$P = U \cdot I = R \cdot I^{2} = \frac{U^{2}}{R}$", {"color": BLUE,
                                                                 "size": 26}),
], interligne=0.95, largeur=5.0)

bloc("fig/eq_16_regles.png", [
    ("branche série", r"$I$ identique  $\rightarrow$  $U = R \cdot I$"),
    ("groupe parallèle", r"$U$ identique  $\rightarrow$  $I = \frac{U}{R}$"),
], interligne=0.56, taille=17, x_eq=0.155)

bloc("fig/eq_27_ecart.png", [
    (None, r"$\mathrm{\acute{e}cart} = \frac{\mathrm{mesure} - \mathrm{calcul}}{\mathrm{calcul}} \cdot 100\ \%$",
     {"color": NAVY, "size": 22}),
], interligne=0.95, largeur=6.0)

# ------------------------------------------------------------------ exemple A
bloc("fig/eq_A1.png",
     T3("R23", r"R_{23} = \frac{R_2 \cdot R_3}{R_2 + R_3}",
        r"R_{23} = \frac{0{,}2 \cdot 10^{3} \cdot 0{,}3 \cdot 10^{3}}"
        r"{0{,}2 \cdot 10^{3} + 0{,}3 \cdot 10^{3}} = "
        r"\frac{0{,}06 \cdot 10^{6}}{0{,}5 \cdot 10^{3}} = 0{,}12 \cdot 10^{3}\ \Omega",
        r"R_{23} = 120\ \Omega"),
     interligne=0.50, taille=15)

bloc("fig/eq_A2.png",
     T3("", r"R_{tot} = R_1 + R_{23}",
        r"R_{tot} = 0{,}12 \cdot 10^{3} + 0{,}12 \cdot 10^{3} = 0{,}24 \cdot 10^{3}\ \Omega",
        r"R_{tot} = 240\ \Omega")
     + [(None, None)]
     + T3("", r"I_1 = \frac{U}{R_{tot}}",
          r"I_1 = \frac{12}{0{,}24 \cdot 10^{3}} = 50 \cdot 10^{-3}\ \mathrm{A}",
          r"I_1 = 50\ \mathrm{mA}"),
     interligne=0.47, taille=15)

bloc("fig/eq_A3.png",
     T3("", r"U_1 = R_1 \cdot I_1",
        r"U_1 = 0{,}12 \cdot 10^{3} \cdot 50 \cdot 10^{-3} = 6\ \mathrm{V}", r"U_1 = 6\ \mathrm{V}")
     + [(None, None)]
     + T3("", r"U_{23} = U - U_1", r"U_{23} = 12 - 6 = 6\ \mathrm{V}", r"U_{23} = 6\ \mathrm{V}"),
     interligne=0.47, taille=15)

bloc("fig/eq_A4.png",
     T3("", r"I_2 = \frac{U_{23}}{R_2}",
        r"I_2 = \frac{6}{0{,}2 \cdot 10^{3}} = 30 \cdot 10^{-3}\ \mathrm{A}", r"I_2 = 30\ \mathrm{mA}")
     + T3("", r"I_3 = \frac{U_{23}}{R_3}",
          r"I_3 = \frac{6}{0{,}3 \cdot 10^{3}} = 20 \cdot 10^{-3}\ \mathrm{A}", r"I_3 = 20\ \mathrm{mA}")
     + [("contrôle",
         r"$I_2 + I_3 = 30 \cdot 10^{-3} + 20 \cdot 10^{-3} = 50 \cdot 10^{-3}\ \mathrm{A} "
         r"= I_1$  (OK)", B_)],
     interligne=0.42, taille=14)

# ------------------------------------------------------------------ exemple B
bloc("fig/eq_B1.png",
     T3("", r"R_{12} = R_1 + R_2",
        r"R_{12} = 0{,}1 \cdot 10^{3} + 0{,}2 \cdot 10^{3} = 0{,}3 \cdot 10^{3}\ \Omega",
        r"R_{12} = 300\ \Omega")
     + [(None, None)]
     + T3("", r"R_{tot} = \frac{R_{12} \cdot R_3}{R_{12} + R_3}",
          r"R_{tot} = \frac{0{,}3 \cdot 10^{3} \cdot 0{,}6 \cdot 10^{3}}"
          r"{0{,}9 \cdot 10^{3}} = \frac{0{,}18 \cdot 10^{6}}{0{,}9 \cdot 10^{3}} "
          r"= 0{,}2 \cdot 10^{3}\ \Omega",
          r"R_{tot} = 200\ \Omega"),
     interligne=0.47, taille=15)

bloc("fig/eq_B2.png",
     T3("", r"I_1 = \frac{U}{R_{tot}}",
        r"I_1 = \frac{12}{0{,}2 \cdot 10^{3}} = 60 \cdot 10^{-3}\ \mathrm{A}", r"I_1 = 60\ \mathrm{mA}")
     + T3("", r"I_2 = \frac{U}{R_{12}}",
          r"I_2 = \frac{12}{0{,}3 \cdot 10^{3}} = 40 \cdot 10^{-3}\ \mathrm{A}", r"I_2 = 40\ \mathrm{mA}")
     + T3("", r"I_3 = \frac{U}{R_3}",
          r"I_3 = \frac{12}{0{,}6 \cdot 10^{3}} = 20 \cdot 10^{-3}\ \mathrm{A}", r"I_3 = 20\ \mathrm{mA}"),
     interligne=0.42, taille=14)

bloc("fig/eq_B3.png",
     T3("", r"U_1 = R_1 \cdot I_2",
        r"U_1 = 0{,}1 \cdot 10^{3} \cdot 40 \cdot 10^{-3} = 4\ \mathrm{V}", r"U_1 = 4\ \mathrm{V}")
     + T3("", r"U_2 = R_2 \cdot I_2",
          r"U_2 = 0{,}2 \cdot 10^{3} \cdot 40 \cdot 10^{-3} = 8\ \mathrm{V}", r"U_2 = 8\ \mathrm{V}")
     + [(None, None),
        ("nœuds", r"$40 \cdot 10^{-3} + 20 \cdot 10^{-3} = 60 \cdot 10^{-3}\ \mathrm{A} = I_1$  (OK)",
         B_),
        ("mailles", r"$U_1 + U_2 = 4 + 8 = 12\ \mathrm{V} = U$  (OK)", B_)],
     interligne=0.42, taille=14)

# ------------------------------------------------------------------ à toi (corrigé)
bloc("fig/eq_AT.png",
     T3("", r"R_{23} = \frac{R_2 \cdot R_3}{R_2 + R_3}",
        r"R_{23} = \frac{0{,}2 \cdot 10^{3} \cdot 0{,}6 \cdot 10^{3}}"
        r"{0{,}8 \cdot 10^{3}} = 0{,}15 \cdot 10^{3}\ \Omega", r"R_{23} = 150\ \Omega")
     + T3("", r"R_{tot} = R_1 + R_{23}",
          r"R_{tot} = 0{,}1 \cdot 10^{3} + 0{,}15 \cdot 10^{3} = 0{,}25 \cdot 10^{3}\ \Omega",
          r"R_{tot} = 250\ \Omega")
     + T3("", r"I_1 = \frac{U}{R_{tot}}",
          r"I_1 = \frac{18}{0{,}25 \cdot 10^{3}} = 72 \cdot 10^{-3}\ \mathrm{A}", r"I_1 = 72\ \mathrm{mA}"),
     interligne=0.42, taille=14)

bloc("fig/eq_AT2.png",
     T3("", r"U_1 = R_1 \cdot I_1",
        r"U_1 = 0{,}1 \cdot 10^{3} \cdot 72 \cdot 10^{-3} = 7{,}2\ \mathrm{V}", r"U_1 = 7{,}2\ \mathrm{V}")
     + T3("", r"I_2 = \frac{U - U_1}{R_2}",
          r"I_2 = \frac{18 - 7{,}2}{0{,}2 \cdot 10^{3}} = \frac{10{,}8}"
          r"{0{,}2 \cdot 10^{3}} = 54 \cdot 10^{-3}\ \mathrm{A}", r"I_2 = 54\ \mathrm{mA}")
     + T3("", r"I_3 = \frac{U - U_1}{R_3}",
          r"I_3 = \frac{10{,}8}{0{,}6 \cdot 10^{3}} = 18 \cdot 10^{-3}\ \mathrm{A}",
          r"I_3 = 18\ \mathrm{mA}")
     + [("contrôle", r"$54 \cdot 10^{-3} + 18 \cdot 10^{-3} = 72 \cdot 10^{-3}\ \mathrm{A} = I_1$  (OK)",
         B_)],
     interligne=0.40, taille=13.5)

# ------------------------------------------------------------------ exemple C
bloc("fig/eq_C1.png",
     T3("", r"R_{34} = R_3 + R_4",
        r"R_{34} = 0{,}2 \cdot 10^{3} + 0{,}4 \cdot 10^{3} = 0{,}6 \cdot 10^{3}\ \Omega",
        r"R_{34} = 600\ \Omega")
     + T3("", r"R_{234} = \frac{R_2 \cdot R_{34}}{R_2 + R_{34}}",
          r"R_{234} = \frac{0{,}3 \cdot 10^{3} \cdot 0{,}6 \cdot 10^{3}}"
          r"{0{,}9 \cdot 10^{3}} = \frac{0{,}18 \cdot 10^{6}}{0{,}9 \cdot 10^{3}} = "
          r"0{,}2 \cdot 10^{3}\ \Omega", r"R_{234} = 200\ \Omega")
     + T3("", r"R_{tot} = R_1 + R_{234} + R_5",
          r"R_{tot} = 0{,}15 \cdot 10^{3} + 0{,}2 \cdot 10^{3} + 0{,}05 \cdot 10^{3} "
          r"= 0{,}4 \cdot 10^{3}\ \Omega", r"R_{tot} = 400\ \Omega"),
     interligne=0.42, taille=14)

bloc("fig/eq_C2.png",
     T3("", r"I_1 = \frac{U}{R_{tot}}",
        r"I_1 = \frac{24}{0{,}4 \cdot 10^{3}} = 60 \cdot 10^{-3}\ \mathrm{A}", r"I_1 = 60\ \mathrm{mA}")
     + T3("", r"U_1 = R_1 \cdot I_1",
          r"U_1 = 0{,}15 \cdot 10^{3} \cdot 60 \cdot 10^{-3} = 9\ \mathrm{V}", r"U_1 = 9\ \mathrm{V}")
     + T3("", r"U_2 = R_{234} \cdot I_1",
          r"U_2 = 0{,}2 \cdot 10^{3} \cdot 60 \cdot 10^{-3} = 12\ \mathrm{V}", r"U_2 = 12\ \mathrm{V}")
     + T3("", r"U_5 = R_5 \cdot I_1",
          r"U_5 = 0{,}05 \cdot 10^{3} \cdot 60 \cdot 10^{-3} = 3\ \mathrm{V}", r"U_5 = 3\ \mathrm{V}"),
     interligne=0.38, taille=13)

bloc("fig/eq_C3.png",
     T3("", r"I_2 = \frac{U_2}{R_2}",
        r"I_2 = \frac{12}{0{,}3 \cdot 10^{3}} = 40 \cdot 10^{-3}\ \mathrm{A}", r"I_2 = 40\ \mathrm{mA}")
     + T3("", r"I_3 = \frac{U_2}{R_{34}}",
          r"I_3 = \frac{12}{0{,}6 \cdot 10^{3}} = 20 \cdot 10^{-3}\ \mathrm{A}", r"I_3 = 20\ \mathrm{mA}")
     + T3("", r"U_3 = R_3 \cdot I_3",
          r"U_3 = 0{,}2 \cdot 10^{3} \cdot 20 \cdot 10^{-3} = 4\ \mathrm{V}", r"U_3 = 4\ \mathrm{V}")
     + T3("", r"U_4 = R_4 \cdot I_3",
          r"U_4 = 0{,}4 \cdot 10^{3} \cdot 20 \cdot 10^{-3} = 8\ \mathrm{V}", r"U_4 = 8\ \mathrm{V}"),
     interligne=0.38, taille=13)

bloc("fig/eq_C4.png", [
    ("puissance", r"$P_1 = U_1 \cdot I_1 = 9 \cdot 60 \cdot 10^{-3} = "
                  r"540 \cdot 10^{-3}\ \mathrm{W} = 540\ \mathrm{mW}$"),
    ("", r"$P_2 = 12 \cdot 40 \cdot 10^{-3} = 480\ \mathrm{mW} \qquad "
         r"P_3 = 4 \cdot 20 \cdot 10^{-3} = 80\ \mathrm{mW}$"),
    ("", r"$P_4 = 8 \cdot 20 \cdot 10^{-3} = 160\ \mathrm{mW} \qquad "
         r"P_5 = 3 \cdot 60 \cdot 10^{-3} = 180\ \mathrm{mW}$"),
    (None, None),
    ("contrôle", r"$\sum P = 1440\ \mathrm{mW} = U \cdot I_1 = 24 \cdot 60 \cdot 10^{-3} "
                 r"= 1{,}44\ \mathrm{W}$  (OK)", B_),
], interligne=0.44, taille=14)

bloc("fig/eq_30_synthese.png", [
    ("série", r"$R_{tot} = R_1 + R_2 + \dots$"),
    ("parallèle", r"$R_{tot} = \frac{R_1 \cdot R_2}{R_1 + R_2}$"),
    ("loi d'Ohm", r"$U = R \cdot I \qquad I = \frac{U}{R} \qquad R = \frac{U}{I}$"),
    ("puissance", r"$P = U \cdot I = R \cdot I^{2} = \frac{U^{2}}{R}$"),
], interligne=0.60, taille=16, x_eq=0.125, couleur=BLUE)

print("blocs d'équations : ok")
