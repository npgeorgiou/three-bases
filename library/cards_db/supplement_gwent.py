"""Gwent's supplement (supplement/gwent.jsonl): glossary words the gwent.one export (v14.8) has no keyword entry for but card
texts use as a status. Spying: given by Disloyal and Seize (both defined in the export); its meaning from the bluestacks
decks guide (library/games/gwent.md, "# term:" line). Ids from 9000001 (source.py).
Usage: supplement_gwent.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [dict(id=9000001, game='gwent', ext_id='kw:Spying', name='Spying', category='keyword',
             source_type='keyword (bluestacks.com Gwent decks guide; library/games/gwent.md)',
             text='Spying units are played on the opponent\'s side of the board but benefit their owner.')]
with open(os.path.join(HERE, 'supplement', 'gwent.jsonl'), 'w', encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(len(rows), 'rows')
