"""Star Wars: Unlimited -> two load files (format in load_cards.py): <out>_keywords.json (keywords, traits) and <out>_cards.json.
Source: sets/<set>.json of github.com/Yannick101984/swucardex-data at commit a86faed (20 Oct 2026), an export of the official
card database (French records with every localisation): SOR, SHD, TWI, JTL, LOF, SEC, LAW, ASH and the Intro Battle: Hoth set.
- Text, title, deployed side and epic action come from the English localisation; a card listed as a reprint is left out.
- Keyword names: the export names them in French; each was matched to the English word found on the English text of every
  card that has it (Sentinelle -> Sentinel on 165 of 165 cards, and so on: KW below). Definitions are the most common reminder text the
  English cards print (with that card's numbers, e.g. Raid 1), else Claude's summary (source_type says which).
- Aspects (French in the export) map to the English aspect names (ASP). Faction: the card's colour aspect (Vigilance, Command,
  Aggression, Cunning; two joined with '-'), else its alignment (Heroism, Villainy), else Neutral; all aspects in extra.aspects.
- Traits (French in the export) are translated by Claude (TRAIT) and become tribes.
- Category: Unit unit, Event spell, Upgrade item, Leader hero, Base building, Token created unit or item.
Usage: conv_swu.py <out> <set.json> [<set.json> ...]"""
import collections, json, re, sys
out, files = sys.argv[1], sys.argv[2:]
KW = {'Sentinelle': 'Sentinel', 'Débordement': 'Overwhelm', 'Raid': 'Raid', 'Embuscade': 'Ambush', 'Récupération': 'Restore',
      'Saboteur': 'Saboteur', 'Protégée': 'Shielded', 'Dissimulée': 'Hidden', 'Aplomb': 'Grit', 'Pilotage': 'Piloting',
      'Contrebande': 'Smuggle', 'Prime': 'Bounty', 'Complot': 'Plot', 'Soutien': 'Support', 'Valorisation': 'Exploit',
      'Coordination': 'Coordinate'}
SUMMARY = {  # Claude's summaries, used only where no card prints a reminder text
 'Sentinel': 'Enemy units in its arena must attack a unit with Sentinel if able.', 'Overwhelm': 'When it defeats a unit, the excess damage is dealt to the opponent\'s base.',
 'Raid': 'It gets +N power while attacking.', 'Ambush': 'When played, it may ready and attack an enemy unit.', 'Restore': 'When it attacks, heal N damage from your base.',
 'Saboteur': 'When it attacks, it ignores Sentinel and defeats the defender\'s shields.', 'Shielded': 'When played, it gets a Shield token.',
 'Grit': 'It gets +1 power for each damage on it.', 'Coordinate': 'It has this ability while you control 3 or more units.',
 'Piloting': 'It may be played as an upgrade on a friendly Vehicle unit without a Pilot, for its Piloting cost.',
 'Smuggle': 'It may be played from your resources for its Smuggle cost; replace it with the top card of your deck.', 'Bounty': 'When it is defeated or captured, the opponent collects the bounty.'}
ASP = {'Infâmie': 'Villainy', 'Héroïsme': 'Heroism', 'Ruse': 'Cunning', 'Commandement': 'Command', 'Vigilance': 'Vigilance', 'Agressivité': 'Aggression'}
COLOUR = ['Vigilance', 'Command', 'Aggression', 'Cunning']
TRAIT = {'Véhicule': 'Vehicle', 'Pègre': 'Underworld', 'Impérial': 'Imperial', 'Force': 'Force', 'Rebelle': 'Rebel', 'Soldat': 'Trooper',
         'Chasseur': 'Fighter', 'République': 'Republic', 'Officiel': 'Official', 'Tactique': 'Tactic', 'Transport': 'Transport', 'Frange': 'Fringe',
         'Jedi': 'Jedi', 'Séparatiste': 'Separatist', 'Droïde': 'Droid', 'Chasseur De Primes': 'Bounty Hunter', 'Mandalorien': 'Mandalorian',
         'Vaisseau Capital': 'Capital Ship', 'Créature': 'Creature', 'Objet': 'Item', 'Inné': 'Innate', 'Pilote': 'Pilot', 'Arme': 'Weapon',
         'Plan': 'Plan', 'Astuce': 'Trick', 'Sith': 'Sith', 'Résistance': 'Resistance', 'Clone': 'Clone', 'Acquis': 'Learned', 'Réserve': 'Supply',
         'Gambit': 'Gambit', 'Spectre': 'Spectre', 'Premier Ordre': 'First Order', 'Marcheur': 'Walker', 'Condition': 'Condition',
         'Nouvelle République': 'New Republic', 'Wookie': 'Wookiee', 'Nuit': 'Night', 'Loi': 'Law', 'Speeder': 'Speeder', 'Naboo': 'Naboo',
         'Sabre Laser': 'Lightsaber', "Twi'lek": "Twi'lek", 'Tank': 'Tank', 'Armure': 'Armor', 'Désastre': 'Disaster', 'Inquisiteur': 'Inquisitor',
         'Prime': 'Bounty', 'Modification': 'Modification', 'Hutt': 'Hutt', 'Nihil': 'Nihil', 'Ewok': 'Ewok', 'Mort-vivant': 'Undead',
         'Kaminoen': 'Kaminoan', 'Gungan': 'Gungan', 'Musicien': 'Musician', 'Tusken': 'Tusken', 'Jawa': 'Jawa'}
