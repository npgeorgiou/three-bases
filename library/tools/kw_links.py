"""Step 4 of the tag-fix plan: keywords (build step after pattern_fix.py, before parent_rule.py).
1. Keyword entries get the tags their two readers (and a third for disagreements) read from them: tools/key/kw_<game>/key.json.
   An older tag of the keyword stays when the keyword's own text justifies it (a wording pattern of that concept matches) or a
   hand review confirmed it; a hand-reviewed drop is never added.
   Entries both readers marked as not a real keyword of the game (notkw.json) lose their has/grants links.
2. Link rule: a card has a keyword only when the word is used as that game's keyword:
     - listed for that card in the source data (link evidence names a source field or list), or
     - standing where the game prints keywords: at the start of the text or of a line, sentence or clause (after '.', ':', ';',
       '-', '/', a line break, or in a 'Keywords:' list) and followed by the end of the clause (end, '.', ',', ':', ';', '-',
       '(', a number or a line break) -- 'Taunt', 'Deathrattle: ...', 'Countdown (1)', 'Production - ...';
     - or, for a keyword action (the keyword's own reading says it does something when used: Freeze, Discover, Silence),
       standing at such a start as the verb of the clause ('Freeze a minion.').
   Other has_keyword links become mentions_keyword ('a minion with Taunt', 'trigger a Deathrattle').
3. Inheritance only through has_keyword and grants_keyword links, never through a mention. A card's via_keyword tags become
   the union of its has/grants keywords' tags. A via_keyword tag that no remaining link supports is checked against the card's
   own text before it goes: it stays, as the card's own tag (method text_pattern, evidence 'kept: own text, step 4'), when a
   wording pattern of that concept matches the text or the answer key / a judged sample says the card has it; else it is removed.
The per-game rule was tested on the answer-key entries (tools/key/kw_rule_test.txt). Usage: kw_links.py <db> [test]"""
import collections, glob, json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KEYD = os.path.join(HERE, 'key')
sys.path.insert(0, os.path.join(HERE, 'step3')); sys.path.insert(0, HERE)
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
TEST = sys.argv[2:] == ['test']
sys.path.insert(0, HERE)
from step_games import step_games
ALLOW = step_games('kw_links')   # None = every game
FIELD = re.compile(r'field|list|scryfall|sigils|special|traits|warscroll', re.I)
B = r"(?:^|[\n.:;/]\s*|\s-\s*|-{3,}\s*|keywords?:\s*(?:[^.\n]*?,\s*)*)"

def kw_reading():
    """keyword entity id -> (set of concepts read, not-real flag), for keywords whose reading is final."""
    out = {}
    for d in glob.glob(os.path.join(KEYD, 'kw_*')):
        kf = os.path.join(d, 'key.json')
        if not os.path.exists(kf): continue
        notk = []
        for r in ('A', 'B'):
            f = os.path.join(d, r, 'notkw.json')
            notk.append({int(x) for x in json.load(open(f))} if os.path.exists(f) else set())
        both = notk[0] & notk[1]
        for i, v in json.load(open(kf)).items(): out[int(i)] = ({k for k, _ in v['tags']}, int(i) in both)
    return out

def valid(text, kname, action):
    t = text or ''; k = re.escape(kname)
    if re.search(B + k + r"(?=\s*(?:$|[\n.,:;(/]|\d|\s-))", t, re.I): return True
    if action and re.search(B + k + r"\s+(?:a|an|the|all|each|your|any|one|two|three|\d|it|them|this|that|up to|another|enemy|friendly|random)\b", t, re.I): return True
    return False

read = kw_reading()
kws = {i: (g, n) for i, g, n in q("SELECT id, game, name FROM entities WHERE category='keyword'")}
if ALLOW is not None: read = {i: v for i, v in read.items() if kws.get(i, ('',))[0] in ALLOW}
txt = dict(q('SELECT id, text FROM entities'))
ACTION = {'damage', 'destroy', 'draw', 'summon', 'generate_cards', 'disable', 'silence', 'selection', 'transform', 'movement',
          'forced_movement', 'discard', 'copy', 'heal', 'stat_gain', 'stat_loss', 'banish', 'bounce_enemy', 'return_to_hand', 'tutor'}
