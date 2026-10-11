"""Add Marvel Snap to the Three Bases inspiration library (Library.sqlite). Re-runnable: it replaces the game's rows.
Usage: python3 -I load_snap.py <Library.sqlite> <cards.json> [locations.json|-] [review.json]
Every card in the source is kept (released, unreleased, created/token and mode-variant cards), with its full source record."""
import json, re, sqlite3, sys, os

DB, SRC = sys.argv[1], sys.argv[2]
LOC = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '-' else None
REVIEW = sys.argv[4] if len(sys.argv) > 4 else None
G = 'marvel_snap'
c = sqlite3.connect(DB)
q = lambda s, *a: c.execute(s, a).fetchall()

# ---------- clean re-run ----------
for (i,) in q("select id from entities where game=?", G):
    c.execute("insert into entity_fts(entity_fts,rowid,name,text) select 'delete',id,name,text from entities where id=?", (i,))
    c.execute("delete from entity_concepts where entity=?", (i,))
    c.execute("delete from trigger_effect where entity=?", (i,))
    c.execute("delete from entity_links where src=? or dst=?", (i, i))
for t in ['entities', 'load_log', 'factions', 'faction_archetypes', 'concept_patterns']:
    c.execute(f"delete from {t} where game=?", (G,))
c.execute("delete from games where id=?", (G,))

c.execute("insert into games values(?,?,?,?,?,?,?)", (
    G, 'Marvel Snap', 'Marvel Snap', 'full card list as of 5 Oct 2026 (released, unreleased, created and mode cards)' + (' and locations' if LOC else ''),
    'cards: cards.json from github.com/ineffectivecoder/snap-dossier (commit of 5 Oct 2026), a marvelsnapzone.com export'
    + ('; locations: marvelsnapzone.com locations list (name, tier, rarity, effect) copied by Kaptain on 11 Oct 2026' if LOC else ''),
    'Two-player card game of about six turns played over three lanes called locations; each location is revealed on '
    'turns 1-3 and carries its own rule; energy equals the turn number; both players play face down at the same time, '
    'then cards reveal, the player winning more locations first; each side holds at most 4 cards per location; '
    "a card's power is its points; whoever has more total power at a location wins it, and winning 2 of 3 locations "
    'wins the game; players can Snap to double the stakes or retreat early. No factions; cards come in series (pools).',
    "Nothing is dropped. The source has no keyword glossary, so keyword definitions are Claude's inference from how "
    "cards use them. Flavour text, art URL and source status are kept in each entry's extra field. Concept tags: "
    'general patterns, Marvel Snap patterns (concept_patterns rows with game marvel_snap), keywords, and a Claude review '
    'of every card (method claude_review).' + ('' if LOC else ' Locations are not loaded yet.')))

def log(step, n, note=''):
    c.execute("insert into load_log values(?,?,?,?)", (G, step, n, note))

nid = [q("select max(id) from entities")[0][0]]
COLS = ['id', 'game', 'ext_id', 'name', 'category', 'source_type', 'edition', 'faction', 'subtypes', 'rarity',
        'cost', 'cost_num', 'stats', 'text', 'extra', 'variants']
def add_entity(**f):
    nid[0] += 1
    row = {'id': nid[0], 'game': G, **f}
    c.execute(f"insert into entities({','.join(COLS)}) values({','.join('?' * len(COLS))})", [row.get(k) for k in COLS])
    c.execute("insert into entity_fts(rowid,name,text) values(?,?,?)", (nid[0], row.get('name'), row.get('text')))
    return nid[0]

def tag(e, concept, role, method, ev=None):
    c.execute("insert or ignore into entity_concepts values(?,?,?,?,?)", (e, concept, role, method, ev))
def link(a, rel, b, ev):
    if a != b: c.execute("insert or ignore into entity_links values(?,?,?,?)", (a, rel, b, ev))

