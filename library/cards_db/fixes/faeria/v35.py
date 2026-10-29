"""All games, 29 Oct 2026 (v35), by rule; safe to run twice.
- A "used a keyword" trigger (event keyword_used) whose object names no keyword: the keyword the card's text names in its
  trigger ("If I'm Tossed", "Whenever you discover a Treasure") is added as a keyword filter on the object, so the trigger
  matches cards that use that keyword (Fugoro, Captain of the Gagana; Keelbreaker; Platewyrm Egg).
  Only when exactly one of the game's keywords appears in a trigger phrase.
- An ability given for the next time something happens "this turn" / "this round" ("The next creature you play this turn
  costs 4 faeria less", "the first creature summoned on it this turn"): the give_ability lasts this_round (Failed
  Experiment, Path to Paradise), when the record has no this_round anywhere.
- "Last Words - ... Summon this in a random space.": the card summons itself again when it dies (Annoying Gnat was read as
  moving when played).
- Faeria "this turn" is the span this_round (BRIEF Game words: Faeria), never this_turn ("this action"); "a creature that
  attacked a god this turn" is state struck_player_this_round, not attacked_this_round (The World's Tear).
- Faeria keyword_action with a keyword no glossary has (readers' stand-ins for missing values): Empty / Refill a faeria
  well = empty_resource / refill_resource; Destroy a well = kill on it; End the turn = end_turn; Extra turn = extra_turn;
  Refresh power wheel (Ignusi Ritualist) = refresh on the turn's choice (kind effect; act refresh from Duelyst).
- A summoned or transformed-into token's keywords in the text ("a 5/2 Flying Demon Wing", "a 6/3 Oblivion Rider with Charge
  3", "a 4/4 Flying Charge 2 Dune Drake"): give_keyword on it for each, when the record lacks it (Demon Wrangler).
- Board forms, one per meaning (29 Oct 2026, the positional pass):
  * "moves onto enemy land" / "moves into a forest" (event moves_onto): the moving unit is the object (like moves, N16) and
    the space is its position filter `same_space of {the space}`; never the space as object with the unit as actor.
  * "in its place" / "where this died": summon to `{"kind": "position", "with": [same_space of {"pick": "it"}]}`.
  * "Can be summoned adjacent to friendly creatures": can summoned to `{"kind": "position", "with": [bordering of
    {"kind": "unit", "side": "mine"}]}` (a space, like Wind Gate's), never "to" the units.
  * "on or adjacent to that space": one target, position in [same_space, bordering] of the space (Meteor's form), not two
    effects (Firestorm).
  * "destroy it" on the card itself is kill (self-destruct), not sacrifice (Doomgate).
  * "You can summon creatures on spaces adjacent to this structure": the permission is on my creatures, not on the
    structure (Wind Gate); "(you may summon it on an ocean tile)": the token goes to ocean or land (Gabrian Noble).
  * Keyword entries: "in a straight line" (Charge, Dash, Ranged Attack) is position straight_line of the unit; Ranged
    shoots the nearest enemy in that line (line of sight: pick nearest); Jump's "up
    to 2 spaces" is distance le 2 (attr distance); those readers' unsure flags go."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
TRIG = re.compile(r"\b(?:if i'm|when i'm|whenever you|when you|the first time you|each time you)\s+(\w+)", re.I)


STAND_IN = {'Empty': 'empty_resource', 'Refill': 'refill_resource', 'Destroy': 'kill', 'End the turn': 'end_turn',
            'Extra turn': 'extra_turn', 'Refresh power wheel': 'refresh'}


def board_forms(r, t):
    def walk(o):
        if isinstance(o, dict):
            for k in ('when', 'trigger'):
                ev = o.get(k)
                if isinstance(ev, dict) and ev.get('event') == 'moves_onto' and (ev.get('object') or {}).get('kind') == 'position':
                    space = ev.pop('object'); mover = ev.pop('actor', None) or {}
                    mover.setdefault('with', []).append({'attr': 'position', 'op': 'is', 'val': 'same_space', 'of': space})
                    ev['object'] = mover
            do = o.get('do') if isinstance(o.get('do'), list) else []
            for j, e in enumerate(do):
                to = e.get('to') if isinstance(e.get('to'), dict) else None
                if e.get('act') in ('summon', 'revive', 'copy') and to and to.get('kind') == 'position' and to.get('pick') == 'it':
                    for f in to.get('with', []):
                        if f.get('attr') == 'position' and f.get('val') == 'same_space' and 'of' not in f:
                            f['of'] = {'pick': 'it'}; to.pop('pick')
                if e.get('act') in ('can', 'cant') and (e.get('params') or {}).get('event') in ('summoned', 'played') and to and to.get('kind') == 'unit' \
                        and any(f.get('val') == 'bordering' for f in to.get('with', [])):
                    of = {k: v for k, v in to.items() if k in ('kind', 'side')}
                    keep = [f for f in to.get('with', []) if f.get('attr') != 'position']  # "next to friendly Yaks": the Yak filter stays
                    if keep: of['with'] = keep
                    e['to'] = {'kind': 'position', 'with': [{'attr': 'position', 'op': 'is', 'val': 'bordering', 'of': of}]}
                if e.get('act') == 'sacrifice' and (e.get('on') or {}).get('pick') == 'self' and re.search(r'\bdestroy (?:it|this)\b', t, re.I) \
                        and not re.search(r'\bsacrifice (?:this|it|a card bearing)', t, re.I):
                    e['act'] = 'kill'
            if re.search(r'You can summon creatures on spaces adjacent to this', t):
                for e in do:
                    if e.get('act') == 'can' and (e.get('on') or {}).get('pick') == 'self' and (e.get('params') or {}).get('event') == 'summoned':
                        e['on'] = {'kind': 'unit', 'side': 'mine', 'pick': 'all'}
            if re.search(r'you may summon it on an ocean (?:tile|space)', t):
                for e in do:
                    if e.get('act') == 'summon' and 'to' not in e:
                        e['to'] = {'kind': 'position', 'with': [{'attr': 'terrain', 'op': 'in', 'vals': ['ocean', 'land']}]}
            # "on or adjacent to that space": same_space of X, then the same act on bordering of it -> one target
            for j in range(len(do) - 1):
                a, b = do[j], do[j + 1]
                fa = [f for f in (a.get('on') or {}).get('with', []) if f.get('attr') == 'position' and f.get('val') == 'same_space' and 'of' in f]
                fb = [f for f in (b.get('on') or {}).get('with', []) if f.get('attr') == 'position' and f.get('val') == 'bordering' and (f.get('of') or {}).get('pick') == 'it']
                if fa and fb and a.get('act') == b.get('act') and a.get('params') == b.get('params') and \
                        {k: v for k, v in a['on'].items() if k != 'with'} == {k: v for k, v in b['on'].items() if k != 'with'}:
                    fa[0].pop('val'); fa[0]['op'] = 'in'; fa[0]['vals'] = ['same_space', 'bordering']
                    do.pop(j + 1); break
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(r)


WORD = {'two': 2, 'three': 3, 'four': 4}
LINE = {'attr': 'position', 'op': 'is', 'val': 'straight_line', 'of': {'pick': 'self'}}


def keyword_forms(r, name, t):
    """the keyword entries' board words, now that values exist for them"""
    for ab in r.get('abilities', []):
        for e in ab.get('do', []):
            to = e.get('to') if isinstance(e.get('to'), dict) else None
            if re.search(r'straight line', t) and to is not None and LINE not in to.get('with', []) and \
                    (e.get('act') in ('move', 'strike') or (e.get('act') == 'can' and (e.get('params') or {}).get('event') == 'moves')):
                to.setdefault('with', []).append(dict(LINE))
            if re.search(r'line of sight', t) and e.get('act') == 'strike' and to is not None and to.get('pick') != 'nearest':
                to['pick'] = 'nearest'; to['kind'] = 'anything'  # Ranged: the first enemy in the line (a unit in between blocks it)
            m = re.search(r'up to (\d+|two|three|four) (?:tiles|spaces)', t)
            if m and e.get('act') == 'can' and (e.get('params') or {}).get('event') == 'moves' and (e.get('params') or {}).get('amount'):
                e['params'].pop('amount')
                e['to'] = {'kind': 'position', 'with': [{'attr': 'distance', 'op': 'le', 'n': int(WORD.get(m.group(1), m.group(1))), 'of': {'pick': 'self'}}]}
    if r.get('unsure'):
        if re.search(r'straight line', t): r['unsure'] = [u for u in r['unsure'] if u != 'position']
        if re.search(r'up to (?:\d+|two|three|four) (?:tiles|spaces)', t): r['unsure'] = [u for u in r['unsure'] if u != 'params']
        if not r['unsure']: r.pop('unsure')


