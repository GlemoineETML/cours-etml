// ================================================================ leçons animées de la page 101 (présentation 100)
const VTX = (v, d = 2) => v.toFixed(d).replace(".", ",") + " V";
const hcState = (v, fam = "HC") => { const [vil, vih] = D.NIV[fam]; return v <= vil ? 0 : (v >= vih ? 1 : "x"); };

// ---------------------------------------------------------------- L1 familles et référence (diapos 3 et 5)
lesson("L1", {
  dur: 30, label: "Animation : les familles TTL, CMOS et 74HC(T), puis la référence SN74HCT00N découpée en cinq parties",
  steps: [
    [0, "Trois grandes familles de CI logiques : le TTL (transistors bipolaires), le CMOS (MOSFET) et l'hybride 74HC(T), en CMOS mais avec le brochage de la série 74."],
    [7.5, "Sur le boîtier, une seule référence : SN74HCT00N. On la lit de gauche à droite, morceau par morceau."],
    [11.5, "SN : le fabricant. 74 : la plage de température. HCT : la technologie. 00 : la fonction. N : le boîtier."],
    [22, "Même fonction chez un autre fabricant : M74HCT00 (ST). La série 4000 a aussi 4 portes NON-ET (CD4011BE), mais ses broches ne sont pas au même endroit."],
  ],
  draw(t) {
    let s = '<svg viewBox="0 0 960 410">';
    const fa = 1 - prog(t, 6.6, 7.6);
    if (fa > 0) {
      const FAM = [["TTL", "Transistor-Transistor Logic", ["transistors bipolaires", "alimentation 5 V", "rapide, mais gourmand", "série 74xx, ex. 7400"]],
        ["CMOS", "Complementary MOS", ["MOSFET canal N et canal P", "consomme très peu au repos", "rapide (familles modernes)", "série 40xx, ex. 4011"]],
        ["74HC(T)", "CMOS au brochage 74xx", ["structure interne CMOS", "brochage de la série 74", "HCT : entrées compatibles TTL", "ex. 74HCT00"]]];
      FAM.forEach(([n, sub, li], i) => {
        const o = prog(t, 0.4 + i * 1.8, 1.4 + i * 1.8) * fa, x = 30 + i * 310, y = 50 + (1 - o) * 20;
        if (o <= 0) return;
        s += `<g style="opacity:${o}"><rect x="${x}" y="${y}" width="290" height="300" rx="14" style="fill:${i === 2 ? "var(--tint)" : "var(--surface)"};stroke:${i === 2 ? "var(--blue)" : "var(--line)"};stroke-width:2"/>`;
        s += TX(x + 22, y + 50, n, { size: 36, bold: true, color: "var(--head)" }) + TX(x + 22, y + 80, sub, { size: 15, italic: true, color: "var(--muted)" });
        li.forEach((l, j) => { s += `<circle cx="${x + 28}" cy="${y + 130 + j * 42}" r="4.5" style="fill:var(--blue)"/>` + TX(x + 42, y + 136 + j * 42, l, { size: 17 }); });
        s += "</g>";
      });
    }
    const fb = prog(t, 7.4, 8.4);
    if (fb > 0) {
      s += `<g style="opacity:${fb}">` + dipG(40, 110, 250, 80, "SN74HCT00N", { fs: 21 }) +
        TX(165, 236, "vue de dessus : l'encoche marque le côté de la broche 1", { size: 12.5, anchor: "middle", italic: true, color: "var(--muted)" }) + "</g>";
      const SEG = [["SN", "fabricant", "Texas Instruments (ST : M, onsemi : MC)"], ["74", "plage", "commerciale, 0 … 70 °C (54 : militaire)"],
        ["HCT", "technologie", "CMOS, entrées compatibles TTL"], ["00", "fonction", "4 portes NON-ET à 2 entrées"], ["N", "boîtier", "DIP 14 (D : SOIC)"]];
      const W = [80, 80, 116, 80, 60], gap = 16 * prog(t, 9.5, 11);
      let x = 360;
      SEG.forEach(([c, r, m], i) => {
        const t0 = 11.5 + i * 2, on = t >= t0, act = on && t < t0 + 2 && t < 22;
        s += `<g style="opacity:${fb}"><rect x="${x}" y="40" width="${W[i]}" height="64" rx="8" style="fill:${act ? "var(--blue)" : on ? "var(--tint)" : "var(--surface)"};stroke:var(--blue);stroke-width:2"/>` +
          TX(x + W[i] / 2, 85, c, { size: 36, bold: true, mono: true, anchor: "middle", color: act ? "#fff" : "var(--head)" }) + "</g>";
        if (on) {
          const o = prog(t, t0, t0 + 0.8), y = 150 + i * 38;
          s += `<g style="opacity:${o}">` + TX(360, y, c, { size: 22, bold: true, mono: true, color: "var(--blue)" }) +
            TX(440, y, r, { size: 18, bold: true, color: "var(--head)" }) + TX(560, y, m, { size: 17 }) + "</g>";
        }
        x += W[i] + gap;
      });
      [[22.5, true, "M74HCT00 (ST)", "même fonction, même brochage"], [25.5, false, "CD4011BE (série 4000)", "4 NON-ET aussi, mais autre brochage"]].forEach(([t0, ok, a, b], i) => {
        const o = prog(t, t0, t0 + 0.8); if (o <= 0) return;
        const y = 300 + i * 62;
        s += `<g style="opacity:${o}">` + okMark(54, y, ok, 13) + TX(78, y + 6, a, { size: 18, bold: true }) + TX(78, y + 28, b, { size: 15, color: "var(--muted)" }) + "</g>";
      });
    }
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L2 niveaux d'entrée (diapo 16)
const L2V = (s) => {
  if (s < 3) return 0.3; if (s < 3.6) return lerp(0.3, 4.6, (s - 3) / 0.6); if (s < 7) return 4.6; if (s < 7.6) return lerp(4.6, 0.3, (s - 7) / 0.6);
  if (s < 9) return 0.3; if (s < 15) return lerp(0.3, 4.6, (s - 9) / 6); if (s < 17) return 4.6; if (s < 17.4) return lerp(4.6, 2.5, (s - 17) / 0.4);
  return 2.5 + 0.1 * Math.sin(s * 9) + 0.05 * Math.sin(s * 23);
};
lesson("L2", {
  dur: 27, label: "Animation : une tension qui change sur l'entrée d'un 74HC, comparée aux seuils VIL et VIH, et l'état lu par la porte",
  steps: [
    [0, "Un 74HC alimenté en 5 V : en dessous de V<sub>IL</sub> = 1,5 V, l'entrée lit 0 ; au-dessus de V<sub>IH</sub> = 3,5 V, elle lit 1."],
    [3, "Signal propre : il saute d'un niveau à l'autre et ne s'arrête jamais dans la zone interdite."],
    [9, "La tension monte lentement : entre 1,5 V et 3,5 V, l'état n'est pas garanti. La porte peut lire 0 ou 1."],
    [17, "Panne typique : une entrée en l'air ou une mauvaise soudure reste vers 2,5 V. Le multimètre le montre tout de suite."],
  ],
  draw(t) {
    const x0 = 90, x1 = 640, Y = (v) => 300 - v * 52, X = (s) => x0 + (x1 - x0) * s / 24, [vil, vih] = D.NIV.HC, sc = Math.min(t, 24);
    let s = '<svg viewBox="0 0 960 345">';
    s += `<rect x="${x0}" y="${Y(5)}" width="${x1 - x0}" height="${Y(vih) - Y(5)}" style="fill:var(--one);opacity:.13"/>`;
    s += `<rect x="${x0}" y="${Y(vih)}" width="${x1 - x0}" height="${Y(vil) - Y(vih)}" style="fill:var(--warn-bg)"/>`;
    s += `<rect x="${x0}" y="${Y(vil)}" width="${x1 - x0}" height="${Y(0) - Y(vil)}" style="fill:var(--zero);opacity:.13"/>`;
    s += TX(x1 - 10, (Y(5) + Y(vih)) / 2 + 7, "lu comme 1", { anchor: "end", bold: true, size: 15, color: "var(--muted)" });
    s += TX(212, (Y(vih) + Y(vil)) / 2 - 4, "zone", { anchor: "middle", bold: true, size: 15, color: "var(--warn)" }) + TX(212, (Y(vih) + Y(vil)) / 2 + 14, "interdite", { anchor: "middle", bold: true, size: 15, color: "var(--warn)" });
    s += TX(x1 - 10, (Y(vil) + Y(0)) / 2 + 7, "lu comme 0", { anchor: "end", bold: true, size: 15, color: "var(--muted)" });
    [[vih, `${SUBV("IH")} = 3,5 V`], [vil, `${SUBV("IL")} = 1,5 V`]].forEach(([v, l]) => {
      s += `<line x1="${x0}" y1="${Y(v)}" x2="${x1}" y2="${Y(v)}" style="stroke:var(--warn);stroke-width:2;stroke-dasharray:7 5"/>` + TX(x0 - 8, Y(v) + 5, l, { anchor: "end", size: 13.5 });
    });
    [[5, "5 V"], [0, "0 V"]].forEach(([v, l]) => { s += TX(x0 - 8, Y(v) + 5, l, { anchor: "end", size: 13.5 }); });
    s += `<rect x="${x0}" y="${Y(5)}" width="${x1 - x0}" height="${Y(0) - Y(5)}" style="fill:none;stroke:var(--ink);stroke-width:1.5"/>`;
    s += TX((x0 + x1) / 2, 330, "temps", { anchor: "middle", size: 13, italic: true, color: "var(--muted)" });
    // trace colorée selon l'état lu
    let seg = [], st = null; const col = { 0: "var(--zero)", 1: "var(--one)", x: "var(--warn)" };
    const flush = () => { if (seg.length > 1) s += `<polyline points="${seg.join(" ")}" fill="none" style="stroke:${col[st]};stroke-width:4;stroke-linejoin:round"/>`; };
    for (let u = 0; u <= sc + 1e-9; u += 0.04) {
      const v = L2V(u), k = hcState(v), p = `${X(u).toFixed(1)},${Y(v).toFixed(1)}`;
      if (k !== st) { if (seg.length) { seg.push(p); flush(); } seg = [p]; st = k; } else seg.push(p);
    }
    flush();
    const v = L2V(sc), k = hcState(v);
    s += `<circle cx="${X(sc)}" cy="${Y(v)}" r="7" style="fill:${col[k]};stroke:var(--surface);stroke-width:2"/>`;
    // multimètre et état lu
    s += `<rect x="690" y="40" width="240" height="110" rx="12" style="fill:#1E2238;stroke:#3A3F5C;stroke-width:2"/>` + TX(706, 64, "multimètre, V DC", { size: 13, color: "#ACCBF9" }) +
      TX(912, 128, VTX(v), { size: 40, bold: true, mono: true, anchor: "end", color: "#BEFFC8" });
    s += TX(690, 196, "Le 74HC lit :", { size: 17, bold: true });
    const fill = k === 1 ? "var(--one)" : k === 0 ? "var(--zero)" : "var(--warn-bg)", tc = k === 1 ? "#fff" : k === 0 ? "var(--surface)" : "var(--warn)";
    s += `<rect x="690" y="210" width="240" height="72" rx="12" style="fill:${fill};stroke:${k === "x" ? "var(--warn)" : fill};stroke-width:2.5${k === "x" ? ";stroke-dasharray:7 5" : ""}"/>`;
    s += TX(810, k === "x" ? 256 : 262, k === "x" ? "? non garanti" : String(k), { size: k === "x" ? 26 : 44, bold: true, anchor: "middle", color: tc });
    s += TX(810, 310, k === 1 ? "U ≥ V_IH" : k === 0 ? "U ≤ V_IL" : "V_IL < U < V_IH", { size: 15, anchor: "middle", color: "var(--muted)" }).replace(/V_(IH|IL)/g, (m, i) => SUBV(i));
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L3 marge de bruit (diapos 12 et 17)
let l3pair = 0, l3noise = 0.7;
const L3PAIRS = [["HC", "HC", "74HC → 74HC"], ["TTL", "HCT", "TTL → 74HCT"], ["TTL", "HC", "TTL → 74HC"]];
const L3PAT = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0];
const rnd = (k) => { const x = Math.sin(k * 12.9898 + 4.1) * 43758.5453; return x - Math.floor(x); };
const L3 = lesson("L3", {
  dur: 18, label: "Animation : des bits envoyés sur un long câble avec des parasites, et les bits lus par l'entrée selon la marge de bruit",
  extra: '<span class="muted">Liaison :</span><span class="chips" id="l3-pair"></span><label class="muted" for="l3-n">Parasites :</label><input type="range" id="l3-n" min="0" max="2" step="0.1" value="0.7"><b id="l3-nt">0,7 V</b><span class="tag" id="l3-stat"></span>',
  steps: [
    [0, "La carte A envoie des 0 et des 1 à la carte B par un long câble. Un moteur voisin ajoute des parasites sur le signal."],
    [6, "Tant qu'un parasite reste plus petit que la marge de bruit (bande verte), l'entrée lit le bon bit."],
    [12, "Augmente les parasites avec le curseur, ou choisis TTL → 74HC : des bits deviennent faux (croix rouge)."],
  ],
  draw(t, T) {
    const [src, dst, nm] = L3PAIRS[l3pair], [, , vol, voh] = D.NIV[src], [vil, vih] = D.NIV[dst];
    const x0 = 110, x1 = 900, Y = (v) => 300 - v * 44, BT = 1.25, PX = 64, X = (u) => x1 - (T - u) * PX;
    let s = '<svg viewBox="0 0 960 350">';
    // schéma : carte A — câble — carte B, moteur parasite
    s += `<rect x="110" y="12" width="190" height="34" rx="6" style="fill:var(--tint);stroke:var(--blue);stroke-width:2"/>` + TX(205, 35, "carte A : sortie " + nm.split(" → ")[0], { size: 14, bold: true, anchor: "middle" });
    s += `<rect x="710" y="12" width="190" height="34" rx="6" style="fill:var(--tint);stroke:var(--blue);stroke-width:2"/>` + TX(805, 35, "carte B : entrée " + nm.split(" → ")[1], { size: 14, bold: true, anchor: "middle" });
    let cab = "M 300 29"; for (let x = 300; x <= 710; x += 10) cab += ` L ${x} ${29 + 3 * Math.sin(x / 9)}`;
    s += `<path d="${cab}" fill="none" style="stroke:var(--ink);stroke-width:2.5"/>`;
    s += `<circle cx="505" cy="29" r="15" style="fill:var(--surface);stroke:var(--warn);stroke-width:2.5"/>` + TX(505, 35, "M", { size: 16, bold: true, anchor: "middle", color: "var(--warn)" });
    if (l3noise > 0) s += `<path d="M 485 14 l -8 -6 M 525 14 l 8 -6 M 485 44 l -8 6 M 525 44 l 8 6" style="stroke:var(--warn);stroke-width:2"/>`;
    // zones, marges
    s += `<rect x="${x0}" y="${Y(vih)}" width="${x1 - x0}" height="${Y(vil) - Y(vih)}" style="fill:var(--warn-bg)"/>`;
    const band = (a, b, ok, txt) => {
      const top = Y(Math.max(a, b)), h = Math.abs(Y(a) - Y(b));
      s += `<rect x="${x0}" y="${top}" width="${x1 - x0}" height="${h}" style="fill:${ok ? "var(--ok)" : "var(--bad)"};opacity:.22"/>` +
        TX(x1 - 8, top + h / 2 + 5, txt, { size: 13, bold: true, anchor: "end", color: ok ? "var(--ok)" : "var(--bad)" });
    };
    const nh = voh - vih, nl = vil - vol;
    band(voh, vih, nh >= 0, nh >= 0 ? `marge haute ${VTX(nh)}` : "pas de marge : le 1 n'est pas reconnu");
    band(vol, vil, nl >= 0, nl >= 0 ? `marge basse ${VTX(nl)}` : "pas de marge");
    [[voh, "OH", "var(--one)", ""], [vol, "OL", "var(--one)", ""], [vih, "IH", "var(--warn)", "7 5"], [vil, "IL", "var(--warn)", "7 5"]].forEach(([v, i, c, da]) => {
      s += `<line x1="${x0}" y1="${Y(v)}" x2="${x1}" y2="${Y(v)}" style="stroke:${c};stroke-width:1.6${da ? ";stroke-dasharray:" + da : ""}"/>` + TX(x0 - 8, Y(v) + 5, SUBV(i, " " + VTX(v)), { size: 12.5, anchor: "end" });
    });
    s += `<rect x="${x0}" y="${Y(5)}" width="${x1 - x0}" height="${Y(0) - Y(5)}" style="fill:none;stroke:var(--ink);stroke-width:1.2"/>`;
    // signal reçu : niveau de sortie + parasite (dirigé vers le seuil) + ondulation
    const uS = Math.max(0, T - (x1 - x0) / PX), bit = (k) => L3PAT[k % 16];
    const vAt = (u) => {
      const k = Math.floor(u / BT), c = (k + 0.5) * BT, lv = bit(k) ? voh : vol, a = l3noise * (0.45 + 0.55 * rnd(k)), z = Math.max(0, 1 - Math.abs(u - c) / 0.2);
      return lv + (bit(k) ? -1 : 1) * a * z + 0.06 * l3noise * Math.sin(u * 37);
    };
    let pts = [];
    for (let u = uS; u <= T + 1e-9; u += 0.02) pts.push(`${X(u).toFixed(1)},${Y(clamp(vAt(u), -0.3, 5.3)).toFixed(1)}`);
    if (pts.length > 1) s += `<polyline points="${pts.join(" ")}" fill="none" style="stroke:var(--ink);stroke-width:2.4;stroke-linejoin:round"/>`;
    let bad = 0, n = 0;
    for (let k = Math.max(0, Math.floor(uS / BT)); k <= Math.floor(T / BT); k++) {
      const c = (k + 0.5) * BT, xc = X(c); if (xc < x0 + 10 || c > T) continue;
      const v = vAt(c), st = hcState(v, dst), ok = st === bit(k); n++; if (!ok) bad++;
      s += TX(xc, 72, bit(k), { size: 16, bold: true, mono: true, anchor: "middle", color: "var(--muted)" });
      s += TX(xc - 6, 328, st === "x" ? "?" : st, { size: 17, bold: true, mono: true, anchor: "middle", color: ok ? "var(--ink)" : st === "x" ? "var(--warn)" : "var(--bad)" }) + okMark(xc + 12, 322, ok, 8);
    }
    s += TX(x0 - 8, 76, "envoyé", { size: 12, anchor: "end", color: "var(--muted)" }) + TX(x0 - 8, 330, "lu", { size: 12, anchor: "end", color: "var(--muted)" });
    const stat = $("l3-stat"); if (stat) { stat.textContent = n ? `bits faux : ${bad} sur ${n}` : ""; stat.className = "tag " + (bad ? "bad" : "ok"); }
    return s + "</svg>";
  },
});
L3PAIRS.forEach(([, , nm], i) => {
  const b = document.createElement("button"); b.type = "button"; b.className = "chip"; b.textContent = nm; b.setAttribute("aria-pressed", i === l3pair ? "true" : "false");
  b.onclick = () => { l3pair = i; $("l3-pair").querySelectorAll(".chip").forEach((c, j) => c.setAttribute("aria-pressed", j === i ? "true" : "false")); L3.dirty = true; };
  $("l3-pair").appendChild(b);
});
$("l3-n").oninput = () => { l3noise = +$("l3-n").value; $("l3-nt").textContent = VTX(l3noise, 1); L3.dirty = true; };

// ---------------------------------------------------------------- L4 temps de propagation (diapo 18)
lesson("L4", {
  dur: 22, label: "Animation au ralenti : un changement d'état traverse quatre portes NON-ET, 12 ns par porte",
  steps: [
    [0, "Quatre portes NON-ET d'un 74HCT00, entrées reliées : chacune inverse le signal. Ralenti : ici, 1 seconde = 4 ns."],
    [2, "L'entrée A passe à 1. La sortie Y1 ne réagit pas tout de suite."],
    [5, "Après t<sub>PD</sub> = 12 ns, Y1 bascule. Le changement passe ensuite de porte en porte, avec 12 ns de retard à chaque fois."],
    [15, "Après 4 portes : 4 × 12 ns = 48 ns de retard entre A et Y4."],
  ],
  draw(t) {
    const sns = clamp((t - 0.5) * 4 - 6, -6, 60), val = (i, s) => (i % 2) ^ (s >= 12 * i ? 1 : 0);
    let s = '<svg viewBox="0 0 960 345">', prev = [40, 0];
    for (let i = 0; i < 4; i++) {
      const vi = val(i, sns), vo = val(i + 1, sns), g = gateAt("NON-ET", vi, vi, vo, 120 + i * 190, 18, 0.55, { labels: ["", ""], out: "" });
      if (i === 0) prev = [40, g.outY];
      s += wireP([prev, [g.inX, g.outY]], vi) + `<line x1="${g.inX}" y1="${g.inY[0]}" x2="${g.inX}" y2="${g.inY[1]}" style="${wireStyle(vi)}"/>` +
        `<circle cx="${g.inX}" cy="${g.outY}" r="3.5" style="fill:var(--ink)"/>` + g.svg;
      s += TX(i === 0 ? 30 : prev[0] + 22, g.outY - 10, i === 0 ? "A" : "Y" + i, { size: 17, bold: true, italic: true, anchor: i === 0 ? "end" : "start" });
      prev = [g.outX, g.outY];
      if (i === 3) s += wireP([prev, [930, g.outY]], vo) + TX(prev[0] + 22, g.outY - 10, "Y4", { size: 17, bold: true, italic: true });
    }
    s += TX(930, 122, sns >= 0 ? `t = ${Math.floor(sns)} ns` : "t < 0", { size: 20, bold: true, anchor: "end", color: "var(--head)" }) +
      TX(930, 140, "ralenti 250 millions de fois", { size: 12, anchor: "end", color: "var(--muted)" });
    const x0 = 140, w = 760, X = (ns) => x0 + w * (ns + 6) / 66;
    const rows = [0, 1, 2, 3, 4].map((i) => ({ name: i ? "Y" + i : "A", f: (u) => val(i, u - 6), color: i ? "var(--one)" : "var(--ink)" }));
    s += traceG(x0, 150, w, rows, sns + 6, 66, { rh: 32, dt: 0.25 });
    for (let i = 1; i <= 4; i++) if (sns >= 12 * i) {
      const y = 150 + i * 32 + 26 - 9;
      s += `<line x1="${X(12 * (i - 1))}" y1="${y}" x2="${X(12 * i) - 2}" y2="${y}" style="stroke:var(--bad);stroke-width:2"/><path d="M ${X(12 * i)} ${y} l -8 -4.5 v 9 z" style="fill:var(--bad)"/>` +
        TX((X(12 * (i - 1)) + X(12 * i)) / 2, y - 4, "12 ns", { size: 12, bold: true, anchor: "middle", color: "var(--bad)" });
    }
    [0, 12, 24, 36, 48, 60].forEach((ns) => { s += `<line x1="${X(ns)}" y1="306" x2="${X(ns)}" y2="312" style="stroke:var(--muted)"/>` + TX(X(ns), 328, ns + " ns", { size: 12, anchor: "middle", color: "var(--muted)" }); });
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L5 température et boîtiers (diapos 8 et 10)
const L5T = (t) => t < 4.5 ? 20 : t < 5.5 ? lerp(20, -30, ease(t - 4.5)) : t < 9.5 ? -30 : t < 10.5 ? lerp(-30, 80, ease(t - 9.5)) : 80;
lesson("L5", {
  dur: 31, label: "Animation : trois plages de température comparées à trois usages, puis les boîtiers DIP, SOIC et BGA",
  steps: [
    [0, "Un même CI existe en plusieurs plages de température. Un appareil de salon à 20 °C : les trois plages conviennent."],
    [5, "Une voiture en hiver à −30 °C : la plage Consumer (0 … 70 °C) ne suffit plus."],
    [10, "Une machine en extérieur, en plein été, à 80 °C : il faut au moins la plage Industrial (−40 … 85 °C)."],
    [17, "Boîtier DIP (traversant) : il s'enfiche dans une breadboard. C'est celui des prototypes au laboratoire."],
    [20.5, "Boîtier SOIC (CMS) : une machine le pose sur la carte. C'est celui de la production en série."],
    [24, "Boîtier BGA : des billes sous le boîtier. Impossible à souder au fer, il faut un four."],
  ],
  draw(t) {
    let s = '<svg viewBox="0 0 960 350">';
    const fa = 1 - prog(t, 16, 17);
    if (fa > 0) {
      const X = (c) => 170 + (c + 60) * 700 / 190, tc = L5T(t);
      s += `<g style="opacity:${fa}"><line x1="${X(-60)}" y1="60" x2="${X(130)}" y2="60" style="stroke:var(--ink);stroke-width:2"/>`;
      [-40, 0, 40, 85, 125].forEach((c) => { s += `<line x1="${X(c)}" y1="54" x2="${X(c)}" y2="66" style="stroke:var(--ink);stroke-width:2"/>` + TX(X(c), 46, String(c).replace("-", "−") + " °C", { size: 13, anchor: "middle" }); });
      [["Consumer", 0, 70], ["Industrial", -40, 85], ["Military", -55, 125]].forEach(([n, lo, hi], i) => {
        const y = 84 + i * 42, ok = tc >= lo && tc <= hi;
        s += TX(155, y + 20, n, { size: 16, bold: true, anchor: "end" }) +
          `<rect x="${X(lo)}" y="${y}" width="${X(hi) - X(lo)}" height="28" rx="6" style="fill:${ok ? "var(--ok-bg)" : "var(--bad-bg)"};stroke:${ok ? "var(--ok)" : "var(--bad)"};stroke-width:2"/>` +
          // libellé de la plage du côté opposé au trait rouge de la température (jamais posé sur le trait)
          (X(tc) > (X(lo) + X(hi)) / 2 ? TX(X(lo) + 10, y + 19, `${String(lo).replace("-", "−")} … ${hi} °C`, { size: 13.5, anchor: "start" })
            : TX(X(hi) - 10, y + 19, `${String(lo).replace("-", "−")} … ${hi} °C`, { size: 13.5, anchor: "end" })) + okMark(X(hi) + 18, y + 14, ok, 10);
      });
      const lab = tc > 50 ? "machine en extérieur, été" : tc < -10 ? "voiture en hiver" : "appareil de salon", xc = X(tc), bw = 310, bx = clamp(xc - bw / 2, 170, 920 - bw);
      s += `<line x1="${xc}" y1="40" x2="${xc}" y2="216" style="stroke:var(--bad);stroke-width:3"/><circle cx="${xc}" cy="60" r="7" style="fill:var(--bad)"/>` +
        `<rect x="${bx}" y="222" width="${bw}" height="40" rx="10" style="fill:var(--surface);stroke:var(--bad);stroke-width:2"/>` +
        TX(bx + bw / 2, 248, `${String(Math.round(tc)).replace("-", "−")} °C · ${lab}`, { size: 16, bold: true, anchor: "middle" }) + "</g>";
    }
    if (t >= 16.8) {
      const o = prog(t, 16.8, 17.6);
      s += `<g style="opacity:${o}">`;
      // DIP sur breadboard
      s += `<rect x="60" y="230" width="220" height="44" rx="4" style="fill:#EEF0F4;stroke:#B8BED0"/>`;
      for (let x = 72; x <= 268; x += 14) s += `<circle cx="${x}" cy="244" r="2.4" style="fill:#9AA2B4"/><circle cx="${x}" cy="262" r="2.4" style="fill:#9AA2B4"/>`;
      const yd = lerp(140, 196, prog(t, 17.5, 19.5));
      for (let i = 0; i < 7; i++) s += `<rect x="${117 + i * 17}" y="${yd + 28}" width="4" height="22" style="fill:#AEB5C4"/>`;
      s += `<rect x="110" y="${yd}" width="120" height="30" rx="4" style="fill:#3A3F52"/>` + TX(170, 306, "DIP (traversant)", { size: 17, bold: true, anchor: "middle" }) + TX(170, 328, "breadboard, prototypes", { size: 15, anchor: "middle", color: "var(--muted)" });
      // SOIC posé par une machine
      if (t >= 20.3) {
        const ys = lerp(110, 228, prog(t, 20.8, 22.5)), yn = lerp(ys, 50, prog(t, 23.2, 24.2));
        s += `<rect x="370" y="250" width="220" height="16" style="fill:#2F7D4F"/><rect x="440" y="246" width="12" height="4" style="fill:#D9B44A"/><rect x="508" y="246" width="12" height="4" style="fill:#D9B44A"/>`;
        s += `<polyline points="452,${ys + 8} 446,${ys + 8} 446,${ys + 20} 440,${ys + 20}" style="fill:none;stroke:#AEB5C4;stroke-width:3"/><polyline points="508,${ys + 8} 514,${ys + 8} 514,${ys + 20} 520,${ys + 20}" style="fill:none;stroke:#AEB5C4;stroke-width:3"/>`;
        s += `<rect x="452" y="${ys}" width="56" height="16" rx="2" style="fill:#3A3F52"/><g style="opacity:${1 - prog(t, 24, 24.8)}"><rect x="474" y="20" width="12" height="${Math.max(0, yn - 20)}" style="fill:var(--muted)"/><rect x="466" y="14" width="28" height="10" style="fill:var(--muted)"/></g>`;
        s += TX(480, 306, "SOIC (CMS)", { size: 17, bold: true, anchor: "middle" }) + TX(480, 328, "posé par machine, en série", { size: 15, anchor: "middle", color: "var(--muted)" });
      }
      // BGA dans le four
      if (t >= 23.8) {
        const yb = lerp(150, 216, prog(t, 24.2, 25.5));
        s += `<rect x="680" y="250" width="220" height="16" style="fill:#2F7D4F"/>`;
        for (let x = 752; x <= 828; x += 12) s += `<circle cx="${x}" cy="${yb + 26}" r="5" style="fill:#C8CEDA;stroke:#8A92A4"/>`;
        s += `<rect x="740" y="${yb}" width="100" height="20" rx="2" style="fill:#3A3F52"/>`;
        if (t >= 25.5) for (let i = 0; i < 3; i++) {
          let d = ""; const xb = 712 + i * 66, ph = t * 3 + i;
          for (let y = 0; y <= 60; y += 4) d += `${d ? " L" : "M"} ${xb + 8 * Math.sin(y / 9 + ph)} ${200 - y - ((t * 14) % 12)}`;
          s += `<path d="${d}" fill="none" style="stroke:var(--warn);stroke-width:3;opacity:.8"/>`;
        }
        s += TX(790, 306, "BGA (billes)", { size: 17, bold: true, anchor: "middle" }) + TX(790, 328, "soudé dans un four", { size: 15, anchor: "middle", color: "var(--muted)" });
      }
      s += "</g>";
    }
    return s + "</svg>";
  },
});
