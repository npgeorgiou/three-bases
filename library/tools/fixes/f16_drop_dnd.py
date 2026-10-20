"""One-time fix of 20 Oct 2026: D&D 5e is removed from the library (Kaptain's decision: its tags were the least precise and it
is not a card or board game). Deletes every D&D entry, every row that points at one, and the game's per-game rows. Run on an
expanded database (compact_text.py expand; compacting again rebuilds the text notes, so unused ones go) and follow it with
the build's last steps (signature, precision, finalize, checks, compact). Usage: f16_drop_dnd.py <db>"""
import sqlite3, sys
G = 'dnd5e'
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
tables = {t for t, in q("SELECT name FROM sqlite_master WHERE type='table'")}
c.execute('CREATE TEMP TABLE gone AS SELECT id FROM entities WHERE game=?', (G,))
n = {}
def run(name, sql, *a):
    if name.split()[0] in tables: n[name] = c.execute(sql, a).rowcount
run('entity_concepts', 'DELETE FROM entity_concepts WHERE entity IN (SELECT id FROM gone)')
run('trigger_effect', 'DELETE FROM trigger_effect WHERE entity IN (SELECT id FROM gone) OR game=?', G)
run('entity_links', 'DELETE FROM entity_links WHERE src IN (SELECT id FROM gone) OR dst IN (SELECT id FROM gone)')
run('mechanic_repeat', 'DELETE FROM mechanic_repeat WHERE entity IN (SELECT id FROM gone) OR same_as IN (SELECT id FROM gone) OR game=?', G)
run('merged_entities', 'DELETE FROM merged_entities WHERE kept_id IN (SELECT id FROM gone) OR game=?', G)
run('tree_v3_moved', 'DELETE FROM tree_v3_moved WHERE entity IN (SELECT id FROM gone)')
run('tree_v3_added', 'DELETE FROM tree_v3_added WHERE entity IN (SELECT id FROM gone)')
for t in ['faction_signature', 'factions', 'faction_archetypes', 'load_log', 'concept_precision', 'concept_patterns',
          'v2_concept_patterns', 'pattern_fixes']:
    run(t, 'DELETE FROM %s WHERE game=?' % t, G)
run('games', 'DELETE FROM games WHERE id=?', G)
run('entities', 'DELETE FROM entities WHERE id IN (SELECT id FROM gone)')
c.commit()
print('deleted:', ', '.join('%s %d' % kv for kv in n.items()))
