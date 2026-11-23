// 100 Familles de circuits logiques : diapositives (moteur : moteur/deck.js).
// Sources : nextecmedia, Technique numérique, 4.1 Familles de circuits ; Floyd chap. 3 (3-8 Logique à fonction fixe, p. 146-155).
// Champ LFB_El_DT1 (LZ_4255, LZ_4256). Fin : exercices 110 EX, page interactive 101, animation 105.
// Historique : v1.1 NON-OU = 7402, sortie push-pull, « Lire une référence », « Dans le boîtier », « Niveaux de sortie et marge de bruit » ;
// v1.2 tables B A Y, typographie, liens Floyd, cartouche sans éditeur ; v1.3 (11/16/2026) fin de présentation exercices, page, animation.
module.exports = function (E) {
  const { pres, DATA, NAVY, BLUE, LBLUE, TINT, K, GR, RED, F, MATIERE, CLASSE, ANNEE, CHAMP, slide, txt, card, frame, badge, img, bullets, life,
    boxTitle, cell, H, BORDER, LINK, NEXTEC, FLOYDL, LZL, exoSlide, pageSlide, videoSlide, nandCEI, squeeze, tailles, eqImg, eqName } = E;
  const REF = (label) => NEXTEC("fam", label);
  const FLOYD = (label, p) => FLOYDL(3, label, p);

  // ============================== 1. TITRE · OBJECTIFS · QUESTION DE DÉPART
  {
    const s = pres.addSlide({ masterName: "TITRE" });
    squeeze(s, 0.6, 9.5, 8.9);
    txt(s, "TEST ET MESURE 1 – EL DT 1", { x: 0.6, y: 0.4, w: 5.4, h: 0.3, fontSize: 12, bold: true, color: BLUE, charSpacing: 1 });
    txt(s, "Familles de circuits\nlogiques", { x: 0.6, y: 0.7, w: 5.4, h: 1.05, fontSize: 28, bold: true, color: NAVY, valign: "middle" });
    txt(s, "TTL, CMOS, niveaux logiques et fiches techniques", { x: 0.6, y: 1.78, w: 5.4, h: 0.4, fontSize: 12.5, color: GR });
    txt(s, "À la fin de la leçon, je suis capable de…", { x: 0.6, y: 2.25, w: 5.4, h: 0.3, fontSize: 13.5, bold: true });
    const obj = [
      [{ text: "expliquer les niveaux 0 et 1 d'une famille (" }, LZL("LZ_4255"), { text: ") ;" }],
      [{ text: "citer les caractéristiques des familles actuelles (" }, LZL("LZ_4256"), { text: ") ;" }],
      [{ text: "trouver brochage, niveaux et limites dans une fiche technique ;" }],
      [{ text: "dire quand il faut un convertisseur de niveaux." }]];
    obj.forEach((t, i) => {
      const y = 2.62 + i * 0.42;
      badge(s, 0.6, y + 0.03, String(i + 1), 0.3);
      s.addText(t, { x: 1.02, y, w: 5.0, h: 0.36, fontFace: F, fontSize: 12.5, color: K, margin: 0, valign: "middle" });
    });
    frame(s, 6.15, 0.55, 3.35, 2.6);
    txt(s, "Question de départ", { x: 6.3, y: 0.63, w: 3.1, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    txt(s, "Un Arduino Uno travaille en 5 V. Ton capteur de température est alimenté en 3,3 V. Peux-tu relier directement ses broches à l'Arduino ?", { x: 6.3, y: 0.97, w: 3.1, h: 1.45, fontSize: 11.5 });
    txt(s, "Écris ton hypothèse. Réponse aux diapositives 12 et 17.", { x: 6.3, y: 2.62, w: 3.1, h: 0.42, fontSize: 10, italic: true, color: GR });
    nandCEI(s, 7.1, 3.4, 0.95);
    card(s, 0.6, 4.5, 8.9, 1.0);
    s.addText([
      { text: `Classe ${CLASSE} · ${ANNEE} · ${MATIERE} · champ `, options: { bold: true } },
      { text: CHAMP, options: { bold: true, hyperlink: { url: DATA.EDGE + DATA.FUTUREMEM_CHAMP, tooltip: "Champ d'apprentissage sur FutureMEM" } } },
      { text: "", options: { breakLine: true } },
      { text: "Références : ", options: { color: K } }, REF("nextecmedia, 4.1 Familles de circuits"),
      { text: " · ", options: { color: K } }, FLOYD("Floyd, chap. 3, 3-8 Logique à fonction fixe (p. 146-155)", 146),
    ], { x: 0.8, y: 4.55, w: 8.5, h: 0.9, fontFace: F, fontSize: 11, color: NAVY, margin: 0, valign: "middle", paraSpaceAfter: 3 });
    s.addNotes("Durée : 2 × 45 min. Diapositives 2 à 13 : familles de circuits (nextecmedia 4.1, Floyd 3-8). Diapositives 14 à 18 : lecture d'une fiche technique, niveaux logiques et temps de propagation. Diapositive 19 : synthèse et ticket de sortie. Diapositives 20 à 22 : exercices (fiche 110 EX Familles de circuits logiques), page interactive 101, animation 105.\n" +
      "Prérequis : notions de tension et de courant. Les portes logiques sont vues en détail dans la présentation 120.\n" +
      "Question de départ : chaque apprenti·e note une hypothèse sans correction immédiate. Réponse à la diapositive 12 : non, une sortie 5 V appliquée à une entrée 3,3 V dépasse sa valeur limite et peut la détruire ; il faut un convertisseur de niveaux, bidirectionnel si la liaison est un bus I²C. La diapositive 17 complète l'autre sens : une sortie 3,3 V n'atteint pas V_IH = 3,5 V d'une entrée 74HC alimentée en 5 V.\n" +
      "Objectifs évaluateurs du plan de formation : LZ_4255 (expliquer les niveaux numériques des familles) et LZ_4256 (citer les caractéristiques des familles actuelles). Les codes sont cliquables (FutureMEM).\n" +
      "Liens Floyd : " + DATA.FLOYD_NOTE);
  }

  // ============================== 2. QU'EST-CE QU'UNE FAMILLE ?
  {
    const s = slide("Une famille de circuits, c'est quoi ?",
      "Définition (nextecmedia 4.1) : un groupe de CI logiques de même technologie, aux propriétés électriques définies, qu'on peut relier entre eux en toute sécurité.\n" +
      "Analogie : une famille, c'est une langue commune. Deux CI de la même famille se comprennent : même tension d'alimentation, mêmes niveaux logiques.\n" +
      "Sortie d'un CI CMOS : deux transistors travaillent en interrupteurs, l'un vers +V_CC, l'autre vers la masse. Un seul conduit à la fois. Celui du haut conduit → Y = 1 ; celui du bas conduit → Y = 0. Pas d'état intermédiaire en fonctionnement normal.\n" +
      "Cas particulier : une sortie à collecteur (ou drain) ouvert n'a que le transistor du bas. Le 1 est alors donné par une résistance de tirage vers +V_CC.\n" +
      "Aujourd'hui, les CI numériques sont surtout faits de transistors à effet de champ (MOSFET), parfois combinés à des bipolaires. Le type de semi-conducteur et la construction donnent la technologie de fabrication.");
    card(s, 0.5, 0.95, 9.0, 1.0, NAVY);
    s.addText([
      { text: "Un groupe de CI logiques ", options: { color: "FFFFFF" } }, { text: "de même technologie", options: { color: LBLUE, bold: true } },
      { text: ", aux propriétés électriques définies, qu'on peut ", options: { color: "FFFFFF" } }, { text: "relier entre eux en toute sécurité.", options: { color: LBLUE, bold: true } },
    ], { x: 0.75, y: 0.95, w: 8.5, h: 1.0, fontFace: F, fontSize: 16, margin: 0, valign: "middle" });
    txt(s, "La famille fixe :", { x: 0.5, y: 2.12, w: 4.0, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    [["1", "les niveaux", "quelle tension vaut 0, quelle tension vaut 1"], ["2", "la vitesse", "à quelle vitesse le signal peut commuter"], ["3", "le courant", "combien le CI consomme et peut fournir"]].forEach((r, i) => {
      const y = 2.5 + i * 0.6;
      badge(s, 0.5, y, r[0], 0.36);
      txt(s, [{ text: r[1] + " : ", options: { bold: true } }, { text: r[2] }], { x: 1.0, y, w: 3.5, h: 0.45, fontSize: 12.5, valign: "middle" });
    });
    img(s, "fig_pushpull.png", 4.75, 2.05, 4.75, 2.2);
    txt(s, "Sortie CMOS : un seul des deux transistors conduit.", { x: 4.75, y: 4.1, w: 4.75, h: 0.3, fontSize: 11, italic: true, color: GR, align: "center" });
    life(s, 0.5, 4.45, 9.0, 1.1, [
      "Sur une carte, on garde si possible une seule famille : les CI se branchent directement, sans adaptation.",
      "Quand on répare ou remplace un CI, on choisit un composant de la même famille (ex. un 74HC pour un 74HC).",
    ]);
  }

  // ============================== 3. TTL · CMOS · 74HC(T)
  {
    const s = slide("TTL, CMOS… et l'hybride 74HC(T)",
      "TTL : transistors bipolaires, 5 V, rapide mais gourmand. Série 74xx, ex. 7400. Floyd 3-8 p. 150 : la famille LS (Schottky à faible consommation) est la plus courante des bipolaires.\n" +
      "CMOS : MOSFET canal N et canal P, consommation très faible surtout au repos. Série 4000, ex. 4011.\n" +
      "Nuance à donner : la série CMOS 4000 d'origine est lente (environ 100 ns) ; ce sont les familles CMOS modernes (HC, AC, LVC…) qui sont rapides.\n" +
      "74HC : structure CMOS, brochage de la série 74, entrées CMOS. 74HCT : même chose avec des entrées compatibles TTL (V_IH = 2 V, V_IL = 0,8 V). Le manuel dit « 74HC compatible TTL » : il s'agit de la version HCT.");
    const cols = [
      ["TTL", "Transistor-Transistor Logic", NAVY, ["Transistors bipolaires", "Alimentation : 5 V", "Rapide, mais gourmand", "Série 74xx, ex. 7400"]],
      ["CMOS", "Complementary MOS", BLUE, ["MOSFET canal N et canal P", "Consommation très faible au repos", "Rapide (familles modernes)", "Série 40xx, ex. 4011"]],
      ["74HC(T)", "CMOS au brochage 74xx", "1B5FA8", ["Structure interne CMOS", "Brochage de la série 74", "HCT : entrées compatibles TTL", "Ex. 74HCT00"]],
    ];
    cols.forEach(([h, sub, col, pts], k) => {
      const x = 0.5 + k * 3.05, w = 2.9;
      s.addShape(pres.shapes.RECTANGLE, { x, y: 0.95, w, h: 0.9, fill: { color: col }, line: { color: col } });
      txt(s, h, { x: x + 0.15, y: 1.0, w: w - 0.3, h: 0.45, fontSize: 21, bold: true, color: "FFFFFF" });
      txt(s, sub, { x: x + 0.15, y: 1.45, w: w - 0.3, h: 0.32, fontSize: 10.5, italic: true, color: "FFFFFF" });
      card(s, x, 1.9, w, 2.15);
      bullets(s, pts, { x: x + 0.15, y: 2.02, w: w - 0.3, h: 1.95, fontSize: 12 });
    });
    life(s, 0.5, 4.2, 9.0, 1.35, [
      "Le 74HC est la famille la plus courante en atelier et en formation : on la trouve chez tous les distributeurs.",
      "Les CI en TTL pur (74xx, 74LS) ne se rencontrent plus guère qu'en maintenance d'anciens appareils.",
      "Les microcontrôleurs, les FPGA et les mémoires sont tous en technologie CMOS.",
    ]);
  }

  // ============================== 4. ÉQUIVALENCES ET SYMBOLE CEI
  {
    const s = slide("Même fonction, deux références",
      "Même fonction logique en TTL (74xx) et en CMOS (40xx). La porte NON-OU standard de la série 74 est le 7402 (4 × NON-OU à 2 entrées, Floyd figure 3-62) ; le 7428 est une version « buffer » de la même fonction.\n" +
      "Symbole selon CEI 60617-12 : rectangle avec le qualificatif « & », cercle de négation en sortie. Équation (notation du Floyd) : Y = A·B surligné.\n" +
      "À souligner : la fonction est la même, mais le brochage et la tension d'alimentation diffèrent. Exemple : le 7400 et le 4011 sont tous les deux 4 × NON-ET, mais les broches des portes ne sont pas au même endroit. On ne remplace jamais l'un par l'autre sans regarder les deux fiches techniques.\n" +
      "Les portes elles-mêmes (tables de vérité, chronogrammes) sont traitées dans la présentation 120.");
    s.addTable([
      [cell("TTL", H), cell("CMOS", H), cell("Fonction", H)],
      [cell("7400"), cell("4011"), cell("4 portes NON-ET (NAND), 2 entrées", { align: "left" })],
      [cell("7402"), cell("4001"), cell("4 portes NON-OU (NOR), 2 entrées", { align: "left" })],
      [cell("7404"), cell("4069"), cell("6 inverseurs (NON)", { align: "left" })],
      [cell("7408"), cell("4081"), cell("4 portes ET (AND), 2 entrées", { align: "left" })],
      [cell("7432"), cell("4071"), cell("4 portes OU (OR), 2 entrées", { align: "left" })],
    ], { x: 0.5, y: 0.95, w: 5.6, colW: [0.95, 0.95, 3.7], rowH: 0.42, border: BORDER, fontSize: 12 });
    frame(s, 6.4, 0.95, 3.1, 2.5);
    txt(s, "Symbole CEI : NON-ET", { x: 6.5, y: 1.02, w: 2.9, h: 0.3, fontSize: 12, bold: true, color: BLUE, align: "center" });
    nandCEI(s, 7.4, 1.45, 1);
    eqImg(s, "eq_NON-ET.png", DATA.GATES["NON-ET"][14], 7.15, 2.75, 1.7, 0.5);
    frame(s, 0.5, 3.75, 5.6, 0.75);
    txt(s, "Même fonction ≠ même brochage ni même alimentation : on vérifie toujours la fiche technique.", { x: 0.65, y: 3.78, w: 5.3, h: 0.7, fontSize: 12.5, bold: true, color: RED, valign: "middle" });
    life(s, 6.4, 3.6, 3.1, 1.95, [
      "Un 7400 manque au magasin : le 74HC00 a le même brochage, pas le 4011.",
      "Les deux derniers chiffres (00, 02, 04, 08…) indiquent la fonction dans toute la série 74.",
    ], 10.5);
  }

  // ============================== 5. LIRE UNE RÉFÉRENCE (nouveau)
  {
    const s = slide("Lire une référence de CI",
      "Floyd 3-8 p. 146 : dans 74xxyy, 74 = CI logique à fonction fixe de la série 74, xx = technologie, yy = fonction. Le préfixe 54 désigne la version militaire (figure 3-65 du Floyd).\n" +
      "Préfixe et suffixe dépendent du fabricant : SN (Texas Instruments), M (STMicroelectronics), MC (onsemi)… La lettre finale donne le boîtier ; la liste exacte est dans la fiche technique, rubrique « Ordering information ».\n" +
      "Exemples Texas Instruments : SN74HCT00N = DIP 14 ; SN74HCT00D = SOIC 14. CD4011BE : CD = série 4000, 4011 = 4 × NON-ET, B = version à sorties tamponnées, E = DIP.\n" +
      "Activité : faire décoder une référence lue sur un CI de la caisse de composants.");
    const parts = [["SN", "fabricant", "Texas Instruments", GR], ["74", "plage", "commerciale\n(54 : militaire)", NAVY], ["HCT", "technologie", "CMOS, entrées TTL", BLUE],
      ["00", "fonction", "4 portes NON-ET", NAVY], ["N", "boîtier", "DIP 14 (D : SOIC)", GR]];
    const W = [1.25, 1.25, 1.6, 1.25, 1.25];
    let x = 0.5;
    parts.forEach(([code, lab, det, col], k) => {
      const w = W[k] + 0.35;
      s.addShape(pres.shapes.RECTANGLE, { x, y: 1.0, w: w - 0.1, h: 0.95, fill: { color: col }, line: { color: col } });
      txt(s, code, { x, y: 1.0, w: w - 0.1, h: 0.95, fontSize: 30, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
      txt(s, lab, { x, y: 2.05, w: w - 0.1, h: 0.3, fontSize: 12.5, bold: true, color: col === GR ? K : col, align: "center" });
      txt(s, det, { x, y: 2.37, w: w - 0.1, h: 0.55, fontSize: 11, color: GR, align: "center" });
      x += w;
    });
    boxTitle(s, 0.5, 3.1, 4.4, 1.15, "Série 4000 : CD4011BE", ["CD : série 4000 · 4011 : 4 portes NON-ET", "B : sorties tamponnées · E : boîtier DIP"], 11, true);
    boxTitle(s, 5.1, 3.1, 4.4, 1.15, "Même fonction, autre fabricant", ["M74HCT00 (ST) = SN74HCT00 (TI)", "La fiche liste les boîtiers : « Ordering information »"], 11, true);
    life(s, 0.5, 4.4, 9.0, 1.15, [
      "Au magasin ou chez un distributeur, on cherche d'abord la fonction (74HCT00), puis on choisit le boîtier : DIP pour la breadboard, SOIC pour une carte en série.",
      "Une référence notée seulement « 74HCT00 » sur un schéma laisse le choix du fabricant.",
    ], 10.5);
    s.addText([{ text: "Source : ", options: { color: GR } }, FLOYD("Floyd 3-8 p. 146", 146)], { x: 6.9, y: 0.6, w: 2.6, h: 0.25, fontFace: F, fontSize: 9.5, color: GR, margin: 0, align: "right" });
  }

  // ============================== 6. SIX CARACTÉRISTIQUES
  {
    const s = slide("Six caractéristiques pour comparer les familles",
      "Tableau de nextecmedia 4.1. Faire remarquer que chacune de ces lignes se retrouve dans une fiche technique : on y reviendra aux diapositives 14 à 18.\n" +
      "Niveau d'entrée : plage de tensions reconnue comme 0 ou comme 1. Niveau de sortie : tension garantie à l'état haut ou bas. C'est la comparaison des deux qui dit si deux CI peuvent se parler (diapositive 17).");
    const p = [["Tension d'alimentation", "5 V (TTL), 3,3 V (CMOS moderne)"], ["Consommation de courant", "courant absorbé par le CI"],
      ["Niveau d'entrée", "tensions reconnues comme 0 ou 1"], ["Niveau de sortie", "tension fournie à l'état High / Low"],
      ["Vitesse de commutation", "vitesse du passage de 0 à 1"], ["Résistance aux perturbations", "immunité de la famille au bruit"]];
    p.forEach(([h, d], k) => {
      const col = k % 3, row = Math.floor(k / 3);
      const x = 0.5 + col * 3.05, y = 1.0 + row * 1.6;
      card(s, x, y, 2.9, 1.4);
      badge(s, x + 0.15, y + 0.15, String(k + 1), 0.38);
      txt(s, h, { x: x + 0.65, y: y + 0.12, w: 2.15, h: 0.5, fontSize: 13, bold: true, valign: "middle" });
      txt(s, d, { x: x + 0.15, y: y + 0.72, w: 2.6, h: 0.6, fontSize: 11.5, color: GR });
    });
    life(s, 0.5, 4.3, 9.0, 1.25, [
      "Au moment de choisir un CI chez un distributeur (DigiKey, Distrelec…), ce sont ces critères qu'on filtre.",
      "Un appareil sur batterie privilégie la consommation ; un appareil de mesure rapide, la vitesse.",
    ]);
  }

  // ============================== 7. ALIMENTATION ET CONSOMMATION
  {
    const s = slide("Tension d'alimentation et consommation",
      "Les familles récentes baissent la tension d'alimentation : moins de pertes, vitesse plus élevée, idéal sur batterie (technologie 3 V).\n" +
      "Revers : l'écart entre les niveaux Low et High (marge de bruit) diminue, le circuit devient plus sensible aux perturbations.\n" +
      "Consommation : sur batterie, elle fixe l'autonomie ; avec une forte densité d'intégration (processeurs), la chaleur à évacuer devient un problème. Floyd 3-8 p. 153 : un CMOS HC consomme environ 2,75 µW par porte au repos et 600 µW par porte à 1 MHz ; la consommation CMOS augmente avec la fréquence.\n" +
      "Exemple concret : un processeur de smartphone tourne autour de 1 V au cœur et est entouré de régulateurs qui fournissent 1,8 V et 3,3 V aux autres CI.");
    [["5 V", "TTL classique", NAVY], ["3,3 V", "CMOS moderne", BLUE]].forEach(([v, l, col], k) => {
      const x = 0.5 + k * 2.25;
      card(s, x, 0.95, 2.1, 1.55);
      txt(s, v, { x, y: 1.0, w: 2.1, h: 0.95, fontSize: 38, bold: true, color: col, align: "center", valign: "middle" });
      txt(s, l, { x, y: 1.95, w: 2.1, h: 0.4, fontSize: 12, color: GR, align: "center" });
    });
    s.addShape(pres.shapes.RIGHT_ARROW, { x: 0.5, y: 2.7, w: 4.35, h: 0.5, fill: { color: NAVY }, line: { color: NAVY } });
    txt(s, "Tendance : tensions en baisse", { x: 0.65, y: 2.7, w: 3.9, h: 0.5, fontSize: 12, bold: true, color: "FFFFFF", valign: "middle" });
    txt(s, [{ text: "+ ", options: { bold: true, color: BLUE } }, { text: "moins de pertes, plus rapide, idéal sur batterie", options: { breakLine: true } },
      { text: "− ", options: { bold: true, color: RED } }, { text: "marge de bruit plus petite : plus sensible aux perturbations" }],
      { x: 0.5, y: 3.35, w: 4.4, h: 0.85, fontSize: 12.5, paraSpaceAfter: 4 });
    boxTitle(s, 5.1, 0.95, 4.4, 2.15, "Consommation", [
      "Sur batterie : elle fixe l'autonomie.",
      "Forte densité d'intégration : la chaleur à évacuer devient un problème.",
      "En CMOS, elle augmente avec la fréquence.",
    ], 12, true);
    life(s, 5.1, 3.25, 4.4, 2.3, [
      "Smartphone : le cœur du processeur tourne vers 1 V, les autres CI en 1,8 V et 3,3 V.",
      "Un capteur sans fil sur pile doit durer des années : on choisit du CMOS basse consommation.",
      "Un PC a besoin d'un radiateur et d'un ventilateur pour évacuer la chaleur du processeur.",
    ]);
  }

  // ============================== 8. TEMPÉRATURE · VITESSE · COURANTS DE SORTIE
  {
    const s = slide("Température, vitesse et courant de sortie",
      "Plages de température (valables pour tous les CI) : Consumer 0 à 70 °C, Industrial −40 à 85 °C, Military −55 à 125 °C. La référence d'un CI indique sa plage (préfixe 54 ou lettre du suffixe).\n" +
      "Vitesse : on adapte la vitesse de la logique aux besoins. Plus c'est rapide, plus c'est sensible aux perturbations.\n" +
      "Courant de sortie : pour alimenter directement un afficheur 7 segments ou une LED de forte intensité, certaines familles fournissent plus de 30 mA, par exemple les sorties à collecteur ouvert. Sinon on ajoute un transistor ou un driver.");
    txt(s, "Plages de température", { x: 0.5, y: 0.95, w: 5.0, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    const x0 = 1.95, x1 = 5.5, tmin = -60, tmax = 130, X = (t) => x0 + (t - tmin) / (tmax - tmin) * (x1 - x0);
    [["Consumer", 0, 70, BLUE], ["Industrial", -40, 85, "1B5FA8"], ["Military", -55, 125, NAVY]].forEach(([l, a, b, col], k) => {
      const y = 1.4 + k * 0.62;
      txt(s, l, { x: 0.5, y, w: 1.4, h: 0.45, fontSize: 12.5, bold: true, valign: "middle" });
      s.addShape(pres.shapes.RECTANGLE, { x: X(a), y, w: X(b) - X(a), h: 0.45, fill: { color: col }, line: { color: col } });
      txt(s, `${a < 0 ? "−" + (-a) : a} … ${b} °C`, { x: X(a), y, w: X(b) - X(a), h: 0.45, fontSize: 11, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    });
    const ya = 3.32;
    s.addShape(pres.shapes.LINE, { x: x0, y: ya, w: x1 - x0, h: 0, line: { color: GR, width: 1 } });
    [-40, 0, 40, 85, 125].forEach(t => {
      s.addShape(pres.shapes.LINE, { x: X(t), y: ya - 0.05, w: 0, h: 0.1, line: { color: GR, width: 1 } });
      txt(s, `${t < 0 ? "−" + (-t) : t}`, { x: X(t) - 0.3, y: ya + 0.07, w: 0.6, h: 0.22, fontSize: 9.5, color: GR, align: "center" });
    });
    txt(s, "ϑ en °C", { x: x1 - 0.8, y: ya + 0.3, w: 0.8, h: 0.22, fontSize: 9.5, color: GR, align: "right" });
    boxTitle(s, 5.85, 0.95, 3.65, 1.3, "Vitesse de commutation", ["Adaptée aux besoins de l'application.", "Plus rapide = plus sensible au bruit."], 11, true);
    boxTitle(s, 5.85, 2.4, 3.65, 1.3, "Courant de sortie", ["Afficheur 7 segments : > 30 mA.", "Ex. sorties à collecteur ouvert."], 11, true);
    life(s, 0.5, 3.95, 9.0, 1.6, [
      "Une électronique de voiture ou de machine en extérieur doit fonctionner de −40 °C à 85 °C : on commande des CI « Industrial » ou « Automotive ».",
      "Un jouet ou un appareil de salon peut se contenter de la plage « Consumer ».",
      "Une sortie de CI ne pilote pas un relais ou un moteur : on passe par un transistor, comme vu au laboratoire.",
    ]);
  }

  // ============================== 9. DANS LE BOÎTIER (nouveau)
  {
    const s = slide("Dans le boîtier : la puce",
      "Photos reprises de l'ancienne présentation « Circuits intégrés logiques » (ETML, 2016).\n" +
      "À gauche : la puce d'un 74HC00 (vue au microscope), quelques millimètres de côté. On distingue les 4 portes et les plots de connexion sur le pourtour. À droite : un boîtier ouvert, avec les fils de liaison (bonding) entre la puce et les broches.\n" +
      "Floyd figure 3-65 (fiche MC74HC00A) : « Chip Complexity: 32 FETs or 8 Equivalent Gates », soit 32 transistors pour 4 portes NON-ET.\n" +
      "Le boîtier protège la puce, la relie aux broches et évacue la chaleur. Le même circuit existe dans plusieurs boîtiers (diapositive suivante).");
    img(s, "fig_puce.jpg", 0.5, 0.95, 3.0, 3.25);
    img(s, "fig_puce_ouverte.jpg", 3.75, 0.95, 3.0, 3.25);
    txt(s, "Puce d'un 74HC00 : quelques millimètres", { x: 0.5, y: 4.0, w: 3.2, h: 0.3, fontSize: 10, italic: true, color: GR, align: "center" });
    txt(s, "Boîtier ouvert : fils de liaison", { x: 3.75, y: 4.0, w: 3.6, h: 0.3, fontSize: 10, italic: true, color: GR, align: "center" });
    card(s, 7.05, 0.95, 2.45, 1.45, NAVY);
    txt(s, "32", { x: 7.05, y: 1.0, w: 2.45, h: 0.8, fontSize: 40, bold: true, color: LBLUE, align: "center", valign: "middle" });
    txt(s, "transistors dans un 74HC00 (4 portes)", { x: 7.15, y: 1.8, w: 2.25, h: 0.55, fontSize: 10.5, color: "FFFFFF", align: "center" });
    boxTitle(s, 7.05, 2.55, 2.45, 1.7, "Le boîtier", ["protège la puce", "la relie aux broches", "évacue la chaleur"], 11, true);
    life(s, 0.5, 4.4, 9.0, 1.15, [
      "Un processeur de smartphone loge plusieurs milliards de transistors sur une puce à peine plus grande que celle d'un 74HC00.",
      "Une décharge électrostatique peut détruire ces transistors : on manipule les CI CMOS avec un bracelet relié à la terre (Floyd p. 149).",
    ], 10.5);
  }

  // ============================== 10. BOÎTIERS
  {
    const s = slide("Boîtiers : un même CI, plusieurs formes",
      "Image de nextecmedia 4.1. Le même circuit (ex. 74HC00) existe en DIP (traversant), SOIC, TSSOP… La fiche technique donne les dimensions et les références de commande de chaque boîtier. Floyd 1-6 p. 26-28 et 3-8 p. 149 (figure 3-64).\n" +
      "Faire circuler des échantillons réels si disponibles à l'atelier (DIP, SOIC, QFP).\n" +
      "Repère de la broche 1 : encoche ou point sur le boîtier. La numérotation tourne dans le sens inverse des aiguilles d'une montre, vue de dessus.");
    img(s, "fig_boitiers.png", 0.5, 0.95, 5.6);
    boxTitle(s, 6.35, 0.95, 3.15, 2.35, "Repères", [
      "CMS (SMD) : montage en surface.",
      "SOIC, SOT, QFP : broches sur les côtés.",
      "PLCC, LCCC : broches sur 4 côtés.",
      "BGA : billes sous le boîtier.",
    ], 11.5, true);
    life(s, 6.35, 3.45, 3.15, 2.1, [
      "Breadboard et prototypes : boîtier DIP, facile à souder.",
      "Production en série : CMS, posés par une machine.",
      "BGA : impossible à souder au fer, il faut un four.",
    ], 10.5);
  }

  // ============================== 11. AFFECTATION DES BROCHES
  {
    const s = slide("Affectation des broches",
      "Un CI possède un nombre fixe de broches (8, 14, 16…), numérotées selon un schéma fixe et attribuées à des fonctions (nextecmedia 4.1).\n" +
      "Exemple du 74HCT00 à droite : broche 14 = V_CC, broche 7 = GND. On repère la broche 1 grâce à l'encoche.\n" +
      "Erreur classique en laboratoire : inverser l'alimentation (V_CC et GND). Le CI chauffe et meurt en quelques secondes. Toujours vérifier le brochage avant la mise sous tension.\n" +
      "Une entrée CMOS non utilisée ne doit jamais rester en l'air : on la relie à V_CC ou à GND.");
    s.addTable([
      [cell("Broche", H), cell("Rôle", H)],
      [cell("V_{CC} / V_{DD}", { bold: true }), cell("alimentation (+5 V TTL, +3,3 V CMOS moderne)", { align: "left" })],
      [cell("GND", { bold: true }), cell("masse : référence de toutes les tensions", { align: "left" })],
      [cell("Entrées", { bold: true }), cell("signaux qui pilotent le CI", { align: "left" })],
      [cell("Sorties", { bold: true }), cell("résultat de la fonction logique", { align: "left" })],
      [cell("Commande", { bold: true }), cell("Enable, Clock, Reset…", { align: "left" })],
      [cell("NC", { bold: true }), cell("No Connection : non reliée", { align: "left" })],
    ], { x: 0.5, y: 0.95, w: 5.4, colW: [1.35, 4.05], rowH: 0.4, border: BORDER, fontSize: 11.5 });
    img(s, "fig_pinout.png", 6.5, 0.95, 2.7, 3.35);
    txt(s, "74HCT00 : 4 portes NON-ET", { x: 6.15, y: 4.35, w: 3.35, h: 0.25, fontSize: 10, italic: true, color: GR, align: "center" });
    life(s, 0.5, 3.95, 5.4, 1.6, [
      "Avant de câbler sur breadboard : repérer la broche 1, puis V_{CC} et GND.",
      "Alimentation inversée = CI détruit en quelques secondes.",
      "Entrée CMOS inutilisée : la relier à V_{CC} ou à GND, jamais en l'air.",
    ], 10.5);
  }

  // ============================== 12. CHOIX DE FAMILLE ET CONVERTISSEUR DE NIVEAUX
  {
    const s = slide("Choisir la famille, adapter les niveaux",
      "Règle (nextecmedia 4.1) : on utilise en principe une seule famille dans un même circuit, pour éviter les problèmes de tension d'alimentation, de niveaux et de temps de commutation.\n" +
      "FPGA et EPLD sont construits en CMOS mais avec d'autres niveaux de signal.\n" +
      "Convertisseur de niveaux (level shifter) : adapte les tensions entre deux circuits de niveaux différents (5 V ↔ 3,3 V ; 3,3 V ↔ 1,8 V). Unidirectionnel : un seul sens. Bidirectionnel : les deux sens, par exemple pour un bus I²C.\n" +
      "Réponse à la question de départ : la sortie 5 V de l'Arduino dépasse la tension maximale de l'entrée 3,3 V du capteur → risque de destruction. Dans l'autre sens, le 3,3 V du capteur n'est pas un 1 garanti pour une entrée 74HC alimentée en 5 V (V_IH = 3,5 V, diapositive 17). Solution : un module convertisseur de niveaux bidirectionnel entre les deux.");
    card(s, 0.5, 0.95, 9.0, 0.85);
    badge(s, 0.65, 1.17, "!", 0.4);
    txt(s, [{ text: "Règle : une seule famille par circuit. ", options: { bold: true } }, { text: "Attention : FPGA et EPLD sont en CMOS, mais avec d'autres niveaux." }],
      { x: 1.2, y: 0.95, w: 8.15, h: 0.85, fontSize: 12.5, valign: "middle" });
    const y = 2.05;
    const box = (x, w, t, sub, col) => {
      s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.95, fill: { color: col }, line: { color: col } });
      txt(s, t, { x, y: y + 0.1, w, h: 0.42, fontSize: 17, bold: true, color: "FFFFFF", align: "center" });
      txt(s, sub, { x, y: y + 0.55, w, h: 0.3, fontSize: 10.5, color: "FFFFFF", align: "center" });
    };
    box(0.5, 2.3, "5 V", "ex. Arduino Uno", NAVY);
    box(3.85, 2.3, "Level shifter", "convertisseur de niveaux", BLUE);
    box(7.2, 2.3, "3,3 V", "ex. capteur", NAVY);
    [2.85, 6.2].forEach(x => s.addShape(pres.shapes.LEFT_RIGHT_ARROW, { x, y: y + 0.28, w: 0.95, h: 0.4, fill: { color: LBLUE }, line: { color: LBLUE } }));
    txt(s, [{ text: "Unidirectionnel : ", options: { bold: true, color: NAVY } }, { text: "un seul sens (ex. 5 V → 3,3 V)" }], { x: 0.5, y: 3.12, w: 4.4, h: 0.35, fontSize: 12 });
    txt(s, [{ text: "Bidirectionnel : ", options: { bold: true, color: BLUE } }, { text: "dans les deux sens (ex. bus I²C)" }], { x: 5.1, y: 3.12, w: 4.4, h: 0.35, fontSize: 12 });
    frame(s, 0.5, 3.6, 5.0, 1.95);
    txt(s, "Réponse à la question de départ", { x: 0.65, y: 3.67, w: 4.7, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, "Non : le 5 V de l'Arduino dépasse la tension maximale de l'entrée 3,3 V du capteur, qui peut être détruite. Dans l'autre sens, 3,3 V n'est pas toujours reconnu comme un 1 (diapositive 17). On intercale un convertisseur de niveaux bidirectionnel.", { x: 0.65, y: 4.0, w: 4.7, h: 1.45, fontSize: 11.5 });
    life(s, 5.7, 3.6, 3.8, 1.95, [
      "Modules « level shifter » à quelques francs : Arduino ↔ capteurs, écrans, cartes SD.",
      "Raspberry Pi : entrées 3,3 V seulement, jamais de 5 V direct.",
    ], 10.5);
  }

  // ============================== 13. APPLICATIONS
  {
    const s = slide("Où trouve-t-on ces circuits ?",
      "nextecmedia 4.1 (exemples pratiques) : trois grandes catégories d'applications.\n" +
      "Microcontrôleur : processeur, mémoire (Flash/RAM) et périphériques (ADC, PWM, UART) sur une seule puce (ATmega328P, STM32). Remplace des circuits complexes par un composant programmable.\n" +
      "CI logiques : portes, multiplexeurs, bascules. Exemples : anti-rebond d'un bouton avec des portes NON-ET, décodage d'adresses avec un démultiplexeur 74HC138.\n" +
      "CI mémoire : EEPROM 24C256 (paramètres conservés sans alimentation), SRAM 23LC1024 (tampon rapide). Mémoire firmware des microcontrôleurs, tampon des modules Ethernet.\n" +
      "Domaines : informatique, téléphones et électronique grand public, automobile (gestion moteur, sécurité), automatisation et robotique.");
    const a = [
      ["Microcontrôleurs", "processeur + mémoire + périphériques (ADC, PWM, UART) sur une puce", "ATmega328P, STM32 : machine à laver, robot"],
      ["CI logiques", "portes, multiplexeurs, bascules", "anti-rebond (NON-ET), décodage d'adresses (74HC138)"],
      ["CI mémoire", "volatile (SRAM) ou non volatile (EEPROM)", "24C256 : réglages · 23LC1024 : tampon rapide"],
    ];
    a.forEach(([h, d, e], k) => {
      const x = 0.5 + k * 3.05, w = 2.9;
      card(s, x, 0.95, w, 2.85);
      badge(s, x + 0.15, 1.08, String(k + 1), 0.38);
      txt(s, h, { x: x + 0.65, y: 1.06, w: w - 0.75, h: 0.42, fontSize: 14, bold: true, valign: "middle" });
      txt(s, d, { x: x + 0.15, y: 1.65, w: w - 0.3, h: 0.95, fontSize: 12 });
      txt(s, e, { x: x + 0.15, y: 2.65, w: w - 0.3, h: 1.05, fontSize: 11, italic: true, color: BLUE });
    });
    txt(s, "Domaines d'application", { x: 0.5, y: 4.0, w: 9.0, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    [["Informatique", "processeurs, mémoires"], ["Grand public", "smartphones, TV, consoles"], ["Automobile", "gestion moteur, sécurité"], ["Industrie", "automates, robots"]].forEach(([h, d], k) => {
      const x = 0.5 + k * 2.28;
      frame(s, x, 4.38, 2.15, 1.15);
      txt(s, h, { x: x + 0.12, y: 4.45, w: 1.9, h: 0.35, fontSize: 12.5, bold: true });
      txt(s, d, { x: x + 0.12, y: 4.82, w: 1.9, h: 0.6, fontSize: 11, color: GR });
    });
  }

  // ============================== 14. LA FICHE TECHNIQUE
  {
    const s = slide("La fiche technique (datasheet)",
      "La fiche technique rassemble les informations d'un composant. Pour relier plusieurs composants, il faut connaître leur fonction interne et leurs détails techniques (nextecmedia 4.1).\n" +
      "Structure type : description de la fonction, tables de vérité, affectation des raccordements, valeurs limites et caractéristiques, diagrammes, dimensions mécaniques et boîtier, circuits d'application et de test. Elle est en général en anglais. Floyd 3-8 p. 151-152 montre deux fiches partielles (74HC00A et 74LS00).\n" +
      "Exemple suivi jusqu'à la diapositive 18 : M74HCT00 de STMicroelectronics. Distribuer la fiche complète. Faire repérer en binôme : fabricant, désignation, description abrégée, boîtiers et codes de commande.");
    const parts = ["Description de la fonction", "Tables de vérité", "Affectation des raccordements", "Valeurs limites et caractéristiques", "Diagrammes", "Dimensions mécaniques / boîtier", "Circuits d'application et de test"];
    parts.forEach((p, k) => {
      const y = 1.0 + k * 0.45;
      badge(s, 0.5, y, String(k + 1), 0.34);
      txt(s, p, { x: 0.98, y, w: 3.7, h: 0.34, fontSize: 12.5, valign: "middle" });
    });
    img(s, "fig_datasheet.png", 4.85, 0.95, 4.65, 3.2);
    life(s, 0.5, 4.3, 9.0, 1.25, [
      "Avant de souder ou de commander un composant, l'électronicien·ne télécharge sa fiche technique (site du fabricant ou du distributeur).",
      "Les fiches sont presque toujours en anglais : on apprend à reconnaître les mots clés (supply voltage, pin connection, ratings…).",
    ]);
  }

  // ============================== 15. BROCHAGE ET SYMBOLE CEI DU M74HCT00
  {
    const s = slide("M74HCT00 : brochage et symbole CEI",
      "Lecture du brochage : broche 14 = V_CC, broche 7 = GND ; quatre portes indépendantes (1A, 1B → 1Y, etc.).\n" +
      "Le symbole CEI regroupe les quatre portes sous le qualificatif « & ». La fiche utilise le triangle de polarité en sortie ; le cercle de négation de la diapositive 4 est l'autre forme prévue par la CEI 60617-12, celle utilisée dans nos supports.\n" +
      "Table de vérité : entrées du poids fort (B) au poids faible (A), puis la sortie, comme dans tout le cours. Dans la fiche, L = 0 et H = 1. Faire vérifier une ligne de la table au laboratoire avec deux interrupteurs et une LED.");
    img(s, "fig_brochage_cei.png", 0.5, 0.95, 6.3);
    txt(s, "Table de vérité", { x: 7.05, y: 0.95, w: 2.4, h: 0.3, fontSize: 13, bold: true, color: BLUE, align: "center" });
    const tv = [["B", "A", "Y"]].concat(DATA.GATES["NON-ET"][12].map(r => r.map(String)));   // poids fort → poids faible
    s.addTable(tv.map((r, i) => r.map((c, j) => cell(c, i === 0 ? H : (j === 2 ? { bold: true, color: BLUE } : {})))),
      { x: 7.1, y: 1.32, w: 2.3, colW: [0.77, 0.77, 0.76], rowH: 0.38, border: BORDER });
    frame(s, 0.5, 3.6, 4.4, 1.95);
    txt(s, "Lire le brochage", { x: 0.65, y: 3.67, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    bullets(s, ["Broche 14 : V_{CC} · broche 7 : GND.", "4 portes indépendantes : 1A, 1B → 1Y…", "Symbole CEI : un rectangle « & » commun aux 4 portes."], { x: 0.65, y: 4.02, w: 4.1, h: 1.45, fontSize: 11.5 });
    life(s, 5.1, 3.6, 4.4, 1.95, [
      "Au laboratoire : deux interrupteurs sur A et B, une LED sur Y, et on vérifie la table ligne par ligne.",
      "En fiche technique : L = Low = 0, H = High = 1.",
    ], 10.5);
  }

  // ============================== 16. NIVEAUX D'ENTRÉE ET VALEURS LIMITES
  {
    const s = slide("Niveaux d'entrée et valeurs limites",
      "Objectif LZ_4255. Valeurs tirées de la fiche M74HCT00 (DC specifications, recommended operating conditions, absolute maximum ratings).\n" +
      "V_IH min = 2 V : toute tension au-dessus est reconnue comme 1. V_IL max = 0,8 V : toute tension en dessous est reconnue comme 0. Entre les deux, l'état n'est pas garanti. Le Floyd (3-8 p. 154) note ces tensions V_EH et V_EB.\n" +
      "Faire dessiner cette échelle des niveaux par les apprenti·e·s dans leur cahier.\n" +
      "Valeurs limites absolues : à ne jamais dépasser, sinon le CI peut être détruit. Le bon fonctionnement n'est garanti que dans les conditions recommandées (V_CC de 4,5 à 5,5 V).");
    const bx = 0.95, by = 1.0, bh = 4.4, bw = 0.8, V = (v) => by + bh - v / 5 * bh;
    s.addShape(pres.shapes.RECTANGLE, { x: bx, y: V(5), w: bw, h: V(2) - V(5), fill: { color: BLUE }, line: { color: BLUE } });
    s.addShape(pres.shapes.RECTANGLE, { x: bx, y: V(2), w: bw, h: V(0.8) - V(2), fill: { color: "D5DDDF" }, line: { color: "D5DDDF" } });
    s.addShape(pres.shapes.RECTANGLE, { x: bx, y: V(0.8), w: bw, h: V(0) - V(0.8), fill: { color: NAVY }, line: { color: NAVY } });
    txt(s, "1", { x: bx, y: V(5), w: bw, h: V(2) - V(5), fontSize: 28, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    txt(s, "0", { x: bx, y: V(0.8), w: bw, h: V(0) - V(0.8), fontSize: 16, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    [[5, "5 V"], [2, "2 V"], [0.8, "0,8 V"], [0, "0 V"]].forEach(([v, l]) => txt(s, l, { x: 0.3, y: V(v) - 0.12, w: 0.58, h: 0.24, fontSize: 10.5, color: GR, align: "right" }));
    txt(s, [{ text: "V_{IH} min = 2 V", options: { bold: true, color: BLUE, breakLine: true } }, { text: "au-dessus : reconnu comme 1" }], { x: 1.9, y: V(3.9), w: 2.4, h: 0.55, fontSize: 11.5 });
    txt(s, [{ text: "zone interdite", options: { bold: true, breakLine: true } }, { text: "état non garanti" }], { x: 1.9, y: V(1.72), w: 2.4, h: 0.55, fontSize: 11.5, color: GR });
    txt(s, [{ text: "V_{IL} max = 0,8 V", options: { bold: true, color: NAVY, breakLine: true } }, { text: "en dessous : reconnu comme 0" }], { x: 1.9, y: V(0.72), w: 2.4, h: 0.55, fontSize: 11.5 });
    s.addTable([
      [cell("Grandeur", H), cell("Recommandé", H), cell("Limite absolue", H)],
      [cell("V_{CC}", { bold: true }), cell("4,5 … 5,5 V"), cell("−0,5 … +7 V")],
      [cell("Température", { bold: true }), cell("−55 … 125 °C"), cell("stockage −65 … 150 °C")],
      [cell("Courant de sortie", { bold: true }), cell("non indiqué", { fontSize: 10 }), cell("± 25 mA")],
    ], { x: 4.55, y: 1.0, w: 4.95, colW: [1.6, 1.5, 1.85], rowH: 0.42, border: BORDER, fontSize: 11 });
    frame(s, 4.55, 2.9, 4.95, 1.05);
    txt(s, [{ text: "Limite absolue : ", options: { bold: true, color: RED } }, { text: "à ne jamais dépasser, sinon le CI peut être détruit." }], { x: 4.7, y: 2.93, w: 4.65, h: 1.0, fontSize: 12.5, valign: "middle" });
    life(s, 4.55, 4.1, 4.95, 1.45, [
      "Une entrée 3,3 V reliée à une sortie 5 V dépasse sa limite : c'est la question de départ.",
      "En dépannage, on mesure la tension d'une entrée et on la compare à V_{IH} et V_{IL}.",
    ], 10.5);
  }

  // ============================== 17. NIVEAUX DE SORTIE ET MARGE DE BRUIT (nouveau)
  {
    const s = slide("Niveaux de sortie et marge de bruit",
      "Objectif LZ_4255. Valeurs garanties du Floyd 3-8 p. 154 (V_CC = 5 V) : TTL V_IL = 0,8 V, V_IH = 2 V, V_OL = 0,4 V, V_OH = 2,4 V ; CMOS 5 V (74HC) V_IL = 1,5 V, V_IH = 3,5 V, V_OL = 0,33 V, V_OH = 4,4 V. Le Floyd écrit V_EB, V_EH, V_SB, V_SH.\n" +
      "Marge de bruit : réserve de tension entre ce que la sortie garantit et ce que l'entrée exige. N_H = V_OH − V_IH ; N_L = V_IL − V_OL. TTL : 0,4 V et 0,4 V. 74HC : 0,9 V et 1,17 V. Un parasite plus petit que la marge ne change pas l'état lu.\n" +
      "Règle de compatibilité : une sortie peut piloter une entrée si V_OH(sortie) ≥ V_IH(entrée) et V_OL(sortie) ≤ V_IL(entrée).\n" +
      "Exemples : TTL → 74HC : 2,4 V < 3,5 V, le 1 n'est pas garanti → on prend un 74HCT (V_IH = 2 V). 74HC → TTL : 4,4 V ≥ 2 V et 0,33 V ≤ 0,8 V → compatible. Sortie 3,3 V → entrée 74HC sous 5 V : au plus 3,3 V < 3,5 V → pas de 1 garanti (fin de la réponse à la question de départ).\n" +
      "À faire calculer : les marges de 74HC → TTL (2,4 V et 0,47 V). Exercice complet : fiche 110, N°3.");
    img(s, "fig_marges.png", 0.5, 0.95, 5.55, 3.4);
    frame(s, 6.25, 0.95, 3.25, 1.75);
    txt(s, "Compatible si…", { x: 6.4, y: 1.02, w: 3.0, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, [{ text: "V_{OH}(sortie) ≥ V_{IH}(entrée)", options: { bold: true, breakLine: true } }, { text: "et", options: { breakLine: true, color: GR } },
      { text: "V_{OL}(sortie) ≤ V_{IL}(entrée)", options: { bold: true } }], { x: 6.4, y: 1.4, w: 3.0, h: 1.2, fontSize: 12.5, align: "center", valign: "middle" });
    card(s, 6.25, 2.85, 3.25, 1.5);
    txt(s, "Exemples", { x: 6.4, y: 2.92, w: 3.0, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    bullets(s, ["TTL → 74HC : 2,4 V < 3,5 V ✗", "TTL → 74HCT : 2,4 V ≥ 2 V ✓", "3,3 V → 74HC (5 V) : 3,3 V < 3,5 V ✗"], { x: 6.4, y: 3.27, w: 3.05, h: 1.05, fontSize: 11 });
    life(s, 0.5, 4.5, 9.0, 1.05, [
      "Un câble long dans une machine capte des parasites : plus la marge de bruit est grande, plus la liaison est fiable.",
      "Une vieille carte TTL pilote une nouvelle carte : on choisit du 74HCT, pas du 74HC.",
    ], 10.5);
  }

  // ============================== 18. TEMPS DE PROPAGATION
  {
    const s = slide("Propriétés dynamiques : le temps de propagation",
      "Le temps de propagation est mesuré entre les points à 1,3 V du signal d'entrée et du signal de sortie. t_PHL : la sortie passe de High à Low ; t_PLH : de Low à High. t_THL et t_TLH sont les temps de descente et de montée de la sortie. Le Floyd (3-8 p. 152) écrit t_PHB et t_PBH.\n" +
      "Pour le 74HCT00, t_PD vaut 12 ns typique à V_CC = 4,5 V et t_PLH ≈ t_PHL (retards équilibrés).\n" +
      "Ordre de grandeur à faire calculer : 12 ns, c'est la durée d'une période d'un signal de 83 MHz. Si on met 10 portes en série, le retard total est de 120 ns.");
    img(s, "fig_propagation.png", 0.5, 0.95, 5.7, 3.6);
    card(s, 6.45, 0.95, 3.05, 1.5, NAVY);
    txt(s, "12 ns", { x: 6.45, y: 1.0, w: 3.05, h: 0.85, fontSize: 36, bold: true, color: LBLUE, align: "center", valign: "middle" });
    txt(s, "t_{PD} typique à V_{CC} = 4,5 V", { x: 6.45, y: 1.85, w: 3.05, h: 0.45, fontSize: 11.5, color: "FFFFFF", align: "center", valign: "middle" });
    txt(s, [{ text: "t_{PHL}", options: { bold: true, color: NAVY } }, { text: " : la sortie passe de High à Low", options: { breakLine: true } },
      { text: "t_{PLH}", options: { bold: true, color: BLUE } }, { text: " : la sortie passe de Low à High", options: { breakLine: true } },
      { text: "t_{THL} / t_{TLH}", options: { bold: true } }, { text: " : temps de descente / montée" }],
      { x: 6.45, y: 2.6, w: 3.05, h: 1.4, fontSize: 11.5, paraSpaceAfter: 5 });
    life(s, 0.5, 4.65, 9.0, 0.9, [
      "Dix portes en série font 120 ns de retard ; ce retard limite la fréquence maximale d'un circuit numérique.",
    ]);
  }

  // ============================== 19. À RETENIR · TICKET DE SORTIE
  {
    const s = slide("À retenir · ticket de sortie",
      "Synthèse (nextecmedia 4.1, « Signification des familles de circuits ») : niveaux compatibles entre CI d'une même famille, conception facilitée car les propriétés électriques sont connues et normalisées, remplacement et combinaison plus faciles.\n" +
      "Ticket de sortie (5 min, seul·e, sans support ; à ramasser). Réponses : 1) Non : V_OH(TTL) = 2,4 V < V_IH(74HC) = 3,5 V, le 1 n'est pas garanti ; il faut un 74HCT. 2) TTL : bipolaire, 5 V, gourmand ; CMOS : MOSFET, très faible consommation au repos. 3) V_IH min = 2 V et V_IL max = 0,8 V : 1,5 V n'est ni un 0 ni un 1 garanti. 4) Un convertisseur de niveaux (level shifter).\n" +
      "Ensuite : fiche 110 EX Familles de circuits logiques, puis auto-contrôle du chapitre 4 dans nextecmedia (liens sur la diapositive).");
    const r = [["Niveaux compatibles", "les CI d'une même famille se branchent sans adaptation"], ["Marge de bruit", "N_{H} = V_{OH} − V_{IH} · N_{L} = V_{IL} − V_{OL}"], ["Remplacement facile", "même famille : on échange et on combine les composants"]];
    r.forEach(([h, d], k) => {
      const x = 0.5 + k * 3.05;
      card(s, x, 0.95, 2.9, 1.3);
      txt(s, h, { x: x + 0.15, y: 1.02, w: 2.6, h: 0.35, fontSize: 13, bold: true, color: BLUE });
      txt(s, d, { x: x + 0.15, y: 1.4, w: 2.6, h: 0.8, fontSize: 11.5 });
    });
    frame(s, 0.5, 2.45, 9.0, 2.45);
    txt(s, "Ticket de sortie : seul·e, 5 minutes, sans support", { x: 0.65, y: 2.52, w: 8.7, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    [["1", "Une sortie TTL peut-elle piloter une entrée 74HC ? Justifie avec V_{OH} et V_{IH}."], ["2", "Cite une différence entre TTL et CMOS."],
     ["3", "74HCT00 : une entrée à 1,5 V est-elle lue comme 0 ou 1 ? Pourquoi ?"], ["4", "Que faut-il entre une sortie 5 V et une entrée 3,3 V ?"]].forEach((q, i) => {
      const x = 0.65 + (i % 2) * 4.45, y = 2.95 + Math.floor(i / 2) * 0.9;
      badge(s, x, y + 0.13, q[0], 0.34);
      txt(s, q[1], { x: x + 0.45, y, w: 3.85, h: 0.62, fontSize: 12, valign: "middle" });
    });
    card(s, 0.5, 5.02, 9.0, 0.55);
    s.addText([{ text: "Ensuite : ", options: { bold: true } }, { text: "fiche 110 EX Familles de circuits logiques · " },
      REF("auto-contrôle dans nextecmedia (4.1)"), { text: " · " }, FLOYD("Floyd 3-8 p. 146-155", 146)],
      { x: 0.65, y: 5.02, w: 8.7, h: 0.55, fontFace: F, fontSize: 11.5, color: NAVY, margin: 0, valign: "middle" });
  }

  // ============================== 20 à 22. EXERCICES · PAGE INTERACTIVE · ANIMATION
  exoSlide("110 EX", DATA.TEAMS["110"], [
    ["1", "Lire une référence de CI", "≈ 8 min · diapositives 4 et 5"], ["2", "Choisir le bon CI", "≈ 8 min · diapositives 3, 7 et 8"],
    ["3", "Les niveaux sont-ils compatibles ?", "≈ 12 min · diapositives 16 et 17"], ["4", "Lire la fiche technique du M74HCT00", "≈ 10 min · diapositives 14 à 18"],
    ["5", "Dépannage : mesurer les niveaux", "≈ 7 min · diapositives 11 et 16"]],
    "Tu fais ton stage au service de maintenance d'une entreprise d'embouteillage. La ligne de remplissage est pilotée par des cartes de plusieurs générations : une ancienne carte TTL, des cartes récentes en 74HC et un module à microcontrôleur alimenté en 3,3 V.",
    "En binôme, 45 min. Justifie chaque réponse avec une valeur : tension, courant, température ou temps. La fiche technique du M74HCT00 est distribuée avant le N°4.",
    ["Ce sont les vérifications d'un technicien de maintenance : lire une référence, comparer des niveaux, choisir une pièce de rechange qui convient."],
    "Fiche 110 EX Familles de circuits logiques (45 min, en binôme). Temps indicatifs : N°1 8 min, N°2 8 min, N°3 12 min, N°4 10 min, N°5 7 min. Distribuer la fiche technique M74HCT00 avant le N°4.\n" +
    "Correction en plénière, en faisant justifier chaque réponse par une valeur. Corrigé : 110 EX C Familles de circuits logiques (pour l'enseignant·e). Ramasser l'auto-évaluation.\n" +
    "Le lien vise le dossier Teams El_DT1/PMT&SBT : il fonctionne une fois le fichier déposé sous ce nom.");
  pageSlide("101", DATA.FILES["101"], DATA.TEAMS["101"], DATA.ART["101"], "shot_101.png",
    ["Lis la référence sur le CI", "Que lit l'entrée ?", "Peut-on relier ces deux circuits ?", "Le retard d'une chaîne de portes", "Choisis la bonne famille, le bon boîtier"],
    ["Les situations viennent de l'atelier, du magasin et du dépannage : ce sont les vérifications qu'un électronicien fait en entreprise.",
     "À refaire à la maison avant le test : chaque erreur est expliquée avec les valeurs."],
    "Page interactive 101 : un seul fichier .html, sans installation ni connexion. Cinq étapes ; chacune commence par une animation « Comprendre » reprise des diapositives (3 et 5, 16, 12 et 17, 18, 8 et 10), puis un exercice « À toi » corrigé tout de suite.\n" +
    "Utilisation : projeter l'animation d'une étape, faire répondre la classe, vérifier ensemble ; ou à faire à la maison. Le score n'est pas enregistré.\n" +
    "Déposer le fichier « 101 Familles de circuits logiques.html » dans le dossier Teams El_DT1/PMT&SBT : le lien de la diapositive vise ce chemin. Teams peut le télécharger au lieu de l'afficher : l'ouvrir alors dans Edge ou Chrome (l'aperçu de fichier n'exécute pas les animations).\n" +
    "Le lien « artefact claude.ai » ne fonctionne pour les apprenti·e·s qu'une fois l'artefact partagé depuis claude.ai.");
  videoSlide("105", DATA.FILES["105"], DATA.TEAMS["105"], "cover_105.png", "5 minutes",
    [["Lire une référence de CI", "SN74HCT00N, partie par partie"], ["Les niveaux d'entrée", "quand une tension devient un 0 ou un 1"],
     ["Compatibilité et marge de bruit", "TTL, 74HC et 74HCT"], ["Le convertisseur de niveaux", "Arduino 5 V et capteur 3,3 V"],
     ["Le temps de propagation", "quatre portes NON-ET en série"]],
    ["Pour réviser à la maison ou rattraper une absence : la vidéo reprend la leçon avec les mêmes situations que la présentation.",
     "Chaque partie commence par une carte de 13 s : la situation, la question et ce qu'on va voir."],
    "Animation 105 Familles de circuits logiques : 4 min 48, 1920 × 1080. La vidéo est intégrée à la présentation : elle se lit dans PowerPoint sans connexion (clic sur l'image en mode diaporama).\n" +
    "PowerPoint dans Teams ou dans le navigateur ne lit pas toujours une vidéo intégrée : utiliser alors le lien « La vidéo sur Teams » (fichier 105 Familles de circuits logiques.mp4, à déposer dans le dossier El_DT1/PMT&SBT).\n" +
    "Suggestion : la montrer en fin de leçon pour revoir les cinq points, ou la donner à regarder avant la fiche 110 EX.");
};
