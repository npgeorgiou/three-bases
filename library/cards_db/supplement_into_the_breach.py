"""Into the Breach: every mech, weapon, passive and pilot, and the units the weapons put on the board, from the wiki's own
tables (supplement/into_the_breach_wiki.txt, copied 30 Oct 2026 from intothebreach.fandom.com pages Weapons, Passives, Mechs
and Pilots through api.php; each table checked against the page by length and SHA-256). The library had 38 of 43 mechs,
97 weapons without the Advanced Edition ones, 15 of 17 passives and 17 of 20 pilots, and its texts mixed page fragments
("Class: Any. Availability:"), so this supplement holds all of them (source.py FULL replaces the library's unit, ability,
item and hero entries). Tokens (Walking Bomb, Arachnoid, the four deployed tanks) come from the weapon pages' unit boxes.
A mech's text holds its starting weapons and passive in full: a squad (3 mechs) is the deck, so what a mech does is what
its loadout does. Run: python3 supplement_into_the_breach.py"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'supplement', 'into_the_breach_wiki.txt')
OUT = os.path.join(HERE, 'supplement', 'into_the_breach.jsonl')
LINKS = os.path.join(HERE, 'supplement', 'into_the_breach_links.jsonl')
G = 'into_the_breach'
SOURCE = 'intothebreach.fandom.com %s table, 30 Oct 2026 (supplement)'
POWER = re.compile(r'^(Free|\((\d)\)|Kill)$')
# a mech's weapon templates in the Mechs table name the weapon by its debug name; these differ from the Weapons table's
TEMPLATE = {'Brute_APCannon': 'AP Cannon', 'Ranged_BombDispenser': 'Bomb Dispenser', 'Science_ForceSwap': 'Force Swap',
            'Brute_RicochetRocket': 'Ricochet Rocket', 'Ranged_ArachnoidsInjector': 'Arachnoid Injector',
            'Science_AreaShift': 'Area Shift', 'Brute_ReverseThrusters': 'Reverse Thrusters',
            'Ranged_SmolderingShells': 'Smoldering Shells', 'Passive_NanofilterMending': 'Nanofilter Mending',
            'Science_ControlShot': 'Control Shot', 'Prime_ThermalDischarger': 'Thermal Discharger',
            'Brute_QuickFireRockets': 'Quick-Fire Rockets', 'Science_FirestormGenerator': 'Firestorm Generator',
            'Passive_HeatEngines': 'Heat Engines', 'Prime_HydraulicLifter': 'Hydraulic Lifter', 'Ranged_TriRocket': 'Tri-Rocket',
            'Science_SeismicCapacitor': 'Seismic Capacitor'}
# Mechs table "special" templates: Flying and Armored are the game's keywords Flying and Natural Armor (Abilities page:
# "Weapon damage to this unit is reduced by 1"; the Mechs page calls it Armored with the same words)
SPECIAL = {'flying': 'Flying', 'armored': 'Natural Armor'}
# units a weapon puts on the board (the weapon pages' unit boxes and descriptions, 30 Oct 2026)
TOKENS = [
    ('Walking Bomb', 'Bomb Dispenser', 1, 3, 'Trigger: Detonate the Walking Bomb. Damage: 1. Temporary Unit: This unit will die '
     'at the end of the Enemy Turn.'),
    ('Arachnoid', 'Arachnoid Injector', 1, 3, 'Suicide Strike: Sacrifice self to damage and push the target. Damage: 1.'),
    ('Light Tank (unit)', 'Light Tank', 1, 3, 'It shoots a projectile that does no damage and pushes the target.'),
    ('Shield-Tank (unit)', 'Shield-Tank', 1, 3, 'It can give Shields to allies.'),
    ('A.C.I.D. Tank (unit)', 'A.C.I.D. Tank', 1, 3, 'It can apply A.C.I.D. to targets.'),
    ('Pull-Tank (unit)', 'Pull-Tank', 1, 3, 'It can pull targets with a projectile.'),
]


def sections():
    out, cur = {}, None
    for line in open(SRC, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('### '): cur = line[4:]; out[cur] = []
        elif line: out[cur].append(line)
    return out


def upgrades(cells):
    ups = []
    for c in cells:
        m = re.match(r'^;\s*(.+?)\s*\((\d)\):\s*(.*)$', c)
        if m: ups.append(f"{m.group(1)} ({m.group(2)} Reactor Core{'s' if m.group(2) != '1' else ''}): {m.group(3).strip().rstrip('.')}")
    return ups


def power(p):
    return 'Free' if p == 'Free' else 'kill' if p == 'Kill' else f"{p[1]} Reactor Core{'s' if p[1] != '1' else ''}"


def weapons(rows):
    out = []
    for row in rows:
        sec, rest = row.split(' :: ', 1)
        cells = rest.split(' ¦ ')
        name = cells[0]
        i = 1
        dmg = None
        if not POWER.match(cells[1]): dmg, i = cells[1], 2
        if cells[i] == 'Kill': dmg, i = 'kills', i + 1  # Self-Destruct: "Kill" in the damage column
        pw = cells[i]; effect = cells[i + 1]
        tail = cells[i + 2:]
        hp = [re.sub(r'^align="center"\|', '', c) for c in tail if c.startswith('align=')]
        ups = upgrades(tail)
        default = tail[-2] if len(tail) >= 2 else 'None'
        cls = 'Any' if sec.startswith(('Any', 'Deployables')) else sec.split('-')[0]
        parts = [effect if effect.endswith(('.', ')')) else effect + '.']
        if hp: parts.append(f'The unit it deploys has Health {hp[0]}, move {hp[1]}.')
        if dmg is not None:
            d = re.sub(r'\((\d) self\)', r'(\1 to self)', dmg)
            parts.append(f'Damage: {d}.' if dmg != 'kills' else 'Damage: kills.')
        parts.append(f'Power: {power(pw)}.')
        if ups: parts.append('Upgrades: ' + '; '.join(ups) + '.')
        out.append({'name': name, 'class': cls, 'text': ' '.join(parts), 'default': default,
                    'debug': cells[-1].split()[0], 'deploy': sec == 'Deployables'})
    return out


def passives(rows):
    out = []
    for row in rows:
        cells = row.split(' :: ', 1)[1].split(' ¦ ')
        name, pw, effect = cells[0], cells[1], cells[2]
        ups = upgrades(cells[3:])
        parts = [effect.rstrip('.') + '.', f'Power: {power(pw)}.']
        if ups: parts.append('Upgrades: ' + '; '.join(ups) + '.')
        out.append({'name': name, 'class': 'Any', 'text': ' '.join(parts), 'default': cells[-2], 'debug': cells[-1]})
    return out


def mechs(rows, by_debug):
    out = []
    for row in rows:
        cells = row.split(' :: ', 1)[1].split(' ¦ ')
        name = re.match(r'\{\{ficon\|[^|]*\|\s*([^|]+)\|', cells[0]).group(1).strip()
        cells = [re.sub(r'^(rowspan|align)="[^"]*"\s*\|', '', c).strip() for c in cells[1:]]
        cls = cells[0]
        nums = [c for c in cells if c.isdigit()]
        health, move = nums[0], nums[1]
        tpl = next(c for c in cells if c.startswith('{{') and c.lower().strip('{}') not in SPECIAL)
        kit = [by_debug.get(t) or by_debug.get(TEMPLATE.get(t)) for t in re.findall(r'\{\{([^}]+)\}\}', tpl)]
        assert all(kit), (name, tpl)
        spec = [SPECIAL[c.strip('{}').lower()] for c in cells if c.strip('{}').lower() in SPECIAL]
        out.append({'name': name, 'class': cls, 'health': health, 'move': move, 'kit': kit, 'special': spec})
    return out


def pilots(rows):
    out = []
    for row in rows:
        sec, rest = row.split(' :: ', 1)
        if sec not in ('Time Travelers', 'Secret Pilots'): continue  # AI and corporate pilots have no ability; CEOs fly nothing
        cells = rest.split(' ¦ ')
        name = re.sub(r'^center\|link=\S+\s+', '', cells[0]).strip()
        ab = next(c for c in cells if c.lstrip().startswith('*'))
        m = re.match(r'^\*\s*([^:]+):\s*(.*)$', ab.strip())
        out.append({'name': name, 'text': f'Pilot ability: {m.group(1).strip()}: {m.group(2).strip()}',
                    'corp': cells[1] if len(cells) > 3 and cells[1] not in ('None',) and not cells[1].startswith('*') else None})
    return out


def main():
    s = sections()
    ws, ps = weapons(s['Weapons']), passives(s['Passives'])
    by_debug = {w['debug']: w for w in ws + ps}
    by_debug.update({w['name']: w for w in ws + ps})
    ms = mechs(s['Mechs'], by_debug)
    pil = pilots(s['Pilots'])
    out, i = [], 6000001

    def add(name, cat, stype, fac, stats, text, cost=None):
        nonlocal i
        out.append({'game': G, 'ext_id': name, 'name': name, 'category': cat, 'source_type': stype, 'edition': None,
                    'faction': fac, 'subtypes': None, 'rarity': None, 'cost': cost, 'cost_num': None,
                    'stats': json.dumps(stats) if stats else None, 'text': text, 'extra': None, 'variants': None, 'id': i})
        i += 1
        return i - 1
    ids = {}
    for m in ms:
        kit = []
        for w in m['kit']:
            kind = 'Passive' if w['debug'].startswith('Passive_') else 'Weapon'
            kit.append(f"{kind}: {w['name']}: {w['text']}")
        kw = f"Keywords: {', '.join(m['special'])}. " if m['special'] else ''
        ids[m['name']] = add(m['name'], 'unit', SOURCE % 'Mechs (mech)', m['class'], {'health': m['health'], 'move': m['move']},
                             f"{kw}Health {m['health']}, move {m['move']}. " + ' '.join(kit))
    for w in ws:
        if 'debug' in w['default']: continue  # Rock Launcher: "Only available through debug"
        ids[w['name']] = add(w['name'], 'ability', SOURCE % 'Weapons (weapon)', w['class'], None, w['text'],
                             cost=None)
    for p in ps:
        ids[p['name']] = add(p['name'], 'item', SOURCE % 'Passives (passive)', 'Any', None, p['text'])
    for p in pil:
        ids[p['name']] = add(p['name'], 'hero', SOURCE % 'Pilots (pilot)', p['corp'], None, p['text'])
    links = []
    for name, maker, hp, mv, text in TOKENS:
        tid = add(name, 'unit', SOURCE % 'Weapons (unit a weapon deploys, token)', None, {'health': str(hp), 'move': str(mv)},
                  f'Health {hp}, move {mv}. {text}')
        links.append({'src': ids[maker], 'rel': 'generates', 'dst': tid, 'evidence': f'{maker} page: unit box / description'})
        for m in ms:
            if any(w['name'] == maker for w in m['kit']):
                links.append({'src': ids[m['name']], 'rel': 'generates', 'dst': tid, 'evidence': f'starting weapon {maker}'})
    open(OUT, 'w').write(''.join(json.dumps(e) + '\n' for e in out))
    open(LINKS, 'w').write(''.join(json.dumps(l) + '\n' for l in links))
    print(len(ms), 'mechs', len(ws), 'weapons', len(ps), 'passives', len(pil), 'pilots', len(TOKENS), 'tokens', len(links), 'links')


if __name__ == '__main__':
    main()
