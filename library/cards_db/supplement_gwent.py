"""Gwent's supplement (supplement/gwent.jsonl): glossary words the gwent.one export (v14.8) has no keyword entry for but card
texts use as a status. Spying: given by Disloyal and Seize (both defined in the export); its meaning from the bluestacks
decks guide (library/games/gwent.md, "# term:" line). Ids from 9000001 (source.py). Also the text-less units other cards make (see below).
Usage: supplement_gwent.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [dict(id=9000001, game='gwent', ext_id='kw:Spying', name='Spying', category='keyword',
             source_type='keyword (bluestacks.com Gwent decks guide; library/games/gwent.md)',
             text='Spying units are played on the opponent\'s side of the board but benefit their owner.')]
# cards named in other cards' texts that the export (v14.8) gives without text, so the library dropped them; no stats are
# known here, so none are written (Endrega Larva was wrongly merged into Nekker by the first build)
for n, (name, by) in enumerate([('Chort', 'Prize-Winning Cow'), ('Old Speartip', 'Old Speartip: Asleep'),
                                ('Elder Bear', 'Bearification'), ('Endrega Larva', 'Koshchey'), ('Treant Mantis: Strike', 'Treant Mantis: Stalk')], start=9000002):
    rows.append(dict(id=n, game='gwent', ext_id='named:' + name, name=name, category='unit', source_type='Unit',
                     edition='non-collectible', text='', created=1,
                     extra=json.dumps({'note': 'named in the text of ' + by + '; a text-less card the gwent.one export lists without ability'})))
with open(os.path.join(HERE, 'supplement', 'gwent.jsonl'), 'w', encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(len(rows), 'rows')
