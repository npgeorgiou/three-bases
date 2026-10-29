"""Inscryption: every card from the Inscryption fandom wiki's card boxes, and the sigils the library has no entry for.
Why: the library's 164 Inscryption units came from the same wiki but are not usable as cards: cards with the same text were
merged (Hawk, Raven, Sparrow and Mothman into Bat; Skeleton into Revenant), cards without sigils were dropped (Wolf, Coyote,
Grizzly, Stoat, Opossum ...), and a page's tabs were stored under the tab's label (Left, Right, Normal, Dormant, Base Form).
So every card is written here, and source.py FULL replaces all the library's Inscryption units and terrain with these.
Cards: library/tools/convert/inscryption_wiki_cards.jsonl (215 pages, the first {{Card}} box of every page in
Category:Cards plus Loose Tail, sha256 2e0d2c72...) and inscryption_wiki_cards_more.jsonl (the further boxes: Gem Vessels on
Empty Vessel, Act III Trees on Trees, sha256 3493c1ba...), read through the wiki's api.php in the built-in browser on
29 Oct 2026; each line has the page title, revision id, the page's act/faction/tribe categories and the box (images removed).
Rules for turning boxes into cards (Claude's, from the box layout):
- Every tab is a card. A tab named Act I/II/III, Kaycee's Mod or Menu Preview is a version of the same card (extra.versions),
  unless its cost type differs from the first tab's (Daus in Act III costs Energy): then it is its own card "<name> (<tab>)".
- A tab whose label is a state of the card (FORM_TABS: Left, Defense, Base Form, Dormant ...) is "<title> (<tab>)"; any other
  tab label is the card's name (Wolf Cub, Spore Mice, Sarcophagus). A tab with its own titleN uses that title.
- The same name from another page takes that page's title (Amalgam (Act II)); from the same page it is a version.
- Faction: the page's one faction category; with several, the tab's cost (Energy Technology, Mox Magick, Blood Beast, Bones
  Undead when the page is Undead and not Beast, else Beast); with none: the library's faction for the name, then the page's
  own words ("is a Technology card"), then the cost, then a Beast tribe category; else none.
- Terrain trait -> category terrain, else unit. Text: the sigils, a power icon the library defines (Ants) and traits it defines (Ant, Uncuttable) are the Keywords
  field ("Keywords: Ants, Ant Spawner, Ant."), so a card inherits its keywords' records; other traits follow ("Traits: Goat.").
- Links: a Fledgling (or Finical Hatchling) tab transforms_into the next tab of its page, or the first when it is last;
  Transformer and Swapper tabs transform into each other.
Not cards: Bottled Cards (an item; its tabs are the Squirrel, Black Goat, Frozen Opossum and Boulder cards), the Deathcard
page's portrait gallery tab. Tail (Loose Tail page): no title in the box; the page names it Tail and gives 0 Power, 2 Health.
Sigils: Great Mox and Kraken Waterborne have no library entry; Gemified (the Act III upgrade, wiki page Gemification) neither; Green, Orange and Blue Mox are the library's Mox Sigils entry,
one per colour (the names the cards use). Texts from the wiki pages Mox Sigils (rev 12604) and Waterborne (rev 12626).
Writes supplement/inscryption.jsonl and supplement/inscryption_links.jsonl; ids from 4000001 (source.py), kept stable.
Usage: supplement_inscryption.py"""
import json, os, re, sqlite3
HERE = os.path.dirname(os.path.abspath(__file__))
CONV = os.path.join(HERE, '..', 'tools', 'convert')
OUT = os.path.join(HERE, 'supplement', 'inscryption.jsonl')
LINKS = os.path.join(HERE, 'supplement', 'inscryption_links.jsonl')
LIB = os.path.join(HERE, '..', 'three-bases-library.sqlite')
SRC = 'Inscryption fandom wiki card box (inscryption.fandom.com, read 29 Oct 2026), supplement'
EDITIONS = {'Act I', 'Act II', 'Act III', "Kaycee's Mod", 'Menu Preview'}
FORM_TABS = {'Left', 'Right', 'Defense', 'Attack', 'Base Form', 'Beast Form', 'Dormant', 'Awakened', 'Undead',
             'Rabbit', 'Wolf', 'Golden', 'Emerald', 'Ruby', 'Sapphire'}
