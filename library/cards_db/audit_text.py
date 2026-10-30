"""Compares every card's text with its rows by pattern, the same way in every game: a word in the text that its rows do not
show is a reading error (Make it Rain: "three enemies or the enemy Nexus" stored as enemy units only).
Usage: audit_text.py <game> [--list rule]   prints, per rule, how many cards break it and some names; run.py runs it.
A flag read and found right goes to audit_text_explained.tsv (game, card, rule, why); a wrong row is fixed by a rule script.
A rule is (name, text pattern, what the rows must have). Text is the card's own text without its Keywords field; a keyword entry's
rulebook line when it has one."""
import collections, glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); import source

PLAYER = {'runeterra': r'Nexus', 'stormbound': r'\bbase\b', 'monster_train': r'\bPyre\b', 'faeria': r"\b(?:gods?|opponent)\b(?!'s)", 'inscryption': r"\b(?:opponent|scale)\b(?!'s)", 'duelyst': r'\bGenerals?\b', 'into_the_breach': r'\b(?:Power Grid|Grid Power)\b'}


def parts(rec):
    """every target, effect and event of a record, flattened: (kind of object, the object)"""
    out = []
    def walk(o, key=''):
        if isinstance(o, dict):
            out.append((key, o))
            for k, v in o.items(): walk(v, k)
        elif isinstance(o, list):
            for v in o: walk(v, key)
    walk(rec)
    return out


def acts(rec): return {o['act'] for k, o in parts(rec) if 'act' in o}
def kinds(rec): return {o.get('kind') for k, o in parts(rec) if 'kind' in o}
def has(rec, key, val): return any(o.get(key) == val for k, o in parts(rec))
def words(rec): return json.dumps(rec)


def rules(game):
    pl = PLAYER[game]
    return [
        # a player named as what an effect or condition is about: some row is about a player
        ('player named', rf'(?:\b(?:enemy|your|both|the|a|opponent\'s)\s+(?:\w+\s+)?){pl}', lambda r: 'player' in kinds(r) or has(r, 'kind', 'any') or has(r, 'kind', 'anything') or has(r, 'event', 'strikes_nexus') or has(r, 'event', 'nexus_damaged') or has(r, 'val', 'struck_player_this_round')),
        ('deal damage', r'\b(?:deal|deals|dealt)\s+(?:\d|X\b|that much|damage|\w+ damage)', lambda r: acts(r) & {'damage', 'strike', 'keyword_action', 'excess_damage', 'negate_damage'} or 'damage' in words(r)),
        ('draw', r'\bdraw\s+(?!pile)(?:\d|a\b|an?\b|that|it|them|cards?|X|\w+\b(?! at))', lambda r: acts(r) & {'draw', 'keyword_action', 'put_on_top', 'steal'} or '"draw' in words(r)),
        ('create', r'\bcreate\b', lambda r: acts(r) & {'create', 'copy', 'keyword_action', 'choose_card', 'random_one', 'set_terrain'} or has(r, 'event', 'terrain_changed')),
        ('summon', r'(?<!you )\bsummon\s(?!effect)', lambda r: acts(r) & {'summon', 'copy', 'revive', 'play_card', 'transform', 'keyword_action', 'create'}),
        ('heal', r'\bheal\b|\brestore\s+\d', lambda r: acts(r) & {'heal', 'keyword_action'} or '"healed"' in words(r)),
        ('kill or destroy', r'(?<!you )(?<!or )\b(?:kill|destroy)\b(?!ed)', lambda r: acts(r) & {'kill', 'sacrifice', 'obliterate', 'keyword_action', 'strike', 'spend_mana', 'unequip', 'max_mana_change'} or '"killed"' in words(r) or '"dies"' in words(r)),
        ('discard', r'\bdiscard\b(?! pile)', lambda r: acts(r) & {'discard', 'keyword_action'} or 'discard' in words(r)),
        ('stat gift', r'\+\d+[|/]\+\d+|\bgive\s+[\d/]+\s+strength|\bgain\s+[\d/]+\s+strength|\+\d+ (?:Attack|Health)\b', lambda r: acts(r) & {'stat_change', 'grow', 'give_keyword', 'keyword_action', 'increase_effect'}),
        ('cost less', r'\bcosts?\s+[\dX]+\s+less|\breduce\s+(?:its|their|the)\s+cost|\bcost\s+-\d', lambda r: acts(r) & {'cost_change', 'cost_set'}),
        ('this round', r'\bthis round\b', lambda r: 'this_round' in words(r)),
        ('everywhere', r'\beverywhere\b', lambda r: 'everywhere' in words(r)),
        ('for each', r'\bfor each\b|\bper\b(?! turn| stack)', lambda r: re.search(r'"x": ?"(?!n")', words(r)) is not None or 'per_' in words(r) or 'times' in words(r)),
        ('random', r'\brandom', lambda r: 'random' in words(r) or 'spread' in words(r)),
        ('spells and Skills', r'spells?,?\s+(?:and|or)\s+skills?', lambda r: '"skill"' in words(r)),
        ('level up', r'\bLevel up:', lambda r: 'level_up' in acts(r)),
        # board words (Faeria lands, wells, adjacency); a game without them never matches
        ('this turn', r'\bthis turn\b', lambda r: 'this_round' in words(r) or 'this_turn' in words(r)),
        ('land act', r'\b(?:create|transform|destroy|move)\b[^.]{0,30}\b(?:lands?|forests?|lakes?|mountains?|deserts?|prairies?)\b', lambda r: acts(r) & {'set_terrain', 'move', 'steal'} or '"terrain"' in words(r)),
        ('adjacent', r'\badjacent\b', lambda r: '"bordering"' in words(r) or '"sides"' in words(r)),  # a hex board's neighbours, or a row's (Inscryption)
        ('harvest', r'(?<!can )(?<!can\'t )\bharvest(?:s|ed|ing)? (?:faeria|from|over)\b', lambda r: 'harvest' in words(r)),  # collecting from the board; Monster Train's "Harvest:" is a death trigger
        # grid words (Duelyst: "nearby" is the 8 spaces around); a game without them never matches
        ('nearby', r'\bnearby\b|\baround (?:it|this|your|the|an?)\b', lambda r: re.search(r'"(?:surrounding|area_3x3|bordering|diagonal)"', words(r))),
        ('stun', r'\bstun(?:s|ned)?\b', lambda r: 'Stun' in words(r) or 'stun' in acts(r) or '"stunned"' in words(r)),
        ('dispel', r'\bdispel', lambda r: 'silence' in acts(r) or 'Dispel' in words(r)),
        ('double', r'\bdouble\b(?! attack)', lambda r: re.search(r'event_amount|double|"x": ?"stat"|times|"x": ?"count"', words(r)) or acts(r) & {'repeat', 'copy'}),
    ] + ([('Rally', r'\bRally\b', lambda r: acts(r) & {'gain_attack_token', 'keyword_action'})] if game == 'runeterra' else [])  # Monster Train's Rally is a trigger