# ---------- keywords (Claude's definitions; the source has none) ----------
KW = {
    'On Reveal': ('Triggers once, when the card is revealed after being played.', [('on_play', 'does')], r'on reveal'),
    'Ongoing': ('A continuous effect that applies while the card is on the board.', [('passive', 'does')], r'ongoing'),
    'Activate': ('An effect the player triggers once, on a later turn of their choosing, after the card is revealed.',
                 [('activated', 'does'), ('once_per_game', 'does')], r'activate'),
    'End of Turn': ('Triggers at the end of each turn while the card is on the board.', [('turn_end', 'does')], r'end of turn'),
    'Start of Turn': ('Triggers at the start of each turn while the card is on the board.', [('turn_start', 'does')], r'start of turn'),
    'Game Start': ('Triggers at the start of the game, from the deck or hand.', [('start_of_game', 'does')], r'game start'),
    'When Destroyed': ('Triggers when the card is destroyed.', [('death_trigger', 'does')], r'when (discarded or )?destroyed'),
    'When Discarded': ('Triggers when the card is discarded from hand.', [('discard', 'benefits')], r'when discarded( or destroyed)?'),
    'Objective': ('A goal written on the card with a progress counter; reaching it gives the reward that follows.',
                  [('quests', 'does')], r'objective'),
    'Moveable': ('The card can be moved once per turn by its player (a move ability on the card).', [('movement', 'does')], r'moveable'),
    'Quickdraw': ('An alternative, stronger effect written after the word, which applies under a condition the game sets '
                  '(the condition is not in the source).', [('condition', 'does')], r'quickdraw'),
    'Empowered': ('Triggers when the card gains power while in hand, deck or play (as written on the card).', [('buff', 'benefits')], r'empowered'),
    'Horde': ('Adds power to a separate Zombie Horde of its player (a mode mechanic; its exact rules are not in the source).',
              [('summon', 'does'), ('permanent_growth', 'does')], r'\bhorde\b'),
    'Destroy': ('Removes a card from the board.', [('destroy', 'does')], None),
    'Discard': ('Removes a card from a hand.', [('discard', 'does')], None),
    'Move': ('A card changes location after it is revealed.', [('movement', 'does')], None),
    'Merge': ('Two cards become one, adding their power.', [('merge_attach', 'does')], None),
    'Afflict': ('Lowers the power of cards (as an ongoing or one-time debuff).', [('debuff', 'does')], None),
}
LABEL = {k: re.compile(r'(^|[.):] *|\s)' + v[2] + r'(\s+(and|or)\s+[a-z ]+?)?\s*:', re.I) for k, v in KW.items() if v[2] and k not in ('Moveable', 'Empowered', 'Horde')}
LABEL['Moveable'] = re.compile(r'\b(is|are|becomes?) moveable|\bmoveable\b(?! card)', re.I)
LABEL['Empowered'] = re.compile(r'when (this|it) is empowered', re.I)
LABEL['Horde'] = re.compile(r'\bhorde \+\d', re.I)
VERB = {'Destroy': r'\bdestroy(?!ed\b)', 'Discard': r'\bdiscard(?!ed\b)', 'Move': r'\bmoves?\b(?! this game)', 'Merge': r'\bmerges?\b', 'Afflict': r'\bafflict'}
kwid = {}
for name, (d, cs, _) in KW.items():
    e = add_entity(ext_id='kw:' + name, name=name, category='keyword', source_type='keyword (no definition in source; Claude inference)', text=d)
    kwid[name] = e
    for con, role in cs: tag(e, con, role, 'claude_inference')
others = {}
for (o, con) in q("select ec.entity, ec.concept from entity_concepts ec join entities e on e.id=ec.entity "
                  "where e.category='keyword' and e.game!=? and ec.method='claude_review' and ec.role='does'", G):
    others.setdefault(o, set()).add(con)
