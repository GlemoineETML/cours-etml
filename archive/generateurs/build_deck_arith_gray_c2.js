// Présentation « Arithmétique binaire, code Gray et compléments » — charte ETML couleurs (T&M : marine 242852, bleu 297FD5), Arial, 16:10
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.defineLayout({ name: "ETML1610", width: 10, height: 6.25 });
pres.layout = "ETML1610";
pres.author = "Gaël Lemoine";
pres.title = "Arithmétique binaire, code Gray et compléments";
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };

const NAVY = "242852", BLUE = "297FD5", LBLUE = "ACCBF9", TINT = "E8EFFB";
const K = NAVY, GR = "5A6478", LG = LBLUE, VLG = TINT, RED = "EE0000";
const F = "Arial", MONO = "Courier New";
const TOPIC = "Arithmétique binaire, code Gray et compléments";
const LFB = "LFB_Pr_Basis";   // référence FutureMem du champ, en lien cliquable
const LFB_URL = "https://skills.futuremem.swiss/fr/data/4000_lfe_17/#02B5481A-671C-5A41-868A-24EFB25175EE";
const LFB_TIP = "LFB_Pn_ENTBAS - LFB_Pü_Pr2 - FUTUREMEM";
const FLOYD_PDF = "https://eduvaud.sharepoint.com/:b:/r/sites/msteams_76c9d9/Documents%20partages/Documentation/Electronique%20num%C3%A9rique%20TMLO/10%20Floyd%20V11/10%20Floyd%20V11%20Basse%20d%C3%A9finition%20par%20chapitre/Chap%2002%20-%20Syst%C3%A8mes%20de%20num%C3%A9ration,%20op%C3%A9rations%20et%20codes.pdf?d=w933f2237d1814185b6a6b02be82abe0b&csf=1&web=1&e=eHqofE";   // Floyd chap. 2 sur Teams
const MODULE = "Test et Mesure 1 – " + LFB, CLASSE = "XLO1", ANNEE = "2026-2027", CHAMP = "LZ_4258";
const LOGO_BAND = "logo_white_v.png";   // logo ETML du modèle Rapport_Simple.dotx, en blanc, tourné à 90° pour le bandeau
const NEXTEC_TOPIC = "https://app.nextecmedia.ch/resolve?courseProductReference=P108e2&issueProductReference=P108e7&contentType=topic&fileReference=F15614_2&contentId=5.1&contentReference=23060";
const NEXTEC_GRAY = "https://app.nextecmedia.ch/resolve?courseProductReference=P108e2&issueProductReference=P108e7&contentType=exercise&exerciseGroup=16&contentId=&contentReference=24154";

// Bandeau vertical marine à droite (modèle T&M ETML) : texte « Electronique » + numéro de diapo
const BAND = (pg) => [
  { rect: { x: 9.25, y: 0, w: 0.75, h: 6.25, fill: { color: NAVY } } },
  { image: { path: LOGO_BAND, x: 9.39, y: 0.35, w: 0.47, h: 1.95 } },
  { text: { text: "Electronique", options: { x: 8.325, y: 3.675, w: 2.6, h: 0.75, rotate: 270, fontFace: F, fontSize: 20, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0 } } },
];
pres.defineSlideMaster({
  title: "CONTENU",
  background: { color: "FFFFFF" },
  objects: BAND().concat([
    { rect: { x: 9.37, y: 5.62, w: 0.5, h: 0.5, fill: { color: LBLUE } } },
  ]),
  slideNumber: { x: 9.37, y: 5.62, w: 0.5, h: 0.5, fontFace: F, fontSize: 12, bold: true, color: NAVY, align: "center", valign: "middle" },
});
pres.defineSlideMaster({
  title: "TITRE",
  background: { color: "FFFFFF" },
  objects: BAND().concat([
  ]),
});

// Zone utile réduite à x ≤ 8,9" à cause du bandeau : on compresse horizontalement toutes les positions
function squeeze(s, x0, x1, nx1) {
  const k = (nx1 - x0) / (x1 - x0);
  const fx = (o, img) => {
    if (!o || o.placeholder) return o;
    if (typeof o.x === "number") o.x = x0 + (o.x - x0) * k;
    if (typeof o.w === "number") o.w = o.w * k;
    if (img && typeof o.h === "number") { o.y = o.y + o.h * (1 - k) / 2; o.h = o.h * k; }
    if (Array.isArray(o.colW)) o.colW = o.colW.map(c => c * k);
    return o;
  };
  const at = s.addText.bind(s), ash = s.addShape.bind(s), ai = s.addImage.bind(s), atb = s.addTable.bind(s);
  s.addText = (t, o) => at(t, fx(o));
  s.addShape = (sh, o) => ash(sh, fx(o));
  s.addImage = (o) => ai(fx(o, true));
  s.addTable = (r, o) => atb(r, fx(o));
  return s;
}