def main():
    game = sys.argv[1]; show = sys.argv[sys.argv.index('--list') + 1] if '--list' in sys.argv else None
    lib = source.lib()
    text = {i: (n.strip(), ' '.join((t or '').split())) for i, n, t in lib.execute("select id, name, text from entities where game=?", (game,))}
    # keyword entries too (v36: Inscryption's cards are only their sigils, so a misread sigil is every card's error); a keyword
    # whose entry has a rulebook line is checked on that line (wiki notes follow it)
    for i, (n, t) in list(text.items()):
        m = re.match(r'Rulebook:\s*(.*?\.)(?:\s|\||$)', t)
        if m: text[i] = (n, m.group(1))
    recs = {}
    for p in sorted(glob.glob(os.path.join(HERE, 'read', game, '*.jsonl'))):  # every record file load.py loads; one card can have several
        if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
        for l in open(p):
            if not l.strip(): continue
            r = json.loads(l)
            if 'id' not in r: continue
            recs.setdefault(r['id'], {'id': r['id'], 'abilities': []})['abilities'] += r.get('abilities', [])
            if r.get('trigger') or r.get('condition'): recs[r['id']]['says_by_form'] = True  # a trigger or condition keyword
    explained = {(r[1], r[2]) for r in (l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'audit_text_explained.tsv')))
                 if len(r) >= 4 and r[0] == game}  # (card, rule) read and explained: the rows say it another way, or nothing to write
    bad = collections.defaultdict(list)
    for i, r in recs.items():
        if i not in text or r.get('says_by_form'): continue  # trigger and condition keywords say it by their form
        n, t = text[i]
        t = re.sub(r'^Keywords:[^.]*\.\s*', '', t)
        for name, pat, ok in rules(game):
            if re.search(pat, t, re.I if name not in ('Rally', 'level up') else 0) and not ok(r) and (n, name) not in explained: bad[name].append((n, t))
    total = 0
    for name, *_ in rules(game):
        xs = bad.get(name, []); total += len(xs)
        print(f'{name}: {len(xs)}' + (f'  e.g. {", ".join(x[0] for x in xs[:4])}' if xs else ''))
        if show == name:
            for n, t in xs: print(f'    {n} | {t[:200]}')
    print(f'{game}: {total} text words without rows')


if __name__ == '__main__':
    main()
