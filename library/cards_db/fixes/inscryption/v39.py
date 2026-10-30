"""Inscryption records, 29 Oct 2026 (v39), from Claude's check of CHECK_20_inscryption.md against the texts; by rule, safe to run twice.
1. Burrower ("When an empty space would be struck, ... will move to that space"): the struck empty space is on its own side
   (an enemy strikes it), so the space is side mine.
2. "rotate one space clockwise" (Wiseclock): every unit moves to a bordering space (BRIEF "The board": bordering), the move
   had no place.
3. "it replaces all spaces on opponent's side of the board with itself ... clears all spaces" (The Moon, The Limoncello):
   it takes every space of its side, BRIEF "Room": stat_set size = the count of spaces of its side. Its side is mine:
   the behaviour page speaks as the player, and these giants are the opponent's own cards (Claude's reading)."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
text = {}
for f in glob.glob(os.path.join(HERE, 'input', 'inscryption', '*.jsonl')):
    for l in open(f):
        x = json.loads(l); text[x['id']] = ' '.join(x['text'].split()).lower()
for P in (os.path.join(HERE, 'read', 'inscryption', 'keywords.jsonl'), os.path.join(HERE, 'read', 'inscryption', 'batch_001.jsonl')):
    recs = [json.loads(l) for l in open(P)]; changed = 0
    for r in recs:
        t = text.get(r['id'], ''); before = json.dumps(r, sort_keys=True)
        for ab in r['abilities']:
            w = ab.get('when') or {}
            if 'when an empty space would be struck' in t and w.get('event') == 'strikes' and isinstance(w.get('object'), dict):
                w['object']['side'] = 'mine'
            for e in ab['do']:
                if re.search(r'rotate one space (?:counter-?)?clockwise', t) and e.get('act') == 'move' and not e.get('to'):
                    e['to'] = {'kind': 'position', 'with': [{'attr': 'position', 'op': 'is', 'val': 'bordering'}]}
        if "replaces all spaces on opponent's side of the board with itself" in t:
            room = {'when': {'event': 'played', 'object': {'pick': 'self'}}, 'do': [{'act': 'stat_set', 'on': {'pick': 'self'},
                    'params': {'size': {'x': 'count', 'of': {'kind': 'position', 'side': 'mine', 'zone': 'board'}}}, 'lasts': 'while'}]}
            if room not in r['abilities']: r['abilities'].append(room)
        changed += json.dumps(r, sort_keys=True) != before
    open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
    print(os.path.basename(P), changed, 'records changed')
