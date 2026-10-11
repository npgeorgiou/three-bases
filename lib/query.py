"""Search helpers for the Three Bases inspiration library.
Usage: python3 query.py <command> <args>   (see SEARCH_GUIDE.md)"""
import sqlite3, json, sys, collections, os
DB = os.environ.get('TB_LIB', '/home/claude/library/three-bases-library.sqlite')
db = sqlite3.connect(DB)
q = lambda s, *a: db.execute(s, a).fetchall()

def concepts(term=''):
    """Find concepts by id/name/description."""
    t = f'%{term}%'
    for r in q('''SELECT c.id, c.facet, c.name, (SELECT count(DISTINCT entity) FROM entity_concepts ec JOIN concept_tree ct ON ct.id=ec.concept WHERE ct.root=c.id)
                 FROM concepts c WHERE c.id LIKE ? OR c.name LIKE ? OR c.description LIKE ? ORDER BY c.facet, c.id''', t, t, t):
        print(f'{r[0]:24} {r[1]:10} {r[3]:6}  {r[2]}')

def concept(cid, per_game=4, role=None, game=None):
    """Everything linked to a concept and its sub-concepts, broken down per game."""
    c = q('SELECT id, name, facet, description FROM concepts WHERE id=?', cid)
    if not c: print('no concept', cid); return concepts(cid)
    print('==', c[0][1], f'[{c[0][2]}]', c[0][3] or '')
    print('parents:', [r[0] for r in q('SELECT parent FROM concept_parents WHERE child=?', cid)])
    print('children:', [r[0] for r in q('SELECT child FROM concept_parents WHERE parent=?', cid)])
    for a, rel, b, note in q('SELECT a, rel, b, note FROM concept_relations WHERE a=? OR b=?', cid, cid):
        print(f'  relation: {a} --{rel}--> {b}' + (f'  ({note})' if note else ''))
    where = 'ct.root=?' + (' AND ec.role=?' if role else '') + (' AND e.game=?' if game else '')
    args = [cid] + ([role] if role else []) + ([game] if game else [])
    rows = q(f'''SELECT e.game, e.category, ec.role, count(DISTINCT e.id) FROM entity_concepts ec
        JOIN concept_tree ct ON ct.id=ec.concept JOIN entities e ON e.id=ec.entity WHERE {where} GROUP BY 1,2,3 ORDER BY 1,4 DESC''', *args)
    print('counts (game, category, role, n):'); [print('  ', r) for r in rows]
    for g, in q(f'SELECT DISTINCT e.game FROM entity_concepts ec JOIN concept_tree ct ON ct.id=ec.concept JOIN entities e ON e.id=ec.entity WHERE {where}', *args):
        print(f'-- {g}: keywords')
        for r in q(f'''SELECT DISTINCT e.name, ec.concept, ec.role, substr(replace(e.text,char(10),' '),1,160) FROM entity_concepts ec JOIN concept_tree ct ON ct.id=ec.concept
            JOIN entities e ON e.id=ec.entity WHERE {where} AND e.game=? AND e.category='keyword' LIMIT 40''', *args, g):
            print(f'   [{r[1]}/{r[2]}] {r[0]}: {r[3]}')
        print(f'-- {g}: examples (one per category/role, most specific first)')
        for r in q(f'''SELECT e.category, ec.role, e.name, ec.concept, ec.method, substr(replace(e.text,char(10),' '),1,200) FROM entity_concepts ec
            JOIN concept_tree ct ON ct.id=ec.concept JOIN entities e ON e.id=ec.entity
            WHERE {where} AND e.game=? AND e.category<>'keyword' ORDER BY e.category, ec.role, (ec.method='claude_review') DESC, random() ''', *args, g)[:200]:
            pass
        seen = collections.Counter()
        for r in q(f'''SELECT e.category, ec.role, e.name, ec.concept, ec.method, substr(replace(e.text,char(10),' '),1,200) FROM entity_concepts ec
            JOIN concept_tree ct ON ct.id=ec.concept JOIN entities e ON e.id=ec.entity
            WHERE {where} AND e.game=? AND e.category<>'keyword' ORDER BY random() LIMIT 400''', *args, g):
            k = (r[0], r[1])
            if seen[k] >= per_game: continue
            seen[k] += 1
            print(f'   {r[0]}/{r[1]} [{r[3]} via {r[4]}] {r[2]}: {r[5]}')

