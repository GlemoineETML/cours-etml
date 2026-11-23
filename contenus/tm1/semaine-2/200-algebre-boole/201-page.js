// ================================================================ leçons animées de la page 201 (présentation 200)
// Sortie S, entrées A, B, C (REGLES 3.4). Briques : moteur/pages/common.js (lesson, gateAt, TX, pill, ease, prog…).

// barre de négation au-dessus d'un texte SVG centré en x (largeur w), à la hauteur y
const BAR = (x, y, w, o = {}) => `<line x1="${x - w / 2}" y1="${y}" x2="${x + w / 2}" y2="${y}" style="stroke:${o.color || "var(--ink)"};stroke-width:${o.sw || 3};opacity:${o.op != null ? o.op : 1}"/>`;
// cercle de négation sur une entrée de porte placée par gateAt (le rectangle commence 50 unités après inX)
const NEGIN = (g, i, s) => `<circle cx="${g.inX + 50 * s - 7 * s}" cy="${g.inY[i]}" r="${7 * s}" style="fill:var(--surface);stroke:var(--ink);stroke-width:2.5"/>`;

// ---------------------------------------------------------------- L1 règles 1 à 8 sur une porte (diapos 6 et 7)
const L1R = [   // [porte, entrée 2 : "0", "1", "A" ou "nA", résultat affiché, équation]
  ["OU", "0", "A", "A + 0 = A"], ["OU", "1", "1", "A + 1 = 1"], ["ET", "0", "0", "A · 0 = 0"], ["ET", "1", "A", "A · 1 = A"],
  ["OU", "A", "A", "A + A = A"], ["OU", "nA", "1", "A + Ā = 1"], ["ET", "A", "A", "A · A = A"], ["ET", "nA", "0", "A · Ā = 0"],
];
lesson("L1", {
  dur: 40, label: "Animation : une porte OU puis une porte ET reçoivent A sur une entrée et 0, 1, A ou l'inverse de A sur l'autre ; la sortie illustre les règles 1 à 8",
  steps: [
    [0, "Règle 1 : un OU avec une entrée à 0. Quand A change, S suit A : l'entrée à 0 ne change rien."],
    [5, "Règle 2 : un OU avec une entrée à 1. La sortie reste à 1, quelle que soit A."],
    [10, "Règle 3 : un ET avec une entrée à 0. La sortie reste bloquée à 0."],
    [15, "Règle 4 : un ET avec une entrée à 1. La porte laisse passer A : c'est un signal de validation."],
    [20, "Règles 5 et 7 : A sur les deux entrées. Le OU et le ET redonnent simplement A."],
    [30, "Règles 6 et 8 : A et son inverse. Le OU donne toujours 1, le ET toujours 0 : l'un des deux vaut toujours 1, jamais les deux."],
  ],
  draw(t) {
    const k = Math.min(7, Math.floor(t / 5)), u = t - 5 * k, a = u < 2.5 ? 0 : 1;
    const [key, e2, res, eq] = L1R[k];
    const b = e2 === "0" ? 0 : e2 === "1" ? 1 : e2 === "A" ? a : 1 - a;
    const s = FN[key](a, b);
    const lab2 = e2 === "nA" ? "Ā" : e2;
    let h = '<svg viewBox="0 0 960 360">';
    const g = gateAt(key, a, b, s, 120, 60, 1.7, { labels: ["A", lab2], out: "S" });
    h += g.svg;
    h += TX(140, 40, "règle " + (k + 1), { size: 22, bold: true, color: "var(--muted)" });
    h += pill(60, g.inY[0], a) + pill(60, g.inY[1], b);
    h += TX(620, 120, eq, { size: 40, bold: true, color: "var(--head)" });
    h += TX(620, 180, `A = ${a}  →  S = ${s}`, { size: 26, mono: true });
    h += TX(620, 230, res === "A" ? "S suit A : l'entrée 2 ne change rien." : `S reste à ${res}, quelle que soit A.`, { size: 20, color: "var(--muted)" });
    // petite frise des 8 règles
    for (let i = 0; i < 8; i++) h += `<rect x="${100 + i * 95}" y="310" width="85" height="30" rx="6" style="fill:${i === k ? "var(--one)" : "var(--surface)"};stroke:var(--line);stroke-width:2"/>` +
      TX(142 + i * 95, 331, String(i + 1), { size: 16, anchor: "middle", bold: true, color: i === k ? "#fff" : "var(--muted)" });
    return h + "</svg>";
  },
});

