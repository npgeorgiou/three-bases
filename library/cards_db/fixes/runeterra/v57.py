"""Runeterra records, 30 Oct 2026 (v57), by rule; safe to run twice. Found by Kaptain on Dragon Ambush:
- "Start a free attack with N <card>": the N cards are summoned for the attack (as Nagakabouros' Tantrum was read), not
  picked among cards already in play: summon N of that card, then start an attack with them."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
WORD = {'a': 1, 'an': 1, 'two': 2, 'three': 3, 'four': 4}
text = {i: ' '.join((t or '').split()) for i, t in lib.execute("select id, text from entities where game='runeterra'")}
n = 0
for P in glob.glob(os.path.join(HERE, 'read', 'runeterra', '*.jsonl')):
    recs = [json.loads(l) for l in open(P) if l.strip()]; changed = False
    for r in recs:
        m = re.search(r"[Ss]tarts? a free attack with (\d+|an?|two|three|four) ([A-Z][\w' ]+?)s?\.", text.get(r.get('id'), ''))
        if not m: continue
        k = int(m.group(1)) if m.group(1).isdigit() else WORD[m.group(1)]
        for ab in r.get('abilities', []):
            do = ab.get('do', [])
            for j, e in enumerate(do):
                on = e.get('on') or {}
                ref = next((x.get('ref') for x in on.get('with', []) if x.get('attr') == 'card' and x.get('op') == 'is'), None)
                if e.get('act') == 'start_attack' and ref and on.get('pick') != 'it':
                    do[j:j + 1] = [{'act': 'summon', 'zone': 'board', 'card': ref, 'params': {'amount': k}},
                                   {'act': 'start_attack', 'on': {'kind': 'unit', 'side': 'mine', 'pick': 'it', 'zone': 'board'}, 'link': 'then'}]
                    n += 1; changed = True; break
    if changed: open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
print(n, 'effects changed')
