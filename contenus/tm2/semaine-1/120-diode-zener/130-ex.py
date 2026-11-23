# -*- coding: utf-8 -*-
"""130 EX Diode et Zener (+ corrigé 130 EX C) · TM2 – El Dim 4 · semaine 1, ligne 11 du plan.
Objectifs LZ_5627 (diode) et LZ_5628 (Zener et LED). Fil rouge : l'extension de l'équipement de test de la ligne de production.
Niveau voulu par Gaël (11/23/2026) : expliquer (C2) ; calculs limités à r_Z et P_Z (et une soustraction de tensions).
Valeurs lues sur les courbes de figures.py, recalculées par verif.py. Pas de référence Floyd ni nextecmedia."""
from moteur.fiche import NAVY, TW
from moteur.nombres import ing_eq

TITLE = "Diode et Zener"
S = CTX = None                        # fixés par produire(ctx)


def build(corr, out):
    F = S.module("figures")
    x = CTX.doc(corr, out, TITLE, "Corrigé" if corr else "Exercices",
                "130 EX Diode et Zener – " + ("Corrigé" if corr else "Exercices") + " – El Dim 4", f"{S.matiere} – {S.classe} – {S.annee}")
    LZ = lambda c: (c, S.lz_link(c))
    x.head(TITLE,
           [(f"Fiche d'exercices · {S.matiere} · Classe {S.classe} · {S.annee}", None), ("\n", None),
            ("Champ ", None), (S.champ, S.fm(S.futuremem_champ)),
            (" · Objectifs ", None), LZ("LZ_5627"), (", ", None), LZ("LZ_5628")],
           ["Déroulement (enseignant·e) : environ 50 min, seul·e ou en binôme, après la présentation 120, puis correction en plénière.",
            "Temps indicatifs : N°1 8 min, N°2 8 min, N°3 8 min, N°4 10 min, N°5 6 min, N°6 10 min.",
            "Correction : exiger la justification (niveau C2 : expliquer) et, pour les calculs, formule, application numérique, résultat, contrôle."],
           ["**Consignes :** justifie chaque réponse en une phrase. Pour un calcul : formule, application numérique, résultat, contrôle."],
           [("Présentation : ", [(S.fichier("120"), S.teams_url("120")), (" (diapositives 3 à 16)", None)])])
    x.CTX("tu prépares l'extension de l'équipement de test de la ligne : protection de l'alimentation 24 V, entrées limitées à 5,1 V, voyants. "
          "L'ingénieure de développement vérifie tes choix avant le prototype.")

    # ---------------------------------------------------------------- N°1 (LZ_5627, LZ_5628 : sens de conduction, LED)
    x.EX(1, "La LED s'allume-t-elle ? (≈ 8 min)", [("Présentation diapositives 4 à 6", S.teams_url("120"))])
    x.CTX("chaque circuit est alimenté par une source de 9 V. Le + est repéré en rouge, la flèche U va du + vers le −.")
    t = x.TABLE([TW / 4 - 0.01] * 4, [["", "", "", ""]], header=False, height=4.6, first_left=False)
    for j, f in enumerate(("fig_ex1_a.png", "fig_ex1_b.png", "fig_ex1_c.png", "fig_ex1_d.png")):
        x.IMG(f, 4.1, parent=t.rows[0].cells[j], after=0)
    x.Q("a)", "Pour chaque circuit, la LED s'allume-t-elle ? Justifie.")
    rows = [["Circuit", "LED", "Justification"],
            ["a)", ("R", "allumée"), ("R", "D_{1} et la LED D_{2} sont toutes deux dans le sens direct (anode vers le +)")],
            ["b)", ("R", "éteinte"), ("R", "D_{1} est dans le sens inverse : elle bloque, aucun courant")],
            ["c)", ("R", "éteinte"), ("R", "la LED D_{1} est dans le sens inverse : elle bloque")],
            ["d)", ("R", "allumée"), ("R", "la source est retournée : la LED, retournée aussi, est dans le sens direct")]]
    x.TABLE([2.0, 2.6, TW - 4.6 - 0.02], rows, height=0.6, height_eleve=0.9, size=10, gauche=(2,))
    x.Q("b)", "Dans le circuit c), quelle tension la LED reçoit-elle ? Que risque-t-elle si sa tension inverse maximale est U_{R} = 5 V ?")
    x.ANS("Aucun courant, donc 0 V sur R_{1} : la LED reçoit toute la tension, 9 V en inverse.\n"
          "9 V > 5 V : la LED peut claquer et être détruite.", 2)

    # ---------------------------------------------------------------- N°2 (LZ_5627 : caractéristique)
    u10, u30, u1 = F.u_diode(10e-3), F.u_diode(30e-3), F.u_diode(1e-3)
    x.HR(); x.EX(2, "Lire la caractéristique d'une diode (≈ 8 min)", [("Présentation diapositives 8 et 9", S.teams_url("120"))])
    x.CTX("caractéristique directe d'une diode au silicium de l'équipement, relevée en laboratoire.")
    x.IMG("fig_carac_directe_ex.png", 8.6, keep=True)
    x.Q("a)", "À partir de quelle tension le courant dépasse-t-il 1 mA ?")
    x.ANS("Environ 0,6 V (lecture : un peu moins de 0,6 V).", 1)
    x.Q("b)", "Que vaut U_{F} pour I_{F} = 10 mA ? Et pour I_{F} = 30 mA ?")
    x.ANS("10 mA : environ 0,7 V. 30 mA : environ 0,8 V.", 1)
    x.Q("c)", "Le courant triple. Que fait la tension ? Quel modèle simple de la diode peux-tu en tirer ?")
    x.ANS("Elle ne monte que d'environ 0,1 V : au-dessus du seuil, la tension varie peu.\n"
          "Modèle avec seuil : U_{F} = 0,7 V dès que la diode conduit.", 2)

    # ---------------------------------------------------------------- N°3 (LZ_5627 : valeurs limites)
    i_carte, u_alim, uf_max = 0.6, 24.0, 1.1
    x.HR(); x.EX(3, "Lire une fiche technique (≈ 8 min)", [("Présentation diapositive 10", S.teams_url("120"))])
    x.CTX("pour protéger la carte contre une alimentation branchée à l'envers, tu places une diode 1N4007 en série. "
          "La carte consomme 0,6 A sous 24 V. Extrait de la fiche technique :")
    x.TABLE([3.0, 7.0, TW - 10.0 - 0.02], [["Grandeur", "Signification", "1N4007"],
            ["U_{RRM}", "tension inverse maximale", "1000 V"], ["I_{F(AV)}", "courant direct maximal (moyen)", "1 A"],
            ["U_{F}", "tension directe", "≤ 1,1 V à 1 A"]], height=0.55, size=10, keep_after=True)
    x.Q("a)", "La 1N4007 supporte-t-elle le courant de la carte ? Et la tension si on branche à l'envers ? Justifie.")
    x.ANS("Courant : 0,6 A < 1 A, oui.\nÀ l'envers, la diode bloquée reçoit les 24 V : 24 V < 1000 V, oui, avec beaucoup de marge.", 2)
    x.Q("b)", "Dans le pire cas, quelle tension la carte reçoit-elle quand l'alimentation est bien branchée ?")
    x.ANS(f"$U_{{carte}}=U-U_{{F}}=24\\u{{ [V]}}-1,1\\u{{ [V]}}={ing_eq(u_alim - uf_max, 'V')}$\n"
          "Contrôle : 22,9 V + 1,1 V = 24 V. La carte fonctionne toujours.", 2)

    # ---------------------------------------------------------------- N°4 (LZ_5628 : Zener, résistance dynamique)
    uz5, uz25 = F.u_zener(5e-3), F.u_zener(25e-3)
    rz = (round(uz25, 1) - round(uz5, 1)) / 20e-3
    x.HR(); x.EX(4, "La caractéristique d'une Zener (≈ 10 min)", [("Présentation diapositives 11 et 12", S.teams_url("120"))])
    x.CTX("zone de claquage d'une Zener 5V1 de l'entrée de l'équipement, relevée en sens inverse (U_{Z} et I_{Z} comptés positifs).")
    x.IMG("fig_carac_zener_ex.png", 8.6, keep=True)
    x.Q("a)", "Lis U_{Z} pour I_{Z} = 5 mA, puis pour I_{Z} = 25 mA.")
    x.ANS("5 mA : U_{Z} = 5,1 V. 25 mA : U_{Z} = 5,3 V.", 1)
    x.Q("b)", "Calcule la résistance dynamique r_{Z} entre ces deux points.")
    x.ANS(f"$r_{{Z}}=\\f{{\\Delta U_{{Z}}}}{{\\Delta I_{{Z}}}}=\\f{{5,3\\u{{ [V]}}-5,1\\u{{ [V]}}}}{{25\\u{{ [mA]}}-5\\u{{ [mA]}}}}"
          f"=\\f{{0,2\\u{{ [V]}}}}{{0,02\\u{{ [A]}}}}={ing_eq(rz, 'Ω')}$\n"
          "Contrôle : 10 Ω · 20 mA = 0,2 V.", 2)
    x.Q("c)", "Le courant est multiplié par 5. De combien de pour-cent la tension change-t-elle ? Pourquoi dit-on que la Zener « tient » sa tension ?")
    x.ANS("0,2 V sur 5,1 V : environ 4 %. Le courant varie beaucoup, la tension presque pas.", 2)

    # ---------------------------------------------------------------- N°5 (LZ_5628 : puissance)
    ptot, uz = 0.5, 5.1
    izmax = ptot / uz
    pz25 = 5.3 * 25e-3
    x.HR(); x.EX(5, "La puissance de la Zener (≈ 6 min)", [("Présentation diapositive 12", S.teams_url("120"))])
    x.CTX("la Zener est une BZX55C5V1 : U_{Z} = 5,1 V, P_{tot} = 500 mW.")
    x.Q("a)", "Calcule le courant maximal I_{Zmax}.")
    x.ANS(f"$I_{{Zmax}}=\\f{{P_{{tot}}}}{{U_{{Z}}}}=\\f{{500\\u{{ [mW]}}}}{{5,1\\u{{ [V]}}}}={ing_eq(izmax, 'A')}$\n"
          "Contrôle : 5,1 V · 98 mA ≈ 500 mW.", 2)
    x.Q("b)", "En service, I_{Z} = 25 mA et U_{Z} = 5,3 V. Calcule P_{Z}. La Zener est-elle en sécurité ?")
    x.ANS(f"$P_{{Z}}=U_{{Z}}\\cdot I_{{Z}}=5,3\\u{{ [V]}}\\cdot 25\\u{{ [mA]}}={ing_eq(pz25, 'W')}$\n"
          "132,5 mW < 500 mW : oui, avec de la marge. Contrôle : 5 V · 25 mA = 125 mW, même ordre de grandeur.", 2)

    # ---------------------------------------------------------------- N°6 (LZ_5628 : applications Zener et LED)
    x.HR(); x.EX(6, "L'équipement de test (≈ 10 min)", [("Présentation diapositives 13 à 15", S.teams_url("120"))])
    x.CTX("un capteur de la ligne envoie 0 à 24 V. L'entrée du contrôleur accepte 5 V au plus. Le voyant « en marche » est une LED rouge.")
    t = x.TABLE([TW / 2 - 0.01] * 2, [["", ""]], header=False, height=3.9, first_left=False)
    x.IMG("fig_zener_entree.png", 5.9, parent=t.rows[0].cells[0], after=0)
    x.IMG("fig_led_voyant.png", 3.8, parent=t.rows[0].cells[1], after=0)
    x.Q("a)", "Le capteur envoie U_{e} = 24 V. Que vaut U_{s} ? Quelle tension R_{1} prend-elle ?")
    x.ANS("La Zener conduit : U_{s} ≈ 5,1 V. R_{1} prend le reste : 24 V − 5,1 V = 18,9 V.", 2)
    x.Q("b)", "Le capteur envoie U_{e} = 3 V. Que vaut U_{s} ? Justifie.")
    x.ANS("3 V < 5,1 V : la Zener est bloquée, aucun courant ne passe, R_{1} ne prend aucune tension. U_{s} = U_{e} = 3 V.", 2)
    x.Q("c)", "Pour le voyant, pourquoi la résistance R_{1} est-elle indispensable ? Que se passerait-il si on retournait la LED ?")
    x.ANS("Sans R_{1}, la LED serait reliée directement au 24 V : le courant monterait très haut et la LED serait détruite.\n"
          "Retournée, elle bloque et reçoit 24 V en inverse, bien plus que ses 5 V : elle peut claquer.", 3)

    # ---------------------------------------------------------------- auto-évaluation (fiche élève seulement, REGLES 4)
    if not corr:
        x.P("**Auto-évaluation**", keep=True, after=1, before=10, color=NAVY)
        x.P("Après la correction : ✓ je sais seul·e · ~ avec une aide · ✗ à revoir (reprends la diapositive indiquée).", keep=True, size=10)
        x.TABLE([TW / 6 - 0.01] * 6, [["Sens de conduction (N°1, diapos 4-6)", "Caractéristique (N°2, diapos 8-9)", "Fiche technique (N°3, diapo 10)",
                                       "Zener : r_{Z} (N°4, diapo 12)", "Zener : P_{Z} (N°5, diapo 12)", "Applications (N°6, diapos 13-15)"],
                                      ["", "", "", "", "", ""]], height=0.75, size=9, first_left=False)
    x.finish()


def produire(ctx):
    global S, CTX
    S, CTX = ctx.S, ctx
    build(False, ctx.sortie_de("130"))
    build(True, ctx.sortie_de("130C"))
