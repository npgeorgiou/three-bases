"""Step 3, every game: effect records by script, built on the library's own wording patterns (concept_patterns) and stored tags.
For each entry, its text as the patterns read it (reading.py) is cut into sentences. In each sentence:
  trigger    a trigger concept the entry is tagged with whose pattern matches the sentence; else the trigger of the sentence
             before (same ability); else on_play for spells and one-off cards, passive (always on) for the rest
  effect     every effect concept the entry is tagged with (does / grants) whose pattern matches the sentence, at that place;
             a broader concept is dropped when a narrower one matches the same words (concept_parents)
  target     the first target phrase after the effect's words (else the subject before them), from the phrase table below
  amount     the numbers in the effect's words (+2/+2, 3 damage, 2 cards)
  duration   duration words in the sentence; else permanent for lasting changes, instant for the rest, while for passives
  condition  "if / unless / as long as / while / only ..." in the sentence
A sentence that yields no effect is "unread"; an entry with no unread sentence and every effect's target found is "covered".
Usage: auto_records.py <db> [game ...] [--sample N] [--out DIR]   prints coverage per game; --out writes <game>.tsv"""
import collections, os, random, re, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import compact_text as CT
from common import COLUMNS

EFFECT_FACETS = ('effect', 'combat', 'cost', 'resource', 'structure')
SKIP = {'effect', 'helps_me', 'hurts_enemy', 'suppress', 'combat', 'structure', 'economy', 'condition', 'trigger', 'role',
        'scope', 'high_cost', 'game_rules', 'card_flow', 'death', 'randomness', 'lanes', 'rows', 'positional'}
ONE_OFF = ('spell', 'event', 'item', 'ability', 'modifier', 'status')