def cooccur(cid, game=None, top=25):
    """Concepts that most often appear on the same entities (synergy/idea mining)."""
    args = [cid] + ([game] if game else [])
    rows = q(f'''SELECT ec2.concept, count(DISTINCT ec2.entity) n FROM entity_concepts ec JOIN concept_tree ct ON ct.id=ec.concept
        JOIN entity_concepts ec2 ON ec2.entity=ec.entity JOIN entities e ON e.id=ec.entity
        WHERE ct.root=? {'AND e.game=?' if game else ''} AND ec2.concept NOT IN (SELECT id FROM concept_tree WHERE root=?)
        GROUP BY 1 ORDER BY 2 DESC LIMIT ?''', *args, cid, top)
    for r in rows: print(f'  {r[0]:24} {r[1]}')

def search(text, game=None, limit=30):
    """Full-text search over names and rules text (FTS5 syntax)."""
    rows = q(f'''SELECT e.game, e.category, e.name, substr(replace(e.text,char(10),' '),1,220) FROM entity_fts f JOIN entities e ON e.id=f.rowid
        WHERE entity_fts MATCH ? {'AND e.game=?' if game else ''} LIMIT ?''', *([text] + ([game] if game else []) + [limit]))
    for r in rows: print(r)

def entity(name, game=None):
    """Full record of an entity with its keywords, concepts and links."""
    for e in q(f"SELECT * FROM entities WHERE name=? {'AND game=?' if game else ''}", *([name] + ([game] if game else []))):
        cols = [d[0] for d in db.execute('SELECT * FROM entities LIMIT 0').description]
        for c, v in zip(cols, e):
            if v not in (None, ''): print(f'{c}: {v}')
        print('concepts:', q('SELECT concept, role, method FROM entity_concepts WHERE entity=?', e[0]))
        print('links out:', q('SELECT l.rel, x.name FROM entity_links l JOIN entities x ON x.id=l.dst WHERE l.src=?', e[0]))
        print('links in:', q('SELECT l.rel, x.name FROM entity_links l JOIN entities x ON x.id=l.src WHERE l.dst=? LIMIT 30', e[0]))
        print()

def faction(game, name=None):
    for f, n, p in q(f"SELECT name, entity_count, profile FROM factions WHERE game=? {'AND name=?' if name else ''}", *([game] + ([name] if name else []))):
        print(f'== {game} / {f} ({n} entities)')
        for x in json.loads(p): print(f"   {x['concept']:24} share {x['share']:.2f}  lift {x['lift']}")

def problem(pid):
    """Design problem -> concepts that mitigate it or are in tension with it, with example counts."""
    concept(pid, per_game=2)
    print('== related mechanics')
    for a, rel, b, note in q("SELECT a, rel, b, note FROM concept_relations WHERE b=? OR a=?", pid, pid):
        other = a if b == pid else b
        n = q('SELECT count(DISTINCT ec.entity) FROM entity_concepts ec JOIN concept_tree ct ON ct.id=ec.concept WHERE ct.root=?', other)[0][0]
        print(f'  {other:24} {rel:12} entities: {n}  {note}')

def _ent(name, game=None):
    r = q(f"SELECT id, game, name FROM entities WHERE name=? {'AND game=?' if game else ''} AND category NOT IN ('keyword','tribe')", *([name] + ([game] if game else [])))
    if not r: print('not found', name); return None
    if len(r) > 1: print('several matches, using first:', r[:5])
    return r[0]

