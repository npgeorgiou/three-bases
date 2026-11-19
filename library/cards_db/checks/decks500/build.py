"""Turns the fetched deck files of this folder into new decks.tsv rows (decks_new.tsv) and a count per game.
Run from library/cards_db/: python3 checks/decks500/build.py [--write]  (--write appends decks_new.tsv to decks.tsv)
Picks per game: top-rated first, then variety (faction, average cost, key cards: champions, leader, general, archetype),
never two decks of a game sharing more than 80% of their cards. Card names the library does not know stay as written."""
import sys, os, re, csv, json, sqlite3, collections, unicodedata
sys.path.insert(0, '.')
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import source, lor
P = lambda f: os.path.join(D, f)
lib = source.lib()
db = sqlite3.connect('cards.sqlite')
TARGET = {'marvel_snap': 500, 'faeria': 500, 'runeterra': 500, 'gwent': 500, 'duelyst': 300, 'stormbound': 300,
          'sts1': 10**6, 'monster_train': 10**6, 'inscryption': 10**6, 'into_the_breach': 10**6}


def norm(s):
    s = unicodedata.normalize('NFKD', s).replace('’', "'").replace('‘', "'")
    return re.sub(r'[^a-z0-9]', '', ''.join(ch for ch in s if not unicodedata.combining(ch)).lower())


known, cost, region = {}, {}, {}
for g in TARGET:
    known[g] = {}
    for n, c, r in db.execute('select name, cost, regions from card where game=? and is_keyword=0 and is_stub=0', (g,)):
        known[g].setdefault(norm(n), n); cost[(g, n)] = c; region[(g, n)] = r
def name(g, n):
    n = ' '.join(n.split())
    return known[g].get(norm(n), n)


existing = collections.defaultdict(list); names_used = collections.defaultdict(set)
for r in csv.DictReader(open('decks.tsv', encoding='utf-8'), delimiter='\t'):
    existing[r['game']].append({x.strip() for x in r['cards'].split(', ')}); names_used[r['game']].add(r['deck'])
def sim(a, b): return len(a & b) / max(len(a), len(b))
def copies(cards): return ', '.join(f'{n} {k}' for n, k in cards)
def clean(s): return re.sub(r'\s+', ' ', ''.join(ch for ch in s if unicodedata.category(ch)[0] in 'LNPZ' or ch in "'&+-")).strip(' -|')
def uniq_name(g, nm):
    nm = clean(nm) or 'deck'; n, i = nm, 2
    while n in names_used[g]: n = f'{nm} ({i})'; i += 1
    names_used[g].add(n); return n

cands = collections.defaultdict(list)  # game -> dict(name, source, cards=[(name, count)], group, keys, score)
def add(g, **c):
    c['cards'] = [(name(g, n), k) for n, k in c['cards'] if n.strip()]
    cands[g].append(c)

# Gwent: playgwent.com deck guides, the most voted guides of each faction and leader ability
L = open(P('gwent_raw.txt'), encoding='utf-8').read().split('\n'); GD = L[0].split('~')
GF = {'mon': 'monsters', 'nil': 'nilfgaard', 'nor': 'northern realms', 'sco': "scoia'tael", 'ske': 'skellige', 'syn': 'syndicate'}
for l in L[1:]:
    i, v, dt, f, au, nm, ld, st, cs = l.split('|')
    cards = [(GD[int(t.partition('x')[0])], int(t.partition('x')[2] or 1)) for t in cs.split()]
    one = sum(1 for _, k in cards if k == 1); two = sum(1 for _, k in cards if k == 2); tot = sum(k for _, k in cards)
    lead = [(GD[int(ld)], 1)] + ([(GD[int(st)], 1)] if GD[int(st)] else [])
    add('gwent', name=nm or f'Gwent guide {i}', cards=lead + cards, group=GF[f], keys={GD[int(ld)]}, score=int(v),
        source=f'https://www.playgwent.com/en/decks/guides/{i} (deck guide, {v} votes, {dt}, by {au}); full deck: {tot} cards, {one} with one copy and {two} with two, plus leader ability and stratagem (deck size 25 or more)')

