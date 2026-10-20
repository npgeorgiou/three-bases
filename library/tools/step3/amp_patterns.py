"""Amplifiers: cards that make more of what other cards do (asked by Kaptain, 20 Oct 2026; script only, no readers).
The wording comes from the cards: step3/amp_patterns.py scan groups every amplifying word family (double, twice, triple, extra,
additional, more, plus, that many, increase...) by the phrase around it in every game; the amplifier forms below are the groups
that are amplifiers (Claude read them), with the games they occur in:
  F1  "... trigger(s) / activate(s) an extra time / twice"        Magic, Hearthstone, Battlegrounds, Shadowverse, Runeterra, Duelyst
  F2  "twice / three times that many"                              Magic
  F3  "that many plus one", "those tokens plus", "plus an additional" Magic, Gwent, Underworlds, Slay the Spire 2
  F4  "double the number / amount of", "double all"                              Magic, Kill Team, Age of Sigmar, Shadowverse, Gwent, 40k
  F5  "... are / is doubled" (not "this card's / its")             Runeterra, Hearthstone, Marvel Snap, Slay the Spire 2...
  F6  "shuffle / plant / summon / create / add ... an extra / additional copy / one" (other cards' effect, after "whenever / when")
  F7  "deals double / twice that damage"                           Magic
  F8  "that much damage / life plus"                               Magic
  F9  "attack or defense is increased by an effect"                Shadowverse (a payoff for being buffed: buff only, its own line)
  F10 "your / allied / friendly ... deal / gain / restore N more / extra"  Hearthstone, Runeterra, Slay the Spire, Battlegrounds...
The thing amplified is read from the same sentence and the card gets that concept with role 'benefits' (it pays off when other
cards do it), which links it to every card that does it. F1 also gives repeat_trigger (its definition: a trigger happens again).
  amp_patterns.py scan [db]    the phrase groups (counts per game, two examples each) -> step3/amp_scan.txt
  amp_patterns.py check [db]   per concept and game: matches, and 20 random matches for Claude to read
  amp_patterns.py write [db]   'new' lines (marked |amp) into decisions.tsv, except pairs in DROP"""
import collections, os, random, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import patterns3 as P
FORM = (r"(?:\b(?:trigger|triggers|activate|activates|resolve|resolves|take effect|takes effect)\s+(?:an? (?:extra|additional) time|twice|two times)\b"
        r"|\b(?:twice|three times) that many\b|\bthat many plus (?:one|\d+)\b|\bthose tokens plus\b|\bplus an additional\b"
        r"|\bdouble (?:the )?(?:number|amount|value) of\b|\bdouble all\b|\bdouble (?:the |an? )?(?:enemy's |target's |its |their )?(?:poison|burn|doom)\b|(?<!this card's )(?<!its )(?<!this minion's )(?<!this unit's )\b(?:are|is) doubled\b"
        r"|\b(?:whenever|when|each time|if)\b[^.\n]{0,50}?\b(?:shuffle|plant|summon|create|add|put)s?\b[^.\n]{0,40}?\b(?:an?|one) (?:extra|additional) (?:copy|one)\b"
        r"|\bdeals? (?:double|twice) (?:that|the) (?:damage|much)\b|\bthat much (?:damage|life|healing|armor|block) plus\b"
        r"|\b(?:your|allied|friendly|other)\b[^.\n]{0,30}?\b(?:deal|deals|gain|gains|restore|restores|get|gets)\s+(?:\d+|an?)\s+(?:more|additional|extra)\b)")
