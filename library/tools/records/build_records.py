"""Effect records from hints, checked against the card's words (TAGGING_RECORDS.md, step 3, agreed 27 Oct 2026).
The card text is the truth. Hints, none trusted alone:
  tag      the entry's current tags, placed at the words they store (entity_concepts ev_form/ev_pos)
  key      the hand answer key (tools/key/<game>/key.json), placed at its quoted words
  pattern  the library's wording patterns (general, _all, the game's) matching in the sentence
  rule     this game's record rules (records/rules/<game>.txt: 'concept|regex' supports, '!concept|regex' rejects)
  keyword  the keyword records (keywords/<game>.txt), through the card's has / grants keyword links
A concept goes into a row when a rule supports it, or when two kinds of hint agree on it in the same sentence; a reject rule
keeps it out. Everything else is a difference (written to the differences file, never to the rows).
Usage: build_records.py <db> <game> [--out DIR] [--sample N]"""
import collections, json, os, random, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import auto_records as A
import compact_text as CT
from common import COLUMNS

SHAPES = [(re.compile(p), n) for p, n in [
    (r"\branks? (?:\d(?:, | and |, and )?)+", 'ranks'), (r"\b\d+ tiles?\b|\b\d+-tile\b", 'tiles'),
    (r"\b(?:in a (?:straight )?line|straight line|line of|in one straight line)\b", 'line'),
    (r"\b(?:this|that|the opposite|its|a|each|every|their) rows?\b|\bon (?:the )?(?:melee|ranged|siege) row\b", 'row'),
    (r"\b(?:this|that|a|each|every|its|another|the same) (?:lanes?|locations?|arenas?)\b", 'lane'),
    (r"\bcolumn\b", 'column'), (r"\bcone\b", 'cone'), (r"\bcross\b|\bplus shape\b", 'cross'),
    (r"\b(?:surrounding|around (?:it|the target|this|them)|radius|in a circle)\b", 'around'),
    (r"\b(?:adjacent|nearby|next to|to the (?:left|right)|left and right|beside)\b", 'adjacent'),
    (r"\b(?:opposing (?:space|creature|card|unit)|across from|opposite|in front of)\b", 'opposite'),
    (r"\bbehind\b", 'behind'), (r"\bdiagonal", 'diagonal'),
]]
SPLIT = re.compile(r"\b(?:split|divided?|distribute[ds]?)\b")
EFFECT = set(A.EFFECT_FACETS)
CHECKED = {'into_the_breach', 'inscryption', 'faeria', 'duelyst', 'darkest_dungeon'}  # tags redone in the patterns check:
# there a wording pattern alone (no tag) is only a maybe (kept as extra "maybe:<concept>"), elsewhere it makes a row
LABELS = re.compile(r"^(?:keywords?|sigils?|special|rulebook|description): ")  # labels of the source's layout, not triggers
DASHLABEL = re.compile(r"^([\w'’ ]{2,30}) - ")  # "Last Words - ...", "Gift - ...": a trigger keyword written with a dash
PROPERTY = {'ranged'}  # how a unit or weapon attacks: kept as extra, not an effect row (the keyword's own rows still carry it)
CARD_KIND = {'items_consumables', 'run_structure', 'rest_phase', 'boss_phases', 'difficulty_modifiers', 'game_rules', 'terrain'}
DATA = re.compile(r"(?:keywords?|class|availability|cooldown|counter|charges?|cost|rarity|type|tier|loot|choices|level)\s*:.*"
                  r"|(?:health|move|cooldown|charges?|level|tier|cost)\s*:?\s*\d+(?:\s*,\s*(?:health|move)\s*:?\s*\d+)*\.?")  # data lines
KEYGAMES = os.path.join(os.path.dirname(HERE), 'key')


def rules(game):
    sup, rej, f = collections.defaultdict(list), collections.defaultdict(list), os.path.join(HERE, 'rules', f'{game}.txt')
    if os.path.exists(f):
        for line in open(f, encoding='utf-8'):
            line = line.rstrip('\n')
            if not line or line.startswith('#'): continue
            k, rx = line.split('|', 1)
            (rej if k.startswith('!') else sup)[k.lstrip('!')].append(re.compile(rx, re.I))
    return sup, rej


