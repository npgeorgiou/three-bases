"""Monster Train: every card, the champions' upgrade paths and the wiki's glossary of effects and triggers.
Sources (all from the Monster Train fandom wiki, monster-train.fandom.com, Monster Train 1 with The Last Divinity):
- Cards: library/sources/monster_train_cards.psv, the wiki's Module:Cards/Data (revision of 19 Jan 2024) flattened to
  one line per card on 20 Oct 2026 (format in conv_monster_train.py): 282 cards, the six clans and clanless cards. The
  library has only 272 of them, so every card is written here and replaces the library's entry with the same name.
  That flattening lost some numbers ({{Value|n|X Cost|Icon}}, lower-case {{value}}) and the <hr> between a card's versions;
  RAW below holds those cards' descriptions as the module has them (read 28 Oct 2026), flattened here by flat().
- Champions: the module has no text for them. supplement/monster_train_champions.psv: each champion page's Upgrades table
  (champion#path#level I#level II#level III), read 28 Oct 2026, sha256 7410231...
- Glossary: supplement/monster_train_glossary.psv: the tables of the pages Status Effects and Card Effects
  (page#section#name#description), read 28 Oct 2026 (first 85 lines, sha256 ffbe989...); the last line, Charged Echo, is the
  page Charged Echoes in the wiki's words, shortened.
- Tokens the module lacks: Twin of Wax and Mote of Wax (made by Legion of Wax), from the {{Card}} boxes on the wiki page
  Legion of Wax, read 29 Oct 2026 (TOKENS below; the page gives no type or rarity).
- Olde Magic has no text: its effects are chosen in a run (wiki: Concealed Caverns, Arcane Machine). Demon Fiend, Shadowsiege
  and Train Steward are units without text.
Writes supplement/monster_train.jsonl in the library's entities columns; ids from 2000001 (source.py), kept stable for
entries already in the file.
Usage: supplement_monster_train.py"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'supplement', 'monster_train.jsonl')
CARDS = os.path.join(HERE, '..', 'sources', 'monster_train_cards.psv')
CHAMPS = os.path.join(HERE, 'supplement', 'monster_train_champions.psv')
GLOSS = os.path.join(HERE, 'supplement', 'monster_train_glossary.psv')
WIKI = 'Monster Train fandom wiki'
RAW = {
    'Kindle': "'''Consume.'''<br>Gain {{Value|2|X Cost|Ember}}.",
    'Prism Retrieval': "'''Consume.'''<br>Draw a unit and apply {{Value|+5|X Cost|Attack}} and {{Value|-|X Cost|Ember}}.",
    'Waxen Spike': "'''Consume.'''<br>Apply {{Value|+4|X Cost|Attack}} and '''Burnout 4''' to friendly units.",
    'Bone Rattler': "'''Consume.'''<br>Apply {{Value|+5|X Cost|Attack}} to your Pyre.",
    'Gift of Gratitude': "'''Purge.'''<br>Gain {{Value|40|X Cost|Gold}}.",
    'Forgotten Trade': "'''Consume'''.<br>Gain {{value|1|Ember}} per [Echo].",
    'Eternal Kinstone': "Add {{value|1|Echo}} that cannot be removed.",
    'Blazing Bolts': "'''Purge.'''<br>Deal 30 damage to the front enemy unit. Add a stronger version of this card to your discard."
                     "<hr>'''Purge.'''<br>Deal 30 damage to a random unit, two times. Add a stronger version of this card to "
                     "your discard.<hr>Deal 30 damage to a random unit, four times.",
    'Spikedriver Colony': "'''Multistrike 1.'''<br>'''Extinguish:''' Add a permanent copy of this card to your discard pile."
                          "<hr>{{Value|+20|Attack}} and remove '''Extinguish.'''",
}
TOKENS = [('Twin of Wax', "'''Extinguish:''' Summon 2 '''Mote of Wax.''' '''Enhance''' them with all enhancements and card upgrades on this unit.", '2', '4', '4'),
          ('Mote of Wax', '', '1', '2', '2')]
# Glossary terms no card of the game uses (enemy, artifact and run terms), and "Add", which the wiki marks as its own word
# for the verb "add a card", not the game's: left out, so card texts are not linked to them.
UNUSED = {'Add', 'Cardless', 'Haste', 'Hellborne Harvest', 'Heartless', 'Immobile', 'Intrinsic', 'Purify', 'Recover',
          'Relentless', 'Spell Shield', 'Spellchain'}
ICON = {'X Cost': 'X', 'Echo': 'Echo', 'EchoSlot': 'Echo slot', 'Attack': 'Attack', 'Health': 'Health', 'Ember': 'Ember',
        'Capacity': 'Capacity', 'Gold': 'Gold', 'Pyre Health': 'Pyre health'}


def value(m):
    parts = m.group(1).split('|')
    n, icons = parts[0], parts[1:]
    if icons and icons[0] == 'X Cost':  # a number per X Ember spent
        rest = ' '.join(ICON.get(i, i) for i in icons[1:])
        if n in ('', '-', '+'): return f'{n}X {rest}'.strip()
        return f'{n} {rest} per X'.replace('  ', ' ') if rest else f'{n} per X'
    return ' '.join(x for x in [n] + [ICON.get(i, i) for i in icons] if x)


def flat(s):
    s = re.sub(r'\{\{[Vv]alue\|([^}]*)\}\}', value, s)
    s = re.sub(r'<!--.*?-->', '', s)
    s = s.replace("'''", '').replace("''", '')
    s = re.sub(r'<hr\s*/?>', ' / Next version: ', s)
    s = re.sub(r'<br\s*/?>', ' / ', s)
    return clean(s)


def clean(s):
    """Icons written as [Name] in the module's text, and spacing."""
    s = re.sub(r'\[(X Cost|Echo|EchoSlot|Attack|Health|Ember|Capacity|Gold)\]', lambda m: ICON[m.group(1)], s)
    s = re.sub(r'\{\{(Echo|EchoSlot)\}\}', lambda m: ICON[m.group(1)], s)
    s = s.replace('24px|link=|', '')
    return ' '.join(s.split())