def interactions(name, game=None, per=8):
    """Cards that interact with this card: direct references, shared types, keyword partners and concept partners (role-matched)."""
    e = _ent(name, game)
    if not e: return
    eid, g, nm = e
    print('==', nm, f'[{g}]')
    print('-- direct links (this card names / is named by):')
    for rel, n2 in q('SELECT l.rel, x.name FROM entity_links l JOIN entities x ON x.id=l.dst WHERE l.src=? AND l.rel IN ("references","summons","generates","transforms_into","variant_of")', eid): print(f'   {rel} -> {n2}')
    for rel, n2 in q('SELECT l.rel, x.name FROM entity_links l JOIN entities x ON x.id=l.src WHERE l.dst=? AND l.rel IN ("references","summons","generates","transforms_into")', eid)[:per]: print(f'   {n2} {rel} -> this')
    print('-- types: this card is / cares about:')
    for rel, tid, tn in q('SELECT l.rel, x.id, x.name FROM entity_links l JOIN entities x ON x.id=l.dst WHERE l.src=? AND l.rel IN ("has_type","cares_about_type")', eid):
        other = 'cares_about_type' if rel == 'has_type' else 'has_type'
        ps = q('SELECT x.name FROM entity_links l JOIN entities x ON x.id=l.src WHERE l.dst=? AND l.rel=? AND x.id<>? ORDER BY random() LIMIT ?', tid, other, eid, per)
        print(f'   {rel} {tn}: partners ({other}):', ', '.join(p[0] for p in ps))
    print('-- keyword partners:')
    for rel, kid, kn in q('SELECT l.rel, k.id, k.name FROM entity_links l JOIN entities k ON k.id=l.dst WHERE l.src=? AND k.category="keyword"', eid):
        other = ('grants_keyword', 'mentions_keyword') if rel == 'has_keyword' else ('has_keyword',)
        ps = q(f'SELECT x.name, l.rel FROM entity_links l JOIN entities x ON x.id=l.src WHERE l.dst=? AND l.rel IN ({",".join("?"*len(other))}) AND x.id<>? ORDER BY random() LIMIT ?', kid, *other, eid, per)
        print(f'   {rel} {kn}:', ', '.join(f'{a} ({b})' for a, b in ps))
    print('-- concept partners in the same game (what this benefits from <-> who does it; what this does <-> who benefits):')
    mine = q('SELECT concept, role FROM entity_concepts WHERE entity=?', eid)
    does = {c for c, r in mine if r in ('does', 'grants')}; ben = {c for c, r in mine if r == 'benefits'}; cost = {c for c, r in mine if r == 'cost'}
    rel = q('SELECT a, b FROM concept_relations WHERE rel IN ("synergizes","enables")')
    syn = {a: set() for a, _ in rel}
    for a, b in rel: syn.setdefault(a, set()).add(b); syn.setdefault(b, set()).add(a)
    def partners(concepts, roles, label):
        for c in sorted(concepts):
            ps = q(f'SELECT DISTINCT x.name FROM entity_concepts ec JOIN concept_tree ct ON ct.id=ec.concept JOIN entities x ON x.id=ec.entity WHERE ct.root=? AND x.game=? AND x.id<>? AND ec.role IN ({",".join("?"*len(roles))}) AND x.category NOT IN ("keyword","tribe") ORDER BY random() LIMIT ?', c, g, eid, *roles, per)
            if ps: print(f'   {label} {c}:', ', '.join(p[0] for p in ps))
    partners(ben | cost, ('does', 'grants'), 'needs/benefits from')
    partners({b for c in (ben | cost) for b in syn.get(c, ())} - ben - cost, ('does', 'grants'), 'enabled by (concept relation)')
    partners(does, ('benefits',), 'feeds (cards that benefit from)')
    partners({b for c in does for b in syn.get(c, ())} - does, ('does', 'grants'), 'synergy (concept relation) with')

