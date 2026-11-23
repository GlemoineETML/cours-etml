// ================================================================ leçons animées de la page 121 (présentation 120)
const OVN = '<tspan style="text-decoration:overline">N</tspan>';

// ---------------------------------------------------------------- L1 la ligne de remplissage (diapo 2)
// temps du scénario u = t / 1.5 (ralenti), boucle de 27 s de scénario
const LK = (u) => { let k = 0; for (const [a, b] of [[0, 3], [6, 9], [12, 15], [21, 24]]) { if (u >= b) k++; else if (u > a) return k + ease((u - a) / (b - a)); else return k; } return k; };
const LFILL = { 1: [3, 6], 2: [9, 12], 3: [18, 21], 4: [24, 27] };
const lfill = (j, u) => j <= 0 ? 1 : LFILL[j] ? clamp((u - LFILL[j][0]) / 3) : 0;
const inI = (u, iv) => iv.some(([a, b]) => u >= a && u < b);
const LB = (u) => inI(u, [[3, 6], [9, 12], [15, 21], [24, 27]]) ? 1 : 0;
const LL = (u) => u < 3 ? 0.7 : u < 6 ? lerp(0.7, 0.6, (u - 3) / 3) : u < 9 ? 0.6 : u < 12 ? lerp(0.6, 0.5, (u - 9) / 3) : u < 18 ? 0.5 :
  u < 23 ? lerp(0.5, 0.8, (u - 18) / 5) : u < 24 ? 0.8 : u < 27 ? lerp(0.8, 0.7, (u - 24) / 3) : 0.7;
