"""tag_read_sum.py: the readers' verdicts (reads/batch_NN.verdicts.tsv) per family of tag_reads.tsv -> tag_verdicts.tsv.
A family is fixed when 4 of 5 read say wrong the same way (all, when fewer than 4 were read), stays when 4 of 5 say right,
and is mixed otherwise (the script splits it by one more detail and 5 cards of each half are read)."""
import csv, glob, collections, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
v = {}
for f in sorted(glob.glob(os.path.join(HERE, 'reads', '*.verdicts.tsv'))):
    for r in csv.reader(open(f), delimiter='\t'):
        if r and r[0].strip().isdigit(): v[r[0].strip()] = r[1].strip() if len(r) > 1 else ''
fam = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(HERE, 'tag_reads.tsv')), delimiter='\t'):
    if r['card id'] in v: fam[(r['concept'], r['family'], r['why suspect'])].append(v[r['card id']])
with open(os.path.join(HERE, 'tag_verdicts.tsv'), 'w') as f:
    f.write('concept\tfamily\twhy suspect\tread\tright\twrong\tunsure\tmost said wrong as\tresult\n')
    for (k, fm, why), vs in sorted(fam.items()):
        n = len(vs); rt = sum(a.lower().startswith('right') for a in vs)
        w = [re.sub(r'^wrong:?\s*(should be)?\s*', '', a, flags=re.I).strip().lower() for a in vs if a.lower().startswith('wrong')]
        top = collections.Counter(w).most_common(1); tn = top[0][1] if top else 0
        need = 4 if n >= 4 else n
        res = 'fix' if tn >= need else 'stays' if rt >= need else 'mixed'
        f.write('\t'.join([k, fm, why, str(n), str(rt), str(len(w)), str(n - rt - len(w)), top[0][0] if top else '', res]) + '\n')
