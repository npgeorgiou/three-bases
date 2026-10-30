"""Slay the Spire: every entry of the game, with the library's broken texts repaired.
Source: the library's sts1 entries (cards from the Slay the Spire wiki's Module:Cards/data via library/tools/convert/conv_sts.py;
relics, potions, powers, monsters, events and Ascension levels from the game's localization). They are whole: 75 cards per
character, colorless cards, curses and statuses, an upgraded form 'Name+' where the upgrade changes more than numbers; every
card of every guide deck in decks.tsv is among them (checked 30 Oct 2026).
What is repaired, each by one rule for every entry (so the supplement holds every entry and replaces the library's, source.py
FULL; cards and their powers share card codes, so a partial supplement would drop one of them):
- Energy icons: the conversion wrote each icon as a word ("Gain energy energy." = 2 energy, Bloodletting; "Sunder ... gain
  energy energy energy" = 3). Runs of the word are counted; a lone icon after "gain" is 1 ("Gain energy." Adrenaline), except
  "gain energy equal to ..." (Recycle).
- Numbers the conversion lost: Genetic Algorithm "Gain Block." and Ritual Dagger "Deal damage." take the number of the same
  sentence in the source's own upgraded_text (extra.upgraded_text: "Gain 1 Block", "Deal 15 damage"; the upgrade changes
  only the other number). Happy Flower, Sundial, Nunchaku: the wiki's Module:Relics/data (read 30 Oct 2026, RELICS below).
- Powers (category status) kept the game's format strings ("X%1$s", "draw X1 card.Whenever ... draw X"): the wiki's
  Module:Powers/data texts (read 30 Oct 2026, POWERS below), markup removed; other powers keep their first sentence group.
  "LocalizedStrings.PERIOD" is a period; a number glued after X ("X2 turns") is that number.
- Keywords the card has itself, written as a sentence of their own (Exhaust., Ethereal., Innate., Retain., Unplayable.), go
  in the Keywords field (PROCESS "A card list that looked whole" 3), so each card takes the keyword's record.
- Powers (the game's statuses, category status) are keywords when a text names them and no glossary keyword or card holds
  them already: Plated Armor, Mark, Hex, Stasis, Surrounded, Metallicize (a potion gives it; category keyword). Left out (glossary terms no card uses,
  PROCESS 0.5): powers that only repeat a glossary keyword (Strength, Weakened = Weak ...), powers that only repeat their
  card's text (Barricade, Demon Form ...), powers no text names (enemy powers such as Curl Up, Thievery), and the glossary
  keywords Opener (a Slay the Spire 2 word) and Vigor, which no text uses.
- One name, two entries (PROCESS "Importing Duelyst" 2): each character's Strike and Defend are "Strike (Ironclad)" ...
  (the wiki's own page names); two monsters of one name take their kind from the game's code ("Louse (defensive)",
  "Slaver (blue)"); the event Golden Idol is "Golden Idol (event)" (the relic keeps the name). A keyword may share a card's
  name (Shiv, Burn, Wound).
- Card kinds (Attack, Skill, Power, Status, Curse; the source's type) are the cards' types: "Whenever you play an Attack" is
  filter type Attack, never Runeterra's category skill.
- A relic with no character takes the character of the relic that "Replaces" it (Pure Water <- Holy Water: Watcher).
- X costs: the conversion wrote them as "-1 energy" (the game's code for X: Whirlwind, Skewer, Malaise ...): "X energy", no
  number, so no "cost 0" filter matches them.
Writes supplement/sts1.jsonl in the library's entities columns; ids from 7000001 in library order (source.py).
Usage: supplement_sts1.py"""
import json, os, re, sqlite3
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'supplement', 'sts1.jsonl')
DB = os.path.join(HERE, '..', 'three-bases-library.sqlite')
COLS = ['id', 'game', 'ext_id', 'name', 'category', 'source_type', 'edition', 'faction', 'subtypes', 'rarity', 'cost', 'cost_num',
        'stats', 'text', 'extra', 'variants']
