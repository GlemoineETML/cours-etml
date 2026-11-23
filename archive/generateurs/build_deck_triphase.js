// Présentation « Le courant alternatif triphasé » · 10 diapositives · charte ETML (marine 242852, bleu 297FD5), Arial, 16:10
// Source : Électrotechnique, fascicule 03, chapitre 11 (p. 11.1 à 11.38). Classe XLO4, 2026-2027.
const pptxgen = require("pptxgenjs");
const RATIO = require("./ratios.json");
const pres = new pptxgen();
pres.defineLayout({ name: "ETML1610", width: 10, height: 6.25 });
pres.layout = "ETML1610";
pres.author = "Gaël Lemoine";
pres.company = "ETML – Section électronique";
pres.title = "Le courant alternatif triphasé";
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };

const NAVY = "242852", BLUE = "297FD5", LBLUE = "ACCBF9", TINT = "E8EFFB";
const K = NAVY, GR = "5A6478", RED = "EE0000";
const F = "Arial";
const MATIERE = "Électrotechnique – triphasé";
const TOPIC = MATIERE + " · Courant alternatif triphasé";
const CLASSE = "XLO4", ANNEE = "2026-2027", CHAMP = "Programme de la dernière ligne droite";
const DATE_US = "11/10/2026";
const FASC_URL = "https://eduvaud.sharepoint.com/:b:/r/sites/msteams_76c9d9/Documents%20partages/Documentation/Electrotechnique%20ELEC/FET%20Electrotechnique%203/ElectrotechniqueFascicule03_V2014_opt.pdf?d=w58dfaaa0153748aa92aceeae8e494206&csf=1&web=1&e=AtwPZK";
const LOGO_BAND = "logo_white_v.png";

const BAND = () => [
  { rect: { x: 9.25, y: 0, w: 0.75, h: 6.25, fill: { color: NAVY } } },
  { image: { path: LOGO_BAND, x: 9.39, y: 0.35, w: 0.47, h: 1.95 } },
  { text: { text: "Section électronique", options: { x: 8.125, y: 3.575, w: 3.0, h: 0.75, rotate: 270, fontFace: F, fontSize: 14, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0 } } },
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
    { rect: { x: 9.37, y: 5.62, w: 0.5, h: 0.5, fill: { color: LBLUE } } },
  ]),
  slideNumber: { x: 9.37, y: 5.62, w: 0.5, h: 0.5, fontFace: F, fontSize: 12, bold: true, color: NAVY, align: "center", valign: "middle" },
});

