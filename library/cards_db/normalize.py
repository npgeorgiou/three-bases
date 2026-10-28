"""Puts records into one canonical form where readers wrote the same meaning in different ways (found by comparing first
and second readings). Safe to run any number of times. Each rule is listed in CHANGES.md.
  N1 create / summon of a named card: the receiving player in "on" is dropped (the card and zone say it all).
  N2 a keyword used on a target is keyword_action when the keyword's own record is an action (an "activated" ability),
     and give_keyword when it is a status the target then has (Frostbite, Stun-like keywords given "this round").
  N3 null values and empty lists/objects are dropped.
  N4 "follower" and "champion" are categories, not states; a category filter "unit" on a target of kind unit is dropped.
  N5 when the text says "another ally" / "other allies", the event object and the effect targets of my units get the
     not-this-card filter if they lack it.
  N6 names.tsv: a name read as a keyword or a card that is something else becomes it (keyword, card, type, name_has) or
     is dropped (filters and effects naming it removed); a keyword that is a card becomes play_card of it. Per game, with reasons.
  N7 a unit put into play attacking ("summon an attacking X", "revive an attacking copy") = the summon/revive/copy, then
     start_attack on it (link and); a state attacking filter on its target is that, written the other way.
  N8 a copy of a dead unit put into play (copy, on: unit in discard, zone board) is revive.
  N9 a keyword used as an action whose own record picks its target itself (Toss: the bottom of your deck; Nab; Rally)
     carries no "on": the keyword's record says what it acts on.
  N11 summon / create / copy / play_card of a named card: an "on" that only says the kind (unit, landmark) is dropped; the
     card says what it is (same meaning as N1).
  N12 a trigger on being given a keyword, narrowed by an it_matches condition that names the keyword ("keyword is Stun", or a
     state given by it: "state is stunned"), is written as the trigger's object filter "keyword is <it>" (one form, every game;
     Yasuo, Fae Bladetwirler and The Tidedancer were read the other way).
  N13 steal aimed at my own side (pick self or side mine: "convert itself") is donate; steal is only taking the enemy's.
  N10 games whose units have one stat, strength (Stormbound): "strongest" / "weakest" are pick highest / lowest by strength,
     never the Power-based picks.
Usage: normalize.py <game> <file.jsonl> [...]   rewrites the files in place, prints how many records changed."""
import csv, glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def keyword_kinds(game):
    """keyword name (lower) -> 'action' or 'status', from read/<game>/keywords.jsonl and the input names."""
    names = {json.loads(l)['id']: json.loads(l)['name'].lower() for l in open(os.path.join(HERE, 'input', game, 'keywords.jsonl'))}
    kinds = {}
    for l in open(os.path.join(HERE, 'read', game, 'keywords.jsonl')):
        r = json.loads(l); ab = r.get('abilities', [])
        if ab: kinds[names[r['id']]] = 'action' if any(a.get('when', {}).get('event') == 'activated' for a in ab) else 'status'
        act = [a for a in ab if a.get('when', {}).get('event') == 'activated']
        if act and '"it"' not in json.dumps(act): SELF_TARGET.add(names[r['id']])
    return kinds

SELF_TARGET = set()  # N9

def clean(x):
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items() if v is not None and (k == 'abilities' or (v != [] and v != {}))}
    if isinstance(x, list): return [clean(v) for v in x]
    return x

def fix_filters(x):
    if isinstance(x, dict):
        if isinstance(x.get('with'), list):
            w = []
            for f in x['with']:
                if f.get('attr') == 'state' and f.get('val') in ('follower', 'champion'): f['attr'] = 'category'
                if f.get('attr') == 'category' and f.get('val') == 'unit' and f.get('op') == 'is' and x.get('kind') == 'unit': continue
                w.append(f)
            x['with'] = w
            if not w: x.pop('with')
        for v in x.values(): fix_filters(v)
    elif isinstance(x, list):
        for v in x: fix_filters(v)

