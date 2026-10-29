"""Runeterra cards the library lacks (by card code and by name; stubs included), taken from Riot's own card data (Data Dragon JSON, mirrored
on GitHub: noxelisdev/LoR_DDragon_Set1 ... Set9, Set6cde, Set7b, file data/set<N>-en_us.json). Writes supplement/runeterra.jsonl
in the library's entities columns; ids from 900001 up, kept stable for entries already in the file.
Usage: supplement_runeterra.py <folder with set*.json> (fetch: git clone --depth 1 --filter=blob:none --no-checkout <repo>,
then git -C <clone> show HEAD:data/set<N>-en_us.json > set<N>.json; keywords: globals.json = core/data/globals-en_us.json of
InFinity54/LoR_DDragon)."""
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
    import source
    lib = source.lib()
    codes = {e.split(':')[-1] for (e,) in lib.execute("select ext_id from main.entities where game='runeterra'")}
    have = {n.lower() for (n,) in lib.execute("select name from main.entities where game='runeterra'")}
    stubs = {n for (n,) in db.execute("select name from card where game='runeterra' and is_stub=1")}
    stubs |= {cs[0]['name'] for cs in riot.values() if cs[0]['name'].lower() not in have and all(c['cardCode'] not in codes for c in cs)}
    stubs = sorted(stubs)
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
    # champions' level-up forms the library lacks (Riot: the non-collectible champion of the same name, code <base>T<n>), named and
    # coded like the library's ("Lucian (level 2)", ext_id lvl:<code>), and links: base transforms_into level form, generates
    # for every associated card Riot lists (the library has links for its own cards only)
    have_lvl = {e.split(':')[-1] for (e,) in lib.execute("select ext_id from main.entities where game='runeterra' and ext_id like 'lvl:%'")}
    code_id = {e.split(':')[-1]: i for i, e in lib.execute("select id, ext_id from main.entities where game='runeterra'")}
    code_id.update({e['ext_id']: e['id'] for e in out})
    for e in list(out):
        if not e['source_type'].startswith('Champion') or 'Level up:' not in e['text']: continue
        lv = [c for c in riot.get(e['name'].lower(), []) if not c['collectible'] and c['supertype'] == 'Champion' and c['type'] == 'Unit'
              and c['cardCode'].startswith(e['ext_id'] + 'T') and c['cardCode'] not in have_lvl]
        if not lv: continue
        x = entry(lv[0]); x['name'] = e['name'] + ' (level 2)'; x['ext_id'] = 'lvl:' + lv[0]['cardCode']
        x['id'] = old.get(x['ext_id']) or nxt; nxt += x['id'] == nxt
        out.append(x); code_id[lv[0]['cardCode']] = x['id']
    links = []
    for e in out:
        code = e['ext_id'].split(':')[-1]
        if e['ext_id'].startswith('lvl:'):
            base = code_id.get(code.split('T')[0])
            if base: links.append({'src': base, 'rel': 'transforms_into', 'dst': e['id'], 'evidence': 'Riot level-up form'})
        rc = next((c for cs in riot.values() for c in cs if c['cardCode'] == code), None)
        for ref in (rc or {}).get('associatedCardRefs', []):
            if ref in code_id and code_id[ref] != e['id']:
                links.append({'src': e['id'], 'rel': 'generates', 'dst': code_id[ref], 'evidence': 'Riot associatedCardRefs'})
    open(os.path.join(HERE, 'supplement', 'runeterra_links.jsonl'), 'w').write(''.join(json.dumps(l) + '\n' for l in links))
    # keywords the cards name that the library lacks, with Riot's own definition (globals-en_us.json keywords and vocabTerms)
    gpath = os.path.join(sys.argv[1], 'globals.json')
    if not os.path.exists(gpath): out += [r for r in rows if r['category'] == 'keyword']  # no glossary given: keep the keywords already taken
    else:
        g = json.load(open(gpath))
        terms = {k['name'].lower(): k for k in g['keywords'] + g['vocabTerms'] if k.get('description', '').strip()}
        oldk = {r['ext_id']: r['id'] for r in rows if r['category'] == 'keyword'}
        kstubs = {n for (n,) in db.execute("select name from card where game='runeterra' and is_stub=1 and is_keyword=1")}
        kstubs |= {r['name'] for r in rows if r['category'] == 'keyword'}
        for n in sorted(kstubs):
            k = terms.get(n.lower())
            if not k: continue
            code = 'keyword:' + k['nameRef']
            out.append({'id': oldk.get(code) or nxt, 'game': 'runeterra', 'ext_id': code, 'name': k['name'], 'category': 'keyword',
                        'source_type': 'keyword (Riot Data Dragon globals, supplement)', 'text': k['description']})
            nxt += out[-1]['id'] == nxt
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w').write(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in sorted(out, key=lambda e: e['id'])))
    print(len(out), 'supplement cards;', len(stubs) - len(out), 'stubs not found in the Riot data')


main()
