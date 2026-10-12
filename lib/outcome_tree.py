"""Effect concepts by OUTCOME (what the effect achieves first, the mechanism as a child; a concept may have several parents),
so the same outcome is found across games however each game does it. Changes (Claude's network):
  suppress            stop an enemy unit from doing something (parent: control)
    no_damage_output  the unit deals no damage, however it is done:
      attack_lock       an enemy can't attack (a lock put on an enemy; cant_attack stays a unit's own drawback)
      attack_zero       an enemy's attack/power/strength set to 0 (also under stat_set)
      damage_prevention damage an enemy would deal is prevented / it deals no damage
    cant_block        an enemy can't block
    immobilize        an enemy can't move
    silence           abilities removed (moved here from debuff)
    disable           total: can't act at all (stun, freeze, sleep, paralysis, skip a turn); under no_damage_output, cant_block, immobilize
  debuff              renamed "Stat loss": lower stats, any size (disable, silence, damage_over_time, mark_target no longer under it)
  temporary_effect    lasts only this turn or round, buff or not (temporary_buff becomes its child, for bonuses only)
  card_advantage      gain cards: parent of draw, generate_cards, copy
  return_to_hand      also under removal (it removes a unit from the board); revive under death and summon (a unit comes back)
Text-pattern tags are recomputed for the moved concepts: a text_pattern 'disable' that only says "can't attack" / "can't move" /
"can't block" becomes the matching partial lock; a text_pattern temporary_buff without a bonus becomes temporary_effect.
Hand-reviewed tags are not touched here (keywords are re-checked in lib/reviews_outcome/). Idempotent. Usage: outcome_tree.py <db>"""
import re, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
NEW = {
 'suppress': ('Suppress', 'effect', ['control'], 'Stop an enemy unit from doing something: attacking, dealing damage, blocking, moving, using abilities, or acting at all.'),
 'no_damage_output': ('No damage output', 'effect', ['suppress'], 'The unit deals no damage, however it is done: it cannot attack, its attack is set to 0, or its damage is prevented.'),
 'attack_lock': ('Attack lock', 'effect', ['no_damage_output'], "An enemy unit can't attack (a lock put on an enemy, often for a turn or round)."),
 'attack_zero': ('Attack set to 0', 'effect', ['no_damage_output', 'stat_set'], "An enemy unit's attack, power or strength is set to 0."),
 'damage_prevention': ('Damage prevention', 'effect', ['no_damage_output'], 'Damage an enemy unit would deal is prevented, or it deals no damage.'),
 'cant_block': ("Can't block", 'effect', ['suppress'], "An enemy unit can't block or intercept."),
 'immobilize': ('Immobilize', 'effect', ['suppress'], "An enemy unit can't move: root, snare, pin."),
 'temporary_effect': ('This turn / round only', 'structure', ['structure'], 'Lasts only this turn or round, whether a bonus, a penalty or a lock.'),
 'card_advantage': ('Card advantage', 'effect', ['effect'], 'Gain cards: draw, create or copy cards.'),
}
PARENTS = {'disable': ['suppress', 'no_damage_output', 'cant_block', 'immobilize'], 'silence': ['suppress', 'control'],
           'damage_over_time': ['damage'], 'mark_target': ['combo_sequence'], 'temporary_buff': ['buff', 'temporary_effect'],
           'draw': ['card_flow', 'card_advantage'], 'generate_cards': ['draw', 'card_advantage'], 'copy': ['effect', 'card_advantage'],
           'return_to_hand': ['control', 'tempo', 'removal'], 'revive': ['death', 'summon']}
DESC = {'debuff': ('Stat loss', 'Lower an enemy\'s stats, any size: -power, -attack, -health, shrink, wither. Locks and silence are under suppress.'),
        'disable': ('Total disable', "The unit can't act at all: stun, freeze, sleep, paralysis, skips its turn."),
        'temporary_buff': ('Temporary bonus', 'Bonuses that last only this turn or round.'),
        'cant_attack': ("Can't attack (own drawback)", "The unit itself can't attack: defender, wall; a pure blocker. Locks on enemies are attack_lock.")}
