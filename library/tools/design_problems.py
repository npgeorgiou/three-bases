"""Design problems seen in Three Bases playtests (README suggestion 9), linked to the mechanics that mitigate them or make them worse.
All relations are Claude's analysis (origin claude_analysis), like the other problem links. Idempotent. Usage: design_problems.py <db>"""
import sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
P = {
 'p_objective_stalemate': ('Objective stalemate', 'Problem: both sides hold their objectives (dots, zones, control points) and neither can break the other; the game stops moving.',
   ['anti_stalemate'],
   {'mitigates': [('forced_movement', 'moves holders off the objective without killing them'), ('piercing', 'gets through the defences that keep holders alive'),
                  ('ranged', 'reaches holders protected by the units in front'), ('aoe_damage', 'wears down a whole line of holders'),
                  ('banish', 'removes a holder for good'), ('silence', 'switches off the abilities that keep a holder alive'),
                  ('fatigue', 'escalating pressure ends the standoff'), ('turn_number', 'a scheduled change of the rules breaks the lock'),
                  ('race_objective', 'rewards the first to break through'), ('scoring_objectives', 'scores every round, so a stalemate still decides the game'),
                  ('lane_closure', 'closing a contested zone moves the fight elsewhere'), ('zone_of_control', 'pins defenders so other objectives open up')],
    'tension': [('blocking', 'blockers hold objectives indefinitely'), ('taunt', 'forces attacks into the sturdiest holder'), ('regeneration', 'holders recover every round'),
                ('damage_reduction', 'holders never fall'), ('shield', 'absorbs the damage meant to break the hold'), ('immunity', 'holders that cannot be answered')]}),
 'p_resource_hoarding': ('Resource hoarding', 'Problem: banking resources across rounds is rewarded over spending them, so a player passes rounds to save for one huge round.',
   ['p_turtling'],
   {'mitigates': [('upkeep', 'saved resources cost something each round'), ('overload_debt', 'big rounds are paid back later'), ('tempo', 'acting now beats acting later'),
                  ('turn_number', 'deadlines make late saving useless'), ('points_scoring', 'every round scores, so skipped rounds are lost points'),
                  ('race_objective', 'the first to act wins the reward'), ('steal', 'a bank can be taken'), ('board_presence', 'the board itself is worth points each round')],
    'tension': [('resource_banking', 'payoffs for unspent resources'), ('round_carryover', 'carried-over resources make saving free'),
                ('kicker', 'paid-up versions reward waiting'), ('finisher', 'one huge purchase decides the game')]}),
 'p_front_pileup': ('Front-row pile-up', 'Problem: one row or position holds all the value, so every unit crowds into it and the other positions are unused.',
   ['p_dominant_strategy'],
   {'mitigates': [('rows', 'gives back rows a job of their own'), ('row_effects', 'effects that favour other rows'), ('ranged', 'units that work from behind'),
                  ('rank_positions', 'skills that only work from certain ranks'), ('support', 'units that help from behind'), ('assists_support', 'bonuses for units behind or beside'),
                  ('aoe_damage', 'punishes crowding'), ('area_templates', 'area shapes punish clumps'), ('flanking', 'rewards positions other than straight ahead'),
                  ('reserve_bench', 'value from units kept back'), ('board_limit', 'caps how many units one row can hold')],
    'tension': [('zone_control', 'only the front holds objectives'), ('taunt', 'front units soak all attacks'), ('blocking', 'only front units block')]}),
 'p_draw_engine': ('Card-draw engine', 'Problem: repeatable draw triggers bury the opponent in card advantage and make long games one-sided.',
   ['p_degenerate_combo'],
   {'mitigates': [('once_per_game', 'a draw that fires once'), ('cooldowns', 'a draw capped per turn'), ('hand_size', 'a hand cap wastes extra draws'),
                  ('fatigue', 'drawing too much runs the deck out'), ('hand_disruption', 'the opponent can take cards from a full hand'),
                  ('silence', 'switches the engine off'), ('removal', 'kills the engine piece'), ('life_payment', 'each draw costs something')],
    'tension': [('draw', 'the payoff itself'), ('card_flow', 'cycling feeds the engine'), ('on_spell', 'draw on every spell cast'),
                ('on_ally_play', 'draw on every unit played'), ('death_count', 'draw on every death'), ('repeat_trigger', 'doubled draw triggers'),
                ('on_damaged', 'draw each time something takes damage')]}),
 'p_holder_snowball': ('Objective-holder snowball', 'Problem: rewards for holding an objective make the holder stronger, so whoever takes it first keeps it.',
   ['p_snowballing'],
   {'mitigates': [('comeback', 'help for the side that does not hold it'), ('enemy_benefit', 'the holder pays the other side'), ('symmetric_effect', 'both sides get the reward'),
                  ('rest_phase', 'recovery windows for the side behind'), ('round_passing', 'losing a round does not lose the game'), ('temporary_buff', 'holder bonuses that do not last'),
                  ('race_objective', 'one-time rewards instead of lasting ones'), ('board_wipe', 'resets a dominant board')],
    'tension': [('control_reward', 'the holder gets more'), ('territory_trigger', 'bonuses for being in the zone'), ('permanent_growth', 'holder bonuses that stack'),
                ('scoring_objectives', 'points per round for the holder'), ('resource_gain', 'the holder earns more resources')]}),
}
ok = {i for (i,) in q('SELECT id FROM concepts')}
for pid, (name, desc, parents, rels) in P.items():
    c.execute("INSERT OR REPLACE INTO concepts VALUES(?,?,?,?)", (pid, name, 'problem', desc))
    c.execute("INSERT OR IGNORE INTO concept_parents VALUES(?,?)", (pid, 'design_problem'))
    c.execute("DELETE FROM concept_relations WHERE (a=? OR b=?) AND origin='claude_analysis'", (pid, pid))
    for par in parents:
        if par in ok: c.execute("INSERT INTO concept_relations VALUES(?,?,?,?,'claude_analysis')", (pid, 'variant_of', par, 'closely related problem'))
    for rel, items in rels.items():
        for m, note in items:
            if m not in ok: print('unknown concept', m); continue
            c.execute("INSERT INTO concept_relations VALUES(?,?,?,?,'claude_analysis')", (m, rel, pid, note))
c.commit()
print('design problems added:', len(P), ' relations:', q("SELECT count(*) FROM concept_relations WHERE b IN (%s)" % ','.join('?' * len(P)), *P)[0][0])
