"""Trigger wording that no trigger pattern covered (found by step3/trigger_gaps.py, 19 Oct 2026; script only, no readers).
CANDIDATES are Claude's regexes: some for existing trigger concepts, some for the new trigger concepts added to the tree the same day
(listed in key/added_concepts.txt; the answer key has no tags for them, so the scorers leave them out).
  trigger_patterns.py check [db]   per pattern and game: matches, key matches, key right (existing concepts), and 20 random
                                   matches (seed 1) as short snippets for Claude to judge
  trigger_patterns.py write [db]   writes 'new' lines into decisions.tsv for every pattern and game it matches in, except
                                   pairs in DROP (key below 90% right with 3+ key matches, or judged wrong on the snippets)"""
import collections, os, random, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, TOOLS)
import patterns3 as P
K = P.K
U = r"(?:a|an|this|that|the|one|another|any|each|a friendly|an enemy)\s+(?:model|unit|operative|fighter|creature|minion|follower|character)"
CANDIDATES = [
    ('on_attack', 'trigger', r"\beach time " + U + r"\b[^.,:\n]{0,40}?\b(?:makes? an? (?:melee |ranged |shooting )?attack|fights?|shoots?|is selected to (?:fight|shoot))"),
    ('on_attack', 'trigger', r"\bafter (?:this|that) (?:model|unit|operative|fighter) has (?:shot|fought)\b"),
    ('on_attack', 'trigger', r"\bwhenever (?:you attack|this creature attacks|name attacks)\b"),
    ('turn_start', 'trigger', r"\bat the (?:start|beginning) of (?:the |your |each |its |their |the owner's |its owner's |the opponent's |each player's )?(?:next )?(?:turn|round|battle round|upkeep)\b"),
    ('turn_end', 'trigger', r"\bat the end of (?:the |your |each |its |their |the owner's |its owner's |the opponent's |each player's )?(?:next )?(?:turn|round|battle round)\b"),
    ('on_spell', 'trigger', r"\bwhenever (?:you|a player|an opponent) casts? (?:[\w-]+ ){0,5}?(?:spells?|instants?|sorcer(?:y|ies))\b"),
    ('on_ally_play', 'trigger', r"\bwhenever (?:one or more )?(?:another |other )?(?:creatures?|artifacts?|permanents?|tokens?)\b[^.,:\n]{0,30}?\byou control enters?\b"),
    ('on_ally_play', 'trigger', r"\bwhen(?:ever)? you play an?\b"),
    ('on_damaged', 'trigger', r"\beach time an? (?:ranged |melee |shooting )?attack (?:is made against|targets) (?:this|that)\b"),
    ('on_enemy_enter', 'trigger', r"\beach time an enemy (?:unit|operative|model)\b[^.,:\n]{0,40}?\bends? an? (?:normal|advance|fall back|charge|reposition|dash) move\b"),
    ('on_draw', 'trigger', r"\bwhen(?:ever)? (?:you|a player|the player|each player|that player|an opponent|your opponent|each opponent|target player|your hero|they) draws?\b"),
    ('on_discard', 'trigger', r"\bwhen(?:ever)? (?:you|a player|the player|each player|that player|an opponent|your opponent|each opponent|target player|your hero|they) discards?\b|\bwhen(?:ever)? (?:this|name|this card|a card) is discarded\b"),
    ('on_lifegain', 'trigger', r"\bwhen(?:ever)? (?:you|a player|the player|each player|that player|an opponent|your opponent|each opponent|target player|your hero|they) gains? (?:\d+ |that much |\w+ )?life\b|\bwhen(?:ever)? (?:your hero|you) (?:is|are) healed\b"),
    ('on_block', 'trigger', r"\bwhen(?:ever)? (?:this creature|name) blocks\b|\bwhen(?:ever)? (?:this creature|name) becomes blocked\b"),
    ('on_targeted', 'trigger', r"\bwhen(?:ever)? (?:this (?:creature|permanent|unit|minion)|name) becomes the target of\b"),
    ('on_sacrifice', 'trigger', r"\bwhen(?:ever)? (?:you|a player|the player|each player|that player|an opponent|your opponent|each opponent|target player|your hero|they) sacrifices?\b"),
]
DROP = set()   # (pattern index, game) pairs Claude judged wrong; filled after 'check'
DB = sys.argv[2] if len(sys.argv) > 2 else P.DB
c = sqlite3.connect(DB)
ents = collections.defaultdict(list)
for i, g, n, t in c.execute('SELECT id, game, name, text FROM entities WHERE text IS NOT NULL'): ents[g].append((i, n, P.norm_text(g, n, t)))
ky = P.keys()
mode = sys.argv[1]
out = []
for j, (k, role, p) in enumerate(CANDIDATES):
    r = re.compile(p, re.I); hits = []
    for g, es in ents.items():
        if g == 'marvel_snap' and False: continue
        m = [(i, n, t) for i, n, t in es if r.search(t)]
        if not m: continue
        kn = [i for i, _, _ in m if i in ky.get(g, {})]
        kr = sum(P.right(k, ky[g][i]) for i in kn) if k in K.TREE and k not in K.NOT_IN_KEY else None
        bad = kr is not None and len(kn) >= 3 and kr < 0.9 * len(kn)
        if mode == 'check': print(f'{j:2} {k:14} {g:18} matches {len(m):5} key {len(kn):3} right {kr}{"  WEAK" if bad else ""}')
        hits += [(g, n, t, r.search(t)) for i, n, t in m]
        if mode == 'write' and not bad and (j, g) not in DROP: out.append(f'new\t{k}|{role}|{g}|trigger\t{g}\t{p}')
    if mode == 'check':
        for g, n, t, mm in random.Random(1).sample(hits, min(20, len(hits))):
            print(f'     {g[:10]:10} {n[:24]:24} …{t[max(0, mm.start() - 25): mm.end() + 35]}…'.replace('\n', ' / '))
if mode == 'write':
    D = os.path.join(HERE, 'decisions.tsv')
    keep = [l for l in open(D, encoding='utf-8') if not (l.startswith('new\t') and l.split('\t')[1].endswith('|trigger')) and not l.startswith('# trigger_patterns')]
    keep.append('# trigger_patterns.py: trigger wording no trigger pattern covered (Claude\'s regexes, checked on the key and on samples)\n')
    open(D, 'w', encoding='utf-8').writelines(keep + [l + '\n' for l in out])
    print('trigger pattern lines', len(out))