// Cartouche de pied de page : posé sur chaque diapositive (et non dans le masque) pour rester éditable
function cartouche(s, titre) {
  const y = titre ? 5.6 : 5.78, ty = titre ? 5.66 : 5.82, fs = titre ? 11 : 9;
  s.addShape(pres.shapes.LINE, { x: titre ? 0.6 : 0.5, y, w: titre ? 8.3 : 8.4, h: 0, line: { color: BLUE, width: 0.75 } });
  s.addText("Section électronique", { x: titre ? 0.6 : 0.5, y: ty, w: 2.4, h: 0.3, fontFace: F, fontSize: fs, italic: true, color: NAVY, margin: 0, isTextBox: true });
  const runs = [
    { text: "Test et Mesure 1 – ", options: {} },
    { text: LFB, options: { hyperlink: { url: LFB_URL, tooltip: LFB_TIP } } },
    { text: titre ? " · Version : 11.2026 / 1.3" : " · " + TOPIC, options: {} },
  ];
  s.addText(runs, { x: titre ? 3.4 : 2.9, y: ty, w: titre ? 5.5 : 6.0, h: 0.3, fontFace: F, fontSize: fs, color: titre ? NAVY : GR, align: "right", margin: 0, isTextBox: true });
}
function slide(title, notes) {
  const s = pres.addSlide({ masterName: "CONTENU" });
  cartouche(s, false);
  s.addText(title, { x: 0.5, y: 0.25, w: 8.4, h: 0.5, fontFace: F, fontSize: 24, bold: true, color: NAVY, margin: 0, valign: "middle", isTextBox: true, fit: "shrink" });
  squeeze(s, 0.5, 9.5, 8.9);
  if (notes) s.addNotes(notes);
  return s;
}
function txt(s, text, o) {
  s.addText(text, Object.assign({ fontFace: F, fontSize: 15, color: K, margin: 0, valign: "top", isTextBox: true }, o));
}
function card(s, x, y, w, h, fill) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill || VLG }, line: { color: fill ? fill : VLG, width: 0 } });
}
function frame(s, x, y, w, h) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.25 } });
}
function life(s, x, y, w, h, text, fs) {
  card(s, x, y, w, h);
  s.addText([{ text: "Dans la vraie vie", options: { bold: true, color: BLUE, breakLine: true } }, { text, options: { color: K } }],
    { x: x + 0.18, y: y + 0.1, w: w - 0.36, h: h - 0.2, fontFace: F, fontSize: fs || 12, margin: 0, valign: "top", paraSpaceAfter: 3, isTextBox: true });
}
function badge(s, x, y, label) {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.42, h: 0.42, fill: { color: K }, line: { color: K } });
  s.addText(label, { x, y, w: 0.42, h: 0.42, fontFace: F, fontSize: 14, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
}
const cell = (t, o) => ({ text: String(t), options: Object.assign({ align: "center", valign: "middle", fontFace: F }, o || {}) });
const bits = (v, n) => v.toString(2).padStart(n, "0").split("");

// addition column table: weights, carries, A, B, sum (9 colonnes de bits)
function addTable(a, b, n, hideFrom) {
  const W = []; for (let i = n; i >= 0; i--) W.push(2 ** i);
  const carry = Array(n + 1).fill(""); let c = 0;
  for (let i = 0; i < n; i++) { const t = ((a >> i) & 1) + ((b >> i) & 1) + c; c = t >> 1; if (c) carry[n - i - 1] = "1"; }
  const sum = bits(a + b, n + 1);
  const hide = (row, j) => hideFrom !== undefined && (n - j) > hideFrom; // bits de rang > hideFrom masqués
  const H = { fill: { color: LG }, fontSize: 11, italic: true };
  const rows = [
    [cell("Poids", Object.assign({ align: "left" }, H))].concat(W.map(w => cell(w, H))).concat([cell("Décimal", H)]),
    [cell("Retenues", { align: "left", fontSize: 12, italic: true })].concat(carry.map((x, j) => cell((hideFrom !== undefined && (n - j) > hideFrom + 1) ? "" : x, { fontSize: 14, color: GR }))).concat([cell("")]),
    [cell("A", { align: "left", bold: true })].concat([cell("")]).concat(bits(a, n).map(x => cell(x, { fontFace: MONO, fontSize: 18, bold: true }))).concat([cell(a + "d")]),
    [cell("+ B", { align: "left", bold: true })].concat([cell("")]).concat(bits(b, n).map(x => cell(x, { fontFace: MONO, fontSize: 18, bold: true }))).concat([cell(b + "d")]),
    [cell("= Somme", { align: "left", bold: true, fill: { color: VLG } })].concat(sum.map((x, j) => cell(hide(1, j) ? "" : x, { fontFace: MONO, fontSize: 18, bold: true, fill: { color: VLG } }))).concat([cell(hideFrom !== undefined ? "?" : (a + b) + "d", { bold: true, fill: { color: VLG } })]),
  ];
  return rows;
}
const colW = (n) => [1.15].concat(Array(n + 1).fill(0.58)).concat([1.0]);

// ============================== 1. TITRE (coordonnées réelles, zone utile x ≤ 8,9")
{
  const s = pres.addSlide({ masterName: "TITRE" });
  cartouche(s, true);
  s.addText([{ text: "TEST ET MESURE 1 – ", options: {} }, { text: LFB, options: { hyperlink: { url: LFB_URL, tooltip: LFB_TIP } } }],
    { x: 0.6, y: 0.55, w: 5.4, h: 0.35, fontFace: F, fontSize: 13, bold: true, color: BLUE, charSpacing: 1, margin: 0, valign: "top", isTextBox: true });
  txt(s, "Arithmétique binaire, code Gray et compléments", { x: 0.6, y: 0.95, w: 5.3, h: 1.5, fontSize: 28, bold: true, color: NAVY, valign: "top" });
  txt(s, "Systèmes de numération et codes", { x: 0.6, y: 1.9, w: 5.3, h: 0.4, fontSize: 17, color: GR });
  txt(s, "Comment un microcontrôleur additionne, multiplie, lit un bouton rotatif et gère les nombres négatifs.", { x: 0.6, y: 2.35, w: 5.3, h: 0.65, fontSize: 13, italic: true, color: NAVY });
  ["Addition", "Multiplication et × 2", "Code Gray", "Compléments à 1 et à 2"].forEach((t, i) => {
    const x = 0.6 + (i % 2) * 2.7, y = 3.15 + Math.floor(i / 2) * 0.52;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.55, h: 0.42, rectRadius: 0.08, fill: { color: NAVY }, line: { color: NAVY } });
    txt(s, t, { x, y, w: 2.55, h: 0.42, fontSize: 12, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
  });
  card(s, 0.6, 4.35, 8.3, 1.05);
  s.addText([
    { text: `Classe ${CLASSE} · année ${ANNEE} · champ d'apprentissage ${CHAMP}`, options: { bold: true, breakLine: true } },
    { text: "« Elles/Ils décrivent le code binaire, BCD, Gray, Unicode et le code ASCII. »", options: { italic: true, breakLine: true } },
    { text: "Éditeur : Gaël Lemoine", options: { color: GR } },
  ], { x: 0.8, y: 4.42, w: 7.9, h: 0.92, fontFace: F, fontSize: 12, color: NAVY, margin: 0, valign: "middle", isTextBox: true });
  s.addImage({ path: "fig_disque_corr.png", x: 6.2, y: 0.75, w: 2.6, h: 2.6 });
  txt(s, "Disque codeur en code Gray", { x: 6.0, y: 3.4, w: 3.0, h: 0.3, fontSize: 10, italic: true, color: GR, align: "center" });
  s.addNotes("Durée ≈ 2 × 45 min avec les exercices. Déroulé de la théorie : échauffement (3 min) → addition (8 min) → × 2 et multiplication (12 min) → code Gray et applications (15 min) → compléments et nombres négatifs (12 min) → ticket de sortie (4 min).");
}

// ============================== 2. OBJECTIFS
{
  const s = slide("À la fin de cette leçon, je suis capable de…",
    "Lire les objectifs à voix haute. Les apprentis évaluent eux-mêmes en fin de leçon chaque « je suis capable » (pouce haut / milieu / bas). Les ressources sont celles du cours : Nextec Media (manuel numérique) et le Floyd chap. 2, à consulter pour les explications détaillées et les exercices supplémentaires.");
  const items = [
    ["1", "Additionner deux nombres binaires en notant les retenues, et repérer un dépassement."],
    ["2", "Multiplier en binaire, et multiplier par 2, 4, 8… par simple décalage."],
    ["3", "Expliquer pourquoi on utilise le code Gray et convertir binaire ↔ Gray."],
    ["4", "Calculer le complément à 1 et à 2, et l'utiliser pour les nombres négatifs."],
  ];
  items.forEach((it, i) => {
    const x = 0.5 + (i % 2) * 4.55, y = 1.05 + Math.floor(i / 2) * 1.35;
    card(s, x, y, 4.35, 1.15);
    badge(s, x + 0.18, y + 0.36, it[0]);
    txt(s, it[1], { x: x + 0.78, y: y + 0.12, w: 3.4, h: 0.95, fontSize: 14, valign: "middle" });
  });
  frame(s, 0.5, 3.9, 9.0, 1.7);
  txt(s, "Ressources", { x: 0.7, y: 4.0, w: 3, h: 0.3, fontSize: 13, bold: true });
  s.addText([
    { text: "Nextec Media – chapitre 5.1 Systèmes de numération et codes", options: { hyperlink: { url: NEXTEC_TOPIC }, breakLine: true } },
    { text: "Nextec Media – exercice complémentaire sur le code Gray", options: { hyperlink: { url: NEXTEC_GRAY }, breakLine: true } },
    { text: "Floyd, chap. 2 (PDF sur Teams) – sections 2-4, 2-5, 2-6, 2-7 et 2-11", options: { hyperlink: { url: FLOYD_PDF, tooltip: "Ouvrir le chapitre 2 du Floyd" } } },
  ], { x: 0.7, y: 4.35, w: 8.6, h: 1.15, fontFace: F, fontSize: 12, color: K, margin: 0, valign: "top", paraSpaceAfter: 4, isTextBox: true });
}

// ============================== 3. ÉCHAUFFEMENT
{
  const s = slide("Échauffement : 3 minutes, sans calculatrice",
    "Pratique de récupération : chacun répond seul sur une feuille, puis on compare avec le voisin, puis correction au tableau.\nRéponses : 1) 1011b = 8 + 2 + 1 = 11d. 2) 13d = 8 + 4 + 1 = 1101b. 3) Avec 4 bits : 2^4 = 16 combinaisons, de 0d à 15d (= 2^4 − 1).\nSi beaucoup d'erreurs : refaire au tableau la ligne des poids 128-64-32-16-8-4-2-1.");
  const q = [["1011b = ? d", "Binaire → décimal"], ["13d = ? b", "Décimal → binaire"], ["Plus grand nombre sur 4 bits ?", "Capacité d'un mot"]];
  q.forEach((t, i) => {
    const x = 0.5 + i * 3.05;
    card(s, x, 1.25, 2.85, 2.6);
    badge(s, x + 0.2, 1.45, String(i + 1));
    txt(s, t[0], { x: x + 0.2, y: 2.15, w: 2.45, h: 1.0, fontSize: 22, bold: true, align: "center", valign: "middle" });
    txt(s, t[1], { x: x + 0.2, y: 3.25, w: 2.45, h: 0.4, fontSize: 12, color: GR, align: "center" });
  });
  txt(s, "Écris ta réponse seul·e → compare avec ton voisin → correction ensemble.", { x: 0.5, y: 4.25, w: 9, h: 0.4, fontSize: 15, italic: true });
  txt(s, "Rappel des poids :  128 · 64 · 32 · 16 · 8 · 4 · 2 · 1", { x: 0.5, y: 4.85, w: 9, h: 0.4, fontSize: 15, fontFace: MONO, bold: true });
}

// ============================== 4. ADDITION : RÈGLES
{
  const s = slide("Addition binaire : il n'y a que 4 cas",
    "Partir de l'analogie décimale : en décimal on retient dès qu'on dépasse 9 ; en binaire on retient dès qu'on dépasse 1. Faire dire aux apprentis le 5e cas (1 + 1 + 1) qui apparaît dès qu'il y a une retenue. Source : Floyd 2-4 p. 60.");
  const H = { fill: { color: LG }, italic: true, fontSize: 13 };
  const M = { fontFace: MONO, fontSize: 20, bold: true };
  s.addTable([
    [cell("Calcul", H), cell("Somme", H), cell("Retenue", H)],
    [cell("0 + 0", M), cell("0", M), cell("0", M)],
    [cell("0 + 1", M), cell("1", M), cell("0", M)],
    [cell("1 + 0", M), cell("1", M), cell("0", M)],
    [cell("1 + 1", M), cell("0", M), cell("1", Object.assign({}, M, { fill: { color: VLG } }))],
    [cell("1 + 1 + 1", Object.assign({}, M, { color: GR })), cell("1", Object.assign({}, M, { color: GR })), cell("1", Object.assign({}, M, { color: GR, fill: { color: VLG } }))],
  ], { x: 0.5, y: 1.1, w: 4.4, colW: [1.9, 1.25, 1.25], rowH: 0.55, border: { type: "solid", color: K, pt: 0.75 } });
  txt(s, "(avec une retenue venant de la droite)", { x: 0.5, y: 4.45, w: 4.4, h: 0.3, fontSize: 11, italic: true, color: GR });
  txt(s, "On additionne colonne par colonne, de droite (LSB) à gauche (MSB), en écrivant chaque retenue au-dessus de la colonne suivante.", { x: 0.5, y: 4.85, w: 4.4, h: 0.7, fontSize: 12 });
  card(s, 5.3, 1.1, 4.2, 1.6);
  txt(s, "Comme en décimal…", { x: 5.5, y: 1.22, w: 3.8, h: 0.35, fontSize: 15, bold: true });
  txt(s, "9 + 1 = 10 : on écrit 0 et on retient 1.\nEn binaire, on « déborde » déjà à 2.", { x: 5.5, y: 1.62, w: 3.8, h: 1.0, fontSize: 14 });
  frame(s, 5.3, 2.95, 4.2, 1.2);
  txt(s, "1 + 1 = 10b", { x: 5.5, y: 3.05, w: 3.8, h: 0.5, fontSize: 26, bold: true, fontFace: MONO, align: "center" });
  txt(s, "et pas 2 : le chiffre 2 n'existe pas !", { x: 5.5, y: 3.6, w: 3.8, h: 0.4, fontSize: 13, italic: true, align: "center" });
  life(s, 5.3, 4.3, 4.2, 1.25, "L'unité de calcul d'un microcontrôleur additionne ainsi : compteur de pièces sur une chaîne de production, total d'un compteur d'énergie.");
}

// ============================== 5. EXEMPLE GUIDÉ
{
  const s = slide("Exemple guidé : 91d + 54d en binaire",
    "Exemple travaillé : faire l'addition au tableau colonne par colonne en verbalisant (« 1 + 0 = 1, pas de retenue… 1 + 1 = 0, je retiens 1… »). Contrôle final en décimal : 145d = 128 + 16 + 1 = 1001 0001b. Le 9e bit (poids 256) reste à 0 : le résultat tient dans un octet.");
  s.addTable(addTable(91, 54, 8), { x: 0.5, y: 1.05, w: 9.0, colW: colW(8), rowH: [0.38, 0.42, 0.55, 0.55, 0.55], border: { type: "solid", color: K, pt: 0.75 } });
  card(s, 0.5, 3.75, 4.35, 1.8);
  txt(s, "Méthode", { x: 0.7, y: 3.85, w: 4, h: 0.3, fontSize: 14, bold: true });
  txt(s, [
    { text: "Aligner les deux nombres à droite.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "Colonne par colonne, de droite à gauche.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "Noter la retenue au-dessus de la colonne suivante.", options: { bullet: { type: "number" } } },
  ], { x: 0.7, y: 4.2, w: 4.0, h: 1.3, fontSize: 13, paraSpaceAfter: 3 });
  frame(s, 5.15, 3.75, 4.35, 1.8);
  txt(s, "Toujours contrôler", { x: 5.35, y: 3.85, w: 4, h: 0.3, fontSize: 14, bold: true });
  txt(s, "Résultat : 1001 0001b\n= 128 + 16 + 1 = 145d\n91d + 54d = 145d  ✓", { x: 5.35, y: 4.2, w: 4.0, h: 1.3, fontSize: 15, fontFace: MONO });
}

// ============================== 6. À TOI
{
  const s = slide("À toi : 109d + 87d",
    "Exercice à compléter (on retire l'aide progressivement) : les deux premières colonnes sont faites, l'apprenti termine. 2 min seul, puis comparaison avec le voisin.\nSolution : 0110 1101b + 0101 0111b = 1100 0100b = 196d (retenues aux poids 2, 4, 8, 16, 32, 64, 128 ; aucune retenue vers le poids 256).\nQuestion dépassement : 217d + 108d = 325d > 255d : il faut 9 bits. Un registre 8 bits ne garde que 0100 0101b = 69d (= 325 − 256) : c'est un dépassement (overflow). Lien avec la notion de retenue finale (carry) des microcontrôleurs.");
  s.addTable(addTable(109, 87, 8, 1), { x: 0.5, y: 1.05, w: 9.0, colW: colW(8), rowH: [0.38, 0.42, 0.55, 0.55, 0.55], border: { type: "solid", color: K, pt: 0.75 } });
  txt(s, "Les deux colonnes de droite sont faites : termine, puis contrôle en décimal.", { x: 0.5, y: 3.65, w: 9, h: 0.35, fontSize: 14, italic: true });
  card(s, 0.5, 4.2, 9.0, 1.35);
  badge(s, 0.7, 4.45, "?");
  txt(s, "Et si on additionne 217d + 108d dans un registre de 8 bits ? Combien vaut le résultat, combien de bits faudrait-il, et que garde le registre ?", { x: 1.3, y: 4.3, w: 8.0, h: 1.15, fontSize: 15, valign: "middle" });
}

// ============================== 7. × 2 = DÉCALAGE (avant les produits partiels : chaque produit partiel est une copie décalée)
{
  const s = slide("Multiplier par 2 : un simple décalage à gauche",
    "Message clé : en binaire, × 2 = décaler d'un rang à gauche (un 0 entre au LSB). C'est exactement ce que fait un registre à décalage (vu plus tard en logique séquentielle) ou l'instruction « shift left » d'un microcontrôleur. Analogie : en décimal, × 10 ajoute un zéro.\nPiège : sur un nombre fixe de bits (8 bits), le MSB qui sort est perdu : 1000 0000b × 2 donne 0000 0000b.");
  s.addImage({ path: "fig_decalage.png", x: 0.45, y: 1.0, w: 6.0, h: 2.57 });
  card(s, 6.75, 1.0, 2.75, 2.55);
  txt(s, "En décimal", { x: 6.95, y: 1.1, w: 2.4, h: 0.3, fontSize: 14, bold: true });
  txt(s, "× 10 ajoute un 0 :\n37 → 370 → 3 700", { x: 6.95, y: 1.45, w: 2.4, h: 0.8, fontSize: 13 });
  txt(s, "En binaire", { x: 6.95, y: 2.3, w: 2.4, h: 0.3, fontSize: 14, bold: true });
  txt(s, "× 2 ajoute un 0 :\n10110b → 101100b", { x: 6.95, y: 2.65, w: 2.4, h: 0.8, fontSize: 13 });
  const rules = [["× 2ⁿ", "décaler de n rangs à gauche (× 4 = 2 rangs, × 8 = 3 rangs)"], ["÷ 2", "décaler d'un rang à droite (le LSB sort et est perdu)"], ["Attention", "en 8 bits, le bit qui sort à gauche est perdu : dépassement !"]];
  rules.forEach((r, i) => {
    const y = 3.85 + i * 0.6;
    frame(s, 0.5, y, 9.0, 0.5);
    txt(s, r[0], { x: 0.65, y: y + 0.06, w: 1.5, h: 0.38, fontSize: 16, bold: true, valign: "middle" });
    txt(s, r[1], { x: 2.2, y: y + 0.06, w: 7.2, h: 0.38, fontSize: 14, valign: "middle" });
  });
}

// ============================== 8. MULTIPLICATION : PRODUITS PARTIELS (grille alignée par poids)
{
  const s = slide("Multiplication binaire : produits partiels",
    "On s'appuie sur la diapo précédente : chaque ligne (produit partiel) est le multiplicande multiplié par un seul bit du multiplicateur, donc soit une copie du multiplicande (bit 1), soit une ligne de 0 (bit 0), puis décalée comme pour × 2, × 4. On additionne ensuite les lignes colonne par colonne, avec les retenues. Exemple : 1011b × 101b = 11d × 5d. Ligne du poids 1 : 1011 ; ligne du poids 2 : 0000 décalée d'un rang ; ligne du poids 4 : 1011 décalée de deux rangs (= 101100b = 44d). Somme : 11 + 0 + 44 = 55d = 110111b. Contexte : les petits microcontrôleurs sans multiplieur matériel multiplient exactement ainsi, par décalages et additions. Source : Floyd 2-4 p. 62.");
  const A = 0b1011, B = 0b101, N = 6;          // 6 colonnes : poids 32 … 1
  const W = [32, 16, 8, 4, 2, 1];
  const H = { fill: { color: LG }, italic: true, fontSize: 12 };
  const digits = (v, shift, len) => W.map((w, j) => {
    const p = N - 1 - j;                       // rang du bit (0 = poids 1)
    if (p < shift) return { t: "0", ghost: true };            // 0 ajouté par le décalage
    if (p >= shift + len) return { t: "" };
    return { t: String((v >> (p - shift)) & 1) };
  });
  const rows = [];
  const pp = [0, 1, 2].map(k => ((B >> k) & 1) ? A << k : 0);
  let c = 0; const carry = Array(N).fill("");
  for (let p = 0; p < N; p++) {
    const t = pp.reduce((acc, v) => acc + ((v >> p) & 1), 0) + c; c = t >> 1;
    if (c && p + 1 < N) carry[N - 2 - p] = String(c);
  }
  const prod = A * B;
  const M = (d, extra) => cell(d.t, Object.assign({ fontFace: MONO, fontSize: 18, bold: !d.ghost, color: d.ghost ? "9AA3B5" : K }, extra || {}));
  rows.push([cell("", H)].concat(W.map(w => cell(w, H))).concat([cell("Ce qu'on fait", H)]));
  rows.push([cell("Multiplicande", { align: "left", fontSize: 12, bold: true })].concat(digits(A, 0, 4).map(d => M(d))).concat([cell("1011b = 11d", { align: "left", fontSize: 12 })]));
  rows.push([cell("× multiplicateur", { align: "left", fontSize: 12, bold: true })].concat(digits(B, 0, 3).map(d => M(d))).concat([cell("101b = 5d : bits de poids 4, 2 et 1 = 1, 0, 1", { align: "left", fontSize: 12 })]));
  const expl = ["bit de poids 1 = 1 → on recopie 1011", "bit de poids 2 = 0 → ligne de 0, décalée d'1 rang", "bit de poids 4 = 1 → on recopie 1011, décalée de 2 rangs"];
  [0, 1, 2].forEach(k => {
    const bit = (B >> k) & 1;
    rows.push([cell(`Ligne ${k + 1}`, { align: "left", fontSize: 12, fill: { color: VLG } })]
      .concat(digits(bit ? A : 0, k, 4).map(d => M(d, { fill: { color: VLG } })))
      .concat([cell(expl[k], { align: "left", fontSize: 12, fill: { color: VLG } })]));
  });
  rows.push([cell("Retenues", { align: "left", fontSize: 11, italic: true })].concat(carry.map(x => cell(x, { fontSize: 13, color: GR }))).concat([cell("on additionne les 3 lignes, colonne par colonne", { align: "left", fontSize: 11, italic: true })]));
  rows.push([cell("= Produit", { align: "left", fontSize: 13, bold: true, fill: { color: LG } })].concat(prod.toString(2).padStart(N, " ").split("").map(x => cell(x.trim(), { fontFace: MONO, fontSize: 18, bold: true, fill: { color: LG } }))).concat([cell(`110111b = 32 + 16 + 4 + 2 + 1 = ${prod}d ✓ (11d × 5d)`, { align: "left", fontSize: 12, bold: true, fill: { color: LG } })]));
  s.addTable(rows, { x: 0.5, y: 1.0, w: 9.0, colW: [1.75, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 3.95], rowH: [0.34, 0.45, 0.45, 0.45, 0.45, 0.45, 0.34, 0.5], border: { type: "solid", color: K, pt: 0.75 } });
  card(s, 0.5, 4.75, 9.0, 0.8);
  txt(s, "Règle : un bit à 1 → on recopie le multiplicande, un bit à 0 → une ligne de 0. Chaque ligne est décalée d'un rang de plus (× 2, × 4…). Les 0 gris sont ceux ajoutés par le décalage.", { x: 0.7, y: 4.82, w: 8.6, h: 0.66, fontSize: 13, valign: "middle" });
}

// ============================== 9. ASTUCE ×10 (application : produits partiels sans les lignes de 0)
{
  const s = slide("Application : 13d × 10d uniquement avec des décalages",
    "Lien avec la diapo précédente : 10d = 1010b, ses bits à 1 sont aux poids 8 et 2. Les produits partiels se réduisent donc à deux lignes : 13 décalé de 3 rangs (× 8 = × 2³) et 13 décalé d'1 rang (× 2 = × 2¹) ; les lignes des bits à 0 sont nulles. Calculs : 0000 1101b décalé de 3 rangs = 0110 1000b = 64 + 32 + 8 = 104d ; décalé d'1 rang = 0001 1010b = 16 + 8 + 2 = 26d ; 0110 1000b + 0001 1010b = 1000 0010b = 128 + 2 = 130d = 104d + 26d. Contexte : c'est ainsi qu'un microcontrôleur convertit rapidement une valeur lue (par ex. × 10 pour afficher en décimal) sans instruction de multiplication.");
  card(s, 0.5, 1.0, 9.0, 0.75);
  txt(s, "10d = 1010b = 8d + 2d   donc   13d × 10d = (13d × 8d) + (13d × 2d)", { x: 0.7, y: 1.05, w: 8.6, h: 0.65, fontSize: 16, bold: true, align: "center", valign: "middle" });
  const L = [
    ["13d", "0000 1101b", "nombre de départ : 8 + 4 + 1 = 13d"],
    ["13d × 8d", "0110 1000b", "× 2³ → décaler de 3 rangs à gauche : 64 + 32 + 8 = 104d"],
    ["13d × 2d", "0001 1010b", "× 2¹ → décaler d'1 rang à gauche : 16 + 8 + 2 = 26d"],
    ["Somme", "1000 0010b", "addition binaire des deux lignes : 128 + 2 = 130d = 104d + 26d ✓"],
  ];
  const H = { fill: { color: LG }, italic: true, fontSize: 13 };
  s.addTable([[cell("", H), cell("Binaire (8 bits)", H), cell("Comment", H)]].concat(L.map((r, i) => [
    cell(r[0], { bold: true, fontSize: 15, align: "left", fill: { color: i === 3 ? VLG : "FFFFFF" } }),
    cell(r[1], { fontFace: MONO, fontSize: 20, bold: true, fill: { color: i === 3 ? VLG : "FFFFFF" } }),
    cell(r[2], { fontSize: 12, align: "left", fill: { color: i === 3 ? VLG : "FFFFFF" } })])),
    { x: 0.5, y: 2.0, w: 9.0, colW: [1.35, 2.45, 5.2], rowH: [0.36, 0.55, 0.55, 0.55, 0.55], border: { type: "solid", color: K, pt: 0.75 } });
  txt(s, "C'est la méthode des produits partiels, sans écrire les lignes de 0 : un petit processeur multiplie ainsi, avec des décalages et des additions.", { x: 0.5, y: 5.0, w: 9.0, h: 0.55, fontSize: 13, italic: true });
}

// ============================== 10. 11d × 5d PAR DÉCALAGE + ADDITION (même exemple que la diapo 8)
{
  const s = slide("Même exemple : 11d × 5d avec un décalage et une addition",
    "On reprend la multiplication de la diapo 8 avec la méthode de la diapo 9. 5d = 101b = 4d + 1d, donc 11d × 5d = (11d × 4d) + 11d. 11d × 4d : on décale 0000 1011b de 2 rangs et on obtient 0010 1100b = 32 + 8 + 4 = 44d. On ajoute 11d = 0000 1011b. Addition : bit 1 : 0 + 1 = 1 ; bit 2 : 0 + 1 = 1 ; bit 4 : 1 + 0 = 1 ; bit 8 : 1 + 1 = 0 retenue 1 ; bit 16 : 0 + 0 + 1 = 1 ; bit 32 : 1 → 0011 0111b = 32 + 16 + 4 + 2 + 1 = 55d. On retrouve le résultat de la grille : ce sont les lignes 1 et 3, la ligne de 0 a disparu.");
  card(s, 0.5, 1.0, 9.0, 0.7);
  txt(s, "5d = 101b = 4d + 1d   donc   11d × 5d = (11d × 4d) + 11d", { x: 0.7, y: 1.05, w: 8.6, h: 0.6, fontSize: 17, bold: true, align: "center", valign: "middle" });
  const L = [
    ["11d", "0000 1011b", "nombre de départ : 8 + 2 + 1 = 11d"],
    ["11d × 4d", "0010 1100b", "× 2² → décaler de 2 rangs à gauche : 32 + 8 + 4 = 44d"],
    ["+ 11d", "0000 1011b", "le bit de poids 1 du 5 vaut 1 → on ajoute le nombre lui-même"],
    ["Somme", "0011 0111b", "32 + 16 + 4 + 2 + 1 = 55d = 44d + 11d ✓"],
  ];
  const H = { fill: { color: LG }, italic: true, fontSize: 13 };
  s.addTable([[cell("", H), cell("Binaire (8 bits)", H), cell("Comment", H)]].concat(L.map((r, i) => [
    cell(r[0], { bold: true, fontSize: 15, align: "left", fill: { color: i === 3 ? VLG : "FFFFFF" } }),
    cell(r[1], { fontFace: MONO, fontSize: 20, bold: true, fill: { color: i === 3 ? VLG : "FFFFFF" } }),
    cell(r[2], { fontSize: 12, align: "left", fill: { color: i === 3 ? VLG : "FFFFFF" } })])),
    { x: 0.5, y: 1.85, w: 9.0, colW: [1.35, 2.45, 5.2], rowH: [0.36, 0.5, 0.5, 0.5, 0.5], border: { type: "solid", color: K, pt: 0.75 } });
  txt(s, "Même résultat que la grille de la diapo 8 (lignes 1 et 3) : la ligne de 0 n'a pas besoin d'être écrite.", { x: 0.5, y: 4.65, w: 4.4, h: 0.9, fontSize: 13, italic: true, valign: "middle" });
  life(s, 5.1, 4.5, 4.4, 1.1, "Un microcontrôleur 8 bits sans multiplieur calcule × 5 ainsi (mise à l'échelle d'une mesure, par ex.) : 2 décalages + 1 addition.", 11);
}

// ============================== 11. POURQUOI GRAY
{
  const s = slide("Pourquoi le code Gray ? Le codeur rotatif",
    "Problème concret : un disque codeur lu par 3 capteurs optiques. En binaire, passer de 011 à 100 change 3 bits en même temps ; comme les capteurs ne sont jamais parfaitement alignés, on peut lire brièvement 111, 000, 101… → position fausse. En Gray, deux secteurs voisins ne diffèrent que d'un bit : la seule erreur possible est de lire l'un ou l'autre des deux secteurs voisins. Applications : codeurs angulaires de moteurs, bouton de volume rotatif, robotique. Source : Floyd 2-11 p. 90-92, fig. 2-7.");
  s.addImage({ path: "fig_disques.png", x: 0.4, y: 0.95, w: 5.6, h: 2.8 });
  txt(s, "Piste intérieure = MSB · foncé = 1, clair = 0", { x: 0.5, y: 3.8, w: 5.5, h: 0.3, fontSize: 11, italic: true, color: GR, align: "center" });
  card(s, 6.25, 1.0, 3.25, 1.45);
  txt(s, "Binaire : 011 → 100", { x: 6.4, y: 1.1, w: 3.0, h: 0.35, fontSize: 15, bold: true });
  txt(s, "3 bits changent en même temps. Un capteur un peu en avance → on lit 111 ou 000 : position fausse !", { x: 6.4, y: 1.5, w: 3.0, h: 0.9, fontSize: 12 });
  card(s, 6.25, 2.6, 3.25, 1.45);
  txt(s, "Gray : 010 → 110", { x: 6.4, y: 2.7, w: 3.0, h: 0.35, fontSize: 15, bold: true });
  txt(s, "Un seul bit change. On lit soit l'ancienne, soit la nouvelle position : jamais une fausse.", { x: 6.4, y: 3.1, w: 3.0, h: 0.9, fontSize: 12 });
  frame(s, 0.5, 4.35, 9.0, 1.15);
  txt(s, "Code Gray : entre deux valeurs voisines, un seul bit change.", { x: 0.7, y: 4.45, w: 8.6, h: 0.45, fontSize: 18, bold: true });
  txt(s, "C'est un code non pondéré : les bits n'ont pas de poids, on ne calcule pas avec le Gray.", { x: 0.7, y: 4.95, w: 8.6, h: 0.4, fontSize: 13 });
}

// ============================== 12. OÙ TROUVE-T-ON LE CODE GRAY ?
{
  const s = slide("Où trouve-t-on le code Gray ?",
    "Trois familles d'applications à citer avec des objets que les apprentis connaissent. 1) Codeur incrémental : bouton de volume d'un autoradio, molette de souris, bouton de réglage d'un oscilloscope ou d'une alimentation de labo. Deux contacts A et B donnent la suite 00 → 01 → 11 → 10 (code Gray à 2 bits) ; un seul contact change à chaque cran, et l'ordre de la suite donne le sens de rotation (horaire : 00 → 01 → 11 → 10 ; antihoraire : 00 → 10 → 11 → 01). 2) Codeur absolu : angle d'un bras de robot, axe de machine-outil CNC, orientation d'un panneau solaire ou des pales d'une éolienne ; le disque est gravé en Gray, la position est juste dès la mise sous tension et jamais fausse pendant une transition. 3) Plus loin dans la formation : les tableaux de Karnaugh (simplification des fonctions logiques) rangent leurs cases dans l'ordre Gray.");
  s.addImage({ path: "fig_quadrature.png", x: 0.45, y: 0.95, w: 6.1, h: 2.29 });
  card(s, 6.8, 0.95, 2.7, 2.3);
  txt(s, "Sens de rotation", { x: 6.95, y: 1.05, w: 2.4, h: 0.3, fontSize: 13, bold: true });
  txt(s, "horaire :\n00 → 01 → 11 → 10\n\nantihoraire :\n00 → 10 → 11 → 01", { x: 6.95, y: 1.4, w: 2.45, h: 1.75, fontSize: 12, fontFace: MONO });
  const A = [
    ["Bouton rotatif", "Volume d'un autoradio, molette de souris, réglage d'un oscilloscope : 2 contacts A et B = Gray à 2 bits."],
    ["Codeur absolu", "Angle d'un bras de robot, axe de machine CNC, orientation d'un panneau solaire : disque gravé en Gray."],
    ["Logique (plus tard)", "Les tableaux de Karnaugh rangent leurs cases en code Gray pour simplifier les fonctions logiques."],
  ];
  A.forEach((a, i) => {
    const x = 0.5 + i * 3.05;
    frame(s, x, 3.5, 2.9, 2.05);
    badge(s, x + 0.15, 3.62, String(i + 1));
    txt(s, a[0], { x: x + 0.68, y: 3.62, w: 2.1, h: 0.42, fontSize: 14, bold: true, valign: "middle" });
    txt(s, a[1], { x: x + 0.15, y: 4.15, w: 2.6, h: 1.3, fontSize: 12 });
  });
}

// ============================== 13. TABLE GRAY / MIROIR
{
  const s = slide("La table du code Gray : la méthode du miroir",
    "Construction réfléchie (d'où le nom anglais « reflected binary code ») : on écrit la liste à n bits, on la recopie en miroir en dessous, puis on ajoute 0 devant la première moitié et 1 devant la seconde. Faire vérifier aux apprentis, sur la table, qu'un seul bit change entre deux colonnes voisines, y compris entre 15 et 0 (1000 → 0000) : le code est cyclique.");
  const H = { fill: { color: LG }, italic: true, fontSize: 11 };
  const mk = (from) => {
    const r1 = [cell("Décimal", Object.assign({ align: "left" }, H))], r2 = [cell("Binaire", { align: "left", fontSize: 11, italic: true })], r3 = [cell("Gray", { align: "left", fontSize: 11, bold: true, fill: { color: VLG } })];
    for (let i = from; i < from + 8; i++) {
      r1.push(cell(i, H));
      r2.push(cell(i.toString(2).padStart(4, "0"), { fontFace: MONO, fontSize: 13 }));
      r3.push(cell((i ^ (i >> 1)).toString(2).padStart(4, "0"), { fontFace: MONO, fontSize: 13, bold: true, fill: { color: VLG } }));
    }
    return [r1, r2, r3];
  };
  const opt = (y) => ({ x: 0.5, y, w: 9.0, colW: [1.0].concat(Array(8).fill(1.0)), rowH: 0.36, border: { type: "solid", color: K, pt: 0.75 } });
  s.addTable(mk(0), opt(1.0));
  s.addTable(mk(8), opt(2.2));
  const steps = [
    ["1 bit", "0\n1"],
    ["miroir", "0\n1\n1\n0"],
    ["2 bits", "00\n01\n11\n10"],
    ["3 bits", "000\n001\n011\n010\n110\n111\n101\n100"],
  ];
  txt(s, "Construire sans apprendre par cœur :", { x: 0.5, y: 3.45, w: 4, h: 0.3, fontSize: 13, bold: true });
  steps.forEach((st, i) => {
    const x = 0.5 + i * 1.25;
    txt(s, st[0], { x, y: 3.8, w: 1.1, h: 0.25, fontSize: 11, italic: true, color: GR, align: "center" });
    txt(s, st[1], { x, y: 4.05, w: 1.1, h: 1.65, fontSize: 10.5, fontFace: MONO, bold: true, align: "center", lineSpacingMultiple: 0.85 });
  });
  card(s, 5.6, 3.55, 3.9, 2.0);
  txt(s, [
    { text: "On écrit la liste.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "On la recopie en miroir dessous.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "On met 0 devant la 1re moitié, 1 devant la 2e.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "On recommence pour 1 bit de plus.", options: { bullet: { type: "number" } } },
  ], { x: 5.8, y: 3.7, w: 3.55, h: 1.75, fontSize: 13, paraSpaceAfter: 4, valign: "middle" });
}

// ============================== 14. BINAIRE → GRAY
{
  const s = slide("Convertir binaire → Gray",
    "Règle : le MSB est recopié, puis chaque bit Gray vaut 1 si les deux bits binaires voisins sont différents, 0 s'ils sont identiques. C'est la fonction OU exclusif (symbole CEI « =1 »), qu'on retrouvera au chapitre des portes logiques. Exemple : 1011b → 1, 1⊕0 = 1, 0⊕1 = 1, 1⊕1 = 0 → 1110 Gray. Contrôle avec la table : 11d → 1110. Source : Floyd 2-11 p. 90-91.");
  card(s, 0.5, 1.05, 4.3, 2.6);
  badge(s, 0.7, 1.25, "1");
  txt(s, "Recopier le MSB (bit de gauche).", { x: 1.3, y: 1.25, w: 3.4, h: 0.45, fontSize: 14, valign: "middle" });
  badge(s, 0.7, 1.95, "2");
  txt(s, "De gauche à droite, comparer chaque paire de bits binaires voisins :", { x: 1.3, y: 1.9, w: 3.4, h: 0.6, fontSize: 14, valign: "middle" });
  txt(s, "différents → 1\nidentiques → 0", { x: 1.3, y: 2.55, w: 3.4, h: 0.65, fontSize: 15, bold: true });
  txt(s, "C'est le OU exclusif (CEI : « =1 »).", { x: 1.3, y: 3.2, w: 3.4, h: 0.35, fontSize: 12, italic: true, color: GR });
  s.addImage({ path: "fig_gray_xor.png", x: 5.0, y: 1.0, w: 4.5, h: 2.76 });
  frame(s, 0.5, 3.95, 9.0, 1.6);
  txt(s, "Exemple : 1011b", { x: 0.7, y: 4.05, w: 3, h: 0.35, fontSize: 14, bold: true });
  const ex = [["b", "1", "0", "1", "1"], ["g", "1", "1⊕0=1", "0⊕1=1", "1⊕1=0"]];
  txt(s, "Binaire :   1     0     1     1", { x: 0.7, y: 4.45, w: 5, h: 0.4, fontSize: 16, fontFace: MONO, bold: true });
  txt(s, "Gray :      1     1     1     0", { x: 0.7, y: 4.95, w: 5, h: 0.4, fontSize: 16, fontFace: MONO, bold: true });
  txt(s, "recopié · 1≠0 → 1 · 0≠1 → 1 · 1=1 → 0", { x: 5.6, y: 4.5, w: 3.8, h: 0.4, fontSize: 12, color: GR });
  txt(s, "Résultat : 1110 (Gray)", { x: 5.6, y: 4.95, w: 3.8, h: 0.4, fontSize: 15, bold: true });
}

// ============================== 15. GRAY → BINAIRE
{
  const s = slide("Convertir Gray → binaire",
    "Différence essentielle avec le sens inverse : on compare le bit binaire qu'on VIENT DE TROUVER avec le bit Gray suivant (et non deux bits Gray entre eux). Exemple : 1101 Gray → b3 = 1 ; b2 = 1⊕1 = 0 ; b1 = 0⊕0 = 0 ; b0 = 0⊕1 = 1 → 1001b = 9d. Contrôle avec la table : 9d ↔ 1101. Source : Floyd 2-11 p. 91 (exemple 2-37).");
  card(s, 0.5, 1.05, 4.3, 2.35);
  badge(s, 0.7, 1.25, "1");
  txt(s, "Recopier le MSB.", { x: 1.3, y: 1.25, w: 3.4, h: 0.45, fontSize: 14, valign: "middle" });
  badge(s, 0.7, 1.95, "2");
  txt(s, "Bit binaire suivant = bit binaire qu'on vient d'écrire ⊕ bit Gray suivant.", { x: 1.3, y: 1.85, w: 3.4, h: 0.85, fontSize: 14, valign: "middle" });
  txt(s, "différents → 1 · identiques → 0", { x: 1.3, y: 2.8, w: 3.4, h: 0.4, fontSize: 13, bold: true });
  frame(s, 5.1, 1.05, 4.4, 2.35);
  txt(s, "Piège n° 1", { x: 5.3, y: 1.15, w: 4, h: 0.35, fontSize: 15, bold: true });
  txt(s, "On ne compare pas deux bits Gray entre eux ! On compare toujours avec le bit binaire déjà trouvé (la flèche en diagonale).", { x: 5.3, y: 1.55, w: 4.0, h: 1.7, fontSize: 14 });
  // diagonale
  const g = ["1", "1", "0", "1"], b = ["1", "0", "0", "1"];
  frame(s, 0.5, 3.65, 9.0, 1.9);
  txt(s, "Gray", { x: 0.7, y: 3.85, w: 1.2, h: 0.45, fontSize: 14, italic: true, valign: "middle" });
  txt(s, "Binaire", { x: 0.7, y: 4.8, w: 1.2, h: 0.45, fontSize: 14, italic: true, valign: "middle" });
  for (let i = 0; i < 4; i++) {
    const x = 2.2 + i * 1.6;
    txt(s, g[i], { x, y: 3.85, w: 0.5, h: 0.45, fontSize: 22, bold: true, fontFace: MONO, align: "center", valign: "middle" });
    txt(s, b[i], { x, y: 4.8, w: 0.5, h: 0.45, fontSize: 22, bold: true, fontFace: MONO, align: "center", valign: "middle" });
    s.addShape(pres.shapes.LINE, { x: x + 0.25, y: 4.32, w: 0, h: 0.45, line: { color: K, width: 1.2, endArrowType: "triangle" } });
    if (i < 3) s.addShape(pres.shapes.LINE, { x: x + 0.55, y: 4.95, w: 1.0, h: 0, line: { color: GR, width: 1.2, dashType: "dash", endArrowType: "triangle" } });
    if (i > 0) txt(s, `${b[i - 1]}⊕${g[i]}=${b[i]}`, { x: x - 0.7, y: 4.35, w: 1.0, h: 0.3, fontSize: 10, color: GR, align: "center" });
  }
  txt(s, "1101 Gray = 1001b = 9d", { x: 7.3, y: 4.25, w: 2.1, h: 0.6, fontSize: 13, bold: true, align: "center", valign: "middle" });
}

// ============================== 16. COMPLÉMENT À 1
{
  const s = slide("Complément à 1 : on inverse chaque bit",
    "Le complément à 1 (C1) s'obtient en remplaçant chaque 0 par 1 et chaque 1 par 0. En électronique : 8 inverseurs en parallèle (symbole CEI : rectangle « 1 » avec indicateur de négation en sortie). Exemple : 0010 1101b (45d) → 1101 0010b. On travaille toujours avec un nombre de bits fixé (ici 8 bits) : les 0 de gauche comptent ! Source : Floyd 2-5 p. 63, fig. 2-2.");
  s.addImage({ path: "fig_inverseurs.png", x: 0.5, y: 1.0, w: 5.6, h: 2.25 });
  txt(s, "8 inverseurs CEI en parallèle : 0010 1101b (45d) → 1101 0010b", { x: 0.5, y: 3.3, w: 5.6, h: 0.3, fontSize: 11, italic: true, color: GR, align: "center" });
  card(s, 6.4, 1.0, 3.1, 2.6);
  txt(s, "Règle", { x: 6.6, y: 1.1, w: 2.7, h: 0.35, fontSize: 15, bold: true });
  txt(s, "0 → 1\n1 → 0", { x: 6.6, y: 1.5, w: 2.7, h: 0.9, fontSize: 24, bold: true, fontFace: MONO, align: "center" });
  txt(s, "pour tous les bits, y compris les 0 de gauche.", { x: 6.6, y: 2.5, w: 2.7, h: 0.8, fontSize: 13 });
  frame(s, 0.5, 3.9, 9.0, 1.65);
  txt(s, "Toujours fixer le nombre de bits d'abord", { x: 0.7, y: 4.0, w: 8.6, h: 0.35, fontSize: 15, bold: true });
  txt(s, "101b sur 4 bits = 0101b → C1 = 1010b\n101b sur 8 bits = 0000 0101b → C1 = 1111 1010b", { x: 0.7, y: 4.45, w: 8.6, h: 0.9, fontSize: 16, fontFace: MONO });
}

// ============================== 17. COMPLÉMENT À 2
{
  const s = slide("Complément à 2 : complément à 1, puis + 1",
    "Deux méthodes, même résultat. Méthode A (de base) : C1 puis + 1 (en ignorant une éventuelle retenue au-delà des 8 bits). Méthode B (rapide, pour le contrôle) : de droite à gauche, on recopie les bits jusqu'au premier 1 inclus, puis on inverse tout le reste. Exemple : 0010 1101b → C1 1101 0010b → C2 1101 0011b. Source : Floyd 2-5 p. 64, exemples 2-12 et 2-13.");
  const H = { fill: { color: LG }, italic: true, fontSize: 12 };
  const M = { fontFace: MONO, fontSize: 18, bold: true };
  txt(s, "Méthode A : C1 + 1", { x: 0.5, y: 1.0, w: 4.4, h: 0.35, fontSize: 16, bold: true });
  s.addTable([
    [cell("", H), cell("8 bits", H), cell("", H)],
    [cell("Nombre", { align: "left", fontSize: 13 }), cell("0010 1101", M), cell("45d", { fontSize: 13 })],
    [cell("C1", { align: "left", fontSize: 13 }), cell("1101 0010", M), cell("inverser", { fontSize: 12, color: GR })],
    [cell("+ 1", { align: "left", fontSize: 13 }), cell("0000 0001", M), cell("ajouter 1", { fontSize: 12, color: GR })],
    [cell("C2", { align: "left", fontSize: 13, bold: true, fill: { color: VLG } }), cell("1101 0011", Object.assign({}, M, { fill: { color: VLG } })), cell("", { fill: { color: VLG } })],
  ], { x: 0.5, y: 1.4, w: 4.4, colW: [1.15, 2.1, 1.15], rowH: 0.48, border: { type: "solid", color: K, pt: 0.75 } });
  card(s, 5.15, 1.0, 4.35, 2.85);
  txt(s, "Méthode B : la méthode rapide", { x: 5.35, y: 1.1, w: 4.0, h: 0.35, fontSize: 16, bold: true });
  txt(s, "De droite à gauche : recopier jusqu'au premier «\u00a01\u00a0» inclus, puis inverser tout le reste.", { x: 5.35, y: 1.5, w: 4.0, h: 0.8, fontSize: 13 });
  txt(s, "0010 110 | 1\n1101 001 | 1", { x: 5.35, y: 2.35, w: 4.0, h: 0.85, fontSize: 20, bold: true, fontFace: MONO, align: "center" });
  txt(s, "inversé      recopié", { x: 5.35, y: 3.25, w: 4.0, h: 0.35, fontSize: 12, color: GR, align: "center", fontFace: MONO });
  frame(s, 0.5, 4.15, 9.0, 1.4);
  txt(s, "Vérification qui marche toujours", { x: 0.7, y: 4.25, w: 8.6, h: 0.35, fontSize: 15, bold: true });
  txt(s, "Nombre + C2 = 0 (la retenue du 9e bit est ignorée) :\n0010 1101 + 1101 0011 = 1 0000 0000  →  0000 0000", { x: 0.7, y: 4.65, w: 8.6, h: 0.8, fontSize: 14 });
}

// ============================== 18. NOMBRES NÉGATIFS
{
  const s = slide("À quoi ça sert ? Les nombres négatifs",
    "En complément à 2 sur 8 bits, le MSB a un poids de −128 : c'est le bit de signe (0 = positif, 1 = négatif). −45d s'écrit donc C2(45) = 1101 0011b = −128 + 64 + 16 + 2 + 1. Étendue : −128d à +127d. Intérêt majeur : la soustraction devient une addition, donc le processeur n'a besoin que d'un additionneur. Exemple : 80 − 45 = 80 + (−45) → la retenue du 9e bit est rejetée → 0010 0011b = 35d. Source : Floyd 2-6 p. 66-68 et 2-7 p. 72-73.");
  const H = { fill: { color: LG }, italic: true, fontSize: 11 };
  const W = ["−128", "64", "32", "16", "8", "4", "2", "1"];
  s.addTable([
    [cell("Poids", Object.assign({ align: "left" }, H))].concat(W.map((w, i) => cell(w, Object.assign({}, H, i === 0 ? { bold: true } : {})))).concat([cell("Valeur", H)]),
    [cell("−45d", { align: "left", bold: true })].concat("11010011".split("").map((x, i) => cell(x, { fontFace: MONO, fontSize: 18, bold: true, fill: { color: i === 0 ? VLG : "FFFFFF" } }))).concat([cell("−128+64+16+2+1", { fontSize: 10 })]),
  ], { x: 0.5, y: 1.05, w: 9.0, colW: [1.0].concat(Array(8).fill(0.72)).concat([2.24]), rowH: [0.36, 0.55], border: { type: "solid", color: K, pt: 0.75 } });
  txt(s, "Bit de signe : 0 = positif, 1 = négatif · étendue sur 8 bits : −128d à +127d", { x: 0.5, y: 2.05, w: 9, h: 0.35, fontSize: 13, italic: true });
  card(s, 0.5, 2.6, 5.3, 2.95);
  txt(s, "Soustraire = additionner le C2 : 80d − 45d = 80d + (−45d)", { x: 0.7, y: 2.7, w: 5.0, h: 0.6, fontSize: 14, bold: true });
  const rows = [["    0101 0000", "+80d"], ["  + 1101 0011", "−45d"], ["  -----------", ""], ["  1 0010 0011", "→ +35d ✓"]];
  rows.forEach((r, i) => {
    txt(s, r[0], { x: 0.8, y: 3.3 + i * 0.47, w: 3.4, h: 0.45, fontSize: 18, fontFace: MONO, bold: i === 3 });
    txt(s, r[1], { x: 4.3, y: 3.35 + i * 0.47, w: 1.45, h: 0.4, fontSize: 13, color: i === 3 ? K : GR });
  });
  txt(s, "la retenue du 9e bit est rejetée", { x: 0.8, y: 5.2, w: 4.9, h: 0.3, fontSize: 11, italic: true, color: GR });
  life(s, 6.05, 2.6, 3.45, 2.95, "Un capteur de température numérique envoie sa mesure en C2 sur 8 bits :\n0001 1001b = +25 °C\n1111 0110b = −10 °C\nLe microcontrôleur calcule l'écart 25 − (−10) = 35 °C avec son seul additionneur.", 12);
}

// ============================== 19. PIÈGES
{
  const s = slide("Les 6 pièges classiques",
    "Faire chercher en binôme, pour chaque piège, un exemple d'erreur et sa correction (auto-explication). Ce sont les erreurs observées le plus souvent aux tests.");
  const P = [
    ["Écrire 1 + 1 = 2", "Le chiffre 2 n'existe pas : 1 + 1 = 10b."],
    ["Oublier une retenue", "Écrire les retenues au-dessus, toujours."],
    ["Décaler sans limite", "En 8 bits, le bit qui sort à gauche est perdu."],
    ["Gray → binaire", "Comparer avec le bit binaire trouvé, pas avec le Gray."],
    ["Oublier le nombre de bits", "C1 et C2 se calculent sur un format fixé (4, 8, 16 bits)."],
    ["Oublier le « + 1 »", "C2 = C1 + 1. Contrôle : nombre + C2 = 0."],
  ];
  P.forEach((p, i) => {
    const x = 0.5 + (i % 2) * 4.55, y = 1.0 + Math.floor(i / 2) * 1.55;
    card(s, x, y, 4.35, 1.35);
    badge(s, x + 0.18, y + 0.2, String(i + 1));
    txt(s, p[0], { x: x + 0.78, y: y + 0.18, w: 3.45, h: 0.45, fontSize: 15, bold: true, valign: "middle" });
    txt(s, p[1], { x: x + 0.78, y: y + 0.65, w: 3.45, h: 0.6, fontSize: 13 });
  });
}

// ============================== 20. TICKET DE SORTIE
{
  const s = slide("Ticket de sortie : 4 questions, 4 minutes",
    "Évaluation formative : une question par objectif. Ramasser les tickets pour adapter la prochaine leçon.\nRéponses : 1) 0111b + 0101b = 1100b (7 + 5 = 12). 2) 0001 0110b × 4 = 0101 1000b (22 × 4 = 88 : 2 décalages). 3) 1001b → 1101 Gray. 4) C2 de 0001 1000b (24d) = 1110 1000b (= −24d).\nDevoirs : feuille d'exercices + exercice Gray Nextec Media + Floyd p. 104-107, problèmes 15, 17, 21, 22, 25, 56, 57.");
  const Q = [["1", "0111b + 0101b = ?"], ["2", "0001 0110b × 4 = ?  (par décalage)"], ["3", "1001b en code Gray = ?"], ["4", "Complément à 2 de 0001 1000b = ?"]];
  Q.forEach((q, i) => {
    const y = 1.0 + i * 0.72;
    frame(s, 0.5, y, 5.6, 0.6);
    badge(s, 0.62, y + 0.09, q[0]);
    txt(s, q[1], { x: 1.2, y: y + 0.08, w: 4.8, h: 0.45, fontSize: 16, bold: true, valign: "middle" });
  });
  card(s, 6.4, 1.0, 3.1, 2.75);
  txt(s, "Auto-évaluation", { x: 6.6, y: 1.1, w: 2.7, h: 0.35, fontSize: 14, bold: true });
  txt(s, "Pour chaque objectif, je note :\n✓ je sais faire seul·e\n~ je sais avec la fiche\n✗ je dois revoir", { x: 6.6, y: 1.5, w: 2.75, h: 2.1, fontSize: 13 });
  frame(s, 0.5, 4.05, 9.0, 1.5);
  txt(s, "Pour s'entraîner", { x: 0.7, y: 4.12, w: 8.6, h: 0.35, fontSize: 14, bold: true });
  s.addText([
    { text: "Feuille d'exercices « Arithmétique binaire, code Gray et compléments »", options: { breakLine: true } },
    { text: "Nextec Media – exercice complémentaire code Gray", options: { hyperlink: { url: NEXTEC_GRAY }, breakLine: true } },
    { text: "Floyd chap. 2 (PDF), problèmes p. 104-107 : n° 15, 17 (2-4) · 21, 22 (2-5) · 25 (2-6) · 56, 57 (2-11)", options: { hyperlink: { url: FLOYD_PDF, tooltip: "Ouvrir le chapitre 2 du Floyd" } } },
  ], { x: 0.7, y: 4.5, w: 8.6, h: 1.0, fontFace: F, fontSize: 12, color: K, margin: 0, valign: "top", paraSpaceAfter: 3, isTextBox: true });
}

pres.writeFile({ fileName: "deck.pptx" }).then(() => console.log("deck ok"));
