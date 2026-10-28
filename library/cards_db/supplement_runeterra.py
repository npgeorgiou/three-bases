"""Runeterra cards the library lacks but card texts name (stubs), taken from Riot's own card data (Data Dragon JSON, mirrored
on GitHub: noxelisdev/LoR_DDragon_Set1 ... Set9, Set6cde, Set7b, file data/set<N>-en_us.json). Writes supplement/runeterra.jsonl
in the library's entities columns; ids from 900001 up, kept stable for entries already in the file.
Usage: supplement_runeterra.py <folder with set*.json> (fetch: git clone --depth 1 --filter=blob:none --no-checkout <repo>,
then git -C <clone> show HEAD:data/set<N>-en_us.json > set<N>.json)."""
import glob, json, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'supplement', 'runeterra.jsonl')
CAT = {'Unit': 'unit', 'Spell': 'spell', 'Landmark': 'building', 'Equipment': 'item', 'Ability': 'ability', 'Trap': 'spell'}  # traps: as the library stores them (Poison Puffcap)


def entry(c):
    champ = c.get('supertype') == 'Champion'
    kws = [k for k in c['keywords'] if k != 'Missing Translation']
    text = (f"Keywords: {', '.join(kws)}. " if kws else '') + c['descriptionRaw']
    lv = c.get('levelupDescriptionRaw') or ''
    if lv and lv != 'Missing Translation': text += ' Level up: ' + lv
    stats = json.dumps({'power': c['attack'], 'health': c['health']}) if c['type'] == 'Unit' else None
    return {'game': 'runeterra', 'ext_id': c['cardCode'], 'name': c['name'],
            'category': 'hero' if champ and c['type'] == 'Unit' else CAT[c['type']],
            'source_type': ('Champion ' if champ else '') + c['type'] + ' (Riot Data Dragon, supplement)',
            'edition': c['set'], 'faction': c['regions'][0] if c['regions'] else None,
            'subtypes': json.dumps([c['spellSpeed'] + ' spell']) if c['type'] == 'Spell' and c['spellSpeed'] else
                        (json.dumps([s.title() for s in c['subtypes']]) if c.get('subtypes') else None),
            'rarity': c['rarity'].lower() if c['collectible'] else None, 'cost': f"{c['cost']} mana", 'cost_num': float(c['cost']),
            'stats': stats, 'text': text, 'extra': None, 'variants': None}


def main():
    riot = {}
    for f in glob.glob(os.path.join(sys.argv[1], 'set*.json')):
        for c in json.load(open(f)): riot.setdefault(c['name'].lower(), []).append(c)
    db = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
    stubs = sorted({n for (n,) in db.execute("select name from card where game='runeterra' and is_stub=1")})
    rows = [json.loads(l) for l in open(OUT)] if os.path.exists(OUT) else []
    old = {r['ext_id']: r['id'] for r in rows}; stubs = sorted(set(stubs) | {r['name'] for r in rows})
    nxt = max(list(old.values()) + [900000]) + 1; out = []
    for n in stubs:
        cs = riot.get(n.lower())
        if not cs: continue
        c = sorted(cs, key=lambda x: (not x['collectible'], x['cardCode']))[0]  # the collectible card if one is, else the first code
        if c['type'] not in CAT: continue
        e = entry(c); e['id'] = old.get(e['ext_id']) or nxt; nxt += e['id'] == nxt
        out.append(e)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w').write(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in sorted(out, key=lambda e: e['id'])))
    print(len(out), 'supplement cards;', len(stubs) - len(out), 'stubs not found in the Riot data')


main()
