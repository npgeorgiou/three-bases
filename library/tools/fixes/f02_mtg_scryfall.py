"""Magic data from the Scryfall Oracle Cards file, for every Magic entry (matched by oracle id):
  - set name and rarity where missing (entries loaded from MTGJSON had only set codes);
  - generates links from a card to the tokens and emblems Scryfall lists as its parts (replacing the name-based links the
    token load made: token names like 'Zombie' are words in many texts); a part whose name and type line match several tokens is skipped;
  - references links between cards Scryfall lists as related (combo_piece), both ways as Scryfall lists them;
  - keyword links: has_keyword = Scryfall's keyword list for the card (its own abilities and keyword actions) or a keyword the
    card gives itself ("this creature gains first strike"); grants_keyword = given to other objects ("creatures you control have
    flying", "target creature gains haste", "equipped creature has ..."); mentions_keyword = only referred to ("creatures with
    flying", "loses flying"); inherited via_keyword tags follow: role 'does' for own keywords,
    'grants' for granted ones. Text read without reminder text, own name as 'name'.
Usage: f02_mtg_scryfall.py <db> <oracle-cards file>"""
import json, re, sqlite3, sys, collections
db, src = sys.argv[1:3]
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
def rows(p):
    txt = open(p, encoding='utf-8').read().strip()
    if txt.startswith('['): yield from json.loads(txt); return
    for line in txt.splitlines():
        line = line.strip().rstrip(',')
        if line and line not in '[]': yield json.loads(line)
S = {x['oracle_id']: x for x in rows(src) if x.get('oracle_id')}
ent = {}
for i, e, n, ed, ra in q("SELECT id, ext_id, name, edition, rarity FROM entities WHERE game='mtg' AND category NOT IN ('keyword','tribe')"):
    oid = e.split(':')[-1]
    if oid in S: ent[i] = (oid, n, ed, ra)
C = collections.Counter()
# 1. set names and rarity
for i, (oid, n, ed, ra) in ent.items():
    x = S[oid]
    if not ed and x.get('set_name'): c.execute("UPDATE entities SET edition=? WHERE id=?", (x['set_name'], i)); C['set name added'] += 1
    if not ra and x.get('rarity'): c.execute("UPDATE entities SET rarity=? WHERE id=?", (x['rarity'], i)); C['rarity added'] += 1
# 2. generates links to tokens
tok = collections.defaultdict(list); tokoid = {}
for i, e in q("SELECT id, ext_id FROM entities WHERE game='mtg' AND ext_id LIKE 'add:scryfall_tokens:%'"):
    x = S.get(e.split(':')[-1])
    if x: tok[(x['name'], x.get('type_line'))].append(i); tokoid[i] = x['oracle_id']
tokids = {i for v in tok.values() for i in v}
C['name-based token links removed'] = c.execute("DELETE FROM entity_links WHERE rel='generates' AND evidence='names a created card' AND dst IN (%s)" % ','.join(map(str, tokids))).rowcount
byname = collections.defaultdict(list)
for i, (oid, n, ed, ra) in ent.items(): byname[n].append(i)
for i, (oid, n, ed, ra) in ent.items():
    for p in S[oid].get('all_parts') or []:
        if p.get('name') == S[oid]['name']: continue
        if p['component'] == 'token' and i not in tokids:
            t = tok.get((p['name'], p.get('type_line')), [])
            if len(t) == 1: C['generates'] += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (i, 'generates', t[0], 'Scryfall related token')).rowcount
            elif len(t) > 1:   # several tokens share name and type: pick the one whose stats, colour and keywords the card's text names
                low = (S[oid].get('oracle_text') or ' '.join(f.get('oracle_text', '') for f in S[oid].get('card_faces') or [])).lower()
                def score(j):
                    x = S[tokoid[j]]; sc = 0
                    if 'power' in x and f"{x['power']}/{x['toughness']}".lower() in low: sc += 2
                    cw = {'W': 'white', 'U': 'blue', 'B': 'black', 'R': 'red', 'G': 'green'}
                    cols = [cw[k] for k in x.get('colors') or []]
                    if cols and all(w in low for w in cols): sc += 1
                    if not cols and 'colorless' in low: sc += 1
                    sc += sum(1 for k in x.get('keywords') or [] if k.lower() in low)
                    return sc
                sc = sorted(((score(j), j) for j in t), reverse=True)
                if sc[0][0] > 0 and sc[0][0] > sc[1][0]: C['generates'] += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (i, 'generates', sc[0][1], 'Scryfall related token (matched by stats, colour, keywords)')).rowcount
                else: C['token part ambiguous, skipped'] += 1
        elif p['component'] == 'combo_piece' and i not in tokids:
            t = [j for j in byname.get(p['name'], []) if j != i and j not in tokids]
            if len(t) == 1: C['references'] += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (i, 'references', t[0], 'Scryfall related card')).rowcount
