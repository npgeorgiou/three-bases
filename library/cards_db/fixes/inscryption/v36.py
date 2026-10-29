"""Inscryption records, 29 Oct 2026 (v36), done by rule over the texts instead of a re-read; safe to run twice.
- "within a circuit completed by a card bearing this sigil": every target on my side (not the card itself) gets position
  in_circuit of the card (the readers had no value: proposal in_circuit, 10 records).
- "If a card bearing this sigil is within a circuit" / "is part of a completed circuit": the condition is the card itself in a
  circuit (count of self with position in_circuit >= 1), replacing the readers' placeholder "have self".
- "move in the direction inscribed": the space it moves to is position sides (its row's neighbour; proposal
  inscribed_direction, 5 records); cards "in the way" are on its sides too (not in_front / behind, a column's words).
- "a Green / Orange / Blue Gem is provided" (Great Mox: all three): when played, mana_gain on kind gem of that colour
  (proposal gem_provided, 5 records).
- "is healed" with no number: params amount x unstated."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
text = {}
for f in glob.glob(os.path.join(HERE, 'input', 'inscryption', '*.jsonl')):
    for l in open(f):
        x = json.loads(l); text[x['id']] = ' '.join(x['text'].split())
CIRC = {'attr': 'position', 'op': 'is', 'val': 'in_circuit', 'of': {'pick': 'self'}}
SELF_IN = {'test': 'count', 'of': {'pick': 'self', 'with': [{'attr': 'position', 'op': 'is', 'val': 'in_circuit'}]}, 'op': 'ge', 'n': 1}
SIDES = {'attr': 'position', 'op': 'is', 'val': 'sides'}


def rulebook(t):
    m = re.search(r'Rulebook: (.*?\.)(?: |$)', t)
    return (m.group(1) if m else t).lower()


def fix(r):
    t = text.get(r['id'], ''); rb = rulebook(t); low = t.lower(); done = set()
    for ab in r['abilities']:
        if re.search(r'\bif a card bearing this sigil is (?:within a circuit|part of a completed circuit)', rb):
            ab['if'] = [c for c in ab.get('if', []) if not (c.get('test') == 'have' and c.get('of') == {'pick': 'self'})]
            if SELF_IN not in ab['if']: ab['if'].append(SELF_IN)
            done |= {'if', 'position'}
        for e in ab['do']:
            if 'within a circuit completed by a card bearing this sigil' in rb:
                for k in ('on', 'to'):
                    tg = e.get(k)
                    if isinstance(tg, dict) and tg.get('pick') != 'self' and tg.get('kind') in ('unit', 'position'):
                        w = tg.setdefault('with', [])
                        if CIRC not in w: w.append(CIRC)
                        done.add('position')
            if 'direction inscribed' in low and e.get('act') == 'move':
                for k in ('on', 'to'):
                    tg = e.get(k) or {}
                    for f in tg.get('with', []):
                        if f.get('attr') == 'position' and f.get('val') in ('in_front', 'behind'): f['val'] = 'sides'
                to = e.get('to')
                if e.get('on') == {'pick': 'self'} and isinstance(to, dict) and to.get('kind') == 'position' and not to.get('with'):
                    to['with'] = [dict(SIDES)]
                done.add('to')
            if e.get('act') == 'heal' and not (e.get('params') or {}).get('amount') and re.search(r'\bhealed?\b', rb) and not re.search(r'\bheal(?:ed)? (?:by )?\d', rb):
                e['params'] = dict(e.get('params') or {}, amount={'x': 'unstated'}); done.add('params')
    gems = re.findall(r'\b(green|orange|blue)\b', rb) if re.search(r'gems? (?:is|are) provided', rb) and '(green, orange, or blue)' not in rb else []
    if gems:
        ab = {'when': {'event': 'played', 'object': {'pick': 'self'}}, 'do': []}
        for i, g in enumerate(dict.fromkeys(gems)):
            e = {'act': 'mana_gain', 'on': {'kind': 'gem', 'side': 'mine', 'with': [{'attr': 'region', 'op': 'is', 'val': g.capitalize()}]}, 'params': {'amount': 1}}
            if i: e['link'] = 'and'
            ab['do'].append(e)
        if ab not in r['abilities']: r['abilities'].insert(0, ab)
        done.add('act')
    if done and r.get('unsure'):
        r['unsure'] = [u for u in r['unsure'] if u not in done]
        if not r['unsure']: del r['unsure']


for P in glob.glob(os.path.join(HERE, 'read', 'inscryption', '*.jsonl')) + glob.glob(os.path.join(HERE, 'second', 'inscryption', '*.jsonl')):
    if P.endswith(('proposals.jsonl', 'rejected.jsonl')) or os.path.basename(P) in ('game_rules.jsonl', 'auto.jsonl'): continue
    recs = [json.loads(l) for l in open(P)]; changed = 0
    for r in recs:
        before = json.dumps(r, sort_keys=True); fix(r); changed += json.dumps(r, sort_keys=True) != before
    open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
    print(os.path.basename(P), changed, 'records changed')

# names.tsv for the keyword records too (run.py normalizes card batches only): Push / Pull are no Inscryption keywords,
# "a Pelt card" is the Pelts family, Nano Armor is Armored
import sys; sys.path.insert(0, HERE); import normalize
P = os.path.join(HERE, 'read', 'inscryption', 'keywords.jsonl'); table = normalize.names_table('inscryption')
recs = [json.loads(l) for l in open(P)]; before = json.dumps(recs)
for r in recs: normalize.fix_names(r, table)
open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
print('keywords.jsonl names', 'changed' if json.dumps(recs) != before else 'unchanged')

# second reading judged by Claude (compare.py): the kept reading is fixed where the second was right
# - event moves: the unit that moves is the object (vocab: "a unit is about to move"; Stormbound "moves, object self"); Sentry
#   had it as actor, and damaged "actor"
# - Boon of Goat's Blood: the Black Goat is placed on the player's side ("to" my side)
# - Bell Ringer: Power is the space number plus 1 per adjacent Chime: the Chimes add to it (stat_change), not set it
def moves_object(x):
    if isinstance(x, dict):
        w = x.get('when') or {}
        if w.get('event') == 'moves' and 'actor' in w and 'object' not in w:
            w['object'] = w.pop('actor')
            for e in x.get('do', []):
                if e.get('on') == {'pick': 'actor'}: e['on'] = {'pick': 'it'}
        for v in x.values(): moves_object(v)
    elif isinstance(x, list):
        for v in x: moves_object(v)

for P in (os.path.join(HERE, 'read', 'inscryption', 'keywords.jsonl'), os.path.join(HERE, 'read', 'inscryption', 'batch_001.jsonl')):
    recs = [json.loads(l) for l in open(P)]
    for r in recs:
        moves_object(r)
        name = text.get(r['id'], '')
        if 'Boon of Goat' in name or "Boon of Goat's Blood" in name:
            for ab in r['abilities']:
                for e in ab['do']:
                    if e.get('act') == 'summon' and e.get('card') == 'Black Goat': e.setdefault('to', {'kind': 'position', 'side': 'mine'})
        if name.startswith('The Bell Ringer symbol'):
            for ab in r['abilities']:
                for e in ab['do']:
                    if e.get('act') == 'stat_set': e['act'] = 'stat_change'; e['lasts'] = 'while'
            r['unsure'] = sorted(set(r.get('unsure', [])) | {'params'})  # the space number has no value
    open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
print('second reading fixes applied')

# giving up my own unit is act sacrifice (normalize N17; keyword records are not normalized): True Scholar

P = os.path.join(HERE, 'read', 'inscryption', 'keywords.jsonl'); recs = [json.loads(l) for l in open(P)]
inputs = {}
for l in open(os.path.join(HERE, 'input', 'inscryption', 'keywords.jsonl')): x = json.loads(l); inputs[x['id']] = x
for r in recs: normalize.sacrifice_form(r, inputs)
open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
print('sacrifice form applied to keywords')
