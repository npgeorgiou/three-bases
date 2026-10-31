"""Every line network.py draws between two cards of one game that can share a deck, stored in links.sqlite (not in git; rebuilt
from cards.sqlite). Tables: phrase(id, kind, text) with the two cards' names as {A} and {B}; link(game, a, b, phrase, weight).
Usage: links.py [game ...]   (no game: all; a game's old rows are replaced; then the cases of cases/links.tsv)"""
import collections, csv, os, random, sqlite3, sys, time
import network, deck_analysis

HERE = os.path.dirname(os.path.abspath(__file__))
OWNED = ("select id from card where game=? and is_keyword=0 and is_stub=0 and coalesce(category,'') not in "
         "('game_rule','boss','monster','event','modifier','tribe')")
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
        drop = {i for i in ids if nm[i] in INSCRYPTION_NOT_OWNED and nm[i].lower() not in off and i not in listed}
    makers = collections.defaultdict(set)
    for a, b in c.execute("select src, dst from card_link where rel in ('transforms_into', 'generates') and src!=dst"): makers[b].add(a)
    for a, b in c.execute(f"select card, card_ref from flat_do where act in ({','.join('?' * len(network.PUTS))}) and card_ref is not null "
                          f"and card_ref!=card", list(network.PUTS)): makers[b].add(a)
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
    return {b for b in got & set(owned) if rar.get(b) in (None, 'tokenunit', 'special') and b not in listed}


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
            L.execute('insert into link values (?, ?, ?, ?, ?)', (game, a, b, phr[key], weight)); rows += 1; got = True
        pairs += got
    used = L.execute('select count(distinct phrase) from link where game=?', (game,)).fetchone()[0]
    print(f'{game}: {len(ids)} cards, {pairs} pairs, {rows} rows, {used} phrases, {time.time() - t:.0f} s')


def case_failures(c, games):
    """cases/links.tsv: a line of the table that must be there (with the reason's words, when given) or must not; returns the rows that fail"""
    c.execute(f"attach database '{os.path.join(HERE, 'links.sqlite')}' as L") if 'L' not in [d[1] for d in c.execute('pragma database_list')] else None
    bad = []
    for r in csv.DictReader(open(os.path.join(HERE, 'cases', 'links.tsv'), encoding='utf-8'), delimiter='\t'):
        if r['game'] not in games: continue
        q = """select p.kind || ': ' || p.text from L.link l join L.phrase p on p.id=l.phrase join card a on a.id=l.a join card b on b.id=l.b
               where l.game=? and b.name=?""" + ('' if r['from'] == '*' else ' and a.name=?')
        got = [x for (x,) in c.execute(q, (r['game'], r['to']) + (() if r['from'] == '*' else (r['from'],)))]
        hit = [x for x in got if r['reason'] in x]
        if bool(hit) != (r['expect'] == 'line'): bad.append(f"{r['id']} {r['from']} -> {r['to']} {r['expect']} {r['reason']}: {'; '.join(got)[:200] or '-'}")
    return bad


def main():
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
    bad = deck_analysis.share_failures(c)
    if bad: sys.exit('can_share fails cases/share.tsv:\n' + '\n'.join(bad))
    games = sys.argv[1:] or [g for (g,) in c.execute('select distinct game from card order by game')]
    L = sqlite3.connect(os.path.join(HERE, 'links.sqlite'))
    L.executescript("""create table if not exists phrase(id integer primary key, kind text, text text);
        create table if not exists link(game text, a integer, b integer, phrase integer, weight real);
        create index if not exists la on link(game, a); create index if not exists lb on link(game, b);
        create index if not exists lp on link(phrase);""")
    for g in games: build(c, L, g); L.commit()
    L.execute('delete from phrase where id not in (select phrase from link)'); L.commit(); L.execute('vacuum')
    print(f'links.sqlite: {os.path.getsize(os.path.join(HERE, "links.sqlite")) / 1e6:.1f} MB')
    L.close(); bad = case_failures(c, games)
    print('cases/links.tsv: ' + ('all pass' if not bad else 'FAILED\n  ' + '\n  '.join(bad)))


if __name__ == '__main__': main()
