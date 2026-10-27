"""The questions, asked of each clause of a card's text (TAGGING_RECORDS.md step 3, agreed 27 Oct 2026).
A sentence is cut into clauses, one per verb ("deal 6 damage to a creature and 3 damage to all adjacent enemies" is two; the
second borrows the verb). For each clause:
  when       the sentence's opening ("Last Words -", "Whenever you draw ...,", "At the end of your turn,"), else the card's default
  what       the clause's verb with its words (VERBS below); the card's tags only name a narrower concept for the same thing
  who        the verb's object ("to all adjacent enemies"), else its subject ("this gains"); "it"/"they" mean what was last named
  how much   the numbers in the clause; how long, condition: the duration and condition words of the clause (and of the sentence)
answer(sentence, ...) -> [dict(trigger, effect, target, shape, amount, duration, condition, words)]"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import auto_records as A

N = r"(?:\d+|x|an?|one|two|three|four|five|six|seven|eight|nine|ten)"
RES = r"(?:mana|faeria|coins?|crowns?|gold|bones?|energy|gems?|mox|crystals?|play points?|resources?|ink|lore|points?)"
KEYS = ('taunt', 'divine shield', 'rush', 'charge', 'windfury', 'stealth', 'lifesteal', 'poisonous', 'reborn', 'flying', 'haste',
        'ranged', 'provoke', 'frenzy', 'celerity', 'airdrop', 'rebirth', 'zeal', 'backstab', 'protection', 'jump', 'aquatic',
        'deathtouch', 'divine', 'elusive', 'trample', 'armor', 'shield', 'ward', 'flanking', 'grow', 'forcefield', 'dash')

# verb -> how its clause is read: (regex on the clause from the verb, effect, where the target is: 'obj' after the verb,
# 'subj' before it, or a fixed target)
VERBS = [
    (r"(?:deals?|dealing|inflicts?) (?P<n>\d+|x|that much|damage equal|double)?[^.]*?\bdamage\b", 'damage', 'obj'),
    (r"(?:takes?|suffers?) (?P<n>\d+|x|that much|double)?[^.]*?\bdamage\b", 'damage', 'subj'),
    (r"damages? (?P<n>)", 'damage', 'obj'),
    (r"(?:destroy|destroys|kill|kills|slay)\b", 'destroy', 'obj'),
    (r"(?:banish|banishes|exile|exiles|obliterate|obliterates|remove [^.]* from the game)\b", 'banish', 'obj'),
    (r"(?:dies|perishes|is destroyed)\b", 'self_destruct', 'subj'),
    (r"(?:summon|summons|spawn|spawns|deploy|deploys|call in|calls in)\b", 'summon', 'position chosen'),
    (rf"(?:create|creates)\b(?=[^.]*\b(?:forest|lake|desert|mountain|land|tile|smoke|fire|water|ice|chasm|lava)\b)", 'terrain', 'position chosen'),
    (r"(?:create|creates|conjure|conjures)\b(?=[^.]*\b(?:to|into|in) your (?:hand|deck)\b)", 'generate_cards', 'zone'),
    (r"(?:create|creates)\b", 'summon', 'position chosen'),
    (r"(?:add|adds|get|gets|put|puts|shuffle|shuffles)\b(?=[^.]*\b(?:to|into|in) (?:your|their|its owner's|the opponent's|your opponent's) (?:hand|deck|action bar)\b)", 'generate_cards', 'zone'),
    (r"(?:draw|draws)\b", 'draw', 'subj_player'),
    (r"(?:discover|discovers)\b", 'generate_cards', 'my_player'),
    (r"(?:search|searches|tutor)\b", 'tutor', 'card:deck chosen'),
    (r"(?:restore|restores|heal|heals|recover|recovers)\b(?! (?:\d+ )?play points?)", 'heal', 'obj'),
    (rf"(?:gain|gains|get|gets|recover|recovers|refill|refills|add|adds) (?:an? |\d+ |x |an empty )?(?:\w+ )?{RES}\b", 'resource_gain', 'subj_player'),
    (r"(?:gain|gains|get|gets) (?:\d+|x) (?:life|health)\b", 'heal', 'subj_player'),
    (r"(?:gain|gains|get|gets) (?:\d+|x) armou?r\b", 'block_armor', 'subj'),
    (r"(?:gain|gains|take|takes|gets?) control of\b", 'steal', 'obj'),
    (r"(?:steal|steals)\b", 'steal', 'obj'),
    (r"(?:gain|gains|get|gets|has|have|is given)\s+[+-]?(?:\d+|x)/[+-]?(?:\d+|x)", 'stat', 'subj'),
    (r"(?:gain|gains|get|gets|has|have)\s+[+-](?:\d+|x) (?:attack|power|strength)", 'attack_gain', 'subj'),
    (r"(?:gain|gains|get|gets|has|have)\s+[+-](?:\d+|x) (?:health|life|defense|toughness|armor)", 'defence_gain', 'subj'),
    (r"(?:give|gives|grant|grants)\s+[^.]*?[+-]?(?:\d+|x)/[+-]?(?:\d+|x)", 'stat', 'obj'),
    (r"(?:give|gives|grant|grants)\s+[^.]*?[+-](?:\d+|x) (?:attack|power|strength)", 'attack_gain', 'obj'),
    (r"(?:give|gives|grant|grants)\s+[^.]*?[+-](?:\d+|x) (?:health|defense)", 'defence_gain', 'obj'),
    (r"(?:boost|boosts|strengthen|strengthens)\b", 'stat_gain', 'obj'),
    (r"(?:weaken|weakens)\b", 'stat_loss', 'obj'),
    (r"(?:gain|gains|get|gets|has|have|give|gives|grant|grants)\b[^.]*?\b(?P<kw>" + '|'.join(KEYS) + r")\b", 'keyword', 'grant'),
    (r"(?:freeze|freezes|stun|stuns|shackle|shackles|sleep)\b", 'disable', 'obj'),
    (r"(?:can't|cannot|can no longer) move\b", 'immobilize', 'subj'),
    (r"(?:can't|cannot|can no longer) attack\b", 'attack_lock', 'subj'),
    (r"(?:can't|cannot) block\b", 'cant_block', 'subj'),
    (r"(?:can't|cannot) be (?:targeted|attacked|damaged|chosen)\b|(?:is|are) immune\b|ignores? (?:all )?damage", 'immunity', 'subj'),
    (r"(?:silence|silences|dispel|dispels|lock|locks)\b", 'silence', 'obj'),
    (r"(?:push|pushes|pull|pulls|knock|knocks|throw|throws|toss|tosses)\b", 'forced_movement', 'obj'),
    (r"(?:swap|swaps|exchange)\b", 'swap', 'obj'),
    (r"(?:move|moves|teleport|teleports|relocate)\b", 'move', 'obj'),
    (r"(?:return|returns|recall|recalls|bounce|unsummon)\b(?=[^.]*\b(?:hand|action bar)\b)", 'return', 'obj'),
    (r"(?:return|returns|revive|revives|resurrect|resurrects|reanimate)\b", 'revive', 'obj'),
    (r"(?:transform|transforms|turn|turns)\b(?=[^.]*\binto\b)|becomes? an? \d+/\d+|becomes? an? (?!copy)\w+", 'transform', 'obj'),
    (r"(?:copy|copies|duplicate|duplicates)\b", 'copy', 'obj'),
    (r"(?:discard|discards)\b", 'discard', 'obj'),
    (r"(?:sacrifice|sacrifices)\b", 'sacrifice', 'obj'),
    (r"(?:mill|mills)\b", 'mill', 'obj'),
    (r"costs? (?:\(?\d+\)?|x) (?:\w+ )?less\b|reduce (?:the|its|their) cost", 'cost_reduction', 'subj'),
    (r"costs? (?:\(?\d+\)?|x) (?:\w+ )?more\b", 'cost_increase', 'subj'),
    (r"costs? \(?\d+\)?(?! (?:\w+ )?(?:less|more))", 'cost_set', 'subj'),
    (r"(?:double|doubles|triple|triples)\b", 'stat_multiply', 'obj'),
    (r"(?:lose|loses) (?:\d+|x) (?:life|health)\b", 'life_loss', 'subj_player'),
    (r"(?:lose|loses|gets?|gain|gains)\s+-(?:\d+|x)", 'stat_loss', 'subj'),
    (r"(?:set|sets)\b[^.]*\bto (?:\d+|x)\b", 'stat_set', 'obj'),
    (r"(?:play|plays|cast|casts)\b[^.]*\b(?:for free|without paying|from (?:your|the) (?:deck|graveyard))", 'free_play', 'card:deck chosen'),
    (r"(?:level up|levels up|upgrade|upgrades|evolve|evolves)\b", 'upgrade', 'subj'),
    (r"(?:reveal|reveals|look at|looks at)\b", 'information', 'obj'),
    (r"(?:purify|purifies|cleanse|cleanses|cure|cures|remove all (?:statuses|debuffs))\b", 'rewind', 'obj'),
    (r"(?:attack|attacks|strike|strikes) (?:an?|the|all|each|target|any)\b", 'attack_now', 'subj'),
    (r"(?:poison|poisons|bleed|burns?)\b(?= (?:an?|all|each|target|the|it|them)\b)", 'damage_over_time', 'obj'),
]
VERBS = [(re.compile(r"\b" + p), k, w) for p, k, w in VERBS]  # a verb starts at a word boundary ("kills" is not in "skills")
VERBSTART = re.compile(r"(?:" + '|'.join(re.sub(r"\(\?P<\w+>", '(?:', p.pattern) for p, k, w in VERBS) + r")")
SKILLDATA = re.compile(r"^(?:health \d+, move \d+\.?\s*)?(?:weapons/skills|special): ")
OPEN = [  # (opening words, trigger)
    (r"^(?:gift|battlecry|deploy|opening gambit|fanfare|play|when played|on play|when (?:you play|i'm summoned|this enters|this is played|you summon this|summoned))\b", 'on_play'),
    (r"^(?:last words|deathrattle|dying wish|deathwish|last breath|when (?:this|it|i) (?:dies|is destroyed|perishes))\b", 'death_trigger'),
    (r"^(?:whenever|when|after) (?:a|an|another|any) [^,]*?(?:dies|is destroyed|perishes)\b", 'other_death_trigger'),
    (r"^(?:production|round start|at the (?:start|beginning) of (?:your|each|the) (?:turn|round))\b", 'turn_start'),
    (r"^(?:round end|at the end of (?:your|each|the|every|your opponent's) (?:turn|round))\b", 'turn_end'),
    (r"^(?:combat|attack|strike|whenever (?:this|it)[^,]*? attacks|after (?:this|it) attacks|when (?:this|it) attacks)\b", 'on_attack'),
    (r"^(?:whenever|when|after) (?:this|it)[^,]*? (?:takes|is dealt|suffers) damage\b|^frenzy\b|^enrage\b", 'on_damaged'),
    (r"^(?:whenever|when|after) (?:this|it|your general)[^,]*? (?:deals|damages)\b", 'on_attack'),
    (r"^(?:whenever|when|after) you draw\b", 'on_draw'),
    (r"^(?:whenever|when|after) you (?:cast|play) (?:a|an) (?:spell|event)\b|^spellburst\b", 'on_spell'),
    (r"^(?:whenever|when|after) you (?:play|summon) (?:a|an|another)\b", 'on_ally_play'),
    (r"^(?:activate|order|action|tap|exert)\b", 'activated'),
    (r"^(?:corrupt|infiltrate)\b", 'territory_trigger'),
    (r"^(?:bloodbound spell)\b", 'hero_power'),
    (r"^(?:whenever|when|after|each time|the first time|at the|on your opponent's|during)\b", 'trigger'),
]
OPEN = [(re.compile(p), t) for p, t in OPEN]
OPENING = re.compile(r"^(?:(?:when(?:ever)?|at the (?:beginning|start|end)|after|each time|the first time|during|on your opponent's)\b[^,:]*[,:]"
                     r"|[\w'’/ -]{2,30}(?:\([^)]*\))?\s*(?::|\s-\s)(?!\w*:))\s*")
SPLIT = re.compile(r",? but |,? and (?=(?:then )?(?:%s|[+-]?\d+[ /]|%s\b))|,? then |, (?=(?:%s))| to (?=(?:gain|draw|deal|summon|give|destroy)\b)|\. (?=[a-z])"
                   % (VERBSTART.pattern, 'give|deal|draw|summon|gain', VERBSTART.pattern))
COND = re.compile(r"\b(?:if|unless|while|as long as|for each|equal to|for every|only if|instead)\b[^,.;:]*")
PRON = re.compile(r"^\W*(?:it|its|them|they|their|those|these|that (?:minion|creature|unit|card|ally|enemy))\b")


def who(phrase, last, opening, cat, k):
    """The target named by a phrase; pronouns point back."""
    p = phrase.strip(' ,.')
    if re.match(r"(?:an?|another|target|chosen|one|\d+) (?:\w+ )?(?:lands?|spaces?|tiles?|wells?)\b", p): return 'position chosen'
    if re.match(r"your (?!(?:other )?(?:creatures?|units?|minions?|characters?|followers?|allies|hand|deck|general|hero|god|orb|nexus|leader|base|opponent)\b)[\w'-]+", p):
        return 'card:hand chosen'  # "your Krog": that card
    if re.match(r"(?:other )?(?:friendly|allied) (?:creatures|units|minions|characters|followers)\b", p): return 'ally_unit all'
    if re.match(r"(?:other )?(?:enemy|opposing) (?:creatures|units|minions|characters|followers)\b", p): return 'enemy_unit all'
    if re.search(r"\byourself\b|\byour (?:general|hero|god|orb|nexus|leader|base)\b", p): return 'my_player'
    if re.search(r"\b(?:your opponent|the opponent|enemy (?:general|god|orb|hero|nexus|leader|base)|each opponent)\b(?!'s (?:hand|deck))", p): return 'enemy_player'
    if re.search(r"\b(?:both (?:generals|heroes|players)|each player|all players)\b", p): return 'each_player'
    if PRON.match(p) or re.fullmatch(r"(?:it|them|they)", p):
        return last or (A_from_opening(opening) if opening else 'self')
    t = A.target(p, '')
    if t: return t
    if re.search(r"\b(?:this|itself|name|~)\b", p): return 'self'
    if re.search(r"\b(?:an?|another|target|chosen|one) (?:\w+ )?(?:land|space|tile|well|row|lane)\b", p): return 'position chosen'
    if re.search(r"\b(?:an?|another|target) [\w-]+(?:'s)?\b", p): return 'any_unit chosen'
    return ''


def A_from_opening(op):
    if re.search(r"\byou draw\b|\bis drawn\b", op): return 'card:hand triggering'
    t = A.target(op, '')
    if not t or t == 'self': return 'self' if (t == 'self' or re.search(r"\bthis\b", op)) else 'any_unit triggering'
    w = t.split()[0]
    return w + ' triggering' if w.endswith('_unit') else t


def side(k, tg):
    """The effect's concept, made exact by who it hits (moving an enemy is forced movement, returning one bounces it)."""
    enemy = tg.startswith(('enemy_unit', 'enemy_player'))
    if k == 'move': return 'forced_movement' if enemy else 'terrain' if tg.startswith('position') else 'movement'
    if k == 'return': return 'bounce_enemy' if enemy else 'return_to_hand'
    if k == 'transform': return 'polymorph' if enemy else 'transform'
    if k == 'discard': return 'hand_disruption' if enemy or tg.startswith('enemy') else 'discard'
    if k == 'life_loss': return 'direct_damage' if tg == 'enemy_player' else 'life_payment'
    if k == 'damage': return 'direct_damage' if tg == 'enemy_player' else 'aoe_damage' if ' all' in tg else 'damage'
    if k == 'destroy': return 'self_destruct' if tg == 'self' else 'board_wipe' if tg.endswith(' all') and tg.startswith(('any_unit', 'enemy_unit')) else 'destroy'
    return k


