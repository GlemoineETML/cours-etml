import re, pathlib
src = pathlib.Path("artefact/page.html").read_text(encoding="utf-8")

def inline(m):
    nom = m.group(1)
    p = pathlib.Path("fig") / (nom + ".svg")
    s = p.read_text(encoding="utf-8")
    s = re.sub(r'<\?xml[^>]*\?>\s*', '', s)
    s = re.sub(r'<!DOCTYPE[^>]*>\s*', '', s)
    # retirer width/height de la balise <svg ...>, garder viewBox
    def fix(mm):
        tag = mm.group(0)
        tag = re.sub(r'\s(width|height)="[^"]*"', '', tag)
        if 'viewBox' not in tag:
            raise SystemExit("pas de viewBox dans " + nom)
        if 'preserveAspectRatio' not in tag:
            tag = tag.replace('<svg', '<svg preserveAspectRatio="xMidYMid meet"', 1)
        return tag
    s = re.sub(r'<svg\b[^>]*>', fix, s, count=1)
    # espace de noms des identifiants (marqueurs de flèches) pour éviter les doublons
    ids = sorted(set(re.findall(r'id="([A-Za-z_][\w-]*)"', s)))
    for i in ids:
        s = s.replace('id="%s"' % i, 'id="%s-%s"' % (i, nom))
        s = s.replace('url(#%s)' % i, 'url(#%s-%s)' % (i, nom))
    return s.strip()

out, n = re.subn(r'\{\{SVG:([A-Za-z0-9_]+)\}\}', inline, src)
reste = re.findall(r'\{\{[^}]*\}\}', out)
if reste:
    raise SystemExit("placeholders restants : %r" % reste)
pathlib.Path("artefact/eleves-140.html").write_text(out, encoding="utf-8")
print("substitutions :", n, "| octets :", len(out))
