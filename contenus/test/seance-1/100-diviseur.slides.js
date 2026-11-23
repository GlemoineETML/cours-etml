// 100 Diviseur de tension : diapositives (moteur : moteur/deck.js). Séance de test du workflow, hors réforme.
// Fil rouge : surveiller la batterie d'une voiture (12 V, 14,4 V en charge) avec l'entrée analogique d'un Arduino (0 … 5 V).
// Toutes les valeurs sont recalculées par verif.py.
module.exports = function (E) {
  const { pres, DATA, NAVY, BLUE, LBLUE, TINT, K, GR, RED, F, slide, txt, card, frame, badge, img, eqImg, bullets, life,
    boxTitle, cell, H, BORDER, exoSlide, titreSlide } = E;

  // ============================== 1. TITRE · OBJECTIFS · QUESTION DE DÉPART
  titreSlide({
    titre: "Diviseur de\ntension",
    sousTitre: "Partager une tension avec deux résistances",
    objectifs: ["calculer la tension de sortie d'un diviseur ;", "contrôler le résultat avec la loi des mailles ;",
      "choisir deux résistances pour adapter une tension ;", "expliquer l'effet d'une charge sur le diviseur."],
    question: "La batterie d'une voiture fait 12 V, et jusqu'à 14,4 V pendant la charge. Tu veux la surveiller avec l'entrée analogique d'un Arduino, qui accepte de 0 à 5 V. Comment faire ?",
    indice: "Écris ton hypothèse. Réponse à la diapositive 5.",
    notes: "Durée : 45 min. Diapositives 2 et 3 : le principe et la formule. Diapositive 4 : exemple travaillé. Diapositive 5 : réponse à la question de départ. Diapositive 6 : effet d'une charge. Diapositive 7 : synthèse et ticket de sortie. Diapositive 8 : fiche 110 EX.\n" +
      "Prérequis : loi d'Ohm, résistances en série et en parallèle, loi des mailles.\n" +
      "Question de départ : noter les hypothèses sans les corriger. Réponse à la diapositive 5 : un diviseur 22k / 10k ramène 14,4 V à 4,5 V.",
  });

  // ============================== 2. LE PRINCIPE
  {
    const s = slide("Le diviseur de tension : le principe",
      "Deux résistances en série sont traversées par le même courant : la tension U se partage entre elles, proportionnellement à leur valeur.\n" +
      "La tension de sortie U_2 ne dépend que du rapport des résistances, pas de leur valeur absolue (tant que rien n'est branché sur la sortie : diapositive 6).\n" +
      "Faire prédire : si R_1 = R_2, que vaut U_2 ? (la moitié de U).");
    img(s, "fig_diviseur.png", 0.5, 0.95, 4.6, 3.3);
    frame(s, 5.3, 0.95, 4.2, 1.4);
    txt(s, "La formule", { x: 5.45, y: 1.0, w: 3.9, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    eqImg(s, "eq_diviseur.png", "U_{2}=U\\cdot \\f{R_{2}}{R_{1}+R_{2}}", 5.75, 1.35, 3.3, 0.85, 2400);
    card(s, 5.3, 2.5, 4.2, 1.75);
    bullets(s, ["Deux résistances en série se partagent la tension U.", "La plus grande résistance reçoit la plus grande part.",
      "U_{2} ne dépend que du rapport des résistances."], { x: 5.45, y: 2.62, w: 3.9, h: 1.55, fontSize: 12 });
    life(s, 0.5, 4.4, 9.0, 1.15, [
      "Mesurer la tension d'une batterie avec l'entrée analogique d'un microcontrôleur, qui n'accepte que 0 à 5 V.",
      "Un potentiomètre est un diviseur réglable : bouton de volume, consigne de température d'un thermostat.",
    ]);
  }

  // ============================== 3. D'OÙ VIENT LA FORMULE ?
  {
    const s = slide("D'où vient la formule ?",
      "Démonstration en trois lignes, à faire au tableau avec la classe. Elle ne demande que la loi d'Ohm et la règle du circuit série.\n" +
      "Contrôle à faire à chaque calcul : U_1 + U_2 = U (loi des mailles). Le contrôle écrit fait partie de l'évaluation.");
    [["1", "R_{1} et R_{2} sont en série : le même courant I les traverse."],
     ["2", "Loi d'Ohm sur tout le circuit :"],
     ["3", "Loi d'Ohm sur R_{2} seule : U_{2} = R_{2} · I."],
     ["4", "On remplace I : on retrouve la formule du diviseur."]].forEach((r, i) => {
      const y = 1.0 + i * 0.78;
      badge(s, 0.5, y + 0.05, r[0], 0.38);
      txt(s, r[1], { x: 1.0, y, w: i === 1 ? 2.6 : 4.3, h: 0.5, fontSize: 12.5, valign: "middle" });
    });
    eqImg(s, "eq_courant.png", "I=\\f{U}{R_{1}+R_{2}}", 3.5, 1.68, 1.9, 0.68, 2000);
    frame(s, 5.6, 0.95, 3.9, 2.5);
    txt(s, "Résultat", { x: 5.75, y: 1.02, w: 3.6, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    eqImg(s, "eq_diviseur.png", "U_{2}=U\\cdot \\f{R_{2}}{R_{1}+R_{2}}", 5.9, 1.45, 3.3, 0.85, 2400);
    txt(s, [{ text: "Contrôle : ", options: { bold: true } }, { text: "U_{1} + U_{2} = U (loi des mailles)." }], { x: 5.75, y: 2.6, w: 3.6, h: 0.7, fontSize: 12 });
    life(s, 0.5, 4.3, 9.0, 1.25, [
      "Le même raisonnement sert pour un capteur résistif (thermistance, photorésistance) monté en diviseur : la tension mesurée suit la résistance du capteur.",
    ]);
  }

  // ============================== 4. EXEMPLE TRAVAILLÉ
  {
    const s = slide("Exemple travaillé : la batterie de la voiture",
      "Les quatre étapes de toute résolution : formule littérale, application numérique avec les unités, résultat avec unité, contrôle.\n" +
      "U_2 = 12 V · 10 kΩ / 32 kΩ = 3,75 V. Contrôle : U_1 = 12 V · 22 kΩ / 32 kΩ = 8,25 V et 8,25 V + 3,75 V = 12 V. Courant : I = 12 V / 32 kΩ = 375 µA.");
    img(s, "fig_batterie.png", 0.5, 0.95, 4.2, 3.3);
    const etapes = [["1", "Formule"], ["2", "Application numérique"], ["3", "Résultat"], ["4", "Contrôle"]];
    etapes.forEach((r, i) => {
      const y = 0.95 + i * 0.86;
      badge(s, 4.95, y + 0.04, r[0], 0.34);
      txt(s, r[1], { x: 5.4, y, w: 4.1, h: 0.3, fontSize: 12, bold: true, color: BLUE, valign: "middle" });
    });
    eqImg(s, "eq_diviseur.png", "U_{2}=U\\cdot \\f{R_{2}}{R_{1}+R_{2}}", 5.4, 1.22, 2.4, 0.55, 1800);
    eqImg(s, "eq_an.png", "U_{2}=12\\u{ [V]}\\cdot \\f{10\\u{ [kΩ]}}{22\\u{ [kΩ]}+10\\u{ [kΩ]}}", 5.4, 2.08, 3.6, 0.55, 1600);
    txt(s, "U_{2} = 3,75 V", { x: 5.4, y: 3.0, w: 4.1, h: 0.4, fontSize: 15, bold: true, color: NAVY, valign: "middle" });
    txt(s, "U_{1} = 8,25 V et 8,25 V + 3,75 V = 12 V ✓", { x: 5.4, y: 3.86, w: 4.1, h: 0.35, fontSize: 12, valign: "middle" });
    life(s, 0.5, 4.45, 9.0, 1.1, [
      "Le contrôle par la loi des mailles prend dix secondes et attrape la plupart des erreurs de calcul.",
      "Au laboratoire : on mesure U_{1} et U_{2} au multimètre et on compare au calcul.",
    ]);
  }

  // ============================== 5. RÉPONSE À LA QUESTION DE DÉPART
  {
    const s = slide("Réponse à la question de départ",
      "Le cas le plus défavorable est la batterie en charge, 14,4 V : il faut alors U_2 ≤ 5 V. Avec R_2 = 10 kΩ : R_1 ≥ 14,4 V · 10 kΩ / 5 V − 10 kΩ = 18,8 kΩ. On prend 22 kΩ, valeur de la série E12.\n" +
      "Vérification : 14,4 V → 4,5 V ; 12 V → 3,75 V. Courant consommé au plus : 14,4 V / 32 kΩ = 450 µA, négligeable pour une batterie.");
    s.addTable([
      [cell("Batterie", H), cell("U", H), cell("U_{2}", H)],
      [cell("au repos", { align: "left" }), cell("12 V"), cell("3,75 V", { bold: true, color: BLUE })],
      [cell("en charge", { align: "left" }), cell("14,4 V"), cell("4,5 V", { bold: true, color: BLUE })],
    ], { x: 0.5, y: 0.95, w: 4.4, colW: [1.6, 1.4, 1.4], rowH: 0.45, border: BORDER, fontSize: 12 });
    frame(s, 0.5, 2.5, 4.4, 1.75);
    txt(s, "Réponse", { x: 0.65, y: 2.57, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, "Un diviseur 22k / 10k ramène 14,4 V à 4,5 V : l'entrée de l'Arduino reste sous 5 V, même pendant la charge.", { x: 0.65, y: 2.92, w: 4.1, h: 1.25, fontSize: 12 });
    boxTitle(s, 5.1, 0.95, 4.4, 2.0, "Pourquoi 22k et 10k ?", [
      "Il faut R_{1} ≥ 18,8 kΩ pour rester sous 5 V : on prend 22k (série E12).",
      "Avec quelques dizaines de kΩ, le diviseur consomme moins de 0,5 mA."], 11.5, false);
    life(s, 5.1, 3.1, 4.4, 1.15, ["Le même montage surveille la batterie d'un vélo électrique ou d'un robot."], 10.5);
    card(s, 0.5, 4.45, 9.0, 1.1, NAVY);
    txt(s, [{ text: "À retenir : ", options: { bold: true, color: LBLUE } }, { text: "on dimensionne pour le cas le plus défavorable (la tension la plus haute), puis on vérifie le cas normal.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 4.45, w: 8.6, h: 1.1, fontSize: 12.5, valign: "middle" });
  }

  // ============================== 6. ATTENTION À LA CHARGE
  {
    const s = slide("Attention à la charge",
      "Une charge R_L branchée sur la sortie se met en parallèle avec R_2 : la résistance du bas diminue, U_2 baisse.\n" +
      "R_L = 10 kΩ : R_2 // R_L = 5 kΩ, U_2 = 12 V · 5 kΩ / 27 kΩ = 2,222 V au lieu de 3,75 V, soit −40,74 %.\n" +
      "R_L = 100 kΩ : R_2 // R_L = 9,091 kΩ, U_2 = 3,509 V, soit −6,433 %. Règle pratique : R_L ≥ 10 · R_2.\n" +
      "L'entrée analogique de l'ATmega328P a une résistance de 100 MΩ (fiche technique) : elle ne charge pas le diviseur.");
    img(s, "fig_charge.png", 0.5, 0.95, 4.9, 3.25);
    frame(s, 5.6, 0.95, 3.9, 2.05);
    txt(s, "R_{L} = 10 kΩ en parallèle sur R_{2}", { x: 5.75, y: 1.0, w: 3.6, h: 0.3, fontSize: 12, bold: true, color: BLUE });
    eqImg(s, "eq_parallele.png", "R_{2L}=\\f{R_{2}\\cdot R_{L}}{R_{2}+R_{L}}", 5.85, 1.35, 2.7, 0.6, 1800);
    txt(s, [{ text: "R_{2L} = 5 kΩ → U_{2} = 2,222 V", options: { bold: true, breakLine: true } }, { text: "au lieu de 3,75 V : −40,74 %", options: { color: RED } }],
      { x: 5.75, y: 2.1, w: 3.6, h: 0.8, fontSize: 12 });
    card(s, 5.6, 3.1, 3.9, 1.1);
    txt(s, [{ text: "Règle : ", options: { bold: true, color: BLUE } }, { text: "R_{L} ≥ 10 · R_{2}. Avec R_{L} = 100 kΩ, U_{2} = 3,509 V (−6,433 %)." }],
      { x: 5.75, y: 3.1, w: 3.6, h: 1.1, fontSize: 11.5, valign: "middle" });
    life(s, 0.5, 4.35, 9.0, 1.2, [
      "L'entrée analogique d'un microcontrôleur a une très grande résistance (100 MΩ pour l'ATmega328P) : elle ne charge pas le diviseur.",
      "Un voltmètre aussi est une charge : c'est pour cela qu'un multimètre numérique a 10 MΩ de résistance interne.",
    ], 10.5);
  }

  // ============================== 7. À RETENIR · TICKET DE SORTIE
  {
    const s = slide("À retenir · ticket de sortie",
      "Ticket de sortie (5 min, seul·e, sans support). Réponses : 1) 5 V. 2) La plus grande résistance. 3) U_2 baisse : la charge se met en parallèle avec R_2. " +
      "4) Le courant serait de 14,4 V / 32 Ω = 450 mA et les résistances dissiperaient 6,48 W : on gaspille l'énergie de la batterie et les résistances chauffent.\n" +
      "Ensuite : fiche 110 EX Diviseur de tension.");
    [["Le principe", "deux résistances en série se partagent la tension U"], ["Le contrôle", "U_{1} + U_{2} = U, toujours"], ["La charge", "R_{L} ≥ 10 · R_{2}, sinon U_{2} baisse"]].forEach(([h, d], k) => {
      const x = 0.5 + k * 3.05;
      card(s, x, 0.95, 2.9, 1.3);
      txt(s, h, { x: x + 0.15, y: 1.02, w: 2.6, h: 0.35, fontSize: 13, bold: true, color: BLUE });
      txt(s, d, { x: x + 0.15, y: 1.4, w: 2.6, h: 0.8, fontSize: 11.5 });
    });
    frame(s, 0.5, 2.45, 9.0, 2.45);
    txt(s, "Ticket de sortie : seul·e, 5 minutes, sans support", { x: 0.65, y: 2.52, w: 8.7, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    [["1", "R_{1} = R_{2} = 4k7 sous 10 V : combien vaut U_{2} ?"], ["2", "Laquelle des deux résistances reçoit la plus grande tension ?"],
     ["3", "On branche une charge de 1 kΩ sur R_{2} = 10 kΩ. U_{2} monte ou baisse ?"], ["4", "Pourquoi ne pas prendre 22 Ω et 10 Ω pour surveiller la batterie ?"]].forEach((q, i) => {
      const x = 0.65 + (i % 2) * 4.45, y = 2.95 + Math.floor(i / 2) * 0.9;
      badge(s, x, y + 0.13, q[0], 0.34);
      txt(s, q[1], { x: x + 0.45, y, w: 3.85, h: 0.62, fontSize: 12, valign: "middle" });
    });
    card(s, 0.5, 5.02, 9.0, 0.55);
    txt(s, [{ text: "Ensuite : ", options: { bold: true } }, { text: "fiche 110 EX Diviseur de tension." }], { x: 0.65, y: 5.02, w: 8.7, h: 0.55, fontSize: 11.5, valign: "middle" });
  }

  // ============================== 8. EXERCICES
  exoSlide("110 EX", DATA.TEAMS["110"], [
    ["1", "Calculer un diviseur", "≈ 8 min · diapositives 2 à 4"], ["2", "Surveiller une batterie", "≈ 12 min · diapositive 5"],
    ["3", "Brancher une charge", "≈ 12 min · diapositive 6"], ["4", "Dépannage", "≈ 8 min · diapositives 2 et 6"]],
    "Tu équipes un robot de démonstration pour les journées portes ouvertes. Son microcontrôleur doit surveiller la batterie et lire la position d'un potentiomètre.",
    "Seul·e ou en binôme, 40 min. Pour chaque calcul : formule, application numérique avec les unités, résultat, contrôle.",
    ["C'est le travail d'un électronicien de développement : adapter les tensions avant de les envoyer au microcontrôleur."],
    "Fiche 110 EX Diviseur de tension (40 min). Temps indicatifs : N°1 8 min, N°2 12 min, N°3 12 min, N°4 8 min.\n" +
    "Corrigé : 110 EX C Diviseur de tension (pour l'enseignant·e).");
};
