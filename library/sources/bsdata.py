"""Read a BSData repo: rules, ability profiles and unit/model entries per catalogue.
Yields dicts: kind (rule|ability|unit), name, faction (catalogue name), profile type, text, stats."""
import os, re, xml.etree.ElementTree as ET
def strip(t): return t.split('}', 1)[1] if t.startswith('{') else t
def txt(e): return re.sub(r'\s+', ' ', (e.text or '')).strip() if e is not None else ''
def kids(e, tag): return [x for x in e if strip(x.tag) == tag]
def walk(e):
    yield e
    for x in e: yield from walk(x)
def profile_text(p):
    ch = {}
    for cs in kids(p, 'characteristics'):
        for x in kids(cs, 'characteristic'): ch[x.get('name')] = txt(x)
    return ch
def read(repo, files=None):
    out = []
    for f in sorted(os.listdir(repo)):
        if not (f.endswith('.cat') or f.endswith('.gst')) or (files and not files(f)): continue
        try: root = ET.parse(os.path.join(repo, f)).getroot()
        except ET.ParseError: continue
        fac = root.get('name'); fid = root.get('id')
        for e in walk(root):
            t = strip(e.tag)
            if t == 'rule' and e.get('name'):
                d = [txt(x) for x in kids(e, 'description')]
                if d and d[0]: out.append(dict(kind='rule', name=e.get('name'), faction=fac, file=f, text=d[0], hidden=e.get('hidden')))
            elif t == 'profile' and e.get('name'):
                ch = profile_text(e)
                ty = e.get('typeName') or ''
                out.append(dict(kind='profile', ptype=ty, name=e.get('name'), faction=fac, file=f, chars=ch, hidden=e.get('hidden')))
            elif t == 'selectionEntry' and e.get('type') in ('unit', 'model'):
                out.append(dict(kind='unit', etype=e.get('type'), name=e.get('name'), faction=fac, file=f, el=e))
    return out
