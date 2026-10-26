"""Tags from the cost field (method data_rule) for games whose cards print the cost apart from the text, so no wording pattern can
read it. Per game: a regex on entities.cost and the concepts and roles it gives. Inscryption: Blood is paid by sacrificing your own
creatures; Bones and Mox gems are payments other than the usual resource; Energy refills each turn like mana and gets no tag (Claude's
reading). Usage: cost_rules.py <db>"""
import re, sqlite3, sys
RULES = {
    'inscryption': [
        (r'\bblood\b', [('sacrifice', 'cost')], 'cost paid in Blood: sacrifice your own creatures'),
        (r'\bbones?\b', [('cost_type', 'cost')], 'cost paid in Bones'),
        (r'\bmox\b', [('cost_type', 'cost')], 'cost paid in Mox gems'),
    ],
}
c = sqlite3.connect(sys.argv[1]); n = 0
for g, rules in RULES.items():
    for e, cost in c.execute("SELECT id, cost FROM entities WHERE game=? AND cost IS NOT NULL AND category NOT IN ('keyword','tribe')", (g,)).fetchall():
        for rx, tags, why in rules:
            if re.search(rx, cost, re.I):
                for con, role in tags:
                    n += c.execute('INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)', (e, con, role, 'data_rule', f'{why} ({cost})')).rowcount
c.commit(); print('cost rules: tags', n)
