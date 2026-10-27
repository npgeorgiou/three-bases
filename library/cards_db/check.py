"""Checks reader records against the shapes in BRIEF.md and the values in vocab.tsv, and resolves every name to an entry id.
Usage: check.py <game> <records.jsonl> [--input batch.jsonl]   prints each problem with the card id and path; exit code 1 on any.
Imported by load.py (resolve, check_card)."""
import csv, json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, '..', 'three-bases-library.sqlite')
sys.path.insert(0, HERE)
from build_input import types_of


def vocab():
    v = {}
    for r in csv.DictReader(open(os.path.join(HERE, 'vocab.tsv')), delimiter='\t'): v.setdefault(r['field'], set()).add(r['value'])
    return v


class Names:
    """name -> ids per link kind: card (any entry but keywords and tribes), keyword, type (subtypes and tribe entries)."""
    def __init__(self, c, game):
        self.card, self.keyword, self.type = {}, {}, {}
        for i, n, cat, sub in c.execute("select id, name, category, subtypes from entities where game=?", (game,)):
            key = (n or '').lower().strip()
            if cat == 'keyword': self.keyword.setdefault(key, []).append(i)
            elif cat == 'tribe': self.type.setdefault(key, []).append(i)
            else:
                self.card.setdefault(key, []).append(i)
                for t in types_of(sub): self.type.setdefault(t.lower(), [])
    def resolve(self, kind, name):
        d = getattr(self, kind); key = (name or '').lower().strip()
        if key in d: return d[key] or ['type:' + key]
        if kind == 'type' and key.endswith('s') and key[:-1] in d: return d[key[:-1]] or ['type:' + key[:-1]]
        return None


SHAPES = {
    'card': {'id', 'name', 'abilities', 'unsure', 'trigger', 'condition'},
    'ability': {'when', 'limit', 'if', 'do'},
    'event': {'event', 'actor', 'object'},
    'target': {'kind', 'side', 'pick', 'n', 'zone', 'with', 'by'},
    'filter': {'attr', 'op', 'n', 'ref', 'val', 'vals', 'refs'},
    'cond': {'test', 'of', 'attr', 'op', 'n', 'span', 'event', 'ref', 'value'},
    'effect': {'act', 'on', 'to', 'zone', 'card', 'keyword', 'params', 'lasts', 'link', 'ability', 'type'},
    'amount': {'x', 'of', 'attr', 'event', 'span', 'inner', 'items'},
}
NEEDS_LASTS = {'stat_change', 'give_keyword', 'cant', 'can', 'cost_change'}


