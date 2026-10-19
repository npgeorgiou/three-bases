"""Concept definitions fixed on 12 Oct 2026 (Claude's review of all 277 definitions; build step, idempotent).
A definition that overlapped another concept, or covered more than its name says, is narrowed; a parent that the child does not
imply is replaced, so the parent and child rule (parent_rule.py) never removes a correct tag. The general wording patterns
(game NULL) of the narrowed concepts are rewritten to match, and those concepts are re-derived on every entry (Marvel Snap
excluded: it has its own tagging). Hand-reviewed tags (regression.tsv) are kept. Usage: concept_defs.py <db>"""
import csv, os, re, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
DESC = {
 'stat_swap': 'Swap two stats with each other, on one unit or between units: swap attack and health, swap power and cost. Setting stats to a fixed value is stat_set.',
 'stat_set': "Set a unit's attack, health or both to a fixed number: health becomes 1, becomes a 1/1, power set to 3.",
 'swap': 'Swap the positions of two units, or of units between lanes or locations. Stat swaps are stat_swap; hand and deck swaps are hand_deck_swap.',
 'haste': 'Can attack or act the turn it arrives: haste, rush, charge.',
 'attack_now': 'An effect makes a unit attack at once, outside its normal attack: put into play attacking, an immediate or free attack. Extra attacks per turn are multi_attack; readying a used unit is untap.',
 'immunity': "Immune or untargetable: immune, can't be targeted, hexproof. Hard to block (elusive) is evasion.",
 'bodyguard': 'Protect a specific ally by taking its hits or redirecting attacks or damage from it: guard an ally, bodyguard, intercept. Forcing all attacks onto itself is taunt.',
 'draw': 'Draw cards from your deck.',
 'cost_reduction': 'Make cards cost less by an amount: discounts, cost reduction. Free plays are free_play; a cost set to 0 is cost_set.',
 'reveal_order': 'Effects that depend on or change the order in which the players act or reveal: who reveals or acts first, priority, initiative. The order of your own plays is combo_sequence.',
}
PARENTS = {   # child: parents (the child must imply each parent)
 'stat_set': ['buff', 'debuff'],          # was under stat_swap
 'attack_now': ['combat', 'tempo'],       # was under haste: an effect that makes a unit attack is not haste
 'bodyguard': ['protection'],             # was under taunt
 'generate_cards': ['card_advantage'],    # was under draw: creating a card is not drawing
 'deck_condition': ['condition'],         # was under deck_modification: caring about the deck does not change it
 'distribute': ['effect'],                # was under buff: damage can be distributed too
 'modal_choice': ['effect'],              # was under selection (card selection)
 'mark_target': ['condition'],            # was under combo_sequence (order of plays)
 'damage_types': ['combat'],              # was under damage: a resistance deals no damage
 'cross_lane': ['lanes'],                 # was under scope_multi: moving to another lane is not multi-target
 'deck_modification': ['card_flow'],      # was under run_structure and permanent_growth: adding a card to a deck is neither
 'junk_cards': ['card_flow'],             # was under drawback and disruption: junk can go to either player's deck
 'mill': ['card_flow'],                   # was also under alt_wincon: milling is a win condition only in some games
}
PATS = {   # general patterns (game NULL), replacing the old ones
 'stat_swap': [r'\b(switch|swap|exchange)(es|s)? [^.]{0,30}\b(attack|power) and (health|toughness|defen[cs]e|cost)\b',
               r'\b(swap|switch|exchange)(es|s)? [^.]{0,30}\b(power|attack|health|toughness|stats)\b[^.]{0,30}\b(of|with)\b',
               r'\b(switch|swap|exchange)(es|s)? [^.]{0,30}\b(health|toughness) and (attack|power)\b'],
 'stat_set': [r'change the (attack|health|power|toughness)[^.]{0,40} to \d+', r'set [^.]{0,40}(attack|power|health|toughness) to \d+',
              r'\bbecomes? (a )?\d+/\d+', r'\bset [^.]{0,30}to \d+/\d+', r'\bchange [^.]{0,30}to \d+/\d+',
              r'base (power and toughness|attack and health) \d+/\d+', r'\bbase (power|attack|health) (becomes|is) \d+', r'\bhas base (power|toughness) \d+\b'],
 'swap': [r'\b(swap|switch|exchange)(es|s)? (their |its |the )?(places|positions|lanes|locations)\b', r'\b(swap|switch|exchange)(es|s)? (the )?(positions?|places) of\b',
          r'\bswap (me|this|it|itself|name) with (a|an|the|another|target)\b(?![^.]{0,40}\b(hand|deck|tavern)\b)',
          r'\bswap (two|2) (allies|allied \w+|units|minions|creatures|followers|fighters|enemies|enemy \w+)\b'],
 'attack_now': [r'\b(summon|summons|put|puts|create|creates|play|plays)\b[^.]{0,50}\battacking\b', r'\battacks? immediately\b', r'\bstart a free attack\b'],
 'immunity': [r'\bimmune\b', r'\bimmunity\b', r"can't be targeted", r'\bhexproof\b', r'\bshroud\b', r'\buntargetable\b',
              r'\binvulnerab(le|ility)\b(?! saves?)', r"can't be attacked", r'cannot be attacked'],
 'cost_reduction': [r'costs? \{\d+\} less', r'cost \{\d+\} less', r'costs? \(?\d+\)? less', r'costs? less', r'costs? \(?\d+\)? (?!or )\w+ less',
                    r'reduce .{0,20}cost', r'\bcost reduction', r'\bdiscount'],
 'cost_type': [r'as an additional cost', r'instead of paying', r'\balternative cost', r'pay .{0,10}(life|health)', r'rather than pay'],
}
REL = [('heal', 'synergizes', 'life_payment', 'gained life pays life costs')]   # Claude's analysis
for a, r, b, n in REL:
    if not q('SELECT 1 FROM concept_relations WHERE a=? AND rel=? AND b=?', a, r, b): c.execute('INSERT INTO concept_relations VALUES(?,?,?,?,?)', (a, r, b, n, 'claude_analysis'))
