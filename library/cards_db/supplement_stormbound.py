"""Stormbound cards the library lacks (by card code and by name), and the rulebook's glossary terms as keywords.
Cards: the library's own source, src/data/cards.json of github.com/Stormbound-Games/stormbound-kitty at commit 96a86726
(28 Feb 2022). The old library dropped 42 of its 232 cards (41 without ability text, mostly tokens); they come back here in the
same form as the library's Stormbound entries (text without the *...* marks, level numbers as "1/2/3/4/5").
Glossary: the statuses and special effects of the Stormbound Kitty rulebook (https://stormbound-kitty.com/rulebook), the game
having no official rulebook or keyword list; each definition is recorded with that source.
Writes supplement/stormbound.jsonl in the library's entities columns; ids from 1000001 (source.py), kept stable for entries
already in the file.
Usage: supplement_stormbound.py <cards.json> (fetch: git clone --filter=blob:none --no-checkout
https://github.com/Stormbound-Games/stormbound-kitty <clone>, then git -C <clone> show 96a86726:src/data/cards.json > cards.json)."""
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


def card(c):
    stats = {k: v for k, v in [('strength', c.get('strength')), ('movement', c.get('movement'))] if v not in (None, '')}
    race = (c.get('race') or '').capitalize()
    extra = {k: True for k in ('hero', 'elder', 'ancient') if c.get(k)}
    if c.get('token'): extra['token'] = True
    return {'game': 'stormbound', 'ext_id': c['id'], 'name': c['name'], 'category': CAT[c['type']],
            'source_type': c['type'] + ' (Stormbound Kitty cards.json 28 Feb 2022, supplement)', 'edition': None,
            'faction': FAC.get(c['faction'], c['faction']), 'subtypes': json.dumps([race]) if race else None,
            'rarity': c.get('rarity'), 'cost': str(c['mana']) if c.get('mana') is not None else None,
            'cost_num': float(c['mana']) if c.get('mana') is not None else None,
            'stats': json.dumps(stats) if stats else None, 'text': re.sub(r'\*', '', c.get('ability') or '').strip(),
            'extra': json.dumps(extra) if extra else None, 'variants': None}


def main():
    src = json.load(open(sys.argv[1], encoding='utf-8'))
    lib = sqlite3.connect(os.path.join(HERE, '..', 'three-bases-library.sqlite'))
    codes = {e.split(':')[-1] for (e,) in lib.execute("select ext_id from entities where game='stormbound'")}
    names = {n.lower() for (n,) in lib.execute("select name from entities where game='stormbound'")}
    rows = [json.loads(l) for l in open(OUT)] if os.path.exists(OUT) else []
    old = {r['ext_id']: r['id'] for r in rows}
    nxt = max(list(old.values()) + [1000000]) + 1
    out = [card(c) for c in src if c['id'] not in codes and c['name'].lower() not in names]
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
