const $ = (id) => document.getElementById(id);
const FN = {
  "NON": (a) => 1 - a, "ET": (a, b) => a & b, "OU": (a, b) => a | b, "NON-ET": (a, b) => 1 - (a & b),
  "NON-OU": (a, b) => 1 - (a | b), "OUX": (a, b) => a ^ b, "NON-OUX": (a, b) => 1 - (a ^ b),
};
const QUAL = { "NON": "1", "ET": "&amp;", "OU": "≥1", "NON-ET": "&amp;", "NON-OU": "≥1", "OUX": "=1", "NON-OUX": "=1" };
const NEG = { "NON": 1, "ET": 0, "OU": 0, "NON-ET": 1, "NON-OU": 1, "OUX": 0, "NON-OUX": 1 };
const EQH = {
  "NON": 'Y = <span class="ov">A</span>', "ET": "Y = A · B", "OU": "Y = A + B", "NON-ET": 'Y = <span class="ov">A · B</span>',
  "NON-OU": 'Y = <span class="ov">A + B</span>', "OUX": "Y = A ⊕ B", "NON-OUX": 'Y = <span class="ov">A ⊕ B</span>',
};
// table de vérité, entrées du poids fort au poids faible : [B, A, Y] ou [A, Y]
function tdv(key) {
  if (key === "NON") return [[0, 1], [1, 0]];
  const r = [];
  for (const b of [0, 1]) for (const a of [0, 1]) r.push([b, a, FN[key](a, b)]);
  return r;
}
const wireStyle = (v) => v === 1 ? "stroke:var(--one);stroke-width:5" : (v === 0 ? "stroke:var(--zero);stroke-width:3" : "stroke:var(--muted);stroke-width:3");

// Symbole CEI 60617-12 : rectangle, qualificatif, cercle de négation
function gateParts(key, a, b, y, opt = {}) {
  const n = key === "NON" ? 1 : 2, w = 90, h = n === 1 ? 90 : 116, x0 = 84, y0 = 14, L = 50;
  const labels = opt.labels || ["A", "B"], out = opt.out != null ? opt.out : "Y";
  const ys = n === 1 ? [y0 + h / 2] : [y0 + h * 0.28, y0 + h * 0.72];
  let s = "";
  const vin = n === 1 ? [a] : [a, b];
  ys.forEach((yy, i) => {
    s += `<line x1="${x0 - L}" y1="${yy}" x2="${x0}" y2="${yy}" style="${wireStyle(vin[i])}"/>`;
    s += `<text x="${x0 - L - 8}" y="${yy + 6}" text-anchor="end" font-size="18" font-style="italic" font-weight="700" style="fill:var(--ink)">${labels[i]}</text>`;
  });
  s += `<rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="2" style="fill:var(--surface);stroke:var(--ink);stroke-width:3"/>`;
  s += `<text x="${x0 + w / 2}" y="${y0 + 30}" text-anchor="middle" font-size="24" font-weight="700" style="fill:var(--ink)">${QUAL[key]}</text>`;
  let xo = x0 + w;
  if (NEG[key]) { s += `<circle cx="${xo + 7}" cy="${y0 + h / 2}" r="7" style="fill:var(--surface);stroke:var(--ink);stroke-width:2.5"/>`; xo += 14; }
  s += `<line x1="${xo}" y1="${y0 + h / 2}" x2="${xo + L}" y2="${y0 + h / 2}" style="${wireStyle(y)}"/>`;
  s += `<text x="${xo + L + 8}" y="${y0 + h / 2 + 6}" font-size="18" font-style="italic" font-weight="700" style="fill:var(--ink)">${out}</text>`;
  return { w: x0 + w + 2 * L + 50, h: h + 2 * y0, body: s, inX: x0 - L, inY: ys, outX: xo + L, outY: y0 + h / 2 };
}
function gateSVG(key, a, b, y, opt = {}) {
  const p = gateParts(key, a, b, y, opt);
  return `<svg viewBox="0 0 ${p.w} ${p.h}" width="${p.w * (opt.scale || 1)}" role="img" aria-label="Symbole CEI de la porte ${key}">${p.body}</svg>`;
}
// porte placée dans un dessin : renvoie le groupe SVG et les points de raccordement (entrées, sortie)
function gateAt(key, a, b, y, X, Y, s = 1, opt = {}) {
  const p = gateParts(key, a, b, y, opt);
  return { svg: `<g transform="translate(${X} ${Y}) scale(${s})">${p.body}</g>`, inX: X + p.inX * s, inY: p.inY.map((v) => Y + v * s), outX: X + p.outX * s, outY: Y + p.outY * s, w: p.w * s, h: p.h * s };
}