U = r"(?:creatures?|units?|minions?|characters?|followers?|allies|ally|permanents?|heroes|monsters?|models?|vek|mechs?|lands?|artifacts?|enchantments?|planeswalkers?|tokens?|landmarks?|structures?|items?|locations?|attackers?|blockers?)"
ZONE = r"(?:in|from) (?:your |their |your opponent's |the opponent's |its owner's |each player's |a player's )?(hand|deck|library|graveyard|discard pile)"
TARGETS = [  # (pattern, target); within a span the earliest match wins, ties go to the longer one
    (rf"\b(?:an?|one|two|three|\d+) random [\w' -]{{0,50}}? {ZONE}", 'card:{zone} random {n}'),
    (rf"\b(?:all|each|every|the) [\w' -]{{0,50}}? {ZONE}|\b\w+s {ZONE}", 'card:{zone} all'),
    (rf"\b(?:an?|one|target|another) [\w' -]{{0,50}}? {ZONE}", 'card:{zone} chosen'),
    (r"\byour next \w+", 'card:hand chosen'),
    (r"\ballied [\w' ]{0,40}?s\b", 'ally_unit all'),
    (rf"\b(?:each|all|every) (?:other )?(?:enemy|opposing) {U}|\benemies\b|\b{U} (?:your opponents? controls?|an opponent controls|you don't control)|\ball opposing\b|\bopposing {U}\b", 'enemy_unit all'),
    (rf"\b(?:an?|one|two|three|\d+) random (?:enemy|opposing) {U}|\b(?:an?|\d+) random enem(?:y|ies)", 'enemy_unit random {n}'),
    (rf"\b(?:target|an?|another|chosen|up to one|one) (?:enemy|opposing) {U}|\btarget {U} (?:an opponent controls|you don't control)|\ban enemy\b|\bchosen opposing\b", 'enemy_unit chosen'),
    (rf"\b(?:each|all|every) (?:other )?(?:friendly|allied) {U}|\b(?:other )?{U} you control\b|\byour (?:other )?{U}\b|\b(?:other )?allies\b|\ball friendly\b", 'ally_unit all'),
    (rf"\b(?:an?|one|two|\d+) random (?:friendly|allied) {U}|\b(?:an?|\d+) random all(?:y|ies)\b", 'ally_unit random {n}'),
    (rf"\b(?:target|an?|another|chosen|up to one|one) (?:other )?(?:friendly|allied) {U}|\btarget {U} you control\b|\b(?:an?|another) ally\b|\bchosen character of yours\b", 'ally_unit chosen'),
    (rf"\b(?:an?|one|two|three|\d+) random (?:other )?{U}", 'any_unit random {n}'),
    (rf"\b(?:each|all|every) (?:other )?{U}|\beverything\b|\bboth sides\b", 'any_unit all'),
    (rf"\badjacent {U}|\b{U} (?:adjacent|next) to\b|\badjacent\b|\bneighbou?r", 'ally_unit adjacent'),
    (rf"\b(?:target|chosen|an?|any|another|up to one|up to (?:two|three|\d+)) (?:other )?(?:[\w-]+,? )?(?:\w+ )?{U}\b|\bany target\b|\btarget\b", 'any_unit chosen'),
    (rf"\b{U} attacking you\b|\battacking {U}\b", 'enemy_unit all'),
    (r"\b(?:each opponent|target opponent|target player|your opponent|the opponent|the enemy (?:hero|nexus|player|base|leader|general)|enemy (?:hero|nexus|base|leader|general)|opponent's (?:hero|nexus|base|leader))\b|\bdefending player\b", 'enemy_player'),
    (r"\b(?:each|every|both) players?\b", 'each_player'),
    (r"\bthat player\b|\bthat opponent\b", 'enemy_player'),
    (r"\b(?:your (?:hero|nexus|base|leader|general|life|health)|you gain|you lose|you draw|you may draw|you get|you have|you)\b", 'my_player'),
    (r"\b(?:that|the) (?:creature|unit|minion|character|follower|card|ally|enemy|attacker|blocker|target)\b|\bthe (?:attacking|blocking|damaged|chosen|dead|destroyed) \w+", 'any_unit triggering'),
    (rf"\bname\b|\bthis (?:{U}|card|spirit|vehicle|equipment|aura|saga|class|creature|unit|minion|character|follower|champion|hero|item|weapon|relic|skill)\b|\bitself\b|\b(?:grant|give) me\b|\bi (?:have|get|deal|strike)\b|\bme\b|\bself\b", 'self'),
    (r"\b(?:your|their|its owner's|their owner's|that player's) hand\b|\bin hand\b", 'card:hand chosen'),
    (r"\b(?:your|their|its owner's|that player's) (?:deck|library|draw pile)\b", 'card:deck chosen'),
    (r"\b(?:graveyard|discard pile|discard)\b", 'card:discard chosen'),
    (r"\b(?:lane|location|row|space|tile|cell|zone|square)s?\b", 'position chosen'),
]
TARGETS = [(re.compile(p), t) for p, t in TARGETS]
OWN = {'draw': 'my_player', 'resource_gain': 'my_player', 'generate_cards': 'my_player', 'summon': 'position chosen',
       'card_advantage': 'my_player', 'tutor': 'card:deck chosen', 'self_mill': 'card:deck chosen', 'mill': 'card:deck chosen',
       'block_armor': 'self', 'cost_reduction': 'card:hand chosen', 'resource_banking': 'my_player', 'extra_turn': 'my_player',
       'discard': 'card:hand chosen', 'recycle': 'card:discard chosen', 'revive': 'card:discard chosen', 'selection': 'card:deck chosen',
       'coin_economy': 'my_player', 'shop_gold': 'my_player', 'life_payment': 'my_player', 'sacrifice': 'ally_unit chosen',
       'self_destruct': 'self', 'spell_power': 'my_player', 'direct_damage': 'enemy_player', 'retain': 'card:hand chosen',
       'exhaust': 'self', 'free_play': 'card:hand chosen', 'cast_from_zone': 'self', 'overload_debt': 'my_player'}
WORDNUM = {'a': '1', 'an': '1', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
           'eight': '8', 'nine': '9', 'ten': '10'}
DURATIONS = [  # (pattern, duration); first match wins
    (r"\buntil (?:the )?end of (?:the |this )?turn\b|\bthis turn\b|\bthis phase\b|\buntil end of turn\b", 'this_turn'),
    (r"\bthis round\b|\buntil (?:the )?end of (?:the )?round\b", 'this_round'),
    (r"\buntil (?:the start of )?your next turn\b", 'until_my_next_turn'),
    (r"\bfor (?:\d+|two|three|four|a number of) (?:more )?turns\b", 'n_turns'),
    (r"\bfor (?:\d+|two|three|four) (?:more )?rounds\b", 'n_rounds'),
    (r"\b(?:during )?(?:its|their|your|the|the opponent's) next turn\b|\bnext turn\b", 'next_turn'),
    (r"\b(?:this|the) (?:combat|battle|fight)\b|\buntil end of combat\b", 'this_combat'),
    (r"\bfor the rest of the game\b|\bthis game\b|\bpermanently\b", 'this_game'),
    (r"\buntil (?:it|this|name|that \w+) leaves\b", 'until_leaves'),
    (r"\bas long as\b|\bwhile\b", 'while'),
]
DURATIONS = [(re.compile(p), d) for p, d in DURATIONS]
LASTING = {'stat_gain', 'attack_gain', 'defence_gain', 'stat_loss', 'debuff', 'buff', 'summon', 'transform', 'polymorph', 'silence',
           'permanent_growth', 'upgrade', 'in_hand_buff', 'cost_reduction', 'cost_increase', 'cost_set', 'steal', 'merge_attach',
           'type_grant', 'random_ability', 'shield', 'taunt', 'stealth', 'immunity', 'evasion', 'haste', 'lifesteal', 'deathtouch',
           'first_strike', 'multi_attack', 'protection', 'cant_attack', 'cant_block', 'attack_lock', 'stat_multiply', 'block_armor'}