// ---------------------------------------------------------------- L2 vérifier la distributivité par la table (diapo 5)
const L2C = [["C", (c, b, a) => c], ["B", (c, b, a) => b], ["A", (c, b, a) => a], ["B + C", (c, b, a) => b | c], ["A · (B + C)", (c, b, a) => a & (b | c)],
  ["A · B", (c, b, a) => a & b], ["A · C", (c, b, a) => a & c], ["A · B + A · C", (c, b, a) => (a & b) | (a & c)]];
const L2W = [50, 50, 50, 100, 140, 90, 90, 160];
lesson("L2", {
  dur: 26, label: "Animation : la table de vérité de la distributivité se remplit ligne par ligne, puis les deux colonnes finales sont comparées",
  steps: [
    [0, "Pour vérifier A · (B + C) = A · B + A · C, on écrit toutes les combinaisons de C, B et A : 8 lignes, dans l'ordre du comptage binaire."],
    [3, "Une colonne par morceau de l'équation : d'abord B + C, puis A · (B + C), puis A · B, A · C et leur somme."],
    [19, "On compare les deux colonnes finales, ligne par ligne : elles sont identiques. La loi est vérifiée."],
  ],
  draw(t) {
    const rows = bits(3), x0 = 70, y0 = 30, rh = 34, nl = clamp(Math.floor((t - 3) / 2) + 1, 0, 8);
    let h = '<svg viewBox="0 0 960 400">', x = x0;
    const xs = L2W.map((w) => { const v = x; x += w; return v; });
    const cmp = t >= 19;
    L2C.forEach(([nm], j) => {
      const fin = j === 4 || j === 7;
      h += `<rect x="${xs[j]}" y="${y0}" width="${L2W[j]}" height="${rh}" style="fill:${fin && cmp ? "var(--one)" : "var(--tint)"};stroke:var(--line);stroke-width:1.5"/>`;
      h += TX(xs[j] + L2W[j] / 2, y0 + 23, nm, { size: 16, bold: true, anchor: "middle", color: fin && cmp ? "#fff" : "var(--head)" });
    });
    rows.forEach(([c, b, a], i) => {
      const y = y0 + rh * (i + 1);
      L2C.forEach(([, f], j) => {
        h += `<rect x="${xs[j]}" y="${y}" width="${L2W[j]}" height="${rh}" style="fill:var(--surface);stroke:var(--line);stroke-width:1.5"/>`;
        if (j < 3 || i < nl) { const v = f(c, b, a); h += TX(xs[j] + L2W[j] / 2, y + 23, String(v), { size: 17, anchor: "middle", mono: true, bold: j >= 3 && v, color: j >= 3 && v ? "var(--one)" : "var(--ink)" }); }
      });
      if (cmp && i < 8) h += okMark(xs[7] + L2W[7] + 26, y + rh / 2, true, 10);
    });
    if (cmp) h += TX(x0 + 365, 385, "colonnes identiques sur les 8 lignes : la loi est vraie", { size: 18, bold: true, anchor: "middle", color: "var(--ok)" });
    return h + "</svg>";
  },
});

// ---------------------------------------------------------------- L3 le convoyeur : simplifier, contrôler, dessiner (diapos 14 et 15)
lesson("L3", {
  dur: 30, label: "Animation : l'équation du convoyeur S = A · B + A · B barré · C se simplifie en S = A · (B + C), puis passe de quatre portes à deux",
  steps: [
    [0, "Le cahier des charges donne deux termes : « en marche et bouteille pleine », ou « en marche, pas de bouteille pleine, et vidange »."],
    [6, "A est commun aux deux termes : on le met en évidence (distributivité)."],
    [12, "Dans la parenthèse, on reconnaît la règle 11 : B + B̄ · C = B + C."],
    [18, "Résultat : S = A · (B + C). Câblé tel quel, il fallait 4 portes sur 4 CI ; il en reste 2."],
  ],
  draw(t) {
    let h = '<svg viewBox="0 0 960 380">';
    const L = [[0, "S = A · B + A · ", "B", " · C", ""], [6, "S = A · (B + ", "B", " · C)", "distributivité"], [12, "S = A · (B + C)", "", "", "règle 11"]];
    L.forEach(([t0, s1, sb, s2, why], i) => {
      const op = prog(t, t0, t0 + 1.2); if (op <= 0) return;
      const y = 60 + i * 64, fs = 34;
      h += `<g style="opacity:${op}">` + `<text x="40" y="${y}" font-size="${fs}" font-weight="700" style="fill:var(--head)">${s1}<tspan style="text-decoration:overline">${sb}</tspan>${s2}</text>`;
      if (why) h += TX(560, y - 6, why, { size: 20, italic: true, color: "var(--blue)" });
      h += "</g>";
    });
    const op = prog(t, 18, 19.5);
    if (op > 0) {
      h += `<g style="opacity:${op}">`;
      h += `<rect x="40" y="230" width="380" height="120" rx="12" style="fill:var(--tint)"/>` + TX(60, 266, "Câblé tel quel", { size: 20, bold: true, color: "var(--muted)" }) +
        TX(60, 300, "NON, ET, ET à 3 entrées, OU", { size: 18 }) + TX(60, 330, "4 portes · 4 CI", { size: 22, bold: true });
      const go = gateAt("OU", null, null, null, 470, 230, 0.7, { labels: ["B", "C"], out: "" });
      const g0 = gateAt("ET", null, null, null, 0, 0, 0.7, { labels: ["A", ""], out: "S" });
      const ga = gateAt("ET", null, null, null, go.outX - g0.inX, go.outY - g0.inY[1], 0.7, { labels: ["A", ""], out: "S" });
      h += go.svg + ga.svg;
      h += TX(700, 345, "2 portes · 2 CI", { size: 22, bold: true, anchor: "middle", color: "var(--one)" });
      h += "</g>";
    }
    return h + "</svg>";
  },
});