def keyword_rows(game):
    """{keyword entity id: [record fields]} from keywords/<game>.txt."""
    out, f = collections.defaultdict(list), os.path.join(HERE, 'keywords', f'{game}.txt')
    if os.path.exists(f):
        for line in open(f, encoding='utf-8'):
            p = [x.strip() for x in line.rstrip('\n').split('|')]
            if line.startswith('#') or not p[0].isdigit(): continue
            out[int(p[0])].append((p + [''] * 8)[:8])
    return out


def sentences(rt):
    return [(m.start(), m.end()) for m in A.SENT.finditer(rt) if len(m.group(0).strip()) > 2]


def place(sents, a, b, skip=()):
    """Index of the sentence with the largest overlap with [a, b), leaving out the sentences in skip."""
    best, bi = 0, None
    for i, (x, y) in enumerate(sents):
        o = min(b, y) - max(a, x)
        if o > best: best, bi = o, i
    return None if bi in skip else bi  # words mostly on a skipped line (a keyword line, a note) belong there


CONDWORDS = re.compile(r"\b(?:if|unless|while|as long as|for each|equal to|for every|than)\b[^,.:;]*")
SUBJ = re.compile(r"(?:^|[,;] |\band |\bthen )(?P<subj>this(?: \w+)?|it|they|name|your [\w' -]+?|each [\w' -]+?|all [\w' -]+?|target [\w' -]+?|(?:an?|another|the) (?:friendly |enemy |allied |opposing |random )?[\w' -]+?|(?:friendly|enemy|allied|other|opposing) [\w' -]+?) (?:has|have|gets?|gains?|loses?|costs?|takes?|deals?|drains?|becomes?|can|cannot|can't|must|is|are|returns?|dies|attacks?|moves?)\b[^,;]*$")
SPACE = [(re.compile(r"\b(?:in|on|into) (?:a |an |\d+ |\w+ )?random (?:adjacent |empty )?(?:spaces?|tiles?|lands?|rows?|lanes?)"), 'position random'),
         (re.compile(r"\b(?:in|on|into) (?:an? |each )?(?:adjacent|nearby|empty adjacent) (?:spaces?|tiles?)|\bnearby\b"), 'position adjacent'),
         (re.compile(r"\b(?:every|each|all) (?:empty )?(?:spaces?|tiles?|lands?)"), 'position all'),
         (re.compile(r"\b(?:a|an|target|chosen) (?:empty )?(?:spaces?|tiles?|lands?|well|row|lane|location)\b"), 'position chosen')]
PLACED = {'summon', 'terrain', 'spawn_blocking', 'board_clog', 'lane_closure', 'row_effects'}  # put into or onto a place


STATS = {'stat_gain', 'attack_gain', 'defence_gain', 'temporary_buff', 'permanent_growth'}
STATAMT = re.compile(r"\+\d+/[+-]?\d+")


def from_opening(op):
    """What "it" means after a trigger opening: the card drawn, the unit that did it, or this card."""
    if re.search(r"\byou draw\b|\bis drawn\b", op): return 'card:hand triggering'
    t = A.target(op, '')
    if t == 'self' or not t: return 'self' if t == 'self' or re.search(r"\bthis\b", op) else 'any_unit triggering'
    who = t.split()[0]
    return who + ' triggering' if who.endswith('_unit') else t


def blank_conditions(s):
    """The sentence with its conditions blanked (same length), so their words name no target."""
    return CONDWORDS.sub(lambda m: ' ' * len(m.group(0)), s)


