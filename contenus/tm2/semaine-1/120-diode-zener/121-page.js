// ================================================================ leçons animées et dessins de la page 121 (présentation 120 Diode et diode Zener)
// Tout est écrit en déclarations de fonction : les exercices de la page les appellent avant que ce bloc ne soit lu.
// Modèles identiques à figures.py (courbes de la présentation et de la fiche 130).

// ---------------------------------------------------------------- modèles
function uDiode(i) { return 1.9 * 0.02585 * Math.log(i / 10e-9 + 1) + 2.0 * i; }          // diode Si d'exercice
function iDiode(u) {                                                                       // inverse, par dichotomie
  if (u <= 0) return 0;
  let a = 0, b = 1;
  for (let k = 0; k < 60; k++) { const m = (a + b) / 2; if (uDiode(m) > u) b = m; else a = m; }
  return a;
}
function uZener(i) { return 5.05 + 10 * i - 0.08 * Math.exp(-i / 1e-3); }                 // Zener 5V1 d'exercice
function iZener(ue, r) {                                                                   // courant de la Zener avec R en série
  if (ue <= uZener(0)) return 0;
  let a = 0, b = 0.2;
  for (let k = 0; k < 60; k++) { const m = (a + b) / 2; if (r * m + uZener(m) > ue) b = m; else a = m; }
  return a;
}

