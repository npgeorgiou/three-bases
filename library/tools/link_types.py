"""Link types the combo validation set was missing (README suggestion 11): blink, cast from another zone, untap, stat setting,
and expensive cards as the target of ramp. New concepts (Claude's network), their wording patterns (also stored in
concept_patterns), the tags they add (method text_pattern; high_cost: data_rule), and the concept relations that join them to
their enablers and payoffs. Also adds the modern Magic wording "When this creature enters" to on_play (with its trigger ->
effect pairs) and "put ... card from a graveyard onto the battlefield" to revive, both of which the general patterns missed.
Idempotent. Usage: link_types.py <db>"""
import re, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
CON = {
 'blink': ('Blink', 'effect', ['movement', 'effect'], 'Remove a unit and bring it straight back, so it re-enters fresh and repeats its on-enter effect: flicker, blink.',
   [r"exile [^.]{0,60}(,|\.)? ?(then )?return (it|that card|them|those cards|that creature|the exiled card)[^.]{0,30} to the battlefield"]),
 'cast_from_zone': ('Cast from another zone', 'structure', ['structure'], 'Play cards from somewhere other than the hand: from exile, the graveyard or discard pile, or the top of the deck.',
   [r"(you may )?(cast|play) (this card|~|it|cards?|spells?|that card|those cards|the exiled card)[^.]{0,40} from (exile|your graveyard|a graveyard|the graveyard|the top of your library|your discard pile|your deck)",
    r"\bflashback\b", r"\bescape\b(?= ?[—-])", r"\bunearth\b"]),
 'untap': ('Untap / ready again', 'effect', ['extra_turn'], 'Untap or ready a used unit or permanent so its tap ability or action can be used again.',
   [r"(?<!t )\buntap (target|it|all|up to|another|each|that|this|~|those|a|an|two|x)\b"]),
 'stat_set': ('Set stats', 'effect', ['buff', 'debuff'], "Set a unit's attack, health or both to a fixed number: health becomes 1, becomes a 1/1, power set to 3.",
   [r"change the (attack|health|power|toughness)[^.]{0,40} to \d+", r"set [^.]{0,40}(attack|power|health|toughness) to \d+", r"\bbecomes? (a )?\d+/\d+",
    r"\bset [^.]{0,30}to \d+/\d+", r"\bchange [^.]{0,30}to \d+/\d+", r"base (power and toughness|attack and health) \d+/\d+",
    r"\bbase (power|attack|health) (becomes|is) \d+", r"\bhas base (power|toughness) \d+\b"]),   # kept equal to concept_defs.py (12 Oct 2026)
 'attack_now': ('Attack right away', 'combat', ['combat', 'tempo'], 'An effect makes a unit attack at once, outside its normal attack: put into play attacking, an immediate or free attack. Extra attacks per turn are multi_attack; readying a used unit is untap.',
   [r"\b(summon|summons|put|puts|create|creates|play|plays)\b[^.]{0,50}\battacking\b", r"\battacks? immediately\b", r"\bstart a free attack\b"]),
 'type_grant': ('Counts as another type', 'structure', ['tribal'], 'Makes cards count as a type, tribe, colour or faction they are not, or as every type: changeling, all minion types, a chosen colour in addition.',
   [r"\bis every creature type\b", r"\bchangeling\b", r"\ball (minion|creature) types\b", r"\bin addition to (its|their) other (colors|colours|types|creature types)\b",
    r"\bcounts? as (a|an|every|all)\b[^.]{0,20}\b(type|tribe|color|colour|faction|region|creature)\b", r"\bhas all (types|tribes|regions)\b"]),
 'high_cost': ('Expensive card', 'resource', ['economy'], "Cards at the top of their game's cost curve (top 10% of costs in that game): what ramp, cost reduction, cheating into play and reanimation aim for.", []),
}
REL = [('attack_now', 'enables', 'on_attack', 'an immediate attack sets off attack effects'),
       ('haste', 'enables', 'on_attack', 'attacking the turn it arrives sets off attack effects at once'),
       ('type_grant', 'enables', 'tribal', 'cards counting as every type feed type-matters payoffs'),
       ('blink', 'synergizes', 'on_play', 'a returning unit repeats its on-enter effect'),
       ('copy', 'synergizes', 'on_play', 'a copy of a unit repeats its on-enter effect'),
       ('banish', 'enables', 'cast_from_zone', 'exiled cards that can be cast from exile'),
       ('graveyard', 'enables', 'cast_from_zone', 'cards in the graveyard that can be cast from there'),
       ('mill', 'enables', 'cast_from_zone', 'milled cards land where they can be cast'),
       ('untap', 'synergizes', 'activated', 'tap abilities used again'),
       ('stat_set', 'synergizes', 'ping', 'health set low lets small damage finish units'),
       ('stat_set', 'synergizes', 'aoe_damage', 'health set low lets area damage clear the board'),
       ('resource_gain', 'enables', 'high_cost', 'ramp reaches expensive cards sooner'),
       ('cost_reduction', 'enables', 'high_cost', 'cheaper expensive cards'),
       ('free_play', 'enables', 'high_cost', 'cheating an expensive card into play'),
       ('revive', 'enables', 'high_cost', 'reanimating an expensive unit for a low price')]
