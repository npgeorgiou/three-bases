"""Step 3: effect records by script for games with fixed wording. A card is covered when every sentence of its text is read
completely by the wording below (a trigger opening, an optional condition, then effects with target, amount and duration);
a covered card gets source "script" and is not read by Claude. Anything left over sends the whole card to reading.
Keyword-only sentences ("Taunt. Rush.") are covered by the keyword records (step 2).
Usage: script_records.py <db> <game> [sample N]   prints coverage, then N covered cards with their records and N not covered."""
import os, random, re, sqlite3, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import COLUMNS

NUM = r'(\d+|an?|one|two|three|four|five|six|seven|eight|nine|ten|x)'
WORDNUM = {'a': '1', 'an': '1', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
           'eight': '8', 'nine': '9', 'ten': '10', 'x': 'X'}
def n(s): return WORDNUM.get(s.lower(), s)
NAME = r"((?:random )?[a-z0-9'-]+(?: [a-z0-9'-]+)*?(?: with (?:taunt|divine shield|rush|charge|windfury|stealth|lifesteal|poisonous|reborn)(?:(?:,| and) (?:taunt|divine shield|rush|charge|windfury|stealth|lifesteal|poisonous|reborn))*)?)"
STOP = r"(?<! for each)(?<! that)(?<! if)"  # a name that runs into a rule ("for each spell") is not a name

# ---- Hearthstone wording ----
HS_UNIT = r'(?:minions?|characters?)'
HS_TARGETS = [  # (pattern, target); first match wins, so longer phrases come first
    (rf'(?:all )?other friendly {HS_UNIT}|your other minions', 'ally_unit all'),
    (rf'all friendly {HS_UNIT}|your minions|your characters', 'ally_unit all'),
    (rf'all enemy {HS_UNIT}|all enemies|enemy minions', 'enemy_unit all'),
    (rf'all other {HS_UNIT}|all {HS_UNIT}', 'any_unit all'),
    (rf'adjacent minions', 'ally_unit adjacent'),
    (rf'{NUM} random enemy {HS_UNIT}|{NUM} random enem(?:y|ies)', 'enemy_unit random {0}'),
    (rf'{NUM} random friendly {HS_UNIT}', 'ally_unit random {0}'),
    (rf'{NUM} random (?:other )?{HS_UNIT}', 'any_unit random {0}'),
    (rf'(?:an?|another) enemy {HS_UNIT}|an enemy', 'enemy_unit chosen'),
    (rf'(?:an?|another) friendly {HS_UNIT}', 'ally_unit chosen'),
    (rf'(?:an?|another) {HS_UNIT}', 'any_unit chosen'),
    (r'the enemy hero|your opponent', 'enemy_player'),
    (r'your hero|you', 'my_player'),
    (r'each player|both players', 'each_player'),
    (r'this minion|itself|this', 'self'),
]
HS_TRIGGERS = [  # sentence openings
    (r'battlecry:', 'on_play'), (r'deathrattle:', 'death_trigger'), (r'spellburst:', 'on_spell'), (r'frenzy:', 'on_damaged'),
    (r'overkill:', 'on_kill'), (r'inspire:', 'hero_power'), (r'start of game:', 'start_of_game'),
    (r'at the end of your turn,', 'turn_end'), (r'at the start of your turn,', 'turn_start'),
    (r'(?:whenever|after) you cast a spell,', 'on_spell'), (r'(?:whenever|after) this (?:minion )?attacks,', 'on_attack'),
    (r'whenever this minion takes damage,', 'on_damaged'), (r'(?:whenever|after) (?:a|another) friendly minion dies,', 'other_death_trigger'),
    (r'(?:whenever|after) you (?:play|summon) a minion,', 'on_ally_play'), (r'whenever you draw a card,', 'on_draw'),
]
HS_CONDITIONS = [r'combo:', r'outcast:', r'if [^,]+,', r'finale:', r'corrupt:']
HS_KEYWORDS = r'(?:taunt|rush|charge|divine shield|windfury|mega-windfury|stealth|lifesteal|poisonous|venomous|reborn|elusive|echo|twinspell|tradeable|magnetic|spell damage \+\d+|overload: \(\d+\)|immune|dormant)'
# effects: (pattern with a {T} slot for the target, effect, amount group or text, duration)
HS_EFFECTS = [
    (r'deal (\d+) damage to {T}', 'damage', 1, 'instant'),
    (r'deal (\d+) damage', 'damage', 1, 'instant', 'any_unit chosen'),  # a spell's bare "Deal N damage." is aimed by the player
    (r'restore (\d+) health to {T}', 'heal', 1, 'instant'),
    (r'give {T} \+(\d+)/\+(\d+) this turn', 'temporary_buff', '+{1}/+{2}', 'this_turn'),
    (r'give {T} \+(\d+) attack this turn', 'temporary_buff', '+{1} Attack', 'this_turn'),
    (r'give {T} \+(\d+)/\+(\d+)', 'stat_gain', '+{1}/+{2}', 'permanent'),
    (r'give {T} \+(\d+) attack', 'attack_gain', '+{1} Attack', 'permanent'),
    (r'give {T} \+(\d+) health', 'defence_gain', '+{1} Health', 'permanent'),
    (r'gain \+(\d+)/\+(\d+)', 'stat_gain', '+{1}/+{2}', 'permanent', 'self'),
    (r'gain \+(\d+) attack', 'attack_gain', '+{1} Attack', 'permanent', 'self'),
    (r'gain (\d+) armor', 'block_armor', '{1}', 'permanent', 'my_player'),
    (rf'draw {NUM} cards?', 'draw', '{1}', 'instant', 'my_player'),
    (rf'discover an? {NAME}', 'generate_cards', '1 of 3: {1}', 'instant', 'my_player'),
    (rf'add {NUM} {NAME} to your hand', 'generate_cards', '{1} {2}', 'instant', 'my_player'),
    (rf'summon {NUM} (\d+/\d+) {NAME}', 'summon', '{1} {2} {3}', 'permanent', 'position chosen'),
    (r'freeze {T}', 'disable', 'misses its next attack', 'next_turn'),
    (r'destroy {T}', 'destroy', '', 'instant'),
    (r'silence {T}', 'silence', '', 'permanent'),
    (r'return {T} to (?:its owner\'s|your) hand', 'return_to_hand', '', 'instant'),
    (r'give {T} (taunt|divine shield|rush|windfury|stealth|lifesteal|poisonous|reborn|charge)', 'buff', '{1}', 'permanent'),
    (r'gain (\d+) mana crystals?', 'resource_gain', '{1}', 'permanent', 'my_player'),
    (r'gain an empty mana crystal', 'resource_gain', '1 empty', 'permanent', 'my_player'),
]
GAMES = {'hearthstone': (HS_TRIGGERS, HS_CONDITIONS, HS_EFFECTS, HS_TARGETS, HS_KEYWORDS)}