# Runeterra: runeterra.ar meta, each archetype's most played list and the lists its best players play (ranked, last days)
rn = {e: n.strip() for e, n in lib.execute("select ext_id, name from entities where game='runeterra'")}
hero = {e for e, in lib.execute("select ext_id from entities where game='runeterra' and category='hero'")}
for l in open(P('rt_ar.txt'), encoding='utf-8'):
    fmt, kind, arch, cnt, wr, who, code, dt = l.rstrip('\n').split('|')
    try: cs = lor.decode(code)
    except Exception: continue
    cards = [(rn.get(c, c), k) for c, k in cs]
    champs = sorted({rn[c] for c, _ in cs if c in hero})
    regs = sorted({c[2:4] for c, _ in cs})
    by = f'the archetype\'s most played list ({cnt} ranked games, {wr}% won)' if kind == 'arch' else f'played by {who} ({cnt} ranked games, {wr}% won)'
    add('runeterra', name=arch + ('' if kind == 'arch' else f' ({who})'), cards=cards, group='+'.join(regs), keys=set(champs) or {arch},
        score=int(cnt) * (2 if kind == 'arch' else 1),
        source=f'https://runeterra.ar/lor/meta/code/{code}; runeterra.ar {fmt} meta of {dt}, archetype {arch}: {by}; decoded from the deck code; full deck: 40 cards; copies: {copies(cards)}')

# Stormbound: every deck ever in Stormbound-Kitty's featured list and tournament hall of fame (the site's GitHub history)
sb = {k.upper(): v.strip() for k, v in lib.execute("select ext_id, name from entities where game='stormbound'")}
FAC = {'n': 'neutral', 's': 'swarm', 'w': 'winter', 'f': 'shadowfen', 'i': 'ironclad'}
def sb_toks(i):
    if not re.match(r'^[0-9]', i):  # the site's older ids: base64 of "5N1,5N2,..." (level, then the card)
        import base64
        try: return [t.strip(' "')[1:].lower() for t in base64.b64decode(i + '=' * (-len(i) % 4)).decode().strip(' "').split(',')]
        except Exception: return []
    if re.match(r'^\dx', i): return re.findall(r'[nswfi]\d+', i[2:])
    return [t[1:] for t in re.findall(r'\d[nswfi]\d+?(?=\d[nswfi]|$)', i)]
for i, d in json.load(open(P('sb_git.json'), encoding='utf-8')).items():
    toks = sb_toks(i)
    if len(toks) != 12: continue
    cards = [(sb.get(t.upper(), t.upper()), 1) for t in toks]
    fac = sorted({FAC[t[0]] for t in toks} - {'neutral'}) or ['neutral']
    tags = [x.lower().replace('_', ' ') for x in d.get('tags', [])]
    if d['kind'] == 'featured':
        what = f"Stormbound-Kitty featured deck by {d.get('author')}, {d.get('date')}" + (f"; tags: {', '.join(tags)}" if tags else '') + (f"; marked nerfed {d['nerfed']}" if d.get('nerfed') else '')
        sc = 3 if not d.get('nerfed') else 2
    else:
        what = f"Stormbound-Kitty tournament hall of fame: {d.get('name')} ({d.get('date')})"; sc = 4
    add('stormbound', name=d.get('name') if d['kind'] == 'featured' else f"{d.get('name')} deck", cards=cards, group='+'.join(fac),
        keys={next((t for t in tags if t in ('rush', 'control', 'midrange')), '')} - {''} or {'+'.join(fac)}, score=sc,
        source=f'https://stormbound-kitty.com/deck/{i}/detail; {what}; found in the site\'s deck lists on GitHub (KittySparkles/stormbound-kitty, src/data); 12 cards, one copy each')

# Slay the Spire: winning Ascension 20 runs (the Heart beaten) of top streamers, github.com/MaT1g3R/Slay-the-Spire-data
sts = {e: n.strip() for e, n in lib.execute("select ext_id, name from entities where game='sts1'")}
WHO = {'chegs': 'Chegs', 'robit': 'Robit', 'panacea-ironclad-sample': 'Panacea108', 'bad-silent': 'vmService (Bad Silent)',
       '200-rotating-sample': 'vmService', 'lose-all-gold-max-hp-sample': 'vmService'}
CH = {'IRONCLAD': 'Ironclad', 'THE_SILENT': 'Silent', 'DEFECT': 'Defect', 'WATCHER': 'Watcher'}
def sts_id(x): return sts.get(re.sub(r'\+\d+$', '', x).upper().replace(' ', '_').replace('-', '_'), re.sub(r'\+\d+$', '', x))
for r in json.load(open(P('sts_runs.json'), encoding='utf-8')):
    cnt = collections.Counter(sts_id(x) for x in r['deck'])
    cards = list(cnt.items()) + [(sts_id(x), 1) for x in r['relics']]
    who = WHO.get(r['file'].split('/')[1], r['file'].split('/')[1])
    top = [n for n, _ in cnt.most_common() if not n.startswith(('Strike', 'Defend'))][:3]
    add('sts1', name=f"{CH[r['char']]} {' '.join(top[:2])} ({who})", cards=cards, group=CH[r['char']], keys={top[0]} if top else set(),
        score=1, source=f"https://github.com/MaT1g3R/Slay-the-Spire-data/blob/master/{r['file']} ; {who}'s winning Ascension 20 run (the Heart beaten), "
                         f"the run file's final deck ({len(r['deck'])} cards) and relics; copies: {copies(list(cnt.items()))}")

