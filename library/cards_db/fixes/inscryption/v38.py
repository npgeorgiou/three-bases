"""Inscryption records, 29 Oct 2026 (v38), from deck_read_inscryption.md; by rule over the sigil texts, safe to run twice.
1. A strike into an empty opposing space hits the opponent (wiki Card Battle: "cards striking empty board spaces" tip the
   scale; Omni Strike: "It will strike directly if no creatures oppose it"): every strike a sigil aims at opposing spaces
   (Bifurcated, Trifurcated, Trifurcated When Powered, Sniper) also strikes the enemy player, link or. Double Strike
   ("strike the opposing space an extra time") is a second strike there, not Runeterra's double_strike (strike first and
   together).
2. Board forms (BRIEF "The board"): "moves towards them" (Clinger) = to the sides of them; "moves to the right" (Loose Tail)
   = to its sides; "pushing any cards in the way" (Hefty) = the units on its sides move too; "moves into the space
   opposing" (Sentry) = moves_onto with the mover as object and same_space of the opposing space.
3. Deck conditions: Finical Hatchling hatches when drawn if Power and Health 1 to 5 and every tribe are in the deck: one
   count per number and per tribe (the six tribes of the wiki's Amalgam).
4. "Within a circuit": a circuit is two conduit cards on the same side (wiki Circuits), so the condition also counts two
   Conduit Cards of mine."""
import json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(HERE, 'read', 'inscryption', 'keywords.jsonl')
text = {}
for l in open(os.path.join(HERE, 'input', 'inscryption', 'keywords.jsonl')):
    x = json.loads(l); text[x['id']] = (x['name'], ' '.join(x['text'].split()))
PLAYER = {'act': 'strike', 'on': {'pick': 'self'}, 'to': {'kind': 'player', 'side': 'enemy'}, 'link': 'or'}
OPPOSING = {'kind': 'unit', 'side': 'enemy', 'zone': 'board', 'with': [{'attr': 'position', 'op': 'is', 'val': 'same_lane'}]}
SIDES = {'attr': 'position', 'op': 'is', 'val': 'sides'}
TRIBES = ['Avian', 'Canine', 'Hooved', 'Reptile', 'Insect', 'Squirrel']
CONDUITS = {'test': 'count', 'of': {'kind': 'unit', 'side': 'mine', 'zone': 'board', 'with': [{'attr': 'type', 'op': 'is', 'ref': 'Conduit Card'}]},
            'op': 'ge', 'n': 2}


def deck_count(f):
    return {'test': 'count', 'of': {'kind': 'unit', 'side': 'mine', 'zone': 'deck', 'with': [f]}, 'op': 'ge', 'n': 1}


recs = [json.loads(l) for l in open(P)]; changed = 0
for r in recs:
    name, t = text.get(r['id'], ('', '')); low = t.lower(); before = json.dumps(r, sort_keys=True)
    for ab in r['abilities']:
        do = ab['do']
        if re.search(r'strike each opposing space|which opposing space', low) and any(e.get('act') == 'strike' for e in do) \
           and not any(e.get('act') == 'strike' and (e.get('to') or {}).get('kind') == 'player' for e in do):
            do.append(dict(PLAYER))
        if name == 'Double Strike':
            ab['do'] = [{'act': 'strike', 'on': {'pick': 'self'}, 'to': dict(OPPOSING)}, dict(PLAYER)]
        if 'within a circuit' in low or 'part of a completed circuit' in low:
            if CONDUITS not in ab.setdefault('if', []): ab['if'].append(CONDUITS)
        for e in ab['do']:
            if name == 'Clinger' and e.get('act') == 'move':
                e['to'] = {'kind': 'position', 'with': [{'attr': 'position', 'op': 'is', 'val': 'sides', 'of': {'pick': 'it'}}]}
            if name == 'Loose Tail' and e.get('act') == 'move':
                e['to'] = {'kind': 'position', 'with': [dict(SIDES)]}
        if name == 'Hefty' and not any(e.get('on', {}).get('pick') == 'all' for e in ab['do']):
            ab['do'].append({'act': 'move', 'on': {'kind': 'unit', 'pick': 'all', 'zone': 'board', 'with': [dict(SIDES)]},
                             'to': {'kind': 'position', 'with': [dict(SIDES)]}, 'link': 'and'})
        if name == 'Sentry' and ab['when'].get('event') == 'moves':
            ab['when'] = {'event': 'moves_onto', 'object': {'kind': 'unit', 'side': 'enemy', 'with': [{'attr': 'position', 'op': 'is',
                          'val': 'same_space', 'of': {'kind': 'position', 'side': 'enemy', 'with': [{'attr': 'position', 'op': 'is', 'val': 'same_lane'}]}}]}}
    if name == 'Finical Hatchling':
        conds = [deck_count({'attr': a, 'op': 'eq', 'n': n}) for a in ('power', 'health') for n in range(1, 6)]
        conds += [deck_count({'attr': 'type', 'op': 'is', 'ref': x}) for x in TRIBES]
        for ab in r['abilities']: ab['if'] = conds
    if name in ('Clinger', 'Loose Tail', 'Finical Hatchling') and r.get('unsure'):
        r['unsure'] = [u for u in r['unsure'] if u not in ('to', 'if')]
        if not r['unsure']: del r['unsure']
    changed += json.dumps(r, sort_keys=True) != before
open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
print(changed, 'records changed')
