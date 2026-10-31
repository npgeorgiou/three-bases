"""Real-world cases: what players and guides say about each game (library/games/<game>.md, ```tsv blocks; how they are made:
library/realworld/RESEARCH.md), checked against the answers of the card database. Every miss is read: the data, the
question or the case is wrong.
  signature <faction> <concept>    the faction is among the game's 3 factions with the highest share of cards with it
  splash    <faction> <concept>    the faction has at least one card with it
  archetype <faction> <archetype>  the same as signature, for the archetype's concepts (ARCHETYPE below, Claude's mapping
                                   of library/realworld/archetypes.txt to concepts)
  combo     <card A> <card B>      a line between the two cards in a network of the two, or a way one sets off the other
               (library/realworld/combos_known.tsv: the same for combos from other sources)
Usage: realworld.py [game ...]   prints the misses per game and the counts."""
import collections, csv, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.argv, ARGS = sys.argv[:1] + ['all', 'list', 'concepts'], sys.argv[1:]
import ask, connections, network, source
LIB = source.lib()
c = ask.c
ARCHETYPE = {'swarm': ('summon', 'generate_cards', 'board_presence'), 'sacrifice': ('sacrifice', 'death_trigger', 'other_death_trigger'),
             'graveyard': ('revive', 'recycle', 'graveyard'), 'control': ('removal', 'suppress'), 'burn': ('direct_damage', 'aoe_damage'),
             'aggro_tempo': ('haste', 'attack_gain', 'evasion', 'tempo'), 'scaling': ('permanent_growth', 'snowball'),
             'fortress': ('protection', 'taunt', 'tank'), 'sustain': ('heal',), 'spellslinger': ('spell_power', 'spells_played_condition', 'on_spell'),
             'ramp': ('resource_gain', 'cost_reduction'), 'positional': ('movement', 'forced_movement', 'positional'),
             'disruption': ('disruption', 'debuff'), 'trickery': ('stealth', 'trap_secret', 'information'), 'chaos': ('random_effect',),
             'card_advantage': ('card_advantage',), 'tribal': ('tribal',), 'objectives': ('zone_control', 'scoring_objectives'),
             'poison_attrition': ('damage_over_time',), 'transformation': ('transform', 'stances', 'merge_attach')}
NOT_FACTION = ('boss', 'neutral', 'colorless', 'curse', 'status', 'token', 'event', 'shared', 'universal', '(none)', 'runeterra')  # Runeterra's own region is neutral (Kaptain)


def cases(game):
    t = open(os.path.join(HERE, '..', 'games', game + '.md'), encoding='utf-8').read()
    return [l.split('\t') for b in re.findall(r'```tsv\n(.*?)```', t, re.S) for l in b.splitlines() if l.strip() and not l.startswith('#')]


def shares(game, concepts):
    """faction -> share of its cards with any of the concepts (or one under them)"""
    got = {i for x in concepts if not x.startswith('kw:') for (i,) in c.execute('select card from flat_concept where under(concept, ?)', (x,))}
    for x in concepts:  # kw:<Keyword>: the card has the keyword or gives it
        if x.startswith('kw:'):
            got |= {i for (i,) in c.execute("select ck.card from card_keyword ck join card k on k.id=ck.keyword where k.game=? and k.name=? "
                                             "union select d.card from flat_do d join card k on k.id=d.keyword_ref where k.game=? and k.name=?", (game, x[3:], game, x[3:]))}
    got |= {a for a, b in c.execute('select card, made from flat_made') if b in got}  # a card is what it makes
    per = collections.defaultdict(lambda: [0, 0])
    for i, regs in c.execute("""select id, regions from card where game=? and is_keyword=0 and is_stub=0 and coalesce(category,'')
                                not in ('game_rule','boss','monster','event','modifier')
                                and not (category='ability' and id in (select made from flat_made))""", (game,)):  # a skill a card makes is no card of its own (an Into the Breach weapon is)
        for r in (regs or '').split(';'):
            if r: per[r][1] += 1; per[r][0] += i in got
    return {r: n / t for r, (n, t) in per.items() if t}


def ranked(game, concepts):
    s = shares(game, concepts)
    return [r for r, _ in sorted(s.items(), key=lambda x: -x[1]) if r.lower().split(' (')[0] not in NOT_FACTION], s


def carried(game, i):
    """what a unit carries from the start, named in its text (Into the Breach: "Weapon: Titan Fist: ...", "Passive: Storm Generator: ...")"""
    if game not in network.CARRIED: return set()
    t = (LIB.execute('select text from entities where id=?', (i,)).fetchone() or [''])[0] or ''
    names = re.findall(r'(?:Weapon|Passive): ([^:.]+):', t)
    return {j for n in names for (j,) in c.execute('select id from card where game=? and name=?', (game, n.strip()))}


