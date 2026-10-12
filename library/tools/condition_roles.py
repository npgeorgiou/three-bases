"""Condition-aware D&D keywords (README suggestion 6). D&D conditions (Blinded ... Unconscious) were linked to entries only as
has_keyword / grants_keyword, and entries inherited the condition's concepts as 'does', so a spell that ENDS Frightened looked
like one that CAUSES it. Each sentence that names a condition is read (Claude's wording rules) and the link is replaced by:
  inflicts_keyword   the entry gives the condition to a target ("the target has the Poisoned condition", "or fall Prone")
  counters_keyword   immunity, protection, ending or curing it ("immune to", "advantage on saving throws against", "ends")
  suffers_keyword    the entry's user gets it as a price ("you have the Incapacitated condition")
  benefits_keyword   it profits from a target that has it ("attack rolls against a Paralyzed creature")
  mentions_keyword   none of these
The condition's own concepts (debuff, disable, control, fatigue ...) are inherited with the matching role:
inflicts -> does, counters -> counters, suffers -> cost, benefits -> benefits (method via_keyword). Inherited 'does' tags,
and text_pattern 'does' tags whose evidence is the condition's own wording, are removed from entries that never inflict it.
Usage: condition_roles.py <db>"""
import re, sqlite3, sys, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
G = 'dnd5e'
CONDS = ['Blinded', 'Charmed', 'Deafened', 'Exhaustion', 'Frightened', 'Grappled', 'Incapacitated', 'Invisible', 'Paralyzed',
         'Petrified', 'Poisoned', 'Prone', 'Restrained', 'Stunned', 'Unconscious']
FORMS = {'Exhaustion': r'exhaust(ion|ed)', 'Invisible': r'invisible', 'Frightened': r'frighten(ed)?', 'Charmed': r'charm(ed)?'}
kid = dict(q("SELECT name, id FROM entities WHERE game=? AND category='keyword' AND name IN (%s)" % ','.join('?' * len(CONDS)), G, *CONDS))
kcon = {k: [x for (x,) in q("SELECT concept FROM entity_concepts WHERE entity=? AND role='does'", i)] for k, i in kid.items()}
SENT = re.compile(r'(?<=[.!?])\s+|\n+|•')

def rules(C):
    return [
     ('counters', re.compile(r"\bimmun\w* to[^.]{0,100}\b" + C + r"|\bcan'?t be " + C + r"|\bcannot be " + C + r"|\bisn'?t " + C + r"|advantage on[^.]{0,60}saving throws[^.]{0,10}(against|to avoid|to end)[^.]{0,100}" + C +
                              r"|\b(ends?|ending|removes?|suppress\w*|cures?|lift\w*|reduce\w*|neither|nor)\b[^.,]{0,60}\b" + C + r"|\bceases? to be " + C + r"|\bno longer\b[^.]{0,40}\b" + C +
                              r"|\b" + C + r"\b[^.]{0,20}condition (ends|is removed)|\bcondition immunities\b[^.]{0,80}" + C, re.I)),
     (None, re.compile(r"\b(doesn'?t|don'?t|aren'?t|not|unless|without)\b[^.]{0,20}\b(have the |has the |be |is )?" + C + r"\b", re.I)),
     ('benefits', re.compile(r"\b(that|who|which) (is|are|has|have)\b[^.]{0,40}\b" + C + r"\b", re.I)),
     ('suffers', re.compile(r"\byou (have|are|fall|become|gain)[^.]{0,15}(the )?" + C + r"\b", re.I)),
     ('inflicts', re.compile(r"(target|creature|it|they|them|each|enemy|foe|that creature|the creature|victim|opponent|anyone|those)[^.]{0,50}\b(has|have|gains?|is|are|falls?|becomes?|be|knocked|is knocked)\b[^.]{0,20}\b(the )?" + C + r"\b"
                              r"|\bor (be|have the|become|fall|is|are)[^.]{0,12}" + C + r"\b|\bknocks?[^.]{0,40}\bprone\b|\b(inflicts?|imposes?|causes?)[^.]{0,30}" + C + r"\b"
                              r"|\b(gain|gains|suffer|suffers)[^.]{0,10}\d? ?(levels? of )?exhaustion\b", re.I)),
     ('benefits', re.compile(r"\b(against|while|if|whenever|when)\b[^.]{0,60}\b(is|are|has the|have the|that has the|that is|that are)\b[^.]{0,6}" + C + r"\b|\b" + C + r" (creature|target|foe|enemy|ally|ones?)\b|\b(attacks?|attack rolls?) against[^.]{0,30}" + C, re.I))]