EXTRA = {'steal': [r'\bexchange control of\b']}   # general patterns added next to the existing ones (role does)
for cid, d in DESC.items(): c.execute('UPDATE concepts SET description=? WHERE id=?', (d, cid))
for cid, ps in PARENTS.items():
    c.execute('DELETE FROM concept_parents WHERE child=?', (cid,))
    for p in ps: c.execute('INSERT INTO concept_parents VALUES(?,?)', (cid, p))
ROLE = {'cost_type': 'cost'}   # the role the general patterns give (default does)
role = lambda k: ROLE.get(k, 'does')
old = {}
for k, p, r in q("SELECT concept, pattern, role FROM concept_patterns WHERE game IS NULL"):
    if r == role(k): old.setdefault(k, set()).add(p)
added = {k: [re.compile(p, re.I) for p in ps if p not in old.get(k, set())] for k, ps in PATS.items()}
removed = {k: [(None, re.compile(p, re.I)) for p in old.get(k, set()) - set(ps)] for k, ps in PATS.items()}
here = os.path.dirname(os.path.abspath(__file__)); filep = {}
for f in os.listdir(os.path.join(here, 'patterns')):
    if not f.endswith('.txt') or f == '_all.txt': continue
    for line in open(os.path.join(here, 'patterns', f), encoding='utf-8'):
        x = line.rstrip('\n').split('|', 2)
        if len(x) == 3 and x[0] in PATS and x[1] == role(x[0]): filep.setdefault(x[0], set()).add((f[:-4], x[2]))
for k, p, g, r in q("SELECT concept, pattern, game, role FROM concept_patterns WHERE game IS NOT NULL"):
    if k in PATS and r == role(k) and (g, p) not in filep.get(k, set()): removed[k].append((g, re.compile(p, re.I)))
for cid, ps in PATS.items():
    c.execute("DELETE FROM concept_patterns WHERE concept=? AND game IS NULL", (cid,))
    for p in ps: c.execute("INSERT INTO concept_patterns VALUES(?,?,?,NULL)", (cid, role(cid), p))
kept = dict(q('SELECT old_id, kept_id FROM merged_entities')) if q("SELECT 1 FROM sqlite_master WHERE name='merged_entities'") else {}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from concept_tree import to_old as _to_old
reviewed = {(kept.get(int(r['entity']), int(r['entity'])), _to_old(r['concept'])) for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'regression.tsv'), encoding='utf-8'), delimiter='\t') if r['expect'] == 'present'}
pats = {}
for con, p in q("SELECT concept, pattern FROM concept_patterns WHERE game IS NULL AND concept IN (%s)" % ','.join('?' * len(PATS)), *PATS): pats.setdefault(con, []).append((None, re.compile(p, re.I)))
for con, s in filep.items():
    for g, p in s: pats.setdefault(con, []).append((g, re.compile(p, re.I)))
gain = {k: 0 for k in PATS}; lose = {k: 0 for k in PATS}
have = {(e, k) for e, k, r in q("SELECT entity, concept, role FROM entity_concepts WHERE concept IN (%s)" % ','.join('?' * len(PATS)), *PATS) if r == role(k)}
tp = {(e, k) for e, k, r in q("SELECT entity, concept, role FROM entity_concepts WHERE method='text_pattern' AND concept IN (%s)" % ','.join('?' * len(PATS)), *PATS) if r == role(k)}
for e, g, t, nm in q("SELECT id, game, text, name FROM entities WHERE text IS NOT NULL AND game != 'marvel_snap' AND category NOT IN ('tribe')"):
    low = t.lower()
    if g == 'mtg': low = re.sub(r'\([^()]*\)', ' ', low)
    for x in [nm] + nm.split(' // '):
        if len(x) > 2: low = low.replace(x.lower(), 'name')
    for k, ps in pats.items():   # only what the changed patterns change: a new pattern adds, a removed one takes its tags away
        m = next((m for p in added[k] for m in [p.search(low)] if m), None)
        if m and (e, k) not in have:
            gain[k] += c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, k, role(k), 'text_pattern', low[max(0, m.start() - 20): m.start() + 40])).rowcount
        elif (e, k) in tp and (e, k) not in reviewed and any(gg in (None, g) and p.search(low) for gg, p in removed[k]) and not any(p.search(low) for gg, p in ps if gg in (None, g)):
            lose[k] += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND role=? AND method='text_pattern'", (e, k, role(k))).rowcount
for k, ps in EXTRA.items():
    new = [p for p in ps if not q("SELECT 1 FROM concept_patterns WHERE concept=? AND game IS NULL AND pattern=?", k, p)]
    for p in new: c.execute("INSERT INTO concept_patterns VALUES(?,?,?,NULL)", (k, 'does', p))
    comp = [re.compile(p, re.I) for p in new]
    if not comp: continue
    for e, t in q("SELECT id, text FROM entities WHERE text IS NOT NULL AND game != 'marvel_snap' AND category NOT IN ('tribe')"):
        m = next((m for p in comp for m in [p.search(t.lower())] if m), None)
        if m: gain[k] = gain.get(k, 0) + c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, k, 'does', 'text_pattern', t.lower()[max(0, m.start() - 20): m.start() + 40])).rowcount
c.commit()
print('concept definitions fixed:', len(DESC), ' parents:', len(PARENTS), ' gained:', {k: v for k, v in gain.items() if v}, ' lost:', {k: v for k, v in lose.items() if v})