RENAME = {'Gem Vessels (Emerald)': 'Emerald Vessel', 'Gem Vessels (Ruby)': 'Ruby Vessel',
          'Gem Vessels (Sapphire)': 'Sapphire Vessel'}   # the wiki's redirects Emerald/Ruby/Sapphire Vessel -> Empty Vessel#Gem Vessels
SKIP_PAGES = {'Bottled Cards'}
SKIP_TABS = {('Deathcard', 'Deathcard portraits')}
FACTIONS = ['Beast', 'Undead', 'Technology', 'Magick']
TRIBES = {'Avian', 'Canine', 'Hooved', 'Insect', 'Reptile', 'Squirrel'}
OWN_WORDS = {"Goranj's Vessel": 'Technology', 'Gems Conduit': 'Technology', 'Mycobot': 'Technology', 'Librarian': 'Technology'}
SIGIL_NAMES = {'Green Mox', 'Orange Mox', 'Blue Mox', 'Great Mox', 'Kraken Waterborne'}
WIKI_SIGILS = [
    ('Green Mox', "Rulebook: When a card bearing this sigil is played, a Green Gem is provided to the owner. In Act III a Green "
                  "Mox on the board gives Gemified cards 2 Health.", 'Mox Sigils'),
    ('Orange Mox', "Rulebook: When a card bearing this sigil is played, an Orange Gem is provided to the owner. In Act III an "
                   "Orange Mox on the board gives Gemified cards 1 Power.", 'Mox Sigils'),
    ('Blue Mox', "Rulebook: When a card bearing this sigil is played, a Blue Gem is provided to the owner. In Act III a Blue Mox "
                 "on the board lowers Gemified cards' cost by 1 Energy.", 'Mox Sigils'),
    ('Great Mox', "Rulebook: When a card bearing this sigil is played, a Green, an Orange and a Blue Gem are provided to the owner "
                  "(it combines the effects of the other three Mox sigils).", 'Mox Sigils'),
    ('Kraken Waterborne', "Rulebook: A card bearing this sigil submerges during its opponent's turn: an opposing creature attacks "
                          "the space directly, skipping over it. When it re-emerges it transforms into a random Tentacle card "
                          "(Bell Tentacle, Hand Tentacle, Mirror Tentacle), losing this sigil and its other sigils.", 'Waterborne'),
    ('Gemified', "A card chosen at the Gemification event (Act III) is Gemified: it gains no sigil, but while its owner has a "
                 "Green Gem it has 2 more Health, with an Orange Gem 1 more Power, and with a Blue Gem it costs 1 Energy less.",
     'Gemification'),
]


