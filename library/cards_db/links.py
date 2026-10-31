"""Every line network.py draws between two cards of one game that can share a deck, stored in links.sqlite (not in git; rebuilt
from cards.sqlite). Tables: phrase(id, kind, text) with the two cards' names as {A} and {B}; link(game, a, b, phrase, weight).
Usage: links.py [game ...]   (no game: all; a game's old rows are replaced)"""
import os, random, sqlite3, sys, time
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


def build(c, L, game):
    t = time.time()
    ids = [i for (i,) in c.execute(OWNED, (game,))]; owned = set(ids)
    names = {i: n for i, n in c.execute('select id, name from card where game=?', (game,))}
    print(game, 'sample:', ', '.join(names[i] for i in random.Random(1).sample(ids, min(10, len(ids)))))
    nodes, lines = network.network(c, game, ids)
    phr = {(k, x): i for i, k, x in L.execute('select id, kind, text from phrase')}
    L.execute('delete from link where game=?', (game,)); pairs = rows = 0
    for (a, b), ls in lines.items():
        if a not in owned or b not in owned or a == b or not deck_analysis.can_share(c, game, a, b): continue
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


main()
