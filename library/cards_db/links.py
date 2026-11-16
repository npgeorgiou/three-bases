"""Every line network.py draws between two cards of one game that can share a deck, stored in links.sqlite (not in git; rebuilt
from cards.sqlite). Tables: phrase(id, kind, text) with the two cards' names as {A} and {B}; link(game, a, b, phrase, weight, site, a_ab, b_ab): site = the
network.py line of the rule that made it (one sentence can come from several rules); a_ab, b_ab = what of each card made it
(effect rows 'ability.seq', ability ids, 'kw<keyword id>', 'c:<concept>', 'type', 'rule'; several joined by ';').
Usage: links.py [game ...]   (no game: all; a game's old rows are replaced; then the cases of cases/links.tsv)"""
import collections, csv, os, random, sqlite3, sys, time
import network, deck_analysis

HERE = os.path.dirname(os.path.abspath(__file__))
OWNED = ("select id from card where game=? and is_keyword=0 and is_stub=0 and coalesce(category,'') not in "
         "('game_rule','boss','monster','event','modifier','tribe') "
         "and not (coalesce(category,'')='terrain' and game not in ('inscryption'))")  # map tiles; Inscryption's Terrain cards are creatures
WORD_KIND = {w: k for k, w in network.KIND_WORD.items()}
NO_STORE = ('carries',)  # Into the Breach: a mech and what it carries comes from a deck's order, not from two cards


def reasons(kind, why):
    """a pair's joined reasons, each with its kind: "costs 6: ...; also makes stronger: can give it +3|+3" """
    out = []
    for n, part in enumerate(why.split('; also ')):
        k = kind
        if n:
            w = next((w for w in sorted(WORD_KIND, key=len, reverse=True) if part.startswith(w + ': ')), None)
            if w: k, part = WORD_KIND[w], part[len(w) + 2:]
        out.append((k, part))
    return out


def as_phrase(text, a_name, b_name):
    """the reason with the two cards' names as {A} and {B}, the longer name first ("Zed (level 2)" before "Zed")"""
    for name, mark in sorted(((a_name, '{A}'), (b_name, '{B}')), key=lambda x: -len(x[0])):
        text = text.replace(name, '\0' + mark[1] + '\0')
    return text.replace('\0A\0', '{A}').replace('\0B\0', '{B}')


# Inscryption cards only a boss or the map uses: the wiki Cards page's "Non-obtainable / Boss exclusive" lists of every act
# (inscryption.fandom.com/wiki/Cards, read 31 Oct 2026; "Mole" and "The Daus" of Act III are Mole (Act III), Daus (Act III))
INSCRYPTION_NOT_OWNED = ('Bait Bucket', 'Gold Nugget', 'Grand Fir', 'Leaping Trap', 'Pack Mule', 'Snowy Fir', 'Starvation',
    'Strange Frog', 'Stump', 'The Moon', 'Mole Seaman', 'Skeleton Crew', 'Zombie Parrot', 'The Limoncello', 'Burrowing Trap',
    'Kingfisher', 'Coyote', 'Inspector', 'Melter', 'Magnus Mox', '!CORRUPTED', 'Ancient Fir', 'Dead Tree', 'Annoy FM',
    'Bridge Rails', 'Broken Bot', 'Conduit Tower', 'Tombstone', 'Librarian', 'Mole (Act III)', 'Daus (Act III)', 'Shutterbug')
INSCRYPTION_NOT_CARDS = ('Consumable Items',)  # the wiki's page about all items, imported as an item: no card
ENEMY_CATS = ('boss', 'monster')  # an event gives the player its cards (Council of Ghosts: Apparitions), so it is no enemy


