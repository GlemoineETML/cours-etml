// 120 Diode et diode Zener : diapositives (moteur : moteur/deck.js). TM2, semaine 1, ligne 11 du plan.
// Objectifs : LZ_5627 (C2) fonctionnement de la diode ; LZ_5628 (C2) Zener et LED (le transistor de commutation : présentation 240).
// Fil rouge : l'équipement de test de la ligne de production (situation de travail du champ LFB_El_Dim4).
// Cadrage validé par Gaël (11/23/2026) : la LED entre dans la séance ; calculs limités à r_Z et P_Z ;
// pas de calcul de résistance série (présentation 140). Pas de référence Floyd ni nextecmedia.
module.exports = function (E) {
  const { pres, DATA, NAVY, BLUE, LBLUE, TINT, K, GR, RED, F, slide, txt, card, frame, badge, img, eqImg, bullets, life,
    boxTitle, cell, H, BORDER, LZL, exoSlide, pageSlide, videoSlide, titreSlide } = E;
  const obj = (t, codes, fin) => [{ text: t + " (" }].concat(...codes.map((c, i) => i ? [{ text: ", " }, LZL(c)] : [LZL(c)]), [{ text: fin || ") ;" }]);
  const L = { align: "left", bold: true };

  // ============================== 1. TITRE · OBJECTIFS · QUESTION DE DÉPART
  titreSlide({
    titre: "La diode et\nla diode Zener",
    sousTitre: "et la LED : trois composants à jonction PN",
    objectifs: [obj("expliquer le sens de conduction d'une diode", ["LZ_5627"]),
      obj("lire la caractéristique I(U) d'une diode", ["LZ_5627"]),
      obj("expliquer la Zener et ses usages", ["LZ_5628"]),
      obj("expliquer la LED et ses limites", ["LZ_5628"], ").")],
    question: "Sur la ligne, quelqu'un branche l'alimentation 24 V de l'équipement de test à l'envers. Comment une seule diode peut-elle protéger toute la carte ?",
    indice: "Écris ton hypothèse. Réponse à la diapositive 17.",
    notes: "Durée : 3 périodes de présentation, puis la fiche 130 EX (4e période). Niveau visé (C2) : expliquer ; deux petits calculs seulement (r_Z et P_Z).\n" +
      "Objectifs FutureMEM (champ LFB_El_Dim4), cliquables : LZ_5627 diode (diapositives 3 à 10) ; LZ_5628 Zener (11 à 13) et LED (14 et 15). " +
      "Le transistor de commutation, aussi cité par LZ_5628, vient en présentation 240.\n" +
      "Les deux objectifs sont couverts en pratique (TM2-A1-S2 caractéristique de la Zener, A1-S3 diode Si, A2-S1 lampe à LED, A2-S3 Zener) : " +
      "la théorie prépare ce que l'apprenti·e va mesurer.\n" +
      "Question de départ : noter les hypothèses au tableau sans les corriger. Réponse à la diapositive 17.",
  });

  // ============================== 2. LA SITUATION · CE QUE TU SAIS DÉJÀ
  {
    const s = slide("La situation et ce que tu sais déjà",
      "Rappel de la présentation 100 : le dopage n donne des électrons libres majoritaires, le dopage p des trous majoritaires ; un champ très fort fait claquer le cristal.\n" +
      "Activation, 5 min en binôme. Réponses : 1) des électrons libres. 2) des trous. 3) le claquage : les liaisons cèdent, le courant monte d'un coup.\n" +
      "Les trois composants du jour ont tous une jonction PN : la diode, la Zener et la LED.");
    card(s, 0.5, 0.95, 4.4, 1.5);
    txt(s, "Ta mission", { x: 0.65, y: 1.02, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, "Étendre l'équipement de test de la ligne : protéger l'alimentation, limiter la tension des entrées, ajouter des voyants.", { x: 0.65, y: 1.36, w: 4.1, h: 1.0, fontSize: 12 });
    s.addTable([
      [cell("Besoin", H), cell("Composant", H)],
      [cell("alimentation branchée à l'envers", { align: "left" }), cell("diode")],
      [cell("entrée limitée à 5,1 V", { align: "left" }), cell("diode Zener")],
      [cell("voyant « en marche »", { align: "left" }), cell("LED")],
    ], { x: 0.5, y: 2.6, w: 4.4, colW: [2.75, 1.65], rowH: 0.38, border: BORDER, fontSize: 11.5 });
    frame(s, 5.1, 0.95, 4.4, 3.2);
    txt(s, "Ce que tu sais déjà (en binôme, 5 min)", { x: 5.25, y: 1.02, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    [["1", "Silicium dopé n : quels porteurs sont majoritaires ?"], ["2", "Et dans le silicium dopé p ?"],
     ["3", "Que se passe-t-il quand le champ électrique devient très fort ?"]].forEach(([n, q], i) => {
      const y = 1.45 + i * 0.85;
      badge(s, 5.25, y + 0.08, n, 0.36);
      txt(s, q, { x: 5.75, y, w: 3.6, h: 0.6, fontSize: 12.5, valign: "middle" });
    });
    life(s, 0.5, 4.35, 9.0, 1.2, ["En pratique (TM2-A1), tu relèves la caractéristique d'une diode au silicium et d'une Zener : ce cours explique ce que tu vas mesurer.",
      "Une zone p et une zone n dans le même cristal : c'est la jonction PN de toutes les diodes."], 11);
  }

  // ============================== 3. LA JONCTION PN
  {
    const s = slide("La jonction PN",
      "Une zone p et une zone n dans le même cristal. À la frontière, des électrons libres de la zone n comblent des trous de la zone p.\n" +
      "Il reste une zone vidée de porteurs libres : la zone de déplétion (ou zone de charge d'espace). Seuls restent les ions fixes du dopage : " +
      "négatifs côté p (bore qui a capté un électron), positifs côté n (phosphore qui a perdu le sien).\n" +
      "Ces ions créent une barrière : pour la franchir dans le silicium, il faut environ 0,6 à 0,7 V. Sans tension extérieure, aucun courant ne circule.");
    img(s, "fig_jonction.png", 0.5, 0.95, 5.3, 3.4);
    boxTitle(s, 6.0, 0.95, 3.5, 1.55, "Zone de déplétion", ["Plus de porteurs libres à la frontière.", "Elle se comporte comme un isolant."], 13, true);
    boxTitle(s, 6.0, 2.65, 3.5, 1.7, "Une barrière", ["Les ions fixes repoussent les porteurs.", "Silicium : il faut ≈ 0,7 V pour la franchir."], 13, false);
    life(s, 0.5, 4.55, 9.0, 1.0, ["Toutes les diodes de l'équipement de test, Zener et LED comprises, reposent sur cette jonction."], 11);
  }

  // ============================== 4. SENS DIRECT, SENS INVERSE
  {
    const s = slide("Sens direct, sens inverse",
      "Sens direct : le + sur la zone p (anode). Les porteurs sont poussés vers la frontière, la zone de déplétion devient mince : dès ≈ 0,7 V, le courant passe.\n" +
      "Sens inverse : le + sur la zone n (cathode). Les porteurs sont tirés loin de la frontière, la zone s'élargit : pas de courant, sauf un courant de fuite minuscule (nA à µA).\n" +
      "Faire le lien avec un clapet anti-retour : l'eau passe dans un sens, pas dans l'autre.");
    img(s, "fig_pol_directe.png", 0.5, 0.95, 4.35, 2.8);
    img(s, "fig_pol_inverse.png", 5.15, 0.95, 4.35, 2.8);
    card(s, 0.5, 3.75, 9.0, 0.7, NAVY);
    txt(s, [{ text: "À retenir : ", options: { bold: true, color: LBLUE } }, { text: "une diode conduit de l'anode vers la cathode, et bloque dans l'autre sens.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 3.75, w: 8.6, h: 0.7, fontSize: 13, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, ["Comme un clapet anti-retour sur une conduite d'eau : le courant passe dans un sens, jamais dans l'autre."], 11);
  }

  // ============================== 5. LA DIODE DANS UN CIRCUIT
  {
    const s = slide("La diode dans un circuit",
      "Sens direct : la diode prend environ 0,7 V, la résistance prend le reste (U_R = U − U_F). Le courant est fixé par la résistance (calcul : présentation 140).\n" +
      "Sens inverse : aucun courant, donc aucune tension sur la résistance (U_R = R · I = 0). La diode bloquée reçoit toute la tension de la source : U_D = U = 9 V.\n" +
      "Erreur fréquente : croire qu'une diode bloquée « n'a pas de tension ». C'est l'inverse : c'est elle qui prend toute la tension. D'où la valeur limite U_RRM (diapositive 10).");
    img(s, "fig_circ_directe.png", 0.5, 0.95, 2.75, 3.5);
    img(s, "fig_circ_inverse.png", 3.3, 0.95, 2.75, 3.5);
    boxTitle(s, 6.1, 0.95, 3.4, 1.6, "Sens direct", ["La diode conduit : U_{F} ≈ 0,7 V.", "La résistance prend le reste."], 13, true);
    boxTitle(s, 6.1, 2.7, 3.4, 1.7, "Sens inverse", ["I = 0, donc U_{R} = 0.", "La diode reçoit toute la tension : U_{D} = 9 V."], 13, false);
    life(s, 0.5, 4.55, 9.0, 1.0, ["Une diode bloquée prend toute la tension : sa tension inverse maximale doit dépasser celle de la source."], 11);
  }

  // ============================== 6. SYMBOLES ET REPÉRAGE
  {
    const s = slide("Symboles et repérage des bornes",
      "Symboles CEI 60617 : triangle et trait. La pointe du triangle montre le sens du courant direct, de l'anode A vers la cathode K.\n" +
      "Zener : le trait de cathode a un petit retour. LED : deux flèches qui sortent (la lumière émise). Une photodiode a des flèches qui entrent (présentation 220).\n" +
      "Sur le composant : l'anneau de la diode marque la cathode, comme le trait du symbole. LED : patte longue = anode, méplat de la collerette = cathode. En cas de doute : multimètre en position diode.");
    img(s, "fig_symboles.png", 0.5, 0.95, 5.0, 2.35);
    img(s, "fig_boitiers.png", 0.5, 3.35, 5.0, 2.3);
    card(s, 5.7, 0.95, 3.8, 1.75);
    txt(s, [{ text: "Moyen mnémotechnique", options: { bold: true, color: BLUE, breakLine: true } },
      { text: "L'anneau sur le boîtier est à la place du trait sur le symbole : les deux marquent la cathode." }],
      { x: 5.85, y: 1.02, w: 3.5, h: 1.6, fontSize: 12.5, paraSpaceAfter: 4 });
    boxTitle(s, 5.7, 2.85, 3.8, 1.5, "LED", ["Patte longue : anode.", "Méplat de la collerette : cathode."], 12, true);
    life(s, 5.7, 4.5, 3.8, 1.1, ["Multimètre en position diode : ≈ 0,6 V en direct (pointe rouge sur l'anode), « OL » en inverse."], 10.5);
  }

  // ============================== 7. LA CARACTÉRISTIQUE I(U)
  {
    const s = slide("La caractéristique I(U) de la diode",
      "La caractéristique donne le courant I en fonction de la tension U. Elle est relevée en pratique (TM2-A1-S3).\n" +
      "Sens direct : presque rien jusqu'à ≈ 0,6 V, puis le courant monte très vite. Sens inverse : un courant de fuite minuscule.\n" +
      "Claquage : au-delà de la tension inverse maximale (U_BR, des dizaines à des centaines de volts), le courant monte brusquement. Pour une diode ordinaire, cela la détruit.\n" +
      "Les échelles ne sont pas les mêmes dans les deux sens : mA et dixièmes de volt à droite, µA et dizaines de volts à gauche.");
    img(s, "fig_carac_diode.png", 0.5, 0.95, 5.4, 3.55);
    [["Sens direct", "le courant passe dès ≈ 0,6 V"], ["Sens inverse", "bloquée : courant de fuite"], ["Claquage", "diode ordinaire : détruite"]].forEach(([t, d], i) => {
      const y = 0.95 + i * 1.2;
      card(s, 6.1, y, 3.4, 1.08);
      txt(s, t, { x: 6.25, y: y + 0.07, w: 3.1, h: 0.3, fontSize: 12.5, bold: true, color: i === 2 ? RED : BLUE });
      txt(s, d, { x: 6.25, y: y + 0.42, w: 3.1, h: 0.58, fontSize: 12 });
    });
    life(s, 0.5, 4.65, 9.0, 0.9, ["En TM2-A1-S3, tu relèves cette courbe point par point : alimentation réglable, résistance de protection, deux multimètres."], 11);
  }

  // ============================== 8. LIRE LA CARACTÉRISTIQUE DIRECTE
  {
    const s = slide("Lire la caractéristique directe",
      "Courbe d'une diode au silicium, à l'échelle. Lecture : on part de l'axe du courant, on rejoint la courbe, on descend sur l'axe de la tension.\n" +
      "À 10 mA, U_F ≈ 0,7 V. À 30 mA, U_F ≈ 0,8 V seulement : le courant triple, la tension monte d'un dixième de volt. D'où le modèle « U_F = 0,7 V » de la diapositive suivante.\n" +
      "Tensions de seuil usuelles : germanium ≈ 0,3 V ; Schottky 0,2 à 0,4 V ; silicium 0,6 à 0,7 V ; LED 1,3 à 3,4 V selon la couleur.");
    img(s, "fig_carac_directe.png", 0.5, 0.95, 5.0, 3.4);
    s.addTable([
      [cell("Diode", H), cell("Tension de seuil", H)],
      [cell("germanium", { align: "left" }), cell("≈ 0,3 V")],
      [cell("Schottky", { align: "left" }), cell("0,2 à 0,4 V")],
      [cell("silicium", { align: "left", bold: true }), cell("0,6 à 0,7 V", { bold: true, color: BLUE })],
      [cell("LED", { align: "left" }), cell("1,3 à 3,4 V")],
    ], { x: 5.75, y: 0.95, w: 3.75, colW: [1.65, 2.1], rowH: 0.42, border: BORDER, fontSize: 12 });
    txt(s, "Au-dessus du seuil, la tension varie peu : 10 mA → 0,7 V, 30 mA → 0,8 V.", { x: 5.75, y: 3.2, w: 3.75, h: 1.1, fontSize: 12, bold: true, color: NAVY });
    life(s, 0.5, 4.55, 9.0, 1.0, ["Quand tu mesures une diode qui conduit, tu lis presque toujours entre 0,6 et 0,8 V : au-delà de 1 V, cherche l'erreur de câblage."], 11);
  }

  // ============================== 9. DEUX MODÈLES POUR CALCULER
  {
    const s = slide("Deux modèles pour calculer",
      "On remplace la vraie courbe (en pointillé) par un modèle simple.\n" +
      "Diode idéale : un interrupteur, fermé en direct (0 V), ouvert en inverse. Suffit quand la source est grande (24 V : 0,7 V ne change presque rien) ou pour savoir si une diode conduit.\n" +
      "Diode avec seuil : U_F = 0,7 V dès qu'elle conduit. À utiliser quand la source est petite (5 V, 3,3 V) ou pour une LED (U_F de 2 V ou 3 V).\n" +
      "La résistance de la diode en conduction (pente de la courbe) est négligée ici ; on l'utilise pour la Zener (diapositive 12).");
    img(s, "fig_modeles.png", 0.5, 0.95, 5.6, 2.75);
    boxTitle(s, 6.3, 0.95, 3.2, 1.35, "Diode idéale", ["Grande tension de source.", "« Conduit-elle ou pas ? »"], 11.5, true);
    boxTitle(s, 6.3, 2.4, 3.2, 1.35, "Diode avec seuil", ["Petite tension de source.", "LED : U_{F} de 2 à 3 V."], 11.5, false);
    card(s, 0.5, 3.9, 9.0, 0.6, NAVY);
    txt(s, [{ text: "Règle : ", options: { bold: true, color: LBLUE } }, { text: "si U_{F} est petite devant la tension de la source, le modèle idéal suffit.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 3.9, w: 8.6, h: 0.6, fontSize: 12.5, valign: "middle" });
    life(s, 0.5, 4.65, 9.0, 0.9, ["Sur l'alimentation 24 V de l'équipement, la diode de protection « coûte » ≈ 0,7 V : la carte reçoit encore plus de 23 V."], 11);
  }

  // ============================== 10. LES VALEURS LIMITES
  {
    const s = slide("Les valeurs limites de la fiche technique",
      "Les valeurs limites (absolute maximum ratings) ne doivent jamais être dépassées, même un instant.\n" +
      "U_RRM : tension inverse répétitive maximale. I_F(AV) : courant direct moyen maximal. U_F : tension directe pour un courant donné. P_tot : puissance maximale.\n" +
      "1N4148 : petite diode de signal, rapide. 1N4007 : diode de redressement, 1 A et 1000 V. Valeurs arrondies : toujours vérifier la fiche du fabricant.\n" +
      "Pour l'équipement de test : la diode de protection de l'alimentation doit supporter le courant de la carte et la tension inverse si on branche à l'envers.");
    const g = (t) => cell(t, { align: "left", bold: true });
    s.addTable([
      [cell("Grandeur", H), cell("Signification", H), cell("1N4148", H), cell("1N4007", H)],
      [g("U_{RRM}"), cell("tension inverse maximale", { align: "left" }), cell("100 V"), cell("1000 V")],
      [g("I_{F(AV)}"), cell("courant direct maximal (moyen)", { align: "left" }), cell("≈ 150 mA"), cell("1 A")],
      [g("U_{F}"), cell("tension directe", { align: "left" }), cell("≤ 1 V à 10 mA"), cell("≤ 1,1 V à 1 A")],
      [g("Usage"), cell("domaine d'emploi", { align: "left" }), cell("signaux, logique"), cell("alimentations")],
    ], { x: 0.5, y: 0.95, w: 9.0, colW: [1.5, 3.4, 2.05, 2.05], rowH: 0.5, border: BORDER, fontSize: 12 });
    card(s, 0.5, 3.65, 9.0, 0.8, NAVY);
    txt(s, [{ text: "À retenir : ", options: { bold: true, color: LBLUE } }, { text: "on choisit une diode avec de la marge sur U_{RRM} et sur I_{F}.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 3.65, w: 8.6, h: 0.8, fontSize: 13, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, ["La 1N4007 est la diode de protection classique : 1 A, 1000 V, quelques centimes. Elle protège l'alimentation 24 V de l'équipement."], 11);
  }

  // ============================== 11. LA DIODE ZENER
  {
    const s = slide("La diode Zener : le claquage utilisé",
      "Une diode ordinaire est détruite par le claquage. La Zener est fabriquée (dopage plus fort, jonction mince) pour claquer à une tension précise U_Z sans être détruite, tant que sa puissance reste sous P_tot.\n" +
      "On la branche en inverse : la cathode vers le +. Dans la zone de claquage, sa tension reste presque constante quand le courant varie.\n" +
      "En sens direct, elle se comporte comme une diode ordinaire (≈ 0,7 V).\n" +
      "Valeurs courantes de U_Z : de 2,4 V à plus de 100 V (série E24 : 3V3, 5V1, 12 V…).");
    img(s, "fig_carac_zener_allure.png", 0.5, 0.95, 5.4, 3.55);
    boxTitle(s, 6.1, 0.95, 3.4, 1.75, "Branchée en inverse", ["Cathode vers le +.", "Au-dessus de U_{Z} : elle conduit.", "Sa tension reste ≈ U_{Z}."], 11.5, true);
    boxTitle(s, 6.1, 2.85, 3.4, 1.65, "Pas détruite", ["Le claquage est voulu.", "Condition : P_{Z} < P_{tot}."], 11.5, false);
    life(s, 0.5, 4.65, 9.0, 0.9, ["En TM2-A1-S2, tu relèves la caractéristique d'une Zener : tu verras la tension se fixer à U_{Z}."], 11);
  }

  // ============================== 12. LES PARAMÈTRES DE LA ZENER
  {
    const s = slide("Les paramètres de la Zener",
      "U_Z : tension Zener, donnée pour un courant de test (BZX55C5V1 : 5,1 V à 5 mA, entre 4,8 et 5,4 V).\n" +
      "r_Z : résistance dynamique, pente de la courbe dans la zone de claquage. Plus elle est petite, plus la tension est stable. Ici : 0,2 V de plus pour 20 mA de plus, soit 10 Ω.\n" +
      "I_Zmax : courant maximal, fixé par la puissance P_tot. Calcul : I_Zmax = 500 mW / 5,1 V = 98,04 mA. Contrôle : 5,1 V · 98 mA ≈ 500 mW.\n" +
      "Sous I_Zmin (le coude, ≈ 1 mA), la tension n'est plus stable.");
    img(s, "fig_carac_zener.png", 0.5, 0.95, 4.6, 3.6);
    // équations éditables : PowerPoint les affiche à leur taille de police, sans les réduire au cadre.
    // Une fraction occupe ≈ 2,6 fois le corps : cadre de 0,62" → 17 pt ; 0,6" → 15 pt (controle/mise_en_page.py le vérifie).
    frame(s, 5.3, 0.95, 4.2, 1.7);
    txt(s, "Résistance dynamique", { x: 5.45, y: 1.0, w: 3.9, h: 0.3, fontSize: 12, bold: true, color: BLUE });
    eqImg(s, "eq_rz.png", "r_{Z}=\\f{\\Delta U_{Z}}{\\Delta I_{Z}}", 5.45, 1.3, 1.6, 0.62, 1700);
    eqImg(s, "eq_rz_an.png", "r_{Z}=\\f{5,3\\u{ [V]}-5,1\\u{ [V]}}{25\\u{ [mA]}-5\\u{ [mA]}}=10\\u{ [Ω]}", 5.45, 1.97, 3.9, 0.6, 1500);
    frame(s, 5.3, 2.75, 4.2, 1.85);
    txt(s, "Courant maximal (P_{tot} = 500 mW)", { x: 5.45, y: 2.8, w: 3.9, h: 0.3, fontSize: 12, bold: true, color: BLUE });
    eqImg(s, "eq_izmax.png", "I_{Zmax}=\\f{P_{tot}}{U_{Z}}", 5.45, 3.1, 1.6, 0.62, 1700);
    eqImg(s, "eq_izmax_an.png", "I_{Zmax}=\\f{500\\u{ [mW]}}{5,1\\u{ [V]}}=98,04\\u{ [mA]}", 5.45, 3.75, 3.9, 0.55, 1500);
    txt(s, "Contrôle : 5,1 V · 98 mA ≈ 500 mW ✓", { x: 5.45, y: 4.3, w: 3.9, h: 0.26, fontSize: 10.5, italic: true, color: GR });
    card(s, 0.5, 4.7, 9.0, 0.4, NAVY);
    txt(s, [{ text: "Puissance : ", options: { bold: true, color: LBLUE } }, { text: "P_{Z} = U_{Z} · I_{Z}, toujours inférieure à P_{tot}.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 4.7, w: 8.6, h: 0.4, fontSize: 12, valign: "middle" });
    life(s, 0.5, 5.17, 9.0, 0.55, ["Le courant de la Zener se règle avec une résistance en série : calcul en présentation 200 (stabilisation)."], 10.5);
  }

  // ============================== 13. APPLICATIONS DE LA ZENER
  {
    const s = slide("Applications de la Zener",
      "Protection d'entrée (fil rouge) : un capteur de la ligne envoie 0 à 24 V, l'entrée du contrôleur accepte 5 V au plus. Avec R_1 et une Zener 5V1, U_s ne dépasse pas ≈ 5,1 V.\n" +
      "Sous 5,1 V, la Zener est bloquée : pas de courant, pas de tension sur R_1, U_s = U_e. Au-dessus, elle conduit : R_1 prend la différence (24 − 5,1 = 18,9 V).\n" +
      "Autres usages : tension de référence (comparateur, chargeur), stabilisation d'une alimentation simple (présentation 200), écrêtage de surtensions.\n" +
      "Sans R_1, la Zener serait reliée directement à la source : courant énorme, Zener détruite.");
    img(s, "fig_zener_entree.png", 0.5, 0.95, 4.2, 3.55);
    s.addTable([
      [cell("U_{e}", H), cell("Zener", H), cell("U_{s}", H)],
      [cell("3 V"), cell("bloquée"), cell("3 V")],
      [cell("12 V"), cell("conduit"), cell("≈ 5,1 V", { bold: true, color: BLUE })],
      [cell("24 V"), cell("conduit"), cell("≈ 5,1 V", { bold: true, color: BLUE })],
    ], { x: 4.95, y: 0.95, w: 4.55, colW: [1.2, 1.75, 1.6], rowH: 0.4, border: BORDER, fontSize: 12 });
    boxTitle(s, 4.95, 2.75, 4.55, 1.75, "Les usages", ["Protéger une entrée (écrêtage).", "Tension de référence.", "Stabiliser une alimentation (présentation 200)."], 11.5, true);
    life(s, 0.5, 4.65, 9.0, 0.9, ["La résistance R_{1} est indispensable : c'est elle qui prend la différence de tension et limite le courant de la Zener."], 11);
  }

  // ============================== 14. LA LED
  {
    const s = slide("La LED : une diode qui éclaire",
      "LED : diode électroluminescente. Quand elle conduit, des électrons retombent dans des trous à la jonction : l'énergie libérée sort en lumière (photon).\n" +
      "Le matériau n'est pas du silicium : arséniure de gallium (rouge, infrarouge), nitrure de gallium-indium (bleu, vert vif, blanc). La couleur dépend du matériau, et U_F avec elle.\n" +
      "Une LED blanche est une LED bleue recouverte d'un luminophore jaune.\n" +
      "Valeurs typiques à 20 mA, à vérifier sur la fiche technique.");
    img(s, "fig_led_principe.png", 0.5, 0.95, 4.6, 2.3);
    s.addTable([
      [cell("Couleur", H), cell("U_{F} typique", H)],
      [cell("infrarouge", { align: "left" }), cell("≈ 1,3 V")],
      [cell("rouge", { align: "left" }), cell("≈ 1,9 V")],
      [cell("jaune, orange", { align: "left" }), cell("≈ 2,1 V")],
      [cell("vert", { align: "left" }), cell("2,2 à 3 V")],
      [cell("bleu, blanc", { align: "left" }), cell("≈ 3,2 V")],
    ], { x: 5.4, y: 0.95, w: 4.1, colW: [2.0, 2.1], rowH: 0.42, border: BORDER, fontSize: 12 });
    card(s, 0.5, 3.4, 4.6, 1.1);
    txt(s, [{ text: "Plus la lumière est « bleue », plus U_{F} est grande.", options: { bold: true, color: NAVY } }],
      { x: 0.7, y: 3.4, w: 4.2, h: 1.1, fontSize: 12.5, valign: "middle" });
    life(s, 0.5, 4.65, 9.0, 0.9, ["Sur l'équipement, la LED sert de voyant, d'afficheur et d'émetteur dans l'optocoupleur des entrées (présentation 220)."], 11);
  }

  // ============================== 15. LA LED DANS L'ÉQUIPEMENT
  {
    const s = slide("Brancher une LED sans la détruire",
      "Une LED ne se branche jamais seule sur une source : au-dessus de U_F, son courant monte très vite (même courbe qu'une diode). On limite toujours le courant avec une résistance en série (calcul en présentation 140, pratique TM2-A2-S1).\n" +
      "Valeurs limites typiques d'une LED rouge 5 mm : I_F max 20 à 30 mA ; U_R max 5 V seulement. Une LED branchée à l'envers sur 9 V ou 24 V peut claquer.\n" +
      "La luminosité dépend du courant : quelques mA suffisent pour un voyant moderne.");
    img(s, "fig_led_voyant.png", 0.5, 0.95, 3.0, 3.55);
    s.addTable([
      [cell("Valeur limite", H), cell("LED rouge 5 mm", H), cell("Conséquence", H)],
      [cell("I_{F} max", { align: "left", bold: true }), cell("20 à 30 mA"), cell("toujours une résistance en série", { align: "left" })],
      [cell("U_{R} max", { align: "left", bold: true }), cell("5 V", { bold: true, color: RED }), cell("jamais à l'envers sur 24 V", { align: "left" })],
      [cell("U_{F}", { align: "left", bold: true }), cell("≈ 1,9 V"), cell("la résistance prend le reste", { align: "left" })],
    ], { x: 3.75, y: 0.95, w: 5.75, colW: [1.45, 1.6, 2.7], rowH: 0.5, border: BORDER, fontSize: 11.5 });
    card(s, 3.75, 3.2, 5.75, 1.3, NAVY);
    txt(s, [{ text: "À retenir : ", options: { bold: true, color: LBLUE } },
      { text: "une LED a toujours une résistance en série, et sa tension inverse maximale est petite (≈ 5 V).", options: { color: "FFFFFF" } }],
      { x: 3.95, y: 3.2, w: 5.35, h: 1.3, fontSize: 12.5, valign: "middle" });
    life(s, 0.5, 4.65, 9.0, 0.9, ["Le voyant « en marche » de l'équipement : LED rouge et R_{1} = 2k2 sur 24 V (dimensionnement en présentation 140)."], 11);
  }

  // ============================== 16. COMPARER
  {
    const s = slide("Diode, Zener, LED : comparer",
      "Synthèse à faire recopier ou compléter dans la carte mentale.\n" +
      "Point commun : une jonction PN, un sens direct à partir d'une tension de seuil. Différences : le sens de branchement, la tension utile, l'usage.");
    const B = { bold: true, color: BLUE };
    s.addTable([
      [cell("", H), cell("Diode", H), cell("Diode Zener", H), cell("LED", H)],
      [cell("Branchée en", L), cell("direct (conduit)\ninverse (bloque)"), cell("inverse", B), cell("direct", B)],
      [cell("Tension utile", L), cell("U_{F} ≈ 0,7 V"), cell("U_{Z} (2,4 à 100 V)"), cell("U_{F} 1,3 à 3,4 V")],
      [cell("Valeur limite", L), cell("U_{RRM}, I_{F}"), cell("P_{tot}"), cell("I_{F} max, U_{R} ≈ 5 V")],
      [cell("Usage", L), cell("protection, redressement"), cell("référence, protection d'entrée"), cell("voyant, affichage")],
    ], { x: 0.5, y: 0.95, w: 9.0, colW: [1.8, 2.4, 2.4, 2.4], rowH: 0.58, border: BORDER, fontSize: 12 });
    card(s, 0.5, 4.0, 9.0, 0.6, NAVY);
    txt(s, [{ text: "Point commun : ", options: { bold: true, color: LBLUE } }, { text: "une jonction PN, qui conduit de l'anode vers la cathode.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 4.0, w: 8.6, h: 0.6, fontSize: 13, valign: "middle" });
    life(s, 0.5, 4.75, 9.0, 0.8, ["Ces trois composants suffisent pour l'extension : protection de l'alimentation, entrées limitées, voyants."], 11);
  }

  // ============================== 17. RÉPONSE · TICKET DE SORTIE
  {
    const s = slide("Réponse à la question · ticket de sortie",
      "Réponse : une diode en série dans l'alimentation (1N4007). Branchée correctement, elle conduit et ne coûte que ≈ 0,7 V. Branchée à l'envers, elle bloque : aucun courant ne peut abîmer la carte, et c'est la diode qui prend les 24 V (U_RRM = 1000 V).\n" +
      "Ticket de sortie (5 min, seul·e, sans support). Réponses : 1) de l'anode vers la cathode. 2) Environ 0,7 V. 3) Elle conduit et sa tension reste ≈ 5,1 V. 4) Sa tension inverse maximale est ≈ 5 V : elle peut claquer.\n" +
      "Ensuite : la fiche 130 EX.");
    img(s, "fig_anti_inversion.png", 0.5, 0.95, 3.0, 4.0);
    card(s, 3.7, 0.95, 5.8, 1.45, NAVY);
    txt(s, [{ text: "Réponse : ", options: { bold: true, color: LBLUE } },
      { text: "une diode en série. À l'endroit, elle conduit (≈ 0,7 V perdus). À l'envers, elle bloque : la carte ne reçoit rien.", options: { color: "FFFFFF" } }],
      { x: 3.9, y: 0.95, w: 5.4, h: 1.45, fontSize: 12.5, valign: "middle" });
    frame(s, 3.7, 2.55, 5.8, 2.4);
    txt(s, "Ticket de sortie : seul·e, 5 minutes, sans support", { x: 3.85, y: 2.62, w: 5.5, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    [["1", "Dans quel sens une diode conduit-elle ?"], ["2", "Diode au silicium à 10 mA : U_{F} environ ?"],
     ["3", "Zener 5V1 en inverse, U monte à 12 V : que fait-elle ?"], ["4", "Pourquoi jamais une LED à l'envers sur 9 V ?"]].forEach((q, i) => {
      const y = 3.0 + i * 0.47;
      badge(s, 3.85, y + 0.06, q[0], 0.32);
      txt(s, q[1], { x: 4.3, y, w: 5.1, h: 0.44, fontSize: 11.5, valign: "middle" });
    });
    card(s, 0.5, 5.05, 9.0, 0.5);
    txt(s, [{ text: "Ensuite : ", options: { bold: true } }, { text: "complète ta carte mentale, puis fiche 130 EX Diode et Zener." }], { x: 0.65, y: 5.05, w: 8.7, h: 0.5, fontSize: 11.5, valign: "middle" });
  }

  // ============================== 18. EXERCICES
  exoSlide("130 EX", DATA.TEAMS["130"], [
    ["1", "La LED s'allume-t-elle ?", "≈ 8 min · diapositives 4 à 6"], ["2", "Lire la caractéristique d'une diode", "≈ 8 min · diapositives 8 et 9"],
    ["3", "Lire une fiche technique", "≈ 8 min · diapositive 10"], ["4", "La caractéristique d'une Zener", "≈ 10 min · diapositive 12"],
    ["5", "La puissance de la Zener", "≈ 6 min · diapositive 12"], ["6", "L'équipement de test", "≈ 10 min · diapositives 13 à 15"]],
    "Tu prépares l'extension de l'équipement de test : protection de l'alimentation, entrées limitées à 5,1 V, voyants. L'ingénieure de développement vérifie tes choix.",
    "Seul·e ou en binôme, environ 50 min. Formule, application numérique, résultat, contrôle.",
    ["Ces lectures de courbes et de fiches techniques préparent les mesures de TM2-A1 et TM2-A2."],
    "Fiche 130 EX Diode et Zener : environ 50 min de travail, puis la correction en plénière. Temps indicatifs : N°1 8 min, N°2 8 min, N°3 8 min, N°4 10 min, N°5 6 min, N°6 10 min.\n" +
    "Corrigé : 130 EX C Diode et Zener (pour l'enseignant·e).");

  // ============================== 19. PAGE INTERACTIVE (phase médias)
  pageSlide("121", DATA.FILES["121"], DATA.TEAMS["121"], DATA.ART["121"], "shot_121.png",
    ["Polarise la jonction PN", "Lis la caractéristique de la diode", "Fais claquer la Zener", "Allume la LED sans la détruire"],
    ["À refaire à la maison avant le test : chaque erreur est expliquée."],
    "Page interactive 121 : un seul fichier .html, sans installation. Quatre étapes, chacune avec une animation « Comprendre » puis un exercice « À toi » corrigé tout de suite.\n" +
    "Déposer le fichier « 121 Diode et diode Zener.html » dans le dossier Teams LFB_El_Dim4 : le lien de la diapositive vise ce chemin.");

  // ============================== 20. VIDÉO (phase médias)
  videoSlide("125", DATA.FILES["125"], DATA.TEAMS["125"], "cover_125.png", "3 minutes et demie",
    [["La jonction PN", "sens direct, sens inverse"], ["La caractéristique", "seuil, fuite, claquage"],
     ["La Zener", "le claquage utilisé"], ["La LED", "la jonction qui éclaire"]],
    ["Pour réviser à la maison ou rattraper une absence."],
    "Animation 125 Diode et diode Zener : 3 min 36, 1920 × 1080. La vidéo est intégrée à la présentation (clic sur l'image en mode diaporama).\n" +
    "Déposer aussi le fichier « 125 Diode et diode Zener.mp4 » dans le dossier Teams LFB_El_Dim4 : le lien sous la vidéo vise ce chemin.");
};