for name, (d, cs, _) in KW.items():
    want = {x for x, r in cs if r == 'does'}
    if not want or name in VERB: continue
    for o, have in others.items():
        if have == want:
            link(kwid[name], 'equivalent_keyword', o, 'same mechanic (Claude)'); link(o, 'equivalent_keyword', kwid[name], 'same mechanic (Claude)')
log('keywords (definitions are Claude inference)', len(KW))

# ---------- Marvel Snap wording the general patterns miss ----------
SNAP_PATTERNS = [
    ('buff', 'does', r'\+\d+ power'), ('buff', 'does', r'double (its|their|this|the|your)[^.]{0,30}power'),
    ('debuff', 'does', r'-\d+ power'), ('debuff', 'does', r'\bloses? \d+ power'), ('debuff', 'does', r'\bafflict'),
    ('permanent_growth', 'does', r'(whenever|each time|after|end of turn|start of turn)[^.]{0,80}(this|it|this card) (gains|gets) \+\d+ power'),
    ('permanent_growth', 'does', r'(end of turn|start of turn)\s*~?[^.]{0,10}\+\d+ power'),
    ('temporary_buff', 'does', r'\+\d+ power[^.]{0,30}(this turn|until)'),
    ('destroy', 'benefits', r'\b(is|are|was|were|gets?) destroyed'), ('destroy', 'benefits', r'destroyed this game'),
    ('death_count', 'does', r'(for each|number of)[^.]{0,40}destroyed'), ('death_count', 'does', r'destroyed[^.]{0,20}this game'),
    ('sacrifice', 'does', r'destroy (one of |another of |a card of )?(your|yours)\b'), ('sacrifice', 'does', r'destroy (a|another|one) (other )?(card|character) you'),
    ('self_destruct', 'does', r'destroy (this|itself)'), ('self_destruct', 'does', r'this (is|gets) destroyed'),
    ('discard', 'benefits', r'(after|when|whenever) you discard'), ('discard', 'benefits', r'discarded( cards)? this game'),
    ('movement', 'benefits', r'(after|when|whenever|each time)[^.]{0,30}\bmoves?\b'), ('movement', 'benefits', r'moved this (game|turn)'),
    ('forced_movement', 'does', r'move (an?|the|all|each)?\s*(enemy|opposing|of your opponent)'), ('forced_movement', 'does', r"move[^.]{0,30}opponent's"),
    ('return_to_hand', 'does', r'return[^.]{0,40}to (your|their|its owner.s) hand'), ('return_to_hand', 'does', r'\bbounce'),
    ('generate_cards', 'does', r'\badd [^.]{0,60}(to|into) (your|their|both|each player.s|all) (hands?|decks?)'),
    ('summon', 'does', r'\badd [^.]{0,60}(to|at) (this|each|a|another|other|the|that|its|every|random|any)[^.]{0,20}locations?'),
    ('summon', 'does', r'\badd [^.]{0,40}\bhere\b'), ('summon', 'does', r'\b(create|summon|spawn)s? [^.]{0,40}(here|location)'),
    ('junk_cards', 'does', r"(add|shuffle|put)[^.]{0,40}(to|into) (your )?opponent'?s (hand|deck)"),
    ('generate_cards', 'does', r'\b(create|put) [^.]{0,40}(into|in) (your|their) (hand|deck)'),
    ('copy', 'does', r'\bcop(y|ies)\b'), ('copy', 'does', r'\bclone'),
    ('transform', 'does', r'\btransforms?\b'), ('transform', 'does', r'\breplace (this|it|them|a|an|each)'), ('transform', 'does', r'\bturn (it|them|this) into'),
    ('merge_attach', 'does', r'\bmerge'), ('merge_attach', 'does', r'\battach'),
    ('draw', 'does', r'\bdraws?\b'), ('tutor', 'does', r'draw (a|your|the|their)[^.]{0,30}(cost|highest|lowest|power|character|card that)'),
    ('deck_modification', 'does', r'shuffle[^.]{0,40}into (your|their|the) deck'), ('deck_modification', 'does', r'\binto (your|their) deck'),
    ('cost_reduction', 'does', r'costs? \d+ less'), ('cost_reduction', 'does', r'-\d+ cost'), ('cost_reduction', 'does', r'cost 0\b'),
    ('cost_increase', 'does', r'costs? \d+ more'), ('cost_increase', 'does', r'\+\d+ cost'),
    ('cost_set', 'does', r'set[^.]{0,30}cost'), ('cost_set', 'does', r'(costs?|cost of) become'),
    ('resource_gain', 'does', r'\+\d+ (max )?energy'), ('resource_gain', 'does', r'(gain|get) \d+ energy'),
    ('resource_banking', 'does', r'unspent energy'), ('resource_banking', 'does', r'energy (next turn|left)'),
    ('play_restriction', 'does', r"can't (be )?play"), ('play_restriction', 'does', r"cards can't be played"), ('play_restriction', 'does', r'(only|must) (be )?play'),
    ('protection', 'does', r"can't be (destroyed|moved|discarded|reduced|afflicted)"), ('protection', 'does', r"\b(power|cards) can't be (reduced|lowered)"),
    ('silence', 'does', r"(lose|loses|remove|removes|without) (their|its|all|the)? ?(text|abilit)"), ('silence', 'does', r"(abilities|effects) (don't|won't|do not|can't) "),
    ('disable', 'does', r"can't (move|be moved|attack)"),
    ('steal', 'does', r'\bsteal'), ('steal', 'does', r'switch sides'), ('steal', 'does', r"(take control|move [^.]{0,20}to your side)"),
    ('donate', 'does', r"(give|move)[^.]{0,40}(to your opponent|opponent's side|their side)"),
    ('scope_global', 'does', r'\b(all|every|each) (cards?|characters?|locations?)\b'), ('scope_global', 'does', r'\bboth (players|sides)'),
    ('condition', 'does', r'(^|[.:~] *)if '), ('condition', 'does', r'\bunless\b'), ('condition', 'does', r'\botherwise\b'),
    ('condition_count', 'does', r'\bfor each\b'), ('condition_count', 'does', r'\bfor every\b'),
    ('zone_control', 'does', r"(you're|you are|if you're) winning"), ('zone_control', 'does', r"(win|winning|lose|losing) (here|this location|there)"),
    ('comeback', 'does', r"(you're|you are|if you're) losing"),
    ('terrain', 'does', r'(change|transform|replace)[^.]{0,30}(location|locations)'), ('rule_change', 'does', r'(change|transform|replace)[^.]{0,30}(location|locations)'),
    ('random_effect', 'does', r'\brandom'), ('hand_size', 'does', r'(for each|number of)[^.]{0,20}cards? in (your|their) hand'), ('hand_size', 'does', r'hand is (empty|full)'),
    ('hand_size', 'does', r'\d+ or (more|fewer|less) cards in (your|their) hand'),
    ('hand_position', 'does', r'\b(leftmost|rightmost|left-?most|right-?most)\b'),
    ('deck_condition', 'does', r'(in|of) your deck'), ('deck_position', 'does', r'(top|bottom) (card )?of (your|their) deck'),
    ('revive', 'does', r'\bresurrect'), ('revive', 'does', r'\brevive'), ('revive', 'does', r'return[^.]{0,30}destroyed[^.]{0,30}(to|here|play)'),
    ('banish', 'does', r'\bbanish'), ('swap', 'does', r'\bswap'), ('swap', 'does', r'switch (places|positions|locations)'),
    ('stat_swap', 'does', r'swap[^.]{0,30}(power|cost)[^.]{0,20}(power|cost)'),
    ('on_ally_play', 'does', r'(after|when|whenever|each time) you play'),
    ('reactions', 'does', r"(after|when|whenever) (your )?opponent plays"), ('reactions', 'does', r"(after|when|whenever) an? (enemy|opposing) card"),
    ('on_enemy_enter', 'does', r"(enemy|opposing|opponent's) cards? (is |are )?(played|arrives?|moves?) (here|to this)"),
    ('delayed', 'does', r'\bnext turn\b'), ('delayed', 'does', r'\bin \d turns?'),
    ('information', 'does', r"(see|look at|reveal)[^.]{0,30}(opponent.s|their|enemy) (hand|deck|card)"), ('information', 'does', r'\bface-?down\b'),
    ('turn_structure', 'does', r'\bturn [1-9]\b'), ('turn_structure', 'does', r'\b(last|final) turn'), ('extra_turn', 'does', r'(extra|additional) turn|\bturn 7\b|game lasts'),
    ('aura', 'does', r'ongoing\s*~?[^.]{0,80}(your|other|all|cards)[^.]{0,40}(\+|-)\d+ power'),
    ('adjacency', 'does', r'(location|locations) to the (left|right)'), ('adjacency', 'does', r'\badjacent\b'),
    ('board_limit', 'does', r'\b(full|empty) (location|locations|here)'), ('board_limit', 'does', r'(location|this) is (full|empty)'), ('board_limit', 'does', r'\bfront row\b'),
    ('repeat_trigger', 'does', r'\brepeats?\b'), ('repeat_trigger', 'does', r'\btrigger (twice|again)'), ('repeat_trigger', 'does', r'happens? twice'),
    ('lanes', 'does', r'\b(this|other|each|every|a|that|another|its) locations?\b'), ('lanes', 'does', r'\bhere\b'), ('lanes', 'does', r'\blocations?\b'),
    ('modal_choice', 'does', r'\bchoose\b'), ('selection', 'does', r'\bchoose (one|a|1|from)'),
]
for con, role, p in SNAP_PATTERNS: c.execute("insert into concept_patterns values(?,?,?,?)", (con, role, p, G))
SKIP = {'stress_morale'}   # its general patterns catch 'afflict', a different mechanic in Darkest Dungeon
# general patterns that misread Marvel Snap wording (energy gains, 'reveal' as a turn step, merges, created cards)
EXCL = {('buff', r'gets? \+\d+'), ('deck_modification', r'\bmerge'), ('upgrade', r'\bempowered\b'), ('information', r'\breveal'),
        ('return_to_hand', r"to (your )?opponent'?s hand"), ('hand_size', r'cards in (your|their) hand')}
