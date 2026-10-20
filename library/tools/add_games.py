"""Insert-only loading (20 Oct 2026): adding games only adds rows; the library's existing rows are never rewritten.
  prepare <work.sqlite> <game> [...]   the work copy keeps only the shared tables (concepts, patterns, archetypes ...): every
                                       other game is dropped, and a placeholder row keeps new entry ids above the library's
  copy <out.sqlite> <work.sqlite> <game> [...]
                                       after the build steps ran on the work copy, its rows of the new games are inserted into
                                       the library (entries, tags, pairs, links, merges, repeats, tree records, per-game rows)
  verify <out.sqlite> <in.sqlite>      every row the input had is in the output unchanged (entries, tags, pairs, links); stops
                                       the build otherwise
build.sh runs these when it is given load files. The games must not be in the library yet (drop_game.py first to reload one)."""
import os, sqlite3, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
cmd, db = sys.argv[1], sys.argv[2]
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
SENTINEL = '_add_games_placeholder'
if cmd == 'prepare':
    games = set(sys.argv[3:])
    have = {g for (g,) in q('SELECT DISTINCT game FROM entities')}
    if games & have: sys.exit(f'already in the library: {sorted(games & have)} (drop_game.py first)')
    top = q('SELECT max(id) FROM entities')[0][0]
    c.close()
    for g in sorted(have): subprocess.run([sys.executable, '-I', os.path.join(HERE, 'drop_game.py'), db, g], check=True, stdout=subprocess.DEVNULL)
    c = sqlite3.connect(db)
    c.execute("INSERT INTO entities(id, game, name, category) VALUES(?,?,?,?)", (top, SENTINEL, SENTINEL, 'tribe')); c.commit()
    print('work copy: shared tables only, new ids start after', top)
elif cmd == 'copy':
    work, games = sys.argv[3], sys.argv[4:]
    c.execute('ATTACH ? AS w', (work,))
    gl = ','.join('?' * len(games))
    c.execute(f"CREATE TEMP TABLE new_ids AS SELECT id FROM w.entities WHERE game IN ({gl})", games)
    cols = lambda t: ','.join(r[1] for r in q(f'PRAGMA main.table_info({t})'))
    n = {}
    def put(t, cond):
        if not q("SELECT 1 FROM w.sqlite_master WHERE name=?", t) or not q("SELECT 1 FROM main.sqlite_master WHERE name=?", t): return
        verb = 'INSERT OR REPLACE' if t == 'merged_entities' else 'INSERT'   # a reload keeps the game's merge records; the new build may write them again
        n[t] = c.execute(f"{verb} INTO main.{t}({cols(t)}) SELECT {cols(t)} FROM w.{t} WHERE {cond}", games if '?' in cond else ()).rowcount
    put('entities', f"game IN ({gl})")
    for t in ('entity_concepts', 'trigger_effect', 'tree_v3_moved', 'tree_v3_added'): put(t, 'entity IN (SELECT id FROM temp.new_ids)')
    put('entity_links', 'src IN (SELECT id FROM temp.new_ids) AND dst IN (SELECT id FROM temp.new_ids)')
    for t in ('merged_entities', 'mechanic_repeat', 'load_log', 'factions', 'concept_patterns', 'v2_concept_patterns', 'pattern_fixes'): put(t, f"game IN ({gl})")
    put('games', f"id IN ({gl})")
    c.commit(); print('inserted:', ', '.join(f'{t} {k}' for t, k in n.items()))
elif cmd == 'verify':
    c.execute('ATTACH ? AS i', (sys.argv[3],))
    bad = {}
    for t in ('entities', 'entity_concepts', 'trigger_effect', 'entity_links'):
        cs = ','.join(r[1] for r in q(f'PRAGMA i.table_info({t})'))
        bad[t] = q(f'SELECT count(*) FROM (SELECT {cs} FROM i.{t} EXCEPT SELECT {cs} FROM main.{t})')[0][0]
    if any(bad.values()): sys.exit(f'old rows changed or missing: {bad}')
    print('old rows unchanged:', ', '.join(f'{t} ok' for t in bad))
