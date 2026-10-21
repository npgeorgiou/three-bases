"""The answer key wins over the review files (Kaptain's decision, 19 Oct 2026; script only, no readers).
Only on key entries, only the concept in conflict, and never a 'benefits' or 'counters' line (the readers tagged what a card
does, not what it pays off or answers: Brann Bronzebeard benefits from battlecries without doing one): the entry's other tags stay (the key may not have explored them).
  - a review tag the key calls wrong (neither a key concept nor a broader or narrower one): the tag is removed;
  - a review tag that is a broader or narrower form of a key concept (not the key concept itself): the review's concept is removed
    and the key's related concepts are added;
  - a review drop of a concept the key has: the key's concept is added.
  key_wins.py make          -> tools/key/key_wins.tsv (entity, concept, action add|drop, why) and removes the conflicting lines from
                               tools/regression.tsv (so no step treats the review's version as known right any more); regression.py
                               make leaves out the lines listed in key_wins.tsv
  key_wins.py apply <db>    build step after final_revert.py: applies key_wins.tsv (adds use method 'answer_key')"""
import collections, csv, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'key'))
OUT = os.path.join(HERE, 'key', 'key_wins.tsv'); REG = os.path.join(HERE, 'regression.tsv')
mode = sys.argv[1]
if mode == 'make':
    import key as K
    from concept_tree import primary, REMOVED
    c = sqlite3.connect(os.path.join(os.path.dirname(HERE), 'three-bases-library.sqlite'))
    mk = dict(c.execute('SELECT old_id, kept_id FROM merged_entities'))
    keys = {int(i): K.narrow({k for k, _ in v['tags']}) for g in K.GAMES for i, v in K.load(g).items()}
    rows = list(csv.DictReader(open(REG, encoding='utf-8'), delimiter='\t')); fields = list(rows[0].keys())
    acts = set(); keep = []; n = collections.Counter()
    for r in rows:
        e = mk.get(int(r['entity']), int(r['entity']))
        if e not in keys: keep.append(r); continue
        ks = keys[e]
        if r['role'] in ('benefits', 'counters'): keep.append(r); continue   # a payoff or an answer: the key reads what a card does, not what it rewards
        if r['expect'] == 'present':   # a removed old concept is checked as any of its new ids (as regression.py does)
            pk = [r['concept']]
            if any(k in ks or k in K.GROUPS for k in pk): keep.append(r); continue
            rel = {x for x in ks for k in pk if k in K.ANC[x] or k in K.DESC[x]}
            for k in pk: acts.add((e, k, 'drop', 'review concept broader or narrower than the key\'s' if rel else 'review tag the key calls wrong'))
            for x in rel: acts.add((e, x, 'add', 'key concept'))
            n['nested' if rel else 'review adds, key lacks'] += 1
            continue
        k = r['concept']
        if True:
            if k in ks:
                acts.add((e, k, 'add', 'review dropped a key concept')); n['review drops, key has'] += 1
            else: keep.append(r)
    with open(REG, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(keep)
    adds = {(e, k) for e, k, a, _ in acts if a == 'add'}
    acts = {x for x in acts if not (x[2] == 'drop' and (x[0], x[1]) in adds)}   # a key concept is never dropped
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write('entity\tconcept\taction\twhy\n')
        for e, k, a, why in sorted(acts): fh.write(f'{e}\t{k}\t{a}\t{why}\n')
    print('regression lines removed', len(rows) - len(keep), dict(n), 'actions', len(acts))
else:
    c = sqlite3.connect(sys.argv[2])
    if not os.path.exists(OUT): print('key wins: none'); sys.exit(0)
    role = {}
    for k, r, n in c.execute('SELECT concept, role, count(*) FROM concept_patterns GROUP BY 1, 2 ORDER BY 3'): role[k] = r
    live = {i for i, in c.execute('SELECT id FROM entities')}
    import key as K   # the key as it is now (key/key.py load: the readers' key with the keyword credit)
    keyed = {}
    for (g,) in c.execute('SELECT id FROM games'):
        try: keyed.update({int(i): {t[0] for t in v['tags']} for i, v in K.load(g).items()})
        except FileNotFoundError: pass
    add = drop = 0
    for r in csv.DictReader(open(OUT, encoding='utf-8'), delimiter='\t'):
        e, k = int(r['entity']), r['concept']
        if e not in live: continue
        if r['action'] == 'drop' and k in keyed.get(e, ()): continue   # the key was corrected since the line was made: it has the concept now
        if r['action'] == 'drop':
            drop += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND role NOT IN ('benefits', 'counters')", (e, k)).rowcount   # payoff and answer tags stay
            c.execute('DELETE FROM trigger_effect WHERE entity=? AND (trigger=? OR effect=?)', (e, k, k))
        elif not c.execute('SELECT 1 FROM entity_concepts WHERE entity=? AND concept=?', (e, k)).fetchone():
            add += c.execute('INSERT INTO entity_concepts VALUES(?,?,?,?,?)', (e, k, role.get(k, 'does'), 'answer_key', 'key wins over review (19 Oct 2026)')).rowcount
    c.commit(); print('key wins: tags removed', drop, 'added', add)
