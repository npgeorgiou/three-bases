"""Search helpers for the Three Bases inspiration library.
Usage: python3 query.py <command> <args>   (see SEARCH_GUIDE.md)"""
import sqlite3, json, sys, collections, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compact_text import clause_text, evidence_text   # Step 6: evidence and clauses are positions in the entry's text
DB = os.environ.get('TB_LIB', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'three-bases-library.sqlite'))  # the database sits next to tools/
db = sqlite3.connect(DB)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import indexes; indexes.fts_temp(db)   # stored without it
q = lambda s, *a: db.execute(s, a).fetchall()

def concepts(term=''):
    """Find concepts by id/name/description."""
    t = f'%{term}%'
    for r in q('''SELECT c.id, c.facet, c.name, (SELECT count(DISTINCT entity) FROM entity_concepts ec JOIN concept_tree ct ON ct.id=ec.concept WHERE ct.root=c.id)
                 FROM concepts c WHERE c.id LIKE ? OR c.name LIKE ? OR c.description LIKE ? ORDER BY c.facet, c.id''', t, t, t):
        print(f'{r[0]:24} {r[1]:10} {r[3]:6}  {r[2]}')

def concept(cid, per_game=4, role=None, game=None, distinct=0):
    """Everything linked to a concept and its sub-concepts, broken down per game. distinct=1: examples skip entries that repeat
    an earlier entry's mechanic (table mechanic_repeat)."""
    c = q('SELECT id, name, facet, description FROM concepts WHERE id=?', cid)
    if not c: print('no concept', cid); return concepts(cid)
    print('==', c[0][1], f'[{c[0][2]}]', c[0][3] or '')
    print('parents:', [r[0] for r in q('SELECT parent FROM concept_parents WHERE child=?', cid)])
    if q("SELECT 1 FROM sqlite_master WHERE name='concept_precision'"):
        w = q('SELECT game, precision FROM concept_precision WHERE concept=? AND precision < 0.7 ORDER BY precision', cid)
        if w: print('WARNING, automatic tags for this concept are often wrong in:', ', '.join(f'{g} ({p:.0%} right)' for g, p in w), '- read the card text there')
    print('children:', [r[0] for r in q('SELECT child FROM concept_parents WHERE parent=?', cid)])
    for a, rel, b, note in q('SELECT a, rel, b, note FROM concept_relations WHERE a=? OR b=?', cid, cid):
        print(f'  relation: {a} --{rel}--> {b}' + (f'  ({note})' if note else ''))
    where = 'ct.root=?' + (' AND ec.role=?' if role else '') + (' AND e.game=?' if game else '') + (' AND e.id NOT IN (SELECT entity FROM mechanic_repeat)' if int(distinct) else '')
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
    """Concepts that most often appear on the same entities (synergy/idea mining). Each game counts equally: per game, the share
    of the concept's entries that also carry the other concept; ranked by the mean share over the games that have the concept."""
    rows = q(f'''SELECT e.game, ec2.concept, count(DISTINCT ec2.entity) FROM entity_concepts ec JOIN concept_tree ct ON ct.id=ec.concept
        JOIN entity_concepts ec2 ON ec2.entity=ec.entity JOIN entities e ON e.id=ec.entity
        WHERE ct.root=? {'AND e.game=?' if game else ''} AND ec2.concept NOT IN (SELECT id FROM concept_tree WHERE root=?)
        GROUP BY 1,2''', *([cid] + ([game] if game else []) + [cid]))
    base = dict(q(f'''SELECT e.game, count(DISTINCT e.id) FROM entity_concepts ec JOIN concept_tree ct ON ct.id=ec.concept JOIN entities e ON e.id=ec.entity
        WHERE ct.root=? {'AND e.game=?' if game else ''} GROUP BY 1''', *([cid] + ([game] if game else []))))
    agg = {}
    for g, k, n in rows: agg.setdefault(k, []).append(n / base[g])
    games = len(base) or 1
    out = sorted(((sum(v) / games, len(v), k) for k, v in agg.items()), reverse=True)[:top]
    print(f'  ({len(base)} games; share = mean over games of the share of entries with {cid} that also have the concept)')
    for sh, ng, k in out: print(f'  {k:24} share {sh:.2f}  games {ng}')

