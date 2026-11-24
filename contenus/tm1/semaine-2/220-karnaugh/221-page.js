// ================================================================ leçons animées de la page 221 (présentation 220)
// Sortie S, entrées A, B, C, D (REGLES 3.4). Tableaux : kmapSVG du gabarit (modèle de Gaël). Briques : moteur/pages/common.js.

const RINC = tabVals(3, (a, b, c) => (b | (a & c)) ? 1 : 0);
// table de vérité dessinée à gauche de la leçon
function miniTable(x, y, vals, actif, nf) {
  let h = "", rh = 30, cw = 40;
  ["C", "B", "A", "S"].forEach((t, j) => { h += `<rect x="${x + j * cw}" y="${y}" width="${cw}" height="${rh}" style="fill:var(--light)"/>` + TX(x + j * cw + cw / 2, y + 21, t, { size: 16, bold: true, anchor: "middle", color: "#242852" }); });
  for (let k = 0; k < 8; k++) {
    const yy = y + rh * (k + 1);
    h += `<rect x="${x}" y="${yy}" width="${4 * cw}" height="${rh}" style="fill:${k === actif ? "#FFE9A8" : "var(--surface)"};stroke:var(--line)"/>`;
    [(k >> 2) & 1, (k >> 1) & 1, k & 1, vals[k]].forEach((v, j) => { h += TX(x + j * cw + cw / 2, yy + 21, String(v), { size: 16, anchor: "middle", mono: true, bold: j === 3 && v === 1, color: j === 3 && v === 1 ? "var(--one)" : "var(--ink)", op: k < nf || j < 3 ? 1 : 0.35 }); });
  }
  return h;
}
const imbrique = (svg, x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})">${svg.replace(/^<svg[^>]*>/, "").replace(/<\/svg>$/, "")}</g>`;

// ---------------------------------------------------------------- L1 remplir (diapos 3 et 4)
lesson("L1", {
  dur: 30, label: "Animation : chaque ligne de la table de la buse de rinçage est reportée dans sa case, repérée par la ligne C et la colonne BA",
  steps: [
    [0, "La table a 8 lignes, le tableau a 8 cases : une case par ligne."],
    [3, "Chaque ligne trouve sa case avec les codes gris : la ligne C, puis la colonne BA."],
    [12, "L'ordre des colonnes est 00, 01, 11, 10 : la ligne 011 va dans la 3e colonne, la ligne 010 dans la 4e."],
    [21, "Les zones jaunes disent la même chose : la case 101 est dans les zones C et A, hors de la zone B."],
  ],
  draw(t) {
    const k = t < 3 ? -1 : Math.min(7, Math.floor((t - 3) / 2.6)), nf = t < 3 ? 0 : Math.min(8, Math.floor((t - 3) / 2.6) + 1);
    const vals = RINC.map((v, i) => (i < nf ? v : null));
    let h = '<svg viewBox="0 0 960 380">' + miniTable(40, 40, RINC, k, nf);
    h += imbrique(kmapSVG(3, vals, { hl: k >= 0 && nf <= 8 ? new Set([k]) : new Set(), zone: t >= 21 ? (t < 24 ? "C" : t < 27 ? "A" : "B") : null, u: 70 }), 300, 20, 1.1);
    if (k >= 0) h += TX(300, 360, `${(k >> 2) & 1}${(k >> 1) & 1}${k & 1}  →  ligne C = ${(k >> 2) & 1}, colonne BA = ${(k >> 1) & 1}${k & 1}`, { size: 20, bold: true, color: "var(--blue)" });
    return h + "</svg>";
  },
});

// ---------------------------------------------------------------- L2 lire un groupe (diapo 6)
lesson("L2", {
  dur: 28, label: "Animation : le groupe vert puis le groupe rouge du tableau de la rinceuse ; chaque zone jaune s'allume pour dire si le groupe est dedans, dehors ou à cheval",
  steps: [
    [0, "Groupe vert : 4 cases. On regarde chaque zone jaune l'une après l'autre."],
    [3, "Zone C : le groupe a des cases dedans et dehors. Il est à cheval, C disparaît."],
    [6, "Zone A : à cheval aussi, A disparaît. Zone B : tout le groupe est dedans, il reste B."],
    [13, "Groupe rouge : dans la zone C, dans la zone A, à cheval sur B. Il reste A · C."],
    [22, "On additionne les termes : S = B + A · C."],
  ],
  draw(t) {
    const g = t < 13 ? [[2, 3, 6, 7]] : [[2, 3, 6, 7], [5, 7]];
    const z = t < 3 ? null : t < 6 ? "C" : t < 9 ? "A" : t < 13 ? "B" : t < 16 ? "C" : t < 19 ? "A" : t < 22 ? "B" : null;
    let h = '<svg viewBox="0 0 960 380">' + imbrique(kmapSVG(3, RINC, { groups: g.map((k) => ({ k })), zone: z, u: 70 }), 30, 20, 1.1);
    const L = [[3, "C : à cheval → disparaît", KCOL[0]], [6, "A : à cheval → disparaît", KCOL[0]], [9, "B : dans la zone → B", KCOL[0]],
      [13, "C : dans la zone → C", KCOL[1]], [16, "A : dans la zone → A", KCOL[1]], [19, "B : à cheval → disparaît", KCOL[1]]];
    L.forEach(([t0, s, c], i) => { const op = prog(t, t0, t0 + 0.8); if (op > 0) h += TX(560, 60 + i * 44 + (i >= 3 ? 16 : 0), s, { size: 22, bold: true, color: c, op }); });
    const op = prog(t, 22, 23);
    if (op > 0) h += TX(560, 350, "S = B + A · C", { size: 34, bold: true, color: "var(--head)", op });
    return h + "</svg>";
  },
});