KEEP_POWERS = {'Plated Armor', 'Mark', 'Hex', 'Stasis', 'Surrounded', 'Metallicize'}
DROP_KEYWORDS = {'Opener', 'Vigor'}
KWS = ['Unplayable', 'Innate', 'Ethereal', 'Retain', 'Exhaust']
RELICS = {  # Module:Relics/data, markup removed
    'Happy Flower': 'Every 3 turns, gain 1 energy.',
    'Sundial': 'Every 3 times you shuffle your draw pile, gain 2 energy.',
    'Nunchaku': 'Every time you play 10 Attacks, gain 1 energy.',
}
POWERS = {  # Module:Powers/data, markup removed (library name -> text)
    'Buffer': 'Prevent the next X times you would lose HP.',
    'Blur': 'Block is not removed at the beginning of your next X turns.',
    'Burst': 'Your next X Skills are played twice this turn.',
    'Collect': 'At the start of your next X turns, put a Miracle+ into your hand.',
    'Corpse Explosion': 'On death, deal damage equal to Max HP X times to ALL enemies.',
    'Dark Embrace': 'Whenever a card is Exhausted, draw X cards.',
    'Double Tap': 'Your next X Attacks are played twice this turn.',
    'Draw Reduction': 'Draw X less cards next turn.',
    'Echo Form': 'The first X cards you play each turn are played twice.',
    'Equilibrium': 'Retain your hand for X turns.',
    'Evolve': 'Whenever you draw a Status card, draw X cards.',
    'Loop': 'At the start of your turn, trigger the passive ability of your next Orb X times.',
    'Magnetism': 'At the start of your turn, add X random Colorless cards into your hand.',
    'Mayhem': 'At the start of your turn, play the top X cards of your draw pile.',
    'Phantasmal': 'Deal Double Damage for the next X turns.',
    'The Bomb': 'At the end of X turns, deal X damage to ALL enemies.',
    'Time Warp': 'Whenever you play a certain number of cards, ends your turn and gains X Strength.',
    'Tools Of The Trade': 'At the start of your turn, draw X cards and discard X cards.',
    'Lock-On': 'Receives 50% more damage from Orbs for X turns.',
    'Vulnerable': 'Receive 50% more damage from Attacks for X turns.',
    'Weakened': 'Attacks deal 25% less damage for X turns.',
    'Frail': 'Gain 25% less Block from cards for X turns.',
    'Barricade': 'Block is not removed at the beginning of your turn.',
    'Back Attack': 'Deals 50% more damage as it is attacking you from behind.',
}
TYPES = {'attack card': 'Attack', 'skill card': 'Skill', 'power card': 'Power', 'status card': 'Status', 'curse card': 'Curse'}


def energy(t):
    t = re.sub(r'\benergy(?: energy)+\b', lambda m: f"{len(m.group(0).split())} energy", t)
    return re.sub(r'\b([Gg]ain) energy\b(?! equal)', r'\1 1 energy', t)


def keywords_field(t):
    found = [k for k in KWS if re.search(rf'(?:^|(?<=\. )){k}(?:\.(?=\s|$)|$)', t)]
    for k in found: t = re.sub(rf'(?:^|(?<=\. )){k}(?:\.(?:\s+|$)|$)', '', t)
    t = t.strip()
    return (f"Keywords: {', '.join(found)}. " + t).strip() if found else t


def repair(r):
    t = (r['text'] or '').replace(' LocalizedStrings.PERIOD', '.').replace('LocalizedStrings.PERIOD', '.')
    if r['category'] == 'spell':
        up = (json.loads(r['extra']) if r['extra'] and r['extra'].startswith('{') else {}).get('upgraded_text', '')
        for pat in (r'^Gain (\d+) Block\.', r'^Deal (\d+) damage\.'):
            m = re.search(pat, up); word = pat.split(' ')[0][1:]
            if m and re.match(rf'^{word} (Block|damage)\.', t): t = re.sub(rf'^{word} ', f'{word} {m.group(1)} ', t)
        t = keywords_field(energy(t))
        r['subtypes'] = TYPES.get(r['source_type'])
        if r['cost'] == '-1 energy': r['cost'], r['cost_num'] = 'X energy', None  # the wiki's module writes an X cost as -1
    elif r['category'] == 'relic' and r['name'] in RELICS:
        t = RELICS[r['name']]
    elif r['category'] == 'status':
        t = POWERS.get(r['name']) or re.split(r'(?<=[a-z0-9.!])\.(?=[A-Z])', t)[0].rstrip('.') + '.'
        t = re.sub(r'\bX(\d)', r'\1', t)  # "revives in X2 turns at X50% HP": the number is written after the X
    else:
        t = energy(t)
    r['text'] = t
    return r


c = sqlite3.connect(DB)
out = []
for n, row in enumerate(c.execute(f"select {','.join(COLS)} from entities where game='sts1' order by id")):
    r = repair(dict(zip(COLS, row)))
    r['id'] = 7000001 + n  # by library order, so ids stay stable whatever is left out
    if r['category'] == 'status':
        if r['name'] not in KEEP_POWERS: continue
        r['category'] = 'keyword'
    if r['category'] == 'keyword' and r['name'] in DROP_KEYWORDS: continue
    out.append(r)
SAME = {}
for r in out:
    if r['category'] != 'keyword': SAME.setdefault(r['name'], []).append(r)
MON = {'FUZZYLOUSEDEFENSIVE': 'defensive', 'FUZZYLOUSENORMAL': 'normal', 'SLAVERBLUE': 'blue', 'SLAVERRED': 'red'}
for n, rs in SAME.items():
    if len(rs) < 2: continue
    for r in rs:
        if r['category'] == 'spell': r['name'] = f"{n} ({r['faction']})"
        elif r['category'] == 'monster': r['name'] = f"{n} ({MON[r['ext_id']]})"
        elif r['category'] == 'event': r['name'] = f'{n} (event)'
by_name = {r['name']: r for r in out}
for r in out:  # "Replaces Pure Water" (Holy Water, Watcher): the relic it replaces is that character's too
    m = re.match(r'Replaces ([^.]+)\.', r['text'] or '')
    if m and r['faction'] and m.group(1) in by_name and not by_name[m.group(1)]['faction']: by_name[m.group(1)]['faction'] = r['faction']
with open(OUT, 'w') as f:
    for r in out: f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(f'{len(out)} entries -> {OUT}')