COND = re.compile(r"\b(?:if|unless|as long as|only if|only|while|when(?:ever)? you have)\b[^,.:]*")
AMOUNT = re.compile(r"[+-]?\d+[/|][+-]?\d+|[+-]x/[+-]x|[+-]?\d+%?|\bx\b|\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\b(?= (?:\w+ )?(?:damage|cards?|counters?|life|health|armor|mana|coins?|gold|energy|tokens?|times)\b)")
SENT = re.compile(r"(?:[^.\n;]|\.(?=\d))+(?:[.;]|\n|$)")  # a dot inside a number (+0.5) does not end a sentence
DATA = re.compile(r"(?:keywords?|class|availability|health|move|cooldown|counter|charge|cost|rarity|type|tier|loot|choices|actions|skills|upgrades?|level)\b[^.]*:?[ \w,.*()-]*")


def load(c):
    facet = dict(c.execute("SELECT id, facet FROM concepts"))
    parents = collections.defaultdict(set)
    for ch, pa in c.execute("SELECT child, parent FROM concept_parents"): parents[ch].add(pa)
    def anc(k, seen=None):
        seen = set() if seen is None else seen
        for p in parents[k]:
            if p not in seen: seen.add(p); anc(p, seen)
        return seen
    pats = collections.defaultdict(list)
    for k, role, p, g in c.execute("SELECT concept, role, pattern, game FROM concept_patterns WHERE role IN ('does','trigger','grants')"):
        try: pats[(k, g)].append(re.compile(p, re.I))
        except re.error: pass
    return facet, {k: anc(k) for k in facet}, pats


def find(pats, k, game, s):
    """Positions where concept k's patterns (general, patterns/_all.txt for every game but Marvel Snap, and this game's
    patterns/<game>.txt) match sentence s."""
    out = []
    for rx in pats.get((k, None), []) + (pats.get((k, '_all'), []) if game != 'marvel_snap' else []) + pats.get((k, game), []):
        out += [(m.start(), m.end()) for m in rx.finditer(s)]
    return sorted(out)


def target(span, before):
    best = None
    for rx, t in TARGETS:
        m = rx.search(span)
        if m and (best is None or m.start() < best[0] or (m.start() == best[0] and m.end() > best[1])): best = (m.start(), m.end(), t, m.group(0))
    if best is None:
        for rx, t in TARGETS:
            for m in rx.finditer(before):
                if best is None or (m.end(), m.end() - m.start()) > (best[1], best[1] - best[0]): best = (m.start(), m.end(), t, m.group(0))
    if best is None: return ''
    t = best[2]
    if '{zone}' in t:
        z = re.search(ZONE, best[3]).group(1)
        t = t.replace('{zone}', {'library': 'deck', 'graveyard': 'discard', 'discard pile': 'discard'}.get(z, z))
    if '{n}' in t:
        w = best[3].split()[0]
        t = t.replace('{n}', WORDNUM.get(w, w if w.isdigit() else '1'))
    return t


MARKERS = {'temporary_buff', 'temporary_effect', 'graveyard', 'random_effect', 'random_target', 'target_choice', 'scope_multi',
           'scope_global', 'scope_self', 'distribute', 'multi_target_attack', 'excess_damage'}  # dropped when another effect shares the words
OPENING = re.compile(r"^(?:(?:when(?:ever)?|at the (?:beginning|start|end)|after|each time|the first time|once per|during)\b[^,:]*[,:]|[\w'’ -]{2,30}(?:\([^)]*\))?:(?!\w))\s*")
LABEL = re.compile(r"^([\w'’ -]{2,30})(?:\([^)]*\))?:(?!\w)")
SUBJECT_VERB = re.compile(r"\b(?:gets?|gains?|has|have|becomes?|costs?|loses?|can't|cannot|can|must|deals?|takes?|enters?|attacks?)\b")
PRONOUN = re.compile(r"\b(?:it|its|them|they|their|that card|those \w+|he|she|him|her)\b")
OBJECT_FX = {'summon', 'generate_cards', 'copy', 'transform', 'polymorph', 'tutor'}  # "summon a 2/2 with Rush": the keywords describe the new card

