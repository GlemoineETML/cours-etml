// Présentation « La charge d'un condensateur » — 4 diapositives — charte ETML (marine 242852, bleu 297FD5), Arial, 16:10
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.defineLayout({ name: "ETML1610", width: 10, height: 6.25 });
pres.layout = "ETML1610";
pres.author = "Gaël Lemoine";
pres.company = "ETML – Section électronique";
pres.title = "La charge d'un condensateur";
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };

const NAVY = "242852", BLUE = "297FD5", LBLUE = "ACCBF9", TINT = "E8EFFB";
const K = NAVY, GR = "5A6478", RED = "EE0000";
const F = "Arial", MONO = "Courier New";
const TOPIC = "Test et Mesure 1 – El DT 1 · Charge d'un condensateur";
const CLASSE = "CLO1B", ANNEE = "2026-2027", CHAMP = "LZ_6969";
const DATE_US = "11/05/2026";               // date à l'américaine (MM/DD/YYYY)
const FLOYD_URL = "", NEXTEC_URL = "";      // références sans lien pour cette édition test
const LOGO_BAND = "logo_white_v.png";       // logo du modèle Rapport_Simple.dotx, en blanc, vertical

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

// zone utile x ≤ 8,9" (bandeau) : on écrit sur une grille 0,5 → 9,5" puis on comprime horizontalement
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

// « u_{C} » → indice, « e^{−t/τ} » → exposant (notation CEI : grandeur en italique, indice droit)
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
function expand(t) {
  if (typeof t === "string") return R(t) || t;
  if (Array.isArray(t)) return [].concat(...t.map(r => (r && typeof r.text === "string" && R(r.text, r.options)) || [r]));
  return t;
}
function slide(title, notes) {
  const s = pres.addSlide({ masterName: "CONTENU" });
  s.addText(expand(title), { x: 0.5, y: 0.25, w: 8.4, h: 0.55, fontFace: F, fontSize: 24, bold: true, color: NAVY, margin: 0, valign: "middle", fit: "shrink" });
  squeeze(s, 0.5, 9.5, 8.9);
  if (notes) s.addNotes(notes);
  return s;
}
function txt(s, text, o) { s.addText(expand(text), Object.assign({ fontFace: F, fontSize: 14, color: K, margin: 0, valign: "top" }, o)); }
function card(s, x, y, w, h, fill) { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill || TINT }, line: { color: fill || TINT, width: 0 } }); }
function frame(s, x, y, w, h) { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.25 } }); }
function badge(s, x, y, label, d) {
  d = d || 0.4;
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: K }, line: { color: K } });
  s.addText(label, { x, y, w: d, h: d, fontFace: F, fontSize: 13, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0 });
}
function life(s, x, y, w, h, lines, fs) {
  card(s, x, y, w, h);
  const runs = [{ text: "Dans la vraie vie", options: { bold: true, color: BLUE, breakLine: true } }];
  lines.forEach((l, i) => runs.push({ text: l, options: { color: K, bullet: { indent: 12 }, breakLine: i < lines.length - 1 } }));
  s.addText(expand(runs), { x: x + 0.15, y: y + 0.08, w: w - 0.3, h: h - 0.16, fontFace: F, fontSize: fs || 11.5, margin: 0, valign: "top", paraSpaceAfter: 2 });
}
const cell = (t, o) => ({ text: expand(String(t)), options: Object.assign({ align: "center", valign: "middle", fontFace: F, fontSize: 13, color: K }, o || {}) });
const H = { fill: { color: LBLUE }, bold: true, fontSize: 12, color: NAVY };
const BORDER = { type: "solid", color: K, pt: 0.75 };
const ref = (label, url, extra) => url
  ? { text: label, options: Object.assign({ hyperlink: { url } }, extra || {}) }
  : { text: label + " [lien à compléter]", options: Object.assign({ color: GR }, extra || {}) };

