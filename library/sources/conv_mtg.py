"""MTGJSON AtomicCards.json -> load_cards.py JSON (Magic cards the library lacks). Usage: conv_mtg.py <AtomicCards.json> <db> <out.json>"""
import json, re, sqlite3, sys, collections
src, db, out = sys.argv[1:4]
D = json.load(open(src, encoding='utf-8'))['data']
c = sqlite3.connect(db)
have_names = {n for (n,) in c.execute("SELECT name FROM entities WHERE game='mtg'")}
have_ids = {e for (e,) in c.execute("SELECT ext_id FROM entities WHERE game='mtg'")}
merged = set()
try: merged = {n for (n,) in c.execute("SELECT name FROM merged_entities WHERE game='mtg'")}
except Exception: pass
UN = {'UGL', 'UNH', 'UST', 'UND', 'UNF', 'SUNF', 'UGH'}
SKIP_LAYOUT = {'planar', 'scheme', 'vanguard'}
SKIP_TYPE = {'Conspiracy', 'Plane', 'Phenomenon', 'Scheme', 'Vanguard', 'Dungeon', 'Emblem', 'Hero'}
TWO = ('standard', 'pioneer', 'modern', 'legacy', 'vintage', 'pauper')
drop = collections.Counter(); cards = []
def cat(types):
    t = set(types)
    if 'Creature' in t: return 'unit'
    if 'Planeswalker' in t: return 'hero'
    if 'Battle' in t: return 'building'
    if t & {'Instant', 'Sorcery'}: return 'spell'
    if 'Artifact' in t: return 'item'
    if 'Enchantment' in t: return 'modifier'
    if 'Land' in t: return 'terrain'
    return None
nr = lambda s: re.sub(r'\s*\([^()]*\)', '', s or '').strip()   # reminder text off, for the vanilla tests
for name, faces in D.items():
    f0 = faces[0]
    oid = f0.get('identifiers', {}).get('scryfallOracleId')
    if name in have_names or name in merged or oid in have_ids: drop['already in the library'] += 1; continue
    if f0.get('isFunny') or (set(f0.get('printings') or []) & UN and set(f0.get('printings') or []) <= UN | {'PLST', 'SLD', 'PLIST'}): drop['joke sets'] += 1; continue
    if any(re.search(p, x.get('text') or '') for x in faces for p in (r'\bsticker', r'\bAttraction', r'\{TK\}', r'\bdraft', r'outside the game this turn')) and set(f0.get('printings') or []) & (UN | {'CNS', 'CN2', 'CMB1', 'CMB2', 'MB2'}): drop['joke and draft-matters cards'] += 1; continue
    if set(f0.get('printings') or []) <= {'CMB1', 'CMB2', 'MB2'}: drop['playtest cards'] += 1; continue
    if f0.get('layout') in SKIP_LAYOUT or SKIP_TYPE & set(f0.get('types', [])): drop['non-playable (planes, schemes, vanguard, conspiracies, dungeons)'] += 1; continue
    texts = [(f.get('faceName') or f['name'], f.get('text') or '') for f in faces]
    if not any(t for _, t in texts): drop['no rules text'] += 1; continue
    types = f0.get('types', [])
    k = cat(types)
    if k == 'terrain' and 'Creature' not in types and len(faces) == 1: drop['non-creature lands'] += 1; continue
    if k is None: drop['other types'] += 1; continue
    kws = set(f0.get('keywords') or [])
    body = nr(texts[0][1])
    if k == 'unit' and len(faces) == 1 and body and all(all(p.strip().split(' ')[0].rstrip(',') in kws or p.strip() in kws or re.sub(r'\s*[\d{].*$', '', p.strip()) in kws for p in re.split(r',|;', line) if p.strip()) for line in body.split('\n')):
        drop['keyword-only creatures'] += 1; continue
    if len(faces) == 1 and body and all(re.fullmatch(r'\{T\}(, [^:]+)?: Add [^.]+\.?', l.strip()) for l in body.split('\n')):
        drop['mana-only cards'] += 1; continue
    lg = f0.get('legalities') or {}
    fmt = 'Commander products (not legal in a two-player constructed format)' if lg.get('commander') and not any(lg.get(x) for x in TWO) else None
    if len(faces) > 1:
        text = ' // '.join(f'{a}: {b}' for a, b in texts)
        st = ' // '.join(f['type'] for f in faces)
        costs = [f.get('manaCost') for f in faces if f.get('manaCost')]
        cost = ' // '.join(costs) if costs else None
        sub = []
        for i, f in enumerate(faces):
            if i: sub.append('//')
            sub += f.get('subtypes', [])
    else:
        text, st, cost, sub = texts[0][1], f0['type'], f0.get('manaCost'), f0.get('subtypes', [])
    col = f0.get('colors') or []
    fac = 'Colorless' if not col else ({'W': 'White', 'U': 'Blue', 'B': 'Black', 'R': 'Red', 'G': 'Green'}[col[0]] if len(col) == 1 else 'Multicolor (' + ''.join(sorted(col)) + ')')
    stats = {'power': f0['power'], 'toughness': f0['toughness']} if 'power' in f0 else None
    pr = f0.get('printings') or []
    extra = {'printings': pr}
    if fmt: extra['format'] = fmt
    if lg.get('pauper'): extra['printed_at_common'] = True
    cards.append(dict(ext_id=oid or name, name=name, category=k, source_type=st, edition=None, faction=fac,
                      subtypes=[s for s in sub if s] or None, rarity='common' if lg.get('pauper') else None, cost=cost,
                      cost_num=f0.get('manaValue'), stats=stats, text=text, extra=extra, keywords=sorted(kws)))
json.dump({'_tag': 'mtgjson', '_source': 'MTGJSON AtomicCards.json 5.3.0+20261011: cards the library lacked (commons, Commander-product cards, cards the first build dropped). Set codes of all printings in extra.printings (AtomicCards has no set names); rarity = common when the card is Pauper-legal (AtomicCards has no rarity).', 'cards': cards}, open(out, 'w', encoding='utf-8'))
print(len(cards), dict(drop), collections.Counter(x['category'] for x in cards), sum(1 for x in cards if x['extra'].get('format')))
