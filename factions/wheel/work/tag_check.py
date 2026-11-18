"""tag_check.py (run from library/cards_db): step 1, the tag check. For every usable concept (concepts.tsv), its real cards
grouped by what put the tag on them: the row (table, action or test or event, whose side, when it fires, from where, and
whether the card's own text or a keyword gave it), the keyword, or the general rule and the row that set it off.
A group is suspect when it acts on the wrong side (it helps the enemy, or hurts me) or when its rows match what the
concept's definition gives to another concept (CHECKS below). Writes tag_groups.tsv (every group) and tag_reads.tsv
(5 cards per suspect family: one concept, one action or test, one reason; spread over the games; verdict and
why left empty, for the reader) only with --reads; always tag_cards.tsv (every card of every suspect family)."""
import collections, os, random, re, sqlite3, sys
sys.path.insert(0, os.getcwd())
import flat

HERE = os.path.dirname(os.path.abspath(__file__))
c = sqlite3.connect('cards.sqlite')
usable = [r.split('\t')[0] for r in open(os.path.join(HERE, 'concepts.tsv')).read().splitlines()[1:] if r.split('\t')[3] == 'usable']
tree = {}
for l in open('../concept_tree.txt'):
    if l.startswith('#') or '|' not in l: continue
    p = [x.strip() for x in l.split('|')]
    tree[p[0]] = (p[3].split(',') if p[3] else [], p[4], p[5] if len(p) > 5 else '')


def ancestors(k, seen=None):
    seen = seen if seen is not None else set()
    for p in tree.get(k, ([],))[0]:
        if p and p not in seen: seen.add(p); ancestors(p, seen)
    return seen


real = {i: (g, n) for i, g, n in c.execute('select id, game, name from card where coalesce(is_keyword,0)=0 and coalesce(is_stub,0)=0')}
trig = collections.defaultdict(list)  # (card, ability) -> when it fires
for card, ab, e, ok, os_, op in c.execute('select card, ability, event, obj_kind, obj_side, obj_pick from flat_when'):
    trig[(card, ab)].append(f"{e}{'(self)' if op == 'self' else ''}")
COLS = {'flat_do': "rowid, card, ability, origin, via, 'do ' || act, on_kind, on_side, on_pick, coalesce(on_zone, eff_zone), to_side, params, concept",
        'flat_when': "rowid, card, ability, origin, via, 'when ' || event, obj_kind, obj_side, obj_pick, null, actor_side, lim, concept",
        'flat_if': "rowid, card, ability, origin, via, 'if ' || test || coalesce(' ' || event, ''), of_kind, of_side, of_pick, of_zone, ev_obj_side, span, concept"}
kwname = {i: n for i, n in c.execute('select id, name from card where is_keyword=1')}


def row_key(t, r):
    _, card, ab, origin, via, what, kind, side, pick, zone, other, extra, _k = r
    w = trig.get((card, ab), [])
    src = origin if origin == 'own' else f"{origin} {kwname.get(via, via)}" if origin in ('has_keyword', 'uses_keyword') else origin
    to = (f' to {other}' if t == 'flat_do' else f' by {other}' if t == 'flat_when' else f' event on {other}') if other else ''
    return (what, f"{kind or '-'}/{side or '-'}/{pick or '-'}{to}", zone or '-', ','.join(sorted(set(w))) or '-', src)


rows = collections.defaultdict(list)  # (concept, key) -> [(card, row)]
for t in COLS:
    for r in c.execute(f"select {COLS[t]} from {t} where concept in ({','.join('?' * len(usable))})", usable):
        if r[1] in real: rows[(r[12], ('row',) + row_key(t, r))].append((r[1], (t, r)))
for k, t, cond in flat.RULES:
    if k not in usable: continue
    for r in c.execute(f"select {COLS[t]} from {t} where {cond}"):
        if r[1] in real: rows[(k, ('rule ' + k,) + row_key(t, r))].append((r[1], (t, r)))
for card, k, kw in c.execute("select distinct ck.card, v.tree, k.name from card_keyword ck join card k on k.id=ck.keyword join vocab v on "
                             "v.field='keyword' and v.value=coalesce((select s.value from vocab s where s.field='keyword' and s.value=k.game || ':' || k.name), k.name) "
                             f"where v.tree in ({','.join('?' * len(usable))})", usable):
    if card in real: rows[(k, ('keyword', kw, '-', '-', '-', 'has_keyword'))].append((card, None))
for card, k, kw in c.execute("select distinct a.card, v.tree, k.name from cond cd join ability a on a.id=cd.ability join card k on k.id=cd.ref_keyword "
                             "join vocab v on v.field='keyword' and v.value=coalesce((select s.value from vocab s where s.field='keyword' and s.value=k.game || ':' || k.name), k.name) "
                             f"where cd.test='keyword_condition' and v.tree in ({','.join('?' * len(usable))})", usable):
    if card in real: rows[(k, ('keyword condition', kw, '-', '-', '-', 'own'))].append((card, None))

# what the tag of each concept is (only concepts the tree places on one side are checked for side)
HELPS = {k for k in tree if 'helps_me' in ancestors(k) or k == 'helps_me'}
HURTS = {k for k in tree if 'hurts_enemy' in ancestors(k) or k == 'hurts_enemy'}
MY_TRIGGERS = {'on_ally_play', 'on_sacrifice', 'on_life_loss', 'on_draw', 'on_discard'}  # "when I ..." / "the owner ..."
ONCE = {'played', 'summoned', 'played(self)', 'summoned(self)', 'enters', 'enters(self)', 'start_of_game', 'start_of_game(self)'}


