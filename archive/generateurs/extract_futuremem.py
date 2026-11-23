#!/usr/bin/env python3
"""Extrait d'une page « Semestre » FutureMEM les champs d'apprentissage demandés.
Usage : python3 -I extract_futuremem.py page.html URL_DE_LA_PAGE LFB_El_Dim4 LFB_El_DT2 ... > data.json
"""
import sys, re, json
from bs4 import BeautifulSoup

norm = lambda x: re.sub(r'\s+', ' ', x or '').strip()

def field_heading(soup, code):
    for h in soup.find_all('h2'):
        if norm(h.get_text()).startswith(code) and h.get('id'):
            return h
    raise SystemExit(f'Champ introuvable sur la page : {code}')

def parse_rows(block):
    rows = []
    for tr in block.find_all('tr'):
        tds = tr.find_all('td', recursive=True)
        tds = [td for td in tds if td.find_parent('td') is None]   # cellules de premier niveau
        if len(tds) < 4:
            continue
        c0, c1, c2, c3 = tds[:4]
        a = c0.find_all('a')
        lz = []
        for link in c1.find_all('a'):
            code = norm(link.get_text())
            if not code.startswith('LZ_'):
                continue
            tax = link.find_next('abbr')
            # texte jusqu'au <br> ou au lien LZ suivant
            parts = []
            for sib in tax.next_siblings:
                if getattr(sib, 'name', None) in ('br', 'a'):
                    break
                parts.append(sib.get_text() if hasattr(sib, 'get_text') else str(sib))
            texte = norm(''.join(parts)).lstrip('- ').strip()
            lz.append({'code': code, 'niveau': norm(tax.get_text()), 'texte': texte, 'url': link['href']})
        conn = [norm(t) for t in c2.get_text('\n').split('\n') if norm(t)]
        t0 = norm(c0.get_text(' '))
        m = re.search(r'CO:\s*(.*?)\s*CP:\s*(.*?)\s*Niveau cible:\s*(.*)$', t0)
        cp_link = [x for x in a if 'lkn' in x['href'] or x is not a[0]][-1]
        rows.append({
            'co': m.group(1), 'co_url': a[0]['href'], 'co_titre': norm(c0.find('span')['title']),
            'cp': m.group(2), 'cp_url': cp_link['href'],
            'niveau_cible': m.group(3),
            'lz': lz, 'connaissances': conn,
            'periodes': int(re.search(r'\d+', c3.get_text()).group()),
        })
    return rows

def main():
    page, url, codes = sys.argv[1], sys.argv[2].split('#')[0], sys.argv[3:]
    soup = BeautifulSoup(open(page, encoding='utf-8').read(), 'html.parser')
    out = []
    for code in codes:
        h = field_heading(soup, code)
        titre = norm(h.get_text())
        intro = h.find_next_sibling('p')
        ts = h.find_next('div', class_='tabbed-set')
        labels = [norm(l.get_text()) for l in ts.find('div', class_='tabbed-labels').find_all('label')]
        blocks = ts.find('div', class_='tabbed-content').find_all('div', class_='tabbed-block', recursive=False)
        tab = dict(zip(labels, blocks))
        sit = tab['Situations de travail et d’action typiques']
        situation = norm(sit.get_text(' '))
        did = []
        inner = tab['Didactique'].find('div', class_='tabbed-set')
        ilabels = [norm(l.get_text()) for l in inner.find('div', class_='tabbed-labels').find_all('label')]
        iblocks = inner.find('div', class_='tabbed-content').find_all('div', class_='tabbed-block', recursive=False)
        for lab, bl in zip(ilabels, iblocks):
            steps = []
            for p in bl.find_all('p', recursive=False)[1:]:
                step = norm(p.find(string=True, recursive=False) or '')
                td = p.find('td')
                steps.append([step, norm(td.get_text(' ')) if td else ''])
            did.append({'approche': lab, 'etapes': steps})
        ctl = [{'nom': norm(a.get_text()), 'description': norm(a.get('title', ''))}
               for a in tab['Contrôles de compétence'].find_all('abbr')]
        rows = parse_rows(tab['Compétences opérationnelles et critères de performance'])
        out.append({'code': code, 'page_url': url, 'titre': titre, 'ancre': h['id'], 'intro': norm(intro.get_text()) if intro else '',
                    'situation': situation, 'didactique': did, 'controles': ctl, 'lignes': rows,
                    'total_periodes': sum(r['periodes'] for r in rows)})
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
