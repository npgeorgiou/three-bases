"""Text clean-up (leftovers of the source formats). Usage: f04_text.py <db>
  - Hearthstone / Battlegrounds: hsdata placeholders. An entry whose text is only placeholders ("{0} {1}": the game fills it
    in) has no rules text and goes, as the first build dropped entries without text; in other texts {n} becomes X,
    "@..." alternative text is cut, "|4(card, cards)" becomes "cards", and "_" (hsdata's non-breaking space) becomes a space.
  - D&D and Kill Team: words split at a PDF line break ("Ar- mor") are joined ("6th- level" -> "6th-level").
  - Slay the Spire: a leading "Keywords: X." repeated in the text is removed; a keyword not in the text moves to the end.
  - Wiki markup (Inscryption, Into the Breach, Gwent): list stars, table rows and [link text] brackets are removed."""
import re, sqlite3, sys, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
C = collections.Counter()
def drop(i):
    for st in ("DELETE FROM entity_concepts WHERE entity=?", "DELETE FROM trigger_effect WHERE entity=?", "DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM entities WHERE id=?"):
        c.execute(st, (i,) * st.count('?'))
def put(i, t, old, why):
    if t != old: c.execute("UPDATE entities SET text=? WHERE id=?", (t, i)); C[why] += 1
for i, g, t in q("SELECT id, game, text FROM entities WHERE game IN ('hearthstone','hs_battlegrounds') AND text IS NOT NULL"):
    if re.search(r'\{\d\}', t) and not re.sub(r'\{\d\}|\s', '', t): drop(i); C['hearthstone placeholder-only entry removed'] += 1; continue
    n = t
    if re.search(r'\{\d\}', n):
        n = n.split('@')[0] if '@' in n and re.search(r'\{\d\}', n.split('@', 1)[1]) else n
        n = re.sub(r'\{\d\}/\{\d\}', 'X/X', n); n = re.sub(r'\ba\{\d\} \{\d\}', 'an X/X', n); n = re.sub(r'\{\d\}', 'X', n)
    n = re.sub(r'\|4\(([^,()]+), ?([^()]+)\)', r'\2', n)
    n = re.sub(r'(?<=\w)_(?=[\w(])', ' ', n).replace(' _', ' ')
    put(i, re.sub(r'\s+', ' ', n).strip(), t, 'hearthstone text cleaned')
STOP = {'the', 'a', 'an', 'and', 'or', 'of', 'to', 'in', 'on'}
for i, g, t in q("SELECT id, game, text FROM entities WHERE game IN ('dnd5e','wh_killteam') AND text GLOB '*[a-z]- [a-z]*'"):
    def j(m):
        a, b = m.group(1), m.group(2)
        if b.lower() in STOP: return a + ' ' + b
        if re.search(r'\d(st|nd|rd|th)$', a) or g == 'wh_killteam': return a + '-' + b
        return a + b
    put(i, re.sub(r'\b(\w+)- ([a-z]\w*)', j, t), t, 'line-break hyphen joined')
for i, t in q("SELECT id, text FROM entities WHERE game IN ('sts1','sts2') AND text LIKE 'Keywords:%'"):
    m = re.match(r'Keywords:\s*([^.]*)\.\s*', t)
    if not m: continue
    rest = t[m.end():]; ks = [k.strip() for k in m.group(1).split(',') if k.strip()]
    missing = [k for k in ks if not re.search(r'\b' + re.escape(k) + r'\b', rest)]
    put(i, (rest + (' ' + ' '.join(k + '.' for k in missing) if missing else '')).strip(), t, 'slay the spire keyword prefix removed')
for i, t in q("SELECT id, text FROM entities WHERE game IN ('inscryption','into_the_breach','gwent') AND (text LIKE '%**%' OR text LIKE '%|-%' OR text LIKE '%[http%' OR text LIKE '%* %')"):
    n = re.sub(r'\[https?://\S+ ([^\]]+)\]', r'\1', t)
    n = re.sub(r'(?m)^\s*(\{\||\|\}|\|-|!.*\|\|.*)\s*$', '', n)
    n = re.sub(r'(?m)^\s*\*+\s*', '- ', n); n = re.sub(r'\s\*\*\s', ' ', n); n = n.replace('**', '')
    put(i, re.sub(r'\n{3,}', '\n\n', n).strip(), t, 'wiki markup removed')
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit(); print(dict(C))
