"""Gwent, 6 Nov 2026 (v78, family 1: "Create" written without what is created, BRIEF Game words: Gwent); safe to run twice.
- A `keyword_action Create` row (no `on`) becomes {"act":"create","on":{kind,side,pick:random,with:[...]},"zone":"hand"}; the
  filter is read from the words after the n-th "Create" in the card text (state, faction, kind, provision cost, keyword, type,
  starting deck, opponent's faction/hand). Words that are not read are printed and noted in the record's `unsure` as "create".
- A card whose text says Create and whose rows have no Create row at all, only a `summon` of a spell/card by region (Radeyah:
  "Create a Neutral stratagem"), gets that summon turned into `create` (its `to` stays).
Run from library/cards_db: python3 fixes/gwent/v78.py"""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'gwent'
REG = {'Skellige': 'Skellige', 'Northern Realms': 'Northern Realms', 'Nilfgaard': 'Nilfgaard', 'Monsters': 'Monsters',
       "Scoia'tael": 'Scoiatael', 'Syndicate': 'Syndicate', 'Neutral': 'Neutral', 'neutrals': 'Neutral'}
KW = {'Fee', 'Disloyal'}
W = lambda a, op, v, key='val': {'attr': a, 'op': op, key: v}


def texts():
    T = {}
    for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
        for l in open(f):
            if l.strip(): d = json.loads(l); T[d['id']] = d.get('text', '')
    return T


def clause(t, i):
    pos = [m.end() for m in re.finditer(r'\bCreate\b', t)]
    if i >= len(pos): return None
    c = t[pos[i]:]
    c = re.split(r'\. |\.$|, then|, and |, add | then | and give | and boost | to replace| 3 times|, depending', c)[0]
    return re.sub(r'^ and play ', ' ', c).strip()


def parse(c):
    w, side, zone, left, kind = [], 'mine', None, c, 'card'
    def take(pat, f=None):
        nonlocal left
        m = re.search(pat, left)
        if m:
            left = (left[:m.start()] + ' ' + left[m.end():]).strip()
            if f: f(m)
        return bool(m)
    take(r"from your opponent's starting deck", lambda m: (w.append(W('state', 'is', 'started_in_deck')), globals().__setitem__('_s', 'enemy')))
    if '_s' in globals(): side = globals().pop('_s')
    take(r"from either player's starting deck", lambda m: w.append(W('state', 'is', 'started_in_deck')))
    take(r"from your starting deck", lambda m: w.append(W('state', 'is', 'started_in_deck')))
    if take(r"from your opponent's hand"): side, zone = 'enemy', 'hand'
    take(r"(?:that )?(?:was )?not in your starting deck", lambda m: w.append(W('state', 'not', 'started_in_deck')))
    take(r"(?:that )?(?:was )?not in their starting deck", lambda m: w.append(W('state', 'not', 'started_in_deck')))
    take(r"from your opponent's faction", lambda m: w.append(W('state', 'is', 'opponent_faction')))
    take(r"from any faction")
    take(r"from your faction", lambda m: w.append(W('region', 'is', 'own_regions')))
    m = re.search(r'\b(bronze|silver|gold|legendary)\b', left)
    if m: w.append(W('state', 'is', 'gold' if m.group(1) == 'legendary' else m.group(1))); take(r'\b(bronze|silver|gold|legendary)\b')
    for k in REG:
        if take(r"(?<![A-Za-z])" + re.escape(k) + r"(?![A-Za-z])"): w.append(W('region', 'is', REG[k]))
    take(r"provision cost equal to,? or lower than,? (?:this|the) (?:unit|card)'s power", lambda m: w.append(W('cost', 'le', {'x': 'stat', 'attr': 'strength', 'of': {'pick': 'self'}}, 'n')))
    take(r"provision cost equal to,? (?:this|the) (?:unit|card)'s power", lambda m: w.append(W('cost', 'eq', {'x': 'stat', 'attr': 'strength', 'of': {'pick': 'self'}}, 'n')))
    take(r"\[?(\d+)\]?-provision(?: cost)?", lambda m: w.append(W('cost', 'eq', int(m.group(1)), 'n')))
    take(r"\d+-power copy of")
    if take(r"special card"): w.append(W('category', 'is', 'spell'))
    elif take(r"\b[Ss]pell\b"): w.append(W('category', 'is', 'spell'))
    elif take(r"\bartifact\b"): w.append(W('category', 'is', 'landmark'))
    elif take(r"\bunit\b"): kind = 'unit'
    take(r"with an? ([A-Z]\w+) ability", lambda m: w.append(W('keyword', 'is', m.group(1), 'ref')))
    take(r"with an? ([A-Z]\w+)", lambda m: w.append(W('keyword', 'is', m.group(1), 'ref')))
    take(r"\bcard\b")
    for m in re.finditer(r"\b[A-Z][A-Za-z']+(?: [A-Z][A-Za-z']+)*", left):
        s = m.group(0)
        w.append(W('keyword', 'is', s, 'ref') if s in KW else W('type', 'is', s, 'ref'))
        left = left.replace(s, ' ')
    left = re.sub(r'\b(a|an|and|or|with|play|the|of|from)\b', ' ', left).strip()
    on = {'kind': kind, 'side': side, 'pick': 'random'}
    if zone: on['zone'] = zone
    if w: on['with'] = w
    return on, left


def main():
    T = texts(); total = 0
    for path in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path or 'keywords' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            t = T.get(r.get('id'), '')
            if not re.search(r'\bCreate\b', t) or not r.get('abilities'): continue
            i = 0; bad = False
            acts = [a for ab in r['abilities'] for a in ab.get('do', [])]
            for a in acts:
                if a.get('act') == 'keyword_action' and a.get('keyword') == 'Create' and 'on' not in a:
                    c = clause(t, i); i += 1
                    if c is None: print('NO CLAUSE', r['id']); continue
                    on, left = parse(c)
                    new = {'act': 'create', 'on': on, 'zone': 'hand'}
                    if a.get('link'): new['link'] = a['link']
                    a.clear(); a.update(new); n += 1
                    if left: bad = True; print('LEFT', r['id'], repr(c), '->', repr(left))
            if i == 0 and not any(a.get('act') == 'create' for a in acts):
                for a in acts:
                    if a.get('act') == 'summon' and isinstance(a.get('on'), dict) and a['on'].get('kind') == 'spell' and not a['on'].get('side') \
                       and any(x.get('val') == 'Neutral' for x in a['on'].get('with', [])):
                        a['act'] = 'create'; a['zone'] = 'hand'; n += 1
            if bad:
                r['unsure'] = sorted(set(r.get('unsure', []) + ['create']))
        if n:
            open(path, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L)); total += n
        print(os.path.basename(path), n, 'changed')
    print('total', total)


if __name__ == '__main__':
    main()