R = {k: rules(FORMS.get(k, k.lower())) for k in CONDS}
REL = {'inflicts': 'inflicts_keyword', 'counters': 'counters_keyword', 'suffers': 'suffers_keyword', 'benefits': 'benefits_keyword', None: 'mentions_keyword'}
ROLE = {'inflicts': 'does', 'counters': 'counters', 'suffers': 'cost', 'benefits': 'benefits'}
ids = ','.join(map(str, kid.values()))
links = q(f"SELECT l.src, l.dst, l.rel FROM entity_links l JOIN entities x ON x.id=l.src WHERE x.game=? AND x.category NOT IN ('keyword','tribe') AND l.dst IN ({ids}) AND l.rel IN ('has_keyword','grants_keyword','mentions_keyword','inflicts_keyword','counters_keyword','suffers_keyword','benefits_keyword')", G)
name_of = {v: k for k, v in kid.items()}
found = collections.defaultdict(set)
for src, dst, rel in links: found[src, dst]
text = dict(q("SELECT id, text FROM entities WHERE game=?", G))
for (src, dst) in list(found):
    k = name_of[dst]; C = re.compile(r'\b' + FORMS.get(k, k.lower()) + r'\b', re.I)
    for s in SENT.split(text.get(src) or ''):
        if not C.search(s): continue
        role = next((r for r, rx in R[k] if rx.search(s)), None)
        found[src, dst].add(role)
cnt = collections.Counter()
for (src, dst), roles in found.items():
    real = roles - {None}
    c.execute(f"DELETE FROM entity_links WHERE src=? AND dst=? AND rel IN ('has_keyword','grants_keyword','mentions_keyword','inflicts_keyword','counters_keyword','suffers_keyword','benefits_keyword')", (src, dst))
    for r in (real or {None}):
        c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (src, REL[r], dst, 'condition role (condition_roles.py)')); cnt[REL[r]] += 1
# concepts: rebuild the inherited ones by role (first remove what an earlier run inherited)
for r in ROLE:
    for k in CONDS: c.execute("DELETE FROM entity_concepts WHERE method='via_keyword' AND evidence=?", (f'{r} {k}',))
inflicted = collections.defaultdict(set)
for (src, dst), roles in found.items():
    for r in roles - {None}:
        for con in kcon[name_of[dst]]:
            if r == 'inflicts': inflicted[src].add(con)
            c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (src, con, ROLE[r], 'via_keyword', f'{r} {name_of[dst]}'))
drop = 0
words = re.compile(r'\b(' + '|'.join(FORMS.get(k, k.lower()) for k in CONDS) + r')\b', re.I)
for src in {s for s, _ in found}:
    cons = {con for (s, d) in found if s == src for con in kcon[name_of[d]]} - inflicted[src]
    other = {x for (x,) in q(f"SELECT ec.concept FROM entity_links l JOIN entity_concepts ec ON ec.entity=l.dst AND ec.role='does' WHERE l.src=? AND l.dst NOT IN ({ids}) AND l.rel IN ('has_keyword','grants_keyword','mentions_keyword')", src)}
    for con in cons:
        if con not in other: drop += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND role='does' AND method='via_keyword'", (src, con)).rowcount
        for ev, in q("SELECT evidence FROM entity_concepts WHERE entity=? AND concept=? AND role='does' AND method='text_pattern'", src, con):
            if ev and words.search(ev): drop += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND role='does' AND method='text_pattern'", (src, con)).rowcount
c.commit()
print('condition links:', dict(cnt), ' wrong does-tags removed:', drop)
