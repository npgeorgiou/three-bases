"""Scryfall Oracle Cards bulk file (.json or .jsonl) -> load_cards.py JSON of Magic tokens and emblems with rules text
(vanilla tokens add no mechanic and are left out; so are bios, minigame and helper cards, bosses and events). Usage: conv_scryfall_tokens.py <oracle-cards> <out.json>"""
import json, re, sys, collections
src, out = sys.argv[1:3]
def rows(p):
    txt = open(p, encoding='utf-8').read().strip()
    if txt.startswith('['): yield from json.loads(txt); return
    for line in txt.splitlines():
        line = line.strip().rstrip(',')
        if line and line not in '[]': yield json.loads(line)
COL = {'W': 'White', 'U': 'Blue', 'B': 'Black', 'R': 'Red', 'G': 'Green'}
def cat(t):
    if 'Creature' in t: return 'unit'
    if 'Emblem' in t: return 'modifier'
    if 'Artifact' in t: return 'item'
    if 'Enchantment' in t: return 'modifier'
    if 'Land' in t: return 'terrain'
    return 'spell'
cards = []; C = collections.Counter()
for x in rows(src):
    if x.get('layout') not in ('token', 'double_faced_token', 'emblem'): continue
    faces = x.get('card_faces') or [x]
    text = ' // '.join(f"{f['name']}: {f.get('oracle_text','')}" for f in faces) if len(faces) > 1 else (x.get('oracle_text') or '')
    if not text.strip(): C['vanilla'] += 1; continue
    tl0 = x.get('type_line', '')
    if x.get('set_type') in ('memorabilia', 'minigame') or not re.match(r'(Token|Emblem|Creature|Artifact)\b', tl0): C['not a token (bios, minigame, helper cards, bosses, events)'] += 1; continue
    col = x.get('colors') or (faces[0].get('colors') or [])
    fac = 'Colorless' if not col else (COL[col[0]] if len(col) == 1 else 'Multicolor (' + ''.join(sorted(col)) + ')')
    tl = x.get('type_line', '')
    sub = tl.split('—', 1)[1].split() if '—' in tl else []
    st = {'power': x['power'], 'toughness': x['toughness']} if 'power' in x else None
    cards.append(dict(ext_id=x['oracle_id'], name=x['name'], category=cat(tl), source_type=tl, edition=x.get('set_name'), faction=fac,
                      subtypes=sub or None, rarity=x.get('rarity'), stats=st, text=text, keywords=x.get('keywords') or [], created=True,
                      extra={'layout': x['layout']}))
    C[x['layout']] += 1
json.dump({'_tag': 'scryfall_tokens', '_strip_reminder': True, '_keywords_from_field': True,
           '_source': 'Scryfall Oracle Cards bulk file of 11 Oct 2026: tokens and emblems with rules text', 'cards': cards}, open(out, 'w', encoding='utf-8'))
print(len(cards), dict(C))