# Marvel Snap: Untapped.gg archetype pages as the Internet Archive kept them, each the archetype's most played deck then
for l in open(P('ms_untapped_archive.txt'), encoding='utf-8'):
    _, snap, arch, ng, nw, ag, tf, cs = l.rstrip('\n').split('|')
    ts, url = snap.split(' ', 1)
    cards = [(c.split('*')[0], 1) for c in cs.split(';')]
    add('marvel_snap', name=f'{arch} (Untapped {ts[:4]}-{ts[4:6]})', cards=cards, group=arch, keys={arch}, score=int(ng),
        source=f'https://web.archive.org/web/{ts}/{url} ; Untapped.gg archetype page as archived {ts[:4]}-{ts[4:6]}-{ts[6:8]}: the most played {arch} deck, '
               f'{ng} games, {round(100 * int(nw) / max(1, int(ng)))}% won; full deck: 12 cards, one copy each')
if os.path.exists(P('ms_msz_articles.txt')):
    msn = {e: n.strip() for e, n in lib.execute("select ext_id, name from entities where game='marvel_snap'")}
    seen = {}  # one deck per card list: the articles that show it (how often Marvel Snap Zone's writers picked it)
    for l in open(P('ms_msz_articles.txt'), encoding='utf-8'):
        if not l.strip(): continue
        snap, title, dn, cs = l.rstrip('\n').split('|')
        ids = cs.split(';')
        if len(ids) != 12: continue
        k = tuple(sorted(ids))
        if k in seen: seen[k]['n'] += 1; continue
        ts, url = snap.split(' ', 1)
        seen[k] = dict(n=1, ts=ts, url=url, title=title.replace(' - Marvel Snap Zone', ''), dn=dn, ids=ids)
    for d in seen.values():
        add('marvel_snap', name=d['dn'] or d['title'], cards=[(msn.get(x, x), 1) for x in d['ids']], group=d['dn'] or d['title'], keys={d['dn'] or d['title']},
            score=d['n'], source=f"{d['url']} (archived https://web.archive.org/web/{d['ts']}/{d['url']}); Marvel Snap Zone article \"{d['title']}\", "
                                 f"shown in {d['n']} of the site's tier-list and best-decks articles; decoded from the article's deck code; full deck: 12 cards, one copy each")

# Duelyst: manaspring.ru deck lists (rating, author, general), as the Internet Archive kept them
if os.path.exists(P('du_manaspring.txt')):
    gfac = {n: r for n, r in db.execute("select name, regions from card where game='duelyst' and category='leader'")}
    for l in open(P('du_manaspring.txt'), encoding='utf-8'):
        i, url, t = l.rstrip('\n').split('|', 2)
        m = re.match(r'(.*?) (\d{1,2}\.\d{1,2}\.\d{4}) (.*?) Главная страница', t)
        rating = re.search(r'Rating: ([+-]?\d+)', t)
        body = t.split('Cost in Spirit:')[-1]
        cards = [(n.strip(), int(k)) for n, k in re.findall(r'\d([^\d✕][^✕]*?)✕([1-3])', re.sub(r'^\s*\d+ ', '', body).split(' In Deckbuilder')[0])]
        gm = re.search(r'Artifacts (.+?) GENERAL', t); gen = name('duelyst', gm.group(1)) if gm else ''
        if not m or len(cards) < 8: continue
        tot = sum(k for _, k in cards)
        add('duelyst', name=m.group(1), cards=([(gen, 1)] if gen else []) + cards, group=gfac.get(gen) or gen, keys={gen}, score=int(rating.group(1)) if rating else 0,
            source=f'http://manaspring.ru/decklist/{i}/ (archived {url}); manaspring.ru deck list by {m.group(3)}, {m.group(2)}, rating {rating.group(1) if rating else "none"}; '
                   f'full deck: {tot} cards and the general; copies: {copies(cards)}')