// ---------------------------------------------------------------- L3 les bords se touchent (diapo 8)
const K4 = tabVals(4, (a, b, c, d) => (a === c) ? 1 : 0);
lesson("L3", {
  dur: 24, label: "Animation : dans un tableau à 4 variables, les quatre coins forment un seul groupe ouvert vers l'extérieur, puis le carré du centre",
  steps: [
    [0, "Tableau de 16 cases : A en haut, B en bas, C à gauche, D à droite."],
    [4, "La colonne de gauche touche la colonne de droite, la ligne du haut touche celle du bas : les quatre coins sont voisins."],
    [9, "Les coins forment un groupe de 4, dessiné ouvert vers l'extérieur. Hors de A, hors de C, à cheval sur B et D : il reste Ā · C̄."],
    [15, "Le carré du centre est dans les zones A et C : il reste A · C. B et D ont disparu."],
  ],
  draw(t) {
    const g = t < 9 ? [] : t < 15 ? [[0, 2, 8, 10]] : [[0, 2, 8, 10], [5, 7, 13, 15]];
    const hl = t >= 4 && t < 9 ? new Set([0, 2, 8, 10]) : new Set();
    let h = '<svg viewBox="0 0 960 420">' + imbrique(kmapSVG(4, K4, { groups: g.map((k) => ({ k })), hl, u: 64 }), 40, 10, 1.0);
    if (t >= 4 && t < 9) {
      const op = prog(t, 4, 5);
      h += TX(560, 120, "les bords se touchent", { size: 26, bold: true, color: "var(--blue)", op });
    }
    if (t >= 9) h += `<text x="560" y="160" font-size="30" font-weight="700" style="fill:${KCOL[0]}">Ā · C̄</text>`;
    if (t >= 15) h += `<text x="560" y="220" font-size="30" font-weight="700" style="fill:${KCOL[1]}">A · C</text>` + TX(560, 300, "S = Ā · C̄ + A · C", { size: 32, bold: true, color: "var(--head)" });
    return h + "</svg>";
  },
});

// ---------------------------------------------------------------- L4 cas X (diapo 12)
const VID = tabVals(3, (a, b, c) => (c | (!a & b)) ? 1 : 0, [4, 5]);
lesson("L4", {
  dur: 22, label: "Animation : la pompe de vidange ; les deux X agrandissent le groupe de la zone C, puis le 1 restant forme un groupe de 2",
  steps: [
    [0, "Les cases 100 et 101 valent X : ces combinaisons n'arrivent jamais."],
    [4, "Sans les X, la zone C donne un groupe de 2 seulement : B · C."],
    [9, "Avec les X, toute la zone C forme un groupe de 4 : il reste C."],
    [15, "Le 1 de la case 010 s'allie à la case 110 : hors de A, dans la zone B. Il reste Ā · B. S = C + Ā · B."],
  ],
  draw(t) {
    const g = t < 4 ? [] : t < 9 ? [[6, 7]] : t < 15 ? [[4, 5, 6, 7]] : [[4, 5, 6, 7], [2, 6]];
    let h = '<svg viewBox="0 0 960 360">' + imbrique(kmapSVG(3, VID, { groups: g.map((k) => ({ k })), hl: t < 4 ? new Set([4, 5]) : new Set(), u: 70 }), 30, 20, 1.1);
    const s = t < 4 ? "" : t < 9 ? "sans les X : S = B · C + …" : t < 15 ? "avec les X : C" : "S = C + Ā · B";
    if (s) h += TX(560, 180, s, { size: 30, bold: true, color: t < 9 ? "var(--muted)" : "var(--head)" });
    return h + "</svg>";
  },
});