// ============================== 1. TITRE · OBJECTIFS · QUESTION DE DÉPART
{
  const s = pres.addSlide({ masterName: "TITRE" });
  squeeze(s, 0.6, 9.5, 8.9);
  txt(s, "TEST ET MESURE 1 – EL DT 1", { x: 0.6, y: 0.45, w: 5.2, h: 0.3, fontSize: 12, bold: true, color: BLUE, charSpacing: 1 });
  txt(s, "La charge\nd'un condensateur", { x: 0.6, y: 0.75, w: 5.4, h: 1.05, fontSize: 28, bold: true, color: NAVY, valign: "middle" });
  txt(s, "Circuit RC, constante de temps τ et mesure à l'oscilloscope", { x: 0.6, y: 1.82, w: 5.4, h: 0.52, fontSize: 13, color: GR });
  txt(s, "À la fin de la leçon, je suis capable de…", { x: 0.6, y: 2.42, w: 5.4, h: 0.3, fontSize: 14, bold: true });
  ["décrire u_{C} et i pendant la charge ;", "calculer τ = R · C et la durée de charge (5τ) ;", "calculer u_{C} à un instant t donné ;", "mesurer τ à l'oscilloscope."].forEach((t, i) => {
    const y = 2.8 + i * 0.44;
    badge(s, 0.6, y + 0.02, String(i + 1), 0.36);
    txt(s, t, { x: 1.1, y, w: 4.9, h: 0.4, fontSize: 14, valign: "middle" });
  });
  s.addImage({ path: "fig_circuit.png", x: 6.15, y: 0.45, w: 3.35, h: 1.61 });
  txt(s, "Circuit de charge RC (symboles CEI 60617)", { x: 6.15, y: 2.1, w: 3.35, h: 0.28, fontSize: 9.5, italic: true, color: GR, align: "center" });
  frame(s, 6.15, 2.5, 3.35, 1.95);
  txt(s, "Question de départ", { x: 6.3, y: 2.58, w: 3.1, h: 0.3, fontSize: 13, bold: true, color: BLUE });
  txt(s, "Après un éclair, le flash d'un appareil photo doit attendre quelques secondes avant de pouvoir se redéclencher. Pourquoi ?", { x: 6.3, y: 2.9, w: 3.1, h: 1.0, fontSize: 12 });
  txt(s, "Écris ton hypothèse. Réponse en fin de leçon.", { x: 6.3, y: 3.98, w: 3.1, h: 0.4, fontSize: 10.5, italic: true, color: GR });
  card(s, 0.6, 4.6, 8.9, 0.88);
  s.addText(expand([
    { text: `Classe ${CLASSE} · année ${ANNEE} · champ d'apprentissage ${CHAMP} · éditeur : Gaël Lemoine · ${DATE_US}`, options: { bold: true, breakLine: true } },
    { text: "Références : ", options: { color: K } },
    ref("Floyd, chapitre sur les circuits RC", FLOYD_URL),
    { text: " · ", options: { color: K } },
    ref("Nextec Media, chapitre condensateur", NEXTEC_URL),
  ]), { x: 0.8, y: 4.65, w: 8.5, h: 0.78, fontFace: F, fontSize: 11.5, color: NAVY, margin: 0, valign: "middle", paraSpaceAfter: 3 });
  s.addNotes("Durée : 45 min de théorie, puis 45 min d'exercices (fiche N°1 à N°7 ; N°8 est à donner une semaine plus tard).\n" +
    "Déroulé : question de départ (3 min) → que se passe-t-il quand on ferme S (12 min) → constante de temps et exemple guidé (15 min) → mesure à l'oscilloscope et applications (10 min) → ticket de sortie (5 min).\n" +
    "Prérequis : loi d'Ohm, loi des mailles, puissance P = U · I, préfixes (k, M, m, µ, n), le condensateur stocke des charges (Q = C · U).\n" +
    "Question de départ : faire écrire une hypothèse individuelle, sans corriger. Prédire avant d'apprendre améliore la mémorisation. Réponse : le flash est alimenté par un condensateur chargé à travers une résistance ; la charge suit une courbe RC et prend environ 5τ, donc quelques secondes.");
}

