// Présentations ETML (REGLES 5) : format 16:10, Arial, couleurs ETML, bande bleue à droite avec le logo blanc,
// « Section électronique » et numéro de page ; masques TITRE et CONTENU ; typographie française (moteur/typo.js) ;
// aides de mise en page (cartes, badges, listes, « Dans la vraie vie », tableaux, liens) ;
// diapositives de fin : exercices → page interactive → vidéo.
//
// Utilisation : node moteur/deck.js <config.json>
//   config : { donnees: <json de la séance>, diapositives: <fichier .slides.js>, titre, version, date (facultative), travail, videos, sortie }
//   Le fichier de diapositives exporte une fonction (E) => { … } qui reçoit les briques ci-dessous.
// Les images sont lues dans le dossier « travail » (figures, logos, captures, couvertures).
"use strict";
const path = require("path"), fs = require("fs");
const MODULES = [path.join(__dirname, "..", "node_modules"), "/opt/npm-tools/node_modules"];
const need = (m) => { try { return require(m); } catch (e) { for (const d of MODULES) { try { return require(path.join(d, m)); } catch (e2) {} } throw e; } };
const pptxgen = need("pptxgenjs"), JSZip = need("jszip");
const { TY, TYR, TYROWS } = require("./typo.js");

// largeur et hauteur en pixels d'une image PNG ou JPEG
function taille(f) {
  const b = fs.readFileSync(f);
  if (b.readUInt32BE(0) === 0x89504e47) return [b.readUInt32BE(16), b.readUInt32BE(20)];
  let i = 2;
  while (i < b.length) {
    const m = b[i + 1], len = b.readUInt16BE(i + 2);
    if (m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc) return [b.readUInt16BE(i + 7), b.readUInt16BE(i + 5)];
    i += 2 + len;
  }
  throw new Error("taille inconnue : " + f);
}
// rapport hauteur / largeur arrondi à 5 décimales (comme les anciens ratios.json)
const RATIO = new Proxy({}, { get: (o, f) => { const [w, h] = taille(f); return Math.round(h / w * 1e5) / 1e5; } });
// dimensions en pixels des images dont le nom correspond au motif (ex. /^eq_.*\.png$/)
function tailles(motif) {
  const r = {};
  for (const f of fs.readdirSync(".").filter(n => motif.test(n)).sort()) r[f] = taille(f);
  return r;
}

