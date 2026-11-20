"""One faction from the concepts Kaptain gives, made the way step 6 makes the roster's factions (kernel_factions.py).
python3 factions/roster/work/make_faction.py "armour" "heal" ["<concept>" ...] [--name "Can't be broken"] [--alone]
  (from the repo, about a minute) -> factions/roster/work/made/<name>.md, one faction sheet like kernel_factions.md.
A concept is named by its key or by words of its plain name.
1. Its kernel: the concepts given.
2. Its concepts: every other usable concept ranked by its fit to the kernel, filling the faction to 22 with the kernel.
3. What it is about: the kernel and its strong concepts (fit 1/3 or more); its decks, deck style and what of it acts on
   enemy units come from these.
4. With the roster (the default): a concept already in 3 of the roster's factions (work/kernel_factions.tsv) is not
   taken, and the page shows its strongest partners (strong card links between what it is about and what each roster
   faction is about) and the factions it shares most concepts with. With --alone, the roster is not looked at."""
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


kernel = list(dict.fromkeys(find(w) for w in words))
name = NAME or ' + '.join(K.name(c) for c in kernel)
roster = [] if ALONE else list(csv.DictReader(open(os.path.join(HERE, 'kernel_factions.tsv'), encoding='utf-8'), delimiter='\t'))
held = collections.Counter(c for f in roster for c in f['concepts'].split(','))
fit = {c: v for c, v in K.fit_to(kernel).items() if held[c] < K.MAX_SHARE}
concepts = kernel + sorted(fit, key=lambda c: (-fit[c], c))[:K.LIST - len(kernel)]
mine = K.about(kernel, concepts, fit)
partner_names, shares = [], []
if roster:
    rows = []
    for f in roster:
        theirs = f['kernel'].split(',') + [c for c in f['strong'].split(',') if c]
        links = sum(K.linked(a, b) for a in mine for b in theirs if a not in theirs and b not in mine)
        rows.append((links, len(set(concepts) & set(f['concepts'].split(','))), f['name']))
    partner_names = [n for l, s, n in sorted(rows, reverse=True)[:K.PARTNERS] if l]
    shares = [n for l, s, n in sorted(rows, key=lambda t: (-t[1], t[2])) if s][:3]
page = [K.KEY, ''] + K.sheet(name, '', '', [], kernel, mine[len(kernel):], concepts, [c for c in mine if c in K.hurts],
                              K.markers_of(K.kernel_decks(mine)), partner_names)
page += (['### Shares most concepts with', ''] + [f'- {n}' for n in shares] + ['']) if roster else ['Made alone: the roster was not looked at.', '']
os.makedirs(os.path.join(HERE, 'made'), exist_ok=True)
out = os.path.join(HERE, 'made', re.sub(r'[^\w]+', '_', name.lower()).strip('_') + '.md')
open(out, 'w', encoding='utf-8').write('\n'.join(page) + '\n')
print('\n'.join(page)); print('->', out)