# Faeria: faeria.com hub decks, every deck id read, the most liked first
if os.path.exists(P('fa_hub.txt')):
    fn = {e: n.strip() for e, n in lib.execute("select ext_id, name from entities where game='faeria'")}
    fcol = {e: f for e, f in lib.execute("select ext_id, faction from entities where game='faeria'")}
    for l in open(P('fa_hub.txt'), encoding='utf-8'):
        if not l.strip(): continue
        i, lk, dt, au, nm, cs = l.rstrip('\n').split('|')
        cards = [(fn.get(t.partition('x')[0], t.partition('x')[0]), int(t.partition('x')[2] or 1)) for t in cs.split()]
        tot = sum(k for _, k in cards)
        if tot != 30 or int(lk) < 2: continue
        cols = sorted({fcol.get(t.partition('x')[0]) for t in cs.split()} - {None, 'Neutral', 'neutral'}) or ['neutral only']
        slug = re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', nm.lower())).strip('-')
        add('faeria', name=nm, cards=sorted(cards, key=lambda c: -c[1]), group='+'.join(c.lower() for c in cols), keys={'+'.join(cols)}, score=int(lk),
            source=f'https://www.faeria.com/the-hub/deck/{i}-{slug}; faeria.com hub deck by {au}, {dt}, {lk} likes; full deck: 30 cards; copies: {copies(sorted(cards, key=lambda c: -c[1]))}')

# the small games: the rows the readers found (new_<game>.tsv)
for g in ('monster_train', 'inscryption', 'into_the_breach'):
    f = P(f'new_{g}.tsv')
    if not os.path.exists(f): continue
    for r in csv.DictReader(open(f, encoding='utf-8'), delimiter='\t'):
        cs = [x.strip() for x in r['cards'].split(', ') if x.strip()]
        add(g, name=r['deck'], cards=[(c, 1) for c in cs], group=r['deck'].split(' ')[0], keys={r['deck'].split(' (')[0]}, score=1, source=r['source'])


def avg_cost(g, cards):
    cs = [cost.get((g, n)) for n, k in cards for _ in range(k)]
    cs = [c for c in cs if c is not None]
    return round(sum(cs) / len(cs)) if cs else -1


def pick(g, cs, n):
    """top-rated first, then the faction, average cost and key cards fewest picked so far; never over 80% alike"""
    for c in cs: c['s'] = {x for x, _ in c['cards']}; c['cb'] = avg_cost(g, c['cards'])
    cs = sorted(cs, key=lambda c: -c['score'])
    for r, c in enumerate(cs): c['rank'] = 1 - r / max(1, len(cs))
    pool, kept = [], []
    for c in cs:
        if len(c['s']) < 5 or any(sim(c['s'], e) > 0.8 for e in existing[g]) or any(sim(c['s'], k['s']) > 0.8 for k in pool): continue
        pool.append(c)
    grp, cb, key = collections.Counter(), collections.Counter(), collections.Counter()
    ng = max(1, len({c['group'] for c in pool})); nb = max(1, len({c['cb'] for c in pool}))
    while pool and len(kept) < n:
        m = len(kept) + 1
        best = max(pool, key=lambda c: c['rank'] + 0.6 * (1 - grp[c['group']] * ng / m) + 0.3 * (1 - cb[c['cb']] * nb / m)
                   + 0.4 * (not any(key[k] for k in c['keys'])))
        pool.remove(best); kept.append(best)
        grp[best['group']] += 1; cb[best['cb']] += 1
        for k in best['keys']: key[k] += 1
    return kept, len(pool)


out, unk = [], collections.Counter()
for g in TARGET:
    if not cands[g]: continue
    kept, left = pick(g, cands[g], TARGET[g] - len(existing[g]))
    for c in kept:
        for x in c['s']:
            if norm(x) not in known[g]: unk[g] += 1
        out.append((g, uniq_name(g, c['name']), c['source'], ', '.join(dict.fromkeys(x for x, _ in c['cards']))))
    print(f"{g}: had {len(existing[g])}, candidates {len(cands[g])}, new {len(kept)} (left {left}), total {len(existing[g]) + len(kept)}; "
          f"groups {len({c['group'] for c in kept})}, cost levels {sorted(collections.Counter(c['cb'] for c in kept).items())}; "
          f"names not in the library {unk[g]}")
with open(P('decks_new.tsv'), 'w', encoding='utf-8') as f:
    for r in out: f.write('\t'.join(x.replace('\t', ' ').replace('\n', ' ') for x in r) + '\n')
if '--write' in sys.argv:
    with open('decks.tsv', 'a', encoding='utf-8') as f:
        for r in out: f.write('\t'.join(x.replace('\t', ' ').replace('\n', ' ') for x in r) + '\n')
    print('appended', len(out))
