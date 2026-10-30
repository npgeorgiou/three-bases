"""Into the Breach, 30 Oct 2026 (Kaptain: a squad has weapons, the starting ones and the extra ones a mech is equipped with):
a mech's starting weapon and passive are cards of their own, listed in the squad next to the mech (decks.tsv). The mech's
record keeps only what the mech is (its keywords: Flying, Massive, Natural Armor); its weapon's and passive's rows stay on the
weapon and passive cards, so nothing is counted twice. Safe to run twice."""
import glob, json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
G = 'into_the_breach'
TEXT = {i: ' '.join((t or '').split()) for i, t in source.lib().execute('select id, text from entities where game=?', (G,))}
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
MECHS = {i for (i,) in c.execute("""select k.id from card k join card_type ct on ct.card=k.id join type t on t.id=ct.type
                                    where k.game=? and t.name='Mech'""", (G,))}


def own_keywords(t):
    m = re.match(r'Keywords: ([^.]+)\.', t)
    return {k.strip() for k in m.group(1).split(',')} if m else set()


def fix(r):
    if r.get('id') not in MECHS or not re.search(r'\bWeapon: ', TEXT.get(r['id'], '')): return 0
    kws = own_keywords(TEXT[r['id']])
    keep = []
    for a in r.get('abilities', []):
        do = [e for e in a['do'] if e.get('act') == 'give_keyword' and (e.get('on') or {}).get('pick') == 'self' and e.get('keyword') in kws]
        if (a.get('when') or {}).get('event') == 'always' and do and len(do) == len(a['do']) and not a.get('if'): keep.append(a)
    if keep == r.get('abilities', []): return 0
    n = len(r.get('abilities', [])) - len(keep)
    r['abilities'] = keep
    for f in ('unsure',): r.pop(f, None)
    return n


for p in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]
    n = sum(fix(r) for r in recs)
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), n, 'changed')