def owned(c, game):
    """the cards a player owns (Kaptain 31 Oct 2026): not a keyword, stub, rule, boss, monster, event, modifier or tribe; not a card
    only a boss or the map uses (Inscryption: the wiki's list; a card some act offers or a deck lists stays: Kingfisher); not a
    card of no deck rarity that only bosses, monsters or such cards make (Duelyst: Restoring Light, made only by boss Generals)"""
    ids = {i for (i,) in c.execute(OWNED, (game,))}
    listed = deck_listed(c, game)
    rar = dict(c.execute('select id, rarity from card where game=?', (game,)))
    nm = dict(c.execute('select id, name from card where game=?', (game,)))
    enemy = {i for (i,) in c.execute(f"select id from card where game=? and category in ({','.join('?' * len(ENEMY_CATS))})", (game,) + ENEMY_CATS)}
    drop = set()
    if game == 'inscryption':
        off = inscryption_offered()
        drop = {i for i in ids if (nm[i] in INSCRYPTION_NOT_OWNED and nm[i].lower() not in off and i not in listed) or nm[i] in INSCRYPTION_NOT_CARDS}
    makers = collections.defaultdict(set)
    for a, b in c.execute("select src, dst from card_link where rel in ('transforms_into', 'generates') and src!=dst"): makers[b].add(a)
    for a, b, side in c.execute(f"select card, card_ref, act in ('summon','create','copy') and 'enemy' in (coalesce(on_side,''), coalesce(to_side,'')) from flat_do where act in "
                                f"({','.join('?' * len(network.PUTS))}) and card_ref is not null and card_ref!=card", list(network.PUTS)):
        makers[b].add(-1 if side else a)  # made on the enemy's side (Cuckoo's Broken Egg): the enemy owns it
    enemy.add(-1)
    while True:  # Skeleton Crew is made only by The Limoncello
        more = {i for i in ids - drop if makers.get(i) and makers[i] <= enemy | drop and i not in listed
                and (game == 'inscryption' or rar.get(i) in (None, 'tokenunit', 'special'))}
        if not more: return ids - drop
        drop |= more


def deck_listed(c, game):
    listed = set()
    for f in ('decks.tsv', os.path.join('cases', 'decks.tsv')):
        for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t'):
            if r['game'] == game: listed |= set(deck_analysis.parse_deck(c, game, r['cards'])[0])
    return listed


def only_made(c, game, owned):
    """cards that come only from other cards: made by one (levels into it, a skill it casts, makes, plants or puts into play),
    of no deck rarity (none, token, special) and in no deck of decks.tsv"""
    marks = ','.join('?' * len(owned)); q = list(owned)
    got = {b for (b,) in c.execute(f"select dst from card_link where rel in ('transforms_into', 'generates') and src in ({marks}) and dst!=src", q)}
    got |= {b for (b,) in c.execute(f"select card_ref from flat_do where act in ({','.join('?' * len(network.PUTS))}) and card in ({marks}) "
                                     f"and card_ref!=card", list(network.PUTS) + q)}
    listed = deck_listed(c, game)
    rar = dict(c.execute('select id, rarity from card where game=?', (game,)))
    if game == 'inscryption':  # no rarities: a card the game offers (a card choice, the Trader, a pack, a rare) has an offer category
        offered = inscryption_offered()
        rar = {i: 'offered' if n.lower() in offered else None for i, n in c.execute('select id, name from card where game=?', (game,))}
    by = collections.defaultdict(set)  # who makes each card
    for a, b in c.execute(f"select src, dst from card_link where rel in ('transforms_into', 'generates') and src in ({marks}) and dst!=src", q): by[b].add(a)
    for a, b in c.execute(f"select card, card_ref from flat_do where act in ({','.join('?' * len(network.PUTS))}) and card in ({marks}) "
                          f"and card_ref!=card", list(network.PUTS) + q): by[b].add(a)
    nm = dict(c.execute('select id, name from card where game=?', (game,)))
    # two forms that turn into each other (GR1ZZ and GR1ZZ (Beast Form), Transformer): the one whose name the other extends is played
    base = {b for b in got if by[b] and all(b in by.get(a, ()) and nm[a].startswith(nm[b] + ' ') for a in by[b])}
    return {b for b in got & set(owned) if rar.get(b) in (None, 'tokenunit', 'special') and b not in listed and b not in base}


def inscryption_offered():
    """names of the wiki's Inscryption cards with an offer category (ChoiceNode, TraderOffer, GBCPack, Part3Random, AscensionUnlock, Rare)"""
    import json, re
    out = set()
    for f in ('inscryption_wiki_cards.jsonl', 'inscryption_wiki_cards_more.jsonl'):
        for line in open(os.path.join(HERE, '..', 'sources', f), encoding='utf-8'):
            d = json.loads(line)
            if re.search(r'ChoiceNode|TraderOffer|GBCPack|Part3Random|AscensionUnlock|Rare card', d['b']): out.add(d['title'].lower())
    return out


