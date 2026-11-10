"""Turns the fetched pick files into new decks.tsv rows (decks_new.tsv) and a report of decks with cards the library does
not know (unknown.tsv). Run from library/cards_db/: python3 checks/decks300/build.py"""
import sys, os, re, csv, pickle, sqlite3, collections, unicodedata
sys.path.insert(0, '.')
import source
from lor_deckcodes import LoRDeck
D = os.path.dirname(os.path.abspath(__file__))
P = lambda f: os.path.join(D, f)
lib = source.lib()
db = sqlite3.connect('cards.sqlite')
known = {g: {r[0] for r in db.execute('select name from card where game=?', (g,))} for g in
         ('gwent', 'faeria', 'runeterra', 'stormbound', 'duelyst')}
code = lambda g: {e: n.strip() for e, n in lib.execute('select ext_id,name from entities where game=?', (g,))}
existing = collections.defaultdict(list)
names_used = collections.defaultdict(set)
for l in open('decks.tsv', encoding='utf-8'):
    p = l.rstrip('\n').split('\t')
    if p[0] == 'game': continue
    existing[p[0]].append(set(p[3].split(', ')))
    names_used[p[0]].add(p[1])
TARGET = {'faeria': 221, 'runeterra': 200, 'gwent': 270, 'stormbound': 999, 'duelyst': 999}
GAMES = ('stormbound', 'duelyst', 'faeria', 'runeterra', 'gwent')

def sim(a, b): return len(a & b) / max(len(a), len(b))
def clean(s):
    s = ''.join(ch for ch in s if unicodedata.category(ch)[0] in 'LNPZ' or ch in "'&+-")
    return re.sub(r'\s+', ' ', s).strip(' -|')
def copies(cards): return ', '.join(f'{k} {n}' for n, k in cards)
def uniq_name(g, name):
    n, i = name, 2
    while n in names_used[g]: n = f'{name} ({i})'; i += 1
    names_used[g].add(n); return n

cands = collections.defaultdict(list)   # game -> [dict(name, source, cards=[(name,count)], group)]
# Stormbound: Stormbound-Kitty featured decks, hall of fame, guides
sb = {k.upper() if re.fullmatch(r'[nswfi]\d+', k) else k: v for k, v in code('stormbound').items()}
def sb_cards(i):
    if re.match(r'^\dx', i): toks = re.findall(r'[nswfi]\d+', i[2:])
    else: toks = [t[1:] for t in re.findall(r'\d[nswfi]\d+?(?=\d[nswfi]|$)', i)]
    return [(sb.get(t.upper(), '?' + t.upper()), 1) for t in toks]
FAC = {'n': 'neutral', 's': 'swarm', 'w': 'winter', 'f': 'shadowfen', 'i': 'ironclad'}
def sb_fac(i):
    f = sorted({FAC[c] for c in re.findall(r'(?<![0-9a-z])?([swfi])\d', i[2:] if re.match(r'^\dx', i) else i)})
    return '+'.join(f) or 'neutral'
for l in open(P('sb_feat.txt'), encoding='utf-8'):
    i, n, dt, au, tags, nerf = l.rstrip('\n').split('|')
    t = [x.lower().replace('_', ' ') for x in tags.split(',') if x]
    cands['stormbound'].append(dict(name=clean(n), cards=sb_cards(i), group=sb_fac(i),
        arch=next((x for x in t if x in ('rush', 'control', 'midrange')), 'not labelled'),
        source=f'https://stormbound-kitty.com/deck/{i}/detail; Stormbound-Kitty featured deck by {au}, {dt}; tags: {", ".join(t)}'
               + ('; marked nerfed' if nerf else '') + '; 12 cards, one copy each'))
for l in open(P('sb_tourn.txt'), encoding='utf-8'):
    i, n, dt, tn, hosts = l.rstrip('\n').split('|')
    cands['stormbound'].append(dict(name=clean(f'{tn.strip()} {dt} {n or "deck"}'), cards=sb_cards(i), group=sb_fac(i), arch='not labelled',
        source=f'https://stormbound-kitty.com/deck/{i}/detail; Stormbound-Kitty hall of fame: {tn.strip()} ({dt}), hosted by {hosts}; 12 cards, one copy each'))
