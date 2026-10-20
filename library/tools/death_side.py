"""Whose death or leaving sets off a trigger (Kaptain's decision, 20 Oct 2026): death_trigger is the entry's own death,
other_death_trigger another unit's death, leave_trigger the entry leaving play by any means, other_leave_trigger another unit
leaving play. The tag follows the words: "when this leaves the battlefield" is leave_trigger only, "when this dies or is
exiled" gets both. Used by the key correction (key/death_split.py), the build (concept_tree.py split rule) and regression.tsv.
side(clause, name, spell) -> set of those four concepts read from the clause, empty when the wording names no death or leaving,
or {'?'} when a death or leaving is named but whose it is can't be read."""
import re

DIE = r"(?:dies|die|died|dying|is destroyed|are destroyed|was destroyed|were destroyed|be destroyed|destroyed(?! (?:this|that|it|them|him|her|a|an|the|one|another|any|enemy)\b)|is killed|are killed|killed(?! (?:this|that|it|them|him|her|a|an|the|one|another|any|enemy)\b)|perish(?:es|ed)?|is slain|are slain|slain(?! (?:models?|units?|fighters?|operatives?|this|that|it|them|an?|the|enemy)\b)|(?:is|are|would be|be) incapacitated|(?<!has )(?<!have )incapacitated(?! (?:this|that|it|them|an?|the|enemy|one)\b)|(?:is|are|be) taken out of action|taken out of action|suffers a dead result|(?:is|are) defeated|defeated|(?:is|are) put into (?:a|your|its owner's|their owner's) graveyard from the battlefield)"
LEAVE = r"(?:leaves?|left) (?:the battlefield|play|the board|the field)|(?:is|are|be) banished(?! (?:from (?:your |the |their )?(?:deck|hand|graveyard)|by this))|(?:is|are) removed from (?:play|the battlefield)"
SPELLS = {'spell', 'tactic', 'ploy', 'stratagem', 'event', 'action'}
START = r"(?:when(?:ever)?|after|each time|every time|the first time|if|once|before|as soon as)"   # not "until": "until this leaves the battlefield" is a duration
# the games' own words for "when this dies": a card with one of these has an own-death trigger
OWN_KW = re.compile(r"\b(dying wish|deathwish|deathrattle|last words|last breath|deadly demise|deathblow|when destroyed|on death|upon death|death:)", re.I)
OWN = re.compile(r"^(this|it|i|i'm|me|~|itself|self|he|she|they)\b|\bthis (\w+ ){0,2}(card|unit|minion|creature|follower|model|operative|fighter|character|item|location|structure|manifestation|warrior|permanent|token|enchantment|artifact|vehicle|squad|player)\b|\bthis\b", re.I)
OTHER = re.compile(r"\b(another|other|an?|any|each|one or more|friendly|enemy|enemies|allied|ally|allies|your|their|opposing|all|its owner's|that)\b", re.I)
TRIG = re.compile(START + r"\b\s+([^.;:!?\n,—–]{0,60}?)\b(" + DIE + r"|" + LEAVE + r")\b", re.I)

SELF_GROUP = re.compile(r"bearing (this|it)\b|with this (sigil|ability|skill|status|trait|rule|keyword)\b|copy of it\b|one of these models|causes it\b|such a model|\b(in|from) this (\w+ )?(unit|squad)\b|this model['’]s unit", re.I)
NOT_SELF = re.compile(r"\b(bearer|equipped|enchanted|quarry|anyone|everyone)\b", re.I)

def _whose(subject, name, spell=False):
    s = subject.strip().lower()
    if SELF_GROUP.search(s): return True, False   # the entry's own unit or the card carrying the sigil
    n0 = (name or '').lower().split(',')[0].strip()
    if n0 and len(n0) > 2 and n0 in s: return True, bool(re.search(r"\bor (another|an?|any)\b", s))   # its own name: "your Canis Rex model"
    if re.match(r"(another|an?|any|each|one|every|all|enemy|friendly|allied|your|their|that|the bearer)\b", s) and not re.search(r"\bor (this|it)\b", s):
        return False, True   # the subject's head is another unit ("an enemy unit in combat with this unit"); "this" only qualifies it
    if NOT_SELF.search(s): return False, True     # the unit carrying or enchanted by this card, or anyone
    if spell and re.match(r"(it|they|them)\b", s): return False, False   # on a spell, "it" is the target, not the card
    n = n0
    own = bool(OWN.search(s)) or (n and n in s)
    other = bool(OTHER.search(re.sub(r"\bthis\b.*", "", s))) if own else bool(OTHER.search(s))
    if re.search(r"\b(this|it)\b[^.]{0,20}\bor (another|an?|any)\b|\b(another|an?|any)\b[^.]{0,30}\bor (this|it)\b", s): own = other = True
    return own, other

