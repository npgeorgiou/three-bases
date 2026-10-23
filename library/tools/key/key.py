"""Answer key (Step 2 of the tag-fix plan, 13 Oct 2026). It only measures: it is never used to fix library entries and never
edited to agree with the library. Prints counts and sampled lines only.

  key.py defs                         concept definitions -> key/defs.txt (id | name | counts | not)
  key.py sample <game|all>            500 entries per game, seed 1 (all of a game with 500 or fewer), plus the entries named
                                      in tools/audit/<game>_judgments.json -> key/<game>/entries.json
  key.py coverage <game>              concepts on fewer than 5 key entries of the game: candidates found by the concept's typical
                                      words (its wording patterns) among the game's other entries -> key/<game>/cov_entries.json
                                      (read like the key; their tags come from reading, never from the search)
  key.py read <game> [cov|kw]         the reading request: rules + game block -> key/<game>/read.txt, cards -> cards[_cov|_kw]_N.txt
                                      (200 card lines each; kw: only the sample's keyword entries)
  key.py answer <game> [cov|kw]       quote check of key/<game>/answer[_cov|_kw].txt -> key/<game>/key.json (cov, kw: merged in)
  key.py credit [<game>...]            keyword credit for cards that name keywords, written into key/<game>/key.json
  key.py score <db> [game ...]        wrong tags and missed mechanics per 100 key entries (script; see SCORING below)

READING (Kaptain's decision, 21 Oct 2026): one process reads read.txt and the cards files once and writes one line per card to answer.txt;
ADDING_GAMES.md, "Reading cards", says how.

SCORING. Key concepts K (narrowest, as read) and library tags L of an entry, any role. Game-structure tags (method
game_structure: "this game has lanes") and cost-data tags (data_rule) are left out on both sides, since they are not read
from the text. A library tag is right when it is a key concept, an ancestor of one, or a descendant of one; otherwise wrong.
A key concept is missed when no library tag is that concept, a descendant of it, or an ancestor of it below the four
branches and the roots. An older database is scored after its tags are moved through the Step 1 map (concept_tree.py)."""
import json, os, random, re, sqlite3, sys, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS); import games as GM
from concept_tree import TREE, targets, MAP, REMOVED
DB = os.environ.get('TB_LIB', os.path.join(os.path.dirname(TOOLS), 'three-bases-library.sqlite'))
NOT_IN_KEY = {l.strip() for l in open(os.path.join(HERE, 'added_concepts.txt'), encoding='utf-8') if l.strip() and not l.startswith('#')} if os.path.exists(os.path.join(HERE, 'added_concepts.txt')) else set()
GROUPS = {'effect', 'helps_me', 'hurts_enemy', 'drawback', 'game_rules'} | {i for i, d in TREE.items() if not d['parents']}
def gdir(g): d = os.path.join(HERE, g); os.makedirs(d, exist_ok=True); return d
def norm(s): return re.sub(r'\s+', ' ', (s or '').lower().replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')).strip()
KIDS = collections.defaultdict(set)
for i, d in TREE.items():
    for p in d['parents']: KIDS[p].add(i)
def desc(i, s=None):
    s = s if s is not None else set()
    for k in KIDS[i]:
        if k not in s: s.add(k); desc(k, s)
    return s
def anc(i, s=None):
    s = s if s is not None else set()
    for p in TREE[i]['parents']:
        if p not in s: s.add(p); anc(p, s)
    return s
DESC = {i: desc(i) for i in TREE}; ANC = {i: anc(i) for i in TREE}

def db(): return sqlite3.connect(DB)

def defs():
    out = [f"{i} | {d['name']} | {d['counts']} | Not: {d['no']}" for i, d in TREE.items() if d['facet'] != 'problem' and i not in GROUPS]
    open(os.path.join(HERE, 'defs.txt'), 'w').write('\n'.join(out) + '\n'); print('defs:', len(out), 'concepts')

def sample(g):
    c = db()
    ids = sorted(i for i, in c.execute('SELECT id FROM entities WHERE game=?', (g,)))
    pick = ids if len(ids) <= 500 else random.Random(1).sample(ids, 500)
    jf = os.path.join(TOOLS, 'audit', f'{g}_judgments.json')
    live = set(ids)
    extra = [int(i) for i in json.load(open(jf))] if os.path.exists(jf) else []
    sel = list(dict.fromkeys(pick + [i for i in extra if i in live]))
    rows = {i: (n, t) for i, n, t in c.execute('SELECT id, name, text FROM entities WHERE game=?', (g,))}
    ents = [{'id': i, 'name': rows[i][0], 'text': rows[i][1] or ''} for i in sel]
    d = gdir(g); json.dump(ents, open(os.path.join(d, 'entries.json'), 'w'), indent=0)
    for f in glob.glob(os.path.join(d, 'batch_*.txt')): os.remove(f)
    print(g, 'key entries', len(ents), '(random', len(pick), '+ audit', len(sel) - len(pick), ')')

def texts(g):
    return {e['id']: e for e in json.load(open(os.path.join(gdir(g), 'entries.json')))} | \
           {e['id']: e for f in glob.glob(os.path.join(gdir(g), 'cov_entries.json')) for e in json.load(open(f))}

def check_tags(ent, tags):
    ok, bad = [], []
    t = norm(ent['name'] + ' ' + ent['text'])
    for x in tags:
        if not (isinstance(x, list) and len(x) == 2): bad.append((x, 'form')); continue
        k, w = x[0].strip(), norm(x[1])
        if k not in TREE or k in GROUPS or TREE[k]['facet'] == 'problem': bad.append((x, 'concept')); continue
        if not w or w not in t: bad.append((x, 'words')); continue
        ok.append([k, x[1]])
    return ok, bad

def narrow(ks):   # keep the narrowest: drop a concept when a descendant of it is also there
    return {k for k in ks if not (DESC[k] & ks)}

ROLES = {'does', 'grants', 'benefits', 'counters', 'cost'}
RULES = '''# Reading request: {game}
Read this file once, then every card in the cards files, in order. Judge only against the concept definitions at the end of the game block; use
the game's rules, keywords and factions to understand what a card does. Write nothing but the answer lines.

## How to read a card
- Go clause by clause and write each concept the clause expresses, with the exact words that justify it, copied character for
  character from the card's name or text (a short phrase is best). A script rejects any tag whose words are not in the text.
- Use the most specific concept that fits; do not add its parent as well. Check sibling concepts against their "Not:" lines.
- A clause can express several concepts (a trigger, a condition and an effect). Triggers and conditions count too.
- A keyword or ability named on the card counts: tag that keyword's effects, quoting the keyword's name.
- Keyword or glossary entries: tag what the keyword itself does.
- A card with no mechanic (lore, a bare name, plain stats with nothing else) gets an empty answer.
- Do not guess beyond the text. If the text doesn't say it, it isn't there.

## Answer: one line per card line of the cards files, in the same order
`<ids>|<concept>:<role>:<exact words>;<concept>:<role>:<exact words>;...`   (nothing after `|` for a card with no mechanic)
<ids> as given on the card line. Roles: does (the card does it), grants (it gives it to another card), benefits (it is better
when this happens), counters (it answers this), cost (it is part of the cost). The exact words never contain `;` or `|`:
choose a shorter phrase.
'''

def block(g):
    """The game block: everything the library holds about how the game is played, then the concept definitions."""
    c = db(); out = []
    name, fam, ed, struct, notes = c.execute('SELECT name, family, edition, structure, notes FROM games WHERE id=?', (g,)).fetchone()
    out += ['# Game block: %s (%s)' % (name, ed), '', '## Rules', struct or '', notes or '']
    kws = c.execute("SELECT name, text FROM entities WHERE game=? AND category='keyword' ORDER BY name", (g,)).fetchall()
    if kws: out += ['', '## Keywords'] + ['- %s: %s' % (n, t.replace('\n', ' / ')) if (t or '').strip() else '- %s (no definition in the library; see Rules and terms)' % n for n, t in kws]
    fs = c.execute('SELECT name, entity_count FROM factions WHERE game=? ORDER BY name', (g,)).fetchall()
    if fs: out += ['', '## Factions (cards)'] + ['- %s (%s)' % f for f in fs]
    ts = [n for n, in c.execute("SELECT name FROM entities WHERE game=? AND category='tribe' ORDER BY name", (g,))]
    if ts: out += ['', '## Card types and tribes', ', '.join(ts)]
    mf = GM.path(g)   # the game's mechanics file: its rules and terms, and the mechanics its guides name
    if os.path.exists(mf):
        ls = [l.rstrip('\n') for l in GM.block(mf, 'mechanics')]
        ts = [l[len('# term: '):] for l in ls if l.startswith('# term: ')]
        if ts: out += ['', '## Rules and terms'] + ['- ' + t for t in ts]
        ms = [l.split('|')[0].strip() for l in ls if l.strip() and not l.startswith('#')]
        out += ['', "## Mechanics the game's guides name", ', '.join(dict.fromkeys(ms))]
    out += ['', '## Concepts (id | name | what counts | Not: what does not count and where it goes)']
    out += [l.rstrip('\n') for l in open(os.path.join(HERE, 'defs.txt'), encoding='utf-8')]
    return '\n'.join(out)

def card_lines(g, part):
    f = os.path.join(gdir(g), 'cov_entries.json' if part == 'cov' else 'entries.json')
    ents = json.load(open(f))
    if part == 'kw':   # the game's keyword entries of the sample only
        kw = {i for i, in db().execute("SELECT id FROM entities WHERE game=? AND category='keyword'", (g,))}
        ents = [e for e in ents if e['id'] in kw]
    groups = {}
    for e in ents:   # identical cards are sent once
        groups.setdefault((e['name'], e['text']), []).append(str(e['id']))
    return ['%s|%s: %s' % (','.join(ids), n, t.replace('\n', ' / ')) for (n, t), ids in groups.items()]

def undefined(g):
    """Refuse to read while a keyword of the game has no definition: neither its entry's text nor a '# term:' line of the
    mechanics file explains it (the reading would then tag it from guesses). --force reads anyway."""
    mf = GM.path(g)
    terms = {norm(l[len('# term: '):].split(':')[0].split(' (')[0]) for l in GM.block(mf, 'mechanics') if l.startswith('# term: ')} if os.path.exists(mf) else set()
    miss = [n for n, t in db().execute("SELECT name, text FROM entities WHERE game=? AND category='keyword'", (g,)) if not (t or '').strip() and norm(n) not in terms]
    if miss and '--force' not in sys.argv:
        sys.exit(g + ': keywords without a definition (research them, or assume from game knowledge, into the ```mechanics block of tools/games/' + g + '.md): ' + ', '.join(sorted(miss)))

PART = 200   # card lines per cards file: each file and read.txt can be read in one go
def read(g, part=''):
    """read.txt (rules + game block) and cards[_part]_N.txt; one process reads them all once, in order."""
    undefined(g)
    d = gdir(g); lines = card_lines(g, part); sfx = '_' + part if part else ''
    for f in glob.glob(os.path.join(d, 'cards%s_*.txt' % sfx)): os.remove(f)
    open(os.path.join(d, 'read.txt'), 'w', encoding='utf-8').write(RULES.format(game=g) + '\n' + block(g) + '\n')
    n = 0
    for n, b0 in enumerate(range(0, len(lines), PART), 1):
        open(os.path.join(d, 'cards%s_%d.txt' % (sfx, n)), 'w', encoding='utf-8').write('# Cards (<ids>|<name>: <text>)\n' + '\n'.join(lines[b0:b0 + PART]) + '\n')
    print(g, 'card lines', len(lines), 'in', n, 'cards files; read.txt', os.path.getsize(os.path.join(d, 'read.txt')), 'characters')

def answer(g, part=''):
    d = gdir(g); ents = texts(g); want = {i for l in card_lines(g, part) for i in l.split('|')[0].split(',')}
    new = {}; nb = collections.Counter(); ex = []
    for l in open(os.path.join(d, 'answer_%s.txt' % part if part else 'answer.txt'), encoding='utf-8'):
        if '|' not in l: continue
        ids, _, rest = l.rstrip('\n').partition('|')
        for i in ids.split(','):
            i = i.strip(); e = ents.get(int(i)) if i.isdigit() else None
            if not e: nb['unknown card'] += 1; continue
            tags = []
            for x in filter(None, (y.strip() for y in rest.split(';'))):
                k, _, rw = x.partition(':'); r, _, w = rw.partition(':')
                if r.strip() not in ROLES: nb['role'] += 1; ex.append((i, x, 'role')); continue
                ok, bad = check_tags(e, [[k, w]]); tags += ok
                for y, why in bad: nb[why] += 1; ex.append((i, x, why))
            new[i] = {'tags': tags, 'by': 'read'}
    miss = want - set(new)
    kf = os.path.join(d, 'key.json')
    if part: key = json.load(open(kf)); key.update(new); new = key   # cov / kw: merged into the key
    elif os.path.exists(kf) and '--force' not in sys.argv:
        sys.exit(g + ': key.json exists (it may have corrections); --force replaces it')
    json.dump(new, open(kf, 'w'), indent=0)
    print(g, 'answered', len(want) - len(miss), 'of', len(want), 'tags kept', sum(len(v['tags']) for v in new.values()), 'rejected', dict(nb))
    for x in ex[:5]: print('  rejected', x)
    if miss: print('  not answered:', ' '.join(sorted(miss, key=int)[:20]))

def coverage(g):
    d = gdir(g); key = load(g)
    cnt = collections.Counter(k for v in key.values() for k in narrow({k for k, _ in v['tags']}) | {a for k, _ in v['tags'] for a in ANC[k]})
    low = [k for k in TREE if k not in GROUPS and TREE[k]['facet'] != 'problem' and cnt[k] < 5]
    c = db(); pats = collections.defaultdict(list)
    for k, p, gg in c.execute('SELECT concept, pattern, game FROM concept_patterns'):
        if gg in (None, g):
            try: pats[k].append(re.compile(p, re.I))
            except re.error: pass
    inkey = {int(i) for i in key}
    rows = [(i, n, t or '') for i, n, t in c.execute('SELECT id, name, text FROM entities WHERE game=?', (g,)) if i not in inkey]
    rnd = random.Random(1); cand = {}
    for k in low:
        need = 5 - cnt[k]; rx = pats.get(k, [])
        if not rx: continue
        hits = [r for r in rows if any(x.search(r[2].lower()) for x in rx) and r[0] not in cand]
        rnd.shuffle(hits)
        for r in hits[:need]: cand[r[0]] = r   # round 1: as many as the concept still needs; later rounds take more
    ents = [{'id': i, 'name': n, 'text': t} for i, n, t in cand.values()]
    json.dump(ents, open(os.path.join(d, 'cov_entries.json'), 'w'), indent=0)
    print(g, 'concepts under 5:', len(low), 'with patterns to search:', sum(1 for k in low if pats.get(k)), 'candidates', len(ents))

def lib_tags(c, ids, old=False):
    out = collections.defaultdict(set)
    txt = dict(c.execute('SELECT id, text FROM entities'))
    q = 'SELECT entity, concept, method FROM entity_concepts WHERE entity IN (%s)' % ','.join(str(i) for i in ids)
    for e, k, m in c.execute(q):
        if m in ('game_structure', 'data_rule'): continue
        ks = targets(k, txt.get(e)) if (old and (k in MAP or k in REMOVED)) else {k}
        out[e] |= {x for x in ks if x in TREE and x not in NOT_IN_KEY}
    return out

def score(dbpath, games):
    c = sqlite3.connect(dbpath)
    old = not c.execute("SELECT 1 FROM concepts WHERE id='helps_me'").fetchone()
    tot = [0, 0, 0]
    for g in games:
        f = os.path.join(HERE, g, 'key.json')
        if not os.path.exists(f): continue
        key = load(g); ids = [int(i) for i in key]
        live = {i for i, in c.execute('SELECT id FROM entities WHERE game=?', (g,))}
        ids = [i for i in ids if i in live]
        L = lib_tags(c, ids, old)
        wrong = missed = 0
        for i in ids:
            K = narrow({k for k, _ in key[str(i)]['tags']})
            ok = set(K) | {a for k in K for a in ANC[k]} | {d for k in K for d in DESC[k]}
            wrong += sum(1 for l in L[i] if l not in ok and l not in GROUPS)
            for k in K:
                near = {k} | DESC[k] | (ANC[k] - GROUPS)
                if not (L[i] & near): missed += 1
        n = len(ids); tot[0] += n; tot[1] += wrong; tot[2] += missed
        print(f'{g:18} entries {n:4}  wrong/100 {100 * wrong / max(n, 1):6.1f}  missed/100 {100 * missed / max(n, 1):6.1f}')
    print(f"{'all':18} entries {tot[0]:4}  wrong/100 {100 * tot[1] / max(tot[0], 1):6.1f}  missed/100 {100 * tot[2] / max(tot[0], 1):6.1f}")


# --- Keyword credit ----------------------------------------------------------------------------------------------------------
# A card that names a keyword has that keyword's effects, so its key entry carries them ('Skills: Dodge.', 'Taunt'). 'key.py
# credit' adds to each key entry the tags of the keywords the card has: listed for it in the source data (a has_keyword link whose
# evidence names a field or list) or standing where the game prints keywords (the position rule of kw_links.py; the name may stand
# in square brackets: '[LETHAL HITS]'). The tags are the keyword's own from kw_<game>/key.json (or the game's keyword entries),
# quoted with the keyword's name as it appears in the card's text. Keywords the key marked as not real are never credited.
# Decided from the repo database (text and source links), never from a build being measured. The added tags are listed again in
# the entry's 'credited' field and its keywords in 'keywords', so a new credit replaces the old one and the quote checks know them.
KW_FIELD = re.compile(r'field|list|scryfall|sigils|special|traits|warscroll', re.I)
KW_B = r"(?:^|[\n.:;/]\s*|\s-\s*|-{3,}\s*|keywords?:\s*(?:[^.\n]*?,\s*)*)"
KW_ACTION = {'damage', 'destroy', 'draw', 'summon', 'generate_cards', 'disable', 'silence', 'selection', 'transform', 'movement',
             'forced_movement', 'discard', 'copy', 'heal', 'stat_gain', 'stat_loss', 'banish', 'bounce_enemy', 'return_to_hand', 'tutor'}
def kw_valid(text, kname, action):
    t = text or ''; k = r'\[?' + re.escape(kname) + r'\]?'
    if re.search(KW_B + k + r"(?=\s*(?:$|[\n.,:;(/]|\d|\s-))", t, re.I): return True
    if action and re.search(KW_B + k + r"\s+(?:a|an|the|all|each|your|any|one|two|three|\d|it|them|this|that|up to|another|enemy|friendly|random)\b", t, re.I): return True
    return False

def credit(g):
    f = os.path.join(HERE, 'kw_' + g, 'key.json'); kf = os.path.join(HERE, g, 'key.json')
    key = json.load(open(kf))
    for v in key.values():   # take the previous credit out
        v['tags'] = [t for t in v['tags'] if t not in v.pop('credited', [])]; v.pop('keywords', None)
    c = db(); kwids = {i for i, in c.execute("SELECT id FROM entities WHERE game=? AND category='keyword'", (g,))}
    if os.path.exists(f): kwk = {int(i): v['tags'] for i, v in json.load(open(f)).items()}
    else: kwk = {int(i): v['tags'] for i, v in key.items() if int(i) in kwids}   # the keyword entries read with the game's cards
    notk = []
    for r in ('A', 'B'):
        nf = os.path.join(HERE, 'kw_' + g, r, 'notkw.json')
        notk.append({int(x) for x in json.load(open(nf))} if os.path.exists(nf) else set())
    bad = notk[0] & notk[1]
    names = {i: n for i, n in c.execute("SELECT id, name FROM entities WHERE game=? AND category='keyword'", (g,)) if i in kwk and i not in bad and kwk[i]}
    nk = nt = 0
    for i, v in key.items():
        row = c.execute('SELECT text FROM entities WHERE id=?', (int(i),)).fetchone()
        if not row or not names: continue
        text = row[0] or ''
        have = {d for d, ev in c.execute("SELECT dst, evidence FROM entity_links WHERE src=? AND rel='has_keyword'", (int(i),)) if d in names and ev and KW_FIELD.search(ev)}
        for d, n in names.items():
            if d != int(i) and d not in have and kw_valid(text, n, bool({k for k, _ in kwk[d]} & KW_ACTION)): have.add(d)
        if not have: continue
        add = []
        for d in sorted(have):
            m = re.search(re.escape(names[d]), text, re.I); w = m.group(0) if m else names[d]
            for k, _ in kwk[d]:
                if k in TREE and [k, w] not in v['tags'] and [k, w] not in add: add.append([k, w])
        v['keywords'] = sorted(have); v['tags'] += add
        if add: v['credited'] = add
        nk += 1; nt += len(add)
    json.dump(key, open(kf, 'w'), indent=0)
    print(f'{g:18} key entries credited {nk:4}  keyword tags {nt:5}')

def load(g):
    """The game's key, keyword credit included: {id: {'tags': [[concept, words], ...], ...}}."""
    return json.load(open(os.path.join(HERE, g, 'key.json')))

GAMES = ['into_the_breach', 'inscryption', 'faeria', 'duelyst', 'sts1', 'marvel_snap', 'darkest_dungeon', 'sts2',
         'gwent', 'hs_battlegrounds', 'runeterra', 'wh_aos_4th', 'wh_40k_10e', 'shadowverse', 'hearthstone', 'mtg',
         'lorcana', 'stormbound', 'swu', 'tesl', 'monster_train']   # the last five: read with one request each (21 Oct 2026)
if __name__ == '__main__':
    cmd, *a = sys.argv[1:]
    if cmd == 'defs': defs()
    elif cmd == 'sample': [sample(g) for g in (GAMES if a[0] == 'all' else a)]
    elif cmd == 'read': read(a[0], next((x for x in a[1:] if x in ('cov', 'kw')), ''))
    elif cmd == 'answer': answer(a[0], next((x for x in a[1:] if x in ('cov', 'kw')), ''))
    elif cmd == 'coverage': coverage(a[0])
    elif cmd == 'credit': [credit(g) for g in (a or GAMES)]   # run again after 'answer' or a key correction
    elif cmd == 'score': score(a[0], a[1:] or GAMES)