DD_STAT = re.compile(r"^([+-]?\d+(?:\.\d+)?%?) ([a-z_' ]+?)(?: (while|with|vs|when|on|in|at) (.*?))?(?:\. (class: \w+))?$")
DD_STATK = {'dodge': 'defence_gain', 'protection': 'defence_gain', 'max hp': 'defence_gain', 'damage': 'attack_gain',
            'accuracy': 'attack_gain', 'crit': 'attack_gain', 'speed': 'speed'}  # which stat goes up
DD_WHO = {'(self)': 'self', '(party_other)': 'ally_unit all', '(party)': 'ally_unit all', '(global)': 'each_player', '(target)': 'ally_unit chosen'}
DD_FX = [  # (words, effect) for skill and camping effects the stat reader does not cover; the rest of the item is the amount
    (r"^(?:relieve stress|stress heal|reduce stress)", 'stress_morale'), (r"^(?:health heal|heal)", 'heal'),
    (r"^health damage", 'damage'), (r"^(?:inflict )?disease", 'debuff'), (r"^summon\b", 'summon'),
    (r"^(?:increase|decrease|reduce) light|^light ", 'light_level'), (r"^reduce ambush|^ambush", 'protection'),
    (r"^buff: ", 'temporary_buff'), (r"^remove (?:bleed|blight|debuff|disease)|^cure", 'heal'), (r".*\bstress\b", 'stress_morale'),
    (r".*\bdebuff\b", 'debuff'), (r".*\bbuff\b", 'temporary_buff'), (r"^(?:clear|remove) .*", 'rewind'),
    (r"^(?:kill|execute)\b", 'destroy'), (r"^(?:tag|mark)\b", 'mark_target'), (r"^(?:shuffle|swap)", 'forced_movement')]
DD_FX = [(re.compile(p), k) for p, k in DD_FX]