def has_kw(t):
    return any(f.get('attr') == 'keyword' for f in (t or {}).get('with', []))


for game in ('runeterra', 'stormbound', 'monster_train', 'faeria'):
    text = {i: ' '.join((t or '').split()) for i, t in lib.execute('select id, text from entities where game=?', (game,))}
    kws = [n for (n,) in lib.execute("select name from entities where game=? and category='keyword'", (game,))]
    for p in sorted(glob.glob(os.path.join(HERE, 'read', game, 'batch_*.jsonl')) + glob.glob(os.path.join(HERE, 'read', game, 'keywords.jsonl'))):
        recs = [json.loads(l) for l in open(p) if l.strip()]; n = 0
        for r in recs:
            words = [w.lower() for w in TRIG.findall(text.get(r.get('id'), ''))]
            hit = {k for k in kws for w in words if re.match(re.escape(k.lower().rstrip('es')), w)}
            if len(hit) != 1: continue
            for ab in r.get('abilities', []):
                ev = ab.get('when') or {}
                if ev.get('event') == 'keyword_used' and not has_kw(ev.get('object')):
                    ev.setdefault('object', {}).setdefault('with', []).append({'attr': 'keyword', 'op': 'is', 'ref': hit.pop()}); n += 1
                    break
        for r in recs:
            t = text.get(r.get('id'), '')
            if re.search(r'\bthis (?:turn|round)\b', t, re.I) and 'this_round' not in json.dumps(r):
                for ab in r.get('abilities', []):
                    for e in ab.get('do', []):
                        if e.get('act') == 'give_ability' and 'lasts' not in e: e['lasts'] = 'this_round'; n += 1
            if re.search(r'Last Words - [^.]*\. Summon this in a random space', t):
                name = lib.execute('select name from entities where id=?', (r['id'],)).fetchone()[0].strip()
                abs_ = r.get('abilities', [])
                lw = [ab for ab in abs_ if (ab.get('when') or {}).get('event') == 'dies' and ((ab['when'].get('object') or {}).get('pick') == 'self')]
                if lw and not any(e.get('act') == 'summon' for e in lw[0]['do']):
                    lw[0]['do'].append({'act': 'summon', 'card': name, 'to': {'kind': 'position', 'pick': 'random'}, 'link': 'then'})
                    r['abilities'] = [ab for ab in abs_ if not ((ab.get('when') or {}).get('event') == 'played' and ab.get('do') and
                                      all(e.get('act') == 'move' and (e.get('to') or {}).get('pick') == 'random' for e in ab['do']))]
                    n += 1
        if game == 'faeria':
            for r in recs:
                t = text.get(r.get('id'), ''); before = json.dumps(r)
                def walk(o):
                    if isinstance(o, dict):
                        if o.get('span') == 'this_turn': o['span'] = 'this_round'
                        if o.get('attr') == 'state' and o.get('val') == 'attacked_this_round' and re.search(r'attacked a god', t): o['val'] = 'struck_player_this_round'
                        for v in o.values(): walk(v)
                    elif isinstance(o, list):
                        for v in o: walk(v)
                walk(r)
                for ab in r.get('abilities', []):
                    for e in ab.get('do', []):
                        if e.get('act') != 'keyword_action': continue
                        k = e.get('keyword')
                        if k in STAND_IN:
                            e['act'] = STAND_IN[k]; del e['keyword']; e.pop('lasts', None)
                            if k == 'Refresh power wheel': e['on'] = {'kind': 'effect'}
                            if 'act' in (r.get('unsure') or []): r['unsure'] = [u for u in r['unsure'] if u != 'act'] or None
                if r.get('unsure') is None: r.pop('unsure', None)
                for ab in r.get('abilities', []):
                    do = ab.get('do', [])
                    for j, e in enumerate(list(do)):
                        if e.get('act') not in ('summon', 'transform') or not e.get('card'): continue
                        tok = re.escape(e['card'])
                        m = re.search(r'\d+/\d+ ((?:[A-Z][a-z]+(?: [A-Z][a-z]+)?(?: \d+)?,? )*)' + tok + r's?(?: with ((?:[A-Z][a-z]+(?: [A-Z][a-z]+)?(?: \d+)?(?:,? and |, )?)+))?', t)
                        if not m: continue
                        words = ' '.join(x for x in m.groups() if x)
                        have = {x.get('keyword') for x in do if x.get('act') == 'give_keyword' and (x.get('on') or {}).get('pick') == 'it'}
                        add = []
                        for k in sorted(kws, key=len, reverse=True):
                            mm = re.search(r'\b' + re.escape(k) + r'(?: (\d+))?\b', words)
                            if mm and k not in have and k not in ('Wild', 'Transform', 'Fight', 'Teleport', 'Discover', 'Swallow'):
                                g = {'act': 'give_keyword', 'on': {'pick': 'it'}, 'keyword': k, 'lasts': e.get('lasts', 'permanent'), 'link': 'and'}
                                if mm.group(1): g['params'] = {'amount': int(mm.group(1))}
                                add.append(g); words = words.replace(mm.group(0), '')
                        for g in reversed(add): do.insert(j + 1, g)
                if json.dumps(r) != before: n += 1
        for r in recs:
            before = json.dumps(r); t = text.get(r.get('id'), '')
            board_forms(r, t)
            if p.endswith('keywords.jsonl') and game == 'faeria':
                keyword_forms(r, None, t)
            if json.dumps(r) != before: n += 1
        if n:
            open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs)); print(game, os.path.basename(p), n)
