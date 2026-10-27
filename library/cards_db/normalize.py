"""Puts records into one canonical form where readers wrote the same meaning in different ways (found by comparing first
and second readings). Safe to run any number of times. Each rule is listed in CHANGES.md.
  N1 create / summon of a named card: the receiving player in "on" is dropped (the card and zone say it all).
  N2 a keyword used on a target is keyword_action when the keyword's own record is an action (an "activated" ability),
     and give_keyword when it is a status the target then has (Frostbite, Stun-like keywords given "this round").
  N3 null values and empty lists/objects are dropped.
  N4 "follower" and "champion" are categories, not states; a category filter "unit" on a target of kind unit is dropped.
  N5 when the text says "another ally" / "other allies", the event object and the effect targets of my units get the
     not-this-card filter if they lack it.
Usage: normalize.py <game> <file.jsonl> [...]   rewrites the files in place, prints how many records changed."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def keyword_kinds(game):
    """keyword name (lower) -> 'action' or 'status', from read/<game>/keywords.jsonl and the input names."""
    names = {json.loads(l)['id']: json.loads(l)['name'].lower() for l in open(os.path.join(HERE, 'input', game, 'keywords.jsonl'))}
    kinds = {}
    for l in open(os.path.join(HERE, 'read', game, 'keywords.jsonl')):
        r = json.loads(l); ab = r.get('abilities', [])
        if ab: kinds[names[r['id']]] = 'action' if any(a.get('when', {}).get('event') == 'activated' for a in ab) else 'status'
    return kinds

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
    act = e.get('act')
    if act in ('create', 'summon') and e.get('card') and (e.get('on') or {}).get('kind') == 'player': e.pop('on')
    kw = (e.get('keyword') or '').lower()
    if act in ('keyword_action', 'give_keyword') and kw in kinds:
        e['act'] = 'keyword_action' if kinds[kw] == 'action' else 'give_keyword'
        if e['act'] == 'keyword_action': e.pop('lasts', None)
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

def main():
    game = sys.argv[1]; kinds = keyword_kinds(game)
    inputs = {}
    for f in glob.glob(os.path.join(HERE, 'input', game, '*.jsonl')):
        for l in open(f): x = json.loads(l); inputs[x['id']] = x
    for path in sys.argv[2:]:
        L = [json.loads(l) for l in open(path) if l.strip()]; out = []; n = 0
        for r in L:
            r2 = clean(json.loads(json.dumps(r)))
            for ab in r2.get('abilities', []): fix_ability(ab, kinds)
            fix_filters(r2); another(r2, inputs)
            n += r2 != r; out.append(r2)
        open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in out))
        print(f'{os.path.basename(path)}: {n} of {len(L)} records changed')

if __name__ == '__main__':
    main()
