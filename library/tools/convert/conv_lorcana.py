"""Disney Lorcana -> two load files (format in load_cards.py): keywords and classifications first, then the cards.
Source: the SQLite file in the npm package lorcana-oracle (dist/data/lorcana.sqlite), built from LorcanaJSON (lorcanajson.org):
sets 1-12 and Illumineer's Quest Q1-Q2 (set 12 incomplete, 13-14 not yet in it; package 0.1.2).
- One entry per card: reprints (reprint_of_id) and alternate printings (base_id: enchanted, epic, iconic) are left out.
- Ability names (the capitalised titles before an ability, flavour only) go to extra.ability_names, not the text, so the
  wording patterns do not read them; each ability keeps its own line.
- Text: the card's full text with its line wrapping undone (a line break is kept where a line ends a sentence or reminder text
  and the next starts with a keyword, an ability name in capitals or a bullet) and the game's icons written as words: ¤ strength, ⛉ willpower, ◊ lore, ⟳ exert, ⬡ ink, ◉ inkwell symbol.
- Keywords from the source's keyword field; a keyword's definition is its reminder text as the cards print it (the most common
  wording, numbers written as N, a character's name as <name>). Patterns read the text without reminder text (_strip_reminder), as for Magic.
- Classifications (Storyborn, Hero, Villain, Song ...) become tribe entries, so cards that care about one are linked.
- Data rules (method data_rule): a location holds a zone (zone_control); a song can be sung instead of paid for (cost_type).
- Category: Character unit, Action spell (songs too), Item item, Location building. Faction: the ink colour (dual-ink cards
  'Amber-Steel'); Illumineer's Quest boss cards have none.
Usage: conv_lorcana.py <lorcana.sqlite> <out_dir>"""
import collections, json, os, re, sqlite3, sys
src, out = sys.argv[1:3]
c = sqlite3.connect(src); q = lambda s, *a: c.execute(s, a).fetchall()
ICON = {'¤': 'strength', '⛉': 'willpower', '◊': 'lore', '⟳': 'exert', '⬡': 'ink', '◉': 'inkwell symbol'}
CAT = {'Character': 'unit', 'Action': 'spell', 'Item': 'item', 'Location': 'building'}
sets = {k: n for k, n in q('SELECT code, name FROM sets')}
rows = q('''SELECT id, full_name, type, color, cost, inkwell, strength, willpower, lore, move_cost, rarity, number, set_code,
            full_text, subtypes, keyword_abilities FROM cards WHERE reprint_of_id IS NULL AND base_id IS NULL ORDER BY id''')
kwnames = sorted({k for r in rows for k in json.loads(r[15] or '[]')}, key=len, reverse=True)
ANAME = re.compile(r"^((?=[^a-z]*[A-Z]{2})[A-Z0-9][A-Z0-9'’!?,.&:-]*(?: [A-Z0-9][A-Z0-9'’!?,.&:-]*)*) (?=\S)")   # an ability name: capitals, one word of 2+ letters
START = re.compile(r'^(?:' + '|'.join(re.escape(k) for k in kwnames) + r')\b|^•') 

def split_name(ln):
    m = ANAME.match(ln)
    return (m.group(1), ln[m.end():]) if m else (None, ln)

def clean(t):
    lines = (t or '').split('\n'); res = []
    for ln in lines:
        if res and not (res[-1].rstrip().endswith(('.', ')', '!', '?')) and (START.match(ln) or ANAME.match(ln))): res[-1] += ' ' + ln
        else: res.append(ln)
    names = []
    for j, ln in enumerate(res):
        nm, rest = split_name(ln)
        if nm: names.append(nm); res[j] = rest
    t = '\n'.join(res)
    for k, v in ICON.items(): t = t.replace(' ' + k, ' ' + v).replace(k, v)
    return re.sub(r'[ \t]+', ' ', t).strip(), names

# keyword definitions from the printed reminder text
rem = collections.defaultdict(collections.Counter)
cards = []
for (i, name, typ, color, cost, ink, s, w, lore, mv, rar, num, sc, text, sub, kws) in rows:
    t, names = clean(text); kl = json.loads(kws or '[]')
    for k in kl:
        m = re.search(r'(?:^|\n)' + re.escape(k) + r'(?: \+?\d+)?(?: [^\n(]{0,40})? \(([^)]*)\)', t)
        if m: rem[k][re.sub(r'named [^.]+\.', 'named <name>.', re.sub(r'\d+', 'N', m.group(1)))] += 1
    stats = {k: v for k, v in [('strength', s), ('willpower', w), ('lore', lore), ('move_cost', mv)] if v is not None}
    cards.append({'ext_id': str(i), 'name': name, 'category': CAT[typ], 'source_type': typ.lower(), 'edition': sets.get(sc, sc),
                  'faction': color or None, 'subtypes': json.loads(sub or '[]'), 'rarity': rar, 'cost': cost, 'stats': stats or None,
                  'text': t, 'keywords': kl,
                  'tags': ([('zone_control', 'does', 'data: a location (characters move here; it gives lore)')] if typ == 'Location' else []) +
                          ([('cost_type', 'does', 'data: a song (a character can exert to sing it instead of paying ink)')] if 'Song' in json.loads(sub or '[]') else []),
                  'extra': {'set': sc, 'number': num, 'inkwell': bool(ink), **({'ability_names': names} if names else {})}})
kw = [{'ext_id': 'kw:' + k, 'name': k, 'category': 'keyword', 'source_type': 'keyword',
       'text': (rem[k].most_common(1)[0][0] if rem[k] else None)} for k in sorted(kwnames)]
tribes = collections.Counter(s for cd in cards for s in cd['subtypes'])
tr = [{'ext_id': 'type:' + t, 'name': t, 'category': 'tribe', 'source_type': 'card type / tribe', 'text': f'{t}: {n} entities of this type.'}
      for t, n in sorted(tribes.items())]
game = {'id': 'lorcana', 'name': 'Disney Lorcana', 'family': 'Disney Lorcana', 'edition': 'sets 1-12 (12 incomplete) and Illumineer\'s Quest Q1-Q2',
        'source': 'LorcanaJSON (lorcanajson.org), as bundled in the npm package lorcana-oracle 0.1.2',
        'structure': 'Two-player card game; ink (any card with the inkwell symbol can be put face down as ink, one per turn) pays for cards; '
                     'characters quest for lore (first to 20 wins) or challenge exerted opposing characters; songs can be sung by exerting a '
                     'character instead of paying; locations give lore each turn and characters move to them by paying their move cost.',
        'notes': 'Keyword definitions are the reminder text the cards print. Reprints and alternate printings left out.'}
src_note = 'LorcanaJSON via npm lorcana-oracle 0.1.2'
os.makedirs(out, exist_ok=True)
json.dump({'_source': src_note, '_tag': 'lorcana_kw', '_game': game, 'cards': kw + tr}, open(os.path.join(out, 'lorcana_keywords.json'), 'w'), ensure_ascii=False, indent=0)
json.dump({'_source': src_note, '_tag': 'lorcana', '_strip_reminder': True, '_keywords_from_field': True, 'cards': cards},
          open(os.path.join(out, 'lorcana_cards.json'), 'w'), ensure_ascii=False, indent=0)
print('cards', len(cards), 'keywords', len(kw), 'without definition', [k['name'] for k in kw if not k['text']], 'tribes', len(tr))
