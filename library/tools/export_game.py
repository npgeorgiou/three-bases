"""Export one game of the library as load files, to reload it with today's patterns and steps (README suggestion 2).
Each entry keeps its id, ext_id and name (load file option _reload), so the hand reviews, the answer key, regression.tsv, key_wins
and revert lists, which name entries by id, still apply after the reload. Writes <out>_kw.json (keywords and tribes) and <out>.json (every
other entry with its converter data tags and created flag, and every link between the game's entries, restored as they are:
keyword, type, name and variant links come from the first build's sources and are not all re-derivable). Links to other games and
merged_entities rows stay in the library (drop_game.py --reload). Run on an expanded database. Usage: export_game.py <db> <game> <out prefix>
Reload: tools/reload_game.sh <game> <scratch dir>."""
import json, sqlite3, sys
db, G, out = sys.argv[1:4]
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
game = dict(zip(['id', 'name', 'family', 'edition', 'source', 'structure', 'notes'], q('SELECT * FROM games WHERE id=?', G)[0]))
data = {}
for e, k, r, ev in q("SELECT ec.entity, ec.concept, ec.role, ec.evidence FROM entity_concepts ec JOIN entities x ON x.id=ec.entity WHERE x.game=? AND ec.method='data_rule'", G):
    data.setdefault(e, []).append([k, r, ev])
cols = ['id', 'ext_id', 'name', 'category', 'source_type', 'edition', 'faction', 'subtypes', 'rarity', 'cost', 'cost_num', 'stats', 'text', 'extra']
kw_cards, cards = [], []
for row in q(f"SELECT {','.join(cols)} FROM entities WHERE game=? ORDER BY id", G):
    e = dict(zip(cols, row)); i = e['id']
    e['subtypes'] = json.loads(e['subtypes']) if e['subtypes'] else None
    e['extra'] = json.loads(e['extra']) if e['extra'] else None
    if e['edition'] == 'non-collectible':   # load_cards moves a created card's set back into edition
        e['created'] = True; ex = dict(e['extra'] or {}); e['edition'] = ex.pop('set', None); e['extra'] = ex or None
    if i in data: e['tags'] = data[i]
    (kw_cards if e['category'] in ('keyword', 'tribe') else cards).append({k: v for k, v in e.items() if v is not None})
head = {'_source': f'reload of {G} from the library', '_reload': True, '_game': game}
json.dump(dict(head, _tag='reload-kw', cards=kw_cards), open(out + '_kw.json', 'w', encoding='utf-8'), ensure_ascii=False)
links = q("SELECT l.src, l.rel, l.dst, l.evidence FROM entity_links l JOIN entities s ON s.id=l.src JOIN entities d ON d.id=l.dst WHERE s.game=? AND d.game=?", G, G)
json.dump(dict(head, _tag='reload', cards=cards, _links=[list(r) for r in links]),
          open(out + '.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(G, 'exported', len(kw_cards), 'keywords and tribes,', len(cards), 'entries')
