"""Concept tree v3 (Step 1 of the tag-fix plan, 13 Oct 2026; Claude's design, from the player's point of view).
The tree itself is tools/concept_tree_v3.txt; examples are tools/concept_examples.tsv. This module
  - loads the tree (TREE) and the old -> new concept map (MAP, with the split rules below), for any script that needs them;
  - as a build step (after regression.py enforce, before parent_rule.py) replaces the concepts and concept_parents tables with the
    tree and moves every tag, trigger -> effect pair, concept relation, pattern row and archetype to the new concepts.
The split rules read the card's text with wording made for each concept (who is moved, whose hand, whose deck...).
Earlier build steps still write the old ids (in their vocabulary 'buff' and 'debuff' mean stat gain and stat loss); this step
moves them, so nothing upstream had to change. It logs the tags it moved (tables tree_v3_moved, tree_v3_added, v2_*), and the
first build step undoes that, so every build starts from the old ids and the step stays exact. Trigger -> effect pairs are moved
without a log: trigger_pairs.py keeps existing pairs and only adds, so the moved pairs simply stay. New ids written upstream pass through unchanged.

How old tags move (every old concept maps to one or more new ones; a tag keeps its role, method and evidence):
  rename          buff -> stat_gain, debuff -> stat_loss (buff and debuff are now the wider "stronger / weaker" groups; concept
                  relations about them stay on the groups, which still cover stat gain and loss through the tree)
  removed         stat_set, stat_swap (mechanisms): stat_gain when the target ends up stronger, stat_loss when weaker,
                  both when the card can hit either side. attack_mod (a mixed group): buff for bonuses, debuff for penalties,
                  both when the text has both or neither. control (a vague group): steal for taking control, else hurts_enemy.
  split by side   the text around the tag is read for enemy words (enemy, opponent, foe, their...) and own words (your,
                  friendly, ally, itself, me...): return_to_hand -> bounce_enemy for enemy units; transform -> polymorph for
                  enemy units; movement -> forced_movement for enemy units; discard -> hand_disruption for the opponent's
                  hand; mill -> self_mill for the owner's own deck; recycle -> bounce_enemy for enemy units. Text that names
                  both sides, or a target of either side ("target creature"), gets both.
  carried along   where a move cuts a parent the tag used to imply, the parent is kept as its own tag when the text supports it:
                  aura (now under passive) keeps buff, or gets debuff when it touches enemies; in_hand_buff keeps stat_gain
                  for +stats; sacrifice (no longer a cost) keeps cost_type when it is paid as a cost and gets destroy when
                  the opponent sacrifices; condition_life gives low_life when the player's own life is meant; tutor keeps
                  draw when the card goes to hand; revive keeps summon unless it only returns to hand; copy keeps
                  generate_cards when the copy goes to hand or deck; upgrade keeps buff for units that level up or evolve;
                  merge_attach (now a structure concept) keeps buff, or gets debuff for harmful attachments; variety_payoff
                  keeps deckbuilding_effect for deck rules; autonomous_units keeps random_effect when random; donate gets
                  board_clog for harmful gifts; play_restriction, forced_placement, lane_closure and hand_deck_swap keep
                  disruption when only the opponent is bound; cost_set gets cost_increase on enemy cards; junk_cards put in
                  one's own deck also get drawback; swap gets forced_movement when enemy units are swapped; forced_attack on
                  one's own units becomes drawback ("must attack") or attack_now.
  unchanged id    every other concept (its parents or definition may have changed).
Usage: concept_tree.py <db> restore   (first build step: undoes the last apply, so the earlier steps see the old ids)
       concept_tree.py <db> apply     (after regression.py enforce)"""
import json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def load_tree():
    t = {}
    for line in open(os.path.join(HERE, 'concept_tree_v3.txt'), encoding='utf-8'):
        if not line.strip() or line.startswith('#'): continue
        i, name, facet, par, counts, no = [x.strip() for x in line.split('|')]
        t[i] = dict(name=name, facet=facet, parents=[p for p in par.split(',') if p], counts=counts, no=no)
    return t
TREE = load_tree()

