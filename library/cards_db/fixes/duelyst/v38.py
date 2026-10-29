"""Duelyst, 29 Oct 2026 (v38 deck read, deck_read_duelyst.md), by rule; safe to run twice.
- The MECHAZ0R keyword (its entry says only "When MECHAZ0R is complete, lookout!") gets what the game's code does
  (open-duelyst app/sdk/playerModifiers/playerModifierMechazorBuildProgress.coffee: each piece adds 20%; when the pieces
  played reach 100% the card played deploys MECHAZ0R!): used as an action, if the MECHAZ0R progress used this game adds up to
  100 (five uses of 20%: the count of uses; Silica Weaver's 40% counts as one), summon MECHAZ0R! nearby. Written by Claude from the code; every piece then helps the others complete it.
- "a Spellsword" (Shidai Stormblossom, Petal Flurry) is one of the four Spellswords the game's code names for these cards
  (Murasame, Kiyomori, Tanahashi, Kotetsu; Cards.Spell.SpellSword1-4): create a random card that is one of them."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
ID = {n: i for i, n in lib.execute("select id, name from entities where game='duelyst'")}
MECH = {'abilities': [{'when': {'event': 'activated'}, 'if': [{'test': 'event_count', 'event': {'event': 'keyword_used', 'object': {
    'kind': 'keyword', 'with': [{'attr': 'keyword', 'op': 'is', 'ref': 'MECHAZ0R'}]}}, 'op': 'ge', 'n': 5,
    'span': 'this_game'}], 'do': [{'act': 'summon', 'card': 'MECHAZ0R!', 'to': {'kind': 'position', 'with': [
    {'attr': 'position', 'op': 'is', 'val': 'surrounding'}]}}]}]}
SWORDS = ['Murasame', 'Kiyomori', 'Tanahashi', 'Kotetsu']
for p in sorted(glob.glob(os.path.join(HERE, 'read', 'duelyst', '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]; n = 0
    for r in recs:
        before = json.dumps(r, sort_keys=True)
        if r.get('id') == ID['MECHAZ0R'] and p.endswith('keywords.jsonl'): r.clear(); r.update({'id': ID['MECHAZ0R'], **MECH})
        for a in r.get('abilities', []):
            for e in a.get('do', []):
                if e.get('card') == 'Spellsword':
                    e.pop('card'); e['on'] = {'kind': 'card', 'pick': 'random', 'with': [{'attr': 'card', 'op': 'in', 'refs': SWORDS}]}
                for f in (e.get('on') or {}).get('with', []):
                    if f.get('attr') == 'card' and f.get('ref') == 'Spellsword': f.pop('ref'); f['op'] = 'in'; f['refs'] = SWORDS
        n += json.dumps(r, sort_keys=True) != before
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), n, 'changed')
