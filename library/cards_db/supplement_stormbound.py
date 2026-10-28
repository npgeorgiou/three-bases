"""Stormbound: every card from the game's current card data, and the rulebook's glossary terms as keywords.
Cards: Stormbound Kitty's card database (the Sanity CMS its site and bin/export-cards.js read: project 5hlpazgd, dataset
production), 284 cards on 28 Oct 2026. It is newer than the library's copy (the repository's cards.json of 28 Feb 2022, 232
cards), so every card is written here and replaces the library's entry with the same card code (source.py). Fetch: GROQ query
*[_type=="card"]{"id": id.current, name, type, faction, unitTypes, rarity, mana, ability, strength, movement, token} at
https://5hlpazgd.apicdn.sanity.io/v2022-02-01/data/query/production (the workspace cannot reach it; read in the browser), saved
one card per line as id|name|type|faction|unitTypes|rarity|mana|strength|movement|token|ability (text without *...* marks).
Glossary: the statuses and special effects of the Stormbound Kitty rulebook (https://stormbound-kitty.com/rulebook), the game
having no official rulebook or keyword list; each definition is recorded with that source.
Writes supplement/stormbound.jsonl in the library's entities columns; ids from 1000001 (source.py), kept stable for entries
already in the file.
Usage: supplement_stormbound.py <cards.psv>"""
import json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'supplement', 'stormbound.jsonl')
CAT = {'unit': 'unit', 'spell': 'spell', 'structure': 'building'}
FAC = {'neutral': 'Neutral', 'winter': 'Winter', 'ironclad': 'Ironclad', 'shadowfen': 'Shadowfen', 'swarm': 'Swarm'}
RULEBOOK = 'Stormbound Kitty rulebook glossary (https://stormbound-kitty.com/rulebook), supplement'
GLOSSARY = [
    ('Poison', 'status', 'A poisoned unit takes 1 damage at the start of each turn until it dies or is vitalized.'),
    ('Vitalize', 'status', 'A vitalized unit gains 1 strength at the start of each turn until it is poisoned.'),
    ('Freeze', 'status', "A frozen unit does not move at the start of its next turn and its ability is disabled for that turn; "
                         'it lasts one turn.'),
    ('Confuse', 'status', 'A confused unit moves sideways at random during its movement; it lasts one turn.'),
    ('Disable', 'status', 'A disabled unit loses its ability until it dies.'),
    ('Command', 'effect', 'Forces a unit to move forward, ignoring its attack pattern and enemies on its sides.'),
    ('Convert', 'effect', "Switches a unit to the other player's side."),
    ('Destroy', 'effect', 'Removes a target from the board whatever its strength.'),
    ('Drain', 'effect', 'Damages one unit and gives the same amount of health to another.'),
    ('Force attack', 'effect', 'Makes a unit attack a bordering tile, usually at random; its before- and after-attacking '
                               'abilities trigger.'),
    ('Move fixedly forward', 'effect', 'Moves a unit forward while ignoring enemies on its sides.'),
    ('Pull', 'effect', 'Moves a unit toward another unit in the same row or column when nothing is between them; damage dealt '
                       'with it comes after the move.'),
    ('Push', 'effect', 'Moves a unit along a row or column until it reaches the edge of the board or another unit or structure; '
                       'a unit cannot be pushed into a base.'),
    ('Reduce strength', 'effect', 'Sets a unit\'s strength to a value; this is not damage.'),
    ('Spawn', 'effect', 'Creates a unit or structure on a tile; a random spawn is always within the front line.'),
]


def card(line):
    cid, name, typ, fac, types, rar, mana, strength, movement, token, text = line.rstrip('\n').split('|', 10)
    stats = {k: v for k, v in [('strength', strength), ('movement', int(movement) if movement.isdigit() else movement)] if v not in (None, '')}
    return {'game': 'stormbound', 'ext_id': cid, 'name': name, 'category': CAT[typ],
            'source_type': typ + ' (Stormbound Kitty card database 28 Oct 2026, supplement)', 'edition': None,
            'faction': FAC.get(fac, fac), 'subtypes': json.dumps([t.capitalize() for t in types.split(',')]) if types else None,
            'rarity': rar or None, 'cost': mana, 'cost_num': float(mana), 'stats': json.dumps(stats) if stats else None,
            'text': text.strip(), 'extra': json.dumps({'token': True}) if token == '1' else None, 'variants': None}


def main():
    lines = [l for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
    lib = sqlite3.connect(os.path.join(HERE, '..', 'three-bases-library.sqlite'))
    names = {n.lower() for (n,) in lib.execute("select name from entities where game='stormbound' and category='keyword'")}
    rows = [json.loads(l) for l in open(OUT)] if os.path.exists(OUT) else []
    old = {r['ext_id']: r['id'] for r in rows}
    nxt = max(list(old.values()) + [1000000]) + 1
    out = [card(l) for l in lines]
    out += [{'game': 'stormbound', 'ext_id': 'glossary:' + n, 'name': n, 'category': 'keyword',
             'source_type': f'{kind} ({RULEBOOK})', 'edition': None, 'faction': None, 'subtypes': None, 'rarity': None,
             'cost': None, 'cost_num': None, 'stats': None, 'text': t, 'extra': None, 'variants': None}
            for n, kind, t in GLOSSARY if n.lower() not in names]
    for e in out:
        e['id'] = old.get(e['ext_id']) or nxt
        nxt += e['id'] == nxt
    with open(OUT, 'w') as f:
        for e in out: f.write(json.dumps(e, ensure_ascii=False) + '\n')
    print('cards', sum(e['category'] != 'keyword' for e in out), 'keywords', sum(e['category'] == 'keyword' for e in out))


if __name__ == '__main__':
    main()