def load_examples():
    ex = {}
    p = os.path.join(HERE, 'concept_examples.tsv')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            if line.startswith('concept\t') or not line.strip(): continue
            k, fit1, fit2, near = (line.rstrip('\n').split('\t') + ['', '', ''])[:4]
            ex[k] = (fit1, fit2, near)
    return ex

def description(i, ex=None):
    d = TREE[i]; s = d['counts'] + ' Not: ' + d['no']
    e = (ex or {}).get(i) or ('', '', '')
    s += (' Fits: ' + '; '.join(x for x in e[:2] if x) + '.') if e[0] else (' No card in the library is linked to it yet.' if TREE[i]['facet'] == 'problem' else '')
    if e[2]: s += ' Looks similar but not: ' + e[2] + '.'
    return s

EN = re.compile(r"\b(enem(y|ies)|opponents?'?s?|opposing|foes?|their|they control|an? opponent controls|target player|that player)\b")
OW = re.compile(r"\b(your|you control|friendly|all(y|ies)|allied|own|yourself|itself|this (unit|minion|creature|card|follower|model|fighter|character)|me|my)\b")
ANY = re.compile(r"\b(target|a|an|another|any|each|all) (minion|creature|unit|follower|card|model|fighter|character|permanent)s?\b")
def side(t):
    e, o = bool(EN.search(t)), bool(OW.search(t))
    return 'both' if e and o else 'enemy' if e else 'own' if o else 'none'
def has(rx, t): return re.search(rx, t) is not None

E_ = r"(enem(y|ies)|opponents?'?s?|opposing|foes?)"
def stat_set(t):
    enemy = has(E_ + r"[^.]{0,40}\b(set|sets|become|becomes|base)\b|\bsets?\b[^.]{0,30}" + E_, t)
    own = has(r"\b(your|friendly|allied|this|itself|namedcard|~|me|my)\b[^.]{0,30}\b(set|sets|become|becomes|base)\b|\bset (its|your|my)\b", t)
    low = has(r"\b(to|becomes?|become a|base) (0|1)\b|\b[01]/[01]\b|\b1\|1\b|(health|attack|power) (is |becomes )?(0|1)\b", t)
    out = ({'stat_loss'} if enemy or low else set()) | ({'stat_gain'} if own else set())
    return out or {'stat_gain', 'stat_loss'}
def stat_swap(t):
    enemy = has(E_ + r"[^.]{0,40}\bswap|\bswap[^.]{0,40}" + E_, t); own = has(r"\b(your|friendly|allied|this|itself|namedcard|~|me|my)\b[^.]{0,30}\bswap|\bswap (its|your|my)\b", t)
    return {'stat_loss'} if enemy and not own else {'stat_gain'} if own and not enemy else {'stat_gain', 'stat_loss'}
def attack_mod(t):
    plus = has(r"\+\d|bonus|re-?roll|improve|increase|better|\badd (1|one|\d)\b", t); minus = has(r"(^|[^\w+])-\d|penalt|subtract|worse|reduce|disadvantage", t)
    return {'buff'} if plus and not minus else {'debuff'} if minus and not plus else {'buff', 'debuff'}
def control(t): return {'steal'} if has(r"gains? control|take control|switch(es)? sides|under your control|charm", t) else {'hurts_enemy'}
def aura(t):
    enemy = has(E_ + r"[^.]{0,40}\b(get|gets|have|has|lose|loses|can'?t|cannot|cost|costs|deal|take)\b|\bgets? -\d", t)
    own = has(r"\b(your|friendly|allied|other|you control)\b[^.]{0,40}\b(get|gets|have|has|gain|gains)\b|\bgets? \+|\+\d", t)
    return {'aura', 'debuff'} if enemy and not own else {'aura', 'buff', 'debuff'} if enemy and own else {'aura', 'buff'}
