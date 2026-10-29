"""Faeria: the cards the library lacks, from the game's own card export, and the glossary terms it lacks.
Cards: Abrakam's public repository github.com/abrakam/Faeria_Cards (commit 12b7207 "Gagana's new cards"), files
CardExport/merlin_shortened.csv (462 cards: card_id;color;card_name;card_type;card_subtype;faeria;wild_land;lake;forest;
mountain;desert;power;life;codex_id;rarity) and CardExport/English/cards.csv (<id>.name / <id>.text), copied to
library/tools/convert/faeria_merlin_shortened.csv and faeria_cards_english.csv (sha256 9199d280... and 96d3ada5...).
The library holds 443 of these cards from the same export, so only the cards it lacks, and the cards whose library text
differs from render() (choices of 3 or 4 options kept the markup "{green.|..."; land icons were written "lake lake" for two
lakes), are written here; they replace the library's entry.
Glossary: the repository README's function list and faeria.com's Keyword Rulings guide (Abrakam's own definitions); a term
is written only when cards use it and the library has no keyword entry for it.
Writes supplement/faeria.jsonl in the library's entities columns; ids from 3000001 (source.py).
Usage: supplement_faeria.py"""
import csv, json, os, re, sqlite3
HERE = os.path.dirname(os.path.abspath(__file__))
CONV = os.path.join(HERE, '..', 'tools', 'convert')
OUT = os.path.join(HERE, 'supplement', 'faeria.jsonl')
LIB = os.path.join(HERE, '..', 'three-bases-library.sqlite')
SRC = 'Abrakam Faeria_Cards CardExport (github.com/abrakam/Faeria_Cards 12b7207), supplement'
README = 'Abrakam Faeria_Cards README function list (github.com/abrakam/Faeria_Cards), supplement'
CAT = {'creature': 'unit', 'event': 'spell', 'structure': 'building'}
FAC = {'HUMAN': 'Neutral (Human)', 'BLUE': 'Blue', 'GREEN': 'Green', 'RED': 'Red', 'YELLOW': 'Yellow', 'PANDORA': 'Pandora'}
LANDS = ['wild land', 'lake', 'forest', 'mountain', 'desert']
RULINGS = 'faeria.com Keyword Rulings guide (https://www.faeria.com/the-hub/guide/443-keyword-rulings), supplement'
GLOSSARY = [  # (name, code, definition, source): terms cards use that the library has no keyword entry for
    ('Wild', 'kw:wild', 'A card is wild when all the lands it requires are wild: any land colours pay them, and a wild '
                        'creature can be summoned on any of your lands, including prairies.', README + '; ' + RULINGS),
    ('Fight', 'kw:fight', 'Your creature exchanges attacks with an enemy creature anywhere on the board; this does not count '
                          "as the creature's attack for the turn.", RULINGS),
    ('Teleport', 'kw:teleport', "Moves a creature to another tile; this does not count as the creature's movement for the "
                                'turn.', RULINGS),
    ('Transform', 'kw:transform', "Turns a creature into another; its stats return to the new card's printed values "
                                  '(buffs and damage are removed); it is not a summon.', RULINGS),
]
LAND = {'blue': 'lake', 'green': 'forest', 'red': 'mountain', 'yellow': 'desert'}
NAMES = {'ranged_attack': 'Ranged Attack', 'last_words': 'Last Words', 'wild': 'wild land'}


def lands(m):
    """land icons: one is its name ("Create forest"), several the same are counted ("{blue}{blue}" -> "2 lakes")"""
    cs = re.findall(r'\w+', m[0])
    if len(cs) > 1 and len(set(cs)) == 1: return f'{len(cs)} {LAND[cs[0]]}s'
    return ' '.join(LAND[c] for c in cs)


def render(t):
    """The export's markup as the library writes it: {gift} -> Gift, {charge|3} -> Charge 3, {faeria|2} -> 2 faeria."""
    t = t.replace('\\n', '\n').replace('<b>', '').replace('</b>', '')
    t = re.sub(r'(?:\{(?:blue|green|red|yellow)\})+', lands, t)
    t = re.sub(r'\{dynamic_number\|[^}]*\}', 'X', t)  # a counter the card shows in play; its text says what it counts
    t = re.sub(r'\{faeria\|(\d+)\}', r'\1 faeria', t)
    t = re.sub(r'\{(\w+)\}', lambda m: NAMES.get(m[1], m[1].replace('_', ' ').title()), t)
    t = re.sub(r'\{options\|([^{}]*)\}', lambda m: 'Choose one: ' + ' / '.join(o.strip().rstrip('.') for o in m[1].split('|')) + '.', t)
    t = t.replace('., ', ', ')
    t = re.sub(r'\{(\w+)\|([^}]*)\}', lambda m: f"{NAMES.get(m[1], m[1].replace('_', ' ').title())} {m[2]}", t)
    return t.strip()


def main():
    text = {}
    for line in open(os.path.join(CONV, 'faeria_cards_english.csv'), encoding='utf-8'):
        k, _, v = line.rstrip('\n').partition(';')
        i, _, f = k.partition('.')
        text.setdefault(i, {})[f] = v
    lib = sqlite3.connect(LIB)
    have = dict(lib.execute("select ext_id, text from entities where game='faeria'"))
    out, nid = [], 3000001
    for r in csv.reader(open(os.path.join(CONV, 'faeria_merlin_shortened.csv'), encoding='utf-8'), delimiter=';'):
        cid, color, name, kind, sub, faeria = r[:6]
        if cid in have and have[cid] == (render(text[cid].get('text', '')) or None):
            continue
        lands = {LANDS[i]: int(v) for i, v in enumerate(r[6:11]) if v}
        cost = ', '.join([f'{faeria} faeria'] + [f'{v} {k}' for k, v in lands.items()])
        stats = None
        if kind != 'event':
            stats = json.dumps({'attack': int(r[11] or 0), 'life': int(r[12] or 0)})
        out.append({'id': nid, 'game': 'faeria', 'ext_id': cid, 'name': text[cid]['name'], 'category': CAT[kind],
                    'source_type': f'{kind} ({SRC})', 'edition': None, 'faction': FAC[color],
                    'subtypes': json.dumps([sub]) if sub else None, 'rarity': r[14].lower(), 'cost': cost,
                    'cost_num': float(faeria), 'stats': stats, 'text': render(text[cid].get('text', '')) or None,
                    'extra': json.dumps({'land_requirements': lands}) if lands else None, 'variants': None})
        nid += 1
    for name, code, d, src in GLOSSARY:
        if code not in have:
            out.append({'id': nid, 'game': 'faeria', 'ext_id': code, 'name': name, 'category': 'keyword',
                        'source_type': f'keyword (definition: {src})', 'edition': None, 'faction': None,
                        'subtypes': None, 'rarity': None, 'cost': None, 'cost_num': None, 'stats': None, 'text': d,
                        'extra': None, 'variants': None})
            nid += 1
    with open(OUT, 'w', encoding='utf-8') as f:
        for e in out:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    print(len(out), 'entries ->', OUT)


if __name__ == '__main__':
    main()