EXTRA = [('tribal', r"\bshares? (a|any|the same) (color|colour|type|creature type|card type|faction|region|tribe|keyword)\b"),
         ('on_play', r"\bwhen (this|~) (creature|permanent|artifact|enchantment|vehicle|land|minion|unit|follower|card) enters\b"),
         ('revive', r"\bput [^.]{0,50}card[^.]{0,30} from (a|your|an opponent's|any) graveyard onto the battlefield")]
ok = {i for (i,) in q('SELECT id FROM concepts')}
for cid, (name, facet, parents, desc, pats) in CON.items():
    c.execute('INSERT OR REPLACE INTO concepts VALUES(?,?,?,?)', (cid, name, facet, desc))
    for p in parents:
        if p in ok or p in CON: c.execute('INSERT OR IGNORE INTO concept_parents VALUES(?,?)', (cid, p))
    c.execute('DELETE FROM concept_patterns WHERE concept=? AND game IS NULL', (cid,))
    for p in pats: c.execute("INSERT INTO concept_patterns VALUES(?,?,?,NULL)", (cid, 'does', p))
ROLE = {'tribal': 'benefits'}   # "if two cards share a colour" is a payoff for shared types, not a type effect
for con, p in EXTRA:
    if not q('SELECT 1 FROM concept_patterns WHERE concept=? AND pattern=?', con, p): c.execute("INSERT INTO concept_patterns VALUES(?,?,?,NULL)", (con, ROLE.get(con, 'does'), p))
for a, rel, b, note in REL:
    if not q('SELECT 1 FROM concept_relations WHERE a=? AND rel=? AND b=?', a, rel, b): c.execute("INSERT INTO concept_relations VALUES(?,?,?,?,'claude_analysis')", (a, rel, b, note))
# tags from the new and extra patterns (Marvel Snap included; it has its own reviewed tags, these only add)
new = [(cid, re.compile(p, re.I)) for cid, v in CON.items() for p in v[4]] + [(con, re.compile(p, re.I)) for con, p in EXTRA]
ONPLAY = next(p for con, p in EXTRA if con == 'on_play')
effp = []
root = dict(q("SELECT id, root FROM concept_tree WHERE root='effect'"))
for con, p in q("SELECT concept, pattern FROM concept_patterns WHERE role='does' AND game IS NULL"):
    if root.get(con) == 'effect':
        try: effp.append((con, re.compile(p, re.I)))
        except re.error: pass
SPLIT = re.compile(r'(?<=[.!;])\s+|\n+')
c.execute("DELETE FROM entity_concepts WHERE method='text_pattern' AND concept IN (%s)" % ','.join('?' * len(CON)), list(CON))
n = npair = 0
for e, g, t in q("SELECT id, game, text FROM entities WHERE text IS NOT NULL AND category NOT IN ('tribe')"):
    low = t.lower()
    for con, p in new:
        m = p.search(low)
        if m: n += c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, con, ROLE.get(con, 'does') if con not in CON else 'does', 'text_pattern', low[max(0, m.start() - 20): m.start() + 40])).rowcount
    if 'enters' in low and len(low) < 4000:
        for cl in SPLIT.split(low):
            if re.search(ONPLAY, cl):
                for b in {x for x, p in effp if p.search(cl)}:
                    if not q("SELECT 1 FROM trigger_effect WHERE entity=? AND trigger='on_play' AND effect=?", e, b):
                        c.execute("INSERT INTO trigger_effect(entity, game, trigger, effect, clause) VALUES(?,?,?,?,?)", (e, g, 'on_play', b, cl.strip()[:300])); npair += 1
# high_cost: top 10% of costs per game (cards with a numeric cost), role benefits
c.execute("DELETE FROM entity_concepts WHERE concept='high_cost'")
h = 0
for (g,) in q("SELECT DISTINCT game FROM entities WHERE cost_num IS NOT NULL"):
    cs = sorted(x for (x,) in q("SELECT cost_num FROM entities WHERE game=? AND cost_num IS NOT NULL AND category NOT IN ('keyword','tribe')", g))
    if len(cs) < 50: continue
    cut = cs[int(len(cs) * 0.9)]
    if cut <= cs[0]: continue
    h += c.execute("INSERT OR IGNORE INTO entity_concepts SELECT id, 'high_cost', 'benefits', 'data_rule', 'cost ' || cost_num || ' (top 10%% in its game: ' || ? || '+)' FROM entities WHERE game=? AND cost_num>=? AND category NOT IN ('keyword','tribe')".replace('%%', '%'), (cut, g, cut)).rowcount
c.commit()
print('link types: pattern tags', n, ' new on_play pairs', npair, ' high_cost tags', h)
