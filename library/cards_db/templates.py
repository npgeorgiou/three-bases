"""Sentence templates: rows written by script for the wordings many cards share, so readers read only the rest (START_DATABASE
Part 2 step 0.13a).
  templates.py <game> shapes [min]   the sentence shapes (numbers -> N, names of other cards -> NAME) used by min (5)+ cards,
                                     most used first, and the share of all sentences they cover
  templates.py <game> apply          for every card, the sentences matching templates/<game>.tsv (columns: regex, ability as
                                     JSON with "{1}", "{2}" for the regex groups); writes read/<game>/templates.jsonl (cards
                                     fully covered) and input/<game>/prefilled.json (id -> rows already written, for readers)"""
import collections, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)


def sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])', ' '.join((text or '').split())) if s.strip()]


def shape(s, names=()):
    for n in sorted(names, key=len, reverse=True): s = s.replace(n, 'NAME')
    return re.sub(r'\d+', 'N', s)


def card_shapes(x):
    return {shape(s, x.get('names_in_text') or []) for s in sentences(x['text'])}


def shapes(cards):
    out = collections.defaultdict(set)
    for x in cards:
        for s in card_shapes(x): out[s].add(x['id'])
    return out


def load_inputs(game):
    import glob
    return {x['id']: x for f in glob.glob(os.path.join(HERE, 'input', game, 'batch_*.jsonl')) for x in map(json.loads, open(f))}


def main():
    game, cmd = sys.argv[1], sys.argv[2]
    if cmd == 'shapes':
        import build_input, source
        cards = [x for x in build_input.cards(source.lib(), game) if re.sub(r'[\W_]', '', x['_rest'])]
        lo = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        sh = shapes(cards); total = sum(len(card_shapes(x)) for x in cards)
        common = sorted(((len(v), k) for k, v in sh.items() if len(v) >= lo), reverse=True)
        cov = sum(n for n, _ in common)
        full = sum(1 for x in cards if all(len(sh[s]) >= lo for s in card_shapes(x)))
        for n, k in common: print(n, k, sep='\t')
        print(f'{len(common)} shapes used by {lo}+ cards cover {cov} of {total} sentences ({100 * cov // max(total, 1)}%); '
              f'{full} of {len(cards)} cards are fully covered', file=sys.stderr)
    elif cmd == 'apply':
        T = [(re.compile(r), a) for r, a in (l.rstrip('\n').split('\t')[:2] for l in open(os.path.join(HERE, 'templates', game + '.tsv'))
                                             if l.strip() and not l.startswith('#'))]
        inputs = load_inputs(game); done, pre = [], {}
        for i, x in inputs.items():
            rows, left = [], 0
            for s in sentences(x['text']):
                m = next(((m, a) for r, a in T for m in [r.fullmatch(s)] if m), None)
                if not m: left += 1; continue
                a = m[1]
                for k, g in enumerate(m[0].groups(), 1): a = a.replace('{%d}' % k, g or '')
                rows.append(json.loads(a))
            if rows and not left: done.append({'id': i, 'abilities': rows})
            elif rows: pre[i] = rows
        with open(os.path.join(HERE, 'read', game, 'templates.jsonl'), 'w') as f:
            for r in done: f.write(json.dumps(r, separators=(',', ':')) + '\n')
        json.dump(pre, open(os.path.join(HERE, 'input', game, 'prefilled.json'), 'w'))
        print(f'{len(done)} cards fully written by templates, {len(pre)} partly (prefilled for readers)')


if __name__ == '__main__':
    main()
