"""Prints cards with their text and records in a short readable form, for checking by eye.
Usage: show.py <game> <records.jsonl> <input.jsonl> [ids comma-separated | --random N | --all]"""
import json, random, sys

def tg(t):
    if not t: return ''
    if set(t) == {'pick'}: return t['pick']
    parts = [str(t.get(k)) for k in ('pick', 'side', 'kind') if t.get(k)]
    if 'n' in t: parts.insert(0, am(t['n']))
    if t.get('zone'): parts.append('in ' + t['zone'])
    for f in t.get('with', []):
        parts.append('[%s %s %s]' % (f.get('attr'), f.get('op'), f.get('ref', f.get('val', f.get('n')))))
    return ' '.join(parts)

def am(a):
    if isinstance(a, (int, float)): return str(a)
    s = a.get('x', '?')
    if 'attr' in a: s += ' ' + a['attr']
    if 'of' in a: s += ' of (' + tg(a['of']) + ')'
    if 'event' in a: s += ' of (' + ev(a['event']) + ')'
    if 'span' in a: s += ' ' + a['span']
    if 'inner' in a: s += ' (' + am(a['inner']) + ')'
    return s

def ev(e):
    s = e.get('event', '?')
    if 'actor' in e: s += ' by ' + tg(e['actor'])
    if 'object' in e: s += ' of ' + tg(e['object'])
    return s

def cond(c):
    s = c.get('test', '?')
    for k in ('of', 'event'):
        if k in c: s += ' ' + (tg(c[k]) if k == 'of' else ev(c[k]))
    for k in ('attr', 'op'):
        if k in c: s += ' ' + str(c[k])
    if 'n' in c: s += ' ' + am(c['n'])
    if 'span' in c: s += ' ' + c['span']
    if 'ref' in c: s += ' ' + c['ref']
    return s

def eff(e):
    s = (e.get('link', '') + ' ' if e.get('link') else '') + e.get('act', '?')
    if 'keyword' in e: s += ' ' + e['keyword']
    if 'card' in e: s += ' "' + e['card'] + '"'
    if 'on' in e: s += ' -> ' + tg(e['on'])
    if 'to' in e: s += ' to ' + tg(e['to'])
    if 'zone' in e: s += ' into ' + e['zone']
    for p, a in (e.get('params') or {}).items(): s += f' {p}={a if isinstance(a, str) else am(a)}'
    if 'lasts' in e: s += ' (' + e['lasts'] + ')'
    return s

def render(rec):
    out = []
    if 'trigger' in rec: out.append('  trigger: ' + ev(rec['trigger']))
    for c in rec.get('condition', []): out.append('  condition: ' + cond(c))
    for ab in rec.get('abilities', []):
        head = 'WHEN ' + ev(ab.get('when', {}))
        if ab.get('limit'): head += ' [' + ab['limit'] + ']'
        if ab.get('if'): head += ' IF ' + ' AND '.join(cond(c) for c in ab['if'])
        out.append('  ' + head)
        for e in ab.get('do', []): out.append('     ' + eff(e))
    if rec.get('unsure'): out.append('  unsure: ' + ', '.join(rec['unsure']))
    return '\n'.join(out) or '  (no abilities)'

if __name__ == '__main__':
    recs = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[2]) if l.strip()}
    inp = [json.loads(l) for l in open(sys.argv[3])]
    sel = sys.argv[4] if len(sys.argv) > 4 else '--all'
    if sel == '--random': random.seed(int(sys.argv[6]) if len(sys.argv) > 6 else 1); inp = random.sample(inp, int(sys.argv[5]))
    elif sel != '--all': want = {int(x) for x in sel.split(',')}; inp = [x for x in inp if x['id'] in want]
    for x in inp:
        print(f"## {x['name']} ({x['category']}) {x['id']}\n  TEXT: {x['text']}")
        print(render(recs.get(x['id'], {})))
