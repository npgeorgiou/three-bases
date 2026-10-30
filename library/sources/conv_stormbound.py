"""Stormbound -> two load files (format in load_cards.py).
Source: src/data/cards.json of github.com/Stormbound-Games/stormbound-kitty at commit 96a86726 (28 Feb 2022), the last commit
that kept the card list in the repository (later the site reads it from its CMS); 232 cards with level-1-to-5 values.
- Text: the ability with the site's emphasis marks (*...*) removed; a number that changes with the card's level is written as the
  five level values ("2/3/4/5/6"), as the source does. Strength by level and movement go to stats.
- Category: unit, spell, structure (building). Faction: Neutral, Winter, Ironclad, Shadowfen, Swarm. Race (Dragon, Knight, ...)
  becomes a tribe. Tokens (the source's 'token') are created cards. The source has no keyword list; its status words (freeze,
  poison, vitalize, confuse, disable) are read by the game's patterns (patterns/stormbound.txt).
Writes <out>_types.json (races) and <out>_cards.json. Usage: conv_stormbound.py <cards.json> <out>"""
import collections, json, re, sys
src, out = sys.argv[1:3]
d = json.load(open(src, encoding='utf-8'))
CAT = {'unit': 'unit', 'spell': 'spell', 'structure': 'building'}
FAC = {'neutral': 'Neutral', 'winter': 'Winter', 'ironclad': 'Ironclad', 'shadowfen': 'Shadowfen', 'swarm': 'Swarm'}
cards = []
for c in d:
    text = re.sub(r'\*', '', c.get('ability') or '').strip()
    race = (c.get('race') or '').capitalize()
    stats = {k: v for k, v in [('strength', c.get('strength')), ('movement', c.get('movement'))] if v not in (None, '')}
    mana = c.get('mana')
    cards.append({'ext_id': c['id'], 'name': c['name'], 'category': CAT[c['type']], 'source_type': c['type'],
                  'faction': FAC.get(c['faction'], c['faction']), 'subtypes': [race] if race else [], 'rarity': c.get('rarity'),
                  'cost': str(mana) if mana is not None else None, 'stats': stats or None, 'text': text,
                  'created': bool(c.get('token')),
                  'extra': {k: v for k, v in [('hero', c.get('hero')), ('elder', c.get('elder')), ('ancient', c.get('ancient'))] if v}})
races = collections.Counter(s for x in cards for s in x['subtypes'])
tr = [{'ext_id': 'type:' + t, 'name': t, 'category': 'tribe', 'source_type': 'card type / tribe', 'text': f'{t}: {n} entities of this type.'}
      for t, n in sorted(races.items())]
game = {'id': 'stormbound', 'name': 'Stormbound', 'family': 'Stormbound', 'edition': 'card list of 28 Feb 2022 (Stormbound Kitty)',
        'source': 'github.com/Stormbound-Games/stormbound-kitty src/data/cards.json at commit 96a86726 (28 Feb 2022)',
        'structure': 'Two-player card game on a board of 4 lanes and 5 rows between two bases. Units are played on free tiles up to the '
                     "player's front line and move forward at the start of their owner's turn, attacking what stands in front; a unit "
                     "that reaches the enemy base deals its strength as damage to the base. Structures do not move. Mana grows by 1 "
                     'each turn. Each card has five levels with growing numbers.',
        'notes': 'No keyword list in the source; status words are read by patterns. Numbers that change by level are written as five values.'}
src = 'Stormbound Kitty cards.json (28 Feb 2022)'   # races first, in their own file, so the cards link to them
json.dump({'_source': src, '_tag': 'stormbound_kw', '_game': game, 'cards': tr}, open(out + '_types.json', 'w'), ensure_ascii=False, indent=0)
json.dump({'_source': src, '_tag': 'stormbound', 'cards': cards}, open(out + '_cards.json', 'w'), ensure_ascii=False, indent=0)
print('cards', len(cards), 'tokens', sum(x['created'] for x in cards), 'tribes', len(tr), 'without text', sum(not x['text'] for x in cards))