// zone utile x ≤ 8,9" (bandeau) : grille 0,5 → 9,5" comprimée horizontalement
function squeeze(s, x0, x1, nx1) {
  const k = (nx1 - x0) / (x1 - x0);
  const fx = (o, img) => {
    if (!o) return o;
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
const RE = /_\{([^}]*)\}|\^\{([^}]*)\}/g;
function R(str, base) {
  base = base || {};
  if (typeof str !== "string" || !str.match(RE)) return null;
  const out = []; let pos = 0; RE.lastIndex = 0; let m;
  while ((m = RE.exec(str))) {
    if (m.index > pos) out.push({ text: str.slice(pos, m.index), options: Object.assign({}, base) });
    out.push({ text: m[1] !== undefined ? m[1] : m[2], options: Object.assign({}, base, m[1] !== undefined ? { subscript: true } : { superscript: true }) });
    pos = m.index + m[0].length;
  }
  if (pos < str.length) out.push({ text: str.slice(pos), options: Object.assign({}, base) });
  out.forEach((r, i) => {
    if (i < out.length - 1) delete r.options.breakLine;
    if (i > 0) { delete r.options.bullet; delete r.options.indentLevel; }
  });
  return out;
}
function lines(str, base) {            // texte multiligne avec indices : un paragraphe par ligne
  const L = str.split("\n"), out = [];
  L.forEach((l, i) => {
    const runs = R(l, base) || [{ text: l, options: Object.assign({}, base || {}) }];
    if (i < L.length - 1) runs[runs.length - 1].options.breakLine = true;
    out.push(...runs);
  });
  return out;
}
function expand(t) {
  if (typeof t === "string") return (t.includes("\n") && t.match(RE)) ? lines(t) : (R(t) || t);
  if (Array.isArray(t)) return [].concat(...t.map(r => (r && typeof r.text === "string" && R(r.text, r.options)) || [r]));
  return t;
}
function slide(title, notes) {
  const s = pres.addSlide({ masterName: "CONTENU" });
  s.addText(expand(title), { x: 0.5, y: 0.25, w: 9.0, h: 0.55, fontFace: F, fontSize: 23, bold: true, color: NAVY, margin: 0, valign: "middle", fit: "shrink" });
  squeeze(s, 0.5, 9.5, 8.9);
  if (notes) s.addNotes(notes);
  return s;
}
function txt(s, text, o) { s.addText(expand(text), Object.assign({ fontFace: F, fontSize: 13, color: K, margin: 0, valign: "top" }, o)); }
function card(s, x, y, w, h, fill) { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill || TINT }, line: { color: fill || TINT, width: 0 } }); }
function frame(s, x, y, w, h) { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.25 } }); }
function badge(s, x, y, label, d) {
  d = d || 0.4;
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: K }, line: { color: K } });
  s.addText(label, { x, y, w: d, h: d, fontFace: F, fontSize: 12, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0 });
}
function img(s, file, x, y, w, maxH) {
  let h = w * RATIO[file];
  if (maxH && h > maxH) { w = maxH / RATIO[file]; h = maxH; }
  s.addImage({ path: file, x, y, w, h });
  return h;
}
function bullets(s, items, o, numbered) {
  const runs = items.map((t, i) => ({ text: t, options: { bullet: numbered ? { type: "number" } : { indent: 12 }, breakLine: i < items.length - 1 } }));
  s.addText(expand(runs), Object.assign({ fontFace: F, fontSize: 12, color: K, margin: 0, valign: "top", paraSpaceAfter: 3 }, o));
}
function life(s, x, y, w, h, lines, fs) {
  card(s, x, y, w, h);
  const runs = [{ text: "Dans la vraie vie", options: { bold: true, color: BLUE, breakLine: true } }];
  lines.forEach((l, i) => runs.push({ text: l, options: { color: K, bullet: { indent: 12 }, breakLine: i < lines.length - 1 } }));
  s.addText(expand(runs), { x: x + 0.15, y: y + 0.08, w: w - 0.3, h: h - 0.16, fontFace: F, fontSize: fs || 11, margin: 0, valign: "top", paraSpaceAfter: 2 });
}
function boxTitle(s, x, y, w, h, title, lines, fs, isFrame) {
  (isFrame ? frame : card)(s, x, y, w, h);
  txt(s, title, { x: x + 0.15, y: y + 0.07, w: w - 0.3, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
  bullets(s, lines, { x: x + 0.15, y: y + 0.4, w: w - 0.3, h: h - 0.47, fontSize: fs || 11 });
}
const cell = (t, o) => ({ text: expand(String(t)), options: Object.assign({ align: "center", valign: "middle", fontFace: F, fontSize: 12, color: K }, o || {}) });
const H = { fill: { color: LBLUE }, bold: true, fontSize: 11.5, color: NAVY };
const BORDER = { type: "solid", color: K, pt: 0.75 };

// ============================== 1. TITRE · OBJECTIFS · QUESTION DE DÉPART
{
  const s = pres.addSlide({ masterName: "TITRE" });
  squeeze(s, 0.6, 9.5, 8.9);
  txt(s, "ÉLECTROTECHNIQUE – TRIPHASÉ", { x: 0.6, y: 0.4, w: 5.4, h: 0.3, fontSize: 12, bold: true, color: BLUE, charSpacing: 1 });
  txt(s, "Le courant alternatif\ntriphasé", { x: 0.6, y: 0.7, w: 5.4, h: 1.05, fontSize: 28, bold: true, color: NAVY, valign: "middle" });
  txt(s, "Tensions, couplages étoile et triangle, puissances, neutre, compensation", { x: 0.6, y: 1.78, w: 5.4, h: 0.5, fontSize: 12.5, color: GR });
  txt(s, "À la fin de la leçon, je suis capable de…", { x: 0.6, y: 2.32, w: 5.4, h: 0.3, fontSize: 13.5, bold: true });
  ["passer de U à U_{ph} et inversement ;", "choisir Y ou Δ d'après la plaque signalétique ;", "calculer I, P, Q et S d'un récepteur équilibré ;",
   "expliquer le rôle du neutre et le danger de sa coupure ;", "dimensionner une compensation et une chute de tension."].forEach((t, i) => {
    const y = 2.68 + i * 0.37;
    badge(s, 0.6, y + 0.02, String(i + 1), 0.3);
    txt(s, t, { x: 1.02, y, w: 5.0, h: 0.34, fontSize: 12.5, valign: "middle" });
  });
  img(s, "fig_tensions.png", 6.75, 0.35, 2.05);
  frame(s, 6.15, 2.55, 3.35, 1.95);
  txt(s, "Question de départ", { x: 6.3, y: 2.62, w: 3.1, h: 0.3, fontSize: 13, bold: true, color: BLUE });
  txt(s, "Une borne de recharge de 11 kW tire 16 A. Une prise domestique de 16 A ne donne que 3,7 kW. D'où viennent les 7 kW de plus ?", { x: 6.3, y: 2.94, w: 3.1, h: 1.05, fontSize: 11.5 });
  txt(s, "Écris ton hypothèse. Réponse à la diapositive 6.", { x: 6.3, y: 4.05, w: 3.1, h: 0.38, fontSize: 10, italic: true, color: GR });
  card(s, 0.6, 4.65, 8.9, 0.83);
  s.addText(expand([
    { text: `Classe ${CLASSE} · ${ANNEE} · ${CHAMP} · éditeur : Gaël Lemoine · ${DATE_US}`, options: { bold: true, breakLine: true } },
    { text: "Référence : ", options: { color: K } },
    { text: "Électrotechnique, fascicule 03, chapitre 11 « Courant alternatif triphasé »", options: { hyperlink: { url: FASC_URL } } },
  ]), { x: 0.8, y: 4.7, w: 8.5, h: 0.73, fontFace: F, fontSize: 11.5, color: NAVY, margin: 0, valign: "middle", paraSpaceAfter: 3 });
  s.addNotes("Durée : 2 × 45 min de théorie (diapositives 1 à 10), puis 2 × 45 min d'exercices (fiche N°1 à N°9). N°10 est l'exercice de révision à donner une semaine plus tard, sans la fiche.\n" +
    "Public : 4e année CFC, dernière ligne droite avant la procédure de qualification. La plupart des notions ont déjà été vues en alternatif monophasé (cos φ, P, Q, S) ; on les étend au triphasé.\n" +
    "Prérequis : alternatif monophasé (valeur efficace, déphasage, cos φ, triangle des puissances), loi d'Ohm, lois de Kirchhoff, vecteurs.\n" +
    "Question de départ : chaque apprenti·e écrit une hypothèse, sans correction immédiate. Prédire avant d'apprendre aide à retenir. Réponse à la diapositive 6 : la borne utilise trois conducteurs polaires sous 400 V entre phases, P = √3 · 400 V · 16 A = 11 kW, contre 230 V · 16 A = 3,7 kW en monophasé.");
}

// ============================== 2. TROIS TENSIONS DÉCALÉES DE 120°
{
  const s = slide("Le triphasé : trois tensions décalées de 120°",
    "Définition du fascicule : trois courants (ou tensions) de même valeur efficace, décalés d'un tiers de période, donc de 120°.\n" +
    "Origine : l'alternateur possède trois enroulements statoriques U1-U2, V1-V2, W1-W2 disposés à 120°. Le rotor (aimant ou électroaimant) induit dans chacun la même tension, avec un tiers de période de retard.\n" +
    "Point clé à faire constater sur le graphique : à tout instant, la somme des trois valeurs instantanées vaut zéro (par exemple au sommet de u_L1 : 1 + (−0,5) + (−0,5) = 0). C'est ce qui permet de supprimer les conducteurs de retour quand la charge est équilibrée.\n" +
    "Faire relier chaque avantage à un objet que les apprentis connaissent : ligne haute tension (3 câbles), moteur de pompe ou de compresseur, prise CEE rouge 5 pôles de l'atelier, cuisinière.");
  img(s, "fig_systeme.png", 0.5, 0.95, 9.0);
  boxTitle(s, 0.5, 4.15, 4.4, 1.45, "Pourquoi trois phases ?", [
    "Plus de puissance transportée pour la même masse de cuivre.",
    "Champ magnétique tournant : le moteur démarre seul.",
    "Deux tensions disponibles : 230 V et 400 V.",
  ], 11);
  life(s, 5.1, 4.15, 4.4, 1.45, [
    "Alternateurs des centrales, lignes à 3 câbles.",
    "Prise CEE rouge 5 pôles, cuisinière, pompe à chaleur.",
    "Onduleur photovoltaïque et borne de recharge 11 / 22 kW.",
  ]);
}

// ============================== 3. U ET U_ph
{
  const s = slide("Tension de phase U_{ph} et tension réseau U",
    "Tension de phase U_ph : mesurée entre un conducteur polaire et le neutre (L1-N, L2-N, L3-N). Tension réseau U : mesurée entre deux conducteurs polaires (L1-L2, L2-L3, L3-L1).\n" +
    "Démonstration rapide au tableau : dans le triangle isocèle L1-N-L2, la hauteur coupe U en deux ; U/2 = U_ph · cos 30° → U = 2 · U_ph · √3/2 = √3 · U_ph.\n" +
    "Faire mesurer au laboratoire, sur le tableau d'essai, avec un multimètre de catégorie CAT III au minimum : L1-N ≈ 230 V, L1-L2 ≈ 400 V.\n" +
    "Dénomination : « 3 × 400 V » = trois conducteurs polaires sans neutre. « 3 × 400/230 V » = trois conducteurs polaires et un neutre. La plus grande des tensions indiquées est toujours la tension réseau.\n" +
    "Couleurs selon CEI 60445 : L1 brun, L2 noir, L3 gris, N bleu clair, PE vert-jaune.");
  img(s, "fig_tensions.png", 0.6, 0.95, 3.6, 4.6);
  card(s, 4.5, 0.95, 5.0, 1.3);
  txt(s, "U = √3 · U_{ph}", { x: 4.6, y: 1.0, w: 4.8, h: 0.6, fontSize: 26, bold: true, color: BLUE, align: "center", valign: "middle" });
  txt(s, "400 V = 1,73 × 231 V    ·    U_{ph} = U / √3", { x: 4.6, y: 1.62, w: 4.8, h: 0.5, fontSize: 13, align: "center", valign: "middle" });
  s.addTable([
    [cell("On mesure entre…", H), cell("C'est…", H), cell("Valeur", H)],
    [cell("L1-N, L2-N, L3-N"), cell("U_{ph}, tension de phase"), cell("230 V", { bold: true })],
    [cell("L1-L2, L2-L3, L3-L1"), cell("U, tension réseau"), cell("400 V", { bold: true })],
  ], { x: 4.5, y: 2.45, w: 5.0, colW: [1.8, 2.2, 1.0], rowH: 0.36, border: BORDER, fontSize: 11 });
  boxTitle(s, 4.5, 3.75, 5.0, 1.8, "Lire la désignation d'un réseau", [
    "3 × 400 V : trois conducteurs polaires, sans neutre.",
    "3 × 400/230 V : trois polaires + neutre (+ PE).",
    "Couleurs : L1 brun, L2 noir, L3 gris, N bleu, PE vert-jaune.",
  ], 11.5, true);
}

// ============================== 4. ÉTOILE ET TRIANGLE
{
  const s = slide("Étoile Y ou triangle Δ : deux façons de brancher",
    "Étoile : chaque élément est entre une phase et le point étoile, donc sous U_ph = 230 V. Le courant de ligne traverse directement l'élément : I = I_ph. Si la charge est équilibrée, le neutre ne transporte rien et peut être omis.\n" +
    "Triangle : chaque élément est entre deux phases, donc sous U = 400 V. Au nœud A (L1), Kirchhoff donne I1 = I_ph1 − I_ph3 (somme vectorielle) ; avec deux courants égaux décalés de 120°, on obtient I = √3 · I_ph.\n" +
    "Erreur fréquente : écrire I = 3 · I_ph en triangle. Rappeler que l'addition est vectorielle.\n" +
    "Le conducteur PE ne participe pas au fonctionnement ; il relie les parties métalliques à la terre.\n" +
    "Faire compléter oralement : « à éléments identiques, lequel consomme le plus ? » → triangle, 3 fois plus (chaque élément a √3 fois plus de tension, donc 3 fois plus de puissance).");
  txt(s, "Étoile Y", { x: 0.5, y: 0.9, w: 4.4, h: 0.32, fontSize: 15, bold: true, color: BLUE });
  img(s, "fig_etoile.png", 0.5, 1.25, 4.4, 2.55);
  txt(s, "Triangle Δ", { x: 5.1, y: 0.9, w: 4.4, h: 0.32, fontSize: 15, bold: true, color: BLUE });
  img(s, "fig_triangle.png", 5.55, 1.25, 3.6, 2.55);
  [[0.5, ["U_{ph} = U / √3 = 230 V", "I = I_{ph}"], "Chaque élément sous 230 V"],
   [5.1, ["U_{ph} = U = 400 V", "I = √3 · I_{ph}"], "Chaque élément sous 400 V"]].forEach(([x, f, t]) => {
    card(s, x, 3.95, 4.4, 1.0);
    txt(s, f[0] + "\n" + f[1], { x: x + 0.15, y: 4.0, w: 2.6, h: 0.9, fontSize: 16, bold: true, valign: "middle" });
    txt(s, t, { x: x + 2.75, y: 4.0, w: 1.55, h: 0.9, fontSize: 11, italic: true, color: GR, valign: "middle" });
  });
  frame(s, 0.5, 5.07, 9.0, 0.5);
  txt(s, "À éléments identiques, le triangle consomme 3 fois plus que l'étoile :  P_{Δ} = 3 · P_{Y}", { x: 0.65, y: 5.1, w: 8.7, h: 0.44, fontSize: 13, bold: true, valign: "middle" });
}

// ============================== 5. PLAQUE SIGNALÉTIQUE ET PLAQUE À BORNES
{
  const s = slide("Lire la plaque signalétique avant de coupler",
    "Règle : la plus petite tension de la plaque est la tension que supporte un enroulement. On choisit le couplage qui met chaque enroulement sous cette tension.\n" +
    "Sur notre réseau 3 × 400/230 V : « 230 Δ / 400 Y » → étoile (chaque enroulement reçoit 230 V). « 400 Δ / 690 Y » → triangle (chaque enroulement reçoit 400 V).\n" +
    "Les deux courants de la plaque (14,2 / 8,2 A) correspondent aux deux couplages : 14,2 A sur un réseau 3 × 230 V en triangle, 8,2 A sur un réseau 3 × 400 V en étoile. Le rapport vaut √3.\n" +
    "Plaque à bornes CEI : U1 V1 W1 en haut, W2 U2 V2 en bas (décalés) pour que les barrettes soient soit horizontales (étoile), soit verticales (triangle).\n" +
    "Démarrage étoile-triangle : un moteur 400 Δ démarre en étoile (courant et couple divisés par 3) puis passe en triangle. On le voit sur les pompes et les ventilateurs de plus de quelques kW.\n" +
    "Danger : un moteur 230 Δ / 400 Y couplé en triangle sur 400 V reçoit √3 fois trop de tension par enroulement : surintensité, échauffement, destruction de l'isolation.");
  img(s, "fig_plaque_moteur.png", 0.5, 0.95, 3.9);
  txt(s, "Plaque d'un moteur (exemple)", { x: 0.5, y: 3.1, w: 3.9, h: 0.25, fontSize: 9.5, italic: true, color: GR, align: "center" });
  img(s, "fig_plaque_Y.png", 4.7, 0.92, 2.3);
  img(s, "fig_plaque_D.png", 7.2, 0.92, 2.3);
  s.addTable([
    [cell("Plaque", H), cell("Réseau 3 × 400/230 V", H), cell("Un enroulement reçoit", H)],
    [cell("230 Δ / 400 Y"), cell("étoile Y", { bold: true, color: BLUE }), cell("230 V")],
    [cell("400 Δ / 690 Y"), cell("triangle Δ", { bold: true, color: BLUE }), cell("400 V")],
  ], { x: 0.5, y: 3.45, w: 4.6, colW: [1.4, 1.65, 1.55], rowH: 0.34, border: BORDER });
  frame(s, 0.5, 4.6, 4.6, 0.95);
  txt(s, "Règle : la plus petite tension de la plaque est la tension d'un enroulement.", { x: 0.65, y: 4.66, w: 4.3, h: 0.83, fontSize: 12.5, bold: true, valign: "middle" });
  life(s, 5.3, 3.45, 4.2, 2.1, [
    "Démarrage étoile-triangle : le moteur démarre en Y (courant ÷ 3), puis passe en Δ.",
    "Erreur de couplage = enroulements sous √3 fois trop de tension : le moteur brûle.",
    "Avant toute mise en service : lire la plaque, puis poser les barrettes.",
  ]);
}

// ============================== 6. PUISSANCES ET EXEMPLE GUIDÉ
{
  const s = slide("Puissances : la même formule en étoile et en triangle",
    "Démonstration en étoile : P = 3 · U_ph · I_ph · cos φ avec U_ph = U/√3 et I_ph = I → P = √3 · U · I · cos φ. En triangle : U_ph = U et I_ph = I/√3 → même résultat.\n" +
    "Conséquence pratique (remarque 2 du fascicule) : si on connaît U, I de ligne et cos φ, on calcule la puissance sans se soucier du couplage. C'est ce que fait l'électricien avec une pince ampèremétrique sur la ligne.\n" +
    "Exemple guidé (fascicule, exemple 1 p. 11.9), au tableau en verbalisant chaque étape : moteur 2,8 kW absorbés, 3 × 400 V, cos φ = 0,85, étoile. I = 2800 / (1,732 · 400 · 0,85) = 4,75 A. En étoile, courant dans l'enroulement = 4,75 A. Tension d'un enroulement = 400 / 1,732 = 231 V. sin φ = 0,527 → Q = 1,732 · 400 · 4,75 · 0,527 = 1,74 kvar.\n" +
    "Réponse à la question de départ : borne 11 kW → I = 11 000 / (1,732 · 400) = 15,9 A, soit 16 A par phase. La prise domestique : 230 V · 16 A = 3,7 kW. On transporte trois fois plus de puissance avec le même courant par conducteur.\n" +
    "Le N°1 de la fiche reprend la démarche sans cette aide, sur la plaque de la diapositive 5.");
  card(s, 0.5, 0.95, 4.4, 2.1);
  txt(s, "P = √3 · U · I · cos φ", { x: 0.6, y: 1.0, w: 4.2, h: 0.55, fontSize: 21, bold: true, color: BLUE, align: "center", valign: "middle" });
  txt(s, "Q = √3 · U · I · sin φ        S = √3 · U · I", { x: 0.6, y: 1.55, w: 4.2, h: 0.4, fontSize: 13.5, bold: true, align: "center", valign: "middle" });
  txt(s, "U : tension réseau [V] · I : courant de ligne [A]\nP en W · Q en var · S en VA", { x: 0.6, y: 2.0, w: 4.2, h: 0.5, fontSize: 11, italic: true, align: "center" });
  txt(s, "Valable en Y et en Δ, dès que la charge est équilibrée.", { x: 0.6, y: 2.55, w: 4.2, h: 0.4, fontSize: 11.5, bold: true, align: "center" });
  frame(s, 5.1, 0.95, 4.4, 2.1);
  txt(s, "Réponse à la question de départ", { x: 5.25, y: 1.02, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
  txt(s, "Borne 11 kW en triphasé :\nI = 11 000 W / (√3 · 400 V) = 15,9 A ≈ 16 A\n\nPrise 16 A en monophasé :\nP = 230 V · 16 A = 3,7 kW", { x: 5.25, y: 1.36, w: 4.1, h: 1.62, fontSize: 12 });
  txt(s, "Exemple guidé : moteur 2,8 kW absorbés, 3 × 400 V, cos φ = 0,85, couplé en étoile", { x: 0.5, y: 3.2, w: 9.0, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
  const S = [
    ["1", "Courant de ligne", "I = 2800 / (√3 · 400 · 0,85)\n= 4,75 A"],
    ["2", "Courant d'enroulement", "étoile : I_{ph} = I\n= 4,75 A"],
    ["3", "Tension d'enroulement", "U_{ph} = 400 / √3\n= 231 V"],
    ["4", "Puissance réactive", "sin φ = 0,527\nQ = 1,74 kvar"],
  ];
  S.forEach((st, i) => {
    const x = 0.5 + i * 2.27;
    card(s, x, 3.55, 2.15, 1.95);
    badge(s, x + 0.1, 3.63, st[0], 0.32);
    txt(s, st[1], { x: x + 0.48, y: 3.6, w: 1.62, h: 0.4, fontSize: 11, bold: true, valign: "middle" });
    txt(s, st[2], { x: x + 0.1, y: 4.1, w: 1.98, h: 1.3, fontSize: 12, bold: true, valign: "middle" });
  });
}

// ============================== 7. DÉSÉQUILIBRE ET COURANT DE NEUTRE
{
  const s = slide("Charge déséquilibrée : le neutre ramène la différence",
    "Les récepteurs monophasés (éclairage, prises, petits appareils) sont branchés entre une phase et le neutre, sous 230 V. Vus ensemble, ils forment une étoile déséquilibrée.\n" +
    "Avec le neutre, chaque récepteur reste sous 230 V. Le neutre transporte la somme vectorielle des trois courants (et non la somme arithmétique).\n" +
    "Construction graphique : on place les vecteurs bout à bout en respectant 120° entre eux ; le vecteur qui referme la figure est I_N. Exemple du graphique : 10 A, 6 A et 4 A résistifs → I_N = 5,3 A.\n" +
    "Formule (récepteurs de même cos φ) : I_N = √(I1² + I2² + I3² − I1·I2 − I1·I3 − I2·I3) = √(100 + 36 + 16 − 60 − 40 − 24) = √28 = 5,29 A.\n" +
    "Attention : avec des charges de cos φ différents (exemple 2 du fascicule), I_N peut dépasser le plus grand courant de phase. Il faut alors un diagramme vectoriel complet.\n" +
    "Puissance d'une charge déséquilibrée : P = P1 + P2 + P3 (somme arithmétique) ; Q = Q_L − Q_C.");
  img(s, "fig_IN_demo.png", 0.5, 0.92, 3.9, 3.05);
  txt(s, "L1 : 10 A · L2 : 6 A · L3 : 4 A (résistifs)", { x: 0.5, y: 4.0, w: 3.9, h: 0.3, fontSize: 10.5, italic: true, color: GR, align: "center" });
  card(s, 4.6, 0.95, 4.9, 1.85);
  txt(s, "Courant dans le neutre (charges de même cos φ)", { x: 4.75, y: 1.0, w: 4.6, h: 0.3, fontSize: 12, bold: true, color: BLUE });
  txt(s, "I_{N} = √(I_{1}^{2} + I_{2}^{2} + I_{3}^{2} − I_{1}·I_{2} − I_{1}·I_{3} − I_{2}·I_{3})", { x: 4.75, y: 1.35, w: 4.6, h: 0.55, fontSize: 13, bold: true, valign: "middle" });
  txt(s, "Puissance totale : P = P_{1} + P_{2} + P_{3}\nRéactive : Q = Q_{L} − Q_{C}", { x: 4.75, y: 1.95, w: 4.6, h: 0.8, fontSize: 12.5 });
  boxTitle(s, 4.6, 2.95, 4.9, 1.25, "Ce qu'il faut retenir", [
    "Équilibré : I_{N} = 0, on peut se passer du neutre.",
    "Déséquilibré : le neutre maintient 230 V sur chaque récepteur.",
  ], 11.5, true);
  life(s, 0.5, 4.4, 9.0, 1.15, [
    "L'installateur répartit les groupes monophasés (éclairage, prises, cuisine) sur L1, L2 et L3 pour réduire I_{N}.",
    "Un tableau de répartition équilibré chauffe moins et laisse plus de réserve aux disjoncteurs.",
  ]);
}

// ============================== 8. PANNES : NEUTRE OUVERT, PHASE COUPÉE
{
  const s = slide("Pannes : neutre ouvert, phase ou élément coupé",
    "Neutre ouvert (exemple du fascicule p. 11.18) : plaque 800 W sur L1, radiateur 3000 W sur L2. Sans neutre, les deux appareils sont en série sous 400 V. R_plaque = 230²/800 = 66,1 Ω ; R_radiateur = 230²/3000 = 17,6 Ω ; I = 400/83,7 = 4,78 A. U_plaque = 316 V (détruite), U_radiateur = 84 V. Le petit appareil reçoit la surtension.\n" +
    "Danger pour les personnes : en schéma TN-C (conducteur PEN commun), une coupure du PEN met les carcasses sous tension.\n" +
    "Ordre obligatoire. Déconnexion : L1 - L2 - L3 - N - PE. Connexion : PE - N - L1 - L2 - L3. Le neutre se coupe en dernier et se rétablit en premier ; c'est pourquoi le pôle neutre d'un disjoncteur est à coupure retardée.\n" +
    "Tableau des puissances (récepteur résistif équilibré, fascicule p. 11.24) : en triangle, une phase coupée donne P/2 et un élément coupé 2P/3. En étoile sans neutre, une phase ou un élément coupé donne P/2.\n" +
    "Diagnostic : un chauffe-eau qui chauffe deux fois plus lentement peut avoir un fusible de ligne fondu. On le confirme en mesurant les trois courants de ligne avec une pince.");
  img(s, "fig_neutre_coupe.png", 0.5, 0.95, 4.5);
  card(s, 0.5, 3.55, 4.5, 0.75);
  txt(s, "U_{plaque} = 316 V → détruite\nU_{radiateur} = 84 V", { x: 0.65, y: 3.58, w: 4.2, h: 0.7, fontSize: 13, bold: true, color: RED, valign: "middle" });
  frame(s, 0.5, 4.45, 4.5, 1.1);
  txt(s, "Ordre de manœuvre", { x: 0.65, y: 4.5, w: 4.2, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
  txt(s, "Déconnecter : L1 → L2 → L3 → N → PE\nConnecter : PE → N → L1 → L2 → L3", { x: 0.65, y: 4.82, w: 4.2, h: 0.68, fontSize: 12.5, bold: true });
  txt(s, "Puissance restante (récepteur résistif équilibré)", { x: 5.2, y: 0.95, w: 4.3, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
  s.addTable([
    [cell("Défaut", H), cell("Triangle Δ", H), cell("Étoile Y sans N", H)],
    [cell("Un fil de ligne coupé"), cell("P / 2", { bold: true }), cell("P / 2", { bold: true })],
    [cell("Un élément coupé"), cell("2P / 3", { bold: true }), cell("P / 2", { bold: true })],
  ], { x: 5.2, y: 1.3, w: 4.3, colW: [1.7, 1.3, 1.3], rowH: 0.42, border: BORDER });
  boxTitle(s, 5.2, 2.75, 4.3, 1.2, "Contrôle à l'ohmmètre (Δ, barrettes en place)", [
    "On mesure R ∥ 2R = 2R/3, pas R.",
    "Pour lire un élément seul : retirer les barrettes.",
  ], 11);
  life(s, 5.2, 4.1, 4.3, 1.45, [
    "Chauffe-eau qui chauffe 2 fois plus lentement : fusible de ligne fondu ?",
    "Neutre desserré dans un tableau : ampoules qui grillent, appareils détruits.",
  ]);
}

// ============================== 9. MESURE DE PUISSANCE ET COMPENSATION
{
  const s = slide("Mesurer la puissance et améliorer le cos φ",
    "Mesure : charge équilibrée avec neutre accessible → un seul wattmètre, P = 3 · P1. Charge quelconque avec neutre → trois wattmètres, P = P1 + P2 + P3. Réseau à trois conducteurs → méthode des deux wattmètres, P = P1 + P2 (somme algébrique). Si un wattmètre dévie à l'envers, on inverse son circuit tension et on soustrait sa lecture. Aujourd'hui, un analyseur de réseau fait ces calculs, mais le principe est le même ; les compteurs d'énergie à trois conducteurs l'utilisent aussi.\n" +
    "Compensation : une batterie de condensateurs centralisée, couplée en triangle (chaque condensateur sous 400 V), fournit Q_C = P · (tan φ1 − tan φ2). Chaque condensateur fournit Q_C/3 ; C = Q_C1 / (U² · ω).\n" +
    "Exemple du fascicule p. 11.29 : usine 160 kW, cos φ = 0,72, batterie 80 kvar → cos φ passe à 0,91, le courant de ligne de 321 A à 254 A.\n" +
    "Intérêt : moins de courant dans les lignes et les transformateurs, moins de pertes (3 · R · I²), pas d'énergie réactive facturée. Un régulateur enclenche les échelons selon le besoin, sans passer en capacitif.\n" +
    "Le seuil de facturation dépend du contrat du distributeur (0,95 dans l'exemple du fascicule).");
  txt(s, "Méthode des deux wattmètres", { x: 0.5, y: 0.92, w: 4.4, h: 0.3, fontSize: 13, bold: true, color: BLUE });
  img(s, "fig_2w.png", 0.6, 1.25, 4.1);
  s.addTable([
    [cell("Situation", H), cell("Mesure", H)],
    [cell("Équilibré, neutre accessible", { fontSize: 10.5 }), cell("P = 3 · P_{1}", { bold: true })],
    [cell("Quelconque, avec neutre", { fontSize: 10.5 }), cell("P = P_{1} + P_{2} + P_{3}", { bold: true })],
    [cell("Quelconque, 3 conducteurs", { fontSize: 10.5 }), cell("P = P_{1} + P_{2}", { bold: true })],
  ], { x: 0.5, y: 3.35, w: 4.4, colW: [2.5, 1.9], rowH: 0.34, border: BORDER, fontSize: 10.5 });
  txt(s, "Si un wattmètre dévie à l'envers : inverser son circuit tension et soustraire sa lecture.", { x: 0.5, y: 5.12, w: 4.4, h: 0.45, fontSize: 10, italic: true, color: GR });
  txt(s, "Compensation du facteur de puissance", { x: 5.1, y: 0.92, w: 4.4, h: 0.3, fontSize: 13, bold: true, color: BLUE });
  img(s, "fig_comp.png", 5.2, 1.25, 3.9);
  card(s, 5.1, 3.6, 4.4, 1.05);
  txt(s, "Q_{C} = P · (tan φ_{1} − tan φ_{2})\nC = Q_{C1} / (U^{2} · ω)   avec Q_{C1} = Q_{C} / 3", { x: 5.25, y: 3.65, w: 4.1, h: 0.95, fontSize: 13, bold: true, valign: "middle" });
  life(s, 5.1, 4.75, 4.4, 0.8, [
    "Moins de courant, moins de pertes, pas d'énergie réactive facturée.",
  ], 10.5);
}

// ============================== 10. CHUTE DE TENSION · TICKET DE SORTIE
{
  const s = slide("Chute de tension en ligne · ticket de sortie",
    "En monophasé, le courant fait l'aller et le retour : on compte deux fois la longueur. En triphasé équilibré, il n'y a pas de retour (I_N = 0) : chaque conducteur polaire est une résistance R_c = ρ · l / A en série avec le récepteur, et la chute de tension réseau vaut ΔU = √3 · R_c · I.\n" +
    "Exemple rapide : 60 m de cuivre 4 mm² (ρ = 0,0175 Ω·mm²/m) → R_c = 0,26 Ω ; I = 14,5 A → ΔU = 6,6 V, soit 1,6 % de 400 V. Pertes : 3 · 0,26 · 14,5² = 165 W.\n" +
    "Remarque du fascicule : en basse tension, on vérifie aussi qu'un court-circuit en bout de ligne fait déclencher la protection dans les 5 s.\n" +
    "Ticket de sortie (5 min, seul·e, sans la fiche ; à ramasser pour préparer la séance suivante). Réponses : 1) U_ph = 400/√3 = 231 V. 2) I_ph = 17,3/√3 = 10 A. 3) L1 - L2 - L3 - N - PE (neutre en dernier, PE tout à la fin). 4) Étoile, car la plus petite tension (230 V) est celle d'un enroulement et notre réseau fournit 400 V entre phases.\n" +
    "Puis : fiche d'exercices N°1 à N°9.");
  card(s, 0.5, 0.95, 4.4, 1.75);
  txt(s, "ΔU = √3 · R_{c} · I", { x: 0.6, y: 1.0, w: 4.2, h: 0.55, fontSize: 22, bold: true, color: BLUE, align: "center", valign: "middle" });
  txt(s, "R_{c} = ρ · l / A   (un seul conducteur, longueur simple)\nPertes : P_{l} = 3 · R_{c} · I^{2}\nU_{2} ≈ U_{1} − ΔU", { x: 0.65, y: 1.6, w: 4.1, h: 1.05, fontSize: 12, align: "center" });
  frame(s, 5.1, 0.95, 4.4, 1.75);
  txt(s, "Pourquoi pas 2 × l comme en monophasé ?", { x: 5.25, y: 1.0, w: 4.1, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
  txt(s, "En triphasé équilibré, il n'y a pas de courant de retour. Le facteur √3 convertit la chute d'un conducteur en chute de tension réseau.", { x: 5.25, y: 1.35, w: 4.1, h: 1.3, fontSize: 12 });
  frame(s, 0.5, 2.9, 9.0, 2.65);
  txt(s, "Ticket de sortie : seul·e, 5 minutes, sans la fiche", { x: 0.65, y: 2.97, w: 8.7, h: 0.3, fontSize: 13, bold: true, color: BLUE });
  [["1", "Réseau 3 × 400 V : que vaut U_{ph} ?"], ["2", "Corps de chauffe en Δ, I = 17,3 A : courant dans un élément ?"],
   ["3", "Dans quel ordre déconnecter L1, L2, L3, N et PE ?"], ["4", "Moteur 230 Δ / 400 Y sur notre réseau : quel couplage ? Pourquoi ?"]].forEach((q, i) => {
    const x = 0.65 + (i % 2) * 4.45, y = 3.4 + Math.floor(i / 2) * 0.85;
    badge(s, x, y + 0.12, q[0], 0.34);
    txt(s, q[1], { x: x + 0.45, y, w: 3.85, h: 0.62, fontSize: 12, valign: "middle" });
  });
  txt(s, "Puis : fiche d'exercices N°1 à N°9.", { x: 0.65, y: 5.15, w: 8.7, h: 0.3, fontSize: 10.5, italic: true, color: GR });
}

// pptxgenjs écrit un <a:pPr> par run : on ne garde que le premier de chaque paragraphe (sinon la puce disparaît)
const JSZip = (function(){try{return require("jszip")}catch(e){return require("/opt/npm-tools/node_modules/jszip")}})(), fs = require("fs");
pres.write({ outputType: "nodebuffer" }).then(async (buf) => {
  const zip = await JSZip.loadAsync(buf);
  for (const name of Object.keys(zip.files).filter(n => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    let x = await zip.file(name).async("string");
    x = x.replace(/<a:p>([\s\S]*?)<\/a:p>/g, (m, inner) => {
      let first = true;
      inner = inner.replace(/<a:pPr\b[^>]*\/>|<a:pPr\b[^>]*>[\s\S]*?<\/a:pPr>/g, (pp) => { if (first) { first = false; return pp; } return ""; });
      return "<a:p>" + inner + "</a:p>";
    });
    zip.file(name, x);
  }
  const clean = new JSZip();                     // sans entrées de dossier (gênent l'ouverture dans SharePoint/Teams)
  for (const n of Object.keys(zip.files)) if (!zip.files[n].dir) clean.file(n, await zip.file(n).async("nodebuffer"), { createFolders: false });
  fs.writeFileSync("out/Courant alternatif triphasé – présentation.pptx", await clean.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
  console.log("deck ok");
});
