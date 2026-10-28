"""Reader input for one game: every card that has text beyond its Keywords field, with its keywords, types and the names of
other entries its text mentions; cut into batches by amount of text. Keyword-only cards get an empty record directly.
Usage: build_input.py <game> <chars per batch> [--only id,id,...]   writes input/<game>/batch_NNN.jsonl, read/<game>/auto.jsonl"""
import json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
import source
DB = os.path.join(HERE, '..', 'three-bases-library.sqlite')
KWFIELD = re.compile(r'^\s*Keywords:\s*([^.]*)\.\s*', re.S)
# Keywords-field entries that are not keywords. Runeterra "Missing Translation": Riot's own card data has keywordRef
# AuraVisualFakeKeyword there on all 42 such cards (a display marker of aura cards, no rule text in any language)
NOT_KEYWORDS = {'missing translation'}


def types_of(subtypes):
    s = (subtypes or '').strip()
    if s.startswith('['): items = json.loads(s)
    else: items = [x.strip() for x in s.split(',') if x.strip()]
    return [x.title() for x in items if not x.lower().endswith(' spell')]


def speed_of(subtypes):
    m = re.search(r'(burst|fast|slow|focus) spell', (subtypes or '').lower())
    return m.group(1) if m else ''


def excluded(c, game):
    """ids left out of the reading (exclude.tsv: whole editions or sources Kaptain does not want)."""
    import csv
    out = set()
    for r in csv.DictReader(open(os.path.join(HERE, 'exclude.tsv')), delimiter='\t'):
        if r['game'] == game and r['column'] in ('edition', 'source_type', 'category'):
            out |= {i for (i,) in c.execute(f"select id from entities where game=? and {r['column']}=?", (game, r['value']))}
    return out


def cards(c, game):
    names = {}
    for i, n, cat in c.execute("select id, name, category from entities where game=?", (game,)):
        if n and len(n) > 2: names.setdefault(n.lower(), n)
    # one pattern for all names, longest first, so each text is scanned once
    pat = re.compile(r'\b(?:' + '|'.join(re.escape(k) for k in sorted(names, key=len, reverse=True)) + r')\b')
    out = []; skip = excluded(c, game)
    for i, n, cat, sub, t in c.execute("select id, name, category, subtypes, text from entities where game=? and category "
                                        "not in ('keyword','tribe') order by id", (game,)):
        if i in skip: continue
        t = ' '.join((t or '').split())
        m = KWFIELD.match(t)
        kws = [k.strip() for k in m.group(1).split(',')] if m else []
        rest = t[m.end():] if m else t
        low = rest.lower()
        mentioned = sorted({names[m2.group(0)] for m2 in pat.finditer(low) if m2.group(0) != n.lower()})
        out.append({'id': i, 'name': n, 'category': cat, 'speed': speed_of(sub), 'types': types_of(sub), 'keywords': kws,
                    'text': t, 'names_in_text': mentioned, '_rest': rest})
    return out


def main():
    game, budget = sys.argv[1], int(sys.argv[2])
    only = set(int(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else None
    c = source.lib()
    allc = cards(c, game)
    os.makedirs(os.path.join(HERE, 'input', game), exist_ok=True); os.makedirs(os.path.join(HERE, 'read', game), exist_ok=True)
    auto = [x for x in allc if not re.sub(r'[\W_]', '', x['_rest'])]
    with open(os.path.join(HERE, 'read', game, 'auto.jsonl'), 'w') as f:
        for x in auto: f.write(json.dumps({'id': x['id'], 'abilities': []}) + '\n')
    todo = [x for x in allc if x not in auto and (only is None or x['id'] in only)]
    batches, cur, size = [], [], 0
    for x in todo:
        if cur and size + len(x['text']) > budget: batches.append(cur); cur, size = [], 0
        cur.append(x); size += len(x['text'])
    if cur: batches.append(cur)
    for k, b in enumerate(batches, 1):
        with open(os.path.join(HERE, 'input', game, 'batch_%03d.jsonl' % k), 'w') as f:
            for x in b: f.write(json.dumps({k2: v for k2, v in x.items() if not k2.startswith('_')}) + '\n')
    with open(os.path.join(HERE, 'input', game, 'keywords.jsonl'), 'w') as f:
        for i, n, t in c.execute("select id, name, text from entities where game=? and category='keyword' order by id", (game,)):
            f.write(json.dumps({'id': i, 'name': n, 'category': 'keyword', 'text': ' '.join((t or '').split())}) + '\n')
    print(f'{game}: {len(allc)} cards, {len(auto)} keyword-only (no reading), {len(todo)} to read in {len(batches)} batches '
          f'({sum(len(x["text"]) for x in todo)} chars)')


if __name__ == '__main__':
    main()