def in_hand_buff(t): return {'in_hand_buff'} | ({'stat_gain'} if has(r"\+\d|\+x\b|(gains?|gets?|give|have) [^.]{0,25}\b(power|attack|health|stats)\b", t) else set())
def return_to_hand(t):
    enemy = has(r"return[^.]{0,40}\b(enemy|enemies|opponents? controls?|opposing)\b|" + E_ + r"[^.]{0,30}\bto (its|their) (owner'?s?|owners'?) hands?", t)
    own = has(r"return[^.]{0,30}\b(you control|your|friendly|allied|ally|allies|this|itself|namedcard|~|me|it)\b[^.]{0,30}\bhand|recall (an? ally|this|me|it|a unit you)|\breturn (this|it|me|namedcard|~) to (your|my|its owner'?s?) hand", t)
    either = has(r"return (up to (one|two|three|\w+) )?(target|a|an|another|all|each|any)\b[^.]{0,40}\bto (its|their) owners?'? hands?", t)
    return {'bounce_enemy'} if enemy and not own and not either else {'return_to_hand'} if own and not enemy and not either else {'return_to_hand', 'bounce_enemy'}
def sacrifice(t):
    out = {'sacrifice'}
    if has(r"sacrifice[^.:\n]{0,50}:|additional cost|as a cost|sacrifice[^.\n]{0,40}\bto (play|cast|activate|summon)", t): out.add('cost_type')
    if has(r"(?<!whenever )(?<!when )(each opponent|target opponent|target player|each player|each other player|that player) (sacrifices|must sacrifice)|unless[^.]{0,30}(opponent|player) sacrifices", t): out.add('destroy')
    return out
def condition_life(t):
    player = has(r"you have \d+ or (less|fewer) (life|health|hp)|you have [^.]{0,20}\bhp\b|\byour (life|health|hp)\b|\byour (hero|leader)'?s? (health|life|defense)|life total|hero'?s? health|leader'?s? (defense|health)|vengeance|\bat \d+ or (less|fewer) life", t)
    unit = has(r"damaged|wounded|bloodied|enrage|injured|survives? damage|death'?s door", t)
    return {'low_life', 'condition_life'} if player and unit else {'low_life'} if player else {'condition_life'}
def movement(t):
    V = r"\b(push|pushes|pushed|pull|pulls|pulled|knockback|knock back|knocked back|shove|throw|move|moves|relocate|switch)\b"
    enemy = has(V + r"[^.]{0,30}\b(enemy|enemies|opponent'?s?|opposing|target (creature|unit|minion|model|fighter))\b|\b(enemy|opposing)\b[^.]{0,20}\b(unit|minion|model|fighter|creature|card)s?\b[^.]{0,20}\b(is |are )?(moved|pushed|pulled)\b|\bknock(ed)? ?back\b", t)
    own = has(V + r"[^.]{0,30}\b(this|it|me|your|friendly|allied|ally|allies|namedcard|~|yourself|itself)\b|\b(this|it|namedcard|~) (can )?moves?\b|\bmoveable|\bmove (up to )?\d", t)
    return {'forced_movement'} if enemy and not own else {'movement', 'forced_movement'} if enemy and own else {'movement'}
def swap(t): return {'swap', 'forced_movement'} if has(r"\bswap[^.]{0,40}" + E_ + "|" + E_ + r"[^.]{0,40}\bswap", t) else {'swap'}
def transform(t):
    other = has(r"\btransforms? (a|an|target|another|all|each|up to|enemy|enemies)\b|\bturn (a|an|target|all|each|an enemy|enemy)\b[^.]{0,30}\binto\b", t)
    if not other: return {'transform'}
    enemy = has(r"\b(transforms?|turn)\b[^.]{0,20}\b(enemy|enemies|opponent'?s?|opposing)\b|\b(enemy|opponent'?s?) [^.]{0,20}\btransforms?\b", t)
    own = has(r"\b(transforms?|turn)\b[^.]{0,20}\b(friendly|your|allied|ally|you control)\b", t)
    return {'polymorph'} if enemy and not own else {'transform'} if own and not enemy else {'transform', 'polymorph'}
def discard(t):
    enemy = has(r"(opponents?|enemy|each player|target player|that player|each other player)s? (discards?|reveals)|discard[^.]{0,30}\b(opponent|enemy)'?s? hand|from (your opponent'?s?|their|the enemy'?s?|an opponent'?s?) hand", t)
    own = has(r"(?<!opponent )(?<!player )\bdiscard (a|an|one|two|three|x|your|this|that|up to|\d|cards?)\b|\bwhen you discard|\byou discard|each player discards", t)
    return {'hand_disruption'} if enemy and not own else {'discard', 'hand_disruption'} if enemy and own else {'discard'}
