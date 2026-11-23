// 100 Semi-conducteurs : diapositives (moteur : moteur/deck.js). TM2, semaine 1, ligne 10 du plan.
// Objectifs : LZ_1879 (C4), LZ_4066 (C2), LZ_4067 (C2). Pas de référence Floyd ni nextecmedia pour cette séance.
// Fil rouge : l'équipement de test de la ligne de production (situation de travail du champ LFB_El_Dim4).
// Niveau voulu par Gaël (11/23/2026) : clair et simple ; comprendre et savoir que ça existe, pas de calcul.
module.exports = function (E) {
  const { pres, DATA, NAVY, BLUE, LBLUE, TINT, K, GR, F, slide, txt, card, frame, badge, img, bullets, life,
    boxTitle, cell, H, BORDER, LZL, exoSlide, pageSlide, videoSlide, titreSlide } = E;
  const obj = (t, codes, fin) => [{ text: t + " (" }].concat(...codes.map((c, i) => i ? [{ text: ", " }, LZL(c)] : [LZL(c)]), [{ text: fin || ") ;" }]);

  // ============================== 1. TITRE · OBJECTIFS · QUESTION DE DÉPART
  titreSlide({
    titre: "Les semi-\nconducteurs",
    sousTitre: "Le matériau de tous les composants électroniques",
    objectifs: [obj("différencier les trois familles de matériaux", ["LZ_1879"]),
      obj("décrire l'effet de la chaleur et du champ", ["LZ_4066"]),
      obj("expliquer monocristal et conduction intrinsèque", ["LZ_4067"]),
      obj("expliquer le dopage n et le dopage p", ["LZ_4067"], ").")],
    question: "Le cuivre conduit très bien, la porcelaine pas du tout. Pourquoi les diodes et les transistors sont-ils faits d'un matériau qui conduit « à moitié » ?",
    indice: "Écris ton hypothèse. Réponse à la diapositive 10.",
    notes: "Durée : 2 périodes, puis la fiche 110 EX. Niveau visé : comprendre et savoir que ça existe ; aucun calcul dans la présentation.\n" +
      "Objectifs FutureMEM (champ LFB_El_Dim4), cliquables sur la diapositive : LZ_1879 (C4) différencier (diapositives 3 à 5) ; LZ_4066 (C2) chaleur et champ électrique (7 et 8) ; " +
      "LZ_4067 (C2) monocristal, conduction intrinsèque, dopage (6 et 9). Aucune situation pratique TM2 ne couvre ces objectifs.\n" +
      "Question de départ : noter les hypothèses au tableau sans les corriger. Réponse à la diapositive 10.",
  });

  // ============================== 2. LA SITUATION · CE QUE TU SAIS DÉJÀ
  {
    const s = slide("La situation et ce que tu sais déjà",
      "Situation de travail du champ LFB_El_Dim4 : étendre l'équipement de test d'une ligne de production (voyants, entrées protégées, sorties commandées).\n" +
      "Activation, 5 min en binôme, carte mentale « Matériaux en électricité ». Réponses attendues : 1) un déplacement de charges (des électrons dans un fil). 2) Il a des électrons libres. 3) La résistivité ρ.\n" +
      "Les LED ne sont pas en silicium : arséniure de gallium (GaAs) ou nitrure de gallium-indium (InGaN). L'optocoupleur associe une LED GaAs et un phototransistor au silicium.");
    card(s, 0.5, 0.95, 4.4, 1.25);
    txt(s, "Ta mission", { x: 0.65, y: 1.02, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, "Étendre l'équipement de test de la ligne : des voyants, des entrées protégées, des sorties commandées.", { x: 0.65, y: 1.36, w: 4.1, h: 0.8, fontSize: 12 });
    s.addTable([
      [cell("Composant", H), cell("Matériau", H)],
      [cell("diode, transistor", { align: "left" }), cell("silicium")],
      [cell("LED", { align: "left" }), cell("gallium (GaAs, InGaN)")],
      [cell("optocoupleur", { align: "left" }), cell("LED GaAs + silicium")],
    ], { x: 0.5, y: 2.35, w: 4.4, colW: [1.9, 2.5], rowH: 0.42, border: BORDER, fontSize: 11.5 });
    frame(s, 5.1, 0.95, 4.4, 3.1);
    txt(s, "Ce que tu sais déjà (en binôme, 5 min)", { x: 5.25, y: 1.02, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    [["1", "Qu'est-ce qu'un courant électrique ?"], ["2", "Pourquoi un fil de cuivre conduit-il ?"], ["3", "Quelle grandeur dit si un matériau conduit bien ?"]].forEach(([n, q], i) => {
      const y = 1.45 + i * 0.82;
      badge(s, 5.25, y + 0.08, n, 0.36);
      txt(s, q, { x: 5.75, y, w: 3.6, h: 0.55, fontSize: 12.5, valign: "middle" });
    });
    life(s, 0.5, 4.3, 9.0, 1.25, ["Tous ces composants sont faits de semi-conducteurs. Qu'ont-ils de particulier ?",
      "En pratique (TM2-A1), tu relèves la caractéristique d'une diode au silicium : ce cours explique ce qui se passe dans le matériau."], 11);
  }

  // ============================== 3. LA RÉSISTIVITÉ
  {
    const s = slide("Conducteur, semi-conducteur, isolant",
      "La résistivité ρ (Ω·m) dit si un matériau conduit bien. Elle ne dépend que du matériau et de la température.\n" +
      "Échelle logarithmique : chaque graduation multiplie par 100. Les limites des zones sont des ordres de grandeur.\n" +
      "Le nichrome (fil chauffant) reste un conducteur. Le silicium dopé et le silicium pur sont le même matériau : le dopage change tout (diapositive 9).");
    img(s, "fig_echelle_rho.png", 0.5, 0.95, 9.0, 2.75);
    [["Conducteurs", "cuivre, aluminium : conduisent toujours très bien"], ["Semi-conducteurs", "silicium : conduction faible, mais réglable"],
     ["Isolants", "porcelaine, PVC : ne conduisent pratiquement pas"]].forEach(([t, d], k) => {
      const x = 0.5 + k * 3.05;
      card(s, x, 3.85, 2.9, 1.7);
      txt(s, t, { x: x + 0.15, y: 3.93, w: 2.6, h: 0.32, fontSize: 13, bold: true, color: BLUE });
      txt(s, d, { x: x + 0.15, y: 4.3, w: 2.6, h: 1.15, fontSize: 12 });
    });
  }

  // ============================== 4. LES ÉLECTRONS DE VALENCE
  {
    const s = slide("Pourquoi ? Les électrons de valence",
      "Les électrons de valence sont ceux de la couche extérieure : ils forment les liaisons et peuvent devenir libres.\n" +
      "Métal : 1 à 3 électrons de valence, peu liés, donc beaucoup d'électrons libres. Silicium : 4 électrons de valence, tous pris dans des liaisons ; " +
      "un peu d'énergie (chaleur, lumière) en libère quelques-uns. Isolant : liaisons très solides, pratiquement aucun électron libre.");
    img(s, "fig_valence.png", 0.5, 0.95, 5.0, 3.2);
    [["Métal", "beaucoup d'électrons libres, toujours"], ["Semi-conducteur", "4 électrons de valence, presque tous liés"], ["Isolant", "aucun électron libre"]].forEach(([t, d], i) => {
      const y = 0.95 + i * 1.08;
      card(s, 5.7, y, 3.8, 0.98);
      txt(s, t, { x: 5.85, y: y + 0.07, w: 3.5, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
      txt(s, d, { x: 5.85, y: y + 0.42, w: 3.5, h: 0.5, fontSize: 12 });
    });
    life(s, 0.5, 4.4, 9.0, 1.15, ["Le silicium vient du sable : c'est le deuxième élément le plus abondant de la croûte terrestre."], 11);
  }

  // ============================== 5. DIFFÉRENCIER
  {
    const s = slide("Différencier les trois familles",
      "Synthèse pour l'objectif LZ_1879 (niveau C4 : différencier). Les limites de résistivité sont floues : le comportement à la chaleur tranche.\n" +
      "Faire justifier à l'oral : « le germanium est un semi-conducteur parce que… », avec une valeur et un comportement.");
    const L = { align: "left", bold: true };
    s.addTable([
      [cell("", H), cell("Conducteur", H), cell("Semi-conducteur", H), cell("Isolant", H)],
      [cell("Résistivité ρ", L), cell("très faible"), cell("moyenne, réglable"), cell("très grande")],
      [cell("Électrons libres", L), cell("beaucoup"), cell("très peu"), cell("aucun")],
      [cell("Quand il chauffe", L), cell("R augmente un peu"), cell("R diminue fortement", { bold: true, color: BLUE }), cell("reste isolant")],
      [cell("Exemples", L), cell("cuivre, aluminium"), cell("silicium, germanium"), cell("porcelaine, PVC")],
    ], { x: 0.5, y: 0.95, w: 9.0, colW: [2.1, 2.2, 2.5, 2.2], rowH: 0.52, border: BORDER, fontSize: 12 });
    card(s, 0.5, 3.75, 9.0, 0.7, NAVY);
    txt(s, [{ text: "À retenir : ", options: { bold: true, color: LBLUE } }, { text: "un semi-conducteur est un matériau dont on peut régler la conduction.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 3.75, w: 8.6, h: 0.7, fontSize: 13, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, ["Sur un circuit imprimé : la plaque est isolante (époxy), les pistes conduisent (cuivre), les puces sont en silicium."], 11);
  }

  // ============================== 6. LE CRISTAL DE SILICIUM
  {
    const s = slide("Le cristal de silicium",
      "Monocristal : les atomes sont rangés régulièrement dans tout le morceau. Chaque atome partage ses 4 électrons de valence avec 4 voisins (dessin à plat ; en réalité en 3 dimensions).\n" +
      "Le silicium des puces est purifié à 99,9999999 %, tiré en lingot à partir d'un germe, puis scié en plaquettes (wafers).\n" +
      "Conduction intrinsèque : à température ambiante, la chaleur rompt quelques liaisons. Chaque rupture donne un électron libre et un trou (une place vide qui se comporte comme une charge +). " +
      "Le matériau pur conduit par ces paires, mais très peu : environ un électron libre pour 3 000 milliards d'atomes.");
    img(s, "fig_paire.png", 0.5, 0.95, 3.4, 3.55);
    boxTitle(s, 4.1, 0.95, 5.4, 1.5, "Monocristal", ["Atomes rangés régulièrement dans tout le morceau.", "Chaque atome est lié à 4 voisins."], 12, true);
    boxTitle(s, 4.1, 2.6, 5.4, 1.9, "Conduction intrinsèque", ["La chaleur rompt une liaison : un électron libre et un trou.",
      "Le silicium pur conduit par ces paires, mais très peu."], 12, false);
    life(s, 0.5, 4.65, 9.0, 0.9, ["Les puces sont découpées dans des plaquettes (wafers) de silicium monocristallin."], 11);
  }

  // ============================== 7. LA CHALEUR
  {
    const s = slide("Influence de la chaleur",
      "Métal : en chauffant, les atomes vibrent et freinent les électrons. R augmente un peu (cuivre : environ 0,4 % par °C).\n" +
      "Semi-conducteur : la chaleur crée des paires électron-trou. Le nombre de porteurs double environ tous les 10 °C : R diminue fortement. La courbe est une allure.\n" +
      "Dans les composants : la tension directe d'une diode au silicium baisse d'environ 2 mV par °C. La plupart des puces au silicium sont limitées à 150 °C.");
    img(s, "fig_temperature.png", 0.5, 0.95, 4.9, 3.4);
    boxTitle(s, 5.6, 0.95, 3.9, 1.4, "Métal", ["R augmente un peu."], 12, true);
    boxTitle(s, 5.6, 2.5, 3.9, 1.85, "Semi-conducteur", ["La chaleur libère des porteurs.", "R diminue fortement."], 12, false);
    life(s, 0.5, 4.5, 9.0, 1.05, ["Dans une armoire chaude, une diode conduit un peu plus tôt : les fiches techniques donnent les valeurs selon la température.",
      "Une thermistance CTN utilise cet effet pour mesurer la température."], 11);
  }

  // ============================== 8. LE CHAMP ÉLECTRIQUE
  {
    const s = slide("Influence du champ électrique",
      "Une tension crée un champ électrique : les électrons vont vers le +, les trous vers le −. Les deux courants s'additionnent.\n" +
      "Champ très fort : les liaisons cèdent (effet Zener ou avalanche), le courant monte d'un coup : le claquage. La diode Zener l'utilise (présentation 120).\n" +
      "Champ commandé : une électrode isolée attire ou repousse les porteurs : le transistor à effet de champ, FET (présentation 300).\n" +
      "La lumière agit comme la chaleur : photodiode, phototransistor (présentation 220).");
    img(s, "fig_champ.png", 0.5, 0.95, 5.0, 2.5);
    [["Champ normal", "électrons vers le +, trous vers le −"], ["Champ très fort", "claquage : la diode Zener"], ["Champ commandé", "le transistor à effet de champ (FET)"]].forEach(([t, d], i) => {
      const y = 0.95 + i * 1.12;
      card(s, 5.7, y, 3.8, 1.02);
      txt(s, t, { x: 5.85, y: y + 0.07, w: 3.5, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
      txt(s, d, { x: 5.85, y: y + 0.42, w: 3.5, h: 0.52, fontSize: 12 });
    });
    life(s, 0.5, 4.5, 9.0, 1.05, ["La lumière agit comme la chaleur : elle libère des porteurs. C'est le principe du phototransistor de l'optocoupleur."], 11);
  }

  // ============================== 9. LE DOPAGE
  {
    const s = slide("Le dopage : type n et type p",
      "Doper, c'est ajouter très peu d'atomes d'un autre élément dans le cristal.\n" +
      "Type n : atome à 5 électrons de valence (phosphore P, arsenic As). Le 5e électron devient libre : les électrons sont majoritaires. Ces atomes sont des donneurs.\n" +
      "Type p : atome à 3 électrons de valence (bore B, gallium Ga). Il manque un électron : il reste un trou, les trous sont majoritaires. Ces atomes sont des accepteurs.\n" +
      "Ordre de grandeur : un atome de phosphore pour environ 50 millions d'atomes de silicium divise la résistivité par plusieurs dizaines de milliers.\n" +
      "Erreur fréquente : un morceau dopé n n'est pas chargé négativement. Chaque atome de phosphore a aussi un proton de plus : le morceau reste neutre.");
    [["fig_dopage_n.png", "Type n", "phosphore : 5 électrons de valence", "le 5e électron devient libre", "majoritaires : électrons"],
     ["fig_dopage_p.png", "Type p", "bore : 3 électrons de valence", "il manque un électron : un trou", "majoritaires : trous"]].forEach(([f, t, a, b, c], k) => {
      const x = 0.5 + k * 4.55;
      img(s, f, x, 0.95, 2.25, 2.4);
      card(s, x + 2.3, 0.95, 2.15, 2.4);
      txt(s, t, { x: x + 2.42, y: 1.02, w: 1.95, h: 0.32, fontSize: 13, bold: true, color: BLUE });
      bullets(s, [a, b], { x: x + 2.42, y: 1.4, w: 1.95, h: 1.3, fontSize: 11 });
      txt(s, c, { x: x + 2.42, y: 2.75, w: 1.95, h: 0.5, fontSize: 11.5, bold: true });
    });
    frame(s, 0.5, 3.6, 9.0, 0.85);
    txt(s, [{ text: "Les deux restent neutres. ", options: { bold: true, color: BLUE } }, { text: "Une zone p et une zone n dans le même cristal forment une jonction PN : la diode (présentation 120)." }],
      { x: 0.65, y: 3.6, w: 8.7, h: 0.85, fontSize: 12, valign: "middle" });
    life(s, 0.5, 4.6, 9.0, 0.95, ["Un atome de phosphore pour 50 millions d'atomes de silicium suffit : on règle la conduction à la fabrication."], 11);
  }

  // ============================== 10. RÉPONSE · TICKET DE SORTIE
  {
    const s = slide("Réponse à la question · ticket de sortie",
      "Réponse : on choisit un semi-conducteur parce qu'on peut régler sa conduction. Le cuivre conduit toujours, la porcelaine jamais : avec eux, pas d'interrupteur électronique ni d'amplificateur.\n" +
      "Ticket de sortie (5 min, seul·e, sans support). Réponses : 1) conducteur, semi-conducteur, isolant. 2) Elle baisse : la chaleur libère des porteurs. 3) Un atome à 3 électrons de valence, par exemple le bore. 4) Non, il reste neutre.\n" +
      "Ensuite : compléter la carte mentale de la diapositive 2, puis la fiche 110 EX.");
    card(s, 0.5, 0.95, 9.0, 0.6, NAVY);
    txt(s, [{ text: "Réponse : ", options: { bold: true, color: LBLUE } }, { text: "on peut régler la conduction d'un semi-conducteur.", options: { color: "FFFFFF" } }],
      { x: 0.7, y: 0.95, w: 8.6, h: 0.6, fontSize: 13, valign: "middle" });
    [["Dopage", "diodes, transistors"], ["Champ électrique", "FET, diode Zener"], ["Lumière", "phototransistor"], ["Chaleur", "thermistance CTN"]].forEach(([t, c], k) => {
      const x = 0.5 + k * 2.28;
      card(s, x, 1.65, 2.15, 0.85);
      txt(s, t, { x: x + 0.12, y: 1.68, w: 1.95, h: 0.35, fontSize: 12, bold: true, color: BLUE });
      txt(s, c, { x: x + 0.12, y: 2.03, w: 1.95, h: 0.4, fontSize: 11 });
    });
    frame(s, 0.5, 2.65, 9.0, 2.25);
    txt(s, "Ticket de sortie : seul·e, 5 minutes, sans support", { x: 0.65, y: 2.72, w: 8.7, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    [["1", "Classe : cuivre, silicium, porcelaine."], ["2", "Un semi-conducteur chauffe : sa résistance monte ou baisse ?"],
     ["3", "Quel atome ajoutes-tu au silicium pour un type p ?"], ["4", "Un morceau de silicium dopé n est-il chargé ?"]].forEach((q, i) => {
      const x = 0.65 + (i % 2) * 4.45, y = 3.12 + Math.floor(i / 2) * 0.85;
      badge(s, x, y + 0.13, q[0], 0.34);
      txt(s, q[1], { x: x + 0.45, y, w: 3.85, h: 0.62, fontSize: 12, valign: "middle" });
    });
    card(s, 0.5, 5.02, 9.0, 0.55);
    txt(s, [{ text: "Ensuite : ", options: { bold: true } }, { text: "complète ta carte mentale, puis fiche 110 EX Semi-conducteurs." }], { x: 0.65, y: 5.02, w: 8.7, h: 0.55, fontSize: 11.5, valign: "middle" });
  }

  // ============================== 11. EXERCICES
  exoSlide("110 EX", DATA.TEAMS["110"], [
    ["1", "Classer des matériaux", "≈ 12 min · diapositives 3 à 5"], ["2", "Le cristal de silicium", "≈ 10 min · diapositive 6"],
    ["3", "L'effet de la chaleur", "≈ 12 min · diapositive 7"], ["4", "Le champ électrique", "≈ 8 min · diapositive 8"],
    ["5", "Le dopage", "≈ 10 min · diapositive 9"]],
    "Tu prépares l'extension de l'équipement de test de la ligne. L'ingénieure de développement te demande de vérifier tes bases sur les matériaux des composants.",
    "Seul·e ou en binôme, environ 50 min. Justifie chaque réponse en une phrase.",
    ["Ces bases servent à lire une fiche technique : valeurs selon la température, courant de fuite, tension de claquage."],
    "Fiche 110 EX Semi-conducteurs : environ 50 min de travail, puis la correction en plénière. Temps indicatifs : N°1 12 min, N°2 10 min, N°3 12 min, N°4 8 min, N°5 10 min.\n" +
    "Corrigé : 110 EX C Semi-conducteurs (pour l'enseignant·e).");

  // ============================== 12. PAGE INTERACTIVE (phase médias)
  pageSlide("101", DATA.FILES["101"], DATA.TEAMS["101"], DATA.ART["101"], "shot_101.png",
    ["Range les matériaux sur l'échelle", "Fais chauffer le cristal", "Applique un champ électrique", "Dope le silicium : n ou p ?"],
    ["À refaire à la maison avant le test : chaque erreur est expliquée."],
    "Page interactive 101 : un seul fichier .html, sans installation. Quatre étapes, chacune avec une animation « Comprendre » puis un exercice « À toi » corrigé tout de suite.\n" +
    "Déposer le fichier « 101 Semi-conducteurs.html » dans le dossier Teams LFB_El_Dim4 : le lien de la diapositive vise ce chemin.");

  // ============================== 13. VIDÉO (phase médias)
  videoSlide("105", DATA.FILES["105"], DATA.TEAMS["105"], "cover_105.png", "4 minutes",
    [["Trois familles", "résistivité et électrons libres"], ["Le cristal", "paires électron-trou"],
     ["Chaleur et champ", "plus de porteurs, claquage"], ["Le dopage", "type n et type p"]],
    ["Pour réviser à la maison ou rattraper une absence."],
    "Animation 105 Semi-conducteurs : 4 min 10, 1920 × 1080. La vidéo est intégrée à la présentation : elle se lit dans PowerPoint sans connexion (clic sur l'image en mode diaporama).\n" +
    "Déposer aussi le fichier « 105 Semi-conducteurs.mp4 » dans le dossier Teams LFB_El_Dim4 : le lien sous la vidéo vise ce chemin.");
};