GOOD = {'summon', 'create', 'draw', 'mana_gain', 'max_mana_change', 'heal', 'give_keyword', 'give_ability', 'play_card', 'revive', 'ready',
        'repeat', 'increase_effect', 'swap', 'cost_set', 'can', 'put_on_top', 'shuffle_into_deck', 'copy_keywords'}  # good for whom they act on
BAD = {'damage', 'kill', 'excess_damage', 'mark', 'obliterate'}  # bad for whom they act on
TO = {'summon', 'create', 'copy', 'move'}  # where the thing is put says whose it is


def lowers(r): return bool(re.search(r'=-|=minus', r[1][11] or ''))


def checks(k, key, items):
    """why a group is suspect (empty when it is not): one line per reason"""
    why = []
    src, what, who, zone, when = key[0], key[1], key[2], key[3], key[4]
    side = who.split('/')[1] if '/' in who else '-'
    other = who.split(' ')[-1] if ' ' in who else '-'
    act = what.split(' ', 1)[1] if ' ' in what else what
    rs = [r for _, r in items if r]
    if rs and rs[0][0] == 'flat_do':
        if k in HELPS and side == 'enemy' and (act in GOOD or (act == 'stat_change' and not all(lowers(r) for r in rs))): why.append('helps the enemy: acts on an enemy')
        if k in HELPS and act in TO and other == 'enemy': why.append('helps the enemy: puts it on the enemy side')
        if k in HURTS and side == 'mine' and act in BAD: why.append('hurts me: acts on my own side')
        if k in ('stat_gain', 'attack_gain', 'defence_gain', 'buff') and act == 'stat_change' and all(lowers(r) for r in rs): why.append('lowers a stat: that is stat_loss')
        if k == 'cost_reduction' and any(re.search(r'cost=[0-9]', r[1][11] or '') for r in rs): why.append('raises a cost')
        if k == 'permanent_growth' and when != '-' and set(when.split(',')) <= ONCE: why.append('grows once, when played: a single lasting bonus is stat_gain')
        if k == 'shield' and act in ('counter', 'remove_keyword', 'silence'): why.append(f'{act}: cancelling a spell or removing a keyword is not absorbing a hit')
        if k == 'immunity' and act == 'cant': why.append('a "can\'t" row: check it guards my unit')
        if k == 'return_to_hand': why.append('return to hand: its rows say neither whose unit nor from where (the rows that say go to return_from_board, return_on_leave)')
    if rs and rs[0][0] == 'flat_when':
        if k in MY_TRIGGERS and 'enemy' in (other, side): why.append('fires on the enemy\'s action')
    if rs and rs[0][0] == 'flat_if':
        if k == 'count_payoff' and what.startswith('if amount_count'): why.append('counts what is on the board now: that is condition_count')
    return why


out = []
fam = collections.defaultdict(list)  # (concept, action or test, why) -> its suspect groups' cards: the unit that is read
for (k, key), items in sorted(rows.items(), key=lambda x: (x[0][0], -len({i for i, _ in x[1]}))):
    cards = sorted({i for i, _ in items})
    why = checks(k, key, items)
    games = collections.Counter(real[i][0] for i in cards)
    out.append([k, *key, str(len(cards)), ','.join(f'{g}:{n}' for g, n in sorted(games.items())), 'suspect' if why else '', '; '.join(why),
                ', '.join(real[i][1] for i in cards[:6])])
    if why: fam[(k, key[1], '; '.join(why))] += [(i, ' | '.join(key)) for i in cards]
rnd = random.Random(0)
reads = []
for (k, what, why), cs in sorted(fam.items()):
    seen = {}
    for i, g in cs: seen.setdefault(i, g)
    by_game = collections.defaultdict(list)  # spread the 5 over the games
    for i in sorted(seen): by_game[real[i][0]].append(i)
    pick = []
    while len(pick) < min(5, len(seen)):
        for g in sorted(by_game):
            if by_game[g] and len(pick) < 5: pick.append(by_game[g].pop(rnd.randrange(len(by_game[g]))))
    for i in pick: reads.append([k, what, why, seen[i], real[i][0], real[i][1], str(i), '', ''])
with open(os.path.join(HERE, 'tag_cards.tsv'), 'w') as f:  # every card of every suspect family, with its group
    f.write('concept\tfamily\twhy suspect\tgroup\tgame\tcard\tcard id\n')
    for (k, what, why), cs in sorted(fam.items()):
        seen = {}
        for i, g in cs: seen.setdefault(i, g)
        for i in sorted(seen): f.write('\t'.join([k, what, why, seen[i], real[i][0], real[i][1], str(i)]) + '\n')
if '--reads' not in sys.argv: sys.exit(print(f'{len(out)} groups, {sum(1 for r in out if r[9])} suspect in {len(fam)} families (tag_cards.tsv; --reads writes tag_groups.tsv and tag_reads.tsv)'))
with open(os.path.join(HERE, 'tag_groups.tsv'), 'w') as f:
    f.write('concept\tsource\twhat\ton (kind/side/pick, to or by whose side)\tzone\twhen\tgiven by\tcards\tgames\tsuspect\twhy\texamples\n')
    for r in out: f.write('\t'.join(r) + '\n')
with open(os.path.join(HERE, 'tag_reads.tsv'), 'w') as f:
    f.write('concept\tfamily\twhy suspect\tgroup\tgame\tcard\tcard id\tverdict\treader why\n')
    for r in reads: f.write('\t'.join(r) + '\n')
sus = [r for r in out if r[9]]
print(f'{len(out)} groups, {len(sus)} suspect in {len(fam)} families, {len(reads)} cards to read; suspect cards per family:')
for (k, what, why), cs in sorted(fam.items(), key=lambda x: -len({i for i, _ in x[1]})): print(f'  {len({i for i, _ in cs})}\t{k}\t{what}\t{why}')
