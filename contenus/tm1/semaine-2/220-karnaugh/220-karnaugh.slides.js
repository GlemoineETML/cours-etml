// 220 Simplification par Karnaugh : diapositives (moteur : moteur/deck.js).
// Fil rouge : ligne de remplissage de boissons (situation de travail FutureMEM du champ LFB_El_DT1). Champ LFB_El_DT1 : LZ_2225 (C3).
// Convention (REGLES 3.4) : sortie S, entrées A, B, C, D avec une légende. A poids faible ; combinaison k = 8·D + 4·C + 2·B + A.
// Tableau sur le modèle de Gaël (11/24/2026) : codes BA et DC, zones jaunes A en haut, B en bas, C à gauche, D à droite ; chaque groupe relié à son terme par un trait.
// Prérequis : présentation 200. Le code Gray n'est vu qu'en semaine 4 : on parle ici de « cases voisines ».
// Va avec la fiche 230 EX Simplification par Karnaugh. Pas de lien Floyd ni nextecmedia.
module.exports = function (E) {
  const { pres, DATA, NAVY, BLUE, LBLUE, TINT, K, GR, RED, F, slide, txt, card, frame, badge, img, bullets, life,
    boxTitle, cell, H, BORDER, LINK, LZL, exoSlide, pageSlide, videoSlide, eqImg, titreSlide } = E;
  const EQS = require("./equations.json");
  const EQ = (s, k, x, y, w, maxH, sz, color) => eqImg(s, k + ".png", EQS[k], x, y, w, maxH, sz || 2000, color);
  const T200 = LINK("présentation 200", DATA.TEAMS["200"], "Présentation 200 Algèbre de Boole");
  const T130 = LINK("fiche 130 EX", DATA.TEAMS["130"], "Fiche 130 EX Portes logiques de base");
  const B = (t) => ({ text: t, options: { bold: true } });
  const N = (t) => ({ text: t });
  const LZ = () => LZL("LZ_2225");
  const RINC = [0, 0, 1, 1, 0, 1, 1, 1];   // buse de rinçage, k = 4·C + 2·B + A

  // ============================== 1. TITRE
  titreSlide({
    titre: "Simplification\npar Karnaugh",
    sousTitre: "Trouver la plus courte équation en regroupant des cases",
    objectifs: [
      [N("écrire la somme de produits d'une table ("), LZ(), N(") ;")],
      [N("remplir un tableau à 3 ou 4 variables ("), LZ(), N(") ;")],
      [N("regrouper les 1 et lire l'équation simplifiée ("), LZ(), N(") ;")],
      [N("utiliser les cas indifférents X ("), LZ(), N(").")]],
    question: "Sur une ancienne machine de la ligne, on a relevé au banc la table de vérité de la buse de rinçage. Elle a cinq lignes à 1. Quelle est l'équation la plus courte pour la refaire avec des portes ?",
    indice: "Écris ton idée. Réponse à la diapositive 7.",
    references: [LZ(), T200],
    notes: "Durée : 2 périodes. Présentation ≈ 45 min, puis fiche 230 EX (45 min).\n" +
      "Déroulement : 2 somme de produits ; 3 et 4 le tableau à zones ; 5 et 6 regrouper et lire ; 7 exemple travaillé (réponse) ; 8 et 9 quatre variables ; 10 et 11 à toi ; 12 cas indifférents ; 13 retour au convoyeur de la présentation 200 ; 14 ticket de sortie ; 15 à 17 fiche, page 221, animation 225.\n" +
      "Prérequis : présentation 200 (règles, méthode, contrôle par la table). Convention : sortie S, entrées A, B, C, D, A poids faible.\n" +
      "Légende de la buse : S buse ouverte, A machine en marche, B bouteille sale détectée, C cycle de nettoyage demandé. Réponse : S = B + A · C.",
  });

  // ============================== 2. DE LA TABLE À LA SOMME DE PRODUITS
  {
    const s = slide("De la table à l'équation : la somme de produits",
      "Rappel de la fiche 130 EX, N°1 : une ligne à 1 donne un produit (ET) de toutes les entrées, avec une barre sur celles qui valent 0. Nouveau : plusieurs lignes à 1, on additionne (OU) les produits.\n" +
      "Ligne C B A = 010 : C = 0, B = 1, A = 0, donc Ā · B · C̄. Faire écrire la ligne 011 par la classe.\n" +
      "Le résultat est juste mais long : 5 produits de 3 variables. La présentation 200 permettrait de le simplifier, mais c'est long et on peut se tromper. Karnaugh fait la même chose en dessinant.");
    const head = ["C", "B", "A", "S", "produit"].map(c => cell(c, H));
    const rows = [head];
    const PROD = { 2: "Ā · B · C̄", 3: "A · B · C̄", 5: "A · B̄ · C", 6: "Ā · B · C", 7: "A · B · C" };
    for (let k = 0; k < 8; k++) {
      const c = (k >> 2) & 1, b = (k >> 1) & 1, a = k & 1;
      rows.push([c, b, a, RINC[k], PROD[k] || ""].map((v, j) => cell(v, { fontSize: 11.5, bold: j === 3 && v === 1, color: j === 3 && v === 1 ? BLUE : K, align: j === 4 ? "left" : "center" })));
    }
    s.addTable(rows, { x: 0.5, y: 0.95, w: 4.0, colW: [0.5, 0.5, 0.5, 0.6, 1.9], rowH: 0.33, border: BORDER });
    frame(s, 4.7, 0.95, 4.8, 1.45);
    txt(s, "Une ligne à 1 = un produit", { x: 4.85, y: 1.02, w: 4.5, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, "ET de toutes les entrées ; une barre sur celles qui valent 0. Les produits s'additionnent (OU).", { x: 4.85, y: 1.38, w: 4.5, h: 0.95, fontSize: 11.5 });
    card(s, 4.7, 2.55, 4.8, 1.0);
    EQ(s, "eq_sdp1", 4.8, 2.63, 4.6, 0.38, 1600);
    EQ(s, "eq_sdp2", 4.8, 3.05, 4.6, 0.38, 1600);
    txt(s, [N("Juste, mais 5 produits. Rappel : "), T130, N(", N°1.")], { x: 4.7, y: 3.6, w: 4.8, h: 0.35, fontSize: 10.5, italic: true, color: GR });
    life(s, 4.7, 4.05, 4.8, 1.5, ["S : buse de rinçage ouverte · A : machine en marche · B : bouteille sale détectée · C : cycle de nettoyage demandé."], 10.5);
  }

  // ============================== 3. LE TABLEAU DE KARNAUGH
  {
    const s = slide("Le tableau de Karnaugh : une case par ligne de la table",
      "Le tableau a autant de cases que la table a de lignes : 8 pour 3 variables, 16 pour 4. Le chiffre gris de chaque case est le numéro de la ligne (combinaison) : k = 8 · D + 4 · C + 2 · B + A.\n" +
      "Chaque variable a sa zone jaune : A en haut, B en bas, C à gauche, D à droite. Elle vaut 1 dans les colonnes ou les lignes de sa zone, 0 ailleurs. Les codes gris le disent aussi : colonne 01 → B = 0, A = 1. Ordre 00, 01, 11, 10 : entre deux cases voisines, une seule variable change, même entre le bord gauche et le bord droit. On reverra cet ordre en semaine 4.");
    img(s, "k_idx3.png", 0.5, 1.0, 4.2, 2.3);
    img(s, "k_idx4.png", 5.2, 0.95, 3.4, 3.4);
    card(s, 0.5, 3.45, 4.4, 1.0);
    txt(s, [B("Une zone par variable : "), N("A en haut, B en bas, C à gauche, D à droite. La variable vaut 1 dans sa zone, 0 ailleurs.")], { x: 0.65, y: 3.45, w: 4.1, h: 1.0, fontSize: 12, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, [
      "Les zones se chevauchent à moitié : entre deux cases voisines, une seule variable change (codes 00, 01, 11, 10).",
      "Les bords se touchent : la première colonne est voisine de la dernière, la première ligne de la dernière.",
    ], 10.5);
  }

  // ============================== 4. REMPLIR LE TABLEAU
  {
    const s = slide("Remplir le tableau",
      "On reporte chaque ligne de la table dans sa case. Méthode sûre : chercher la case avec les zones ou les codes (ligne C, colonne BA), pas en comptant les cases.\n" +
      "Erreur fréquente : remplir les cases dans l'ordre de la table, de gauche à droite. Les 1 se retrouvent au mauvais endroit et les regroupements sont faux.");
    const head = ["C", "B", "A", "S"].map(c => cell(c, H));
    const rows = [head];
    for (let k = 0; k < 8; k++) rows.push([(k >> 2) & 1, (k >> 1) & 1, k & 1, RINC[k]].map((v, j) => cell(v, { fontSize: 11.5, bold: j === 3 && v === 1, color: j === 3 && v === 1 ? BLUE : K })));
    s.addTable(rows, { x: 0.5, y: 0.95, w: 2.4, colW: [0.6, 0.6, 0.6, 0.6], rowH: 0.36, border: BORDER });
    txt(s, "→", { x: 3.0, y: 1.9, w: 0.5, h: 0.5, fontSize: 30, bold: true, color: BLUE, align: "center" });
    img(s, "k_rinc_v.png", 3.6, 1.0, 4.6, 2.5);
    card(s, 3.6, 3.65, 5.9, 0.75);
    txt(s, [B("Repère : "), N("C = 1, B = 0, A = 1 : ligne 1, colonne 01 ; dans les zones C et A, hors de la zone B (k = 5).")], { x: 3.75, y: 3.65, w: 5.6, h: 0.75, fontSize: 12, valign: "middle" });
    life(s, 0.5, 4.55, 9.0, 1.0, ["Erreur à éviter : remplir les cases dans l'ordre de la table, de gauche à droite. Les 1 tombent au mauvais endroit et les regroupements sont faux."], 10.5);
  }

  // ============================== 5. REGROUPER LES 1
  {
    const s = slide("Regrouper les 1 : les règles",
      "Les groupes sont des rectangles de 1, 2, 4, 8 ou 16 cases (une puissance de 2). On les fait les plus grands possible, et le moins nombreux possible. Chaque 1 doit être dans au moins un groupe ; un 1 peut servir deux fois.\n" +
      "Les bords se touchent : un groupe peut passer d'un bord à l'autre (diapositives 8 et 9). Jamais de 0 dans un groupe. Chaque groupe est relié à son terme par un trait.");
    img(s, "k_rinc.png", 0.5, 1.0, 4.4, 2.4);
    boxTitle(s, 5.1, 0.95, 4.4, 3.4, "Les règles", [
      "rectangles de 1, 2, 4, 8 cases (jamais 3 ou 6) ;",
      "les plus grands possible ;",
      "le moins de groupes possible ;",
      "chaque 1 dans au moins un groupe ; un 1 peut servir deux fois ;",
      "jamais de 0 dans un groupe ; les bords se touchent."], 11.5, true);
    card(s, 0.5, 3.55, 4.4, 0.8);
    txt(s, [B("Ici : "), N("un groupe de 4 (vert) et un groupe de 2 (rouge). Le 1 de la case 111 sert deux fois.")], { x: 0.65, y: 3.55, w: 4.1, h: 0.8, fontSize: 11.5, valign: "middle" });
    life(s, 0.5, 4.5, 9.0, 1.05, ["Plus un groupe est grand, plus son terme est court : un groupe de 4 cases dans un tableau à 3 variables ne garde qu'une variable."], 10.5);
  }

  // ============================== 6. LIRE UN GROUPE
  {
    const s = slide("Lire un groupe : garder ce qui ne change pas",
      "Pour chaque groupe et chaque variable : groupe entièrement dans la zone de la variable → on écrit la variable ; entièrement hors de sa zone → la variable barrée ; à cheval sur le bord de la zone → elle disparaît.\n" +
      "Groupe vert (cases 010, 011, 110, 111) : à cheval sur C et sur A, entièrement dans la zone B → B. Groupe rouge (101, 111) : dans les zones C et A, à cheval sur B → A · C.\n" +
      "Lien avec la présentation 200 : c'est la règle 6 (B + B̄ = 1) appliquée automatiquement.");
    img(s, "k_rinc.png", 0.5, 1.0, 4.4, 2.4);
    const rows = [[cell("Groupe", H), cell("C", H), cell("B", H), cell("A", H), cell("terme", H)],
      [cell("vert", { bold: true, color: "1E8C46" }), cell("à cheval"), cell("dans", { bold: true }), cell("à cheval"), cell("")],
      [cell("rouge", { bold: true, color: RED }), cell("dans", { bold: true }), cell("à cheval"), cell("dans", { bold: true }), cell("")]];
    s.addTable(rows, { x: 5.1, y: 1.0, w: 4.4, colW: [0.9, 0.85, 0.85, 0.85, 0.95], rowH: 0.5, border: BORDER, fontSize: 11.5 });
    EQ(s, "eq_g1", 8.75, 1.58, 0.35, 0.35);
    EQ(s, "eq_g2", 8.62, 2.08, 0.75, 0.35);
    card(s, 5.1, 2.7, 4.4, 1.0, NAVY);
    txt(s, [{ text: "Règle : ", options: { bold: true, color: LBLUE } }, { text: "dans la zone → la variable ; hors de la zone → barrée ; à cheval → elle disparaît.", options: { color: "FFFFFF" } }],
      { x: 5.25, y: 2.7, w: 4.1, h: 1.0, fontSize: 12.5, valign: "middle" });
    life(s, 0.5, 3.85, 9.0, 1.7, [
      "C'est la règle 6 de la présentation 200 faite en dessinant : B + B̄ = 1, la variable à cheval disparaît.",
      "Un groupe de 2 cases supprime 1 variable, un groupe de 4 en supprime 2, un groupe de 8 en supprime 3.",
    ]);
  }

  // ============================== 7. EXEMPLE TRAVAILLÉ : LA BUSE DE RINÇAGE
  {
    const s = slide("Exemple travaillé : la buse de rinçage",
      "Réponse à la question de départ. On additionne les termes des groupes : S = B + A · C. 5 produits de 3 variables deviennent une porte ET et une porte OU.\n" +
      "Contrôle : avec la table, S = 1 sur les lignes 010, 011, 101, 110, 111. B + A · C donne 1 pour B = 1 (010, 011, 110, 111) et pour A = C = 1 (101, 111) : les mêmes lignes.\n" +
      "Relecture : la buse s'ouvre dès qu'une bouteille sale est détectée, ou quand la machine est en marche et qu'un nettoyage est demandé.");
    [["1", "Remplir le tableau"], ["2", "Regrouper"], ["3", "Lire chaque groupe"], ["4", "Additionner"], ["5", "Contrôler"]].forEach(([n, t], i) => {
      const y = 0.98 + i * 0.5;
      badge(s, 0.5, y, n, 0.34);
      txt(s, t, { x: 0.95, y, w: 2.3, h: 0.34, fontSize: 12, bold: true, valign: "middle" });
    });
    img(s, "k_rinc.png", 3.2, 0.95, 3.3, 1.8);
    frame(s, 6.7, 0.95, 2.8, 1.8);
    txt(s, "Résultat", { x: 6.85, y: 1.0, w: 2.5, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    EQ(s, "eq_rinc", 6.9, 1.45, 2.3, 0.55, 2400);
    txt(s, "5 produits → 2 portes", { x: 6.85, y: 2.2, w: 2.5, h: 0.4, fontSize: 11.5, bold: true });
    img(s, "fig_rinceuse.png", 3.4, 3.0, 3.2, 1.45);
    card(s, 6.7, 3.0, 2.8, 1.45);
    txt(s, [B("Contrôle : "), N("S = 1 sur les mêmes lignes que la table (010, 011, 101, 110, 111).")], { x: 6.85, y: 3.0, w: 2.5, h: 1.45, fontSize: 11, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, ["Relecture : la buse s'ouvre dès qu'une bouteille sale est détectée, ou quand la machine est en marche et qu'un nettoyage est demandé."], 10.5);
  }

  // ============================== 8. QUATRE VARIABLES
  {
    const s = slide("Quatre variables : les quatre coins se touchent",
      "Tableau 4 × 4 : zones A en haut, B en bas, C à gauche, D à droite. Le haut touche le bas, la gauche touche la droite : les quatre coins forment un seul groupe.\n" +
      "Coins (0, 2, 8, 10) : A = 0 et C = 0 partout, B et D changent → Ā · C̄. Centre (5, 7, 13, 15) : A = 1 et C = 1 → A · C. S = Ā · C̄ + A · C : B et D n'interviennent pas.");
    img(s, "k_k4.png", 0.5, 0.95, 3.7, 3.55);
    boxTitle(s, 4.5, 0.95, 5.0, 1.8, "Ce qui change avec 4 variables", [
      "16 cases : A en haut, B en bas, C à gauche, D à droite ;",
      "le haut touche le bas, la gauche touche la droite ;",
      "les quatre coins forment un groupe de 4."], 11.5, true);
    card(s, 4.5, 2.9, 5.0, 1.6);
    txt(s, "Lecture", { x: 4.65, y: 2.97, w: 4.7, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    EQ(s, "eq_k4", 4.7, 3.35, 3.5, 0.5);
    txt(s, "Les deux groupes sont à cheval sur B et sur D : ils disparaissent.", { x: 4.65, y: 3.95, w: 4.7, h: 0.5, fontSize: 11 });
    life(s, 0.5, 4.65, 9.0, 0.9, ["Karnaugh montre aussi les entrées qui ne servent à rien : ici, deux capteurs sur quatre peuvent être débranchés."], 10.5);
  }

  // ============================== 9. EXEMPLE TRAVAILLÉ À 4 VARIABLES : L'ÉJECTEUR
  {
    const s = slide("Exemple travaillé à 4 variables : l'éjecteur",
      "Contrôle qualité en fin de ligne. Légende : S éjecteur (la bouteille est retirée), A bouchon présent, B étiquette présente, C niveau correct, D mode réglage.\n" +
      "Cahier des charges : en production (D = 0), on retire toute bouteille qui a un défaut ; en mode réglage (D = 1), on ne retire que les bouteilles sans bouchon. Table : 11 lignes à 1 sur 16.\n" +
      "Groupe vert de 8 : les deux colonnes hors de la zone A, qui se touchent par les bords → Ā. Rouge : hors de B, hors de D → B̄ · D̄. Bleu : la première ligne, hors de C et hors de D → C̄ · D̄. S = Ā + B̄ · D̄ + C̄ · D̄.\n" +
      "Contrôle : 8 + 2 + 1 = 11 cases à 1, comme dans la table (les cases communes ne comptent qu'une fois).");
    img(s, "k_ejec.png", 0.5, 0.95, 5.2, 3.5);
    frame(s, 5.9, 0.95, 3.6, 1.45);
    txt(s, "Résultat", { x: 6.05, y: 1.0, w: 3.3, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    EQ(s, "eq_ejec", 6.05, 1.45, 3.3, 0.55);
    card(s, 5.9, 2.55, 3.6, 1.9);
    txt(s, [B("Le groupe de 8 : "), N("les deux colonnes hors de la zone A se touchent par les bords."), { text: "", options: { breakLine: true } },
      B("Contrôle : "), N("11 cases à 1, comme dans la table.")], { x: 6.05, y: 2.6, w: 3.3, h: 1.8, fontSize: 11, valign: "middle", paraSpaceAfter: 4 });
    life(s, 0.5, 4.6, 9.0, 0.95, ["S : éjecteur · A : bouchon présent · B : étiquette présente · C : niveau correct · D : mode réglage. En réglage, seul le bouchon manquant fait retirer la bouteille."], 10.5);
  }

  // ============================== 10. À TOI
  {
    const s = slide("À toi : regroupe et lis l'équation",
      "6 min, seul·e puis comparaison avec le voisin. Correction : diapositive 11.\n" +
      "Aide : commencer par le plus grand groupe possible. Dans 3), penser que la ligne D C = 00 forme un groupe de 4.");
    ["t1", "t2"].forEach((k, i) => {
      const x = 0.5 + i * 3.05;
      badge(s, x, 1.0, String(i + 1), 0.34);
      img(s, `k_${k}_v.png`, x + 0.4, 0.95, 2.5, 1.5);
    });
    badge(s, 6.6, 1.0, "3", 0.34);
    img(s, "k_t3_v.png", 6.95, 0.95, 2.55, 2.5);
    card(s, 0.5, 2.8, 5.9, 1.3);
    txt(s, [B("Pour chaque tableau : "), N("dessine les groupes, lis chaque groupe, puis écris S."), { text: "", options: { breakLine: true } },
      N("Commence toujours par le plus grand groupe possible.")], { x: 0.65, y: 2.8, w: 5.6, h: 1.3, fontSize: 12, valign: "middle" });
    life(s, 0.5, 4.3, 9.0, 1.25, ["Sur la fiche 230 EX, tu rempliras toi-même les tableaux à partir des tables de vérité."], 10.5);
  }

  // ============================== 11. CORRECTION
  {
    const s = slide("Correction",
      "1) Un groupe de 4 hors de la zone B → B̄. 2) Deux groupes de 2 qui partagent la case 111 : A · B et B · C. 3) La première ligne (hors de C, hors de D, groupe de 4) donne C̄ · D̄ ; le groupe vertical 5, 13 donne A · B̄ · C.\n" +
      "Faire contrôler une réponse en relisant les cases à 1.");
    [["t1", "eq_t1"], ["t2", "eq_t2"], ["t3", "eq_t3"]].forEach(([k, e], i) => {
      const x = 0.5 + i * 3.05;
      img(s, `k_${k}.png`, x, 0.95, 2.9, 2.45);
      EQ(s, e, x + 0.1, 3.45, 2.7, 0.45);
    });
    card(s, 0.5, 4.05, 9.0, 0.45, NAVY);
    txt(s, [{ text: "Réflexe : ", options: { bold: true, color: LBLUE } }, { text: "le plus grand groupe d'abord, puis les 1 restants.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 4.05, w: 8.6, h: 0.45, fontSize: 12.5, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, ["Un 1 isolé reste un groupe de 1 : son terme garde toutes les variables."], 10.5);
  }

  // ============================== 12. LES CAS INDIFFÉRENTS
  {
    const s = slide("Les cas indifférents X",
      "Certaines combinaisons ne peuvent pas arriver : le capteur haut (C) ne peut pas être mouillé si le capteur bas (B) est sec. Dans la table, on écrit X : la sortie peut valoir 0 ou 1, peu importe.\n" +
      "Dans le tableau, on compte un X comme 1 s'il agrandit un groupe, sinon on l'ignore. Ici, avec les X : S = C + Ā · B. Sans les X : S = B · C + Ā · B, un terme plus long.\n" +
      "Légende : S pompe de vidange, A machine en marche, B capteur bas mouillé, C capteur haut mouillé. La pompe vide si le niveau haut est atteint, ou si la machine est arrêtée et qu'il reste du liquide.");
    img(s, "k_vid0.png", 0.5, 1.0, 3.0, 1.65);
    EQ(s, "eq_sx", 0.6, 2.75, 2.8, 0.45);
    txt(s, "sans les X", { x: 0.5, y: 3.25, w: 3.0, h: 0.3, fontSize: 11, italic: true, color: GR, align: "center" });
    img(s, "k_vid.png", 3.8, 1.0, 3.0, 1.65);
    EQ(s, "eq_x", 3.95, 2.75, 2.6, 0.45);
    txt(s, "avec les X", { x: 3.8, y: 3.25, w: 3.0, h: 0.3, fontSize: 11, italic: true, color: BLUE, align: "center", bold: true });
    boxTitle(s, 7.0, 0.95, 2.5, 2.65, "Un X", ["combinaison impossible ;", "compte comme 1 s'il agrandit un groupe ;", "sinon on l'ignore."], 11, true);
    life(s, 0.5, 3.75, 9.0, 1.8, [
      "Pompe de vidange : S pompe en marche, A machine en marche, B capteur bas mouillé, C capteur haut mouillé.",
      "Le capteur haut ne peut pas être mouillé si le capteur bas est sec : les combinaisons C = 1, B = 0 sont des X.",
      "On retrouve des X partout où des capteurs sont liés : fins de course, niveaux, codes qui n'existent pas.",
    ], 10.5);
  }

  // ============================== 13. KARNAUGH OU ALGÈBRE ?
  {
    const s = slide("Karnaugh ou algèbre : le même résultat",
      "Retour au convoyeur de la présentation 200 : S = A · B + A · B̄ · C. Les 1 sont en 011, 101 et 111. Deux groupes de 2 : A · B et A · C. Avec la distributivité, A · B + A · C = A · (B + C) : le même résultat que l'algèbre.\n" +
      "Quand choisir ? L'algèbre pour une équation courte ou pour mettre en évidence. Karnaugh dès qu'on part d'une table de vérité, jusqu'à 4 variables.");
    img(s, "k_conv.png", 0.5, 0.95, 3.6, 2.15);
    card(s, 4.3, 0.95, 5.2, 0.85);
    txt(s, [N("Convoyeur de la "), T200, N(" : S = A · B + A · B̄ · C.")], { x: 4.45, y: 0.95, w: 4.9, h: 0.85, fontSize: 11.5, valign: "middle" });
    frame(s, 4.3, 1.95, 5.2, 1.0);
    EQ(s, "eq_conv", 4.5, 2.2, 4.8, 0.5);
    const rows = [[cell("", H), cell("Algèbre", H), cell("Karnaugh", H)],
      [cell("part de", { bold: true, align: "left" }), cell("une équation"), cell("une table de vérité")],
      [cell("idéal pour", { bold: true, align: "left" }), cell("mettre en évidence, De Morgan"), cell("2 à 4 variables, cas X")]];
    s.addTable(rows, { x: 0.5, y: 3.2, w: 9.0, colW: [1.6, 3.7, 3.7], rowH: 0.42, border: BORDER, fontSize: 11.5 });
    life(s, 0.5, 4.6, 9.0, 0.95, ["Au-delà de 4 variables, on laisse faire le logiciel : Quartus ou un autre outil simplifie lui-même les équations d'un CPLD (semaine 5)."], 10.5);
  }

  // ============================== 14. À RETENIR · TICKET DE SORTIE
  {
    const s = slide("À retenir · ticket de sortie",
      "Ticket de sortie (5 min, seul·e, sans support). Réponses : 1) Dans les cases de sa zone jaune. 2) 1, 2, 4, 8 ou 16 cases, des rectangles. 3) Elle disparaît. 4) On le compte comme 1 s'il agrandit un groupe, sinon on l'ignore.\n" +
      "Ensuite : fiche 230 EX.");
    [["Zones", "une variable vaut 1 dans sa zone jaune"], ["Groupes", "1, 2, 4, 8 cases, les plus grands possible"], ["Lecture", "à cheval sur une zone : la variable disparaît"]].forEach(([h, d], k) => {
      const x = 0.5 + k * 3.05;
      card(s, x, 0.95, 2.9, 1.2);
      txt(s, h, { x: x + 0.15, y: 1.02, w: 2.6, h: 0.35, fontSize: 13, bold: true, color: BLUE });
      txt(s, d, { x: x + 0.15, y: 1.4, w: 2.6, h: 0.7, fontSize: 11.5 });
    });
    frame(s, 0.5, 2.35, 9.0, 3.2);
    txt(s, "Ticket de sortie : seul·e, 5 minutes, sans support", { x: 0.65, y: 2.42, w: 8.7, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    [["1", "Où la variable A vaut-elle 1 dans le tableau ?"], ["2", "Combien de cases peut compter un groupe ?"],
     ["3", "Que devient une variable dont la zone coupe un groupe en deux ?"], ["4", "Que fait-on d'un X ?"]].forEach((q, i) => {
      const x = 0.65 + (i % 2) * 4.45, y = 2.95 + Math.floor(i / 2) * 1.2;
      badge(s, x, y + 0.2, q[0], 0.36);
      txt(s, q[1], { x: x + 0.48, y, w: 3.8, h: 0.8, fontSize: 12.5, valign: "middle" });
    });
  }

  // ============================== 15. EXERCICES
  exoSlide("230 EX", DATA.TEAMS["230"], [
    ["1", "Écrire la somme de produits", "≈ 6 min · diapositive 2"], ["2", "Remplir, regrouper, lire", "≈ 10 min · diapositives 3 à 7"],
    ["3", "Quatre variables", "≈ 12 min · diapositives 8 et 9"], ["4", "La pompe de vidange (cas X)", "≈ 10 min · diapositive 12"],
    ["5", "Comparer avec l'algèbre", "≈ 7 min · diapositive 13"]],
    "Sur la ligne de remplissage, tu repars des tables de vérité relevées au banc et tu cherches l'équation la plus courte avant de câbler.",
    "En binôme, 45 min. Pour chaque tableau : remplir, regrouper, lire chaque groupe, additionner, puis contrôler.",
    ["Les logiciels de CPLD et de FPGA font ce travail automatiquement, mais il faut savoir le faire pour vérifier leur résultat."],
    "Fiche 230 EX Simplification par Karnaugh (45 min). Temps indicatifs : N°1 6 min, N°2 10 min, N°3 12 min, N°4 10 min, N°5 7 min.\n" +
    "Corrigé : 230 EX C Simplification par Karnaugh (pour l'enseignant·e).");

  // ============================== 16. PAGE INTERACTIVE
  pageSlide("221", DATA.FILES["221"], DATA.TEAMS["221"], DATA.ART["221"], "shot_221.png",
    ["Remplir un tableau depuis la table", "Lire chaque groupe", "Regrouper toi-même, jusqu'à 4 variables", "Les cas indifférents X", "Contrôler le travail d'un collègue"],
    ["Pour réviser à la maison ou rattraper une absence : la page reprend les tableaux et les exercices de la présentation."],
    "Page interactive 221 : à ouvrir dans Edge ou Chrome. Chaque étape a une partie « Comprendre » et une partie « À toi » corrigée tout de suite.");

  // ============================== 17. ANIMATION
  videoSlide("225", DATA.FILES["225"], DATA.TEAMS["225"], "cover_225.png", "2 min 47", [
    ["Remplir le tableau", "la buse de rinçage"], ["Regrouper et lire", "dans, hors, à cheval"],
    ["Quatre variables, cas X", "les bords, la pompe de vidange"]],
    ["La vidéo reprend la leçon avec la même ligne de remplissage : pour réviser ou rattraper une absence."],
    "Animation 225 : trois démonstrations, une introduction et un récapitulatif.");
};
