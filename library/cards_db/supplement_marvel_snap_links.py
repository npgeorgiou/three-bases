"""Marvel Snap's links between cards (supplement/marvel_snap_links.jsonl): a card whose text adds, creates, summons, puts,
shuffles, transforms into or replaces with a card named in it generates that card (the export has no field for this).
Longest name first (Ebony Blade, not Blade); a name in a possessive (Ultron's Stones) or after other words is not taken.
Usage: supplement_marvel_snap_links.py"""
import json, os, re, sqlite3
HERE = os.path.dirname(os.path.abspath(__file__))
V = r"(?:adds?|creates?|summons?|puts?|shuffles?|(?:transforms?|turns?|splits?) into|replaces? (?:it |this )?with)"
cards = [json.loads(l) for l in open(os.path.join(HERE, 'supplement', 'marvel_snap.jsonl'), encoding='utf-8')]
loaded = {i for (i,) in sqlite3.connect(os.path.join(HERE, 'cards.sqlite')).execute("select id from card where game='marvel_snap'")}
names = sorted({x['name']: x['id'] for x in cards if x['category'] != 'keyword' and len(x['name']) > 2 and x['id'] in loaded}.items(),
               key=lambda t: -len(t[0]))
out = set()
for x in cards:
    t = x.get('text') or ''
    if not t or x['category'] == 'keyword' or x['id'] not in loaded: continue
    taken = []
    for n, i in names:
        if i == x['id'] or n.lower() not in t.lower(): continue
        # the make words in any case, the name only as written (Random is a card, "a random card" is not)
        for m in re.finditer("(?i:" + V + r"\s+(?:(?:a|an|the|\d+|two|three|copies of|copy of|your)\s+){0,3})" + re.escape(n) + r"(?![\w'’])", t):
            s = m.end() - len(n)
            if any(a <= s < b for a, b in taken): continue
            taken.append((s, m.end())); out.add((x['id'], i, n))
with open(os.path.join(HERE, 'supplement', 'marvel_snap_links.jsonl'), 'w', encoding='utf-8') as f:
    for a, b, n in sorted(out): f.write(json.dumps({'src': a, 'rel': 'generates', 'dst': b, 'evidence': 'card text: makes ' + n}) + '\n')
print(len(out), 'links')
