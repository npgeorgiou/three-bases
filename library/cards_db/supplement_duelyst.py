"""Duelyst: every card from the open-sourced game, and its board tiles as keywords.
Cards: library/tools/convert/duelyst_cards.psv (conv_duelyst.py over github.com/open-duelyst/duelyst commit 2843f24, 1 Aug
2025: the card factories, the card id list and the English texts; 1116 entries). The library's copy (duelyst.json, 793 cards)
lacks the basic cards (Tempest, Phoenix Fire), most tokens (Wraithling) and others the guides' decks use (Mirrorrim, Disciple
of Yggdra), so every card is written here and replaces the library's entry with the same card code (source.py).
Tiles are left out as cards: Shadow Creep, Hallowed Ground, Exhuming Sand and Primal Flourish are the library's keyword
entries (modifiers.json); Mana Spring, which no keyword entry has, is added as one from the game's tips
(app/localization/locales/en/game_tips.json novice_tip_0). Cards with no name (internal helpers) are left out.
Links (supplement/duelyst_links.jsonl): a card generates every other card its factory code names (the token it summons, the
form it transforms into, a General's Bloodbound Spell), and to a tile's keyword entry.
Writes supplement/duelyst.jsonl in the library's entities columns; ids from 5000001 (source.py), kept stable.
Usage: supplement_duelyst.py"""
import csv, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
PSV = os.path.join(HERE, '..', 'tools', 'convert', 'duelyst_cards.psv')
OUT = os.path.join(HERE, 'supplement', 'duelyst.jsonl')
LINKS = os.path.join(HERE, 'supplement', 'duelyst_links.jsonl')
SRC = 'open-duelyst 2843f24 card factories, supplement'
RACE = {'BattlePet': 'Battle Pet'}
TILE_KW = {'Cards.Tile.Shadow': 'kw:Shadow Creep', 'Cards.Tile.Hallowed': 'kw:Hallowed Ground',
           'Cards.Tile.SandPortal': 'kw:Exhuming Sand', 'Cards.Tile.PrimalMojo': 'kw:Primal Flourish',
           'Cards.Tile.BonusMana': 'kw:Mana Spring'}
MOD = 'keyword (open-duelyst app/sdk/modifiers/modifier%s.coffee keywordDefinition, supplement)'
GLOSSARY = [('kw:Mana Spring', 'Mana Spring', 'Occupying a Mana Spring gives you +1 bonus Mana for that turn.',
             'keyword (open-duelyst game_tips.json novice_tip_0, supplement)'),
            ('kw:Intensify', 'Intensify', 'Effect is boosted each time you play it.', MOD % 'Intensify'),
            ('kw:Trial', 'Trial', 'Starts locked in your action bar. Complete the Trial to unlock the ability to play this card.',
             MOD % 'Fate'),
            ('kw:Destiny', 'Destiny', 'Summon to gain a permanent game-changing effect.', MOD % 'OnSummonFromHandApplyEmblems'),
            ('kw:Bloodbound Spell', 'Bloodbound Spell', "Your General's own spell; it counts down each turn until it refreshes.",
             'keyword (open-duelyst tutorial.json lesson_4_bloodborn_instruction_1: "Your Bloodbound Spell counts down each turn '
             'until it refreshes", supplement)')]
# Types: the race (Golem, Mech, ...). Each General's own spell (its signatureCardData) and the cards that replace one (code
# ending BBS) have the keyword Bloodbound Spell, so "your Bloodbound Spell" is a keyword filter, so
# "your Bloodbound Spell" is a type filter


def category(r):
    if r['class'] == 'Unit':
        if r['faction'] == 'Boss': return 'boss'
        return 'leader' if r['general'] else 'unit'  # a General is its player (BRIEF Game words: Duelyst)
    if r['class'] == 'Artifact': return 'item'
    return 'spell'


BBS = set()  # the cards a General's code names: its Bloodbound Spell


def kind(r):
    """what a non-collectible card with a collectible card's name is, for its name"""
    if r['faction'] == 'Tutorial': return 'tutorial'
    if r['faction'] == 'Boss': return 'boss'
    if r['code'].endswith('BBS') or r['code'] in BBS: return 'Bloodbound Spell'
    if 'Followup' in r['code']: return 'follow-up'
    if r['hidden']: return 'token'
    return ''


def names(rows):
    """One name, one card: a card sharing its name with another keeps it when it is the collectible one (shown in the
    collection, not tutorial or boss); the others are "<name> (<kind>)", then "<name> (<kind>, <code name>)" if still shared
    (Tempest and its Bloodbound Spell copy; the 14 Build structures all called Building)."""
    import collections
    by = collections.defaultdict(list)
    for r in rows: by[r['name']].append(r)
    for n, rs in by.items():
        if len(rs) < 2: continue
        keep = [r for r in rs if not kind(r)]
        for r in rs:
            if keep and r is keep[0]: continue
            r['name'] = f"{n} ({kind(r) or 'token'})"
    by = collections.defaultdict(list)
    for r in rows: by[r['name']].append(r)
    for n, rs in by.items():
        if len(rs) > 1:
            for r in rs[1 if not kind(rs[0]) and '(' not in n else 0:]:
                r['name'] = f"{n[:-1] if n.endswith(')') else n + ' ('}{', ' if n.endswith(')') else ''}{r['code'].split('.')[-1]})"


