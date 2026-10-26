"""Step 2 of the test: pour each entry's tags into rows, one trigger with the effects it causes, read in text order.
- A row ends at a line break, a named block ("Leader:", "Deathrattle:", "When Played:") or a full stop, unless the next sentence
  continues it ("If you do", "Then", "It", "That unit", "Otherwise", "Instead", a lower-case start after ';').
- A trigger tag starts a new row when the current row already has a trigger and an effect after it; triggers joined before
  their effect ("Battlecry and Deathrattle:") share a row. Effects with no trigger before them form a static row.
- Tags from a keyword (method via_keyword, or words in a keyword list) form one row per keyword.
- Tags without words, and cost/structure tags, go in one card-level row.
Pairs: every trigger of a row with every effect of the row (a trigger concept is never the effect) -> records_pairs.
Compounds, computed per sentence and row (Claude's rules and wording lists, DUR and AREA below):
  temporary_buff: a buff in a sentence with duration words or a temporary tag; aoe_damage: damage in a sentence with area
  words or a many-targets tag; permanent_growth: a stat gain of the card itself (SELF) without duration words in a row whose trigger repeats.
  A compound tag with no words is kept as stored. -> records_compound(entity, concept, how).
Tables: rows(id, entity, ord, kind, ev_pos, ev_len), row_tags(rid, row, cross). Usage: rows.py <copy.sqlite>"""
import bisect, collections, re, sys
import common as C

PREFIX_WORDS = ['Gift', 'Battlecry', 'Deathrattle', 'Deploy', 'Last Words', 'Fanfare', 'Last Breath', 'Dying Wish', 'Deathwish',
                'On Reveal', 'Opening Gambit', 'Play', 'Slay', 'Strike', 'Nexus Strike', 'Clash', 'Attack', 'Rally', 'Round Start',
                'Round End', 'Start of Turn', 'End of Turn', 'Production', 'When Destroyed']   # the agreed ones + trigger_pairs.py's EXTRA
SENT = re.compile(r'(?<=[.!?;])\s+(?=\S)')
BLOCK = re.compile(r"(?:^|(?<=\s))(?<!and )(?<!or )(?:(?:" + '|'.join(PREFIX_WORDS) + r")\s*[:\-–—]\s"
                   r"|(?:\{[^}]+\}[, ]*)+:"
                   r"|[A-Z][\w'’\-]*(?:\s+(?:of|the|and|in|on|to|a|an|[A-Z][\w'’\-]*)){0,5}(?:\s*\([^)]{1,40}\))?(?:\s*\[[^\]]{1,30}\])?:\s)")
CONT = re.compile(r"^(?:[a-z]|if (?:you do|it|they|that|this|so|not)\b|then\b|otherwise\b|instead\b|it\b|its\b|they\b|them\b|those\b|that\b|"
                  r"this (?:way|unit|minion|creature|model|character|card|follower|ally)\b|when you do\b|repeat\b|do this\b|also\b)", re.I)
DUR = re.compile(r"\b(?:this (?:turn|round|combat|phase|fight)|until (?:the )?end of (?:the |your |this |that )?(?:turn|round|phase|combat|battle)|"
                 r"until end of turn|until your next turn|for the rest of the (?:turn|round|phase|battle))\b", re.I)
AREA = re.compile(r"\b(?:all|each|every)\b(?:\s+\w+){0,3}?\s+(?:enem\w*|minions?|creatures?|units?|characters?|followers?|models?|others?|"
                  r"players?|opponents?|tiles?|allies|allied|monsters?|lanes?)\b|\badjacent\b|\bsplash\b|\bin (?:a|the|its|that) (?:row|lane|area)\b", re.I)
ONCE = {'on_play', 'death_trigger', 'leave_trigger', 'start_of_game', 'once_per_game', 'trap_secret', 'delayed', 'turn_number',
        'game_end_trigger', 'other_leave_trigger', 'passive', 'aura', 'trigger'}   # Claude's: triggers that do not repeat for one card
SELF = re.compile(r"\b(?:this|it|itself|i|name|he|she)\b(?:\s+\w+){0,2}\s+(?:gains?|gets?|grows?)\b|\bgain \+|\bgrows?\b", re.I)   # Claude's: the card itself grows
GAIN = {'stat_gain', 'attack_gain', 'defence_gain', 'permanent_growth', 'temporary_buff'}