def search(text, game=None, limit=30, per_game=4, distinct=0):
    """Full-text search over names and rules text (FTS5 syntax). At most per_game hits per game (all hits up to limit with game=x).
    distinct=1 skips entries that repeat an earlier entry's mechanic."""
    rows = q(f'''SELECT game, category, name, t FROM (SELECT e.game, e.category, e.name, substr(replace(e.text,char(10),' '),1,220) t,
        row_number() OVER (PARTITION BY e.game ORDER BY f.rank) r FROM entity_fts f JOIN entities e ON e.id=f.rowid
        WHERE entity_fts MATCH ? {'AND e.game=?' if game else ''} {'AND e.id NOT IN (SELECT entity FROM mechanic_repeat)' if int(distinct) else ''}) WHERE r<=? ORDER BY game, r LIMIT ?''', *([text] + ([game] if game else []) + [limit if game else int(per_game), limit if game else 400]))
    for r in rows: print(r)

def entity(name, game=None):
    """Full record of an entity with its keywords, concepts and links."""
    rows = q(f"SELECT * FROM entities WHERE name=? {'AND game=?' if game else ''}", *([name] + ([game] if game else [])))
    if not rows and q("SELECT 1 FROM sqlite_master WHERE name='merged_entities'"):
        rows = q(f"SELECT x.* FROM merged_entities m JOIN entities x ON x.id=m.kept_id WHERE m.name=? {'AND m.game=?' if game else ''}", *([name] + ([game] if game else [])))
        if rows: print(f'{name} was merged into {rows[0][3]} (same mechanic)')
    for e in rows:
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
    if not r and q("SELECT 1 FROM sqlite_master WHERE name='merged_entities'"):
        r = q(f"SELECT x.id, x.game, x.name FROM merged_entities m JOIN entities x ON x.id=m.kept_id WHERE m.name=? {'AND m.game=?' if game else ''}", *([name] + ([game] if game else [])))
        if r: print(f'{name} was merged into {r[0][2]} (same mechanic)')
    if not r:   # a combo can name a keyword (an Inscryption sigil given to a card) or a tribe (a totem gives a sigil to a tribe)
        r = q(f"SELECT id, game, name FROM entities WHERE name=? {'AND game=?' if game else ''} AND category IN ('keyword','tribe')", *([name] + ([game] if game else [])))
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

_ANC = {}
def _anc(c):
    """A concept with all its ancestors (a payoff for a parent concept is also a payoff for its children)."""
    if not _ANC:   # the whole tree once: one query instead of one per concept per call
        for i, r in q('SELECT id, root FROM concept_tree'): _ANC.setdefault(i, set()).add(r)
    return _ANC.get(c, set()) | {c}

FEEDS = {   # which effects set off which triggers (Claude's mapping)
    'on_ally_play': {'summon', 'revive', 'free_play'}, 'death_count': {'sacrifice', 'destroy', 'self_destruct', 'board_wipe', 'aoe_damage'},
    'on_damaged': {'damage', 'friendly_fire'}, 'on_attack': {'attack_now', 'haste', 'multi_attack', 'forced_attack'},
    'on_kill': {'destroy', 'deathtouch'}, 'on_play': {'blink', 'copy', 'return_to_hand'}, 'death_trigger': {'sacrifice', 'self_destruct', 'destroy'},
    'other_death_trigger': {'sacrifice', 'self_destruct', 'destroy', 'board_wipe', 'aoe_damage'}, 'leave_trigger': {'sacrifice', 'self_destruct', 'destroy', 'blink', 'return_to_hand'},
    'other_leave_trigger': {'sacrifice', 'self_destruct', 'destroy', 'board_wipe', 'blink', 'return_to_hand', 'banish', 'bounce_enemy'},
    'on_life_loss': {'life_payment', 'friendly_fire'}, 'on_lifegain': {'heal', 'lifesteal'}, 'on_draw': {'draw', 'tutor'}, 'on_discard': {'discard'},
    'on_sacrifice': {'sacrifice'}, 'on_targeted': set(), 'on_block': set()}

