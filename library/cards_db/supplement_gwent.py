"""Gwent's supplement (supplement/gwent.jsonl): glossary words the gwent.one export (v14.8) has no keyword entry for but card
texts use as a status. Spying: given by Disloyal and Seize (both defined in the export); its meaning from the bluestacks
decks guide (library/games/gwent.md, "# term:" line). Ids from 9000001 (source.py). Also the text-less units other cards make (see below).
Usage: supplement_gwent.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [dict(id=9000001, game='gwent', ext_id='kw:Spying', name='Spying', category='keyword',
             source_type='keyword (bluestacks.com Gwent decks guide; library/games/gwent.md)',
             text='Spying units are played on the opponent\'s side of the board but benefit their owner.')]
# cards other cards make that the gwent.one export (v14.8) lists without ability text, so the library dropped them; stats from
# their gwent.one card pages (game version 14.10.0, fetched 6 Nov 2026; armor only where the page lists it). Endrega Larva has the same text as Nekker, and the
# first build wrongly merged the two by text.
SRC = 'gwent.one card page, game version 14.10.0, fetched 6 Nov 2026: '
for n, (name, by, url, fac, cat, prov, power, armor, text) in enumerate([
        ('Chort', 'Prize-Winning Cow', 'https://gwent.one/en/card/200320', 'Neutral', 'Relict', 6, 10, 0, ''),
        ('Old Speartip', 'Old Speartip: Asleep', 'https://gwent.one/en/card/132408', 'Monster', 'Ogroid', 10, 12, 0, ''),
        ('Elder Bear', 'Bearification', 'https://gwent.one/en/card/152405', 'Neutral', 'Beast', 4, 5, 0, ''),
        ('Endrega Larva', 'Koshchey', 'https://gwent.one/en/card/202440', 'Monster', 'Insectoid', 5, 2, 1,
         'Thrive. Deploy: Spawn a base copy of self on this row.'),
        ('Treant Mantis: Strike', 'Treant Mantis: Stalk', 'https://gwent.one/en/card/202293', "Scoiatael", 'Treant', 6, 6, 0, '')],
        start=9000002):
    rows.append(dict(id=n, game='gwent', ext_id='named:' + name, name=name, category='unit', source_type='Unit',
                     edition='non-collectible', faction=fac, subtypes=json.dumps([cat]), cost=f'{prov} provisions',
                     cost_num=float(prov), stats=json.dumps({'power': power, 'armor': armor} if armor else {'power': power}), text=text, created=1,
                     extra=json.dumps({'source': SRC + url, 'made_by': by})))
# collectible cards the gwent.one export (v14.8) lacks that playgwent deck guides use (Kaptain, 10 Nov 2026: add them so the
# decks can go in); text, stats and faction from their gwent.one card pages (game version 14.10.0, fetched 10 Nov 2026); ext_id
# = the card's gwent.one id
for n, (gid, name, cat, stype, fac, subs, rar, color, prov, power, armor, text) in enumerate([
        ('202397', 'Knickers', 'unit', 'Unit', 'Neutral', ['Beast', 'Bandit'], 'legendary', 'Gold', 8, 3, 1,
         'This unit may raid the battlefield to aid you in battle.'),
        ('132212', 'Ice Giant', 'unit', 'Unit', 'Monster', ['Ogroid'], 'common', 'Bronze', 5, 7, 0, ''),
        ('122301', 'Ballista', 'unit', 'Unit', 'Northern Realms', ['Machine', 'Siege Engine'], 'common', 'Bronze', 4, 4, 0,
         'Deploy: Damage an enemy unit by 1. Order: Damage an enemy unit by 2.'),
        ('201634', "Bekker's Rockslide", 'spell', 'Special', 'Neutral', ['Spell'], 'epic', 'Gold', 7, None, None, 'Damage a unit by 8.'),
        ('113306', 'Manticore Venom', 'spell', 'Special', 'Neutral', ['Organic'], 'epic', 'Gold', 8, None, None,
         'Damage 3 enemy units by 3.')], start=9000007):
    st = None if power is None else json.dumps({'power': power, 'armor': armor} if armor else {'power': power})
    rows.append(dict(id=n, game='gwent', ext_id=gid, name=name, category=cat, source_type=stype, edition='BaseSet', faction=fac,
                     subtypes=json.dumps(subs), rarity=rar, cost=f'{prov} provisions', cost_num=float(prov), stats=st, text=text,
                     extra=json.dumps({'color': color, 'source': f'gwent.one card page, game version 14.10.0, fetched 10 Nov 2026: https://gwent.one/en/card/{gid}'})))
with open(os.path.join(HERE, 'supplement', 'gwent.jsonl'), 'w', encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(len(rows), 'rows')