def target(phrase, targets):
    """The record target for a phrase that is all target, or None."""
    for pat, t in targets:
        m = re.fullmatch(pat, phrase.strip())
        if m: return t.format(*[n(x) for x in m.groups() if x]) if '{0}' in t else t
    return None


def effects(clause, effs, targets):
    """[(effect, target, amount, duration)] for a clause made only of effects joined by 'and' / ',', or None."""
    clause = clause.strip(' .,')
    if not clause: return []
    for pat, eff, amt, dur, *fixed in effs:
        rx = pat.replace('{T}', '(?P<t>.+?)')
        m = re.match(rx + r'(?=$|,? and |\. |, then |\.$)', clause)
        if m and re.search(r'\b(?:for each|that|if|whose|who|which|cost|costs|copy|copies|for)\b|\band\b(?! (?:taunt|divine shield|rush|charge|windfury|stealth|lifesteal|poisonous|reborn))', m.group(0)): m = None
        if not m: continue
        if fixed: tg = fixed[0]
        elif 't' in m.groupdict(): tg = target(m.group('t'), targets)
        else: tg = None
        if tg is None: continue
        ti = m.re.groupindex.get('t')
        g = [x or '' for k, x in enumerate(m.groups(), 1) if k != ti]
        a = amt if isinstance(amt, str) else m.group(amt)
        a = a.format('', *[n(x) for x in g]) if '{' in a else a
        rest = re.sub(r'^(?:,? and |, then |\. )', '', clause[m.end():])
        more = effects(rest, effs, targets)
        if more is None: continue
        return [(eff, tg, a, dur or 'instant')] + more
    return None


def read_card(game, text, kind):
    """Records [(ability, trigger, effect, target, amount, duration, condition)] when the whole text is read, else None."""
    trigs, conds, effs, targets, kws = GAMES[game]
    low = re.sub(r'\s+', ' ', (text or '').lower()).strip()
    low = re.sub(rf'^(?:{kws})(?:[,.]? (?:{kws}))*\.?\s*', '', low)  # leading keyword list
    if not low: return []
    out = []; prev = None; k = 0
    for sent in re.split(r'(?<=\.) (?=[a-z(])', low):
        s = sent.strip()
        if re.fullmatch(rf'(?:{kws})(?:[,.]? (?:{kws}))*\.?', s): continue
        trig = 'on_play' if kind == 'spell' else prev or 'passive'  # a unit's sentence with no opening continues the last trigger
        opened = False
        for pat, t in trigs:
            if re.match(pat, s): trig = t; s = s[re.match(pat, s).end():].strip(); opened = True; break
        if opened or k == 0: k += 1  # one ability per trigger opening; a spell is one ability
        prev = trig if trig != 'passive' else None
        if trig == 'passive' and kind != 'spell': return None  # a unit sentence with no trigger: an aura or a rule, read it
        cond = ''
        for pat in conds:
            m = re.match(pat, s)
            if m: cond = m.group(0).strip(' ,:'); s = s[m.end():].strip(); break
        es = effects(s, effs, targets)
        if not es: return None
        out += [(k, trig, *e, cond) for e in es]
    return out


if __name__ == '__main__':
    db, game = sys.argv[1], sys.argv[2]
    sample = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    c = sqlite3.connect(db)
    rows = c.execute("SELECT id, name, category, text FROM entities WHERE game=? AND category IN ('unit','spell') "
                     "AND text IS NOT NULL AND text != ''", (game,)).fetchall()
    got = {e: read_card(game, t, cat) for e, nm, cat, t in rows}
    cov = [r for r in rows if got[r[0]] is not None]
    print(f'{game}: {len(cov)} of {len(rows)} cards covered ({100 * len(cov) / len(rows):.1f}%)')
    random.seed(1)
    for e, nm, cat, t in random.sample(cov, min(sample, len(cov))):
        print(f'\n{nm} | {t}')
        for r in got[e]: print('   ', ' | '.join(str(x) for x in r))
    left = [r for r in rows if got[r[0]] is None]
    if sample: print('\nnot covered:')
    for e, nm, cat, t in random.sample(left, min(sample, len(left))): print(f'  {nm} | {t}')
