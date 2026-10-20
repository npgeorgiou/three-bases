"""The first tagging of every entry, as load_cards.py tags a new card, so the build can start from the card data alone
(21 Oct 2026, one chain): the general wording patterns (patterns/general.tsv, old concept ids, every game but Marvel Snap, which
its own loader tags) become text_pattern tags, then every entry inherits its keywords' tags along its keyword links
(has_keyword as they are, grants_keyword as 'grants'). A game file's '!' lines switch a general pattern off for that game.
The text is read as reading.py says, with the entry's own name as 'name' and "named X" as 'named namedcard'.
Build step after concept_defs.py, before game_patterns.py. Usage: general_tags.py <db>"""
import os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import reading as RD
from concept_tree import primary
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'patterns', 'general.tsv'), encoding='utf-8') if l.strip() and not l.startswith('#')]
c.execute('DELETE FROM concept_patterns WHERE game IS NULL')
c.executemany('INSERT INTO concept_patterns VALUES(?,?,?,NULL)', rows)
n = 0
for (g,) in q("SELECT id FROM games WHERE id != 'marvel_snap'"):
    excl = set()
    pf = os.path.join(HERE, 'patterns', g + '.txt')
    if os.path.exists(pf):
        excl = {tuple(l[1:].rstrip('\n').split('|', 1)) for l in open(pf, encoding='utf-8') if l.startswith('!')}
    pats = []
    for con, role, p in rows:
        if any((con == a or con in primary(a)) and b in p for a, b in excl): continue
        try: pats.append((con, role, re.compile(p, re.I)))
        except re.error: pass
    names = [n_ for n_, in q("SELECT name FROM entities WHERE game=? AND category NOT IN ('keyword','tribe')", g)]
    NAMED = re.compile(r'\bnamed (' + '|'.join(re.escape(x.lower()) for x in sorted(names, key=len, reverse=True) if len(x) >= 4) + r')\b') if names else re.compile(r'(?!x)x')
    for e, name, text in q("SELECT id, name, text FROM entities WHERE game=? AND text IS NOT NULL", g):
        low = RD.strip(g, text.lower())
        for nm in [name] + name.split(' // '):
            if len(nm) > 2: low = low.replace(nm.lower(), 'name')
        low = NAMED.sub('named namedcard', low)
        for con, role, p in pats:
            m = p.search(low)
            if m: n += c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, con, role, 'text_pattern', low[max(0, m.start() - 20): m.start() + 40])).rowcount
k = c.execute("INSERT OR IGNORE INTO entity_concepts SELECT l.src, ec.concept, ec.role, 'via_keyword', 'inherited from a reviewed keyword' FROM entity_links l JOIN entity_concepts ec ON ec.entity = l.dst WHERE l.rel = 'has_keyword'").rowcount
k += c.execute("INSERT OR IGNORE INTO entity_concepts SELECT l.src, ec.concept, 'grants', 'via_keyword', 'inherited from a reviewed keyword' FROM entity_links l JOIN entity_concepts ec ON ec.entity = l.dst WHERE l.rel = 'grants_keyword' AND ec.role = 'does'").rowcount
c.commit()
print('general_tags: text_pattern', n, 'inherited', k)