// suivi des exercices réussis (en mémoire seulement)
const DONE = new Set();
function markDone(id, ok) {
  if (ok) DONE.add(id); else DONE.delete(id);
  const dots = document.querySelectorAll(".score .dots i");
  dots.forEach((d) => d.classList.toggle("on", DONE.has(d.dataset.id)));
  $("score-n").textContent = DONE.size;
}
function feedback(el, kind, title, html) {
  el.className = "fb " + kind;
  el.innerHTML = `<b>${title}</b>${html}`;
}
const fmtV = (x) => String(x).replace(".", ",") + " V";
// liens externes dans un nouvel onglet
// démarrage : tout de suite si la page est déjà chargée (certains lecteurs injectent la page après DOMContentLoaded)
const ready = (f) => { if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", f); else f(); };
// liens externes : <a href> simples ; le lecteur d'artefact les ouvre lui-même hors de la page (pas de target="_blank", refusé dans le cadre isolé)
// typographie française : espaces insécables (avant « : ; ? ! », nombre + unité, « A = 1 », plages « 0 … 70 »)
const NBSP = "\u00a0";
function typo(s) {
  return s
    .replace(/ ([:;?!»])/g, NBSP + "$1").replace(/« /g, "«" + NBSP)
    .replace(/ (=|·|×|≥|≤|<|>|→|⊕|…|\+) /g, NBSP + "$1" + NBSP)
    .replace(/(\d) (ou|à) (?=[\d−])/g, "$1" + NBSP + "$2" + NBSP)
    .replace(/(\d) (?=(V|mV|mA|ns|ms|µs|s|°C|%|ko|L|[a-zà-ÿ]))/g, "$1" + NBSP)
    .replace(/\b(p\.|chap\.|diapos?|N°|Floyd|LZ) (?=\d)/g, "$1" + NBSP);
}
function typoTree(root) {
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: (n) => /^(SCRIPT|STYLE)$/.test(n.parentNode.nodeName) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
  let n; while ((n = w.nextNode())) { const t = typo(n.nodeValue); if (t !== n.nodeValue) n.nodeValue = t; }
}
const inStage = (n) => { const e = n.nodeType === 1 ? n : n.parentElement; return !!(e && e.closest && e.closest(".ls-stage, .nt")); };
ready(() => {
  typoTree(document.body);
  new MutationObserver((ms) => ms.forEach((m) => { if (inStage(m.target)) return; m.addedNodes.forEach((x) => { if (x.nodeType === 3) { const t = typo(x.nodeValue); if (t !== x.nodeValue) x.nodeValue = t; } else if (x.nodeType === 1 && !/^(SCRIPT|STYLE)$/.test(x.nodeName)) typoTree(x); }); }))
    .observe(document.body, { childList: true, subtree: true });
});

// ---------------------------------------------- outils de dessin des animations
const REDUCE = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const ease = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
const prog = (t, a, b) => ease((t - a) / (b - a));
const lerp = (a, b, p) => a + (b - a) * p;
// texte SVG ; o = { size, anchor, bold, italic, mono, color, op }
const TX = (x, y, s, o = {}) => `<text x="${x}" y="${y}" font-size="${o.size || 16}"${o.anchor ? ` text-anchor="${o.anchor}"` : ""}${o.bold ? ' font-weight="700"' : ""}${o.italic ? ' font-style="italic"' : ""}${o.mono ? ' font-family="IBM Plex Mono, Liberation Mono, monospace"' : ""} style="fill:${o.color || "var(--ink)"}${o.op != null ? ";opacity:" + o.op : ""}">${s}</text>`;
const SUBV = (i, rest = "") => `V<tspan font-size="0.72em" dy="0.3em">${i}</tspan><tspan dy="-0.3em">${rest}</tspan>`;
const wireP = (pts, v) => `<polyline points="${pts.map((p) => p.join(",")).join(" ")}" fill="none" style="${wireStyle(v)};stroke-linejoin:round"/>`;
// Liaisons (REGLES 3.3) : point de liaison à chaque jonction en T ; un croisement sans liaison est un saut de fil
// (« jumpover » d'Altium) : le tronçon horizontal saute le tronçon vertical (demi-cercle de rayon r), jamais de point.
// cheminSauts(pts, autres) : chemin SVG d'un fil orthogonal ; autres = les autres fils (listes de points) qu'il peut croiser.
function cheminSauts(pts, autres = [], r = 6) {
  const verts = [];
  autres.forEach((q) => { for (let i = 1; i < q.length; i++) if (q[i - 1][0] === q[i][0]) verts.push([q[i - 1], q[i]]); });
  let d = `M ${pts[0][0]} ${pts[0][1]}`;
  for (let i = 1; i < pts.length; i++) {
    const [x1, y1] = pts[i - 1], [x2, y2] = pts[i];
    if (y1 === y2 && x1 !== x2) {
      const s = Math.sign(x2 - x1), lo = Math.min(x1, x2) + r, hi = Math.max(x1, x2) - r;
      const xs = [...new Set(verts.filter(([a, b]) => y1 > Math.min(a[1], b[1]) + 0.5 && y1 < Math.max(a[1], b[1]) - 0.5 && a[0] > lo && a[0] < hi).map(([a]) => a[0]))];
      xs.sort((u, v) => s * (u - v)).forEach((xc) => { d += ` L ${xc - s * r} ${y1} A ${r} ${r} 0 0 ${s > 0 ? 1 : 0} ${xc + s * r} ${y1}`; });
    }
    d += ` L ${x2} ${y2}`;
  }
  return d;
}
// fil dessiné avec ses sauts ; o.style remplace le style « valeur logique » (alimentation, masse) ; class="fil" : vu par le contrôle
const filP = (pts, v, autres = [], o = {}) => `<path class="fil" d="${cheminSauts(pts, autres, o.r)}" fill="none" style="${o.style || wireStyle(v)};stroke-linejoin:round;stroke-linecap:round"/>`;
const liaison = (x, y, c = "var(--ink)", r = 4) => `<circle cx="${x}" cy="${y}" r="${r}" style="fill:${c}"/>`;
// alimentation (+5 V) au-dessus du nœud (x, y) et masse (GND) au-dessous : court fil et trait horizontal (REGLES 3.3)
const alimG = (x, y, lab = "+5 V", o = {}) => { const h = o.fil || 14, c = o.color || "var(--ink)";
  return `<line x1="${x}" y1="${y}" x2="${x}" y2="${y - h}" style="stroke:${c};stroke-width:2.5"/><line x1="${x - 14}" y1="${y - h}" x2="${x + 14}" y2="${y - h}" style="stroke:${c};stroke-width:3.5"/>` +
    TX(x, y - h - 8, lab, { size: o.size || 14, bold: true, anchor: "middle", color: c }); };
const masseG = (x, y, o = {}) => { const h = o.fil || 14, c = o.color || "var(--ink)";
  return `<line x1="${x}" y1="${y}" x2="${x}" y2="${y + h}" style="stroke:${c};stroke-width:2.5"/><line x1="${x - 14}" y1="${y + h}" x2="${x + 14}" y2="${y + h}" style="stroke:${c};stroke-width:3.5"/>` +
    TX(x + 20, y + h + 5, "GND", { size: o.size || 13, color: c }); };
const lampG = (x, y, r, on, col = "var(--one)") => (on ? `<circle cx="${x}" cy="${y}" r="${r + 8}" style="fill:${col};opacity:.25"/>` : "") +
  `<circle cx="${x}" cy="${y}" r="${r}" style="fill:${on ? col : "var(--surface)"};stroke:var(--ink);stroke-width:2.5"/>`;
const pill = (x, y, v, o = {}) => `<rect x="${x - 15}" y="${y - 15}" width="30" height="30" rx="7" style="fill:${v ? "var(--one)" : "var(--surface)"};stroke:var(--head);stroke-width:2"/>` +
  TX(x, y + 7, v, { size: 19, bold: true, mono: true, anchor: "middle", color: v ? "#fff" : "var(--ink)" });
const okMark = (x, y, ok, r = 11) => `<circle cx="${x}" cy="${y}" r="${r}" style="fill:${ok ? "var(--ok)" : "var(--bad)"}"/>` +
  (ok ? `<path d="M ${x - r * .45} ${y} l ${r * .3} ${r * .35} l ${r * .55} ${-r * .7}" style="fill:none;stroke:#fff;stroke-width:2.6"/>`
      : `<path d="M ${x - r * .4} ${y - r * .4} l ${r * .8} ${r * .8} M ${x + r * .4} ${y - r * .4} l ${-r * .8} ${r * .8}" style="stroke:#fff;stroke-width:2.6"/>`);
// boîtier DIP 14 vu de dessus, encoche à gauche : broches 1 à 7 en bas (gauche → droite), 8 à 14 en haut (droite → gauche)
function dipG(x, y, w, h, label, o = {}) {
  const n = 7, pw = w / n; let s = "";
  for (let i = 0; i < n; i++) {
    const px = x + pw * (i + 0.5) - 6;
    s += `<rect x="${px}" y="${y - 14}" width="12" height="14" style="fill:#C8CEDA;stroke:#5A6478"/><rect x="${px}" y="${y + h}" width="12" height="14" style="fill:#C8CEDA;stroke:#5A6478"/>`;
  }
  s += `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" style="fill:#3A3F52;stroke:#23263A;stroke-width:2"/>`;
  s += `<path d="M ${x} ${y + h / 2 - 12} a 12 12 0 0 1 0 24 z" style="fill:#23263A"/><circle cx="${x + 16}" cy="${y + h - 14}" r="5" style="fill:#5A6070"/>`;
  if (label) s += TX(x + w / 2, y + h / 2 + 8, label, { size: o.fs || 22, bold: true, mono: true, anchor: "middle", color: "#EEF1F7" });
  if (o.nums) for (let i = 0; i < n; i++) {
    s += TX(x + pw * (i + 0.5), y + h - 6, i + 1, { size: 11, anchor: "middle", color: "#B8BED0" });
    s += TX(x + pw * (i + 0.5), y + 14, 14 - i, { size: 11, anchor: "middle", color: "#B8BED0" });
  }
  return s;
}
const dipPin = (x, y, w, h, k) => k <= 7 ? [x + (w / 7) * (k - 0.5), y + h + 14] : [x + (w / 7) * (14 - k + 0.5), y - 14];
// chronogramme qui s'écrit au fil du temps : rows = [{ name, f(s) → 0/1, color }], de s = 0 à min(t, tmax)
function traceG(x, y, w, rows, t, tmax, o = {}) {
  const rh = o.rh || 34, hi = rh * 0.55, X = (s) => x + w * s / tmax, dt = o.dt || tmax / 400, end = Math.min(t, tmax);
  let g = "";
  rows.forEach((r, i) => {
    const yb = y + i * rh + rh - 6, yh = yb - hi;
    g += TX(x - 10, yb - 3, r.name, { anchor: "end", bold: true, italic: true, size: o.fs || 15 });
    g += `<line x1="${x}" y1="${yb}" x2="${x + w}" y2="${yb}" style="stroke:var(--line);stroke-width:1"/>`;
    if (end <= 0) return;
    let v = r.f(0), d = `M ${x} ${v ? yh : yb}`;
    for (let s = dt; s <= end + 1e-9; s += dt) { const nv = r.f(s); if (nv !== v) { d += ` L ${X(s)} ${v ? yh : yb} L ${X(s)} ${nv ? yh : yb}`; v = nv; } }
    d += ` L ${X(end)} ${v ? yh : yb}`;
    g += `<path d="${d}" fill="none" style="stroke:${r.color || "var(--ink)"};stroke-width:2.6;stroke-linejoin:round"/>`;
  });
  if (o.cursor !== false && t > 0 && t < tmax) g += `<line x1="${X(end)}" y1="${y}" x2="${X(end)}" y2="${y + rows.length * rh}" style="stroke:var(--bad);stroke-width:1.5"/>`;
  return g;
}

// ---------------------------------------------- leçons animées : lecture, pause, étapes numérotées, sous-titres
// L'animation tourne en boucle et s'arrête quand elle sort de l'écran. Avec « réduire les animations », elle démarre en pause.
const LESSONS = [];
function lesson(id, cfg) {
  const root = $(id), body = root.querySelector(".ls-body");
  body.innerHTML = `<div class="ls-stage"></div><div class="ls-cap"></div>
    <div class="ls-ctrl"><button class="ls-btn ls-play" type="button"></button><button class="ls-btn ls-back" type="button">↺ Recommencer</button>
    <span class="ls-steps" role="group" aria-label="Étapes"></span><span class="ls-prog"><i></i></span></div>`;
  if (cfg.extra) { const e = document.createElement("div"); e.className = "ls-extra"; e.innerHTML = cfg.extra; body.insertBefore(e, body.querySelector(".ls-cap")); }
  const st = { t: 0, T: 0, playing: !REDUCE, vis: true, last: null, step: -1, dirty: true, cfg };
  const stage = body.querySelector(".ls-stage"), cap = body.querySelector(".ls-cap"), play = body.querySelector(".ls-play"), bar = body.querySelector(".ls-prog i"), steps = body.querySelector(".ls-steps");
  stage.setAttribute("role", "img"); stage.setAttribute("aria-label", cfg.label);
  cfg.steps.forEach(([t0], i) => {
    const b = document.createElement("button"); b.type = "button"; b.textContent = i + 1; b.setAttribute("aria-label", "Étape " + (i + 1));
    b.onclick = () => { st.t = t0 + 0.01; st.dirty = true; }; steps.appendChild(b);
  });
  const setPlay = () => { play.textContent = st.playing ? "❚❚ Pause" : "▶ Lecture"; };
  play.onclick = () => { st.playing = !st.playing; setPlay(); }; setPlay();
  body.querySelector(".ls-back").onclick = () => { st.t = 0; st.dirty = true; if (!st.playing) { st.playing = true; setPlay(); } };
  if ("IntersectionObserver" in window) new IntersectionObserver((es) => es.forEach((e) => { st.vis = e.isIntersecting; st.last = null; }), { threshold: 0.1 }).observe(stage);
  st.render = () => {
    stage.innerHTML = cfg.draw(st.t, st.T, st);
    let k = 0; cfg.steps.forEach(([t0], i) => { if (st.t >= t0) k = i; });
    if (k !== st.step) {
      st.step = k; cap.innerHTML = `<b>${k + 1}.</b> ${cfg.steps[k][1]}`;
      steps.querySelectorAll("button").forEach((b, i) => b.setAttribute("aria-current", i === k ? "step" : "false"));
    }
    bar.style.width = (100 * st.t / cfg.dur).toFixed(1) + "%";
  };
  LESSONS.push(st);
  try { st.render(); } catch (e) { console.error(e); }   // première image tout de suite, même si l'animation ne démarre pas
  return st;
}
function lessonLoop(ts) {
  LESSONS.forEach((st) => {
    if (!st.vis) return;
    const dt = st.last == null ? 0 : Math.min(0.1, (ts - st.last) / 1000); st.last = ts;
    if (st.playing) { st.t += dt; st.T += dt; if (st.t >= st.cfg.dur) st.t = 0; st.dirty = true; }
    if (st.dirty && ts - (st.drawn || 0) > 33) { st.render(); st.drawn = ts; st.dirty = false; }
  });
  requestAnimationFrame(lessonLoop);
}
ready(() => requestAnimationFrame(lessonLoop));
