"""Basic word checks against the records: plain wording that must show up somewhere in a card's record.
If a card's text says "Round Start:", some ability of it waits for round_start; if it says "Stun", some effect stuns; if it
names a keyword (outside its own Keywords field), the record links that keyword somewhere. Only unambiguous wording.
Usage: pattern_check.py <game> [--json out.json]   prints the cards that miss something (id, name, what is missing)."""
import glob, json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_input import KWFIELD
import source

# wording -> what must be in the record: ('event', value) | ('act', value) | ('cond_kw', keyword name)
TRIGGERS = [
    (r'\bround start\b', ('event', 'round_start')), (r'\bround end\b', ('event', 'round_end')),
    (r'(?:^|\. |: )play:', ('event', 'played')), (r'\bwhen i\'?m summoned\b', ('event', 'summoned')),
    (r'(?:^|\. |: )attack:', ('event', 'attacks')), (r'(?<!nexus )\bstrike:', ('event', 'strikes')),
    (r'\bnexus strike:', ('event', 'strikes_nexus')), (r'\blast breath:', ('event', 'dies')),
    (r'\blevel up:', ('act', 'level_up')), (r'\bcountdown \d+:', ('event', 'countdown_done')),
    (r'\bdaybreak:', ('cond_kw', 'Daybreak')), (r'\bnightfall:', ('cond_kw', 'Nightfall')), (r'\bplunder:', ('cond_kw', 'Plunder')),
    (r'\bflow:', ('cond_kw', 'Flow')), (r'\ballegiance:', ('cond_kw', 'Allegiance')), (r'\benlightened:', ('cond_kw', 'Enlightened')),
]
# a verb is satisfied by any of these values anywhere in the record (as an effect, or as the event the card waits for)
VERBS = [
    (r'\bstun', 'stun|stunned|given_keyword'), (r'\bdraw', 'draw|drawn'), (r'\bcreate', 'create|copy|created'),
    (r'\bsummon', 'summon|copy|summoned|revive'), (r'\bdeal\b|\bdamage', 'damage|damaged|survives_damage|nexus_damaged|excess_damage'),
    (r'\bheals?\b', 'heal|healed'), (r'\bkill', 'kill|killed|dies'), (r'\bobliterate', 'obliterate|obliterated|keyword_action'),
    (r'\bdiscard', 'discard|discarded'), (r'\bsilence', 'silence|keyword_action'), (r'\brecall', 'return_to_hand|keyword_action|recalled'),
]
# keywords that records say through an act or a value instead of a link to the keyword
KW_EQUIV = {'landmark': 'landmark', 'equipment': 'equipment|attach|attached_to|equipped', 'equip': 'attach|equipped|attached_to|equipment',
            'rally': 'gain_attack_token', 'advance': 'countdown_advance', 'behold': 'have', 'ephemeral': 'ephemeral',
            'fleeting': 'fleeting', 'capture': 'capture', 'frostbite': 'frostbitten', 'vulnerable': 'vulnerable'}

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
    c = source.lib()
    kwnames = {n.lower(): n for (n,) in c.execute("select name from entities where game=? and category='keyword'", (game,))}
    skipkw = {'play', 'attack', 'strike', 'round start', 'round end', 'last breath', 'level up', 'nexus strike', 'countdown',
              'burst', 'fast', 'slow', 'focus', 'skill', 'everywhere', 'weakest', 'strongest', 'attack strike', 'slay'}
    kwpat = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted(kwnames, key=len, reverse=True) if k not in skipkw) + r')\b')
    inputs = {}
    for f in glob.glob(os.path.join(HERE, 'input', game, 'batch_*.jsonl')):
        for l in open(f): x = json.loads(l); inputs[x['id']] = x
    recs = {}
    for f in glob.glob(os.path.join(HERE, 'read', game, 'batch_*.jsonl')):
        if 'proposals' in f: continue
        for l in open(f): r = json.loads(l); recs[r['id']] = r
    bad = {}
    for i, x in inputs.items():
        r = recs.get(i)
        if not r: continue
        t = ' '.join(x['text'].split()); m = KWFIELD.match(t); rest = (t[m.end():] if m else t).lower()
        for nm in sorted(x.get('names_in_text', []), key=len, reverse=True):  # words inside other cards' names do not count
            if nm.lower() not in kwnames: rest = rest.replace(nm.lower(), ' ')
        got = {'event': set(), 'act': set(), 'name': set(), 'value': set()}; walk(r, got)
        miss = []
        for p, (kind, val) in TRIGGERS:
            if re.search(p, rest):
                if kind == 'cond_kw' and val.lower() not in got['name']: miss.append('condition ' + val)
                elif kind in ('event', 'act') and val not in got[kind]: miss.append(f'{kind} {val}')
        for p, acts in VERBS:
            if re.search(p, rest) and not (set(acts.split('|')) & got['value']): miss.append('act ' + acts.split('|')[0])
        own = {k.lower() for k in x['keywords']}
        for k in set(kwpat.findall(rest)):
            if k in own or k in got['name'] or k in ('stun', 'recall', 'obliterate', 'silence'): continue
            if k in KW_EQUIV and set(KW_EQUIV[k].split('|')) & got['value']: continue
            miss.append('keyword ' + kwnames[k])
        if miss: bad[i] = {'name': x['name'], 'missing': sorted(set(miss))}
    for i, b in sorted(bad.items()): print(i, b['name'], '|', '; '.join(b['missing']))
    print(f'{len(bad)} of {len(recs)} cards miss something the plain wording requires')
    if '--json' in sys.argv: json.dump(bad, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=0)

if __name__ == '__main__':
    main()
