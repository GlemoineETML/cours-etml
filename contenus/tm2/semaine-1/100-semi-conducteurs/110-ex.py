# -*- coding: utf-8 -*-
"""110 EX Semi-conducteurs (+ corrigé 110 EX C) · TM2 – El Dim 4 · semaine 1, ligne 10 du plan.
Objectifs LZ_1879, LZ_4066, LZ_4067. Fil rouge : l'extension de l'équipement de test de la ligne de production.
Niveau voulu par Gaël (11/23/2026) : comprendre et savoir que ça existe ; un seul petit calcul (N°3 c).
Valeurs recalculées par verif.py. Pas de référence Floyd ni nextecmedia pour cette séance."""
from moteur.fiche import NAVY, TW
from moteur.nombres import ing_eq

TITLE = "Semi-conducteurs"
S = CTX = None                        # fixés par produire(ctx)


def build(corr, out):
    x = CTX.doc(corr, out, TITLE, "Corrigé" if corr else "Exercices",
                "110 EX Semi-conducteurs – " + ("Corrigé" if corr else "Exercices") + " – El Dim 4", f"{S.matiere} – {S.classe} – {S.annee}")
    LZ = lambda c: (c, S.lz_link(c))
    x.head(TITLE,
           [(f"Fiche d'exercices · {S.matiere} · Classe {S.classe} · {S.annee}", None), ("\n", None),
            ("Champ ", None), (S.champ, S.fm(S.futuremem_champ)),
            (" · Objectifs ", None), LZ("LZ_1879"), (", ", None), LZ("LZ_4066"), (", ", None), LZ("LZ_4067")],
           ["Déroulement (enseignant·e) : environ 50 min, seul·e ou en binôme, après la présentation 100, puis correction en plénière.",
            "Temps indicatifs : N°1 12 min, N°2 10 min, N°3 12 min, N°4 8 min, N°5 10 min.",
            "Correction : exiger une justification d'une phrase (niveau C4 du N°1). Ramasser l'auto-évaluation."],
           ["**Consignes :** réponds en une ou deux phrases et justifie chaque réponse."],
           [("Présentation : ", [(S.fichier("100"), S.teams_url("100")), (" (diapositives 3 à 9)", None)])])
    x.CTX("tu prépares l'extension de l'équipement de test de la ligne (voyants, entrées protégées, sorties à transistors). "
          "L'ingénieure de développement te demande de vérifier tes bases sur les matériaux de ces composants.")

    # ---------------------------------------------------------------- N°1 (LZ_1879, C4)
    x.EX(1, "Classer des matériaux (≈ 12 min)", [("Présentation diapositives 3 à 5", S.teams_url("100"))])
    x.Q("a)", "Classe chaque matériau : conducteur, semi-conducteur ou isolant. Justifie en quelques mots.")
    rows = [["Matériau", "Utilisation", "Famille", "Justification"],
            ["Cuivre", "pistes et fils", ("R", "conducteur"), ("R", "beaucoup d'électrons libres, ρ très faible")],
            ["Silicium", "diodes, transistors", ("R", "semi-conducteur"), ("R", "4 électrons de valence, conduction réglable")],
            ["Porcelaine", "isolateurs", ("R", "isolant"), ("R", "aucun électron libre, ρ très grande")],
            ["Germanium", "anciennes diodes", ("R", "semi-conducteur"), ("R", "4 électrons de valence, comme le silicium")]]
    x.TABLE([2.6, 3.3, 3.7, TW - 9.6 - 0.02], rows, height=0.7, height_eleve=0.9, size=10, gauche=(3,))
    x.Q("b)", "Tu chauffes deux échantillons inconnus de 20 °C à 40 °C. La résistance de X passe de 10 Ω à 10,8 Ω, "
              "celle de Y de 1,2 kΩ à 300 Ω. À quelle famille appartient chacun ? Pourquoi ?")
    x.ANS("X est un conducteur : sa résistance augmente un peu quand il chauffe.\n"
          "Y est un semi-conducteur : sa résistance diminue fortement, car la chaleur libère des porteurs.", 3)

    # ---------------------------------------------------------------- N°2 (LZ_4067 : monocristal, conduction intrinsèque)
    x.HR(); x.EX(2, "Le cristal de silicium (≈ 10 min)", [("Présentation diapositive 6", S.teams_url("100"))])
    x.Q("a)", "Explique en une phrase ce qu'est un monocristal de silicium.")
    x.ANS("Un morceau de silicium dont les atomes sont rangés régulièrement dans tout le volume.", 2)
    x.Q("b)", "Coche vrai ou faux. Corrige les affirmations fausses.")
    rows = [["Affirmation", "Vrai / faux", "Correction"],
            ["Chaque atome de silicium est lié à 4 voisins.", ("R", "vrai"), ("R", "")],
            ["La chaleur rompt des liaisons : il apparaît un électron libre et un trou.", ("R", "vrai"), ("R", "")],
            ["Un trou est une particule chargée positivement.", ("R", "faux"), ("R", "c'est une place vide qui se comporte comme une charge +")],
            ["Le silicium pur conduit très bien.", ("R", "faux"), ("R", "il conduit très peu : peu de paires électron-trou")]]
    x.TABLE([7.4, 2.2, TW - 9.6 - 0.02], rows, height=0.8, height_eleve=0.9, size=10, bold_first=False, gauche=(2,))

    # ---------------------------------------------------------------- N°3 (LZ_4066 : chaleur)
    d_t = 40
    uf = 0.65 - 0.002 * d_t
    x.HR(); x.EX(3, "L'effet de la chaleur (≈ 12 min)", [("Présentation diapositive 7", S.teams_url("100"))])
    x.CTX("en été, l'armoire de l'équipement de test passe de 20 °C à 60 °C.")
    x.Q("a)", "La bobine d'un relais est en cuivre. Sa résistance monte-t-elle ou baisse-t-elle ? Beaucoup ou un peu ?")
    x.ANS("Elle monte un peu (environ 16 % pour 40 °C) : dans un métal, les atomes qui vibrent freinent les électrons.", 2)
    x.Q("b)", "Dans le silicium, le nombre de porteurs libres double environ tous les 10 °C. Combien de fois plus de porteurs à 60 °C qu'à 20 °C ? "
              "Que devient la résistance ?")
    x.ANS("40 °C = 4 fois 10 °C : 2 · 2 · 2 · 2 = 16 fois plus de porteurs. La résistance diminue fortement.", 2)
    x.Q("c)", "La diode d'entrée (silicium) a une tension directe U_{F} = 0,65 V à 20 °C. Elle baisse de 2 mV par °C. Que vaut U_{F} à 60 °C ?")
    x.ANS(f"$U_{{F}}=0,65\\u{{ [V]}}-2\\u{{ [mV/°C]}}\\cdot 40\\u{{ [°C]}}={ing_eq(uf, 'V')}$ : à chaud, la diode conduit plus tôt.", 1)

    # ---------------------------------------------------------------- N°4 (LZ_4066 : champ électrique)
    x.HR(); x.EX(4, "Le champ électrique (≈ 8 min)", [("Présentation diapositive 8", S.teams_url("100"))])
    x.CTX("on applique une tension à un barreau de silicium : le + à gauche, le − à droite.")
    x.Q("a)", "Vers où vont les électrons libres ? Et les trous ?")
    x.ANS("Les électrons vont vers le + (à gauche), les trous vers le − (à droite).", 1)
    x.Q("b)", "On augmente beaucoup la tension sur une jonction très mince. Que se passe-t-il ? Quel composant utilise cet effet ?")
    x.ANS("Les liaisons cèdent et le courant monte d'un coup : c'est le claquage. La diode Zener l'utilise.", 2)
    x.Q("c)", "Quel transistor est commandé par un champ électrique ?")
    x.ANS("Le transistor à effet de champ (FET).", 1)

    # ---------------------------------------------------------------- N°5 (LZ_4067 : dopage)
    x.HR(); x.EX(5, "Le dopage (≈ 10 min)", [("Présentation diapositive 9", S.teams_url("100"))])
    x.Q("a)", "Complète le tableau.")
    rows = [["Atome ajouté au silicium", "Électrons de valence", "Type obtenu", "Porteurs majoritaires"],
            ["Phosphore P", ("R", "5"), ("R", "n"), ("R", "électrons")],
            ["Bore B", ("R", "3"), ("R", "p"), ("R", "trous")]]
    x.TABLE([5.2, 4.0, 3.3, TW - 12.5 - 0.02], rows, height=0.6, height_eleve=0.8, size=10)
    x.Q("b)", "Un collègue affirme : « Le silicium dopé n est chargé négativement, puisqu'il a des électrons en plus. » A-t-il raison ?")
    x.ANS("Non. Chaque atome de phosphore apporte un électron, mais aussi un proton de plus dans son noyau : le morceau reste neutre.", 2)

    # ---------------------------------------------------------------- auto-évaluation (fiche élève seulement, REGLES 4)
    if not corr:
        x.P("**Auto-évaluation**", keep=True, after=1, before=10, color=NAVY)
        x.P("Après la correction : ✓ je sais seul·e · ~ avec une aide · ✗ à revoir (reprends la diapositive indiquée).", keep=True, size=10)
        x.TABLE([TW / 5 - 0.01] * 5, [["Classer (N°1, diapos 3-5)", "Le cristal (N°2, diapo 6)", "La chaleur (N°3, diapo 7)",
                                       "Le champ (N°4, diapo 8)", "Le dopage (N°5, diapo 9)"], ["", "", "", "", ""]],
                height=0.75, size=9, first_left=False)
    x.finish()


def produire(ctx):
    global S, CTX
    S, CTX = ctx.S, ctx
    build(False, ctx.sortie_de("110"))
    build(True, ctx.sortie_de("110C"))
