"""The Elder Scrolls: Legends -> one load file (format in load_cards.py).
Source: database/dbCards.json and dbTokens.json of github.com/edipo2s/TESLegendsTracker at commit c541e82 (22 Apr 2018):
855 cards of Core Set, Madhouse Collection, Dark Brotherhood, Heroes of Skyrim, Clockwork City, Forgotten Hero and Houses of
Morrowind, plus 79 tokens. Later sets (Isle of Madness onward) are not in it.
- Faction: the attribute (Strength, Intelligence, Willpower, Agility, Endurance, Neutral); a dual card is '<attr1>-<attr2>'.
- Category: Creature unit, Action spell, Item item, Support building. Race becomes a tribe. Tokens are created cards.
- Keywords from the source's keyword field, kept when they are Legends keywords (KW below). The source has no keyword
  definitions; the keyword entries carry Claude's one-line summary of the rule (source_type says so), and their concepts are
  in reviews/tesl.json.
Writes <out>_keywords.json (keywords and races, loaded first so the cards can link to them) and <out>_cards.json.
Usage: conv_tesl.py <dbCards.json> <dbTokens.json> <out>"""
import collections, json, re, sys
cards_f, tokens_f, out = sys.argv[1:4]
KW = {  # Claude's summaries of the rules (not source text)
 'Breakthrough': 'Damage it deals beyond what kills a creature is dealt to the opponent.',
 'Charge': 'It can attack the turn it is played.',
 'Drain': 'On your turn, damage it deals heals you that much.',
 'Guard': 'Enemy creatures in its lane must attack it before attacking anything else.',
 'Lethal': 'Any damage it deals to a creature destroys that creature.',
 'Regenerate': 'At the start of your turn it heals all its damage.',
 'Ward': 'The first damage or effect that would hit it is prevented and the Ward is removed.',
 'Prophecy': 'When it is drawn from a broken rune, you may play it at once for free.',
 'Summon': 'Triggers when the creature is played.',
 'Last Gasp': 'Triggers when the creature dies.',
 'Slay': 'Triggers when it destroys an enemy creature on your turn.',
 'Pilfer': 'Triggers when it deals damage to the opponent.',
 'Rally': 'When it attacks, a random creature in your hand gets +1/+1.',
 'Activate': 'Triggers when you use the support (supports have a number of uses).',
 'Exalt': 'Pay extra magicka when you play it to get a bonus.',
 'Shackle': 'A shackled creature cannot attack or block on its next turn.',
 'Plot': 'Triggers if you played another card this turn.',
 'Betray': 'After you play it, you may sacrifice a creature to play it again.',
 'Treasure Hunt': 'It collects treasure when you draw cards of the listed kinds and gets a bonus once all are found.',
 'Silence': 'Removes all text and effects from a creature.',
 'Shout': 'Each time you play a shout, all your copies of it level up.',
 'Unsummon': "Returns a creature to its owner's hand.",
 'Battle': 'Two creatures deal damage to each other without attacking.',
 'Assemble': 'Choose one of two bonuses; all your Factotums get it.',
 'Cover': 'It cannot be attacked (creatures in the shadow lane get Cover for a turn).',
 'Evolves': 'It transforms into a stronger creature when its condition is met.',
 'Beast Form': None, 'Ongoing': None,   # names kept, rule not summarised (Claude unsure of the exact rule)
}
CAT = {'creature': 'unit', 'action': 'spell', 'item': 'item', 'support': 'building'}
def cards_of(path, created):
    d = json.load(open(path, encoding='utf-8')); res = []
    for st, byattr in d.items():
        for attr, cs in byattr.items():
            for key, v in cs.items():
                fac = attr.capitalize() if attr != 'dual' else f"{v.get('attr1', '').capitalize()}-{v.get('attr2', '').capitalize()}"
                kws = [k.strip() for k in re.split(r'[,.]', v.get('keyword') or '') if k.strip() in KW]
                stats = {k: v[k] for k in ('attack', 'health') if v.get(k) not in (None, '')}
                res.append({'ext_id': f'{st}:{key}', 'name': v['name'], 'category': CAT[v['type'].lower()], 'source_type': v['type'].lower(),
                            'edition': st, 'faction': fac, 'subtypes': [v['race']] if v.get('race') else [], 'rarity': v.get('rarity'),
                            'cost': v.get('cost'), 'stats': stats or None, 'text': (v.get('text') or '').strip(), 'keywords': kws,
                            'created': created,
                            'tags': [('merge_attach', 'does', 'data: an item is equipped to a creature')] if v['type'].lower() == 'item' else [],
                            'extra': {k: v[k] for k in ('tokens', 'creators') if v.get(k)}})
    return res
cards = cards_of(cards_f, False) + cards_of(tokens_f, True)
kw = [{'ext_id': 'kw:' + k, 'name': k, 'category': 'keyword', 'source_type': "keyword (Claude's summary of the rule)", 'text': t}
      for k, t in sorted(KW.items())]
races = collections.Counter(s for x in cards for s in x['subtypes'])
tr = [{'ext_id': 'type:' + t, 'name': t, 'category': 'tribe', 'source_type': 'card type / tribe', 'text': f'{t}: {n} entities of this type.'}
      for t, n in sorted(races.items())]
game = {'id': 'tesl', 'name': 'The Elder Scrolls: Legends', 'family': 'The Elder Scrolls: Legends',
        'edition': 'sets up to Houses of Morrowind (2018)', 'source': 'github.com/edipo2s/TESLegendsTracker database/ at commit c541e82 (Apr 2018)',
        'structure': 'Two-player card game with two lanes: the field lane and the shadow lane, where a creature gets Cover (cannot be '
                     'attacked) on the turn it arrives. Each player has 30 health with five runes at 25, 20, 15, 10 and 5; breaking a rune '
                     'draws a card, which may be played for free if it has Prophecy. Magicka grows by 1 each turn. Creatures attack '
                     'creatures in their own lane or the opponent.',
        'notes': "Keyword field from the source; keyword definitions are Claude's summaries. Sets after Houses of Morrowind are missing."}
src = 'TESLegendsTracker dbCards.json + dbTokens.json (c541e82)'
json.dump({'_source': src, '_tag': 'tesl_kw', '_game': game, 'cards': kw + tr}, open(out + '_keywords.json', 'w'), ensure_ascii=False, indent=0)
json.dump({'_source': src, '_tag': 'tesl', '_keywords_from_field': True, 'cards': cards}, open(out + '_cards.json', 'w'), ensure_ascii=False, indent=0)
print('cards', len(cards), 'keywords', len(kw), 'tribes', len(tr))
