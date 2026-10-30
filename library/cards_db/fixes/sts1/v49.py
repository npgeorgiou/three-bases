"""Slay the Spire records, 30 Oct 2026 (v49): the readers' repeated proposals, fixed by rule over the texts; safe to run twice.
Each rule names the text it reads and the value it writes (vocab rows of v49):
- "Every N turns / times / time you play N Attacks" (op every_nth): the event_count COND takes op every (Happy Flower,
  Sundial, Nunchaku, Pen Nib, Ink Bottle, Incense Burner).
- "Orb slot(s)", "Potion slot(s)" (orb_slot, potion_slot): the target is `{"kind": "slot", "side": "mine"}` with the kind
  of slot as a keyword filter for Orbs; "for each orb slot" counts slots.
- "the last card played ... was an X", "the previous card played was X" (last_card_played): COND test last_card of the
  readers' filter (it_matches was the placeholder).
- "the enemy intends to attack" (intends_attack): COND have of the chosen enemy with state intends_attack.
- "Elite combats", "Boss and Elite combats" (elite_combat, elite_enemy): COND have of an enemy with state elite (or boss);
  "Enemies in Elite combats" filters the enemies.
- "Colorless" cards and potions (colorless, region Colorless, potion): the made card's filter region Colorless, or
  category item for potions.
- "Cannot be removed from your deck", "no escape from this Curse" (removed_from_deck): cant, params event
  removed_from_deck; "If transformed or removed from your deck" (Parasite): a second ability on removed_from_deck.
- "Block is not removed" (keyword_removed): cant, params event keyword_removed, on the player's Block.
- "unblocked (attack) damage" (unblocked_damage, unblocked): the damaged event's object gets state unblocked.
- What changes the run between fights (map, rest sites, shops, rewards, chests, Ascension levels; proposals run_modifier,
  map_rule, rest_site_rule, reward_rule, fight_reward, shop_rule, potion_rule, gold_rule, deck_add_choice, potion_slot ...):
  act run_rule on the player, replacing the readers' stand-ins (cant activated, empty abilities); its triggers ("whenever you
  rest", "enter a shop / rest site / room", "open a chest", "climb a floor") are event run_event.
- "Orb" alone ("for each Orb", "your next Orb") is no keyword: keyword in Lightning, Frost, Dark, Plasma.
- Shop prices ("discount on all products", "Merchant prices") are run rules, never card cost changes.
- A family by name that is exactly one card of the game ("Shivs") is that card (filter card), unless the text says
  "containing" (Strike Dummy: "Cards containing Strike").
- "all (your) Gold" (all_gold): amount x all_of.
- Channel / Evoke entries: the Orb's place is a slot, not a board space (orb_slot). An Orb entry ("Orb: Gains Block.") keeps
  its end-of-turn ability as its passive (trigger_orb_passive).
- "trigger the passive ability of (ALL / your next) Orb(s)" (trigger_orb_passive): act repeat on the Orbs."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'sts1'
text, name = {}, {}
for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
    for l in open(f):
        x = json.loads(l); text[x['id']] = ' '.join(x['text'].split()); name[x['id']] = x['name']
RUN_ACTS = {'run_modifier', 'map_rule', 'rest_site_rule', 'reward_rule', 'fight_reward', 'shop_rule', 'potion_rule', 'gold_rule',
            'deck_add_choice', 'potion_slot', 'card_reward_options', 'keep_rest', 'relic', 'hide_intents', 'special_relic',
            'offer_reward', 'book_relic', 'chance_combat', 'face_relic', 'reveal_boss', 'minigame', 'fight_boss', 'relic_exchange',
            'chance_relic', 'travel_to_boss', 'chance_win', 'chance_curse', 'store_card', 'random_result', 'escape_combat', 'shop_zone'}
RUN_EVENTS = {'rest_site_rule', 'enters_rest_site', 'enter_shop', 'climb_floor', 'enter_map_room', 'opens_chest'}
RUN_TEXT = re.compile(r'\b(?:rest site|rest\b|smith|shop|merchant|chest|card rewards?|map|floor|\?\s*rooms?|potion slots?|'
                      r'elites? drop|ascension|bosses?\b.*\brelic|obtain|upon pickup|pick up|gold)\b', re.I)
CARDS = {n for i, n in name.items()}
RUN_RULE = {'act': 'run_rule', 'on': {'kind': 'player', 'side': 'mine'}}
SLOT = {'kind': 'slot', 'side': 'mine'}


def proposals():
    out = {}
    for f in glob.glob(os.path.join(HERE, 'read', G, '*.proposals.jsonl')):
        for l in open(f):
            if l.strip():
                p = json.loads(l); out.setdefault(p['id'], []).append(p)
    return out


def walk(o, fn):
    if isinstance(o, dict):
        fn(o)
        for v in list(o.values()): walk(v, fn)
    elif isinstance(o, list):
        for v in o: walk(v, fn)


def fix(r, props):
    t = text.get(r['id'], ''); low = t.lower(); done = set(); needs = {str(p.get('need')) for p in props}
    abs_ = r['abilities']
    # every Nth
    if re.search(r'\bevery (?:\d+ (?:turns|times)|time you play \d+|\d+th\b)|\bwhenever you play \d+ cards\b', low):
        def f(o):
            if o.get('test') == 'event_count' and o.get('op') in ('ge', 'eq', 'every_nth'): o['op'] = 'every'
        walk(abs_, f); done |= {'op', 'every_nth'}
    # Orb / potion slots
    if re.search(r'\b(?:orb|potion) slots?\b', low):
        def f(o):
            for k in ('on', 'to', 'of'):
                tg = o.get(k)
                if isinstance(tg, dict) and any(w.get('ref') in ('Orb', 'Orb slot', 'Potion') for w in tg.get('with', [])):
                    o[k] = dict(SLOT)
        walk(abs_, f); done |= {'on', 'kind', 'amount', 'orb_slot', 'potion_slot'}
    # last card played
    if re.search(r'\b(?:last|previous) card played\b', low):
        def f(o):
            if o.get('test') in ('it_matches', 'last_card_played'): o['test'] = 'last_card'
        walk(abs_, f); done |= {'test', 'last_card_played'}
    # intends to attack
    if 'intends to attack' in low:
        for ab in abs_:
            for c in ab.get('if', []):
                if c.get('test') == 'have' and isinstance(c.get('of'), dict) and c['of'].get('side') == 'enemy':
                    w = c['of'].setdefault('with', [])
                    if {'attr': 'state', 'op': 'is', 'val': 'intends_attack'} not in w: w.append({'attr': 'state', 'op': 'is', 'val': 'intends_attack'})
        done |= {'if', 'intends_attack'}
    # Elite combats
    m = re.search(r'\b(boss and elite|elite) combats?\b', low)
    if m and 'enemies in elite combats' not in low and not re.search(r'elites? drop', low):
        vals = ['boss', 'elite'] if 'boss' in m.group(1) else ['elite']
        cond = {'test': 'have', 'of': {'kind': 'unit', 'side': 'enemy', 'with': [{'attr': 'state', 'op': 'in', 'vals': vals}]}, 'op': 'is'}
        for ab in abs_:
            if ab['when'].get('event') in ('turn_start', 'combat_start') and cond not in ab.setdefault('if', []): ab['if'].append(cond)
        done |= {'if', 'when', 'elite_combat', 'elite_enemy'}
    if 'enemies in elite combats' in low:
        def f(o):
            tg = o.get('on')
            if isinstance(tg, dict) and tg.get('side') == 'enemy':
                w = tg.setdefault('with', [])
                if {'attr': 'state', 'op': 'is', 'val': 'elite'} not in w: w.append({'attr': 'state', 'op': 'is', 'val': 'elite'})
        walk(abs_, f); done |= {'if', 'elite_combat'}
    # Colorless cards, potions
    if 'colorless' in low or re.search(r'\bpotions?\b', low):
        def f(o):
            if o.get('act') in ('create', 'choose_card') and isinstance(o.get('on'), dict):
                tg = o['on']; w0 = tg.get('with', [])
                potion = any(x.get('ref') == 'Potion' or x.get('val') == 'item' for x in w0) or (
                    not w0 and re.search(r'\bpotions?\b', low) and not re.search(r'\bcards?\b', low))
                w = [x for x in w0 if x.get('attr') not in ('region', 'category') and x.get('ref') != 'Potion']
                if 'colorless' in low and not potion: w.append({'attr': 'region', 'op': 'is', 'val': 'Colorless'})
                elif potion and o['act'] == 'create': w.append({'attr': 'category', 'op': 'is', 'val': 'item'})
                tg['with'] = w
                if not w: tg.pop('with')
        walk(abs_, f); done |= {'on', 'with', 'colorless', 'region Colorless', 'potion', 'None'}
    # cannot be removed from the deck
    if re.search(r'cannot be removed from your deck|no escape from this curse', low):
        def f(o):
            if o.get('act') == 'cant': o['params'] = {'event': 'removed_from_deck'}
        walk(abs_, f); done |= {'params', 'removed_from_deck'}
    if 'removed from your deck' in low and 'transformed' in low:
        for ab in list(abs_):
            if ab['when'].get('event') == 'transformed' and not any(a['when'].get('event') == 'removed_from_deck' for a in abs_):
                nb = json.loads(json.dumps(ab)); nb['when']['event'] = 'removed_from_deck'
                if nb not in abs_: abs_.append(nb)
        done |= {'when', 'removed_from_deck'}
    # Block is not removed
    if 'block is not removed' in low:
        def f(o):
            if o.get('act') == 'cant': o['params'] = {'event': 'keyword_removed'}
        walk(abs_, f); done |= {'params', 'keyword_removed'}
    # unblocked damage
    if 'unblocked' in low:
        for ab in abs_:
            w = ab['when']
            if w.get('event') == 'damaged':
                ob = w.setdefault('object', {})
                ww = ob.setdefault('with', [])
                if {'attr': 'state', 'op': 'is', 'val': 'unblocked'} not in ww: ww.append({'attr': 'state', 'op': 'is', 'val': 'unblocked'})
        done |= {'when', 'state', 'unblocked', 'unblocked_damage'}
    # "Orb" is no keyword: the four Orbs are ("for each Orb", "your next Orb", "Evoke all Orbs")
    def f(o):
        for w in o.get('with', []) if isinstance(o.get('with'), list) else []:
            if w.get('attr') == 'keyword' and w.get('ref') == 'Orb':
                w.pop('ref'); w['op'] = 'in'; w['refs'] = ['Lightning', 'Frost', 'Dark', 'Plasma']
    walk(abs_, f)
    # the passive ability of Orbs again
    if re.search(r'trigger the passive ability of', low):
        def f(o):
            if o.get('act') in ('trigger_orb_passive', 'give_keyword') and isinstance(o.get('on'), dict) and o['on'].get('kind') == 'keyword':
                o['act'] = 'repeat'; o.pop('keyword', None); o.pop('lasts', None)
        walk(abs_, f); done |= {'act', 'trigger_orb_passive'}
    # Channel / Evoke entries: an Orb goes into an empty Orb slot (the readers wrote a board space)
    if name.get(r['id']) in ('Channel', 'Evoke'):
        def f(o):
            for k in ('on', 'to', 'of'):
                tg = o.get(k)
                if isinstance(tg, dict) and tg.get('kind') == 'position': tg['kind'] = 'slot'
        walk(abs_, f); done |= {'kind', 'on', 'orb_slot'}
    # an Orb entry's passive is its end-of-turn ability (wiki Keywords: Orbs trigger at the end of your turn)
    if re.match(r'orb:', low) and any(ab['when'].get('event') == 'turn_end' for ab in abs_):
        done |= {'act', 'when', 'trigger_orb_passive'}
    # shop prices are no card costs ("50% discount on all products", "Merchant prices")
    if re.search(r'\b(?:merchant|discount|prices?|products?)\b', low):
        abs_[:] = [ab for ab in abs_ if not any(e.get('act') in ('cost_change', 'cost_set') for e in ab['do'])]
        if not any(e.get('act') == 'run_rule' for a in abs_ for e in a['do']): abs_.append({'when': {'event': 'always'}, 'do': [dict(RUN_RULE)]})
        done |= {'act', 'zone', 'shop_zone'}
    # a family by name that is one card ("Shivs deal 4 additional damage"): the card
    def f(o):
        for w in o.get('with', []) if isinstance(o.get('with'), list) else []:
            if w.get('attr') == 'name_has' and w.get('ref') in CARDS and 'containing' not in low:
                w['attr'] = 'card'
    walk(abs_, f)
    # rewards dropped after a fight ("Elites drop an additional relic") change the run, not the fight
    if re.search(r'\bdrops? an additional\b', low):
        abs_[:] = [{'when': {'event': 'always'}, 'do': [dict(RUN_RULE)]}]
        done |= {'when', 'do', 'elite_enemy', 'relic'}
    # all Gold
    if re.search(r'\ball (?:of )?(?:your )?gold\b', low):
        def f(o):
            if o.get('act') == 'gold_gain' and isinstance(o.get('params', {}).get('amount'), dict): o['params']['amount'] = {'x': 'all_of'}
        walk(abs_, f); done |= {'params', 'all_gold'}
    # "the number of Frost / Lightning Channeled this combat": the Orb used, as the readers wrote it (v52: Channel now makes it)
    # the run between fights
    if needs & RUN_ACTS or (not abs_ and (RUN_TEXT.search(t) or re.search(r'\b(?:drop|relic)\b', low))):
        abs_[:] = [ab for ab in abs_ if not any(e.get('act') == 'cant' and (e.get('params') or {}).get('event') == 'activated' for e in ab['do'])]
        ev = 'run_event' if needs & RUN_EVENTS else 'always'
        ab = {'when': {'event': ev}, 'do': [dict(RUN_RULE)]}
        if not any(e.get('act') == 'run_rule' for a in abs_ for e in a['do']): abs_.append(ab)
        done |= {'act', 'do', 'params'} | (needs & RUN_ACTS)
    if needs & RUN_EVENTS:
        for ab in abs_:
            if ab['when'].get('event') in ('always', 'activated', 'played') and not any(e.get('act') == 'run_rule' for e in ab['do']):
                ab['when'] = {'event': 'run_event'}
        done |= {'event', 'when'} | (needs & RUN_EVENTS)
    if r.get('unsure'):
        left = [p for p in props if str(p.get('need')) not in done and p.get('field') not in done]
        r['unsure'] = sorted({p.get('field') for p in left if p.get('field')})
        if not r['unsure']: r.pop('unsure')
    return done


def main():
    props = proposals(); n = 0; solved = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
        b = os.path.basename(f)
        if b.endswith(('proposals.jsonl', 'rejected.jsonl')) or b in ('auto.jsonl', 'game_rules.jsonl'): continue
        recs = [json.loads(l) for l in open(f) if l.strip()]
        for r in recs:
            before = json.dumps(r, sort_keys=True)
            solved[r['id']] = fix(r, props.get(r['id'], []))
            n += json.dumps(r, sort_keys=True) != before
        open(f, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
    for f in glob.glob(os.path.join(HERE, 'read', G, '*.proposals.jsonl')):
        ps = [json.loads(l) for l in open(f) if l.strip()]
        keep = [p for p in ps if str(p.get('need')) not in solved.get(p['id'], set())]
        open(f, 'w').write(''.join(json.dumps(p, ensure_ascii=False) + '\n' for p in keep))
    print(f'{n} records changed')


main()