pats = [(con, role, re.compile(p, re.I)) for con, role, p, g in q("select concept,role,pattern,game from concept_patterns where game is null or game=?", G)
        if con not in SKIP and (con, p) not in EXCL]
MASK = re.compile(r'\b(on reveal|ongoing|activate|end of turn|start of turn|game start|objective|quickdraw|when (discarded|destroyed)( or (discarded|destroyed))?)\b', re.I)
root = dict(q("select id,root from concept_tree where root in ('trigger','effect')"))
snip = lambda t, m: t[max(0, m.start() - 20): m.start() + 40]
SPLIT = re.compile(r'(?<=[.!)])\s+|\s{2,}|(?=\b(?:On Reveal|Ongoing|Activate|End of Turn|Start of Turn|Game Start|When Destroyed|When Discarded|Quickdraw):)')

def tag_text(e, t):
    """Concepts from text patterns and keywords, links to keywords, trigger -> effect pairs clause by clause."""
    low = t.lower(); mlow = MASK.sub('~', low)
    for con, role, p in pats:
        m = p.search(mlow)
        if m: tag(e, con, role, 'text_pattern', snip(mlow, m))
    for k, rx in LABEL.items():
        m = rx.search(t)
        if m:
            link(e, 'has_keyword', kwid[k], snip(low, m))
            for con, role in KW[k][1]: tag(e, con, role, 'via_keyword')
        elif re.search(KW[k][2], low):
            link(e, 'mentions_keyword', kwid[k], low[:50])
    for k, rx in VERB.items():
        m = re.search(rx, low)
        if m:
            link(e, 'has_keyword', kwid[k], snip(low, m))
            for con, role in KW[k][1]: tag(e, con, role, 'via_keyword')
    for cl in SPLIT.split(t):
        if not cl or not cl.strip(): continue
        lc = MASK.sub('~', cl.lower())
        trig = {con for con, role, p in pats if role == 'does' and root.get(con) == 'trigger' and p.search(lc)}
        for k, rx in LABEL.items():
            if rx.search(cl): trig |= {con for con, _ in KW[k][1] if root.get(con) == 'trigger'}
        eff = {con for con, role, p in pats if role == 'does' and root.get(con) == 'effect' and p.search(lc)}
        for k, rx in VERB.items():
            if re.search(rx, lc): eff |= {con for con, _ in KW[k][1] if root.get(con) == 'effect'}
        for a in trig:
            for b in eff: c.execute("insert into trigger_effect values(?,?,?,?,?)", (e, G, a, b, cl.strip()))

