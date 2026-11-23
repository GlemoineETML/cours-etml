// Présentation « Conversion analogique-numérique et numérique-analogique (CAN / CNA) » — charte ETML couleurs (T&M : marine 242852, bleu 297FD5), Arial, 16:10
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.defineLayout({ name: "ETML1610", width: 10, height: 6.25 });
pres.layout = "ETML1610";
pres.author = "Gaël Lemoine";
pres.company = "ETML – Section électronique";
pres.title = "Conversion analogique-numérique et numérique-analogique";
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };

const NAVY = "242852", BLUE = "297FD5", LBLUE = "ACCBF9", TINT = "E8EFFB";
const K = NAVY, GR = "5A6478", LG = LBLUE, VLG = TINT, RED = "EE0000";
const F = "Arial", MONO = "Courier New";
const TITLE = "Conversion analogique-numérique et numérique-analogique";
const TOPIC = "Test et Mesure 1 – El DT 1 · Conversion A/N et N/A (CAN / CNA)";
const MODULE = "Test et Mesure 1 – El DT 1", CLASSE = "XLO1", ANNEE = "2026-2027", CHAMP = "sur la vie, niveau 2";
const DATE_US = "11/04/2026";              // date à l'américaine (MM/DD/YYYY)
// Références : liens à compléter (Floyd, Nextec) — laisser l'URL vide affiche un emplacement repérable
const FLOYD_URL = "", NEXTEC_URL = "", NEXTEC_EX_URL = "";
const LOGO_BAND = "logo_white_v.png";      // logo ETML du modèle Rapport_Simple.dotx, en blanc, tourné à 90° pour le bandeau

const BAND = () => [
  { rect: { x: 9.25, y: 0, w: 0.75, h: 6.25, fill: { color: NAVY } } },
  { image: { path: LOGO_BAND, x: 9.39, y: 0.35, w: 0.47, h: 1.95 } },
  { text: { text: "Electronique", options: { x: 8.325, y: 3.675, w: 2.6, h: 0.75, rotate: 270, fontFace: F, fontSize: 20, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0 } } },
];
pres.defineSlideMaster({
  title: "CONTENU", background: { color: "FFFFFF" },
  objects: BAND().concat([
    { line: { x: 0.5, y: 5.78, w: 8.4, h: 0, line: { color: BLUE, width: 0.75 } } },
    { text: { text: "Section électronique", options: { x: 0.5, y: 5.82, w: 2.4, h: 0.3, fontFace: F, fontSize: 9, italic: true, color: NAVY, margin: 0 } } },
    { text: { text: TOPIC, options: { x: 2.9, y: 5.82, w: 6.0, h: 0.3, fontFace: F, fontSize: 9, color: GR, align: "right", margin: 0 } } },
    { rect: { x: 9.37, y: 5.62, w: 0.5, h: 0.5, fill: { color: LBLUE } } },
  ]),
  slideNumber: { x: 9.37, y: 5.62, w: 0.5, h: 0.5, fontFace: F, fontSize: 12, bold: true, color: NAVY, align: "center", valign: "middle" },
});
pres.defineSlideMaster({
  title: "TITRE", background: { color: "FFFFFF" },
  objects: BAND().concat([
    { line: { x: 0.6, y: 5.6, w: 8.3, h: 0, line: { color: BLUE, width: 0.75 } } },
    { text: { text: "Section électronique", options: { x: 0.6, y: 5.66, w: 4, h: 0.3, fontFace: F, fontSize: 11, italic: true, color: NAVY, margin: 0 } } },
    { text: { text: `Version : ${DATE_US} / 1.0`, options: { x: 5.4, y: 5.66, w: 3.5, h: 0.3, fontFace: F, fontSize: 11, color: NAVY, align: "right", margin: 0 } } },
  ]),
});

// Zone utile x ≤ 8,9" à cause du bandeau : compression horizontale des positions écrites sur une grille de 0,5 à 9,5"
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
  s.addText = (t, o) => at(t, fx(o)); s.addShape = (sh, o) => ash(sh, fx(o));
  s.addImage = (o) => ai(fx(o, true)); s.addTable = (r, o) => atb(r, fx(o));
  return s;
}
function slide(title, notes) {
  const s = pres.addSlide({ masterName: "CONTENU" });
  s.addText(expand(title), { x: 0.5, y: 0.25, w: 8.4, h: 0.5, fontFace: F, fontSize: 24, bold: true, color: NAVY, margin: 0, valign: "middle", isTextBox: true, fit: "shrink" });
  squeeze(s, 0.5, 9.5, 8.9);
  if (notes) s.addNotes(notes);
  return s;
}

