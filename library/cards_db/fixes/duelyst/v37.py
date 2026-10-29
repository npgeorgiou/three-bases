"""Duelyst, 29 Oct 2026 (v37), by rule; safe to run twice.
- A card whose text is a Sentinel ("Sentinel: This transforms into a powerful minion if its hidden condition is met.", the
  face the opponent sees) has the keyword Sentinel: an ability giving itself Sentinel, permanent, when its record names no
  Sentinel (the three Watchful Sentinels had empty records).
- "Your Bloodbound Spell" is the keyword Bloodbound Spell, never a type of that name (types drop names ending in Spell).
- A keyword of another game used by a Duelyst record (Countdown) is dropped from the effect (normalize N6 does it for names;
  here for give_keyword of a keyword the game lacks).
- A trigger that only holds "this turn" ("Whenever a friendly minion dies this turn, draw a card", "If it dies this turn,
  ...", "Other minions you summon this turn gain +1/+1") is an ability the card gives its player for this turn: the same
  form as Runeterra's "the next time ... this round" (give_ability on the player, lasts this_round), inside the card's own
  trigger (played, or its Opening Gambit / Bloodbound Spell ability). A transform "this turn" lasts this_round.
- Written by Claude (one card each, the text's words): Scion of the Void deals double damage when it counterattacks
  (increase_effect times 2 when it is attacked, not double_strike); Sun Elemental's "two random friendly minions" are pick
  random; Eight Gates is unsure ("spells that deal damage"); Valknu's Seal's Egg hatches into a copy of your General (copy of the player after the summon).
- New values (v37): "reactivate" = act ready (was can attacks this_round); "non-token" = state not token; "nearest" /
  "closest" = pick nearest (was chosen); a faction named ("Songhai spell", "Vetruvian artifacts", "Magmar minion",
  "neutral minion") = filter region on what is created, summoned or equipped; "becomes your General" / "becomes their new
  General" = become_leader (was transform to the player). The unsure marks these needs set are removed."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
text = {i: t or '' for i, t in lib.execute("select id, text from entities where game='duelyst'")}
kws = {n for (n,) in lib.execute("select name from entities where game='duelyst' and category='keyword'")}


def walk(x, f):
    if isinstance(x, dict):
        f(x)
        for v in list(x.values()): walk(v, f)
    elif isinstance(x, list):
        for v in x: walk(v, f)


def bbs_type(d):
    for w in d.get('with', []) if isinstance(d.get('with'), list) else []:
        if w.get('attr') == 'type' and w.get('ref') == 'Bloodbound Spell': w['attr'] = 'keyword'


WINDOW = re.compile(r"\b(?:whenever|if|after|when|other minions you summon|the next)\b[^.]*\bthis turn\b", re.I)


def own_trigger(a):
    w = a.get('when') or {}
    return w.get('event') == 'played' and ((w.get('object') or {}).get('pick') == 'self' or 'Bloodbound Spell' in json.dumps(w))


def this_turn(r, t):
    abs_ = r.get('abilities', [])
    if re.search(r"\bis [A-Z][\w' ]+ this turn\b", t):
        for a in abs_:
            for e in a.get('do', []):
                if e.get('act') == 'transform' and 'lasts' not in e: e['lasts'] = 'this_round'
    if not WINDOW.search(t) or 'this_round' in json.dumps(r): return
    host = next((a for a in abs_ if own_trigger(a)), None)
    delayed = [a for a in abs_ if a is not host and (a.get('when') or {}).get('event') not in ('always', None)]
    if host is None and len(delayed) == 1:
        host = {'when': {'event': 'played', 'object': {'pick': 'self'}}, 'do': []}; abs_.insert(0, host)
    if host is None: return
    if not delayed and len(abs_) == 1 and host.get('limit') == 'next_time':  # the window is the host itself (Flash Reincarnation)
        inner = dict(host); delayed = [inner]; host = {'when': {'event': 'played', 'object': {'pick': 'self'}}, 'do': []}
        abs_[:] = [host]
    for a in delayed:
        if a in abs_: abs_.remove(a)
        e = {'act': 'give_ability', 'on': {'kind': 'player', 'side': 'mine'}, 'ability': a, 'lasts': 'this_round'}
        if host['do']: e['link'] = 'and'
        host['do'].append(e)


SOBORO = next(iter(lib.execute("select id from entities where game='duelyst' and name='Soboro'").fetchone()))
EIGHT_GATES = next(iter(lib.execute("select id from entities where game='duelyst' and name='Eight Gates'").fetchone()))


FACTION = {'lyonar': 'Lyonar Kingdoms', 'songhai': 'Songhai Empire', 'vetruvian': 'Vetruvian Imperium', 'abyssian': 'Abyssian Host',
           'magmar': 'Magmar Aspects', 'vanar': 'Vanar Kindred', 'neutral': 'Neutral'}
FACTION_RE = re.compile(r"\b(lyonar|songhai|vetruvian|abyssian|magmar|vanar|neutral)\s+(?:\w+\s+)?(spells?|minions?|artifacts?|cards?)\b", re.I)
RESOLVED = {'act', 'state', 'pick', 'with', 'region', 'limit', 'lasts', 'when'}


def new_values(r, t):
    fixed = set()
    def each(f):
        for a in r.get('abilities', []):
            for e in a.get('do', []):
                f(e)
                if isinstance(e.get('ability'), dict):
                    for e2 in e['ability'].get('do', []): f(e2)
    if re.search(r'\breactivate', t, re.I):
        def ready(e):
            if e.get('act') == 'can' and (e.get('params') or {}).get('event') == 'attacks' and e.get('lasts') == 'this_round':
                e['act'] = 'ready'; e.pop('params', None); e.pop('lasts', None); fixed.add('act')
        each(ready)
    if re.search(r'\bnon-token\b', t, re.I):
        def token(e):
            o = e.get('on') or {}
            if e.get('act') in ('summon', 'revive') and o.get('zone') == 'discard' and 'token' not in json.dumps(o):
                o.setdefault('with', []).append({'attr': 'state', 'op': 'not', 'val': 'token'}); fixed.add('state'); fixed.add('with')
        each(token)
    if re.search(r'\b(?:nearest|closest)\b', t, re.I):
        def near(e):
            for k in ('on', 'to'):
                o = e.get(k) or {}
                if o.get('side') == 'enemy' and o.get('pick') in ('chosen', None) and e.get('act') in ('silence', 'damage', 'start_attack', 'move', 'kill'):
                    o['pick'] = 'nearest'; fixed.add('pick')
        each(near)
    m = FACTION_RE.search(t)
    if m and '"attr": "region"' not in json.dumps(r):
        reg = FACTION[m.group(1).lower()]
        def region(e):
            if e.get('act') in ('create', 'summon', 'attach', 'transform'):
                o = e.get('to') if e.get('act') in ('attach', 'transform') and isinstance(e.get('to'), dict) else e.get('on')
                if isinstance(o, dict) and o.get('pick') == 'random':
                    o.setdefault('with', []).append({'attr': 'region', 'op': 'is', 'val': reg}); fixed.add('with'); fixed.add('region')
        each(region)
    if re.search(r'\bbecomes? (?:your|their)(?: new)? General\b', t, re.I):
        def lead(e):
            if e.get('act') == 'transform' and (e.get('to') or {}).get('kind') == 'player':
                e['act'] = 'become_leader'; e.pop('to', None); fixed.add('act')
        each(lead)
    if 'this_round' in json.dumps(r) and re.search(r'this turn', t): fixed |= {'limit', 'lasts'}
    if 'increase_effect' in json.dumps(r) and re.search(r'counter ?attack', t, re.I): fixed.add('when')
    if fixed and r.get('unsure'):
        r['unsure'] = [u for u in r['unsure'] if u not in (fixed & RESOLVED)]
        if not r['unsure']: r.pop('unsure')


def direct(r):
    i = r.get('id')
    if i == 5000653:  # Scion of the Void
        r['abilities'] = [a for a in r['abilities'] if 'double_strike' not in json.dumps(a)]
        if 'increase_effect' not in json.dumps(r):
            r['abilities'].append({'when': {'event': 'attacks', 'object': {'pick': 'self'}}, 'do': [{'act': 'increase_effect',
                                   'on': {'pick': 'self'}, 'params': {'times': 2}, 'lasts': 'this_round'}]})
    if i == 5000803:  # Sun Elemental
        for a in r['abilities']:
            for e in a.get('do', []):
                if e.get('on', {}).get('pick') == 'chosen': e['on']['pick'] = 'random'
    if i == SOBORO:  # "Whenever this damages a neutral minion, destroy that minion"
        for a in r['abilities']:
            o = (a.get('when') or {}).get('object') or {}
            if o.get('kind') == 'unit' and '"region"' not in json.dumps(o):
                o.setdefault('with', []).append({'attr': 'region', 'op': 'is', 'val': 'Neutral'})
        if 'unsure' in r:
            r['unsure'] = [u for u in r['unsure'] if u != 'with']
            if not r['unsure']: r.pop('unsure')
    if i == EIGHT_GATES and 'with' not in r.get('unsure', []):  # "spells that deal damage": no value says it
        r.setdefault('unsure', []).append('with')
    if i == 5000038 and '"copy"' not in json.dumps(r):  # Valknu's Seal
        r['abilities'][0]['do'].append({'act': 'copy', 'on': {'kind': 'player', 'side': 'mine'}, 'zone': 'board', 'link': 'then'})


for p in sorted(glob.glob(os.path.join(HERE, 'read', 'duelyst', '*.jsonl'))) + sorted(glob.glob(os.path.join(HERE, 'second', 'duelyst', '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]; n = 0
    for r in recs:
        before = json.dumps(r, sort_keys=True)
        walk(r, bbs_type)
        for ab in r.get('abilities', []):
            do = [e for e in ab.get('do', []) if not (e.get('act') == 'give_keyword' and e.get('keyword') and e['keyword'] not in kws)]
            if len(do) != len(ab.get('do', [])) and do:
                do[0].pop('link', None); ab['do'] = do
        t = re.sub(r'^Keywords:[^.]*\.\s*', '', text.get(r.get('id'), ''))
        if t.startswith('Sentinel:') and '"Sentinel"' not in json.dumps(r):
            r.setdefault('abilities', []).append({'when': {'event': 'always'}, 'do': [{'act': 'give_keyword', 'keyword': 'Sentinel',
                                                  'on': {'pick': 'self'}, 'lasts': 'permanent'}]})
        n += json.dumps(r, sort_keys=True) != before
    for r in recs:
        before = json.dumps(r, sort_keys=True)
        this_turn(r, text.get(r.get('id'), ''))
        new_values(r, text.get(r.get('id'), ''))
        direct(r)
        n += json.dumps(r, sort_keys=True) != before
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), n, 'changed')
