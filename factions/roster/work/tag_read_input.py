"""tag_read_input.py (run from library/cards_db): the reader's inputs for work/tag_reads.tsv. Per family: the concept's
definition and what it is not (concept tree); per card: its text, keywords and rows, its keywords' entries (their rules in
its game) and the cards it names or makes (rows.py). Writes work/reads/batch_NN.md, about 20 cards each, families kept
whole; the reader writes work/reads/batch_NN.verdicts.tsv (card id, verdict, why). With `tag_reads2.tsv round2`: the
second reading's cards not read yet, into work/reads/round2_NN.md."""
import contextlib, csv, io, os, sqlite3, sys
sys.path.insert(0, os.getcwd())
import rows

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'reads'); os.makedirs(OUT, exist_ok=True)
c = sqlite3.connect('cards.sqlite')
tree = {}
for l in open('../concept_tree.txt'):
    if l.startswith('#') or '|' not in l: continue
    p = [x.strip() for x in l.split('|')]
    tree[p[0]] = p


def show(i):
    f = io.StringIO()
    try:
        with contextlib.redirect_stdout(f): rows.show(i)
    except TypeError: return f'(card {i} has no text in the library)\n'  # a card the library has rows for but no text
    return f.getvalue()


fams = {}
SRC, PRE = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('tag_reads.tsv', 'batch')
for r in csv.DictReader(open(os.path.join(HERE, SRC)), delimiter='\t'):
    if r.get('verdict'): continue  # read before
    fams.setdefault((r['concept'], r['family'], r['why suspect']), []).append(r)
batches, cur = [], []
for k, rs in fams.items():
    if cur and len(cur) + len(rs) > 20: batches.append(cur); cur = []
    cur += [(k, r) for r in rs]
if cur: batches.append(cur)
for n, b in enumerate(batches, 1):
    out = [f'# Tag reading, batch {n:02d}', '']
    last = None
    for (k, fam, why), r in b:
        if (k, fam, why) != last:
            t = tree.get(k, [k, k, '', '', '', ''])
            out += ['', f'## Family: concept `{k}` ("{t[1]}"), from rows `{fam}`', f'- Counts as {k}: {t[4]}', f'- Not {k}: {t[5]}',
                    f'- Why the script suspects it: {why}', '']
            last = (k, fam, why)
        i = int(r['card id'])
        out += [f'### Card {i} ({r["game"]}), tagged from: {r["group"]}', '', show(i)]
        kws = [k2 for (k2,) in c.execute('select keyword from card_keyword where card=?', (i,))]
        kws += [k2 for (k2,) in c.execute('select distinct keyword_ref from effect e join ability a on a.id=e.ability where a.card=? and keyword_ref is not null', (i,)) if k2 not in kws]
        for k2 in kws[:4]: out += ['Keyword entry:', show(k2)]
        refs = [x for (x,) in c.execute('select distinct card_ref from effect e join ability a on a.id=e.ability where a.card=? and card_ref is not null and card_ref!=?', (i, i))]
        for x in refs[:3]: out += ['Card it names or makes:', show(x)]
    open(os.path.join(OUT, f'{PRE}_{n:02d}.md'), 'w').write('\n'.join(out) + '\n')
print(len(batches), 'batches', sum(len(b) for b in batches), 'cards')