def combo(a, b, game=None):
    """Explain every known connection between two cards."""
    ea, eb = _ent(a, game), _ent(b, game)
    if not ea or not eb: return
    ia, ib = ea[0], eb[0]
    print('direct:', q('SELECT rel FROM entity_links WHERE (src=? AND dst=?) OR (src=? AND dst=?)', ia, ib, ib, ia))
    print('shared keywords:', q('SELECT k.name, l1.rel, l2.rel FROM entity_links l1 JOIN entity_links l2 ON l1.dst=l2.dst JOIN entities k ON k.id=l1.dst WHERE l1.src=? AND l2.src=? AND k.category IN ("keyword","tribe")', ia, ib))
    ca = q('SELECT concept, role FROM entity_concepts WHERE entity=?', ia); cb = q('SELECT concept, role FROM entity_concepts WHERE entity=?', ib)
    print('A does what B benefits from:', sorted({c for c, r in ca if r in ('does','grants')} & {c for c, r in cb if r in ('benefits','cost')}))
    print('B does what A benefits from:', sorted({c for c, r in cb if r in ('does','grants')} & {c for c, r in ca if r in ('benefits','cost')}))
    rel = q('SELECT a, rel, b FROM concept_relations')
    sa = {c for c, _ in ca}; sb = {c for c, _ in cb}
    print('concept relations between their concepts:', [(x, r, y) for x, r, y in rel if (x in sa and y in sb) or (x in sb and y in sa)][:20])

def grid(trigger=None, effect=None, game=None, examples=3):
    """Trigger x effect design space. With no args: matrix of counts (games using each pair). With trigger and/or effect: examples per game."""
    w = ' AND '.join(x for x in ['trigger=?' if trigger else '', 'effect=?' if effect else '', 'game=?' if game else ''] if x) or '1=1'
    args = [a for a in (trigger, effect, game) if a]
    if not trigger and not effect:
        for r in q(f'SELECT trigger, effect, count(*), count(DISTINCT game) FROM trigger_effect WHERE {w} GROUP BY 1,2 ORDER BY 4 DESC, 3 DESC LIMIT 60', *args): print(f'  {r[0]:18} -> {r[1]:20} entries {r[2]:5} games {r[3]}')
        return
    for r in q(f'SELECT trigger, effect, count(*), count(DISTINCT game) FROM trigger_effect WHERE {w} GROUP BY 1,2 ORDER BY 3 DESC LIMIT 40', *args): print(f'  {r[0]:18} -> {r[1]:20} entries {r[2]:5} games {r[3]}')
    for g, in q(f'SELECT DISTINCT game FROM trigger_effect WHERE {w}', *args):
        print('--', g)
        for c, in q(f'SELECT clause FROM trigger_effect WHERE {w} AND game=? ORDER BY random() LIMIT ?', *args, g, examples): print('    ', c[:160])

def unused_pairs(trigger):
    """Effects that no game pairs with this trigger (gaps in the design space)."""
    used = {r[0] for r in q('SELECT DISTINCT effect FROM trigger_effect WHERE trigger=?', trigger)}
    allf = {r[0] for r in q('SELECT DISTINCT effect FROM trigger_effect')}
    print(sorted(allf - used))

def archetypes(name=None, game=None):
    """Faction archetypes. No args: list archetypes with their factions. With an archetype id: factions per game. With game=: archetypes of each faction."""
    if game and not name:
        for f, a in q('SELECT faction, group_concat(archetype || " (x" || lift || ")", ", ") FROM faction_archetypes WHERE game=? GROUP BY 1', game): print(f'  {f}: {a}')
        return
    for aid, d, cs in q('SELECT id, description, concepts FROM archetypes' + (' WHERE id=?' if name else ''), *([name] if name else [])):
        print(f'== {aid}: {d}  concepts: {cs}')
        for g, f, s, l in q('SELECT game, faction, share, lift FROM faction_archetypes WHERE archetype=? ORDER BY lift DESC' + ('' if name else ' LIMIT 8'), aid): print(f'   {g:16} {f:35} share {s:.2f} lift {l}')

def games():
    for r in q('SELECT g.id, g.name, (SELECT count(*) FROM entities WHERE game=g.id), g.structure FROM games g'): print(r)
    for r in q('SELECT game, category, count(*) FROM entities GROUP BY 1,2 ORDER BY 1,3 DESC'): print('  ', r)

if __name__ == '__main__':
    cmd, *a = sys.argv[1:]
    kw = {k: (int(v) if v.isdigit() else v) for k, v in (x.split('=', 1) for x in a if '=' in x)}
    pos = [x for x in a if '=' not in x]
    globals()[cmd](*pos, **kw)