def links_in(v):
    """[[A]] or [[A|B]] -> names: the link target for sigils (the library's entry names), the label otherwise."""
    return [(a, b or a) for a, b in re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', v or '')]


def plain(v):
    v = re.sub(r'<br\s*/?>', ', ', v or '')
    v = re.sub(r'\[\[(?:[^\]|]+\|)?([^\]]+)\]\]', r'\1', v)
    return re.sub(r'<[^>]+>', '', v).strip()


def tabs(box):
    """The box's fields per tab: {n: {field: value}}; a plain Card box is tab 1."""
    f = {}
    for k, v in re.findall(r'^\|([a-z_]+?\d*)\s*=(.*)$', box, re.M):
        m = re.match(r'([a-z_]+?)(\d*)$', k)
        f.setdefault(int(m.group(2) or 1), {})[m.group(1)] = v.strip().rstrip('}').strip()
    return f


def cost(v):
    v = plain(v)
    if not v: return None, None, None
    m = re.match(r'(\d+)\s*(Blood|Bones?|Energy)$', v)
    if m:
        kind = {'Bone': 'Bones'}.get(m.group(2), m.group(2))
        return f'{m.group(1)} {kind}', float(m.group(1)), kind
    if 'Mox' in v: return v, float(v.count('Mox')), 'Mox'
    return v, None, None


def faction(page, name, kind, libfac):
    fs = [x for x in FACTIONS if x in page['cats']]
    if len(fs) == 1: return fs[0]
    if len(fs) > 1:
        if kind == 'Energy' and 'Technology' in fs: return 'Technology'
        if kind == 'Mox' and 'Magick' in fs: return 'Magick'
        if kind == 'Bones' and 'Undead' in fs and 'Beast' not in fs: return 'Undead'
        return libfac.get(name) or ('Beast' if 'Beast' in fs else fs[0])
    if libfac.get(name): return libfac[name]
    if page['title'] in OWN_WORDS: return OWN_WORDS[page['title']]
    if kind == 'Energy': return 'Technology'
    if kind == 'Mox': return 'Magick'
    if kind in ('Blood', 'Bones') or TRIBES & set(page['cats']): return 'Beast'
    return None


def main():
    lib = sqlite3.connect(LIB)
    libfac = {}
    for n, f in lib.execute("select name, faction from entities where game='inscryption' and category in ('unit','terrain') "
                            "and faction is not null"):
        libfac.setdefault(n, f)
    kwname = {re.sub(r'\W', '', n.lower()): n for (n,) in lib.execute("select name from entities where game='inscryption' and category='keyword'")}
    libkw = {n.lower() for n in kwname.values()}
    kwname.update({re.sub(r'\W', '', n.lower()): n for n in SIGIL_NAMES})
    kwnames = {n.lower() for n in kwname.values()}
    canon = lambda n: kwname.get(re.sub(r'\W', '', n.lower()))
    pages = [json.loads(l) for l in open(os.path.join(CONV, 'inscryption_wiki_cards.jsonl'))]
    cats = {p['title']: p['cats'] for p in pages}
    pages += [dict(p, cats=cats[p['title']]) for p in map(json.loads, open(os.path.join(CONV, 'inscryption_wiki_cards_more.jsonl')))]
    cards, by_name, page_tabs = [], {}, []
    for p in pages:
        if p['title'] in SKIP_PAGES: continue
        T = tabs(p['b'])
        t1 = plain(T.get(1, {}).get('title')) or ('Tail' if p['title'] == 'Loose Tail' else p['title'])
        first_kind, made = None, []
        for n in sorted(T):
            f = T[n]
            tab = plain(f.get('tab')) or t1
            if (p['title'], tab) in SKIP_TABS: continue
            c, cnum, kind = cost(f.get('cost'))
            if n == min(T): first_kind = kind
            own = plain(f.get('title')) if n > 1 and f.get('title') else None
            if own and own != tab: name = f'{own} ({tab})'
            elif tab in EDITIONS or tab in (t1, 'Normal'): name = t1
            elif tab in FORM_TABS: name = f'{t1} ({tab})'
            else: name = tab
            name = RENAME.get(name, name)
            version = tab in EDITIONS and n > min(T)
            if version and kind != first_kind: name, version = f'{t1} ({tab})', False
            power, health = plain(f.get('power')), plain(f.get('health'))
            if p['title'] == 'Loose Tail': power = '0'
            sig = [a for a, b in links_in(f.get('sigils')) if a.lower() in kwnames or a in SIGIL_NAMES]
            sigtext = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', lambda m: m.group(1) if m.group(1) in sig else (m.group(2) or m.group(1)),
                             re.sub(r'<br\s*/?>', ', ', f.get('sigils') or ''))
            sigtext = re.sub(r'\s+([.,])', r'\1', re.sub(r'<[^>]+>', '', sigtext)).strip().rstrip('.')
            # traits: Terrain is the category, Mox Card a type; a trait the library defines as a keyword joins the Keywords field
            traits = [t.strip() for t in re.split(r',|<br\s*/?>', re.sub(r'\[\[(?:[^\]|]+\|)?([^\]]+)\]\]', r'\1', f.get('traits') or '')) if t.strip()]
            types = ['Mox Card'] if 'Mox Card' in traits else []
            terrain = 'Terrain' in traits
            kw_traits = [canon(t) for t in traits if canon(t)]
            traits = [t for t in traits if t not in ('Terrain', 'Mox Card') and not canon(t)]
            stats = {k: v for k, v in (('power', power), ('health', health)) if v}
            # the Keywords field: a power icon defined as a keyword, the sigils, keyword traits; sigil words that are no link
            # (Boulder "(In Kaycee's Mod)", Starvation "5th Starvation onward:") keep the sigils as text instead
            plain_sig = not re.sub(r'\[\[[^\]]+\]\]|,|<br\s*/?>|\s', '', f.get('sigils') or '')
            kws = ([canon(power)] if power and canon(power) else []) + ([canon(x) or x for x in sig] if plain_sig else []) + kw_traits
            parts = []
            if kws: parts.append('Keywords: ' + ', '.join(kws) + '.')
            if power and not re.fullmatch(r'\d+', power) and not canon(power): parts.append(f'Power: {power}.')
            if sigtext and not plain_sig: parts.append('Sigils: ' + sigtext + '.')
            if traits: parts.append('Traits: ' + ', '.join(traits) + '.')
            if f.get('description'): parts.append(plain(f['description']))
            acts = [x for x in p['cats'] if re.fullmatch(r"Act I{1,3}|Kaycee's Mod|Finale", x)]
            entry = {'game': 'inscryption', 'ext_id': None, 'name': name,
                     'category': 'terrain' if terrain else 'unit', 'source_type': f"card ({SRC}; page {p['title']} rev {p['rev']})",
                     'edition': ', '.join(acts) or None, 'faction': faction(p, name, kind, libfac),
                     'subtypes': json.dumps([t for t in re.findall(r'[A-Z][a-z]+', plain(f.get('tribe'))) if t in TRIBES] + types) if f.get('tribe') or types else None,
                     'rarity': 'Rare' if 'Rare' in (f.get('meta_categories') or '') else None,
                     'cost': c, 'cost_num': cnum,
                     'stats': json.dumps(stats) if stats else None, 'text': ' '.join(parts),
                     'extra': None, 'variants': None, '_asset': plain(f.get('asset_name')), '_sig': sig, '_page': p['title']}
            if name in by_name:
                prev = by_name[name]
                if version or prev['_page'] == p['title']:
                    ex = json.loads(prev['extra'] or '{}')
                    ex.setdefault('versions', []).append({'tab': tab, 'cost': c, 'stats': stats, 'text': entry['text']})
                    prev['extra'] = json.dumps(ex)
                    made.append(prev)
                    continue
                entry['name'] = name = p['title']
            by_name[name] = entry
            cards.append(entry)
            made.append(entry)
        page_tabs.append(made)
    # ext_id: the game's asset name, else the name; stable ids
    for e in cards:
        e['ext_id'] = 'wiki:' + (e['_asset'] or e['name'])
    old = {}
    if os.path.exists(OUT):
        old = {r['ext_id']: r['id'] for r in map(json.loads, open(OUT))}
    nxt = max(list(old.values()) + [4000000]) + 1
    sig = [{'game': 'inscryption', 'ext_id': 'wiki:sigil:' + n, 'name': n, 'category': 'keyword',
            'source_type': f'sigil (Inscryption fandom wiki page {pg}, read 29 Oct 2026, supplement)', 'edition': None,
            'faction': None, 'subtypes': None, 'rarity': None, 'cost': None, 'cost_num': None, 'stats': None, 'text': t,
            'extra': None, 'variants': None} for n, t, pg in WIKI_SIGILS if n.lower() not in libkw]
    out = cards + sig
    for e in out:
        e['id'] = old.get(e['ext_id']) or nxt
        nxt += e['id'] == nxt
    links = []
    for made in page_tabs:
        uniq = []
        for e in made:
            if e not in uniq: uniq.append(e)
        for i, e in enumerate(uniq):
            if {'Fledgling', 'Finical Hatchling'} & set(e['_sig']) and len(uniq) > 1:
                dst = uniq[i + 1] if i + 1 < len(uniq) else uniq[0]
                if dst is not e: links.append({'src': e['id'], 'rel': 'transforms_into', 'dst': dst['id'], 'evidence': 'wiki card page: grown form'})
            if {'Transformer', 'Swapper'} & set(e['_sig']):
                for d in uniq:
                    if d is not e and {'Transformer', 'Swapper'} & set(d['_sig']):
                        links.append({'src': e['id'], 'rel': 'transforms_into', 'dst': d['id'], 'evidence': 'wiki card page: other form'})
    with open(OUT, 'w') as f:
        for e in out:
            f.write(json.dumps({k: v for k, v in e.items() if not k.startswith('_')}, ensure_ascii=False) + '\n')
    with open(LINKS, 'w') as f:
        for l in links: f.write(json.dumps(l) + '\n')
    print('cards', len(cards), 'sigils', len(sig), 'links', len(links))


if __name__ == '__main__':
    main()
