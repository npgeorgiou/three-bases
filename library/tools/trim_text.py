"""Cut text that carries no mechanic out of entries (Kaptain, 26 Oct 2026). Run on an expanded database (compact_text.py expand):
the tags keep their evidence as text, and compact_text.py compact afterwards stores evidence the trimmed text no longer holds as
a note, so no tag is lost.
  inscryption  every entry keeps its first paragraph (the rulebook line); the wiki prose after it goes
  wh_40k_10e   the lists of special rules and weapon abilities (the unit keeps them as keyword links) and designer's notes go
Usage: trim_text.py <db>"""
import re, sqlite3, sys
RULES = {
    'inscryption': [(r'\n\s*\n.*', re.S)],
    'wh_40k_10e': [(r"\s*Special rules:[^.]*(?:\.|$)", 0), (r"\s*(?:[A-Z][\w'’ -]{0,40} )?Weapon abilities:[^.]*(?:\.|$)", 0),
                   (r"\s*Designer[’']s Note:[^\n]*", 0)],
}
c = sqlite3.connect(sys.argv[1]); n = {}
for g, rules in RULES.items():
    for i, t in c.execute('SELECT id, text FROM entities WHERE game=? AND text IS NOT NULL', (g,)).fetchall():
        s = t
        for rx, fl in rules: s = re.sub(rx, '', s, flags=fl)
        s = s.strip()
        if s != t: c.execute('UPDATE entities SET text=? WHERE id=?', (s, i)); n[g] = n.get(g, 0) + 1
c.commit(); print('trimmed:', n)