def is_action(kid):
    ks = read.get(kid, (set(), False))[0] or {k for k, in q("SELECT concept FROM entity_concepts WHERE entity=?", kid)}
    return bool(ks & ACTION)

# The position rule is applied only where the rule test (kw_rule_test.txt, 19 Oct 2026, after the keyword readings) showed the
# dropped links' tags as mostly wrong (50% or less right) and less right than the kept links' tags; elsewhere dropping them would
# lose right tags (not-real keywords still lose their links everywhere).
SKIP = {'hearthstone', 'into_the_breach', 'faeria', 'hs_battlegrounds', 'marvel_snap', 'shadowverse', 'sts1'}
links = q("SELECT l.rowid, l.src, l.dst, l.evidence FROM entity_links l WHERE l.rel='has_keyword'")
drop = []
for rid, s, d, ev in links:
    if d not in kws: continue
    if ALLOW is not None and kws[d][0] not in ALLOW: continue
    if kws[d][0] in SKIP and not read.get(d, (None, False))[1]: continue
    if read.get(d, (None, False))[1]: drop.append(rid); continue
    if ev and FIELD.search(ev): continue
    if not valid(txt.get(s), kws[d][1], is_action(d)): drop.append(rid)
if TEST:
    # rule test on key entries: tags the dropped links pass on, compared with the key
    import patterns3 as P
    ky = P.keys(); kk = {e: ks for g in ky.values() for e, ks in g.items()}
    stat = collections.defaultdict(lambda: [0, 0, 0, 0])   # game: kept-link tags right/all, dropped-link tags right/all
    dropset = set(drop)
    for rid, s, d, ev in links:
        if s not in kk or d not in kws: continue
        ks = read.get(d, (set(), False))[0] or {k for k, in q("SELECT concept FROM entity_concepts WHERE entity=?", d)}
        g = kws[d][0]; i = 2 if rid in dropset else 0
        for k in ks:
            stat[g][i + 1] += 1; stat[g][i] += P.right(k, kk[s])
    with open(os.path.join(KEYD, 'kw_rule_test.txt'), 'w') as fh:
        for g, (kr, ka, dr, da) in sorted(stat.items()):
            line = f'{g:18} kept links: tags right {kr}/{ka} ({100 * kr / max(ka, 1):.0f}%)   dropped links: tags right {dr}/{da} ({100 * dr / max(da, 1):.0f}%)'
            print(line); fh.write(line + '\n')
    sys.exit(0)
c.executemany("UPDATE OR IGNORE entity_links SET rel='mentions_keyword' WHERE rowid=?", [(r,) for r in drop])
c.executemany("DELETE FROM entity_links WHERE rowid=? AND rel='has_keyword'", [(r,) for r in drop])   # a mention link already existed
# 1. keyword entries' own tags (a tag an earlier hand review confirmed stays; one it dropped is not added)
import csv as _csv
from concept_tree import primary as _prim, REMOVED as _REM
_mk = dict(q('SELECT old_id, kept_id FROM merged_entities')); _rp = collections.defaultdict(set); _ra = set()
for r in _csv.DictReader(open(os.path.join(HERE, 'regression.tsv'), encoding='utf-8'), delimiter='\t'):
    e = _mk.get(int(r['entity']), int(r['entity']))
    if r['expect'] == 'present': _rp[e] |= set(_prim(r['concept']))
    elif r['concept'] not in _REM: _ra.add((e, _prim(r['concept'])[0]))
import patterns3 as _P
_pats = collections.defaultdict(list)
for k, p_, g in q('SELECT concept, pattern, game FROM concept_patterns'):
    try: _pats[k].append((g, re.compile(p_, re.I)))
    except re.error: pass