// ---------------------------------------------------------------- briques de dessin
function diodeV(x, y1, y2, o) {
  // diode verticale (CEI 60617-5) entre y1 et y2 ; o.sens « bas » (anode en haut) ou « haut » ; o.genre « diode », « zener », « led »
  o = o || {};
  const ym = (y1 + y2) / 2, t = o.t || 15, s = o.sens === "haut" ? -1 : 1, ya = ym - s * t, yk = ym + s * t;
  let g = `<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" style="stroke:var(--ink);stroke-width:3"/>` +
    `<polygon points="${x - t},${ya} ${x + t},${ya} ${x},${yk}" style="fill:var(--surface);stroke:var(--ink);stroke-width:3;stroke-linejoin:round"/>` +
    `<line x1="${x}" y1="${ya}" x2="${x}" y2="${yk}" style="stroke:var(--ink);stroke-width:3"/>` +
    `<line x1="${x - t}" y1="${yk}" x2="${x + t}" y2="${yk}" style="stroke:var(--ink);stroke-width:4"/>`;
  if (o.genre === "zener") g += `<line x1="${x + t}" y1="${yk}" x2="${x + t}" y2="${yk - s * 8}" style="stroke:var(--ink);stroke-width:4"/>`;
  if (o.genre === "led") [0, 12].forEach((d) => {
    const x0 = x + t + 4, y0 = ym - 2 + d;
    g += `<line x1="${x0}" y1="${y0}" x2="${x0 + 16}" y2="${y0 - 12}" style="stroke:var(--ink);stroke-width:2.2"/>` +
      `<polygon points="${x0 + 19},${y0 - 14} ${x0 + 10},${y0 - 12} ${x0 + 16},${y0 - 5}" style="fill:var(--ink)"/>`;
  });
  return g;
}
function NOMI(l, i) { return `${l}<tspan font-size="0.72em" dy="0.3em" font-style="normal">${i}</tspan>`; }
function resV(x, y1, y2, nom, val) {
  const ym = (y1 + y2) / 2;
  return `<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" style="stroke:var(--ink);stroke-width:3"/>` +
    `<rect x="${x - 10}" y="${ym - 26}" width="20" height="52" style="fill:var(--surface);stroke:var(--ink);stroke-width:3"/>` +
    (nom ? TX(x - 20, ym - 4, nom, { size: 17, anchor: "end", italic: true, color: "var(--head)" }) : "") +
    (val ? TX(x - 20, ym + 18, val, { size: 15, anchor: "end", color: "var(--muted)" }) : "");
}
function sourceV(x, y1, y2, val) {
  const ym = (y1 + y2) / 2;
  return `<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" style="stroke:var(--ink);stroke-width:3"/>` +
    `<circle cx="${x}" cy="${ym}" r="20" style="fill:var(--surface);stroke:var(--ink);stroke-width:3"/>` +
    `<line x1="${x}" y1="${ym - 20}" x2="${x}" y2="${ym + 20}" style="stroke:var(--ink);stroke-width:3"/>` +
    TX(x - 28, ym + 6, val, { size: 16, anchor: "end", color: "var(--muted)" }) +
    TX(x - 14, y1 + 26, "+", { size: 20, bold: true, anchor: "middle", color: "var(--bad)" });
}
function flecheU(x, yh, yb, nom) {   // flèche de tension bleue, du + (haut) vers le − (bas), nom à droite
  return `<line x1="${x}" y1="${yh + 6}" x2="${x}" y2="${yb - 12}" style="stroke:var(--blue);stroke-width:3"/>` +
    `<polygon points="${x - 7},${yb - 14} ${x + 7},${yb - 14} ${x},${yb}" style="fill:var(--blue)"/>` +
    TX(x + 10, (yh + yb) / 2 + 6, nom, { size: 17, italic: true, color: "var(--blue)" });
}
function porteurs(x0, x1, y0, y1, n, genre, graine, dx) {
  // porteurs sur une grille (pas de 30 px) légèrement décalée : jamais deux porteurs l'un sur l'autre
  const pas = 30, cols = Math.max(1, Math.floor((x1 - x0 - 16) / pas)), rows = Math.max(1, Math.floor((y1 - y0 - 16) / pas));
  const larg = cols * pas;
  let g = "", k = 0;
  for (let c = 0; c < cols; c++) for (let r = 0; r < rows; r++) {
    const h = ((Math.sin(graine * 12.9898 + (c * 7 + r) * 78.233) * 43758.5453) % 1 + 1) % 1;
    if (h > 0.55) continue;                                     // environ une case sur deux occupée
    let x = x0 + 8 + pas / 2 + c * pas + (h - 0.27) * 10, y = y0 + 8 + pas / 2 + r * pas + (h - 0.27) * 8;
    if (dx) x = x0 + 8 + (((x - x0 - 8) + dx) % larg + larg) % larg;
    k++;
    g += genre === "trou"
      ? `<circle cx="${x}" cy="${y}" r="9" style="fill:var(--surface);stroke:var(--bad);stroke-width:2.2"/>` + TX(x, y + 5, "+", { size: 13, bold: true, anchor: "middle", color: "var(--bad)" })
      : `<circle cx="${x}" cy="${y}" r="9" style="fill:var(--blue);stroke:#242852;stroke-width:1.5"/>` + TX(x, y + 5, "−", { size: 13, bold: true, anchor: "middle", color: "#fff" });
  }
  return g;
}
function jonctionG(x, y, w, h, k, t, flux) {
  // barreau PN ; k : largeur relative de la zone de déplétion (1 au repos) ; flux : porteurs qui traversent
  const zw = 60 * k, xm = x + w / 2, xg = xm - zw / 2, xd = xm + zw / 2, dx = flux ? (t || 0) * 40 : 0;
  let g = `<rect x="${x}" y="${y}" width="${xg - x}" height="${h}" style="fill:#E8EFFB"/>` +
    `<rect x="${xd}" y="${y}" width="${x + w - xd}" height="${h}" style="fill:#ACCBF9"/>` +
    `<rect x="${xg}" y="${y}" width="${zw}" height="${h}" style="fill:#fff;stroke:#5A6478;stroke-dasharray:5 4"/>`;
  g += porteurs(x, xg, y, y + h, Math.max(3, Math.round((xg - x) / 26)), "trou", 3, dx);
  g += porteurs(xd, x + w, y, y + h, Math.max(3, Math.round((x + w - xd) / 26)), "e", 5, -dx);
  for (let j = 0; j < 3; j++) {
    const yy = y + 22 + j * (h - 44) / 2;
    g += `<rect x="${xg + zw * 0.25 - 8}" y="${yy - 8}" width="16" height="16" style="fill:#fff;stroke:#242852;stroke-width:1.6"/>` + TX(xg + zw * 0.25, yy + 5, "−", { size: 13, bold: true, anchor: "middle", color: "#242852" }) +
      `<rect x="${xd - zw * 0.25 - 8}" y="${yy - 8}" width="16" height="16" style="fill:#fff;stroke:#C81E1E;stroke-width:1.6"/>` + TX(xd - zw * 0.25, yy + 5, "+", { size: 13, bold: true, anchor: "middle", color: "#C81E1E" });
  }
  g += `<rect x="${x}" y="${y}" width="${w}" height="${h}" style="fill:none;stroke:#242852;stroke-width:2.5"/>` +
    TX(x + 6, y - 8, "zone p", { size: 16, bold: true, color: "var(--head)" }) + TX(x + w - 6, y - 8, "zone n", { size: 16, bold: true, anchor: "end", color: "var(--head)" });
  return g;
}
function pileG(cx, yb, direct) {
  const xp = direct ? cx - 18 : cx + 18, xn = direct ? cx + 18 : cx - 18;
  return `<polyline points="20,95 6,95 6,${yb} ${cx - 18},${yb}" style="fill:none;stroke:var(--ink);stroke-width:2.5"/>` +
    `<polyline points="440,95 454,95 454,${yb} ${cx + 18},${yb}" style="fill:none;stroke:var(--ink);stroke-width:2.5"/>` +
    `<line x1="${xp}" y1="${yb - 20}" x2="${xp}" y2="${yb + 20}" style="stroke:var(--ink);stroke-width:2.5"/>` +
    `<line x1="${xn}" y1="${yb - 11}" x2="${xn}" y2="${yb + 11}" style="stroke:var(--ink);stroke-width:7"/>` +
    TX(xp, yb - 26, "+", { size: 20, bold: true, anchor: "middle", color: "var(--bad)" }) + TX(xn, yb - 26, "−", { size: 20, bold: true, anchor: "middle", color: "var(--head)" });
}
function caracG(x, y, w, h, u, o) {
  // caractéristique directe (0 à 0,9 V, 0 à 40 mA) et point de fonctionnement à u ; o.marques : repères 10 et 30 mA
  o = o || {};
  const X = (v) => x + w * v / 0.9, Y = (i) => y + h - h * Math.min(i, 0.04) / 0.04;
  let g = "";
  for (let v = 0; v <= 0.9001; v += 0.1) g += `<line x1="${X(v)}" y1="${y}" x2="${X(v)}" y2="${y + h}" style="stroke:var(--line);stroke-width:1"/>` + TX(X(v), y + h + 20, vir(v, 1), { size: 13, anchor: "middle", color: "var(--muted)" });
  for (let i = 0; i <= 0.04001; i += 0.005) g += `<line x1="${x}" y1="${Y(i)}" x2="${x + w}" y2="${Y(i)}" style="stroke:var(--line);stroke-width:1"/>` + (Math.round(i * 1e3) % 10 === 0 ? TX(x - 8, Y(i) + 5, Math.round(i * 1e3), { size: 13, anchor: "end", color: "var(--muted)" }) : "");
  let pts = [];
  for (let k = 0; k <= 900; k++) { const v = k / 1000, i = iDiode(v); if (i > 0.04) break; pts.push([X(v), Y(i)]); }
  g += `<polyline points="${pts.map((p) => p.join(",")).join(" ")}" style="fill:none;stroke:var(--blue);stroke-width:3.5"/>`;
  g += `<line x1="${x}" y1="${y + h}" x2="${x + w}" y2="${y + h}" style="stroke:var(--ink);stroke-width:2"/><line x1="${x}" y1="${y}" x2="${x}" y2="${y + h}" style="stroke:var(--ink);stroke-width:2"/>`;
  g += TX(x + w, y + h + 42, "U<tspan font-size=\"0.7em\" dy=\"0.3em\" font-style=\"normal\">F</tspan><tspan dy=\"-0.3em\" font-style=\"normal\"> [V]</tspan>", { size: 15, anchor: "end", italic: true, color: "var(--head)" });
  g += TX(x + 6, y - 6, "I<tspan font-size=\"0.7em\" dy=\"0.3em\" font-style=\"normal\">F</tspan><tspan dy=\"-0.3em\" font-style=\"normal\"> [mA]</tspan>", { size: 15, italic: true, color: "var(--head)" });
  (o.marques || []).forEach(([i, op]) => {
    const v = uDiode(i);
    g += `<g style="opacity:${op}"><line x1="${x}" y1="${Y(i)}" x2="${X(v)}" y2="${Y(i)}" style="stroke:var(--bad);stroke-width:1.8;stroke-dasharray:6 4"/>` +
      `<line x1="${X(v)}" y1="${Y(i)}" x2="${X(v)}" y2="${y + h}" style="stroke:var(--bad);stroke-width:1.8;stroke-dasharray:6 4"/>` +
      TX(X(v) - 10, Y(i) - 8, Math.round(i * 1e3) + " mA → " + vir(v, 2) + " V", { size: 14, bold: true, anchor: "end", color: "var(--bad)" }) + "</g>";
  });
  if (u != null) {
    const i = iDiode(u);
    g += `<line x1="${X(u)}" y1="${Y(i)}" x2="${X(u)}" y2="${y + h}" style="stroke:var(--head);stroke-width:1.5;stroke-dasharray:4 4"/>` +
      `<circle cx="${X(u)}" cy="${Y(i)}" r="8" style="fill:var(--bad);stroke:var(--surface);stroke-width:2"/>`;
  }
  return g;
}
function zenerG(x, y, ue, us, iz) {
  // protection d'entrée : source U_e, R1 = 2k2, Zener 5V1 vers la masse, sortie U_s
  const xs = x + 60, xr = x + 220, xo = x + 330, yh = y + 20, yn = y + 130, yb = y + 240;
  let g = sourceV(xs, yh, yb, vir(ue, 0) + " V") + flecheU(xs + 32, yh + 30, yb - 30, "U<tspan font-size=\"0.7em\" dy=\"0.3em\" font-style=\"normal\">e</tspan>");
  g += `<polyline points="${xs},${yh} ${xr},${yh}" style="fill:none;stroke:var(--ink);stroke-width:3"/><polyline points="${xs},${yb} ${xo},${yb}" style="fill:none;stroke:var(--ink);stroke-width:3"/>`;
  g += resV(xr, yh, yn, NOMI("R", 1), "2k2") + diodeV(xr, yn, yb, { sens: "haut", genre: "zener" });
  g += TX(xr - 34, yn + 62, "5V1", { size: 15, anchor: "end", color: "var(--muted)" });
  g += `<line x1="${xr}" y1="${yn}" x2="${xo}" y2="${yn}" style="stroke:var(--ink);stroke-width:3"/>` +
    `<circle cx="${xr}" cy="${yn}" r="5" style="fill:var(--ink)"/><circle cx="${xr}" cy="${yb}" r="5" style="fill:var(--ink)"/>` +
    `<circle cx="${xo}" cy="${yn}" r="6" style="fill:var(--surface);stroke:var(--ink);stroke-width:2.5"/><circle cx="${xo}" cy="${yb}" r="6" style="fill:var(--surface);stroke:var(--ink);stroke-width:2.5"/>`;
  g += flecheU(xo + 24, yn + 12, yb - 10, "U<tspan font-size=\"0.7em\" dy=\"0.3em\" font-style=\"normal\">s</tspan>");
  g += TX(xo + 34, (yn + yb) / 2 + 34, vir(us, 2) + " V", { size: 17, bold: true, color: "var(--head)" });
  if (iz > 5e-5) g += `<circle cx="${xr}" cy="${(yn + yb) / 2}" r="26" style="fill:none;stroke:var(--bad);stroke-width:2.5;stroke-dasharray:4 3"/>` +
    TX(xr + 32, (yn + yb) / 2 - 22, "elle conduit", { size: 14, bold: true, color: "var(--bad)" });
  return g;
}
function ledCircuitG(x, y, r, direct, e, col) {
  const xs = x + 70, xb = x + 250, yh = y + 20, ym = y + 130, yb = y + 240;
  let g = sourceV(xs, yh, yb, "24 V") + flecheU(xs + 32, yh + 30, yb - 30, "U");
  g += `<polyline points="${xs},${yh} ${xb},${yh}" style="fill:none;stroke:var(--ink);stroke-width:3"/><polyline points="${xs},${yb} ${xb},${yb}" style="fill:none;stroke:var(--ink);stroke-width:3"/>`;
  g += r > 0 ? resV(xb, yh, ym, NOMI("R", 1), { 470: "470", 1000: "1k", 2200: "2k2", 4700: "4k7" }[r] || String(r)) : `<line x1="${xb}" y1="${yh}" x2="${xb}" y2="${ym}" style="stroke:var(--ink);stroke-width:3"/>` + TX(xb - 14, (yh + ym) / 2 + 5, "sans R", { size: 15, anchor: "end", color: "var(--bad)", bold: true });
  if (!e.casse && e.i > 0) {
    const op = clamp(e.i / 0.02, 0.15, 1);
    g += `<circle cx="${xb}" cy="${(ym + yb) / 2}" r="${30 + 14 * op}" style="fill:${col};opacity:${0.35 * op}"/>`;
  }
  g += diodeV(xb, ym, yb, { sens: direct ? "bas" : "haut", genre: "led" });
  g += TX(xb - 52, (ym + yb) / 2 + 6, NOMI("D", 1), { size: 17, italic: true, anchor: "end", color: "var(--head)" });
  if (e.casse) g += `<line x1="${xb - 30}" y1="${(ym + yb) / 2 - 30}" x2="${xb + 30}" y2="${(ym + yb) / 2 + 30}" style="stroke:var(--bad);stroke-width:5"/>` +
    `<line x1="${xb + 30}" y1="${(ym + yb) / 2 - 30}" x2="${xb - 30}" y2="${(ym + yb) / 2 + 30}" style="stroke:var(--bad);stroke-width:5"/>` +
    TX(xb + 42, (ym + yb) / 2 + 6, e.mot || "détruite", { size: 16, bold: true, color: "var(--bad)" });
  return g;
}