def pick_target(k, s, a, b, skip_to, cat, last_tg, tags, anc, last_fx=''):
    """Who an effect at s[a:b] hits. The words win over hints: the subject of the clause ("this gains", "your Krog costs"),
    else the object after the effect, a pronoun meaning the last target, a place for things put somewhere, then the effect's
    usual target and the side and scope from the card's tags."""
    a = max(a, skip_to)
    span, before = s[a:b], s[skip_to:a]
    if last_fx in ('draw', 'generate_cards', 'tutor', 'copy') and re.match(r"\W*(?:they|it|them|those|these)\b", s[skip_to:]):
        return 'card:hand triggering'  # "draw a card. it costs 0": the card drawn
    if k in PLACED:
        for rx, t in SPACE:
            if rx.search(span): return t
    m = SUBJ.search(s[skip_to:min(len(s), a + 12)])
    if m and re.search(r"\bdeals?\b", m.group(0)[len(m.group('subj')):len(m.group('subj')) + 8]): m = None  # who deals is not who is hit
    if m:
        subj = m.group('subj')
        if subj.startswith('your ') and not A.target(subj, ''): return 'card:hand chosen'  # "your Krog costs less": that card
        if subj in ('it', 'they'): return last_tg or (from_opening(s[:skip_to]) if skip_to else 'self')
        t = A.target(subj, '') or ('self' if subj.startswith('this') or subj == 'name' else '')
        if t: return t
    obj = A.target(span[:60], '')
    if not obj and re.search(r"\b(?:a|an|another|target) (?:nearby |friendly |enemy |allied )?[\w-]+'s\b", span[:60]): obj = 'any_unit chosen'
    if re.search(r"\bthe next (?:card|minion|spell|unit|creature)\b", s[skip_to:b]) and not obj: return 'card:hand chosen'
    pm = A.PRONOUN.search(span[:40])
    if pm and (not obj or span.find(pm.group(0)) < span.find(next((x for x in span.split() if A.target(x, '')), '~~'))):
        if last_fx in ('draw', 'generate_cards', 'tutor', 'copy'): return 'card:hand triggering'
        return last_tg or from_opening(s[:skip_to])
    if re.search(r"\byourself\b", span[:50]): return 'my_player'
    if obj: return obj
    if A.OWN.get(k) == 'my_player': return 'my_player'
    if re.match(r"(?:has|have|gets?|gains?|costs?|loses?|takes?)\b", span) and cat not in A.ONE_OFF: return 'self'
    if re.search(r"\bthis\b(?! (?:turn|round|game|way|phase|combat|match))", span[:40]): return 'self'
    return A.target('', before) or A.OWN.get(k, '') or ('self' if 'scope_self' in tags else '') \
        or ('self' if cat not in A.ONE_OFF and k in A.LASTING else '') or A.hinted(k, tags, anc)


def shape_of(span):
    for rx, n in SHAPES:
        m = rx.search(span)
        if m: return n if n not in ('tiles', 'ranks') else m.group(0).strip(' ,')
    return ''