WEARS = {'inscryption'}  # games where any sigil can be put on any card or tribe (Mysterious Stones, totems; library/games/inscryption.md)
PUTS_SELF = ('copy', 'return_card', 'play_card', 'summon', 'revive')


def worn(game, s, w):
    """sigil s on card or tribe w (a combo named as a card plus a sigil): s acts on its wearer (Fecundity copies it, Unkillable
    brings it back, Corpse Eater plays it), one of them makes on itself what the other waits for on itself (Corpse Eater plays
    it: Fecundity), s's value comes free on a card that costs nothing (Squirrel), or s on a tribe makes more of the tribe (Bees)"""
    if (s, w) in c.execute('select keyword, card from card_keyword where keyword=? and card=?', (s, w)).fetchall(): return False
    if c.execute(f"""select 1 from flat_do where card=? and origin='own' and on_pick='self' and card_ref is null and act in
                 ({','.join('?' * len(PUTS_SELF))})""", (s,) + PUTS_SELF).fetchone(): return True
    members = [w] if c.execute('select is_keyword from card where id=?', (w,)).fetchone()[0] or \
        c.execute("select category from card where id=?", (w,)).fetchone()[0] != 'tribe' else \
        [m for (m,) in c.execute('select ct.card from card_type ct join type t on t.id=ct.type where t.tribe_entry=?', (w,))]
    if len(members) > 1 and c.execute(f"""select 1 from flat_do d join card_type ct on ct.card=d.card_ref join type t on t.id=ct.type
            where d.card=? and d.origin='own' and d.act in ('create','summon') and t.tribe_entry=?""", (s, w)).fetchone(): return True
    rows = lambda x, role: {h for (h,) in c.execute("""select happening from flat_ref where card=? and role=? and origin in ('own','has_keyword')
                            and coalesce(pick,'') in ('self','actor_self')""", (x, role))}
    sm, sw = rows(s, 'makes'), rows(s, 'trigger') | rows(s, 'condition')
    by_me = {h for (h,) in c.execute("select happening from flat_ref where card=? and role='trigger' and pick='actor_self'", (s,))}  # "when this damages"
    for m in members:
        own = {h for (h,) in c.execute("select happening from flat_ref where card=? and role='makes' and origin in ('own','has_keyword')", (m,))}
        if sm & (rows(m, 'trigger') | rows(m, 'condition')) or rows(m, 'makes') & sw or by_me & own: return True
        if not (c.execute('select cost from card where id=?', (m,)).fetchone()[0] or 0) and sw & {'played', 'sacrificed', 'summoned'}: return True
    return False


def combo(game, a, b):
    ids = {n: i for i, n in c.execute('select id, name from card where game=? order by is_keyword desc', (game,))}  # a sigil or keyword named in a combo too
    if a not in ids or b not in ids: return None
    ia, ib = ids[a], ids[b]
    fa, fb = ({i} | network.made(c, game, [i]) | carried(game, i) for i in (ia, ib))  # a card with what it makes and carries
    lines = network.network(c, game, list(dict.fromkeys([ia, ib] + sorted((fa | fb) - {ia, ib}))))[1]
    if any(x != y and ((x in fa and y in fb) or (x in fb and y in fa)) for x, y in lines): return True
    if game in WEARS:
        kw = {i for i in (ia, ib) if c.execute('select is_keyword from card where id=?', (i,)).fetchone()[0]}
        for s in kw:
            if worn(game, s, ib if s == ia else ia): return True
    return bool(list(connections.reasons(c, a, b)) or list(connections.reasons(c, b, a)))


def run(game):
    ok, miss = 0, []
    for row in cases(game):
        kind, a, b = row[0], row[1], row[2]
        if kind in ('signature', 'archetype', 'splash'):
            cons = ARCHETYPE.get(b, ()) if kind == 'archetype' else (b,)
            if not cons: miss.append((kind, a, b, 'no concepts for this archetype')); continue
            order, s = ranked(game, cons)
            hit = (s.get(a, 0) > 0) if kind == 'splash' else a in order[:3]
            why = f"{a}: {s.get(a, 0):.0%}, rank {order.index(a) + 1 if a in order else '-'} of {len(order)}; top: {', '.join(order[:3])}"
        elif kind == 'combo':
            r = combo(game, a, b); hit = bool(r); why = 'card not in the database' if r is None else 'no line'
        else: continue
        if hit: ok += 1
        else: miss.append((kind, a, b, why))
    return ok, miss


if __name__ == '__main__':
    games = ARGS or ['runeterra', 'stormbound', 'monster_train', 'duelyst', 'faeria', 'inscryption', 'into_the_breach', 'sts1']
    for g in games:
        ok, miss = run(g)
        print(f'## {g}: {ok} of {ok + len(miss)} cases hold')
        for m in miss: print('  MISS ' + ' | '.join(m))
