// ================================================================ leçons animées de la page 121 (présentation 120)
// Sortie S, entrées A, B, C, D (REGLES 3.4). V2 (11/27/2026) : la voiture électrique remplace la ligne de remplissage.

// ---------------------------------------------------------------- L1 la voiture électrique (diapositives 2 et 13)
// Entrées du fascicule (A = 0 ceinture bouclée, B = 1 sur P, C = 0 frein enfoncé, D = 1 service), voyant actif à 1 (Gaël, 11/27/2026) :
// S = B · (D + /(A + C)) ; S = 1 : LED allumée, démarrage autorisé. Scénario : [instant (s), changements]
const L1SC = [[0, { A: 1, B: 0, C: 1, D: 0 }], [5, { A: 0 }], [10, { B: 1 }], [15, { C: 0 }], [21, { C: 1 }], [25, { A: 1 }], [27, { D: 1 }], [32, { B: 0 }]];
const l1at = (u) => { const v = {}; for (const [t0, ch] of L1SC) if (u >= t0) Object.assign(v, ch); return v; };
const l1S = (v) => v.B & (v.D | (1 - (v.A | v.C)));
const L1CARD = [["B", "Sélecteur", (x) => (x ? "sur P" : "sur D (conduite)")], ["D", "Mode service", (x) => (x ? "actif" : "inactif")],
  ["A", "Ceinture", (x) => (x ? "débouclée" : "bouclée")], ["C", "Frein", (x) => (x ? "pédale relâchée" : "pédale enfoncée")]];