// ============================== 2. QUE SE PASSE-T-IL QUAND ON FERME S ?
{
  const s = slide("Que se passe-t-il quand on ferme l'interrupteur S ?",
    "Faire d'abord prédire aux apprentis : « à t = 0, le condensateur est vide ; quelle tension a-t-il ? Où se retrouve toute la tension U ? » Puis dérouler les 3 cartes.\n" +
    "Un condensateur vide a u_C = 0, donc la loi des mailles donne u_R = U et le courant de départ vaut I0 = U / R (c'est le courant maximal). À mesure que des charges s'accumulent, u_C augmente, u_R = U − u_C diminue, donc le courant diminue. Quand u_C = U, plus aucun courant ne circule : en régime continu établi, le condensateur se comporte comme un circuit ouvert.\n" +
    "Analogie si besoin : remplir un réservoir par un tuyau étroit (la résistance). Au début l'eau entre vite ; plus le niveau monte, plus le débit ralentit. Limite de l'analogie à signaler : dans le circuit, c'est la différence U − u_C qui pousse le courant.\n" +
    "Symboles CEI 60617 : résistance = rectangle, condensateur = deux plaques parallèles, source de tension idéale = cercle traversé par le conducteur. Grandeurs variables en minuscules (u_C, i), grandeurs constantes en majuscules (U, I0).");
  s.addImage({ path: "fig_circuit.png", x: 0.5, y: 0.95, w: 3.9, h: 1.88 });
  const C = [
    ["1", "t = 0 : le condensateur est vide", "u_{C} = 0 → toute la tension est sur R : u_{R} = U. Le courant est maximal : I_{0} = U / R."],
    ["2", "Pendant la charge", "u_{C} monte, donc u_{R} = U − u_{C} diminue, et le courant i diminue."],
    ["3", "Fin de charge", "u_{C} = U, u_{R} = 0, i = 0 : en continu, le condensateur chargé bloque le courant."],
  ];
  C.forEach((c, i) => {
    const y = 0.95 + i * 0.66;
    card(s, 4.6, y, 4.9, 0.6);
    badge(s, 4.7, y + 0.1, c[0]);
    s.addText(expand([{ text: c[1], options: { bold: true, breakLine: true } }, { text: c[2], options: {} }]),
      { x: 5.22, y: y + 0.03, w: 4.22, h: 0.54, fontFace: F, fontSize: 11, color: K, margin: 0, valign: "middle" });
  });
  s.addImage({ path: "fig_courbes.png", x: 0.5, y: 2.95, w: 6.85, h: 2.61 });
  frame(s, 7.65, 3.05, 1.85, 2.4);
  txt(s, "À chaque instant", { x: 7.75, y: 3.12, w: 1.7, h: 0.3, fontSize: 11.5, bold: true, color: BLUE });
  txt(s, "U = u_{R} + u_{C}", { x: 7.7, y: 3.45, w: 1.75, h: 0.4, fontSize: 15, bold: true, align: "center" });
  txt(s, "(loi des mailles)", { x: 7.7, y: 3.85, w: 1.75, h: 0.28, fontSize: 10, italic: true, color: GR, align: "center" });
  txt(s, "La tension monte vite au début, puis de plus en plus lentement.", { x: 7.75, y: 4.2, w: 1.7, h: 1.15, fontSize: 10.5 });
}

