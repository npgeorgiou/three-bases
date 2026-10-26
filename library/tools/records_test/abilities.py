"""Step 2 of the test: each card's abilities, made from its tags.
- Tags a card has from a keyword (method via_keyword) form that keyword's ability. Cost and structure tags form the card ability.
- A card with no trigger tag: one static ability with all its tags. One trigger: one ability, that trigger with all the tags.
- Two or more triggers: one ability per trigger group, triggers next to each other with no effect between them sharing one
  ("Battlecry and Deathrattle: ..."). Each other tag goes to the nearest trigger group before its words (position rule); words
  before every trigger go to the first group when no sentence end lies between, else to a static ability. A tag whose words
  are unknown goes where this game's one-trigger cards say it belongs (the trigger seen most often with it: statistics rule),
  else to the card ability. Test per game: on tags with known words, how often both rules agree.
Tables: abilities(id, entity, ord, kind, triggers), ability_tags(rid, ability, how, stats_agree), records_pairs.
Usage: abilities.py <copy.sqlite>"""
import collections, re, sys
import common as C

NOT_TRIGGER = {'trigger', 'passive', 'aura'}
STRUCT = {'data_rule', 'game_structure'}

def main(path):
    c = C.connect(path); eff, _ = C.concept_kinds(c)
    trig = {i for (i,) in c.execute("SELECT id FROM concept_tree WHERE root='trigger'")} - NOT_TRIGGER
    c.executescript('DROP TABLE IF EXISTS rows; DROP TABLE IF EXISTS row_tags; DROP TABLE IF EXISTS records_compound;'
                    'DROP TABLE IF EXISTS abilities; CREATE TABLE abilities(id INTEGER PRIMARY KEY, entity INT, ord INT, kind TEXT, triggers TEXT);'
                    'DROP TABLE IF EXISTS ability_tags; CREATE TABLE ability_tags(rid INT PRIMARY KEY, ability INT, how TEXT, stats_agree INT);'
                    'DROP TABLE IF EXISTS records_pairs; CREATE TABLE records_pairs(entity INT, ability INT, trigger TEXT, effect TEXT);')
    ent = {i: (g, t or '') for i, g, t in c.execute("SELECT id, game, text FROM entities")}
    kwcon = collections.defaultdict(set)
    for e, k in c.execute("SELECT ec.entity, ec.concept FROM entity_concepts ec JOIN entities x ON x.id=ec.entity WHERE x.category='keyword'"): kwcon[e].add(k)
    haskw = collections.defaultdict(list)
    kwname = {}
    for s, d, n in c.execute("SELECT l.src, l.dst, k.name FROM entity_links l JOIN entities k ON k.id=l.dst WHERE l.rel='has_keyword' AND k.category='keyword'"):
        haskw[s].append(d); kwname[d] = re.sub(r'\([^)]*\)', '', (n or '').lower()).strip()
    tags = collections.defaultdict(list); words = {}
    for rid, e, k, meth, pos, ln in c.execute('SELECT ec.rowid, ec.entity, ec.concept, ec.method, w.pos, w.len FROM entity_concepts ec JOIN tag_words w ON w.rid=ec.rowid '
                                          "JOIN entities x ON x.id=ec.entity WHERE x.category NOT IN ('keyword','tribe')"):
        tags[e].append((rid, k, meth, pos)); words[rid] = re.sub(r'[\s\dX+]+$', '', (ent[e][1][pos:pos + ln] if pos is not None else '').lower().strip(' .,:'))
    def own_kw(e, pos, ln):
        """words at pos start a keyword the card has: only keyword names before them in the sentence, not a trigger prefix ("Battlecry:")"""
        if pos is None: return False
        text = ent[e][1]; start = max(text.rfind(ch, 0, pos) for ch in '.!?;\n') + 1
        before = re.sub(r'\([^)]*\)', ' ', text[start:pos]).lower().strip(' ,'); names = sorted({kwname[d] for d in haskw.get(e, [])}, key=len, reverse=True)
        while before:
            n = next((n for n in names if n and before.startswith(n)), None)
            if not n: return False
            before = re.sub(r'^[\s\dx+,]+', '', before[len(n):])
        after = text[pos + ln:pos + ln + 40]
        return not re.match(r"(?:\s*[\dX+]*\s*|\s+(?:and|or)\s+[A-Z][\w ]{0,20}?)[:\-–—]\s", after)
    def split(lst):
        kwa, card, rest = collections.defaultdict(list), [], []
        for t in lst:
            rid, k, meth, pos = t
            if meth in STRUCT: card.append(t); continue
            d = next((d for d in haskw.get(e_of[rid], []) if words.get(rid) and words[rid] == kwname.get(d)), None) if own_kw(e_of[rid], pos, len(words.get(rid) or '')) else None   # its words name a keyword the card has, in its keyword list
            if d is not None: kwa[d].append(t); continue
            if meth == 'via_keyword':
                d = next((d for d in haskw.get(e_of[rid], []) if k in kwcon[d]), None)
                if d is not None: kwa[d].append(t); continue
            rest.append(t)
        return kwa, card, rest
    e_of = {rid: e for e, lst in tags.items() for rid, *_ in lst}
    # the statistics rule, learned per game from the one-trigger cards: how often each trigger comes with each other tag
    stats = collections.defaultdict(collections.Counter)
    for e, lst in tags.items():
        _, _, rest = split(lst); ts = {k for _, k, _, _ in rest if k in trig}
        if len(ts) == 1:
            t = next(iter(ts))
            for _, k, _, _ in rest:
                if k not in trig: stats[ent[e][0]][(t, k)] += 1
    A, AT, PR = [], [], []
    nid = [0]
    def ability(e, o, kind, ts):
        nid[0] += 1; A.append((nid[0], e, o, kind, ','.join(sorted(ts)))); return nid[0]
    for e, lst in tags.items():
        g, text = ent[e]; kwa, card, rest = split(lst); order = 0
        for d, ts in kwa.items():
            a = ability(e, -2, 'keyword', {k for _, k, _, _ in ts if k in trig})
            for rid, *_ in ts: AT.append((rid, a, 'keyword', None))
        trig_tags = [t for t in rest if t[1] in trig]; other = [t for t in rest if t[1] not in trig]
        distinct = {t[1] for t in trig_tags}
        groups = []   # (triggers, start position, ability id)
        if len(distinct) <= 1:
            a = ability(e, 0, 'trigger' if distinct else 'static', distinct); groups.append((distinct, None, a))
            for rid, *_ in rest: AT.append((rid, a, 'one trigger' if distinct else 'no trigger', None))
        else:
            known = sorted((t for t in trig_tags if t[3] is not None), key=lambda t: t[3]); placed = {}
            tag_pos = sorted(t[3] for t in other if t[3] is not None)
            cur = None
            for t in known:   # triggers with no effect between them share a group
                if cur and t[1] in cur[0]: placed[t[0]] = cur; continue
                if cur and not any(cur[2] < p < t[3] for p in tag_pos) and not re.search(r'[.!?;\n]', text[cur[2]:t[3]]):   # "Battlecry and Deathrattle:"
                    cur[0].add(t[1]); cur[2] = t[3]; placed[t[0]] = cur; continue
                cur = [{t[1]}, t[3], t[3]]; groups.append(cur); placed[t[0]] = cur
            for t in trig_tags:   # a trigger with no words: its own group at the end
                if t[0] not in placed:
                    hit = next((gr for gr in groups if t[1] in gr[0]), None)
                    if hit is None: hit = [{t[1]}, None, None]; groups.append(hit)
                    placed[t[0]] = hit
            for gr in groups: order += 1; gr.append(ability(e, order, 'trigger', gr[0]))
            static = None
            for t in trig_tags: AT.append((t[0], placed[t[0]][-1], 'trigger', None))
            def by_stats(k):
                cnt = stats[g]; best = max(groups, key=lambda gr: sum(cnt[(x, k)] for x in gr[0]))
                return best if sum(cnt[(x, k)] for x in best[0]) > 0 else None
            for rid, k, meth, pos in other:
                sg = by_stats(k)
                if pos is not None and any(gr[1] is not None for gr in groups):
                    before = [gr for gr in groups if gr[1] is not None and gr[1] <= pos]
                    if before: gr = max(before, key=lambda x: x[1]); how = 'position'
                    else:
                        first = min((gr for gr in groups if gr[1] is not None), key=lambda x: x[1])
                        if not re.search(r'[.!?;\n]', text[pos:first[1]]): gr = first; how = 'position (trigger after)'
                        else:
                            if static is None: order += 1; static = [set(), None, None, ability(e, order, 'static', set())]
                            gr = static; how = 'position (before every trigger)'
                    AT.append((rid, gr[-1], how, None if sg is None else int(sg is gr)))
                elif sg is not None: AT.append((rid, sg[-1], 'statistics', None))
                else:
                    if not card: card = []
                    card.append((rid, k, meth, pos))
        if card:
            a = ability(e, -1, 'card', set())
            for t in card: AT.append((t[0], a, 'card', None))
    by_ab = collections.defaultdict(set); ent_of = {x[0]: x[1] for x in A}
    rid_k = {rid: k for lst in tags.values() for rid, k, _, _ in lst}
    for rid, a, _, _ in AT: by_ab[a].add(rid_k[rid])
    trig_any = trig | NOT_TRIGGER
    for a, ks in by_ab.items():
        for t in ks & trig:
            for f in (ks & eff) - trig_any: PR.append((ent_of[a], a, t, f))
    c.executemany('INSERT INTO abilities VALUES(?,?,?,?,?)', A); c.executemany('INSERT OR REPLACE INTO ability_tags VALUES(?,?,?,?)', AT)
    c.executemany('INSERT INTO records_pairs VALUES(?,?,?,?)', PR); c.commit()
    print('abilities', len(A), 'tags', len(AT), collections.Counter(h for _, _, h, _ in AT), 'pairs', len({(a, b, d) for a, _, b, d in PR}))

if __name__ == '__main__': main(sys.argv[1])
