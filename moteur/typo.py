# -*- coding: utf-8 -*-
"""Typographie française (REGLES 7) pour les fiches Word et les pages : espaces insécables, trait d'union insécable.
Mêmes règles que moteur/typo.js (présentations)."""
import re

NB, NNB = " ", " "
UNITES = r"(?:V|mV|mA|A|µA|ns|ms|µs|s|MHz|kHz|Hz|µW|mW|W|pJ|°C|%|min|L|cm|mm|lignes|portes|entrées|broches|bits|bytes|bouteilles|transistors|inverseurs)"


def typo(t):
    """Espaces insécables : nombre + unité, avant « : ; ? ! » et à l'intérieur des guillemets français."""
    if not isinstance(t, str) or "://" in t:
        return t
    t = re.sub(r" ([:;?!»])", NB + r"\1", t)
    t = t.replace("« ", "«" + NB)
    t = re.sub(r"(\d) (?=" + UNITES + r"\b)", r"\1" + NB, t)
    t = re.sub(r"(\d) (?=°C)", r"\1" + NB, t)
    t = re.sub(r"\b(N°|n°|p\.|chap\.|diapositives?|LZ|Floyd) (?=\d)", lambda m: m.group(1) + NB, t)
    t = re.sub(r"(\d) … (\d|−)", r"\1" + NB + "…" + NB + r"\2", t)
    for _ in range(2):   # « A = 1 », « A = B = 1 » ne se coupent pas
        t = re.sub(r"(^|[\s(])(\w{1,3}) = ([\w−]{1,3})(?=$|[\s,.;:)!?])", r"\1\2" + NB + "=" + NB + r"\3", t)
    t = re.sub(r"(\d) ou (\d)", r"\1" + NB + "ou" + NB + r"\2", t)
    t = re.sub(r"(\d) (?=[a-zà-ÿ])", r"\1" + NB, t)      # « 4 portes », « 8 lignes »
    t = re.sub(r"\bNON-(ET|OU)\b", "NON‑\\1", t)      # trait d'union insécable (docx : w:noBreakHyphen)
    return t
