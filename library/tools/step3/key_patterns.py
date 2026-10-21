"""Step 3b of the tag-fix plan (19 Oct 2026): new wording patterns built from the answer key's quoted words.
For each game, the key (tools/key/<game>/key.json) is split 50/50 with seed 1. Every quoted phrase of one half becomes a candidate regex
for its concept: read as the patterns read text (lower case, the entry's own name as 'name', Magic without reminder text), escaped,
spaces as \\s+, numbers as \\d+, word boundaries at word ends. A candidate is tested on the other half (the entries it was not built
from) and kept only if it matches there at least MIN times and is 90%+ right (right as key.py scores: the key's concepts, a narrower or
a broader one below the four branches). Both directions are run; the kept candidates of a game and concept are joined into one regex.
Claude's choices (not in the plan): numbers as \\d+, a phrase must be at least 4 characters and not only the name, MIN = 3 held-out
matches, never a candidate that matches an entry a hand review dropped the concept from (regression.tsv 'absent'), and the role is the concept's most common role among the existing patterns ('does' when it has none).
Two more checks (21 Oct 2026): a phrase that is only one of the game's keyword names matches only where the game prints keywords
(the position rule of kw_links.py, so "with Prophecy" or "the Consume pile" do not tag), and a candidate is kept only if it is also
90%+ right on the whole key (ADDING_GAMES.md 4b.6), not only on the held-out half.
Writes the 'new' lines of tools/step3/decisions.tsv (narrow lines are kept as they are) and prints counts only.
Only the games named are rewritten; every other game's lines stay as they are, so a game changes only when it is worked on and
measured (compare_builds.py).
Usage: key_patterns.py <db> <game> [<game> ...]"""
import collections, json, os, random, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, TOOLS)
import patterns3 as P
K = P.K
if len(sys.argv) < 3: sys.exit('usage: key_patterns.py <db> <game> [<game> ...]')
DB, ONLY = sys.argv[1], set(sys.argv[2:])
assert ONLY <= set(P.GAMES), ONLY - set(P.GAMES)
MIN, PREC = 3, 0.9
c = sqlite3.connect(DB)
roles = collections.defaultdict(collections.Counter)
for k, r in c.execute('SELECT concept, role FROM concept_patterns'): roles[k][r] += 1
role = lambda k: roles[k].most_common(1)[0][0] if roles[k] else 'does'
import csv
from concept_tree import primary, REMOVED
mk = dict(c.execute('SELECT old_id, kept_id FROM merged_entities'))
absent = collections.defaultdict(set)   # (game, concept) -> entities a hand review says must not have it (regression.tsv)
for r in csv.DictReader(open(os.path.join(TOOLS, 'regression.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['expect'] == 'absent':
        absent[r['game'], r['concept']].add(mk.get(int(r['entity']), int(r['entity'])))
ent = {i: (g, n, t) for i, g, n, t in c.execute('SELECT id, game, name, text FROM entities')}

KW_AFTER = r"(?=\s*(?:$|[\n.,:;(/]|\d|\s-))"
KW_ACT = r"\s+(?:a|an|the|all|each|your|any|one|two|three|\d|it|them|this|that|up to|another|enemy|friendly|random)\b"
kwnames = collections.defaultdict(set)   # game -> its keyword names, lower case
for g, n in c.execute("SELECT game, name FROM entities WHERE category='keyword'"): kwnames[g].add(re.sub(r'\s+', ' ', n.lower()).strip())

def kw_rx(phrase, concept):
    # a keyword name counts only where the game prints keywords (kw_links.py valid())
    k = re.sub(r'(\\ )+', r'\\s+', re.escape(phrase))
    r = K.KW_B + k + KW_AFTER
    return '(?:%s|%s)' % (r, K.KW_B + k + KW_ACT) if concept in K.KW_ACTION else r

def rx(phrase):
    s = re.escape(phrase)
    s = re.sub(r'(\\ )+', r'\\s+', s)
    s = re.sub(r'\d+', r'\\d+', s)
    if re.match(r'\w', phrase): s = r'\b' + s
    if re.search(r'\w$', phrase): s = s + r'\b'
    return s

out = []; stats = collections.Counter()
for g in [g for g in P.GAMES if g in ONLY]:
    f = os.path.join(TOOLS, 'key', g, 'key.json')
    if not os.path.exists(f): continue
    raw = K.load(g)   # with the keyword credit (KEY_BUG.md)
    ids = sorted(int(i) for i in raw if int(i) in ent)
    keyset = {i: K.narrow({k for k, _ in raw[str(i)]['tags']}) for i in ids}
    text = {i: P.norm_text(g, ent[i][1], ent[i][2]) for i in ids}
    sh = ids[:]; random.Random(1).shuffle(sh); half = [set(sh[:len(sh) // 2]), set(sh[len(sh) // 2:])]
    kept = collections.defaultdict(set)
    for a, b in ((0, 1), (1, 0)):
        cand = set()
        for i in half[a]:
            for k, words in raw[str(i)]['tags']:
                if k not in K.TREE or k in K.GROUPS: continue
                w = re.sub(r'\s+', ' ', P.norm_text(g, ent[i][1], words)).strip(' .,;:')
                if len(w) < 4 or w == 'name' or not re.search(rx(w), text[i], re.I): continue
                cand.add((k, kw_rx(w, k) if w in kwnames[g] else rx(w)))
        for k, p in cand:
            r = re.compile(p, re.I); n = ok = 0
            for i in half[b]:
                if r.search(text[i]):
                    n += 1; ok += P.right(k, keyset[i])
            stats['candidates'] += 1
            if any(r.search(P.norm_text(g, ent[e][1], ent[e][2])) for e in absent[g, k] if e in ent): stats['hit a reviewed drop'] += 1; continue
            if not (n >= MIN and ok >= PREC * n): continue
            m = [i for i in ids if r.search(text[i])]   # the whole key
            if sum(P.right(k, keyset[i]) for i in m) >= PREC * len(m): kept[k].add(p)
            else: stats['under 90% on the whole key'] += 1
    for k in sorted(kept):
        ps = sorted(kept[k]); stats['kept'] += len(ps); stats['concepts'] += 1
        p = '|'.join('(?:%s)' % x for x in ps) if len(ps) > 1 else ps[0]
        out.append(f'new\t{k}|{role(k)}|{g}|key\t{g}\t{p}')
    print(f'{g:18} key {len(ids):4}  concepts {len(kept):3}  patterns {sum(len(v) for v in kept.values()):4}')
D = os.path.join(HERE, 'decisions.tsv')
keep = [l for l in open(D, encoding='utf-8') if not (l.startswith('new\t') and l.split('\t')[1].endswith('|key') and l.split('\t')[2] in ONLY) and not l.startswith('# key_patterns')]   # other games' and other scripts' lines stay
with open(D, 'w', encoding='utf-8') as fh:
    fh.writelines(keep)
    fh.write('# key_patterns.py (patterns from the answer key quotes, 90%+ right on held-out key entries): new <concept|role|game|key> <game> <regex>\n')
    for l in out: fh.write(l + '\n')
print(dict(stats))
