"""Duelyst: every card from the open-sourced game (github.com/open-duelyst/duelyst, commit 2843f24, 1 Aug 2025).
Reads the card factories (app/sdk/cards/factory/<set>/*.coffee), the card id list (app/sdk/cards/cardsLookup.coffee) and the
English texts (app/localization/locales/en/*.json) of a checkout, and writes duelyst_cards.psv next to this file, one card per
line: card_id|code|set|class|faction|race|rarity|mana|atk|hp|general|hidden|legacy|name|text|refs|signature
(code = Cards.<Group>.<Name>, the library's ext_id; refs = the other cards the card's code names, e.g. the token it summons; signature = a General's Bloodbound Spell, its signatureCardData).
Usage: conv_duelyst.py <open-duelyst checkout>"""
import glob, json, os, re, sys

ROOT = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'duelyst_cards.psv')
FACTION = {'Faction1': 'Lyonar Kingdoms', 'Faction2': 'Songhai Empire', 'Faction3': 'Vetruvian Imperium',
           'Faction4': 'Abyssian Host', 'Faction5': 'Magmar Aspects', 'Faction6': 'Vanar Kindred', 'Neutral': 'Neutral',
           'Tutorial': 'Tutorial', 'Boss': 'Boss'}
RARITY = {'Fixed': 'fixed', 'Common': 'common', 'Rare': 'rare', 'Epic': 'epic', 'Legendary': 'legendary',
          'TokenUnit': 'tokenunit', 'Mythron': 'mythron'}


def lookup_ids():
    ids, grp = {}, None
    for line in open(os.path.join(ROOT, 'app/sdk/cards/cardsLookup.coffee')):
        g = re.match(r'\s*@(\w+)\s*:\s*\{', line)
        if g:
            grp = g.group(1)
            continue
        k = re.match(r'\s*(\w+)\s*:\s*(\d+)\s*$', line)
        if k and grp:
            ids['Cards.%s.%s' % (grp, k.group(1))] = int(k.group(2))
    return ids


def texts():
    t = {}
    for f in glob.glob(os.path.join(ROOT, 'app/localization/locales/en/*.json')):
        ns = os.path.basename(f)[:-5]
        for k, v in json.load(open(f)).items():
            if isinstance(v, str):
                t[ns + '.' + k] = v
    return t


def text_of(expr, t):
    m = re.search(r'i18next\.t\("([\w.]+)"', expr)
    if m:
        return t.get(m.group(1), '')
    m = re.match(r'\s*"(.*)"\s*$', expr)
    return m.group(1) if m else ''


def main():
    ids, t = lookup_ids(), texts()
    rows, seen = [], set()
    for f in sorted(glob.glob(os.path.join(ROOT, 'app/sdk/cards/factory/*/*.coffee'))):
        cset = f.split('/')[-2] + '/' + os.path.basename(f)[:-7]
        src = open(f).read()
        parts = re.split(r'\n\s*if \(?identifier == (Cards\.\w+\.\w+)\)?\s*\n', src)
        for code, body in zip(parts[1::2], parts[2::2]):
            if code in seen:
                continue
            seen.add(code)
            get = lambda pat: (re.search(pat, body) or [None, ''])[1]
            name = text_of(get(r'card\.name\s*=\s*(.+)'), t)
            desc = text_of(get(r'card\.setDescription\((.+)\)\s*$|card\.setDescription\((.+)\)') or '', t)
            if not desc:
                m = re.search(r'card\.setDescription\((.+)\)', body)
                desc = text_of(m.group(1), t) if m else ''
            refs = sorted(set(re.findall(r'(?<![\w.])Cards\.\w+\.\w+', body)) - {code})
            rows.append([ids.get(code, ''), code, cset, get(r'card = new (\w+)'),
                         FACTION.get(get(r'card\.factionId\s*=\s*Factions\.(\w+)'), ''),
                         get(r'card\.raceId\s*=\s*Races\.(\w+)'), RARITY.get(get(r'card\.rarityId\s*=\s*Rarity\.(\w+)'), ''),
                         get(r'card\.manaCost\s*=\s*(\d+)'), get(r'card\.atk\s*=\s*(\d+)'), get(r'card\.maxHP\s*=\s*(\d+)'),
                         '1' if re.search(r'setIsGeneral\(true\)', body) else '',
                         '1' if re.search(r'setIsHiddenInCollection\(true\)', body) else '',
                         '1' if re.search(r'setIsLegacy\(true\)', body) else '',
                         name, ' '.join(desc.split()), ','.join(refs),
                         get(r'signatureCardData\s*=\s*\{id:\s*(Cards\.\w+\.\w+)')])
    with open(OUT, 'w') as o:
        o.write('card_id|code|set|class|faction|race|rarity|mana|atk|hp|general|hidden|legacy|name|text|refs|signature\n')
        for r in rows:
            o.write('|'.join(str(x).replace('|', '/') for x in r) + '\n')
    print(len(rows), 'cards ->', OUT)


main()
