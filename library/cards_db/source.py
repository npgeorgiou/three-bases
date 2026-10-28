"""The card source: the library's entities plus supplement/<game>.jsonl (cards the library lacks, taken from another source,
same columns as entities). Every script opens the library through lib(), so a supplement card is a card like any other."""
import glob, json, os, sqlite3
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, '..', 'three-bases-library.sqlite')
COLS = ['id', 'game', 'ext_id', 'name', 'category', 'source_type', 'edition', 'faction', 'subtypes', 'rarity', 'cost', 'cost_num',
        'stats', 'text', 'extra', 'variants']


def lib():
    c = sqlite3.connect(DB)
    c.execute('create temp table supplement as select * from main.entities where 0')
    for f in sorted(glob.glob(os.path.join(HERE, 'supplement', '*.jsonl'))):
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                c.execute(f"insert into temp.supplement({','.join(COLS)}) values({','.join('?' * len(COLS))})", [r.get(k) for k in COLS])
    c.execute('create temp view entities as select * from main.entities union all select * from temp.supplement')
    return c