T = r"\b(target|enemy|enemies|opponent'?s?|that|those|each|all other|the chosen|the attacked|the targeted)\b"   # a determiner: "this creature can't attack" stays an own drawback
PATS = {
 'attack_lock': [T + r"[^.]{0,40}\b(can'?t|cannot|may not|is unable to) attack", r"\b(can'?t|cannot) attack (this|next|until|during)"],
 'attack_zero': [r"\b(attack|power|strength) (to|becomes) 0\b", r"\bset[^.]{0,30}(attack|power|strength)[^.]{0,10} to 0\b", r"\bfrostbite"],
 'damage_prevention': [r"\bprevent (all )?(the )?(combat )?damage (that would be )?dealt by", r"\bdeals? no (combat )?damage\b", r"\b(can'?t|cannot) deal (combat )?damage\b(?! to (this|you|your|friendly|it|him|her|them|allies))"],
 'cant_block': [T + r"[^.]{0,40}\b(can'?t|cannot|may not|is unable to) block", r"\bcan'?t be (used as a )?blocker"],
 'immobilize': [T + r"[^.]{0,40}\b(can'?t|cannot|may not) (move|be moved by its controller)", r"\b(is|are|becomes?|become) (rooted|snared|pinned)\b", r"\b(root|snare)s? (target|an|the|that|each)\b"],
 'temporary_effect': [r"(until|till) (the )?end of (the |your |this )?(turn|round)", r"\b(gets?|gains?|has|have|loses?|becomes?|can'?t|cannot|deals?|takes?|set[s]?)\b[^.]{0,40}\bthis (turn|round)\b", r"until (the start of )?your next turn", r"\buntil the end of the (battle round|phase|turning point)"],   # "this turn" as a condition window ("if you discarded it this turn") is not a duration
}
TOTAL = re.compile(r"\bstun|\bfreez|\bfrozen\b|\bparaly|\bsleep|\bdaze|skip (its|their) (next )?(turn|activation)|can'?t (attack or block|act|take actions)|\bincapacitat", re.I)
BONUS = re.compile(r"\+\d|\bgains?\b|\bget[s]? \+|\bhas \+|\bbonus|\bboost", re.I)
ok = {i for (i,) in q('SELECT id FROM concepts')}
for cid, (name, facet, parents, desc) in NEW.items():
    c.execute('INSERT OR REPLACE INTO concepts VALUES(?,?,?,?)', (cid, name, facet, desc))
for cid, (name, facet, parents, desc) in NEW.items():
    c.execute('DELETE FROM concept_parents WHERE child=?', (cid,))
    for p in parents: c.execute('INSERT INTO concept_parents VALUES(?,?)', (cid, p))
for cid, ps in PARENTS.items():
    if cid not in ok: continue
    c.execute('DELETE FROM concept_parents WHERE child=?', (cid,))
    for p in ps: c.execute('INSERT INTO concept_parents VALUES(?,?)', (cid, p))
for cid, (name, desc) in DESC.items(): c.execute('UPDATE concepts SET name=?, description=? WHERE id=?', (name, desc, cid))
for cid, ps in PATS.items():
    c.execute('DELETE FROM concept_patterns WHERE concept=? AND game IS NULL', (cid,))
    for p in ps: c.execute("INSERT INTO concept_patterns VALUES(?,?,?,NULL)", (cid, 'does', p))
# enemy locks are no longer general cant_attack / disable wording
c.execute("DELETE FROM concept_patterns WHERE concept='disable' AND game IS NULL AND pattern IN (?,?,?)", ("can't attack", r'\broot(ed)?\b', r'\bimmobil'))
comp = {k: [re.compile(p, re.I) for p in v] for k, v in PATS.items()}
# tags a hand review confirmed are kept even when an older pattern made them (regression set, 'present' lines)
import csv, os
kept = dict(q('SELECT old_id, kept_id FROM merged_entities')) if q("SELECT 1 FROM sqlite_master WHERE name='merged_entities'") else {}
reviewed = {(kept.get(int(r['entity']), int(r['entity'])), r['concept']) for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'regression.tsv'), encoding='utf-8'), delimiter='\t') if r['expect'] == 'present'}
for e, k in q("SELECT entity, concept FROM entity_concepts WHERE method='text_pattern' AND concept IN (%s)" % ','.join('?' * len(PATS)), *PATS):
    if (e, k) not in reviewed: c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND method='text_pattern'", (e, k))
n = {k: 0 for k in PATS}; moved = 0; tb = 0
rows = q("SELECT id, game, text FROM entities WHERE text IS NOT NULL AND category NOT IN ('tribe')")
dis = {e for (e,) in q("SELECT entity FROM entity_concepts WHERE concept='disable' AND method='text_pattern'")}
tmpb = {e for (e,) in q("SELECT entity FROM entity_concepts WHERE concept='temporary_buff' AND method='text_pattern'")}
for e, g, t in rows:
    low = t.lower()
    for k, ps in comp.items():
        m = next((m for p in ps for m in [p.search(low)] if m), None)
        if m: n[k] += c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, k, 'does', 'text_pattern', low[max(0, m.start() - 20): m.start() + 40])).rowcount
    if e in dis and not TOTAL.search(low) and (e, 'disable') not in reviewed:
        moved += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept='disable' AND method='text_pattern'", (e,)).rowcount
    if e in tmpb and not BONUS.search(low) and (e, 'temporary_buff') not in reviewed:
        tb += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept='temporary_buff' AND method='text_pattern'", (e,)).rowcount
        c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, 'temporary_effect', 'does', 'text_pattern', 'was temporary_buff without a bonus'))
c.commit()
print('outcome tree:', n, ' partial locks no longer total disable:', moved, ' temporary_buff without bonus moved:', tb)
