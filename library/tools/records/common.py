"""Effect records (TAGGING_RECORDS.md, top section). One record per effect:
  entity, ability, trigger, effect, target, amount, duration, condition, source
entity: entity id; ability: 1, 2, ... in the order the card states its abilities; trigger: a trigger concept id
(on_play, activated, passive, ...); effect: an effect concept id; amount: free text ("+5/+5", "2", "X"); condition: free text
or empty; source: keyword / script / reading.
Keyword records (step 2) come in three kinds: an effect keyword (Taunt) has trigger and effect; trigger "-" means the card's
clause that uses the keyword gives the trigger ("Battlecry: Freeze ..."). A trigger keyword (Battlecry) has only a trigger, a
condition keyword (Combo) only a condition: cards with them inherit that field.
target: "<who> <how>[ <count>]", or just "self", "my_player", "enemy_player" or "each_player". who: WHO; a card target names its zone after a colon (card:hand, card:deck,
card:discard). how: HOW. count only when more than one, or a number is printed ("enemy_unit random 2").
duration: one of DURATION; "n_turns" and "n_rounds" carry the number in amount after a semicolon ("+45%; 2").
Records are TSV files with these columns in this order; load_records.py (step 6) checks them with check()."""
import re

COLUMNS = ('entity', 'ability', 'trigger', 'effect', 'target', 'amount', 'duration', 'condition', 'source')
WHO = ('self', 'ally_unit', 'enemy_unit', 'any_unit', 'my_player', 'enemy_player', 'each_player', 'card', 'position')
HOW = ('chosen', 'all', 'random', 'adjacent', 'triggering')
DURATION = ('instant', 'this_turn', 'this_round', 'until_my_next_turn', 'next_turn', 'n_turns', 'n_rounds', 'this_combat',
            'while', 'until_leaves', 'permanent', 'this_game', 'stacks')
SOURCES = ('keyword', 'script', 'reading')
ZONES = ('hand', 'deck', 'discard')


def check_target(t):
    """Empty string when the target is well formed, otherwise what is wrong."""
    if t in ('self', 'my_player', 'enemy_player', 'each_player'): return ''
    p = t.split()
    if len(p) not in (2, 3): return 'needs "<who> <how>[ <count>]"'
    who, how = p[0], p[1]
    base, _, zone = who.partition(':')
    if base not in WHO or base == 'self': return f'who "{who}"'
    if zone and (base != 'card' or zone not in ZONES): return f'zone "{zone}"'
    if how not in HOW: return f'how "{how}"'
    if len(p) == 3 and not re.fullmatch(r'\d+|X|N', p[2]): return f'count "{p[2]}"'
    return ''


def check(rec, triggers, effects):
    """Problems with one record (a dict over COLUMNS); triggers/effects are the allowed concept ids."""
    out = []
    if rec['source'] == 'keyword' and not rec['effect']:
        if any(rec[k] for k in ('target', 'amount', 'duration')): out.append('trigger/condition keyword with effect fields')
        if not (rec['trigger'] in triggers or rec['condition']): out.append('needs a trigger or a condition')
        return out
    if rec['trigger'] not in triggers and not (rec['trigger'] == '-' and rec['source'] == 'keyword'): out.append(f"trigger {rec['trigger']}")
    if rec['effect'] not in effects: out.append(f"effect {rec['effect']}")
    if (m := check_target(rec['target'])): out.append('target ' + m)
    if rec['duration'] not in DURATION: out.append(f"duration {rec['duration']}")
    if rec['duration'] in ('n_turns', 'n_rounds') and ';' not in rec['amount']: out.append('duration count missing in amount')
    if rec['source'] not in SOURCES: out.append(f"source {rec['source']}")
    return out


def norm(name, text):
    """Card text with the card's own name and every number blanked: texts equal here share one reading (step 4)."""
    t = text or ''
    if name:
        t = t.replace(name, '~')
        if ',' in name: t = t.replace(name.split(',')[0], '~')  # Magic: "Gideon, Ally of Zendikar" -> "Gideon"
        if ' - ' in name: t = t.replace(name.split(' - ')[0], '~')  # Lorcana: "Jasmine - Resourceful Infiltrator"
    t = re.sub(r'[+\-–]?\d+', 'N', t)
    return re.sub(r'\s+', ' ', t).strip().lower()
