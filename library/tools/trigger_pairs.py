"""Rebuild the trigger -> effect table for every game. Every clause of every entry is read: its triggers
(general and per-game trigger patterns plus the trigger words below) and its effects (general and per-game effect patterns) are
paired. Entries inherit the pairs of the keywords they have. Existing rows are kept (Marvel Snap's own loader); new pairs are added.
Coverage check: per game, the share of entries with a trigger tag that have at least one pair; `check` fails below 50%.
Usage: trigger_pairs.py <db> [check | pairs_only]  (pairs_only: after the tree move, pairs the entry's existing tags and adds no tag)"""
import os, re, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refast import Fast
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
EXTRA = {   # trigger wording the general patterns miss (Claude's list, from the misses)
 'on_attack': [r"\b(whenever|when|each time) (this|it|~|this (creature|unit|minion|follower|model|operative|vehicle)|enchanted creature|equipped creature|(a|another|one or more) (\w+ )?creatures? you control)\b[^.,:]{0,20}\bdeals? combat damage to (a player|an opponent|one or more players|a creature)\b", r"\b(the first time|whenever|when|each time|after) (i|this|it|~|he|she|they|this (unit|creature|minion|follower|model|operative))\b[^.,:]{0,15}\battacks?\b", r"\b(nexus )?strike:", r"\bclash:", r"\battack:", r"\brally:"],
 'on_play': [r"\b(gift|deploy|fanfare|battlecry)\s*[-–:]", r"\bwhen i'?m (summoned|played)\b", r"\bwhen you (play|cast) (this|me|~)\b", r"\bon reveal:", r"\bdeploy:", r"\bfanfare:", r"\bopening gambit", r"\bplay:", r"\bgift:", r"\bbattlecry:", r"\bwhen (this|~) (creature|permanent|minion|unit) enters\b"],
 'death_trigger': [r"\blast words\s*[-–]", r"\blast breath:", r"\bwhen i die\b", r"\bwhen (this|it|~) (dies|is destroyed|perishes)\b", r"\bdying wish:", r"\bdeathwish:", r"\blast words:", r"\bwhen destroyed:", r"\bdeathrattle:"],
 'death_count': [r"\b(when|whenever|each time|after) (an?|another|any|one or more|a friendly|an allied|an enemy|your)\b[^.,:]{0,35}\b(dies|die|is destroyed|are destroyed|perishes|is slain|are slain)\b"],
 'turn_start': [r"\bproduction\s*[-–]", r"\bround start:", r"\bat the (start|beginning) of (each|your|the|every)\b(?! (?:\w+ )?(?:runs?|phases?|fights?|battles?|games?|encounters?|matches?|acts?)\b)", r"\bstart of turn:", r"\bproduction:"],
 'turn_end': [r"\bround end:", r"\bat the end of (each|your|the|every)\b(?! (?:\w+ )?(?:runs?|phases?|fights?|battles?|games?|encounters?|matches?|acts?)\b)", r"\bend of turn:"],
 'on_ally_play': [r"\bwhen(ever)? you (play|summon) (an?|another)\b(?! spell)", r"\bwhen(ever)? (an?|another) (ally|allied|friendly)[^.,:]{0,20}(is summoned|is played|enters)\b"],
 'on_spell': [r"\bwhen(ever)? you (cast|play) (an?|another)? ?[^.,:]{0,12}(spell|skill)\b", r"\bspellburst\b", r"\bmagecraft\b", r"\bprowess\b"],
 'on_damaged': [r"\bwhen(ever)? (i|this|it|~)\b[^.,:]{0,15}\b(takes|survives) damage\b", r"\benrage\b", r"\bwhen i'?m damaged\b"],
 'on_kill': [r"\bwhen(ever)? (i|this|it|~)\b[^.,:]{0,10}\b(kills?|slays?)\b", r"\bslay:", r"\bdeathblow\b", r"\boverkill\b"],
}
if len(sys.argv) < 3 or sys.argv[2] != 'check':
    root = dict(q("SELECT id, root FROM concept_tree WHERE root IN ('trigger','effect') ORDER BY root DESC"))   # a concept under both (death_count) reads its patterns as effects; its trigger wording is in EXTRA
    pats = {}
    for con, p, g in q("SELECT concept, pattern, game FROM concept_patterns WHERE role='does'"):
        if root.get(con) in ('trigger', 'effect'):
            try: pats.setdefault(g, []).append((con, root[con], re.compile(p, re.I)))
            except re.error: pass
    for con, ps in EXTRA.items():
        for p in ps: pats.setdefault(None, []).append((con, 'trigger', re.compile(p, re.I)))
    if sys.argv[2:] == ['pairs_only']:   # the death and leave-play triggers split by whose (death_side.py): which clause holds them, for pairing only
        import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import death_side as DS
        for con in ('death_trigger', 'other_death_trigger', 'leave_trigger', 'other_leave_trigger'):
            root.setdefault(con, 'trigger')
        pats.setdefault(None, []).extend([('death_trigger', 'trigger', DS.OWN_KW), ('other_death_trigger', 'trigger', re.compile(r"\b" + DS.DIE + r"\b", re.I)),
                                          ('leave_trigger', 'trigger', re.compile(DS.LEAVE, re.I)), ('other_leave_trigger', 'trigger', re.compile(DS.LEAVE, re.I))])
    import os
    excl = {}   # a pattern file's '!concept|pattern' lines (game_patterns.py): that pattern adds no tag of the concept here either
    pd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patterns')
    for f in os.listdir(pd):
        if f.endswith('.txt'):
            excl[f[:-4]] = {tuple(l[1:].rstrip('\n').split('|', 1)) for l in open(os.path.join(pd, f), encoding='utf-8') if l.startswith('!')}
    have = {(e, t, f) for e, t, f in q('SELECT entity, trigger, effect FROM trigger_effect')}
    ONLY = sys.argv[2:] == ['pairs_only']
    tags = {}
    if ONLY:
        for e, k in q('SELECT entity, concept FROM entity_concepts'): tags.setdefault(e, set()).add(k)
    SPLIT = re.compile(r'(?<=[.!;])\s+|\n+')
    n = 0
    # whole-entry triggers that are not in the wording (monster intents, structure rules, reviewed tags): used when no clause names a trigger
    whole = {}
    for e, k in q("SELECT entity, concept FROM entity_concepts WHERE role='does' AND method IN ('game_structure','data_rule','claude_review','via_keyword','claude_inference')"):
        if root.get(k) == 'trigger' and k not in ('passive', 'aura', 'trigger'): whole.setdefault(e, set()).add(k)
    LISTS = {}   # per game, once: the trigger and effect patterns, and the whole-entry ones ("(?s)^(?!...") apart, since they are checked on the entry's text
    def lists(g):
        if g not in LISTS:
            P = pats.get(None, []) + pats.get(g, [])
            X = excl.get(g, set()) | (excl.get('_all', set()) if g != 'marvel_snap' else set())
            if X: P = [x for x in P if (x[0], x[2].pattern) not in X]
            whole = lambda x: x[2].pattern.startswith('(?s)^(?!')
            LISTS[g] = tuple([(x[0], Fast(x[2])) for x in P if x[1] == r and whole(x) == w] for r in ('trigger', 'effect') for w in (False, True))
        return LISTS[g]
    for e, g, t in q("SELECT id, game, text FROM entities WHERE text IS NOT NULL AND category NOT IN ('tribe') AND length(text) < 6000"):
        tl = t.lower()   # a whole-entry pattern is checked on the whole text, not per clause
        trN, trW, efN, efW = lists(g)
        TR = [x for x in trN if x[1].maybe(tl)] + [x for x in trW if x[1].search(tl)]   # only the patterns whose literal the entry holds can match a clause
        EF = [x for x in efN if x[1].maybe(tl)] + [x for x in efW if x[1].search(tl)]
        efm = {}
        def effects(low):   # the effect concepts of one clause, found once
            if low not in efm: efm[low] = {con for con, p in EF if p.search(low)}
            return efm[low]
        found = False
        cls = [x.lower().strip() for x in SPLIT.split(t)]
        for j, low in enumerate(cls):
            cl = low
            if not low: continue
            tr = {con for con, p in TR if p.search(low)}
            if ONLY: tr &= tags.get(e, set())   # after the tree move: pair only the tags the entry has, add none
            if not tr: continue
            found = True
            if not ONLY:
                for a in tr: c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, a, 'does', 'text_pattern', low[:60]))   # the entry gets the trigger tag too
            ef = set(effects(low))
            if not ef:   # "At the start of each turn, repeat this." — the effect is in the clause before or after
                for nb in (cls[j - 1] if j else '', cls[j + 1] if j + 1 < len(cls) else ''):
                    ef |= effects(nb)
            if ONLY: ef &= tags.get(e, set())
            for a in tr:
                for b in ef:
                    if (e, a, b) in have: continue
                    have.add((e, a, b)); n += 1
                    c.execute("INSERT INTO trigger_effect(entity, game, trigger, effect, clause) VALUES(?,?,?,?,?)", (e, g, a, b, cl.strip()[:300]))
        if not found and e in whole:
            for cl in SPLIT.split(t):
                low = cl.lower().strip()
                ef = effects(low)
                for a in whole[e]:
                    for b in ef:
                        if (e, a, b) in have: continue
                        have.add((e, a, b)); n += 1
                        c.execute("INSERT INTO trigger_effect(entity, game, trigger, effect, clause) VALUES(?,?,?,?,?)", (e, g, a, b, cl.strip()[:300]))
    # an entry that has a keyword also has that keyword's trigger -> effect pairs (Inscryption sigils...)
    k = 0
    kwp = {}
    for e, t, f, cl in q("SELECT t.entity, t.trigger, t.effect, t.clause FROM trigger_effect t JOIN entities x ON x.id=t.entity WHERE x.category='keyword'"): kwp.setdefault(e, []).append((t, f, cl))
    for src, dst, g, kn in q("SELECT l.src, l.dst, x.game, k.name FROM entity_links l JOIN entities x ON x.id=l.src JOIN entities k ON k.id=l.dst WHERE l.rel IN ('has_keyword','grants_keyword') AND k.category='keyword'"):
        for t, f, cl in kwp.get(dst, []):
            if (src, t, f) in have: continue
            have.add((src, t, f)); k += 1
            c.execute("INSERT INTO trigger_effect(entity, game, trigger, effect, clause) VALUES(?,?,?,?,?)", (src, g, t, f, f'via keyword {kn}: {cl}'[:300]))
    c.commit(); print('trigger pairs added:', n, ' inherited from keywords:', k)
trig = {i for (i,) in q("SELECT id FROM concept_tree WHERE root='trigger'")} - {'passive', 'aura', 'trigger'}
bad = []
for g, in q('SELECT DISTINCT game FROM entities'):
    tagged = {e for (e, k) in q("SELECT ec.entity, ec.concept FROM entity_concepts ec JOIN entities x ON x.id=ec.entity WHERE x.game=? AND ec.role='does' AND x.category NOT IN ('keyword','tribe')", g) if k in trig}
    paired = {e for (e,) in q('SELECT DISTINCT entity FROM trigger_effect WHERE game=?', g)}
    if len(tagged) >= 50:
        share = len(tagged & paired) / len(tagged)
        if share < 0.5: bad.append(f'{g} {share:.0%}')
print('trigger coverage below 50%:', bad or 'none')
if sys.argv[2:] == ['check'] and bad: sys.exit(1)
