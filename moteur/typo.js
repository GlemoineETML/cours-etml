// Typographie française (REGLES 7) pour les présentations : mêmes règles que moteur/typo.py.
"use strict";
// typographie française : espaces insécables (nombre + unité, avant : ; ? ! », après «, N°, p., diapositive)
const UNITS = "(?:V|mV|mA|A|µA|ns|ms|µs|s|MHz|kHz|Hz|µW|mW|W|pJ|°C|%|min|L|cm|mm|lignes|portes|entrées|broches|bits|bytes|bouteilles|transistors|inverseurs)";
function TY(t) {
  if (typeof t !== "string" || t.includes("://")) return t;
  t = t.replace(/ ([:;?!»])/g, "\u00a0$1").replace(/« /g, "«\u00a0");
  t = t.replace(new RegExp("(\\d) (?=" + UNITS + "(?![\\wÀ-ÿ]))", "g"), "$1\u00a0").replace(/(\d) (?=°C)/g, "$1\u00a0");
  t = t.replace(/(N°|n°|p\.|chap\.|diapositives?|LZ|Floyd) (?=\d)/g, "$1\u00a0").replace(/(\d) … (\d|−)/g, "$1\u00a0…\u00a0$2");
  const EQ = /(^|[\s(])([\wÀ-ÿ]{1,3}) = ([\wÀ-ÿ−]{1,3})(?=$|[\s,.;:)!?])/g;      // « A = 1 » ne se coupe pas
  t = t.replace(EQ, "$1$2\u00a0=\u00a0$3").replace(EQ, "$1$2\u00a0=\u00a0$3");
  t = t.replace(/(\d) ou (\d)/g, "$1\u00a0ou\u00a0$2").replace(/(\d) (?=[a-zà-ÿ])/g, "$1\u00a0");   // « 0 ou 1 », « 4 côtés »
  t = t.replace(/\bNON-(ET|OU)\b/g, "NON\u2011$1");                // trait d'union insécable (U+2011), comme typo.py
  return t;
}
const TYR = (t) => typeof t === "string" ? TY(t) : (Array.isArray(t) ? t.map(r => (r && typeof r.text === "string") ? Object.assign({}, r, { text: TY(r.text) }) : r) : t);
const TYROWS = (rows) => rows.map(row => row.map(c => (c && c.text !== undefined) ? Object.assign({}, c, { text: TYR(c.text) }) : c));

module.exports = { TY, TYR, TYROWS, UNITS };