# ---------- cards: every record in the source ----------
cards = json.load(open(SRC, encoding='utf-8'))
strip = lambda t: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t or '')).replace(' :', ':').strip()
alltext = ' '.join(strip(x.get('ability')) for x in cards)
def kind(x):
    src = x.get('source') or 'None'
    if x.get('status') == 'released' and src != 'None': return 'collectible', src
    if x.get('status') == 'released': return 'mode variant', None
    if re.search(r'\b' + re.escape(x['name']) + r's?\b', alltext): return 'created card (token)', None
    return 'unreleased or not collectible', None
ids, counts = {}, {}
for x in cards:
    k, series = kind(x)
    counts[k] = counts.get(k, 0) + 1
    t = strip(x.get('ability'))
    extra = {k2: v for k2, v in x.items() if k2 not in ('name', 'ability', 'cost', 'power', 'carddefid') and v not in (None, '', 'None')}
    e = add_entity(ext_id=x.get('carddefid'), name=x['name'], category='unit', source_type=f"Character ({k})",
                   subtypes=series, cost=f"{x.get('cost')} energy", cost_num=float(x['cost']) if x.get('cost') is not None else None,
                   stats=json.dumps({'power': x.get('power')}), text=t or None, extra=json.dumps(extra, ensure_ascii=False))
    ids[e] = (x, t, k)