def connections(ia, ib):
    """Every known connection between two entities, by layer: link, type, keyword, role (exact), role (concept tree), relation, engine."""
    out = []
    for r in q('SELECT rel FROM entity_links WHERE src=? AND dst=?', ia, ib): out.append(('link', f'A {r[0]} B'))
    for r in q('SELECT rel FROM entity_links WHERE src=? AND dst=?', ib, ia): out.append(('link', f'B {r[0]} A'))
    for k, r1, r2, cat in q('SELECT k.name, l1.rel, l2.rel, k.category FROM entity_links l1 JOIN entity_links l2 ON l1.dst=l2.dst JOIN entities k ON k.id=l1.dst WHERE l1.src=? AND l2.src=? AND k.category IN ("keyword","tribe")', ia, ib):
        out.append(('type' if cat == 'tribe' else 'keyword', f'{k} (A {r1}, B {r2})'))
    cats = {i: (q('SELECT category FROM entities WHERE id=?', i) or [(None,)])[0][0] for i in (ia, ib)}
    if {cats[ia], cats[ib]} == {'tribe', 'keyword'}:   # a tribe and a keyword: cards of the tribe that bear the keyword
        t, k = (ia, ib) if cats[ia] == 'tribe' else (ib, ia)
        for (n,) in q("SELECT DISTINCT e.name FROM entity_links a JOIN entity_links b ON a.src=b.src JOIN entities e ON e.id=a.src WHERE a.dst=? AND a.rel='has_type' AND b.dst=? AND b.rel='has_keyword'", t, k):
            out.append(('type', f'{n} is of the tribe and bears the keyword'))
    ca = q('SELECT concept, role FROM entity_concepts WHERE entity=?', ia); cb = q('SELECT concept, role FROM entity_concepts WHERE entity=?', ib)
    rel = {}
    for a, r, b in q('SELECT a, rel, b FROM concept_relations WHERE rel IN ("synergizes","enables")'):
        rel.setdefault((a, b), r); rel.setdefault((b, a), r)
    for x, y, lx, ly in ((ca, cb, 'A', 'B'), (cb, ca, 'B', 'A')):
        does = {c for c, r in x if r in ('does', 'grants')}; need = {c for c, r in y if r in ('benefits', 'cost')}
        for c in sorted(does & need): out.append(('role', f'{lx} does {c}, {ly} benefits'))
        for c in sorted({c for c, r in x if r == 'cost'} & {c for c, r in y if r == 'benefits'}): out.append(('role', f'{lx} pays {c} as a cost, {ly} benefits'))
        for c in sorted(does):
            for n in sorted((_anc(c) - {c}) & need): out.append(('role_tree', f'{lx} does {c} (a kind of {n}), {ly} benefits from {n}'))
        for c in sorted(does):
            for n in sorted({d for d, r in y if r in ('benefits', 'cost', 'does')}):
                hit = [(a, b) for a in _anc(c) for b in _anc(n) if (a, b) in rel]
                if hit: out.append(('relation', f'{lx} does {c}, {ly} has {n}: {hit[0][0]} {rel[hit[0]]} {hit[0][1]}'))
    # engine: one card's trigger is the other's effect (enabler -> payoff), from trigger_effect
    for x, y, lx, ly in ((ia, ib, 'A', 'B'), (ib, ia, 'B', 'A')):
        trig_ids = {i for (i,) in q("SELECT id FROM concept_tree WHERE root='trigger'")}
        eff = {e for (e,) in q('SELECT effect FROM trigger_effect WHERE entity=?', x)} | {c for c, r in q('SELECT concept, role FROM entity_concepts WHERE entity=?', x) if r in ('does', 'grants', 'cost') and c not in trig_ids}   # paying a cost (life, a unit) is doing it
        cat = q('SELECT category FROM entities WHERE id=?', x)[0][0]
        tp = q('SELECT DISTINCT trigger, effect FROM trigger_effect WHERE entity=?', y)
        tp += [(t, 'its effect') for (t,) in q("SELECT concept FROM entity_concepts WHERE entity=? AND role='trigger'", y) if t not in {a for a, _ in tp}]   # a trigger tag without a stored pair
        for t, e in tp:
            m = sorted(c for c in eff if t in _anc(c) or (FEEDS.get(t, set()) & _anc(c)))
            if t == 'on_spell' and cat == 'spell': m = m or ['a spell']
            if m: out.append(('engine', f'{lx} does {m[0]} -> {ly} triggers on {t} ({e})'))
    seen = set(); res = []
    for o in out:
        if o not in seen: seen.add(o); res.append(o)
    return res

