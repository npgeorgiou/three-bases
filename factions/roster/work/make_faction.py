"""One faction from the concepts Kaptain gives, made the way step 6 makes the roster's factions (kernel_factions.py).
python3 factions/roster/work/make_faction.py "armour" "heal" ["<concept>" ...] [--name "Can't be broken"] [--alone]
  (from the repo, about a minute) -> factions/roster/work/made/<name>.md, one faction sheet like kernel_factions.md.
A concept is named by its key or by words of its plain name.
1. Its kernel: the concepts given (its core); its decks: the real decks whose cards with any kernel concept make up twice
   the share its game's decks average or more.
2. A first ranked fill: every other usable concept scored by how well it goes with the core (step 6, 4), the best 22.
3. Its answers: between lanes from its core alone (step 6); for each other question its core does not answer, up to 2
   concepts that answer it, from the fill and the top of
   its list, the ones that go best with the core (step 6, 12); they join the kernel.
4. The ranked fill again, by fit to the core, outside the whole kernel: 12 concepts, then its extras to 22.
5. With the roster (the default): a concept already in 3 of the roster's factions (work/kernel_factions.tsv) is not
   taken, no answer uses a concept a roster faction answers the same question with, and the page shows its strongest
   partners and the factions it shares most concepts with. With --alone, the roster is not looked at.
The page is laid out like kernel_factions.md (K.sheet): concepts with [K] on the kernel, design answers, deck style."""
import collections, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
args = sys.argv[1:]
ALONE = '--alone' in args
NAME = args[args.index('--name') + 1] if '--name' in args else None
words = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] != '--name')]
if not words: sys.exit(__doc__)
import kernel_factions as K  # its data and the step 6 functions (the roster itself is not run)


def find(word):
    """a concept key from its key or words of its plain name"""
    if word in K.usable: return word
    hits = [c for c in K.usable if all(w in K.plain.get(c, c).lower() for w in re.findall(r'\w+', word.lower()))]
    if not hits: sys.exit(f'No usable concept for "{word}".')
    paren = lambda c: re.findall(r'\((.*)\)', K.plain.get(c, c))
    return min(hits, key=lambda c: (word.lower() not in c, not any(word.lower() in p.lower() for p in paren(c)), len(K.plain.get(c, c)), c))


core = list(dict.fromkeys(find(w) for w in words))
name = NAME or ' + '.join(K.plain.get(c, c) for c in core)
roster = [] if ALONE else list(csv.DictReader(open(os.path.join(HERE, 'kernel_factions.tsv'), encoding='utf-8'), delimiter='\t'))
held = collections.Counter(c for f in roster for c in set(f['concepts'].split(',') + [e for e in f['extras'].split(',') if e]))
taken = collections.defaultdict(set)  # question -> concepts a roster faction answers it with
for f in roster:
    for part in (f.get('by_question') or '').split(';'):
        if ':' in part:
            q, cs = part.split(':', 1); taken[q] |= {c for c in cs.split('+') if c and c not in f['kernel'].split(',')}
full = {c for c, n in held.items() if n >= K.MAX_SHARE}


def ranked(kernel, base):
    """usable concepts not in the kernel, best fit to base first, without those already in MAX_SHARE roster factions"""
    fit = {c: sum(K.fit2(c, q) for q in base) / len(base) for c in K.usable if c not in kernel and c not in full}
    return fit, sorted(fit, key=lambda c: (-fit[c], c))


x = {'name': name, 'core': core, 'kernel': list(core), 'theme_likes': set()}
fit, order = ranked(core, core)
x['concepts'] = core + order[:K.OWN - len(core)]; x['extras'] = order[K.OWN - len(core):K.OWN + K.EXTRAS - len(core)]
x['score'] = {c: v[0] for c, v in K.lib.scores(x['concepts']).items()}
ban = {q: set(taken.get(q, ())) if q != 'cares' else set() for q in K.Q5}; ban['all'] = set(full)
by_q = K.choose(x, ban)
kernel = core + sorted(set().union(*by_q.values()) - set(core))
fit, order = ranked(kernel, core)
concepts = order[:max(0, K.OWN - len(kernel))]; extras = order[len(concepts):len(concepts) + K.EXTRAS]
decks = K.kernel_decks(kernel)

partner_names, shares = [], []
if roster:
    mine = set(kernel + concepts + extras); rows = []
    for f in roster:
        theirs = set(f['concepts'].split(',') + [e for e in f['extras'].split(',') if e])
        links = sum(K.linked(a, b) for a in mine for b in theirs if a not in theirs and b not in mine)
        rows.append((links, len(mine & theirs), f['name']))
    partner_names = [n for l, s, n in sorted(rows, reverse=True)[:K.PARTNERS]]
    shares = [n for l, s, n in sorted(rows, key=lambda t: -t[1]) if s][:3]
page = ['[K] marks a kernel concept.', ''] + K.sheet(name, '', '', [], kernel, concepts + extras, by_q, K.markers_of(decks), partner_names)
page += ['### Shares most concepts with', ''] + [f'- {n}' for n in shares] + [''] if roster else ['Made alone: the roster was not looked at.', '']
os.makedirs(os.path.join(HERE, 'made'), exist_ok=True)
out = os.path.join(HERE, 'made', re.sub(r'[^\w]+', '_', name.lower()).strip('_') + '.md')
open(out, 'w', encoding='utf-8').write('\n'.join(page) + '\n')
print('\n'.join(page)); print('->', out)
