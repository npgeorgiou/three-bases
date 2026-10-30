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
import ask, connections, network
c = ask.c
ARCHETYPE = {'swarm': ('summon', 'generate_cards', 'board_presence'), 'sacrifice': ('sacrifice', 'death_trigger', 'other_death_trigger'),
             'graveyard': ('revive', 'recycle', 'graveyard'), 'control': ('removal', 'suppress'), 'burn': ('direct_damage', 'aoe_damage'),
             'aggro_tempo': ('haste', 'attack_gain', 'evasion', 'tempo'), 'scaling': ('permanent_growth', 'snowball'),
             'fortress': ('protection', 'taunt'), 'sustain': ('heal',), 'spellslinger': ('spell_power', 'spells_played_condition', 'on_spell'),
             'ramp': ('resource_gain', 'cost_reduction'), 'positional': ('movement', 'forced_movement', 'positional'),
             'disruption': ('disruption', 'debuff'), 'trickery': ('stealth', 'trap_secret', 'information'), 'chaos': ('random_effect',),
             'card_advantage': ('card_advantage',), 'tribal': ('tribal',), 'objectives': ('zone_control', 'scoring_objectives'),
             'poison_attrition': ('damage_over_time',), 'transformation': ('transform', 'stances', 'merge_attach')}
NOT_FACTION = ('boss', 'neutral', 'colorless', 'curse', 'status', 'token', 'event', 'shared', 'universal', '(none)')


def cases(game):
    t = open(os.path.join(HERE, '..', 'games', game + '.md'), encoding='utf-8').read()
    return [l.split('\t') for b in re.findall(r'```tsv\n(.*?)```', t, re.S) for l in b.splitlines() if l.strip() and not l.startswith('#')]


def shares(game, concepts):
    """faction -> share of its cards with any of the concepts (or one under them)"""
    got = {i for x in concepts for (i,) in c.execute('select card from flat_concept where under(concept, ?)', (x,))}
    got |= {a for a, b in c.execute('select card, made from flat_made') if b in got}  # a card is what it makes
    per = collections.defaultdict(lambda: [0, 0])
    for i, regs in c.execute("""select id, regions from card where game=? and is_keyword=0 and is_stub=0 and coalesce(category,'')
                                not in ('game_rule','ability','boss','monster','event','modifier')""", (game,)):
        for r in (regs or '').split(';'):
            if r: per[r][1] += 1; per[r][0] += i in got
    return {r: n / t for r, (n, t) in per.items() if t}


def ranked(game, concepts):
    s = shares(game, concepts)
    return [r for r, _ in sorted(s.items(), key=lambda x: -x[1]) if r.lower().split(' (')[0] not in NOT_FACTION], s


def combo(game, a, b):
    ids = {n: i for i, n in c.execute('select id, name from card where game=? order by is_keyword desc', (game,))}  # a sigil or keyword named in a combo too
    if a not in ids or b not in ids: return None
    lines = network.network(c, game, [ids[a], ids[b]])[1]
    return bool(lines.get((ids[a], ids[b])) or lines.get((ids[b], ids[a])) or list(connections.reasons(c, a, b))
                or list(connections.reasons(c, b, a)))


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