def combo(a, b, game=None):
    """Explain every known connection between two cards, layer by layer (link, type, keyword, role, role_tree, relation, engine)."""
    ea, eb = _ent(a, game), _ent(b, game)
    if not ea or not eb: return
    res = connections(ea[0], eb[0])
    if not res: print('no known connection'); return
    for layer, d in res[:40]: print(f'  {layer:10} {d}')

def grid(trigger=None, effect=None, game=None, examples=3, freq=None):
    """Trigger x effect design space. With no args: matrix of counts (games using each pair). With trigger and/or effect: examples per game."""
    w = ' AND '.join(x for x in ['trigger IN (SELECT id FROM concept_tree WHERE root=?)' if trigger else '', 'effect IN (SELECT id FROM concept_tree WHERE root=?)' if effect else '', 'game=?' if game else '', 'frequency=?' if freq else ''] if x) or '1=1'
    args = [a for a in (trigger, effect, game, freq) if a]
    if not trigger and not effect:
        for r in q(f'SELECT trigger, effect, count(*), count(DISTINCT game) FROM trigger_effect WHERE {w} GROUP BY 1,2 ORDER BY 4 DESC, 3 DESC LIMIT 60', *args): print(f'  {r[0]:18} -> {r[1]:20} entries {r[2]:5} games {r[3]}')
        return
    for r in q(f'SELECT trigger, effect, count(*), count(DISTINCT game) FROM trigger_effect WHERE {w} GROUP BY 1,2 ORDER BY 3 DESC LIMIT 40', *args): print(f'  {r[0]:18} -> {r[1]:20} entries {r[2]:5} games {r[3]}')
    for g, in q(f'SELECT DISTINCT game FROM trigger_effect WHERE {w}', *args):
        print('--', g)
        for e, f, p, l in q(f'SELECT entity, cl_form, cl_pos, cl_len FROM trigger_effect WHERE {w} AND game=? ORDER BY random() LIMIT ?', *args, g, examples): print('    ', (clause_text(db, e, f, p, l) or '')[:160])

def unused_pairs(trigger):
    """Effects that no game pairs with this trigger (gaps in the design space)."""
    used = {r[0] for r in q('SELECT DISTINCT effect FROM trigger_effect WHERE trigger IN (SELECT id FROM concept_tree WHERE root=?)', trigger)}
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

def frequency(bound=None, trigger=None, effect=None, game=None, examples=3):
    """Trigger -> effect pairs by frequency limit (per_card, per_round, unbounded, static). No bound: per bound, its share of each
    game's pairs, averaged over games (each game counts equally), with the raw count. With a bound: pairs ranked by the number of
    games that have them, then by the mean share per game."""
    w = ' AND '.join(x for x in ['frequency=?' if bound else '', 'trigger IN (SELECT id FROM concept_tree WHERE root=?)' if trigger else '', 'effect IN (SELECT id FROM concept_tree WHERE root=?)' if effect else '', 'game=?' if game else ''] if x) or '1=1'
    args = [a for a in (bound, trigger, effect, game) if a]
    tot = dict(q('SELECT game, count(*) FROM trigger_effect GROUP BY 1'))
    if not bound:
        per = {}
        for f, g, n in q(f'SELECT frequency, game, count(*) FROM trigger_effect WHERE {w} GROUP BY 1,2', *args): per.setdefault(f, {})[g] = n
        gs = {g for d in per.values() for g in d}
        for f, d in sorted(per.items(), key=lambda x: -sum(n / tot[g] for g, n in x[1].items())):
            print(f'  {f:10} mean share {sum(n / tot[g] for g, n in d.items()) / len(gs):.2f}  entries {sum(d.values()):6}  games {len(d)}')
        return
    per = {}
    for t, e, g, n in q(f'SELECT trigger, effect, game, count(*) FROM trigger_effect WHERE {w} GROUP BY 1,2,3', *args): per.setdefault((t, e), {})[g] = n
    for (t, e), d in sorted(per.items(), key=lambda x: (-len(x[1]), -sum(n / tot[g] for g, n in x[1].items())))[:25]:
        print(f'  {t:18} -> {e:20} games {len(d):2}  mean share {sum(n / tot[g] for g, n in d.items()) / len(d):.3f}  entries {sum(d.values())}')
    for g, in q(f'SELECT DISTINCT game FROM trigger_effect WHERE {w}', *args):
        print('--', g)
        for n, e, f, p, l, b in q(f'SELECT x.name, t.entity, t.cl_form, t.cl_pos, t.cl_len, t.basis FROM trigger_effect t JOIN entities x ON x.id=t.entity WHERE {w.replace("game=?", "t.game=?")} AND t.game=? ORDER BY random() LIMIT ?', *args, g, examples):
            print(f'    {n}: {(clause_text(db, e, f, p, l) or "")[:130]}  [{b}]')