def dd_records(e, cat, text):
    """Darkest Dungeon's fixed formats: skills (targets, damage, effects list), stat lines of items and statuses, event outcomes."""
    out, unread, t = [], 0, (text or '').lower()
    if cat == 'event' and 'possible outcomes:' in t:  # a curio: random outcomes, and outcomes for using an item on it
        body = t.split('possible outcomes:', 1)[1]
        parts = [x.strip(' .') for x in body.split(';') if x.strip(' .')]
        rnd = [x for x in parts if not x.startswith('use ')]
        out.append((e, 1, 'activated', 'random_effect', 'my_player', '; '.join(rnd)[:80], 'instant', '', 'script'))
        for n, x in enumerate([x for x in parts if x.startswith('use ')], 2):
            item, _, res = x[4:].partition(':')
            out.append((e, n, 'activated', 'items_consumables', 'my_player', res.strip()[:60], 'instant', f'use {item.strip()}', 'script'))
        return out, 0
    if t.startswith('camping skill'):  # camping: "effect amount (who)" items
        for it in [x.strip(' .') for x in re.split(r";", t.split('.', 1)[1]) if x.strip(' .')]:
            if it.startswith('uses per camp'): continue
            who = next((v for k, v in DD_WHO.items() if k in it), 'self'); it2 = re.sub(r"\([a-z_]+\)", '', it).strip()
            k = next((k for rx, k in DD_FX if rx.search(it2)), None)
            if k: out.append((e, 1, 'activated', k, who, it2[:50], 'instant' if k != 'temporary_buff' else 'this_combat', 'camping', 'script'))
            else: unread += 1
        return out, unread
    if 'skill.' in t or cat == 'ability':
        for ab, sk in enumerate(re.split(r" \| ", re.sub(r"^skills: ", "", t)), 1):
            sk = re.sub(r"^[^.:]+: (?=(?:melee|ranged) skill)", "", sk)
            tm = re.search(r"targets (all of )?(enemy|ally) ranks", sk)
            tg = (('enemy_unit' if tm.group(2) == 'enemy' else 'ally_unit') + (' all' if tm.group(1) else ' chosen')) if tm else 'self'
            dm = re.search(r"deals damage(?: \(modifier ([+-]?\d+%)\)| (\d+-\d+))?", sk)
            if dm and '-100%' not in dm.group(0): out.append((e, ab, 'activated', 'aoe_damage' if tm and tm.group(1) else 'damage', tg, dm.group(1) or dm.group(2) or '', 'instant', '', 'script'))
            hm = re.search(r"\bheals (\d+)(?: (\d+))?", sk)
            if hm: out.append((e, ab, 'activated', 'heal', tg, '-'.join(x for x in hm.groups() if x), 'instant', '', 'script'))
            if re.search(r"moves self", sk): out.append((e, ab, 'activated', 'movement', 'self', '', 'instant', '', 'script'))
            fx = sk.split('effects:')[1] if 'effects:' in sk else ''
            for it in [x.strip(' .') for x in re.split(r"[;,]", fx) if x.strip(' .')]:
                own = 'self' if '(self)' in it else tg
                it = it.replace('(self)', '').strip()
                rm = re.search(r"for (\d+) rounds?", it); dur, rn = ('n_rounds', '; ' + rm.group(1)) if rm else (None, '')
                if m := re.match(r"(bleed|blight) (\d+)", it): out.append((e, ab, 'activated', 'damage_over_time', own, m.group(2) + rn, dur or 'n_rounds', m.group(1), 'script'))
                elif it.startswith('stun'): out.append((e, ab, 'activated', 'disable', own, '', 'next_turn', '', 'script'))
                elif re.match(r"(push|pull|knock)", it): out.append((e, ab, 'activated', 'forced_movement', own, it[:30], 'instant', '', 'script'))
                elif m := re.match(r"stress (?:heal )?([+-]?\d+)", it): out.append((e, ab, 'activated', 'stress_morale', own, m.group(1), 'instant', '', 'script'))
                elif it.startswith('guard'): out.append((e, ab, 'activated', 'bodyguard', 'ally_unit chosen', rn.strip('; '), dur or 'instant', '', 'script'))
                elif it.startswith('mark'): out.append((e, ab, 'activated', 'mark_target', own, '', dur or 'instant', '', 'script'))
                elif m := re.match(r"heal (\d+(?:-\d+)?)", it): out.append((e, ab, 'activated', 'heal', own, m.group(1), 'instant', '', 'script'))
                elif m := re.match(r"([+-]\d+(?:\.\d+)?%?) ([a-z ]+?)(?: for \d+ rounds?)?$", it):
                    k = DD_STATK.get(next((w for w in DD_STATK if w in m.group(2)), ''), 'stat_gain') if m.group(1).startswith('+') else 'stat_loss'
                    out.append((e, ab, 'activated', k, own, f'{m.group(1)} {m.group(2)}' + rn, dur or 'n_rounds', '', 'script'))
                elif it.startswith('only if '): pass  # a condition of the skill, kept by the tags
                elif (k := next((k for rx, k in DD_FX if rx.search(it)), None)): out.append((e, ab, 'activated', k, own, it[:50], dur or 'instant', '', 'script'))
                else: unread += 1
        if out or unread: return out, unread
    for ln in [x.strip(' .') for x in re.split(r"[;\n]", t) if x.strip(' .')]:
        m = DD_STAT.match(ln)
        if not m:
            if cat == 'status' and re.search(r"[a-z]{4}", ln): out.append((e, 1, 'passive', 'traits_quirks', 'self', ln[:60], 'while', '', 'script'))
            else: unread += 1
            continue
        k = 'stat_loss' if m.group(1).startswith('-') else DD_STATK.get(next((w for w in DD_STATK if w in m.group(2)), ''), 'stat_gain')
        cond = '; '.join(x for x in (f'{m.group(3)} {m.group(4)}'.strip() if m.group(3) else '', m.group(5) or '') if x)
        out.append((e, 1, 'passive', k, 'self', f'{m.group(1)} {m.group(2).strip()}', 'while' if cond else 'permanent', cond, 'script'))
    return out, unread


def hinted(k, tags, anc):
    """A target from the entry's own tags when the words name none: the side from who the effect helps or hurts (concept
    tree), how many from its scope tags (random_target; aoe_damage, board_wipe, scope_global; adjacency; scope_self)."""
    if 'scope_self' in tags: return 'self'
    side = 'enemy_unit' if 'hurts_enemy' in anc.get(k, ()) else 'ally_unit' if 'helps_me' in anc.get(k, ()) else ''
    if not side: return ''
    if 'random_target' in tags: return side + ' random 1'
    if tags & {'aoe_damage', 'board_wipe', 'scope_global'}: return side + ' all'
    if 'adjacency' in tags: return side + ' adjacent'
    return side + ' chosen' if side == 'enemy_unit' else 'self'


