# -*- coding: utf-8 -*-
"""Chapitre 300 — blocs d'équations des diapositives, en typographie mathématique."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eqimg import bloc, NAVY, BLUE, RED, GREY

A, N, I = "algébrique", "numérique", "ingénieur"
R_ = {"color": RED}
B_ = {"color": BLUE}


def T3(alg, num, ing):
    """Les trois temps imposés : forme algébrique, puissances de dix, ingénieur."""
    return [(A, "$" + alg + "$"), (N, "$" + num + "$"), (I, "$" + ing + "$", R_)]


# ------------------------------------------------------------------ 04 la charge
bloc("fig/eq_04_charge.png", [
    (None, r"$Q = I \cdot t$", {"size": 20}),
    (None, r"$[Q] = \mathrm{A} \cdot \mathrm{s} = \mathrm{C}$   (coulomb)",
     {"size": 15, "color": GREY}),
    (None, None),
    (None, r"$i = \frac{\Delta Q}{\Delta t}$", {"size": 20, "color": BLUE}),
    (None, r"le courant est le débit de charge : autant de coulombs par seconde",
     {"size": 15, "color": GREY}),
], interligne=0.52)

# ------------------------------------------------------------------ 05 exemple 1
bloc("fig/eq_05_ex1.png", T3(
    r"Q = I \cdot t",
    r"Q = 250 \cdot 10^{-3} \cdot 7{,}2 \cdot 10^{3}",
    r"Q = 1{,}8 \cdot 10^{3}\ \mathrm{C} = 1{,}8\ \mathrm{kC}"))

# ------------------------------------------------------------------ 08 champ
bloc("fig/eq_08_champ.png", [
    (None, r"$E = \frac{U}{d}$", {"size": 22}),
    (None, r"$[E] = \frac{\mathrm{V}}{\mathrm{m}}$   —   souvent en $\mathrm{V/mm}$ "
           r"ou $\mathrm{kV/mm}$", {"size": 15, "color": GREY}),
    (None, None),
    (None, r"$F = Q \cdot E$", {"size": 20, "color": BLUE}),
    (None, r"force subie par une charge $Q$ placée dans le champ",
     {"size": 15, "color": GREY}),
], interligne=0.56)

# ------------------------------------------------------------------ 09 exemple 2
bloc("fig/eq_09_ex2.png", T3(
    r"E = \frac{U}{d}",
    r"E = \frac{400}{0{,}2 \cdot 10^{-3}}",
    r"E = 2 \cdot 10^{6}\ \mathrm{V/m} = 2\ \mathrm{MV/m}"))

# ------------------------------------------------------------------ 10 capacité
bloc("fig/eq_10_condo.png", [
    (None, r"$C = \frac{Q}{U}$", {"size": 22}),
    (None, r"$[C] = \frac{\mathrm{C}}{\mathrm{V}} = \mathrm{F}$   (farad)",
     {"size": 15, "color": GREY}),
    (None, None),
    (None, r"$Q = C \cdot U$", {"size": 20, "color": BLUE}),
    (None, r"sous la même tension, un $C$ deux fois plus grand stocke deux fois "
           r"plus de charge", {"size": 15, "color": GREY}),
], interligne=0.56)

# ------------------------------------------------------------------ 11 géométrie
bloc("fig/eq_11_geometrie.png", [
    (None, r"$C = \varepsilon_0 \cdot \varepsilon_r \cdot \frac{A}{d}$", {"size": 22}),
    (None, r"$\varepsilon_0 = 8{,}85 \cdot 10^{-12}\ \mathrm{F/m}$   ·   "
           r"$\varepsilon_r$ : sans unité, $1$ pour l'air", {"size": 15, "color": GREY}),
], interligne=0.60)

# ------------------------------------------------------------------ 12 énergie
bloc("fig/eq_12_energie.png", [
    (None, r"$W = \frac{1}{2} \cdot C \cdot U^{2}$", {"size": 21}),
    (None, None),
    (A, r"$W = \frac{1}{2} \cdot C \cdot U^{2}$"),
    (N, r"$W = 0{,}5 \cdot 10 \cdot 10^{-6} \cdot (100)^{2}$"),
    (I, r"$W = 50 \cdot 10^{-3}\ \mathrm{J} = 50\ \mathrm{mJ}$", R_),
], interligne=0.46)

# ------------------------------------------------------------------ 13 groupements
bloc("fig/eq_13_groupements.png", [
    ("en parallèle", r"$C = C_1 + C_2 + C_3 + \ldots$", {"size": 19}),
    (None, None),
    ("en série", r"$\frac{1}{C} = \frac{1}{C_1} + \frac{1}{C_2} + \frac{1}{C_3} "
                 r"+ \ldots$", {"size": 19}),
    (None, None),
    ("deux seulement", r"$C = \frac{C_1 \cdot C_2}{C_1 + C_2}$", {"size": 19}),
], interligne=0.60, x_eq=0.145)

# ------------------------------------------------------------------ 16 exemple 3
bloc("fig/eq_16_ex3.png", [
    ("① série", r"$C_{12} = \frac{C_1 \cdot C_2}{C_1 + C_2} = "
                r"\frac{20 \cdot 10^{-6} \cdot 30 \cdot 10^{-6}}"
                r"{50 \cdot 10^{-6}} = 12 \cdot 10^{-6}\ \mathrm{F}$"),
    ("② parallèle", r"$C_{123} = C_{12} + C_3 = 12 \cdot 10^{-6} + 8 \cdot 10^{-6} "
                    r"= 20 \cdot 10^{-6}\ \mathrm{F}$"),
    ("③ série", r"$C_{AB} = \frac{C_4 \cdot C_{123}}{C_4 + C_{123}} = "
                r"\frac{20 \cdot 10^{-6} \cdot 20 \cdot 10^{-6}}"
                r"{40 \cdot 10^{-6}} = 10 \cdot 10^{-6}\ \mathrm{F}$"),
    ("ingénieur", r"$C_{AB} = 10\ \mathrm{\mu F}$", R_),
], interligne=0.58, x_eq=0.135)

# ------------------------------------------------------------------ 17 transitoire
bloc("fig/eq_17_transitoire.png", [
    (None, r"$i_C = C \cdot \frac{\Delta u_C}{\Delta t}$", {"size": 21}),
    (None, None),
    (None, r"la tension d'un condensateur ne peut PAS sauter — le courant, si",
     {"size": 16, "color": BLUE}),
    (None, r"régime établi : $\Delta u_C = 0$, donc $i_C = 0$ — le condensateur "
           r"se comporte comme un circuit ouvert", {"size": 15, "color": GREY}),
], interligne=0.54)

# ------------------------------------------------------------------ 18 charge
bloc("fig/eq_18_charge.png", [
    ("constante de temps", r"$\tau = R \cdot C$", {"size": 20}),
    (None, None),
    ("tension", r"$u_C(t) = E \cdot \left(1 - e^{-t/\tau}\right)$", {"size": 19}),
    ("courant", r"$i_C(t) = \frac{E}{R} \cdot e^{-t/\tau}$", {"size": 19}),
    (None, r"à $t = 0$ le condensateur est vide : toute la tension est sur $R$, "
           r"donc $I_0 = E / R$", {"size": 15, "color": GREY}),
], interligne=0.56, x_eq=0.185)

# ------------------------------------------------------------------ 21 décharge
bloc("fig/eq_21_decharge.png", [
    ("tension", r"$u_C(t) = U_0 \cdot e^{-t/\tau}$", {"size": 19}),
    ("courant", r"$i_C(t) = \frac{U_0}{R} \cdot e^{-t/\tau}$", {"size": 19}),
    (None, None),
    (None, r"même $\tau$, mais $R$ est la résistance dans laquelle le condensateur "
           r"se vide", {"size": 16, "color": BLUE}),
], interligne=0.56, x_eq=0.135)

# ------------------------------------------------------------------ 22 lecture inverse
bloc("fig/eq_22_inverse.png", [
    ("on part de", r"$i = I_0 \cdot e^{-t/\tau}$", {"size": 19}),
    ("on isole", r"$\tau = \frac{t}{\ln\left(\dfrac{I_0}{i}\right)}$", {"size": 19}),
    ("cas très fréquent", r"$i = \frac{I_0}{2}\ \Rightarrow\ \tau = "
                          r"\frac{t}{\ln 2} = \frac{t}{0{,}693}$", {"size": 19}),
    (None, None),
    (None, r"puis $C = \dfrac{\tau}{R}$", {"size": 19, "color": BLUE}),
], interligne=0.66, x_eq=0.185)

# ------------------------------------------------------------------ 23 exemple 4
bloc("fig/eq_23_ex4.png", [
    ("① le départ", r"$I_0 = \frac{U}{R} = \frac{20}{1 \cdot 10^{3}} "
                    r"= 20 \cdot 10^{-3}\ \mathrm{A}$"),
    ("② la lecture", r"$i = 10 \cdot 10^{-3}\ \mathrm{A} = \frac{I_0}{2}$ "
                     r"  à   $t = 15 \cdot 10^{-6}\ \mathrm{s}$"),
    ("③ algébrique", r"$\tau = \frac{t}{\ln 2}$        "
                     r"$C_x = \frac{\tau}{R}$"),
    ("④ numérique", r"$\tau = \frac{15 \cdot 10^{-6}}{0{,}693} "
                    r"= 21{,}6 \cdot 10^{-6}\ \mathrm{s}$      "
                    r"$C_x = \frac{21{,}6 \cdot 10^{-6}}{1 \cdot 10^{3}}$"),
    ("ingénieur", r"$\tau = 21{,}6\ \mathrm{\mu s}$        "
                  r"$C_x = 21{,}6 \cdot 10^{-9}\ \mathrm{F} \approx 22\ \mathrm{nF}$", R_),
], interligne=0.60, x_eq=0.155)

# ------------------------------------------------------------------ 25 exemple 5 a
bloc("fig/eq_25_ex5a.png", [
    ("① régime établi", r"$i_C = 0$ : le condensateur est un circuit ouvert, "
                        r"tout le courant passe dans $R_2$"),
    (A, r"$U_{C\,\mathrm{max}} = E \cdot \frac{R_2}{R_1 + R_2}$"),
    (N, r"$U_{C\,\mathrm{max}} = 20 \cdot \frac{20}{30 + 20} = 20 \cdot 0{,}4$"),
    (I, r"$U_{C\,\mathrm{max}} = 8\ \mathrm{V}$", R_),
], interligne=0.56, x_eq=0.165)

# ------------------------------------------------------------------ 26 exemple 5 b
bloc("fig/eq_26_ex5b.png", [
    ("② la décharge", r"$S$ ouvert : $R_1$ et $E$ sont hors circuit, "
                      r"$C$ se vide dans $R_2$ seul"),
    (A, r"$\tau = R_2 \cdot C$          $I_{C\,\mathrm{max}} = \frac{U_{C\,\mathrm{max}}}{R_2}$"),
    (N, r"$\tau = 20 \cdot 4 \cdot 10^{-6}$          "
        r"$I_{C\,\mathrm{max}} = \frac{8}{20}$"),
    (I, r"$\tau = 80 \cdot 10^{-6}\ \mathrm{s} = 80\ \mathrm{\mu s}$          "
        r"$I_{C\,\mathrm{max}} = 0{,}4\ \mathrm{A} = 400\ \mathrm{mA}$", R_),
    (None, r"régime terminé après $5\,\tau = 400\ \mathrm{\mu s}$",
     {"size": 15, "color": GREY}),
], interligne=0.56, x_eq=0.165)

# ------------------------------------------------------------------ 27 formulaire
bloc("fig/eq_27_formulaire.png", [
    (None, r"$Q = I \cdot t$      $Q = C \cdot U$      $E = \frac{U}{d}$      "
           r"$F = Q \cdot E$", {"size": 20}),
    (None, None),
    (None, r"$C = \varepsilon_0 \varepsilon_r \frac{A}{d}$      "
           r"$W = \frac{1}{2} C U^{2}$      "
           r"$C_{par} = C_1 + C_2$      "
           r"$\frac{1}{C_{ser}} = \frac{1}{C_1} + \frac{1}{C_2}$", {"size": 20}),
    (None, None),
    (None, r"$\tau = R \cdot C$      "
           r"$u_C = E\left(1 - e^{-t/\tau}\right)$      "
           r"$u_C = U_0 e^{-t/\tau}$      "
           r"$\tau = \frac{t}{\ln(I_0/i)}$", {"size": 20}),
], interligne=0.62)

print("équations 300 : ok")
