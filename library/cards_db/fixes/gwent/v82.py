"""Gwent, 6 Nov 2026 (v82, families 3, 4, 6 of checks/gwent/step2/families.md); safe to run twice.
- Family 4: "N adjacent units" gets position adjacent_group (kept n); Temple Guard and the Salamandra/Drummond reads too.
- Family 3: Leticia (turn_end, next_time, instead), Aen Elle (state applied_this_turn), Madame Luiza (this_round).
- Family 6: x unstated replaced by the new attr/x/span values."""
import glob, json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AG = {"attr": "position", "op": "is", "val": "adjacent_group"}
ME = {"kind": "player", "side": "mine"}


def walk(o, fn):
    if isinstance(o, dict):
        fn(o)
        for v in o.values(): walk(v, fn)
    elif isinstance(o, list):
        for v in o: walk(v, fn)


def armor(r):
    def f(d):
        if d.get('kind') == 'unit' and d.get('pick') == 'chosen' and d.get('n') == 3 and not d.get('with'):
            d['with'] = [AG]
    walk(r, f)


def fix(r, i):
    ab = r['abilities']
    if i in (756688, 756267, 756345):
        walk(r, lambda d: d.update({'with': [AG if x.get('val') == 'sides' and d.get('pick') == 'chosen' else x for x in d['with']]}) if isinstance(d.get('with'), list) and d.get('n') else None)
    elif i in (756516, 757222):
        walk(r, lambda d: d.update({'with': [AG]}) if d.get('n') == 3 and isinstance(d.get('with'), list) else None)
    elif i == 756912:
        walk(r, lambda d: d.update({'pick': 'chosen', 'n': 3, 'with': [AG]}) if d.get('kind') == 'unit' and d.get('side') == 'mine' and d.get('pick') == 'all' else None)
    elif i == 756952:
        armor(r)
    elif i == 757279:
        if ab[1]['do'][0].get('act') == 'give_ability': return True
        a = ab[1]['do'][0]; a['link'] = 'instead'
        ab[1]['do'] = [{"act": "give_ability", "on": {"pick": "self"}, "ability": {"when": {"event": "turn_end", "actor": ME}, "limit": "next_time", "do": [a]}, "lasts": "permanent"}]
    elif i == 757395:
        st = {"attr": "state", "op": "is", "val": "applied_this_turn"}
        walk(r, lambda d: d['with'].append(st) if d.get('kind') == 'position' and d.get('pick') == 'all' and st not in d['with'] else None)
    elif i == 756863:
        walk(r, lambda d: (d.update(lasts='this_round'), d.pop('limit', None)) if d.get('act') == 'cost_set' else None)
    elif i == 757296:
        walk(r, lambda d: d.update(turns={"x": "stat", "attr": "unused_provisions", "of": ME}) if d.get('turns') == {"x": "unstated"} else None)
    elif i == 756842:
        walk(r, lambda d: d.update(amount={"x": "stat", "attr": "distance_from_top", "of": {"kind": "card", "side": "mine", "pick": "chosen", "zone": "deck_top"}}) if d.get('amount') == {"x": "unstated"} else None)
    elif i == 756412:
        walk(r, lambda d: d.update(amount={"x": "stat", "attr": "rows_between", "of": {"kind": "unit", "side": "enemy", "pick": "chosen", "zone": "board"}}) if d.get('amount') == {"x": "unstated"} else None)
    elif i == 757405:
        walk(r, lambda d: d['strength'].pop('n', None) if isinstance(d.get('strength'), dict) and d['strength'].get('attr') == 'provisions_below_limit' else None)
        walk(r, lambda d: d.update(strength={"x": "stat", "attr": "provisions_below_limit", "of": {"kind": "unit", "side": "enemy", "pick": "chosen", "n": 3, "zone": "deck"}}) if d.get('strength') == {"x": "unstated"} else None)
    elif i == 757394:
        walk(r, lambda d: d.update(strength={"x": "event_total", "event": {"event": "damaged", "object": {"kind": "unit", "with": [{"attr": "keyword", "op": "is", "ref": "Frost"}]}}, "span": "last_5_enemy_turns"}) if d.get('strength') == {"x": "unstated"} else None)
        walk(r, lambda d: (d['strength'].pop('turns', None), d['strength'].update(span='last_5_enemy_turns')) if isinstance(d.get('strength'), dict) and d['strength'].get('span') == 'last_enemy_turns' else None)
        walk(r, lambda d: d['strength']['event'].update({'object': {'kind': 'unit', 'with': d['strength']['event'].pop('with')}}) if isinstance(d.get('strength'), dict) and 'with' in d['strength'].get('event', {}) else None)
    else: return False
    r.pop('unsure', None) if i in (757296, 756842, 756412, 757405, 757394) else None
    return True


IDS = {756688, 756267, 756345, 756516, 757222, 756912, 756952, 757279, 757395, 756863, 757296, 756842, 756412, 757405, 757394}


def main():
    for path in sorted(glob.glob(os.path.join(HERE, 'read', 'gwent', '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path or 'keywords' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            if r.get('id') in IDS and 'abilities' in r:
                before = json.dumps(r, sort_keys=True); fix(r, r['id']); n += before != json.dumps(r, sort_keys=True)
        if n: open(path, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
