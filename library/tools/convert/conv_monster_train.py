"""Monster Train -> two load files (format in load_cards.py): <out>_keywords.json (keywords, unit types) and <out>_cards.json.
Source: Module:Cards/Data of the Monster Train fandom wiki (monster-train.fandom.com), read through Kaptain's Chrome on
20 Oct 2026 and flattened by a browser script to one line per card: name|clan|type|rarity|cost|capacity|attack|health|tags|
description|essence (wiki markup removed; {{Value|n|Icon}} written as 'n Icon', an X-cost multiple as 'n per X'). 282 cards:
the six clans (Hellhorned, Awoken, Stygian Guard, Umbra, Melting Remnant, Wurmkin) and clanless cards.
- Category: Spell spell, Champion hero, Blight and Scourge (junk cards) spell, every other type a unit whose type is its tribe
  ('Demon Imp' -> Demon, Imp). Faction: the clan. Champions have no text in the source, only their tags.
- Keywords: the wiki's tags that are game keywords (KW); the other tags (Create, Draw, Move ...) are left out. The source has
  no keyword definitions; keyword concepts are in reviews/monster_train.json. Essence (the upgraded text) goes to extra.
Usage: conv_monster_train.py <cards.psv> <out>"""
import collections, json, sys
src, out = sys.argv[1:3]
KW = {'Armor', 'Rage', 'Multistrike', 'Slay', 'Revenge', 'Summon', 'Resolve', 'Incant', 'Strike', 'Extinguish', 'Harvest', 'Gorge',
      'Eaten', 'Burnout', 'Endless', 'Consume', 'Permafrost', 'Piercing', 'Attuned', 'Pyrebound', 'Offering', 'Quick', 'Sweep',
      'Trample', 'Lifesteal', 'Damage Shield', 'Spikes', 'Regen', 'Frostbite', 'Sap', 'Dazed', 'Rooted', 'Melee Weakness',
      'Spell Weakness', 'Stealth', 'Fragile', 'Inert', 'Fuel', 'Shell', 'Hatch', 'Reap', 'Etch', 'Inspire', 'Extract', 'Infused',
      'Charged Echo', 'Emberdrain', 'Silence', 'Phased', 'Purge', 'Reserve', 'Unplayable', 'Unpurgeable', 'Rejuvenate',
      'Cultivate', 'Ascend', 'Descend', 'Reform', 'Rally', 'Action', 'Enchant', 'Hunger', 'Buffet', 'Armored', 'Magic Power', 'Frozen'}
JUNK = {'Blight', 'Scourge'}
cards = []
for ln in open(src, encoding='utf-8'):
    p = ln.rstrip('\n').split('|')
    if len(p) < 11: continue
    name, clan, typ, rar, cost, cap, atk, hp, tags, desc, ess = p[:11]
    tl = [t.strip() for t in tags.split(',') if t.strip()]
    cat = 'spell' if typ == 'Spell' or typ in JUNK else 'hero' if typ == 'Champion' else 'unit'
    sub = [typ] if typ in JUNK else [] if cat != 'unit' else typ.split()
    stats = {k: v for k, v in [('capacity', cap), ('attack', atk), ('health', hp)] if v}
    cards.append({'ext_id': name, 'name': name, 'category': cat, 'source_type': typ.lower(), 'faction': clan, 'subtypes': sub,
                  'rarity': rar or None, 'cost': cost or None, 'stats': stats or None, 'text': desc,
                  'keywords': [t for t in tl if t in KW], 'extra': {k: v for k, v in [('essence', ess), ('tags', tl)] if v}})
kw = [{'ext_id': 'kw:' + k, 'name': k, 'category': 'keyword', 'source_type': 'keyword', 'text': None} for k in sorted(KW)]
types = collections.Counter(s for x in cards for s in x['subtypes'])
tr = [{'ext_id': 'type:' + t, 'name': t, 'category': 'tribe', 'source_type': 'card type / tribe', 'text': f'{t}: {n} entities of this type.'} for t, n in sorted(types.items())]
game = {'id': 'monster_train', 'name': 'Monster Train', 'family': 'Monster Train', 'edition': 'six clans incl. Wurmkin (fandom wiki card data)',
        'source': 'monster-train.fandom.com Module:Cards/Data, read 20 Oct 2026',
        'structure': 'Single-player roguelike deckbuilder. The player defends a train of three floors with the Pyre on top; waves of '
                     'enemies enter the bottom floor and fight the units there, then ascend floor by floor toward the Pyre. Units are '
                     'played onto floors with a limited capacity; the front unit of each side fights first. Ember pays for cards; '
                     'each run uses a main and an allied clan and a champion.',
        'notes': 'Keyword list from the wiki tags; no keyword definitions in the source.'}
s = 'Monster Train fandom wiki Module:Cards/Data (20 Oct 2026)'
json.dump({'_source': s, '_tag': 'monster_train_kw', '_game': game, 'cards': kw + tr}, open(out + '_keywords.json', 'w'), ensure_ascii=False, indent=0)
json.dump({'_source': s, '_tag': 'monster_train', '_keywords_from_field': True, 'cards': cards}, open(out + '_cards.json', 'w'), ensure_ascii=False, indent=0)
print('cards', len(cards), 'keywords', len(kw), 'types', len(tr), collections.Counter(x['category'] for x in cards))
