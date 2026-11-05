"""Marvel Snap: every card of the game's card list, and the keywords with definitions from the game's sources.
Why: the library's 699 Marvel Snap units came from an older copy of the same export (5 Oct 2026) and are not usable as
cards: cards with the same text were merged (dedupe, 49 entries: Groot, Wong, Hawkeye, Scarlet Witch, Rocket Raccoon ...),
so every card is written here and source.py FULL replaces all the library's Marvel Snap units, keywords and game rules.
The library's 212 locations (marvelsnapzone.com list, copied by Kaptain on 11 Oct 2026) and 12 tribes stay as they are.
Cards: library/sources/marvel_snap_cards.json = cards.json of github.com/ineffectivecoder/snap-dossier commit a23b31f
(2 Nov 2026), a marvelsnapzone.com export (getinfo searchtype=cards); 748 cards, sha256 29464b718b664ced...
Each card: ext_id = the game's carddefid; name and text with the export's markup removed; cost N energy; stats power.
What a card is (Claude's, from the export's fields):
- collectible: the export names its source (Series 1-5, Starter Card, Collection Level, Recruit Season).
- mode variant (left out, exclude.tsv): the carddefid is another card's carddefid plus a mode or team tag (Champion,
  Doomsday, Avengers, XMen, WebSlingers, GuardiansOfTheGalaxy, Thunderbolts, BrotherhoodOfMutants) or a Skill01 card;
  these are the cards of other modes (Team Clash, Grand Arena, Champions; Overdrive's OverloadedReactor cards, Kaptain
  5 Nov 2026), following Kaptain's rule "base game only, no
  modes" (Runeterra, Stormbound 28 Oct 2026).
- everything else (no source): created cards and forms (tokens, never left out: Rock, Squirrel, Mjolnir, Herbie programs,
  Nico Minoru's spells) and cards the export marks unreleased; source_type says which.
Texts the export lacks (TEXT_GAPS): released cards whose export entry has no ability; the ability from snap.fan's series
pages (read 5 Nov 2026), written in Claude's words with the same meaning. The plain cards (Abomination, Cyclops, Hulk, Misty
Knight, Shocker, The Thing, Wasp) have no ability on snap.fan either: no text.
Keywords: definitions from the game's help center (marvelsnap.helpshift.com), Second Dinner's articles and the players'
sites named in each entry, in Claude's words. Written: every keyword the card texts use.
Writes supplement/marvel_snap.jsonl; ids from 8000001 (source.py), kept stable by carddefid order.
Usage: supplement_marvel_snap.py"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC_FILE = os.path.join(HERE, '..', 'sources', 'marvel_snap_cards.json')
OUT = os.path.join(HERE, 'supplement', 'marvel_snap.jsonl')
SRC = 'marvelsnapzone.com export, snap-dossier a23b31f, 2 Nov 2026'
MODE_TAGS = ('Champion', 'Doomsday', 'Avengers', 'XMen', 'WebSlingers', 'GuardiansOfTheGalaxy', 'Thunderbolts',
             'BrotherhoodOfMutants')
MODE_TYPE = f'mode variant ({SRC})'   # exclude.tsv leaves these out

# snap.fan series pages (Series 2, 3, 4, 5), read 5 Nov 2026: the ability of released cards the export has none for
TEXT_GAPS = {
    'Batroc': 'Once per turn: when a card moves, this moves with it and gets +2 Power.',
    'BlackKnight': 'Once per game: after you discard a card, add the Ebony Blade to your hand with the Power of that card.',
    'MBaku': 'At the end of the game, this moves from your deck to your location with the lowest Power (one that is not full).',
    'Martyr': 'At the end of the game, this moves to a location where it makes you lose the game (if it can).',
    'Nebula': 'Every turn your opponent plays no card here, this gets +2 Power (not on the turn you play this).',
    'NegasonicTeenageWarhead': 'Once per game: after an enemy character is played here, destroy it.',
    'Scream': 'Once per turn: when an enemy card moves, steal 2 Power from it.',
    'TheCollector': 'When a card enters your hand from anywhere except your deck, this gets +1 Power.',
    'WeaponXWolverine': 'After one of your other cards is destroyed, this gets +1 Power. Every third time, this effect gets '
                        '1 bigger. (0/3)',
}
# tokens the export lacks, named by a card's text (snap.fan card list, read 5 Nov 2026)
TOKENS = [('EbonyBlade', 'Ebony Blade', 'Ongoing: This can not be destroyed.', 'Black Knight')]
# tokens found later, written after the keywords so earlier ids stay (source, text in the source's words)
LATE_TOKENS = [('MuramasaShard', 'Muramasa Shard', "When this is discarded or destroyed, double Daken's Power.", 'Daken',
                'marvelsnap.com Character Spotlight: Daken (read 5 Nov 2026); snap.fan lists it as Daken\'s token')]

H = 'marvelsnap.helpshift.com'
# trigger labels found later, written last so earlier ids stay (Kaptain, 5 Nov 2026: handled like End of Turn)
LATE_KEYWORDS = [('When Discarded', 'Acts when the card is discarded from its player\'s hand.',
                  'a trigger label of the card texts (Apocalypse, Swarm, Zombie Black Cat "another When Discarded card")')]
KEYWORDS = [
    ('On Reveal', 'Acts once, when the card is turned face up on the board: after it is played, and also when a location or '
     'card puts it there, unless something stops On Reveal (Cosmo).',
     f'{H} faq 48 and 42; marvelsnapzone.com abilities guide'),
    ('Ongoing', 'A lasting effect that holds for as long as the card is on the board.',
     f'{H} faq 99; marvelsnapzone.com abilities guide'),
    ('Activate', 'The card does nothing when played; from the turn after it was played its player can choose a turn to use '
     'the ability, which then happens as that turn plays out.',
     'marvel.com article on Activate (The Amazing Spider-Season, Sep 2024); marvelsnapzone.com activate ability guide'),
    ('End of Turn', 'Acts at the end of every turn while the card is on the board.',
     'fourthlocation.com, A unifying language for Snap (19 Aug 2026): an official timing keyword'),
    ('Start of Turn', 'Acts at the start of every turn while the card is on the board.',
     'fourthlocation.com, A unifying language for Snap (19 Aug 2026), late edit: a datamined timing keyword'),
    ('Game Start', 'Acts when the game begins, from the deck or hand (Second Dinner: a wording, not yet a keyword with rules '
     'of its own).', 'marvelsnapzone.com developer answer "New keyword(s): Game Start" (13 Dec 2024)'),
    ('Objective', 'A goal on the card with a counter (0/6); the counter counts from the start of the game, and the reward '
     'happens after the turn ends (after End of Turn effects) if the card is in play with the goal met.',
     'snap.fan, Keyword datamine: what is Objective (23 Feb 2026)'),
    ('Moveable', 'The card can be moved by its player.', f'{H} faq 604 New Keywords'),
    ('Empowered', 'A card is Empowered when its Power is raised permanently (also by setting it higher); Power from '
     'Ongoing effects does not count.', f'{H} faq 604 New Keywords'),
    ('Quickdraw', 'The stronger ability after the word is used instead of the normal one when the card is played on the '
     'same turn it was drawn.', 'snapvault.app, Fractured Frontier season guide (28 Jul 2026)'),
    ('Horde', 'The first time you play a Horde card you get a plain Zombie Horde card at a random location with 0 Power; '
     'every Horde +N adds N Power to your Zombie Horde.', 'snap.fan, Developer update: Undead Horde (2 Oct 2025)'),
    ('Merge', 'A card merges into another: their Power is added together, the merged card goes under the other, and no '
     'ability happens again. It frees a place at the location.', 'snap.fan, Man-Spider card preview (3 Nov 2025)'),
    ('Afflict', 'Give an enemy card negative Power.', 'snap.fan, Man-Spider card preview (3 Nov 2025)'),
    ('Destroy', 'Remove a card from the board; destroyed cards are gone, there is no graveyard.',
     'thegamer.com, Marvel Snap cards effects explained (8 Nov 2022); marvelsnapzone.com abilities guide'),
    ('Discard', 'Remove a card from your hand.', 'marvelsnapzone.com abilities guide'),
    ('Move', 'A card on the board goes to another location; not past the left or right location and not into a full one; '
     'its player, the opponent or a location can move it.',
     f'{H} faq 42; thegamer.com, Marvel Snap cards effects explained (8 Nov 2022)'),
]
strip = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s or '')).strip()


def kind(x, ids):
    k = x['carddefid']
    if k.startswith('Skill01') or any(k.endswith(t) and k[:-len(t)] in ids for t in MODE_TAGS) \
            or any(k.endswith(t) for t in ('FirstStepsChampion', 'RiderChampion', 'SpiderChampion')) or 'OverloadedReactor' in k:
        return MODE_TYPE
    if x['source'] not in (None, 'None', ''): return f"card ({SRC}; collectible)"
    if x['status'] == 'unreleased': return f"card ({SRC}; unreleased or created card)"
    return f"card ({SRC}; released, not collectible: created card or form)"


def main():
    d = json.load(open(SRC_FILE)); ids = {x['carddefid'] for x in d}
    rows = []
    for x in sorted(d, key=lambda x: x['carddefid']):
        text = strip(x['ability']).lstrip('!').strip()
        if text.lower() == 'none': text = ''  # the export's placeholder for no ability (Bug, Foggy Nelson ...)
        st = kind(x, ids)
        if not text and x['carddefid'] in TEXT_GAPS:
            text = TEXT_GAPS[x['carddefid']]; st += '; text from snap.fan, Claude\'s words'
        src = x['source'] if x['source'] not in (None, 'None') else None
        rows.append({'game': 'marvel_snap', 'ext_id': x['carddefid'], 'name': strip(x['name']).lstrip('!').strip(),
                     'category': 'unit', 'source_type': st, 'edition': src, 'cost': f"{x['cost']} energy",
                     'cost_num': float(x['cost']), 'stats': json.dumps({'power': x['power']}), 'text': text,
                     'extra': json.dumps({'status': x['status'], 'source_slug': x['source_slug']})})
    for k, n, t, by in TOKENS:
        if k not in ids:
            rows.append({'game': 'marvel_snap', 'ext_id': k, 'name': n, 'category': 'unit',
                         'source_type': f'card (created by {by}; snap.fan card list, read 5 Nov 2026; Claude\'s words)',
                         'edition': None, 'cost': None, 'cost_num': None, 'stats': None, 'text': t, 'extra': None})
    for n, t, s in KEYWORDS:
        rows.append({'game': 'marvel_snap', 'ext_id': 'kw:' + n, 'name': n, 'category': 'keyword',
                     'source_type': f'keyword ({s}; Claude\'s words)', 'text': t})
    for k, n, t, by, src in LATE_TOKENS:
        if k not in ids:
            rows.append({'game': 'marvel_snap', 'ext_id': k, 'name': n, 'category': 'unit',
                         'source_type': f'card (created by {by}; {src})', 'edition': None, 'cost': None, 'cost_num': None,
                         'stats': None, 'text': t, 'extra': None})
    for n, t, src in LATE_KEYWORDS:
        rows.append({'game': 'marvel_snap', 'ext_id': 'kw:' + n, 'name': n, 'category': 'keyword',
                     'source_type': f'keyword ({src}; Claude\'s words)', 'text': t})
    for i, r in enumerate(rows): r['id'] = 8000001 + i
    with open(OUT, 'w') as f:
        for r in rows: f.write(json.dumps(r) + '\n')
    from collections import Counter
    print(len(rows), Counter(r['source_type'].split(';')[-1].strip() if r['category'] == 'unit' else 'keyword' for r in rows))


if __name__ == '__main__':
    main()
