"""Weak automatic tags (concept_precision below 70%): wording patterns that the hand reviews judged wrong every time they were
checked (3+ reviewed hits, none right) are switched off for that game: a general pattern gets a '!' line in patterns/<game>.txt,
a game pattern is removed from that file. Their tags are removed where no other pattern of the concept matches (the '!' rule),
except tags the reviews confirmed. Usage: f08_weak_patterns.py <db> (idempotent; the list is below)."""
import os, re, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
lib = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF = [  # (game, concept, start of the pattern), from s/weak.py on 12 Oct 2026: reviewed hits wrong / right
 ('darkest_dungeon', 'debuff', r'-\d+(\.\d+)?%? (accuracy'), ('darkest_dungeon', 'debuff', r'-\d+(\.\d+)? (accuracy'),   # 234/0, 214/0 (own skills' minus stats = drawback)
 ('hearthstone', 'recycle', r'shuffle .{0,40}into (your|their'), ('hearthstone', 'recycle', r'put .{0,30}on the (top|bottom) of'), ('hearthstone', 'recycle', r'\bshuffle (this|it|them'),
 ('into_the_breach', 'upgrade', r'\bupgrade'), ('sts1', 'debuff', r'\bcurse'), ('into_the_breach', 'summon', r'\bspawn'),
 ('wh_killteam', 'debuff', r'(worsen|subtract \d+ from) .{0,40}(characteristic'), ('wh_killteam', 'debuff', r'\bhalve'),
 ('hearthstone', 'cost_increase', r'costs? more'), ('hearthstone', 'resource_gain', r'mana crystal'), ('gwent', 'board_clog', r"\b(enemy|opponent'?s?) side of"),
 ('hearthstone', 'passive', r'\bwhile\b'), ('into_the_breach', 'passive', r'\bwhile\b'), ('into_the_breach', 'passive', r'\bpassive'),
 ('hearthstone', 'damage_over_time', r'at the (start|end|beginning) of .{0,30}(lose'), ('sts2', 'damage_over_time', r'at the (start|end|beginning) of .{0,30}(lose'),
 ('sts1', 'damage_over_time', r'at the (start|end|beginning) of .{0,30}(lose'), ('hearthstone', 'movement', r'\bswap'),
 ('runeterra', 'activated', r'\bactivate'), ('runeterra', 'activated', r'\bspend \d'), ('runeterra', 'cost_condition', r'\b\d+[- ]cost\b'),
 ('wh_bloodbowl3', 'activated', r'\bspecial action\b'), ('wh_bloodbowl3', 'destroy', r'\bcasualty\b'), ('wh_bloodbowl3', 'disable', r'\bknock(s|ed)? down\b'),
 ('duelyst', 'draw', r'(put|add) .{0,40}into your action bar'), ('hearthstone', 'donate', r'shuffle .{0,40}into your opponent'),
 ('hearthstone', 'autonomous_units', r'attacks? (a|the) random'), ('sts1', 'graveyard', r'discard pile'), ('sts1', 'blocking', r'(?<!\d )(?<!gain )(?<!stat )\bblocks?\b'),
 ('marvel_snap', 'turn_structure', r'\b(last|final) turn'), ('hearthstone', 'coin_economy', r'\bspend \d+ \w+ to'), ('hearthstone', 'activated', r'\bspend \d'),
 ('faeria', 'ping', r'deal 1 damage'), ('hs_battlegrounds', 'scope_global', r'\ball (creatures|minions'), ('into_the_breach', 'zone_control', r'\bobjective'),
 ('into_the_breach', 'rows', r'\bfront\b'), ('gwent', 'symmetric_effect', r'\bboth players\b|\beach player\b'), ('gwent', 'symmetric_effect', r'\b(to|on) each side\b'),
 ('hearthstone', 'debuff', r'-\d+(\.\d+)? (accuracy'),
 ('runeterra', 'stat_multiply', r'\bdoubl(e|es|ed)\b'), ('marvel_snap', 'recycle', r'shuffle .{0,40}into (your|their'),
 ('wh_aos_4th', 'death_trigger', r'\bdeathrattle'), ('wh_aos_4th', 'shop_gold', r'\bgold\b'), ('wh_40k_10e', 'shop_gold', r'\bteeth\b'),
 ('wh_aos_4th', 'shop_gold', r'\bteeth\b'), ('wh_killteam', 'counter_spell', r'\bdeny\b'),   # AoS Deathrattle = a faction keyword; Ur-gold; 40k teeth; KT deny (from the 12 Oct review)
 ('wh_40k_10e', 'bodyguard', r'\bbodyguard'),   # 40k "Bodyguard unit" = the unit a Leader is attached to, not a bodyguard mechanic
 ('mtg', 'terrain', r'\blands?\b'), ('mtg', 'terrain', r'\bdeserts?\b'), ('mtg', 'terrain', r'\bforests?\b'), ('mtg', 'terrain', r'\bmountains?\b'),   # Magic lands are mana, not board terrain
 ('hearthstone', 'board_clog', r"(?:^|[.:;,] |\bthen |\band )(target |each |your )?opponents?"),
]
ADD = [('hearthstone', 'resource_gain|does|\\bgain (an? |\\d+ |two |three )?(empty )?mana crystals?\\b|\\bgain .{0,15}mana crystals? this turn\\b')]
keep = set()
for line in open(os.path.join(lib, 'regression.tsv'), encoding='utf-8'):
    f = line.rstrip('\n').split('\t')
    if len(f) >= 6 and f[5] == 'present' and f[1].isdigit(): keep.add((int(f[1]), f[3]))
n = 0
for g, con, start in OFF:
    rows = q("SELECT pattern, game FROM concept_patterns WHERE concept=? AND (game IS NULL OR game=?) AND substr(pattern,1,?)=?", con, g, len(start), start)
    if not rows: print('not found:', g, con, start); continue
    pf = os.path.join(lib, 'patterns', g + '.txt'); lines = open(pf, encoding='utf-8').read().splitlines() if os.path.exists(pf) else []
    for p, pg in rows:
        if pg is None:
            ln = f'!{con}|{p}'
            if ln not in lines: lines.append(ln)
        else:
            lines = [l for l in lines if not (l.startswith(con + '|') and l.split('|', 2)[2] == p)]
            c.execute("DELETE FROM concept_patterns WHERE concept=? AND game=? AND pattern=?", (con, g, p))
    open(pf, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    bad = [re.compile(p, re.I) for p, _ in rows]
    others = [re.compile(p, re.I) for (p,) in q("SELECT pattern FROM concept_patterns WHERE concept=? AND (game IS NULL OR game=?)", con, g) if p not in {x for x, _ in rows}]
    for e, t in q("SELECT e.id, e.text FROM entity_concepts x JOIN entities e ON e.id=x.entity WHERE e.game=? AND x.concept=? AND x.method='text_pattern'", g, con):
        low = (t or '').lower()
        if (e, con) in keep or not any(b.search(low) for b in bad) or any(o.search(low) for o in others): continue
        n += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND method='text_pattern'", (e, con)).rowcount
for g, line in ADD:
    pf = os.path.join(lib, 'patterns', g + '.txt'); lines = open(pf, encoding='utf-8').read().splitlines()
    if line not in lines: open(pf, 'a', encoding='utf-8').write(line + '\n')
c.commit(); print('weak tags removed:', n)