function creer(cfg) {
  process.chdir(cfg.travail);
  const DATA = cfg.donnees;
  const pres = new pptxgen();
  pres.defineLayout({ name: "ETML1610", width: 10, height: 6.25 });
  pres.layout = "ETML1610";
  pres.author = "Gaël Lemoine";
  pres.company = "ETML – Section électronique";
  pres.title = cfg.titre;
  pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };

  const NAVY = "242852", BLUE = "297FD5", LBLUE = "ACCBF9", TINT = "E8EFFB";
  const K = NAVY, GR = "5A6478", RED = "EE0000";
  const F = "Arial";
  const MATIERE = DATA.MATIERE;
  const TOPIC = MATIERE + " · " + cfg.titre;
  const CLASSE = DATA.CLASSE, ANNEE = DATA.ANNEE, CHAMP = DATA.CHAMP;
  const DATE_US = cfg.date || DATA.DATE_US, VERSION = cfg.version;   // date propre au fichier (seance.yaml, dates) ou date de la séance
  const FLOYDP = (chap, p) => DATA.FLOYD_PAGES[chap + "-" + p] || DATA.FLOYD[String(chap)][0];   // le lien ouvre le chapitre (REGLES 6)
  const LZURL = (c) => DATA.EDGE + DATA.LZ[c][2];   // lien propre à chaque LZ (donné par Gaël) ; microsoft-edge: sinon PowerPoint pour Windows perd l'ancre
  const LOGO_BAND = "logo_white_v.png";
  const NOMBRES = ["", "Une", "Deux", "Trois", "Quatre", "Cinq", "Six", "Sept"];

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
      { text: { text: `${DATA.EDITEUR} · ${DATE_US} · version ${VERSION}`, options: { x: 4.6, y: 5.66, w: 4.3, h: 0.3, fontFace: F, fontSize: 11, color: NAVY, align: "right", margin: 0 } } },
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
    const at = s.addText.bind(s), ash = s.addShape.bind(s), ai = s.addImage.bind(s), atb = s.addTable.bind(s), an = s.addNotes.bind(s);
    s.addText = (t, o) => at(TYR(t), fx(o)); s.addShape = (sh, o) => ash(sh, fx(o));
    s.addImage = (o) => ai(fx(o, true)); s.addTable = (r, o) => atb(TYROWS(r), fx(o)); s.addNotes = (n) => an(TY(n));
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
  function lines(str, base) {
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
    s.addText(expand(TY(title)), { x: 0.5, y: 0.25, w: 9.0, h: 0.55, fontFace: F, fontSize: 23, bold: true, color: NAVY, margin: 0, valign: "middle", fit: "shrink" });
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
  // ---------------------------------------------------------------- diapositive de titre (REGLES 5)
  // o = { titre, sousTitre, objectifs: [texte ou runs], question, indice, references: [runs], dessin: (s) => {…}, notes }
  // Cartouche : classe, année, matière et champ (lien FutureMEM), sauf cours hors réforme ; références si la séance en a.
  function titreSlide(o) {
    const s = pres.addSlide({ masterName: "TITRE" });
    squeeze(s, 0.6, 9.5, 8.9);
    txt(s, MATIERE.toUpperCase(), { x: 0.6, y: 0.4, w: 5.4, h: 0.3, fontSize: 12, bold: true, color: BLUE, charSpacing: 1 });
    txt(s, o.titre, { x: 0.6, y: 0.7, w: 5.4, h: 1.05, fontSize: 28, bold: true, color: NAVY, valign: "middle" });
    if (o.sousTitre) txt(s, o.sousTitre, { x: 0.6, y: 1.78, w: 5.4, h: 0.4, fontSize: 12.5, color: GR });
    txt(s, "À la fin de la leçon, je suis capable de…", { x: 0.6, y: 2.25, w: 5.4, h: 0.3, fontSize: 13.5, bold: true });
    const n = o.objectifs.length, pas = n > 4 ? 0.38 : 0.42;
    o.objectifs.forEach((t, i) => {
      const y = 2.62 + i * pas;
      badge(s, 0.6, y + 0.03, String(i + 1), 0.3);
      s.addText(typeof t === "string" ? [{ text: t }] : t, { x: 1.02, y, w: 5.0, h: pas - 0.04, fontFace: F, fontSize: n > 4 ? 12 : 12.5, color: K, margin: 0, valign: "middle" });
    });
    frame(s, 6.15, 0.55, 3.35, 2.6);
    txt(s, "Question de départ", { x: 6.3, y: 0.63, w: 3.1, h: 0.3, fontSize: 13, bold: true, color: BLUE });
    txt(s, o.question, { x: 6.3, y: 0.97, w: 3.1, h: 1.6, fontSize: 11.5 });
    if (o.indice) txt(s, o.indice, { x: 6.3, y: 2.62, w: 3.1, h: 0.42, fontSize: 10, italic: true, color: GR });
    if (o.dessin) o.dessin(s);
    card(s, 0.6, 4.5, 8.9, 1.0);
    const cart = [{ text: `Classe ${CLASSE} · ${ANNEE} · ${MATIERE}` + (DATA.HORS_REFORME ? "" : " · champ "), options: { bold: true } }];
    if (!DATA.HORS_REFORME) cart.push({ text: CHAMP, options: { bold: true, hyperlink: { url: DATA.EDGE + DATA.FUTUREMEM_CHAMP, tooltip: "Champ d'apprentissage sur FutureMEM" } } });
    if (o.references && o.references.length) {
      cart.push({ text: "", options: { breakLine: true } }, { text: "Références : ", options: { color: K } });
      o.references.forEach((r, i) => { if (i) cart.push({ text: " · ", options: { color: K } }); cart.push(r); });
    } else if (DATA.HORS_REFORME) {
      cart.push({ text: "", options: { breakLine: true } }, { text: "Cours hors réforme", options: { color: GR, italic: true } });
    }
    s.addText(cart, { x: 0.8, y: 4.55, w: 8.5, h: 0.9, fontFace: F, fontSize: 11, color: NAVY, margin: 0, valign: "middle", paraSpaceAfter: 3 });
    if (o.notes) s.addNotes(o.notes);
    return s;
  }

  // ---------------------------------------------------------------- équations (REGLES 3.2)
  // eqImg / eqName : une image d'équation (figures.py) qui devient, avec cfg.equations = "omml", une équation PowerPoint
  // éditable ; l'image reste en secours (mc:Fallback) pour les lecteurs qui ne lisent pas les équations (LibreOffice…).
  const EQS = [];
  const OMML = cfg.equations === "omml";
  function eqName(src, sz, color, w, h) {
    if (!OMML) return undefined;
    EQS.push({ src, sz: sz || 2400, color: color || NAVY, w: (w || 0) * 72, h: (h || 0) * 72 });
    return "EQ:" + (EQS.length - 1);
  }
  // PowerPoint affiche l'équation éditable à sa taille de police, centrée, sans la réduire au cadre (contrairement à l'image
  // de secours, seule visible dans LibreOffice et l'aperçu claude.ai). Premier bornage grossier ici ; la taille finale est
  // calculée par omml.py (ajuster : mesure réelle en Cambria Math, espaces des opérateurs compris) au moment d'écrire le fichier.
  function eqTaille(src, sz, w, h) {
    const fr = (src.match(/\\f\{/g) || []).length;
    const car = src.replace(/\\(?:f|u|cdot|Delta|approx|Omega|mu|times|bar|sqrt)\b/g, "X").replace(/\\[a-zA-Z]+/g, "").replace(/[{}_^\s]/g, "").length;
    const maxH = Math.floor(h * 72 / (fr ? 2.6 : 1.3) * 100);
    const maxW = Math.floor(w * KSQ * 72 / (0.55 * car * (fr ? 0.6 : 1)) * 100);
    const ok = Math.min(sz || 2400, maxH, maxW);
    return ok;
  }
  function eqImg(s, file, src, x, y, w, maxH, sz, color) {
    let h = w * RATIO[file];
    if (maxH && h > maxH) { w = maxH / RATIO[file]; h = maxH; }
    sz = eqTaille(src, sz, w, h);
    const o = { path: file, x, y, w, h }, nm = eqName(src, sz, color, w, h);
    if (nm) o.objectName = nm;
    s.addImage(o);
    return h;
  }
  function remplacerEquations(x, maths) {
    return x.replace(/<p:pic>((?:(?!<p:pic>)[\s\S])*?)<\/p:pic>/g, (pic, inner) => {
      const m = inner.match(/<p:cNvPr id="(\d+)" name="EQ:(\d+)"/);
      if (!m) return pic;
      const xfrm = inner.match(/<a:xfrm[\s\S]*?<\/a:xfrm>/)[0];
      const sp = `<p:sp><p:nvSpPr><p:cNvPr id="${m[1]}" name="Équation ${+m[2] + 1}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>` +
        `<p:spPr>${xfrm}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>` +
        `<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"><a:noAutofit/></a:bodyPr><a:lstStyle/>` +
        `<a:p><a:pPr algn="ctr"/><a14:m><m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">` +
        `<m:oMathParaPr><m:jc m:val="centerGroup"/></m:oMathParaPr>${maths[+m[2]]}</m:oMathPara></a14:m><a:endParaRPr lang="fr-CH"/></a:p></p:txBody></p:sp>`;
      return `<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">` +
        `<mc:Choice xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" Requires="a14">${sp}</mc:Choice>` +
        `<mc:Fallback>${pic.replace(/ name="EQ:\d+"/, ` name="Équation ${+m[2] + 1} (image)"`)}</mc:Fallback></mc:AlternateContent>`;
    });
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
  const LINK = (label, url, tip) => ({ text: label, options: { hyperlink: { url, tooltip: tip || "Ouvrir le lien" } } });
  const NEXTEC = (key, label) => LINK(label || DATA.NEXTEC[key][1], DATA.NEXTEC[key][0], "Ouvrir le chapitre dans nextecmedia");
  const FLOYDL = (chap, label, p) => LINK(label, FLOYDP(chap, p), "Floyd, chapitre " + chap + " sur Teams : aller ensuite à la page " + p);
  const LZL = (c) => LINK(c, LZURL(c), c + " sur FutureMEM");

  // ============================== fin de présentation : exercices → page interactive → vidéo (v1.3, demande de Gaël du 11/16/2026)
  const KSQ = (8.9 - 0.5) / (9.5 - 0.5);                      // compression horizontale de squeeze() (zone utile à gauche du bandeau)
  const PNGURI = (f) => "data:image/png;base64," + fs.readFileSync(f).toString("base64");
  const ARROW = { text: "▶ ", options: { color: BLUE, bold: true } };
  function exoSlide(code, url, items, situ, cons, lifeLines, notes) {
    const s = slide(`S'exercer : fiche ${code}`, notes);
    items.forEach(([n, t, d], i) => {
      const y = 0.95 + i * 0.58;
      badge(s, 0.5, y + 0.06, n, 0.4);
      txt(s, t, { x: 1.02, y, w: 4.45, h: 0.3, fontSize: 12.5, bold: true, valign: "middle" });
      txt(s, d, { x: 1.02, y: y + 0.29, w: 4.45, h: 0.24, fontSize: 10, color: GR, valign: "middle" });
    });
    card(s, 5.7, 0.95, 3.8, 2.05);
    txt(s, "La situation", { x: 5.85, y: 1.02, w: 3.5, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, situ, { x: 5.85, y: 1.36, w: 3.5, h: 1.58, fontSize: 11 });
    frame(s, 5.7, 3.12, 3.8, 1.38);
    txt(s, cons, { x: 5.85, y: 3.2, w: 3.5, h: 0.84, fontSize: 11 });
    s.addText([ARROW, LINK(`Ouvrir la fiche ${code} sur Teams`, url, "Fiche d'exercices sur Teams")],
      { x: 5.85, y: 4.1, w: 3.5, h: 0.3, fontFace: F, fontSize: 11.5, bold: true, color: NAVY, margin: 0, valign: "middle" });
    life(s, 0.5, 4.65, 9.0, 0.9, lifeLines, 10.5);
    return s;
  }
  // Phase « contenu » (cfg.medias === false) : la capture, la vidéo et les liens de la page et de la vidéo sont remplacés
  // par un emplacement provisoire ; ils arrivent en phase « medias » (REGLES 10).
  const MEDIAS = cfg.medias !== false;
  function provisoire(s, x, y, w, h, texte) {
    card(s, x, y, w, h);
    txt(s, texte, { x: x + 0.2, y, w: w - 0.4, h, fontSize: 12, italic: true, color: GR, align: "center", valign: "middle" });
  }
  function pageSlide(num, file, url, art, shot, steps, lifeLines, notes) {
    const s = slide(`Page interactive ${num} : comprendre, puis s'exercer`, notes);
    const r = 1290 / 1800, h = 3.42, w = h / r;
    frame(s, 0.5, 0.95, 5.05, 3.56);
    if (MEDIAS) s.addImage({ path: shot, x: 0.5 + (5.05 - w) / 2, y: 1.02, w, h });
    else provisoire(s, 0.6, 1.05, 4.85, 3.36, `Capture de la page interactive ${num} : ajoutée en phase médias.`);
    card(s, 5.75, 0.95, 3.75, 1.22);
    txt(s, "Chaque étape, en deux temps", { x: 5.9, y: 1.0, w: 3.5, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    txt(s, [{ text: "Comprendre : ", options: { bold: true } }, { text: "une animation reprise de la présentation, avec pause et étapes.", options: { breakLine: true } },
      { text: "À toi : ", options: { bold: true } }, { text: "un exercice corrigé tout de suite, avec l'explication." }],
      { x: 5.9, y: 1.3, w: 3.5, h: 0.84, fontSize: 10.5, paraSpaceAfter: 3 });
    txt(s, "Les étapes", { x: 5.75, y: 2.25, w: 3.75, h: 0.28, fontSize: 12, bold: true, color: NAVY });
    bullets(s, steps, { x: 5.75, y: 2.55, w: 3.75, h: 1.36, fontSize: 10.5 }, true);
    frame(s, 5.75, 3.95, 3.75, 0.56);
    // sans artefact (art vide : demande de Gaël du 11/24/2026), seul le lien SharePoint est donné
    if (MEDIAS) s.addText(art ? [ARROW, LINK(`Ouvrir la page ${num} sur Teams`, url, file + " : à ouvrir dans Edge ou Chrome"), { text: "", options: { breakLine: true } },
      { text: "version en ligne : ", options: { color: GR, bold: false } }, LINK("artefact claude.ai", art, "Page en ligne (une fois partagée)")] :
      [ARROW, LINK(`Ouvrir la page ${num} sur Teams`, url, file + " : à ouvrir dans Edge ou Chrome")],
      { x: 5.9, y: 3.97, w: 3.5, h: 0.52, fontFace: F, fontSize: 10.5, bold: true, color: NAVY, margin: 0, valign: "middle" });
    else txt(s, "Liens Teams et artefact : phase médias", { x: 5.9, y: 3.97, w: 3.5, h: 0.52, fontSize: 10.5, italic: true, color: GR, valign: "middle" });
    life(s, 0.5, 4.65, 9.0, 0.9, lifeLines, 10.5);
    return s;
  }
  function videoSlide(num, file, url, cover, dur, chapters, lifeLines, notes) {
    const s = slide(`Animation ${num} : toute la leçon en ${dur}`, notes);
    const w = 5.6 * KSQ, h = w * 9 / 16;
    if (MEDIAS) {
      s.addMedia({ type: "video", path: path.join(cfg.videos, file), x: 0.5, y: 0.95, w, h, cover: PNGURI(cover) });
      s.addText([{ text: "En diaporama, clique sur l'image pour lancer la vidéo. · ", options: { color: GR } }, LINK("La vidéo sur Teams", url, file)],
        { x: 0.5, y: 0.95 + h + 0.07, w: 5.6, h: 0.3, fontFace: F, fontSize: 10.5, color: NAVY, margin: 0, valign: "middle" });
    } else {
      provisoire(s, 0.5, 0.95, w, h, `Vidéo ${num} : ajoutée en phase médias.`);
    }
    txt(s, (NOMBRES[chapters.length] || String(chapters.length)) + " démonstrations", { x: 6.3, y: 0.95, w: 3.2, h: 0.3, fontSize: 12.5, bold: true, color: BLUE });
    chapters.forEach(([t, d], i) => {
      const y = 1.32 + i * 0.6;
      badge(s, 6.3, y + 0.05, String(i + 1), 0.36);
      txt(s, t, { x: 6.76, y, w: 2.75, h: 0.28, fontSize: 11.5, bold: true, valign: "middle" });
      txt(s, d, { x: 6.76, y: y + 0.27, w: 2.75, h: 0.24, fontSize: 9.5, color: GR, valign: "middle" });
    });
    life(s, 0.5, 4.65, 9.0, 0.9, lifeLines, 10.5);
    return s;
  }

  // Symbole CEI 60617-12 d'une porte NON-ET : rectangle « & » + cercle de négation
  function nandCEI(s, x, y, sc) {
    sc = sc || 1;
    const w = 0.85 * sc, h = 1.05 * sc, L = 0.32 * sc;
    [0.28, 0.77].forEach(f => s.addShape(pres.shapes.LINE, { x: x - L, y: y + h * f, w: L, h: 0, line: { color: K, width: 1.5 } }));
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: K, width: 1.75 } });
    txt(s, "&", { x, y: y + 0.05, w, h: 0.38 * sc, fontSize: 17, bold: true, align: "center" });
    const d = 0.14 * sc;
    s.addShape(pres.shapes.OVAL, { x: x + w, y: y + h / 2 - d / 2, w: d, h: d, fill: { color: "FFFFFF" }, line: { color: K, width: 1.5 } });
    s.addShape(pres.shapes.LINE, { x: x + w + d, y: y + h / 2, w: L, h: 0, line: { color: K, width: 1.5 } });
    txt(s, "A", { x: x - L - 0.25, y: y + h * 0.28 - 0.13, w: 0.2, h: 0.26, fontSize: 12, bold: true, align: "right" });
    txt(s, "B", { x: x - L - 0.25, y: y + h * 0.77 - 0.13, w: 0.2, h: 0.26, fontSize: 12, bold: true, align: "right" });
    txt(s, "Y", { x: x + w + d + L + 0.05, y: y + h / 2 - 0.13, w: 0.2, h: 0.26, fontSize: 12, bold: true });
  }

  // pptxgenjs écrit un <a:pPr> par run : on ne garde que le premier de chaque paragraphe (sinon la puce disparaît)
  function ecrire(sortie) {
    return pres.write({ outputType: "nodebuffer" }).then(async (buf) => {
    const zip = await JSZip.loadAsync(buf);
    // taille réelle du cadre de chaque équation, lue dans le XML final (squeeze() a pu le comprimer) : omml.py y ajuste le corps
    const slides = Object.keys(zip.files).filter(n => /^ppt\/slides\/slide\d+\.xml$/.test(n));
    for (const name of slides) {
      const x = await zip.file(name).async("string");
      for (const m of x.matchAll(/name="EQ:(\d+)"[\s\S]*?<a:ext cx="(\d+)" cy="(\d+)"/g)) {
        EQS[+m[1]].w = +m[2] / 12700; EQS[+m[1]].h = +m[3] / 12700;
      }
    }
    const maths = EQS.length ? JSON.parse(require("child_process").execFileSync("python3", [path.join(__dirname, "omml.py")],
      { input: JSON.stringify(EQS.map(e => [e.src, e.color, e.sz, e.w, e.h])), cwd: path.join(__dirname, "..") }).toString()) : [];
    for (const name of Object.keys(zip.files).filter(n => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
      let x = await zip.file(name).async("string");
      x = x.replace(/<a:p>([\s\S]*?)<\/a:p>/g, (m, inner) => {
        let first = true;
        inner = inner.replace(/<a:pPr\b[^>]*\/>|<a:pPr\b[^>]*>[\s\S]*?<\/a:pPr>/g, (pp) => { if (first) { first = false; return pp; } return ""; });
        return "<a:p>" + inner + "</a:p>";
      });
      if (maths.length) x = remplacerEquations(x, maths);
      zip.file(name, x);
    }
    const clean = new JSZip();
    for (const n of Object.keys(zip.files)) if (!zip.files[n].dir) clean.file(n, await zip.file(n).async("nodebuffer"), { createFolders: false });
    fs.writeFileSync(sortie, await clean.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
    console.log("ok", path.basename(sortie));
    });
  }

  return { pres, DATA, NAVY, BLUE, LBLUE, TINT, K, GR, RED, F, MATIERE, TOPIC, CLASSE, ANNEE, CHAMP, DATE_US, VERSION, LZURL, LOGO_BAND, TY, TYR, TYROWS, squeeze, R, lines, expand, slide, txt, card, frame, badge, img, bullets, life, boxTitle, cell, H, BORDER, LINK, NEXTEC, FLOYDP, FLOYDL, LZL, KSQ, PNGURI, ARROW, exoSlide, pageSlide, videoSlide, nandCEI, tailles, eqImg, eqName, titreSlide, ecrire };
}

module.exports = creer;

if (require.main === module) {
  const cfg = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
  cfg.donnees = JSON.parse(fs.readFileSync(cfg.donnees, "utf-8"));
  const E = creer(cfg);
  require(path.resolve(cfg.diapositives))(E);
  E.ecrire(cfg.sortie);
}