class Game:
    def __init__(self, c, game):
        self.c, self.g = c, game
        self.facet, self.anc, self.pats = A.load(c)
        self.prep = A.prep(c, game, self.facet, self.pats)
        self.sup, self.rej = rules(game)
        self.anypat = collections.defaultdict(list)
        for (k, g2), rxs in self.pats.items(): self.anypat[k] += rxs
        self.kwrows = keyword_rows(game)
        self.kwname = dict(c.execute("SELECT id, lower(name) FROM entities WHERE game=? AND category='keyword'", (game,)))
        self.kwid = {}
        for i, n in sorted(self.kwname.items()):
            self.kwid.setdefault(n, i); self.kwid.setdefault(re.sub(r"\s*\([^)]*\)$", '', n), i)
        kf = os.path.join(KEYGAMES, game, 'key.json')
        self.key = json.load(open(kf)) if os.path.exists(kf) else {}
        self.links = collections.defaultdict(list)
        for s, rel, d in c.execute("SELECT l.src, l.rel, l.dst FROM entity_links l JOIN entities x ON x.id=l.dst "
                                   "WHERE x.game=? AND x.category='keyword' AND l.rel IN ('has_keyword','grants_keyword')", (game,)):
            self.links[s].append((rel, d))
        self.tags = collections.defaultdict(list)
        for e, k, role, meth, f, p, l in c.execute("SELECT e.entity, e.concept, e.role, e.method, e.ev_form, e.ev_pos, e.ev_len "
                                                   "FROM entity_concepts e JOIN entities x ON x.id=e.entity WHERE x.game=?", (game,)):
            self.tags[e].append((k, role, meth, f, p, l))

    def concepts_with_patterns(self):
        return [k for k in self.facet if self.facet[k] != 'problem' and ((k, None) in self.pats or (k, self.g) in self.pats or (k, '_all') in self.pats)]

    def entry(self, e, name, cat, text):
        """(rows, differences) for one entry."""
        g, rt = self.g, CT.read_text(self.g, name, text)
        sents = sentences(rt)
        kwre = self.prep[0]
        linked = {self.kwname.get(d, '') for _, d in self.links.get(e, [])}
        traits, named = [], set()
        skip = set()  # notes, data lines, and keyword lines whose keywords the card is linked to (their rows come from the links)
        for i, (x, y) in enumerate(sents):
            s0 = rt[x:y].strip()
            if s0.startswith('(') or '(same as the unevolved form' in s0: skip.add(i)
            elif DATA.fullmatch(s0.strip(' .;')) and not re.search(r'\b(?:deal|damage|gain|draw|give|summon|destroy|push)', s0): skip.add(i)
            elif re.match(r"traits?: ", s0): skip.add(i); traits.append(s0)  # what the card is, kept as card facts
            elif kwre is not None and kwre.fullmatch(LABELS.sub('', s0.strip(' .,'))):
                skip.add(i)
                for w in re.split(r"[,.]| and ", LABELS.sub('', s0.strip(' .,'))):
                    w = re.sub(r"[: ]*[+-]?\d+\+?$| x$|\s*\([^)]*\)$", '', w.strip())
                    if w in self.kwid: named.add(self.kwid[w])
        hint = collections.defaultdict(lambda: collections.defaultdict(set))  # sentence -> concept -> hint kinds
        pos = collections.defaultdict(dict)                                    # sentence -> concept -> first position
        role = {}
        unplaced, windows = [], []
        def add(i, k, kind, at):
            hint[i][k].add(kind)
            if at is not None and (k not in pos[i] or at < pos[i][k]): pos[i][k] = at
        for k, r, meth, f, p, l in self.tags[e]:
            role.setdefault(k, r)
            if f == 1 and l: win = (p, p + l)
            elif f == 0 and l:
                w = (text or '')[p:p + l].lower().strip()
                j = rt.find(w) if len(w) > 3 else -1
                win = (j, j + len(w)) if j >= 0 else None
            else: win = None
            if win is None: unplaced.append((k, r, meth, CT.evidence_text(self.c, e, f, p, l) or ''))
            else: windows.append((k, win))
        for k, words in self.key.get(str(e), {}).get('tags', []):
            w = (words or '').lower().replace((name or '').lower(), 'name')
            j = rt.find(w) if len(w) > 3 else -1
            if j >= 0 and place(sents, j, j + len(w), skip) is not None: add(place(sents, j, j + len(w), skip), k, 'key', j)
            else: unplaced.append((k, 'does', 'key', words))
        pk = self.concepts_with_patterns()
        for i, (x, y) in enumerate(sents):
            if i in skip: continue
            s = rt[x:y]
            for k in pk:
                f = A.find(self.pats, k, g, s)
                if f: add(i, k, 'pattern', x + f[0][0])
            for k, rxs in self.sup.items():
                for rx in rxs:
                    m = rx.search(s)
                    if m: add(i, k, 'rule', x + m.start())
            for k, rxs in self.rej.items():
                if k in hint[i] and any(rx.search(s) for rx in rxs): hint[i][k].add('reject')
        # a tag's stored words are a window around the match: it goes to the sentence in that window where a pattern of the
        # same or a related concept matches, else to the sentence the window overlaps most
        rel0 = lambda a, b: a == b or b in self.anc.get(a, ()) or a in self.anc.get(b, ())
        for k, (a, b) in windows:
            cand = [i for i, (x, y) in enumerate(sents) if i not in skip and min(b, y) > max(a, x) and any(rel0(k, o) for o in hint[i])]
            i = cand[0] if cand else place(sents, a, b, skip)
            if i is not None: add(i, k, 'tag', max(a, sents[i][0]) if not cand else None)
        # a tag with no stored words (a hand review) goes to the sentence where a hint of the same or a related concept is,
        # or to the only sentence; card-level facts (from the cost field, the game's structure) go on every row as extra
        rel = lambda a, b: a == b or b in self.anc.get(a, ()) or a in self.anc.get(b, ())
        CARD_LEVEL = ('data_rule', 'game_structure', 'engine_rule')
        card_facts, still = [], []
        for k, r, meth, ev in unplaced:
            if meth in CARD_LEVEL: card_facts.append(k); continue
            if meth in ('claude_review', 'restored', 'answer_key', 'via_link', 'text_pattern'):
                where = [i for i in hint if i not in skip and any(rel(k, o) for o in hint[i])]
                if not where:  # the concept's wording in any game's patterns
                    rx = self.anypat.get(k, [])
                    where = [i for i, (x, y) in enumerate(sents) if i not in skip and any(r.search(rt[x:y]) for r in rx)]
                if not where and len(sents) - len(skip) == 1: where = [i for i in range(len(sents)) if i not in skip]
                if where: add(where[0], k, 'tag', None); continue
            still.append((k, r, meth, ev))
        unplaced = still
        # hints on related concepts (a parent and its child in the tree) agree: the narrower concept takes both
        for i in list(hint):
            ks = list(hint[i])
            for k in ks:
                for o in ks:
                    if o != k and o in self.anc.get(k, ()):
                        hint[i][k] |= hint[i][o] - {'covered'}; hint[i][o].add('covered')
        rows, diffs = [], []
        kwre, allfx, kwfx, kwgrant, kwtrig = self.prep
        prev, ab, last_tg, last_fx, leftover = None, 0, '', '', []
        tagset = {k for k, *_ in self.tags[e]}
        for i, (x, y) in enumerate(sents):
            if i in skip: continue
            s = LABELS.sub('', rt[x:y].strip().lstrip('•*-– ').strip())
            body = s
            need = {'rule', 'tag'} if g in CHECKED else {'rule', 'tag', 'pattern'}
            ok = {k for k, h in hint[i].items() if 'reject' not in h and 'covered' not in h and h & need}
            maybe = sorted(k for k, h in hint[i].items() if k not in ok and 'covered' not in h and 'reject' not in h and 'pattern' in h
                           and self.facet.get(k) in EFFECT and k not in A.SKIP)
            # words inside a condition ("if it's a flying creature", "for each forest") are the condition, not an effect;
            # keywords inside what a summon or create makes describe the new card
            cspans = [(x + m.start(), x + m.end()) for m in re.finditer(r"\b(?:if|unless|while|as long as|for each|equal to|whenever|when|with (?:a|an|the) \w+|than)\b[^,.:;]*", rt[x:y])]
            made = [(pos[i][o], y) for o in ok if o in A.OBJECT_FX and o in pos[i]]
            moved = {}
            for k in list(ok):
                at = pos[i].get(k)
                if at is None or self.facet.get(k) not in EFFECT or 'rule' in hint[i][k]: continue
                if any(a < at < b for a, b in cspans): moved[k] = 'condition'
                elif any(a < at < b for a, b in made) and k not in A.OBJECT_FX: moved[k] = 'made'
            ok -= set(moved)
            for k, h in hint[i].items():
                if k not in ok and k not in moved and 'covered' not in h: diffs.append((e, i, k, '+'.join(sorted(h)), s[:160]))
            trig = [k for k in ok if self.facet.get(k) == 'trigger']
            trig.sort(key=lambda k: pos[i].get(k, 9e9))
            op = A.OPENING.match(body) or DASHLABEL.match(body); lab = A.LABEL.match(body) or DASHLABEL.match(body)
            t = trig[0] if trig else (kwtrig.get(lab.group(1).strip()) if lab else None)
            if not t and (re.match(r"(?:weapons/skills|pilot ability|skill)\b", body) or (g == 'into_the_breach' and cat == 'ability')):
                t = 'activated'  # a weapon or skill is used by the player
            if t or op: ab += 1; t = t or 'trigger'
            elif prev: t = prev
            else: t = 'on_play' if cat in A.ONE_OFF else 'passive'; ab += 1
            prev = t if t != 'passive' else None
            skip_to = op.end() if op else 0
            fx = [k for k in ok if self.facet.get(k) in EFFECT and k not in A.SKIP and k not in CARD_KIND - {'terrain'} and k not in PROPERTY
                  and role.get(k, 'does') in ('does', 'grants', 'trigger')]
            fx = [k for k in fx if not any(o != k and k in self.anc.get(o, ()) for o in fx)]  # keep the narrowest
            fx.sort(key=lambda k: pos[i].get(k, 9e9))
            other = sorted(k for k in ok if k not in fx and k not in trig and not any(k in self.anc.get(o, ()) for o in fx))
            extra = ', '.join([f'{v}:{k}' for k, v in sorted(moved.items())]
                              + [f'maybe:{k}' for k in maybe] + [('cost:' if role.get(k) == 'cost' else f'{role[k]}:' if role.get(k) in ('benefits', 'counters') else '') + k for k in other])
            dur = next((d for rx, d in A.DURATIONS if rx.search(s)), None)
            conds = [m.group(0).strip() for m in A.COND.finditer(s)]
            if op and t == 'trigger': conds.insert(0, op.group(0).strip(' ,:'))
            plain = blank_conditions(s)
            for n, k in enumerate(fx):
                a = max(0, pos[i].get(k, x) - x)
                nxt = min([max(0, pos[i][o] - x) for o in fx[n + 1:] if o in pos[i] and pos[i][o] - x > a] or [len(s)])
                span = s[a:nxt]
                tg = pick_target(k, plain, a, nxt, skip_to, cat, last_tg, tagset | set(hint[i]), self.anc, last_fx)
                last_fx = k
                cut = re.search(r",| unless | if | as long as | instead\b", span[1:])
                am = ', '.join(m.group(0) for m in A.AMOUNT.finditer(span[:cut.start() + 1] if cut else span))[:40]
                if SPLIT.search(span): am = ('split ' + am).strip()
                d = dur or ('while' if t in ('passive', 'aura') else 'permanent' if k in A.LASTING else 'instant')
                if d in ('n_turns', 'n_rounds'):
                    nm = re.search(r'for (\d+|two|three|four)', s); am += '; ' + (A.WORDNUM.get(nm.group(1), nm.group(1)) if nm else 'N')
                kinds = '+'.join(sorted(hint[i][k] - {'reject'}))
                if k in STATS and len(STATAMT.findall(s)) > 1:  # "+1/+1 while ... and +0/+2 while ...": one row per amount
                    if any(o in STATS for o in fx[:n]): continue
                    for xm in STATAMT.finditer(s):
                        xa = xm.group(0); cm = re.match(r"[^,.;]*?\b(?:while|if|as long as|for each)\b[^,.;]*?(?= and |$|[,.;])", s[xm.end():])
                        k2 = 'attack_gain' if re.fullmatch(r"\+\d+/\+?0", xa) else 'defence_gain' if re.fullmatch(r"\+?0/\+\d+", xa) else 'stat_gain' if k in ('attack_gain', 'defence_gain') else k
                        rows.append((e, ab, t, k2, tg or '', shape_of(span), xa, d, (cm.group(0).strip() if cm else '; '.join(conds))[:80], extra, kinds, ''))
                    continue
                rows.append((e, ab, t, k, tg or '', shape_of(span), am.replace('name', name or '~'), d, '; '.join(conds)[:80], extra, kinds, ''))
                if tg and not tg.startswith(('my_player', 'position', 'each_player')): last_tg = tg
            if not fx and not any(self.facet.get(k) in EFFECT for k in hint[i]): diffs.append((e, i, '-', 'no hint', s[:160]))
            if not fx: leftover.extend(other + [f'{v}:{k}' for k, v in moved.items()])  # a sentence with no effect row: kept on the card
        # keyword rows through the card's own keyword links
        uses = [('has_keyword', d) for d in sorted(named)]
        for rel, d in self.links.get(e, []):
            nm = self.kwname.get(d, '')
            if d not in named and nm and re.search(rf"\b{re.escape(nm)}\b", rt): uses.append((rel, d))  # a link counts only where the text names it
        for rel, d in uses:
            nm = self.kwname.get(d, '')
            for kr in self.kwrows.get(d, []):
                ka, kt, kfx, ktg, kam, kdur, kcond = kr[1:8]
                if not kfx: continue  # a trigger or condition keyword: it set the trigger or condition of its sentence
                m = re.search(rf"\b{re.escape(nm)}\b[ :(]*([+-]?\d+)", rt)
                if m and 'N' in kam: kam = kam.replace('N', m.group(1))
                if rel == 'grants_keyword':
                    j = rt.find(nm); i = place(sents, j, j + len(nm)) if j >= 0 else None
                    ktg = A.target(rt[sents[i][0]:sents[i][1]], '') if i is not None else ''
                    kt = 'passive'
                rows.append((e, 'kw', '' if kt == '-' else kt, kfx, ktg, '', kam, kdur, kcond, '', 'keyword', nm))
        keep = sorted({k for k, r, meth, ev in unplaced if meth != 'key' and self.facet.get(k) != 'problem'})
        tr = {k for k, (a, b) in windows if any(min(b, sents[i][1]) > max(a, sents[i][0]) for i in range(len(sents)) if rt[sents[i][0]:sents[i][1]].strip().startswith(('trait', 'traits')))}
        keep = [f'card:{k}' for k in sorted(set(card_facts) | tr) if self.facet.get(k) != 'problem'] + ['tag:' + k for k in keep if k not in tr]
        keep += sorted(set(leftover) - set(keep))
        if traits: keep.append('traits: ' + '; '.join(t.split(':', 1)[1].strip(' .') for t in traits)[:80])
        if keep and not rows: rows = [(e, 'card', '', '', '', '', '', '', '', '', 'tag', '')]  # nothing else: the card's facts alone
        if keep:
            rows = [x[:9] + ((x[9] + ', ' if x[9] else '') + ', '.join(keep),) + x[10:] for x in rows]
        for k, r, meth, ev in unplaced:
            if self.facet.get(k) == 'problem': continue
            if meth == 'via_keyword' and self.links.get(e): continue  # the keyword's own rows carry it
            diffs.append((e, None, k, f'unplaced {meth}', ev[:160]))
        return rows, diffs

    def run(self, outdir=None, sample=0):
        rows = self.c.execute("SELECT id, name, category, text FROM entities WHERE game=? AND category NOT IN ('keyword','tribe') "
                              "AND text IS NOT NULL AND text != ''", (self.g,)).fetchall()
        allr, alld, res = [], [], {}
        for e, nm, cat, t in rows:
            if self.g == 'darkest_dungeon' and cat in ('ability', 'item', 'monster', 'status', 'event'):
                r, d = dd_entry(self, e, nm, cat, t)
            else: r, d = self.entry(e, nm, cat, t)
            res[e] = (r, d); allr += r; alld += d
        clean = sum(1 for r, d in res.values() if r and not d)
        tags = sum(1 for e, *_ in rows for k in {x[0] for x in self.tags[e]} if self.facet.get(k) != 'problem')
        def held(e, k):
            for r in res[e][0]:
                if k == r[2] or k == r[3] or re.search(rf"(?:^|[ :,]){re.escape(k)}(?:,|$)", r[9] or ''): return True
                if k in self.anc.get(r[3], ()) or k in self.anc.get(r[2], ()): return True
                if r[10] == 'keyword': return True if any(k == x[3] for x in []) else None
            return False
        kwk = collections.defaultdict(set)
        for e, *_ in rows:
            for rel, d in self.links.get(e, []):
                for kr in self.kwrows.get(d, []): kwk[e] |= {kr[2], kr[3]}
        lost = sum(1 for e, *_ in rows for k in {x[0] for x in self.tags[e]}
                   if self.facet.get(k) != 'problem' and not held(e, k) and k not in kwk[e]
                   and not any(m == 'via_keyword' for kk, _, m, *_ in self.tags[e] if kk == k))
        print(f'{self.g:16} entries {len(rows):5}  rows {len(allr):6}  entries with no difference {100 * clean / len(rows):5.1f}%  '
              f'differences {len(alld):5}  tags not in a row {lost} of {tags}')
        if outdir:
            os.makedirs(outdir, exist_ok=True)
            with open(os.path.join(outdir, f'{self.g}.tsv'), 'w') as f:
                f.write('\t'.join(COLUMNS) + '\n')
                for r in allr: f.write('\t'.join(str(x) for x in r) + '\n')
            with open(os.path.join(outdir, f'{self.g}.diff.tsv'), 'w') as f:
                for d in alld: f.write('\t'.join(str(x) for x in d) + '\n')
        return rows, res