def fix_effect(e, kinds):
    if e.get('act') == 'steal' and ((e.get('on') or {}).get('pick') == 'self' or (e.get('on') or {}).get('side') == 'mine'):
        e['act'] = 'donate'  # N13
    if e.get('card') and e.get('act') in ('summon', 'create', 'copy', 'play_card') and isinstance(e.get('on'), dict) and set(e['on']) <= {'kind'}:
        e.pop('on')  # N11
    act = e.get('act')
    if act in ('create', 'summon') and e.get('card') and (e.get('on') or {}).get('kind') == 'player': e.pop('on')
    kw = (e.get('keyword') or '').lower()
    if act in ('keyword_action', 'give_keyword') and kw in kinds:
        e['act'] = 'keyword_action' if kinds[kw] == 'action' else 'give_keyword'
        if e['act'] == 'keyword_action': e.pop('lasts', None)
        if e['act'] == 'keyword_action' and kw in SELF_TARGET: e.pop('on', None)  # N9
        elif 'lasts' not in e: e['lasts'] = 'unstated'
    if 'ability' in e: fix_ability(e['ability'], kinds)

def fix_ability(ab, kinds):
    for e in ab.get('do', []): fix_effect(e, kinds)

ANOTHER = re.compile(r"\b(?:another|other) (?:allied |\w+ )?(?:all(?:y|ies)|units?|followers?)\b", re.I)

def not_self(t, name):
    if not isinstance(t, dict) or t.get('side') != 'mine' or t.get('pick') in ('self', 'it', 'attached_to', 'right_of_self', 'left_of_self'): return
    if t.get('kind') not in (None, 'unit'): return
    if any(f.get('attr') == 'card' and f.get('op') == 'not' for f in t.get('with', [])): return
    t.setdefault('with', []).append({'attr': 'card', 'op': 'not', 'ref': name})

def another(r, inputs):
    x = inputs.get(r.get('id'))
    if not x or not ANOTHER.search(x['text']): return
    for ab in r.get('abilities', []):
        not_self((ab.get('when') or {}).get('object'), x['name'])
        for e in ab.get('do', []): not_self(e.get('on'), x['name'])

def names_table(game):
    import csv
    return {(r['read_as'], r['name'].lower()): r for r in csv.DictReader(open(os.path.join(HERE, 'names.tsv')), delimiter='\t')
            if r['game'] == game}

def fix_names(x, table):
    """N6"""
    if isinstance(x, dict):
        if isinstance(x.get('with'), list):
            w = []
            for f in x['with']:
                r = table.get((f.get('attr'), str(f.get('ref', '')).lower())) if f.get('attr') in ('keyword', 'card') else None
                if r and r['becomes'] == 'drop': continue
                if r: f['attr'] = r['becomes']; f['ref'] = r['new_name']
                w.append(f)
            x['with'] = w
        if isinstance(x.get('do'), list):
            keep = []
            for e in x['do']:
                rk = table.get(('keyword', (e.get('keyword') or '').lower())); rc = table.get(('card', (e.get('card') or '').lower()))
                if (rk or rc or {}).get('becomes') == 'drop': continue
                if rk and rk['becomes'] == 'keyword': e['keyword'] = rk['new_name']
                if rk and rk['becomes'] == 'card': e.pop('keyword'); e['act'] = 'play_card'; e['card'] = rk['new_name']
                if rc and rc['becomes'] == 'card': e['card'] = rc['new_name']
                if rc and rc['becomes'] == 'type': e.pop('card'); e['type'] = rc['new_name']
                keep.append(e)
            x['do'] = keep
        for v in x.values(): fix_names(v, table)
    elif isinstance(x, list):
        for v in x: fix_names(v, table)