def mill(t):
    own = has(r"\byou mill|\bmill (a|an|one|two|three|four|five|six|seven|eight|nine|ten|x|that many|\d+) cards?\b|mills? yourself|\byour (library|deck|draw pile)\b[^.]{0,30}(graveyard|discard)|each player mills", t)
    enemy = has(r"(opponent|target player|each player|that player|each other player)s? mills?|(opponent'?s?|their|enemy) (library|deck)", t)
    return {'self_mill', 'mill'} if own and enemy else {'self_mill'} if own else {'mill'}
def recycle(t): return {'bounce_enemy'} if has(r"shuffle[^.]{0,40}\b(enemy|opponent'?s?|opposing)\b[^.]{0,30}\binto|\b(enemy|opposing)\b[^.]{0,30}\b(into|on (the )?top of|on the bottom of) (its|their) (owner'?s? )?(deck|library)", t) else {'recycle'}
def junk_cards(t):
    own = has(r"\b(into|to|in) your (hand|deck|draw pile|discard pile|library)\b", t); enemy = has(r"\b(into|to|in) (your opponent'?s?|their|the enemy'?s?|enemy|each opponent'?s?|an opponent'?s?) (hand|deck|draw pile|library)", t)
    return {'junk_cards', 'drawback'} if own and not enemy else {'junk_cards'}
def forced_attack(t):
    if has(r"\b(this creature|this unit|this minion|namedcard|~|it) (attacks|must attack)[^.]{0,20}(each|if able)|attacks each (combat|turn) if able|\bmust attack\b", t) and not has(E_, t): return {'drawback'}
    if has(E_, t): return {'forced_attack'}
    return {'attack_now'} if has(r"\byour (minions|units|creatures|followers)\b|\ballies\b", t) else {'forced_attack'}
def tutor(t): return {'tutor', 'draw'} if has(r"\b(into|to) your hand\b|\bdraw\b|add[^.]{0,30}\bto your hand", t) else {'tutor'}
def revive(t):
    hand = has(r"(to|into) (your|its owner'?s?|their|my) hand", t)
    play = has(r"battlefield|summon|resurrect|reanimate|into play|onto the board|to (the )?(play|board)|revive|raise|deploy|return[^.]{0,40}\bto (a|the|its|this) (lane|location|row|zone)", t)
    return {'revive'} if hand and not play else {'revive', 'summon'}
def copy_(t): return {'copy', 'generate_cards'} if has(r"(to|into) your (hand|deck)|add a copy|copy of[^.]{0,40}\b(hand|deck)|shuffle[^.]{0,40}cop", t) else {'copy'}
def upgrade(t): return {'upgrade', 'buff'} if has(r"\blevel|\bevolve|rank up", t) else {'upgrade'}
def merge_attach(t):
    neg = has(r"\b(enchanted|equipped|attached)\b[^.]{0,30}\b(can'?t|cannot|gets? -|loses|doesn'?t untap)|enchant (creature|permanent) an opponent controls", t)
    pos = has(r"\b(enchanted|equipped|attached|bonded|merged)\b[^.]{0,40}\b(gets? \+|has|have|gains?)\b|\bmagnetic\b|\bequip\b", t)
    return {'merge_attach', 'debuff'} if neg and not pos else {'merge_attach', 'buff', 'debuff'} if neg and pos else {'merge_attach', 'buff'}
def variety_payoff(t): return {'variety_payoff', 'deckbuilding_effect'} if has(r"deck (has|contains) no|no duplicates|highlander|singleton|starting deck|in your deck (are|have) different", t) else {'variety_payoff'}
def autonomous_units(t): return {'autonomous_units', 'random_effect'} if 'random' in t else {'autonomous_units'}
def donate(t): return {'donate', 'board_clog'} if has(r"damage|loses?|can'?t|cannot|(^|[^\w+])-\d|destroy|curse", t) else {'donate'}
def enemy_only(base, extra):
    return lambda t: {base, extra} if side(t) == 'enemy' else {base}