for k, n in counts.items(): log(f'loaded unit: {k}', n)
names = {}
for e, (x, t, k) in ids.items():
    if x['name'] not in names or k == 'collectible': names[x['name']] = e

for e, (x, t, k) in ids.items():
    tag(e, 'lanes', 'benefits', 'game_structure', 'played at one of three locations')
    tag(e, 'points_scoring', 'benefits', 'game_structure', "a card's power is its points")
    if not t: continue
    tag_text(e, t)
    taken = []   # name spans already matched (a longer name wins over a name inside it: DoomBot 2099 over DoomBot)
    for other in sorted(names, key=len, reverse=True):
        o = names[other]
        if o == e or len(other) < 3 or other == x['name']: continue
        m = next((m for m in re.finditer(r'\b' + re.escape(other) + r's?\b', t) if not any(a <= m.start() < b for a, b in taken)), None)
        if not m: continue
        taken.append((m.start(), m.end()))
        pre, post = t[max(0, m.start() - 70): m.start()].lower(), t[m.end(): m.end() + 40].lower()
        made = re.search(r'\b(add|adds|create|creates|shuffle|put|puts|summon|summons|spawn|fill|fills|give you|get)\b[^.]*$', pre)
        rel = ('transforms_into' if re.search(r'(transforms?|becomes?|turns? (it|them|this|itself)?\s*into|replace[sd]? (it|this|them)? ?with)[^.]*$', pre) else
               'generates' if made and re.search(r'\b(hand|deck)\b', post + pre[-30:]) else
               'summons' if made else 'references')
        link(e, rel, o, t[max(0, m.start() - 25): m.end() + 15])