// ============================== 3. LA CONSTANTE DE TEMPS τ
{
  const s = slide("La constante de temps τ = R · C fixe la vitesse de charge",
    "τ (tau) se mesure en secondes : 1 Ω × 1 F = 1 s. Faire convertir les préfixes en puissances de 10 avant de multiplier ; c'est l'erreur la plus fréquente.\n" +
    "La courbe a toujours la même forme, quelles que soient les valeurs de R et C : seule l'échelle de temps change. Après τ, le condensateur est chargé à 63 % ; après 5τ, à 99 % : en pratique, on le considère chargé. La tangente à l'origine coupe le palier U à t = τ (deuxième méthode de lecture graphique).\n" +
    "Formule u_C(t) = U · (1 − e^(−t/τ)) : la calculatrice suffit (touche e^x). La démonstration n'est pas au programme de première année.\n" +
    "Exemple guidé au tableau, en verbalisant chaque étape (R = 10 kΩ, C = 100 µF, U = 12 V) : τ = 10·10³ Ω × 100·10⁻⁶ F = 1 s ; après 1 s, u_C = 0,632 × 12 V = 7,6 V ; chargé après 5τ = 5 s ; courant de départ I0 = 12 V / 10 kΩ = 1,2 mA. L'exercice N°1 reprend ensuite la démarche, sans cette aide.");
  card(s, 0.5, 0.95, 4.4, 1.55);
  txt(s, "τ = R · C", { x: 0.65, y: 1.0, w: 4.1, h: 0.55, fontSize: 26, bold: true, color: BLUE, align: "center", valign: "middle" });
  txt(s, "τ en s  ·  R en Ω  ·  C en F", { x: 0.65, y: 1.55, w: 4.1, h: 0.3, fontSize: 11.5, italic: true, align: "center" });
  txt(s, "u_{C}(t) = U · (1 − e^{−t / τ})", { x: 0.65, y: 1.9, w: 4.1, h: 0.5, fontSize: 17, bold: true, align: "center", valign: "middle" });
  s.addTable([
    [cell("t", H), cell("τ", H), cell("2τ", H), cell("3τ", H), cell("4τ", H), cell("5τ", H)],
    [cell("u_{C} / U", { bold: true, fontSize: 12 }), cell("63 %", { bold: true }), cell("86 %"), cell("95 %"), cell("98 %"), cell("99 %", { bold: true, fill: { color: TINT } })],
  ], { x: 0.5, y: 2.65, w: 4.4, colW: [1.0, 0.68, 0.68, 0.68, 0.68, 0.68], rowH: 0.36, border: BORDER });
  frame(s, 0.5, 3.5, 4.4, 0.46);
  txt(s, "Règle de métier : après 5τ, le condensateur est chargé.", { x: 0.62, y: 3.53, w: 4.2, h: 0.4, fontSize: 12, bold: true, valign: "middle" });
  s.addImage({ path: "fig_tau.png", x: 5.1, y: 0.92, w: 4.4, h: 2.83 });
  txt(s, "Exemple guidé : R = 10 kΩ, C = 100 µF, U = 12 V", { x: 0.5, y: 4.07, w: 9.0, h: 0.3, fontSize: 13, bold: true, color: BLUE });
  const S = [
    ["1", "Constante de temps", "τ = 10 kΩ × 100 µF\n= 10⁴ Ω × 10⁻⁴ F = 1 s"],
    ["2", "Tension après τ", "u_{C} = 0,632 × 12 V = 7,6 V"],
    ["3", "Durée de charge", "5τ = 5 × 1 s = 5 s"],
    ["4", "Courant de départ", "I_{0} = 12 V / 10 kΩ\n= 1,2 mA"],
  ];
  S.forEach((st, i) => {
    const x = 0.5 + i * 2.27;
    card(s, x, 4.42, 2.15, 1.12);
    badge(s, x + 0.1, 4.5, st[0], 0.34);
    txt(s, st[1], { x: x + 0.5, y: 4.5, w: 1.6, h: 0.34, fontSize: 11, bold: true, valign: "middle" });
    txt(s, st[2], { x: x + 0.1, y: 4.88, w: 1.98, h: 0.6, fontSize: 11.5, bold: true, valign: "middle" });
  });
}