def records(c, e, game, name, cat, text, tags, facet, anc, pats, kwre=None, allfx=(), kwfx=(), kwgrant=(), kwtrig={}):
    """(records, unread sentence count). kwre: the game's keyword names (a sentence of keywords only is read through the
    keyword records); allfx: every effect concept with a pattern in this game, tried when no tagged concept matches;
    kwfx: the game's action keywords used as verbs ("obliterate a unit"), with their records' effect."""
    if game == 'darkest_dungeon' and cat in ('ability', 'item', 'monster', 'status', 'event'): return dd_records(e, cat, text)
    rt = CT.read_text(game, name, text)
    trig_tags = [k for k in tags if facet.get(k) == 'trigger']
    eff_tags = [k for k in tags if facet.get(k) in EFFECT_FACETS and k not in SKIP]
    out, unread, prev, ab, last_tg = [], 0, None, 0, ''
    for sm in SENT.finditer(rt):
        s = sm.group(0).strip()
        if len(s) < 3 or s.startswith('(') or '(same as the unevolved form' in s: continue  # a note in brackets explains the sentence before it
        bullet = s[:1] in '•*'
        s = s.lstrip('•*-– ').strip()
        if bullet and re.match(r"[\d+x-]+/[\d+x-]+ ", s) and out and out[-1][3] in OBJECT_FX:  # a token description under "create"
            continue
        s = re.sub(r'["“][^"”]*["”]', '"granted ability"', s)  # a quoted ability is given, not done now
        if DATA.fullmatch(s.strip(' .;')) and not re.search(r'\b(?:deal|damage|gain|draw|give|summon|destroy)\b', s): continue
        if kwre is not None:
            if kwre.fullmatch(s.strip(' .,')): continue
            m = kwre.match(s)
            if m and m.end() < len(s) and s[m.end()] in ' .,' and not LABEL.match(s) and not (any(rx.match(s) for rx, _ in kwfx) and re.match(
                    r"[ ,.]*(?:an?|target|all|the|each|up|one|two|three|any|another|\d+|it|them)\b", s[m.end():])):
                s = s[m.end():].strip(' .,')
            if len(s) < 3: continue
        trig, tpos = None, len(s)
        for k in trig_tags:
            f = find(pats, k, game, s)
            if f and f[0][0] < tpos: trig, tpos = k, f[0][0]
        op = OPENING.match(s)
        skip_to = op.end() if op else 0  # words of the trigger itself are not effects
        lab = LABEL.match(s)
        if not trig and lab and lab.group(1).strip() in kwtrig: trig = kwtrig[lab.group(1).strip()]
        if trig: ab += 1
        elif op: trig = 'trigger'; ab += 1
        elif prev: trig = prev
        else: trig = 'on_play' if cat in ONE_OFF else 'passive'; ab += 1
        prev = trig if trig != 'passive' else None
        cspans = [(m.start(), m.end()) for m in COND.finditer(s)]
        conds = [s[x:y].strip() for x, y in cspans]
        if op and trig == 'trigger': conds.insert(0, op.group(0).strip(' ,:'))
        hits = []
        for k in eff_tags:
            hits += [(x, y, k) for x, y in find(pats, k, game, s)]
        if not any(x >= skip_to for x, y, k in hits):
            for k in allfx:
                hits += [(x, y, k) for x, y in find(pats, k, game, s)]
        for rx, k in kwfx:
            for m in rx.finditer(s):
                if not any(h[0] < m.end() and m.start() < h[1] for h in hits): hits.append((m.start(), m.end(), k))
        hits = [h for h in hits if h[0] >= skip_to and not any(x <= h[0] and h[1] <= y for x, y in cspans)]
        ov = lambda h, o: o[0] < h[1] and h[0] < o[1]
        hits = [h for h in hits if not any(o[2] != h[2] and h[2] in anc.get(o[2], ()) and ov(h, o) for o in hits)]
        for rx, k in kwgrant:  # "grant allied Spritelings Spirit", "it gains trample": the keyword record's effect
            for m in rx.finditer(s):
                if m.start() >= skip_to and not any(ov((m.start(), m.end()), h) for h in hits): hits.append((m.start(), m.end(), k))
        hits = [h for h in hits if not (h[2] in MARKERS and any(o[2] not in MARKERS for o in hits))]
        hits = [h for h in hits if not re.search(r"\b(?:can't|cannot|can not|don't|doesn't|isn't|aren't|won't) (?:be )?$", s[max(0, h[0] - 14):h[0]])]
        ks = {h[2] for h in hits}
        if {'attack_gain', 'defence_gain'} <= ks:  # +2/+2 is one stat gain
            ag = [h for h in hits if h[2] == 'attack_gain']; dg = [h for h in hits if h[2] == 'defence_gain']
            if any(ov(x, y) or abs(x[0] - y[0]) < 12 for x in ag for y in dg):
                hits = [h for h in hits if h[2] != 'defence_gain']; hits = [(x, y, 'stat_gain' if k == 'attack_gain' else k) for x, y, k in hits]
        hits.sort(); seen = set(); eff = []
        for x, y, k in hits:
            if k in seen or any(ov((x, y), (p, q)) for p, q, _ in eff): continue
            seen.add(k); eff.append((x, y, k))
        # keywords inside the object of a summon or create are part of what is made
        folded = []
        for i, (x, y, k) in enumerate(eff):
            if k in OBJECT_FX:
                end = re.search(r"(?:\.|,(?! and)| then | and (?!\w+ and)(?=(?:deal|draw|give|gain|destroy|return|put|you|it|they|each|all|target|summon|create)\b)|$)", s[y:])
                folded.append((y, y + (end.start() if end else len(s) - y)))
        eff = [(x, y, k) for x, y, k in eff if k in OBJECT_FX or not any(p <= x < q for p, q in folded)]
        if not eff: unread += 1; continue
        dur = next((d for rx, d in DURATIONS if rx.search(s)), None)
        for i, (x, y, k) in enumerate(eff):
            nxt = eff[i + 1][0] if i + 1 < len(eff) and eff[i + 1][0] > y else len(s)
            span = s[x:nxt]
            before = s[skip_to:x]
            sv = SUBJECT_VERB.search(s[max(skip_to, x - 14):y])
            pm = PRONOUN.search(span)
            tg = ''
            if k in OWN and k in ('draw', 'resource_gain', 'generate_cards', 'summon', 'coin_economy', 'shop_gold', 'extra_turn'):
                tg = OWN[k]
            elif sv:
                tb = target('', before)
                pb = list(PRONOUN.finditer(before))
                if pb and (not tb or pb[-1].end() > max((m.end() for rx, t in TARGETS for m in rx.finditer(before)), default=-1)):
                    tg = last_tg or ('self' if op and target('', op.group(0)) == 'self' else 'any_unit triggering')
                else: tg = tb
            if not tg:
                tg = target(span, '')
                if pm and (not tg or span.find(pm.group(0)) < min((m.start() for rx, t in TARGETS for m in [rx.search(span)] if m), default=999)):
                    tg = last_tg or ('self' if op and target('', op.group(0)) == 'self' else 'any_unit triggering')
            if not tg: tg = target('', before)
            if not tg and re.match(r"(?:lose|loses|pay|pays|take|takes|discard)\b", s[x:]): tg = 'my_player' if cat in ONE_OFF else 'self'
            tg = tg or OWN.get(k, '') or ('self' if cat not in ONE_OFF and k in LASTING else '') \
                or ('self' if cat in ('item', 'relic', 'status', 'hero') else '') \
                or hinted(k, tags, anc)
            cut = re.search(r",| unless | if | as long as | instead\b", span[1:])
            am = ', '.join(m.group(0) for m in AMOUNT.finditer(span[:cut.start() + 1] if cut else span))[:40]
            if k in OBJECT_FX:
                ob = [f for f in folded if f[0] == y]
                if ob: am = s[ob[0][0]:ob[0][1]].strip(' ,.')[:60]
            d = dur or ('while' if trig in ('passive', 'aura') else 'permanent' if k in LASTING else 'instant')
            if d in ('n_turns', 'n_rounds'):
                nm = re.search(r'for (\d+|two|three|four)', s); am += '; ' + (WORDNUM.get(nm.group(1), nm.group(1)) if nm else 'N')
            am = am.replace('name', name or '~')
            out.append((e, ab, trig, k, tg, am, d, '; '.join(conds)[:80], 'script'))
            if tg and not tg.startswith(('my_player', 'position', 'card')): last_tg = tg
    return out, unread