# variants: mode cards ("Hulk Champion", "Thor - Avengers") and alternative versions point at their base card
coll = sorted((n for n, o in names.items() if ids[o][2] == 'collectible' and len(n) > 3), key=len, reverse=True)
nvar = 0
for e, (x, t, k) in ids.items():
    nm = x['name']
    for b in coll:
        if nm != b and (nm.startswith(b + ' ') or (k != 'collectible' and nm.replace(' ', '').lower().startswith(b.replace(' ', '').lower()))):
            link(e, 'variant_of', names[b], f'{nm} is a version of {b}'); nvar += 1; break
log('variant_of links (mode and alternative versions to their base card)', nvar)

# ---------- teams and families (the game's tribes): cards of a team, and cards that care about one ----------
TRIBES = {  # name: (how a card belongs: name suffix / prefix regex, how a card cares: text regex)
    'Avengers': (r' - Avengers$|Avengers$', r'\bavengers?\b'), 'Spider-Verse': (r' - Spider-Verse$', r'\bspider-verse\b'),
    'X-Men': (r' - X-Men$', r'\bx-men\b'), 'Guardians of the Galaxy': (r' - Guardians of the Galaxy$', r'\bguardians?\b'),
    'Thunderbolts': (r' - Thunderbolts$', r'\bthunderbolts?\b'), 'Brotherhood of Mutants': (r' - Brotherhood of Mutants$', r'\bbrotherhood\b'),
    'Zombies': (r'^Zombie ', r'\b(zombie|horde)\b'), 'Vampires': (r'^Vampire ', r'\bvampir'),
    'Horsemen of Apocalypse': (r' Horseman of ', r'\bhorsem[ae]n\b'), 'Infinity Stones': (r' Stone$', r'\b(infinity )?stones?\b'),
    'Champions': (r' Champion$', r'\bchampion\b'), 'Fractured Frontier': (r' Fractured Frontier$', r'\bfractured frontier\b'),
}
nt = 0
for tname, (member, cares) in TRIBES.items():
    te = add_entity(ext_id='tribe:' + tname, name=tname, category='tribe', source_type='card type / tribe', text=f'Marvel Snap cards of the {tname} group, and cards that care about them.')
    tag(te, 'tribal', 'does', 'game_structure', 'a card group other cards refer to')
    for e, (x, t, k) in ids.items():
        if re.search(member, x['name']): link(e, 'has_type', te, x['name']); nt += 1
        if t and re.search(cares, t, re.I):
            link(e, 'cares_about_type', te, t[:60]); tag(e, 'tribal', 'does', 'text_pattern', t[:50])
log('tribes (teams, families and modes named on the cards)', len(TRIBES))

# ---------- locations (when supplied) ----------
if LOC:
    data = json.load(open(LOC, encoding='utf-8'))
    locs = data if isinstance(data, list) else (data.get('success') or {}).get('locations') or (data.get('success') or {}).get('cards') or data.get('locations') or data.get('cards') or list(data.values())
    n = 0
    for x in locs:
        nm = x.get('name'); t = strip(x.get('ability') or x.get('description') or x.get('text'))
        if not nm: continue
        extra = {k2: v for k2, v in x.items() if k2 not in ('name', 'ability', 'description', 'text') and v not in (None, '', 'None')}
        e = add_entity(ext_id='loc:' + nm, name=nm, category='terrain', source_type='Location',
                       subtypes=x.get('tier'), rarity=x.get('rarity'), text=t or None, extra=json.dumps(extra, ensure_ascii=False))
        ids[e] = (x, t, 'location'); n += 1
        tag(e, 'lanes', 'does', 'game_structure', 'a location is a lane with its own rule')
        tag(e, 'terrain', 'does', 'game_structure', 'a location is a lane with its own rule')
        tag(e, 'lane_rule', 'does', 'game_structure', 'a location is a lane with its own rule')
        tag(e, 'symmetric_effect', 'does', 'game_structure', "a location's rule applies to both players")
        if t:
            tag(e, 'rule_change', 'does', 'game_structure', 'its text changes the rules of its lane')
            tag_text(e, t)
            for other, o in names.items():
                if len(other) > 2 and re.search(r'\b' + re.escape(other) + r's?\b', t): link(e, 'references', o, t[:60])
    log('loaded terrain (locations)', n)