# keyword entries whose death or leave-play sentences only state how the game handles removal (Kaptain's decision, 21 Oct 2026):
# no death or leave trigger is read from them, so no card inherits one through them
RULE_ONLY = {('wh_40k_10e', 'leader'), ('gwent', 'doomed')}
BANISH_DIES = {'lorcana'}   # in Lorcana a banished character is one that was defeated: banished is its word for dying

def side(clause, name='', spell=False, game=''):
    t = clause or ''; out = set()
    if (game, (name or '').lower()) in RULE_ONLY: return out
    if game in BANISH_DIES: t = re.sub(r"\b(is|are|be) banished\b", r"\1 destroyed", t, flags=re.I)
    t = re.sub(r"\bwould (die|leave)\b", "would_\\1", t, flags=re.I)   # (see above)
    t = re.sub(r"\bbefore (it|they|this \w+) (is|are) removed from", "before_removed", t, flags=re.I)   # removing a destroyed model is part of its death   # "if it would die / leave, ... instead" replaces the event, it is not a trigger
    if OWN_KW.search(t): out.add('death_trigger')
    for m in re.finditer(r"\btakes? ([^.;:]{0,50}?) out of action(?! test)|\byou slay (another|an?) ", t, re.I):   # active voice: "takes a fighter out of action"
        own, other = _whose(m.group(1) or 'another', name, spell); out |= {'death_trigger'} if own and not other else {'other_death_trigger'} if other else {'?'}
    for m in TRIG.finditer(t):
        subj, ev = m.group(1), m.group(2)
        subj = re.split(r"\b" + START + r"\b", subj, flags=re.I)[-1]   # "if that model was attached when it was destroyed": the nearest start
        if re.search(r"\b(not|neither|never|no)\b|n't\b", subj, re.I) or re.search(r"triggered\s*$", t[:m.start()], re.I): continue   # "if it is not destroyed", "rules triggered when"
        leave = bool(re.match(LEAVE, ev, re.I))
        own, other = _whose(subj, name, spell)
        if not own and not other: out.add('?'); continue
        if own: out.add('leave_trigger' if leave else 'death_trigger')
        if other: out.add('other_leave_trigger' if leave else 'other_death_trigger')
    if not out and re.search(r"\b" + DIE + r"\b|\b" + LEAVE, t, re.I): out.add('?')
    return out

# death_count is counting deaths; one single death trigger with no counting is other_death_trigger
SINGLE = re.compile(r"\b(a|an|another|any|one of (your|its|their)( other)?|each)\b", re.I)
NUM = re.compile(r"\b(x|y|n|\d+|two|three|four|five|second|subsequent|more|multiple|several)\b", re.I)
COUNT = re.compile(r"\b(for each|number of|how many|times|tally|counter|this game|this battle|this match|this turn|so far|died this|x is|equal to)\b", re.I)

def split(k, clause, name='', spell=False, game=''):
    """New concepts for one death_trigger or death_count tag, read from the sentence that holds it (empty: the tag goes)."""
    if (game, (name or '').lower()) in RULE_ONLY: return set()
    s = side(clause, name, spell, game) - {'?'}
    if k == 'death_count':
        return {'other_death_trigger'} if s == {'other_death_trigger'} and SINGLE.search(clause) and not NUM.search(clause) and not COUNT.search(clause) else {'death_count'}
    if spell and not s and re.search(r"\bif (it|they) (dies|die)\b", clause, re.I): return {'on_kill'}   # a spell's target dying (Kaptain's decision)
    return s or {k}

if __name__ == '__main__':
    tests = [("Dying Wish: Draw a card.", {'death_trigger'}), ("Whenever another friendly creature dies, gain 1.", {'other_death_trigger'}),
             ("When this creature leaves the battlefield, return the exiled cards.", {'leave_trigger'}),
             ("Whenever a creature you control leaves the battlefield, put its counters here.", {'other_leave_trigger'}),
             ("When Varchild leaves the battlefield, gain control of all Survivors.", {'leave_trigger'}),
             ("Whenever this or another creature you control dies, draw a card.", {'death_trigger', 'other_death_trigger'}),
             ("If this operative is incapacitated, remove its Mine token.", {'death_trigger'}),
             ("If a friendly SERGEANT VETERAN operative is incapacitated, nominate another.", {'other_death_trigger'}),
             ("When I die, summon a Spiderling.", {'death_trigger'}), ("When this dies or is exiled, draw.", {'death_trigger'}),
             ("Deal 3 damage to a minion. If it dies, gain 2.", {'death_trigger'}),
             ("Each time a model (friendly or enemy) is slain within 12\", give a token.", {'other_death_trigger'}),
             ("If this Manifestation is banished, set up the unit.", {'leave_trigger'}), ("Gain 3 armour.", set())]
    bad = [(s, side(s, 'Varchild, Betrayer of Kjeldor'), w) for s, w in tests if side(s, 'Varchild, Betrayer of Kjeldor') != w]
    for b in bad: print('FAIL', b)
    print(len(tests) - len(bad), 'of', len(tests), 'right')
