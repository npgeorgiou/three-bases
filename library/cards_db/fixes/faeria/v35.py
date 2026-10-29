"""All games, 29 Oct 2026 (v35), by rule; safe to run twice.
- A "used a keyword" trigger (event keyword_used) whose object names no keyword: the keyword the card's text names in its
  trigger ("If I'm Tossed", "Whenever you discover a Treasure") is added as a keyword filter on the object, so the trigger
  matches cards that use that keyword (Fugoro, Captain of the Gagana; Keelbreaker; Platewyrm Egg).
  Only when exactly one of the game's keywords appears in a trigger phrase.
- An ability given for the next time something happens "this turn" / "this round" ("The next creature you play this turn
  costs 4 faeria less", "the first creature summoned on it this turn"): the give_ability lasts this_round (Failed
  Experiment, Path to Paradise), when the record has no this_round anywhere.
- "Last Words - ... Summon this in a random space.": the card summons itself again when it dies (Annoying Gnat was read as
  moving when played).
- Faeria "this turn" is the span this_round (BRIEF Game words: Faeria), never this_turn ("this action"); "a creature that
  attacked a god this turn" is state struck_player_this_round, not attacked_this_round (The World's Tear)."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
TRIG = re.compile(r"\b(?:if i'm|when i'm|whenever you|when you|the first time you|each time you)\s+(\w+)", re.I)


def has_kw(t):
    return any(f.get('attr') == 'keyword' for f in (t or {}).get('with', []))


for game in ('runeterra', 'stormbound', 'monster_train', 'faeria'):
    text = {i: ' '.join((t or '').split()) for i, t in lib.execute('select id, text from entities where game=?', (game,))}
    kws = [n for (n,) in lib.execute("select name from entities where game=? and category='keyword'", (game,))]
    for p in sorted(glob.glob(os.path.join(HERE, 'read', game, 'batch_*.jsonl'))):
        recs = [json.loads(l) for l in open(p) if l.strip()]; n = 0
        for r in recs:
            words = [w.lower() for w in TRIG.findall(text.get(r.get('id'), ''))]
            hit = {k for k in kws for w in words if re.match(re.escape(k.lower().rstrip('es')), w)}
            if len(hit) != 1: continue
            for ab in r.get('abilities', []):
                ev = ab.get('when') or {}
                if ev.get('event') == 'keyword_used' and not has_kw(ev.get('object')):
                    ev.setdefault('object', {}).setdefault('with', []).append({'attr': 'keyword', 'op': 'is', 'ref': hit.pop()}); n += 1
                    break
        for r in recs:
            t = text.get(r.get('id'), '')
            if re.search(r'\bthis (?:turn|round)\b', t, re.I) and 'this_round' not in json.dumps(r):
                for ab in r.get('abilities', []):
                    for e in ab.get('do', []):
                        if e.get('act') == 'give_ability' and 'lasts' not in e: e['lasts'] = 'this_round'; n += 1
            if re.search(r'Last Words - [^.]*\. Summon this in a random space', t):
                name = lib.execute('select name from entities where id=?', (r['id'],)).fetchone()[0].strip()
                abs_ = r.get('abilities', [])
                lw = [ab for ab in abs_ if (ab.get('when') or {}).get('event') == 'dies' and ((ab['when'].get('object') or {}).get('pick') == 'self')]
                if lw and not any(e.get('act') == 'summon' for e in lw[0]['do']):
                    lw[0]['do'].append({'act': 'summon', 'card': name, 'to': {'kind': 'position', 'pick': 'random'}, 'link': 'then'})
                    r['abilities'] = [ab for ab in abs_ if not ((ab.get('when') or {}).get('event') == 'played' and ab.get('do') and
                                      all(e.get('act') == 'move' and (e.get('to') or {}).get('pick') == 'random' for e in ab['do']))]
                    n += 1
        if game == 'faeria':
            for r in recs:
                t = text.get(r.get('id'), ''); before = json.dumps(r)
                def walk(o):
                    if isinstance(o, dict):
                        if o.get('span') == 'this_turn': o['span'] = 'this_round'
                        if o.get('attr') == 'state' and o.get('val') == 'attacked_this_round' and re.search(r'attacked a god', t): o['val'] = 'struck_player_this_round'
                        for v in o.values(): walk(v)
                    elif isinstance(o, list):
                        for v in o: walk(v)
                walk(r)
                if json.dumps(r) != before: n += 1
        if n:
            open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs)); print(game, os.path.basename(p), n)