const LN = (u) => LL(u) > 0.5001 ? 1 : 0;
const LV = (u) => LB(u) & LN(u);
lesson("L1", {
  dur: 40.5, label: "Animation : la ligne de remplissage, avec le capteur de bouteille B, le capteur de niveau N, la vanne V = B · N et son chronogramme",
  steps: [
    [0, "Sur la ligne de remplissage, chaque capteur donne un 0 ou un 1. B = 1 : une bouteille vide est sous le bec."],
    [6, "N = 1 : la cuve contient assez de liquide. La vanne s'ouvre seulement si B = 1 et N = 1 : V = B · N, une porte ET."],
    [13.5, "La cuve se vide peu à peu. Quand le liquide passe sous le capteur, N tombe à 0."],
    [22.5, "Une bouteille attend (B = 1), mais N = 0 : la vanne reste fermée et le voyant « cuve vide » s'allume."],
    [27, "La pompe remplit la cuve : N repasse à 1 et la vanne s'ouvre enfin."],
    [33, "Le chronogramme garde la trace de B, N et V : V vaut 1 seulement quand B et N valent 1 en même temps."],
  ],
  draw(t) {
    const u = t / 1.5, k = LK(u), B = LB(u), N = LN(u), V = LV(u), L = LL(u), pump = u >= 18 && u < 23;
    let s = '<svg viewBox="0 0 960 400">';
    // pompe et cuve
    s += `<line x1="110" y1="60" x2="194" y2="60" style="stroke:var(--muted);stroke-width:6"/><line x1="226" y1="60" x2="270" y2="60" style="stroke:var(--muted);stroke-width:6"/>`;
    s += `<circle cx="210" cy="60" r="16" style="fill:var(--surface);stroke:var(--ink);stroke-width:2.5"/>`;
    const an = pump ? u * 7 : 0.6;
    s += `<line x1="${210 - 11 * Math.cos(an)}" y1="${60 - 11 * Math.sin(an)}" x2="${210 + 11 * Math.cos(an)}" y2="${60 + 11 * Math.sin(an)}" style="stroke:${pump ? "var(--one)" : "var(--ink)"};stroke-width:3"/>`;
    s += TX(210, 98, pump ? "pompe : marche" : "pompe", { size: 13, anchor: "middle", color: pump ? "var(--one)" : "var(--muted)", bold: pump });
    s += `<rect x="270" y="${150 - L * 120}" width="160" height="${L * 120}" style="fill:var(--one);opacity:.45"/>`;
    s += `<rect x="270" y="30" width="160" height="120" rx="4" style="fill:none;stroke:var(--ink);stroke-width:3"/>` + TX(350, 24, "cuve", { size: 13, anchor: "middle", color: "var(--muted)" });
    s += `<line x1="272" y1="90" x2="428" y2="90" style="stroke:var(--muted);stroke-width:1;stroke-dasharray:4 4"/><path d="M 444 90 l 12 -8 v 16 z" style="fill:${N ? "var(--one)" : "var(--ink)"}"/>`;
    s += TX(462, 96, "N", { size: 18, bold: true, italic: true }) + pill(500, 90, N);
    s += lampG(570, 72, 14, !N, "var(--warn)") + TX(570, 106, "cuve vide", { size: 13, anchor: "middle", bold: !N, color: !N ? "var(--warn)" : "var(--muted)" }) +
      TX(570, 124, "= " + OVN, { size: 14, anchor: "middle", italic: true });
    // bec, vanne, jet
    s += `<line x1="350" y1="150" x2="350" y2="214" style="stroke:var(--muted);stroke-width:8"/>`;
    s += `<polygon points="336,170 336,186 350,178 364,170 364,186 350,178" style="fill:${V ? "var(--one)" : "var(--surface)"};stroke:var(--ink);stroke-width:2"/>`;
    s += TX(374, 184, "V", { size: 18, bold: true, italic: true }) + pill(410, 178, V);
    if (V) s += `<rect x="346" y="214" width="8" height="24" style="fill:var(--one);opacity:.8"/>`;
    // convoyeur et bouteilles
    s += `<rect x="10" y="310" width="610" height="14" rx="7" style="fill:var(--line);stroke:var(--ink);stroke-width:1.5"/>`;
    for (let i = 0; i < 16; i++) { const x = 10 + ((i * 40 + k * 120) % 640); if (x < 616) s += `<line x1="${x}" y1="312" x2="${x}" y2="322" style="stroke:var(--muted);stroke-width:2"/>`; }
    const bot = [];
    for (let j = Math.floor(k) - 3; j <= Math.floor(k) + 4; j++) {
      const x = 350 + (k - j) * 120; if (x < 26 || x > 604) continue;
      const f = lfill(j, u); bot.push(x);
      s += `<rect x="${x - 6}" y="236" width="12" height="15" style="fill:var(--surface);stroke:var(--ink);stroke-width:1.8"/>`;
      s += `<rect x="${x - 16}" y="250" width="32" height="60" rx="5" style="fill:var(--surface);stroke:var(--ink);stroke-width:1.8"/>`;
      if (f > 0) s += `<rect x="${x - 14}" y="${308 - 56 * f}" width="28" height="${56 * f}" rx="3" style="fill:var(--one);opacity:.7"/>`;
    }
    // barrière lumineuse B
    const hit = bot.filter((x) => x + 16 > 304 && x - 16 < 396).map((x) => x - 16).sort((a, b) => a - b)[0];
    s += `<rect x="296" y="276" width="8" height="18" style="fill:var(--ink)"/><rect x="396" y="276" width="8" height="18" style="fill:var(--ink)"/>`;
    s += `<line x1="304" y1="285" x2="${hit != null ? Math.max(304, hit) : 396}" y2="285" style="stroke:var(--bad);stroke-width:2;stroke-dasharray:5 3"/>`;
    s += pill(150, 352, B) + TX(124, 359, "B", { size: 18, bold: true, italic: true, anchor: "end" }) +
      TX(176, 358, "barrière lumineuse : une bouteille vide est sous le bec", { size: 14, color: "var(--muted)" });
    // logique et chronogramme
    const g = gateAt("ET", B, N, V, 640, 0, 0.85, { labels: ["B", "N"], out: "V" });
    s += g.svg + TX(790, 142, "V = B · N", { size: 20, bold: true, anchor: "middle", color: "var(--head)" });
    s += traceG(700, 156, 240, [{ name: "B", f: LB }, { name: "N", f: LN }, { name: "V", f: LV, color: "var(--one)" }], u, 27, { rh: 42, dt: 0.05 });
    s += TX(820, 298, "chronogramme", { size: 12, anchor: "middle", color: "var(--muted)" });
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
  const rows = [["A", (h) => h.a, "var(--ink)"], ["B", (h) => h.b, one ? "var(--line)" : "var(--ink)"], ["Y", (h) => (one ? FN.NON(h.a) : FN[gk](h.a, h.b)), "var(--one)"]];
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
    [3, "Colonnes du poids fort au poids faible : C B A, puis la sortie Y. Les lignes suivent le comptage binaire, de 000 à 111."],
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
    s += `<line x1="376" y1="102" x2="408" y2="102" style="${wireStyle(y)}"/>` + lampG(424, 102, 13, y) + TX(424, 136, "Y", { size: 15, bold: true, italic: true, anchor: "middle" });
    // tableau
    const tx = 520, cw = 70, ry = (r) => 64 + r * 36;
    ["C", "B", "A", "Y"].forEach((n, i) => {
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
    if (cr >= 0 && t < 24) s += TX(60, 230, `ligne ${cr} : C B A = ${cur.join(" ")}`, { size: 20, bold: true }) + TX(60, 262, `Y = A · B · C = ${y}`, { size: 20, color: y ? "var(--one)" : "var(--ink)", bold: true });
    if (t >= 24) { const o = prog(t, 24, 25); s += `<g style="opacity:${o}">` + TX(60, 236, "3 entrées → 2³ = 8 lignes", { size: 26, bold: true, color: "var(--head)" }) + TX(60, 274, "n entrées → 2ⁿ lignes", { size: 22, color: "var(--head)" }) + "</g>"; }
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L3 lire un chronogramme (diapo 4)
let l3g = "ET";
const L3C = lesson("L3", {
  dur: 27, label: "Animation : un curseur parcourt le chronogramme intervalle par intervalle, lit A et B, et trouve Y dans la table de vérité",
  extra: '<span class="muted">Porte :</span><span class="chips" id="l3-g"></span>',
  steps: [
    [0, "Le temps avance de gauche à droite. On découpe le chronogramme en intervalles : dans chacun, aucun signal ne change."],
    [2, "Pour chaque intervalle, on lit A et B, puis on cherche la ligne B A dans la table : elle donne Y."],
    [12.4, "On continue jusqu'au bout. La courbe Y obtenue est le chronogramme de sortie de la porte."],
    [23, "Si un seul intervalle ne correspond pas à la table, ce n'est pas cette porte : c'est la méthode de cet exercice."],
  ],
  draw(t) {
    const CA = D.CHRONO_A, CB = D.CHRONO_B, n = CA.length, x0 = 70, pw = 540 / n, CY = CA.map((a, i) => FN[l3g](a, CB[i]));
    const cur = t < 2 ? -1 : Math.min(n - 1, Math.floor((t - 2) / 2.6)), done = t >= 2 + n * 2.6;
    let s = '<svg viewBox="0 0 960 300">';
    if (cur >= 0 && !done) s += `<rect x="${x0 + cur * pw}" y="30" width="${pw}" height="232" style="fill:var(--tint);stroke:var(--blue);stroke-width:2"/>`;
    for (let i = 0; i <= n; i++) s += `<line x1="${x0 + i * pw}" y1="30" x2="${x0 + i * pw}" y2="262" style="stroke:var(--line);stroke-dasharray:3 4"/>`;
    for (let i = 0; i < n; i++) s += TX(x0 + i * pw + pw / 2, 22, i + 1, { size: 13, anchor: "middle", color: "var(--muted)" });
    [["A", CA, n, "var(--ink)"], ["B", CB, n, "var(--ink)"], ["Y", CY, done ? n : cur + 1, "var(--one)"]].forEach(([nm, sig, upto, col], r) => {
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
    ["B", "A", "Y"].forEach((h, i) => { s += `<rect x="${tx + i * cw}" y="32" width="${cw}" height="34" style="fill:var(--light);stroke:var(--line)"/>` + TX(tx + i * cw + cw / 2, 56, h, { size: 18, bold: true, anchor: "middle", color: "#242852" }); });
    const row = cur >= 0 && !done ? CB[cur] * 2 + CA[cur] : -1;
    tdv(l3g).forEach((r, k) => {
      const y = 66 + k * 36;
      r.forEach((v, i) => { s += `<rect x="${tx + i * cw}" y="${y}" width="${cw}" height="36" style="fill:${k === row ? "var(--tint)" : "var(--surface)"};stroke:var(--line)"/>` + TX(tx + i * cw + cw / 2, y + 25, v, { size: 19, mono: true, anchor: "middle", bold: i === 2 && v === 1, color: i === 2 && v ? "var(--one)" : "var(--ink)" }); });
      if (k === row) s += `<rect x="${tx}" y="${y}" width="${3 * cw}" height="36" style="fill:none;stroke:var(--blue);stroke-width:2.5"/>`;
    });
    s += `<line x1="${tx + 2 * cw}" y1="32" x2="${tx + 2 * cw}" y2="210" style="stroke:var(--head);stroke-width:3"/>`;
    if (row >= 0) s += TX(tx + 1.5 * cw, 244, `intervalle ${cur + 1} : B A = ${CB[cur]} ${CA[cur]}`, { size: 16, anchor: "middle" }) +
      TX(tx + 1.5 * cw, 272, `→ Y = ${CY[cur]}`, { size: 22, bold: true, anchor: "middle", color: CY[cur] ? "var(--one)" : "var(--head)" });
    return s + "</svg>";
  },
});
D.ORDER.filter((k) => k !== "NON").forEach((k) => {
  const b = document.createElement("button"); b.type = "button"; b.className = "chip"; b.textContent = D.GATES[k].nom; b.setAttribute("aria-pressed", k === l3g ? "true" : "false");
  b.onclick = () => { l3g = k; $("l3-g").querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", c.textContent === D.GATES[k].nom ? "true" : "false")); L3C.t = 0; L3C.dirty = true; };
  $("l3-g").appendChild(b);
});

// ---------------------------------------------------------------- L4 le 74HC08 sur breadboard (diapo 13)
lesson("L4", {
  dur: 20, label: "Animation : un 74HC08 câblé sur breadboard, deux interrupteurs B et N sur la porte 1 et une LED sur sa sortie",
  steps: [
    [0, "Le 74HC08 contient 4 portes ET. On utilise la porte 1 : entrées 1A (broche 1) et 1B (broche 2), sortie 1Y (broche 3)."],
    [5, "Alimentation : +5 V sur VCC (broche 14), masse sur GND (broche 7). Sans elles, le CI ne fonctionne pas."],
    [10, "Les entrées des portes inutilisées (broches 4, 5, 9, 10, 12, 13) vont à GND : une entrée CMOS ne reste jamais en l'air."],
    [15, "Avec B = 1 et N = 1, la sortie 1Y passe à 1 et la LED (la vanne) s'allume. Dans les trois autres cas, elle reste éteinte."],
  ],
  draw(t) {
    const CMB = [[0, 0], [1, 0], [0, 1], [1, 1]][Math.min(3, Math.floor(t / 5))], [B, N] = CMB, V = B & N;
    const cx = 330, cy = 160, cw = 300, ch = 70, P = (k) => dipPin(cx, cy, cw, ch, k);
    const ink = "#242852", wv = (v) => v ? "stroke:#297FD5;stroke-width:5" : "stroke:#242852;stroke-width:3", pl = (pts, st) => `<polyline points="${pts.map((p) => p.join(",")).join(" ")}" fill="none" style="${st};stroke-linejoin:round"/>`;
    const T2 = (x, y, s, o = {}) => TX(x, y, s, Object.assign({ color: ink }, o));
    let s = '<svg viewBox="0 0 960 380">';
    s += `<rect x="20" y="28" width="920" height="340" rx="12" style="fill:#F4F5F8;stroke:#C9D2E3"/>`;
    for (let x = 40; x <= 920; x += 20) for (const y of [120, 300]) s += `<circle cx="${x}" cy="${y}" r="2" style="fill:#C9CFDB"/>`;
    s += `<line x1="40" y1="52" x2="920" y2="52" style="stroke:#D0312D;stroke-width:4"/>` + T2(44, 46, "+5 V", { size: 13, bold: true, color: "#D0312D" });
    s += `<line x1="380" y1="80" x2="920" y2="80" style="stroke:${ink};stroke-width:4"/>` + T2(916, 74, "GND", { size: 13, bold: true, anchor: "end" });
    s += `<line x1="40" y1="348" x2="920" y2="348" style="stroke:${ink};stroke-width:4"/>` + T2(916, 364, "GND", { size: 13, bold: true, anchor: "end" });
    // alimentation et entrées inutilisées
    s += pl([P(14), [P(14)[0], 52]], "stroke:#D0312D;stroke-width:3") + `<circle cx="${P(14)[0]}" cy="52" r="4" style="fill:#D0312D"/>`;
    [13, 12, 10, 9].forEach((k) => { s += pl([P(k), [P(k)[0], 80]], "stroke:#5A6478;stroke-width:2.5") + `<circle cx="${P(k)[0]}" cy="80" r="3.5" style="fill:${ink}"/>`; });
    s += pl([P(7), [P(7)[0], 348]], `stroke:${ink};stroke-width:3`) + `<circle cx="${P(7)[0]}" cy="348" r="4" style="fill:${ink}"/>`;
    s += pl([P(4), [P(4)[0], 262], [P(7)[0], 262]], "stroke:#5A6478;stroke-width:2.5") + pl([P(5), [P(5)[0], 262]], "stroke:#5A6478;stroke-width:2.5") + `<circle cx="${P(7)[0]}" cy="262" r="3.5" style="fill:${ink}"/>`;
    // interrupteurs B et N
    [["B", "bouteille", B, 280, 1], ["N", "niveau", N, 318, 2]].forEach(([n, l, v, y, pin]) => {
      s += `<rect x="54" y="${y - 16}" width="140" height="32" rx="6" style="fill:#FFFFFF;stroke:#9AA2B4"/>` + T2(64, y + 6, `${n} ${l}`, { size: 14, bold: true });
      s += `<rect x="150" y="${y - 8}" width="34" height="16" rx="8" style="fill:${v ? "#297FD5" : "#C9CFDB"}"/><circle cx="${v ? 176 : 158}" cy="${y}" r="7" style="fill:#FFFFFF;stroke:${ink}"/>`;
      s += pl([[194, y], [P(pin)[0], y], P(pin)], wv(v)) + T2(204, y - 6, n + " = " + v, { size: 13, bold: true, color: v ? "#297FD5" : ink });
    });
    // sortie 1Y → LED → résistance → GND
    const xo = P(3)[0], on = V === 1;
    s += pl([P(3), [xo, 266]], wv(V));
    if (on) s += `<circle cx="${xo}" cy="282" r="22" style="fill:#FF5A3C;opacity:.3"/>`;
    s += `<polygon points="${xo - 11},266 ${xo + 11},266 ${xo},286" style="fill:${on ? "#FF5A3C" : "#FFFFFF"};stroke:${ink};stroke-width:2"/><line x1="${xo - 11}" y1="287" x2="${xo + 11}" y2="287" style="stroke:${ink};stroke-width:2.5"/>`;
    s += `<path d="M ${xo + 13} 272 l 10 -8 m -4 0 h 4 v 4 M ${xo + 13} 280 l 10 -8 m -4 0 h 4 v 4" style="fill:none;stroke:${on ? "#FF5A3C" : ink};stroke-width:1.6"/>`;
    s += pl([[xo, 287], [xo, 300]], `stroke:${ink};stroke-width:2.5`) + `<rect x="${xo - 6}" y="300" width="12" height="30" style="fill:#FFFFFF;stroke:${ink};stroke-width:2"/>` + pl([[xo, 330], [xo, 348]], `stroke:${ink};stroke-width:2.5`);
    s += T2(xo + 30, 296, "LED = vanne V", { size: 13, bold: true, color: on ? "#D0312D" : ink });
    s += dipG(cx, cy, cw, ch, "74HC08", { nums: true, fs: 24 });
    // repères de l'étape en cours
    const step = Math.min(3, Math.floor(t / 5)), pulse = 0.55 + 0.45 * Math.sin(t * 5);
    const ring = (k) => `<circle cx="${P(k)[0]}" cy="${P(k)[1] + (k <= 7 ? -7 : 7)}" r="13" style="fill:none;stroke:#EE8A00;stroke-width:3;opacity:${pulse}"/>`;
    ({ 0: [1, 2, 3], 1: [14, 7], 2: [4, 5, 9, 10, 12, 13], 3: [3] })[step].forEach((k) => { s += ring(k); });
    return s + "</svg>";
  },
});