def build(c, L, game):
    t = time.time()
    mine = owned(c, game); ids = sorted(mine)
    names = {i: n for i, n in c.execute('select id, name from card where game=?', (game,))}
    print(game, 'sample:', ', '.join(names[i] for i in random.Random(1).sample(ids, min(10, len(ids)))))
    only = only_made(c, game, mine)  # as in a deck: a card only other cards make is "made" (Wraithling, Chime, a level-up form)
    nodes, lines = network.network(c, game, [i for i in ids if i not in only])
    rule_ab = {str(i) for (i,) in c.execute("select a.id from ability a join card k on k.id=a.card where k.category='game_rule'")}
    as_src = lambda x: 'rule' if x.split('.')[0] in rule_ab else x  # an ability of a game rule (units fight, Blood is paid): the game's rules
    src_by = collections.defaultdict(list)  # (a, b) -> [(sentence, sources)]: for a reason joined from two lines
    for (a, b, z), v in network.SRC.items(): src_by[(a, b)].append((z, v))
    phr = {(k, x): i for i, k, x in L.execute('select id, kind, text from phrase')}
    L.execute('delete from link where game=?', (game,)); pairs = rows = 0
    for (a, b), ls in lines.items():
        if a not in mine or b not in mine or a == b or not deck_analysis.can_share(c, game, a, b): continue
        kind, weight, why = ls[0]; got = False
        for k, part in reasons(kind, why):
            if k in NO_STORE: continue
            key = (k, as_phrase(part, names[a], names[b]))
            if key not in phr:
                phr[key] = L.execute('insert into phrase(kind, text) values (?, ?)', key).lastrowid
            site = min(network.SITE.get((a, b, part)) or network.SITE.get((a, b, why)) or {0})
            src = network.SRC.get((a, b, part)) or network.SRC.get((a, b, why)) or \
                {x for z, v in src_by.get((a, b), ()) if z in why or part in z for x in v}  # what of A and of B made it; a reason joined from
            # two (one_link: "brings it back" + "its summon effect goes off"): the lines it was joined from
            a_ab = ';'.join(sorted({as_src(x) for s_, _ in src for x in s_.split(';') if x})) or None
            b_ab = ';'.join(sorted({as_src(x) for _, s_ in src for x in s_.split(';') if x})) or None
            L.execute('insert into link values (?, ?, ?, ?, ?, ?, ?, ?)', (game, a, b, phr[key], weight, site, a_ab, b_ab)); rows += 1; got = True
        pairs += got
    used = L.execute('select count(distinct phrase) from link where game=?', (game,)).fetchone()[0]
    print(f'{game}: {len(ids)} cards, {pairs} pairs, {rows} rows, {used} phrases, {time.time() - t:.0f} s')


def side_says(c, src):
    """what a link's a_ab or b_ab holds, as words a case can test: each concept of its rows ('ability.seq': that effect row only;
    an ability: all its rows), and 'type', 'rule' or 'kw' for a source with no ability"""
    out = set()
    for x in (src or '').split(';'):
        if not x: continue
        if x.startswith('kw'): out |= {'kw'} | {v for (v,) in c.execute("""select v.tree from card k join vocab v on v.field='keyword' and
                                          v.value in (k.name, k.game || ':' || k.name) where k.id=?""", (int(x[2:]),)) if v} if x[2:].isdigit() else {'kw'}
        elif x.startswith('c:'): out.add(x[2:])
        elif not x[0].isdigit(): out.add(x)
        else:
            ab, _, sq = x.partition('.')
            q = 'select concept from flat_do where ability=? and seq=?' if sq else \
                'select concept from flat_do where ability=? union select concept from flat_if where ability=? union select concept from flat_when where ability=?'
            out |= {v for (v,) in c.execute(q, (int(ab), int(sq)) if sq else (int(ab),) * 3) if v}
    return out


