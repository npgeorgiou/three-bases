"""The card source: the library's entities plus supplement/<game>.jsonl (cards the library lacks, taken from another source,
same columns as entities). Every script opens the library through lib(), so a supplement card is a card like any other.
Id blocks, one per game (PROCESS.md step 0.4); a new game writes its line here first:
  runeterra   900001-999999     cards from Riot's data from 900001; Kaptain's definitions from 990001
  stormbound  1000001-1999999   cards and glossary keywords from 1000001; Kaptain's definitions from 1900001
  monster_train 2000001-2999999 cards and glossary keywords from 2000001; Kaptain's definitions from 2900001
  faeria      3000001-3999999   cards and glossary keywords from 3000001; Kaptain's definitions from 3900001
  inscryption 4000001-4999999   cards and glossary keywords from 4000001; Kaptain's definitions from 4900001
  duelyst     5000001-5999999   cards and glossary keywords from 5000001; Kaptain's definitions from 5900001
  into_the_breach 6000001-6999999 cards and glossary keywords from 6000001; Kaptain's definitions from 6900001
  then        7000001-7999999, 8000001-8999999, ... (each game takes the first free block and writes its line here)"""
import glob, json, os, sqlite3
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, '..', 'three-bases-library.sqlite')
# a supplement that holds a game's full card list replaces every library entry of these categories (not only same codes)
FULL = {'inscryption': ('unit', 'terrain')}
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
    # a supplement entry replaces the library's entry with the same card code, bare (Faeria '45') or prefixed (the game's own newer data)
    full = ' or '.join(f"(e.game='{g}' and e.category in ({','.join(repr(x) for x in cats)}))" for g, cats in FULL.items()) or '0'
    c.execute("create temp view entities as select * from main.entities e where not exists (select 1 from temp.supplement s "
              "where s.game=e.game and s.ext_id is not null and (e.ext_id = s.ext_id or e.ext_id like '%:' || s.ext_id)) "
              f"and not ({full}) union all select * from temp.supplement")
    # links between supplement cards (level-up forms, generated cards): supplement/<game>_links.jsonl
    c.execute('create temp table supplement_links as select * from main.entity_links where 0')
    for f in sorted(glob.glob(os.path.join(HERE, 'supplement', '*_links.jsonl'))):
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                c.execute('insert into temp.supplement_links(src, rel, dst, evidence) values(?,?,?,?)', (r['src'], r['rel'], r['dst'], r.get('evidence')))
    c.execute('create temp view entity_links as select * from main.entity_links union all select * from temp.supplement_links')
    return c
