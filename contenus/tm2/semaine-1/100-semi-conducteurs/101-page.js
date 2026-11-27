// ================================================================ leçons animées de la page 101 (présentation 100 Semi-conducteurs)

// ---------------------------------------------------------------- cristal de silicium à plat (3 × 3 atomes)
// o = { pairs : liaisons rompues (paires électron-trou), center : "Si" | "P" | "B", t : temps (agitation), field : -1 | 0 | 1 (dérive) }
const BONDS = [[1, 1, "h"], [0, 0, "v"], [1, 0, "h"], [2, 1, "v"], [0, 2, "h"], [1, 1, "v"], [0, 1, "h"], [2, 0, "v"], [1, 2, "h"], [0, 1, "v"], [0, 0, "h"], [1, 0, "v"]];
function latticeG(ox, oy, d, o = {}) {
  const t = o.t || 0, pairs = o.pairs || 0, center = o.center || "Si";
  const P = (i, j) => [ox + i * d, oy + j * d];
  let s = "", holes = [], frees = [];
  const e = (x, y) => `<circle cx="${x}" cy="${y}" r="${d * 0.055}" style="fill:var(--blue)"/>`;
  const hole = (x, y) => `<circle cx="${x}" cy="${y}" r="${d * 0.07}" style="fill:var(--surface);stroke:var(--bad);stroke-width:2.2"/>` +
    TX(x, y + d * 0.045, "+", { size: d * 0.12, bold: true, anchor: "middle", color: "var(--bad)" });
  // liaisons vers l'extérieur
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
    const [x, y] = P(i, j);
    [[-1, 0], [1, 0], [0, -1], [0, 1]].forEach(([dx, dy]) => {
      const ni = i + dx, nj = j + dy;
      if (ni >= 0 && ni < 3 && nj >= 0 && nj < 3) return;
      // les liaisons partent du bord de l'atome : aucun trait sous le symbole (Si, B, P)
      s += `<line x1="${x + dx * d * 0.2}" y1="${y + dy * d * 0.2}" x2="${x + dx * d * 0.42}" y2="${y + dy * d * 0.42}" style="stroke:var(--muted);stroke-width:1.5"/>`;
      s += e(x + dx * d * 0.3 - dy * d * 0.065, y + dy * d * 0.3 + dx * d * 0.065) + e(x + dx * d * 0.3 + dy * d * 0.065, y + dy * d * 0.3 - dx * d * 0.065);
    });
  }
  // liaisons internes : deux électrons, ou une paire rompue
  const broken = new Set(BONDS.slice(0, pairs).map((b) => b.join(",")));
  if (center === "B") broken.add("1,1,h");
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) [["h", 1, 0], ["v", 0, 1]].forEach(([k, dx, dy]) => {
    if (i + dx > 2 || j + dy > 2) return;
    const [x0, y0] = P(i, j), [x1, y1] = P(i + dx, j + dy), mx = (x0 + x1) / 2, my = (y0 + y1) / 2, nx = -dy * d * 0.065, ny = dx * d * 0.065;
    s += `<line x1="${x0 + dx * d * 0.2}" y1="${y0 + dy * d * 0.2}" x2="${x1 - dx * d * 0.2}" y2="${y1 - dy * d * 0.2}" style="stroke:var(--muted);stroke-width:1.5"/>`;
    s += e(mx + nx, my + ny);
    // électron libéré : posé à un quart de maille de sa liaison, vers l'intérieur de la case (jamais sur un trou, un atome ou un autre électron)
    if (broken.has([i, j, k].join(","))) { holes.push([mx - nx, my - ny]); if (!(center === "B" && [i, j, k].join(",") === "1,1,h")) frees.push([mx + dy * d * 0.27 * (i < 2 ? 1 : -1), my + dx * d * 0.27 * (j < 2 ? 1 : -1), frees.length]); }
    else s += e(mx - nx, my - ny);
  });
  holes.forEach(([x, y]) => { s += hole(x, y); });
  // atomes
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
    const [x, y] = P(i, j), sym = i === 1 && j === 1 ? center : "Si";
    s += `<circle cx="${x}" cy="${y}" r="${d * 0.2}" style="fill:${sym === "Si" ? "#3A428C" : "#297FD5"};stroke:var(--surface);stroke-width:2"/>` +
      TX(x, y + d * 0.065, sym, { size: d * 0.18, bold: true, anchor: "middle", color: "#fff" });
  }
  if (center === "P") frees.push([ox + d * 1.5, oy + d * 0.5, 7]);
  // électrons libres : ils s'agitent dans les cases vides ; avec un champ, ils dérivent
  frees.forEach(([x, y, k]) => {
    const fx = o.field ? ((x - ox + o.field * -1 * t * d * 0.35) % (2 * d) + 2 * d) % (2 * d) + ox : x + Math.sin(t * 2.1 + k) * d * 0.05;
    const fy = y + Math.cos(t * 1.7 + k * 1.3) * d * 0.05;
    s += `<circle cx="${fx}" cy="${fy}" r="${d * 0.075}" style="fill:var(--blue);stroke:#242852;stroke-width:2"/>` +
      TX(fx, fy + d * 0.04, "−", { size: d * 0.12, bold: true, anchor: "middle", color: "#fff" });
  });
  return s;
}
function thermo(x, y, h, th, tmin = 20, tmax = 60) {
  const f = clamp((th - tmin) / (tmax - tmin)), r = 16;
  return `<rect x="${x - 9}" y="${y}" width="18" height="${h}" rx="9" style="fill:var(--surface);stroke:var(--ink);stroke-width:2"/>` +
    `<rect x="${x - 5}" y="${y + h - h * (0.1 + 0.9 * f)}" width="10" height="${h * (0.1 + 0.9 * f)}" rx="5" style="fill:var(--bad)"/>` +
    `<circle cx="${x}" cy="${y + h + r - 4}" r="${r}" style="fill:var(--bad);stroke:var(--ink);stroke-width:2"/>` +
    TX(x + 26, y + h - h * (0.1 + 0.9 * f) + 6, Math.round(th) + " °C", { size: 20, bold: true });
}

