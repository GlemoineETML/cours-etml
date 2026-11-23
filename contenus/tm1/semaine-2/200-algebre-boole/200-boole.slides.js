// 200 Algèbre de Boole : diapositives (moteur : moteur/deck.js).
// Fil rouge : ligne de remplissage de boissons (situation de travail FutureMEM du champ LFB_El_DT1).
// Champ LFB_El_DT1 : LZ_2225 (C3, appliquer les lois), LZ_2226 (C5, développer et dessiner des circuits logiques).
// Convention (REGLES 3.4) : sortie S, entrées A, B, C… avec une légende ; jamais d'initiales (M, P, V…).
// Prérequis (semaine 1, non refaits ici) : notation du Floyd, sept portes, tables de vérité, CI 74HC (présentation 120, fiche 130 EX).
// Va avec la fiche 210 EX Algèbre de Boole (partie A pendant la présentation, partie B ensuite). Pas de lien Floyd ni nextecmedia.
module.exports = function (E) {
  const { pres, DATA, NAVY, BLUE, LBLUE, TINT, K, GR, RED, F, slide, txt, card, frame, badge, img, bullets, life,
    boxTitle, cell, H, BORDER, LINK, LZL, exoSlide, pageSlide, videoSlide, eqImg, titreSlide } = E;
  const EQS = require("./equations.json");
  const EQ = (s, k, x, y, w, maxH, sz, color) => eqImg(s, k + ".png", EQS[k], x, y, w, maxH, sz || 2000, color);
  const T120 = LINK("présentation 120", DATA.TEAMS["120"], "Présentation 120 Portes logiques et tables de vérité");
  const T130 = LINK("fiche 130 EX", DATA.TEAMS["130"], "Fiche 130 EX Portes logiques de base");
  const B = (t) => ({ text: t, options: { bold: true } });
  const N = (t) => ({ text: t });
  const OV = (t) => [...t].map(c => c + "\u0305").join("");   // barre continue sur une expression (texte affiché)
  const tdv = (n) => Array.from({ length: 1 << n }, (_, i) => Array.from({ length: n }, (_, j) => (i >> (n - 1 - j)) & 1));   // poids fort à gauche

  // ============================== 1. TITRE · OBJECTIFS · QUESTION DE DÉPART
  titreSlide({
    titre: "Algèbre de Boole",
    sousTitre: "Calculer avec des 0 et des 1 pour simplifier un circuit",
    objectifs: [
      [N("lire une équation dans le bon ordre : NON, ET, OU ;")],
      [N("appliquer les 3 lois et les 12 règles (") , LZL("LZ_2225"), N(") ;")],
      [N("appliquer le théorème de De Morgan (") , LZL("LZ_2225"), N(") ;")],
      [N("simplifier une équation et contrôler le résultat ;")],
      [N("dessiner le schéma du circuit simplifié (") , LZL("LZ_2226"), N(").")]],
    question: "Sur la ligne de remplissage, un collègue a câblé la commande du convoyeur de sortie telle qu'il l'a écrite. Il lui faut quatre portes sur quatre CI différents. Peut-on obtenir le même fonctionnement avec moins ?",
    indice: "Écris ton idée. Réponse aux diapositives 14 et 15.",
    dessin: (s) => { EQ(s, "eq_depart", 6.35, 3.25, 2.95, 0.5, 2000);
      txt(s, "S : convoyeur · A : machine en marche · B : bouteille pleine · C : vidange", { x: 6.15, y: 3.8, w: 3.35, h: 0.5, fontSize: 9.5, italic: true, color: GR, align: "center" }); },
    references: [LZL("LZ_2225"), LZL("LZ_2226"), T120, T130],
    notes: "Durée : 2 périodes. Présentation ≈ 45 min, avec la partie A de la fiche 210 EX (lois, règles, De Morgan) complétée au fur et à mesure ; puis partie B de la fiche 210 EX (45 min).\n" +
      "Déroulement : diapositive 2 rappel et ordre des opérations ; 3 pourquoi simplifier ; 4 et 5 les trois lois ; 6 à 8 les douze règles ; 9 et 10 à toi ; 11 à 13 De Morgan et NON-ET ; 14 et 15 méthode et schéma (réponse à la question de départ) ; 16 ticket de sortie ; 17 à 19 fiche, page interactive 201, animation 205.\n" +
      "Question de départ : S = A · B + A · B̄ · C (S : le convoyeur de sortie tourne ; A : machine en marche, B : bouteille pleine détectée, C : bouton de vidange). Noter les idées sans corriger. Réponse : S = A · (B + C), deux portes au lieu de quatre.\n" +
      "Convention (REGLES 3.4) : la sortie s'appelle toujours S, les entrées A, B, C… ; le sens de chaque lettre est donné en légende.",
  });

  // ============================== 2. CE QUE TU SAIS DÉJÀ · LIRE UNE ÉQUATION
  {
    const s = slide("Ce que tu sais déjà · lire une équation",
      "Activation (3 min, seul·e, sans support) : 1) 0, une porte ET ne donne 1 que si toutes ses entrées valent 1. 2) 2^3 = 8 lignes. 3) NON-OU (S = 1 seulement si A = B = 0).\n" +
      "Renvois : présentation 120, diapositive 4 (notation) et 12 (les sept portes) ; fiche 130 EX, N°1 (équation tirée d'une table).\n" +
      "Nouveau : l'ordre des opérations. Comme × avant + en calcul, ET passe avant OU. La barre longue agit comme une parenthèse : on calcule d'abord ce qu'elle couvre, puis on inverse.");
    frame(s, 0.5, 0.95, 4.3, 3.35);
    txt(s, "Rappel éclair : 3 minutes, seul·e", { x: 0.65, y: 1.02, w: 4.0, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    [["1", "A = 1 et B = 0 : que vaut A · B ?"], ["2", "Combien de lignes compte la table de vérité d'un système à 3 entrées ?"],
     ["3", "Quelle porte donne S = 1 seulement quand A = 0 et B = 0 ?"]].forEach((q, i) => {
      const y = 1.42 + i * 0.75;
      badge(s, 0.65, y + 0.1, q[0], 0.34);
      txt(s, q[1], { x: 1.1, y, w: 3.55, h: 0.6, fontSize: 12, valign: "middle" });
    });
    txt(s, [N("Notation et portes : "), T120, N(", diapositives 4 et 12.")], { x: 0.65, y: 3.75, w: 4.0, h: 0.45, fontSize: 10, color: GR });
    card(s, 5.0, 0.95, 4.5, 3.35);
    txt(s, "Ordre : NON, puis ET, puis OU", { x: 5.15, y: 1.02, w: 4.2, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    EQ(s, "eq_prio", 5.35, 1.45, 1.75, 0.45);
    txt(s, "se lit", { x: 7.15, y: 1.5, w: 0.6, h: 0.35, fontSize: 11, color: GR, valign: "middle" });
    EQ(s, "eq_prio_p", 7.7, 1.45, 1.7, 0.45);
    txt(s, "Comme en calcul, où × passe avant + : le ET passe avant le OU.", { x: 5.15, y: 2.05, w: 4.2, h: 0.55, fontSize: 11.5 });
    EQ(s, "eq_barre", 5.35, 2.7, 1.4, 0.48);
    txt(s, "La barre longue agit comme une parenthèse : on calcule A + B, puis on inverse.", { x: 6.85, y: 2.65, w: 2.5, h: 0.95, fontSize: 11 });
    txt(s, "Partie A de la fiche 210 EX : à compléter pendant la présentation.", { x: 5.15, y: 3.72, w: 4.2, h: 0.5, fontSize: 10.5, italic: true, color: GR });
    life(s, 0.5, 4.45, 9.0, 1.1, [
      "Un programme d'automate ou de microcontrôleur suit les mêmes priorités : une parenthèse oubliée et la vanne s'ouvre au mauvais moment.",
      "Dans le doute, mets des parenthèses.",
    ]);
  }

  // ============================== 3. POURQUOI SIMPLIFIER ?
  {
    const s = slide("Pourquoi simplifier ?",
      "Le schéma est celui de la question de départ, câblé tel que l'équation est écrite : une porte par opération.\n" +
      "Inventaire : NON (74HC04), ET à 2 entrées (74HC08), ET à 3 entrées (74HC11), OU (74HC32) : 4 portes, 4 CI différents, et dans chaque CI les autres portes ne servent à rien.\n" +
      "L'algèbre de Boole (George Boole, 1854) est un calcul sur des variables qui ne valent que 0 ou 1. Elle permet de transformer une équation sans changer sa table de vérité.");
    img(s, "fig_conv_avant.png", 0.5, 0.95, 4.7, 3.1);
    txt(s, "S = 1 : le convoyeur de sortie tourne. A : machine en marche · B : bouteille pleine détectée · C : bouton de vidange appuyé.",
      { x: 0.5, y: 4.0, w: 4.7, h: 0.45, fontSize: 9.5, italic: true, color: GR });
    card(s, 5.4, 0.95, 4.1, 1.55);
    txt(s, "Câblé tel quel", { x: 5.55, y: 1.02, w: 3.8, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    bullets(s, ["4 portes : NON, ET, ET à 3 entrées, OU", "4 CI : 74HC04, 74HC08, 74HC11, 74HC32"], { x: 5.55, y: 1.38, w: 3.8, h: 1.05, fontSize: 11.5 });
    frame(s, 5.4, 2.62, 4.1, 1.8);
    txt(s, "L'algèbre de Boole", { x: 5.55, y: 2.69, w: 3.8, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, "Un calcul sur des variables qui valent 0 ou 1. On transforme l'équation sans changer sa table de vérité, jusqu'à la forme qui demande le moins de portes.",
      { x: 5.55, y: 3.03, w: 3.8, h: 1.3, fontSize: 11.5 });
    life(s, 0.5, 4.55, 9.0, 1.0, [
      "Moins de CI : une carte plus petite et moins chère, moins de soudures, moins de pannes possibles.",
      "Dans un CPLD ou un FPGA (semaine 5), une équation plus courte occupe moins de ressources dans la puce.",
    ], 10.5);
  }

  // ============================== 4. LES TROIS LOIS
  {
    const s = slide("Les trois lois",
      "Partie A de la fiche 210 EX, A.1 : les apprenti·e·s complètent les lois au fur et à mesure.\n" +
      "Commutativité : l'ordre des entrées ne compte pas. Associativité : l'ordre des regroupements ne compte pas. Distributivité : comme en calcul, on peut développer ou mettre en évidence.\n" +
      "Faire remarquer : la distributivité dans le sens « mise en évidence » (de droite à gauche) est l'outil principal de la simplification (diapositive 14).");
    const rows = [[cell("Loi", H), cell("pour le OU (+)", H), cell("pour le ET (·)", H)],
      [cell("Commutativité", { bold: true, align: "left" }), cell(""), cell("")],
      [cell("Associativité", { bold: true, align: "left" }), cell(""), cell("")],
      [cell("Distributivité", { bold: true, align: "left" }), cell("", { colspan: 2 })]];
    s.addTable(rows, { x: 0.5, y: 0.95, w: 9.0, colW: [2.0, 3.5, 3.5], rowH: [0.38, 0.62, 0.62, 0.62], border: BORDER, fontSize: 12 });
    EQ(s, "eq_com1", 2.95, 1.43, 2.1, 0.42);
    EQ(s, "eq_com2", 6.45, 1.43, 2.1, 0.42);
    EQ(s, "eq_ass1", 2.75, 2.05, 3.05, 0.42);
    EQ(s, "eq_ass2", 6.2, 2.05, 3.05, 0.42);
    EQ(s, "eq_dis", 4.6, 2.67, 3.3, 0.42);
    txt(s, "« mise en évidence » quand on la lit de droite à gauche", { x: 2.6, y: 3.05, w: 6.8, h: 0.25, fontSize: 9.5, italic: true, color: GR, align: "center" });
    life(s, 0.5, 3.55, 9.0, 2.0, [
      "Commutativité : sur la carte, tu peux échanger les fils A et B d'une porte pour simplifier le routage.",
      "Associativité : un ET à 3 entrées (74HC11) peut être remplacé par deux ET à 2 entrées d'un 74HC08 déjà présent sur la carte.",
      "Distributivité : mettre A en évidence dans A · B + A · C économise une porte ET.",
    ]);
  }

  // ============================== 5. EXEMPLE TRAVAILLÉ : VÉRIFIER UNE LOI
  {
    const s = slide("Exemple travaillé : vérifier une loi avec la table de vérité",
      "Méthode générale (elle sert aussi de contrôle à chaque simplification) : une colonne par morceau de l'équation, puis on compare les deux colonnes finales ligne par ligne.\n" +
      "Ici, les colonnes A · (B + C) et A · B + A · C sont identiques sur les 8 lignes : la distributivité est vérifiée.\n" +
      "Entrées du poids fort au poids faible (C B A), lignes dans l'ordre du comptage binaire, comme en semaine 1.");
    const head = ["C", "B", "A", "B + C", "A · (B + C)", "A · B", "A · C", "A · B + A · C"].map(c => cell(c, Object.assign({}, H, { fontSize: 10.5 })));
    const rows = [head].concat(tdv(3).map(([c, b, a]) => {
      const l = a & (b | c), r = (a & b) | (a & c);
      return [c, b, a, b | c, l, a & b, a & c, r].map((v, j) => cell(v, { fontSize: 11, bold: j === 4 || j === 7, color: (j === 4 || j === 7) && v ? BLUE : K,
        fill: (j === 4 || j === 7) ? { color: TINT } : undefined }));
    }));
    s.addTable(rows, { x: 0.5, y: 0.95, w: 5.9, colW: [0.45, 0.45, 0.45, 0.8, 1.1, 0.75, 0.75, 1.15], rowH: 0.36, border: BORDER });
    frame(s, 6.6, 0.95, 2.9, 3.25);
    txt(s, "La méthode", { x: 6.75, y: 1.02, w: 2.6, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    bullets(s, ["toutes les combinaisons des entrées, dans l'ordre", "une colonne par morceau", "on compare les deux colonnes finales",
      "identiques sur toutes les lignes : l'égalité est vraie"], { x: 6.75, y: 1.38, w: 2.6, h: 2.75, fontSize: 11 }, true);
    card(s, 0.5, 4.35, 9.0, 1.2, NAVY);
    txt(s, [{ text: "Contrôle : ", options: { bold: true, color: LBLUE } },
      { text: "après chaque simplification, compare la table de vérité de départ et celle du résultat. Si elles sont identiques, la simplification est juste. Le contrôle écrit fait partie de l'évaluation.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 4.35, w: 8.6, h: 1.2, fontSize: 12, valign: "middle" });
  }

  // ============================== 6. RÈGLES 1 À 4 : AVEC 0 ET 1
  {
    const s = slide("Règles 1 à 4 : une entrée à 0 ou à 1",
      "Fiche 210 EX, A.2, règles 1 à 4. Les faire trouver par la classe avec la table de vérité du OU et du ET (présentation 120, diapositive 12).\n" +
      "Image à retenir : une entrée à 1 sur un ET laisse passer A ; une entrée à 0 sur un ET bloque la sortie à 0. Pour le OU, c'est l'inverse.\n" +
      "Lien avec la fiche 130 EX, N°4 c) : une entrée inutilisée se relie à un niveau fixe. Sur un ET, à VCC (règle 4) ; sur un OU, à GND (règle 1) : la porte garde sa fonction.");
    img(s, "fig_regles_01.png", 0.5, 0.95, 9.0, 1.85);
    ["r1", "r2", "r3", "r4"].forEach((k, i) => EQ(s, k, 0.75 + i * 2.25, 2.95, 1.6, 0.42));
    card(s, 0.5, 3.5, 4.4, 0.95);
    txt(s, [B("OU : "), N("une entrée à 0 ne change rien, une entrée à 1 force la sortie à 1.")], { x: 0.65, y: 3.5, w: 4.1, h: 0.95, fontSize: 11.5, valign: "middle" });
    card(s, 5.1, 3.5, 4.4, 0.95);
    txt(s, [B("ET : "), N("une entrée à 1 ne change rien, une entrée à 0 force la sortie à 0.")], { x: 5.25, y: 3.5, w: 4.1, h: 0.95, fontSize: 11.5, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, [
      "Validation : un ET laisse passer la commande de la vanne seulement si l'autorisation vaut 1.",
      "Entrée inutilisée (fiche 130 EX, N°4) : à VCC sur un ET, à GND sur un OU.",
    ], 10.5);
  }

  // ============================== 7. RÈGLES 5 À 9 : A AVEC LUI-MÊME OU SON INVERSE
  {
    const s = slide("Règles 5 à 9 : A avec lui-même ou avec son inverse",
      "Fiche 210 EX, A.2, règles 5 à 9. Vérification immédiate : A vaut 0 ou 1, on essaie les deux valeurs.\n" +
      "Règles 6 et 8 : A et Ā ne valent jamais 1 en même temps, et l'un des deux vaut toujours 1.\n" +
      "Règle 9 : deux inverseurs en série ne changent pas la fonction logique.");
    img(s, "fig_regles_aa.png", 0.5, 0.95, 9.0, 1.85);
    ["r5", "r6", "r7", "r8"].forEach((k, i) => EQ(s, k, 0.75 + i * 2.25, 2.95, 1.6, 0.42));
    frame(s, 0.5, 3.5, 4.4, 0.95);
    txt(s, "Règle 9", { x: 0.65, y: 3.55, w: 2.4, h: 0.3, fontSize: 12, bold: true, color: BLUE });
    EQ(s, "r9", 3.2, 3.6, 1.45, 0.75);
    txt(s, "Double négation : deux barres s'annulent.", { x: 0.65, y: 3.88, w: 2.4, h: 0.5, fontSize: 11 });
    card(s, 5.1, 3.5, 4.4, 0.95);
    txt(s, [B("A et Ā : "), N("jamais 1 en même temps, et toujours l'un des deux à 1.")], { x: 5.25, y: 3.5, w: 4.1, h: 0.95, fontSize: 11.5, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, [
      "Un capteur câblé deux fois sur la même porte ne change rien (règles 5 et 7) : c'est souvent une erreur de schéma.",
      "Deux inverseurs en série servent à remettre en forme un signal sans changer la logique (règle 9).",
    ], 10.5);
  }

  // ============================== 8. RÈGLES 10 À 12 : L'ABSORPTION
  {
    const s = slide("Règles 10 à 12 : l'absorption",
      "Fiche 210 EX, A.2, règles 10 à 12. Ce sont les règles qui simplifient le plus.\n" +
      "Démonstration de la règle 10 avec la classe : mise en évidence, puis règles 2 et 4. Règle 11 : on écrit A = A + A · B (règle 10), puis mise en évidence de B, puis règles 6 et 4.\n" +
      "Règle 12 : démonstration par la table de vérité dans la fiche 210 EX, N°1.\n" +
      "Important : A et B peuvent être n'importe quelle expression. Exemple : B̄ + B · C = B̄ + C (règle 11 avec B̄ à la place de A, puis règle 9).");
    [["10", "r10", "d10"], ["11", "r11", null], ["12", "r12", null]].forEach(([n, r, d], i) => {
      const y = 0.95 + i * 0.62;
      badge(s, 0.5, y + 0.08, n, 0.38);
      EQ(s, r, 1.05, y + 0.06, 2.9, 0.42);
    });
    frame(s, 4.2, 0.95, 5.3, 2.75);
    txt(s, "Pourquoi c'est vrai ?", { x: 4.35, y: 1.02, w: 5.0, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, "Règle 10 :", { x: 4.35, y: 1.4, w: 1.2, h: 0.35, fontSize: 11, bold: true, valign: "middle" });
    EQ(s, "d10", 4.4, 1.75, 4.9, 0.4);
    txt(s, "Règle 11 :", { x: 4.35, y: 2.25, w: 1.2, h: 0.35, fontSize: 11, bold: true, valign: "middle" });
    EQ(s, "d11a", 4.4, 2.6, 4.1, 0.4);
    EQ(s, "d11b", 4.4, 3.05, 4.5, 0.4);
    txt(s, "Règle 12 : tu la vérifies dans la fiche 210 EX, N°1.", { x: 0.5, y: 2.95, w: 3.5, h: 0.5, fontSize: 10.5, italic: true, color: GR });
    card(s, 0.5, 3.85, 9.0, 0.75, NAVY);
    txt(s, [{ text: "Astuce : ", options: { bold: true, color: LBLUE } },
      { text: "dans les règles, A et B peuvent remplacer n'importe quelle expression. Exemple : B̄ + B · C = B̄ + C (règle 11).", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 3.85, w: 8.6, h: 0.75, fontSize: 12, valign: "middle" });
    life(s, 0.5, 4.72, 9.0, 0.83, [
      "Règle 10 sur la ligne : « vanne ouverte, ou vanne ouverte et bouteille présente » revient à « vanne ouverte ». La deuxième condition n'apporte rien.",
    ], 10.5);
  }

  // ============================== 9. À TOI
  {
    const s = slide("À toi : simplifie et nomme les règles",
      "5 min, seul·e puis comparaison avec le voisin. Pour chaque étape, noter le numéro de la règle ou le nom de la loi. Correction : diapositive 10.\n" +
      "Aide pour 1) : mettre A en évidence. Aide pour 3) : chercher la forme d'une règle de la diapositive 8.");
    [["1", "e1"], ["2", "e2"], ["3", "e3"]].forEach(([n, k], i) => {
      const y = 1.0 + i * 0.95;
      frame(s, 0.5, y, 9.0, 0.8);
      badge(s, 0.65, y + 0.2, n, 0.4);
      EQ(s, k, 1.25, y + 0.17, 3.0, 0.46);
      txt(s, "= …", { x: 4.6, y: y + 0.17, w: 1.0, h: 0.46, fontSize: 16, color: GR, valign: "middle" });
      txt(s, "règle(s) : …", { x: 6.5, y: y + 0.17, w: 2.8, h: 0.46, fontSize: 12, color: GR, valign: "middle" });
    });
    life(s, 0.5, 4.2, 9.0, 1.35, [
      "Dans le 3), S : la pompe d'appoint peut tourner · B : niveau suffisant dans la cuve · C : vanne d'appoint ouverte.",
      "Dans les programmes d'automate, ces simplifications se font à la main avant d'écrire le code : moins de conditions, moins d'erreurs.",
    ]);
    txt(s, "Indice : dans 1), mets A en évidence ; dans 3), compare avec les règles de la diapositive 8.", { x: 0.5, y: 3.78, w: 9.0, h: 0.3, fontSize: 10.5, italic: true, color: GR });
  }

  // ============================== 10. CORRECTION
  {
    const s = slide("Correction",
      "1) Distributivité (mise en évidence de A), règle 6, règle 4. 2) Règle 9, règle 4, règle 1. 3) Règle 11 avec B à la place de A et C à la place de B.\n" +
      "Faire contrôler une des réponses par la table de vérité (2 entrées : 4 lignes).");
    [["1", "s1", "distributivité, règles 6 et 4"], ["2", "s2", "règles 9, 4 et 1"], ["3", "s3", "règle 11"]].forEach(([n, k, r], i) => {
      const y = 1.0 + i * 0.95;
      card(s, 0.5, y, 9.0, 0.8);
      badge(s, 0.65, y + 0.2, n, 0.4);
      EQ(s, k, 1.25, y + 0.17, 4.3, 0.46, 2000);
      txt(s, r, { x: 6.2, y: y + 0.17, w: 3.15, h: 0.46, fontSize: 12, bold: true, color: BLUE, valign: "middle" });
    });
    card(s, 0.5, 4.0, 9.0, 1.55, NAVY);
    txt(s, [{ text: "Réflexe : ", options: { bold: true, color: LBLUE } },
      { text: "avant de chercher une règle, regarde si une variable est commune à tous les termes. Si oui, mets-la en évidence (distributivité).", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 4.0, w: 8.6, h: 1.55, fontSize: 13, valign: "middle" });
  }

  // ============================== 11. THÉORÈME DE DE MORGAN
  {
    const s = slide("Le théorème de De Morgan",
      "Fiche 210 EX, A.3. Augustus De Morgan, mathématicien britannique (1806-1871).\n" +
      "Moyen mnémotechnique : on casse la barre et on change le signe (· devient +, + devient ·). Chaque variable garde sa propre barre.\n" +
      "Vérification par la table pour la première forme : les colonnes (A · B) barré et Ā + B̄ sont identiques. La seconde se vérifie de la même façon (fiche 210 EX, N°3).");
    frame(s, 0.5, 0.95, 4.3, 1.6);
    EQ(s, "dm1", 0.9, 1.1, 3.5, 0.55);
    EQ(s, "dm2", 0.9, 1.8, 3.5, 0.55);
    card(s, 0.5, 2.7, 4.3, 1.5);
    txt(s, "Casse la barre, change le signe", { x: 0.65, y: 2.78, w: 4.0, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    txt(s, "Le · devient +, le + devient ·, et chaque variable garde sa propre barre.", { x: 0.65, y: 3.15, w: 4.0, h: 0.95, fontSize: 12 });
    const head = ["B", "A", "A · B", OV("A · B"), "Ā", "B̄", "Ā + B̄"].map(c => cell(c, Object.assign({}, H, { fontSize: 10 })));
    const rows = [head].concat(tdv(2).map(([b, a]) => [b, a, a & b, 1 - (a & b), 1 - a, 1 - b, (1 - a) | (1 - b)].map((v, j) =>
      cell(v, { fontSize: 11, bold: j === 3 || j === 6, color: (j === 3 || j === 6) && v ? BLUE : K, fill: (j === 3 || j === 6) ? { color: TINT } : undefined }))));
    s.addTable(rows, { x: 5.0, y: 0.95, w: 4.5, colW: [0.45, 0.45, 0.6, 1.0, 0.5, 0.5, 1.0], rowH: 0.42, border: BORDER });
    txt(s, "Les deux colonnes en couleur sont identiques : la première forme est vraie.", { x: 5.0, y: 3.15, w: 4.5, h: 0.5, fontSize: 10.5, italic: true, color: GR });
    life(s, 0.5, 4.35, 9.0, 1.2, [
      "De Morgan explique pourquoi un capteur actif à 0 (contact qui s'ouvre) s'utilise aussi bien qu'un capteur actif à 1 : on déplace la barre.",
      "C'est l'outil qui permet de tout construire avec un seul type de porte (diapositive 13).",
    ]);
  }

  // ============================== 12. DE MORGAN SUR LA LIGNE : SYMBOLES ÉQUIVALENTS
  {
    const s = slide("De Morgan sur la ligne : symboles équivalents",
      "Retour sur la fiche 130 EX, N°5 (avec la convention de lettres de la semaine 2 : A et B sont les deux arrêts d'urgence, S l'autorisation) : le convoyeur n'est autorisé que si aucun des deux arrêts d'urgence n'est actionné. Les apprenti·e·s avaient choisi une NON-OU (74HC02).\n" +
      "Avec De Morgan : « U1 n'est pas actionné ET U2 n'est pas actionné » donne la même table que la NON-OU. Les deux dessins du bas sont la même porte.\n" +
      "À toi (réponse) : (Ā · B) barré = A + B̄ (De Morgan, puis règle 9). Correction en commun.");
    card(s, 0.5, 0.95, 9.0, 0.8);
    EQ(s, "dm_u", 0.8, 1.08, 4.2, 0.55);
    txt(s, [N("Arrêts d'urgence de la "), T130, N(", N°5 : A et B sont les arrêts d'urgence. La NON-OU dit la même chose que « ni A ni B ».")],
      { x: 5.15, y: 0.95, w: 4.25, h: 0.8, fontSize: 10.5, valign: "middle" });
    img(s, "fig_demorgan.png", 0.5, 1.9, 5.6, 2.6);
    frame(s, 6.3, 1.9, 3.2, 2.55);
    txt(s, "À toi", { x: 6.45, y: 1.97, w: 2.9, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, "Applique De Morgan, puis simplifie :", { x: 6.45, y: 2.3, w: 2.9, h: 0.5, fontSize: 11 });
    EQ(s, "e4", 6.55, 2.9, 2.0, 0.55);
    txt(s, "Réponse en commun.", { x: 6.45, y: 3.95, w: 2.9, h: 0.35, fontSize: 10, italic: true, color: GR });
    life(s, 0.5, 4.6, 9.0, 0.95, [
      "Un cercle à l'entrée d'un symbole CEI signale une entrée active à 0 : c'est la notation que tu verras sur les schémas des fiches techniques.",
    ], 10.5);
  }

  // ============================== 13. TOUT AVEC DES NON-ET
  {
    const s = slide("Tout avec des NON-ET : un seul CI, le 74HC00",
      "NON : on relie les deux entrées (A · A = A, règle 7, puis la barre). ET : une NON-ET suivie d'une NON-ET montée en inverseur (règle 9). OU : on inverse A et B, puis NON-ET ; avec De Morgan, (Ā · B̄) barré = A + B.\n" +
      "La NON-OU est aussi universelle (même raisonnement).\n" +
      "Faire le lien avec la question de départ : l'apprenti·e retrouvera dans la fiche 210 EX, N°4 et N°5, un circuit complet réalisé avec un seul 74HC00.");
    img(s, "fig_nand.png", 0.5, 0.95, 9.0, 2.5);
    card(s, 0.5, 3.6, 4.4, 0.9);
    txt(s, [B("NON-ET universelle : "), N("NON, ET et OU se construisent avec des NON-ET seulement.")], { x: 0.65, y: 3.6, w: 4.1, h: 0.9, fontSize: 11.5, valign: "middle" });
    card(s, 5.1, 3.6, 4.4, 0.9);
    txt(s, [B("Pour le OU : "), N("De Morgan donne " + OV("Ā · B̄") + " = A + B.")], { x: 5.25, y: 3.6, w: 4.1, h: 0.9, fontSize: 11.5, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, [
      "En production, on limite le nombre de références de CI : un seul type à commander et à stocker.",
      "Le 74HC00 contient quatre NON-ET : de quoi réaliser un petit circuit complet avec un seul boîtier.",
    ], 10.5);
  }

  // ============================== 14. LA MÉTHODE · RÉPONSE À LA QUESTION DE DÉPART
  {
    const s = slide("La méthode · réponse à la question de départ",
      "Étape 1 : une ligne du cahier des charges donne un terme (convoyeur : « en marche et bouteille pleine », ou « en marche, pas de bouteille pleine, et vidange »). Légende : A machine en marche, B bouteille pleine, C vidange, S convoyeur.\n" +
      "Étape 2 : A est commun aux deux termes, on le met en évidence. Étape 3 : règle 11 (B à la place de A, C à la place de B).\n" +
      "Étape 4, contrôle : avec C B A (A poids faible), les deux équations donnent S = 1 sur les mêmes lignes 011, 101 et 111, et 0 ailleurs.");
    [["1", "Écrire l'équation", "un terme par condition"], ["2", "Mettre en évidence", "la variable commune (distributivité)"],
     ["3", "Appliquer les règles", "noter la règle à chaque étape"], ["4", "Contrôler", "par la table de vérité"]].forEach(([n, t, d], i) => {
      const y = 0.95 + i * 0.62;
      badge(s, 0.5, y + 0.06, n, 0.38);
      txt(s, t, { x: 1.0, y, w: 3.2, h: 0.28, fontSize: 12, bold: true, valign: "middle" });
      txt(s, d, { x: 1.0, y: y + 0.27, w: 3.2, h: 0.26, fontSize: 10, color: GR, valign: "middle" });
    });
    frame(s, 4.4, 0.95, 5.1, 2.45);
    txt(s, "Le convoyeur de sortie S", { x: 4.55, y: 1.02, w: 4.8, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    [["m1", ""], ["m2", "distributivité"], ["m3", "règle 11"]].forEach(([k, r], i) => {
      const y = 1.4 + i * 0.62;
      EQ(s, k, 4.6, y, 3.0, 0.42);
      txt(s, r, { x: 7.75, y, w: 1.65, h: 0.42, fontSize: 10.5, italic: true, color: BLUE, valign: "middle" });
    });
    card(s, 0.5, 3.55, 9.0, 0.85);
    txt(s, [B("Contrôle : "), N("C B A = 011, 101 et 111 donnent S = 1 avec les deux équations, toutes les autres lignes donnent 0. Le fonctionnement est le même.")],
      { x: 0.65, y: 3.55, w: 8.7, h: 0.85, fontSize: 11.5, valign: "middle" });
    life(s, 0.5, 4.55, 9.0, 1.0, [
      "Le résultat se relit en français : le convoyeur tourne quand la machine est en marche et qu'il y a une bouteille pleine ou une vidange.",
      "Si la phrase simplifiée a du sens pour l'opérateur, c'est un deuxième contrôle.",
    ], 10.5);
  }

  // ============================== 15. DE L'ÉQUATION AU SCHÉMA
  {
    const s = slide("De l'équation au schéma",
      "Objectif LZ_2226 (C5) : développer et dessiner un circuit logique. On part de l'équation simplifiée et on dessine une porte par opération, en commençant par l'intérieur des parenthèses.\n" +
      "Avant : 4 portes, 4 CI (74HC04, 74HC08, 74HC11, 74HC32). Après : 2 portes, 2 CI (74HC32 et 74HC08), avec la même table de vérité.\n" +
      "Prolongement (fiche 210 EX, N°5) : en développant A · B + A · C et avec De Morgan, le convoyeur se câble avec trois NON-ET d'un seul 74HC00.");
    card(s, 0.5, 0.95, 4.4, 2.6);
    txt(s, "Avant : 4 portes, 4 CI", { x: 0.65, y: 1.0, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: GR });
    img(s, "fig_conv_avant.png", 0.7, 1.35, 4.0, 2.1);
    frame(s, 5.1, 0.95, 4.4, 2.6);
    txt(s, "Après : 2 portes, 2 CI", { x: 5.25, y: 1.0, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    img(s, "fig_conv_apres.png", 5.4, 1.45, 3.8, 1.85);
    txt(s, "Dessiner un schéma logique", { x: 0.5, y: 3.68, w: 9.0, h: 0.3, fontSize: 12.5, bold: true, color: NAVY });
    bullets(s, ["entrées à gauche, sortie à droite ; symboles CEI (rectangle et qualificatif) ;",
      "une porte par opération, en commençant par l'intérieur des parenthèses : ici B + C, puis le ET avec A ;",
      "une même variable peut alimenter plusieurs entrées : un point marque chaque dérivation."], { x: 0.5, y: 4.0, w: 9.0, h: 1.55, fontSize: 11.5 }, true);
  }

  // ============================== 16. À RETENIR · TICKET DE SORTIE
  {
    const s = slide("À retenir · ticket de sortie",
      "Ticket de sortie (5 min, seul·e, sans support). Réponses : 1) 1 (règle 2). 2) A (règle 10). 3) Ā · B̄ (De Morgan). 4) Elle montre que l'équation simplifiée donne la même sortie que l'équation de départ pour toutes les combinaisons des entrées.\n" +
      "Ensuite : fiche 210 EX, partie B.");
    [["Lois et règles", "3 lois, 12 règles : fiche 210 EX, partie A"], ["De Morgan", "casse la barre, change le signe"], ["Méthode", "écrire, mettre en évidence, règles, contrôler"]].forEach(([h, d], k) => {
      const x = 0.5 + k * 3.05;
      card(s, x, 0.95, 2.9, 1.2);
      txt(s, h, { x: x + 0.15, y: 1.02, w: 2.6, h: 0.35, fontSize: 13, bold: true, color: BLUE });
      txt(s, d, { x: x + 0.15, y: 1.4, w: 2.6, h: 0.7, fontSize: 11.5 });
    });
    frame(s, 0.5, 2.35, 9.0, 3.2);
    txt(s, "Ticket de sortie : seul·e, 5 minutes, sans support", { x: 0.65, y: 2.42, w: 8.7, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    [["1", "Que vaut A + 1 ?"], ["2", "Simplifie S = A + A · B."], ["3", "Écris " + OV("A + B") + " avec De Morgan."],
     ["4", "À quoi sert la table de vérité après une simplification ?"]].forEach((q, i) => {
      const x = 0.65 + (i % 2) * 4.45, y = 2.95 + Math.floor(i / 2) * 1.2;
      badge(s, x, y + 0.2, q[0], 0.36);
      txt(s, q[1], { x: x + 0.48, y, w: 3.8, h: 0.8, fontSize: 12.5, valign: "middle" });
    });
  }

  // ============================== 17. EXERCICES
  exoSlide("210 EX", DATA.TEAMS["210"], [
    ["1", "Vérifier une règle par la table", "≈ 8 min · diapositive 5"], ["2", "Simplifier avec les règles", "≈ 10 min · diapositives 6 à 10"],
    ["3", "De Morgan", "≈ 8 min · diapositives 11 et 12"], ["4", "Le voyant « défaut remplissage »", "≈ 14 min · diapositives 13 à 15"],
    ["5", "Le convoyeur en NON-ET", "≈ 5 min · diapositives 11 et 13"]],
    "Sur la ligne de remplissage, tu reprends des commandes écrites telles que le cahier des charges les décrit, et tu les simplifies avant de les câbler.",
    "En binôme, 45 min. Pour chaque simplification : une étape par ligne, la règle à côté, puis le contrôle par la table de vérité.",
    ["C'est le travail d'un électronicien de développement : un circuit plus simple coûte moins cher et tombe moins souvent en panne."],
    "Fiche 210 EX Algèbre de Boole, partie B (45 min). Temps indicatifs : N°1 8 min, N°2 10 min, N°3 8 min, N°4 14 min, N°5 5 min.\n" +
    "Corrigé : 210 EX C Algèbre de Boole (pour l'enseignant·e).");

  // ============================== 18. PAGE INTERACTIVE
  pageSlide("201", DATA.FILES["201"], DATA.TEAMS["201"], DATA.ART["201"], "shot_201.png",
    ["Les lois et les règles, en portes", "Simplifier pas à pas : choisir la règle", "De Morgan : casser la barre", "Contrôle automatique par la table de vérité"],
    ["Pour réviser à la maison ou rattraper une absence : la page reprend les règles et les exercices de la présentation."],
    "Page interactive 201 : à ouvrir dans Edge ou Chrome. Chaque étape a une partie « Comprendre » et une partie « À toi » corrigée tout de suite.");

  // ============================== 19. ANIMATION
  videoSlide("205", DATA.FILES["205"], DATA.TEAMS["205"], "cover_205.png", "3 min 52", [
    ["Les règles en portes", "une entrée à 0 ou à 1"], ["De Morgan", "casser la barre, changer le signe"],
    ["Le convoyeur", "simplifier, contrôler, dessiner"]],
    ["La vidéo reprend la leçon avec la même ligne de remplissage : pour réviser ou rattraper une absence."],
    "Animation 205 : 3 min 52, trois démonstrations, une introduction et un récapitulatif.");
};