def keywords_field(text, kws):
    """Lines that are only keywords ("Provoke", "Flying", "Airdrop, Forcefield") become the Keywords field, so the card
    inherits the keywords' records (PROCESS "A card list that looked whole" 3); labels ("Opening Gambit:") and keywords with
    a number ("Backstab: (2).") stay in the text."""
    alt = '|'.join(re.escape(k) for k in sorted(kws, key=len, reverse=True))
    only = re.compile(rf'^(?:{alt})(?:\s*,\s*|\s+(?:and\s+)?)?(?:(?:{alt})(?:\s*,\s*|\s+(?:and\s+)?)?)*\.?$', re.I)
    found, rest = [], []
    lead = re.compile(rf'^((?:{alt})(?:\s*,\s*(?:{alt}))*)\.\s+(?=[A-Z])')  # "Forcefield. Your Bloodbound Spell is Tempest."
    for line in text.split('\n'):
        m = lead.match(line.strip())
        if line.strip() and only.match(line.strip()):
            found += [m.group(0) for m in re.finditer(alt, line, re.I)]
        elif m:
            found += [k.group(0) for k in re.finditer(alt, m.group(1), re.I)]
            rest.append(line.strip()[m.end():])
        else:
            rest.append(line)
    canon = {k.lower(): k for k in kws}
    found = list(dict.fromkeys(canon[f.lower()] for f in found))
    body = '\n'.join(rest).strip()
    return (f"Keywords: {', '.join(found)}." + (' ' + body if body else '')) if found else body


def main():
    old = {}
    if os.path.exists(OUT):
        for line in open(OUT):
            e = json.loads(line); old[e['ext_id']] = e['id']
    nxt = max(list(old.values()) + [5000000]) + 1
    rows = [r for r in csv.DictReader(open(PSV), delimiter='|', quoting=csv.QUOTE_NONE)
            if r['name'] and r['class'] != 'Tile']
    BBS.update(r['signature'] for r in rows if r['signature'])
    names(rows)
    import sqlite3
    lib = sqlite3.connect(os.path.join(HERE, '..', 'three-bases-library.sqlite'))
    kw_names = {n for (n,) in lib.execute("select name from entities where game='duelyst' and category='keyword'")}
    kw_names |= {n for _, n, *_ in GLOSSARY}
    out, ids = [], {}
    for r in rows:
        i = old.get(r['code'])
        if i is None: i, nxt = nxt, nxt + 1
        ids[r['code']] = i
        cat = category(r)
        stats = {'attack': r['atk'], 'health': r['hp']} if r['class'] == 'Unit' else None
        extra = {'card_id': int(r['card_id']) if r['card_id'] else None, 'set': r['set']}
        for k in ('hidden', 'legacy'):
            if r[k]: extra[k] = True
        out.append({'game': 'duelyst', 'ext_id': r['code'], 'name': r['name'], 'category': cat,
                    'source_type': f"{r['class']} ({SRC})", 'edition': r['set'].split('/')[0],
                    'faction': r['faction'] or None,
                    'subtypes': json.dumps([RACE.get(r['race'], r['race'])]) if r['race'] else None,
                    'rarity': r['rarity'] or None, 'cost': f"{r['mana']} mana" if r['mana'] else None,
                    'cost_num': float(r['mana']) if r['mana'] else None,
                    'stats': json.dumps(stats) if stats else None,
                    'text': keywords_field(('Bloodbound Spell\n' if r['code'] in BBS or r['code'].endswith('BBS') else '')
                                           + r['text'].replace('\\n', '\n'), kw_names),
                    'extra': json.dumps(extra), 'variants': None, 'id': i})
    for code, name, text, st in GLOSSARY:
        i = old.get(code)
        if i is None: i, nxt = nxt, nxt + 1
        ids[code] = i
        out.append({'game': 'duelyst', 'ext_id': code, 'name': name, 'category': 'keyword', 'source_type': st,
                    'edition': None, 'faction': None, 'subtypes': None, 'rarity': None, 'cost': None, 'cost_num': None,
                    'stats': None, 'text': text, 'extra': None, 'variants': None, 'id': i})
    open(OUT, 'w').write(''.join(json.dumps(e) + '\n' for e in out))
    # links to the library's keyword entries go by their ids there
    kw = {x: i for x, i in lib.execute("select ext_id, id from entities where game='duelyst' and ext_id like 'kw:%'")}
    kw.update({k: ids[k] for k, *_ in GLOSSARY})
    links = []
    for r in rows:
        for ref in filter(None, r['refs'].split(',')):
            dst = ids.get(ref) or kw.get(TILE_KW.get(ref, ''))
            if dst and dst != ids[r['code']]:
                links.append({'src': ids[r['code']], 'rel': 'generates', 'dst': dst, 'evidence': 'open-duelyst factory code'})
    open(LINKS, 'w').write(''.join(json.dumps(l) + '\n' for l in links))
    print(len(out), 'entries,', len(links), 'links')


main()
