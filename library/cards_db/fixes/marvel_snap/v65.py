"""Marvel Snap, 5 Nov 2026 (v65, step 2.4 names); safe to run twice.
- A name for a set of cards ("4 Ancient Arcana", "2 Arrows", "an Incantation", "2 Thief's Tools", "an Infinity Shot") is one
  of the cards the game's sources list for it: the card filter in refs (create or shuffle: on kind card with that filter).
  Sets from snap.fan's Tokens lists (read 5 Nov 2026) and the cards' previews: Agamotto, Merlin, Prowler; Kate Bishop's
  four Arrows (snap.fan card preview Kate Bishop); Thanos Fractured Frontier's six Shots (marvelsnapzone.com guide).
- "Not revealed until the game ends" has no value (names.tsv drops Hidden): Invisible Woman and Malekith are unsure (act)."""
import glob, json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'marvel_snap'
SETS = {'Ancient Arcana': ['Winds of Watoomb', 'Temporal Manipulation', 'Images of Ikonn', 'Bolts of Balthakk'],
        'Arrow': ['Acid Arrow', 'Basic Arrow', 'Grapple Arrow', 'PymParticle Arrow'],
        'Incantation': ['Omniversal Presence', 'Once And Future', 'Polymorph'],
        "Thief's Tools": ['Remote Mines', 'Vibro-Shock Gauntlets', 'Flight Harness'],
        'Infinity Shot': ['Mind Shot', 'Power Shot', 'Reality Shot', 'Soul Shot', 'Space Shot', 'Time Shot']}
UNSURE = {8000268, 8000350}


def walk(x):
    n = 0
    if isinstance(x, dict):
        if x.get('card') in SETS and 'act' in x:
            on = x.get('on') if isinstance(x.get('on'), dict) and x['on'].get('kind') == 'card' else {'kind': 'card'}
            on.pop('pick', None) if on.get('pick') == 'self' else None
            on['with'] = [f for f in on.get('with', []) if f.get('attr') != 'card'] + [{'attr': 'card', 'op': 'in', 'refs': SETS[x.pop('card')]}]
            x['on'] = on; n += 1
        for f in x.get('with', []) if isinstance(x.get('with'), list) else []:
            if f.get('attr') == 'card' and f.get('ref') in SETS:
                f['op'] = 'in'; f['refs'] = SETS[f.pop('ref')]; n += 1
        for v in x.values(): n += walk(v)
    elif isinstance(x, list):
        for v in x: n += walk(v)
    return n


for p in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]
    n = 0
    for r in recs:
        n += walk(r.get('abilities', []))
        if r.get('id') in UNSURE and 'act' not in r.get('unsure', []): r['unsure'] = r.get('unsure', []) + ['act']; n += 1
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    if n: print(os.path.relpath(p, HERE), n, 'changed')