for l in open(P('sb_guides.txt'), encoding='utf-8'):
    i, u = l.rstrip('\n').split('|')
    cands['stormbound'].append(dict(name=clean(f'{u.split("/")[-1].replace("-", " ").title()} guide deck {i[:12]}'), cards=sb_cards(i), group=sb_fac(i), arch='not labelled',
        source=f'https://stormbound-kitty.com/deck/{i}/detail; deck in the Stormbound-Kitty guide https://stormbound-kitty.com{u}; 12 cards, one copy each'))
# Duelyst: duelspot.com legacy decks with an import code
dn = {r['card_id']: r['name'].strip() for r in csv.DictReader(open('../sources/duelyst_cards.psv', encoding='utf-8'), delimiter='|')}
GENERALS = sorted({r['name'].strip() for r in csv.DictReader(open('../sources/duelyst_cards.psv', encoding='utf-8'), delimiter='|') if r['general']}, key=len, reverse=True)
dfac = {r['card_id']: r['faction'] for r in csv.DictReader(open('../sources/duelyst_cards.psv', encoding='utf-8'), delimiter='|')}
for l in open(P('du_pick.txt'), encoding='utf-8'):
    slug, title, cat, arch, patch, au, dt, cs, ex = l.rstrip('\n').split('|')
    if ex: continue
    cards = [(dn.get(t.partition('x')[0], '?' + t.partition('x')[0]), int(t.partition('x')[2] or 1)) for t in cs.split()]
    gen = next((g for g in GENERALS if title.endswith(' ' + g)), ''); nm = title[:-len(gen)].strip() if gen else title
    cands['duelyst'].append(dict(name=clean(nm), cards=cards, group=dfac.get(cs.split()[0].partition('x')[0], '?'),
        arch=arch.lower() or 'not labelled',
        source=f'https://duelspot.com/deck/{slug}/; Duelspot legacy deck by {au}, {dt}, patch {patch}' + (f', {cat}' if cat else '')
               + (f', archetype {arch}' if arch else '') + f'; decoded from the page\'s import code; full deck: 40 cards; copies: {copies(cards)}'))
# Faeria and Runeterra: the planned picks (plan2.py, plan3.py), then the rest of the candidates as reserve
plan = pickle.load(open(P('plan.pkl'), 'rb'))
fn = code('faeria')
FCOL = {'B': 'blue', 'G': 'green', 'R': 'red', 'Y': 'yellow', 'N': 'neutral only'}
def fslug(n): return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', n.lower())).strip('-')
order = [d['i'] for d in plan['faeria_plan']] + [d['i'] for d in plan['faeria'][2] if d not in plan['faeria_plan']]
rows = {l.split('|')[0]: l.rstrip('\n').split('|') for l in open(P('faeria_pick.txt'), encoding='utf-8')}
colmap = {d['i']: d['col'] for d in plan['faeria'][2]}
archmap = {d['i']: d['ar'] for d in plan['faeria'][2]}
for i in order:
    _, n, a, dt, lk, cs = rows[i]
    cards = [(fn.get(t.partition('x')[0], '?' + t.partition('x')[0]), int(t.partition('x')[2] or 1)) for t in cs.split()]
    cards.sort(key=lambda c: -c[1])
    cands['faeria'].append(dict(name=clean(n), cards=cards, group='+'.join(FCOL[x] for x in colmap[i]), arch=archmap[i],
        source=f'https://www.faeria.com/the-hub/deck/{i}-{fslug(n)}; faeria.com hub deck by {a}, {dt}, {lk} likes; full deck: 30 cards; copies: {copies(cards)}'))
rn = code('runeterra')
order = plan['runeterra_plan'] + [d for d in plan['runeterra'][2] if d not in plan['runeterra_plan']]
hero = {e for e, in lib.execute("select ext_id from entities where game='runeterra' and category='hero'")}
for d in order:
    cards = [(rn.get(c, '?' + c), k) for c, k in d['cards']]
    champs = [rn[c] for c, _ in d['cards'] if c in hero]
    nm = ' '.join(dict.fromkeys(champs)) or d['col'].replace('+', ' ') + ' deck'
    cands['runeterra'].append(dict(name=nm, cards=cards, group=d['col'], arch='not labelled',
        source=f'https://masteringruneterra.com/{d["slug"]}/; article of {d["dt"]}; decoded from the article\'s deck code {d["code"]}; full deck: 40 cards; copies: {copies(cards)}'))
