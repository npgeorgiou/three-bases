"""Gwent, 6 Nov 2026 (v75, fix round after the readings); safe to run twice.
- A keyword alone in the text with its number ("Cooldown: 5", "Insanity.", "Charge: 1", "Counter: 6", "Timer 3") is the card
  having that keyword (BRIEF Game words: Gwent): an always ability with keyword_action of it on nothing or on itself becomes
  give_keyword on self, permanent, its number kept as params amount.
- A trigger written after its label ("Crew: Whenever you play a unit next to this card, ...") holds only while that label's
  condition is met: an ability whose card text has "Crew:" and whose trigger is a unit played next to it gets COND
  keyword_condition Crew when it has none (Raffard's Vengeance)."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'gwent'
OWN = {'Cooldown', 'Insanity', 'Charge', 'Counter', 'Timer', 'Banish'}


def own_keyword(ab):
    n = 0
    if ab.get('when', {}).get('event') != 'always': return 0
    for d in ab.get('do', []):
        if d.get('act') == 'keyword_action' and d.get('keyword') in OWN and d.get('on', {'pick': 'self'}) == {'pick': 'self'}:
            d['act'] = 'give_keyword'; d['on'] = {'pick': 'self'}; d['lasts'] = 'permanent'; n += 1
    return n


def crew(ab, text):
    if 'Crew:' not in text or any(c.get('ref') == 'Crew' for c in ab.get('if', [])): return 0
    obj = ab.get('when', {}).get('object') or {}
    if ab.get('when', {}).get('event') != 'played' or not any(w.get('val') == 'sides' for w in obj.get('with', [])): return 0
    ab.setdefault('if', []).append({'test': 'keyword_condition', 'ref': 'Crew'}); return 1


def main():
    inp = {}
    for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
        for l in open(f):
            x = json.loads(l)
            if 'id' in x: inp[x['id']] = x
    for path in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            text = (inp.get(r.get('id')) or {}).get('text') or ''
            for ab in r.get('abilities', []): n += own_keyword(ab) + crew(ab, text)
        if n: open(path, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