def side_fails(c, want, src):
    """a case's a_side / b_side: words that must be there, '!word' that must not; an empty source fails any test"""
    if not (want or '').strip(): return ''
    if not src: return 'no source'
    got = side_says(c, src)
    bad = [w for w in want.split() if (w[1:] in got) if w.startswith('!')] + [w for w in want.split() if not w.startswith('!') and w not in got]
    return f"{', '.join(bad)} (has {', '.join(sorted(got))})" if bad else ''


def foreign_sides(c, L):
    """link sides naming an effect that is not on that card (its own rows, a keyword's rows it has, or its abilities): a rule
    that took an ability from flat_ref without its origin (a game rule's ability is the game's rules)"""
    on = collections.defaultdict(set)
    for t in ('flat_do', 'flat_if', 'flat_when'):
        for card, ab in c.execute(f'select distinct card, ability from {t} where ability is not null'): on[card].add(str(ab))
    for i, card in c.execute('select id, card from ability'): on[card].add(str(i))
    return sum(1 for a, b, sa, sb in L.execute('select a, b, a_ab, b_ab from link') for card, s in ((a, sa), (b, sb))
               for t in (s or '').split(';') if t[:1].isdigit() and t.split('.')[0] not in on[card])


def case_failures(c, games):
    """cases/links.tsv: a line of the table that must be there (with the reason's words, when given) or must not; a_side and b_side:
    what of each card must have made it (side_fails); returns the rows that fail"""
    c.execute(f"attach database '{os.path.join(HERE, 'links.sqlite')}' as L") if 'L' not in [d[1] for d in c.execute('pragma database_list')] else None
    bad = []
    for r in csv.DictReader(open(os.path.join(HERE, 'cases', 'links.tsv'), encoding='utf-8'), delimiter='\t'):
        if r['game'] not in games: continue
        q = """select p.kind || ': ' || p.text, l.a_ab, l.b_ab from L.link l join L.phrase p on p.id=l.phrase join card a on a.id=l.a join card b on b.id=l.b
               where l.game=? and b.name=?""" + ('' if r['from'] == '*' else ' and a.name=?')
        got = c.execute(q, (r['game'], r['to']) + (() if r['from'] == '*' else (r['from'],))).fetchall()
        hit = [x for x in got if r['reason'] in x[0]]
        if bool(hit) != (r['expect'] == 'line'): bad.append(f"{r['id']} {r['from']} -> {r['to']} {r['expect']} {r['reason']}: {'; '.join(x[0] for x in got)[:200] or '-'}"); continue
        for side, col in (('a_side', 1), ('b_side', 2)):
            why = [side_fails(c, r.get(side), x[col]) for x in hit]
            if hit and all(why): bad.append(f"{r['id']} {r['from']} -> {r['to']} {side} {r[side]}: {why[0]}")
    return bad


def main():
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
    bad = deck_analysis.share_failures(c)
    if bad: sys.exit('can_share fails cases/share.tsv:\n' + '\n'.join(bad))
    games = sys.argv[1:] or [g for (g,) in c.execute('select distinct game from card order by game')]
    L = sqlite3.connect(os.path.join(HERE, 'links.sqlite'))
    L.executescript("""create table if not exists phrase(id integer primary key, kind text, text text);
        create table if not exists link(game text, a integer, b integer, phrase integer, weight real, site integer, a_ab text, b_ab text);
        create index if not exists la on link(game, a); create index if not exists lb on link(game, b);
        create index if not exists lp on link(phrase);""")
    for col in ('a_ab', 'b_ab'):
        if col not in [r[1] for r in L.execute('pragma table_info(link)')]: L.execute(f'alter table link add column {col} text')
    for g in games: build(c, L, g); L.commit()
    L.execute('delete from phrase where id not in (select phrase from link)'); L.commit(); L.execute('vacuum')
    print(f'links.sqlite: {os.path.getsize(os.path.join(HERE, "links.sqlite")) / 1e6:.1f} MB')
    L.close(); bad = case_failures(c, games)
    print('cases/links.tsv: ' + ('all pass' if not bad else 'FAILED\n  ' + '\n  '.join(bad)))
    n = foreign_sides(c, L)
    print('link sides naming another card\'s effect: ' + ('none' if not n else f'{n} FAILED'))


if __name__ == '__main__': main()