CAT = {'Unit': 'unit', 'Event': 'spell', 'Upgrade': 'item', 'Leader': 'hero', 'Base': 'building'}
names = lambda rel: [x['attributes']['name'] for x in (rel or {}).get('data') or []]
cards, rem, untrans = [], collections.defaultdict(collections.Counter), collections.Counter()
for f in files:
    for rec in json.load(open(f, encoding='utf-8'))['data']:
        a = rec['attributes']
        if (a.get('reprintOf') or {}).get('data'): continue
        en = [l['attributes'] for l in a['localizations']['data'] if l['attributes']['locale'] == 'en']
        if not en: continue
        e = en[0]; typ = a['type']['data']['attributes']['value']
        typ2 = ((a.get('type2') or {}).get('data') or {}).get('attributes', {}).get('value')
        parts = [e.get('text')] + ([f"Deployed: {e['deployBox']}"] if e.get('deployBox') else []) + ([f"Epic Action: {e['epicAction']}"] if e.get('epicAction') else [])
        text = '\n'.join(p.strip() for p in parts if p and p.strip())
        kws = [KW[k] for k in names(a['keywords']) if k in KW]
        for k in kws:
            m = re.search(r'\b' + k + r'(?: \d+)?\s*\(([^)]*)\)', text)
            if m: rem[k][m.group(1).strip()] += 1
        asp = [ASP.get(x, x) for x in names(a['aspects']) + names(a.get('aspectDuplicates'))]
        col = sorted({x for x in asp if x in COLOUR}, key=COLOUR.index)
        fac = '-'.join(col) if col else next((x for x in asp if x in ('Heroism', 'Villainy')), 'Neutral')
        tr = []
        for t in names(a['traits']):
            if t in TRAIT: tr.append(TRAIT[t])
            else: untrans[t] += 1
        token = typ == 'Token' or 'Token' in (typ2 or '')
        cat = CAT.get(typ2 if typ == 'Token' and typ2 else typ) or ('item' if 'Upgrade' in (typ2 or '') else 'unit')
        stats = {k: v for k, v in [('power', a.get('power')), ('hp', a.get('hp')), ('upgrade_power', a.get('upgradePower')), ('upgrade_hp', a.get('upgradeHp'))] if v is not None}
        name = e['title'] + (f" - {e['subtitle']}" if e.get('subtitle') else '')
        cards.append({'ext_id': a.get('cardUid') or rec['id'], 'name': name, 'category': cat, 'source_type': (typ2 or typ).lower(),
                      'edition': a['expansion']['data']['attributes']['code'], 'faction': fac, 'subtypes': tr,
                      'rarity': names({'data': [a['rarity']['data']]})[0] if (a.get('rarity') or {}).get('data') else None,
                      'cost': None if a.get('cost') is None else str(a['cost']), 'stats': stats or None, 'text': text, 'keywords': kws, 'created': token,
                      'tags': [('merge_attach', 'does', 'data: an upgrade is attached to a unit')] if cat == 'item' else [],
                      'extra': {'aspects': asp, 'arenas': names(a.get('arenas')), 'unique': bool(a.get('unique'))}})
kw = []
for k in sorted(set(KW.values())):
    if rem[k]: kw.append({'ext_id': 'kw:' + k, 'name': k, 'category': 'keyword', 'source_type': 'keyword (reminder text printed on the cards)', 'text': rem[k].most_common(1)[0][0]})
    else: kw.append({'ext_id': 'kw:' + k, 'name': k, 'category': 'keyword', 'source_type': "keyword (Claude's summary of the rule)", 'text': SUMMARY.get(k)})
tribes = collections.Counter(s for x in cards for s in x['subtypes'])
trb = [{'ext_id': 'type:' + t, 'name': t, 'category': 'tribe', 'source_type': 'card type / tribe', 'text': f'{t}: {n} entities of this type.'} for t, n in sorted(tribes.items())]
game = {'id': 'swu', 'name': 'Star Wars: Unlimited', 'family': 'Star Wars: Unlimited', 'edition': 'sets SOR to ASH and Intro Battle: Hoth',
        'source': 'github.com/Yannick101984/swucardex-data sets/*.json at commit a86faed (export of the official card database)',
        'structure': 'Two-player card game. Each player has a leader and a base with health; units are played into one of two arenas, '
                     'ground and space, and attack enemy units in the same arena or the enemy base; the first base destroyed loses. '
                     'Players take actions in turn and pass; any card can be played face down as a resource. The leader can deploy as a unit.',
        'notes': "Keyword and trait names translated from the French export (keywords checked against the English texts); keyword "
                 "definitions are printed reminder text where cards have one, else Claude's summary."}
src = 'swucardex-data sets (a86faed)'
json.dump({'_source': src, '_tag': 'swu_kw', '_game': game, 'cards': kw + trb}, open(out + '_keywords.json', 'w'), ensure_ascii=False, indent=0)
json.dump({'_source': src, '_tag': 'swu', '_keywords_from_field': True, '_strip_reminder': True, 'cards': cards}, open(out + '_cards.json', 'w'), ensure_ascii=False, indent=0)
print('cards', len(cards), 'keywords', len(kw), [k['name'] for k in kw if 'summary' in k['source_type']], 'tribes', len(trb), 'untranslated traits', dict(untrans))