# Gwent: playgwent.com deck guides
GD = open(P('gw_dict.txt'), encoding='utf-8').read().rstrip('\n').split('|')
gf = {}
for l in [x for f in ('gw_rows.txt', 'gw_rows_b.txt') for x in open(P(f), encoding='utf-8')]:
    i, n, dt, v, au, ld, st, cs = l.rstrip('\n').split('|')
    cards = [(GD[int(t.partition('x')[0])].strip(), int(t.partition('x')[2] or 1)) for t in cs.split()]
    one = sum(1 for _, k in cards if k == 1); two = sum(1 for _, k in cards if k == 2); tot = sum(k for _, k in cards)
    lead = [(GD[int(ld)].strip(), 1)] + ([(GD[int(st)].strip(), 1)] if GD[int(st)] else [])
    cands['gwent'].append(dict(name=clean(n) or f'Gwent guide {i}', cards=lead + cards, group=None, arch=None, gid=i,
        source=f'https://www.playgwent.com/en/decks/guides/{i} (deck guide, {v} votes, {dt}, by {au}); full deck: {tot} cards, {one} with one copy and {two} with two, plus leader ability and stratagem (deck size 25 or more)'))
# each guide's faction, from the playgwent guide list
if os.path.exists(P('gw_faction.txt')):
    gf = dict(l.rstrip('\n').split('|') for l in open(P('gw_faction.txt'), encoding='utf-8'))
for c in cands['gwent']: c['group'] = gf.get(c['gid'], '?')

AR = [('rush', r'\b(rush|aggro|face|burn|swarm|tempo|weenie|blitz|dash|fast)\b'), ('control', r'\b(control|mill|lock)\b'),
      ('combo', r'\b(combo|otk|wombo)\b'), ('ramp', r'\b(ramp)\b'), ('midrange', r'\b(mid-?range|mid|value)\b')]
def arch(n):
    for a, r in AR:
        if re.search(r, n.lower()): return a
    return 'not labelled'
out, unk, stat = [], [], {}
for g in GAMES:
    kept = []; quota = collections.Counter(); per = None
    if g == 'gwent': per = TARGET[g] // 6
    for c in cands[g]:
        if c['arch'] is None: c['arch'] = arch(c['name'])
        s = {n for n, _ in c['cards']}
        miss = sorted(n for n in s if n not in known[g])
        if len({n for n, _ in c['cards']}) < 8: continue  # not a full deck (a guide's partial list)
        if any(sim(s, e) > 0.8 for e in existing[g]) or any(sim(s, k['s']) > 0.8 for k in kept): continue
        if miss:
            unk.append((g, c['name'], c['source'].split(';')[0].split(' (')[0], ', '.join(miss))); continue
        if len(kept) >= TARGET[g] or (per and quota[c['group']] >= per): continue
        c['s'] = s; kept.append(c); quota[c['group']] += 1
    for c in kept:
        out.append((g, uniq_name(g, c['name']), c['source'], ', '.join(dict.fromkeys(n for n, _ in c['cards']))))
    stat[g] = (len(existing[g]), len(kept), collections.Counter(c['group'] for c in kept), collections.Counter(c['arch'] for c in kept))
with open(P('decks_new.tsv'), 'w', encoding='utf-8') as f:
    for r in out: f.write('\t'.join(r) + '\n')
with open(P('unknown.tsv'), 'w', encoding='utf-8') as f:
    f.write('game\tdeck\tsource\tcards the library does not know\n')
    for r in unk: f.write('\t'.join(r) + '\n')
for g, (n0, n1, grp, ar) in stat.items():
    print(g, 'now', n0, 'new', n1, 'total', n0 + n1, '| unknown-card decks', sum(1 for u in unk if u[0] == g))
    print('  groups', dict(grp.most_common())); print('  arch', dict(ar.most_common()))
