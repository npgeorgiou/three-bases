"""Checks of the links between cards, for every game (run by run.py; lists, never fails the build; a new game must explain
or fix every line it prints). Found by Kaptain's check of the deck networks (29 Oct 2026):
  1 needs no card of the game makes: something a card waits for, counts or tests that no effect, keyword or card causes
    (a missing `causes`, a keyword condition with no record, two words for one event: activated / trap_activated)
  2 keywords without a vocab concept row, and keyword conditions or action keywords whose record has no rows
  3 champions with a level-up condition but no level-up form (cards the source lacks: take them from the game's data)
  4 cards named in effects (summon X, plant X) that are no card of the game
  6 keyword entries that hold no definition, only a pointer to other pages (Inscryption's Ants and Ant kept just "This
    article is about the variable stat..."; the readers wrote nothing, so Ant Queen did not count Ants)
  5 cards of a guide deck (decks.tsv, cases/decks.tsv) that are no card of the game: the game's card list is not whole (the
    library merged Inscryption cards with the same text and dropped cards without sigils: Hawk, Wolf, Coyote)
Usage: audit_links.py <game> [...]"""
import collections, csv, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deck_analysis
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
nm = lambda i: (c.execute('select name from card where id=?', (i,)).fetchone() or ['?'])[0]


def audit(g):
    out = []
    rows = c.execute("""select f.card, f.role, f.happening, f.side, f.keyword, f.pick, f.origin from flat_ref f join card k on k.id=f.card
                        where k.game=? and k.is_keyword=0 and k.is_stub=0""", (g,)).fetchall()
    makes = collections.defaultdict(set)
    for card, role, h, side, kw, pick, o in rows:
        if role == 'makes': makes[h].add((side, kw))
    need = collections.defaultdict(set)
    for card, role, h, side, kw, pick, o in rows:
        if role == 'makes' or h in deck_analysis.EVERY_GAME or (pick == 'self' and h in ('played', 'summoned')): continue
        if o not in ('own', 'uses_keyword'): continue
        s = 'mine' if pick == 'self' else side
        if not any((ms in ('', 'any', None) or s in ('', 'any', None) or ms == s) and (mk is None or kw is None or mk == kw) for ms, mk in makes.get(h, ())):
            need[(h, nm(kw) if kw else '', s or 'any')].add(card)
    out += [f'1 nothing makes "{h}{" " + k if k else ""}" ({s}), needed by {len(v)}: ' + ', '.join(sorted(nm(i) for i in v)[:5])
            for (h, k, s), v in sorted(need.items(), key=lambda x: -len(x[1]))]
    vocab = {(r['field'], r['value']) for r in csv.DictReader(open(os.path.join(HERE, 'vocab.tsv'), encoding='utf-8'), delimiter='\t')}
    for i, n in c.execute('select id, name from card where game=? and is_keyword=1', (g,)):
        used = c.execute('select (select count(*) from card_keyword where keyword=?) + (select count(*) from flat_do where keyword_ref=?) + '
                         '(select count(*) from cond where ref_keyword=?)', (i, i, i)).fetchone()[0]
        if not used: continue
        if ('keyword', n) not in vocab and ('keyword', f'{g}:{n}') not in vocab: out.append(f'2 keyword {n} (used {used}x) has no vocab concept row')
        has_rows = c.execute('select 1 from ability where card=? union select 1 from cond where keyword=? union select 1 from keyword_trigger where keyword=?',
                             (i, i, i)).fetchone()
        if not has_rows and c.execute("select 1 from cond where ref_keyword=? and test='keyword_condition' union select 1 from flat_do d join card u "
                                      "on u.id=d.card where d.keyword_ref=? and d.act='keyword_action' and u.is_keyword=0", (i, i)).fetchone():
            out.append(f'2 keyword {n} is a condition or an action but its record has no rows')
    for i, n in c.execute("""select distinct k.id, k.name from card k join flat_do d on d.card=k.id and d.act='level_up' where k.game=? and
                             k.is_stub=0 and k.is_keyword=0 and d.origin='own' and d.on_pick='self' and not exists (select 1 from card_link l where l.src=k.id and l.rel='transforms_into')
                             and not exists (select 1 from flat_do t where t.card=k.id and t.act='transform' and t.card_ref is not null)""", (g,)):
        out.append(f'3 {n} levels up but has no level-up form')
    for n, cnt in c.execute("""select k.name, count(*) from flat_do d join card k on k.id=d.card_ref where k.game=? and k.is_stub=1 group by k.id""", (g,)):
        out.append(f'4 {n} is named by {cnt} effects but is no card')
    for f in ('decks.tsv', os.path.join('cases', 'decks.tsv')):
        for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t'):
            if r['game'] != g: continue
            miss = deck_analysis.parse_deck(c, g, r['cards'])[1]  # read as the networks read it
            if miss: out.append(f"5 deck {r['deck']} names {len(miss)} cards that are no card: " + ', '.join(miss[:6]))
    import source
    for n, t in source.lib().execute("select name, text from entities where game=? and category='keyword'", (g,)):
        t = ' '.join((t or '').split())
        if re.fullmatch(r"(?:This (?:article|page) is about [^.]*\.\s*(?:For [^.]*\.\s*)*)", t): out.append(f'6 keyword {n} has no definition, only: {t[:80]}')
    return out


if __name__ == '__main__':
    for g in sys.argv[1:]:
        o = audit(g); print(f'{g}: {len(o)} link findings'); print('\n'.join('  ' + x for x in o))