def prep(c, g, facet, pats):
    """The game's keyword-only sentence matcher, its effect concepts with patterns, and its keyword verbs."""
    kws = sorted((re.escape(x.lower()) for (x,) in c.execute("SELECT name FROM entities WHERE game=? AND category='keyword'", (g,))), key=len, reverse=True)
    kw = rf"(?:{'|'.join(kws)})(?::? ?\+?\d+\+?| \{{[^}}]*\}}+| x)?" if kws else None
    kwre = re.compile(rf"(?:keywords?: )?{kw}(?:[,.]? (?:and )?{kw})*") if kw else None
    allfx = [k for k in facet if facet[k] in EFFECT_FACETS and k not in SKIP and ((k, None) in pats or (k, g) in pats or (k, '_all') in pats)]
    kwfx, kwgrant, kwtrig, f = [], [], {}, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keywords', f'{g}.txt')
    if os.path.exists(f):
        names = dict(c.execute("SELECT id, lower(name) FROM entities WHERE game=? AND category='keyword'", (g,)))
        for line in open(f):
            p = [x.strip() for x in line.split('|')]
            if line.startswith('#') or len(p) < 4 or not p[0].isdigit(): continue
            nm = names.get(int(p[0]))
            if nm and p[2] and p[2] != '-' and not p[3]: kwtrig[nm] = p[2]
            if not p[3]: continue
            if not nm or len(nm) < 4: continue
            if p[2] == '-': kwfx.append((re.compile(rf"\b{re.escape(nm)}(?:s|d|ed|es)?\b"), p[3]))
            else: kwgrant.append((re.compile(rf"\b(?:grant|gives?|gains?|gets?|has|have|with) (?:[\w' ]{{0,40}} )?{re.escape(nm)}\b"), p[3]))
    return kwre, allfx, kwfx, kwgrant, kwtrig