ROMAN = ['I', 'II', 'III']


def path_text(path, levels):
    """One upgrade path: numbers per level as a/b/c when the three levels have the same wording, else each level."""
    levels = [clean(x) for x in levels]
    skel = [re.sub(r'[+-]?\d+', '#', x) for x in levels]
    if len(set(skel)) == 1:
        nums = [re.findall(r'[+-]?\d+', x) for x in levels]
        it = iter(range(len(nums[0])))
        def rep(_):
            k = next(it); vals = [n[k] for n in nums]
            if len(set(vals)) == 1: return vals[0]
            sign = vals[0][0] if vals[0][0] in '+-' else ''
            return sign + '/'.join(v.lstrip('+') for v in vals)
        return f'{path} path (upgrades I/II/III): ' + re.sub(r'[+-]?\d+', rep, levels[0])
    return f'{path} path: ' + ' '.join(f'Upgrade {ROMAN[i]}: {x}' for i, x in enumerate(levels))


def main():
    old = {}
    if os.path.exists(OUT):
        for line in open(OUT):
            r = json.loads(line); old[r['ext_id']] = r['id']
    nxt = max(list(old.values()) + [2000000]) + 1
    rows = []
    def add(r):
        nonlocal nxt
        if r['ext_id'] in old: r['id'] = old[r['ext_id']]
        else: r['id'] = nxt; nxt += 1
        rows.append(r)
    paths = {}
    for ln in open(CHAMPS, encoding='utf-8'):
        p = ln.rstrip('\n').split('#')
        if len(p) == 5: paths.setdefault(p[0], []).append(path_text(p[1], p[2:]))
    for ln in open(CARDS, encoding='utf-8'):
        p = ln.rstrip('\n').split('|')
        name, clan, typ, rar, cost, cap, atk, hp, tags, desc, ess = p[:11]
        desc = flat(RAW[name]) if name in RAW else clean(desc)
        cat = 'spell' if typ in ('Spell', 'Blight', 'Scourge') else 'hero' if typ == 'Champion' else 'unit'
        sub = [typ] if typ in ('Blight', 'Scourge') else [] if cat != 'unit' else typ.split()
        if cat == 'hero':
            assert name in paths, name
            desc = ' / '.join(([desc] if desc else []) + paths[name])
        stats = {k: v for k, v in [('capacity', cap), ('attack', atk), ('health', hp)] if v}
        extra = {k: v for k, v in [('essence', clean(ess)), ('tags', [t.strip() for t in tags.split(',') if t.strip()])] if v}
        cn = float(cost) if re.fullmatch(r'\d+', cost or '') else None
        add({'game': 'monster_train', 'ext_id': name, 'name': name, 'category': cat,
             'source_type': f'{typ.lower()} ({WIKI} Module:Cards/Data, supplement)', 'edition': None, 'faction': clan,
             'subtypes': json.dumps(sub) if sub else None, 'rarity': rar or None, 'cost': cost or None, 'cost_num': cn,
             'stats': json.dumps(stats) if stats else None, 'text': desc or None,
             'extra': json.dumps(extra, ensure_ascii=False) if extra else None, 'variants': None})
    for name, desc, cap, atk, hp in TOKENS:
        add({'game': 'monster_train', 'ext_id': name, 'name': name, 'category': 'unit',
             'source_type': f'unit token ({WIKI} page Legion of Wax, supplement)', 'edition': None, 'faction': 'Melting Remnant',
             'subtypes': None, 'rarity': None, 'cost': None, 'cost_num': None,
             'stats': json.dumps({'capacity': cap, 'attack': atk, 'health': hp}), 'text': flat(desc) or None, 'extra': None, 'variants': None})
    assert len(paths) == 12 and sum(r['category'] == 'hero' for r in rows) == 12
    for ln in open(GLOSS, encoding='utf-8'):
        p = ln.rstrip('\n').split('#')
        if len(p) != 4 or p[2].startswith('{{'): continue  # the X Cost row of Card Effects is an icon, not a term
        if p[2] in UNUSED: continue
        page, sec, name, text = p
        add({'game': 'monster_train', 'ext_id': 'kw:' + name, 'name': name, 'category': 'keyword',
             'source_type': f'{sec.lower()} ({WIKI} {page}, supplement)', 'edition': None, 'faction': None, 'subtypes': None,
             'rarity': None, 'cost': None, 'cost_num': None, 'stats': None, 'text': flat(text), 'extra': None, 'variants': None})
    with open(OUT, 'w') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(len(rows), 'entries:', sum(r['category'] != 'keyword' for r in rows), 'cards,',
          sum(r['category'] == 'keyword' for r in rows), 'glossary terms')


if __name__ == '__main__':
    main()