// indices : « U_ref », « f_max », « Uₑ », « fₑ », « Tₑ », « Uₛ » → U avec indice réel (notation CEI)
const SUBRE = /([UfTq])(?:_(ref|max|e|s)|(ₑ|ₛ))/g;
function R(str, base) {
  base = base || {};
  if (typeof str !== "string" || !str.match(SUBRE)) return null;
  const out = []; let pos = 0; SUBRE.lastIndex = 0; let m;
  while ((m = SUBRE.exec(str))) {
    if (m.index > pos) out.push({ text: str.slice(pos, m.index), options: Object.assign({}, base) });
    out.push({ text: m[1], options: Object.assign({}, base) });
    out.push({ text: m[2] || (m[3] === "ₑ" ? "e" : "s"), options: Object.assign({}, base, { subscript: true }) });
    pos = m.index + m[0].length;
  }
  if (pos < str.length) out.push({ text: str.slice(pos), options: Object.assign({}, base) });
  out.forEach((r, i) => {
    if (i < out.length - 1) delete r.options.breakLine;
    if (i > 0) { delete r.options.bullet; delete r.options.indentLevel; delete r.options.paraSpaceAfter; }
  });
  return out;
}
function expand(t) {
  if (typeof t === "string") return R(t) || t;
  if (Array.isArray(t)) return [].concat(...t.map(r => (r && typeof r.text === "string" && R(r.text, r.options)) || [r]));
  return t;
}
function txt(s, text, o) { s.addText(expand(text), Object.assign({ fontFace: F, fontSize: 15, color: K, margin: 0, valign: "top", isTextBox: true }, o)); }
function card(s, x, y, w, h, fill) { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill || VLG }, line: { color: fill || VLG, width: 0 } }); }
function frame(s, x, y, w, h) { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.25 } }); }
function life(s, x, y, w, h, text, fs) {
  card(s, x, y, w, h);
  s.addText(expand([{ text: "Dans la vraie vie", options: { bold: true, color: BLUE, breakLine: true } }, { text, options: { color: K } }]),
    { x: x + 0.18, y: y + 0.1, w: w - 0.36, h: h - 0.2, fontFace: F, fontSize: fs || 12, margin: 0, valign: "top", paraSpaceAfter: 3, isTextBox: true });
}
function badge(s, x, y, label) {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.42, h: 0.42, fill: { color: K }, line: { color: K } });
  s.addText(label, { x, y, w: 0.42, h: 0.42, fontFace: F, fontSize: 14, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
}
const cell = (t, o) => ({ text: expand(String(t)), options: Object.assign({ align: "center", valign: "middle", fontFace: F, fontSize: 13 }, o || {}) });
const H = { fill: { color: LG }, italic: true, fontSize: 12, color: NAVY };
const BORDER = { type: "solid", color: K, pt: 0.75 };
const sub = (t) => ({ text: t, options: { subscript: true } });
// lien : cliquable si l'URL est connue, sinon emplacement « [lien à compléter] » en gris
const link = (label, url, extra) => url
  ? { text: label, options: Object.assign({ hyperlink: { url } }, extra || {}) }
  : { text: label + " [lien à compléter]", options: Object.assign({ color: GR }, extra || {}) };

// ============================== 1. TITRE
{
  const s = pres.addSlide({ masterName: "TITRE" });
  txt(s, "TEST ET MESURE 1 – EL DT 1", { x: 0.6, y: 0.55, w: 5.4, h: 0.35, fontSize: 13, bold: true, color: BLUE, charSpacing: 1 });
  txt(s, "Conversion analogique-numérique et numérique-analogique", { x: 0.6, y: 0.95, w: 5.4, h: 1.4, fontSize: 27, bold: true, color: NAVY });
  txt(s, "CAN (ADC) et CNA (DAC)", { x: 0.6, y: 2.35, w: 5.3, h: 0.4, fontSize: 17, color: GR });
  txt(s, "Comment un thermomètre, un téléphone ou un multimètre transforment une tension en nombre… et l'inverse.", { x: 0.6, y: 2.8, w: 5.3, h: 0.7, fontSize: 13, italic: true, color: NAVY });
  ["Résolution et quantum", "Tension ↔ code", "Échantillonnage", "CNA et applications"].forEach((t, i) => {
    const x = 0.6 + (i % 2) * 2.7, y = 3.6 + Math.floor(i / 2) * 0.48;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.55, h: 0.4, rectRadius: 0.08, fill: { color: NAVY }, line: { color: NAVY } });
    txt(s, t, { x, y, w: 2.55, h: 0.4, fontSize: 12, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
  });
  card(s, 0.6, 4.6, 8.3, 0.88);
  s.addText([
    { text: `Classe ${CLASSE} · année ${ANNEE} · champ d'apprentissage : ${CHAMP}`, options: { bold: true, breakLine: true } },
    { text: `Éditeur : Gaël Lemoine · ${DATE_US}`, options: { color: GR } },
  ], { x: 0.8, y: 4.65, w: 7.9, h: 0.78, fontFace: F, fontSize: 12, color: NAVY, margin: 0, valign: "middle", isTextBox: true });
  s.addImage({ path: "fig_escalier.png", x: 6.15, y: 0.6, w: 2.75, h: 1.98 });
  txt(s, "La fonction de transfert d'un CAN : un escalier", { x: 6.0, y: 2.65, w: 3.0, h: 0.5, fontSize: 10, italic: true, color: GR, align: "center" });
  s.addNotes("Durée ≈ 2 × 45 min de théorie + 2 × 45 min d'exercices. Déroulé : échauffement (5 min) → pourquoi convertir (5 min) → résolution et quantum (10 min) → tension ↔ code avec exemple guidé (15 min) → approximations successives (10 min) → échantillonnage (10 min) → CNA (15 min) → symboles CEI et multimètre (10 min) → application LM35 (5 min) → pièges et ticket de sortie (5 min). Prérequis : binaire et puissances de 2 (leçon « Systèmes de numération »).");
}

// ============================== 2. OBJECTIFS
{
  const s = slide("À la fin de cette leçon, je suis capable de…",
    "Lire les objectifs à voix haute. En fin de leçon, chaque apprenti s'auto-évalue sur chaque « je suis capable » (✓ / ~ / ✗). Les compétences visées sont transversales au métier : lire la fiche technique d'un convertisseur, choisir une résolution, interpréter une valeur affichée par un appareil de mesure numérique.");
  const items = [
    ["1", "Expliquer pourquoi on convertit et situer CAN et CNA dans une chaîne de mesure."],
    ["2", "Calculer le nombre de niveaux et le quantum q d'un convertisseur de n bits."],
    ["3", "Convertir une tension en code (CAN) et un code en tension (CNA)."],
    ["4", "Choisir une fréquence d'échantillonnage suffisante (règle de Shannon)."],
    ["5", "Lire les symboles CEI et la résolution d'un multimètre numérique."],
  ];
  items.forEach((it, i) => {
    const col = i < 3 ? 0 : 1, row = i < 3 ? i : i - 3;
    const x = 0.5 + col * 4.55, y = 1.0 + row * 0.95;
    card(s, x, y, 4.35, 0.82);
    badge(s, x + 0.15, y + 0.2, it[0]);
    txt(s, it[1], { x: x + 0.72, y: y + 0.06, w: 3.5, h: 0.7, fontSize: 13, valign: "middle" });
  });
  frame(s, 5.05, 2.9, 4.45, 0.82);
  txt(s, "Prérequis : binaire, poids des bits, puissances de 2.", { x: 5.25, y: 2.95, w: 4.1, h: 0.72, fontSize: 13, italic: true, valign: "middle" });
  frame(s, 0.5, 4.0, 9.0, 1.55);
  txt(s, "Ressources", { x: 0.7, y: 4.08, w: 3, h: 0.3, fontSize: 13, bold: true });
  s.addText(expand([
    link("Floyd – chapitre « Conversion analogique-numérique et numérique-analogique » (PDF sur Teams)", FLOYD_URL, { breakLine: true }),
    link("Nextec Media – chapitre sur les convertisseurs A/N et N/A", NEXTEC_URL, { breakLine: true }),
    link("Nextec Media – exercices complémentaires", NEXTEC_EX_URL),
  ]), { x: 0.7, y: 4.42, w: 8.6, h: 1.05, fontFace: F, fontSize: 12, color: K, margin: 0, valign: "top", paraSpaceAfter: 4, isTextBox: true });
}

// ============================== 3. ÉCHAUFFEMENT
{
  const s = slide("Échauffement : 4 minutes, sans calculatrice",
    "Pratique de récupération (rappel des bases indispensables) : seul, puis comparaison avec le voisin, puis correction.\nRéponses : 1) 2⁸ = 256. 2) 1111 1111b = 255d. 3) 0110 0100b = 64 + 32 + 4 = 100d. 4) Question ouverte, sans corriger tout de suite : on y revient en fin de leçon (le micro donne une tension, un CAN la transforme en nombres plusieurs milliers de fois par seconde).");
  const q = [["2⁸ = ?", "Puissance de 2"], ["1111 1111b = ? d", "Plus grand nombre sur 8 bits"], ["0110 0100b = ? d", "Binaire → décimal"]];
  q.forEach((t, i) => {
    const x = 0.5 + i * 3.05;
    card(s, x, 1.05, 2.85, 2.1);
    badge(s, x + 0.2, 1.22, String(i + 1));
    txt(s, t[0], { x: x + 0.15, y: 1.75, w: 2.55, h: 0.8, fontSize: 21, bold: true, align: "center", valign: "middle" });
    txt(s, t[1], { x: x + 0.15, y: 2.6, w: 2.55, h: 0.4, fontSize: 12, color: GR, align: "center" });
  });
  frame(s, 0.5, 3.45, 9.0, 1.3);
  badge(s, 0.7, 3.7, "4");
  txt(s, "Défi : ta voix est une onde de pression, donc une grandeur continue. Comment ton téléphone peut-il l'enregistrer sous forme de 0 et de 1 ?", { x: 1.3, y: 3.55, w: 8.0, h: 1.1, fontSize: 15, valign: "middle" });
  txt(s, "Écris ta réponse seul·e → compare avec ton voisin → correction ensemble.", { x: 0.5, y: 5.0, w: 9, h: 0.4, fontSize: 14, italic: true });
}

// ============================== 4. POURQUOI CONVERTIR ?
{
  const s = slide("Le monde est analogique, le microcontrôleur est numérique",
    "Message clé : les grandeurs physiques (température, son, lumière, pression) varient de façon continue. Un capteur les transforme en tension. Le microcontrôleur, lui, ne manipule que des nombres binaires. Il faut donc un convertisseur analogique-numérique (CAN, en anglais ADC) à l'entrée et, si l'on veut agir sur le monde réel, un convertisseur numérique-analogique (CNA, en anglais DAC) à la sortie. Faire citer aux apprentis 3 appareils de leur quotidien contenant un CAN (téléphone, thermostat, balance de cuisine, multimètre, voiture…).");
  s.addImage({ path: "fig_chaine.png", x: 0.45, y: 0.95, w: 9.05, h: 2.23 });
  card(s, 0.5, 3.45, 2.9, 2.1);
  txt(s, "CAN = ADC", { x: 0.7, y: 3.55, w: 2.5, h: 0.35, fontSize: 15, bold: true });
  txt(s, "Analog to Digital Converter : tension → nombre binaire.", { x: 0.7, y: 3.95, w: 2.55, h: 1.5, fontSize: 13 });
  card(s, 3.55, 3.45, 2.9, 2.1);
  txt(s, "CNA = DAC", { x: 3.75, y: 3.55, w: 2.5, h: 0.35, fontSize: 15, bold: true });
  txt(s, "Digital to Analog Converter : nombre binaire → tension.", { x: 3.75, y: 3.95, w: 2.55, h: 1.5, fontSize: 13 });
  life(s, 6.6, 3.45, 2.9, 2.1, "Téléphone : micro → CAN → mémoire → CNA → écouteurs. Thermostat : sonde → CAN → régulation → CNA → vanne. Ta future carte électronique en contiendra presque toujours un.", 11.5);
}

// ============================== 5. TROIS ÉTAPES
{
  const s = slide("De l'analogique au numérique en 3 étapes",
    "1) Le signal analogique prend une infinité de valeurs. 2) Échantillonner : on ne mesure qu'à intervalles réguliers (période d'échantillonnage Tₑ, fréquence fₑ = 1/Tₑ). 3) Quantifier : chaque mesure est arrondie au niveau permis le plus proche par en dessous et codée en binaire. Ici 3 bits = 8 niveaux seulement : on voit bien la perte d'information. Avec 16 bits (65 536 niveaux), l'escalier devient invisible à l'œil et à l'oreille.");
  s.addImage({ path: "fig_signal.png", x: 0.45, y: 0.95, w: 9.05, h: 2.6 });
  const E = [["Échantillonner", "Combien de fois par seconde je mesure ?", "→ fréquence d'échantillonnage fₑ"],
             ["Quantifier", "Avec quelle finesse je mesure ?", "→ nombre de bits n, quantum q"],
             ["Coder", "Comment j'écris la mesure ?", "→ un nombre binaire de n bits"]];
  E.forEach((e, i) => {
    const x = 0.5 + i * 3.05;
    frame(s, x, 3.8, 2.85, 1.75);
    badge(s, x + 0.15, 3.92, String(i + 1));
    txt(s, e[0], { x: x + 0.68, y: 3.92, w: 2.1, h: 0.42, fontSize: 15, bold: true, valign: "middle" });
    txt(s, e[1], { x: x + 0.15, y: 4.45, w: 2.6, h: 0.5, fontSize: 12 });
    txt(s, e[2], { x: x + 0.15, y: 5.0, w: 2.6, h: 0.45, fontSize: 12, bold: true, color: BLUE });
  });
}

// ============================== 6. RÉSOLUTION ET QUANTUM
{
  const s = slide("Résolution : combien de « marches » ?",
    "Un CAN de n bits fournit 2ⁿ codes différents, de 0 à 2ⁿ − 1. La plage de mesure est fixée par la tension de référence U_ref. Le quantum q (ou LSB, Least Significant Bit) est la plus petite variation de tension que le convertisseur sait distinguer : q = U_ref / 2ⁿ. Faire calculer la ligne 8 bits ensemble, puis laisser compléter mentalement les autres (5 V / 1024 ≈ 4,88 mV). Insister : plus de bits = marches plus fines = mesure plus précise, mais convertisseur plus cher et souvent plus lent.");
  card(s, 0.5, 1.0, 4.2, 1.85);
  txt(s, [{ text: "Nombre de niveaux = 2", options: {} }, { text: "n", options: { superscript: true } }], { x: 0.7, y: 1.1, w: 3.9, h: 0.55, fontSize: 20, bold: true, align: "center" });
  txt(s, [{ text: "q = U", options: {} }, sub("ref"), { text: " / 2", options: {} }, { text: "n", options: { superscript: true } }], { x: 0.7, y: 1.7, w: 3.9, h: 0.55, fontSize: 22, bold: true, align: "center", color: BLUE });
  txt(s, "q = quantum = 1 LSB = la hauteur d'une marche", { x: 0.7, y: 2.3, w: 3.9, h: 0.4, fontSize: 12, italic: true, align: "center" });
  s.addTable([
    [cell("Bits n", H), cell("Niveaux 2ⁿ", H), cell("q pour U_ref = 5 V", H)],
    [cell("8"), cell("256"), cell("19,5 mV")],
    [cell("10"), cell("1 024"), cell("4,88 mV")],
    [cell("12"), cell("4 096"), cell("1,22 mV")],
    [cell("16"), cell("65 536"), cell("76,3 µV")],
  ], { x: 5.0, y: 1.0, w: 4.5, colW: [1.1, 1.5, 1.9], rowH: 0.37, border: BORDER });
  frame(s, 0.5, 3.1, 4.2, 1.15);
  txt(s, "Plus de bits → marches plus fines → mesure plus précise.", { x: 0.7, y: 3.2, w: 3.85, h: 0.95, fontSize: 14, bold: true, valign: "middle" });
  life(s, 5.0, 3.1, 4.5, 2.45, "Arduino Uno : CAN 10 bits, U_ref = 5 V → q ≈ 4,88 mV.\nMicrocontrôleur STM32 : 12 bits.\nCarte son, studio d'enregistrement : 24 bits.\nBalance de cuisine (jauge de contrainte) : jusqu'à 24 bits, car le signal du capteur ne fait que quelques millivolts.", 11.5);
  card(s, 0.5, 4.45, 4.2, 1.1);
  txt(s, [{ text: "Rappel unités : ", options: { bold: true } }, { text: "1 mV = 10⁻³ V · 1 µV = 10⁻⁶ V. Écris toujours l'unité et le préfixe." }], { x: 0.7, y: 4.52, w: 3.9, h: 0.96, fontSize: 12, valign: "middle" });
}

// ============================== 7. ESCALIER ET FORMULE
{
  const s = slide("Le CAN : de la tension au code",
    "La fonction de transfert d'un CAN est un escalier. Exemple : 3 bits, U_ref = 8 V → q = 1 V. Toute tension entre 2,0 V et 2,999 V donne le même code 010b : on perd l'information « à l'intérieur d'une marche ». C'est l'erreur de quantification, toujours inférieure à 1 q. Formule (convertisseur qui tronque, cas du Floyd et de la plupart des fiches techniques simplifiées) : N = partie entière de Uₑ / q. Si Uₑ ≥ U_ref, le CAN sature au code maximal 2ⁿ − 1 (ici 111b). Certains CAN arrondissent au lieu de tronquer : la fiche technique le précise.");
  s.addImage({ path: "fig_escalier.png", x: 0.45, y: 0.95, w: 4.6, h: 3.3 });
  card(s, 5.25, 1.0, 4.25, 1.5);
  txt(s, [{ text: "N = partie entière de ( U", options: {} }, sub("e"), { text: " / q )", options: {} }], { x: 5.4, y: 1.1, w: 4.0, h: 0.6, fontSize: 19, bold: true, align: "center" });
  txt(s, "on garde la partie avant la virgule, puis on écrit N en binaire sur n bits", { x: 5.4, y: 1.72, w: 4.0, h: 0.7, fontSize: 12, italic: true, align: "center" });
  frame(s, 5.25, 2.7, 4.25, 1.55);
  txt(s, "À retenir", { x: 5.45, y: 2.78, w: 3.9, h: 0.3, fontSize: 14, bold: true });
  txt(s, [
    { text: "Une marche = q volts.", options: { bullet: true, breakLine: true } },
    { text: "Erreur de quantification < 1 q.", options: { bullet: true, breakLine: true } },
    { text: "Code max = 2ⁿ − 1 (saturation).", options: { bullet: true } },
  ], { x: 5.45, y: 3.12, w: 3.95, h: 1.1, fontSize: 13, paraSpaceAfter: 2 });
  life(s, 0.5, 4.45, 9.0, 1.1, "Dans un programme Arduino, analogRead() renvoie justement ce nombre N (0 à 1023). C'est au programmeur de le convertir en volts, en degrés ou en bars : il doit donc connaître q.", 12);
}

// ============================== 8. EXEMPLE GUIDÉ
{
  const s = slide("Exemple guidé : 2,00 V dans un CAN 10 bits, U_ref = 5 V",
    "Exemple travaillé, à faire au tableau en verbalisant chaque étape. 1) q = 5 V / 1024 = 4,883 mV. 2) Uₑ / q = 2,00 V / 4,883 mV = 409,6 → N = 409. 3) 409 = 256 + 128 + 16 + 8 + 1 → 01 1001 1001b (10 bits). 4) Contrôle : 409 × 4,883 mV = 1,997 V : écart de 3 mV, plus petit que q ✓. Insister sur l'étape 4 : un professionnel contrôle toujours son résultat.");
  const steps = [
    ["1", "Quantum", "q = 5 V / 2¹⁰ = 5 V / 1024 = 4,883 mV"],
    ["2", "Nombre de marches", "Uₑ / q = 2,00 V / 4,883 mV = 409,6  →  N = 409"],
    ["3", "En binaire (10 bits)", "409 = 256 + 128 + 16 + 8 + 1  →  01 1001 1001b"],
    ["4", "Contrôle", "409 × 4,883 mV = 1,997 V  →  écart 3 mV < q  ✓"],
  ];
  steps.forEach((st, i) => {
    const y = 1.0 + i * 0.98;
    (i === 3 ? frame : card)(s, 0.5, y, 9.0, 0.82);
    badge(s, 0.68, y + 0.2, st[0]);
    txt(s, st[1], { x: 1.3, y: y + 0.08, w: 2.3, h: 0.66, fontSize: 14, bold: true, valign: "middle" });
    txt(s, st[2], { x: 3.5, y: y + 0.08, w: 5.95, h: 0.66, fontSize: 13.5, fontFace: MONO, bold: true, valign: "middle", fit: "shrink" });
  });
  txt(s, "Méthode : quantum → nombre de marches → binaire → contrôle. Toujours dans cet ordre.", { x: 0.5, y: 5.0, w: 9.0, h: 0.5, fontSize: 14, italic: true, valign: "middle" });
}

// ============================== 9. À TOI
{
  const s = slide("À toi : CAN 8 bits, U_ref = 5,12 V",
    "Exercice d'application, aide retirée progressivement : le quantum est donné, l'apprenti fait le reste. 3 min seul, puis comparaison avec le voisin.\nSolutions : q = 5,12 V / 256 = 20 mV. a) 1,30 V / 20 mV = 65 → 0100 0001b (64 + 1) ; contrôle 65 × 20 mV = 1,30 V. b) 3,47 V / 20 mV = 173,5 → 173 → 1010 1101b (128 + 32 + 8 + 4 + 1) ; 173 × 20 mV = 3,46 V. c) 6 V > U_ref : saturation, N = 255 = 1111 1111b. Le CAN affiche 5,10 V : la mesure est fausse ! C'est pour cela qu'on adapte toujours le signal (diviseur de tension) avant le CAN.");
  card(s, 0.5, 1.0, 9.0, 0.7);
  txt(s, "q = 5,12 V / 256 = 20 mV  (valeur choisie exprès pour faciliter le calcul)", { x: 0.7, y: 1.05, w: 8.6, h: 0.6, fontSize: 15, bold: true, align: "center", valign: "middle" });
  const Q = [["a)", "Uₑ = 1,30 V", "N = ?   en binaire ?"], ["b)", "Uₑ = 3,47 V", "N = ?   en binaire ?   contrôle ?"], ["c)", "Uₑ = 6,00 V", "Que se passe-t-il ? Que lit le microcontrôleur ?"]];
  Q.forEach((q, i) => {
    const y = 1.95 + i * 0.95;
    frame(s, 0.5, y, 9.0, 0.8);
    txt(s, q[0], { x: 0.7, y: y + 0.1, w: 0.5, h: 0.6, fontSize: 18, bold: true, valign: "middle" });
    txt(s, q[1], { x: 1.25, y: y + 0.1, w: 2.4, h: 0.6, fontSize: 18, bold: true, fontFace: MONO, valign: "middle" });
    txt(s, q[2], { x: 3.8, y: y + 0.1, w: 5.5, h: 0.6, fontSize: 15, valign: "middle" });
  });
  life(s, 0.5, 4.78, 9.0, 0.8, "Une batterie de voiture (12 V) ne se branche jamais directement sur un CAN 5 V : on la divise d'abord avec deux résistances.", 12);
}

// ============================== 10. APPROXIMATIONS SUCCESSIVES
{
  const s = slide("Comment le CAN trouve le code : approximations successives",
    "Analogie : le jeu du nombre mystère entre 0 et 15. La meilleure stratégie est de couper l'intervalle en deux à chaque question : « est-ce plus que 8 ? ». En 4 questions, on trouve n'importe quel nombre de 4 bits. Le CAN fait exactement cela : un CNA interne propose une tension d'essai, un comparateur dit « plus » ou « moins », et l'on décide bit par bit, du MSB au LSB. Exemple : 4 bits, U_ref = 5 V, q = 0,3125 V, Uₑ = 3,3 V. Essai 1000b = 2,5 V ≤ 3,3 V → b3 = 1. Essai 1100b = 3,75 V > 3,3 V → b2 = 0. Essai 1010b = 3,125 V ≤ 3,3 V → b1 = 1. Essai 1011b = 3,4375 V > 3,3 V → b0 = 0. Résultat 1010b = 10 → 3,125 V. Contrôle : 3,3 / 0,3125 = 10,56 → 10 ✓. C'est le type de CAN des microcontrôleurs (SAR = Successive Approximation Register).");
  s.addImage({ path: "fig_sar.png", x: 0.45, y: 0.95, w: 5.4, h: 2.84 });
  card(s, 6.05, 1.0, 3.45, 2.75);
  txt(s, "Le jeu du nombre mystère", { x: 6.2, y: 1.08, w: 3.2, h: 0.35, fontSize: 14, bold: true });
  txt(s, "« Plus grand que 8 ? » → oui\n« Plus grand que 12 ? » → non\n« Plus grand que 10 ? » → oui\n« Plus grand que 11 ? » → non\n→ c'est 10 !", { x: 6.2, y: 1.48, w: 3.2, h: 2.2, fontSize: 12 });
  frame(s, 0.5, 4.0, 9.0, 1.55);
  txt(s, "4 bits, U_ref = 5 V, q = 0,3125 V, Uₑ = 3,3 V", { x: 0.7, y: 4.07, w: 8.6, h: 0.32, fontSize: 13, bold: true });
  txt(s, [
    { text: "On met le MSB à 1 et on compare la tension d'essai à la tension d'entrée : plus petite ou égale → on garde 1, plus grande → on remet 0.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "On recommence avec le bit suivant, jusqu'au LSB : n bits = n comparaisons.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "Résultat : 1010b = 10 → 10 × 0,3125 V = 3,125 V.", options: { bullet: { type: "number" } } },
  ], { x: 0.7, y: 4.42, w: 8.6, h: 1.08, fontSize: 12, paraSpaceAfter: 2 });
}

// ============================== 11. TYPES DE CAN
{
  const s = slide("Quel CAN pour quel usage ?",
    "Pas besoin de connaître le fonctionnement interne détaillé en première année : il faut savoir que les familles existent et pourquoi on choisit l'une ou l'autre (compromis vitesse / précision / prix). On les retrouvera en lisant des fiches techniques et en utilisant les appareils du laboratoire : l'oscilloscope numérique du labo utilise un CAN flash ou pipeline de 8 bits à plusieurs centaines de mégaéchantillons par seconde ; le multimètre de table, un CAN double rampe ou sigma-delta lent mais très précis.");
  s.addTable([
    [cell("Type", H), cell("Principe (en une phrase)", H), cell("Vitesse", H), cell("Précision", H), cell("Où on le trouve", H)],
    [cell("Approximations successives (SAR)", { bold: true, align: "left", fontSize: 12 }), cell("Devine bit par bit, du MSB au LSB", { align: "left", fontSize: 12 }), cell("moyenne", { fontSize: 12 }), cell("8 à 16 bits", { fontSize: 12 }), cell("Microcontrôleurs (Arduino, STM32), capteurs", { align: "left", fontSize: 12 })],
    [cell("Flash", { bold: true, align: "left", fontSize: 12 }), cell("Un comparateur par niveau : tout en même temps", { align: "left", fontSize: 12 }), cell("très rapide", { fontSize: 12 }), cell("6 à 8 bits", { fontSize: 12 }), cell("Oscilloscope numérique, radar, vidéo", { align: "left", fontSize: 12 })],
    [cell("Double rampe", { bold: true, align: "left", fontSize: 12 }), cell("Mesure un temps de charge d'un condensateur", { align: "left", fontSize: 12 }), cell("lente", { fontSize: 12 }), cell("très bonne", { fontSize: 12 }), cell("Multimètre numérique", { align: "left", fontSize: 12 })],
    [cell("Sigma-delta (ΣΔ)", { bold: true, align: "left", fontSize: 12 }), cell("Mesure très vite sur 1 bit, puis fait la moyenne", { align: "left", fontSize: 12 }), cell("lente à moyenne", { fontSize: 12 }), cell("16 à 24 bits", { fontSize: 12 }), cell("Carte son, balance, multimètre de table", { align: "left", fontSize: 12 })],
  ], { x: 0.5, y: 1.0, w: 9.0, colW: [2.0, 2.6, 1.1, 1.1, 2.2], rowH: [0.4, 0.7, 0.7, 0.7, 0.7], border: BORDER });
  life(s, 0.5, 4.45, 9.0, 1.1, "Choisir un CAN, c'est toujours un compromis : rapide OU précis OU bon marché. L'oscilloscope du labo est rapide mais n'a que 8 bits ; le multimètre est lent mais affiche 4 à 6 chiffres.", 12);
}

// ============================== 12. ÉCHANTILLONNAGE / SHANNON
{
  const s = slide("Échantillonner assez vite : la règle de Shannon",
    "fₑ = nombre de mesures par seconde. Règle de Shannon (théorème de Nyquist-Shannon) : il faut fₑ > 2 · f_max, f_max étant la plus haute fréquence contenue dans le signal. Sinon on reconstitue un faux signal plus lent : c'est le repliement (aliasing). Exemple bien connu : dans un film, les roues d'une voiture semblent tourner à l'envers, parce que la caméra (25 images par seconde) échantillonne trop lentement la rotation des rayons. Exemples : CD audio fₑ = 44,1 kHz > 2 × 20 kHz (limite de l'oreille) ; téléphone fₑ = 8 kHz > 2 × 3,4 kHz (voix) ; température d'une pièce : 1 mesure par seconde suffit largement.");
  s.addImage({ path: "fig_shannon.png", x: 0.45, y: 0.95, w: 9.05, h: 2.42 });
  card(s, 0.5, 3.6, 3.6, 1.95);
  txt(s, [{ text: "f", options: {} }, sub("e"), { text: " > 2 · f", options: {} }, sub("max")], { x: 0.7, y: 3.72, w: 3.2, h: 0.6, fontSize: 26, bold: true, align: "center", color: BLUE });
  txt(s, "Mesurer au moins 2 fois par période de la plus haute fréquence du signal. En pratique, on prend 5 à 10 fois plus.", { x: 0.7, y: 4.4, w: 3.25, h: 1.1, fontSize: 12 });
  s.addTable([
    [cell("Application", H), cell("f_max", H), cell("fₑ utilisée", H)],
    [cell("Téléphone (voix)", { align: "left", fontSize: 12 }), cell("3,4 kHz", { fontSize: 12 }), cell("8 kHz", { fontSize: 12 })],
    [cell("CD audio", { align: "left", fontSize: 12 }), cell("20 kHz", { fontSize: 12 }), cell("44,1 kHz", { fontSize: 12 })],
    [cell("Thermostat", { align: "left", fontSize: 12 }), cell("≈ 0,01 Hz", { fontSize: 12 }), cell("1 Hz", { fontSize: 12 })],
  ], { x: 4.35, y: 3.6, w: 5.15, colW: [2.15, 1.4, 1.6], rowH: 0.45, border: BORDER });
}

// ============================== 13. LE CNA
{
  const s = slide("Le CNA : du code à la tension",
    "Le CNA fait l'opération inverse : Uₛ = N · q, avec q = U_ref / 2ⁿ. Exemple affiché : CNA 4 bits, U_ref = 3,2 V → q = 0,2 V. Si un compteur fait défiler les codes 0000 → 1111, la sortie monte en escalier de 0 V à 3,0 V (= U_ref − q, jamais U_ref !). Après le CNA, un filtre passe-bas lisse les marches. C'est ainsi qu'un générateur de fonctions du laboratoire fabrique un sinus ou une rampe, et qu'un téléphone pilote ses écouteurs.");
  s.addImage({ path: "fig_cna.png", x: 0.45, y: 0.95, w: 5.6, h: 2.88 });
  card(s, 6.25, 1.0, 3.25, 1.6);
  txt(s, [{ text: "U", options: {} }, sub("s"), { text: " = N · q", options: {} }], { x: 6.4, y: 1.1, w: 2.95, h: 0.6, fontSize: 24, bold: true, align: "center", color: BLUE });
  txt(s, [{ text: "q = U", options: {} }, sub("ref"), { text: " / 2", options: {} }, { text: "n", options: { superscript: true } }], { x: 6.4, y: 1.75, w: 2.95, h: 0.45, fontSize: 16, bold: true, align: "center" });
  txt(s, "Tension max = U_ref − q", { x: 6.4, y: 2.2, w: 2.95, h: 0.35, fontSize: 12, italic: true, align: "center" });
  frame(s, 6.25, 2.75, 3.25, 1.1);
  txt(s, "Exemple : 1010b = 10 → 10 × 0,2 V = 2,0 V", { x: 6.4, y: 2.82, w: 2.95, h: 0.95, fontSize: 13, bold: true, valign: "middle" });
  life(s, 0.5, 4.05, 9.0, 1.5, "Écouteurs et haut-parleurs d'un téléphone · générateur de fonctions du labo (sinus, triangle, rampe) · consigne de vitesse envoyée à un variateur de moteur (0-10 V en automatisme industriel) · luminosité d'un éclairage LED réglable.", 12);
}

// ============================== 14. POIDS DES BITS DANS UN CNA
{
  const s = slide("Dans un CNA, chaque bit apporte son poids",
    "Lien avec la numération : le bit de poids fort apporte U_ref / 2, le suivant U_ref / 4, puis U_ref / 8… et le LSB apporte q. La tension de sortie est la somme des poids des bits à 1. Exemple : CNA 4 bits, U_ref = 3,2 V : b3 = 1,6 V, b2 = 0,8 V, b1 = 0,4 V, b0 = 0,2 V. 1010b → 1,6 V + 0,4 V = 2,0 V (même résultat que N · q = 10 × 0,2 V). 1111b → 1,6 + 0,8 + 0,4 + 0,2 = 3,0 V. Dans le circuit réel, ce sont des résistances (réseau R-2R) qui produisent ces poids : on le verra plus tard avec l'amplificateur opérationnel.");
  const HB = Object.assign({}, H, { fontSize: 13 });
  s.addTable([
    [cell("Bit", HB), cell("b3 (MSB)", HB), cell("b2", HB), cell("b1", HB), cell("b0 (LSB)", HB)],
    [cell("Poids", { bold: true, align: "left" }), cell("U_ref / 2"), cell("U_ref / 4"), cell("U_ref / 8"), cell("U_ref / 16 = q")],
    [cell("U_ref = 3,2 V", { bold: true, align: "left" }), cell("1,6 V", { bold: true }), cell("0,8 V", { bold: true }), cell("0,4 V", { bold: true }), cell("0,2 V", { bold: true })],
  ], { x: 0.5, y: 1.0, w: 9.0, colW: [2.0, 1.75, 1.75, 1.75, 1.75], rowH: 0.48, border: BORDER });
  const M = { fontFace: MONO, fontSize: 18, bold: true };
  s.addTable([
    [cell("Code", HB), cell("Bits à 1", HB), cell("Calcul", HB), cell("Uₛ", HB)],
    [cell("1010b", M), cell("b3, b1", {}), cell("1,6 V + 0,4 V", {}), cell("2,0 V", { bold: true, fill: { color: VLG } })],
    [cell("0101b", M), cell("b2, b0", {}), cell("0,8 V + 0,2 V", {}), cell("1,0 V", { bold: true, fill: { color: VLG } })],
    [cell("1111b", M), cell("tous", {}), cell("1,6 + 0,8 + 0,4 + 0,2", {}), cell("3,0 V", { bold: true, fill: { color: VLG } })],
  ], { x: 0.5, y: 2.65, w: 5.6, colW: [1.3, 1.2, 2.1, 1.0], rowH: 0.5, border: BORDER });
  card(s, 6.35, 2.65, 3.15, 2.0);
  txt(s, "Même logique que la conversion binaire → décimal : on additionne les poids des bits à 1. Seule l'unité change (des volts au lieu de 1, 2, 4, 8).", { x: 6.5, y: 2.75, w: 2.85, h: 1.8, fontSize: 12.5, valign: "middle" });
  txt(s, "Contrôle : N · q = 10 × 0,2 V = 2,0 V ✓", { x: 0.5, y: 4.95, w: 9, h: 0.45, fontSize: 14, italic: true });
}

// ============================== 15. SYMBOLES CEI
{
  const s = slide("Les symboles CEI des convertisseurs",
    "Norme CEI 60617-13 (opérateurs analogiques) : un convertisseur est un rectangle portant un symbole distinctif. « ∩ » désigne une grandeur analogique, « # » une grandeur numérique. CAN = « ∩/# » (de l'analogique vers le numérique), CNA = « #/∩ ». Une liaison numérique de n bits (bus) est dessinée en trait épais barré d'un petit trait oblique avec le nombre de bits. On lit le symbole de gauche à droite : entrée à gauche, sortie à droite. Ces symboles apparaissent dans les schémas-blocs des fiches techniques et des dossiers de fabrication.");
  s.addImage({ path: "fig_symboles.png", x: 0.8, y: 0.95, w: 6.6, h: 1.98 });
  const R = [["∩", "grandeur analogique (tension continue)"], ["#", "grandeur numérique (nombre binaire)"], ["∩/#", "CAN : analogique → numérique"], ["#/∩", "CNA : numérique → analogique"], ["╱ n", "bus de n lignes (n bits) sur un trait épais"]];
  R.forEach((r, i) => {
    const y = 3.15 + i * 0.47;
    frame(s, 0.5, y, 9.0, 0.4);
    txt(s, r[0], { x: 0.65, y: y + 0.02, w: 1.2, h: 0.36, fontSize: 17, bold: true, align: "center", valign: "middle" });
    txt(s, r[1], { x: 2.0, y: y + 0.02, w: 7.3, h: 0.36, fontSize: 13, valign: "middle" });
  });
}

// ============================== 16. MULTIMÈTRE
{
  const s = slide("En mesure : ton multimètre numérique est un CAN",
    "Lien direct avec Test et Mesure : un multimètre « 3½ digits » affiche de 0000 à 1999, soit 2000 points. Sa résolution (le plus petit pas affiché) dépend du calibre : calibre 2 V → 2 V / 2000 = 1 mV ; 20 V → 10 mV ; 200 V → 0,1 V. Pour mesurer une pile de 1,5 V, on choisit le calibre 2 V (affichage 1,500 → 4 chiffres utiles) plutôt que 20 V (01,50 → 3 chiffres). Si la tension dépasse le calibre, l'appareil affiche « 1 » ou « OL » (Over Load) : c'est la saturation du CAN. Attention : la résolution n'est pas la précision ; la précision est donnée dans la notice (± % de la lecture ± digits).");
  card(s, 0.5, 1.0, 4.2, 1.75);
  txt(s, "3½ digits = 2000 points", { x: 0.7, y: 1.08, w: 3.85, h: 0.42, fontSize: 18, bold: true });
  txt(s, "affichage de 0000 à 1999 ; le premier chiffre ne peut valoir que 0 ou 1 (le « ½ digit »)", { x: 0.7, y: 1.55, w: 3.85, h: 1.1, fontSize: 12.5 });
  s.addTable([
    [cell("Calibre", H), cell("Résolution", H), cell("Pile 1,5 V affichée", H)],
    [cell("200 mV"), cell("0,1 mV"), cell("1   (OL)", { color: RED, bold: true })],
    [cell("2 V"), cell("1 mV"), cell("1,500", { fontFace: MONO, bold: true, fill: { color: VLG } })],
    [cell("20 V"), cell("10 mV"), cell("01,50", { fontFace: MONO, bold: true })],
    [cell("200 V"), cell("0,1 V"), cell("001,5", { fontFace: MONO, bold: true })],
  ], { x: 5.0, y: 1.0, w: 4.5, colW: [1.2, 1.4, 1.9], rowH: 0.4, border: BORDER });
  frame(s, 0.5, 3.0, 4.2, 1.3);
  txt(s, "Résolution = calibre / nombre de points", { x: 0.7, y: 3.08, w: 3.85, h: 0.45, fontSize: 13, bold: true, color: BLUE });
  txt(s, "Choisis le plus petit calibre qui ne sature pas : c'est lui qui donne le plus de chiffres utiles.", { x: 0.7, y: 3.55, w: 3.85, h: 0.7, fontSize: 12.5 });
  life(s, 0.5, 4.5, 9.0, 1.05, "Au labo et en entreprise, tu notes toujours le calibre utilisé dans ton rapport de mesure : sans lui, on ne connaît pas la résolution de ta valeur. Résolution ≠ précision : la précision est dans la notice (± % de la lecture ± digits).", 12);
}

// ============================== 17. APPLICATION COMPLÈTE LM35
{
  const s = slide("Application : un thermomètre avec un LM35 et un Arduino",
    "Situation réelle et complète. Le LM35 est un capteur de température courant qui fournit 10 mV par °C. À 25,0 °C il donne 0,250 V. CAN 10 bits, U_ref = 5 V : q = 4,883 mV. N = 0,250 / 0,004883 = 51,2 → 51. Le programme recalcule : 51 × 4,883 mV = 249,0 mV → 24,9 °C. Résolution en température : q / 10 mV = 0,49 °C : on ne peut pas afficher mieux qu'environ 0,5 °C. Amélioration : utiliser la référence interne de 1,1 V → q = 1,074 mV → 0,11 °C, mais on ne peut plus mesurer au-delà de 110 °C. Encore le compromis plage / résolution.");
  s.addImage({ path: "fig_lm35.png", x: 0.45, y: 0.95, w: 9.05, h: 2.47 });
  s.addTable([
    [cell("Étape", H), cell("Calcul", H), cell("Résultat", H)],
    [cell("Tension du capteur", { align: "left", fontSize: 12 }), cell("25,0 °C × 10 mV/°C", { fontSize: 12 }), cell("0,250 V", { bold: true, fontSize: 12 })],
    [cell("Code N", { align: "left", fontSize: 12 }), cell("0,250 V / 4,883 mV = 51,2", { fontSize: 12 }), cell("51 = 00 0011 0011b", { bold: true, fontSize: 10.5 })],
    [cell("Température affichée", { align: "left", fontSize: 12 }), cell("51 × 4,883 mV / 10 mV/°C", { fontSize: 12 }), cell("24,9 °C", { bold: true, fontSize: 12 })],
    [cell("Résolution", { align: "left", fontSize: 12 }), cell("4,883 mV / 10 mV/°C", { fontSize: 12 }), cell("≈ 0,5 °C", { bold: true, fontSize: 12, fill: { color: VLG } })],
  ], { x: 0.5, y: 3.6, w: 6.0, colW: [1.75, 2.25, 2.0], rowH: 0.38, border: BORDER });
  card(s, 6.75, 3.6, 2.75, 1.95);
  txt(s, "Et avec U_ref = 1,1 V ?", { x: 6.9, y: 3.68, w: 2.5, h: 0.35, fontSize: 13, bold: true });
  txt(s, "q ≈ 1,07 mV → résolution ≈ 0,1 °C… mais mesure limitée à 110 °C. Toujours un compromis plage / résolution.", { x: 6.9, y: 4.05, w: 2.5, h: 1.45, fontSize: 11.5 });
}

// ============================== 18. PIÈGES
{
  const s = slide("Les 6 pièges classiques",
    "Faire chercher en binôme, pour chaque piège, un exemple d'erreur et sa correction (auto-explication). Ce sont les erreurs les plus fréquentes aux tests.");
  const P = [
    ["Diviser par 2ⁿ − 1", "q = U_ref / 2ⁿ (256, 1024…), pas / 255 ou / 1023."],
    ["Arrondir N", "Le CAN tronque : 409,6 → 409, pas 410."],
    ["Oublier les unités", "mV et V mélangés : écrire chaque préfixe."],
    ["Croire que Uₛ max = U_ref", "La sortie max vaut U_ref − q, le code max 2ⁿ − 1."],
    ["Échantillonner trop lentement", "fₑ > 2 · f_max, sinon faux signal (repliement)."],
    ["Résolution = précision", "La résolution est le pas ; la précision est dans la notice."],
  ];
  P.forEach((p, i) => {
    const x = 0.5 + (i % 2) * 4.55, y = 1.0 + Math.floor(i / 2) * 1.55;
    card(s, x, y, 4.35, 1.35);
    badge(s, x + 0.18, y + 0.2, String(i + 1));
    txt(s, p[0], { x: x + 0.78, y: y + 0.18, w: 3.45, h: 0.45, fontSize: 15, bold: true, valign: "middle" });
    txt(s, p[1], { x: x + 0.78, y: y + 0.65, w: 3.45, h: 0.6, fontSize: 13 });
  });
}

// ============================== 19. TICKET DE SORTIE
{
  const s = slide("Ticket de sortie : 4 questions, 5 minutes",
    "Évaluation formative : une question par grand objectif. Ramasser les tickets pour adapter la prochaine leçon.\nRéponses : 1) q = 5 V / 256 = 19,5 mV. 2) q = 8 V / 16 = 0,5 V ; 3,7 / 0,5 = 7,4 → 7 = 0111b. 3) q = 2,56 V / 256 = 10 mV ; 1000 0000b = 128 → 1,28 V. 4) fₑ > 2 × 4 kHz = 8 kHz.\nRetour au défi de l'échauffement : le micro donne une tension, un CAN 16 bits la mesure 44 100 fois par seconde → des nombres binaires en mémoire.");
  const Q = [["1", "CAN 8 bits, U_ref = 5 V : q = ?"], ["2", "CAN 4 bits, U_ref = 8 V, Uₑ = 3,7 V : code ?"], ["3", "CNA 8 bits, U_ref = 2,56 V : 1000 0000b donne ?"], ["4", "Signal jusqu'à 4 kHz : fₑ minimale ?"]];
  Q.forEach((q, i) => {
    const y = 1.0 + i * 0.72;
    frame(s, 0.5, y, 5.6, 0.6);
    badge(s, 0.62, y + 0.09, q[0]);
    txt(s, q[1], { x: 1.2, y: y + 0.08, w: 4.8, h: 0.45, fontSize: 14, bold: true, valign: "middle" });
  });
  card(s, 6.4, 1.0, 3.1, 2.75);
  txt(s, "Auto-évaluation", { x: 6.6, y: 1.1, w: 2.7, h: 0.35, fontSize: 14, bold: true });
  txt(s, "Pour chaque objectif, je note :\n✓ je sais faire seul·e\n~ je sais avec la fiche\n✗ je dois revoir", { x: 6.6, y: 1.5, w: 2.75, h: 2.1, fontSize: 13 });
  frame(s, 0.5, 4.05, 9.0, 1.5);
  txt(s, "Pour s'entraîner", { x: 0.7, y: 4.12, w: 8.6, h: 0.35, fontSize: 14, bold: true });
  s.addText([
    { text: "Feuille d'exercices « Conversion A/N et N/A (CAN / CNA) »", options: { breakLine: true } },
    link("Nextec Media – exercices complémentaires", NEXTEC_EX_URL, { breakLine: true }),
    link("Floyd – chapitre conversion A/N et N/A, problèmes de fin de chapitre", FLOYD_URL),
  ], { x: 0.7, y: 4.5, w: 8.6, h: 1.0, fontFace: F, fontSize: 12, color: K, margin: 0, valign: "top", paraSpaceAfter: 3, isTextBox: true });
}

pres.writeFile({ fileName: "out/Conversion AN et NA (CAN-CNA) – présentation.pptx" }).then(() => console.log("deck ok"));
