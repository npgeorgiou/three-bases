"""Remove a game from the library: every entry of the game, every row that points at one, and the game's per-game rows.
Used to drop a game, or to reload one: drop it from the input, then build with its load files, so its entries are new and get
the current patterns. Run on an expanded database (compact_text.py expand).
Usage: drop_game.py <db> <game> [--reload]   --reload (reload_game.sh, ids kept): links to other games' entries and the game's
merged_entities rows stay, as they are still right when the entries come back with the same ids."""
import sqlite3, sys
G = sys.argv[2]; RELOAD = sys.argv[3:] == ['--reload']
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
tables = {t for t, in q("SELECT name FROM sqlite_master WHERE type='table'")}
c.execute('CREATE TEMP TABLE gone AS SELECT id FROM entities WHERE game=?', (G,))
n = {}
def run(name, sql, *a):
    if name.split()[0] in tables: n[name] = c.execute(sql, a).rowcount
run('entity_concepts', 'DELETE FROM entity_concepts WHERE entity IN (SELECT id FROM gone)')
run('trigger_effect', 'DELETE FROM trigger_effect WHERE entity IN (SELECT id FROM gone) OR game=?', G)
run('entity_links', 'DELETE FROM entity_links WHERE src IN (SELECT id FROM gone) AND dst IN (SELECT id FROM gone)' if RELOAD else
    'DELETE FROM entity_links WHERE src IN (SELECT id FROM gone) OR dst IN (SELECT id FROM gone)')
run('mechanic_repeat', 'DELETE FROM mechanic_repeat WHERE entity IN (SELECT id FROM gone) OR same_as IN (SELECT id FROM gone) OR game=?', G)
if not RELOAD: run('merged_entities', 'DELETE FROM merged_entities WHERE kept_id IN (SELECT id FROM gone) OR game=?', G)
for t in ['base_tags', 'base_pairs']:   # the frozen base (full form, indexes.py create)
    run(t, 'DELETE FROM %s WHERE entity IN (SELECT id FROM gone)' % t)
if not RELOAD: run('base_patterns', 'DELETE FROM base_patterns WHERE game=?', G)
run('tree_v3_moved', 'DELETE FROM tree_v3_moved WHERE entity IN (SELECT id FROM gone)')
run('tree_v3_added', 'DELETE FROM tree_v3_added WHERE entity IN (SELECT id FROM gone)')
for t in ['faction_signature', 'faction_concept_ov', 'factions', 'faction_archetypes', 'load_log', 'concept_precision', 'concept_patterns',
          'v2_concept_patterns', 'pattern_fixes']:
    run(t, 'DELETE FROM %s WHERE game=?' % t, G)
run('games', 'DELETE FROM games WHERE id=?', G)
run('entities', 'DELETE FROM entities WHERE id IN (SELECT id FROM gone)')
c.commit()
print('deleted:', ', '.join('%s %d' % kv for kv in n.items()))