def cost_set(t): return {'cost_set', 'cost_increase'} if has(E_ + r"[^.]{0,40}\bcosts?\b", t) and not has(r"\byour\b[^.]{0,30}\bcosts?\b", t) else {'cost_set'}

MAP = {
 'buff': lambda t: {'stat_gain'}, 'debuff': lambda t: {'stat_loss'},
 'stat_set': stat_set, 'stat_swap': stat_swap, 'attack_mod': attack_mod, 'control': control,
 'aura': aura, 'in_hand_buff': in_hand_buff, 'return_to_hand': return_to_hand,
 'sacrifice': sacrifice, 'condition_life': condition_life, 'movement': movement, 'swap': swap,
 'transform': transform, 'discard': discard, 'mill': mill, 'recycle': recycle,
 'junk_cards': junk_cards, 'forced_attack': forced_attack, 'tutor': tutor, 'revive': revive, 'copy': copy_,
 'upgrade': upgrade, 'merge_attach': merge_attach, 'variety_payoff': variety_payoff, 'autonomous_units': autonomous_units,
 'donate': donate, 'play_restriction': enemy_only('play_restriction', 'disruption'),
 'forced_placement': enemy_only('forced_placement', 'disruption'), 'lane_closure': enemy_only('lane_closure', 'disruption'),
 'hand_deck_swap': enemy_only('hand_deck_swap', 'disruption'), 'cost_set': cost_set,
}
# what an old concept can become at most (for relations, patterns, archetypes, the regression set): its main targets only,
# not the parents carried along for single tags
PRIMARY = {'buff': ['stat_gain'], 'debuff': ['stat_loss'], 'stat_set': ['stat_gain', 'stat_loss'], 'stat_swap': ['stat_gain', 'stat_loss'],
           'attack_mod': ['buff', 'debuff'], 'control': ['hurts_enemy', 'steal'], 'condition_life': ['condition_life', 'low_life'],
           'return_to_hand': ['return_to_hand', 'bounce_enemy'], 'transform': ['transform', 'polymorph'],
           'movement': ['movement', 'forced_movement'], 'discard': ['discard', 'hand_disruption'], 'mill': ['mill', 'self_mill'],
           'recycle': ['recycle', 'bounce_enemy'], 'forced_attack': ['forced_attack', 'attack_now', 'drawback']}
REMOVED = {'stat_set', 'stat_swap', 'attack_mod', 'control'}

def primary(k): return PRIMARY.get(k, [k])
# a concept relation about old 'buff' / 'debuff' ("buff synergizes stat_condition") holds for the whole new group, which still
# covers stat gain and stat loss through the tree
def rel_primary(k): return {'buff': ['buff'], 'debuff': ['debuff']}.get(k) or primary(k)
def targets(k, text):
    """New concepts for one old tag; text is the clause or card text around it."""
    f = MAP.get(k)
    return f((text or '').lower()) if f else {k}

def clause(ev, text):
    """The sentence of the entry's text that holds the tag's evidence (the whole text when it can't be found)."""
    t = (text or '').lower(); e = (ev or '').lower().strip()
    if len(e) >= 8:
        i = t.find(e[:40])
        if i >= 0:
            a = max(t.rfind('.', 0, i), t.rfind('\n', 0, i)) + 1
            b = min([x for x in (t.find('.', i + len(e[:40])), t.find('\n', i + len(e[:40]))) if x >= 0] or [len(t)])
            return t[a:b + 1]
        return e
    return t

V2 = ['concepts', 'concept_parents', 'concept_relations', 'concept_patterns', 'archetypes']

