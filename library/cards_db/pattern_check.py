"""Basic word checks against the records: plain wording that must show up somewhere in a card's record.
If a card's text says "Round Start:", some ability of it waits for round_start; if it says "Stun", some effect stuns; if it
names a keyword (outside its own Keywords field), the record links that keyword somewhere. Only unambiguous wording.
The wording rules are in patterns/patterns.tsv (one line each: game or *, id, regex, what the record must hold, use
yes / no / strip (wording with no effect, removed before checking), reason); each named keyword outside the card's own Keywords field must be linked (rule KW). Other cards' names are masked.
Flags already judged (patterns/verdicts.tsv) are not repeated.
Usage: pattern_check.py <game> [--reread]   writes patterns/<game>_flags.tsv; --reread makes the re-read batches with notes."""
import csv, glob, json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_input import KWFIELD
import source

# keywords that records say through an act or a value instead of a link to the keyword
KW_EQUIV = {'landmark': 'landmark', 'equipment': 'equipment|attach|attached_to|equipped|unequip', 'equip': 'attach|equipped|attached_to|equipment',
            'rally': 'gain_attack_token', 'advance': 'countdown_advance', 'behold': 'have', 'ephemeral': 'ephemeral',
            'fleeting': 'fleeting', 'capture': 'capture', 'frostbite': 'frostbitten', 'vulnerable': 'vulnerable'}

def patterns(game):
    return [r for r in csv.DictReader(open(os.path.join(HERE, 'patterns', 'patterns.tsv')), delimiter='\t')
            if r['game'] in ('*', game) and r['use'] == 'yes']

def strips(game):
    return [r['wording'] for r in csv.DictReader(open(os.path.join(HERE, 'patterns', 'patterns.tsv')), delimiter='\t')
            if r['game'] in ('*', game) and r['use'] == 'strip']

def verdicts(game):
    return {(int(r['card']), r['pattern']) for r in csv.DictReader(open(os.path.join(HERE, 'patterns', 'verdicts.tsv')), delimiter='\t')
            if r['game'] == game}

def walk(x, out):
    if isinstance(x, dict):
        for v in x.values():
            if isinstance(v, str): out['value'].add(v.lower())
        for v in x.get('vals', []): out['value'].add(str(v).lower())
        if 'event' in x and isinstance(x['event'], str): out['event'].add(x['event'])
        if 'act' in x: out['act'].add(x['act'])
        for k in ('keyword', 'ref'):
            if isinstance(x.get(k), str): out['name'].add(x[k].lower())
        for k in ('refs',):
            for r in x.get(k, []): out['name'].add(str(r).lower())
        if isinstance(x.get('card'), str): out['name'].add(x['card'].lower())
        for v in x.values(): walk(v, out)
    elif isinstance(x, list):
        for v in x: walk(v, out)

def main():
    game = sys.argv[1]
    c = source.lib(); pats = patterns(game); judged = verdicts(game); cut = strips(game)
    kwnames = {n.lower(): n for (n,) in c.execute("select name from entities where game=? and category='keyword'", (game,))}
    skipkw = {'play', 'attack', 'strike', 'round start', 'round end', 'last breath', 'level up', 'nexus strike', 'countdown',
              'burst', 'fast', 'slow', 'focus', 'skill', 'everywhere', 'weakest', 'strongest', 'attack strike', 'slay', 'support'}
    kwpat = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted(kwnames, key=len, reverse=True) if k not in skipkw) + r')\b')
    multi = {n for (n,) in c.execute("select name from entities where game=? and category not in ('keyword','tribe')", (game,)) if ' ' in n}
    maskall = re.compile('(?:' + '|'.join(re.escape(n.lower()) for n in sorted(multi, key=len, reverse=True) if n.lower() not in kwnames) + r')s?\b')
    inputs = {}
    for f in glob.glob(os.path.join(HERE, 'input', game, 'batch_*.jsonl')):
        for l in open(f): x = json.loads(l); inputs[x['id']] = x
    recs = {}
    for f in glob.glob(os.path.join(HERE, 'read', game, 'batch_*.jsonl')):
        if 'proposals' in f: continue
        for l in open(f): r = json.loads(l); recs[r['id']] = r
    flags = []
    for i, x in inputs.items():
        r = recs.get(i)
        if not r: continue
        t = ' '.join(x['text'].split()); m = KWFIELD.match(t); rest = (t[m.end():] if m else t).lower()
        names = [n.lower() for n in set(x.get('names_in_text', [])) | {x['name']} if n.lower() not in kwnames]
        for sp in cut: rest = re.sub(sp, ' ', rest)  # wording with no effect in play (use strip)
        rest = maskall.sub(' # ', rest)  # cards' names are not wording
        if names: rest = re.sub('(?:' + '|'.join(re.escape(n) for n in sorted(names, key=len, reverse=True)) + r')s?\b', ' # ', rest)
        got = {'event': set(), 'act': set(), 'name': set(), 'value': set()}; walk(r, got)
        for p in pats:
            hit = re.search(p['wording'], rest)
            if not hit: continue
            kind, vals = p['requires'].split(':', 1); vals = set(vals.split('|'))
            if not (vals & got[kind]): flags.append((i, x['name'], p['id'], p['requires'], rest[max(0, hit.start() - 30):hit.end() + 30]))
        own = {k.lower() for k in x['keywords']}
        for k in set(kwpat.findall(rest)):
            if k in own or k in got['name'] or k in ('stun', 'recall', 'obliterate', 'silence'): continue
            if any(re.search(p['wording'], k) for p in pats): continue  # a keyword used as a verb is checked by its verb pattern
            if k in KW_EQUIV and set(KW_EQUIV[k].split('|')) & got['value']: continue
            flags.append((i, x['name'], 'KW', 'name:' + k, rest[max(0, rest.find(k) - 30):rest.find(k) + len(k) + 30]))
    flags = [f for f in flags if (f[0], f[2]) not in judged and (f[0], f[2] + ':' + f[3]) not in judged]
    out = os.path.join(HERE, 'patterns', game + '_flags.tsv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['card', 'name', 'pattern', 'requires', 'text'])
        for row in sorted(flags): w.writerow(row)
    print(f'{len(flags)} flags on {len({f[0] for f in flags})} cards -> {out}')
    if '--reread' in sys.argv:  # one re-read batch for every flagged card, the flags as notes in its input
        import reread
        before = set(glob.glob(os.path.join(HERE, 'input', game, 'fix_*.jsonl')))
        reread.make(game, {f[0] for f in flags}, 20000)
        notes = {}
        for f in flags: notes.setdefault(f[0], []).append(f"the text says '{f[4].strip()}': the record has none of {f[3]}")
        for path in set(glob.glob(os.path.join(HERE, 'input', game, 'fix_*.jsonl'))) - before:
            L = [json.loads(l) for l in open(path)]
            open(path, 'w').write(''.join(json.dumps({**x, 'check_note': notes.get(x['id'], [])}) + '\n' for x in L))

if __name__ == '__main__':
    main()
