"""Check reading files (keywords/<game>.txt, readings/<game>.txt: "entity | ability | trigger | effect | target | amount |
duration | condition", # comments) against the record format in common.py. Prints each bad line and a count per file.
Usage: check_records.py <db> <file>..."""
import os, sqlite3, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import COLUMNS, check
c = sqlite3.connect(sys.argv[1])
triggers = {r[0] for r in c.execute("SELECT id FROM concepts WHERE facet='trigger'")}
effects = {r[0] for r in c.execute("SELECT id FROM concepts WHERE facet NOT IN ('trigger','problem')")}
ids = {r[0] for r in c.execute("SELECT id FROM entities")}


def read(path):
    src = 'keyword' if os.path.basename(os.path.dirname(path)) == 'keywords' else 'reading'
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        if not line.strip() or line.startswith('#'): continue
        f = [x.strip() for x in line.rstrip('\n').split('|')]
        f += [''] * (8 - len(f))
        yield n, dict(zip(COLUMNS, f[:8] + [src]))


if __name__ == '__main__':
    for p in sys.argv[2:]:
        bad = 0; recs = 0
        for n, r in read(p):
            recs += 1
            prob = check(r, triggers, effects) + ([] if r['entity'].isdigit() and int(r['entity']) in ids else ['entity'])
            if prob: bad += 1; print(f'{p}:{n}: ' + '; '.join(prob))
        print(f'{p}: {recs} records, {bad} with problems')