// ---------------------------------------------------------------- L1 trois familles (diapos 3 et 4)
lesson("L1", {
  dur: 30, label: "Animation : l'échelle des résistivités, avec les conducteurs, les semi-conducteurs et les isolants, puis les électrons libres de chaque famille",
  steps: [
    [0, "La résistivité dit si un matériau conduit bien. L'échelle va de 10<sup>−9</sup> à 10<sup>16</sup> Ω·m : chaque graduation multiplie par 100."],
    [7, "Le cuivre à gauche, la porcelaine à droite. Le silicium est entre les deux."],
    [15, "Pourquoi ? Le métal a beaucoup d'électrons libres, le silicium très peu, l'isolant aucun."],
    [24, "À retenir : un semi-conducteur est un matériau dont on peut régler la conduction."],
  ],
  draw(t) {
    let s = '<svg viewBox="0 0 960 430">';
    const x0 = 60, x1 = 900, X = (e) => x0 + (x1 - x0) * (e + 9) / 25, y = 90;
    const z = prog(t, 0.3, 1.5);
    // couleurs fixes (pas celles du thème) : le texte marine reste lisible sur les trois zones, en clair comme en sombre
    [[-9, -5, "#ACCBF9", "Conducteurs"], [-5, 8, "#E8EFFB", "Semi-conducteurs"], [8, 16, "#C9D2E3", "Isolants"]].forEach(([a, b, c, n], i) => {
      // la zone se déroule (opaque), puis son nom apparaît : jamais de texte marine sur un fond à moitié transparent
      const o = prog(t, 0.5 + i * 0.8, 1.5 + i * 0.8), ol = prog(t, 1.3 + i * 0.8, 1.7 + i * 0.8);
      if (o > 0) s += `<rect x="${X(a)}" y="${y}" width="${(X(b) - X(a)) * o}" height="46" style="fill:${c}"/>`;
      if (ol > 0) s += TX((X(a) + X(b)) / 2, y + 30, n, { size: 18, bold: true, anchor: "middle", color: "#242852", op: ol });
    });
    s += `<line x1="${x0}" y1="${y + 60}" x2="${x1}" y2="${y + 60}" style="stroke:var(--ink);stroke-width:2;opacity:${z}"/>`;
    for (let e = -9; e <= 15; e += 4) s += `<line x1="${X(e)}" y1="${y + 56}" x2="${X(e)}" y2="${y + 64}" style="stroke:var(--ink);opacity:${z}"/>` +
      TX(X(e), y + 84, `10<tspan font-size="11" dy="-7">${e < 0 ? "−" + -e : e}</tspan>`, { size: 15, anchor: "middle", op: z });
    s += TX((x0 + x1) / 2, y + 108, "résistivité ρ [Ω·m]", { size: 14, anchor: "middle", italic: true, color: "var(--muted)", op: z });
    [["cuivre", -7.75, 0, 7], ["silicium pur", 3.36, 0, 9], ["porcelaine", 12, 0, 11]].forEach(([n, e, h, t0]) => {
      const o = prog(t, t0, t0 + 0.8); if (o <= 0) return;
      const yl = y - 14 - h * 24;
      s += `<line x1="${X(e)}" y1="${yl + 4}" x2="${X(e)}" y2="${y}" style="stroke:var(--blue);stroke-width:3;opacity:${o}"/>` +
        TX(X(e), yl, n, { size: 16, bold: true, anchor: "middle", op: o });
    });
    const f = prog(t, 15, 16.2);
    if (f > 0) [["Métal", 30], ["Semi-conducteur", 3], ["Isolant", 0]].forEach(([n, k], i) => {
      const bx = 60 + i * 290, by = 240;
      s += `<g style="opacity:${f}"><rect x="${bx}" y="${by}" width="260" height="130" rx="12" style="fill:var(--surface);stroke:var(--line);stroke-width:2"/>` +
        TX(bx + 14, by + 26, n, { size: 17, bold: true, color: "var(--head)" }) +
        TX(bx + 246, by + 26, k ? (k > 10 ? "beaucoup" : "très peu") : "aucun", { size: 14, anchor: "end", color: "var(--muted)" });
      for (let q = 0; q < k; q++) {
        const ex = bx + 22 + ((q * 67) % 216) + Math.sin(t * 2.3 + q * 1.9) * 9, ey = by + 52 + ((q * 53) % 64) + Math.cos(t * 2.9 + q) * 7;
        s += `<circle cx="${ex}" cy="${ey}" r="5" style="fill:var(--blue)"/>`;
      }
      s += "</g>";
    });
    const r = prog(t, 24, 25);
    if (r > 0) s += `<rect x="60" y="384" width="840" height="40" rx="8" style="fill:#242852;opacity:${r}"/>` +
      TX(480, 410, "Semi-conducteur : on peut régler sa conduction.", { size: 18, bold: true, anchor: "middle", color: "#fff", op: r });
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L2 chaleur (diapos 6 et 7)
lesson("L2", {
  dur: 28, label: "Animation : un cristal de silicium qu'on chauffe de 20 à 60 °C ; des liaisons se rompent et des paires électron-trou apparaissent",
  steps: [
    [0, "Le cristal de silicium : chaque atome partage ses 4 électrons de valence avec 4 voisins. Tout est rangé : c'est un monocristal."],
    [4, "On chauffe. Une liaison se rompt : un électron devient libre, il laisse un trou (une place vide, qui se comporte comme une charge +)."],
    [12, "Plus il fait chaud, plus il y a de paires électron-trou : environ deux fois plus tous les 10 °C. La résistance baisse fortement."],
    [21, "Le silicium pur conduit par ces paires : c'est la conduction intrinsèque. Dans un métal, c'est l'inverse : la résistance monte un peu."],
  ],
  draw(t) {
    const th = 20 + 40 * prog(t, 4, 20), k = Math.pow(2, (th - 20) / 10);
    let s = '<svg viewBox="0 0 960 380">' + latticeG(120, 70, 120, { pairs: t < 4 ? 0 : Math.min(8, Math.max(1, Math.floor(k))), t });
    s += thermo(560, 60, 220, th);
    s += TX(660, 110, "Porteurs libres", { size: 18, bold: true, color: "var(--head)" }) + TX(660, 150, "× " + (Math.round(k * 10) / 10).toString().replace(".", ","), { size: 34, bold: true, color: "var(--blue)" });
    s += TX(660, 190, "(par rapport à 20 °C)", { size: 14, color: "var(--muted)" });
    const R = 1 / k;
    s += TX(660, 250, "Résistance", { size: 18, bold: true, color: "var(--head)" }) +
      `<rect x="660" y="262" width="240" height="18" rx="9" style="fill:var(--line)"/><rect x="660" y="262" width="${240 * R}" height="18" rx="9" style="fill:var(--bad)"/>`;
    const m = prog(t, 21, 22);
    if (m > 0) s += `<g style="opacity:${m}"><rect x="560" y="310" width="380" height="56" rx="10" style="fill:var(--tint)"/>` +
      TX(576, 334, "Cuivre (métal) : R monte un peu.", { size: 16, bold: true }) + TX(576, 356, "Silicium : R baisse fortement.", { size: 16, bold: true, color: "var(--blue)" }) + "</g>";
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L3 champ électrique (diapo 8)
lesson("L3", {
  dur: 26, label: "Animation : un barreau de silicium entre deux électrodes ; avec une tension, les électrons vont vers le plus et les trous vers le moins, puis le claquage",
  steps: [
    [0, "Sans tension, les électrons libres et les trous s'agitent dans tous les sens : pas de courant."],
    [5, "Avec une tension, le champ électrique pousse les électrons vers le + et les trous vers le −. Les deux courants s'additionnent."],
    [14, "Champ très fort : les liaisons cèdent, les porteurs se multiplient et le courant monte d'un coup. C'est le claquage, utilisé par la diode Zener."],
    [21, "Un champ peut aussi commander la conduction : c'est le transistor à effet de champ (FET)."],
  ],
  draw(t) {
    const x0 = 140, x1 = 760, y0 = 90, y1 = 250, on = t >= 5, strong = t >= 14 && t < 21;
    let s = '<svg viewBox="0 0 960 360">';
    s += `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" rx="6" style="fill:var(--tint);stroke:#242852;stroke-width:2"/>`;
    s += `<rect x="${x0 - 22}" y="${y0 - 14}" width="22" height="${y1 - y0 + 28}" style="fill:var(--muted)"/><rect x="${x1}" y="${y0 - 14}" width="22" height="${y1 - y0 + 28}" style="fill:var(--muted)"/>`;
    if (on) s += TX(x0 - 11, y0 - 24, "+", { size: 30, bold: true, anchor: "middle", color: "var(--bad)" }) + TX(x1 + 11, y0 - 24, "−", { size: 30, bold: true, anchor: "middle", color: "var(--ink)" });
    const n = strong ? 14 + Math.min(16, Math.floor((t - 14) * 4)) : 7, W = x1 - x0 - 40;
    for (let q = 0; q < n; q++) {
      // trois couloirs par sorte de porteur, porteurs régulièrement espacés dans chaque couloir : jamais deux porteurs l'un sur l'autre
      const m = Math.ceil(n / 3), lane = q % 3, base = Math.floor(q / 3) * W / m + lane * W / (3 * m);
      const drift = on ? (strong ? 160 : 55) * (t - 5) : 0, jit = Math.sin(t * 3 + q * 1.7) * 6;
      const ex = x0 + 20 + (((base - drift + jit) % W) + W) % W, ey = y0 + 22 + lane * 24 + Math.cos(t * 2.5 + q) * 2;
      const hx = x0 + 20 + (((base + W / (6 * m) + drift - jit) % W) + W) % W, hy = y0 + 92 + lane * 24 + Math.sin(t * 2.2 + q) * 2;
      s += `<circle cx="${ex}" cy="${ey}" r="10" style="fill:var(--blue);stroke:#242852;stroke-width:1.5"/>` + TX(ex, ey + 5, "−", { size: 14, bold: true, anchor: "middle", color: "#fff" });
      s += `<circle cx="${hx}" cy="${hy}" r="10" style="fill:var(--surface);stroke:var(--bad);stroke-width:2"/>` + TX(hx, hy + 5, "+", { size: 14, bold: true, anchor: "middle", color: "var(--bad)" });
    }
    if (on && t < 21) {
      s += `<line x1="${x0 + 80}" y1="285" x2="${x1 - 80}" y2="285" style="stroke:#242852;stroke-width:3"/><path d="M ${x1 - 80} 285 l -14 -8 v 16 z" style="fill:#242852"/>`;
      s += TX((x0 + x1) / 2, 312, "champ électrique et sens du courant (du + vers le −)", { size: 15, anchor: "middle", color: "var(--muted)" });
      s += TX(800, 120, "électrons", { size: 16, bold: true, color: "var(--blue)" }) + TX(800, 140, "vers le +", { size: 16, color: "var(--blue)" });
      s += TX(800, 200, "trous", { size: 16, bold: true, color: "var(--bad)" }) + TX(800, 220, "vers le −", { size: 16, color: "var(--bad)" });
      const I = strong ? 1 : 0.25;
      s += TX(140, 345, "Courant", { size: 16, bold: true }) + `<rect x="230" y="332" width="400" height="16" rx="8" style="fill:var(--line)"/><rect x="230" y="332" width="${400 * I}" height="16" rx="8" style="fill:${strong ? "var(--bad)" : "var(--blue)"}"/>`;
      if (strong) s += TX(650, 345, "claquage !", { size: 16, bold: true, color: "var(--bad)" });
    }
    const f = prog(t, 21, 22);
    if (f > 0) s += `<g style="opacity:${f}"><rect x="${x0 + 120}" y="40" width="${x1 - x0 - 240}" height="26" rx="4" style="fill:#242852"/>` +
      TX((x0 + x1) / 2, 59, "grille (électrode isolée) : elle attire les porteurs", { size: 15, bold: true, anchor: "middle", color: "#fff" }) +
      TX((x0 + x1) / 2, 300, "FET : le champ de la grille commande la conduction", { size: 17, bold: true, anchor: "middle", color: "var(--head)" }) + "</g>";
    return s + "</svg>";
  },
});

// ---------------------------------------------------------------- L4 dopage (diapo 9)
lesson("L4", {
  dur: 24, label: "Animation : un atome de silicium remplacé par du phosphore, qui libère un électron, puis par du bore, qui laisse un trou",
  steps: [
    [0, "Silicium pur : toutes les liaisons sont complètes. Doper, c'est remplacer très peu d'atomes par un autre élément."],
    [4, "Phosphore P : 5 électrons de valence. Quatre forment les liaisons, le cinquième devient libre. Type n : électrons majoritaires."],
    [12, "Bore B : 3 électrons de valence. Il manque un électron pour la 4e liaison : il reste un trou. Type p : trous majoritaires."],
    [19, "Dans les deux cas, le morceau reste neutre. Une zone p collée à une zone n forme une jonction PN : la diode."],
  ],
  draw(t) {
    const center = t < 4 ? "Si" : t < 12 ? "P" : t < 19 ? "B" : "P";
    let s = '<svg viewBox="0 0 960 370">';
    if (t < 19) s += latticeG(130, 70, 115, { center, t });
    else s += `<g transform="translate(40 70) scale(0.62)">` + latticeG(70, 30, 115, { center: "P", t }) + `</g><g transform="translate(260 70) scale(0.62)">` + latticeG(70, 30, 115, { center: "B", t }) + "</g>";
    const box = (y, a, b, c) => `<rect x="560" y="${y}" width="380" height="96" rx="12" style="fill:var(--tint)"/>` + TX(578, y + 30, a, { size: 20, bold: true, color: "var(--blue)" }) +
      TX(578, y + 58, b, { size: 16 }) + TX(578, y + 82, c, { size: 16, bold: true });
    if (t >= 4) s += `<g style="opacity:${prog(t, 4, 5)}">` + box(60, "Type n (phosphore)", "5 électrons de valence : 1 en trop", "majoritaires : électrons") + "</g>";
    if (t >= 12) s += `<g style="opacity:${prog(t, 12, 13)}">` + box(170, "Type p (bore)", "3 électrons de valence : 1 trou", "majoritaires : trous") + "</g>";
    if (t >= 19) s += `<g style="opacity:${prog(t, 19, 20)}"><rect x="40" y="300" width="900" height="46" rx="10" style="fill:#242852"/>` +
      TX(490, 330, "Les deux restent neutres · zone p + zone n = jonction PN = diode", { size: 18, bold: true, anchor: "middle", color: "#fff" }) +
      TX(140, 285, "type n", { size: 16, bold: true, anchor: "middle", color: "var(--head)" }) + TX(360, 285, "type p", { size: 16, bold: true, anchor: "middle", color: "var(--head)" }) + "</g>";
    return s + "</svg>";
  },
});