OBJ = {   # concept: words in the same sentence that name what is amplified
    'summon': r"\btokens?\b|\bsummon",
    'buff': r"\bcounters?\b|\battack or defense\b|\bdefense or attack\b|\bstats?\b",
    'damage': r"\bdamage\b(?! to (?:itself|you)\b)(?! against this unit)(?![^.\n]{0,40}?\b(?:that many cards|is doubled))",   # not its own damage
    'heal': r"\bheal(?:ing|s)?\b|\blife\b|\bhealth\b",
    'block_armor': r"\barmor\b(?! class)|\bblock\b",
    'trap_secret': r"\btraps?\b|\bsecrets?\b",
    'draw': r"\bdraws?\b|\bcards? drawn\b",
    'deck_modification': r"\bwhenever you shuffle\b",
    'damage_over_time': r"\bpoison\b|\bburn\b|\bdoom\b",
    'death_trigger': r"\bdeathrattles\b|\blast words effects\b|\bdeathwish effects\b",
    'on_play': r"\bbattlecries\b|\bfanfares\b|\bon reveal abilities\b|\bplay skills\b",
    'turn_end': r"\bend of turn effects\b|\bround end effects\b",
    'turn_start': r"\bstart of turn effects\b|\bround start effects\b",
    'resource_gain': r"\bmana\b(?! value)|\btreasures?\b",
}
SENT = r"[^.\n]{0,40}?"   # the amplified thing sits next to the amplifying words
def patterns():
    out = [('buff', 'benefits', r"\b(?:attack|defense) (?:or (?:attack|defense) )?(?:is|are) increased by an effect\b"),   # F9: a payoff for being buffed
           ('repeat_trigger', 'does', r"\b(?:trigger|triggers|activate|activates|resolve|resolves)\s+(?:an? (?:extra|additional) time|twice|two times)\b")]
    for k, o in OBJ.items():
        out.append((k, 'benefits', r"(?:" + FORM + r")" + SENT + r"(?:" + o + r")|(?:" + o + r")" + SENT + r"(?:" + FORM + r")"))
    return out
DROP = set()   # (concept, game) pairs Claude judged wrong after 'check'
mode = sys.argv[1]; db = sys.argv[2] if len(sys.argv) > 2 else P.DB
c = sqlite3.connect(db)
ents = collections.defaultdict(list)
for i, g, n, t in c.execute('SELECT id, game, name, text FROM entities WHERE text IS NOT NULL'): ents[g].append((n, P.norm_text(g, n, t)))
if mode == 'scan':
    W = r"(?:double[sd]?|twice|triple[sd]?|extra|additional(?:ly)?|again|one more|\d+ more|that many|that much|plus (?:one|that|an?|\d+)|increase[sd]?)"
    R = re.compile(r"((?:\S+\s+){0,3})(" + W + r")((?:\s+\S+){0,4})", re.I)
    grp = collections.defaultdict(lambda: [collections.Counter(), []])
    for g, es in ents.items():
        for n, t in es:
            for m in R.finditer(t.replace('\n', ' ')):
                key = re.sub(r'\d+', 'N', m.group(2).lower()) + ' | ' + ' '.join(re.sub(r'\d+', 'N', m.group(3)).split()[:2]).strip(' .,;:')
                grp[key][0][g] += 1
                if len(grp[key][1]) < 2: grp[key][1].append(f'{n[:18]}: ...{m.group(0)[:80]}...')
    with open(os.path.join(HERE, 'amp_scan.txt'), 'w', encoding='utf-8') as fh:
        for k, (cnt, ex) in sorted(grp.items(), key=lambda x: -sum(x[1][0].values())):
            fh.write(f'{sum(cnt.values()):5}  {k:34} {", ".join(f"{g} {v}" for g, v in cnt.most_common(4))}\n        {" || ".join(ex)[:170]}\n')
    print('phrase groups', len(grp)); sys.exit(0)
lines = []
for k, role, p in patterns():
    r = re.compile(p, re.I); hits = []
    for g, es in sorted(ents.items()):
        m = [(n, t) for n, t in es if r.search(t)]
        if not m: continue
        if mode == 'check': print(f'{k:18} {g:18} matches {len(m):4}')
        hits += [(g, n, t) for n, t in m]
        if (k, g) not in DROP: lines.append(f'new\t{k}|{role}|{g}|amp\t{g}\t{p}')
    if mode == 'check':
        for g, n, t in random.Random(1).sample(hits, min(20, len(hits))):
            mm = r.search(t); print(f'     {g[:10]:10} {n[:22]:22} ...{t[max(0, mm.start() - 20): mm.end() + 15]}...'.replace('\n', ' '))
if mode == 'write':
    D = os.path.join(HERE, 'decisions.tsv')
    keep = [l for l in open(D, encoding='utf-8') if not (l.startswith('new\t') and l.split('\t')[1].endswith('|amp')) and not l.startswith('# amp_patterns')]
    keep.append('# amp_patterns.py: amplifiers (cards that make more of what other cards do) benefit from what they amplify\n')
    open(D, 'w', encoding='utf-8').writelines(keep + [l + '\n' for l in lines])
    print('amplifier lines', len(lines))
