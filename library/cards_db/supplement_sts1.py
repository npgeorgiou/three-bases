"""Slay the Spire: entries whose library text is broken.
The library's cards come from the Slay the Spire wiki's Module:Cards/data (library/tools/convert/conv_sts.py) and are whole:
75 cards per character, colorless cards, curses and statuses, with an upgraded form ('Name+') where the upgrade changes more
than numbers; relics, potions, powers (status), monsters, events and Ascension levels come from the game's localization.
Every card of every guide deck in decks.tsv is among them (checked 30 Oct 2026).
Only one text is broken: the power The Bomb kept the game's format strings ("X%1$s turns"); its text here is the card The
Bomb's text with the numbers as X, as every other power is written ("At the start of your turn, gain X Strength").
Writes supplement/sts1.jsonl in the library's entities columns; ids from 7000001 (source.py).
Usage: supplement_sts1.py"""
import json, os, sqlite3
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'supplement', 'sts1.jsonl')
DB = os.path.join(HERE, '..', 'three-bases-library.sqlite')
FIX = {('THEBOMB', 'status'): 'At the end of X turns, deal X damage to ALL enemies.'}
COLS = ['id', 'game', 'ext_id', 'name', 'category', 'source_type', 'edition', 'faction', 'subtypes', 'rarity', 'cost', 'cost_num',
        'stats', 'text', 'extra', 'variants']

c = sqlite3.connect(DB)
out = []
for n, ((ext, cat), text) in enumerate(sorted(FIX.items())):
    r = dict(zip(COLS, c.execute(f"select {','.join(COLS)} from entities where game='sts1' and ext_id=? and category=?", (ext, cat)).fetchone()))
    r.update(id=7000001 + n, text=text, source_type=r['source_type'])
    out.append(r)
with open(OUT, 'w') as f:
    for r in out: f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(f'{len(out)} entries -> {OUT}')
