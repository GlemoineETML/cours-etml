// 120 Portes logiques et tables de vérité : diapositives (moteur : moteur/deck.js).
// Fil rouge : ligne de remplissage de boissons (situation de travail FutureMEM du champ LFB_El_DT1).
// Symboles CEI 60617-12 seulement ; équations en notation du Floyd (point = ET, + = OU, barre = NON, ⊕ = OU exclusif).
// Champ LFB_El_DT1 (LZ_4242, LZ_130, LZ_27, LZ_29, LZ_2223). Va avec la fiche 130 EX Portes logiques de base. Tables : entrées du poids fort au poids faible.
// v1.2 (11/16/2026) : fiche 130 EX ; fin : exercices, page interactive 121, animation 125.
module.exports = function (E) {
  const { pres, DATA, NAVY, BLUE, LBLUE, TINT, K, GR, RED, F, MATIERE, CLASSE, ANNEE, CHAMP, slide, txt, card, frame, badge, img, bullets, life,
    boxTitle, cell, H, BORDER, LINK, NEXTEC, FLOYDL, LZL, exoSlide, pageSlide, videoSlide, nandCEI, squeeze, tailles, eqImg, eqName } = E;

  const G = DATA.GATES;               // clé : [nom, anglais, qualificatif, négation, nb entrées, règle, CI 74HC, CI 4000, contenu, section, page, lien Floyd, tdv, chrono]
  const T130 = "fiche 130 EX Portes logiques de base";
  const NXR = DATA.NEXTEC.repr, NXI = DATA.NEXTEC.intro;
  const FLOYD = (label, p) => FLOYDL(3, label, p);
  const FLOYD1 = (label, p) => FLOYDL(1, label, p);
  const FLOYDG = (k) => LINK(`Floyd ${G[k][9]} p. ${G[k][10]}`, G[k][11], "Floyd, chapitre 3 sur Teams : aller ensuite à la page " + G[k][10]);
  const EX = {
    "NON": ["Voyant « cuve vide » : il s'allume quand le capteur de niveau N vaut 0.", "Un capteur actif à 0 (contact qui s'ouvre) : on l'inverse pour retrouver un 1 = vrai."],
    "ET": ["Vanne de remplissage : V = B · N. Elle s'ouvre seulement si une bouteille est sous le bec ET si le niveau est suffisant.", "Presse à deux mains : elle ne descend que si les deux boutons sont appuyés."],
    "OU": ["Voyant « défaut » : il s'allume si la pompe OU le convoyeur est en défaut (ou les deux).", "Plafonnier de voiture : il s'allume si une des portières est ouverte."],
    "NON-ET": ["Voyant « remplir » : il s'allume dès qu'une des deux cuves (sirop, eau) n'a plus un niveau suffisant.", "Le 74HC00 est très répandu : avec des NON-ET seulement, on peut construire toutes les autres portes."],
    "NON-OU": ["Le convoyeur peut tourner seulement si aucun des deux arrêts d'urgence n'est actionné.", "Avec des NON-OU aussi, on peut construire toutes les autres portes."],
    "OUX": ["Éclairage d'escalier en va-et-vient : chaque interrupteur change l'état de la lampe.", "L'OU exclusif additionne deux bits : on le retrouve dans l'additionneur (semaine 4)."],
    "NON-OUX": ["Deux capteurs de niveau redondants : « capteurs cohérents » = 1 quand ils donnent la même valeur.", "Comparateur d'égalité : un bit par porte, puis un ET sur toutes les sorties."],
  };
  const SLIDE_OF = { "NON": 5, "ET": 6, "OU": 7, "NON-ET": 8, "NON-OU": 9, "OUX": 10, "NON-OUX": 11 };
  const FIG = { "NON": "A.1", "ET": "A.2", "OU": "A.3", "NON-ET": "A.4", "NON-OU": "A.5", "OUX": "A.6", "NON-OUX": "A.7" };

  // ============================== 1. TITRE · OBJECTIFS · QUESTION DE DÉPART
  {
    const s = pres.addSlide({ masterName: "TITRE" });
    squeeze(s, 0.6, 9.5, 8.9);
    txt(s, "TEST ET MESURE 1 – EL DT 1", { x: 0.6, y: 0.35, w: 5.4, h: 0.3, fontSize: 12, bold: true, color: BLUE, charSpacing: 1 });
    txt(s, "Portes logiques et\ntables de vérité", { x: 0.6, y: 0.62, w: 5.4, h: 1.0, fontSize: 27, bold: true, color: NAVY, valign: "middle" });
    txt(s, "Des 0 et des 1, sept portes de base et quatre façons de les décrire", { x: 0.6, y: 1.62, w: 5.4, h: 0.35, fontSize: 12, color: GR });
    txt(s, "À la fin de la leçon, je suis capable de…", { x: 0.6, y: 2.0, w: 5.4, h: 0.3, fontSize: 13, bold: true });
    const obj = [
      [{ text: "dessiner la table de vérité d'un système (" }, LZL("LZ_4242"), { text: ") ;" }],
      [{ text: "décrire les portes de base et leur symbole CEI (" }, LZL("LZ_130"), { text: ") ;" }],
      [{ text: "relier équation, table de vérité et chronogramme (" }, LZL("LZ_27"), { text: ") ;" }],
      [{ text: "reconnaître une porte sous ses quatre formes (" }, LZL("LZ_29"), { text: ") ;" }],
      [{ text: "citer le CI qui contient une porte donnée (" }, LZL("LZ_2223"), { text: ")." }]];
    obj.forEach((t, i) => {
      const y = 2.36 + i * 0.4;
      badge(s, 0.6, y + 0.03, String(i + 1), 0.29);
      s.addText(t, { x: 1.0, y, w: 5.1, h: 0.35, fontFace: F, fontSize: 12, color: K, margin: 0, valign: "middle" });
    });
    frame(s, 6.25, 0.5, 3.25, 2.75);
    txt(s, "Question de départ", { x: 6.4, y: 0.58, w: 3.0, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    txt(s, "Sur une ligne de remplissage de boissons, la vanne ne doit s'ouvrir que si une bouteille est sous le bec et que la cuve contient assez de liquide. Comment un circuit électronique prend-il cette décision ?", { x: 6.4, y: 0.92, w: 3.0, h: 1.85, fontSize: 11 });
    txt(s, "Écris ton idée. Réponse à la diapositive 6.", { x: 6.4, y: 2.85, w: 3.0, h: 0.3, fontSize: 10, italic: true, color: GR });
    img(s, "gate_ET.png", 6.9, 3.4, 2.0, 1.1);
    card(s, 0.6, 4.5, 8.9, 1.0);
    s.addText([
      { text: `Classe ${CLASSE} · ${ANNEE} · ${MATIERE} · champ `, options: { bold: true } },
      { text: CHAMP, options: { bold: true, hyperlink: { url: DATA.EDGE + DATA.FUTUREMEM_CHAMP, tooltip: "Champ d'apprentissage sur FutureMEM" } } },
      { text: "", options: { breakLine: true } },
      { text: "Références : ", options: { color: K } }, LINK("nextecmedia 1.1 et 1.2.1", NXR[0], "Formes de représentation des circuits numériques"),
      { text: " · ", options: { color: K } }, FLOYD("Floyd, chap. 3 Portes logiques (p. 111-138)", 112),
      { text: " · ", options: { color: K } }, FLOYD1("chap. 1 (p. 5-12)", 5),
    ], { x: 0.8, y: 4.55, w: 8.5, h: 0.9, fontFace: F, fontSize: 11, color: NAVY, margin: 0, valign: "middle", paraSpaceAfter: 3 });
    s.addNotes("Durée : 2 × 45 min avec la partie A de la fiche 130 EX (les apprenti·e·s complètent la fiche pendant la présentation). Partie B de la fiche 130 EX : 45 min en binôme.\n" +
      "Déroulement : diapositives 2 à 4, les outils (variables, table de vérité, chronogramme). Diapositives 5 à 7 : NON, ET, OU avec la classe. Diapositives 8 à 11 : NON-ET à NON-OU exclusif, les apprenti·e·s complètent seul·e·s la table et le chronogramme à partir de l'équation et de la règle. Diapositive 12 : correction et synthèse. Diapositive 13 : les CI. Diapositive 14 : ticket de sortie. Diapositives 15 à 17 : exercices (fiche 130 EX, partie B), page interactive 121, animation 125.\n" +
      "Question de départ : noter les idées sans corriger. Réponse à la diapositive 6 : une porte ET, V = B · N.\n" +
      "Objectifs évaluateurs (FutureMEM, LFB_El_DT1) : LZ_4242 (C3), LZ_130 (C2), LZ_27 (C3), LZ_29 (C4), LZ_2223 (C1). Les codes sont cliquables.\n" +
      "Liens Floyd : " + DATA.FLOYD_NOTE);
  }

  // ============================== 2. DES 0 ET DES 1 SUR LA LIGNE DE REMPLISSAGE
  {
    const s = slide("Des 0 et des 1 sur la ligne de remplissage",
      "Situation de travail du champ LFB_El_DT1 (FutureMEM) : commande d'une ligne de remplissage de boissons, avec des capteurs et des interrupteurs en entrée, des vannes, un convoyeur et une pompe en sortie. Première étape d'un projet : le tableau des entrées et des sorties.\n" +
      "Variable binaire : elle ne prend que deux valeurs. Convention du cours (Floyd 1-2 p. 5) : 1 = vrai = actif = niveau HAUT ; 0 = faux = inactif = niveau BAS.\n" +
      "Activité (didactique constructiviste FutureMEM) : faire lister par les apprenti·e·s d'autres situations « logiques » du quotidien : ascenseur, lave-linge, portail automatique…");
    img(s, "fig_ligne.png", 0.5, 0.95, 5.75, 3.3);
    frame(s, 6.45, 0.95, 3.05, 2.05);
    txt(s, "Variable binaire", { x: 6.6, y: 1.02, w: 2.8, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, [{ text: "1", options: { bold: true, color: BLUE } }, { text: " = vrai, actif, niveau HAUT", options: { breakLine: true } },
      { text: "0", options: { bold: true, color: NAVY } }, { text: " = faux, inactif, niveau BAS", options: { breakLine: true } },
      { text: "Pas d'autre valeur possible.", options: { italic: true, color: GR } }], { x: 6.6, y: 1.38, w: 2.8, h: 1.5, fontSize: 12, paraSpaceAfter: 4 });
    card(s, 6.45, 3.1, 3.05, 1.2);
    txt(s, [{ text: "Entrées : ", options: { bold: true, color: BLUE } }, { text: "capteurs, boutons", options: { breakLine: true } },
      { text: "Sorties : ", options: { bold: true, color: NAVY } }, { text: "vannes, moteurs, voyants" }], { x: 6.6, y: 3.2, w: 2.8, h: 1.0, fontSize: 12, valign: "middle", paraSpaceAfter: 4 });
    life(s, 0.5, 4.45, 9.0, 1.1, [
      "Pour toute machine automatique, on commence par la liste des entrées et des sorties : c'est la base du cahier des charges.",
      "Un automate ou un microcontrôleur fait la même chose : il lit des entrées 0 ou 1 et commande des sorties 0 ou 1.",
    ]);
  }

  // ============================== 3. CONSTRUIRE UNE TABLE DE VÉRITÉ
  {
    const s = slide("Construire une table de vérité",
      "Objectif LZ_4242. La table de vérité donne la valeur de chaque sortie pour toutes les combinaisons possibles des entrées.\n" +
      "Méthode : une colonne par entrée, du poids fort au poids faible (C B A), puis une par sortie ; n entrées donnent 2^n lignes ; on range les lignes dans l'ordre du comptage binaire (000, 001, 010…) pour n'en oublier aucune. A est toujours le poids faible.\n" +
      "Floyd 3-2 : exemples de tables à 2, 3 et 4 entrées (la porte ET à 4 entrées a 16 lignes). Lien avec la numération : la colonne des entrées est le comptage binaire de 0 à 2^n − 1.\n" +
      "Exercice d'application : fiche 130 EX, partie B, N°1 (convoyeur à 3 entrées E, L, U).");
    [["1", "Une colonne par entrée, du poids fort au poids faible (C B A), puis la sortie."], ["2", "n entrées → 2^{n} lignes."], ["3", "On compte en binaire, de 000 à 111."], ["4", "Pour chaque ligne, on lit le cahier des charges et on écrit la sortie."]].forEach((r, i) => {
      const y = 1.0 + i * 0.62;
      badge(s, 0.5, y, r[0], 0.38);
      txt(s, r[1], { x: 1.0, y, w: 3.6, h: 0.5, fontSize: 12.5, valign: "middle" });
    });
    s.addTable([[cell("Entrées", H), cell("Lignes", H)], [cell("1"), cell("2")], [cell("2"), cell("4")], [cell("3"), cell("8")], [cell("4"), cell("16")]],
      { x: 0.5, y: 3.6, w: 2.6, colW: [1.3, 1.3], rowH: 0.3, border: BORDER, fontSize: 11 });
    const rows = [[cell("C", H), cell("B", H), cell("A", H), cell("Y", H)]];      // C poids fort, A poids faible
    for (let v = 0; v < 8; v++) rows.push([cell((v >> 2) & 1), cell((v >> 1) & 1), cell(v & 1), cell("?", { color: GR })]);
    s.addTable(rows, { x: 5.0, y: 0.95, w: 2.8, colW: [0.7, 0.7, 0.7, 0.7], rowH: 0.3, border: BORDER, fontSize: 11.5 });
    txt(s, "3 entrées → 8 lignes, de 000 à 111 (C B A)", { x: 4.8, y: 3.72, w: 3.2, h: 0.3, fontSize: 10.5, italic: true, color: GR, align: "center" });
    s.addShape(pres.shapes.RIGHT_BRACE || pres.shapes.RECTANGLE, { x: 7.9, y: 1.25, w: 0.2, h: 2.4, line: { color: BLUE, width: 1.25 }, fill: { color: "FFFFFF" } });
    txt(s, "comptage\nbinaire\n0 à 7", { x: 8.15, y: 2.0, w: 1.3, h: 0.9, fontSize: 10.5, color: BLUE, valign: "middle" });
    life(s, 3.3, 4.15, 6.2, 1.4, [
      "En dépannage, on compare la table de vérité à ce qu'on mesure, ligne par ligne, avec des interrupteurs et une LED.",
      "La table de vérité figure dans la fiche technique de chaque CI (« Function table », L = 0, H = 1).",
    ], 10.5);
  }

  // ============================== 4. LIRE UN CHRONOGRAMME
  {
    const s = slide("Lire un chronogramme",
      "Objectif LZ_27 : relier le tableau de valeurs (table de vérité) et la représentation graphique (chronogramme). Floyd 1-2 p. 9 : le chronogramme montre plusieurs formes d'onde sur le même axe du temps.\n" +
      "Méthode : on découpe le temps en intervalles où rien ne change ; dans chaque intervalle, on lit A et B, on cherche la ligne de la table de vérité, on dessine Y.\n" +
      "Exemple surligné : intervalle 4, A = 1 et B = 1 → pour une porte ET, Y = 1. Chaque intervalle du chronogramme correspond à une ligne de la table de vérité, dans l'ordre où les combinaisons se présentent.\n" +
      "Au laboratoire : oscilloscope deux voies ou analyseur logique (Floyd 1-7 p. 29-37).");
    img(s, "chrono_lecture.png", 0.5, 0.95, 5.6, 3.3);
    frame(s, 6.35, 0.95, 3.15, 3.3);
    txt(s, "Méthode", { x: 6.5, y: 1.02, w: 2.9, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    bullets(s, ["Le temps avance de gauche à droite.", "Une ligne par variable : A, B, puis Y.", "On lit verticalement, intervalle par intervalle.",
      "Intervalle 4 : A = 1, B = 1 → Y = 1 (porte ET)."], { x: 6.5, y: 1.4, w: 2.9, h: 2.75, fontSize: 11.5 }, true);
    life(s, 0.5, 4.4, 9.0, 1.15, [
      "L'oscilloscope et l'analyseur logique affichent des chronogrammes : c'est ce que tu vois au laboratoire en mesurant un circuit.",
      "Chaque intervalle du chronogramme correspond à une ligne de la table de vérité.",
    ]);
  }

  // ============================== 5 à 11. LES SEPT PORTES
  function gateSlide(k, guided) {
    const g = G[k], n = g[4], eqFile = `eq_${k}.png`;
    const title = `Porte ${g[0]} (${g[1]})`;
    const notes = [
      `Floyd ${g[9]} p. ${g[10]}. Symbole CEI 60617-12 : rectangle, qualificatif « ${g[2]} »` + (g[3] ? ", cercle de négation en sortie." : "."),
      `Règle : ${g[5]} Équation (notation Floyd) : voir l'image. CI : ${g[6]} (${g[8]}), série 4000 : ${g[7]}.`,
      guided ? "Démarche guidée : faire prédire la colonne Y de la table avant de la commenter, puis faire compléter la fiche 130 EX (" + FIG[k] + ")."
             : "Démarche autonome : les apprenti·e·s complètent la table et le chronogramme de la fiche 130 EX (" + FIG[k] + ") à partir de la règle et de l'équation. Correction : diapositive 12.",
      "Exemples : " + EX[k].join(" "),
    ].join("\n");
    const s = slide(title, notes);
    // symbole
    img(s, `gate_${k}.png`, 0.5, 0.95, 2.05, 1.5);
    // table de vérité
    const tv = g[12];
    const hdr = (n === 1 ? ["A", "Y"] : ["B", "A", "Y"]).map(c => cell(c, H));   // poids fort → poids faible, puis Y
    const rows = [hdr].concat(tv.map(r => r.map((c, j) => j === r.length - 1
      ? cell(guided ? c : "?", { bold: true, color: guided ? BLUE : GR }) : cell(c))));
    const cw = n === 1 ? [0.7, 0.7] : [0.6, 0.6, 0.6];
    s.addTable(rows, { x: 2.85, y: 0.95, w: cw.reduce((a, b) => a + b), colW: cw, rowH: 0.33, border: BORDER, fontSize: 12 });
    // chronogramme
    img(s, guided ? `chrono_${k}.png` : `chrono_${k}_q.png`, 0.5, 2.75, 4.75, 2.05);
    // carte équation, règle, CI
    frame(s, 5.45, 0.95, 4.05, 2.15);
    txt(s, "Équation", { x: 5.6, y: 1.0, w: 1.4, h: 0.3, fontSize: 12, bold: true, color: BLUE });
    eqImg(s, eqFile, g[14], 6.9, 1.0, 2.0, 0.42);
    txt(s, [{ text: "Règle : ", options: { bold: true } }, { text: g[5] }], { x: 5.6, y: 1.5, w: 3.75, h: 0.75, fontSize: 12 });
    txt(s, [{ text: "CI : ", options: { bold: true } }, { text: `${g[6]} · série 4000 : ${g[7]}`, options: { breakLine: true } }, { text: g[8], options: { color: GR } }],
      { x: 5.6, y: 2.3, w: 3.75, h: 0.7, fontSize: 11 });
    // vraie vie
    const lv = k === "ET" ? [EX[k][0], "Réponse à la question de départ : la vanne est commandée par une porte ET."] : EX[k];
    life(s, 5.45, 3.2, 4.05, 1.6, lv, 10.5);
    // bandeau bas
    card(s, 0.5, 4.95, 9.0, 0.6, guided ? TINT : NAVY);
    s.addText(guided
      ? [{ text: `Fiche 130 EX, ${FIG[k]} : `, options: { bold: true } }, { text: "complète la table, l'équation, la règle et le chronogramme. · " }, FLOYDG(k)]
      : [{ text: `À toi (fiche 130 EX, ${FIG[k]}) : `, options: { bold: true, color: LBLUE } }, { text: "à partir de la règle et de l'équation, complète la colonne Y et dessine Y. · ", options: { color: "FFFFFF" } },
         Object.assign(FLOYDG(k), { options: Object.assign({}, FLOYDG(k).options, { color: LBLUE }) })],
      { x: 0.65, y: 4.95, w: 8.7, h: 0.6, fontFace: F, fontSize: 11, color: NAVY, margin: 0, valign: "middle" });
  }
  ["NON", "ET", "OU"].forEach(k => gateSlide(k, true));
  ["NON-ET", "NON-OU", "OUX", "NON-OUX"].forEach(k => gateSlide(k, false));

  // ============================== 12. SYNTHÈSE : SEPT PORTES, QUATRE REPRÉSENTATIONS
  {
    const s = slide("Synthèse : sept portes, quatre représentations",
      "Correction des diapositives 8 à 11 (fiche 130 EX, A.4 à A.7). Objectif LZ_29 : différencier les portes par le symbole, la table de vérité, l'équation et le chronogramme.\n" +
      "Pour reconnaître une porte, on cherche la combinaison qui la distingue : A = B = 1 sépare OU (Y = 1) et OU exclusif (Y = 0) ; A = B = 0 sépare NON-OU (seul Y = 1 sur cette ligne) et NON-OU exclusif.\n" +
      "Une porte « NON-… » donne exactement l'inverse de la porte de base : sa colonne Y est complémentée.\n" +
      "Exercice : fiche 130 EX, partie B, N°2 et N°3.");
    const order = DATA.ORDER;
    const colW = [1.45, 1.05, 1.75, 0.55, 0.55, 0.55, 0.55, 2.45];
    const head = ["Porte", "Symbole", "Équation", "00", "01", "10", "11", "Y = 1 si…"].map(c => cell(c, H));
    const short = { "NON": "A = 0", "ET": "A et B valent 1", "OU": "au moins une entrée vaut 1", "NON-ET": "pas les deux à 1",
      "NON-OU": "A = 0 et B = 0", "OUX": "A ≠ B", "NON-OUX": "A = B" };
    const rows = [head].concat(order.map(k => {
      const g = G[k];
      const ys = g[4] === 1 ? [0, 1, 0, 1].map(a => 1 - a) : g[12].map(r => r[2]);   // colonnes BA = 00, 01, 10, 11 : A vaut 0, 1, 0, 1
      return [cell(g[0], { bold: true, align: "left", fontSize: 11 }), cell(""), cell(""),
        ...ys.map(y => cell(y, { bold: true, color: y ? BLUE : NAVY })), cell(short[k], { align: "left", fontSize: 10.5 })];
    }));
    const y0 = 0.95, rh = 0.47, hh = 0.36;
    s.addTable(rows, { x: 0.5, y: y0, w: colW.reduce((a, b) => a + b), colW, rowH: [hh].concat(order.map(() => rh)), border: BORDER, fontSize: 11 });
    // images posées sur les cellules (le squeeze s'applique aussi aux images)
    order.forEach((k, i) => {
      const yy = y0 + hh + i * rh;
      const gx = 0.5 + colW[0], ex = gx + colW[1];
      s.addImage({ path: `gate_${k}.png`, x: gx + 0.17, y: yy + 0.04, w: 0.58, h: 0.39 });
      const EQD = tailles(/^eq_.*\.png$/), PX = 0.38 / Math.max(...Object.values(EQD).map(v => v[1]));
      const ew = EQD[`eq_${k}.png`][0] * PX, eh = EQD[`eq_${k}.png`][1] * PX;
      s.addImage({ path: `eq_${k}.png`, x: ex + (colW[2] - ew) / 2, y: yy + (rh - eh) / 2, w: ew, h: eh, objectName: eqName(G[k][14], 1600) });
    });
    txt(s, "Colonnes 00 à 11 : valeurs de B et A (B, poids fort, à gauche). Pour NON, seule A compte.", { x: 0.5, y: y0 + hh + 7 * rh + 0.05, w: 9.0, h: 0.25, fontSize: 9.5, italic: true, color: GR });
    card(s, 0.5, 4.95, 9.0, 0.6);
    txt(s, [{ text: "Reconnaître une porte : ", options: { bold: true, color: BLUE } }, { text: "cherche la ligne qui la distingue. A = B = 1 sépare OU (Y = 1) et OU exclusif (Y = 0)." }],
      { x: 0.65, y: 4.95, w: 8.7, h: 0.6, fontSize: 11.5, valign: "middle" });
  }

  // ============================== 13. DES PORTES AUX CI
  {
    const s = slide("Des portes aux circuits intégrés",
      "Objectif LZ_2223 : citer des exemples de CI. Floyd 3-8 p. 146-149 (figures 3-59 à 3-63 : brochages des 74xx08, 74xx00, 74xx32, 74xx02, 74xx86).\n" +
      "La fonction se lit dans les deux derniers chiffres de la série 74 (présentation 100, diapositive 5). Le 74HC7266 (NON-OU exclusif) est moins courant que les autres.\n" +
      "Point de vigilance : le 74HC02 (NON-OU) n'a pas le même brochage que le 74HC00 : sorties sur les broches 1, 4, 10 et 13. Toujours vérifier la fiche technique.\n" +
      "Exercice : fiche 130 EX, partie B, N°4 (câbler la vanne V = B · N sur un 74HC08).");
    const rows = [[cell("Porte", H), cell("CI 74HC", H), cell("CI 4000", H), cell("Contenu", H)]].concat(DATA.ORDER.map(k => {
      const g = G[k];
      return [cell(g[0], { bold: true, align: "left" }), cell(g[6]), cell(g[7]), cell(g[8], { align: "left", fontSize: 10.5 })];
    }));
    s.addTable(rows, { x: 0.5, y: 0.95, w: 6.2, colW: [1.4, 1.15, 0.85, 2.8], rowH: 0.4, border: BORDER, fontSize: 11 });
    img(s, "dip_74HC08.png", 7.0, 0.95, 2.3, 2.49);
    txt(s, "74HC08 : 4 portes ET (vue de dessus)", { x: 6.85, y: 3.5, w: 2.6, h: 0.25, fontSize: 9.5, italic: true, color: GR, align: "center" });
    life(s, 0.5, 4.3, 9.0, 1.25, [
      "Sur une carte, on prend le CI dans la même famille que le reste (74HC avec du 74HC, présentation 100).",
      "Les portes inutilisées d'un CI ont leurs entrées reliées à GND ou à V_{CC}, jamais en l'air.",
    ]);
  }

  // ============================== 14. À RETENIR · TICKET DE SORTIE
  {
    const s = slide("À retenir · ticket de sortie",
      "Ticket de sortie (5 min, seul·e, sans support). Réponses : 1) 2^3 = 8 lignes. 2) Rectangle avec « ≥1 » et un cercle de négation en sortie. 3) NON-OU (Y = 1 seulement quand A = 0 et B = 0). 4) 74HC32 (ou 4071 en série 4000).\n" +
      "Ensuite : fiche 130 EX, partie B, en binôme (45 min), puis nextecmedia 1.2.1.");
    const r = [["Table de vérité", "2^{n} lignes, dans l'ordre du comptage binaire"], ["Quatre représentations", "symbole CEI, table, équation, chronogramme"], ["Une porte, un CI", "74HC08 ET · 74HC32 OU · 74HC04 NON · 74HC00 NON-ET"]];
    r.forEach(([h, d], k) => {
      const x = 0.5 + k * 3.05;
      card(s, x, 0.95, 2.9, 1.3);
      txt(s, h, { x: x + 0.15, y: 1.02, w: 2.6, h: 0.35, fontSize: 13, bold: true, color: BLUE });
      txt(s, d, { x: x + 0.15, y: 1.4, w: 2.6, h: 0.8, fontSize: 11.5 });
    });
    frame(s, 0.5, 2.45, 9.0, 2.45);
    txt(s, "Ticket de sortie : seul·e, 5 minutes, sans support", { x: 0.65, y: 2.52, w: 8.7, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    [["1", "Combien de lignes compte la table de vérité d'un système à 3 entrées ?"], ["2", "Dessine le symbole CEI d'une porte NON-OU."],
     ["3", "Y = 1 seulement quand A = 0 et B = 0 : quelle porte ?"], ["4", "Quel CI de la série 74HC contient 4 portes OU ?"]].forEach((q, i) => {
      const x = 0.65 + (i % 2) * 4.45, y = 2.95 + Math.floor(i / 2) * 0.9;
      badge(s, x, y + 0.13, q[0], 0.34);
      txt(s, q[1], { x: x + 0.45, y, w: 3.85, h: 0.62, fontSize: 12, valign: "middle" });
    });
    card(s, 0.5, 5.02, 9.0, 0.55);
    s.addText([{ text: "Ensuite : ", options: { bold: true } }, { text: T130 + ", partie B · " },
      LINK("nextecmedia 1.2.1", NXR[0], "Formes de représentation des circuits numériques"), { text: " · " }, FLOYD("Floyd chap. 3", 112)],
      { x: 0.65, y: 5.02, w: 8.7, h: 0.55, fontFace: F, fontSize: 11.5, color: NAVY, margin: 0, valign: "middle" });
  }

  // ============================== 15 à 17. EXERCICES · PAGE INTERACTIVE · ANIMATION
  exoSlide("130 EX", DATA.TEAMS["130"], [
    ["A", "Partie A : les sept portes", "pendant la présentation · diapositives 5 à 12"],
    ["1", "Du cahier des charges à la table de vérité", "≈ 12 min · diapositives 2 et 3"], ["2", "Table de vérité, équation et chronogramme", "≈ 10 min · diapositives 4 et 12"],
    ["3", "Reconnaître une porte à son chronogramme", "≈ 8 min · diapositive 12"], ["4", "Choisir le CI et numéroter les broches", "≈ 8 min · diapositive 13"],
    ["5", "Quelle porte pour quelle situation ?", "≈ 7 min · diapositives 5 à 12"]],
    "La ligne de remplissage de boissons de la diapositive 2 : capteurs, vanne, voyants. Un capteur donne 1 quand ce qu'il surveille est vrai ; un actionneur est en marche quand sa sortie vaut 1.",
    "Partie A pendant la présentation. Partie B en binôme, 45 min. Écris toujours la règle ou l'intervalle qui justifie ta réponse.",
    ["En automatisation, on suit toujours ce chemin : cahier des charges, table de vérité, équation, puis câblage du circuit intégré."],
    "Fiche 130 EX Portes logiques de base. Partie A : complétée pendant la présentation (diapositives 5 à 12). Partie B : 45 min en binôme (N°1 12 min ; N°2 10 min ; N°3 et N°4 8 min chacun ; N°5 7 min).\n" +
    "Corrigé : 130 EX C Portes logiques de base (pour l'enseignant·e).\n" +
    "Le lien vise le dossier Teams El_DT1/PMT&SBT : il fonctionne une fois le fichier déposé sous ce nom.");
  pageSlide("121", DATA.FILES["121"], DATA.TEAMS["121"], DATA.ART["121"], "shot_121.png",
    ["Essaie chaque porte (chronogramme en direct)", "Prépare la table de test d'un CI", "Le voyant « défaut » de la ligne", "Reconnais la porte à son chronogramme",
     "Quelle porte, quel CI ?", "Câble la vanne sur un 74HC08"],
    ["Les situations viennent de la ligne de remplissage et du laboratoire : capteurs, voyants, vanne, analyseur logique et breadboard.",
     "À refaire à la maison avant le test : chaque erreur est expliquée."],
    "Page interactive 121 : un seul fichier .html, sans installation ni connexion. Six exercices ; quatre commencent par une animation « Comprendre » reprise des diapositives 2, 3, 4 et 13, et le N°1 affiche un chronogramme en direct (diapositive 12).\n" +
    "Utilisation : projeter l'animation, faire répondre la classe, vérifier ensemble ; ou à faire à la maison. Le score n'est pas enregistré.\n" +
    "Déposer le fichier « 121 Portes logiques et tables de vérité.html » dans le dossier Teams El_DT1/PMT&SBT : le lien de la diapositive vise ce chemin. Teams peut le télécharger au lieu de l'afficher : l'ouvrir alors dans Edge ou Chrome (l'aperçu de fichier n'exécute pas les animations).\n" +
    "Le lien « artefact claude.ai » ne fonctionne pour les apprenti·e·s qu'une fois l'artefact partagé depuis claude.ai.");
  videoSlide("125", DATA.FILES["125"], DATA.TEAMS["125"], "cover_125.png", "5 minutes",
    [["Des 0 et des 1", "la ligne de remplissage de boissons"], ["Construire une table de vérité", "toutes les combinaisons, dans l'ordre"],
     ["Lire un chronogramme", "de l'analyseur logique à la table"], ["Les sept portes de base", "symboles CEI, tables, équations"],
     ["Du symbole au circuit intégré", "câbler la vanne sur un 74HC08"]],
    ["Pour réviser à la maison ou rattraper une absence : la vidéo reprend la leçon avec la même ligne de remplissage.",
     "Chaque partie commence par une carte de 13 s : la situation, la question et ce qu'on va voir."],
    "Animation 125 Portes logiques et tables de vérité : 5 min 25, 1920 × 1080. La vidéo est intégrée à la présentation : elle se lit dans PowerPoint sans connexion (clic sur l'image en mode diaporama).\n" +
    "PowerPoint dans Teams ou dans le navigateur ne lit pas toujours une vidéo intégrée : utiliser alors le lien « La vidéo sur Teams » (fichier 125 Portes logiques et tables de vérité.mp4, à déposer dans le dossier El_DT1/PMT&SBT).\n" +
    "Suggestion : la montrer en fin de leçon pour revoir les cinq points, ou la donner à regarder avant la partie B de la fiche 130 EX.");
};
