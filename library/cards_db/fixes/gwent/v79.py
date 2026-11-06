"""Gwent, 6 Nov 2026 (v79, family 1 second pass, BRIEF Game words: Gwent); safe to run twice.
Cards whose create rows v78 wrote with a filter it could not fully read (`unsure` holds "create") are read again with v78's
improved reader: the n-th `create` row (made from text) gets the filter of the n-th "Create" in the text, when both counts match."""
import glob, json, os, re, importlib.util
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location('v78', os.path.join(HERE, 'fixes', 'gwent', 'v78.py')); v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)


def main():
    T = v.texts()
    for path in sorted(glob.glob(os.path.join(HERE, 'read', 'gwent', '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path or 'keywords' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            if 'create' not in r.get('unsure', []): continue
            t = T.get(r['id'], '')
            acts = [a for ab in r['abilities'] for a in ab.get('do', []) if a.get('act') == 'create' and isinstance(a.get('on'), dict) and a['on'].get('pick') == 'random']
            if len(acts) != len(re.findall(r'\bCreate\b', t)): print('SKIP', r['id']); continue
            bad = False
            for i, a in enumerate(acts):
                on, left = v.parse(v.clause(t, i)); a['on'] = on; n += 1
                if left: bad = True; print('LEFT', r['id'], repr(left))
            if not bad:
                r['unsure'] = [u for u in r['unsure'] if u != 'create']
                if not r['unsure']: r.pop('unsure')
        if n: open(path, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'reread')


if __name__ == '__main__':
    main()