def attacking(x):
    """N7"""
    if isinstance(x, dict):
        if isinstance(x.get('do'), list):
            out = []
            for k, e in enumerate(x['do']):
                out.append(e)
                o = e.get('on') if isinstance(e.get('on'), dict) else {}
                if e.get('act') == 'copy' and o.get('zone') == 'discard' and o.get('kind') == 'unit' and e.get('zone') == 'board':
                    e['act'] = 'revive'; e.pop('zone')  # N8
                if e.get('act') not in ('summon', 'revive', 'copy'): continue
                hit = False
                for side in ('on', 'to'):
                    t = e.get(side)
                    if isinstance(t, dict) and isinstance(t.get('with'), list):
                        w = [f for f in t['with'] if not (f.get('attr') == 'state' and f.get('val') == 'attacking' and f.get('op') in ('is', 'in'))]
                        if len(w) != len(t['with']):
                            hit = True; t['with'] = w
                            if not w: t.pop('with')
                            if side == 'to' and set(t) <= {'kind', 'side'}: e.pop('to')
                nxt = x['do'][k + 1] if k + 1 < len(x['do']) else {}
                if hit and nxt.get('act') != 'start_attack': out.append({'act': 'start_attack', 'on': {'pick': 'it'}, 'link': 'and'})
            x['do'] = out
        for v in x.values(): attacking(v)
    elif isinstance(x, list):
        for v in x: attacking(v)

STRENGTH_GAMES = {'stormbound'}

def strength_picks(x):
    """N10"""
    if isinstance(x, dict):
        if x.get('pick') in ('strongest', 'weakest'):
            x['by'] = 'strength'; x['pick'] = 'highest' if x['pick'] == 'strongest' else 'lowest'
        for v in x.values(): strength_picks(v)
    elif isinstance(x, list):
        for v in x: strength_picks(v)

def status_keywords():
    """state -> the keyword that gives it (vocab causes given_keyword:<Keyword>)"""
    out = {}
    for r in csv.DictReader(open(os.path.join(HERE, 'vocab.tsv')), delimiter='\t'):
        if r['field'] == 'state' and r['causes'].startswith('given_keyword:'): out[r['value']] = r['causes'].split(':', 1)[1]
    return out

def keyword_trigger_form(r, st):
    """N12"""
    for ab in r.get('abilities', []):
        w = ab.get('when') or {}
        if w.get('event') != 'given_keyword': continue
        keep = []
        for cd in ab.get('if', []):
            fs = (cd.get('of') or {}).get('with', [])
            names = [f.get('ref') if f.get('attr') == 'keyword' else st.get(f.get('val')) for f in fs
                     if f.get('op') == 'is' and (f.get('attr') == 'keyword' or (f.get('attr') == 'state' and f.get('val') in st))]
            if cd.get('test') == 'it_matches' and fs and len(names) == len(fs) and len(set(names)) == 1:
                obj = w.setdefault('object', {}); obj.setdefault('with', [])
                if not any(f.get('attr') == 'keyword' for f in obj['with']): obj['with'].append({'attr': 'keyword', 'op': 'is', 'ref': names[0]})
            else: keep.append(cd)
        if keep: ab['if'] = keep
        else: ab.pop('if', None)

def main():
    global STATUS
    game = sys.argv[1]; kinds = keyword_kinds(game); table = names_table(game); STATUS = status_keywords()
    inputs = {}
    for f in glob.glob(os.path.join(HERE, 'input', game, '*.jsonl')):
        for l in open(f): x = json.loads(l); inputs[x['id']] = x
    for path in sys.argv[2:]:
        L = [json.loads(l) for l in open(path) if l.strip()]; out = []; n = 0
        for r in L:
            r2 = clean(json.loads(json.dumps(r)))
            for ab in r2.get('abilities', []): fix_ability(ab, kinds)
            fix_names(r2, table); attacking(r2); fix_filters(r2); another(r2, inputs)
            if game in STRENGTH_GAMES: strength_picks(r2)
            keyword_trigger_form(r2, STATUS)
            n += r2 != r; out.append(r2)
        open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in out))
        print(f'{os.path.basename(path)}: {n} of {len(L)} records changed')

if __name__ == '__main__':
    main()