DD_CONTEXT = {'items_consumables', 'run_structure', 'rank_positions', 'ranged', 'rest_phase', 'cooldowns', 'upkeep', 'board_limit',
              'light_level', 'traits_quirks', 'drawback', 'saving_throws', 'stress_morale', 'speed'}  # what the card is, not a row


DD_NAMES = [(r"resistance", 'immunity'), (r"resistance", 'saving_throws'), (r"death_blow|death's door", 'cheat_death'),
            (r"bleed|blight|poison", 'damage_over_time'), (r"heal", 'heal'), (r"stress", 'stress_morale'), (r"speed", 'speed'),
            (r"\bmark", 'mark_target'), (r"\bmove", 'movement'), (r"stun", 'disable'), (r"debuff", 'debuff')]


def dd_entry(G, e, nm, cat, t):
    """Darkest Dungeon's fixed formats (auto_records.dd_records), with the skill's target ranks as shape, compared with the tags."""
    r, unread = A.dd_records(e, cat, t)
    ranks = [m.group(0) for m in re.finditer(r"targets (?:all of )?(?:enemy|ally) ranks [\d, ]+", (t or '').lower())]
    out = []
    for x in r:
        sh = ''
        if isinstance(x[1], int) and 0 < x[1] <= len(ranks): sh = re.sub(r'^targets (?:all of )?(?:enemy|ally) ', '', ranks[x[1] - 1]).strip(' ,')
        out.append((x[0], x[1], x[2], x[3], x[4], sh, x[5], x[6], x[7], '', 'script', ''))
    got = {x[3] for x in out}
    for x in out:  # what a stat row's words name (a resistance, death's door, a bleed chance) is the concept the tags say
        got |= {k for rx, k in DD_NAMES if re.search(rx, str(x[5]))}
    diffs, extra = [], []
    for k, role, meth, f, p, l in G.tags[e]:
        if G.facet.get(k) == 'problem' or any(k == g or k in G.anc.get(g, ()) or g in G.anc.get(k, ()) for g in got): continue
        extra.append(('tag:' if G.facet.get(k) in EFFECT and k not in A.SKIP else '') + k)  # kept on the rows, nothing lost
        if G.facet.get(k) in EFFECT and k not in A.SKIP and role in ('does', 'grants') and k not in DD_CONTEXT:
            diffs.append((e, None, k, f'tag only ({meth})', (CT.evidence_text(G.c, e, f, p, l) or '')[:160]))
    ex = ', '.join(sorted(set(extra)))
    out = [x[:9] + (ex,) + x[10:] for x in out]
    diffs += [(e, None, '-', 'unread', '')] * unread
    return out, diffs


if __name__ == '__main__':
    a = sys.argv[1:]
    outdir = a[a.index('--out') + 1] if '--out' in a else None
    sample = int(a[a.index('--sample') + 1]) if '--sample' in a else 0
    c = sqlite3.connect(a[0])
    for g in [x for x in a[1:] if not x.startswith('--') and x != outdir and not x.isdigit()]:
        Game(c, g).run(outdir, sample)
