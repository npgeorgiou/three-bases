"""Frequency limit on every trigger -> effect pair (factions.txt Part 5, step 7: the FREQUENCY check).
Adds trigger_effect.frequency and trigger_effect.basis. Classes:
  per_card   fires at most once for the card: a spell, a Place/on-play effect, the card's OWN death, once per game, a one-time delayed effect
  per_round  explicit "once per turn/round" cap, or a trigger of the card itself that comes once per round (turn start/end, its own attack or kill, a tap ability)
  unbounded  fires on other units' events or on repeated events (any ally dies, any spell cast, each time it takes damage, whenever an ally is played)
  static     aura / ongoing text: not a trigger
Rules are wording patterns per clause (Claude's classification); the basis column says which rule decided.
A per_card own-death effect on a card that can return (revive, return to hand, cheat death) is flagged in basis: its death can repeat.
Usage: frequency.py <db>   (last build step: nothing inserts into trigger_effect afterwards)"""
import re, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
cols = [r[1] for r in q('PRAGMA table_info(trigger_effect)')]
for col in ('frequency', 'basis'):
    if col not in cols: c.execute(f'ALTER TABLE trigger_effect ADD COLUMN {col} TEXT')

CAP_ROUND = re.compile(r"once (per|each|a|every) (turn|round|turning point|phase|battle round|activation)|only once each turn|\d+ times? (per|each|a) turn|up to (once|twice|\w+ times) (per|each) turn|first time (each|every|this) (turn|round)|\bthe first .{0,40} each (turn|round)")
CAP_CARD = re.compile(r"once per (game|battle|match|combat)|\bthe next time\b|\bonly once\b(?! (per|each))|\bthis game, the first\b")
OTHERS = re.compile(r"\b(whenever|each time|every time|after|when) (another|a|an|any|one or more|each|your|other|an allied|a friendly|an enemy|a nearby|one of your|the enemy|you|your opponent|a player)\b(?! (this|~))")
SELF = re.compile(r"\b(whenever|each time|every time|when|after) (this|~|it|he|she|i|me|i'm|i am)\b")
ANOTHER = re.compile(r"\b(whenever|each time|every time|when|after)\b.{0,40}\b(another|other|a friendly|an allied|an ally|an enemy|any)\b")
REPEAT_ACT = re.compile(r"^\s*((\{[^}t]*\}|[0-9]+ ?(mana|energy|cp|ap)?)[ ,]*)+:")  # mana-only activation, no tap symbol

PER_CARD = {'on_play', 'death_trigger', 'once_per_game', 'start_of_game', 'game_end_trigger', 'trap_secret', 'delayed', 'turn_number'}
PER_ROUND = {'turn_start', 'turn_end', 'combat_start', 'cooldowns', 'hero_power', 'territory_trigger', 'concentration', 'on_attack', 'on_kill', 'activated', 'telegraphed_threats'}
UNBOUNDED = {'on_ally_play', 'on_spell', 'on_damaged', 'reactions', 'on_enemy_enter', 'death_count', 'counterattack'}
STATIC = {'aura', 'passive'}
ONE_SHOT = {'spell', 'event'}
returns = {e for (e,) in q("SELECT DISTINCT entity FROM entity_concepts WHERE concept IN ('revive','return_to_hand','cheat_death','recursion') AND role='does'")}
cat = dict(q('SELECT id, category FROM entities'))

game = dict(q('SELECT id, game FROM entities')); ename = {i: (n or '').lower().split(',')[0] for i, n in q('SELECT id, name FROM entities')}
SELF_COST = re.compile(r'(sacrifice|exile|discard|return) (this|~)\b|\bcycling\b')

def classify(e, trig, clause):
    cl = (clause or '').lower()
    head = re.split(r'[,:]', cl, maxsplit=1)[0]   # the trigger part of the clause
    watch = bool(OTHERS.search(head) and not SELF.search(head)) or bool(ANOTHER.search(head))
    if CAP_CARD.search(cl): return 'per_card', 'explicit cap (once per game / next time)'
    if CAP_ROUND.search(cl): return 'per_round', 'explicit cap (once per turn/round)'
    if trig in STATIC: return 'static', 'aura/ongoing'
    if cat.get(e) in ONE_SHOT and trig in ('on_play', 'delayed', 'activated'): return 'per_card', 'spell/event: resolves once'
    if trig in UNBOUNDED: return 'unbounded', f'{trig}: repeated or shared event'
    if trig == 'death_trigger':
        if watch: return 'unbounded', "others' deaths"
        return 'per_card', 'own death' + ('; card can return, so the death can repeat' if e in returns else '')
    if trig in PER_CARD: return 'per_card', f'{trig}: once per card'
    if trig in PER_ROUND:
        if trig in ('on_attack', 'on_kill') and watch: return 'unbounded', f"{trig} of other units"
        if trig == 'activated' and ':' in cl and (SELF_COST.search(cl.split(':')[0]) or (ename.get(e) and re.search(r'(sacrifice|exile|discard) ' + re.escape(ename[e]), cl.split(':')[0]))): return 'per_card', 'activation uses up the card itself'
        if trig == 'activated' and (REPEAT_ACT.search(cl) or (game.get(e) == 'mtg' and ':' in cl and '{t}' not in cl.split(':')[0] and '{q}' not in cl.split(':')[0])): return 'unbounded', 'repeatable activation (no tap symbol or once-cap)'
        return 'per_round', f'{trig}: once per round for this card'
    return 'unbounded', f'{trig}: no bound found'

rows = q('SELECT rowid, entity, trigger, clause FROM trigger_effect')
for rid, e, t, cl in rows:
    f, b = classify(e, t, cl)
    c.execute('UPDATE trigger_effect SET frequency=?, basis=? WHERE rowid=?', (f, b, rid))
c.commit()
print('frequency:', dict(q('SELECT frequency, count(*) FROM trigger_effect GROUP BY 1')))