_ent = {i: (g, n, t) for i, g, n, t in q("SELECT id, game, name, text FROM entities WHERE category='keyword'")}
kw_removed = 0
for kid, (ks, notreal) in read.items():
    if kid not in kws: continue
    g_, n_, t_ = _ent[kid]; low = _P.norm_text(g_, n_, t_)
    for k, in q("SELECT concept FROM entity_concepts WHERE entity=? AND role='does' AND method!='game_structure'", kid):
        if k in ks or k in _rp[kid]: continue
        if any(gg in (None, g_) and rx.search(low) for gg, rx in _pats.get(k, ())): continue   # the keyword's own text justifies it
        kw_removed += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND role='does'", (kid, k)).rowcount
    for k in ks:
        if (kid, k) not in _ra: c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (kid, k, 'does', 'claude_review', 'keyword read twice (step 4)'))
    for k, in q('SELECT concept FROM entity_concepts WHERE entity=?', kid):
        if (kid, k) in _ra: c.execute('DELETE FROM entity_concepts WHERE entity=? AND concept=?', (kid, k))
    if notreal:
        c.execute("UPDATE OR IGNORE entity_links SET rel='mentions_keyword' WHERE dst=? AND rel IN ('has_keyword','grants_keyword')", (kid,))
        c.execute("DELETE FROM entity_links WHERE dst=? AND rel IN ('has_keyword','grants_keyword')", (kid,))
# 3. inheritance
kwtags = collections.defaultdict(set)
for e, k, r in q("SELECT entity, concept, role FROM entity_concepts WHERE entity IN (SELECT id FROM entities WHERE category='keyword')"):
    kwtags[e].add((k, r))
want = collections.defaultdict(set)
for s, rel, d in q("SELECT src, rel, dst FROM entity_links WHERE rel IN ('has_keyword','grants_keyword')"):
    for k, r in kwtags.get(d, ()): want[s].add((k, r if rel == 'has_keyword' else 'grants'))
import patterns3 as P
pats = collections.defaultdict(list)
for k, p, g in q('SELECT concept, pattern, game FROM concept_patterns'):
    try: pats[k].append((g, re.compile(p, re.I)))
    except re.error: pass
known = collections.defaultdict(set)
for g, kk in P.keys().items():
    for e, ks in kk.items(): known[e] |= ks | {a for x in ks for a in P.K.ANC[x]}
if os.path.exists(os.path.join(HERE, 'step3', 'questions.json')):
    Qs, ans, _, _ = P.answers()
    for qid, (e, k, dd) in Qs['q'].items():
        if ans.get(qid) is True: known[e].add(k)
# hand reviews (regression.tsv) are known too: a reviewed tag is kept, a reviewed drop is never added back
import csv
from concept_tree import primary, REMOVED
mk = dict(q('SELECT old_id, kept_id FROM merged_entities'))
rev_absent = set()
for r in csv.DictReader(open(os.path.join(HERE, 'regression.tsv'), encoding='utf-8'), delimiter='\t'):
    e = mk.get(int(r['entity']), int(r['entity']))
    if r['expect'] == 'present': known[e] |= set(primary(r['concept']))
    elif r['concept'] not in REMOVED: rev_absent.add((e, primary(r['concept'])[0]))
ent = {i: (g, n, t) for i, g, n, t in q('SELECT id, game, name, text FROM entities')}
removed = kept = added = 0
have = collections.defaultdict(set)
for e, k, r in q("SELECT entity, concept, role FROM entity_concepts WHERE method='via_keyword'"): have[e].add((k, r))
egame = dict(q('SELECT id, game FROM entities'))
for e in set(have) | set(want):
    if ALLOW is not None and egame.get(e) not in ALLOW: continue
    for k, r in have[e] - want[e]:
        g, n, t = ent.get(e, ('', '', ''))
        low = P.norm_text(g, n, t)
        if k in known[e] or any(gg in (None, g) and rx.search(low) for gg, rx in pats.get(k, ())):
            c.execute("UPDATE entity_concepts SET method='text_pattern', evidence='kept: own text, step 4' WHERE entity=? AND concept=? AND role=?", (e, k, r)); kept += 1
        else:
            removed += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND role=? AND method='via_keyword'", (e, k, r)).rowcount
    for k, r in want[e] - have[e]:
        if (e, k) in rev_absent: continue
        added += c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, k, r, 'via_keyword', 'inherited from a keyword read twice (step 4)')).rowcount
c.commit()
print('keyword links: has_keyword links turned into mentions', len(drop), '; keyword entries read', len(read), ', their old tags removed', kw_removed,
      '; inherited tags removed', removed, ', kept as own text', kept, ', added', added)