def run(c, games, sample=0, outdir=None):
    facet, anc, pats = load(c)
    tags = collections.defaultdict(set)
    for e, k in c.execute("SELECT entity, concept FROM entity_concepts WHERE role IN ('does','grants','trigger','cost')"): tags[e].add(k)
    random.seed(1)
    for g in games:
        kwre, allfx, kwfx, kwgrant, kwtrig = prep(c, g, facet, pats)
        rows = c.execute("SELECT id, name, category, text FROM entities WHERE game=? AND category NOT IN ('keyword','tribe') "
                         "AND text IS NOT NULL AND text != ''", (g,)).fetchall()
        got, n_cov, n_rec, n_tg = {}, 0, 0, 0
        for e, nm, cat, t in rows:
            recs, unread = records(c, e, g, nm, cat, t, tags[e], facet, anc, pats, kwre, allfx, kwfx, kwgrant, kwtrig)
            got[e] = (recs, unread)
            n_rec += len(recs); n_tg += sum(1 for r in recs if r[4])
            if recs and not unread and all(r[4] for r in recs): n_cov += 1
        print(f'{g:18} entries {len(rows):6}  covered {100 * n_cov / max(1, len(rows)):5.1f}%  records {n_rec:6}  with target {100 * n_tg / max(1, n_rec):5.1f}%')
        if outdir:
            with open(os.path.join(outdir, f'{g}.tsv'), 'w') as f:
                f.write('\t'.join(c for c in COLUMNS if c not in ('shape', 'extra', 'keyword')) + '\n')
                for recs, _ in got.values():
                    for r in recs: f.write('\t'.join(str(x) for x in r) + '\n')
        for e, nm, cat, t in random.sample(rows, min(sample, len(rows))):
            recs, unread = got[e]
            print(f'\n  {nm} [{cat}] | {t[:300]}' + (f'   (unread sentences: {unread})' if unread else ''))
            for r in recs: print('     ', ' | '.join(str(x) for x in r[1:8]))


if __name__ == '__main__':
    a = sys.argv[1:]
    sample = int(a[a.index('--sample') + 1]) if '--sample' in a else 0
    outdir = a[a.index('--out') + 1] if '--out' in a else None
    db = a[0]; games = [x for x in a[1:] if not x.startswith('--') and not x.isdigit() and x != outdir]
    c = sqlite3.connect(db)
    if not games: games = [r[0] for r in c.execute("SELECT game FROM entities GROUP BY game ORDER BY count(*) DESC")]
    run(c, games, sample, outdir)


def diag(c, g, n=10):
    """Unread sentences and records without a target, a random sample of each (for improving the wording)."""
    facet, anc, pats = load(c)
    tags = collections.defaultdict(set)
    for e, k in c.execute("SELECT entity, concept FROM entity_concepts WHERE role IN ('does','grants','trigger','cost')"): tags[e].add(k)
    kwre, allfx, kwfx, kwgrant, kwtrig = prep(c, g, facet, pats)
    un, nt = [], []
    for e, nm, cat, t in c.execute("SELECT id, name, category, text FROM entities WHERE game=? AND category NOT IN ('keyword','tribe') AND text != ''", (g,)).fetchall():
        rt = CT.read_text(g, nm, t)
        for sm in SENT.finditer(rt):
            s = sm.group(0).strip()
            r, u = records(c, e, g, nm, cat, s, tags[e], facet, anc, pats, kwre, allfx, kwfx, kwgrant, kwtrig)
            if u: un.append(f'[{cat}] {s}')
            nt += [f'[{cat}] {x[3]} | {s}' for x in r if not x[4]]
    random.seed(5)
    print(g, 'unread', len(un), 'no target', len(nt))
    for x in random.sample(un, min(n, len(un))): print('  U', x[:170])
    for x in random.sample(nt, min(n, len(nt))): print('  T', x[:170])
