"""Gwent's links the library lacks (supplement/gwent_links.jsonl): a card whose text spawns, creates or transforms into a card
named in it generates that card (plural names too: "3 Harald's Pals", "2 Rats"); a card whose text evolves or transforms
itself turns into the other forms of its name ("Auberon: King" -> "Auberon: Invader", "Shaping Nature" -> "Shaping Nature:
Veil"). Only links the library's entity_links does not have. Longest name first; names as written.
Usage: supplement_gwent_links.py"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
import source
V = r"(?:spawns?(?: and play)?|creates?(?: and play)?|(?:transforms?|turns?) (?:self |itself |it |them )?into)"
c = source.lib()
cards = list(c.execute("select id, name, text from entities where game='gwent' and category not in ('keyword','tribe')"))
have = {(a, b) for a, b in c.execute("select src, dst from main.entity_links where rel in ('generates','summons','transforms_into')")}
names = sorted({n.replace(' (created)', ''): i for i, n, _ in cards if len(n) > 2 and not n.endswith(' (created)')}.items(),
               key=lambda t: -len(t[0]))
out = set()
for i, n, t in cards:
    t = t or ''; taken = []
    for nm, j in names:
        if j == i or nm.lower() not in t.lower(): continue
        for m in re.finditer("(?i:" + V + r"\s+(?:(?:a|an|the|\d+|two|three|copies of|copy of|your)\s+){0,3})" + re.escape(nm)
                             + r"(?:s|es)?(?![\w'’])", t):
            s = m.start()
            if any(a <= s < b for a, b in taken): continue
            taken.append((s, m.end())); out.add((i, j, 'generates', 'card text: makes ' + nm))
    if re.search(r'\b(evolves?|transforms? (?:self|itself)|and transform\b|choose one|awaken|on an adventure)', t, re.I):
        pre = re.sub(r"'s Day Off$", '', n.replace(' (created)', '').split(':')[0].strip())
        for j, m2, _ in [x for x in cards if x[0] != i]:
            if m2.split(':')[0].strip() == pre and ':' in m2 and m2.replace(' (created)', '') != n.replace(' (created)', ''):
                out.add((i, j, 'transforms_into', 'card text: evolves or transforms into another form of ' + pre))
# makers whose text names the made cards in other words (forms named after another name, "a mutagen", "a curse")
BY_TEXT = {'Harald an Craite': ('evolves', ['Harald: Warmonger', 'Harald the Cripple'], 'transforms_into'),
           'Jacques: Miracle Child': ('evolves', ['Jacques de Aldersberg'], 'transforms_into'),
           'Stolen Mutagens': ('Choose a mutagen: Red, Blue, Green', ['Red Mutagen', 'Blue Mutagen', 'Green Mutagen'], 'generates'),
           'Renfri': ('Create a curse ... Create a blessing', [n for _, n, _ in cards if n.startswith(('Curse of ', 'Blessing of '))], 'generates'),
           'Mysterious Puzzle Box': ('transform ... into Thing From the Box', ['Thing from the Box'], 'generates')}
ids = {n: i for i, n, _ in cards}
for a, (why, bs, rel) in BY_TEXT.items():
    for b in bs: out.add((ids[a], ids[b], rel, 'card text: ' + why))
out = {x for x in out if (x[0], x[1]) not in have}
with open(os.path.join(HERE, 'supplement', 'gwent_links.jsonl'), 'w', encoding='utf-8') as f:
    for a, b, r, e in sorted(out): f.write(json.dumps({'src': a, 'rel': r, 'dst': b, 'evidence': e}) + '\n')
print(len(out), 'links')