def stat(amount):
    m = re.search(r"([+-]?)(\d+|x)/([+-]?)(\d+|x)", amount)
    if not m: return 'stat_gain'
    a, b = m.group(2), m.group(4)
    if m.group(1) == '-' or m.group(3) == '-': return 'stat_loss'
    return 'attack_gain' if b == '0' else 'defence_gain' if a == '0' else 'stat_gain'


def answer(s, cat, default_trigger, kwtrig, kwfx, last=''):
    """Rows for one sentence (lower case, the card's own name as 'name'), and the target last named."""
    out, trig, op = [], None, ''
    m = OPENING.match(s)
    if m:
        op = m.group(0).strip(' ,:-')
        lab = re.sub(r"\s*\([^)]*\)", '', op).strip()
        trig = kwtrig.get(lab) or next((t for rx, t in OPEN if rx.search(op)), None)
        if trig is None and re.match(r"^[\w' ]{2,30}$", lab): trig = None; op = lab  # an unknown label ("Rulebook") is no trigger
        body = s[m.end():] if trig else s
    else: body = s
    trig = trig or default_trigger
    if re.search(r"\bthe next (?:card|minion|spell|unit|creature|character)\b", body): last = 'card:hand chosen'
    cond_all = [c.group(0).strip() for c in COND.finditer(body)]
    if op and trig == 'trigger': cond_all.insert(0, op)
    if re.match(r"choose one\b", body):
        out.append(dict(trigger=trig, effect='modal_choice', target='self', shape='', amount='', duration='instant', condition='', words='choose one'))
        body = re.sub(r"^choose one\W*", '', body)
    parts = [x for x in SPLIT.split(body) if x and x.strip(' ,.')]
    verb_prev = None
    for cl in parts:
        cl = cl.strip(' ,.;')
        hit = None
        ch = re.match(r"choose (.+)$", cl)
        if ch: last = who(ch.group(1), last, op, cat, '') or last; continue  # "choose an enemy minion. it ...": names what "it" is
        for rx, k, w in VERBS:
            for mm in rx.finditer(cl):
                if re.search(r"\b(?:you|that|which|who|they|it|we) $", cl[:mm.start()]) and VERBSTART.search(cl[mm.end():]):
                    continue  # a verb inside the subject ("the first golem you summon each turn costs 1 less")
                if hit is None or mm.start() < hit[0].start(): hit = (mm, k, w)
                break
        if hit is None and verb_prev and re.match(r"[+-]?(?:\d+|x)\b", cl): hit = (re.match('', cl), verb_prev[1], verb_prev[2])  # "... and 3 to all enemies"
        if hit is None: continue
        mm, k, w = hit; verb_prev = hit
        subj, rest = cl[:mm.start()], cl[mm.start():]
        if w == 'obj':
            obj = re.search(r"\bto (.+)$", rest) if k in ('damage', 'heal') else None
            tg = who(obj.group(1) if obj else re.sub(r"^\S+\s*", '', rest), last, op, cat, k) if rest else ''
            if not tg and subj.strip(): tg = who(subj, last, op, cat, k)
        elif w in ('subj', 'subj_player'):
            tg = who(subj, last, op, cat, k) if subj.strip(' ,') else ''
            if not tg: tg = 'my_player' if w == 'subj_player' or cat in A.ONE_OFF else 'self'
        elif w == 'grant':
            g = re.match(r"\S+\s+(.*?)\b" + re.escape(mm.group('kw')), rest)
            tg = (who(g.group(1), last, op, cat, k) if g and g.group(1).strip() else '') or (who(subj, last, op, cat, k) if subj.strip() else 'self')
        elif w == 'zone':
            z = re.search(r"\b(?:to|into|in) (your|their|its owner's|the opponent's|your opponent's) (hand|deck|action bar)", cl)
            tg = ('card:' + ('hand' if z.group(2) in ('hand', 'action bar') else 'deck') + ' chosen') if z else 'my_player'
        else: tg = w
        if k == 'summon' or tg == 'position chosen':
            if re.search(r"\brandom (?:adjacent |nearby )?(?:empty )?(?:spaces?|tiles?|lands?)", rest): tg = 'position random' + (' adjacent' if re.search(r"adjacent|nearby", rest) else '')
            elif re.search(r"\b(?:adjacent|nearby)\b", rest): tg = 'position adjacent'
        amt_src = rest
        amount = ', '.join(x.group(0) for x in A.AMOUNT.finditer(amt_src))[:40]
        if k == 'stat': k = stat(amount)
        if hit[0].group(0) == '' and re.match(r"-\d", cl) and k in ('attack_gain', 'defence_gain', 'stat_gain'): k = 'stat_loss'  # "+2 attack, but -2 health"
        if k == 'keyword':
            kname = mm.group('kw')
            k = kwfx.get(kname) or {'taunt': 'taunt', 'divine shield': 'shield', 'shield': 'shield', 'stealth': 'stealth', 'lifesteal': 'lifesteal',
                                    'poisonous': 'deathtouch', 'deathtouch': 'deathtouch', 'rush': 'haste', 'charge': 'haste', 'haste': 'haste',
                                    'flying': 'evasion', 'elusive': 'evasion', 'windfury': 'multi_attack', 'celerity': 'multi_attack',
                                    'reborn': 'cheat_death', 'rebirth': 'cheat_death', 'provoke': 'taunt', 'armor': 'block_armor',
                                    'ward': 'shield', 'protection': 'shield', 'trample': 'excess_damage'}.get(kname, 'buff')
            amount = kname
        if k == 'stat_set': k = 'stat_loss' if re.search(r"\bto [01]\b", rest) else 'stat_gain'
        k = side(k, tg)
        dur = next((d for rx, d in A.DURATIONS if rx.search(cl)), None)
        conds = [c.group(0).strip() for c in COND.finditer(cl)] or cond_all
        out.append(dict(trigger=trig, effect=k, target=tg, shape='', amount=amount, duration=dur or '', condition='; '.join(conds)[:80], words=cl[:80]))
        if tg and not tg.startswith(('my_player', 'enemy_player', 'each_player', 'position')): last = tg
        if k in ('draw', 'generate_cards', 'tutor'): last = 'card:hand triggering'  # "draw a card. it costs 0"
    return out, last