# 3. keyword links
kw = {n.lower(): k for n, k in q("SELECT name, id FROM entities WHERE game='mtg' AND category='keyword'")}
# 'Double' is not a Magic keyword: a leftover of an older Scryfall keyword list (double strike / double team cards)
for (bad,) in q("SELECT id FROM entities WHERE game='mtg' AND category='keyword' AND name='Double' AND text IS NULL"):
    for st in ("DELETE FROM entity_concepts WHERE entity=?", "DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM entities WHERE id=?"): c.execute(st, (bad,) * st.count('?'))
    c.execute("DELETE FROM load_log WHERE game='mtg' AND step LIKE 'removed keyword Double%'")
    c.execute("INSERT INTO load_log VALUES('mtg','removed keyword Double (not a Magic keyword; leftover of an older keyword list)',1,'')")
    kw = {n.lower(): k for n, k in q("SELECT name, id FROM entities WHERE game='mtg' AND category='keyword'")}
LONGER = {}
for k in kw: LONGER[k] = [x for x in kw if x != k and re.search(r'\b' + re.escape(k) + r'\b', x)]
kwc = collections.defaultdict(list)
for k, con, role in q("SELECT entity, concept, role FROM entity_concepts x JOIN entities e ON e.id=x.entity WHERE e.game='mtg' AND e.category='keyword'"): kwc[k].append((con, role))
SELF = re.compile(r"\b(name|this (creature|permanent|vehicle|land|artifact|enchantment|spacecraft|planeswalker|token))\W*$")
def kind(t, k, listed):
    """own / grants / mentions / None for keyword k in prepared text t. Scryfall's keyword list is the card's own keywords
    (abilities and keyword actions such as scry, mill, fight); a keyword not in that list is granted when the text gives it
    to other objects, own when the card gives it to itself, and mentioned when the text only refers to it."""
    kr = re.escape(k)
    if k in listed: return 'own'
    for longer in LONGER.get(k, ()): t = t.replace(longer, '#')   # "double" inside "double strike" is not the keyword
    if not re.search(r'\b' + kr + r'\b', t): return None
    if re.search(r'(^|\n|//[^:\n]*:\s*|\d+\+? \| )\s*(\w+( \w+)?, )*' + kr + r'\b(?=[^.\n]{0,40}(\n|$|,))', t): return 'own'   # keyword line, level line
    res = None
    for m in re.finditer(r'\b(have|has|gains?)\b([^.:;\n]{0,40}?)\b' + kr + r'\b', t):
        mid = m.group(2)
        if re.search(r'life|\bthen\b|\d|counter|control|card|\bdamage\b', mid): continue
        before = re.split(r'[.:;\n—]', t[:m.start()])[-1]
        if re.search(r'\b(name|this (creature|permanent|vehicle|land|artifact|enchantment|spacecraft|token))\b', before) and not re.search(r'\b(other|another|each|all|target|equipped|enchanted|creatures)\b', before): return 'own'
        res = 'grants'
    if res: return res
    if re.search(r'\b(tokens?|becomes?[^.]{0,40}\bcreature)\b[^.]{0,25}\bwith\b[^.]{0,30}\b' + kr + r'\b', t): return 'grants'   # creates or animates bodies with the keyword
    if re.search(r'\b(with|without|has|have|had|loses?|lost|has no)\s+(\w+ ){0,2}' + kr + r'\b', t): return 'mentions'
    return None
def prep(n, t):
    t = re.sub(r'\([^()]*\)', ' ', (t or '').lower())
    for x in [n] + n.split(' // ') + ([n.split(',')[0]] if ',' in n else []):   # a legendary card's short name too
        if len(x) > 2: t = t.replace(x.lower(), 'name')
    return t
for i, n, t, e in q("SELECT id, name, text, ext_id FROM entities WHERE game='mtg' AND category NOT IN ('keyword','tribe')"):
    oid = e.split(':')[-1]; listed = {k.lower() for k in (S.get(oid, {}).get('keywords') or [])}
    pt = prep(n, t)
    have = {(r, d) for r, d in q("SELECT rel, dst FROM entity_links WHERE src=? AND rel IN ('has_keyword','grants_keyword','mentions_keyword')", i)}
    want = set()
    for k, kid in kw.items():
        if len(k) < 3: continue
        r = kind(pt, k, listed)
        if r is None: continue
        want.add(({'own': 'has_keyword', 'grants': 'grants_keyword', 'mentions': 'mentions_keyword'}[r], kid))
    if want == have: continue
    for r, d in have - want:
        c.execute("DELETE FROM entity_links WHERE src=? AND rel=? AND dst=?", (i, r, d)); C['keyword link removed ' + r] += 1
    for r, d in want - have:
        c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (i, r, d, 'keyword in text (Scryfall keywords, 2026-10-12 rule)')); C['keyword link added ' + r] += 1
    # inherited tags: own -> does, grants -> grants; tags from keywords no longer linked that way go
    c.execute("DELETE FROM entity_concepts WHERE entity=? AND method='via_keyword'", (i,))
    for r, d in want:
        if r == 'mentions_keyword': continue
        for con, role in kwc[d]:
            c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (i, con, role if r == 'has_keyword' else 'grants', 'via_keyword', 'inherited from a reviewed keyword'))
c.commit(); print(dict(C))