lesson("L1", {
  dur: 42, label: "Animation : la commande de démarrage d'une voiture électrique, avec les entrées A, B, C, D, trois portes (NON-OU, OU, ET), la LED entre S et GND, et le chronogramme",
  steps: [
    [0, "Chaque entrée donne un 0 ou un 1. Attention : la ceinture donne A = 0 quand elle est bouclée, le frein C = 0 quand la pédale est enfoncée. La LED s'allume quand S = 1."],
    [5, "Ceinture bouclée : A passe à 0. Le sélecteur n'est pas sur P (B = 0) : S = 0, la LED reste éteinte."],
    [10, "Sélecteur sur P : B = 1. Il manque encore le frein : la NON-OU donne 0, donc S = 0."],
    [15, "Pédale de frein enfoncée : C = 0. La NON-OU donne 1 (A = 0 et C = 0), l'OU donne 1, le ET donne S = 1 : la LED s'allume."],
    [21, "Frein relâché : C = 1. La NON-OU repasse à 0, S = 0 : la LED s'éteint."],
    [25, "Au garage, ceinture débouclée (A = 1). Le technicien active le mode service : D = 1 suffit à l'OU, et S = 1."],
    [32, "Sélecteur hors de P : B = 0. Même en mode service, S = 0 : sans P, pas de démarrage."],
    [37, "Le chronogramme garde la trace : S vaut 1 seulement quand B = 1, avec D = 1 ou A = C = 0."],
  ],
  draw(t) {
    const v = l1at(t), N = 1 - (v.A | v.C), O = v.D | N, S = l1S(v), sc = 0.7, dy = 97.52 * sc;
    const g1 = gateAt("NON-OU", v.A, v.C, N, 330, 152.5, sc, { labels: ["", ""], out: "" });
    const g2 = gateAt("OU", v.D, N, O, 510, g1.outY - dy, sc, { labels: ["", ""], out: "" });
    const g3 = gateAt("ET", v.B, O, S, 680, g2.outY - dy, sc, { labels: ["", ""], out: "" });
    const ROW = { B: 60, D: 120, A: g1.inY[0], C: 255 };
    const wS = (pts, x) => wireP(pts, x).replace(/stroke-width:(\d+)/, (m, w) => "stroke-width:" + w * sc);   // même épaisseur que les portes réduites
    let s = '<svg viewBox="0 0 960 462">';
    // entrées : une carte par capteur
    L1CARD.forEach(([n, nom, etat]) => {
      const y = ROW[n], x = v[n];
      s += `<rect x="16" y="${y - 23}" width="258" height="46" rx="8" style="fill:var(--surface);stroke:var(--line);stroke-width:1.5"/>`;
      s += TX(28, y - 4, nom, { size: 15, bold: true }) + TX(28, y + 15, etat(x), { size: 14, color: "var(--muted)" });
      s += TX(208, y + 7, n, { size: 20, bold: true, italic: true, anchor: "middle" }) + pill(244, y, x);
    });
    s += wS([[259, ROW.A], [g1.inX, g1.inY[0]]], v.A);
    s += wS([[259, ROW.C], [312, ROW.C], [312, g1.inY[1]], [g1.inX, g1.inY[1]]], v.C);
    s += wS([[259, ROW.D], [g2.inX - 16, ROW.D], [g2.inX - 16, g2.inY[0]], [g2.inX, g2.inY[0]]], v.D);
    s += wS([[259, ROW.B], [g3.inX - 16, ROW.B], [g3.inX - 16, g3.inY[0]], [g3.inX, g3.inY[0]]], v.B);
    s += wS([[g1.outX, g1.outY], [g2.inX, g2.inY[1]]], N) + wS([[g2.outX, g2.outY], [g3.inX, g3.inY[1]]], O);
    s += g1.svg + g2.svg + g3.svg;
    [[g1, 330, "74HC02"], [g2, 510, "74HC32"], [g3, 680, "74HC08"]].forEach(([g, X, ci]) => {
      s += TX(X + 129 * sc, g.outY + 58 * sc + 20, ci, { size: 13, anchor: "middle", color: "var(--muted)" });
    });
    // sortie S, résistance et LED vers GND (la LED s'allume quand S = 1)
    const xl = 905, yo = g3.outY, led = S === 1;
    s += wS([[g3.outX, yo], [xl, yo], [xl, yo + 12]], S) + TX((g3.outX + xl) / 2, yo - 10, "S", { size: 18, bold: true, italic: true, anchor: "middle" });
    s += `<line x1="${xl}" y1="${yo + 12}" x2="${xl}" y2="${yo + 100}" style="stroke:var(--ink);stroke-width:2.5"/>`;
    s += `<rect x="${xl - 7}" y="${yo + 12}" width="14" height="36" style="fill:var(--surface);stroke:var(--ink);stroke-width:2.2"/>` + TX(xl - 16, yo + 36, "R", { size: 15, italic: true, anchor: "end" });
    if (led) s += `<circle cx="${xl}" cy="${yo + 70}" r="24" style="fill:#FF5A3C;opacity:.3"/>`;
    s += `<polygon points="${xl - 12},${yo + 60} ${xl + 12},${yo + 60} ${xl},${yo + 80}" style="fill:${led ? "#FF5A3C" : "var(--surface)"};stroke:var(--ink);stroke-width:2"/>`;
    s += `<line x1="${xl - 12}" y1="${yo + 81}" x2="${xl + 12}" y2="${yo + 81}" style="stroke:var(--ink);stroke-width:2.6"/>` + TX(xl - 30, yo + 76, "LED", { size: 13, anchor: "end" });
    s += `<path d="M ${xl + 15} ${yo + 66} l 10 -8 m -4 0 h 4 v 4 M ${xl + 15} ${yo + 74} l 10 -8 m -4 0 h 4 v 4" style="fill:none;stroke:${led ? "#D0312D" : "var(--ink)"};stroke-width:1.6"/>`;
    s += masseG(xl, yo + 100, { fil: 0 });
    s += TX(870, 272, led ? "LED allumée : démarrage autorisé" : "LED éteinte", { size: 14, bold: led, anchor: "end", color: led ? "var(--bad)" : "var(--muted)" });
    // chronogramme
    s += TX(520, 288, "chronogramme", { size: 12, anchor: "middle", color: "var(--muted)" });
    const f = (k) => (u) => l1at(u)[k];
    s += traceG(120, 296, 800, [{ name: "A", f: f("A") }, { name: "B", f: f("B") }, { name: "C", f: f("C") }, { name: "D", f: f("D") },
      { name: "S", f: (u) => l1S(l1at(u)), color: "var(--one)" }], Math.min(t, 40), 40, { rh: 32, dt: 0.05 });
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- N°1 : chronogramme en direct de la porte choisie (diapo 12)
let gAuto = !REDUCE, gT = 0, gHist = [{ tm: 0, a: 0, b: 0 }], gNext = 2.5, gIdx = 0, gLast = null, gVis = true, gDrawn = 0;
const G_SEQ = [[0, 0], [0, 1], [1, 0], [1, 1]];   // (B, A) dans l'ordre de la table
function gSet(a, b) { ga = a; gb = b; gHist.push({ tm: gT, a, b }); while (gHist.length > 2 && gHist[1].tm < gT - 30) gHist.shift(); drawSim(); }
const gBtn = () => { $("g-auto").textContent = gAuto ? "❚❚ Arrêter la démonstration" : "▶ Démonstration automatique"; };
$("g-auto").onclick = () => { gAuto = !gAuto; gNext = gT + 0.8; gBtn(); }; gBtn();
$("g-a").onclick = () => { gAuto = false; gBtn(); gSet(1 - ga, gb); };
$("g-b").onclick = () => { gAuto = false; gBtn(); gSet(ga, 1 - gb); };
if ("IntersectionObserver" in window) new IntersectionObserver((es) => es.forEach((e) => { gVis = e.isIntersecting; gLast = null; }), { threshold: 0.1 }).observe($("g-chrono"));
function gChrono() {
  const W = 20, x0 = 60, x1 = 940, X = (tm) => x1 - (gT - tm) * (x1 - x0) / W, ws = gT - W, one = gk === "NON";
  const rows = [["A", (h) => h.a, "var(--ink)"], ["B", (h) => h.b, one ? "var(--line)" : "var(--ink)"], ["S", (h) => (one ? FN.NON(h.a) : FN[gk](h.a, h.b)), "var(--one)"]];
  let s = '<svg viewBox="0 0 960 186">';
  for (let k = Math.ceil(ws); k <= gT; k++) s += `<line x1="${X(k)}" y1="8" x2="${X(k)}" y2="176" style="stroke:var(--line);stroke-width:1;stroke-dasharray:2 5"/>`;
  rows.forEach(([nm, f, col], i) => {
    const yb = 18 + i * 56 + 40, yh = yb - 28;
    let e = gHist[0]; for (const h of gHist) if (h.tm <= ws) e = h;
    let v = f(e), d = `M ${x0} ${v ? yh : yb}`;
    for (const h of gHist) if (h.tm > ws) { const nv = f(h); if (nv !== v) { d += ` L ${X(h.tm)} ${v ? yh : yb} L ${X(h.tm)} ${nv ? yh : yb}`; v = nv; } }
    d += ` L ${x1} ${v ? yh : yb}`;
    s += TX(x0 - 14, yb - 6, nm, { size: 18, bold: true, italic: true, anchor: "end", color: i === 1 && one ? "var(--muted)" : "var(--ink)" }) +
      `<line x1="${x0}" y1="${yb}" x2="${x1}" y2="${yb}" style="stroke:var(--line)"/><path d="${d}" fill="none" style="stroke:${col};stroke-width:3;stroke-linejoin:round"/>`;
  });
  s += `<line x1="${x1}" y1="8" x2="${x1}" y2="176" style="stroke:var(--bad);stroke-width:2"/>` + TX(x1 - 6, 184, "maintenant", { size: 11, anchor: "end", color: "var(--bad)" });
  $("g-chrono").innerHTML = s + "</svg>";
}
function gLoop(ts) {
  if (gVis) {
    const dt = gLast == null ? 0 : Math.min(0.1, (ts - gLast) / 1000); gLast = ts; gT += dt;
    if (gAuto && gT >= gNext) { gIdx = (gIdx + 1) % 4; const [b, a] = G_SEQ[gIdx]; gSet(a, b); gNext += 2.5; }
    if (ts - gDrawn > 40) { gChrono(); gDrawn = ts; }
  }
  requestAnimationFrame(gLoop);
}
gChrono(); ready(() => requestAnimationFrame(gLoop));

// ---------------------------------------------------------------- L2 construire une table de vérité (diapo 3)
lesson("L2", {
  dur: 30, label: "Animation : la table de vérité d'une porte ET à trois entrées se remplit ligne par ligne, en comptant en binaire de 000 à 111",
  steps: [
    [0, "Une table de vérité donne la sortie pour toutes les combinaisons des entrées. Exemple : une porte ET à 3 entrées (74HC11), testée sur un banc."],
    [3, "Colonnes du poids fort au poids faible : C B A, puis la sortie S. Les lignes suivent le comptage binaire, de 000 à 111."],
    [16, "Pour ne rien oublier : A change à chaque ligne, B toutes les 2 lignes, C toutes les 4 lignes."],
    [24, "3 entrées : 2³ = 8 lignes. Avec n entrées, la table a 2ⁿ lignes."],
  ],
  draw(t) {
    const cr = t < 3 ? -1 : Math.min(7, Math.floor((t - 3) / 1.6)), bits = (r) => [(r >> 2) & 1, (r >> 1) & 1, r & 1], cur = cr < 0 ? [0, 0, 0] : bits(cr);
    const y = cur[0] & cur[1] & cur[2];
    let s = '<svg viewBox="0 0 960 370">';
    s += TX(140, 28, "banc de test", { size: 14, anchor: "middle", bold: true, color: "var(--muted)" });
    ["C", "B", "A"].forEach((n, i) => {
      const x = 70 + i * 70, v = cur[i];
      s += TX(x, 52, n, { size: 18, bold: true, italic: true, anchor: "middle" }) +
        `<rect x="${x - 14}" y="62" width="28" height="80" rx="14" style="fill:var(--line);stroke:var(--ink);stroke-width:1.5"/>` +
        `<circle cx="${x}" cy="${v ? 82 : 122}" r="12" style="fill:${v ? "var(--one)" : "var(--surface)"};stroke:var(--ink);stroke-width:2"/>` +
        TX(x, 170, v, { size: 22, bold: true, mono: true, anchor: "middle", color: v ? "var(--one)" : "var(--ink)" });
    });
    // porte ET à 3 entrées (CEI) et lampe
    ["C", "B", "A"].forEach((n, i) => {
      const yy = 76 + i * 26;
      s += `<line x1="276" y1="${yy}" x2="306" y2="${yy}" style="${wireStyle(cur[i])}"/>` + TX(268, yy + 5, n, { size: 15, bold: true, italic: true, anchor: "end" });
    });
    s += `<rect x="306" y="56" width="70" height="92" style="fill:var(--surface);stroke:var(--ink);stroke-width:3"/>` + TX(341, 86, "&amp;", { size: 22, bold: true, anchor: "middle" });
    s += `<line x1="376" y1="102" x2="408" y2="102" style="${wireStyle(y)}"/>` + lampG(424, 102, 13, y) + TX(424, 136, "S", { size: 15, bold: true, italic: true, anchor: "middle" });
    // tableau
    const tx = 520, cw = 70, ry = (r) => 64 + r * 36;
    ["C", "B", "A", "S"].forEach((n, i) => {
      s += `<rect x="${tx + i * cw}" y="28" width="${cw}" height="36" style="fill:var(--light);stroke:var(--line)"/>` + TX(tx + i * cw + cw / 2, 53, n, { size: 18, bold: true, anchor: "middle", color: "#242852" });
    });
    for (let r = 0; r < 8; r++) {
      const o = prog(t, 3 + r * 1.6, 3.6 + r * 1.6); if (o <= 0) continue;
      const b = bits(r), yv = b[0] & b[1] & b[2], hl = r === cr && t < 16;
      s += `<g style="opacity:${o}">`;
      [...b, yv].forEach((v, i) => {
        let fill = hl ? "var(--tint)" : "var(--surface)";
        const runLen = [4, 2, 1][i], phase = [21.4, 18.7, 16][i];
        if (i < 3 && t >= phase && Math.floor(r / runLen) % 2 === 1) fill = "rgba(41,127,213,.22)";
        s += `<rect x="${tx + i * cw}" y="${ry(r)}" width="${cw}" height="36" style="fill:${fill};stroke:var(--line)"/>` +
          TX(tx + i * cw + cw / 2, ry(r) + 25, v, { size: 20, mono: true, bold: i === 3 && v === 1, anchor: "middle", color: i === 3 && v ? "var(--one)" : "var(--ink)" });
      });
      if (hl) s += `<rect x="${tx}" y="${ry(r)}" width="${4 * cw}" height="36" style="fill:none;stroke:var(--blue);stroke-width:2.5"/>`;
      s += "</g>";
    }
    s += `<line x1="${tx + 3 * cw}" y1="28" x2="${tx + 3 * cw}" y2="${ry(8)}" style="stroke:var(--head);stroke-width:3"/>`;
    [["A : à chaque ligne", 16, 2], ["B : toutes les 2", 18.7, 1], ["C : toutes les 4", 21.4, 0]].forEach(([txt, t0, col], i) => {
      const o = prog(t, t0, t0 + 0.8); if (o <= 0) return;
      s += `<g style="opacity:${o}">` +
        TX(820, 110 + i * 60, txt, { size: 16, bold: true, color: "var(--blue)" }) + "</g>";
    });
    if (cr >= 0 && t < 24) s += TX(60, 230, `ligne ${cr} : C B A = ${cur.join(" ")}`, { size: 20, bold: true }) + TX(60, 262, `S = A · B · C = ${y}`, { size: 20, color: y ? "var(--one)" : "var(--ink)", bold: true });
    if (t >= 24) { const o = prog(t, 24, 25); s += `<g style="opacity:${o}">` + TX(60, 236, "3 entrées → 2³ = 8 lignes", { size: 26, bold: true, color: "var(--head)" }) + TX(60, 274, "n entrées → 2ⁿ lignes", { size: 22, color: "var(--head)" }) + "</g>"; }
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L3 lire un chronogramme (diapo 4)
let l3g = "ET";
const L3C = lesson("L3", {
  dur: 27, label: "Animation : un curseur parcourt le chronogramme intervalle par intervalle, lit A et B, et trouve S dans la table de vérité",
  extra: '<span class="muted">Porte :</span><span class="chips" id="l3-g"></span>',
  steps: [
    [0, "Le temps avance de gauche à droite. On découpe le chronogramme en intervalles : dans chacun, aucun signal ne change."],
    [2, "Pour chaque intervalle, on lit A et B, puis on cherche la ligne B A dans la table : elle donne S."],
    [12.4, "On continue jusqu'au bout. La courbe S obtenue est le chronogramme de sortie de la porte."],
    [23, "Si un seul intervalle ne correspond pas à la table, ce n'est pas cette porte : c'est la méthode de cet exercice."],
  ],
  draw(t) {
    const CA = D.CHRONO_A, CB = D.CHRONO_B, n = CA.length, x0 = 70, pw = 540 / n, CY = CA.map((a, i) => FN[l3g](a, CB[i]));
    const cur = t < 2 ? -1 : Math.min(n - 1, Math.floor((t - 2) / 2.6)), done = t >= 2 + n * 2.6;
    let s = '<svg viewBox="0 0 960 300">';
    if (cur >= 0 && !done) s += `<rect x="${x0 + cur * pw}" y="30" width="${pw}" height="232" style="fill:var(--tint);stroke:var(--blue);stroke-width:2"/>`;
    for (let i = 0; i <= n; i++) s += `<line x1="${x0 + i * pw}" y1="30" x2="${x0 + i * pw}" y2="262" style="stroke:var(--line);stroke-dasharray:3 4"/>`;
    for (let i = 0; i < n; i++) s += TX(x0 + i * pw + pw / 2, 22, i + 1, { size: 13, anchor: "middle", color: "var(--muted)" });
    [["A", CA, n, "var(--ink)"], ["B", CB, n, "var(--ink)"], ["S", CY, done ? n : cur + 1, "var(--one)"]].forEach(([nm, sig, upto, col], r) => {
      const yb = 100 + r * 75, yh = yb - 42;
      s += TX(x0 - 14, yb - 12, nm, { size: 20, bold: true, italic: true, anchor: "end" }) + `<line x1="${x0}" y1="${yb}" x2="${x0 + n * pw}" y2="${yb}" style="stroke:var(--line)"/>`;
      if (upto > 0) {
        let d = `M ${x0} ${sig[0] ? yh : yb}`;
        for (let i = 0; i < upto; i++) { const yy = sig[i] ? yh : yb; d += ` L ${x0 + i * pw} ${yy} L ${x0 + (i + 1) * pw} ${yy}`; }
        s += `<path d="${d}" fill="none" style="stroke:${col};stroke-width:3.2;stroke-linejoin:round"/>`;
      }
      if (r === 2 && upto < n) s += TX(x0 + upto * pw + 12, yb - 14, "?", { size: 20, bold: true, color: "var(--muted)" });
    });
    // table B A Y
    const tx = 690, cw = 64;
    s += TX(tx + 1.5 * cw, 22, `Porte ${D.GATES[l3g].nom}`, { size: 15, bold: true, anchor: "middle", color: "var(--head)" });
    ["B", "A", "S"].forEach((h, i) => { s += `<rect x="${tx + i * cw}" y="32" width="${cw}" height="34" style="fill:var(--light);stroke:var(--line)"/>` + TX(tx + i * cw + cw / 2, 56, h, { size: 18, bold: true, anchor: "middle", color: "#242852" }); });
    const row = cur >= 0 && !done ? CB[cur] * 2 + CA[cur] : -1;
    tdv(l3g).forEach((r, k) => {
      const y = 66 + k * 36;
      r.forEach((v, i) => { s += `<rect x="${tx + i * cw}" y="${y}" width="${cw}" height="36" style="fill:${k === row ? "var(--tint)" : "var(--surface)"};stroke:var(--line)"/>` + TX(tx + i * cw + cw / 2, y + 25, v, { size: 19, mono: true, anchor: "middle", bold: i === 2 && v === 1, color: i === 2 && v ? "var(--one)" : "var(--ink)" }); });
      if (k === row) s += `<rect x="${tx}" y="${y}" width="${3 * cw}" height="36" style="fill:none;stroke:var(--blue);stroke-width:2.5"/>`;
    });
    s += `<line x1="${tx + 2 * cw}" y1="32" x2="${tx + 2 * cw}" y2="210" style="stroke:var(--head);stroke-width:3"/>`;
    if (row >= 0) s += TX(tx + 1.5 * cw, 244, `intervalle ${cur + 1} : B A = ${CB[cur]} ${CA[cur]}`, { size: 16, anchor: "middle" }) +
      TX(tx + 1.5 * cw, 272, `→ S = ${CY[cur]}`, { size: 22, bold: true, anchor: "middle", color: CY[cur] ? "var(--one)" : "var(--head)" });
    return s + "</svg>";
  },
});
D.ORDER.filter((k) => k !== "NON").forEach((k) => {
  const b = document.createElement("button"); b.type = "button"; b.className = "chip"; b.textContent = D.GATES[k].nom; b.setAttribute("aria-pressed", k === l3g ? "true" : "false");
  b.onclick = () => { l3g = k; $("l3-g").querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", c.textContent === D.GATES[k].nom ? "true" : "false")); L3C.t = 0; L3C.dirty = true; };
  $("l3-g").appendChild(b);
});

// ---------------------------------------------------------------- L4 le démarrage sur breadboard (diapositives 13 et 14)
// Entrées : résistance de pull-up vers +5 V, interrupteur vers GND : fermé → 0 (ceinture bouclée, frein enfoncé), ouvert → 1.
// 74HC02 : A → 1A (2), C → 1B (3), 1Y (1) → 74HC32 1A (1) ; D → 1B (2) ; 1Y (3) → 74HC08 1A (1) ; B → 1B (2) ; 1Y (3) = S → R → LED → GND.
// Liaisons (REGLES 3.3) : point à chaque jonction en T, saut de fil à chaque croisement sans liaison.
const L4UNUSED = [[[8, 9, 11, 12], [5, 6]], [[9, 10, 12, 13], [4, 5]], [[9, 10, 12, 13], [4, 5]]];     // entrées inutilisées : [haut, bas]
const L4T = [0, 5, 10, 16, 22, 28, 34, 40, 46];

// contact à fermeture (CEI 60617-7) vertical entre y0 et y1 : languette fixe en haut, levier qui pivote en bas ; fermé : il touche la languette
function contact(x, y0, y1, ferme, c, k = 1) {
  const a = y0 + 8 * k, b = y1 - 8 * k, st = `stroke:${c};stroke-width:${2.4 * Math.min(k, 1.2)};stroke-linecap:round`;
  return `<line x1="${x}" y1="${y0}" x2="${x}" y2="${a}" style="${st}"/><line x1="${x}" y1="${a}" x2="${x + 8 * k}" y2="${a}" style="${st}"/>` +
    `<line x1="${x}" y1="${b}" x2="${x}" y2="${y1}" style="${st}"/><circle cx="${x}" cy="${b}" r="${2.2 * k}" style="fill:${c}"/>` +
    `<line x1="${x}" y1="${b}" x2="${x + (ferme ? 7 : 17) * k}" y2="${ferme ? a : a + 6 * k}" style="${st}"/>`;
}

// zoom sur une entrée : pull-up et interrupteur (étapes 1 et 2)
function l4zoom(t) {
  const ferme = t >= 5, v = ferme ? 0 : 1, x = 300, yn = 240;
  let s = '<svg viewBox="0 0 960 440">';
  s += TX(30, 34, "Zoom sur une entrée : résistance de pull-up et interrupteur", { size: 17, bold: true, color: "var(--head)" });
  s += alimG(x, 92, "+5 V") + `<line x1="${x}" y1="92" x2="${x}" y2="110" style="stroke:var(--ink);stroke-width:2.5"/>`;
  s += `<rect x="${x - 11}" y="110" width="22" height="70" style="fill:var(--surface);stroke:var(--ink);stroke-width:2.5"/>`;
  s += TX(x - 24, 140, "R", { size: 17, italic: true, anchor: "end" }) + TX(x - 24, 162, "10 kΩ", { size: 15, anchor: "end", color: "var(--muted)" });
  s += filP([[x, 180], [x, 280]], v) + liaison(x, yn, "var(--ink)", 5);
  s += filP([[x, yn], [600, yn]], v) + `<path d="M 600 ${yn - 7} L 614 ${yn} L 600 ${yn + 7} z" style="fill:${v ? "var(--one)" : "var(--zero)"}"/>`;
  s += TX(624, yn + 6, "vers l'entrée du CI", { size: 15, color: "var(--muted)" });
  s += TX(500, yn - 24, "entrée", { size: 15, anchor: "end", color: "var(--muted)" }) + pill(526, yn - 30, v);
  // interrupteur (contact à fermeture, CEI 60617-7) vers GND
  s += contact(x, 280, 352, ferme, "var(--ink)", 1.6);
  s += TX(x - 24, 306, "interrupteur", { size: 15, anchor: "end", color: "var(--muted)" }) + TX(x - 24, 326, ferme ? "fermé" : "ouvert", { size: 15, bold: true, anchor: "end" });
  s += masseG(x, 352);
  if (ferme) {   // courant : +5 V → R → interrupteur → GND
    s += `<path d="M ${x - 7} 200 L ${x} 214 L ${x + 7} 200 z" style="fill:var(--bad)"/>` + TX(x + 16, 212, '<tspan font-style="italic">I</tspan> = 0,5 mA', { size: 15, bold: true, color: "var(--bad)" });
  }
  s += TX(640, 110, ferme ? "Interrupteur fermé" : "Interrupteur ouvert", { size: 17, bold: true });
  s += TX(640, 138, ferme ? "courant dans la résistance : 0,5 mA" : "aucun courant dans la résistance", { size: 16 });
  s += TX(640, 164, ferme ? "entrée reliée à GND : 0" : "entrée tirée à +5 V : 1", { size: 16, bold: true, color: ferme ? "var(--ink)" : "var(--one)" });
  return s + "</svg>";
}

lesson("L4", {
  dur: 52, label: "Animation : une entrée avec résistance de pull-up, puis la commande de démarrage câblée sur breadboard (74HC02, 74HC32, 74HC08, quatre interrupteurs avec pull-up, LED entre S et GND)",
  steps: [
    [0, "Zoom sur une entrée : la résistance de pull-up R relie l'entrée à +5 V. Interrupteur ouvert : aucun courant dans R, l'entrée est tirée à +5 V, elle vaut 1."],
    [5, "Interrupteur fermé : il relie l'entrée à GND, elle vaut 0. Le courant passe dans R : 5 V divisés par 10 kΩ, soit 0,5 mA. Sans R, l'interrupteur court-circuiterait l'alimentation."],
    [10, "Chaque interrupteur a sa résistance de pull-up : A ceinture, C frein, D service, B sélecteur. Ceinture bouclée et frein enfoncé ferment le contact : A = 0 et C = 0."],
    [16, "Trois CI : 74HC02 (NON-OU), 74HC32 (OU) et 74HC08 (ET). Chacun reçoit +5 V sur la broche 14 et GND sur la broche 7."],
    [22, "Sur le 74HC02, la sortie 1Y est la broche 1 ; les entrées 1A et 1B sont les broches 2 et 3. A et C y arrivent."],
    [28, "La sortie du 74HC02 va sur l'entrée 1A du 74HC32 (broche 1), D sur 1B (broche 2). La sortie 1Y est la broche 3."],
    [34, "Le 74HC08 reçoit la sortie de l'OU (broche 1) et B (broche 2). Sa sortie 1Y (broche 3) est S : elle commande la LED, branchée vers GND à travers R."],
    [40, "Les entrées des portes inutilisées vont à GND. Un point : les fils sont reliés. Un demi-cercle : les fils se croisent sans contact."],
    [46, "Essai : ceinture bouclée et frein enfoncé (A et C fermés : 0), sélecteur sur P (B ouvert : 1). S = 1 : la LED s'allume."],
  ],
  draw(t) {
    if (t < 10) return l4zoom(t);
    const essai = t >= 46, V = { A: essai ? 0 : 1, B: essai ? 1 : 0, C: essai ? 0 : 1, D: 0 };
    const N = 1 - (V.A | V.C), O = V.D | N, S = V.B & O, led = S === 1;
    const cy = 130, ch = 56, cw = 160, CX = [300, 490, 680], P = (c, k) => dipPin(CX[c], cy, cw, ch, k);
    const R5 = 36, GT = 62, GB = 440, Y7 = 212, LO = 226, SW0 = 360, SW1 = 400, xl = 860;
    const COL = [["A", 55, 260, [0, 2]], ["C", 110, 285, [0, 3]], ["D", 165, 310, [1, 2]], ["B", 220, 335, [2, 2]]];
    const ink = "#242852", red = "#D0312D", gnd = "#5A6478";
    const ROUGE = `stroke:${red};stroke-width:2.5`, GRIS = `stroke:${gnd};stroke-width:2.2`;
    const sig = (x) => (x ? "stroke:#297FD5;stroke-width:4.5" : `stroke:${ink};stroke-width:3`);
    const T2 = (x, y, s, o = {}) => TX(x, y, s, Object.assign({ color: ink }, o));
    // tous les fils : [points, style] ; chaque fil saute les tronçons verticaux des autres (REGLES 3.3)
    const F = [], pts = [], dots = [];
    const add = (p, st) => { F.push([p, st]); pts.push(p); };
    add([[30, R5], [930, R5]], `stroke:${red};stroke-width:4`);
    add([[290, GT], [820, GT]], `stroke:${ink};stroke-width:4`);
    add([[30, GB], [930, GB]], `stroke:${ink};stroke-width:4`);
    CX.forEach((_, c) => {
      const [x14] = P(c, 14), [x7] = P(c, 7);
      add([P(c, 14), [x14, R5]], ROUGE); dots.push([x14, R5, red]);
      add([P(c, 7), [x7, GB]], GRIS); dots.push([x7, GB, ink]);
      L4UNUSED[c][0].forEach((k) => { const [x] = P(c, k); add([P(c, k), [x, GT]], GRIS); dots.push([x, GT, ink]); });
      const bas = L4UNUSED[c][1].map((k) => P(c, k)[0]);
      L4UNUSED[c][1].forEach((k, j) => { add([P(c, k), [bas[j], Y7]], GRIS); if (j > 0) dots.push([bas[j], Y7, gnd]); });
      add([[bas[0], Y7], [x7, Y7]], GRIS); dots.push([x7, Y7, gnd]);
    });
    COL.forEach(([n, x, ly, [c, k]]) => {
      const v = V[n], [px, py] = P(c, k);
      add([[x, R5], [x, 70]], ROUGE); dots.push([x, R5, red]);
      add([[x, 110], [x, SW0]], sig(v)); dots.push([x, ly, v ? "#297FD5" : ink]);
      add([[x, ly], [px, ly], [px, py]], sig(v));
      add([[x, SW1], [x, GB]], GRIS); dots.push([x, GB, ink]);
    });
    add([P(0, 1), [P(0, 1)[0], LO], [P(1, 1)[0], LO], P(1, 1)], sig(N));
    add([P(1, 3), [P(1, 3)[0], LO], [P(2, 1)[0], LO], P(2, 1)], sig(O));
    add([P(2, 3), [P(2, 3)[0], LO], [xl, LO], [xl, 250]], sig(S));
    add([[xl, 332], [xl, GB]], GRIS); dots.push([xl, GB, ink]);
    let s = '<svg viewBox="0 0 960 460">';
    s += `<rect x="14" y="14" width="932" height="440" rx="12" style="fill:#F4F5F8;stroke:#C9D2E3"/>`;
    s += T2(34, 29, "+5 V", { size: 13, bold: true, color: red }) + T2(284, 67, "GND", { size: 13, bold: true, anchor: "end" }) + T2(926, 433, "GND", { size: 13, bold: true, anchor: "end" });
    CX.forEach((x, c) => { s += dipG(x, cy, cw, ch, ["74HC02", "74HC32", "74HC08"][c], { nums: true, fs: 18 }); });
    F.forEach(([p, st], i) => { s += filP(p, null, pts.filter((_, j) => j !== i), { style: st }); });
    dots.forEach(([x, y, c]) => { s += liaison(x, y, c, 3.8); });
    // résistances de pull-up et interrupteurs (contact à fermeture, CEI 60617-7)
    s += T2(236, 88, "pull-up", { size: 13, bold: true }) + T2(236, 106, "10 kΩ", { size: 13, color: gnd });
    COL.forEach(([n, x]) => {
      s += `<rect x="${x - 5}" y="70" width="10" height="40" style="fill:#FFFFFF;stroke:${ink};stroke-width:1.8"/>`;
      s += contact(x, SW0, SW1, V[n] === 0, ink, 1) + T2(x - 15, 386, n, { size: 16, bold: true, italic: true, anchor: "end" });
    });
    // sortie S → R → LED → GND
    s += `<rect x="${xl - 6}" y="250" width="12" height="40" style="fill:#FFFFFF;stroke:${ink};stroke-width:2"/>` + T2(xl - 12, 276, "R", { size: 14, italic: true, anchor: "end" });
    s += `<line x1="${xl}" y1="290" x2="${xl}" y2="302" style="stroke:${ink};stroke-width:2.5"/>`;
    if (led) s += `<circle cx="${xl}" cy="311" r="22" style="fill:#FF5A3C;opacity:.3"/>`;
    s += `<polygon points="${xl - 11},302 ${xl + 11},302 ${xl},320" style="fill:${led ? "#FF5A3C" : "#FFFFFF"};stroke:${ink};stroke-width:2"/><line x1="${xl - 11}" y1="321" x2="${xl + 11}" y2="321" style="stroke:${ink};stroke-width:2.5"/>`;
    s += `<line x1="${xl}" y1="321" x2="${xl}" y2="332" style="stroke:${ink};stroke-width:2.5"/>`;
    s += `<path d="M ${xl + 13} 308 l 10 -8 m -4 0 h 4 v 4 M ${xl + 13} 316 l 10 -8 m -4 0 h 4 v 4" style="fill:none;stroke:${led ? "#FF5A3C" : ink};stroke-width:1.6"/>`;
    s += T2(842, 218, "S", { size: 16, bold: true, italic: true, anchor: "middle" });
    s += T2(876, 366, "LED", { size: 14, bold: true, color: led ? red : gnd }) + T2(876, 384, led ? "allumée" : "éteinte", { size: 14, bold: true, color: led ? red : gnd });
    // repères de l'étape en cours
    const step = L4T.filter((x) => t >= x).length - 1, pulse = 0.55 + 0.45 * Math.sin(t * 5);
    const ring = (x, y) => `<circle cx="${x}" cy="${y}" r="11" style="fill:none;stroke:#EE8A00;stroke-width:3;opacity:${pulse}"/>`;
    const pin = (c, k) => { const [x, y] = P(c, k); return [x, y + (k <= 7 ? -6 : 6)]; };
    const R = { 2: COL.map(([, x]) => [x, (SW0 + SW1) / 2]), 3: [0, 1, 2].flatMap((c) => [pin(c, 14), pin(c, 7)]), 4: [1, 2, 3].map((k) => pin(0, k)),
      5: [1, 2, 3].map((k) => pin(1, k)), 6: [1, 2, 3].map((k) => pin(2, k)), 7: L4UNUSED.flatMap(([h, b], c) => h.concat(b).map((k) => pin(c, k))), 8: [pin(2, 3)] }[step] || [];
    R.forEach(([x, y]) => { s += ring(x, y); });
    return s + "</svg>";
  },
});