// ---------------------------------------------------------------- L1 la jonction (diapos 3 et 4)
lesson("L1", {
  dur: 26, label: "Animation : une jonction PN au repos, puis en sens direct (la zone de déplétion devient mince et le courant passe), puis en sens inverse (la zone s'élargit, pas de courant)",
  steps: [
    [0, "Au repos : à la frontière, il ne reste que des ions fixes. Cette zone de déplétion n'a pas de porteurs libres : elle isole."],
    [6, "Sens direct : le + sur la zone p. La zone devient mince ; au-dessus de ≈ 0,7 V, les porteurs la traversent : le courant passe."],
    [14, "Sens inverse : le + sur la zone n. Les porteurs sont tirés loin de la frontière, la zone s'élargit : pas de courant."],
    [21, "À retenir : une diode conduit de l'anode (zone p) vers la cathode (zone n), et bloque dans l'autre sens."],
  ],
  draw(t) {
    let k = 1, direct = true, flux = false;
    if (t >= 6 && t < 14) { k = 1 - 0.7 * prog(t, 6, 8); flux = t > 8; }
    if (t >= 14) { direct = false; k = 1 + 1.4 * prog(t, 14, 16); }
    let s = '<svg viewBox="0 0 960 380"><g transform="translate(250,30)">' + jonctionG(20, 30, 420, 130, k, t, flux);
    if (t >= 6) s += pileG(230, 220, direct);
    if (flux) s += `<line x1="140" y1="0" x2="300" y2="0" style="stroke:var(--bad);stroke-width:4"/><polygon points="300,-9 318,0 300,9" style="fill:var(--bad)"/>` +
      TX(230, -10, "courant", { size: 16, bold: true, anchor: "middle", color: "var(--bad)" });
    if (t >= 14 && t < 21) s += TX(230, 300, "pas de courant", { size: 20, bold: true, anchor: "middle", color: "var(--head)" });
    s += "</g>";
    const r = prog(t, 21, 22);
    if (r > 0) s += `<rect x="90" y="330" width="780" height="42" rx="8" style="fill:#242852;opacity:${r}"/>` +
      TX(480, 358, "Anode vers cathode : elle conduit. Dans l'autre sens : elle bloque.", { size: 18, bold: true, anchor: "middle", color: "#fff", op: r });
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L2 la caractéristique (diapos 7 et 8)
lesson("L2", {
  dur: 24, label: "Animation : le point de fonctionnement d'une diode au silicium monte le long de sa caractéristique ; presque rien sous 0,6 volt, puis le courant monte très vite",
  steps: [
    [0, "On augmente la tension U<sub>F</sub> de la diode et on lit le courant I<sub>F</sub>."],
    [3, "Jusqu'à ≈ 0,6 V : presque pas de courant. La barrière de la jonction n'est pas franchie."],
    [10, "Au-dessus du seuil, le courant monte très vite pour une petite hausse de tension."],
    [17, "10 mA → 0,70 V ; 30 mA → 0,79 V. Le courant triple, la tension monte d'à peine 0,1 V : d'où le modèle U<sub>F</sub> = 0,7 V."],
  ],
  draw(t) {
    const u = t < 3 ? 0 : (t < 17 ? 0.82 * prog(t, 3, 16) : null);
    let s = '<svg viewBox="0 0 960 380"><g transform="translate(260,20)">' +
      caracG(60, 10, 400, 290, u, { marques: [[10e-3, prog(t, 17, 18)], [30e-3, prog(t, 18.5, 19.5)]] }) + "</g>";
    if (u != null) {
      const i = iDiode(u);
      s += TX(780, 120, "U = " + vir(u, 2) + " V", { size: 20, bold: true, color: "var(--head)" }) +
        TX(780, 152, "I " + (i < 1e-4 ? "≈ 0" : "= " + vir(i * 1e3, 1)) + " mA", { size: 20, bold: true, color: "var(--bad)" });
    }
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L3 la Zener (diapos 11 et 13)
lesson("L3", {
  dur: 24, label: "Animation : la tension d'entrée monte de 0 à 24 volts ; la sortie suit l'entrée jusqu'à 5,1 volts, puis la Zener conduit et la sortie reste vers 5,1 volts",
  steps: [
    [0, "La protection d'entrée : R<sub>1</sub> en série, la Zener 5V1 branchée en inverse (cathode vers le +)."],
    [3, "Sous 5,1 V, la Zener est bloquée : aucun courant, R<sub>1</sub> ne prend rien. La sortie suit l'entrée."],
    [9, "Au-dessus de 5,1 V, la Zener claque : elle conduit et sa tension reste presque constante. R<sub>1</sub> prend la différence."],
    [19, "À 24 V : U<sub>s</sub> ≈ 5,1 V, R<sub>1</sub> prend ≈ 18,9 V. L'entrée du contrôleur est protégée."],
  ],
  draw(t) {
    const ue = 24 * prog(t, 3, 18), iz = iZener(ue, 2200), us = iz > 0 ? uZener(iz) : ue;
    let s = '<svg viewBox="0 0 960 380"><g transform="translate(40,40)">' + zenerG(0, 0, ue, us, iz) + "</g>";
    // courbe U_s(U_e) tracée au fur et à mesure
    const x0 = 560, y0 = 320, W = 340, H = 260, X = (v) => x0 + W * v / 24, Y = (v) => y0 - H * v / 12;
    s += `<line x1="${x0}" y1="${y0}" x2="${x0 + W}" y2="${y0}" style="stroke:var(--ink);stroke-width:2"/><line x1="${x0}" y1="${y0}" x2="${x0}" y2="${y0 - H}" style="stroke:var(--ink);stroke-width:2"/>`;
    [0, 6, 12, 18, 24].forEach((v) => { s += TX(X(v), y0 + 20, v, { size: 13, anchor: "middle", color: "var(--muted)" }); });
    [0, 5.1, 10].forEach((v) => { s += TX(x0 - 8, Y(v) + 5, vir(v, v % 1 ? 1 : 0), { size: 13, anchor: "end", color: "var(--muted)" }); });
    s += `<line x1="${x0}" y1="${Y(5.1)}" x2="${x0 + W}" y2="${Y(5.1)}" style="stroke:var(--muted);stroke-width:1.2;stroke-dasharray:5 4"/>`;
    s += TX(x0 + W, y0 + 40, "U<tspan font-size=\"0.7em\" dy=\"0.3em\" font-style=\"normal\">e</tspan><tspan dy=\"-0.3em\" font-style=\"normal\"> [V]</tspan>", { size: 15, anchor: "end", italic: true, color: "var(--head)" });
    s += TX(x0 + 6, y0 - H - 8, "U<tspan font-size=\"0.7em\" dy=\"0.3em\" font-style=\"normal\">s</tspan><tspan dy=\"-0.3em\" font-style=\"normal\"> [V]</tspan>", { size: 15, italic: true, color: "var(--head)" });
    const pts = [];
    for (let v = 0; v <= ue + 1e-9; v += 0.25) { const i = iZener(v, 2200); pts.push([X(v), Y(i > 0 ? uZener(i) : v)]); }
    if (pts.length > 1) s += `<polyline points="${pts.map((p) => p.join(",")).join(" ")}" style="fill:none;stroke:var(--bad);stroke-width:3.5"/>`;
    s += `<circle cx="${X(ue)}" cy="${Y(us)}" r="7" style="fill:var(--bad)"/>`;
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L4 la LED (diapos 14 et 15)
lesson("L4", {
  dur: 22, label: "Animation : une LED rouge et sa résistance sur 24 volts éclairent ; sans résistance la LED est détruite ; à l'envers elle reçoit 24 volts en inverse et peut claquer",
  steps: [
    [0, "Une LED rouge et R<sub>1</sub> = 2k2 sur 24 V : la LED prend ≈ 1,9 V, R<sub>1</sub> le reste. Environ 10 mA : la LED éclaire."],
    [6, "Sans R<sub>1</sub>, rien ne limite le courant : il dépasse vite I<sub>F</sub> max. La LED est détruite."],
    [12, "LED à l'envers : elle bloque, mais elle reçoit 24 V en inverse. Sa limite U<sub>R</sub> max n'est que de 5 V : elle peut claquer."],
    [18, "À retenir : une LED a toujours une résistance en série, et ne se branche jamais à l'envers sur une tension plus grande que 5 V."],
  ],
  draw(t) {
    let r = 2200, direct = true;
    if (t >= 6 && t < 12) r = 0;
    if (t >= 12) direct = t < 18 ? false : true;
    if (t >= 18) r = 2200;
    const casse = (t >= 7 && t < 12) || (t >= 13 && t < 18);
    const e = !direct ? { i: 0, casse, mot: "claquage" } : (r === 0 ? { i: Infinity, casse } : { i: (24 - 1.9) / r, casse: false });
    let s = '<svg viewBox="0 0 960 380"><g transform="translate(300,40)">' + ledCircuitG(0, 0, r, direct, e, "#E53935") + "</g>";
    if (t >= 12 && t < 18) s += TX(720, 190, "24 V en inverse > 5 V", { size: 18, bold: true, color: "var(--bad)" });
    if (t < 6 || t >= 18) s += TX(720, 190, "I ≈ 10 mA", { size: 18, bold: true, color: "var(--head)" });
    return s + "</svg>";
  },
});