else:
    log('locations not loaded: no source file yet', 0)

# ---------- Claude's review of every card (adds concepts, removes wrong automatic tags) ----------
if REVIEW and os.path.exists(REVIEW):
    rv = json.load(open(REVIEW, encoding='utf-8'))
    byname, bytext = {}, {}
    for e, (x, t, k) in ids.items():
        byname.setdefault(x['name'], []).append(e)
        if t: bytext.setdefault(t, []).append(e)
    nrev = 0
    for nm, r in rv.items():
        # the reviewed card, and every other card with the very same text (its mode variants)
        targets = set(byname.get(nm, [])) | {o for e in byname.get(nm, []) for o in bytext.get(ids[e][1], [])}
        for e in targets:
            for item in r.get('drop', []):
                con, role = (item.split(':') + [None])[:2]
                if role:
                    c.execute("delete from entity_concepts where entity=? and concept=? and role=? and method in ('text_pattern','via_keyword')", (e, con, role))
                else:
                    c.execute("delete from entity_concepts where entity=? and concept=? and method in ('text_pattern','via_keyword')", (e, con))
                    c.execute("delete from trigger_effect where entity=? and (trigger=? or effect=?)", (e, con, con))
            for item in r.get('add', []):
                con, role = (item.split(':') + ['does'])[:2]
                tag(e, con, role, 'claude_review', 'hand-mapped from the card text')
            nrev += 1
    log('cards reviewed by Claude (concepts added or corrected)', nrev)

# a specific turn number already says it is about turn structure
c.execute("""delete from entity_concepts where concept='turn_structure' and method='text_pattern' and entity in (select id from entities where game=?)
             and entity in (select entity from entity_concepts where concept='turn_number')""", (G,))

# ---------- game rules ----------
RULES = [
    ('Locations', 'Three lanes called locations. One is revealed on each of turns 1, 2 and 3; each carries its own rule that changes play there (most are random each game).', ['lanes', 'rule_change', 'terrain', 'randomness']),
    ('Winning a location', 'Whoever has more total power at a location at the end of the game wins it; winning 2 of the 3 locations wins the game; a tie is broken by total power across all locations.', ['points_scoring', 'zone_control']),
    ('Simultaneous turns and reveal order', 'Both players play cards face down at the same time; then cards are revealed, all of the player who is winning more locations first (a coin flip on ties), in the order played.', ['turn_structure', 'information', 'simultaneous_play', 'reveal_order']),
    ('Energy and game length', 'Energy each turn equals the turn number and does not carry over; the game lasts 6 turns.', ['turn_structure', 'resource_gain']),
    ('Location capacity', 'Each player can have at most 4 cards at a location.', ['board_limit', 'lanes']),
    ('Snap and retreat', 'A player can Snap to double the ranked stakes of the game, and either player can retreat before the end to lose only the current stakes.', ['information', 'stakes_wager']),
]
for n, t, cs in RULES:
    e = add_entity(ext_id='rule:' + n, name=n, category='game_rule', source_type='game rule (Claude summary)', text=t)
    for con in cs: tag(e, con, 'does', 'claude_review')
log('loaded game_rule (Claude summaries of the core rules)', len(RULES))
log('no factions: the game has none (cards come in series), so no faction or archetype profiles', 0)
c.commit()
print('entities', q("select count(*) from entities where game=?", G)[0][0], counts)