class Checker:
    def __init__(self, game):
        self.v = vocab(); self.names = Names(sqlite3.connect(DB), game); self.errors = []; self.links = []; self.stubs = []
    def err(self, cid, path, msg): self.errors.append((cid, path, msg))
    def enum(self, cid, path, field, val):
        if val not in self.v.get(field, ()): self.err(cid, path, f'{field} value {val!r} not in vocab')
    def keys(self, cid, path, shape, d):
        if not isinstance(d, dict): self.err(cid, path, f'{shape} must be an object'); return False
        for k in d:
            if k not in SHAPES[shape]: self.err(cid, path, f'{shape} has unknown key {k!r}')
        return True
    def link(self, cid, path, kind, name):
        ids = self.names.resolve(kind, name)
        if not ids and kind in ('card', 'keyword') and isinstance(name, str) and name.strip():
            self.stubs.append((cid, path, kind, name))  # named in the text but missing from the library: kept as a stub entry
        elif not ids: self.err(cid, path, f'{kind} name {name!r} not found')
        elif len(ids) > 1 and kind == 'card': self.links.append((cid, path, kind, name, ids))  # several entries share the name
        return ids
    def amount(self, cid, path, a):
        if isinstance(a, (int, float)) and not isinstance(a, bool): return
        if not self.keys(cid, path, 'amount', a): return
        self.enum(cid, path + '.x', 'x', a.get('x'))
        if 'of' in a: self.target(cid, path + '.of', a['of'])
        if 'attr' in a: self.enum(cid, path + '.attr', 'attr', a['attr'])
        if 'event' in a: self.event(cid, path + '.event', a['event'])
        if 'span' in a: self.enum(cid, path + '.span', 'span', a['span'])
        if 'inner' in a: self.amount(cid, path + '.inner', a['inner'])
        for k, it in enumerate(a.get('items', [])): self.amount(cid, f'{path}.items[{k}]', it)
    def target(self, cid, path, t):
        if not self.keys(cid, path, 'target', t): return
        for f in ('kind', 'side', 'pick', 'zone'):
            if f in t: self.enum(cid, f'{path}.{f}', f, t[f])
        if 'n' in t: self.amount(cid, path + '.n', t['n'])
        if 'by' in t: self.enum(cid, path + '.by', 'attr', t['by'])
        for k, f in enumerate(t.get('with', [])): self.filt(cid, f'{path}.with[{k}]', f)
    def filt(self, cid, path, f):
        if not self.keys(cid, path, 'filter', f): return
        a = f.get('attr'); self.enum(cid, path + '.attr', 'attr', a); self.enum(cid, path + '.op', 'op', f.get('op'))
        if a in ('keyword', 'type', 'card'):
            for r in (f['refs'] if 'refs' in f else [f.get('ref')]): self.link(cid, path + '.ref', a, r)
        elif a in ('state', 'category', 'region', 'origin', 'rarity'):
            for x in (f['vals'] if 'vals' in f else [f.get('val')]): self.enum(cid, path + '.val', 'state' if a == 'origin' else a, x)
        elif a == 'name_has':
            if not isinstance(f.get('ref'), str) or not f['ref'].strip(): self.err(cid, path + '.ref', 'name word expected')
        elif a in ('power', 'health', 'cost', 'count', 'base_power', 'base_health', 'damage', 'countdown'):
            if 'vals' in f and f.get('op') == 'in':
                if not all(isinstance(v, (int, float)) for v in f['vals']): self.err(cid, path + '.vals', 'numbers expected')
            elif 'n' not in f: self.err(cid, path + '.n', 'number or amount expected')
            else: self.amount(cid, path + '.n', f['n'])
    def event(self, cid, path, e):
        if not self.keys(cid, path, 'event', e): return
        self.enum(cid, path + '.event', 'event', e.get('event'))
        for k in ('actor', 'object'):
            if k in e: self.target(cid, f'{path}.{k}', e[k])
    def cond(self, cid, path, c):
        if not self.keys(cid, path, 'cond', c): return
        self.enum(cid, path + '.test', 'test', c.get('test'))
        if 'of' in c: self.target(cid, path + '.of', c['of'])
        if 'attr' in c: self.enum(cid, path + '.attr', 'attr', c['attr'])
        if 'op' in c: self.enum(cid, path + '.op', 'op', c['op'])
        if 'n' in c: self.amount(cid, path + '.n', c['n'])
        if 'span' in c: self.enum(cid, path + '.span', 'span', c['span'])
        if 'event' in c: self.event(cid, path + '.event', c['event'])
        if 'ref' in c: self.link(cid, path + '.ref', 'keyword', c['ref'])
        if 'value' in c: self.amount(cid, path + '.value', c['value'])
    def effect(self, cid, path, e, first):
        if not self.keys(cid, path, 'effect', e): return
        act = e.get('act'); self.enum(cid, path + '.act', 'act', act)
        for k in ('on', 'to'):
            if k in e: self.target(cid, f'{path}.{k}', e[k])
        if 'zone' in e: self.enum(cid, path + '.zone', 'zone', e['zone'])
        if 'card' in e: self.link(cid, path + '.card', 'card', e['card'])
        if 'keyword' in e: self.link(cid, path + '.keyword', 'keyword', e['keyword'])
        if 'type' in e: self.link(cid, path + '.type', 'type', e['type'])
        if 'ability' in e: self.ability(cid, path + '.ability', e['ability'])
        for p, a in (e.get('params') or {}).items():
            if p == 'event': self.enum(cid, f'{path}.params.event', 'event', a)
            elif p == 'attr': self.enum(cid, f'{path}.params.attr', 'attr', a)
            else: self.enum(cid, f'{path}.params', 'param', p); self.amount(cid, f'{path}.params.{p}', a)
        if 'lasts' in e: self.enum(cid, path + '.lasts', 'lasts', e['lasts'])
        elif act in NEEDS_LASTS: self.err(cid, path, f'{act} needs lasts')
        if 'link' in e: self.enum(cid, path + '.link', 'link', e['link'])
        elif not first: self.err(cid, path, 'link needed from the 2nd effect on')
    def card(self, rec):
        cid = rec.get('id')
        if not self.keys(cid, 'card', 'card', rec): return
        if not isinstance(rec.get('abilities'), list): self.err(cid, 'abilities', 'list expected'); return
        if 'trigger' in rec: self.event(cid, 'trigger', rec['trigger'])
        for j, c in enumerate(rec.get('condition', [])): self.cond(cid, f'condition[{j}]', c)
        for k, ab in enumerate(rec['abilities']): self.ability(cid, f'abilities[{k}]', ab)
    def ability(self, cid, p, ab):
        if not self.keys(cid, p, 'ability', ab): return
        if 'when' not in ab: self.err(cid, p, 'when missing')
        else: self.event(cid, p + '.when', ab['when'])
        if 'limit' in ab: self.enum(cid, p + '.limit', 'limit', ab['limit'])
        for j, c in enumerate(ab.get('if', [])): self.cond(cid, f'{p}.if[{j}]', c)
        if not ab.get('do'): self.err(cid, p, 'do missing')
        for j, e in enumerate(ab.get('do', [])): self.effect(cid, f'{p}.do[{j}]', e, j == 0)


def main():
    game, path = sys.argv[1], sys.argv[2]
    ch = Checker(game); seen = []
    for n, line in enumerate(open(path), 1):
        if not line.strip(): continue
        try: rec = json.loads(line)
        except Exception as e: ch.err('line %d' % n, '', 'not JSON: %s' % e); continue
        seen.append(rec.get('id')); ch.card(rec)
    if '--input' in sys.argv:
        want = [json.loads(l)['id'] for l in open(sys.argv[sys.argv.index('--input') + 1])]
        for i in set(want) - set(seen): ch.err(i, '', 'card missing from the output')
        for i in set(seen) - set(want): ch.err(i, '', 'card not in the input')
    for e in ch.errors: print('%s | %s | %s' % e)
    for e in ch.stubs: print('stub | %s | %s | %s %r' % e)
    print(f'{len(seen)} records, {len(ch.errors)} problems, {len(ch.links)} names with several entries, {len(ch.stubs)} stub names')
    sys.exit(1 if ch.errors else 0)


if __name__ == '__main__':
    main()