def units(text):
    """sentences cut again at named blocks: (start, end, starts_block)"""
    out = []
    for line in re.finditer(r'[^\n]+', text):
        a0 = line.start(); s = line.group(0); first = True
        cuts = [0] + [m.end() for m in SENT.finditer(s)]
        for x, y in zip(cuts, cuts[1:] + [len(s)]):
            pts = [x] + [x + m.start() for m in BLOCK.finditer(s[x:y]) if m.start() > 0] + [y]
            for j, (u, v) in enumerate(zip(pts, pts[1:])):
                seg = s[u:v]; lead = len(seg) - len(seg.lstrip()); seg = seg.strip()
                if seg: out.append((a0 + u + lead, a0 + u + lead + len(seg), first or j > 0 or bool(BLOCK.match(seg)), x))
                first = False
    return out

def main(path):
    c = C.connect(path); eff, trig = C.concept_kinds(c)
    trig_any = {i for (i,) in c.execute("SELECT id FROM concept_tree WHERE root='trigger'")}
    dmg = C.subtree(c, 'damage'); buff = C.subtree(c, 'buff') - {'temporary_buff', 'permanent_growth'}
    many = C.subtree(c, 'scope_multi') | {'board_wipe'}
    c.executescript('DROP TABLE IF EXISTS rows; CREATE TABLE rows(id INTEGER PRIMARY KEY, entity INT, ord INT, kind TEXT, ev_pos INT, ev_len INT);'
                    'DROP TABLE IF EXISTS row_tags; CREATE TABLE row_tags(rid INT PRIMARY KEY, row INT, cross INT);'
                    'DROP TABLE IF EXISTS records_pairs; CREATE TABLE records_pairs(entity INT, row INT, trigger TEXT, effect TEXT);'
                    'DROP TABLE IF EXISTS records_compound; CREATE TABLE records_compound(entity INT, concept TEXT, how TEXT);')
    kw = collections.defaultdict(set)
    for g, n in c.execute("SELECT game, name FROM entities WHERE category='keyword'"):
        n = re.sub(r'\([^)]*\)', '', n or '').strip().lower()
        if n: kw[g].add(n)
    ent = {i: (g, t or '') for i, g, t in c.execute('SELECT id, game, text FROM entities')}
    tags = collections.defaultdict(list)
    for rid, e, k, meth, how, pos, ln in c.execute('SELECT ec.rowid, ec.entity, ec.concept, ec.method, w.how, w.pos, w.len FROM entity_concepts ec JOIN tag_words w ON w.rid=ec.rowid'):
        tags[e].append((rid, k, meth, how, pos, ln))
    R, RT, PR, CP = [], [], [], []
    nid = [0]
    def new_row(e, o, kind, a, b):
        nid[0] += 1; R.append([nid[0], e, o, kind, a, b]); return R[-1]
    for e, lst in tags.items():
        g, text = ent[e]; U = units(text) if text.strip() else []
        starts = [u[0] for u in U]
        def unit_of(p):
            j = bisect.bisect_right(starts, p) - 1; return max(j, 0)
        order = 0; rows_of = collections.defaultdict(list)
        card = None; kwrows = {}
        worded = []
        for t in lst:
            rid, k, meth, how, pos, ln = t
            if pos is None or not U:
                if card is None: card = new_row(e, -1, 'card', None, None)
                RT.append((rid, card[0], 0)); rows_of[card[0]].append(t); continue
            u = U[unit_of(pos)]; body = text[u[0]:u[1]]
            parts = [p.strip(' .').lower() for p in re.sub(r'^[^:]{0,30}:\s*', '', body).split(',')]
            parts = [re.sub(r'\s+[\dX+]+$', '', re.sub(r'\([^)]*\)', '', p)).strip() for p in parts]
            w = re.sub(r'[\s\d+X]+$', '', text[pos:pos + ln].lower().strip(' .,'))
            prefix = bool(re.match(r'(?:\s*[\dX+]*\s*|\s+(?:and|or)\s+[A-Z][\w ]{0,20}?)[:\-–—]\s', text[pos + ln:pos + ln + 30]))   # "Battlecry:", "Battlecry and Deathrattle:"
            before = [re.sub(r'[\s\dX+]+$', '', re.sub(r'\([^)]*\)', '', x)).strip().lower() for x in re.sub(r'^[^:,.]{0,30}:\s*', '', text[u[0]:pos]).split(',')]
            own = all(not x or x in kw[g] for x in before) or all(x in kw[g] for x in before[:-1]) and before[-1] in kw[g] | {''}   # only keyword names before it: a keyword the card has
            if not prefix and own and (w in kw[g] or meth == 'via_keyword' or how == 'keyword' or (len(parts) > 1 and all(p in kw[g] for p in parts))):
                hit = next((r for (a, b), r in kwrows.items() if a < pos + ln and pos < b), None)   # one row per keyword: overlapping words share it
                if hit is None: hit = kwrows[(pos, pos + ln)] = new_row(e, -2, 'keyword', pos, ln)
                RT.append((rid, hit[0], 0)); rows_of[hit[0]].append(t); continue
            worded.append(t)
        cur = None; cur_unit = None; has_t = has_e = False; last_e = last_t = -1
        for t in sorted(worded, key=lambda x: (x[4], x[0])):
            rid, k, meth, how, pos, ln = t; j = unit_of(pos); u = U[j]
            if cur is not None and j != cur_unit:   # a new sentence or block: does it continue the row?
                for jj in range(cur_unit + 1, j + 1):
                    if U[jj][2] or not CONT.match(text[U[jj][0]:U[jj][1]]): cur = None; break
            is_t = k in trig_any
            if cur is not None and is_t and has_t and last_e > last_t: cur = None   # an effect since the last trigger: a new trigger starts a new row
            if cur is None:
                order += 1; cur = new_row(e, order, 'static', u[0], u[1] - u[0]); has_t = has_e = False; last_e = last_t = -1
            cur_unit = j; cur[5] = max(cur[4] + cur[5], u[1]) - cur[4]
            if is_t: has_t = True; cur[3] = 'trigger'; last_t = max(last_t, pos)
            elif k in eff and how != 'excerpt': has_e = True; last_e = pos   # an excerpt's words are unknown: its position decides nothing
            RT.append((rid, cur[0], int(pos + ln > cur[4] + cur[5] and pos + ln > u[1]))); rows_of[cur[0]].append(t)
        # pairs and compounds
        have = {k for _, k, _, _, _, _ in lst}; made = set()
        for r, ts in rows_of.items():
            ks = {t[1] for t in ts}
            for a in ks & trig:
                for b in (ks & eff) - trig_any:
                    if a != b: PR.append((e, r, a, b))
        sent_of = {}   # the whole sentence (all its blocks) each worded tag sits in
        for rid, k, meth, how, pos, ln in lst:
            if pos is None or not U: continue
            u = U[unit_of(pos)]; line_start = text.rfind('\n', 0, u[0]) + 1
            s0 = line_start + u[3]; s1 = next((m.start() + s0 for m in SENT.finditer(text, s0) if m.start() >= u[1]), None)
            nl = text.find('\n', u[0]); s1 = min(x for x in (s1, nl if nl >= 0 else None, len(text)) if x is not None)
            sent_of[rid] = (s0, s1)
        by_sent = collections.defaultdict(set)
        for rid, k, meth, how, pos, ln in lst:
            if rid in sent_of: by_sent[sent_of[rid]].add(k)
        for (s0, s1), ks in by_sent.items():
            st = text[s0:s1]
            if ks & (buff | {'temporary_buff'}) and (DUR.search(st) or ks & {'temporary_effect', 'temporary_buff'}): made.add(('temporary_buff', 'sentence'))
            if ks & dmg and (AREA.search(st) or ks & (many | {'aoe_damage'})): made.add(('aoe_damage', 'sentence'))
        for r, ts in rows_of.items():
            ks = {t[1] for t in ts}
            if not ks & (trig - ONCE): continue
            for rid, k, meth, how, pos, ln in ts:
                st = text[sent_of[rid][0]:sent_of[rid][1]] if rid in sent_of else ''
                if k in GAIN - {'temporary_buff'} and st and not DUR.search(st) and SELF.search(st):
                    made.add(('permanent_growth', 'row')); break
        for rid, k, meth, how, pos, ln in lst:   # a compound tag the text gives no words for stays as stored
            if k in ('temporary_buff', 'aoe_damage', 'permanent_growth') and pos is None: made.add((k, 'stored, no words'))
        for k, h in made: CP.append((e, k, h))
    c.executemany('INSERT INTO rows VALUES(?,?,?,?,?,?)', R); c.executemany('INSERT INTO row_tags VALUES(?,?,?)', RT)
    c.executemany('INSERT INTO records_pairs VALUES(?,?,?,?)', PR); c.executemany('INSERT INTO records_compound VALUES(?,?,?)', CP)
    c.commit()
    print('rows', len(R), 'tags', len(RT), 'crossing', sum(x[2] for x in RT), 'pairs', len({(a, b, d) for a, _, b, d in PR}),
          'compounds', collections.Counter(k for _, k, _ in CP))

if __name__ == '__main__': main(sys.argv[1])