def signature(game, faction=None, per=3):
    """Per source faction: its signature mechanics (with example cards) and the other factions' mechanics it splashes."""
    fs = [faction] if faction else [f for (f,) in q('SELECT DISTINCT faction FROM faction_signature WHERE game=? ORDER BY 1', game)]
    for f in fs:
        sig = q("SELECT concept, entities, share, lift FROM faction_signature WHERE game=? AND faction=? AND kind='signature' ORDER BY lift DESC", game, f)
        print(f'== {f}')
        for k, n, s, l in sig:
            ex = q("SELECT DISTINCT x.name FROM entities x JOIN entity_concepts ec ON ec.entity=x.id WHERE x.game=? AND x.faction=? AND ec.concept=? AND ec.role IN ('does','grants') AND x.category NOT IN ('keyword','tribe') ORDER BY random() LIMIT ?", game, f, k, per)
            print(f'   signature {k:22} cards {n:4} share {s:.2f} lift {l:4}  e.g. ' + ', '.join(e[0] for e in ex))
        kws = q("SELECT concept, entities, lift FROM faction_signature WHERE game=? AND faction=? AND kind='keyword_signature' ORDER BY entities DESC", game, f)
        if kws: print('   own keywords:', ', '.join(f'{k[3:]} ({n} cards, {int(l * 100)}% of its uses)' for k, n, l in kws))
        sp = q("SELECT concept, entities, owner FROM faction_signature WHERE game=? AND faction=? AND kind='splash' ORDER BY entities LIMIT 12", game, f)
        if sp: print('   splash (others\' signatures, few cards):', ', '.join(f'{k} x{n} (of {o})' for k, n, o in sp))

def splash(concept, game=None, per=3):
    """Cards that use another faction's signature mechanic sparingly, per game, with the splashing faction's own signatures each card also carries."""
    games = [game] if game else [g for (g,) in q("SELECT DISTINCT game FROM faction_signature WHERE concept=? AND kind='splash' ORDER BY 1", concept)]
    for g in games:
        own = q("SELECT faction, share FROM faction_signature WHERE game=? AND concept=? AND kind='signature' ORDER BY share DESC", g, concept)
        print(f'== {g}: signature of', ', '.join(f'{f} ({s:.2f})' for f, s in own) or 'no faction')
        for f, n, s in q("SELECT faction, entities, share FROM faction_signature WHERE game=? AND concept=? AND kind='splash' ORDER BY entities", g, concept):
            fsig = {k for (k,) in q("SELECT concept FROM faction_signature WHERE game=? AND faction=? AND kind='signature'", g, f)}
            cards = q("SELECT DISTINCT x.id, x.name, x.text FROM entities x JOIN entity_concepts ec ON ec.entity=x.id WHERE x.game=? AND x.faction=? AND ec.concept=? AND ec.role IN ('does','grants') AND x.category NOT IN ('keyword','tribe') ORDER BY random() LIMIT ?", g, f, concept, per)
            print(f'   {f}: {n} cards (share {s:.2f})')
            for i, nm, t in cards:
                tr = sorted(fsig & {k for (k,) in q("SELECT concept FROM entity_concepts WHERE entity=? AND role IN ('does','grants')", i)})
                print(f'     {nm}: {(t or "")[:110]}' + (f'  [own trait: {", ".join(tr)}]' if tr else ''))

def games():
    for r in q('SELECT g.id, g.name, (SELECT count(*) FROM entities WHERE game=g.id), g.structure FROM games g'): print(r)
    for r in q('SELECT game, category, count(*) FROM entities GROUP BY 1,2 ORDER BY 1,3 DESC'): print('  ', r)

if __name__ == '__main__':
    cmd, *a = sys.argv[1:]
    kw = {k: (int(v) if v.isdigit() else v) for k, v in (x.split('=', 1) for x in a if '=' in x)}
    pos = [x for x in a if '=' not in x]
    globals()[cmd](*pos, **kw)