// ============================== 4. MESURER τ · APPLICATIONS · TICKET DE SORTIE
{
  const s = slide("Mesurer τ à l'oscilloscope et le retrouver dans les appareils",
    "Cette diapositive relie la charge RC à la mesure. Sur l'écran affiché, CH1 est à 2 V/div et la base de temps à 1 ms/div. Le palier final est à 5 divisions → U = 10 V. 63 % de U = 6,3 V (≈ 3,2 div). Le temps entre le début de la charge et le point à 63 % vaut 2 div × 1 ms/div = 2 ms → τ = 2 ms. Si R est connue (par exemple 1 kΩ), on en déduit C = τ / R = 2 µF  : on contrôle ainsi un condensateur au marquage illisible.\n" +
    "Réglages : couplage DC (sinon la courbe est déformée), masse placée en bas de l'écran, base de temps choisie pour voir au moins 5τ, signal carré du générateur comme source (il charge puis décharge le condensateur à chaque période).\n" +
    "Sécurité : un condensateur peut rester chargé après la coupure. Celui d'un flash atteint environ 300 V. On le décharge avec une résistance adaptée avant d'intervenir, jamais avec un tournevis.\n" +
    "Ticket de sortie (5 min, seul, sans la fiche ; ramasser pour préparer la séance suivante). Réponses : 1) τ = 2,2·10³ Ω × 470·10⁻⁶ F = 1,03 s. 2) 5τ ≈ 5,2 s. 3) u_C = 0,632 × 9 V = 5,7 V.\n" +
    "Retour à la question de départ : le flash se recharge à travers une résistance, il lui faut environ 5τ pour être prêt.");
  s.addImage({ path: "fig_oscillo_demo.png", x: 0.5, y: 0.92, w: 4.55, h: 3.2 });
  frame(s, 5.25, 0.95, 4.25, 1.85);
  txt(s, "Méthode des 63 %", { x: 5.4, y: 1.0, w: 4.0, h: 0.3, fontSize: 13, bold: true, color: BLUE });
  s.addText(expand([
    { text: "Régler : couplage DC, masse en bas, base de temps pour voir 5τ.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "Lire U sur le palier : 5 div × 2 V/div = 10 V.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "Calculer 63 % de U : 6,3 V.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "Lire le temps à 63 % : 2 div × 1 ms/div → τ = 2 ms.", options: { bullet: { type: "number" } } },
  ]), { x: 5.4, y: 1.33, w: 4.0, h: 1.42, fontFace: F, fontSize: 11, color: K, margin: 0, valign: "top", paraSpaceAfter: 2 });
  life(s, 5.25, 2.92, 4.25, 1.38, [
    "Reset d'un microcontrôleur : le délai τ laisse à l'alimentation le temps de se stabiliser.",
    "Minuterie d'escalier, relais temporisé, anti-rebond de bouton.",
    "Sécurité : un condensateur reste chargé après coupure (flash ≈ 300 V).",
  ], 10);
  frame(s, 0.5, 4.38, 9.0, 1.18);
  txt(s, "Ticket de sortie : seul·e, 5 minutes, sans la fiche", { x: 0.65, y: 4.44, w: 8.7, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
  [["1", "R = 2,2 kΩ, C = 470 µF : τ = ?"], ["2", "Combien de temps pour être chargé ?"], ["3", "U = 9 V : que vaut u_{C} après τ ?"]].forEach((q, i) => {
    const x = 0.65 + i * 2.95;
    badge(s, x, 4.86, q[0], 0.34);
    txt(s, q[1], { x: x + 0.42, y: 4.8, w: 2.45, h: 0.5, fontSize: 11.5, valign: "middle" });
  });
  txt(s, "Puis : fiche d'exercices N°1 à N°7.", { x: 0.65, y: 5.3, w: 8.7, h: 0.22, fontSize: 10, italic: true, color: GR });
}

pres.writeFile({ fileName: "out/Charge du condensateur – présentation.pptx" }).then(() => console.log("deck ok"));