// ---------------------------------------------------------------- L4 De Morgan (diapos 11 et 12)
function dmForm(x, y, p, vers) {
  // vers = "ET" : barre(A · B) → Ā + B̄ ; vers = "OU" : barre(A + B) → Ā · B̄ ; p de 0 à 1
  const fs = 56, xa = x, xo = x + 70, xb = x + 140;
  const op1 = vers === "ET" ? "·" : "+", op2 = vers === "ET" ? "+" : "·";
  let h = TX(x - 170, y, "S =", { size: fs, bold: true, color: "var(--head)" });
  h += TX(xa, y, "A", { size: fs, bold: true, anchor: "middle", italic: true }) + TX(xb, y, "B", { size: fs, bold: true, anchor: "middle", italic: true });
  h += TX(xo, y, op1, { size: fs, bold: true, anchor: "middle", op: 1 - prog(p, 0.4, 0.7) });
  h += TX(xo, y, op2, { size: fs, bold: true, anchor: "middle", color: "var(--one)", op: prog(p, 0.4, 0.7) });
  // la barre se casse : une seule barre (0) → deux barres sur A et B (1)
  const q = prog(p, 0, 0.4), yb = y - 50;
  h += `<line x1="${lerp(xa - 22, xa - 22, q)}" y1="${yb}" x2="${lerp(xb + 22, xa + 22, q)}" y2="${yb}" style="stroke:var(--ink);stroke-width:4"/>`;
  h += `<line x1="${lerp(xa - 22, xb - 22, q)}" y1="${yb}" x2="${xb + 22}" y2="${yb}" style="stroke:var(--ink);stroke-width:4"/>`;
  return h;
}
lesson("L4", {
  dur: 24, label: "Animation : la barre au-dessus de A · B se casse en deux barres et le point devient un plus ; même chose pour A + B ; puis les symboles CEI équivalents",
  steps: [
    [0, "Première forme : la barre couvre A · B. On la casse : chaque variable garde sa propre barre, et le · devient +."],
    [8, "Seconde forme : la barre couvre A + B. On la casse, et le + devient ·. « Ni A ni B » : c'est l'autorisation des arrêts d'urgence."],
    [16, "Sur un schéma, les deux dessins représentent la même porte : un NON-ET est un OU dont les entrées sont inversées."],
  ],
  draw(t) {
    let h = '<svg viewBox="0 0 960 360">';
    if (t < 16) {
      const vers = t < 8 ? "ET" : "OU", p = prog(t, vers === "ET" ? 2 : 10, vers === "ET" ? 6 : 14);
      h += dmForm(380, 170, p, vers);
      h += TX(480, 290, p > 0.7 ? "casse la barre, change le signe" : "la barre couvre toute l'expression", { size: 24, anchor: "middle", color: p > 0.7 ? "var(--one)" : "var(--muted)", bold: p > 0.7 });
    } else {
      const g1 = gateAt("NON-ET", null, null, null, 60, 80, 1.3, { labels: ["A", "B"], out: "S" });
      const g2 = gateAt("OU", null, null, null, 520, 80, 1.3, { labels: ["A", "B"], out: "S" });
      h += g1.svg + g2.svg + NEGIN(g2, 0, 1.3) + NEGIN(g2, 1, 1.3);
      h += TX(470, 180, "=", { size: 60, bold: true, anchor: "middle", color: "var(--one)" });
      h += TX(480, 330, "NON-ET  =  OU avec les entrées inversées", { size: 24, bold: true, anchor: "middle", color: "var(--head)" });
    }
    return h + "</svg>";
  },
});