def restore(c):
    """Undo the last apply (first build step): the earlier steps work in the old ids and re-derive their tags each build."""
    q = lambda s, *a: c.execute(s, a).fetchall()
    if not q("SELECT 1 FROM sqlite_master WHERE name='tree_v3_moved'"): return 0
    live = {e for e, in q('SELECT id FROM entities')}
    kept = {o: k for o, k in q('SELECT old_id, kept_id FROM merged_entities') if o not in live} if q("SELECT 1 FROM sqlite_master WHERE name='merged_entities'") else {}
    c.execute('DELETE FROM entity_concepts WHERE rowid IN (SELECT ec.rowid FROM entity_concepts ec JOIN tree_v3_added a ON a.entity=ec.entity AND a.concept=ec.concept AND a.role=ec.role)')
    for e, k, r, m, ev in q('SELECT * FROM tree_v3_moved'):
        c.execute('INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)', (kept.get(e, e), k, r, m, ev))
    # trigger -> effect pairs are not put back: trigger_pairs.py keeps existing rows and adds the old-id pairs again, and apply
    # moves those onto the rows that are already there
    for t in V2:
        c.execute('DELETE FROM %s' % t); c.execute('INSERT INTO %s SELECT * FROM v2_%s' % (t, t)); c.execute('DROP TABLE v2_%s' % t)
    for t in ['tree_v3_moved', 'tree_v3_added']: c.execute('DROP TABLE %s' % t)
    c.commit(); return 1

def apply(c):
    q = lambda s, *a: c.execute(s, a).fetchall()
    ex = load_examples()
    for t in V2: c.execute('DROP TABLE IF EXISTS v2_%s' % t); c.execute('CREATE TABLE v2_%s AS SELECT * FROM %s' % (t, t))
    c.execute('CREATE TABLE tree_v3_moved(entity INTEGER, concept TEXT, role TEXT, method TEXT, evidence TEXT)')
    c.execute('CREATE TABLE tree_v3_added(entity INTEGER, concept TEXT, role TEXT, source TEXT)')
    c.execute('DELETE FROM concepts'); c.execute('DELETE FROM concept_parents')
    c.executemany('INSERT INTO concepts VALUES(?,?,?,?)', [(i, d['name'], d['facet'], description(i, ex)) for i, d in TREE.items()])
    c.executemany('INSERT INTO concept_parents VALUES(?,?)', [(i, p) for i, d in TREE.items() for p in d['parents']])
    text = dict(q('SELECT id, text FROM entities'))
    old = set(MAP) | REMOVED
    kept = dict(q('SELECT old_id, kept_id FROM merged_entities')) if q("SELECT 1 FROM sqlite_master WHERE name='merged_entities'") else {}
    import csv
    rev = [r for r in csv.DictReader(open(os.path.join(HERE, 'regression.tsv'), encoding='utf-8'), delimiter='\t')]
    for r in rev: r['e'] = kept.get(int(r['entity']), int(r['entity']))
    # a split rule never adds a concept a hand review dropped from that entry (except the plan's own rule for the removed mechanisms)
    dropped = {(r['e'], primary(r['concept'])[0]) for r in rev if r['expect'] == 'absent' and r['concept'] not in REMOVED}
    moved = {}
    for rid, e, k, role, m, ev in q('SELECT rowid, entity, concept, role, method, evidence FROM entity_concepts WHERE concept IN (%s)' % ','.join('?' * len(old)), *old):
        new = targets(k, text.get(e))
        if k not in REMOVED:
            new = {n for n in new if n == k or (e, n) not in dropped}
            if not new & set(primary(k)): new.add(k)   # nothing it may move to: it stays as it is
        if k not in new:
            c.execute('DELETE FROM entity_concepts WHERE rowid=?', (rid,)); c.execute('INSERT INTO tree_v3_moved VALUES(?,?,?,?,?)', (e, k, role, m, ev))
        for n in new - {k}:
            if c.execute('INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)', (e, n, role, m, ev)).rowcount:
                c.execute('INSERT INTO tree_v3_added VALUES(?,?,?,?)', (e, n, role, k)); moved[k, n] = moved.get((k, n), 0) + 1
    # a tag a hand review judged right is never lost through the move: where none of its new concepts (or narrower ones) is left
    # on the entry, it is kept as its own tag
    desc = {}
    for root, i in q('SELECT root, id FROM concept_tree'): desc.setdefault(root, set()).add(i)
    have = {}
    for e, k, role in q('SELECT entity, concept, role FROM entity_concepts'): have.setdefault(e, set()).add((k, role))
    kept_n = 0
    for r in rev:
        if r['expect'] != 'present' or r['e'] not in text: continue
        e, k = r['e'], r['concept']; ps = primary(k)
        roles = {ro for _, ro in have.get(e, ())} if r['role'] == '*' else {r['role']}
        if any((d, ro) in have.get(e, ()) for p in ps for d in desc.get(p, {p}) for ro in roles): continue
        ok = [p for p in ps if (e, p) not in dropped] or ps[:1]
        new = (targets(k, text.get(e)) & set(ok)) or set(ok[:1])
        role = r['role'] if r['role'] != '*' else 'does'
        for n in new:
            if c.execute('INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)', (e, n, role, 'claude_review', 'hand review, kept through the concept tree move')).rowcount:
                c.execute('INSERT INTO tree_v3_added VALUES(?,?,?,?)', (e, n, role, 'review:' + k)); kept_n += 1; have.setdefault(e, set()).add((n, role))
    te = 0
    for row in q('SELECT rowid, entity, game, trigger, effect, clause, frequency, basis FROM trigger_effect WHERE trigger IN (%s) OR effect IN (%s)' % (','.join('?' * len(old)), ','.join('?' * len(old))), *old, *old):
        rid, e, g, t, f, cl, fr, b = row
        ts = targets(t, cl) if t in old else {t}; fs = targets(f, cl) if f in old else {f}
        c.execute('DELETE FROM trigger_effect WHERE rowid=?', (rid,)); te += 1
        for a in ts:
            for z in fs:
                if not q('SELECT 1 FROM trigger_effect WHERE entity=? AND trigger=? AND effect=? AND clause IS ?', e, a, z, cl):
                    c.execute('INSERT INTO trigger_effect(entity, game, trigger, effect, clause, frequency, basis) VALUES(?,?,?,?,?,?,?)', (e, g, a, z, cl, fr, b))
    rel = q('SELECT a, rel, b, note, origin FROM concept_relations'); c.execute('DELETE FROM concept_relations'); seen = set()
    for a, r, b, note, o in rel:
        for x in rel_primary(a):
            for y in rel_primary(b):
                if x != y and (x, r, y) not in seen: seen.add((x, r, y)); c.execute('INSERT INTO concept_relations VALUES(?,?,?,?,?)', (x, r, y, note, o))
    pat = q('SELECT concept, role, pattern, game FROM concept_patterns'); c.execute('DELETE FROM concept_patterns'); seen = set()
    for k, r, p, g in pat:
        for x in primary(k):
            if (x, r, p, g) not in seen: seen.add((x, r, p, g)); c.execute('INSERT INTO concept_patterns VALUES(?,?,?,?)', (x, r, p, g))
    for a, js in q('SELECT id, concepts FROM archetypes'):
        new = []
        for k in json.loads(js):
            for x in primary(k):
                if x not in new: new.append(x)
        c.execute('UPDATE archetypes SET concepts=? WHERE id=?', (json.dumps(new), a))
    bad = [k for k, in q('SELECT DISTINCT concept FROM entity_concepts WHERE concept NOT IN (SELECT id FROM concepts)')]
    bad += [k for k, in q('SELECT DISTINCT trigger FROM trigger_effect WHERE trigger NOT IN (SELECT id FROM concepts) UNION SELECT DISTINCT effect FROM trigger_effect WHERE effect NOT IN (SELECT id FROM concepts)')]
    c.commit()
    nm = q('SELECT count(*) FROM tree_v3_moved')[0][0]
    print('concept tree v3:', len(TREE), 'concepts; tags moved', nm, ', added', sum(moved.values()), ', reviewed tags kept', kept_n, '; pairs rewritten', te, '; unknown concepts', sorted(set(bad)))
    return bad

if __name__ == '__main__':
    c = sqlite3.connect(sys.argv[1])
    if sys.argv[2:] == ['restore']: print('concept tree v3: restored the old ids' if restore(c) else 'concept tree v3: nothing to restore')
    elif sys.argv[2:] == ['apply']:
        if apply(c): sys.exit(1)
    else: sys.exit('usage: concept_tree.py <db> restore|apply')
